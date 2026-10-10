/**
 * Soru kitapçığı: her soru Çıkmış sayfasındaki kartla (cx-q) aynı işaretlemeyle çizilir; açıklama
 * "Hakkında" penceresindeki SourceText ile, şık analizi aynı ms-about-analysis listesiyle gelir.
 */
import React from 'react';
import { BookOpen, Check, ShieldCheck, Library, PencilLine } from 'lucide-react';
import { StemText } from '../ui/StemText';
import { SourceText } from '../ui/SourceText';
import type { PdfQuestion } from './pdfSources';
import { committeeShort } from './pdfSources';
import { Cover, Masthead, type CoverInfo } from './PdfParts';

export type BookletMode = 'student' | 'solution' | 'key';
export type OptionNotes = 'off' | 'inline' | 'analysis';
export type GroupBy = 'none' | 'discipline' | 'year' | 'committee' | 'topic' | 'group';

export interface QuestionDocOptions {
  mode: BookletMode;
  markCorrect: boolean;
  explanation: boolean;
  optionNotes: OptionNotes;
  refs: boolean;
  meta: boolean;
  badges: boolean;
  /** Çözüm bilgisi soru altında mı, kitapçığın sonunda mı */
  solutionsAtEnd: boolean;
  answerKey: boolean;
  opticForm: boolean;
  columns: 1 | 2;
  compact: boolean;
  groupBy: GroupBy;
  groupNewPage: boolean;
  writeSpace: boolean;
  /** Her soru (ve sonda çözüm varsa her çözüm) ayrı sayfada; sütun tek olur */
  questionPerPage?: boolean;
  numbering: 'sequential' | 'original';
  cover: boolean;
}

const DIFF_TONE: Record<string, string> = { kolay: 'is-ok', orta: 'is-accent', zor: 'is-warn' };
const DIFF_LABEL: Record<string, string> = { kolay: 'Kolay', orta: 'Orta', zor: 'Zor' };

const groupKey = (q: PdfQuestion, by: GroupBy): string => {
  if (by === 'discipline') return q.discipline || 'Diğer';
  if (by === 'year') return q.year || 'Yılı belirsiz';
  if (by === 'committee') return committeeShort(q.committeeId) || 'Kurul belirsiz';
  if (by === 'topic') return q.topic || 'Konu belirsiz';
  if (by === 'group') return q.group || q.topic || 'Diğer';
  return '';
};

/** Şık analizi: Hakkında penceresindeki liste. */
const Analysis: React.FC<{ q: PdfQuestion }> = ({ q }) => (
  <section className="pd-qblock">
    <span className="pd-qblock-h"><ShieldCheck /> Şık analizi</span>
    <ol className="ms-about-analysis">
      {q.options
        .filter((o) => o.why)
        .map((o) => {
          const isAnswer = q.answer === o.key;
          return (
            <li key={o.key} className={isAnswer ? 'is-answer' : ''}>
              <span className="ms-about-analysis-key">{o.key}</span>
              <div className="min-w-0 flex-1 flex flex-col gap-1">
                <div className="flex flex-wrap items-center gap-1.5">
                  <span className="text-[13.5px] font-medium text-ink leading-snug mr-1">{o.text}</span>
                  {o.verdict && <span className={`ms-tag is-${o.verdict.tone}`}>{o.verdict.label}</span>}
                  {isAnswer && <span className="ms-tag is-ok"><Check /> Cevap</span>}
                </div>
                <p className="m-0 text-[13px] text-ink-2 leading-relaxed">{o.why}</p>
              </div>
            </li>
          );
        })}
    </ol>
  </section>
);

