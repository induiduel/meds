/**
 * PDF Stüdyosu: çıkmış sorular, soru havuzu, örnek sorular, Öğren dersleri, mini sorular ve ders özetleri
 * için dinamik PDF. Ayarlar dört adımda toplanır: Kaynak (ne basılacak) → Düzen (gruplama, sıralama, cevapların
 * yeri, içindekiler) → Görünüm (şablon, yazı, sütun, sayfaya sığdırma) → Sayfa (kâğıt, yön, kenar boşluğu).
 * Sağdaki önizleme indirilecek belgenin aynısıdır (bkz. pdfDocument.ts). Telefonda tek sütun: Ayarlar /
 * Önizleme arasında alttaki çubuktan geçilir, "PDF indir" her zaman altta durur.
 *
 * Sınıf öneki `ps-` (pdf.css). Belge içindeki bloklar `pd-` önekini kullanır.
 */
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  X, Download, FileText, FileDown, FileCode, GraduationCap, RefreshCw, EyeOff, BookOpenCheck, Grid3x3, Check, ChevronDown,
  Archive, Users, Target, HelpCircle, BookMarked, Printer, Zap, Eye, MonitorSmartphone, ChevronLeft, ChevronRight, Shuffle,
  RectangleVertical, RectangleHorizontal, SlidersHorizontal, Minus, Plus,
} from 'lucide-react';
import type { Committee, QuestionItem } from '../../types';
import { ApiService, getCustomApiUrl } from '../../services/api';
import { normalizeDonem3Discipline, isDonem3Question } from '../../data/curriculumData';
import { DECK_CATALOG, loadDeck, deckName, loadDeckCatalog } from '../../data/deckStore';
import type { InteractiveDeck } from '../learn/InteractiveDeckView';
import { buildSteps, buildSections, loadKazanimIndex, type DeckKazanim } from '../learn/lesson/lessonModel';
import { IX_META } from '../learn/lesson/LessonBlocks';
import { BlurOverlay, PaperLoader } from '../ui/Animations';
import { toast } from '../ui/Toast';
import summariesMeta from '../../data/summaries_meta.json';
import {
  buildDocument, renderMarkup, serverPdfAvailable, renderPdfOnServer, downloadBlob, printDocument, downloadHtml, safeFileName,
  computeFitZoom, estimatePages, normalizePage, pageGeometry, pageLabel,
  PAPER, PAPER_ORDER, MARGINS, TEMPLATES, DEFAULT_PAGE, ZOOM, DESIGNS, DESIGN_ORDER,
  type PageSettings, type FontScale, type DocumentOptions, type TemplateId, type MarginPreset, type FitMode, type PaperSize, type PdfDesign,
} from './pdfDocument';
import {
  fromPastQuestion, fromPoolQuestion, loadOrnekQuestions, miniQuestionsFromDeck, ORNEK_INDEX, COMMITTEE_NAME, sortYears,
  type PdfQuestion,
} from './pdfSources';
import { arrangeQuestions, attachDeckKazanim, GROUP_LABEL, SORT_LABEL, type GroupBy, type GroupOrder, type SortBy } from './pdfOrder';
import {
  QuestionDoc, normalizeQ, type QuestionDocOptions, type OptionNotes, type BookletMode, type AnswersAt, type Numbering,
} from './PdfQuestionDoc';
import { LessonDoc, IX_TYPES, type LessonDocOptions, type IxType, type AnswerMode } from './PdfLessonDoc';
import { SummaryDoc, type SummaryDocOptions, type SummaryForPdf, type SummaryQuestions } from './PdfSummaryDoc';
import type { CoverInfo } from './PdfParts';
import './pdf.css';
// Katalog tembel yüklenir; bu modül eşzamanlı okuduğundan yüklenirken hazır olmasını bekle.
await loadDeckCatalog().catch(() => undefined);

export type PdfContentKind = 'past' | 'pool' | 'ornek' | 'learn' | 'mini' | 'summary';

export interface PdfStudioProps {
  isOpen: boolean;
  onClose: () => void;
  committee?: Committee;
  committees?: Committee[];
  questions: QuestionItem[];
  /** Öğren'den açılınca bu destenin bu adımı seçili gelir */
  initialSlide?: { deckId: string; slideNumber: number } | null;
  /** Açıldığı sayfaya göre başlangıç içeriği */
  initialContent?: PdfContentKind;
}

const KINDS: { id: PdfContentKind; label: string; hint: string; icon: React.ElementType }[] = [
  { id: 'past', label: 'Çıkmış', hint: 'Geçmiş sınav soruları', icon: Archive },
  { id: 'pool', label: 'Havuz', hint: 'Öğrencilerin topladığı', icon: Users },
  { id: 'ornek', label: 'Örnek soru', hint: 'Kazanım temelli', icon: Target },
  { id: 'learn', label: 'Öğren', hint: 'Ders adımları', icon: GraduationCap },
  { id: 'mini', label: 'Mini soru', hint: 'Destedeki sorular', icon: HelpCircle },
  { id: 'summary', label: 'Ders özeti', hint: 'Kurul özetleri', icon: BookMarked },
];
const isQuestionKind = (k: PdfContentKind) => k === 'past' || k === 'pool' || k === 'ornek' || k === 'mini';

type StepId = 'source' | 'layout' | 'look' | 'page';
const STEPS: { id: StepId; label: string }[] = [
  { id: 'source', label: 'Kaynak' },
  { id: 'layout', label: 'Düzen' },
  { id: 'look', label: 'Görünüm' },
  { id: 'page', label: 'Sayfa' },
];

/* ---------------------------------------------------------------------------
 * Ayarlar: belge ayarları (profil eşitlemesine giren v2 anahtarları) ve seçim (yalnız bu cihaz)
 * ------------------------------------------------------------------------- */
const PRESETS: { id: string; label: string; hint: string; icon: React.ElementType; apply: Partial<QuestionDocOptions> }[] = [
  { id: 'student', label: 'Öğrenci', hint: 'Cevapsız, optik form', icon: EyeOff, apply: { mode: 'student', answerKey: false, opticForm: true, cover: true, columns: 2, writeSpace: false, questionPerPage: false } },
  { id: 'solution', label: 'Çözümlü', hint: 'Cevap ve açıklama altında', icon: BookOpenCheck, apply: { mode: 'solution', markCorrect: true, explanation: true, optionNotes: 'inline', answersAt: 'inline', answerKey: true, opticForm: false, columns: 1 } },
  { id: 'review', label: 'Hızlı tekrar', hint: 'Doğru şık işaretli, sıkı', icon: Zap, apply: { mode: 'solution', markCorrect: true, explanation: false, optionNotes: 'off', refs: false, answersAt: 'inline', answerKey: false, opticForm: false, columns: 2, cover: false, questionPerPage: false } },
  { id: 'exam', label: 'Deneme', hint: 'Sorular önde, çözüm sonda', icon: FileText, apply: { mode: 'solution', markCorrect: true, explanation: true, optionNotes: 'analysis', answersAt: 'end', answerKey: true, opticForm: true, columns: 2, cover: true, links: true } },
  { id: 'key', label: 'Anahtar', hint: 'Yalnız cevaplar', icon: Grid3x3, apply: { mode: 'key', answerKey: true, opticForm: false, cover: false } },
];
const matchesPreset = (o: QuestionDocOptions, p: Partial<QuestionDocOptions>) => (Object.keys(p) as (keyof QuestionDocOptions)[]).every((k) => o[k] === p[k]);

const DEFAULT_L: LessonDocOptions = {
  narrative: true, keyPoints: true, tables: true, visuals: true, teacher: true, spots: true, tips: true, terms: false, cards: true,
  interactives: [...IX_TYPES], answers: 'shown', optionNotes: true, stepPerPage: false, sectionTitles: true, toc: false, cover: false,
};
const DEFAULT_S: SummaryDocOptions = { keyPoints: true, tables: true, callouts: true, questions: 'answered', toc: true, cover: false };

interface Selection {
  kind: PdfContentKind;
  committeeId: string;
  year: string;
  discipline: string;
  topic: string;
  kazanim: string;
  onlyAnswered: boolean;
  onlyExplained: boolean;
  onlyAudited: boolean;
  limit: number;
  ornekDers: string;
  ornekLevels: string[];
  includeBranching: boolean;
  deckId: string;
  sumKurul: number;
}
const SEL_KEY = 'medsoru_pdf_sel_v1';
const readSaved = <T,>(key: string): Partial<T> | null => {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as Partial<T>) : null;
  } catch {
    return null;
  }
};

function usePersisted<T extends object>(key: string, normalize: (raw: any) => T): [T, (patch: Partial<T>) => void] {
  const [v, setV] = useState<T>(() => normalize(readSaved<T>(key)));
  const set = useCallback((patch: Partial<T>) => setV((p) => ({ ...p, ...patch })), []);
  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(v));
    } catch {}
  }, [key, v]);
  return [v, set];
}

const disciplineGroup = (raw: string) => (raw || 'Diğer').split(/\s*(?:\/|&|,|\sve\s)\s*/)[0].trim() || 'Diğer';
const PREVIEW_Q = 40;
const PREVIEW_STEPS = 8;
const PREVIEW_SUMMARIES = 1;

type SummaryMeta = { id: string; kurul: number; committeeId: string; discipline: string; title: string; instructor?: string; keyPoints: string[] };
const SUMMARY_META = summariesMeta as SummaryMeta[];
const summaryChunks: Record<number, () => Promise<any>> = {
  1: () => import('../../data/summaries/kurul1.json'),
  2: () => import('../../data/summaries/kurul2.json'),
  3: () => import('../../data/summaries/kurul3.json'),
  4: () => import('../../data/summaries/kurul4.json'),
  5: () => import('../../data/summaries/kurul5.json'),
  6: () => import('../../data/summaries/kurul6.json'),
};
async function loadSummary(meta: SummaryMeta): Promise<SummaryForPdf | null> {
  let content = '';
  try {
    const mod = await summaryChunks[meta.kurul]?.();
    const list: any[] = (mod?.default || mod || []) as any[];
    content = list.find((x) => x.id === meta.id)?.content || '';
  } catch {}
  if (!content) {
    try {
      const res = await fetch(`${getCustomApiUrl() || ''}/api/summaries/${encodeURIComponent(meta.id)}`);
      if (res.ok && res.headers.get('content-type')?.includes('json')) content = (await res.json())?.summary?.content || '';
    } catch {}
  }
  return content ? { id: meta.id, title: meta.title, discipline: meta.discipline, kurul: meta.kurul, instructor: meta.instructor, keyPoints: meta.keyPoints || [], content } : null;
}

const fold = (t: string) => t.toLocaleLowerCase('tr-TR').normalize('NFKD').replace(/[̀-ͯ]/g, '');

