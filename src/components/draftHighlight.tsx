import React from 'react';
import { areWordsFuzzyEqual, foldTurkish, toContextHashtag } from '../utils/fuzzyMatching';

// ---------------------------------------------------------------------------
// Shared-word colouring: words that recur across drafts of one cluster get the
// same pastel colour, so overlaps are visible at a glance.
// Tolerates typos, missing letters (sendrmu -> sendromu) and transpositions
// (sendormu -> sendromu).
// ---------------------------------------------------------------------------
export const WORD_COLORS = [
  '#FEF08A', // pastel sarı
  '#BBF7D0', // pastel yeşil
  '#FBCFE8', // pastel pembe
  '#BFDBFE', // pastel mavi
  '#DDD6FE', // pastel mor
  '#FED7AA', // pastel turuncu
  '#99F6E4', // pastel turkuaz
  '#FECDD3', // pastel mercan
];

const STOP = new Set(
  'hasta hastada hastanın hastaya hastanin olan olarak ile için icin veya hangisi hangisidir aşağıdaki asagidaki daha gibi sonra kadar soru sorusu sorudu bunun buna olan yaşında yasinda ancak değil degil dolayı ilgili durum durumu durumda şekilde sekilde vardı vardi oldu olur olması olmasi kişi kisi hocam hoca bence sanki hatırlıyorum hatirliyorum hatırlanan sordu sorulmuştu şıkkı sikki şıklar siklar cevap doğru dogru yanlış yanlis bulunan bulunur görülür gorulur görüldü tanısı tanisi tanı tani ilgili arasında arasinda sırasında sirasinda nedir neden her bir iki üç dört beş'.split(' ')
);

export const wordKey = (w: string): string => {
  const t = foldTurkish(w).trim();
  return t.length >= 7 ? t.slice(0, 5) : t;
};

export const tokens = (text: string): string[] =>
  (text.match(/[\p{L}\p{N}]+/gu) || []).filter(
    (w) => w.length >= 3 && !STOP.has(foldTurkish(w))
  );

/**
 * Kelimeleri harf eksikliği, yer değiştirmesi ve Türkçe gövdeye göre kümeleyip
 * her ortak kümeye aynı rengi atar.
 */
export const sharedWordColors = (texts: string[]): Map<string, string> => {
  // 1. Tüm metinlerdeki benzersiz kelimeleri topla
  const textWordSets: Array<Set<string>> = texts.map(
    (t) => new Set(tokens(t).map((w) => foldTurkish(w)))
  );

  // 2. Bulanık kümeleme (Fuzzy clusters): Birbirine benzer kelimeler tek kümede birleşir
  interface WordCluster {
    rep: string; // Temsilci kelime
    variants: Set<string>;
    seenInCount: number;
  }

  const clusters: WordCluster[] = [];

  for (const wordSet of textWordSets) {
    const matchedClustersInDoc = new Set<WordCluster>();

    for (const word of wordSet) {
      // Var olan bir küme ile eşleşiyor mu? (Harf eksikliği / yer değiştirmesi denetimi)
      let found = clusters.find((c) => areWordsFuzzyEqual(word, c.rep));
      if (!found) {
        found = {
          rep: word,
          variants: new Set([word]),
          seenInCount: 0,
        };
        clusters.push(found);
      } else {
        found.variants.add(word);
        // Daha uzun / düzgün kelimeyi temsilci yap
        if (word.length > found.rep.length && !word.endsWith('u') && !word.endsWith('i')) {
          found.rep = word;
        }
      }
      matchedClustersInDoc.add(found);
    }

    for (const c of matchedClustersInDoc) {
      c.seenInCount++;
    }
  }

  // 3. En az 2 farklı metinde görülen kümeleri frekans ve uzunluğa göre sırala
  const shared = clusters
    .filter((c) => c.seenInCount >= 2)
    .sort((a, b) => b.seenInCount - a.seenInCount || b.rep.length - a.rep.length)
    .slice(0, WORD_COLORS.length);

  // 4. Tüm kelime varyasyonlarını aynı renge haritala
  const colorMap = new Map<string, string>();
  shared.forEach((c, idx) => {
    const color = WORD_COLORS[idx];
    for (const v of c.variants) {
      colorMap.set(v, color);
      colorMap.set(wordKey(v), color);
    }
  });

  return colorMap;
};

