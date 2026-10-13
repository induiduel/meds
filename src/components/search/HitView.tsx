import React, { useMemo, useState } from 'react';
import { Check, Eye, EyeOff } from 'lucide-react';
import { NoteLeafContext, NoteMarkdown } from '../ui/NoteMarkdown';
import { Highlight } from './searchShared';
import type { FormattedHit } from './hitFormat';

/** Markdown gövde; düz metin parçalarında sorgu vurgulanır */
export const HitMarkdown: React.FC<{ text: string; query: string; className?: string }> = ({ text, query, className }) => {
  const leaf = useMemo(() => (t: string) => <Highlight text={t} query={query} />, [query]);
  return (
    <NoteLeafContext.Provider value={leaf}>
      <NoteMarkdown text={text} className={className} />
    </NoteLeafContext.Provider>
  );
};

/** Kapalı kart önizlemesi: sorularda kök + doğru şık, diğerlerinde eşleşme çevresi */
export const HitPreview: React.FC<{ f: FormattedHit; query: string }> = ({ f, query }) => {
  const [main, answer] = f.preview.split('\n✓ ');
  return (
    <>
      <span className="ms-hit-snippet"><Highlight text={main} query={query} /></span>
      {answer && (
        <span className="rb-hit-answer">
          <Check className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
          <span className="min-w-0 truncate"><Highlight text={answer} query={query} /></span>
        </span>
      )}
    </>
  );
};

/** Açık kartın yapılandırılmış içeriği */
export const HitDetail: React.FC<{ f: FormattedHit; query: string }> = ({ f, query }) => {
  const q = f.question;
  const [reveal, setReveal] = useState(true);
  return (
    <div className="rb-hit-detail">
      {f.context && (
        <p className="rb-hit-context"><b>Kazanım</b> {f.context}</p>
      )}

      {f.keyPoints.length > 0 && (
        <ul className="rb-hit-keys" aria-label="Öne çıkanlar">
          {f.keyPoints.map((k, i) => <li key={i}><Highlight text={k} query={query} /></li>)}
        </ul>
      )}

      {q && (
        <section className="rb-q" aria-label="Soru">
          <p className="rb-q-stem"><Highlight text={q.stem} query={query} /></p>
          {q.options.length > 0 && (
            <ol className="rb-q-opts">
              {q.options.map((o) => {
                const right = reveal && o.key === q.answer;
                return (
                  <li key={o.key} className={right ? 'is-right' : ''}>
                    <span className="rb-q-key" aria-hidden="true">{right ? <Check className="w-3.5 h-3.5" /> : o.key}</span>
                    <span className="min-w-0"><span className="sr-only">{o.key}) </span><Highlight text={o.text} query={query} /></span>
                    {right && <span className="sr-only"> — doğru cevap</span>}
                  </li>
                );
              })}
            </ol>
          )}
          {q.answer && q.options.length > 0 && (
            <div className="rb-q-bar">
              {reveal ? (
                <span className="rb-q-answer">Doğru cevap: <b>{q.answer}</b></span>
              ) : (
                <span className="text-sm text-ink-3">Cevap gizli — önce kendin dene</span>
              )}
              <button type="button" className="rb-q-toggle" onClick={() => setReveal((v) => !v)} aria-pressed={!reveal}>
                {reveal ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                {reveal ? 'Cevabı gizle' : 'Cevabı göster'}
              </button>
            </div>
          )}
          {(reveal || !q.options.length) && q.explanation && (
            <div className="rb-q-exp">
              <h4 className="rb-q-exp-h">Açıklama</h4>
              <HitMarkdown text={q.explanation} query={query} />
            </div>
          )}
        </section>
      )}

      {f.body && <HitMarkdown text={f.body} query={query} className="rb-hit-md" />}
    </div>
  );
};
