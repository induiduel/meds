import React, { createContext, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  X,
  Volume2,
  BookOpen,
  Search,
  Sparkles,
  ExternalLink,
  ChevronRight,
  Filter,
} from 'lucide-react';
import { GLOSSARY } from '../../data/glossary';

// ---------------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------------
export interface GlossaryItem {
  term: string;
  aliases: string[];
  category: string;
  pronunciation?: string;
  definition: string;
  clinicalPearls?: string;
  badgeColor?: string;
}

export type TermTriggerSource = 'hover' | 'tap';

export interface ActiveGlossaryState {
  item: GlossaryItem;
  triggerRect?: DOMRect;
  source: TermTriggerSource;
}

export interface GlossaryContextValue {
  activeState: ActiveGlossaryState | null;
  showTerm: (item: GlossaryItem, rect?: DOMRect, source?: TermTriggerSource) => void;
  hideTerm: (immediate?: boolean) => void;
  lookupTerm: (termOrAlias: string) => GlossaryItem | undefined;
  glossaryList: GlossaryItem[];
  isDrawerOpen: boolean;
  setIsDrawerOpen: (open: boolean) => void;
  currentSlideText?: string;
  setCurrentSlideText?: (text: string) => void;
}

// ---------------------------------------------------------------------------
// Context
// ---------------------------------------------------------------------------
export const GlossaryContext = createContext<GlossaryContextValue | null>(null);

const fallbackGlossaryContext: GlossaryContextValue = {
  activeState: null,
  showTerm: () => {},
  hideTerm: () => {},
  lookupTerm: (termOrAlias: string) => {
    const q = (termOrAlias || '').trim().toLowerCase();
    return (GLOSSARY as unknown as GlossaryItem[]).find(
      (g) => g.term.toLowerCase() === q || (g.aliases || []).some((a) => a.toLowerCase() === q)
    );
  },
  glossaryList: GLOSSARY as unknown as GlossaryItem[],
  isDrawerOpen: false,
  setIsDrawerOpen: () => {},
  currentSlideText: '',
  setCurrentSlideText: () => {},
};

export const useGlossary = () => {
  const ctx = useContext(GlossaryContext);
  return ctx || fallbackGlossaryContext;
};

// ---------------------------------------------------------------------------
// Helper: Category Badge Styling
// ---------------------------------------------------------------------------
export const getCategoryBadgeStyle = (category: string, badgeColor?: string) => {
  switch (badgeColor || category.toLowerCase()) {
    case 'red':
    case 'bakteriyoloji':
      return 'bg-red-500/10 text-red-600 dark:text-red-400 border-red-500/20';
    case 'rose':
    case 'viroloji':
      return 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20';
    case 'purple':
    case 'tıbbi patoloji':
      return 'bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-500/20';
    case 'indigo':
    case 'genetik & dismorfoloji':
    case 'genetik & patoloji':
      return 'bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border-indigo-500/20';
    case 'teal':
    case 'latin / anatomi':
      return 'bg-teal-500/10 text-teal-600 dark:text-teal-400 border-teal-500/20';
    case 'blue':
    case 'üroloji / nefroloji':
      return 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/20';
    case 'cyan':
    case 'farmakoloji':
      return 'bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 border-cyan-500/20';
    case 'amber':
    case 'izolasyon':
    case 'epidemiyoloji':
      return 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20';
    default:
      return 'bg-accent-soft text-accent border-accent/20';
  }
};

