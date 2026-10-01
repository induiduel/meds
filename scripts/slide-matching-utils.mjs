/**
 * MedSoru Slayt Eşleştirme ve Denetim Yardımcı Modülü
 * (scripts/slide-matching-utils.mjs)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
export const ROOT_DIR = path.resolve(__dirname, '..');
export const DATA_PAST_PATH = path.join(ROOT_DIR, 'data', 'pastQuestions.json');
export const SRC_PAST_PATH = path.join(ROOT_DIR, 'src', 'data', 'pastQuestions.json');
export const LECTURE_NOTES_PATH = path.join(ROOT_DIR, 'data', 'lecture_notes.json');

// Türkçe karakter duyarlı küçük harfe dönüştürme ve sadeleştirme
export function turkishToLower(str) {
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

// URL encode çözme ve temizleme (örn: %20 -> boşluk)
export function cleanTitle(title) {
  if (!title) return '';
  try {
    title = decodeURIComponent(title);
  } catch (_) {}
  return title
    .replace(/\.(pdf|pptx|txt)$/i, '')
    .replace(/^(\d+[\.\-\)]\s*)+/, '') // Baştaki "1) ", "22. " gibi sıralamaları at
    .replace(/[_]+/g, ' ')
    .trim();
}

// Genel Türkçe ve Sınav Dolgu Kelimeleri (Tıbbi değer taşımayan)
export const STOPWORDS = new Set([
  've', 'ile', 'veya', 'ya', 'da', 'de', 'için', 'gibi', 'kadar', 'daha', 'olan', 'olarak', 'bunun',
  'buna', 'şekilde', 'üzere', 'bir', 'bu', 'şu', 'o', 'her', 'tüm', 'bütün', 'sayfa', 'slayt',
  'bölüm', 'ders', 'notu', 'konu', 'ünite', 'tablo', 'şekil', 'görsel', 'hangisidir', 'hangisi',
  'aşağıdakilerden', 'nedir', 'doğrudur', 'yanlıştır', 'vardır', 'yoktur', 'özelliğidir', 'seçenektir',
  'hastada', 'hangi', 'kadın', 'erkek', 'yaşındaki', 'yıl', 'gün', 'saat', 'verilen', 'yapılan',
  'izlenen', 'belirtilen', 'görülen', 'olur', 'durumda', 'olması', 'neden', 'hangisinde', 'uygundur',
  'değildir', 'ilişkilidir', 'almaz', 'sayılmaz', 'yer', 'en', 'sık', 'ilk', 'son', 'sonra', 'önce',
  'the', 'and', 'for', 'with', 'from', 'that', 'this', 'are', 'was'
]);

// Tıbbi disiplin normalizasyonu
export function normalizeDiscipline(rawDiscipline, committeeId = '') {
  if (!rawDiscipline) return 'Tıp Ders Notu';
  const lower = rawDiscipline.toLowerCase();
  if (lower.includes('patoloji')) return 'Tıbbi Patoloji';
  if (lower.includes('farmakoloji') || lower.includes('ilaç')) return 'Tıbbi Farmakoloji';
  if (lower.includes('mikrobiyoloji') || lower.includes('bakteri') || lower.includes('viroloji') || lower.includes('parazit')) return 'Tıbbi Mikrobiyoloji';
  if (lower.includes('genetik')) return 'Tıbbi Genetik';
  if (lower.includes('halk sağlığı') || lower.includes('epidemiyoloji')) return 'Halk Sağlığı';
  if (lower.includes('dahiliye') || lower.includes('iç hastalıkları')) return 'İç Hastalıkları';
  if (lower.includes('biyokimya')) return 'Tıbbi Biyokimya';
  if (lower.includes('fizyoloji')) return 'Tıbbi Fizyoloji';
  if (lower.includes('anatomi') || lower.includes('histoloji')) return 'Tıbbi Anatomi / Histoloji';
  if (lower.includes('kardiyo')) return 'Kardiyoloji';
  if (lower.includes('pediatri') || lower.includes('çocuk')) return 'Çocuk Sağlığı';
  return rawDiscipline.trim();
}

/**
 * Gerçek amfi ders notlarını yükler (çıkmış soru dosyalarını eler)
 */
export function loadRealLectureNotes() {
  if (!fs.existsSync(LECTURE_NOTES_PATH)) {
    throw new Error(`lecture_notes.json bulunamadı: ${LECTURE_NOTES_PATH}`);
  }
  const raw = fs.readFileSync(LECTURE_NOTES_PATH, 'utf8');
  const allNotes = JSON.parse(raw);

  // Sadece gerçek amfi ders sunumlarını filtrele (meds_sorular, local_sorular elenir)
  const realNotes = allNotes.filter(n => {
    const p = (n.filePath || '').toLowerCase();
    const t = (n.title || '').toLowerCase();
    const isExamFile = 
      p.includes('meds_sorular') || 
      p.includes('local_sorular') || 
      t.includes('çıkmış') || 
      t.includes('cikmis') || 
      t.includes('bütünleme') ||
      t.includes('butunleme') ||
      t.includes('sorular') ||
      t.includes('komite soruları');
    return !isExamFile && n.pages && n.pages.length > 0;
  });

  return realNotes;
}

/**
 * Ders notları başlık ve id haritası oluşturur (doğrulama için)
 */
