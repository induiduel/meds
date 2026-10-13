/**
 * Soru kitapçığı: her soru Çıkmış sayfasındaki kartla (cx-q) aynı işaretlemeyle çizilir; açıklama
 * "Hakkında" penceresindeki SourceText ile, şık analizi aynı ms-about-analysis listesiyle gelir.
 *
 * Belge içi bağlantılar: soru numarası çözümüne (#cevap-…) ya da cevap anahtarındaki hücresine (#anahtar-…)
 * gider; çözüm ve anahtar hücresi soruya geri döner (#soru-…). İçindekiler grup başlıklarına (#bolum-…) bağlanır.
 */
import React from 'react';
import { BookOpen, Check, ShieldCheck, Library, PencilLine, CornerLeftUp } from 'lucide-react';
import { StemText } from '../ui/StemText';
import { SourceText } from '../ui/SourceText';
import type { PdfQuestion } from './pdfSources';
import { committeeShort } from './pdfSources';
import { Cover, Masthead, type CoverInfo } from './PdfParts';
import { makeAnchorer, type ArrangedItem, type GroupBy, type GroupOrder, type SortBy, type SortDir } from './pdfOrder';

export type BookletMode = 'student' | 'solution' | 'key';
export type OptionNotes = 'off' | 'inline' | 'analysis';
/** Çözümlerin yeri: soru altında, her bölümün sonunda, kitapçığın sonunda */
export type AnswersAt = 'inline' | 'group' | 'end';
export type Numbering = 'sequential' | 'original' | 'group';
export type { GroupBy };

export interface QuestionDocOptions {
  mode: BookletMode;
  markCorrect: boolean;
  explanation: boolean;
  optionNotes: OptionNotes;
  refs: boolean;
  meta: boolean;
  badges: boolean;
  answersAt: AnswersAt;
  answerKey: boolean;
  opticForm: boolean;
  columns: 1 | 2 | 3;
  /** Gruplama (iki kademe) ve sıralama */
  group1: GroupBy;
  group2: GroupBy;
  groupOrder: GroupOrder;
  sortBy: SortBy;
  sortDir: SortDir;
  seed: number;
  groupNewPage: boolean;
  writeSpace: boolean;
  /** Her soru (ve sonda çözüm varsa her çözüm) ayrı sayfada; sütun tek olur */
  questionPerPage: boolean;
  numbering: Numbering;
  cover: boolean;
  toc: boolean;
  /** Soru ↔ cevap bağlantıları ve "soruya dön" işaretleri */
  links: boolean;
}

export const DEFAULT_Q: QuestionDocOptions = {
  mode: 'solution', markCorrect: true, explanation: true, optionNotes: 'inline', refs: false, meta: true, badges: false,
  answersAt: 'inline', answerKey: true, opticForm: false, columns: 1,
  group1: 'none', group2: 'none', groupOrder: 'natural', sortBy: 'source', sortDir: 'asc', seed: 1,
  groupNewPage: false, writeSpace: false, questionPerPage: false, numbering: 'sequential', cover: false, toc: false, links: true,
};

/** Eski (v2) kayıtları yeni alanlara taşır. */
export function normalizeQ(raw: any): QuestionDocOptions {
  const o: any = { ...DEFAULT_Q, ...(raw && typeof raw === 'object' ? raw : {}) };
  if (raw && raw.answersAt == null && typeof raw.solutionsAtEnd === 'boolean') o.answersAt = raw.solutionsAtEnd ? 'end' : 'inline';
  if (raw && raw.group1 == null && raw.groupBy) o.group1 = raw.groupBy === 'none' ? 'none' : raw.groupBy;
  delete o.solutionsAtEnd;
  delete o.groupBy;
  delete o.compact;
  if (![1, 2, 3].includes(o.columns)) o.columns = 1;
  if (!['inline', 'group', 'end'].includes(o.answersAt)) o.answersAt = 'inline';
  if (!['sequential', 'original', 'group'].includes(o.numbering)) o.numbering = 'sequential';
  return o as QuestionDocOptions;
}

const DIFF_TONE: Record<string, string> = { kolay: 'is-ok', orta: 'is-new', zor: 'is-warn' };
const DIFF_LABEL: Record<string, string> = { kolay: 'Kolay', orta: 'Orta', zor: 'Zor' };

