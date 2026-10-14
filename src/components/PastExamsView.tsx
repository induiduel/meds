import React, { useCallback, useState, useMemo, useEffect, useDeferredValue, useRef } from 'react';
import { useAnswerDoubtfulQuery, useAiReviewQueueQuery } from '../hooks/useMedicalQueries';
import { CikmisCard } from '../screens/cikmis/CikmisCard';
import { PastQuestionRichCard, PastQuestionRichCardProps, RichCardSkeleton, LoadMoreSentinel } from './cikmis/PastQuestionRichCard';
import { CikmisViewSwitch, useCikmisGorunum } from './cikmis/CikmisViewSwitch';
import { PageToolbar, QuickOptions, type ToolbarChip, type ToolbarQuick } from './ui/PageToolbar';
import { useAppearance } from '../utils/appearance';
import { CikmisV12, type C12Facet } from './v12/CikmisV12';
import { getProgress, recordAttempt, getFavorites, setFavorite, OptionKey, AttemptRecord } from '../services/studyStore';
import { logActivity } from '../services/activityLog';
import { FilterGroup } from './ui/FilterGroup';
import { copyQuestion } from '../utils/copyQuestion';
import { getVoterId, toggledVote } from '../utils/voterId';
import { AnswerPoll } from './AnswerPoll';
import { StemText } from './ui/StemText';
import { Collapsible } from './ui/Collapsible';
import { Dialog } from './ui/Dialog';
import { Sheet } from './ui/Sheet';
import { confirmDialog } from './ui/ConfirmDialog';
import { foldText, parseQuery, scoreFields, SearchField } from '../services/searchText';
import { QuestionAboutDialog, normalizeRefList } from './QuestionAboutDialog';
import { SourceText, Marked } from './ui/SourceText';
import { buildQuestionFocus, QuestionFocus } from '../services/questionFocus';
import { toast } from './ui/Toast';
import { ErrorReportHistoryModal } from './ErrorReportHistoryModal';
import { triggerDomHighlightAndScroll, shareDeepLink } from '../services/universalRedirectService';
import {
  Sparkles,
  Info,
  BookOpen,
  Search,
  Layers,
  ChevronLeft,
  ChevronRight,
  X,
  FileText,
  HelpCircle,
  Copy,
  Check,
  GraduationCap,
  ArrowUpDown,
  RefreshCw,
  Tag,
  Flag,
  Send,
  SlidersHorizontal,
  ChevronDown,
  Wand2,
  BarChart3,
  Share2,
  ShieldAlert,
  ShieldCheck,
  History,
  Trash2,
} from 'lucide-react';
import { ActionItem } from './ui/ActionMenu';
import { ReportQuestionModal } from './ReportQuestionModal';
import { EmptySearch, SectionLoader } from './ui/Animations';
import { disciplineClass, disciplineLabel, groupDisciplines } from '../utils/discipline';
import { QuestionItem, LectureNote, LectureNotePage, QuestionLectureMatch } from '../types';
import { AppUser, ADMIN_EMAIL } from '../services/auth';
import { ApiService } from '../services/api';
import { pastQuestionsCache, CacheSyncStatus } from '../services/pastQuestionsCache';
import { AdminCustomRedactModal } from './AdminCustomRedactModal';
import { learnMatcher, QuestionLearnMatch, isReliableLearnMatch } from '../services/learnMatcher';
const LazyFlashcardComponent = React.lazy(() =>
  import('./learn/InteractiveDeckView').then((m) => ({ default: m.FlashcardComponent })),
);
import { pathFor, parseLocation, writeLocation } from '../router';
import { censorProfanity } from '../utils/profanityFilter';
import {
  OFFICIAL_CURRICULUM_COMMITTEES,
  DONEM3_CURRICULUM_DISCIPLINES,
  normalizeDonem3Discipline,
  normalizeCommitteeId,
  isDonem3Question,
} from '../data/curriculumData';

/** Denetleyici Onayı almış (altın standart, doğrulanmış) soru */
// Check-solve sırasında özgün sınavda olmayıp sonradan yazılan şıklar (checkSolve.eklenenSiklar) Hakkında'da açıkça belirtilir
const provenanceNoteFor = (q: any): string | undefined => {
  const added: string[] = Array.isArray(q?.checkSolve?.eklenenSiklar) ? q.checkSolve.eklenenSiklar : [];
  if (!added.length) return undefined;
  if (added.length >= 3) {
    return 'Bu sorunun şıkları özgün sınavdan alınmamıştır. Kayıtta sınavın şıkları eksik ya da okunamaz olduğu için soru, özgün sınavdaki bilgi korunarak şıkları sonradan yazılıp yeniden kurulmuştur.';
  }
  return `${added.join(', ')} ${added.length > 1 ? 'şıkları' : 'şıkkı'} özgün sınavda yoktu (eksik ya da okunamazdı); soru tamamlansın diye sonradan eklenmiştir. Diğer şıklar özgün sınavdandır.`;
};

export const editedTags = (q: any, ts: number): string[] => {
  const age = Date.now() - ts;
  const out: string[] = [];
  if (ts && age <= 864e5) out.push('son24');
  if (ts && age <= 7 * 864e5) out.push('son7');
  if (q?.checkSolve?.cevapDegisti) out.push('cevap');
  if ((q?.checkSolve?.eklenenSiklar?.length || 0) >= 3) out.push('kurulan');
  return out;
};

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

/** Çözülmemiş hata bildirimi var mı (çözülen/geçersiz sayılan bildirim "Hata bildirilen" süzgecinde tutulmaz). */
const hasOpenReport = (q: QuestionItem): boolean =>
  (q.reports || []).some((r: any) => !['resolved', 'verified_correct', 'rejected', 'dismissed'].includes(r?.status));

const isNewQ = (q: QuestionItem): boolean =>
  Boolean(
    q.isNewQuestion ||
      (q.examYear ? q.examYear.includes('2026') || q.examYear.includes('2027') : false) ||
      (q.createdAt ? new Date(q.createdAt).getTime() > Date.now() - 30 * 86400000 : false),
  );

