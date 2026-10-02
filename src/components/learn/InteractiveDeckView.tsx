import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  Sparkles,
  BookOpen,
  Volume2,
  Maximize2,
  Minimize2,
  ChevronLeft,
  ChevronRight,
  HelpCircle,
  CheckCircle2,
  XCircle,
  Lightbulb,
  Search,
  Layers,
  Clock,
  User,
  GraduationCap,
  MessageSquare,
  Send,
  RotateCcw,
  List,
  Check,
  Zap,
  ArrowRight,
  ExternalLink,
  Flame,
  AlertTriangle,
  Play,
  Share2,
  Sliders,
  Compass,
  LayoutGrid
} from 'lucide-react';
import interactiveDecksData from '../../data/interactive_learning_decks.json';

export interface ProfessorAudioHighlight {
  timestamp: string;
  quote: string;
  emphasisType: 'direct_exam_warning' | 'pearl' | 'clinical_tip' | 'slide_missing';
  note: string;
}

export interface SlideQuestionOption {
  key: string;
  text: string;
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
  badge: string;
  badgeColor?: string;
  professorAudioHighlight?: ProfessorAudioHighlight;
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
  totalSlides: number;
  matchedPastQuestionsCount: number;
  slides: SlideItem[];
}

interface InteractiveDeckViewProps {
  onOpenPdfModal?: () => void;
  initialDeckId?: string | null;
  onSelectCommittee?: (committeeId: string) => void;
}

const DISCIPLINE_THEMES: Record<string, { bg: string; text: string; border: string; accent: string; badgeBg: string }> = {
  'Halk Sağlığı': {
    bg: 'bg-sky-50 dark:bg-sky-950/40',
    text: 'text-sky-800 dark:text-sky-300',
    border: 'border-sky-200 dark:border-sky-800/60',
    accent: 'bg-sky-600',
    badgeBg: 'bg-sky-100 text-sky-800 border-sky-300',
  },
  'Tıbbi Genetik': {
    bg: 'bg-indigo-50 dark:bg-indigo-950/40',
    text: 'text-indigo-800 dark:text-indigo-300',
    border: 'border-indigo-200 dark:border-indigo-800/60',
    accent: 'bg-indigo-600',
    badgeBg: 'bg-indigo-100 text-indigo-800 border-indigo-300',
  },
  'Enfeksiyon Hastalıkları': {
    bg: 'bg-emerald-50 dark:bg-emerald-950/40',
    text: 'text-emerald-800 dark:text-emerald-300',
    border: 'border-emerald-200 dark:border-emerald-800/60',
    accent: 'bg-emerald-600',
    badgeBg: 'bg-emerald-100 text-emerald-800 border-emerald-300',
  },
  'Üroloji': {
    bg: 'bg-amber-50 dark:bg-amber-950/40',
    text: 'text-amber-800 dark:text-amber-300',
    border: 'border-amber-200 dark:border-amber-800/60',
    accent: 'bg-amber-600',
    badgeBg: 'bg-amber-100 text-amber-800 border-amber-300',
  },
};

