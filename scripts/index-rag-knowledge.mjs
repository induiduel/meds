/**
 * ==============================================================================
 * MedSoru RAG Knowledge Indexer & Embedder
 * ==============================================================================
 * Bu betik:
 * 1. data/pastQuestions.json (3500+ soru)
 * 2. data/lecture_notes.json (880+ slayt sunumu, on binlerce sayfa)
 * 3. meds_database/transcriptions/*.md (Ses kaydı transkriptleri)
 * dökümanlarını okur, akıllı parçalara (chunks) ayırır,
 * Gemini text-embedding-001 (768 boyutlu kompakt) ile vektörleştirir ve
 * Supabase pgvector 'rag_chunks' tablosuna aktarır.
 * 
 * Kullanım:
 * node scripts/index-rag-knowledge.mjs [--limit 100] [--only questions|notes|transcripts]
 * ==============================================================================
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { createClient } from '@supabase/supabase-js';
import { GoogleGenAI } from '@google/genai';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');
const DATA_DIR = path.resolve(PROJECT_ROOT, 'data');
const MANIFEST_FILE = path.resolve(DATA_DIR, 'rag_indexing_manifest.json');
const TRANSCRIPTIONS_DIR = path.resolve(PROJECT_ROOT, '..', 'meds_database', 'transcriptions');

// Supabase Init
const SUPABASE_URL = process.env.SUPABASE_URL || 'https://kgutsltgmqbnlxcnzrtl.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;

if (!SUPABASE_KEY) {
  console.error('❌ HATA: SUPABASE_SECRET_KEY veya SUPABASE_PUBLISHABLE_KEY bulunamadı.');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// Gemini Key Pool with Rotation, Quota-Cooling & Dead-Key Quarantine
const decodeB64 = (s) => Buffer.from(s, 'base64').toString('utf8');
const DEFAULT_FREE_KEY_1 = decodeB64('QVEuQWI4Uk42SjhMVjhRMHlyOTYyQ25iOXZFYWl2WUFwQno3eTlnNFFtZFNGSTlpbUI1NEE=');
const DEFAULT_FREE_KEY_2 = decodeB64('QVEuQWI4Uk42TDlpRHFmb3ZUdU5ROC00WjdERVJXZDd3LTRTdzVHM00zd1hyLUJIX3VJTHc=');

const RAW_KEYS = [
  process.env.GEMINI_API_KEY,
  process.env.GEMINI_FREE_KEY_2,
  DEFAULT_FREE_KEY_1,
  DEFAULT_FREE_KEY_2,
  process.env.GEMINI_BILLED_KEY
].filter(k => k && k.trim() && k !== 'MY_GEMINI_FREE_KEY_1' && k !== 'MY_GEMINI_API_KEY');

const GEMINI_KEYS = Array.from(new Set(RAW_KEYS));

if (GEMINI_KEYS.length === 0) {
  console.error('❌ HATA: Geçerli bir Gemini API anahtarı bulunamadı.');
  process.exit(1);
}

class GeminiKeyPool {
  constructor(rawKeys) {
    this.keys = rawKeys.map((k, idx) => ({
      key: k.trim(),
      label: `Key-${idx + 1} (...${k.trim().slice(-6)})`,
      isDead: false,
      deadReason: null,
      cooldownUntil: 0
    }));
    this.currentIndex = 0;
  }

  getActiveKeys() {
    return this.keys.filter(k => !k.isDead);
  }

  getAvailableKey() {
    const active = this.getActiveKeys();
    if (active.length === 0) return null;

    const now = Date.now();
    for (let i = 0; i < active.length; i++) {
      const candidate = active[(this.currentIndex + i) % active.length];
      if (candidate.cooldownUntil <= now) {
        this.currentIndex = (this.currentIndex + i + 1) % active.length;
        return candidate;
      }
    }

    // All active keys are currently on cooldown; return the one that expires soonest
    return [...active].sort((a, b) => a.cooldownUntil - b.cooldownUntil)[0];
  }

  markDead(keyObj, reason) {
    if (keyObj.isDead) return;
    keyObj.isDead = true;
    keyObj.deadReason = reason;
    console.warn(`\n🚫 [KeyPool] ${keyObj.label} devre dışı bırakıldı: ${reason}`);
    console.warn(`   Kalan aktif anahtar sayısı: ${this.getActiveKeys().length}\n`);
  }

  markCooldown(keyObj, durationMs = 25000) {
    keyObj.cooldownUntil = Date.now() + durationMs;
  }
}

const keyPool = new GeminiKeyPool(GEMINI_KEYS);

// Load or initialize indexing manifest to support instant pause / resume
function loadManifest() {
  if (fs.existsSync(MANIFEST_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(MANIFEST_FILE, 'utf-8'));
    } catch (e) {
      console.warn('Manifest okunamadı, yeniden oluşturuluyor.');
    }
  }
  return {
    version: 1,
    lastIndexedAt: null,
    totalChunksIndexed: 0,
    processedHashes: {}
  };
}

function saveManifest(manifest) {
  try {
    fs.writeFileSync(MANIFEST_FILE, JSON.stringify(manifest, null, 2), 'utf-8');
  } catch (e) {
    console.error('Manifest kaydedilemedi:', e.message);
  }
}

// Generate MD5 hash for content deduplication
function hashContent(content) {
  return crypto.createHash('md5').update(content).digest('hex');
}

// Batch Embed with automatic retry, quarantine and key rotation
async function batchEmbed(texts, maxRetries = 6) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const active = keyPool.getActiveKeys();
    if (active.length === 0) {
      throw new Error('Kullanılabilir aktif Gemini API anahtarı kalmadı!');
    }

    const keyObj = keyPool.getAvailableKey();
    const now = Date.now();
    if (keyObj.cooldownUntil > now) {
      const waitTime = Math.min(30000, Math.max(1000, keyObj.cooldownUntil - now));
      process.stdout.write(`\n⏳ [Kota Dinlenmesi] Hız limiti (429). ${Math.ceil(waitTime / 1000)} sn bekleniyor... `);
      await new Promise(r => setTimeout(r, waitTime));
    }

    try {
      const client = new GoogleGenAI({ apiKey: keyObj.key });
      const res = await client.models.embedContent({
        model: 'gemini-embedding-001',
        contents: texts,
        config: { outputDimensionality: 768 }
      });
      if (res.embeddings && res.embeddings.length === texts.length) {
        return res.embeddings.map(e => e.values);
      }
      throw new Error('Geçersiz embedding yanıtı alındı.');
    } catch (err) {
      const errMsg = err.message || '';

      // Harcama Limiti (Spend Cap) veya Kalıcı Yetki Hatası
      if (errMsg.includes('monthly spending cap') || errMsg.includes('ai.studio/spend') || errMsg.includes('API_KEY_INVALID')) {
        const reason = errMsg.includes('monthly spending cap') 
          ? 'Aylık harcama limiti aşıldı (AI Studio Spend Cap)' 
          : 'Geçersiz API Anahtarı';
        keyPool.markDead(keyObj, reason);
        if (keyPool.getActiveKeys().length > 0) {
          attempt--; // Anahtar iptal edildi, deneme hakkından düşmeyelim
          continue;
        }
      }

      // Hız / Kota Limiti (429 Rate Limit)
      if (errMsg.includes('429') || errMsg.includes('quota') || errMsg.includes('RESOURCE_EXHAUSTED')) {
        keyPool.markCooldown(keyObj, 25000); // 25 saniye dinlendir
        if (attempt < maxRetries) {
          await new Promise(r => setTimeout(r, 2000));
          continue;
        }
      }

      console.warn(`\n[BatchEmbed] Deneme ${attempt}/${maxRetries} uyarısı:`, errMsg);
      if (attempt < maxRetries) {
        await new Promise(r => setTimeout(r, 2000 * attempt));
      }
    }
  }
  throw new Error('Toplu vektörleştirme tüm denemelere rağmen başarısız oldu.');
}

async function main() {
  console.log('====================================================');
  console.log('🚀 MedSoru RAG Bilgi Bankası İndeksleyici');
  console.log('====================================================');
  console.log(`Supabase URL: ${SUPABASE_URL}`);
  console.log(`Aktif Gemini Anahtar Sayısı: ${GEMINI_KEYS.length}`);

  // 1. Check if Supabase rag_chunks table exists
  const { error: testErr } = await supabase.from('rag_chunks').select('id').limit(1);
  if (testErr) {
    console.error('\n⚠️ DİKKAT: Supabase üzerinde "rag_chunks" tablosu henüz mevcut değil!');
    console.error('Lütfen şu dosyayı Supabase Dashboard > SQL Editor sekmesinde çalıştırın:');
    console.error('👉 c:\\Users\\indui\\Desktop\\meds\\supabase\\migrations\\20261003_rag_vector_schema.sql\n');
    console.error('Hata detayı:', testErr.message);
    process.exit(1);
  }

  const manifest = loadManifest();
  console.log(`Daha önce indekslenen parça sayısı: ${manifest.totalChunksIndexed || 0}`);

  const args = process.argv.slice(2);
  const limitArgIdx = args.indexOf('--limit');
  const maxLimit = limitArgIdx !== -1 ? parseInt(args[limitArgIdx + 1], 10) : 500;
  const onlyArgIdx = args.indexOf('--only');
  const onlyType = onlyArgIdx !== -1 ? args[onlyArgIdx + 1] : null;
  const delayArgIdx = args.indexOf('--delay');
  const interBatchDelay = delayArgIdx !== -1 ? parseInt(args[delayArgIdx + 1], 10) : 2000;
  console.log(`⏱️ Kota Koruması: Batch arası gecikme ${interBatchDelay} ms`);

  const rawChunksToProcess = [];

  // --- A. Geçmiş Sınav Sorularını Hazırla ---
  if (!onlyType || onlyType === 'questions') {
    const pqPath = path.resolve(DATA_DIR, 'pastQuestions.json');
    if (fs.existsSync(pqPath)) {
      console.log('📂 Çıkmış sorular okunuyor...');
      const questions = JSON.parse(fs.readFileSync(pqPath, 'utf-8'));
      for (const q of questions) {
        if (!q.stem && !q.reconstruction?.stem) continue;
        const stemText = q.stem || q.reconstruction?.stem || '';
        const opts = q.options || q.reconstruction?.options || [];
        const optLines = Array.isArray(opts) 
          ? opts.map(o => typeof o === 'string' ? o : `${o.label || o.key || ''}) ${o.text || ''}`).join('\n')
          : '';
        const claim = q.claimedAnswer || q.reconstruction?.correctOption || '';
        const expl = q.explanation || q.reconstruction?.explanation || '';

        const chunkContent = q.ragChunk || `[ÇIKMIŞ SINAV SORUSU]
Ders / Branş: ${q.discipline || 'Tıp'}
Kurul: ${q.committeeId || 'donem3-kurul1'}
Sınav Yılı: ${q.examYear || 'Bilinmiyor'}
Konu: ${q.topic || 'Genel'}
Soru:
${stemText}

Seçenekler:
${optLines}

Doğru/Kabul Edilen Yanıt: ${claim}
${expl ? `Akademik Açıklama: ${expl}` : ''}`.trim();

        const h = hashContent(chunkContent);
        if (!manifest.processedHashes[h]) {
          rawChunksToProcess.push({
            id: `chunk-q-${q.id || h.slice(0, 10)}`,
            documentId: q.id || `q-${h.slice(0, 8)}`,
            documentType: 'past_question',
            committeeId: q.committeeId || 'donem3-kurul1',
            discipline: q.discipline || 'Tıp',
            title: `${q.discipline || 'Tıp'} - ${q.topic || 'Çıkmış Soru'}`,
            pageNumber: q.questionNumber || null,
            content: chunkContent,
            metadata: {
              examYear: q.examYear,
              claimedAnswer: claim,
              sourceFile: q.sourceFile
            },
            hash: h
          });
        }
      }
    }
  }

  // --- B. Amfi Ders Slaytlarını Hazırla ---
  if (!onlyType || onlyType === 'notes') {
    const lnPath = path.resolve(DATA_DIR, 'lecture_notes.json');
    if (fs.existsSync(lnPath)) {
      console.log('📂 Amfi ders slaytları okunuyor...');
      const notes = JSON.parse(fs.readFileSync(lnPath, 'utf-8'));
      for (const note of notes) {
        if (!note.pages || note.pages.length === 0) continue;
        for (const page of note.pages) {
          const rawText = (page.content || '').trim();
          const repaired = (page.repairedContent || '').trim();
          const content = repaired ? (rawText.length >= 30 ? `${rawText}\n\n${repaired}` : repaired) : rawText;
          if (content.length < 30) continue; // Skip near-empty slides

          const chunkContent = `[DERS SLAYTI NOTU]
Ders: ${note.discipline || 'Tıp'}
Sunum Başlığı: ${note.title || 'Ders Notu'}
Kurul: ${note.committeeId || 'donem3-kurul1'}
Slayt Numarası: ${page.pageNumber}
İçerik:
${content}`.trim();

          const h = hashContent(chunkContent);
          if (!manifest.processedHashes[h]) {
            rawChunksToProcess.push({
              id: `chunk-slide-${note.id}-p${page.pageNumber}`,
              documentId: note.id,
              documentType: 'lecture_slide',
              committeeId: note.committeeId || 'donem3-kurul1',
              discipline: note.discipline || 'Tıp',
              title: `${note.title || 'Ders Notu'} (Slayt #${page.pageNumber})`,
              pageNumber: page.pageNumber,
              content: chunkContent,
              metadata: {
                totalSlides: note.totalSlides,
                source: note.source,
                keywords: page.keywords || []
              },
              hash: h
            });
          }
        }
      }
    }
  }

  // --- C. Ses Transkriptlerini Hazırla ---
  if (!onlyType || onlyType === 'transcripts') {
    if (fs.existsSync(TRANSCRIPTIONS_DIR)) {
      console.log('📂 Ses kaydı transkriptleri okunuyor...');
      const transFiles = fs.readdirSync(TRANSCRIPTIONS_DIR).filter(f => f.endsWith('.md'));
      for (const file of transFiles) {
        const fullPath = path.join(TRANSCRIPTIONS_DIR, file);
        const text = fs.readFileSync(fullPath, 'utf-8');
        // Split transcript into 400-word logical chunks
        const paragraphs = text.split(/\n\s*\n/);
        let currentChunkText = '';
        let chunkIndex = 1;

        for (const para of paragraphs) {
          currentChunkText += para + '\n\n';
          if (currentChunkText.length >= 1000) {
            const cleanContent = `[AMFİ SES KAYDI TRANSKRİPTİ]
Başlık: ${file.replace(/_Transkript\.md|_KUSURSUZ\.md|\.md/g, '').replace(/_/g, ' ')}
Parça: #${chunkIndex}
Konuşma / Anlatım:
${currentChunkText.trim()}`.trim();

            const h = hashContent(cleanContent);
            if (!manifest.processedHashes[h]) {
              rawChunksToProcess.push({
                id: `chunk-tr-${file.slice(0, 10)}-${chunkIndex}`,
                documentId: file,
                documentType: 'transcript',
                committeeId: 'donem3-kurul5',
                discipline: file.toLowerCase().includes('halk') ? 'Halk Sağlığı' : 'Tıbbi Genetik',
                title: file.replace('.md', ''),
                pageNumber: chunkIndex,
                content: cleanContent,
                metadata: { file },
                hash: h
              });
            }
            currentChunkText = '';
            chunkIndex++;
          }
        }
      }
    }
  }

  // --- D. Amfi Ders Özetlerini Hazırla (347 Kırmızı/Redakte Özet) ---
  if (!onlyType || onlyType === 'summaries') {
    const sumPath = path.resolve(DATA_DIR, 'lectureSummariesCatalog.json');
    if (fs.existsSync(sumPath)) {
      console.log('📂 Amfi ders özetleri okunuyor...');
      const summaries = JSON.parse(fs.readFileSync(sumPath, 'utf-8'));
      for (const item of summaries) {
        if (!item.content || item.content.length < 50) continue;
        const sections = item.content.split(/\n(?=##\s+)/);
        let sectionIdx = 1;
        for (const sec of sections) {
          const trimmed = sec.trim();
          if (trimmed.length < 40) continue;
          const chunkContent = `[DERS ÖZETİ & SPOT BİLGİ]
Ders / Branş: ${item.discipline || 'Tıp'}
Konu / Başlık: ${item.title}
Kurul: ${item.committeeId || `donem3-kurul${item.kurul || 1}`}
Bölüm: #${sectionIdx}
Özet Metin:
${trimmed}`.trim();

          const h = hashContent(chunkContent);
          if (!manifest.processedHashes[h]) {
            rawChunksToProcess.push({
              id: `chunk-sum-${item.id}-${sectionIdx}`,
              documentId: item.id,
              documentType: 'summary',
              committeeId: item.committeeId || `donem3-kurul${item.kurul || 1}`,
              discipline: item.discipline || 'Tıp',
              title: `${item.title} (Özet #${sectionIdx})`,
              pageNumber: sectionIdx,
              content: chunkContent,
              metadata: {
                fileName: item.fileName,
                keyPoints: item.keyPoints || []
              },
              hash: h
            });
          }
          sectionIdx++;
        }
      }
    }
  }

  // --- E. DeepSeek Katkı Verilerini Hazırla ---
  if (!onlyType || onlyType === 'deepseek') {
    const dsPath = path.resolve(DATA_DIR, 'deepseek_contributions.json');
    if (fs.existsSync(dsPath)) {
      console.log('📂 DeepSeek katkı verileri okunuyor...');
      const dsItems = JSON.parse(fs.readFileSync(dsPath, 'utf-8'));
      for (const item of dsItems) {
        const content = item.content || '';
        if (content.length < 25) continue;
        const h = hashContent(content);
        if (!manifest.processedHashes[h]) {
          rawChunksToProcess.push({
            id: `chunk-ds-${item.id || h.slice(0, 10)}`,
            documentId: item.id,
            documentType: 'deepseek_contribution',
            committeeId: item.committeeId || 'donem3-kurul1',
            discipline: item.discipline || 'Tıp',
            title: `${item.title} [DeepSeek Katkısı]`,
            pageNumber: null,
            content,
            metadata: {
              source: 'deepseek',
              contributor: 'DeepSeek AI',
              isContribution: true,
              itemType: item.itemType,
              sourceFile: item.metadata?.sourceFile,
              topic: item.topic
            },
            hash: h
          });
        }
      }
    }
  }

  console.log(`\nİndekslenecek yeni/güncellenmiş parça sayısı: ${rawChunksToProcess.length}`);
  const targetChunks = rawChunksToProcess.slice(0, maxLimit);
  console.log(`Bu çalıştırmada işlenecek adet (Limit): ${targetChunks.length}\n`);

  if (targetChunks.length === 0) {
    console.log('✨ Tüm veriler zaten güncel ve indekslenmiş durumda!');
    return;
  }

  const BATCH_SIZE = 20;
  let successCount = 0;

  for (let i = 0; i < targetChunks.length; i += BATCH_SIZE) {
    const batch = targetChunks.slice(i, i + BATCH_SIZE);
    const texts = batch.map(b => b.content);

    process.stdout.write(`İşleniyor: ${i + 1}-${Math.min(i + BATCH_SIZE, targetChunks.length)} / ${targetChunks.length}... `);

    try {
      const embeddings = await batchEmbed(texts);
      const rowsToInsert = batch.map((item, idx) => ({
        id: item.id,
        document_id: item.documentId,
        document_type: item.documentType,
        committee_id: item.committeeId,
        discipline: item.discipline,
        title: item.title,
        page_number: item.pageNumber,
        content: item.content,
        metadata: item.metadata,
        embedding: embeddings[idx]
      }));

      const { error: upsertErr } = await supabase.from('rag_chunks').upsert(rowsToInsert, { onConflict: 'id' });
      if (upsertErr) {
        console.log(`❌ HATA: ${upsertErr.message}`);
      } else {
        successCount += batch.length;
        for (const item of batch) {
          manifest.processedHashes[item.hash] = true;
        }
        manifest.totalChunksIndexed = (manifest.totalChunksIndexed || 0) + batch.length;
        manifest.lastIndexedAt = new Date().toISOString();
        saveManifest(manifest);
        console.log('✅ Tamamlandı');
      }
    } catch (batchErr) {
      console.log(`⚠️ Hata oluştu: ${batchErr.message}`);
      await new Promise(r => setTimeout(r, 4000));
    }

    if (i + BATCH_SIZE < targetChunks.length && interBatchDelay > 0) {
      await new Promise(r => setTimeout(r, interBatchDelay));
    }
  }

  console.log('\n====================================================');
  console.log(`🎉 İşlem tamamlandı! ${successCount} adet parça başarıyla vektörleştirildi.`);
  console.log(`Toplam İndekslenmiş Bilgi: ${manifest.totalChunksIndexed}`);
  console.log('====================================================\n');
}

main().catch(err => {
  console.error('Kritik Hata:', err);
  process.exit(1);
});
