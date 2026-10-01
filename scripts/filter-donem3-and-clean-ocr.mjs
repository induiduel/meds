/**
 * scripts/filter-donem3-and-clean-ocr.mjs
 * 
 * 1. Dönem 3 müfredatına (Tıbbi Patoloji, Farmakoloji, Dahiliye, Kardiyoloji, Pediatri,
 *    Üroloji, Kadın Doğum, Enfeksiyon, Ortopedi, Acil Tıp, Nöroloji, Psikiyatri, FTR, Genetik vb.)
 *    uygun çıkmış soruları tespit eder.
 * 2. 'tüm sorular.txt' dosyasından gelen ve aslında Dönem 2'ye ait olan Anatomi, Histoloji,
 *    normal Fizyoloji ve Biyofizik sorularını ayıklar; yalnızca Dönem 3'e ait gerçek Patoloji
 *    ve klinik sorularını korur.
 * 3. Hatalı OCR okumalarını (anlaşılmayan bozuk karakterler, portal url/tablo çöpleri,
 *    birbirine girmiş şıklar, cevap anahtarı dump'ları) kesin olarak eler.
 * 4. Yerel veritabanlarını (data/pastQuestions.json ve src/data/pastQuestions.json) günceller.
 * 5. Supabase 'past_questions' tablosunu temizleyip arındırılmış sorularla eşitler.
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
const BACKUP_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.backup.json');
const REPORT_PATH = path.join(ROOT_DIR, 'data', 'eliminated_questions_report.json');

// --- DÖNEM 3 PATOLOJİ VE KLİNİK ANAHTAR KELİMELERİ ---
const PATHOLOGY_AND_CLINICAL_KEYWORDS = [
  'patoloji', 'patolojik', 'nekroz', 'apoptoz', 'karsinom', 'adenokarsinom', 'karsinoma', 'tümör', 'tumör',
  'neoplaz', 'neoplastik', 'enflamasyon', 'inflamasyon', 'iltihap', 'granülom', 'granülomatöz',
  'atero', 'ateroskleroz', 'aterom', 'infarkt', 'infarktüs', 'iskemi', 'iskemik', 'tromboz', 'trombüs',
  'emboli', 'embolizm', 'siroz', 'hepatit', 'gastrit', 'kolit', 'glomerülo', 'glomerülonefrit',
  'nefritik', 'nefrotik', 'metaplazi', 'displazi', 'hipertrofi', 'hiperplazi', 'atrofi', 'amiloid', 'amiloidoz',
  'eksüda', 'transüda', 'kanser', 'metastaz', 'metastatik', 'kazeifikasyon', 'koagülasyon nekrozu',
  'likefaksiyon', 'gangren', 'steatoz', 'lipofuscin', 'kalsifikasyon', 'dev hücre', 'epiteloid',
  'anaplaz', 'anaplastik', 'lösemi', 'lenfoma', 'melanom', 'karsinogenez', 'fibrozis', 'kist hidatik',
  'granülasyon dokusu', 'onkojen', 'tümör süpresör', 'p53', 'karsinoid', 'polip', 'ülseratif kolit',
  'crohn', 'barrett', 'lezyon', 'ödem patofizyolojisi', 'şok patofizyolojisi', 'hücre hasarı',
  'hücre ölümü', 'doku onarımı', 'skar', 'keloid', 'otoimmün', 'vaskülit', 'tüberküloz', 'lepra',
  'sifiliz', 'sarılık', 'sirozda kollajen', 'granülomatozis', 'endokrin patoloji', 'diyabet patolojisi',
  'tiroid patolojisi', 'menenjit patolojisi', 'akut faz reaktanı', 'warthin finkeldey', 'hpv', 'dane partikülü',
  'toksoplazma', 'bruselloz', 'negri cisimciği', 'ektima gangrenosum'
];

// --- DÖNEM 2 SAF ANATOMİ / HİSTOLOJİ / EMBRİYOLOJİ / NORMAL FİZYOLOJİ / BİYOFİZİK TERİMLERİ ---
const DONEM2_EXCLUSION_KEYWORDS = [
  'mediastinum posterius', 'mediastinum anterius', 'a. subclavia', 'a. carotis', 'a. axillaris', 'a. brachialis',
  'a. radialis', 'a. ulnaris', 'a. femoralis', 'a. tibialis', 'v. azygos', 'v. hemiazygos', 'v. saphena',
  'v. cephalica', 'v. basilica', 'truncus coeliacus', 'truncus pulmonalis', 'truncus brachiocephalicus',
  'rete articulare', 'rima glottidis', 'ligamentum arteriosum', 'ligamentum vocale', 'ligamentum patellae',
  'ligamentum teres', 'ligamentum trietz', 'trietz ligamenti', 'm. cricothyroideus', 'm. vocalis',
  'm. cricoarytenoideus', 'm. thyroarytenoideus', 'm. biceps', 'm. triceps', 'm. deltoideus',
  'm. gastrocnemius', 'm. quadriceps', 'plexus brachialis', 'plexus lumbalis', 'plexus cervicalis',
  'n. medianus', 'n. ulnaris', 'n. radialis', 'n. femoralis', 'n. ischiadicus', 'n. vagus anatomisi',
  'sinus sphenoidalis anatomisi', 'sinus maxillaris', 'sinus frontalis', 'meatus nasi', 'os sphenoidale',
  'os ethmoidale', 'os temporale', 'concha nasalis', 'trigonum fibrosum', 'sulcus coronarius',
  'valva mitralis dinleme', 'valva aortae dinleme', 'nodus atrioventriculare', 'nodus sinuatrialis anatomisi',
  'alveol transmüral basınç', 'poiseuille', 'laplace kanunu', 'alveol yüzey gerilimi',
  'blastokist', 'morula', 'trofoblast', 'sinsityotrofoblast', 'sitotrofoblast', 'koryon villusları gelişimi',
  'somit', 'nöral tüp kapanması', 'brankiyal yarık', 'faringeal ark anatomisi', 'kardiyak tüp gelişimi',
  'lamina propria histolojisi', 'gevşek bağ dokusu', 'hyalin kıkırdak', 'elastik kıkırdak', 'fibrokıkırdak',
  'osteon', 'havers kanalı', 'volkmann', 'çizgili kas bantları', 'a bandı', 'ı bandı', 'sarcomer',
  'sarkomer boyu', 'aksiyon potansiyeli fazları', 'depolarizasyon hızı', 'refrakter periyot fizyolojisi',
  'dii qrs kompleksi aks', 'kalbin elektrik aksı', 'bainbridge refleksi fizyolojisi',
  'solunum mekaniği spirometri', 'rezidüel hacim', 'vital kapasite fizyolojisi',
  'toraks duvarı, diyafram, mediasten', 'kalbe giren ve çıkan büyük damarlar', 'burun ve paranasal sinusler',
  'larynx anatomisi', 'üst extremite arter ve venleri', 'gövde ve alt ekstremitenin arter ve venleri'
];

/**
 * Hatalı / Bozuk OCR Kontrolü
 */