// ---------------------------------------------------------------------------
// Provider Component
// ---------------------------------------------------------------------------
export const GlossaryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Normalised list (handles both glossary file shapes, skips entries without a definition)
  const glossaryList = GLOSSARY as GlossaryItem[];
  const [activeState, setActiveState] = useState<ActiveGlossaryState | null>(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [currentSlideText, setCurrentSlideText] = useState<string>('');
  const hideTimeoutRef = useRef<number | null>(null);

  // Fast lookup map (lowercased alias/term -> GlossaryItem)
  const lookupMap = useMemo(() => {
    const map = new Map<string, GlossaryItem>();
    glossaryList.forEach((item) => {
      map.set(item.term.toLowerCase(), item);
      item.aliases?.forEach((alias) => {
        map.set(alias.toLowerCase(), item);
      });
    });
    return map;
  }, [glossaryList]);

  const lookupTerm = (text: string): GlossaryItem | undefined => {
    return lookupMap.get(text.toLowerCase().trim());
  };

  const showTerm = (item: GlossaryItem, rect?: DOMRect, source: TermTriggerSource = 'tap') => {
    if (hideTimeoutRef.current) {
      window.clearTimeout(hideTimeoutRef.current);
      hideTimeoutRef.current = null;
    }
    setActiveState({ item, triggerRect: rect, source });
  };

  const hideTerm = (immediate: boolean = false) => {
    if (immediate) {
      if (hideTimeoutRef.current) {
        window.clearTimeout(hideTimeoutRef.current);
        hideTimeoutRef.current = null;
      }
      setActiveState(null);
      return;
    }

    // Debounced hide for hover
    if (hideTimeoutRef.current) {
      window.clearTimeout(hideTimeoutRef.current);
    }
    hideTimeoutRef.current = window.setTimeout(() => {
      setActiveState(null);
      hideTimeoutRef.current = null;
    }, 450);
  };

  return (
    <GlossaryContext.Provider
      value={{
        activeState,
        showTerm,
        hideTerm,
        lookupTerm,
        glossaryList,
        isDrawerOpen,
        setIsDrawerOpen,
        currentSlideText,
        setCurrentSlideText,
      }}
    >
      {children}
      <GlossaryLayer />
    </GlossaryContext.Provider>
  );
};

/**
 * In native fullscreen the browser only paints the fullscreen element's subtree, so the
 * popover and drawer must live inside it; otherwise they open invisibly.
 */
const GlossaryLayer: React.FC = () => {
  const [fsHost, setFsHost] = useState<Element | null>(() => (typeof document !== 'undefined' ? document.fullscreenElement : null));
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const update = () => setFsHost(document.fullscreenElement);
    document.addEventListener('fullscreenchange', update);
    document.addEventListener('webkitfullscreenchange', update);
    return () => {
      document.removeEventListener('fullscreenchange', update);
      document.removeEventListener('webkitfullscreenchange', update);
    };
  }, []);

  if (!mounted || typeof document === 'undefined') return null;

  const layer = (
    <div className="medical-glossary-portal-root">
      <FloatingGlossaryToast />
      <MedicalGlossaryDrawer />
    </div>
  );
  return createPortal(layer, fsHost || document.body);
};

// ---------------------------------------------------------------------------
// Dynamic Slide Clinical Synthesis / Knowledge Extractor
// ---------------------------------------------------------------------------
export function extractSlideKnowledge(item: GlossaryItem, slideText?: string): string | null {
  if (!slideText || !slideText.trim()) return null;

  const cleanTerm = item.term.replace(/\s*\([^)]*\)/g, '').trim().toLowerCase();
  const searchTerms = [
    cleanTerm,
    ...(item.aliases || []).map((a) => a.trim().toLowerCase()),
  ].filter((t) => t.length >= 2);

  const lines = slideText.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  const matchedSentences: string[] = [];

  for (const line of lines) {
    const lowerLine = line.toLowerCase();
    const hasMatch = searchTerms.some((st) => {
      if (st.length <= 4) {
        const reg = new RegExp(`(?<![\\p{L}\\p{N}])${st.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\p{L}\\p{N}])`, 'iu');
        return reg.test(lowerLine);
      }
      return lowerLine.includes(st);
    });

    if (hasMatch) {
      const cleaned = line
        .replace(/^[•\-\*]\s*/, '')
        .replace(/^>\s*/, '')
        .replace(/^[]\s*/, '')
        .trim();

      if (cleaned.length > 15) {
        matchedSentences.push(cleaned);
      }
    }
  }

  if (matchedSentences.length === 0) {
    const firstLine = lines[0] || '';
    const lowerFirstLine = firstLine.toLowerCase();
    const titleMatch = searchTerms.some((st) => lowerFirstLine.includes(st));
    if (titleMatch && lines.length > 1) {
      const narrativeLine = lines.find((l) => l.length > 25 && !l.startsWith('#')) || lines[1];
      if (narrativeLine) {
        return narrativeLine.replace(/^[•\-\*]\s*/, '').replace(/^>\s*/, '').trim();
      }
    }
    return null;
  }

  // Deduplicate and combine up to 2 distinct informative sentences/bullets
  const unique = Array.from(new Set(matchedSentences));
  const summary = unique.slice(0, 2).join(' • ');

  if (summary.length > 250) {
    return summary.slice(0, 247) + '...';
  }
  return summary;
}

