import { foldText } from './searchText';

/**
 * Bir sorudan slaytta/kaynakta işaretlenecek ifadeler: soru kökünün ayırt edici kelimeleri ve doğru şık.
 * Terimler katlanmış (Türkçe karakter + küçük harf) döner; ekli biçimleri de yakalamak için uzun kelimelerin kökü alınır.
 */
export interface QuestionFocus {
  questionId: string;
  label: string;
  /** Hangi slayt için (Öğren'de yalnız o slaytta bant gösterilir) */
  deckId?: string;
  slideNumber?: number;
  terms: string[];
  answerTerms: string[];
  answerKey?: string;
  answerText?: string;
}

const STOP = new Set(
  [
    'asagidakilerden', 'asagidaki', 'hangisi', 'hangisidir', 'hangileri', 'yanlistir', 'dogrudur', 'degildir', 'yukaridakilerden',
    'olarak', 'olan', 'olmayan', 'icin', 'ile', 'veya', 'ancak', 'gibi', 'daha', 'en', 'cok', 'bir', 'iki', 'uc', 'bu', 'su',
    'hasta', 'hastanin', 'hastada', 'yasinda', 'yasindaki', 'erkek', 'kadin', 'basvuran', 'basvurdu', 'sikayetiyle', 'sikayeti',
    'bulgu', 'bulgusu', 'bulgular', 'bulgulari', 'tani', 'tanisi', 'tedavi', 'tedavisi', 'durum', 'durumda', 'neden', 'nedeni',
    'ozellik', 'ozelligi', 'ozellikleri', 'iliskili', 'birlikte', 'sonra', 'once', 'kadar', 'fazla', 'genellikle', 'siklikla',
    'muayenesinde', 'muayene', 'saptanan', 'saptanir', 'gorulur', 'gorulen', 'olabilir', 'edilir', 'yapilir', 'tanimlanir',
    'hepsi', 'hicbiri', 'tumu', 'sadece', 'yalniz', 'diger', 'durumlardan', 'ifadelerden', 'bilgilerden',
  ].map((w) => foldText(w)),
);

const words = (text: string) =>
  foldText(String(text || ''))
    .replace(/[^a-z0-9çğıöşü\s-]/g, ' ')
    .split(/\s+/)
    .filter((w) => w.length >= 4 && !STOP.has(w) && !/^\d+$/.test(w));

/** Uzun kelimenin ekleri atılır: "hepatitinde" → "hepati" (alt dizgi araması ekli biçimleri de bulur). */
const stem = (w: string) => (w.length > 7 ? w.slice(0, Math.max(6, w.length - 3)) : w);

export function buildQuestionFocus(input: {
  id: string;
  label: string;
  stem: string;
  options?: { key: string; text: string }[];
  answer?: string;
  deckId?: string;
  slideNumber?: number;
}): QuestionFocus {
  const key = String(input.answer || '').trim().toUpperCase();
  const answerText = String(input.options?.find((o) => String(o.key).toUpperCase() === key)?.text || '').trim();
  const answerWords = Array.from(new Set(words(answerText).map(stem)));
  const answerTerms = [...(answerText && answerText.length <= 48 ? [foldText(answerText)] : []), ...answerWords].filter(Boolean);
  // Kökte geçen kelimeler sıklık/uzunluğa göre: uzun ve tıbbi görünenler önce
  const seen = new Set(answerWords);
  const terms: string[] = [];
  for (const w of words(input.stem).sort((a, b) => b.length - a.length)) {
    const s = stem(w);
    if (s.length < 5 || seen.has(s)) continue;
    seen.add(s);
    terms.push(s);
    if (terms.length >= 10) break;
  }
  return {
    questionId: input.id,
    label: input.label,
    deckId: input.deckId,
    slideNumber: input.slideNumber,
    terms,
    answerTerms,
    answerKey: key || undefined,
    answerText: answerText || undefined,
  };
}

const isWordChar = (c: string) => /[\p{L}\p{N}]/u.test(c);

/** Katlanmış metinde terimlerin kapladığı aralıklar; 2 = doğru şık, 1 = soru terimi (şık önceliklidir). */
export function focusMarks(text: string, terms: string[], answerTerms: string[]): Uint8Array {
  const folded = foldText(text);
  const marks = new Uint8Array(text.length);
  if (folded.length !== text.length) return marks;
  const paint = (list: string[], v: number) => {
    for (const t of list) {
      if (!t || t.length < 3) continue;
      let from = 0;
      for (;;) {
        const i = folded.indexOf(t, from);
        if (i < 0) break;
        from = i + t.length;
        // Yalnızca kelime başında eşleş; kök eşleşmesini kelimenin sonuna kadar uzat ("polip" → "polipler")
        if (i > 0 && isWordChar(folded[i - 1])) continue;
        let end = i + t.length;
        while (end < folded.length && isWordChar(folded[end])) end++;
        for (let j = i; j < end; j++) if (marks[j] < v) marks[j] = v;
      }
    }
  };
  paint(terms, 1);
  paint(answerTerms, 2);
  return marks;
}