export function checkFaultyOcr(q) {
  const stem = (q.rawQuestion && q.rawQuestion.stem) || '';
  const options = (q.rawQuestion && q.rawQuestion.options) || [];
  const fullText = (stem + ' ' + options.map(o => o.text || '').join(' ')).trim();

  // 1. Web portalı URL'si veya ekran kazıma başlığı
  if (stem.includes('karabuk.edu.tr') || stem.includes('Anal z/') || stem.includes('Ders / Ünite /Konu') || stem.includes('Sıra No Ders')) {
    return { isFaulty: true, reason: 'Portal ekran kazıma / URL başlığı' };
  }

  // 2. Sınav idari metinleri (soru metni değil)
  if (stem.includes('Bu sınav toplam') && stem.includes('sorudan oluşmaktadır')) {
    return { isFaulty: true, reason: 'Sınav idari yönerge metni (soru değil)' };
  }

  // 3. Yalnızca şık harflerinden oluşan cevap anahtarı dump'ı
  if (/^[A-E\s]{6,}$/.test(stem.trim()) || stem.trim() === 'C B C D D D' || stem.startsWith('Cevap Anahtarı:')) {
    return { isFaulty: true, reason: 'Ham cevap anahtarı harf yığını' };
  }

  // 4. Eksik veya bağlamsız soru kökü
  if (stem.trim().length === 0 || ['Hangisi doğrudur?', 'Hangisi yanlıştır?', 'Terminal sinir'].includes(stem.trim())) {
    return { isFaulty: true, reason: 'Boş veya kesilmiş/bağlamsız soru kökü' };
  }

  // 5. Birbirine girmiş tablo dump'ı (tek bir seçenekte 650 karakterden uzun metin)
  if (options.some(o => (o.text || '').length > 650)) {
    return { isFaulty: true, reason: 'Şık içine sıkışmış ayrıştırılamayan tablo yığını (>650 kr)' };
  }

  // 6. Kök içinde 3 veya daha fazla tablo başlığı tekrarı
  const siraNoCount = (stem.match(/Sıra No/gi) || []).length;
  if (siraNoCount >= 3) {
    return { isFaulty: true, reason: 'Soru kökünde tekrarlayan tablo başlığı dökümü' };
  }

  // 7. Okunamayan anlamsız OCR çöpü karakter grupları
  if (/\b(?:SzRARM|mpsziz|pfBğösr|vndgu7|krv9|xkp\w+|pBğösr|EBEs\$|Egağ|Söse|Saz ör)\b/i.test(fullText)) {
    return { isFaulty: true, reason: 'Okunamayan anlamsız OCR karakter çöpü' };
  }

  // 8. Null byte veya ağır bozuk karakter kodlaması
  if (stem.includes('\u0000') || (stem.match(/[\uFFFD]/g) || []).length > 2) {
    return { isFaulty: true, reason: 'Null bayt / ağır karakter kodlama hasarı' };
  }

  // 9. Ağır font bozulması: kelime içlerinde yoğun ünlem işareti (>10 adet)
  const exclCount = (stem.match(/!/g) || []).length;
  if (exclCount > 10) {
    return { isFaulty: true, reason: `Ağır font hasarı / ünlem karakter bozulması (${exclCount} adet)` };
  }

  // 10. Kök içinde birbirine kaynamış birden fazla soru ve cevap sızıntısı
  if (stem.includes('Cevap=') && stem.includes('Hang!s!') || stem.includes('--> Der!')) {
    return { isFaulty: true, reason: 'Kök içine yapışmış birden çok soru ve cevap' };
  }

  return { isFaulty: false };
}

