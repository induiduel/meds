import fs from 'fs';

const pq = JSON.parse(fs.readFileSync('data/pastQuestions.json', 'utf8'));
const curriculum = JSON.parse(fs.readFileSync('data/donem3_curriculum.json', 'utf8'));

// High-yield Dönem 3 Pathology, Microbiology/Infectious disease, Genetics, and Clinical terms
const pathologyKeywords = [
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

// Pure Dönem 2 normal anatomy / histology / embryology / normal physiology / biophysics terms
const donem2ExclusionKeywords = [
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

export function checkFaultyOcr(q) {
  const stem = (q.rawQuestion && q.rawQuestion.stem) || '';
  const options = (q.rawQuestion && q.rawQuestion.options) || [];
  const fullText = (stem + ' ' + options.map(o => o.text || '').join(' ')).trim();

  // 1. Portal header / URL scrape
  if (stem.includes('karabuk.edu.tr') || stem.includes('Anal z/') || stem.includes('Ders / Ünite /Konu') || stem.includes('Sıra No Ders')) {
    return { isFaulty: true, reason: 'Portal scrape / URL header' };
  }

  // 2. Exam administrative meta instructions
  if (stem.includes('Bu sınav toplam') && stem.includes('sorudan oluşmaktadır')) {
    return { isFaulty: true, reason: 'Exam administrative instructions' };
  }

  // 3. Raw answer key text
  if (/^[A-E\s]{6,}$/.test(stem.trim()) || stem.trim() === 'C B C D D D' || stem.startsWith('Cevap Anahtarı:')) {
    return { isFaulty: true, reason: 'Raw answer key dump' };
  }

  // 4. Broken stem (empty, too short without context, or meaningless fragment)
  if (stem.trim().length === 0 || ['Hangisi doğrudur?', 'Hangisi yanlıştır?', 'Terminal sinir'].includes(stem.trim())) {
    return { isFaulty: true, reason: 'Empty or truncated question stem' };
  }

  // 5. Mashed table dump in options (a single option > 650 chars indicates unparsed table dump)
  if (options.some(o => (o.text || '').length > 650)) {
    return { isFaulty: true, reason: 'Mashed table dump in options (>650 chars)' };
  }

  // 6. Repeated table headers in stem
  const siraNoCount = (stem.match(/Sıra No/gi) || []).length;
  if (siraNoCount >= 3) {
    return { isFaulty: true, reason: 'Repeated table headers in stem' };
  }

  // 7. Garbled OCR gibberish strings
  if (/\b(?:SzRARM|mpsziz|pfBğösr|vndgu7|krv9|xkp\w+|pBğösr|EBEs\$|Egağ|Söse|Saz ör)\b/i.test(fullText)) {
    return { isFaulty: true, reason: 'Garbled OCR gibberish' };
  }

  // 8. Null bytes or severe encoding artifacts
  if (stem.includes('\u0000') || (stem.match(/[\uFFFD]/g) || []).length > 2) {
    return { isFaulty: true, reason: 'Null bytes / severe character encoding corruption' };
  }

  // 9. Severe broken font artifact: excessive exclamation marks inside words (> 10 occurrences)
  const exclCount = (stem.match(/!/g) || []).length;
  if (exclCount > 10) {
    return { isFaulty: true, reason: `Unreadable font replacement (${exclCount} exclamation marks)` };
  }

  // 10. Chained questions in single stem with answer leak
  if (stem.includes('Cevap=') && stem.includes('Hang!s!') || stem.includes('--> Der!')) {
    return { isFaulty: true, reason: 'Concatenated multi-question leak in stem' };
  }

  return { isFaulty: false };
}

export function checkDonem3Eligibility(q) {
  const isTum = (q.sourceFile || '').includes('tüm sorular') || (q.sourceFile || '').includes('tum sorular');
  const stem = (q.rawQuestion && q.rawQuestion.stem) || '';
  const options = (q.rawQuestion && q.rawQuestion.options) || [];
  const fullText = (stem + ' ' + options.map(o => o.text || '').join(' ')).trim().toLowerCase();

  if (isTum) {
    // For tüm sorular: keep ONLY genuine Pathology / Dönem 3 clinical content
    const isPathology = pathologyKeywords.some(kw => fullText.includes(kw));
    const isDonem2 = donem2ExclusionKeywords.some(kw => fullText.includes(kw));

    if (isPathology && !isDonem2) {
      return { isEligible: true, isFromTum: true };
    } else {
      return { isEligible: false, reason: 'Dönem 2 Anatomy/Physiology/Histology/Biophysics' };
    }
  } else {
    // For other files: exclude if strictly matches Dönem 2 exclusion without any Dönem 3 clinical relevance
    const isStrictDonem2 = donem2ExclusionKeywords.some(kw => fullText.includes(kw)) &&
                           !pathologyKeywords.some(kw => fullText.includes(kw));
    if (isStrictDonem2) {
      return { isEligible: false, reason: 'Dönem 2 content in exam file' };
    }
    return { isEligible: true, isFromTum: false };
  }
}

// Dry run execution
let faultyOcr = 0;
let donem2Excluded = 0;
let preservedTum = 0;
let preservedOther = 0;

const finalKept = [];
const finalExcluded = [];

pq.forEach(q => {
  const ocrCheck = checkFaultyOcr(q);
  if (ocrCheck.isFaulty) {
    faultyOcr++;
    finalExcluded.push({ id: q.id, source: q.sourceFile, reason: ocrCheck.reason, stem: q.rawQuestion.stem });
    return;
  }

  const d3Check = checkDonem3Eligibility(q);
  if (!d3Check.isEligible) {
    donem2Excluded++;
    finalExcluded.push({ id: q.id, source: q.sourceFile, reason: d3Check.reason, stem: q.rawQuestion.stem });
    return;
  }

  if (d3Check.isFromTum) {
    preservedTum++;
    q.discipline = 'Tıbbi Patoloji';
  } else {
    preservedOther++;
  }
  finalKept.push(q);
});

console.log('=== DRY RUN SUMMARY ===');
console.log(`Original total questions: ${pq.length}`);
console.log(`Faulty OCR / Corrupted eliminated: ${faultyOcr}`);
console.log(`Dönem 2 (Non-Dönem 3) eliminated: ${donem2Excluded}`);
console.log(`Total preserved for Dönem 3: ${finalKept.length}`);
console.log(`  - Preserved from tüm sorular (Patoloji): ${preservedTum}`);
console.log(`  - Preserved from other exam files: ${preservedOther}`);
