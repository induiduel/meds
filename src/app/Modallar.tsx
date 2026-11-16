/**
 * Uygulama modalları (2026-11-17, App.tsx'ten taşındı — davranış aynı). Durum App'te kalır; bu bileşen yalnız
 * App'in verdiği bağlamla (ModalBaglami) koşullu modalları çizer. Her modal tembel parça (guvenliLazy).
 */
import { guvenliLazy } from '../utils/guvenliLazy';
import React, { Suspense } from 'react';
import { AppRoute } from '../router';
import { Committee, QuestionItem } from '../types';
import { toast } from '../components/ui/Toast';
import { offlineDatabaseService } from '../services/offlineDatabaseService';

const ExamPdfModal = guvenliLazy(() => import('../components/ExamPdfModal').then(m => ({ default: m.ExamPdfModal })));
const ContributeModal = guvenliLazy(() => import('../components/ContributeModal').then(m => ({ default: m.ContributeModal })));
const AddCommitteeModal = guvenliLazy(() => import('../components/AddCommitteeModal').then(m => ({ default: m.AddCommitteeModal })));
const DriveSaveModal = guvenliLazy(() => import('../components/DriveSaveModal').then(m => ({ default: m.DriveSaveModal })));
const UserAuthModal = guvenliLazy(() => import('../components/UserAuthModal').then(m => ({ default: m.UserAuthModal })));
const EditMyQuestionModal = guvenliLazy(() => import('../components/EditMyQuestionModal').then(m => ({ default: m.EditMyQuestionModal })));
const RevisionHistoryModal = guvenliLazy(() => import('../components/RevisionHistoryModal').then(m => ({ default: m.RevisionHistoryModal })));
const AdminPastExamImporterModal = guvenliLazy(() => import('../components/AdminPastExamImporterModal').then(m => ({ default: m.AdminPastExamImporterModal })));
const AiQuestionOptimizerModal = guvenliLazy(() => import('../components/AiQuestionOptimizerModal').then(m => ({ default: m.AiQuestionOptimizerModal })));
const NotebookLMSyncModal = guvenliLazy(() => import('../components/NotebookLMSyncModal').then(m => ({ default: m.NotebookLMSyncModal })));
const SubagentMonitorModal = guvenliLazy(() => import('../components/SubagentMonitorModal').then(m => ({ default: m.SubagentMonitorModal })));
const SystemDiagnosticsModal = guvenliLazy(() => import('../components/SystemDiagnosticsModal').then(m => ({ default: m.SystemDiagnosticsModal })));
const OfflineDatabaseModal = guvenliLazy(() => import('../components/pwa/OfflineDatabaseModal').then(m => ({ default: m.OfflineDatabaseModal })));
const PwaInstallWelcomeModal = guvenliLazy(() => import('../components/pwa/PwaInstallWelcomeModal').then(m => ({ default: m.PwaInstallWelcomeModal })));
const PwaInstallGuideModal = guvenliLazy(() => import('../components/pwa/PwaInstallGuideModal').then(m => ({ default: m.PwaInstallGuideModal })));
const QuestionClusterAutomationModal = guvenliLazy(() => import('../components/admin/QuestionClusterAutomationModal').then(m => ({ default: m.QuestionClusterAutomationModal })));

import { ADMIN_EMAIL, AppUser } from '../services/auth';

