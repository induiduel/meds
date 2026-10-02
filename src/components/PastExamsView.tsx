import React, { useState, useMemo, useEffect } from 'react';
import {
  Sparkles,
  BookOpen,
  Search,
  Filter,
  CheckCircle2,
  Calendar,
  Layers,
  ChevronLeft,
  ChevronRight,
  ThumbsUp,
  ExternalLink,
  BookMarked,
  X,
  FileText,
  HelpCircle,
  Copy,
  Check,
  GraduationCap,
  Eye,
  ArrowUpDown,
  RefreshCw,
  Clock,
  Tag,
  Stethoscope,
  Flag,
  MessageSquare,
  Send,
  AlertCircle,
  Database,
  HardDrive,
  Zap,
  SlidersHorizontal,
  ChevronDown,
  Wand2,
  PenLine,
} from 'lucide-react';
import { ActionMenu, ActionItem } from './ui/ActionMenu';
import { QuestionItem, LectureNote, LectureNotePage, QuestionLectureMatch } from '../types';
import { AppUser, ADMIN_EMAIL } from '../services/auth';
import { ApiService } from '../services/api';
import { pastQuestionsCache, CacheSyncStatus } from '../services/pastQuestionsCache';
import { AdminCustomRedactModal } from './AdminCustomRedactModal';
import { AiQuestionOptimizerModal } from './AiQuestionOptimizerModal';
import { AdvancedQuestionUpgradeModal } from './AdvancedQuestionUpgradeModal';
import { renderHighlightedSnippet } from './QuestionCard';
import { learnMatcher, QuestionLearnMatch } from '../services/learnMatcher';
import { FlashcardComponent } from './learn/InteractiveDeckView';

interface PastExamsViewProps {
  currentUser: AppUser | null;
  lectureNotes?: LectureNote[];
  onOpenNote?: (noteId: string, pageNumber?: number) => void;
  onUpdateQuestionReference?: (questionId: string, match: QuestionLectureMatch) => Promise<void>;
  onNavigateToLearn?: (deckId?: string, slideNumber?: number) => void;
}

