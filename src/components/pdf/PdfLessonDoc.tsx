/**
 * Öğren dersinin PDF'i: her adım LessonPlayer'daki işaretlemeyle (ls-head, ls-prose, ls-keys, ls-table,
 * ls-ix …) çizilir. Etkileşimler basılı hâle çevrilir: cevaplar açık, çalışma kâğıdı (boşluklu) ya da
 * cevaplar belge sonunda.
 */
import React from 'react';
import { Flag, Mic, Sparkles, Tag, Layers, Table2 } from 'lucide-react';
import type { InteractiveDeck } from '../learn/InteractiveDeckView';
import { buildSteps, buildSections, mdToHtml, inline, spotTone, stripEmoji, type LessonStep, type LessonSection } from '../learn/lesson/lessonModel';
import { KeyPoints, Infographic, Formula, IX_META, cleanWhy, safeHint } from '../learn/lesson/LessonBlocks';
import { Cover, Masthead, type CoverInfo } from './PdfParts';

export type AnswerMode = 'shown' | 'end' | 'hidden';
export const IX_TYPES = ['micro_quiz', 'cloze_masking', 'interactive_table', 'causal_chain', 'branching_logic', 'before_after_slider', 'active_recall'] as const;
export type IxType = (typeof IX_TYPES)[number];

export interface LessonDocOptions {
  narrative: boolean;
  keyPoints: boolean;
  tables: boolean;
  visuals: boolean;
  teacher: boolean;
  spots: boolean;
  tips: boolean;
  terms: boolean;
  cards: boolean;
  interactives: IxType[];
  answers: AnswerMode;
  optionNotes: boolean;
  stepPerPage: boolean;
  sectionTitles: boolean;
  toc: boolean;
  cover: boolean;
}

const Html: React.FC<{ html: string; as?: 'div' | 'span' | 'p'; className?: string }> = ({ html, as = 'span', className }) =>
  React.createElement(as, { className, dangerouslySetInnerHTML: { __html: html } });

/** Belge sonundaki cevap listesi için toplanan kayıt */
interface AnswerEntry { step: number; label: string; html: string }

const chainSteps = (e: any): [string, string][] =>
  (e.steps || []).map((x: any) => {
    const t = String(typeof x === 'string' ? x : x?.text || x?.label || '').replace(/^\d+[.)]\s*/, '');
    const k = t.indexOf(':');
    return k > 0 && k < 48 ? [t.slice(0, k), t.slice(k + 1).trim()] : ['', t];
  });

const clozeParts = (e: any) => {
  const s = String(e.sentence || '');
  const term = String(e.maskedTerm || '');
  const low = s.toLocaleLowerCase('tr-TR');
  const t = term.toLocaleLowerCase('tr-TR');
  const bi = t ? low.indexOf(`[${t}]`) : -1;
  const i = bi >= 0 ? bi : t ? low.indexOf(t) : -1;
  const len = bi >= 0 ? term.length + 2 : term.length;
  return { s, term, i, len, answer: i >= 0 ? s.slice(i, i + len).replace(/^\[|\]$/g, '') : term };
};

const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c] as string);

const typeOf = (e: any): string => (e.type === 'hidden_table' ? 'interactive_table' : e.type);
const selectedIx = (step: LessonStep, o: LessonDocOptions) => step.interactives.filter((e) => (o.interactives as string[]).includes(typeOf(e)));