export const InteractiveDeckView: React.FC<InteractiveDeckViewProps> = ({
  initialDeckId,
}) => {
  const allDecks: InteractiveDeck[] = interactiveDecksData as InteractiveDeck[];

  // Selected deck & active slide
  const [selectedDeckId, setSelectedDeckId] = useState<string | null>(initialDeckId || null);
  const [activeSlideIndex, setActiveSlideIndex] = useState<number>(0);

  // View presentation mode: 'presentation' (PPTX slide deck) or 'continuous' (downward scrolling)
  const [viewMode, setViewMode] = useState<'presentation' | 'continuous'>('presentation');

  // Fullscreen state
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const presentationContainerRef = useRef<HTMLDivElement>(null);

  // Slide drawer / TOC
  const [isDrawerOpen, setIsDrawerOpen] = useState<boolean>(false);

  // Search & Filter in Deck Hub
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('all');

  // Interactive Quiz state: { [questionId]: selectedOptionKey }
  const [quizAnswers, setQuizAnswers] = useState<Record<string, string>>({});
  const [revealedExplanations, setRevealedExplanations] = useState<Record<string, boolean>>({});

  // Slide RAG AI Chat
  const [aiQuery, setAiQuery] = useState('');
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [aiReferences, setAiReferences] = useState<any[]>([]);
  const [copiedQuote, setCopiedQuote] = useState(false);

  // Active deck object
  const activeDeck = useMemo(() => {
    return allDecks.find((d) => d.id === selectedDeckId) || null;
  }, [allDecks, selectedDeckId]);

  // Active slide object
  const activeSlide = useMemo(() => {
    if (!activeDeck || !activeDeck.slides || activeDeck.slides.length === 0) return null;
    const safeIdx = Math.min(Math.max(0, activeSlideIndex), activeDeck.slides.length - 1);
    return activeDeck.slides[safeIdx];
  }, [activeDeck, activeSlideIndex]);

  // Discipline options
  const disciplines = useMemo(() => {
    const set = new Set<string>();
    allDecks.forEach((d) => d.discipline && set.add(d.discipline));
    return Array.from(set).sort();
  }, [allDecks]);

  // Filtered decks for Hub list
  const filteredDecks = useMemo(() => {
    return allDecks.filter((d) => {
      if (selectedDiscipline !== 'all' && d.discipline !== selectedDiscipline) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const inTitle = d.title.toLowerCase().includes(q);
        const inDisc = d.discipline.toLowerCase().includes(q);
        const inOverview = d.overview.toLowerCase().includes(q);
        const inPearls = d.highYieldPearls.some((p) => p.toLowerCase().includes(q));
        if (!inTitle && !inDisc && !inOverview && !inPearls) return false;
      }
      return true;
    });
  }, [allDecks, selectedDiscipline, searchQuery]);

  // Handle Fullscreen toggle
  const toggleFullscreen = () => {
    if (!presentationContainerRef.current) return;
    if (!document.fullscreenElement) {
      presentationContainerRef.current.requestFullscreen().catch(() => {});
      setIsFullscreen(true);
    } else {
      document.exitFullscreen().catch(() => {});
      setIsFullscreen(false);
    }
  };

  useEffect(() => {
    const handleFsChange = () => {
      setIsFullscreen(Boolean(document.fullscreenElement));
    };
    document.addEventListener('fullscreenchange', handleFsChange);
    return () => document.removeEventListener('fullscreenchange', handleFsChange);
  }, []);

  // Keyboard navigation for presentation mode
  useEffect(() => {
    if (!activeDeck || viewMode !== 'presentation') return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (['input', 'textarea'].includes((e.target as HTMLElement)?.tagName?.toLowerCase())) return;

      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
        e.preventDefault();
        setActiveSlideIndex((prev) => Math.min(prev + 1, activeDeck.slides.length - 1));
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        setActiveSlideIndex((prev) => Math.max(prev - 1, 0));
      } else if (e.key.toLowerCase() === 'f') {
        toggleFullscreen();
      } else if (e.key === 'Escape' && isFullscreen) {
        document.exitFullscreen().catch(() => {});
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [activeDeck, viewMode, isFullscreen]);

  // Reset slide index & AI response when deck changes
  const handleSelectDeck = (deckId: string) => {
    setSelectedDeckId(deckId);
    setActiveSlideIndex(0);
    setAiResponse(null);
    setAiReferences([]);
    setAiQuery('');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Submit AI Question using RAG Engine
  const handleAskAi = async (customPrompt?: string) => {
    const promptToSend = customPrompt || aiQuery;
    if (!promptToSend.trim() || !activeSlide || !activeDeck) return;

    setAiLoading(true);
    setAiResponse(null);
    setAiReferences([]);

    try {
      const slideContext = `
Ders: ${activeDeck.title} (${activeDeck.discipline} - ${activeDeck.committee})
Öğretim Üyesi: ${activeDeck.instructor}
Slayt Başlığı: ${activeSlide.title} - ${activeSlide.subtitle}
Hocanın Amfi Vurgusu: "${activeSlide.professorAudioHighlight?.quote || ''}" (Dakika: ${activeSlide.professorAudioHighlight?.timestamp || ''})
Slayt Temel İçeriği:
${activeSlide.coreContent.keyBullets?.map((b) => `- ${b.title}: ${b.desc}`).join('\n') || ''}
Spot Bilgiler:
${activeSlide.spotPearls.map((p) => `* ${p}`).join('\n')}
      `.trim();

      const response = await fetch('/api/rag/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: `${promptToSend}\n\n[İlgili Ders Slayt ve Hoca Ses Bağlamı]:\n${slideContext}`,
          discipline: activeDeck.discipline,
          committeeId: activeDeck.committee,
          mode: 'qa',
          limit: 4,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.answer) {
          setAiResponse(data.answer);
          setAiReferences(data.references || []);
          setAiLoading(false);
          return;
        }
      }
    } catch (_) {}

    // Fallback response if offline or server API unavailable
    setTimeout(() => {
      const quote = activeSlide.professorAudioHighlight?.quote;
      const fallback = `
### 🩺 Amfi & Sınav Değerlendirmesi:
**Soru:** *${promptToSend}*

Bu konuda ders sorumlusu hocamız **[${activeSlide.professorAudioHighlight?.timestamp || 'Ders İçi'}]** dakikasında özellikle şu can alıcı noktayı vurguladı:
> "${quote || activeSlide.title}"

**Klinik & Sınav İpucu:**
${activeSlide.spotPearls.join('\n\n')}

Bu konuyla ilgili geçmiş kurullarda **${activeSlide.relatedQuestions.length} adet çıkmış soru** bulunmaktadır. Lütfen slayt altındaki çıkmış soru seçeneklerini çözerek bilginizi pekiştirin.
      `.trim();

      setAiResponse(fallback);
      setAiLoading(false);
    }, 600);
  };

  const handleCopyQuote = (quote: string) => {
    navigator.clipboard.writeText(quote);
    setCopiedQuote(true);
    setTimeout(() => setCopiedQuote(false), 2000);
  };

  // If no deck selected, show the Decks Hub (Öğren Kataloğu)
  if (!activeDeck) {
    return (
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-10 space-y-8 animate-in fade-in duration-300">
        {/* Hero Header */}
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-6 sm:p-10 border border-slate-800 shadow-2xl">
          <div className="absolute top-0 right-0 -mt-10 -mr-10 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 left-1/3 -mb-10 w-80 h-80 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />

          <div className="relative z-10 max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/20 border border-indigo-400/30 text-indigo-300 text-xs font-bold tracking-wide uppercase">
              <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
              Yapay Zeka Destekli Ses & Slayt Hub'ı
            </div>

            <h1 className="text-2xl sm:text-4xl lg:text-5xl font-black tracking-tight leading-tight text-white">
              Hocanın Sesiyle Ders Notları & Çıkmış Sorular Tek Bir Yerde
            </h1>

            <p className="text-sm sm:text-base text-slate-300 leading-relaxed">
              Amfi ses kayıtlarındaki hocaların <strong className="text-white font-semibold">"Buradan soru sorarız"</strong> ve <strong className="text-white font-semibold">"Slaytta yok, beni dinleyin"</strong> dediği en kritik yerler tespit edildi; tam metin ders slaytları, spot hap bilgiler ve gerçek kurul çıkmış sorularıyla eşleştirildi.
            </p>

            <div className="flex flex-wrap items-center gap-4 pt-2 text-xs sm:text-sm text-slate-300 font-medium">
              <span className="flex items-center gap-1.5 bg-white/10 px-3 py-1.5 rounded-xl border border-white/10">
                <Volume2 className="w-4 h-4 text-sky-400" />
                7 Tam Ses Transkripti Eşleşti
              </span>
              <span className="flex items-center gap-1.5 bg-white/10 px-3 py-1.5 rounded-xl border border-white/10">
                <Layers className="w-4 h-4 text-emerald-400" />
                877 Ders Notu Arşivinden Doğrulandı
              </span>
              <span className="flex items-center gap-1.5 bg-white/10 px-3 py-1.5 rounded-xl border border-white/10">
                <GraduationCap className="w-4 h-4 text-amber-400" />
                3.349 Çıkmış Soruyla İlişkilendirildi
              </span>
            </div>
          </div>
        </div>

        {/* Filter & Search Bar */}
        <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center justify-between">
          <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0 no-scrollbar">
            <button
              onClick={() => setSelectedDiscipline('all')}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all shrink-0 cursor-pointer ${
                selectedDiscipline === 'all'
                  ? 'bg-slate-900 text-white shadow-sm'
                  : 'bg-white hover:bg-slate-100 text-slate-600 border border-slate-200'
              }`}
            >
              Tüm Disiplinler ({allDecks.length})
            </button>
            {disciplines.map((d) => (
              <button
                key={d}
                onClick={() => setSelectedDiscipline(d)}
                className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all shrink-0 cursor-pointer ${
                  selectedDiscipline === d
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'bg-white hover:bg-slate-100 text-slate-600 border border-slate-200'
                }`}
              >
                {d}
              </button>
            ))}
          </div>

          <div className="relative min-w-[260px]">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Ders adı, hoca vurgusu veya anahtar kelime..."
              className="w-full pl-9 pr-4 py-2 bg-white rounded-xl border border-slate-200 text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all placeholder:text-slate-400"
            />
          </div>
        </div>

        {/* Deck Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDecks.map((deck) => {
            const theme = DISCIPLINE_THEMES[deck.discipline] || DISCIPLINE_THEMES['Halk Sağlığı'];

            return (
              <div
                key={deck.id}
                className="group bg-white rounded-2xl border border-slate-200 hover:border-indigo-300 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col overflow-hidden"
              >
                {/* Card Top Banner */}
                <div className={`p-5 ${theme.bg} border-b ${theme.border} flex flex-col gap-2.5`}>
                  <div className="flex items-center justify-between gap-2">
                    <span className={`text-[11px] font-bold px-2.5 py-1 rounded-full border uppercase tracking-wider ${theme.badgeBg}`}>
                      {deck.discipline}
                    </span>
                    <span className="text-[11px] font-medium text-slate-500 flex items-center gap-1 bg-white/80 px-2 py-0.5 rounded-md border border-slate-200">
                      <Clock className="w-3 h-3 text-slate-400" />
                      {deck.audioDuration}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-slate-900 group-hover:text-indigo-600 transition-colors line-clamp-2 leading-snug">
                    {deck.title}
                  </h3>

                  {deck.instructor && deck.instructor !== 'Öğretim Üyesi' && (
                    <p className="text-xs text-slate-600 flex items-center gap-1">
                      <User className="w-3.5 h-3.5 text-slate-400" />
                      {deck.instructor}
                    </p>
                  )}
                </div>

                {/* Card Body */}
                <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
                  <p className="text-xs sm:text-[13px] text-slate-600 leading-relaxed line-clamp-3">
                    {deck.overview}
                  </p>

                  {/* Highlights Pill Box */}
                  <div className="space-y-2 pt-2 border-t border-slate-100">
                    <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                      <Flame className="w-3 h-3 text-rose-500" />
                      Öne Çıkan Amfi Hapı
                    </div>
                    {deck.highYieldPearls.length > 0 && (
                      <p className="text-xs text-slate-700 bg-slate-50 p-2.5 rounded-xl border border-slate-200/80 leading-snug line-clamp-2">
                        {deck.highYieldPearls[0]}
                      </p>
                    )}
                  </div>

                  {/* Metrics Bar */}
                  <div className="grid grid-cols-2 gap-2 text-center text-xs">
                    <div className="bg-slate-50 p-2 rounded-xl border border-slate-100">
                      <div className="font-extrabold text-slate-900 text-sm">{deck.totalSlides} Slayt</div>
                      <div className="text-[10px] text-slate-500 font-medium">İnteraktif Slayt</div>
                    </div>
                    <div className="bg-indigo-50/60 p-2 rounded-xl border border-indigo-100">
                      <div className="font-extrabold text-indigo-700 text-sm">{deck.matchedPastQuestionsCount} Soru</div>
                      <div className="text-[10px] text-indigo-600 font-medium">Eşleşen Çıkmış</div>
                    </div>
                  </div>

                  {/* Action Button */}
                  <button
                    onClick={() => handleSelectDeck(deck.id)}
                    className="w-full mt-2 py-2.5 px-4 rounded-xl bg-slate-900 hover:bg-indigo-600 text-white text-xs sm:text-sm font-bold flex items-center justify-center gap-2 transition-all shadow-sm group-hover:shadow cursor-pointer"
                  >
                    <span>Dersi İncele & Slayt Sunumu</span>
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  // --------------------------------------------------------------------------
  // ACTIVE DECK PLAYER (PPTX Presentation Mode + Continuous Scroll Mode)
  // --------------------------------------------------------------------------
  const theme = DISCIPLINE_THEMES[activeDeck.discipline] || DISCIPLINE_THEMES['Halk Sağlığı'];
  const totalSlides = activeDeck.slides.length;
  const currentSlideNum = activeSlide ? activeSlide.slideNumber : 1;

  return (
    <div
      ref={presentationContainerRef}
      className={`min-h-screen bg-slate-100 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors ${
        isFullscreen ? 'p-3 sm:p-6 flex flex-col justify-between' : 'pb-16'
      }`}
    >
      {/* Top Sticky Navigation Bar */}
      <div className="sticky top-0 z-30 bg-white/95 dark:bg-slate-900/95 backdrop-blur border-b border-slate-200 dark:border-slate-800 shadow-xs px-3 sm:px-6 py-2.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-3">
          {/* Left: Back button + Title */}
          <div className="flex items-center gap-3 min-w-0">
            <button
              onClick={() => setSelectedDeckId(null)}
              className="p-1.5 sm:px-3 sm:py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer shrink-0"
              title="Öğren Kataloğuna Dön"
            >
              <ChevronLeft className="w-4 h-4" />
              <span className="hidden sm:inline">Kataloğa Dön</span>
            </button>

            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md border ${theme.badgeBg}`}>
                  {activeDeck.discipline}
                </span>
                <span className="text-[11px] text-slate-500 truncate hidden md:inline">
                  {activeDeck.committee}
                </span>
              </div>
              <h2 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-white truncate">
                {activeDeck.title}
              </h2>
            </div>
          </div>

          {/* Center / Right: Mode Switchers & Controls */}
          <div className="flex items-center gap-2 shrink-0">
            {/* Presentation Mode vs Continuous Scroll Toggle */}
            <div className="bg-slate-100 dark:bg-slate-800 p-0.5 rounded-xl flex items-center border border-slate-200 dark:border-slate-700">
              <button
                onClick={() => setViewMode('presentation')}
                className={`px-2.5 py-1 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer ${
                  viewMode === 'presentation'
                    ? 'bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 shadow-xs'
                    : 'text-slate-500 hover:text-slate-800'
                }`}
                title="PPTX Slayt Sunumu Modu"
              >
                <Sliders className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Slayt Modu</span>
              </button>
              <button
                onClick={() => setViewMode('continuous')}
                className={`px-2.5 py-1 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer ${
                  viewMode === 'continuous'
                    ? 'bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 shadow-xs'
                    : 'text-slate-500 hover:text-slate-800'
                }`}
                title="Aşağı Doğru Kaydırma Modu"
              >
                <List className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Dikey Akış</span>
              </button>
            </div>

            {/* Slide Index Pill in Presentation Mode */}
            {viewMode === 'presentation' && (
              <span className="text-xs font-bold font-mono px-2.5 py-1 bg-slate-100 dark:bg-slate-800 rounded-lg text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 hidden sm:inline">
                {currentSlideNum} / {totalSlides}
              </span>
            )}

            {/* Slide Drawer Toggle */}
            <button
              onClick={() => setIsDrawerOpen(!isDrawerOpen)}
              className="p-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition-all cursor-pointer"
              title="Slayt Listesi / İndeks"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>

            {/* Fullscreen Toggle */}
            <button
              onClick={toggleFullscreen}
              className="p-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition-all cursor-pointer"
              title={isFullscreen ? 'Tam Ekrandan Çık (Esc / F)' : 'Tam Ekran Sunum (F)'}
            >
              {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="max-w-6xl mx-auto px-3 sm:px-6 pt-4 sm:pt-6 relative">
        {/* Slide Drawer Dropdown / Modal */}
        {isDrawerOpen && (
          <div className="mb-6 p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xl space-y-3 animate-in fade-in duration-200">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Slayt Listesi ({totalSlides} Slayt)
              </span>
              <button
                onClick={() => setIsDrawerOpen(false)}
                className="text-xs text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 font-bold"
              >
                Kapat
              </button>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 max-h-60 overflow-y-auto pr-1">
              {activeDeck.slides.map((s, idx) => (
                <button
                  key={s.slideNumber}
                  onClick={() => {
                    setActiveSlideIndex(idx);
                    setIsDrawerOpen(false);
                  }}
                  className={`text-left p-2.5 rounded-xl border text-xs transition-all cursor-pointer flex items-start gap-2.5 ${
                    activeSlideIndex === idx
                      ? 'border-indigo-500 bg-indigo-50/70 dark:bg-indigo-950/60 font-semibold text-indigo-900 dark:text-indigo-200'
                      : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 text-slate-700 dark:text-slate-300'
                  }`}
                >
                  <span className="w-6 h-6 rounded-lg bg-slate-200 dark:bg-slate-800 flex items-center justify-center font-mono font-bold text-[11px] shrink-0">
                    {s.slideNumber}
                  </span>
                  <div className="min-w-0">
                    <div className="truncate font-bold">{s.title}</div>
                    <div className="text-[10px] text-slate-500 truncate">{s.subtitle}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* MODE 1: PPTX PRESENTATION SLIDE MODE */}
        {viewMode === 'presentation' && activeSlide && (
          <div className="space-y-6">
            {/* The PPTX Slide Canvas Card */}
            <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden flex flex-col min-h-[620px]">
              {/* Slide Top Header Bar */}
              <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-950 text-white px-5 sm:px-8 py-5 flex items-start justify-between gap-4 border-b border-slate-800">
                <div className="space-y-1.5 min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="bg-indigo-500/20 text-indigo-300 text-[10px] font-bold px-2.5 py-0.5 rounded-full border border-indigo-400/30 uppercase tracking-wider">
                      Slayt {activeSlide.slideNumber} / {totalSlides}
                    </span>
                    <span className="bg-amber-500/20 text-amber-300 text-[10px] font-bold px-2.5 py-0.5 rounded-full border border-amber-400/30 uppercase tracking-wider flex items-center gap-1">
                      <Flame className="w-3 h-3 text-amber-400" />
                      {activeSlide.badge}
                    </span>
                  </div>

                  <h1 className="text-xl sm:text-2xl lg:text-3xl font-black text-white tracking-tight leading-tight">
                    {activeSlide.title}
                  </h1>

                  <p className="text-xs sm:text-sm text-indigo-200 font-medium">
                    {activeSlide.subtitle}
                  </p>
                </div>

                <div className="hidden sm:flex items-center gap-2 shrink-0">
                  {activeDeck.instructor && (
                    <div className="text-right text-xs text-slate-300 font-medium">
                      <div>{activeDeck.instructor}</div>
                      <div className="text-[10px] text-slate-400">{activeDeck.audioFile}</div>
                    </div>
                  )}
                </div>
              </div>

              {/* Slide Body Container */}
              <div className="p-5 sm:p-8 space-y-6 flex-1">
                {/* 1. HOCANIN SES KAYDI & AMFİ VURGUSU BOX */}
                {activeSlide.professorAudioHighlight && (
                  <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-rose-50 via-amber-50/50 to-orange-50 dark:from-rose-950/30 dark:via-amber-950/20 dark:to-orange-950/30 border-2 border-rose-200 dark:border-rose-900/60 p-4 sm:p-5 shadow-xs space-y-2.5">
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex items-center gap-2 text-rose-800 dark:text-rose-300 text-xs font-black uppercase tracking-wider">
                        <Volume2 className="w-4 h-4 text-rose-600 animate-pulse" />
                        <span>Hocanın Ses Kaydı & Amfi Vurgusu</span>
                        <span className="bg-rose-200/80 dark:bg-rose-900/60 text-rose-900 dark:text-rose-200 font-mono text-[11px] px-2 py-0.5 rounded-md">
                          [{activeSlide.professorAudioHighlight.timestamp}]
                        </span>
                      </div>

                      <button
                        onClick={() => handleCopyQuote(activeSlide.professorAudioHighlight!.quote)}
                        className="text-[11px] font-bold text-rose-700 dark:text-rose-300 hover:underline flex items-center gap-1 cursor-pointer"
                      >
                        {copiedQuote ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Share2 className="w-3.5 h-3.5" />}
                        {copiedQuote ? 'Kopyalandı' : 'Alıntıyı Kopyala'}
                      </button>
                    </div>

                    <blockquote className="text-sm sm:text-base font-semibold text-slate-900 dark:text-slate-100 italic leading-relaxed pl-3 border-l-3 border-rose-400">
                      "{activeSlide.professorAudioHighlight.quote}"
                    </blockquote>

                    <p className="text-xs text-rose-900/80 dark:text-rose-300/80 font-medium">
                      💡 <strong>Sınav Analizi:</strong> {activeSlide.professorAudioHighlight.note}
                    </p>
                  </div>
                )}

                {/* 2. DERS NOTU & SLAYT TEMEL İÇERİĞİ */}
                {activeSlide.coreContent && (
                  <div className="space-y-4">
                    {/* Key Bullets */}
                    {activeSlide.coreContent.keyBullets && activeSlide.coreContent.keyBullets.length > 0 && (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {activeSlide.coreContent.keyBullets.map((bullet, bIdx) => (
                          <div
                            key={bIdx}
                            className="bg-slate-50 dark:bg-slate-800/60 rounded-xl p-3.5 border border-slate-200/80 dark:border-slate-700/60 flex items-start gap-3"
                          >
                            <span className="w-6 h-6 rounded-lg bg-indigo-100 dark:bg-indigo-900/60 text-indigo-700 dark:text-indigo-300 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                              {bIdx + 1}
                            </span>
                            <div className="space-y-0.5 min-w-0">
                              <h4 className="text-xs sm:text-sm font-bold text-slate-900 dark:text-white">
                                {bullet.title}
                              </h4>
                              <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                                {bullet.desc}
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Table if present */}
                    {activeSlide.coreContent.table && (
                      <div className="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 shadow-xs">
                        {activeSlide.coreContent.table.title && (
                          <div className="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 font-bold text-xs text-slate-700 dark:text-slate-300 border-b border-slate-200 dark:border-slate-700">
                            📊 {activeSlide.coreContent.table.title}
                          </div>
                        )}
                        <div className="overflow-x-auto">
                          <table className="w-full text-left text-xs">
                            <thead>
                              <tr className="bg-slate-50 dark:bg-slate-800/40 border-b border-slate-200 dark:border-slate-700 text-slate-500 font-bold uppercase tracking-wider">
                                {activeSlide.coreContent.table.headers.map((h, hIdx) => (
                                  <th key={hIdx} className="px-4 py-3">
                                    {h}
                                  </th>
                                ))}
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                              {activeSlide.coreContent.table.rows.map((row, rIdx) => (
                                <tr key={rIdx} className="hover:bg-slate-50/80 dark:hover:bg-slate-800/50 transition-colors">
                                  {row.map((cell, cIdx) => (
                                    <td key={cIdx} className="px-4 py-3 font-medium text-slate-800 dark:text-slate-200">
                                      {cell}
                                    </td>
                                  ))}
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    )}

                    {/* Formula Box if present */}
                    {activeSlide.coreContent.formulaBox && (
                      <div className="rounded-2xl bg-indigo-900 text-white p-5 space-y-2 border border-indigo-700 shadow-md">
                        <div className="text-xs font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                          <Zap className="w-4 h-4 text-amber-400" />
                          {activeSlide.coreContent.formulaBox.title}
                        </div>
                        <div className="font-mono text-sm sm:text-base font-bold text-amber-300 bg-black/30 p-3 rounded-xl border border-white/10 overflow-x-auto">
                          {activeSlide.coreContent.formulaBox.formula}
                        </div>
                        <p className="text-xs text-indigo-200">
                          {activeSlide.coreContent.formulaBox.explanation}
                        </p>
                      </div>
                    )}
                  </div>
                )}

                {/* 3. SPOT BİLGİLER & HAP NOTLAR */}
                {activeSlide.spotPearls && activeSlide.spotPearls.length > 0 && (
                  <div className="rounded-2xl bg-amber-50/70 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/50 p-4 sm:p-5 space-y-3">
                    <div className="flex items-center gap-2 text-amber-800 dark:text-amber-300 text-xs font-bold uppercase tracking-wider">
                      <Zap className="w-4 h-4 text-amber-500" />
                      Spot Bilgiler & Akılda Tutma İpuçları (High-Yield Pearls)
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                      {activeSlide.spotPearls.map((pearl, pIdx) => (
                        <div key={pIdx} className="flex items-start gap-2 text-xs text-amber-950 dark:text-amber-200 leading-snug">
                          <CheckCircle2 className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
                          <span>{pearl}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* 4. ÇIKMIŞ SORU ATÖLYESİ (INTERACTIVE EXAM QUESTIONS) */}
                {activeSlide.relatedQuestions && activeSlide.relatedQuestions.length > 0 && (
                  <div className="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-800">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 text-indigo-900 dark:text-indigo-300 font-bold text-sm">
                        <GraduationCap className="w-5 h-5 text-indigo-600" />
                        <span>Bu Slaytla Eşleşen Gerçek Çıkmış Kurul Soruları</span>
                        <span className="bg-indigo-100 text-indigo-800 text-xs font-mono px-2 py-0.5 rounded-full font-bold">
                          {activeSlide.relatedQuestions.length} Soru
                        </span>
                      </div>
                    </div>

                    <div className="space-y-4">
                      {activeSlide.relatedQuestions.map((q) => {
                        const userChoice = quizAnswers[q.id];
                        const isAnswered = Boolean(userChoice);
                        const isCorrect = userChoice === q.correctAnswer;
                        const showExplanation = revealedExplanations[q.id] || isAnswered;

                        return (
                          <div
                            key={q.id}
                            className="bg-slate-50 dark:bg-slate-800/40 rounded-2xl border border-slate-200 dark:border-slate-700/80 p-4 sm:p-5 space-y-3.5"
                          >
                            <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
                              <span className="font-bold text-slate-500 font-mono bg-white dark:bg-slate-800 px-2.5 py-1 rounded-md border border-slate-200 dark:border-slate-700">
                                {q.examYear} • {q.committeeId}
                              </span>
                              <span className="text-[11px] font-semibold text-indigo-600 dark:text-indigo-400">
                                {q.topic || activeDeck.discipline}
                              </span>
                            </div>

                            {/* Stem */}
                            <p className="text-xs sm:text-sm font-semibold text-slate-900 dark:text-white leading-relaxed">
                              {q.stem}
                            </p>

                            {/* Options */}
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                              {q.options.map((opt) => {
                                const isSelected = userChoice === opt.key;
                                const isRealAnswer = q.correctAnswer === opt.key;

                                let optClasses = 'bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 hover:border-indigo-400';
                                if (isAnswered) {
                                  if (isRealAnswer) {
                                    optClasses = 'bg-emerald-50 dark:bg-emerald-950/50 border-emerald-500 text-emerald-900 dark:text-emerald-200 font-semibold ring-1 ring-emerald-500';
                                  } else if (isSelected && !isCorrect) {
                                    optClasses = 'bg-rose-50 dark:bg-rose-950/50 border-rose-500 text-rose-900 dark:text-rose-200 font-semibold';
                                  } else {
                                    optClasses = 'opacity-60 bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700';
                                  }
                                }

                                return (
                                  <button
                                    key={opt.key}
                                    onClick={() => {
                                      setQuizAnswers((prev) => ({ ...prev, [q.id]: opt.key }));
                                    }}
                                    className={`w-full text-left p-2.5 rounded-xl border text-xs transition-all flex items-start gap-2.5 cursor-pointer ${optClasses}`}
                                  >
                                    <span
                                      className={`w-6 h-6 rounded-lg flex items-center justify-center font-mono font-bold text-xs shrink-0 ${
                                        isAnswered && isRealAnswer
                                          ? 'bg-emerald-600 text-white'
                                          : isAnswered && isSelected && !isCorrect
                                          ? 'bg-rose-600 text-white'
                                          : 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
                                      }`}
                                    >
                                      {opt.key}
                                    </span>
                                    <span className="flex-1 mt-0.5">{opt.text}</span>
                                  </button>
                                );
                              })}
                            </div>

                            {/* Answer Feedback & Explanation */}
                            {showExplanation && (
                              <div className="pt-2 text-xs space-y-2 animate-in fade-in duration-200">
                                <div
                                  className={`p-3 rounded-xl border flex items-start gap-2 font-medium ${
                                    isCorrect
                                      ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-200 text-emerald-800 dark:text-emerald-300'
                                      : 'bg-slate-100 dark:bg-slate-800 border-slate-200 text-slate-800 dark:text-slate-200'
                                  }`}
                                >
                                  {isCorrect ? (
                                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                                  ) : (
                                    <HelpCircle className="w-4 h-4 text-indigo-600 shrink-0 mt-0.5" />
                                  )}
                                  <div>
                                    <p className="font-bold">
                                      Doğru Cevap: <span className="font-mono">{q.correctAnswer}</span>
                                    </p>
                                    <p className="mt-1 leading-relaxed">
                                      {q.explanation || 'Bu soru doğrudan yukarıdaki slaytta açıklanan temel ilke ve formüle dayanmaktadır.'}
                                    </p>
                                  </div>
                                </div>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>

              {/* Slide Bottom Presentation Controller */}
              <div className="bg-slate-50 dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 px-5 sm:px-8 py-4 flex flex-col sm:flex-row items-center justify-between gap-4">
                {/* Dots / Timeline */}
                <div className="flex items-center gap-1.5 overflow-x-auto max-w-full pb-1 sm:pb-0 no-scrollbar">
                  {activeDeck.slides.map((s, idx) => (
                    <button
                      key={s.slideNumber}
                      onClick={() => setActiveSlideIndex(idx)}
                      className={`h-2.5 rounded-full transition-all cursor-pointer ${
                        activeSlideIndex === idx
                          ? 'w-8 bg-indigo-600'
                          : 'w-2.5 bg-slate-300 dark:bg-slate-700 hover:bg-slate-400'
                      }`}
                      title={`Slayt ${s.slideNumber}: ${s.title}`}
                    />
                  ))}
                </div>

                {/* Prev / Next Buttons */}
                <div className="flex items-center gap-3">
                  <button
                    disabled={activeSlideIndex <= 0}
                    onClick={() => setActiveSlideIndex((prev) => Math.max(0, prev - 1))}
                    className="px-4 py-2 rounded-xl bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-bold border border-slate-200 dark:border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5 transition-all cursor-pointer shadow-xs"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    Önceki Slayt
                  </button>

                  <span className="text-xs font-mono font-bold text-slate-500">
                    {currentSlideNum} / {totalSlides}
                  </span>

                  <button
                    disabled={activeSlideIndex >= totalSlides - 1}
                    onClick={() => setActiveSlideIndex((prev) => Math.min(totalSlides - 1, prev + 1))}
                    className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5 transition-all cursor-pointer shadow-sm"
                  >
                    Sonraki Slayt
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* LIVE RAG AI ASSISTANT FOR THIS SLIDE */}
            <div className="rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-5 sm:p-7 shadow-sm space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-xl bg-indigo-600 text-white flex items-center justify-center font-bold">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900 dark:text-white">
                      Ders Asistanına Sor (Canlı RAG Destekli)
                    </h3>
                    <p className="text-xs text-slate-500">
                      Bu slayt, hocanın ses kaydı ve çıkmış sorular bağlamında anında soru sor.
                    </p>
                  </div>
                </div>
              </div>

              {/* Quick AI Prompts */}
              <div className="flex flex-wrap gap-2">
                {activeSlide.aiPromptSuggestions.map((prompt, prIdx) => (
                  <button
                    key={prIdx}
                    onClick={() => {
                      setAiQuery(prompt);
                      handleAskAi(prompt);
                    }}
                    className="text-xs font-medium px-3 py-1.5 rounded-full bg-slate-100 hover:bg-indigo-50 dark:bg-slate-800 dark:hover:bg-indigo-950/50 hover:text-indigo-600 border border-slate-200 dark:border-slate-700 transition-colors text-slate-700 dark:text-slate-300 cursor-pointer"
                  >
                    💡 {prompt}
                  </button>
                ))}
              </div>

              {/* Prompt Input Form */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleAskAi();
                }}
                className="flex items-center gap-2"
              >
                <input
                  type="text"
                  value={aiQuery}
                  onChange={(e) => setAiQuery(e.target.value)}
                  placeholder="Bu slayttaki konu veya hocanın vurgusu hakkında soru sor..."
                  className="flex-1 px-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 text-slate-900 dark:text-white placeholder:text-slate-400"
                />
                <button
                  type="submit"
                  disabled={aiLoading || !aiQuery.trim()}
                  className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white text-xs sm:text-sm font-bold flex items-center gap-1.5 transition-all cursor-pointer shadow-sm shrink-0"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>{aiLoading ? 'Düşünüyor...' : 'Sor'}</span>
                </button>
              </form>

              {/* AI Response Display */}
              {aiResponse && (
                <div className="p-4 sm:p-5 rounded-2xl bg-indigo-50/70 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-900/60 text-xs sm:text-sm text-slate-800 dark:text-slate-200 leading-relaxed space-y-3 animate-in fade-in duration-200">
                  <div className="flex items-center justify-between pb-2 border-b border-indigo-100 dark:border-indigo-900/50 text-[11px] font-bold text-indigo-700 dark:text-indigo-300">
                    <span className="flex items-center gap-1">
                      <Check className="w-3.5 h-3.5 text-emerald-600" />
                      Yapay Zeka Tıp Yanıtı (RAG Tabanlı Doğrulandı)
                    </span>
                    <button
                      onClick={() => setAiResponse(null)}
                      className="text-slate-400 hover:text-slate-600 cursor-pointer"
                    >
                      Kapat
                    </button>
                  </div>
                  <div className="whitespace-pre-wrap font-sans">{aiResponse}</div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* MODE 2: CONTINUOUS VERTICAL SCROLL MODE */}
        {viewMode === 'continuous' && (
          <div className="space-y-8">
            {activeDeck.slides.map((slide) => (
              <div
                key={slide.slideNumber}
                id={`slide-${slide.slideNumber}`}
                className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-md p-6 sm:p-8 space-y-6"
              >
                {/* Header */}
                <div className="flex items-start justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="w-7 h-7 rounded-lg bg-indigo-600 text-white font-mono font-bold text-xs flex items-center justify-center">
                        {slide.slideNumber}
                      </span>
                      <span className="text-xs font-bold text-amber-600 bg-amber-50 px-2 py-0.5 rounded-md border border-amber-200 uppercase tracking-wide">
                        {slide.badge}
                      </span>
                    </div>
                    <h3 className="text-lg sm:text-xl font-black text-slate-900 dark:text-white">
                      {slide.title}
                    </h3>
                    <p className="text-xs text-slate-500 font-medium">{slide.subtitle}</p>
                  </div>
                </div>

                {/* Professor Voice Quote */}
                {slide.professorAudioHighlight && (
                  <div className="rounded-2xl bg-rose-50/70 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/60 p-4 space-y-2">
                    <div className="flex items-center gap-2 text-rose-800 dark:text-rose-300 text-xs font-bold">
                      <Volume2 className="w-4 h-4 text-rose-600" />
                      <span>Hocanın Amfi Vurgusu [{slide.professorAudioHighlight.timestamp}]</span>
                    </div>
                    <blockquote className="text-xs sm:text-sm font-semibold italic text-slate-800 dark:text-slate-200">
                      "{slide.professorAudioHighlight.quote}"
                    </blockquote>
                    <p className="text-[11px] text-rose-800/80">
                      💡 {slide.professorAudioHighlight.note}
                    </p>
                  </div>
                )}

                {/* Bullets */}
                {slide.coreContent.keyBullets && (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {slide.coreContent.keyBullets.map((b, bIdx) => (
                      <div key={bIdx} className="bg-slate-50 dark:bg-slate-800 p-3 rounded-xl border border-slate-200 text-xs space-y-0.5">
                        <div className="font-bold text-slate-900 dark:text-white">{b.title}</div>
                        <div className="text-slate-600 dark:text-slate-300">{b.desc}</div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Spot Pearls */}
                <div className="bg-amber-50/60 dark:bg-amber-950/20 p-4 rounded-2xl border border-amber-200/80 space-y-2">
                  <div className="text-xs font-bold text-amber-800 uppercase tracking-wide flex items-center gap-1.5">
                    <Zap className="w-3.5 h-3.5 text-amber-600" />
                    Spot Bilgiler
                  </div>
                  <ul className="text-xs text-amber-900 dark:text-amber-200 space-y-1 list-disc list-inside">
                    {slide.spotPearls.map((p, pIdx) => (
                      <li key={pIdx}>{p}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
