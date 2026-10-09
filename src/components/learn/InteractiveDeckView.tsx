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
  ArrowRight,
  Bot,
  Columns,
  Cloud,
  Compass,
  Lock,
  ListTree,
} from 'lucide-react';
import { DeckPdfViewer } from './DeckPdfViewer';
import { PageHeader } from '../ui/PageHeader';
import { useUiVersion } from '../../utils/uiVersion';
import { getDeckOriginalPdf } from '../../data/deckPdfCatalog';
import { getSlidePdfLocation, SlidePdfLocation } from '../../services/slidePdfMappingService';
import { DECK_CATALOG, loadDeck, type DeckCatalogEntry } from '../../data/deckStore';
import {
  GlossaryProvider,
  RenderWithGlossaryTerms,
  SlideTermsPills,
  useGlossary,
} from './MedicalGlossaryPopover';
import { AiThinking } from '../ui/Animations';
import { HighlighterToolbar, Highlightable, isPenActive, usePenActive, stopPen } from '../ui/Highlighter';
import { SlideDrawingCanvas, DrawingModeToolbarTrigger, useDrawingGlobalState, setDrawingGlobalState } from './SlideDrawingCanvas';
import { toast } from '../ui/Toast';
import { safeJsonFetch } from '../../services/api';
import { QuestionFocus, focusMarks } from '../../services/questionFocus';
import { InteractiveStepRenderer } from './InteractiveStepElements';
import { LessonPlayer } from './lesson/LessonPlayer';
import { LearnHub, touchRecent } from './LearnHub';

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
  subtopic?: string;
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

export interface SlideMedicalTerm {
  term: string;
  explanation: string;
}

export interface SlideLayoutBlock {
  id: string;
  type:
    | 'header'
    | 'professor_pearl'
    | 'narrative'
    | 'key_bullets'
    | 'table'
    | 'medical_terms'
    | 'interactive_element'
    | 'spot_pearls'
    | 'flashcards'
    | 'related_questions';
  order: number;
  visible?: boolean;
  styleConfig?: {
    size?: 'compact' | 'normal' | 'large';
    tone?: 'default' | 'accent' | 'amber' | 'emerald' | 'rose' | 'indigo' | 'teal' | 'violet';
    title?: string;
    containerClass?: string;
    borderStyle?: 'solid' | 'dashed' | 'subtle' | 'none';
  };
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
  medicalTerms?: SlideMedicalTerm[];
  interactiveElement?: any;
  interactiveElements?: any[];
  layoutBlocks?: SlideLayoutBlock[];
  sourcePdf?: {
    fileName: string;
    fileId?: string;
    startPage: number;
    endPage: number;
    primaryPage: number;
    citation: string;
  };
  sourcePage?: number;
  sourcePageRange?: [number, number];
  sourceCitation?: string;
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
  /** Çıkmış sorudan gelindiyse: sorunun ifadeleri ve doğru şık slaytta işaretlenir */
  questionFocus?: QuestionFocus | null;
  onClearQuestionFocus?: () => void;
  isAdmin?: boolean;
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

  // Ham LaTeX ve matematiksel ifadelerin (örn. $\times$, $\ge$, $\to$) temizlenmesi
  const clean = text
    .replace(/\$\\times\$/g, '×')
    .replace(/\\times\b/g, '×')
    .replace(/\$\\to\$/g, '→')
    .replace(/\\to\b/g, '→')
    .replace(/\$\\rightarrow\$/g, '→')
    .replace(/\\rightarrow\b/g, '→')
    .replace(/\$\\ge\s*(\d+)/g, '≥ $1')
    .replace(/\$\\ge\$/g, '≥')
    .replace(/\\ge\b/g, '≥')
    .replace(/\$\\le\s*(\d+)/g, '≤ $1')
    .replace(/\$\\le\$/g, '≤')
    .replace(/\\le\b/g, '≤')
    .replace(/\$\\pm\$/g, '±')
    .replace(/\\pm\b/g, '±')
    .replace(/\$\\approx\$/g, '≈')
    .replace(/\\approx\b/g, '≈')
    .replace(/\$\/\\mu\s*L\$/gi, '/µL')
    .replace(/\$\\mu\s*L\$/gi, 'µL')
    .replace(/\\mu\s*L\b/gi, 'µL')
    .replace(/\$([a-zA-Z0-9_+^–-]+)\$/g, '$1');

  // Satırları gruplayalım: tabloları ve normal blokları ayırt edelim
  const rawLines = clean.split('\n');
  const elements: React.ReactNode[] = [];
  let i = 0;

