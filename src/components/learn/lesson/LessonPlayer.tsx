import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { startLearnTour } from '../../onboarding/learnTourState';
import { useLiveEvent } from '../../../hooks/useLiveEvent';
import { observeScrollReveal } from '../../../utils/scrollReveal';
import { DeckNotePanel } from './DeckNotePanel';
import { onSpeakingChange, speak, speakOgrenStep, stopSpeaking } from '../../../utils/tts';
import {
  BookOpen,
  Check,
  Eraser,
  Hand,
  Highlighter,
  PenLine,
  ChevronDown,
  ChevronLeft,
  ChevronUp,
  ChevronRight,
  Columns,
  EyeOff,
  FileDown,
  FileText,
  GalleryHorizontal,
  Info,
  LayoutPanelLeft,
  ListTree,
  Maximize2,
  MessageCircleQuestion,
  Minimize2,
  MoreHorizontal,
  NotebookText,
  NotebookPen,
  PanelsTopLeft,
  Rows3,
  Search,
  Sparkles,
  X,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Type,
  Users,
  Timer,
  Moon,
  Sun,
  Compass,
} from 'lucide-react';
import type { InteractiveDeck } from '../InteractiveDeckView';
import { AskAi, GlobalTopicSearchModal, SpotList } from '../InteractiveDeckView';
import type { DeckViewMode } from '../InteractiveDeckView';
import { DeckPdfViewer } from '../DeckPdfViewer';
import { SplitPane } from './SplitPane';
import { useGlossary } from '../MedicalGlossaryPopover';
import { HL_COLORS, Highlightable, isPenActive, setHighlighterTool, stopPen, useHighlighterTool, usePenActive } from '../../ui/Highlighter';
import { resetPenDevice, usePenDevice } from '../../ui/penInput';
import { penPalette, SlideDrawingCanvas, setDrawingGlobalState, useDrawingGlobalState } from '../SlideDrawingCanvas';
import { getSlidePdfLocation } from '../../../services/slidePdfMappingService';
import { useDeckPdf } from '../../../services/deckPdfService';
import { QuestionFocus, focusMarks } from '../../../services/questionFocus';
import { detectIosDevice, openPwaInstallGuide } from '../../../services/pwaService';
import { shouldAvoidNativeFullscreen } from '../../../utils/device';
import { releasePageFullscreen, wasRecentlyScrollingOrTouching } from '../../../utils/fullscreen';
import { lockScroll, unlockScroll } from '../../../utils/scrollLock';
import { toast } from '../../ui/Toast';
import { deckName } from '../../../data/deckStore';
import {
  buildSections, buildSteps, DeckKazanim, LessonSection, LessonStep, loadKazanimIndex, matchKazanim, PracticeItem, readDone, writeDone,
} from './lessonModel';
import { practiceOf, stripEmoji, withGlossaryTerms } from './lessonModel';
import { setLessonZoom, stepZoom, useLessonZoom, useLessonZoomGestures, ZOOM_MAX, ZOOM_MIN } from './lessonZoom';
import { FeedbackItem, FeedbackTarget, listFeedback } from './lessonFeedback';
import { FeedbackDialog, FeedbackFlag, FeedbackProvider, groupFeedback } from './LessonFeedbackUI';
import { Formula, hideTermTip, InfoId, InfoPane, Infographic, infoTabsFor, KeyPoints, LessonTable, PracticeCard, practiceMeta, Prose } from './LessonBlocks';
import { LessonRail } from './LessonRail';
import { Sheet } from '../../ui/Sheet';
import { registerSelectionActions } from '../../../utils/selectionShare';
import { selectionContext, useLearnSocial } from './learnSocial';
import { ComposerReq, ReportReq, ReportSheet, setSocialVisible, SocialProvider, StepSocial, ThreadSheet, useSocialVisible } from './LearnSocialUI';
import '../../../styles/learn-v10.css';
import '../../../styles/v12/lesson.css';
import { useAppearance, setAppearance } from '../../../utils/appearance';

// Gece modu: dersten çıkmadan Koyu ↔ son açık tema (Açık/Sarı) arasında geçer.
const DAY_KEY = 'medsoru_lesson_day_mode';
const NightToggle: React.FC = () => {
  const { mode } = useAppearance();
  const dark = mode === 'dark';
  const toggle = () => {
    if (dark) {
      let day: 'light' | 'sepia' = 'light';
      try { if (localStorage.getItem(DAY_KEY) === 'sepia') day = 'sepia'; } catch { /* gizli pencere */ }
      setAppearance({ mode: day });
    } else {
      try { localStorage.setItem(DAY_KEY, mode); } catch { /* gizli pencere */ }
      setAppearance({ mode: 'dark' });
    }
  };
  return (
    <button type="button" className="ls-btn is-icon is-ghost" onClick={toggle} aria-pressed={dark} aria-label={dark ? 'Gündüz moduna geç' : 'Gece moduna geç'} title={dark ? 'Gündüz modu' : 'Gece modu'}>
      {dark ? <Sun aria-hidden /> : <Moon aria-hidden />}
    </button>
  );
};
import { FocusSession, IX_EVENT, IxEventDetail } from './FocusSession';
import { recordResult } from '../../../services/learnReview';
import { tekrarTamamlandi, useKonuSayaci, useSoruSayaci } from '../../../services/calismaTakip';
import { ogrenTakipId } from '../../takip/ogrenTakipId';
import type { IxResult } from './lessonModel';
import { MetinAktarMenu } from '../../MetinAktarMenu';
import type { AktarBelge } from '../../../services/metinDisaAktar';
import { mdDuzenle } from '../../../services/maddeDuzen';

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
 * Yönetici bağlantısı: /ogren/<deste>?adim=5&hedef=<targetKey> (paylaşım biçimi ?slide=5&target=… da okunur).
 * Oynatıcı kurulurken bir kez okunur, adres çubuğu temizlenir; ders o adımda açılır ve öğe vurgulanır.
 */
const readDeepLink = (): { adim?: number; hedef?: string; tartisma?: string } | null => {
  try {
    const sp = new URLSearchParams(window.location.search);
    const adim = Number(sp.get('adim')) || Number(sp.get('slide')) || undefined;
    // Paylaşım bağlantısındaki target yalnız öğe anahtarıysa (ör. "s12:q:0") hedef sayılır.
    const target = sp.get('target');
    const hedef = sp.get('hedef') || (target && target.includes(':') ? target : undefined);
    const tartisma = sp.get('tartisma') || undefined;
    if (!adim && !hedef && !tartisma) return null;
    sp.delete('tartisma');
    sp.delete('adim');
    sp.delete('hedef');
    sp.delete('slide');
    sp.delete('target');
    const q = sp.toString();
    window.history.replaceState(window.history.state, '', window.location.pathname + (q ? `?${q}` : '') + window.location.hash);
    return { adim, hedef, tartisma };
  } catch {
    return null;
  }
};
type ReadMode = 'paged' | 'scroll';
type Sheet = null | 'notes' | 'ai' | 'mine';

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

const useMedia = (q: string) => {
  const [m, setM] = useState(() => typeof window !== 'undefined' && window.matchMedia(q).matches);
  useEffect(() => {
    const mq = window.matchMedia(q);
    const on = () => setM(mq.matches);
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, [q]);
  return m;
};
const useIsPhone = () => useMedia('(max-width: 767px)');
/** v10: slayt rayı yalnız ≥1024 px'te solda durur; altında Sheet olarak açılır */
const useIsWide = () => useMedia('(min-width: 1024px)');

const isTyping = (t: EventTarget | null) => {
  const el = t as HTMLElement | null;
  return !!el && (el.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName));
};


/* Bölüm/slayt listesi v10'da LessonRail.tsx'te (düz numaralı ray; telefon/tablette Sheet). */

/* ---------------------------------------------------------------------------
 * Adım içeriği (başlık + anlatım + tablo); kalem ve çizim katmanları bu kutuya bağlı
 * ------------------------------------------------------------------------- */
// Adımı EMA sesiyle okur (öncelikle statik EMA mp3 dosyası, yoksa fallback): başlık, anlatım, (anlatım yoksa) anahtar maddeler.
const ListenButton: React.FC<{ step: LessonStep; deckId?: string }> = ({ step, deckId }) => {
  const [on, setOn] = useState(false);
  useEffect(() => onSpeakingChange(setOn), []);
  useEffect(() => () => stopSpeaking(), [step.number]);
  const text = () => {
    const keys = step.bullets.length > 1 || !step.narrative.trim() ? step.bullets.map((b) => `${b.title}: ${b.desc}`) : [];
    return [step.title, step.slide.subtitle, step.narrative, ...keys]
      .filter(Boolean)
      .join('. ')
      .replace(/\[\[([^\]|]+)(\|[^\]]+)?\]\]/g, '$1')
      .replace(/^\s*[-*•]\s+/gm, '');
  };
  return (
    <button
      type="button"
      className={`ls-tag ${on ? 'is-accent' : 'is-plain'}`}
      onClick={() => (on ? stopSpeaking() : deckId ? speakOgrenStep(deckId, step.number, text()) : speak(text()))}
      aria-pressed={on}
      title={on ? 'Okumayı durdur' : 'Bu adımı sesli dinle (EMA)'}
    >
      {on ? '■ Durdur' : '▶ Dinle'}
    </button>
  );
};