/** İçerik türüne göre anlamlı gruplama ölçütleri */
const groupChoices = (kind: PdfContentKind): GroupBy[] =>
  kind === 'past'
    ? ['committee', 'discipline', 'topic', 'kazanim', 'year']
    : kind === 'pool'
      ? ['committee', 'discipline', 'topic', 'kazanim', 'year']
      : kind === 'ornek'
        ? ['discipline', 'topic', 'kazanim', 'difficulty']
        : ['group', 'kazanim'];
const GROUP_QUICK: Record<'q' | 'ornek' | 'mini', [GroupBy, GroupBy, string][]> = {
  q: [['none', 'none', 'Yok'], ['discipline', 'none', 'Ders'], ['topic', 'none', 'Konu'], ['kazanim', 'none', 'Kazanım'], ['discipline', 'topic', 'Ders › Konu'], ['topic', 'kazanim', 'Konu › Kazanım'], ['year', 'none', 'Yıl'], ['discipline', 'year', 'Ders › Yıl']],
  ornek: [['none', 'none', 'Yok'], ['topic', 'none', 'Ders'], ['kazanim', 'none', 'Kazanım'], ['topic', 'kazanim', 'Ders › Kazanım'], ['difficulty', 'none', 'Zorluk'], ['kazanim', 'difficulty', 'Kazanım › Zorluk']],
  mini: [['none', 'none', 'Yok'], ['group', 'none', 'Adım'], ['kazanim', 'none', 'Kazanım'], ['kazanim', 'group', 'Kazanım › Adım']],
};
const sortChoices = (kind: PdfContentKind): SortBy[] =>
  kind === 'past' ? ['source', 'year', 'number', 'discipline', 'topic', 'random'] : kind === 'pool' ? ['source', 'year', 'number', 'discipline', 'topic', 'random'] : kind === 'ornek' ? ['source', 'difficulty', 'random'] : ['source', 'random'];

