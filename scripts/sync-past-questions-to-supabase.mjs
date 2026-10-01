/**
 * scripts/sync-past-questions-to-supabase.mjs
 * 
 * pastQuestions.json dosyasındaki 2922 adet çıkmış soruyu
 * güvenli 25'lik partiler halinde ve otomatik tekrar (retry) mekanizmasıyla
 * Supabase 'past_questions' tablosuna aktarır.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const PAST_JSON_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.json');

function cleanForPostgres(data) {
  if (data === null || data === undefined) return data;
  if (typeof data === 'string') {
    return data.replace(/\u0000/g, '').replace(/\x00/g, '');
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

async function uploadChunkWithRetry(supabase, rows, chunkIndex, total, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const { error } = await supabase.from('past_questions').upsert(cleanForPostgres(rows), { onConflict: 'id' });
      if (!error) {
        return true;
      }
      console.warn(`Parti [${chunkIndex}/${total}] Deneme ${attempt} hatası:`, error.message);
    } catch (err) {
      console.warn(`Parti [${chunkIndex}/${total}] Deneme ${attempt} istisna:`, err.message);
    }
    await new Promise(r => setTimeout(r, 1500 * attempt));
  }
  return false;
}

async function syncPastQuestions() {
  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;

  if (!supabaseUrl || !supabaseKey) {
    console.error('❌ Supabase bilgileri eksik!');
    process.exit(1);
  }

  const supabase = createClient(supabaseUrl, supabaseKey);
  const list = JSON.parse(fs.readFileSync(PAST_JSON_PATH, 'utf8'));
  console.log(`📦 ${list.length} adet çıkmış soru Supabase 'past_questions' tablosuna aktarılıyor...`);

  const BATCH_SIZE = 25;
  let successCount = 0;
  const totalBatches = Math.ceil(list.length / BATCH_SIZE);

  for (let i = 0; i < list.length; i += BATCH_SIZE) {
    const chunk = list.slice(i, i + BATCH_SIZE);
    const batchNum = Math.floor(i / BATCH_SIZE) + 1;
    const rows = chunk.map(q => ({
      id: q.id,
      committee_id: q.committeeId,
      discipline: q.discipline || 'Tıbbi Patoloji',
      topic: q.topic || `Soru #${q.questionNumber || i + 1}`,
      exam_year: q.examYear || 'Geçmiş Yıllar Çıkmışı (Arşiv)',
      source_file: q.sourceFile || null,
      ai_category: q.aiCategory || null,
      claimed_answer: q.claimedAnswer || q.reconstruction?.correctAnswer || null,
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
      updated_at: new Date().toISOString()
    }));

    const ok = await uploadChunkWithRetry(supabase, rows, batchNum, totalBatches);
    if (ok) {
      successCount += chunk.length;
    }
    console.log(`[${batchNum}/${totalBatches}] ${successCount} / ${list.length} aktarıldı.`);
  }

  console.log(`\n✅ Supabase 'past_questions' başarıyla tamamlandı: ${successCount} / ${list.length}`);
}

syncPastQuestions().catch(e => {
  console.error('Hata:', e);
  process.exit(1);
});