export const PastExamsView: React.FC<PastExamsViewProps> = ({
  currentUser,
  lectureNotes = [],
  onOpenNote,
  onUpdateQuestionReference,
  onNavigateToLearn,
}) => {
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [internalNotes, setInternalNotes] = useState<LectureNote[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Filter States
  const [selectedCommittee, setSelectedCommittee] = useState<string>('all');
  const [selectedYear, setSelectedYear] = useState<string>('all');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('all');
  const [viewMode, setViewMode] = useState<'redacted' | 'raw' | 'split'>('redacted');
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [openExplanations, setOpenExplanations] = useState<Record<string, boolean>>({});
  const [ambiguityTab, setAmbiguityTab] = useState<'valid' | 'ambiguous' | 'all'>('valid');
  
  // Per-question card override: questionId -> 'redacted' | 'raw' | 'split'
  const [cardViewOverrides, setCardViewOverrides] = useState<Record<string, 'redacted' | 'raw' | 'split'>>({});
  
  // Selected Öğren modülü match modal state
  const [selectedLearnMatch, setSelectedLearnMatch] = useState<{
    question: QuestionItem;
    match: QuestionLearnMatch;
  } | null>(null);

  // Selected Ham Soru location modal state
  const [selectedRawSourceQuestion, setSelectedRawSourceQuestion] = useState<QuestionItem | null>(null);

  // AI Similar Question Modal State
  const [similarModalQuestion, setSimilarModalQuestion] = useState<any | null>(null);
  const [isGeneratingSimilar, setIsGeneratingSimilar] = useState<string | null>(null);

  // Admin Custom AI Redaction Modal State
  const [customRedactQuestion, setCustomRedactQuestion] = useState<{ question: QuestionItem; match: any } | null>(null);

  // Student & User AI Question Optimizer Modal State
  const [optimizeModalQuestion, setOptimizeModalQuestion] = useState<QuestionItem | null>(null);

  // Advanced Question Upgrade Modal State (Gelişmiş Klinik Vaka)
  const [upgradeModalQuestion, setUpgradeModalQuestion] = useState<QuestionItem | null>(null);

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 25;

  // Report Modal State
  const [reportingQuestion, setReportingQuestion] = useState<any | null>(null);
  const [reportReason, setReportReason] = useState('Hatalı Soru Kökü');
  const [reportDetails, setReportDetails] = useState('');
  const [isSubmittingReport, setIsSubmittingReport] = useState(false);
  const [reportSuccessMsg, setReportSuccessMsg] = useState<string | null>(null);

  // Active Comments Drawer State
  const [expandedCommentsQuestionId, setExpandedCommentsQuestionId] = useState<string | null>(null);
  const [newCommentText, setNewCommentText] = useState('');
  const [isSubmittingComment, setIsSubmittingComment] = useState(false);

  // Feedback & Copy state
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Client-Side Caching & Delta-Sync State
  const [cacheStatus, setCacheStatus] = useState<CacheSyncStatus>(pastQuestionsCache.getStatus());

  // Load questions
  const loadPastQuestions = async () => {
    setIsLoading(true);
    try {
      const data = await ApiService.getPastQuestions();
      setQuestions(data.filter(q => !q.id?.startsWith('civan-') && !q.tags?.some((t: string) => /civan/i.test(t))));
    } catch (e) {
      console.warn('Could not load past questions:', e);
    } finally {
      setIsLoading(false);
    }
  };

  // Manual Trigger to Check Database Updates
  const handleManualSync = async () => {
    await pastQuestionsCache.syncWithRemote();
  };

  // Submit Question Report ("Şikayet Et / Hata Bildir")
  const handleReportSubmit = async () => {
    if (!reportingQuestion) return;
    setIsSubmittingReport(true);
    try {
      await ApiService.reportPastQuestion(
        reportingQuestion.id,
        reportReason,
        reportDetails,
        currentUser?.displayName || 'Tıp Öğrencisi'
      );
      setReportSuccessMsg('Geri bildiriminiz ve şikayetiniz incelenmek üzere kaydedildi. Katkınız için teşekkür ederiz!');
      setTimeout(() => {
        setReportSuccessMsg(null);
        setReportingQuestion(null);
        setReportDetails('');
      }, 2000);
    } catch (e: any) {
      alert('Şikayet kaydedilemedi: ' + (e.message || 'Bilinmeyen hata'));
    } finally {
      setIsSubmittingReport(false);
    }
  };

  // Submit Question Comment ("Öneri / Çözüm Yolu Ekle")
  const handleCommentSubmit = async (qId: string) => {
    if (!newCommentText.trim()) return;
    setIsSubmittingComment(true);
    try {
      const res = await ApiService.commentPastQuestion(
        qId,
        currentUser?.displayName || 'Tıp Öğrencisi',
        newCommentText.trim()
      );
      if (res && res.comment) {
        setQuestions(prev => prev.map(q => {
          if (q.id === qId) {
            const comments = (q as any).comments || [];
            return { ...q, comments: [...comments, res.comment] };
          }
          return q;
        }));
        setNewCommentText('');
      }
    } catch (e: any) {
      alert('Yorum kaydedilemedi: ' + (e.message || 'Bilinmeyen hata'));
    } finally {
      setIsSubmittingComment(false);
    }
  };

  // Generate similar practice question handler
  const handleGenerateSimilarQuestion = async (q: QuestionItem, slideMatch: any) => {
    setIsGeneratingSimilar(q.id);
    try {
      const generated = await ApiService.generateSimilarQuestion(q, slideMatch);
      if (generated) {
        setSimilarModalQuestion(generated);
      }
    } catch (e) {
      console.warn('Generate similar question error:', e);
    } finally {
      setIsGeneratingSimilar(null);
    }
  };

  useEffect(() => {
    loadPastQuestions();

    // Subscribe to incremental cache updates (Soru bazında anlık canlı güncelleme)
    const unsubscribe = pastQuestionsCache.subscribe((status, updatedList) => {
      setCacheStatus(status);
      if (updatedList && updatedList.length > 0) {
        const updateMap = new Map(updatedList.map(q => [q.id, q]));
        setQuestions(prev => {
          let hasChange = false;
          const next = prev.map(existing => {
            if (updateMap.has(existing.id)) {
              hasChange = true;
              return updateMap.get(existing.id)!;
            }
            return existing;
          });
          for (const newQ of updatedList) {
            if (!prev.some(p => p.id === newQ.id)) {
              next.unshift(newQ);
              hasChange = true;
            }
          }
          return hasChange ? next : prev;
        });
      }
    });

    ApiService.getLectureNotes()
      .then(notes => {
        if (notes && notes.length > 0) setInternalNotes(notes);
      })
      .catch(err => console.warn('Could not fetch lecture notes for past exams:', err));

    return () => unsubscribe();
  }, []);

  // Upvote / Like toggle
  const handleToggleLike = async (q: QuestionItem) => {
    const userUid = currentUser?.uid || 'anonim-std';
    const isLiked = (q.likedBy || []).includes(userUid);
    const newLikedBy = isLiked
      ? (q.likedBy || []).filter(u => u !== userUid)
      : [...(q.likedBy || []), userUid];
    const newUpvotes = isLiked
      ? Math.max(0, (q.upvotes || 1) - 1)
      : (q.upvotes || 0) + 1;

    // Optimistic UI update
    setQuestions(prev =>
      prev.map(item =>
        item.id === q.id
          ? { ...item, upvotes: newUpvotes, likedBy: newLikedBy }
          : item
      )
    );

    try {
      await ApiService.upvoteQuestion(q.id, userUid);
    } catch (err) {
      // Revert if error
      console.warn('Like toggle error:', err);
    }
  };

  // Copy question text to clipboard
  const handleCopyQuestion = (q: QuestionItem) => {
    const stem = q.reconstruction?.stem || q.fragments?.[0]?.text || q.topic;
    const optionsText = (q.reconstruction?.options || q.options || [])
      .map((o: any) => `${o.key}) ${o.text}`)
      .join('\n');
    const answer = q.reconstruction?.correctAnswer || q.claimedAnswer ? `\nDoğru Cevap: ${q.reconstruction?.correctAnswer || q.claimedAnswer}` : '';
    const explanation = q.reconstruction?.explanation ? `\nAçıklama: ${q.reconstruction.explanation}` : '';
    
    const fullText = `[MedSoru Çıkmış Soru - ${q.discipline} #${q.questionNumber}]\n\n${stem}\n\n${optionsText}${answer}${explanation}`;
    navigator.clipboard.writeText(fullText);
    setCopiedId(q.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const effectiveNotes = lectureNotes && lectureNotes.length > 0 ? lectureNotes : internalNotes;

  // Find best matching lecture note page for a question
  const getQuestionSlideMatch = useMemo(() => {
    const cache = new Map<string, { note: LectureNote; page: LectureNotePage; score: number } | null>();

    return (q: QuestionItem): { note: LectureNote; page: LectureNotePage; score: number } | null => {
      if (cache.has(q.id)) return cache.get(q.id)!;
      if (!effectiveNotes || effectiveNotes.length === 0) return null;

      const qText = `${q.topic} ${q.discipline} ${q.reconstruction?.stem || ''} ${q.fragments?.map(f => f.text).join(' ') || ''}`.toLowerCase();

      let best: { note: LectureNote; page: LectureNotePage; score: number } | null = null;

      for (const n of effectiveNotes) {
        const isDisciplineMatch = q.discipline && n.discipline && (
          q.discipline.toLowerCase() === n.discipline.toLowerCase() ||
          q.discipline.toLowerCase().includes(n.discipline.toLowerCase()) ||
          n.discipline.toLowerCase().includes(q.discipline.toLowerCase())
        );

        for (const page of n.pages) {
          let score = 0;
          if (isDisciplineMatch) score += 20;

          // Keyword matches
          for (const kw of page.keywords) {
            if (kw.length >= 4 && qText.includes(kw.toLowerCase())) {
              score += 15;
            }
          }

          if (score >= 35) {
            if (!best || score > best.score) {
              best = { note: n, page, score };
            }
          }
        }
      }

      cache.set(q.id, best);
      return best;
    };
  }, [effectiveNotes]);

  // Format raw source file and location labels
  const getRawSourceBadge = (q: QuestionItem) => {
    const file = (q.sourceFile || q.sourceNote || 'Sınav Arşivi')
      .replace(/\.[^/.]+$/, '')
      .replace(/_/g, ' ');
    const page = q.matchedSlidePage ? ` #${q.matchedSlidePage}` : '';
    return `${file.substring(0, 18)}${page}`;
  };

  const getRawSourceSummary = (q: QuestionItem) => {
    const file = (q.sourceFile || q.sourceNote || 'Sınav Arşivi')
      .replace(/\.[^/.]+$/, '')
      .replace(/_/g, ' ');
    const page = q.matchedSlidePage ? ` · Sayfa #${q.matchedSlidePage}` : '';
    const qNum = q.questionNumber ? ` · Soru #${q.questionNumber}` : '';
    return `${file}${page}${qNum}`;
  };

  // Curriculum Disciplines List
  const CURRICULUM_DISCIPLINES = [
    'Tıbbi Biyoloji ve Genetik',
    'Tıbbi Biyokimya',
    'Tıbbi Patoloji',
    'Tıbbi Farmakoloji',
    'Tıbbi Mikrobiyoloji',
    'Histoloji ve Embriyoloji',
    'Anatomi',
    'Fizyoloji',
    'İç Hastalıkları',
    'Kardiyoloji',
    'Göğüs Hastalıkları',
    'Enfeksiyon Hastalıkları',
    'Pediatri (Çocuk Sağlığı)',
    'Kadın Hastalıkları ve Doğum',
    'Genel Cerrahi',
    'Üroloji',
    'Nöroloji',
    'Psikiyatri',
    'Beyin ve Sinir Cerrahisi',
    'Ortopedi ve Travmatoloji',
    'Acil Tıp',
    'Aile Hekimliği',
    'Halk Sağlığı',
    'Tıbbi Genetik',
    'FTR',
    'Anesteziyoloji ve Reanimasyon',
  ];

  // Available options for filters derived from data
  const filterOptions = useMemo(() => {
    const committees = new Set<string>();
    const years = new Set<string>();
    const disciplines = new Set<string>(CURRICULUM_DISCIPLINES);

    questions.forEach(q => {
      if (q.committeeId) committees.add(q.committeeId);
      if (q.examYear && !q.examYear.includes('2026') && !q.examYear.toLowerCase().includes('civan')) {
        years.add(q.examYear);
      }
      if (q.discipline) disciplines.add(q.discipline);
    });

    years.add('Kategorisiz');

    return {
      committees: Array.from(committees).sort(),
      years: Array.from(years).sort(),
      disciplines: Array.from(disciplines).sort(),
    };
  }, [questions]);

  // Counts for tabs
  const tabCounts = useMemo(() => {
    const validCount = questions.filter(q => !q.isAmbiguous).length;
    const ambiguousCount = questions.filter(q => q.isAmbiguous).length;
    return { validCount, ambiguousCount, totalCount: questions.length };
  }, [questions]);

  // Filtered Questions
  const filteredQuestions = useMemo(() => {
    return questions.filter(q => {
      // 1. Ambiguity Filter (Muallak vs Tam Metin)
      if (ambiguityTab === 'valid' && q.isAmbiguous) return false;
      if (ambiguityTab === 'ambiguous' && !q.isAmbiguous) return false;

      // 2. Search
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase();
        const inTopic = (q.topic || '').toLowerCase().includes(query);
        const inDiscipline = (q.discipline || '').toLowerCase().includes(query);
        const inStem = (q.reconstruction?.stem || '').toLowerCase().includes(query);
        const inFragments = (q.fragments || []).some(f => f.text.toLowerCase().includes(query));
        const inOptions = (q.options || []).some(o => o.text.toLowerCase().includes(query));
        const inNumber = (q.questionNumber?.toString() || '').includes(query);
        const inYear = (q.examYear || '').toLowerCase().includes(query);
        const inFile = (q.sourceFile || '').toLowerCase().includes(query);

        if (!inTopic && !inDiscipline && !inStem && !inFragments && !inOptions && !inNumber && !inYear && !inFile) {
          return false;
        }
      }

      // 3. Committee filter
      if (selectedCommittee !== 'all') {
        if (q.committeeId !== selectedCommittee) {
          return false;
        }
      }

      // 4. Year filter
      if (selectedYear !== 'all') {
        if (selectedYear === 'Kategorisiz') {
          if (q.examYear && q.examYear !== 'Kategorisiz' && q.examYear !== 'Çıkmış Soru') return false;
        } else if (q.examYear !== selectedYear) {
          return false;
        }
      }

      // 5. Discipline filter
      if (selectedDiscipline !== 'all') {
        const qDisc = (q.discipline || '').toLowerCase();
        const selDisc = selectedDiscipline.toLowerCase();
        if (qDisc !== selDisc && !qDisc.includes(selDisc) && !selDisc.includes(qDisc)) {
          return false;
        }
      }

      return true;
    });
  }, [questions, ambiguityTab, searchQuery, selectedCommittee, selectedYear, selectedDiscipline]);

  // Paginated list
  const totalPages = Math.max(1, Math.ceil(filteredQuestions.length / itemsPerPage));
  const paginatedQuestions = useMemo(() => {
    const start = (currentPage - 1) * itemsPerPage;
    return filteredQuestions.slice(start, start + itemsPerPage);
  }, [filteredQuestions, currentPage]);

  // Human committee name translator
  const formatCommitteeName = (cId: string) => {
    // Dönem 3
    if (cId === 'donem3-kurul1') return 'Dönem 3 Kurul 1: TIP 310 - Ürogenital ve Obstetrik';
    if (cId === 'donem3-kurul2') return 'Dönem 3 Kurul 2: TIP 320 - Nöropsikiyatri';
    if (cId === 'donem3-kurul3') return 'Dönem 3 Kurul 3: TIP 330 - Gastrointestinal Sistem';
    if (cId === 'donem3-kurul4') return 'Dönem 3 Kurul 4: TIP 340 - Dolaşım, Solunum ve Tümör';
    if (cId === 'donem3-kurul5') return 'Dönem 3 Kurul 5: TIP 350 - Ortopedi, Travmatoloji ve Hematopoetik Sistem';
    if (cId === 'donem3-kurul6') return 'Dönem 3 Kurul 6: TIP 360 - Endokrin, Metabolizma ve Yaşlanma';
    if (cId === 'donem3-final') return 'Dönem 3 Final Sınavı (28.06.2027)';
    if (cId === 'donem3-butunleme') return 'Dönem 3 Bütünleme Sınavı (16.07.2027)';

    // Dönem 2
    if (cId === 'donem2-kurul1') return 'Dönem 2 Kurul 1: TIP 211 - Dolaşım ve Solunum Sistemleri';
    if (cId === 'donem2-kurul2') return 'Dönem 2 Kurul 2: TIP 212 - Sindirim ve Metabolizma Sistemleri';
    if (cId === 'donem2-kurul3') return 'Dönem 2 Kurul 3: TIP 213 - Ürogenital ve Endokrin Sistemleri';
    if (cId === 'donem2-kurul4') return 'Dönem 2 Kurul 4: TIP 214 - Sinir Sistemi ve Duyu Organları';
    if (cId === 'donem2-kurul5') return 'Dönem 2 Kurul 5: TIP 215 - Hastalıkların Biyolojik Temelleri';
    if (cId === 'donem2-final') return 'Dönem 2 Final Sınavı';

    // Dönem 1
    if (cId === 'donem1-kurul1') return 'Dönem 1 Kurul 1: TIP 111 - Hücre Biyolojisi I';
    if (cId === 'donem1-kurul2') return 'Dönem 1 Kurul 2: TIP 112 - Hücre Biyolojisi II';
    if (cId === 'donem1-kurul3') return 'Dönem 1 Kurul 3: TIP 113 - Hücre Biyolojisi III';
    if (cId === 'donem1-kurul4') return 'Dönem 1 Kurul 4: TIP 114 - Kemik ve Eklem Kurulu';
    if (cId === 'donem1-kurul5') return 'Dönem 1 Kurul 5: TIP 115 - Kas Kurulu';

    return cId;
  };

  const activeFilterChips: { label: string; clear: () => void }[] = [
    ...(ambiguityTab !== 'valid'
      ? [{ label: ambiguityTab === 'ambiguous' ? 'İnceleme bekleyen' : 'Tüm havuz', clear: () => setAmbiguityTab('valid') }]
      : []),
    ...(selectedCommittee !== 'all'
      ? [{ label: formatCommitteeName(selectedCommittee).split(':')[0], clear: () => setSelectedCommittee('all') }]
      : []),
    ...(selectedYear !== 'all' ? [{ label: selectedYear, clear: () => setSelectedYear('all') }] : []),
    ...(selectedDiscipline !== 'all' ? [{ label: selectedDiscipline, clear: () => setSelectedDiscipline('all') }] : []),
    ...(viewMode !== 'redacted'
      ? [{ label: viewMode === 'raw' ? 'Ham görünüm' : 'Karşılaştır', clear: () => setViewMode('redacted') }]
      : []),
  ];
  const clearAllFilters = () => {
    setSearchQuery('');
    setAmbiguityTab('valid');
    setSelectedCommittee('all');
    setSelectedYear('all');
    setSelectedDiscipline('all');
    setViewMode('redacted');
    setCurrentPage(1);
  };
  const isAdminUser = currentUser?.email === ADMIN_EMAIL || !!currentUser?.isAdmin;
  const chipCls = (on: boolean) =>
    `h-9 px-3.5 rounded-full text-[13.5px] whitespace-nowrap cursor-pointer transition-colors ${
      on ? 'bg-accent-soft text-accent font-semibold ring-1 ring-inset ring-accent' : 'bg-white text-ink border border-line hover:border-line-2'
    }`;
  const selectCls =
    'w-full h-11 sm:h-10 rounded-[10px] bg-field border border-line px-3 text-[14px] text-ink cursor-pointer outline-0 focus:border-accent';

  return (
    <div className="flex flex-col gap-3 sm:gap-4 pb-12 min-w-0 w-full max-w-[880px] mx-auto">
      {/* Title */}
      <div className="flex items-end gap-3">
        <div className="min-w-0 flex-1">
          <h1 className="m-0 font-display font-bold text-[28px] sm:text-[30px] leading-[1.1] tracking-[-0.03em] text-ink">Çıkmış sorular</h1>
          <p className="m-0 mt-1 text-[14px] text-ink-3">
            {tabCounts.validCount.toLocaleString('tr-TR')} tam metin soru
            {tabCounts.ambiguousCount > 0 && ` · ${tabCounts.ambiguousCount.toLocaleString('tr-TR')} inceleme bekliyor`}
          </p>
        </div>
        <button
          type="button"
          onClick={handleManualSync}
          disabled={cacheStatus.isSyncing}
          aria-label="Güncellemeleri denetle"
          title={`Cihazda ${questions.length.toLocaleString('tr-TR')} soru · güncellemeleri denetle`}
          className="w-10 h-10 rounded-[10px] border border-line bg-white text-ink-2 flex items-center justify-center cursor-pointer hover:border-line-2 disabled:opacity-60 shrink-0"
        >
          <RefreshCw className={`w-4 h-4 ${cacheStatus.isSyncing ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Search + one filter button */}
      <div className="flex gap-2">
        <label className="flex-1 min-w-0 flex items-center gap-2 h-11 px-3.5 rounded-[12px] bg-white border border-line focus-within:border-accent">
          <Search className="w-[17px] h-[17px] text-ink-3 shrink-0" />
          <span className="sr-only">Çıkmış sorularda ara</span>
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setCurrentPage(1);
            }}
            placeholder="Soru, şık ya da konu ara"
            className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[16px] sm:text-[15px] placeholder:text-[#7A8693]"
          />
          {searchQuery && (
            <button type="button" onClick={() => setSearchQuery('')} aria-label="Aramayı temizle" className="w-7 h-7 -mr-1 rounded-full flex items-center justify-center text-ink-3 hover:bg-canvas cursor-pointer">
              <X className="w-4 h-4" />
            </button>
          )}
        </label>
        <button
          type="button"
          onClick={() => setFiltersOpen((v) => !v)}
          aria-expanded={filtersOpen}
          aria-label={`Filtrele${activeFilterChips.length ? `, ${activeFilterChips.length} etkin` : ''}`}
          className={`relative h-11 px-3 sm:px-3.5 rounded-[12px] border text-[14px] font-semibold flex items-center gap-2 cursor-pointer shrink-0 transition-colors ${
            filtersOpen ? 'bg-accent-soft border-accent text-accent' : 'bg-white border-line text-ink hover:border-line-2'
          }`}
        >
          <SlidersHorizontal className="w-[17px] h-[17px]" />
          <span className="hidden sm:inline">Filtrele</span>
          {activeFilterChips.length > 0 && (
            <span className="absolute -top-1.5 -right-1.5 sm:static min-w-5 h-5 px-1.5 rounded-full bg-accent text-white text-[12px] inline-flex items-center justify-center">
              {activeFilterChips.length}
            </span>
          )}
        </button>
      </div>

      {/* Filter panel: inline on tablet/desktop, bottom sheet on phones */}
      {filtersOpen && (
        <div className="fixed inset-0 z-[60] flex items-end sm:static sm:z-auto sm:block" role="dialog" aria-label="Filtreler">
          <button type="button" aria-label="Kapat" onClick={() => setFiltersOpen(false)} className="sm:hidden absolute inset-0 bg-[rgba(14,26,38,0.4)] cursor-default" />
          <div className="relative w-full max-h-[85dvh] overflow-y-auto sm:overflow-visible bg-white rounded-t-[24px] sm:rounded-[16px] sm:border sm:border-line px-4 pt-2 sm:pt-4 pb-[max(env(safe-area-inset-bottom),20px)] sm:pb-4 flex flex-col gap-4 shadow-[0_-10px_40px_rgba(14,26,38,0.18)] sm:shadow-none">
            <span className="sm:hidden self-center w-10 h-[5px] rounded-full bg-line-2" aria-hidden="true" />
            <div className="sm:hidden flex items-center">
              <span className="flex-1 text-[18px] font-bold">Filtrele</span>
              <button type="button" onClick={() => setFiltersOpen(false)} className="h-9 px-2 text-[15px] font-semibold text-accent cursor-pointer">
                Bitti
              </button>
            </div>

            <div className="flex flex-col gap-1.5">
              <span className="text-[12.5px] font-semibold text-ink-3">Havuz</span>
              <div className="flex flex-wrap gap-1.5">
                {(
                  [
                    ['valid', `Tam metin · ${tabCounts.validCount}`],
                    ['ambiguous', `İnceleme bekleyen · ${tabCounts.ambiguousCount}`],
                    ['all', `Tümü · ${tabCounts.totalCount}`],
                  ] as const
                ).map(([id, label]) => (
                  <button
                    key={id}
                    type="button"
                    aria-pressed={ambiguityTab === id}
                    onClick={() => {
                      setAmbiguityTab(id);
                      setCurrentPage(1);
                    }}
                    className={chipCls(ambiguityTab === id)}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <label className="flex flex-col gap-1.5">
                <span className="text-[12.5px] font-semibold text-ink-3">Sınav</span>
                <select
                  value={selectedCommittee}
                  onChange={(e) => {
                    setSelectedCommittee(e.target.value);
                    setCurrentPage(1);
                  }}
                  className={selectCls}
                >
                  <option value="all">Tüm kurul ve sınavlar</option>
                  {filterOptions.committees.map((cId) => (
                    <option key={cId} value={cId}>
                      {formatCommitteeName(cId)}
                    </option>
                  ))}
                </select>
              </label>
              <label className="flex flex-col gap-1.5">
                <span className="text-[12.5px] font-semibold text-ink-3">Yıl</span>
                <select
                  value={selectedYear}
                  onChange={(e) => {
                    setSelectedYear(e.target.value);
                    setCurrentPage(1);
                  }}
                  className={selectCls}
                >
                  <option value="all">Tüm yıllar</option>
                  {filterOptions.years.map((yr) => (
                    <option key={yr} value={yr}>
                      {yr}
                    </option>
                  ))}
                </select>
              </label>
              <label className="flex flex-col gap-1.5">
                <span className="text-[12.5px] font-semibold text-ink-3">Branş</span>
                <select
                  value={selectedDiscipline}
                  onChange={(e) => {
                    setSelectedDiscipline(e.target.value);
                    setCurrentPage(1);
                  }}
                  className={selectCls}
                >
                  <option value="all">Tüm branşlar</option>
                  {filterOptions.disciplines.map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <div className="flex flex-col gap-1.5">
              <span className="text-[12.5px] font-semibold text-ink-3">Görünüm</span>
              <div role="radiogroup" aria-label="Görünüm" className="grid grid-cols-3 sm:inline-grid sm:w-[360px] gap-1 bg-canvas rounded-[12px] p-1">
                {(
                  [
                    ['redacted', 'Düzenlenmiş'],
                    ['raw', 'Ham'],
                    ['split', 'Karşılaştır'],
                  ] as const
                ).map(([id, label]) => (
                  <button
                    key={id}
                    type="button"
                    role="radio"
                    aria-checked={viewMode === id}
                    onClick={() => setViewMode(id)}
                    className={`h-9 rounded-[9px] text-[13.5px] cursor-pointer ${
                      viewMode === id ? 'bg-white font-semibold text-ink shadow-[0_1px_3px_rgba(14,26,38,0.12)]' : 'text-ink-2'
                    }`}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between gap-2 pt-3 border-t border-line-soft">
              <button type="button" onClick={clearAllFilters} className="h-10 px-2 text-[14px] text-ink-2 font-semibold cursor-pointer">
                Temizle
              </button>
              <button
                type="button"
                onClick={() => setFiltersOpen(false)}
                className="h-11 sm:h-10 px-5 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-[14.5px] font-semibold cursor-pointer"
              >
                {filteredQuestions.length.toLocaleString('tr-TR')} soruyu göster
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Active filters as removable chips */}
      {(activeFilterChips.length > 0 || searchQuery) && (
        <div className="flex flex-wrap items-center gap-1.5">
          {activeFilterChips.map((c) => (
            <button
              key={c.label}
              type="button"
              onClick={() => {
                c.clear();
                setCurrentPage(1);
              }}
              className="h-8 pl-3 pr-2 rounded-full bg-accent-soft text-accent text-[13px] font-semibold inline-flex items-center gap-1 cursor-pointer max-w-full"
              aria-label={`${c.label} filtresini kaldır`}
            >
              <span className="truncate">{c.label}</span>
              <X className="w-3.5 h-3.5 shrink-0" />
            </button>
          ))}
          <span className="ml-auto text-[13px] text-ink-3">{filteredQuestions.length.toLocaleString('tr-TR')} soru</span>
        </div>
      )}

      {/* Questions Listing */}
      {isLoading ? (
        <div className="bg-white rounded-[18px] border border-line p-12 text-center flex flex-col items-center gap-2">
          <RefreshCw className="w-6 h-6 text-accent animate-spin" />
          <p className="m-0 text-[14px] text-ink-2">Çıkmış sorular yükleniyor…</p>
        </div>
      ) : paginatedQuestions.length === 0 ? (
        <div className="bg-white rounded-[18px] border border-line px-6 py-12 text-center flex flex-col items-center gap-3">
          <HelpCircle className="w-9 h-9 text-ink-3" />
          <p className="m-0 font-display text-[20px] font-bold">Eşleşen soru yok</p>
          <p className="m-0 text-[14px] text-ink-2 max-w-sm">Aramayı ya da filtreleri değiştirip yeniden dene.</p>
          <button type="button" onClick={clearAllFilters} className="h-10 px-4 rounded-[10px] bg-accent-soft text-accent font-semibold text-[14px] cursor-pointer">
            Filtreleri temizle
          </button>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {paginatedQuestions.map((q) => {
            const effectiveMode: 'redacted' | 'raw' | 'split' = cardViewOverrides[q.id] || viewMode;
            const learnMatch = learnMatcher.getMatch(q);
            const slideMatch = getQuestionSlideMatch(q);
            const isLiked = (q.likedBy || []).includes(currentUser?.uid || 'anonim-std');

            const stem = q.reconstruction?.stem || q.fragments?.[0]?.text || q.topic;
            const options = q.reconstruction?.options || q.options || [];
            const correctAnswer = q.reconstruction?.correctAnswer || q.claimedAnswer;
            const explanation = q.reconstruction?.explanation;
            const commentsCount = (q as any).comments?.length || 0;
            const expOpen = !!openExplanations[q.id];
            const meta = [q.discipline || 'Tıp', formatCommitteeName(q.committeeId).split(':')[0], q.examYear].filter(Boolean).join(' · ');
            const setCardMode = (m: 'redacted' | 'raw' | 'split') => setCardViewOverrides((prev) => ({ ...prev, [q.id]: m }));

            const actions: ActionItem[] = [
              {
                label: isGeneratingSimilar === q.id ? 'Benzer soru üretiliyor…' : 'Benzer soru üret',
                icon: Sparkles,
                group: 'Yapay zekâ',
                tone: 'accent',
                disabled: isGeneratingSimilar === q.id,
                onClick: () => handleGenerateSimilarQuestion(q, learnMatch || slideMatch),
              },
              ...(isAdminUser
                ? [
                    { label: 'AI ile düzenle', icon: Wand2, group: 'Yapay zekâ', onClick: () => setOptimizeModalQuestion(q) },
                    {
                      label: 'AI ile redakte et',
                      icon: PenLine,
                      group: 'Yapay zekâ',
                      onClick: () => setCustomRedactQuestion({ question: q, match: learnMatch || slideMatch }),
                    },
                  ]
                : []),
              { label: 'Gelişmiş soruya çevir', icon: Zap, group: 'Yapay zekâ', onClick: () => setUpgradeModalQuestion(q) },
              { label: 'Düzenlenmiş', icon: Sparkles, group: 'Görünüm', hint: effectiveMode === 'redacted' ? '✓' : undefined, onClick: () => setCardMode('redacted') },
              { label: 'Ham metin', icon: FileText, group: 'Görünüm', hint: effectiveMode === 'raw' ? '✓' : undefined, onClick: () => setCardMode('raw') },
              { label: 'Karşılaştır', icon: Layers, group: 'Görünüm', hint: effectiveMode === 'split' ? '✓' : undefined, onClick: () => setCardMode('split') },
              ...(learnMatch
                ? [{ label: `Öğren · slayt ${learnMatch.slideNumber}`, icon: GraduationCap, group: 'Diğer', onClick: () => setSelectedLearnMatch({ question: q, match: learnMatch }) }]
                : []),
              { label: 'Kaynak dosyayı göster', icon: FileText, group: 'Diğer', onClick: () => setSelectedRawSourceQuestion(q) },
              { label: copiedId === q.id ? 'Kopyalandı' : 'Soruyu kopyala', icon: copiedId === q.id ? Check : Copy, group: 'Diğer', onClick: () => handleCopyQuestion(q) },
              { label: 'Hata bildir', icon: Flag, group: 'Diğer', tone: 'danger', onClick: () => setReportingQuestion(q) },
            ];

            return (
              <article key={q.id} className="bg-white rounded-[18px] border border-line p-4 sm:p-5 flex flex-col gap-3.5">
                <header className="flex items-center gap-2.5 min-w-0">
                  <span className="font-mono text-[13px] font-semibold text-ink shrink-0">#{q.questionNumber}</span>
                  <span className="text-[13px] text-ink-3 truncate min-w-0" title={formatCommitteeName(q.committeeId)}>
                    {meta}
                  </span>
                  {q.isAmbiguous ? (
                    <span className="h-[22px] px-2 rounded-full bg-warn-soft text-warn text-[12px] font-semibold inline-flex items-center shrink-0">Eksik</span>
                  ) : q.reconstruction ? (
                    <span className="hidden sm:inline-flex h-[22px] px-2 rounded-full bg-ok-soft text-ok text-[12px] font-semibold items-center shrink-0">Doğrulandı</span>
                  ) : null}
                  {isGeneratingSimilar === q.id && <RefreshCw className="w-4 h-4 text-accent animate-spin shrink-0" aria-label="Benzer soru üretiliyor" />}
                  <span className="flex-1" />
                  <ActionMenu items={actions} label="İşlemler" title={`Soru #${q.questionNumber}`} />
                </header>

                {effectiveMode === 'split' ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div className="bg-canvas rounded-[14px] p-3.5 flex flex-col gap-2">
                      <span className="text-[12px] font-semibold text-ink-3 uppercase tracking-[0.06em]">Ham metin</span>
                      <p className="m-0 text-[14.5px] text-ink leading-relaxed whitespace-pre-wrap">{q.fragments?.[0]?.text || stem}</p>
                      {q.options && q.options.length > 0 && (
                        <ol className="list-none m-0 p-0 flex flex-col gap-1 text-[14px] text-ink-2">
                          {q.options.map((opt) => (
                            <li key={opt.key} className="flex gap-2">
                              <span className="font-mono text-ink-3">{opt.key})</span>
                              <span>{opt.text}</span>
                            </li>
                          ))}
                        </ol>
                      )}
                    </div>
                    <div className="bg-accent-soft/50 rounded-[14px] p-3.5 flex flex-col gap-2">
                      <span className="text-[12px] font-semibold text-accent uppercase tracking-[0.06em]">Düzenlenmiş</span>
                      <p className="m-0 text-[14.5px] text-ink font-medium leading-relaxed">{stem}</p>
                      {options.length > 0 && (
                        <ol className="list-none m-0 p-0 flex flex-col gap-1 text-[14px]">
                          {options.map((opt: any) => (
                            <li key={opt.key} className={`flex gap-2 ${opt.key === correctAnswer ? 'text-ok font-semibold' : 'text-ink-2'}`}>
                              <span className="font-mono">{opt.key})</span>
                              <span>{opt.text}</span>
                            </li>
                          ))}
                        </ol>
                      )}
                    </div>
                  </div>
                ) : effectiveMode === 'raw' ? (
                  <div className="bg-canvas rounded-[14px] p-3.5 flex flex-col gap-2.5">
                    <span className="text-[12px] font-semibold text-ink-3 uppercase tracking-[0.06em]">Ham metin · {q.sourceFile || 'PDF kaynağı'}</span>
                    <p className="m-0 text-[15px] text-ink leading-relaxed whitespace-pre-wrap">
                      {(q as any).rawQuestion?.stem || q.fragments?.[0]?.text || q.rawStem || q.topic}
                    </p>
                    {(((q as any).rawQuestion?.options && (q as any).rawQuestion.options.length > 0) || (q.options && q.options.length > 0)) && (
                      <ol className="list-none m-0 p-0 flex flex-col gap-1">
                        {((q as any).rawQuestion?.options || q.options).map((opt: any) => {
                          const isClaimed = opt.key === (q.claimedAnswer || (q as any).rawQuestion?.claimedAnswer);
                          return (
                            <li key={opt.key} className={`flex gap-2 text-[14px] px-2 py-1 rounded-lg ${isClaimed ? 'bg-warn-soft text-ink font-semibold' : 'text-ink-2'}`}>
                              <span className="font-mono text-ink-3">{opt.key})</span>
                              <span className="flex-1">{opt.text}</span>
                              {isClaimed && <span className="text-[12px] text-warn">İşaretlenen</span>}
                            </li>
                          );
                        })}
                      </ol>
                    )}
                  </div>
                ) : (
                  <>
                    <p className="m-0 text-[16px] sm:text-[17px] font-medium text-ink leading-[1.5]">{stem}</p>
                    {options && options.length > 0 && (
                      <ol className="list-none m-0 p-0 flex flex-col gap-1.5">
                        {options.map((opt: any) => {
                          const isCorrect = opt.key === correctAnswer;
                          return (
                            <li
                              key={opt.key}
                              className={`grid grid-cols-[28px_minmax(0,1fr)_auto] items-center gap-2.5 px-3 py-2.5 rounded-[12px] border ${
                                isCorrect ? 'bg-ok-tint border-[#9FD9B5]' : 'bg-white border-line-soft'
                              }`}
                            >
                              <span
                                className={`w-7 h-7 rounded-[8px] flex items-center justify-center font-mono text-[13px] font-semibold ${
                                  isCorrect ? 'bg-ok text-white' : 'bg-canvas text-ink-2'
                                }`}
                              >
                                {opt.key}
                              </span>
                              <span className={`text-[14.5px] leading-[1.45] ${isCorrect ? 'font-semibold text-ink' : 'text-ink'}`}>{opt.text}</span>
                              {isCorrect ? <span className="text-[12px] font-semibold text-ok">Doğru</span> : <span />}
                            </li>
                          );
                        })}
                      </ol>
                    )}
                    {explanation && (
                      <div className="rounded-[12px] bg-field">
                        <button
                          type="button"
                          onClick={() => setOpenExplanations((prev) => ({ ...prev, [q.id]: !prev[q.id] }))}
                          aria-expanded={expOpen}
                          className="w-full h-11 px-3.5 flex items-center justify-between text-[14px] font-semibold text-ink cursor-pointer"
                        >
                          Açıklama
                          <ChevronDown className={`w-4 h-4 text-ink-3 transition-transform ${expOpen ? 'rotate-180' : ''}`} />
                        </button>
                        {expOpen && <p className="m-0 px-3.5 pb-3.5 text-[14.5px] text-ink-2 leading-[1.6] whitespace-pre-line">{explanation}</p>}
                      </div>
                    )}
                  </>
                )}

                {/* Footer: like, comments, learn link */}
                <footer className="flex items-center gap-2 text-[13px] text-ink-3">
                  <button
                    type="button"
                    onClick={() => handleToggleLike(q)}
                    aria-pressed={isLiked}
                    title={isLiked ? 'Beğeniyi geri al' : 'Soruyu beğen'}
                    className={`h-8 px-2.5 rounded-[9px] border inline-flex items-center gap-1.5 cursor-pointer transition-colors ${
                      isLiked ? 'bg-accent-soft border-accent/30 text-accent font-semibold' : 'bg-white border-line text-ink-2 hover:border-line-2'
                    }`}
                  >
                    <ThumbsUp className={`w-3.5 h-3.5 ${isLiked ? 'fill-current' : ''}`} />
                    {q.upvotes || 0}
                  </button>
                  <button
                    type="button"
                    onClick={() => setExpandedCommentsQuestionId(expandedCommentsQuestionId === q.id ? null : q.id)}
                    aria-expanded={expandedCommentsQuestionId === q.id}
                    className={`h-8 px-2.5 rounded-[9px] inline-flex items-center gap-1.5 cursor-pointer ${
                      expandedCommentsQuestionId === q.id ? 'bg-canvas text-ink font-semibold' : 'text-ink-2 hover:bg-canvas'
                    }`}
                  >
                    <MessageSquare className="w-3.5 h-3.5" />
                    {commentsCount > 0 ? `${commentsCount} yorum` : 'Yorum'}
                  </button>
                  <span className="flex-1" />
                  {learnMatch && (
                    <button
                      type="button"
                      onClick={() => setSelectedLearnMatch({ question: q, match: learnMatch })}
                      title={`${learnMatch.deckTitle} · slayt ${learnMatch.slideNumber}`}
                      className="h-8 px-2.5 rounded-[9px] inline-flex items-center gap-1.5 text-accent font-semibold hover:bg-accent-soft cursor-pointer min-w-0"
                    >
                      <GraduationCap className="w-4 h-4 shrink-0" />
                      <span className="truncate max-w-[180px] sm:max-w-[260px]">Öğren · slayt {learnMatch.slideNumber}</span>
                    </button>
                  )}
                </footer>

                {expandedCommentsQuestionId === q.id && (
                  <div className="bg-field rounded-[14px] p-3 flex flex-col gap-2.5">
                    <div className="flex flex-col gap-2 max-h-56 overflow-y-auto">
                      {commentsCount > 0 ? (
                        (q as any).comments.map((c: any) => (
                          <div key={c.id} className="bg-white border border-line-soft rounded-[10px] px-3 py-2 flex flex-col gap-0.5">
                            <div className="flex items-center justify-between gap-2 text-[12px] text-ink-3">
                              <span className="font-semibold text-ink">{c.author || 'Tıp öğrencisi'}</span>
                              <span>{new Date(c.timestamp).toLocaleDateString('tr-TR')}</span>
                            </div>
                            <p className="m-0 text-[14px] text-ink-2 leading-relaxed">{c.text}</p>
                          </div>
                        ))
                      ) : (
                        <p className="m-0 text-[14px] text-ink-3">Henüz yorum yok. Bir ipucu ya da alternatif çözüm ekleyen ilk kişi ol.</p>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <input
                        type="text"
                        value={newCommentText}
                        onChange={(e) => setNewCommentText(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') handleCommentSubmit(q.id);
                        }}
                        placeholder="Yorum ya da ipucu yaz…"
                        aria-label="Yorum"
                        className="flex-1 min-w-0 h-10 bg-white border border-line rounded-[10px] px-3 text-[15px] outline-0 focus:border-accent"
                      />
                      <button
                        type="button"
                        onClick={() => handleCommentSubmit(q.id)}
                        disabled={isSubmittingComment || !newCommentText.trim()}
                        aria-label="Gönder"
                        className="w-10 h-10 rounded-[10px] bg-accent text-white flex items-center justify-center disabled:opacity-50 cursor-pointer shrink-0"
                      >
                        <Send className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                )}
              </article>
            );
          })}

          {totalPages > 1 && (
            <nav aria-label="Sayfalar" className="flex items-center justify-between gap-2 pt-2 text-[14px]">
              <button
                type="button"
                onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
                disabled={currentPage === 1}
                className="h-10 px-3 rounded-[10px] border border-line bg-white inline-flex items-center gap-1 font-semibold disabled:opacity-40 cursor-pointer"
              >
                <ChevronLeft className="w-4 h-4" />
                <span className="hidden sm:inline">Önceki</span>
              </button>
              <span className="text-ink-3">
                <span className="font-semibold text-ink">{currentPage}</span> / {totalPages}
              </span>
              <button
                type="button"
                onClick={() => setCurrentPage((prev) => Math.min(totalPages, prev + 1))}
                disabled={currentPage === totalPages}
                className="h-10 px-3 rounded-[10px] border border-line bg-white inline-flex items-center gap-1 font-semibold disabled:opacity-40 cursor-pointer"
              >
                <span className="hidden sm:inline">Sonraki</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </nav>
          )}
        </div>
      )}

      {/* Öğren Modülü / İnteraktif Amfi Slaytı Eşleşmesi Modal */}
      {selectedLearnMatch && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl max-w-2xl w-full shadow-2xl border border-slate-200 overflow-hidden space-y-4 my-6 animate-fade-in flex flex-col max-h-[88vh]">
            {/* Modal Header */}
            <div className="bg-gradient-to-r from-emerald-900 via-teal-900 to-slate-900 text-white p-4 sm:p-5 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-400/30 flex items-center justify-center text-emerald-300">
                  <GraduationCap className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-sm sm:text-base flex items-center gap-2">
                    <span>{selectedLearnMatch.match.deckTitle}</span>
                    <span className="text-[11px] bg-emerald-500/30 text-emerald-200 px-2 py-0.5 rounded-full font-mono">
                      Slayt #{selectedLearnMatch.match.slideNumber}
                    </span>
                  </h4>
                  <p className="text-xs text-slate-300">
                    {selectedLearnMatch.match.discipline} • {selectedLearnMatch.match.committee}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setSelectedLearnMatch(null)}
                className="text-slate-300 hover:text-white p-1 rounded-lg hover:bg-white/10 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-4 sm:p-6 overflow-y-auto space-y-4 flex-1 text-xs">
              {/* Question Context Banner */}
              <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3 text-emerald-900 space-y-1">
                <div className="flex items-center justify-between">
                  <strong className="block font-bold">
                    Çıkmış Soru: #{selectedLearnMatch.question.questionNumber} - {selectedLearnMatch.question.topic || selectedLearnMatch.question.discipline}
                  </strong>
                  <span className="text-[10px] font-semibold bg-emerald-200/80 text-emerald-900 px-2 py-0.5 rounded">
                    {selectedLearnMatch.match.matchType === 'direct' ? '✓ Müfredat Eşleşmesi' : '%90+ Konu Eşleşmesi'}
                  </span>
                </div>
                <p className="text-[11px] text-emerald-800 leading-relaxed">
                  Bu soru, Öğren modülündeki <strong>"{selectedLearnMatch.match.deckTitle}"</strong> dersinin <strong>#{selectedLearnMatch.match.slideNumber}</strong> numaralı interaktif amfi slaytına ve akıl kartlarına bağlanmıştır.
                </p>
              </div>

              {/* Slide Title & Badge */}
              <div className="space-y-1 border-b border-slate-100 pb-3">
                <span className="bg-teal-100 text-teal-800 text-[11px] font-bold px-2 py-0.5 rounded-md inline-block">
                  {selectedLearnMatch.match.badge}
                </span>
                <h5 className="font-bold text-slate-900 text-sm">
                  {selectedLearnMatch.match.slideTitle}
                </h5>
              </div>

              {/* Synthesis Narrative (Ders Sentezi) */}
              {selectedLearnMatch.match.synthesisNarrative && (
                <div className="space-y-2">
                  <span className="text-[11px] font-bold text-slate-500 block">Amfi ve Ders Notu Sentezi:</span>
                  <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs sm:text-sm font-sans text-slate-900 leading-relaxed max-h-56 overflow-y-auto whitespace-pre-wrap">
                    {selectedLearnMatch.match.synthesisNarrative}
                  </div>
                </div>
              )}

              {/* Spot Pearls */}
              {selectedLearnMatch.match.spotPearls && selectedLearnMatch.match.spotPearls.length > 0 && (
                <div className="space-y-2">
                  <span className="text-[11px] font-bold text-amber-800 flex items-center gap-1">
                    <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                    Sınav İçin Spot Hap Bilgiler:
                  </span>
                  <div className="bg-amber-50/60 border border-amber-200 rounded-xl p-3 space-y-1.5">
                    {selectedLearnMatch.match.spotPearls.map((pearl, i) => (
                      <div key={i} className="flex items-start gap-1.5 text-slate-800 text-xs">
                        <span className="text-amber-600 font-bold shrink-0">•</span>
                        <span>{pearl}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Flashcards (Akıl Kartları) */}
              {selectedLearnMatch.match.flashcards && selectedLearnMatch.match.flashcards.length > 0 && (
                <div className="space-y-2">
                  <span className="text-[11px] font-bold text-slate-600 flex items-center gap-1">
                    <BookOpen className="w-3.5 h-3.5 text-slate-500" />
                    İlgili 3D Akıl Kartları ({selectedLearnMatch.match.flashcards.length}):
                  </span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    {selectedLearnMatch.match.flashcards.map((card) => (
                      <FlashcardComponent key={card.id} card={card} />
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="bg-slate-50 border-t border-slate-200 p-4 flex items-center justify-between shrink-0 text-xs">
              <button
                onClick={() => setSelectedLearnMatch(null)}
                className="px-4 py-2 rounded-xl text-slate-600 font-semibold hover:bg-slate-200 cursor-pointer"
              >
                Kapat
              </button>

              {onNavigateToLearn && (
                <button
                  onClick={() => {
                    const dId = selectedLearnMatch.match.deckId;
                    const sNum = selectedLearnMatch.match.slideNumber;
                    setSelectedLearnMatch(null);
                    onNavigateToLearn(dId, sNum);
                  }}
                  className="bg-emerald-700 hover:bg-emerald-800 text-white font-bold px-4 py-2 rounded-xl flex items-center gap-1.5 cursor-pointer shadow-xs transition-colors"
                >
                  <GraduationCap className="w-4 h-4" />
                  <span>Öğren Sayfasında Tam Ekran Aç</span>
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Ham Sorunun Bulunduğu Yer (Arşiv Konumu) Modal */}
      {selectedRawSourceQuestion && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl max-w-2xl w-full shadow-2xl border border-slate-200 overflow-hidden space-y-4 my-6 animate-fade-in flex flex-col max-h-[85vh]">
            {/* Modal Header */}
            <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white p-4 sm:p-5 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-slate-700 flex items-center justify-center text-slate-200">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-sm sm:text-base">
                    Ham Soru Arşiv Konumu & Orijinal Belge
                  </h4>
                  <p className="text-xs text-slate-400">
                    {selectedRawSourceQuestion.discipline || 'Tıp'} • {formatCommitteeName(selectedRawSourceQuestion.committeeId)}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setSelectedRawSourceQuestion(null)}
                className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-4 sm:p-6 overflow-y-auto space-y-4 flex-1 text-xs">
              {/* Source Location Details */}
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2.5">
                <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                  <span className="font-bold text-slate-500 text-[11px] uppercase tracking-wider">Orijinal Sınav Dosyası:</span>
                  <span className="font-mono text-xs font-bold text-slate-900 bg-white border border-slate-200 px-2 py-0.5 rounded max-w-[280px] truncate" title={selectedRawSourceQuestion.sourceFile || selectedRawSourceQuestion.sourceNote}>
                    {selectedRawSourceQuestion.sourceFile || selectedRawSourceQuestion.sourceNote || 'Geçmiş Kurul Arşivi'}
                  </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-1 text-xs">
                  <div className="bg-white border border-slate-200 rounded-lg p-2.5">
                    <span className="text-[10px] text-slate-400 font-semibold block">Sınav Yılı / Dönem</span>
                    <strong className="text-slate-800 font-bold">{selectedRawSourceQuestion.examYear || 'Arşiv'}</strong>
                  </div>
                  <div className="bg-white border border-slate-200 rounded-lg p-2.5">
                    <span className="text-[10px] text-slate-400 font-semibold block">Soru Numarası</span>
                    <strong className="text-slate-800 font-bold">Soru #{selectedRawSourceQuestion.questionNumber}</strong>
                  </div>
                  <div className="bg-white border border-slate-200 rounded-lg p-2.5 col-span-2 sm:col-span-1">
                    <span className="text-[10px] text-slate-400 font-semibold block">Belge İçi Sayfa</span>
                    <strong className="text-slate-800 font-bold">
                      {selectedRawSourceQuestion.matchedSlidePage ? `Sayfa #${selectedRawSourceQuestion.matchedSlidePage}` : 'Arşiv Kitapçığı'}
                    </strong>
                  </div>
                </div>

                <p className="text-[11px] text-slate-500 italic pt-1">
                  📌 Bu soru henüz doğrudan bir amfi slaytına bağlanmamıştır; tıp fakültesi geçmiş kurul sınav kitapçığından ve öğrenci hafıza parçalarından derlenmiştir. Orijinal sınav kitapçığındaki konumu gösterilmektedir.
                </p>
              </div>

              {/* Raw Question Stem */}
              <div className="space-y-2">
                <span className="text-[11px] font-bold text-slate-700 block">Orijinal Ham Soru Metni:</span>
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs sm:text-sm font-serif text-slate-900 leading-relaxed whitespace-pre-wrap">
                  {selectedRawSourceQuestion.rawStem ||
                   selectedRawSourceQuestion.rawQuestion?.stem ||
                   selectedRawSourceQuestion.fragments?.[0]?.text ||
                   selectedRawSourceQuestion.stem ||
                   selectedRawSourceQuestion.topic}
                </div>
              </div>

              {/* Options */}
              <div className="space-y-2">
                <span className="text-[11px] font-bold text-slate-700 block">Seçenekler:</span>
                <div className="space-y-1.5">
                  {(selectedRawSourceQuestion.rawQuestion?.options || selectedRawSourceQuestion.options || []).map((opt: any, i: number) => {
                    const key = typeof opt === 'string' ? String.fromCharCode(65 + i) : opt.key;
                    const text = typeof opt === 'string' ? opt : opt.text;
                    const isCorrect = key === (selectedRawSourceQuestion.correctAnswer || selectedRawSourceQuestion.claimedAnswer);
                    return (
                      <div
                        key={key}
                        className={`p-2.5 rounded-lg border text-xs flex items-start gap-2 ${
                          isCorrect
                            ? 'bg-emerald-50 border-emerald-300 text-emerald-950 font-semibold'
                            : 'bg-white border-slate-200 text-slate-700'
                        }`}
                      >
                        <span className={`w-5 h-5 rounded flex items-center justify-center font-bold text-[11px] shrink-0 ${
                          isCorrect ? 'bg-emerald-700 text-white' : 'bg-slate-100 text-slate-600'
                        }`}>
                          {key}
                        </span>
                        <span className="flex-1 leading-snug">{text}</span>
                        {isCorrect && (
                          <span className="text-[10px] font-bold text-emerald-700 bg-emerald-100 px-1.5 py-0.5 rounded">
                            Cevap
                          </span>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="bg-slate-50 border-t border-slate-200 p-4 flex items-center justify-between shrink-0 text-xs">
              <button
                onClick={() => setSelectedRawSourceQuestion(null)}
                className="px-4 py-2 rounded-xl text-slate-600 font-semibold hover:bg-slate-200 cursor-pointer"
              >
                Kapat
              </button>

              <span className="text-slate-400 text-[11px]">
                Fakülte Kurul Sınavı Arşivi
              </span>
            </div>
          </div>
        </div>
      )}

      {/* AI Generated Similar Practice Question Modal ("Ek Soru Sor") */}
      {similarModalQuestion && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-2xl w-full shadow-2xl border border-slate-200 overflow-hidden space-y-4 my-6 animate-fade-in flex flex-col max-h-[90vh]">
            {/* Modal Header */}
            <div className="bg-gradient-to-r from-teal-900 to-slate-900 text-white p-4 sm:p-5 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-2.5">
                <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-300 border border-teal-500/30 flex items-center justify-center">
                  <Sparkles className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-sm sm:text-base">Yapay Zeka Destekli Ek Pratik Sorusu</h4>
                  <p className="text-xs text-teal-300">
                    {similarModalQuestion.discipline} • {similarModalQuestion.topic}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setSimilarModalQuestion(null)}
                className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-white/10 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-4 sm:p-6 overflow-y-auto space-y-4 flex-1 text-xs sm:text-sm">
              {/* Origin Badges */}
              <div className="flex flex-wrap items-center gap-2 p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs">
                <span className="bg-white border border-slate-300 text-slate-700 px-2 py-1 rounded-md font-semibold flex items-center gap-1">
                  <FileText className="w-3.5 h-3.5 text-slate-500" />
                  Orijinal Çıkmış: {similarModalQuestion.sourceExamPdf}
                </span>
                {similarModalQuestion.matchedNoteTitle && (
                  <span className="bg-emerald-50 border border-emerald-300 text-emerald-900 px-2 py-1 rounded-md font-semibold flex items-center gap-1">
                    <BookMarked className="w-3.5 h-3.5 text-emerald-600" />
                    Ders: {similarModalQuestion.matchedNoteTitle} (Slayt #{similarModalQuestion.matchedSlidePage})
                  </span>
                )}
              </div>

              {(similarModalQuestion.lectureReference?.matchedSnippet || similarModalQuestion.matchedSnippet) && (
                <div className="p-3 bg-amber-50/70 border border-amber-200 rounded-xl text-xs text-amber-950">
                  <div className="font-bold flex items-center gap-1.5 mb-1 text-amber-900">
                    <BookOpen className="w-3.5 h-3.5 text-amber-700" />
                    Slayttaki İlgili Bilgi & Metin:
                  </div>
                  <p className="leading-relaxed">
                    {renderHighlightedSnippet(similarModalQuestion.lectureReference?.matchedSnippet || similarModalQuestion.matchedSnippet)}
                  </p>
                </div>
              )}

              {/* Question Stem */}
              <div className="space-y-2">
                <span className="text-xs font-bold text-slate-500 block">Soru Metni:</span>
                <p className="font-medium text-slate-900 leading-relaxed bg-teal-50/40 p-4 rounded-xl border border-teal-200 whitespace-pre-wrap">
                  {similarModalQuestion.stem}
                </p>
              </div>

              {/* Options */}
              <div className="space-y-2 pt-2">
                <span className="text-xs font-bold text-slate-500 block">Seçenekler:</span>
                <div className="space-y-2">
                  {similarModalQuestion.options.map((opt: any) => {
                    const isCorrect = opt.key === similarModalQuestion.correctAnswer;
                    return (
                      <div
                        key={opt.key}
                        className={`p-3 rounded-xl border flex items-start justify-between gap-3 ${
                          isCorrect
                            ? 'bg-emerald-50 border-emerald-400 text-emerald-950 font-bold'
                            : 'bg-white border-slate-200 text-slate-700'
                        }`}
                      >
                        <div className="flex items-start gap-2.5">
                          <span className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${
                            isCorrect ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-700'
                          }`}>
                            {opt.key}
                          </span>
                          <span>{opt.text}</span>
                        </div>
                        {isCorrect && (
                          <span className="text-[10px] bg-emerald-200 text-emerald-900 px-2 py-0.5 rounded font-extrabold uppercase shrink-0">
                            ✓ Doğru Cevap
                          </span>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Clinical Explanation */}
              {similarModalQuestion.explanation && (
                <div className="bg-teal-50 border border-teal-200 rounded-xl p-4 text-xs space-y-1">
                  <div className="flex items-center gap-1.5 font-bold text-teal-900">
                    <CheckCircle2 className="w-4 h-4 text-teal-700" />
                    <span>Patofizyolojik & Klinik Gerekçe:</span>
                  </div>
                  <p className="text-slate-700 leading-relaxed pl-5">
                    {similarModalQuestion.explanation}
                  </p>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="bg-slate-50 border-t border-slate-200 p-4 flex items-center justify-between shrink-0 text-xs">
              <button
                onClick={() => setSimilarModalQuestion(null)}
                className="px-4 py-2 rounded-xl text-slate-600 font-semibold hover:bg-slate-200 cursor-pointer"
              >
                Kapat
              </button>

              <button
                onClick={() => {
                  const text = `[MedSoru Ek Pratik Sorusu - ${similarModalQuestion.discipline}]\n\n${similarModalQuestion.stem}\n\n${similarModalQuestion.options.map((o: any) => `${o.key}) ${o.text}`).join('\n')}\n\nDoğru Cevap: ${similarModalQuestion.correctAnswer}\n\nAçıklama: ${similarModalQuestion.explanation}`;
                  navigator.clipboard.writeText(text);
                  alert('Ek soru panoya kopyalandı!');
                }}
                className="bg-teal-700 hover:bg-teal-800 text-white font-bold px-4 py-2 rounded-xl flex items-center gap-1.5 cursor-pointer shadow-xs"
              >
                <Copy className="w-3.5 h-3.5 text-teal-200" />
                <span>Soruyu Kopyala</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Question Report / Complaint Modal */}
      {reportingQuestion && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[90vh]">
            <div className="bg-slate-900 text-white p-4 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-2">
                <Flag className="w-5 h-5 text-rose-400" />
                <div>
                  <h3 className="font-bold text-sm">Soru Hata Bildirimi & Şikayet</h3>
                  <p className="text-[11px] text-slate-400">
                    Soru #{reportingQuestion.questionNumber} - {reportingQuestion.discipline} ({reportingQuestion.examYear})
                  </p>
                </div>
              </div>
              <button
                onClick={() => setReportingQuestion(null)}
                className="p-1 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-5 space-y-4 overflow-y-auto text-xs">
              {reportSuccessMsg ? (
                <div className="bg-emerald-50 border border-emerald-300 rounded-xl p-4 text-emerald-950 flex items-center gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
                  <p className="font-bold">{reportSuccessMsg}</p>
                </div>
              ) : (
                <>
                  <div className="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1">
                    <span className="text-[11px] font-bold text-slate-500">Bildirilen Soru Kökü:</span>
                    <p className="text-slate-800 font-medium line-clamp-2">
                      {reportingQuestion.reconstruction?.stem || reportingQuestion.rawQuestion?.stem || reportingQuestion.topic}
                    </p>
                  </div>

                  <div className="space-y-1.5">
                    <label className="font-bold text-slate-700">Şikayet / Bildirim Türü:</label>
                    <select
                      value={reportReason}
                      onChange={(e) => setReportReason(e.target.value)}
                      className="w-full bg-slate-50 border border-slate-300 rounded-xl p-2.5 text-xs font-semibold text-slate-900 focus:bg-white focus:outline-teal-600"
                    >
                      <option value="Hatalı Soru Kökü">Hatalı veya Eksik Soru Kökü</option>
                      <option value="Yanlış / Eksik Şıklar">Eksik veya Yanlış Seçenekler</option>
                      <option value="Hatalı Doğru Cevap">Hatalı Doğru Cevap Anahtarı</option>
                      <option value="Hatalı Branş / Kurul Eşleşmesi">Hatalı Branş veya Kurul Eşleşmesi</option>
                      <option value="Yapay Zeka Redaksiyon Hatası">Yapay Zeka Redaksiyonu Yetersiz / Hatalı</option>
                      <option value="Diğer">Diğer Sorun / İtiraz</option>
                    </select>
                  </div>

                  <div className="space-y-1.5">
                    <label className="font-bold text-slate-700">Detaylı Açıklama veya Düzeltme Öneriniz (Opsiyonel):</label>
                    <textarea
                      value={reportDetails}
                      onChange={(e) => setReportDetails(e.target.value)}
                      rows={3}
                      placeholder="Örn: Bu sorunun cevabı C şıkkı olmalı çünkü hoca slayt 12'de amiloidozis ile ilişkisini vurgulamıştı..."
                      className="w-full bg-slate-50 border border-slate-300 rounded-xl p-2.5 text-xs text-slate-900 focus:bg-white focus:outline-teal-600"
                    />
                  </div>
                </>
              )}
            </div>

            {!reportSuccessMsg && (
              <div className="bg-slate-50 border-t border-slate-200 p-4 flex items-center justify-between shrink-0 text-xs">
                <button
                  onClick={() => setReportingQuestion(null)}
                  className="px-4 py-2 rounded-xl text-slate-600 font-semibold hover:bg-slate-200 cursor-pointer"
                >
                  İptal
                </button>
                <button
                  onClick={handleReportSubmit}
                  disabled={isSubmittingReport}
                  className="bg-rose-600 hover:bg-rose-700 disabled:opacity-50 text-white font-bold px-4 py-2 rounded-xl flex items-center gap-1.5 cursor-pointer shadow-xs"
                >
                  <Flag className="w-3.5 h-3.5" />
                  <span>{isSubmittingReport ? 'İletiliyor...' : 'Şikayeti İlet'}</span>
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Admin AI Question Optimizer Modal */}
      {(currentUser?.email === ADMIN_EMAIL || currentUser?.isAdmin) && optimizeModalQuestion && (
        <AiQuestionOptimizerModal
          question={optimizeModalQuestion}
          isOpen={Boolean(optimizeModalQuestion)}
          onClose={() => setOptimizeModalQuestion(null)}
          currentUser={currentUser}
          onSaved={(updated) => {
            setQuestions(prev => prev.map(q => q.id === updated.id ? updated : q));
            setOptimizeModalQuestion(null);
          }}
          onOpenSlideReader={(note, pageNum) => {
            if (onOpenNote && note?.id) {
              onOpenNote(note.id, pageNum);
            }
          }}
        />
      )}

      {/* Admin Custom AI Redaction Modal */}
      {(currentUser?.email === ADMIN_EMAIL || currentUser?.isAdmin) && customRedactQuestion && (
        <AdminCustomRedactModal
          question={customRedactQuestion.question}
          isOpen={Boolean(customRedactQuestion)}
          onClose={() => setCustomRedactQuestion(null)}
          onSaved={(updated) => {
            setQuestions(prev => prev.map(q => q.id === updated.id ? updated : q));
            setCustomRedactQuestion(null);
          }}
          matchedSlideNote={customRedactQuestion.match ? {
            noteTitle: customRedactQuestion.match.note.title,
            pageNumber: customRedactQuestion.match.page.pageNumber,
            snippet: customRedactQuestion.match.page.content.substring(0, 300)
          } : null}
        />
      )}

      {/* Advanced Question Upgrade Modal */}
      {upgradeModalQuestion && (
        <AdvancedQuestionUpgradeModal
          question={upgradeModalQuestion}
          isOpen={Boolean(upgradeModalQuestion)}
          onClose={() => setUpgradeModalQuestion(null)}
          onSaveUpgraded={(questionId, advancedData) => {
            setQuestions(prev => prev.map(q => q.id === questionId ? { ...q, advancedQuestion: advancedData, hasAdvancedVersion: true } : q));
          }}
        />
      )}
    </div>
  );
};
