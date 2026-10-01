/**
 * scripts/fix-question-typos.mjs
 * 
 * MedSoru Soru Yazım Hatalarını ve Bozuk OCR İfadelerini Tespit ve Düzeltme Motoru
 * 
 * Özellikler:
 * 1. Tire Bölünmelerini Düzeltir:
 *    - "Send- romu" -> "Sendromu"
 *    - "mev- cuttur" -> "mevcuttur"
 *    - "biri- kir" -> "birikir"
 *    - "ya- yılır" -> "yayılır"
 *    - Roman rakamlarını korur (II- Kolestiramin bozulmaz)
 *    - Biyolojik kısaltmaları korur (TGF-B, HLA-B27, anti-DNA bozulmaz)
 *    - Tıbbi önekleri korur (non- eozinofilik -> non-eozinofilik)
 * 2. Tıbbi ve Sınav Sözlüğü Hatalarını Düzeltir:
 *    - "etenol" -> "etanol"
 *    - "aseteldehit" -> "asetaldehit"
 *    - "endometriodi" -> "endometrioid"
 *    - "yanlştır" -> "yanlıştır", "aşağidakilerden" -> "aşağıdakilerden", vb.
 * 3. OCR Karakter Bozulmalarını Düzeltir:
 *    - "!" harfini kelime içinde "i" yapar ("hang!s!" -> "hangisi", "!nflamasyon" -> "inflamasyon")
 *    - Birbirine yapışmış kelimeleri ayırır ("görülenkanser" -> "görülen kanser")
 * 4. Soru Kökü Dilbilgisi İyileştirmeleri:
 *    - "hangi over tümörü ilişkili?" -> "hangi over tümörü ile ilişkilidir?"
 * 5. Yerel Dosyaları ve Opsiyonel Olarak Supabase'i Günceller (--fix, --sync-supabase)
 * 6. Detaylı JSON Raporu Üretir (data/spelling_errors_report.json)
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

const DATA_PAST_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.json');
const SRC_PAST_PATH = path.join(ROOT_DIR, 'src', 'data', 'pastQuestions.json');
const BACKUP_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.backup_before_typo_fix.json');
const REPORT_PATH = path.join(ROOT_DIR, 'data', 'spelling_errors_report.json');

// --- KORUNACAK ROMAN RAKAMLARI & MADDE NUMARALARI ---
const ROMAN_NUMERALS = new Set([
  'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
  'l', 'll', 'lll', 'Il', 'Ill', 'lI', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]);

// --- TIBBİ TİRE KORUNACAK ÖNEKLER ---
const PREFIXES_RETAIN_HYPHEN = new Set([
  'anti', 'non', 'pre', 'post', 'sub', 'oto', 'pan', 'intra', 'ekstra', 'inter', 'peri'
]);

// --- TIBBİ VE SINAV DİLİ YAZIM HATALARI SÖZLÜĞÜ ---
const MEDICAL_AND_EXAM_DICTIONARY = {
  // Kullanıcının belirttiği örnekler
  'etenol': 'etanol',
  'etenolün': 'etanolün',
  'etenole': 'etanole',
  'etenolü': 'etanolü',
  'aseteldehit': 'asetaldehit',
  'aseteldehiti': 'asetaldehiti',
  'aseteldehid': 'asetaldehit',
  'endometriodi': 'endometrioid',

  // Sık yapılan tıbbi yazım hataları
  'senderomu': 'sendromu',
  'senderom': 'sendrom',
  'mustasyon': 'mutasyon',
  'mustasyonlar': 'mutasyonlar',
  'karsinoru': 'karsinomu',
  'farmakoloj': 'farmakoloji',
  'glukagonoma': 'glukagonom',
  'staphyolococcus': 'staphylococcus',
  'inflarmasyona': 'inflamasyona',
  'inflarmasyon': 'inflamasyon',
  'waldenstrom': 'waldenström',
  'bartolin': 'bartholin',
  'kolestrol': 'kolesterol',
  'metobolizma': 'metabolizma',
  'metobolizması': 'metabolizması',
  'biyopsiyle': 'biyopsi ile',
  'perferik': 'periferik',
  'nflamatuar': 'inflamatuar',
  'nflamasyon': 'inflamasyon',
  'tümöru': 'tümörü',
  'karaciğerdeyağ': 'karaciğerde yağ',
  'görülenkanser': 'görülen kanser',
  'hangisiyanlıştır': 'hangisi yanlıştır',
  'hangisidoğrudur': 'hangisi doğrudur',

  // OCR Kaynaklı Soru Kökü Kelime Bozulmaları
  'yanlştır': 'yanlıştır',
  'yalnıştır': 'yanlıştır',
  'yanliştir': 'yanlıştır',
  'yanliştır': 'yanlıştır',
  'yanlıştr': 'yanlıştır',
  'yaniıştır': 'yanlıştır',
  'yanlılştır': 'yanlıştır',
  'aşağidakilerden': 'aşağıdakilerden',
  'aşağdakilerden': 'aşağıdakilerden',
  'aşağıdakierden': 'aşağıdakilerden',
  'aşagidakilerden': 'aşağıdakilerden',
  'asağidakilerden': 'aşağıdakilerden',
  'aşağdekilerden': 'aşağıdakilerden',
  'asagidakilerden': 'aşağıdakilerden',
  'asagidaki': 'aşağıdaki',
  'aşağidaki': 'aşağıdaki',
  'hanigisi': 'hangisi',
  'hafigisi': 'hangisi',
  'hangist': 'hangisi',
  'hengist': 'hangisi',
  'hangisş': 'hangisi',
  'hangsi': 'hangisi',
  'haneisi': 'hangisi',
  'hanigi': 'hangisi',
  'hangisidr': 'hangisidir',
  'hangsidir': 'hangisidir',
  'hangisidır': 'hangisidir',
  'dogrudur': 'doğrudur',
  'dogru': 'doğru',
  'yanlis': 'yanlış',
  'özellliklerinden': 'özelliklerinden',
  'özelliklertnden': 'özelliklerinden'
};

// Cümle düzeltmeleri (RegExp bazlı kalıplar)
const PHRASE_CORRECTIONS = [
  {
    regex: /\bhangi\s+over\s+tümörü\s+ilişkili\??/gi,
    replacement: 'hangi over tümörü ile ilişkilidir?'
  },
  {
    regex: /\bhangi\s+tümörle\s+ilişkili\??/gi,
    replacement: 'hangi tümör ile ilişkilidir?'
  },
  {
    regex: /\bhangisiyle\s+ilişkili\??/gi,
    replacement: 'hangisiyle ilişkilidir?'
  },
  {
    regex: /\bhangisi\s+ile\s+ilişkili\??/gi,
    replacement: 'hangisi ile ilişkilidir?'
  }
];

/**
 * Tek bir metin dizesini analiz edip tüm yazım ve OCR hatalarını düzeltir.
 */
