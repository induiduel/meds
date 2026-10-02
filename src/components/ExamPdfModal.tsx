import React, { useState, useEffect, useMemo } from 'react';
import { createPortal } from 'react-dom';
import { 
  X, 
  Printer, 
  Download, 
  FileText, 
  CheckCircle2, 
  Columns, 
  Square, 
  Filter,
  Layers,
  Calendar,
  Sparkles,
  BookOpen,
  GraduationCap,
  HardDrive,
  RefreshCw,
  SlidersHorizontal,
  FolderOpen
} from 'lucide-react';
import { Committee, QuestionItem } from '../types';
import { ApiService } from '../services/api';
import { downloadBookletPdfLocally } from '../services/drive';
import { filterCurrent2026_2027Committees } from '../services/firestoreDb';
import { generateSlidePdfBlob, downloadSlidePdf } from '../services/slidePdf';
import type { InteractiveDeck } from './learn/InteractiveDeckView';

/** Primary branch of a deck ("Enfeksiyon Hastalıkları / Klinik Mikrobiyoloji" → "Enfeksiyon Hastalıkları"). */
const disciplineGroup = (raw: string) => (raw || 'Diğer').split(/\s*(?:\/|&|,|\sve\s)\s*/)[0].trim() || 'Diğer';

interface ExamPdfModalProps {
  isOpen: boolean;
  onClose: () => void;
  committee?: Committee;
  committees?: Committee[];
  questions: QuestionItem[];
  /** Open on the Öğren tab with this deck's slide preselected */
  initialSlide?: { deckId: string; slideNumber: number } | null;
}

export interface NormalizedPdfQuestion {
  id: string;
  source: 'past_exams' | 'collaborative';
  committeeId: string;
  questionNumber: number;
  discipline: string;
  topic: string;
  examYear?: string;
  stem: string;
  options: { key: string; text: string; isCorrect?: boolean }[];
  correctAnswer: string;
  explanation: string;
  isReady: boolean;
}

