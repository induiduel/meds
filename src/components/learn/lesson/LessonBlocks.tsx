import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  Archive, BookOpenText, Brain, Check, ChevronDown, ChevronLeft, ChevronRight, X, Eye, FileText, Flag, GitBranch, HelpCircle, Info,
  Layers, Link2, Mic, Quote, Sparkles, SplitSquareHorizontal, Table2, Tag, Target,
  ShieldAlert, Zap, Scale, Columns, Award, RotateCcw,
} from 'lucide-react';
import type { LessonCard, LessonQuestion, LessonStep, PracticeItem, DeckKazanim } from './lessonModel';
import { inline, mdToHtml, spotTone, stripEmoji } from './lessonModel';
import type { FeedbackTarget } from './lessonFeedback';
import { FeedbackFlag } from './LessonFeedbackUI';

/* ---------------------------------------------------------------------------
 * Anlatım: markdown + metindeki tıbbi terimler (ilk geçtiği yer altı noktalı; dokununca tanım)
 * ------------------------------------------------------------------------- */
const tipEl = (): HTMLDivElement => {
  let el = document.getElementById('ls-term-tip') as HTMLDivElement | null;
  if (!el) {
    el = document.createElement('div');
    el.id = 'ls-term-tip';
    el.className = 'ls-tip';
    el.setAttribute('role', 'tooltip');
    document.body.appendChild(el);
  }
  return el;
};
export const hideTermTip = () => document.getElementById('ls-term-tip')?.classList.remove('is-on');

