import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

dotenv.config({ path: path.join(ROOT_DIR, '.env') });

const SUPABASE_URL = process.env.LOCAL_SUPABASE_URL || process.env.SUPABASE_URL || 'http://127.0.0.1:8000';
const SUPABASE_KEY = process.env.LOCAL_SUPABASE_KEY || process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;
const EMBED_SERVER_URL = 'http://127.0.0.1:8091/embed';

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error('❌ Supabase bilgileri eksik!');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

function cleanForPostgres(data) {
  if (data === null || data === undefined) return data;
  if (typeof data === 'string') return data.replace(/\u0000/g, '').replace(/\x00/g, '');
  if (Array.isArray(data)) return data.map(cleanForPostgres);
  if (typeof data === 'object') {
    const cleaned = {};
    for (const [k, v] of Object.entries(data)) cleaned[k] = cleanForPostgres(v);
    return cleaned;
  }
  return data;
}

async function getEmbeddings(texts) {
  try {
    const res = await fetch(EMBED_SERVER_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texts, kind: 'passage' })
    });
    if (!res.ok) {
      throw new Error(`Embed server HTTP ${res.status}`);
    }
    const data = await res.json();
    return data.vectors;
  } catch (err) {
    console.error('Embed alma hatası:', err.message);
    return null;
  }
}

export async function indexPracticeQuestionsToRag() {
  console.log('🔍 [RAG Chunk & Vectorizer] practice_questions tablosu okunuyor...');

  // Sayfalama ile tüm practice_questions verilerini çek
  let allRows = [];
  let page = 0;
  const PAGE_SIZE = 1000;
  while (true) {
    const { data, error } = await supabase
      .from('practice_questions')
      .select('*')
      .range(page * PAGE_SIZE, (page + 1) * PAGE_SIZE - 1);

    if (error) {
      console.error('Soru çekme hatası:', error.message);
      break;
    }
    if (!data || data.length === 0) break;
    allRows = allRows.concat(data);
    page++;
    process.stdout.write(`\rYüklenen soru: ${allRows.length}`);
  }
  console.log(`\nToplam ${allRows.length} soru RAG chunk havuzuna dönüştürülüyor...`);

  // Mevcut practice_question chunk id'lerini alalım (tekrar aynı hash ile vektörlememek için)
  const { data: existingChunks } = await supabase
    .from('rag_chunks')
    .select('id, content_hash')
    .eq('document_type', 'practice_question');

  const existingMap = new Map();
  if (existingChunks) {
    for (const ec of existingChunks) {
      existingMap.set(ec.id, ec.content_hash);
    }
  }
  console.log(`Mevcut kayıtlı practice_question chunk sayısı: ${existingMap.size}`);

  const chunksToProcess = [];
  for (const q of allRows) {
    const chunkId = `pq_${q.id}`;
    
    // Zengin RAG içerik formatı: Soru, şıklar, doğru yanıt ve fizyopatolojik açıklama
    const optLines = Object.entries(q.secenekler || {})
      .map(([k, v]) => `  ${k}) ${v}`)
      .join('\n');
    
    const expLines = Object.entries(q.sik_aciklamalari || {})
      .map(([k, v]) => `  [${k} Analizi]: ${v}`)
      .join('\n');

    const contentText = [
      `[Tıp Kazanım Soru]: ${q.soru}`,
      `Seçenekler:\n${optLines}`,
      `Doğru Cevap: ${q.dogru}`,
      q.aciklama ? `Genel Tıbbi Açıklama: ${q.aciklama}` : '',
      expLines ? `Şık Analizleri:\n${expLines}` : '',
      `Ders: ${q.ders} | Konu: ${q.konu} | Kazanım: ${q.kazanim_metin} | Zorluk: ${q.zorluk}`
    ].filter(Boolean).join('\n\n');

    const contentHash = crypto.createHash('sha256').update(contentText).digest('hex');

    if (existingMap.get(chunkId) === contentHash) {
      // İçerik ve vektör değişmemiş, atla
      continue;
    }

    chunksToProcess.push({
      id: chunkId,
      document_id: q.id,
      document_type: 'practice_question',
      committee_id: `donem3-kurul${q.kurul || 1}`,
      discipline: q.ders || 'Tıp Fakültesi',
      title: `${q.ders} - ${q.konu} (K${q.kazanim_no}) [${q.zorluk || 'orta'}]`,
      page_number: q.kazanim_no || 1,
      content: contentText,
      content_hash: contentHash,
      metadata: {
        version: q.version,
        lesson_id: q.lesson_id,
        ders: q.ders,
        konu: q.konu,
        zorluk: q.zorluk,
        dogru: q.dogru,
        kazanim_no: q.kazanim_no
      }
    });
  }

  console.log(`Yeni veya güncellenmesi gereken chunk sayısı: ${chunksToProcess.length}`);
  if (chunksToProcess.length === 0) {
    console.log('✅ Tüm örnek sorular zaten güncel şekilde vektörlenmiş!');
    return;
  }

  const BATCH_SIZE = 64;
  let processed = 0;

  for (let i = 0; i < chunksToProcess.length; i += BATCH_SIZE) {
    const batch = chunksToProcess.slice(i, i + BATCH_SIZE);
    const texts = batch.map(c => c.content.slice(0, 1500));
    const vectors = await getEmbeddings(texts);

    const rowsToUpsert = batch.map((c, idx) => ({
      ...c,
      embedding_e5: vectors && vectors[idx] ? vectors[idx] : null,
      updated_at: new Date().toISOString()
    }));

    const { error: upsertErr } = await supabase
      .from('rag_chunks')
      .upsert(cleanForPostgres(rowsToUpsert), { onConflict: 'id' });

    if (upsertErr) {
      console.error(`Parti [${i}] upsert hatası:`, upsertErr.message);
    } else {
      processed += batch.length;
      process.stdout.write(`\rVektörlenen ve RAG'e yazılan: ${processed} / ${chunksToProcess.length}`);
    }
  }

  console.log(`\n🎉 [BAŞARILI] Toplam ${processed} örnek soru RAG chunk ve e5-384 vektör tablosuna işlendi!`);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  indexPracticeQuestionsToRag().catch(console.error);
}
