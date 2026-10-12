import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  Search,
  X,
  Copy,
  Check,
  CheckCircle2,
  Lightbulb,
  AlertTriangle,
  AlertCircle,
  HelpCircle,
  Sparkles,
  Send,
  RefreshCw,
  BookOpen,
  BrainCircuit,
  RotateCcw,
  ArrowLeftRight,
  ArrowRight,
  Bot,
} from 'lucide-react';
import { DECK_CATALOG, loadDeck } from '../../data/deckStore';
import {
  RenderWithGlossaryTerms,
} from './MedicalGlossaryPopover';
import { AiThinking } from '../ui/Animations';
import { toast } from '../ui/Toast';
import { safeJsonFetch } from '../../services/api';
import { QuestionFocus } from '../../services/questionFocus';
import { LessonPlayer } from './lesson/LessonPlayer';
import { LearnHub, touchRecent } from './LearnHub';
import { Dialog } from '../ui/Dialog';
import type { DeckCatalogEntry } from '../../data/deckStore';
import { triggerDomHighlightAndScroll } from '../../services/universalRedirectService';

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
  /** Desteye bağlı sorular (targetSlide ile adımlara dağıtılır) */
  questions?: any[];
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
          <div key={`table-${i}`} className="my-3 overflow-hidden rounded-xl border border-line bg-white shadow-2xs">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm sm:text-sm border-collapse">
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
          className="m-0 pt-3 pb-1 border-b border-line-soft text-md sm:text-md font-bold text-ink flex items-center gap-2"
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
          className="m-0 pt-2 text-sm sm:text-sm font-bold uppercase tracking-wider text-accent flex items-center gap-2"
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
          className={`p-3 sm:p-3.5 my-2 rounded-xl border text-sm sm:text-sm leading-relaxed flex items-start gap-2.5 shadow-2xs ${
            isRed
              ? 'bg-bad-soft/90 border-bad/30 text-bad-text '
              : 'bg-accent-soft/40 border-accent/40 text-ink'
          }`}
        >
          <span className="text-md select-none shrink-0 mt-0.5" aria-hidden="true">{icon}</span>
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
          className="ml-7 sm:ml-10 my-1 p-2 sm:p-2.5 rounded-lg bg-field/80 border-l-2 border-accent/40 border-t border-r border-b border-line-soft/80 text-sm text-ink-3 leading-relaxed flex items-start gap-2.5 shadow-2xs hover:border-accent/60 transition-colors"
        >
          <span className="text-accent text-xs select-none shrink-0 mt-0.5 font-bold">↳</span>
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
          className="ml-3 sm:ml-5 my-1.5 p-2.5 sm:p-3 rounded-xl bg-field/90 border-l-3 border-accent border-t border-r border-b border-line-soft text-sm sm:text-base text-ink-2 leading-relaxed flex items-start gap-3 shadow-2xs hover:border-accent transition-all"
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
          className="my-1.5 p-3 sm:p-3.5 rounded-xl bg-white border border-line-soft hover:border-accent/40 text-base text-ink leading-relaxed flex items-start gap-3 shadow-2xs transition-all"
        >
          <span className="shrink-0 w-5.5 h-5.5 rounded-lg bg-accent text-white text-xs font-bold flex items-center justify-center mt-0.5 shadow-xs">
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
          className="my-2 p-3 sm:p-3.5 rounded-xl bg-white border border-line-soft hover:border-accent/50 text-base sm:text-base text-ink leading-relaxed flex items-start gap-3 shadow-2xs transition-all"
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
      <p key={`p-${i}`} className="m-0 text-base sm:text-base text-ink-2 leading-[1.8] font-normal my-1.5">
        <Rich text={line} />
      </p>
    );
    i++;
  }

  return <div className="flex flex-col gap-1">{elements}</div>;
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
            ? 'border-ok bg-ok-soft/20'
            : status === 'review'
            ? 'border-warn bg-warn-soft/20'
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
            <span className="min-w-0 min-h-6 px-2.5 py-1 rounded-lg text-xs leading-tight font-semibold bg-warn-soft text-warn uppercase tracking-[0.04em] inline-flex items-center gap-1.5 border border-warn/80 ">
              <BrainCircuit className="w-3.5 h-3.5 shrink-0 text-warn " />
              <span className="min-w-0">{card.category || card.subtopic || 'Klinik Spot'}</span>
            </span>
            <div className="flex items-center gap-1.5">
              {status === 'learned' && (
                <span className="px-2 py-0.5 rounded-full text-2xs font-bold bg-ok-soft text-ok border border-ok/30">
                  Öğrenildi ✓
                </span>
              )}
              {status === 'review' && (
                <span className="px-2 py-0.5 rounded-full text-2xs font-bold bg-warn-soft text-warn border border-warn/30">
                  Tekrar Edilecek
                </span>
              )}
              <span aria-hidden="true" className="shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-canvas text-accent shadow-2xs border border-line-soft">
                <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
              </span>
            </div>
          </div>

          <div className="my-2.5 flex-1 flex flex-col justify-center">
            <h4 className="m-0 text-base sm:text-md font-bold text-ink leading-snug tracking-[-0.01em] break-words">
              {frontText}
            </h4>
            {card.hint && (
              <div className="mt-2.5">
                {showHint ? (
                  <p className="m-0 text-xs text-warn bg-warn-soft border border-warn/30 rounded-xl p-2.5 leading-relaxed shadow-2xs">
                    <strong>İpucu:</strong> {card.hint}
                  </p>
                ) : (
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      setShowHint(true);
                    }}
                    className="text-xs font-semibold text-accent hover:text-accent-hover hover:underline cursor-pointer inline-flex items-center gap-1"
                  >
                    <span>İpucunu Göster</span>
                  </button>
                )}
              </div>
            )}
          </div>

          <div className="pt-2 border-t border-line-soft/60 flex items-center justify-between text-2xs text-ink-3">
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
            <span className="min-w-0 min-h-6 px-2.5 py-1 rounded-lg text-xs leading-tight font-semibold bg-ok-soft text-ok uppercase tracking-[0.04em] inline-flex items-center gap-1.5 border border-ok/80 ">
              <CheckCircle2 className="w-3.5 h-3.5 shrink-0 text-ok " />
              <span className="min-w-0">Çözüm & Mekanizma</span>
            </span>
            <span aria-hidden="true" className="shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-white/80 text-ok border border-ok/30 shadow-2xs">
              <RefreshCw className="w-4 h-4 group-hover:rotate-180 transition-transform duration-500" />
            </span>
          </div>

          <div className="my-2.5 flex-1 text-sm sm:text-base font-medium text-ink leading-relaxed whitespace-pre-line break-words select-text">
            <Rich text={backText} />
          </div>

          <div className="pt-2.5 border-t border-line-soft/80 flex items-center justify-between gap-2" onClick={(e) => e.stopPropagation()}>
            <span className="text-2xs font-medium text-ink-3">Hafıza Durumu:</span>
            <div className="flex items-center gap-1.5">
              <button
                type="button"
                onClick={() => setStatus('learned')}
                className={`px-2.5 py-1 rounded-lg text-2xs font-bold transition-all cursor-pointer flex items-center gap-1 ${
                  status === 'learned'
                    ? 'bg-ok text-white shadow-xs ring-2 ring-ok/30'
                    : 'bg-ok-soft text-ok border border-ok/30 hover:bg-ok-soft'
                }`}
              >
                <Check className="w-3 h-3" />
                <span>Biliyorum</span>
              </button>
              <button
                type="button"
                onClick={() => setStatus('review')}
                className={`px-2.5 py-1 rounded-lg text-2xs font-bold transition-all cursor-pointer flex items-center gap-1 ${
                  status === 'review'
                    ? 'bg-warn text-white shadow-xs ring-2 ring-warn/30'
                    : 'bg-warn-soft text-warn border border-warn/30 hover:bg-warn-soft'
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
  // Liste hafif katalogdan gelir; slaytlar yalnızca açılan deste için yüklenir (12 MB tek parça yerine)
  const [deckId, setDeckId] = useState<string | null>(initialDeckId || null);
  const [playerViewMode, setPlayerViewMode] = useState<DeckViewMode>('interactive');
  const [adminArchiveFilter, setAdminArchiveFilter] = useState<'new_only' | 'all' | 'legacy_only'>('new_only');

  // URL'deki deste değişince izle: tarayıcının geri tuşu deste kimliğini kaldırınca açık ders de kapanır
  const prevInitial = useRef(initialDeckId);
  useEffect(() => {
    if (initialDeckId) setDeckId(initialDeckId);
    else if (prevInitial.current) setDeckId(null);
    prevInitial.current = initialDeckId;
  }, [initialDeckId]);

  const [progress, setProgress] = useState<DeckProgress>(readProgress);

  const [activeDeck, setActiveDeck] = useState<InteractiveDeck | null>(null);
  const [deckLoading, setDeckLoading] = useState(false);
  // Panelden deste değişince (canlı içerik): liste yeniden çizilir, açık deste yeniden yüklenir
  const [liveTick, setLiveTick] = useState(0);
  const [catalogTick, setCatalogTick] = useState(0);
  const allDecks = useMemo(() => [...DECK_CATALOG], [catalogTick]);
  // Sürümlü dersler (V1, V2…): listede yalnız grubun ilk sürümü görünür; açarken öğrenci sürümü seçer
  const hubDecks = useMemo(() => allDecks.filter((d) => !d.versionGroup || d.versionGroup === d.id), [allDecks]);
  const versionLabels = useMemo(() => {
    const m: Record<string, string[]> = {};
    allDecks.forEach((d) => {
      if (d.versionGroup) (m[d.versionGroup] ||= []).push(String(d.versionLabel || 'V1'));
    });
    Object.keys(m).forEach((k) => (m[k].length > 1 ? m[k].sort((x, y) => x.localeCompare(y, 'tr', { numeric: true })) : delete m[k]));
    return m;
  }, [allDecks]);
  const [versionPick, setVersionPick] = useState<{ list: DeckCatalogEntry[]; pdf?: boolean } | null>(null);
  const versionsOf = (id: string) => {
    const g = allDecks.find((d) => d.id === id)?.versionGroup;
    if (!g) return [];
    return allDecks
      .filter((d) => d.id === g || d.versionGroup === g)
      .sort((a, b) => String(a.versionLabel || 'V1').localeCompare(String(b.versionLabel || 'V1'), 'tr', { numeric: true }));
  };
  const deckIdRef = useRef(deckId);
  deckIdRef.current = deckId;
  useEffect(() => {
    const onChange = (e: Event) => {
      const ids: string[] = (e as CustomEvent).detail?.ids || [];
      setLiveTick((n) => (deckIdRef.current && ids.includes(deckIdRef.current) ? n + 1 : n));
      setCatalogTick((n) => n + 1);
    };
    window.addEventListener('medsoru:decks-changed', onChange);
    return () => window.removeEventListener('medsoru:decks-changed', onChange);
  }, []);
  useEffect(() => {
    if (!deckId) { setActiveDeck(null); return; }
    let alive = true;
    if (!liveTick) setDeckLoading(true);
    loadDeck<InteractiveDeck>(deckId).then((d) => {
      if (!alive) return;
      const ok = d && Array.isArray(d.slides) && d.slides.length > 0 ? d : null;
      setActiveDeck(ok);
      setDeckLoading(false);
      // Yüklenemediyse kullanıcı boş ekranda kalmasın: bildir ve kataloğa dön (bağlantı gelince yeniden denenebilir)
      if (!ok) {
        toast.error('Ders açılamadı', 'Bağlantıyı kontrol edip yeniden deneyin. Dersi çevrimdışı kullanmak için önce indirin.');
        setDeckId(null);
        onDeckChange?.(null);
      }
    });
    return () => { alive = false; };
  }, [deckId, liveTick]); // eslint-disable-line react-hooks/exhaustive-deps

  // Cümle/Metin odaklama (?highlight=...) kontrolü
  useEffect(() => {
    if (typeof window !== 'undefined' && activeDeck) {
      const sp = new URLSearchParams(window.location.search);
      const hl = sp.get('highlight');
      if (hl) {
        const t = window.setTimeout(() => triggerDomHighlightAndScroll(hl), 600);
        return () => window.clearTimeout(t);
      }
    }
  }, [activeDeck, initialSlideNumber]);

  return (
    <div className="flex flex-col gap-3 sm:gap-4 min-w-0">
      <LearnHub
        decks={hubDecks}
        versions={versionLabels}
        progress={progress}
        isAdmin={isAdmin}
        archive={adminArchiveFilter}
        onArchive={setAdminArchiveFilter}
        onOpen={(id, pdf) => {
          const versions = versionsOf(id);
          if (versions.length > 1) {
            setVersionPick({ list: versions, pdf });
            return;
          }
          touchRecent(id);
          setPlayerViewMode(pdf ? 'pdf' : 'interactive');
          setDeckId(id);
          onDeckChange?.(id);
        }}
      />

      {versionPick && (
        <VersionPicker
          versions={versionPick.list}
          progress={progress}
          onClose={() => setVersionPick(null)}
          onPick={(id) => {
            const pdf = versionPick.pdf;
            setVersionPick(null);
            touchRecent(versionPick.list[0].id);
            setPlayerViewMode(pdf ? 'pdf' : 'interactive');
            setDeckId(id);
            onDeckChange?.(id);
          }}
        />
      )}

      {deckId && deckLoading && !activeDeck && (
        <div className="fixed inset-0 z-[60] bg-canvas flex items-center justify-center" role="status" aria-live="polite">
          <div className="flex flex-col items-center gap-4">
            <span className="flex items-center gap-3 text-md text-ink-2">
              <span className="w-5 h-5 rounded-full border-2 border-accent border-t-transparent animate-spin" aria-hidden="true" />
              Ders açılıyor…
            </span>
            <button type="button" className="ui-btn is-sm is-ghost" onClick={() => { setDeckId(null); onDeckChange?.(null); }}>
              Vazgeç
            </button>
          </div>
        </div>
      )}

      {activeDeck && activeDeck.id === deckId && (
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
            onDeckChange?.(null);
          }}
          onExportPdf={onOpenPdfModal ? (slideNumber) => onOpenPdfModal({ deckId: activeDeck.id, slideNumber }) : undefined}
          focus={questionFocus && (!questionFocus.deckId || questionFocus.deckId === activeDeck.id) ? questionFocus : null}
          onClearFocus={onClearQuestionFocus}
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
    <div className="ms-overlay fixed inset-0 z-[70] bg-[var(--color-scrim)] flex items-center justify-center p-3 sm:p-6" role="dialog" aria-modal="true">
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
            className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-md sm:text-md placeholder:text-ink-2"
          />
          {q && (
            <button type="button" onClick={() => setQ('')} className="p-1 text-ink-3 hover:text-ink cursor-pointer">
              <X className="w-4 h-4" />
            </button>
          )}
          <button
            type="button"
            onClick={onClose}
            className="shrink-0 whitespace-nowrap h-8 px-2.5 rounded-lg bg-canvas hover:bg-line text-xs font-semibold text-ink-2 cursor-pointer"
          >
            Kapat (Esc)
          </button>
        </div>

        {/* Modal Results List */}
        <div className="flex-1 min-h-0 overflow-y-auto p-3 sm:p-4 flex flex-col gap-2">
          {!q.trim() ? (
            <div className="py-12 text-center text-ink-3 text-base">
              <Search className="w-8 h-8 mx-auto mb-2 text-ink-3 opacity-40" />
              <p className="m-0 font-medium text-ink-2">Bu dersteki tüm slaytlar, klinik maddeler ve akıl kartları taranır.</p>
              <p className="m-0 text-sm mt-1">Aramak istediğin tıbbi kavramı yazmaya başla (örn. forniks, trabekülasyon, POD, pyelointerstisyel, BPH)...</p>
            </div>
          ) : results.length === 0 ? (
            <div className="py-12 text-center text-ink-3 text-base">
              <p className="m-0 font-medium text-ink-2">"{q}" için ders içeriğinde eşleşme bulunamadı.</p>
              <p className="m-0 text-sm mt-1">Farklı bir tıp terimi ya da kelime kökü dene.</p>
            </div>
          ) : (
            <>
              <div className="text-xs font-semibold text-ink-3 px-1 pb-1">
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
                    <span className="font-semibold text-sm text-accent flex items-center gap-1.5">
                      <span className="font-mono text-2xs px-1.5 py-0.5 rounded bg-accent-soft text-accent">
                        Slayt {r.slideNumber}
                      </span>
                      <span className="truncate">{r.slideTitle}</span>
                    </span>
                    <span className="text-2xs font-semibold text-ink-2 bg-black/5 px-2 py-0.5 rounded">
                      {r.matchedType}
                    </span>
                  </div>
                  <p className="m-0 text-base leading-[1.5] text-ink line-clamp-2">
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
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-xs font-semibold bg-bad/10 text-bad-text border border-bad/20 shadow-2xs">
          <span className="w-1.5 h-1.5 rounded-full bg-bad shrink-0" />
          <Rich text={cellText} />
        </span>
      );
    }

    // 2. Green / Emerald (Benign, Normal, Negative, Good prognosis)
    const isGreen =
      /\b(benign|iyi huylu|normal|negatif|kür|yüksek sağkalım|spontan geriler|reversibl|minimal)\b/i.test(t);

    if (isGreen) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-xs font-medium bg-ok/10 text-ok border border-ok/20 shadow-2xs">
          <span className="w-1.5 h-1.5 rounded-full bg-ok shrink-0" />
          <Rich text={cellText} />
        </span>
      );
    }

    // 3. Amber (Warning, Pitfall, Moderate risk, Variable, Recurrence)
    const isAmber =
      /\b(tuzak|dikkat|şüpheli|orta risk|değişken|relaps sık|sık nüks|subklinik)\b/i.test(t);

    if (isAmber) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-xs font-medium bg-warn/10 text-warn border border-warn/20 shadow-2xs">
          <span className="w-1.5 h-1.5 rounded-full bg-warn shrink-0" />
          <Rich text={cellText} />
        </span>
      );
    }

    // 4. Blue / Indigo (Diagnostic Criteria, Gold standard, Specific hallmark)
    const isBlue =
      /\b(altın standart|tanı kriteri|patognomonik|spike and dome|hump|tram-track|kresent|lineer if|granüler if)\b/i.test(t);

    if (isBlue) {
      return (
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-xs font-medium bg-accent/10 text-accent border border-accent/20 shadow-2xs">
          <span className="w-1.5 h-1.5 rounded-full bg-accent shrink-0" />
          <Rich text={cellText} />
        </span>
      );
    }

    return <Rich text={cellText} />;
  };

  return (
    <div className={`rounded-xl border border-line overflow-hidden bg-white shadow-2xs ${compact ? 'mt-1' : 'mt-2.5'}`}>
      {/* Table Header Banner */}
      <div className="px-3.5 py-2 bg-canvas text-xs font-bold border-b border-line text-ink flex items-center justify-between gap-2">
        <div className="flex items-center gap-2 min-w-0">
          <span className="w-2 h-2 rounded-full bg-accent shrink-0 shadow-2xs" />
          <span className="truncate">{table.title || 'Klinik & Patolojik Karşılaştırma Tablosu'}</span>
        </div>
        {isDiffDiagnosis && (
          <span className="shrink-0 text-2xs font-bold uppercase tracking-wider bg-accent-soft text-accent border border-accent/20 px-2 py-0.5 rounded-full shadow-2xs">
            Ayırıcı Tanı & Sınıflama
          </span>
        )}
      </div>

      <div className="overflow-x-auto custom-scrollbar">
        <table className={`w-full border-collapse ${table.headers.length >= 4 || compact ? 'text-xs' : 'text-sm sm:text-sm'}`}>
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
                      <span className="text-accent text-2xs"></span>
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
        <span className="text-xs font-bold uppercase tracking-wider text-ink-3 flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-accent" />
          <span>Kritik Ders Notları, Spotlar ve Ayırt Edici Özellikler</span>
        </span>
        <span className="text-2xs font-mono font-semibold text-ink-3 bg-canvas px-2 py-0.5 rounded-md border border-line">
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

          let badgeCls = 'bg-ok/10 text-ok border-ok/20';
          let borderCls = 'bg-ok-soft/20 border-line-soft';
          let icon = <BookOpen className="w-3.5 h-3.5 text-ok shrink-0" />;

          if (isRed) {
            badgeCls = 'bg-bad/10 text-bad-text border-bad/30';
            borderCls = 'bg-bad-soft/40 border-bad/20';
            icon = <AlertTriangle className="w-3.5 h-3.5 text-bad-text shrink-0" />;
          } else if (isAmber) {
            badgeCls = 'bg-warn/10 text-warn border-warn/30';
            borderCls = 'bg-warn-soft/40 border-warn/20';
            icon = <Lightbulb className="w-3.5 h-3.5 text-warn shrink-0" />;
          } else if (isBlue) {
            badgeCls = 'bg-accent/10 text-accent border-accent/30';
            borderCls = 'bg-accent-soft/40 border-accent/20';
            icon = <ArrowLeftRight className="w-3.5 h-3.5 text-accent shrink-0" />;
          } else if (isPurple) {
            badgeCls = 'bg-ai/10 text-ai border-ai/30';
            borderCls = 'bg-ai-soft/40 border-ai/20';
            icon = <RotateCcw className="w-3.5 h-3.5 text-ai shrink-0" />;
          }

          return (
            <div
              key={i}
              className={`rounded-xl p-3 sm:p-3.5 border transition-all duration-150 flex items-start gap-3 shadow-2xs ${borderCls}`}
            >
              <div className="mt-0.5 shrink-0 flex flex-col items-center gap-1">
                <span className="w-6 h-6 rounded-lg bg-white/90 shadow-2xs border border-line flex items-center justify-center">
                  {icon}
                </span>
                <span className="text-2xs font-mono font-bold text-ink-3">
                  #{i + 1}
                </span>
              </div>

              <div className="flex flex-col gap-1 min-w-0 flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className={`text-2xs font-bold px-2 py-0.5 rounded-md border shadow-2xs ${badgeCls}`}>
                    {b.title}
                  </span>
                </div>
                <div className="text-sm sm:text-sm text-ink leading-relaxed font-normal">
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
  <section className={`rounded-2xl border-2 border-warn/90 bg-gradient-to-br from-warn-soft/95 via-warn-soft/40 to-warn-soft/60 shadow-sm flex flex-col ${compact ? 'p-3 gap-2.5' : 'p-4 sm:p-5 gap-3.5'}`}>
    <header className="flex items-center gap-2.5 pb-2.5 border-b border-warn/80 ">
      <span className="w-8 h-8 rounded-xl bg-gradient-to-br from-warn to-warn text-white flex items-center justify-center shrink-0 shadow-xs" aria-hidden="true">
        <Lightbulb className="w-4.5 h-4.5" />
      </span>
      <div className="min-w-0">
        <span className="text-xs sm:text-sm font-black uppercase tracking-wider text-warn block">
          {title}
        </span>
        <span className="text-2xs text-warn/80 font-medium">
          Komite ve kurul sınavlarında doğrudan puan getiren kilit prensipler
        </span>
      </div>
      <span className="ml-auto font-mono text-xs font-bold text-warn bg-warn/80 px-2.5 py-0.5 rounded-full border border-warn/30 ">
        {items.length} Spot
      </span>
    </header>
    {note && <p className="m-0 -mt-1 text-sm text-warn/80 font-medium">{note}</p>}
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
                ? 'border-l-bad bg-bad-soft/90 border-bad/30 text-bad-text '
                : isBlue
                ? 'border-l-accent bg-accent-soft/90 border-accent/30 text-accent '
                : 'border-l-warn bg-white border-warn/80 text-ink'
            } p-3 sm:p-3.5 text-sm sm:text-base leading-[1.65]`}
          >
            <div className="flex items-center justify-between gap-2 mb-1.5 pb-1 border-b border-inherit/20">
              <span className="inline-flex items-center gap-1.5">
                {isRed ? (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-2xs font-bold bg-bad-soft text-bad-text ">
                    <AlertCircle className="w-3 h-3" /> {pBadge ? pBadge.replace(/^[🚨]\s*/, '') : 'KRİTİK UYARI'}
                  </span>
                ) : isBlue ? (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-2xs font-bold bg-accent-soft text-accent ">
                    <HelpCircle className="w-3 h-3" /> {pBadge ? pBadge.replace(/^[❓]\s*/, '') : 'ÇIKMIŞ SORU ODAĞI'}
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-2xs font-bold bg-warn-soft text-warn ">
                    <Lightbulb className="w-3 h-3 text-warn" /> {pBadge ? pBadge.replace(/^[💡]\s*/, '') : 'SINAV SPOTU'}
                  </span>
                )}
              </span>
              <span className="font-mono text-2xs font-bold text-ink-3">#{i + 1}</span>
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
                    <div key={lIdx} className="ml-3 pl-2.5 py-0.5 border-l-2 border-warn/30 text-sm flex items-start gap-1.5 text-ink-2">
                      <span className="text-2xs opacity-70 mt-1 select-none">▫</span>
                      <span className="min-w-0 flex-1"><Rich text={cleanText} /></span>
                    </div>
                  );
                }

                if (isUpperBullet) {
                  const cleanText = trimmed.replace(/^([•*]|\d+\.)\s*/, '');
                  return (
                    <div key={lIdx} className="font-semibold flex items-start gap-2 pt-0.5 text-ink">
                      <span className="w-1.5 h-1.5 rounded-full bg-warn mt-2 shrink-0" />
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
            <span className="text-sm font-bold text-ink">Kapsamlı Ders Notu Sentezi</span>
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
          <span className="text-xs font-semibold uppercase text-accent">{c.formulaBox.title}</span>
          <code className="font-mono text-sm text-ink">{c.formulaBox.formula}</code>
          {c.formulaBox.explanation && <span className="text-xs text-ink-2">{c.formulaBox.explanation}</span>}
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
      // safeJsonFetch honours the custom API URL (Oracle / tünel)
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
          <span className="text-xs font-semibold text-ink-2 px-1">Hazır sorular</span>
          {slide.aiPromptSuggestions.map((s, i) => (
            <button
              key={i}
              type="button"
              disabled={loading}
              onClick={() => ask(s)}
              className="text-left rounded-lg border border-line px-2.5 py-2 text-sm leading-snug hover:border-accent cursor-pointer disabled:opacity-50 transition-colors"
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
          <label htmlFor="deck-ai-model-select" className="text-xs font-semibold text-ink-2 inline-flex items-center gap-1.5">
            <BrainCircuit className="w-3.5 h-3.5 text-accent" />
            <span>Yapay Zeka Modeli:</span>
          </label>
          <select
            id="deck-ai-model-select"
            value={selectedModel}
            disabled={loading}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="bg-white border border-line-2 rounded-md px-2 py-0.5 text-xs font-medium text-ink outline-none cursor-pointer focus:border-accent disabled:opacity-50"
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
          className="resize-none border border-line-2 rounded-[10px] px-3 py-2.5 text-base bg-field outline-0 focus:border-accent"
        />
        <button
          type="submit"
          disabled={loading || !q.trim()}
          className="h-10 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-base font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
        >
          {loading ? <Sparkles className="w-4 h-4 animate-pulse" /> : <Send className="w-4 h-4" />}
          {loading ? 'Yanıt hazırlanıyor…' : 'Sor'}
        </button>
      </form>
      {loading && <AiThinking />}
      {answer && (
        <div className="rounded-xl bg-accent-soft border border-accent/20 p-3.5 flex flex-col gap-2.5 shadow-2xs" role="status">
          <div className="flex items-center justify-between gap-2 flex-wrap border-b border-accent/15 pb-2">
            <span className="inline-flex items-center gap-1.5 text-sm font-bold text-accent">
              <Sparkles className="w-3.5 h-3.5" /> AI Yanıtı
            </span>
            {modelUsed && (
              <span
                className="inline-flex items-center gap-1.5 text-2xs font-medium bg-white/95 text-ink-2 px-2.5 py-0.5 rounded-full border border-accent/25 shadow-2xs"
                title={`Bu yanıtı üreten yapay zeka: ${modelUsed}`}
              >
                <Bot className="w-3.5 h-3.5 text-accent shrink-0" />
                <span className="text-ink-3">Model:</span>
                <span className="font-semibold text-accent font-mono">{formatAiModelDisplayName(modelUsed)}</span>
              </span>
            )}
          </div>
          <div className="text-base leading-[1.65] text-ink whitespace-pre-line">
            <Rich text={answer.replace(/^#+\s*/gm, '').replace(/^>\s?/gm, '')} />
          </div>
          {refs.length > 0 && (
            <ul className="list-none m-0 p-0 flex flex-col gap-1 border-t border-accent/15 pt-2">
              {refs.slice(0, 4).map((r: any, i: number) => (
                <li key={i} className="text-xs text-ink-2 truncate flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-accent shrink-0" />
                  <span>{r.title || r.noteTitle || r.source || `Kaynak ${i + 1}`}</span>
                </li>
              ))}
            </ul>
          )}
          <div className="flex items-center justify-between gap-2 pt-2 border-t border-accent/15 text-2xs text-ink-3">
            {modelUsed && (
              <span className="inline-flex items-center gap-1 text-2xs text-ink-2">
                <span>Kullanılan Yapay Zeka:</span>
                <strong className="text-ink font-mono font-medium">{formatAiModelDisplayName(modelUsed)}</strong>
              </span>
            )}
            <button
              type="button"
              onClick={handleCopy}
              className="inline-flex items-center gap-1 text-xs text-ink-2 hover:text-ink cursor-pointer px-2 py-0.5 rounded hover:bg-white/60 transition-colors ml-auto"
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

/** Bir dersin birden çok sürümü varsa (V1, V2…) öğrenci hangisini açacağını ölçülere bakarak seçer. */
const VersionPicker: React.FC<{
  versions: DeckCatalogEntry[];
  progress: DeckProgress;
  onClose: () => void;
  onPick: (id: string) => void;
}> = ({ versions, progress, onClose, onPick }) => {
  const base = versions[0];
  return (
    <Dialog title={base.shortTitle || base.title} subtitle="Bu dersin birden çok sürümü var. Hangisini açmak istersin?" onClose={onClose}>
      <ul className="flex flex-col gap-3">
        {versions.map((v) => {
          const adim = v.slideCount || 0;
          const etk = v.interactiveCount ?? 0;
          const kelime = v.wordCount ?? 0;
          const dk = Math.max(1, Math.round(kelime / 180 + etk * 0.4));
          const seen = progress[v.id]?.seen?.length || 0;
          const detay = adim ? (kelime / adim >= 130 ? 'Ayrıntılı anlatım' : kelime / adim >= 90 ? 'Orta yoğunluk' : 'Kısa ve öz') : '';
          return (
            <li key={v.id}>
              <button
                type="button"
                onClick={() => onPick(v.id)}
                className="w-full text-left rounded-xl border border-line-soft hover:border-accent p-4 transition-colors cursor-pointer"
              >
                <div className="flex items-center gap-2">
                  <span className="ui-tag is-accent font-semibold">{v.versionLabel || 'V1'}</span>
                  <b className="min-w-0 truncate">{v.versionNote || (v.versionLabel && v.versionLabel !== 'V1' ? 'Yeni sürüm' : 'İlk sürüm')}</b>
                  {seen > 0 && <span className="ui-tag ml-auto">{seen}/{adim} adım görüldü</span>}
                </div>
                <dl className="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-3 text-sm">
                  <div><dt className="text-ink-3 text-xs">Adım</dt><dd className="font-semibold">{adim}</dd></div>
                  <div><dt className="text-ink-3 text-xs">Etkileşim</dt><dd className="font-semibold">{etk}</dd></div>
                  <div><dt className="text-ink-3 text-xs">Uzunluk</dt><dd className="font-semibold">~{dk} dk · {kelime.toLocaleString('tr-TR')} kelime</dd></div>
                  <div><dt className="text-ink-3 text-xs">Boyut</dt><dd className="font-semibold">{v.sizeKb ? `${v.sizeKb} KB` : '–'}</dd></div>
                </dl>
                {detay && <p className="text-xs text-ink-2 mt-2">{detay} · adım başına ~{adim ? Math.round(kelime / adim) : 0} kelime, {adim ? (etk / adim).toFixed(1) : 0} etkileşim</p>}
              </button>
            </li>
          );
        })}
      </ul>
    </Dialog>
  );
};
