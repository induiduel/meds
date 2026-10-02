import React from 'react';

// ---------------------------------------------------------------------------
// Shared-word colouring: words that recur across drafts of one cluster get the
// same pastel colour, so overlaps are visible at a glance.
// Used by DraftDeduplicationModal and the manage-console drafts workshop.
// ---------------------------------------------------------------------------
export const WORD_COLORS = ['#FEF08A', '#BBF7D0', '#FBCFE8', '#BFDBFE', '#DDD6FE', '#FED7AA', '#99F6E4', '#FECDD3'];

const STOP = new Set(
  'hasta hastada hastanın hastaya hastanin olan olarak ile için icin veya hangisi hangisidir aşağıdaki asagidaki daha gibi sonra kadar soru sorusu sorudu bunun buna olan yaşında yasinda ancak değil degil dolayı ilgili durum durumu durumda şekilde sekilde vardı vardi oldu olur olması olmasi kişi kisi hocam hoca bence sanki hatırlıyorum hatirliyorum hatırlanan sordu sorulmuştu şıkkı sikki şıklar siklar cevap doğru dogru yanlış yanlis bulunan bulunur görülür gorulur görüldü tanısı tanisi tanı tani ilgili arasında arasinda sırasında sirasinda nedir neden'.split(' ')
);

export const wordKey = (w: string) => {
  const t = w.toLocaleLowerCase('tr-TR');
  // Turkish suffixes: compare by the first 5 letters of longer words ("sendromu" ~ "sendrom")
  return t.length >= 7 ? t.slice(0, 5) : t;
};

export const tokens = (text: string) =>
  (text.match(/[\p{L}\p{N}]+/gu) || []).filter((w) => w.length >= 4 && !STOP.has(w.toLocaleLowerCase('tr-TR')));

/** Word keys that appear in at least two different texts, coloured by how widely they recur. */
export const sharedWordColors = (texts: string[]): Map<string, string> => {
  const seenIn = new Map<string, number>();
  texts.forEach((t) => {
    new Set(tokens(t).map(wordKey)).forEach((k) => seenIn.set(k, (seenIn.get(k) || 0) + 1));
  });
  const shared = [...seenIn.entries()]
    .filter(([, n]) => n >= 2)
    .sort((a, b) => b[1] - a[1] || b[0].length - a[0].length)
    .slice(0, WORD_COLORS.length);
  return new Map(shared.map(([k], i) => [k, WORD_COLORS[i]]));
};

/** Renders text with shared words painted in their colour. */
export const Colored: React.FC<{ text: string; colors: Map<string, string> }> = ({ text, colors }) => {
  if (!colors.size || !text) return <>{text}</>;
  const parts = text.split(/([\p{L}\p{N}]+)/u);
  return (
    <>
      {parts.map((part, i) => {
        const c = i % 2 === 1 && part.length >= 4 ? colors.get(wordKey(part)) : undefined;
        return c ? (
          <mark key={i} className="rounded-[4px] px-[2px] -mx-[1px] text-inherit" style={{ background: c }}>
            {part}
          </mark>
        ) : (
          <React.Fragment key={i}>{part}</React.Fragment>
        );
      })}
    </>
  );
};

/** The coloured keywords as a small legend. */
export const WordLegend: React.FC<{ texts: string[]; colors: Map<string, string> }> = ({ texts, colors }) => {
  if (!colors.size) return null;
  // Show one real spelling per key
  const spelled = new Map<string, string>();
  texts.forEach((t) => tokens(t).forEach((w) => !spelled.has(wordKey(w)) && spelled.set(wordKey(w), w.toLocaleLowerCase('tr-TR'))));
  return (
    <span className="flex flex-wrap items-center gap-1">
      <span className="text-[11.5px] text-ink-3 mr-0.5">Ortak:</span>
      {[...colors.entries()].map(([k, c]) => (
        <span key={k} className="h-5 px-1.5 rounded-[6px] text-[11.5px] text-ink inline-flex items-center" style={{ background: c }}>
          {spelled.get(k) || k}
        </span>
      ))}
    </span>
  );
};
