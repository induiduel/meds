import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  BookOpen,
  Search,
  FileText,
  Copy,
  Check,
  Clock,
  Sparkles,
  AlertTriangle,
  ChevronRight,
  ChevronDown,
  ChevronUp,
  X,
  Printer,
  Download,
  GraduationCap,
  BookMarked,
  Layers,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Maximize2,
  Minimize2,
  List,
  Sun,
  Moon,
  Coffee,
  Highlighter,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Stethoscope,
  Pill,
  Dna,
  Flame,
  Bookmark,
  Eye,
  EyeOff,
  Table as TableIcon,
  Compass,
  ArrowUp,
  Share2,
  User,
  Calendar,
  Building
} from 'lucide-react';
import { SummaryDetail } from './LectureSummariesView';

interface SummaryArtifactReaderProps {
  summary: SummaryDetail;
  onClose: () => void;
  onOpenPdfModal?: () => void;
}

type ReaderTheme = 'light' | 'sepia' | 'dark' | 'cobalt';
type LineHeightMode = 'tight' | 'normal' | 'relaxed';
type FontFamily = 'sans' | 'serif';
type WidthMode = 'standard' | 'wide' | 'fullscreen';

interface ParsedDossier {
  rawTitle?: string;
  courseCode?: string;
  instructor?: string;
  term?: string;
  sources?: string;
  group?: string;
}

interface TocItem {
  id: string;
  title: string;
  level: number;
  type: 'section' | 'sub' | 'spot' | 'question' | 'table';
}

interface QuestionBlock {
  id: string;
  number: string;
  examTag?: string;
  stem: string;
  options: { letter: string; text: string }[];
  answer?: string;
  explanation?: string;
}

interface TableBlock {
  headers: string[];
  rows: string[][];
}

interface CalloutBlock {
  type: 'warning' | 'important' | 'tip' | 'note';
  title?: string;
  content: string;
}

interface BulletItem {
  key?: string;
  content: string;
  subItems?: string[];
  numberedPills?: string[];
}