export const ExamPdfModal: React.FC<ExamPdfModalProps> = ({
  isOpen,
  onClose,
  committee,
  committees = [],
  questions = [],
  initialSlide = null,
}) => {
  // What goes into the PDF: past/pool questions or Öğren slides
  const [contentType, setContentType] = useState<'questions' | 'slides'>(initialSlide ? 'slides' : 'questions');
  const [highlightCorrect, setHighlightCorrect] = useState(true);
  // Configurable Selection States
  const [selectedCommitteeId, setSelectedCommitteeId] = useState<string>(() => committee?.id || 'all');
  const [sourceMode, setSourceMode] = useState<'past_exams' | 'collaborative' | 'all'>('past_exams');
  const [selectedYear, setSelectedYear] = useState<string>('all');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('all');
  const [filterReadyOnly, setFilterReadyOnly] = useState(false);
  const [questionLimit, setQuestionLimit] = useState<number>(100);
  const [bookletMode, setBookletMode] = useState<'student' | 'solution' | 'answers_only'>('solution');
  const [columns, setColumns] = useState<'two' | 'one'>('two');
  const [includeAnswerMatrix, setIncludeAnswerMatrix] = useState(true);
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const [pdfError, setPdfError] = useState<string | null>(null);

  // Öğren slides
  const [decks, setDecks] = useState<InteractiveDeck[]>([]);
  const [deckId, setDeckId] = useState<string>(initialSlide?.deckId || '');
  const [pickedSlides, setPickedSlides] = useState<number[]>(initialSlide ? [initialSlide.slideNumber] : []);
  const [includeCards, setIncludeCards] = useState(true);
  const [includeSlideQuestions, setIncludeSlideQuestions] = useState(false);
  const [slidePreviewUrl, setSlidePreviewUrl] = useState<string | null>(null);
  const [isBuildingPreview, setIsBuildingPreview] = useState(false);

  // Past Questions Loading State
  const [pastQuestions, setPastQuestions] = useState<any[]>([]);
  const [isLoadingPast, setIsLoadingPast] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);

  // Sync committee id if external committee prop changes
  useEffect(() => {
    if (committee?.id) {
      setSelectedCommitteeId(committee.id);
    }
  }, [committee?.id]);

  // Load Past Questions dynamically when modal is opened
  useEffect(() => {
    if (!isOpen) return;
    let isMounted = true;

    const fetchPast = async () => {
      setIsLoadingPast(true);
      setLoadError(null);
      try {
        const data = await ApiService.getPastQuestions();
        if (isMounted) {
          const clean = data.filter((q: any) => !q.id?.startsWith('civan-') && !q.tags?.some((t: string) => /civan/i.test(t)));
          setPastQuestions(clean);
        }
      } catch (err: any) {
        if (isMounted) {
          console.warn('PDF Modal past questions could not be loaded:', err);
          setLoadError('Çıkmış sorular yüklenemedi. İmece soru havuzu gösteriliyor.');
        }
      } finally {
        if (isMounted) setIsLoadingPast(false);
      }
    };

    fetchPast();
    return () => {
      isMounted = false;
    };
  }, [isOpen]);

  // Filter committees strictly for 2026-2027 academic year
  const cleanCommittees = useMemo(() => filterCurrent2026_2027Committees(committees), [committees]);

  // Determine current active committee object
  const activeCommittee = useMemo(() => {
    if (selectedCommitteeId === 'all') return undefined;
    return cleanCommittees.find((c) => c.id === selectedCommitteeId) || committee;
  }, [cleanCommittees, selectedCommitteeId, committee]);

  // Build Normalized Questions Pool
  const allNormalized = useMemo<NormalizedPdfQuestion[]>(() => {
    const list: NormalizedPdfQuestion[] = [];

    // 1. Process Past Exam Questions
    if (sourceMode === 'past_exams' || sourceMode === 'all') {
      for (const q of pastQuestions) {
        const rec = q.reconstruction;
        const stem = rec?.stem || q.stem || q.rawQuestion?.stem || (q.fragments?.map((f: any) => f.text).join(' ')) || '';
        if (!stem) continue;

        const rawOpts = rec?.options || q.options || q.rawQuestion?.options || [];
        const correctAns = rec?.correctAnswer || q.correctAnswer || q.claimedAnswer || '';
        const opts = rawOpts.map((o: any) => ({
          key: String(o.key || '').trim().toUpperCase(),
          text: String(o.text || '').trim(),
          isCorrect: String(o.key || '').trim().toUpperCase() === correctAns.toUpperCase() || !!o.isCorrect
        })).filter((o: any) => o.key && o.text);

        const explanation = rec?.explanation || q.explanation || '';
        const isReady = Boolean(rec || correctAns || opts.some((o: any) => o.isCorrect));

        list.push({
          id: String(q.id),
          source: 'past_exams',
          committeeId: q.committeeId || 'donem3-kurul1',
          questionNumber: Number(q.questionNumber) || 0,
          discipline: q.discipline || 'Genel Tıp',
          topic: q.topic || '',
          examYear: q.examYear || '',
          stem,
          options: opts,
          correctAnswer: correctAns,
          explanation,
          isReady
        });
      }
    }

    // 2. Process Collaborative Questions (Real-time student pool)
    if (sourceMode === 'collaborative' || sourceMode === 'all') {
      for (const q of questions) {
        const rec = q.reconstruction;
        const stem = rec?.stem || (q.fragments?.map((f: any) => f.text).join(' ')) || (q as any).stem || '';
        if (!stem) continue;

        const rawOpts = rec?.options || q.options || [];
        const correctAns = rec?.correctAnswer || q.claimedAnswer || '';
        const opts = rawOpts.map((o: any) => ({
          key: String(o.key || '').trim().toUpperCase(),
          text: String(o.text || '').trim(),
          isCorrect: String(o.key || '').trim().toUpperCase() === correctAns.toUpperCase() || !!o.isCorrect
        })).filter((o: any) => o.key && o.text);

        const explanation = rec?.explanation || '';
        const isReady = Boolean(rec || q.status === 'completed');

        // Prevent duplicate if already added by pastQuestions in 'all' mode
        if (sourceMode === 'all' && list.some(existing => existing.id === q.id)) {
          continue;
        }

        list.push({
          id: q.id,
          source: 'collaborative',
          committeeId: q.committeeId,
          questionNumber: q.questionNumber || 0,
          discipline: q.discipline || 'Genel Tıp',
          topic: q.topic || '',
          examYear: q.examYear || 'Güncel Havuz',
          stem,
          options: opts,
          correctAnswer: correctAns,
          explanation,
          isReady
        });
      }
    }

    return list;
  }, [pastQuestions, questions, sourceMode]);

  // Available Years for filter
  const availableYears = useMemo(() => {
    const years = new Set<string>();
    for (const q of allNormalized) {
      if (selectedCommitteeId === 'all' || q.committeeId === selectedCommitteeId) {
        if (q.examYear) years.add(q.examYear);
      }
    }
    return Array.from(years).sort().reverse();
  }, [allNormalized, selectedCommitteeId]);

  // Available Disciplines for filter
  const availableDisciplines = useMemo(() => {
    const disc = new Set<string>();
    for (const q of allNormalized) {
      if (selectedCommitteeId === 'all' || q.committeeId === selectedCommitteeId) {
        if (q.discipline) disc.add(q.discipline);
      }
    }
    return Array.from(disc).sort((a, b) => a.localeCompare(b, 'tr'));
  }, [allNormalized, selectedCommitteeId]);

  // Filtered & Sorted Questions
  const filteredQuestions = useMemo(() => {
    let result = allNormalized.filter((q) => {
      // Committee filter
      if (selectedCommitteeId !== 'all' && q.committeeId !== selectedCommitteeId) {
        return false;
      }
      // Year filter
      if (selectedYear !== 'all' && q.examYear !== selectedYear) {
        return false;
      }
      // Discipline filter
      if (selectedDiscipline !== 'all' && q.discipline !== selectedDiscipline) {
        return false;
      }
      // Ready only filter
      if (filterReadyOnly && !q.isReady) {
        return false;
      }
      return true;
    });

    // Sort by question number (or id)
    result.sort((a, b) => {
      if (a.questionNumber && b.questionNumber) {
        return a.questionNumber - b.questionNumber;
      }
      return a.id.localeCompare(b.id);
    });

    // Apply question count limit if specified
    if (questionLimit > 0 && result.length > questionLimit) {
      result = result.slice(0, questionLimit);
    }

    return result;
  }, [allNormalized, selectedCommitteeId, selectedYear, selectedDiscipline, filterReadyOnly, questionLimit]);

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

  // Load decks only when the slide tab is used (the JSON is large)
  useEffect(() => {
    if (!isOpen || contentType !== 'slides' || decks.length) return;
    let alive = true;
    import('../data/interactive_learning_decks.json').then((mod: any) => {
      if (!alive) return;
      const list = ((mod.default || mod) as InteractiveDeck[]).filter((d) => d && Array.isArray(d.slides) && d.slides.length > 0);
      setDecks(list);
      if (!list.some((d) => d.id === deckId) && list[0]) {
        setDeckId(list[0].id);
        setPickedSlides([list[0].slides[0].slideNumber]);
      }
    });
    return () => {
      alive = false;
    };
  }, [isOpen, contentType, decks.length, deckId]);

  const activeDeck = useMemo(() => decks.find((d) => d.id === deckId) || null, [decks, deckId]);
  const chosenSlides = useMemo(
    () => (activeDeck ? activeDeck.slides.filter((sl) => pickedSlides.includes(sl.slideNumber)) : []),
    [activeDeck, pickedSlides]
  );
  const slideOptions = { includeFlashcards: includeCards, includeQuestions: includeSlideQuestions, highlightCorrect };

  // Live PDF preview for slides (debounced)
  useEffect(() => {
    if (!isOpen || contentType !== 'slides' || !activeDeck || chosenSlides.length === 0) {
      setSlidePreviewUrl(null);
      return;
    }
    let alive = true;
    let url: string | null = null;
    setIsBuildingPreview(true);
    const t = setTimeout(async () => {
      try {
        const blob = await generateSlidePdfBlob(activeDeck, chosenSlides.slice(0, 12), slideOptions);
        if (!alive) return;
        url = URL.createObjectURL(blob);
        setSlidePreviewUrl(url);
      } catch (e) {
        console.warn('Slayt PDF önizlemesi oluşturulamadı', e);
        if (alive) setSlidePreviewUrl(null);
      } finally {
        if (alive) setIsBuildingPreview(false);
      }
    }, 350);
    return () => {
      alive = false;
      clearTimeout(t);
      if (url) URL.revokeObjectURL(url);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen, contentType, activeDeck, chosenSlides, includeCards, includeSlideQuestions, highlightCorrect]);

  if (!isOpen) return null;

  const handleSlidePdfDownload = async () => {
    if (!activeDeck || chosenSlides.length === 0) return;
    setPdfError(null);
    setIsGeneratingPdf(true);
    try {
      await downloadSlidePdf(activeDeck, chosenSlides, slideOptions);
    } catch (err) {
      console.error('Slayt PDF hatası:', err);
      setPdfError('Slayt PDF oluşturulamadı. Lütfen tekrar dene.');
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  // Booklet Header Details
  const displayTitle = activeCommittee?.name || (selectedCommitteeId === 'all' ? 'TÜM KURULLAR BİRLEŞİK SINAV KİTAPÇIĞI' : 'TIP FAKÜLTESİ KURUL SINAVI');
  const displayTerm = activeCommittee?.term || '2025-2026';
  const displayTarget = filteredQuestions.length;
  const examDuration = Math.round(displayTarget * 1.1); // ~1.1 min per question

  const handlePrint = () => {
    window.print();
  };

  const handleDirectPdfDownload = async () => {
    setPdfError(null);
    setIsGeneratingPdf(true);
    try {
      const qItems: QuestionItem[] = filteredQuestions.map((q, idx) => ({
        id: q.id,
        committeeId: q.committeeId || activeCommittee?.id || 'genel',
        questionNumber: q.questionNumber || (idx + 1),
        discipline: q.discipline,
        topic: q.topic,
        examYear: q.examYear,
        status: q.isReady ? 'completed' : 'gathering',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        tags: [],
        fragments: [],
        options: q.options.map((o) => ({ key: o.key as 'A' | 'B' | 'C' | 'D' | 'E', text: o.text, upvotes: 0 })),
        claimedAnswer: (['A', 'B', 'C', 'D', 'E'].includes(q.correctAnswer) ? (q.correctAnswer as 'A' | 'B' | 'C' | 'D' | 'E') : undefined),
        reconstruction: q.correctAnswer
          ? {
              stem: q.stem,
              options: q.options.map((o) => ({ key: o.key as 'A' | 'B' | 'C' | 'D' | 'E', text: o.text, isAiFilled: false })),
              correctAnswer: (['A', 'B', 'C', 'D', 'E'].includes(q.correctAnswer) ? (q.correctAnswer as 'A' | 'B' | 'C' | 'D' | 'E') : 'A'),
              explanation: q.explanation || '',
              confidenceScore: 0,
              notesAndDiscrepancies: '',
              lastUpdated: new Date().toISOString(),
            }
          : undefined,
      }));

      const commObj: Committee = activeCommittee || {
        id: selectedCommitteeId === 'all' ? 'tum-kurullar' : selectedCommitteeId,
        name: displayTitle,
        year: 3,
        term: displayTerm,
        targetCount: filteredQuestions.length,
        description: '',
      };

      const sanitizedName = displayTitle.replace(/[^a-zA-Z0-9_\u00C0-\u017F-]/g, '_').slice(0, 40);
      const customName = `${sanitizedName}_${sourceMode === 'past_exams' ? 'Cikmislar' : 'Kitapcik'}_${displayTarget}Soru.pdf`;
      await downloadBookletPdfLocally(commObj, qItems, customName, {
        mode: bookletMode,
        includeAnswerKey: bookletMode === 'answers_only' || includeAnswerMatrix,
        title: displayTitle,
        subtitle: selectedYear !== 'all' ? selectedYear : undefined,
        columns,
        highlightCorrect,
      });
    } catch (err: any) {
      console.error('PDF oluşturma hatası:', err);
      setPdfError('PDF oluşturulamadı. "Yazdır" ile tarayıcıdan PDF olarak kaydedebilirsin.');
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  const handleDownloadHtml = () => {
    const printableElement = document.getElementById('exam-printable-content');
    if (!printableElement) return;

    const htmlContent = `<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>${displayTitle} - Soru Kitapçığı</title>
  <style>
    @page { size: A4 portrait; margin: 12mm 14mm; }
    *, *:before, *:after { box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; color: #0f172a; margin: 0; padding: 20px; line-height: 1.45; font-size: 11pt; background: #fff; }
    .header { border-bottom: 2px solid #0f172a; padding-bottom: 12px; margin-bottom: 20px; text-align: center; }
    .header h1 { margin: 6px 0; font-size: 16pt; text-transform: uppercase; letter-spacing: 0.5px; }
    .header .meta { font-size: 10pt; color: #475569; margin: 4px 0; }
    .instructions { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px 14px; font-size: 9.5pt; margin-bottom: 22px; }
    .exam-columns-2 { columns: 2; column-gap: 28px; column-rule: 1px solid #e2e8f0; }
    .exam-columns-1 { max-width: 800px; margin: 0 auto; }
    .exam-question-item { break-inside: avoid; page-break-inside: avoid; margin-bottom: 18px; padding-bottom: 14px; border-bottom: 1px solid #e2e8f0; font-size: 10pt; }
    .q-badge { display: inline-block; background: #0f172a; color: #fff; font-family: monospace; font-size: 9pt; padding: 2px 7px; border-radius: 4px; font-weight: bold; }
    .q-meta { font-size: 9pt; color: #0f766e; font-weight: bold; text-transform: uppercase; float: right; }
    .q-stem { margin: 8px 0; font-family: Georgia, serif; font-size: 11pt; line-height: 1.5; text-align: justify; }
    .q-option { margin-bottom: 4px; padding: 3px 6px; display: flex; gap: 8px; font-size: 10pt; border-radius: 4px; }
    .q-option.correct { font-weight: bold; color: #065f46; background: #ecfdf5; border: 1px solid #a7f3d0; }
    .explanation { margin-top: 8px; padding: 8px 12px; background: #f0fdf4; border-left: 3px solid #059669; font-size: 9.5pt; color: #065f46; border-radius: 4px; }
    .answer-key-section { break-before: page; page-break-before: always; margin-top: 30px; padding-top: 20px; border-top: 2px solid #0f172a; text-align: center; }
    .answer-grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 6px; font-size: 9pt; margin-top: 14px; }
    .answer-cell { border: 1px solid #cbd5e1; padding: 5px; border-radius: 4px; background: #f8fafc; text-align: center; }
    .answer-cell .num { font-size: 8pt; color: #64748b; font-family: monospace; display: block; }
    .answer-cell .ans { font-size: 11pt; font-weight: bold; color: #0f766e; display: block; }
    @media print {
      body { padding: 0; }
      .no-print { display: none !important; }
    }
  </style>
</head>
<body>
  ${printableElement.innerHTML}
</body>
</html>`;

    const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${displayTitle.replace(/[^a-zA-Z0-9_\u00C0-\u017F-]/g, '_')}_A4_Kitapcik.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const modeOptions: { id: typeof bookletMode; label: string; hint: string }[] = [
    { id: 'student', label: 'Öğrenci', hint: 'Cevaplar gizli' },
    { id: 'solution', label: 'Çözümlü', hint: 'Cevap ve açıklama' },
    { id: 'answers_only', label: 'Cevap anahtarı', hint: 'Yalnızca tablo' },
  ];
  const showKey = bookletMode === 'answers_only' || includeAnswerMatrix;
  const fieldCls = 'h-10 w-full border border-line-2 rounded-[10px] px-3 text-[14px] text-ink bg-white cursor-pointer min-w-0';
  const labelCls = 'flex flex-col gap-1.5 text-[13px] font-semibold text-ink-2';

  return createPortal(
    <div
      id="exam-pdf-modal-portal"
      className="pdf-modal-backdrop fixed inset-0 z-[80] bg-[rgba(14,26,38,0.45)] flex items-stretch sm:items-center justify-center sm:p-4"
      onMouseDown={(e) => e.target === e.currentTarget && onClose()}
    >
      <style>{`
        @media print {
          html, body { margin: 0 !important; padding: 0 !important; background: #fff !important; color: #000 !important; height: auto !important; overflow: visible !important; }
          body > *:not(#exam-pdf-modal-portal) { display: none !important; }
          .pdf-modal-backdrop, .pdf-modal-card, .pdf-modal-scrollable {
            position: static !important; display: block !important; background: #fff !important; padding: 0 !important; margin: 0 !important;
            width: 100% !important; max-width: 100% !important; height: auto !important; max-height: none !important; overflow: visible !important;
            border: none !important; box-shadow: none !important; border-radius: 0 !important;
          }
          .no-print { display: none !important; }
          #exam-printable-content { box-shadow: none !important; border: none !important; margin: 0 !important; padding: 0 !important; max-width: 100% !important; width: 100% !important; }
          .exam-columns-2 { columns: 2 !important; column-gap: 8mm !important; }
          .exam-question-item { break-inside: avoid !important; page-break-inside: avoid !important; }
          .exam-answer-table { break-before: page !important; page-break-before: always !important; }
          @page { size: A4 portrait; margin: 12mm 14mm; }
        }
      `}</style>

      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="pdf-modal-title"
        className="pdf-modal-card bg-white w-full max-w-[1240px] h-full sm:h-[min(94vh,980px)] sm:rounded-[20px] shadow-[0_24px_80px_rgba(14,26,38,0.28)] overflow-hidden flex flex-col text-ink"
      >
        {/* Header */}
        <header className="no-print shrink-0 flex items-center gap-3 px-4 sm:px-5 py-3 border-b border-line">
          <span className="w-9 h-9 rounded-[10px] bg-accent-soft text-accent flex items-center justify-center shrink-0">
            <FileText className="w-[18px] h-[18px]" />
          </span>
          <div className="min-w-0 flex-1">
            <h2 id="pdf-modal-title" className="m-0 font-display font-bold text-[18px] sm:text-[20px] tracking-[-0.02em] leading-tight">
              PDF oluştur
            </h2>
            <p className="m-0 text-[13px] text-ink-2 truncate" role="status">
              {contentType === 'slides'
                ? activeDeck
                  ? `${chosenSlides.length} slayt · ${activeDeck.title}`
                  : 'Dersler yükleniyor…'
                : isLoadingPast
                  ? 'Çıkmış sorular yükleniyor…'
                  : `${displayTarget} soru · ${displayTitle}`}
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="PDF penceresini kapat"
            className="w-10 h-10 rounded-[10px] flex items-center justify-center text-ink-2 hover:text-ink hover:bg-canvas cursor-pointer shrink-0"
          >
            <X className="w-5 h-5" />
          </button>
        </header>

        <div className="pdf-modal-scrollable flex-1 min-h-0 overflow-y-auto lg:overflow-hidden grid grid-cols-1 lg:grid-cols-[320px_minmax(0,1fr)]">
          {/* Settings */}
          <aside className="no-print lg:overflow-y-auto border-b lg:border-b-0 lg:border-r border-line bg-[#FAFBFC] p-4 sm:p-5 flex flex-col gap-4 min-w-0">
            <div role="radiogroup" aria-label="İçerik" className="grid grid-cols-2 gap-1 bg-white border border-line rounded-[12px] p-1">
              {(
                [
                  ['questions', FileText, 'Çıkmış sorular'],
                  ['slides', GraduationCap, 'Öğren slaytı'],
                ] as const
              ).map(([id, Icon, label]) => (
                <button
                  key={id}
                  type="button"
                  role="radio"
                  aria-checked={contentType === id}
                  onClick={() => setContentType(id)}
                  className={`h-10 rounded-[9px] inline-flex items-center justify-center gap-1.5 text-[13.5px] cursor-pointer ${
                    contentType === id ? 'bg-ink text-white font-semibold' : 'text-ink-2 hover:text-ink'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {label}
                </button>
              ))}
            </div>

            {contentType === 'slides' && (
              <>
                <label className={labelCls}>
                  Ders
                  <select
                    value={deckId}
                    onChange={(e) => {
                      const d = decks.find((x) => x.id === e.target.value);
                      setDeckId(e.target.value);
                      setPickedSlides(d ? [d.slides[0].slideNumber] : []);
                    }}
                    className={fieldCls}
                    disabled={!decks.length}
                  >
                    {!decks.length && <option>Yükleniyor…</option>}
                    {decks.map((d) => (
                      <option key={d.id} value={d.id}>
                        {disciplineGroup(d.discipline)} · {d.title}
                      </option>
                    ))}
                  </select>
                </label>

                {activeDeck && (
                  <div className="flex flex-col gap-1.5 min-h-0">
                    <div className="flex items-center justify-between">
                      <span className="text-[13px] font-semibold text-ink-2">Slaytlar · {pickedSlides.length} seçili</span>
                      <button
                        type="button"
                        onClick={() =>
                          setPickedSlides(
                            pickedSlides.length === activeDeck.slides.length ? [activeDeck.slides[0].slideNumber] : activeDeck.slides.map((sl) => sl.slideNumber)
                          )
                        }
                        className="h-8 px-2 text-[13px] font-semibold text-accent cursor-pointer"
                      >
                        {pickedSlides.length === activeDeck.slides.length ? 'Yalnız ilki' : 'Tümünü seç'}
                      </button>
                    </div>
                    <ul className="list-none m-0 p-1 bg-white border border-line rounded-[12px] max-h-[260px] lg:max-h-[300px] overflow-y-auto flex flex-col">
                      {activeDeck.slides.map((sl) => {
                        const on = pickedSlides.includes(sl.slideNumber);
                        return (
                          <li key={sl.slideNumber}>
                            <label
                              className={`flex items-center gap-2.5 min-h-10 px-2 rounded-[9px] cursor-pointer text-[13.5px] ${
                                on ? 'bg-accent-soft text-ink' : 'text-ink-2 hover:bg-canvas'
                              }`}
                            >
                              <input
                                type="checkbox"
                                checked={on}
                                onChange={() =>
                                  setPickedSlides((prev) =>
                                    on ? prev.filter((x) => x !== sl.slideNumber) : [...prev, sl.slideNumber].sort((a, b) => a - b)
                                  )
                                }
                                className="w-4 h-4 accent-[#1E4FD8] shrink-0"
                              />
                              <span className="font-mono text-[12px] text-ink-3 w-6 shrink-0">{sl.slideNumber}</span>
                              <span className="truncate">{sl.title}</span>
                            </label>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                )}

                <div className="flex flex-col gap-0.5">
                  <label className="flex items-center gap-2.5 min-h-10 text-[14px] text-ink cursor-pointer">
                    <input type="checkbox" checked={includeCards} onChange={(e) => setIncludeCards(e.target.checked)} className="w-4 h-4 accent-[#1E4FD8]" />
                    Akıl kartlarını ekle
                  </label>
                  <label className="flex items-center gap-2.5 min-h-10 text-[14px] text-ink cursor-pointer">
                    <input type="checkbox" checked={includeSlideQuestions} onChange={(e) => setIncludeSlideQuestions(e.target.checked)} className="w-4 h-4 accent-[#1E4FD8]" />
                    Eşleşen çıkmış soruları ekle
                  </label>
                  <label className="flex items-center gap-2.5 min-h-10 text-[14px] text-ink cursor-pointer">
                    <input type="checkbox" checked={highlightCorrect} onChange={(e) => setHighlightCorrect(e.target.checked)} className="w-4 h-4 accent-[#1E4FD8]" />
                    Doğru cevapları yeşil göster
                  </label>
                </div>
              </>
            )}

            {contentType === 'questions' && (
            <>
            <div className="flex flex-col gap-1.5">
              <span className="text-[13px] font-semibold text-ink-2">Kitapçık türü</span>
              <div role="radiogroup" aria-label="Kitapçık türü" className="grid grid-cols-3 gap-1 bg-canvas rounded-[12px] p-1">
                {modeOptions.map((m) => {
                  const on = bookletMode === m.id;
                  return (
                    <button
                      key={m.id}
                      type="button"
                      role="radio"
                      aria-checked={on}
                      onClick={() => {
                        setBookletMode(m.id);
                        if (m.id === 'student') setIncludeAnswerMatrix(false);
                      }}
                      className={`min-h-12 px-1.5 py-1 rounded-[9px] flex flex-col items-center justify-center text-center cursor-pointer ${
                        on ? 'bg-white text-accent shadow-[0_1px_2px_rgba(14,26,38,0.1)]' : 'text-ink-2 hover:text-ink'
                      }`}
                    >
                      <span className={`text-[13px] leading-tight ${on ? 'font-semibold' : 'font-medium'}`}>{m.label}</span>
                      <span className="text-[12px] leading-tight text-ink-3">{m.hint}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="grid grid-cols-2 lg:grid-cols-1 gap-3">
              <label className={labelCls}>
                Kurul
                <select
                  value={selectedCommitteeId}
                  onChange={(e) => {
                    setSelectedCommitteeId(e.target.value);
                    setSelectedYear('all');
                    setSelectedDiscipline('all');
                  }}
                  className={fieldCls}
                >
                  <option value="all">Tüm kurullar</option>
                  {cleanCommittees.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name.replace(/^Dönem 3\s*-\s*/i, '')}
                    </option>
                  ))}
                </select>
              </label>
              <label className={labelCls}>
                Kaynak
                <select value={sourceMode} onChange={(e) => setSourceMode(e.target.value as any)} className={fieldCls}>
                  <option value="past_exams">Çıkmış sorular ({pastQuestions.length})</option>
                  <option value="collaborative">Güncel havuz ({questions.length})</option>
                  <option value="all">İkisi birlikte</option>
                </select>
              </label>
              {availableYears.length > 0 && sourceMode !== 'collaborative' && (
                <label className={labelCls}>
                  Yıl
                  <select value={selectedYear} onChange={(e) => setSelectedYear(e.target.value)} className={fieldCls}>
                    <option value="all">Tüm yıllar</option>
                    {availableYears.map((yr) => (
                      <option key={yr} value={yr}>
                        {yr}
                      </option>
                    ))}
                  </select>
                </label>
              )}
              {availableDisciplines.length > 0 && (
                <label className={labelCls}>
                  Ders
                  <select value={selectedDiscipline} onChange={(e) => setSelectedDiscipline(e.target.value)} className={fieldCls}>
                    <option value="all">Tüm dersler</option>
                    {availableDisciplines.map((d) => (
                      <option key={d} value={d}>
                        {d}
                      </option>
                    ))}
                  </select>
                </label>
              )}
              <label className={labelCls}>
                Soru sayısı
                <select value={questionLimit} onChange={(e) => setQuestionLimit(Number(e.target.value))} className={fieldCls}>
                  <option value={50}>İlk 50</option>
                  <option value={100}>İlk 100</option>
                  <option value={150}>İlk 150</option>
                  <option value={0}>Hepsi</option>
                </select>
              </label>
              <div className="flex flex-col gap-1.5">
                <span className="text-[13px] font-semibold text-ink-2">Sütun</span>
                <div role="radiogroup" aria-label="Sütun" className="grid grid-cols-2 gap-1 bg-canvas rounded-[10px] p-[3px]">
                  {(
                    [
                      ['two', Columns, '2 sütun'],
                      ['one', Square, 'Tek'],
                    ] as const
                  ).map(([id, Icon, label]) => (
                    <button
                      key={id}
                      type="button"
                      role="radio"
                      aria-checked={columns === id}
                      onClick={() => setColumns(id)}
                      className={`h-9 rounded-lg inline-flex items-center justify-center gap-1.5 text-[13px] cursor-pointer ${
                        columns === id ? 'bg-white text-ink font-semibold shadow-[0_1px_2px_rgba(14,26,38,0.08)]' : 'text-ink-2'
                      }`}
                    >
                      <Icon className="w-3.5 h-3.5" />
                      {label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <div className="flex flex-col gap-1">
              <label className={`flex items-center gap-2.5 min-h-10 text-[14px] text-ink cursor-pointer ${bookletMode === 'answers_only' ? 'opacity-50' : ''}`}>
                <input
                  type="checkbox"
                  checked={showKey}
                  disabled={bookletMode === 'answers_only'}
                  onChange={(e) => setIncludeAnswerMatrix(e.target.checked)}
                  className="w-4 h-4 accent-[#1E4FD8]"
                />
                Sona cevap anahtarı ekle
              </label>
              <label className="flex items-center gap-2.5 min-h-10 text-[14px] text-ink cursor-pointer">
                <input type="checkbox" checked={filterReadyOnly} onChange={(e) => setFilterReadyOnly(e.target.checked)} className="w-4 h-4 accent-[#1E4FD8]" />
                Yalnızca cevabı belli sorular
              </label>
              <label className={`flex items-center gap-2.5 min-h-10 text-[14px] text-ink cursor-pointer ${bookletMode !== 'solution' ? 'opacity-50' : ''}`}>
                <input
                  type="checkbox"
                  checked={highlightCorrect}
                  disabled={bookletMode !== 'solution'}
                  onChange={(e) => setHighlightCorrect(e.target.checked)}
                  className="w-4 h-4 accent-[#1E4FD8]"
                />
                Doğru şıkkı yeşil işaretle
              </label>
            </div>
            </>
            )}

            {loadError && <p className="m-0 text-[13px] text-warn bg-warn-soft rounded-lg px-3 py-2">{loadError}</p>}
            {pdfError && (
              <p role="alert" className="m-0 text-[13px] text-bad-text bg-bad-soft rounded-lg px-3 py-2">
                {pdfError}
              </p>
            )}

            {/* Actions (sticky on phones) */}
            <div className="sticky bottom-0 mt-auto -mx-4 sm:-mx-5 -mb-4 sm:-mb-5 px-4 sm:px-5 py-3 bg-[#FAFBFC] border-t border-line flex flex-col gap-2 z-10">
              {contentType === 'slides' ? (
                <button
                  type="button"
                  onClick={handleSlidePdfDownload}
                  disabled={!activeDeck || chosenSlides.length === 0 || isGeneratingPdf}
                  className="h-11 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-[15px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isGeneratingPdf ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
                  {isGeneratingPdf ? 'PDF hazırlanıyor…' : `PDF indir (${chosenSlides.length} slayt)`}
                </button>
              ) : (
              <>
              <button
                type="button"
                onClick={handleDirectPdfDownload}
                disabled={displayTarget === 0 || isGeneratingPdf}
                className="h-11 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-[15px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGeneratingPdf ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
                {isGeneratingPdf ? 'PDF hazırlanıyor…' : `PDF indir (${displayTarget} soru)`}
              </button>
              <div className="grid grid-cols-2 gap-2">
                <button
                  type="button"
                  onClick={handlePrint}
                  disabled={displayTarget === 0}
                  title="Tarayıcının yazdırma penceresinde Hedef: PDF olarak kaydet"
                  className="h-10 rounded-[10px] border border-line-2 bg-white text-ink text-[14px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer hover:border-ink-3 disabled:opacity-50"
                >
                  <Printer className="w-4 h-4" /> Yazdır
                </button>
                <button
                  type="button"
                  onClick={handleDownloadHtml}
                  disabled={displayTarget === 0}
                  title="İnternetsiz açılabilen tek dosya HTML kitapçık"
                  className="h-10 rounded-[10px] border border-line-2 bg-white text-ink text-[14px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer hover:border-ink-3 disabled:opacity-50"
                >
                  <FileText className="w-4 h-4" /> HTML
                </button>
              </div>
              </>
              )}
            </div>
          </aside>

          {/* Slide PDF preview: the real PDF, so what you see is what you get */}
          {contentType === 'slides' && (
            <div className="no-print bg-canvas p-3 sm:p-5 flex flex-col min-w-0 min-h-[420px] lg:min-h-0">
              {slidePreviewUrl ? (
                <iframe
                  key={slidePreviewUrl}
                  title="Slayt PDF önizlemesi"
                  src={`${slidePreviewUrl}#view=FitH&toolbar=0&navpanes=0`}
                  className={`flex-1 w-full rounded-[12px] border border-line bg-white transition-opacity ${isBuildingPreview ? 'opacity-60' : ''}`}
                />
              ) : (
                <div className="flex-1 flex flex-col items-center justify-center gap-2 text-center text-ink-2 bg-white border border-dashed border-line-2 rounded-[12px] p-8">
                  {isBuildingPreview ? <RefreshCw className="w-6 h-6 text-accent animate-spin" /> : <GraduationCap className="w-7 h-7 text-ink-3" />}
                  <p className="m-0 text-[14px]">{isBuildingPreview ? 'Önizleme hazırlanıyor…' : 'Önizleme için bir ders ve en az bir slayt seç.'}</p>
                </div>
              )}
              {chosenSlides.length > 12 && (
                <p className="m-0 mt-2 text-[12.5px] text-ink-3">Önizlemede ilk 12 slayt gösteriliyor; indirilen PDF hepsini içerir.</p>
              )}
            </div>
          )}

          {/* A4 preview */}
          <div className={`bg-canvas lg:overflow-y-auto p-3 sm:p-6 justify-center min-w-0 ${contentType === 'slides' ? 'hidden print:flex' : 'flex'}`}>
            <div
              id="exam-printable-content"
              className="print-container bg-white border border-line rounded-sm shadow-[0_2px_12px_rgba(14,26,38,0.08)] w-full max-w-[210mm] sm:min-h-[297mm] h-fit p-4 sm:p-[14mm] text-[#0f172a]"
            >
              <div className="header border-b-2 border-[#0f172a] pb-3 mb-4">
                <div className="meta text-[12px] font-semibold text-[#475569] uppercase tracking-[0.06em]">MedSoru · Dönem {activeCommittee?.year || 3}</div>
                <h1 className="m-0 mt-1 text-[16px] sm:text-[19px] font-bold uppercase leading-snug">{displayTitle}</h1>
                <div className="meta mt-1 text-[12px] text-[#475569]">
                  {displayTarget} soru
                  {bookletMode !== 'answers_only' && ` · ~${examDuration} dakika`}
                  {selectedYear !== 'all' && ` · ${selectedYear}`}
                  {' · '}
                  {modeOptions.find((m) => m.id === bookletMode)?.label}
                </div>
              </div>

              {filteredQuestions.length === 0 && (
                <div className="text-center py-14 px-4 bg-[#f8fafc] rounded-lg border border-dashed border-[#cbd5e1]">
                  <p className="m-0 font-semibold text-[15px]">Bu seçimde soru yok</p>
                  <p className="m-0 mt-1 text-[13px] text-[#475569]">Kurul, kaynak, yıl ya da ders filtresini değiştir.</p>
                </div>
              )}

              {bookletMode !== 'answers_only' && filteredQuestions.length > 0 && (
                <div className={`exam-columns-${columns === 'two' ? '2' : '1'} ${columns === 'two' ? 'md:columns-2 md:gap-8' : ''}`}>
                  {filteredQuestions.map((q, idx) => {
                    const meta = [q.discipline, q.examYear, q.questionNumber ? `S.${q.questionNumber}` : ''].filter(Boolean).join(' · ');
                    return (
                      <div key={q.id} className="exam-question-item break-inside-avoid mb-3 pb-2.5 border-b border-[#eef1f4]">
                        <div className="q-meta text-[11px] text-[#7a8693] truncate pl-5">{meta}</div>
                        <p className="q-stem m-0 mb-1 text-[13px] leading-[1.5] whitespace-pre-line">
                          <span className="q-badge font-bold text-[#1E4FD8] inline-block w-5">{idx + 1}.</span>
                          {q.stem}
                        </p>
                        <div className="flex flex-col gap-0.5">
                          {q.options.map((opt) => {
                            const isCorrect = bookletMode === 'solution' && highlightCorrect && (q.correctAnswer === opt.key || !!opt.isCorrect);
                            return (
                              <div key={opt.key} className={`q-option${isCorrect ? ' correct' : ''} flex gap-1.5 text-[12.5px] leading-snug pl-5 pr-1 rounded ${isCorrect ? 'font-semibold text-[#065f46] bg-[#ecfdf5]' : ''}`}>
                                <span className="font-semibold shrink-0">{opt.key})</span>
                                <span>{opt.text}</span>
                              </div>
                            );
                          })}
                        </div>
                        {bookletMode === 'solution' && (
                          <div className={`explanation mt-1.5 ml-5 pl-2 py-0.5 border-l-2 text-[11.5px] leading-[1.5] text-[#4a5868] ${highlightCorrect ? 'border-[#059669]' : 'border-[#dce2e8]'}`}>
                            <strong className={highlightCorrect ? 'text-[#065f46]' : 'text-[#0e1a26]'}>Cevap: {q.correctAnswer || 'belirtilmemiş'}</strong>
                            {q.explanation && <span className="block whitespace-pre-line mt-0.5">{q.explanation.replace(/【([^】]+)】\s*:?\s*/g, '\n$1: ').trim()}</span>}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}

              {showKey && filteredQuestions.length > 0 && (
                <div className={`exam-answer-table answer-key-section ${bookletMode === 'answers_only' ? '' : 'mt-6 pt-4 border-t-2 border-[#0f172a]'}`}>
                  <h3 className="m-0 mb-3 text-[14px] font-bold uppercase tracking-[0.04em]">Cevap anahtarı</h3>
                  <div className="answer-grid grid grid-cols-5 sm:grid-cols-10 gap-1 text-center">
                    {filteredQuestions.map((q, idx) => {
                      const ans = q.correctAnswer || '–';
                      return (
                        <div key={q.id + '-' + idx} className="answer-cell border border-[#cbd5e1] rounded py-1">
                          <span className="num block text-[12px] text-[#64748b] font-mono">{idx + 1}</span>
                          <span className={`ans block text-[14px] font-bold ${ans === '–' ? 'text-[#94a3b8]' : 'text-[#1E4FD8]'}`}>{ans}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>,
    document.body
  );
};