/* =========================================================================== */
export const PdfStudio: React.FC<PdfStudioProps> = ({ isOpen, onClose, committee, questions = [], initialSlide = null, initialContent }) => {
  const saved = useMemo(() => readSaved<Selection>(SEL_KEY) || {}, []);
  const [kind, setKind] = useState<PdfContentKind>(() => (initialSlide ? 'learn' : initialContent || (saved.kind as PdfContentKind) || 'past'));
  const [page, setPage] = usePersisted<PageSettings>('medsoru_pdf_page_v2', normalizePage);
  const [qopt, setQopt] = usePersisted<QuestionDocOptions>('medsoru_pdf_q_v2', normalizeQ);
  const [lopt, setLopt] = usePersisted<LessonDocOptions>('medsoru_pdf_l_v2', (r) => ({ ...DEFAULT_L, ...(r || {}) }));
  const [sopt, setSopt] = usePersisted<SummaryDocOptions>('medsoru_pdf_s_v2', (r) => ({ ...DEFAULT_S, ...(r || {}) }));
  const [step, setStep] = useState<StepId>('source');
  const [mobileView, setMobileView] = useState<'options' | 'preview'>('options');

  // Soru seçimi (açıldığı kurul bağlamı kayıttan önce gelir)
  const [committeeId, setCommitteeId] = useState<string>(committee?.id || saved.committeeId || 'all');
  const [year, setYear] = useState(saved.year || 'all');
  const [discipline, setDiscipline] = useState(saved.discipline || 'all');
  const [topic, setTopic] = useState(saved.topic || 'all');
  const [kazanimFilter, setKazanimFilter] = useState(saved.kazanim || 'all');
  const [search, setSearch] = useState('');
  const [onlyAnswered, setOnlyAnswered] = useState(!!saved.onlyAnswered);
  const [onlyExplained, setOnlyExplained] = useState(!!saved.onlyExplained);
  const [onlyAudited, setOnlyAudited] = useState(!!saved.onlyAudited);
  const [limit, setLimit] = useState<number>(typeof saved.limit === 'number' ? saved.limit : 100);
  const [ornekDers, setOrnekDers] = useState<string>(saved.ornekDers && (saved.ornekDers === 'all' || ORNEK_INDEX.some((r) => r.id === saved.ornekDers)) ? saved.ornekDers : ORNEK_INDEX[0]?.id || '');
  const [ornekLevels, setOrnekLevels] = useState<string[]>(Array.isArray(saved.ornekLevels) && saved.ornekLevels.length ? saved.ornekLevels : ['kolay', 'orta', 'zor']);
  const [includeBranching, setIncludeBranching] = useState(!!saved.includeBranching);

  // Öğren
  const [deckId, setDeckId] = useState<string>(
    initialSlide?.deckId || (saved.deckId && DECK_CATALOG.some((d) => d.id === saved.deckId) ? saved.deckId : DECK_CATALOG[0]?.id || '')
  );
  const [deck, setDeck] = useState<InteractiveDeck | null>(null);
  const [pickedSteps, setPickedSteps] = useState<number[]>(initialSlide ? [initialSlide.slideNumber] : []);
  const [kazIndex, setKazIndex] = useState<Record<string, DeckKazanim[]> | null>(null);

  // Özet
  const [sumKurul, setSumKurul] = useState<number>(() => Number(String(committee?.id || '').match(/kurul(\d)/)?.[1]) || saved.sumKurul || 1);
  const [sumIds, setSumIds] = useState<string[]>([]);

  // Seçimi hatırla
  useEffect(() => {
    try {
      const sel: Selection = { kind, committeeId, year, discipline, topic, kazanim: kazanimFilter, onlyAnswered, onlyExplained, onlyAudited, limit, ornekDers, ornekLevels, includeBranching, deckId, sumKurul };
      localStorage.setItem(SEL_KEY, JSON.stringify(sel));
    } catch {}
  }, [kind, committeeId, year, discipline, topic, kazanimFilter, onlyAnswered, onlyExplained, onlyAudited, limit, ornekDers, ornekLevels, includeBranching, deckId, sumKurul]);

  // Veriler
  const [past, setPast] = useState<any[] | null>(null);
  const [ornek, setOrnek] = useState<PdfQuestion[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);

  // Çıktı
  const [serverOk, setServerOk] = useState<boolean | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [previewHtml, setPreviewHtml] = useState('');
  const [previewMode, setPreviewMode] = useState<'html' | 'pdf'>('html');
  const [pdfPreviewUrl, setPdfPreviewUrl] = useState<string | null>(null);
  const [pageCount, setPageCount] = useState<{ n: number; exact: boolean } | null>(null);
  const [fitInfo, setFitInfo] = useState<{ zoom: number; pages: number; basePages: number } | null>(null);
  const [building, setBuilding] = useState(false);
  const frameBox = useRef<HTMLDivElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const [frameW, setFrameW] = useState(800);

  useEffect(() => {
    if (!isOpen) return;
    serverPdfAvailable().then(setServerOk);
  }, [isOpen]);

  useEffect(() => {
    if (!isOpen) return;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = prev;
    };
  }, [isOpen, onClose]);

  useEffect(() => {
    const el = frameBox.current;
    if (!el) return;
    const ro = new ResizeObserver(() => setFrameW(el.clientWidth));
    ro.observe(el);
    setFrameW(el.clientWidth);
    return () => ro.disconnect();
  }, [isOpen, mobileView]);

  useEffect(() => {
    panelRef.current?.scrollTo({ top: 0 });
  }, [step, kind]);

  /* ---- Veri yükleme ---- */
  useEffect(() => {
    if (!isOpen || kind !== 'past' || past) return;
    let alive = true;
    setLoading(true);
    setLoadError(null);
    ApiService.getPastQuestions()
      .then((data: any[]) => {
        if (!alive) return;
        setPast(
          data
            .filter((q: any) => !q.id?.startsWith('civan-') && !q.tags?.some((t: string) => /civan/i.test(t)))
            .filter(isDonem3Question)
            .map((q: any) => {
              const norm = normalizeDonem3Discipline(q.discipline);
              return norm ? { ...q, discipline: norm } : q;
            })
        );
      })
      .catch(() => alive && setLoadError('Çıkmış sorular yüklenemedi. Bağlantını kontrol edip tekrar dene.'))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [isOpen, kind, past]);

  useEffect(() => {
    if (!isOpen || kind !== 'ornek') return;
    let alive = true;
    setLoading(true);
    setOrnek(null);
    const ids = ornekDers === 'all' ? ORNEK_INDEX.map((r) => r.id) : [ornekDers];
    Promise.all(ids.map(loadOrnekQuestions))
      .then((lists) => alive && setOrnek(lists.flat()))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [isOpen, kind, ornekDers]);

  useEffect(() => {
    if (!isOpen || (kind !== 'learn' && kind !== 'mini') || !deckId) return;
    let alive = true;
    setLoading(true);
    loadDeck<InteractiveDeck>(deckId)
      .then((d) => {
        if (!alive) return;
        setDeck(d);
        if (d && kind === 'learn') setPickedSteps((p) => (p.length && d.slides.some((s) => p.includes(s.slideNumber)) ? p : []));
      })
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [isOpen, kind, deckId]);

  useEffect(() => {
    if (!isOpen || kind !== 'mini' || kazIndex) return;
    let alive = true;
    loadKazanimIndex().then((m) => alive && setKazIndex(m));
    return () => {
      alive = false;
    };
  }, [isOpen, kind, kazIndex]);

  const kurulSummaries = useMemo(() => SUMMARY_META.filter((m) => m.kurul === sumKurul), [sumKurul]);
  useEffect(() => {
    setSumIds((ids) => (ids.some((id) => kurulSummaries.some((m) => m.id === id)) ? ids : kurulSummaries.slice(0, 1).map((m) => m.id)));
  }, [kurulSummaries]);

  /* ---- Öğren adımları ---- */
  const steps = useMemo(() => (deck ? buildSteps(deck) : []), [deck]);
  const sections = useMemo(() => buildSections(steps), [steps]);
  const ixCounts = useMemo(() => {
    const c: Record<string, number> = {};
    steps.forEach((s) => s.interactives.forEach((e) => {
      const t = e.type === 'hidden_table' ? 'interactive_table' : e.type;
      c[t] = (c[t] || 0) + 1;
    }));
    return c;
  }, [steps]);
  const chosenStepCount = pickedSteps.length || steps.length;

  /* ---- Soru havuzu (türe göre) ---- */
  const baseQuestions = useMemo<PdfQuestion[]>(() => {
    if (kind === 'past') return (past || []).map(fromPastQuestion).filter(Boolean) as PdfQuestion[];
    if (kind === 'pool') return questions.map(fromPoolQuestion).filter(Boolean) as PdfQuestion[];
    if (kind === 'ornek') return (ornek || []).filter((q) => !q.difficulty || ornekLevels.includes(q.difficulty));
    if (kind === 'mini' && deck) return attachDeckKazanim(miniQuestionsFromDeck(deck, includeBranching), deck.id, `${deck.title} ${deck.discipline || ''}`, steps, kazIndex);
    return [];
  }, [kind, past, questions, ornek, ornekLevels, deck, includeBranching, steps, kazIndex]);

  const crossKind = kind === 'past' || kind === 'pool';
  const inCommittee = useCallback((q: PdfQuestion) => committeeId === 'all' || q.committeeId === committeeId, [committeeId]);
  const years = useMemo(() => sortYears(baseQuestions.filter(inCommittee).map((q) => q.year || '')), [baseQuestions, inCommittee]);
  const disciplines = useMemo(
    () => [...new Set(baseQuestions.filter(inCommittee).map((q) => q.discipline))].sort((a, b) => a.localeCompare(b, 'tr')),
    [baseQuestions, inCommittee]
  );
  const topics = useMemo(
    () =>
      [...new Set(baseQuestions.filter((q) => inCommittee(q) && (discipline === 'all' || q.discipline === discipline)).map((q) => q.topic || ''))]
        .filter(Boolean)
        .sort((a, b) => a.localeCompare(b, 'tr')),
    [baseQuestions, inCommittee, discipline]
  );
  const kazanimlar = useMemo(() => {
    const m = new Map<string, { text: string; rank: string; n: number }>();
    baseQuestions
      .filter((q) => (!crossKind || inCommittee(q)) && (discipline === 'all' || !crossKind || q.discipline === discipline) && (topic === 'all' || kind !== 'past' || q.topic === topic))
      .forEach((q) => {
        if (!q.kazanim?.text) return;
        const key = q.kazanim.id || q.kazanim.text;
        const cur = m.get(key);
        if (cur) cur.n++;
        else m.set(key, { text: q.kazanim.text, rank: q.kazanim.id || `~${q.kazanim.text}`, n: 1 });
      });
    return [...m.entries()].sort((a, b) => a[1].rank.localeCompare(b[1].rank, 'tr', { numeric: true })).map(([key, v]) => ({ key, ...v }));
  }, [baseQuestions, crossKind, inCommittee, discipline, topic, kind]);

  const filtered = useMemo(() => {
    const needle = fold(search.trim());
    return baseQuestions.filter((q) => {
      if (crossKind && !inCommittee(q)) return false;
      if (kind === 'past' && year !== 'all' && q.year !== year) return false;
      if (crossKind && discipline !== 'all' && q.discipline !== discipline) return false;
      if (kind === 'past' && topic !== 'all' && q.topic !== topic) return false;
      if (kazanimFilter !== 'all') {
        const key = q.kazanim ? q.kazanim.id || q.kazanim.text : '';
        if (kazanimFilter === '?' ? !!key : key !== kazanimFilter) return false;
      }
      if (onlyAnswered && !q.answer) return false;
      if (onlyExplained && !q.explanation && !q.options.some((o) => o.why)) return false;
      if (kind === 'past' && onlyAudited && !q.badges.some((b) => b.label.startsWith('Denetleyici'))) return false;
      if (needle && !fold(`${q.stem} ${q.options.map((o) => o.text).join(' ')} ${q.topic || ''} ${q.kazanim?.text || ''}`).includes(needle)) return false;
      return true;
    });
  }, [baseQuestions, crossKind, kind, inCommittee, year, discipline, topic, kazanimFilter, onlyAnswered, onlyExplained, onlyAudited, search]);

  // Önce yıl yeniden eskiye ve soru no (kaynak sırası), sonra seçilen gruplama/sıralama; en sonda ilk N
  const arranged = useMemo(() => {
    const base = crossKind
      ? [...filtered].sort((a, b) => {
          const ya = a.year && /\d{4}/.test(a.year) ? a.year : '';
          const yb = b.year && /\d{4}/.test(b.year) ? b.year : '';
          return yb.localeCompare(ya, 'tr', { numeric: true }) || (a.number || 0) - (b.number || 0);
        })
      : filtered;
    const allowed = new Set(groupChoices(kind));
    const out = arrangeQuestions(base, {
      group1: allowed.has(qopt.group1) ? qopt.group1 : 'none',
      group2: allowed.has(qopt.group2) ? qopt.group2 : 'none',
      groupOrder: qopt.groupOrder,
      sortBy: sortChoices(kind).includes(qopt.sortBy) ? qopt.sortBy : 'source',
      sortDir: qopt.sortDir,
      seed: qopt.seed,
    });
    return limit > 0 ? out.slice(0, limit) : out;
  }, [filtered, crossKind, kind, qopt.group1, qopt.group2, qopt.groupOrder, qopt.sortBy, qopt.sortDir, qopt.seed, limit]);
  const effectiveQ = useMemo<QuestionDocOptions>(() => {
    const allowed = new Set(groupChoices(kind));
    return {
      ...qopt,
      group1: allowed.has(qopt.group1) ? qopt.group1 : 'none',
      group2: allowed.has(qopt.group2) ? qopt.group2 : 'none',
      numbering: qopt.numbering === 'original' && !crossKind ? 'sequential' : qopt.numbering,
    };
  }, [qopt, kind, crossKind]);

  /* ---- Kapak / başlık bilgisi ---- */
  const coverInfo = useMemo<CoverInfo>(() => {
    const kurul = committeeId !== 'all' ? COMMITTEE_NAME[committeeId] : '';
    if (kind === 'learn' && deck) {
      const ixTotal = steps.filter((s) => !pickedSteps.length || pickedSteps.includes(s.number)).reduce((a, s) => a + s.interactives.length, 0);
      return {
        kicker: `Öğren · ${disciplineGroup(deck.discipline)}`,
        title: deckName(deck, false),
        subtitle: [deck.instructor, deck.committee].filter(Boolean).join(' · ') || undefined,
        stats: [{ value: chosenStepCount, label: 'Adım' }, { value: ixTotal, label: 'Etkileşim' }, { value: lopt.answers === 'shown' ? 'Açık' : lopt.answers === 'end' ? 'Sonda' : 'Gizli', label: 'Cevaplar' }],
        tags: [],
      };
    }
    if (kind === 'summary') {
      return {
        kicker: `Ders özeti · Kurul ${sumKurul}`,
        title: sumIds.length === 1 ? SUMMARY_META.find((m) => m.id === sumIds[0])?.title || 'Ders özeti' : `${COMMITTEE_NAME[`donem3-kurul${sumKurul}`] || `Kurul ${sumKurul}`} ders özetleri`,
        subtitle: sumIds.length === 1 ? SUMMARY_META.find((m) => m.id === sumIds[0])?.instructor : undefined,
        stats: [{ value: sumIds.length, label: 'Ders' }],
        tags: [],
      };
    }
    const label = kind === 'past' ? 'Çıkmış sorular' : kind === 'pool' ? 'Soru havuzu' : kind === 'ornek' ? 'Örnek sorular' : 'Mini sorular';
    const title =
      kind === 'ornek'
        ? ornekDers === 'all' ? 'Kurul 1 · tüm dersler' : ORNEK_INDEX.find((r) => r.id === ornekDers)?.konu || 'Örnek sorular'
        : kind === 'mini'
          ? deck ? deckName(deck, false) : 'Mini sorular'
          : [discipline !== 'all' ? discipline : '', kurul.split(' · ')[1] || ''].filter(Boolean).join(' · ') || 'Tüm kurullar';
    const kzLabel = kazanimFilter === 'all' ? '' : kazanimFilter === '?' ? 'Kazanımı belirsiz' : kazanimlar.find((k) => k.key === kazanimFilter)?.text || '';
    const tags = [
      kurul && crossKind ? kurul : '',
      year !== 'all' && kind === 'past' ? year : '',
      topic !== 'all' && kind === 'past' ? topic : '',
      kzLabel ? (kzLabel.length > 60 ? `${kzLabel.slice(0, 58)}…` : kzLabel) : '',
      search ? `“${search}”` : '',
    ].filter(Boolean);
    return {
      kicker: label,
      title,
      subtitle: kind === 'ornek' ? ORNEK_INDEX.find((r) => r.id === ornekDers)?.ogretim_uyesi : undefined,
      stats: [
        { value: arranged.length, label: 'Soru' },
        ...(qopt.mode !== 'key' ? [{ value: `~${Math.max(1, Math.round(arranged.length * 1.1))} dk`, label: 'Süre' }] : []),
        { value: arranged.filter((x) => x.q.answer).length, label: 'Cevaplı' },
      ],
      tags,
      studentFields: qopt.mode === 'student',
    };
  }, [kind, deck, steps, pickedSteps, chosenStepCount, lopt.answers, sumKurul, sumIds, committeeId, discipline, year, topic, kazanimFilter, kazanimlar, search, arranged, qopt.mode, ornekDers, crossKind]);

  const docOptions: DocumentOptions = useMemo(
    () => ({ title: coverInfo.title, runningHead: `${coverInfo.kicker} · ${coverInfo.title}`, ...page }),
    [coverInfo, page]
  );

  /** İçeriğin HTML gövdesi; önizlemede kısaltılır. */
  const buildBody = useCallback(
    async (preview: boolean): Promise<string | null> => {
      if (isQuestionKind(kind)) {
        if (!arranged.length) return null;
        const items = preview ? arranged.slice(0, PREVIEW_Q) : arranged;
        return renderMarkup(<QuestionDoc items={items} options={effectiveQ} cover={coverInfo} />);
      }
      if (kind === 'learn') {
        if (!deck) return null;
        let nums = pickedSteps.length ? pickedSteps : steps.map((s) => s.number);
        if (preview) nums = nums.slice(0, PREVIEW_STEPS);
        return renderMarkup(<LessonDoc deck={deck} slideNumbers={nums} options={lopt} cover={coverInfo} />);
      }
      if (kind === 'summary') {
        const ids = preview ? sumIds.slice(0, PREVIEW_SUMMARIES) : sumIds;
        const metas = ids.map((id) => SUMMARY_META.find((m) => m.id === id)).filter(Boolean) as SummaryMeta[];
        const list = (await Promise.all(metas.map(loadSummary))).filter(Boolean) as SummaryForPdf[];
        if (!list.length) return null;
        return renderMarkup(<SummaryDoc summaries={list} options={sopt} cover={coverInfo} />);
      }
      return null;
    },
    [kind, arranged, effectiveQ, coverInfo, deck, pickedSteps, steps, lopt, sumIds, sopt]
  );

  const previewTruncated =
    isQuestionKind(kind) ? arranged.length > PREVIEW_Q : kind === 'learn' ? chosenStepCount > PREVIEW_STEPS : kind === 'summary' ? sumIds.length > PREVIEW_SUMMARIES : false;

  /* ---- Önizleme ---- */
  const geo = pageGeometry(page);
  const pageWidthPx = (geo.w / 25.4) * 96 + 48;
  const previewZoom = Math.min(1, Math.max(0.22, (frameW - 8) / pageWidthPx));
  useEffect(() => {
    if (!isOpen || loading) return;
    let alive = true;
    setBuilding(true);
    const t = setTimeout(async () => {
      try {
        const body = await buildBody(true);
        if (!alive) return;
        if (!body) {
          setPreviewHtml('');
          setPageCount(null);
          setFitInfo(null);
          return;
        }
        let opts = docOptions;
        if (page.fit === 'pages') {
          const full = previewTruncated ? await buildBody(false) : body;
          if (!alive || !full) return;
          const r = await computeFitZoom(full, docOptions);
          if (!alive) return;
          setFitInfo(r);
          opts = { ...docOptions, fitZoom: r.zoom };
        } else setFitInfo(null);
        const html = buildDocument(body, opts);
        setPreviewHtml(html);
        if (previewMode === 'pdf' && serverOk) {
          const blob = await renderPdfOnServer(html, docOptions.title, 'onizleme.pdf');
          if (!alive) return;
          setPdfPreviewUrl((old) => {
            if (old) URL.revokeObjectURL(old);
            return URL.createObjectURL(blob);
          });
          const raw = await blob.text();
          const n = (raw.match(/\/Type\s*\/Page[^s]/g) || []).length;
          setPageCount(n ? { n, exact: !previewTruncated } : null);
        } else if (!previewTruncated) {
          const n = await estimatePages(body, opts);
          if (alive) setPageCount({ n, exact: false });
        } else setPageCount(null);
      } catch (e) {
        console.warn('PDF önizlemesi oluşturulamadı', e);
      } finally {
        if (alive) setBuilding(false);
      }
    }, previewMode === 'pdf' ? 700 : page.fit === 'pages' ? 500 : 260);
    return () => {
      alive = false;
      clearTimeout(t);
    };
  }, [isOpen, loading, buildBody, docOptions, previewMode, serverOk, page.fit, previewTruncated]);

  useEffect(() => () => {
    if (pdfPreviewUrl) URL.revokeObjectURL(pdfPreviewUrl);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const previewDoc = useMemo(
    () => (previewHtml ? previewHtml.replace('</head>', `<style>html{zoom:${previewZoom.toFixed(3)}}body{padding:16px 0 32px!important}</style></head>`) : ''),
    [previewHtml, previewZoom]
  );

  /* ---- Çıktı ---- */
  const fileName = `${safeFileName(`${coverInfo.kicker}_${coverInfo.title}`)}_${PAPER[page.paper].label}${page.orientation === 'landscape' ? '_yatay' : ''}.pdf`;
  const fullDocument = async () => {
    const body = await buildBody(false);
    if (!body) throw new Error('Seçimde içerik yok');
    if (page.fit === 'pages') {
      setBusy('Sayfaya sığdırılıyor…');
      const r = await computeFitZoom(body, docOptions);
      return buildDocument(body, { ...docOptions, fitZoom: r.zoom });
    }
    return buildDocument(body, docOptions);
  };

  const handleDownload = async () => {
    setBusy('PDF hazırlanıyor…');
    try {
      const html = await fullDocument();
      setBusy('PDF hazırlanıyor…');
      if (serverOk) {
        try {
          const blob = await renderPdfOnServer(html, docOptions.title, fileName);
          downloadBlob(blob, fileName);
          toast.success('PDF indirildi', fileName);
          return;
        } catch (err: any) {
          toast.error('Sunucu PDF basamadı', `${err?.message || ''} Tarayıcının yazdırma penceresi açılıyor; “PDF olarak kaydet”i seç.`);
        }
      }
      await printDocument(html);
    } catch (err: any) {
      toast.error('PDF oluşturulamadı', err?.message || 'Lütfen tekrar dene.', { label: 'Tekrar dene', onClick: () => handleDownload() });
    } finally {
      setBusy(null);
    }
  };
  const handlePrint = async () => {
    setBusy('Yazdırma hazırlanıyor…');
    try {
      await printDocument(await fullDocument());
    } catch (err: any) {
      toast.error('Yazdırılamadı', err?.message || '');
    } finally {
      setBusy(null);
    }
  };
  const handleHtml = async () => {
    try {
      downloadHtml(await fullDocument(), fileName.replace(/\.pdf$/, '.html'));
    } catch (err: any) {
      toast.error('HTML oluşturulamadı', err?.message || '');
    } finally {
      setBusy(null);
    }
  };

  if (!isOpen) return null;

  /* ---- Adım özetleri ---- */
  const canInlinePdf = typeof navigator === 'undefined' || (navigator as any).pdfViewerEnabled !== false;
  const itemCount = isQuestionKind(kind) ? arranged.length : kind === 'learn' ? (deck ? chosenStepCount : 0) : sumIds.length;
  const unit = isQuestionKind(kind) ? 'soru' : kind === 'learn' ? 'adım' : 'özet';
  const kindLabel = KINDS.find((k) => k.id === kind)?.label || '';
  const groupText = isQuestionKind(kind)
    ? [effectiveQ.group1, effectiveQ.group2].filter((g) => g !== 'none').map((g) => GROUP_LABEL[g]).join(' › ') || 'Gruplama yok'
    : kind === 'learn'
      ? lopt.answers === 'end' ? 'Cevaplar sonda' : lopt.answers === 'hidden' ? 'Çalışma kâğıdı' : 'Cevaplar açık'
      : sopt.toc ? 'İçindekilerle' : 'Düz';
  const stepSummary: Record<StepId, string> = {
    source: loading ? 'Yükleniyor…' : `${kindLabel} · ${itemCount} ${unit}`,
    layout: groupText,
    look: `${DESIGNS[page.design].label.replace(/ \(.*\)/, '')} · ${TEMPLATES[page.template].label}${page.fit === 'pages' ? ` · ${page.fitPages} sayfaya` : page.fit === 'width' ? ' · genişliğe' : ''}`,
    page: `${pageLabel(page)} · ${MARGINS[page.margins].label.toLocaleLowerCase('tr-TR')}`,
  };
  const stepIndex = STEPS.findIndex((s) => s.id === step);
  const pagesText = pageCount ? `${pageCount.exact ? '' : '≈ '}${pageCount.n} sayfa${previewTruncated && previewMode === 'pdf' ? ' (önizleme)' : ''}` : '';

  return createPortal(
    <div className="ms-overlay ps-overlay" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div role="dialog" aria-modal="true" aria-labelledby="ps-title" aria-busy={!!busy} className="ps-dialog ms-keep-shell" data-view={mobileView}>
        {/* ---------- Üst ---------- */}
        <header className="ps-head">
          <span className="ps-logo" aria-hidden="true"><FileDown /></span>
          <div className="ps-head-t">
            <h2 id="ps-title">PDF stüdyosu</h2>
            <p>{serverOk === false ? 'Tarayıcının yazdırma penceresiyle kaydedilir' : 'Ekrandaki tasarımla, tıklanabilir bağlantılarla'}</p>
          </div>
          <button type="button" className="ps-icon-btn" onClick={onClose} aria-label="PDF stüdyosunu kapat">
            <X />
          </button>
        </header>

        <div className="ps-body">
          {/* ---------- Ayarlar ---------- */}
          <aside className="ps-side" aria-label="PDF ayarları">
            <nav className="ps-steps" aria-label="Adımlar">
              {STEPS.map((s, i) => (
                <button key={s.id} type="button" className={`ps-step ${step === s.id ? 'is-on' : ''}`} aria-current={step === s.id ? 'step' : undefined} onClick={() => setStep(s.id)}>
                  <span className="ps-step-n">{i + 1}</span>
                  <span className="ps-step-t">
                    <b>{s.label}</b>
                    <small>{stepSummary[s.id]}</small>
                  </span>
                </button>
              ))}
            </nav>

            <div className="ps-panel" ref={panelRef}>
              {step === 'source' && (
                <>
                  <Group title="İçerik">
                    <div className="ps-kinds" role="radiogroup" aria-label="İçerik türü">
                      {KINDS.map(({ id, label, hint, icon: Icon }) => (
                        <button key={id} type="button" role="radio" aria-checked={kind === id} className={`ps-choice ${kind === id ? 'is-on' : ''}`} onClick={() => setKind(id)}>
                          <span className="ps-choice-ic"><Icon /></span>
                          <span className="ps-choice-t"><b>{label}</b><small>{hint}</small></span>
                        </button>
                      ))}
                    </div>
                  </Group>
                  {isQuestionKind(kind) && (
                    <QuestionSource
                      kind={kind}
                      sel={{
                        committeeId, setCommitteeId, years, year, setYear, disciplines, discipline, setDiscipline, topics, topic, setTopic,
                        kazanimlar, kazanim: kazanimFilter, setKazanim: setKazanimFilter,
                        search, setSearch, onlyAnswered, setOnlyAnswered, onlyExplained, setOnlyExplained, onlyAudited, setOnlyAudited,
                        limit, setLimit, ornekDers, setOrnekDers, ornekLevels, setOrnekLevels, includeBranching, setIncludeBranching,
                        deckId, setDeckId, total: baseQuestions.length, matched: filtered.length,
                      }}
                    />
                  )}
                  {kind === 'learn' && (
                    <LessonSource
                      deckId={deckId}
                      setDeckId={(id) => {
                        setDeckId(id);
                        setPickedSteps([]);
                      }}
                      steps={steps.map((s) => ({ number: s.number, title: s.title, section: s.section, checkpoint: s.checkpoint }))}
                      sections={sections.map((s) => ({ index: s.index, name: s.name, numbers: s.steps.map((i) => steps[i].number) }))}
                      picked={pickedSteps}
                      setPicked={setPickedSteps}
                    />
                  )}
                  {kind === 'summary' && <SummarySource kurul={sumKurul} setKurul={setSumKurul} list={kurulSummaries} picked={sumIds} setPicked={setSumIds} />}
                  {loadError && <p className="ps-error">{loadError}</p>}
                </>
              )}

              {step === 'layout' && (
                <>
                  {isQuestionKind(kind) && <QuestionLayout kind={kind} o={qopt} set={setQopt} />}
                  {kind === 'learn' && <LessonLayout o={lopt} set={setLopt} />}
                  {kind === 'summary' && <SummaryLayout o={sopt} set={setSopt} />}
                </>
              )}

              {step === 'look' && (
                <>
                  <LookCommon page={page} setPage={setPage} fitInfo={fitInfo} unit={unit} />
                  {isQuestionKind(kind) && <QuestionLook o={qopt} set={setQopt} />}
                  {kind === 'learn' && <LessonLook o={lopt} set={setLopt} ixCounts={ixCounts} />}
                  {kind === 'summary' && <SummaryLook o={sopt} set={setSopt} />}
                </>
              )}

              {step === 'page' && <PageStep page={page} setPage={setPage} />}

              <div className="ps-panel-nav">
                <button type="button" className="ps-btn" disabled={stepIndex === 0} onClick={() => setStep(STEPS[stepIndex - 1].id)}>
                  <ChevronLeft /> Geri
                </button>
                {stepIndex < STEPS.length - 1 ? (
                  <button type="button" className="ps-btn is-soft" onClick={() => setStep(STEPS[stepIndex + 1].id)}>
                    Sonraki: {STEPS[stepIndex + 1].label} <ChevronRight />
                  </button>
                ) : (
                  <button type="button" className="ps-btn is-soft ps-only-mobile" onClick={() => setMobileView('preview')}>
                    Önizlemeye geç <Eye />
                  </button>
                )}
              </div>
            </div>
          </aside>

          {/* ---------- Önizleme ---------- */}
          <section className="ps-preview" aria-label="Önizleme">
            <div className="ps-pv-bar">
              <span className="ps-pv-h">Önizleme</span>
              <span className="ps-pill">{pageLabel(page)}</span>
              {building ? (
                <span className="ps-pill is-accent"><RefreshCw className="ps-spin" /> Güncelleniyor</span>
              ) : (
                pagesText && <span className="ps-pill">{pagesText}</span>
              )}
              <span className="ps-grow" />
              <div role="radiogroup" aria-label="Tasarım" className="ps-seg is-small" title="PDF'in tasarım sürümü">
                {DESIGN_ORDER.map((id) => (
                  <button key={id} type="button" role="radio" aria-checked={page.design === id} className={page.design === id ? 'is-on' : ''} onClick={() => setPage({ design: id })}>
                    {id === 'v12' ? 'Net · v12' : 'Klasik · v10'}
                  </button>
                ))}
              </div>
              {serverOk && canInlinePdf && (
                <div role="radiogroup" aria-label="Önizleme türü" className="ps-seg is-small">
                  {(
                    [
                      ['html', 'Hızlı', MonitorSmartphone],
                      ['pdf', 'Gerçek PDF', FileText],
                    ] as const
                  ).map(([id, label, Icon]) => (
                    <button key={id} type="button" role="radio" aria-checked={previewMode === id} className={previewMode === id ? 'is-on' : ''} onClick={() => setPreviewMode(id)}>
                      <Icon /> {label}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <div ref={frameBox} className="ps-frame">
              {previewMode === 'pdf' && pdfPreviewUrl && serverOk ? (
                <iframe key={pdfPreviewUrl} title="PDF önizlemesi" src={`${pdfPreviewUrl}#view=FitH&toolbar=0&navpanes=0`} />
              ) : previewDoc ? (
                <iframe title="Belge önizlemesi" srcDoc={previewDoc} sandbox="allow-same-origin" />
              ) : null}
              <BlurOverlay show={building && !!previewDoc} icon={<PaperLoader size={72} />} label={page.fit === 'pages' ? 'Sayfaya sığdırılıyor…' : 'Önizleme güncelleniyor…'} />
              {!previewDoc && (
                <div className="ps-empty ms-fade-in">
                  {loading || building ? (
                    <>
                      <PaperLoader />
                      <b>Sayfalar diziliyor…</b>
                      <span>Önizleme birazdan burada</span>
                    </>
                  ) : (
                    <>
                      <span className="ps-empty-ic"><Eye /></span>
                      <b>Bu seçimde içerik yok</b>
                      <span>Kaynak adımındaki süzgeçleri gevşet ya da başka bir ders seç.</span>
                      <button type="button" className="ps-btn is-soft" onClick={() => { setStep('source'); setMobileView('options'); }}>Kaynağa dön</button>
                    </>
                  )}
                </div>
              )}
            </div>
            {previewDoc && (
              <p className="ps-note">
                {previewTruncated
                  ? `Önizleme hızlı olsun diye kısaltıldı; indirilen PDF seçimin tamamını (${itemCount} ${unit}) içerir.`
                  : 'Soru numaraları, cevaplar ve içindekiler önizlemede de tıklanabilir.'}
              </p>
            )}
          </section>
        </div>

        <BlurOverlay show={!!busy} fixed={false} icon={<PaperLoader size={96} />} label={busy || ''} hint="Büyük seçimlerde yarım dakikayı bulabilir" />

        {/* ---------- Alt çubuk ---------- */}
        <footer className="ps-foot">
          <div className="ps-seg ps-only-mobile ps-viewseg" role="radiogroup" aria-label="Görünüm">
            <button type="button" role="radio" aria-checked={mobileView === 'options'} className={mobileView === 'options' ? 'is-on' : ''} onClick={() => setMobileView('options')}>
              <SlidersHorizontal /> Ayarlar
            </button>
            <button type="button" role="radio" aria-checked={mobileView === 'preview'} className={mobileView === 'preview' ? 'is-on' : ''} onClick={() => setMobileView('preview')}>
              <Eye /> Önizleme
            </button>
          </div>
          <p className="ps-foot-sum" role="status">
            <b>{loading ? 'Yükleniyor…' : `${itemCount} ${unit}`}</b>
            <span>{[groupText, `${page.design} · ${TEMPLATES[page.template].label}`, pageLabel(page), pagesText].filter(Boolean).join(' · ')}</span>
          </p>
          <button type="button" className="ps-btn ps-hide-mobile" onClick={handlePrint} disabled={!itemCount || !!busy} title="Tarayıcının yazdırma penceresini açar">
            <Printer /> Yazdır
          </button>
          <button type="button" className="ps-btn ps-hide-mobile" onClick={handleHtml} disabled={!itemCount || !!busy} title="İnternetsiz açılabilen tek dosya HTML">
            <FileCode /> HTML
          </button>
          <button type="button" className="ps-btn is-primary" onClick={handleDownload} disabled={!itemCount || !!busy || loading}>
            {busy ? <RefreshCw className="ps-spin" /> : <Download />}
            {busy ? 'Hazırlanıyor…' : 'PDF indir'}
          </button>
        </footer>
      </div>
    </div>,
    document.body
  );
};

/* ===========================================================================
 * 1 · Kaynak
 * ========================================================================= */
interface QSel {
  committeeId: string; setCommitteeId: (v: string) => void;
  years: string[]; year: string; setYear: (v: string) => void;
  disciplines: string[]; discipline: string; setDiscipline: (v: string) => void;
  topics: string[]; topic: string; setTopic: (v: string) => void;
  kazanimlar: { key: string; text: string; n: number }[]; kazanim: string; setKazanim: (v: string) => void;
  search: string; setSearch: (v: string) => void;
  onlyAnswered: boolean; setOnlyAnswered: (v: boolean) => void;
  onlyExplained: boolean; setOnlyExplained: (v: boolean) => void;
  onlyAudited: boolean; setOnlyAudited: (v: boolean) => void;
  limit: number; setLimit: (v: number) => void;
  ornekDers: string; setOrnekDers: (v: string) => void;
  ornekLevels: string[]; setOrnekLevels: (v: string[]) => void;
  includeBranching: boolean; setIncludeBranching: (v: boolean) => void;
  deckId: string; setDeckId: (v: string) => void;
  total: number;
  matched: number;
}

const QuestionSource: React.FC<{ kind: PdfContentKind; sel: QSel }> = ({ kind, sel }) => {
  const cross = kind === 'past' || kind === 'pool';
  const kzShort = (t: string) => (t.length > 80 ? `${t.slice(0, 78)}…` : t);
  return (
    <>
      <Group title="Seçim" aside={<span className="ps-count">{sel.matched} / {sel.total} soru</span>}>
        {kind === 'ornek' && (
          <>
            <Field label="Ders" value={sel.ornekDers} onChange={(v) => { sel.setOrnekDers(v); sel.setKazanim('all'); }}>
              <option value="all">Kurul 1 · tüm dersler</option>
              {ORNEK_INDEX.map((r) => (
                <option key={r.id} value={r.id}>{r.sira}. {r.konu} · {r.soru_sayisi}</option>
              ))}
            </Field>
            <Chips
              label="Zorluk"
              options={[['kolay', 'Kolay'], ['orta', 'Orta'], ['zor', 'Zor']]}
              value={sel.ornekLevels}
              onChange={(v) => sel.setOrnekLevels(v.length ? v : ['kolay', 'orta', 'zor'])}
            />
          </>
        )}
        {kind === 'mini' && (
          <>
            <DeckSelect value={sel.deckId} onChange={(v) => { sel.setDeckId(v); sel.setKazanim('all'); }} />
            <Switches>
              <Toggle label="Klinik karar soruları" hint="Vaka senaryolu karar sorularını da ekle" checked={sel.includeBranching} onChange={sel.setIncludeBranching} />
            </Switches>
          </>
        )}
        {cross && (
          <>
            <Field
              label="Kurul"
              value={sel.committeeId}
              onChange={(v) => {
                sel.setCommitteeId(v);
                sel.setYear('all');
                sel.setDiscipline('all');
                sel.setTopic('all');
                sel.setKazanim('all');
              }}
            >
              <option value="all">Tüm kurullar</option>
              {Object.entries(COMMITTEE_NAME).map(([id, name]) => <option key={id} value={id}>{name}</option>)}
            </Field>
            <div className="ps-row2">
              {kind === 'past' && (
                <Field label="Yıl" value={sel.year} onChange={sel.setYear} disabled={!sel.years.length}>
                  <option value="all">Tüm yıllar</option>
                  {sel.years.map((y) => <option key={y} value={y}>{y}</option>)}
                </Field>
              )}
              <Field label="Ders" value={sel.discipline} onChange={(v) => { sel.setDiscipline(v); sel.setTopic('all'); sel.setKazanim('all'); }} disabled={!sel.disciplines.length}>
                <option value="all">Tüm dersler</option>
                {sel.disciplines.map((d) => <option key={d} value={d}>{d}</option>)}
              </Field>
            </div>
            {kind === 'past' && sel.topics.length > 0 && (
              <Field label="Konu" value={sel.topic} onChange={(v) => { sel.setTopic(v); sel.setKazanim('all'); }}>
                <option value="all">Tüm konular</option>
                {sel.topics.map((t) => <option key={t} value={t}>{t}</option>)}
              </Field>
            )}
          </>
        )}
        {sel.kazanimlar.length > 0 && (
          <Field label={`Kazanım · ${sel.kazanimlar.length}`} value={sel.kazanim} onChange={sel.setKazanim}>
            <option value="all">Tüm kazanımlar</option>
            {sel.kazanimlar.map((k) => <option key={k.key} value={k.key}>{kzShort(k.text)} · {k.n}</option>)}
            <option value="?">Kazanımı belirsiz olanlar</option>
          </Field>
        )}
        <label className="ps-field">
          <span>Metinde ara</span>
          <input type="search" value={sel.search} onChange={(e) => sel.setSearch(e.target.value)} placeholder="ör. nefrotik, ADAMTS13" />
        </label>
        <Seg
          label="En çok"
          value={String(sel.limit)}
          onChange={(v) => sel.setLimit(Number(v))}
          options={[['50', '50'], ['100', '100'], ['200', '200'], ['500', '500'], ['0', 'Hepsi']]}
        />
        <Switches>
          <Toggle label="Yalnız cevabı belli olanlar" checked={sel.onlyAnswered} onChange={sel.setOnlyAnswered} />
          <Toggle label="Yalnız açıklamalı olanlar" hint="Açıklaması ya da şık analizi olan" checked={sel.onlyExplained} onChange={sel.setOnlyExplained} />
          {kind === 'past' && <Toggle label="Yalnız denetleyici onaylı" checked={sel.onlyAudited} onChange={sel.setOnlyAudited} />}
        </Switches>
      </Group>
    </>
  );
};

const LessonSource: React.FC<{
  deckId: string;
  setDeckId: (v: string) => void;
  steps: { number: number; title: string; section: number; checkpoint: number }[];
  sections: { index: number; name: string; numbers: number[] }[];
  picked: number[];
  setPicked: (v: number[] | ((p: number[]) => number[])) => void;
}> = ({ deckId, setDeckId, steps, sections, picked, setPicked }) => {
  const all = !picked.length;
  const has = (n: number) => all || picked.includes(n);
  const toggleSection = (nums: number[]) => {
    const base = all ? steps.map((s) => s.number) : picked;
    const allIn = nums.every((n) => base.includes(n));
    const next = allIn ? base.filter((n) => !nums.includes(n)) : [...new Set([...base, ...nums])].sort((a, b) => a - b);
    setPicked(next.length === steps.length ? [] : next);
  };
  return (
    <>
      <Group title="Ders">
        <DeckSelect value={deckId} onChange={setDeckId} />
      </Group>
      {steps.length > 0 && (
        <Group
          title={`Adımlar · ${all ? steps.length : picked.length}/${steps.length}`}
          aside={!all && <button type="button" className="ps-link-btn" onClick={() => setPicked([])}>Tümünü seç</button>}
        >
          <ul className="ps-list">
            {sections.map((sec) => {
              const secOn = sec.numbers.every(has);
              const secSome = sec.numbers.some(has);
              return (
                <li key={sec.index}>
                  <button type="button" role="checkbox" aria-checked={secOn ? true : secSome ? 'mixed' : false} className="ps-li is-head" onClick={() => toggleSection(sec.numbers)}>
                    <CheckBox on={secOn} mixed={!secOn && secSome} />
                    <small>Bölüm {sec.index + 1}</small>
                    <b>{sec.name}</b>
                  </button>
                  {sec.numbers.map((n) => {
                    const st = steps.find((s) => s.number === n)!;
                    const on = has(n);
                    return (
                      <button
                        key={n}
                        type="button"
                        role="checkbox"
                        aria-checked={on}
                        className={`ps-li is-sub ${on ? 'is-on' : ''}`}
                        onClick={() => {
                          const base = all ? steps.map((s) => s.number) : picked;
                          const next = on ? base.filter((x) => x !== n) : [...base, n].sort((a, b) => a - b);
                          setPicked(next.length === steps.length ? [] : next);
                        }}
                      >
                        <CheckBox on={on} />
                        <code>{n}</code>
                        <span>{st?.title}</span>
                        {st?.checkpoint > 0 && <span className="ms-tag is-accent">Tekrar</span>}
                      </button>
                    );
                  })}
                </li>
              );
            })}
          </ul>
        </Group>
      )}
    </>
  );
};

const SummarySource: React.FC<{ kurul: number; setKurul: (k: number) => void; list: SummaryMeta[]; picked: string[]; setPicked: (v: string[]) => void }> = ({ kurul, setKurul, list, picked, setPicked }) => (
  <>
    <Group title="Kurul">
      <Field label="Kurul" value={String(kurul)} onChange={(v) => setKurul(Number(v))}>
        {[1, 2, 3, 4, 5, 6].map((k) => <option key={k} value={k}>{COMMITTEE_NAME[`donem3-kurul${k}`]}</option>)}
      </Field>
    </Group>
    <Group
      title={`Özetler · ${picked.length}/${list.length}`}
      aside={
        <button type="button" className="ps-link-btn" onClick={() => setPicked(picked.length === list.length ? list.slice(0, 1).map((m) => m.id) : list.map((m) => m.id))}>
          {picked.length === list.length ? 'Seçimi sıfırla' : 'Tümünü seç'}
        </button>
      }
    >
      <ul className="ps-list">
        {list.map((m) => {
          const on = picked.includes(m.id);
          return (
            <li key={m.id}>
              <button
                type="button"
                role="checkbox"
                aria-checked={on}
                className={`ps-li ${on ? 'is-on' : ''}`}
                onClick={() => setPicked(on ? picked.filter((x) => x !== m.id) : list.filter((x) => x.id === m.id || picked.includes(x.id)).map((x) => x.id))}
              >
                <CheckBox on={on} />
                <span className="ps-li-2"><b>{m.title}</b><small>{m.discipline}</small></span>
              </button>
            </li>
          );
        })}
      </ul>
    </Group>
  </>
);

/* ===========================================================================
 * 2 · Düzen
 * ========================================================================= */
const QuestionLayout: React.FC<{ kind: PdfContentKind; o: QuestionDocOptions; set: (p: Partial<QuestionDocOptions>) => void }> = ({ kind, o, set }) => {
  const sol = o.mode === 'solution';
  const choices = groupChoices(kind);
  const quick = GROUP_QUICK[kind === 'ornek' ? 'ornek' : kind === 'mini' ? 'mini' : 'q'];
  const g1 = choices.includes(o.group1) ? o.group1 : 'none';
  const g2 = choices.includes(o.group2) ? o.group2 : 'none';
  const sorts = sortChoices(kind);
  const sortBy = sorts.includes(o.sortBy) ? o.sortBy : 'source';
  return (
    <>
      <Group title="Hazır kitapçık">
        <div className="ps-presets" role="radiogroup" aria-label="Hazır kitapçık">
          {PRESETS.map((p) => {
            const on = matchesPreset(o, p.apply);
            const Icon = p.icon;
            return (
              <button key={p.id} type="button" role="radio" aria-checked={on} className={`ps-preset ${on ? 'is-on' : ''}`} onClick={() => set(p.apply)}>
                <Icon />
                <b>{p.label}</b>
                <small>{p.hint}</small>
              </button>
            );
          })}
        </div>
      </Group>

      <Group title="Gruplama">
        <div className="ps-chips" role="radiogroup" aria-label="Hızlı gruplama">
          {quick.map(([a, b, label]) => {
            const on = g1 === a && g2 === b;
            return (
              <button key={label} type="button" role="radio" aria-checked={on} className={on ? 'is-on' : ''} onClick={() => set({ group1: a, group2: b })}>
                {on && <Check />} {label}
              </button>
            );
          })}
        </div>
        <div className="ps-row2">
          <Field label="1. kademe" value={g1} onChange={(v) => set({ group1: v as GroupBy, ...(v === 'none' || v === g2 ? { group2: 'none' } : {}) })}>
            <option value="none">Yok</option>
            {choices.map((c) => <option key={c} value={c}>{GROUP_LABEL[c]}</option>)}
          </Field>
          <Field label="2. kademe" value={g2} onChange={(v) => set({ group2: v as GroupBy })} disabled={g1 === 'none'}>
            <option value="none">Yok</option>
            {choices.filter((c) => c !== g1).map((c) => <option key={c} value={c}>{GROUP_LABEL[c]}</option>)}
          </Field>
        </div>
        <Seg<GroupOrder>
          label="Grupların sırası"
          value={o.groupOrder}
          onChange={(v) => set({ groupOrder: v })}
          disabled={g1 === 'none'}
          options={[['natural', 'Müfredat'], ['alpha', 'A → Z'], ['count', 'Soru sayısı']]}
        />
        {g1 !== 'none' && (
          <p className="ps-hint">
            {[g1, g2].includes('kazanim')
              ? 'Kazanımı eşlenmemiş sorular en sonda “Kazanımı belirsiz” başlığında toplanır.'
              : 'Belirsiz değerli sorular her zaman en sonda toplanır.'}
          </p>
        )}
      </Group>

      <Group title="Sıralama">
        <div className="ps-row2 is-grow">
          <Field label={g1 === 'none' ? 'Sorular' : 'Grup içinde'} value={sortBy} onChange={(v) => set({ sortBy: v as SortBy })}>
            {sorts.map((s) => <option key={s} value={s}>{SORT_LABEL[s]}</option>)}
          </Field>
          {sortBy === 'random' ? (
            <button type="button" className="ps-btn is-tall" onClick={() => set({ seed: (o.seed % 9973) + 1 + Math.floor(Math.random() * 1000) })}>
              <Shuffle /> Yeniden karıştır
            </button>
          ) : (
            <Seg label="Yön" value={o.sortDir} onChange={(v) => set({ sortDir: v })} options={[['asc', 'Artan'], ['desc', 'Azalan']]} />
          )}
        </div>
        <Seg<Numbering>
          label="Numaralandırma"
          value={o.numbering === 'original' && kind !== 'past' && kind !== 'pool' ? 'sequential' : o.numbering}
          onChange={(v) => set({ numbering: v })}
          options={[
            ['sequential', 'Baştan sona'],
            ['group', 'Her grupta 1’den'],
            ...((kind === 'past' || kind === 'pool' ? [['original', 'Orijinal no']] : []) as [Numbering, string][]),
          ]}
        />
      </Group>

      <Group title="Cevaplar">
        <Seg<BookletMode>
          label="Kitapçık türü"
          value={o.mode}
          onChange={(v) => set({ mode: v, ...(v === 'student' ? { answerKey: false } : {}) })}
          options={[['student', 'Cevapsız'], ['solution', 'Çözümlü'], ['key', 'Yalnız anahtar']]}
        />
        <Seg<AnswersAt>
          label="Çözümün yeri"
          value={o.answersAt}
          onChange={(v) => set({ answersAt: v })}
          disabled={!sol}
          options={[['inline', 'Soru altında'], ['group', 'Bölüm sonunda'], ['end', 'Kitapçık sonunda']]}
        />
        <Switches>
          <Toggle
            label="Cevap anahtarı"
            hint={o.answersAt === 'group' ? 'Her bölümün sonunda tablo' : 'Belgenin sonunda tablo'}
            checked={o.answerKey || o.mode === 'key'}
            disabled={o.mode === 'key'}
            onChange={(v) => set({ answerKey: v })}
          />
          <Toggle label="Optik form" hint="Kurşun kalemle doldurmak için" checked={o.opticForm} onChange={(v) => set({ opticForm: v })} />
        </Switches>
      </Group>

      <Group title="Belge yapısı">
        <Switches>
          <Toggle label="Kapak sayfası" hint="Başlık, istatistik, ad-no alanı" checked={o.cover} onChange={(v) => set({ cover: v })} />
          <Toggle label="İçindekiler" hint="Bölümlere, çözümlere ve anahtara tıklanır" checked={o.toc} onChange={(v) => set({ toc: v })} />
          <Toggle label="Tıklanabilir bağlantılar" hint="Soru no → cevabı, cevap → soruya dön" checked={o.links} onChange={(v) => set({ links: v })} />
          <Toggle label="Her grup yeni sayfada" checked={o.groupNewPage} disabled={g1 === 'none'} onChange={(v) => set({ groupNewPage: v })} />
          <Toggle
            label="Her soru ayrı sayfada"
            hint={o.answersAt !== 'inline' ? 'Çözümler de birer sayfa' : 'Soru ve çözümü tek sayfada'}
            checked={o.questionPerPage}
            onChange={(v) => set({ questionPerPage: v })}
          />
        </Switches>
      </Group>
    </>
  );
};

const LessonLayout: React.FC<{ o: LessonDocOptions; set: (p: Partial<LessonDocOptions>) => void }> = ({ o, set }) => (
  <>
    <Group title="Cevaplar">
      <Seg<AnswerMode> label="Etkileşim cevapları" value={o.answers} onChange={(v) => set({ answers: v })} options={[['shown', 'Açık'], ['end', 'Belge sonunda'], ['hidden', 'Çalışma kâğıdı']]} />
      {o.answers === 'end' && <p className="ps-hint">Her adımdaki “Cevaplar →” bağlantısı sondaki cevabına, cevaptaki adım numarası adıma geri götürür.</p>}
    </Group>
    <Group title="Belge yapısı">
      <Switches>
        <Toggle label="Kapak sayfası" checked={o.cover} onChange={(v) => set({ cover: v })} />
        <Toggle label="İçindekiler" hint="Bölüm ve adımlara tıklanır" checked={o.toc} onChange={(v) => set({ toc: v })} />
        <Toggle label="Bölüm başlıkları" checked={o.sectionTitles} onChange={(v) => set({ sectionTitles: v })} />
        <Toggle label="Her adım yeni sayfada" hint="Kapalıyken adımlar akarak dizilir" checked={o.stepPerPage} onChange={(v) => set({ stepPerPage: v })} />
      </Switches>
    </Group>
  </>
);

const SummaryLayout: React.FC<{ o: SummaryDocOptions; set: (p: Partial<SummaryDocOptions>) => void }> = ({ o, set }) => (
  <>
    <Group title="Belge yapısı">
      <Switches>
        <Toggle label="Kapak sayfası" checked={o.cover} onChange={(v) => set({ cover: v })} />
        <Toggle label="İçindekiler" hint="Birden çok özet seçiliyse; başlığa tıklanır" checked={o.toc} onChange={(v) => set({ toc: v })} />
      </Switches>
    </Group>
    <Group title="Özetteki sorular">
      <Seg<SummaryQuestions> label="Sorular" value={o.questions} onChange={(v) => set({ questions: v })} options={[['answered', 'Cevaplı'], ['plain', 'Cevapsız'], ['none', 'Çıkar']]} />
    </Group>
  </>
);

/* ===========================================================================
 * 3 · Görünüm
 * ========================================================================= */
const TEMPLATE_ORDER: TemplateId[] = ['modern', 'sade', 'klasik', 'kompakt', 'sinav'];

const LookCommon: React.FC<{ page: PageSettings; setPage: (p: Partial<PageSettings>) => void; fitInfo: { zoom: number; pages: number; basePages: number } | null; unit: string }> = ({ page, setPage, fitInfo }) => (
  <>
    <Group title="Tasarım">
      <div className="ps-tpls ps-designs" role="radiogroup" aria-label="Tasarım">
        {DESIGN_ORDER.map((id) => {
          const on = page.design === id;
          return (
            <button key={id} type="button" role="radio" aria-checked={on} className={`ps-tpl ${on ? 'is-on' : ''}`} onClick={() => setPage({ design: id })}>
              <DesignGlyph id={id} />
              <b>{DESIGNS[id].label}</b>
              <small>{DESIGNS[id].hint}</small>
            </button>
          );
        })}
      </div>
      <p className="ps-hint">Şablonlar seçilen tasarımın üstüne biner; “Uygulama” şablonu tasarımı en yalın hâliyle gösterir.</p>
    </Group>
    <Group title="Şablon">
      <div className="ps-tpls" role="radiogroup" aria-label="Şablon">
        {TEMPLATE_ORDER.map((id) => {
          const on = page.template === id;
          return (
            <button key={id} type="button" role="radio" aria-checked={on} className={`ps-tpl ${on ? 'is-on' : ''}`} onClick={() => setPage({ template: id })}>
              <TemplateGlyph id={id} />
              <b>{TEMPLATES[id].label}</b>
              <small>{TEMPLATES[id].hint}</small>
            </button>
          );
        })}
      </div>
    </Group>
    <Group title="Yazı ve renk">
      <Seg<FontScale> label="Yazı boyutu" value={page.fontScale} onChange={(v) => setPage({ fontScale: v })} options={[['xs', 'En küçük'], ['sm', 'Küçük'], ['md', 'Orta'], ['lg', 'Büyük'], ['xl', 'En büyük']]} />
      <Seg label="Renk" value={page.ink} onChange={(v) => setPage({ ink: v })} options={[['color', 'Renkli'], ['mono', 'Siyah-beyaz']]} />
    </Group>
    <Group title="Sayfaya sığdır">
      <Seg<FitMode>
        label="Sığdırma"
        value={page.fit}
        onChange={(v) => setPage({ fit: v })}
        options={[['off', 'Kapalı'], ['width', 'Genişliğe'], ['pages', 'Sayfa sayısına']]}
      />
      {page.fit === 'width' && <p className="ps-hint">Geniş tablolar, görseller ve uzun satırlar sayfa kenarından taşmaz; yazı boyutu değişmez.</p>}
      {page.fit === 'pages' && (
        <>
          <div className="ps-stepper">
            <span>En çok</span>
            <button type="button" aria-label="Bir sayfa azalt" onClick={() => setPage({ fitPages: Math.max(1, page.fitPages - 1) })}><Minus /></button>
            <input
              type="number"
              min={1}
              max={500}
              inputMode="numeric"
              aria-label="Hedef sayfa sayısı"
              value={page.fitPages}
              onChange={(e) => setPage({ fitPages: Math.max(1, Math.min(500, Math.round(Number(e.target.value) || 1))) })}
            />
            <button type="button" aria-label="Bir sayfa artır" onClick={() => setPage({ fitPages: Math.min(500, page.fitPages + 1) })}><Plus /></button>
            <span>sayfa</span>
          </div>
          <p className="ps-hint">
            {fitInfo
              ? fitInfo.basePages <= page.fitPages
                ? `Zaten sığıyor: yaklaşık ${fitInfo.basePages} sayfa, yazı küçültülmedi.`
                : `Yaklaşık ${fitInfo.basePages} sayfa → ${fitInfo.pages} sayfa; yazı %${Math.round((fitInfo.zoom / ZOOM[page.fontScale]) * 100)} ölçekte.${fitInfo.pages > page.fitPages ? ' En küçük yazıda bile sığmadı; daha az içerik seç ya da sayfa sayısını artır.' : ''}`
              : 'Yazı, içerik hedef sayfaya sığana dek küçültülür (en çok yarıya). Tahmindir, ±1 sayfa sapabilir.'}
          </p>
        </>
      )}
    </Group>
  </>
);

const QuestionLook: React.FC<{ o: QuestionDocOptions; set: (p: Partial<QuestionDocOptions>) => void }> = ({ o, set }) => {
  const sol = o.mode === 'solution';
  return (
    <>
      <Group title="Sütun">
        <div className="ps-cols" role="radiogroup" aria-label="Sütun" aria-disabled={o.questionPerPage}>
          {([1, 2, 3] as const).map((n) => {
            const on = o.columns === n && !o.questionPerPage;
            return (
              <button key={n} type="button" role="radio" aria-checked={on} disabled={o.questionPerPage} className={`ps-choice is-col ${on ? 'is-on' : ''}`} onClick={() => set({ columns: n })}>
                <ColumnGlyph cols={n} />
                <span className="ps-choice-t"><b>{n === 1 ? 'Tek sütun' : `${n} sütun`}</b><small>{n === 1 ? 'Geniş satırlar' : n === 2 ? 'Kitapçık gibi' : 'A3 / yatay için'}</small></span>
              </button>
            );
          })}
        </div>
        {o.questionPerPage && <p className="ps-hint">“Her soru ayrı sayfada” açıkken tek sütun kullanılır.</p>}
      </Group>
      <Group title="Soruda görünenler">
        <Switches>
          <Toggle label="Doğru şıkkı işaretle" hint="Yeşil ve ✓ (çözüm soru altındayken)" checked={sol && o.markCorrect} disabled={!sol || o.answersAt !== 'inline'} onChange={(v) => set({ markCorrect: v })} />
          <Toggle label="Soru açıklaması" checked={sol && o.explanation} disabled={!sol} onChange={(v) => set({ explanation: v })} />
          <Toggle label="Referans kaynaklar" checked={sol && o.refs} disabled={!sol} onChange={(v) => set({ refs: v })} />
          <Toggle label="Üst bilgi" hint="Ders · kurul · yıl satırı" checked={o.meta} onChange={(v) => set({ meta: v })} />
          <Toggle label="Rozetler" hint="Denetleyici, Faz 14, tartışmalı cevap" checked={o.badges} onChange={(v) => set({ badges: v })} />
          <Toggle label="Not alanı" hint="Her sorunun altında yazma satırları" checked={o.writeSpace} onChange={(v) => set({ writeSpace: v })} />
        </Switches>
        <Seg<OptionNotes>
          label="Şık açıklamaları"
          value={o.optionNotes}
          onChange={(v) => set({ optionNotes: v })}
          disabled={!sol}
          options={[['off', 'Yok'], ['inline', 'Şık altında'], ['analysis', 'Analiz tablosu']]}
        />
      </Group>
    </>
  );
};

const LessonLook: React.FC<{ o: LessonDocOptions; set: (p: Partial<LessonDocOptions>) => void; ixCounts: Record<string, number> }> = ({ o, set, ixCounts }) => (
  <>
    <Group title="Adım içeriği">
      <Switches>
        <Toggle label="Anlatım" checked={o.narrative} onChange={(v) => set({ narrative: v })} />
        <Toggle label="Anahtar maddeler" checked={o.keyPoints} onChange={(v) => set({ keyPoints: v })} />
        <Toggle label="Tablolar" checked={o.tables} onChange={(v) => set({ tables: v })} />
        <Toggle label="İnfografik ve formüller" checked={o.visuals} onChange={(v) => set({ visuals: v })} />
        <Toggle label="Hocanın vurgusu" checked={o.teacher} onChange={(v) => set({ teacher: v })} />
        <Toggle label="Sınav spotları" checked={o.spots} onChange={(v) => set({ spots: v })} />
        <Toggle label="Önemli nokta ve sınav ipucu" checked={o.tips} onChange={(v) => set({ tips: v })} />
        <Toggle label="Terimler sözlüğü" hint="Adımdaki tıbbi terimler ve tanımları" checked={o.terms} onChange={(v) => set({ terms: v })} />
        <Toggle label="Akıl kartları" checked={o.cards} onChange={(v) => set({ cards: v })} />
      </Switches>
    </Group>
    <Group
      title="Etkileşimler"
      aside={
        <button type="button" className="ps-link-btn" onClick={() => set({ interactives: o.interactives.length ? [] : [...IX_TYPES] })}>
          {o.interactives.length ? 'Hiçbiri' : 'Hepsi'}
        </button>
      }
    >
      <div className="ps-chips">
        {IX_TYPES.map((t) => {
          const on = o.interactives.includes(t);
          const [Icon, label] = IX_META[t];
          const n = ixCounts[t] || 0;
          return (
            <button
              key={t}
              type="button"
              role="checkbox"
              aria-checked={on}
              className={`${on ? 'is-on' : ''} ${n ? '' : 'is-dim'}`}
              onClick={() => set({ interactives: on ? o.interactives.filter((x) => x !== t) : ([...o.interactives, t] as IxType[]) })}
            >
              <Icon /> {label} <code>{n}</code>
            </button>
          );
        })}
      </div>
      <Switches>
        <Toggle label="Şık açıklamaları" hint="Mini soru ve klinik kararda neden doğru / yanlış" checked={o.optionNotes && o.answers !== 'hidden'} disabled={o.answers === 'hidden'} onChange={(v) => set({ optionNotes: v })} />
      </Switches>
    </Group>
  </>
);

const SummaryLook: React.FC<{ o: SummaryDocOptions; set: (p: Partial<SummaryDocOptions>) => void }> = ({ o, set }) => (
  <Group title="Özette görünenler">
    <Switches>
      <Toggle label="Konu başlıkları" hint="Özetin başında başlık kartları" checked={o.keyPoints} onChange={(v) => set({ keyPoints: v })} />
      <Toggle label="Tablolar" checked={o.tables} onChange={(v) => set({ tables: v })} />
      <Toggle label="Not kutuları" hint="Önemli, sınav spotu, klinik ipucu" checked={o.callouts} onChange={(v) => set({ callouts: v })} />
    </Switches>
  </Group>
);

/* ===========================================================================
 * 4 · Sayfa
 * ========================================================================= */
const PageStep: React.FC<{ page: PageSettings; setPage: (p: Partial<PageSettings>) => void }> = ({ page, setPage }) => {
  const land = page.orientation === 'landscape';
  return (
    <>
      <Group title="Kâğıt boyutu">
        <div className="ps-papers" role="radiogroup" aria-label="Kâğıt boyutu">
          {PAPER_ORDER.map((id: PaperSize) => {
            const on = page.paper === id;
            const p = PAPER[id];
            const w = land ? p.h : p.w;
            const h = land ? p.w : p.h;
            const scale = 30 / 420;
            return (
              <button key={id} type="button" role="radio" aria-checked={on} className={`ps-paper ${on ? 'is-on' : ''}`} onClick={() => setPage({ paper: id, ...(id === 'tablet' ? { margins: 'narrow' as MarginPreset } : {}) })}>
                <span className="ps-paper-box" aria-hidden="true">
                  <i style={{ width: Math.max(9, w * scale * 1.25), height: Math.max(9, h * scale * 1.25) }} className={id === 'tablet' ? 'is-round' : ''} />
                </span>
                <b>{p.label}</b>
                <small>{p.hint}</small>
              </button>
            );
          })}
        </div>
      </Group>
      <Group title="Yön">
        <div className="ps-orient" role="radiogroup" aria-label="Sayfa yönü">
          {(
            [
              ['portrait', 'Dikey', RectangleVertical, 'Soru kitapçığı, okuma'],
              ['landscape', 'Yatay', RectangleHorizontal, 'Geniş tablo, 2–3 sütun'],
            ] as const
          ).map(([id, label, Icon, hint]) => (
            <button key={id} type="button" role="radio" aria-checked={page.orientation === id} className={`ps-choice ${page.orientation === id ? 'is-on' : ''}`} onClick={() => setPage({ orientation: id })}>
              <span className="ps-choice-ic"><Icon /></span>
              <span className="ps-choice-t"><b>{label}</b><small>{hint}</small></span>
            </button>
          ))}
        </div>
      </Group>
      <Group title="Kenar boşluğu">
        <Seg<MarginPreset>
          label="Boşluk"
          value={page.margins}
          onChange={(v) => setPage({ margins: v })}
          options={(Object.keys(MARGINS) as MarginPreset[]).map((k) => [k, `${MARGINS[k].label} · ${MARGINS[k].mm[1]} mm`])}
        />
      </Group>
      <Group title="Sayfa bilgileri">
        <Switches>
          <Toggle label="Sayfa numarası" hint="Sağ altta 3 / 12" checked={page.pageNumbers} onChange={(v) => setPage({ pageNumbers: v })} />
          <Toggle label="Üst bilgi" hint="Her sayfada belge adı" checked={page.runningHeader} onChange={(v) => setPage({ runningHeader: v })} />
        </Switches>
        <button type="button" className="ps-link-btn is-start" onClick={() => setPage({ ...DEFAULT_PAGE, template: page.template, fontScale: page.fontScale, ink: page.ink, fit: page.fit, fitPages: page.fitPages })}>
          Sayfa ayarlarını sıfırla (A4 dikey, normal)
        </button>
      </Group>
    </>
  );
};

/* ===========================================================================
 * Yapı taşları
 * ========================================================================= */
const DeckSelect: React.FC<{ value: string; onChange: (v: string) => void }> = ({ value, onChange }) => {
  const groups = useMemo(() => {
    const m = new Map<string, typeof DECK_CATALOG>();
    DECK_CATALOG.forEach((d) => {
      const g = disciplineGroup(d.discipline);
      if (!m.has(g)) m.set(g, []);
      m.get(g)!.push(d);
    });
    return [...m.entries()].sort((a, b) => a[0].localeCompare(b[0], 'tr'));
  }, []);
  return (
    <Field label="Ders" value={value} onChange={onChange}>
      {groups.map(([g, list]) => (
        <optgroup key={g} label={g}>
          {list.map((d) => <option key={d.id} value={d.id}>{deckName(d)} · {d.slideCount} adım</option>)}
        </optgroup>
      ))}
    </Field>
  );
};

const Group: React.FC<{ title: string; aside?: React.ReactNode; children: React.ReactNode }> = ({ title, aside, children }) => (
  <section className="ps-group">
    <div className="ps-group-h">
      <h3>{title}</h3>
      {aside}
    </div>
    {children}
  </section>
);

const Field: React.FC<{ label: string; value: string; onChange: (v: string) => void; disabled?: boolean; children: React.ReactNode }> = ({ label, value, onChange, disabled, children }) => (
  <label className={`ps-field is-select ${disabled ? 'is-off' : ''}`}>
    <span>{label}</span>
    <select value={value} disabled={disabled} onChange={(e) => onChange(e.target.value)}>
      {children}
    </select>
    <ChevronDown aria-hidden="true" />
  </label>
);

function Seg<T extends string>({ label, value, onChange, options, disabled }: { label: string; value: T; onChange: (v: T) => void; options: [T, string][]; disabled?: boolean }) {
  return (
    <div className={`ps-segwrap ${disabled ? 'is-off' : ''}`}>
      <span className="ps-seg-l">{label}</span>
      <div role="radiogroup" aria-label={label} aria-disabled={disabled} className="ps-seg" style={{ gridTemplateColumns: `repeat(${options.length}, minmax(0, 1fr))` }}>
        {options.map(([id, text]) => (
          <button key={id} type="button" role="radio" aria-checked={value === id} disabled={disabled} className={value === id ? 'is-on' : ''} onClick={() => onChange(id)}>
            {text}
          </button>
        ))}
      </div>
    </div>
  );
}

const Chips: React.FC<{ label: string; options: [string, string][]; value: string[]; onChange: (v: string[]) => void }> = ({ label, options, value, onChange }) => (
  <div className="ps-segwrap">
    <span className="ps-seg-l">{label}</span>
    <div className="ps-chips">
      {options.map(([id, text]) => {
        const on = value.includes(id);
        return (
          <button key={id} type="button" role="checkbox" aria-checked={on} className={on ? 'is-on' : ''} onClick={() => onChange(on ? value.filter((x) => x !== id) : [...value, id])}>
            {on && <Check />} {text}
          </button>
        );
      })}
    </div>
  </div>
);

const Switches: React.FC<{ children: React.ReactNode }> = ({ children }) => <div className="ps-switches">{children}</div>;

const Toggle: React.FC<{ label: string; hint?: string; checked: boolean; onChange: (v: boolean) => void; disabled?: boolean }> = ({ label, hint, checked, onChange, disabled }) => (
  <button type="button" role="switch" aria-checked={checked} disabled={disabled} className="ps-switch" onClick={() => onChange(!checked)}>
    <span className="ps-switch-t">
      <b>{label}</b>
      {hint && <small>{hint}</small>}
    </span>
    <span className={`ps-knob ${checked ? 'is-on' : ''}`} aria-hidden="true"><i /></span>
  </button>
);

const CheckBox: React.FC<{ on: boolean; mixed?: boolean }> = ({ on, mixed }) => (
  <span className={`ps-check ${on || mixed ? 'is-on' : ''}`} aria-hidden="true">
    {on ? <Check strokeWidth={3} /> : mixed ? <i /> : null}
  </span>
);

const ColumnGlyph: React.FC<{ cols: 1 | 2 | 3 }> = ({ cols }) => (
  <span className="ps-glyph" aria-hidden="true">
    {Array.from({ length: cols }).map((_, i) => (
      <span key={i}>
        {[0, 1, 2, 3, 4].map((j) => <i key={j} style={{ width: j === 4 ? '60%' : '100%' }} />)}
      </span>
    ))}
  </span>
);

/** Şablonun küçük çizimi: kart / çizgi / tırnaklı / sıkı / sınav */
/** Tasarım önizleme simgesi: v10 koyu numara + yuvarlak kart, v12 düz kart + ince çizgi */
const DesignGlyph: React.FC<{ id: PdfDesign }> = ({ id }) => (
  <span className={`ps-dglyph is-${id}`} aria-hidden="true">
    <span className="ps-dglyph-card">
      <em>{id === 'v12' ? 'S1' : '1'}</em>
      <span><i /><i /></span>
    </span>
    <span className="ps-dglyph-opts"><i /><i /><i /></span>
  </span>
);

const TemplateGlyph: React.FC<{ id: TemplateId }> = ({ id }) => (
  <span className={`ps-tglyph is-${id}`} aria-hidden="true">
    <em>{id === 'klasik' ? 'Aa' : id === 'sinav' ? '1.' : ''}</em>
    <span><i /><i /><i /></span>
    {id !== 'kompakt' && <span><i /><i /></span>}
  </span>
);