export const SummaryArtifactReader: React.FC<SummaryArtifactReaderProps> = ({
  summary,
  onClose,
  onOpenPdfModal,
}) => {
  // Reading Preferences (Stored in localStorage for persistence)
  const [fontScale, setFontScale] = useState<number>(() => {
    try {
      const saved = localStorage.getItem('medsoru_reader_font_scale');
      return saved ? parseInt(saved, 10) : 100;
    } catch {
      return 100;
    }
  });

  const [lineHeight, setLineHeight] = useState<LineHeightMode>('normal');
  const [fontFamily, setFontFamily] = useState<FontFamily>('sans');
  const [theme, setTheme] = useState<ReaderTheme>(() => {
    try {
      const saved = localStorage.getItem('medsoru_reader_theme') as ReaderTheme;
      return saved || 'light';
    } catch {
      return 'light';
    }
  });
  const [widthMode, setWidthMode] = useState<WidthMode>('standard');
  const [markerMode, setMarkerMode] = useState<boolean>(true);
  const [showToc, setShowToc] = useState<boolean>(true);

  // Search in document
  const [searchQuery, setSearchQuery] = useState('');
  const [activeMatchIndex, setActiveMatchIndex] = useState(0);

  // Interactive Question State
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const [revealedAnswers, setRevealedAnswers] = useState<Record<string, boolean>>({});

  // Scroll Progress & Active Section
  const [scrollProgress, setScrollProgress] = useState(0);
  const [activeSectionId, setActiveSectionId] = useState<string>('');
  const [copied, setCopied] = useState(false);
  const [copiedSpot, setCopiedSpot] = useState(false);

  const containerRef = useRef<HTMLDivElement>(null);
  const contentAreaRef = useRef<HTMLDivElement>(null);

  // Save preferences
  useEffect(() => {
    try {
      localStorage.setItem('medsoru_reader_font_scale', fontScale.toString());
      localStorage.setItem('medsoru_reader_theme', theme);
    } catch {}
  }, [fontScale, theme]);

  // Handle escape key to close
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  // Track scroll progress and active section
  const handleScroll = () => {
    const el = contentAreaRef.current;
    if (!el) return;
    const { scrollTop, scrollHeight, clientHeight } = el;
    const progress = Math.min(100, Math.max(0, Math.round((scrollTop / (scrollHeight - clientHeight)) * 100)));
    setScrollProgress(isNaN(progress) ? 0 : progress);

    // Find current active heading
    const headings = el.querySelectorAll<HTMLElement>('[data-section-id]');
    let currentId = '';
    headings.forEach((h) => {
      const rect = h.getBoundingClientRect();
      const parentRect = el.getBoundingClientRect();
      if (rect.top - parentRect.top <= 120) {
        currentId = h.getAttribute('data-section-id') || '';
      }
    });
    if (currentId) {
      setActiveSectionId(currentId);
    }
  };

  // Smooth scroll to section
  const scrollToSection = (id: string) => {
    const el = contentAreaRef.current;
    if (!el) return;
    const target = el.querySelector(`[data-section-id="${id}"]`);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setActiveSectionId(id);
    }
  };

  // Copy full markdown
  const handleCopyMarkdown = () => {
    if (!summary.content) return;
    navigator.clipboard.writeText(summary.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Print
  const handlePrint = () => {
    window.print();
  };

  // ==========================================
  // PARSER: Converts raw medical summary into structured AST
  // ==========================================
  const { dossier, tocItems, sections, spotWallItems } = useMemo(() => {
    const raw = summary.content || '';
    // 1. Normalize line endings and cleanup runaway tabs
    const text = raw.replace(/\r\n/g, '\n').replace(/\r/g, '\n');

    // Extract Dossier metadata from the start
    const dossier: ParsedDossier = {};
    const firstSectionIdx = text.search(/^##\s+/m);
    const headerBlock = firstSectionIdx > 0 ? text.slice(0, firstSectionIdx) : '';

    const lines = headerBlock.split('\n');
    lines.forEach((l) => {
      const t = l.trim();
      if (t.startsWith('📘')) {
        dossier.rawTitle = t.replace(/^📘\s*/, '').replace(/:\s*Detaylı Çalışma Metni.*$/, '').trim();
      } else if (t.includes('**Ders Kodu & Başlığı:**')) {
        dossier.courseCode = t.replace(/.*\*\*Ders Kodu & Başlığı:\*\*\s*/, '').trim();
      } else if (t.includes('**Öğretim Üyesi:**')) {
        dossier.instructor = t.replace(/.*\*\*Öğretim Üyesi:\*\*\s*/, '').trim();
      } else if (t.includes('**Müfredat Dönemi:**')) {
        dossier.term = t.replace(/.*\*\*Müfredat Dönemi:\*\*\s*/, '').trim();
      } else if (t.includes('**Tıbbi Kaynak ve Kılavuzlar:**')) {
        dossier.sources = t.replace(/.*\*\*Tıbbi Kaynak ve Kılavuzlar:\*\*\s*/, '').trim();
      } else if (t.includes('**Öğrenci / Çalışma Grubu:**')) {
        dossier.group = t.replace(/.*\*\*Öğrenci \/ Çalışma Grubu:\*\*\s*/, '').trim();
      }
    });

    const bodyText = firstSectionIdx > 0 ? text.slice(firstSectionIdx) : text;

    // Split into ## sections
    const rawSections = bodyText.split(/(?=^##\s+)/m);
    const tocItems: TocItem[] = [];
    const spotWallItems: string[] = [];

    const parsedSections = rawSections.map((secStr, secIndex) => {
      const secLines = secStr.split('\n');
      const firstLine = secLines[0] || '';
      const headingMatch = firstLine.match(/^##\s+(.*)/);
      const rawHeading = headingMatch ? headingMatch[1].trim() : `Bölüm ${secIndex + 1}`;

      // Smart Heading cleanup: If slide title is a 200-char case report, extract concise title & subtitle
      let secNumber = '';
      let secTitle = rawHeading;
      let secContext = '';

      const numMatch = rawHeading.match(/^(\d+)[\.\-\)]\s*(.*)/);
      if (numMatch) {
        secNumber = numMatch[1];
        secTitle = numMatch[2].trim();
      }

      // Check if spot wall
      const isSpotWall = secTitle.includes('SPOT BİLGİLER') || secTitle.includes('HIZLI TEKRAR');

      if (secTitle.length > 70) {
        // Find first punctuation breakpoint
        const breakMatch = secTitle.match(/^([^,:;\.!?\n]{25,65})([,:;\.!?\n]\s*)(.*)/);
        if (breakMatch) {
          secContext = (breakMatch[2] + breakMatch[3]).trim();
          secTitle = breakMatch[1].trim();
        } else {
          secContext = secTitle.slice(55);
          secTitle = secTitle.slice(0, 55) + '...';
        }
      }

      const secId = `section-${secIndex}-${secTitle.slice(0, 20).toLowerCase().replace(/[^a-z0-9]/g, '-')}`;

      // Add to TOC
      tocItems.push({
        id: secId,
        title: isSpotWall ? '⚡ Spot Bilgiler Duvarı' : (secNumber ? `${secNumber}. ${secTitle}` : secTitle),
        level: 2,
        type: isSpotWall ? 'spot' : 'section',
      });

      // Parse inner content of this section
      const innerContent = secLines.slice(1).join('\n');
      const subBlocks: any[] = [];

      // Split inner content by subsections (###) or callouts or tables or questions
      const chunks = innerContent.split(/(?=^###\s+|^>\s*\[!|^\|.*\|.*\|)/m);

      chunks.forEach((chunk, cIdx) => {
        const trimmedChunk = chunk.trim();
        if (!trimmedChunk) return;

        // 1. Heading 3 (###) or Questions
        if (trimmedChunk.startsWith('### ')) {
          const subHeadingLine = trimmedChunk.split('\n')[0].replace(/^###\s+/, '').trim();
          const subRest = trimmedChunk.split('\n').slice(1).join('\n');

          // Check if this is a Question (### Soru ...)
          const qMatch = subHeadingLine.match(/Soru\s*(\d+)?:?\s*(?:\[(.*?)\])?/i);
          if (qMatch && (subRest.includes('**Soru / Öncül:**') || subRest.includes('- **A)**') || subRest.includes('<details>'))) {
            // Parse question
            const qId = `q-${secIndex}-${cIdx}`;
            let stem = '';
            const options: { letter: string; text: string }[] = [];
            let answer = '';
            let explanation = '';

            const subLines = subRest.split('\n');
            let inDetails = false;

            for (let i = 0; i < subLines.length; i++) {
              const l = subLines[i].trim();
              if (l.includes('<details>')) {
                inDetails = true;
                continue;
              }
              if (l.includes('</details>')) {
                inDetails = false;
                continue;
              }

              if (inDetails) {
                if (l.includes('Doğru Cevap:')) {
                  const ansMatch = l.match(/Doğru Cevap:\*\*\s*([A-Ea-e])/);
                  if (ansMatch) answer = ansMatch[1].toUpperCase();
                } else if (l.includes('Klinik & Patofizyolojik Çözüm Notu:')) {
                  explanation = l.replace(/.*Klinik & Patofizyolojik Çözüm Notu:\*\*\s*/, '');
                } else if (explanation && l) {
                  explanation += '\n' + l;
                }
                continue;
              }

              if (l.startsWith('**Soru / Öncül:**')) {
                stem = l.replace(/^\*\*Soru \/ Öncül:\*\*\s*/, '').trim();
              } else if (l.match(/^[\-\*]\s*\*\*([A-Ea-e])\)\*\*/)) {
                const optMatch = l.match(/^[\-\*]\s*\*\*([A-Ea-e])\)\*\*\s*(.*)/);
                if (optMatch) {
                  options.push({ letter: optMatch[1].toUpperCase(), text: optMatch[2].trim() });
                }
              } else if (stem && !l.startsWith('-') && !l.startsWith('<')) {
                // Multi-line stem
                stem += ' ' + l;
              }
            }

            subBlocks.push({
              type: 'question',
              data: {
                id: qId,
                number: qMatch[1] || `${cIdx + 1}`,
                examTag: qMatch[2] || 'Kurul Sınavı Çıkmış Soru',
                stem,
                options,
                answer,
                explanation: explanation.trim()
              } as QuestionBlock
            });

            tocItems.push({
              id: qId,
              title: `Soru: ${qMatch[1] || `${cIdx + 1}`} (${qMatch[2] || 'Çıkmış'})`,
              level: 3,
              type: 'question'
            });

            return;
          }

          // Regular H3 Subsection
          const subId = `sub-${secIndex}-${cIdx}`;
          let subType: 'concept' | 'clinic' | 'standard' = 'standard';
          if (subHeadingLine.includes('Temel Kavramlar') || subHeadingLine.includes('Patofizyolojik')) {
            subType = 'concept';
          } else if (subHeadingLine.includes('Klinik Özellikler') || subHeadingLine.includes('Tanı ve Yaklaşım')) {
            subType = 'clinic';
          }

          tocItems.push({
            id: subId,
            title: subHeadingLine,
            level: 3,
            type: 'sub'
          });

          subBlocks.push({
            type: 'heading3',
            id: subId,
            title: subHeadingLine,
            subType,
            content: subRest
          });
          return;
        }

        // 2. Callout Block (> [!WARNING], > [!IMPORTANT], > [!TIP], > [!NOTE])
        if (trimmedChunk.startsWith('>')) {
          const calloutLines = trimmedChunk.split('\n');
          const first = calloutLines[0];
          let type: 'warning' | 'important' | 'tip' | 'note' = 'note';

          if (first.includes('[!WARNING]')) type = 'warning';
          else if (first.includes('[!IMPORTANT]')) type = 'important';
          else if (first.includes('[!TIP]')) type = 'tip';
          else if (first.includes('[!NOTE]')) type = 'note';

          const content = calloutLines
            .map((l) => l.replace(/^>\s*\[!.*\]/, '').replace(/^>\s*/, '').trim())
            .filter(Boolean)
            .join(' ');

          subBlocks.push({
            type: 'callout',
            data: {
              type,
              content
            } as CalloutBlock
          });
          return;
        }

        // 3. Markdown Table (| ... |)
        if (trimmedChunk.startsWith('|')) {
          const tableLines = trimmedChunk.split('\n').filter((l) => l.trim().startsWith('|'));
          if (tableLines.length >= 2) {
            const parseRow = (line: string) =>
              line
                .split('|')
                .slice(1, -1)
                .map((cell) => cell.trim());

            const headers = parseRow(tableLines[0]);
            // Check if second line is separator
            const isSep = tableLines[1].replace(/[:\-\|\s]/g, '').length === 0;
            const rowLines = isSep ? tableLines.slice(2) : tableLines.slice(1);
            const rows = rowLines.map(parseRow);

            if (headers.length > 0 && rows.length > 0) {
              const tableId = `table-${secIndex}-${cIdx}`;
              tocItems.push({
                id: tableId,
                title: `Tablo: ${headers.slice(0, 2).join(' / ')}`,
                level: 3,
                type: 'table'
              });

              subBlocks.push({
                type: 'table',
                id: tableId,
                data: {
                  headers,
                  rows
                } as TableBlock
              });
              return;
            }
          }
        }

        // 4. Default: Paragraphs or Bullet Lists
        // Split by standard paragraphs
        const paragraphs = trimmedChunk.split(/\n\n+/);
        paragraphs.forEach((para) => {
          const pTrim = para.trim();
          if (!pTrim) return;

          // Check if bullet list
          if (pTrim.startsWith('- ') || pTrim.startsWith('* ')) {
            const pLines = pTrim.split('\n');
            const items: BulletItem[] = [];
            let currentItem: BulletItem | null = null;

            pLines.forEach((pl) => {
              const isSub = pl.startsWith('  ') || pl.startsWith('\t');
              const cleanLine = pl.replace(/^[\s\t]*[-\*]\s*/, '').trim();

              if (!isSub && (pl.trim().startsWith('-') || pl.trim().startsWith('*'))) {
                // Top-level bullet
                let key = '';
                let content = cleanLine;

                const boldMatch = cleanLine.match(/^\*\*(.*?)\*\*[:\.]?\s*(.*)/);
                if (boldMatch) {
                  key = boldMatch[1].trim();
                  content = boldMatch[2].trim();
                }

                // Check for concatenated numbered list items: e.g. "1. Standart 2. Bulaş Yolu"
                const numberedMatches = content.match(/\b\d+\.\s+[^1-9\n]+/g);
                let numberedPills: string[] | undefined = undefined;
                if (numberedMatches && numberedMatches.length >= 2) {
                  numberedPills = numberedMatches.map((m) => m.trim());
                }

                currentItem = { key, content, subItems: [], numberedPills };
                items.push(currentItem);

                if (isSpotWall && key) {
                  spotWallItems.push(`${key}: ${content}`);
                }
              } else if (currentItem) {
                // Sub-bullet
                currentItem.subItems = currentItem.subItems || [];
                currentItem.subItems.push(cleanLine);
              }
            });

            if (items.length > 0) {
              subBlocks.push({
                type: 'bulletList',
                items
              });
              return;
            }
          }

          // Fallback plain paragraph
          subBlocks.push({
            type: 'paragraph',
            text: pTrim
          });
        });
      });

      return {
        id: secId,
        number: secNumber,
        title: secTitle,
        context: secContext,
        isSpotWall,
        blocks: subBlocks
      };
    });

    return {
      dossier,
      tocItems,
      sections: parsedSections,
      spotWallItems
    };
  }, [summary.content]);

  // Copy spot notes
  const handleCopySpotWall = () => {
    if (spotWallItems.length === 0) return;
    navigator.clipboard.writeText(spotWallItems.map((s, i) => `⚡ Spot ${i + 1}: ${s}`).join('\n\n'));
    setCopiedSpot(true);
    setTimeout(() => setCopiedSpot(false), 2000);
  };

  // Option selection for questions
  const handleSelectOption = (qId: string, letter: string) => {
    setSelectedAnswers((prev) => ({ ...prev, [qId]: letter }));
  };

  const toggleRevealSolution = (qId: string) => {
    setRevealedAnswers((prev) => ({ ...prev, [qId]: !prev[qId] }));
  };

  // ==========================================
  // INLINE TEXT HIGHLIGHTER & SEARCH RENDERER
  // ==========================================
  const renderHighlightedText = (text: string) => {
    if (!text) return null;

    // 1. If search query is active, highlight search query matches
    if (searchQuery.trim().length >= 2) {
      const q = searchQuery.trim();
      const regex = new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
      const parts = text.split(regex);

      return (
        <span>
          {parts.map((part, i) =>
            regex.test(part) ? (
              <mark key={i} className="reader-search-match">
                {part}
              </mark>
            ) : (
              <span key={i} dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(part, markerMode) }} />
            )
          )}
        </span>
      );
    }

    // Standard markdown inline formatting + medical marker detection
    return <span dangerouslySetInnerHTML={{ __html: formatInlineMarkdown(text, markerMode) }} />;
  };

  const formatInlineMarkdown = (str: string, useMarkers: boolean): string => {
    let out = str
      .replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-inherit">$1</strong>')
      .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')
      .replace(/`([^`]+)`/g, '<code class="font-mono text-xs px-1 py-0.5 rounded bg-black/5">$1</code>');

    if (useMarkers) {
      // Automatic Highlighting for high-yield medical concepts:
      // Yellow marker: Spot, TUS, Komite, En sık, Altın standart, İlk tercih
      out = out.replace(/\b(en sık|altın standart|ilk tercih|en önemli|en duyarlı|en özgül|patognomonik)\b/gi, '<mark class="reader-mark-yellow">$1</mark>');
      // Rose marker: Kontrendike, Toksisite, Yan etki, Ölümcül, Risk, Tuzak
      out = out.replace(/\b(kontrendike|toksisite|yan etki|ölümcül|teratojenik|nefrotoksisite|hepatotoksisite)\b/gi, '<mark class="reader-mark-rose">$1</mark>');
      // Green marker: İlaç isimleri & Tedavi
      out = out.replace(/\b(siklosporin|takrolimus|sirolimus|everolimus|azatioprin|mikofenolat mofetil|kortikosteroidler|prednizon|talidomid|lenalidomid|metotreksat)\b/gi, '<mark class="reader-mark-green">$1</mark>');
      // Cyan marker: İmmun & Patoloji kavramları
      out = out.replace(/\b(MHC sınıf I|MHC sınıf II|NF-AT|kalsinörin|interlökin|IFN-γ|TNF-α|IgE|IgG|IgM|fagositoz)\b/g, '<mark class="reader-mark-cyan">$1</mark>');
    }

    return out;
  };

  // Theme-specific container classes
  const themeClasses: Record<ReaderTheme, { container: string; text: string; card: string; border: string }> = {
    light: {
      container: 'reader-theme-light bg-slate-100 text-slate-900',
      text: 'text-slate-800',
      card: 'bg-white border-slate-200/80 shadow-xs',
      border: 'border-slate-200',
    },
    sepia: {
      container: 'reader-theme-sepia bg-[#F4ECD8] text-[#2D2319]',
      text: 'text-[#3E3224]',
      card: 'bg-[#FCF8EE] border-[#DFD5C2] shadow-xs',
      border: 'border-[#DFD5C2]',
    },
    dark: {
      container: 'reader-theme-dark bg-[#0B0F17] text-slate-100',
      text: 'text-slate-200',
      card: 'bg-[#151D2A] border-[#1E293B] shadow-lg',
      border: 'border-[#1E293B]',
    },
    cobalt: {
      container: 'reader-theme-cobalt bg-[#0A192F] text-sky-100',
      text: 'text-slate-100',
      card: 'bg-[#112240] border-[#1E3A5F] shadow-lg',
      border: 'border-[#1E3A5F]',
    },
  };

  const curTheme = themeClasses[theme];

  // Font family class
  const fontFamClass = fontFamily === 'serif' ? 'font-reading-serif' : 'font-reading-sans';

  // Line height class
  const lineHeightClass =
    lineHeight === 'tight' ? 'leading-normal' : lineHeight === 'relaxed' ? 'leading-loose' : 'leading-relaxed';

  // Container width class
  const widthClass =
    widthMode === 'fullscreen'
      ? 'w-full h-full max-w-none rounded-none m-0'
      : widthMode === 'wide'
      ? 'max-w-6xl w-full mx-auto my-3 sm:my-5 rounded-2xl max-h-[94vh]'
      : 'max-w-5xl w-full mx-auto my-3 sm:my-5 rounded-2xl max-h-[94vh]';

  return (
    <div
      ref={containerRef}
      className={`fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex flex-col justify-center items-center p-0 sm:p-4 overflow-hidden select-text ${curTheme.container}`}
      onClick={(e) => e.stopPropagation()}
    >
      {/* ========================================================
          MODAL READER WINDOW (Artifact Container)
          ======================================================== */}
      <div
        className={`flex flex-col bg-[var(--reader-bg,#ffffff)] border border-[var(--reader-border,#e2e8f0)] shadow-2xl overflow-hidden transition-all duration-200 ${widthClass}`}
      >
        {/* ========================================================
            TOP DOCK TOOLBAR (Artifact Design Header)
            ======================================================== */}
        <header className="bg-slate-900 border-b border-slate-800 text-white shrink-0 px-3 sm:px-5 py-2.5 flex items-center justify-between gap-2 z-20">
          {/* Left: Info & Back */}
          <div className="flex items-center gap-2 sm:gap-3 min-w-0">
            <button
              type="button"
              onClick={onClose}
              className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-slate-300 hover:text-white cursor-pointer transition-colors"
              title="Kapat (ESC)"
            >
              <X className="w-4 h-4" />
            </button>

            <div className="min-w-0">
              <div className="flex items-center gap-1.5 text-[11px] text-teal-300 font-semibold truncate">
                <span className="bg-teal-500/20 px-2 py-0.5 rounded border border-teal-500/30">
                  Kurul {summary.kurul}
                </span>
                <span>•</span>
                <span className="text-slate-300 truncate">{summary.discipline}</span>
                <span className="hidden md:inline text-slate-400">• ~{summary.readingTimeMinutes} dk okuma</span>
              </div>
              <h2 className="text-sm sm:text-base font-bold text-white truncate max-w-md sm:max-w-lg mt-0.5">
                {summary.title}
              </h2>
            </div>
          </div>

          {/* Center / Right: Reader Controls (Büyütme/Küçültme, Renkler, Arama, TOC, Yazdır) */}
          <div className="flex items-center gap-1 sm:gap-2 shrink-0">
            {/* Search Input */}
            <div className="relative hidden md:flex items-center">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Özet içinde ara..."
                className="w-36 lg:w-48 pl-8 pr-6 py-1 text-xs bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-hidden focus:border-teal-500 transition-all"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery('')}
                  className="absolute right-2 text-slate-400 hover:text-white"
                >
                  <X className="w-3 h-3" />
                </button>
              )}
            </div>

            {/* Font Scale (Büyütme / Küçültme) */}
            <div className="flex items-center bg-slate-800 rounded-lg p-0.5 border border-slate-700">
              <button
                type="button"
                onClick={() => setFontScale((s) => Math.max(75, s - 10))}
                title="Yazıyı Küçült"
                className="p-1 rounded text-slate-300 hover:text-white hover:bg-slate-700 transition-colors"
              >
                <ZoomOut className="w-3.5 h-3.5" />
              </button>
              <span className="text-[11px] font-mono font-bold px-1.5 text-teal-300 select-none">
                %{fontScale}
              </span>
              <button
                type="button"
                onClick={() => setFontScale((s) => Math.min(160, s + 10))}
                title="Yazıyı Büyüt"
                className="p-1 rounded text-slate-300 hover:text-white hover:bg-slate-700 transition-colors"
              >
                <ZoomIn className="w-3.5 h-3.5" />
              </button>
              {fontScale !== 100 && (
                <button
                  type="button"
                  onClick={() => setFontScale(100)}
                  title="Yazı Boyutunu Sıfırla (%100)"
                  className="p-1 text-slate-400 hover:text-white transition-colors"
                >
                  <RotateCcw className="w-3 h-3" />
                </button>
              )}
            </div>

            {/* Font Family Switch (Sans vs Serif) */}
            <button
              type="button"
              onClick={() => setFontFamily((f) => (f === 'sans' ? 'serif' : 'sans'))}
              title={`Yazı Tipi: ${fontFamily === 'sans' ? 'Serif (Kitap Okuma)' : 'Sans-Serif (Modern)'}`}
              className={`p-1.5 rounded-lg border text-xs font-bold transition-colors ${
                fontFamily === 'serif'
                  ? 'bg-amber-500/20 border-amber-400 text-amber-200'
                  : 'bg-slate-800 border-slate-700 text-slate-300 hover:text-white'
              }`}
            >
              <span className="font-serif px-0.5">Aa</span>
            </button>

            {/* Medical Marker Highlighter Toggle */}
            <button
              type="button"
              onClick={() => setMarkerMode((m) => !m)}
              title={markerMode ? 'Fosforlu Kalem Vurgularını Kapat' : 'Fosforlu Kalem Vurgularını Aç'}
              className={`p-1.5 rounded-lg border text-xs flex items-center gap-1 transition-colors ${
                markerMode
                  ? 'bg-amber-400 text-slate-950 font-bold border-amber-300 shadow-xs'
                  : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white'
              }`}
            >
              <Highlighter className="w-3.5 h-3.5" />
              <span className="hidden xl:inline text-[11px]">Marker</span>
            </button>

            {/* Theme Selector (Açık, Sepya, Gece, Kobalt) */}
            <div className="flex items-center bg-slate-800 rounded-lg p-0.5 border border-slate-700">
              <button
                type="button"
                onClick={() => setTheme('light')}
                title="Açık Tema (Temiz Beyaz)"
                className={`p-1.5 rounded transition-colors ${
                  theme === 'light' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-400 hover:text-white'
                }`}
              >
                <Sun className="w-3.5 h-3.5" />
              </button>
              <button
                type="button"
                onClick={() => setTheme('sepia')}
                title="Sepya Tema (Göz Dinlendirici Kitap Kağıdı)"
                className={`p-1.5 rounded transition-colors ${
                  theme === 'sepia' ? 'bg-[#FCF8EE] text-[#5C4B3A] shadow-xs' : 'text-slate-400 hover:text-white'
                }`}
              >
                <Coffee className="w-3.5 h-3.5" />
              </button>
              <button
                type="button"
                onClick={() => setTheme('dark')}
                title="Gece Teması (Koyu)"
                className={`p-1.5 rounded transition-colors ${
                  theme === 'dark' ? 'bg-slate-950 text-teal-400 shadow-xs' : 'text-slate-400 hover:text-white'
                }`}
              >
                <Moon className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Table of Contents Toggle */}
            <button
              type="button"
              onClick={() => setShowToc((v) => !v)}
              title={showToc ? 'İçindekiler Menüsünü Gizle' : 'İçindekiler Menüsünü Göster'}
              className={`p-1.5 rounded-lg border text-xs flex items-center gap-1 transition-colors ${
                showToc
                  ? 'bg-teal-700 border-teal-600 text-white'
                  : 'bg-slate-800 border-slate-700 text-slate-300 hover:text-white'
              }`}
            >
              <List className="w-3.5 h-3.5" />
              <span className="hidden lg:inline text-[11px]">İçindekiler</span>
            </button>

            {/* Print / PDF */}
            <button
              type="button"
              onClick={handlePrint}
              title="Yazdır / PDF Olarak Kaydet"
              className="p-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors"
            >
              <Printer className="w-3.5 h-3.5" />
            </button>

            {/* Layout Width Toggle */}
            <button
              type="button"
              onClick={() =>
                setWidthMode((w) => (w === 'standard' ? 'wide' : w === 'wide' ? 'fullscreen' : 'standard'))
              }
              title={`Genişlik: ${widthMode === 'standard' ? 'Genişlet' : widthMode === 'wide' ? 'Tam Ekran' : 'Normal'}`}
              className="hidden sm:flex p-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-300 hover:text-white transition-colors"
            >
              {widthMode === 'fullscreen' ? (
                <Minimize2 className="w-3.5 h-3.5" />
              ) : (
                <Maximize2 className="w-3.5 h-3.5" />
              )}
            </button>
          </div>
        </header>

        {/* ========================================================
            TOP READING PROGRESS BAR
            ======================================================== */}
        <div className="w-full h-1 bg-slate-800/20 shrink-0 relative overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-teal-500 via-emerald-400 to-teal-600 transition-all duration-150"
            style={{ width: `${scrollProgress}%` }}
          />
        </div>

        {/* ========================================================
            MAIN BODY (TOC SIDEBAR + DOCUMENT PROSE AREA)
            ======================================================== */}
        <div className="flex-1 flex overflow-hidden relative">
          {/* ----------------------------------------------------
              COLLAPSIBLE TABLE OF CONTENTS (İÇİNDEKİLER) SIDEBAR
              ---------------------------------------------------- */}
          {showToc && (
            <aside className="w-64 sm:w-72 shrink-0 border-r border-[var(--reader-border,#e2e8f0)] bg-[var(--reader-surface,#f8fafc)] flex flex-col overflow-hidden select-none animate-fadeIn">
              <div className="p-3 border-b border-[var(--reader-border,#e2e8f0)] flex items-center justify-between">
                <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700 dark:text-slate-200">
                  <Compass className="w-3.5 h-3.5 text-teal-600" />
                  <span>Ders İçindekiler ({tocItems.length})</span>
                </div>
                <span className="text-[10px] font-mono font-bold text-teal-700 dark:text-teal-400 bg-teal-50 dark:bg-teal-950/60 px-1.5 py-0.5 rounded border border-teal-200 dark:border-teal-800">
                  %{scrollProgress}
                </span>
              </div>

              {/* Quick Jump Shortcuts */}
              <div className="p-2 border-b border-[var(--reader-border,#e2e8f0)] grid grid-cols-2 gap-1 text-[11px] font-semibold">
                {spotWallItems.length > 0 && (
                  <button
                    type="button"
                    onClick={() => {
                      const spotEl = contentAreaRef.current?.querySelector('[data-type="spot-wall"]');
                      spotEl?.scrollIntoView({ behavior: 'smooth' });
                    }}
                    className="p-1.5 rounded bg-amber-50 dark:bg-amber-950/40 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800/50 flex items-center gap-1 hover:bg-amber-100 transition-colors"
                  >
                    <Flame className="w-3 h-3 text-amber-500" />
                    <span>Spot Duvarı</span>
                  </button>
                )}

                <button
                  type="button"
                  onClick={handleCopyMarkdown}
                  className="p-1.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 flex items-center gap-1 hover:bg-slate-200 transition-colors"
                >
                  {copied ? <Check className="w-3 h-3 text-emerald-500" /> : <Copy className="w-3 h-3" />}
                  <span>{copied ? 'Kopyalandı' : 'Markdown'}</span>
                </button>
              </div>

              {/* Headings List */}
              <div className="flex-1 overflow-y-auto p-2 space-y-1 text-xs">
                {tocItems.map((item, idx) => {
                  const isActive = activeSectionId === item.id;
                  const isSpot = item.type === 'spot';
                  const isQ = item.type === 'question';
                  const isTable = item.type === 'table';

                  return (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => scrollToSection(item.id)}
                      className={`w-full text-left px-2 py-1.5 rounded-lg transition-all flex items-start gap-1.5 cursor-pointer ${
                        item.level === 3 ? 'pl-4 text-[11px]' : 'font-semibold'
                      } ${
                        isActive
                          ? 'bg-teal-600 text-white font-bold shadow-xs'
                          : isSpot
                          ? 'text-amber-700 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-950/40'
                          : isQ
                          ? 'text-indigo-700 dark:text-indigo-300 hover:bg-indigo-50 dark:hover:bg-indigo-950/40'
                          : 'text-slate-600 dark:text-slate-400 hover:bg-slate-200/60 dark:hover:bg-slate-800'
                      }`}
                    >
                      <span className="shrink-0 mt-0.5">
                        {isSpot ? (
                          '⚡'
                        ) : isQ ? (
                          '🎯'
                        ) : isTable ? (
                          '📊'
                        ) : item.level === 2 ? (
                          <ChevronRight className="w-3 h-3" />
                        ) : (
                          '•'
                        )}
                      </span>
                      <span className="line-clamp-2 leading-tight">{item.title}</span>
                    </button>
                  );
                })}
              </div>
            </aside>
          )}

          {/* ----------------------------------------------------
              DOCUMENT CONTENT AREA (High-Yield Medical Reading Canvas)
              ---------------------------------------------------- */}
          <main
            ref={contentAreaRef}
            onScroll={handleScroll}
            className={`flex-1 overflow-y-auto p-4 sm:p-8 lg:p-12 space-y-8 scroll-smooth ${fontFamClass} ${lineHeightClass}`}
            style={{ fontSize: `${fontScale}%` }}
          >
            {!summary.content ? (
              <div className="py-24 text-center space-y-4">
                <div className="w-10 h-10 border-3 border-teal-600 border-t-transparent rounded-full animate-spin mx-auto" />
                <p className="text-sm font-semibold text-slate-700 dark:text-slate-300">Ders notları ve spot bilgiler yükleniyor...</p>
                <p className="text-xs text-slate-400">Tıp Fakültesi müfredat kataloğu hazırlanıyor</p>
              </div>
            ) : (
              <>
            {/* 1. EXECUTIVE DOSSIER CARD (DERS BİLGİ KARTI) */}
            <div
              className={`p-6 sm:p-7 rounded-2xl border ${curTheme.card} ${curTheme.border} relative overflow-hidden`}
            >
              <div className="absolute top-0 right-0 w-64 h-64 bg-teal-500/5 rounded-full blur-3xl pointer-events-none" />

              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-[var(--reader-border,#e2e8f0)]">
                <div className="space-y-1">
                  <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-teal-50 dark:bg-teal-950/50 text-teal-800 dark:text-teal-300 border border-teal-200 dark:border-teal-800">
                    <GraduationCap className="w-3.5 h-3.5" />
                    <span>Dönem 3 Amfi Ders Çalışma Notu</span>
                  </div>
                  <h1 className="text-xl sm:text-2xl font-black font-display tracking-tight text-slate-900 dark:text-white">
                    {dossier.rawTitle || summary.title}
                  </h1>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-teal-600" />
                    <span>~{summary.readingTimeMinutes} Dakika</span>
                  </span>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 flex items-center gap-1">
                    <FileText className="w-3.5 h-3.5 text-teal-600" />
                    <span>{summary.charCount.toLocaleString()} Karakter</span>
                  </span>
                </div>
              </div>

              {/* Dossier Meta Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-4 text-xs">
                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/70 dark:border-slate-800 space-y-1">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                    <Building className="w-3 h-3 text-teal-600" /> Ders & Kurul
                  </span>
                  <p className="font-bold text-slate-800 dark:text-slate-200 line-clamp-1">
                    {dossier.courseCode || `TIP 3${summary.kurul}0 · Kurul ${summary.kurul}`}
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/70 dark:border-slate-800 space-y-1">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                    <User className="w-3 h-3 text-teal-600" /> Öğretim Üyesi
                  </span>
                  <p className="font-bold text-slate-800 dark:text-slate-200 line-clamp-1">
                    {dossier.instructor || `${summary.discipline} ABD`}
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/70 dark:border-slate-800 space-y-1">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                    <Calendar className="w-3 h-3 text-teal-600" /> Müfredat Yılı
                  </span>
                  <p className="font-bold text-slate-800 dark:text-slate-200 line-clamp-1">
                    {dossier.term || '2025 - 2026 Akademik Yılı'}
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200/70 dark:border-slate-800 space-y-1">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                    <BookMarked className="w-3 h-3 text-teal-600" /> Temel Kılavuzlar
                  </span>
                  <p className="font-bold text-slate-800 dark:text-slate-200 line-clamp-1">
                    {dossier.sources || 'Tıp Fakültesi Ders Kurulu Rehberleri'}
                  </p>
                </div>
              </div>
            </div>

            {/* 2. DYNAMICALLY PARSED CHAPTERS & SECTIONS */}
            {sections.map((section, sIdx) => {
              return (
                <section
                  key={sIdx}
                  data-section-id={section.id}
                  className={`space-y-6 pt-4 border-t border-[var(--reader-border,#e2e8f0)] first:border-t-0`}
                >
                  {/* CHAPTER HEADING (H2) */}
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      {section.isSpotWall ? (
                        <span className="px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-black text-xs flex items-center gap-1 shadow-xs">
                          <Flame className="w-3.5 h-3.5 fill-current" />
                          <span>HIZLI TEKRAR DUVARI</span>
                        </span>
                      ) : section.number ? (
                        <span className="px-2.5 py-0.5 rounded-md bg-teal-100 dark:bg-teal-950/70 text-teal-800 dark:text-teal-300 font-bold text-xs border border-teal-200 dark:border-teal-800">
                          Bölüm {section.number}
                        </span>
                      ) : null}
                    </div>

                    <h2 className="text-lg sm:text-xl font-black font-display text-teal-950 dark:text-teal-100 tracking-tight leading-snug">
                      {section.title}
                    </h2>

                    {/* Subtitle / Case Vignette (if the slide title was very long) */}
                    {section.context && (
                      <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 italic bg-slate-50 dark:bg-slate-900/50 p-3 rounded-lg border border-slate-200/60 dark:border-slate-800">
                        {section.context}
                      </p>
                    )}
                  </div>

                  {/* SPOT DUVALI DEDICATED CARDS (If this is the spot wall section) */}
                  {section.isSpotWall && spotWallItems.length > 0 && (
                    <div
                      data-type="spot-wall"
                      className="p-5 rounded-2xl bg-gradient-to-br from-amber-500/10 via-amber-400/5 to-transparent border border-amber-300/60 dark:border-amber-700/50 space-y-4"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Sparkles className="w-4 h-4 text-amber-500" />
                          <h3 className="font-bold text-sm text-amber-950 dark:text-amber-200">
                            Sınav Öncesi Kritik Spot Bilgi Özeti ({spotWallItems.length})
                          </h3>
                        </div>
                        <button
                          type="button"
                          onClick={handleCopySpotWall}
                          className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-amber-500 hover:bg-amber-600 text-slate-950 flex items-center gap-1 transition-colors cursor-pointer"
                        >
                          {copiedSpot ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                          <span>{copiedSpot ? 'Kopyalandı' : 'Tümünü Kopyala'}</span>
                        </button>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                        {spotWallItems.map((sp, spIdx) => (
                          <div
                            key={spIdx}
                            className="p-3 rounded-xl bg-white dark:bg-slate-900 border border-amber-200 dark:border-amber-800/60 shadow-2xs space-y-1"
                          >
                            <span className="font-bold text-[10px] text-amber-700 dark:text-amber-400 uppercase tracking-wider flex items-center gap-1">
                              ⚡ Spot #{spIdx + 1}
                            </span>
                            <p className="text-slate-800 dark:text-slate-200 leading-relaxed font-medium">
                              {renderHighlightedText(sp)}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* SECTION INNER BLOCKS */}
                  <div className="space-y-5">
                    {section.blocks.map((block: any, bIdx: number) => {
                      // 1. Heading 3 (### Subsections)
                      if (block.type === 'heading3') {
                        const isConcept = block.subType === 'concept';
                        const isClinic = block.subType === 'clinic';

                        return (
                          <div key={bIdx} data-section-id={block.id} className="pt-3 space-y-3">
                            <div className="flex items-center gap-2">
                              {isConcept && <Dna className="w-4 h-4 text-indigo-500 shrink-0" />}
                              {isClinic && <Stethoscope className="w-4 h-4 text-emerald-500 shrink-0" />}
                              <h3 className="font-bold text-sm sm:text-base text-slate-900 dark:text-slate-100 font-display">
                                {block.title}
                              </h3>
                            </div>

                            {block.content && (
                              <p className="text-xs sm:text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                                {renderHighlightedText(block.content)}
                              </p>
                            )}
                          </div>
                        );
                      }

                      // 2. Callout Cards ([!WARNING], [!IMPORTANT], [!TIP])
                      if (block.type === 'callout') {
                        const c = block.data as CalloutBlock;
                        const isWarn = c.type === 'warning';
                        const isImp = c.type === 'important';
                        const isTip = c.type === 'tip';

                        const calloutColors = isWarn
                          ? 'bg-rose-50 dark:bg-rose-950/30 border-rose-500 text-rose-950 dark:text-rose-200'
                          : isImp
                          ? 'bg-indigo-50 dark:bg-indigo-950/30 border-indigo-500 text-indigo-950 dark:text-indigo-200'
                          : isTip
                          ? 'bg-emerald-50 dark:bg-emerald-950/30 border-emerald-500 text-emerald-950 dark:text-emerald-200'
                          : 'bg-sky-50 dark:bg-sky-950/30 border-sky-500 text-sky-950 dark:text-sky-200';

                        const calloutBadge = isWarn
                          ? { icon: AlertTriangle, text: 'SINAV TUZAĞI & DİKKAT NOKTASI', color: 'text-rose-700 dark:text-rose-400' }
                          : isImp
                          ? { icon: Sparkles, text: 'DERS NOTU HOCA VURGUSU | AMFİ SORU İKAZI', color: 'text-indigo-700 dark:text-indigo-400' }
                          : isTip
                          ? { icon: Pill, text: 'KLİNİK İNCİ & SPOT İPUCU', color: 'text-emerald-700 dark:text-emerald-400' }
                          : { icon: Bookmark, text: 'ÖNEMLİ TIBBİ NOT', color: 'text-sky-700 dark:text-sky-400' };

                        const IconCmp = calloutBadge.icon;

                        return (
                          <div
                            key={bIdx}
                            className={`p-4 sm:p-5 rounded-xl border-l-4 shadow-2xs space-y-1.5 my-3 ${calloutColors}`}
                          >
                            <div className={`font-bold flex items-center gap-1.5 text-xs ${calloutBadge.color}`}>
                              <IconCmp className="w-4 h-4 shrink-0" />
                              <span>{calloutBadge.text}</span>
                            </div>
                            <p className="text-xs sm:text-sm leading-relaxed">{renderHighlightedText(c.content)}</p>
                          </div>
                        );
                      }

                      // 3. Responsive Markdown Tables
                      if (block.type === 'table') {
                        const t = block.data as TableBlock;
                        return (
                          <div
                            key={bIdx}
                            data-section-id={block.id}
                            className="my-4 rounded-xl border border-[var(--reader-border,#e2e8f0)] overflow-hidden shadow-2xs bg-white dark:bg-slate-900"
                          >
                            <div className="p-2.5 bg-slate-50 dark:bg-slate-800 border-b border-[var(--reader-border,#e2e8f0)] flex items-center gap-2 text-xs font-bold text-slate-700 dark:text-slate-300">
                              <TableIcon className="w-4 h-4 text-teal-600" />
                              <span>Tıbbi Karşılaştırma & Sınıflandırma Tablosu</span>
                            </div>

                            <div className="overflow-x-auto">
                              <table className="w-full text-left text-xs sm:text-sm border-collapse">
                                <thead>
                                  <tr className="bg-teal-900 text-white font-semibold">
                                    {t.headers.map((h, hIdx) => (
                                      <th key={hIdx} className="px-4 py-2.5 border-b border-teal-800 font-bold">
                                        {h}
                                      </th>
                                    ))}
                                  </tr>
                                </thead>
                                <tbody>
                                  {t.rows.map((row, rIdx) => (
                                    <tr
                                      key={rIdx}
                                      className={`border-b border-slate-100 dark:border-slate-800 hover:bg-teal-50/50 dark:hover:bg-slate-800/60 transition-colors ${
                                        rIdx % 2 === 1 ? 'bg-slate-50/60 dark:bg-slate-900/40' : 'bg-transparent'
                                      }`}
                                    >
                                      {row.map((cell, cIdx) => (
                                        <td key={cIdx} className="px-4 py-3 leading-relaxed">
                                          {renderHighlightedText(cell)}
                                        </td>
                                      ))}
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>
                          </div>
                        );
                      }

                      // 4. Interactive Past Exam Questions (ÇIKMIŞ SORU SİMÜLASYONU)
                      if (block.type === 'question') {
                        const q = block.data as QuestionBlock;
                        const userChoice = selectedAnswers[q.id];
                        const isRevealed = Boolean(revealedAnswers[q.id]);
                        const isCorrect = userChoice && q.answer && userChoice.toUpperCase() === q.answer.toUpperCase();

                        return (
                          <div
                            key={bIdx}
                            data-section-id={q.id}
                            className="my-5 rounded-2xl border-2 border-indigo-200 dark:border-indigo-900/80 bg-white dark:bg-slate-900 p-5 sm:p-6 shadow-sm space-y-4"
                          >
                            <div className="flex items-center justify-between gap-2 border-b border-indigo-100 dark:border-indigo-900/50 pb-3">
                              <div className="flex items-center gap-2">
                                <span className="bg-indigo-600 text-white font-black text-xs px-2.5 py-0.5 rounded-full">
                                  Soru {q.number}
                                </span>
                                <span className="text-xs font-bold text-indigo-700 dark:text-indigo-300">
                                  {q.examTag}
                                </span>
                              </div>
                              <span className="text-[11px] font-semibold text-slate-400">
                                Sınav Simülasyonu
                              </span>
                            </div>

                            {/* Question Stem */}
                            <p className="font-semibold text-xs sm:text-sm text-slate-900 dark:text-slate-100 leading-relaxed">
                              {renderHighlightedText(q.stem)}
                            </p>

                            {/* Multiple Choice Options */}
                            <div className="space-y-2">
                              {q.options.map((opt) => {
                                const isSelected = userChoice === opt.letter;
                                const isAnswerOpt = isRevealed && q.answer && opt.letter === q.answer.toUpperCase();
                                const isWrongOpt = isRevealed && isSelected && !isAnswerOpt;

                                let optClasses = 'border-slate-200 dark:border-slate-800 hover:border-indigo-300 dark:hover:border-indigo-700 bg-slate-50 dark:bg-slate-800/50 text-slate-800 dark:text-slate-200';
                                if (isSelected) {
                                  optClasses = 'border-indigo-600 bg-indigo-50 dark:bg-indigo-950/60 font-semibold';
                                }
                                if (isAnswerOpt) {
                                  optClasses = 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/60 text-emerald-950 dark:text-emerald-200 font-bold';
                                } else if (isWrongOpt) {
                                  optClasses = 'border-rose-500 bg-rose-50 dark:bg-rose-950/60 text-rose-950 dark:text-rose-200 line-through';
                                }

                                return (
                                  <button
                                    key={opt.letter}
                                    type="button"
                                    onClick={() => handleSelectOption(q.id, opt.letter)}
                                    className={`w-full text-left p-3 rounded-xl border flex items-start gap-2.5 transition-all cursor-pointer text-xs sm:text-sm ${optClasses}`}
                                  >
                                    <span
                                      className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 font-bold text-xs ${
                                        isAnswerOpt
                                          ? 'bg-emerald-600 text-white'
                                          : isWrongOpt
                                          ? 'bg-rose-600 text-white'
                                          : isSelected
                                          ? 'bg-indigo-600 text-white'
                                          : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
                                      }`}
                                    >
                                      {opt.letter}
                                    </span>
                                    <span className="leading-snug pt-0.5">{renderHighlightedText(opt.text)}</span>
                                  </button>
                                );
                              })}
                            </div>

                            {/* Solution & Answer Key Reveal Toggle */}
                            <div className="pt-2 flex flex-col gap-3">
                              <button
                                type="button"
                                onClick={() => toggleRevealSolution(q.id)}
                                className="self-start text-xs font-bold px-3 py-1.5 rounded-lg bg-indigo-50 dark:bg-indigo-950 hover:bg-indigo-100 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 flex items-center gap-1.5 transition-colors cursor-pointer"
                              >
                                {isRevealed ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                                <span>{isRevealed ? 'Çözümü Gizle' : '👉 Çözümü ve Doğru Cevabı Göster'}</span>
                              </button>

                              {isRevealed && (
                                <div className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-800 space-y-2 animate-fadeIn text-xs sm:text-sm">
                                  <div className="flex items-center gap-2">
                                    <span className="bg-emerald-600 text-white font-black text-xs px-2.5 py-0.5 rounded">
                                      Doğru Cevap: {q.answer || 'Belirtilmemiş'}
                                    </span>
                                    {userChoice && (
                                      <span
                                        className={`font-bold text-xs flex items-center gap-1 ${
                                          isCorrect ? 'text-emerald-700 dark:text-emerald-300' : 'text-rose-600'
                                        }`}
                                      >
                                        {isCorrect ? (
                                          <>
                                            <CheckCircle2 className="w-3.5 h-3.5" /> Tebrikler, Doğru Çözdünüz!
                                          </>
                                        ) : (
                                          <>
                                            <XCircle className="w-3.5 h-3.5" /> Yanıtınız ({userChoice}) Hatalıydı
                                          </>
                                        )}
                                      </span>
                                    )}
                                  </div>

                                  {q.explanation && (
                                    <div className="pt-2 border-t border-emerald-200 dark:border-emerald-800/60 text-slate-800 dark:text-slate-200 leading-relaxed">
                                      <span className="font-bold text-emerald-800 dark:text-emerald-300 block mb-1">
                                        💡 Klinik & Patofizyolojik Çözüm Notu:
                                      </span>
                                      <p>{renderHighlightedText(q.explanation)}</p>
                                    </div>
                                  )}
                                </div>
                              )}
                            </div>
                          </div>
                        );
                      }

                      // 5. Hierarchical Bullet Lists (Maddelendirmeler)
                      if (block.type === 'bulletList') {
                        return (
                          <div key={bIdx} className="space-y-3 my-2">
                            {block.items.map((it: BulletItem, itIdx: number) => {
                              return (
                                <div
                                  key={itIdx}
                                  className="p-3.5 sm:p-4 rounded-xl bg-[var(--reader-card,#ffffff)] border border-[var(--reader-border,#e2e8f0)] space-y-2 hover:border-teal-400/60 transition-colors shadow-2xs"
                                >
                                  {/* Lead-in Keyword */}
                                  <div className="flex items-start gap-2.5">
                                    <span className="w-2 h-2 rounded-full bg-teal-600 shrink-0 mt-2" />
                                    <div className="flex-1 space-y-1">
                                      {it.key && (
                                        <h4 className="font-bold text-xs sm:text-sm text-slate-900 dark:text-slate-100">
                                          {renderHighlightedText(it.key)}
                                        </h4>
                                      )}
                                      {it.content && (
                                        <p className="text-xs sm:text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                                          {renderHighlightedText(it.content)}
                                        </p>
                                      )}
                                    </div>
                                  </div>

                                  {/* Concatenated Numbered Pills (e.g. 1. Standart Önlemler, 2. Bulaş Yolu) */}
                                  {it.numberedPills && it.numberedPills.length > 0 && (
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 pl-4">
                                      {it.numberedPills.map((pill, pIdx) => (
                                        <div
                                          key={pIdx}
                                          className="p-2 rounded-lg bg-teal-50/70 dark:bg-teal-950/40 border border-teal-200 dark:border-teal-800/60 text-xs font-medium text-teal-900 dark:text-teal-200"
                                        >
                                          {renderHighlightedText(pill)}
                                        </div>
                                      ))}
                                    </div>
                                  )}

                                  {/* Nested Sub-bullets */}
                                  {it.subItems && it.subItems.length > 0 && (
                                    <ul className="pl-6 space-y-1.5 border-l-2 border-teal-200 dark:border-teal-800/80 ml-3.5 mt-2">
                                      {it.subItems.map((sub, sIdx) => (
                                        <li
                                          key={sIdx}
                                          className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 flex items-start gap-2 leading-relaxed"
                                        >
                                          <span className="text-teal-500 font-bold shrink-0 mt-0.5">•</span>
                                          <span>{renderHighlightedText(sub)}</span>
                                        </li>
                                      ))}
                                    </ul>
                                  )}
                                </div>
                              );
                            })}
                          </div>
                        );
                      }

                      // 6. Regular Paragraph
                      return (
                        <p
                          key={bIdx}
                          className="text-xs sm:text-sm text-slate-700 dark:text-slate-300 leading-relaxed"
                        >
                          {renderHighlightedText(block.text)}
                        </p>
                      );
                    })}
                  </div>
                </section>
              );
            })}

            {/* Back to top & PDF footer action */}
            <div className="pt-10 pb-6 border-t border-[var(--reader-border,#e2e8f0)] flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-600" />
                <span>Bu ders özetinin sonuna ulaştınız. Harika bir çalışma oldu!</span>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => contentAreaRef.current?.scrollTo({ top: 0, behavior: 'smooth' })}
                  className="px-3 py-1.5 rounded-lg border border-[var(--reader-border,#e2e8f0)] hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center gap-1 font-semibold cursor-pointer"
                >
                  <ArrowUp className="w-3.5 h-3.5" />
                  <span>Başa Dön</span>
                </button>

                {onOpenPdfModal && (
                  <button
                    type="button"
                    onClick={onOpenPdfModal}
                    className="px-3 py-1.5 rounded-lg bg-teal-700 hover:bg-teal-800 text-white font-bold flex items-center gap-1 cursor-pointer"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>PDF İndirme Merkezine Git</span>
                  </button>
                )}
              </div>
            </div>
            </>
            )}
          </main>
        </div>

        {/* ========================================================
            BOTTOM STATUS BAR
            ======================================================== */}
        <footer className="p-3 bg-slate-900 border-t border-slate-800 text-slate-400 text-xs flex items-center justify-between shrink-0">
          <div className="flex items-center gap-2 truncate">
            <span className="font-semibold text-slate-300">MedSoru Artifact Reader</span>
            <span>•</span>
            <span className="truncate">{summary.title}</span>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <span className="font-mono text-[11px] text-teal-400">Okuma İlerlemesi: %{scrollProgress}</span>
            <button
              type="button"
              onClick={onClose}
              className="bg-slate-800 hover:bg-slate-700 text-white font-bold px-3 py-1 rounded-lg cursor-pointer transition-colors"
            >
              Kapat (ESC)
            </button>
          </div>
        </footer>
      </div>
    </div>
  );
};
