import React, { useState, useEffect, useMemo } from 'react';
import { createPortal } from 'react-dom';
import {
  X,
  Printer,
  Download,
  FileText,
  FileDown,
  FileCode,
  GraduationCap,
  RefreshCw,
  EyeOff,
  BookOpenCheck,
  Grid3x3,
  Check,
  ChevronDown,
} from 'lucide-react';
import { Committee, QuestionItem } from '../types';
import { ApiService } from '../services/api';
import { downloadBookletPdfLocally, generateBookletPdfBlob } from '../services/drive';
import { filterCurrent2026_2027Committees } from '../services/firestoreDb';
import { normalizeDonem3Discipline, isDonem3Question } from '../data/curriculumData';
import { generateSlidePdfBlob, downloadSlidePdf } from '../services/slidePdf';
import type { InteractiveDeck } from './learn/InteractiveDeckView';
import { BlurOverlay, PaperLoader } from './ui/Animations';
import { toast } from './ui/Toast';

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
  // A4 for printing, tablet for reading on screen (remembered per device)
  const [pageFormat, setPageFormat] = useState<'a4' | 'tablet'>(() => {
    try {
      return localStorage.getItem('medsoru_pdf_format') === 'tablet' ? 'tablet' : 'a4';
    } catch {
      return 'a4';
    }
  });
  useEffect(() => {
    try {
      localStorage.setItem('medsoru_pdf_format', pageFormat);
    } catch {}
  }, [pageFormat]);
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
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [pageCount, setPageCount] = useState<number | null>(null);
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
          const clean = data
            .filter((q: any) => !q.id?.startsWith('civan-') && !q.tags?.some((t: string) => /civan/i.test(t)))
            .filter(isDonem3Question)
            .map((q: any) => {
              const norm = normalizeDonem3Discipline(q.discipline);
              return norm ? { ...q, discipline: norm } : q;
            });
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
  const slideOptions = { includeFlashcards: includeCards, includeQuestions: includeSlideQuestions, highlightCorrect, pageFormat };

  // Booklet header details
  const displayTitle = activeCommittee?.name || (selectedCommitteeId === 'all' ? 'Tüm kurullar · birleşik kitapçık' : 'Tıp fakültesi kurul sınavı');
  const displayTerm = activeCommittee?.term || '2025-2026';
  const displayTarget = filteredQuestions.length;
  const examDuration = Math.round(displayTarget * 1.1); // ~1.1 min per question
  const showKey = bookletMode === 'answers_only' || includeAnswerMatrix;

  /** Arguments for the question booklet PDF (shared by preview and download). */
  const buildBooklet = () => {
    const qItems: QuestionItem[] = filteredQuestions.map((q, idx) => ({
      id: q.id,
      committeeId: q.committeeId || activeCommittee?.id || 'genel',
      questionNumber: q.questionNumber || idx + 1,
      discipline: q.discipline,
      topic: q.topic,
      examYear: q.examYear,
      status: q.isReady ? 'completed' : 'gathering',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      tags: [],
      fragments: [],
      options: q.options.map((o) => ({ key: o.key as 'A' | 'B' | 'C' | 'D' | 'E', text: o.text, upvotes: 0 })),
      claimedAnswer: ['A', 'B', 'C', 'D', 'E'].includes(q.correctAnswer) ? (q.correctAnswer as 'A' | 'B' | 'C' | 'D' | 'E') : undefined,
      reconstruction: q.correctAnswer
        ? {
            stem: q.stem,
            options: q.options.map((o) => ({ key: o.key as 'A' | 'B' | 'C' | 'D' | 'E', text: o.text, isAiFilled: false })),
            correctAnswer: ['A', 'B', 'C', 'D', 'E'].includes(q.correctAnswer) ? (q.correctAnswer as 'A' | 'B' | 'C' | 'D' | 'E') : 'A',
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
    const opts = {
      mode: bookletMode,
      includeAnswerKey: showKey,
      title: displayTitle,
      subtitle: selectedYear !== 'all' ? selectedYear : undefined,
      columns,
      highlightCorrect,
      pageFormat,
    };
    return { qItems, commObj, opts };
  };

  // Android/iOS browsers often cannot show a PDF inside an iframe
  const canInlinePdf = typeof navigator === 'undefined' || (navigator as any).pdfViewerEnabled !== false;

  // Live preview of the real PDF (debounced), for both questions and slides
  useEffect(() => {
    const ready = contentType === 'slides' ? !!activeDeck && chosenSlides.length > 0 : displayTarget > 0 && !isLoadingPast;
    if (!isOpen || !canInlinePdf || !ready) {
      setPreviewUrl(null);
      setPageCount(null);
      return;
    }
    let alive = true;
    let url: string | null = null;
    setIsBuildingPreview(true);
    const t = setTimeout(async () => {
      try {
        let blob: Blob;
        if (contentType === 'slides') {
          blob = await generateSlidePdfBlob(activeDeck!, chosenSlides.slice(0, 12), slideOptions);
        } else {
          const { qItems, commObj, opts } = buildBooklet();
          blob = await generateBookletPdfBlob(commObj, qItems.slice(0, PREVIEW_QUESTION_CAP), opts);
        }
        if (!alive) return;
        url = URL.createObjectURL(blob);
        setPreviewUrl(url);
        const raw = await blob.text();
        if (alive) setPageCount((raw.match(/\/Type\s*\/Page[^s]/g) || []).length || null);
      } catch (e) {
        console.warn('PDF önizlemesi oluşturulamadı', e);
        if (alive) setPreviewUrl(null);
      } finally {
        if (alive) setIsBuildingPreview(false);
      }
    }, 450);
    return () => {
      alive = false;
      clearTimeout(t);
      if (url) URL.revokeObjectURL(url);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    isOpen,
    contentType,
    activeDeck,
    chosenSlides,
    includeCards,
    includeSlideQuestions,
    highlightCorrect,
    filteredQuestions,
    bookletMode,
    columns,
    includeAnswerMatrix,
    isLoadingPast,
    pageFormat,
  ]);

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
      toast.error('Slayt PDF oluşturulamadı', 'Lütfen tekrar dene.', { label: 'Tekrar dene', onClick: () => handleSlidePdfDownload() });
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  const handleDirectPdfDownload = async () => {
    setPdfError(null);
    setIsGeneratingPdf(true);
    try {
      const { qItems, commObj, opts } = buildBooklet();
      const sanitizedName = displayTitle.replace(/[^a-zA-Z0-9_À-ſ-]/g, '_').slice(0, 40);
      const customName = `${sanitizedName}_${sourceMode === 'past_exams' ? 'Cikmislar' : 'Kitapcik'}_${displayTarget}Soru${pageFormat === 'tablet' ? '_Tablet' : ''}.pdf`;
      await downloadBookletPdfLocally(commObj, qItems, customName, opts);
    } catch (err: any) {
      console.error('PDF oluşturma hatası:', err);
      setPdfError('PDF oluşturulamadı. "Yazdır" ile tarayıcıdan PDF olarak kaydedebilirsin.');
      toast.error('PDF oluşturulamadı', '"Yazdır" ile tarayıcıdan PDF olarak kaydedebilirsin.', { label: 'Tekrar dene', onClick: () => handleDirectPdfDownload() });
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  const handlePrint = () => window.print();

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
    body { font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif; color: #0e1a26; margin: 0; padding: 20px; line-height: 1.45; font-size: 10.5pt; background: #fff; }
    .header { border-bottom: 1.5px solid #0e1a26; padding-bottom: 10px; margin-bottom: 16px; }
    .header h1 { margin: 4px 0; font-size: 15pt; }
    .meta { font-size: 9pt; color: #5f6b79; }
    .exam-columns-2 { columns: 2; column-gap: 26px; column-rule: 1px solid #eef1f4; }
    .exam-question-item { break-inside: avoid; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #eef1f4; }
    .q-meta { font-size: 8pt; color: #7a8693; padding-left: 18px; }
    .q-num { color: #1e4fd8; font-weight: bold; display: inline-block; width: 18px; }
    .q-stem { margin: 2px 0 4px; }
    .q-option { padding: 1px 4px 1px 18px; border-radius: 4px; }
    .q-option.correct { font-weight: bold; color: #065f46; background: #ecfdf5; }
    .explanation { margin: 6px 0 0 18px; padding-left: 8px; border-left: 2px solid #dce2e8; font-size: 9pt; color: #4a5868; }
    .explanation.green { border-color: #059669; }
    .answer-key-section { break-before: page; margin-top: 20px; }
    .answer-grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 5px; margin-top: 10px; }
    .answer-cell { border-radius: 4px; background: #f6f7f9; text-align: center; padding: 4px; }
    .answer-cell .num { font-size: 7.5pt; color: #7a8693; display: block; }
    .answer-cell .ans { font-size: 11pt; font-weight: bold; color: #1e4fd8; display: block; }
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
    a.download = `${displayTitle.replace(/[^a-zA-Z0-9_À-ſ-]/g, '_')}_A4_Kitapcik.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const modeOptions: { id: typeof bookletMode; label: string; hint: string; icon: React.ElementType }[] = [
    { id: 'student', label: 'Öğrenci', hint: 'Cevaplar gizli', icon: EyeOff },
    { id: 'solution', label: 'Çözümlü', hint: 'Cevap + açıklama', icon: BookOpenCheck },
    { id: 'answers_only', label: 'Anahtar', hint: 'Yalnız cevaplar', icon: Grid3x3 },
  ];
  const isSlides = contentType === 'slides';
  const canDownload = isSlides ? !!activeDeck && chosenSlides.length > 0 : displayTarget > 0;
  const summary = isSlides
    ? activeDeck
      ? `${chosenSlides.length} slayt · ${activeDeck.title}`
      : 'Dersler yükleniyor…'
    : isLoadingPast
      ? 'Sorular yükleniyor…'
      : `${displayTarget} soru · ${modeOptions.find((m) => m.id === bookletMode)?.label} · ${
          pageFormat === 'tablet' ? 'tablet' : columns === 'two' ? '2 sütun' : 'tek sütun'
        }`;
  const previewNote = isSlides
    ? chosenSlides.length > 12
      ? 'Önizlemede ilk 12 slayt var; indirilen PDF hepsini içerir.'
      : null
    : displayTarget > PREVIEW_QUESTION_CAP
      ? `Önizlemede ilk ${PREVIEW_QUESTION_CAP} soru var; indirilen PDF ${displayTarget} sorunun hepsini içerir.`
      : null;

  return createPortal(
    <div
      id="exam-pdf-modal-portal"
      className="ms-overlay pdf-modal-backdrop fixed inset-0 z-[80] bg-[rgba(14,26,38,0.5)] backdrop-blur-[2px] flex items-stretch sm:items-center justify-center sm:p-5"
      onMouseDown={(e) => e.target === e.currentTarget && onClose()}
    >
      <style>{`
        @media print {
          html, body { margin: 0 !important; padding: 0 !important; background: #fff !important; color: #000 !important; height: auto !important; overflow: visible !important; }
          body > *:not(#exam-pdf-modal-portal) { display: none !important; }
          .pdf-modal-backdrop, .pdf-modal-card, .pdf-modal-scrollable {
            position: static !important; display: block !important; background: #fff !important; padding: 0 !important; margin: 0 !important;
            width: 100% !important; max-width: 100% !important; height: auto !important; max-height: none !important; overflow: visible !important;
            border: none !important; box-shadow: none !important; border-radius: 0 !important; backdrop-filter: none !important;
          }
          .no-print { display: none !important; }
          #exam-printable-content { display: block !important; padding: 0 !important; }
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
        aria-busy={isGeneratingPdf}
        className="relative pdf-modal-card bg-white w-full max-w-[1260px] h-full sm:h-[min(92vh,920px)] sm:rounded-[24px] shadow-[0_30px_90px_rgba(14,26,38,0.32)] overflow-hidden grid grid-rows-[auto_minmax(0,1fr)_auto] text-ink"
      >
        {/* ---------- Header ---------- */}
        <header className="no-print flex flex-wrap items-center gap-x-4 gap-y-3 px-4 sm:px-6 py-3.5 border-b border-line">
          <span className="w-10 h-10 rounded-[12px] bg-accent text-white flex items-center justify-center shrink-0 shadow-[0_6px_16px_rgba(30,79,216,0.28)]">
            <FileDown className="w-5 h-5" />
          </span>
          <div className="min-w-0 flex-1 sm:flex-none sm:w-[260px]">
            <h2 id="pdf-modal-title" className="m-0 font-display font-bold text-[19px] tracking-[-0.02em] leading-tight">
              PDF oluştur
            </h2>
            <p className="m-0 text-[13px] text-ink-3 truncate">{pageFormat === 'tablet' ? 'Tablette okumaya hazır' : 'A4, yazdırmaya hazır'}</p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="PDF penceresini kapat"
            className="sm:order-last w-10 h-10 rounded-full flex items-center justify-center text-ink-2 hover:text-ink hover:bg-canvas cursor-pointer shrink-0"
          >
            <X className="w-5 h-5" />
          </button>
          <div className="w-full sm:w-auto sm:flex-1 flex sm:justify-center">
            <div role="radiogroup" aria-label="İçerik" className="w-full sm:w-[340px] grid grid-cols-2 gap-1 bg-canvas rounded-[14px] p-1">
              {(
                [
                  ['questions', FileText, 'Sorular'],
                  ['slides', GraduationCap, 'Öğren slaytı'],
                ] as const
              ).map(([id, Icon, label]) => {
                const on = contentType === id;
                return (
                  <button
                    key={id}
                    type="button"
                    role="radio"
                    aria-checked={on}
                    onClick={() => setContentType(id)}
                    className={`h-10 rounded-[11px] inline-flex items-center justify-center gap-2 text-[14px] cursor-pointer transition-all ${
                      on ? 'bg-white text-ink font-semibold shadow-[0_1px_3px_rgba(14,26,38,0.14)]' : 'text-ink-2 hover:text-ink'
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

        {/* ---------- Body ---------- */}
        <div className="pdf-modal-scrollable min-h-0 overflow-y-auto lg:overflow-hidden grid grid-cols-1 lg:grid-cols-[384px_minmax(0,1fr)]">
          {/* Settings */}
          <aside className="no-print lg:overflow-y-auto bg-[#FAFBFC] lg:border-r border-line px-4 sm:px-6 py-5 flex flex-col gap-6 min-w-0">
            {isSlides ? (
              <>
                <Section title="Ders">
                  <SelectField
                    label="Ders"
                    value={deckId}
                    disabled={!decks.length}
                    onChange={(v) => {
                      const d = decks.find((x) => x.id === v);
                      setDeckId(v);
                      setPickedSlides(d ? [d.slides[0].slideNumber] : []);
                    }}
                  >
                    {!decks.length && <option>Yükleniyor…</option>}
                    {decks.map((d) => (
                      <option key={d.id} value={d.id}>
                        {disciplineGroup(d.discipline)} · {d.title}
                      </option>
                    ))}
                  </SelectField>
                </Section>

                {activeDeck && (
                  <Section
                    title={`Slaytlar · ${pickedSlides.length}/${activeDeck.slides.length}`}
                    aside={
                      <button
                        type="button"
                        onClick={() =>
                          setPickedSlides(
                            pickedSlides.length === activeDeck.slides.length ? [activeDeck.slides[0].slideNumber] : activeDeck.slides.map((sl) => sl.slideNumber)
                          )
                        }
                        className="text-[13px] font-semibold text-accent cursor-pointer"
                      >
                        {pickedSlides.length === activeDeck.slides.length ? 'Seçimi sıfırla' : 'Tümünü seç'}
                      </button>
                    }
                  >
                    <ul className="list-none m-0 p-1.5 bg-white border border-line rounded-[16px] max-h-[300px] overflow-y-auto flex flex-col gap-0.5">
                      {activeDeck.slides.map((sl) => {
                        const on = pickedSlides.includes(sl.slideNumber);
                        return (
                          <li key={sl.slideNumber}>
                            <button
                              type="button"
                              role="checkbox"
                              aria-checked={on}
                              onClick={() =>
                                setPickedSlides((prev) =>
                                  on ? prev.filter((x) => x !== sl.slideNumber) : [...prev, sl.slideNumber].sort((a, b) => a - b)
                                )
                              }
                              className={`w-full flex items-center gap-3 min-h-11 px-2.5 rounded-[11px] text-left cursor-pointer transition-colors ${
                                on ? 'bg-accent-soft' : 'hover:bg-canvas'
                              }`}
                            >
                              <span
                                className={`w-5 h-5 rounded-[6px] flex items-center justify-center shrink-0 transition-colors ${
                                  on ? 'bg-accent text-white' : 'bg-white border border-line-2'
                                }`}
                              >
                                {on && <Check className="w-3.5 h-3.5" strokeWidth={3} />}
                              </span>
                              <span className={`font-mono text-[12px] w-5 shrink-0 ${on ? 'text-accent' : 'text-ink-3'}`}>{sl.slideNumber}</span>
                              <span className={`text-[14px] truncate ${on ? 'text-ink font-medium' : 'text-ink-2'}`}>{sl.title}</span>
                            </button>
                          </li>
                        );
                      })}
                    </ul>
                  </Section>
                )}

                <Section title="Sayfa boyutu">
                  <FormatPicker value={pageFormat} onChange={setPageFormat} landscape />
                </Section>

                <Section title="İçerik">
                  <SwitchGroup>
                    <SwitchRow label="Akıl kartları" hint="Soru → cevap kartları slaytın altında" checked={includeCards} onChange={setIncludeCards} />
                    <SwitchRow label="Eşleşen çıkmış sorular" hint="Ayrı sayfada, iki sütun" checked={includeSlideQuestions} onChange={setIncludeSlideQuestions} />
                    <SwitchRow label="Doğru cevaplar yeşil" hint="Kapalıyken yalnızca harf yazılır" checked={highlightCorrect} onChange={setHighlightCorrect} />
                  </SwitchGroup>
                </Section>
              </>
            ) : (
              <>
                <Section title="Kitapçık türü">
                  <div role="radiogroup" aria-label="Kitapçık türü" className="grid grid-cols-3 gap-2">
                    {modeOptions.map((m) => {
                      const on = bookletMode === m.id;
                      const Icon = m.icon;
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
                          className={`min-h-[92px] px-2 py-3 rounded-[16px] border flex flex-col items-center justify-center gap-1.5 text-center cursor-pointer transition-all ${
                            on
                              ? 'border-accent bg-accent-soft/60 shadow-[0_0_0_3px_rgba(30,79,216,0.12)]'
                              : 'border-line bg-white hover:border-line-2'
                          }`}
                        >
                          <span className={`w-9 h-9 rounded-[11px] flex items-center justify-center ${on ? 'bg-accent text-white' : 'bg-canvas text-ink-2'}`}>
                            <Icon className="w-[18px] h-[18px]" />
                          </span>
                          <span className={`text-[13.5px] leading-tight ${on ? 'font-semibold text-ink' : 'font-medium text-ink'}`}>{m.label}</span>
                          <span className="text-[12px] leading-tight text-ink-3">{m.hint}</span>
                        </button>
                      );
                    })}
                  </div>
                </Section>

                <Section title="Sorular">
                  <Segmented
                    label="Kaynak"
                    value={sourceMode}
                    onChange={(v) => setSourceMode(v)}
                    options={[
                      ['past_exams', 'Çıkmış'],
                      ['collaborative', 'Havuz'],
                      ['all', 'İkisi'],
                    ]}
                  />
                  <SelectField
                    label="Kurul"
                    value={selectedCommitteeId}
                    onChange={(v) => {
                      setSelectedCommitteeId(v);
                      setSelectedYear('all');
                      setSelectedDiscipline('all');
                    }}
                  >
                    <option value="all">Tüm kurullar</option>
                    {cleanCommittees.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name.replace(/^Dönem 3\s*-\s*/i, '')}
                      </option>
                    ))}
                  </SelectField>
                  <div className="grid grid-cols-2 gap-2">
                    <SelectField label="Yıl" value={selectedYear} onChange={setSelectedYear} disabled={sourceMode === 'collaborative' || availableYears.length === 0}>
                      <option value="all">Tüm yıllar</option>
                      {availableYears.map((yr) => (
                        <option key={yr} value={yr}>
                          {yr}
                        </option>
                      ))}
                    </SelectField>
                    <SelectField label="Ders" value={selectedDiscipline} onChange={setSelectedDiscipline} disabled={availableDisciplines.length === 0}>
                      <option value="all">Tüm dersler</option>
                      {availableDisciplines.map((d) => (
                        <option key={d} value={d}>
                          {d}
                        </option>
                      ))}
                    </SelectField>
                  </div>
                  <Segmented
                    label="Soru sayısı"
                    value={String(questionLimit)}
                    onChange={(v) => setQuestionLimit(Number(v))}
                    options={[
                      ['50', '50'],
                      ['100', '100'],
                      ['150', '150'],
                      ['0', 'Hepsi'],
                    ]}
                  />
                </Section>

                <Section title="Sayfa">
                  <FormatPicker value={pageFormat} onChange={setPageFormat} />
                  {pageFormat === 'a4' && (
                  <div role="radiogroup" aria-label="Sütun" className="grid grid-cols-2 gap-2">
                    {(
                      [
                        ['two', '2 sütun', 'Kompakt'],
                        ['one', 'Tek sütun', 'Geniş satırlar'],
                      ] as const
                    ).map(([id, label, hint]) => {
                      const on = columns === id;
                      return (
                        <button
                          key={id}
                          type="button"
                          role="radio"
                          aria-checked={on}
                          onClick={() => setColumns(id)}
                          className={`flex items-center gap-3 px-3 py-2.5 rounded-[14px] border text-left cursor-pointer transition-all ${
                            on ? 'border-accent bg-accent-soft/60 shadow-[0_0_0_3px_rgba(30,79,216,0.12)]' : 'border-line bg-white hover:border-line-2'
                          }`}
                        >
                          <PageGlyph cols={id === 'two' ? 2 : 1} on={on} />
                          <span className="min-w-0">
                            <span className={`block text-[13.5px] ${on ? 'font-semibold' : 'font-medium'} text-ink`}>{label}</span>
                            <span className="block text-[12px] text-ink-3">{hint}</span>
                          </span>
                        </button>
                      );
                    })}
                  </div>
                  )}
                  <SwitchGroup>
                    <SwitchRow
                      label="Cevap anahtarı"
                      hint="Son sayfada tablo olarak"
                      checked={showKey}
                      disabled={bookletMode === 'answers_only'}
                      onChange={setIncludeAnswerMatrix}
                    />
                    <SwitchRow
                      label="Doğru şık yeşil"
                      hint={bookletMode === 'solution' ? 'Kapalıyken yalnızca “Cevap: X” yazar' : 'Yalnızca çözümlü kitapçıkta'}
                      checked={highlightCorrect && bookletMode === 'solution'}
                      disabled={bookletMode !== 'solution'}
                      onChange={setHighlightCorrect}
                    />
                    <SwitchRow label="Yalnızca cevabı belli olanlar" checked={filterReadyOnly} onChange={setFilterReadyOnly} />
                  </SwitchGroup>
                </Section>

                {loadError && <p className="m-0 text-[13px] text-warn bg-warn-soft rounded-[12px] px-3 py-2.5">{loadError}</p>}
              </>
            )}
          </aside>

          {/* Preview */}
          <section aria-label="Önizleme" className="no-print bg-[#EDF0F3] flex flex-col min-w-0 min-h-[62vh] lg:min-h-0 p-3 sm:p-5 gap-3">
            <div className="flex items-center gap-2 px-1">
              <span className="text-[12px] font-semibold uppercase tracking-[0.08em] text-ink-3">Önizleme</span>
              {pageCount && !isBuildingPreview && (
                <span className="h-6 px-2 rounded-full bg-white text-[12px] text-ink-2 font-medium inline-flex items-center">
                  {previewNote ? `Önizleme ${pageCount} sayfa` : `${pageCount} sayfa`} ·{' '}
                  {pageFormat === 'tablet' ? (isSlides ? 'Tablet 4:3 yatay' : 'Tablet 3:4 dikey') : isSlides ? 'A4 yatay' : 'A4 dikey'}
                </span>
              )}
              {isBuildingPreview && (
                <span className="h-6 px-2 rounded-full bg-white text-[12px] text-accent font-medium inline-flex items-center gap-1.5">
                  <RefreshCw className="w-3 h-3 animate-spin" />
                  Güncelleniyor
                </span>
              )}
            </div>

            <div className="relative flex-1 min-h-[420px] rounded-[16px] overflow-hidden bg-white shadow-[0_12px_32px_rgba(14,26,38,0.12)] ring-1 ring-[rgba(14,26,38,0.06)]">
              {previewUrl ? (
                <iframe
                  key={previewUrl}
                  title="PDF önizlemesi"
                  src={`${previewUrl}#view=FitH&toolbar=0&navpanes=0`}
                  className="absolute inset-0 w-full h-full border-0"
                />
              ) : null}
              {previewUrl && <BlurOverlay show={isBuildingPreview} icon={<PaperLoader size={72} />} label="Önizleme güncelleniyor…" />}
              {!previewUrl && (
                <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 text-center px-8 ms-fade-in">
                  {isBuildingPreview || (isLoadingPast && !isSlides) ? (
                    <>
                      <PaperLoader />
                      <p className="m-0 text-[15px] font-semibold text-ink">Sayfalar diziliyor…</p>
                      <p className="m-0 text-[13px] text-ink-3">Önizleme birazdan burada</p>
                    </>
                  ) : !canInlinePdf ? (
                    <>
                      <span className="w-14 h-14 rounded-[16px] bg-accent-soft text-accent flex items-center justify-center">
                        <FileDown className="w-7 h-7" />
                      </span>
                      <p className="m-0 text-[16px] font-semibold text-ink">{summary}</p>
                      <p className="m-0 text-[14px] text-ink-2 max-w-[320px]">Bu tarayıcı PDF'i sayfa içinde gösteremiyor. İndirdikten sonra PDF görüntüleyicide açılır.</p>
                    </>
                  ) : (
                    <>
                      <span className="w-14 h-14 rounded-[16px] bg-canvas text-ink-3 flex items-center justify-center">
                        {isSlides ? <GraduationCap className="w-7 h-7" /> : <FileText className="w-7 h-7" />}
                      </span>
                      <p className="m-0 text-[16px] font-semibold text-ink">{isSlides ? 'Slayt seç' : 'Bu seçimde soru yok'}</p>
                      <p className="m-0 text-[14px] text-ink-2 max-w-[320px]">
                        {isSlides ? 'Soldan bir ders ve en az bir slayt seçince önizleme burada görünür.' : 'Kurul, kaynak, yıl ya da ders seçimini değiştir.'}
                      </p>
                    </>
                  )}
                </div>
              )}
            </div>
            {previewNote && <p className="m-0 px-1 text-[12.5px] text-ink-3">{previewNote}</p>}
          </section>

          {/* Print-only HTML booklet (used by "Yazdır" and the HTML download) */}
          {!isSlides && (
            <div id="exam-printable-content" className="hidden print:block text-[#0e1a26]">
              <div className="header">
                <div className="meta">MedSoru · Dönem {activeCommittee?.year || 3}</div>
                <h1>{displayTitle}</h1>
                <div className="meta">
                  {displayTarget} soru
                  {bookletMode !== 'answers_only' && ` · ~${examDuration} dakika`}
                  {selectedYear !== 'all' && ` · ${selectedYear}`} · {modeOptions.find((m) => m.id === bookletMode)?.label}
                </div>
              </div>
              {bookletMode !== 'answers_only' && (
                <div className={columns === 'two' ? 'exam-columns-2' : 'exam-columns-1'}>
                  {filteredQuestions.map((q, idx) => {
                    const meta = [q.discipline, q.examYear].filter(Boolean).join(' · ');
                    return (
                      <div key={q.id} className="exam-question-item">
                        {meta && <div className="q-meta">{meta}</div>}
                        <p className="q-stem">
                          <span className="q-num">{idx + 1}.</span>
                          {q.stem}
                        </p>
                        {q.options.map((opt) => {
                          const isCorrect = bookletMode === 'solution' && highlightCorrect && (q.correctAnswer === opt.key || !!opt.isCorrect);
                          return (
                            <div key={opt.key} className={`q-option${isCorrect ? ' correct' : ''}`}>
                              <strong>{opt.key})</strong> {opt.text}
                            </div>
                          );
                        })}
                        {bookletMode === 'solution' && (
                          <div className={`explanation${highlightCorrect ? ' green' : ''}`}>
                            <strong>Cevap: {q.correctAnswer || 'belirtilmemiş'}</strong>
                            {q.explanation && <span style={{ display: 'block', whiteSpace: 'pre-line' }}>{q.explanation.replace(/【([^】]+)】\s*:?\s*/g, '\n$1: ').trim()}</span>}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
              {showKey && filteredQuestions.length > 0 && (
                <div className="exam-answer-table answer-key-section">
                  <h3>Cevap anahtarı</h3>
                  <div className="answer-grid">
                    {filteredQuestions.map((q, idx) => (
                      <div key={q.id + '-' + idx} className="answer-cell">
                        <span className="num">{idx + 1}</span>
                        <span className="ans">{q.correctAnswer || '–'}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        <BlurOverlay show={isGeneratingPdf} fixed={false} icon={<PaperLoader size={96} />} label="PDF hazırlanıyor…" hint="Birkaç saniye sürebilir" />

        {/* ---------- Footer: summary + actions, always visible ---------- */}
        <footer className="no-print border-t border-line bg-white px-4 sm:px-6 py-3 pb-[max(env(safe-area-inset-bottom),12px)] sm:pb-3 flex flex-wrap sm:flex-nowrap items-center gap-x-3 gap-y-2">
          <div className="min-w-0 flex-1 basis-full sm:basis-auto">
            {pdfError ? (
              <p role="alert" className="m-0 text-[13.5px] text-bad-text font-medium truncate">
                {pdfError}
              </p>
            ) : (
              <p className="m-0 text-[14px] text-ink-2 truncate" role="status">
                <span className="font-semibold text-ink">{summary}</span>
              </p>
            )}
          </div>
          {!isSlides && (
            <>
              <button
                type="button"
                onClick={handlePrint}
                disabled={!canDownload}
                title="Tarayıcının yazdırma penceresini açar"
                className="h-11 px-3.5 rounded-[12px] border border-line bg-white text-ink text-[14px] font-semibold inline-flex items-center gap-2 cursor-pointer hover:border-line-2 disabled:opacity-50"
              >
                <Printer className="w-4 h-4" />
                <span className="hidden sm:inline">Yazdır</span>
              </button>
              <button
                type="button"
                onClick={handleDownloadHtml}
                disabled={!canDownload}
                title="İnternetsiz açılabilen tek dosya HTML kitapçık"
                className="h-11 px-3.5 rounded-[12px] border border-line bg-white text-ink text-[14px] font-semibold inline-flex items-center gap-2 cursor-pointer hover:border-line-2 disabled:opacity-50"
              >
                <FileCode className="w-4 h-4" />
                <span className="hidden sm:inline">HTML</span>
              </button>
            </>
          )}
          <button
            type="button"
            onClick={isSlides ? handleSlidePdfDownload : handleDirectPdfDownload}
            disabled={!canDownload || isGeneratingPdf}
            className="flex-1 sm:flex-none h-11 px-6 rounded-[12px] bg-accent hover:bg-accent-hover text-white text-[15px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_6px_16px_rgba(30,79,216,0.25)]"
          >
            {isGeneratingPdf ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
            {isGeneratingPdf ? 'Hazırlanıyor…' : 'PDF indir'}
          </button>
        </footer>
      </div>
    </div>,
    document.body
  );
};

// ---------------------------------------------------------------------------
// Small building blocks (module level so inputs keep focus across renders)
// ---------------------------------------------------------------------------
const PREVIEW_QUESTION_CAP = 60;

const Section: React.FC<{ title: string; aside?: React.ReactNode; children: React.ReactNode }> = ({ title, aside, children }) => (
  <section className="flex flex-col gap-2.5">
    <div className="flex items-baseline justify-between gap-2 px-0.5">
      <h3 className="m-0 text-[12px] font-semibold uppercase tracking-[0.08em] text-ink-3">{title}</h3>
      {aside}
    </div>
    {children}
  </section>
);

const SelectField: React.FC<{
  label: string;
  value: string;
  onChange: (v: string) => void;
  disabled?: boolean;
  children: React.ReactNode;
}> = ({ label, value, onChange, disabled, children }) => (
  <label className={`relative flex flex-col min-w-0 ${disabled ? 'opacity-50' : ''}`}>
    <span className="sr-only">{label}</span>
    <span className="pointer-events-none absolute left-3.5 top-2 text-[11px] font-semibold text-ink-3">{label}</span>
    <select
      value={value}
      disabled={disabled}
      onChange={(e) => onChange(e.target.value)}
      className="appearance-none w-full h-[54px] pt-4 pl-3.5 pr-9 rounded-[14px] border border-line bg-white text-[14.5px] text-ink cursor-pointer outline-0 focus:border-accent focus:shadow-[0_0_0_3px_rgba(30,79,216,0.12)] truncate disabled:cursor-not-allowed"
    >
      {children}
    </select>
    <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-3" />
  </label>
);

function Segmented<T extends string>({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: T;
  onChange: (v: T) => void;
  options: [T, string][];
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <span className="px-0.5 text-[12.5px] font-medium text-ink-2">{label}</span>
      <div role="radiogroup" aria-label={label} className="grid gap-1 bg-[#EEF1F4] rounded-[12px] p-1" style={{ gridTemplateColumns: `repeat(${options.length}, minmax(0, 1fr))` }}>
        {options.map(([id, text]) => {
          const on = value === id;
          return (
            <button
              key={id}
              type="button"
              role="radio"
              aria-checked={on}
              onClick={() => onChange(id)}
              className={`h-9 rounded-[9px] text-[13.5px] cursor-pointer transition-all ${
                on ? 'bg-white text-ink font-semibold shadow-[0_1px_3px_rgba(14,26,38,0.14)]' : 'text-ink-2 hover:text-ink'
              }`}
            >
              {text}
            </button>
          );
        })}
      </div>
    </div>
  );
}

const SwitchGroup: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="bg-white border border-line rounded-[16px] divide-y divide-line-soft overflow-hidden">{children}</div>
);

const SwitchRow: React.FC<{
  label: string;
  hint?: string;
  checked: boolean;
  onChange: (v: boolean) => void;
  disabled?: boolean;
}> = ({ label, hint, checked, onChange, disabled }) => (
  <button
    type="button"
    role="switch"
    aria-checked={checked}
    disabled={disabled}
    onClick={() => onChange(!checked)}
    className="w-full flex items-center gap-3 min-h-[56px] px-4 py-2 text-left cursor-pointer disabled:cursor-not-allowed disabled:opacity-50 hover:bg-[#FAFBFC]"
  >
    <span className="flex-1 min-w-0">
      <span className="block text-[14px] font-medium text-ink">{label}</span>
      {hint && <span className="block text-[12.5px] text-ink-3 leading-snug">{hint}</span>}
    </span>
    <span className={`relative w-[42px] h-[26px] rounded-full shrink-0 transition-colors ${checked ? 'bg-accent' : 'bg-line-2'}`} aria-hidden="true">
      <span
        className={`absolute top-[3px] left-[3px] w-5 h-5 rounded-full bg-white shadow-[0_1px_3px_rgba(14,26,38,0.25)] transition-transform ${
          checked ? 'translate-x-4' : ''
        }`}
      />
    </span>
  </button>
);

/** A4 (print) vs tablet (screen) page shape picker. */
const FormatPicker: React.FC<{ value: 'a4' | 'tablet'; onChange: (v: 'a4' | 'tablet') => void; landscape?: boolean }> = ({
  value,
  onChange,
  landscape = false,
}) => (
  <div role="radiogroup" aria-label="Sayfa boyutu" className="grid grid-cols-2 gap-2">
    {(
      [
        ['a4', 'A4', 'Yazdırmak için', landscape ? [30, 21] : [21, 30]],
        ['tablet', 'Tablet', landscape ? 'Ekranı doldurur · 4:3' : 'Ekranı doldurur · 3:4', landscape ? [28, 21] : [21, 28]],
      ] as const
    ).map(([id, label, hint, [w, h]]) => {
      const on = value === id;
      return (
        <button
          key={id}
          type="button"
          role="radio"
          aria-checked={on}
          onClick={() => onChange(id)}
          className={`flex items-center gap-3 px-3 py-2.5 rounded-[14px] border text-left cursor-pointer transition-all ${
            on ? 'border-accent bg-accent-soft/60 shadow-[0_0_0_3px_rgba(30,79,216,0.12)]' : 'border-line bg-white hover:border-line-2'
          }`}
        >
          <span className="w-8 h-10 flex items-center justify-center shrink-0" aria-hidden="true">
            <span
              className={`rounded-[4px] border-[1.5px] ${on ? 'border-accent bg-white' : 'border-line-2 bg-white'} ${id === 'tablet' ? 'rounded-[6px]' : ''}`}
              style={{ width: w, height: h }}
            />
          </span>
          <span className="min-w-0">
            <span className={`block text-[13.5px] ${on ? 'font-semibold' : 'font-medium'} text-ink`}>{label}</span>
            <span className="block text-[12px] text-ink-3 leading-snug">{hint}</span>
          </span>
        </button>
      );
    })}
  </div>
);

/** Tiny page icon showing one or two text columns. */
const PageGlyph: React.FC<{ cols: 1 | 2; on: boolean }> = ({ cols, on }) => (
  <span
    className={`w-8 h-10 rounded-[5px] border flex gap-[3px] p-[5px] shrink-0 ${on ? 'border-accent bg-white' : 'border-line-2 bg-white'}`}
    aria-hidden="true"
  >
    {Array.from({ length: cols }).map((_, i) => (
      <span key={i} className="flex-1 flex flex-col gap-[3px]">
        {[0, 1, 2, 3, 4].map((j) => (
          <span key={j} className={`h-[2px] rounded-full ${on ? 'bg-accent/60' : 'bg-line-2'}`} style={{ width: j === 4 ? '60%' : '100%' }} />
        ))}
      </span>
    ))}
  </span>
);