/** "Cevaplar sonda" modunda belge sonuna yazılacak cevaplar (etkileşim sırasıyla). */
function stepAnswers(step: LessonStep, o: LessonDocOptions): AnswerEntry[] {
  const out: AnswerEntry[] = [];
  const add = (label: string, html: string) => html && out.push({ step: step.number, label, html });
  for (const e of selectedIx(step, o)) {
    const label = (IX_META[typeOf(e)] || [null, 'Alıştırma'])[1];
    if (e.type === 'micro_quiz' || e.type === 'branching_logic') {
      const isB = e.type === 'branching_logic';
      const opts = isB ? e.options || [] : e.microQuizOptions || e.options || [];
      const k = opts.findIndex((x: any) => x?.isCorrect);
      if (k < 0) continue;
      const r = opts[k];
      const why = cleanWhy(isB ? r.feedback : r.explanation);
      add(label, `<b>${esc(isB ? String.fromCharCode(65 + k) : r.key || String.fromCharCode(65 + k))})</b> ${inline(String(r.text ?? ''))}${o.optionNotes && why ? ` — ${inline(why)}` : ''}`);
    } else if (e.type === 'cloze_masking') add(label, `<b>${esc(clozeParts(e).answer)}</b>`);
    else if (typeOf(e) === 'interactive_table') {
      const headers: string[] = (e.tableHeaders?.length ? e.tableHeaders : e.headers) || e.table?.headers || [];
      const rows: any[][] = ((e.tableRows?.length ? e.tableRows : e.rows) || e.table?.rows || []).map((r: any) => (Array.isArray(r) ? r : r?.cells || []));
      const hidden = rows.flatMap((r) => r.map((c: any, ci: number) => (c && typeof c === 'object' && c.isMasked ? `${stripEmoji(headers[ci] || '').replace(/\*\*/g, '')}${headers[ci] ? ': ' : ''}${c.text}` : null))).filter(Boolean) as string[];
      add(label, hidden.map((h) => esc(h)).join(' · '));
    } else if (e.type === 'causal_chain') add(label, chainSteps(e).map(([a, b], i) => `${i + 1}. ${a ? `<b>${esc(a)}</b>: ` : ''}${inline(b)}`).join('<br>'));
    else if (e.type === 'active_recall') add(label, inline(e.answer || ''));
  }
  if (o.cards) step.cards.forEach((c) => add('Kart', `${esc(c.front)} → <b>${esc(c.back)}</b>`));
  return out;
}