export function cleanSpellingAndOcr(text) {
  if (!text || typeof text !== 'string') return { text, changes: [] };
  let result = text;
  const changes = [];

  // --- 1. OCR Karakter Bozulması: '!' yerine 'i' düzeltmesi ---
  // e.g. "hang!s!", "!nflamasyon", "egzers!z"
  const beforeExcl = result;
  // Kelime ortasında !
  result = result.replace(/(?<=[a-zA-ZğüşıöçĞÜŞİÖÇ])!(?=[a-zA-ZğüşıöçĞÜŞİÖÇ])/g, 'i');
  // Kelime başında ! (örn: "!nflamasyon")
  result = result.replace(/(^|\s)!(?=[a-zA-ZğüşıöçĞÜŞİÖÇ])/g, (m, p1) => `${p1}i`);
  // Kelime sonunda ! (örn: "hangisi!")
  result = result.replace(/(?<=[a-zA-ZğüşıöçĞÜŞİÖÇ])!(?=$|\s|[.,;:?()])/g, 'i');
  if (result !== beforeExcl) {
    changes.push({
      type: 'OCR_EXCLAMATION_REPAIR',
      from: beforeExcl,
      to: result,
      description: 'OCR ünlem (!) harf bozulması "i" harfine dönüştürüldü'
    });
  }

  // --- 2. OCR Satır Sonu Tire Bölünmeleri (Hyphenated Line Breaks) ---
  // e.g. "Send- romu" -> "Sendromu", "mev- cuttur" -> "mevcuttur", "biri- kir" -> "birikir"
  result = result.replace(/([a-zA-ZğüşıöçĞÜŞİÖÇ]{2,})-(?:\s+)([a-zA-ZğüşıöçĞÜŞİÖÇ]{2,})/g, (m, p1, p2) => {
    // Roman rakamları listeleme maddesiyse koru (II- Kolestiramin)
    if (ROMAN_NUMERALS.has(p1) || /^[IVXLCDMivxlcdm]+$/.test(p1)) {
      return m;
    }
    // Gen / Reseptör / Molekül kısaltmasıysa koru (TGF-B, HLA-B27)
    if (/^[A-Z0-9]{1,5}$/.test(p1) && /^[A-Z0-9]{1,2}$/.test(p2)) {
      return m;
    }
    // Tıbbi önek ise tireyi koru, aradaki OCR boşluğunu kaldır (non- eozinofilik -> non-eozinofilik)
    const p1Lower = p1.toLowerCase();
    if (PREFIXES_RETAIN_HYPHEN.has(p1Lower)) {
      const fixedPrefix = `${p1}-${p2}`;
      changes.push({
        type: 'PREFIX_HYPHEN_NORMALIZATION',
        from: m,
        to: fixedPrefix,
        description: `Tıbbi önek tire boşluğu giderildi: "${m}" -> "${fixedPrefix}"`
      });
      return fixedPrefix;
    }

    // Kelime parçalanmasıysa birleştir: "Send- romu" -> "Sendromu", "mev- cuttur" -> "mevcuttur"
    // İkinci parçanın baş harfini küçük harf yap
    const merged = p1 + p2.toLowerCase();
    changes.push({
      type: 'HYPHEN_SPLIT_MERGED',
      from: m,
      to: merged,
      description: `Bölünmüş kelime birleştirildi: "${m}" -> "${merged}"`
    });
    return merged;
  });

  // --- 3. Tıbbi Terim & Sınav Dili Sözlüğü Düzeltmeleri ---
  for (const [typo, correct] of Object.entries(MEDICAL_AND_EXAM_DICTIONARY)) {
    const reg = new RegExp(`\\b${typo}\\b`, 'gi');
    if (reg.test(result)) {
      result = result.replace(reg, (matched) => {
        let replacement = correct;
        if (matched[0] === matched[0].toUpperCase() && matched[0] !== matched[0].toLowerCase()) {
          replacement = correct.charAt(0).toUpperCase() + correct.slice(1);
        }
        changes.push({
          type: 'DICTIONARY_CORRECTION',
          from: matched,
          to: replacement,
          description: `Sözlük düzeltmesi: "${matched}" -> "${replacement}"`
        });
        return replacement;
      });
    }
  }

  // --- 4. Soru Kökü Dilbilgisi ve Cümle Düşüklüğü Düzeltmeleri ---
  for (const phrase of PHRASE_CORRECTIONS) {
    if (phrase.regex.test(result)) {
      const beforePhrase = result;
      result = result.replace(phrase.regex, (matched) => {
        changes.push({
          type: 'PHRASE_GRAMMAR_CORRECTION',
          from: matched,
          to: phrase.replacement,
          description: `Cümle kalıbı düzeltildi: "${matched}" -> "${phrase.replacement}"`
        });
        return phrase.replacement;
      });
    }
  }

  // --- 5. Fazla Boşluk ve Noktalama Temizliği ---
  // Çift boşlukları tek boşluğa indir
  result = result.replace(/[ \t]{2,}/g, ' ');
  // Soru işareti veya virgül öncesi gereksiz boşluğu sil ("hangisidir ?" -> "hangisidir?")
  result = result.replace(/\s+([?,.!])/g, '$1');

  return { text: result, changes };
}

