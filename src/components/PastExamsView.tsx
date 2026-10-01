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
  AlertCircle
} from 'lucide-react';
import { QuestionItem, LectureNote, LectureNotePage, QuestionLectureMatch } from '../types';
import { AppUser } from '../services/auth';
import { ApiService } from '../services/api';

interface PastExamsViewProps {
  currentUser: AppUser | null;
  lectureNotes?: LectureNote[];
  onOpenNote?: (noteId: string, pageNumber?: number) => void;
  onUpdateQuestionReference?: (questionId: string, match: QuestionLectureMatch) => Promise<void>;
}

export const PastExamsView: React.FC<PastExamsViewProps> = ({
  currentUser,
  lectureNotes = [],
  onOpenNote,
  onUpdateQuestionReference,
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
  const [ambiguityTab, setAmbiguityTab] = useState<'valid' | 'ambiguous' | 'all'>('valid');
  
  // Per-question card override: questionId -> 'redacted' | 'raw' | 'split'
  const [cardViewOverrides, setCardViewOverrides] = useState<Record<string, 'redacted' | 'raw' | 'split'>>({});
  
  // Selected slide snippet modal
  const [selectedSlideSnippet, setSelectedSlideSnippet] = useState<{
    note: LectureNote;
    page: LectureNotePage;
    question: QuestionItem;
    score: number;
  } | null>(null);

  // AI Similar Question Modal State
  const [similarModalQuestion, setSimilarModalQuestion] = useState<any | null>(null);
  const [isGeneratingSimilar, setIsGeneratingSimilar] = useState<string | null>(null);

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

  // Load questions
  const loadPastQuestions = async () => {
    setIsLoading(true);
    try {
      const data = await ApiService.getPastQuestions();
      setQuestions(data.filter(q => !q.id?.startsWith('civan-') && !q.tags?.some(t => /civan/i.test(t))));
    } catch (e) {
      console.warn('Could not load past questions:', e);
    } finally {
      setIsLoading(false);
    }
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
    ApiService.getLectureNotes()
      .then(notes => {
        if (notes && notes.length > 0) setInternalNotes(notes);
      })
      .catch(err => console.warn('Could not fetch lecture notes for past exams:', err));
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
    if (cId === 'donem3-kurul1') return 'Dönem 3 Kurul 1';
    if (cId === 'donem3-kurul2') return 'Dönem 3 Kurul 2';
    if (cId === 'donem3-kurul3') return 'Dönem 3 Kurul 3';
    if (cId === 'donem3-kurul4') return 'Dönem 3 Kurul 4';
    if (cId === 'donem3-kurul5') return 'Dönem 3 Kurul 5';
    if (cId === 'donem3-kurul6') return 'Dönem 3 Kurul 6';
    if (cId === 'donem3-final') return 'Dönem 3 Final Sınavı';
    if (cId === 'donem3-butunleme') return 'Dönem 3 Bütünleme';
    return cId;
  };

  return (
    <div className="space-y-6 animate-fade-in pb-12">
      {/* Top Hero Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-teal-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl border border-teal-800/60 relative overflow-hidden">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-radial from-teal-500/10 to-transparent pointer-events-none" />
        
        <div className="max-w-3xl space-y-3 relative z-10">
          <div className="flex flex-wrap items-center gap-2">
            <span className="bg-teal-500/20 text-teal-300 border border-teal-400/30 text-xs font-bold px-3 py-1 rounded-full flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-teal-300" />
              Tıp Fakültesi Çıkmış Sınav Soruları Arşivi
            </span>
            <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-xs font-bold px-3 py-1 rounded-full">
              {tabCounts.validCount.toLocaleString('tr-TR')} Tam Metin Soru
            </span>
            <span className="bg-amber-500/20 text-amber-300 border border-amber-400/30 text-xs font-bold px-3 py-1 rounded-full">
              {tabCounts.ambiguousCount.toLocaleString('tr-TR')} Muallak / İnceleme Bekleyen
            </span>
          </div>

          <h2 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
            Geçmiş Kurul ve Final Çıkmış Soruları
          </h2>
          <p className="text-sm text-slate-300 leading-relaxed">
            Dönem 3 kurul sınavlarında çıkmış sorular ve yerel meds_sorular arşivinden taranan sınav soruları. 
            Soruların hem <strong className="text-teal-300">orijinal ham metinlerini</strong> hem de yapay zeka ile <strong className="text-teal-300">redakte edilmiş 5 şıklı & gerekçeli</strong> versiyonlarını inceleyebilir, amfi ders slaytlarıyla eşleştirilmiş referansları tek tıkla görüntüleyebilir ve "Ek Soru Sor" butonu ile yeni deneme soruları üretebilirsiniz.
          </p>
        </div>

        {/* Global Statistics Cards */}
        <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 pt-5 border-t border-white/10 text-xs">
          <div className="bg-white/5 backdrop-blur-xs p-3 rounded-2xl border border-white/10">
            <span className="text-slate-400 block text-[11px]">Kaliteli Tam Sorular</span>
            <strong className="text-lg font-black text-white">{tabCounts.validCount} Soru</strong>
          </div>
          <div className="bg-white/5 backdrop-blur-xs p-3 rounded-2xl border border-white/10">
            <span className="text-slate-400 block text-[11px]">Filtrelenen Sonuç</span>
            <strong className="text-lg font-black text-teal-300">{filteredQuestions.length} Soru</strong>
          </div>
          <div className="bg-white/5 backdrop-blur-xs p-3 rounded-2xl border border-white/10">
            <span className="text-slate-400 block text-[11px]">Ders Slayt Eşleşmesi</span>
            <strong className="text-lg font-black text-emerald-300">
              {lectureNotes.length} Slayt Hazır
            </strong>
          </div>
          <div className="bg-white/5 backdrop-blur-xs p-3 rounded-2xl border border-white/10">
            <span className="text-slate-400 block text-[11px]">Görünüm Modu</span>
            <strong className="text-lg font-black text-amber-300 capitalize">
              {viewMode === 'redacted' ? 'Yapay Zeka Redakte' : viewMode === 'raw' ? 'Ham Metin' : 'İkili Karşılaştır'}
            </strong>
          </div>
        </div>
      </div>

      {/* Filter and Control Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-4 sm:p-5 shadow-xs space-y-4">
        {/* Search & View Mode Switch */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setCurrentPage(1);
              }}
              placeholder="Çıkmış soru metni, şık, branş, konu, dosya adı veya yıl ara..."
              className="w-full pl-10 pr-4 py-2.5 text-xs sm:text-sm bg-slate-50 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-400 focus:bg-white focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 transition-all"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 p-1 cursor-pointer"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* View Mode Toggle */}
          <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl shrink-0 self-start sm:self-auto text-xs font-bold">
            <button
              onClick={() => setViewMode('redacted')}
              className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all cursor-pointer ${
                viewMode === 'redacted'
                  ? 'bg-white text-teal-800 shadow-2xs font-extrabold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
              title="Yapay zeka tarafından temizlenmiş, şıklandırılmış ve gerekçeli soru görünümü"
            >
              <Sparkles className="w-3.5 h-3.5 text-teal-600" />
              <span>Redakte Edilmiş</span>
            </button>

            <button
              onClick={() => setViewMode('raw')}
              className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all cursor-pointer ${
                viewMode === 'raw'
                  ? 'bg-white text-teal-800 shadow-2xs font-extrabold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
              title="Öğrencilerin sınav sonrası hatırladığı orijinal ham metinler"
            >
              <FileText className="w-3.5 h-3.5 text-slate-500" />
              <span>Ham Orijinal</span>
            </button>

            <button
              onClick={() => setViewMode('split')}
              className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all cursor-pointer ${
                viewMode === 'split'
                  ? 'bg-white text-teal-800 shadow-2xs font-extrabold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
              title="Ham soru ile Redakte soruyu yan yana karşılaştır"
            >
              <Layers className="w-3.5 h-3.5 text-purple-600" />
              <span>Karşılaştır</span>
            </button>
          </div>
        </div>

        {/* Quality & Ambiguity Filter Pills */}
        <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-100">
          <span className="text-[11px] font-bold text-slate-500">Soru Havuzu:</span>
          <button
            onClick={() => { setAmbiguityTab('valid'); setCurrentPage(1); }}
            className={`px-3 py-1 rounded-full text-xs font-bold transition-all cursor-pointer ${
              ambiguityTab === 'valid'
                ? 'bg-emerald-600 text-white shadow-xs'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
            }`}
          >
            ✓ Tam Metin Soru Havuzu ({tabCounts.validCount})
          </button>
          <button
            onClick={() => { setAmbiguityTab('ambiguous'); setCurrentPage(1); }}
            className={`px-3 py-1 rounded-full text-xs font-bold transition-all cursor-pointer ${
              ambiguityTab === 'ambiguous'
                ? 'bg-amber-600 text-white shadow-xs'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
            }`}
            title="Eksik metin veya şık içeren, arka planda muallak olarak işaretlenen sorular"
          >
            ⚠️ Muallak / Parça Sorular ({tabCounts.ambiguousCount})
          </button>
          <button
            onClick={() => { setAmbiguityTab('all'); setCurrentPage(1); }}
            className={`px-3 py-1 rounded-full text-xs font-bold transition-all cursor-pointer ${
              ambiguityTab === 'all'
                ? 'bg-slate-800 text-white shadow-xs'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
            }`}
          >
            Tümü ({tabCounts.totalCount})
          </button>
        </div>

        {/* Multi-Facet Dropdowns */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs pt-3 border-t border-slate-100">
          {/* Kurul / Sınav Dropdown */}
          <div className="space-y-1">
            <label className="text-[11px] font-bold text-slate-700 flex items-center gap-1">
              <GraduationCap className="w-3.5 h-3.5 text-teal-600" />
              Kurul / Sınav Türü:
            </label>
            <select
              value={selectedCommittee}
              onChange={(e) => {
                setSelectedCommittee(e.target.value);
                setCurrentPage(1);
              }}
              className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-teal-500"
            >
              <option value="all">Tüm Kurul ve Sınavlar</option>
              {filterOptions.committees.map(cId => (
                <option key={cId} value={cId}>
                  {formatCommitteeName(cId)}
                </option>
              ))}
            </select>
          </div>

          {/* Sene / Yıl Dropdown */}
          <div className="space-y-1">
            <label className="text-[11px] font-bold text-slate-700 flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5 text-teal-600" />
              Sınav Yılı / Kaynak:
            </label>
            <select
              value={selectedYear}
              onChange={(e) => {
                setSelectedYear(e.target.value);
                setCurrentPage(1);
              }}
              className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-teal-500"
            >
              <option value="all">Tüm Yıllar & Dönemler</option>
              {filterOptions.years.map(yr => (
                <option key={yr} value={yr}>
                  {yr}
                </option>
              ))}
            </select>
          </div>

          {/* Branş / Ders Dropdown */}
          <div className="space-y-1">
            <label className="text-[11px] font-bold text-slate-700 flex items-center gap-1">
              <Stethoscope className="w-3.5 h-3.5 text-teal-600" />
              Tıbbi Branş / Ders:
            </label>
            <select
              value={selectedDiscipline}
              onChange={(e) => {
                setSelectedDiscipline(e.target.value);
                setCurrentPage(1);
              }}
              className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-xs font-semibold text-slate-900 focus:bg-white focus:border-teal-500"
            >
              <option value="all">Tüm Tıp Branşları</option>
              {filterOptions.disciplines.map(d => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Questions Listing */}
      {isLoading ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3 shadow-xs">
          <RefreshCw className="w-8 h-8 text-teal-600 animate-spin mx-auto" />
          <h4 className="font-bold text-slate-800 text-sm">Çıkmış Sorular Yükleniyor...</h4>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Veritabanındaki tüm çıkmış sınav soruları ve ders notları arşivi hazırlanıyor...
          </p>
        </div>
      ) : paginatedQuestions.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3 shadow-xs">
          <HelpCircle className="w-10 h-10 text-slate-400 mx-auto" />
          <h4 className="font-bold text-slate-800 text-base">Eşleşen Çıkmış Soru Bulunamadı</h4>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            Arama kriterlerinize veya seçilen filtrelere uygun soru bulunamadı. Filtreleri sıfırlayarak tüm soruları görebilirsiniz.
          </p>
          <button
            onClick={() => {
              setSearchQuery('');
              setSelectedCommittee('all');
              setSelectedYear('all');
              setSelectedDiscipline('all');
            }}
            className="bg-teal-50 hover:bg-teal-100 text-teal-800 font-bold px-4 py-2 rounded-xl text-xs cursor-pointer"
          >
            Filtreleri Temizle
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {paginatedQuestions.map((q) => {
            const effectiveMode: 'redacted' | 'raw' | 'split' = cardViewOverrides[q.id] || viewMode;
            const slideMatch = getQuestionSlideMatch(q);
            const isLiked = (q.likedBy || []).includes(currentUser?.uid || 'anonim-std');

            const stem = q.reconstruction?.stem || q.fragments?.[0]?.text || q.topic;
            const options = q.reconstruction?.options || q.options || [];
            const correctAnswer = q.reconstruction?.correctAnswer || q.claimedAnswer;
            const explanation = q.reconstruction?.explanation;

            return (
              <div
                key={q.id}
                className="bg-white rounded-2xl border border-slate-200 hover:border-teal-300 transition-all p-4 sm:p-6 shadow-xs space-y-4"
              >
                {/* Header Metadata Bar */}
                <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-100">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="font-black text-slate-900 text-sm bg-slate-100 px-2.5 py-1 rounded-lg">
                      #{q.questionNumber}
                    </span>

                    <span className="bg-teal-50 text-teal-800 border border-teal-200 text-xs font-bold px-2.5 py-0.5 rounded-md">
                      {q.discipline || 'Tıp'}
                    </span>

                    <span className="bg-slate-100 text-slate-700 text-xs font-semibold px-2 py-0.5 rounded-md">
                      {formatCommitteeName(q.committeeId)}
                    </span>

                    {q.examYear && (
                      <span className="bg-amber-50 text-amber-900 border border-amber-200 text-xs font-bold px-2 py-0.5 rounded-md flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-amber-600" />
                        {q.examYear}
                      </span>
                    )}

                    {/* Exact source file name badge */}
                    <span className="bg-slate-100 text-slate-700 text-xs font-semibold px-2 py-0.5 rounded-md flex items-center gap-1" title="Sınav sorusunun çıkarıldığı orijinal PDF dosyası">
                      <FileText className="w-3 h-3 text-slate-500" />
                      <span className="truncate max-w-[150px] sm:max-w-[220px]">
                        {q.sourceFile || 'Çıkmış Dosyası'}
                      </span>
                    </span>

                    {q.isAmbiguous && (
                      <span className="bg-amber-100 text-amber-900 border border-amber-300 text-[10px] font-bold px-2 py-0.5 rounded-full">
                        ⚠️ Muallak Parça
                      </span>
                    )}
                  </div>

                  {/* Actions & Card Flip */}
                  <div className="flex items-center gap-1.5">
                    {/* AI Similar Question Generator Button ("Ek Soru Sor") */}
                    <button
                      onClick={() => handleGenerateSimilarQuestion(q, slideMatch)}
                      disabled={isGeneratingSimilar === q.id}
                      className="bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-300 px-2.5 py-1 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer shadow-2xs"
                      title="Bu çıkmış soru ve ders notu konusundan yola çıkarak yapay zeka ile benzer soru üret"
                    >
                      {isGeneratingSimilar === q.id ? (
                        <RefreshCw className="w-3.5 h-3.5 animate-spin text-teal-600" />
                      ) : (
                        <Sparkles className="w-3.5 h-3.5 text-teal-600" />
                      )}
                      <span>{isGeneratingSimilar === q.id ? 'Üretiliyor...' : 'Ek Soru Sor'}</span>
                    </button>

                    {/* Slide Match Reference Badge */}
                    {slideMatch && (
                      <button
                        onClick={() => setSelectedSlideSnippet({
                          note: slideMatch.note,
                          page: slideMatch.page,
                          question: q,
                          score: slideMatch.score,
                        })}
                        className="bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-300 px-2.5 py-1 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer shadow-2xs"
                        title="Bu sorunun değinildiği amfi ders slaytını aç"
                      >
                        <BookMarked className="w-3.5 h-3.5 text-emerald-700" />
                        <span className="truncate max-w-[150px]">Slayt #{slideMatch.page.pageNumber}</span>
                      </button>
                    )}

                    {/* Mode Toggle for this single card */}
                    <div className="bg-slate-100 p-0.5 rounded-lg flex text-[11px] font-bold">
                      <button
                        onClick={() => setCardViewOverrides(prev => ({ ...prev, [q.id]: 'redacted' }))}
                        className={`px-2 py-0.5 rounded transition-all cursor-pointer ${
                          effectiveMode === 'redacted' ? 'bg-white text-teal-800 shadow-2xs' : 'text-slate-500'
                        }`}
                        title="Yapay zeka redakte görünümü"
                      >
                        Redakte
                      </button>
                      <button
                        onClick={() => setCardViewOverrides(prev => ({ ...prev, [q.id]: 'raw' }))}
                        className={`px-2 py-0.5 rounded transition-all cursor-pointer ${
                          effectiveMode === 'raw' ? 'bg-white text-teal-800 shadow-2xs' : 'text-slate-500'
                        }`}
                        title="Ham orijinal metin görünümü"
                      >
                        Ham
                      </button>
                    </div>

                    {/* Copy Button */}
                    <button
                      onClick={() => handleCopyQuestion(q)}
                      className="p-1.5 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer"
                      title="Soruyu metin olarak kopyala"
                    >
                      {copiedId === q.id ? (
                        <Check className="w-4 h-4 text-emerald-600" />
                      ) : (
                        <Copy className="w-4 h-4" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Question Topic */}
                <div className="text-xs font-bold text-slate-500">
                  Konu: <span className="text-slate-800 font-semibold">{q.topic}</span>
                </div>

                {/* CONTENT AREA: Depends on Mode */}
                {effectiveMode === 'split' ? (
                  /* SPLIT SIDE-BY-SIDE VIEW */
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                    {/* Raw Column */}
                    <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-3">
                      <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700 pb-1 border-b border-slate-200">
                        <FileText className="w-3.5 h-3.5 text-slate-500" />
                        <span>Ham / Orijinal Hatırlanan Metin</span>
                      </div>
                      <p className="text-xs text-slate-800 leading-relaxed font-sans">
                        {q.fragments?.[0]?.text || stem}
                      </p>
                      {q.options && q.options.length > 0 && (
                        <div className="space-y-1.5 text-xs">
                          {q.options.map(opt => (
                            <div key={opt.key} className="flex items-start gap-2 text-slate-700">
                              <span className="font-bold text-slate-500">{opt.key})</span>
                              <span>{opt.text}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* Redacted Column */}
                    <div className="bg-teal-50/50 border border-teal-200 rounded-xl p-4 space-y-3">
                      <div className="flex items-center gap-1.5 text-xs font-bold text-teal-900 pb-1 border-b border-teal-200">
                        <Sparkles className="w-3.5 h-3.5 text-teal-600" />
                        <span>Yapay Zeka Redakte Hali</span>
                      </div>
                      <p className="text-xs text-slate-900 font-medium leading-relaxed">
                        {stem}
                      </p>
                      {options.length > 0 && (
                        <div className="space-y-1.5 text-xs">
                          {options.map((opt: any) => {
                            const isCorrect = opt.key === correctAnswer;
                            return (
                              <div
                                key={opt.key}
                                className={`p-2 rounded-lg border transition-all flex items-start justify-between gap-2 ${
                                  isCorrect
                                    ? 'bg-emerald-100/70 border-emerald-400 text-emerald-950 font-bold'
                                    : 'bg-white border-slate-200 text-slate-700'
                                }`}
                              >
                                <div className="flex items-start gap-2">
                                  <span className={isCorrect ? 'text-emerald-800' : 'text-slate-400'}>{opt.key})</span>
                                  <span>{opt.text}</span>
                                </div>
                                {isCorrect && (
                                  <span className="text-[10px] text-emerald-700 font-extrabold uppercase shrink-0">
                                    ✓ Doğru
                                  </span>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  </div>
                ) : effectiveMode === 'raw' ? (
                  /* RAW ORIGINAL VIEW */
                  <div className="space-y-3 bg-slate-50 border border-slate-200 rounded-xl p-4">
                    <div className="flex items-center justify-between text-xs text-slate-500 pb-1 border-b border-slate-200">
                      <span className="font-semibold flex items-center gap-1.5">
                        <FileText className="w-3.5 h-3.5 text-slate-500" />
                        Orijinal Sınav Metni
                      </span>
                      <span className="text-[11px] font-bold text-amber-800 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                        {q.sourceFile || 'PDF Kaynağı'}
                      </span>
                    </div>

                    <div className="text-xs sm:text-sm text-slate-900 leading-relaxed font-sans">
                      <p className="font-medium whitespace-pre-wrap">
                        {(q as any).rawQuestion?.stem || q.fragments?.[0]?.text || q.rawStem || q.topic}
                      </p>
                    </div>

                    {(((q as any).rawQuestion?.options && (q as any).rawQuestion.options.length > 0) || (q.options && q.options.length > 0)) && (
                      <div className="space-y-1.5 pt-2 border-t border-slate-200">
                        {((q as any).rawQuestion?.options || q.options).map((opt: any) => {
                          const isClaimed = opt.key === (q.claimedAnswer || (q as any).rawQuestion?.claimedAnswer);
                          return (
                            <div key={opt.key} className={`flex items-start gap-2 text-xs p-1.5 rounded ${isClaimed ? 'bg-amber-50 text-amber-950 font-bold border border-amber-200' : 'text-slate-700'}`}>
                              <span className="font-bold text-slate-500">{opt.key})</span>
                              <span>{opt.text}</span>
                              {isClaimed && <span className="text-[10px] text-amber-800 ml-auto font-semibold">İşaretlenen</span>}
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                ) : (
                  /* REDACTED (DEFAULT AI FORMAT) */
                  <div className="space-y-3.5">
                    {/* Stem */}
                    <p className="text-xs sm:text-sm font-medium text-slate-900 leading-relaxed">
                      {stem}
                    </p>

                    {/* Options Grid */}
                    {options && options.length > 0 && (
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                        {options.map((opt: any) => {
                          const isCorrect = opt.key === correctAnswer;
                          return (
                            <div
                              key={opt.key}
                              className={`p-2.5 rounded-xl border transition-all flex items-start justify-between gap-2 ${
                                isCorrect
                                  ? 'bg-emerald-50 border-emerald-400 text-emerald-950 font-bold shadow-2xs'
                                  : 'bg-slate-50/60 border-slate-200 text-slate-800'
                              }`}
                            >
                              <div className="flex items-start gap-2">
                                <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold shrink-0 ${
                                  isCorrect ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-600'
                                }`}>
                                  {opt.key}
                                </span>
                                <span className="leading-snug pt-0.5">{opt.text}</span>
                              </div>
                              {isCorrect && (
                                <span className="text-[10px] bg-emerald-200 text-emerald-900 px-1.5 py-0.5 rounded font-extrabold shrink-0">
                                  Doğru
                                </span>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    )}

                    {/* Clinical / Pathological Explanation Box */}
                    {explanation && (
                      <div className="bg-teal-50/70 border border-teal-200/80 rounded-xl p-3 text-xs space-y-1">
                        <div className="flex items-center gap-1.5 font-bold text-teal-900">
                          <CheckCircle2 className="w-3.5 h-3.5 text-teal-700" />
                          <span>Klinik Patofizyolojik Açıklama & Sınav Notu:</span>
                        </div>
                        <p className="text-slate-700 leading-relaxed pl-5 whitespace-pre-line">
                          {explanation}
                        </p>
                      </div>
                    )}
                  </div>
                )}

                {/* Footer Bar: Likes, Comments, Report & Matched Slide Preview */}
                <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100 text-xs">
                  {/* Left: Like, Comment & Report Interaction */}
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleToggleLike(q)}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-bold transition-all cursor-pointer ${
                        isLiked
                          ? 'bg-teal-700 text-white shadow-xs'
                          : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                      }`}
                      title={isLiked ? 'Beğeniyi geri al' : 'Soruyu beğen'}
                    >
                      <ThumbsUp className={`w-3.5 h-3.5 ${isLiked ? 'fill-current' : ''}`} />
                      <span>{q.upvotes || 0}</span>
                    </button>

                    {/* Comments Toggle Button */}
                    <button
                      onClick={() => setExpandedCommentsQuestionId(expandedCommentsQuestionId === q.id ? null : q.id)}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-bold transition-all cursor-pointer ${
                        expandedCommentsQuestionId === q.id
                          ? 'bg-blue-600 text-white shadow-xs'
                          : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                      }`}
                      title="Soruya ait öğrenci öneri ve yorumlarını göster"
                    >
                      <MessageSquare className="w-3.5 h-3.5" />
                      <span>Öneri & Yorum ({(q as any).comments?.length || 0})</span>
                    </button>

                    {/* Report / Complaint Button ("Şikayet Et / Hata Bildir") */}
                    <button
                      onClick={() => setReportingQuestion(q)}
                      className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg font-semibold text-rose-600 hover:bg-rose-50 border border-transparent hover:border-rose-200 transition-all cursor-pointer"
                      title="Soru hakkında hata veya şikayet bildir"
                    >
                      <Flag className="w-3.5 h-3.5" />
                      <span className="hidden sm:inline">Hata Bildir</span>
                    </button>

                    <span className="text-[11px] text-slate-400 hidden md:inline">
                      {q.reconstruction ? '✓ Redakte Doğrulandı' : 'Öğrenci Katkısı'}
                    </span>
                  </div>

                  {/* Right: Slide Link */}
                  {slideMatch && (
                    <button
                      onClick={() => setSelectedSlideSnippet({
                        note: slideMatch.note,
                        page: slideMatch.page,
                        question: q,
                        score: slideMatch.score,
                      })}
                      className="text-teal-800 hover:text-teal-950 font-bold flex items-center gap-1 cursor-pointer"
                    >
                      <span>İlgili Ders Slaytı Kesiti: {slideMatch.note.title.substring(0, 30)}...</span>
                      <ExternalLink className="w-3 h-3 text-slate-400" />
                    </button>
                  )}
                </div>

                {/* Expandable Comments & Suggestions Drawer */}
                {expandedCommentsQuestionId === q.id && (
                  <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-3 pt-3">
                    <div className="flex items-center justify-between text-xs font-bold text-slate-800 pb-2 border-b border-slate-200">
                      <span className="flex items-center gap-1.5">
                        <MessageSquare className="w-3.5 h-3.5 text-blue-600" />
                        Öğrenci Tartışmaları, Alternatif Çözümler & Mnemonicler ({(q as any).comments?.length || 0})
                      </span>
                    </div>

                    {/* Comments List */}
                    <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                      {((q as any).comments && (q as any).comments.length > 0) ? (
                        (q as any).comments.map((c: any) => (
                          <div key={c.id} className="bg-white border border-slate-200 rounded-lg p-2.5 text-xs space-y-1">
                            <div className="flex items-center justify-between text-[11px] text-slate-500 font-semibold">
                              <span className="text-slate-800 font-bold">{c.author || 'Tıp Öğrencisi'}</span>
                              <span>{new Date(c.timestamp).toLocaleString('tr-TR')}</span>
                            </div>
                            <p className="text-slate-700 leading-relaxed">{c.text}</p>
                          </div>
                        ))
                      ) : (
                        <p className="text-xs text-slate-500 italic py-1">
                          Henüz bir öneri veya yorum eklenmemiş. Bu soruya ait klinik ipucu veya alternatif çözüm yolunu ilk sen ekle!
                        </p>
                      )}
                    </div>

                    {/* New Comment Input */}
                    <div className="flex items-center gap-2 pt-2 border-t border-slate-200">
                      <input
                        type="text"
                        value={newCommentText}
                        onChange={(e) => setNewCommentText(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') handleCommentSubmit(q.id);
                        }}
                        placeholder="Öneri, pratik çözüm ipucu veya yorumunuzu yazın..."
                        className="flex-1 bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-xs text-slate-900 focus:outline-teal-600"
                      />
                      <button
                        onClick={() => handleCommentSubmit(q.id)}
                        disabled={isSubmittingComment || !newCommentText.trim()}
                        className="bg-teal-700 hover:bg-teal-800 disabled:opacity-50 text-white font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1 cursor-pointer transition-colors"
                      >
                        <Send className="w-3.5 h-3.5" />
                        <span>Gönder</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            );
          })}

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between pt-6 border-t border-slate-200 text-xs font-semibold">
              <span className="text-slate-500">
                Sayfa {currentPage} / {totalPages} (Toplam {filteredQuestions.length} soru)
              </span>

              <div className="flex items-center gap-1">
                <button
                  onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-1.5 rounded-lg border border-slate-300 hover:bg-slate-100 disabled:opacity-40 cursor-pointer flex items-center gap-1"
                >
                  <ChevronLeft className="w-3.5 h-3.5" />
                  <span>Önceki</span>
                </button>

                <div className="hidden sm:flex items-center gap-1 px-2">
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    let pageNum = i + 1;
                    if (currentPage > 3 && totalPages > 5) {
                      pageNum = Math.min(totalPages - 4 + i, Math.max(1, currentPage - 2 + i));
                    }
                    return (
                      <button
                        key={pageNum}
                        onClick={() => setCurrentPage(pageNum)}
                        className={`w-7 h-7 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                          currentPage === pageNum
                            ? 'bg-teal-700 text-white'
                            : 'hover:bg-slate-100 text-slate-700'
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                </div>

                <button
                  onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-1.5 rounded-lg border border-slate-300 hover:bg-slate-100 disabled:opacity-40 cursor-pointer flex items-center gap-1"
                >
                  <span>Sonraki</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Slide Excerpt Popover Modal */}
      {selectedSlideSnippet && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl max-w-2xl w-full shadow-2xl border border-slate-200 overflow-hidden space-y-4 my-6 animate-fade-in flex flex-col max-h-[85vh]">
            {/* Modal Header */}
            <div className="bg-slate-900 text-white p-4 sm:p-5 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-teal-500/20 text-teal-400 border border-teal-500/30 flex items-center justify-center">
                  <BookMarked className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-sm sm:text-base">Ders Notu / Slayt Eşleşmesi</h4>
                  <p className="text-xs text-slate-400">
                    {selectedSlideSnippet.note.discipline} • Slayt Sayfası #{selectedSlideSnippet.page.pageNumber}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setSelectedSlideSnippet(null)}
                className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-4 sm:p-6 overflow-y-auto space-y-4 flex-1 text-xs">
              <div className="bg-teal-50 border border-teal-200 rounded-xl p-3 text-teal-900 space-y-1">
                <strong className="block font-bold">
                  Soru: #{selectedSlideSnippet.question.questionNumber} - {selectedSlideSnippet.question.topic}
                </strong>
                <p className="text-[11px] text-teal-800">
                  Bu sorunun sınavda ölçtüğü bilgi, amfide anlatılan <strong>"{selectedSlideSnippet.note.title}"</strong> dersinin <strong>#{selectedSlideSnippet.page.pageNumber}</strong> numaralı slaytında birebir geçmektedir.
                </p>
              </div>

              {/* Verbatim Page Content */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-slate-700 font-bold border-b border-slate-200 pb-1">
                  <span>Slayt Metni Kesiti (Verbatim / Sayfa #{selectedSlideSnippet.page.pageNumber}):</span>
                  <span className="text-[10px] text-teal-700 bg-teal-100 px-2 py-0.5 rounded font-mono">
                    %{selectedSlideSnippet.score} Eşleşme
                  </span>
                </div>

                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs sm:text-sm font-sans text-slate-900 leading-relaxed max-h-60 overflow-y-auto whitespace-pre-wrap">
                  {selectedSlideSnippet.page.content}
                </div>
              </div>

              {/* Keywords */}
              {selectedSlideSnippet.page.keywords && selectedSlideSnippet.page.keywords.length > 0 && (
                <div className="space-y-1.5 pt-2">
                  <span className="text-[11px] font-bold text-slate-500 block">Slaytta Geçen Anahtar Kavramlar:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {selectedSlideSnippet.page.keywords.map((kw, i) => (
                      <span key={i} className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-[10px] font-medium">
                        #{kw}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="bg-slate-50 border-t border-slate-200 p-4 flex items-center justify-between shrink-0 text-xs">
              <button
                onClick={() => setSelectedSlideSnippet(null)}
                className="px-4 py-2 rounded-xl text-slate-600 font-semibold hover:bg-slate-200 cursor-pointer"
              >
                Kapat
              </button>

              {onOpenNote && (
                <button
                  onClick={() => {
                    const noteId = selectedSlideSnippet.note.id;
                    const pageNo = selectedSlideSnippet.page.pageNumber;
                    setSelectedSlideSnippet(null);
                    onOpenNote(noteId, pageNo);
                  }}
                  className="bg-teal-700 hover:bg-teal-800 text-white font-bold px-4 py-2 rounded-xl flex items-center gap-1.5 cursor-pointer shadow-xs"
                >
                  <BookOpen className="w-3.5 h-3.5 text-teal-200" />
                  <span>Ders Notunu Tam Ekranda Aç</span>
                </button>
              )}
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
                <span className="bg-emerald-50 border border-emerald-300 text-emerald-900 px-2 py-1 rounded-md font-semibold flex items-center gap-1">
                  <BookMarked className="w-3.5 h-3.5 text-emerald-600" />
                  Ders: {similarModalQuestion.matchedNoteTitle} (Slayt #{similarModalQuestion.matchedSlidePage})
                </span>
              </div>

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
    </div>
  );
};
