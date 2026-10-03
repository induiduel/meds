import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import {
  Search,
  X,
  ChevronLeft,
  ChevronRight,
  Maximize2,
  Minimize2,
  Clock,
  User,
  Layers,
  Volume2,
  Copy,
  Check,
  CheckCircle2,
  XCircle,
  Lightbulb,
  AlertTriangle,
  AlertCircle,
  HelpCircle,
  EyeOff,
  Stethoscope,
  Sparkles,
  Send,
  RefreshCw,
  PanelRightOpen,
  PanelRightClose,
  GalleryHorizontal,
  Rows3,
  Play,
  BookOpen,
  ChevronDown,
  ChevronUp,
  BrainCircuit,
  RotateCcw,
  GraduationCap,
  FileText,
  FileDown,
  ArrowLeftRight,
  Bot,
  Columns,
  Cloud,
} from 'lucide-react';
import { DeckPdfViewer } from './DeckPdfViewer';
import { getDeckOriginalPdf } from '../../data/deckPdfCatalog';
import interactiveDecksData from '../../data/interactive_learning_decks.json';
import {
  GlossaryProvider,
  RenderWithGlossaryTerms,
  SlideTermsPills,
  useGlossary,
} from './MedicalGlossaryPopover';
import { AiThinking } from '../ui/Animations';
import { HighlighterToolbar, Highlightable, isPenActive } from '../ui/Highlighter';
import { SlideDrawingCanvas, DrawingModeToolbarTrigger } from './SlideDrawingCanvas';
import { toast } from '../ui/Toast';
import { safeJsonFetch } from '../../services/api';

// ---------------------------------------------------------------------------
// Data types (shape of interactive_learning_decks.json)
// ---------------------------------------------------------------------------
export interface ProfessorAudioHighlight {
  timestamp: string;
  quote: string;
  emphasisType: 'direct_exam_warning' | 'pearl' | 'clinical_tip' | 'slide_missing';
  note: string;
}

export interface TranscriptUtterance {
  timestamp: string;
  text: string;
  isHighlighted?: boolean;
}

export interface SlideFlashcard {
  id: string;
  category?: string;
  front?: string;
  back?: string;
  question?: string;
  answer?: string;
  hint?: string;
}

export interface SlideQuestionOption {
  key: string;
  text: string;
  isCorrect?: boolean;
}

export interface SlideRelatedQuestion {
  id: string;
  examYear?: string;
  committeeId?: string;
  discipline?: string;
  topic?: string;
  stem: string;
  options: SlideQuestionOption[];
  correctAnswer: string;
  explanation: string;
  matchScore?: number;
  isPracticeQuestion?: boolean;
}

export interface SlideContentTable {
  title?: string;
  headers: string[];
  rows: string[][];
}

export interface SlideContentFormula {
  title: string;
  formula: string;
  explanation: string;
}

export interface SlideContentInfographic {
  type: 'comparison' | 'process' | 'hierarchy' | 'metrics';
  items: Array<{ label: string; value: string; detail: string; color?: string }>;
}

export interface SlideItem {
  slideNumber: number;
  title: string;
  subtitle: string;
  timeWindow?: string;
  badge: string;
  badgeColor?: string;
  discipline?: string;
  professorAudioHighlight?: ProfessorAudioHighlight;
  synthesisNarrative?: string;
  flashcards?: SlideFlashcard[];
  transcriptUtterances?: TranscriptUtterance[];
  transcriptUtteranceCount?: number;
  coreContent: {
    keyBullets?: Array<{ title: string; desc: string; isKey?: boolean }>;
    table?: SlideContentTable;
    formulaBox?: SlideContentFormula;
    infographic?: SlideContentInfographic;
  };
  spotPearls: string[];
  relatedQuestions: SlideRelatedQuestion[];
  aiPromptSuggestions: string[];
}

export interface InteractiveDeck {
  id: string;
  title: string;
  shortTitle: string;
  discipline: string;
  committee: string;
  instructor: string;
  audioFile: string;
  audioDuration: string;
  confidence: string;
  themeColor: string;
  matchedNoteId: string;
  matchedNoteTitle: string;
  overview: string;
  highYieldPearls: string[];
  slides: SlideItem[];
  totalSlides: number;
  matchedPastQuestionsCount: number;
  totalUtterancesCount?: number;
  assignedUtterancesCount?: number;
}

interface InteractiveDeckViewProps {
  initialDeckId?: string;
  initialSlideNumber?: number;
  /** Fired when a deck is opened (id) or closed (null) so the URL can follow. */
  onDeckChange?: (deckId: string | null) => void;
  /** Opens the PDF dialog; with a target it starts on that deck's slide. */
  onOpenPdfModal?: (target?: { deckId: string; slideNumber: number }) => void;
  onSelectCommittee?: (committeeId: string) => void;
}

// ---------------------------------------------------------------------------
// Small helpers
// ---------------------------------------------------------------------------
const PROGRESS_KEY = 'medsoru_learn_progress_v1';
type DeckProgress = Record<string, { last: number; seen: number[] }>;
const readProgress = (): DeckProgress => {
  try {
    return JSON.parse(localStorage.getItem(PROGRESS_KEY) || '{}');
  } catch {
    return {};
  }
};
const writeProgress = (p: DeckProgress) => {
  try {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(p));
  } catch {
    /* storage unavailable */
  }
};

/** Renders rich text segments with bolding, sub-details, and interactive medical glossary terms. */
const Rich: React.FC<{ text: string; className?: string }> = ({ text, className }) => {
  return <RenderWithGlossaryTerms text={text} className={className} />;
};

/**
 * Structured Synthesis Renderer:
 * Parses paragraphs, ### H3 headings, #### H4 sub-headings, • bullet points,
 * and callouts to provide a clean typographic reading experience.
 */
const StructuredSynthesisRenderer: React.FC<{ text?: string }> = ({ text }) => {
  if (!text) return null;

  // Split into lines
  const lines = text.split('\n');

  return (
    <div className="flex flex-col gap-2 sm:gap-2.5">
      {lines.map((rawLine, idx) => {
        const line = rawLine.trim();
        if (!line) {
          return <div key={idx} className="h-1" />;
        }

        // Section Heading (### Başlık)
        if (line.startsWith('### ')) {
          return (
            <h4
              key={idx}
              className="m-0 pt-2.5 pb-1 border-b border-line-soft text-[14px] sm:text-[15px] font-bold text-ink flex items-center gap-2"
            >
              <span className="w-2 h-2 rounded-full bg-accent shrink-0 shadow-2xs" />
              <Rich text={line.slice(4)} />
            </h4>
          );
        }

        // Sub-heading (#### Alt Başlık)
        if (line.startsWith('#### ')) {
          return (
            <h5
              key={idx}
              className="m-0 pt-1 text-[12px] sm:text-[12.5px] font-bold uppercase tracking-wider text-accent flex items-center gap-2"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-accent/60 shrink-0" />
              <Rich text={line.slice(5)} />
            </h5>
          );
        }

        // Callout (> veya 💡 veya ⚠️ veya 🔴 veya 🚨)
        if (
          line.startsWith('> ') ||
          line.startsWith('💡 ') ||
          line.startsWith('⚠️ ') ||
          line.startsWith('🔴 ') ||
          line.startsWith('🚨 ')
        ) {
          const isRed =
            line.startsWith('🔴') ||
            line.startsWith('🚨') ||
            line.startsWith('⚠️') ||
            /(?:ölümcül|asla|acil|hayati|kritik|kontrendike|sınav tuzağı)/i.test(line);

          const icon = line.startsWith('🚨')
            ? '🚨'
            : line.startsWith('🔴')
              ? '🔴'
              : line.startsWith('⚠️')
                ? '⚠️'
                : isRed
                  ? '🔴'
                  : '💡';

          const content = (line.startsWith('> ') ? line.slice(2) : line).replace(
            /^\s*(💡|⚠️|🔴|🚨)\s*/u,
            ''
          );

          return (
            <div
              key={idx}
              className={`p-2.5 sm:p-3 my-1 rounded-xl border-l-4 text-[12px] sm:text-[12.5px] leading-relaxed flex items-center gap-2.5 shadow-2xs ${
                isRed
                  ? 'bg-red-500/10 dark:bg-red-500/20 border-red-500 text-red-950 dark:text-red-200'
                  : 'bg-accent-soft/30 border-accent text-ink'
              }`}
            >
              <span className="text-[14px] select-none shrink-0" aria-hidden="true">
                {icon}
              </span>
              <div className="min-w-0 flex-1">
                <Rich text={content} />
              </div>
            </div>
          );
        }

        // Sub-bullet (girintili alt madde)
        if (rawLine.startsWith('  - ') || rawLine.startsWith('  • ') || rawLine.startsWith('\t- ') || rawLine.startsWith('\t• ')) {
          const cleanText = line.replace(/^[•\-\*]\s*/, '');
          return (
            <div
              key={idx}
              className="flex items-start gap-2 ml-4.5 my-0.5 text-[11.5px] sm:text-[12px] text-ink-3 leading-relaxed"
            >
              <span className="mt-1.5 w-1 h-1 rounded-full bg-ink-4 shrink-0" />
              <div className="min-w-0 flex-1">
                <Rich text={cleanText} />
              </div>
            </div>
          );
        }

        // Numbered list item (1. 2. 3.)
        const numMatch = line.match(/^(\d+)\.\s+(.*)$/);
        if (numMatch) {
          return (
            <div
              key={idx}
              className="flex items-start gap-2.5 my-1 text-[12.5px] sm:text-[13px] text-ink-2 leading-[1.68]"
            >
              <span className="shrink-0 w-4.5 h-4.5 rounded-full bg-accent-soft text-accent text-[10.5px] font-bold flex items-center justify-center mt-0.5 border border-accent/20 shadow-2xs">
                {numMatch[1]}
              </span>
              <div className="min-w-0 flex-1">
                <Rich text={numMatch[2]} />
              </div>
            </div>
          );
        }

        // Top-level Bullet item (• veya - veya *)
        if (line.startsWith('• ') || line.startsWith('- ') || line.startsWith('* ')) {
          const cleanText = line.replace(/^[•\-\*]\s*/, '');
          return (
            <div
              key={idx}
              className="flex items-start gap-2.5 my-1 text-[12.5px] sm:text-[13px] text-ink-2 leading-[1.68]"
            >
              <span className="mt-2 w-1.5 h-1.5 rounded-full bg-accent shrink-0" />
              <div className="min-w-0 flex-1">
                <Rich text={cleanText} />
              </div>
            </div>
          );
        }

        // Check if paragraph contains semicolon-separated bold points (e.g. "...; **Title**: desc")
        if (line.includes('; **') || line.includes(': **')) {
          const parts = line.split(/(?<=[;:])\s+(?=\*\*)/g);
          if (parts.length > 1) {
            return (
              <div key={idx} className="flex flex-col gap-1 my-1">
                {parts.map((p, pIdx) => {
                  const cleanP = p.replace(/^;\s*/, '').trim();
                  if (pIdx === 0 && !cleanP.startsWith('**')) {
                    return (
                      <p key={pIdx} className="m-0 text-[12.5px] sm:text-[13px] text-ink-2 leading-[1.72] font-normal mb-1">
                        <Rich text={cleanP} />
                      </p>
                    );
                  }
                  return (
                    <div key={pIdx} className="flex items-start gap-2.5 my-1 text-[12.5px] sm:text-[13px] text-ink-2 leading-[1.68]">
                      <span className="mt-2 w-1.5 h-1.5 rounded-full bg-accent shrink-0" />
                      <div className="min-w-0 flex-1">
                        <Rich text={cleanP} />
                      </div>
                    </div>
                  );
                })}
              </div>
            );
          }
        }

        // Check if a long continuous paragraph has multiple distinct sentences (> 120 chars)
        if (line.length > 120) {
          const sentences = line.split(/(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9\*\*])/g);
          if (sentences.length > 1) {
            return (
              <div key={idx} className="flex flex-col gap-1 my-1">
                <p className="m-0 text-[12.5px] sm:text-[13px] text-ink-2 leading-[1.72] font-normal mb-1">
                  <Rich text={sentences[0]} />
                </p>
                {sentences.slice(1).map((s, sIdx) => (
                  <div key={sIdx} className="flex items-start gap-2.5 my-1 text-[12.5px] sm:text-[13px] text-ink-2 leading-[1.68]">
                    <span className="mt-2 w-1.5 h-1.5 rounded-full bg-accent shrink-0" />
                    <div className="min-w-0 flex-1">
                      <Rich text={s} />
                    </div>
                  </div>
                ))}
              </div>
            );
          }
        }

        // Regular narrative paragraph
        return (
          <p
            key={idx}
            className="m-0 text-[12.5px] sm:text-[13px] text-ink-2 leading-[1.72] font-normal my-1"
          >
            <Rich text={line} />
          </p>
        );
      })}
    </div>
  );
};

/** Soft badge palette keyed by the colour names used in the data. */
const TONE: Record<string, { bg: string; fg: string }> = {
  sky: { bg: '#E6F3FB', fg: '#0B5C86' },
  blue: { bg: '#E8EEFD', fg: '#1E4FD8' },
  indigo: { bg: '#ECEBFD', fg: '#4338CA' },
  violet: { bg: '#F1EBFD', fg: '#6D28D9' },
  rose: { bg: '#FDECEF', fg: '#B4233C' },
  red: { bg: '#FDECEC', fg: '#B42318' },
  amber: { bg: '#FDF2E1', fg: '#9A4D06' },
  orange: { bg: '#FDEFE3', fg: '#A64B0A' },
  emerald: { bg: '#E4F3E9', fg: '#157A3E' },
  green: { bg: '#E4F3E9', fg: '#157A3E' },
  teal: { bg: '#E0F4F1', fg: '#0F6E63' },
  slate: { bg: '#EEF1F4', fg: '#4A5868' },
};
const tone = (c?: string) => TONE[(c || '').toLowerCase()] || TONE.blue;

const EMPHASIS: Record<ProfessorAudioHighlight['emphasisType'], { label: string; icon: React.ElementType; c: string }> = {
  direct_exam_warning: { label: 'Sınavda sorulur', icon: AlertTriangle, c: 'rose' },
  slide_missing: { label: 'Slaytta yok', icon: EyeOff, c: 'amber' },
  pearl: { label: 'Spot bilgi', icon: Lightbulb, c: 'blue' },
  clinical_tip: { label: 'Klinik ipucu', icon: Stethoscope, c: 'emerald' },
};