type FacetKey = 'pool' | 'committee' | 'year' | 'discipline' | 'topic' | 'answer' | 'explanation' | 'source' | 'p14' | 'denetleyici' | 'newness' | 'manual' | 'repeated' | 'quarantine' | 'edited';
interface Prep {
  q: QuestionItem;
  disc: string;
  topic: string;
  year: string;
  yearNum: number;
  qualityScore: number;
  popularityScore: number;
  updatedTimestamp: number;
  comms: string[];
  isNew: boolean;
  isManual: boolean;
  isRepeated: boolean;
  hasAnswer: boolean;
  doubtful: boolean;
  hasExpl: boolean;
  isQuarantined: boolean;
  isInaccessible: boolean;
  isDonem3: boolean;
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

/** v12'de kart listesini CikmisV12 çerçevesine (araç çubuğu + süzgeç sütunu) yerleştirir; v10/v11'de liste olduğu gibi çizilir. */
const V12Frame: React.FC<{ on: boolean; props?: () => Omit<React.ComponentProps<typeof CikmisV12>, 'children'>; children: React.ReactNode }> = ({ on, props, children }) =>
  on && props ? <CikmisV12 {...props()}>{children}</CikmisV12> : <>{children}</>;

export const PastExamsView: React.FC<PastExamsViewProps> = ({
  currentUser,
  lectureNotes = [],
  initialSearchQuery = '',
  onOpenNote,
  onUpdateQuestionReference,
  onNavigateToLearn,
}) => {
  // v12 "Net": araç çubuğu + gelişmiş süzgeç sütunu components/v12/CikmisV12'de; kart listesi ortak
  const v12 = useAppearance().design === 'v12';
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [internalNotes, setInternalNotes] = useState<LectureNote[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(initialSearchQuery);
  
  // Filter States
  const [selectedCommittee, setSelectedCommittee] = useState<string>('all');
  const [selectedYear, setSelectedYear] = useState<string>('all');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('all');
  const browseRef = useRef<HTMLUListElement>(null);
  const [deepseekFilter, setDeepseekFilter] = useState<'all' | 'deepseek_only' | 'standard_only'>('all');
  const [sourceFilter, setSourceFilter] = useState<'all' | 'gemini_v3' | 'existing'>('all');
  const [phase14Filter, setPhase14Filter] = useState<'all' | 'faz14' | 'faz14_onayli' | 'faz14_bekleyen'>('all');
  // Yönetim: son değiştirilen sorular (düzenlenme zamanı / check-solve sonucu)
  const [editedFilter, setEditedFilter] = useState<'all' | 'son24' | 'son7' | 'cevap' | 'kurulan'>('all');
  const [denetleyiciFilter, setDenetleyiciFilter] = useState<'all' | 'denetleyici_only' | 'standard_only'>('all');
  const [versionViewOverrides, setVersionViewOverrides] = useState<Record<string, 'denetleyici' | 'eski' | 'karsilastir'>>({});
  const [analysisOpen, setAnalysisOpen] = useState<Record<string, boolean>>({});
  const [newnessFilter, setNewnessFilter] = useState<'all' | 'new_only' | 'archived_only'>('all');
  const [manualFilter, setManualFilter] = useState<'all' | 'manual_only' | 'standard_only'>('all');
  const [repeatedFilter, setRepeatedFilter] = useState<'all' | 'repeated_only' | 'unique_only'>('all');
  const [quarantineFilter, setQuarantineFilter] = useState<'standard' | 'karantina' | 'inaccessible' | 'all'>('standard');
  const [viewMode, setViewMode] = useState<'redacted' | 'raw' | 'split'>('redacted');
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [answerFilter, setAnswerFilter] = useState<'all' | 'with' | 'without' | 'doubtful'>('all');
  const [selectedTopic, setSelectedTopic] = useState<string>('all');
  const [suggestOpen, setSuggestOpen] = useState(false);
  const [advFiltersOpen, setAdvFiltersOpen] = useState(false);
  const searchRef = useRef<HTMLInputElement>(null);
  // Kendini sına: cevaplar gizli, şıkka dokununca doğru cevap görünür (cihazda hatırlanır)
  const [quizMode, setQuizMode] = useState<boolean>(() => {
    try { return localStorage.getItem('cikmis_quiz') === '1'; } catch { return false; }
  });
  const [picks, setPicks] = useState<Record<string, string>>({});
  // Kart / Kompakt görünüm (cihazda hatırlanır) ve Kart görünümünde kademeli çizim sınırı
  const [gorunum, setGorunum] = useCikmisGorunum();
  const RICH_STEP = 20;
  const [richLimit, setRichLimit] = useState(RICH_STEP);
  // Çözüm durumu (studyStore: bu cihazdaki cevaplar) ve kaydedilen sorular
  const [attempts, setAttempts] = useState<Record<string, AttemptRecord>>(() => getProgress());
  const [savedIds, setSavedIds] = useState<Set<string>>(() => getFavorites());
  const [statusFilter, setStatusFilter] = useState<'all' | 'unsolved' | 'wrong' | 'saved'>('all');
  // Liste, segment seçildiği andaki duruma göre süzülür: cevaplanan kart "Çözülmedi" listesinden anında kaybolmasın
  const [statusSnap, setStatusSnap] = useState<{ attempts: Record<string, AttemptRecord>; saved: Set<string> }>(() => ({ attempts: getProgress(), saved: getFavorites() }));
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

  // Hata bildirimi ve değişim geçmişi penceresi için seçilen soru
  const [selectedQuestionForReportHistory, setSelectedQuestionForReportHistory] = useState<QuestionItem | null>(null);

  // Cümle/Metin odaklama parametresi (?highlight=...) kontrolü
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const sp = new URLSearchParams(window.location.search);
      const hl = sp.get('highlight');
      if (hl) {
        setTimeout(() => triggerDomHighlightAndScroll(hl), 450);
      }
    }
  }, [sharedId]);

  // Cevabı belirsiz sorular TanStack Query ile önbelleklenir ve arka planda güncellenir
  const { data: rawDoubtData } = useAnswerDoubtfulQuery();
  const [doubtOverrides, setDoubtOverrides] = useState<{
    ids: Set<string>;
    options: Record<string, Record<string, string>>;
    resolved: Record<string, { answer: string; by: string }>;
  } | null>(null);

  const doubtInfo = useMemo(() => {
    if (!rawDoubtData && !doubtOverrides) return null;
    const baseIds = rawDoubtData?.ids ? new Set(rawDoubtData.ids) : new Set<string>();
    const baseOptions = { ...(rawDoubtData?.options || {}) };
    const baseResolved = { ...(rawDoubtData?.resolved || {}) };

    if (doubtOverrides) {
      doubtOverrides.ids.forEach((id) => baseIds.add(id));
      Object.assign(baseOptions, doubtOverrides.options);
      Object.assign(baseResolved, doubtOverrides.resolved);
    }

    return { ids: baseIds, options: baseOptions, resolved: baseResolved };
  }, [rawDoubtData, doubtOverrides]);

  // Yapay zekâ inceleme kuyruğu (TanStack Query ile önbellekli)
  const { data: aiQueueData, refetch: refetchAiQueue } = useAiReviewQueueQuery();
  const aiQueue = useMemo(() => aiQueueData?.items || {}, [aiQueueData]);
  const loadAiQueue = useCallback(() => { refetchAiQueue(); }, [refetchAiQueue]);

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
      setDoubtOverrides((prev) => ({
        ids: prev?.ids ? new Set([...prev.ids, String(q.id)]) : new Set([String(q.id)]),
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
      (document.querySelector('[data-page-search]') as HTMLInputElement | null)?.focus();
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);
  const [explanationFilter, setExplanationFilter] = useState<'all' | 'with' | 'without'>('all');
  const [sortOrder, setSortOrder] = useState<'default' | 'newest' | 'oldest' | 'number' | 'quality_desc' | 'quality_asc' | 'popular' | 'discipline' | 'updated'>('default');
  // Faz 14 düzeltmesinin öncesi yalnız istenince gösterilir (rozet ⓘ ya da İşlemler menüsü)
  const [p14Open, setP14Open] = useState<Record<string, boolean>>({});
  const [ambiguityTab, setAmbiguityTab] = useState<'valid' | 'ambiguous' | 'reported' | 'quarantined' | 'all'>('valid');
  
  // Per-question card override: questionId -> 'redacted' | 'raw' | 'split'
  const [cardViewOverrides, setCardViewOverrides] = useState<Record<string, 'redacted' | 'raw' | 'split'>>({});
  
  // Selected Öğren modülü match modal state
  const [selectedLearnMatch, setSelectedLearnMatch] = useState<{
    question: QuestionItem;
    match: QuestionLearnMatch;
  } | null>(null);
  // Eşleşme indeksi hafif gelir; anlatım/inciler/kartlar pencere açılınca yalnız o desteden yüklenir
  useEffect(() => {
    const m = selectedLearnMatch?.match;
    if (!m) return;
    let alive = true;
    learnMatcher.withDetails(m).then((full) => {
      if (alive && full !== m) setSelectedLearnMatch((prev) => (prev && prev.match === m ? { ...prev, match: full } : prev));
    });
    return () => { alive = false; };
  }, [selectedLearnMatch?.match]);

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
  const [focusCommentId, setFocusCommentId] = useState<string | null>(null);
  // Derin bağlantı: /cikmis/<id>?sec=comments yorumları açar. Bildirimden uygulama içinde gelinince (popstate)
  // paylaşılan soru ve bölüm yeniden okunur; sayfa yenilenmez.
  useEffect(() => {
    const apply = () => {
      try {
        const r = parseLocation();
        const id = r.route === 'past_exams' && r.param ? r.param : null;
        if (id) setSharedId(id);
        const sec = new URLSearchParams(window.location.search).get('sec');
        if (id && sec === 'comments') setExpandedCommentsQuestionId(id);
        // #comm-<yorum> çapası: yorum kapalı bir yanıt zincirindeyse zincir açılır.
        const anchor = decodeURIComponent(window.location.hash.slice(1));
        setFocusCommentId(anchor.startsWith('comm-') ? anchor.slice(5) : null);
      } catch { /* yoksay */ }
    };
    apply();
    window.addEventListener('popstate', apply);
    return () => window.removeEventListener('popstate', apply);
  }, []);
  const [newCommentText, setNewCommentText] = useState('');
  // Yanıtlanan yorum (soru + yorum kimliği + yazar); gönderince temizlenir
  const [replyTo, setReplyTo] = useState<{ qId: string; id: string; author: string } | null>(null);
  const [openThreads, setOpenThreads] = useState<Record<string, boolean>>({});
  const [isSubmittingComment, setIsSubmittingComment] = useState(false);

  // Feedback & Copy state
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [deletingQuestionId, setDeletingQuestionId] = useState<string | null>(null);

  // Client-Side Caching & Delta-Sync State
  const [cacheStatus, setCacheStatus] = useState<CacheSyncStatus>(pastQuestionsCache.getStatus());

  // Load questions - Tüm sorular yüklenir ve etiketlenir; filtreler ile karantina ve erişilemeyen sorulara doğrudan erişilir
  const loadPastQuestions = async () => {
    setIsLoading(true);
    try {
      const data = await ApiService.getPastQuestions();
      const processed = data
        .filter(q => !q.id?.startsWith('civan-') && !q.tags?.some((t: string) => /civan/i.test(t)))
        .map(q => {
          const normComm = normalizeCommitteeId(q.committeeId);
          const normDisc = normalizeDonem3Discipline(q.discipline);
          const isQuarantined = Boolean(
            (q as any).isQuarantined ||
            (q as any).quarantined ||
            (Array.isArray(q.tags) && q.tags.includes('karantina'))
          );
          const isDonem3 = isDonem3Question({ ...q, committeeId: normComm || q.committeeId });
          const isHidden = Boolean((q as any).hidden || (q as any).data?.hidden);
          const isInaccessible = isQuarantined || !isDonem3 || isHidden;
          return {
            ...q,
            committeeId: normComm || q.committeeId,
            discipline: normDisc || q.discipline,
            isQuarantined,
            isInaccessible,
            isDonem3,
          };
        });
      setQuestions(processed);
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

  const [editingCommentId, setEditingCommentId] = useState<string | null>(null);
  const [editCommentText, setEditCommentText] = useState('');
  const [isUpdatingComment, setIsUpdatingComment] = useState(false);

  const getMyCommentIds = (): string[] => {
    try {
      const raw = localStorage.getItem('my_comment_ids');
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  };

  const saveMyCommentId = (id: string) => {
    try {
      const cur = getMyCommentIds();
      if (!cur.includes(id)) {
        localStorage.setItem('my_comment_ids', JSON.stringify([...cur, id]));
      }
    } catch (_) {}
  };

  const saveMyReportId = (id: string) => {
    try {
      const raw = localStorage.getItem('my_report_ids');
      const cur = raw ? JSON.parse(raw) : [];
      if (!cur.includes(id)) {
        localStorage.setItem('my_report_ids', JSON.stringify([...cur, id]));
      }
    } catch (_) {}
  };

  const canManageComment = (c: any) => {
    if (isAdminUser) return true;
    if (!c) return false;
    if (currentUser?.uid && c.authorUid === currentUser.uid) return true;
    if (currentUser?.email && c.authorEmail && c.authorEmail.toLowerCase() === currentUser.email.toLowerCase()) return true;
    if (currentUser?.displayName && c.author && c.author.trim().toLowerCase() === currentUser.displayName.trim().toLowerCase()) return true;
    if (getMyCommentIds().includes(c.id)) return true;
    return false;
  };

  // Submit Question Comment ("Öneri / Çözüm Yolu Ekle")
  const handleCommentSubmit = async (qId: string) => {
    if (!newCommentText.trim()) return;
    const sanitizedText = censorProfanity(newCommentText.trim());
    setIsSubmittingComment(true);
    try {
      const res = await ApiService.commentPastQuestion(
        qId,
        currentUser?.displayName || 'Tıp Öğrencisi',
        sanitizedText,
        {
          uid: currentUser?.uid,
          email: currentUser?.email ?? undefined,
          parentId: replyTo && replyTo.qId === qId ? replyTo.id : undefined,
        }
      );
      if (res && res.comment) {
        logActivity('katki', replyTo && replyTo.qId === qId ? 'Bir yoruma yanıt yazdın' : 'Bir soruya yorum yazdın');
        if (res.comment.id) saveMyCommentId(res.comment.id);
        if (replyTo && replyTo.qId === qId && !res.comment.parentId) res.comment.parentId = replyTo.id;
        setReplyTo(null);
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

  const handleCommentEdit = async (qId: string, commentId: string) => {
    if (!editCommentText.trim()) return;
    const sanitizedEdit = censorProfanity(editCommentText.trim());
    setIsUpdatingComment(true);
    try {
      const res = await ApiService.editPastComment(
        qId,
        commentId,
        sanitizedEdit,
        {
          uid: currentUser?.uid,
          email: currentUser?.email ?? undefined,
          author: currentUser?.displayName ?? undefined,
          adminEmail: isAdminUser ? (currentUser?.email || ADMIN_EMAIL) : undefined,
        }
      );
      if (res.success) {
        setQuestions(prev => prev.map(q => {
          if (q.id === qId) {
            const comments = ((q as any).comments || []).map((c: any) =>
              c.id === commentId ? { ...c, text: editCommentText.trim(), isEdited: true, updatedAt: new Date().toISOString() } : c
            );
            return { ...q, comments };
          }
          return q;
        }));
        setEditingCommentId(null);
      } else {
        alert(res.message || 'Yorum güncellenemedi.');
      }
    } catch (e: any) {
      alert('Yorum güncellenemedi: ' + (e.message || 'Bağlantı hatası'));
    } finally {
      setIsUpdatingComment(false);
    }
  };

  const handleCommentDelete = async (qId: string, commentId: string) => {
    if (!(await confirmDialog({ title: 'Yorum silinsin mi?', message: 'Yorum kalıcı olarak kaldırılır.', confirmLabel: 'Sil', tone: 'danger' }))) {
      return;
    }
    try {
      const res = await ApiService.deletePastComment(
        qId,
        commentId,
        {
          uid: currentUser?.uid,
          email: currentUser?.email ?? undefined,
          author: currentUser?.displayName ?? undefined,
          adminEmail: isAdminUser ? (currentUser?.email || ADMIN_EMAIL) : undefined,
        }
      );
      if (res.success) {
        setQuestions(prev => prev.map(q => {
          if (q.id === qId) {
            const comments = ((q as any).comments || []).filter((c: any) => c.id !== commentId);
            return { ...q, comments };
          }
          return q;
        }));
      } else {
        alert(res.message || 'Yorum silinemedi.');
      }
    } catch (e: any) {
      alert('Yorum silinemedi: ' + (e.message || 'Bağlantı hatası'));
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
        const processedUpdated = updatedList
          .filter(q => !q.id?.startsWith('civan-') && !q.tags?.some((t: string) => /civan/i.test(t)))
          .map(q => {
            const normComm = normalizeCommitteeId(q.committeeId);
            const normDisc = normalizeDonem3Discipline(q.discipline);
            const isQuarantined = Boolean(
              (q as any).isQuarantined ||
              (q as any).quarantined ||
              (Array.isArray(q.tags) && q.tags.includes('karantina'))
            );
            const isDonem3 = isDonem3Question({ ...q, committeeId: normComm || q.committeeId });
            const isHidden = Boolean((q as any).hidden || (q as any).data?.hidden);
            const isInaccessible = isQuarantined || !isDonem3 || isHidden;
            return {
              ...q,
              committeeId: normComm || q.committeeId,
              discipline: normDisc || q.discipline,
              isQuarantined,
              isInaccessible,
              isDonem3,
            };
          });
        if (processedUpdated.length === 0) return;
        const updateMap = new Map(processedUpdated.map(q => [q.id, q]));
        setQuestions(prev => {
          let hasChange = false;
          const next = prev.map(existing => {
            if (updateMap.has(existing.id)) {
              hasChange = true;
              return updateMap.get(existing.id)!;
            }
            return existing;
          });
          for (const newQ of processedUpdated) {
            if (!prev.some(p => p.id === newQ.id)) {
              next.unshift(newQ);
              hasChange = true;
            }
          }
          return hasChange ? next : prev;
        });
      }
    });

    let idleTimer: any = null;
    if ((onOpenNote || currentUser?.email === ADMIN_EMAIL || currentUser?.isAdmin) && (!lectureNotes || lectureNotes.length === 0)) {
      idleTimer = setTimeout(() => {
        ApiService.getLectureNotes()
          .then(notes => {
            if (notes && notes.length > 0) setInternalNotes(notes);
          })
          .catch(err => console.warn('Could not fetch lecture notes for past exams:', err));
      }, 1500);
    }

    return () => {
      unsubscribe();
      if (idleTimer) clearTimeout(idleTimer);
    };
  }, []);

  // Upvote / Like toggle — kişi başı tek oy, ikinci basış geri çeker
  // Oy uçları aç/kapa çalışır: istek sürerken gelen ikinci dokunuş sunucuda oyu geri alıyor, ekranla
  // veri ayrışıyordu. Aynı soruda istek bitene kadar yeni oy dokunuşu yok sayılır (tek uçuş kilidi).
  const voteInFlight = useRef<Set<string>>(new Set());
  const handleToggleLike = async (q: QuestionItem) => {
    if (voteInFlight.current.has(q.id)) return;
    voteInFlight.current.add(q.id);
    const userUid = getVoterId(currentUser);
    const liked = toggledVote(q, userUid);
    const undoDislike = liked.likedBy.includes(userUid) && (q.dislikedBy || []).includes(userUid);
    const dis = undoDislike ? toggledVote({ upvotes: q.downvotes, likedBy: q.dislikedBy }, userUid) : { upvotes: q.downvotes || 0, likedBy: q.dislikedBy || [] };
    const newUpvotes = liked.upvotes, newLikedBy = liked.likedBy;
    const newDownvotes = dis.upvotes, newDislikedBy = dis.likedBy;

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
    } finally {
      voteInFlight.current.delete(q.id);
    }
  };

  // Downvote / Dislike toggle
  const handleToggleDislike = async (q: QuestionItem) => {
    if (voteInFlight.current.has(q.id)) return;
    voteInFlight.current.add(q.id);
    const userUid = getVoterId(currentUser);
    const dis = toggledVote({ upvotes: q.downvotes, likedBy: q.dislikedBy }, userUid);
    const undoLike = dis.likedBy.includes(userUid) && (q.likedBy || []).includes(userUid);
    const liked = undoLike ? toggledVote(q, userUid) : { upvotes: q.upvotes || 0, likedBy: q.likedBy || [] };
    const newUpvotes = liked.upvotes, newLikedBy = liked.likedBy;
    const newDownvotes = dis.upvotes, newDislikedBy = dis.likedBy;

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
    } finally {
      voteInFlight.current.delete(q.id);
    }
  };

  // Copy question text to clipboard
  const handleCopyQuestion = (q: QuestionItem) => {
    const stem = q.reconstruction?.stem || q.fragments?.[0]?.text || q.topic;
    const optionsSource = (item: QuestionItem) => (item.reconstruction?.options || item.options || []) as any[];
    void copyQuestion(stem, optionsSource(q));
    setCopiedId(q.id);
    setTimeout(() => setCopiedId(null), 2000);
  };
  const handleShareQuestion = async (q: QuestionItem, subTarget?: string) => {
    await shareDeepLink({
      type: 'past_question',
      id: q.id,
      committeeId: q.committeeId,
      subTarget,
    });
  };

  // Yönetici: Çıkmış soruyu kalıcı olarak sil
  const handleDeletePastQuestion = async (targetQ: QuestionItem) => {
    if (!isAdminUser) return;
    const label = targetQ.questionNumber ? `Soru #${targetQ.questionNumber}'ı` : 'Bu çıkmış soruyu';
    const confirmMsg = `${label} (${targetQ.discipline || 'Çıkmış soru'})\n\nKalıcı olarak tüm veritabanlarından, sunucudan ve cihaz önbelleğinden silmek istediğinize emin misiniz?\n\nBu işlem geri alınamaz.`;
    if (!(await confirmDialog({ title: 'Soru kalıcı olarak silinsin mi?', message: confirmMsg, confirmLabel: 'Kalıcı sil', tone: 'danger' }))) return;

    setDeletingQuestionId(targetQ.id);
    try {
      await ApiService.adminDeletePastQuestion(currentUser?.email || ADMIN_EMAIL, targetQ.id);
      try {
        await pastQuestionsCache.removeQuestions([targetQ.id]);
      } catch {}
      try {
        const { broadcastLiveEvent } = await import('../services/supabaseDb');
        broadcastLiveEvent('past_questions_changed', { eventType: 'DELETE', old: { id: targetQ.id }, id: targetQ.id });
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
  const filterSig = `${searchQuery}|${selectedCommittee}|${selectedDiscipline}|${selectedTopic}|${selectedYear}|${answerFilter}|${ambiguityTab}|${quarantineFilter}`;
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
      const yearVal = parseInt((q.examYear || '').match(/\d{4}/)?.[0] || '0', 10);
      const qScore = getQualityScore(q);
      const popScore = (q.upvotes || 0) - (q.downvotes || 0) + (q.comments?.length || 0);
      const updTime = Date.parse(String(anyQ.updatedAt || q.createdAt || 0)) || 0;
      return {
        q,
        disc,
        topic: String(q.topic || ''),
        year: yearKey(q.examYear),
        yearNum: yearVal,
        qualityScore: qScore,
        popularityScore: popScore,
        updatedTimestamp: updTime,
        comms: uncertain ? (content ? [content] : []) : Array.from(new Set([q.committeeId, content].filter(Boolean) as string[])),
        isNew: isNewQ(q),
        isManual: Boolean(q.is_manual_entry || (q as any).manuel_ekleme || (Array.isArray(q.tags) && q.tags.includes('manuel_ekleme'))),
        isRepeated: Boolean((q.appearanceCount && q.appearanceCount > 1) || (q.similarPastQuestions && q.similarPastQuestions.length > 0) || (Array.isArray(q.tags) && q.tags.includes('tekrarlayan_soru'))),
        hasAnswer: Boolean(q.correctAnswer || q.claimedAnswer || q.reconstruction?.correctAnswer) && !(isPhase14Pending(q) && !anyQ.phase14Original?.correctAnswer),
        doubtful: isDoubtful(q),
        hasExpl: Boolean(expl.trim()),
        isQuarantined: Boolean(anyQ.isQuarantined || (Array.isArray(q.tags) && q.tags.includes('karantina'))),
        isInaccessible: Boolean(anyQ.isInaccessible),
        isDonem3: Boolean(anyQ.isDonem3 !== false),
        get fields() {
          if (anyQ._cachedFields) return anyQ._cachedFields;
          const f: SearchField[] = [
            { text: foldText(stem), weight: 3 },
            { text: foldText(opts), weight: 2 },
            { text: foldText(`${q.topic || ''} \n ${disc}`), weight: 2 },
            { text: foldText(expl), weight: 0.8 },
            { text: foldText(`${q.id} ${q.examYear || ''} ${q.sourceFile || ''} ${(q.fragments || []).map((f: any) => f.text).join(' ')}`), weight: 0.6 },
          ];
          anyQ._cachedFields = f;
          return f;
        },
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
      (ambiguityTab === 'reported' && hasOpenReport(p.q)) ||
      (ambiguityTab === 'quarantined' && p.isQuarantined),
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
    edited: (p) => editedFilter === 'all' || editedTags(p.q, p.updatedTimestamp).includes(editedFilter),
    quarantine: (p) => {
      if (quarantineFilter === 'standard') {
        return !p.isQuarantined && p.isDonem3 && (!((p.q as any).hidden || (p.q as any).data?.hidden) || isAdminUser);
      }
      if (quarantineFilter === 'karantina') {
        return p.isQuarantined;
      }
      if (quarantineFilter === 'inaccessible') {
        return p.isInaccessible;
      }
      if (quarantineFilter === 'all') {
        return true;
      }
      return true;
    },
  };
  const facetValues: Record<FacetKey, (p: Prep) => (string | null)[]> = {
    pool: (p) => [p.q.isAmbiguous ? 'ambiguous' : 'valid', hasOpenReport(p.q) ? 'reported' : null, p.isQuarantined ? 'quarantined' : null],
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
    edited: (p) => editedTags(p.q, p.updatedTimestamp),
    quarantine: (p) => [
      !p.isQuarantined && p.isDonem3 && (!((p.q as any).hidden || (p.q as any).data?.hidden) || isAdminUser) ? 'standard' : null,
      p.isQuarantined ? 'karantina' : null,
      p.isInaccessible ? 'inaccessible' : null,
      'all',
    ],
  };

  const { filteredQuestions, facetCounts, statusCounts } = useMemo(() => {
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
    if (sortOrder === 'default' && searchScores) hits.sort((a, b) => (searchScores.get(b.q.id) || 0) - (searchScores.get(a.q.id) || 0));
    else if (sortOrder === 'newest') hits.sort((a, b) => b.yearNum - a.yearNum);
    else if (sortOrder === 'oldest') hits.sort((a, b) => (a.yearNum || 9999) - (b.yearNum || 9999));
    else if (sortOrder === 'number') hits.sort((a, b) => (a.q.questionNumber || 9999) - (b.q.questionNumber || 9999));
    else if (sortOrder === 'quality_desc') hits.sort((a, b) => b.qualityScore - a.qualityScore);
    else if (sortOrder === 'quality_asc') hits.sort((a, b) => a.qualityScore - b.qualityScore);
    else if (sortOrder === 'popular') hits.sort((a, b) => b.popularityScore - a.popularityScore);
    else if (sortOrder === 'discipline') hits.sort((a, b) => a.disc.localeCompare(b.disc, 'tr') || (a.q.questionNumber || 0) - (b.q.questionNumber || 0));
    else if (sortOrder === 'updated') hits.sort((a, b) => b.updatedTimestamp - a.updatedTimestamp);
    const all = hits.map((p) => p.q);
    // Durum segmenti (Tümü / Çözülmedi / Yanlışlar / Kaydedilenler): sayılar canlı, liste seçim anındaki duruma göre
    const statusCounts = { all: all.length, unsolved: 0, wrong: 0, saved: 0 };
    for (const q of all) {
      const a = attempts[q.id];
      if (!a) statusCounts.unsolved++;
      else if (!a.correct) statusCounts.wrong++;
      if (savedIds.has(q.id)) statusCounts.saved++;
    }
    const list = statusFilter === 'all'
      ? all
      : all.filter((q) => {
          const a = statusSnap.attempts[q.id];
          if (statusFilter === 'unsolved') return !a;
          if (statusFilter === 'wrong') return Boolean(a && !a.correct);
          return statusSnap.saved.has(q.id);
        });
    return { filteredQuestions: list, facetCounts: counts, statusCounts };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter, statusSnap, attempts, savedIds, prepared, searchScores, ambiguityTab, selectedCommittee, selectedYear, selectedDiscipline, selectedTopic, answerFilter, explanationFilter, sourceFilter, phase14Filter, denetleyiciFilter, newnessFilter, manualFilter, repeatedFilter, quarantineFilter, editedFilter, sortOrder]);
  const fc = (k: FacetKey, v = 'all') => facetCounts[k].get(v) || 0;

  // Seçili kurul/ders artık sonuç vermiyorsa (başka seçim yüzünden) seçimi düşürme: kullanıcı neyi seçtiyse o kalır,
  // yalnızca listelerde 0 sayılı seçenekler sönük gösterilir.
  const committeeList = useMemo(() => {
    const present = new Set<string>();
    for (const q of questions) {
      if (q.committeeId) present.add(q.committeeId);
      if ((q as any).contentCommitteeId) present.add((q as any).contentCommitteeId);
    }
    const order = ['donem3-kurul1', 'donem3-kurul2', 'donem3-kurul3', 'donem3-kurul4', 'donem3-kurul5', 'donem3-kurul6', 'donem3-final', 'donem3-butunleme'];
    return order.filter((c) => present.has(c));
  }, [questions]);
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
        .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'tr'))
        .slice(0, 40),
    [facetCounts],
  );
  const yearList = useMemo(
    // En yeni sınav yılı önce
    () => Array.from(new Set(prepared.map((p) => p.year))).filter((y) => !y.includes('2026') && !y.toLowerCase().includes('civan')).sort().reverse(),
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
  // Birleştirilen sorunun eski kimliği (arama dizini, eski paylaşım bağlantısı) yaşayan kayda yönlenir.
  const mergedTarget = useMemo(() => {
    if (!sharedId || questions.some((q) => String(q.id) === sharedId)) return null;
    const has = (v: unknown) => (Array.isArray(v) ? v.map(String).includes(sharedId) : false);
    return questions.find((q: any) => has(q.mergedFrom) || has(q.mergedQuestionIds)) || null;
  }, [sharedId, questions]);
  useEffect(() => {
    if (!mergedTarget) return;
    const id = String(mergedTarget.id);
    setSharedId(id);
    writeLocation('past_exams', id, true);
  }, [mergedTarget]);
  const paginatedQuestions = useMemo(() => {
    if (sharedId) return questions.filter((q) => String(q.id) === sharedId);
    if (gorunum === 'kart') return filteredQuestions.slice(0, richLimit);
    const start = (currentPage - 1) * itemsPerPage;
    return filteredQuestions.slice(start, start + itemsPerPage);
  }, [filteredQuestions, currentPage, sharedId, questions, gorunum, richLimit]);
  // Süzgeç sonucu değişince Kart görünümü yeniden ilk 20 kartla başlar
  useEffect(() => { setRichLimit(RICH_STEP); }, [filteredQuestions]);

  const resetPage = () => setCurrentPage(1);
  const LABELS = {
    pool: { valid: 'Tam metin', ambiguous: 'İncelemede', reported: 'Hata bildirilen', quarantined: 'Karantina', all: 'Tüm havuz' } as Record<string, string>,
    quarantine: {
      standard: 'Standart (Yayında)',
      karantina: 'Karantinaya Alınanlar',
      inaccessible: 'Tüm Erişilemeyenler',
      all: 'Tüm Sorular (Karantina Dahil)',
    } as Record<string, string>,
    answer: { with: 'Cevaplı', without: 'Cevapsız', doubtful: 'Cevap belirsiz' } as Record<string, string>,
    source: { gemini_v3: 'Gemini v3', existing: 'Mevcut veriler' } as Record<string, string>,
    p14: { faz14: 'Faz 14', faz14_onayli: 'Faz 14 · onaylı', faz14_bekleyen: 'Faz 14 · onay bekliyor' } as Record<string, string>,
    denetleyici: { denetleyici_only: 'Denetleyici Onayı', standard_only: 'Standart' } as Record<string, string>,
    newness: { new_only: 'Yeni sorular', archived_only: 'Arşiv' } as Record<string, string>,
    manual: { manual_only: 'Manuel Eklenenler', standard_only: 'Otomatik Havuz' } as Record<string, string>,
    repeated: { repeated_only: 'Tekrarlayan Sorular', unique_only: 'Tekil Sorular' } as Record<string, string>,
    edited: { son24: 'Son 24 saatte değişen', son7: 'Son 7 günde değişen', cevap: 'Cevabı düzeltilen', kurulan: 'Şıkları sonradan kurulan' } as Record<string, string>,
    sort: { newest: 'Yeniden eskiye', oldest: 'Eskiden yeniye', number: 'Soru numarası', quality_desc: 'Kalite: en iyi önce', quality_asc: 'Kalite: en sorunlu önce', popular: 'En popüler', discipline: 'Derse göre', updated: 'Son güncellenen', default: searchQuery.trim() ? 'En ilgili' : 'Varsayılan' } as Record<string, string>,
    view: { raw: 'Ham metin', split: 'Karşılaştır' } as Record<string, string>,
  };
  // Şeritte görünmeyen etkin süzgeçler kaldırılabilir çip olarak listelenir
  const activeFilterChips: { label: string; clear: () => void }[] = [
    ...(quarantineFilter !== 'standard' ? [{ label: LABELS.quarantine[quarantineFilter] || 'Karantina', clear: () => setQuarantineFilter('standard') }] : []),
    ...(ambiguityTab !== 'valid' ? [{ label: LABELS.pool[ambiguityTab], clear: () => setAmbiguityTab('valid') }] : []),
    ...(selectedDiscipline !== 'all' ? [{ label: selectedDiscipline, clear: () => { setSelectedDiscipline('all'); setSelectedTopic('all'); } }] : []),
    ...(selectedTopic !== 'all' ? [{ label: selectedTopic, clear: () => setSelectedTopic('all') }] : []),
    ...(selectedYear !== 'all' ? [{ label: selectedYear, clear: () => setSelectedYear('all') }] : []),
    ...(answerFilter !== 'all' ? [{ label: LABELS.answer[answerFilter], clear: () => setAnswerFilter('all') }] : []),
    ...(explanationFilter !== 'all' ? [{ label: explanationFilter === 'with' ? 'Açıklamalı' : 'Açıklamasız', clear: () => setExplanationFilter('all') }] : []),
    ...(sourceFilter !== 'all' ? [{ label: LABELS.source[sourceFilter], clear: () => setSourceFilter('all') }] : []),
    ...(denetleyiciFilter !== 'all' ? [{ label: LABELS.denetleyici[denetleyiciFilter], clear: () => setDenetleyiciFilter('all') }] : []),
    ...(phase14Filter !== 'all' ? [{ label: LABELS.p14[phase14Filter], clear: () => setPhase14Filter('all') }] : []),
    ...(editedFilter !== 'all' ? [{ label: LABELS.edited[editedFilter], clear: () => setEditedFilter('all') }] : []),
    ...(newnessFilter !== 'all' ? [{ label: LABELS.newness[newnessFilter], clear: () => setNewnessFilter('all') }] : []),
    ...(manualFilter !== 'all' ? [{ label: LABELS.manual[manualFilter], clear: () => setManualFilter('all') }] : []),
    ...(repeatedFilter !== 'all' ? [{ label: LABELS.repeated[repeatedFilter], clear: () => setRepeatedFilter('all') }] : []),
    ...(viewMode !== 'redacted' ? [{ label: LABELS.view[viewMode], clear: () => setViewMode('redacted') }] : []),
  ];
  const advancedCount = activeFilterChips.length;
  // Ders ve konu hızlı süzgeç haplarında görünür; çip satırında ve Süzgeç rozetinde yalnız sayfadaki süzgeçler sayılır
  const sheetChips = activeFilterChips.filter((c) => c.label !== selectedDiscipline && c.label !== selectedTopic);
  const STATUS_LABEL: Record<string, string> = { unsolved: 'Çözülmedi', wrong: 'Yanlışlar', saved: 'Kaydedilenler' };
  const anyFilter = advancedCount > 0 || selectedCommittee !== 'all' || searchQuery.trim() !== '';
  const clearAllFilters = () => {
    setSearchQuery('');
    setAmbiguityTab('valid');
    setQuarantineFilter('standard');
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
    setEditedFilter('all');
    setSortOrder('default');
    setStatusFilter('all');
    setCurrentPage(1);
  };
  const pickCommittee = (c: string) => {
    setSelectedCommittee(c);
    resetPage();
    if (c !== 'all' && selectedDiscipline !== 'all') {
      const commObj = OFFICIAL_CURRICULUM_COMMITTEES.find((x) => x.id === c);
      if (commObj && !commObj.allDisciplineNames.map((d) => normalizeDonem3Discipline(d) || d).includes(selectedDiscipline)) setSelectedDiscipline('all');
    }
  };
  const pickStatus = (v: 'all' | 'unsolved' | 'wrong' | 'saved') => {
    setStatusSnap({ attempts: getProgress(), saved: getFavorites() });
    setStatusFilter(v);
    resetPage();
  };
  // Kart görünümü: cevap bu cihazın çalışma kaydına yazılır (studyStore → Çalış ekranı, yanlışlar tekrar listesine)
  const handleRichAnswer = (q: QuestionItem, key: string, correct: boolean) => {
    setAttempts({ ...recordAttempt(String(q.id), key as OptionKey, correct) });
  };
  const toggleSave = (id: string) => {
    setSavedIds((prev) => {
      const s = setFavorite(id, !prev.has(id));
      toast.success(s.has(id) ? 'Kaydedildi' : 'Kayıttan çıkarıldı');
      return new Set(s);
    });
  };
  // Ders notunda aç: mevcut slayt/sayfa eşleştiricisi; eşleşme yoksa "Hakkında" penceresi (kaynak ve kanıt)
  const openNoteFor = (q: QuestionItem) => {
    const m = getQuestionSlideMatch(q);
    if (m && onOpenNote) onOpenNote(m.note.id, m.page.pageNumber);
    else {
      toast.info('Ders notu eşleşmesi yok', 'Soru hakkındaki kaynak bilgisi açıldı.');
      setAboutQuestion(q);
    }
  };
  const CardView: React.FC<PastQuestionRichCardProps> = gorunum === 'kart' ? PastQuestionRichCard : CikmisCard;
  const isAdminUser = currentUser?.email === ADMIN_EMAIL || !!currentUser?.isAdmin;
  const n = (v: number) => v.toLocaleString('tr-TR');

  // Bölümlü seçim (filtre çekmecesi): seçenek sayıları canlı
  const segRow = <T extends string>(label: string, value: T, set: (v: T) => void, opts: [T, string, number?][]) => (
    <div className="ui-row ui-row-stack cx-facet">
      <span className="cx-facet-h">{label}</span>
      <div className="cx-facet-chips" role="radiogroup" aria-label={label}>
        {opts.map(([id, text, count]) => (
          <button
            key={id}
            type="button"
            role="radio"
            aria-checked={value === id}
            onClick={() => { set(id); resetPage(); }}
            className={`cx-fchip ${count === 0 && value !== id ? 'is-zero' : ''}`}
          >
            {value === id && <Check aria-hidden />}
            {text}
            {typeof count === 'number' && <span className="n">{n(count)}</span>}
          </button>
        ))}
      </div>
    </div>
  );

  // v12 çerçevesinin girdileri (yalnız v12'de çağrılır): mevcut durum + işleyiciler, yeni veri mantığı yok
  const buildV12Props = (): Omit<React.ComponentProps<typeof CikmisV12>, 'children'> => {
    const facet = (id: string, label: string, value: string, set: (v: any) => void, opts: [string, string, number?][]): C12Facet => ({
      id, label, value, options: opts.map(([oid, l, c]) => ({ id: oid, label: l, count: c })), onPick: (v) => { set(v); resetPage(); },
    });
    // Kayıtlı görünüm: yalnız varsayılandan farklı değerler (anahtar → [değer, varsayılan, ayarlayıcı])
    const viewKeys: Record<string, [string, string, (v: any) => void]> = {
      q: [searchQuery.trim(), '', setSearchQuery], st: [statusFilter, 'all', setStatusFilter], k: [selectedCommittee, 'all', setSelectedCommittee],
      y: [selectedYear, 'all', setSelectedYear], d: [selectedDiscipline, 'all', setSelectedDiscipline], t: [selectedTopic, 'all', setSelectedTopic],
      a: [answerFilter, 'all', setAnswerFilter], e: [explanationFilter, 'all', setExplanationFilter], r: [repeatedFilter, 'all', setRepeatedFilter],
      p: [ambiguityTab, 'valid', setAmbiguityTab], n: [newnessFilter, 'all', setNewnessFilter], m: [viewMode, 'redacted', setViewMode], s: [sortOrder, 'default', setSortOrder],
      ...(isAdminUser ? {
        kr: [quarantineFilter, 'standard', setQuarantineFilter], ky: [sourceFilter, 'all', setSourceFilter], dn: [denetleyiciFilter, 'all', setDenetleyiciFilter],
        f14: [phase14Filter, 'all', setPhase14Filter], sd: [editedFilter, 'all', setEditedFilter], ma: [manualFilter, 'all', setManualFilter],
      } as Record<string, [string, string, (v: any) => void]> : {}),
    };
    return {
      total: filteredQuestions.length,
      shown: paginatedQuestions.length,
      scope: selectedCommittee !== 'all' ? committeeShort(selectedCommittee) : undefined,
      search: { value: searchQuery, onChange: (v) => { setSearchQuery(v); resetPage(); } },
      suggest: {
        disciplines: suggestions.disciplines,
        topics: suggestions.topics,
        onDiscipline: (d) => { setSelectedDiscipline(d); setSelectedTopic('all'); setSearchQuery(''); resetPage(); },
        onTopic: (t) => { setSelectedTopic(t); setSearchQuery(''); resetPage(); },
      },
      status: { value: statusFilter, counts: statusCounts, onPick: pickStatus },
      committee: committeeList.length > 1 ? {
        value: selectedCommittee,
        label: selectedCommittee !== 'all' ? committeeShort(selectedCommittee) : undefined,
        options: [{ id: 'all', label: 'Tüm kurullar', count: fc('committee') }, ...committeeList.map((c) => ({ id: c, label: committeeShort(c), count: fc('committee', c) }))],
        onPick: pickCommittee,
      } : null,
      year: {
        value: selectedYear,
        options: [{ id: 'all', label: 'Tüm yıllar', count: fc('year') }, ...yearList.map((y) => ({ id: y, label: y, count: fc('year', y) }))],
        onPick: (y) => { setSelectedYear(y); resetPage(); },
      },
      discipline: {
        value: selectedDiscipline,
        label: selectedDiscipline !== 'all' ? disciplineLabel(selectedDiscipline) || selectedDiscipline : undefined,
        options: [
          { id: 'all', label: 'Tüm dersler', count: fc('discipline') },
          ...groupDisciplines(disciplineList.filter((d) => fc('discipline', d) > 0 || selectedDiscipline === d), (d) => d, (d) => fc('discipline', d))
            .flatMap((g) => g.items.map((d) => ({ id: d, label: disciplineLabel(d) || d, count: fc('discipline', d), group: g.label }))),
        ],
        onPick: (d) => { setSelectedDiscipline(d); setSelectedTopic('all'); resetPage(); },
      },
      topic: selectedDiscipline !== 'all' && (topicList.length > 0 || selectedTopic !== 'all') ? {
        value: selectedTopic,
        options: [{ id: 'all', label: 'Tüm konular' }, ...topicList.map(([t, cnt]) => ({ id: t, label: t, count: cnt }))],
        onPick: (t) => { setSelectedTopic(t); resetPage(); },
      } : null,
      sort: {
        value: sortOrder,
        options: (['default', 'newest', 'oldest', 'number', 'discipline', 'popular', 'updated', 'quality_desc', 'quality_asc'] as const).map((k) => ({ id: k, label: LABELS.sort[k] })),
        onPick: (v) => { setSortOrder(v as typeof sortOrder); resetPage(); },
      },
      facets: [
        facet('cevap', 'Cevap', answerFilter, setAnswerFilter, [['all', 'Tümü', fc('answer')], ['with', 'Cevaplı', fc('answer', 'with')], ['without', 'Cevapsız', fc('answer', 'without')], ['doubtful', 'Cevabı tartışmalı', fc('answer', 'doubtful')]]),
        facet('aciklama', 'Açıklama', explanationFilter, setExplanationFilter, [['all', 'Tümü', fc('explanation')], ['with', 'Var', fc('explanation', 'with')], ['without', 'Yok', fc('explanation', 'without')]]),
        facet('tekrar', 'Tekrar', repeatedFilter, setRepeatedFilter, [['all', 'Tümü', fc('repeated')], ['repeated_only', 'Birden çok sınavda', fc('repeated', 'repeated_only')], ['unique_only', 'Tek sınavda', fc('repeated', 'unique_only')]]),
        facet('havuz', 'Havuz', ambiguityTab, setAmbiguityTab, [['valid', 'Tam metin', fc('pool', 'valid')], ['ambiguous', 'İncelemede', fc('pool', 'ambiguous')], ['reported', 'Hata bildirilen', fc('pool', 'reported')], ['quarantined', 'Karantina', fc('pool', 'quarantined')], ['all', 'Tümü', fc('pool')]]),
        facet('yenilik', 'Yenilik', newnessFilter, setNewnessFilter, [['all', 'Tümü', fc('newness')], ['new_only', 'Yeni', fc('newness', 'new_only')], ['archived_only', 'Arşiv', fc('newness', 'archived_only')]]),
        facet('metin', 'Metin', viewMode, setViewMode, [['redacted', 'Düzenlenmiş'], ['raw', 'Ham'], ['split', 'Karşılaştır']]),
      ],
      adminFacets: isAdminUser ? [
        facet('karantina', 'Karantina ve erişim', quarantineFilter, setQuarantineFilter, [['standard', 'Yayında', fc('quarantine', 'standard')], ['karantina', 'Karantinada', fc('quarantine', 'karantina')], ['inaccessible', 'Erişilemeyen', fc('quarantine', 'inaccessible')], ['all', 'Tümü', fc('quarantine', 'all')]]),
        facet('kaynak', 'Kaynak', sourceFilter, setSourceFilter, [['all', 'Tümü', fc('source')], ['gemini_v3', 'Gemini v3', fc('source', 'gemini_v3')], ['existing', 'Mevcut', fc('source', 'existing')]]),
        facet('denetleyici', 'Denetleyici', denetleyiciFilter, setDenetleyiciFilter, [['all', 'Tümü', fc('denetleyici')], ['denetleyici_only', 'Onaylı', fc('denetleyici', 'denetleyici_only')], ['standard_only', 'Onaysız', fc('denetleyici', 'standard_only')]]),
        facet('p14', 'AI inceleme', phase14Filter, setPhase14Filter, [['all', 'Tümü', fc('p14')], ['faz14', 'Faz 14', fc('p14', 'faz14')], ['faz14_onayli', 'Onaylı', fc('p14', 'faz14_onayli')], ['faz14_bekleyen', 'Onay bekliyor', fc('p14', 'faz14_bekleyen')]]),
        facet('degisiklik', 'Son değişiklik', editedFilter, setEditedFilter, [['all', 'Tümü', fc('edited')], ['son24', 'Son 24 saat', fc('edited', 'son24')], ['son7', 'Son 7 gün', fc('edited', 'son7')], ['cevap', 'Cevabı düzeltilen', fc('edited', 'cevap')], ['kurulan', 'Şıkları sonradan kurulan', fc('edited', 'kurulan')]]),
        facet('yukleme', 'Yükleme', manualFilter, setManualFilter, [['all', 'Tümü', fc('manual')], ['manual_only', 'Elle eklenen', fc('manual', 'manual_only')], ['standard_only', 'Otomatik', fc('manual', 'standard_only')]]),
      ] : undefined,
      // Kurul/yıl/ders/konu hızlı haplarda; çip satırında yalnız haplarda görünmeyenler
      chips: activeFilterChips
        .filter((c) => c.label !== selectedDiscipline && c.label !== selectedTopic && c.label !== selectedYear)
        .map((c) => ({ label: c.label, onRemove: () => { c.clear(); resetPage(); } })),
      anyFilter: anyFilter || statusFilter !== 'all' || sortOrder !== 'default',
      onClearAll: clearAllFilters,
      quiz: { on: quizMode, onToggle: () => setQuizMode((v) => !v) },
      view: { value: gorunum, onChange: setGorunum },
      adminHref: isAdminUser ? pathFor('test_cikmis') : undefined,
      practiceHref: pathFor('practice'),
      sync: { busy: cacheStatus.isSyncing, onSync: handleManualSync, deviceCount: questions.length },
      views: {
        snapshot: () => Object.fromEntries(Object.entries(viewKeys).filter(([, [v, def]]) => v !== def).map(([k, [v]]) => [k, v])),
        apply: (st) => {
          clearAllFilters();
          for (const [k, [, , set]] of Object.entries(viewKeys)) if (typeof st[k] === 'string') set(st[k]);
          if (st.st) setStatusSnap({ attempts: getProgress(), saved: getFavorites() });
        },
        suggestName: () =>
          [
            selectedCommittee !== 'all' ? committeeShort(selectedCommittee) : '',
            selectedYear !== 'all' ? selectedYear : '',
            selectedDiscipline !== 'all' ? disciplineLabel(selectedDiscipline) || selectedDiscipline : '',
            selectedTopic !== 'all' ? selectedTopic : '',
            statusFilter !== 'all' ? STATUS_LABEL[statusFilter] : '',
            ...activeFilterChips.filter((c) => ![selectedDiscipline, selectedTopic, selectedYear].includes(c.label)).map((c) => c.label),
            searchQuery.trim() ? `“${searchQuery.trim()}”` : '',
          ].filter(Boolean).join(' · ').slice(0, 80) || 'Görünüm',
      },
    };
  };

  return (
    <div className="cx">
      {/* Ortak kompakt araç çubuğu: başlık · sayı · arama · durum segmenti · Süzgeç (sayfa) · görünüm seçici */}
      {!v12 && (
      <div
        style={{ display: 'contents' }}
        onFocus={(e) => { if ((e.target as HTMLElement).matches?.('[data-page-search]')) setSuggestOpen(true); }}
        onBlur={(e) => { if ((e.target as HTMLElement).matches?.('[data-page-search]')) window.setTimeout(() => setSuggestOpen(false), 120); }}
      >
      <PageToolbar
        className="cx-pt"
        title="Çıkmış sorular"
        count={`${n(filteredQuestions.length)} soru`}
        search={{ value: searchQuery, onChange: (v) => { setSearchQuery(v); resetPage(); setSuggestOpen(true); }, placeholder: 'Soru kökü ara' }}
        quick={[
          {
            id: 'durum',
            label: 'Durum',
            value: statusFilter !== 'all' ? STATUS_LABEL[statusFilter] : undefined,
            onClear: () => pickStatus('all'),
            content: (close) => (
              <QuickOptions close={close} value={statusFilter} onPick={(v) => pickStatus(v as typeof statusFilter)} options={[
                { id: 'all', label: 'Tümü', count: statusCounts.all },
                { id: 'unsolved', label: STATUS_LABEL.unsolved, count: statusCounts.unsolved },
                { id: 'wrong', label: STATUS_LABEL.wrong, count: statusCounts.wrong },
                { id: 'saved', label: STATUS_LABEL.saved, count: statusCounts.saved },
              ]} />
            ),
          },
          ...(committeeList.length > 1 ? [{
            id: 'kurul',
            label: 'Kurul',
            value: selectedCommittee !== 'all' ? committeeShort(selectedCommittee) : undefined,
            onClear: () => pickCommittee('all'),
            content: (close: () => void) => (
              <QuickOptions close={close} value={selectedCommittee} onPick={pickCommittee} options={[
                { id: 'all', label: 'Tüm kurullar', count: fc('committee') },
                ...committeeList.map((c) => ({ id: c, label: committeeShort(c), count: fc('committee', c) })),
              ]} />
            ),
          }] : []),
          {
            id: 'ders',
            label: 'Ders',
            wide: true,
            value: selectedDiscipline !== 'all' ? disciplineLabel(selectedDiscipline) || selectedDiscipline : undefined,
            onClear: () => { setSelectedDiscipline('all'); setSelectedTopic('all'); resetPage(); },
            content: (close) => (
              <QuickOptions
                close={close}
                searchable={disciplineList.length > 8}
                placeholder="Ders ara"
                value={selectedDiscipline}
                onPick={(d) => { setSelectedDiscipline(d); setSelectedTopic('all'); resetPage(); }}
                options={[
                  { id: 'all', label: 'Tüm dersler', count: fc('discipline') },
                  ...groupDisciplines(
                    disciplineList.filter((d) => fc('discipline', d) > 0 || selectedDiscipline === d),
                    (d) => d,
                    (d) => fc('discipline', d),
                  ).flatMap((g) => g.items.map((d) => ({ id: d, label: disciplineLabel(d) || d, count: fc('discipline', d), group: g.label }))),
                ]}
              />
            ),
          },
          ...(selectedDiscipline !== 'all' && (topicList.length > 0 || selectedTopic !== 'all') ? [{
            id: 'konu',
            label: 'Konu',
            wide: true,
            value: selectedTopic !== 'all' ? selectedTopic : undefined,
            onClear: () => { setSelectedTopic('all'); resetPage(); },
            content: (close: () => void) => (
              <QuickOptions
                close={close}
                searchable={topicList.length > 8}
                placeholder="Konu ara"
                value={selectedTopic}
                onPick={(t) => { setSelectedTopic(t); resetPage(); }}
                options={[{ id: 'all', label: 'Tüm konular' }, ...topicList.map(([t, cnt]) => ({ id: t, label: t, count: cnt }))]}
              />
            ),
          }] : []),
          {
            id: 'sira',
            label: 'Sırala',
            value: sortOrder !== 'default' ? LABELS.sort[sortOrder] : undefined,
            onClear: () => { setSortOrder('default'); resetPage(); },
            content: (close) => (
              <QuickOptions close={close} value={sortOrder} onPick={(v) => { setSortOrder(v as any); resetPage(); }} options={
                (['default', 'newest', 'oldest', 'number', 'discipline', 'popular', 'updated', 'quality_desc', 'quality_asc'] as const).map((k) => ({ id: k, label: LABELS.sort[k] }))
              } />
            ),
          },
        ] as ToolbarQuick[]}
        filterTitle="Süzgeçler"
        filterCount={sheetChips.length}
        chips={sheetChips.map((c, i) => ({ id: `f${i}-${c.label}`, label: c.label, onRemove: () => { c.clear(); resetPage(); } })) as ToolbarChip[]}
        onClearChips={clearAllFilters}
        tools={<>
          {isAdminUser && (
            <a href={pathFor('test_cikmis')} className="pt-icon" title="Faz 14 düzeltme önerilerini incele" aria-label="Faz 14 incelemesi">
              <Sparkles aria-hidden />
            </a>
          )}
          <CikmisViewSwitch value={gorunum} onChange={setGorunum} />
        </>}
        filters={<>
          <fieldset className="pt-fgroup">
            <legend>Kompakt görünüm</legend>
            <button
              type="button"
              role="switch"
              aria-checked={quizMode}
              onClick={() => setQuizMode((v) => !v)}
              className="cx-pt-quiz"
              title="Kompakt kartlarda cevaplar gizlenir; şıkkı işaretleyince doğru cevap görünür (Kart görünümü her zaman böyledir)"
            >
              <span className="cx-switch" aria-hidden><i /></span>
              Kendini sına: cevapları gizle
            </button>
          </fieldset>
        <div className="cx-filters">
          <FilterGroup
            title="Sınav ve cevap"
            summary={[selectedYear !== 'all' ? selectedYear : '', answerFilter !== 'all' ? 'cevap süzgeci' : ''].filter(Boolean).join(' · ') || 'Tümü'}
          >
            <div className="ui-group">
              {segRow('Yıl', selectedYear, setSelectedYear, [['all', 'Tümü', fc('year')], ...yearList.map((y) => [y, y, fc('year', y)] as [string, string, number])])}
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
              {segRow('Tekrar', repeatedFilter, setRepeatedFilter, [
                ['all', 'Tümü', fc('repeated')],
                ['repeated_only', 'Birden çok sınavda', fc('repeated', 'repeated_only')],
                ['unique_only', 'Tek sınavda', fc('repeated', 'unique_only')],
              ])}
            </div>
          </FilterGroup>

          {/* Gelişmiş: sık kullanılmayan süzgeçler varsayılan olarak gizli */}
          <button
            type="button"
            className="rb-adv-toggle"
            aria-expanded={advFiltersOpen}
            onClick={() => setAdvFiltersOpen((v) => !v)}
          >
            <SlidersHorizontal aria-hidden />
            {advFiltersOpen ? 'Gelişmiş süzgeçleri gizle' : 'Gelişmiş süzgeçler'}
            <ChevronDown aria-hidden className={advFiltersOpen ? 'rotate-180' : ''} />
          </button>
          {advFiltersOpen && (<>
          <FilterGroup title="Durum ve görünüm">
            <div className="ui-group">
              {segRow('Havuz', ambiguityTab, setAmbiguityTab, [
                ['valid', 'Tam metin', fc('pool', 'valid')],
                ['ambiguous', 'İncelemede', fc('pool', 'ambiguous')],
                ['reported', 'Hata bildirilen', fc('pool', 'reported')],
                ['quarantined', 'Karantina', fc('pool', 'quarantined')],
                ['all', 'Tümü', fc('pool')],
              ])}
              {segRow('Yenilik', newnessFilter, setNewnessFilter, [
                ['all', 'Tümü', fc('newness')],
                ['new_only', 'Yeni', fc('newness', 'new_only')],
                ['archived_only', 'Arşiv', fc('newness', 'archived_only')],
              ])}
              {segRow('Metin', viewMode, setViewMode, [
                ['redacted', 'Düzenlenmiş'],
                ['raw', 'Ham'],
                ['split', 'Karşılaştır'],
              ])}
            </div>
          </FilterGroup>

          {isAdminUser && (
            <FilterGroup title="Yönetim" defaultOpen={false}>
              <div className="ui-group">
                {segRow('Karantina ve erişim', quarantineFilter, setQuarantineFilter, [
                  ['standard', 'Yayında', fc('quarantine', 'standard')],
                  ['karantina', 'Karantinada', fc('quarantine', 'karantina')],
                  ['inaccessible', 'Erişilemeyen', fc('quarantine', 'inaccessible')],
                  ['all', 'Tümü', fc('quarantine', 'all')],
                ])}
                {segRow('Kaynak', sourceFilter, setSourceFilter, [
                  ['all', 'Tümü', fc('source')],
                  ['gemini_v3', 'Gemini v3', fc('source', 'gemini_v3')],
                  ['existing', 'Mevcut', fc('source', 'existing')],
                ])}
                {segRow('Denetleyici', denetleyiciFilter, setDenetleyiciFilter, [
                  ['all', 'Tümü', fc('denetleyici')],
                  ['denetleyici_only', 'Onaylı', fc('denetleyici', 'denetleyici_only')],
                  ['standard_only', 'Onaysız', fc('denetleyici', 'standard_only')],
                ])}
                {segRow('AI inceleme', phase14Filter, setPhase14Filter, [
                  ['all', 'Tümü', fc('p14')],
                  ['faz14', 'Faz 14', fc('p14', 'faz14')],
                  ['faz14_onayli', 'Onaylı', fc('p14', 'faz14_onayli')],
                  ['faz14_bekleyen', 'Onay bekliyor', fc('p14', 'faz14_bekleyen')],
                ])}
                {segRow('Son değişiklik', editedFilter, setEditedFilter, [
                  ['all', 'Tümü', fc('edited')],
                  ['son24', 'Son 24 saat', fc('edited', 'son24')],
                  ['son7', 'Son 7 gün', fc('edited', 'son7')],
                  ['cevap', 'Cevabı düzeltilen', fc('edited', 'cevap')],
                  ['kurulan', 'Şıkları sonradan kurulan', fc('edited', 'kurulan')],
                ])}
                {segRow('Yükleme', manualFilter, setManualFilter, [
                  ['all', 'Tümü', fc('manual')],
                  ['manual_only', 'Elle eklenen', fc('manual', 'manual_only')],
                  ['standard_only', 'Otomatik', fc('manual', 'standard_only')],
                ])}
              </div>
            </FilterGroup>
          )}
          </>)}
        </div>
          <div className="cx-sheet-end">
            <button type="button" onClick={clearAllFilters} className="ui-btn is-ghost" disabled={!anyFilter && statusFilter === 'all'}>Tüm süzgeçleri sıfırla</button>
            <button type="button" onClick={handleManualSync} disabled={cacheStatus.isSyncing} className="ui-btn is-ghost" title={`Cihazda ${n(questions.length)} soru`}>
              <RefreshCw aria-hidden className={`w-4 h-4 ${cacheStatus.isSyncing ? 'animate-spin' : ''}`} /> Güncellemeleri denetle
            </button>
          </div>
        </>}
      >
        {suggestOpen && searchQuery.trim().length >= 2 && (
          <div className="cx-pt-suggest">
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
          </div>
        )}
      </PageToolbar>
      </div>
      )}

      {/* Derslere göz at (Apple Sağlık "Göz at" listesi): süzgeç yokken ders renkli kısa yol (v12'de Ders hapı/sütunu) */}
      {!v12 && !isLoading && !sharedId && selectedDiscipline === 'all' && !searchQuery.trim() && currentPage === 1 && (() => {
        const rows = disciplineList.map((d) => ({ d, cnt: fc('discipline', d) })).filter((r) => r.cnt > 0).sort((a, b) => b.cnt - a.cnt);
        if (rows.length < 2) return null;
        // Tek satır, yatay kayan şerit: tüm dersler sırayla; masaüstünde ‹ › ile bir ekran kayar
        const scrollBy = (dir: 1 | -1) => {
          const el = browseRef.current;
          if (el) el.scrollBy({ left: dir * Math.max(200, el.clientWidth * 0.8), behavior: 'smooth' });
        };
        return (
          <section className="hk-browse" aria-label="Derslere göz at">
            <header className="hk-sec-h">
              <h2>Derslere göz at <small className="hk-browse-cnt">{rows.length} ders</small></h2>
              <span className="hk-rail-nav">
                <button type="button" className="hk-rail-btn" onClick={() => scrollBy(-1)} aria-label="Önceki dersler"><ChevronLeft aria-hidden /></button>
                <button type="button" className="hk-rail-btn" onClick={() => scrollBy(1)} aria-label="Sonraki dersler"><ChevronRight aria-hidden /></button>
              </span>
            </header>
            <ul className="hk-browse-list is-rail" ref={browseRef}>
              {/* Gruplu: Temel tıp · Dahili · Cerrahi · Toplum sağlığı; grup içinde soru sayısına göre */}
              {groupDisciplines(rows, (r) => r.d, (r) => r.cnt).map((g, gi) => (
                <React.Fragment key={g.id}>
                  <li className="hk-rail-gl" aria-hidden><span>{g.label}</span></li>
                  {g.items.map(({ d, cnt }, i) => (
                    <li key={d} className={disciplineClass(d)} style={{ animationDelay: `${Math.min(gi * 2 + i, 8) * 30}ms` }}>
                      <button type="button" onClick={() => { setSelectedDiscipline(d); setSelectedTopic('all'); resetPage(); }} aria-label={`${g.label} · ${disciplineLabel(d)}, ${cnt} soru`}>
                        <span className="hk-tile is-sm"><BookOpen aria-hidden /></span>
                        <span className="hk-browse-t">{disciplineLabel(d)}</span>
                        <span className="hk-browse-n hk-num">{n(cnt)}</span>
                      </button>
                    </li>
                  ))}
                </React.Fragment>
              ))}
            </ul>
            <h2 className="hk-sec-title">Tüm sorular</h2>
          </section>
        );
      })()}

      {/* Questions Listing (v12: CikmisV12 çerçevesinin sonuç sütununda) */}
      <V12Frame on={v12} props={v12 ? buildV12Props : undefined}>
      {isLoading && gorunum === 'kart' ? (
        <div className="cx-list ck-list" aria-busy="true" aria-label="Çıkmış sorular yükleniyor">
          {[0, 1, 2].map((i) => <RichCardSkeleton key={i} />)}
        </div>
      ) : isLoading ? (
        <div className="bg-white rounded-2xl border border-line">
          <SectionLoader label="Çıkmış sorular yükleniyor…" />
        </div>
      ) : sharedId && paginatedQuestions.length === 0 ? (
        <div className="ms-qcard items-center text-center py-10">
          <HelpCircle className="w-8 h-8 text-ink-3" />
          <p className="m-0 text-base font-semibold">Paylaşılan soru bulunamadı</p>
          <p className="m-0 text-sm text-ink-3 max-w-sm">Soru kaldırılmış, birleştirilmiş ya da bağlantı eksik olabilir.</p>
          <button type="button" onClick={showAllQuestions} className="ms-btn is-tonal">Tüm çıkmış sorular</button>
        </div>
      ) : paginatedQuestions.length === 0 ? (
        <div className="ms-qcard ms-empty items-center text-center py-6">
          <EmptySearch size={64} />
          <p className="m-0 text-base font-semibold">Eşleşen soru yok</p>
          <p className="m-0 text-sm text-ink-3 max-w-sm">
            {searchQuery.trim() ? 'Kelimeyi kısaltmayı ya da bir süzgeci kaldırmayı dene.' : 'Seçili süzgeçlerin hepsine uyan soru yok.'}
          </p>
          <button type="button" onClick={clearAllFilters} className="ms-btn is-tonal">Filtreleri temizle</button>
        </div>
      ) : (
        <div className={`cx-list ${gorunum === 'kart' ? 'ck-list' : ''}`} key={`${gorunum}-${currentPage}-${filteredQuestions.length}-${sharedId || ''}`}>
          {sharedId && (
            <div className="ms-shared-band" role="status">
              <Share2 className="w-4 h-4 shrink-0" aria-hidden />
              <span className="min-w-0 flex-1">Paylaşılan soru gösteriliyor</span>
              <button type="button" onClick={showAllQuestions} className="ms-btn is-ghost is-sm">Tüm sorular <ChevronRight /></button>
            </div>
          )}
          {paginatedQuestions.map((q) => {
            const effectiveMode: 'redacted' | 'raw' | 'split' = cardViewOverrides[q.id] || viewMode;
            const userUid = getVoterId(currentUser);
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
              // check-solve ile düzeltilmiş kayıt güncel sürümle açılır; eskiSurum/phase14Original yalnız istenince gösterilir
              versionViewOverrides[q.id] || (isDenetleyici || (q as any).checkSolve?.status === 'onayli' ? 'denetleyici' : 'eski');

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
              ...((q.reports || []).length > 0
                ? [{ label: 'Bildirim geçmişi', icon: History, group: 'Diğer', hint: String((q.reports || []).length), onClick: () => setSelectedQuestionForReportHistory(q) }]
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

            const flagNodes: React.ReactNode[] = [];
            // Yalnız işe yarayan işaretler: açık bildirim, cevap belirsizliği, AI kuyruğu, Yeni/Eksik, çok sınavda çıkma.
            // (Çözülmüş bildirim, "Onaylı", "Onay bekliyor", kabul edilmiş "Anket" gibi bilgi taşımayan etiketler gösterilmez;
            //  bildirim geçmişi ⋯ menüsünde.)
            const openReports = (q.reports || []).filter((r: any) => r.status !== 'resolved' && r.status !== 'verified_correct').length;
            if (openReports > 0) {
              flagNodes.push(
                <button type="button" onClick={() => setSelectedQuestionForReportHistory(q)} className="cx-flag is-warn" title="Açık hata bildirimleri: geçmişi gör">
                  <Flag aria-hidden />{openReports} bildirim
                </button>
              );
            }
            if (pollMode && !acceptedPoll) flagNodes.push(<span className="cx-flag is-warn"><BarChart3 aria-hidden />{doubtful ? 'Cevabı belirsiz' : 'Cevapsız'}</span>);
            if (aiQueue[String(q.id)]) flagNodes.push(<span className="cx-flag is-ai"><Sparkles aria-hidden />{aiQueue[String(q.id)].status === 'yonetici_onayi' ? 'Onayda' : `Sırada ${aiQueue[String(q.id)].position}`}</span>);
            if (isAdminUser && (q as any).isQuarantined) flagNodes.push(<span className="cx-flag is-bad" title={((q as any).quarantineReasons || []).join(', ')}><ShieldAlert aria-hidden />Karantina</span>);
            if (isNewQuestion) flagNodes.push(<span className="cx-flag is-new">Yeni</span>);
            if (q.isAmbiguous) flagNodes.push(<span className="cx-flag is-warn">Eksik</span>);
            if (q.similarPastQuestions && q.similarPastQuestions.length > 0) flagNodes.push(<span className="cx-flag is-ai" title="Birden çok sınavda çıktı"><Layers aria-hidden />{q.similarPastQuestions.length + 1} sınav</span>);
            if (isAdminUser && p14Fixed && isPhase14Pending(q)) flagNodes.push(<span className="cx-flag is-ai"><Sparkles aria-hidden />Onay bekliyor</span>);
            if (isAdminUser) {
              // Kalite puanı rozeti (Q0–Q100) kullanıcı isteğiyle kaldırıldı (2026-10-11); kalite sıralaması süzgeçte duruyor
              if (!(q as any).isDonem3) flagNodes.push(<span className="cx-flag is-warn">{(q as any).committeeId || 'Diğer dönem'}</span>);
              if ((q as any).hidden || (q as any).data?.hidden) flagNodes.push(<span className="cx-flag is-warn">Gizli</span>);
              if (q.is_manual_entry || (q as any).manuel_ekleme) flagNodes.push(<span className="cx-flag is-new">Manuel</span>);
              if (isGeminiV3Question(q)) flagNodes.push(<span className="cx-flag is-ai">Gemini v3</span>);
            }

            const kazanimData = (q as any).notebooklm_verisi || q.notebooklm_verisi;
            const kurulId = (q as any).committeeUncertain ? (q as any).contentCommitteeId : ((q as any).contentCommitteeId || q.committeeId);
            const kurulChip = kurulId ? committeeShort(kurulId).replace(/^Kurul\s*/i, 'K') : null;
            const p14History = p14Fixed ? () => {
                  const o: any = (q as any).phase14Original || {};
                  const p14: any = (q as any).phase14 || {};
                  return (
                    <div className="ms-pop-in rounded-xl bg-field px-3 py-2.5 text-sm text-ink-2 flex flex-col gap-1.5">
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
                        <p className="m-0 text-sm"><span className="text-ink-3">Önceki kurul/ders/konu:</span> {[o.committeeId ? committeeShort(String(o.committeeId).replace(/^TIP\s*3(\d)0$/i, 'donem3-kurul$1')) : null, o.discipline, o.topic].filter(Boolean).join(' · ')}</p>
                      )}
                      {o.stem && <p className="m-0"><span className="text-ink-3">Önceki kök:</span> {o.stem}</p>}
                      {Array.isArray(o.options) && o.options.length > 0 && (
                        <ul className="m-0 pl-4 text-sm">
                          {o.options.map((op: any) => <li key={op.key}>{op.key}) {op.text}</li>)}
                        </ul>
                      )}
                      {o.explanation && (
                        <details className="text-sm"><summary className="cursor-pointer text-ink-3">Önceki açıklama</summary><p className="m-0 mt-1 whitespace-pre-wrap">{o.explanation}</p></details>
                      )}
                    </div>
                  );
                } : null;

            const specialView = isCompareView ? (
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
                    <span className="text-xs font-semibold text-ink-3 truncate">Ham metin · {q.sourceFile || 'PDF kaynağı'}</span>
                    <p className="m-0 text-md text-ink leading-relaxed whitespace-pre-wrap">{(q as any).rawQuestion?.stem || q.fragments?.[0]?.text || q.rawStem || q.topic}</p>
                    {(((q as any).rawQuestion?.options && (q as any).rawQuestion.options.length > 0) || (q.options && q.options.length > 0)) && (
                      <ol className="ms-opts">
                        {((q as any).rawQuestion?.options || q.options).map((opt: any) => {
                          const isClaimed = !hideAnswer && opt.key === (q.claimedAnswer || (q as any).rawQuestion?.claimedAnswer);
                          return (
                            <li key={opt.key} className={`ms-opt ${isClaimed ? 'is-claimed' : ''}`}>
                              <span className="ms-opt-key">{opt.key}</span>
                              <span>{opt.text}</span>
                              <span className="ms-opt-side">{isClaimed && <span className="text-xs font-semibold text-warn">İşaretlenen</span>}</span>
                            </li>
                          );
                        })}
                      </ol>
                    )}
                  </div>
                ) : pollMode ? (
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
                ) : undefined;

            const cmts: any[] = (q as any).comments || [];
            const lastCm = cmts.length ? cmts[cmts.length - 1] : null;
            const att = attempts[q.id];
            return (
              <CardView
                key={q.id}
                rich={gorunum === 'kart' ? {
                  number: q.questionNumber || '',
                  year: q.examYear,
                  status: isDenetleyici || (q as any).checkSolve?.status === 'onayli' || (q as any).answerStatus === 'dogrulandi'
                    ? { label: 'Onaylı', tone: 'ok' }
                    : p14Fixed && !isPhase14Pending(q) ? { label: 'Düzeltildi', tone: 'info' } : null,
                  saved: savedIds.has(q.id),
                  onToggleSave: () => toggleSave(q.id),
                  onInfo: () => setAboutQuestion(q),
                  onOpenNote: onOpenNote ? () => openNoteFor(q) : undefined,
                  attempt: att ? { picked: att.picked, correct: att.correct } : null,
                  onAnswer: (k, ok) => handleRichAnswer(q, k, ok),
                  voterUid: userUid,
                  topic: q.topic ? String(q.topic) : undefined,
                  commentPreview: lastCm ? { author: String(lastCm.author || 'Tıp öğrencisi'), text: censorProfanity(String(lastCm.text || '')), more: cmts.length - 1 } : null,
                } : undefined}
                id={String(q.id)}
                anchorId={`q-${q.id}`}
                className={disciplineClass(q.discipline)}
                kurul={kurulChip}
                kunye={[q.examYear, q.questionNumber ? `S${q.questionNumber}` : 'S?'].filter(Boolean).join(' · ')}
                ders={(q as any).committeeUncertain ? 'Kurul belirsiz' : disciplineLabel(q.discipline) || q.discipline || 'Tıp'}
                numberLabel={q.questionNumber ? `#${q.questionNumber}` : 'işlemleri'}
                flags={flagNodes}
                stem={<StemText text={stem} terms={terms} />}
                kazanim={kazanimData?.kazanim ? { baslik: ['Müfredat kazanımı', kazanimData.ders, kazanimData.konu].filter(Boolean).join(' · '), metin: String(kazanimData.kazanim) } : null}
                special={specialView}
                options={options as any[]}
                correctAnswer={correctAnswer ? String(correctAnswer) : undefined}
                terms={terms}
                quiz={{
                  on: quizMode,
                  picked,
                  onPick: (k) => setPicks((pp) => ({ ...pp, [q.id]: k })),
                  onReset: () => setPicks((pp) => { const x = { ...pp }; delete x[q.id]; return x; }),
                }}
                optionInfo={(key) => {
                  if (!p14Fixed) return null;
                  const opt: any = options.find((o: any) => String(o.key) === key);
                  const before = oldOpt(key);
                  if (!opt || !(opt.isAiGenerated || (before && norm(before) !== norm(opt.text)))) return null;
                  return {
                    title: `${key} şıkkı ${before ? 'düzeltildi' : 'eklendi'} (Faz 14)`,
                    before,
                    after: String(opt.text),
                    note: opt.isAiGenerated ? 'Kaynakta bu şık eksikti; yapay zekâ tamamladı (doğrulanmadı).' : undefined,
                  };
                }}
                onObject={(key, text) => setObjection({ question: q, option: { key, text } })}
                notes={<>
                  {!hideAnswer && !pollMode && (q as any).answerStatus === 'dogrulanmadi' && (
                      <p className="cx-note is-warn">Cevap doğrulanmadı: kaynaktaki işaret bir öğrencinin cevabıydı.</p>
                    )}
                    {!hideAnswer && (q as any).answerStatus === 'dogrulandi' && <p className="cx-note is-ok">Cevap ders slaytı kanıtıyla doğrulandı.</p>}

                    {/* Çoklu referans / alternatif sınav yılları bandı */}
                    {q.similarPastQuestions && q.similarPastQuestions.length > 0 && (
                      <div className="cx-alt mt-2.5 pt-2 border-t border-line/60 flex flex-wrap items-center gap-1.5 text-xs text-ink-3">
                        <span className="font-semibold text-ink-2 flex items-center gap-1">
                          <Layers className="w-3.5 h-3.5 text-accent" />
                          Diğer yıllardaki çıkmış örnekleri:
                        </span>
                        {q.similarPastQuestions.map((alt) => (
                          <span
                            key={alt.id}
                            className="inline-flex items-center px-2 py-0.5 rounded-md bg-field border border-line text-xs font-medium text-ink"
                            title={alt.olasi && alt.benzerlik ? `Olası aynı soru — metin benzerliği %${Math.round(alt.benzerlik * 100)} · Soru ID: ${alt.id}` : `Soru ID: ${alt.id}`}
                          >
                            {alt.label || `${alt.examYear} - Soru ${alt.questionNumber}`}
                            {alt.olasi && alt.benzerlik ? <span className="ml-1 font-normal text-ink-3 tabular-nums">· olası %{Math.round(alt.benzerlik * 100)}</span> : null}
                          </span>
                        ))}
                      </div>
                    )}
                </>}
                explanation={explanation ? String(explanation) : undefined}
                analysis={saEntries.map(([k, v]) => [k, typeof v === 'string' ? v : JSON.stringify(v)] as [string, string])}
                refs={refList}
                history={p14History ? p14History() : undefined}
                historyBadge={p14Fixed ? 'Faz 14' : undefined}
                copy={{ stem: q.reconstruction?.stem || q.fragments?.[0]?.text || q.topic, options: (q.reconstruction?.options || q.options || []) as any[] }}
                actions={actions}
                menuHighlight={reliableLearn ? { icon: GraduationCap, title: `Öğren slaytı var (slayt ${reliableLearn.slideNumber})` } : undefined}
                social={{
                  liked: isLiked,
                  disliked: isDisliked,
                  up: q.upvotes || 0,
                  down: q.downvotes || 0,
                  comments: commentsCount,
                  commentsOpen: expandedCommentsQuestionId === q.id,
                  onLike: () => handleToggleLike(q),
                  onDislike: () => handleToggleDislike(q),
                  onComments: () => setExpandedCommentsQuestionId(expandedCommentsQuestionId === q.id ? null : q.id),
                  onShare: () => handleShareQuestion(q),
                }}
                onReport={() => setReportingQuestion(q)}
                comments={<>
                {expandedCommentsQuestionId === q.id && (() => {
                  const all: any[] = (q as any).comments || [];
                  const byId = new Map(all.map((c) => [c.id, c]));
                  // Yanıtın kökü: zincirde en üstteki yorum (görselde tek girinti)
                  const rootOf = (c: any) => {
                    let cur = c;
                    const seen = new Set<string>();
                    while (cur?.parentId && byId.has(cur.parentId) && !seen.has(cur.id)) {
                      seen.add(cur.id);
                      cur = byId.get(cur.parentId);
                    }
                    return cur;
                  };
                  const roots = all.filter((c) => !c.parentId || !byId.has(c.parentId));
                  const repliesOf = (r: any) => all.filter((c) => c !== r && c.parentId && rootOf(c)?.id === r.id);
                    const renderOne = (c: any, isReply: boolean) => {
                    const canManage = canManageComment(c);
                    const isEditing = editingCommentId === c.id;
                    const parent = isReply && c.parentId ? byId.get(c.parentId) : null;
                    return (
                      <div key={c.id} id={`comm-${c.id}`} className={`cm ${isReply ? 'is-reply' : ''} ${replyTo?.id === c.id ? 'is-target' : ''}`}>
                        <span className="ui-avatar cm-av" style={{ '--av': isReply ? '24px' : '28px' } as React.CSSProperties}>
                          {String(c.author || 'T').trim().charAt(0).toLocaleUpperCase('tr-TR')}
                        </span>
                        <div className="cm-main">
                          <div className="cm-head">
                            <b>{c.author || 'Tıp öğrencisi'}</b>
                            {isAdminUser && (c.authorUid || c.authorEmail) && (
                              <a className="cm-to" href={`/manage/kisiler/${encodeURIComponent(c.authorUid ? `u:${c.authorUid}` : c.authorEmail)}`} target="_blank" rel="noreferrer" title="Yönetimde bu kişinin tüm izini aç">
                                kişi ↗
                              </a>
                            )}
                            {parent && rootOf(c)?.id !== parent.id && <span className="cm-to">↳ {parent.author || 'Tıp öğrencisi'}</span>}
                            <span className="cm-time">{c.timestamp || c.createdAt ? new Date(c.timestamp || c.createdAt).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' }) : ''}</span>
                            {c.isEdited && <span className="cm-time">· düzenlendi</span>}
                          </div>
                          {isEditing ? (
                            <div className="cm-edit">
                              <textarea value={editCommentText} onChange={(e) => setEditCommentText(e.target.value)} rows={2} className="ui-input" style={{ height: 'auto', paddingBlock: 8 }} aria-label="Yorumu düzenle" />
                              <div className="flex items-center justify-end gap-1.5">
                                <button type="button" onClick={() => setEditingCommentId(null)} className="ui-btn is-ghost is-sm">Vazgeç</button>
                                <button type="button" disabled={isUpdatingComment || !editCommentText.trim()} onClick={() => handleCommentEdit(q.id, c.id)} className={`ui-btn is-primary is-sm ${isUpdatingComment ? 'is-loading' : ''}`}>Kaydet</button>
                              </div>
                            </div>
                          ) : (
                            <p className="cm-text">{censorProfanity(c.text)}</p>
                          )}
                          {!isEditing && (
                            <div className="cm-acts">
                              <button type="button" onClick={() => setReplyTo({ qId: q.id, id: c.id, author: c.author || 'Tıp öğrencisi' })}>Yanıtla</button>
                              {canManage && (
                                <>
                                  <button type="button" onClick={() => { setEditingCommentId(c.id); setEditCommentText(c.text || ''); }}>Düzenle</button>
                                  <button type="button" className="is-bad" onClick={() => handleCommentDelete(q.id, c.id)}>Sil</button>
                                </>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  };
                  return (
                    <div id={`comments-${q.id}`} className="cm-wrap">
                      <div className="cm-list">
                        {roots.length > 0 ? (
                          roots.map((r) => {
                            const reps = repliesOf(r);
                            const open = openThreads[r.id] || reps.length <= 2 || reps.some((c) => c.id === focusCommentId);
                            return (
                              <div key={r.id} className="cm-thread">
                                {renderOne(r, false)}
                                {reps.length > 0 && (
                                  <div className="cm-replies">
                                    {(open ? reps : reps.slice(-1)).map((c) => renderOne(c, true))}
                                    {!open && (
                                      <button type="button" className="cm-more" onClick={() => setOpenThreads((o) => ({ ...o, [r.id]: true }))}>
                                        {reps.length - 1} yanıtı daha göster
                                      </button>
                                    )}
                                  </div>
                                )}
                              </div>
                            );
                          })
                        ) : (
                          <p className="cm-none">Henüz yorum yok. Bir ipucu ya da alternatif çözüm ekleyen ilk kişi ol.</p>
                        )}
                      </div>
                      {replyTo?.qId === q.id && (
                        <div className="cm-replying">
                          <span><b>{replyTo.author}</b> adlı kişiye yanıt</span>
                          <button type="button" onClick={() => setReplyTo(null)} aria-label="Yanıtı iptal et"><X /></button>
                        </div>
                      )}
                      <div className="cm-compose">
                        <textarea
                          value={newCommentText}
                          onChange={(e) => setNewCommentText(e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey || !e.shiftKey && window.matchMedia('(pointer: fine)').matches)) {
                              e.preventDefault();
                              handleCommentSubmit(q.id);
                            }
                          }}
                          rows={1}
                          placeholder={replyTo?.qId === q.id ? 'Yanıtını yaz…' : 'Yorum ya da ipucu yaz…'}
                          aria-label="Yorum"
                          className="cm-input"
                        />
                        <button type="button" onClick={() => handleCommentSubmit(q.id)} disabled={isSubmittingComment || !newCommentText.trim()} aria-label="Gönder" className={`ui-btn is-primary cm-send ${isSubmittingComment ? 'is-loading' : ''}`}>
                          <Send />
                        </button>
                      </div>
                    </div>
                  );
                })()}
                </>}
              />
            );
          })}

          {gorunum === 'kart' && !sharedId && (
            <LoadMoreSentinel remaining={filteredQuestions.length - paginatedQuestions.length} onMore={() => setRichLimit((l) => l + RICH_STEP)} shown={paginatedQuestions.length} total={filteredQuestions.length} />
          )}
          {gorunum === 'kompakt' && totalPages > 1 && !sharedId && (
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
      </V12Frame>

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
          <p className="m-0 text-sm text-ink-2 leading-relaxed">
            <b className="text-ink">Soru #{selectedLearnMatch.question.questionNumber}</b> bu slayta bağlı
            <span className="ms-tag is-accent ml-1.5 align-middle">{selectedLearnMatch.match.matchType === 'direct' ? 'Müfredat eşleşmesi' : 'Konu eşleşmesi'}</span>
          </p>
          <div className="flex flex-col gap-1">
            {selectedLearnMatch.match.badge && <span className="ms-tag self-start">{selectedLearnMatch.match.badge}</span>}
            <h3 className="m-0 text-md font-semibold text-ink">{selectedLearnMatch.match.slideTitle}</h3>
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
              <h4 className="m-0 text-sm font-semibold text-ink-3">Sınav için önemli noktalar</h4>
              <ul className="ms-stem-list">
                {selectedLearnMatch.match.spotPearls.map((pearl: any, i: number) => {
                  const isObj = pearl && typeof pearl === 'object';
                  return (
                    <li key={i} className="text-base text-ink-2 leading-relaxed">
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
              <h4 className="m-0 text-sm font-semibold text-ink-3">İlgili kartlar · {selectedLearnMatch.match.flashcards.length}</h4>
              <React.Suspense fallback={null}>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {selectedLearnMatch.match.flashcards.map((card) => (
                    <LazyFlashcardComponent key={card.id} card={card} />
                  ))}
                </div>
              </React.Suspense>
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
            <dl className="m-0 grid grid-cols-2 sm:grid-cols-4 gap-x-4 gap-y-2 text-sm">
              <div className="col-span-2 min-w-0">
                <dt className="text-xs text-ink-3">Dosya</dt>
                <dd className="m-0 font-medium text-ink truncate" title={rq.sourceFile || rq.sourceNote}>{rq.sourceFile || rq.sourceNote || 'Geçmiş kurul arşivi'}</dd>
              </div>
              <div>
                <dt className="text-xs text-ink-3">Yıl</dt>
                <dd className="m-0 font-medium text-ink">{rq.examYear || 'Arşiv'}</dd>
              </div>
              <div>
                <dt className="text-xs text-ink-3">Soru · sayfa</dt>
                <dd className="m-0 font-medium text-ink">#{rq.questionNumber}{rq.matchedSlidePage ? ` · s. ${rq.matchedSlidePage}` : ''}</dd>
              </div>
            </dl>
            <section className="flex flex-col gap-1.5">
              <h4 className="m-0 text-sm font-semibold text-ink-3">Ham soru metni</h4>
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
        const isLegacyView = (versionViewOverrides[q.id] || (isDenetleyiciQuestion(q) || q.checkSolve?.status === 'onayli' ? 'denetleyici' : 'eski')) === 'eski';
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
            provenanceNote={provenanceNoteFor(q)}
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
              if (res.report.id) saveMyReportId(res.report.id);
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
              if (res.report.id) saveMyReportId(res.report.id);
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

      {/* Hata Bildirimi ve Değişim Geçmişi Modalı (#000001, #000002) */}
      <ErrorReportHistoryModal
        isOpen={Boolean(selectedQuestionForReportHistory)}
        onClose={() => setSelectedQuestionForReportHistory(null)}
        question={selectedQuestionForReportHistory}
        currentUser={currentUser}
        onQuestionUpdated={(updatedQ) => {
          setSelectedQuestionForReportHistory(updatedQ);
          setQuestions((prev) => prev.map((q) => (q.id === updatedQ.id ? updatedQ : q)));
        }}
      />
    </div>
  );
};
