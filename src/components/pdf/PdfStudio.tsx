/**
 * PDF Stüdyosu: çıkmış sorular, soru havuzu, örnek sorular, Öğren dersleri, mini sorular ve ders özetleri
 * için dinamik PDF. İçerik uygulamanın kendi bileşen sınıflarıyla çizilir (bkz. pdfDocument.ts), filtreler
 * neyin PDF'e gireceğini belirler; sağdaki önizleme indirilecek belgenin aynısıdır.
 */
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  X, Download, FileText, FileDown, FileCode, GraduationCap, RefreshCw, EyeOff, BookOpenCheck, Grid3x3, Check, ChevronDown,
  Archive, Users, Target, HelpCircle, BookMarked, Printer, Zap, Eye, MonitorSmartphone,
} from 'lucide-react';
import type { Committee, QuestionItem } from '../../types';
import { ApiService, getCustomApiUrl } from '../../services/api';
import { normalizeDonem3Discipline, isDonem3Question } from '../../data/curriculumData';
import { DECK_CATALOG, loadDeck, deckName } from '../../data/deckStore';
import type { InteractiveDeck } from '../learn/InteractiveDeckView';
import { buildSteps, buildSections } from '../learn/lesson/lessonModel';
import { IX_META } from '../learn/lesson/LessonBlocks';
import { BlurOverlay, PaperLoader } from '../ui/Animations';
import { toast } from '../ui/Toast';
import summariesMeta from '../../data/summaries_meta.json';
import {
  buildDocument, renderMarkup, serverPdfAvailable, renderPdfOnServer, downloadBlob, printDocument, downloadHtml, safeFileName,
  PAGE_SIZE, type PageFormat, type FontScale, type DocumentOptions,
} from './pdfDocument';
import {
  fromPastQuestion, fromPoolQuestion, loadOrnekQuestions, miniQuestionsFromDeck, ORNEK_INDEX, COMMITTEE_NAME, sortYears,
  type PdfQuestion,
} from './pdfSources';
import { QuestionDoc, type QuestionDocOptions, type GroupBy, type OptionNotes, type BookletMode } from './PdfQuestionDoc';
import { LessonDoc, IX_TYPES, type LessonDocOptions, type IxType, type AnswerMode } from './PdfLessonDoc';
import { SummaryDoc, type SummaryDocOptions, type SummaryForPdf, type SummaryQuestions } from './PdfSummaryDoc';
import type { CoverInfo } from './PdfParts';
import './pdf.css';

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

const KINDS: { id: PdfContentKind; label: string; icon: React.ElementType }[] = [
  { id: 'past', label: 'Çıkmış', icon: Archive },
  { id: 'pool', label: 'Havuz', icon: Users },
  { id: 'ornek', label: 'Örnek soru', icon: Target },
  { id: 'learn', label: 'Öğren', icon: GraduationCap },
  { id: 'mini', label: 'Mini soru', icon: HelpCircle },
  { id: 'summary', label: 'Ders özeti', icon: BookMarked },
];
const isQuestionKind = (k: PdfContentKind) => k === 'past' || k === 'pool' || k === 'ornek' || k === 'mini';

/* ---------------------------------------------------------------------------
 * Ayarlar: her içerik türü kendi ayarını cihazda hatırlar
 * ------------------------------------------------------------------------- */
interface PageSettings { format: PageFormat; fontScale: FontScale; pageNumbers: boolean; runningHeader: boolean }
const DEFAULT_PAGE: PageSettings = { format: 'a4', fontScale: 'md', pageNumbers: true, runningHeader: true };

const DEFAULT_Q: QuestionDocOptions = {
  mode: 'solution', markCorrect: true, explanation: true, optionNotes: 'inline', refs: false, meta: true, badges: false,
  solutionsAtEnd: false, answerKey: true, opticForm: false, columns: 1, compact: false, questionPerPage: false, groupBy: 'none', groupNewPage: false,
  writeSpace: false, numbering: 'sequential', cover: false,
};
const PRESETS: { id: string; label: string; hint: string; icon: React.ElementType; apply: Partial<QuestionDocOptions> }[] = [
  { id: 'student', label: 'Öğrenci', hint: 'Cevapsız, optik form', icon: EyeOff, apply: { mode: 'student', answerKey: false, opticForm: true, cover: true, columns: 2, solutionsAtEnd: false, writeSpace: false } },
  { id: 'solution', label: 'Çözümlü', hint: 'Cevap + açıklama + şıklar', icon: BookOpenCheck, apply: { mode: 'solution', markCorrect: true, explanation: true, optionNotes: 'inline', solutionsAtEnd: false, answerKey: true, opticForm: false, columns: 1 } },
  { id: 'review', label: 'Hızlı tekrar', hint: 'Doğru şık işaretli, sıkı', icon: Zap, apply: { mode: 'solution', markCorrect: true, explanation: false, optionNotes: 'off', refs: false, solutionsAtEnd: false, answerKey: false, opticForm: false, columns: 2, compact: true, cover: false, questionPerPage: false } },
  { id: 'exam', label: 'Deneme', hint: 'Sorular, çözüm sonda', icon: FileText, apply: { mode: 'solution', markCorrect: true, explanation: true, optionNotes: 'analysis', solutionsAtEnd: true, answerKey: true, opticForm: true, columns: 2, cover: true } },
  { id: 'key', label: 'Anahtar', hint: 'Yalnız cevaplar', icon: Grid3x3, apply: { mode: 'key', answerKey: true, opticForm: false, cover: false } },
];

const DEFAULT_L: LessonDocOptions = {
  narrative: true, keyPoints: true, tables: true, visuals: true, teacher: true, spots: true, tips: true, terms: false, cards: true,
  interactives: [...IX_TYPES], answers: 'shown', optionNotes: true, stepPerPage: false, sectionTitles: true, toc: false, cover: false,
};
const DEFAULT_S: SummaryDocOptions = { keyPoints: true, tables: true, callouts: true, questions: 'answered', toc: true, cover: false };