  while (i < rawLines.length) {
    const rawLine = rawLines[i];
    const line = rawLine.trim();

    // 1. Tablo Bloğu Tespiti (| col1 | col2 |)
    if (line.startsWith('|') && line.endsWith('|')) {
      const tableLines: string[] = [];
      while (i < rawLines.length && rawLines[i].trim().startsWith('|') && rawLines[i].trim().endsWith('|')) {
        tableLines.push(rawLines[i].trim());
        i++;
      }

      // Tabloyu parse et
      if (tableLines.length >= 2) {
        const parseRow = (rowStr: string) =>
          rowStr
            .slice(1, -1)
            .split('|')
            .map((c) => c.trim());

        const headers = parseRow(tableLines[0]);
        // İkinci satır genellikle |---|---| ayracıdır
        const dataRows = tableLines.slice(1).filter((r) => !/^\|[\s\-:|]+\|$/.test(r)).map(parseRow);

        elements.push(
          <div key={`table-${i}`} className="my-3 overflow-hidden rounded-xl border border-line bg-white dark:bg-zinc-900 shadow-2xs">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-[12.5px] sm:text-[13px] border-collapse">
                <thead>
                  <tr className="bg-accent/10 border-b border-line text-accent font-bold">
                    {headers.map((h, hIdx) => (
                      <th key={hIdx} className="px-3.5 py-2.5 whitespace-nowrap">
                        <Rich text={h} />
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-line/60">
                  {dataRows.map((row, rIdx) => (
                    <tr
                      key={rIdx}
                      className={rIdx % 2 === 1 ? 'bg-canvas/50 hover:bg-accent-soft/20 transition-colors' : 'hover:bg-accent-soft/20 transition-colors'}
                    >
                      {row.map((cell, cIdx) => (
                        <td key={cIdx} className="px-3.5 py-2.5 text-ink-2 align-top leading-relaxed">
                          <Rich text={cell} />
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        );
        continue;
      }
    }

    if (!line) {
      elements.push(<div key={`spacer-${i}`} className="h-1.5" />);
      i++;
      continue;
    }

    // 2. Section Heading (### Başlık)
    if (line.startsWith('### ')) {
      elements.push(
        <h4
          key={`h3-${i}`}
          className="m-0 pt-3 pb-1 border-b border-line-soft text-[14.5px] sm:text-[15.5px] font-bold text-ink flex items-center gap-2"
        >
          <span className="w-2.5 h-2.5 rounded-full bg-accent shrink-0 shadow-2xs" />
          <Rich text={line.slice(4)} />
        </h4>
      );
      i++;
      continue;
    }

    // 3. Sub-heading (#### Alt Başlık)
    if (line.startsWith('#### ')) {
      elements.push(
        <h5
          key={`h4-${i}`}
          className="m-0 pt-2 text-[12.5px] sm:text-[13px] font-bold uppercase tracking-wider text-accent flex items-center gap-2"
        >
          <span className="w-1.5 h-1.5 rounded-full bg-accent/60 shrink-0" />
          <Rich text={line.slice(5)} />
        </h5>
      );
      i++;
      continue;
    }

    // 4. Callout (> veya Özel İpuçları)
    if (line.startsWith('> ') || line.startsWith('📌') || line.startsWith('⚠️') || line.startsWith('💡') || line.startsWith('🚨')) {
      const isRed = line.startsWith('🚨') || line.startsWith('⚠️') || /(?:ölümcül|asla|acil|hayati|kritik|kontrendike|sınav tuzağı)/i.test(line);
      const icon = line.startsWith('💡') ? '💡' : line.startsWith('📌') ? '📌' : line.startsWith('⚠️') ? '⚠️' : isRed ? '🚨' : 'ℹ️';
      const content = (line.startsWith('> ') ? line.slice(2) : line).replace(/^\s*(?:💡|📌|⚠️|🚨|ℹ️)\s*/u, '');

      elements.push(
        <div
          key={`callout-${i}`}
          className={`p-3 sm:p-3.5 my-2 rounded-xl border text-[12.5px] sm:text-[13px] leading-relaxed flex items-start gap-2.5 shadow-2xs ${
            isRed
              ? 'bg-rose-50/90 dark:bg-rose-950/30 border-rose-300 dark:border-rose-800 text-rose-950 dark:text-rose-200'
              : 'bg-accent-soft/40 dark:bg-accent-soft/10 border-accent/40 text-ink'
          }`}
        >
          <span className="text-[15px] select-none shrink-0 mt-0.5" aria-hidden="true">{icon}</span>
          <div className="min-w-0 flex-1 leading-relaxed">
            <Rich text={content} />
          </div>
        </div>
      );
      i++;
      continue;
    }

    // 5. İkinci Seviye İç İçe Alt Madde (4 boşluk veya 2 boşluklu girinti)
    if (rawLine.startsWith('    - ') || rawLine.startsWith('    • ') || rawLine.startsWith('\t\t- ')) {
      const cleanText = line.replace(/^[•\-\*]\s*/, '');
      elements.push(
        <div
          key={`subsub-${i}`}
          className="ml-7 sm:ml-10 my-1 p-2 sm:p-2.5 rounded-lg bg-slate-50/80 dark:bg-zinc-850/60 border-l-2 border-accent/40 border-t border-r border-b border-line-soft/80 text-[12.5px] text-ink-3 leading-relaxed flex items-start gap-2.5 shadow-2xs hover:border-accent/60 transition-colors"
        >
          <span className="text-accent text-[12px] select-none shrink-0 mt-0.5 font-bold">↳</span>
          <div className="min-w-0 flex-1 leading-relaxed">
            <Rich text={cleanText} />
          </div>
        </div>
      );
      i++;
      continue;
    }

    // 6. Birinci Seviye İç İçe Alt Madde (2 boşluklu girinti)
    if (rawLine.startsWith('  - ') || rawLine.startsWith('  • ') || rawLine.startsWith('\t- ') || rawLine.startsWith('\t• ')) {
      const cleanText = line.replace(/^[•\-\*]\s*/, '');
      elements.push(
        <div
          key={`sub-${i}`}
          className="ml-3 sm:ml-5 my-1.5 p-2.5 sm:p-3 rounded-xl bg-slate-50/90 dark:bg-zinc-850/80 border-l-3 border-accent border-t border-r border-b border-line-soft text-[13px] sm:text-[13.5px] text-ink-2 leading-relaxed flex items-start gap-3 shadow-2xs hover:border-accent transition-all"
        >
          <span className="mt-2 w-2 h-2 rounded-sm bg-accent/80 shrink-0 rotate-45" />
          <div className="min-w-0 flex-1 leading-relaxed">
            <Rich text={cleanText} />
          </div>
        </div>
      );
      i++;
      continue;
    }

    // 7. Numaralı Liste (1. 2. 3.)
    const numMatch = line.match(/^(\d+)\.\s+(.*)$/);
    if (numMatch) {
      elements.push(
        <div
          key={`num-${i}`}
          className="my-1.5 p-3 sm:p-3.5 rounded-xl bg-white dark:bg-zinc-850 border border-line-soft hover:border-accent/40 text-[13.5px] text-ink leading-relaxed flex items-start gap-3 shadow-2xs transition-all"
        >
          <span className="shrink-0 w-5.5 h-5.5 rounded-lg bg-accent text-white text-[11.5px] font-bold flex items-center justify-center mt-0.5 shadow-xs">
            {numMatch[1]}
          </span>
          <div className="min-w-0 flex-1 leading-relaxed">
            <Rich text={numMatch[2]} />
          </div>
        </div>
      );
      i++;
      continue;
    }

    // 8. Ana Madde (• veya - veya *)
    if (line.startsWith('• ') || line.startsWith('- ') || line.startsWith('* ')) {
      const cleanText = line.replace(/^[•\-\*]\s*/, '');
      elements.push(
        <div
          key={`bullet-${i}`}
          className="my-2 p-3 sm:p-3.5 rounded-xl bg-white dark:bg-zinc-850 border border-line-soft hover:border-accent/50 text-[13.5px] sm:text-[14px] text-ink leading-relaxed flex items-start gap-3 shadow-2xs transition-all"
        >
          <span className="mt-2 w-2.5 h-2.5 rounded-full bg-accent shrink-0 shadow-xs ring-4 ring-accent/15" />
          <div className="min-w-0 flex-1 leading-relaxed">
            <Rich text={cleanText} />
          </div>
        </div>
      );
      i++;
      continue;
    }

    // 9. Normal Paragraf
    elements.push(
      <p key={`p-${i}`} className="m-0 text-[13.5px] sm:text-[14px] text-ink-2 leading-[1.8] font-normal my-1.5">
        <Rich text={line} />
      </p>
    );
    i++;
  }

  return <div className="flex flex-col gap-1">{elements}</div>;
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
  const [status, setStatus] = useState<'none' | 'learned' | 'review'>('none');

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
        className={`w-full grid rounded-2xl transition-all duration-500 ease-out shadow-xs hover:shadow-md min-h-[175px] border ${
          status === 'learned'
            ? 'border-emerald-400 dark:border-emerald-700 bg-emerald-50/20'
            : status === 'review'
            ? 'border-amber-400 dark:border-amber-700 bg-amber-50/20'
            : 'border-line hover:border-accent/40 bg-canvas'
        }`}
        style={{
          transformStyle: 'preserve-3d',
          transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
        }}
      >
        {/* FRONT FACE */}
        <div
          className={`[grid-area:1/1] min-w-0 select-none rounded-2xl p-4 sm:p-5 flex flex-col justify-between ${
            isFlipped ? 'pointer-events-none' : ''
          }`}
          style={{
            backfaceVisibility: 'hidden',
          }}
        >
          <div className="flex items-start justify-between gap-2 shrink-0">
            <span className="min-w-0 min-h-6 px-2.5 py-1 rounded-lg text-[11.5px] leading-tight font-semibold bg-amber-100 dark:bg-amber-950/60 text-amber-900 dark:text-amber-200 uppercase tracking-[0.04em] inline-flex items-center gap-1.5 border border-amber-200/80 dark:border-amber-800">
              <BrainCircuit className="w-3.5 h-3.5 shrink-0 text-amber-700 dark:text-amber-400" />
              <span className="min-w-0">{card.category || card.subtopic || 'Klinik Spot'}</span>
            </span>
            <div className="flex items-center gap-1.5">
              {status === 'learned' && (
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
                  Öğrenildi ✓
                </span>
              )}
              {status === 'review' && (
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
                  Tekrar Edilecek
                </span>
              )}
              <span aria-hidden="true" className="shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-canvas text-accent shadow-2xs border border-line-soft">
                <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
              </span>
            </div>
          </div>

          <div className="my-2.5 flex-1 flex flex-col justify-center">
            <h4 className="m-0 text-[13.5px] sm:text-[14.5px] font-bold text-ink leading-snug tracking-[-0.01em] break-words">
              {frontText}
            </h4>
            {card.hint && (
              <div className="mt-2.5">
                {showHint ? (
                  <p className="m-0 text-[12px] text-amber-950 dark:text-amber-200 bg-amber-50 dark:bg-amber-950/50 border border-amber-200 dark:border-amber-800 rounded-xl p-2.5 leading-relaxed shadow-2xs">
                    <strong>İpucu:</strong> {card.hint}
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
                    <span>İpucunu Göster</span>
                  </button>
                )}
              </div>
            )}
          </div>

          <div className="pt-2 border-t border-line-soft/60 flex items-center justify-between text-[11px] text-ink-3">
            <span>Kafanda yanıtla</span>
            <span className="font-semibold text-accent flex items-center gap-1">
              <span>Cevabı Gör (Tıkla)</span>
              <ArrowRight className="w-3 h-3" />
            </span>
          </div>
        </div>

        {/* BACK FACE */}
        <div
          className={`[grid-area:1/1] min-w-0 rounded-2xl p-4 sm:p-5 flex flex-col justify-between bg-canvas ${
            !isFlipped ? 'pointer-events-none' : ''
          }`}
          style={{
            backfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)',
          }}
        >
          <div className="flex items-start justify-between gap-2 shrink-0 select-none">
            <span className="min-w-0 min-h-6 px-2.5 py-1 rounded-lg text-[11.5px] leading-tight font-semibold bg-emerald-100 dark:bg-emerald-950/60 text-emerald-900 dark:text-emerald-200 uppercase tracking-[0.04em] inline-flex items-center gap-1.5 border border-emerald-300/80 dark:border-emerald-800">
              <CheckCircle2 className="w-3.5 h-3.5 shrink-0 text-emerald-700 dark:text-emerald-400" />
              <span className="min-w-0">Çözüm & Mekanizma</span>
            </span>
            <span aria-hidden="true" className="shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-white/80 dark:bg-zinc-800 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800 shadow-2xs">
              <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
            </span>
          </div>

          <div className="my-2.5 flex-1 text-[12.5px] sm:text-[13.5px] font-medium text-ink leading-relaxed whitespace-pre-line break-words select-text">
            <Rich text={backText} />
          </div>

          <div className="pt-2.5 border-t border-line-soft/80 flex items-center justify-between gap-2" onClick={(e) => e.stopPropagation()}>
            <span className="text-[11px] font-medium text-ink-3">Hafıza Durumu:</span>
            <div className="flex items-center gap-1.5">
              <button
                type="button"
                onClick={() => setStatus('learned')}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition-all cursor-pointer flex items-center gap-1 ${
                  status === 'learned'
                    ? 'bg-emerald-600 text-white shadow-xs ring-2 ring-emerald-300'
                    : 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 hover:bg-emerald-100'
                }`}
              >
                <Check className="w-3 h-3" />
                <span>Biliyorum</span>
              </button>
              <button
                type="button"
                onClick={() => setStatus('review')}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition-all cursor-pointer flex items-center gap-1 ${
                  status === 'review'
                    ? 'bg-amber-600 text-white shadow-xs ring-2 ring-amber-300'
                    : 'bg-amber-50 dark:bg-amber-950/40 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800 hover:bg-amber-100'
                }`}
              >
                <RotateCcw className="w-3 h-3" />
                <span>Tekrar Et</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Hub (deck catalogue)
// ---------------------------------------------------------------------------

export const InteractiveDeckView: React.FC<InteractiveDeckViewProps> = ({ initialDeckId, initialSlideNumber, onDeckChange, onOpenPdfModal, questionFocus, onClearQuestionFocus, isAdmin = false }) => {
  // Yeni ders ekranı varsayılan; klasik slayt ekranı Araçlar menüsünden açılır ve deste kapanınca sıfırlanır
  const [classicPlayer, setClassicPlayer] = useState(false);
  // Liste hafif katalogdan gelir; slaytlar yalnızca açılan deste için yüklenir (12 MB tek parça yerine)
  const allDecks = DECK_CATALOG;
  const [deckId, setDeckId] = useState<string | null>(initialDeckId || null);
  const [playerViewMode, setPlayerViewMode] = useState<DeckViewMode>('interactive');
  const [adminArchiveFilter, setAdminArchiveFilter] = useState<'new_only' | 'all' | 'legacy_only'>('new_only');

  useEffect(() => {
    if (initialDeckId) {
      setDeckId(initialDeckId);
    }
  }, [initialDeckId]);

  const [progress, setProgress] = useState<DeckProgress>(readProgress);

  const [activeDeck, setActiveDeck] = useState<InteractiveDeck | null>(null);
  const [deckLoading, setDeckLoading] = useState(false);
  useEffect(() => {
    if (!deckId) { setActiveDeck(null); return; }
    let alive = true;
    setDeckLoading(true);
    loadDeck<InteractiveDeck>(deckId).then((d) => {
      if (!alive) return;
      setActiveDeck(d && Array.isArray(d.slides) && d.slides.length > 0 ? d : null);
      setDeckLoading(false);
    });
    return () => { alive = false; };
  }, [deckId]);

  return (
    <div className="flex flex-col gap-3 sm:gap-4 min-w-0">
      <LearnHub
        decks={allDecks}
        progress={progress}
        isAdmin={isAdmin}
        archive={adminArchiveFilter}
        onArchive={setAdminArchiveFilter}
        onOpen={(id, pdf) => {
          touchRecent(id);
          setPlayerViewMode(pdf ? 'pdf' : 'interactive');
          setDeckId(id);
          onDeckChange?.(id);
        }}
      />

      {deckId && deckLoading && !activeDeck && (
        <div className="fixed inset-0 z-[60] bg-canvas flex items-center justify-center" role="status" aria-live="polite">
          <span className="flex items-center gap-3 text-[15px] text-ink-2">
            <span className="w-5 h-5 rounded-full border-2 border-accent border-t-transparent animate-spin" aria-hidden="true" />
            Ders açılıyor…
          </span>
        </div>
      )}

      {activeDeck && activeDeck.id === deckId && (classicPlayer ? (
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
            setClassicPlayer(false);
            onDeckChange?.(null);
          }}
          onExportPdf={onOpenPdfModal ? (slideNumber) => onOpenPdfModal({ deckId: activeDeck.id, slideNumber }) : undefined}
          focus={questionFocus && (!questionFocus.deckId || questionFocus.deckId === activeDeck.id) ? questionFocus : null}
          onClearFocus={onClearQuestionFocus}
        />
      ) : (
        <LessonPlayer
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
            setClassicPlayer(false);
            onDeckChange?.(null);
          }}
          onExportPdf={onOpenPdfModal ? (slideNumber) => onOpenPdfModal({ deckId: activeDeck.id, slideNumber }) : undefined}
          focus={questionFocus && (!questionFocus.deckId || questionFocus.deckId === activeDeck.id) ? questionFocus : null}
          onClearFocus={onClearQuestionFocus}
          onClassic={() => setClassicPlayer(true)}
        />
      ))}
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
  focus?: QuestionFocus | null;
  onClearFocus?: () => void;
}> = ({ deck, startAt, initialViewMode = 'interactive', onProgress, onClose, onExportPdf, focus, onClearFocus }) => {
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
  // Mobil çekmece: sürükle-kapat
  const [sheetDrag, setSheetDrag] = useState(0);
  const sheetStartY = useRef<number | null>(null);
  const [isFs, setIsFs] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  // Tasarımdaki sol içindekiler: geniş ekranda açık başlar, tercih hatırlanır
  // Hatırlama modu: kalın anahtar ifadeler örtülür, dokununca açılır (aktif hatırlama)
  const [recall, setRecall] = useState(false);
  useEffect(() => {
    rootRef.current?.querySelectorAll('.ms-shown').forEach((el) => el.classList.remove('ms-shown'));
  }, [index, recall]);
  const [tocOpen, setTocOpen] = useState(() => {
    try {
      const v = localStorage.getItem('medsoru_learn_toc');
      if (v) return v === '1';
    } catch {
      /* ignore */
    }
    return typeof window !== 'undefined' && window.innerWidth >= 1280;
  });
  useEffect(() => {
    try {
      localStorage.setItem('medsoru_learn_toc', tocOpen ? '1' : '0');
    } catch {
      /* ignore */
    }
  }, [tocOpen]);
  const { setIsDrawerOpen, glossaryList, setCurrentSlideText } = useGlossary();
  const rootRef = useRef<HTMLDivElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const sectionRefs = useRef<(HTMLElement | null)[]>([]);
  const stripRef = useRef<HTMLDivElement>(null);
  const programmatic = useRef(false);
  const touch = useRef<{ x: number; y: number; at: number } | null>(null);
  // İşaretleme kilidi: kalem ya da çizim açıkken kaydırma sayfa çevirmez
  const penOn = usePenActive();
  const { activeMode: drawMode } = useDrawingGlobalState();
  const marking = penOn || drawMode !== 'none';

  const slide = slides[index];
  // Soru odağı: bağlı slaytta sorunun ifadeleri (mavi) ve doğru şık (yeşil) işaretlenir.
  // DOM'a dokunmadan CSS Custom Highlight API ile; destek yoksa yalnız bant görünür.
  const stageRef = useRef<HTMLDivElement>(null);
  const focusOnSlide = Boolean(focus && (!focus.slideNumber || focus.slideNumber === slide?.slideNumber));
  const [focusHits, setFocusHits] = useState<number | null>(null);
  useEffect(() => {
    const reg = (globalThis as any).CSS?.highlights;
    const HL = (globalThis as any).Highlight;
    if (!reg || !HL) return;
    reg.delete('ms-q-focus');
    reg.delete('ms-q-answer');
    setFocusHits(null);
    if (!focus || !focusOnSlide) return;
    const t = window.setTimeout(() => {
      const root = stageRef.current;
      if (!root) return;
      const q: Range[] = [];
      const a: Range[] = [];
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      for (let node = walker.nextNode(); node; node = walker.nextNode()) {
        const text = node.nodeValue || '';
        if (text.trim().length < 3 || (node.parentElement && node.parentElement.closest('button, [aria-hidden="true"]'))) continue;
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
  }, [focus, focusOnSlide, index, viewMode, mode]);

  // Synchronized PDF page state
  const [activePdfPage, setActivePdfPage] = useState<number>(() => {
    const loc = getSlidePdfLocation(deck.id, slides[index]?.slideNumber, slides[index], n);
    return loc.primaryPage;
  });

  // When slide index changes, sync target PDF page for split/pdf views
  useEffect(() => {
    if (!slides[index]) return;
    const loc = getSlidePdfLocation(deck.id, slides[index].slideNumber, slides[index], n);
    setActivePdfPage(loc.primaryPage);
  }, [index, deck.id, slides, n]);

  const handleOpenPdfAtPage = (targetPage?: number) => {
    const loc = getSlidePdfLocation(deck.id, slides[index]?.slideNumber, slides[index], n);
    const page = targetPage ?? loc.primaryPage;
    setActivePdfPage(page);
    setViewMode('split');
    toast.info(`Orijinal Ders PDF'i Sayfa ${page} açıldı (${loc.citation})`);
  };

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

  // Native fullscreen on top of the overlay (with cross-browser & mobile/tablet support)
  useEffect(() => {
    const onFs = () => {
      const doc = document as any;
      const fsEl = doc.fullscreenElement || doc.webkitFullscreenElement || doc.mozFullScreenElement || doc.msFullscreenElement;
      setIsFs(fsEl === rootRef.current);
    };
    document.addEventListener('fullscreenchange', onFs);
    document.addEventListener('webkitfullscreenchange', onFs);
    document.addEventListener('mozfullscreenchange', onFs);
    document.addEventListener('MSFullscreenChange', onFs);
    return () => {
      document.removeEventListener('fullscreenchange', onFs);
      document.removeEventListener('webkitfullscreenchange', onFs);
      document.removeEventListener('mozfullscreenchange', onFs);
      document.removeEventListener('MSFullscreenChange', onFs);
    };
  }, []);
  // Tarayıcı tam ekranı yoksa (iPhone Safari vb.) ya da reddedilirse "odak / immersive" moduna geçilir:
  // üst araç çubuğu gizlenir, slayt tüm ekrana (100dvh x 100vw) yayılır, yalnızca küçük bir çıkış düğmesi kalır.
  const [immersive, setImmersive] = useState(false);
  const canFullscreen = true;
  const toggleFullscreen = () => {
    if (!rootRef.current) return;
    if (immersive) {
      setImmersive(false);
      return;
    }
    const doc = document as any;
    const fsEl = doc.fullscreenElement || doc.webkitFullscreenElement || doc.mozFullScreenElement || doc.msFullscreenElement;
    if (fsEl) {
      if (doc.exitFullscreen) {
        doc.exitFullscreen().catch(() => {});
      } else if (doc.webkitExitFullscreen) {
        doc.webkitExitFullscreen();
      } else if (doc.mozCancelFullScreen) {
        doc.mozCancelFullScreen();
      } else if (doc.msExitFullscreen) {
        doc.msExitFullscreen();
      }
      setIsFs(false);
      return;
    }
    const elem: any = rootRef.current;
    if (elem.requestFullscreen) {
      elem.requestFullscreen().catch(() => setImmersive(true));
    } else if (elem.webkitRequestFullscreen) {
      elem.webkitRequestFullscreen();
    } else if (elem.webkitEnterFullscreen) {
      elem.webkitEnterFullscreen();
    } else if (elem.mozRequestFullScreen) {
      elem.mozRequestFullScreen();
    } else if (elem.msRequestFullscreen) {
      elem.msRequestFullscreen();
    } else {
      setImmersive(true);
    }
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

  // Swipe (paged mode). Yazı seçerken yanlışlıkla sayfa geçmesin: uzun basma,
  // çoklu dokunma, kalem, seçili metin ve işaretleme modu kaydırmayı iptal eder.
  const onTouchStart = (e: React.TouchEvent) => {
    const t = e.touches[0];
    const stylus = (t as Touch & { touchType?: string }).touchType === 'stylus';
    touch.current = e.touches.length === 1 && !stylus ? { x: t.clientX, y: t.clientY, at: Date.now() } : null;
  };
  const onTouchEnd = (e: React.TouchEvent) => {
    const start = touch.current;
    touch.current = null;
    if (!start || mode !== 'paged' || isPenActive() || marking) return;
    if (Date.now() - start.at > 450) return;
    const sel = window.getSelection();
    if (sel && !sel.isCollapsed && sel.toString().trim()) return;
    const t = e.changedTouches[0];
    const dx = t.clientX - start.x;
    const dy = t.clientY - start.y;
    if (Math.abs(dx) > 90 && Math.abs(dx) > Math.abs(dy) * 2) (dx < 0 ? next : prev)();
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
      className={`ms-reader ${recall ? 'ms-recall' : ''} fixed inset-0 z-[60] h-[var(--vvh,100dvh)] w-full bg-canvas text-ink flex flex-col outline-none`}
      onClickCapture={(e) => {
        if (!recall) return;
        const t = (e.target as HTMLElement).closest('.ms-slide strong, .ms-slide b');
        if (t && !t.closest('.ms-slide-meta') && !t.classList.contains('ms-shown')) {
          t.classList.add('ms-shown');
          e.stopPropagation();
        }
      }}
    >
      {/* Top bar */}
      {immersive && (
        <button
          type="button"
          onClick={() => setImmersive(false)}
          aria-label="Tam ekrandan çık"
          className="fixed z-[70] right-3 top-[max(12px,env(safe-area-inset-top))] w-10 h-10 rounded-full bg-ink/70 text-white backdrop-blur flex items-center justify-center shadow-md cursor-pointer"
        >
          <Minimize2 className="w-5 h-5" />
        </button>
      )}
      <header className={`ms-reader-bar shrink-0 min-h-14 bg-white border-b border-line px-1.5 sm:px-3 flex flex-wrap sm:flex-nowrap items-center gap-1 sm:gap-1.5 min-w-0 sm:overflow-x-auto no-scrollbar ${immersive ? 'hidden' : ''}`}>
        <button type="button" onClick={onClose} aria-label="Sunumu kapat" title="Kapat (Esc)" className={iconBtn}>
          <X className="w-5 h-5" />
        </button>
        <button
          type="button"
          onClick={() => setTocOpen((v) => !v)}
          aria-pressed={tocOpen}
          aria-label="İçindekiler"
          title="İçindekiler"
          className={`${iconBtn} hidden lg:flex ${tocOpen ? 'bg-accent-soft text-accent' : ''}`}
        >
          <ListTree className="w-5 h-5" />
        </button>
        <div className="min-w-[96px] flex-1">
          <div className="text-[11.5px] text-ink-3 truncate leading-tight">
            {deck.discipline}
            {deck.instructor ? ` · ${deck.instructor}` : ''}
          </div>
          <div className="text-[15px] font-semibold truncate leading-tight" title={deck.title}>
            {deck.shortTitle || deck.title}
          </div>
        </div>

        {/* Global topic search trigger */}
        <button
          type="button"
          onClick={() => setSearchOpen(true)}
          title="Ders İçinde Konu, Soru ve Spot Ara (Ctrl+K veya /)"
          className="h-9 px-2.5 rounded-[10px] bg-canvas hover:bg-white border border-line text-ink-2 hover:text-ink text-[13px] font-medium inline-flex items-center gap-1.5 cursor-pointer shrink-0 transition-colors"
        >
          <Search className="w-4 h-4 text-accent" />
          <span className="hidden xl:inline">Ara</span>
          <kbd className="hidden lg:inline text-[11px] font-mono text-ink-3 bg-white px-1.5 py-0.5 rounded border border-line">Ctrl+K</kbd>
        </button>

        {/* Medical Glossary Dictionary trigger */}
        <button
          type="button"
          onClick={() => setIsDrawerOpen(true)}
          title="Tıbbi Terimler Sözlüğü (Latin İsimler, Bakteri, Virüs ve İlaçlar)"
          className="hidden sm:inline-flex h-9 px-2.5 rounded-[10px] bg-canvas hover:bg-white border border-line text-ink-2 hover:text-teal-700 dark:hover:text-teal-400 text-[13px] font-medium items-center gap-1.5 cursor-pointer shrink-0 transition-colors"
        >
          <BookOpen className="w-4 h-4 text-teal-600 dark:text-teal-400" />
          <span className="hidden xl:inline">Sözlük</span>
          <span className="hidden sm:inline text-[11.5px] font-bold bg-teal-500/10 text-teal-700 dark:text-teal-300 px-1.5 py-0.5 rounded-full border border-teal-500/20">
            {glossaryList.length}
          </span>
        </button>

        <span className="font-mono text-[12px] sm:text-[13px] text-ink-2 px-1.5 py-0.5 rounded-md bg-canvas shrink-0" aria-live="polite">
          {index + 1} / {n}
        </span>

        {/* View Mode Switcher: Interactive / Split / PDF */}
        <div role="radiogroup" aria-label="Çalışma Modu" className="hidden md:flex items-center h-9 bg-canvas rounded-[10px] p-0.5 border border-line/60">
          <button
            type="button"
            role="radio"
            aria-checked={viewMode === 'interactive'}
            aria-label="Etkileşimli Slaytlar"
            title="Etkileşimli Slaytlar"
            onClick={() => setViewMode('interactive')}
            className={`h-8 px-2 sm:px-2.5 rounded-lg inline-flex items-center gap-1.5 text-[12px] sm:text-[13px] cursor-pointer transition-colors ${
              viewMode === 'interactive'
                ? 'bg-white text-accent font-semibold shadow-xs'
                : 'text-ink-2 hover:text-ink'
            }`}
          >
            <GalleryHorizontal className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-accent" />
            <span className="hidden 2xl:inline">Slaytlar</span>
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
                ? 'bg-white text-indigo-600 dark:text-indigo-400 font-semibold shadow-xs'
                : 'text-ink-2 hover:text-ink'
            }`}
          >
            <Columns className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-indigo-600 dark:text-indigo-400" />
            <span className="hidden 2xl:inline">Yan Yana</span>
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
                ? 'bg-white text-rose-600 dark:text-rose-400 font-semibold shadow-xs'
                : 'text-ink-2 hover:text-ink'
            }`}
          >
            <FileText className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-rose-500" />
            <span className="hidden 2xl:inline">Orijinal PDF</span>
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
                  mode === id ? 'bg-white text-accent font-semibold shadow-xs' : 'text-ink-2 hover:text-ink'
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
            <button
              type="button"
              onClick={() => setRecall((v) => !v)}
              aria-pressed={recall}
              title="Hatırlama modu: kalın anahtar ifadeleri ört, önce hatırla, sonra dokunup aç"
              className={`h-9 px-3 rounded-full text-[13px] font-medium inline-flex items-center gap-1.5 cursor-pointer shrink-0 transition-colors ${
                recall ? 'bg-accent-soft text-accent' : 'text-ink-2 hover:bg-canvas'
              }`}
            >
              <EyeOff className="w-4 h-4" />
              <span className="hidden md:inline">Hatırla</span>
            </button>
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
            className={`${iconBtn} hidden md:flex`}
          >
            <FileDown className="w-5 h-5" />
          </button>
        )}
        <button
          type="button"
          onClick={() => setPanelOpen((v) => !v)}
          aria-pressed={panelOpen}
          aria-label="Etkileşim panelini aç/kapat"
          title="Akıl kartları, ders notu ve AI"
          className={`${iconBtn} ${panelOpen ? 'bg-accent-soft text-accent' : ''}`}
        >
          {panelOpen ? <PanelRightClose className="w-5 h-5" /> : <PanelRightOpen className="w-5 h-5" />}
        </button>
        {canFullscreen && (
          <button type="button" onClick={toggleFullscreen} aria-label={isFs ? 'Tam ekrandan çık' : 'Tam ekran'} title="Tam ekran (F)" className={iconBtn}>
            {isFs || immersive ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
          </button>
        )}
      </header>
      <div className="shrink-0 h-[3px] bg-line-soft" aria-hidden="true">
        <div className="h-full bg-accent transition-[width] duration-300" style={{ width: `${((index + 1) / n) * 100}%` }} />
      </div>
      {marking && (
        <div role="status" className="ms-pop-in shrink-0 flex items-center gap-2 px-3 sm:px-4 py-1.5 bg-warn-soft text-warn text-[12.5px] font-medium">
          <Lock className="w-3.5 h-3.5 shrink-0" />
          <span className="flex-1 min-w-0 truncate">İşaretleme modu: kaydırma sayfa çevirmez. Kalem çizer, parmak kaydırır.</span>
          <button
            type="button"
            onClick={() => {
              stopPen();
              setDrawingGlobalState({ activeMode: 'none' });
            }}
            className="shrink-0 h-7 px-2.5 rounded-md bg-white/70 hover:bg-white text-ink text-[12px] font-semibold cursor-pointer"
          >
            Bitti
          </button>
        </div>
      )}

      {/* Stage + panel */}
      <div className="flex-1 min-h-0 flex">
        {tocOpen && (
          <aside aria-label="İçindekiler" className="ms-fade-in hidden lg:flex w-[248px] shrink-0 flex-col bg-white border-r border-line min-h-0">
            <div className="px-4 pt-3 pb-1.5 text-[11px] font-semibold uppercase tracking-[.06em] text-ink-3">Bölümler · {n}</div>
            <ol className="list-none m-0 px-2 pb-3 flex-1 min-h-0 overflow-y-auto overscroll-contain flex flex-col gap-0.5">
              {slides.map((sl, i) => {
                const on = i === index;
                const done = i < index;
                return (
                  <li key={sl.slideNumber ?? i}>
                    <button
                      type="button"
                      onClick={() => goTo(i)}
                      aria-current={on ? 'step' : undefined}
                      className={`w-full min-h-[34px] px-2.5 rounded-lg flex items-center gap-2 text-left text-[13px] cursor-pointer transition-colors ${
                        on ? 'bg-accent-soft text-accent font-semibold' : 'text-ink-2 hover:bg-canvas hover:text-ink'
                      }`}
                    >
                      <span
                        className={`w-4 h-4 rounded-full shrink-0 border-[1.5px] flex items-center justify-center ${
                          done ? 'bg-ok border-ok text-white' : on ? 'border-accent' : 'border-line-2'
                        }`}
                        aria-hidden="true"
                      >
                        {done && <Check className="w-2.5 h-2.5" strokeWidth={3.5} />}
                      </span>
                      <span className="min-w-0 flex-1 truncate" title={sl.title}>
                        {sl.title || `Slayt ${i + 1}`}
                      </span>
                    </button>
                  </li>
                );
              })}
            </ol>
          </aside>
        )}
      <div className={`flex-1 min-w-0 min-h-0 grid grid-cols-1 ${panelOpen ? 'lg:grid-cols-[minmax(0,1fr)_400px]' : ''}`}>
        <div ref={stageRef} className="min-h-0 min-w-0 relative">
          {focus && focusOnSlide && (
            <div className="ms-qfocus-band ms-pop-in" role="status">
              <span className="ms-qfocus-dot is-q" aria-hidden /> <span className="truncate">{focus.label}</span>
              {focus.answerKey && (
                <span className="ms-qfocus-ans">
                  <span className="ms-qfocus-dot is-a" aria-hidden /> Doğru şık {focus.answerKey}
                  {focus.answerText ? <span className="hidden sm:inline">: {focus.answerText.length > 48 ? focus.answerText.slice(0, 46) + '…' : focus.answerText}</span> : null}
                </span>
              )}
              {focusHits === 0 && <span className="text-ink-3 hidden sm:inline">· slayt metninde birebir geçmiyor</span>}
              {onClearFocus && (
                <button type="button" onClick={onClearFocus} className="ms-qfocus-x" aria-label="İşaretlemeyi kaldır">
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          )}
          {viewMode === 'pdf' ? (
            <div className="absolute inset-0 p-2 sm:p-4 flex flex-col">
              <DeckPdfViewer
                deck={deck}
                currentSlideNumber={slide.slideNumber}
                currentSlide={slide}
                targetPage={activePdfPage}
                targetPageRange={slide.sourcePageRange}
                onToggleSplitView={() => setViewMode('split')}
                onPageChange={(p) => setActivePdfPage(p)}
              />
            </div>
          ) : viewMode === 'split' ? (
            <div className="absolute inset-0 p-2 sm:p-3 grid grid-cols-1 lg:grid-cols-2 gap-2 sm:gap-3">
              <div
                className="min-h-0 h-full flex flex-col rounded-2xl overflow-hidden border border-line bg-white/50 backdrop-blur-sm relative shadow-sm"
                onTouchStart={onTouchStart}
                onTouchEnd={onTouchEnd}
              >
                <SlideCanvas
                  key={`split-${index}`}
                  deckId={deck.id}
                  slide={slide}
                  highlightScope={`deck:${deck.id}:${slide.slideNumber}`}
                  index={index}
                  total={n}
                  paged
                  onNext={next}
                  onPrev={prev}
                  onOpenPdfAtPage={handleOpenPdfAtPage}
                  onToggleFullscreen={toggleFullscreen}
                  isFullscreen={isFs || immersive}
                  onOpenQuestions={() => {
                    setTab('flashcards');
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
              <div className="min-h-0 h-full flex flex-col rounded-2xl overflow-hidden border border-line bg-white shadow-sm">
                <DeckPdfViewer
                  deck={deck}
                  currentSlideNumber={slide.slideNumber}
                  currentSlide={slide}
                  targetPage={activePdfPage}
                  targetPageRange={slide.sourcePageRange}
                  isSplitView
                  onToggleSplitView={() => setViewMode('interactive')}
                  onPageChange={(p) => setActivePdfPage(p)}
                />
              </div>
            </div>
          ) : mode === 'paged' ? (
            <div className="ms-swipe-stage absolute inset-0 p-1 sm:p-2.5 lg:p-3 flex bg-slate-50/70 dark:bg-zinc-950" onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
              <SlideCanvas
                key={index}
                deckId={deck.id}
                slide={slide}
                highlightScope={`deck:${deck.id}:${slide.slideNumber}`}
                index={index}
                total={n}
                paged
                onNext={next}
                onPrev={prev}
                onOpenPdfAtPage={handleOpenPdfAtPage}
                onToggleFullscreen={toggleFullscreen}
                isFullscreen={isFs || immersive}
                onOpenQuestions={() => {
                  setTab('flashcards');
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
            <div ref={scrollRef} className="absolute inset-0 overflow-y-auto snap-y snap-proximity overscroll-contain bg-slate-50/70 dark:bg-zinc-950" aria-label="Slaytlar">
              {slides.map((s, i) => (
                <section
                  key={i}
                  data-index={i}
                  ref={(el) => {
                    sectionRefs.current[i] = el;
                  }}
                  aria-label={`Slayt ${i + 1}`}
                  className="min-h-full snap-start p-1 sm:p-2.5 lg:p-3 flex"
                >
                  <SlideCanvas
                    deckId={deck.id}
                    slide={s}
                    highlightScope={`deck:${deck.id}:${s.slideNumber}`}
                    index={i}
                    total={n}
                    onOpenPdfAtPage={handleOpenPdfAtPage}
                    onToggleFullscreen={toggleFullscreen}
                    isFullscreen={isFs || immersive}
                    onOpenQuestions={() => {
                      setTab('flashcards');
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
            <button type="button" aria-label="Paneli kapat" onClick={() => setPanelOpen(false)} className="ms-fade-in lg:hidden fixed inset-0 z-[61] bg-[rgba(14,26,38,0.35)] cursor-default" />
            <aside
              aria-label="Etkileşim paneli"
              className="ms-sheet-up lg:animate-none fixed lg:static z-[62] left-0 right-0 bottom-0 max-h-[78dvh] lg:max-h-none lg:h-full rounded-t-2xl lg:rounded-none bg-white border-t lg:border-t-0 lg:border-l border-line flex flex-col min-h-0 shadow-lg lg:shadow-none"
              style={sheetDrag > 0 ? { transform: `translateY(${sheetDrag}px)`, transition: 'none' } : { transition: 'transform .22s var(--ease-out-soft)' }}
            >
              {/* Tutamaç: aşağı sürükleyince çekmece parmağı izler; yeterince çekilirse kapanır */}
              <div
                className="lg:hidden flex justify-center pt-2.5 pb-2 cursor-grab touch-none select-none"
                aria-hidden="true"
                onPointerDown={(e) => { sheetStartY.current = e.clientY; (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId); }}
                onPointerMove={(e) => { if (sheetStartY.current != null) setSheetDrag(Math.max(0, e.clientY - sheetStartY.current)); }}
                onPointerUp={() => {
                  if (sheetDrag > 90) setPanelOpen(false);
                  sheetStartY.current = null;
                  setSheetDrag(0);
                }}
                onPointerCancel={() => { sheetStartY.current = null; setSheetDrag(0); }}
              >
                <span className="w-12 h-1.5 rounded-full bg-line-2" />
              </div>
              <InteractionPanel deck={deck} slide={slide} tab={tab} setTab={setTab} />
            </aside>
          </>
        )}
      </div>
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
                className={`shrink-0 h-9 sm:h-10 rounded-lg px-2.5 flex items-center gap-2 text-left cursor-pointer border transition-colors ${
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
export const GlobalTopicSearchModal: React.FC<{
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
      const slideSpots = (slide.spotPearls && Array.isArray(slide.spotPearls) && slide.spotPearls.length > 0)
        ? slide.spotPearls
        : (Array.isArray((slide as any).spots) ? (slide as any).spots : []);
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
    });

    return matches;
  }, [deck, q]);

  return (
    <div className="ms-overlay fixed inset-0 z-[70] bg-[rgba(14,26,38,0.5)] backdrop-blur-xs flex items-center justify-center p-3 sm:p-6" role="dialog" aria-modal="true">
      <div className="w-full max-w-2xl bg-white border border-line rounded-2xl shadow-2xl flex flex-col max-h-[85dvh] overflow-hidden animate-in fade-in duration-200">
        {/* Modal Search Header */}
        <div className="p-3.5 sm:p-4 border-b border-line flex items-center gap-2.5">
          <Search className="w-5 h-5 text-accent shrink-0" />
          <input
            ref={inputRef}
            type="search"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Ders içinde konu, patofizyoloji, tanı, akıl kartı veya soru ara..."
            className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[15px] sm:text-[16px] placeholder:text-slate-600"
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
      <div className="px-3.5 py-2 bg-canvas text-[12px] font-bold border-b border-line text-ink flex items-center justify-between gap-2">
        <div className="flex items-center gap-2 min-w-0">
          <span className="w-2 h-2 rounded-full bg-accent shrink-0 shadow-2xs" />
          <span className="truncate">{table.title || 'Klinik & Patolojik Karşılaştırma Tablosu'}</span>
        </div>
        {isDiffDiagnosis && (
          <span className="shrink-0 text-[11px] font-bold uppercase tracking-wider bg-accent-soft text-accent border border-accent/20 px-2 py-0.5 rounded-full shadow-2xs">
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
                      <span className="text-accent text-[11px]"></span>
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
            /^(?:||)/.test(b.title) ||
            /\b(dikkat|tuzak|sınav tuzağı|kritik|ölümcül|acil|hayati|kontrendike|yanılgı|hata|sakın)\b/i.test(t) ||
            /\b(asla|ölümcül|kontrendike)\b/i.test(d);

          // 2. Amber: Spot Bilgi / Hoca İncisi / Sınav Sorusu / Püf Nokta
          const isAmber =
            !isRed &&
            (/(?:||)/.test(b.title) ||
              /\b(spot|hoca incisi|sınav spotu|püf nokta|ipucu|çıkmış soru|komite|tus)\b/i.test(t));

          // 3. Blue: Ayırt Edici Özellikler / Ayırıcı Tanı / Karşılaştırma / Kriter
          const isBlue =
            !isRed &&
            !isAmber &&
            (/(?:||)/.test(b.title) ||
              /\b(ayırt edici|ayırıcı tanı|fark|karşılaştırma|kriter|altın standart|patognomonik|spesifik)\b/i.test(t));

          // 4. Purple: Özet / Tekrar / Sentez / Hatırlatma
          const isPurple =
            !isRed &&
            !isAmber &&
            !isBlue &&
            (/(?:||)/.test(b.title) ||
              /\b(özet|tekrar|sentez|hatırlatma|yaklaşım|prognoz|sonuç)\b/i.test(t));

          let badgeCls = 'bg-teal-500/10 text-teal-800 dark:text-teal-300 border-teal-500/20';
          let borderCls = 'bg-teal-50/20 dark:bg-teal-950/20 border-line-soft';
          let icon = <BookOpen className="w-3.5 h-3.5 text-teal-600 shrink-0" />;

          if (isRed) {
            badgeCls = 'bg-rose-500/10 text-rose-800 dark:text-rose-300 border-rose-500/30';
            borderCls = 'bg-rose-50/40 dark:bg-rose-950/30 border-rose-500/20';
            icon = <AlertTriangle className="w-3.5 h-3.5 text-rose-600 shrink-0" />;
          } else if (isAmber) {
            badgeCls = 'bg-amber-500/10 text-amber-900 dark:text-amber-300 border-amber-500/30';
            borderCls = 'bg-amber-50/40 dark:bg-amber-950/30 border-amber-500/20';
            icon = <Lightbulb className="w-3.5 h-3.5 text-amber-600 shrink-0" />;
          } else if (isBlue) {
            badgeCls = 'bg-blue-500/10 text-blue-900 dark:text-blue-300 border-blue-500/30';
            borderCls = 'bg-blue-50/40 dark:bg-blue-950/30 border-blue-500/20';
            icon = <ArrowLeftRight className="w-3.5 h-3.5 text-blue-600 shrink-0" />;
          } else if (isPurple) {
            badgeCls = 'bg-purple-500/10 text-purple-900 dark:text-purple-300 border-purple-500/30';
            borderCls = 'bg-purple-50/40 dark:bg-purple-950/30 border-purple-500/20';
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
                <span className="text-[11px] font-mono font-bold text-ink-3">
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
  deckId?: string;
  slide: SlideItem;
  index: number;
  total: number;
  onOpenQuestions?: () => void;
  onOpenFlashcards?: () => void;
  onOpenNotes?: () => void;
  onOpenPdfAtPage?: (page?: number) => void;
  onNext?: () => void;
  onPrev?: () => void;
  paged?: boolean;
  /** Storage key for the student's own highlights on this slide */
  highlightScope?: string;
  onToggleFullscreen?: () => void;
  isFullscreen?: boolean;
}> = ({
  deckId = '',
  slide,
  index,
  total,
  onOpenQuestions,
  onOpenFlashcards,
  onOpenNotes,
  onOpenPdfAtPage,
  onNext,
  paged = false,
  highlightScope,
  onToggleFullscreen,
  isFullscreen = false,
}) => {
  const [copied, setCopied] = useState(false);
  const containerRef = useRef<HTMLElement>(null);

  // When changing slides in paged mode, scroll to top immediately
  useEffect(() => {
    containerRef.current?.scrollTo({ top: 0, behavior: 'instant' });
  }, [index, slide]);

  const slidePdfLoc = useMemo(() => {
    return getSlidePdfLocation(deckId, slide.slideNumber, slide, total);
  }, [deckId, slide, total]);

  const hl = slide.professorAudioHighlight;
  const emph = hl ? EMPHASIS[hl.emphasisType] || EMPHASIS.pearl : null;
  const c = slide.coreContent || {};
  const badge = tone(slide.badgeColor);
  const flashcards = slide.flashcards || [];
  const narrative = slide.synthesisNarrative || (slide as any).content || '';
  const spots = (slide.spotPearls && slide.spotPearls.length > 0) ? slide.spotPearls : ((slide as any).spots || []);
  const interactiveData = slide.interactiveElements && slide.interactiveElements.length > 0
    ? slide.interactiveElements
    : slide.interactiveElement;

  const copyQuote = () => {
    if (!hl?.quote) return;
    navigator.clipboard?.writeText(hl.quote).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    });
  };

  // Modular Block Renderers
  const renderHeader = (config?: SlideLayoutBlock['styleConfig']) => (
    <header className="ms-slide-head flex flex-col gap-2.5 pb-2 border-b border-line-soft">
      {/* Üst Başlık (Eyebrow & Metadata) */}
      <div className="ms-slide-meta flex items-center gap-2 flex-wrap text-[12px]">
        <span className="font-mono font-bold text-accent bg-accent-soft px-2.5 py-1 rounded-lg border border-accent/20 flex items-center gap-1.5 shadow-2xs">
          <GraduationCap className="w-3.5 h-3.5" />
          <span>Slayt {String(index + 1).padStart(2, '0')} / {String(total).padStart(2, '0')}</span>
        </span>
        {slide.badge && (
          <span className="h-7 px-3 rounded-lg text-[12px] font-bold tracking-[0.03em] inline-flex items-center shadow-2xs" style={{ background: badge.bg, color: badge.fg }}>
            {slide.badge}
          </span>
        )}
        {/* Orijinal Ders PDF'i Kaynak Çipi / Butonu */}
        <button
          type="button"
          onClick={() => onOpenPdfAtPage?.(slidePdfLoc.startPage)}
          title={`Orijinal ders sunumunda ${slidePdfLoc.citation} bölümünü yan ekranda aç`}
          className="h-7 px-2.5 rounded-lg text-[11.5px] font-semibold bg-amber-500/10 hover:bg-amber-500/20 text-amber-800 dark:text-amber-300 border border-amber-500/25 inline-flex items-center gap-1.5 transition-all shadow-2xs cursor-pointer group active:scale-95"
        >
          <FileText className="w-3.5 h-3.5 text-amber-600 group-hover:scale-110 transition-transform" />
          <span>Ders Notu: <strong>{slidePdfLoc.citation}</strong></span>
          <ArrowRight className="w-3 h-3 text-amber-500/70 group-hover:translate-x-0.5 transition-transform" />
        </button>
        {/* 1-Tap Tam Ekran / Odak Modu Butonu */}
        {onToggleFullscreen && (
          <button
            type="button"
            onClick={onToggleFullscreen}
            title={isFullscreen ? 'Tam ekrandan çık' : 'Tüm ekrana yay / Tam ekran oku'}
            className="h-7 px-2.5 rounded-lg text-[11.5px] font-semibold bg-accent-soft hover:bg-accent/20 text-accent border border-accent/25 inline-flex items-center gap-1.5 transition-all shadow-2xs cursor-pointer group active:scale-95 ml-auto sm:ml-0"
          >
            {isFullscreen ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
            <span className="hidden sm:inline">{isFullscreen ? 'Küçült' : 'Tam Ekran Oku'}</span>
          </button>
        )}
      </div>

      {/* Köken açıklaması */}
      <div className="ms-origin-legend" aria-label="İçerik kaynağı">
        <span data-o="hoca">Hoca / ders notu</span>
        <span data-o="ai">Yapay zekâ özeti</span>
      </div>
      {/* Büyük Ana Başlık */}
      <h2 className="ms-slide-title m-0 font-display font-extrabold tracking-[-0.025em] leading-[1.18] text-[20px] sm:text-[24px] lg:text-[27px] text-ink">
        {slide.title}
      </h2>

      {/* Vurgulu Alt Başlık */}
      {slide.subtitle && (
        <div className="ms-slide-lead p-2.5 sm:p-3 rounded-xl bg-canvas border border-accent/20 flex items-start gap-2.5 shadow-2xs">
          <span className="ms-slide-emoji text-[14px] shrink-0 select-none mt-0.5"></span>
          <div className="flex flex-col gap-0.5 min-w-0">
            <span className="ms-slide-eyebrow text-[11.5px] font-bold uppercase tracking-wider text-accent">Kavram & Odak Özeti</span>
            <p className="m-0 text-[12.5px] sm:text-[13.5px] font-medium text-ink-2 leading-[1.55]">
              {slide.subtitle}
            </p>
          </div>
        </div>
      )}
    </header>
  );

  const renderProfessorPearl = () => {
    if (!hl || !emph) return null;
    return (
      <figure data-origin="hoca" className="ms-slide-pearl m-0 rounded-2xl border-2 border-accent/20 bg-canvas p-3.5 sm:p-4.5 flex flex-col gap-2 shadow-xs">
        <figcaption className="flex items-center gap-2">
          <span
            className="h-6 px-2.5 rounded-full text-[11.5px] font-semibold inline-flex items-center gap-1.5 shadow-2xs"
            style={{ background: tone(emph.c).bg, color: tone(emph.c).fg }}
          >
            <emph.icon className="w-3.5 h-3.5" />
            {emph.label}
          </span>
          <span className="ms-slide-eyebrow text-[11.5px] font-semibold text-accent uppercase tracking-wider">
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
            <strong>Klinik Yaklaşım:</strong> {hl.note}
          </p>
        )}
      </figure>
    );
  };

  const renderNarrative = () => {
    if (!narrative) return null;
    return (
      <section data-origin="ai" className="ms-slide-narr rounded-2xl border border-line bg-canvas p-3.5 sm:p-5 shadow-xs flex flex-col gap-2.5">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line pb-2.5">
          <div className="flex items-center gap-2.5 min-w-[min(100%,220px)] flex-1">
            <span className="ms-slide-badgeicon w-7 h-7 rounded-xl bg-accent text-white flex items-center justify-center shrink-0 shadow-xs">
              <BookOpen className="w-4 h-4" />
            </span>
            <div className="min-w-0">
              <span className="ms-slide-eyebrow text-[11.5px] font-bold uppercase tracking-wider text-accent block">
                Öğrenim Bölümü • Detaylı Müfredat Analizi
              </span>
              <h3 className="m-0 text-[14.5px] sm:text-[15.5px] font-bold text-ink">
                {slide.discipline?.toLowerCase().includes('patoloji')
                  ? 'Kapsamlı Ders Notu ve Patoloji Sentezi'
                  : `Kapsamlı Ders Notu ve ${slide.discipline || 'Müfredat'} Sentezi`}
              </h3>
            </div>
          </div>
          <div className="flex items-center gap-1.5 shrink-0">
            {onOpenPdfAtPage && (
              <button
                type="button"
                onClick={() => onOpenPdfAtPage(slidePdfLoc.startPage)}
                title={`Orijinal ders sunumunun ${slidePdfLoc.citation} sayfalarını yan ekranda aç`}
                className="shrink-0 whitespace-nowrap h-7.5 px-2.5 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/25 text-[11.5px] font-semibold text-amber-800 dark:text-amber-300 inline-flex items-center gap-1.5 cursor-pointer transition-colors shadow-2xs active:scale-95"
              >
                <BookOpen className="w-3.5 h-3.5 text-amber-600" />
                <span className="hidden sm:inline">PDF'te Aç</span>
                <span>({slidePdfLoc.citation})</span>
              </button>
            )}
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
        </div>

        <StructuredSynthesisRenderer text={narrative} />
      </section>
    );
  };

  const renderTable = () => {
    if (!c.table || !c.table.headers?.length) return null;
    return <EnhancedDifferentialTable table={c.table} />;
  };

  const renderInteractive = () => {
    if (!interactiveData) return null;
    return <InteractiveStepRenderer data={interactiveData} />;
  };

  const renderSpots = () => {
    if (spots.length === 0) return null;
    return (
      <div data-origin="ai" className="mt-1">
        <SpotList items={spots} />
      </div>
    );
  };

  const renderKeyBullets = () => {
    if (!c.keyBullets || c.keyBullets.length === 0) return null;
    return <KeyBulletsRenderer bullets={c.keyBullets} />;
  };

  const renderFlashcards = () => {
    if (flashcards.length === 0) return null;
    const isCheckpoint =
      slide.badge === 'Tekrar Sayfası' ||
      slide.title.includes('TEKRAR SAYFASI') ||
      slide.title.includes('BÜYÜK FİNAL');

    return (
      <section
        data-origin="ai"
        className={`flex flex-col gap-3 pt-1 transition-all ${
          isCheckpoint
            ? 'p-4 sm:p-5 rounded-2xl bg-amber-50/50 dark:bg-amber-950/25 border-2 border-amber-300/80 dark:border-amber-800/60 shadow-sm'
            : ''
        }`}
      >
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2.5 min-w-0">
            <span
              className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 shadow-xs ${
                isCheckpoint ? 'bg-amber-600 text-white' : 'bg-amber-500 text-white'
              }`}
            >
              <BrainCircuit className="w-4.5 h-4.5" />
            </span>
            <div>
              <h3 className="m-0 text-[14.5px] sm:text-[15.5px] font-bold text-ink flex flex-wrap items-center gap-x-2 gap-y-1">
                <span>
                  {isCheckpoint ? '🎯 Pekiştirme Akıl Kartları İstasyonu' : 'Akıl Kartları (Tıkla & Çevir)'}
                </span>
                <span className="shrink-0 whitespace-nowrap font-mono text-[11px] font-bold text-amber-900 dark:text-amber-200 bg-amber-200/80 dark:bg-amber-900/60 px-2.5 py-0.5 rounded-full border border-amber-300 dark:border-amber-700">
                  {flashcards.length} Hafıza Kartı
                </span>
              </h3>
              <p className="m-0 text-[12px] text-ink-3">
                {isCheckpoint
                  ? 'Bölümün kilit sınav spotlarını ve fizyopatolojik mekanizmalarını kartları çevirerek zihninizde sınayın'
                  : 'Kafanda yanıtla, ardından karta tıklayarak cevabı ve amfi ipucunu aç'}
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

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-3.5">
          {flashcards.map((card) => (
            <FlashcardComponent key={card.id} card={card} />
          ))}
        </div>
      </section>
    );
  };

  const renderQuestions = () => {
    // Kullanıcı talimatı: Etkileşimli öğrenim sayfalarından örnek soru ve çıkmış soru gösterimi kaldırıldı.
    return null;
  };

  // Kritik Tıbbi Terimler - Kullanıcı talimatı: Slaytın en altında yer alır
  const renderMedicalTerms = () => {
    if (!slide.medicalTerms || slide.medicalTerms.length === 0) return null;
    return (
      <section data-origin="ders" className="mt-4 pt-3.5 border-t border-line-soft">
        <div className="text-[11.5px] font-bold uppercase tracking-wider text-teal-800 dark:text-teal-300 mb-2.5 flex items-center gap-1.5">
          <BookOpen className="w-3.5 h-3.5 text-teal-600" />
          <span>Kritik Tıbbi Terimler & Sözlük Kartları</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {slide.medicalTerms.map((t, idx) => (
            <div key={idx} className="p-2.5 rounded-xl bg-teal-50/30 dark:bg-zinc-800/80 border border-teal-200/50 text-[12px] shadow-2xs">
              <strong className="text-teal-900 dark:text-teal-300 block font-bold text-[12.5px] mb-0.5">{t.term}</strong>
              <span className="text-ink-2 leading-relaxed">{t.explanation}</span>
            </div>
          ))}
        </div>
      </section>
    );
  };

  const sortedBlocks = useMemo(() => {
    if (!slide.layoutBlocks || slide.layoutBlocks.length === 0) return null;
    return [...slide.layoutBlocks].filter((b) => b.visible !== false).sort((a, b) => a.order - b.order);
  }, [slide.layoutBlocks]);

  const renderBlockItem = (block: SlideLayoutBlock) => {
    const bType = (block.type || '').toLowerCase();
    switch (bType) {
      case 'header':
        return <React.Fragment key={block.id}>{renderHeader(block.styleConfig)}</React.Fragment>;
      case 'professor_pearl':
      case 'pearl':
        return <React.Fragment key={block.id}>{renderProfessorPearl()}</React.Fragment>;
      case 'narrative':
      case 'content':
        return <React.Fragment key={block.id}>{renderNarrative()}</React.Fragment>;
      case 'table':
      case 'table_block':
        return <React.Fragment key={block.id}>{renderTable()}</React.Fragment>;
      case 'interactive':
      case 'interactive_element':
      case 'interactive_elements':
      case 'interactives':
        return <React.Fragment key={block.id}>{renderInteractive()}</React.Fragment>;
      case 'spots':
      case 'spot_pearls':
      case 'spot_list':
      case 'spotpearls':
        return <React.Fragment key={block.id}>{renderSpots()}</React.Fragment>;
      case 'key_bullets':
      case 'bullets':
        return <React.Fragment key={block.id}>{renderKeyBullets()}</React.Fragment>;
      case 'flashcards':
      case 'flashcard':
        return <React.Fragment key={block.id}>{renderFlashcards()}</React.Fragment>;
      case 'terms':
      case 'medical_terms':
      case 'medicalterms':
        return <React.Fragment key={block.id}>{renderMedicalTerms()}</React.Fragment>;
      default:
        return null;
    }
  };

  return (
    <article
      key={slide.slideNumber}
      ref={containerRef}
      className={`w-full ${paged ? 'h-full overflow-y-auto overscroll-contain' : 'min-h-full'} max-w-[1720px] 2xl:max-w-none mx-auto bg-white dark:bg-zinc-900 border border-line/80 rounded-2xl shadow-sm flex flex-col min-h-0 custom-scrollbar relative ms-slide ms-view-enter transition-all duration-300`}
    >
      {/* Çizim katmanı içeriğin tamamını kaplar (kaydırılan kutunun yalnız ilk ekranını değil) */}
      <div className="relative min-w-0">
        <SlideDrawingCanvas scope={highlightScope || `slide:${slide.slideNumber}`} />
        <Highlightable
          scope={highlightScope || `slide:${slide.slideNumber}:${slide.title}`}
          className="px-4 py-4 sm:px-8 sm:py-6 lg:px-12 lg:py-7 flex flex-col gap-4 sm:gap-6 w-full max-w-full"
        >
          {sortedBlocks ? (
            <>
              {sortedBlocks.map(renderBlockItem)}
              {/* Güvenlik Ağı 1: Eğer sortedBlocks içinde interactive bloğu yoksa ama slaytta interaktif ögeler varsa MUTLAKA render et */}
              {!sortedBlocks.some((b) =>
                ['interactive', 'interactive_element', 'interactive_elements', 'interactives'].includes(b.type?.toLowerCase())
              ) && renderInteractive()}
              {/* Güvenlik Ağı 2: Eğer sortedBlocks içinde terim bloğu yoksa ama tıbbi terimler varsa en altta render et */}
              {!sortedBlocks.some((b) =>
                ['terms', 'medical_terms', 'medicalterms'].includes(b.type?.toLowerCase())
              ) && renderMedicalTerms()}
            </>
          ) : (
            <>
              {renderHeader()}
              {renderProfessorPearl()}
              {renderNarrative()}
              {renderTable()}
              {renderInteractive()}
              {renderSpots()}
              {renderKeyBullets()}
              {renderFlashcards()}
              {renderMedicalTerms()}
            </>
          )}

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
      </div>
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
export const SpotList: React.FC<{ items: Array<string | any>; title?: string; note?: string; compact?: boolean }> = ({
  items,
  title = 'YÜKSEK VERİM (HIGH-YIELD) · AKILDA TUT',
  note,
  compact = false,
}) => (
  <section className={`rounded-2xl border-2 border-amber-300/90 dark:border-amber-700/60 bg-gradient-to-br from-amber-50/95 via-amber-50/40 to-orange-50/60 dark:from-amber-950/40 dark:via-zinc-900 dark:to-orange-950/20 shadow-sm flex flex-col ${compact ? 'p-3 gap-2.5' : 'p-4 sm:p-5 gap-3.5'}`}>
    <header className="flex items-center gap-2.5 pb-2.5 border-b border-amber-200/80 dark:border-amber-800/40">
      <span className="w-8 h-8 rounded-xl bg-gradient-to-br from-amber-500 to-amber-600 text-white flex items-center justify-center shrink-0 shadow-xs" aria-hidden="true">
        <Lightbulb className="w-4.5 h-4.5" />
      </span>
      <div className="min-w-0">
        <span className="text-[12px] sm:text-[13px] font-black uppercase tracking-wider text-amber-900 dark:text-amber-300 block">
          {title}
        </span>
        <span className="text-[11px] text-amber-800/80 dark:text-amber-400 font-medium">
          Komite ve kurul sınavlarında doğrudan puan getiren kilit prensipler
        </span>
      </div>
      <span className="ml-auto font-mono text-[11.5px] font-bold text-amber-900 bg-amber-200/80 dark:bg-amber-900/60 px-2.5 py-0.5 rounded-full border border-amber-300 dark:border-amber-700">
        {items.length} Spot
      </span>
    </header>
    {note && <p className="m-0 -mt-1 text-[13px] text-amber-900/80 dark:text-amber-300/80 font-medium">{note}</p>}
    <ol className={`list-none m-0 p-0 flex flex-col ${compact ? 'gap-2' : 'gap-2.5'}`}>
      {items.map((p, i) => {
        const isObj = p && typeof p === 'object';
        const pText: string = isObj ? (p.text || '') : String(p || '');
        const pBadge: string = isObj ? (p.badge || '') : '';
        const pType: string = isObj ? (p.type || '') : '';
        const pColor: string = isObj ? (p.color || '') : '';

        const isRed = pType === 'warning' || pColor === 'rose' || pBadge.includes('🚨') || /(?:ölümcül|asla|acil|hayati|kritik|kontrendike|\[kırmızı|\[red|önemli)/i.test(pText);
        const isBlue = !isRed && (pType === 'exam' || pColor === 'sky' || pBadge.includes('❓') || /(?:çıkmış soru|çıkmış|komite sorusu|tus sorusu|soruldu|ösym|\[mavi|\[blue|\[çıkmış|soru:)/i.test(pText));

        const rawLines = pText.split('\n');

        return (
          <li
            key={i}
            className={`rounded-xl transition-all shadow-2xs border-l-4 border-t border-r border-b ${
              isRed
                ? 'border-l-red-600 bg-red-50/90 dark:bg-red-950/30 border-red-200 dark:border-red-900/50 text-red-950 dark:text-red-100'
                : isBlue
                ? 'border-l-blue-600 bg-blue-50/90 dark:bg-blue-950/30 border-blue-200 dark:border-blue-900/50 text-blue-950 dark:text-blue-100'
                : 'border-l-amber-500 bg-white dark:bg-zinc-800/90 border-amber-200/80 dark:border-zinc-700 text-ink'
            } p-3 sm:p-3.5 text-[13px] sm:text-[13.5px] leading-[1.65]`}
          >
            <div className="flex items-center justify-between gap-2 mb-1.5 pb-1 border-b border-inherit/20">
              <span className="inline-flex items-center gap-1.5">
                {isRed ? (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-bold bg-red-100 dark:bg-red-900/60 text-red-700 dark:text-red-200">
                    <AlertCircle className="w-3 h-3" /> {pBadge ? pBadge.replace(/^[🚨]\s*/, '') : 'KRİTİK UYARI'}
                  </span>
                ) : isBlue ? (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-bold bg-blue-100 dark:bg-blue-900/60 text-blue-700 dark:text-blue-200">
                    <HelpCircle className="w-3 h-3" /> {pBadge ? pBadge.replace(/^[❓]\s*/, '') : 'ÇIKMIŞ SORU ODAĞI'}
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-bold bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300">
                    <Lightbulb className="w-3 h-3 text-amber-600" /> {pBadge ? pBadge.replace(/^[💡]\s*/, '') : 'SINAV SPOTU'}
                  </span>
                )}
              </span>
              <span className="font-mono text-[11px] font-bold text-ink-3">#{i + 1}</span>
            </div>

            <div className="flex flex-col gap-1 min-w-0 break-words">
              {rawLines.map((line, lIdx) => {
                const trimmed = line.trim();
                if (!trimmed) return null;

                const isSubBullet = (line.startsWith('  ') || line.startsWith('\t')) && (trimmed.startsWith('- ') || trimmed.startsWith('• ') || trimmed.startsWith('* ') || trimmed.startsWith('→ '));
                const isUpperBullet = !isSubBullet && (trimmed.startsWith('• ') || trimmed.startsWith('* ') || /^[0-9]+\.\s/.test(trimmed));

                if (isSubBullet) {
                  const cleanText = trimmed.replace(/^[-•*→]\s*/, '');
                  return (
                    <div key={lIdx} className="ml-3 pl-2.5 py-0.5 border-l-2 border-amber-300 dark:border-amber-700 text-[12.5px] flex items-start gap-1.5 text-ink-2">
                      <span className="text-[10px] opacity-70 mt-1 select-none">▫</span>
                      <span className="min-w-0 flex-1"><Rich text={cleanText} /></span>
                    </div>
                  );
                }

                if (isUpperBullet) {
                  const cleanText = trimmed.replace(/^([•*]|\d+\.)\s*/, '');
                  return (
                    <div key={lIdx} className="font-semibold flex items-start gap-2 pt-0.5 text-ink">
                      <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-2 shrink-0" />
                      <span className="min-w-0 flex-1"><Rich text={cleanText} /></span>
                    </div>
                  );
                }

                return (
                  <div key={lIdx} className="text-ink font-medium leading-relaxed">
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
  const cards = slide.flashcards || [];

  // Sade panel: Kartlar, Notlar ve AI.
  // Kullanıcı talimatı: Örnek soru ve çıkmış soru gösterimi kaldırıldı.
  const tabs: { id: PanelTab; label: string; count?: number }[] = [
    ...(cards.length ? [{ id: 'flashcards' as PanelTab, label: 'Kartlar', count: cards.length }] : []),
    { id: 'notes', label: 'Notlar' },
    { id: 'ai', label: 'Sor' },
  ];
  const wanted: PanelTab = (tab === 'pdf' || tab === 'questions') ? 'flashcards' : tab === 'pearls' ? 'notes' : tab;
  const active: PanelTab = tabs.some((t) => t.id === wanted) ? wanted : (tabs[0]?.id || 'notes');

  return (
    <>
      <div role="tablist" aria-label="Etkileşim" className="shrink-0 grid gap-1 m-3 mb-0 bg-canvas rounded-xl p-1" style={{ gridTemplateColumns: `repeat(${tabs.length}, minmax(0, 1fr))` }}>
        {tabs.map((t) => (
          <button
            key={t.id}
            type="button"
            role="tab"
            aria-selected={active === t.id}
            onClick={() => setTab(t.id)}
            className={`h-9 px-1 rounded-lg text-[12.5px] cursor-pointer truncate inline-flex items-center justify-center gap-1 transition-colors ${active === t.id ? 'bg-white text-ink font-semibold shadow-xs' : 'text-ink-2 hover:text-ink'}`}
          >
            {t.label}
            {!!t.count && <span className="font-mono text-[11px] text-ink-3">{t.count}</span>}
          </button>
        ))}
      </div>
      <div key={active} className="ms-pop-in flex-1 min-h-0 overflow-y-auto overscroll-contain p-3 flex flex-col gap-3">
        {active === 'flashcards' && (
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
        {active === 'notes' && <SlideNotesTab slide={slide} />}
        {active === 'notes' && (
          (deck.highYieldPearls || []).length > 0 ? (
            <SpotList items={deck.highYieldPearls || []} title="Dersin spotları" note="Dersin tamamından en çok sorulan bilgiler" compact />
          ) : (
            <p className="m-0 text-[14px] text-ink-2 px-1 py-4">Bu ders için spot bilgi yok.</p>
          )
        )}
        {active === 'ai' && <AskAi key={slide.slideNumber} deck={deck} slide={slide} />}
      </div>
    </>
  );
};

// ---------------------------------------------------------------------------
// Slide Notes Tab: Structured medical textbook notes and tables for the slide
// ---------------------------------------------------------------------------
export const SlideNotesTab: React.FC<{ slide: SlideItem }> = ({ slide }) => {
  const c = slide.coreContent || {};
  const narrative = slide.synthesisNarrative || (slide as any).content || '';
  const spots = (slide.spotPearls && slide.spotPearls.length > 0) ? slide.spotPearls : ((slide as any).spots || []);

  return (
    <div className="flex flex-col gap-3.5">
      {/* Narrative block */}
      {narrative && (
        <div className="rounded-xl border border-line bg-canvas p-3.5 flex flex-col gap-2.5">
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

const QuizCard: React.FC<{ q: SlideRelatedQuestion | string | any; n: number }> = ({ q, n }) => {
  const [picked, setPicked] = useState<string | null>(null);
  const [showExp, setShowExp] = useState(true);

  if (typeof q === 'string') {
    return (
      <article className="rounded-xl border border-amber-200 dark:border-amber-900/40 bg-amber-50/20 dark:bg-amber-950/10 p-3 flex flex-col gap-2 transition-all shadow-2xs">
        <header className="flex items-center justify-between gap-2 text-[12px] text-ink-3">
          <div className="flex items-center gap-1.5 min-w-0">
            <span className="font-mono font-semibold px-1.5 py-0.5 rounded text-[11px] bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300">
              Soru {n}
            </span>
            <span className="truncate font-medium text-ink-2">Klinik Tartışma & Muhakeme</span>
          </div>
          <span className="shrink-0 px-2 py-0.5 rounded-full text-[11.5px] font-bold bg-amber-100 dark:bg-amber-900/60 text-amber-800 dark:text-amber-200 border border-amber-300 dark:border-amber-700 flex items-center gap-1 shadow-2xs">
            <Sparkles className="w-3 h-3 text-amber-600 dark:text-amber-400" />
            Öz Değerlendirme
          </span>
        </header>
        <p className="m-0 text-[14px] leading-[1.5] font-medium text-ink">{q}</p>
      </article>
    );
  }

  const options: SlideQuestionOption[] = Array.isArray(q?.options) ? q.options : [];
  const answer = q?.correctAnswer || options.find((o) => o?.isCorrect)?.key || '';
  const done = picked !== null;
  const right = done && picked === answer;
  const isPractice =
    Boolean(q?.isPracticeQuestion) ||
    Boolean(q?.examYear && (q.examYear.includes('Çalışma') || q.examYear.includes('Özgün') || q.examYear.includes('Pekiştirme')));

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
          <span className="truncate font-medium text-ink-2">{[q?.examYear, q?.topic].filter(Boolean).join(' · ')}</span>
        </div>
        {isPractice ? (
          <span className="shrink-0 px-2 py-0.5 rounded-full text-[11.5px] font-bold bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-200 border border-emerald-300 dark:border-emerald-700 flex items-center gap-1 shadow-2xs">
            <Sparkles className="w-3 h-3 text-emerald-600 dark:text-emerald-400" />
            Özgün Çalışma Sorusu
          </span>
        ) : (
          <span className="shrink-0 px-2 py-0.5 rounded-full text-[11.5px] font-bold bg-blue-100 dark:bg-blue-900/60 text-blue-800 dark:text-blue-200 border border-blue-300 dark:border-blue-700 flex items-center gap-1 shadow-2xs">
            <GraduationCap className="w-3 h-3 text-blue-600 dark:text-blue-400" />
            Çıkmış Sınav Sorusu
          </span>
        )}
      </header>
      <p className="m-0 text-[14px] leading-[1.5] font-medium text-ink">{q?.stem || ''}</p>
      {options.length > 0 && (
        <div role="radiogroup" aria-label={`Soru ${n} şıkları`} className="flex flex-col gap-1.5">
          {options.map((o) => {
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
      )}
      {done && (
        <div className={`rounded-lg px-2.5 py-2 text-[13px] ${right ? 'bg-ok-soft dark:bg-ok/20 border border-ok/30' : 'bg-bad-soft dark:bg-bad/20 border border-bad/30'}`}>
          <div className="flex items-center justify-between gap-2">
            <strong className={right ? 'text-ok dark:text-emerald-400' : 'text-bad-text dark:text-rose-400'}>{right ? '✓ Tebrikler, Doğru Yanıt!' : `Yanlış. Doğru cevap ${answer}`}</strong>
            <span className="flex gap-1">
              {q?.explanation && (
                <button type="button" onClick={() => setShowExp((v) => !v)} className="h-7 px-2 rounded-md text-[12px] font-semibold text-ink-2 hover:bg-white/70 dark:hover:bg-white/10 cursor-pointer">
                  {showExp ? 'Açıklamayı gizle' : 'Açıklama'}
                </button>
              )}
              <button type="button" onClick={() => setPicked(null)} className="h-7 px-2 rounded-md text-[12px] font-semibold text-ink-2 hover:bg-white/70 dark:hover:bg-white/10 cursor-pointer">
                Tekrar Dene
              </button>
            </span>
          </div>
          {showExp && q?.explanation && <p className="m-0 mt-1.5 text-ink-2 dark:text-ink-muted leading-[1.55] whitespace-pre-line">{q.explanation.replace(/\n(?!\n)/g, ' ')}</p>}
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

export const AskAi: React.FC<{ deck: InteractiveDeck; slide: SlideItem }> = ({ deck, slide }) => {
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
