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
} from 'lucide-react';
import interactiveDecksData from '../../data/interactive_learning_decks.json';

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
  front: string;
  back: string;
  hint?: string;
}

export interface SlideQuestionOption {
  key: string;
  text: string;
  isCorrect?: boolean;
}

export interface SlideRelatedQuestion {
  id: string;
  examYear: string;
  committeeId: string;
  discipline: string;
  topic: string;
  stem: string;
  options: SlideQuestionOption[];
  correctAnswer: string;
  explanation: string;
  matchScore?: number;
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
  onOpenPdfModal?: () => void;
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

/** Renders rich text segments with bolding, sub-details, and code styling. */
const Rich: React.FC<{ text: string; className?: string }> = ({ text, className }) => {
  const parts = String(text || '').split(/(\*\*[^*]+\*\*)/g);
  return (
    <span className={className}>
      {parts.map((p, i) =>
        p.startsWith('**') && p.endsWith('**') ? (
          <strong
            key={i}
            className="font-bold text-ink bg-amber-100/60 dark:bg-amber-950/40 px-1 py-0.5 rounded shadow-2xs"
          >
            {p.slice(2, -2)}
          </strong>
        ) : (
          <React.Fragment key={i}>{p}</React.Fragment>
        )
      )}
    </span>
  );
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

        // Callout (> veya 💡 veya ⚠️)
        if (line.startsWith('> ') || line.startsWith('💡 ') || line.startsWith('⚠️ ')) {
          // One icon only: take it from the line itself (💡 / ⚠️) and strip it from the text
          const icon = line.startsWith('⚠️') ? '⚠️' : '💡';
          const content = (line.startsWith('> ') ? line.slice(2) : line).replace(/^\s*(💡|⚠️)\s*/u, '');
          return (
            <div
              key={idx}
              className="p-2.5 sm:p-3 my-1 rounded-xl bg-accent-soft/30 border-l-3 border-accent text-[12px] sm:text-[12.5px] text-ink leading-relaxed flex items-center gap-2.5 shadow-2xs"
            >
              <span className="text-[14px] select-none shrink-0" aria-hidden="true">{icon}</span>
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
      aria-label={`${card.front} akıl kartı`}
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
              {card.front}
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
            <Rich text={card.back} />
          </div>
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Hub (deck catalogue)
// ---------------------------------------------------------------------------
export const InteractiveDeckView: React.FC<InteractiveDeckViewProps> = ({ initialDeckId, initialSlideNumber, onDeckChange }) => {
  const allDecks = useMemo(
    () => ((interactiveDecksData as unknown as InteractiveDeck[]) || []).filter((d) => d && Array.isArray(d.slides) && d.slides.length > 0),
    []
  );
  const [deckId, setDeckId] = useState<string | null>(initialDeckId || null);

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
    allDecks.forEach((d) => (m[d.discipline] = (m[d.discipline] || 0) + 1));
    return Object.entries(m).sort((a, b) => a[0].localeCompare(b[0], 'tr'));
  }, [allDecks]);

  const visible = useMemo(() => {
    const q = query.trim().toLocaleLowerCase('tr-TR');
    return allDecks.filter((d) => {
      if (discipline !== 'all' && d.discipline !== discipline) return false;
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

      <div role="radiogroup" aria-label="Ders" className="flex gap-1.5 overflow-x-auto no-scrollbar -mx-3 px-3 sm:mx-0 sm:px-0">
        {[['all', allDecks.length] as [string, number], ...disciplines].map(([d, n]) => {
          const on = discipline === d;
          const dot = d === 'all' ? '#0E1A26' : tone(allDecks.find((x) => x.discipline === d)?.themeColor).fg;
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
      </div>

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
            const t = tone(d.themeColor);
            return (
              <li key={d.id} className="min-w-0">
                <button
                  type="button"
                  onClick={() => {
                    setDeckId(d.id);
                    onDeckChange?.(d.id);
                  }}
                  className="w-full h-full text-left bg-white border border-line rounded-[16px] p-4 flex flex-col gap-2.5 cursor-pointer hover:border-accent hover:shadow-[0_6px_20px_rgba(14,26,38,0.06)] transition-all group"
                >
                  <span className="flex items-center gap-2 min-w-0 text-[12.5px] text-ink-3">
                    <span className="w-2 h-2 rounded-full shrink-0" style={{ background: t.fg }} aria-hidden="true" />
                    <span className="truncate">{d.discipline}</span>
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
                    <span
                      className={`h-[34px] px-3 rounded-[10px] inline-flex items-center gap-1.5 text-[13px] font-semibold shrink-0 ${
                        started ? 'bg-accent text-white' : 'bg-accent-soft text-accent'
                      }`}
                    >
                      <Play className="w-3 h-3 fill-current" />
                      {done ? 'Tekrar' : started ? 'Devam et' : 'Başla'}
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
        />
      )}
    </div>
  );
};

// ---------------------------------------------------------------------------
// Player: full-viewport overlay, paged or scrolling, optional native fullscreen
// ---------------------------------------------------------------------------
type PanelTab = 'flashcards' | 'questions' | 'notes' | 'pearls' | 'ai';

const DeckPlayer: React.FC<{
  deck: InteractiveDeck;
  startAt: number;
  onProgress: (index: number) => void;
  onClose: () => void;
}> = ({ deck, startAt, onProgress, onClose }) => {
  const slides = deck.slides;
  const n = slides.length;
  const [index, setIndex] = useState(() => Math.min(Math.max(0, startAt), n - 1));
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
  const rootRef = useRef<HTMLDivElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const sectionRefs = useRef<(HTMLElement | null)[]>([]);
  const stripRef = useRef<HTMLDivElement>(null);
  const programmatic = useRef(false);
  const touch = useRef<{ x: number; y: number } | null>(null);

  const slide = slides[index];

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
    if (!touch.current || mode !== 'paged') return;
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

        <span className="hidden sm:inline font-mono text-[13px] text-ink-2 px-1" aria-live="polite">
          {index + 1} / {n}
        </span>
        <div role="radiogroup" aria-label="Görünüm" className="flex items-center h-9 bg-canvas rounded-[10px] p-0.5">
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
              className={`h-8 px-2 sm:px-2.5 rounded-lg inline-flex items-center gap-1.5 text-[13px] cursor-pointer ${
                mode === id ? 'bg-white text-accent font-semibold shadow-[0_1px_2px_rgba(14,26,38,0.1)]' : 'text-ink-2 hover:text-ink'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span className="hidden md:inline">{label}</span>
            </button>
          ))}
        </div>
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
          {mode === 'paged' ? (
            <div className="absolute inset-0 p-2 sm:p-4 lg:p-6 flex" onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
              <SlideCanvas
                key={index}
                slide={slide}
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
      // 2. Synthesis Narrative
      if (slide.synthesisNarrative && slide.synthesisNarrative.toLocaleLowerCase('tr-TR').includes(queryNorm)) {
        const idx = slide.synthesisNarrative.toLocaleLowerCase('tr-TR').indexOf(queryNorm);
        const start = Math.max(0, idx - 40);
        const end = Math.min(slide.synthesisNarrative.length, idx + queryNorm.length + 80);
        matches.push({
          slideIndex: sIdx,
          slideNumber: slide.slideNumber,
          slideTitle: slide.title,
          matchedType: 'Ders Notu Sentezi',
          snippet: (start > 0 ? '...' : '') + slide.synthesisNarrative.slice(start, end) + (end < slide.synthesisNarrative.length ? '...' : ''),
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
        (fc) => fc.front.toLocaleLowerCase('tr-TR').includes(queryNorm) || fc.back.toLocaleLowerCase('tr-TR').includes(queryNorm)
      );
      if (foundCard) {
        matches.push({
          slideIndex: sIdx,
          slideNumber: slide.slideNumber,
          slideTitle: slide.title,
          matchedType: 'Akıl Kartı',
          snippet: `Soru: ${foundCard.front} -> ${foundCard.back.slice(0, 110)}...`,
        });
        return;
      }
      // 5. Spot Pearls
      const foundPearl = (slide.spotPearls || []).find((p) => p.toLocaleLowerCase('tr-TR').includes(queryNorm));
      if (foundPearl) {
        matches.push({
          slideIndex: sIdx,
          slideNumber: slide.slideNumber,
          slideTitle: slide.title,
          matchedType: 'Spot İnci',
          snippet: foundPearl,
        });
        return;
      }
      // 6. Questions
      const foundQ = (slide.relatedQuestions || []).find(
        (rq) => rq.stem.toLocaleLowerCase('tr-TR').includes(queryNorm) || rq.explanation.toLocaleLowerCase('tr-TR').includes(queryNorm)
      );
      if (foundQ) {
        matches.push({
          slideIndex: sIdx,
          slideNumber: slide.slideNumber,
          slideTitle: slide.title,
          matchedType: 'Çıkmış Soru',
          snippet: foundQ.stem.slice(0, 130) + '...',
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
}> = ({ slide, index, total, onOpenQuestions, onOpenFlashcards, onOpenNotes, onNext, paged = false }) => {
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
      className={`w-full ${paged ? 'h-full overflow-y-auto overscroll-contain' : 'min-h-full'} max-w-[1280px] mx-auto bg-white border border-line rounded-[18px] shadow-[0_2px_16px_rgba(14,26,38,0.06)] flex flex-col min-h-0 custom-scrollbar`}
    >
      <div className="px-4 py-4 sm:px-6 sm:py-5 lg:px-8 lg:py-6 flex flex-col gap-4 sm:gap-6">
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
        {slide.synthesisNarrative && (
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
            
            <StructuredSynthesisRenderer text={slide.synthesisNarrative} />

            {/* Comparison / Classification Table on Slide Canvas */}
            {c.table && (
              <div className="rounded-xl border border-line overflow-hidden bg-white mt-2 shadow-2xs">
                {c.table.title && (
                  <div className="px-3 py-2 bg-gradient-to-r from-canvas via-white to-canvas text-[12px] font-bold border-b border-line text-ink flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                    <span>{c.table.title}</span>
                  </div>
                )}
                <div className="overflow-x-auto">
                  <table className="w-full text-[12px] border-collapse">
                    <thead>
                      <tr className="bg-canvas/80">
                        {c.table.headers.map((h, i) => (
                          <th key={i} className="text-left font-semibold text-ink-2 px-3 py-2 border-b border-line">
                            {h}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {c.table.rows.map((row, ri) => (
                        <tr key={ri} className="border-b border-line-soft last:border-0 hover:bg-canvas/30 transition-colors">
                          {row.map((cell, ci) => (
                            <td key={ci} className={`px-3 py-2 ${ci === 0 ? 'font-semibold text-ink' : 'text-ink-2'}`}>
                              <Rich text={cell} />
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
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

        {/* 5. High-yield action bar (Questions, Flashcards, Notes) */}
        <div className="rounded-xl border border-line bg-gradient-to-r from-accent-soft/20 via-white to-transparent p-2.5 sm:p-3 flex items-center justify-between gap-3 flex-wrap">
          <div className="flex items-center gap-2 text-[12px] sm:text-[12.5px] font-medium text-ink-2">
            <Sparkles className="w-3.5 h-3.5 text-accent shrink-0" />
            <span>Bu konu için <strong>{flashcards.length} akıl kartı</strong> ve <strong>{(slide.relatedQuestions || []).length} çıkmış soru</strong> slayt üzerine yerleştirildi.</span>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            {flashcards.length > 0 && onOpenFlashcards && (
              <button
                type="button"
                onClick={onOpenFlashcards}
                className="shrink-0 whitespace-nowrap h-7.5 px-2.5 rounded-lg bg-amber-500 hover:bg-amber-600 text-white text-[11.5px] font-semibold inline-flex items-center gap-1 cursor-pointer transition-colors"
              >
                <BrainCircuit className="w-3.5 h-3.5" />
                <span>Akıl Kartları ({flashcards.length})</span>
              </button>
            )}
            {(slide.relatedQuestions || []).length > 0 && (
              <button
                type="button"
                onClick={() => {
                  const el = document.getElementById(`slide-questions-${slide.slideNumber}`);
                  if (el) {
                    el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                  } else if (onOpenQuestions) {
                    onOpenQuestions();
                  }
                }}
                className="shrink-0 whitespace-nowrap h-7.5 px-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-[11.5px] font-semibold inline-flex items-center gap-1 cursor-pointer transition-colors shadow-2xs"
              >
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Çıkmış Sorular ({(slide.relatedQuestions || []).length})</span>
              </button>
            )}
            {onOpenNotes && (
              <button
                type="button"
                onClick={onOpenNotes}
                className="shrink-0 whitespace-nowrap h-7.5 px-2.5 rounded-lg bg-white border border-line text-ink-2 hover:text-ink text-[11.5px] font-semibold inline-flex items-center gap-1 cursor-pointer transition-colors"
              >
                <BookOpen className="w-3.5 h-3.5 text-accent" />
                <span>Ders Notu Özeti</span>
              </button>
            )}
          </div>
        </div>

        {/* 6. Core content: formulas, tables, bullets, infographics */}
        <div className={`grid grid-cols-1 ${c.table && c.table.headers?.length > 0 ? '' : 'lg:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)]'} gap-4 sm:gap-5 lg:gap-7 items-start`}>
          {/* Main content */}
          <div className="flex flex-col gap-4 min-w-0">
            {c.keyBullets && c.keyBullets.length > 0 && (
              <ol className="list-none m-0 p-0 flex flex-col gap-2">
                {c.keyBullets.map((b, i) => (
                  <li key={i} className={`grid grid-cols-[24px_minmax(0,1fr)] gap-2.5 items-start ${b.isKey ? 'bg-accent-soft/50 rounded-xl p-2 -m-1.5' : ''}`}>
                    <span className="w-6 h-6 rounded-lg bg-accent-soft text-accent font-mono text-[11px] font-semibold flex items-center justify-center">{i + 1}</span>
                    <span className="flex flex-col gap-0.5 min-w-0">
                      <span className="text-[13.5px] sm:text-[14px] font-semibold leading-snug">{b.title}</span>
                      <Rich text={b.desc} className="text-[12.5px] sm:text-[13px] text-ink-2 leading-[1.6]" />
                    </span>
                  </li>
                ))}
              </ol>
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
              <div className="rounded-xl border border-line overflow-hidden">
                {c.table.title && <div className="px-3 py-2 bg-canvas text-[13px] font-semibold border-b border-line">{c.table.title}</div>}
                <div className="overflow-x-auto">
                  <table className={`w-full border-collapse ${c.table.headers.length >= 4 ? 'text-[12.5px] sm:text-[13px]' : 'text-[13px] sm:text-[14px]'}`}>
                    <thead>
                      <tr className="bg-[#FAFBFC]">
                        {c.table.headers.map((h, i) => (
                          <th key={i} scope="col" className="text-left font-semibold text-ink-2 px-3 py-2 border-b border-line align-bottom break-words">
                            {h}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {c.table.rows.map((r, ri) => (
                        <tr key={ri} className="border-b border-line-soft last:border-0 align-top">
                          {r.map((cell, ci) => (
                            <td key={ci} className={`px-3 py-2 break-words leading-[1.5] ${ci === 0 ? 'font-semibold text-ink' : 'text-ink-2'}`}>
                              <Rich text={cell} />
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>

          {/* Side: spot pearls */}
          <div className="flex flex-col gap-3 min-w-0">
            {slide.spotPearls?.length > 0 && (
              <div className="rounded-xl border border-line p-3.5 sm:p-4 flex flex-col gap-2 bg-[#FAFBFC]">
                <span className="text-[12px] font-semibold uppercase tracking-[0.06em] text-ink-2">Akılda Tutulacak Spotlar</span>
                <ul className="list-none m-0 p-0 flex flex-col gap-2">
                  {slide.spotPearls.map((p, i) => (
                    <li key={i} className="grid grid-cols-[16px_minmax(0,1fr)] gap-2 text-[14px] leading-[1.5]">
                      <CheckCircle2 className="w-4 h-4 text-ok mt-0.5" />
                      <Rich text={p} />
                    </li>
                  ))}
                </ul>
              </div>
            )}
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
      </div>
    </article>
  );
};

// ---------------------------------------------------------------------------
// Interaction panel: flashcards, questions, structured notes, deck pearls, ask AI
// ---------------------------------------------------------------------------
const InteractionPanel: React.FC<{
  deck: InteractiveDeck;
  slide: SlideItem;
  tab: PanelTab;
  setTab: (t: PanelTab) => void;
}> = ({ deck, slide, tab, setTab }) => {
  const qs = slide.relatedQuestions || [];
  const cards = slide.flashcards || [];

  const tabs: { id: PanelTab; label: string }[] = [
    { id: 'flashcards', label: `Kartlar ${cards.length}` },
    { id: 'questions', label: `Sorular ${qs.length}` },
    { id: 'notes', label: 'Ders Notu' },
    { id: 'pearls', label: 'Spotlar' },
    { id: 'ai', label: "AI'ya sor" },
  ];

  return (
    <>
      <div role="tablist" aria-label="Etkileşim" className="shrink-0 grid grid-cols-5 gap-1 m-3 mb-0 bg-canvas rounded-[12px] p-1">
        {tabs.map((t) => (
          <button
            key={t.id}
            type="button"
            role="tab"
            aria-selected={tab === t.id}
            onClick={() => setTab(t.id)}
            className={`h-9 rounded-[9px] text-[12px] cursor-pointer truncate ${tab === t.id ? 'bg-white text-ink font-semibold shadow-[0_1px_2px_rgba(14,26,38,0.08)]' : 'text-ink-2 hover:text-ink'}`}
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
            <p className="m-0 text-[14px] text-ink-2 px-1 py-4">Bu slayta eşleşen çıkmış soru yok.</p>
          ) : (
            qs.map((q, i) => <QuizCard key={`${slide.slideNumber}-${q.id}`} q={q} n={i + 1} />)
          ))}
        {tab === 'notes' && <SlideNotesTab slide={slide} />}
        {tab === 'pearls' && (
          <div className="flex flex-col gap-2">
            <p className="m-0 text-[13px] text-ink-2 px-1">{deck.title} dersinin tamamından yüksek verimli bilgiler.</p>
            <ul className="list-none m-0 p-0 flex flex-col gap-2">
              {(deck.highYieldPearls || []).map((p, i) => (
                <li key={i} className="rounded-xl border border-line p-3 text-[14px] leading-[1.55] text-ink-2">
                  <Rich text={p} />
                </li>
              ))}
            </ul>
          </div>
        )}
        {tab === 'ai' && <AskAi key={slide.slideNumber} deck={deck} slide={slide} />}
      </div>
    </>
  );
};

// ---------------------------------------------------------------------------
// Slide Notes Tab: Structured medical textbook notes and tables for the slide
// ---------------------------------------------------------------------------
const SlideNotesTab: React.FC<{ slide: SlideItem }> = ({ slide }) => {
  const c = slide.coreContent || {};
  return (
    <div className="flex flex-col gap-3.5">
      {/* Narrative block */}
      {slide.synthesisNarrative && (
        <div className="rounded-xl border border-line bg-gradient-to-br from-blue-50/50 via-white to-indigo-50/20 p-3.5 flex flex-col gap-2.5">
          <div className="flex items-center gap-2 pb-1.5 border-b border-line-soft">
            <BookOpen className="w-4 h-4 text-accent" />
            <span className="text-[13px] font-bold text-ink">Kapsamlı Ders Notu Sentezi</span>
          </div>
          <StructuredSynthesisRenderer text={slide.synthesisNarrative} />
        </div>
      )}

      {/* Key Bullets */}
      {c.keyBullets && c.keyBullets.length > 0 && (
        <div className="rounded-xl border border-line p-3.5 bg-white flex flex-col gap-2.5">
          <span className="text-[12px] font-semibold uppercase tracking-wider text-ink-3">Önemli Klinik & Patolojik Maddeler</span>
          <div className="flex flex-col gap-2">
            {c.keyBullets.map((b, i) => (
              <div key={i} className="text-[13px] leading-snug">
                <span className="font-semibold text-ink">{b.title}: </span>
                <Rich text={b.desc} className="text-ink-2" />
              </div>
            ))}
          </div>
        </div>
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
        <div className="rounded-xl border border-line overflow-hidden bg-white">
          {c.table.title && (
            <div className="px-3 py-1.5 bg-canvas text-[12px] font-semibold border-b border-line text-ink">
              {c.table.title}
            </div>
          )}
          <div className="overflow-x-auto">
            <table className="w-full text-[12px] border-collapse">
              <thead>
                <tr className="bg-canvas">
                  {c.table.headers.map((h, i) => (
                    <th key={i} className="text-left font-semibold text-ink-2 px-2.5 py-1.5 border-b border-line">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {c.table.rows.map((row, ri) => (
                  <tr key={ri} className="border-b border-line-soft last:border-0">
                    {row.map((cell, ci) => (
                      <td key={ci} className={`px-2.5 py-1.5 ${ci === 0 ? 'font-semibold text-ink' : 'text-ink-2'}`}>
                        <Rich text={cell} />
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Spot pearls */}
      {slide.spotPearls && slide.spotPearls.length > 0 && (
        <div className="rounded-xl border border-line p-3 bg-canvas/60 flex flex-col gap-2">
          <span className="text-[11.5px] font-semibold uppercase tracking-wider text-ink-3">Bu Slaytın Spot İnci Bilgileri</span>
          <ul className="list-none m-0 p-0 flex flex-col gap-1.5">
            {slide.spotPearls.map((p, i) => (
              <li key={i} className="flex items-start gap-2 text-[12.5px] text-ink-2 leading-relaxed">
                <CheckCircle2 className="w-3.5 h-3.5 text-ok shrink-0 mt-0.5" />
                <Rich text={p} />
              </li>
            ))}
          </ul>
        </div>
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
  return (
    <article className="rounded-xl border border-line p-3 flex flex-col gap-2.5">
      <header className="flex items-center gap-2 text-[12px] text-ink-3">
        <span className="font-mono font-semibold text-accent">S{n}</span>
        <span className="truncate">{[q.examYear, q.topic].filter(Boolean).join(' · ')}</span>
      </header>
      <p className="m-0 text-[14px] leading-[1.5] font-medium">{q.stem}</p>
      <div role="radiogroup" aria-label={`Soru ${n} şıkları`} className="flex flex-col gap-1.5">
        {q.options.map((o) => {
          const isAns = o.key === answer;
          const isPick = o.key === picked;
          const cls = !done
            ? 'border-line hover:border-accent bg-white'
            : isAns
              ? 'border-ok-bright bg-ok-tint'
              : isPick
                ? 'border-bad bg-bad-soft'
                : 'border-line bg-white opacity-70';
          return (
            <button
              key={o.key}
              type="button"
              role="radio"
              aria-checked={isPick}
              disabled={done}
              onClick={() => setPicked(o.key)}
              className={`w-full min-h-10 px-2.5 py-1.5 rounded-lg border text-left flex items-start gap-2 text-[13px] leading-snug ${done ? 'cursor-default' : 'cursor-pointer'} ${cls}`}
            >
              <span className={`font-mono font-semibold shrink-0 ${done && isAns ? 'text-ok' : done && isPick ? 'text-bad-text' : 'text-ink-2'}`}>{o.key})</span>
              <span className="flex-1">{o.text}</span>
              {done && isAns && <CheckCircle2 className="w-4 h-4 text-ok shrink-0" />}
              {done && isPick && !isAns && <XCircle className="w-4 h-4 text-bad-text shrink-0" />}
            </button>
          );
        })}
      </div>
      {done && (
        <div className={`rounded-lg px-2.5 py-2 text-[13px] ${right ? 'bg-ok-soft' : 'bg-bad-soft'}`}>
          <div className="flex items-center justify-between gap-2">
            <strong className={right ? 'text-ok' : 'text-bad-text'}>{right ? 'Doğru' : `Doğru cevap ${answer}`}</strong>
            <span className="flex gap-1">
              {q.explanation && (
                <button type="button" onClick={() => setShowExp((v) => !v)} className="h-7 px-2 rounded-md text-[12px] font-semibold text-ink-2 hover:bg-white/70 cursor-pointer">
                  {showExp ? 'Açıklamayı gizle' : 'Açıklama'}
                </button>
              )}
              <button type="button" onClick={() => setPicked(null)} className="h-7 px-2 rounded-md text-[12px] font-semibold text-ink-2 hover:bg-white/70 cursor-pointer">
                Tekrar
              </button>
            </span>
          </div>
          {showExp && q.explanation && <p className="m-0 mt-1.5 text-ink-2 leading-[1.55] whitespace-pre-line">{q.explanation.replace(/\n(?!\n)/g, ' ')}</p>}
        </div>
      )}
    </article>
  );
};

const AskAi: React.FC<{ deck: InteractiveDeck; slide: SlideItem }> = ({ deck, slide }) => {
  const [q, setQ] = useState('');
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState<string | null>(null);
  const [refs, setRefs] = useState<any[]>([]);

  const ask = async (prompt?: string) => {
    const text = (prompt ?? q).trim();
    if (!text) return;
    setQ(text);
    setLoading(true);
    setAnswer(null);
    setRefs([]);
    const ctx = [
      `Ders: ${deck.title} (${deck.discipline} - ${deck.committee})`,
      `Öğretim üyesi: ${deck.instructor}`,
      `Slayt: ${slide.title} - ${slide.subtitle}`,
      slide.professorAudioHighlight ? `Hocanın vurgusu (${slide.professorAudioHighlight.timestamp}): "${slide.professorAudioHighlight.quote}"` : '',
      slide.synthesisNarrative ? `Ders ve amfi sentezi: ${slide.synthesisNarrative}` : '',
      ...(slide.coreContent?.keyBullets || []).map((b) => `- ${b.title}: ${b.desc}`),
      ...(slide.spotPearls || []).map((p) => `* ${p}`),
    ]
      .filter(Boolean)
      .join('\n');
    try {
      const res = await fetch('/api/rag/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: `${text}\n\n[Slayt ve ders bağlamı]:\n${ctx}`, discipline: deck.discipline, committeeId: deck.committee, mode: 'qa', limit: 4 }),
      });
      if (res.ok && res.headers.get('content-type')?.includes('application/json')) {
        const data = await res.json();
        if (data.answer) {
          setAnswer(data.answer);
          setRefs(data.references || []);
          setLoading(false);
          return;
        }
      }
    } catch {
      /* offline: fall through to the slide-based answer */
    }
    const hl = slide.professorAudioHighlight;
    setAnswer(
      [
        `Sunucuya ulaşılamadı; bu slaytın kendi notlarından bir özet:`,
        hl ? `Hoca ${hl.timestamp} dakikasında: "${hl.quote}"` : '',
        slide.synthesisNarrative ? `Sentez: ${slide.synthesisNarrative}` : '',
        ...(slide.spotPearls || []).map((p) => `• ${p}`),
      ]
        .filter(Boolean)
        .join('\n\n')
    );
    setLoading(false);
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
              className="text-left rounded-lg border border-line px-2.5 py-2 text-[13px] leading-snug hover:border-accent cursor-pointer disabled:opacity-50"
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
        <label htmlFor="deck-ai-q" className="sr-only">
          Sorunu yaz
        </label>
        <textarea
          id="deck-ai-q"
          rows={3}
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Bu slaytla ilgili sorunu yaz…"
          className="resize-none border border-line-2 rounded-[10px] px-3 py-2.5 text-[14px] bg-field outline-0 focus:border-accent"
        />
        <button
          type="submit"
          disabled={loading || !q.trim()}
          className="h-10 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-[14px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
        >
          {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          {loading ? 'Yanıt hazırlanıyor…' : 'Sor'}
        </button>
      </form>
      {answer && (
        <div className="rounded-xl bg-accent-soft p-3 flex flex-col gap-2" role="status">
          <span className="inline-flex items-center gap-1.5 text-[12px] font-semibold text-accent">
            <Sparkles className="w-3.5 h-3.5" /> Yanıt
          </span>
          <div className="text-[14px] leading-[1.6] text-ink whitespace-pre-line">
            <Rich text={answer.replace(/^#+\s*/gm, '').replace(/^>\s?/gm, '')} />
          </div>
          {refs.length > 0 && (
            <ul className="list-none m-0 p-0 flex flex-col gap-1 border-t border-white/60 pt-2">
              {refs.slice(0, 4).map((r: any, i: number) => (
                <li key={i} className="text-[12px] text-ink-2 truncate">
                  {r.title || r.noteTitle || r.source || `Kaynak ${i + 1}`}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};