/**
 * Tek bir soru objesinin tüm metin alanlarını temizler.
 */
export function cleanQuestionObject(q) {
  let modified = false;
  const itemChanges = [];

  // 1. rawQuestion.stem
  if (q.rawQuestion && q.rawQuestion.stem) {
    const res = cleanSpellingAndOcr(q.rawQuestion.stem);
    if (res.changes.length > 0) {
      modified = true;
      itemChanges.push({
        field: 'rawQuestion.stem',
        before: q.rawQuestion.stem,
        after: res.text,
        changes: res.changes
      });
      q.rawQuestion.stem = res.text;
    }
  }

  // 2. rawQuestion.options
  if (q.rawQuestion && Array.isArray(q.rawQuestion.options)) {
    q.rawQuestion.options.forEach((opt, idx) => {
      if (opt && opt.text) {
        const res = cleanSpellingAndOcr(opt.text);
        if (res.changes.length > 0) {
          modified = true;
          itemChanges.push({
            field: `rawQuestion.options[${opt.key || idx}]`,
            before: opt.text,
            after: res.text,
            changes: res.changes
          });
          opt.text = res.text;
        }
      }
    });
  }

  // 3. reconstruction.stem
  if (q.reconstruction && q.reconstruction.stem) {
    const res = cleanSpellingAndOcr(q.reconstruction.stem);
    if (res.changes.length > 0) {
      modified = true;
      itemChanges.push({
        field: 'reconstruction.stem',
        before: q.reconstruction.stem,
        after: res.text,
        changes: res.changes
      });
      q.reconstruction.stem = res.text;
    }
  }

  // 4. reconstruction.options
  if (q.reconstruction && Array.isArray(q.reconstruction.options)) {
    q.reconstruction.options.forEach((opt, idx) => {
      if (opt && opt.text) {
        const res = cleanSpellingAndOcr(opt.text);
        if (res.changes.length > 0) {
          modified = true;
          itemChanges.push({
            field: `reconstruction.options[${opt.key || idx}]`,
            before: opt.text,
            after: res.text,
            changes: res.changes
          });
          opt.text = res.text;
        }
      }
    });
  }

  // 5. reconstruction.explanation
  if (q.reconstruction && q.reconstruction.explanation) {
    const res = cleanSpellingAndOcr(q.reconstruction.explanation);
    if (res.changes.length > 0) {
      modified = true;
      itemChanges.push({
        field: 'reconstruction.explanation',
        before: q.reconstruction.explanation,
        after: res.text,
        changes: res.changes
      });
      q.reconstruction.explanation = res.text;
    }
  }

  if (modified) {
    q.updatedAt = new Date().toISOString();
  }

  return { isModified: modified, changes: itemChanges, question: q };
}

