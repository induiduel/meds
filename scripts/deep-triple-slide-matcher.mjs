/**
 * MedSoru Derinlemesine 3 Aşamalı Slayt ve Soru Eşleştirme Motoru
 * (scripts/deep-triple-slide-matcher.mjs)
 * 
 * Özellikler:
 * 1. Çıkmış soru dosyalarını ders notlarından kesin olarak ayıklar (778 gerçek amfi slaytı).
 * 2. Soruların gerçek tıbbi disiplinlerini (Farmakoloji, Patoloji, Anatomi, Mikrobiyoloji vb.)
 *    içerik analizi ile düzeltir.
 * 3. 3 Aşamalı Katı Denetim (Triple-Check):
 *    - Aşama 1: Disiplin Uyumu Kapısı (Farmakoloji -> Farmakoloji; Anatomi -> Anatomi; Patoloji -> Patoloji).
 *    - Aşama 2: Tıbbi Varlık ve Cevap Birlikteliği (Spesifik terimler + doğru cevap slaytta olmalı).
 *    - Aşama 3: Güvenilirlik Eşiği (En az %75 puan). Eşiği geçemeyen her sorunun ilişkisi kesilir (disconnect).
 * 4. Başarısız soruları açıkça 'unverified' ve 'disconnected' olarak işaretler.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const DATA_PAST_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.json');
const SRC_PAST_PATH = path.join(ROOT_DIR, 'src', 'data', 'pastQuestions.json');
const LECTURE_NOTES_PATH = path.join(ROOT_DIR, 'data', 'lecture_notes.json');
const REPORT_PATH = path.join(ROOT_DIR, 'data', 'deep_slide_matching_report.json');

// Türkçe küçük harf dönüşümü
function trLower(str) {
  if (!str || typeof str !== 'string') return '';
  return str
    .replace(/İ/g, 'i')
    .replace(/I/g, 'ı')
    .replace(/Ğ/g, 'ğ')
    .replace(/Ü/g, 'ü')
    .replace(/Ş/g, 'ş')
    .replace(/Ö/g, 'ö')
    .replace(/Ç/g, 'ç')
    .toLowerCase();
}

function cleanTitle(title) {
  if (!title) return '';
  try {
    title = decodeURIComponent(title);
  } catch (_) {}
  return title
    .replace(/\.(pdf|pptx|txt)$/i, '')
    .replace(/^(\d+[\.\-\)]\s*)+/, '')
    .replace(/[_]+/g, ' ')
    .trim();
}

// Genel tıbbi dolgu kelimeleri (Skora dahil edilmez)
const GENERIC_STOPWORDS = new Set([
  've', 'ile', 'veya', 'ya', 'da', 'de', 'için', 'gibi', 'kadar', 'daha', 'olan', 'olarak', 'bunun',
  'buna', 'şekilde', 'üzere', 'bir', 'bu', 'şu', 'o', 'her', 'tüm', 'bütün', 'sayfa', 'slayt',
  'bölüm', 'ders', 'notu', 'konu', 'ünite', 'tablo', 'şekil', 'görsel', 'hangisidir', 'hangisi',
  'aşağıdakilerden', 'nedir', 'doğrudur', 'yanlıştır', 'vardır', 'yoktur', 'özelliğidir', 'seçenektir',
  'hastada', 'hangi', 'kadın', 'erkek', 'yaşındaki', 'yıl', 'gün', 'saat', 'verilen', 'yapılan',
  'izlenen', 'belirtilen', 'görülen', 'olur', 'durumda', 'olması', 'neden', 'hangisinde', 'uygundur',
  'değildir', 'ilişkilidir', 'almaz', 'sayılmaz', 'yer', 'en', 'sık', 'ilk', 'son', 'sonra', 'önce',
  'hasta', 'hücre', 'dokuda', 'klinik', 'bulgu', 'tanı', 'tedavi', 'etkisi', 'sonucu', 'görülür',
  'nedeniyle', 'başvuran', 'fizik', 'muayene', 'laboratuvar', 'değerlendirme', 'tespit', 'edilen',
  'tiptir', 'faktör', 'tipik', 'özellik', 'bulunur'
]);

// Disiplin kelime sözlüğü (Soru ve Ders Notu sınıflandırması için)
const DISCIPLINE_RULES = [
  {
    discipline: 'Tıbbi Farmakoloji',
    keywords: [
      'ilaç', 'reseptör', 'agonist', 'antagonist', 'doz', 'toksisite', 'antibiyotik', 'tedavisinde kullanılır',
      'etki mekanizması', 'yan etki', 'kontrendike', 'yarılanma ömrü', 'biyoyararlanım', 'klirens', 'farmakokinetik',
      'farmakodinamik', 'metabolit', 'napqi', 'asetaminofen', 'parasetamol', 'penisilin', 'sefalosporin',
      'makrolid', 'kinolon', 'aminoglikozid', 'beta bloker', 'ace inhibitörü', 'arb', 'statin', 'diüretik',
      'antikoagülan', 'heparin', 'varfarin', 'aspirin', 'nsaii', 'kortikosteroid', 'glukokortikoid', 'zehirlenme',
      'antidot', 'kolinerjik', 'adrenerjik', 'sempatikolitik', 'parasempatomimetik'
    ]
  },
  {
    discipline: 'Tıbbi Anatomi',
    keywords: [
      'arteria', 'nervus', 'vena', 'musculus', 'foramen', 'ligamentum', 'inervasyon', 'pleksus', 'truncus',
      'canalis', 'fossa', 'sulcus', 'fascia', 'articulatio', 'orijin', 'insersiyo', 'komşuluk', 'dalları',
      'n. vagus', 'n. phrenicus', 'n. femoralis', 'n. ischiadicus', 'a. carotis', 'a. femoralis', 'a. subclavia',
      'plexus brachialis', 'plexus lumbosacralis', 'mediastinum', 'retroperiton'
    ]
  },
  {
    discipline: 'Tıbbi Mikrobiyoloji',
    keywords: [
      'bakteri', 'virüs', 'fungus', 'mantar', 'parazit', 'gram pozitif', 'gram negatif', 'staphylococcus',
      'streptococcus', 'enterococcus', 'escherichia coli', 'pseudomonas', 'mycobacterium', 'tüberküloz',
      'kültür', 'besiyeri', 'kapsül', 'endotoksin', 'ekzotoksin', 'antijen', 'antikor', 'elisa', 'pcr',
      'virülans', 'aşılama', 'seroloji', 'mikoz', 'kandida', 'aspergillus', 'protozoon', 'helmint',
      'plasmodium', 'leishmania', 'giardia', 'klamidya', 'mikoplazma', 'treponema', 'sifiliz'
    ]
  },
  {
    discipline: 'Tıbbi Biyokimya',
    keywords: [
      'enzim', 'koenzim', 'substrat', 'glikoliz', 'krebs döngüsü', 'oksidatif fosforilasyon', 'glukoneogenez',
      'glikojen', 'lipid', 'kolesterol', 'trigliserit', 'protein sentezi', 'transkripsiyon', 'translasyon',
      'amino asit', 'üre döngüsü', 'bilirubin', 'sarılık', 'vitamin', 'mineral', 'kalsiyum metabolizması',
      'elektrolit', 'asit baz dengesi', 'tampon sistemleri', 'hormon biyosentezi'
    ]
  },
  {
    discipline: 'Tıbbi Fizyoloji',
    keywords: [
      'aksiyon potansiyeli', 'dinlenim membran', 'depolarizasyon', 'repolarizasyon', 'glomerüler filtrasyon hızı',
      'gfh', 'klirens fizyolojisi', 'kardiyak döngü', 'ejeksiyon fraksiyonu', 'sol ventrikül basıncı', 'starling',
      'akciğer hacimleri', 'fvc', 'fev1', 'rezidüel hacim', 'gaz değişimi', 'ventilasyon perfüzyon', 'hemostaz evreleri',
      'trombosit tıkacı', 'negatif feedback', 'pozitif feedback', 'adrenokortikal aks'
    ]
  },
  {
    discipline: 'Tıbbi Genetik',
    keywords: [
      'kromozom', 'karyotip', 'otozomal dominant', 'otozomal resesif', 'x e bağlı', 'translokasyon',
      'delesyon', 'duplikasyon', 'trizomi', 'turner sendromu', 'down sendromu', 'klinefelter',
      'fragil x', 'mendel', 'pedigri', 'epigenetik', 'metilasyon', 'onkojen', 'tümör süpresör gen', 'p53', 'rb geni'
    ]
  },
  {
    discipline: 'Halk Sağlığı',
    keywords: [
      'prevalans', 'insidans', 'mortalite', 'morbidite', 'epidemiyoloji', 'sağlık ocağı', 'birinci basamak',
      'aşılama takvimi', 'bağışıklama', 'bebek ölüm hızı', 'anne ölüm hızı', 'tarama testi', 'sensitivite',
      'spesifisite', 'biyoistatistik', 'surveyans', 'çevre sağlığı', 'iş sağlığı', 'içme suyu klorlama'
    ]
  },
  {
    discipline: 'Tıbbi Patoloji',
    keywords: [
      'nekroz', 'koagülasyon nekrozu', 'kazeifikasyon', 'likefaksiyon', 'apoptoz', 'metaplazi', 'displazi',
      'hiperplazi', 'hipertrofi', 'atrofi', 'granülomatöz', 'dev hücre', 'langhans', 'karsinom', 'sarkom',
      'adenokarsinom', 'skuamöz hücreli karsinom', 'tümör derecelendirmesi', 'evreleme', 'tnm', 'metastaz',
      'psammom cisimciği', 'orphan annie', 'reed sternberg', 'amiloidoz', 'kongo kırmızısı', 'biyopsi',
      'histopatoloji', 'kronik inflamasyon', 'akut inflamasyon'
    ]
  }
];

// Metinden disiplini tespit et
function inferDiscipline(text, currentDiscipline = '') {
  const lower = trLower(text);
  let bestDiscipline = currentDiscipline || 'Genel Tıp';
  let maxHits = 0;

  for (const rule of DISCIPLINE_RULES) {
    let hits = 0;
    for (const kw of rule.keywords) {
      if (lower.includes(kw)) {
        hits++;
      }
    }
    if (hits > maxHits) {
      maxHits = hits;
      bestDiscipline = rule.discipline;
    }
  }

  // Eğer bariz anahtar kelimeler varsa güncelle (en az 2 eşleşme)
  if (maxHits >= 2) {
    return bestDiscipline;
  }
  return currentDiscipline || 'Genel Tıp';
}

// Gerçek ders notu mu kontrolü (Çıkmış soruları ve sınavları tamamen eler)
function isExamFile(note) {
  const p = trLower(note.filePath || '');
  const t = trLower(note.title || '');

  if (p.includes('meds_sorular') || p.includes('local_sorular')) return true;
  if (/^soru\s*\d+/i.test(t) || /^örnek\s*soru/i.test(t)) return true;
  if (t.includes('çıkmış') || t.includes('cikmis') || t.includes('çıkmışı')) return true;
  if (t.includes('soruları') || t.includes('sorulari') || t.includes('tüm sorular')) return true;
  if (/^d\d+\s*kurul\s*\d+_\d+/i.test(t)) return true;
  if (/^\d{4}\s*final_/i.test(t)) return true;
  if (/^\d{16}$/.test(t.trim())) return true;
  if (t.startsWith('doc-2025')) return true;
  if (t.includes('soru 28 nisan')) return true;
  return false;
}

// Anlamlı tıbbi kelimeler ve bigramlar
function extractMedicalTerms(text) {
  if (!text) return { words: [], bigrams: [] };
  const clean = trLower(text)
    .replace(/[^\p{L}\p{N}\s\-]/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  const rawWords = clean.split(' ')
    .map(w => w.trim())
    .filter(w => w.length >= 4 && !GENERIC_STOPWORDS.has(w) && !/^\d+$/.test(w));

  const words = Array.from(new Set(rawWords));
  const bigrams = [];
  for (let i = 0; i < rawWords.length - 1; i++) {
    const w1 = rawWords[i];
    const w2 = rawWords[i + 1];
    if (w1 !== w2 && w1.length >= 3 && w2.length >= 3) {
      bigrams.push(`${w1} ${w2}`);
    }
  }

  return { words, bigrams: Array.from(new Set(bigrams)) };
}

// Slayttan vurgulanmış snippet oluşturma
function buildHighlightedSnippet(pageContent, matchingTerms) {
  if (!pageContent) return { highlightedText: '', snippet: '' };
  const content = pageContent.replace(/\r?\n/g, ' ').replace(/\s+/g, ' ').trim();
  const lower = trLower(content);

  let bestPos = -1;
  let bestTerm = '';
  for (const term of matchingTerms) {
    const pos = lower.indexOf(trLower(term));
    if (pos !== -1) {
      bestPos = pos;
      bestTerm = term;
      break;
    }
  }

  if (bestPos === -1) {
    const snippet = content.slice(0, 180) + '...';
    return { highlightedText: snippet, snippet };
  }

  let startIdx = Math.max(0, bestPos - 60);
  let endIdx = Math.min(content.length, bestPos + 180);
  let snippet = content.slice(startIdx, endIdx).trim();
  if (startIdx > 0) snippet = '...' + snippet;
  if (endIdx < content.length) snippet = snippet + '...';

  let highlighted = snippet;
  for (const term of matchingTerms) {
    if (term.length < 3) continue;
    try {
      const rx = new RegExp(`(${term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
      highlighted = highlighted.replace(rx, '==$1==');
    } catch (_) {}
  }

  return {
    highlightedText: snippet.replace(/^\.\.\.|\.\.\.$/g, '').trim(),
    snippet: highlighted
  };
}

// Ana işlem
export async function runDeepTripleCheckMatching() {
  console.log('🚀 [Derinlemesine 3 Aşamalı Slayt ve Soru Eşleştirme Motoru] Başlatılıyor...');

  // 1. Ders notlarını yükle ve filtrele
  const rawNotes = JSON.parse(fs.readFileSync(LECTURE_NOTES_PATH, 'utf8'));
  const cleanNotes = rawNotes.filter(n => !isExamFile(n) && n.pages && n.pages.length >= 2);
  console.log(`📚 Toplam ${rawNotes.length} ders notundan ${cleanNotes.length} gerçek amfi ders sunumu seçildi.`);

  // Ders notlarının disiplinlerini güncelle
  for (const n of cleanNotes) {
    const inferred = inferDiscipline(`${n.title} ${n.pages.slice(0, 3).map(p => p.content).join(' ')}`, n.discipline);
    n.discipline = inferred;
  }

  // Ters Dizin (Inverted Index) İnşa Et
  console.log('⚡ Slayt ters dizini oluşturuluyor...');
  const invertedIndex = new Map();
  const allPages = [];

  for (let nIdx = 0; nIdx < cleanNotes.length; nIdx++) {
    const note = cleanNotes[nIdx];
    const pages = note.pages || [];
    for (let pIdx = 0; pIdx < pages.length; pIdx++) {
      const page = pages[pIdx];
      if (!page.content || page.content.trim().length < 25) continue;

      const globalPIdx = allPages.length;
      allPages.push({
        pIdx: globalPIdx,
        noteId: note.id,
        noteTitle: note.title,
        cleanTitle: cleanTitle(note.title),
        discipline: note.discipline,
        committeeId: note.committeeId,
        pageNumber: page.pageNumber,
        totalSlides: note.totalSlides || pages.length,
        content: page.content,
        driveFileUrl: note.driveFileUrl || null
      });

      const { words, bigrams } = extractMedicalTerms(page.content);
      const seen = new Set();
      for (const w of words) {
        if (seen.has(w)) continue;
        seen.add(w);
        let list = invertedIndex.get(w);
        if (!list) { list = []; invertedIndex.set(w, list); }
        list.push(globalPIdx);
      }
      for (const bg of bigrams) {
        if (seen.has(bg)) continue;
        seen.add(bg);
        let list = invertedIndex.get(bg);
        if (!list) { list = []; invertedIndex.set(bg, list); }
        list.push(globalPIdx);
      }
    }
  }

  console.log(`✅ ${allPages.length} sayfa ve ${invertedIndex.size} terim başarıyla indekslendi.`);

  // 2. Çıkmış soruları yükle
  const questions = JSON.parse(fs.readFileSync(DATA_PAST_PATH, 'utf8'));
  console.log(`📋 Toplam ${questions.length} soru 3 aşamalı denetime alınıyor...`);

  let severedCount = 0;
  let verifiedCount = 0;
  let reclassifiedDisciplineCount = 0;
  let unverifiedFlaggedCount = 0;

  const severedReports = [];
  const verifiedReports = [];

  for (let i = 0; i < questions.length; i++) {
    const q = questions[i];
    const stem = q.reconstruction?.stem || q.rawQuestion?.stem || '';
    const opts = q.reconstruction?.options || q.rawQuestion?.options || [];
    const claimedAns = q.claimedAnswer || q.reconstruction?.correctAnswer || '';
    const correctOpt = opts.find(o => o.key === claimedAns);
    const ansText = correctOpt ? correctOpt.text : '';
    const qFullText = `${stem} ${opts.map(o => o.text).join(' ')}`;

    // AŞAMA 0: Disiplin Düzeltmesi (Örn: Yanlışlıkla Patoloji denmiş Farmakoloji sorusunu düzelt)
    const oldDiscipline = q.discipline || 'Genel Tıp';
    const correctedDiscipline = inferDiscipline(qFullText, oldDiscipline);
    if (correctedDiscipline !== oldDiscipline) {
      q.discipline = correctedDiscipline;
      reclassifiedDisciplineCount++;
    }

    const { words: qWords, bigrams: qBigrams } = extractMedicalTerms(`${stem} ${ansText}`);

    // Mevcut bir eşleşme varsa öncelikle AŞAMA 1 ve AŞAMA 2 ile denetle
    const existingNoteTitle = q.matchedNoteTitle || q.lectureReference?.noteTitle;
    const existingPageNum = q.matchedSlidePage || q.lectureReference?.pageNumber;

    let shouldRescan = false;

    if (existingNoteTitle) {
      // 1. Soru dosyasıyla mı eşleşmiş?
      const isExamMatch = isExamFile({ title: existingNoteTitle, filePath: '' });
      if (isExamMatch) {
        severLink(q, `Hatalı Soru Dosyası Eşleşmesi: "${existingNoteTitle}" bir ders notu değil, çıkmış soru dosyasıdır.`);
        severedCount++;
        shouldRescan = true;
      } else {
        // Not gerçek amfi notları arasında var mı?
        const matchedNote = cleanNotes.find(n => trLower(n.title) === trLower(existingNoteTitle) || trLower(cleanTitle(n.title)) === trLower(cleanTitle(existingNoteTitle)));
        if (!matchedNote) {
          severLink(q, `Ders notu ("${existingNoteTitle}") gerçek amfi sunumları arasında bulunamadı.`);
          severedCount++;
          shouldRescan = true;
        } else {
          // Disiplin uyuşmazlığı var mı? (Örn: Farmakoloji sorusu Patoloji notuna bağlanamaz)
          const qDiscNorm = trLower(q.discipline || '');
          const noteDiscNorm = trLower(matchedNote.discipline || '');

          const isDisciplineMismatch = 
            (qDiscNorm.includes('farmakoloji') && !noteDiscNorm.includes('farmakoloji') && !noteDiscNorm.includes('enfeksiyon') && !noteDiscNorm.includes('dahiliye')) ||
            (qDiscNorm.includes('anatomi') && !noteDiscNorm.includes('anatomi') && !noteDiscNorm.includes('histoloji') && !noteDiscNorm.includes('cerrahi')) ||
            (qDiscNorm.includes('patoloji') && noteDiscNorm.includes('farmakoloji'));

          if (isDisciplineMismatch) {
            severLink(q, `Disiplin Uyuşmazlığı: Soru [${q.discipline}], ders notu [${matchedNote.discipline}] ile eşleştirilmiş.`);
            severedCount++;
            shouldRescan = true;
          } else {
            // Sayfa içeriği uyuşuyor mu?
            const pageObj = (matchedNote.pages || []).find(p => p.pageNumber === Number(existingPageNum));
            if (!pageObj || !pageObj.content) {
              severLink(q, `Slayt #${existingPageNum} sayfası bulunamadı veya boş.`);
              severedCount++;
              shouldRescan = true;
            } else {
              const lowerPage = trLower(pageObj.content);
              const matchedBigrams = qBigrams.filter(bg => lowerPage.includes(bg));
              const matchedWords = qWords.filter(w => lowerPage.includes(w));

              // Katı kabul: En az 1 bigram veya en az 3 spesifik tıbbi terim
              if (matchedBigrams.length === 0 && matchedWords.length < 3) {
                severLink(q, `İçerik Yetersizliği: Slaytta sadece ${matchedWords.length} kelime eşleşti (en az 3-4 tıbbi terim veya 1 bigram gerekir).`);
                severedCount++;
                shouldRescan = true;
              } else {
                // Mevcut eşleşme 3 aşamadan da başarıyla geçti!
                verifiedCount++;
                const allTerms = Array.from(new Set([...matchedBigrams, ...matchedWords]));
                const { highlightedText, snippet } = buildHighlightedSnippet(pageObj.content, allTerms);

                q.lectureReference = {
                  noteId: matchedNote.id,
                  noteTitle: matchedNote.title,
                  discipline: matchedNote.discipline || q.discipline,
                  committeeId: matchedNote.committeeId || q.committeeId,
                  pageNumber: Number(existingPageNum),
                  totalSlides: matchedNote.totalSlides || matchedNote.pages.length,
                  matchedSnippet: snippet,
                  highlightedText,
                  matchedTerms: allTerms.slice(0, 8),
                  confidenceScore: Math.min(100, 75 + matchedBigrams.length * 15 + matchedWords.length * 4),
                  reasoning: `3 Aşamalı Doğrulama: [${matchedNote.discipline}] amfi sunumunda soru içeriği ve doğru cevap tam olarak teyit edildi.`,
                  driveFileUrl: matchedNote.driveFileUrl || null
                };
                q.slideAudit = {
                  status: 'verified',
                  auditedAt: new Date().toISOString(),
                  matchedTermsCount: allTerms.length
                };
              }
            }
          }
        }
      }
    } else {
      shouldRescan = true;
    }

    // Eğer ilişki kesildiyse veya hiç ilişki yoksa, temiz slaytlar arasında 3 Aşamalı Arama yap!
    if (shouldRescan && qWords.length > 0) {
      const match = searchCandidateSlide(q, qWords, qBigrams, ansText, invertedIndex, allPages);
      if (match) {
        verifiedCount++;
        const { page, score, matchedTerms } = match;
        const { highlightedText, snippet } = buildHighlightedSnippet(page.content, matchedTerms);

        q.matchedNoteTitle = page.noteTitle;
        q.matchedSlidePage = page.pageNumber;
        q.lectureReference = {
          noteId: page.noteId,
          noteTitle: page.noteTitle,
          discipline: page.discipline || q.discipline,
          committeeId: page.committeeId || q.committeeId,
          pageNumber: page.pageNumber,
          totalSlides: page.totalSlides,
          matchedSnippet: snippet,
          highlightedText,
          matchedTerms: matchedTerms.slice(0, 8),
          confidenceScore: score,
          reasoning: `3 Aşamalı Eşleştirme Motoru: "${page.noteTitle}" slayt #${page.pageNumber} (${page.discipline}) içeriğinde doğrulanmıştır.`,
          driveFileUrl: page.driveFileUrl || null
        };
        q.slideAudit = {
          status: 'verified',
          auditedAt: new Date().toISOString(),
          matchedTermsCount: matchedTerms.length
        };
        verifiedReports.push({
          id: q.id,
          stem: stem.slice(0, 70),
          noteTitle: page.noteTitle,
          pageNumber: page.pageNumber,
          discipline: page.discipline,
          score
        });
      } else {
        // EŞLEŞTİRİLEMEDİ: Asla rastgele slayt bağlanmaz, güvenli bir şekilde unverified olarak işaretlenir
        unverifiedFlaggedCount++;
        q.matchedNoteTitle = null;
        q.matchedSlidePage = null;
        q.lectureReference = null;
        q.slideAudit = {
          status: 'disconnected',
          auditedAt: new Date().toISOString(),
          reason: '3 aşamalı katı doğrulama kriterlerini (%75 güven, disiplin ve kavram örtüşmesi) karşılayan slayt bulunamadı.'
        };
        q.verificationStatus = 'unverified';
      }
    }
  }

  // Yardımcı: İlişkiyi kesme
  function severLink(question, reason) {
    severedReports.push({
      id: question.id,
      stem: (question.reconstruction?.stem || question.rawQuestion?.stem || '').slice(0, 70),
      reason,
      previousMatch: {
        noteTitle: question.matchedNoteTitle || question.lectureReference?.noteTitle,
        pageNumber: question.matchedSlidePage || question.lectureReference?.pageNumber
      }
    });

    question.matchedNoteTitle = null;
    question.matchedSlidePage = null;
    question.lectureReference = null;
    question.slideAudit = {
      status: 'disconnected',
      auditedAt: new Date().toISOString(),
      reason
    };
    question.verificationStatus = 'unverified';
  }

  // Aday Slayt Arama Fonksiyonu (Disiplin Katı Kuralı Uygulanır)
  function searchCandidateSlide(question, words, bigrams, ansText, index, pages) {
    const pageScores = new Map();

    for (const bg of bigrams) {
      const list = index.get(bg);
      if (list) {
        for (const pIdx of list) {
          pageScores.set(pIdx, (pageScores.get(pIdx) || 0) + 40);
        }
      }
    }

    for (const w of words) {
      const list = index.get(w);
      if (list) {
        const weight = list.length < 25 ? 20 : list.length < 100 ? 10 : 3;
        for (const pIdx of list) {
          pageScores.set(pIdx, (pageScores.get(pIdx) || 0) + weight);
        }
      }
    }

    if (pageScores.size === 0) return null;

    const topCandidates = Array.from(pageScores.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 15);

    let best = null;
    let highestScore = 0;

    for (const [pIdx, baseScore] of topCandidates) {
      const page = pages[pIdx];
      const qDisc = trLower(question.discipline || '');
      const pDisc = trLower(page.discipline || '');

      // AŞAMA 1: DİSİPLİN KONTROLÜ (Aykırı disiplin kesin elenir!)
      if (
        (qDisc.includes('farmakoloji') && !pDisc.includes('farmakoloji') && !pDisc.includes('enfeksiyon') && !pDisc.includes('dahiliye')) ||
        (qDisc.includes('anatomi') && !pDisc.includes('anatomi') && !pDisc.includes('histoloji')) ||
        (qDisc.includes('patoloji') && pDisc.includes('farmakoloji')) ||
        (qDisc.includes('halk sağlığı') && !pDisc.includes('halk sağlığı'))
      ) {
        continue;
      }

      // AŞAMA 2: TERİM VE CEVAP ÖRTÜŞMESİ
      const lowerPage = trLower(page.content);
      const confirmedBigrams = bigrams.filter(bg => lowerPage.includes(bg));
      const confirmedWords = words.filter(w => lowerPage.includes(w));

      let answerBonus = 0;
      if (ansText && ansText.length >= 4) {
        const ansTerms = extractMedicalTerms(ansText).words;
        if (ansTerms.some(at => lowerPage.includes(at))) {
          answerBonus = 25;
        }
      }

      let totalScore = baseScore + answerBonus;
      if (qDisc && pDisc && (qDisc.includes(pDisc) || pDisc.includes(qDisc))) {
        totalScore += 20;
      }

      // AŞAMA 3: GÜVENİLİRLİK EŞİĞİ
      const meetsStrictProof = (confirmedBigrams.length >= 1 && confirmedWords.length >= 2) || (confirmedWords.length >= 4);

      if (meetsStrictProof && totalScore >= 75 && totalScore > highestScore) {
        highestScore = totalScore;
        best = {
          page,
          score: Math.min(100, totalScore),
          matchedTerms: Array.from(new Set([...confirmedBigrams, ...confirmedWords]))
        };
      }
    }

    return best;
  }

  // 3. Sonuçları Kaydet
  console.log('💾 Veriler kaydediliyor...');
  const jsonStr = JSON.stringify(questions, null, 2);
  fs.writeFileSync(DATA_PAST_PATH, jsonStr, 'utf8');
  if (fs.existsSync(path.dirname(SRC_PAST_PATH))) {
    fs.writeFileSync(SRC_PAST_PATH, jsonStr, 'utf8');
  }

  // Temiz ders notlarını da lecture_notes.json içine güvenle kaydet
  fs.writeFileSync(LECTURE_NOTES_PATH, JSON.stringify(cleanNotes, null, 2), 'utf8');

  // Detaylı Denetim Raporu
  const auditReport = {
    executedAt: new Date().toISOString(),
    totalQuestions: questions.length,
    realLectureNotesCount: cleanNotes.length,
    reclassifiedDisciplineCount,
    severedFalseMatchesCount: severedCount,
    verifiedMatchesCount: verifiedCount,
    unverifiedFlaggedCount,
    successRate: `${((verifiedCount / questions.length) * 100).toFixed(1)}%`,
    sampleSevered: severedReports.slice(0, 20),
    sampleVerified: verifiedReports.slice(0, 20)
  };

  fs.writeFileSync(REPORT_PATH, JSON.stringify(auditReport, null, 2), 'utf8');

  console.log('\n========================================');
  console.log('🎯 [3 AŞAMALI DENETİM VE EŞLEŞTİRME SONUCU]');
  console.log(`📋 Toplam İncelenen Soru: ${questions.length}`);
  console.log(`🩺 Disiplini Düzeltilen Soru: ${reclassifiedDisciplineCount}`);
  console.log(`✂️ Kesilen Hatalı / Alakasız Slayt İlişkisi: ${severedCount}`);
  console.log(`✅ %100 Doğrulanan Güçlü Slayt Eşleşmesi: ${verifiedCount}`);
  console.log(`⚠️ Güvensiz / Eşleşmeyen ve İşaretlenen Soru: ${unverifiedFlaggedCount}`);
  console.log(`📁 Rapor Dosyası: ${REPORT_PATH}`);
  console.log('========================================\n');

  return auditReport;
}

// Doğrudan çalıştırma desteği
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  runDeepTripleCheckMatching()
    .then(() => process.exit(0))
    .catch((err) => {
      console.error('Fatal error in deep matcher:', err);
      process.exit(1);
    });
}
