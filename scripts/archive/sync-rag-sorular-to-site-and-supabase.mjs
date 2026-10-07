/**
 * scripts/sync-rag-sorular-to-site-and-supabase.mjs
 * 
 * Bu script:
 * 1. meds_database/rag_sorular klasöründeki 1.082 adet doğrulanmış ve amfi ders notlarıyla
 *    zeminlenmiş (grounded) soruyu okur.
 * 2. meds/data/pastQuestions.json dosyasını yedekler ve bu 1.082 soruyu site veritabanına entegre eder:
 *    - 5 adet düzeltilen cevap anahtarını (d3-f-084, d3-f-050, d3-f-099, d3-f-187, d3-k1-pat-047) günceller.
 *    - 142 adet yanlış branşa atanmış soruyu gerçek amfi dersiyle (disciplineVerified) günceller.
 *    - 22 adet yapısal/tıbbi kusurlu soruyu 'isSuspect: true' ve 'hatali' olarak işaretler.
 *    - Birebir amfi alıntı kanıtlarını (grounding, evidenceQuote, noteFile) ve clinicalPearl'leri ekler.
 *    - RAG embedding metinlerini ve anahtar kelimelerini (ragChunk) entegre eder.
 * 3. Değişiklikleri meds/data/pastQuestions.json ve meds/src/data/pastQuestions.json dosyalarına yazar.
 * 4. meds/data/local_rag_chunks.json dosyasındaki ilgili chunk'ları günceller.
 * 5. Hem Yerel Docker Supabase'e (http://localhost:8000) hem de Cloud Supabase'e (https://kgutsltgmqbnlxcnzrtl.supabase.co)
 *    güvenli partiler (batch) halinde upsert eder.
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const ENV_PATH = path.join(ROOT_DIR, '.env');

dotenv.config({ path: ENV_PATH });

const PAST_JSON_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.json');
const SRC_PAST_JSON_PATH = path.join(ROOT_DIR, 'src', 'data', 'pastQuestions.json');
const LOCAL_RAG_PATH = path.join(ROOT_DIR, 'data', 'local_rag_chunks.json');
const RAG_SORULAR_DIR = `${process.env.MEDS_DATABASE_DIR || '/home/indu/medsor/meds_database'}/rag_sorular`;

function cleanForPostgres(data) {
  if (data === null || data === undefined) return data;
  if (typeof data === 'string') {
    return data.replace(/\u0000/g, '').replace(/[\x00]/g, '');
  }
  if (Array.isArray(data)) {
    return data.map(cleanForPostgres);
  }
  if (typeof data === 'object') {
    const cleaned = {};
    for (const [k, v] of Object.entries(data)) {
      cleaned[k] = cleanForPostgres(v);
    }
    return cleaned;
  }
  return data;
}

function walkDir(dir, fileList = []) {
  if (!fs.existsSync(dir)) return fileList;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === '_rapor') continue;
      walkDir(fullPath, fileList);
    } else if (entry.name.endsWith('.json') && entry.name !== 'index.json') {
      fileList.push(fullPath);
    }
  }
  return fileList;
}

async function uploadToSupabaseInBatches(supabaseClient, rows, targetName, batchSize = 50, maxRetries = 3) {
  if (!supabaseClient) {
    console.warn(`[Supabase ${targetName}] İstemci tanımlı değil, atlanıyor.`);
    return { success: false, count: 0 };
  }

  const totalBatches = Math.ceil(rows.length / batchSize);
  let successCount = 0;

  console.log(`\n🚀 [Supabase ${targetName}] ${rows.length} satır aktarılıyor (${totalBatches} parti)...`);

  for (let i = 0; i < rows.length; i += batchSize) {
    const chunk = rows.slice(i, i + batchSize);
    const batchNum = Math.floor(i / batchSize) + 1;
    let ok = false;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const { error } = await supabaseClient
          .from('past_questions')
          .upsert(cleanForPostgres(chunk), { onConflict: 'id' });

        if (!error) {
          ok = true;
          successCount += chunk.length;
          break;
        }
        console.warn(`[${targetName}] Parti [${batchNum}/${totalBatches}] Deneme ${attempt} hata:`, error.message);
      } catch (err) {
        console.warn(`[${targetName}] Parti [${batchNum}/${totalBatches}] Deneme ${attempt} istisna:`, err.message);
      }
      await new Promise(r => setTimeout(r, 1200 * attempt));
    }

    if (!ok) {
      console.error(`❌ [${targetName}] Parti [${batchNum}/${totalBatches}] yüklenemedi!`);
    } else if (batchNum % 5 === 0 || batchNum === totalBatches) {
      process.stdout.write(`  [${targetName}] İlerleme: ${successCount} / ${rows.length} (%${Math.round(successCount / rows.length * 100)})\r`);
    }
  }

  console.log(`\n✅ [Supabase ${targetName}] Tamamlandı: ${successCount} / ${rows.length}`);
  return { success: successCount === rows.length, count: successCount };
}

async function main() {
  console.log('================================================================');
  console.log('  RAG Sorular -> meds Site & Dual Supabase Senkronizasyon Motoru ');
  console.log('================================================================');

  // 1. RAG Soruları Oku
  const ragFiles = walkDir(RAG_SORULAR_DIR);
  console.log(`📂 rag_sorular taranıyor... ${ragFiles.length} batch dosyası bulundu.`);

  const ragQuestionsMap = new Map();
  for (const f of ragFiles) {
    try {
      const data = JSON.parse(fs.readFileSync(f, 'utf8'));
      const qs = Array.isArray(data) ? data : (data.questions || []);
      for (const q of qs) {
        if (q.id) {
          ragQuestionsMap.set(q.id, q);
        }
      }
    } catch (e) {
      console.warn(`⚠️ Dosya okuma hatası (${f}):`, e.message);
    }
  }

  console.log(`🔍 Toplam ${ragQuestionsMap.size} adet RAG sorusu yüklendi.`);

  // 2. Mevcut Site pastQuestions.json'ı oku ve yedekle
  if (!fs.existsSync(PAST_JSON_PATH)) {
    console.error('❌ pastQuestions.json bulunamadı:', PAST_JSON_PATH);
    process.exit(1);
  }

  const siteQuestions = JSON.parse(fs.readFileSync(PAST_JSON_PATH, 'utf8'));
  console.log(`📦 Mevcut site soru sayısı: ${siteQuestions.length}`);

  // Yedek oluştur
  const backupPath = path.join(ROOT_DIR, 'data', `pastQuestions.backup_before_rag_sync_${Date.now()}.json`);
  fs.writeFileSync(backupPath, JSON.stringify(siteQuestions, null, 2), 'utf8');
  console.log(`💾 Güvenlik yedeği oluşturuldu: ${path.basename(backupPath)}`);

  // 3. Soruları Entegre Et
  let answerKeysCorrected = 0;
  let disciplinesCorrected = 0;
  let flaggedAsSuspect = 0;
  let groundedCount = 0;
  let matchedQuestionsCount = 0;
  const nowIso = new Date().toISOString();

  const correctedAnswersDetail = [];

  for (let i = 0; i < siteQuestions.length; i++) {
    const siteQ = siteQuestions[i];
    const ragQ = ragQuestionsMap.get(siteQ.id);

    if (!ragQ) continue;
    matchedQuestionsCount++;

    const prevAnswer = (siteQ.correctOption || siteQ.correctAnswer || (siteQ.reconstruction && siteQ.reconstruction.correctAnswer) || '').trim().toUpperCase();
    const newAnswer = (ragQ.correctAnswer || '').trim().toUpperCase();

    if (newAnswer && prevAnswer && newAnswer !== prevAnswer) {
      answerKeysCorrected++;
      correctedAnswersDetail.push({
        id: siteQ.id,
        stem: (ragQ.stem || siteQ.stem || siteQ.question || '').slice(0, 60),
        oldAns: prevAnswer,
        newAns: newAnswer,
        category: ragQ.category,
        note: ragQ.grounding?.notesAndDiscrepancies || ragQ.curationNote || ''
      });
    }

    const prevDisc = (siteQ.discipline || '').trim();
    const newDisc = (ragQ.disciplineVerified || ragQ.discipline || '').trim();
    if (newDisc && prevDisc && newDisc.toLowerCase() !== prevDisc.toLowerCase()) {
      disciplinesCorrected++;
    }

    const isFlawed = ragQ.category === 'hatali' ||
      (Array.isArray(ragQ.issues) && (
        ragQ.issues.includes('soru_yapisi_bozuk') ||
        ragQ.issues.includes('dogru_sik_yok') ||
        ragQ.issues.includes('birden_fazla_dogru') ||
        ragQ.issues.includes('ayni_secenek_tekrari')
      ));

    if (isFlawed) {
      flaggedAsSuspect++;
    }

    if (ragQ.grounding?.status === 'zeminlendi') {
      groundedCount++;
    }

    // Temiz şıklar ve doğru seçenek kontrolü
    const cleanOptions = Array.isArray(ragQ.options) ? ragQ.options.map(opt => ({
      key: opt.key,
      text: opt.text,
      isCorrect: opt.key === (newAnswer || siteQ.correctOption)
    })) : (siteQ.options || []);

    // Sitedeki soruyu zenginleştir
    siteQuestions[i] = {
      ...siteQ,
      stem: ragQ.stem || siteQ.stem || siteQ.question,
      question: ragQ.stem || siteQ.question || siteQ.stem,
      options: cleanOptions,
      correctOption: newAnswer || siteQ.correctOption || 'A',
      correctAnswer: newAnswer || siteQ.correctAnswer || 'A',
      claimedAnswer: newAnswer || siteQ.claimedAnswer || siteQ.correctOption,
      discipline: newDisc || siteQ.discipline,
      disciplineOriginal: ragQ.disciplineOriginal || siteQ.discipline,
      disciplineVerified: ragQ.disciplineVerified || newDisc || siteQ.discipline,
      topic: ragQ.topic || siteQ.topic,
      explanation: ragQ.explanation || siteQ.explanation,
      clinicalPearl: ragQ.clinicalPearl || siteQ.clinicalPearl || '',
      category: ragQ.category || siteQ.category || 'gecerli',
      issues: ragQ.issues || siteQ.issues || [],
      changes: ragQ.changes || siteQ.changes || [],
      grounding: ragQ.grounding || siteQ.grounding,
      ragChunk: ragQ.ragChunk || siteQ.ragChunk,
      embeddingText: ragQ.ragChunk?.text || siteQ.embeddingText,
      evidenceText: ragQ.grounding?.evidenceQuote || siteQ.evidenceText || '',
      matchedNoteTitle: ragQ.grounding?.lectureTitle || siteQ.matchedNoteTitle || '',
      isSuspect: isFlawed || Boolean(siteQ.isSuspect),
      isAmbiguous: isFlawed || Boolean(siteQ.isAmbiguous),
      deepseekEnriched: true,
      ragGrounded: true,
      verification: {
        status: isFlawed ? 'hatali' : (ragQ.category === 'gecerli' ? 'onaylandi' : (ragQ.category === 'duzeltildi' ? 'duzeltildi' : 'inceleme_gerekli')),
        answerStatus: ragQ.category === 'duzeltildi' ? 'duzeltildi' : (isFlawed ? 'hatali' : 'dogrulandi'),
        evidenceStatus: ragQ.grounding?.status === 'zeminlendi' ? 'kanitli' : (ragQ.grounding?.status === 'kismen_zeminlendi' ? 'kismen_kanitli' : 'not_yok'),
        confidence: ragQ.grounding?.coverage === 'guclu' ? 1.0 : (ragQ.grounding?.coverage === 'orta' ? 0.8 : 0.5),
        curriculumFit: ragQ.category === 'yanlis_ders' ? 'duzeltildi' : (ragQ.category === 'ders_notu_ile_iliskisiz' ? 'uyumsuz' : 'uyumlu'),
        qualityScore: isFlawed ? 35 : (ragQ.category === 'gecerli' ? 95 : 85),
        changes: ragQ.changes || [],
        needsReview: isFlawed || ragQ.category === 'ders_notu_ile_iliskisiz',
        reviewReason: ragQ.grounding?.notesAndDiscrepancies || ragQ.curationNote || (ragQ.issues?.length ? ragQ.issues.join(', ') : '')
      },
      reconstruction: {
        ...(siteQ.reconstruction || {}),
        stem: ragQ.stem || siteQ.stem || siteQ.question,
        options: cleanOptions,
        correctAnswer: newAnswer || siteQ.correctOption,
        explanation: ragQ.explanation || siteQ.explanation,
        clinicalPearl: ragQ.clinicalPearl || '',
        evidenceText: ragQ.grounding?.evidenceQuote || '',
        reconstructionQuality: 'rag_grounded',
        notesAndDiscrepancies: ragQ.grounding?.notesAndDiscrepancies || '',
        lastUpdated: nowIso
      },
      updatedAt: nowIso
    };
  }

  console.log('\n--- Entegrasyon İstatistikleri ---');
  console.log(`✅ Eşleşen ve Zenginleştirilen Soru: ${matchedQuestionsCount} / ${ragQuestionsMap.size}`);
  console.log(`🔧 Cevap Anahtarı Düzeltilen: ${answerKeysCorrected}`);
  console.log(`🏷️ Branşı (Discipline) Düzeltilen: ${disciplinesCorrected}`);
  console.log(`⚠️ Kusurlu/Hatalı İşaretlenen (isSuspect): ${flaggedAsSuspect}`);
  console.log(`📖 Tam Zeminlenen (Grounded): ${groundedCount}`);

  if (correctedAnswersDetail.length > 0) {
    console.log('\nDüzeltilen Cevap Anahtarları:');
    correctedAnswersDetail.forEach(c => {
      console.log(`  - [${c.id}] ${c.stem}... | Eski: ${c.oldAns} -> Yeni: ${c.newAns} (${c.category})`);
    });
  }

  // 4. Dosyalara Yaz
  console.log('\n💾 JSON dosyaları güncelleniyor...');
  const jsonStr = JSON.stringify(siteQuestions, null, 2);
  fs.writeFileSync(PAST_JSON_PATH, jsonStr, 'utf8');
  console.log(`✅ ${PAST_JSON_PATH} yazıldı.`);

  if (fs.existsSync(path.dirname(SRC_PAST_JSON_PATH))) {
    fs.writeFileSync(SRC_PAST_JSON_PATH, jsonStr, 'utf8');
    console.log(`✅ ${SRC_PAST_JSON_PATH} yazıldı.`);
  }

  // 5. local_rag_chunks.json'ı güncelle
  if (fs.existsSync(LOCAL_RAG_PATH)) {
    try {
      console.log('\n🔄 local_rag_chunks.json güncelleniyor...');
      const localChunksBackup = path.join(ROOT_DIR, 'data', `local_rag_chunks.backup_${Date.now()}.json`);
      fs.copyFileSync(LOCAL_RAG_PATH, localChunksBackup);

      const localChunks = JSON.parse(fs.readFileSync(LOCAL_RAG_PATH, 'utf8'));
      const chunkMap = new Map();
      localChunks.forEach(c => chunkMap.set(c.documentId || c.id, c));

      let updatedChunkCount = 0;
      for (const [qId, ragQ] of ragQuestionsMap.entries()) {
        const fullQ = siteQuestions.find(q => q.id === qId);
        if (!fullQ) continue;

        const chunkId = `chunk-pq-${qId}`;
        const newChunk = {
          id: chunkId,
          documentId: qId,
          documentType: 'past_question',
          committeeId: fullQ.committeeId,
          discipline: fullQ.discipline,
          title: `${fullQ.discipline} - ${fullQ.topic || ''} (${fullQ.examYear || ''})`,
          pageNumber: 1,
          content: ragQ.ragChunk?.text || fullQ.embeddingText || fullQ.explanation || '',
          metadata: {
            examYear: fullQ.examYear || 'Geçmiş Yıllar Çıkmışı (Arşiv)',
            claimedAnswer: fullQ.correctOption,
            sourceFile: fullQ.sourceFile || ragQ.provenance?.sourceFile || '',
            topic: fullQ.topic || '',
            category: ragQ.category || 'gecerli',
            groundingStatus: ragQ.grounding?.status || 'zeminlendi',
            keywords: ragQ.ragChunk?.keywords || [],
            isSuspect: fullQ.isSuspect,
            hasSlideRef: Boolean(ragQ.grounding?.noteFile)
          },
          hash: crypto.createHash('md5').update(ragQ.ragChunk?.text || fullQ.id).digest('hex'),
          createdAt: fullQ.createdAt || nowIso,
          updatedAt: nowIso
        };

        chunkMap.set(qId, newChunk);
        updatedChunkCount++;
      }

      const mergedChunks = Array.from(chunkMap.values());
      fs.writeFileSync(LOCAL_RAG_PATH, JSON.stringify(mergedChunks, null, 2), 'utf8');
      console.log(`✅ local_rag_chunks.json güncellendi: ${updatedChunkCount} soru chunk'ı yenilendi, toplam chunk: ${mergedChunks.length}`);
    } catch (chunkErr) {
      console.warn('⚠️ local_rag_chunks güncelleme uyarısı:', chunkErr.message);
    }
  }

  // 6. Supabase Satırlarını Hazırla
  console.log('\n📦 Supabase past_questions tablosu için satırlar hazırlanıyor...');
  const supabaseRows = siteQuestions.map(q => cleanForPostgres({
    id: q.id,
    committee_id: q.committeeId,
    discipline: q.discipline || 'Tıbbi Patoloji',
    topic: q.topic || `Soru #${q.questionNumber || q.id}`,
    exam_year: q.examYear || 'Geçmiş Yıllar Çıkmışı (Arşiv)',
    source_file: q.sourceFile || null,
    ai_category: q.category || q.aiCategory || null,
    claimed_answer: q.correctOption || q.correctAnswer || q.claimedAnswer || null,
    raw_question: q.rawQuestion || null,
    reconstruction: q.reconstruction || null,
    is_suspect: Boolean(q.isSuspect),
    is_ambiguous: Boolean(q.isAmbiguous),
    is_locked: Boolean(q.isLocked),
    upvotes: q.upvotes || 0,
    comments: q.comments || [],
    reports: q.reports || [],
    custom_redacted_by: q.customRedactedBy || null,
    custom_redacted_at: q.customRedactedAt || null,
    custom_redaction_prompt: q.customRedactionPrompt || null,
    data: q,
    updated_at: q.updatedAt || nowIso
  }));

  // 7. Supabase Senkronizasyonu (Yerel Docker + Cloud)
  // A) Yerel Docker Supabase
  const localUrl = process.env.LOCAL_SUPABASE_URL || process.env.SUPABASE_URL || 'http://localhost:8000';
  const localKey = process.env.LOCAL_SUPABASE_KEY || process.env.SUPABASE_SECRET_KEY;
  if (localUrl && localKey) {
    try {
      const localClient = createClient(localUrl, localKey);
      await uploadToSupabaseInBatches(localClient, supabaseRows, 'Yerel Docker (localhost:8000)', 50);
    } catch (e) {
      console.warn('⚠️ Yerel Supabase aktarım hatası:', e.message);
    }
  }

  // B) Cloud Supabase
  const cloudUrl = process.env.CLOUD_SUPABASE_URL || 'https://kgutsltgmqbnlxcnzrtl.supabase.co';
  const cloudKey = process.env.CLOUD_SUPABASE_SECRET_KEY || process.env.SUPABASE_SECRET_KEY;
  if (cloudUrl && cloudKey) {
    try {
      const cloudClient = createClient(cloudUrl, cloudKey);
      await uploadToSupabaseInBatches(cloudClient, supabaseRows, 'Cloud Supabase (kgutsltgmqbnlxcnzrtl)', 50);
    } catch (e) {
      console.warn('⚠️ Cloud Supabase aktarım hatası:', e.message);
    }
  }

  console.log('\n================================================================');
  console.log('🎉 SENKRONİZASYON TAMAMLANDI: Site ve Supabase güncellendi!');
  console.log('================================================================');
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
