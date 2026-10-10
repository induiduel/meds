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
const OptionList: React.FC<{ question: string; options: OptLike[]; onDone?: () => void; extraWhy?: string }> = ({ question, options, onDone, extraWhy }) => {
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
 * Yeni İnteraktif Modeller:
 * 1. SpotTheLie: Hata / Tuzak Avı (3 doğru, 1 yanıltıcı çeldiriciyi bulma)
 * 2. SwipeMatching: Hızlı Kart Eşleme / Kategori Kaydırma (Tinder stili refleks testi)
 * 3. FeatureBidding: Özellik Açık Artırması / Puan Bahsi (Metabilişsel güven çarpanı)
 * 4. VennGrid: Teşhis Çapraz Tablosu (Doğru - Yanlış - Her İkisi / Ayırıcı Tanı Matrisi)
 * ------------------------------------------------------------------------- */

export const SpotTheLie: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const [selectedIdx, setSelectedIdx] = useState<number | null>(null);
  const [revealed, setRevealed] = useState<Set<number>>(new Set());
  const items: any[] = Array.isArray(e.items) ? e.items : [];
  const topic = e.topic || e.question || 'Aşağıdaki önermelerden hangisi yanıltıcı bir tuzaktır?';
  const lieIdx = items.findIndex((it) => !!(it.isLie || it.isTrap));

  const handleSelect = (idx: number) => {
    if (selectedIdx === null) {
      setSelectedIdx(idx);
      setRevealed(new Set([idx]));
      onDone?.();
    } else {
      setRevealed((prev) => {
        const next = new Set(prev);
        if (next.has(idx)) next.delete(idx);
        else next.add(idx);
        return next;
      });
    }
  };

  const isLieSelected = selectedIdx !== null && selectedIdx === lieIdx;

  return (
    <div className="ls-ix-body">
      <div className="ls-stl-header">
        <Inline text={topic} as="p" className="ls-ix-q" />
        <span className="ls-stl-instruction">
          <ShieldAlert aria-hidden /> 3 doğru, 1 yanıltıcı çeldirici var. Tuzağı tespit et!
        </span>
      </div>

      <ul className="ls-stl-list">
        {items.map((it, idx) => {
          const isLie = !!(it.isLie || it.isTrap);
          const isPicked = selectedIdx === idx;
          const isOpen = revealed.has(idx);

          let cardTone = '';
          if (selectedIdx !== null) {
            if (isLie) {
              cardTone = 'is-lie-card';
            } else if (isPicked) {
              cardTone = 'is-wrong-pick';
            } else {
              cardTone = 'is-safe-card';
            }
          }

          return (
            <li key={idx} className={`ls-stl-item ${cardTone} ${isOpen ? 'is-open' : ''}`}>
              <button
                type="button"
                className="ls-stl-btn"
                onClick={() => handleSelect(idx)}
                aria-expanded={isOpen}
              >
                <span className="ls-stl-badge">
                  {selectedIdx === null ? (
                    String.fromCharCode(65 + idx)
                  ) : isLie ? (
                    <ShieldAlert aria-hidden />
                  ) : isPicked ? (
                    <X aria-hidden />
                  ) : (
                    <Check aria-hidden />
                  )}
                </span>
                <span className="ls-stl-text">
                  <Inline text={it.text || ''} />
                </span>
                {selectedIdx !== null && it.explanation && (
                  <ChevronDown className="ls-opt-chev" aria-hidden />
                )}
              </button>

              {selectedIdx !== null && isOpen && it.explanation && (
                <div className="ls-stl-panel">
                  <span className={`ls-stl-verdict ${isLie ? 'is-trap-tag' : 'is-fact-tag'}`}>
                    {isLie ? '🚨 TUZAK / YANILTICI ÖNERME' : '✅ TIBBEN DOĞRU BİLGİ'}
                  </span>
                  <p className="ls-stl-expl">
                    <Inline text={cleanWhy(it.explanation)} />
                  </p>
                </div>
              )}
            </li>
          );
        })}
      </ul>

      {selectedIdx !== null && (
        <div className={`ls-fb ${isLieSelected ? 'is-ok' : 'is-bad'}`} role="status">
          <b>
            {isLieSelected
              ? '🎯 Tebrikler! Tuzağı başarıyla yakaladın.'
              : '⚠️ Bu önerme tıbben doğrudur! Yanıltıcı çeldiriciyi incele.'}
          </b>
          <span className="ls-fb-hint"> Maddelere dokunarak gerekçelerini inceleyebilirsin.</span>
        </div>
      )}
    </div>
  );
};