const StepHead: React.FC<{ step: LessonStep; total: number; sectionName?: string; deckId?: string }> = ({ step, total, sectionName, deckId }) => {
  // v12 (canvas LearnPlayer): üstte sade künye satırı (bölüm · adım), bayrak başlığın yanında
  const v12 = useAppearance().design === 'v12';
  if (v12) {
    return (
      <header className="ls-head x12-head" data-fb-key={`${step.number}:text:0`}>
        <div className="ls-eyebrow-row">
          <span className="x12-head-meta">{sectionName ? `${sectionName} · ` : ''}Adım {step.number} / {total}</span>
          {step.checkpoint > 0 && <span className="ls-tag is-warn">Tekrar {step.checkpoint}</span>}
          {step.game && <span className="ls-tag is-ai">Ders sonu oyunları</span>}
          {step.badge && !step.checkpoint && !step.game && <span className="ls-tag is-plain">{step.badge}</span>}
          {step.questions.length > 0 && <span className="ls-tag is-warn">{step.questions.length} soru</span>}
          <ListenButton step={step} deckId={deckId} />
        </div>
        <div className="x12-title-row">
          <h1 className="ls-title"><span>{step.title}</span></h1>
          <FeedbackFlag target={fbTarget(step, 'text', 0, 'Anlatım', step.title, 'Ana içerik › Başlık ve anlatım')} className="ls-head-flag" />
        </div>
        {step.slide.subtitle && <p className="ls-sub">{step.slide.subtitle}</p>}
      </header>
    );
  }
  return (
    <header className="ls-head" data-fb-key={`${step.number}:text:0`}>
      <div className="ls-eyebrow-row">
        <span>Bölüm {step.section + 1}</span>
        <span className="dot" aria-hidden />
        <span>Adım {step.number} / {total}</span>
        {step.checkpoint > 0 && <span className="ls-tag is-accent">Tekrar {step.checkpoint}</span>}
        {step.game && <span className="ls-tag is-ok">Ders sonu oyunları</span>}
        {step.badge && !step.checkpoint && !step.game && <span className="ls-tag is-plain">{step.badge}</span>}
        {step.questions.length > 0 && <span className="ls-tag is-warn">{step.questions.length} soru</span>}
        <ListenButton step={step} deckId={deckId} />
        <FeedbackFlag target={fbTarget(step, 'text', 0, 'Anlatım', step.title, 'Ana içerik › Başlık ve anlatım')} className="ls-head-flag" />
      </div>
      <h1 className="ls-title"><span>{step.title}</span></h1>
      {step.slide.subtitle && <p className="ls-sub">{step.slide.subtitle}</p>}
    </header>
  );
};

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

