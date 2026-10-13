import React from 'react';

/**
 * Test çöz · soru gezgini (v10). Masaüstünde sağ sütunda durur, telefon/tablette aynı ızgara
 * alt sayfada (Sheet) açılır. Hücre durumları: şu anki · işaretli · doğru · yanlış · boş.
 */
export interface NavItem {
  id: string;
  answer?: string;
  correct?: string;
}

interface Props {
  items: NavItem[];
  current: number;
  marked: Set<string>;
  onGo: (i: number) => void;
  /** Ezber başlığı (ör. "Soru gezgini") — yalnız ekran okuyucular için */
  label?: string;
}

export const navCounts = (items: NavItem[], marked: Set<string>) => {
  let answered = 0;
  let correct = 0;
  items.forEach((q) => {
    if (!q.answer) return;
    answered++;
    if (q.answer === q.correct) correct++;
  });
  const markedN = items.filter((q) => marked.has(q.id)).length;
  return { answered, correct, wrong: answered - correct, empty: items.length - answered, marked: markedN };
};

export const TestNavigator: React.FC<Props> = ({ items, current, marked, onGo, label = 'Soru gezgini' }) => {
  const c = navCounts(items, marked);
  return (
    <div className="tx-nav">
      <div className="tx-nav-legend" aria-live="polite">
        <span><i className="is-ans" aria-hidden />Cevaplanan <b>{c.answered}</b></span>
        <span><i className="is-mark" aria-hidden />İşaretli <b>{c.marked}</b></span>
        <span><i className="is-empty" aria-hidden />Boş <b>{c.empty}</b></span>
      </div>
      <nav aria-label={label} className="tx-nav-grid">
        {items.map((q, i) => {
          const isCur = i === current;
          const isMarked = marked.has(q.id);
          const st = q.answer ? (q.answer === q.correct ? 'is-ok' : 'is-bad') : '';
          const desc = [q.answer ? (q.answer === q.correct ? 'doğru' : 'yanlış') : 'boş', isMarked ? 'işaretli' : ''].filter(Boolean).join(', ');
          return (
            <button
              key={q.id}
              type="button"
              onClick={() => onGo(i)}
              aria-current={isCur ? 'step' : undefined}
              aria-label={`Soru ${i + 1}, ${desc}`}
              className={`tx-cell ${st} ${isMarked ? 'is-mark' : ''} ${isCur ? 'is-cur' : ''}`}
            >
              {i + 1}
            </button>
          );
        })}
      </nav>
    </div>
  );
};
