import React, { useState } from 'react';
import { AlertTriangle, Check, Copy, Eye, Lightbulb, Megaphone, NotebookPen, Target, X, Zap } from 'lucide-react';
import type { CalloutTone, Question, Spot } from './parseSummary';

/** Özet okuyucusunun blok parçaları. Yalnız token renkleri (styles/summary.css · .sr-*). */
type RenderText = (text: string) => React.ReactNode;

const CALLOUT: Record<CalloutTone, { icon: React.ElementType; label: string }> = {
  warning: { icon: AlertTriangle, label: 'Sınav tuzağı' },
  important: { icon: Megaphone, label: 'Hoca vurgusu' },
  tip: { icon: Lightbulb, label: 'Klinik ipucu' },
  note: { icon: NotebookPen, label: 'Not' },
};

/** "DERS NOTU HOCA VURGUSU | Sınav İkazı" → "Hoca vurgusu · Sınav ikazı" */
const tidyTitle = (t: string) =>
  t
    .split('|')
    .map((p) => p.trim().replace(/^ders notu\s+/i, ''))
    .filter(Boolean)
    .map((p) => (p === p.toLocaleUpperCase('tr') ? p.toLocaleLowerCase('tr') : p))
    .map((p) => p.charAt(0).toLocaleUpperCase('tr') + p.slice(1))
    .join(' · ');

export const Callout: React.FC<{ tone: CalloutTone; title?: string; text: string; items: string[]; renderText: RenderText }> = ({
  tone,
  title,
  text,
  items,
  renderText,
}) => {
  const c = CALLOUT[tone];
  const Icon = c.icon;
  return (
    <aside className={`sr-callout is-${tone}`}>
      <div className="sr-callout-h">
        <Icon aria-hidden />
        <b>{title ? tidyTitle(title) : c.label}</b>
      </div>
      {text && <p>{renderText(text)}</p>}
      {items.length > 0 && (
        <ul>
          {items.map((it, i) => (
            <li key={i}>{renderText(it)}</li>
          ))}
        </ul>
      )}
    </aside>
  );
};

export const DataTable: React.FC<{ id: string; headers: string[]; rows: string[][]; renderText: RenderText }> = ({ id, headers, rows, renderText }) => (
  <figure className="sr-table" data-anchor={id}>
    <div className="sr-table-scroll" tabIndex={0} role="region" aria-label={`Tablo: ${headers.slice(0, 2).join(' / ')}`}>
      <table>
        <thead>
          <tr>
            {headers.map((h, i) => (
              <th key={i} scope="col">
                {renderText(h)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, ri) => (
            <tr key={ri}>
              {r.map((cell, ci) =>
                ci === 0 ? (
                  <th key={ci} scope="row">
                    {renderText(cell)}
                  </th>
                ) : (
                  <td key={ci}>{renderText(cell)}</td>
                )
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </figure>
);

export const Objectives: React.FC<{ items: string[]; renderText: RenderText }> = ({ items, renderText }) => (
  <ol className="sr-goals">
    {items.map((it, i) => (
      <li key={i} style={{ '--i': i } as React.CSSProperties}>
        <Target aria-hidden />
        <span>{renderText(it)}</span>
      </li>
    ))}
  </ol>
);

export const SpotWall: React.FC<{ spots: Spot[]; renderText: RenderText }> = ({ spots, renderText }) => {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    const txt = spots.map((s, i) => `${i + 1}. ${s.term ? `${s.term}: ` : ''}${s.text}`).join('\n');
    navigator.clipboard?.writeText(txt).then(
      () => {
        setCopied(true);
        window.setTimeout(() => setCopied(false), 1800);
      },
      () => {}
    );
  };
  return (
    <div className="sr-spots">
      <div className="sr-spots-bar">
        <span>
          <Zap aria-hidden /> {spots.length} yüksek verimli bilgi
        </span>
        <button type="button" className="sr-chip-btn" onClick={copy} aria-live="polite">
          {copied ? <Check aria-hidden /> : <Copy aria-hidden />}
          {copied ? 'Kopyalandı' : 'Kopyala'}
        </button>
      </div>
      <ol className="sr-spots-grid">
        {spots.map((s, i) => (
          <li key={i} className="sr-spot" style={{ '--i': i } as React.CSSProperties}>
            <span className="sr-spot-n">{String(i + 1).padStart(2, '0')}</span>
            {s.term && <b>{renderText(s.term)}</b>}
            <p>{renderText(s.text)}</p>
          </li>
        ))}
      </ol>
    </div>
  );
};

/** Çıkmış soru: şıkka dokununca hemen değerlendirilir; çözüm kayarak açılır. */
export const QuestionCard: React.FC<{
  q: Question;
  picked?: string;
  revealed: boolean;
  onPick: (letter: string) => void;
  onReveal: () => void;
  renderText: RenderText;
}> = ({ q, picked, revealed, onPick, onReveal, renderText }) => {
  const done = revealed || !!picked;
  const correct = picked && q.answer ? picked === q.answer : undefined;
  return (
    <article className={`sr-q ${done ? 'is-done' : ''}`} data-anchor={q.id}>
      <header className="sr-q-h">
        <span className="sr-q-no">Soru {q.number}</span>
        {q.tag && <span className="sr-q-tag">{q.tag}</span>}
        {picked && correct !== undefined && (
          <span className={`sr-q-verdict ${correct ? 'is-ok' : 'is-bad'}`}>
            {correct ? <Check aria-hidden /> : <X aria-hidden />}
            {correct ? 'Doğru' : 'Yanlış'}
          </span>
        )}
      </header>
      <div className="sr-q-stem">
        {q.stem.split('\n').map((l, i) => (
          <p key={i}>{renderText(l)}</p>
        ))}
      </div>
      {q.options.length > 0 && (
        <div className="sr-q-opts" role="group" aria-label={`Soru ${q.number} şıkları`}>
          {q.options.map((o) => {
            const isAns = done && q.answer === o.letter;
            const isWrong = done && picked === o.letter && q.answer && q.answer !== o.letter;
            const state = isAns ? 'is-ans' : isWrong ? 'is-wrong' : picked === o.letter ? 'is-picked' : done ? 'is-dim' : '';
            return (
              <button key={o.letter} type="button" className={`sr-opt ${state}`} onClick={() => !done && onPick(o.letter)} aria-disabled={done} aria-pressed={picked === o.letter}>
                <b>{isAns ? <Check aria-hidden /> : isWrong ? <X aria-hidden /> : o.letter}</b>
                <span>{renderText(o.text)}</span>
              </button>
            );
          })}
        </div>
      )}
      {!done && (
        <button type="button" className="sr-q-reveal" onClick={onReveal}>
          <Eye aria-hidden /> Çözümü göster
        </button>
      )}
      <div className={`sr-q-sol ${done ? 'is-open' : ''}`} aria-hidden={!done} inert={!done ? true : undefined}>
        <div>
          <div className="sr-q-sol-in">
            <p className="sr-q-key">
              Doğru cevap: <b>{q.answer || 'anahtar yok'}</b>
            </p>
            {q.explanation && q.explanation.split('\n').map((l, i) => <p key={i}>{renderText(l)}</p>)}
          </div>
        </div>
      </div>
    </article>
  );
};
