/**
 * scripts/sync-database-json-to-cloud.mjs
 * 
 * C:\Users\indui\Desktop\meds_database\database_json altındaki yapılandırılmış JSON dosyalarını
 * doğrudan Supabase (PostgreSQL) ve Firebase (Firestore) veritabanlarına yükler.
 * 
 * Kullanım:
 * node scripts/sync-database-json-to-cloud.mjs --all
 * node scripts/sync-database-json-to-cloud.mjs --folder=donem3k1
 * node scripts/sync-database-json-to-cloud.mjs --dry-run
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
const BASE_JSON_DIR = 'C:\\Users\\indui\\Desktop\\meds_database\\database_json';

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;

// Argümanları ayrıştır
const args = process.argv.slice(2);
const isDryRun = args.includes('--dry-run');
const folderArg = args.find(a => a.startsWith('--folder='))?.split('=')[1] || null;

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

async function main() {
  console.log('☁️ [Database JSON Cloud Sync] Başlatılıyor...');
  console.log(`📁 Kaynak Dizin: ${BASE_JSON_DIR}`);
  if (isDryRun) {
    console.log('🔍 [DRY-RUN] Simülasyon modunda çalışılıyor. Veritabanına yazma yapılmayacak.');
  }

  if (!fs.existsSync(BASE_JSON_DIR)) {
    console.error(`❌ Dizin bulunamadı: ${BASE_JSON_DIR}`);
    process.exit(1);
  }

  let supabase = null;
  if (!isDryRun) {
    if (!SUPABASE_URL || !SUPABASE_KEY) {
      console.warn('⚠️ Supabase URL veya KEY bulunamadı (.env kontrol edin). Yalnızca yerel kontrol yapılıyor.');
    } else {
      supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
      console.log(`🔗 Supabase Bağlantısı Hazır: ${SUPABASE_URL}`);
    }
  }

  // Taranacak klasörler
  let folders = fs.readdirSync(BASE_JSON_DIR).filter(f => {
    const full = path.join(BASE_JSON_DIR, f);
    return fs.statSync(full).isDirectory();
  });

  if (folderArg) {
    folders = folders.filter(f => f.toLowerCase() === folderArg.toLowerCase());
    if (folders.length === 0) {
      console.error(`❌ Belirtilen klasör bulunamadı: ${folderArg}`);
      process.exit(1);
    }
  }

  console.log(`📦 İşlenecek Klasör Sayısı: ${folders.length}`);

  let totalPastUploaded = 0;
  let totalRealtimeUploaded = 0;

  for (const folder of folders) {
    const folderPath = path.join(BASE_JSON_DIR, folder);
    const pastFile = path.join(folderPath, 'pastquestions.json');
    const realtimeFile = path.join(folderPath, 'realtimequestion.json');
    const committeeFile = path.join(folderPath, 'committee.json');

    console.log(`\n📂 Klasör İşleniyor: [${folder}]`);

    // 1. Kurul Meta Verisi
    if (fs.existsSync(committeeFile) && supabase) {
      try {
        const comm = JSON.parse(fs.readFileSync(committeeFile, 'utf8'));
        const row = {
          id: comm.committeeId || comm.id,
          name: comm.name,
          academic_year: comm.academicYear || comm.term || '2026-2027',
          target_questions: comm.targetCount || 100,
          color: comm.color || 'teal',
          data: comm
        };
        const { error } = await supabase.from('committees').upsert(cleanForPostgres(row), { onConflict: 'id' });
        if (error) console.warn(`  ⚠️ Kurul meta aktarım hatası (${folder}):`, error.message);
        else console.log(`  ✅ Kurul meta verisi aktarıldı: ${comm.name}`);
      } catch (e) {
        console.warn('  ⚠️ committee.json okuma hatası:', e.message);
      }
    }

    // 2. Çıkmış Sorular
    if (fs.existsSync(pastFile)) {
      try {
        const pastList = JSON.parse(fs.readFileSync(pastFile, 'utf8'));
        console.log(`  📝 Çıkmış Soru Sayısı: ${pastList.length}`);

        if (supabase && pastList.length > 0) {
          const BATCH_SIZE = 50;
          for (let i = 0; i < pastList.length; i += BATCH_SIZE) {
            const batch = pastList.slice(i, i + BATCH_SIZE);
            const rows = batch.map(q => ({
              id: q.id,
              committee_id: q.committeeId,
              discipline: q.discipline || 'Tıbbi Patoloji',
              topic: q.topic || 'Genel Konu',
              exam_year: q.examYear || 'Geçmiş Yıllar Çıkmışı (Arşiv)',
              source_file: q.sourceFile || null,
              ai_category: q.aiCategory || null,
              claimed_answer: q.claimedAnswer || null,
              raw_question: q.rawQuestion || null,
              reconstruction: q.reconstruction || null,
              is_suspect: Boolean(q.isSuspect),
              is_ambiguous: Boolean(q.isAmbiguous),
              is_locked: Boolean(q.isLocked),
              upvotes: q.upvotes || 0,
              comments: q.comments || [],
              reports: q.reports || [],
              data: q,
              updated_at: new Date().toISOString()
            }));

            const { error } = await supabase.from('past_questions').upsert(cleanForPostgres(rows), { onConflict: 'id' });
            if (error) {
              console.warn(`  ⚠️ Parti aktarım hatası [${i}-${i + batch.length}]:`, error.message);
            } else {
              totalPastUploaded += batch.length;
              process.stdout.write(`\r  ⬆️ Supabase Çıkmış Soru Aktarımı: ${totalPastUploaded} soru yüklendi...`);
            }
          }
          console.log('');
        }
      } catch (e) {
        console.warn('  ⚠️ pastquestions.json okuma hatası:', e.message);
      }
    }

    // 3. Canlı / Mevcut Sorular
    if (fs.existsSync(realtimeFile)) {
      try {
        const realtimeList = JSON.parse(fs.readFileSync(realtimeFile, 'utf8'));
        if (realtimeList.length > 0) {
          console.log(`  ⚡ Canlı Soru Sayısı: ${realtimeList.length}`);
          if (supabase) {
            const rows = realtimeList.map(q => ({
              id: q.id,
              committee_id: q.committeeId,
              question_number: q.questionNumber,
              discipline: q.discipline,
              topic: q.topic,
              status: q.status || 'gathering',
              claimed_answer: q.claimedAnswer,
              upvotes: q.upvotes || 0,
              tags: q.tags || [],
              fragments: q.fragments || [],
              options: q.options || [],
              reconstruction: q.reconstruction || null,
              data: q,
              updated_at: new Date().toISOString()
            }));

            const { error } = await supabase.from('questions').upsert(cleanForPostgres(rows), { onConflict: 'id' });
            if (error) {
              console.warn('  ⚠️ Canlı soru aktarım hatası:', error.message);
            } else {
              totalRealtimeUploaded += rows.length;
              console.log(`  ✅ ${rows.length} Canlı soru Supabase 'questions' tablosuna aktarıldı.`);
            }
          }
        }
      } catch (e) {
        console.warn('  ⚠️ realtimequestion.json okuma hatası:', e.message);
      }
    }
  }

  console.log('\n=============================================');
  console.log('🎉 [Bulu Senkronizasyonu Tamamlandı]');
  console.log(`📊 Toplam Aktarılan Çıkmış Soru: ${totalPastUploaded}`);
  console.log(`📊 Toplam Aktarılan Canlı Soru: ${totalRealtimeUploaded}`);
  console.log('=============================================\n');
}

main().catch(err => {
  console.error('❌ Kritik Hata:', err);
  process.exit(1);
});
