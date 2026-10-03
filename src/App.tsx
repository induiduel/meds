import React, { useState, useEffect, useMemo, useCallback, Suspense } from 'react';
import { AppRoute, parseLocation, writeLocation, ROUTE_TITLES } from './router';
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
  FileText
} from 'lucide-react';
import { Committee, QuestionItem, QuestionLectureMatch } from './types';
import { Header } from './components/Header';
import { MetricsBar } from './components/MetricsBar';
import { QuestionCard } from './components/QuestionCard';
import { QuickAddHero, committeeShortLabel, questionStemText } from './components/QuickAddHero';
import { MobileBottomNav } from './components/MobileBottomNav';
import { SectionLoader } from './components/ui/Animations';
import { ToastHost, toast } from './components/ui/Toast';

// Lazy-loaded Views (Split into separate on-demand chunks)
const PracticeMode = React.lazy(() => import('./components/PracticeMode').then(m => ({ default: m.PracticeMode })));
const StudyHub = React.lazy(() => import('./components/study/StudyHub').then(m => ({ default: m.StudyHub })));
const BookletView = React.lazy(() => import('./components/BookletView').then(m => ({ default: m.BookletView })));
const LeaderboardView = React.lazy(() => import('./components/LeaderboardView').then(m => ({ default: m.LeaderboardView })));
const LectureNotesView = React.lazy(() => import('./components/LectureNotesView').then(m => ({ default: m.LectureNotesView })));
const PastExamsView = React.lazy(() => import('./components/PastExamsView').then(m => ({ default: m.PastExamsView })));
const QuestionMatrix = React.lazy(() => import('./components/QuestionMatrix').then(m => ({ default: m.QuestionMatrix })));

// Lazy-loaded Modals (Only downloaded when opened)
const AdminPanelModal = React.lazy(() => import('./components/AdminPanelModal').then(m => ({ default: m.AdminPanelModal })));
const ExamPdfModal = React.lazy(() => import('./components/ExamPdfModal').then(m => ({ default: m.ExamPdfModal })));
const ContributeModal = React.lazy(() => import('./components/ContributeModal').then(m => ({ default: m.ContributeModal })));
const AddCommitteeModal = React.lazy(() => import('./components/AddCommitteeModal').then(m => ({ default: m.AddCommitteeModal })));
const GithubPagesGuideModal = React.lazy(() => import('./components/GithubPagesGuideModal').then(m => ({ default: m.GithubPagesGuideModal })));
const AuthErrorModal = React.lazy(() => import('./components/AuthErrorModal').then(m => ({ default: m.AuthErrorModal })));
const DriveSaveModal = React.lazy(() => import('./components/DriveSaveModal').then(m => ({ default: m.DriveSaveModal })));
const UserAuthModal = React.lazy(() => import('./components/UserAuthModal').then(m => ({ default: m.UserAuthModal })));
const UserProfileModal = React.lazy(() => import('./components/UserProfileModal').then(m => ({ default: m.UserProfileModal })));
const EditMyQuestionModal = React.lazy(() => import('./components/EditMyQuestionModal').then(m => ({ default: m.EditMyQuestionModal })));
const RevisionHistoryModal = React.lazy(() => import('./components/RevisionHistoryModal').then(m => ({ default: m.RevisionHistoryModal })));
const AdminPastExamImporterModal = React.lazy(() => import('./components/AdminPastExamImporterModal').then(m => ({ default: m.AdminPastExamImporterModal })));
const AiQuestionOptimizerModal = React.lazy(() => import('./components/AiQuestionOptimizerModal').then(m => ({ default: m.AiQuestionOptimizerModal })));
const NotebookLMSyncModal = React.lazy(() => import('./components/NotebookLMSyncModal').then(m => ({ default: m.NotebookLMSyncModal })));
const SubagentMonitorModal = React.lazy(() => import('./components/SubagentMonitorModal').then(m => ({ default: m.SubagentMonitorModal })));
const SystemDiagnosticsModal = React.lazy(() => import('./components/SystemDiagnosticsModal').then(m => ({ default: m.SystemDiagnosticsModal })));
const AiQuotaAlertModal = React.lazy(() => import('./components/AiQuotaAlertModal').then(m => ({ default: m.AiQuotaAlertModal })));
const LectureSummariesView = React.lazy(() => import('./components/LectureSummariesView').then(m => ({ default: m.LectureSummariesView })));
const TranscriptionsView = React.lazy(() => import('./components/TranscriptionsView').then(m => ({ default: m.TranscriptionsView })));
const FlashcardsView = React.lazy(() => import('./components/flashcards/FlashcardsView').then(m => ({ default: m.FlashcardsView })));
const InteractiveDeckView = React.lazy(() => import('./components/learn/InteractiveDeckView').then(m => ({ default: m.InteractiveDeckView })));
const MedicalEncyclopediaView = React.lazy(() => import('./components/encyclopedia/MedicalEncyclopediaView').then(m => ({ default: m.MedicalEncyclopediaView })));
const ManageConsole = React.lazy(() => import('./components/manage/ManageConsole').then(m => ({ default: m.ManageConsole })));