export type ModalBaglami = {
  accessToken: string | null;
  activeTab: AppRoute;
  authModalInitialMode: "admin" | "login" | "register";
  clusterFocusId: string | null;
  committees: Committee[];
  contributeDefaultNumber: number | undefined;
  currentCommittee: Committee | undefined;
  currentUser: AppUser | null;
  fetchQuestions: () => Promise<void>;
  handleAddCommittee: (data: { name: string; year: number; term: string; targetCount: number; description: string; }) => Promise<void>;
  handleAddQuestionContribution: (data: { committeeId: string; questionNumber?: number; isUnknownNumber?: boolean; discipline: string; topic: string; fragmentText: string; author: string; authorUid?: string; authorStudentNumber?: string; claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E'; options?: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string; }[]; targetQuestionId?: string; examYear?: string; }) => Promise<{ intakeId: string | null; }>;
  handleAuthSuccess: (user: AppUser, token?: string | null) => void;
  isAdmin: boolean;
  isAuthModalOpen: boolean;
  isContributeModalOpen: boolean;
  isDiagnosticsOpen: boolean;
  isDriveModalOpen: boolean;
  isEditQuestionModalOpen: boolean;
  isHistoryModalOpen: boolean;
  isNewCommitteeModalOpen: boolean;
  isNotebookLMModalOpen: boolean;
  isOfflineModalOpen: boolean;
  isPastExamImporterOpen: boolean;
  isPdfModalOpen: boolean;
  isPwaWelcomeOpen: boolean;
  isSubagentMonitorOpen: boolean;
  optimizeQuestion: QuestionItem | null;
  pdfSlideTarget: { deckId: string; slideNumber: number; } | null;
  questions: QuestionItem[];
  selectedCommitteeId: string;
  selectedQuestionForHistory: QuestionItem | null;
  selectedQuestionToEdit: QuestionItem | null;
  setActiveTab: (tab: AppRoute) => void;
  setDriveUploadSuccess: React.Dispatch<React.SetStateAction<{ fileId: string; fileName: string; webViewLink?: string; } | null>>;
  setIsAuthModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsContributeModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsDiagnosticsOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsDriveModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsEditQuestionModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsHistoryModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsNewCommitteeModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsNotebookLMModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsOfflineModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsPastExamImporterOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsPdfModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsPwaWelcomeOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsSubagentMonitorOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setOptimizeQuestion: React.Dispatch<React.SetStateAction<QuestionItem | null>>;
  setPdfSlideTarget: React.Dispatch<React.SetStateAction<{ deckId: string; slideNumber: number; } | null>>;
  setQuestions: React.Dispatch<React.SetStateAction<QuestionItem[]>>;
  setSelectedQuestionForHistory: React.Dispatch<React.SetStateAction<QuestionItem | null>>;
  setSelectedQuestionToEdit: React.Dispatch<React.SetStateAction<QuestionItem | null>>;
  setShowClusterModal: React.Dispatch<React.SetStateAction<boolean>>;
  showClusterModal: boolean;
  showOnboarding: boolean;
};

export function Modallar(p: ModalBaglami) {
  const {
    accessToken,
    activeTab,
    authModalInitialMode,
    clusterFocusId,
    committees,
    contributeDefaultNumber,
    currentCommittee,
    currentUser,
    fetchQuestions,
    handleAddCommittee,
    handleAddQuestionContribution,
    handleAuthSuccess,
    isAdmin,
    isAuthModalOpen,
    isContributeModalOpen,
    isDiagnosticsOpen,
    isDriveModalOpen,
    isEditQuestionModalOpen,
    isHistoryModalOpen,
    isNewCommitteeModalOpen,
    isNotebookLMModalOpen,
    isOfflineModalOpen,
    isPastExamImporterOpen,
    isPdfModalOpen,
    isPwaWelcomeOpen,
    isSubagentMonitorOpen,
    optimizeQuestion,
    pdfSlideTarget,
    questions,
    selectedCommitteeId,
    selectedQuestionForHistory,
    selectedQuestionToEdit,
    setActiveTab,
    setDriveUploadSuccess,
    setIsAuthModalOpen,
    setIsContributeModalOpen,
    setIsDiagnosticsOpen,
    setIsDriveModalOpen,
    setIsEditQuestionModalOpen,
    setIsHistoryModalOpen,
    setIsNewCommitteeModalOpen,
    setIsNotebookLMModalOpen,
    setIsOfflineModalOpen,
    setIsPastExamImporterOpen,
    setIsPdfModalOpen,
    setIsPwaWelcomeOpen,
    setIsSubagentMonitorOpen,
    setOptimizeQuestion,
    setPdfSlideTarget,
    setQuestions,
    setSelectedQuestionForHistory,
    setSelectedQuestionToEdit,
    setShowClusterModal,
    showClusterModal,
    showOnboarding,
  } = p;
  return (
    <>
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
              throw new Error('Google ile giriş kaldırıldı. PDF\'i indirip istediğin yere kaydedebilirsin.');
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

      {/* Çevrimdışı Veritabanı & PWA Yönetim Modalı */}
      {isOfflineModalOpen && (
        <Suspense fallback={null}>
          <OfflineDatabaseModal
            isOpen={isOfflineModalOpen}
            onClose={() => setIsOfflineModalOpen(false)}
            isAdmin={isAdmin}
          />
        </Suspense>
      )}

      {/* PWA & Çevrimdışı Veritabanı Açılış Önerisi Modalı */}
      {isPwaWelcomeOpen && !isAdmin && !offlineDatabaseService.getState().isDatabaseDownloaded && (
        <Suspense fallback={null}>
          <PwaInstallWelcomeModal
            isOpen={true}
            onClose={() => setIsPwaWelcomeOpen(false)}
            onOpenOfflineDatabase={() => setIsOfflineModalOpen(true)}
          />
        </Suspense>
      )}
      <Suspense fallback={null}><PwaInstallGuideModal /></Suspense>

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
      {showClusterModal && (
        <Suspense fallback={null}>
          <QuestionClusterAutomationModal
            isOpen={showClusterModal}
            onClose={() => setShowClusterModal(false)}
            currentUser={currentUser}
            isAdmin={isAdmin}
            committeeId={activeTab === 'questions' ? selectedCommitteeId : undefined}
            focusClusterId={clusterFocusId}
          />
        </Suspense>
      )}

    </>
  );
}