/**
 * Belirli bir kelimenin renklendirme haritasındaki karşılığını döner.
 * Harf eksikliği veya yer değiştirme varsa bile doğru rengi bulur.
 */
export function getWordColor(word: string, colors: Map<string, string>): string | undefined {
  if (!colors.size || !word) return undefined;
  const raw = foldTurkish(word);
  const direct = colors.get(raw) || colors.get(wordKey(raw));
  if (direct) return direct;

  // Doğrudan eşleşmediyse bulanık eşleşen varyasyonun rengini al
  for (const [key, color] of colors.entries()) {
    if (areWordsFuzzyEqual(raw, key)) {
      return color;
    }
  }
  return undefined;
}

/** Renders text with shared words painted in their colour. */
export const Colored: React.FC<{ text: string; colors: Map<string, string> }> = ({ text, colors }) => {
  if (!colors.size || !text) return <>{text}</>;
  const parts = text.split(/([\p{L}\p{N}]+)/u);
  return (
    <>
      {parts.map((part, i) => {
        const c = i % 2 === 1 && part.length >= 3 ? getWordColor(part, colors) : undefined;
        return c ? (
          <mark key={i} className="rounded px-1 -mx-0.5 font-medium text-ink" style={{ backgroundColor: c }}>
            {part}
          </mark>
        ) : (
          <React.Fragment key={i}>{part}</React.Fragment>
        );
      })}
    </>
  );
};

/**
 * Bağlam etiketi rozeti (#DownSendromu gibi).
 * Her iki sorunun ortak konusu / bağlamı varsa aynı renkte gösterilir.
 */
export const ContextBadge: React.FC<{
  hashtag: string;
  className?: string;
  colorIndex?: number;
}> = ({ hashtag, className = '', colorIndex = 1 }) => {
  if (!hashtag) return null;
  const tag = hashtag.startsWith('#') ? hashtag : `#${hashtag}`;
  const bg = WORD_COLORS[colorIndex % WORD_COLORS.length];

  return (
    <span
      className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[12px] font-semibold text-ink border border-black/5 shadow-2xs ${className}`}
      style={{ backgroundColor: bg }}
      title={`Ortak bağlam: ${tag}`}
    >
      <span className="opacity-75 font-mono">#</span>
      <span>{tag.replace(/^#/, '')}</span>
    </span>
  );
};

/** The coloured keywords as a small legend. */
export const WordLegend: React.FC<{ texts: string[]; colors: Map<string, string> }> = ({ texts, colors }) => {
  if (!colors.size) return null;
  const spelled = new Map<string, string>();
  texts.forEach((t) =>
    tokens(t).forEach((w) => {
      const c = getWordColor(w, colors);
      if (c && !spelled.has(c)) {
        spelled.set(c, w.toLocaleLowerCase('tr-TR'));
      }
    })
  );

  if (spelled.size === 0) return null;

  return (
    <div className="flex flex-wrap items-center gap-1.5 pt-0.5">
      <span className="text-[11.5px] font-semibold text-ink-3 mr-0.5">Ortak terimler:</span>
      {Array.from(spelled.entries()).map(([c, word]) => (
        <span
          key={c}
          className="h-5 px-2 rounded-md text-[11.5px] font-medium text-ink inline-flex items-center shadow-2xs border border-black/5"
          style={{ backgroundColor: c }}
        >
          {word}
        </span>
      ))}
    </div>
  );
};