const ViewFallback = () => <SectionLoader />;
import { GlossaryProvider } from './components/learn/MedicalGlossaryPopover';
import { systemHealthMonitor } from './services/systemHealthMonitor';
import { ApiService } from './services/api';
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
      if (typeof window !== 'undefined' && /^manage\./i.test(window.location.hostname) && parsed.route === 'quick_add') {
        return { route: 'manage' as ValidAppTab, param: undefined as string | undefined };
      }
    } catch {}
    return parsed;
  });
  const [activeTab, setActiveTabState] = useState<ValidAppTab>(initialRoute.route);
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
  const [contributeDefaultNumber, setContributeDefaultNumber] = useState<number | undefined>(undefined);

  // User Auth & Profile Modals
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authModalInitialMode, setAuthModalInitialMode] = useState<'login' | 'register' | 'admin'>('login');
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
  const [selectedLearnSlideNumber, setSelectedLearnSlideNumber] = useState<number | undefined>(undefined);
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

  // Normalise legacy #tab links to their path once, then follow back / forward
  useEffect(() => {
    writeLocation(initialRoute.route, initialRoute.param, true);
    const onPop = () => {
      const { route, param } = parseLocation();
      setActiveTabState(route);
      if (route === 'learn') {
        setSelectedLearnDeckId(param);
        setSelectedLearnSlideNumber(undefined);
      }
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    document.title = activeTab === 'quick_add' ? 'MedSoru · Soru ekle' : `${ROUTE_TITLES[activeTab]} · MedSoru`;
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

  const currentCommittee = committees.find((c) => c.id === selectedCommitteeId);
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
    const currentUserId = currentUser?.uid || currentUser?.email || localStorage.getItem('medsoru_device_token') || 'local_user';
    setQuestions((prev) =>
      prev.map((q) => {
        if (q.id === questionId) {
          const likedBy = q.likedBy || [];
          const idx = likedBy.indexOf(currentUserId);
          const newLikedBy = idx >= 0
            ? likedBy.filter((u) => u !== currentUserId)
            : [...likedBy, currentUserId];
          return {
            ...q,
            upvotes: idx >= 0 ? Math.max(0, (q.upvotes || 1) - 1) : (q.upvotes || 0) + 1,
            likedBy: newLikedBy,
          };
        }
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
    const currentUserId = currentUser?.uid || currentUser?.email || localStorage.getItem('medsoru_device_token') || 'local_user';
    setQuestions((prev) =>
      prev.map((q) => {
        if (q.id === questionId) {
          return {
            ...q,
            fragments: q.fragments.map((f) => {
              if (f.id === fragmentId) {
                const likedBy = f.likedBy || [];
                const idx = likedBy.indexOf(currentUserId);
                const newLikedBy = idx >= 0
                  ? likedBy.filter((u) => u !== currentUserId)
                  : [...likedBy, currentUserId];
                return {
                  ...f,
                  upvotes: idx >= 0 ? Math.max(0, (f.upvotes || 1) - 1) : (f.upvotes || 0) + 1,
                  likedBy: newLikedBy,
                };
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
    const currentUserId = currentUser?.uid || currentUser?.email || localStorage.getItem('medsoru_device_token') || 'local_user';
    setQuestions((prev) =>
      prev.map((q) => {
        if (q.id === questionId) {
          return {
            ...q,
            options: q.options.map((o) => {
              if (o.key === key) {
                const likedBy = o.likedBy || [];
                const idx = likedBy.indexOf(currentUserId);
                const newLikedBy = idx >= 0
                  ? likedBy.filter((u) => u !== currentUserId)
                  : [...likedBy, currentUserId];
                return {
                  ...o,
                  upvotes: idx >= 0 ? Math.max(0, (o.upvotes || 1) - 1) : (o.upvotes || 0) + 1,
                  likedBy: newLikedBy,
                };
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
    if (!window.confirm(`${label} kalıcı olarak veritabanından silmek istediğinize emin misiniz? Bu işlem geri alınamaz.`)) {
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

  // Trigger Gemini AI Reconstruction
  const handleReconstructWithAi = async (questionId: string) => {
    setReconstructingMap((prev) => ({ ...prev, [questionId]: true }));
    try {
      const updatedQuestion = await ApiService.reconstructWithAi(questionId);
      if (updatedQuestion) {
        setQuestions((prev) =>
          prev.map((q) => (q.id === questionId ? updatedQuestion : q))
        );
      }
    } catch (err: any) {
      console.error('Reconstruct error:', err);
      alert('Yapay zeka rekonstrüksiyonu sırasında bağlantı hatası oluştu: ' + (err.message || ''));
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
  }) => {
    try {
      const savedQuestion = await ApiService.addQuestionContribution({
        ...data,
        authorUid: currentUser?.uid || data.authorUid,
        authorStudentNumber: currentUser?.studentNumber || data.authorStudentNumber,
      });

      // Anında arayüze yansıt (0ms Optimistic UI)
      if (savedQuestion) {
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
        const comm = committees.find((c) => c.id === data.committeeId);
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
      const currentComm = committees.find((c) => c.id === selectedCommitteeId);
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

  const completedQuestions = questions.filter(
    (q) => q.status === 'completed' && q.reconstruction
  );
  const gatheringQuestions = questions.filter(
    (q) => q.status === 'gathering' || (q.status !== 'completed' && q.fragments.length > 0)
  );
  const emptyQuestions = questions.filter(
    (q) => q.status === 'empty' && q.fragments.length === 0
  );

  const myQuestions = questions.filter(
    (q) =>
      currentUser &&
      (q.contributedByUid === currentUser.uid ||
        (currentUser.displayName && q.contributedByName === currentUser.displayName) ||
        q.fragments.some((f) => f.authorUid === currentUser.uid || (currentUser.displayName && f.author === currentUser.displayName)) ||
        q.options.some((o) => o.suggestedByUid === currentUser.uid || (currentUser.displayName && o.suggestedBy === currentUser.displayName)))
  );

  // Ultra-fast in-memory filtering: 0ms search & filter without network lag
  const filteredQuestions = useMemo(() => {
    let result = questions;
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
          item.options?.some((o) => o.text.toLowerCase().includes(q))
      );
    }
    return result;
  }, [questions, selectedDiscipline, selectedStatus, searchQuery]);

  // Progressive rendering: Keep DOM lightweight with 30 cards at a time
  const [visibleCount, setVisibleCount] = useState<number>(30);

  useEffect(() => {
    setVisibleCount(30);
  }, [selectedCommitteeId, selectedDiscipline, selectedStatus, searchQuery, filterMyQuestionsOnly]);

  const poolQuestions = filterMyQuestionsOnly ? myQuestions : filteredQuestions;
  const displayedQuestions = poolQuestions.slice(0, visibleCount);

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

  return (
    <GlossaryProvider>
      <div className="min-h-screen bg-canvas text-ink flex flex-col font-sans antialiased">
      <ToastHost />
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
      ) : activeTab === 'manage' ? (
        isAdmin ? (
          <Suspense fallback={<ViewFallback />}>
            <ManageConsole
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
            <div className="max-w-[440px] w-full bg-white border border-line rounded-[18px] p-6 sm:p-8 flex flex-col items-center text-center gap-3">
              <span className="w-12 h-12 rounded-2xl bg-ink text-white flex items-center justify-center">
                <ShieldCheck className="w-6 h-6" />
              </span>
              <h1 className="m-0 font-display font-bold text-[24px] tracking-[-0.02em]">Yönetim Konsolu</h1>
              <p className="m-0 text-[15px] text-ink-2">Bu konsol yalnızca yöneticilere açık. Devam etmek için yönetici hesabıyla giriş yap.</p>
              <div className="flex gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setActiveTab('quick_add')}
                  className="h-11 px-4 rounded-xl border border-line-2 bg-white font-semibold text-[15px] cursor-pointer"
                >
                  Ana sayfa
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setAuthModalInitialMode('admin');
                    setIsAuthModalOpen(true);
                  }}
                  className="h-11 px-5 rounded-xl bg-accent hover:bg-accent-hover text-white font-semibold text-[15px] cursor-pointer"
                >
                  Yönetici girişi
                </button>
              </div>
            </div>
          </div>
        )
      ) : (
      <>
      {/* Navigation Header with Google Auth & Drive */}
      <Header
        searchQuery={searchQuery}
        onSearch={(q) => {
          setSearchQuery(q);
          setActiveTab('questions');
        }}
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
        onOpenProfileModal={() => setIsProfileModalOpen(true)}
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
      />

      {/* Main Container */}
      <main className="flex-1 max-w-[1280px] w-full mx-auto px-3 sm:px-8 pt-4 sm:pt-8 flex flex-col gap-4 sm:gap-6 pb-28 lg:pb-16">

        {/* Drive Upload Notification Banner if successful */}
        {driveUploadSuccess && (
          <div role="status" className="bg-ok-soft rounded-[14px] px-4 py-3 sm:px-5 sm:py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-5 h-5 text-ok shrink-0 mt-0.5" />
              <div>
                <p className="m-0 font-semibold text-[15px] text-ok">PDF Google Drive'a kaydedildi</p>
                <p className="m-0 text-[14px] text-ink">
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
                  className="h-10 px-4 rounded-[10px] bg-white border border-line-2 text-ink font-semibold text-[14px] inline-flex items-center gap-2"
                >
                  Drive'da aç
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
              <button
                type="button"
                onClick={() => setDriveUploadSuccess(null)}
                className="h-10 px-3 rounded-[10px] text-ink-2 font-semibold text-[14px] cursor-pointer"
              >
                Kapat
              </button>
            </div>
          </div>
        )}

        {/* Celebration / Thank You Notification */}
        {congratsToast && (
          <div role="status" className="bg-ink text-white rounded-[14px] px-4 py-3 sm:px-5 sm:py-4 flex items-center justify-between gap-3">
            <div className="flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-[#FBBF24] shrink-0 mt-0.5" />
              <div>
                <p className="m-0 font-semibold text-[15px]">Teşekkürler!</p>
                <p className="m-0 text-[14px] text-[#B8C3CF]">{congratsToast}</p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setCongratsToast(null)}
              className="h-10 px-4 rounded-[10px] bg-white/10 hover:bg-white/20 font-semibold text-[14px] cursor-pointer shrink-0"
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
          />
        )}

        {/* TAB: Learn / İnteraktif Ses & Slayt Hub'ı */}
        {activeTab === 'learn' && (
          <Suspense fallback={<ViewFallback />}>
            <InteractiveDeckView
              initialDeckId={selectedLearnDeckId}
              initialSlideNumber={selectedLearnSlideNumber}
              onDeckChange={(id) => {
                setSelectedLearnDeckId(id ?? undefined);
                if (id === null) setSelectedLearnSlideNumber(undefined);
                writeLocation('learn', id ?? undefined);
              }}
              onOpenPdfModal={(target) => {
                setPdfSlideTarget(target ?? null);
                setIsPdfModalOpen(true);
              }}
              onSelectCommittee={(id) => setSelectedCommitteeId(id)}
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

        {/* TAB 1: Questions List */}
        {activeTab === 'questions' && (
          <div className="flex flex-col gap-3 sm:gap-5">
            <div className="flex flex-wrap items-center justify-between gap-2 sm:gap-3">
              <nav aria-label="Konum" className="flex flex-wrap items-center gap-2 text-[14px] text-ink-2 min-w-0 flex-1">
                <span className="hidden sm:inline">Soru havuzu</span>
                <span aria-hidden="true" className="hidden sm:inline">/</span>
                <label className="sr-only" htmlFor="pool-committee">Kurul</label>
                <select
                  id="pool-committee"
                  value={selectedCommitteeId}
                  onChange={(e) => setSelectedCommitteeId(e.target.value)}
                  className="h-10 sm:h-9 pl-2 pr-7 rounded-lg border border-line bg-white text-ink font-semibold text-[14px] cursor-pointer w-full sm:w-auto sm:max-w-[60vw] truncate"
                >
                  {committees.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
                {searchQuery && (
                  <>
                    <span aria-hidden="true">/</span>
                    <span className="text-ink font-semibold">“{searchQuery}”</span>
                    <button
                      type="button"
                      onClick={() => setSearchQuery('')}
                      className="h-8 px-2.5 rounded-lg text-accent font-semibold cursor-pointer"
                    >
                      Aramayı temizle
                    </button>
                  </>
                )}
              </nav>
              <button
                type="button"
                onClick={() => {
                  setContributeDefaultNumber(undefined);
                  setIsContributeModalOpen(true);
                }}
                className="hidden sm:inline-flex h-10 px-4 rounded-[10px] bg-accent hover:bg-accent-hover text-white font-semibold text-[14px] items-center gap-2 cursor-pointer"
              >
                <Plus className="w-4 h-4" strokeWidth={2.2} />
                Soru ekle
              </button>
            </div>

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
              <div className="text-center py-16 bg-white rounded-[18px] border border-line">
                <RefreshCw className="w-6 h-6 text-accent animate-spin mx-auto mb-3" />
                <p className="m-0 text-[14px] text-ink-2">Soru havuzu yükleniyor…</p>
              </div>
            ) : poolQuestions.length === 0 ? (
              <div className="bg-white rounded-[18px] border border-line px-6 py-14 text-center flex flex-col items-center gap-4">
                <div>
                  <h3 className="m-0 font-display text-[22px] font-bold tracking-[-0.02em]">
                    {filterMyQuestionsOnly ? 'Henüz katkıda bulunduğun soru yok' : 'Bu kriterlere uyan soru yok'}
                  </h3>
                  <p className="m-0 mt-1.5 text-[15px] text-ink-2 max-w-[420px]">
                    {filterMyQuestionsOnly
                      ? 'Aklında kalan parçaları ekleyerek kurul arşivine katkı sağlayabilirsin.'
                      : 'Henüz soru girilmemiş olabilir ya da filtreye uyan soru yok.'}
                  </p>
                </div>
                <div className="flex items-center justify-center gap-2">
                  {filterMyQuestionsOnly && (
                    <button
                      type="button"
                      onClick={() => setFilterMyQuestionsOnly(false)}
                      className="h-11 px-4 rounded-[10px] border border-line-2 bg-white font-semibold cursor-pointer"
                    >
                      Tüm soruları göster
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={() => {
                      setContributeDefaultNumber(undefined);
                      setIsContributeModalOpen(true);
                    }}
                    className="h-11 px-5 rounded-[10px] bg-accent hover:bg-accent-hover text-white font-semibold cursor-pointer"
                  >
                    İlk soruyu ekle
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex flex-col gap-3 sm:gap-5">
                {displayedQuestions.map((q) => (
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
                ))}
                {poolQuestions.length > visibleCount && (
                  <div className="text-center py-4">
                    <button
                      type="button"
                      onClick={() => setVisibleCount((prev) => prev + 30)}
                      className="h-11 px-6 rounded-xl bg-white border border-line-2 text-ink font-semibold text-[14px] hover:bg-slate-50 cursor-pointer shadow-xs inline-flex items-center gap-2"
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
              onOpenNote={(noteId, pageNumber) => {
                setActiveTab('notes');
              }}
              onUpdateQuestionReference={handleUpdateQuestionReference}
              onNavigateToLearn={(deckId, slideNumber) => {
                setSelectedLearnDeckId(deckId);
                setSelectedLearnSlideNumber(slideNumber);
                setActiveTab('learn');
              }}
            />
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
            <LectureSummariesView onOpenPdfModal={() => setIsPdfModalOpen(true)} />
          </Suspense>
        )}

        {/* TAB 8: Amfi Ses Kaydı Transkriptleri */}
        {activeTab === 'transcripts' && (
          <Suspense fallback={<ViewFallback />}>
            <TranscriptionsView />
          </Suspense>
        )}

        {/* /kartlar — spaced-repetition flashcards (medical terms + lesson cards) */}
        {activeTab === 'flashcards' && (
          <Suspense fallback={<ViewFallback />}>
            <FlashcardsView />
          </Suspense>
        )}

        {/* /yonetim — admin panel as its own page */}
        {activeTab === 'admin' &&
          (isAdmin ? (
            <Suspense fallback={<ViewFallback />}>
              <AdminPanelModal
                variant="page"
                isOpen
                onClose={() => setActiveTab('quick_add')}
                adminEmail={ADMIN_EMAIL}
                committees={committees}
                questions={questions}
                selectedCommitteeId={selectedCommitteeId}
                onRefreshData={fetchQuestions}
                onOpenSubagentMonitor={() => setIsSubagentMonitorOpen(true)}
              />
            </Suspense>
          ) : (
            <div className="max-w-[440px] w-full mx-auto mt-6 sm:mt-14 bg-white border border-line rounded-[18px] p-6 sm:p-8 flex flex-col items-center text-center gap-3">
              <span className="w-12 h-12 rounded-2xl bg-ink text-white flex items-center justify-center">
                <ShieldCheck className="w-6 h-6" />
              </span>
              <h1 className="m-0 font-display font-bold text-[24px] tracking-[-0.02em]">Yönetim</h1>
              <p className="m-0 text-[15px] text-ink-2">Bu sayfa yalnızca yöneticilere açık. Devam etmek için yönetici hesabıyla giriş yap.</p>
              <div className="flex gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setActiveTab('quick_add')}
                  className="h-11 px-4 rounded-xl border border-line-2 bg-white font-semibold text-[15px] cursor-pointer"
                >
                  Ana sayfa
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setAuthModalInitialMode('admin');
                    setIsAuthModalOpen(true);
                  }}
                  className="h-11 px-5 rounded-xl bg-accent hover:bg-accent-hover text-white font-semibold text-[15px] cursor-pointer"
                >
                  Yönetici girişi
                </button>
              </div>
            </div>
          ))}

      </main>

      {/* Footer */}
      <footer className="hidden lg:block border-t border-line bg-white print:hidden">
        <div className="max-w-[1280px] mx-auto px-4 sm:px-8 py-5 flex flex-col sm:flex-row sm:justify-between gap-3 text-[13px] text-ink-3">
          <span>
            MedSoru · Tıp Dönem 3 kurul soru havuzu
            {currentUser ? ` · ${currentUser.email}${isAdmin ? ' (yönetici)' : ''}` : ''}
          </span>
          <span className="flex flex-wrap gap-5">
            <button type="button" onClick={() => { setContributeDefaultNumber(undefined); setIsContributeModalOpen(true); }} className="text-ink-2 hover:text-accent cursor-pointer">Katkı yap</button>
            <button type="button" onClick={() => setIsPdfModalOpen(true)} className="text-ink-2 hover:text-accent cursor-pointer">PDF kitapçık</button>
            {isAdmin && (
              <button type="button" onClick={() => setActiveTab('admin')} className="text-ink-2 hover:text-accent cursor-pointer">Yönetim</button>
            )}
            {isAdmin && (
              <button type="button" onClick={() => setActiveTab('manage')} className="text-ink-2 hover:text-accent cursor-pointer">Yönetim Konsolu</button>
            )}
          </span>
        </div>
      </footer>

      {/* Mobile-First Bottom Navigation Bar */}
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
      />
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

      {/* User Login/Register Modal */}
      {isAuthModalOpen && (
        <Suspense fallback={null}>
          <UserAuthModal
            isOpen={isAuthModalOpen}
            onClose={() => setIsAuthModalOpen(false)}
            initialMode={authModalInitialMode}
            onAuthSuccess={(user, token) => {
              setCurrentUser(user);
              if (token) setAccessToken(token);
              setIsAuthModalOpen(false);
              if (isAdminUser(user)) {
                setActiveTab('admin');
              }
            }}
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

      </div>
    </GlossaryProvider>
  );
}
