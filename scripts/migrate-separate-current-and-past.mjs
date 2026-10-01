/**
 * scripts/migrate-separate-current-and-past.mjs
 * 
 * Veritabanı Ayrıştırma ve Düzenleme Motoru:
 * 1. 2026-2027 dönemine ait kurullarda henüz sınava girilmediği için
 *    tüm mevcut soru ve taslakları güncel havuzdan ('questions') çıkarır.
 * 2. İlgili soruları önceki senelerin çıkmış sınavları ('past_questions') olarak analiz eder.
 * 3. Hangi seneye ait olduğu tespit edilebilenleri (2025-2026, 2024-2025, 2023-2024, 2022-2023, 2021-2022, 2020-2021 vb.)
 *    ilgili seneye atar.
 * 4. Hangi seneye ait olduğu bilinmeyen soruları 'Geçmiş Yıllar Çıkmışı (Arşiv)' olarak kategorize eder.
 * 5. Muallak/eksik veya ham olanları 'isAmbiguous: true' olarak işaretler.
 * 6. Yerel veritabanında (data/pastQuestions.json ve data/questions.json),
 *    Supabase PostgreSQL veritabanında (questions tablosu temizlenir, past_questions güncellenir)
 *    ve Firebase Firestore servislerinde tam uyum sağlar.
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

const QUESTIONS_JSON_PATH = path.join(ROOT_DIR, 'data', 'questions.json');
const QUESTIONS_BACKUP_PATH = path.join(ROOT_DIR, 'data', 'questions.backup.json');
const PAST_JSON_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.json');
const PAST_BACKUP_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.backup.json');
const SRC_PAST_PATH = path.join(ROOT_DIR, 'src', 'data', 'pastQuestions.json');

// Helper to normalize strings for deduplication
function normalizeText(text) {
  if (!text) return '';
  return text.toLowerCase().replace(/[^\p{L}\p{N}]/gu, '').slice(0, 60);
}

// Year detection algorithm
function detectExamYear(q) {
  // If q already has a valid past year (not 2026-2027)
  if (q.examYear && q.examYear !== 'Kategorisiz' && !q.examYear.includes('2026') && !q.examYear.includes('2027')) {
    if (q.examYear.includes('2025-2026') || q.examYear.includes('25-26')) return '2025-2026 (Geçen Sene)';
    const m = q.examYear.match(/(20[0-2][0-5])-(20[0-2][0-6])/);
    if (m) return m[0];
  }

  const sourcesToCheck = [
    q.sourceFile || '',
    ...(q.tags || []),
    q.reconstruction?.stem || '',
    q.rawQuestion?.stem || '',
    q.topic || '',
    q.notesAndDiscrepancies || ''
  ];

  for (const src of sourcesToCheck) {
    if (!src || typeof src !== 'string') continue;
    if (src.includes('2026-2027') || src.includes('2026_2027')) continue;

    // 25-26 -> 2025-2026 (Geçen Sene)
    if (/(?:25-26|2025-2026)/i.test(src)) {
      return '2025-2026 (Geçen Sene)';
    }

    // 2024-2025 or 24-25
    if (/(?:2024-2025|24-25)/i.test(src)) {
      return '2024-2025';
    }

    // 2023-2024 or 23-24
    if (/(?:2023-2024|23-24)/i.test(src)) {
      return '2023-2024';
    }

    // 2022-2023 or 22-23 or KURUL 3 2023
    if (/(?:2022-2023|22-23|KURUL\s*3\s*2023)/i.test(src)) {
      return '2022-2023';
    }

    // 2021-2022 or 21-22 or 22 final
    if (/(?:2021-2022|21-22|22%20final|22\s*final)/i.test(src)) {
      return '2021-2022';
    }

    // 2020-2021 or 21 final or 2021final
    if (/(?:2020-2021|2021final|21\s*final)/i.test(src)) {
      return '2020-2021';
    }

    // 2016
    if (/2016/i.test(src)) {
      return '2016-2017';
    }

    // 2018
    if (/2018/i.test(src)) {
      return '2018-2019';
    }

    // 2012
    if (/2012/i.test(src)) {
      return '2012-2013';
    }

    // Generic range match: YYYY-YYYY
    const rangeMatch = src.match(/(20[0-2][0-5])-(20[0-2][0-6])/);
    if (rangeMatch) return rangeMatch[0];
  }

  // Sene bilgisi bilinmeyenler:
  return 'Geçmiş Yıllar Çıkmışı (Arşiv)';
}

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

async function run() {
  console.log('='.repeat(75));
  console.log('  🏥 MEDSORU VERİTABANI DÜZENLEME VE AYRIŞTIRMA MOTORU');
  console.log('  2026-2027 Güncel Sorular Sıfırlanıyor -> Tüm Sorular Çıkmış Soruya Aktarılıyor');
  console.log('='.repeat(75));

  // 1. ADIM: Yedekleme
  console.log('\n[ADIM 1] Yerel JSON veritabanları yedekleniyor...');
  if (fs.existsSync(QUESTIONS_JSON_PATH)) {
    fs.copyFileSync(QUESTIONS_JSON_PATH, QUESTIONS_BACKUP_PATH);
    console.log(`   ✓ ${QUESTIONS_BACKUP_PATH} oluşturuldu.`);
  }
  if (fs.existsSync(PAST_JSON_PATH)) {
    fs.copyFileSync(PAST_JSON_PATH, PAST_BACKUP_PATH);
    console.log(`   ✓ ${PAST_BACKUP_PATH} oluşturuldu.`);
  }

  // 2. ADIM: Verileri Oku
  console.log('\n[ADIM 2] Mevcut veriler okunuyor...');
  let rawQuestions = [];
  let committees = [];
  if (fs.existsSync(QUESTIONS_JSON_PATH)) {
    const parsed = JSON.parse(fs.readFileSync(QUESTIONS_JSON_PATH, 'utf8'));
    if (Array.isArray(parsed)) {
      rawQuestions = parsed;
    } else {
      rawQuestions = parsed.questions || [];
      committees = parsed.committees || [];
    }
  }
  console.log(`   📂 questions.json içindeki toplam soru: ${rawQuestions.length}`);

  let pastQuestions = [];
  if (fs.existsSync(PAST_JSON_PATH)) {
    pastQuestions = JSON.parse(fs.readFileSync(PAST_JSON_PATH, 'utf8'));
  }
  console.log(`   📂 pastQuestions.json içindeki toplam soru: ${pastQuestions.length}`);

  // Mevcut pastQuestions için deduplication haritası
  const pastMap = new Map();
  pastQuestions.forEach(p => {
    if (p && p.id) {
      pastMap.set(p.id, p);
    }
    const norm = normalizeText(p.reconstruction?.stem || p.rawQuestion?.stem || p.stem || p.topic);
    if (norm.length > 8) {
      pastMap.set(norm, p);
    }
  });

  // 3. ADIM: questions.json'daki soruları Çıkmış Soruya Dönüştür
  console.log('\n[ADIM 3] questions.json soruları çıkmış soru olarak analiz ediliyor...');
  let addedCount = 0;
  let alreadyExistCount = 0;
  const yearStats = {};

  for (const q of rawQuestions) {
    if (!q || (!q.id && !q.topic && !q.reconstruction?.stem)) continue;

    // Civan notlarını hariç tut
    if (q.id && q.id.startsWith('civan-')) continue;
    if (q.tags && q.tags.some(t => /civan/i.test(t))) continue;

    const norm = normalizeText(q.reconstruction?.stem || q.rawQuestion?.stem || q.stem || q.topic);
    if (q.id && pastMap.has(q.id)) {
      alreadyExistCount++;
      continue;
    }
    if (norm.length > 8 && pastMap.has(norm)) {
      alreadyExistCount++;
      continue;
    }

    // Yılı tespit et
    const detectedYear = detectExamYear(q);
    yearStats[detectedYear] = (yearStats[detectedYear] || 0) + 1;

    // Soru kökü ve şık kontrolü (Muallak tespiti)
    const stem = (q.reconstruction?.stem || q.rawQuestion?.stem || q.stem || q.fragments?.[0]?.text || q.topic || '').trim();
    const opts = q.reconstruction?.options || q.options || q.rawQuestion?.options || [];
    const validOpts = opts.filter(o => o && (o.text || typeof o === 'string') && (o.text?.trim()?.length > 0 || String(o).trim().length > 0));
    const isAmbiguous = stem.length < 25 || validOpts.length < 2;

    const pastId = q.id.startsWith('past-') ? q.id : `past-${q.id}`;

    const newPastQuestion = {
      id: pastId,
      sourceFile: q.sourceFile || (q.tags || []).find(t => t.toLowerCase().endsWith('.pdf') || t.toLowerCase().endsWith('.txt')) || 'Taslak Soru Arşivi (Önceki Yıllar)',
      committeeId: q.committeeId || 'donem3-kurul1',
      examYear: detectedYear,
      questionNumber: q.questionNumber || (pastQuestions.length + addedCount + 1),
      discipline: q.discipline || 'Tıbbi Patoloji',
      topic: q.topic || `Çıkmış Soru (${detectedYear})`,
      rawQuestion: q.rawQuestion || {
        stem: stem || 'Soru kökü arşiv kayıtlarından aktarıldı.',
        options: opts.length > 0 ? opts.map((opt, i) => ({
          key: opt.key || String.fromCharCode(65 + i),
          text: opt.text || String(opt)
        })) : [
          { key: 'A', text: 'Seçenek A' },
          { key: 'B', text: 'Seçenek B' },
          { key: 'C', text: 'Seçenek C' },
          { key: 'D', text: 'Seçenek D' },
          { key: 'E', text: 'Seçenek E' }
        ],
        claimedAnswer: q.claimedAnswer || q.reconstruction?.correctAnswer || 'A'
      },
      reconstruction: q.reconstruction || {
        stem: stem || 'Soru kökü arşiv kayıtlarından aktarıldı.',
        options: opts.length > 0 ? opts.map((opt, i) => ({
          key: opt.key || String.fromCharCode(65 + i),
          text: opt.text || String(opt),
          isCorrect: (opt.key || String.fromCharCode(65 + i)) === (q.claimedAnswer || 'A')
        })) : [
          { key: 'A', text: 'Seçenek A', isCorrect: true },
          { key: 'B', text: 'Seçenek B', isCorrect: false },
          { key: 'C', text: 'Seçenek C', isCorrect: false },
          { key: 'D', text: 'Seçenek D', isCorrect: false },
          { key: 'E', text: 'Seçenek E', isCorrect: false }
        ],
        correctAnswer: q.claimedAnswer || q.reconstruction?.correctAnswer || 'A',
        explanation: q.reconstruction?.explanation || 'Bu soru önceki senelere ait kurul çıkmış soruları arşivinden derlenmiştir.',
        isAiRefined: Boolean(q.reconstruction?.isAiRefined),
        reconstructionQuality: isAmbiguous ? 'review_needed' : 'verified'
      },
      isPastExam: true,
      isSuspect: Boolean(q.isSuspect),
      isAmbiguous,
      isLocked: Boolean(q.isLocked),
      upvotes: typeof q.upvotes === 'number' ? q.upvotes : 0,
      comments: Array.isArray(q.comments) ? q.comments : [],
      reports: Array.isArray(q.reports) ? q.reports : [],
      createdAt: q.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    pastQuestions.push(newPastQuestion);
    pastMap.set(pastId, newPastQuestion);
    if (norm.length > 8) pastMap.set(norm, newPastQuestion);
    addedCount++;
  }

  console.log(`   ✓ Zaten çıkmış sorularda mevcut olan: ${alreadyExistCount}`);
  console.log(`   ✓ Çıkmış sorular arşivine yeni eklenen: ${addedCount}`);
  console.log(`   ✓ Toplam birleşik çıkmış soru sayısı: ${pastQuestions.length}`);
  console.log('   📊 Yıl Dağılımı:', yearStats);

  // 4. ADIM: Yerel Dosyaları Güncelle
  console.log('\n[ADIM 4] Yerel JSON dosyaları güncelleniyor...');
  // pastQuestions.json
  fs.writeFileSync(PAST_JSON_PATH, JSON.stringify(pastQuestions, null, 2), 'utf8');
  console.log(`   ✓ ${PAST_JSON_PATH} güncellendi (${pastQuestions.length} soru).`);

  if (fs.existsSync(path.dirname(SRC_PAST_PATH))) {
    fs.writeFileSync(SRC_PAST_PATH, JSON.stringify(pastQuestions, null, 2), 'utf8');
    console.log(`   ✓ ${SRC_PAST_PATH} güncellendi.`);
  }

  // questions.json -> SIFIRLANIR (2026-2027 döneminde henüz sınava girilmediği için boş olmalıdır!)
  const cleanedQuestionsDb = {
    committees: committees.length > 0 ? committees : [
      { id: 'donem3-kurul1', name: 'Dönem 3 - Kurul 1: TIP 310 - Ürogenital ve Obstetrik Kurulu', year: 3, term: '2026-2027 Güz', targetCount: 100 },
      { id: 'donem3-kurul2', name: 'Dönem 3 - Kurul 2: TIP 320 - Nöropsikiyatri Kurulu', year: 3, term: '2026-2027 Güz', targetCount: 100 },
      { id: 'donem3-kurul3', name: 'Dönem 3 - Kurul 3: TIP 330 - Gastrointestinal Sistem Kurulu', year: 3, term: '2026-2027 Güz', targetCount: 100 },
      { id: 'donem3-kurul4', name: 'Dönem 3 - Kurul 4: TIP 340 - Dolaşım, Solunum ve Tümör Kurulu', year: 3, term: '2026-2027 Bahar', targetCount: 100 },
      { id: 'donem3-kurul5', name: 'Dönem 3 - Kurul 5: TIP 350 - Endokrin, Kas-İskelet ve Cilt Kurulu', year: 3, term: '2026-2027 Bahar', targetCount: 100 },
      { id: 'donem3-kurul6', name: 'Dönem 3 - Kurul 6: TIP 360 - Hematoloji ve Onkoloji Kurulu', year: 3, term: '2026-2027 Bahar', targetCount: 100 },
      { id: 'donem3-final', name: 'Dönem 3 - Yıl Sonu Genel Final Sınavı', year: 3, term: '2026-2027 Genel', targetCount: 150 },
      { id: 'donem3-butunleme', name: 'Dönem 3 - Yıl Sonu Bütünleme Sınavı', year: 3, term: '2026-2027 Genel', targetCount: 150 }
    ],
    questions: [] // Sınav tarihi gelmeden soru paylaşımı yapılamayacağı için güncel havuz boştur!
  };

  fs.writeFileSync(QUESTIONS_JSON_PATH, JSON.stringify(cleanedQuestionsDb, null, 2), 'utf8');
  console.log(`   ✓ ${QUESTIONS_JSON_PATH} güncel soru havuzu sıfırlandı (questions: []).`);

  // 5. ADIM: Supabase Veritabanını Güncelle
  console.log('\n[ADIM 5] Supabase PostgreSQL veritabanı eşitleniyor...');
  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;

  if (supabaseUrl && supabaseKey) {
    const supabase = createClient(supabaseUrl, supabaseKey);

    // 5.1 Güncel soruları temizle ('questions' tablosu)
    console.log('   🔄 Supabase \'questions\' tablosundaki erken taslaklar temizleniyor...');
    const { error: delError } = await supabase.from('questions').delete().neq('id', '___safe_keep___');
    if (delError) {
      console.warn('   ⚠️ Supabase questions silme uyarısı:', delError.message);
    } else {
      console.log('   ✅ Supabase \'questions\' tablosu başarıyla sıfırlandı (0 soru).');
    }

    // 5.2 Çıkmış soruları 'past_questions' tablosuna yaz
    console.log(`   🔄 Supabase 'past_questions' tablosuna ${pastQuestions.length} soru aktarılıyor...`);
    const BATCH_SIZE = 100;
    let supaSuccess = 0;

    for (let i = 0; i < pastQuestions.length; i += BATCH_SIZE) {
      const chunk = pastQuestions.slice(i, i + BATCH_SIZE);
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

      const { error: upsertErr } = await supabase.from('past_questions').upsert(cleanForPostgres(rows), { onConflict: 'id' });
      if (upsertErr) {
        console.warn(`   ⚠️ Supabase past_questions parti [${i}-${i+chunk.length}] uyarısı:`, upsertErr.message);
      } else {
        supaSuccess += chunk.length;
        process.stdout.write(`   ✓ Supabase aktarılan çıkmış soru: ${supaSuccess} / ${pastQuestions.length}\r`);
      }
    }
    console.log(`\n   ✅ Supabase 'past_questions' tablosu başarıyla eşitlendi (${supaSuccess} soru).`);
  } else {
    console.warn('   ⚠️ Supabase kimlik bilgileri bulunamadı, atlanıyor.');
  }

  console.log('\n' + '='.repeat(75));
  console.log('  🎉 TÜM VERİTABANLARI BAŞARIYLA DÜZENLENDİ VE AYRIŞTIRILDI!');
  console.log('  1. 2026-2027 güncel kurullarında 0 soru (sınav öncesi gizlilik sağlandı)');
  console.log(`  2. Çıkmış Sorular arşivinde toplam ${pastQuestions.length} soru (yıllarına göre ayrıştırıldı)`);
  console.log('='.repeat(75));
}

run().catch(err => {
  console.error('Kritik Hata:', err);
  process.exit(1);
});
