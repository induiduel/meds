import React, { useState, useEffect, useMemo, useCallback, Suspense } from 'react';
import { logActivity } from './services/activityLog';
import { getVoterId, toggledVote } from './utils/voterId';
import { AppRoute, parseLocation, writeLocation, pathFor, ROUTE_TITLES } from './router';
import { 
  Stethoscope, 
  Sparkles, 
  Plus, 
  RefreshCw, 
  AlertCircle, 
  BookOpen, 
  Layers, 
  Printer, 
  Brain, 
  HelpCircle,
  FolderPlus,
  Cloud,
  CheckCircle2,
  ExternalLink,
  ShieldCheck,
  Zap,
  FileText,
  BrainCircuit,
  Share2,
  ChevronRight
} from 'lucide-react';
import { Committee, QuestionItem, QuestionLectureMatch } from './types';
import { Header } from './components/Header';
import { MetricsBar } from './components/MetricsBar';
import { QuestionCard } from './components/QuestionCard';
import { QuickAddHero, committeeShortLabel, questionStemText } from './components/QuickAddHero';
import { MobileBottomNav } from './components/MobileBottomNav';
import { MusicPlayerProvider } from './components/music/MusicPlayerContext';
import { MiniMusicPlayer } from './components/music/MiniMusicPlayer';
import { AppRail } from './components/AppRail';
import { SideNav } from './components/shell/SideNav';
import { TopBar } from './components/shell/TopBar';
import { TabBar } from './components/shell/TabBar';
import { useUiVersion } from './utils/uiVersion';
import { ConfirmHost, confirmDialog } from './components/ui/ConfirmDialog';
import { PageHeader } from './components/ui/PageHeader';
import { LearnFab } from './components/learn/LearnFab';
import { SplashScreen, Onboarding } from './components/onboarding/Onboarding';
import { SectionLoader } from './components/ui/Animations';
import { ToastHost, toast } from './components/ui/Toast';
import { TooltipHost } from './components/ui/TooltipHost';
import { OfflineDatabaseModal } from './components/pwa/OfflineDatabaseModal';
import { PwaInstallWelcomeModal, PWA_WELCOME_STORAGE_KEY } from './components/pwa/PwaInstallWelcomeModal';
import { offlineDatabaseService } from './services/offlineDatabaseService';
import { pwaService } from './services/pwaService';
import { userNotificationService } from './services/userNotificationService';
import { buildDeepLinkUrl, executeDeepLinkFocus, initDeepLinkAutoScroll } from './services/universalRedirectService';
import { QuestionClusterAutomationModal } from './components/admin/QuestionClusterAutomationModal';

function wrapLazy<T extends { default: React.ComponentType<any> }>(
  promise: Promise<T>
): Promise<T> {
  return promise.catch((err) => {
    console.warn('[SafeLazy] Failed to load component:', err?.message || err);
    if (typeof window !== 'undefined' && navigator.onLine) {
      const msg = String(err?.message || err || '');
      if (
        msg.includes('dynamically imported module') ||
        msg.includes('Failed to fetch') ||
        msg.includes('default')
      ) {
        const lastReload = sessionStorage.getItem('medsoru_chunk_reload');
        if (!lastReload || Date.now() - Number(lastReload) > 8000) {
          sessionStorage.setItem('medsoru_chunk_reload', String(Date.now()));
          window.location.reload();
        }
      }
    }
    return {
      default: (() => (
        <div className="p-8 text-center text-ink-3">
          <p className="font-semibold text-ink">Bileşen yüklenirken bir sorun oluştu.</p>
          <p className="text-sm mt-1">Lütfen sayfayı yenileyiniz.</p>
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="mt-3 px-4 py-2 bg-accent text-white rounded-xl text-sm font-semibold hover:bg-accent-hover cursor-pointer"
          >
            Yenile
          </button>
        </div>
      )) as unknown as T['default']
    } as T;
  });
}

// Lazy-loaded Views (Split into separate on-demand chunks)
const PracticeMode = React.lazy(() => wrapLazy(import('./components/PracticeMode').then(m => ({ default: m.PracticeMode }))));
const StudyHub = React.lazy(() => wrapLazy(import('./components/study/StudyHub').then(m => ({ default: m.StudyHub }))));
const BookletView = React.lazy(() => wrapLazy(import('./components/BookletView').then(m => ({ default: m.BookletView }))));
const LeaderboardView = React.lazy(() => wrapLazy(import('./components/LeaderboardView').then(m => ({ default: m.LeaderboardView }))));
const StatsView = React.lazy(() => wrapLazy(import('./components/stats/StatsView').then(m => ({ default: m.StatsView }))));
const MusicView = React.lazy(() => wrapLazy(import('./components/MusicView').then(m => ({ default: m.MusicView }))));
const LectureNotesView = React.lazy(() => wrapLazy(import('./components/LectureNotesView').then(m => ({ default: m.LectureNotesView }))));
const PastExamsView = React.lazy(() => wrapLazy(import('./components/PastExamsView').then(m => ({ default: m.PastExamsView }))));
const QuestionMatrix = React.lazy(() => wrapLazy(import('./components/QuestionMatrix').then(m => ({ default: m.QuestionMatrix }))));
const LocalAiChatView = React.lazy(() => wrapLazy(import('./components/LocalAiChatView').then(m => ({ default: m.LocalAiChatView }))));
const DataCoreView = React.lazy(() => wrapLazy(import('./components/core/DataCoreView')));
const TestCikmisView = React.lazy(() => wrapLazy(import('./components/TestCikmisView').then(m => ({ default: m.TestCikmisView }))));
const TesterOzetView = React.lazy(() => wrapLazy(import('./components/TesterOzetView').then(m => ({ default: m.TesterOzetView }))));
const PracticeQuestionsView = React.lazy(() => wrapLazy(import('./components/PracticeQuestionsView')));
const KazanimlarView = React.lazy(() => wrapLazy(import('./components/KazanimlarView').then(m => ({ default: m.KazanimlarView }))));
const DiseasesView = React.lazy(() => wrapLazy(import('./components/diseases/DiseasesView').then(m => ({ default: m.DiseasesView }))));

// Lazy-loaded Modals (Only downloaded when opened)
const AdminPanelModal = React.lazy(() => wrapLazy(import('./components/AdminPanelModal').then(m => ({ default: m.AdminPanelModal }))));
const ExamPdfModal = React.lazy(() => wrapLazy(import('./components/ExamPdfModal').then(m => ({ default: m.ExamPdfModal }))));
const ContributeModal = React.lazy(() => wrapLazy(import('./components/ContributeModal').then(m => ({ default: m.ContributeModal }))));
const AddCommitteeModal = React.lazy(() => wrapLazy(import('./components/AddCommitteeModal').then(m => ({ default: m.AddCommitteeModal }))));
const GithubPagesGuideModal = React.lazy(() => wrapLazy(import('./components/GithubPagesGuideModal').then(m => ({ default: m.GithubPagesGuideModal }))));
const AuthErrorModal = React.lazy(() => wrapLazy(import('./components/AuthErrorModal').then(m => ({ default: m.AuthErrorModal }))));
const DriveSaveModal = React.lazy(() => wrapLazy(import('./components/DriveSaveModal').then(m => ({ default: m.DriveSaveModal }))));
const UserAuthModal = React.lazy(() => wrapLazy(import('./components/UserAuthModal').then(m => ({ default: m.UserAuthModal }))));
const ProfileSettingsView = React.lazy(() => wrapLazy(import('./components/settings/ProfileSettingsView').then(m => ({ default: m.ProfileSettingsView }))));
const UserProfileModal = React.lazy(() => wrapLazy(import('./components/UserProfileModal').then(m => ({ default: m.UserProfileModal }))));
const EditMyQuestionModal = React.lazy(() => wrapLazy(import('./components/EditMyQuestionModal').then(m => ({ default: m.EditMyQuestionModal }))));
const RevisionHistoryModal = React.lazy(() => wrapLazy(import('./components/RevisionHistoryModal').then(m => ({ default: m.RevisionHistoryModal }))));
const AdminPastExamImporterModal = React.lazy(() => wrapLazy(import('./components/AdminPastExamImporterModal').then(m => ({ default: m.AdminPastExamImporterModal }))));
const AiQuestionOptimizerModal = React.lazy(() => wrapLazy(import('./components/AiQuestionOptimizerModal').then(m => ({ default: m.AiQuestionOptimizerModal }))));
const NotebookLMSyncModal = React.lazy(() => wrapLazy(import('./components/NotebookLMSyncModal').then(m => ({ default: m.NotebookLMSyncModal }))));
const SubagentMonitorModal = React.lazy(() => wrapLazy(import('./components/SubagentMonitorModal').then(m => ({ default: m.SubagentMonitorModal }))));
const SystemDiagnosticsModal = React.lazy(() => wrapLazy(import('./components/SystemDiagnosticsModal').then(m => ({ default: m.SystemDiagnosticsModal }))));
const AiQuotaAlertModal = React.lazy(() => wrapLazy(import('./components/AiQuotaAlertModal').then(m => ({ default: m.AiQuotaAlertModal }))));
const LectureSummariesView = React.lazy(() => wrapLazy(import('./components/LectureSummariesView').then(m => ({ default: m.LectureSummariesView }))));
const TranscriptionsView = React.lazy(() => wrapLazy(import('./components/TranscriptionsView').then(m => ({ default: m.TranscriptionsView }))));
const FlashcardsView = React.lazy(() => wrapLazy(import('./components/flashcards/FlashcardsView').then(m => ({ default: m.FlashcardsView }))));
const SearchView = React.lazy(() => wrapLazy(import('./components/search/SearchView').then(m => ({ default: m.SearchView }))));
const InteractiveDeckView = React.lazy(() => wrapLazy(import('./components/learn/InteractiveDeckView').then(m => ({ default: m.InteractiveDeckView }))));
const MedicalEncyclopediaView = React.lazy(() => wrapLazy(import('./components/encyclopedia/MedicalEncyclopediaView').then(m => ({ default: m.MedicalEncyclopediaView }))));
const ManageConsole = React.lazy(() => wrapLazy(import('./components/manage/ManageConsole').then(m => ({ default: m.ManageConsole }))));

const ViewFallback = () => <SectionLoader />;
import { GlossaryProvider } from './components/learn/MedicalGlossaryPopover';
import { systemHealthMonitor } from './services/systemHealthMonitor';
import { ApiService } from './services/api';
import type { QuestionFocus } from './services/questionFocus';
import { multiDbManager } from './services/multiDbManager';
import { 
  initAuth, 
  googleSignIn, 
  logout, 
  isAdminUser, 
  ADMIN_EMAIL, 
  getAccessToken,
  getLocalAdminSession,
  setLocalAdminSession,
  clearLocalAdminSession,
  safeStorage,
  updateUserProfileData,
  AppUser
} from './services/auth';
import { getDefaultActiveCommitteeId, filterCurrent2026_2027Committees } from './services/firestoreDb';
import { 
  uploadBookletPdfToDrive, 
  evaluateAutoBackupThreshold, 
  ThresholdStatus,
  FOLDER_NAME
} from './services/drive';

// Top-level pages live at real paths (/ogren, /sorular, /siralama …); see router.ts
export type ValidAppTab = AppRoute;

