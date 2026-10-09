import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  BookOpen, Check, Eraser, Hand, Highlighter, PenLine, ChevronDown, ChevronLeft, ChevronRight, Columns, EyeOff, FileDown, FileText, GalleryHorizontal, History,
  Info, LayoutPanelLeft, ListTree, Lock, Maximize2, MessageCircleQuestion, Minimize2, MoreHorizontal, NotebookText,
  PanelsTopLeft, Rows3, Search, Sparkles, X,
} from 'lucide-react';
import type { InteractiveDeck } from '../InteractiveDeckView';
import { AskAi, GlobalTopicSearchModal, SpotList } from '../InteractiveDeckView';
import type { DeckViewMode } from '../InteractiveDeckView';
import { DeckPdfViewer } from '../DeckPdfViewer';
import { useGlossary } from '../MedicalGlossaryPopover';
import { HL_COLORS, Highlightable, isPenActive, setHighlighterTool, stopPen, useHighlighterTool, usePenActive } from '../../ui/Highlighter';
import { resetPenDevice, usePenDevice } from '../../ui/penInput';
import { PALETTE_COLORS, SlideDrawingCanvas, setDrawingGlobalState, useDrawingGlobalState } from '../SlideDrawingCanvas';
import { getSlidePdfLocation } from '../../../services/slidePdfMappingService';
import { QuestionFocus, focusMarks } from '../../../services/questionFocus';
import { toast } from '../../ui/Toast';
import { deckName } from '../../../data/deckStore';
import {
  buildSections, buildSteps, DeckKazanim, LessonSection, LessonStep, loadKazanimIndex, matchKazanim, PracticeItem, readDone, writeDone,
} from './lessonModel';
import { stripEmoji, withGlossaryTerms } from './lessonModel';
import { FeedbackItem, FeedbackTarget, listFeedback } from './lessonFeedback';
import { FeedbackDialog, FeedbackFlag, FeedbackProvider, groupFeedback } from './LessonFeedbackUI';
import { Formula, hideTermTip, InfoId, InfoPane, Infographic, infoTabsFor, KeyPoints, LessonTable, PracticeCard, practiceMeta, Prose } from './LessonBlocks';

type Layout = 'A' | 'B';

/**
 * scrollIntoView yerine: yalnız en yakın kayan kapsayıcıyı kaydırır. scrollIntoView arkadaki belgeyi de
 * kaydırıyor, telefonda sabit ders katmanının üstünde boşluk bırakıyordu.
 */
const scrollInto = (el: Element | null | undefined, block: 'start' | 'center' | 'nearest' = 'start', smooth = false) => {
  if (!el) return;
  let box = el.parentElement;
  while (box && !(box.scrollHeight > box.clientHeight + 1 && /(auto|scroll)/.test(getComputedStyle(box).overflowY))) box = box.parentElement;
  if (!box) return;
  const r = el.getBoundingClientRect();
  const b = box.getBoundingClientRect();
  let top = box.scrollTop + (r.top - b.top);
  if (block === 'center') top -= (box.clientHeight - r.height) / 2;
  else if (block === 'nearest') {
    if (r.top >= b.top && r.bottom <= b.bottom) return;
    if (r.bottom > b.bottom) top -= box.clientHeight - r.height;
  } else top -= 8;
  box.scrollTo({ top: Math.max(0, top), behavior: smooth ? 'smooth' : 'auto' });
};

/** Geri bildirim hedefi: adım + öğe türü + sıra */
const fbTarget = (step: LessonStep, kind: string, i: number | string, label: string, hint?: string, location?: string): FeedbackTarget => ({
  key: `${step.number}:${kind}:${String(i).replace(/[^\p{L}\p{N}._-]+/gu, '-').slice(0, 80)}`,
  label,
  slideNumber: step.number,
  hint,
  location: location || label,
});

/**
 * Yönetici bağlantısı: /ogren/<deste>?adim=5&hedef=<targetKey>. İlk açılışta bir kez okunur,
 * adres çubuğu temizlenir; ders o adımda açılır ve öğe vurgulanır.
 */
const readDeepLink = (): { adim?: number; hedef?: string } | null => {
  try {
    const sp = new URLSearchParams(window.location.search);
    const adim = Number(sp.get('adim')) || undefined;
    const hedef = sp.get('hedef') || undefined;
    if (!adim && !hedef) return null;
    sp.delete('adim');
    sp.delete('hedef');
    const q = sp.toString();
    window.history.replaceState(window.history.state, '', window.location.pathname + (q ? `?${q}` : '') + window.location.hash);
    return { adim, hedef };
  } catch {
    return null;
  }
};
type ReadMode = 'paged' | 'scroll';
type Sheet = null | 'notes' | 'ai';

const pref = {
  get<T extends string>(k: string, d: T, ok: readonly T[]): T {
    try {
      const v = localStorage.getItem(k) as T | null;
      return v && ok.includes(v) ? v : d;
    } catch {
      return d;
    }
  },
  set(k: string, v: string) {
    try {
      localStorage.setItem(k, v);
    } catch {
      /* ignore */
    }
  },
};

const useIsPhone = () => {
  const q = '(max-width: 767px)';
  const [m, setM] = useState(() => typeof window !== 'undefined' && window.matchMedia(q).matches);
  useEffect(() => {
    const mq = window.matchMedia(q);
    const on = () => setM(mq.matches);
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, []);
  return m;
};

const isTyping = (t: EventTarget | null) => {
  const el = t as HTMLElement | null;
  return !!el && (el.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName));
};

const practiceOf = (s: LessonStep): PracticeItem[] => [
  ...s.interactives.map((data) => ({ kind: 'ix' as const, data })),
  ...(s.cards.length ? [{ kind: 'cards' as const, cards: s.cards }] : []),
  ...s.questions.map((q) => ({ kind: 'question' as const, q })),
];

/* ---------------------------------------------------------------------------
 * Bölüm listesi: bölüm → adım (konu + alt başlık); ilerleme halkası, arama
 * ------------------------------------------------------------------------- */
const Ring: React.FC<{ pct: number }> = ({ pct }) => (
  <svg className="ls-ring" viewBox="0 0 22 22" aria-hidden>
    <circle cx="11" cy="11" r="8.5" fill="none" stroke="var(--color-line)" strokeWidth="2.5" />
    <circle cx="11" cy="11" r="8.5" fill="none" stroke="var(--color-ok)" strokeWidth="2.5" strokeLinecap="round" strokeDasharray={`${(pct * 53.4).toFixed(1)} 60`} transform="rotate(-90 11 11)" />
  </svg>
);