/** Çözüm bilgisi: cevap satırı + açıklama + şık analizi + referanslar */
const Solution: React.FC<{ q: PdfQuestion; o: QuestionDocOptions; withAnswerLine: boolean }> = ({ q, o, withAnswerLine }) => {
  const hasNotes = o.optionNotes === 'analysis' && q.options.some((x) => x.why);
  return (
    <>
      {withAnswerLine && (
        <p className="pd-answer-line m-0">
          {q.answer ? <><span className="cx-bubble">{q.answer}</span> Doğru cevap {q.answer}</> : <span className="text-ink-3">Cevap anahtarı yok</span>}
        </p>
      )}
      {o.explanation && q.explanation && (
        <section className="ls-expl">
          <span className="ls-expl-h"><BookOpen aria-hidden /> Açıklama</span>
          <SourceText text={q.explanation} size="sm" answerTerms={q.options.filter((x) => x.key === q.answer).map((x) => x.text)} />
        </section>
      )}
      {hasNotes && <Analysis q={q} />}
      {o.refs && q.refs.length > 0 && (
        <section className="pd-qblock">
          <span className="pd-qblock-h"><Library /> Referans kaynaklar</span>
          <ul className="pd-refs">{q.refs.map((r, i) => <li key={i}>{r}</li>)}</ul>
        </section>
      )}
    </>
  );
};

const QuestionCard: React.FC<{ q: PdfQuestion; no: number | string; o: QuestionDocOptions }> = ({ q, no, o }) => {
  const showAnswer = o.mode === 'solution' && !o.solutionsAtEnd;
  const mark = showAnswer && o.markCorrect;
  const inlineWhy = showAnswer && o.optionNotes === 'inline';
  const meta = [q.source === 'mini' || q.source === 'ornek' ? q.topic : committeeShort(q.committeeId), q.year].filter(Boolean).join(' · ');
  const short = q.options.every((x) => x.text.length <= 42) && !inlineWhy;
  return (
    <article className="cx-q">
      <header className="cx-q-head">
        <span className="cx-q-no">{no}</span>
        {o.meta && (
          <span className="cx-q-meta">
            <b>{q.discipline}</b>
            {meta && <span>{meta}</span>}
          </span>
        )}
        {!o.meta && <span className="flex-1" />}
        {(o.badges || q.difficulty) && (
          <span className="cx-q-flags">
            {q.difficulty && <span className={`cx-flag ${DIFF_TONE[q.difficulty] === 'is-accent' ? 'is-new' : DIFF_TONE[q.difficulty]}`}>{DIFF_LABEL[q.difficulty]}</span>}
            {o.badges && q.badges.map((b) => <span key={b.label} className={`cx-flag is-${b.tone === 'accent' ? 'new' : b.tone}`}>{b.label}</span>)}
          </span>
        )}
      </header>
      {o.meta && q.group && q.source !== 'past' && <p className="m-0 -mt-1 text-[12.5px] text-ink-3 leading-snug">{q.group}</p>}
      <StemText text={q.stem} />
      {q.options.length > 0 && (
        <ol className={`cx-opts ${short ? 'is-short' : ''}`}>
          {q.options.map((opt) => {
            const ok = mark && opt.key === q.answer;
            return (
              <React.Fragment key={opt.key}>
                <li className={`cx-opt-li ${inlineWhy && opt.why ? 'has-why' : ''}`}>
                  <div className={`cx-opt ${ok ? 'is-correct' : ''}`}>
                    <span className="cx-bubble">{ok ? <Check strokeWidth={3} /> : opt.key}</span>
                    <span className="cx-opt-t">{opt.text}</span>
                  </div>
                </li>
                {inlineWhy && opt.why && (
                  <li className={`pd-why ${opt.key === q.answer ? 'is-ok' : ''}`}>
                    <span className="ls-opt-verdict">{opt.verdict?.label || (opt.key === q.answer ? 'Neden doğru' : 'Neden yanlış')}</span>
                    {opt.why}
                  </li>
                )}
              </React.Fragment>
            );
          })}
        </ol>
      )}
      {showAnswer && <Solution q={q} o={o} withAnswerLine={!o.markCorrect || !q.options.length} />}
      {o.writeSpace && (
        <div className="pd-write" aria-hidden>
          <span className="pd-qblock-h"><PencilLine /> Notlar</span>
          <i /><i />
        </div>
      )}
    </article>
  );
};

export interface QuestionDocProps {
  questions: PdfQuestion[];
  options: QuestionDocOptions;
  cover: CoverInfo;
}