// Postgres için null bayt temizleyici
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
      if (!error) return true;
      console.warn(`Supabase Parti [${chunkIndex}/${total}] Deneme ${attempt} hatası:`, error.message);
    } catch (err) {
      console.warn(`Supabase Parti [${chunkIndex}/${total}] Deneme ${attempt} istisna:`, err.message);
    }
    await new Promise(r => setTimeout(r, 1500 * attempt));
  }
  return false;
}

// --- CLI ÇALIŞTIRICI ---
async function main() {
  const args = process.argv.slice(2);
  const isFix = args.includes('--fix');
  const isSyncSupabase = args.includes('--sync-supabase');
  const isVerbose = args.includes('--verbose');
  const targetIdArg = args.find(a => a.startsWith('--id='))?.split('=')[1] || (args.includes('--id') ? args[args.indexOf('--id') + 1] : null);

  console.log('='.repeat(75));
  console.log('  🔍 MEDSORU YAZIM VE OCR HATALARI TESPİT & DÜZELTME MOTORU');
  console.log('='.repeat(75));
  console.log(`Mod: ${isFix ? '🛠️  DÜZELT VE KAYDET (--fix)' : '👀  ÖNİZLEME & RAPORLAMA (DRY-RUN)'}`);
  if (targetIdArg) {
    console.log(`Hedef Soru ID: ${targetIdArg}`);
  }

  if (!fs.existsSync(DATA_PAST_PATH)) {
    console.error(`HATA: Veritabanı dosyası bulunamadı: ${DATA_PAST_PATH}`);
    process.exit(1);
  }

  const rawList = JSON.parse(fs.readFileSync(DATA_PAST_PATH, 'utf8'));
  console.log(`\nToplam Yüklenen Soru Sayısı: ${rawList.length}`);

  let questionsToProcess = rawList;
  if (targetIdArg) {
    questionsToProcess = rawList.filter(q => q.id === targetIdArg);
    if (questionsToProcess.length === 0) {
      console.error(`HATA: ${targetIdArg} ID'li soru bulunamadı!`);
      process.exit(1);
    }
  }

  const allModifications = [];
  const categoryCounts = {
    HYPHEN_SPLIT_MERGED: 0,
    DICTIONARY_CORRECTION: 0,
    OCR_EXCLAMATION_REPAIR: 0,
    PREFIX_HYPHEN_NORMALIZATION: 0,
    PHRASE_GRAMMAR_CORRECTION: 0
  };

  for (const q of questionsToProcess) {
    const result = cleanQuestionObject(q);
    if (result.isModified) {
      allModifications.push({
        id: q.id,
        sourceFile: q.sourceFile,
        committeeId: q.committeeId,
        discipline: q.discipline,
        changes: result.changes
      });

      result.changes.forEach(c => {
        c.changes.forEach(ch => {
          categoryCounts[ch.type] = (categoryCounts[ch.type] || 0) + 1;
        });
      });
    }
  }

  console.log('\n📊 TESPİT VE DÜZELTME İSTATİSTİKLERİ:');
  console.log(`   • İncelenen Soru Sayısı         : ${questionsToProcess.length}`);
  console.log(`   • Hata Tespit Edilen Soru Sayısı : ${allModifications.length} (%${((allModifications.length / questionsToProcess.length) * 100).toFixed(1)})`);
  console.log(`   • Toplam Düzeltilen Hata Sayısı  : ${Object.values(categoryCounts).reduce((a, b) => a + b, 0)}`);
  console.log('\nKategori Dağılımı:');
  console.log(`   - 🔤 Bölünmüş Kelimeler (Send- romu -> Sendromu) : ${categoryCounts.HYPHEN_SPLIT_MERGED || 0}`);
  console.log(`   - 💊 Tıbbi Sözlük (etenol -> etanol vb.)           : ${categoryCounts.DICTIONARY_CORRECTION || 0}`);
  console.log(`   - ⚡ OCR Ünlem Bozulması (!nflamasyon -> inflamasyon): ${categoryCounts.OCR_EXCLAMATION_REPAIR || 0}`);
  console.log(`   - 🔗 Tıbbi Önek Tire Düzeltmesi (non- eozinofilik): ${categoryCounts.PREFIX_HYPHEN_NORMALIZATION || 0}`);
  console.log(`   - 📝 Dilbilgisi & Cümle Tamamlama                 : ${categoryCounts.PHRASE_GRAMMAR_CORRECTION || 0}`);

  // Örnekleri listele (Özellikle kullanıcının bahsettiği sorular)
  console.log('\n🎯 KULLANICI ÖRNEKLERİ VE TEMEL DOĞRULAMA DURUMU:');
  const userSampleIds = [
    'past-1790877034650-998580', // Meig's Sendromu ve Bazal Hücreli Nevüs Send- romu
    'past-1790877034646-469265', // Hangi etenol metabolizmasından...
    'past-1790877034670-958753'  // TGF-B... mutasyon mev- cuttur?
  ];

  userSampleIds.forEach(sampleId => {
    const found = allModifications.find(m => m.id === sampleId);
    if (found) {
      console.log(`\n[ID: ${found.id}]`);
      found.changes.forEach(fieldChange => {
        console.log(`  🔹 Alan: ${fieldChange.field}`);
        console.log(`     Önce : "${fieldChange.before}"`);
        console.log(`     Sonra: "${fieldChange.after}"`);
      });
    }
  });

  if (isVerbose) {
    console.log('\n📋 TÜM DÜZELTİLEN SORULAR (Ayrıntılı):');
    allModifications.forEach((m, idx) => {
      console.log(`\n[${idx + 1}/${allModifications.length}] ID: ${m.id} (${m.discipline || 'Tıp'})`);
      m.changes.forEach(c => {
        console.log(`   • ${c.field}:`);
        console.log(`     - Önce : ${c.before}`);
        console.log(`     + Sonra: ${c.after}`);
      });
    });
  }

  // Rapor dosyasını yaz
  const report = {
    timestamp: new Date().toISOString(),
    totalAnalyzed: questionsToProcess.length,
    totalModifiedQuestions: allModifications.length,
    totalErrorsFixed: Object.values(categoryCounts).reduce((a, b) => a + b, 0),
    categoryCounts,
    modifications: allModifications
  };
  fs.writeFileSync(REPORT_PATH, JSON.stringify(report, null, 2), 'utf8');
  console.log(`\n📄 Ayrıntılı hata tespit raporu kaydedildi: ${REPORT_PATH}`);

  // Eğer --fix argümanı verilmişse dosyaları güncelle
  if (isFix) {
    console.log('\n💾 Düzeltmeler veritabanına uygulanıyor...');
    // Yedek al
    fs.writeFileSync(BACKUP_PATH, JSON.stringify(rawList, null, 2), 'utf8');
    console.log(`   ✓ Güvenlik yedeği alındı: ${BACKUP_PATH}`);

    // data/pastQuestions.json güncelle
    fs.writeFileSync(DATA_PAST_PATH, JSON.stringify(rawList, null, 2), 'utf8');
    console.log(`   ✓ Güncellendi: ${DATA_PAST_PATH}`);

    // src/data/pastQuestions.json güncelle
    if (fs.existsSync(path.dirname(SRC_PAST_PATH))) {
      fs.writeFileSync(SRC_PAST_PATH, JSON.stringify(rawList, null, 2), 'utf8');
      console.log(`   ✓ Güncellendi: ${SRC_PAST_PATH}`);
    }

    // Supabase eşitlemesi istenmişse
    if (isSyncSupabase) {
      const supabaseUrl = process.env.SUPABASE_URL;
      const supabaseKey = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;

      if (supabaseUrl && supabaseKey) {
        console.log(`\n☁️  Supabase 'past_questions' tablosu güncelleniyor...`);
        const supabase = createClient(supabaseUrl, supabaseKey);

        const modifiedQuestions = rawList.filter(q => allModifications.some(m => m.id === q.id));
        const BATCH_SIZE = 25;
        let synced = 0;
        const totalBatches = Math.ceil(modifiedQuestions.length / BATCH_SIZE);

        for (let i = 0; i < modifiedQuestions.length; i += BATCH_SIZE) {
          const chunk = modifiedQuestions.slice(i, i + BATCH_SIZE);
          const batchNum = Math.floor(i / BATCH_SIZE) + 1;
          const rows = chunk.map((q) => ({
            id: q.id,
            committee_id: q.committeeId,
            discipline: q.discipline || 'Tıbbi Patoloji',
            topic: q.topic || `Soru #${q.questionNumber || 'Arşiv'}`,
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
          if (ok) synced += chunk.length;
          process.stdout.write(`   ✓ Supabase: ${synced} / ${modifiedQuestions.length} soru güncellendi\r`);
        }
        console.log(`\n   🎉 Supabase senkronizasyonu tamamlandı: ${synced} soru güncellendi.`);
      } else {
        console.warn('   ⚠️ Supabase anahtarları bulunamadığı için Supabase eşitlemesi atlandı.');
      }
    }
    console.log('\n🎉 DÜZELTME İŞLEMİ BAŞARIYLA TAMAMLANDI!');
  } else {
    console.log('\n💡 Bilgi: Düzeltmeleri veritabanına ve dosyalara kalıcı olarak uygulamak için:');
    console.log('   node scripts/fix-question-typos.mjs --fix');
    console.log('   (Supabase ile de eşitlemek için: node scripts/fix-question-typos.mjs --fix --sync-supabase)');
  }
}

main().catch(err => {
  console.error('Kritik Hata:', err);
  process.exit(1);
});