export function buildNoteLookup(realNotes) {
  const byId = new Map();
  const byCleanTitle = new Map();
  const byOriginalTitle = new Map();

  for (const note of realNotes) {
    if (note.id) byId.set(note.id, note);
    const origTitle = turkishToLower(note.title.trim());
    byOriginalTitle.set(origTitle, note);

    const cTitle = turkishToLower(cleanTitle(note.title));
    if (cTitle) byCleanTitle.set(cTitle, note);
  }

  return {
    byId,
    byCleanTitle,
    byOriginalTitle,
    findNote(titleOrId) {
      if (!titleOrId) return null;
      const str = String(titleOrId).trim();
      if (byId.has(str)) return byId.get(str);
      const lower = turkishToLower(str);
      if (byOriginalTitle.has(lower)) return byOriginalTitle.get(lower);
      const cleaned = turkishToLower(cleanTitle(str));
      if (byCleanTitle.has(cleaned)) return byCleanTitle.get(cleaned);

      // Kısmi eşleşme (örneğin ders başlığının başlangıcı)
      for (const [key, note] of byCleanTitle.entries()) {
        if (key.length >= 6 && (cleaned.includes(key) || key.includes(cleaned))) {
          return note;
        }
      }
      return null;
    }
  };
}

/**
 * Metinden anlamlı tıbbi anahtar kelimeleri ve 2'li kelime gruplarını (bigram) çıkarır
 */
export function extractSalientTerms(text) {
  if (!text || typeof text !== 'string') return { words: [], bigrams: [] };

  const clean = turkishToLower(text)
    .replace(/[^\p{L}\p{N}\s\-]/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  const rawWords = clean.split(' ')
    .map(w => w.trim())
    .filter(w => w.length >= 4 && !STOPWORDS.has(w) && !/^\d+$/.test(w));

  const words = Array.from(new Set(rawWords));

  // Bigramlar (Örn: "papiller tiroid", "orphan annie", "ince igne", "kuru oksuruk")
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

/**
 * Slayt metninde ilişkili olan kısmı tespit eder ve vurgular (highlight)
 */
export function buildHighlightedSnippet(pageContent, matchingTerms) {
  if (!pageContent) return { highlightedText: '', snippet: '' };

  const content = pageContent.replace(/\r?\n/g, ' ').replace(/\s+/g, ' ').trim();
  const lowerContent = turkishToLower(content);

  // En çok eşleşen terimin geçtiği cümleyi veya bloğu bul
  let bestPos = -1;
  let bestMatchedTerm = '';

  for (const term of matchingTerms) {
    const termLower = turkishToLower(term);
    const pos = lowerContent.indexOf(termLower);
    if (pos !== -1) {
      bestPos = pos;
      bestMatchedTerm = term;
      break;
    }
  }

  if (bestPos === -1) {
    // Terim bulunamadıysa ilk 200 karakteri dön
    const snippet = content.slice(0, 200) + (content.length > 200 ? '...' : '');
    return { highlightedText: snippet, snippet };
  }

  // Cümle sınırlarını tespit et (. ! ? veya madde işaretleri • - ✓)
  const prevPunct = Math.max(
    content.lastIndexOf('.', bestPos),
    content.lastIndexOf('•', bestPos),
    content.lastIndexOf('✓', bestPos),
    content.lastIndexOf('-', bestPos),
    content.lastIndexOf(';', bestPos),
    0
  );
  
  let startIdx = prevPunct > 0 ? prevPunct + 1 : 0;
  if (bestPos - startIdx > 120) {
    startIdx = bestPos - 60;
  }

  const nextPunct = Math.min(
    ...['.', '•', '✓', '\n'].map(p => {
      const idx = content.indexOf(p, bestPos + bestMatchedTerm.length);
      return idx === -1 ? content.length : idx;
    })
  );

  let endIdx = Math.min(content.length, Math.max(nextPunct, bestPos + 180));

  let extractedSentence = content.slice(startIdx, endIdx).trim();
  if (startIdx > 0 && !extractedSentence.startsWith('...')) {
    extractedSentence = '...' + extractedSentence;
  }
  if (endIdx < content.length && !extractedSentence.endsWith('...')) {
    extractedSentence = extractedSentence + '...';
  }

  // İlgili terimleri ==...== ile vurgula
  let highlightedSnippet = extractedSentence;
  for (const term of matchingTerms) {
    if (term.length < 3) continue;
    // Regex ile büyük/küçük harf duyarsız değiştirme
    try {
      const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const rx = new RegExp(`(?<!==)(${escaped})(? !==)`, 'gi');
      highlightedSnippet = highlightedSnippet.replace(rx, '==$1==');
    } catch (_) {}
  }

  return {
    highlightedText: extractedSentence.replace(/^\.\.\.|\.\.\.$/g, '').trim(),
    snippet: highlightedSnippet
  };
}

/**
 * Soruları dosyalara güvenli bir şekilde kaydeder
 */
export function savePastQuestions(questions) {
  const jsonStr = JSON.stringify(questions, null, 2);
  fs.writeFileSync(DATA_PAST_PATH, jsonStr, 'utf8');
  if (fs.existsSync(path.dirname(SRC_PAST_PATH))) {
    fs.writeFileSync(SRC_PAST_PATH, jsonStr, 'utf8');
  }
}
