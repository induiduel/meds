import React, { useCallback, useState, useMemo, useEffect, useDeferredValue, useRef } from 'react';
import { AnswerPoll } from './AnswerPoll';
import { PageHeader } from './ui/PageHeader';
import { StemText, Highlight } from './ui/StemText';
import { Collapsible } from './ui/Collapsible';
import { Dialog } from './ui/Dialog';
import { foldText, parseQuery, scoreFields, SearchField } from '../services/searchText';
import { QuestionAboutDialog, normalizeRefList } from './QuestionAboutDialog';
import { SourceText, Marked } from './ui/SourceText';
import { buildQuestionFocus, QuestionFocus } from '../services/questionFocus';
import { toast } from './ui/Toast';
import { ChangeInfo } from './ui/ChangeInfo';
import {
  Sparkles,
  Info,
  BookOpen,
  Search,
  Filter,
  CheckCircle2,
  Calendar,
  Layers,
  ChevronLeft,
  ChevronRight,
  ThumbsUp,
  ThumbsDown,
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
  SlidersHorizontal,
  ChevronDown,
  Wand2,
  EyeOff,
  BarChart3,
  Share2,
  ShieldAlert,
  ShieldCheck,
  History,
  Scale,
  Trash2,
} from 'lucide-react';
import { ActionMenu, ActionItem } from './ui/ActionMenu';
import { ReportQuestionModal } from './ReportQuestionModal';
import { SectionLoader } from './ui/Animations';
import { QuestionItem, LectureNote, LectureNotePage, QuestionLectureMatch } from '../types';
import { AppUser, ADMIN_EMAIL } from '../services/auth';
import { ApiService } from '../services/api';
import { pastQuestionsCache, CacheSyncStatus } from '../services/pastQuestionsCache';
import { AdminCustomRedactModal } from './AdminCustomRedactModal';
import { renderHighlightedSnippet } from './QuestionCard';
import { learnMatcher, QuestionLearnMatch, isReliableLearnMatch } from '../services/learnMatcher';
import { FlashcardComponent } from './learn/InteractiveDeckView';
import { pathFor, linkClick, parseLocation, writeLocation } from '../router';
import {
  OFFICIAL_CURRICULUM_COMMITTEES,
  DONEM3_CURRICULUM_DISCIPLINES,
  normalizeDonem3Discipline,
  isDonem3Question,
} from '../data/curriculumData';

/** Denetleyici Onayı almış (altın standart, doğrulanmış) soru */
export const isDenetleyiciQuestion = (q: any): boolean =>
  Boolean(q?.denetleyiciOnayi || q?.denetleyici_onayi || q?.surum === 'denetleyici' || (Array.isArray(q?.tags) && q.tags.includes('denetleyici_onayi')));

/** Faz 14'te önerisi onaylanıp canlı soruya uygulanmış soru. */
export const isPhase14Fixed = (q: any): boolean =>
  Boolean(q?.phase14 || (Array.isArray(q?.tags) && q.tags.includes('faz14_duzeltildi')));
/** Faz 14 önerisi gösteriliyor ama yönetici onayı bekliyor (okuma katmanı) */
export const isPhase14Pending = (q: any): boolean => q?.phase14?.status === 'onay_bekliyor';

export const isDeepSeekQuestion = (q: any): boolean => {
  if (!q) return false;
  if (q.answerStatus === 'dogrulanmadi') return false;
  if (q.deepseekEnriched) return true;
  if (q.reconstruction?.reconstructionQuality === 'deepseek_verified') return true;
  if (Array.isArray(q.tags) && (q.tags.includes('deepseek_verified') || q.tags.includes('deepseek') || q.tags.includes('dogrulanmis_soru'))) return true;
  if (q.verification && (q.verification.status === 'onaylandi' || q.verification.answerStatus === 'dogrulandi')) return true;
  if (typeof q.sourceFile === 'string' && q.sourceFile.toLowerCase().includes('deepseek')) return true;
  return false;
};

export const isGeminiV3Question = (q: any): boolean =>
  Array.isArray(q?.tags) && q.tags.includes('gemini_v3');

/** Kalite puanı (0–100): sunucu `qualityScore` yazar; eski önbellek/Supabase kaydı için hafif istemci tahmini. */
export const getQualityScore = (q: any): number => {
  if (typeof q?.qualityScore === 'number' && Number.isFinite(q.qualityScore)) return q.qualityScore;
  let s = 100;
  const stem = String(q?.reconstruction?.stem || q?.stem || q?.fragments?.[0]?.text || '');
  const opts = (q?.reconstruction?.options || q?.options || []) as any[];
  const ans = String(q?.reconstruction?.correctAnswer || q?.correctAnswer || q?.claimedAnswer || '');
  const expl = String(q?.reconstruction?.explanation || q?.explanation || q?.tibbi_aciklama || '');
  if (!stem.trim()) s -= 40; else if (stem.trim().length < 30) s -= 25; else if (stem.trim().length < 50) s -= 12;
  if (opts.length <= 2) s -= 40; else if (opts.length === 3) s -= 18; else if (opts.length === 4) s -= 8;
  if (!ans) s -= 25;
  if (expl.trim().length < 20) s -= 15;
  if (!q?.sik_analizi) s -= 10;
  if (q?.isAmbiguous) s -= 15;
  if (q?.isSuspect) s -= 12;
  return Math.max(0, Math.min(100, s));
};

export const getQualityTier = (q: any): string => {
  if (typeof q?.qualityTier === 'string' && q.qualityTier) return q.qualityTier;
  const s = getQualityScore(q);
  return s >= 90 ? 'altin' : s >= 75 ? 'saglam' : s >= 60 ? 'orta' : s >= 40 ? 'zayif' : 'kritik';
};

const isNewQ = (q: QuestionItem): boolean =>
  Boolean(
    q.isNewQuestion ||
      (q.examYear ? q.examYear.includes('2026') || q.examYear.includes('2027') : false) ||
      (q.createdAt ? new Date(q.createdAt).getTime() > Date.now() - 30 * 86400000 : false),
  );

type FacetKey = 'pool' | 'committee' | 'year' | 'discipline' | 'topic' | 'answer' | 'explanation' | 'source' | 'p14' | 'denetleyici' | 'newness' | 'manual' | 'repeated';
interface Prep {
  q: QuestionItem;
  disc: string;
  topic: string;
  year: string;
  comms: string[];
  isNew: boolean;
  isManual: boolean;
  isRepeated: boolean;
  hasAnswer: boolean;
  doubtful: boolean;
  hasExpl: boolean;
  fields: SearchField[];
}

interface PastExamsViewProps {
  currentUser: AppUser | null;
  lectureNotes?: LectureNote[];
  initialSearchQuery?: string;
  onOpenNote?: (noteId: string, pageNumber?: number) => void;
  onUpdateQuestionReference?: (questionId: string, match: QuestionLectureMatch) => Promise<void>;
  onNavigateToLearn?: (deckId?: string, slideNumber?: number, focus?: QuestionFocus) => void;
}

/** Kelime düzeyinde fark: yeni tarafta eklenenleri, eski tarafta çıkarılanları işaretler. */
const WordDiff: React.FC<{ from: string; to: string; side: 'old' | 'new' }> = ({ from, to, side }) => {
  const parts = React.useMemo(() => {
    const a = from.split(/(\s+)/), b = to.split(/(\s+)/);
    if (from === to || !from || !to || a.length * b.length > 250000) return null;
    const m = a.length, k = b.length;
    const dp: Uint16Array[] = Array.from({ length: m + 1 }, () => new Uint16Array(k + 1));
    for (let i = m - 1; i >= 0; i--) for (let j = k - 1; j >= 0; j--) dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
    const out: { t: string; d: boolean }[] = [];
    let i = 0, j = 0;
    const push = (t: string, d: boolean) => { const last = out[out.length - 1]; if (last && last.d === d) last.t += t; else out.push({ t, d }); };
    while (i < m && j < k) {
      if (a[i] === b[j]) { push(a[i], false); i++; j++; }
      else if (dp[i + 1][j] >= dp[i][j + 1]) { if (side === 'old') push(a[i], !/^\s+$/.test(a[i])); i++; }
      else { if (side === 'new') push(b[j], !/^\s+$/.test(b[j])); j++; }
    }
    if (side === 'old') while (i < m) push(a[i++], true);
    else while (j < k) push(b[j++], true);
    return out;
  }, [from, to, side]);
  const text = side === 'old' ? from : to;
  if (!parts) return <>{text}</>;
  const Tag = side === 'old' ? 'del' : 'ins';
  return <>{parts.map((p, i) => (p.d ? <Tag key={i}>{p.t}</Tag> : <React.Fragment key={i}>{p.t}</React.Fragment>))}</>;
};

/** İki sürümün kitapçık görünümünde farkı: yeni metin + kelime düzeyinde işaret, değişen satırın altında "önceki" hali. */
const DiffSheet: React.FC<{
  oldLabel: string;
  newLabel: string;
  oldStem: string;
  newStem: string;
  oldOpts: { key: string; text: string }[];
  newOpts: { key: string; text: string }[];
  answer?: string;
  oldAnswer?: string;
  hideAnswer?: boolean;
  terms?: string[];
  children?: React.ReactNode;
}> = ({ oldLabel, newLabel, oldStem, newStem, oldOpts, newOpts, answer, oldAnswer, hideAnswer, children }) => {
  const n = (t: any) => String(t ?? '').replace(/\s+/g, ' ').trim();
  const os = n(oldStem);
  const ns = n(newStem) || os;
  const keys = Array.from(new Set([...oldOpts, ...newOpts].map((o) => String(o.key).toUpperCase()))).sort();
  const textOf = (list: { key: string; text: string }[], k: string) => n(list.find((o) => String(o.key).toUpperCase() === k)?.text);
  const answerChanged = !!oldAnswer && !!answer && oldAnswer !== answer;
  const hasOld = !!os || oldOpts.some((o) => n(o.text));
  const changed = !hasOld ? 0 : keys.filter((k) => (oldOpts.length ? textOf(oldOpts, k) !== textOf(newOpts, k) : false)).length + (os && os !== ns ? 1 : 0) + (answerChanged ? 1 : 0);
  return (
    <div className="cx-diff">
      <div className="cx-diff-bar">
        <span className={`cx-diff-count ${changed ? '' : 'is-none'}`}>{!hasOld ? `${oldLabel} sürümün kaydı yok` : changed ? `${changed} değişiklik` : 'Değişiklik yok'}</span>
        {answerChanged && !hideAnswer && <span className="cx-flag is-warn">Cevap {oldAnswer} → {answer}</span>}
        <span className="cx-diff-legend"><ins>{newLabel}</ins><del>{oldLabel}</del></span>
      </div>
      <div className="cx-diff-stem">
        <p className="ms-stem m-0">{os && ns !== os ? <WordDiff from={os} to={ns} side="new" /> : ns}</p>
        {os && ns !== os && <p className="cx-diff-was"><span>{oldLabel}</span><span><WordDiff from={os} to={ns} side="old" /></span></p>}
      </div>
      {keys.length > 0 && (
        <ol className="cx-opts">
          {keys.map((k) => {
            const o = textOf(oldOpts, k);
            const nw = textOf(newOpts, k);
            const isAns = !hideAnswer && k === answer;
            const wasAns = !hideAnswer && answerChanged && k === oldAnswer;
            return (
              <li key={k} className="cx-opt-li">
                <div className={`cx-opt ${isAns ? 'is-correct' : ''} ${wasAns ? 'was-answer' : ''}`}>
                  <span className="cx-bubble" aria-hidden>{isAns ? <Check strokeWidth={3} /> : k}</span>
                  <span className="cx-opt-t">
                    {nw ? (o && o !== nw ? <WordDiff from={o} to={nw} side="new" /> : nw) : <span className="cx-diff-gone">{newLabel} sürümünde yok</span>}
                    {!o && nw && oldOpts.length > 0 && <span className="cx-flag is-new cx-diff-tag">Yeni şık</span>}
                    {wasAns && <span className="cx-flag is-warn cx-diff-tag">{oldLabel} cevap</span>}
                    {o && o !== nw && <span className="cx-diff-was"><span>{oldLabel}</span><span><WordDiff from={o} to={nw} side="old" /></span></span>}
                  </span>
                </div>
              </li>
            );
          })}
        </ol>
      )}
      {children}
    </div>
  );
};