/**
 * Dönem 3 Müfredat Uygunluk Kontrolü
 */
export function checkDonem3Eligibility(q) {
  const isTum = (q.sourceFile || '').includes('tüm sorular') || (q.sourceFile || '').includes('tum sorular');
  const stem = (q.rawQuestion && q.rawQuestion.stem) || '';
  const options = (q.rawQuestion && q.rawQuestion.options) || [];
  const fullText = (stem + ' ' + options.map(o => o.text || '').join(' ')).trim().toLowerCase();

  if (isTum) {
    // tüm sorular.txt dosyasından yalnızca gerçek Patoloji ve Dönem 3 klinik soruları korunur
    const isPathology = PATHOLOGY_AND_CLINICAL_KEYWORDS.some(kw => fullText.includes(kw));
    const isDonem2 = DONEM2_EXCLUSION_KEYWORDS.some(kw => fullText.includes(kw));

    if (isPathology && !isDonem2) {
      return { isEligible: true, isFromTum: true };
    } else {
      return { isEligible: false, reason: 'Dönem 2 İçeriği (Anatomi, Histoloji, Normal Fizyoloji, Biyofizik)' };
    }
  } else {
    // Diğer dosyalardan gelen sorularda Dönem 2 içeriği kontrolü
    const isStrictDonem2 = DONEM2_EXCLUSION_KEYWORDS.some(kw => fullText.includes(kw)) &&
                           !PATHOLOGY_AND_CLINICAL_KEYWORDS.some(kw => fullText.includes(kw));
    if (isStrictDonem2) {
      return { isEligible: false, reason: 'Sınav dosyasında Dönem 2 İçeriği' };
    }
    return { isEligible: true, isFromTum: false };
  }
}

// Postgres için null byte ve özel karakter temizliği
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
      console.warn(`Supabase Parti [${chunkIndex}/${total}] Deneme ${attempt} hatası:`, error.message);
    } catch (err) {
      console.warn(`Supabase Parti [${chunkIndex}/${total}] Deneme ${attempt} istisna:`, err.message);
    }
    await new Promise(r => setTimeout(r, 1500 * attempt));
  }
  return false;
}

