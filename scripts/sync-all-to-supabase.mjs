/**
 * scripts/sync-all-to-supabase.mjs
 * 
 * Veritabanı senkronizasyon motoru:
 * 1. Kurulları (Committees)
 * 2. Çıkmış Soruları (Past Questions - 2314 adet)
 * 3. Amfi Ders Notlarını (Lecture Notes)
 * Supabase PostgreSQL veritabanına aktarır.
 * Böylece Firebase Spark kotası dolduğunda veya kapalıyken
 * sistem %100 kesintisiz olarak Supabase üzerinden veri çeker!
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

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error('❌ HATA: SUPABASE_URL veya SUPABASE_KEY .env dosyasında bulunamadı!');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

console.log('🚀 [Supabase Sync] Başlatılıyor...');
console.log(`🔗 Veritabanı: ${SUPABASE_URL}`);

// 1. Kurullar
const INITIAL_COMMITTEES = [
  {
    id: 'donem3-kurul1',
    name: 'Dönem 3 - Kurul 1: TIP 310 - Ürogenital ve Obstetrik Kurulu',
    year: 3,
    term: '2026-2027 Güz',
    targetCount: 100,
    color: 'teal',
    code: 'TIP 310',
    examDate: '23 Ekim 2026',
    description: 'Tıbbi Patoloji, Enfeksiyon Hastalıkları, Üroloji, Tıbbi Genetik, Halk Sağlığı, Kadın Hastalıkları ve Doğum, Tıbbi Farmakoloji.',
    disciplines: ['Tıbbi Patoloji', 'Tıbbi Biyoloji ve Genetik', 'Tıbbi Biyokimya', 'Enfeksiyon Hastalıkları', 'Üroloji', 'Tıbbi Genetik', 'Halk Sağlığı', 'Kadın Hastalıkları ve Doğum', 'Tıbbi Farmakoloji']
  },
  {
    id: 'donem3-kurul2',
    name: 'Dönem 3 - Kurul 2: TIP 320 - Nöropsikiyatri Kurulu',
    year: 3,
    term: '2026-2027 Güz',
    targetCount: 100,
    color: 'indigo',
    code: 'TIP 320',
    examDate: '04 Aralık 2026',
    description: 'Tıbbi Farmakoloji, Psikiyatri, Nöroloji, Tıbbi Genetik, Aile Hekimliği, Beyin ve Sinir Cerrahisi, Tıbbi Patoloji, FTR, Anesteziyoloji.',
    disciplines: ['Tıbbi Farmakoloji', 'Psikiyatri', 'Nöroloji', 'Tıbbi Genetik', 'Aile Hekimliği', 'Beyin ve Sinir Cerrahisi', 'Tıbbi Patoloji', 'FTR', 'Anesteziyoloji ve Reanimasyon']
  },
  {
    id: 'donem3-kurul3',
    name: 'Dönem 3 - Kurul 3: TIP 330 - Gastrointestinal Sistem Kurulu',
    year: 3,
    term: '2026-2027 Güz',
    targetCount: 100,
    color: 'amber',
    code: 'TIP 330',
    examDate: '22 Ocak 2027',
    description: 'Tıbbi Farmakoloji, İç Hastalıkları, Tıbbi Patoloji, Çocuk Sağlığı ve Hastalıkları, Tıbbi Genetik, Enfeksiyon Hastalıkları.',
    disciplines: ['Tıbbi Farmakoloji', 'İç Hastalıkları', 'Tıbbi Patoloji', 'Çocuk Sağlığı ve Hastalıkları', 'Tıbbi Genetik', 'Enfeksiyon Hastalıkları']
  },
  {
    id: 'donem3-kurul4',
    name: 'Dönem 3 - Kurul 4: TIP 340 - Dolaşım, Solunum ve Tümör Kurulu',
    year: 3,
    term: '2026-2027 Bahar',
    targetCount: 100,
    color: 'rose',
    code: 'TIP 340',
    examDate: '26 Mart 2027',
    description: 'Kardiyoloji, Göğüs Hastalıkları, Onkoloji, Patoloji ve Farmakoloji entegrasyonu.',
    disciplines: ['Tıbbi Farmakoloji', 'Tıbbi Patoloji', 'Kardiyoloji', 'Göğüs Hastalıkları', 'Göğüs Cerrahisi', 'Kalp Damar Cerrahisi', 'Çocuk Sağlığı ve Hastalıkları', 'Tıbbi Genetik']
  },
  {
    id: 'donem3-kurul5',
    name: 'Dönem 3 - Kurul 5: TIP 350 - Endokrin, Kas-İskelet ve Cilt Kurulu',
    year: 3,
    term: '2026-2027 Bahar',
    targetCount: 100,
    color: 'emerald',
    code: 'TIP 350',
    examDate: '07 Mayıs 2027',
    description: 'Endokrinoloji, Romatoloji, Ortopedi, Dermatoloji ve Patoloji sistemleri.',
    disciplines: ['Tıbbi Farmakoloji', 'Tıbbi Patoloji', 'İç Hastalıkları (Endokrin/Romatoloji)', 'Ortopedi ve Travmatoloji', 'Deri ve Zührevi Hastalıklar', 'Çocuk Sağlığı ve Hastalıkları', 'Tıbbi Genetik']
  },
  {
    id: 'donem3-kurul6',
    name: 'Dönem 3 - Kurul 6: TIP 360 - Hematoloji ve Onkoloji Kurulu',
    year: 3,
    term: '2026-2027 Bahar',
    targetCount: 100,
    color: 'purple',
    code: 'TIP 360',
    examDate: '11 Haziran 2027',
    description: 'Hematopoetik sistem, lenfoid doku patolojileri ve onkolojik mekanizmalar.',
    disciplines: ['Hematoloji', 'Onkoloji', 'Tıbbi Farmakoloji', 'Tıbbi Patoloji', 'Tıbbi Biyokimya', 'Tıbbi Genetik', 'Çocuk Hematoloji-Onkoloji']
  },
  {
    id: 'donem3-final',
    name: 'Dönem 3 - Yıl Sonu Genel Final & Bütünleme Sınavı',
    year: 3,
    term: '2026-2027 Genel',
    targetCount: 150,
    color: 'blue',
    code: 'TIP 300-FINAL',
    examDate: 'Temmuz 2027',
    description: 'Tüm kurulları kapsayan yıl sonu genel tıp değerlendirme sınavı.',
    disciplines: ['Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'İç Hastalıkları', 'Pediatri', 'Genel Cerrahi', 'Kadın Doğum', 'Tıbbi Genetik', 'Halk Sağlığı']
  }
];

async function syncCommittees() {
  console.log('\n📚 1/3 Kurullar Supabase\'e yazılıyor...');
  const rows = INITIAL_COMMITTEES.map(c => ({
    id: c.id,
    name: c.name,
    academic_year: c.term || '2026-2027',
    target_questions: c.targetCount || 100,
    color: c.color || 'teal',
    data: c
  }));

  const { error } = await supabase.from('committees').upsert(rows, { onConflict: 'id' });
  if (error) {
    console.error('❌ Kurul aktarım hatası:', error.message);
  } else {
    console.log(`✅ ${rows.length} Kurul başarıyla Supabase'e kaydedildi.`);
  }
}

// 2. Çıkmış Sorular
async function syncPastQuestions() {
  console.log('\n📝 2/3 Çıkmış Sorular Supabase\'e yazılıyor...');
  const pastPath = path.join(ROOT_DIR, 'data', 'pastQuestions.json');
  if (!fs.existsSync(pastPath)) {
    console.warn('⚠️ pastQuestions.json bulunamadı!');
    return;
  }

  const list = JSON.parse(fs.readFileSync(pastPath, 'utf8'));
  console.log(`Toplam ${list.length} soru bulundu. Partiler halinde (50'şerli) yükleniyor...`);

  const BATCH_SIZE = 50;
  let successCount = 0;

  for (let i = 0; i < list.length; i += BATCH_SIZE) {
    const chunk = list.slice(i, i + BATCH_SIZE);
    const rows = chunk.map(q => ({
      id: q.id,
      committee_id: q.committeeId,
      discipline: q.discipline || 'Tıbbi Patoloji',
      topic: q.topic || `Soru #${q.questionNumber || i + 1}`,
      exam_year: q.examYear || '2026-2027',
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

    const { error } = await supabase.from('past_questions').upsert(rows, { onConflict: 'id' });
    if (error) {
      console.warn(`Parti [${i} - ${i + chunk.length}] hatası:`, error.message);
    } else {
      successCount += chunk.length;
      process.stdout.write(`\rİlerleme: ${successCount} / ${list.length} soru aktarıldı...`);
    }
  }
  console.log(`\n✅ Toplam ${successCount} çıkmış soru Supabase'e başarıyla aktarıldı!`);
}

// 3. Amfi Ders Notları
async function syncLectureNotes() {
  console.log('\n📖 3/3 Amfi Ders Notları Supabase\'e yazılıyor...');
  const notesPath = path.join(ROOT_DIR, 'data', 'lecture_notes.json');
  if (!fs.existsSync(notesPath)) {
    console.warn('⚠️ lecture_notes.json bulunamadı!');
    return;
  }

  const notes = JSON.parse(fs.readFileSync(notesPath, 'utf8'));
  console.log(`Toplam ${notes.length} ders notu bulundu. Partiler halinde yükleniyor...`);

  const BATCH_SIZE = 25;
  let successCount = 0;

  for (let i = 0; i < notes.length; i += BATCH_SIZE) {
    const chunk = notes.slice(i, i + BATCH_SIZE);
    const rows = chunk.map(n => ({
      id: n.id,
      committee_id: n.committeeId || 'donem3-kurul1',
      discipline: n.discipline || 'Tıp Ders Notu',
      title: n.title,
      pages: (n.pages || []).slice(0, 50), // İlk 50 sayfa detaylı
      page_count: n.pageCount || (n.pages ? n.pages.length : 0),
      data: {
        id: n.id,
        title: n.title,
        discipline: n.discipline,
        committeeId: n.committeeId,
        sourcePdf: n.sourcePdf,
        totalSlides: n.pageCount || (n.pages ? n.pages.length : 0)
      }
    }));

    const { error } = await supabase.from('lecture_notes').upsert(rows, { onConflict: 'id' });
    if (error) {
      console.warn(`Ders notu parti [${i}] hatası:`, error.message);
    } else {
      successCount += chunk.length;
      process.stdout.write(`\rİlerleme: ${successCount} / ${notes.length} ders notu aktarıldı...`);
    }
  }
  console.log(`\n✅ Toplam ${successCount} ders notu Supabase'e başarıyla aktarıldı!`);
}

async function main() {
  await syncCommittees();
  await syncPastQuestions();
  await syncLectureNotes();
  console.log('\n🎉 [TAMAMLANDI] Supabase artık tüm kurullar, çıkmış sorular ve ders notları ile hazır!');
  console.log('Firebase Spark devre dışı kaldığında MedSoru otomatik olarak Supabase üzerinden çalışmaya devam edecektir.');
}

main().catch(err => {
  console.error('Kritik senkronizasyon hatası:', err);
});