const Outline: React.FC<{
  steps: LessonStep[];
  sections: LessonSection[];
  current: number;
  done: Set<number>;
  onPick: (i: number) => void;
}> = ({ steps, sections, current, done, onPick }) => {
  const curSec = steps[current]?.section ?? 0;
  const [open, setOpen] = useState<Set<number>>(() => new Set([curSec]));
  const [q, setQ] = useState('');
  useEffect(() => setOpen((o) => (o.has(curSec) ? o : new Set(o).add(curSec))), [curSec]);
  const listRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    scrollInto(listRef.current?.querySelector('[aria-current="step"]'), 'nearest');
  }, [current]);
  const nq = q.trim().toLocaleLowerCase('tr-TR');
  return (
    <div className="ls-outline" ref={listRef}>
      <label className="ls-search">
        <Search aria-hidden />
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Adımlarda ara" aria-label="Adımlarda ara" />
        {q && <button type="button" onClick={() => setQ('')} aria-label="Aramayı temizle"><X aria-hidden /></button>}
      </label>
      {sections.map((sec) => {
        const items = sec.steps.filter((i) => !nq || steps[i].title.toLocaleLowerCase('tr-TR').includes(nq));
        if (!items.length) return null;
        const isOpen = !!nq || open.has(sec.index);
        const pct = sec.steps.filter((i) => done.has(steps[i].number)).length / sec.steps.length;
        return (
          <div key={sec.index} className={`ls-ol-sec ${isOpen ? 'is-open' : ''}`}>
            <button
              type="button"
              className="ls-ol-head"
              aria-expanded={isOpen}
              onClick={() => setOpen((o) => { const n = new Set(o); n.has(sec.index) ? n.delete(sec.index) : n.add(sec.index); return n; })}
            >
              <ChevronDown className="chev" aria-hidden />
              <span className="nm">
                <small>Bölüm {sec.index + 1} · {sec.steps.length} adım</small>
                <span>{sec.name}</span>
              </span>
              <Ring pct={pct} />
            </button>
            <div className="ls-ol-list">
              <div>
                {items.map((i) => {
                  const s = steps[i];
                  const isDone = done.has(s.number);
                  return (
                    <button
                      key={i}
                      type="button"
                      className={`ls-ol-item ${i === current ? 'is-cur' : ''} ${isDone ? 'is-done' : ''}`}
                      aria-current={i === current ? 'step' : undefined}
                      onClick={() => onPick(i)}
                    >
                      <span className="no">{isDone ? <Check aria-label="Tamamlandı" /> : s.number}</span>
                      <span className="tx">
                        {s.topic}
                        {s.subtopic && <em>{s.subtopic}</em>}
                      </span>
                      {s.checkpoint > 0 && <span className="ls-tag is-accent">Tekrar</span>}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

/* ---------------------------------------------------------------------------
 * Adım içeriği (başlık + anlatım + tablo); kalem ve çizim katmanları bu kutuya bağlı
 * ------------------------------------------------------------------------- */
const StepHead: React.FC<{ step: LessonStep; total: number }> = ({ step, total }) => (
  <header className="ls-head" data-fb-key={`${step.number}:text:0`}>
    <div className="ls-eyebrow-row">
      <span>Bölüm {step.section + 1}</span>
      <span className="dot" aria-hidden />
      <span>Adım {step.number} / {total}</span>
      {step.checkpoint > 0 && <span className="ls-tag is-accent">Tekrar {step.checkpoint}</span>}
      {step.badge && !step.checkpoint && <span className="ls-tag is-plain">{step.badge}</span>}
      {step.questions.length > 0 && <span className="ls-tag is-warn">{step.questions.length} soru</span>}
      <FeedbackFlag target={fbTarget(step, 'text', 0, 'Anlatım', step.title, 'Ana içerik › Başlık ve anlatım')} className="ls-head-flag" />
    </div>
    <h1 className="ls-title"><span>{step.title}</span></h1>
    {step.slide.subtitle && <p className="ls-sub">{step.slide.subtitle}</p>}
  </header>
);

const StepBody: React.FC<{ step: LessonStep; deckId: string }> = React.memo(({ step, deckId }) => {
  const showKeys = step.bullets.length > 1 || (!step.narrative.trim() && step.bullets.length > 0);
  return (
    <div className="ls-mark-layer">
      <SlideDrawingCanvas scope={`deck:${deckId}:${step.number}`} />
      <Highlightable scope={`deck:${deckId}:${step.number}`} className="ls-content">
        {step.narrative.trim() && <Prose text={step.narrative} terms={step.terms} />}
        {showKeys && <KeyPoints items={step.bullets} />}
        {step.table && <LessonTable title={step.table.title} headers={step.table.headers || []} rows={step.table.rows} target={fbTarget(step, 'table', 0, step.table.title || 'Tablo', undefined, `Ana içerik › Tablo: ${step.table.title || 'adım tablosu'}`)} />}
        {step.infographic && <Infographic data={step.infographic} />}
        {step.formula && <Formula data={step.formula} />}
      </Highlightable>
    </div>
  );
});

/* ---------------------------------------------------------------------------
 * A: Pekiştir — sekmeli tek kart; her adım kendi ilerlemesini tutar
 * ------------------------------------------------------------------------- */
const practiceTarget = (step: LessonStep, p: PracticeItem, i: number) => {
  const [, label] = practiceMeta(p);
  const location = `Pekiştir › ${label} (${i + 1}. etkinlik)`;
  return p.kind === 'question'
    ? fbTarget(step, 'q', p.q.id, label, p.q.stem.slice(0, 90), location)
    : fbTarget(step, p.kind === 'cards' ? 'cards' : `ix-${p.data.type}`, i, label, undefined, location);
};

const PracticeSet: React.FC<{ step: LessonStep; items: PracticeItem[]; jump?: { to: number; at: number } | null; onAllDone: () => void }> = ({ step, items, jump, onAllDone }) => {
  const [cur, setCur] = useState(0);
  const [doneSet, setDoneSet] = useState<Set<number>>(new Set());
  useEffect(() => {
    if (jump && jump.to >= 0 && jump.to < items.length) setCur(jump.to);
  }, [jump, items.length]);
  if (!items.length) return null;
  const item = items[Math.min(cur, items.length - 1)];
  return (
    <section className="ls-practice" aria-label="Pekiştir">
      <div className="ls-sec-h">Pekiştir <span>{doneSet.size}/{items.length}</span></div>
      {items.length > 1 && (
        <div className="ls-ptabs" role="tablist">
          {items.map((p, i) => {
            const [Icon, label] = practiceMeta(p);
            const isDone = doneSet.has(i);
            return (
              <button key={i} type="button" role="tab" aria-selected={i === cur} className={`ls-ptab ${i === cur ? 'is-on' : ''} ${isDone ? 'is-done' : ''}`} onClick={() => setCur(i)} title={label}>
                {isDone ? <Check aria-hidden /> : <Icon aria-hidden />}
                <span className="lbl">{label}</span>
              </button>
            );
          })}
        </div>
      )}
      <PracticeCard
        key={cur}
        className="ls-enter-up"
        item={item}
        target={practiceTarget(step, item, Math.min(cur, items.length - 1))}
        done={doneSet.has(cur)}
        onDone={() =>
          setDoneSet((d) => {
            if (d.has(cur)) return d;
            const nd = new Set(d).add(cur);
            if (nd.size >= items.length) onAllDone();
            return nd;
          })
        }
      />
    </section>
  );
};

/* ---------------------------------------------------------------------------
 * Ana oynatıcı
 * ------------------------------------------------------------------------- */
export interface LessonPlayerProps {
  deck: InteractiveDeck;
  startAt: number;
  initialViewMode?: DeckViewMode;
  onProgress: (index: number) => void;
  onClose: () => void;
  onExportPdf?: (slideNumber: number) => void;
  focus?: QuestionFocus | null;
  onClearFocus?: () => void;
  onClassic?: () => void;
}

export const LessonPlayer: React.FC<LessonPlayerProps> = ({ deck, startAt, initialViewMode = 'interactive', onProgress, onClose, onExportPdf, focus, onClearFocus, onClassic }) => {
  const steps = useMemo(() => buildSteps(deck), [deck]);
  const sections = useMemo(() => buildSections(steps), [steps]);
  const n = steps.length;
  const deepLink = useRef(readDeepLink());
  const [index, setIndex] = useState(() => {
    const byLink = deepLink.current?.adim ? steps.findIndex((s) => s.number === deepLink.current!.adim) : -1;
    return byLink >= 0 ? byLink : Math.min(Math.max(0, startAt), n - 1);
  });
  const [dir, setDir] = useState(1);
  const { setIsDrawerOpen, glossaryList, setCurrentSlideText } = useGlossary();
  // Adımın kendi terimleri + metinde geçen sözlük terimleri (eski destelerde terim alanı boş)
  const step = useMemo(() => withGlossaryTerms(steps[index], glossaryList as any), [steps, index, glossaryList]);

  const isPhone = useIsPhone();
  const [layoutPref, setLayoutPref] = useState<Layout>(() => pref.get('medsoru_learn_layout', 'A', ['A', 'B'] as const));
  const layout: Layout = isPhone ? 'A' : layoutPref;
  const [viewMode, setViewMode] = useState<DeckViewMode>(initialViewMode);
  const [readMode, setReadMode] = useState<ReadMode>(() => pref.get('medsoru_learn_mode', 'paged', ['paged', 'scroll'] as const));
  const [recall, setRecall] = useState(false);
  const [outlineOpen, setOutlineOpen] = useState(() => pref.get('medsoru_learn_toc', typeof window !== 'undefined' && window.innerWidth >= 1100 ? '1' : '0', ['1', '0'] as const) === '1');
  const [outlineMobile, setOutlineMobile] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const [sheet, setSheet] = useState<Sheet>(null);
  const [searchOpen, setSearchOpen] = useState(false);
  const [dockTab, setDockTab] = useState<InfoId | null>(null);
  const [infoSheet, setInfoSheet] = useState<InfoId | null>(null);
  const [practiceJump, setPracticeJump] = useState<{ to: number; at: number } | null>(null);
  const [sideTab, setSideTab] = useState<'ix' | 'cards' | 'q'>('ix');
  const [done, setDone] = useState<Set<number>>(() => readDone(deck.id));
  const [kazIndex, setKazIndex] = useState<Record<string, DeckKazanim[]>>({});
  const [doneIx, setDoneIx] = useState<Set<string>>(new Set());
  const [feedback, setFeedback] = useState<FeedbackItem[]>([]);
  const [fbOpen, setFbOpen] = useState<FeedbackTarget | null>(null);
  useEffect(() => {
    let alive = true;
    listFeedback(deck.id).then((l) => alive && setFeedback(l)).catch(() => {});
    return () => {
      alive = false;
    };
  }, [deck.id]);
  const fbCtx = useMemo(() => ({ byKey: groupFeedback(feedback), open: (t: FeedbackTarget) => setFbOpen(t) }), [feedback]);

  useEffect(() => pref.set('medsoru_learn_layout', layoutPref), [layoutPref]);
  useEffect(() => pref.set('medsoru_learn_mode', readMode), [readMode]);
  useEffect(() => pref.set('medsoru_learn_toc', outlineOpen ? '1' : '0'), [outlineOpen]);
  useEffect(() => {
    let alive = true;
    loadKazanimIndex().then((m) => alive && setKazIndex(m));
    return () => {
      alive = false;
    };
  }, []);

  const rootRef = useRef<HTMLDivElement>(null);
  const mainRef = useRef<HTMLDivElement>(null);
  const stageRef = useRef<HTMLDivElement>(null);
  const toolsRef = useRef<HTMLDivElement>(null);
  const flowRefs = useRef<(HTMLElement | null)[]>([]);
  const programmatic = useRef(false);
  const penOn = usePenActive();
  const drawState = useDrawingGlobalState();
  const drawMode = drawState.activeMode;
  const hlTool = useHighlighterTool();
  const penDevice = usePenDevice();
  const marking = penOn || drawMode !== 'none';

  const pdfLoc = useMemo(() => getSlidePdfLocation(deck.id, step.slide.slideNumber, step.slide, n), [deck.id, step, n]);
  const [pdfPage, setPdfPage] = useState(pdfLoc.primaryPage);
  useEffect(() => setPdfPage(pdfLoc.primaryPage), [pdfLoc.primaryPage]);
  const kaz = useMemo(() => matchKazanim(step, kazIndex[deck.id], pdfLoc.primaryPage, `${deck.title} ${deck.discipline || ''}`), [step, kazIndex, deck.id, deck.title, deck.discipline, pdfLoc.primaryPage]);
  const practice = useMemo(() => practiceOf(step), [step]);
  const infoTabs = useMemo(() => infoTabsFor(step, kaz), [step, kaz]);

  /* --- yaşam döngüsü --- */
  useEffect(() => {
    const prev = document.body.style.overflow;
    const prevHtml = document.documentElement.style.overflow;
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';
    rootRef.current?.focus({ preventScroll: true });
    return () => {
      document.body.style.overflow = prev;
      document.documentElement.style.overflow = prevHtml;
      hideTermTip();
      if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    };
  }, []);
  useEffect(() => onProgress(index), [index]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    setPracticeJump(null);
    setInfoSheet(null);
    setDoneIx(new Set());
    hideTermTip();
    if (readMode === 'paged' || layout === 'B') mainRef.current?.scrollTo({ top: 0 });
    rootRef.current?.querySelectorAll('.ms-shown').forEach((el) => el.classList.remove('ms-shown'));
  }, [index]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (!setCurrentSlideText) return;
    setCurrentSlideText([step.title, step.slide.subtitle, step.narrative, ...step.bullets.map((b) => `${b.title}: ${b.desc}`), ...step.spots, step.table?.title, step.table?.rows.map((r) => r.join(' ')).join('\n')].filter(Boolean).join('\n'));
  }, [step, setCurrentSlideText]);

  /* --- soru odağı: bağlı slaytta sorunun ifadeleri ve doğru şık işaretlenir (CSS Highlight API) --- */
  const focusOnStep = Boolean(focus && (!focus.slideNumber || focus.slideNumber === step.slide.slideNumber));
  const [focusHits, setFocusHits] = useState<number | null>(null);
  useEffect(() => {
    const reg = (globalThis as any).CSS?.highlights;
    const HL = (globalThis as any).Highlight;
    if (!reg || !HL) return;
    reg.delete('ms-q-focus');
    reg.delete('ms-q-answer');
    setFocusHits(null);
    if (!focus || !focusOnStep) return;
    const t = window.setTimeout(() => {
      const root = stageRef.current;
      if (!root) return;
      const q: Range[] = [];
      const a: Range[] = [];
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      for (let node = walker.nextNode(); node; node = walker.nextNode()) {
        const text = node.nodeValue || '';
        if (text.trim().length < 3 || node.parentElement?.closest('button, [aria-hidden="true"]')) continue;
        const marks = focusMarks(text, focus.terms, focus.answerTerms);
        let start = -1;
        for (let i = 0; i <= text.length; i++) {
          const v = i < text.length ? marks[i] : 0;
          if (start >= 0 && v !== marks[start]) {
            const r = document.createRange();
            r.setStart(node, start);
            r.setEnd(node, i);
            (marks[start] === 2 ? a : q).push(r);
            start = -1;
          }
          if (start < 0 && v) start = i;
        }
      }
      if (q.length) reg.set('ms-q-focus', new HL(...q));
      if (a.length) reg.set('ms-q-answer', new HL(...a));
      setFocusHits(q.length + a.length);
    }, 250);
    return () => {
      window.clearTimeout(t);
      reg.delete('ms-q-focus');
      reg.delete('ms-q-answer');
    };
  }, [focus, focusOnStep, index, viewMode, layout, readMode]);

  /* --- gezinme --- */
  const markDone = useCallback(
    (num: number) =>
      setDone((d) => {
        if (d.has(num)) return d;
        const nd = new Set(d).add(num);
        writeDone(deck.id, nd);
        return nd;
      }),
    [deck.id]
  );
  const goTo = useCallback(
    (i: number) => {
      const t = Math.max(0, Math.min(n - 1, i));
      setDir(t >= index ? 1 : -1);
      setIndex(t);
      setOutlineMobile(false);
      if (layout === 'A' && readMode === 'scroll' && viewMode === 'interactive') {
        programmatic.current = true;
        scrollInto(flowRefs.current[t], 'start', true);
        window.setTimeout(() => (programmatic.current = false), 700);
      }
    },
    [n, index, layout, readMode, viewMode]
  );
  const next = () => {
    if (index < n - 1) {
      markDone(step.number);
      goTo(index + 1);
    }
  };
  const prev = () => index > 0 && goTo(index - 1);

  // Kaydırarak okuma: üst üçte birden geçen adım güncel adım olur
  useEffect(() => {
    const sc = mainRef.current;
    if (!sc || layout !== 'A' || readMode !== 'scroll' || viewMode !== 'interactive') return;
    requestAnimationFrame(() => scrollInto(flowRefs.current[index], 'start'));
    const onScroll = () => {
      if (programmatic.current) return;
      const probe = sc.scrollTop + sc.clientHeight * 0.3;
      let i = 0;
      flowRefs.current.forEach((el, k) => {
        if (el && el.offsetTop <= probe) i = k;
      });
      setIndex((p) => (p === i ? p : i));
    };
    sc.addEventListener('scroll', onScroll, { passive: true });
    return () => sc.removeEventListener('scroll', onScroll);
  }, [layout, readMode, viewMode]); // eslint-disable-line react-hooks/exhaustive-deps

  /* --- tam ekran (destek yoksa odak modu) --- */
  const [isFs, setIsFs] = useState(false);
  const [immersive, setImmersive] = useState(false);
  useEffect(() => {
    const on = () => {
      const fs = !!(document.fullscreenElement || (document as any).webkitFullscreenElement);
      setIsFs(fs);
      if (fs) setImmersive(false);
    };
    document.addEventListener('fullscreenchange', on);
    document.addEventListener('webkitfullscreenchange', on);
    return () => {
      document.removeEventListener('fullscreenchange', on);
      document.removeEventListener('webkitfullscreenchange', on);
    };
  }, []);
  // Tam ekran tüm ekranı kaplar: belge kökü tam ekrana alınır (ders katmanı sabit konumlu, ekranı doldurur).
  // API yoksa (iPhone Safari) ya da istek reddedilir/yanıtsız kalırsa yalnız arayüzü gizleyen odak moduna geçilir.
  const toggleFullscreen = () => {
    setToolsOpen(false);
    const d = document as any;
    if (immersive) return setImmersive(false);
    if (d.fullscreenElement || d.webkitFullscreenElement) {
      (d.exitFullscreen || d.webkitExitFullscreen)?.call(d)?.catch?.(() => {});
      return;
    }
    const el: any = document.documentElement;
    const req = el.requestFullscreen || el.webkitRequestFullscreen;
    if (!req) {
      setImmersive(true);
      if (/iPhone|iPod/.test(navigator.userAgent)) toast.info('iPhone tam ekranı desteklemiyor', 'Arayüz gizlendi. Gerçek tam ekran için Safari > Paylaş > Ana Ekrana Ekle ile uygulamayı aç.');
      return;
    }
    let settled = false;
    try {
      const p = req.call(el, { navigationUI: 'hide' });
      p?.then?.(() => (settled = true), () => {
        settled = true;
        setImmersive(true);
      });
    } catch {
      setImmersive(true);
      return;
    }
    window.setTimeout(() => {
      if (!settled && !d.fullscreenElement && !d.webkitFullscreenElement) setImmersive(true);
    }, 1500);
  };
  const fsOn = isFs || immersive;

  /* --- klavye --- */
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (isTyping(e.target)) return;
      // Ders dışındaki bir pencere (PDF oluştur, sözlük vb.) açıkken kısayollar o pencereye aittir
      const foreign = [...document.querySelectorAll<HTMLElement>('[role="dialog"]')].some((d) => d !== rootRef.current && !rootRef.current?.contains(d) && d.getClientRects().length > 0);
      if (foreign || fbOpen) return;
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setSearchOpen((v) => !v);
        return;
      }
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === '/' && !searchOpen) {
        e.preventDefault();
        setSearchOpen(true);
      } else if (e.key === 'ArrowRight' || e.key === 'PageDown') {
        e.preventDefault();
        next();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prev();
      } else if (e.key === 'Home') goTo(0);
      else if (e.key === 'End') goTo(n - 1);
      else if (e.key.toLowerCase() === 'f') toggleFullscreen();
      else if (e.key === 'Escape') {
        if (searchOpen) setSearchOpen(false);
        else if (toolsOpen) setToolsOpen(false);
        else if (sheet) setSheet(null);
        else if (infoSheet) setInfoSheet(null);
        else if (outlineMobile) setOutlineMobile(false);
        else if (immersive) setImmersive(false);
        else if (!document.fullscreenElement) onClose();
      }
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  });

  // Araçlar menüsü dışına tıklayınca kapanır
  useEffect(() => {
    if (!toolsOpen) return;
    const on = (e: PointerEvent) => {
      if (toolsRef.current && !toolsRef.current.contains(e.target as Node) && !(e.target as HTMLElement).closest?.('[data-ls-keep]')) setToolsOpen(false);
    };
    document.addEventListener('pointerdown', on);
    return () => document.removeEventListener('pointerdown', on);
  }, [toolsOpen]);

  /* --- kaydırma hareketi (sayfa sayfa): kalem/çizim açıkken ya da metin seçiliyken çevirmez --- */
  const touch = useRef<{ x: number; y: number; at: number } | null>(null);
  const onTouchStart = (e: React.TouchEvent) => {
    const t = e.touches[0];
    touch.current = e.touches.length === 1 && (t as any).touchType !== 'stylus' ? { x: t.clientX, y: t.clientY, at: Date.now() } : null;
  };
  const onTouchEnd = (e: React.TouchEvent) => {
    const s = touch.current;
    touch.current = null;
    if (!s || (layout === 'A' && readMode === 'scroll') || isPenActive() || marking || Date.now() - s.at > 450) return;
    if ((e.target as HTMLElement).closest('.ls-ix, .ls-table, .ls-dock, input')) return;
    const sel = window.getSelection();
    if (sel && !sel.isCollapsed && sel.toString().trim()) return;
    const t = e.changedTouches[0];
    const dx = t.clientX - s.x;
    const dy = t.clientY - s.y;
    if (Math.abs(dx) > 90 && Math.abs(dx) > Math.abs(dy) * 2) (dx < 0 ? next : prev)();
  };

  const openPdf = (page?: number) => {
    setPdfPage(page ?? pdfLoc.primaryPage);
    setViewMode('split');
    setInfoSheet(null);
    setDockTab(null);
  };

  const ixKey = (p: PracticeItem, i: number) => `${i}:${p.kind}`;
  const onIxDone = (key: string, all: number) =>
    setDoneIx((d) => {
      if (d.has(key)) return d;
      const nd = new Set(d).add(key);
      if (nd.size >= all) markDone(step.number);
      return nd;
    });

  /* ---------------- parçalar ---------------- */
  const section = sections[step.section];
  const secPos = section ? section.steps.indexOf(index) : 0;

  /** Araçlar menüsünden seçilen her işlev menüyü kapatır */
  const pickTool = (fn: () => void) => {
    fn();
    setToolsOpen(false);
  };

  const topBar = (
    <header className={`ls-top ${immersive ? 'is-hidden' : ''}`}>
      <button type="button" className="ls-btn is-icon is-ghost" onClick={onClose} aria-label="Dersi kapat" title="Kapat (Esc)"><X aria-hidden /></button>
      <button
        type="button"
        className={`ls-btn is-icon is-ghost ${(isPhone ? outlineMobile : layout === 'A' ? outlineOpen : outlineMobile) ? 'is-on' : ''}`}
        onClick={() => (layout === 'A' && !isPhone && viewMode === 'interactive' ? setOutlineOpen((v) => !v) : setOutlineMobile((v) => !v))}
        aria-label="Bölümler"
        title="Bölümler"
      >
        <ListTree aria-hidden />
      </button>
      <div className="ls-deck">
        <small>{deck.discipline}{deck.instructor ? ` · ${deck.instructor}` : ''}</small>
        <b title={deck.title}>{deckName(deck)}</b>
      </div>
      {layout === 'B' && !isPhone && (
        <div className="ls-segbar" aria-label="Bölüm ilerlemesi">
          {sections.map((sec) => {
            const pct = sec.steps.filter((i) => done.has(steps[i].number)).length / sec.steps.length;
            return (
              <button
                key={sec.index}
                type="button"
                className={sec.index === step.section ? 'is-cur' : ''}
                style={{ flexGrow: sec.steps.length }}
                onClick={() => goTo(sec.steps[0])}
                title={`Bölüm ${sec.index + 1}: ${sec.name}`}
                aria-label={`Bölüm ${sec.index + 1}: ${sec.name}`}
              >
                <i style={{ width: `${Math.max(pct * 100, sec.index === step.section ? 8 : 0)}%` }} />
              </button>
            );
          })}
        </div>
      )}
      <span className="ls-count" aria-live="polite">{index + 1} / {n}</span>
      <button type="button" className="ls-btn is-icon is-ghost" onClick={() => setSearchOpen(true)} aria-label="Derste ara" title="Derste ara (Ctrl+K)"><Search aria-hidden /></button>
      <button type="button" className="ls-btn is-icon is-ghost ls-hide-phone" onClick={prev} disabled={index === 0} aria-label="Önceki adım" title="Önceki (←)"><ChevronLeft aria-hidden /></button>
      <button type="button" className="ls-btn is-icon is-ghost ls-hide-phone" onClick={next} disabled={index >= n - 1} aria-label="Sonraki adım" title="Sonraki (→)"><ChevronRight aria-hidden /></button>
      <div className="ls-tools" ref={toolsRef}>
        <button type="button" className={`ls-btn ${toolsOpen ? 'is-on' : ''}`} aria-expanded={toolsOpen} aria-haspopup="true" onClick={() => setToolsOpen((v) => !v)}>
          <MoreHorizontal aria-hidden /> <span className="ls-hide-phone">Araçlar</span>
        </button>
        {toolsOpen && (
          <div className="ls-tools-pop" role="menu" aria-label="Araçlar">
            {!isPhone && (
              <div className="ls-tools-grp">
                <span className="ls-eyebrow">Düzen</span>
                <div className="ls-seg" role="radiogroup" aria-label="Düzen">
                  <button type="button" role="radio" aria-checked={layout === 'A'} onClick={() => pickTool(() => setLayoutPref('A'))}><LayoutPanelLeft aria-hidden /> Akış</button>
                  <button type="button" role="radio" aria-checked={layout === 'B'} onClick={() => pickTool(() => setLayoutPref('B'))}><PanelsTopLeft aria-hidden /> Stüdyo</button>
                </div>
              </div>
            )}
            <div className="ls-tools-grp">
              <span className="ls-eyebrow">Görünüm</span>
              <div className="ls-seg" role="radiogroup" aria-label="Görünüm">
                <button type="button" role="radio" aria-checked={viewMode === 'interactive'} onClick={() => pickTool(() => setViewMode('interactive'))}><GalleryHorizontal aria-hidden /> Ders</button>
                <button type="button" role="radio" aria-checked={viewMode === 'split'} onClick={() => pickTool(() => setViewMode('split'))}><Columns aria-hidden /> Yan yana</button>
                <button type="button" role="radio" aria-checked={viewMode === 'pdf'} onClick={() => pickTool(() => setViewMode('pdf'))}><FileText aria-hidden /> PDF</button>
              </div>
              {layout === 'A' && viewMode === 'interactive' && (
                <div className="ls-seg" role="radiogroup" aria-label="Okuma">
                  <button type="button" role="radio" aria-checked={readMode === 'paged'} onClick={() => pickTool(() => setReadMode('paged'))}><GalleryHorizontal aria-hidden /> Sayfa sayfa</button>
                  <button type="button" role="radio" aria-checked={readMode === 'scroll'} onClick={() => pickTool(() => setReadMode('scroll'))}><Rows3 aria-hidden /> Kaydırarak</button>
                </div>
              )}
            </div>
            <div className="ls-tools-grp">
              <span className="ls-eyebrow">Çalışma</span>
              <button type="button" role="menuitemcheckbox" aria-checked={recall} className={`ls-tools-item ${recall ? 'is-on' : ''}`} onClick={() => pickTool(() => setRecall((v) => !v))}>
                <EyeOff aria-hidden /> <span>Hatırlama modu<small>Kalın ifadeler örtülür, dokununca açılır</small></span>
              </button>
              <button type="button" role="menuitemcheckbox" aria-checked={penOn} className={`ls-tools-item ${penOn ? 'is-on' : ''}`} onClick={() => pickTool(() => { setDrawingGlobalState({ activeMode: 'none' }); setHighlighterTool({ active: !penOn, eraser: false }); })}>
                <Highlighter aria-hidden /> <span>Fosforlu kalem (marker)<small>Metni renkli işaretle; renkler ekranın tepesinde</small></span>
              </button>
              <button type="button" role="menuitemcheckbox" aria-checked={drawMode !== 'none'} className={`ls-tools-item ${drawMode !== 'none' ? 'is-on' : ''}`} onClick={() => pickTool(() => { stopPen(); setDrawingGlobalState({ activeMode: drawMode !== 'none' ? 'none' : 'pen' }); })}>
                <PenLine aria-hidden /> <span>Kalem (çizim)<small>Sayfanın üstüne serbest çiz; renk ve kalınlık tepede</small></span>
              </button>
              <button type="button" role="menuitem" className="ls-tools-item" onClick={() => { setSheet('notes'); setToolsOpen(false); }}>
                <NotebookText aria-hidden /> <span>Ders notları<small>Dersin özeti ve en çok sorulan spotlar</small></span>
              </button>
              <button type="button" role="menuitem" className="ls-tools-item" onClick={() => { setSheet('ai'); setToolsOpen(false); }}>
                <MessageCircleQuestion aria-hidden /> <span>Asistana sor<small>Bu adım hakkında soru sor</small></span>
              </button>
              <button type="button" role="menuitem" className="ls-tools-item" onClick={() => { setIsDrawerOpen(true); setToolsOpen(false); }}>
                <BookOpen aria-hidden /> <span>Tıbbi sözlük<small>{glossaryList.length} terim</small></span>
              </button>
            </div>
            <div className="ls-tools-grp">
              <span className="ls-eyebrow">Diğer</span>
              <button type="button" role="menuitem" className="ls-tools-item" onClick={toggleFullscreen}>
                {fsOn ? <Minimize2 aria-hidden /> : <Maximize2 aria-hidden />} <span>{fsOn ? 'Tam ekrandan çık' : 'Tam ekran'}<small>Kısayol: F</small></span>
              </button>
              {onExportPdf && (
                <button type="button" role="menuitem" className="ls-tools-item" onClick={() => { setToolsOpen(false); if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {}); onExportPdf(step.slide.slideNumber); }}>
                  <FileDown aria-hidden /> <span>Bu adımı PDF yap</span>
                </button>
              )}
              {onClassic && (
                <button type="button" role="menuitem" className="ls-tools-item" onClick={() => { setToolsOpen(false); onClassic(); }}>
                  <History aria-hidden /> <span>Klasik görünüm<small>Önceki slayt ekranı</small></span>
                </button>
              )}
            </div>
          </div>
        )}
      </div>
      <button type="button" className="ls-btn is-icon is-ghost ls-hide-phone" onClick={toggleFullscreen} aria-label={fsOn ? 'Tam ekrandan çık' : 'Tam ekran'} title="Tam ekran (F)">
        {fsOn ? <Minimize2 aria-hidden /> : <Maximize2 aria-hidden />}
      </button>
      <div className="ls-prog" aria-hidden><i style={{ width: `${((index + 1) / n) * 100}%` }} /></div>
    </header>
  );

  const markingBar = marking && (
    <div role="toolbar" aria-label={penOn ? 'Fosforlu kalem' : 'Kalem'} className="ls-floatbar" data-ls-keep>
      <span className="ls-floatbar-title">{penOn ? <Highlighter aria-hidden /> : <PenLine aria-hidden />}{penOn ? 'Marker' : 'Kalem'}</span>
      {penOn ? (
        <span className="ls-swatches" role="radiogroup" aria-label="Renk">
          {HL_COLORS.map((c) => (
            <button key={c.id} type="button" role="radio" aria-checked={!hlTool.eraser && hlTool.color === c.id} aria-label={c.label} title={c.label} style={{ ['--sw' as string]: c.swatch }} onClick={() => setHighlighterTool({ color: c.id, eraser: false })} />
          ))}
          <button type="button" className={`ls-fb-tool ${hlTool.eraser ? 'is-on' : ''}`} aria-pressed={hlTool.eraser} onClick={() => setHighlighterTool({ eraser: !hlTool.eraser })} title="Silgi: işarete dokun"><Eraser aria-hidden /></button>
        </span>
      ) : (
        <>
          <span className="ls-seg is-mini" role="radiogroup" aria-label="Çizim aracı">
            {([['pen', 'Kalem'], ['highlighter', 'Marker'], ['eraser', 'Silgi']] as const).map(([m, l]) => (
              <button key={m} type="button" role="radio" aria-checked={drawState.activeMode === m} onClick={() => setDrawingGlobalState({ activeMode: m })}>{l}</button>
            ))}
          </span>
          {drawState.activeMode !== 'eraser' && (
            <span className="ls-swatches" role="radiogroup" aria-label="Renk">
              {PALETTE_COLORS.map((c) => (
                <button key={c.id} type="button" role="radio" aria-checked={drawState.color === c.hex} aria-label={c.label} title={c.label} style={{ ['--sw' as string]: c.hex }} onClick={() => setDrawingGlobalState({ color: c.hex })} />
              ))}
            </span>
          )}
          {drawState.activeMode === 'pen' && (
            <span className="ls-sizes" role="radiogroup" aria-label="Kalınlık">
              {[2, 4, 7].map((z) => (
                <button key={z} type="button" role="radio" aria-checked={drawState.penSize === z} aria-label={`${z} px`} onClick={() => setDrawingGlobalState({ penSize: z })}><i style={{ width: z + 4, height: z + 4 }} /></button>
              ))}
            </span>
          )}
        </>
      )}
      <span className={`ls-input-chip ${penDevice ? 'is-pen' : ''}`} title={penDevice ? 'Kalem algılandı: yalnız kalem yazar, parmak sayfayı kaydırır' : 'Parmakla yazılıyor; kalemle dokunursan otomatik algılanır'}>
        {penDevice ? <><PenLine aria-hidden /> Kalem algılandı · parmak kaydırır</> : <><Hand aria-hidden /> Parmakla yazma</>}
        {penDevice && <button type="button" onClick={resetPenDevice} title="Parmakla da yazmaya dön">Parmakla yaz</button>}
      </span>
      <button type="button" className="ls-floatbar-x" aria-label="İşaretlemeyi kapat" onClick={() => { stopPen(); setDrawingGlobalState({ activeMode: 'none' }); }}><X aria-hidden /></button>
    </div>
  );

  const focusBand = focus && focusOnStep && (
    <div className="ms-qfocus-band ms-pop-in" role="status">
      <span className="ms-qfocus-dot is-q" aria-hidden /> <span className="truncate">{focus.label}</span>
      {focus.answerKey && <span className="ms-qfocus-ans"><span className="ms-qfocus-dot is-a" aria-hidden /> Doğru şık {focus.answerKey}</span>}
      {focusHits === 0 && <span className="text-ink-3 hidden sm:inline">· slayt metninde birebir geçmiyor</span>}
      {onClearFocus && <button type="button" onClick={onClearFocus} className="ms-qfocus-x" aria-label="İşaretlemeyi kaldır"><X className="w-3.5 h-3.5" /></button>}
    </div>
  );

  /* --- derin bağlantı hedefi: gerekli sekme/bölmeyi aç, öğeye kaydır, vurgula --- */
  useEffect(() => {
    const hedef = deepLink.current?.hedef;
    if (!hedef) return;
    deepLink.current = null;
    const kind = hedef.split(':')[1] || '';
    const infoOf: Record<string, InfoId> = { spot: 'spot', term: 'terms', teacher: 'teacher', important: 'teacher', tip: 'teacher' };
    if (infoOf[kind]) {
      if (layout === 'A' || viewMode !== 'interactive') setDockTab(infoOf[kind]);
      else setInfoSheet(infoOf[kind]);
    } else if (kind === 'q' || kind === 'cards' || kind.startsWith('ix-')) {
      const k = practice.findIndex((p, i) => practiceTarget(step, p, i).key === hedef);
      if (layout === 'B' && viewMode === 'interactive') setSideTab(kind === 'q' ? 'q' : kind === 'cards' ? 'cards' : 'ix');
      else if (k >= 0) setPracticeJump({ to: k, at: Date.now() });
    }
    let tries = 0;
    const find = () => {
      const el = rootRef.current?.querySelector<HTMLElement>(`[data-fb-key="${CSS.escape(hedef)}"]`);
      if (!el) {
        if (++tries < 12) window.setTimeout(find, 250);
        else toast.info('Bildirilen öğe bulunamadı', 'İçerik değişmiş olabilir; ilgili adım açıldı.');
        return;
      }
      scrollInto(el, 'center', true);
      el.classList.remove('ls-target-flash');
      void el.offsetWidth;
      el.classList.add('ls-target-flash');
      window.setTimeout(() => el.classList.remove('ls-target-flash'), 3200);
    };
    window.setTimeout(find, 500);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  /** Bilgi bölmesindeki bir sorunun "Çöz"ü: bu adımın Pekiştir bölümünde tam o soruyu açar */
  const solveQuestion = (qi: number) => {
    const q = step.questions[qi];
    if (!q) return;
    setDockTab(null);
    setInfoSheet(null);
    const scroll = (sel: string) => window.setTimeout(() => scrollInto(rootRef.current?.querySelector(sel), 'start', true), 80);
    if (layout === 'B' && viewMode === 'interactive') {
      setSideTab('q');
      scroll(`.ls-B-side [data-q="${CSS.escape(q.id)}"]`);
      return;
    }
    const k = practice.findIndex((p) => p.kind === 'question' && p.q.id === q.id);
    if (k >= 0) setPracticeJump({ to: k, at: Date.now() });
    scroll(`[data-step="${index}"] .ls-practice`);
  };

  const infoPaneProps = { step, kaz, deckPastCount: deck.matchedPastQuestionsCount, citation: pdfLoc.citation, page: pdfLoc.primaryPage, onOpenPdf: () => openPdf() };

  /* ---- A: alt bilgi çekmecesi ---- */
  const Dock = infoTabs.length > 0 && (
    <div className={`ls-dock ${dockTab ? 'is-open' : ''}`}>
      <div className="ls-dock-in">
        <div className="ls-dock-bar" role="tablist" aria-label="Bilgi">
          {infoTabs.map((t) => (
            <button
              key={t.id}
              type="button"
              role="tab"
              aria-selected={dockTab === t.id}
              className={`ls-dock-tab ${dockTab === t.id ? 'is-on' : ''} ${t.hot ? 'is-hot' : ''}`}
              onClick={() => setDockTab((v) => (v === t.id ? null : t.id))}
            >
              <t.icon aria-hidden />
              <span className="lbl">{t.label}</span>
              {t.id !== 'src' && <span className="c">{t.count}</span>}
            </button>
          ))}
          <span className="sp" />
          <button type="button" className="ls-btn is-icon is-ghost" onClick={() => setDockTab((v) => (v ? null : infoTabs[0].id))} aria-label={dockTab ? 'Bilgi bölmesini kapat' : 'Bilgi bölmesini aç'}>
            {dockTab ? <ChevronDown aria-hidden /> : <Info aria-hidden />}
          </button>
        </div>
        <div className="ls-dock-body">
          <div>
            <div className="ls-dock-pane">
              {dockTab && <InfoPane id={dockTab} {...infoPaneProps} onPractice={solveQuestion} />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  /* ---- A: sade gezinme satırı ---- */
  const nextStep = steps[index + 1];
  const FlowNav = (
    <nav className="ls-flownav" aria-label="Adım gezinme">
      <button type="button" className="ls-btn is-icon" onClick={prev} disabled={index === 0} aria-label="Önceki adım"><ChevronLeft aria-hidden /></button>
      <span className={`ls-stepdots ${(section?.steps.length ?? 0) > 7 ? 'is-many' : ''}`} aria-label={`Bölüm ${step.section + 1}, adım ${secPos + 1} / ${section?.steps.length ?? 1}`}>
        {section?.steps.length <= 16 && section.steps.map((i) => <button key={i} type="button" className={`${i === index ? 'is-on' : ''} ${done.has(steps[i].number) ? 'is-done' : ''}`} onClick={() => goTo(i)} aria-label={`Adım ${steps[i].number}`} />)}
        <small className={section?.steps.length <= 16 ? 'alt' : ''}>{secPos + 1} / {section?.steps.length}</small>
      </span>
      {nextStep ? (
        <button type="button" className="ls-next" onClick={next} title={nextStep.title}>
          <span className="lbl"><small>Sonraki</small>{nextStep.topic}</span>
          <ChevronRight aria-hidden />
        </button>
      ) : (
        <button type="button" className="ls-next is-end" onClick={() => { markDone(step.number); toast.success('Ders tamamlandı', `${deckName(deck)} bitti.`); }}>
          <span className="lbl"><small>Son adım</small>Dersi bitir</span>
          <Check aria-hidden />
        </button>
      )}
    </nav>
  );

  const FlowArticle = (s: LessonStep, withPractice: boolean) => (
    <>
      <StepHead step={s} total={n} />
      <StepBody step={s} deckId={deck.id} />
      {withPractice && <PracticeSet step={s} items={s.index === index ? practice : practiceOf(s)} jump={s.index === index ? practiceJump : null} onAllDone={() => markDone(s.number)} />}
    </>
  );

  /* ---- B: sağ panel ---- */
  const bIx = practice.filter((p) => p.kind === 'ix');
  const bCards = practice.filter((p) => p.kind === 'cards');
  const bQs = practice.filter((p) => p.kind === 'question');
  const bTabs = ([['ix', 'Pekiştir', bIx], ['cards', 'Kartlar', bCards], ['q', 'Sorular', bQs]] as const).filter(([, , l]) => l.length > 0);
  const bActive = bTabs.find(([id]) => id === sideTab)?.[0] ?? bTabs[0]?.[0];
  const bList = bTabs.find(([id]) => id === bActive)?.[2] ?? [];

  const stage =
    viewMode === 'pdf' ? (
      <div className="ls-pdf">
        <DeckPdfViewer deck={deck} currentSlideNumber={step.slide.slideNumber} currentSlide={step.slide} targetPage={pdfPage} targetPageRange={step.slide.sourcePageRange} onToggleSplitView={() => setViewMode('split')} onPageChange={setPdfPage} />
      </div>
    ) : viewMode === 'split' ? (
      <div className="ls-split">
        <div className="ls-split-l" ref={mainRef} onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
          <article className={`ls-col ${dir > 0 ? 'ls-enter-r' : 'ls-enter-l'}`} key={index} data-step={index}>
            {FlowArticle(step, true)}
            {FlowNav}
          </article>
        </div>
        <div className="ls-split-r">
          <DeckPdfViewer deck={deck} currentSlideNumber={step.slide.slideNumber} currentSlide={step.slide} targetPage={pdfPage} targetPageRange={step.slide.sourcePageRange} isSplitView onToggleSplitView={() => setViewMode('interactive')} onPageChange={setPdfPage} />
        </div>
      </div>
    ) : layout === 'A' ? (
      <div className={`ls-A ${outlineOpen && !isPhone ? 'has-outline' : ''}`}>
        {outlineOpen && !isPhone && (
          <nav className="ls-A-outline" aria-label="Ders bölümleri">
            <Outline steps={steps} sections={sections} current={index} done={done} onPick={goTo} />
          </nav>
        )}
        <main className="ls-A-main" ref={mainRef} onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
          {readMode === 'scroll' ? (
            <div className="ls-col is-flow">
              {steps.map((s, i) => (
                <article key={i} ref={(el) => { flowRefs.current[i] = el; }} className="ls-flow-step" data-step={i} aria-label={`Adım ${s.number}`}>
                  {FlowArticle(withGlossaryTerms(s, glossaryList as any), true)}
                </article>
              ))}
            </div>
          ) : (
            <article className={`ls-col ${dir > 0 ? 'ls-enter-r' : 'ls-enter-l'}`} key={index} data-step={index}>
              {FlowArticle(step, true)}
              {FlowNav}
            </article>
          )}
          {Dock}
        </main>
      </div>
    ) : (
      <div className="ls-B">
        <div className="ls-B-stage">
          <article className={`ls-B-card ${dir > 0 ? 'ls-enter-r' : 'ls-enter-l'}`} key={index}>
            <div className="ls-B-head"><StepHead step={step} total={n} /></div>
            <div className="ls-B-body" ref={mainRef} onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
              <StepBody step={step} deckId={deck.id} />
            </div>
            <footer className="ls-B-foot">
              <button type="button" className="ls-btn" onClick={prev} disabled={index === 0}><ChevronLeft aria-hidden /> Önceki</button>
              <span className="ttl">{section ? `Bölüm ${step.section + 1} · ${section.name}` : ''}</span>
              <button type="button" className="ls-btn is-primary" onClick={next} disabled={index >= n - 1}>Sonraki <ChevronRight aria-hidden /></button>
            </footer>
          </article>
        </div>
        {bTabs.length > 0 && (
          <aside className="ls-B-side" aria-label="Pekiştir">
            <div className="ls-B-tabs" role="tablist">
              {bTabs.map(([id, label, list]) => (
                <button key={id} type="button" role="tab" aria-selected={bActive === id} className={bActive === id ? 'is-on' : ''} onClick={() => setSideTab(id)}>
                  {label} <span className="c">{list.length}</span>
                </button>
              ))}
            </div>
            <div className="ls-B-side-body" key={`${index}-${bActive}`}>
              {bList.map((p) => {
                const qAnchor = p.kind === 'question' ? p.q.id : undefined;
                const i = practice.indexOf(p);
                const k = ixKey(p, i);
                return <div key={k} data-q={qAnchor} className="ls-anchor"><PracticeCard item={p} target={practiceTarget(step, p, i)} done={doneIx.has(k)} onDone={() => onIxDone(k, practice.length)} className="ls-enter-up" style={{ animationDelay: `${Math.min(i, 6) * 50}ms` }} /></div>;
              })}
            </div>
          </aside>
        )}
        <div className="ls-B-strip">
          {infoTabs.filter((t) => t.id !== 'q').slice(0, 4).map((t) => {
            const first =
              t.id === 'spot' ? step.spots[0] : t.id === 'terms' ? step.terms.map((x) => x.term).join(', ') : t.id === 'kaz' ? kaz[0]?.m : t.id === 'teacher' ? step.teacher?.quote || step.important || step.examTip : pdfLoc.citation;
            return (
              <button key={t.id} type="button" className={`ls-tile ${infoSheet === t.id ? 'is-on' : ''}`} onClick={() => setInfoSheet((v) => (v === t.id ? null : t.id))} aria-expanded={infoSheet === t.id}>
                <span className={`ico is-${t.id === 'spot' ? 'warn' : t.id === 'kaz' ? 'ok' : t.id === 'src' ? 'plain' : 'accent'}`}><t.icon aria-hidden /></span>
                <span className="tx"><b>{t.label}{t.id !== 'src' ? ` · ${t.count}` : ''}</b><small>{stripEmoji(String(first || '')).replace(/^\[?[A-ZÇĞİÖŞÜ ]{4,}\]?\s*:?\s*/, '')}</small></span>
              </button>
            );
          })}
        </div>
        {infoSheet && (
          <div className="ls-infosheet" role="dialog" aria-label="Bilgi">
            <div className="ls-infosheet-h">
              {(() => { const t = infoTabs.find((x) => x.id === infoSheet); return t ? <><t.icon aria-hidden /><span>{t.label}</span></> : null; })()}
              <span className="sp" />
              <button type="button" className="ls-btn is-icon is-ghost" onClick={() => setInfoSheet(null)} aria-label="Kapat"><X aria-hidden /></button>
            </div>
            <div className="ls-infosheet-b"><InfoPane id={infoSheet} {...infoPaneProps} onPractice={solveQuestion} /></div>
          </div>
        )}
      </div>
    );

  return (
    <div
      ref={rootRef}
      tabIndex={-1}
      role="dialog"
      aria-modal="true"
      aria-label={`${deckName(deck, false)} dersi`}
      className={`ls-root ${marking ? 'is-marking' : ''} ${recall ? 'ms-recall' : ''} ${immersive ? 'is-immersive' : ''} ${layout === 'B' ? 'is-B' : 'is-A'}`}
      onClickCapture={(e) => {
        if (!recall) return;
        const t = (e.target as HTMLElement).closest('.ls-content strong, .ls-content b');
        if (t && !t.classList.contains('ms-shown')) {
          t.classList.add('ms-shown');
          e.stopPropagation();
        }
      }}
    >
      <FeedbackProvider value={fbCtx}>
      {immersive && (
        <button type="button" className="ls-exit-immersive" onClick={() => setImmersive(false)} aria-label="Tam ekrandan çık"><Minimize2 aria-hidden /></button>
      )}
      {topBar}
      {markingBar}
      <div className="ls-stage" ref={stageRef}>
        {focusBand}
        {stage}
      </div>

      {outlineMobile && (
        <>
          <button type="button" className="ls-scrim" aria-label="Bölümleri kapat" onClick={() => setOutlineMobile(false)} />
          <nav className="ls-drawer" aria-label="Ders bölümleri">
            <div className="ls-drawer-h"><b>Bölümler</b><button type="button" className="ls-btn is-icon is-ghost" onClick={() => setOutlineMobile(false)} aria-label="Kapat"><X aria-hidden /></button></div>
            <Outline steps={steps} sections={sections} current={index} done={done} onPick={goTo} />
          </nav>
        </>
      )}

      {sheet && (
        <>
          <button type="button" className="ls-scrim is-right" aria-label="Paneli kapat" onClick={() => setSheet(null)} />
          <aside className="ls-side-sheet" aria-label={sheet === 'ai' ? 'Asistana sor' : 'Ders notları'}>
            <div className="ls-drawer-h">
              <b>{sheet === 'ai' ? 'Asistana sor' : 'Ders notları'}</b>
              <button type="button" className="ls-btn is-icon is-ghost" onClick={() => setSheet(null)} aria-label="Kapat"><X aria-hidden /></button>
            </div>
            <div className="ls-side-sheet-b">
              {sheet === 'ai' ? (
                <AskAi key={step.number} deck={deck} slide={step.slide} />
              ) : (
                <>
                  {deck.overview && <Prose text={deck.overview} className="is-sm" />}
                  {(deck.highYieldPearls || []).length > 0 ? (
                    <SpotList items={deck.highYieldPearls} title="Dersin spotları" note="Dersin tamamından en çok sorulan bilgiler" compact />
                  ) : (
                    <p className="ls-hint"><Sparkles aria-hidden /> Bu ders için spot bilgi yok.</p>
                  )}
                </>
              )}
            </div>
          </aside>
        </>
      )}

      {fbOpen && (
        <FeedbackDialog
          deckId={deck.id}
          deckTitle={deckName(deck)}
          target={fbOpen}
          items={feedback.filter((f) => f.targetKey === fbOpen.key)}
          onClose={() => setFbOpen(null)}
          onAdd={(f) => setFeedback((l) => [...l, f])}
          onUpdate={(f) => setFeedback((l) => l.map((x) => (x.id === f.id ? f : x)))}
        />
      )}

      {searchOpen && (
        <GlobalTopicSearchModal
          deck={deck}
          onSelect={(i) => {
            setSearchOpen(false);
            goTo(i);
          }}
          onClose={() => setSearchOpen(false)}
        />
      )}
      </FeedbackProvider>
    </div>
  );
};