async function main() {
  console.log('='.repeat(70));
  console.log('  🏥 DÖNEM 3 MÜFREDAT FİLTRESİ VE BOZUK OCR TEMİZLEME MOTORU');
  console.log('='.repeat(70));

  const rawList = JSON.parse(fs.readFileSync(DATA_PAST_PATH, 'utf8'));
  console.log(`\n1. Başlangıç Soru Sayısı: ${rawList.length}`);

  // Yedek oluştur
  fs.writeFileSync(BACKUP_PATH, JSON.stringify(rawList, null, 2), 'utf8');
  console.log(`   💾 Orijinal veritabanı yedeği alındı: ${BACKUP_PATH}`);

  const kept = [];
  const eliminated = [];
  let badOcrCount = 0;
  let donem2Count = 0;
  let preservedTumCount = 0;
  let preservedOtherCount = 0;

  for (const q of rawList) {
    const ocr = checkFaultyOcr(q);
    if (ocr.isFaulty) {
      badOcrCount++;
      eliminated.push({
        id: q.id,
        source: q.sourceFile,
        category: 'Hatalı / Bozuk OCR',
        reason: ocr.reason,
        stem: (q.rawQuestion && q.rawQuestion.stem) || ''
      });
      continue;
    }

    const d3 = checkDonem3Eligibility(q);
    if (!d3.isEligible) {
      donem2Count++;
      eliminated.push({
        id: q.id,
        source: q.sourceFile,
        category: 'Dönem 2 Sorusudur (Dönem 3 Dışı)',
        reason: d3.reason,
        stem: (q.rawQuestion && q.rawQuestion.stem) || ''
      });
      continue;
    }

    if (d3.isFromTum) {
      preservedTumCount++;
      q.discipline = 'Tıbbi Patoloji';
    } else {
      preservedOtherCount++;
    }

    // Temiz soru
    kept.push(q);
  }

  console.log('\n2. Ayıklama Sonuçları:');
  console.log(`   ❌ Hatalı / Bozuk OCR Nedeniyle Elenenler : ${badOcrCount}`);
  console.log(`   ❌ Dönem 2 (Dönem 3 Dışı) Nedeniyle Elenenler: ${donem2Count}`);
  console.log(`   ✅ KORUNAN DÖNEM 3 ÇIKMIŞ SORU SAYISI     : ${kept.length}`);
  console.log(`      * 'tüm sorular' dosyasından Patoloji    : ${preservedTumCount}`);
  console.log(`      * Diğer çıkmış sınav dosyalarından       : ${preservedOtherCount}`);

  // Rapor kaydet
  fs.writeFileSync(REPORT_PATH, JSON.stringify({
    timestamp: new Date().toISOString(),
    totalInitial: rawList.length,
    totalKept: kept.length,
    badOcrCount,
    donem2Count,
    preservedTumCount,
    preservedOtherCount,
    eliminatedSamples: eliminated.slice(0, 50),
    eliminatedTotalCount: eliminated.length
  }, null, 2), 'utf8');
  console.log(`   📋 Detaylı elenen sorular raporu oluşturuldu: ${REPORT_PATH}`);

  // 3. Yerel JSON Dosyalarını Güncelle
  fs.writeFileSync(DATA_PAST_PATH, JSON.stringify(kept, null, 2), 'utf8');
  fs.writeFileSync(SRC_PAST_PATH, JSON.stringify(kept, null, 2), 'utf8');
  console.log(`\n3. Yerel Dosyalar Güncellendi:`);
  console.log(`   ✓ ${DATA_PAST_PATH} (${kept.length} soru)`);
  console.log(`   ✓ ${SRC_PAST_PATH} (${kept.length} soru)`);

  // 4. Supabase 'past_questions' Eşitlemesi
  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY;

  if (supabaseUrl && supabaseKey) {
    console.log(`\n4. Supabase 'past_questions' Tablosu Temizlenip Güncelleniyor...`);
    const supabase = createClient(supabaseUrl, supabaseKey);

    // Önceki tablodaki elenenleri kaldırmak için tabloyu temizle
    const { error: delError } = await supabase.from('past_questions').delete().neq('id', 'placeholder_keep_none');
    if (delError) {
      console.warn('   ⚠️ Supabase temizleme uyarısı:', delError.message);
    } else {
      console.log('   ✓ Supabase past_questions tablosu sıfırlandı.');
    }

    // Partiler halinde aktar
    const BATCH_SIZE = 25;
    let synced = 0;
    const totalBatches = Math.ceil(kept.length / BATCH_SIZE);

    for (let i = 0; i < kept.length; i += BATCH_SIZE) {
      const chunk = kept.slice(i, i + BATCH_SIZE);
      const batchNum = Math.floor(i / BATCH_SIZE) + 1;
      const rows = chunk.map((q, idx) => ({
        id: q.id,
        committee_id: q.committeeId,
        discipline: q.discipline || 'Tıbbi Patoloji',
        topic: q.topic || `Soru #${q.questionNumber || i + idx + 1}`,
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
        synced += chunk.length;
      }
      process.stdout.write(`   ✓ Supabase: ${synced} / ${kept.length} aktarıldı\r`);
    }

    // Nihai sayıyı doğrula
    const { count: finalCount } = await supabase.from('past_questions').select('*', { count: 'exact', head: true });
    console.log(`\n   🎉 Supabase senkronizasyonu tamamlandı: Doğrulanan Veritabanı Kayıt Sayısı: ${finalCount}`);
  } else {
    console.warn('   ⚠️ Supabase anahtarları bulunamadı, Supabase eşitlemesi atlandı.');
  }

  console.log('\n' + '='.repeat(70));
  console.log('  ✨ TÜM AYIKLAMA VE VERİTABANI GÜNCELLEMESİ BAŞARIYLA BİTTİ!');
  console.log('='.repeat(70));
}

main().catch(err => {
  console.error('Kritik Hata:', err);
  process.exit(1);
});
