import React, { useState, useEffect } from 'react';
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
import { QuestionMatrix } from './components/QuestionMatrix';
import { QuestionCard } from './components/QuestionCard';
import { ContributeModal } from './components/ContributeModal';
import { AddCommitteeModal } from './components/AddCommitteeModal';
import { PracticeMode } from './components/PracticeMode';
import { BookletView } from './components/BookletView';
import { AdminPanelModal } from './components/AdminPanelModal';
import { GithubPagesGuideModal } from './components/GithubPagesGuideModal';
import { AuthErrorModal } from './components/AuthErrorModal';
import { DriveSaveModal } from './components/DriveSaveModal';
import { ExamPdfModal } from './components/ExamPdfModal';
import { QuickAddHero, committeeShortLabel, questionStemText } from './components/QuickAddHero';
import { UserAuthModal } from './components/UserAuthModal';
import { UserProfileModal } from './components/UserProfileModal';
import { EditMyQuestionModal } from './components/EditMyQuestionModal';
import { RevisionHistoryModal } from './components/RevisionHistoryModal';
import { LeaderboardView } from './components/LeaderboardView';
import { LectureNotesView } from './components/LectureNotesView';
import { InfoPopover } from './components/InfoPopover';
import { MobileBottomNav } from './components/MobileBottomNav';
import { PastExamsView } from './components/PastExamsView';
import { AdminPastExamImporterModal } from './components/AdminPastExamImporterModal';
import { NotebookLMSyncModal } from './components/NotebookLMSyncModal';
import { SubagentMonitorModal } from './components/SubagentMonitorModal';
import { REAL_KURUL1_DRIVE_SLIDES } from './services/driveAutomation';
import { ApiService } from './services/api';
import { 
  initAuth, 
  googleSignIn, 
  logout, 
  isAdminUser, 
  ADMIN_EMAIL, 
  getAccessToken,
  getLocalAdminSession,
  setLocalAdminSession,
  updateUserProfileData,
  AppUser
} from './services/auth';
import { getDefaultActiveCommitteeId } from './services/firestoreDb';
import { 
  uploadBookletPdfToDrive, 
  evaluateAutoBackupThreshold, 
  ThresholdStatus,
  FOLDER_NAME
} from './services/drive';