// ---------------------------------------------------------------------------
// Floating Popover / Toast Component (Supports Touch Tap + Desktop Hover)
// ---------------------------------------------------------------------------
export const FloatingGlossaryToast: React.FC = () => {
  const { activeState, hideTerm, showTerm, setIsDrawerOpen, currentSlideText } = useGlossary();
  const [isSpeaking, setIsSpeaking] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);

  const slideKnowledge = useMemo(() => {
    if (!activeState?.item) return null;
    return extractSlideKnowledge(activeState.item, currentSlideText);
  }, [activeState?.item, currentSlideText]);

  // Close on Escape or click outside
  useEffect(() => {
    if (!activeState) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') hideTerm(true);
    };

    const handlePointerDownOutside = (e: PointerEvent) => {
      if (cardRef.current && !cardRef.current.contains(e.target as Node)) {
        // Only dismiss if source was tap
        if (activeState.source === 'tap') {
          hideTerm(true);
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('pointerdown', handlePointerDownOutside);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('pointerdown', handlePointerDownOutside);
    };
  }, [activeState, hideTerm]);

  if (!activeState) return null;

  const { item, triggerRect, source } = activeState;

  // Speak pronunciation
  const speakTerm = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!('speechSynthesis' in window)) return;
    try {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(item.term);
      utterance.lang = 'tr-TR';
      utterance.rate = 0.9;
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);
      window.speechSynthesis.speak(utterance);
    } catch {
      setIsSpeaking(false);
    }
  };

  // Determine position:
  // On mobile (<640px) or on tap source: bottom floating toast.
  // On desktop hover with triggerRect: anchored floating card near word.
  const isMobile = typeof window !== 'undefined' && window.innerWidth < 640;
  const isAnchored = !isMobile && source === 'hover' && triggerRect;

  let style: React.CSSProperties = {};
  if (isAnchored && triggerRect) {
    const cardWidth = 360;
    const cardHeightEst = 220;
    let top = triggerRect.bottom + 8;
    let left = triggerRect.left + triggerRect.width / 2 - cardWidth / 2;

    // Check bottom boundary
    if (top + cardHeightEst > window.innerHeight - 20) {
      top = Math.max(12, triggerRect.top - cardHeightEst - 8);
    }

    // Check horizontal boundaries
    if (left < 16) left = 16;
    if (left + cardWidth > window.innerWidth - 16) {
      left = window.innerWidth - cardWidth - 16;
    }

    style = {
      position: 'fixed',
      top: `${top}px`,
      left: `${left}px`,
      width: `${cardWidth}px`,
      zIndex: 99999,
    };
  } else {
    // Floating bottom toast / sheet
    style = {
      position: 'fixed',
      bottom: '24px',
      left: '50%',
      transform: 'translateX(-50%)',
      width: 'calc(100% - 32px)',
      maxWidth: '460px',
      zIndex: 99999,
    };
  }

  return (
    <div
      ref={cardRef}
      style={style}
      onMouseEnter={() => {
        // Moving from the word onto the card cancels the pending hover-hide
        if (source === 'hover') showTerm(item, triggerRect, 'hover');
      }}
      onMouseLeave={() => {
        if (source === 'hover') hideTerm(false);
      }}
      className="animate-in fade-in zoom-in-95 duration-150 rounded-2xl bg-white dark:bg-white backdrop-blur-md border border-line shadow-2xl p-4 sm:p-5 flex flex-col gap-2.5 text-ink select-text"
      role="dialog"
      aria-modal="false"
      aria-label={item.term}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span
              className={`text-[11.5px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border shadow-2xs ${getCategoryBadgeStyle(
                item.category,
                item.badgeColor
              )}`}
            >
              {item.category}
            </span>
            {item.pronunciation && (
              <span className="text-[11px] text-ink-3 italic font-mono">
                {item.pronunciation}
              </span>
            )}
          </div>
          <h4 className="text-[15px] sm:text-[16px] font-bold text-ink tracking-tight flex items-center gap-1.5 m-0">
            {item.term}
            {'speechSynthesis' in (typeof window !== 'undefined' ? window : {}) && (
              <button
                type="button"
                onClick={speakTerm}
                title="Sesli Telaffuz Et"
                className={`p-1 rounded-md text-ink-3 hover:text-accent hover:bg-accent-soft transition-colors ${
                  isSpeaking ? 'text-accent animate-pulse' : ''
                }`}
              >
                <Volume2 className="w-3.5 h-3.5" />
              </button>
            )}
          </h4>
        </div>

        <button
          type="button"
          onClick={() => hideTerm(true)}
          className="shrink-0 p-1.5 rounded-lg text-ink-3 hover:text-ink hover:bg-canvas transition-colors cursor-pointer"
          title="Kapat (ESC)"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Definition */}
      <p className="m-0 text-[12.5px] sm:text-[13px] text-ink-2 leading-relaxed">
        {item.definition}
      </p>

      {/* Dynamic Slide Clinical Synthesis / Slayt Patoloji Bilgisi */}
      {slideKnowledge && (
        <div className="p-2.5 rounded-xl bg-teal-500/10 dark:bg-teal-500/15 text-[11.5px] sm:text-[12px] text-ink-2 leading-snug flex items-start gap-2 animate-in fade-in duration-200 shadow-2xs">
          <span className="text-[13px] select-none shrink-0 mt-0.5"></span>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-1.5 mb-1">
              <strong className="font-semibold text-teal-900 dark:text-teal-200 text-[11.5px]">
                Slayttaki Bilgi & Patoloji Sentezi:
              </strong>
              <span className="text-[9.5px] font-bold uppercase tracking-wider bg-teal-500/20 text-teal-800 dark:text-teal-300 px-1 py-0.2 rounded">
                Bu Slayt
              </span>
            </div>
            <p className="m-0 text-ink leading-relaxed font-normal">
              {slideKnowledge}
            </p>
          </div>
        </div>
      )}

      {/* Clinical Pearl Box */}
      {item.clinicalPearls && (
        <div className="p-2.5 rounded-xl bg-amber-500/10 dark:bg-amber-500/15 text-[11.5px] sm:text-[12px] text-ink-2 leading-snug flex items-start gap-2">
          <span className="text-[13px] select-none shrink-0 mt-0.5"></span>
          <div className="min-w-0 flex-1">
            <strong className="font-semibold text-amber-900 dark:text-amber-200 block mb-0.5">
              Spot Sınav & Hoca İncisi:
            </strong>
            <span>{item.clinicalPearls}</span>
          </div>
        </div>
      )}

      {/* Footer / Helper hint */}
      <div className="pt-2 border-t border-line-soft flex items-center justify-end gap-1 text-[13px] text-ink-3 min-w-0">
        <div className="flex items-center gap-1 min-w-0">
          <a
            href={`/sozluk?id=${encodeURIComponent(item.term)}`}
            onClick={(e) => {
              e.preventDefault();
              hideTerm(true);
              window.location.href = `/sozluk?id=${encodeURIComponent(item.term)}`;
            }}
            className="h-9 px-3 rounded-lg text-accent hover:bg-accent-soft font-semibold inline-flex items-center gap-1 cursor-pointer whitespace-nowrap"
          >
            <span>Sözlükte aç</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
          <button
            type="button"
            onClick={() => {
              hideTerm(true);
              setIsDrawerOpen(true);
            }}
            className="h-9 px-3 rounded-lg hover:bg-canvas hover:text-ink font-medium transition-colors cursor-pointer inline-flex items-center gap-1 whitespace-nowrap"
          >
            <span>Tüm terimler</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Interactive Word Highlighter Span