function usePersisted<T extends object>(key: string, initial: T): [T, (patch: Partial<T>) => void] {
  const [v, setV] = useState<T>(() => {
    try {
      const raw = localStorage.getItem(key);
      return raw ? { ...initial, ...JSON.parse(raw) } : initial;
    } catch {
      return initial;
    }
  });
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

/** Yılı olmayan ya da "Kategorisiz" etiketli sorular sona düşer. */
const yearKey = (y?: string) => (y && /\d{4}/.test(y) ? y : '');
const fold = (t: string) => t.toLocaleLowerCase('tr-TR').normalize('NFKD').replace(/[̀-ͯ]/g, '');

/* =========================================================================== */
export const PdfStudio: React.FC<PdfStudioProps> = ({ isOpen, onClose, committee, committees = [], questions = [], initialSlide = null, initialContent }) => {
  const [kind, setKind] = useState<PdfContentKind>(() => (initialSlide ? 'learn' : initialContent || 'past'));
  const [page, setPage] = usePersisted<PageSettings>('medsoru_pdf_page_v2', DEFAULT_PAGE);
  const [qopt, setQopt] = usePersisted<QuestionDocOptions>('medsoru_pdf_q_v2', DEFAULT_Q);
  const [lopt, setLopt] = usePersisted<LessonDocOptions>('medsoru_pdf_l_v2', DEFAULT_L);
  const [sopt, setSopt] = usePersisted<SummaryDocOptions>('medsoru_pdf_s_v2', DEFAULT_S);

  // Soru seçimi
  const [committeeId, setCommitteeId] = useState<string>(committee?.id || 'all');
  const [year, setYear] = useState('all');
  const [discipline, setDiscipline] = useState('all');
  const [topic, setTopic] = useState('all');
  const [search, setSearch] = useState('');
  const [onlyAnswered, setOnlyAnswered] = useState(false);
  const [onlyExplained, setOnlyExplained] = useState(false);
  const [onlyAudited, setOnlyAudited] = useState(false);
  const [sortBy, setSortBy] = useState<'number' | 'year' | 'discipline'>('year');
  const [limit, setLimit] = useState(100);
  const [ornekDers, setOrnekDers] = useState<string>(ORNEK_INDEX[0]?.id || '');
  const [ornekLevels, setOrnekLevels] = useState<string[]>(['kolay', 'orta', 'zor']);
  const [includeBranching, setIncludeBranching] = useState(false);

  // Öğren
  const [deckId, setDeckId] = useState<string>(initialSlide?.deckId || DECK_CATALOG[0]?.id || '');
  const [deck, setDeck] = useState<InteractiveDeck | null>(null);
  const [pickedSteps, setPickedSteps] = useState<number[]>(initialSlide ? [initialSlide.slideNumber] : []);

  // Özet
  const [sumKurul, setSumKurul] = useState<number>(() => Number(String(committee?.id || '').match(/kurul(\d)/)?.[1]) || 1);
  const [sumIds, setSumIds] = useState<string[]>([]);

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
  const [pageCount, setPageCount] = useState<number | null>(null);
  const [building, setBuilding] = useState(false);
  const [settingsOpenMobile, setSettingsOpenMobile] = useState(true);
  const frameBox = useRef<HTMLDivElement>(null);
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
  }, [isOpen]);

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

  const kurulSummaries = useMemo(() => SUMMARY_META.filter((m) => m.kurul === sumKurul), [sumKurul]);
  useEffect(() => {
    setSumIds((ids) => (ids.some((id) => kurulSummaries.some((m) => m.id === id)) ? ids : kurulSummaries.slice(0, 1).map((m) => m.id)));
  }, [kurulSummaries]);

  /* ---- Soru havuzu (türe göre) ---- */
  const baseQuestions = useMemo<PdfQuestion[]>(() => {
    if (kind === 'past') return (past || []).map(fromPastQuestion).filter(Boolean) as PdfQuestion[];
    if (kind === 'pool') return questions.map(fromPoolQuestion).filter(Boolean) as PdfQuestion[];
    if (kind === 'ornek') return (ornek || []).filter((q) => !q.difficulty || ornekLevels.includes(q.difficulty));
    if (kind === 'mini') return deck ? miniQuestionsFromDeck(deck, includeBranching) : [];
    return [];
  }, [kind, past, questions, ornek, ornekLevels, deck, includeBranching]);

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

  const filtered = useMemo(() => {
    const needle = fold(search.trim());
    let list = baseQuestions.filter((q) => {
      if ((kind === 'past' || kind === 'pool') && !inCommittee(q)) return false;
      if (kind === 'past' && year !== 'all' && q.year !== year) return false;
      if ((kind === 'past' || kind === 'pool') && discipline !== 'all' && q.discipline !== discipline) return false;
      if (kind === 'past' && topic !== 'all' && q.topic !== topic) return false;
      if (onlyAnswered && !q.answer) return false;
      if (onlyExplained && !q.explanation && !q.options.some((o) => o.why)) return false;
      if (kind === 'past' && onlyAudited && !q.badges.some((b) => b.label.startsWith('Denetleyici'))) return false;
      if (needle && !fold(`${q.stem} ${q.options.map((o) => o.text).join(' ')} ${q.topic || ''}`).includes(needle)) return false;
      return true;
    });
    if (kind === 'past' || kind === 'pool') {
      list = [...list].sort((a, b) =>
        sortBy === 'discipline'
          ? a.discipline.localeCompare(b.discipline, 'tr') || (a.number || 0) - (b.number || 0)
          : sortBy === 'year'
            ? yearKey(b.year).localeCompare(yearKey(a.year), 'tr', { numeric: true }) || (a.number || 0) - (b.number || 0)
            : (a.number || 0) - (b.number || 0)
      );
    }
    return limit > 0 ? list.slice(0, limit) : list;
  }, [baseQuestions, kind, inCommittee, year, discipline, topic, onlyAnswered, onlyExplained, onlyAudited, search, sortBy, limit]);

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
    const tags = [kurul && kind !== 'ornek' && kind !== 'mini' ? kurul : '', year !== 'all' && kind === 'past' ? year : '', topic !== 'all' && kind === 'past' ? topic : '', search ? `“${search}”` : '']
      .filter(Boolean);
    return {
      kicker: label,
      title,
      subtitle: kind === 'ornek' ? ORNEK_INDEX.find((r) => r.id === ornekDers)?.ogretim_uyesi : undefined,
      stats: [
        { value: filtered.length, label: 'Soru' },
        ...(qopt.mode !== 'key' ? [{ value: `~${Math.max(1, Math.round(filtered.length * 1.1))} dk`, label: 'Süre' }] : []),
        { value: filtered.filter((q) => q.answer).length, label: 'Cevaplı' },
      ],
      tags,
      studentFields: qopt.mode === 'student',
    };
  }, [kind, deck, steps, pickedSteps, chosenStepCount, lopt.answers, sumKurul, sumIds, committeeId, discipline, year, topic, search, filtered, qopt.mode, ornekDers]);

  const docOptions: DocumentOptions = useMemo(
    () => ({ title: coverInfo.title, runningHead: `${coverInfo.kicker} · ${coverInfo.title}`, ...page }),
    [coverInfo, page]
  );

  /** İçeriğin HTML gövdesi; önizlemede kısaltılır. */
  const buildBody = useCallback(
    async (preview: boolean): Promise<string | null> => {
      if (isQuestionKind(kind)) {
        if (!filtered.length) return null;
        const qs = preview ? filtered.slice(0, PREVIEW_Q) : filtered;
        return renderMarkup(<QuestionDoc questions={qs} options={qopt} cover={coverInfo} />);
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
    [kind, filtered, qopt, coverInfo, deck, pickedSteps, steps, lopt, sumIds, sopt]
  );

  const previewTruncated =
    isQuestionKind(kind) ? filtered.length > PREVIEW_Q : kind === 'learn' ? chosenStepCount > PREVIEW_STEPS : kind === 'summary' ? sumIds.length > PREVIEW_SUMMARIES : false;

  /* ---- Önizleme ---- */
  const pageWidthPx = (PAGE_SIZE[page.format].w / 25.4) * 96 + 48;
  const previewZoom = Math.min(1, Math.max(0.3, (frameW - 8) / pageWidthPx));
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
          return;
        }
        const html = buildDocument(body, docOptions);
        setPreviewHtml(html);
        if (previewMode === 'pdf' && serverOk) {
          const blob = await renderPdfOnServer(html, docOptions.title, 'onizleme.pdf');
          if (!alive) return;
          setPdfPreviewUrl((old) => {
            if (old) URL.revokeObjectURL(old);
            return URL.createObjectURL(blob);
          });
          const raw = await blob.text();
          setPageCount((raw.match(/\/Type\s*\/Page[^s]/g) || []).length || null);
        } else setPageCount(null);
      } catch (e) {
        console.warn('PDF önizlemesi oluşturulamadı', e);
      } finally {
        if (alive) setBuilding(false);
      }
    }, previewMode === 'pdf' ? 700 : 260);
    return () => {
      alive = false;
      clearTimeout(t);
    };
  }, [isOpen, loading, buildBody, docOptions, previewMode, serverOk]);

  useEffect(() => () => {
    if (pdfPreviewUrl) URL.revokeObjectURL(pdfPreviewUrl);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const previewDoc = useMemo(
    () => (previewHtml ? previewHtml.replace('</head>', `<style>html{zoom:${previewZoom.toFixed(3)}}body{padding:16px 0 32px!important}</style></head>`) : ''),
    [previewHtml, previewZoom]
  );

  /* ---- Çıktı ---- */
  const fileName = `${safeFileName(`${coverInfo.kicker}_${coverInfo.title}`)}${page.format === 'tablet' ? '_Tablet' : ''}.pdf`;
  const fullDocument = async () => {
    const body = await buildBody(false);
    if (!body) throw new Error('Seçimde içerik yok');
    return buildDocument(body, docOptions);
  };

  const handleDownload = async () => {
    setBusy('PDF hazırlanıyor…');
    try {
      const html = await fullDocument();
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
    }
  };

  if (!isOpen) return null;

  const canInlinePdf = typeof navigator === 'undefined' || (navigator as any).pdfViewerEnabled !== false;
  const itemCount = isQuestionKind(kind) ? filtered.length : kind === 'learn' ? (deck ? chosenStepCount : 0) : sumIds.length;
  const summaryLine = loading
    ? 'Yükleniyor…'
    : isQuestionKind(kind)
      ? `${filtered.length} soru · ${PRESETS.find((p) => matchesPreset(qopt, p.apply))?.label || 'Özel'} · ${PAGE_SIZE[page.format].label}`
      : kind === 'learn'
        ? deck ? `${chosenStepCount} adım · ${deckName(deck)} · ${PAGE_SIZE[page.format].label}` : 'Ders seç'
        : `${sumIds.length} özet · ${PAGE_SIZE[page.format].label}`;

  return createPortal(
    <div
      className="ms-overlay fixed inset-0 z-[80] bg-[rgba(14,26,38,0.5)] backdrop-blur-[2px] flex items-stretch sm:items-center justify-center sm:p-5"
      onMouseDown={(e) => e.target === e.currentTarget && onClose()}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="pdf-studio-title"
        aria-busy={!!busy}
        className="relative bg-white w-full max-w-[1320px] h-full sm:h-[min(94vh,960px)] sm:rounded-2xl shadow-xl overflow-hidden grid grid-rows-[auto_minmax(0,1fr)_auto] text-ink"
      >
        {/* ---------- Üst: başlık + içerik türü ---------- */}
        <header className="flex flex-wrap items-center gap-x-4 gap-y-3 px-4 sm:px-6 py-3.5 border-b border-line">
          <span className="w-10 h-10 rounded-xl bg-accent text-white flex items-center justify-center shrink-0 shadow-md">
            <FileDown className="w-5 h-5" />
          </span>
          <div className="min-w-0 flex-1 lg:flex-none lg:w-[220px]">
            <h2 id="pdf-studio-title" className="m-0 font-display font-bold text-[19px] tracking-[-0.02em] leading-tight">PDF stüdyosu</h2>
            <p className="m-0 text-[13px] text-ink-3 truncate">
              {serverOk === false ? 'Tarayıcıdan kaydedilir' : 'Ekrandaki tasarımla, birebir'}
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="PDF stüdyosunu kapat"
            className="lg:order-last w-10 h-10 rounded-full flex items-center justify-center text-ink-2 hover:text-ink hover:bg-canvas cursor-pointer shrink-0"
          >
            <X className="w-5 h-5" />
          </button>
          <div className="w-full lg:w-auto lg:flex-1 min-w-0 flex lg:justify-center">
            <div role="radiogroup" aria-label="İçerik" className="flex gap-1 bg-canvas rounded-xl p-1 overflow-x-auto max-w-full [scrollbar-width:none]">
              {KINDS.map(({ id, label, icon: Icon }) => {
                const on = kind === id;
                return (
                  <button
                    key={id}
                    type="button"
                    role="radio"
                    aria-checked={on}
                    onClick={() => setKind(id)}
                    className={`h-10 px-3.5 rounded-[11px] inline-flex items-center justify-center gap-2 text-[14px] whitespace-nowrap cursor-pointer transition-all ${
                      on ? 'bg-white text-ink font-semibold shadow-xs' : 'text-ink-2 hover:text-ink'
                    }`}
                  >
                    <Icon className={`w-4 h-4 ${on ? 'text-accent' : ''}`} />
                    {label}
                  </button>
                );
              })}
            </div>
          </div>
        </header>

        {/* ---------- Gövde ---------- */}
        <div className="min-h-0 overflow-y-auto lg:overflow-hidden grid grid-cols-1 lg:grid-cols-[400px_minmax(0,1fr)]">
          <aside className="lg:overflow-y-auto bg-blue-50 lg:border-r border-line px-4 sm:px-6 py-5 flex flex-col gap-6 min-w-0">
            <button
              type="button"
              onClick={() => setSettingsOpenMobile((v) => !v)}
              aria-expanded={settingsOpenMobile}
              className="lg:hidden -mb-2 self-start text-[13px] font-semibold text-accent inline-flex items-center gap-1 cursor-pointer"
            >
              <ChevronDown className={`w-4 h-4 transition-transform ${settingsOpenMobile ? 'rotate-180' : ''}`} />
              {settingsOpenMobile ? 'Ayarları gizle' : 'Ayarları göster'}
            </button>
            <div className={`${settingsOpenMobile ? 'flex' : 'hidden'} lg:flex flex-col gap-6 min-w-0`}>
              {isQuestionKind(kind) && (
                <QuestionSettings
                  kind={kind}
                  o={qopt}
                  set={setQopt}
                  sel={{
                    committees, committeeId, setCommitteeId, years, year, setYear, disciplines, discipline, setDiscipline, topics, topic, setTopic,
                    search, setSearch, onlyAnswered, setOnlyAnswered, onlyExplained, setOnlyExplained, onlyAudited, setOnlyAudited,
                    sortBy, setSortBy, limit, setLimit, ornekDers, setOrnekDers, ornekLevels, setOrnekLevels, includeBranching, setIncludeBranching,
                    deckId, setDeckId, total: baseQuestions.length,
                  }}
                />
              )}
              {kind === 'learn' && (
                <LessonSettings
                  o={lopt}
                  set={setLopt}
                  deckId={deckId}
                  setDeckId={(id) => {
                    setDeckId(id);
                    setPickedSteps([]);
                  }}
                  steps={steps.map((s) => ({ number: s.number, title: s.title, section: s.section, checkpoint: s.checkpoint }))}
                  sections={sections.map((s) => ({ index: s.index, name: s.name, numbers: s.steps.map((i) => steps[i].number) }))}
                  picked={pickedSteps}
                  setPicked={setPickedSteps}
                  ixCounts={ixCounts}
                />
              )}
              {kind === 'summary' && (
                <SummarySettings o={sopt} set={setSopt} kurul={sumKurul} setKurul={setSumKurul} list={kurulSummaries} picked={sumIds} setPicked={setSumIds} />
              )}
              <PageSection page={page} setPage={setPage} landscapeHint={kind === 'learn'} />
              {loadError && <p className="m-0 text-[13px] text-warn bg-warn-soft rounded-xl px-3 py-2.5">{loadError}</p>}
            </div>
          </aside>

          {/* Önizleme */}
          <section aria-label="Önizleme" className="bg-blue-100 flex flex-col min-w-0 min-h-[70dvh] lg:min-h-0 p-3 sm:p-5 gap-3">
            <div className="flex items-center gap-2 px-1 flex-wrap">
              <span className="text-[12px] font-semibold uppercase tracking-[0.08em] text-ink-3">Önizleme</span>
              {building ? (
                <span className="h-6 px-2 rounded-full bg-white text-[12px] text-accent font-medium inline-flex items-center gap-1.5">
                  <RefreshCw className="w-3 h-3 animate-spin" /> Güncelleniyor
                </span>
              ) : (
                pageCount != null && previewMode === 'pdf' && (
                  <span className="h-6 px-2 rounded-full bg-white text-[12px] text-ink-2 font-medium inline-flex items-center">
                    {previewTruncated ? `Önizleme ${pageCount} sayfa` : `${pageCount} sayfa`}
                  </span>
                )
              )}
              <span className="flex-1" />
              {serverOk && canInlinePdf && (
                <div role="radiogroup" aria-label="Önizleme türü" className="grid grid-cols-2 gap-1 bg-white/70 rounded-lg p-0.5">
                  {(
                    [
                      ['html', 'Hızlı', MonitorSmartphone],
                      ['pdf', 'Gerçek PDF', FileText],
                    ] as const
                  ).map(([id, label, Icon]) => (
                    <button
                      key={id}
                      type="button"
                      role="radio"
                      aria-checked={previewMode === id}
                      onClick={() => setPreviewMode(id)}
                      className={`h-7 px-2.5 rounded-md text-[12.5px] inline-flex items-center gap-1.5 cursor-pointer ${previewMode === id ? 'bg-white font-semibold text-ink shadow-xs' : 'text-ink-2'}`}
                    >
                      <Icon className="w-3.5 h-3.5" /> {label}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <div ref={frameBox} className="relative flex-1 min-h-[460px] rounded-2xl overflow-hidden bg-[#E9EDF4] ring-1 ring-[rgba(14,26,38,0.06)]">
              {previewMode === 'pdf' && pdfPreviewUrl && serverOk ? (
                <iframe key={pdfPreviewUrl} title="PDF önizlemesi" src={`${pdfPreviewUrl}#view=FitH&toolbar=0&navpanes=0`} className="absolute inset-0 w-full h-full border-0 bg-white" />
              ) : previewDoc ? (
                <iframe title="Belge önizlemesi" srcDoc={previewDoc} sandbox="allow-same-origin" className="absolute inset-0 w-full h-full border-0" />
              ) : null}
              <BlurOverlay show={building && !!previewDoc} icon={<PaperLoader size={72} />} label="Önizleme güncelleniyor…" />
              {!previewDoc && (
                <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 text-center px-8 ms-fade-in">
                  {loading || building ? (
                    <>
                      <PaperLoader />
                      <p className="m-0 text-[15px] font-semibold text-ink">Sayfalar diziliyor…</p>
                      <p className="m-0 text-[13px] text-ink-3">Önizleme birazdan burada</p>
                    </>
                  ) : (
                    <>
                      <span className="w-14 h-14 rounded-2xl bg-white text-ink-3 flex items-center justify-center">
                        <Eye className="w-7 h-7" />
                      </span>
                      <p className="m-0 text-[16px] font-semibold text-ink">Bu seçimde içerik yok</p>
                      <p className="m-0 text-[14px] text-ink-2 max-w-[340px]">Soldaki filtreleri gevşet ya da başka bir ders seç.</p>
                    </>
                  )}
                </div>
              )}
            </div>
            {previewTruncated && previewDoc && (
              <p className="m-0 px-1 text-[12.5px] text-ink-3">
                Önizleme hızlı olsun diye kısaltıldı; indirilen PDF seçimin tamamını ({itemCount} {isQuestionKind(kind) ? 'soru' : kind === 'learn' ? 'adım' : 'özet'}) içerir.
              </p>
            )}
          </section>
        </div>

        <BlurOverlay show={!!busy} fixed={false} icon={<PaperLoader size={96} />} label={busy || ''} hint="Büyük seçimlerde yarım dakikayı bulabilir" />

        {/* ---------- Alt: özet + işlemler ---------- */}
        <footer className="border-t border-line bg-white px-4 sm:px-6 py-3 pb-[max(env(safe-area-inset-bottom),12px)] sm:pb-3 flex flex-wrap sm:flex-nowrap items-center gap-x-3 gap-y-2">
          <p className="m-0 min-w-0 flex-1 basis-full sm:basis-auto text-[14px] text-ink-2 truncate" role="status">
            <span className="font-semibold text-ink">{summaryLine}</span>
          </p>
          <button
            type="button"
            onClick={handlePrint}
            disabled={!itemCount || !!busy}
            title="Tarayıcının yazdırma penceresini açar"
            className="h-11 px-3.5 rounded-xl border border-line bg-white text-ink text-[14px] font-semibold inline-flex items-center gap-2 cursor-pointer hover:border-line-2 disabled:opacity-50"
          >
            <Printer className="w-4 h-4" />
            <span className="hidden sm:inline">Yazdır</span>
          </button>
          <button
            type="button"
            onClick={handleHtml}
            disabled={!itemCount || !!busy}
            title="İnternetsiz açılabilen tek dosya HTML"
            className="h-11 px-3.5 rounded-xl border border-line bg-white text-ink text-[14px] font-semibold inline-flex items-center gap-2 cursor-pointer hover:border-line-2 disabled:opacity-50"
          >
            <FileCode className="w-4 h-4" />
            <span className="hidden sm:inline">HTML</span>
          </button>
          <button
            type="button"
            onClick={handleDownload}
            disabled={!itemCount || !!busy || loading}
            className="flex-1 sm:flex-none h-11 px-6 rounded-xl bg-accent hover:bg-accent-hover text-white text-[15px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
          >
            {busy ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
            {busy ? 'Hazırlanıyor…' : 'PDF indir'}
          </button>
        </footer>
      </div>
    </div>,
    document.body
  );
};

const matchesPreset = (o: QuestionDocOptions, p: Partial<QuestionDocOptions>) =>
  (Object.keys(p) as (keyof QuestionDocOptions)[]).every((k) => o[k] === p[k]);

/* ===========================================================================
 * Soru ayarları
 * ========================================================================= */
interface QSel {
  committees: Committee[]; committeeId: string; setCommitteeId: (v: string) => void;
  years: string[]; year: string; setYear: (v: string) => void;
  disciplines: string[]; discipline: string; setDiscipline: (v: string) => void;
  topics: string[]; topic: string; setTopic: (v: string) => void;
  search: string; setSearch: (v: string) => void;
  onlyAnswered: boolean; setOnlyAnswered: (v: boolean) => void;
  onlyExplained: boolean; setOnlyExplained: (v: boolean) => void;
  onlyAudited: boolean; setOnlyAudited: (v: boolean) => void;
  sortBy: 'number' | 'year' | 'discipline'; setSortBy: (v: 'number' | 'year' | 'discipline') => void;
  limit: number; setLimit: (v: number) => void;
  ornekDers: string; setOrnekDers: (v: string) => void;
  ornekLevels: string[]; setOrnekLevels: (v: string[]) => void;
  includeBranching: boolean; setIncludeBranching: (v: boolean) => void;
  deckId: string; setDeckId: (v: string) => void;
  total: number;
}

const QuestionSettings: React.FC<{ kind: PdfContentKind; o: QuestionDocOptions; set: (p: Partial<QuestionDocOptions>) => void; sel: QSel }> = ({ kind, o, set, sel }) => {
  const sol = o.mode === 'solution';
  const committeeOptions = Object.entries(COMMITTEE_NAME);
  return (
    <>
      <Section title="Hazır ayar">
        <div role="radiogroup" aria-label="Hazır ayar" className="grid grid-cols-3 gap-2">
          {PRESETS.map((p) => {
            const on = matchesPreset(o, p.apply);
            const Icon = p.icon;
            return (
              <button
                key={p.id}
                type="button"
                role="radio"
                aria-checked={on}
                onClick={() => set(p.apply)}
                className={`min-h-[86px] px-1.5 py-2.5 rounded-2xl border flex flex-col items-center justify-center gap-1 text-center cursor-pointer transition-all ${
                  on ? 'border-accent bg-accent-soft/60 shadow-xs' : 'border-line bg-white hover:border-line-2'
                }`}
              >
                <span className={`w-8 h-8 rounded-[10px] flex items-center justify-center ${on ? 'bg-accent text-white' : 'bg-canvas text-ink-2'}`}>
                  <Icon className="w-4 h-4" />
                </span>
                <span className={`text-[13px] leading-tight ${on ? 'font-semibold' : 'font-medium'} text-ink`}>{p.label}</span>
                <span className="text-[11.5px] leading-tight text-ink-3">{p.hint}</span>
              </button>
            );
          })}
        </div>
      </Section>

      <Section title="Seçim" aside={<span className="text-[12.5px] text-ink-3">{sel.total} soru</span>}>
        {kind === 'ornek' && (
          <>
            <SelectField label="Ders" value={sel.ornekDers} onChange={sel.setOrnekDers}>
              <option value="all">Kurul 1 · tüm dersler</option>
              {ORNEK_INDEX.map((r) => (
                <option key={r.id} value={r.id}>{r.sira}. {r.konu} · {r.soru_sayisi}</option>
              ))}
            </SelectField>
            <ChipToggle
              label="Zorluk"
              options={[['kolay', 'Kolay'], ['orta', 'Orta'], ['zor', 'Zor']]}
              value={sel.ornekLevels}
              onChange={(v) => sel.setOrnekLevels(v.length ? v : ['kolay', 'orta', 'zor'])}
            />
          </>
        )}
        {kind === 'mini' && (
          <>
            <DeckSelect value={sel.deckId} onChange={sel.setDeckId} />
            <SwitchGroup>
              <SwitchRow label="Klinik karar soruları" hint="Vaka senaryolu karar sorularını da ekle" checked={sel.includeBranching} onChange={sel.setIncludeBranching} />
            </SwitchGroup>
          </>
        )}
        {(kind === 'past' || kind === 'pool') && (
          <>
            <SelectField
              label="Kurul"
              value={sel.committeeId}
              onChange={(v) => {
                sel.setCommitteeId(v);
                sel.setYear('all');
                sel.setDiscipline('all');
                sel.setTopic('all');
              }}
            >
              <option value="all">Tüm kurullar</option>
              {committeeOptions.map(([id, name]) => <option key={id} value={id}>{name}</option>)}
            </SelectField>
            <div className="grid grid-cols-2 gap-2">
              {kind === 'past' && (
                <SelectField label="Yıl" value={sel.year} onChange={sel.setYear} disabled={!sel.years.length}>
                  <option value="all">Tüm yıllar</option>
                  {sel.years.map((y) => <option key={y} value={y}>{y}</option>)}
                </SelectField>
              )}
              <SelectField label="Ders" value={sel.discipline} onChange={(v) => { sel.setDiscipline(v); sel.setTopic('all'); }} disabled={!sel.disciplines.length}>
                <option value="all">Tüm dersler</option>
                {sel.disciplines.map((d) => <option key={d} value={d}>{d}</option>)}
              </SelectField>
            </div>
            {kind === 'past' && sel.topics.length > 0 && (
              <SelectField label="Konu" value={sel.topic} onChange={sel.setTopic}>
                <option value="all">Tüm konular</option>
                {sel.topics.map((t) => <option key={t} value={t}>{t}</option>)}
              </SelectField>
            )}
          </>
        )}
        <label className="relative flex flex-col min-w-0">
          <span className="pointer-events-none absolute left-3.5 top-2 text-[11px] font-semibold text-ink-3">Metinde ara</span>
          <input
            type="search"
            value={sel.search}
            onChange={(e) => sel.setSearch(e.target.value)}
            placeholder="ör. nefrotik, ADAMTS13"
            className="w-full h-[54px] pt-4 px-3.5 rounded-xl border border-line bg-white text-[14.5px] text-ink outline-0 focus:border-accent"
          />
        </label>
        {(kind === 'past' || kind === 'pool') && (
          <Segmented
            label="Sıralama"
            value={sel.sortBy}
            onChange={sel.setSortBy}
            options={[['year', 'Yıl'], ['discipline', 'Ders'], ['number', 'Soru no']]}
          />
        )}
        <Segmented
          label="Soru sayısı"
          value={String(sel.limit)}
          onChange={(v) => sel.setLimit(Number(v))}
          options={[['50', '50'], ['100', '100'], ['200', '200'], ['500', '500'], ['0', 'Hepsi']]}
        />
        <SwitchGroup>
          <SwitchRow label="Yalnız cevabı belli olanlar" checked={sel.onlyAnswered} onChange={sel.setOnlyAnswered} />
          <SwitchRow label="Yalnız açıklamalı olanlar" hint="Açıklaması ya da şık analizi olan" checked={sel.onlyExplained} onChange={sel.setOnlyExplained} />
          {kind === 'past' && <SwitchRow label="Yalnız denetleyici onaylı" checked={sel.onlyAudited} onChange={sel.setOnlyAudited} />}
        </SwitchGroup>
      </Section>

      <Section title="Kitapçık türü">
        <Segmented<BookletMode>
          label="Cevaplar"
          value={o.mode}
          onChange={(v) => set({ mode: v, ...(v === 'student' ? { answerKey: false } : {}) })}
          options={[['student', 'Gizli'], ['solution', 'Çözümlü'], ['key', 'Yalnız anahtar']]}
        />
      </Section>

      <Section title="PDF'e girecekler">
        <SwitchGroup>
          <SwitchRow label="Doğru şıkkı işaretle" hint="Ekrandaki gibi yeşil ve ✓" checked={sol && o.markCorrect} disabled={!sol} onChange={(v) => set({ markCorrect: v })} />
          <SwitchRow label="Soru açıklaması" hint="Hakkında penceresindeki açıklama" checked={sol && o.explanation} disabled={!sol} onChange={(v) => set({ explanation: v })} />
          <SwitchRow label="Referans kaynaklar" checked={sol && o.refs} disabled={!sol} onChange={(v) => set({ refs: v })} />
          <SwitchRow label="Üst bilgi" hint="Ders · kurul · yıl satırı" checked={o.meta} onChange={(v) => set({ meta: v })} />
          <SwitchRow label="Rozetler" hint="Denetleyici, Faz 14, tartışmalı cevap" checked={o.badges} onChange={(v) => set({ badges: v })} />
          <SwitchRow label="Not alanı" hint="Her sorunun altında yazma satırları" checked={o.writeSpace} onChange={(v) => set({ writeSpace: v })} />
        </SwitchGroup>
        <Segmented<OptionNotes>
          label="Şık açıklamaları"
          value={o.optionNotes}
          onChange={(v) => set({ optionNotes: v })}
          disabled={!sol}
          options={[['off', 'Yok'], ['inline', 'Şık altında'], ['analysis', 'Analiz tablosu']]}
        />
        <Segmented<'inline' | 'end'>
          label="Çözümün yeri"
          value={o.solutionsAtEnd ? 'end' : 'inline'}
          onChange={(v) => set({ solutionsAtEnd: v === 'end' })}
          disabled={!sol}
          options={[['inline', 'Soru altında'], ['end', 'Kitapçık sonunda']]}
        />
        <SwitchGroup>
          <SwitchRow label="Kapak sayfası" hint="Başlık, istatistik, ad-no alanı" checked={o.cover} onChange={(v) => set({ cover: v })} />
          <SwitchRow label="Cevap anahtarı" hint="Son sayfada tablo" checked={o.answerKey || o.mode === 'key'} disabled={o.mode === 'key'} onChange={(v) => set({ answerKey: v })} />
          <SwitchRow label="Optik form" hint="Kurşun kalemle doldurmak için" checked={o.opticForm} onChange={(v) => set({ opticForm: v })} />
        </SwitchGroup>
      </Section>

      <Section title="Düzen">
        <div role="radiogroup" aria-label="Sütun" aria-disabled={!!o.questionPerPage} className={`grid grid-cols-2 gap-2 ${o.questionPerPage ? 'opacity-50 pointer-events-none' : ''}`}>
          {(
            [
              [1, 'Tek sütun', 'Geniş satırlar'],
              [2, '2 sütun', 'Kitapçık gibi'],
            ] as const
          ).map(([n, label, hint]) => {
            const on = o.columns === n;
            return (
              <button
                key={n}
                type="button"
                role="radio"
                aria-checked={on}
                disabled={!!o.questionPerPage}
                onClick={() => set({ columns: n })}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl border text-left cursor-pointer transition-all ${on ? 'border-accent bg-accent-soft/60 shadow-xs' : 'border-line bg-white hover:border-line-2'}`}
              >
                <PageGlyph cols={n} on={on} />
                <span className="min-w-0">
                  <span className={`block text-[13.5px] ${on ? 'font-semibold' : 'font-medium'} text-ink`}>{label}</span>
                  <span className="block text-[12px] text-ink-3">{hint}</span>
                </span>
              </button>
            );
          })}
        </div>
        <SelectField label="Gruplama" value={o.groupBy} onChange={(v) => set({ groupBy: v as GroupBy })}>
          <option value="none">Gruplama yok</option>
          {(kind === 'past' || kind === 'pool') && <option value="discipline">Derse göre</option>}
          {kind === 'past' && <option value="year">Yıla göre</option>}
          {(kind === 'past' || kind === 'pool') && <option value="committee">Kurula göre</option>}
          {kind === 'past' && <option value="topic">Konuya göre</option>}
          {kind === 'ornek' && <option value="group">Kazanıma göre</option>}
          {kind === 'ornek' && <option value="topic">Derse göre</option>}
          {kind === 'mini' && <option value="group">Adıma göre</option>}
        </SelectField>
        <SwitchGroup>
          <SwitchRow label="Her grup yeni sayfada" checked={o.groupNewPage} disabled={o.groupBy === 'none'} onChange={(v) => set({ groupNewPage: v })} />
          <SwitchRow
            label="Her soru ayrı sayfada"
            hint={o.solutionsAtEnd ? 'Sonda çözümler de birer sayfa' : 'Soru ve çözümü tek sayfada'}
            checked={!!o.questionPerPage}
            onChange={(v) => set({ questionPerPage: v })}
          />
          <SwitchRow label="Sıkı yerleşim" hint="Daha az boşluk, daha çok soru" checked={o.compact} disabled={!!o.questionPerPage} onChange={(v) => set({ compact: v })} />
          {(kind === 'past' || kind === 'pool') && (
            <SwitchRow label="Orijinal soru numaraları" hint="Kapalıyken 1'den başlar" checked={o.numbering === 'original'} onChange={(v) => set({ numbering: v ? 'original' : 'sequential' })} />
          )}
        </SwitchGroup>
      </Section>
    </>
  );
};

/* ===========================================================================
 * Öğren ayarları
 * ========================================================================= */
const LessonSettings: React.FC<{
  o: LessonDocOptions;
  set: (p: Partial<LessonDocOptions>) => void;
  deckId: string;
  setDeckId: (v: string) => void;
  steps: { number: number; title: string; section: number; checkpoint: number }[];
  sections: { index: number; name: string; numbers: number[] }[];
  picked: number[];
  setPicked: (v: number[] | ((p: number[]) => number[])) => void;
  ixCounts: Record<string, number>;
}> = ({ o, set, deckId, setDeckId, steps, sections, picked, setPicked, ixCounts }) => {
  const all = !picked.length;
  const has = (n: number) => all || picked.includes(n);
  const toggleSection = (nums: number[]) => {
    const base = all ? steps.map((s) => s.number) : picked;
    const allIn = nums.every((n) => base.includes(n));
    const next = allIn ? base.filter((n) => !nums.includes(n)) : [...new Set([...base, ...nums])].sort((a, b) => a - b);
    setPicked(next.length === steps.length ? [] : next.length ? next : []);
  };
  return (
    <>
      <Section title="Ders">
        <DeckSelect value={deckId} onChange={setDeckId} />
      </Section>

      {steps.length > 0 && (
        <Section
          title={`Adımlar · ${all ? steps.length : picked.length}/${steps.length}`}
          aside={
            !all && (
              <button type="button" onClick={() => setPicked([])} className="text-[13px] font-semibold text-accent cursor-pointer">
                Tümünü seç
              </button>
            )
          }
        >
          <ul className="list-none m-0 p-1.5 bg-white border border-line rounded-2xl max-h-[320px] overflow-y-auto flex flex-col gap-0.5">
            {sections.map((sec) => {
              const secOn = sec.numbers.every(has);
              const secSome = sec.numbers.some(has);
              return (
                <li key={sec.index} className="flex flex-col gap-0.5">
                  <button
                    type="button"
                    role="checkbox"
                    aria-checked={secOn ? true : secSome ? 'mixed' : false}
                    onClick={() => toggleSection(sec.numbers)}
                    className="w-full flex items-center gap-3 min-h-10 px-2.5 rounded-[11px] text-left cursor-pointer hover:bg-canvas"
                  >
                    <CheckBox on={secOn} mixed={!secOn && secSome} />
                    <span className="text-[12px] font-semibold uppercase tracking-[0.06em] text-ink-3 shrink-0">Bölüm {sec.index + 1}</span>
                    <span className="text-[13.5px] font-semibold text-ink truncate">{sec.name}</span>
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
                        onClick={() => {
                          const base = all ? steps.map((s) => s.number) : picked;
                          const next = on ? base.filter((x) => x !== n) : [...base, n].sort((a, b) => a - b);
                          setPicked(next.length === steps.length ? [] : next);
                        }}
                        className={`w-full flex items-center gap-3 min-h-10 pl-7 pr-2.5 rounded-[11px] text-left cursor-pointer transition-colors ${on ? 'bg-accent-soft/50' : 'hover:bg-canvas'}`}
                      >
                        <CheckBox on={on} />
                        <span className={`font-mono text-[12px] w-6 shrink-0 ${on ? 'text-accent' : 'text-ink-3'}`}>{n}</span>
                        <span className={`text-[13.5px] truncate ${on ? 'text-ink' : 'text-ink-2'}`}>{st?.title}</span>
                        {st?.checkpoint > 0 && <span className="ms-tag is-accent shrink-0">Tekrar</span>}
                      </button>
                    );
                  })}
                </li>
              );
            })}
          </ul>
        </Section>
      )}

      <Section title="Adım içeriği">
        <SwitchGroup>
          <SwitchRow label="Anlatım" checked={o.narrative} onChange={(v) => set({ narrative: v })} />
          <SwitchRow label="Anahtar maddeler" checked={o.keyPoints} onChange={(v) => set({ keyPoints: v })} />
          <SwitchRow label="Tablolar" checked={o.tables} onChange={(v) => set({ tables: v })} />
          <SwitchRow label="İnfografik ve formüller" checked={o.visuals} onChange={(v) => set({ visuals: v })} />
          <SwitchRow label="Hocanın vurgusu" checked={o.teacher} onChange={(v) => set({ teacher: v })} />
          <SwitchRow label="Sınav spotları" checked={o.spots} onChange={(v) => set({ spots: v })} />
          <SwitchRow label="Önemli nokta ve sınav ipucu" checked={o.tips} onChange={(v) => set({ tips: v })} />
          <SwitchRow label="Terimler sözlüğü" hint="Adımdaki tıbbi terimler ve tanımları" checked={o.terms} onChange={(v) => set({ terms: v })} />
          <SwitchRow label="Akıl kartları" checked={o.cards} onChange={(v) => set({ cards: v })} />
        </SwitchGroup>
      </Section>

      <Section
        title="Etkileşimler"
        aside={
          <button
            type="button"
            onClick={() => set({ interactives: o.interactives.length ? [] : [...IX_TYPES] })}
            className="text-[13px] font-semibold text-accent cursor-pointer"
          >
            {o.interactives.length ? 'Hiçbiri' : 'Hepsi'}
          </button>
        }
      >
        <div className="flex flex-wrap gap-1.5">
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
                onClick={() => set({ interactives: on ? o.interactives.filter((x) => x !== t) : [...o.interactives, t] as IxType[] })}
                className={`h-9 pl-2.5 pr-3 rounded-full border inline-flex items-center gap-1.5 text-[13px] cursor-pointer transition-all ${
                  on ? 'border-accent bg-accent-soft text-accent font-semibold' : 'border-line bg-white text-ink-2 hover:border-line-2'
                } ${n ? '' : 'opacity-50'}`}
              >
                <Icon className="w-3.5 h-3.5" /> {label}
                <span className="font-mono text-[11px] opacity-70">{n}</span>
              </button>
            );
          })}
        </div>
        <Segmented<AnswerMode>
          label="Cevaplar"
          value={o.answers}
          onChange={(v) => set({ answers: v })}
          options={[['shown', 'Açık'], ['end', 'Belge sonunda'], ['hidden', 'Çalışma kâğıdı']]}
        />
        <SwitchGroup>
          <SwitchRow label="Şık açıklamaları" hint="Mini soru ve klinik kararda neden doğru / yanlış" checked={o.optionNotes && o.answers !== 'hidden'} disabled={o.answers === 'hidden'} onChange={(v) => set({ optionNotes: v })} />
        </SwitchGroup>
      </Section>

      <Section title="Düzen">
        <SwitchGroup>
          <SwitchRow label="Her adım yeni sayfada" hint="Kapalıyken adımlar akarak dizilir" checked={o.stepPerPage} onChange={(v) => set({ stepPerPage: v })} />
          <SwitchRow label="Bölüm başlıkları" checked={o.sectionTitles} onChange={(v) => set({ sectionTitles: v })} />
          <SwitchRow label="İçindekiler" checked={o.toc} onChange={(v) => set({ toc: v })} />
          <SwitchRow label="Kapak sayfası" checked={o.cover} onChange={(v) => set({ cover: v })} />
        </SwitchGroup>
      </Section>
    </>
  );
};

/* ===========================================================================
 * Özet ayarları
 * ========================================================================= */
const SummarySettings: React.FC<{
  o: SummaryDocOptions;
  set: (p: Partial<SummaryDocOptions>) => void;
  kurul: number;
  setKurul: (k: number) => void;
  list: SummaryMeta[];
  picked: string[];
  setPicked: (v: string[]) => void;
}> = ({ o, set, kurul, setKurul, list, picked, setPicked }) => (
  <>
    <Section title="Kurul">
      <SelectField label="Kurul" value={String(kurul)} onChange={(v) => setKurul(Number(v))}>
        {[1, 2, 3, 4, 5, 6].map((k) => <option key={k} value={k}>{COMMITTEE_NAME[`donem3-kurul${k}`]}</option>)}
      </SelectField>
    </Section>
    <Section
      title={`Özetler · ${picked.length}/${list.length}`}
      aside={
        <button type="button" onClick={() => setPicked(picked.length === list.length ? list.slice(0, 1).map((m) => m.id) : list.map((m) => m.id))} className="text-[13px] font-semibold text-accent cursor-pointer">
          {picked.length === list.length ? 'Seçimi sıfırla' : 'Tümünü seç'}
        </button>
      }
    >
      <ul className="list-none m-0 p-1.5 bg-white border border-line rounded-2xl max-h-[320px] overflow-y-auto flex flex-col gap-0.5">
        {list.map((m) => {
          const on = picked.includes(m.id);
          return (
            <li key={m.id}>
              <button
                type="button"
                role="checkbox"
                aria-checked={on}
                onClick={() => setPicked(on ? picked.filter((x) => x !== m.id) : list.filter((x) => x.id === m.id || picked.includes(x.id)).map((x) => x.id))}
                className={`w-full flex items-center gap-3 min-h-11 px-2.5 rounded-[11px] text-left cursor-pointer transition-colors ${on ? 'bg-accent-soft/50' : 'hover:bg-canvas'}`}
              >
                <CheckBox on={on} />
                <span className="min-w-0">
                  <span className={`block text-[13.5px] truncate ${on ? 'text-ink font-medium' : 'text-ink-2'}`}>{m.title}</span>
                  <span className="block text-[12px] text-ink-3 truncate">{m.discipline}</span>
                </span>
              </button>
            </li>
          );
        })}
      </ul>
    </Section>
    <Section title="PDF'e girecekler">
      <SwitchGroup>
        <SwitchRow label="Konu başlıkları" hint="Özetin başında başlık kartları" checked={o.keyPoints} onChange={(v) => set({ keyPoints: v })} />
        <SwitchRow label="Tablolar" checked={o.tables} onChange={(v) => set({ tables: v })} />
        <SwitchRow label="Not kutuları" hint="Önemli, sınav spotu, klinik ipucu" checked={o.callouts} onChange={(v) => set({ callouts: v })} />
        <SwitchRow label="İçindekiler" checked={o.toc} onChange={(v) => set({ toc: v })} />
        <SwitchRow label="Kapak sayfası" checked={o.cover} onChange={(v) => set({ cover: v })} />
      </SwitchGroup>
      <Segmented<SummaryQuestions>
        label="Özetteki sorular"
        value={o.questions}
        onChange={(v) => set({ questions: v })}
        options={[['answered', 'Cevaplı'], ['plain', 'Cevapsız'], ['none', 'Çıkar']]}
      />
    </Section>
  </>
);

/* ===========================================================================
 * Sayfa ayarları ve küçük yapı taşları
 * ========================================================================= */
const PageSection: React.FC<{ page: PageSettings; setPage: (p: Partial<PageSettings>) => void; landscapeHint?: boolean }> = ({ page, setPage }) => (
  <Section title="Sayfa">
    <div role="radiogroup" aria-label="Sayfa boyutu" className="grid grid-cols-2 gap-2">
      {(['a4', 'a4-landscape', 'tablet', 'letter'] as PageFormat[]).map((id) => {
        const on = page.format === id;
        const sz = PAGE_SIZE[id];
        const scale = 34 / Math.max(sz.w, sz.h);
        return (
          <button
            key={id}
            type="button"
            role="radio"
            aria-checked={on}
            onClick={() => setPage({ format: id })}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-xl border text-left cursor-pointer transition-all ${on ? 'border-accent bg-accent-soft/60 shadow-xs' : 'border-line bg-white hover:border-line-2'}`}
          >
            <span className="w-9 h-10 flex items-center justify-center shrink-0" aria-hidden="true">
              <span className={`border-[1.5px] bg-white ${on ? 'border-accent' : 'border-line-2'} ${id === 'tablet' ? 'rounded-md' : 'rounded-sm'}`} style={{ width: sz.w * scale, height: sz.h * scale }} />
            </span>
            <span className="min-w-0">
              <span className={`block text-[13.5px] ${on ? 'font-semibold' : 'font-medium'} text-ink`}>{sz.label}</span>
              <span className="block text-[12px] text-ink-3 leading-snug">{id === 'tablet' ? 'Ekranı doldurur' : id === 'a4-landscape' ? 'Geniş tablolar' : id === 'letter' ? 'ABD kâğıdı' : 'Yazdırmak için'}</span>
            </span>
          </button>
        );
      })}
    </div>
    <Segmented<FontScale> label="Yazı boyutu" value={page.fontScale} onChange={(v) => setPage({ fontScale: v })} options={[['sm', 'Küçük'], ['md', 'Orta'], ['lg', 'Büyük']]} />
    <SwitchGroup>
      <SwitchRow label="Sayfa numarası" hint="Sağ altta 3 / 12" checked={page.pageNumbers} onChange={(v) => setPage({ pageNumbers: v })} />
      <SwitchRow label="Üst bilgi" hint="Her sayfada belge adı" checked={page.runningHeader} onChange={(v) => setPage({ runningHeader: v })} />
    </SwitchGroup>
  </Section>
);

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
    <SelectField label="Ders" value={value} onChange={onChange}>
      {groups.map(([g, list]) => (
        <optgroup key={g} label={g}>
          {list.map((d) => <option key={d.id} value={d.id}>{deckName(d)} · {d.slideCount} adım</option>)}
        </optgroup>
      ))}
    </SelectField>
  );
};

const Section: React.FC<{ title: string; aside?: React.ReactNode; children: React.ReactNode }> = ({ title, aside, children }) => (
  <section className="flex flex-col gap-2.5">
    <div className="flex items-baseline justify-between gap-2 px-0.5">
      <h3 className="m-0 text-[12px] font-semibold uppercase tracking-[0.08em] text-ink-3">{title}</h3>
      {aside}
    </div>
    {children}
  </section>
);

const SelectField: React.FC<{ label: string; value: string; onChange: (v: string) => void; disabled?: boolean; children: React.ReactNode }> = ({ label, value, onChange, disabled, children }) => (
  <label className={`relative flex flex-col min-w-0 ${disabled ? 'opacity-50' : ''}`}>
    <span className="sr-only">{label}</span>
    <span className="pointer-events-none absolute left-3.5 top-2 text-[11px] font-semibold text-ink-3">{label}</span>
    <select
      value={value}
      disabled={disabled}
      onChange={(e) => onChange(e.target.value)}
      className="appearance-none w-full h-[54px] pt-4 pl-3.5 pr-9 rounded-xl border border-line bg-white text-[14.5px] text-ink cursor-pointer outline-0 focus:border-accent focus:shadow-xs truncate disabled:cursor-not-allowed"
    >
      {children}
    </select>
    <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-3" />
  </label>
);

function Segmented<T extends string>({ label, value, onChange, options, disabled }: { label: string; value: T; onChange: (v: T) => void; options: [T, string][]; disabled?: boolean }) {
  return (
    <div className={`flex flex-col gap-1.5 ${disabled ? 'opacity-50 pointer-events-none' : ''}`}>
      <span className="px-0.5 text-[12.5px] font-medium text-ink-2">{label}</span>
      <div role="radiogroup" aria-label={label} aria-disabled={disabled} className="grid gap-1 bg-blue-100 rounded-xl p-1" style={{ gridTemplateColumns: `repeat(${options.length}, minmax(0, 1fr))` }}>
        {options.map(([id, text]) => {
          const on = value === id;
          return (
            <button
              key={id}
              type="button"
              role="radio"
              aria-checked={on}
              disabled={disabled}
              onClick={() => onChange(id)}
              className={`h-9 px-1 rounded-lg text-[13px] leading-tight cursor-pointer transition-all ${on ? 'bg-white text-ink font-semibold shadow-xs' : 'text-ink-2 hover:text-ink'}`}
            >
              {text}
            </button>
          );
        })}
      </div>
    </div>
  );
}

const ChipToggle: React.FC<{ label: string; options: [string, string][]; value: string[]; onChange: (v: string[]) => void }> = ({ label, options, value, onChange }) => (
  <div className="flex flex-col gap-1.5">
    <span className="px-0.5 text-[12.5px] font-medium text-ink-2">{label}</span>
    <div className="flex flex-wrap gap-1.5">
      {options.map(([id, text]) => {
        const on = value.includes(id);
        return (
          <button
            key={id}
            type="button"
            role="checkbox"
            aria-checked={on}
            onClick={() => onChange(on ? value.filter((x) => x !== id) : [...value, id])}
            className={`h-9 px-3.5 rounded-full border inline-flex items-center gap-1.5 text-[13px] cursor-pointer ${on ? 'border-accent bg-accent-soft text-accent font-semibold' : 'border-line bg-white text-ink-2'}`}
          >
            {on && <Check className="w-3.5 h-3.5" strokeWidth={3} />} {text}
          </button>
        );
      })}
    </div>
  </div>
);

const SwitchGroup: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="bg-white border border-line rounded-2xl divide-y divide-line-soft overflow-hidden">{children}</div>
);

const SwitchRow: React.FC<{ label: string; hint?: string; checked: boolean; onChange: (v: boolean) => void; disabled?: boolean }> = ({ label, hint, checked, onChange, disabled }) => (
  <button
    type="button"
    role="switch"
    aria-checked={checked}
    disabled={disabled}
    onClick={() => onChange(!checked)}
    className="w-full flex items-center gap-3 min-h-[54px] px-4 py-2 text-left cursor-pointer disabled:cursor-not-allowed disabled:opacity-50 hover:bg-blue-50"
  >
    <span className="flex-1 min-w-0">
      <span className="block text-[14px] font-medium text-ink">{label}</span>
      {hint && <span className="block text-[12.5px] text-ink-3 leading-snug">{hint}</span>}
    </span>
    <span className={`relative w-[42px] h-[26px] rounded-full shrink-0 transition-colors ${checked ? 'bg-accent' : 'bg-line-2'}`} aria-hidden="true">
      <span className={`absolute top-[3px] left-[3px] w-5 h-5 rounded-full bg-white shadow-xs transition-transform ${checked ? 'translate-x-4' : ''}`} />
    </span>
  </button>
);

const CheckBox: React.FC<{ on: boolean; mixed?: boolean }> = ({ on, mixed }) => (
  <span className={`w-5 h-5 rounded-md flex items-center justify-center shrink-0 transition-colors ${on || mixed ? 'bg-accent text-white' : 'bg-white border border-line-2'}`}>
    {on ? <Check className="w-3.5 h-3.5" strokeWidth={3} /> : mixed ? <span className="w-2.5 h-[2px] rounded bg-white" /> : null}
  </span>
);

const PageGlyph: React.FC<{ cols: 1 | 2; on: boolean }> = ({ cols, on }) => (
  <span className={`w-8 h-10 rounded-sm border flex gap-[3px] p-[5px] shrink-0 ${on ? 'border-accent bg-white' : 'border-line-2 bg-white'}`} aria-hidden="true">
    {Array.from({ length: cols }).map((_, i) => (
      <span key={i} className="flex-1 flex flex-col gap-[3px]">
        {[0, 1, 2, 3, 4].map((j) => (
          <span key={j} className={`h-[2px] rounded-full ${on ? 'bg-accent/60' : 'bg-line-2'}`} style={{ width: j === 4 ? '60%' : '100%' }} />
        ))}
      </span>
    ))}
  </span>
);