export const SwipeMatching: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const cards: any[] = Array.isArray(e.cards) ? e.cards : [];
  const leftLabel = typeof e.leftCategory === 'object' && e.leftCategory ? (e.leftCategory.label || e.leftCategory.name || 'Sol Kategori') : String(e.leftCategory || 'Sol Kategori');
  const rightLabel = typeof e.rightCategory === 'object' && e.rightCategory ? (e.rightCategory.label || e.rightCategory.name || 'Sağ Kategori') : String(e.rightCategory || 'Sağ Kategori');
  const title = e.title || `${leftLabel} vs ${rightLabel}`;

  const [idx, setIdx] = useState(0);
  const [history, setHistory] = useState<Array<{ card: any; chosen: 'left' | 'right'; isCorrect: boolean }>>([]);
  const [dragOffset, setDragOffset] = useState<number>(0);
  const [isDragging, setIsDragging] = useState(false);
  const [animatingDir, setAnimatingDir] = useState<'left' | 'right' | null>(null);
  const startXRef = useRef<number>(0);

  const isCompleted = idx >= cards.length;
  const currentCard = !isCompleted ? cards[idx] : null;

  const handleMatch = (dir: 'left' | 'right') => {
    if (isCompleted || animatingDir || !currentCard) return;
    setAnimatingDir(dir);
    const targetCat = String(currentCard.category || currentCard.correctCategory || '').toLowerCase();
    const isCorrect = (dir === 'left' && (targetCat === 'left' || targetCat === 'l' || targetCat === leftLabel.toLowerCase()))
      || (dir === 'right' && (targetCat === 'right' || targetCat === 'r' || targetCat === rightLabel.toLowerCase()));

    setTimeout(() => {
      setHistory((prev) => [...prev, { card: currentCard, chosen: dir, isCorrect }]);
      const nextIdx = idx + 1;
      setIdx(nextIdx);
      setAnimatingDir(null);
      setDragOffset(0);
      if (nextIdx >= cards.length) {
        onDone?.();
      }
    }, 280);
  };

  const resetAll = () => {
    setIdx(0);
    setHistory([]);
    setDragOffset(0);
    setAnimatingDir(null);
  };

  const handleTouchStart = (ev: React.TouchEvent | React.MouseEvent) => {
    if (isCompleted || animatingDir) return;
    setIsDragging(true);
    const pageX = 'touches' in ev ? ev.touches[0].pageX : ev.pageX;
    startXRef.current = pageX;
  };

  const handleTouchMove = (ev: React.TouchEvent | React.MouseEvent) => {
    if (!isDragging) return;
    const pageX = 'touches' in ev ? ev.touches[0].pageX : ev.pageX;
    const diff = pageX - startXRef.current;
    setDragOffset(diff);
  };

  const handleTouchEnd = () => {
    if (!isDragging) return;
    setIsDragging(false);
    if (dragOffset > 70) {
      handleMatch('right');
    } else if (dragOffset < -70) {
      handleMatch('left');
    } else {
      setDragOffset(0);
    }
  };

  const correctCount = history.filter((h) => h.isCorrect).length;

  return (
    <div className="ls-ix-body">
      <div className="ls-swipe-head">
        <span className="ls-eyebrow">Hızlı Kart Eşleme (Kategori Kaydırma)</span>
        <Inline text={title} as="p" className="ls-ix-q" />
      </div>

      {!isCompleted && currentCard ? (
        <div className="ls-swipe-arena">
          <div className="ls-swipe-targets">
            <button
              type="button"
              className={`ls-swipe-target is-left ${dragOffset < -25 ? 'is-active' : ''}`}
              onClick={() => handleMatch('left')}
            >
              <ChevronLeft aria-hidden />
              <span>{leftLabel}</span>
            </button>

            <span className="ls-swipe-progress">
              {idx + 1} / {cards.length}
            </span>

            <button
              type="button"
              className={`ls-swipe-target is-right ${dragOffset > 25 ? 'is-active' : ''}`}
              onClick={() => handleMatch('right')}
            >
              <span>{rightLabel}</span>
              <ChevronRight aria-hidden />
            </button>
          </div>

          <div
            className={`ls-swipe-card ${animatingDir === 'left' ? 'is-flying-left' : ''} ${animatingDir === 'right' ? 'is-flying-right' : ''}`}
            style={{
              transform: !animatingDir ? `translateX(${dragOffset}px) rotate(${dragOffset * 0.08}deg)` : undefined,
              transition: isDragging ? 'none' : 'transform 0.28s ease-out',
            }}
            onTouchStart={handleTouchStart}
            onTouchMove={handleTouchMove}
            onTouchEnd={handleTouchEnd}
            onMouseDown={handleTouchStart}
            onMouseMove={handleTouchMove}
            onMouseUp={handleTouchEnd}
            onMouseLeave={handleTouchEnd}
          >
            <div className="ls-swipe-card-badge">
              <Zap aria-hidden /> Refleks Kartı
            </div>
            <p className="ls-swipe-card-text">
              <Inline text={currentCard.text || ''} />
            </p>
            <div className="ls-swipe-cue">
              <span className="ls-swipe-cue-left">👈 {leftLabel}</span>
              <span className="ls-swipe-cue-right">{rightLabel} 👉</span>
            </div>
          </div>

          <div className="ls-swipe-actions">
            <button
              type="button"
              className="ls-btn ls-swipe-action-btn is-left"
              onClick={() => handleMatch('left')}
            >
              <ChevronLeft aria-hidden /> {leftLabel}
            </button>
            <button
              type="button"
              className="ls-btn ls-swipe-action-btn is-right"
              onClick={() => handleMatch('right')}
            >
              {rightLabel} <ChevronRight aria-hidden />
            </button>
          </div>
        </div>
      ) : (
        <div className="ls-swipe-summary">
          <div className={`ls-fb ${correctCount === cards.length ? 'is-ok' : 'is-plain'}`}>
            <b>⚡ Eşleme Tamamlandı! Skor: {correctCount} / {cards.length} Doğru</b>
            <span className="ls-fb-hint">
              {correctCount === cards.length
                ? ' Harika refleks! İki klinik tabloyu mükemmel ayırdın.'
                : ' Maddeleri aşağıdan inceleyip reflekslerini tazeleyebilirsin.'}
            </span>
          </div>

          <ul className="ls-swipe-result-list">
            {history.map((h, i) => (
              <li key={i} className={`ls-swipe-result-item ${h.isCorrect ? 'is-ok' : 'is-wrong'}`}>
                <div className="ls-swipe-result-head">
                  <span className="ls-swipe-result-icon">
                    {h.isCorrect ? <Check aria-hidden /> : <X aria-hidden />}
                  </span>
                  <span className="ls-swipe-result-text">
                    <Inline text={h.card.text} />
                  </span>
                  <span className="ls-tag">
                    {h.chosen === 'left' ? leftLabel : rightLabel}
                  </span>
                </div>
                {h.card.explanation && (
                  <p className="ls-swipe-result-expl">
                    <Inline text={cleanWhy(h.card.explanation)} />
                  </p>
                )}
              </li>
            ))}
          </ul>

          <button type="button" className="ls-btn is-sm self-start mt-2" onClick={resetAll}>
            <RotateCcw aria-hidden /> Tekrar Dene
          </button>
        </div>
      )}
    </div>
  );
};