const isTyping = (t: EventTarget | null) => {
  const el = t as HTMLElement | null;
  return !!el && (['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName) || el.isContentEditable);
};

// ---------------------------------------------------------------------------
// 3D Flip Flashcard Component (Akıl Kartı)
// ---------------------------------------------------------------------------
export const FlashcardComponent: React.FC<{ card: SlideFlashcard }> = ({ card }) => {
  const [isFlipped, setIsFlipped] = useState(false);
  const [showHint, setShowHint] = useState(false);

  const frontText = card.front || card.question || '';
  const backText = card.back || card.answer || '';

  return (
    <div
      className="w-full cursor-pointer group"
      style={{ perspective: '1200px' }}
      onClick={() => setIsFlipped((v) => !v)}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          setIsFlipped((v) => !v);
        }
      }}
      tabIndex={0}
      role="button"
      aria-pressed={isFlipped}
      aria-label={`${frontText || 'Akıl Kartı'} akıl kartı`}
    >
      <div
        className="w-full grid rounded-2xl transition-all duration-500 ease-out shadow-xs hover:shadow-md min-h-[160px]"
        style={{
          transformStyle: 'preserve-3d',
          transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
        }}
      >
        {/* FRONT FACE */}
        <div
          className={`[grid-area:1/1] min-w-0 select-none rounded-2xl border p-4 sm:p-5 flex flex-col justify-between bg-gradient-to-br from-white via-white to-amber-50/20 shadow-xs hover:border-accent/40 transition-colors ${
            isFlipped ? 'pointer-events-none' : ''
          }`}
          style={{
            backfaceVisibility: 'hidden',
            borderColor: 'var(--color-line)',
          }}
        >
          <div className="flex items-start justify-between gap-2 shrink-0">
            <span className="min-w-0 min-h-6 px-2 py-1 rounded-lg text-[11.5px] leading-tight font-semibold bg-amber-100 text-amber-900 uppercase tracking-[0.04em] inline-flex items-start gap-1.5 border border-amber-200/80 break-words">
              <BrainCircuit className="w-3.5 h-3.5 shrink-0 text-amber-700" />
              <span className="min-w-0">{card.category || 'Akıl Kartı'}</span>
            </span>
            <span aria-hidden="true" className="shrink-0 w-8 h-8 -mt-1 -mr-1 rounded-full flex items-center justify-center bg-canvas text-accent">
              <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
            </span>
          </div>

          <div className="my-2 flex-1 flex flex-col justify-center">
            <h4 className="m-0 text-[13.5px] sm:text-[14.5px] font-semibold text-ink leading-snug tracking-[-0.01em] break-words">
              {frontText}
            </h4>
            {card.hint && (
              <div className="mt-2.5">
                {showHint ? (
                  <p className="m-0 text-[12px] text-amber-950 bg-amber-50 border border-amber-200 rounded-xl p-2.5 leading-relaxed shadow-2xs">
                    💡 <strong>İpucu:</strong> {card.hint}
                  </p>
                ) : (
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      setShowHint(true);
                    }}
                    className="text-[11.5px] font-semibold text-accent hover:text-accent-hover hover:underline cursor-pointer inline-flex items-center gap-1"
                  >
                    <span>💡 İpucunu Göster</span>
                  </button>
                )}
              </div>
            )}
          </div>

        </div>

        {/* BACK FACE */}
        <div
          className={`[grid-area:1/1] min-w-0 rounded-2xl border p-4 sm:p-5 flex flex-col justify-between bg-gradient-to-br from-emerald-50/95 via-teal-50/30 to-white border-emerald-300 shadow-sm ${
            !isFlipped ? 'pointer-events-none' : ''
          }`}
          style={{
            backfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)',
          }}
        >
          <div className="flex items-start justify-between gap-2 shrink-0 select-none">
            <span className="min-w-0 min-h-6 px-2 py-1 rounded-lg text-[11px] leading-tight font-semibold bg-emerald-100 text-emerald-900 uppercase tracking-[0.04em] inline-flex items-start gap-1.5 border border-emerald-300/80">
              <CheckCircle2 className="w-3.5 h-3.5 shrink-0 text-emerald-700" />
              <span className="min-w-0">Cevap</span>
            </span>
            <span aria-hidden="true" className="shrink-0 w-8 h-8 -mt-1 -mr-1 rounded-full flex items-center justify-center bg-white/80 text-emerald-700 border border-emerald-200">
              <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
            </span>
          </div>

          <div className="my-2 flex-1 text-[12.5px] sm:text-[13px] font-medium text-ink leading-relaxed whitespace-pre-line break-words select-text">
            <Rich text={backText} />
          </div>
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Hub (deck catalogue)
// ---------------------------------------------------------------------------

/**
 * Deck data spells the same branch several ways ("Enfeksiyon Hastalıkları / Klinik Mikrobiyoloji",
 * "… ve Klinik Mikrobiyoloji", "Üroloji / Nefroloji"). The catalogue groups by the primary branch.
 */
export const disciplineGroup = (raw: string) => {
  const first = (raw || 'Diğer').split(/\s*(?:\/|&|,|\sve\s)\s*/)[0].trim();
  return first || 'Diğer';
};

const GROUP_DOTS: Record<string, string> = {
  'Tıbbi Patoloji': '#E0566E',
  'Enfeksiyon Hastalıkları': '#1F9D55',
  'Halk Sağlığı': '#2B8BC6',
  'Tıbbi Genetik': '#6D5BD0',
  Üroloji: '#E0952B',
};
const FALLBACK_DOTS = ['#0F7A5F', '#B4233C', '#4A5868', '#9A4D06', '#1E4FD8'];
const groupDot = (g: string) =>
  GROUP_DOTS[g] || FALLBACK_DOTS[[...g].reduce((n, ch) => n + ch.charCodeAt(0), 0) % FALLBACK_DOTS.length];

/** Horizontally scrolling chip row: wheel scrolls sideways, arrow buttons appear when it overflows. */
const ScrollRow: React.FC<{ label: string; children: React.ReactNode }> = ({ label, children }) => {
  const ref = useRef<HTMLDivElement>(null);
  const [edges, setEdges] = useState({ left: false, right: false });

  const update = useCallback(() => {
    const el = ref.current;
    if (!el) return;
    setEdges({ left: el.scrollLeft > 4, right: el.scrollLeft + el.clientWidth < el.scrollWidth - 4 });
  }, []);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    update();
    const ro = new ResizeObserver(update);
    ro.observe(el);
    const onWheel = (e: WheelEvent) => {
      if (el.scrollWidth <= el.clientWidth || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
      e.preventDefault();
      el.scrollLeft += e.deltaY;
    };
    el.addEventListener('wheel', onWheel, { passive: false });
    return () => {
      ro.disconnect();
      el.removeEventListener('wheel', onWheel);
    };
  }, [update]);

  const nudge = (dir: 1 | -1) => ref.current?.scrollBy({ left: dir * Math.max(200, (ref.current.clientWidth || 400) * 0.7), behavior: 'smooth' });
  const arrow = 'absolute top-1/2 -translate-y-1/2 z-10 w-9 h-9 rounded-full bg-white border border-line shadow-[0_2px_8px_rgba(14,26,38,0.12)] hidden sm:flex items-center justify-center text-ink cursor-pointer hover:border-line-2';

  return (
    <div className="relative -mx-3 sm:mx-0">
      {edges.left && (
        <>
          <span className="pointer-events-none absolute left-0 top-0 bottom-0 w-12 bg-gradient-to-r from-canvas to-transparent z-[5]" aria-hidden="true" />
          <button type="button" onClick={() => nudge(-1)} aria-label="Sola kaydır" className={`${arrow} left-0`}>
            <ChevronLeft className="w-4 h-4" />
          </button>
        </>
      )}
      <div ref={ref} onScroll={update} role="radiogroup" aria-label={label} className="flex gap-1.5 overflow-x-auto no-scrollbar px-3 sm:px-0 scroll-smooth">
        {children}
      </div>
      {edges.right && (
        <>
          <span className="pointer-events-none absolute right-0 top-0 bottom-0 w-12 bg-gradient-to-l from-canvas to-transparent z-[5]" aria-hidden="true" />
          <button type="button" onClick={() => nudge(1)} aria-label="Sağa kaydır" className={`${arrow} right-0`}>
            <ChevronRight className="w-4 h-4" />
          </button>
        </>
      )}
    </div>
  );
};

export const InteractiveDeckView: React.FC<InteractiveDeckViewProps> = ({ initialDeckId, initialSlideNumber, onDeckChange, onOpenPdfModal }) => {
  const allDecks = useMemo(
    () => ((interactiveDecksData as unknown as InteractiveDeck[]) || []).filter((d) => d && Array.isArray(d.slides) && d.slides.length > 0),
    []
  );
  const [deckId, setDeckId] = useState<string | null>(initialDeckId || null);
  const [playerViewMode, setPlayerViewMode] = useState<DeckViewMode>('interactive');

  useEffect(() => {
    if (initialDeckId) {
      setDeckId(initialDeckId);
    }
  }, [initialDeckId]);

  const [query, setQuery] = useState('');
  const [discipline, setDiscipline] = useState('all');
  const [progress, setProgress] = useState<DeckProgress>(readProgress);

  const disciplines = useMemo(() => {
    const m: Record<string, number> = {};
    allDecks.forEach((d) => {
      const g = disciplineGroup(d.discipline);
      m[g] = (m[g] || 0) + 1;
    });
    // Biggest groups first, then alphabetical
    return Object.entries(m).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'tr'));
  }, [allDecks]);

  const visible = useMemo(() => {
    const q = query.trim().toLocaleLowerCase('tr-TR');
    return allDecks.filter((d) => {
      if (discipline !== 'all' && disciplineGroup(d.discipline) !== discipline) return false;
      if (!q) return true;
      return [d.title, d.discipline, d.instructor, d.overview, ...(d.highYieldPearls || [])].join(' ').toLocaleLowerCase('tr-TR').includes(q);
    });
  }, [allDecks, discipline, query]);

  const activeDeck = allDecks.find((d) => d.id === deckId) || null;
  const totalSlides = allDecks.reduce((n, d) => n + d.slides.length, 0);

  return (
    <div className="flex flex-col gap-3 sm:gap-4 min-w-0">
      <div className="flex flex-col md:flex-row md:items-end gap-3">
        <div className="min-w-0 flex-1">
          <h1 className="m-0 font-display font-bold text-[28px] sm:text-[30px] leading-[1.1] tracking-[-0.03em]">Öğren</h1>
          <p className="m-0 mt-1 text-[14px] text-ink-3">
            {allDecks.length} ders · {totalSlides} slayt · hocanın vurguları ve çıkmış sorularla
          </p>
        </div>
        <label className="flex items-center gap-2 h-11 md:h-10 md:w-[300px] px-3 border border-line rounded-[12px] bg-white focus-within:border-accent">
          <Search className="w-4 h-4 text-ink-3 shrink-0" />
          <span className="sr-only">Derslerde ara</span>
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ders ya da konu ara"
            className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[16px] md:text-[14px] placeholder:text-[#7A8693]"
          />
        </label>
      </div>

      <ScrollRow label="Ders">
        {[['all', allDecks.length] as [string, number], ...disciplines].map(([d, n]) => {
          const on = discipline === d;
          const dot = d === 'all' ? '#0E1A26' : groupDot(d);
          return (
            <button
              key={d}
              type="button"
              role="radio"
              aria-checked={on}
              onClick={() => setDiscipline(d)}
              className={`shrink-0 h-9 px-3.5 rounded-full text-[13.5px] whitespace-nowrap cursor-pointer inline-flex items-center gap-1.5 transition-colors ${
                on ? 'bg-ink text-white font-semibold' : 'bg-white border border-line text-ink hover:border-line-2'
              }`}
            >
              <span className="w-2 h-2 rounded-full shrink-0" style={{ background: on && d === 'all' ? '#fff' : dot }} aria-hidden="true" />
              {d === 'all' ? 'Tümü' : d}
              <span className={`font-mono text-[12px] ${on ? 'text-white/70' : 'text-ink-3'}`}>{n}</span>
            </button>
          );
        })}
      </ScrollRow>

      {visible.length === 0 ? (
        <div className="bg-white border border-line rounded-[16px] px-6 py-12 text-center">
          <p className="m-0 font-display text-[20px] font-bold">Bu aramada ders yok</p>
          <p className="m-0 mt-1 text-[14px] text-ink-2">Aramayı temizleyip başka bir ders seçebilirsin.</p>
        </div>
      ) : (
        <ul className="list-none m-0 p-0 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-2.5 sm:gap-3">
          {visible.map((d) => {
            const pr = progress[d.id];
            const seen = pr?.seen?.length || 0;
            const pct = Math.round((seen / d.slides.length) * 100);
            const qCount = d.slides.reduce((n, s) => n + (s.relatedQuestions?.length || 0), 0);
            const cardCount = d.slides.reduce((n, s) => n + (s.flashcards?.length || 0), 0);
            const started = seen > 0;
            const done = seen >= d.slides.length;
            const group = disciplineGroup(d.discipline);
            return (
              <li key={d.id} className="min-w-0">
                <button
                  type="button"
                  onClick={() => {
                    setPlayerViewMode('interactive');
                    setDeckId(d.id);
                    onDeckChange?.(d.id);
                  }}
                  className="w-full h-full text-left bg-white border border-line rounded-[16px] p-4 flex flex-col gap-2.5 cursor-pointer hover:border-accent hover:shadow-[0_6px_20px_rgba(14,26,38,0.06)] transition-all group"
                >
                  <span className="flex items-center gap-2 min-w-0 text-[12.5px] text-ink-3">
                    <span className="w-2 h-2 rounded-full shrink-0" style={{ background: groupDot(group) }} aria-hidden="true" />
                    <span className="truncate" title={d.discipline}>{group}</span>
                    <span className="shrink-0 ml-auto font-mono text-[12px]">{d.slides.length} slayt</span>
                  </span>
                  <span className="text-[16.5px] font-semibold leading-snug text-ink group-hover:text-accent line-clamp-2 min-h-[2.6em]">{d.title}</span>
                  <span className="flex flex-wrap gap-1.5">
                    {d.instructor && (
                      <span className="max-w-full h-6 px-2 rounded-[7px] bg-canvas text-[12px] text-ink-2 inline-flex items-center gap-1 min-w-0">
                        <User className="w-3 h-3 shrink-0" />
                        <span className="truncate">{d.instructor}</span>
                      </span>
                    )}
                    {cardCount > 0 && (
                      <span className="h-6 px-2 rounded-[7px] bg-[#FDF2E1] text-[12px] text-[#9A4D06] inline-flex items-center">{cardCount} kart</span>
                    )}
                    {qCount > 0 && (
                      <span className="h-6 px-2 rounded-[7px] bg-accent-soft text-[12px] text-accent inline-flex items-center">{qCount} soru</span>
                    )}
                  </span>
                  <span className="mt-auto pt-2.5 border-t border-line-soft flex items-center gap-3">
                    <span className="flex-1 min-w-0 flex flex-col gap-1">
                      <span className="text-[12px] text-ink-3">
                        {done ? 'Tamamlandı' : started ? `${(pr?.last ?? 0) + 1} / ${d.slides.length} slayt` : 'Başlanmadı'}
                      </span>
                      <span className="h-[5px] rounded-full bg-line-soft overflow-hidden" aria-hidden="true">
                        <span className="block h-full bg-accent rounded-full" style={{ width: `${pct}%` }} />
                      </span>
                    </span>
                    <span className="flex items-center gap-1.5 shrink-0">
                      <span
                        onClick={(e) => {
                          e.stopPropagation();
                          setPlayerViewMode('pdf');
                          setDeckId(d.id);
                          onDeckChange?.(d.id);
                        }}
                        title="Orijinal PDF Slaytını Aç"
                        className="h-[34px] px-2.5 rounded-[10px] inline-flex items-center gap-1 text-[12px] font-semibold text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200 transition-colors"
                      >
                        <FileText className="w-3.5 h-3.5" />
                        <span>PDF</span>
                      </span>
                      <span
                        className={`h-[34px] px-3 rounded-[10px] inline-flex items-center gap-1.5 text-[13px] font-semibold ${
                          started ? 'bg-accent text-white' : 'bg-accent-soft text-accent'
                        }`}
                      >
                        <Play className="w-3 h-3 fill-current" />
                        {done ? 'Tekrar' : started ? 'Devam et' : 'Başla'}
                      </span>
                    </span>
                  </span>
                </button>
              </li>
            );
          })}
        </ul>
      )}

      {activeDeck && (
        <DeckPlayer
          deck={activeDeck}
          initialViewMode={playerViewMode}
          startAt={initialSlideNumber != null && initialSlideNumber > 0 ? initialSlideNumber - 1 : (progress[activeDeck.id]?.last ?? 0)}
          onProgress={(index) => {
            setProgress((prev) => {
              const cur = prev[activeDeck.id] || { last: 0, seen: [] };
              const seen = cur.seen.includes(index) ? cur.seen : [...cur.seen, index];
              const next = { ...prev, [activeDeck.id]: { last: index, seen } };
              writeProgress(next);
              return next;
            });
          }}
          onClose={() => {
            setDeckId(null);
            onDeckChange?.(null);
          }}
          onExportPdf={onOpenPdfModal ? (slideNumber) => onOpenPdfModal({ deckId: activeDeck.id, slideNumber }) : undefined}
        />
      )}
      </div>
  );
};