export default function App() {
  const [committees, setCommittees] = useState<Committee[]>([]);
  // Open active upcoming committee automatically based on calendar date
  const [selectedCommitteeId, setSelectedCommitteeId] = useState<string>(() => getDefaultActiveCommitteeId());
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Tab Navigation: 'quick_add' (default simple landing page) | 'questions' | 'past_exams' | 'matrix' | 'leaderboard' | 'notes' | 'practice' | 'booklet'
  const [activeTab, setActiveTab] = useState<'quick_add' | 'questions' | 'past_exams' | 'matrix' | 'leaderboard' | 'notes' | 'practice' | 'booklet'>('quick_add');

  // Filters & Search
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('Tümü');
  const [selectedStatus, setSelectedStatus] = useState<string>('Tümü');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [filterMyQuestionsOnly, setFilterMyQuestionsOnly] = useState<boolean>(false);

  // Modals state
  const [isContributeModalOpen, setIsContributeModalOpen] = useState(false);
  const [isNewCommitteeModalOpen, setIsNewCommitteeModalOpen] = useState(false);
  const [isGithubPagesModalOpen, setIsGithubPagesModalOpen] = useState(false);
  const [isAuthErrorModalOpen, setIsAuthErrorModalOpen] = useState(false);
  const [isDriveModalOpen, setIsDriveModalOpen] = useState(false);
  const [isPdfModalOpen, setIsPdfModalOpen] = useState(false);
  const [isAdminPanelOpen, setIsAdminPanelOpen] = useState(false);
  const [isPastExamImporterOpen, setIsPastExamImporterOpen] = useState(false);
  const [isNotebookLMModalOpen, setIsNotebookLMModalOpen] = useState(false);
  const [isSubagentMonitorOpen, setIsSubagentMonitorOpen] = useState(false);
  const [contributeDefaultNumber, setContributeDefaultNumber] = useState<number | undefined>(undefined);

  // User Auth & Profile Modals
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authModalInitialMode, setAuthModalInitialMode] = useState<'login' | 'register' | 'admin'>('login');
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const [isEditQuestionModalOpen, setIsEditQuestionModalOpen] = useState(false);
  const [selectedQuestionToEdit, setSelectedQuestionToEdit] = useState<QuestionItem | null>(null);
  const [isHistoryModalOpen, setIsHistoryModalOpen] = useState(false);
  const [selectedQuestionForHistory, setSelectedQuestionForHistory] = useState<QuestionItem | null>(null);

  // Celebration Toast
  const [congratsToast, setCongratsToast] = useState<string | null>(null);

  // Reconstructing state tracker by question ID
  const [reconstructingMap, setReconstructingMap] = useState<Record<string, boolean>>({});
  const [isGeneratingSlots, setIsGeneratingSlots] = useState(false);

  // Auth state - Default directly to verified admin session (nofrostlife@gmail.com)
  const [currentUser, setCurrentUser] = useState<AppUser | null>(() => {
    try {
      const existing = getLocalAdminSession();
      if (existing) return existing;
      return setLocalAdminSession(ADMIN_EMAIL);
    } catch (e) {
      return null;
    }
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

  // Initialize Auth on mount
  useEffect(() => {
    try {
      const existingAdmin = getLocalAdminSession() || setLocalAdminSession(ADMIN_EMAIL);
      if (existingAdmin) {
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
        if (local) {
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
  }, [selectedCommitteeId, selectedDiscipline, selectedStatus, searchQuery]);

  const fetchCommittees = async () => {
    try {
      const data = await ApiService.getCommittees();
      if (data && data.length > 0) {
        setCommittees(data);
        if (!selectedCommitteeId) {
          setSelectedCommitteeId(data[0].id);
        }
      }
    } catch (err: any) {
      console.error('Failed to load committees:', err);
      setError('Komite listesi yüklenemedi.');
    }
  };

  const fetchQuestions = async () => {
    if (!selectedCommitteeId) return;
    setLoading(true);
    try {
      const data = await ApiService.getQuestions({
        committeeId: selectedCommitteeId,
        discipline: selectedDiscipline,
        status: selectedStatus,
        search: searchQuery,
      });
      setQuestions(data || []);
    } catch (err: any) {
      console.error('Failed to load questions:', err);
      setError('Sorular yüklenirken hata oluştu.');
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
      if (
        err.code === 'auth/unauthorized-domain' ||
        err.message?.includes('unauthorized-domain')
      ) {
        setIsAuthErrorModalOpen(true);
      } else {
        alert('Google ile giriş yapılırken hata oluştu: ' + (err.message || 'Bilinmeyen hata'));
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

  // Toggle Question Upvote
  const handleUpvoteQuestion = async (questionId: string) => {
    try {
      const currentUserId = currentUser?.uid || currentUser?.email || localStorage.getItem('medsoru_device_token') || 'local_user';
      const res = await ApiService.upvoteQuestion(questionId, currentUserId);
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
              upvotes: res.upvotes !== undefined ? res.upvotes : (idx >= 0 ? Math.max(0, (q.upvotes || 1) - 1) : (q.upvotes || 0) + 1),
              likedBy: newLikedBy,
            };
          }
          return q;
        })
      );
    } catch (err) {
      console.error('Upvote question error:', err);
    }
  };

  // Upvote memory fragment (toggle)
  const handleUpvoteFragment = async (questionId: string, fragmentId: string) => {
    try {
      const currentUserId = currentUser?.uid || currentUser?.email || localStorage.getItem('medsoru_device_token') || 'local_user';
      await ApiService.upvoteFragment(questionId, fragmentId, currentUserId);
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

  // Upvote option (toggle)
  const handleUpvoteOption = async (
    questionId: string,
    key: 'A' | 'B' | 'C' | 'D' | 'E'
  ) => {
    try {
      const currentUserId = currentUser?.uid || currentUser?.email || localStorage.getItem('medsoru_device_token') || 'local_user';
      await ApiService.upvoteOption(questionId, key, currentUserId);
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
      await ApiService.addQuestionContribution({
        ...data,
        authorUid: currentUser?.uid || data.authorUid,
        authorStudentNumber: currentUser?.studentNumber || data.authorStudentNumber,
      });

      // Send congratulations email if user is registered and hasn't received one for this committee yet
      // Requirement: "Bunu yalnızca her kurul 1 kez yap."
      if (currentUser && currentUser.email) {
        const comm = committees.find((c) => c.id === data.committeeId);
        const commName = comm?.name || 'Kurul Sınavı';
        const alreadySent = (currentUser.congratsSentCommittees || []).includes(data.committeeId);

        if (!alreadySent) {
          await ApiService.sendCongratulationsEmail(
            currentUser.email,
            currentUser.displayName || data.author,
            currentUser.studentNumber || undefined,
            commName,
            data.committeeId,
            { questionNumber: data.questionNumber, discipline: data.discipline }
          );

          // Update user state and Firestore so email is only sent once per committee
          const updatedCommittees = [...(currentUser.congratsSentCommittees || []), data.committeeId];
          const updatedUser = await updateUserProfileData(currentUser, {
            congratsSentCommittees: updatedCommittees,
          });
          setCurrentUser(updatedUser);

          setCongratsToast(
            `🎉 Tebrikler! ${commName} için ilk soru katkınız kaydedildi. Teşekkür e-postası ${currentUser.email} adresinize iletildi!`
          );
          setTimeout(() => setCongratsToast(null), 8000);
        }
      }

      await fetchQuestions();
    } catch (err: any) {
      console.error('Add question contribution error:', err);
      alert('Soru kaydedilirken hata oluştu: ' + (err.message || ''));
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
    <div className="min-h-screen bg-canvas text-ink flex flex-col font-sans antialiased">
      {activeTab === 'practice' ? (
        <PracticeMode
          questions={questions}
          title={currentCommittee ? `${committeeShortLabel(currentCommittee).charAt(0)}${committeeShortLabel(currentCommittee).slice(1).toLocaleLowerCase('tr-TR')} · Test çöz` : 'Test çöz'}
          subtitle={currentCommittee?.name.split(':').slice(1).join(':').trim() || currentCommittee?.name}
          onExit={() => setActiveTab('quick_add')}
          onOpenQuestion={openQuestion}
          onOpenContributeModal={() => {
            setContributeDefaultNumber(undefined);
            setIsContributeModalOpen(true);
          }}
        />
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
        onOpenNewCommitteeModal={() => setIsNewCommitteeModalOpen(true)}
        onOpenAdminPanel={() => setIsAdminPanelOpen(true)}
        onOpenPastExamModal={() => setIsPastExamImporterOpen(true)}
        onOpenNotebookLMModal={isAdmin ? () => setIsNotebookLMModalOpen(true) : undefined}
        onOpenSubagentMonitor={() => setIsSubagentMonitorOpen(true)}
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
      />

      {/* Main Container */}
      <main className="flex-1 max-w-[1280px] w-full mx-auto px-4 sm:px-8 py-5 sm:py-10 flex flex-col gap-5 sm:gap-8 pb-28 sm:pb-16">

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
            onOpenAdminPanel={() => setIsAdminPanelOpen(true)}
          />
        )}

        {/* TAB 1: Questions List */}
        {activeTab === 'questions' && (
          <div className="flex flex-col gap-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <nav aria-label="Konum" className="flex flex-wrap items-center gap-2 text-[14px] text-ink-2">
                <span>Soru havuzu</span>
                <span aria-hidden="true">/</span>
                <label className="sr-only" htmlFor="pool-committee">Kurul</label>
                <select
                  id="pool-committee"
                  value={selectedCommitteeId}
                  onChange={(e) => setSelectedCommitteeId(e.target.value)}
                  className="h-9 pl-2 pr-7 rounded-lg border border-line bg-white text-ink font-semibold text-[14px] cursor-pointer max-w-[60vw] truncate"
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
                className="h-10 px-4 rounded-[10px] bg-accent hover:bg-accent-hover text-white font-semibold text-[14px] inline-flex items-center gap-2 cursor-pointer"
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
            ) : (filterMyQuestionsOnly ? myQuestions : questions).length === 0 ? (
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
              <div className="flex flex-col gap-5">
                {(filterMyQuestionsOnly ? myQuestions : questions).map((q) => (
                  <QuestionCard
                    key={q.id}
                    question={q}
                    currentUser={currentUser}
                    isAdmin={isAdmin}
                    onEditQuestion={(targetQ) => {
                      setSelectedQuestionToEdit(targetQ);
                      setIsEditQuestionModalOpen(true);
                    }}
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
                    onSetClaimedAnswer={handleSetClaimedAnswer}
                    isReconstructing={!!reconstructingMap[q.id]}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* TAB: Çıkmış Sorular & AI Redaksiyon Arşivi */}
        {activeTab === 'past_exams' && (
          <PastExamsView
            currentUser={currentUser}
            onOpenNote={(noteId, pageNumber) => {
              setActiveTab('notes');
            }}
            onUpdateQuestionReference={handleUpdateQuestionReference}
          />
        )}

        {/* TAB 2: 1-100 Question Matrix */}
        {activeTab === 'matrix' && (
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
        )}

        {/* TAB 4: A4 Booklet / Print Mode */}
        {activeTab === 'booklet' && (
          <BookletView
            committee={currentCommittee}
            questions={questions}
            onOpenPdfModal={() => setIsPdfModalOpen(true)}
          />
        )}

        {/* TAB 5: Leaderboard / Katkı Sıralaması */}
        {activeTab === 'leaderboard' && (
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
        )}

        {/* TAB 6: Ders Notları & Slaytlar */}
        {activeTab === 'notes' && (
          <LectureNotesView
            committee={currentCommittee}
            committees={committees}
            questions={questions}
            currentUser={currentUser}
            isAdmin={isAdmin}
            onUpdateQuestionReference={handleUpdateQuestionReference}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-line bg-white print:hidden mb-[76px] sm:mb-0">
        <div className="max-w-[1280px] mx-auto px-4 sm:px-8 py-5 flex flex-col sm:flex-row sm:justify-between gap-3 text-[13px] text-ink-3">
          <span>
            MedSoru · Tıp Dönem 3 kurul soru havuzu
            {currentUser ? ` · ${currentUser.email}${isAdmin ? ' (yönetici)' : ''}` : ''}
          </span>
          <span className="flex flex-wrap gap-5">
            <button type="button" onClick={() => { setContributeDefaultNumber(undefined); setIsContributeModalOpen(true); }} className="text-ink-2 hover:text-accent cursor-pointer">Katkı yap</button>
            <button type="button" onClick={() => setIsPdfModalOpen(true)} className="text-ink-2 hover:text-accent cursor-pointer">PDF kitapçık</button>
            <button type="button" onClick={() => setIsAdminPanelOpen(true)} className="text-ink-2 hover:text-accent cursor-pointer">Yönetim</button>
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
        onOpenAdminPanel={() => setIsAdminPanelOpen(true)}
        onUploadToDrive={() => handleDriveUpload(false)}
      />
      </>
      )}

      {/* Modals */}
      <ContributeModal
        isOpen={isContributeModalOpen}
        onClose={() => setIsContributeModalOpen(false)}
        committees={committees}
        selectedCommitteeId={selectedCommitteeId}
        defaultQuestionNumber={contributeDefaultNumber}
        onAddQuestionContribution={handleAddQuestionContribution}
      />

      <AddCommitteeModal
        isOpen={isNewCommitteeModalOpen}
        onClose={() => setIsNewCommitteeModalOpen(false)}
        onAddCommittee={handleAddCommittee}
      />

      <GithubPagesGuideModal
        isOpen={isGithubPagesModalOpen}
        onClose={() => setIsGithubPagesModalOpen(false)}
      />

      <AuthErrorModal
        isOpen={isAuthErrorModalOpen}
        onClose={() => setIsAuthErrorModalOpen(false)}
        onLoginSuccess={(user, token) => {
          setCurrentUser(user);
          if (token) setAccessToken(token);
        }}
      />

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

      {/* Admin Panel Modal for nofrostlife@gmail.com */}
      <AdminPanelModal
        isOpen={isAdminPanelOpen}
        onClose={() => setIsAdminPanelOpen(false)}
        adminEmail={ADMIN_EMAIL}
        committees={committees}
        questions={questions}
        selectedCommitteeId={selectedCommitteeId}
        onRefreshData={fetchQuestions}
        onOpenSubagentMonitor={() => setIsSubagentMonitorOpen(true)}
      />

      {/* A4 Medical Exam Booklet & High-Resolution PDF Print Modal */}
      <ExamPdfModal
        isOpen={isPdfModalOpen}
        onClose={() => setIsPdfModalOpen(false)}
        committee={currentCommittee}
        questions={questions}
      />

      {/* User Login/Register Modal */}
      <UserAuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        initialMode={authModalInitialMode}
        onAuthSuccess={(user, token) => {
          setCurrentUser(user);
          if (token) setAccessToken(token);
          setIsAuthModalOpen(false);
          if (isAdminUser(user)) {
            setIsAdminPanelOpen(true);
          }
        }}
      />

      {/* User Profile & Student Number Modal */}
      {currentUser && (
        <UserProfileModal
          isOpen={isProfileModalOpen}
          onClose={() => setIsProfileModalOpen(false)}
          currentUser={currentUser}
          onUpdateUser={(updated: AppUser) => setCurrentUser(updated)}
          questions={questions}
          onOpenAdminPanel={() => setIsAdminPanelOpen(true)}
        />
      )}

      {/* Student Question Edit Modal (Old versions are preserved) */}
      {selectedQuestionToEdit && currentUser && (
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
          }}
          onOpenHistory={() => {
            setSelectedQuestionForHistory(selectedQuestionToEdit);
            setIsHistoryModalOpen(true);
          }}
        />
      )}

      {/* Question Revision History Modal */}
      {selectedQuestionForHistory && (
        <RevisionHistoryModal
          isOpen={isHistoryModalOpen}
          onClose={() => {
            setIsHistoryModalOpen(false);
            setSelectedQuestionForHistory(null);
          }}
          question={selectedQuestionForHistory}
        />
      )}

      {/* Admin Past Exam Questions Importer Modal */}
      <AdminPastExamImporterModal
        isOpen={isPastExamImporterOpen}
        onClose={() => setIsPastExamImporterOpen(false)}
        adminEmail={ADMIN_EMAIL}
        committees={committees}
        selectedCommitteeId={selectedCommitteeId}
        onImportSuccess={fetchQuestions}
      />

      {/* NotebookLM & Gemini Sync Modal (Admin only) */}
      {isAdmin && (
        <NotebookLMSyncModal
          isOpen={isNotebookLMModalOpen}
          onClose={() => setIsNotebookLMModalOpen(false)}
          committee={currentCommittee}
          questions={questions}
          lectureNotes={REAL_KURUL1_DRIVE_SLIDES.map((s) => ({ ...s, committeeId: selectedCommitteeId }))}
          currentUser={currentUser}
          isAdmin={isAdmin}
          onQuestionsUpdated={fetchQuestions}
        />
      )}

      {/* AI Subagents & Hybrid Server Monitor Modal */}
      <SubagentMonitorModal
        isOpen={isSubagentMonitorOpen}
        onClose={() => setIsSubagentMonitorOpen(false)}
      />

    </div>
  );
}