export default function App() {
  const [committees, setCommittees] = useState<Committee[]>([]);
  // Open active upcoming committee automatically based on calendar date or saved choice
  const [selectedCommitteeId, setSelectedCommitteeId] = useState<string>(() => {
    try {
      const saved = localStorage.getItem('medsoru_last_committee_id');
      if (saved) return saved;
    } catch (e) {}
    return getDefaultActiveCommitteeId();
  });
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Page navigation: the address bar is the source of truth (back/forward, shareable links)
  // manage.nofrostlife.com.tr hostunda açılışta yönetim konsoluna yönlendir.
  const [initialRoute] = useState(() => {
    const parsed = parseLocation();
    try {
      if (typeof window !== 'undefined') {
        const p = new URLSearchParams(window.location.search);
        const qId = p.get('questionId');
        if (qId) {
          // Eski paylaşım bağlantıları: /cikmis yolundaysa çıkmış sorusu, aksi halde havuz sorusu
          // (havuzda yoksa aşağıdaki etki çıkmışa yönlendirir).
          const past = /^\/(meds\/)?cikmis/.test(window.location.pathname);
          return { route: (past ? 'past_exams' : 'questions') as ValidAppTab, param: qId };
        }
        if (/^manage\./i.test(window.location.hostname) && parsed.route === 'quick_add') {
          return { route: 'manage' as ValidAppTab, param: undefined as string | undefined };
        }
      }
    } catch {}
    return parsed;
  });
  const [activeTab, setActiveTabState] = useState<ValidAppTab>(initialRoute.route);
  // Havuz derin bağlantısı: /sorular/<soruId> — o soru listenin başında gösterilir ve odaklanır.
  const [poolFocusId, setPoolFocusId] = useState<string | undefined>(initialRoute.route === 'questions' ? initialRoute.param : undefined);
  // v8 kabuğu yeni tasarımda; klasik tasarım (v2) eski üst çubuk, ray ve alt menüyle kalır
  const { isV7: shellV8 } = useUiVersion();
  const setActiveTab = useCallback((tab: ValidAppTab) => {
    setActiveTabState(tab);
    writeLocation(tab);
    window.scrollTo({ top: 0 });
  }, []);

  // Filters & Search with reload persistence
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>(() => {
    try {
      return localStorage.getItem('medsoru_last_discipline') || 'Tümü';
    } catch (e) {
      return 'Tümü';
    }
  });
  const [selectedStatus, setSelectedStatus] = useState<string>(() => {
    try {
      return localStorage.getItem('medsoru_last_status') || 'Tümü';
    } catch (e) {
      return 'Tümü';
    }
  });
  const [searchQuery, setSearchQuery] = useState<string>('');
  // /cikmis/<id> paylaşılan soruyu PastExamsView kendi gösterir; kimlik arama kutusuna yazılmaz
  // (yazılınca "süzgeç değişti" sayılıp paylaşılan görünüm kapanıyor, adres /cikmis'e dönüyordu).
  const [pastExamsSearchQuery, setPastExamsSearchQuery] = useState<string>('');
  const [filterMyQuestionsOnly, setFilterMyQuestionsOnly] = useState<boolean>(false);

  // Modals state
  const [isContributeModalOpen, setIsContributeModalOpen] = useState(false);
  const [isNewCommitteeModalOpen, setIsNewCommitteeModalOpen] = useState(false);
  const [isGithubPagesModalOpen, setIsGithubPagesModalOpen] = useState(false);
  const [isAuthErrorModalOpen, setIsAuthErrorModalOpen] = useState(false);
  const [isDriveModalOpen, setIsDriveModalOpen] = useState(false);
  const [isPdfModalOpen, setIsPdfModalOpen] = useState(false);
  const [pdfSlideTarget, setPdfSlideTarget] = useState<{ deckId: string; slideNumber: number } | null>(null);
  const [isPastExamImporterOpen, setIsPastExamImporterOpen] = useState(false);
  const [isNotebookLMModalOpen, setIsNotebookLMModalOpen] = useState(false);
  const [isSubagentMonitorOpen, setIsSubagentMonitorOpen] = useState(false);
  const [isDiagnosticsOpen, setIsDiagnosticsOpen] = useState(false);
  const [isAiQuotaModalOpen, setIsAiQuotaModalOpen] = useState(false);
  const [isOfflineModalOpen, setIsOfflineModalOpen] = useState(false);
  const [isOnline, setIsOnline] = useState(typeof navigator !== 'undefined' ? navigator.onLine : true);
  const [contributeDefaultNumber, setContributeDefaultNumber] = useState<number | undefined>(undefined);

  useEffect(() => {
    return offlineDatabaseService.subscribe((s) => setIsOnline(s.isOnline));
  }, []);

  // User Auth & Profile Modals - İlk girişte kayıt/tanıtım ekranını zorunlu tut
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(() => {
    try {
      const existingAdmin = getLocalAdminSession();
      if (existingAdmin && existingAdmin.email?.toLowerCase() === ADMIN_EMAIL.toLowerCase()) {
        return false;
      }
      const savedUser = safeStorage.getItem('medsoru_user_registered');
      return !savedUser;
    } catch {
      return false;
    }
  });
  // İlk açılış: HTML splash ekranı (MeDSor nabız animasyonu) ilk andan itibaren görünür; React hazır olunca tek hamlede solar
  const [showSplash, setShowSplash] = useState(false);
  const [showOnboarding, setShowOnboarding] = useState(() => isAuthModalOpen);
  const [isPwaWelcomeOpen, setIsPwaWelcomeOpen] = useState(false);
  const [showClusterModal, setShowClusterModal] = useState(false);

  useEffect(() => {
    const el = document.getElementById('app-splash');
    if (el) {
      const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
      const t = setTimeout(() => {
        el.classList.add('is-leaving');
        setTimeout(() => {
          try { el.remove(); } catch {}
        }, 400);
      }, reduce ? 150 : 850);
      return () => clearTimeout(t);
    }
  }, []);

  // Site açılışında PWA & Çevrimdışı Veritabanı Kurulum Önerisi
  useEffect(() => {
    if (showSplash || showOnboarding) return;
    if (pwaService.isStandalone()) return;

    try {
      const dismissed = localStorage.getItem(PWA_WELCOME_STORAGE_KEY);
      if (dismissed === 'permanent') return;
      if (dismissed) {
        const time = Number(dismissed);
        if (!isNaN(time) && Date.now() - time < 2 * 24 * 60 * 60 * 1000) {
          return;
        }
      }
    } catch {}

    const timer = setTimeout(() => {
      setIsPwaWelcomeOpen(true);
    }, 1200);

    return () => clearTimeout(timer);
  }, [showSplash, showOnboarding]);
  const [justAddedId, setJustAddedId] = useState<string | null>(null);
  const [searchPageQuery, setSearchPageQuery] = useState<string>(() => (initialRoute.route === 'search' ? initialRoute.param || '' : ''));
  const [openSummaryId, setOpenSummaryId] = useState<string | undefined>(undefined);
  const [searchFocusId, setSearchFocusId] = useState<string | undefined>(undefined);
  const openSearchPage = useCallback((q: string, focusId?: string) => {
    setSearchPageQuery(q);
    setSearchFocusId(focusId);
    setActiveTabState('search');
    writeLocation('search', q || undefined);
    window.scrollTo({ top: 0 });
  }, []);
  const [authModalInitialMode, setAuthModalInitialMode] = useState<'login' | 'register' | 'admin'>('register');
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const [isEditQuestionModalOpen, setIsEditQuestionModalOpen] = useState(false);
  const [selectedQuestionToEdit, setSelectedQuestionToEdit] = useState<QuestionItem | null>(null);
  const [isHistoryModalOpen, setIsHistoryModalOpen] = useState(false);
  const [selectedQuestionForHistory, setSelectedQuestionForHistory] = useState<QuestionItem | null>(null);
  const [optimizeQuestion, setOptimizeQuestion] = useState<QuestionItem | null>(null);

  // Selected Learn deck and slide navigation state
  const [selectedLearnDeckId, setSelectedLearnDeckId] = useState<string | undefined>(
    initialRoute.route === 'learn' ? initialRoute.param : undefined
  );
  const [selectedLearnSlideNumber, setSelectedLearnSlideNumber] = useState<number | undefined>(() => {
    if (typeof window !== 'undefined') {
      const sp = new URLSearchParams(window.location.search);
      const s = sp.get('slide');
      if (s) {
        const n = parseInt(s, 10);
        if (!isNaN(n)) return n;
      }
    }
    return undefined;
  });
  // Selected Ornek Sorular lesson and kazanim state
  const [selectedOrnekLessonId, setSelectedOrnekLessonId] = useState<string | null>(null);
  const [selectedOrnekKazanimNo, setSelectedOrnekKazanimNo] = useState<number | null>(null);
  // Çıkmış sorudan Öğren'e gelindiyse soru ifadeleri ve doğru şık slaytta işaretlenir
  const [learnQuestionFocus, setLearnQuestionFocus] = useState<QuestionFocus | null>(null);
  const [selectedGlossaryTermId, setSelectedGlossaryTermId] = useState<string | undefined>(() => {
    if (initialRoute.route === 'glossary' && initialRoute.param) return initialRoute.param;
    if (typeof window !== 'undefined') {
      const p = new URLSearchParams(window.location.search);
      return p.get('id') || undefined;
    }
    return undefined;
  });

  // Celebration Toast
  const [congratsToast, setCongratsToast] = useState<string | null>(null);

  // Reconstructing state tracker by question ID
  const [reconstructingMap, setReconstructingMap] = useState<Record<string, boolean>>({});
  const [isGeneratingSlots, setIsGeneratingSlots] = useState(false);

  // Auth state - Default strictly to null unless authentic session exists
  const [currentUser, setCurrentUser] = useState<AppUser | null>(() => {
    try {
      // Clear any legacy unverified auto-admin session in visitor storage
      const legacyCleaned = safeStorage.getItem('medsoru_legacy_admin_cleaned_v2');
      if (!legacyCleaned) {
        safeStorage.setItem('medsoru_legacy_admin_cleaned_v2', 'true');
        clearLocalAdminSession();
        return null;
      }

      const existingAdmin = getLocalAdminSession();
      if (existingAdmin && existingAdmin.email?.toLowerCase() === ADMIN_EMAIL.toLowerCase()) {
        return existingAdmin;
      }
    } catch (e) {
      return null;
    }
    return null;
  });
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [isLoggingIn, setIsLoggingIn] = useState<boolean>(false);

  // Drive upload state
  const [isUploadingToDrive, setIsUploadingToDrive] = useState<boolean>(false);
  const [driveUploadSuccess, setDriveUploadSuccess] = useState<{
    fileId: string;
    fileName: string;
    webViewLink?: string;
  } | null>(null);
  const [hasAutoBackedUp, setHasAutoBackedUp] = useState<boolean>(false);

  // Derin bağlantı odağı: ilk açılışta, geri/ileri ve çapa değişiminde hedef öğeye kaydırıp vurgular.
  useEffect(() => initDeepLinkAutoScroll(), []);

  // Normalise legacy #tab links to their path once, then follow back / forward
  useEffect(() => {
    // Yol normalleştirilirken derin bağlantının sorgu (?opt, ?sec, ?highlight) ve çapası (#…) korunur.
    try {
      const next = pathFor(initialRoute.route, initialRoute.param);
      const sp = new URLSearchParams(window.location.search);
      sp.delete('questionId');
      const qs = sp.toString();
      if (window.location.pathname.replace(/^\/meds(?=\/|$)/, '') !== next || window.location.search.includes('questionId')) {
        window.history.replaceState({ route: initialRoute.route, param: initialRoute.param }, '', next + (qs ? `?${qs}` : '') + window.location.hash);
      }
    } catch {
      writeLocation(initialRoute.route, initialRoute.param, true);
    }
    const onPop = () => {
      const { route, param } = parseLocation();
      setActiveTabState(route);
      setPoolFocusId(route === 'questions' ? param : undefined);
      if (route === 'search') setSearchPageQuery(param || '');
      if (route === 'learn') {
        setSelectedLearnDeckId(param);
        const sp = new URLSearchParams(window.location.search);
        const s = sp.get('slide');
        setSelectedLearnSlideNumber(s ? parseInt(s, 10) : undefined);
      }
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    document.title = activeTab === 'quick_add' ? 'MeDSor · Soru ekle' : `${ROUTE_TITLES[activeTab]} · MeDSor`;
  }, [activeTab]);

  // Save selectedCommitteeId
  useEffect(() => {
    if (selectedCommitteeId) {
      try {
        localStorage.setItem('medsoru_last_committee_id', selectedCommitteeId);
      } catch (e) {}
    }
  }, [selectedCommitteeId]);

  // Save selectedDiscipline
  useEffect(() => {
    try {
      localStorage.setItem('medsoru_last_discipline', selectedDiscipline);
    } catch (e) {}
  }, [selectedDiscipline]);

  // Save selectedStatus
  useEffect(() => {
    try {
      localStorage.setItem('medsoru_last_status', selectedStatus);
    } catch (e) {}
  }, [selectedStatus]);

  // Scroll Position Restoration: Save scroll position on scroll
  useEffect(() => {
    const handleScroll = () => {
      try {
        sessionStorage.setItem('medsoru_scroll_pos', window.scrollY.toString());
      } catch (e) {}
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Restore scroll position after initial loading completes
  useEffect(() => {
    if (!loading) {
      try {
        const savedPos = sessionStorage.getItem('medsoru_scroll_pos');
        if (savedPos) {
          const y = parseInt(savedPos, 10);
          if (!isNaN(y) && y > 0) {
            const timer = setTimeout(() => {
              window.scrollTo({ top: y, behavior: 'instant' as ScrollBehavior });
            }, 100);
            return () => clearTimeout(timer);
          }
        }
      } catch (e) {}
    }
  }, [loading]);

  // Initialize Auth on mount
  useEffect(() => {
    try {
      const existingAdmin = getLocalAdminSession();
      if (existingAdmin && existingAdmin.email?.toLowerCase() === ADMIN_EMAIL.toLowerCase()) {
        setCurrentUser(existingAdmin);
      }
    } catch (e) {}

    const unsubscribe = initAuth(
      (user, token) => {
        setCurrentUser(user);
        setAccessToken(token);
      },
      () => {
        const local = getLocalAdminSession();
        if (local && local.email?.toLowerCase() === ADMIN_EMAIL.toLowerCase()) {
          setCurrentUser(local);
        } else {
          setCurrentUser(null);
          setAccessToken(null);
        }
      }
    );
    return () => unsubscribe();
  }, []);

  // Load committees on mount
  useEffect(() => {
    fetchCommittees();
  }, []);

  // Load questions when selected committee changes
  useEffect(() => {
    if (selectedCommitteeId) {
      fetchQuestions();
    }
  }, [selectedCommitteeId]);

  // Supabase Realtime Subscription: Sorulardaki yeni ekleme, oy ve güncellemeleri canlı dinle
  useEffect(() => {
    if (!selectedCommitteeId) return;

    const unsub = multiDbManager.subscribeToQuestions((payload) => {
      if ((payload.eventType === 'INSERT' || payload.eventType === 'UPDATE') && payload.new) {
        const raw = payload.new;
        const qData: QuestionItem = raw.data || {
          id: raw.id,
          committeeId: raw.committee_id,
          questionNumber: raw.question_number,
          discipline: raw.discipline,
          topic: raw.topic,
          status: raw.status,
          claimedAnswer: raw.claimed_answer,
          upvotes: raw.upvotes,
          tags: raw.tags || [],
          fragments: raw.fragments || [],
          options: raw.options || [],
          reconstruction: raw.reconstruction,
          createdAt: raw.created_at,
          updatedAt: raw.updated_at,
        };

        if (qData.committeeId === selectedCommitteeId) {
          setQuestions((prev) => {
            const exists = prev.some((item) => item.id === qData.id);
            if (exists) {
              return prev.map((item) => (item.id === qData.id ? { ...item, ...qData } : item));
            }
            return [...prev, qData].sort((a, b) => (a.questionNumber || 0) - (b.questionNumber || 0));
          });
        }
      } else if (payload.eventType === 'DELETE' && payload.old) {
        const deletedId = (payload.old as any)?.id;
        if (deletedId) {
          setQuestions((prev) => prev.filter((item) => item.id !== deletedId));
        }
      }
    });

    return () => {
      unsub();
    };
  }, [selectedCommitteeId]);

  const fetchCommittees = async () => {
    try {
      const data = await ApiService.getCommittees();
      const validCommittees = filterCurrent2026_2027Committees(data);
      if (validCommittees && validCommittees.length > 0) {
        setCommittees(validCommittees);
        if (!selectedCommitteeId || !validCommittees.some((c) => c.id === selectedCommitteeId)) {
          setSelectedCommitteeId(validCommittees[0].id);
        }
      }
    } catch (err: any) {
      console.error('Failed to load committees:', err);
      setError('Komite listesi yüklenemedi.');
      systemHealthMonitor.recordDatabaseError('firebase', err);
    }
  };

  const fetchQuestions = async () => {
    if (!selectedCommitteeId) return;
    setLoading(true);
    try {
      const data = await ApiService.getQuestions({
        committeeId: selectedCommitteeId,
      });
      setQuestions(data || []);
    } catch (err: any) {
      console.error('Failed to load questions:', err);
      setError('Sorular yüklenirken hata oluştu.');
      systemHealthMonitor.recordDatabaseError('firebase', err);
    } finally {
      setLoading(false);
    }
  };

  // Google Login
  const handleGoogleLogin = async () => {
    setIsLoggingIn(true);
    try {
      const result = await googleSignIn();
      if (result) {
        setCurrentUser(result.user);
        setAccessToken(result.accessToken);
      }
    } catch (err: any) {
      console.warn('Google login exception:', err);
      if (
        err.code === 'auth/popup-blocked' ||
        err.code === 'auth/cancelled-popup-request'
      ) {
        try {
          await googleSignIn({ preferRedirect: true });
          return;
        } catch (redirErr) {
          setIsAuthErrorModalOpen(true);
        }
      } else {
        setIsAuthErrorModalOpen(true);
      }
    } finally {
      setIsLoggingIn(false);
    }
  };

  // Google Logout
  const handleGoogleLogout = async () => {
    await logout();
    setCurrentUser(null);
    setAccessToken(null);
    setDriveUploadSuccess(null);
  };

  const currentCommittee = (committees || []).find((c) => c.id === selectedCommitteeId);
  const targetCount = currentCommittee?.targetCount || 100;
  const isAdmin = isAdminUser(currentUser);

  // Real-time health monitoring: only for admin (saves student network and battery)
  useEffect(() => {
    if (isAdmin) {
      systemHealthMonitor.startAutoMonitoring(120000);
      return () => {
        systemHealthMonitor.stopAutoMonitoring();
      };
    }
  }, [isAdmin]);

  // Evaluate the auto-backup threshold requested by the user:
  // "100 soru toplanıp soruların %80'i %90 doğruluğa ulaştığında otomatik olarak bir pdf oluşturup drive'da bir klasöre kayıt etmeni istiyorum."
  const thresholdStatus: ThresholdStatus = evaluateAutoBackupThreshold(questions, targetCount);

  // Auto-backup trigger when threshold is met and user is signed in with Drive access
  useEffect(() => {
    if (thresholdStatus.isThresholdMet && accessToken && !hasAutoBackedUp && !isUploadingToDrive) {
      // Trigger automatic Drive backup
      handleDriveUpload(true);
    }
  }, [thresholdStatus.isThresholdMet, accessToken, hasAutoBackedUp]);

  // Upload to Google Drive
  const handleDriveUpload = async (isAuto: boolean = false) => {
    if (!isAuto) {
      setIsDriveModalOpen(true);
      return;
    }

    let token = accessToken;
    if (!token) return;

    setIsUploadingToDrive(true);
    try {
      const result = await uploadBookletPdfToDrive({
        committee: currentCommittee,
        questions,
        accessToken: token,
      });

      setDriveUploadSuccess({
        fileId: result.fileId,
        fileName: result.fileName,
        webViewLink: result.webViewLink,
      });

      setHasAutoBackedUp(true);
    } catch (err: any) {
      console.error('Auto Drive upload error:', err);
    } finally {
      setIsUploadingToDrive(false);
    }
  };

  // Add memory fragment
  const handleAddFragment = async (
    questionId: string,
    text: string,
    author: string,
    type: 'stem' | 'clue' | 'option'
  ) => {
    try {
      const updatedQuestion = await ApiService.addFragment(questionId, text, author, type);
      logActivity('katki', 'Bir soruya hafıza parçası ekledin');
      if (updatedQuestion) {
        setQuestions((prev) =>
          prev.map((q) => (q.id === questionId ? updatedQuestion : q))
        );
      }
    } catch (err) {
      console.error('Add fragment error:', err);
    }
  };

  // Toggle Question Upvote (0ms Optimistic UI)
  const handleUpvoteQuestion = async (questionId: string) => {
    const currentUserId = getVoterId(currentUser);
    setQuestions((prev) =>
      prev.map((q) => {
        if (q.id === questionId) return toggledVote(q, currentUserId);
        return q;
      })
    );
    try {
      await ApiService.upvoteQuestion(questionId, currentUserId);
    } catch (err) {
      console.error('Upvote question error:', err);
    }
  };

  // Upvote memory fragment (0ms Optimistic UI)
  const handleUpvoteFragment = async (questionId: string, fragmentId: string) => {
    const currentUserId = getVoterId(currentUser);
    setQuestions((prev) =>
      prev.map((q) => {
        if (q.id === questionId) {
          return {
            ...q,
            fragments: q.fragments.map((f) => {
              if (f.id === fragmentId) {
                return toggledVote(f, currentUserId);
              }
              return f;
            }),
          };
        }
        return q;
      })
    );
    try {
      await ApiService.upvoteFragment(questionId, fragmentId, currentUserId);
    } catch (err) {
      console.error('Upvote fragment error:', err);
    }
  };

  // Add option
  const handleAddOption = async (
    questionId: string,
    key: 'A' | 'B' | 'C' | 'D' | 'E',
    text: string,
    suggestedBy: string
  ) => {
    try {
      const updatedQuestion = await ApiService.addOption(questionId, key, text, suggestedBy);
      logActivity('katki', `Bir soruya ${key} şıkkını ekledin`);
      if (updatedQuestion) {
        setQuestions((prev) =>
          prev.map((q) => (q.id === questionId ? updatedQuestion : q))
        );
      }
    } catch (err) {
      console.error('Add option error:', err);
    }
  };

  // Upvote option (0ms Optimistic UI)
  const handleUpvoteOption = async (
    questionId: string,
    key: 'A' | 'B' | 'C' | 'D' | 'E'
  ) => {
    const currentUserId = getVoterId(currentUser);
    setQuestions((prev) =>
      prev.map((q) => {
        if (q.id === questionId) {
          return {
            ...q,
            options: q.options.map((o) => {
              if (o.key === key) {
                return toggledVote(o, currentUserId);
              }
              return o;
            }),
          };
        }
        return q;
      })
    );
    try {
      await ApiService.upvoteOption(questionId, key, currentUserId);
    } catch (err) {
      console.error('Upvote option error:', err);
    }
  };

  // Set claimed answer
  const handleSetClaimedAnswer = async (
    questionId: string,
    answer: 'A' | 'B' | 'C' | 'D' | 'E'
  ) => {
    try {
      await ApiService.setClaimedAnswer(questionId, answer);
      setQuestions((prev) =>
        prev.map((q) => (q.id === questionId ? { ...q, claimedAnswer: answer } : q))
      );
    } catch (err) {
      console.error('Claim answer error:', err);
    }
  };

  // Delete question or draft
  const handleDeleteQuestion = async (targetQ: QuestionItem) => {
    const isDraft = targetQ.isUnassignedNumber || targetQ.questionNumber === 0;
    const label = isDraft ? `"${targetQ.topic || 'Bu taslağı'}"` : `Soru #${targetQ.questionNumber}'ı`;
    if (!(await confirmDialog({ title: isDraft ? 'Taslak silinsin mi?' : `Soru #${targetQ.questionNumber} silinsin mi?`, message: `${isDraft ? `“${targetQ.topic || 'Taslak'}” ` : ''}Veritabanından kalıcı olarak silinir. Bu işlem geri alınamaz.`, confirmLabel: 'Kalıcı sil', tone: 'danger' }))) {
      return;
    }
    try {
      await ApiService.deleteQuestion(targetQ.id, currentUser);
      setQuestions((prev) => prev.filter((item) => item.id !== targetQ.id));
      toast.success('Silindi', `${isDraft ? 'Taslak' : 'Soru'} buluttan ve yerel hafızadan kalıcı olarak silindi.`);
    } catch (err: any) {
      toast.error('Silinemedi', err.message || 'Silme işlemi başarısız oldu.');
    }
  };

  // Trigger Free AI Reconstruction via Queue
  const handleReconstructWithAi = async (questionId: string) => {
    setReconstructingMap((prev) => ({ ...prev, [questionId]: true }));
    const targetQ = questions.find((q) => q.id === questionId);
    const qNum = targetQ?.questionNumber ? `#${targetQ.questionNumber}` : 'Taslak soru';

    toast.info('AI Kuyruğuna Eklendi', `${qNum} ücretsiz yapay zekâ işlem sırasına alındı.`);

    userNotificationService.addNotification({
      type: 'ai_queued',
      title: `${qNum} AI Kuyruğuna Alındı`,
      message: `${qNum} için yapay zeka rekonstrüksiyon isteği ücretsiz sıraya eklendi.`,
      targetType: 'pool_question',
      targetId: questionId,
      deepLinkUrl: buildDeepLinkUrl({ type: 'pool_question', id: questionId, committeeId: targetQ?.committeeId }),
      userEmail: currentUser?.email || undefined,
    });

    try {
      const updatedQuestion = await ApiService.reconstructWithAi(questionId);
      if (updatedQuestion) {
        setQuestions((prev) =>
          prev.map((q) => (q.id === questionId ? updatedQuestion : q))
        );
        toast.success('AI Redaksiyonu Tamamlandı', `${qNum} başarıyla yeniden kuruldu ve müfredatla eşleştirildi.`);
        userNotificationService.addNotification({
          type: 'ai_reconstruction_complete',
          title: `✓ ${qNum} AI Redaksiyonu Tamamlandı`,
          message: `${qNum} yapay zekâ tarafından başarıyla yeniden kuruldu, şıklar ve açıklamalar oluşturuldu.`,
          targetType: 'pool_question',
          targetId: questionId,
          deepLinkUrl: buildDeepLinkUrl({ type: 'pool_question', id: questionId, committeeId: targetQ?.committeeId }),
          userEmail: currentUser?.email || undefined,
        });
      }
    } catch (err: any) {
      console.error('Reconstruct error:', err);
      toast.error('AI İşlem Hatası', 'Yapay zeka işlemi tamamlanamadı: ' + (err.message || ''));
    } finally {
      setReconstructingMap((prev) => ({ ...prev, [questionId]: false }));
    }
  };

  // Add question contribution from modal or quick add
  const handleAddQuestionContribution = async (data: {
    committeeId: string;
    questionNumber?: number;
    isUnknownNumber?: boolean;
    discipline: string;
    topic: string;
    fragmentText: string;
    author: string;
    authorUid?: string;
    authorStudentNumber?: string;
    claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E';
    options?: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[];
    targetQuestionId?: string;
    examYear?: string;
  }) => {
    try {
      const savedQuestion = await ApiService.addQuestionContribution({
        ...data,
        authorUid: currentUser?.uid || data.authorUid,
        authorStudentNumber: currentUser?.studentNumber || data.authorStudentNumber,
      });

      // Anında arayüze yansıt (0ms Optimistic UI)
      if (savedQuestion) {
        setJustAddedId(savedQuestion.id);
        setQuestions((prev) => {
          const idx = prev.findIndex((q) => q.id === savedQuestion.id);
          if (idx >= 0) {
            const next = [...prev];
            next[idx] = savedQuestion;
            return next;
          }
          if (savedQuestion.committeeId === (data.committeeId || selectedCommitteeId)) {
            return [...prev, savedQuestion].sort((a, b) => (a.questionNumber || 0) - (b.questionNumber || 0));
          }
          return prev;
        });
      }

      // Kullanıcı farklı bir kurula taslak eklediyse o kurula geçiş yap ki eklediğini hemen görsün
      if (data.committeeId && data.committeeId !== selectedCommitteeId) {
        setSelectedCommitteeId(data.committeeId);
      }

      // Send congratulations email in the background without blocking the UI
      if (currentUser && currentUser.email) {
        const comm = (committees || []).find((c) => c.id === data.committeeId);
        const commName = comm?.name || 'Kurul Sınavı';
        const alreadySent = (currentUser.congratsSentCommittees || []).includes(data.committeeId);

        if (!alreadySent) {
          ApiService.sendCongratulationsEmail(
            currentUser.email,
            currentUser.displayName || data.author,
            currentUser.studentNumber || undefined,
            commName,
            data.committeeId,
            { questionNumber: data.questionNumber, discipline: data.discipline }
          ).then(async () => {
            const updatedCommittees = [...(currentUser.congratsSentCommittees || []), data.committeeId];
            const updatedUser = await updateUserProfileData(currentUser, {
              congratsSentCommittees: updatedCommittees,
            });
            setCurrentUser(updatedUser);
          }).catch((err) => console.warn('Congrats email non-fatal error:', err));

          setCongratsToast(
            `🎉 Tebrikler! ${commName} için ilk soru katkınız kaydedildi. Teşekkür e-postası ${currentUser.email} adresinize iletildi!`
          );
          setTimeout(() => setCongratsToast(null), 8000);
        }
      }

      // Arka planda verileri tazele
      fetchQuestions().catch((e) => console.warn('Background fetchQuestions error', e));
    } catch (err: any) {
      console.error('Add question contribution error:', err);
      alert('Soru kaydedilirken hata oluştu: ' + (err.message || ''));
      throw err;
    }
  };

  // Add new committee
  const handleAddCommittee = async (data: {
    name: string;
    year: number;
    term: string;
    targetCount: number;
    description: string;
  }) => {
    try {
      const newCommittee = await ApiService.addCommittee(data);
      if (newCommittee) {
        setCommittees((prev) => [...prev, newCommittee]);
        setSelectedCommitteeId(newCommittee.id);
      }
    } catch (err) {
      console.error('Add committee error:', err);
    }
  };

  // Batch generate slots (Admin only)
  const handleGenerateSlots = async () => {
    if (!selectedCommitteeId) return;
    if (!isAdmin) {
      alert('100/150 soruluk yuva açma yetkisi yalnızca sistem yöneticisine (nofrostlife@gmail.com) aittir.');
      return;
    }
    setIsGeneratingSlots(true);
    try {
      const currentComm = (committees || []).find((c) => c.id === selectedCommitteeId);
      const count = currentComm?.targetCount || 100;
      await ApiService.generateSlots(currentUser?.email || '', selectedCommitteeId, count);
      await fetchQuestions();
    } catch (err: any) {
      console.error('Generate slots error:', err);
      alert(err.message || 'Yuva açılırken hata oluştu.');
    } finally {
      setIsGeneratingSlots(false);
    }
  };

  // Bir başka soruya uydu olarak eklenmiş / birleştirilmiş taslakların kimlikleri:
  // Bu sorular soru havuzunda bağımsız bir kart olarak değil, yalnızca birleştikleri ana sorunun katkılarında yer almalıdır.
  const allMergedSatelliteIds = useMemo(() => {
    const ids = new Set<string>();
    for (const q of questions) {
      if (q.mergedSatellites && q.mergedSatellites.length > 0) {
        for (const sat of q.mergedSatellites) {
          if (sat.id) ids.add(sat.id);
        }
      }
    }
    return ids;
  }, [questions]);

  // Sadece bağımsız (başka soruya yutulmamış) sorular
  const standaloneQuestions = useMemo(() => {
    if (allMergedSatelliteIds.size === 0) return questions;
    return questions.filter((q) => !allMergedSatelliteIds.has(q.id));
  }, [questions, allMergedSatelliteIds]);

  const completedQuestions = standaloneQuestions.filter(
    (q) => q.status === 'completed' && q.reconstruction
  );
  const gatheringQuestions = standaloneQuestions.filter(
    (q) => q.status === 'gathering' || (q.status !== 'completed' && q.fragments.length > 0)
  );
  const emptyQuestions = standaloneQuestions.filter(
    (q) => q.status === 'empty' && q.fragments.length === 0
  );

  const myQuestions = standaloneQuestions.filter(
    (q) =>
      currentUser &&
      (q.contributedByUid === currentUser.uid ||
        (currentUser.displayName && q.contributedByName === currentUser.displayName) ||
        q.fragments.some((f) => f.authorUid === currentUser.uid || (currentUser.displayName && f.author === currentUser.displayName)) ||
        q.options.some((o) => o.suggestedByUid === currentUser.uid || (currentUser.displayName && o.suggestedBy === currentUser.displayName)) ||
        (q.mergedSatellites && q.mergedSatellites.some((sat) =>
          sat.contributedByUid === currentUser.uid ||
          (currentUser.displayName && sat.contributedByName === currentUser.displayName) ||
          sat.fragments?.some((f) => f.authorUid === currentUser.uid || (currentUser.displayName && f.author === currentUser.displayName)) ||
          sat.options?.some((o) => o.suggestedByUid === currentUser.uid || (currentUser.displayName && o.suggestedBy === currentUser.displayName))
        )))
  );

  // Ultra-fast in-memory filtering: 0ms search & filter without network lag
  const filteredQuestions = useMemo(() => {
    let result = standaloneQuestions;
    if (selectedDiscipline && selectedDiscipline !== 'Tümü') {
      const discLower = selectedDiscipline.toLowerCase();
      result = result.filter((q) => q.discipline?.toLowerCase() === discLower);
    }
    if (selectedStatus && selectedStatus !== 'Tümü') {
      result = result.filter((q) => q.status === selectedStatus);
    }
    if (searchQuery && searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(
        (item) =>
          item.topic?.toLowerCase().includes(q) ||
          item.discipline?.toLowerCase().includes(q) ||
          item.reconstruction?.stem?.toLowerCase().includes(q) ||
          item.questionNumber?.toString() === q ||
          item.tags?.some((t) => t.toLowerCase().includes(q)) ||
          item.fragments?.some((f) => f.text.toLowerCase().includes(q)) ||
          item.options?.some((o) => o.text.toLowerCase().includes(q)) ||
          item.mergedSatellites?.some((sat) =>
            sat.topic?.toLowerCase().includes(q) ||
            sat.reconstruction?.stem?.toLowerCase().includes(q) ||
            sat.stem?.toLowerCase().includes(q) ||
            sat.fragments?.some((f) => f.text.toLowerCase().includes(q)) ||
            sat.options?.some((o) => o.text.toLowerCase().includes(q))
          )
      );
    }
    return result;
  }, [standaloneQuestions, selectedDiscipline, selectedStatus, searchQuery]);

  // Progressive rendering: Keep DOM lightweight with 30 cards at a time
  const [visibleCount, setVisibleCount] = useState<number>(30);

  useEffect(() => {
    setVisibleCount(30);
  }, [selectedCommitteeId, selectedDiscipline, selectedStatus, searchQuery, filterMyQuestionsOnly]);

  const poolQuestions = filterMyQuestionsOnly ? myQuestions : filteredQuestions;
  const poolFocusQuestion = poolFocusId ? questions.find((q) => String(q.id) === String(poolFocusId)) : undefined;
  const displayedQuestions = poolFocusQuestion ? [poolFocusQuestion] : poolQuestions.slice(0, visibleCount);
  // Havuz derin bağlantısı: soru yüklenince ona kaydır (?opt / ?sec çapası executeDeepLinkFocus ile);
  // havuzda yoksa (eski ?questionId bağlantısı çıkmış sorusuysa) Çıkmış'a geçilir.
  useEffect(() => {
    if (activeTab !== 'questions' || !poolFocusId || loading) return;
    if (!poolFocusQuestion) {
      if (questions.length > 0) {
        setPoolFocusId(undefined);
        setActiveTabState('past_exams');
        writeLocation('past_exams', poolFocusId, true);
      }
      return;
    }
    const t = window.setTimeout(() => {
      const el = document.querySelector(`[data-qid="${CSS.escape(String(poolFocusId))}"]`);
      el?.scrollIntoView({ block: 'start' });
      if (window.location.hash || window.location.search) executeDeepLinkFocus();
    }, 250);
    return () => window.clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab, poolFocusId, loading, Boolean(poolFocusQuestion), questions.length]);

  // Jump to a single question in the pool (home rows, practice "full explanation")
  const openQuestion = (q: QuestionItem) => {
    setSelectedDiscipline('Tümü');
    setSelectedStatus('Tümü');
    setFilterMyQuestionsOnly(false);
    setSearchQuery(q.isUnassignedNumber ? questionStemText(q).slice(0, 40) : String(q.questionNumber));
    setActiveTab('questions');
    window.scrollTo({ top: 0 });
  };

  const handleUpdateQuestionReference = async (questionId: string, reference: QuestionLectureMatch) => {
    try {
      const updated = await ApiService.updateQuestionLectureMatch(questionId, reference);
      setQuestions((prev) => prev.map((q) => (q.id === questionId ? updated : q)));
    } catch (e) {
      console.warn('Lecture reference update fallback', e);
      setQuestions((prev) =>
        prev.map((q) => (q.id === questionId ? { ...q, lectureReference: reference } : q))
      );
    }
  };

  const handleAuthSuccess = (user: AppUser, token?: string | null) => {
    setCurrentUser(user);
    if (token) setAccessToken(token);
    safeStorage.setItem('medsoru_user_registered', 'true');
    setIsAuthModalOpen(false);
    setShowOnboarding(false);
    if (isAdminUser(user)) {
      setActiveTab('admin');
    }
  };

  // Yeni soru eklenince: listede soruya (yoksa sayfa başına) kaydır ve kısa vurgula
  useEffect(() => {
    if (!justAddedId) return;
    const t = window.setTimeout(() => {
      const el = document.querySelector<HTMLElement>(`[data-qid="${CSS.escape(justAddedId)}"]`);
      const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
      if (el) {
        el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
        el.classList.add('ms-just-added');
        window.setTimeout(() => el.classList.remove('ms-just-added'), 1900);
      } else {
        window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      }
      setJustAddedId(null);
    }, 120);
    return () => window.clearTimeout(t);
  }, [justAddedId, questions]);

  return (
    <GlossaryProvider>
    <MusicPlayerProvider>
      {showSplash && <SplashScreen onDone={() => setShowSplash(false)} />}
      {showOnboarding && !currentUser && <Onboarding onAuthSuccess={handleAuthSuccess} />}
      <div className="min-h-dvh bg-canvas text-ink flex flex-col font-sans antialiased">
      <ToastHost />
      <ConfirmHost />
      <TooltipHost />
      {activeTab !== 'music' && activeTab !== 'practice' && activeTab !== 'manage' && (
        <MiniMusicPlayer onOpen={() => setActiveTab('music')} />
      )}
      {activeTab === 'practice' ? (
        <Suspense fallback={<ViewFallback />}>
          <PracticeMode
            questions={questions}
            title={currentCommittee ? `${committeeShortLabel(currentCommittee).charAt(0)}${committeeShortLabel(currentCommittee).slice(1).toLocaleLowerCase('tr-TR')} · Test çöz` : 'Test çöz'}
            subtitle={currentCommittee?.name.split(':').slice(1).join(':').trim() || currentCommittee?.name}
            onExit={() => setActiveTab('study')}
            onOpenQuestion={openQuestion}
            onOpenContributeModal={() => {
              setContributeDefaultNumber(undefined);
              setIsContributeModalOpen(true);
            }}
          />
        </Suspense>
      ) : activeTab === 'manage' || activeTab === 'admin' ? (
        isAdmin ? (
          <Suspense fallback={<ViewFallback />}>
            <ManageConsole
              key={activeTab}
              entry={activeTab === 'admin' ? 'admin' : 'manage'}
              initialSlug={parseLocation().param}
              adminEmail={ADMIN_EMAIL}
              committees={committees}
              questions={questions}
              selectedCommitteeId={selectedCommitteeId}
              onSelectCommittee={(id) => setSelectedCommitteeId(id)}
              onRefreshData={fetchQuestions}
              onExit={() => setActiveTab('quick_add')}
              fullscreen
            />
          </Suspense>
        ) : (
          <div className="min-h-dvh w-full bg-canvas flex items-center justify-center p-4">
            <div className="max-w-[440px] w-full bg-white border border-line rounded-2xl p-6 sm:p-8 flex flex-col items-center text-center gap-3">
              <span className="w-12 h-12 rounded-2xl bg-ink text-white flex items-center justify-center">
                <ShieldCheck className="w-6 h-6" />
              </span>
              <h1 className="m-0 font-display font-bold text-2xl tracking-[-0.02em]">Yönetim Konsolu</h1>
              <p className="m-0 text-md text-ink-2">Bu konsol yalnızca yöneticilere açık. Devam etmek için yönetici hesabıyla giriş yap.</p>
              <div className="flex gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setActiveTab('quick_add')}
                  className="h-11 px-4 rounded-xl border border-line-2 bg-white font-semibold text-md cursor-pointer"
                >
                  Ana sayfa
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setAuthModalInitialMode('admin');
                    setIsAuthModalOpen(true);
                  }}
                  className="h-11 px-5 rounded-xl bg-accent hover:bg-accent-hover text-white font-semibold text-md cursor-pointer"
                >
                  Yönetici girişi
                </button>
              </div>
            </div>
          </div>
        )
      ) : (
      <>
      {/* v3 shell: icon rail on tablet/desktop, bottom tabs on phones */}
      {shellV8 ? (
        <SideNav active={activeTab} onGo={setActiveTab} isAdmin={isAdmin} user={currentUser} />
      ) : (
        <AppRail activeTab={activeTab} setActiveTab={setActiveTab} isAdmin={isAdmin} />
      )}
      <div className={shellV8 ? 'sh-app' : 'ms-shell md:pl-[76px] lg:pl-[208px] flex-1 flex flex-col min-w-0'}>
      {shellV8 ? (
        <TopBar
          active={activeTab}
          onGo={setActiveTab}
          user={currentUser}
          isAdmin={isAdmin}
          searchQuery={searchQuery}
          onSearch={(q, focusId) => openSearchPage(q, focusId)}
          onOpenOffline={() => setIsOfflineModalOpen(true)}
          actions={{
            onSettings: () => setActiveTab('settings'),
            onContribute: () => {
              setContributeDefaultNumber(undefined);
              setIsContributeModalOpen(true);
            },
            onPdf: () => setIsPdfModalOpen(true),
            onOffline: () => setIsOfflineModalOpen(true),
            onLogin: () => {
              setAuthModalInitialMode('login');
              setIsAuthModalOpen(true);
            },
            onAdminLogin: () => {
              setAuthModalInitialMode('admin');
              setIsAuthModalOpen(true);
            },
            onLogout: handleGoogleLogout,
            isLoggingIn,
            admin: isAdmin
              ? {
                  onConsole: () => setActiveTab('manage'),
                  onFaz14: () => setActiveTab('test_cikmis'),
                  onDiagnostics: () => setIsDiagnosticsOpen(true),
                  onPastExam: () => setIsPastExamImporterOpen(true),
                  onNotebookLM: () => setIsNotebookLMModalOpen(true),
                  onDrive: () => handleDriveUpload(false),
                  driveBusy: isUploadingToDrive,
                  driveFresh: !!driveUploadSuccess?.webViewLink,
                  onNewCommittee: () => setIsNewCommitteeModalOpen(true),
                  onSubagents: () => setIsSubagentMonitorOpen(true),
                }
              : undefined,
          }}
        />
      ) : (
      <Header
        searchQuery={searchQuery}
        onSearch={(q, focusId) => openSearchPage(q, focusId)}
        committees={committees}
        selectedCommitteeId={selectedCommitteeId}
        onSelectCommittee={(id) => setSelectedCommitteeId(id)}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenContributeModal={() => {
          setContributeDefaultNumber(undefined);
          setIsContributeModalOpen(true);
        }}
        onOpenNewCommitteeModal={isAdmin ? () => setIsNewCommitteeModalOpen(true) : () => {}}
        onOpenAdminPanel={isAdmin ? () => setActiveTab('admin') : () => {}}
        onOpenPastExamModal={isAdmin ? () => setIsPastExamImporterOpen(true) : undefined}
        onOpenNotebookLMModal={isAdmin ? () => setIsNotebookLMModalOpen(true) : undefined}
        onOpenSubagentMonitor={isAdmin ? () => setIsSubagentMonitorOpen(true) : undefined}
        onOpenProfileModal={() => setActiveTab('settings')}
        onOpenAuthModal={(m) => {
          setAuthModalInitialMode(m);
          setIsAuthModalOpen(true);
        }}
        completedCount={completedQuestions.length}
        totalCount={questions.length}
        targetCount={targetCount}
        currentUser={currentUser}
        isAdmin={isAdmin}
        onLogin={() => {
          setAuthModalInitialMode('login');
          setIsAuthModalOpen(true);
        }}
        onLogout={handleGoogleLogout}
        isLoggingIn={isLoggingIn}
        onUploadToDrive={() => handleDriveUpload(false)}
        isUploadingToDrive={isUploadingToDrive}
        driveLastUploadedLink={driveUploadSuccess?.webViewLink || null}
        onOpenPdfModal={() => setIsPdfModalOpen(true)}
        onOpenDiagnostics={isAdmin ? () => setIsDiagnosticsOpen(true) : undefined}
        onOpenOfflineModal={() => setIsOfflineModalOpen(true)}
      />
      )}

      {!isOnline && shellV8 && (
        <div className="sh-offline" role="status">
          <i aria-hidden="true" />
          <span><b>Çevrimdışısın.</b> Sorular ve desteler cihazdaki kopyadan açılıyor.</span>
          <button type="button" onClick={() => setIsOfflineModalOpen(true)}>Veritabanı</button>
        </div>
      )}
      {!isOnline && !shellV8 && (
        <div className="bg-warn/15 border-b border-warn/30 px-4 py-2.5 text-xs flex items-center justify-between text-warn dark:text-amber-200">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-warn animate-pulse shrink-0" />
            <span><strong>Çevrimdışı Mod:</strong> İnternet bağlantısı yok. Sorular ve desteler cihazınızın yerel belleğinden sunuluyor.</span>
          </div>
          <button
            type="button"
            onClick={() => setIsOfflineModalOpen(true)}
            className="underline font-semibold hover:text-warn dark:hover:text-amber-100 cursor-pointer shrink-0 ml-2"
          >
            Veritabanı
          </button>
        </div>
      )}

      {/* Main Container */}
      <main key={activeTab} className={shellV8 ? `sh-main ms-view-enter ${activeTab === 'ai_chat' ? 'ms-chat-main' : ''}` : `ms-view-enter min-w-0 flex-1 max-w-[1180px] w-full mx-auto px-4 sm:px-5 lg:px-6 pt-3 sm:pt-4 flex flex-col gap-3 ${activeTab === 'ai_chat' ? 'ms-chat-main pb-[84px] md:pb-4' : 'pb-24 md:pb-8'}`}>

        {/* Drive Upload Notification Banner if successful */}
        {driveUploadSuccess && (
          <div role="status" className="bg-ok-soft rounded-xl px-4 py-3 sm:px-5 sm:py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-5 h-5 text-ok shrink-0 mt-0.5" />
              <div>
                <p className="m-0 font-semibold text-md text-ok">PDF Google Drive'a kaydedildi</p>
                <p className="m-0 text-base text-ink">
                  {driveUploadSuccess.fileName} · “{FOLDER_NAME}” klasörü
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 shrink-0">
              {driveUploadSuccess.webViewLink && (
                <a
                  href={driveUploadSuccess.webViewLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="h-10 px-4 rounded-[10px] bg-white border border-line-2 text-ink font-semibold text-base inline-flex items-center gap-2"
                >
                  Drive'da aç
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
              <button
                type="button"
                onClick={() => setDriveUploadSuccess(null)}
                className="h-10 px-3 rounded-[10px] text-ink-2 font-semibold text-base cursor-pointer"
              >
                Kapat
              </button>
            </div>
          </div>
        )}

        {/* Celebration / Thank You Notification */}
        {congratsToast && (
          <div role="status" className="bg-ink text-white rounded-xl px-4 py-3 sm:px-5 sm:py-4 flex items-center justify-between gap-3">
            <div className="flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-warn shrink-0 mt-0.5" />
              <div>
                <p className="m-0 font-semibold text-md">Teşekkürler!</p>
                <p className="m-0 text-base text-accent">{congratsToast}</p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setCongratsToast(null)}
              className="h-10 px-4 rounded-[10px] bg-white/10 hover:bg-white/20 font-semibold text-base cursor-pointer shrink-0"
            >
              Tamam
            </button>
          </div>
        )}

        {/* TAB 0: Home — quick add, pool status, committees */}
        {activeTab === 'quick_add' && (
          <QuickAddHero
            committee={currentCommittee}
            committees={committees}
            onSelectCommittee={(id) => setSelectedCommitteeId(id)}
            onSubmitContribution={handleAddQuestionContribution}
            unassignedCount={questions.filter((q) => q.isUnassignedNumber).length}
            totalQuestionsCount={questions.length}
            questions={questions}
            onOpenQuestion={openQuestion}
            onNavigateTab={(tab) => setActiveTab(tab)}
            isAdmin={isAdmin}
            currentUser={currentUser}
            onOpenAdminPanel={() => setActiveTab('admin')}
            onQuestionsUpdated={fetchQuestions}
          />
        )}

        {/* TAB: Learn / İnteraktif Ses & Slayt Hub'ı */}
        {activeTab === 'learn' && (
          <Suspense fallback={<ViewFallback />}>
            <LearnFab
              onOpenGlossary={() => setActiveTab('glossary')}
              onOpenPdf={() => { setPdfSlideTarget(null); setIsPdfModalOpen(true); }}
            >
            <InteractiveDeckView
              isAdmin={isAdmin}
              initialDeckId={selectedLearnDeckId}
              initialSlideNumber={selectedLearnSlideNumber}
              questionFocus={learnQuestionFocus}
              onClearQuestionFocus={() => setLearnQuestionFocus(null)}
              onDeckChange={(id) => {
                setSelectedLearnDeckId(id ?? undefined);
                if (id === null) {
                  setSelectedLearnSlideNumber(undefined);
                  setLearnQuestionFocus(null);
                }
                writeLocation('learn', id ?? undefined);
              }}
              onOpenPdfModal={(target) => {
                setPdfSlideTarget(target ?? null);
                setIsPdfModalOpen(true);
              }}
              onSelectCommittee={(id) => setSelectedCommitteeId(id)}
            />
            </LearnFab>
          </Suspense>
        )}

        {activeTab === 'search' && (
          <Suspense fallback={<ViewFallback />}>
            <SearchView
              initialQuery={searchPageQuery}
              focusId={searchFocusId}
              committeeId={selectedCommitteeId}
              onQueryChange={(q) => { setSearchPageQuery(q); writeLocation('search', q || undefined, true); }}
              onOpenSource={(hit) => {
                if (hit.documentType === 'past_question' || hit.documentType === 'deepseek_contribution') {
                  setPastExamsSearchQuery(hit.documentId);
                  setActiveTab('past_exams');
                } else if (hit.documentType === 'summary') {
                  setOpenSummaryId(hit.documentId);
                  setActiveTab('summaries');
                } else if (hit.documentType === 'transcript') {
                  setActiveTab('transcripts');
                } else {
                  // Havuz sorusu ve öğrenci katkısı chunk'larında documentId soru kimliğidir
                  const target = questions.find((q) => q.id === hit.documentId);
                  if (target) openQuestion(target);
                  else { setSearchQuery(''); setActiveTab('questions'); }
                }
              }}
            />
          </Suspense>
        )}

        {/* TAB: Glossary & Encyclopedia / Tıbbi Sözlük & Ansiklopedi */}
        {activeTab === 'glossary' && (
          <Suspense fallback={<ViewFallback />}>
            <MedicalEncyclopediaView
              initialTermId={selectedGlossaryTermId}
              onNavigateToDeck={(deckId) => {
                setSelectedLearnDeckId(deckId);
                setActiveTab('learn');
              }}
            />
          </Suspense>
        )}

        {/* TAB: Diseases Atlas / Tıbbi Hastalıklar & Klinik Atlas */}
        {activeTab === 'diseases' && (
          <Suspense fallback={<ViewFallback />}>
            <DiseasesView
              currentUser={currentUser}
              onOpenReportModal={(t) => {
                toast.info('Hata Bildirimi Alındı', `${t.title} için bildiriminiz inceleme sırasına eklendi.`);
              }}
            />
          </Suspense>
        )}

        {/* TAB 1: Questions List */}
        {activeTab === 'questions' && (
          <div className="flex flex-col gap-3 sm:gap-5">
            <PageHeader
              eyebrow="Kolektif arşiv"
              title="Soru havuzu"
              description="Herkesin hatırladığı parçalar burada birleşir; kaynaklarla tamamlanan sorular doğrulanır."
              stats={loading ? undefined : [{ label: 'soru', value: poolQuestions.length.toLocaleString('tr-TR') }]}
              actions={
                <>
                  <label className="sr-only" htmlFor="pool-committee">Kurul</label>
                  <select
                    id="pool-committee"
                    value={selectedCommitteeId}
                    onChange={(e) => setSelectedCommitteeId(e.target.value)}
                    className="ms-select h-10 font-semibold w-full sm:w-auto sm:max-w-[360px] truncate"
                  >
                    {committees.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                  <button
                    type="button"
                    onClick={() => setShowClusterModal(true)}
                    className="inline-flex h-10 px-3.5 rounded-[10px] bg-teal-500/10 hover:bg-teal-500/20 text-teal-400 border border-teal-500/30 font-semibold text-sm items-center gap-2 cursor-pointer shadow-sm transition-all"
                    title="Yapay zeka soru eşleme ve birleştirilmiş öneri taslakları"
                  >
                    <BrainCircuit className="w-4 h-4 text-teal-400" />
                    <span>Öneri Taslak Havuzu</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setContributeDefaultNumber(undefined);
                      setIsContributeModalOpen(true);
                    }}
                    className="hidden sm:inline-flex h-10 px-4 rounded-[10px] bg-accent hover:bg-accent-hover text-white font-semibold text-base items-center gap-2 cursor-pointer shadow-sm"
                  >
                    <Plus className="w-4 h-4" strokeWidth={2.2} />
                    Soru ekle
                  </button>
                </>
              }
            >
              {searchQuery && (
                <div className="flex flex-wrap items-center gap-2 text-base text-ink-2">
                  <span>Arama:</span>
                  <span className="text-ink font-semibold">“{searchQuery}”</span>
                  <button type="button" onClick={() => setSearchQuery('')} className="h-8 px-2.5 rounded-lg text-accent font-semibold cursor-pointer hover:bg-accent-soft">
                    Aramayı temizle
                  </button>
                </div>
              )}
            </PageHeader>

            {/* Filter and Stats Bar */}
            <MetricsBar
              totalTarget={targetCount}
              totalGathered={questions.filter((q) => q.fragments.length > 0).length}
              completedCount={completedQuestions.length}
              gatheringCount={gatheringQuestions.length}
              emptyCount={emptyQuestions.length}
              selectedDiscipline={selectedDiscipline}
              onSelectDiscipline={setSelectedDiscipline}
              selectedStatus={selectedStatus}
              onSelectStatus={setSelectedStatus}
              searchQuery={searchQuery}
              onSearchChange={setSearchQuery}
              onGenerateSlots={handleGenerateSlots}
              isGeneratingSlots={isGeneratingSlots}
              isAdmin={isAdmin}
              myQuestionsCount={myQuestions.length}
              filterMyQuestionsOnly={filterMyQuestionsOnly}
              onToggleMyQuestionsOnly={() => setFilterMyQuestionsOnly(!filterMyQuestionsOnly)}
            />

            {/* Questions Stream */}
            {loading ? (
              <div className="flex flex-col gap-3" aria-busy="true" aria-label="Soru havuzu yükleniyor">
                {[0, 1, 2].map((i) => (
                  <div key={i} className="ui-card flex flex-col gap-2.5">
                    <div className="ui-skel" style={{ width: '32%', height: 10 }} />
                    <div className="ui-skel" style={{ height: 14 }} />
                    <div className="ui-skel" style={{ width: '78%', height: 14 }} />
                    <div className="ui-skel" style={{ width: '54%', height: 10, marginTop: 6 }} />
                  </div>
                ))}
              </div>
            ) : poolQuestions.length === 0 ? (
              <div className="ui-card flex flex-col items-center text-center gap-3" style={{ paddingBlock: 40 }}>
                <span className="ui-ico is-soft" style={{ width: 44, height: 44, borderRadius: 12 }}><Plus className="w-5 h-5" /></span>
                <div className="flex flex-col gap-1">
                  <h3 className="m-0 font-display text-xl font-bold tracking-[-0.02em]">
                    {filterMyQuestionsOnly ? 'Henüz katkıda bulunduğun soru yok' : 'Bu süzgeçlere uyan soru yok'}
                  </h3>
                  <p className="m-0 text-base text-ink-2 max-w-[420px]">
                    {filterMyQuestionsOnly
                      ? 'Aklında kalan tek bir kelime bile işe yarar; parçayı ekle, kaynaklarla tamamlansın.'
                      : 'Branşı ya da durumu değiştir, veya aramayı kısalt.'}
                  </p>
                </div>
                <div className="flex flex-wrap items-center justify-center gap-2">
                  {filterMyQuestionsOnly && (
                    <button type="button" onClick={() => setFilterMyQuestionsOnly(false)} className="ui-btn">
                      Tüm soruları göster
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={() => {
                      setContributeDefaultNumber(undefined);
                      setIsContributeModalOpen(true);
                    }}
                    className="ui-btn is-primary"
                  >
                    Soru parçası ekle
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex flex-col gap-3 sm:gap-5">
                {poolFocusQuestion && (
                  <div className="ms-shared-band" role="status">
                    <Share2 className="w-4 h-4 shrink-0" aria-hidden />
                    <span className="min-w-0 flex-1">Paylaşılan soru gösteriliyor</span>
                    <button type="button" onClick={() => { setPoolFocusId(undefined); writeLocation('questions'); }} className="ms-btn is-ghost is-sm">Tüm sorular <ChevronRight className="w-4 h-4" /></button>
                  </div>
                )}
                {displayedQuestions.map((q) => (
                  <div key={q.id} data-qid={q.id} className="scroll-mt-20 min-w-0">
                  <QuestionCard
                    key={q.id}
                    question={q}
                    currentUser={currentUser}
                    isAdmin={isAdmin}
                    onEditQuestion={(targetQ) => {
                      setSelectedQuestionToEdit(targetQ);
                      setIsEditQuestionModalOpen(true);
                    }}
                    onDeleteQuestion={handleDeleteQuestion}
                    onOpenHistory={(targetQ) => {
                      setSelectedQuestionForHistory(targetQ);
                      setIsHistoryModalOpen(true);
                    }}
                    onAddFragment={handleAddFragment}
                    onUpvoteFragment={handleUpvoteFragment}
                    onAddOption={handleAddOption}
                    onUpvoteOption={handleUpvoteOption}
                    onUpvoteQuestion={handleUpvoteQuestion}
                    onReconstructWithAi={handleReconstructWithAi}
                    onOpenAiOptimizer={(targetQ) => setOptimizeQuestion(targetQ)}
                    onSetClaimedAnswer={handleSetClaimedAnswer}
                    isReconstructing={!!reconstructingMap[q.id]}
                  />
                  </div>
                ))}
                {poolQuestions.length > visibleCount && (
                  <div className="text-center py-4">
                    <button
                      type="button"
                      onClick={() => setVisibleCount((prev) => prev + 30)}
                      className="h-11 px-6 rounded-xl bg-white border border-line-2 text-ink font-semibold text-base hover:bg-field cursor-pointer shadow-xs inline-flex items-center gap-2"
                    >
                      Daha fazla soru göster ({poolQuestions.length - visibleCount} soru daha)
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Study workspace: solve, self-test, notes */}
        {activeTab === 'study' && (
          <Suspense fallback={<ViewFallback />}>
            <StudyHub
              questions={questions}
              committees={committees}
              selectedCommitteeId={selectedCommitteeId}
              onSelectCommittee={(id) => setSelectedCommitteeId(id)}
              onStartQuickTest={() => setActiveTab('practice')}
            />
          </Suspense>
        )}

        {/* TAB: Çıkmış Sorular & AI Redaksiyon Arşivi */}
        {activeTab === 'past_exams' && (
          <Suspense fallback={<ViewFallback />}>
            <PastExamsView
              currentUser={currentUser}
              initialSearchQuery={pastExamsSearchQuery}
              onOpenNote={(noteId, pageNumber) => {
                setActiveTab('notes');
              }}
              onUpdateQuestionReference={handleUpdateQuestionReference}
              onNavigateToLearn={(deckId, slideNumber, focus) => {
                setSelectedLearnDeckId(deckId);
                setSelectedLearnSlideNumber(slideNumber);
                setLearnQuestionFocus(focus || null);
                setActiveTab('learn');
              }}
            />
          </Suspense>
        )}

        {/* TAB: /ornek-sorular — müfredata dayalı örnek çalışma soruları */}
        {activeTab === 'ornek_sorular' && (
          <Suspense fallback={<ViewFallback />}>
            <PracticeQuestionsView
              initialLessonId={selectedOrnekLessonId}
              initialKazanimNo={selectedOrnekKazanimNo}
            />
          </Suspense>
        )}

        {/* TAB: /kazanimlar — müfredat ve kazanımlar haritası */}
        {activeTab === 'kazanimlar' && (
          <Suspense fallback={<ViewFallback />}>
            <KazanimlarView
              onNavigateToLearn={(deckId, slideNumber) => {
                if (deckId) setSelectedLearnDeckId(deckId);
                if (slideNumber) setSelectedLearnSlideNumber(slideNumber);
                setActiveTab('learn');
              }}
              onNavigateToPastExams={(query) => {
                if (query) setPastExamsSearchQuery(query);
                setActiveTab('past_exams');
              }}
              onNavigateToOrnek={(lessonId, kazanimNo) => {
                if (lessonId) setSelectedOrnekLessonId(lessonId);
                if (kazanimNo) setSelectedOrnekKazanimNo(kazanimNo);
                setActiveTab('ornek_sorular');
              }}
            />
          </Suspense>
        )}

        {/* TAB: /test/cikmis — Faz 14 Çıkmış Soru İnceleme & Canlı Test Katmanı */}
        {activeTab === 'test_cikmis' && (
          <Suspense fallback={<ViewFallback />}>
            <TestCikmisView
              currentUser={currentUser}
              isAdmin={isAdmin}
              onBackToPastExams={() => setActiveTab('past_exams')}
            />
          </Suspense>
        )}

        {/* TAB: /tester/ozet — 2026-2027 Ders Notları Test Laboratuvarı */}
        {activeTab === 'tester_ozet' && (
          <Suspense fallback={<ViewFallback />}>
            <TesterOzetView />
          </Suspense>
        )}

        {/* TAB 2: 1-100 Question Matrix */}
        {activeTab === 'matrix' && (
          <Suspense fallback={<ViewFallback />}>
            <QuestionMatrix
              questions={questions}
              targetCount={targetCount}
              onSelectQuestion={(q) => {
                setActiveTab('questions');
                setSearchQuery(q.questionNumber.toString());
              }}
              onAddContributionForNumber={(num) => {
                setContributeDefaultNumber(num);
                setIsContributeModalOpen(true);
              }}
            />
          </Suspense>
        )}

        {/* TAB 4: A4 Booklet / Print Mode */}
        {activeTab === 'booklet' && (
          <Suspense fallback={<ViewFallback />}>
            <BookletView
              committee={currentCommittee}
              questions={questions}
              onOpenPdfModal={() => setIsPdfModalOpen(true)}
            />
          </Suspense>
        )}

        {/* TAB 5: Leaderboard / Katkı Sıralaması */}
        {activeTab === 'stats' && (
          <Suspense fallback={<ViewFallback />}>
            <StatsView questions={questions} currentUser={currentUser} onGo={(r) => setActiveTab(r)} />
          </Suspense>
        )}
        {activeTab === 'leaderboard' && (
          <Suspense fallback={<ViewFallback />}>
            <LeaderboardView
              questions={questions}
              committees={committees}
              selectedCommitteeId={selectedCommitteeId}
              onSelectCommittee={(id) => setSelectedCommitteeId(id)}
              currentUser={currentUser}
              onOpenContributeModal={() => {
                setContributeDefaultNumber(undefined);
                setIsContributeModalOpen(true);
              }}
            />
          </Suspense>
        )}

        {/* Profil ve ayarlar: kimlik, tema × palet, yoğunluk, klasik tasarım */}
        {activeTab === 'settings' && (
          <Suspense fallback={<ViewFallback />}>
            <ProfileSettingsView
              currentUser={currentUser}
              isAdmin={isAdmin}
              questions={questions}
              onUpdateUser={(u: AppUser) => setCurrentUser(u)}
              onOpenAuth={() => {
                setAuthModalInitialMode('login');
                setIsAuthModalOpen(true);
              }}
              onLogout={handleGoogleLogout}
              onOpenAdmin={() => setActiveTab('admin')}
              onOpenOffline={() => setIsOfflineModalOpen(true)}
            />
          </Suspense>
        )}

        {/* Topluluk: Müzik — admin paylaşımlı ses çalar (video yok) */}
        {activeTab === 'music' && (
          <Suspense fallback={<ViewFallback />}>
            <MusicView isAdmin={isAdmin} />
          </Suspense>
        )}

        {/* TAB 6: Ders Notları & Slaytlar */}
        {activeTab === 'notes' && (
          <Suspense fallback={<ViewFallback />}>
            <LectureNotesView
              committee={currentCommittee}
              committees={committees}
              questions={questions}
              currentUser={currentUser}
              isAdmin={isAdmin}
              onUpdateQuestionReference={handleUpdateQuestionReference}
            />
          </Suspense>
        )}

        {/* TAB 7: Amfi Ders Özetleri & Spot Bilgiler */}
        {activeTab === 'summaries' && (
          <Suspense fallback={<ViewFallback />}>
            <LectureSummariesView onOpenPdfModal={() => setIsPdfModalOpen(true)} initialSummaryId={openSummaryId} />
          </Suspense>
        )}

        {/* TAB 8: Amfi Ses Kaydı Transkriptleri */}
        {activeTab === 'transcripts' && (
          <Suspense fallback={<ViewFallback />}>
            <TranscriptionsView />
          </Suspense>
        )}

        {/* /veri — MedSoru Core v2 Veri Merkezi (salt okunur) */}
        {activeTab === 'datacore' && (
          <Suspense fallback={<ViewFallback />}>
            <DataCoreView />
          </Suspense>
        )}

        {/* /kartlar — spaced-repetition flashcards (medical terms + lesson cards) */}
        {activeTab === 'flashcards' && (
          <Suspense fallback={<ViewFallback />}>
            <FlashcardsView />
          </Suspense>
        )}

        {/* /asistan — Local AI & Cloud Medical Assistant / Question Detective */}
        {activeTab === 'ai_chat' && (
          <Suspense fallback={<ViewFallback />}>
            <LocalAiChatView
              currentUser={currentUser}
              isAdmin={isAdmin}
              onNavigateToQuestion={(qId) => {
                setPastExamsSearchQuery(qId);
                setActiveTab('past_exams');
              }}
            />
          </Suspense>
        )}


      </main>

      {/* Footer */}
      <footer className="hidden border-t border-line bg-white print:hidden">
        <div className="max-w-[1280px] mx-auto px-4 sm:px-8 py-5 flex flex-col sm:flex-row sm:justify-between gap-3 text-sm text-ink-3">
          <span>
            MeDSor · Tıp Dönem 3 kurul soru havuzu
            {currentUser ? ` · ${currentUser.email}${isAdmin ? ' (yönetici)' : ''}` : ''}
          </span>
          <span className="flex flex-wrap gap-5">
            <button type="button" onClick={() => { setContributeDefaultNumber(undefined); setIsContributeModalOpen(true); }} className="text-ink-2 hover:text-accent cursor-pointer">Katkı yap</button>
            <a href="/sartlar" target="_blank" rel="noopener noreferrer" className="text-ink-2 hover:text-accent">Şartlar</a>
            <a href="/policy" target="_blank" rel="noopener noreferrer" className="text-ink-2 hover:text-accent">Gizlilik</a>
            {isAdmin && (
              <button type="button" onClick={() => setActiveTab('admin')} className="text-ink-2 hover:text-accent cursor-pointer">Yönetim</button>
            )}
            {isAdmin && (
              <button type="button" onClick={() => setActiveTab('manage')} className="text-ink-2 hover:text-accent cursor-pointer">Yönetim Konsolu</button>
            )}
          </span>
        </div>
      </footer>

      {/* Alt gezinme: v8 TabBar, klasik tasarımda eski alt menü */}
      {shellV8 ? (
        <TabBar
          active={activeTab}
          onGo={setActiveTab}
          isAdmin={isAdmin}
          onPdf={() => setIsPdfModalOpen(true)}
          onOffline={() => setIsOfflineModalOpen(true)}
        />
      ) : (
      <MobileBottomNav
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        questionsCount={questions.length}
        isAdmin={isAdmin}
        onOpenContributeModal={() => {
          setContributeDefaultNumber(undefined);
          setIsContributeModalOpen(true);
        }}
        onOpenPdfModal={() => setIsPdfModalOpen(true)}
        onOpenAdminPanel={() => setActiveTab('admin')}
        onUploadToDrive={() => handleDriveUpload(false)}
        onOpenOfflineModal={() => setIsOfflineModalOpen(true)}
      />
      )}
      </div>
      </>
      )}

      {/* Modals */}
      {/* Modals wrapped in Suspense and conditionally mounted */}
      {isContributeModalOpen && (
        <Suspense fallback={null}>
          <ContributeModal
            isOpen={isContributeModalOpen}
            onClose={() => setIsContributeModalOpen(false)}
            committees={committees}
            selectedCommitteeId={selectedCommitteeId}
            defaultQuestionNumber={contributeDefaultNumber}
            currentUser={currentUser}
            questions={questions}
            onAddQuestionContribution={handleAddQuestionContribution}
          />
        </Suspense>
      )}

      {isAdmin && isNewCommitteeModalOpen && (
        <Suspense fallback={null}>
          <AddCommitteeModal
            isOpen={isNewCommitteeModalOpen}
            onClose={() => setIsNewCommitteeModalOpen(false)}
            onAddCommittee={handleAddCommittee}
          />
        </Suspense>
      )}

      {isGithubPagesModalOpen && (
        <Suspense fallback={null}>
          <GithubPagesGuideModal
            isOpen={isGithubPagesModalOpen}
            onClose={() => setIsGithubPagesModalOpen(false)}
          />
        </Suspense>
      )}

      {isAuthErrorModalOpen && (
        <Suspense fallback={null}>
          <AuthErrorModal
            isOpen={isAuthErrorModalOpen}
            onClose={() => setIsAuthErrorModalOpen(false)}
            onLoginSuccess={(user, token) => {
              setCurrentUser(user);
              if (token) setAccessToken(token);
            }}
          />
        </Suspense>
      )}

      {isDriveModalOpen && (
        <Suspense fallback={null}>
          <DriveSaveModal
            isOpen={isDriveModalOpen}
            onClose={() => setIsDriveModalOpen(false)}
            committee={currentCommittee}
            questions={questions}
            currentUser={currentUser}
            accessToken={accessToken}
            onGoogleSignIn={async () => {
              await handleGoogleLogin();
            }}
            onUploadSuccess={(link, fileName) => {
              setDriveUploadSuccess({
                fileId: 'uploaded',
                fileName,
                webViewLink: link,
              });
            }}
          />
        </Suspense>
      )}

      {/* A4 Medical Exam Booklet & High-Resolution PDF Print Modal */}
      {isPdfModalOpen && (
        <Suspense fallback={null}>
          <ExamPdfModal
            isOpen={isPdfModalOpen}
            onClose={() => {
              setIsPdfModalOpen(false);
              setPdfSlideTarget(null);
            }}
            committee={currentCommittee}
            committees={committees}
            questions={questions}
            initialSlide={pdfSlideTarget}
            initialContent={
              activeTab === 'learn' ? 'learn'
                : activeTab === 'summaries' ? 'summary'
                : activeTab === 'ornek_sorular' || activeTab === 'practice' ? 'ornek'
                : activeTab === 'questions' || activeTab === 'booklet' ? 'pool'
                : 'past'
            }
          />
        </Suspense>
      )}

      {/* System Diagnostics & Database Troubleshooting Modal */}
      {isAdmin && isDiagnosticsOpen && (
        <Suspense fallback={null}>
          <SystemDiagnosticsModal
            isOpen={isDiagnosticsOpen}
            onClose={() => setIsDiagnosticsOpen(false)}
            onRefreshParentData={fetchQuestions}
          />
        </Suspense>
      )}

      {/* Yapay Zeka (AI) Quota & Rate Limit Exceeded Modal */}
      {isAdmin && isAiQuotaModalOpen && (
        <Suspense fallback={null}>
          <AiQuotaAlertModal
            isOpen={isAiQuotaModalOpen}
            onClose={() => setIsAiQuotaModalOpen(false)}
            onRetry={fetchQuestions}
          />
        </Suspense>
      )}

      {/* Çevrimdışı Veritabanı & PWA Yönetim Modalı */}
      <OfflineDatabaseModal
        isOpen={isOfflineModalOpen}
        onClose={() => setIsOfflineModalOpen(false)}
        isAdmin={isAdmin}
      />

      {/* PWA & Çevrimdışı Veritabanı Açılış Önerisi Modalı */}
      <PwaInstallWelcomeModal
        isOpen={isPwaWelcomeOpen && !isAdmin && !offlineDatabaseService.getState().isDatabaseDownloaded}
        onClose={() => setIsPwaWelcomeOpen(false)}
        onOpenOfflineDatabase={() => setIsOfflineModalOpen(true)}
      />

      {/* User Login/Register Modal */}
      {isAuthModalOpen && !showOnboarding && (
        <Suspense fallback={null}>
          <UserAuthModal
            isOpen={isAuthModalOpen}
            onClose={() => setIsAuthModalOpen(false)}
            initialMode={authModalInitialMode}
            mandatory={!currentUser}
            onAuthSuccess={handleAuthSuccess}
          />
        </Suspense>
      )}

      {/* User Profile & Student Number Modal */}
      {isProfileModalOpen && currentUser && (
        <Suspense fallback={null}>
          <UserProfileModal
            isOpen={isProfileModalOpen}
            onClose={() => setIsProfileModalOpen(false)}
            currentUser={currentUser}
            onUpdateUser={(updated: AppUser) => setCurrentUser(updated)}
            questions={questions}
            onOpenAdminPanel={() => setActiveTab('admin')}
          />
        </Suspense>
      )}

      {/* Student Question Edit Modal (Old versions are preserved) */}
      {isEditQuestionModalOpen && selectedQuestionToEdit && currentUser && (
        <Suspense fallback={null}>
          <EditMyQuestionModal
            isOpen={isEditQuestionModalOpen}
            onClose={() => {
              setIsEditQuestionModalOpen(false);
              setSelectedQuestionToEdit(null);
            }}
            question={selectedQuestionToEdit}
            committee={currentCommittee}
            currentUser={currentUser}
            onSaveSuccess={(updated: QuestionItem) => {
              setQuestions((prev) => prev.map((q) => (q.id === updated.id ? updated : q)));
              setSelectedQuestionToEdit(null);
              setIsEditQuestionModalOpen(false);
              toast.success('Değişiklikler Kaydedildi', 'Soru bulut veritabanına ve yerel hafızaya başarıyla kaydedildi.');
            }}
            onOpenHistory={() => {
              setSelectedQuestionForHistory(selectedQuestionToEdit);
              setIsHistoryModalOpen(true);
            }}
          />
        </Suspense>
      )}

      {/* Question Revision History Modal */}
      {isHistoryModalOpen && selectedQuestionForHistory && (
        <Suspense fallback={null}>
          <RevisionHistoryModal
            isOpen={isHistoryModalOpen}
            onClose={() => {
              setIsHistoryModalOpen(false);
              setSelectedQuestionForHistory(null);
            }}
            question={selectedQuestionForHistory}
          />
        </Suspense>
      )}

      {/* Admin Past Exam Questions Importer Modal */}
      {isAdmin && isPastExamImporterOpen && (
        <Suspense fallback={null}>
          <AdminPastExamImporterModal
            isOpen={isPastExamImporterOpen}
            onClose={() => setIsPastExamImporterOpen(false)}
            adminEmail={ADMIN_EMAIL}
            committees={committees}
            selectedCommitteeId={selectedCommitteeId}
            onImportSuccess={fetchQuestions}
          />
        </Suspense>
      )}

      {/* NotebookLM & Gemini Sync Modal (Admin only) */}
      {isAdmin && isNotebookLMModalOpen && (
        <Suspense fallback={null}>
          <NotebookLMSyncModal
            isOpen={isNotebookLMModalOpen}
            onClose={() => setIsNotebookLMModalOpen(false)}
            committee={currentCommittee}
            questions={questions}
            currentUser={currentUser}
            isAdmin={isAdmin}
            onQuestionsUpdated={fetchQuestions}
          />
        </Suspense>
      )}

      {/* Admin AI Question Optimizer Modal */}
      {isAdmin && optimizeQuestion && (
        <Suspense fallback={null}>
          <AiQuestionOptimizerModal
            question={optimizeQuestion}
            isOpen={Boolean(optimizeQuestion)}
            onClose={() => setOptimizeQuestion(null)}
            currentUser={currentUser}
            onSaved={(updated) => {
              setQuestions((prev) => prev.map((q) => (q.id === updated.id ? updated : q)));
              setOptimizeQuestion(null);
            }}
            onOpenSlideReader={(note, pageNumber) => {
              setActiveTab('notes');
              setOptimizeQuestion(null);
            }}
          />
        </Suspense>
      )}

      {/* AI Subagents & Hybrid Server Monitor Modal */}
      {isAdmin && isSubagentMonitorOpen && (
        <Suspense fallback={null}>
          <SubagentMonitorModal
            isOpen={isSubagentMonitorOpen}
            onClose={() => setIsSubagentMonitorOpen(false)}
          />
        </Suspense>
      )}

      {/* Soru Havuzu Kümeleme ve Öneri Taslak Otomasyonu Modalı */}
      <QuestionClusterAutomationModal
        isOpen={showClusterModal}
        onClose={() => setShowClusterModal(false)}
        currentUser={currentUser}
        isAdmin={isAdmin}
      />

      </div>
    </MusicPlayerProvider>
    </GlossaryProvider>
  );
}