// ---------------------------------------------------------------------------
// Player: full-viewport overlay, paged or scrolling, optional native fullscreen
// ---------------------------------------------------------------------------
export type DeckViewMode = 'interactive' | 'pdf' | 'split';
type PanelTab = 'flashcards' | 'questions' | 'notes' | 'pearls' | 'ai' | 'pdf';

const DeckPlayer: React.FC<{
  deck: InteractiveDeck;
  startAt: number;
  initialViewMode?: DeckViewMode;
  onProgress: (index: number) => void;
  onClose: () => void;
  onExportPdf?: (slideNumber: number) => void;
}> = ({ deck, startAt, initialViewMode = 'interactive', onProgress, onClose, onExportPdf }) => {
  const slides = deck.slides;
  const n = slides.length;
  const [index, setIndex] = useState(() => Math.min(Math.max(0, startAt), n - 1));
  const [viewMode, setViewMode] = useState<DeckViewMode>(initialViewMode);
  const [mode, setMode] = useState<'paged' | 'scroll'>(() => {
    try {
      return localStorage.getItem('medsoru_learn_mode') === 'scroll' ? 'scroll' : 'paged';
    } catch {
      return 'paged';
    }
  });
  const [panelOpen, setPanelOpen] = useState(() => typeof window !== 'undefined' && window.innerWidth >= 1100);
  const [tab, setTab] = useState<PanelTab>('flashcards');
  const [isFs, setIsFs] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const { setIsDrawerOpen, glossaryList, setCurrentSlideText } = useGlossary();
  const rootRef = useRef<HTMLDivElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const sectionRefs = useRef<(HTMLElement | null)[]>([]);
  const stripRef = useRef<HTMLDivElement>(null);
  const programmatic = useRef(false);
  const touch = useRef<{ x: number; y: number } | null>(null);

  const slide = slides[index];

  // Keep active slide text in sync with glossary provider for dynamic slide knowledge
  useEffect(() => {
    if (!slide || !setCurrentSlideText) return;
    const narrativeText = slide.synthesisNarrative || (slide as any).content || '';
    const spotsList = (slide.spotPearls && slide.spotPearls.length > 0) ? slide.spotPearls : ((slide as any).spots || []);
    const slideText = [
      slide.title,
      slide.subtitle,
      slide.professorAudioHighlight?.quote,
      slide.professorAudioHighlight?.note,
      narrativeText,
      ...(slide.coreContent?.keyBullets || []).map((b) => `${b.title}: ${b.desc}`),
      ...spotsList.map((p: any) => typeof p === 'string' ? p : `${p?.badge ? p.badge + ' ' : ''}${p?.text || ''}`),
      slide.coreContent?.table?.title,
      slide.coreContent?.table?.rows?.map((r) => r.join(' ')).join('\n'),
    ]
      .filter(Boolean)
      .join('\n');
    setCurrentSlideText(slideText);
  }, [slide, setCurrentSlideText]);

  // Lock page scroll and focus the player while open
  useEffect(() => {
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    rootRef.current?.focus();
    return () => {
      document.body.style.overflow = prev;
      if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    };
  }, []);

  useEffect(() => onProgress(index), [index]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    try {
      localStorage.setItem('medsoru_learn_mode', mode);
    } catch {
      /* ignore */
    }
  }, [mode]);

  // Native fullscreen on top of the overlay (the overlay already fills the viewport)
  useEffect(() => {
    const onFs = () => setIsFs(document.fullscreenElement === rootRef.current);
    document.addEventListener('fullscreenchange', onFs);
    return () => document.removeEventListener('fullscreenchange', onFs);
  }, []);
  const canFullscreen = typeof document !== 'undefined' && !!document.fullscreenEnabled;
  const toggleFullscreen = () => {
    if (!rootRef.current) return;
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    else rootRef.current.requestFullscreen?.().catch(() => {});
  };

  const goTo = useCallback(
    (i: number) => {
      const t = Math.max(0, Math.min(n - 1, i));
      setIndex(t);
      if (mode === 'scroll') {
        programmatic.current = true;
        sectionRefs.current[t]?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        window.setTimeout(() => (programmatic.current = false), 600);
      }
    },
    [mode, n]
  );

  const next = () => {
    if (index < n - 1) goTo(index + 1);
  };
  const prev = () => {
    if (index > 0) goTo(index - 1);
  };
  const atStart = index === 0;
  const atEnd = index >= n - 1;

  // Keep the current slide in view when switching to scroll mode
  useEffect(() => {
    if (mode === 'scroll') {
      requestAnimationFrame(() => sectionRefs.current[index]?.scrollIntoView({ block: 'start' }));
    }
  }, [mode]); // eslint-disable-line react-hooks/exhaustive-deps

  // Scroll mode: slides flow at their natural height; the current one is the
  // section crossing the upper third of the stage.
  useEffect(() => {
    const sc = scrollRef.current;
    if (mode !== 'scroll' || !sc) return;
    const onScroll = () => {
      if (programmatic.current) return;
      const probe = sc.scrollTop + sc.clientHeight * 0.35;
      let i = 0;
      sectionRefs.current.forEach((el, k) => {
        if (el && el.offsetTop <= probe) i = k;
      });
      setIndex((prev) => (prev === i ? prev : i));
    };
    sc.addEventListener('scroll', onScroll, { passive: true });
    return () => sc.removeEventListener('scroll', onScroll);
  }, [mode, n]);

  // Thumbnail strip follows the current slide
  useEffect(() => {
    const el = stripRef.current?.querySelector<HTMLElement>(`[data-thumb="${index}"]`);
    el?.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
  }, [index]);

  // Keyboard
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (isTyping(e.target)) return;
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setSearchOpen((v) => !v);
        return;
      }
      if (e.key === '/' && !searchOpen) {
        e.preventDefault();
        setSearchOpen(true);
        return;
      }
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (['ArrowRight', 'PageDown', ' '].includes(e.key) || (mode === 'paged' && e.key === 'ArrowDown')) {
        e.preventDefault();
        next();
      } else if (['ArrowLeft', 'PageUp'].includes(e.key) || (mode === 'paged' && e.key === 'ArrowUp')) {
        e.preventDefault();
        prev();
      } else if (e.key === 'Home') goTo(0);
      else if (e.key === 'End') goTo(n - 1);
      else if (e.key.toLowerCase() === 'f' && canFullscreen) toggleFullscreen();
      else if (e.key === 'Escape') {
        if (searchOpen) setSearchOpen(false);
        else if (!document.fullscreenElement) onClose();
      }
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  });

  // Swipe (paged mode)
  const onTouchStart = (e: React.TouchEvent) => {
    const t = e.touches[0];
    touch.current = { x: t.clientX, y: t.clientY };
  };
  const onTouchEnd = (e: React.TouchEvent) => {
    // Selecting text with the highlighter must not flip the slide
    if (!touch.current || mode !== 'paged' || isPenActive()) return;
    const t = e.changedTouches[0];
    const dx = t.clientX - touch.current.x;
    const dy = t.clientY - touch.current.y;
    touch.current = null;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) (dx < 0 ? next : prev)();
  };

  const iconBtn =
    'w-10 h-10 shrink-0 rounded-[10px] flex items-center justify-center text-ink-2 hover:text-ink hover:bg-canvas cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed';

  return (
    <div
      ref={rootRef}
      tabIndex={-1}
      role="dialog"
      aria-modal="true"
      aria-label={`${deck.title} sunumu`}
      className="fixed inset-0 z-[60] h-[100dvh] w-screen bg-canvas text-ink flex flex-col outline-none"
    >
      {/* Top bar */}
      <header className="shrink-0 h-14 bg-white border-b border-line px-2 sm:px-3 flex items-center gap-1.5 sm:gap-2">
        <button type="button" onClick={onClose} aria-label="Sunumu kapat" title="Kapat (Esc)" className={iconBtn}>
          <X className="w-5 h-5" />
        </button>
        <div className="min-w-0 flex-1">
          <div className="text-[12px] text-ink-2 truncate">
            {deck.discipline}
            {deck.instructor ? ` · ${deck.instructor}` : ''}
          </div>
          <div className="text-[15px] font-semibold truncate">{deck.shortTitle || deck.title}</div>
        </div>

        {/* Global topic search trigger */}
        <button
          type="button"
          onClick={() => setSearchOpen(true)}
          title="Ders İçinde Konu, Soru ve Spot Ara (Ctrl+K veya /)"
          className="h-9 px-2.5 rounded-[10px] bg-canvas hover:bg-white border border-line text-ink-2 hover:text-ink text-[13px] font-medium inline-flex items-center gap-1.5 cursor-pointer shrink-0 transition-colors"
        >
          <Search className="w-4 h-4 text-accent" />
          <span className="hidden md:inline">Ders İçi Arama</span>
          <kbd className="hidden lg:inline text-[10px] font-mono text-ink-3 bg-white px-1.5 py-0.5 rounded border border-line">Ctrl+K</kbd>
        </button>

        {/* Medical Glossary Dictionary trigger */}
        <button
          type="button"
          onClick={() => setIsDrawerOpen(true)}
          title="Tıbbi Terimler Sözlüğü (Latin İsimler, Bakteri, Virüs ve İlaçlar)"
          className="h-9 px-2.5 rounded-[10px] bg-canvas hover:bg-white border border-line text-ink-2 hover:text-teal-700 dark:hover:text-teal-400 text-[13px] font-medium inline-flex items-center gap-1.5 cursor-pointer shrink-0 transition-colors"
        >
          <BookOpen className="w-4 h-4 text-teal-600 dark:text-teal-400" />
          <span className="hidden md:inline">Tıbbi Sözlük</span>
          <span className="text-[10.5px] font-bold bg-teal-500/10 text-teal-700 dark:text-teal-300 px-1.5 py-0.5 rounded-full border border-teal-500/20">
            {glossaryList.length}
          </span>
        </button>

        <span className="hidden sm:inline font-mono text-[13px] text-ink-2 px-1" aria-live="polite">
          {index + 1} / {n}
        </span>

        {/* View Mode Switcher: Interactive / Split / PDF */}
        <div role="radiogroup" aria-label="Çalışma Modu" className="flex items-center h-9 bg-canvas rounded-[10px] p-0.5 border border-line/60">
          <button
            type="button"
            role="radio"
            aria-checked={viewMode === 'interactive'}
            aria-label="Etkileşimli Slaytlar"
            title="Etkileşimli Slaytlar"
            onClick={() => setViewMode('interactive')}
            className={`h-8 px-2 sm:px-2.5 rounded-lg inline-flex items-center gap-1.5 text-[12px] sm:text-[13px] cursor-pointer transition-colors ${
              viewMode === 'interactive'
                ? 'bg-white text-accent font-semibold shadow-[0_1px_2px_rgba(14,26,38,0.1)]'
                : 'text-ink-2 hover:text-ink'
            }`}
          >
            <GalleryHorizontal className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-accent" />
            <span className="hidden md:inline">Slaytlar</span>
          </button>

          <button
            type="button"
            role="radio"
            aria-checked={viewMode === 'split'}
            aria-label="Yan Yana (Slayt + Orijinal PDF)"
            title="Yan Yana: Sol tarafta slayt, sağ tarafta hoca PDF'i"
            onClick={() => setViewMode('split')}
            className={`h-8 px-2 sm:px-2.5 rounded-lg inline-flex items-center gap-1.5 text-[12px] sm:text-[13px] cursor-pointer transition-colors ${
              viewMode === 'split'
                ? 'bg-white text-indigo-600 dark:text-indigo-400 font-semibold shadow-[0_1px_2px_rgba(14,26,38,0.1)]'
                : 'text-ink-2 hover:text-ink'
            }`}
          >
            <Columns className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-indigo-600 dark:text-indigo-400" />
            <span className="hidden md:inline">Yan Yana</span>
          </button>

          <button
            type="button"
            role="radio"
            aria-checked={viewMode === 'pdf'}
            aria-label="Orijinal Ders PDF'i"
            title="Hocanın orijinal ders sunumu PDF'i"
            onClick={() => setViewMode('pdf')}
            className={`h-8 px-2 sm:px-2.5 rounded-lg inline-flex items-center gap-1.5 text-[12px] sm:text-[13px] cursor-pointer transition-colors ${
              viewMode === 'pdf'
                ? 'bg-white text-rose-600 dark:text-rose-400 font-semibold shadow-[0_1px_2px_rgba(14,26,38,0.1)]'
                : 'text-ink-2 hover:text-ink'
            }`}
          >
            <FileText className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-rose-500" />
            <span className="hidden md:inline">Orijinal PDF</span>
          </button>
        </div>

        {viewMode === 'interactive' && (
          <div role="radiogroup" aria-label="Görünüm" className="hidden xl:flex items-center h-9 bg-canvas rounded-[10px] p-0.5">
            {(
              [
                ['paged', GalleryHorizontal, 'Sayfa sayfa'],
                ['scroll', Rows3, 'Kaydırarak'],
              ] as const
            ).map(([id, Icon, label]) => (
              <button
                key={id}
                type="button"
                role="radio"
                aria-checked={mode === id}
                aria-label={label}
                title={label}
                onClick={() => setMode(id)}
                className={`h-8 px-2 rounded-lg inline-flex items-center gap-1.5 text-[12px] cursor-pointer ${
                  mode === id ? 'bg-white text-accent font-semibold shadow-[0_1px_2px_rgba(14,26,38,0.1)]' : 'text-ink-2 hover:text-ink'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{label}</span>
              </button>
            ))}
          </div>
        )}

        {viewMode !== 'pdf' && (
          <>
            <HighlighterToolbar />
            <DrawingModeToolbarTrigger />
          </>
        )}
        {onExportPdf && (
          <button
            type="button"
            onClick={() => {
              if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {});
              onExportPdf(slides[index].slideNumber);
            }}
            aria-label="Bu slaytı PDF olarak indir"
            title="Bu slaytı PDF yap"
            className={iconBtn}
          >
            <FileDown className="w-5 h-5" />
          </button>
        )}
        <button
          type="button"
          onClick={() => setPanelOpen((v) => !v)}
          aria-pressed={panelOpen}
          aria-label="Etkileşim panelini aç/kapat"
          title="Akıl kartları, çıkmış sorular, ders notu ve AI"
          className={`${iconBtn} ${panelOpen ? 'bg-accent-soft text-accent' : ''}`}
        >
          {panelOpen ? <PanelRightClose className="w-5 h-5" /> : <PanelRightOpen className="w-5 h-5" />}
        </button>
        {canFullscreen && (
          <button type="button" onClick={toggleFullscreen} aria-label={isFs ? 'Tam ekrandan çık' : 'Tam ekran'} title="Tam ekran (F)" className={iconBtn}>
            {isFs ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
          </button>
        )}
      </header>
      <div className="shrink-0 h-[3px] bg-line-soft" aria-hidden="true">
        <div className="h-full bg-accent transition-[width] duration-300" style={{ width: `${((index + 1) / n) * 100}%` }} />
      </div>

      {/* Stage + panel */}
      <div className={`flex-1 min-h-0 grid grid-cols-1 ${panelOpen ? 'lg:grid-cols-[minmax(0,1fr)_420px]' : ''}`}>
        <div className="min-h-0 min-w-0 relative">
          {viewMode === 'pdf' ? (
            <div className="absolute inset-0 p-2 sm:p-4 flex flex-col">
              <DeckPdfViewer
                deck={deck}
                currentSlideNumber={slide.slideNumber}
                onToggleSplitView={() => setViewMode('split')}
              />
            </div>
          ) : viewMode === 'split' ? (
            <div className="absolute inset-0 p-2 sm:p-3 grid grid-cols-1 lg:grid-cols-2 gap-2 sm:gap-3">
              <div
                className="min-h-0 h-full flex flex-col rounded-[16px] overflow-hidden border border-line bg-white/50 backdrop-blur-sm relative shadow-sm"
                onTouchStart={onTouchStart}
                onTouchEnd={onTouchEnd}
              >
                <SlideCanvas
                  key={`split-${index}`}
                  slide={slide}
                  highlightScope={`deck:${deck.id}:${slide.slideNumber}`}
                  index={index}
                  total={n}
                  paged
                  onNext={next}
                  onPrev={prev}
                  onOpenQuestions={() => {
                    setTab('questions');
                    setPanelOpen(true);
                  }}
                  onOpenFlashcards={() => {
                    setTab('flashcards');
                    setPanelOpen(true);
                  }}
                  onOpenNotes={() => {
                    setTab('notes');
                    setPanelOpen(true);
                  }}
                />
              </div>
              <div className="min-h-0 h-full flex flex-col rounded-[16px] overflow-hidden border border-line bg-white shadow-sm">
                <DeckPdfViewer
                  deck={deck}
                  currentSlideNumber={slide.slideNumber}
                  isSplitView
                  onToggleSplitView={() => setViewMode('interactive')}
                />
              </div>
            </div>
          ) : mode === 'paged' ? (
            <div className="absolute inset-0 p-2 sm:p-4 lg:p-6 flex" onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
              <SlideCanvas
                key={index}
                slide={slide}
                highlightScope={`deck:${deck.id}:${slide.slideNumber}`}
                index={index}
                total={n}
                paged
                onNext={next}
                onPrev={prev}
                onOpenQuestions={() => {
                  setTab('questions');
                  setPanelOpen(true);
                }}
                onOpenFlashcards={() => {
                  setTab('flashcards');
                  setPanelOpen(true);
                }}
                onOpenNotes={() => {
                  setTab('notes');
                  setPanelOpen(true);
                }}
              />
            </div>
          ) : (
            <div ref={scrollRef} className="absolute inset-0 overflow-y-auto snap-y snap-proximity overscroll-contain" aria-label="Slaytlar">
              {slides.map((s, i) => (
                <section
                  key={i}
                  data-index={i}
                  ref={(el) => {
                    sectionRefs.current[i] = el;
                  }}
                  aria-label={`Slayt ${i + 1}`}
                  className="min-h-full snap-start p-2 sm:p-4 lg:p-6 flex"
                >
                  <SlideCanvas
                    slide={s}
                    highlightScope={`deck:${deck.id}:${s.slideNumber}`}
                    index={i}
                    total={n}
                    onOpenQuestions={() => {
                      setTab('questions');
                      setPanelOpen(true);
                    }}
                    onOpenFlashcards={() => {
                      setTab('flashcards');
                      setPanelOpen(true);
                    }}
                    onOpenNotes={() => {
                      setTab('notes');
                      setPanelOpen(true);
                    }}
                  />
                </section>
              ))}
            </div>
          )}
        </div>

        {panelOpen && (
          <>
            {/* phone/tablet: bottom sheet */}
            <button type="button" aria-label="Paneli kapat" onClick={() => setPanelOpen(false)} className="lg:hidden fixed inset-0 z-[61] bg-[rgba(14,26,38,0.35)] cursor-default" />
            <aside
              aria-label="Etkileşim paneli"
              className="fixed lg:static z-[62] left-0 right-0 bottom-0 max-h-[78dvh] lg:max-h-none lg:h-full rounded-t-[18px] lg:rounded-none bg-white border-t lg:border-t-0 lg:border-l border-line flex flex-col min-h-0 shadow-[0_-12px_40px_rgba(14,26,38,0.18)] lg:shadow-none"
            >
              <div className="lg:hidden flex justify-center pt-2" aria-hidden="true">
                <span className="w-10 h-1 rounded-full bg-line-2" />
              </div>
              <InteractionPanel deck={deck} slide={slide} tab={tab} setTab={setTab} />
            </aside>
          </>
        )}
      </div>

      {/* Bottom navigation: prev · thumbnails · next */}
      <nav aria-label="Slayt gezgini" className="shrink-0 h-14 sm:h-16 bg-white border-t border-line px-2 sm:px-3 flex items-center gap-2">
        <button type="button" onClick={prev} disabled={atStart} aria-label="Önceki sayfa" className={iconBtn}>
          <ChevronLeft className="w-5 h-5" />
        </button>
        <div ref={stripRef} className="flex-1 min-w-0 flex gap-1.5 overflow-x-auto no-scrollbar py-1">
          {slides.map((s, i) => {
            const on = i === index;
            return (
              <button
                key={i}
                type="button"
                data-thumb={i}
                onClick={() => goTo(i)}
                aria-current={on ? 'step' : undefined}
                aria-label={`Slayt ${i + 1}: ${s.title}`}
                title={s.title}
                className={`shrink-0 h-9 sm:h-10 rounded-[9px] px-2.5 flex items-center gap-2 text-left cursor-pointer border transition-colors ${
                  on ? 'border-accent bg-accent-soft text-accent' : 'border-line bg-white text-ink-2 hover:border-line-2'
                }`}
              >
                <span className="font-mono text-[12px] font-semibold">{String(i + 1).padStart(2, '0')}</span>
                <span className={`hidden md:block max-w-[160px] truncate text-[12px] ${on ? 'font-semibold' : ''}`}>{s.title}</span>
              </button>
            );
          })}
        </div>
        <span className="sm:hidden font-mono text-[12px] text-ink-2 shrink-0">
          {index + 1}/{n}
        </span>
        <button type="button" onClick={next} disabled={atEnd} aria-label="Sonraki sayfa" className={`${iconBtn} bg-accent text-white hover:bg-accent-hover hover:text-white`}>
          <ChevronRight className="w-5 h-5" />
        </button>
      </nav>

      {/* Global topic search modal */}
      {searchOpen && (
        <GlobalTopicSearchModal
          deck={deck}
          onSelect={(slideIdx) => {
            goTo(slideIdx);
            setPanelOpen(true);
            setSearchOpen(false);
          }}
          onClose={() => setSearchOpen(false)}
        />
      )}
    </div>
  );
};

// ---------------------------------------------------------------------------
// Global Topic Search Modal (searches slide contents, notes, cards and questions)
// ---------------------------------------------------------------------------
const GlobalTopicSearchModal: React.FC<{
  deck: InteractiveDeck;
  onSelect: (slideIdx: number) => void;
  onClose: () => void;
}> = ({ deck, onSelect, onClose }) => {
  const [q, setQ] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const results = useMemo(() => {
    const queryNorm = q.trim().toLocaleLowerCase('tr-TR');
    if (!queryNorm || queryNorm.length < 2) return [];

    const matches: Array<{
      slideIndex: number;
      slideNumber: number;
      slideTitle: string;
      matchedType: string;
      snippet: string;
    }> = [];

    deck.slides.forEach((slide, sIdx) => {
      // 1. Title / Subtitle
      if (slide.title.toLocaleLowerCase('tr-TR').includes(queryNorm)) {
        matches.push({
          slideIndex: sIdx,
          slideNumber: slide.slideNumber,
          slideTitle: slide.title,
          matchedType: 'Başlık',
          snippet: slide.subtitle || slide.title,
        });
        return;
      }
      // 2. Synthesis Narrative / Content
      const narrativeText = slide.synthesisNarrative || (slide as any).content || '';
      if (narrativeText && narrativeText.toLocaleLowerCase('tr-TR').includes(queryNorm)) {
        const idx = narrativeText.toLocaleLowerCase('tr-TR').indexOf(queryNorm);
        const start = Math.max(0, idx - 40);
        const end = Math.min(narrativeText.length, idx + queryNorm.length + 80);
        matches.push({
          slideIndex: sIdx,
          slideNumber: slide.slideNumber,
          slideTitle: slide.title,
          matchedType: 'Ders Notu Sentezi',
          snippet: (start > 0 ? '...' : '') + narrativeText.slice(start, end) + (end < narrativeText.length ? '...' : ''),
        });
        return;
      }
      // 3. Key bullets
      const foundBullet = (slide.coreContent?.keyBullets || []).find(
        (b) => b.title.toLocaleLowerCase('tr-TR').includes(queryNorm) || b.desc.toLocaleLowerCase('tr-TR').includes(queryNorm)
      );
      if (foundBullet) {
        matches.push({
          slideIndex: sIdx,
          slideNumber: slide.slideNumber,
          slideTitle: slide.title,
          matchedType: 'Klinik Bilgi',
          snippet: `${foundBullet.title}: ${foundBullet.desc}`,
        });
        return;
      }
      // 4. Flashcards
      const foundCard = (slide.flashcards || []).find(
        (fc) => (fc.front || '').toLocaleLowerCase('tr-TR').includes(queryNorm) || (fc.back || '').toLocaleLowerCase('tr-TR').includes(queryNorm)
      );
      if (foundCard) {
        matches.push({
          slideIndex: sIdx,
          slideNumber: slide.slideNumber,
          slideTitle: slide.title,
          matchedType: 'Akıl Kartı',
          snippet: `Soru: ${foundCard.front || ''} -> ${(foundCard.back || '').slice(0, 110)}...`,
        });
        return;
      }
      // 5. Spot Pearls / Spots
      const slideSpots = (slide.spotPearls && slide.spotPearls.length > 0) ? slide.spotPearls : ((slide as any).spots || []);
      const foundPearl = slideSpots.find((p: any) => {
        const str = typeof p === 'string' ? p : `${p?.badge ? p.badge + ' ' : ''}${p?.text || ''}`;
        return str.toLocaleLowerCase('tr-TR').includes(queryNorm);
      });
      if (foundPearl) {
        const pearlStr = typeof foundPearl === 'string' ? foundPearl : `${foundPearl?.badge ? foundPearl.badge + ' ' : ''}${foundPearl?.text || ''}`;
        matches.push({
          slideIndex: sIdx,
          slideNumber: slide.slideNumber,
          slideTitle: slide.title,
          matchedType: 'Spot İnci',
          snippet: pearlStr,
        });
        return;
      }
      // 6. Questions
      const slideQuestions = (slide.relatedQuestions && slide.relatedQuestions.length > 0)
        ? slide.relatedQuestions
        : ((slide as any).practiceQuestion ? [(slide as any).practiceQuestion] : []);
      const foundQ = slideQuestions.find(
        (rq: any) => (rq.stem || '').toLocaleLowerCase('tr-TR').includes(queryNorm) || (rq.explanation || '').toLocaleLowerCase('tr-TR').includes(queryNorm)
      );
      if (foundQ) {
        matches.push({
          slideIndex: sIdx,
          slideNumber: slide.slideNumber,
          slideTitle: slide.title,
          matchedType: 'Çıkmış Soru',
          snippet: (foundQ.stem || '').slice(0, 130) + '...',
        });
      }
    });

    return matches;
  }, [deck, q]);

  return (
    <div className="fixed inset-0 z-[70] bg-[rgba(14,26,38,0.5)] backdrop-blur-xs flex items-center justify-center p-3 sm:p-6" role="dialog" aria-modal="true">
      <div className="w-full max-w-2xl bg-white border border-line rounded-[18px] shadow-2xl flex flex-col max-h-[85dvh] overflow-hidden animate-in fade-in duration-200">
        {/* Modal Search Header */}
        <div className="p-3.5 sm:p-4 border-b border-line flex items-center gap-2.5">
          <Search className="w-5 h-5 text-accent shrink-0" />
          <input
            ref={inputRef}
            type="search"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Ders içinde konu, patofizyoloji, tanı, akıl kartı veya soru ara..."
            className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[15px] sm:text-[16px] placeholder:text-[#6B7785]"
          />
          {q && (
            <button type="button" onClick={() => setQ('')} className="p-1 text-ink-3 hover:text-ink cursor-pointer">
              <X className="w-4 h-4" />
            </button>
          )}
          <button
            type="button"
            onClick={onClose}
            className="shrink-0 whitespace-nowrap h-8 px-2.5 rounded-lg bg-canvas hover:bg-line text-[12px] font-semibold text-ink-2 cursor-pointer"
          >
            Kapat (Esc)
          </button>
        </div>

        {/* Modal Results List */}
        <div className="flex-1 min-h-0 overflow-y-auto p-3 sm:p-4 flex flex-col gap-2">
          {!q.trim() ? (
            <div className="py-12 text-center text-ink-3 text-[14px]">
              <Search className="w-8 h-8 mx-auto mb-2 text-ink-3 opacity-40" />
              <p className="m-0 font-medium text-ink-2">Bu dersteki tüm slaytlar, klinik maddeler ve akıl kartları taranır.</p>
              <p className="m-0 text-[13px] mt-1">Aramak istediğin tıbbi kavramı yazmaya başla (örn. forniks, trabekülasyon, POD, pyelointerstisyel, BPH)...</p>
            </div>
          ) : results.length === 0 ? (
            <div className="py-12 text-center text-ink-3 text-[14px]">
              <p className="m-0 font-medium text-ink-2">"{q}" için ders içeriğinde eşleşme bulunamadı.</p>
              <p className="m-0 text-[13px] mt-1">Farklı bir tıp terimi ya da kelime kökü dene.</p>
            </div>
          ) : (
            <>
              <div className="text-[12px] font-semibold text-ink-3 px-1 pb-1">
                Ders içeriğinde {results.length} eşleşme bulundu:
              </div>
              {results.map((r, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => onSelect(r.slideIndex)}
                  className="w-full text-left rounded-xl border border-line hover:border-accent p-3 bg-white hover:bg-accent-soft/30 transition-all cursor-pointer flex flex-col gap-1.5 group"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-semibold text-[13px] text-accent flex items-center gap-1.5">
                      <span className="font-mono text-[11px] px-1.5 py-0.5 rounded bg-accent-soft text-accent">
                        Slayt {r.slideNumber}
                      </span>
                      <span className="truncate">{r.slideTitle}</span>
                    </span>
                    <span className="text-[11px] font-semibold text-ink-2 bg-black/5 px-2 py-0.5 rounded">
                      {r.matchedType}
                    </span>
                  </div>
                  <p className="m-0 text-[13.5px] leading-[1.5] text-ink line-clamp-2">
                    {r.snippet}
                  </p>
                </button>
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Enhanced Differential Diagnosis & Comparison Table Component
// ---------------------------------------------------------------------------
export const EnhancedDifferentialTable: React.FC<{
  table: SlideContentTable;
  compact?: boolean;
}> = ({ table, compact = false }) => {
  if (!table || !table.headers || table.headers.length === 0) return null;

  const titleLower = (table.title || '').toLowerCase();
  const isDiffDiagnosis =
    titleLower.includes('ayırıcı') ||
    titleLower.includes('tanı') ||
    titleLower.includes('karşılaştırma') ||
    titleLower.includes('fark') ||
    titleLower.includes('tipler') ||
    titleLower.includes('sınıflama') ||
    table.headers.some((h) => {
      const hl = h.toLowerCase();
      return (
        hl.includes('ayırıcı') ||
        hl.includes('benign') ||
        hl.includes('malign') ||
        hl.includes('tip') ||
        hl.includes('evre')
      );
    });

  // Cell semantic coloring helper
  const renderCellContent = (cellText: string, isFirstCol: boolean) => {
    if (isFirstCol) {
      return (
        <span className="font-bold text-ink">
          <Rich text={cellText} />
        </span>
      );
    }

    const t = cellText.toLowerCase().trim();

    // 1. Red / Rose (Malign, Poor prognosis, Lethal, Cancer, Severe, Urgent)
    const isRed =
      /\b(malign|kötü huylu|karsinom|sarkom|pozitif|ölümcül|acil|kritik|yüksek mortalite|metastaz|irreversibl|nekroz|agresif|kötü prognoz|refrakter)\b/i.test(t);

    if (isRed) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[11.5px] font-semibold bg-rose-500/10 text-rose-700 dark:text-rose-300 border border-rose-500/20 shadow-2xs">
          <span className="w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0" />
          <Rich text={cellText} />
        </span>
      );
    }

    // 2. Green / Emerald (Benign, Normal, Negative, Good prognosis)
    const isGreen =
      /\b(benign|iyi huylu|normal|negatif|kür|yüksek sağkalım|spontan geriler|reversibl|minimal)\b/i.test(t);

    if (isGreen) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[11.5px] font-medium bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20 shadow-2xs">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0" />
          <Rich text={cellText} />
        </span>
      );
    }

    // 3. Amber (Warning, Pitfall, Moderate risk, Variable, Recurrence)
    const isAmber =
      /\b(tuzak|dikkat|şüpheli|orta risk|değişken|relaps sık|sık nüks|subklinik)\b/i.test(t);

    if (isAmber) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[11.5px] font-medium bg-amber-500/10 text-amber-800 dark:text-amber-300 border border-amber-500/20 shadow-2xs">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0" />
          <Rich text={cellText} />
        </span>
      );
    }

    // 4. Blue / Indigo (Diagnostic Criteria, Gold standard, Specific hallmark)
    const isBlue =
      /\b(altın standart|tanı kriteri|patognomonik|spike and dome|hump|tram-track|kresent|lineer if|granüler if)\b/i.test(t);

    if (isBlue) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[11.5px] font-medium bg-blue-500/10 text-blue-800 dark:text-blue-300 border border-blue-500/20 shadow-2xs">
          <span className="w-1.5 h-1.5 rounded-full bg-blue-500 shrink-0" />
          <Rich text={cellText} />
        </span>
      );
    }

    return <Rich text={cellText} />;
  };

  return (
    <div className={`rounded-xl border border-line overflow-hidden bg-white shadow-2xs ${compact ? 'mt-1' : 'mt-2.5'}`}>
      {/* Table Header Banner */}
      <div className="px-3.5 py-2 bg-gradient-to-r from-canvas via-white to-canvas text-[12px] font-bold border-b border-line text-ink flex items-center justify-between gap-2">
        <div className="flex items-center gap-2 min-w-0">
          <span className="w-2 h-2 rounded-full bg-accent shrink-0 shadow-2xs" />
          <span className="truncate">{table.title || 'Klinik & Patolojik Karşılaştırma Tablosu'}</span>
        </div>
        {isDiffDiagnosis && (
          <span className="shrink-0 text-[10px] font-bold uppercase tracking-wider bg-accent-soft text-accent border border-accent/20 px-2 py-0.5 rounded-full shadow-2xs">
            Ayırıcı Tanı & Sınıflama
          </span>
        )}
      </div>

      <div className="overflow-x-auto custom-scrollbar">
        <table className={`w-full border-collapse ${table.headers.length >= 4 || compact ? 'text-[12px]' : 'text-[12.5px] sm:text-[13px]'}`}>
          <thead>
            <tr className="bg-canvas/90 border-b border-line">
              {table.headers.map((h, i) => (
                <th
                  key={i}
                  scope="col"
                  className={`text-left font-bold text-ink px-3 py-2.5 align-middle ${
                    i === 0 ? 'bg-canvas text-ink w-1/4' : 'text-ink-2'
                  }`}
                >
                  <div className="flex items-center gap-1.5">
                    {i === 0 ? (
                      <span className="text-accent text-[11px]">✦</span>
                    ) : (
                      <span className="w-1.5 h-1.5 rounded-full bg-accent/40" />
                    )}
                    <span>{h}</span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {table.rows.map((row, ri) => (
              <tr
                key={ri}
                className={`border-b border-line-soft last:border-0 transition-colors ${
                  ri % 2 === 0 ? 'bg-white' : 'bg-canvas/40'
                } hover:bg-accent-soft/20`}
              >
                {row.map((cell, ci) => (
                  <td
                    key={ci}
                    className={`px-3 py-2.5 align-top leading-relaxed ${
                      ci === 0
                        ? 'font-semibold text-ink bg-canvas/30 border-r border-line-soft'
                        : 'text-ink-2'
                    }`}
                  >
                    {renderCellContent(cell, ci === 0)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Key Bullets Component: Categorized Medical Bullets with Semantic Colors & Icons
// (Ders Notu, Spot Bilgi, Ayırt Edici Özellikler, Dikkat / Tuzak, Özet & Tekrar)
// ---------------------------------------------------------------------------
export const KeyBulletsRenderer: React.FC<{
  bullets: Array<{ title: string; desc: string; isKey?: boolean }>;
  compact?: boolean;
}> = ({ bullets, compact = false }) => {
  if (!bullets || bullets.length === 0) return null;

  return (
    <div className={`flex flex-col ${compact ? 'gap-2' : 'gap-2.5 my-2.5'}`}>
      <div className="flex items-center justify-between gap-2 px-1">
        <span className="text-[11.5px] font-bold uppercase tracking-wider text-ink-3 flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-accent" />
          <span>Kritik Ders Notları, Spotlar ve Ayırt Edici Özellikler</span>
        </span>
        <span className="text-[11px] font-mono font-semibold text-ink-3 bg-canvas px-2 py-0.5 rounded-md border border-line">
          {bullets.length} Madde
        </span>
      </div>

      <div className="grid grid-cols-1 gap-2">
        {bullets.map((b, i) => {
          const t = b.title.toLowerCase();
          const d = b.desc.toLowerCase();

          // 1. Red: Dikkat / Sınav Tuzağı / Kritik / Ölümcül / Kontrendike / Hayati
          const isRed =
            /^(?:🔴|🚨|⚠️)/.test(b.title) ||
            /\b(dikkat|tuzak|sınav tuzağı|kritik|ölümcül|acil|hayati|kontrendike|yanılgı|hata|sakın)\b/i.test(t) ||
            /\b(asla|ölümcül|kontrendike)\b/i.test(d);

          // 2. Amber: Spot Bilgi / Hoca İncisi / Sınav Sorusu / Püf Nokta
          const isAmber =
            !isRed &&
            (/(?:💡|⚡|🎯)/.test(b.title) ||
              /\b(spot|hoca incisi|sınav spotu|püf nokta|ipucu|çıkmış soru|komite|tus)\b/i.test(t));

          // 3. Blue: Ayırt Edici Özellikler / Ayırıcı Tanı / Karşılaştırma / Kriter
          const isBlue =
            !isRed &&
            !isAmber &&
            (/(?:🔍|⚖️|⚡)/.test(b.title) ||
              /\b(ayırt edici|ayırıcı tanı|fark|karşılaştırma|kriter|altın standart|patognomonik|spesifik)\b/i.test(t));

          // 4. Purple: Özet / Tekrar / Sentez / Hatırlatma
          const isPurple =
            !isRed &&
            !isAmber &&
            !isBlue &&
            (/(?:🔄|✨|🧬)/.test(b.title) ||
              /\b(özet|tekrar|sentez|hatırlatma|yaklaşım|prognoz|sonuç)\b/i.test(t));

          let badgeCls = 'bg-teal-500/10 text-teal-800 dark:text-teal-300 border-teal-500/20';
          let borderCls = 'border-l-4 border-l-teal-500 bg-teal-50/20 dark:bg-teal-950/20 border-line-soft';
          let icon = <BookOpen className="w-3.5 h-3.5 text-teal-600 shrink-0" />;

          if (isRed) {
            badgeCls = 'bg-rose-500/10 text-rose-800 dark:text-rose-300 border-rose-500/30';
            borderCls = 'border-l-4 border-l-rose-500 bg-rose-50/40 dark:bg-rose-950/30 border-rose-500/20';
            icon = <AlertTriangle className="w-3.5 h-3.5 text-rose-600 shrink-0" />;
          } else if (isAmber) {
            badgeCls = 'bg-amber-500/10 text-amber-900 dark:text-amber-300 border-amber-500/30';
            borderCls = 'border-l-4 border-l-amber-500 bg-amber-50/40 dark:bg-amber-950/30 border-amber-500/20';
            icon = <Lightbulb className="w-3.5 h-3.5 text-amber-600 shrink-0" />;
          } else if (isBlue) {
            badgeCls = 'bg-blue-500/10 text-blue-900 dark:text-blue-300 border-blue-500/30';
            borderCls = 'border-l-4 border-l-blue-500 bg-blue-50/40 dark:bg-blue-950/30 border-blue-500/20';
            icon = <ArrowLeftRight className="w-3.5 h-3.5 text-blue-600 shrink-0" />;
          } else if (isPurple) {
            badgeCls = 'bg-purple-500/10 text-purple-900 dark:text-purple-300 border-purple-500/30';
            borderCls = 'border-l-4 border-l-purple-500 bg-purple-50/40 dark:bg-purple-950/30 border-purple-500/20';
            icon = <RotateCcw className="w-3.5 h-3.5 text-purple-600 shrink-0" />;
          }

          return (
            <div
              key={i}
              className={`rounded-xl p-3 sm:p-3.5 border transition-all duration-150 flex items-start gap-3 shadow-2xs ${borderCls}`}
            >
              <div className="mt-0.5 shrink-0 flex flex-col items-center gap-1">
                <span className="w-6 h-6 rounded-lg bg-white/90 dark:bg-panel shadow-2xs border border-line flex items-center justify-center">
                  {icon}
                </span>
                <span className="text-[10px] font-mono font-bold text-ink-3">
                  #{i + 1}
                </span>
              </div>

              <div className="flex flex-col gap-1 min-w-0 flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className={`text-[11px] font-bold px-2 py-0.5 rounded-md border shadow-2xs ${badgeCls}`}>
                    {b.title}
                  </span>
                </div>
                <div className="text-[12.5px] sm:text-[13px] text-ink leading-relaxed font-normal">
                  <Rich text={b.desc} />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// One slide, sized to the stage (16:9 feel on wide screens, scrolls inside if long)
// ---------------------------------------------------------------------------
const SlideCanvas: React.FC<{
  slide: SlideItem;
  index: number;
  total: number;
  onOpenQuestions?: () => void;
  onOpenFlashcards?: () => void;
  onOpenNotes?: () => void;
  onNext?: () => void;
  onPrev?: () => void;
  paged?: boolean;
  /** Storage key for the student's own highlights on this slide */
  highlightScope?: string;
}> = ({ slide, index, total, onOpenQuestions, onOpenFlashcards, onOpenNotes, onNext, paged = false, highlightScope }) => {
  const [copied, setCopied] = useState(false);
  const containerRef = useRef<HTMLElement>(null);

  // When changing slides in paged mode, scroll to top immediately
  useEffect(() => {
    containerRef.current?.scrollTo({ top: 0, behavior: 'instant' });
  }, [index, slide]);

  const hl = slide.professorAudioHighlight;
  const emph = hl ? EMPHASIS[hl.emphasisType] || EMPHASIS.pearl : null;
  const c = slide.coreContent || {};
  const badge = tone(slide.badgeColor);
  const flashcards = slide.flashcards || [];
  const narrative = slide.synthesisNarrative || (slide as any).content || '';
  const spots = (slide.spotPearls && slide.spotPearls.length > 0) ? slide.spotPearls : ((slide as any).spots || []);

  const copyQuote = () => {
    if (!hl?.quote) return;
    navigator.clipboard?.writeText(hl.quote).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    });
  };

  return (
    <article
      ref={containerRef}
      className={`w-full ${paged ? 'h-full overflow-y-auto overscroll-contain' : 'min-h-full'} max-w-[1280px] mx-auto bg-white border border-line rounded-[18px] shadow-[0_2px_16px_rgba(14,26,38,0.06)] flex flex-col min-h-0 custom-scrollbar relative`}
    >
      <SlideDrawingCanvas scope={highlightScope || `slide:${slide.slideNumber}`} />
      <Highlightable
        scope={highlightScope || `slide:${slide.slideNumber}:${slide.title}`}
        className="px-4 py-4 sm:px-6 sm:py-5 lg:px-8 lg:py-6 flex flex-col gap-4 sm:gap-6"
      >
        {/* Slide header */}
        <header className="flex flex-col gap-2.5 pb-2 border-b border-line-soft">
          {/* Üst Başlık (Eyebrow & Metadata) */}
          <div className="flex items-center gap-2 flex-wrap text-[12px]">
            <span className="font-mono font-bold text-accent bg-accent-soft px-2.5 py-1 rounded-lg border border-accent/20 flex items-center gap-1.5 shadow-2xs">
              <GraduationCap className="w-3.5 h-3.5" />
              <span>Slayt {String(index + 1).padStart(2, '0')} / {String(total).padStart(2, '0')}</span>
            </span>
            {slide.badge && (
              <span className="h-7 px-3 rounded-lg text-[12px] font-bold tracking-[0.03em] inline-flex items-center shadow-2xs" style={{ background: badge.bg, color: badge.fg }}>
                {slide.badge}
              </span>
            )}
            <span className="hidden sm:inline-flex items-center gap-1 text-ink-3 text-[12px] font-medium">
              <span>•</span>
              <span>Dönem 3 Kurul 1 Patoloji ve Klinik Müfredatı</span>
            </span>
          </div>

          {/* Büyük Ana Başlık */}
          <h2 className="m-0 font-display font-extrabold tracking-[-0.025em] leading-[1.18] text-[20px] sm:text-[24px] lg:text-[27px] text-ink">
            {slide.title}
          </h2>

          {/* Vurgulu Alt Başlık */}
          {slide.subtitle && (
            <div className="p-2.5 sm:p-3 rounded-xl bg-gradient-to-r from-accent-soft/30 via-white to-canvas border border-accent/20 flex items-start gap-2.5 shadow-2xs">
              <span className="text-[14px] shrink-0 select-none mt-0.5">💡</span>
              <div className="flex flex-col gap-0.5 min-w-0">
                <span className="text-[10.5px] font-bold uppercase tracking-wider text-accent">Kavram & Odak Özeti</span>
                <p className="m-0 text-[12.5px] sm:text-[13.5px] font-medium text-ink-2 leading-[1.55]">
                  {slide.subtitle}
                </p>
              </div>
            </div>
          )}
        </header>

        {/* 1. Clinical & Exam Critical Pearl */}
        {hl && emph && (
          <figure className="m-0 rounded-2xl border-2 border-accent/20 bg-gradient-to-r from-accent-soft/30 via-white to-accent-soft/10 p-3.5 sm:p-4.5 flex flex-col gap-2 shadow-xs">
            <figcaption className="flex items-center gap-2">
              <span
                className="h-6 px-2.5 rounded-full text-[11.5px] font-semibold inline-flex items-center gap-1.5 shadow-2xs"
                style={{ background: tone(emph.c).bg, color: tone(emph.c).fg }}
              >
                <emph.icon className="w-3.5 h-3.5" />
                {emph.label}
              </span>
              <span className="text-[11.5px] font-semibold text-accent uppercase tracking-wider">
                Klinik & Sınav Kritik Vurgusu
              </span>
              <button
                type="button"
                onClick={copyQuote}
                aria-label="Alıntıyı kopyala"
                className="ml-auto h-7 px-2 rounded-lg flex items-center gap-1 text-[11.5px] text-ink-2 hover:bg-white border border-transparent hover:border-line cursor-pointer transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-ok" /> : <Copy className="w-3.5 h-3.5" />}
                <span className="hidden sm:inline">{copied ? 'Kopyalandı' : 'Kopyala'}</span>
              </button>
            </figcaption>
            <blockquote className="m-0 text-[13.5px] sm:text-[14.5px] font-medium leading-[1.6] text-ink border-l-3 border-accent pl-3.5 italic">
              “{hl.quote}”
            </blockquote>
            {hl.note && (
              <p className="m-0 text-[12px] sm:text-[12.5px] text-ink-2 leading-[1.55] bg-white/60 p-2 sm:p-2.5 rounded-xl border border-line-soft">
                💡 <strong>Klinik Yaklaşım:</strong> {hl.note}
              </p>
            )}
          </figure>
        )}

        {/* 2. Fluid Synthesized Narrative (Kapsamlı Ders Notu Sentezi) */}
        {narrative && (
          <section className="rounded-2xl border border-line bg-gradient-to-br from-blue-50/40 via-white to-indigo-50/20 p-3.5 sm:p-5 shadow-xs flex flex-col gap-2.5">
            <div className="flex items-center justify-between gap-2 border-b border-line pb-2.5">
              <div className="flex items-center gap-2.5 min-w-0">
                <span className="w-7 h-7 rounded-xl bg-accent text-white flex items-center justify-center shrink-0 shadow-xs">
                  <BookOpen className="w-4 h-4" />
                </span>
                <div>
                  <span className="text-[10.5px] font-bold uppercase tracking-wider text-accent block">
                    Öğrenim Bölümü • Detaylı Müfredat Analizi
                  </span>
                  <h3 className="m-0 text-[14.5px] sm:text-[15.5px] font-bold text-ink">
                    {slide.discipline?.toLowerCase().includes('patoloji')
                      ? 'Kapsamlı Ders Notu ve Patoloji Sentezi'
                      : `Kapsamlı Ders Notu ve ${slide.discipline || 'Müfredat'} Sentezi`}
                  </h3>
                </div>
              </div>
              {onOpenNotes && (
                <button
                  type="button"
                  onClick={onOpenNotes}
                  className="shrink-0 whitespace-nowrap h-7.5 px-2.5 rounded-lg bg-white border border-line text-[11.5px] font-semibold text-accent hover:bg-accent-soft inline-flex items-center gap-1 cursor-pointer transition-colors shadow-2xs"
                >
                  <FileText className="w-3.5 h-3.5" />
                  <span>Panelde Oku</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
            {/* Quick Medical Terms Pills for This Slide */}
            <SlideTermsPills
              textToScan={`${slide.title || ''} ${narrative} ${((slide as any).keyConcepts || []).join(' ')}`}
              className="mb-1"
            />
            
            <StructuredSynthesisRenderer text={narrative} />

            {/* Categorized Key Bullets with Colors & Icons */}
            {c.keyBullets && c.keyBullets.length > 0 && (
              <KeyBulletsRenderer bullets={c.keyBullets} />
            )}

            {/* Comparison / Classification Table on Slide Canvas */}
            {c.table && (
              <EnhancedDifferentialTable table={c.table} />
            )}
          </section>
        )}

        {/* 3. Interactive 3D Flashcards (Akıl Kartları Atölyesi) */}
        {flashcards.length > 0 && (
          <section className="flex flex-col gap-2.5 pt-1">
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2.5 min-w-0">
                <span className="w-7 h-7 rounded-lg bg-amber-500 text-white flex items-center justify-center shrink-0">
                  <BrainCircuit className="w-4 h-4" />
                </span>
                <div>
                  <h3 className="m-0 text-[14px] sm:text-[14.5px] font-bold text-ink flex flex-wrap items-center gap-x-2 gap-y-1">
                    <span>Akıl Kartları (Tıkla & Çevir)</span>
                    <span className="shrink-0 whitespace-nowrap font-mono text-[11px] font-semibold text-amber-800 bg-amber-100 px-2 py-0.5 rounded-full">
                      {flashcards.length} Kart
                    </span>
                  </h3>
                  <p className="m-0 text-[11.5px] text-ink-3">
                    Kafanda yanıtla, ardından karta tıklayarak cevabı ve amfi ipucunu aç
                  </p>
                </div>
              </div>

              {onOpenFlashcards && (
                <button
                  type="button"
                  onClick={onOpenFlashcards}
                  className="shrink-0 whitespace-nowrap h-7.5 px-2.5 rounded-lg bg-canvas hover:bg-white border border-line text-[11.5px] font-semibold text-ink-2 hover:text-ink inline-flex items-center gap-1 cursor-pointer transition-colors"
                >
                  <span>Panelde Çalış</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-3.5">
              {flashcards.map((card) => (
                <FlashcardComponent key={card.id} card={card} />
              ))}
            </div>
          </section>
        )}

        {/* 4. Interactive Questions (Doğrudan Slayt Üzerinde Çözülebilir Sorular) */}
        {(slide.relatedQuestions || []).length > 0 && (
          <section id={`slide-questions-${slide.slideNumber}`} className="flex flex-col gap-2.5 pt-1 scroll-mt-6">
            <div className="flex items-center justify-between gap-2 border-b border-line-soft pb-2">
              <div className="flex items-center gap-2 min-w-0">
                <span className="w-7 h-7 rounded-lg bg-emerald-600 text-white flex items-center justify-center shrink-0 shadow-2xs">
                  <CheckCircle2 className="w-4 h-4" />
                </span>
                <div>
                  <h3 className="m-0 text-[14px] sm:text-[14.5px] font-bold text-ink flex items-center gap-2">
                    <span>Eşleşen Kurul & Çıkmış Sorular</span>
                    <span className="shrink-0 font-mono text-[11px] font-semibold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-full">
                      {(slide.relatedQuestions || []).length} Soru
                    </span>
                  </h3>
                  <p className="m-0 text-[11.5px] text-ink-3">
                    Paneli açmaya gerek kalmadan doğrudan bu slayt üzerinden çözebilirsiniz
                  </p>
                </div>
              </div>

              {onOpenQuestions && (
                <button
                  type="button"
                  onClick={onOpenQuestions}
                  className="shrink-0 whitespace-nowrap h-7.5 px-2.5 rounded-lg bg-canvas hover:bg-white border border-line text-[11.5px] font-semibold text-ink-2 hover:text-ink inline-flex items-center gap-1 cursor-pointer transition-colors"
                >
                  <span>Panelde Aç</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              )}
            </div>

            <div className="grid grid-cols-1 gap-3">
              {(slide.relatedQuestions || []).map((q, i) => (
                <QuizCard key={`canvas-${slide.slideNumber}-${q.id || i}`} q={q} n={i + 1} />
              ))}
            </div>
          </section>
        )}


        {/* 6. Core content: formulas, tables, bullets, infographics */}
        <div className={`grid grid-cols-1 ${c.table && c.table.headers?.length > 0 ? '' : 'lg:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)]'} gap-4 sm:gap-5 lg:gap-7 items-start`}>
          {/* Main content */}
          <div className="flex flex-col gap-4 min-w-0">
            {c.keyBullets && c.keyBullets.length > 0 && (
              <KeyBulletsRenderer bullets={c.keyBullets} />
            )}

            {c.infographic?.items?.length ? (
              <div className={`grid gap-2 ${c.infographic.items.length >= 3 ? 'grid-cols-1 sm:grid-cols-3' : 'grid-cols-1 sm:grid-cols-2'}`}>
                {c.infographic.items.map((it, i) => {
                  const t = tone(it.color);
                  return (
                    <div key={i} className="rounded-xl border border-line p-3 flex flex-col gap-0.5" style={{ background: t.bg }}>
                      <span className="text-[12px] font-semibold" style={{ color: t.fg }}>
                        {it.label}
                      </span>
                      <span className="font-mono text-[18px] sm:text-[20px] font-semibold text-ink leading-tight">{it.value}</span>
                      {it.detail && <span className="text-[12px] text-ink-2 leading-snug">{it.detail}</span>}
                    </div>
                  );
                })}
              </div>
            ) : null}

            {c.formulaBox && (
              <div className="rounded-xl bg-accent-soft p-3.5 sm:p-4 flex flex-col gap-1.5">
                <span className="text-[12px] font-semibold uppercase tracking-[0.06em] text-accent">{c.formulaBox.title}</span>
                <code className="font-mono text-[14px] sm:text-[16px] text-ink whitespace-pre-wrap break-words">{c.formulaBox.formula}</code>
                {c.formulaBox.explanation && <Rich text={c.formulaBox.explanation} className="text-[13px] text-ink-2 leading-[1.55]" />}
              </div>
            )}

            {c.table && c.table.headers?.length > 0 && (
              <EnhancedDifferentialTable table={c.table} />
            )}
          </div>

          {/* Side: spot pearls */}
          <div className="flex flex-col gap-3 min-w-0">
            {spots.length > 0 && <SpotList items={spots} />}
          </div>
        </div>
        {paged && index < total - 1 && onNext && (
          <div className="mt-2 pt-3.5 border-t border-line-soft flex items-center justify-between text-[12.5px] text-ink-3">
            <span>Slayt {index + 1} / {total} · Aşağı kaydırarak tamamını okuyabilirsiniz</span>
            <button
              type="button"
              onClick={onNext}
              className="shrink-0 whitespace-nowrap h-8 px-3 rounded-lg bg-accent-soft hover:bg-accent hover:text-white text-accent font-semibold inline-flex items-center gap-1.5 cursor-pointer transition-colors"
            >
              <span>Sonraki Slayta Geç</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}
      </Highlightable>
    </article>
  );
};

// ---------------------------------------------------------------------------
// Spot list: warm "Akılda tut" card with numbered, structured items
// Supports:
// - Red (Kırmızı) = Önemli / Kritik / Hayati
// - Blue (Mavi) = Sorulmuş Soru / Komite / TUS Sınav Sorusu
// - Normal = Genel Spot Bilgi
// - Sub-bullets (alt madde) and Upper-bullets (üst madde)
// ---------------------------------------------------------------------------
const SpotList: React.FC<{ items: Array<string | any>; title?: string; note?: string; compact?: boolean }> = ({
  items,
  title = 'Akılda tut',
  note,
  compact = false,
}) => (
  <section className={`rounded-2xl border border-[#F2DDB8] bg-[#FFF9EF] dark:bg-[#1C1814] dark:border-[#523A1E] flex flex-col ${compact ? 'p-3 gap-2.5' : 'p-3.5 sm:p-4 gap-3'}`}>
    <header className="flex items-center gap-2">
      <span className="w-7 h-7 rounded-[9px] bg-[#FCE9C6] dark:bg-[#3D2508] text-[#9A4D06] dark:text-[#E6934A] flex items-center justify-center shrink-0" aria-hidden="true">
        <Lightbulb className="w-4 h-4" />
      </span>
      <span className="text-[13.5px] font-semibold text-[#8A4405] dark:text-[#E6934A]">{title}</span>
      <span className="ml-auto text-[12px] font-mono text-[#9A4D06]/70 dark:text-[#E6934A]/70">{items.length}</span>
    </header>
    {note && <p className="m-0 -mt-1 text-[13px] text-[#8A4405]/80 dark:text-[#E6934A]/80">{note}</p>}
    <ol className={`list-none m-0 p-0 flex flex-col ${compact ? 'gap-2' : 'gap-2.5'}`}>
      {items.map((p, i) => {
        const isObj = p && typeof p === 'object';
        const pText: string = isObj ? (p.text || '') : String(p || '');
        const pBadge: string = isObj ? (p.badge || '') : '';
        const pType: string = isObj ? (p.type || '') : '';
        const pColor: string = isObj ? (p.color || '') : '';

        const isRed = pType === 'warning' || pColor === 'rose' || pBadge.includes('🔴') || /(?:🔴|🚨|⚠️|ölümcül|asla|acil|hayati|kritik|kontrendike|\[kırmızı|\[red|önemli)/i.test(pText);
        const isBlue = !isRed && (pType === 'exam' || pColor === 'sky' || pBadge.includes('🔵') || /(?:🔵|❓|❔|çıkmış soru|çıkmış|komite sorusu|tus sorusu|soruldu|ösym|\[mavi|\[blue|\[çıkmış|soru:)/i.test(pText));

        // Split multi-line spot pearls to support main bullets and sub-bullets
        const rawLines = pText.split('\n');

        return (
          <li
            key={i}
            className={`rounded-xl transition-all shadow-[0_1px_2px_rgba(0,0,0,0.04)] border flex flex-col ${
              isRed
                ? 'bg-red-50/80 dark:bg-red-950/25 border-red-200/90 dark:border-red-900/40 text-red-950 dark:text-red-100'
                : isBlue
                ? 'bg-blue-50/80 dark:bg-blue-950/25 border-blue-200/90 dark:border-blue-900/40 text-blue-950 dark:text-blue-100'
                : 'bg-white dark:bg-surface-elevated border-line-soft text-ink'
            } ${compact ? 'p-2.5 text-[13.5px]' : 'p-3 text-[14.5px]'} leading-[1.6]`}
          >
            {/* Top header row: Pill + Badge Icon */}
            <div className="flex items-center justify-between gap-2 mb-1.5 pb-1 border-b border-inherit/20">
              <span className="inline-flex items-center gap-1.5">
                {isRed ? (
                  <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10.5px] font-bold bg-red-100 dark:bg-red-900/60 text-red-700 dark:text-red-200">
                    <AlertCircle className="w-3 h-3" /> {pBadge ? pBadge.replace(/^[🔴🚨⚠️]\s*/, '') : 'ÖNEMLİ'}
                  </span>
                ) : isBlue ? (
                  <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10.5px] font-bold bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-200">
                    <HelpCircle className="w-3 h-3" /> {pBadge ? pBadge.replace(/^[🔵❓❔]\s*/, '') : 'ÇIKMIŞ SORU'}
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10.5px] font-semibold bg-amber-100/70 dark:bg-amber-950/40 text-[#9A4D06] dark:text-amber-300">
                    ⚡ {pBadge ? pBadge.replace(/^[⚡]\s*/, '') : 'SPOT BİLGİ'}
                  </span>
                )}
              </span>
              <span
                className={`w-[20px] h-[20px] rounded-full font-mono text-[11px] font-semibold flex items-center justify-center ${
                  isRed
                    ? 'bg-red-200 text-red-800 dark:bg-red-900/80 dark:text-red-100'
                    : isBlue
                    ? 'bg-blue-200 text-blue-800 dark:bg-blue-900/80 dark:text-blue-100'
                    : 'bg-[#FCE9C6] text-[#9A4D06] dark:bg-amber-950/60 dark:text-amber-200'
                }`}
              >
                {isRed ? '!' : isBlue ? '?' : i + 1}
              </span>
            </div>

            {/* Lines rendering: upper-bullets, sub-bullets, and paragraphs */}
            <div className="flex flex-col gap-1 min-w-0 break-words">
              {rawLines.map((line, lIdx) => {
                const trimmed = line.trim();
                if (!trimmed) return null;

                const isSubBullet =
                  (line.startsWith('  ') || line.startsWith('\t')) &&
                  (trimmed.startsWith('- ') || trimmed.startsWith('• ') || trimmed.startsWith('* ') || trimmed.startsWith('→ '));

                const isUpperBullet =
                  !isSubBullet &&
                  (trimmed.startsWith('• ') || trimmed.startsWith('* ') || /^[0-9]+\.\s/.test(trimmed));

                if (isSubBullet) {
                  const cleanText = trimmed.replace(/^[-•*→]\s*/, '');
                  return (
                    <div
                      key={lIdx}
                      className="ml-3.5 pl-2.5 py-0.5 border-l-2 border-inherit/40 text-[13px] flex items-start gap-1.5"
                    >
                      <span className="text-[10px] opacity-70 mt-1 select-none">▫</span>
                      <span className="min-w-0 flex-1">
                        <Rich text={cleanText} />
                      </span>
                    </div>
                  );
                }

                if (isUpperBullet) {
                  const cleanText = trimmed.replace(/^([•*]|\d+\.)\s*/, '');
                  return (
                    <div key={lIdx} className="font-semibold flex items-start gap-2 pt-0.5">
                      <span className="text-accent mt-0.5 select-none">▸</span>
                      <span className="min-w-0 flex-1">
                        <Rich text={cleanText} />
                      </span>
                    </div>
                  );
                }

                return (
                  <div key={lIdx}>
                    <Rich text={trimmed} />
                  </div>
                );
              })}
            </div>
          </li>
        );
      })}
    </ol>
  </section>
);

// ---------------------------------------------------------------------------
// Interaction panel: flashcards, questions, structured notes, deck pearls, ask AI
// ---------------------------------------------------------------------------
const InteractionPanel: React.FC<{
  deck: InteractiveDeck;
  slide: SlideItem;
  tab: PanelTab;
  setTab: (t: PanelTab) => void;
}> = ({ deck, slide, tab, setTab }) => {
  const qs = (slide.relatedQuestions && slide.relatedQuestions.length > 0)
    ? slide.relatedQuestions
    : ((slide as any).practiceQuestion ? [(slide as any).practiceQuestion] : []);
  const cards = slide.flashcards || [];

  const tabs: { id: PanelTab; label: string }[] = [
    { id: 'flashcards', label: `Kartlar ${cards.length}` },
    { id: 'questions', label: `Sorular ${qs.length}` },
    { id: 'notes', label: 'Ders Notu' },
    { id: 'pearls', label: 'Spotlar' },
    { id: 'ai', label: "AI'ya sor" },
    { id: 'pdf', label: 'PDF' },
  ];

  return (
    <>
      <div role="tablist" aria-label="Etkileşim" className="shrink-0 grid grid-cols-6 gap-0.5 sm:gap-1 m-3 mb-0 bg-canvas rounded-[12px] p-1">
        {tabs.map((t) => (
          <button
            key={t.id}
            type="button"
            role="tab"
            aria-selected={tab === t.id}
            onClick={() => setTab(t.id)}
            className={`h-8 sm:h-9 px-1 rounded-[9px] text-[11px] sm:text-[12px] cursor-pointer truncate ${tab === t.id ? 'bg-white text-ink font-semibold shadow-[0_1px_2px_rgba(14,26,38,0.08)]' : 'text-ink-2 hover:text-ink'}`}
          >
            {t.label}
          </button>
        ))}
      </div>
      <div className="flex-1 min-h-0 overflow-y-auto overscroll-contain p-3 flex flex-col gap-3">
        {tab === 'flashcards' && (
          <div className="flex flex-col gap-3">
            <div className="flex items-center justify-between px-1">
              <span className="text-[12px] text-ink-3">
                {cards.length} akıl kartı · Tıklayarak çevir
              </span>
            </div>
            {cards.length === 0 ? (
              <p className="m-0 text-[14px] text-ink-2 px-1 py-4">Bu slayt için tanımlı akıl kartı yok.</p>
            ) : (
              cards.map((c) => <FlashcardComponent key={c.id} card={c} />)
            )}
          </div>
        )}
        {tab === 'questions' &&
          (qs.length === 0 ? (
            <p className="m-0 text-[14px] text-ink-2 px-1 py-4">Bu slayta eşleşen soru yok.</p>
          ) : (
            qs.map((q, i) => <QuizCard key={`${slide.slideNumber}-${q.id}`} q={q} n={i + 1} />)
          ))}
        {tab === 'notes' && <SlideNotesTab slide={slide} />}
        {tab === 'pearls' && (
          (deck.highYieldPearls || []).length > 0 ? (
            <SpotList items={deck.highYieldPearls || []} title="Dersin spotları" note="Dersin tamamından en çok sorulan bilgiler" compact />
          ) : (
            <p className="m-0 text-[14px] text-ink-2 px-1 py-4">Bu ders için spot bilgi yok.</p>
          )
        )}
        {tab === 'ai' && <AskAi key={slide.slideNumber} deck={deck} slide={slide} />}
        {tab === 'pdf' && (
          <div className="flex-1 min-h-[460px] flex flex-col h-full rounded-xl overflow-hidden border border-line bg-white shadow-sm">
            <DeckPdfViewer deck={deck} currentSlideNumber={slide.slideNumber} compact />
          </div>
        )}
      </div>
    </>
  );
};

// ---------------------------------------------------------------------------
// Slide Notes Tab: Structured medical textbook notes and tables for the slide
// ---------------------------------------------------------------------------
const SlideNotesTab: React.FC<{ slide: SlideItem }> = ({ slide }) => {
  const c = slide.coreContent || {};
  const narrative = slide.synthesisNarrative || (slide as any).content || '';
  const spots = (slide.spotPearls && slide.spotPearls.length > 0) ? slide.spotPearls : ((slide as any).spots || []);

  return (
    <div className="flex flex-col gap-3.5">
      {/* Narrative block */}
      {narrative && (
        <div className="rounded-xl border border-line bg-gradient-to-br from-blue-50/50 via-white to-indigo-50/20 p-3.5 flex flex-col gap-2.5">
          <div className="flex items-center gap-2 pb-1.5 border-b border-line-soft">
            <BookOpen className="w-4 h-4 text-accent" />
            <span className="text-[13px] font-bold text-ink">Kapsamlı Ders Notu Sentezi</span>
          </div>
          <StructuredSynthesisRenderer text={narrative} />
        </div>
      )}

      {/* Key Bullets */}
      {c.keyBullets && c.keyBullets.length > 0 && (
        <KeyBulletsRenderer bullets={c.keyBullets} compact />
      )}

      {/* Formula / Box */}
      {c.formulaBox && (
        <div className="rounded-xl bg-accent-soft p-3 flex flex-col gap-1 border border-accent/20">
          <span className="text-[11.5px] font-semibold uppercase text-accent">{c.formulaBox.title}</span>
          <code className="font-mono text-[13px] text-ink">{c.formulaBox.formula}</code>
          {c.formulaBox.explanation && <span className="text-[12px] text-ink-2">{c.formulaBox.explanation}</span>}
        </div>
      )}

      {/* Table */}
      {c.table && (
        <EnhancedDifferentialTable table={c.table} compact />
      )}

      {/* Spot pearls */}
      {spots.length > 0 && (
        <SpotList items={spots} title="Bu slaytın spotları" compact />
      )}
    </div>
  );
};

const QuizCard: React.FC<{ q: SlideRelatedQuestion; n: number }> = ({ q, n }) => {
  const [picked, setPicked] = useState<string | null>(null);
  const [showExp, setShowExp] = useState(true);
  const answer = q.correctAnswer || q.options.find((o) => o.isCorrect)?.key || '';
  const done = picked !== null;
  const right = done && picked === answer;
  const isPractice =
    Boolean(q.isPracticeQuestion) ||
    Boolean(q.examYear && (q.examYear.includes('Çalışma') || q.examYear.includes('Özgün') || q.examYear.includes('Pekiştirme')));

  return (
    <article
      className={`rounded-xl border p-3 flex flex-col gap-2.5 transition-all shadow-2xs ${
        isPractice
          ? 'border-emerald-200 dark:border-emerald-900/40 bg-emerald-50/20 dark:bg-emerald-950/10'
          : 'border-blue-200 dark:border-blue-900/40 bg-blue-50/20 dark:bg-blue-950/10'
      }`}
    >
      <header className="flex items-center justify-between gap-2 text-[12px] text-ink-3 flex-wrap">
        <div className="flex items-center gap-1.5 min-w-0">
          <span
            className={`font-mono font-semibold px-1.5 py-0.5 rounded text-[11px] ${
              isPractice
                ? 'bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300'
                : 'bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-blue-300'
            }`}
          >
            S{n}
          </span>
          <span className="truncate font-medium text-ink-2">{[q.examYear, q.topic].filter(Boolean).join(' · ')}</span>
        </div>
        {isPractice ? (
          <span className="shrink-0 px-2 py-0.5 rounded-full text-[10.5px] font-bold bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-200 border border-emerald-300 dark:border-emerald-700 flex items-center gap-1 shadow-2xs">
            <Sparkles className="w-3 h-3 text-emerald-600 dark:text-emerald-400" />
            Özgün Çalışma Sorusu
          </span>
        ) : (
          <span className="shrink-0 px-2 py-0.5 rounded-full text-[10.5px] font-bold bg-blue-100 dark:bg-blue-900/60 text-blue-800 dark:text-blue-200 border border-blue-300 dark:border-blue-700 flex items-center gap-1 shadow-2xs">
            <GraduationCap className="w-3 h-3 text-blue-600 dark:text-blue-400" />
            Çıkmış Sınav Sorusu
          </span>
        )}
      </header>
      <p className="m-0 text-[14px] leading-[1.5] font-medium text-ink">{q.stem}</p>
      <div role="radiogroup" aria-label={`Soru ${n} şıkları`} className="flex flex-col gap-1.5">
        {q.options.map((o) => {
          const isAns = o.key === answer;
          const isPick = o.key === picked;
          const cls = !done
            ? 'border-line hover:border-accent bg-white dark:bg-surface-elevated'
            : isAns
              ? 'border-ok-bright bg-ok-tint dark:bg-ok/20 text-ok-bright'
              : isPick
                ? 'border-bad bg-bad-soft dark:bg-bad/20'
                : 'border-line bg-white dark:bg-surface-elevated opacity-70';
          return (
            <button
              key={o.key}
              type="button"
              role="radio"
              aria-checked={isPick}
              disabled={done}
              onClick={() => setPicked(o.key)}
              className={`w-full min-h-10 px-2.5 py-1.5 rounded-lg border text-left flex items-start gap-2 text-[13px] leading-snug transition-colors ${done ? 'cursor-default' : 'cursor-pointer'} ${cls}`}
            >
              <span className={`font-mono font-semibold shrink-0 ${done && isAns ? 'text-ok' : done && isPick ? 'text-bad-text' : 'text-ink-2'}`}>{o.key})</span>
              <span className="flex-1 text-ink">{o.text}</span>
              {done && isAns && <CheckCircle2 className="w-4 h-4 text-ok shrink-0 mt-0.5" />}
              {done && isPick && !isAns && <XCircle className="w-4 h-4 text-bad-text shrink-0 mt-0.5" />}
            </button>
          );
        })}
      </div>
      {done && (
        <div className={`rounded-lg px-2.5 py-2 text-[13px] ${right ? 'bg-ok-soft dark:bg-ok/20 border border-ok/30' : 'bg-bad-soft dark:bg-bad/20 border border-bad/30'}`}>
          <div className="flex items-center justify-between gap-2">
            <strong className={right ? 'text-ok dark:text-emerald-400' : 'text-bad-text dark:text-rose-400'}>{right ? '✓ Tebrikler, Doğru Yanıt!' : `✕ Yanlış. Doğru cevap ${answer}`}</strong>
            <span className="flex gap-1">
              {q.explanation && (
                <button type="button" onClick={() => setShowExp((v) => !v)} className="h-7 px-2 rounded-md text-[12px] font-semibold text-ink-2 hover:bg-white/70 dark:hover:bg-white/10 cursor-pointer">
                  {showExp ? 'Açıklamayı gizle' : 'Açıklama'}
                </button>
              )}
              <button type="button" onClick={() => setPicked(null)} className="h-7 px-2 rounded-md text-[12px] font-semibold text-ink-2 hover:bg-white/70 dark:hover:bg-white/10 cursor-pointer">
                Tekrar Dene
              </button>
            </span>
          </div>
          {showExp && q.explanation && <p className="m-0 mt-1.5 text-ink-2 dark:text-ink-muted leading-[1.55] whitespace-pre-line">{q.explanation.replace(/\n(?!\n)/g, ' ')}</p>}
        </div>
      )}
    </article>
  );
};

const formatAiModelDisplayName = (raw?: string | null): string => {
  if (!raw) return 'Google Gemini 3.8 Flash';
  const val = raw.trim();
  if (val.includes('3.8-flash')) return 'Google Gemini 3.8 Flash';
  if (val.includes('3.7-flash')) return 'Google Gemini 3.7 Flash';
  if (val.includes('3.5-flash-lite')) return 'Google Gemini 3.5 Flash Lite';
  if (val.includes('3.5-flash')) return 'Google Gemini 3.5 Flash';
  if (val.includes('3.1-flash-lite')) return 'Google Gemini 3.1 Flash Lite';
  if (val.includes('gpt-oss-120b')) return 'Groq GPT-OSS 120B';
  if (val.includes('gpt-oss-20b')) return 'Groq GPT-OSS 20B';
  if (val.includes('qwen')) return 'Groq Qwen 27B';
  if (val.includes('spark') || val.includes('muse')) return 'Muse Spark 1.3 Free';
  return val;
};

const AskAi: React.FC<{ deck: InteractiveDeck; slide: SlideItem }> = ({ deck, slide }) => {
  const [q, setQ] = useState('');
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState<string | null>(null);
  const [refs, setRefs] = useState<any[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>('gemini-3.8-flash');
  const [modelUsed, setModelUsed] = useState<string | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  const ask = async (prompt?: string) => {
    const text = (prompt ?? q).trim();
    if (!text) return;
    setQ(text);
    setLoading(true);
    setAnswer(null);
    setModelUsed(null);
    setRefs([]);
    const ctx = [
      `Ders: ${deck.title} (${deck.discipline} - ${deck.committee})`,
      `Öğretim üyesi: ${deck.instructor}`,
      `Slayt: ${slide.title} - ${slide.subtitle}`,
      slide.professorAudioHighlight ? `Hocanın vurgusu (${slide.professorAudioHighlight.timestamp}): "${slide.professorAudioHighlight.quote}"` : '',
      slide.synthesisNarrative ? `Ders ve amfi sentezi: ${slide.synthesisNarrative}` : '',
      ...(slide.coreContent?.keyBullets || []).map((b) => `- ${b.title}: ${b.desc}`),
      ...(slide.spotPearls || []).map((p: any) => `* ${typeof p === 'string' ? p : `${p?.badge ? p.badge + ' ' : ''}${p?.text || ''}`}`),
    ]
      .filter(Boolean)
      .join('\n');
    // 1. Try server RAG endpoint first
    try {
      // safeJsonFetch honours the custom API URL (GitHub Pages + tunnel setups)
      const res = await safeJsonFetch<any>('/api/rag/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: `${text}\n\n[Slayt ve ders bağlamı]:\n${ctx}`,
          discipline: deck.discipline,
          committeeId: deck.committee,
          mode: 'qa',
          limit: 4,
          customModel: selectedModel,
        }),
      });
      if (res.ok && res.data) {
        const data = res.data;
        if (data.answer) {
          setAnswer(data.answer);
          setModelUsed(data.usedModel || selectedModel);
          setRefs(data.references || []);
          setLoading(false);
          return;
        }
      }
    } catch {
      /* network failure or server error: fall back to resilient client AI below */
    }

    // 2. Resilient Client-Side Multi-Provider Fallback (Gemini Pool + Groq Cloud)
    try {
      const { callClientResilientAi } = await import('../../services/api');
      const aiPrompt = `Öğrencinin Sorusu: "${text}"\n\n[Ders ve Slayt Bağlamı]:\n${ctx}\n\nLütfen bu ders notu ve slayt bağlamına sadık kalarak net, açıklayıcı ve sınav odaklı bir yanıt ver.`;
      const isGroq = selectedModel.includes('gpt-oss') || selectedModel.includes('qwen') || selectedModel.includes('llama');
      const isMuse = selectedModel.includes('spark') || selectedModel.includes('muse');
      const preferredProvider = isMuse ? 'muse-spark' : (isGroq ? 'groq' : 'gemini');

      const clientRes = await callClientResilientAi({
        prompt: aiPrompt,
        model: selectedModel,
        preferredProvider,
        responseFormat: 'text',
        systemInstruction: 'Sen Tıp Fakültesi öğrencilerine ders slaytları üzerinden rehberlik eden kıdemli bir tıp akademisyenisin. Slayt içeriğine dayanarak doğru, net ve öğretici cevaplar ver.',
      });

      if (clientRes && clientRes.text) {
        setAnswer(clientRes.text);
        setModelUsed(clientRes.planUsed || clientRes.providerUsed || selectedModel);
        setRefs([
          { title: `${deck.title} — Slayt #${slide.slideNumber} (${deck.discipline})` }
        ]);
        setLoading(false);
        return;
      }
    } catch (clientErr: any) {
      console.warn('Client resilient AI fallback failed:', clientErr);
    }

    toast.error('AI yanıt veremedi', 'Bağlantı kurulamadı. Lütfen tekrar deneyin.', { label: 'Tekrar dene', onClick: () => ask(text) });
    setLoading(false);
  };

  const handleCopy = () => {
    if (!answer) return;
    const modelTag = modelUsed ? `\n\n[Yapay Zeka Modeli: ${formatAiModelDisplayName(modelUsed)}]` : '';
    navigator.clipboard.writeText(answer + modelTag);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
    toast.success('Yanıt kopyalandı', modelUsed ? `Yapay zeka modeli (${formatAiModelDisplayName(modelUsed)}) bilgisiyle panoya alındı.` : undefined);
  };

  return (
    <div className="flex flex-col gap-3">
      {(slide.aiPromptSuggestions || []).length > 0 && (
        <div className="flex flex-col gap-1.5">
          <span className="text-[12px] font-semibold text-ink-2 px-1">Hazır sorular</span>
          {slide.aiPromptSuggestions.map((s, i) => (
            <button
              key={i}
              type="button"
              disabled={loading}
              onClick={() => ask(s)}
              className="text-left rounded-lg border border-line px-2.5 py-2 text-[13px] leading-snug hover:border-accent cursor-pointer disabled:opacity-50 transition-colors"
            >
              {s}
            </button>
          ))}
        </div>
      )}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          ask();
        }}
        className="flex flex-col gap-2"
      >
        <div className="flex items-center justify-between gap-2 px-1">
          <label htmlFor="deck-ai-model-select" className="text-[12px] font-semibold text-ink-2 inline-flex items-center gap-1.5">
            <BrainCircuit className="w-3.5 h-3.5 text-accent" />
            <span>Yapay Zeka Modeli:</span>
          </label>
          <select
            id="deck-ai-model-select"
            value={selectedModel}
            disabled={loading}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="bg-white dark:bg-slate-800 border border-line-2 rounded-md px-2 py-0.5 text-[11.5px] font-medium text-ink outline-none cursor-pointer focus:border-accent disabled:opacity-50"
          >
            <option value="gemini-3.8-flash">Google Gemini 3.8 Flash (Önerilen)</option>
            <option value="gemini-3.7-flash">Google Gemini 3.7 Flash</option>
            <option value="gemini-3.5-flash">Google Gemini 3.5 Flash</option>
            <option value="openai/gpt-oss-120b">Groq GPT-OSS 120B</option>
            <option value="qwen/qwen3.8-27b">Groq Qwen 27B (Türkçe)</option>
            <option value="muse-spark-1.3-contributor-free">Muse Spark 1.3 Free</option>
          </select>
        </div>
        <label htmlFor="deck-ai-q" className="sr-only">
          Sorunu yaz
        </label>
        <textarea
          id="deck-ai-q"
          rows={3}
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Bu slayt ve ders notuyla ilgili sorunu yaz…"
          className="resize-none border border-line-2 rounded-[10px] px-3 py-2.5 text-[14px] bg-field outline-0 focus:border-accent"
        />
        <button
          type="submit"
          disabled={loading || !q.trim()}
          className="h-10 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-[14px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
        >
          {loading ? <Sparkles className="w-4 h-4 animate-pulse" /> : <Send className="w-4 h-4" />}
          {loading ? 'Yanıt hazırlanıyor…' : 'Sor'}
        </button>
      </form>
      {loading && <AiThinking />}
      {answer && (
        <div className="rounded-xl bg-accent-soft border border-accent/20 p-3.5 flex flex-col gap-2.5 shadow-2xs" role="status">
          <div className="flex items-center justify-between gap-2 flex-wrap border-b border-accent/15 pb-2">
            <span className="inline-flex items-center gap-1.5 text-[12.5px] font-bold text-accent">
              <Sparkles className="w-3.5 h-3.5" /> AI Yanıtı
            </span>
            {modelUsed && (
              <span
                className="inline-flex items-center gap-1.5 text-[11px] font-medium bg-white/95 dark:bg-slate-800 text-ink-2 px-2.5 py-0.5 rounded-full border border-accent/25 shadow-2xs"
                title={`Bu yanıtı üreten yapay zeka: ${modelUsed}`}
              >
                <Bot className="w-3.5 h-3.5 text-accent shrink-0" />
                <span className="text-ink-3">Model:</span>
                <span className="font-semibold text-accent font-mono">{formatAiModelDisplayName(modelUsed)}</span>
              </span>
            )}
          </div>
          <div className="text-[14px] leading-[1.65] text-ink whitespace-pre-line">
            <Rich text={answer.replace(/^#+\s*/gm, '').replace(/^>\s?/gm, '')} />
          </div>
          {refs.length > 0 && (
            <ul className="list-none m-0 p-0 flex flex-col gap-1 border-t border-accent/15 pt-2">
              {refs.slice(0, 4).map((r: any, i: number) => (
                <li key={i} className="text-[11.5px] text-ink-2 truncate flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-accent shrink-0" />
                  <span>{r.title || r.noteTitle || r.source || `Kaynak ${i + 1}`}</span>
                </li>
              ))}
            </ul>
          )}
          <div className="flex items-center justify-between gap-2 pt-2 border-t border-accent/15 text-[11px] text-ink-3">
            {modelUsed && (
              <span className="inline-flex items-center gap-1 text-[11px] text-ink-2">
                <span>Kullanılan Yapay Zeka:</span>
                <strong className="text-ink font-mono font-medium">{formatAiModelDisplayName(modelUsed)}</strong>
              </span>
            )}
            <button
              type="button"
              onClick={handleCopy}
              className="inline-flex items-center gap-1 text-[11.5px] text-ink-2 hover:text-ink cursor-pointer px-2 py-0.5 rounded hover:bg-white/60 dark:hover:bg-white/10 transition-colors ml-auto"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-ok" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Kopyalandı' : 'Kopyala'}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
