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
import { QuickAddHero } from './components/QuickAddHero';
import { UserAuthModal } from './components/UserAuthModal';
import { UserProfileModal } from './components/UserProfileModal';
import { EditMyQuestionModal } from './components/EditMyQuestionModal';
import { RevisionHistoryModal } from './components/RevisionHistoryModal';
import { LeaderboardView } from './components/LeaderboardView';
import { LectureNotesView } from './components/LectureNotesView';
import { InfoPopover } from './components/InfoPopover';
import { MobileBottomNav } from './components/MobileBottomNav';
import { AdminPastExamImporterModal } from './components/AdminPastExamImporterModal';
import { NotebookLMSyncModal } from './components/NotebookLMSyncModal';
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

  // Tab Navigation: 'quick_add' (default simple landing page) | 'questions' | 'matrix' | 'leaderboard' | 'notes' | 'practice' | 'booklet'
  const [activeTab, setActiveTab] = useState<'quick_add' | 'questions' | 'matrix' | 'leaderboard' | 'notes' | 'practice' | 'booklet'>('quick_add');

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

  // Upvote memory fragment
  const handleUpvoteFragment = async (questionId: string, fragmentId: string) => {
    try {
      await ApiService.upvoteFragment(questionId, fragmentId);
      setQuestions((prev) =>
        prev.map((q) => {
          if (q.id === questionId) {
            return {
              ...q,
              fragments: q.fragments.map((f) =>
                f.id === fragmentId ? { ...f, upvotes: (f.upvotes || 0) + 1 } : f
              ),
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

  // Upvote option
  const handleUpvoteOption = async (
    questionId: string,
    key: 'A' | 'B' | 'C' | 'D' | 'E'
  ) => {
    try {
      await ApiService.upvoteOption(questionId, key);
      setQuestions((prev) =>
        prev.map((q) => {
          if (q.id === questionId) {
            return {
              ...q,
              options: q.options.map((o) =>
                o.key === key ? { ...o, upvotes: (o.upvotes || 0) + 1 } : o
              ),
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
    <div className="min-h-screen bg-slate-100/70 text-slate-800 flex flex-col font-sans antialiased selection:bg-teal-500 selection:text-white">
      {/* Navigation Header with Google Auth & Drive */}
      <Header
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
      <main className="flex-1 max-w-7xl w-full mx-auto px-3 sm:px-6 py-4 sm:py-6 space-y-4 sm:space-y-6 pb-24 sm:pb-8">
        
        {/* Drive Upload Notification Banner if successful */}
        {driveUploadSuccess && (
          <div className="bg-emerald-50 border border-emerald-300 rounded-xl p-3 sm:p-4 text-emerald-950 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-xs animate-fadeIn">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-emerald-600 text-white shrink-0">
                <Cloud className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-sm flex items-center gap-1.5 text-emerald-900">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  PDF Başarıyla Google Drive'a Kaydedildi!
                </h4>
                <p className="text-xs text-emerald-800 mt-0.5">
                  Dosya Adı: <strong>{driveUploadSuccess.fileName}</strong> • Klasör: <strong>"{FOLDER_NAME}"</strong>
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 self-start sm:self-auto shrink-0">
              {driveUploadSuccess.webViewLink && (
                <a
                  href={driveUploadSuccess.webViewLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-emerald-700 hover:bg-emerald-800 text-white font-bold px-3.5 py-1.5 rounded-lg text-xs flex items-center gap-1.5 shadow-2xs transition-all"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                  <span>Google Drive'da Aç</span>
                </a>
              )}
              <button
                onClick={() => setDriveUploadSuccess(null)}
                className="text-emerald-700 hover:text-emerald-900 text-xs px-2 py-1 cursor-pointer"
              >
                Kapat
              </button>
            </div>
          </div>
        )}

        {/* Compact, Mobile-First Committee & Cloud Archive Strip (Info is tucked into InfoPopover) */}
        {currentCommittee && (
          <div className="bg-white rounded-xl p-3 sm:p-4 border border-slate-200/90 shadow-2xs flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div className="flex items-center gap-2.5 flex-wrap">
              <span className="text-[10px] sm:text-[11px] font-bold uppercase tracking-wider bg-teal-50 text-teal-800 border border-teal-200 px-2 py-0.5 rounded-md">
                Dönem {currentCommittee.year} • {currentCommittee.term}
              </span>
              <h2 className="text-sm sm:text-base font-extrabold text-slate-900 tracking-tight">
                {currentCommittee.name}
              </h2>
              <span className="text-[11px] font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
                {questions.length} / {currentCommittee.targetCount} Soru
              </span>

              {/* Info Popover for Committee description & Drive Archive information */}
              <InfoPopover title="Kurul & Google Drive Arşiv Bilgisi">
                <div className="space-y-2">
                  <div>
                    <h5 className="font-bold text-slate-800 text-xs">Kurul Hakkında:</h5>
                    <p className="text-[11px] text-slate-600 mt-0.5">
                      {currentCommittee.description ||
                        'Öğrencilerin sınav çıkışı hatırladığı soru parçaları toplanır ve tıp literatürü esas alınarak sınav soru kitapçığı haline getirilir.'}
                    </p>
                  </div>
                  <div className="pt-2 border-t border-slate-100">
                    <h5 className="font-bold text-teal-900 text-xs flex items-center gap-1">
                      <Cloud className="w-3.5 h-3.5 text-teal-600" />
                      Google Drive Bulut Arşivi:
                    </h5>
                    <p className="text-[11px] text-slate-600 mt-0.5">
                      Tüm sorular standart A4 formatında Google Drive hesabınızdaki "{FOLDER_NAME}" klasörüne kaydedilir ve dilediğiniz an PDF olarak indirilebilir.
                    </p>
                  </div>
                </div>
              </InfoPopover>
            </div>

            <div className="flex flex-wrap items-center gap-2 shrink-0">
              <button
                onClick={() => {
                  setContributeDefaultNumber(undefined);
                  setIsContributeModalOpen(true);
                }}
                className="bg-teal-700 hover:bg-teal-800 text-white font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 shadow-2xs transition-all cursor-pointer active:scale-95"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Soru Ekle</span>
              </button>

              <button
                onClick={() => setIsPdfModalOpen(true)}
                className="bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold px-2.5 sm:px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 border border-slate-200 transition-all cursor-pointer"
                title="A4 Sınav Kitapçığını PDF olarak indir"
              >
                <Printer className="w-3.5 h-3.5 text-slate-600" />
                <span className="hidden sm:inline">A4 PDF</span>
              </button>

              {isAdmin && (
                <>
                  <button
                    onClick={() => setIsNotebookLMModalOpen(true)}
                    className="bg-purple-50 hover:bg-purple-100 text-purple-900 border border-purple-200 font-bold px-2 sm:px-2.5 py-1.5 rounded-lg text-xs flex items-center gap-1 shadow-2xs transition-all cursor-pointer active:scale-95"
                    title="NotebookLM & Gemini Kaynak Eşitleme (Yönetici Özel)"
                  >
                    <Brain className="w-3.5 h-3.5 text-purple-700" />
                    <span className="hidden sm:inline">NotebookLM</span>
                  </button>

                  <button
                    onClick={() => setIsPastExamImporterOpen(true)}
                    className="bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold px-2 sm:px-2.5 py-1.5 rounded-lg text-xs flex items-center gap-1 cursor-pointer transition-all active:scale-95"
                    title="Geçmiş yılların çıkmış sorularını yapay zekayla yükle"
                  >
                    <Sparkles className="w-3.5 h-3.5 text-emerald-700" />
                    <span className="hidden sm:inline">Çıkmış Soru Yükle</span>
                    <span className="sm:hidden">Çıkmış Yükle</span>
                  </button>

                  <button
                    onClick={() => setIsAdminPanelOpen(true)}
                    className="bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold px-2.5 sm:px-3 py-1.5 rounded-lg text-xs flex items-center gap-1 shadow-2xs transition-all cursor-pointer active:scale-95 ring-1 ring-amber-500/50"
                    title="MedSoru Yönetici & Otomasyon Kontrol Paneli"
                  >
                    <ShieldCheck className="w-3.5 h-3.5" />
                    <span className="font-extrabold">Admin Paneli</span>
                  </button>
                </>
              )}

              {!isAdmin && (
                <button
                  onClick={() => {
                    setAuthModalInitialMode('admin');
                    setIsAuthModalOpen(true);
                  }}
                  className="bg-slate-900 hover:bg-slate-800 text-amber-300 font-bold px-2.5 sm:px-3 py-1.5 rounded-lg text-xs flex items-center gap-1 shadow-2xs transition-all cursor-pointer active:scale-95 border border-slate-700"
                  title="Yönetici Girişi Yap ve Paneli Aç"
                >
                  <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
                  <span>Admin Paneli</span>
                </button>
              )}
            </div>
          </div>
        )}

        {/* Celebration / Thank You Notification */}
        {congratsToast && (
          <div className="bg-gradient-to-r from-emerald-700 via-teal-800 to-slate-900 text-white rounded-xl p-4.5 shadow-lg flex items-center justify-between gap-3 animate-fadeIn border border-emerald-400">
            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-emerald-500/20 rounded-xl border border-emerald-400/30 text-amber-300 shrink-0">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-sm text-emerald-200">Resmi Teşekkür & Tebrik Bildirimi</h4>
                <p className="text-xs text-white mt-0.5">{congratsToast}</p>
              </div>
            </div>
            <button
              onClick={() => setCongratsToast(null)}
              className="text-emerald-200 hover:text-white text-xs font-semibold px-3 py-1.5 bg-white/10 hover:bg-white/20 rounded-lg transition-colors cursor-pointer shrink-0"
            >
              Tamam
            </button>
          </div>
        )}

        {/* TAB 0: Simple Minimal Quick Add Hero (Default Landing View) */}
        {activeTab === 'quick_add' && (
          <QuickAddHero
            committee={currentCommittee}
            committees={committees}
            onSelectCommittee={(id) => setSelectedCommitteeId(id)}
            onSubmitContribution={handleAddQuestionContribution}
            unassignedCount={questions.filter((q) => q.isUnassignedNumber).length}
            totalQuestionsCount={questions.length}
            onNavigateTab={(tab) => setActiveTab(tab)}
            isAdmin={isAdmin}
            currentUser={currentUser}
            onOpenAdminPanel={() => setIsAdminPanelOpen(true)}
          />
        )}

        {/* TAB 1: Questions List */}
        {activeTab === 'questions' && (
          <div className="space-y-5">
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
              <div className="text-center py-16 bg-white rounded-xl border border-slate-200 shadow-xs">
                <RefreshCw className="w-7 h-7 text-teal-600 animate-spin mx-auto mb-2" />
                <p className="text-xs text-slate-500 font-medium">Soru havuzu yükleniyor...</p>
              </div>
            ) : (filterMyQuestionsOnly ? myQuestions : questions).length === 0 ? (
              <div className="bg-white rounded-xl border border-slate-200 p-12 text-center space-y-4 shadow-xs">
                <div className="w-12 h-12 rounded-xl bg-teal-50 border border-teal-200 text-teal-600 flex items-center justify-center mx-auto">
                  <BookOpen className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900">
                    {filterMyQuestionsOnly ? 'Henüz katkıda bulunduğunuz soru yok' : 'Arama kriterlerine uygun soru bulunamadı'}
                  </h3>
                  <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                    {filterMyQuestionsOnly
                      ? 'Hafızanızdaki soru parçalarını ekleyerek kurul arşivine katkı sağlayabilirsiniz.'
                      : 'Henüz soru girilmemiş olabilir ya da uyguladığınız filtreye uyan soru yok.'}
                  </p>
                </div>
                <div className="flex items-center justify-center gap-2">
                  {filterMyQuestionsOnly && (
                    <button
                      onClick={() => setFilterMyQuestionsOnly(false)}
                      className="text-xs text-slate-600 hover:text-slate-900 px-3 py-1.5 rounded-lg border border-slate-200 cursor-pointer"
                    >
                      Tüm Soruları Göster
                    </button>
                  )}
                  <button
                    onClick={() => {
                      setContributeDefaultNumber(undefined);
                      setIsContributeModalOpen(true);
                    }}
                    className="bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold px-4 py-1.5 rounded-lg cursor-pointer"
                  >
                    İlk Soruyu Ekle
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
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
                    onReconstructWithAi={handleReconstructWithAi}
                    onSetClaimedAnswer={handleSetClaimedAnswer}
                    isReconstructing={!!reconstructingMap[q.id]}
                  />
                ))}
              </div>
            )}
          </div>
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

        {/* TAB 3: Practice & Self Test Mode */}
        {activeTab === 'practice' && (
          <PracticeMode
            questions={questions}
            onOpenContributeModal={() => {
              setContributeDefaultNumber(undefined);
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
      <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500 mt-12 print:hidden">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2 text-slate-700 font-semibold">
            <Stethoscope className="w-4 h-4 text-teal-600" />
            <span>MedSoru • Tıp Dönem 3 Kurul Soru Havuzu & AI Rekonstrüksiyon</span>
          </div>
          <div className="flex items-center gap-4 text-slate-500">
            {currentUser && (
              <span className="text-teal-700 font-medium">
                {currentUser.email} {isAdmin ? '(Yönetici)' : ''}
              </span>
            )}
            <span>Google Drive API v3 & Bulut Arşiv</span>
          </div>
        </div>
      </footer>

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
    </div>
  );
}