const PracticeSet: React.FC<{ step: LessonStep; items: PracticeItem[]; jump?: { to: number; at: number } | null; onAllDone: () => void; onResult?: (i: number, item: PracticeItem, r: IxResult) => void }> = ({ step, items, jump, onAllDone, onResult }) => {
  const [cur, setCur] = useState(0);
  const [dir, setDir] = useState<1 | -1>(1);
  const [doneSet, setDoneSet] = useState<Set<number>>(new Set());
  // v12: "Sonraki: <ad>" kartın alt çubuğunda (blok kabuğu), v10/v11'de kartın altında
  const v12 = useAppearance().design === 'v12';
  const go = (i: number) => {
    setDir(i >= cur ? 1 : -1);
    setCur(i);
  };
  useEffect(() => {
    if (jump && jump.to >= 0 && jump.to < items.length) go(jump.to);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [jump, items.length]);
  if (!items.length) return null;
  const at = Math.min(cur, items.length - 1);
  const item = items[at];
  const nextUndone = items.findIndex((_, i) => i > at && !doneSet.has(i));
  const nextIdx = nextUndone >= 0 ? nextUndone : items.findIndex((_, i) => !doneSet.has(i) && i !== at);
  const pct = Math.round((doneSet.size / items.length) * 100);
  const nextBtn = doneSet.has(at) && nextIdx >= 0 ? { label: practiceMeta(items[nextIdx])[1], go: () => go(nextIdx) } : null;
  return (
    <section className="ls-practice" aria-label="Pekiştir">
      <div className="ls-sec-h">Pekiştir <span>{doneSet.size}/{items.length}</span></div>
      {items.length > 1 && (
        <div className="ls-psteps" role="tablist" style={{ '--p': pct } as React.CSSProperties}>
          {items.map((p, i) => {
            const [Icon, label] = practiceMeta(p);
            const isDone = doneSet.has(i);
            return (
              <button
                key={i}
                type="button"
                role="tab"
                aria-selected={i === at}
                aria-label={`${i + 1}. ${label}${isDone ? ' (tamam)' : ''}`}
                title={label}
                className={`ls-pstep ${i === at ? 'is-on' : ''} ${isDone ? 'is-done' : ''}`}
                onClick={() => go(i)}
              >
                {isDone ? <Check aria-hidden /> : <Icon aria-hidden />}
                <span className="lbl"><span>{label}</span></span>
              </button>
            );
          })}
        </div>
      )}
      <PracticeCard
        key={at}
        className={dir > 0 ? 'ls-enter-next' : 'ls-enter-prev'}
        item={item}
        target={practiceTarget(step, item, at)}
        done={doneSet.has(at)}
        next={v12 ? nextBtn : undefined}
        onDone={(r) => {
          if (r) onResult?.(at, item, r);
          setDoneSet((d) => {
            if (d.has(at)) return d;
            const nd = new Set(d).add(at);
            if (nd.size >= items.length) onAllDone();
            return nd;
          });
        }}
      />
      {!v12 && nextBtn && (
        <button type="button" className="ls-pnext" onClick={nextBtn.go}>
          <span>Sonraki</span>
          <b>{nextBtn.label}</b>
          <ChevronRight aria-hidden />
        </button>
      )}
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
  /** Dersin sürümleri (V1, V2…); varsa üst çubukta sürüm anahtarı çıkar, açık olan vurgulanır */
  versions?: { id: string; label: string; note?: string }[];
  onSwitchVersion?: (id: string) => void;
  /** Hata defterini (bu deste) tekrar ekranında aç */
  onOpenReview?: (deckId: string) => void;
}

/** Ders metni (her adımın başlığı, alt başlığı ve anlatımı birebir) → dışa aktarma belgesi */
function ogrenAktarBelgesi(deck: InteractiveDeck): AktarBelge {
  const ust = [deck.discipline, deck.instructor].filter(Boolean).join(' · ');
  return {
    baslik: deckName(deck),
    alt: `${ust ? `${ust} · ` : ''}Etkileşimli ders metni`,
    bolumler: (deck.slides || [])
      .map((sl: any) => ({ sl, md: String(sl.synthesisNarrative || sl.content || '').trim() }))
      .filter((x) => x.md)
      .map(({ sl, md }) => ({ baslik: `${sl.slideNumber}. ${String(sl.title || '').replace(/^\[[^\]]+\]\s*/, '')}`, alt: sl.subtitle || undefined, md: mdDuzenle(md) })),
  };
}

export const LessonPlayer: React.FC<LessonPlayerProps> = ({ deck, startAt, initialViewMode = 'interactive', onProgress, onClose, onExportPdf, focus, onClearFocus, versions, onSwitchVersion, onOpenReview }) => {
  const steps = useMemo(() => buildSteps(deck), [deck]);
  const sections = useMemo(() => buildSections(steps), [steps]);
  const n = steps.length;
  // Yalnız ilk çizimde okunur (useRef(readDeepLink()) her çizimde adresi temizleyip yeni bağlantıyı yutuyordu).
  const [initialLink] = useState(readDeepLink);
  const deepLink = useRef(initialLink);
  const [index, setIndex] = useState(() => {
    const byLink = deepLink.current?.adim ? steps.findIndex((s) => s.number === deepLink.current!.adim) : -1;
    return byLink >= 0 ? byLink : Math.min(Math.max(0, startAt), n - 1);
  });
  const [dir, setDir] = useState(1);
  const { setIsDrawerOpen, glossaryList, setCurrentSlideText } = useGlossary();
  // Adımın kendi terimleri + metinde geçen sözlük terimleri (eski destelerde terim alanı boş)
  const step = useMemo(() => withGlossaryTerms(steps[index], glossaryList as any), [steps, index, glossaryList]);

  const isPhone = useIsPhone();
  const isWide = useIsWide();
  const [layoutPref, setLayoutPref] = useState<Layout>(() => pref.get('medsoru_learn_layout', 'A', ['A', 'B'] as const));
  const layout: Layout = isPhone ? 'A' : layoutPref;
  const [viewMode, setViewMode] = useState<DeckViewMode>(initialViewMode);
  /** v12 (canvas LearnPlayer): Stüdyo = Akış kabuğu (ray + okuma sütunu + bilgi çekmecesi + alt gezinme) içinde iki sütun;
   *  sağda tek etkin bloklu Pekiştir paneli. v10/v11'in kart + yan sekmeler + bilgi karoları Stüdyo'su yalnız onlarda kalır. */
  const appearance = useAppearance();
  const v12 = appearance.design === 'v12';
  const bClassic = layout === 'B' && !v12;
  const studioV12 = layout === 'B' && v12;
  /** Slayt rayı solda mı (≥1024, Akış — v12'de Stüdyo da —, ders görünümü) yoksa Sheet olarak mı açılır */
  const railInline = (layout === 'A' || v12) && isWide && viewMode === 'interactive';
  const [readMode, setReadMode] = useState<ReadMode>(() => pref.get('medsoru_learn_mode', 'paged', ['paged', 'scroll'] as const));
  /** Kaydırarak okuma yalnız Akış'ta (v12 Stüdyo hep sayfa sayfa) */
  const flowScroll = readMode === 'scroll' && layout === 'A';
  const [recall, setRecall] = useState(false);
  const [outlineOpen, setOutlineOpen] = useState(() => pref.get('medsoru_learn_toc', typeof window !== 'undefined' && window.innerWidth >= 1100 ? '1' : '0', ['1', '0'] as const) === '1');
  const [outlineMobile, setOutlineMobile] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const [zoomOpen, setZoomOpen] = useState(false);
  const zoom = useLessonZoom();
  const [zoomBadge, setZoomBadge] = useState(0);
  const [sheet, setSheet] = useState<Sheet>(null);
  /** v12: Notlarım geniş ekranda kalıcı bölme (Akış: sağ sütun, Stüdyo: Pekiştir panelinin üstü); dar ekranda yan sayfa */
  const notesDocked = v12 && sheet === 'mine' && isWide && viewMode === 'interactive';
  const [searchOpen, setSearchOpen] = useState(false);
  const [dockTab, setDockTab] = useState<InfoId | null>(null);
  const [infoSheet, setInfoSheet] = useState<InfoId | null>(null);
  const [practiceJump, setPracticeJump] = useState<{ to: number; at: number } | null>(null);
  const [sideTab, setSideTab] = useState<'ix' | 'cards' | 'q'>('ix');
  const [done, setDone] = useState<Set<number>>(() => readDone(deck.id));
  const [kazIndex, setKazIndex] = useState<Record<string, DeckKazanim[]>>({});
  const [doneIx, setDoneIx] = useState<Set<string>>(new Set());
  const [focusSetup, setFocusSetup] = useState(false);
  const [focusOn, setFocusOn] = useState(false);
  /** Ölçülebilir etkileşim sonucu → hata defteri + odak seansı nabzı */
  // Bitirdiklerim: dersteki etkin süre + yanıtlanan etkileşimler (adım:öge başına bir kez)
  const takipId = useMemo(() => ogrenTakipId(deck.id), [deck.id]);
  useKonuSayaci('ogren', takipId);
  const soruSay = useSoruSayaci('ogren', takipId);
  // tekrar turunda son adıma gelinince konu yeniden "bitti" olur
  useEffect(() => { if (n > 0 && index >= n - 1) tekrarTamamlandi('ogren', takipId); }, [index, n, takipId]);
  const recordIx = useCallback(
    (s: LessonStep, i: number, item: PracticeItem, r: IxResult) => {
      soruSay(`${s.number}:${i}`);
      recordResult({ deckId: deck.id, deckTitle: deckName(deck), slide: s.number, stepTitle: s.title, ix: i, item }, r);
      const detail: IxEventDetail = { deckId: deck.id, slide: s.number, title: s.title, ok: r.ok, ms: r.ms };
      window.dispatchEvent(new CustomEvent(IX_EVENT, { detail }));
    },
    [deck, soruSay]
  );
  const [feedback, setFeedback] = useState<FeedbackItem[]>([]);
  const [fbOpen, setFbOpen] = useState<FeedbackTarget | null>(null);
  useEffect(() => {
    let alive = true;
    listFeedback(deck.id).then((l) => alive && setFeedback(l)).catch(() => {});
    return () => {
      alive = false;
    };
  }, [deck.id]);
  // Başka öğrencinin bildirimi / oyu / yönetici çözümü canlı yansısın
  useLiveEvent('learn_feedback_changed', (p) => {
    if (p?.resync || !p?.deckId || p.deckId === deck.id || feedback.some((f) => f.id === p.id)) {
      listFeedback(deck.id).then(setFeedback).catch(() => {});
    }
  });
  const fbCtx = useMemo(() => ({ byKey: groupFeedback(feedback), open: (t: FeedbackTarget) => setFbOpen(t) }), [feedback]);

  /* --- ortak katman: herkese açık notlar + metin bildirimi tartışmaları (canlı) --- */
  const social = useLearnSocial(deck.id);
  const socialVisible = useSocialVisible();
  const [composer, setComposer] = useState<ComposerReq | null>(null);
  const [reportReq, setReportReq] = useState<ReportReq | null>(null);
  const [threadOpen, setThreadOpen] = useState<string | null>(() => initialLink?.tartisma || null);
  const socialCtx = useMemo(
    () => ({ social, deckId: deck.id, deckTitle: deckName(deck), visible: socialVisible, composer, openComposer: setComposer, openThread: setThreadOpen }),
    [social, deck, socialVisible, composer]
  );
  const indexRef = useRef(index);
  indexRef.current = index;
  // Seçim çubuğu: ders metninde seçim yapılınca "Not ekle" ve "Bildir" düğmeleri (utils/selectionShare)
  useEffect(
    () =>
      registerSelectionActions(({ host }) => {
        const root = rootRef.current;
        if (!root || !root.contains(host) || !host.closest('.ls-content')) return null;
        const at = host.closest('[data-step]')?.getAttribute('data-step');
        const st = steps[at != null ? Number(at) : indexRef.current] || steps[indexRef.current];
        if (!st) return null;
        return [
          {
            id: 'ls-note',
            label: 'Not ekle',
            icon: 'M12 5v14M5 12h14',
            tone: 'accent',
            run: ({ text }) => {
              setSocialVisible(true);
              setComposer({ stepNumber: st.number, anchor: text.slice(0, 300), at: Date.now() });
              window.getSelection()?.removeAllRanges();
            },
          },
          {
            id: 'ls-report',
            label: 'Bildir',
            icon: 'M12 2a10 10 0 1 0 0 20a10 10 0 1 0 0-20M12 8v4M12 16h.01',
            tone: 'danger',
            run: ({ range }) => {
              const c = selectionContext(range);
              if (c.quote.length < 4) return;
              setReportReq({ stepNumber: st.number, ...c });
              window.getSelection()?.removeAllRanges();
            },
          },
        ];
      }),
    [steps]
  );

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
  const zoomRef = useRef<HTMLDivElement>(null);
  // Yakınlaştırma rozeti: hareketle değişince ~0.9 sn ölçeği gösterir
  const flashZoom = useCallback(() => setZoomBadge(Date.now()), []);
  useEffect(() => {
    if (!zoomBadge) return;
    const t = window.setTimeout(() => setZoomBadge(0), 900);
    return () => window.clearTimeout(t);
  }, [zoomBadge]);
  useLessonZoomGestures(stageRef, zoom.gestures, flashZoom);
  const flowRefs = useRef<(HTMLElement | null)[]>([]);
  const programmatic = useRef(false);
  const penOn = usePenActive();
  const drawState = useDrawingGlobalState();
  const drawMode = drawState.activeMode;
  const hlTool = useHighlighterTool();
  const penDevice = usePenDevice();
  const marking = penOn || drawMode !== 'none';

  const pdfInfo = useDeckPdf(deck.id);
  const pdfLoc = useMemo(() => getSlidePdfLocation(deck.id, step.slide.slideNumber, step.slide, n, pdfInfo?.slides), [deck.id, step, n, pdfInfo?.slides]);
  const [pdfPage, setPdfPage] = useState(pdfLoc.primaryPage);
  const pdfUserScrolledPage = useRef<number | null>(null);
  useEffect(() => {
    if (pdfUserScrolledPage.current !== null) {
      pdfUserScrolledPage.current = null;
      return;
    }
    setPdfPage(pdfLoc.primaryPage);
  }, [pdfLoc.primaryPage]);
  // PDF'te kaydırılan sayfa başka bir adımın bölümüne düşerse ders o adıma geçer (özet/tekrar adımları tüm PDF'i
  // kapsadığı için hedef olmaz). Adım değişiminden hemen sonraki programlı kaydırma sayılmaz; kısa bekleme ile süzülür.
  const stepPdfRanges = useMemo(() => steps.map((s) => {
    const al = pdfInfo?.slides?.[String(s.slide.slideNumber)];
    if (!al) return null;
    const [a, b, f = 0] = al;
    const total = pdfInfo?.files[f]?.pages;
    if (a === 1 && (total ? b >= total : b - a >= 20)) return null;
    return { a, b, f };
  }), [steps, pdfInfo]);
  const pdfSyncAt = useRef(0);
  const pdfSyncTimer = useRef<number | undefined>(undefined);
  useEffect(() => { pdfSyncAt.current = Date.now(); }, [index]);
  useEffect(() => () => window.clearTimeout(pdfSyncTimer.current), []);
  const onPdfPage = useCallback((page: number, fileIndex: number, userScroll?: boolean) => {
    setPdfPage(page);
    window.clearTimeout(pdfSyncTimer.current);
    if (!userScroll) return;
    pdfSyncTimer.current = window.setTimeout(() => {
      if (Date.now() - pdfSyncAt.current < 1500) return;
      const cur = stepPdfRanges[index];
      const inside = (r: { a: number; b: number; f: number } | null) => !!r && r.f === fileIndex && page >= r.a && page <= r.b;
      if (cur ? inside(cur) : !stepPdfRanges.some(inside)) return;
      // en yakın eşleşen adım (ileri/geri), birden çoksa güncel adıma en yakını
      let best = -1;
      stepPdfRanges.forEach((r, i) => {
        if (inside(r) && (best < 0 || Math.abs(i - index) < Math.abs(best - index))) best = i;
      });
      if (best >= 0 && best !== index) {
        pdfUserScrolledPage.current = page;
        goToRef.current(best);
      }
    }, 650);
  }, [stepPdfRanges, index]);
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
      if (document.fullscreenElement) releasePageFullscreen();
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
  const goToRef = useRef(goTo);
  goToRef.current = goTo;
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
  const hadNativeFsRef = useRef(false);
  // Tam ekran/immersive açıkken belge kaymasın: iOS'ta adres çubuğu geri gelip katmanı kaydırmasın.
  useEffect(() => {
    if (!immersive) return;
    lockScroll();
    return () => unlockScroll();
  }, [immersive]);
  useEffect(() => {
    const on = () => {
      const d = document as any;
      const fs = !!(d.fullscreenElement || d.webkitFullscreenElement || d.webkitCurrentFullScreenElement);
      setIsFs(fs);
      if (fs) {
        hadNativeFsRef.current = true;
        setImmersive(true);
      } else if (hadNativeFsRef.current) {
        hadNativeFsRef.current = false;
        // Dokunmatik cihazda kaydırma hareketi yüzünden tarayıcı native fullscreen'den çıktıysa tam ekran modunu koru
        if (wasRecentlyScrollingOrTouching()) {
          setImmersive(true);
        } else {
          setImmersive(false);
          document.documentElement.classList.remove('is-app-fullscreen');
        }
      }
    };
    document.addEventListener('fullscreenchange', on);
    document.addEventListener('webkitfullscreenchange', on);
    return () => {
      document.removeEventListener('fullscreenchange', on);
      document.removeEventListener('webkitfullscreenchange', on);
    };
  }, []);
  const toggleFullscreen = () => {
    setToolsOpen(false);
    const d = document as any;
    if (immersive || d.fullscreenElement || d.webkitFullscreenElement || d.webkitCurrentFullScreenElement) {
      setImmersive(false);
      document.documentElement.classList.remove('is-app-fullscreen');
      if (d.fullscreenElement || d.webkitFullscreenElement || d.webkitCurrentFullScreenElement) {
        hadNativeFsRef.current = false;
        (d.exitFullscreen || d.webkitExitFullscreen || d.webkitCancelFullScreen)?.call(d)?.catch?.(() => {});
      }
      return;
    }
    const el: any = document.documentElement;
    el.classList.add('is-app-fullscreen');
    setImmersive(true);
    try {
      window.scrollTo({ top: 0, left: 0, behavior: 'instant' as ScrollBehavior });
    } catch {
      window.scrollTo(0, 0);
    }
    const req = el.requestFullscreen || el.webkitRequestFullscreen || el.webkitRequestFullScreen;
    if (!req || shouldAvoidNativeFullscreen()) {
      const isStandalone = window.matchMedia?.('(display-mode: standalone)').matches || (navigator as any).standalone === true;
      if (detectIosDevice() && !isStandalone) {
        toast.info(
          'Tam ekran ders modu açıldı',
          'Adres çubuğunu da tamamen gizlemek için uygulamayı Ana Ekrana ekleyebilirsin.',
          { label: 'Nasıl eklenir?', onClick: () => openPwaInstallGuide() }
        );
      }
      return;
    }
    try {
      req.call(el, { navigationUI: 'hide' })?.catch?.(() => {});
    } catch {
      try {
        req.call(el)?.catch?.(() => {});
      } catch {
        /* sayfa içi immersive mod zaten aktif */
      }
    }
  };
  const fsOn = isFs || immersive;

  /* --- klavye --- */
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (isTyping(e.target)) return;
      // Ders dışındaki bir pencere (PDF oluştur, sözlük vb.) açıkken kısayollar o pencereye aittir
      const foreign = [...document.querySelectorAll<HTMLElement>('[role="dialog"]')].some((d) => d !== rootRef.current && !rootRef.current?.contains(d) && d.getClientRects().length > 0);
      if (foreign || fbOpen || rootRef.current?.querySelector('.lf-overlay')) return; // odak molası / seans fişi açıkken
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
      else if (e.key.toLowerCase() === 'o' && !focusOn) setFocusSetup(true);
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

  // Araçlar / yakınlaştırma menüsü dışına tıklayınca kapanır
  useEffect(() => {
    if (!toolsOpen && !zoomOpen) return;
    const on = (e: PointerEvent) => {
      const t = e.target as HTMLElement;
      if (t.closest?.('[data-ls-keep]')) return;
      if (toolsOpen && toolsRef.current && !toolsRef.current.contains(t)) setToolsOpen(false);
      if (zoomOpen && zoomRef.current && !zoomRef.current.contains(t)) setZoomOpen(false);
    };
    document.addEventListener('pointerdown', on);
    return () => document.removeEventListener('pointerdown', on);
  }, [toolsOpen, zoomOpen]);

  /* --- kaydırma hareketi (sayfa sayfa): kalem/çizim açıkken ya da metin seçiliyken çevirmez --- */
  const touch = useRef<{ x: number; y: number; at: number } | null>(null);
  const onTouchStart = (e: React.TouchEvent) => {
    if (e.touches.length > 1) {
      touch.current = null;
      return;
    }
    const t = e.touches[0];
    touch.current = e.touches.length === 1 && (t as any).touchType !== 'stylus' ? { x: t.clientX, y: t.clientY, at: Date.now() } : null;
  };
  const onTouchEnd = (e: React.TouchEvent) => {
    const s = touch.current;
    touch.current = null;
    if (e.touches.length > 0) return; // iki parmak (yakınlaştırma) sayfa çevirmez
    if (!s || (layout === 'A' && readMode === 'scroll') || isPenActive() || marking || Date.now() - s.at > 450) return;
    if ((e.target as HTMLElement).closest('.ls-ix, .ls-table, .ls-dock, input, textarea, .x12-notes, .x12-studio-r')) return;
    const sel = window.getSelection();
    if (sel && !sel.isCollapsed && sel.toString().trim()) return;
    const t = e.changedTouches[0];
    const dx = t.clientX - s.x;
    const dy = t.clientY - s.y;
    if (Math.abs(dx) > 90 && Math.abs(dx) > Math.abs(dy) * 2) (dx < 0 ? next : prev)();
  };

  // Kaydırınca beliren başlık, tablo ve etkileşimler (yalnız görünür alanın altındakiler).
  useEffect(() => observeScrollReveal(mainRef.current, '.ls-prose > *, .ls-table, .ls-ix, .ls-dock'), [index, viewMode, layout]);

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

  const zoomPop = zoomOpen && (
    <div className="ls-tools-pop ls-zoom-pop" role="dialog" aria-label="Yazı boyutu">
      <div className="ls-zoom-row">
        <button type="button" className="ls-btn is-icon" onClick={() => stepZoom(-1)} disabled={zoom.scale <= ZOOM_MIN} aria-label="Küçült"><ZoomOut aria-hidden /></button>
        <input
          type="range"
          className="ls-zoom-range"
          min={ZOOM_MIN * 100}
          max={ZOOM_MAX * 100}
          step={10}
          value={Math.round(zoom.scale * 100)}
          onChange={(e) => setLessonZoom({ scale: Number(e.target.value) / 100 })}
          aria-label="Yakınlaştırma oranı"
          style={{ ['--p' as string]: `${((zoom.scale - ZOOM_MIN) / (ZOOM_MAX - ZOOM_MIN)) * 100}%` }}
        />
        <button type="button" className="ls-btn is-icon" onClick={() => stepZoom(1)} disabled={zoom.scale >= ZOOM_MAX} aria-label="Büyüt"><ZoomIn aria-hidden /></button>
      </div>
      <div className="ls-zoom-row is-meta">
        <b className="ls-zoom-val">%{Math.round(zoom.scale * 100)}</b>
        <button type="button" className="ls-btn is-sm is-ghost" onClick={() => setLessonZoom({ scale: 1 })} disabled={zoom.scale === 1}><RotateCcw aria-hidden /> Sıfırla</button>
      </div>
      <label className="ls-zoom-switch">
        <span>Hareketle yakınlaştır<small>İki parmak, trackpad ve Ctrl + / − / 0</small></span>
        <button type="button" role="switch" aria-checked={zoom.gestures} className="ui-switch" onClick={() => setLessonZoom({ gestures: !zoom.gestures })} aria-label="Hareketle yakınlaştırma" />
      </label>
    </div>
  );

  const toolsPop = toolsOpen && (
    <div className="ls-tools-pop ls-tools-v2" role="menu" aria-label="Araçlar">
      {v12 ? (
        /* v12 (canvas Araçlar menüsü): her görünüm ayarı etiketli satırda satır içi segment */
        <div className="ls-tools-grp">
          <span className="ls-eyebrow">Görünüm</span>
          <div className="x12-tl-line">
            <span>Kaynak</span>
            <div className="ls-seg" role="radiogroup" aria-label="Kaynak">
              <button type="button" role="radio" aria-checked={viewMode === 'interactive'} onClick={() => pickTool(() => setViewMode('interactive'))}>Ders</button>
              <button type="button" role="radio" aria-checked={viewMode === 'split'} onClick={() => pickTool(() => setViewMode('split'))}>Yan yana</button>
              <button type="button" role="radio" aria-checked={viewMode === 'pdf'} onClick={() => pickTool(() => setViewMode('pdf'))}>PDF</button>
            </div>
          </div>
          {layout === 'A' && viewMode === 'interactive' && (
            <div className="x12-tl-line">
              <span>Okuma</span>
              <div className="ls-seg" role="radiogroup" aria-label="Okuma">
                <button type="button" role="radio" aria-checked={readMode === 'paged'} onClick={() => pickTool(() => setReadMode('paged'))} title="Sayfa sayfa">Sayfa</button>
                <button type="button" role="radio" aria-checked={readMode === 'scroll'} onClick={() => pickTool(() => setReadMode('scroll'))} title="Kaydırarak">Kaydır</button>
              </div>
            </div>
          )}
          <div className="x12-tl-line">
            <span>Ortak notlar</span>
            <div className="ls-seg" role="radiogroup" aria-label="Ortak notlar">
              <button type="button" role="radio" aria-checked={socialVisible} onClick={() => pickTool(() => setSocialVisible(true))}>Göster</button>
              <button type="button" role="radio" aria-checked={!socialVisible} onClick={() => pickTool(() => setSocialVisible(false))}>Gizle</button>
            </div>
          </div>
          {!isPhone && (
            <div className="x12-tl-line">
              <span>Düzen</span>
              <div className="ls-seg" role="radiogroup" aria-label="Düzen">
                <button type="button" role="radio" aria-checked={layout === 'A'} onClick={() => pickTool(() => setLayoutPref('A'))} title="Akış düzeni">Akış</button>
                <button type="button" role="radio" aria-checked={layout === 'B'} onClick={() => pickTool(() => setLayoutPref('B'))} title="Stüdyo düzeni">Stüdyo</button>
              </div>
            </div>
          )}
        </div>
      ) : (
      <div className="ls-tools-grp">
        <span className="ls-eyebrow">Görünüm</span>
        <div className="ls-seg" role="radiogroup" aria-label="Görünüm">
          <button type="button" role="radio" aria-checked={viewMode === 'interactive'} onClick={() => pickTool(() => setViewMode('interactive'))}><GalleryHorizontal aria-hidden /> Ders</button>
          <button type="button" role="radio" aria-checked={viewMode === 'split'} onClick={() => pickTool(() => setViewMode('split'))}><Columns aria-hidden /> Yan yana</button>
          <button type="button" role="radio" aria-checked={viewMode === 'pdf'} onClick={() => pickTool(() => setViewMode('pdf'))}><FileText aria-hidden /> PDF</button>
        </div>
        {(layout === 'A' && viewMode === 'interactive') || !isPhone ? (
          <div className="ls-seg-pair">
            {layout === 'A' && viewMode === 'interactive' && (
              <div className="ls-seg" role="radiogroup" aria-label="Okuma">
                <button type="button" role="radio" aria-checked={readMode === 'paged'} onClick={() => pickTool(() => setReadMode('paged'))} title="Sayfa sayfa"><GalleryHorizontal aria-hidden /> Sayfa</button>
                <button type="button" role="radio" aria-checked={readMode === 'scroll'} onClick={() => pickTool(() => setReadMode('scroll'))} title="Kaydırarak"><Rows3 aria-hidden /> Kaydır</button>
              </div>
            )}
            {!isPhone && (
              <div className="ls-seg" role="radiogroup" aria-label="Düzen">
                <button type="button" role="radio" aria-checked={layout === 'A'} onClick={() => pickTool(() => setLayoutPref('A'))} title="Akış düzeni"><LayoutPanelLeft aria-hidden /> Akış</button>
                <button type="button" role="radio" aria-checked={layout === 'B'} onClick={() => pickTool(() => setLayoutPref('B'))} title="Stüdyo düzeni"><PanelsTopLeft aria-hidden /> Stüdyo</button>
              </div>
            )}
          </div>
        ) : null}
      </div>
      )}
      <div className="ls-tools-grp">
        <span className="ls-eyebrow">Çalışma</span>
        <div className="ls-tgrid">
          <button type="button" role="menuitemcheckbox" aria-checked={recall} className={`ls-tt ${recall ? 'is-on' : ''}`} onClick={() => pickTool(() => setRecall((v) => !v))} title="Kalın ifadeler örtülür, dokununca açılır">
            <EyeOff aria-hidden /><span>Hatırlama</span>
          </button>
          <button type="button" role="menuitemcheckbox" aria-checked={penOn} className={`ls-tt ${penOn ? 'is-on' : ''}`} onClick={() => pickTool(() => { setDrawingGlobalState({ activeMode: 'none' }); setHighlighterTool({ active: !penOn, eraser: false }); })} title="Metni renkli işaretle">
            <Highlighter aria-hidden /><span>Marker</span>
          </button>
          <button type="button" role="menuitemcheckbox" aria-checked={drawMode !== 'none'} className={`ls-tt ${drawMode !== 'none' ? 'is-on' : ''}`} onClick={() => pickTool(() => { stopPen(); setDrawingGlobalState({ activeMode: drawMode !== 'none' ? 'none' : 'pen' }); })} title="Sayfanın üstüne serbest çiz">
            <PenLine aria-hidden /><span>Kalem</span>
          </button>
          <button type="button" role="menuitem" className={`ls-tt ${sheet === 'mine' ? 'is-on' : ''}`} onClick={() => pickTool(() => setSheet((v) => (v12 && v === 'mine' ? null : 'mine')))} title="Biçimli kişisel not">
            <NotebookPen aria-hidden /><span>Notlarım</span>
          </button>
          {!v12 && (
            <button type="button" role="menuitemcheckbox" aria-checked={socialVisible} className={`ls-tt ${socialVisible ? 'is-on' : ''}`} onClick={() => pickTool(() => setSocialVisible(!socialVisible))} title="Herkesin SPOT / ÖNEMLİ / VURGU notlarını göster ya da gizle">
              <Users aria-hidden /><span>Ortak notlar</span>
            </button>
          )}
          <button type="button" role="menuitem" className={`ls-tt ${sheet === 'notes' ? 'is-on' : ''}`} onClick={() => pickTool(() => setSheet('notes'))} title="Dersin özeti ve spotları">
            <NotebookText aria-hidden /><span>Ders notu</span>
          </button>
          <button type="button" role="menuitem" className={`ls-tt ${sheet === 'ai' ? 'is-on' : ''}`} onClick={() => pickTool(() => setSheet('ai'))} title="Bu adım hakkında soru sor">
            <MessageCircleQuestion aria-hidden /><span>Asistan</span>
          </button>
          <button type="button" role="menuitem" className="ls-tt" onClick={() => pickTool(() => setIsDrawerOpen(true))} title={`${glossaryList.length} terim`}>
            <BookOpen aria-hidden /><span>Sözlük</span>
          </button>
          <button type="button" role="menuitem" className={`ls-tt ${focusOn ? 'is-on' : ''}`} onClick={() => pickTool(() => setFocusSetup(true))} disabled={focusOn} title="Süreli, hedefli çalışma; arayüz sadeleşir (kısayol: O)">
            <Timer aria-hidden /><span>Odak seansı</span>{v12 && <kbd className="x12-kbd" aria-hidden>O</kbd>}
          </button>
          <button type="button" role="menuitem" className={`ls-tt ${fsOn ? 'is-on' : ''}`} onClick={() => pickTool(toggleFullscreen)} title="Kısayol: F">
            {fsOn ? <Minimize2 aria-hidden /> : <Maximize2 aria-hidden />}<span>{fsOn ? 'Küçült' : 'Tam ekran'}</span>{v12 && <kbd className="x12-kbd" aria-hidden>F</kbd>}
          </button>
          {onExportPdf && (
            <button type="button" role="menuitem" className="ls-tt" onClick={() => { setToolsOpen(false); if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {}); onExportPdf(step.slide.slideNumber); }} title="Bu adımı PDF olarak indir">
              <FileDown aria-hidden /><span>PDF yap</span>
            </button>
          )}
          <MetinAktarMenu dugmeSinif="ls-tt" etiket="Ders metnini dışa aktar" dosyaAdi={deckName(deck)} belge={() => ogrenAktarBelgesi(deck)} />
          <button type="button" role="menuitem" className="ls-tt" onClick={() => pickTool(() => startLearnTour('lesson'))} title="Ders ekranı ve etkileşim türleri turu">
            <Compass aria-hidden /><span>Nasıl kullanılır?</span>
          </button>
        </div>
      </div>
    </div>
  );

  const railPressed = railInline ? outlineOpen : outlineMobile;
  const toggleRail = () => (railInline ? setOutlineOpen((v) => !v) : setOutlineMobile((v) => !v));
  const versionSwitch = versions && versions.length > 1 && onSwitchVersion && (
    <span className="lv-vswitch" role="group" aria-label="Ders sürümü">
      {versions.map((v) => (
        <button
          key={v.id}
          type="button"
          aria-pressed={v.id === deck.id}
          onClick={() => v.id !== deck.id && onSwitchVersion(v.id)}
          title={v.id === deck.id ? `${v.label} açık${v.note ? ` · ${v.note}` : ''}` : `${v.label} sürümüne geç${v.note ? ` · ${v.note}` : ''}`}
        >
          {v.label}
        </button>
      ))}
    </span>
  );
  const pdfToggle = (
    <button
      type="button"
      className={`ls-btn lv-pdf-btn ${viewMode !== 'interactive' ? 'is-on' : ''}`}
      aria-pressed={viewMode !== 'interactive'}
      onClick={() => (viewMode !== 'interactive' ? setViewMode('interactive') : isPhone ? (setPdfPage(pdfLoc.primaryPage), setViewMode('pdf')) : openPdf())}
      title={viewMode !== 'interactive' ? 'Derse dön' : 'Bu adımın ders PDF sayfasını aç'}
      aria-label="Ders PDF'i"
    >
      <FileText aria-hidden /><span className="lv-hide-sm">Ders PDF’i</span>
    </button>
  );
  const zoomBtn = (
    <button
      type="button"
      className={`ls-btn is-icon is-ghost ${zoomOpen || zoom.scale !== 1 ? 'is-on' : ''}`}
      aria-expanded={zoomOpen}
      aria-haspopup="true"
      aria-label={`Yazı boyutu ve yakınlaştırma (%${Math.round(zoom.scale * 100)})`}
      title="Yazı boyutu (Ctrl + / −)"
      onClick={() => { setZoomOpen((v) => !v); setToolsOpen(false); }}
    >
      <Type aria-hidden />
    </button>
  );

  /* v12 (canvas LearnPlayer · 52 px): ‹ Kitaplık · Slaytlar | başlık · ince ilerleme + n/N · Ders PDF'i · Notlarım · Akış/Stüdyo · Ara · T · Araçlar */
  const topBarV12 = (
    <header className={`ls-top lv-top x12-top ${immersive ? 'is-hidden' : ''}`}>
      <button type="button" className="ls-btn is-ghost x12-back" onClick={onClose} aria-label="Kitaplığa dön" title="Kitaplığa dön (Esc)">
        <ChevronLeft aria-hidden /><span className="x12-back-l">Kitaplık</span>
      </button>
      <button
        type="button"
        className={`ls-btn is-icon is-ghost lv-rail-btn ${railPressed ? 'is-on' : ''}`}
        onClick={toggleRail}
        aria-label="Slaytlar"
        {...(railInline ? { 'aria-expanded': outlineOpen, 'aria-controls': 'lv-rail' } : { 'aria-haspopup': 'dialog' as const })}
        title="Slaytlar"
      >
        <LayoutPanelLeft aria-hidden />
      </button>
      <span className="x12-vsep" aria-hidden />
      <b className="x12-title" title={`${deck.title}${deck.discipline ? ` · ${deck.discipline}` : ''}${deck.instructor ? ` · ${deck.instructor}` : ''}`}>{deckName(deck)}</b>
      {versionSwitch}
      <div className="x12-prog" role="progressbar" aria-label={`İlerleme: ${n} adımın ${index + 1}. adımı`} aria-valuemin={1} aria-valuemax={n} aria-valuenow={index + 1}>
        <span className="x12-bar" aria-hidden><i style={{ width: `${((index + 1) / n) * 100}%` }} /></span>
        <span className="ls-count" aria-live="polite">{index + 1}<i>/</i>{n}</span>
      </div>
      {pdfToggle}
      <button
        type="button"
        className={`ls-btn x12-notes-btn ${sheet === 'mine' ? 'is-on' : ''}`}
        aria-pressed={sheet === 'mine'}
        onClick={() => setSheet((v) => (v === 'mine' ? null : 'mine'))}
        aria-label="Notlarım"
        title="Notlarım (bu ders, yalnız sen)"
      >
        <NotebookPen aria-hidden /><span className="x12-notes-l">Notlarım</span>
      </button>
      {!isPhone && (
        <div className="ls-seg x12-layout" role="radiogroup" aria-label="Düzen">
          <button type="button" role="radio" aria-checked={layout === 'A'} onClick={() => setLayoutPref('A')}>Akış</button>
          <button type="button" role="radio" aria-checked={layout === 'B'} onClick={() => setLayoutPref('B')}>Stüdyo</button>
        </div>
      )}
      <button type="button" className="ls-btn is-icon is-ghost" onClick={() => setSearchOpen(true)} aria-label="Derste ara" title="Derste ara (Ctrl+K)"><Search aria-hidden /></button>
      <NightToggle />
      <button
        type="button"
        className={`ls-btn is-icon is-ghost ${fsOn ? 'is-on' : ''}`}
        aria-pressed={fsOn}
        onClick={toggleFullscreen}
        aria-label={fsOn ? 'Tam ekrandan çık' : 'Tam ekran'}
        title={fsOn ? 'Tam ekrandan çık (F / Esc)' : 'Tam ekran (F)'}
      >
        {fsOn ? <Minimize2 aria-hidden /> : <Maximize2 aria-hidden />}
      </button>
      <div className="ls-tools" ref={zoomRef}>
        {zoomBtn}
        {zoomPop}
      </div>
      <div className="ls-tools" ref={toolsRef}>
        <button type="button" className={`ls-btn is-icon is-ghost x12-tools-btn ${toolsOpen ? 'is-on' : ''}`} aria-expanded={toolsOpen} aria-haspopup="menu" aria-label="Araçlar" title="Araçlar" onClick={() => { setToolsOpen((v) => !v); setZoomOpen(false); }}>
          <MoreHorizontal aria-hidden />
        </button>
        {toolsPop}
      </div>
      <div className="ls-prog" aria-hidden><i style={{ width: `${((index + 1) / n) * 100}%` }} /></div>
    </header>
  );

  const topBar = v12 ? topBarV12 : (
    <header className={`ls-top lv-top ${immersive ? 'is-hidden' : ''}`}>
      <button type="button" className="ls-btn is-icon is-ghost" onClick={onClose} aria-label="Kitaplığa dön" title="Kitaplığa dön (Esc)"><ChevronLeft aria-hidden /></button>
      <button
        type="button"
        className={`ls-btn is-icon is-ghost lv-rail-btn ${(railInline ? outlineOpen : outlineMobile) ? 'is-on' : ''}`}
        onClick={() => (railInline ? setOutlineOpen((v) => !v) : setOutlineMobile((v) => !v))}
        aria-label="Slaytlar"
        {...(railInline ? { 'aria-expanded': outlineOpen, 'aria-controls': 'lv-rail' } : { 'aria-haspopup': 'dialog' as const })}
        title="Slaytlar"
      >
        <ListTree aria-hidden />
      </button>
      <div className="ls-deck">
        <small>{deck.discipline}{deck.instructor ? ` · ${deck.instructor}` : ''}</small>
        <b title={deck.title}>{deckName(deck)}</b>
      </div>
      {versions && versions.length > 1 && onSwitchVersion && (
        <span className="lv-vswitch" role="group" aria-label="Ders sürümü">
          {versions.map((v) => (
            <button
              key={v.id}
              type="button"
              aria-pressed={v.id === deck.id}
              onClick={() => v.id !== deck.id && onSwitchVersion(v.id)}
              title={v.id === deck.id ? `${v.label} açık${v.note ? ` · ${v.note}` : ''}` : `${v.label} sürümüne geç${v.note ? ` · ${v.note}` : ''}`}
            >
              {v.label}
            </button>
          ))}
        </span>
      )}
      {layout === 'A' && (
        <span className="lv-top-prog" aria-hidden><i style={{ width: `${((index + 1) / n) * 100}%` }} /></span>
      )}
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
      <span className="ls-count" aria-live="polite">{index + 1}<i>/</i>{n}</span>
      <button
        type="button"
        className={`ls-btn lv-pdf-btn ${viewMode !== 'interactive' ? 'is-on' : ''}`}
        aria-pressed={viewMode !== 'interactive'}
        onClick={() => (viewMode !== 'interactive' ? setViewMode('interactive') : isPhone ? (setPdfPage(pdfLoc.primaryPage), setViewMode('pdf')) : openPdf())}
        title={viewMode !== 'interactive' ? 'Derse dön' : 'Bu adımın ders PDF sayfasını aç'}
        aria-label="Ders PDF'i"
      >
        <FileText aria-hidden /><span className="lv-hide-sm">Ders PDF’i</span>
      </button>
      <button type="button" className="ls-btn is-icon is-ghost" onClick={() => setSearchOpen(true)} aria-label="Derste ara" title="Derste ara (Ctrl+K)"><Search aria-hidden /></button>
      <button
        type="button"
        className={`ls-btn is-icon is-ghost ${fsOn ? 'is-on' : ''}`}
        aria-pressed={fsOn}
        onClick={toggleFullscreen}
        aria-label={fsOn ? 'Tam ekrandan çık' : 'Tam ekran'}
        title={fsOn ? 'Tam ekrandan çık (F / Esc)' : 'Tam ekran (F)'}
      >
        {fsOn ? <Minimize2 aria-hidden /> : <Maximize2 aria-hidden />}
      </button>
      <div className="ls-tools" ref={zoomRef}>
        <button
          type="button"
          className={`ls-btn is-icon is-ghost ${zoomOpen || zoom.scale !== 1 ? 'is-on' : ''}`}
          aria-expanded={zoomOpen}
          aria-haspopup="true"
          aria-label={`Yazı boyutu ve yakınlaştırma (%${Math.round(zoom.scale * 100)})`}
          title="Yazı boyutu (Ctrl + / −)"
          onClick={() => { setZoomOpen((v) => !v); setToolsOpen(false); }}
        >
          <Type aria-hidden />
        </button>
        {zoomPop}
      </div>
      <div className="ls-tools" ref={toolsRef}>
        <button type="button" className={`ls-btn ${toolsOpen ? 'is-on' : ''}`} aria-expanded={toolsOpen} aria-haspopup="true" onClick={() => { setToolsOpen((v) => !v); setZoomOpen(false); }}>
          <MoreHorizontal aria-hidden /> <span className="ls-hide-phone">Araçlar</span>
        </button>
        {toolsPop}
      </div>
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
              {penPalette(appearance.mode).map((c) => (
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
      if (!bClassic || viewMode !== 'interactive') setDockTab(infoOf[kind]);
      else setInfoSheet(infoOf[kind]);
    } else if (kind === 'q' || kind === 'cards' || kind.startsWith('ix-')) {
      const k = practice.findIndex((p, i) => practiceTarget(step, p, i).key === hedef);
      if (bClassic && viewMode === 'interactive') setSideTab(kind === 'q' ? 'q' : kind === 'cards' ? 'cards' : 'ix');
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
    if (bClassic && viewMode === 'interactive') {
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
            {v12 ? <ChevronUp aria-hidden className={`x12-chev ${dockTab ? 'is-open' : ''}`} /> : dockTab ? <ChevronDown aria-hidden /> : <Info aria-hidden />}
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
      <button type="button" className="ls-btn lv-prev" onClick={prev} disabled={index === 0} aria-label="Önceki adım"><ChevronLeft aria-hidden /><span className="lv-hide-sm">Önceki</span></button>
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

  const finishDeck = () => { markDone(step.number); toast.success('Ders tamamlandı', `${deckName(deck)} bitti.`); };
  /* ---- v12: alt gezinme çubuğu (canvas lp-nav): Önceki ← · bölüm · bölümde k/N · Sonraki → ---- */
  const NavV12 = (
    <nav className="x12-nav" aria-label="Adım gezinmesi">
      <button type="button" className="ls-btn x12-nav-prev" onClick={prev} disabled={index === 0} aria-label="Önceki adım">
        <ChevronLeft aria-hidden /><span>Önceki</span><kbd className="x12-kbd" aria-hidden>←</kbd>
      </button>
      {/* Bilgi sekmeleri (Sınav spotu · Terimler · Kazanımlar · Kaynak) ayrı satır yerine alt çubukta; bölme çubuğun üstünde açılır */}
      <span className={`x12-nav-mid ${infoTabs.length > 0 ? 'has-tabs' : ''}`}>
        {infoTabs.length > 0 && (
          <span className="x12-nav-tabs" role="tablist" aria-label="Bilgi">
            {infoTabs.map((t) => (
              <button
                key={t.id}
                type="button"
                role="tab"
                aria-selected={dockTab === t.id}
                aria-expanded={dockTab === t.id}
                className={`x12-nav-tab ${dockTab === t.id ? 'is-on' : ''} ${t.hot ? 'is-hot' : ''}`}
                onClick={() => setDockTab((v) => (v === t.id ? null : t.id))}
              >
                <t.icon aria-hidden />
                <span className="lbl">{t.label}</span>
                {t.id !== 'src' && <span className="c">{t.count}</span>}
              </button>
            ))}
          </span>
        )}
        <span className="x12-nav-pos">{section ? `${section.name} · bölümde ${secPos + 1}/${section.steps.length}` : `${index + 1}/${n}`}</span>
      </span>
      {nextStep ? (
        <button type="button" className="ls-btn is-primary x12-nav-next" onClick={next} title={nextStep.title} aria-label={`Sonraki adım: ${nextStep.title}`}>
          <span>Sonraki</span><kbd className="x12-kbd" aria-hidden>→</kbd><ChevronRight aria-hidden />
        </button>
      ) : (
        <button type="button" className="ls-btn is-primary x12-nav-next is-end" onClick={finishDeck}>
          <span>Dersi bitir</span><Check aria-hidden />
        </button>
      )}
    </nav>
  );

  /* ---- v12: Notlarım bölmesi (canvas lp-notes / nt): başlık + hızlı ekleme + not ---- */
  const deckNotePanel = (closeOnJump: boolean) => (
    <DeckNotePanel
      deckId={deck.id}
      deckTitle={deckName(deck)}
      discipline={deck.discipline}
      stepNumber={step.number}
      stepTitle={String((step.slide as any)?.title || '').trim() || `Slayt ${step.slide.slideNumber}`}
      spots={step.spots}
      bullets={step.bullets.map((b: any) => [b.title, b.desc].filter(Boolean).join(': '))}
      onJump={(num) => {
        const i = steps.findIndex((x) => x.number === num);
        if (i >= 0) { goTo(i); if (closeOnJump) setSheet(null); }
      }}
    />
  );
  const notesPaneV12 = (inline: boolean) => (
    <section className={`x12-notes ${inline ? 'is-inline' : 'is-docked'}`} aria-label="Notlarım">
      <div className="x12-notes-h">
        <h2>Notlarım</h2>
        <span className="x12-meta">Bu ders · yalnız sen</span>
        <button type="button" className="ls-btn is-icon is-ghost" onClick={() => setSheet(null)} aria-label="Notlarımı kapat"><X aria-hidden /></button>
      </div>
      {deckNotePanel(false)}
    </section>
  );

  /* ---- v12 Stüdyo: solda ders, sağda yapışkan Pekiştir paneli (tek etkin blok) ---- */
  const StudioArticle = (s: LessonStep) => (
    <div className="x12-studio">
      <div className="x12-studio-l">
        <StepHead step={s} total={n} sectionName={sections[s.section]?.name} deckId={deck.id} />
        <StepBody step={s} deckId={deck.id} />
        <StepSocial step={s} />
      </div>
      {(practice.length > 0 || notesDocked) && (
        <aside className="x12-studio-r" aria-label="Pekiştir">
          {notesDocked && notesPaneV12(true)}
          <PracticeSet step={s} items={practice} jump={practiceJump} onAllDone={() => markDone(s.number)} onResult={(i, item, r) => recordIx(s, i, item, r)} />
        </aside>
      )}
    </div>
  );

  const FlowArticle = (s: LessonStep, withPractice: boolean) => (
    <>
      <StepHead step={s} total={n} sectionName={v12 ? sections[s.section]?.name : undefined} deckId={deck.id} />
      <StepBody step={s} deckId={deck.id} />
      <StepSocial step={s} />
      {withPractice && <PracticeSet step={s} items={s.index === index ? practice : practiceOf(s)} jump={s.index === index ? practiceJump : null} onAllDone={() => markDone(s.number)} onResult={(i, item, r) => recordIx(s, i, item, r)} />}
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
        <DeckPdfViewer deck={deck} currentSlideNumber={step.slide.slideNumber} currentSlide={step.slide} targetPage={pdfPage} targetPageRange={pdfLoc.pageRange} onToggleSplitView={() => setViewMode('split')} onPageChange={onPdfPage} />
      </div>
    ) : viewMode === 'split' ? (
      <SplitPane
        left={
          <div className="ls-split-l" ref={mainRef} onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
            <article className={`ls-col ${dir > 0 ? 'ls-enter-r' : 'ls-enter-l'}`} key={index} data-step={index}>
              {FlowArticle(step, true)}
              {!v12 && FlowNav}
            </article>
            {v12 && NavV12}
          </div>
        }
        right={
          <div className="ls-split-r">
            <DeckPdfViewer deck={deck} currentSlideNumber={step.slide.slideNumber} currentSlide={step.slide} targetPage={pdfPage} targetPageRange={pdfLoc.pageRange} isSplitView onToggleSplitView={() => setViewMode('pdf')} onPageChange={onPdfPage} />
          </div>
        }
      />
    ) : layout === 'A' || v12 ? (
      <div className={`ls-A ${outlineOpen && railInline && !immersive ? 'has-outline' : ''} ${notesDocked && !studioV12 ? 'x12-has-notes' : ''} ${studioV12 ? 'x12-is-studio' : ''}`}>
        {outlineOpen && railInline && !immersive && (
          <nav id="lv-rail" className="ls-A-outline lv-rail" aria-label="Slaytlar">
            <LessonRail steps={steps} sections={sections} current={index} done={done} onPick={goTo} />
          </nav>
        )}
        <main className="ls-A-main" ref={mainRef} onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
          {flowScroll ? (
            <div className="ls-col is-flow">
              {steps.map((s, i) => (
                <article key={i} ref={(el) => { flowRefs.current[i] = el; }} className="ls-flow-step" data-step={i} aria-label={`Adım ${s.number}`}>
                  {FlowArticle(withGlossaryTerms(s, glossaryList as any), true)}
                </article>
              ))}
            </div>
          ) : (
            <article className={`ls-col ${studioV12 ? 'x12-studio-col' : ''} ${dir > 0 ? 'ls-enter-r' : 'ls-enter-l'}`} key={index} data-step={index}>
              {studioV12 ? StudioArticle(step) : FlowArticle(step, true)}
              {!v12 && FlowNav}
            </article>
          )}
          {Dock}
          {v12 && !flowScroll && NavV12}
        </main>
        {notesDocked && !studioV12 && notesPaneV12(false)}
      </div>
    ) : (
      <div className="ls-B">
        <div className="ls-B-stage">
          <article className={`ls-B-card ${dir > 0 ? 'ls-enter-r' : 'ls-enter-l'}`} key={index}>
            <div className="ls-B-head"><StepHead step={step} total={n} deckId={deck.id} /></div>
            <div className="ls-B-body" ref={mainRef} onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
              <StepBody step={step} deckId={deck.id} />
              <StepSocial step={step} />
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
                return <div key={k} data-q={qAnchor} className="ls-anchor"><PracticeCard item={p} target={practiceTarget(step, p, i)} done={doneIx.has(k)} onDone={(r) => { if (r) recordIx(step, i, p, r); onIxDone(k, practice.length); }} className="ls-enter-up" style={{ animationDelay: `${Math.min(i, 6) * 50}ms` }} /></div>;
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
      className={`ls-root ${marking ? 'is-marking' : ''} ${recall ? 'ms-recall' : ''} ${immersive ? 'is-immersive' : ''} ${focusOn ? 'is-focus' : ''} ${layout === 'B' ? 'is-B' : 'is-A'} ${zoom.scale !== 1 ? 'is-zoomed' : ''} ${zoom.gestures ? 'has-pinch' : ''}`}
      style={{ ['--ls-zoom' as string]: zoom.scale }}
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
      <SocialProvider value={socialCtx}>
      {immersive && (
        <button type="button" className="ls-exit-immersive" onClick={toggleFullscreen} aria-label="Tam ekrandan çık" title="Tam ekrandan çık (Esc)">
          <Minimize2 aria-hidden /><span>Küçült</span>
        </button>
      )}
      {topBar}
      <FocusSession
        deckId={deck.id}
        deckTitle={deckName(deck)}
        steps={steps}
        sections={sections}
        index={index}
        done={done}
        setupOpen={focusSetup}
        onSetupClose={() => setFocusSetup(false)}
        onActiveChange={setFocusOn}
        onJump={(num) => {
          const i = steps.findIndex((x) => x.number === num);
          if (i >= 0) goTo(i);
        }}
        onReview={onOpenReview ? () => onOpenReview(deck.id) : undefined}
      />
      {markingBar}
      {zoomBadge > 0 && <div className="ls-zoom-badge" aria-hidden key={zoomBadge}>%{Math.round(zoom.scale * 100)}</div>}
      <div className="ls-stage" ref={stageRef}>
        {focusBand}
        {stage}
      </div>
      {isPhone && (
        <nav className="lv-bottombar" aria-label="Slayt gezinme">
          <button type="button" className="lv-bb-btn" onClick={prev} disabled={index === 0} aria-label="Önceki slayt"><ChevronLeft aria-hidden />Önceki</button>
          <button type="button" className="lv-bb-count" onClick={() => setOutlineMobile(true)} aria-label={`Slayt ${index + 1} / ${n} — slayt listesini aç`} aria-haspopup="dialog">
            <b>{index + 1}</b><i>/</i>{n}
          </button>
          {index < n - 1 ? (
            <button type="button" className="lv-bb-btn is-primary" onClick={next} aria-label="Sonraki slayt">Sonraki<ChevronRight aria-hidden /></button>
          ) : (
            <button type="button" className="lv-bb-btn is-ok" onClick={() => { markDone(step.number); toast.success('Ders tamamlandı', `${deckName(deck)} bitti.`); }}>Bitir<Check aria-hidden /></button>
          )}
        </nav>
      )}

      <Sheet open={outlineMobile} onClose={() => setOutlineMobile(false)} title="Slaytlar" subtitle={`${index + 1} / ${n} · ${deckName(deck)}`} size="full" width={480}>
        <nav className="lv-rail is-sheet" aria-label="Slaytlar">
          <LessonRail steps={steps} sections={sections} current={index} done={done} onPick={goTo} />
        </nav>
      </Sheet>

      {sheet && !notesDocked && (
        <>
          <button type="button" className="ls-scrim is-right" aria-label="Paneli kapat" onClick={() => setSheet(null)} />
          <aside className="ls-side-sheet" aria-label={sheet === 'ai' ? 'Asistana sor' : sheet === 'mine' ? 'Notlarım' : 'Ders notları'}>
            <div className="ls-drawer-h">
              <b>{sheet === 'ai' ? 'Asistana sor' : sheet === 'mine' ? 'Notlarım' : 'Ders notları'}</b>
              <button type="button" className="ls-btn is-icon is-ghost" onClick={() => setSheet(null)} aria-label="Kapat"><X aria-hidden /></button>
            </div>
            <div className="ls-side-sheet-b">
              {sheet === 'ai' ? (
                <AskAi key={step.number} deck={deck} slide={step.slide} />
              ) : sheet === 'mine' ? (
                deckNotePanel(true)
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
      <ReportSheet
        req={reportReq}
        onClose={() => setReportReq(null)}
        onCreated={(t) => {
          setReportReq(null);
          setThreadOpen(t.id);
        }}
      />
      <ThreadSheet
        threadId={threadOpen}
        onClose={() => setThreadOpen(null)}
        onJump={(num) => {
          const i = steps.findIndex((x) => x.number === num);
          setThreadOpen(null);
          if (i >= 0 && i !== index) goTo(i);
          window.setTimeout(() => {
            const el = rootRef.current?.querySelector<HTMLElement>(`${i >= 0 ? `[data-step="${i}"] ` : ''}.ls-sx-flag`);
            if (el) scrollInto(el, 'center', true);
          }, 450);
        }}
      />
      </SocialProvider>
      </FeedbackProvider>
    </div>
  );
};
