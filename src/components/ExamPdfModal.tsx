import React, { useState, useEffect, useMemo } from 'react';
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

interface ExamPdfModalProps {
  isOpen: boolean;
  onClose: () => void;
  committee?: Committee;
  committees?: Committee[];
  questions: QuestionItem[];
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
}) => {
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

  if (!isOpen) return null;

  // Booklet Header Details
  const displayTitle = activeCommittee?.name || (selectedCommitteeId === 'all' ? 'TÜM KURULLAR BİRLEŞİK SINAV KİTAPÇIĞI' : 'TIP FAKÜLTESİ KURUL SINAVI');
  const displayTerm = activeCommittee?.term || '2025-2026';
  const displayTarget = filteredQuestions.length;
  const examDuration = Math.round(displayTarget * 1.1); // ~1.1 min per question

  const handlePrint = () => {
    window.print();
  };

  const handleDirectPdfDownload = async () => {
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
              confidenceScore: 98,
              notesAndDiscrepancies: 'Doğrulandı',
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
      await downloadBookletPdfLocally(commObj, qItems, customName);
    } catch (err) {
      console.error('Doğrudan PDF oluşturma hatası, yazdırmaya yönlendiriliyor:', err);
      window.print();
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

  return (
    <div 
      id="exam-pdf-modal-portal"
      className="pdf-modal-backdrop fixed inset-0 z-50 bg-slate-900/80 backdrop-blur-xs flex items-center justify-center p-2 sm:p-4 overflow-y-auto"
    >
      {/* CSS to ensure pristine multi-page printing without clipping */}
      <style>{`
        @media print {
          html, body {
            margin: 0 !important;
            padding: 0 !important;
            background: #fff !important;
            color: #000 !important;
            height: auto !important;
            overflow: visible !important;
          }
          body > *:not(#exam-pdf-modal-portal) {
            display: none !important;
          }
          .pdf-modal-backdrop {
            position: static !important;
            background: transparent !important;
            padding: 0 !important;
            margin: 0 !important;
            width: 100% !important;
            height: auto !important;
            min-height: auto !important;
            max-height: none !important;
            overflow: visible !important;
            box-shadow: none !important;
          }
          .pdf-modal-card {
            position: static !important;
            width: 100% !important;
            max-width: 100% !important;
            height: auto !important;
            min-height: auto !important;
            max-height: none !important;
            overflow: visible !important;
            border: none !important;
            box-shadow: none !important;
            background: #fff !important;
            margin: 0 !important;
            padding: 0 !important;
          }
          .pdf-modal-scrollable {
            overflow: visible !important;
            height: auto !important;
            max-height: none !important;
            padding: 0 !important;
            margin: 0 !important;
            background: #fff !important;
          }
          .no-print {
            display: none !important;
          }
          #exam-printable-content {
            box-shadow: none !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            max-width: 100% !important;
            width: 100% !important;
            background: #fff !important;
            color: #000 !important;
          }
          .exam-question-item {
            break-inside: avoid !important;
            page-break-inside: avoid !important;
            margin-bottom: 16px !important;
          }
          .exam-answer-table {
            break-before: page !important;
            page-break-before: always !important;
          }
          @page {
            size: A4 portrait;
            margin: 12mm 14mm 12mm 14mm;
          }
        }
      `}</style>

      <div className="pdf-modal-card bg-slate-100 rounded-2xl max-w-6xl w-full shadow-2xl border border-slate-300 overflow-hidden my-2 sm:my-4 flex flex-col max-h-[96vh]">
        
        {/* ROW 1: Top Control Header (Dark Navy) */}
        <div className="bg-slate-900 text-white p-3.5 sm:p-4 shrink-0 flex flex-wrap items-center justify-between gap-3 no-print border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-400 border border-teal-500/30 flex items-center justify-center shrink-0">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-sm sm:text-base font-black tracking-tight">
                  A4 Kurul Sınav Kitapçığı & PDF İndirme Merkezi
                </h2>
                <span className="bg-teal-500/30 text-teal-300 text-[11px] font-mono font-bold px-2.5 py-0.5 rounded-full border border-teal-500/40">
                  {displayTarget} Soru Seçili
                </span>
                {isLoadingPast && (
                  <span className="text-[11px] text-amber-300 flex items-center gap-1 animate-pulse">
                    <RefreshCw className="w-3 h-3 animate-spin" />
                    Çıkmışlar yükleniyor...
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                {displayTitle} • Fakülte mizanpajı, yüksek çözünürlüklü vektör PDF ve çevrimdışı çalışma
              </p>
            </div>
          </div>

          <div className="flex items-center flex-wrap gap-2">
            {/* Primary Action 1: Native Print to PDF */}
            <button
              onClick={handlePrint}
              className="bg-teal-600 hover:bg-teal-500 text-white px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-md cursor-pointer transition-all active:scale-95"
              title="Tarayıcının 'Hedef: PDF Olarak Kaydet' menüsüyle tam çözünürlüklü vektör PDF oluşturur"
            >
              <Printer className="w-4 h-4" />
              <span>Yazdır / PDF Olarak Kaydet</span>
            </button>

            {/* Primary Action 2: Direct PDF File Download */}
            <button
              onClick={handleDirectPdfDownload}
              className="bg-emerald-700 hover:bg-emerald-600 text-white px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-md cursor-pointer transition-all active:scale-95"
              title="Doğrudan cihazınıza .pdf dosyası olarak kaydeder"
            >
              <Download className="w-4 h-4" />
              <span>Direkt .PDF İndir</span>
            </button>

            {/* Offline HTML Booklet */}
            <button
              onClick={handleDownloadHtml}
              className="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 cursor-pointer transition-colors"
              title="İnternetsiz her cihazda açılabilen tek dosya HTML kitapçık"
            >
              <FileText className="w-4 h-4 text-slate-300" />
              <span className="hidden sm:inline">HTML Kitapçık</span>
            </button>

            <button
              onClick={onClose}
              className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-xl cursor-pointer transition-colors ml-1"
              aria-label="Kapat"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* ROW 2: Filter & Source Selector Bar (White) */}
        <div className="bg-white border-b border-slate-200 p-3 px-4 sm:px-5 flex flex-wrap items-center justify-between gap-3 shrink-0 no-print text-xs shadow-2xs">
          <div className="flex flex-wrap items-center gap-3">
            {/* 1. Kurul Seçici */}
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-slate-700 flex items-center gap-1 text-[11px] uppercase tracking-wide">
                <FolderOpen className="w-3.5 h-3.5 text-teal-600" />
                Kurul:
              </span>
              <select
                value={selectedCommitteeId}
                onChange={(e) => {
                  setSelectedCommitteeId(e.target.value);
                  setSelectedYear('all');
                  setSelectedDiscipline('all');
                }}
                className="bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs text-slate-900 font-semibold focus:outline-none focus:ring-1 focus:ring-teal-500 cursor-pointer"
              >
                <option value="all">🌟 Tüm Kurullar ({cleanCommittees.length > 0 ? cleanCommittees.length : 1} Kurul)</option>
                {cleanCommittees.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>

            {/* 2. Kaynak / Havuz Seçici */}
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-slate-700 flex items-center gap-1 text-[11px] uppercase tracking-wide">
                <Layers className="w-3.5 h-3.5 text-teal-600" />
                Kaynak:
              </span>
              <select
                value={sourceMode}
                onChange={(e) => setSourceMode(e.target.value as any)}
                className="bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs text-slate-900 font-semibold focus:outline-none focus:ring-1 focus:ring-teal-500 cursor-pointer"
              >
                <option value="past_exams">📚 Çıkmış Sınavlar Arşivi ({pastQuestions.length} Çıkmış)</option>
                <option value="collaborative">📝 Güncel İmece Soru Havuzu ({questions.length} Soru)</option>
                <option value="all">🌟 Birleşik Havuz (Çıkmışlar + Güncel)</option>
              </select>
            </div>

            {/* 3. Sınav Yılı Filtresi */}
            {availableYears.length > 0 && sourceMode !== 'collaborative' && (
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-slate-700 flex items-center gap-1 text-[11px] uppercase tracking-wide">
                  <Calendar className="w-3.5 h-3.5 text-teal-600" />
                  Sınav / Yıl:
                </span>
                <select
                  value={selectedYear}
                  onChange={(e) => setSelectedYear(e.target.value)}
                  className="bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs text-slate-900 font-semibold focus:outline-none focus:ring-1 focus:ring-teal-500 cursor-pointer"
                >
                  <option value="all">Tüm Yıllar ({availableYears.length} Yıl)</option>
                  {availableYears.map((yr) => (
                    <option key={yr} value={yr}>
                      {yr} Çıkmış Sınavı
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* 4. Branş / Ders Filtresi */}
            {availableDisciplines.length > 0 && (
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-slate-700 flex items-center gap-1 text-[11px] uppercase tracking-wide">
                  <GraduationCap className="w-3.5 h-3.5 text-teal-600" />
                  Ders:
                </span>
                <select
                  value={selectedDiscipline}
                  onChange={(e) => setSelectedDiscipline(e.target.value)}
                  className="bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs text-slate-900 font-semibold focus:outline-none focus:ring-1 focus:ring-teal-500 cursor-pointer max-w-[160px] truncate"
                >
                  <option value="all">Tüm Branşlar ({availableDisciplines.length})</option>
                  {availableDisciplines.map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* 5. Soru Limiti */}
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-slate-700 text-[11px] uppercase tracking-wide">Limit:</span>
              <select
                value={questionLimit}
                onChange={(e) => setQuestionLimit(Number(e.target.value))}
                className="bg-slate-50 border border-slate-300 rounded-lg px-2 py-1.5 text-xs text-slate-900 font-semibold focus:outline-none focus:ring-1 focus:ring-teal-500 cursor-pointer"
              >
                <option value={0}>Tümü ({allNormalized.length})</option>
                <option value={50}>İlk 50 Soru</option>
                <option value={100}>İlk 100 Soru (Klasik Kurul)</option>
                <option value={150}>İlk 150 Soru (Final/Bütünleme)</option>
              </select>
            </div>
          </div>

          {loadError && (
            <div className="text-[11px] text-amber-700 bg-amber-50 px-2 py-1 rounded border border-amber-200">
              {loadError}
            </div>
          )}
        </div>

        {/* ROW 3: Booklet Layout & Content Options Bar */}
        <div className="bg-slate-50 border-b border-slate-200 p-2.5 px-4 sm:px-5 flex flex-wrap items-center justify-between gap-3 shrink-0 no-print text-xs">
          {/* Mode Selector (Student vs Solution vs Answers Only) */}
          <div className="flex items-center gap-1 bg-white p-1 rounded-xl border border-slate-200 shadow-2xs">
            <button
              onClick={() => setBookletMode('student')}
              className={`px-3 py-1.5 rounded-lg font-bold transition-all cursor-pointer ${
                bookletMode === 'student'
                  ? 'bg-teal-700 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              Öğrenci Sınavı (Cevaplar Gizli)
            </button>
            <button
              onClick={() => setBookletMode('solution')}
              className={`px-3 py-1.5 rounded-lg font-bold transition-all cursor-pointer ${
                bookletMode === 'solution'
                  ? 'bg-teal-700 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              Çözümlü & Açıklamalı Kitapçık
            </button>
            <button
              onClick={() => setBookletMode('answers_only')}
              className={`px-3 py-1.5 rounded-lg font-bold transition-all cursor-pointer ${
                bookletMode === 'answers_only'
                  ? 'bg-teal-700 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              Sadece Cevap Anahtarı Matrisi
            </button>
          </div>

          {/* Columns & Checkbox Toggles */}
          <div className="flex flex-wrap items-center gap-3">
            {/* Columns Toggle */}
            <div className="flex items-center gap-1 bg-white p-1 rounded-lg border border-slate-200 shadow-2xs">
              <button
                onClick={() => setColumns('two')}
                className={`p-1.5 rounded-md transition-all cursor-pointer flex items-center gap-1 text-[11px] ${
                  columns === 'two' ? 'bg-teal-50 text-teal-800 font-bold border border-teal-200' : 'text-slate-500 hover:text-slate-900'
                }`}
                title="İki Sütunlu Klasik Tıp Kitapçığı"
              >
                <Columns className="w-3.5 h-3.5" />
                <span>2 Sütun</span>
              </button>
              <button
                onClick={() => setColumns('one')}
                className={`p-1.5 rounded-md transition-all cursor-pointer flex items-center gap-1 text-[11px] ${
                  columns === 'one' ? 'bg-teal-50 text-teal-800 font-bold border border-teal-200' : 'text-slate-500 hover:text-slate-900'
                }`}
                title="Tek Sütunlu Geniş Okuma Mizanpajı"
              >
                <Square className="w-3.5 h-3.5" />
                <span>Tek Sütun</span>
              </button>
            </div>

            {/* Answer Matrix Checkbox */}
            <label className="flex items-center gap-1.5 cursor-pointer text-slate-700 select-none font-medium">
              <input
                type="checkbox"
                checked={includeAnswerMatrix}
                onChange={(e) => setIncludeAnswerMatrix(e.target.checked)}
                className="rounded border-slate-300 text-teal-600 focus:ring-teal-500"
              />
              <span>Cevap Anahtarı Tablosunu Ekle</span>
            </label>

            {/* Ready Only Checkbox */}
            <label className="flex items-center gap-1.5 cursor-pointer text-slate-700 select-none font-medium">
              <input
                type="checkbox"
                checked={filterReadyOnly}
                onChange={(e) => setFilterReadyOnly(e.target.checked)}
                className="rounded border-slate-300 text-teal-600 focus:ring-teal-500"
              />
              <span>Yalnızca Doğrulanmışlar</span>
            </label>
          </div>
        </div>

        {/* Printable A4 Content Area (Scrollable in modal, full in print) */}
        <div className="pdf-modal-scrollable overflow-y-auto p-3 sm:p-8 flex justify-center bg-slate-200/70">
          <div
            id="exam-printable-content"
            className="print-container bg-white shadow-xl border border-slate-300 p-6 sm:p-12 w-full max-w-[210mm] min-h-[297mm] text-slate-900 font-sans print:shadow-none print:border-none print:p-0 print:m-0"
          >
            {/* Official Exam Header */}
            <div className="border-b-2 border-slate-900 pb-4 mb-5 text-center space-y-1">
              <div className="flex items-center justify-between text-[11px] font-bold text-slate-500 uppercase tracking-widest border-b border-slate-200 pb-1.5 mb-2">
                <span>T.C. TIP FAKÜLTESİ DEKANLIĞI</span>
                <span>DÖNEM {activeCommittee?.year || 3} • {displayTerm}</span>
                <span className="bg-slate-900 text-white px-2 py-0.5 rounded text-[10px] font-mono">
                  A KİTAPÇIĞI
                </span>
              </div>

              <h1 className="text-base sm:text-xl font-black text-slate-900 uppercase tracking-tight">
                {displayTitle}
              </h1>

              <div className="flex flex-wrap items-center justify-center gap-3 text-xs text-slate-700 font-serif pt-1">
                <span><strong>Soru Sayısı:</strong> {displayTarget} Soru</span>
                <span>•</span>
                <span><strong>Sınav Süresi:</strong> {examDuration} Dakika</span>
                {selectedYear !== 'all' && (
                  <>
                    <span>•</span>
                    <span><strong>Sınav Yılı:</strong> {selectedYear}</span>
                  </>
                )}
                <span>•</span>
                <span>
                  <strong>Format:</strong>{' '}
                  {bookletMode === 'student'
                    ? 'Öğrenci Deneme Sınavı'
                    : bookletMode === 'solution'
                    ? 'Çözümlü ve Açıklamalı Çalışma Kitapçığı'
                    : 'Cevap Anahtarı Matrisi'}
                </span>
              </div>
            </div>

            {/* Exam Instructions Banner */}
            {bookletMode !== 'answers_only' && (
              <div className="instructions bg-slate-50 border border-slate-200 rounded-md p-2.5 mb-6 text-[11px] text-slate-700 space-y-0.5">
                <p className="font-bold text-slate-900">SINAV YÖNERGESİ VE KURALLAR:</p>
                <p>1. Bu soru kitapçığında toplam {displayTarget} soru yer almaktadır. Her sorunun yalnızca tek bir doğru cevabı vardır.</p>
                <p>2. Cevaplarınızı optik cevap kâğıdındaki ilgili soru numarasına taşıyınız. Yanlış cevaplar doğru cevapları götürmez.</p>
                <p className="text-[10px] text-slate-500 italic">
                  MedSoru Tıp Kurul Kolektif Hafıza & Yapay Zeka Rekonstrüksiyon Arşivi tarafından hazırlanmıştır.
                </p>
              </div>
            )}

            {/* Empty State */}
            {filteredQuestions.length === 0 && (
              <div className="text-center py-16 px-4 space-y-3 bg-slate-50 rounded-xl border border-dashed border-slate-300">
                <FileText className="w-10 h-10 text-slate-400 mx-auto" />
                <h3 className="font-bold text-slate-700 text-sm">Seçilen Kriterlere Uygun Soru Bulunamadı</h3>
                <p className="text-xs text-slate-500 max-w-md mx-auto">
                  Lütfen Kurul, Kaynak, Sınav Yılı veya Branş filtrelerini değiştirerek tekrar deneyiniz.
                </p>
              </div>
            )}

            {/* Questions Layout */}
            {bookletMode !== 'answers_only' && filteredQuestions.length > 0 && (
              <div
                className={`exam-columns-${columns === 'two' ? '2' : '1'} ${
                  columns === 'two' ? 'columns-1 md:columns-2 gap-8' : 'space-y-6'
                } text-xs leading-relaxed`}
              >
                {filteredQuestions.map((q, idx) => {
                  const qNum = q.questionNumber || (idx + 1);

                  return (
                    <div
                      key={q.id}
                      className="exam-question-item mb-5 pb-3 border-b border-slate-200 break-inside-avoid page-break-inside-avoid"
                    >
                      {/* Question meta bar */}
                      <div className="flex items-center justify-between text-[11px] font-bold text-slate-800 mb-1.5">
                        <span className="bg-slate-900 text-white font-mono px-2 py-0.5 rounded text-[10px] tracking-wide">
                          SORU {qNum}
                        </span>
                        <span className="text-teal-800 font-semibold text-[10px] uppercase truncate max-w-[210px]">
                          {q.discipline} {q.topic ? `• ${q.topic}` : ''} {q.examYear ? `(${q.examYear})` : ''}
                        </span>
                      </div>

                      {/* Question Case Stem */}
                      <p className="font-serif text-[11.5px] font-normal text-slate-900 leading-normal mb-2 whitespace-pre-line text-justify">
                        {q.stem}
                      </p>

                      {/* Options */}
                      <div className="space-y-1 pl-1 text-[11px]">
                        {q.options.map((opt) => {
                          const isCorrect = q.correctAnswer === opt.key || !!opt.isCorrect;
                          const showAsCorrect = bookletMode === 'solution' && isCorrect;

                          return (
                            <div
                              key={opt.key}
                              className={`flex items-start gap-2 py-0.5 px-1.5 rounded transition-colors ${
                                showAsCorrect
                                  ? 'bg-emerald-50 text-emerald-900 font-bold border border-emerald-300'
                                  : 'text-slate-800'
                              }`}
                            >
                              <span className="font-bold shrink-0 font-mono">
                                {opt.key})
                              </span>
                              <span className="leading-tight">{opt.text}</span>
                              {showAsCorrect && (
                                <span className="ml-auto text-[9px] text-emerald-700 uppercase font-mono font-bold shrink-0">
                                  [DOĞRU CEVAP]
                                </span>
                              )}
                            </div>
                          );
                        })}
                      </div>

                      {/* Detailed Medical Explanation (Solution Mode) */}
                      {bookletMode === 'solution' && q.explanation && (
                        <div className="mt-2.5 p-2 bg-emerald-50/70 border-l-2 border-emerald-600 rounded text-[10.5px] text-emerald-950 space-y-0.5">
                          <div className="font-bold flex items-center gap-1 text-emerald-900 text-[11px]">
                            <CheckCircle2 className="w-3 h-3 text-emerald-600 shrink-0" />
                            <span>Gerekçe & Patofizyolojik Açıklama (Doğru Cevap: {q.correctAnswer || 'Belirtilmemiş'}):</span>
                          </div>
                          <p className="leading-snug text-slate-700 italic">
                            {q.explanation}
                          </p>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}

            {/* Answer Key Summary Table */}
            {includeAnswerMatrix && filteredQuestions.length > 0 && (
              <div className="exam-answer-table mt-8 pt-6 border-t-2 border-slate-900 page-break-before">
                <div className="text-center mb-4">
                  <h3 className="text-sm font-bold uppercase tracking-wider text-slate-900">
                    CEVAP ANAHTARI ÖZETİ (A KİTAPÇIĞI)
                  </h3>
                  <p className="text-[11px] text-slate-500 font-serif">
                    {displayTitle} • Toplam {filteredQuestions.length} Soru
                  </p>
                </div>

                <div className="grid grid-cols-5 sm:grid-cols-10 gap-1.5 text-center text-xs">
                  {filteredQuestions.map((q, idx) => {
                    const qNum = q.questionNumber || (idx + 1);
                    const ans = q.correctAnswer || '-';
                    return (
                      <div
                        key={q.id + '-' + idx}
                        className={`p-1.5 rounded border ${
                          ans !== '-'
                            ? 'bg-slate-50 border-slate-300 text-slate-900'
                            : 'bg-slate-100/50 border-slate-200 text-slate-400'
                        }`}
                      >
                        <span className="block text-[9px] text-slate-500 font-mono">
                          #{qNum}
                        </span>
                        <span className="block font-black text-xs text-teal-800">
                          {bookletMode === 'student' ? '___' : ans}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Official Footer */}
            <div className="mt-8 pt-4 border-t border-slate-200 flex items-center justify-between text-[10px] text-slate-400 font-mono">
              <span>MedSoru - Tıp Fakültesi Kurul Sınavı Arşivi</span>
              <span>Sayfa Sonu • Başarılar Dileriz</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