// ---------------------------------------------------------------------------
export const GlossaryTermSpan: React.FC<{
  text: string;
  item: GlossaryItem;
}> = ({ text, item }) => {
  const { showTerm, hideTerm } = useGlossary();
  const spanRef = useRef<HTMLSpanElement>(null);

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    const rect = spanRef.current?.getBoundingClientRect();
    showTerm(item, rect, 'tap');
  };

  // Touch screens fire emulated mouseenter/leave around a tap; only a real mouse should hover
  const handlePointerEnter = (e: React.PointerEvent) => {
    if (e.pointerType !== 'mouse') return;
    const rect = spanRef.current?.getBoundingClientRect();
    showTerm(item, rect, 'hover');
  };

  const handlePointerLeave = (e: React.PointerEvent) => {
    if (e.pointerType !== 'mouse') return;
    hideTerm(false);
  };

  return (
    <span
      ref={spanRef}
      role="button"
      tabIndex={0}
      onClick={handleClick}
      onPointerDown={(e) => e.stopPropagation()}
      onPointerUp={(e) => {
        e.stopPropagation();
        const rect = spanRef.current?.getBoundingClientRect();
        showTerm(item, rect, 'tap');
      }}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          showTerm(item, spanRef.current?.getBoundingClientRect(), 'tap');
        }
      }}
      onPointerEnter={handlePointerEnter}
      onPointerLeave={handlePointerLeave}
      className="cursor-pointer font-semibold text-teal-800 dark:text-teal-200 bg-teal-500/15 dark:bg-teal-400/20 hover:bg-teal-500/25 dark:hover:bg-teal-400/30 underline decoration-2 underline-offset-[3px] decoration-teal-500/70 dark:decoration-teal-400/90 px-1 py-0.5 rounded transition-all duration-150 inline-flex items-baseline gap-0.5 select-text"
      title={`${item.term} (${item.category}) - Dokunun veya üzerine gelin`}
    >
      <span>{text}</span>
      <span className="text-[11px] text-teal-600 dark:text-teal-300 opacity-70 select-none"></span>
    </span>
  );
};