export const QuestionDoc: React.FC<QuestionDocProps> = ({ questions, options: o, cover }) => {
  // Gruplar: soru sırası korunur, aynı gruptakiler bir başlık altında toplanır
  const groups: { name: string; items: { q: PdfQuestion; i: number }[] }[] = [];
  if (o.groupBy === 'none') groups.push({ name: '', items: questions.map((q, i) => ({ q, i })) });
  else {
    const map = new Map<string, { q: PdfQuestion; i: number }[]>();
    questions.forEach((q, i) => {
      const k = groupKey(q, o.groupBy);
      if (!map.has(k)) map.set(k, []);
      map.get(k)!.push({ q, i });
    });
    map.forEach((items, name) => groups.push({ name, items }));
  }
  // Gruplamada numara grup sırasına göre yeniden verilir
  let seq = 0;
  const ordered = groups.map((g) => ({ ...g, items: g.items.map((it) => ({ ...it, no: o.numbering === 'original' && it.q.number ? it.q.number : ++seq })) }));
  const flat = ordered.flatMap((g) => g.items);
  const showQuestions = o.mode !== 'key';
  const showSolutionsAtEnd = o.mode === 'solution' && o.solutionsAtEnd;

  return (
    <>
      {o.cover ? <Cover info={cover} /> : <Masthead info={cover} />}

      {showQuestions && (
        <div className={`pd-qlist ${o.questionPerPage ? 'is-page' : o.columns === 2 ? 'is-two' : ''} ${o.compact ? 'is-compact' : ''} ${o.mode === 'solution' && !o.solutionsAtEnd && (o.explanation || o.optionNotes !== 'off') ? 'is-flow' : ''}`}>
          {ordered.map((g, gi) => (
            <React.Fragment key={g.name || gi}>
              {g.name && (
                <h2 className={`pd-group ${o.groupNewPage && gi > 0 ? 'is-break' : ''}`}>
                  {g.name} <span>{g.items.length} soru</span>
                </h2>
              )}
              {g.items.map(({ q, no }) => <QuestionCard key={q.id} q={q} no={no} o={o} />)}
            </React.Fragment>
          ))}
        </div>
      )}

      {showSolutionsAtEnd && (
        <section className="pd-section">
          <h2 className="pd-section-h">Çözümler <span>{flat.length} soru</span></h2>
          {flat.map(({ q, no }) => {
            const right = q.options.find((x) => x.key === q.answer);
            return (
              <div key={q.id} className={`pd-sol ${o.questionPerPage ? 'is-page' : ''}`}>
                <div className="pd-sol-h">
                  <span className="cx-q-no">{no}</span>
                  <b>{q.answer ? `Cevap ${q.answer}` : 'Cevap anahtarı yok'}{right ? ` · ${right.text}` : ''}</b>
                  {o.meta && <small>{q.discipline}</small>}
                </div>
                {o.optionNotes === 'inline' && q.options.some((x) => x.why) ? (
                  <Analysis q={q} />
                ) : null}
                <Solution q={q} o={{ ...o, optionNotes: o.optionNotes === 'inline' ? 'off' : o.optionNotes }} withAnswerLine={false} />
              </div>
            );
          })}
        </section>
      )}

      {(o.answerKey || o.mode === 'key') && flat.length > 0 && (
        <section className={showQuestions || showSolutionsAtEnd ? 'pd-section' : ''}>
          <h2 className="pd-section-h">Cevap anahtarı <span>{flat.filter((x) => x.q.answer).length} / {flat.length} sorunun cevabı belli</span></h2>
          <div className="pd-key">
            {flat.map(({ q, no }) => (
              <div key={q.id}>
                <small>{no}</small>
                <b className={q.answer ? '' : 'is-none'}>{q.answer || '–'}</b>
              </div>
            ))}
          </div>
        </section>
      )}

      {o.opticForm && flat.length > 0 && (
        <section className="pd-section">
          <h2 className="pd-section-h">Optik form <span>Cevabını kurşun kalemle doldur</span></h2>
          <div className="pd-optic">
            {flat.map(({ q, no }) => (
              <div key={q.id}>
                <small>{no}</small>
                {(q.options.length ? q.options.map((x) => x.key) : ['A', 'B', 'C', 'D', 'E']).map((k) => <span key={k}>{k}</span>)}
              </div>
            ))}
          </div>
        </section>
      )}
    </>
  );
};