/** Kitapçıktaki bir soru: numarası ve bağlantı kimlikleri */
interface Entry {
  q: PdfQuestion;
  no: number | string;
  a: string;
  /** Soru numarasının gideceği hedef (yoksa bağlantı yok) */
  to?: string;
}

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
const Solution: React.FC<{ q: PdfQuestion; o: QuestionDocOptions; withAnswerLine: boolean; notes: OptionNotes }> = ({ q, o, withAnswerLine, notes }) => {
  const hasNotes = notes === 'analysis' && q.options.some((x) => x.why);
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

const QuestionCard: React.FC<{ e: Entry; o: QuestionDocOptions }> = ({ e, o }) => {
  const { q, no } = e;
  const showAnswer = o.mode === 'solution' && o.answersAt === 'inline';
  const mark = showAnswer && o.markCorrect;
  const inlineWhy = showAnswer && o.optionNotes === 'inline';
  const meta = [q.source === 'mini' || q.source === 'ornek' ? q.topic : committeeShort(q.committeeId), q.year].filter(Boolean).join(' · ');
  const short = q.options.every((x) => x.text.length <= 42) && !inlineWhy;
  return (
    <article className="cx-q" id={`soru-${e.a}`}>
      <header className="cx-q-head">
        {e.to ? (
          <a className="cx-q-no pd-link" href={`#${e.to}`} title="Cevabına git">{no}</a>
        ) : (
          <span className="cx-q-no">{no}</span>
        )}
        {o.meta && (
          <span className="cx-q-meta">
            <b>{q.discipline}</b>
            {meta && <span>{meta}</span>}
          </span>
        )}
        {!o.meta && <span className="flex-1" />}
        {(o.badges || q.difficulty) && (
          <span className="cx-q-flags">
            {q.difficulty && <span className={`cx-flag ${DIFF_TONE[q.difficulty]}`}>{DIFF_LABEL[q.difficulty]}</span>}
            {o.badges && q.badges.map((b) => <span key={b.label} className={`cx-flag is-${b.tone === 'accent' ? 'new' : b.tone}`}>{b.label}</span>)}
          </span>
        )}
      </header>
      {o.meta && q.group && q.source !== 'past' && <p className="pd-q-sub">{q.group}</p>}
      <StemText text={q.stem} />
      {q.options.length > 0 && (
        <ol className={`cx-opts ${short ? 'is-short' : ''}`}>
          {q.options.map((opt) => {
            const ok = mark && opt.key === q.answer;
            return (
              <React.Fragment key={opt.key}>
                <li className={`cx-opt-li ${inlineWhy && opt.why ? 'has-why' : ''}`}>
                  <div className={`cx-opt ${ok ? 'is-correct' : ''}`}>
                    <span className="cx-bubble" data-k={opt.key}>{ok ? <Check strokeWidth={3} /> : opt.key}</span>
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
      {showAnswer && <Solution q={q} o={o} withAnswerLine={!o.markCorrect || !q.options.length} notes={o.optionNotes} />}
      {o.writeSpace && (
        <div className="pd-write" aria-hidden>
          <span className="pd-qblock-h"><PencilLine /> Notlar</span>
          <i /><i />
        </div>
      )}
    </article>
  );
};

/** Sonda ya da bölüm sonunda çözüm kaydı */
const SolutionEntry: React.FC<{ e: Entry; o: QuestionDocOptions }> = ({ e, o }) => {
  const { q, no } = e;
  const right = q.options.find((x) => x.key === q.answer);
  return (
    <div className={`pd-sol ${o.questionPerPage ? 'is-page' : ''}`} id={`cevap-${e.a}`}>
      <div className="pd-sol-h">
        {o.links && o.mode !== 'key' ? <a className="cx-q-no pd-link" href={`#soru-${e.a}`} title="Soruya dön">{no}</a> : <span className="cx-q-no">{no}</span>}
        <b>{q.answer ? `Cevap ${q.answer}` : 'Cevap anahtarı yok'}{right ? ` · ${right.text}` : ''}</b>
        {o.links && o.mode !== 'key' ? (
          <a className="pd-back" href={`#soru-${e.a}`}><CornerLeftUp aria-hidden /> Soruya dön</a>
        ) : (
          o.meta && <small>{q.discipline}</small>
        )}
      </div>
      {o.optionNotes === 'inline' && q.options.some((x) => x.why) ? <Analysis q={q} /> : null}
      <Solution q={q} o={o} withAnswerLine={false} notes={o.optionNotes === 'inline' ? 'off' : o.optionNotes} />
    </div>
  );
};

const KeyGrid: React.FC<{ entries: Entry[]; o: QuestionDocOptions; withIds: boolean }> = ({ entries, o, withIds }) => (
  <div className="pd-key">
    {entries.map((e) => {
      const back = o.links && o.mode !== 'key';
      const inner = (
        <>
          <small>{e.no}</small>
          <b className={e.q.answer ? '' : 'is-none'}>{e.q.answer || '–'}</b>
        </>
      );
      return back ? (
        <a key={e.a} id={withIds ? `anahtar-${e.a}` : undefined} href={`#soru-${e.a}`} className="pd-link">{inner}</a>
      ) : (
        <div key={e.a} id={withIds ? `anahtar-${e.a}` : undefined}>{inner}</div>
      );
    })}
  </div>
);

/** Düz listeden başlık + soru blokları kurar (grup yolu değiştikçe başlık). */
interface Block {
  id: string;
  key: string;
  title: string;
  level: 1 | 2;
  /** Doğrudan bu başlığın altındaki sorular */
  entries: Entry[];
  subs: Block[];
  /** Alt bölümleriyle birlikte tüm sorular (1. kademe için) */
  all: Entry[];
}

export interface QuestionDocProps {
  /** Gruplanmış ve sıralanmış sorular (pdfOrder.arrangeQuestions) */
  items: ArrangedItem[];
  options: QuestionDocOptions;
  cover: CoverInfo;
}

export const QuestionDoc: React.FC<QuestionDocProps> = ({ items, options: o, cover }) => {
  const anchor = makeAnchorer();
  const showQuestions = o.mode !== 'key';
  const solutionsElsewhere = o.mode === 'solution' && o.answersAt !== 'inline';
  const keyPerGroup = o.answersAt === 'group' && o.answerKey && o.mode !== 'key';
  const keyAtEnd = (o.answerKey && !keyPerGroup) || o.mode === 'key';

  // Bloklar ve numaralar: grup yolu değiştikçe yeni başlık; "grupta 1'den" numarası 1. kademede sıfırlanır
  const blocks: Block[] = [];
  const entries: Entry[] = [];
  let seq = 0;
  let groupSeq = 0;
  let cur1: Block | null = null;
  let cur2: Block | null = null;
  items.forEach(({ q, path }) => {
    const p1 = path[0];
    const p2 = path[1];
    const k1 = p1?.key ?? '';
    if (!cur1 || cur1.key !== k1) {
      cur1 = { id: `bolum-${blocks.filter((x) => x.level === 1).length + 1}`, key: k1, title: p1?.label || '', level: 1, entries: [], all: [], subs: [] };
      blocks.push(cur1);
      cur2 = null;
      groupSeq = 0;
    }
    if (p2 && (!cur2 || cur2.key !== p2.key)) {
      cur2 = { id: `${cur1.id}-${cur1.subs.length + 1}`, key: p2.key, title: p2.label, level: 2, entries: [], all: [], subs: [] };
      cur1.subs.push(cur2);
      blocks.push(cur2);
    }
    seq++;
    groupSeq++;
    const no = o.numbering === 'original' && q.number ? q.number : o.numbering === 'group' ? groupSeq : seq;
    const e: Entry = { q, no, a: anchor(q.id || `q${seq}`) };
    entries.push(e);
    (cur2 || cur1).entries.push(e);
    cur1.all.push(e);
  });
  // Soru numarasının hedefi
  entries.forEach((e) => {
    if (!o.links) return;
    if (solutionsElsewhere) e.to = `cevap-${e.a}`;
    else if (o.answerKey && o.mode !== 'key') e.to = `anahtar-${e.a}`;
  });

  const grouped = blocks.some((b) => b.title);
  const level1 = blocks.filter((b) => b.level === 1);
  const listClass = `pd-qlist ${o.questionPerPage ? 'is-page' : o.columns === 3 ? 'is-three' : o.columns === 2 ? 'is-two' : ''} ${
    o.mode === 'solution' && o.answersAt === 'inline' && (o.explanation || o.optionNotes !== 'off') ? 'is-flow' : ''
  }`;

  const groupTail = (b: Block) =>
    o.answersAt !== 'group' || !showQuestions || !b.all.length ? null : (
      <>
        {o.mode === 'solution' && (
          <section className="pd-gsol" id={`${b.id}-cozum`}>
            <h3 className="pd-gsol-h">{b.title ? `${b.title} · çözümler` : 'Çözümler'} <span>{b.all.length} soru</span></h3>
            {b.all.map((e) => <SolutionEntry key={e.a} e={e} o={o} />)}
          </section>
        )}
        {keyPerGroup && (
          <section className="pd-gkey">
            <h3 className="pd-gsol-h">Cevap anahtarı <span>{b.all.filter((x) => x.q.answer).length} / {b.all.length}</span></h3>
            <KeyGrid entries={b.all} o={o} withIds />
          </section>
        )}
      </>
    );

  const rangeOf = (list: Entry[]) => (list.length ? (list.length === 1 ? `Soru ${list[0].no}` : `Soru ${list[0].no}–${list[list.length - 1].no}`) : '');
  const hasTail = (o.mode === 'solution' && o.answersAt === 'end') || keyAtEnd || o.opticForm;

  return (
    <>
      {o.cover ? <Cover info={cover} /> : <Masthead info={cover} />}

      {o.toc && (grouped || hasTail) && entries.length > 0 && (
        <nav className="pd-box pd-tocbox" aria-label="İçindekiler">
          <div className="ls-sec-h">İçindekiler</div>
          <ol className="pd-toc is-linked">
            {showQuestions && grouped
              ? blocks.map((b) => (
                  <li key={b.id} className={b.level === 2 ? 'is-sub' : ''}>
                    <a href={`#${b.id}`}>
                      <span>{b.title || 'Sorular'}</span>
                      <small>{rangeOf(b.level === 1 ? b.all : b.entries)}</small>
                    </a>
                  </li>
                ))
              : showQuestions && (
                  <li>
                    <a href="#sorular"><span>Sorular</span><small>{rangeOf(entries)}</small></a>
                  </li>
                )}
            {o.mode === 'solution' && o.answersAt === 'end' && (
              <li><a href="#cozumler"><span>Çözümler</span><small>{entries.length} soru</small></a></li>
            )}
            {keyAtEnd && <li><a href="#cevap-anahtari"><span>Cevap anahtarı</span><small>{entries.length} soru</small></a></li>}
            {o.opticForm && <li><a href="#optik-form"><span>Optik form</span><small>A–E</small></a></li>}
          </ol>
        </nav>
      )}

      {showQuestions && (
        <div className={listClass} id="sorular">
          {level1.map((b1, gi) => {
            const subs = b1.subs;
            return (
              <React.Fragment key={b1.id}>
                {b1.title && (
                  <h2 className={`pd-group ${o.groupNewPage && gi > 0 ? 'is-break' : ''}`} id={b1.id}>
                    {b1.title} <span>{b1.all.length} soru</span>
                  </h2>
                )}
                {b1.entries.map((e) => <QuestionCard key={e.a} e={e} o={o} />)}
                {subs.map((b2) => (
                  <React.Fragment key={b2.id}>
                    <h3 className="pd-group is-sub" id={b2.id}>
                      {b2.title} <span>{b2.entries.length} soru</span>
                    </h3>
                    {b2.entries.map((e) => <QuestionCard key={e.a} e={e} o={o} />)}
                  </React.Fragment>
                ))}
                {groupTail(b1)}
              </React.Fragment>
            );
          })}
        </div>
      )}

      {o.mode === 'solution' && o.answersAt === 'end' && entries.length > 0 && (
        <section className="pd-section" id="cozumler">
          <h2 className="pd-section-h">Çözümler <span>{entries.length} soru</span></h2>
          {entries.map((e) => <SolutionEntry key={e.a} e={e} o={o} />)}
        </section>
      )}

      {keyAtEnd && entries.length > 0 && (
        <section className={showQuestions || o.answersAt === 'end' ? 'pd-section' : ''} id="cevap-anahtari">
          <h2 className="pd-section-h">Cevap anahtarı <span>{entries.filter((x) => x.q.answer).length} / {entries.length} sorunun cevabı belli</span></h2>
          <KeyGrid entries={entries} o={o} withIds={!keyPerGroup} />
        </section>
      )}

      {o.opticForm && entries.length > 0 && (
        <section className="pd-section" id="optik-form">
          <h2 className="pd-section-h">Optik form <span>Cevabını kurşun kalemle doldur</span></h2>
          <div className="pd-optic">
            {entries.map((e) => (
              <div key={e.a}>
                <small>{e.no}</small>
                {(e.q.options.length ? e.q.options.map((x) => x.key) : ['A', 'B', 'C', 'D', 'E']).map((k) => <span key={k}>{k}</span>)}
              </div>
            ))}
          </div>
        </section>
      )}
    </>
  );
};