// ---------------------------------------------------------------------------
// Text Parser: Scans plain or markdown text and wraps matching terms
// ---------------------------------------------------------------------------
export const RenderWithGlossaryTerms: React.FC<{
  text: string;
  className?: string;
}> = ({ text, className }) => {
  const { glossaryList } = useGlossary();

  // Build sorted regex of all terms and aliases (longest first to avoid greedy substring collisions)
  const { regex, aliasToItem } = useMemo(() => {
    const map = new Map<string, GlossaryItem>();
    const patterns: string[] = [];
    const STOP_WORDS = new Set(['ile', 've', 'bir', 'için', 'gibi', 'daha', 'çok', 'tip', 'her', 'bu', 'şu', 'veya', 'olan', 'göre']);

    const addPattern = (raw: string, item: GlossaryItem) => {
      const clean = raw.trim();
      if (clean.length < 3) return;
      const lower = clean.toLowerCase();
      if (STOP_WORDS.has(lower)) return;
      patterns.push(clean);
      map.set(lower, item);
      map.set(clean.toLocaleLowerCase('tr-TR'), item);
    };

    glossaryList.forEach((item) => {
      // Add term directly
      addPattern(item.term, item);

      // Add clean term without parentheses
      const cleanTerm = item.term.replace(/\s*\([^)]*\)/g, '').trim();
      addPattern(cleanTerm, item);

      // Add parenthetical contents if any
      const parenMatch = item.term.match(/^(.+?)\s*\((.+?)\)$/);
      if (parenMatch) {
        addPattern(parenMatch[1], item);
        addPattern(parenMatch[2], item);
      }

      // Add aliases
      item.aliases?.forEach((alias) => {
        addPattern(alias, item);
      });
    });

    // Unique and sort by descending length
    const unique = Array.from(new Set(patterns)).sort((a, b) => b.length - a.length);

    if (unique.length === 0) {
      return { regex: /(?!x)x/, aliasToItem: map };
    }

    // Escape regex special chars
    const escaped = unique.map((p) => p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');

    // Use unicode character boundaries (?<![\p{L}\p{N}]) and (?![\p{L}\p{N}])
    const reg = new RegExp(`(?<![\\p{L}\\p{N}])(${escaped})(?![\\p{L}\\p{N}])`, 'giu');

    return { regex: reg, aliasToItem: map };
  }, [glossaryList]);

  // Multi-token parser: Bold (*** / **), Markers (==...== or <mark>...</mark>), Italics (*...* or _..._)
  const cleanText = useMemo(() => {
    return String(text || '')
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
  }, [text]);

  const tokenRegex = /(\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|==[^=]+==|<mark>[^<]+<\/mark>|\*[^*\n]+\*|_[^_\n]+_)/g;
  const parts = cleanText.split(tokenRegex);

  return (
    <span className={className}>
      {parts.map((part, pIdx) => {
        if (!part) return null;

        const isTriple = part.startsWith('***') && part.endsWith('***');
        const isDouble = part.startsWith('**') && part.endsWith('**');
        const isBold = isTriple || isDouble;
        const isMarker = (part.startsWith('==') && part.endsWith('==')) || (part.startsWith('<mark>') && part.endsWith('</mark>'));
        const isItalic = (part.startsWith('*') && part.endsWith('*') && !isBold) || (part.startsWith('_') && part.endsWith('_'));

        let rawContent = part;
        if (isTriple) rawContent = part.slice(3, -3);
        else if (isDouble) rawContent = part.slice(2, -2);
        else if (part.startsWith('==') && part.endsWith('==')) rawContent = part.slice(2, -2);
        else if (part.startsWith('<mark>') && part.endsWith('</mark>')) rawContent = part.slice(6, -7);
        else if (isItalic) rawContent = part.slice(1, -1);

        // Marker color variants (e.g. ==red:...==, ==kırmızı:...==, ==blue:...==, ==mavi:...==)
        let markerColor: 'yellow' | 'red' | 'blue' = 'yellow';
        if (isMarker) {
          if (/^(?:red:|kırmızı:|onemli:|önemli:)/i.test(rawContent)) {
            markerColor = 'red';
            rawContent = rawContent.replace(/^(?:red:|kırmızı:|onemli:|önemli:)/i, '').trim();
          } else if (/^(?:blue:|mavi:|cikmis:|çıkmış:|soru:)/i.test(rawContent)) {
            markerColor = 'blue';
            rawContent = rawContent.replace(/^(?:blue:|mavi:|cikmis:|çıkmış:|soru:)/i, '').trim();
          }
        }

        // Split rawContent by medical terms regex
        const termParts = rawContent.split(regex);
        const renderedContent = termParts.map((tPart, tIdx) => {
          if (!tPart) return null;
          const matchedItem = aliasToItem.get(tPart.toLowerCase()) || aliasToItem.get(tPart.toLocaleLowerCase('tr-TR'));
          if (matchedItem) {
            return <GlossaryTermSpan key={tIdx} text={tPart} item={matchedItem} />;
          }
          return <React.Fragment key={tIdx}>{tPart}</React.Fragment>;
        });

        // 1. Marker Highlight rendering
        if (isMarker) {
          if (markerColor === 'red') {
            return (
              <mark
                key={pIdx}
                className="bg-red-100/90 dark:bg-red-950/50 text-red-800 dark:text-red-200 underline decoration-2 underline-offset-[3px] decoration-red-500 px-1.5 py-0.5 rounded font-semibold not-italic inline-flex items-center gap-1 shadow-2xs"
                title="Önemli / Kritik Vurgu"
              >
                <span className="text-[11px] select-none text-red-500"></span>
                <span>{renderedContent}</span>
              </mark>
            );
          }
          if (markerColor === 'blue') {
            return (
              <mark
                key={pIdx}
                className="bg-blue-100/90 dark:bg-blue-950/50 text-blue-800 dark:text-blue-200 underline decoration-2 underline-offset-[3px] decoration-blue-500 px-1.5 py-0.5 rounded font-semibold not-italic inline-flex items-center gap-1 shadow-2xs"
                title="Sorulmuş / Çıkmış Sınav Sorusu"
              >
                <span className="text-[11px] select-none text-blue-500"></span>
                <span>{renderedContent}</span>
              </mark>
            );
          }
          return (
            <mark
              key={pIdx}
              className="ms-marker-animated shadow-2xs not-italic cursor-default"
              title="Vurgulanmış Temel Bilgi"
            >
              {renderedContent}
            </mark>
          );
        }

        // 2. Bold rendering (Kırmızı = Önemli, Mavi = Sorulmuş Soru, Standart = Vurgulu)
        if (isBold) {
          const isRed =
            isTriple ||
            /^(?:||)/.test(rawContent.trim()) ||
            /(?:ölümcül|asla|acil|hayati|kritik|dikkat!|sınav tuzağı|tuzak:|hayat kurtarır|kontrendike|önemli|\[kırmızı|\[red)/i.test(rawContent);

          const isBlue =
            !isRed &&
            (/^(?:||)/.test(rawContent.trim()) ||
              /(?:çıkmış soru|çıkmış|komite sorusu|tus sorusu|soruldu|ösym|sınav sorusu|sınavda soruldu|\[mavi|\[blue|\[çıkmış)/i.test(rawContent));

          if (isRed) {
            return (
              <strong
                key={pIdx}
                className="font-bold text-red-600 dark:text-red-400 bg-red-500/10 dark:bg-red-500/20 border border-red-500/30 px-1.5 py-0.5 rounded shadow-2xs inline-flex items-center gap-1 my-0.5"
                title="Önemli Bilgi"
              >
                {!rawContent.includes('') && !rawContent.includes('') && !rawContent.includes('') && (
                  <span className="text-[11px] select-none text-red-500"></span>
                )}
                <span>{renderedContent}</span>
              </strong>
            );
          }

          if (isBlue) {
            return (
              <strong
                key={pIdx}
                className="font-bold text-blue-600 dark:text-blue-400 bg-blue-500/10 dark:bg-blue-500/20 border border-blue-500/30 px-1.5 py-0.5 rounded shadow-2xs inline-flex items-center gap-1 my-0.5"
                title="Sorulmuş / Çıkmış Soru"
              >
                {!rawContent.includes('') && !rawContent.includes('') && !rawContent.includes('') && (
                  <span className="text-[11px] select-none text-blue-500"></span>
                )}
                <span>{renderedContent}</span>
              </strong>
            );
          }

          return (
            <strong
              key={pIdx}
              className="font-bold text-ink bg-amber-100/60 dark:bg-amber-950/40 px-1 py-0.5 rounded shadow-2xs"
            >
              {renderedContent}
            </strong>
          );
        }

        // 3. Italic rendering
        if (isItalic) {
          return (
            <em key={pIdx} className="italic text-ink-2 font-medium">
              {renderedContent}
            </em>
          );
        }

        // 4. Regular text with medical term popovers
        return <React.Fragment key={pIdx}>{renderedContent}</React.Fragment>;
      })}
    </span>
  );
};

// ---------------------------------------------------------------------------
// Medical Glossary Drawer / Reference Modal
// ---------------------------------------------------------------------------
export const MedicalGlossaryDrawer: React.FC = () => {
  const { glossaryList, isDrawerOpen, setIsDrawerOpen, showTerm } = useGlossary();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('Tümü');

  const categories = useMemo(() => {
    const set = new Set<string>();
    glossaryList.forEach((g) => set.add(g.category));
    return ['Tümü', ...Array.from(set).sort()];
  }, [glossaryList]);

  const filtered = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    return glossaryList.filter((item) => {
      const matchCat = selectedCategory === 'Tümü' || item.category === selectedCategory;
      if (!matchCat) return false;
      if (!q) return true;
      const matchTerm = item.term.toLowerCase().includes(q);
      const matchDef = item.definition.toLowerCase().includes(q);
      const matchAlias = item.aliases?.some((a) => a.toLowerCase().includes(q));
      const matchPearl = item.clinicalPearls?.toLowerCase().includes(q);
      return matchTerm || matchDef || matchAlias || matchPearl;
    });
  }, [glossaryList, searchQuery, selectedCategory]);

  if (!isDrawerOpen) return null;

  return (
    <div
      className="fixed inset-0 z-[99999] flex justify-end bg-black/50 backdrop-blur-[3px] animate-in fade-in duration-200"
      onClick={() => setIsDrawerOpen(false)}
    >
      <div
        className="w-full max-w-xl h-full bg-white border-l border-line flex flex-col shadow-2xl animate-in slide-in-from-right duration-250 select-text"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Drawer Header */}
        <div className="p-4 sm:p-5 border-b border-line flex items-center justify-between gap-3 bg-field">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-accent-soft text-accent flex items-center justify-center shrink-0">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-[16px] font-bold text-ink m-0 tracking-tight">
                Tıbbi Terimler & Glosser
              </h3>
              <p className="text-[12px] text-ink-3 m-0">
                Kurul 1 Latin Terimleri, Bakteriler, Virüsler ve Patoloji Sözlüğü ({glossaryList.length} Terim)
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={() => setIsDrawerOpen(false)}
            className="p-2 rounded-xl text-ink-3 hover:text-ink hover:bg-canvas transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search & Filter Bar */}
        <div className="p-4 border-b border-line-soft flex flex-col gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-ink-3 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Terim, bakteri, virüs veya semptom ara..."
              className="w-full pl-10 pr-4 py-2 text-[13px] bg-canvas border border-line-soft rounded-xl text-ink placeholder:text-ink-3 focus:outline-hidden focus:border-accent"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-3 hover:text-ink"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* Category Tabs */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-thin">
            {categories.map((cat) => (
              <button
                key={cat}
                type="button"
                onClick={() => setSelectedCategory(cat)}
                className={`px-2.5 py-1 rounded-lg text-[11.5px] font-medium whitespace-nowrap transition-colors cursor-pointer ${
                  selectedCategory === cat
                    ? 'bg-accent text-white shadow-2xs'
                    : 'bg-canvas text-ink-3 hover:text-ink hover:bg-line-soft'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Term List */}
        <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
          {filtered.length === 0 ? (
            <div className="p-8 text-center text-ink-3 text-[13px]">
              Eşleşen tıbbi terim bulunamadı.
            </div>
          ) : (
            filtered.map((item, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-xl border border-line-soft bg-canvas/60 hover:bg-field transition-colors flex flex-col gap-2"
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span
                      className={`text-[11px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${getCategoryBadgeStyle(
                        item.category,
                        item.badgeColor
                      )}`}
                    >
                      {item.category}
                    </span>
                    {item.pronunciation && (
                      <span className="text-[11px] text-ink-3 italic font-mono">
                        {item.pronunciation}
                      </span>
                    )}
                  </div>

                  <button
                    type="button"
                    onClick={(e) => {
                      const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
                      showTerm(item, rect, 'tap');
                      setIsDrawerOpen(false);
                    }}
                    className="text-[11px] text-accent hover:underline font-medium flex items-center gap-1 cursor-pointer"
                  >
                    <span>Toast Gör</span>
                    <ExternalLink className="w-3 h-3" />
                  </button>
                </div>

                <h4 className="text-[14.5px] font-bold text-ink m-0 tracking-tight">
                  {item.term}
                </h4>

                <p className="text-[12.5px] text-ink-2 leading-relaxed m-0">
                  {item.definition}
                </p>

                {item.clinicalPearls && (
                  <div className="p-2 rounded-lg bg-amber-500/10 text-[11.5px] text-ink-2 leading-snug flex items-start gap-1.5">
                    <span className="text-[12px] select-none shrink-0"></span>
                    <span>{item.clinicalPearls}</span>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Slide-level Quick Terms Pills Strip
// ---------------------------------------------------------------------------
export const SlideTermsPills: React.FC<{
  textToScan: string;
  className?: string;
}> = ({ textToScan, className }) => {
  const { glossaryList, showTerm } = useGlossary();

  const foundTerms = useMemo(() => {
    if (!textToScan) return [];
    const textLower = textToScan.toLowerCase();
    const matches: GlossaryItem[] = [];
    const seen = new Set<string>();

    glossaryList.forEach((item) => {
      const baseTerm = item.term.replace(/\s*\([^)]*\)/g, '').toLowerCase().trim();
      const hasTerm = baseTerm.length >= 3 && textLower.includes(baseTerm);
      const hasAlias = item.aliases?.some((a) => a.length >= 3 && textLower.includes(a.toLowerCase()));

      if ((hasTerm || hasAlias) && !seen.has(item.term)) {
        seen.add(item.term);
        matches.push(item);
      }
    });

    return matches.slice(0, 10);
  }, [textToScan, glossaryList]);

  if (foundTerms.length === 0) return null;
  // Aynı terim iki kez görünmesin (ör. "Apoptoz" hem kısa hem uzun adıyla)
  const seen = new Set<string>();
  const uniqueTerms = foundTerms.filter((t) => {
    const k = t.term.toLocaleLowerCase('tr').split(' (')[0];
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });

  return (
    <div className={`ms-terms flex items-center gap-1.5 flex-wrap p-2 rounded-xl bg-teal-500/5 dark:bg-teal-500/10 border border-teal-500/15 ${className || ''}`}>
      <span className="text-[11px] font-semibold text-teal-800 dark:text-teal-300 flex items-center gap-1 shrink-0">
        <Sparkles className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" />
        <span>Slayt Tıbbi Terimleri:</span>
      </span>
      {uniqueTerms.map((term, i) => (
        <button
          key={i}
          type="button"
          onClick={(e) => {
            const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
            showTerm(term, rect, 'tap');
          }}
          className={`px-2 py-0.5 rounded-full text-[11px] font-medium border cursor-pointer hover:scale-105 active:scale-95 transition-all shadow-2xs ${getCategoryBadgeStyle(
            term.category,
            term.badgeColor
          )}`}
          title={`${term.term} (${term.category}) - Tanımı görmek için tıklayın/dokunun`}
        >
          {term.term}
        </button>
      ))}
    </div>
  );
};