const wireTerms = (root: HTMLElement, terms: LessonStep['terms']) => {
  if (!terms.length) return;
  const nodes: Text[] = [];
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) nodes.push(n as Text);
  for (const t of terms) {
    const word = ((t as any).match || t.term).split(/[(/]/)[0].trim();
    if (word.length < 4) continue;
    const re = new RegExp(`(^|[^\\p{L}])(${word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'iu');
    for (const n of nodes) {
      if (!n.parentNode || (n.parentElement && n.parentElement.closest('.ls-term, mark, .ls-tag, th'))) continue;
      const m = n.nodeValue?.match(re);
      if (!m || m.index == null) continue;
      const start = m.index + m[1].length;
      let end = start + m[2].length;
      while (end < n.nodeValue!.length && /\p{L}/u.test(n.nodeValue![end])) end++;
      const mid = n.splitText(start);
      const after = mid.splitText(end - start);
      const sp = document.createElement('span');
      sp.className = 'ls-term';
      sp.tabIndex = 0;
      sp.dataset.t = t.term;
      sp.dataset.d = t.explanation;
      sp.textContent = mid.nodeValue;
      mid.replaceWith(sp);
      nodes.splice(nodes.indexOf(n) + 1, 0, after);
      break;
    }
  }
  const show = (el: HTMLElement) => {
    const tip = tipEl();
    tip.innerHTML = '';
    const b = document.createElement('b');
    b.textContent = el.dataset.t || '';
    tip.append(b, document.createTextNode(el.dataset.d || ''));
    tip.classList.add('is-on');
    const r = el.getBoundingClientRect();
    const tw = tip.offsetWidth;
    const th = tip.offsetHeight;
    tip.style.left = `${Math.max(8, Math.min(window.innerWidth - tw - 8, r.left + r.width / 2 - tw / 2))}px`;
    tip.style.top = `${r.top - th - 8 < 8 ? r.bottom + 8 : r.top - th - 8}px`;
  };
  root.querySelectorAll<HTMLElement>('.ls-term').forEach((el) => {
    el.addEventListener('mouseenter', () => show(el));
    el.addEventListener('focus', () => show(el));
    el.addEventListener('click', () => show(el));
    el.addEventListener('mouseleave', hideTermTip);
    el.addEventListener('blur', hideTermTip);
  });
};

export const Prose: React.FC<{ text: string; terms?: LessonStep['terms']; className?: string }> = ({ text, terms = [], className = '' }) => {
  const ref = useRef<HTMLDivElement>(null);
  const html = useMemo(() => mdToHtml(text), [text]);
  useEffect(() => {
    if (ref.current) wireTerms(ref.current, terms);
    return hideTermTip;
  }, [html, terms]);
  return <div ref={ref} className={`ls-prose ${className}`} dangerouslySetInnerHTML={{ __html: html }} />;
};

const Inline: React.FC<{ text: string; as?: 'span' | 'p' | 'div'; className?: string }> = ({ text, as = 'span', className }) =>
  React.createElement(as, { className, dangerouslySetInnerHTML: { __html: inline(text) } });

/* ---------------------------------------------------------------------------
 * Tablo: ekrana sığar (sabit düzen, kelime kırma); dar ekranda satırlar karta dönüşür
 * ------------------------------------------------------------------------- */
const NUM_RE = /^[~<>≈≥≤]?\s*[\d.,%\s\-x^×/]+\s*(Mb|Gb|bp|kb|gen|mm|cm|mg|g|kg|ml|L|saat|gün|yıl|hafta)?\.?$/i;
type Cell = string | { text: string; isMasked?: boolean; hint?: string };
export const LessonTable: React.FC<{ title?: string; headers: string[]; rows: Cell[][]; masked?: boolean; onAllRevealed?: () => void; target?: FeedbackTarget }> = ({
  title, headers, rows, masked = false, onAllRevealed, target,
}) => {
  const [shown, setShown] = useState<Set<string>>(new Set());
  const total = masked ? rows.reduce((a, r) => a + r.filter((c) => typeof c === 'object' && c.isMasked).length, 0) : 0;
  useEffect(() => {
    if (masked && total && shown.size >= total) onAllRevealed?.();
  }, [shown, total, masked]); // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <figure className="ls-table m-0" data-fb-key={target?.key}>
      {(title || masked || target) && (
        <figcaption>
          <Table2 aria-hidden />
          <span className="min-w-0 flex-1">{title || 'Tablo'}</span>
          {masked && total > 0 && (
            <span className="ls-tag is-accent">
              {shown.size}/{total} açıldı
            </span>
          )}
          {target && <FeedbackFlag target={target} />}
        </figcaption>
      )}
      <table>
        {headers.length > 0 && (
          <thead>
            <tr>{headers.map((h, i) => <th key={i}>{stripEmoji(h).replace(/\*\*/g, '')}</th>)}</tr>
          </thead>
        )}
        <tbody>
          {rows.map((r, ri) => (
            <tr key={ri}>
              {r.map((c, ci) => {
                const cell = typeof c === 'object' && c ? c : { text: String(c ?? '') };
                const id = `${ri}:${ci}`;
                const hidden = masked && cell.isMasked && !shown.has(id);
                const hint = masked && cell.isMasked ? safeHint(cell.hint, String(cell.text)) : '';
                return (
                  <td key={ci} data-h={stripEmoji(headers[ci] || '').replace(/\*\*/g, '')} className={!cell.isMasked && NUM_RE.test(String(cell.text).trim()) ? 'is-num' : ''}>
                    {masked && cell.isMasked ? (
                      <button
                        type="button"
                        className={`ls-mask ${hidden ? '' : 'is-shown'}`}
                        disabled={!hidden}
                        onClick={() => setShown((s) => new Set(s).add(id))}
                        aria-label={hidden ? `Gizli hücreyi aç${hint ? `, ipucu: ${hint}` : ''}` : undefined}
                      >
                        {hidden ? <><Eye aria-hidden /> {hint || 'Göster'}</> : cell.text}
                      </button>
                    ) : (
                      <Inline text={String(cell.text)} />
                    )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </figure>
  );
};

/* ---------------------------------------------------------------------------
 * Anahtar maddeler, infografik, formül, hoca notu
 * ------------------------------------------------------------------------- */
export const KeyPoints: React.FC<{ items: LessonStep['bullets'] }> = ({ items }) => (
  <ul className="ls-keys">
    {items.map((b, i) => (
      <li key={i} className={b.isKey ? 'is-key' : ''}>
        {b.title && <Inline text={b.title} className="ls-keys-t" />}
        {b.desc && <Inline text={b.desc} as="p" />}
      </li>
    ))}
  </ul>
);

const TONE_OF: Record<string, string> = { red: 'bad', rose: 'bad', amber: 'warn', orange: 'warn', green: 'ok', emerald: 'ok', teal: 'ok', blue: 'accent', indigo: 'accent', violet: 'accent' };
export const Infographic: React.FC<{ data: NonNullable<LessonStep['infographic']> }> = ({ data }) =>
  data.type === 'process' ? (
    <ol className="ls-chain is-static">
      {data.items.map((it, i) => (
        <li key={i} className="is-on">
          <span className="n">{i + 1}</span>
          <span className="t"><b>{it.label}</b>{it.value && <> · {it.value}</>}{it.detail && <small>{it.detail}</small>}</span>
        </li>
      ))}
    </ol>
  ) : (
    <div className="ls-metrics">
      {data.items.map((it, i) => (
        <div key={i} className={`is-${TONE_OF[(it.color || '').toLowerCase()] || 'accent'}`}>
          <span className="v">{it.value}</span>
          <span className="l">{it.label}</span>
          {it.detail && <span className="d">{it.detail}</span>}
        </div>
      ))}
    </div>
  );

export const Formula: React.FC<{ data: NonNullable<LessonStep['formula']> }> = ({ data }) => (
  <div className="ls-formula">
    <span className="ls-eyebrow">{data.title}</span>
    <code>{data.formula}</code>
    {data.explanation && <p>{data.explanation}</p>}
  </div>
);

export const TeacherNote: React.FC<{ step: LessonStep }> = ({ step }) =>
  step.teacher ? (
    <figure className="ls-teacher m-0">
      <Mic aria-hidden />
      <div>
        <span className="ls-eyebrow">Hocanın vurgusu</span>
        {step.teacher.quote && <blockquote>“{step.teacher.quote}”</blockquote>}
        {step.teacher.note && <figcaption>{step.teacher.note}</figcaption>}
      </div>
    </figure>
  ) : null;

/* ---------------------------------------------------------------------------
 * Etkileşimler
 * ------------------------------------------------------------------------- */
export const IX_META: Record<string, [React.ElementType, string]> = {
  micro_quiz: [HelpCircle, 'Mini soru'],
  interactive_table: [Table2, 'Gizli tablo'],
  cloze_masking: [Eye, 'Boşluk doldur'],
  causal_chain: [Link2, 'Mekanizma zinciri'],
  branching_logic: [GitBranch, 'Klinik karar'],
  before_after_slider: [SplitSquareHorizontal, 'Karşılaştır'],
  active_recall: [Brain, 'Aktif hatırlama'],
  spot_the_lie: [ShieldAlert, 'Tuzak avı'],
  swipe_matching: [Zap, 'Hızlı eşleme'],
  feature_bidding: [Scale, 'Puan bahsi'],
  venn_grid: [Columns, 'Çapraz tablo'],
  cards: [Layers, 'Çevir kartları'],
  question: [Archive, 'Soru'],
};
export const practiceMeta = (p: PracticeItem): [React.ElementType, string] =>
  p.kind === 'cards' ? IX_META.cards : p.kind === 'question' ? [Archive, p.q.practice ? 'Çalışma sorusu' : 'Çıkmış soru'] : IX_META[p.data.type] || [Sparkles, 'Alıştırma'];

interface OptLike { key: string; text: string; ok: boolean; why?: string }
/**
 * Şıklı soru: ilk seçim cevabı belirler. Sonra her şıkka dokunarak açıklaması kartın içinde açılır,
 * aynı şıkka tekrar dokununca kapanır.
 */
/**
 * Şık açıklamasının başındaki "Doğrudur;", "Yanlıştır;", "Doğru!", "Yanlış.", "A seçeneği yanlıştır:" gibi
 * hüküm ve şık etiketlerini temizler; geriye kalan açıklama cümlesini ilk harfi büyük olacak şekilde döndürür.
 * "dur;", "tır;" gibi eksik kesilme hatalarını ve izole ek kalıntılarını tamamen engeller.
 */
export const cleanWhy = (t?: string): string => {
  if (!t) return '';
  let s = String(t).trim();

  // Tekrarlayan temizlik döngüsü (iç içe veya ardışık kalıplar için)
  let prev = '';
  while (prev !== s) {
    prev = s;
    s = s
      .replace(
        /^(?:(?:\*+)?(?:doğru|yanlış|hatalı)\s+(?:cevap|yanıt|seçenek)(?:\s+[A-Za-z](?:['’][a-z]+)?)?(?:\*+)?|(?:\*+)?(?:\(?[A-Za-z]\)?)?\s*(?:seçeneği|şıkkı|seçenek|şık)?\s*(?:doğrudur|yanlıştır|hatalıdır|doğru|yanlış|hatalı)(?:\s*\([^)]*\))?(?:\*+)?|(?:\*+)?(?:doğrudur|yanlıştır|hatalıdır|doğru|yanlış|hatalı\s+yaklaşım|mükemmel\s+klinik\s+karar|kritik\s+hata)(?:\s*\([^)]*\))?(?:\*+)?)[!.:;\s-]*/iu,
        ''
      )
      .replace(
        /^(?:(?:\*+)?(?:doğru|yanlış|hatalı)\s+(?:bir\s+)?(?:spot\s+)?(?:bilgidir|ifadedir|açıklamadır|yargıdır|yaklaşımdır|tespittir|tanımdır|kuraldır|durumdur|seçenektir)(?:\*+)?|(?:\*+)?(?:bir\s+)?(?:spot\s+)?(?:bilgidir|ifadedir|açıklamadır|yargıdır|yaklaşımdır|tespittir|tanımdır|kuraldır|durumdur)(?:\*+)?)[!.:;\s-]*/iu,
        ''
      )
      .replace(/^(?:dur|dır|dir|dür|tır|tir|tur|tür)[!.:;\s-]+/iu, '')
      .trim();
  }

  // İlk harfi Türkçe kurallarına uygun büyüt
  if (s.length > 0) {
    s = s.charAt(0).toLocaleUpperCase('tr-TR') + s.slice(1);
  }

  return s;
};
const OptionList: React.FC<{ question: string; options: OptLike[]; onDone?: () => void; extraWhy?: string; context?: string }> = ({ question, options, onDone, extraWhy, context }) => {
  const [first, setFirst] = useState<string | null>(null);
  const [opened, setOpened] = useState<Set<string>>(new Set());
  const right = options.find((o) => o.ok);
  const firstOpt = options.find((o) => o.key === first);
  const anyWhy = options.some((o) => o.why);
  const pick = (o: OptLike) => {
    if (!first) {
      setFirst(o.key);
      onDone?.();
      setOpened(new Set(o.why ? [o.key] : []));
      return;
    }
    setOpened((s) => {
      const n = new Set(s);
      n.has(o.key) ? n.delete(o.key) : n.add(o.key);
      return n;
    });
  };
  return (
    <div className="ls-ix-body">
      {context && <Inline text={context} as="p" className="ls-ix-case" />}
      <Inline text={question} as="p" className="ls-ix-q" />
      <ul className="ls-opts">
        {options.map((o) => {
          const isOpen = !!first && opened.has(o.key);
          const tone = !first ? '' : o.ok ? 'is-right' : o.key === first ? 'is-wrong' : 'is-idle';
          const why = cleanWhy(o.why);
          return (
            <li key={o.key} className={`ls-optcard ${tone} ${isOpen ? 'is-open' : ''} ${o.key === first ? 'is-first' : ''}`}>
              <button type="button" className="ls-opt" aria-expanded={first && why ? isOpen : undefined} onClick={() => pick(o)}>
                <span className="k">{tone === 'is-right' ? <Check aria-hidden /> : tone === 'is-wrong' ? <X aria-hidden /> : o.key}</span>
                <Inline text={o.text} />
                {first && why && <ChevronDown className="ls-opt-chev" aria-hidden />}
              </button>
              {first && why && (
                <div className="ls-opt-panel" aria-hidden={!isOpen}>
                  <div>
                    <p>
                      <span className="ls-opt-verdict">{o.ok ? 'Neden doğru' : 'Neden yanlış'}</span>
                      <Inline text={why} />
                    </p>
                  </div>
                </div>
              )}
            </li>
          );
        })}
      </ul>
      {firstOpt && (
        <p className={`ls-fb ${firstOpt.ok ? 'is-ok' : 'is-bad'}`} role="status">
          <b>{firstOpt.ok ? 'Doğru.' : right ? `Yanlış · doğru cevap ${right.key}.` : 'Yanlış.'}</b>
          {anyWhy && <span className="ls-fb-hint"> Şıklara dokunarak açıklamalarını aç, tekrar dokunarak kapat.</span>}
        </p>
      )}
      {firstOpt && extraWhy && (
        <section className="ls-expl" aria-label="Açıklama">
          <span className="ls-expl-h"><BookOpenText aria-hidden /> Açıklama</span>
          <Prose text={extraWhy} className="is-sm" />
        </section>
      )}
    </div>
  );
};

/**
 * Çalışma sorularında açıklama çoğu zaman tek metindir: "Doğru cevap B'dir: …", "A seçeneği yanlıştır: …".
 * Şık satırları ilgili şıkka dağıtılır; geriye kalan genel metin "Açıklama" panelinde gösterilir.
 */
export const splitExplanation = (text: string | undefined, keys: string[]): { perOption: Record<string, string>; rest: string } => {
  const perOption: Record<string, string> = {};
  const rest: string[] = [];
  const ks = keys.join('');
  const optRe = new RegExp(`^\\s*(?:\\*\\*)?\\(?([${ks}])\\)?\\s*(?:seçeneği|şıkkı|şık|\\))\\s*(?:\\*\\*)?\\s*(?:doğrudur|doğru|yanlıştır|yanlış|hatalıdır)?\\s*(?:\\*\\*)?\\s*[:.–-]\\s*(.+)$`, 'i');
  const rightRe = new RegExp(`^\\s*(?:\\*\\*)?doğru\\s+(?:cevap|yanıt|seçenek)\\s*(?:\\*\\*)?\\s*([${ks}])\\S*\\s*(?:\\*\\*)?\\s*[:.–-]\\s*(.+)$`, 'i');
  String(text || '')
    .split(/\n+/)
    .forEach((line) => {
      const m = line.match(rightRe) || line.match(optRe);
      if (m && !perOption[m[1].toUpperCase()]) perOption[m[1].toUpperCase()] = m[2].replace(/^\*+\s*/, '').trim();
      else if (line.trim()) rest.push(line);
    });
  return { perOption, rest: rest.join('\n').trim() };
};

/** Gizli hücre / boşluk ipucu cevabın kendisini (ya da bir parçasını) içeriyorsa gösterilmez. */
const fold = (t: string) => t.toLocaleLowerCase('tr-TR').normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
export const safeHint = (hint: string | undefined, answer: string): string => {
  if (!hint) return '';
  const h = fold(hint);
  const words = (fold(answer).match(/[\p{L}\d][\p{L}\d.,%-]*/gu) || []).filter((w) => w.length >= 3 || /\d/.test(w));
  return words.some((w) => h.includes(w.length > 5 ? w.slice(0, 5) : w)) ? '' : hint;
};

const Cloze: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const [open, setOpen] = useState(false);
  const s = String(e.sentence || '');
  const term = String(e.maskedTerm || '');
  const low = s.toLocaleLowerCase('tr-TR');
  const t = term.toLocaleLowerCase('tr-TR');
  // Bazı cümlelerde gizlenecek kelime köşeli parantezle işaretli ("[CGG]"): parantezler de boşluğa dahil
  const bi = t ? low.indexOf(`[${t}]`) : -1;
  const i = bi >= 0 ? bi : t ? low.indexOf(t) : -1;
  const len = bi >= 0 ? term.length + 2 : term.length;
  const blank = (
    <button
      type="button"
      className={`ls-blank ${open ? 'is-shown' : ''}`}
      onClick={() => {
        setOpen(true);
        onDone?.();
      }}
      disabled={open}
      aria-label={open ? undefined : 'Boşluğu göster'}
    >
      {open ? (i >= 0 ? s.slice(i, i + len).replace(/^\[|\]$/g, '') : term) : '?'}
    </button>
  );
  return (
    <div className="ls-ix-body">
      <p className="ls-cloze">
        {i >= 0 ? <>{s.slice(0, i)}{blank}{s.slice(i + len)}</> : <>{s.replace(/\[([^\]]+)\]/g, '$1')} {blank}</>}
      </p>
      {!open && safeHint(e.hint, term) && <span className="ls-hint"><Info aria-hidden /> İpucu: {safeHint(e.hint, term)}</span>}
    </div>
  );
};

const Chain: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const steps: [string, string][] = (e.steps || []).map((x: any) => {
    const t = String(typeof x === 'string' ? x : x?.text || x?.label || '').replace(/^\d+[.)]\s*/, '');
    const k = t.indexOf(':');
    return k > 0 && k < 48 ? [t.slice(0, k), t.slice(k + 1).trim()] : ['', t];
  });
  const [n, setN] = useState(1);
  return (
    <div className="ls-ix-body">
      {e.chainTitle && <p className="ls-ix-q">{e.chainTitle}</p>}
      <ol className="ls-chain">
        {steps.map(([a, b], i) => (
          <li key={i} className={i < n ? 'is-on' : ''}>
            <span className="n">{i + 1}</span>
            <span className="t">{a && <b>{a}</b>}<Inline text={b} /></span>
          </li>
        ))}
      </ol>
      <button
        type="button"
        className="ls-btn is-primary self-start"
        disabled={n >= steps.length}
        onClick={() => {
          const next = n + 1;
          setN(next);
          if (next >= steps.length) onDone?.();
        }}
      >
        {n >= steps.length ? <><Check aria-hidden /> Zincir tamam</> : <>Sonraki basamak <ChevronRight aria-hidden /></>}
      </button>
    </div>
  );
};

const Compare: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const [side, setSide] = useState<'L' | 'R' | null>(null);
  const L: string[] = e.leftPoints || [];
  const R: string[] = e.rightPoints || [];
  const rows = Math.max(L.length, R.length);
  const pick = (s: 'L' | 'R') => {
    setSide((v) => (v === s ? null : s));
    onDone?.();
  };
  return (
    <div className="ls-ix-body">
      <div className={`ls-vs ${side ? `is-${side}` : ''}`} role="table">
        <div role="row" className="ls-vs-head">
          <button type="button" role="columnheader" onClick={() => pick('L')} aria-pressed={side === 'L'}>{e.leftTitle}</button>
          <button type="button" role="columnheader" onClick={() => pick('R')} aria-pressed={side === 'R'}>{e.rightTitle}</button>
        </div>
        {Array.from({ length: rows }, (_, i) => (
          <div role="row" key={i}>
            <Inline text={L[i] || ''} className="L" />
            <Inline text={R[i] || ''} className="R" />
          </div>
        ))}
      </div>
      <span className="ls-hint"><SplitSquareHorizontal aria-hidden /> Bir sütun başlığına dokununca o taraf öne çıkar; satırlar karşılıklı eşleşir.</span>
    </div>
  );
};

const Recall: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const [open, setOpen] = useState(false);
  const [rate, setRate] = useState<string | null>(null);
  return (
    <div className="ls-ix-body">
      <Inline text={e.question || e.title || ''} as="p" className="ls-ix-q" />
      {!open ? (
        <button type="button" className="ls-btn is-primary self-start" onClick={() => setOpen(true)}>
          <Eye aria-hidden /> Cevabı göster
        </button>
      ) : (
        <>
          <Inline text={e.answer || ''} as="div" className="ls-recall-a" />
          <div className="ls-rate" role="group" aria-label="Ne kadar hatırladın?">
            <span className="ls-hint">Ne kadar hatırladın?</span>
            {['Hatırlamadım', 'Kısmen', 'Tam'].map((r) => (
              <button
                key={r}
                type="button"
                aria-pressed={rate === r}
                className={`ls-btn is-sm ${rate === r ? 'is-on' : ''}`}
                onClick={() => {
                  setRate(r);
                  onDone?.();
                }}
              >
                {r}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

/* ---------------------------------------------------------------------------
 * Karşılaştırmalı modeller: tuzak avı, hızlı eşleme, puan bahsi, çapraz tablo.
 * Ortak ilke: uzun etiketler kesilmez, sarar; renk yalnız sonucu (doğru/yanlış) anlatır;
 * hareket yalnız durum değişimini gösterir (seçim, karar, ilerleme).
 * ------------------------------------------------------------------------- */

/** Veri açıklamalarının başındaki "Tuzak / Yalan!", "Doğru." gibi hükümleri ayıklar (arayüz hükmü zaten gösterir). */
const cleanVerdict = (t?: string): string =>
  cleanWhy(String(t || '').replace(/^\s*(?:tuzak|yalan)(?:\s*\/\s*(?:tuzak|yalan))?\s*[!.:]*\s*/iu, ''));

/** İki kutuplu modellerde kutbun kısa harfi ve tam adı */
const Pole: React.FC<{ k: 'A' | 'B'; label: string }> = ({ k, label }) => (
  <span className={`ls-pole is-${k.toLowerCase()}`}><b>{k}</b><span>{label}</span></span>
);

/** İlerleme şeridi: her parça bir tur/kart; sonucu renkle gösterir */
const Pips: React.FC<{ total: number; at: number; results?: boolean[]; label: string }> = ({ total, at, results = [], label }) => (
  <span className="ls-pips" role="progressbar" aria-label={label} aria-valuemin={0} aria-valuemax={total} aria-valuenow={Math.min(at, total)}>
    {Array.from({ length: total }, (_, i) => (
      <i key={i} className={i < results.length ? (results[i] ? 'is-ok' : 'is-bad') : i === at ? 'is-on' : ''} />
    ))}
  </span>
);

export const SpotTheLie: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const items: any[] = Array.isArray(e.items) ? e.items : [];
  const topic = e.topic || e.question || 'Hangisi yanıltıcı?';
  const lieIdx = items.findIndex((it) => !!(it.isLie || it.isTrap));
  const [picked, setPicked] = useState<number | null>(null);
  const [open, setOpen] = useState<Set<number>>(new Set());

  const pick = (i: number) => {
    if (picked === null) {
      setPicked(i);
      setOpen(new Set([i, lieIdx].filter((x) => x >= 0)));
      onDone?.();
      return;
    }
    setOpen((s) => {
      const n = new Set(s);
      n.has(i) ? n.delete(i) : n.add(i);
      return n;
    });
  };
  const caught = picked !== null && picked === lieIdx;

  return (
    <div className="ls-ix-body">
      <Inline text={topic} as="p" className="ls-ix-q" />
      {picked === null && (
        <span className="ls-hint"><ShieldAlert aria-hidden /> {items.length} önermeden biri yanlış. Onu bul.</span>
      )}
      <ol className={`ls-stl ${picked !== null ? 'is-decided' : ''}`}>
        {items.map((it, i) => {
          const isLie = i === lieIdx;
          const tone = picked === null ? '' : isLie ? 'is-lie' : i === picked ? 'is-miss' : 'is-fact';
          const why = cleanVerdict(it.explanation);
          const isOpen = picked !== null && open.has(i) && !!why;
          return (
            <li key={i} className={`ls-stl-item ${tone} ${isOpen ? 'is-open' : ''}`} style={{ '--i': i } as React.CSSProperties}>
              <button type="button" className="ls-stl-btn" onClick={() => pick(i)} aria-expanded={picked !== null && why ? isOpen : undefined}>
                <span className="ls-stl-badge" aria-hidden>
                  {picked === null ? String.fromCharCode(65 + i) : isLie ? <ShieldAlert /> : i === picked ? <X /> : <Check />}
                </span>
                <Inline text={it.text || ''} className="ls-stl-text" />
                {picked !== null && why && <ChevronDown className="ls-opt-chev" aria-hidden />}
              </button>
              {picked !== null && why && (
                <div className="ls-fold" aria-hidden={!isOpen}>
                  <div>
                    <p className="ls-stl-why">
                      <span className={`ls-verdict ${isLie ? 'is-warn' : 'is-ok'}`}>{isLie ? 'Tuzak' : 'Doğru bilgi'}</span>
                      <Inline text={why} />
                    </p>
                  </div>
                </div>
              )}
            </li>
          );
        })}
      </ol>
      {picked !== null && (
        <p className={`ls-fb ${caught ? 'is-ok' : 'is-bad'}`} role="status">
          <b>{caught ? 'Tuzağı yakaladın.' : `Bu önerme doğru; tuzak ${String.fromCharCode(65 + lieIdx)}.`}</b>
          <span className="ls-fb-hint"> Diğer gerekçeler için önermelere dokun.</span>
        </p>
      )}
    </div>
  );
};

type Side = 'left' | 'right';
export const SwipeMatching: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const cards: any[] = Array.isArray(e.cards) ? e.cards : [];
  const labelOf = (c: any, d: string) => (typeof c === 'object' && c ? c.label || c.name || d : String(c || d));
  const L = labelOf(e.leftCategory, 'Sol');
  const R = labelOf(e.rightCategory, 'Sağ');
  const sideOf = (c: any): Side | null => {
    const t = String(c?.category || c?.correctCategory || '').toLocaleLowerCase('tr-TR');
    if (t === 'left' || t === 'l' || t === L.toLocaleLowerCase('tr-TR')) return 'left';
    if (t === 'right' || t === 'r' || t === R.toLocaleLowerCase('tr-TR')) return 'right';
    return null;
  };

  const [idx, setIdx] = useState(0);
  const [log, setLog] = useState<Array<{ card: any; chosen: Side; ok: boolean }>>([]);
  const [dx, setDx] = useState(0);
  const [drag, setDrag] = useState(false);
  const [verdict, setVerdict] = useState<{ dir: Side; ok: boolean } | null>(null);
  const [fly, setFly] = useState<Side | null>(null);
  const startX = useRef(0);
  const timers = useRef<number[]>([]);
  useEffect(() => () => timers.current.forEach((t) => window.clearTimeout(t)), []);

  const done = idx >= cards.length;
  const card = done ? null : cards[idx];

  const decide = (dir: Side) => {
    if (!card || verdict) return;
    const ok = sideOf(card) === dir;
    setVerdict({ dir, ok });
    setDx(0);
    // Önce karar kartın üstünde görünür, sonra kart seçilen yöne uçar
    timers.current.push(
      window.setTimeout(() => setFly(dir), 520),
      window.setTimeout(() => {
        setLog((l) => [...l, { card, chosen: dir, ok }]);
        setVerdict(null);
        setFly(null);
        setIdx((i) => {
          if (i + 1 >= cards.length) onDone?.();
          return i + 1;
        });
      }, 800),
    );
  };

  const onDown = (ev: React.PointerEvent<HTMLDivElement>) => {
    if (verdict) return;
    ev.currentTarget.setPointerCapture(ev.pointerId);
    startX.current = ev.clientX;
    setDrag(true);
  };
  const onMove = (ev: React.PointerEvent<HTMLDivElement>) => {
    if (drag) setDx(ev.clientX - startX.current);
  };
  const onUp = () => {
    if (!drag) return;
    setDrag(false);
    if (dx > 72) decide('right');
    else if (dx < -72) decide('left');
    else setDx(0);
  };
  const onKey = (ev: React.KeyboardEvent) => {
    if (ev.key === 'ArrowLeft') { ev.preventDefault(); decide('left'); }
    if (ev.key === 'ArrowRight') { ev.preventDefault(); decide('right'); }
  };

  const correct = log.filter((h) => h.ok).length;
  const lean = Math.max(-1, Math.min(1, dx / 120));

  if (done) {
    return (
      <div className="ls-ix-body">
        <div className="ls-score">
          <b>{correct}<small>/{cards.length}</small></b>
          <span>{correct === cards.length ? 'Hepsini doğru ayırdın.' : 'Yanlış eşlediklerinin gerekçesine bak.'}</span>
        </div>
        <ul className="ls-reslist">
          {log.map((h, i) => {
            const right = sideOf(h.card);
            return (
              <li key={i} className={h.ok ? 'is-ok' : 'is-bad'} style={{ '--i': i } as React.CSSProperties}>
                <span className="ls-res-ico" aria-hidden>{h.ok ? <Check /> : <X />}</span>
                <div>
                  <Inline text={h.card.text || ''} as="p" className="ls-res-t" />
                  <span className="ls-res-tag">{right === 'left' ? L : right === 'right' ? R : ''}</span>
                  {h.card.explanation && <Inline text={cleanVerdict(h.card.explanation)} as="p" className="ls-res-why" />}
                </div>
              </li>
            );
          })}
        </ul>
        <button
          type="button"
          className="ls-btn is-sm self-start"
          onClick={() => {
            setIdx(0);
            setLog([]);
          }}
        >
          <RotateCcw aria-hidden /> Yeniden
        </button>
      </div>
    );
  }

  return (
    <div className="ls-ix-body">
      {e.title && <Inline text={e.title} as="p" className="ls-ix-q" />}
      <div className="ls-swipe-top">
        <Pips total={cards.length} at={idx} results={log.map((h) => h.ok)} label="Kart ilerlemesi" />
        <span className="ls-mono">{idx + 1}/{cards.length}</span>
      </div>
      <div className="ls-swipe-deck">
        {cards.slice(idx + 1, idx + 3).map((_, k) => (
          <div key={idx + 1 + k} className="ls-swipe-ghost" style={{ '--d': k + 1 } as React.CSSProperties} aria-hidden />
        ))}
        <div
          key={idx}
          role="group"
          tabIndex={0}
          aria-label={`Kart ${idx + 1}. Sola ${L}, sağa ${R}. Ok tuşları da çalışır.`}
          className={`ls-swipe-card ${drag ? 'is-drag' : ''} ${fly ? `is-fly-${fly}` : ''} ${verdict ? (verdict.ok ? 'is-ok' : 'is-bad') : ''}`}
          style={{ '--dx': `${dx}px`, '--lean': lean } as React.CSSProperties}
          onPointerDown={onDown}
          onPointerMove={onMove}
          onPointerUp={onUp}
          onPointerCancel={onUp}
          onKeyDown={onKey}
        >
          <span className="ls-swipe-hint is-left" aria-hidden>{L}</span>
          <span className="ls-swipe-hint is-right" aria-hidden>{R}</span>
          <Inline text={card?.text || ''} as="p" className="ls-swipe-text" />
          {verdict && (
            <span className="ls-swipe-stamp" role="status">
              {verdict.ok ? <Check aria-hidden /> : <X aria-hidden />}
              {verdict.ok ? 'Doğru' : `Doğrusu: ${sideOf(card) === 'left' ? L : R}`}
            </span>
          )}
        </div>
      </div>
      <div className="ls-swipe-btns">
        <button type="button" className="ls-swipe-btn is-left" onClick={() => decide('left')} disabled={!!verdict}>
          <ChevronLeft aria-hidden /><span>{L}</span>
        </button>
        <button type="button" className="ls-swipe-btn is-right" onClick={() => decide('right')} disabled={!!verdict}>
          <span>{R}</span><ChevronRight aria-hidden />
        </button>
      </div>
    </div>
  );
};

const CONF = [
  { m: 1, t: 'Emin değilim' },
  { m: 2, t: 'Eminim' },
  { m: 3, t: 'Çok eminim' },
] as const;

export const FeatureBidding: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const A = e.optionA || 'A';
  const B = e.optionB || 'B';
  const rounds: any[] = Array.isArray(e.rounds) && e.rounds.length ? e.rounds : [{ feature: e.feature || '', correct: e.correct || e.correctOption || 'A', explanation: e.explanation }];
  const [r, setR] = useState(0);
  const [mult, setMult] = useState<1 | 2 | 3>(2);
  const [pick, setPick] = useState<'A' | 'B' | null>(null);
  const [score, setScore] = useState(0);
  const [log, setLog] = useState<Array<{ round: any; picked: 'A' | 'B'; mult: number; delta: number; ok: boolean }>>([]);
  const round = rounds[r];
  const finished = r >= rounds.length;
  const rightOf = (x: any): 'A' | 'B' => (String(x?.correct || 'A').toUpperCase() === 'B' ? 'B' : 'A');
  const last = log[log.length - 1];

  const choose = (c: 'A' | 'B') => {
    if (pick || !round) return;
    const ok = c === rightOf(round);
    const delta = (ok ? 10 : -10) * mult;
    setPick(c);
    setScore((s) => s + delta);
    setLog((l) => [...l, { round, picked: c, mult, delta, ok }]);
    if (r + 1 >= rounds.length) onDone?.();
  };
  const next = () => {
    setPick(null);
    setMult(2);
    setR((x) => x + 1);
  };
  const fmt = (n: number) => (n > 0 ? `+${n}` : n < 0 ? `\u2212${-n}` : '0');

  return (
    <div className="ls-ix-body">
      {e.title && <Inline text={e.title} as="p" className="ls-ix-q" />}
      <div className="ls-bid-top">
        <Pips total={rounds.length} at={r} results={log.map((x) => x.ok)} label="Tur ilerlemesi" />
        <span className={`ls-bid-score ${score < 0 ? 'is-neg' : ''}`} aria-live="polite">
          <Award aria-hidden /><b key={score}>{fmt(score)}</b>
          {pick && last && <i key={log.length} className={last.ok ? 'is-ok' : 'is-bad'} aria-hidden>{fmt(last.delta)}</i>}
        </span>
      </div>

      {!finished && round ? (
        <>
          <div key={r} className="ls-bid-feature">
            <span className="ls-mono">Tur {r + 1}/{rounds.length}</span>
            <Inline text={round.feature || ''} as="p" />
          </div>
          {!pick && (
            <div className="ls-bid-conf" role="radiogroup" aria-label="Ne kadar eminsin?">
              {CONF.map((c) => (
                <button key={c.m} type="button" role="radio" aria-checked={mult === c.m} className={mult === c.m ? 'is-on' : ''} onClick={() => setMult(c.m)}>
                  <b>{c.m}×</b><span>{c.t}</span><small>±{c.m * 10}</small>
                </button>
              ))}
            </div>
          )}
          <div className="ls-bid-choices">
            {(['A', 'B'] as const).map((k) => {
              const right = pick && rightOf(round) === k;
              const wrong = pick === k && !right;
              return (
                <button
                  key={k}
                  type="button"
                  className={`ls-bid-choice ${right ? 'is-ok' : ''} ${wrong ? 'is-bad' : ''} ${pick && !right && !wrong ? 'is-dim' : ''}`}
                  onClick={() => choose(k)}
                  disabled={!!pick}
                >
                  <span className="k" aria-hidden>{right ? <Check /> : wrong ? <X /> : k}</span>
                  <span className="t">{k === 'A' ? A : B}</span>
                </button>
              );
            })}
          </div>
          {pick && last && (
            <div className="ls-bid-verdict">
              <p className={`ls-fb ${last.ok ? 'is-ok' : 'is-bad'}`} role="status">
                <b>{last.ok ? `Doğru · ${fmt(last.delta)}` : last.mult === 3 ? `Aşırı güven · ${fmt(last.delta)}` : `Yanlış · ${fmt(last.delta)}`}</b>
                {round.explanation && <> <Inline text={cleanVerdict(round.explanation)} /></>}
              </p>
              <button type="button" className="ls-btn is-primary self-start" onClick={next}>
                {r + 1 < rounds.length ? 'Sonraki tur' : 'Sonucu gör'} <ChevronRight aria-hidden />
              </button>
            </div>
          )}
        </>
      ) : (
        <>
          <div className="ls-score">
            <b>{fmt(score)}<small> puan</small></b>
            <span>
              {log.filter((x) => x.ok).length}/{rounds.length} doğru ·{' '}
              {score >= rounds.length * 20 ? 'güvenin bilgine denk.' : score > 0 ? 'iyi denge; tereddütlerini gözden geçir.' : 'güvenini bilginle eşitle; gerekçelere bak.'}
            </span>
          </div>
          <ul className="ls-reslist">
            {log.map((x, i) => (
              <li key={i} className={x.ok ? 'is-ok' : 'is-bad'} style={{ '--i': i } as React.CSSProperties}>
                <span className="ls-res-ico" aria-hidden>{x.ok ? <Check /> : <X />}</span>
                <div>
                  <Inline text={x.round.feature || ''} as="p" className="ls-res-t" />
                  <span className="ls-res-tag">{rightOf(x.round) === 'A' ? A : B} · {x.mult}× · {fmt(x.delta)}</span>
                  {x.round.explanation && <Inline text={cleanVerdict(x.round.explanation)} as="p" className="ls-res-why" />}
                </div>
              </li>
            ))}
          </ul>
          <button
            type="button"
            className="ls-btn is-sm self-start"
            onClick={() => {
              setR(0);
              setPick(null);
              setMult(2);
              setScore(0);
              setLog([]);
            }}
          >
            <RotateCcw aria-hidden /> Yeniden
          </button>
        </>
      )}
    </div>
  );
};

const VENN_KEYS = ['a', 'b', 'both'] as const;
type VennKey = (typeof VENN_KEYS)[number] | 'neither';
const normVenn = (t: string): VennKey => {
  const s = String(t || '').toLocaleLowerCase('tr-TR');
  if (['both', 'both_a_b', 'ikisi', 'her ikisi'].includes(s)) return 'both';
  if (['neither', 'hicbiri', 'hiçbiri'].includes(s)) return 'neither';
  return s === 'b' ? 'b' : 'a';
};

export const VennGrid: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const A = e.labelA || 'A';
  const B = e.labelB || 'B';
  const items: any[] = Array.isArray(e.items) ? e.items : [];
  const hasNeither = items.some((it) => normVenn(it.correct) === 'neither');
  const keys: VennKey[] = hasNeither ? [...VENN_KEYS, 'neither'] : [...VENN_KEYS];
  const short: Record<VennKey, string> = { a: 'A', b: 'B', both: 'İkisi', neither: 'Hiçbiri' };
  const full: Record<VennKey, string> = { a: A, b: B, both: 'Her ikisi', neither: 'Hiçbiri' };
  const [ans, setAns] = useState<Record<number, VennKey>>({});
  const [closed, setClosed] = useState<Set<number>>(new Set());
  const n = Object.keys(ans).length;
  const correct = items.reduce((acc, it, i) => (ans[i] && ans[i] === normVenn(it.correct) ? acc + 1 : acc), 0);

  const choose = (i: number, k: VennKey) =>
    setAns((prev) => {
      if (prev[i]) return prev;
      const next = { ...prev, [i]: k };
      if (Object.keys(next).length === items.length) queueMicrotask(() => onDone?.());
      return next;
    });

  return (
    <div className="ls-ix-body">
      {e.title && <Inline text={e.title} as="p" className="ls-ix-q" />}
      <div className="ls-poles">
        <Pole k="A" label={A} />
        <Pole k="B" label={B} />
        <span className="ls-mono ls-poles-n">{n}/{items.length}</span>
      </div>
      <ol className="ls-vg">
        {items.map((it, i) => {
          const target = normVenn(it.correct);
          const mine = ans[i];
          const ok = mine === target;
          const why = cleanVerdict(it.explanation);
          const isOpen = !!mine && !!why && !closed.has(i);
          return (
            <li key={i} className={`ls-vg-row ${mine ? (ok ? 'is-ok' : 'is-bad') : ''}`} style={{ '--i': i } as React.CSSProperties}>
              <div className="ls-vg-main">
                <Inline text={it.criterion || ''} as="p" className="ls-vg-text" />
                <div className="ls-vg-seg" role="radiogroup" aria-label={`${i + 1}. özellik`}>
                  {keys.map((k) => (
                    <button
                      key={k}
                      type="button"
                      role="radio"
                      aria-checked={mine === k}
                      aria-label={full[k]}
                      title={full[k]}
                      disabled={!!mine}
                      className={mine ? (k === target ? 'is-target' : k === mine ? 'is-miss' : '') : ''}
                      onClick={() => choose(i, k)}
                    >
                      {short[k]}
                    </button>
                  ))}
                </div>
              </div>
              {mine && why && (
                <>
                  <button
                    type="button"
                    className="ls-vg-why-toggle"
                    aria-expanded={isOpen}
                    onClick={() => setClosed((s) => { const c = new Set(s); c.has(i) ? c.delete(i) : c.add(i); return c; })}
                  >
                    {ok ? 'Doğru' : `Doğrusu: ${full[target]}`}
                    <ChevronDown aria-hidden />
                  </button>
                  <div className="ls-fold" aria-hidden={!isOpen}>
                    <div><Inline text={why} as="p" className="ls-vg-why" /></div>
                  </div>
                </>
              )}
            </li>
          );
        })}
      </ol>
      {n === items.length && items.length > 0 && (
        <p className={`ls-fb ${correct === items.length ? 'is-ok' : 'is-plain'}`} role="status">
          <b>{correct}/{items.length} doğru.</b>
          <span className="ls-fb-hint">{correct === items.length ? ' İki tabloyu ayıran her ölçütü yerine koydun.' : ' Kırmızı satırların gerekçesini oku.'}</span>
        </p>
      )}
    </div>
  );
};

export const FlipCards: React.FC<{ cards: LessonCard[]; onDone?: () => void }> = ({ cards, onDone }) => {
  const [i, setI] = useState(0);
  const [turned, setTurned] = useState(false);
  const c = cards[i];
  const go = (d: number) => {
    setTurned(false);
    setI((x) => (x + d + cards.length) % cards.length);
  };
  if (!c) return null;
  return (
    <div className="ls-ix-body">
      <div className={`ls-flip ${turned ? 'is-turned' : ''}`}>
        <button
          type="button"
          className="ls-flip-in"
          aria-label={turned ? 'Kartın önüne dön' : 'Kartı çevir'}
          onClick={() => {
            setTurned((t) => !t);
            onDone?.();
          }}
        >
          <span className="ls-flip-face is-front">
            <small>{c.category || 'Kart'} · {i + 1}/{cards.length}</small>
            <span className="q">{c.front}</span>
            {c.hint && <span className="ls-hint"><Info aria-hidden /> {c.hint}</span>}
          </span>
          <span className="ls-flip-face is-back">
            <small>Cevap</small>
            <span className="q">{c.back}</span>
          </span>
        </button>
      </div>
      {cards.length > 1 && (
        <div className="ls-fc-nav">
          <button type="button" className="ls-btn is-icon" onClick={() => go(-1)} aria-label="Önceki kart"><ChevronLeft aria-hidden /></button>
          <span className="ls-dots" aria-hidden>{cards.map((_, k) => <i key={k} className={k === i ? 'is-on' : ''} />)}</span>
          <button type="button" className="ls-btn is-icon" onClick={() => go(1)} aria-label="Sonraki kart"><ChevronRight aria-hidden /></button>
        </div>
      )}
    </div>
  );
};

export const QuestionCard: React.FC<{ q: LessonQuestion; onDone?: () => void }> = ({ q, onDone }) => {
  const { perOption, rest } = useMemo(() => splitExplanation(q.explanation, q.options.map((o) => o.key)), [q]);
  return (
    <OptionList
      question={q.stem}
      options={q.options.map((o) => ({ key: o.key, text: o.text, ok: o.key === q.answer, why: o.explanation || perOption[o.key] }))}
      extraWhy={rest}
      onDone={onDone}
    />
  );
};

const IxBody: React.FC<{ item: PracticeItem; onDone?: () => void }> = ({ item, onDone }) => {
  if (item.kind === 'cards') return <FlipCards cards={item.cards} onDone={onDone} />;
  if (item.kind === 'question') return <QuestionCard q={item.q} onDone={onDone} />;
  const e = item.data;
  switch (e.type) {
    case 'micro_quiz':
      return (
        <OptionList
          question={e.question || e.sentence || ''}
          options={(e.microQuizOptions || e.options || []).map((o: any, k: number) => ({ key: o.key || String.fromCharCode(65 + k), text: o.text, ok: !!o.isCorrect, why: o.explanation }))}
          onDone={onDone}
        />
      );
    case 'branching_logic': {
      // Veri üç biçimde gelir: options | branchingOptions | choices; soru question/initialQuestion'da, vaka scenario'da
      const ask = e.question || e.initialQuestion || '';
      const opts = [e.options, e.choices, e.branchingOptions].find((x) => Array.isArray(x) && x.length) || [];
      // Bazı vakalarda soru cümlesi senaryonun sonuna da eklenmiş: vaka kutusunda tekrar gösterme
      const caseText = ask && e.scenario ? String(e.scenario).replace(ask, '').replace(/[\s\-–—:]+$/, '').trim() : '';
      return (
        <OptionList
          context={caseText || undefined}
          question={ask || e.scenario || ''}
          options={opts.map((o: any, k: number) => ({ key: String.fromCharCode(65 + k), text: o.text || o.label || '', ok: !!(o.isCorrect ?? o.correct), why: o.feedback || o.explanation }))}
          onDone={onDone}
        />
      );
    }
    case 'interactive_table':
    case 'hidden_table': {
      const title = e.tableTitle || e.title || '';
      const headers = (e.tableHeaders && e.tableHeaders.length ? e.tableHeaders : e.headers) || (e.table && e.table.headers) || [];
      const rawRows = (e.tableRows && e.tableRows.length ? e.tableRows : e.rows) || (e.table && e.table.rows) || [];
      const rows = rawRows.map((r: any) => {
        if (Array.isArray(r)) return r;
        if (r && Array.isArray(r.cells)) return r.cells;
        return [];
      });
      return (
        <div className="ls-ix-body">
          <LessonTable title={title} headers={headers} rows={rows} masked onAllRevealed={onDone} />
        </div>
      );
    }
    case 'cloze_masking':
      return <Cloze e={e} onDone={onDone} />;
    case 'causal_chain':
      return <Chain e={e} onDone={onDone} />;
    case 'before_after_slider':
      return <Compare e={e} onDone={onDone} />;
    case 'active_recall':
      return <Recall e={e} onDone={onDone} />;
    case 'spot_the_lie':
      return <SpotTheLie e={e} onDone={onDone} />;
    case 'swipe_matching':
      return <SwipeMatching e={e} onDone={onDone} />;
    case 'feature_bidding':
      return <FeatureBidding e={e} onDone={onDone} />;
    case 'venn_grid':
      return <VennGrid e={e} onDone={onDone} />;
    default:
      return null;
  }
};

export const PracticeCard: React.FC<{ item: PracticeItem; done?: boolean; onDone?: () => void; style?: React.CSSProperties; className?: string; target?: FeedbackTarget }> = ({ item, done, onDone, style, className = '', target }) => {
  const [Icon, label] = practiceMeta(item);
  return (
    <section className={`ls-ix ${className}`} style={style} aria-label={label} data-fb-key={target?.key}>
      <header className="ls-ix-head">
        <Icon aria-hidden />
        <span className="ls-ix-label" title={label}>{label}</span>
        {item.kind === 'question' && item.q.examYear && <span className="ls-tag is-plain" title={item.q.examYear}>{item.q.examYear}</span>}
        {done && <span className="ls-tag is-ok"><Check aria-hidden /> Tamam</span>}
        {target && <FeedbackFlag target={target} />}
      </header>
      <IxBody item={item} onDone={onDone} />
    </section>
  );
};

/* ---------------------------------------------------------------------------
 * Bilgi bölmesi içerikleri
 * ------------------------------------------------------------------------- */
export type InfoId = 'spot' | 'terms' | 'kaz' | 'q' | 'teacher' | 'src';
export interface InfoTab { id: InfoId; label: string; icon: React.ElementType; count: number; hot?: boolean }

export const infoTabsFor = (step: LessonStep, kaz: DeckKazanim[]): InfoTab[] =>
  [
    { id: 'spot' as const, label: 'Sınav spotu', icon: Flag, count: step.spots.length, hot: true },
    { id: 'teacher' as const, label: 'Hoca notu', icon: Quote, count: (step.teacher ? 1 : 0) + (step.important ? 1 : 0) + (step.examTip ? 1 : 0) },
    { id: 'terms' as const, label: 'Terimler', icon: Tag, count: step.terms.length },
    { id: 'kaz' as const, label: 'Kazanımlar', icon: Target, count: kaz.length },
    { id: 'src' as const, label: 'Kaynak', icon: FileText, count: 1 },
  ].filter((t) => t.count > 0);

const termKey = (term: string) => term.slice(0, 60).replace(/[^\p{L}\d]+/gu, '-');

export const InfoPane: React.FC<{
  id: InfoId;
  step: LessonStep;
  kaz: DeckKazanim[];
  deckPastCount?: number;
  citation: string;
  page: number;
  onOpenPdf: () => void;
  /** Bu adımdaki i. soruyu Pekiştir'de aç */
  onPractice: (questionIndex: number) => void;
}> = ({ id, step, kaz, deckPastCount, citation, page, onOpenPdf, onPractice }) => {
  const PANE: Record<string, string> = { spot: 'Sınav spotu', teacher: 'Hoca notu', important: 'Hoca notu', tip: 'Hoca notu', term: 'Terimler' };
  const t = (kind: string, i: number | string, label: string, hint?: string, nth?: number): FeedbackTarget => ({
    key: `${step.number}:${kind}:${i}`,
    label,
    slideNumber: step.number,
    hint,
    location: `Bilgi bölmesi › ${PANE[kind] || label}${nth != null ? ` › ${nth}. öğe` : ''}${PANE[kind] && PANE[kind] !== label ? ` (${label})` : ''}`,
  });
  const short = (x: string) => stripEmoji(x).replace(/\*\*/g, '').slice(0, 90);
  if (id === 'spot')
    return (
      <ul className="ls-info">
        {step.spots.map((s, i) => (
          <li key={i} data-fb-key={`${step.number}:spot:${i}`}>
            <span className={`ico is-${spotTone(s)}`}><Flag aria-hidden /></span>
            <Inline text={s} />
            <FeedbackFlag target={t('spot', i, 'Sınav spotu', short(s), i + 1)} className="meta" />
          </li>
        ))}
      </ul>
    );
  if (id === 'teacher')
    return (
      <ul className="ls-info">
        {step.teacher && (
          <li data-fb-key={`${step.number}:teacher:0`}>
            <span className="ico is-accent"><Mic aria-hidden /></span>
            <span>{step.teacher.quote && <b>“{step.teacher.quote}”</b>}{step.teacher.note && <><br />{step.teacher.note}</>}</span>
            <FeedbackFlag target={t('teacher', 0, 'Hocanın vurgusu', short(step.teacher.quote || step.teacher.note || ''))} className="meta" />
          </li>
        )}
        {step.important && (
          <li data-fb-key={`${step.number}:important:0`}>
            <span className="ico is-bad"><Sparkles aria-hidden /></span>
            <span><b>Önemli nokta</b><br /><Inline text={step.important} /></span>
            <FeedbackFlag target={t('important', 0, 'Önemli nokta', short(step.important))} className="meta" />
          </li>
        )}
        {step.examTip && (
          <li data-fb-key={`${step.number}:tip:0`}>
            <span className="ico is-warn"><Flag aria-hidden /></span>
            <span><b>Sınav ipucu</b><br /><Inline text={step.examTip} /></span>
            <FeedbackFlag target={t('tip', 0, 'Sınav ipucu', short(step.examTip))} className="meta" />
          </li>
        )}
      </ul>
    );
  if (id === 'terms')
    return (
      <ul className="ls-info">
        {step.terms.map((term, i) => (
          <li key={i} data-fb-key={`${step.number}:term:${termKey(term.term)}`}>
            <span className="ico is-accent"><Tag aria-hidden /></span>
            <span>
              <b>{term.term}</b>
              {(term as any).category && <span className="ls-tag is-plain ls-term-cat">{(term as any).category}</span>}
              <br />
              {term.explanation}
            </span>
            <FeedbackFlag target={t('term', termKey(term.term), `Terim: ${term.term}`, term.term, i + 1)} className="meta" />
          </li>
        ))}
      </ul>
    );
  if (id === 'kaz')
    return (
      <ul className="ls-info">
        {kaz.map((k, i) => (
          <li key={i}>
            <span className="ico is-ok"><Target aria-hidden /></span>
            <span>{k.m}</span>
          </li>
        ))}
      </ul>
    );
  return (
    <ul className="ls-info">
      <li>
        <span className="ico"><FileText aria-hidden /></span>
        <span><b>{citation}</b><br />Hocanın orijinal sunumu · sayfa {page}</span>
        <button type="button" className="ls-btn is-sm meta" onClick={onOpenPdf}><BookOpenText aria-hidden /> PDF'te aç</button>
      </li>
    </ul>
  );
};

export { stripEmoji };