/** Tek etkileşim, basılı hâli (cevaplar açık ya da boşluklu). */
const PrintIx: React.FC<{ e: any; o: LessonDocOptions }> = ({ e, o }) => {
  const show = o.answers === 'shown';
  const [Icon, label] = IX_META[e.type] || [Sparkles, 'Alıştırma'];
  let body: React.ReactNode = null;

  switch (e.type) {
    case 'micro_quiz':
    case 'branching_logic': {
      const isB = e.type === 'branching_logic';
      const opts = (isB ? e.options || [] : e.microQuizOptions || e.options || []).map((x: any, k: number) => ({
        key: isB ? String.fromCharCode(65 + k) : x.key || String.fromCharCode(65 + k),
        text: String(x.text ?? ''),
        ok: !!x.isCorrect,
        why: cleanWhy(isB ? x.feedback : x.explanation),
      }));
      body = (
        <div className="ls-ix-body">
          <Html as="p" className="ls-ix-q" html={inline(isB ? e.scenario || e.question || '' : e.question || e.sentence || '')} />
          <ul className="ls-opts">
            {opts.map((x: any) => {
              const tone = show ? (x.ok ? 'is-right' : 'is-idle') : '';
              const open = show && o.optionNotes && x.why;
              return (
                <li key={x.key} className={`ls-optcard ${tone} ${open ? 'is-open' : ''}`}>
                  <div className="ls-opt">
                    <span className="k">{x.key}</span>
                    <Html html={inline(x.text)} />
                  </div>
                  {open && (
                    <div className="ls-opt-panel">
                      <div>
                        <p>
                          <span className="ls-opt-verdict">{x.ok ? 'Neden doğru' : 'Neden yanlış'}</span>
                          <Html html={inline(x.why)} />
                        </p>
                      </div>
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      );
      break;
    }
    case 'cloze_masking': {
      const c = clozeParts(e);
      const blank = show ? <span className="ls-blank is-shown">{c.answer}</span> : <span className="pd-blank" />;
      const hint = safeHint(e.hint, c.term);
      body = (
        <div className="ls-ix-body">
          <p className="ls-cloze">
            {c.i >= 0 ? <>{c.s.slice(0, c.i)}{blank}{c.s.slice(c.i + c.len)}</> : <>{c.s.replace(/\[([^\]]+)\]/g, '$1')} {blank}</>}
          </p>
          {!show && hint && <span className="ls-hint">İpucu: {hint}</span>}
        </div>
      );
      break;
    }
    case 'interactive_table':
    case 'hidden_table': {
      const headers: string[] = (e.tableHeaders?.length ? e.tableHeaders : e.headers) || e.table?.headers || [];
      const rawRows = (e.tableRows?.length ? e.tableRows : e.rows) || e.table?.rows || [];
      const rows: any[][] = rawRows.map((r: any) => (Array.isArray(r) ? r : Array.isArray(r?.cells) ? r.cells : []));
      body = (
        <div className="ls-ix-body">
          <figure className="ls-table m-0">
            <figcaption><Table2 aria-hidden /><span className="min-w-0 flex-1">{e.tableTitle || e.title || 'Tablo'}</span></figcaption>
            <table>
              {headers.length > 0 && <thead><tr>{headers.map((h, i) => <th key={i}>{stripEmoji(h).replace(/\*\*/g, '')}</th>)}</tr></thead>}
              <tbody>
                {rows.map((r, ri) => (
                  <tr key={ri}>
                    {r.map((cell: any, ci: number) => {
                      const c = typeof cell === 'object' && cell ? cell : { text: String(cell ?? '') };
                      if (c.isMasked) {
                        return <td key={ci}>{show ? <span className="ls-mask is-shown">{c.text}</span> : <span className="pd-mask-blank" />}</td>;
                      }
                      return <td key={ci}><Html html={inline(String(c.text))} /></td>;
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </figure>
        </div>
      );
      break;
    }
    case 'causal_chain': {
      const steps = chainSteps(e);
      body = (
        <div className="ls-ix-body">
          {e.chainTitle && <p className="ls-ix-q">{e.chainTitle}</p>}
          <ol className="ls-chain">
            {steps.map(([a, b], i) => (
              <li key={i} className="is-on">
                <span className="n">{i + 1}</span>
                <span className="t">{a && <b>{a}</b>}{show || i === 0 ? <Html html={inline(b)} /> : <span className="pd-mask-blank" />}</span>
              </li>
            ))}
          </ol>
        </div>
      );
      break;
    }
    case 'before_after_slider': {
      const L: string[] = e.leftPoints || [];
      const R: string[] = e.rightPoints || [];
      body = (
        <div className="ls-ix-body">
          <div className="ls-vs" role="table">
            <div role="row" className="ls-vs-head">
              <button type="button">{e.leftTitle}</button>
              <button type="button">{e.rightTitle}</button>
            </div>
            {Array.from({ length: Math.max(L.length, R.length) }, (_, i) => (
              <div role="row" key={i}>
                <Html className="L" html={inline(L[i] || '')} />
                <Html className="R" html={inline(R[i] || '')} />
              </div>
            ))}
          </div>
        </div>
      );
      break;
    }
    case 'active_recall': {
      body = (
        <div className="ls-ix-body">
          <Html as="p" className="ls-ix-q" html={inline(e.question || e.title || '')} />
          {show ? <Html as="div" className="ls-recall-a" html={inline(e.answer || '')} /> : <div className="pd-lines" aria-hidden><i /><i /><i /></div>}
        </div>
      );
      break;
    }
    default:
      return null;
  }
  return (
    <section className="ls-ix" aria-label={label}>
      <header className="ls-ix-head">
        <Icon aria-hidden />
        <span className="ls-ix-label">{label}</span>
      </header>
      {body}
    </section>
  );
};

const Cards: React.FC<{ step: LessonStep; o: LessonDocOptions }> = ({ step, o }) => {
  return (
    <section className="ls-ix">
      <header className="ls-ix-head"><Layers aria-hidden /><span className="ls-ix-label">Akıl kartları · {step.cards.length}</span></header>
      <div className="ls-ix-body">
        <div className="pd-cards">
          {step.cards.map((c, i) => (
            <div key={c.id} className="pd-card">
              <div className="is-front">
                <small>{c.category || 'Kart'} · {i + 1}</small>
                <span className="q">{c.front}</span>
              </div>
              {o.answers === 'shown' ? (
                <div className="is-back"><small>Cevap</small><span className="q">{c.back}</span></div>
              ) : (
                <div className="is-blank" />
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

const Step: React.FC<{ step: LessonStep; total: number; o: LessonDocOptions }> = ({ step, total, o }) => {
  const showKeys = o.keyPoints && (step.bullets.length > 1 || ((!o.narrative || !step.narrative.trim()) && step.bullets.length > 0));
  const ixs = selectedIx(step, o);
  const infoItems = [
    ...(o.spots ? step.spots.map((s) => ({ tone: spotTone(s), icon: Flag, html: inline(s) })) : []),
    ...(o.tips && step.important ? [{ tone: 'bad', icon: Sparkles, html: `<b>Önemli nokta</b><br>${inline(step.important)}` }] : []),
    ...(o.tips && step.examTip ? [{ tone: 'warn', icon: Flag, html: `<b>Sınav ipucu</b><br>${inline(step.examTip)}` }] : []),
  ];
  return (
    <article className={`pd-step ${o.stepPerPage ? 'is-page' : ''}`} id={`adim-${step.number}`}>
      <header className="ls-head">
        <div className="ls-eyebrow-row">
          <span>Bölüm {step.section + 1}</span>
          <span className="dot" aria-hidden />
          <span>Adım {step.number} / {total}</span>
          {step.checkpoint > 0 && <span className="ls-tag is-accent">Tekrar {step.checkpoint}</span>}
          {step.badge && !step.checkpoint && <span className="ls-tag is-plain">{step.badge}</span>}
        </div>
        <h1 className="ls-title"><span>{step.title}</span></h1>
        {step.slide.subtitle && <p className="ls-sub">{step.slide.subtitle}</p>}
      </header>

      <div className="ls-content">
        {o.narrative && step.narrative.trim() && <Html as="div" className="ls-prose" html={mdToHtml(step.narrative)} />}
        {showKeys && <KeyPoints items={step.bullets} />}
        {o.tables && step.table && (
          <figure className="ls-table m-0">
            {step.table.title && <figcaption><Table2 aria-hidden /><span className="min-w-0 flex-1">{step.table.title}</span></figcaption>}
            <table>
              {(step.table.headers || []).length > 0 && <thead><tr>{step.table.headers.map((h, i) => <th key={i}>{stripEmoji(h).replace(/\*\*/g, '')}</th>)}</tr></thead>}
              <tbody>
                {step.table.rows.map((r, ri) => (
                  <tr key={ri}>{r.map((c: any, ci) => <td key={ci}><Html html={inline(String(typeof c === 'object' && c ? c.text : c ?? ''))} /></td>)}</tr>
                ))}
              </tbody>
            </table>
          </figure>
        )}
        {o.visuals && step.infographic && <Infographic data={step.infographic} />}
        {o.visuals && step.formula && <Formula data={step.formula} />}
        {o.teacher && step.teacher && (
          <figure className="ls-teacher m-0">
            <Mic aria-hidden />
            <div>
              <span className="ls-eyebrow">Hocanın vurgusu</span>
              {step.teacher.quote && <blockquote>“{step.teacher.quote}”</blockquote>}
              {step.teacher.note && <figcaption>{step.teacher.note}</figcaption>}
            </div>
          </figure>
        )}
      </div>

      {infoItems.length > 0 && (
        <div className="pd-box">
          <div className="ls-sec-h">Sınav spotu <span>{infoItems.length}</span></div>
          <ul className="ls-info">
            {infoItems.map((it, i) => (
              <li key={i}>
                <span className={`ico is-${it.tone}`}><it.icon aria-hidden /></span>
                <Html html={it.html} />
              </li>
            ))}
          </ul>
        </div>
      )}

      {o.terms && step.terms.length > 0 && (
        <div className="pd-box">
          <div className="ls-sec-h">Terimler <span>{step.terms.length}</span></div>
          <ul className="ls-info pd-terms">
            {step.terms.map((t, i) => (
              <li key={i}>
                <span className="ico is-accent"><Tag aria-hidden /></span>
                <span><b>{t.term}</b><br />{t.explanation}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {(ixs.length > 0 || (o.cards && step.cards.length > 0)) && (
        <section className="ls-practice">
          <div className="ls-sec-h">Pekiştir <span>{ixs.length + (o.cards && step.cards.length ? 1 : 0)}</span></div>
          <div className="pd-ix-grid">
            {ixs.map((e, i) => <PrintIx key={i} e={e} o={o} />)}
            {o.cards && step.cards.length > 0 && <Cards step={step} o={o} />}
          </div>
        </section>
      )}
    </article>
  );
};

export interface LessonDocProps {
  deck: InteractiveDeck;
  /** Basılacak adım numaraları (slideNumber); boşsa hepsi */
  slideNumbers: number[];
  options: LessonDocOptions;
  cover: CoverInfo;
}

export const LessonDoc: React.FC<LessonDocProps> = ({ deck, slideNumbers, options: o, cover }) => {
  const steps = buildSteps(deck);
  const sections: LessonSection[] = buildSections(steps);
  const picked = new Set(slideNumbers);
  const chosen = steps.filter((s) => !picked.size || picked.has(s.number));
  const answers: AnswerEntry[] = o.answers === 'end' ? chosen.flatMap((st) => stepAnswers(st, o)) : [];

  // Adımlar bölüm başlıklarıyla birlikte sırayla basılır
  const blocks: React.ReactNode[] = [];
  let lastSection = -1;
  chosen.forEach((st) => {
    if (o.sectionTitles && st.section !== lastSection) {
      const sec = sections[st.section];
      const count = sec ? sec.steps.filter((i) => picked.size === 0 || picked.has(steps[i].number)).length : 0;
      blocks.push(
        <div key={`sec-${st.section}`} className="pd-sec-title">
          <small>Bölüm {st.section + 1}</small>
          <b>{sec?.name || st.topic}</b>
          <span>{count} adım</span>
        </div>
      );
      lastSection = st.section;
    }
    blocks.push(<Step key={st.number} step={st} total={steps.length} o={o} />);
  });

  return (
    <>
      {o.cover ? <Cover info={cover} /> : <Masthead info={cover} />}
      {o.toc && chosen.length > 1 && (
        <section className="pd-box" style={{ marginBottom: 22 }}>
          <div className="ls-sec-h">İçindekiler <span>{chosen.length}</span></div>
          <ol className="pd-toc">
            {chosen.map((s) => (
              <li key={s.number}>
                <small>{s.number}</small>
                <span>{s.title}</span>
              </li>
            ))}
          </ol>
        </section>
      )}
      {blocks}
      {o.answers === 'end' && answers.length > 0 && (
        <section className="pd-section">
          <h2 className="pd-section-h">Cevaplar <span>{answers.length} etkinlik</span></h2>
          {answers.map((a, i) => (
            <div key={i} className="pd-ans">
              <small>Adım {a.step}</small>
              <span><span className="ls-tag is-accent">{a.label}</span><Html html={a.html} /></span>
            </div>
          ))}
        </section>
      )}
    </>
  );
};