export const FeatureBidding: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const optA = e.optionA || 'Seçenek A';
  const optB = e.optionB || 'Seçenek B';
  const title = e.title || `${optA} vs ${optB} Özellik Bahsi`;

  const rawRounds: any[] = Array.isArray(e.rounds) && e.rounds.length > 0 ? e.rounds : [
    { feature: e.feature || '', correct: e.correct || e.correctOption || 'A', explanation: e.explanation }
  ];

  const [roundIdx, setRoundIdx] = useState(0);
  const [multiplier, setMultiplier] = useState<1 | 2 | 3>(2);
  const [selectedOpt, setSelectedOpt] = useState<'A' | 'B' | null>(null);
  const [score, setScore] = useState(0);
  const [roundResults, setRoundResults] = useState<Array<{ round: any; picked: 'A' | 'B'; mult: number; delta: number; ok: boolean }>>([]);

  const currentRound = rawRounds[roundIdx];
  const isFinished = roundIdx >= rawRounds.length;

  const handlePick = (choice: 'A' | 'B') => {
    if (selectedOpt !== null || isFinished || !currentRound) return;
    setSelectedOpt(choice);

    const isCorrect = choice.toUpperCase() === String(currentRound.correct || 'A').toUpperCase();
    const basePoints = 10;
    const delta = isCorrect ? basePoints * multiplier : -basePoints * multiplier;

    setScore((s) => s + delta);
    setRoundResults((prev) => [
      ...prev,
      { round: currentRound, picked: choice, mult: multiplier, delta, ok: isCorrect }
    ]);

    if (roundIdx + 1 >= rawRounds.length) {
      onDone?.();
    }
  };

  const handleNextRound = () => {
    setSelectedOpt(null);
    setMultiplier(2);
    setRoundIdx((i) => i + 1);
  };

  const resetGame = () => {
    setRoundIdx(0);
    setSelectedOpt(null);
    setMultiplier(2);
    setScore(0);
    setRoundResults([]);
  };

  return (
    <div className="ls-ix-body">
      <div className="ls-bidding-head">
        <div className="flex items-center justify-between gap-2">
          <span className="ls-eyebrow">Özellik Açık Artırması (Puan Bahsi)</span>
          <span className={`ls-bidding-score ${score >= 0 ? 'is-pos' : 'is-neg'}`}>
            <Award aria-hidden /> Puan: {score > 0 ? `+${score}` : score}
          </span>
        </div>
        <Inline text={title} as="p" className="ls-ix-q" />
      </div>

      {!isFinished && currentRound ? (
        <div className="ls-bidding-arena">
          <div className="ls-bidding-round-badge">
            Tur {roundIdx + 1} / {rawRounds.length}
          </div>

          <div className="ls-bidding-feature-box">
            <span className="ls-bidding-feature-tag">Özellik / Patognomonik Bulgu:</span>
            <p className="ls-bidding-feature-text">
              <Inline text={currentRound.feature || ''} />
            </p>
          </div>

          {selectedOpt === null ? (
            <div className="ls-bidding-controls">
              <div className="ls-bidding-multiplier-row">
                <span className="ls-bidding-mult-label">
                  <Scale aria-hidden /> Kendine ne kadar güveniyorsun?
                </span>
                <div className="ls-bidding-mult-btns">
                  {([1, 2, 3] as const).map((m) => (
                    <button
                      key={m}
                      type="button"
                      className={`ls-bidding-mult-btn ${multiplier === m ? 'is-selected' : ''}`}
                      onClick={() => setMultiplier(m)}
                    >
                      <span className="m-val">{m}x</span>
                      <small className="m-desc">
                        {m === 1 ? 'Emin Değilim (+10/-10)' : m === 2 ? 'Güveniyorum (+20/-20)' : 'Adım Gibi Eminim (+30/-30)'}
                      </small>
                    </button>
                  ))}
                </div>
              </div>

              <div className="ls-bidding-choice-grid">
                <button
                  type="button"
                  className="ls-bidding-choice-btn is-a"
                  onClick={() => handlePick('A')}
                >
                  <span className="k">A</span>
                  <span className="t">{optA}</span>
                </button>
                <button
                  type="button"
                  className="ls-bidding-choice-btn is-b"
                  onClick={() => handlePick('B')}
                >
                  <span className="k">B</span>
                  <span className="t">{optB}</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="ls-bidding-verdict">
              {(() => {
                const isCorrect = selectedOpt.toUpperCase() === String(currentRound.correct || 'A').toUpperCase();
                const delta = isCorrect ? 10 * multiplier : -10 * multiplier;
                return (
                  <div className={`ls-fb ${isCorrect ? 'is-ok' : 'is-bad'}`}>
                    <b>
                      {isCorrect ? (
                        multiplier === 3 ? '🔥 TAM İSABET! Mükemmel Güven (+30 Puan)' : `🎯 Doğru Teşhis! (+${delta} Puan)`
                      ) : (
                        multiplier === 3 ? '🚨 AŞIRI GÜVEN YANILGISI! Dikkat Tuzağı (-30 Puan)' : `⚠️ Yanlış Karar! (${delta} Puan)`
                      )}
                    </b>
                    <p className="mt-1">
                      Bu özellik <b>{String(currentRound.correct).toUpperCase() === 'A' ? optA : optB}</b> tablosuna aittir.
                    </p>
                    {currentRound.explanation && (
                      <p className="mt-1 text-[13px] opacity-90">
                        <Inline text={cleanWhy(currentRound.explanation)} />
                      </p>
                    )}
                  </div>
                );
              })()}

              <button
                type="button"
                className="ls-btn is-primary mt-2"
                onClick={handleNextRound}
              >
                {roundIdx + 1 < rawRounds.length ? 'Sonraki Tur' : 'Sonucu Gör'} <ChevronRight aria-hidden />
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="ls-bidding-summary">
          <div className={`ls-fb ${score > 0 ? 'is-ok' : 'is-plain'}`}>
            <b>🏆 Bahis Tamamlandı! Toplam Puan: {score > 0 ? `+${score}` : score}</b>
            <span className="ls-fb-hint">
              {score >= 40
                ? ' Mükemmel klinik sezgi ve yüksek metabilişsel doğruluk!'
                : score > 0
                ? ' Başarılı bir analiz. Tereddüt ve güven dengesini iyi kurdun.'
                : ' Aşırı güven tuzaklarına dikkat; gerekçeleri tekrar gözden geçir.'}
            </span>
          </div>

          <ul className="ls-bidding-res-list">
            {roundResults.map((r, i) => (
              <li key={i} className={`ls-bidding-res-item ${r.ok ? 'is-ok' : 'is-bad'}`}>
                <div className="flex items-center justify-between gap-2">
                  <span className="font-semibold text-[13.5px]">
                    Tur {i + 1}: {r.ok ? '✅ Doğru' : '❌ Yanlış'} ({r.delta > 0 ? `+${r.delta}` : r.delta} Puan · {r.mult}x)
                  </span>
                  <span className="ls-tag">
                    {r.picked === 'A' ? optA : optB}
                  </span>
                </div>
                <p className="text-[13px] text-ink-2 mt-1">
                  <Inline text={r.round.feature} />
                </p>
                {r.round.explanation && (
                  <p className="text-[12.5px] text-ink-3 mt-1">
                    <Inline text={cleanWhy(r.round.explanation)} />
                  </p>
                )}
              </li>
            ))}
          </ul>

          <button type="button" className="ls-btn is-sm self-start mt-2" onClick={resetGame}>
            <RotateCcw aria-hidden /> Bahsi Yeniden Başlat
          </button>
        </div>
      )}
    </div>
  );
};

export const VennGrid: React.FC<{ e: any; onDone?: () => void }> = ({ e, onDone }) => {
  const labA = e.labelA || 'Durum A';
  const labB = e.labelB || 'Durum B';
  const title = e.title || `${labA} vs ${labB} Çapraz Karşılaştırma`;
  const items: any[] = Array.isArray(e.items) ? e.items : [];

  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [openedExpl, setOpenedExpl] = useState<Set<number>>(new Set());

  const answeredCount = Object.keys(answers).length;
  const isAllAnswered = items.length > 0 && answeredCount === items.length;

  const normTarget = (t: string) => {
    const s = String(t || '').toLowerCase();
    if (s === 'both_a_b' || s === 'ikisi' || s === 'her ikisi') return 'both';
    if (s === 'hicbiri' || s === 'hiçbiri') return 'neither';
    return s;
  };

  const handlePick = (idx: number, choice: string) => {
    if (answers[idx]) return;
    const nextAnswers = { ...answers, [idx]: choice };
    setAnswers(nextAnswers);
    setOpenedExpl((prev) => new Set(prev).add(idx));

    if (Object.keys(nextAnswers).length === items.length) {
      onDone?.();
    }
  };

  const toggleExpl = (idx: number) => {
    setOpenedExpl((prev) => {
      const n = new Set(prev);
      n.has(idx) ? n.delete(idx) : n.add(idx);
      return n;
    });
  };

  const correctCount = items.reduce((acc, it, idx) => {
    const userChoice = answers[idx];
    if (!userChoice) return acc;
    return normTarget(userChoice) === normTarget(it.correct) ? acc + 1 : acc;
  }, 0);

  return (
    <div className="ls-ix-body">
      <div className="ls-vg-head">
        <span className="ls-eyebrow">Teşhis Çapraz Tablosu (Venn Matrisi)</span>
        <Inline text={title} as="p" className="ls-ix-q" />
        <span className="ls-hint">
          Her özellik için ilgili hastalığı ya da her ikisini seçerek matrisi tamamlayın.
        </span>
      </div>

      <div className="ls-vg-table">
        {items.map((it, idx) => {
          const userAns = answers[idx];
          const target = normTarget(it.correct);
          const isAnswered = !!userAns;
          const isCorrect = isAnswered && normTarget(userAns) === target;
          const isExplOpen = openedExpl.has(idx);

          return (
            <div
              key={idx}
              className={`ls-vg-row ${isAnswered ? (isCorrect ? 'is-row-ok' : 'is-row-bad') : ''}`}
            >
              <div className="ls-vg-crit-col">
                <span className="ls-vg-num">{idx + 1}.</span>
                <span className="ls-vg-text">
                  <Inline text={it.criterion || ''} />
                </span>
                {isAnswered && it.explanation && (
                  <button
                    type="button"
                    className="ls-vg-expl-toggle"
                    onClick={() => toggleExpl(idx)}
                    aria-label="Açıklamayı göster/gizle"
                  >
                    <Info aria-hidden /> Gerekçe
                  </button>
                )}
              </div>

              <div className="ls-vg-btns-col">
                {[
                  { key: 'a', label: labA },
                  { key: 'b', label: labB },
                  { key: 'both', label: 'Her İkisi' },
                ].map((btn) => {
                  const isThisPicked = userAns === btn.key;
                  const isThisTarget = target === btn.key;

                  let btnClass = 'ls-vg-btn';
                  if (isAnswered) {
                    if (isThisTarget) btnClass += ' is-target';
                    if (isThisPicked && !isCorrect) btnClass += ' is-wrong-picked';
                    if (isThisPicked && isCorrect) btnClass += ' is-correct-picked';
                  }

                  return (
                    <button
                      key={btn.key}
                      type="button"
                      className={btnClass}
                      disabled={isAnswered}
                      onClick={() => handlePick(idx, btn.key)}
                    >
                      {btn.label}
                    </button>
                  );
                })}
              </div>

              {isAnswered && isExplOpen && it.explanation && (
                <div className="ls-vg-row-expl">
                  <span className={`ls-vg-verdict ${isCorrect ? 'is-ok' : 'is-bad'}`}>
                    {isCorrect ? 'Doğru Eşleşme' : `Hatalı (Doğrusu: ${target === 'both' ? 'Her İkisi' : target === 'a' ? labA : labB})`}
                  </span>
                  <p>
                    <Inline text={cleanWhy(it.explanation)} />
                  </p>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {isAllAnswered && (
        <div className={`ls-fb ${correctCount === items.length ? 'is-ok' : 'is-plain'}`}>
          <b>
            Matris Tamamlandı! Skor: {correctCount} / {items.length} Doğru
          </b>
          <span className="ls-fb-hint">
            {correctCount === items.length
              ? ' Tebrikler, iki antite arasındaki tüm klinik ayrım kriterlerini eksiksiz kavradın!'
              : ' Ayırıcı tanı tablosundaki gerekçeleri inceleyerek bilgileri pekiştirebilirsin.'}
          </span>
        </div>
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
    case 'branching_logic':
      return (
        <OptionList
          question={e.scenario || e.question || ''}
          options={(e.options || []).map((o: any, k: number) => ({ key: String.fromCharCode(65 + k), text: o.text, ok: !!o.isCorrect, why: o.feedback }))}
          onDone={onDone}
        />
      );
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