export const PastExamsView: React.FC<PastExamsViewProps> = ({
  currentUser,
  lectureNotes = [],
  initialSearchQuery = '',
  onOpenNote,
  onUpdateQuestionReference,
  onNavigateToLearn,
}) => {
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [internalNotes, setInternalNotes] = useState<LectureNote[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(initialSearchQuery);
  
  // Filter States
  const [selectedCommittee, setSelectedCommittee] = useState<string>('all');
  const [selectedYear, setSelectedYear] = useState<string>('all');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('all');
  const [deepseekFilter, setDeepseekFilter] = useState<'all' | 'deepseek_only' | 'standard_only'>('all');
  const [sourceFilter, setSourceFilter] = useState<'all' | 'gemini_v3' | 'existing'>('all');
  const [phase14Filter, setPhase14Filter] = useState<'all' | 'faz14' | 'faz14_onayli' | 'faz14_bekleyen'>('all');
  const [denetleyiciFilter, setDenetleyiciFilter] = useState<'all' | 'denetleyici_only' | 'standard_only'>('all');
  const [versionViewOverrides, setVersionViewOverrides] = useState<Record<string, 'denetleyici' | 'eski' | 'karsilastir'>>({});
  const [analysisOpen, setAnalysisOpen] = useState<Record<string, boolean>>({});
  const [newnessFilter, setNewnessFilter] = useState<'all' | 'new_only' | 'archived_only'>('all');
  const [manualFilter, setManualFilter] = useState<'all' | 'manual_only' | 'standard_only'>('all');
  const [repeatedFilter, setRepeatedFilter] = useState<'all' | 'repeated_only' | 'unique_only'>('all');
  const [viewMode, setViewMode] = useState<'redacted' | 'raw' | 'split'>('redacted');
  const [filtersOpen, setFiltersOpen] = useState(false);
  // Filtre çekmecesi kapanırken de kayarak çıkar
  const [filtersClosing, setFiltersClosing] = useState(false);
  const closeFilters = () => {
    if (filtersClosing) return;
    setFiltersClosing(true);
    window.setTimeout(() => { setFiltersOpen(false); setFiltersClosing(false); }, 200);
  };
  const [answerFilter, setAnswerFilter] = useState<'all' | 'with' | 'without' | 'doubtful'>('all');
  const [selectedTopic, setSelectedTopic] = useState<string>('all');
  const [facetQuery, setFacetQuery] = useState('');
  const [suggestOpen, setSuggestOpen] = useState(false);
  const searchRef = useRef<HTMLInputElement>(null);
  // Kendini sına: cevaplar gizli, şıkka dokununca doğru cevap görünür (cihazda hatırlanır)
  const [quizMode, setQuizMode] = useState<boolean>(() => {
    try { return localStorage.getItem('cikmis_quiz') === '1'; } catch { return false; }
  });
  const [picks, setPicks] = useState<Record<string, string>>({});
  // "Hakkında" penceresi ve şıkka itiraz
  const [aboutQuestion, setAboutQuestion] = useState<QuestionItem | null>(null);
  const [objection, setObjection] = useState<{ question: QuestionItem; option: { key: string; text: string } } | null>(null);
  // Paylaşılan soru bağlantısı: /cikmis/<soruId> veya ?questionId=<soruId> yalnız o soruyu gösterir
  const [sharedId, setSharedId] = useState<string | null>(() => {
    try {
      const r = parseLocation();
      if (r.route === 'past_exams' && r.param) return r.param;
      if (typeof window !== 'undefined') {
        const p = new URLSearchParams(window.location.search);
        return p.get('questionId') || p.get('q') || null;
      }
      return null;
    } catch {
      return null;
    }
  });
  // Cevabı belirsiz sorular sunucudan güncel alınır (cihaz önbelleği eski kalsa bile anket açılır)
  const [doubtInfo, setDoubtInfo] = useState<{ ids: Set<string>; options: Record<string, Record<string, string>>; resolved: Record<string, { answer: string; by: string }> } | null>(null);
  useEffect(() => {
    let alive = true;
    const load = () => ApiService.getAnswerDoubtful().then((d) => alive && d && setDoubtInfo({ ids: new Set(d.ids), options: d.options, resolved: d.resolved })).catch(() => {});
    load();
    const t = window.setInterval(() => !document.hidden && load(), 60000);
    return () => { alive = false; window.clearInterval(t); };
  }, []);
  // Yapay zekâ inceleme kuyruğu (Faz 14 · ücretsiz): sıradaki sorular kartta "Sırada" olarak görünür
  const [aiQueue, setAiQueue] = useState<Record<string, { status: string; position?: number; requests: number }>>({});
  const loadAiQueue = useCallback(() => ApiService.getAiReviewQueue().then((d) => d && setAiQueue(d.items)).catch(() => {}), []);
  useEffect(() => {
    loadAiQueue();
    const t = window.setInterval(() => !document.hidden && loadAiQueue(), 90000);
    return () => window.clearInterval(t);
  }, [loadAiQueue]);
  const [aiReviewQ, setAiReviewQ] = useState<QuestionItem | null>(null);
  const [aiReviewMsg, setAiReviewMsg] = useState('');
  const [aiReviewBusy, setAiReviewBusy] = useState(false);
  const sendAiReview = async () => {
    if (!aiReviewQ || aiReviewBusy) return;
    setAiReviewBusy(true);
    try {
      const r = await ApiService.requestAiReview(String(aiReviewQ.id), {
        message: aiReviewMsg.trim() || undefined,
        name: currentUser?.displayName || 'Tıp öğrencisi',
        uid: currentUser?.uid || undefined,
        email: currentUser?.email || undefined,
      });
      toast.success(r.joined ? 'İsteğin mevcut incelemeye eklendi' : 'İncelemeye gönderildi', `Sıra: ${r.position} / ${r.waiting}. Ücretsiz kuyrukta sırayla incelenir; güncellenen soru otomatik yayımlanır.`);
      setAiReviewQ(null);
      setAiReviewMsg('');
      loadAiQueue();
    } catch (e: any) {
      toast.error('Gönderilemedi', e?.message);
    } finally {
      setAiReviewBusy(false);
    }
  };
  const openPoll = async (q: QuestionItem) => {
    const uid = currentUser?.uid || currentUser?.email;
    if (!uid) {
      toast.info('Giriş gerekli', 'Anket açmak ve oy vermek için giriş yap.');
      return;
    }
    try {
      const { answer } = await ApiService.openAnswerPoll(String(q.id), uid);
      setDoubtInfo((prev) => ({
        ids: prev?.ids || new Set(),
        options: prev?.options || {},
        resolved: { ...(prev?.resolved || {}), [String(q.id)]: { answer: answer || String(q.correctAnswer || ''), by: 'kullanici' } },
      }));
      toast.success('Anket açıldı', 'Doğru bildiğin şıkkı doldur; topluluğun cevabı kabul edilen cevapla karşılaştırılır.');
    } catch (e: any) {
      toast.error('Anket açılamadı', e?.message);
    }
  };
  const isDoubtful = (q: QuestionItem) => (doubtInfo ? doubtInfo.ids.has(String(q.id)) : Boolean((q as any).answerDoubtful));
  useEffect(() => {
    try { localStorage.setItem('cikmis_quiz', quizMode ? '1' : '0'); } catch { /* gizli pencere */ }
    if (!quizMode) setPicks({});
  }, [quizMode]);
  // "/" ile aramaya odaklan (yazı alanında değilken)
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      if (e.key !== '/' || e.metaKey || e.ctrlKey || t.closest('input, textarea, select, [contenteditable="true"]')) return;
      e.preventDefault();
      searchRef.current?.focus();
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);
  const [explanationFilter, setExplanationFilter] = useState<'all' | 'with' | 'without'>('all');
  const [sortOrder, setSortOrder] = useState<'default' | 'newest' | 'oldest' | 'number' | 'quality_desc' | 'quality_asc'>('default');
  // Faz 14 düzeltmesinin öncesi yalnız istenince gösterilir (rozet ⓘ ya da İşlemler menüsü)
  const [p14Open, setP14Open] = useState<Record<string, boolean>>({});
  const [ambiguityTab, setAmbiguityTab] = useState<'valid' | 'ambiguous' | 'reported' | 'all'>('valid');
  
  // Per-question card override: questionId -> 'redacted' | 'raw' | 'split'
  const [cardViewOverrides, setCardViewOverrides] = useState<Record<string, 'redacted' | 'raw' | 'split'>>({});
  
  // Selected Öğren modülü match modal state
  const [selectedLearnMatch, setSelectedLearnMatch] = useState<{
    question: QuestionItem;
    match: QuestionLearnMatch;
  } | null>(null);

  // Selected Ham Soru location modal state
  const [selectedRawSourceQuestion, setSelectedRawSourceQuestion] = useState<QuestionItem | null>(null);


  // Admin Custom AI Redaction Modal State
  const [customRedactQuestion, setCustomRedactQuestion] = useState<{ question: QuestionItem; match: any } | null>(null);

  // Student & User AI Question Optimizer Modal State

  // Advanced Question Upgrade Modal State (Gelişmiş Klinik Vaka)

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
  const [deletingQuestionId, setDeletingQuestionId] = useState<string | null>(null);

  // Client-Side Caching & Delta-Sync State
  const [cacheStatus, setCacheStatus] = useState<CacheSyncStatus>(pastQuestionsCache.getStatus());

  // Load questions - Yalnızca Dönem 3 çıkmışları gösterilir, diğer dönemler veritabanında kalır
  const loadPastQuestions = async () => {
    setIsLoading(true);
    try {
      const data = await ApiService.getPastQuestions();
      const donem3Data = data
        .filter(q => !q.id?.startsWith('civan-') && !q.tags?.some((t: string) => /civan/i.test(t)))
        .filter(isDonem3Question)
        // Yöneticinin gizlediği (şikâyet sonrası) sorular yalnızca yöneticiye görünür
        .filter(q => !((q as any).hidden || (q as any).data?.hidden) || currentUser?.email === ADMIN_EMAIL || !!currentUser?.isAdmin)
        .map(q => {
          const normDisc = normalizeDonem3Discipline(q.discipline);
          return normDisc ? { ...q, discipline: normDisc } : q;
        });
      setQuestions(donem3Data);
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

  useEffect(() => {
    if (initialSearchQuery) {
      setSearchQuery(initialSearchQuery);
      setCurrentPage(1);
      // Belirli bir soruya gelindi: süzgeçler onu gizlemesin
      setAmbiguityTab('all');
      setSelectedCommittee('all');
      setSelectedDiscipline('all');
      setDeepseekFilter('all');
    }
  }, [initialSearchQuery]);

  // Slayt eşleştirme indeksi arka planda hazırlanır; hazır olunca kartlar yeniden çizilir
  const [, setLearnReady] = useState(0);
  useEffect(() => {
    let alive = true;
    learnMatcher.ensureLoaded().then(() => alive && setLearnReady((n) => n + 1));
    return () => { alive = false; };
  }, []);

  useEffect(() => {
    loadPastQuestions();

    // Subscribe to incremental cache updates (Soru bazında anlık canlı güncelleme)
    const unsubscribe = pastQuestionsCache.subscribe((status, updatedList) => {
      setCacheStatus(status);
      if (updatedList && updatedList.length > 0) {
        const filteredUpdated = updatedList
          .filter(isDonem3Question)
          .map(q => {
            const normDisc = normalizeDonem3Discipline(q.discipline);
            return normDisc ? { ...q, discipline: normDisc } : q;
          });
        if (filteredUpdated.length === 0) return;
        const updateMap = new Map(filteredUpdated.map(q => [q.id, q]));
        setQuestions(prev => {
          let hasChange = false;
          const next = prev.map(existing => {
            if (updateMap.has(existing.id)) {
              hasChange = true;
              return updateMap.get(existing.id)!;
            }
            return existing;
          });
          for (const newQ of filteredUpdated) {
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
    const userUid = currentUser?.uid || currentUser?.email || 'anonim-std';
    const isLiked = (q.likedBy || []).includes(userUid);
    const isDisliked = (q.dislikedBy || []).includes(userUid);

    const newLikedBy = isLiked
      ? (q.likedBy || []).filter(u => u !== userUid)
      : [...(q.likedBy || []), userUid];
    const newDislikedBy = isDisliked
      ? (q.dislikedBy || []).filter(u => u !== userUid)
      : (q.dislikedBy || []);

    const newUpvotes = isLiked
      ? Math.max(0, (q.upvotes || 1) - 1)
      : (q.upvotes || 0) + 1;
    const newDownvotes = isDisliked
      ? Math.max(0, (q.downvotes || 1) - 1)
      : (q.downvotes || 0);

    // Optimistic UI update
    setQuestions(prev =>
      prev.map(item =>
        item.id === q.id
          ? { ...item, upvotes: newUpvotes, downvotes: newDownvotes, likedBy: newLikedBy, dislikedBy: newDislikedBy }
          : item
      )
    );

    try {
      await ApiService.upvotePastQuestion(q.id, userUid);
    } catch (err) {
      console.warn('Like toggle error:', err);
    }
  };

  // Downvote / Dislike toggle
  const handleToggleDislike = async (q: QuestionItem) => {
    const userUid = currentUser?.uid || currentUser?.email || 'anonim-std';
    const isDisliked = (q.dislikedBy || []).includes(userUid);
    const isLiked = (q.likedBy || []).includes(userUid);

    const newDislikedBy = isDisliked
      ? (q.dislikedBy || []).filter(u => u !== userUid)
      : [...(q.dislikedBy || []), userUid];
    const newLikedBy = isLiked
      ? (q.likedBy || []).filter(u => u !== userUid)
      : (q.likedBy || []);

    const newDownvotes = isDisliked
      ? Math.max(0, (q.downvotes || 1) - 1)
      : (q.downvotes || 0) + 1;
    const newUpvotes = isLiked
      ? Math.max(0, (q.upvotes || 1) - 1)
      : (q.upvotes || 0);

    // Optimistic UI update
    setQuestions(prev =>
      prev.map(item =>
        item.id === q.id
          ? { ...item, upvotes: newUpvotes, downvotes: newDownvotes, likedBy: newLikedBy, dislikedBy: newDislikedBy }
          : item
      )
    );

    try {
      await ApiService.downvotePastQuestion(q.id, userUid);
    } catch (err) {
      console.warn('Dislike toggle error:', err);
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
    
    const fullText = `[MeDSor Çıkmış Soru - ${q.discipline} #${q.questionNumber}]\n\n${stem}\n\n${optionsText}${answer}${explanation}`;
    navigator.clipboard.writeText(fullText);
    setCopiedId(q.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  // Soruyu bağlantı olarak paylaş: telefonda paylaşım menüsü, değilse bağlantı panoya kopyalanır
  const questionLink = (q: QuestionItem) => {
    const base = (window.location.pathname.match(/^\/meds(?=\/|$)/) || [''])[0];
    return `${window.location.origin}${base}${pathFor('past_exams', String(q.id))}`;
  };
  const handleShareQuestion = async (q: QuestionItem) => {
    const url = questionLink(q);
    const title = `Çıkmış soru #${q.questionNumber || ''}${q.discipline ? ` · ${q.discipline}` : ''}`;
    if (navigator.share && window.matchMedia?.('(pointer: coarse)').matches) {
      try {
        await navigator.share({ title, url });
        return;
      } catch (e: any) {
        if (e?.name === 'AbortError') return;
      }
    }
    try {
      await navigator.clipboard.writeText(url);
      toast.success('Bağlantı kopyalandı', 'Soruyu bu bağlantıyla paylaşabilirsin.');
    } catch {
      toast.info('Bağlantı', url);
    }
  };

  // Yönetici: Çıkmış soruyu kalıcı olarak sil
  const handleDeletePastQuestion = async (targetQ: QuestionItem) => {
    if (!isAdminUser) return;
    const label = targetQ.questionNumber ? `Soru #${targetQ.questionNumber}'ı` : 'Bu çıkmış soruyu';
    const confirmMsg = `${label} (${targetQ.discipline || 'Çıkmış soru'})\n\nKalıcı olarak tüm veritabanlarından, sunucudan ve cihaz önbelleğinden silmek istediğinize emin misiniz?\n\nBu işlem geri alınamaz.`;
    if (!window.confirm(confirmMsg)) return;

    setDeletingQuestionId(targetQ.id);
    try {
      await ApiService.adminDeletePastQuestion(currentUser?.email || ADMIN_EMAIL, targetQ.id);
      try {
        await pastQuestionsCache.removeQuestions([targetQ.id]);
      } catch {}
      setQuestions((prev) => prev.filter((q) => q.id !== targetQ.id));
      toast.success('Soru Silindi', `${label} kalıcı olarak silindi.`);
    } catch (err: any) {
      toast.error('Silinemedi', err.message || 'Çıkmış soru silme işlemi başarısız oldu.');
    } finally {
      setDeletingQuestionId(null);
    }
  };

  // Soru → slayt odağı: soru kökünün ayırt edici kelimeleri + doğru şık (Öğren'de ve önizlemede işaretlenir)
  const focusFor = (q: QuestionItem, match?: QuestionLearnMatch | null): QuestionFocus =>
    buildQuestionFocus({
      id: String(q.id),
      label: `Soru #${q.questionNumber || ''}${q.discipline ? ` · ${q.discipline}` : ''}`,
      stem: String(q.reconstruction?.stem || q.stem || q.fragments?.[0]?.text || ''),
      options: (q.reconstruction?.options || q.options || []).map((o: any) => ({ key: String(o.key), text: String(o.text ?? '') })),
      answer: String(q.reconstruction?.correctAnswer || q.correctAnswer || q.claimedAnswer || doubtInfo?.resolved?.[String(q.id)]?.answer || ''),
      deckId: match?.deckId,
      slideNumber: match?.slideNumber,
    });
  const showAllQuestions = () => {
    setSharedId(null);
    writeLocation('past_exams');
  };
  // Geri/ileri: adres çubuğundaki soru kimliği izlenir
  useEffect(() => {
    const onPop = () => {
      const r = parseLocation();
      setSharedId(r.route === 'past_exams' && r.param ? r.param : null);
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);
  // Paylaşılan sorudayken arama ya da süzgeç değişirse normal listeye dönülür
  const filterSig = `${searchQuery}|${selectedCommittee}|${selectedDiscipline}|${selectedTopic}|${selectedYear}|${answerFilter}|${ambiguityTab}`;
  const firstSig = useRef(filterSig);
  useEffect(() => {
    if (sharedId && filterSig !== firstSig.current) showAllQuestions();
    firstSig.current = filterSig;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filterSig]);

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

  // Human committee name translator (Dönem 3 Resmi Programı)
  const formatCommitteeName = (cId: string) => {
    if (cId === 'donem3-kurul1') return 'Kurul 1: TIP 310 - Ürogenital ve Obstetrik';
    if (cId === 'donem3-kurul2') return 'Kurul 2: TIP 320 - Nöropsikiyatri';
    if (cId === 'donem3-kurul3') return 'Kurul 3: TIP 330 - Gastrointestinal Sistem';
    if (cId === 'donem3-kurul4') return 'Kurul 4: TIP 340 - Dolaşım, Solunum ve Tümör';
    if (cId === 'donem3-kurul5') return 'Kurul 5: TIP 350 - Ortopedi, Travmatoloji ve Hematopoetik Sistem';
    if (cId === 'donem3-kurul6') return 'Kurul 6: TIP 360 - Endokrin, Metabolizma ve Yaşlanma';
    if (cId === 'donem3-final') return 'Dönem 3 Final Sınavı (28.06.2027)';
    if (cId === 'donem3-butunleme') return 'Dönem 3 Bütünleme Sınavı (16.07.2027)';
    return cId;
  };
  const committeeShort = (cId: string) =>
    cId === 'donem3-final' ? 'Final' : cId === 'donem3-butunleme' ? 'Bütünleme' : formatCommitteeName(cId).split(':')[0];

  // --- Arama dizini: her soru için katlanmış (Türkçe) alanlar ve süzgeç değerleri bir kez hazırlanır ---
  const prepared = useMemo<Prep[]>(() => {
    const yearKey = (y?: string) => (y && y !== 'Kategorisiz' && y !== 'Çıkmış Soru' ? y : 'Kategorisiz');
    return questions.map((q) => {
      const anyQ = q as any;
      const stem = String(q.reconstruction?.stem || q.stem || q.fragments?.[0]?.text || '');
      const opts = (q.reconstruction?.options || q.options || []).map((o: any) => String(o.text || '')).join(' \n ');
      const expl = String(q.reconstruction?.explanation || anyQ.explanation || '');
      const disc = normalizeDonem3Discipline(q.discipline) || q.discipline || '';
      const content = anyQ.contentCommitteeId as string | undefined;
      const uncertain = Boolean(anyQ.committeeUncertain);
      return {
        q,
        disc,
        topic: String(q.topic || ''),
        year: yearKey(q.examYear),
        comms: uncertain ? (content ? [content] : []) : Array.from(new Set([q.committeeId, content].filter(Boolean) as string[])),
        isNew: isNewQ(q),
        isManual: Boolean(q.is_manual_entry || (q as any).manuel_ekleme || (Array.isArray(q.tags) && q.tags.includes('manuel_ekleme'))),
        isRepeated: Boolean((q.appearanceCount && q.appearanceCount > 1) || (q.similarPastQuestions && q.similarPastQuestions.length > 0) || (Array.isArray(q.tags) && q.tags.includes('tekrarlayan_soru'))),
        hasAnswer: Boolean(q.correctAnswer || q.claimedAnswer || q.reconstruction?.correctAnswer) && !(isPhase14Pending(q) && !anyQ.phase14Original?.correctAnswer),
        doubtful: isDoubtful(q),
        hasExpl: Boolean(expl.trim()),
        fields: [
          { text: foldText(stem), weight: 3 },
          { text: foldText(opts), weight: 2 },
          { text: foldText(`${q.topic || ''} \n ${disc}`), weight: 2 },
          { text: foldText(expl), weight: 0.8 },
          { text: foldText(`${q.id} ${q.examYear || ''} ${q.sourceFile || ''} ${(q.fragments || []).map((f) => f.text).join(' ')}`), weight: 0.6 },
        ],
      };
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [questions, doubtInfo]);

  const deferredQuery = useDeferredValue(searchQuery);
  const parsedQuery = useMemo(() => parseQuery(deferredQuery), [deferredQuery]);
  const hasQuery = parsedQuery.terms.length > 0 || parsedQuery.excluded.length > 0 || parsedQuery.number !== null;
  const searchScores = useMemo(() => {
    if (!hasQuery) return null;
    const m = new Map<string, number>();
    for (const p of prepared) {
      if (parsedQuery.number !== null && p.q.questionNumber !== parsedQuery.number) continue;
      const s = scoreFields(p.fields, parsedQuery);
      if (s > 0) m.set(p.q.id, s);
    }
    return m;
  }, [prepared, parsedQuery, hasQuery]);

  // --- Yönlü süzgeçler: her süzgecin sayıları, diğer tüm seçimler uygulanmış veriden hesaplanır ---
  const facetPass: Record<FacetKey, (p: Prep) => boolean> = {
    pool: (p) =>
      ambiguityTab === 'all' ||
      (ambiguityTab === 'valid' && !p.q.isAmbiguous) ||
      (ambiguityTab === 'ambiguous' && !!p.q.isAmbiguous) ||
      (ambiguityTab === 'reported' && !!p.q.reports?.length),
    committee: (p) => selectedCommittee === 'all' || p.comms.includes(selectedCommittee),
    year: (p) => selectedYear === 'all' || p.year === selectedYear,
    discipline: (p) => selectedDiscipline === 'all' || p.disc === selectedDiscipline,
    topic: (p) => selectedTopic === 'all' || p.topic === selectedTopic,
    answer: (p) =>
      answerFilter === 'all' ||
      (answerFilter === 'with' && p.hasAnswer && !p.doubtful) ||
      (answerFilter === 'without' && !p.hasAnswer) ||
      (answerFilter === 'doubtful' && p.doubtful),
    explanation: (p) => explanationFilter === 'all' || (explanationFilter === 'with') === p.hasExpl,
    source: (p) => sourceFilter === 'all' || (sourceFilter === 'gemini_v3') === isGeminiV3Question(p.q),
    p14: (p) =>
      phase14Filter === 'all' ||
      (phase14Filter === 'faz14' && isPhase14Fixed(p.q)) ||
      (phase14Filter === 'faz14_onayli' && isPhase14Fixed(p.q) && !isPhase14Pending(p.q)) ||
      (phase14Filter === 'faz14_bekleyen' && isPhase14Pending(p.q)),
    denetleyici: (p) =>
      denetleyiciFilter === 'all' ||
      (denetleyiciFilter === 'denetleyici_only' && isDenetleyiciQuestion(p.q)) ||
      (denetleyiciFilter === 'standard_only' && !isDenetleyiciQuestion(p.q)),
    newness: (p) => newnessFilter === 'all' || (newnessFilter === 'new_only') === p.isNew,
    manual: (p) =>
      manualFilter === 'all' ||
      (manualFilter === 'manual_only' && p.isManual) ||
      (manualFilter === 'standard_only' && !p.isManual),
    repeated: (p) =>
      repeatedFilter === 'all' ||
      (repeatedFilter === 'repeated_only' && p.isRepeated) ||
      (repeatedFilter === 'unique_only' && !p.isRepeated),
  };
  const facetValues: Record<FacetKey, (p: Prep) => (string | null)[]> = {
    pool: (p) => [p.q.isAmbiguous ? 'ambiguous' : 'valid', p.q.reports?.length ? 'reported' : null],
    committee: (p) => p.comms,
    year: (p) => [p.year],
    discipline: (p) => [p.disc],
    topic: (p) => [p.topic],
    answer: (p) => [p.hasAnswer && !p.doubtful ? 'with' : null, p.hasAnswer ? null : 'without', p.doubtful ? 'doubtful' : null],
    explanation: (p) => [p.hasExpl ? 'with' : 'without'],
    source: (p) => [isGeminiV3Question(p.q) ? 'gemini_v3' : 'existing'],
    p14: (p) => [isPhase14Fixed(p.q) ? 'faz14' : null, isPhase14Fixed(p.q) && !isPhase14Pending(p.q) ? 'faz14_onayli' : null, isPhase14Pending(p.q) ? 'faz14_bekleyen' : null],
    denetleyici: (p) => [isDenetleyiciQuestion(p.q) ? 'denetleyici_only' : 'standard_only'],
    newness: (p) => [p.isNew ? 'new_only' : 'archived_only'],
    manual: (p) => [p.isManual ? 'manual_only' : 'standard_only'],
    repeated: (p) => [p.isRepeated ? 'repeated_only' : 'unique_only'],
  };

  const { filteredQuestions, facetCounts } = useMemo(() => {
    const keys = Object.keys(facetPass) as FacetKey[];
    const counts = Object.fromEntries(keys.map((k) => [k, new Map<string, number>()])) as Record<FacetKey, Map<string, number>>;
    const bump = (k: FacetKey, p: Prep) => {
      const m = counts[k];
      m.set('all', (m.get('all') || 0) + 1);
      for (const v of facetValues[k](p)) if (v) m.set(v, (m.get(v) || 0) + 1);
    };
    const hits: Prep[] = [];
    for (const p of prepared) {
      if (searchScores && !searchScores.has(p.q.id)) continue;
      let failed: FacetKey | null = null;
      let fails = 0;
      for (const k of keys) {
        if (!facetPass[k](p)) {
          fails++;
          failed = k;
          if (fails > 1) break;
        }
      }
      if (fails > 1) continue;
      if (fails === 1) bump(failed!, p);
      else {
        hits.push(p);
        for (const k of keys) bump(k, p);
      }
    }
    let list = hits.map((p) => p.q);
    const yearOf = (q: QuestionItem) => parseInt((q.examYear || '').match(/\d{4}/)?.[0] || '0', 10);
    if (sortOrder === 'default' && searchScores) list.sort((a, b) => (searchScores.get(b.id) || 0) - (searchScores.get(a.id) || 0));
    if (sortOrder === 'newest') list.sort((a, b) => yearOf(b) - yearOf(a));
    if (sortOrder === 'oldest') list.sort((a, b) => (yearOf(a) || 9999) - (yearOf(b) || 9999));
    if (sortOrder === 'number') list.sort((a, b) => (a.questionNumber || 9999) - (b.questionNumber || 9999));
    if (sortOrder === 'quality_desc') list.sort((a, b) => getQualityScore(b) - getQualityScore(a));
    if (sortOrder === 'quality_asc') list.sort((a, b) => getQualityScore(a) - getQualityScore(b));
    return { filteredQuestions: list, facetCounts: counts };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [prepared, searchScores, ambiguityTab, selectedCommittee, selectedYear, selectedDiscipline, selectedTopic, answerFilter, explanationFilter, sourceFilter, phase14Filter, denetleyiciFilter, newnessFilter, manualFilter, repeatedFilter, sortOrder]);
  const fc = (k: FacetKey, v = 'all') => facetCounts[k].get(v) || 0;

  // Seçili kurul/ders artık sonuç vermiyorsa (başka seçim yüzünden) seçimi düşürme: kullanıcı neyi seçtiyse o kalır,
  // yalnızca listelerde 0 sayılı seçenekler sönük gösterilir.
  const committeeList = useMemo(
    () => ['donem3-kurul1', 'donem3-kurul2', 'donem3-kurul3', 'donem3-kurul4', 'donem3-kurul5', 'donem3-kurul6', 'donem3-final', 'donem3-butunleme'].filter((c) => questions.some((q) => q.committeeId === c || (q as any).contentCommitteeId === c)),
    [questions],
  );
  const disciplineList = useMemo(() => {
    let base = DONEM3_CURRICULUM_DISCIPLINES;
    if (selectedCommittee !== 'all' && !selectedCommittee.includes('final') && !selectedCommittee.includes('butunleme')) {
      const commObj = OFFICIAL_CURRICULUM_COMMITTEES.find((c) => c.id === selectedCommittee);
      if (commObj?.allDisciplineNames?.length) base = Array.from(new Set(commObj.allDisciplineNames.map((d) => normalizeDonem3Discipline(d) || d)));
    }
    return [...base].sort((a, b) => (facetCounts.discipline.get(b) || 0) - (facetCounts.discipline.get(a) || 0) || a.localeCompare(b, 'tr'));
  }, [selectedCommittee, facetCounts]);
  const topicList = useMemo(
    () =>
      Array.from(facetCounts.topic.entries())
        .filter(([t, n]) => t !== 'all' && t && n > 0)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 40),
    [facetCounts],
  );
  const yearList = useMemo(
    () => Array.from(new Set(prepared.map((p) => p.year))).filter((y) => !y.includes('2026') && !y.toLowerCase().includes('civan')).sort(),
    [prepared],
  );

  // Arama önerileri: yazılan kelimeyle eşleşen ders ve konular (tıklayınca süzgeç olur)
  const suggestions = useMemo(() => {
    const last = parsedQuery.terms[parsedQuery.terms.length - 1];
    if (!last || last.length < 2) return { disciplines: [] as [string, number][], topics: [] as [string, number][] };
    const disciplines = DONEM3_CURRICULUM_DISCIPLINES.filter((d) => foldText(d).includes(last))
      .map((d) => [d, prepared.filter((p) => p.disc === d).length] as [string, number])
      .filter(([, n]) => n > 0)
      .slice(0, 3);
    const tc = new Map<string, number>();
    for (const p of prepared) if (p.topic && foldText(p.topic).includes(last)) tc.set(p.topic, (tc.get(p.topic) || 0) + 1);
    const topics = Array.from(tc.entries()).sort((a, b) => b[1] - a[1]).slice(0, 5);
    return { disciplines, topics };
  }, [parsedQuery, prepared]);

  // Paginated list
  const totalPages = Math.max(1, Math.ceil(filteredQuestions.length / itemsPerPage));
  const paginatedQuestions = useMemo(() => {
    if (sharedId) return questions.filter((q) => String(q.id) === sharedId);
    const start = (currentPage - 1) * itemsPerPage;
    return filteredQuestions.slice(start, start + itemsPerPage);
  }, [filteredQuestions, currentPage, sharedId, questions]);

  const resetPage = () => setCurrentPage(1);
  const LABELS = {
    pool: { valid: 'Tam metin', ambiguous: 'İncelemede', reported: 'Hata bildirilen', all: 'Tüm havuz' } as Record<string, string>,
    answer: { with: 'Cevaplı', without: 'Cevapsız', doubtful: 'Cevap belirsiz' } as Record<string, string>,
    source: { gemini_v3: 'Gemini v3', existing: 'Mevcut veriler' } as Record<string, string>,
    p14: { faz14: 'Faz 14', faz14_onayli: 'Faz 14 · onaylı', faz14_bekleyen: 'Faz 14 · onay bekliyor' } as Record<string, string>,
    denetleyici: { denetleyici_only: 'Denetleyici Onayı', standard_only: 'Standart' } as Record<string, string>,
    newness: { new_only: 'Yeni sorular', archived_only: 'Arşiv' } as Record<string, string>,
    manual: { manual_only: 'Manuel Eklenenler', standard_only: 'Otomatik Havuz' } as Record<string, string>,
    repeated: { repeated_only: 'Tekrarlayan Sorular', unique_only: 'Tekil Sorular' } as Record<string, string>,
    sort: { newest: 'Yeniden eskiye', oldest: 'Eskiden yeniye', number: 'Soru numarası', quality_desc: 'Kalite: en iyi önce', quality_asc: 'Kalite: en sorunlu önce', default: searchQuery.trim() ? 'En ilgili' : 'Varsayılan' } as Record<string, string>,
    view: { raw: 'Ham metin', split: 'Karşılaştır' } as Record<string, string>,
  };
  // Şeritte görünmeyen etkin süzgeçler kaldırılabilir çip olarak listelenir
  const activeFilterChips: { label: string; clear: () => void }[] = [
    ...(ambiguityTab !== 'valid' ? [{ label: LABELS.pool[ambiguityTab], clear: () => setAmbiguityTab('valid') }] : []),
    ...(selectedDiscipline !== 'all' ? [{ label: selectedDiscipline, clear: () => { setSelectedDiscipline('all'); setSelectedTopic('all'); } }] : []),
    ...(selectedTopic !== 'all' ? [{ label: selectedTopic, clear: () => setSelectedTopic('all') }] : []),
    ...(selectedYear !== 'all' ? [{ label: selectedYear, clear: () => setSelectedYear('all') }] : []),
    ...(answerFilter !== 'all' ? [{ label: LABELS.answer[answerFilter], clear: () => setAnswerFilter('all') }] : []),
    ...(explanationFilter !== 'all' ? [{ label: explanationFilter === 'with' ? 'Açıklamalı' : 'Açıklamasız', clear: () => setExplanationFilter('all') }] : []),
    ...(sourceFilter !== 'all' ? [{ label: LABELS.source[sourceFilter], clear: () => setSourceFilter('all') }] : []),
    ...(denetleyiciFilter !== 'all' ? [{ label: LABELS.denetleyici[denetleyiciFilter], clear: () => setDenetleyiciFilter('all') }] : []),
    ...(phase14Filter !== 'all' ? [{ label: LABELS.p14[phase14Filter], clear: () => setPhase14Filter('all') }] : []),
    ...(newnessFilter !== 'all' ? [{ label: LABELS.newness[newnessFilter], clear: () => setNewnessFilter('all') }] : []),
    ...(manualFilter !== 'all' ? [{ label: LABELS.manual[manualFilter], clear: () => setManualFilter('all') }] : []),
    ...(repeatedFilter !== 'all' ? [{ label: LABELS.repeated[repeatedFilter], clear: () => setRepeatedFilter('all') }] : []),
    ...(viewMode !== 'redacted' ? [{ label: LABELS.view[viewMode], clear: () => setViewMode('redacted') }] : []),
  ];
  const advancedCount = activeFilterChips.length;
  const anyFilter = advancedCount > 0 || selectedCommittee !== 'all' || searchQuery.trim() !== '';
  const clearAllFilters = () => {
    setSearchQuery('');
    setAmbiguityTab('valid');
    setDeepseekFilter('all');
    setSourceFilter('all');
    setDenetleyiciFilter('all');
    setNewnessFilter('all');
    setManualFilter('all');
    setRepeatedFilter('all');
    setSelectedCommittee('all');
    setSelectedYear('all');
    setSelectedDiscipline('all');
    setSelectedTopic('all');
    setViewMode('redacted');
    setAnswerFilter('all');
    setExplanationFilter('all');
    setPhase14Filter('all');
    setSortOrder('default');
    setCurrentPage(1);
  };
  const isAdminUser = currentUser?.email === ADMIN_EMAIL || !!currentUser?.isAdmin;
  const n = (v: number) => v.toLocaleString('tr-TR');

  // Bölümlü seçim (filtre çekmecesi): seçenek sayıları canlı
  const segRow = <T extends string>(label: string, value: T, set: (v: T) => void, opts: [T, string, number?][]) => (
    <div className="ms-facet">
      <div className="ms-facet-head">{label}</div>
      <div className="ms-facet-list" role="radiogroup" aria-label={label}>
        {opts.map(([id, text, count]) => (
          <button
            key={id}
            type="button"
            role="radio"
            aria-checked={value === id}
            onClick={() => { set(id); resetPage(); }}
            className={`ms-fchip ${value === id ? 'is-on' : ''} ${count === 0 && value !== id ? 'is-zero' : ''}`}
          >
            {value === id && <Check aria-hidden />}
            {text}
            {typeof count === 'number' && <span className="n">{n(count)}</span>}
          </button>
        ))}
      </div>
    </div>
  );

  return (
    <div className="cx">
      {/* Başlık: ad + canlı sayı; yönetici araçları sağda */}
      <header className="cx-head">
        <h1 className="ms-page-title cx-title">Çıkmış sorular</h1>
        <span className="cx-count" aria-live="polite">{n(filteredQuestions.length)} <small>soru</small></span>
        <span className="cx-head-tools">
          {isAdminUser && (
            <a href={pathFor('test_cikmis')} className="cx-iconbtn" title="Faz 14 düzeltme önerilerini incele" aria-label="Faz 14 incelemesi">
              <Sparkles />
            </a>
          )}
          <button
            type="button"
            onClick={handleManualSync}
            disabled={cacheStatus.isSyncing}
            aria-label="Güncellemeleri denetle"
            title={`Cihazda ${n(questions.length)} soru · güncellemeleri denetle`}
            className="cx-iconbtn"
          >
            <RefreshCw className={cacheStatus.isSyncing ? 'animate-spin' : ''} />
          </button>
        </span>
      </header>

      {/* Arama ve filtre tek kontrol */}
      <div className="cx-search">
        <Search aria-hidden />
        <input
          ref={searchRef}
          type="search"
          value={searchQuery}
          onChange={(e) => { setSearchQuery(e.target.value); resetPage(); setSuggestOpen(true); }}
          onFocus={() => setSuggestOpen(true)}
          onBlur={() => window.setTimeout(() => setSuggestOpen(false), 120)}
          onKeyDown={(e) => {
            if (e.key === 'Escape') { if (searchQuery) setSearchQuery(''); else (e.target as HTMLInputElement).blur(); }
            if (e.key === 'Enter') setSuggestOpen(false);
          }}
          placeholder="Kök, şık, konu ya da #numara"
          aria-label="Çıkmış sorularda ara"
          autoComplete="off"
        />
        {searchQuery ? (
          <button type="button" onClick={() => { setSearchQuery(''); searchRef.current?.focus(); }} aria-label="Aramayı temizle" className="cx-search-x">
            <X />
          </button>
        ) : (
          <kbd className="ms-kbd cx-kbd" aria-hidden>/</kbd>
        )}
        <span className="cx-search-sep" aria-hidden />
        <button
          type="button"
          onClick={() => setFiltersOpen(true)}
          aria-haspopup="dialog"
          aria-label={`Filtreler${advancedCount ? `, ${advancedCount} etkin` : ''}`}
          title="Ders, konu, yıl, cevap ve diğer filtreler"
          className={`cx-filterbtn ${advancedCount ? 'is-on' : ''}`}
        >
          <SlidersHorizontal />
          <span className="cx-filterbtn-l">Filtre</span>
          {advancedCount > 0 && <b>{advancedCount}</b>}
        </button>
        {suggestOpen && searchQuery.trim().length >= 2 && (
          <div className="ms-suggest" role="listbox" aria-label="Arama önerileri" onMouseDown={(e) => e.preventDefault()}>
            <button type="button" className="ms-suggest-row is-active" onClick={() => setSuggestOpen(false)}>
              <Search aria-hidden />
              <span className="min-w-0 truncate">“{searchQuery.trim()}” için sonuçlar</span>
              <span className="n">{n(filteredQuestions.length)}</span>
            </button>
            {suggestions.disciplines.length > 0 && <div className="ms-suggest-label">Ders olarak süz</div>}
            {suggestions.disciplines.map(([d, c]) => (
              <button key={d} type="button" className="ms-suggest-row" onClick={() => { setSelectedDiscipline(d); setSelectedTopic('all'); setSearchQuery(''); setSuggestOpen(false); resetPage(); }}>
                <BookOpen aria-hidden /> <span className="min-w-0 truncate">{d}</span> <span className="n">{n(c)}</span>
              </button>
            ))}
            {suggestions.topics.length > 0 && <div className="ms-suggest-label">Konu olarak süz</div>}
            {suggestions.topics.map(([t, c]) => (
              <button key={t} type="button" className="ms-suggest-row" onClick={() => { setSelectedTopic(t); setSearchQuery(''); setSuggestOpen(false); resetPage(); }}>
                <Tag aria-hidden /> <span className="min-w-0 truncate">{t}</span> <span className="n">{n(c)}</span>
              </button>
            ))}
            <p className="ms-suggest-tip m-0">
              <code>"tam ifade"</code> · <code>-hariç</code> · <code>#12</code> soru numarası. Türkçe karakter fark etmez.
            </p>
          </div>
        )}
      </div>

      {/* Kurul sekmeleri + sıralama/kendini sına aynı rayda (telefonda alt alta) */}
      <div className="cx-rail">
      <nav className="cx-tabs" aria-label="Kurul" onWheel={(e) => { if (e.deltaY) e.currentTarget.scrollLeft += e.deltaY; }}>
        {[['all', 'Tümü'] as [string, string], ...committeeList.map((c) => [c, committeeShort(c)] as [string, string])].map(([c, label]) => {
          const on = selectedCommittee === c;
          const cnt = c === 'all' ? fc('committee') : fc('committee', c);
          return (
            <button
              key={c}
              type="button"
              aria-pressed={on}
              title={c === 'all' ? 'Tüm kurullar' : formatCommitteeName(c)}
              className={`cx-tab ${on ? 'is-on' : ''} ${cnt === 0 && !on ? 'is-zero' : ''}`}
              onClick={() => {
                setSelectedCommittee(c);
                resetPage();
                if (c !== 'all' && selectedDiscipline !== 'all') {
                  const commObj = OFFICIAL_CURRICULUM_COMMITTEES.find((x) => x.id === c);
                  if (commObj && !commObj.allDisciplineNames.map((d) => normalizeDonem3Discipline(d) || d).includes(selectedDiscipline)) setSelectedDiscipline('all');
                }
              }}
            >
              {label.replace(/^Kurul\s*/i, 'K')}
              <small>{n(cnt)}</small>
            </button>
          );
        })}
      </nav>

      {/* Etkin filtreler + sıralama + kendini sına */}
      <div className="cx-bar">
        <span className="cx-bar-sp" />
        <label className="cx-sort" title="Sırala">
          <ArrowUpDown aria-hidden />
          <span>{LABELS.sort[sortOrder]}</span>
          <select value={sortOrder} onChange={(e) => { setSortOrder(e.target.value as any); resetPage(); }} aria-label="Sırala">
            <option value="default">{LABELS.sort.default}</option>
            <option value="quality_desc">Kalite: en iyi önce</option>
            <option value="quality_asc">Kalite: en sorunlu önce</option>
            <option value="newest">Yeniden eskiye</option>
            <option value="oldest">Eskiden yeniye</option>
            <option value="number">Soru numarası</option>
          </select>
        </label>
        <button
          type="button"
          role="switch"
          aria-checked={quizMode}
          onClick={() => setQuizMode((v) => !v)}
          title={quizMode ? 'Cevaplar gizli: şıkkı işaretleyince doğru cevap görünür' : 'Cevapları gizleyip kendini sına'}
          className={`cx-quiz ${quizMode ? 'is-on' : ''}`}
        >
          <span className="cx-switch" aria-hidden><i /></span>
          Kendini sına
        </button>
      </div>
      </div>
      {activeFilterChips.length > 0 && (
        <div className="cx-chips">
          {activeFilterChips.map((c) => (
            <button key={c.label} type="button" onClick={() => { c.clear(); resetPage(); }} className="cx-chip" aria-label={`${c.label} filtresini kaldır`}>
              <span>{c.label}</span>
              <X aria-hidden />
            </button>
          ))}
          {anyFilter && <button type="button" onClick={clearAllFilters} className="cx-clear">Temizle</button>}
        </div>
      )}

      {/* Gelişmiş filtreler: yan çekmece (telefonda alttan) */}
      {filtersOpen && (
        <>
          <div className={`ms-drawer-scrim ${filtersClosing ? 'is-closing' : ''}`} onClick={() => closeFilters()} aria-hidden />
          <div className={`ms-drawer ${filtersClosing ? 'is-closing' : ''}`} role="dialog" aria-modal="true" aria-labelledby="cikmis-filter-title" onKeyDown={(e) => e.key === 'Escape' && closeFilters()}>
            <header className="ms-drawer-head">
              <h2 id="cikmis-filter-title" className="ms-drawer-title">Filtreler</h2>
              <button type="button" onClick={() => closeFilters()} aria-label="Kapat" className="ms-btn is-ghost is-icon" autoFocus>
                <X />
              </button>
            </header>
            <div className="ms-drawer-body">
              <div className="ms-facet">
                <div className="ms-facet-head">
                  Ders
                  {selectedDiscipline !== 'all' && <button type="button" onClick={() => { setSelectedDiscipline('all'); setSelectedTopic('all'); resetPage(); }}>Temizle</button>}
                </div>
                {disciplineList.length > 10 && (
                  <div className="ms-qsearch h-9! rounded-xl!">
                    <Search aria-hidden />
                    <input value={facetQuery} onChange={(e) => setFacetQuery(e.target.value)} placeholder="Ders ara" aria-label="Ders ara" />
                  </div>
                )}
                <div className="ms-facet-list ms-facet-scroll">
                  {disciplineList
                    .filter((d) => !facetQuery || foldText(d).includes(foldText(facetQuery)))
                    .map((d) => {
                      const on = selectedDiscipline === d;
                      const cnt = fc('discipline', d);
                      if (!cnt && !on) return null;
                      return (
                        <button key={d} type="button" aria-pressed={on} onClick={() => { setSelectedDiscipline(on ? 'all' : d); setSelectedTopic('all'); resetPage(); }} className={`ms-fchip ${on ? 'is-on' : ''}`}>
                          {on && <Check aria-hidden />} {d} <span className="n">{n(cnt)}</span>
                        </button>
                      );
                    })}
                </div>
              </div>

              {(selectedDiscipline !== 'all' || selectedTopic !== 'all') && topicList.length > 0 && (
                <div className="ms-facet">
                  <div className="ms-facet-head">
                    Konu
                    {selectedTopic !== 'all' && <button type="button" onClick={() => { setSelectedTopic('all'); resetPage(); }}>Temizle</button>}
                  </div>
                  <div className="ms-facet-list ms-facet-scroll">
                    {topicList.map(([t, cnt]) => {
                      const on = selectedTopic === t;
                      return (
                        <button key={t} type="button" aria-pressed={on} onClick={() => { setSelectedTopic(on ? 'all' : t); resetPage(); }} className={`ms-fchip ${on ? 'is-on' : ''}`}>
                          {on && <Check aria-hidden />} <span className="truncate max-w-[260px]">{t}</span> <span className="n">{n(cnt)}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              {segRow('Cevap', answerFilter, setAnswerFilter, [
                ['all', 'Tümü', fc('answer')],
                ['with', 'Cevaplı', fc('answer', 'with')],
                ['without', 'Cevapsız', fc('answer', 'without')],
                ['doubtful', 'Belirsiz', fc('answer', 'doubtful')],
              ])}
              {segRow('Açıklama', explanationFilter, setExplanationFilter, [
                ['all', 'Tümü', fc('explanation')],
                ['with', 'Var', fc('explanation', 'with')],
                ['without', 'Yok', fc('explanation', 'without')],
              ])}
              {segRow('Yıl', selectedYear, setSelectedYear, [['all', 'Tümü', fc('year')], ...yearList.map((y) => [y, y, fc('year', y)] as [string, string, number])])}
              {segRow('Havuz', ambiguityTab, setAmbiguityTab, [
                ['valid', 'Tam metin', fc('pool', 'valid')],
                ['ambiguous', 'İncelemede', fc('pool', 'ambiguous')],
                ['reported', 'Hata bildirilen', fc('pool', 'reported')],
                ['all', 'Tümü', fc('pool')],
              ])}
              {segRow('Yenilik', newnessFilter, setNewnessFilter, [
                ['all', 'Tümü', fc('newness')],
                ['new_only', 'Yeni', fc('newness', 'new_only')],
                ['archived_only', 'Arşiv', fc('newness', 'archived_only')],
              ])}
              {segRow('Kaynak', sourceFilter, setSourceFilter, [
                ['all', 'Tümü', fc('source')],
                ['gemini_v3', 'Gemini v3', fc('source', 'gemini_v3')],
                ['existing', 'Mevcut', fc('source', 'existing')],
              ])}
              {segRow('Denetleyici onayı', denetleyiciFilter, setDenetleyiciFilter, [
                ['all', 'Tümü', fc('denetleyici')],
                ['denetleyici_only', 'Onaylı', fc('denetleyici', 'denetleyici_only')],
                ['standard_only', 'Onaysız', fc('denetleyici', 'standard_only')],
              ])}
              {segRow('AI İnceleme ve Denetim', phase14Filter, setPhase14Filter, [
                ['all', 'Tümü', fc('p14')],
                ['faz14', 'Faz 14', fc('p14', 'faz14')],
                ['faz14_onayli', 'Onaylı', fc('p14', 'faz14_onayli')],
                ['faz14_bekleyen', 'Onay bekliyor', fc('p14', 'faz14_bekleyen')],
              ])}
              {segRow('Yükleme Türü', manualFilter, setManualFilter, [
                ['all', 'Tümü', fc('manual')],
                ['manual_only', 'Manuel Eklenenler', fc('manual', 'manual_only')],
                ['standard_only', 'Otomatik Havuz', fc('manual', 'standard_only')],
              ])}
              {segRow('Soru Tekrarı', repeatedFilter, setRepeatedFilter, [
                ['all', 'Tümü', fc('repeated')],
                ['repeated_only', 'Tekrarlayanlar', fc('repeated', 'repeated_only')],
                ['unique_only', 'Tekil Sorular', fc('repeated', 'unique_only')],
              ])}
              {segRow('Görünüm', viewMode, setViewMode, [
                ['redacted', 'Düzenlenmiş'],
                ['raw', 'Ham metin'],
                ['split', 'Karşılaştır'],
              ])}
            </div>
            <footer className="ms-drawer-foot">
              <button type="button" onClick={clearAllFilters} className="ms-btn">Sıfırla</button>
              <button type="button" onClick={() => closeFilters()} className="ms-btn is-primary">
                {n(filteredQuestions.length)} soruyu göster
              </button>
            </footer>
          </div>
        </>
      )}

      {/* Questions Listing */}
      {isLoading ? (
        <div className="bg-white rounded-2xl border border-line">
          <SectionLoader variant="book" label="Çıkmış sorular yükleniyor…" />
        </div>
      ) : sharedId && paginatedQuestions.length === 0 ? (
        <div className="ms-qcard items-center text-center py-10">
          <HelpCircle className="w-8 h-8 text-ink-3" />
          <p className="m-0 font-display text-[18px] font-semibold">Paylaşılan soru bulunamadı</p>
          <p className="m-0 text-[13.5px] text-ink-2 max-w-sm">Soru kaldırılmış, birleştirilmiş ya da bağlantı eksik olabilir.</p>
          <button type="button" onClick={showAllQuestions} className="ms-btn is-tonal">Tüm çıkmış sorular</button>
        </div>
      ) : paginatedQuestions.length === 0 ? (
        <div className="ms-qcard items-center text-center py-10">
          <HelpCircle className="w-8 h-8 text-ink-3" />
          <p className="m-0 font-display text-[18px] font-semibold">Eşleşen soru yok</p>
          <p className="m-0 text-[13.5px] text-ink-2 max-w-sm">
            {searchQuery.trim() ? 'Kelimeyi kısaltmayı ya da bir süzgeci kaldırmayı dene.' : 'Seçili süzgeçlerin hepsine uyan soru yok.'}
          </p>
          <button type="button" onClick={clearAllFilters} className="ms-btn is-tonal">Filtreleri temizle</button>
        </div>
      ) : (
        <div className="cx-list" key={`${currentPage}-${filteredQuestions.length}-${sharedId || ''}`}>
          {sharedId && (
            <div className="ms-shared-band" role="status">
              <Share2 className="w-4 h-4 shrink-0" aria-hidden />
              <span className="min-w-0 flex-1">Paylaşılan soru gösteriliyor</span>
              <button type="button" onClick={showAllQuestions} className="ms-btn is-ghost is-sm">Tüm sorular <ChevronRight /></button>
            </div>
          )}
          {paginatedQuestions.map((q) => {
            const effectiveMode: 'redacted' | 'raw' | 'split' = cardViewOverrides[q.id] || viewMode;
            const userUid = currentUser?.uid || currentUser?.email || 'anonim-std';
            const isLiked = (q.likedBy || []).includes(userUid);
            const isDisliked = (q.dislikedBy || []).includes(userUid);
            const isNewQuestion = isNewQ(q);

            const learnMatch = learnMatcher.getMatch(q);
            // Mavi ⋯ ve "Öğren slaytı" kısayolu yalnızca güvenilir eşleşmelerde
            const reliableLearn = isReliableLearnMatch(learnMatch) ? learnMatch : null;

            const isDenetleyici = isDenetleyiciQuestion(q);
            const denetleyiciData = (q as any).denetleyiciSurumu || {};
            const eskiData = (q as any).eskiSurum || (q as any).phase14Original || {};
            const activeVersion: 'denetleyici' | 'eski' | 'karsilastir' =
              versionViewOverrides[q.id] || (isDenetleyici ? 'denetleyici' : 'eski');

            const isEskiView = activeVersion === 'eski';
            const isCompareView = activeVersion === 'karsilastir';

            const stem = isEskiView && eskiData.stem
              ? String(eskiData.stem)
              : String(q.reconstruction?.stem || q.stem || q.fragments?.[0]?.text || q.topic || '');
            const options = isEskiView && eskiData.options && eskiData.options.length > 0
              ? eskiData.options
              : (q.reconstruction?.options || q.options || []);
            const correctAnswer = isEskiView && eskiData.correctAnswer
              ? eskiData.correctAnswer
              : (q.reconstruction?.correctAnswer || q.correctAnswer || q.claimedAnswer);
            const explanation = isEskiView
              ? (eskiData.explanation || '')
              : (q.reconstruction?.explanation || q.explanation);

            const saObj = (q as any).sik_analizi || denetleyiciData.sik_analizi;
            const saEntries = saObj && typeof saObj === 'object' ? Object.entries(saObj).sort(([a], [b]) => a.localeCompare(b)) : [];
            const refList: string[] = normalizeRefList((q as any).referans_kaynaklar ?? denetleyiciData.referans_kaynaklar);
            const answerChanged = isDenetleyici && Boolean(eskiData.correctAnswer && eskiData.correctAnswer !== (q.correctAnswer || q.claimedAnswer));

            const doubtful = isDoubtful(q);
            // Asıl kayıtta cevap yoksa (onay bekleyen AI cevabı sayılmaz) ya da cevap tartışmalıysa şıklar ankete döner
            const keyMissing = !correctAnswer || (isPhase14Pending(q) && !(q as any).phase14Original?.correctAnswer);
            // Cevabı yöneticice kabul edilmiş ama anketi açık tutulan soru: kabul edilen cevap + topluluk oyları
            const acceptedPoll = !doubtful ? doubtInfo?.resolved?.[String(q.id)]?.answer : undefined;
            const pollMode = options.length >= 2 && (doubtful || keyMissing || Boolean(acceptedPoll));
            // Faz 14 düzeltmesi: öncesi (phase14Original) ve model notları; ⓘ simgeleri yalnız düzeltilmiş sorularda
            const p14Fixed = isPhase14Fixed(q);
            const p14o: any = p14Fixed ? (q as any).phase14Original || {} : null;
            const p14s: any = p14Fixed ? (q as any).phase14?.summary : null;
            const p14Note = (k: string) => (p14s && typeof p14s === 'object' ? p14s[k] : undefined) as string | undefined;
            const norm = (t: any) => String(t ?? '').replace(/\s+/g, ' ').trim();
            const oldOpt = (key: string) => {
              const o = (p14o?.options || []).find((x: any) => String(x.key).toUpperCase() === String(key).toUpperCase());
              return o ? String(o.text ?? '') : '';
            };
            const commentsCount = (q as any).comments?.length || 0;
            const meta = ((q as any).committeeUncertain
              ? [(q as any).contentCommitteeId ? committeeShort((q as any).contentCommitteeId) : 'Kurul belirsiz', q.examYear]
              : [q.discipline || 'Tıp', committeeShort((q as any).contentCommitteeId || q.committeeId), q.examYear]
            ).filter(Boolean).join(' · ');
            const setCardMode = (m: 'redacted' | 'raw' | 'split') => setCardViewOverrides((prev) => ({ ...prev, [q.id]: m }));
            const picked = picks[q.id];
            const hideAnswer = quizMode && !picked;
            const terms = parsedQuery.terms;
            const explChangedP14 = p14Fixed && norm(p14o?.explanation) !== norm(explanation);

            const actions: ActionItem[] = [
              ...(reliableLearn
                ? [{ label: 'Öğren slaytı', icon: GraduationCap, group: 'Öğren', tone: 'accent' as const, hint: `slayt ${reliableLearn.slideNumber}`, onClick: () => setSelectedLearnMatch({ question: q, match: reliableLearn }) }]
                : []),
              ...(aiQueue[String(q.id)]
                ? [{ label: aiQueue[String(q.id)].status === 'yonetici_onayi' ? 'İncelendi · yönetici onayında' : `İncelemede · sıra ${aiQueue[String(q.id)].position}`, icon: Sparkles, group: 'Yapay zekâ', disabled: aiQueue[String(q.id)].status === 'yonetici_onayi', hint: aiQueue[String(q.id)].status === 'yonetici_onayi' ? undefined : 'not ekle', onClick: () => setAiReviewQ(q) }]
                : [{ label: 'İncelemeye gönder', icon: Sparkles, group: 'Yapay zekâ', tone: 'accent' as const, onClick: () => setAiReviewQ(q) }]),
              ...(isAdminUser
                ? [{ label: 'AI ile düzenle', icon: Wand2, group: 'Yapay zekâ', tone: 'accent' as const, onClick: () => setCustomRedactQuestion({ question: q, match: getQuestionSlideMatch(q) }) }]
                : []),
              ...(isDenetleyici
                ? [
                    { label: 'Denetleyici Sürümü (Yeni)', icon: ShieldCheck, group: 'Sürüm', hint: activeVersion === 'denetleyici' ? '✓' : undefined, onClick: () => setVersionViewOverrides((prev) => ({ ...prev, [q.id]: 'denetleyici' })) },
                    { label: 'Eski Sürüm', icon: History, group: 'Sürüm', hint: activeVersion === 'eski' ? '✓' : undefined, onClick: () => setVersionViewOverrides((prev) => ({ ...prev, [q.id]: 'eski' })) },
                    { label: 'Sürümleri Karşılaştır', icon: Layers, group: 'Sürüm', hint: activeVersion === 'karsilastir' ? '✓' : undefined, onClick: () => setVersionViewOverrides((prev) => ({ ...prev, [q.id]: 'karsilastir' })) },
                  ]
                : []),
              { label: 'Düzenlenmiş', icon: Sparkles, group: 'Görünüm', hint: effectiveMode === 'redacted' ? '✓' : undefined, onClick: () => setCardMode('redacted') },
              { label: 'Ham metin', icon: FileText, group: 'Görünüm', hint: effectiveMode === 'raw' ? '✓' : undefined, onClick: () => setCardMode('raw') },
              { label: 'Karşılaştır', icon: Layers, group: 'Görünüm', hint: effectiveMode === 'split' ? '✓' : undefined, onClick: () => setCardMode('split') },
              { label: 'Hakkında', icon: Info, group: 'Soru', hint: learnMatch ? `slayt ${learnMatch.slideNumber}` : undefined, onClick: () => setAboutQuestion(q) },
              ...(!pollMode && options.length >= 2
                ? [{ label: 'Ankete aç', icon: BarChart3, group: 'Soru', hint: 'topluluk oylasın', onClick: () => openPoll(q) }]
                : []),
              ...(p14Fixed
                ? [{ label: p14Open[q.id] ? 'Düzeltme öncesini gizle' : 'Düzeltme öncesini göster', icon: Info, group: 'Diğer', onClick: () => setP14Open((o) => ({ ...o, [q.id]: !o[q.id] })) }]
                : []),
              { label: copiedId === q.id ? 'Kopyalandı' : 'Metni kopyala', icon: Copy, group: 'Soru', onClick: () => handleCopyQuestion(q) },
              { label: 'Kaynak dosyayı göster', icon: FileText, group: 'Diğer', onClick: () => setSelectedRawSourceQuestion(q) },
              ...(correctAnswer && options.some((o: any) => String(o.key) === String(correctAnswer))
                ? [{ label: `Cevaba itiraz et (${correctAnswer})`, icon: ShieldAlert, group: 'Diğer', onClick: () => setObjection({ question: q, option: { key: String(correctAnswer), text: String(options.find((o: any) => String(o.key) === String(correctAnswer))?.text ?? '') } }) }]
                : []),
              { label: 'Hata bildir', icon: Flag, group: 'Diğer', tone: 'danger', onClick: () => setReportingQuestion(q) },
              ...(isAdminUser
                ? [
                    {
                      label: deletingQuestionId === q.id ? 'Siliniyor…' : 'Soruyu kalıcı sil',
                      icon: Trash2,
                      group: 'Yönetici',
                      tone: 'danger' as const,
                      disabled: deletingQuestionId === q.id,
                      onClick: () => handleDeletePastQuestion(q),
                    },
                  ]
                : []),
            ];

            return (
              <article key={q.id} className="cx-q">
                <header className="cx-q-head">
                  <span className={`cx-q-no ${q.questionNumber ? '' : 'is-none'}`} title={q.questionNumber ? `Soru ${q.questionNumber}` : 'Soru numarası bilinmiyor'}>{q.questionNumber || '?'}</span>
                  <span className="cx-q-meta" title={formatCommitteeName(q.committeeId)}>
                    <b>{(q as any).committeeUncertain ? 'Kurul belirsiz' : q.discipline || 'Tıp'}</b>
                    <span>{[(q as any).committeeUncertain ? ((q as any).contentCommitteeId ? committeeShort((q as any).contentCommitteeId) : null) : committeeShort((q as any).contentCommitteeId || q.committeeId), q.examYear].filter(Boolean).join(' · ')}</span>
                  </span>
                  <span className="cx-q-flags">
                    {q.reports && q.reports.length > 0 && (
                      <span className="cx-flag is-bad" title={`${q.reports.length} hata bildirimi`}><Flag aria-hidden />{q.reports.length}</span>
                    )}
                    {pollMode && (
                      <span className={`cx-flag ${acceptedPoll ? 'is-ok' : 'is-warn'}`} title={acceptedPoll ? 'Cevap kabul edildi; anket açık' : doubtful ? 'Cevap anahtarı tartışmalı' : 'Cevap anahtarı yok'}>
                        <BarChart3 aria-hidden />{acceptedPoll ? 'Anket' : doubtful ? 'Belirsiz' : 'Cevapsız'}
                      </span>
                    )}
                    {aiQueue[String(q.id)] && (
                      <span className="cx-flag is-ai" title={aiQueue[String(q.id)].status === 'yonetici_onayi' ? 'Yapay zekâ inceledi; cevap belirsiz olduğu için yönetici onayı bekliyor' : `Yapay zekâ inceleme kuyruğunda (${aiQueue[String(q.id)].requests} istek)`}>
                        <Sparkles aria-hidden />{aiQueue[String(q.id)].status === 'yonetici_onayi' ? 'Onayda' : `Sırada ${aiQueue[String(q.id)].position}`}
                      </span>
                    )}
                    {q.isAmbiguous && <span className="cx-flag is-warn">Eksik</span>}
                    {isNewQuestion && <span className="cx-flag is-new">Yeni</span>}
                    {(() => {
                      const qs = getQualityScore(q);
                      const tier = getQualityTier(q);
                      const cls = tier === 'altin' ? 'is-ok' : tier === 'saglam' ? 'is-new' : tier === 'orta' ? '' : tier === 'zayif' ? 'is-warn' : 'is-bad';
                      const label = tier === 'altin' ? 'Altın' : tier === 'saglam' ? 'Sağlam' : tier === 'orta' ? 'Orta' : tier === 'zayif' ? 'Zayıf' : 'Kritik';
                      const iss = ((q as any).qualityIssues || []) as string[];
                      return (
                        <span className={`cx-flag ${cls}`} title={`Kalite ${qs}/100 · ${label}${iss.length ? ` · ${iss.join(', ')}` : ''}`}>
                          Q{qs}
                        </span>
                      );
                    })()}
                    {((q as any).customRedactedBy === 'muse' || (q.tags || []).includes('redacted_by_muse')) && (
                      <span className="cx-flag is-ai" title={(q as any).museRedactionNote || 'muse tarafından yazım/biçim yönünden düzenlendi; eski hâli kayıtta saklı'}>
                        muse
                      </span>
                    )}
                    {(q.is_manual_entry || (q as any).manuel_ekleme) && (
                      <span className="cx-flag is-new" title="Bu soru resmi geçmiş kurul sınavı PDF'inden elle doğrulanıp eklenmiştir.">Manuel Ekleme</span>
                    )}
                    {q.similarPastQuestions && q.similarPastQuestions.length > 0 && (
                      <span className="cx-flag is-ai" title={`${q.similarPastQuestions.length + 1} farklı sınavda çıkan soru`}>
                        <Layers aria-hidden className="w-3 h-3 inline mr-0.5" />
                        {q.similarPastQuestions.length + 1} Sınavda Çıktı
                      </span>
                    )}
                    {isDenetleyici && <span className="cx-flag is-ok is-icon" title="Denetleyici onayı: müfredat ve mekanizma doğrulamalı sürüm" aria-label="Denetleyici onaylı"><ShieldCheck /></span>}
                    {p14Fixed && (
                      <button
                        type="button"
                        onClick={() => setP14Open((o) => ({ ...o, [q.id]: !o[q.id] }))}
                        aria-expanded={!!p14Open[q.id]}
                        className={`cx-flag is-ai ${isPhase14Pending(q) ? '' : 'is-icon'}`}
                        title={isPhase14Pending(q) ? 'Düzeltme onay bekliyor: değişiklikleri gör' : 'Yapay zekâ incelemesinde düzeltildi: değişiklikleri ve öncesini gör'}
                        aria-label="Düzeltme ayrıntıları"
                      >
                        <Sparkles aria-hidden />{isPhase14Pending(q) ? 'Onay bekliyor' : null}
                      </button>
                    )}
                    {isAdminUser && isGeminiV3Question(q) && <span className="cx-flag is-ai">Gemini v3</span>}
                  </span>
                  {isDenetleyici && (
                    <span role="group" aria-label="Soru sürümü" className="cx-ver">
                      {([
                        ['denetleyici', ShieldCheck, 'Denetleyici sürümü (yeni)'],
                        ['eski', History, 'Eski sürüm (ham çıkmış sınav)'],
                        ['karsilastir', Layers, 'Sürümleri karşılaştır'],
                      ] as const).map(([v, Icon, label]) => (
                        <button key={v} type="button" onClick={() => setVersionViewOverrides((prev) => ({ ...prev, [q.id]: v }))} aria-pressed={activeVersion === v} aria-label={label} title={label}>
                          <Icon />
                        </button>
                      ))}
                    </span>
                  )}
                  {isAdminUser && (
                    <button
                      type="button"
                      className="cx-iconbtn text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-950/30"
                      title="Soruyu kalıcı sil (Yönetici)"
                      aria-label="Soruyu kalıcı sil"
                      disabled={deletingQuestionId === q.id}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeletePastQuestion(q);
                      }}
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                  <ActionMenu
                    items={actions}
                    title={`Soru #${q.questionNumber}`}
                    highlight={reliableLearn ? { icon: GraduationCap, title: `Öğren slaytı var (slayt ${reliableLearn.slideNumber})` } : undefined}
                  />
                </header>

                {p14Fixed && p14Open[q.id] && (() => {
                  const o: any = (q as any).phase14Original || {};
                  const p14: any = (q as any).phase14 || {};
                  return (
                    <div className="ms-pop-in rounded-xl bg-field px-3 py-2.5 text-[13px] text-ink-2 flex flex-col gap-1.5">
                      <p className="m-0 font-semibold text-ink flex flex-wrap items-center gap-1">
                        Faz 14 düzeltmesi
                        {(p14.changes || []).map((c: string) => <span key={c} className="ms-tag is-ai">{c}</span>)}
                      </p>
                      {p14.summary &&
                        (typeof p14.summary === 'string' ? (
                          <p className="m-0">{p14.summary}</p>
                        ) : (
                          Object.entries(p14.summary as Record<string, any>).map(([k, v]) => (
                            <p key={k} className="m-0">
                              <span className="text-ink-3">{({ soru_koku_duzeltmesi: 'Kök', aciklama_duzeltmesi: 'Açıklama', mufredat_atamasi: 'Müfredat', siklar: 'Şıklar' } as Record<string, string>)[k] || k}:</span> {String(v)}
                            </p>
                          ))
                        ))}
                      {(o.committeeId || o.discipline || o.topic) && (
                        <p className="m-0 text-[12.5px]"><span className="text-ink-3">Önceki kurul/ders/konu:</span> {[o.committeeId ? committeeShort(String(o.committeeId).replace(/^TIP\s*3(\d)0$/i, 'donem3-kurul$1')) : null, o.discipline, o.topic].filter(Boolean).join(' · ')}</p>
                      )}
                      {o.stem && <p className="m-0"><span className="text-ink-3">Önceki kök:</span> {o.stem}</p>}
                      {Array.isArray(o.options) && o.options.length > 0 && (
                        <ul className="m-0 pl-4 text-[12.5px]">
                          {o.options.map((op: any) => <li key={op.key}>{op.key}) {op.text}</li>)}
                        </ul>
                      )}
                      {o.explanation && (
                        <details className="text-[12.5px]"><summary className="cursor-pointer text-ink-3">Önceki açıklama</summary><p className="m-0 mt-1 whitespace-pre-wrap">{o.explanation}</p></details>
                      )}
                    </div>
                  );
                })()}

                {isCompareView ? (
                  <DiffSheet
                    oldLabel="Eski"
                    newLabel="Denetleyici"
                    oldStem={String(eskiData.stem || stem)}
                    newStem={String(denetleyiciData.stem || stem)}
                    oldOpts={eskiData.options || []}
                    newOpts={denetleyiciData.options || options}
                    answer={correctAnswer ? String(correctAnswer) : undefined}
                    oldAnswer={eskiData.correctAnswer ? String(eskiData.correctAnswer) : undefined}
                    hideAnswer={hideAnswer}
                  >
                    {(explanation || String(eskiData.explanation || '').trim() || saEntries.length > 0) && (
                      <div className="cx-diff-foot">
                        {explanation && (
                          <details className="cx-diff-expl">
                            <summary>Açıklama</summary>
                            <SourceText text={String(explanation)} size="sm" />
                          </details>
                        )}
                        {String(eskiData.explanation || '').trim() && (
                          <details className="cx-diff-expl">
                            <summary>Eski açıklama</summary>
                            <p className="m-0 whitespace-pre-wrap">{eskiData.explanation}</p>
                          </details>
                        )}
                        {saEntries.length > 0 && (
                          <button type="button" className="cx-act is-text" onClick={() => setAboutQuestion(q)}>
                            <ShieldCheck aria-hidden /> <span>Şık analizi</span>
                          </button>
                        )}
                      </div>
                    )}
                  </DiffSheet>
                ) : effectiveMode === 'split' ? (
                  <DiffSheet
                    oldLabel="Ham"
                    newLabel="Düzenlenmiş"
                    oldStem={String((q as any).rawQuestion?.stem || q.fragments?.[0]?.text || q.rawStem || stem)}
                    newStem={stem}
                    oldOpts={(q as any).rawQuestion?.options || q.options || []}
                    newOpts={options}
                    answer={!pollMode && correctAnswer ? String(correctAnswer) : undefined}
                    hideAnswer={hideAnswer}
                  />
                ) : effectiveMode === 'raw' ? (
                  <div className="bg-canvas rounded-xl p-3 flex flex-col gap-2">
                    <span className="text-[12px] font-semibold text-ink-3 truncate">Ham metin · {q.sourceFile || 'PDF kaynağı'}</span>
                    <p className="m-0 text-[14.5px] text-ink leading-relaxed whitespace-pre-wrap">{(q as any).rawQuestion?.stem || q.fragments?.[0]?.text || q.rawStem || q.topic}</p>
                    {(((q as any).rawQuestion?.options && (q as any).rawQuestion.options.length > 0) || (q.options && q.options.length > 0)) && (
                      <ol className="ms-opts">
                        {((q as any).rawQuestion?.options || q.options).map((opt: any) => {
                          const isClaimed = !hideAnswer && opt.key === (q.claimedAnswer || (q as any).rawQuestion?.claimedAnswer);
                          return (
                            <li key={opt.key} className={`ms-opt ${isClaimed ? 'is-claimed' : ''}`}>
                              <span className="ms-opt-key">{opt.key}</span>
                              <span>{opt.text}</span>
                              <span className="ms-opt-side">{isClaimed && <span className="text-[12px] font-semibold text-warn">İşaretlenen</span>}</span>
                            </li>
                          );
                        })}
                      </ol>
                    )}
                  </div>
                ) : (
                  <>
                    <div className="flex items-start gap-1.5">
                      <StemText text={stem} terms={terms} className="flex-1 min-w-0" />
                      {p14Fixed &&
                        (norm(p14o?.stem) && norm(p14o.stem) !== norm(stem) ? (
                          <ChangeInfo title="Soru kökü düzeltildi (Faz 14)" before={p14o.stem} after={stem} note={p14Note('soru_koku_duzeltmesi')} />
                        ) : (
                          <ChangeInfo title="Soru kökü (Faz 14)" note={p14Note('soru_koku_duzeltmesi') || 'Kök değiştirilmedi; soru Faz 14 incelemesinden geçti.'} />
                        ))}
                    </div>

                    {pollMode ? (
                      <AnswerPoll
                        questionId={String(q.id)}
                        options={((doubtful || acceptedPoll) && doubtInfo?.options[String(q.id)]) || options}
                        voterUid={currentUser?.uid || null}
                        terms={terms}
                        acceptedAnswer={acceptedPoll}
                        hint={
                          acceptedPoll
                            ? `Cevap ${acceptedPoll} olarak kabul edildi. Anket açık: kendi cevabını ver, topluluğun cevabı kabul edilen cevapla karşılaştırılır.`
                            : doubtful
                            ? 'Cevap anahtarı tartışmalı: bağımsız çözücüler aynı şıkta uzlaşamadı. Doğru bildiğin şıkkı seç.'
                            : 'Bu sorunun cevap anahtarı yok. Doğru bildiğin şıkkı seç; çoğunluğun cevabı öne çıkar.'
                        }
                      />
                    ) : (
                      options.length > 0 && (
                        <ol className={`cx-opts ${options.every((o: any) => String(o.text ?? '').length <= 42) ? 'is-short' : ''}`}>
                          {options.map((opt: any) => {
                            const key = String(opt.key);
                            const isCorrect = key === correctAnswer;
                            const showCorrect = isCorrect && !hideAnswer;
                            const wrongPick = quizMode && picked === key && !isCorrect;
                            const before = p14Fixed ? oldOpt(key) : '';
                            const optChanged = p14Fixed && (opt.isAiGenerated || (before && norm(before) !== norm(opt.text)));
                            const cls = `cx-opt ${showCorrect ? 'is-correct' : ''} ${wrongPick ? 'is-wrong' : ''} ${picked && (showCorrect || wrongPick) ? 'is-reveal' : ''}`;
                            const body = (
                              <>
                                <span className="cx-bubble" aria-hidden>{showCorrect ? <Check strokeWidth={3} /> : wrongPick ? <X strokeWidth={3} /> : key}</span>
                                <span className="cx-opt-t">
                                  <Highlight text={String(opt.text ?? '')} terms={terms} />
                                  {showCorrect && <span className="sr-only"> (doğru cevap)</span>}
                                </span>
                              </>
                            );
                            return (
                              <li key={key} className="cx-opt-li">
                                {quizMode && !picked ? (
                                  <button type="button" className={cls} onClick={() => setPicks((p) => ({ ...p, [q.id]: key }))} aria-label={`${key} şıkkını işaretle`}>
                                    {body}
                                  </button>
                                ) : (
                                  <div className={cls}>{body}</div>
                                )}
                                {optChanged && (
                                  <span className="cx-opt-info">
                                    <ChangeInfo
                                      title={`${key} şıkkı ${before ? 'düzeltildi' : 'eklendi'} (Faz 14)`}
                                      before={before}
                                      after={String(opt.text)}
                                      note={opt.isAiGenerated ? 'Kaynakta bu şık eksikti; yapay zekâ tamamladı (doğrulanmadı).' : undefined}
                                    />
                                  </span>
                                )}
                                {!hideAnswer && (
                                  <button
                                    type="button"
                                    className="cx-objection"
                                    onClick={() => setObjection({ question: q, option: { key, text: String(opt.text ?? '') } })}
                                    aria-label={`${key} şıkkına itiraz et`}
                                    title={`${key} şıkkına itiraz et`}
                                  >
                                    <ShieldAlert aria-hidden />
                                  </button>
                                )}
                              </li>
                            );
                          })}
                        </ol>
                      )
                    )}
                    {quizMode && picked && !pollMode && (
                      <p className={`cx-verdict ${picked === correctAnswer ? 'is-ok' : 'is-bad'}`} role="status">
                        <b>{picked === correctAnswer ? 'Doğru' : `Yanlış · cevap ${correctAnswer}`}</b>
                        <button type="button" onClick={() => setPicks((p) => { const x = { ...p }; delete x[q.id]; return x; })}>Yeniden dene</button>
                        {explanation && <button type="button" onClick={() => setAboutQuestion(q)}>Açıklama</button>}
                      </p>
                    )}

                    {!hideAnswer && !pollMode && (q as any).answerStatus === 'dogrulanmadi' && (
                      <p className="cx-note is-warn">Cevap doğrulanmadı: kaynaktaki işaret bir öğrencinin cevabıydı.</p>
                    )}
                    {!hideAnswer && (q as any).answerStatus === 'dogrulandi' && <p className="cx-note is-ok">Cevap ders slaytı kanıtıyla doğrulandı.</p>}

                    {/* Çoklu referans / alternatif sınav yılları bandı */}
                    {q.similarPastQuestions && q.similarPastQuestions.length > 0 && (
                      <div className="mt-2.5 pt-2 border-t border-line/60 flex flex-wrap items-center gap-1.5 text-[12px] text-ink-3">
                        <span className="font-semibold text-ink-2 flex items-center gap-1">
                          <Layers className="w-3.5 h-3.5 text-accent" />
                          Diğer yıllardaki çıkmış örnekleri:
                        </span>
                        {q.similarPastQuestions.map((alt) => (
                          <span
                            key={alt.id}
                            className="inline-flex items-center px-2 py-0.5 rounded-md bg-field border border-line text-[11.5px] font-medium text-ink"
                            title={`Soru ID: ${alt.id}`}
                          >
                            {alt.label || `${alt.examYear} - Soru ${alt.questionNumber}`}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Açıklama, ilgili slayt ve terimler kartta yer kaplamaz: üç nokta → Hakkında */}
                  </>
                )}

                <footer className="cx-q-foot">
                  <button type="button" onClick={() => handleToggleLike(q)} aria-pressed={isLiked} title={isLiked ? 'Beğeniyi geri al' : 'Soruyu beğen'} className={`cx-act ${isLiked ? 'is-on' : ''}`}>
                    <ThumbsUp className={isLiked ? 'fill-current' : ''} aria-hidden /> <span>{q.upvotes || 0}</span><span className="sr-only"> beğeni</span>
                  </button>
                  <button type="button" onClick={() => handleToggleDislike(q)} aria-pressed={isDisliked} title={isDisliked ? 'Beğenmemeyi geri al' : 'Eksik ya da hatalı'} className={`cx-act ${isDisliked ? 'is-bad' : ''}`}>
                    <ThumbsDown className={isDisliked ? 'fill-current' : ''} aria-hidden /> <span>{q.downvotes || 0}</span><span className="sr-only"> beğenmeme</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setExpandedCommentsQuestionId(expandedCommentsQuestionId === q.id ? null : q.id)}
                    aria-expanded={expandedCommentsQuestionId === q.id}
                    className={`cx-act ${expandedCommentsQuestionId === q.id ? 'is-on' : ''}`}
                    title="Yorumlar"
                  >
                    <MessageSquare aria-hidden /> <span>{commentsCount}</span><span className="sr-only"> yorum</span>
                  </button>
                  <span className="cx-bar-sp" />
                  <button type="button" onClick={() => setAboutQuestion(q)} className="cx-act is-text" title="Açıklama, ilgili slayt, kanıt ve terimler">
                    <BookOpen aria-hidden /> <span>{explanation ? 'Açıklama' : 'Hakkında'}</span>
                  </button>
                  <button type="button" onClick={() => handleShareQuestion(q)} className="cx-act" aria-label="Soruyu paylaş" title="Soru bağlantısını paylaş">
                    <Share2 aria-hidden />
                  </button>
                </footer>

                {expandedCommentsQuestionId === q.id && (
                  <div className="ms-pop-in bg-field rounded-xl p-2.5 flex flex-col gap-2">
                    <div className="flex flex-col gap-1.5 max-h-56 overflow-y-auto">
                      {commentsCount > 0 ? (
                        (q as any).comments.map((c: any) => (
                          <div key={c.id} className="bg-white rounded-[10px] px-3 py-2 flex flex-col gap-0.5">
                            <div className="flex items-center justify-between gap-2 text-[12px] text-ink-3">
                              <span className="font-semibold text-ink">{c.author || 'Tıp öğrencisi'}</span>
                              <span>{new Date(c.timestamp).toLocaleDateString('tr-TR')}</span>
                            </div>
                            <p className="m-0 text-[14px] text-ink-2 leading-relaxed">{c.text}</p>
                          </div>
                        ))
                      ) : (
                        <p className="m-0 px-1 text-[13.5px] text-ink-3">Henüz yorum yok. Bir ipucu ya da alternatif çözüm ekleyen ilk kişi ol.</p>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <input
                        type="text"
                        value={newCommentText}
                        onChange={(e) => setNewCommentText(e.target.value)}
                        onKeyDown={(e) => { if (e.key === 'Enter') handleCommentSubmit(q.id); }}
                        placeholder="Yorum ya da ipucu yaz…"
                        aria-label="Yorum"
                        className="flex-1 min-w-0 h-10 bg-white border border-line rounded-full px-4 text-[15px] outline-0 focus:border-accent"
                      />
                      <button type="button" onClick={() => handleCommentSubmit(q.id)} disabled={isSubmittingComment || !newCommentText.trim()} aria-label="Gönder" className="ms-btn is-primary is-icon">
                        <Send />
                      </button>
                    </div>
                  </div>
                )}
              </article>
            );
          })}

          {totalPages > 1 && !sharedId && (
            <nav aria-label="Sayfalar" className="cx-pager">
              <button type="button" onClick={() => { setCurrentPage((prev) => Math.max(1, prev - 1)); window.scrollTo({ top: 0, behavior: 'smooth' }); }} disabled={currentPage === 1} className="ms-btn is-outline">
                <ChevronLeft /> <span className="hidden sm:inline">Önceki</span>
              </button>
              <span className="text-ink-3">
                <span className="font-semibold text-ink">{currentPage}</span> / {totalPages}
              </span>
              <button type="button" onClick={() => { setCurrentPage((prev) => Math.min(totalPages, prev + 1)); window.scrollTo({ top: 0, behavior: 'smooth' }); }} disabled={currentPage === totalPages} className="ms-btn is-outline">
                <span className="hidden sm:inline">Sonraki</span> <ChevronRight />
              </button>
            </nav>
          )}
        </div>
      )}

      {/* Öğren eşleşmesi: soru hangi slayta bağlı */}
      {selectedLearnMatch && (
        <Dialog
          width="max-w-2xl"
          onClose={() => setSelectedLearnMatch(null)}
          title={selectedLearnMatch.match.deckTitle}
          subtitle={[`Slayt ${selectedLearnMatch.match.slideNumber}`, selectedLearnMatch.match.discipline, selectedLearnMatch.match.committee].filter(Boolean).join(' · ')}
          footer={
            <>
              <button type="button" onClick={() => setSelectedLearnMatch(null)} className="ms-btn is-ghost">Kapat</button>
              {onNavigateToLearn && (
                <button
                  type="button"
                  onClick={() => {
                    const dId = selectedLearnMatch.match.deckId;
                    const sNum = selectedLearnMatch.match.slideNumber;
                    const focus = focusFor(selectedLearnMatch.question, selectedLearnMatch.match);
                    setSelectedLearnMatch(null);
                    onNavigateToLearn(dId, sNum, focus);
                  }}
                  className="ms-btn is-primary"
                >
                  <GraduationCap /> Öğren'de aç
                </button>
              )}
            </>
          }
        >
          <p className="m-0 text-[13px] text-ink-2 leading-relaxed">
            <b className="text-ink">Soru #{selectedLearnMatch.question.questionNumber}</b> bu slayta bağlı
            <span className="ms-tag is-accent ml-1.5 align-middle">{selectedLearnMatch.match.matchType === 'direct' ? 'Müfredat eşleşmesi' : 'Konu eşleşmesi'}</span>
          </p>
          <div className="flex flex-col gap-1">
            {selectedLearnMatch.match.badge && <span className="ms-tag self-start">{selectedLearnMatch.match.badge}</span>}
            <h3 className="m-0 text-[15.5px] font-semibold text-ink">{selectedLearnMatch.match.slideTitle}</h3>
          </div>
          {(() => {
            const f = focusFor(selectedLearnMatch.question, selectedLearnMatch.match);
            return (
              <>
                <div className="ms-focus-legend">
                  <span><mark className="ms-hl">soru ifadesi</mark></span>
                  {f.answerKey && <span><mark className="ms-hl is-answer">doğru şık {f.answerKey}</mark>{f.answerText ? ` — ${f.answerText}` : ''}</span>}
                </div>
                {selectedLearnMatch.match.synthesisNarrative && (
                  <Collapsible className="ms-disc" title="Amfi ve ders notu sentezi" defaultOpen>
                    <div className="max-h-72 overflow-y-auto pr-1">
                      <SourceText text={selectedLearnMatch.match.synthesisNarrative} terms={f.terms} answerTerms={f.answerTerms} size="sm" />
                    </div>
                  </Collapsible>
                )}
              </>
            );
          })()}
          {selectedLearnMatch.match.spotPearls && selectedLearnMatch.match.spotPearls.length > 0 && (
            <section className="flex flex-col gap-1.5">
              <h4 className="m-0 text-[12.5px] font-semibold text-ink-3">Sınav için önemli noktalar</h4>
              <ul className="ms-stem-list">
                {selectedLearnMatch.match.spotPearls.map((pearl: any, i: number) => {
                  const isObj = pearl && typeof pearl === 'object';
                  return (
                    <li key={i} className="text-[13.5px] text-ink-2 leading-relaxed">
                      <span className="ms-stem-mark is-dot" aria-hidden />
                      <span className="min-w-0">
                        {isObj && pearl.badge && <b className="text-ink mr-1">{pearl.badge}</b>}
                        <Marked
                          text={isObj ? String(pearl.text || '') : String(pearl || '')}
                          terms={focusFor(selectedLearnMatch.question).terms}
                          answerTerms={focusFor(selectedLearnMatch.question).answerTerms}
                        />
                      </span>
                    </li>
                  );
                })}
              </ul>
            </section>
          )}
          {selectedLearnMatch.match.flashcards && selectedLearnMatch.match.flashcards.length > 0 && (
            <section className="flex flex-col gap-1.5">
              <h4 className="m-0 text-[12.5px] font-semibold text-ink-3">İlgili kartlar · {selectedLearnMatch.match.flashcards.length}</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {selectedLearnMatch.match.flashcards.map((card) => (
                  <FlashcardComponent key={card.id} card={card} />
                ))}
              </div>
            </section>
          )}
        </Dialog>
      )}

      {/* Ham sorunun arşivdeki yeri */}
      {selectedRawSourceQuestion && (() => {
        const rq: any = selectedRawSourceQuestion;
        const answerKey = rq.correctAnswer || rq.claimedAnswer;
        return (
          <Dialog
            width="max-w-2xl"
            onClose={() => setSelectedRawSourceQuestion(null)}
            title="Kaynak belge"
            subtitle={[rq.discipline || 'Tıp', committeeShort(rq.committeeId)].filter(Boolean).join(' · ')}
            footer={<button type="button" onClick={() => setSelectedRawSourceQuestion(null)} className="ms-btn is-ghost">Kapat</button>}
          >
            <dl className="m-0 grid grid-cols-2 sm:grid-cols-4 gap-x-4 gap-y-2 text-[13px]">
              <div className="col-span-2 min-w-0">
                <dt className="text-[12px] text-ink-3">Dosya</dt>
                <dd className="m-0 font-medium text-ink truncate" title={rq.sourceFile || rq.sourceNote}>{rq.sourceFile || rq.sourceNote || 'Geçmiş kurul arşivi'}</dd>
              </div>
              <div>
                <dt className="text-[12px] text-ink-3">Yıl</dt>
                <dd className="m-0 font-medium text-ink">{rq.examYear || 'Arşiv'}</dd>
              </div>
              <div>
                <dt className="text-[12px] text-ink-3">Soru · sayfa</dt>
                <dd className="m-0 font-medium text-ink">#{rq.questionNumber}{rq.matchedSlidePage ? ` · s. ${rq.matchedSlidePage}` : ''}</dd>
              </div>
            </dl>
            <section className="flex flex-col gap-1.5">
              <h4 className="m-0 text-[12.5px] font-semibold text-ink-3">Ham soru metni</h4>
              <div className="rounded-xl bg-canvas p-3">
                <StemText text={String(rq.rawStem || rq.rawQuestion?.stem || rq.fragments?.[0]?.text || rq.stem || rq.topic || '')} size="sm" />
              </div>
            </section>
            <ol className="ms-opts">
              {(rq.rawQuestion?.options || rq.options || []).map((opt: any, i: number) => {
                const key = typeof opt === 'string' ? String.fromCharCode(65 + i) : opt.key;
                const text = typeof opt === 'string' ? opt : opt.text;
                const isCorrect = key === answerKey;
                return (
                  <li key={key} className={`ms-opt ${isCorrect ? 'is-correct' : ''}`}>
                    <span className="ms-opt-key">{isCorrect ? <Check className="w-4 h-4" strokeWidth={3} /> : key}</span>
                    <span>{text}</span>
                    <span className="ms-opt-side">{isCorrect && <span className="ms-opt-correct">Cevap</span>}</span>
                  </li>
                );
              })}
            </ol>
          </Dialog>
        );
      })()}

      {/* Soru hakkında: künye, ilgili slayt, açıklama, kanıt, terimler */}
      {aboutQuestion && (() => {
        const q: any = aboutQuestion;
        const lm = learnMatcher.getMatch(aboutQuestion);
        const f = focusFor(aboutQuestion, lm);
        const ans = q.reconstruction?.correctAnswer || q.correctAnswer || q.claimedAnswer;
        const expl = q.reconstruction?.explanation || q.explanation;
        const p14 = isPhase14Fixed(q) && String(q.phase14Original?.explanation || '').trim() !== String(expl || '').trim();
        const hidden = quizMode && !picks[q.id];
        const isLegacyView = (versionViewOverrides[q.id] || (isDenetleyiciQuestion(q) ? 'denetleyici' : 'eski')) === 'eski';
        const p14Note = isPhase14Pending(q)
          ? 'Faz 14 yapay zekâ incelemesinden geçti; düzeltme yönetici onayı bekliyor (doğrulanmadı).'
          : isPhase14Fixed(q)
            ? 'Cevap, kurul ve açıklama Faz 14 incelemesinde onaylandı.'
            : undefined;

        return (
          <QuestionAboutDialog
            questionId={String(q.id)}
            title={`Soru #${q.questionNumber || '–'} hakkında`}
            subtitle={[q.discipline, q.examYear].filter(Boolean).join(' · ')}
            facts={[
              { label: 'Kurul', value: formatCommitteeName(q.contentCommitteeId || q.committeeId) },
              { label: 'Ders', value: q.discipline },
              { label: 'Konu', value: q.topic && !/^Soru #/.test(q.topic) ? q.topic : undefined },
              { label: 'Sınav', value: q.examYear },
              { label: 'Soru no', value: q.questionNumber ? `#${q.questionNumber}` : undefined, mono: true },
              { label: 'Cevap', value: hidden ? 'gizli' : ans || doubtInfo?.resolved?.[String(q.id)]?.answer, mono: !hidden },
              { label: 'Kaynak dosya', value: q.sourceFile || q.sourceNote, wide: true },
              {
                label: 'Veri tabanına eklenme',
                value: q.createdAt
                  ? new Date(q.createdAt).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })
                  : undefined,
              },
              {
                label: 'Son düzenlenme',
                value: (q.updatedAt || q.reconstruction?.lastUpdated || q.denetleyiciSurumu?.onayTarihi)
                  ? new Date(q.updatedAt || q.reconstruction?.lastUpdated || q.denetleyiciSurumu?.onayTarihi).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })
                  : undefined,
              },
            ]}
            question={q}
            explanation={expl ? String(expl) : undefined}
            explanationNote={p14 ? <span className="ms-tag is-ai normal-case tracking-normal">Faz 14'te yenilendi</span> : undefined}
            evidence={q.evidenceText || q.reconstruction?.evidenceText}
            evidenceTitle={isDeepSeekQuestion(q) ? 'Ders notu ve slayt kanıtı' : 'Ders notu ve amfi kanıtı'}
            answerHidden={hidden}
            answerTerms={f.answerTerms}
            sikAnalizi={q.sik_analizi || (q as any).denetleyiciSurumu?.sik_analizi}
            referanslar={q.referans_kaynaklar || (q as any).denetleyiciSurumu?.referans_kaynaklar}
            denetleyiciOnayi={isDenetleyiciQuestion(q)}
            learnMatch={lm}
            p14StatusNote={p14Note}
            isEskiView={isLegacyView}
            answerKey={ans ? String(ans) : undefined}
            options={(q.reconstruction?.options || q.options || []) as { key: string; text: string }[]}
            answerChange={isDenetleyiciQuestion(q) && !hidden && (q.eskiSurum || q.phase14Original)?.correctAnswer && (q.eskiSurum || q.phase14Original).correctAnswer !== ans ? { from: String((q.eskiSurum || q.phase14Original).correctAnswer), to: String(ans) } : undefined}
            onOpenSlide={(kaynak, sayfa) => {
              setAboutQuestion(null);
              if (onNavigateToLearn) {
                if (lm) {
                  onNavigateToLearn(lm.deckId, sayfa || lm.slideNumber, f);
                } else {
                  onNavigateToLearn(undefined, sayfa, f);
                }
              }
            }}
            onPreviewSlide={lm ? () => { setAboutQuestion(null); setSelectedLearnMatch({ question: aboutQuestion, match: lm }); } : undefined}
            onOpenInLearn={lm && onNavigateToLearn ? () => { setAboutQuestion(null); onNavigateToLearn(lm.deckId, lm.slideNumber, f); } : undefined}
            onShowSource={() => { setAboutQuestion(null); setSelectedRawSourceQuestion(aboutQuestion); }}
            onClose={() => setAboutQuestion(null)}
          />
        );
      })()}

      {/* Şıkka itiraz */}
      {objection && (
        <ReportQuestionModal
          question={objection.question}
          notifyEmail={isAdminUser ? null : currentUser?.email || null}
          objectOption={objection.option}
          onClose={() => setObjection(null)}
          onSubmit={async (reason, details) => {
            const res = await ApiService.reportPastQuestion(objection.question.id, reason, details, currentUser?.displayName || 'Tıp Öğrencisi', { email: currentUser?.email, uid: currentUser?.uid });
            loadAiQueue();
            if (res?.report) {
              setQuestions((prev) =>
                prev.map((q) => (q.id === objection.question.id && !(q.reports || []).some((r: any) => r.id === res.report.id) ? { ...q, reports: [...(q.reports || []), res.report] } : q)),
              );
            }
          }}
        />
      )}

      {/* Yapay zekâ incelemesine gönder (Faz 14 · ücretsiz kuyruk) */}
      {aiReviewQ && (
        <Dialog
          width="max-w-md"
          onClose={() => !aiReviewBusy && setAiReviewQ(null)}
          title="Yapay zekâ incelemesine gönder"
          subtitle={`Soru #${aiReviewQ.questionNumber}${aiQueue[String(aiReviewQ.id)]?.position ? ` · şu an sırada ${aiQueue[String(aiReviewQ.id)].position}.` : ''}`}
          footer={
            <>
              <button type="button" className="ms-btn is-ghost mr-auto" onClick={() => setAiReviewQ(null)} disabled={aiReviewBusy}>Vazgeç</button>
              <button type="button" className="ms-btn is-primary" onClick={sendAiReview} disabled={aiReviewBusy}>
                <Sparkles /> {aiReviewBusy ? 'Gönderiliyor…' : aiQueue[String(aiReviewQ.id)] ? 'Notu ekle' : 'Gönder'}
              </button>
            </>
          }
        >
          <div className="cx-air">
            <ol className="cx-air-steps">
              <li><b>Sıraya girer.</b> Ücretsiz yapay zekâ kotasıyla sırayla incelenir; yoğunlukta birkaç saat sürebilir.</li>
              <li><b>Kaynakla denetlenir.</b> Kök, şıklar ve cevap ders notlarına göre yeniden kontrol edilir.</li>
              <li><b>Otomatik yayımlanır.</b> Düzeltme gerekirse soru güncellenir. Cevap belirsiz kalırsa yönetici karar verir.</li>
            </ol>
            <label htmlFor="cx-air-msg" className="cx-air-l">Neyi kontrol edelim? <span>isteğe bağlı</span></label>
            <textarea
              id="cx-air-msg"
              rows={3}
              maxLength={1500}
              value={aiReviewMsg}
              onChange={(e) => setAiReviewMsg(e.target.value)}
              placeholder="Ör. Kök eksik görünüyor; C şıkkı da doğru olabilir."
              className="cx-air-t"
              autoFocus
            />
          </div>
        </Dialog>
      )}

      {/* Hata bildir */}
      {reportingQuestion && (
        <ReportQuestionModal
          question={reportingQuestion}
          notifyEmail={isAdminUser ? null : currentUser?.email || null}
          onClose={() => setReportingQuestion(null)}
          onSubmit={async (reason, details) => {
            const res = await ApiService.reportPastQuestion(
              reportingQuestion.id,
              reason,
              details,
              currentUser?.displayName || 'Tıp Öğrencisi',
              { email: currentUser?.email, uid: currentUser?.uid }
            );
            loadAiQueue();
            if (res && res.report) {
              setQuestions((prev) =>
                prev.map((q) => {
                  if (q.id === reportingQuestion.id) {
                    const curReports = q.reports || [];
                    const updatedReports = curReports.some((r: any) => r.id === res.report.id)
                      ? curReports
                      : [...curReports, res.report];
                    return { ...q, reports: updatedReports };
                  }
                  return q;
                })
              );
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
          matchedSlideNote={customRedactQuestion.match?.note && customRedactQuestion.match?.page ? {
            noteTitle: customRedactQuestion.match.note.title || '',
            pageNumber: customRedactQuestion.match.page.pageNumber,
            snippet: String(customRedactQuestion.match.page.content || '').substring(0, 300)
          } : null}
        />
      )}
    </div>
  );
};
