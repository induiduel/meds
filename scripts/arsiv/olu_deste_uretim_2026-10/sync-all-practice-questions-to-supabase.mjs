import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { createClient } from '@supabase/supabase-js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

dotenv.config({ path: path.join(ROOT_DIR, '.env') });

const SUPABASE_URL = process.env.LOCAL_SUPABASE_URL || process.env.SUPABASE_URL || 'http://127.0.0.1:8000';
const SUPABASE_KEY = process.env.LOCAL_SUPABASE_KEY || process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error('❌ Supabase bilgileri bulunamadı!');
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

const DIRS = {
  'v1_editor': path.resolve(ROOT_DIR, '..', 'meds_database_v2', 'ornek_sorular_k1'),
  'v5_muse': path.resolve(ROOT_DIR, '..', 'meds_database_v2', 'ornek_sorular_k1_v5_muse'),
  'v6_muse': path.resolve(ROOT_DIR, '..', 'meds_database_v2', 'ornek_sorular_k1_v6_muse'),
  'v4_kalibrasyon': path.resolve(ROOT_DIR, '..', 'meds_database_v2', 'ornek_sorular_k1_v4'),
  'v2_revize': path.resolve(ROOT_DIR, '..', 'meds_database_v2', 'ornek_sorular_k1_revize'),
  'v3_kalem': path.resolve(ROOT_DIR, '..', 'meds_database_v2', 'ornek_sorular_k1_v3')
};

export async function mergeAndUploadPracticeQuestions() {
  console.log('🚀 [Practice Questions Master Sync] Başlatılıyor...');
  console.log('🔗 Supabase:', SUPABASE_URL);

  const allRecords = [];
  const seenStems = new Set();

  for (const [versionKey, dirPath] of Object.entries(DIRS)) {
    if (!fs.existsSync(dirPath)) {
      console.warn(`Dizin bulunamadı: ${dirPath}`);
      continue;
    }
    const files = fs.readdirSync(dirPath).filter(f => f.startsWith('k1-') && f.endsWith('.json'));

    for (const file of files) {
      let content;
      try {
        content = JSON.parse(fs.readFileSync(path.join(dirPath, file), 'utf-8'));
      } catch (err) {
        continue;
      }

      const lessonId = content.id || file.replace('.json', '');
      const kurul = content.kurul || 1;
      const ders = content.ders || '';
      const konu = content.konu || '';
      const ogretimUyesi = content.ogretim_uyesi || '';

      for (const kaz of (content.kazanimlar || [])) {
        const kazNo = kaz.no || 1;
        const kazMetin = kaz.metin || '';

        for (let qIdx = 0; qIdx < (kaz.sorular || []).length; qIdx++) {
          const q = kaz.sorular[qIdx];
          const stem = (q.soru || '').trim();
          if (!stem || stem.length < 10) continue;

          const stemKey = stem.toLowerCase().slice(0, 150);
          if (seenStems.has(stemKey)) continue;
          seenStems.add(stemKey);

          const qid = q.id ? `${versionKey}_${q.id}` : `${versionKey}_${lessonId}_k${kazNo}_q${qIdx + 1}`;
          allRecords.push({
            id: qid,
            version: versionKey,
            kurul,
            lesson_id: lessonId,
            ders,
            konu,
            ogretim_uyesi: ogretimUyesi,
            kazanim_no: kazNo,
            kazanim_metin: kazMetin,
            zorluk: q.zorluk || 'orta',
            soru: stem,
            secenekler: q.secenekler || {},
            dogru: q.dogru || 'A',
            aciklama: q.aciklama || '',
            sik_aciklamalari: q.sik_aciklamalari || {},
            bilgi: q.bilgi || [],
            benzer_cikmis: q.benzer_cikmis || [],
            data: {
              version: versionKey,
              lesson_id: lessonId,
              ders,
              konu,
              ogretim_uyesi: ogretimUyesi,
              kazanim_no: kazNo,
              kazanim_metin: kazMetin,
              ...q
            },
            updated_at: new Date().toISOString()
          });
        }
      }
    }
  }

  console.log(`\n📊 Toplam filtrelenmiş ve tekilleştirilmiş soru adedi: ${allRecords.length}`);

  // Önce tabloyu temizle
  console.log('Temizleniyor...');
  await supabase.from('practice_questions').delete().neq('id', '___keep___');

  console.log('Partiler halinde (100\'erli) yükleniyor...');
  const BATCH_SIZE = 100;
  let successCount = 0;
  for (let i = 0; i < allRecords.length; i += BATCH_SIZE) {
    const chunk = allRecords.slice(i, i + BATCH_SIZE);
    const { error } = await supabase.from('practice_questions').upsert(cleanForPostgres(chunk), { onConflict: 'id' });
    if (error) {
      console.error(`Parti [${i}] hatası:`, error.message);
    } else {
      successCount += chunk.length;
      process.stdout.write(`\rİlerleme: ${successCount} / ${allRecords.length} soru aktarıldı...`);
    }
  }

  console.log(`\n✅ ${successCount} soru başarıyla practice_questions tablosuna aktarıldı!`);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  mergeAndUploadPracticeQuestions().catch(console.error);
}
