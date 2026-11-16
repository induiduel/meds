/**
 * Rota başına sayfa görünümleri (2026-11-17, App.tsx'ten taşındı — davranış aynı). Durum ve kancalar App'te kalır;
 * bu bileşen App'in verdiği bağlamla (GorunumBaglami) gorunenTab'a göre tembel sayfayı çizer. <main> içinde tek çocuk.
 */
import { guvenliLazy } from '../utils/guvenliLazy';
import KampYonlendir from '../components/v15/ekModul/KampYonlendir';
import React, { Suspense } from 'react';
import type { SearchHit } from '../components/search/searchShared';
import { AppRoute, writeLocation, pathFor, navigateTo } from '../router';
import { bayrak } from '../services/siteAyar';
import { Sparkles, CheckCircle2, ExternalLink } from 'lucide-react';
import { Committee, QuestionItem, QuestionLectureMatch } from '../types';
// Soru havuzu yalnız /sorular'da görünür: açılış paketine (QuestionCard + havuz stilleri) girmesin diye tembel yüklenir.
const PoolView = guvenliLazy(() => import('../components/pool/PoolView').then((m) => ({ default: m.PoolView })));
import { committeeShortLabel } from '../components/quickAddOrtak';
// Soru ekle (ana sayfa) tembel yüklenir (başarım turu 2026-10-20); ana sayfada açılışta hemen istenir.
const quickAddYukle = () => import('../components/QuickAddHero').then((m) => ({ default: m.QuickAddHero }));
if (typeof window !== 'undefined' && /^\/(meds\/?)?$/.test(window.location.pathname)) void quickAddYukle();
const QuickAddHero = guvenliLazy(quickAddYukle);
/** QuickAddHero ile aynı dış kap ve ölçülen yükseklik (1440: 262, 375: 252 px): yüklenirken düzen kaymaz. */
const QuickAddYerTutucu = () => (
  <div className="w-full max-w-[760px] mx-auto lg:mx-0 flex flex-col gap-5 pt-4 sm:pt-8 min-h-[252px] sm:min-h-[262px]" aria-busy="true" />
);
import KurulSeridi from '../components/olasi/KurulSeridi';
import { V15Disinda, V15Icinde } from '../components/v15/V15Disinda';
import { CanliDersDockGate } from '../components/canliDers/CanliDersDockGate';
import { LearnFab } from '../components/learn/LearnFab';
import { PageLoader } from '../components/ui/Animations';
import { toast } from '../components/ui/Toast';

const StudyHub = guvenliLazy(() => import('../components/study/StudyHub').then(m => ({ default: m.StudyHub })));
const BookletView = guvenliLazy(() => import('../components/BookletView').then(m => ({ default: m.BookletView })));
const LeaderboardView = guvenliLazy(() => import('../components/LeaderboardView').then(m => ({ default: m.LeaderboardView })));
const StatsView = guvenliLazy(() => import('../components/stats/StatsView').then(m => ({ default: m.StatsView })));
const FavorilerBugun = guvenliLazy(() => import('../components/v15/FavorilerBugun'));
const TodayView = guvenliLazy(() => import('../components/today/TodayView').then(m => ({ default: m.TodayView })));
const MusicView = guvenliLazy(() => import('../components/MusicView').then(m => ({ default: m.MusicView })));
const LectureNotesView = guvenliLazy(() => import('../components/LectureNotesView').then(m => ({ default: m.LectureNotesView })));
const PastExamsView = guvenliLazy(() => import('../components/PastExamsView').then(m => ({ default: m.PastExamsView })));
const QuestionMatrix = guvenliLazy(() => import('../components/QuestionMatrix').then(m => ({ default: m.QuestionMatrix })));
const LocalAiChatView = guvenliLazy(() => import('../components/LocalAiChatView').then(m => ({ default: m.LocalAiChatView })));
const DataCoreView = guvenliLazy(() => import('../components/core/DataCoreView'));
const TestCikmisView = guvenliLazy(() => import('../components/TestCikmisView').then(m => ({ default: m.TestCikmisView })));
const TesterOzetView = guvenliLazy(() => import('../components/TesterOzetView').then(m => ({ default: m.TesterOzetView })));
const PracticeQuestionsView = guvenliLazy(() => import('../components/PracticeQuestionsView'));
const OncelikliDerslerView = guvenliLazy(() => import('../components/oncelikli/OncelikliDerslerView'));
const KazanimlarView = guvenliLazy(() => import('../components/KazanimlarView').then(m => ({ default: m.KazanimlarView })));
const DiseasesView = guvenliLazy(() => import('../components/diseases/DiseasesView').then(m => ({ default: m.DiseasesView })));
const SaglikView = guvenliLazy(() => import('../components/saglik/SaglikView').then(m => ({ default: m.SaglikView })));
const CanliDersView = guvenliLazy(() => import('../components/canliDers/CanliDersView'));
const PatolojiCheckUp = guvenliLazy(() => import('../components/checkup/PatolojiCheckUp'));
const GenetikCheckUp = guvenliLazy(() => import('../components/checkup/GenetikCheckUp'));
const KmbAsistan = guvenliLazy(() => import('../components/kmb/KmbAsistan'));
const SonProvaView = guvenliLazy(() => import('../components/sonProva/SonProvaView'));
const CikmisCozucuView = guvenliLazy(() => import('../components/cikmisCozucu/CikmisCozucuView'));
const BasarimView = guvenliLazy(() => import('../components/basarim/BasarimView'));
const BitirdiklerimView = guvenliLazy(() => import('../components/takip/BitirdiklerimView'));
const SinavPlaniView = guvenliLazy(() => import('../components/takip/SinavPlaniView'));
const CevrimdisiView = guvenliLazy(() => import('../components/cevrimdisi/CevrimdisiView'));
const OlasiSorularView = guvenliLazy(() => import('../components/olasi/OlasiSorularView'));
const GecmisKurullarView = guvenliLazy(() => import('../components/olasi/GecmisKurullarView'));
const KampView = guvenliLazy(() => import('../components/kamp/KampView'));
const MerkezView = guvenliLazy(() => import('../components/merkez/MerkezView'));
const SoruHaritasiV15 = guvenliLazy(() => import('../components/v15/SoruHaritasiV15'));
const YanlislarimV15 = guvenliLazy(() => import('../components/v15/YanlislarimV15'));
const BildirimlerV15 = guvenliLazy(() => import('../components/v15/BildirimlerV15'));
const MuzikV15 = guvenliLazy(() => import('../components/v15/MuzikV15'));
const ZihinHaritasiV15 = guvenliLazy(() => import('../components/v15/ZihinHaritasiV15'));
const HucremV15 = guvenliLazy(() => import('../components/v15/HucremV15'));
const ToplulukV15 = guvenliLazy(() => import('../components/v15/ToplulukV15'));
const KisiProfilV15 = guvenliLazy(() => import('../components/v15/KisiProfilV15'));
const ArkadaslarV15 = guvenliLazy(() => import('../components/v15/ArkadaslarV15'));
const PdfSihirbaziV15 = guvenliLazy(() => import('../components/v15/PdfSihirbaziV15'));
const NotlarimV15 = guvenliLazy(() => import('../components/v15/NotlarimV15'));
const VideoDersV15 = guvenliLazy(() => import('../components/v15/VideoDersV15'));
const OyunlarV15 = guvenliLazy(() => import('../components/v15/OyunlarV15'));
const MasaView = guvenliLazy(() => import('../components/masa/MasaView'));
const EkModullerV15 = guvenliLazy(() => import('../components/v15/ekModul/EkModullerV15'));
const SoruAktarV15 = guvenliLazy(() => import('../components/v15/SoruAktarV15'));
const DersProgramiV15 = guvenliLazy(() => import('../components/v15/DersProgramiV15'));
const ProgramEkleV15 = guvenliLazy(() => import('../components/v15/ProgramEkleV15'));
const DilBolgeV15 = guvenliLazy(() => import('../components/v15/DilBolgeV15'));
const IlkAdimlarV15 = guvenliLazy(() => import('../components/v15/IlkAdimlarV15'));
const YardimV15 = guvenliLazy(() => import('../components/v15/YardimV15'));
const SinavTakvimiV15 = guvenliLazy(() => import('../components/v15/SinavTakvimiV15'));
const SiralamaV15 = guvenliLazy(() => import('../components/v15/SiralamaV15'));
const DersDetayV15 = guvenliLazy(() => import('../components/v15/DersDetayV15'));
const NeYapmak = guvenliLazy(() => import('../components/merkez/MerkezView').then((m) => ({ default: m.NeYapmak })));
const BulunamadiV15 = guvenliLazy(() => import('../components/v15/BulunamadiV15'));
const GuncellemeGunluguView = guvenliLazy(() => import('../components/guncellemeler/GuncellemeGunluguView'));
const SinavCalismaView = guvenliLazy(() => import('../components/SinavCalismaView').then(m => ({ default: m.SinavCalismaView })));

const ProfileSettingsView = guvenliLazy(() => import('../components/settings/ProfileSettingsView').then(m => ({ default: m.ProfileSettingsView })));
const LectureSummariesView = guvenliLazy(() => import('../components/LectureSummariesView').then(m => ({ default: m.LectureSummariesView })));
const TranscriptionsView = guvenliLazy(() => import('../components/TranscriptionsView').then(m => ({ default: m.TranscriptionsView })));
const FlashcardsView = guvenliLazy(() => import('../components/flashcards/FlashcardsView').then(m => ({ default: m.FlashcardsView })));
const SearchView = guvenliLazy(() => import('../components/search/SearchView').then(m => ({ default: m.SearchView })));
const InteractiveDeckView = guvenliLazy(() => import('../components/learn/InteractiveDeckView').then(m => ({ default: m.InteractiveDeckView })));
const ExamSpotsView = guvenliLazy(() => import('../components/spots/ExamSpotsView').then(m => ({ default: m.ExamSpotsView })));
const AlternatifCozucuView = guvenliLazy(() => import('../components/altCozucu/AlternatifCozucuView').then(m => ({ default: m.default })));
const MedicalEncyclopediaView = guvenliLazy(() => import('../components/encyclopedia/MedicalEncyclopediaView').then(m => ({ default: m.MedicalEncyclopediaView })));

const ViewFallback = () => <PageLoader />;
import type { QuestionFocus } from '../services/questionFocus';
import { AppUser } from '../services/auth';
import { FOLDER_NAME } from '../services/drive';

export type GorunumBaglami = {
  activeTab: AppRoute;
  canliDersKey: string | undefined;
  committees: Committee[];
  completedQuestions: QuestionItem[];
  congratsToast: string | null;
  currentCommittee: Committee | undefined;
  currentUser: AppUser | null;
  deepLinkNonce: number;
  driveUploadSuccess: { fileId: string; fileName: string; webViewLink?: string; } | null;
  emptyQuestions: QuestionItem[];
  fetchQuestions: () => Promise<void>;
  filterMyQuestionsOnly: boolean;
  gatheringQuestions: QuestionItem[];
  gorunenTab: AppRoute;
  handleAddFragment: (questionId: string, text: string, author: string, type: 'stem' | 'clue' | 'option') => Promise<void>;
  handleAddOption: (questionId: string, key: 'A' | 'B' | 'C' | 'D' | 'E', text: string, suggestedBy: string) => Promise<void>;
  handleAddQuestionContribution: (data: { committeeId: string; questionNumber?: number; isUnknownNumber?: boolean; discipline: string; topic: string; fragmentText: string; author: string; authorUid?: string; authorStudentNumber?: string; claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E'; options?: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string; }[]; targetQuestionId?: string; examYear?: string; }) => Promise<{ intakeId: string | null; }>;
  handleDeleteQuestion: (targetQ: QuestionItem) => Promise<void>;
  handleGenerateSlots: () => Promise<void>;
  handleGoogleLogout: () => Promise<void>;
  handleReconstructWithAi: (questionId: string) => Promise<void>;
  handleSetClaimedAnswer: (questionId: string, answer: 'A' | 'B' | 'C' | 'D' | 'E') => Promise<void>;
  handleUpdateQuestionReference: (questionId: string, reference: QuestionLectureMatch) => Promise<void>;
  handleUpvoteFragment: (questionId: string, fragmentId: string) => Promise<void>;
  handleUpvoteOption: (questionId: string, key: 'A' | 'B' | 'C' | 'D' | 'E') => Promise<void>;
  handleUpvoteQuestion: (questionId: string) => Promise<void>;
  isAdmin: boolean;
  isGeneratingSlots: boolean;
  learnLinkNonce: number;
  learnQuestionFocus: QuestionFocus | null;
  loading: boolean;
  myQuestions: QuestionItem[];
  openQuestion: (q: QuestionItem) => void;
  openSearchHit: (hit: SearchHit) => boolean;
  openSummaryId: string | undefined;
  ornekQuestionId: string | undefined;
  pastExamsSearchQuery: string;
  poolFocusQuestion: QuestionItem | undefined;
  poolQuestions: QuestionItem[];
  questions: QuestionItem[];
  reconstructingMap: Record<string, boolean>;
  sayfaGizliMi: boolean;
  sayfaKapaliMi: boolean;
  searchFocusId: string | undefined;
  searchPageQuery: string;
  searchQuery: string;
  selectedCommitteeId: string;
  selectedDiscipline: string;
  selectedDiseaseId: string | undefined;
  selectedGlossaryTermId: string | undefined;
  selectedLearnDeckId: string | undefined;
  selectedLearnSlideNumber: number | undefined;
  selectedOrnekKazanimNo: number | null;
  selectedOrnekLessonId: string | null;
  selectedStatus: string;
  setActiveTab: (tab: AppRoute) => void;
  setAuthModalInitialMode: React.Dispatch<React.SetStateAction<"admin" | "login" | "register">>;
  setClusterFocusId: React.Dispatch<React.SetStateAction<string | null>>;
  setCongratsToast: React.Dispatch<React.SetStateAction<string | null>>;
  setContributeDefaultNumber: React.Dispatch<React.SetStateAction<number | undefined>>;
  setCurrentUser: React.Dispatch<React.SetStateAction<AppUser | null>>;
  setDriveUploadSuccess: React.Dispatch<React.SetStateAction<{ fileId: string; fileName: string; webViewLink?: string; } | null>>;
  setFilterMyQuestionsOnly: React.Dispatch<React.SetStateAction<boolean>>;
  setIsAuthModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsContributeModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsEditQuestionModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsHistoryModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsOfflineModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setIsPdfModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setLearnQuestionFocus: React.Dispatch<React.SetStateAction<QuestionFocus | null>>;
  setOptimizeQuestion: React.Dispatch<React.SetStateAction<QuestionItem | null>>;
  setPastExamsSearchQuery: React.Dispatch<React.SetStateAction<string>>;
  setPdfSlideTarget: React.Dispatch<React.SetStateAction<{ deckId: string; slideNumber: number; } | null>>;
  setPoolFocusId: React.Dispatch<React.SetStateAction<string | undefined>>;
  setSearchPageQuery: React.Dispatch<React.SetStateAction<string>>;
  setSearchQuery: React.Dispatch<React.SetStateAction<string>>;
  setSelectedCommitteeId: React.Dispatch<React.SetStateAction<string>>;
  setSelectedDiscipline: React.Dispatch<React.SetStateAction<string>>;
  setSelectedLearnDeckId: React.Dispatch<React.SetStateAction<string | undefined>>;
  setSelectedLearnSlideNumber: React.Dispatch<React.SetStateAction<number | undefined>>;
  setSelectedOrnekKazanimNo: React.Dispatch<React.SetStateAction<number | null>>;
  setSelectedOrnekLessonId: React.Dispatch<React.SetStateAction<string | null>>;
  setSelectedQuestionForHistory: React.Dispatch<React.SetStateAction<QuestionItem | null>>;
  setSelectedQuestionToEdit: React.Dispatch<React.SetStateAction<QuestionItem | null>>;
  setSelectedStatus: React.Dispatch<React.SetStateAction<string>>;
  setShowClusterModal: React.Dispatch<React.SetStateAction<boolean>>;
  setVisibleCount: React.Dispatch<React.SetStateAction<number>>;
  standaloneQuestions: QuestionItem[];
  targetCount: number;
  visibleCount: number;
};

export function Gorunumler(p: GorunumBaglami) {
  const {
    activeTab,
    canliDersKey,
    committees,
    completedQuestions,
    congratsToast,
    currentCommittee,
    currentUser,
    deepLinkNonce,
    driveUploadSuccess,
    emptyQuestions,
    fetchQuestions,
    filterMyQuestionsOnly,
    gatheringQuestions,
    gorunenTab,
    handleAddFragment,
    handleAddOption,
    handleAddQuestionContribution,
    handleDeleteQuestion,
    handleGenerateSlots,
    handleGoogleLogout,
    handleReconstructWithAi,
    handleSetClaimedAnswer,
    handleUpdateQuestionReference,
    handleUpvoteFragment,
    handleUpvoteOption,
    handleUpvoteQuestion,
    isAdmin,
    isGeneratingSlots,
    learnLinkNonce,
    learnQuestionFocus,
    loading,
    myQuestions,
    openQuestion,
    openSearchHit,
    openSummaryId,
    ornekQuestionId,
    pastExamsSearchQuery,
    poolFocusQuestion,
    poolQuestions,
    questions,
    reconstructingMap,
    sayfaGizliMi,
    sayfaKapaliMi,
    searchFocusId,
    searchPageQuery,
    searchQuery,
    selectedCommitteeId,
    selectedDiscipline,
    selectedDiseaseId,
    selectedGlossaryTermId,
    selectedLearnDeckId,
    selectedLearnSlideNumber,
    selectedOrnekKazanimNo,
    selectedOrnekLessonId,
    selectedStatus,
    setActiveTab,
    setAuthModalInitialMode,
    setClusterFocusId,
    setCongratsToast,
    setContributeDefaultNumber,
    setCurrentUser,
    setDriveUploadSuccess,
    setFilterMyQuestionsOnly,
    setIsAuthModalOpen,
    setIsContributeModalOpen,
    setIsEditQuestionModalOpen,
    setIsHistoryModalOpen,
    setIsOfflineModalOpen,
    setIsPdfModalOpen,
    setLearnQuestionFocus,
    setOptimizeQuestion,
    setPastExamsSearchQuery,
    setPdfSlideTarget,
    setPoolFocusId,
    setSearchPageQuery,
    setSearchQuery,
    setSelectedCommitteeId,
    setSelectedDiscipline,
    setSelectedLearnDeckId,
    setSelectedLearnSlideNumber,
    setSelectedOrnekKazanimNo,
    setSelectedOrnekLessonId,
    setSelectedQuestionForHistory,
    setSelectedQuestionToEdit,
    setSelectedStatus,
    setShowClusterModal,
    setVisibleCount,
    standaloneQuestions,
    targetCount,
    visibleCount,
  } = p;
  return (
    <>

        {/* Bölüm adı üst çubukta görünür (kabuğun grup etiketi); sayfa içinde ayrıca şerit yok (kullanıcı kararı 2026-10-21) */}
        {/* Merkez sayfaları: /dersler · /sorular · /kamplar[/kurulN] · /kaynaklar */}
        {(gorunenTab === 'hub_dersler' || gorunenTab === 'hub_sorular' || gorunenTab === 'hub_kamplar' || gorunenTab === 'hub_kaynaklar') && (
          <Suspense fallback={<ViewFallback />}>
            <MerkezView key={activeTab} kategori={gorunenTab === 'hub_dersler' ? 'dersler' : gorunenTab === 'hub_sorular' ? 'sorular' : gorunenTab === 'hub_kamplar' ? 'kamplar' : 'kaynaklar'} />
          </Suspense>
        )}

        {/* Öğrenciye kapatılan sayfalar (Sınav çalışması, Alternatif çözücü, Ders notları): yalnız yönetici açar */}
        {sayfaKapaliMi && (
          <div className="mz-kapali" role="status">
            <h1>{sayfaGizliMi ? 'Bu sayfa şu an kapalı' : 'Bu sayfa kullanımdan kaldırıldı'}</h1>
            <p>{sayfaGizliMi ? 'Bu bölüm geçici olarak öğrencilere kapatıldı; açıldığında menüde görünecek. Şimdilik ne yapmak istediğini seç:' : 'Aradığın içerik artık yeni bölümlerde. Ne yapmak istediğini seç:'}</p>
            <Suspense fallback={null}><NeYapmak kart /></Suspense>
          </div>
        )}

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
        {gorunenTab === 'quick_add' && <KurulSeridi soruEkleGoster={false} sola />}
        {gorunenTab === 'quick_add' && (
          <Suspense fallback={<QuickAddYerTutucu />}>
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
          </Suspense>
        )}

        {/* TAB: Learn / İnteraktif Ses & Slayt Hub'ı */}
        {gorunenTab === 'learn' && (
          <Suspense fallback={<ViewFallback />}>
            <LearnFab
              onOpenGlossary={() => setActiveTab('glossary')}
              onOpenPdf={() => { setPdfSlideTarget(null); setIsPdfModalOpen(true); }}
            >
            <InteractiveDeckView
              isAdmin={isAdmin}
              initialDeckId={selectedLearnDeckId}
              initialSlideNumber={selectedLearnSlideNumber}
              linkNonce={learnLinkNonce}
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

        {gorunenTab === 'search' && (
          <Suspense fallback={<ViewFallback />}>
            <SearchView
              initialQuery={searchPageQuery}
              focusId={searchFocusId}
              committeeId={selectedCommitteeId}
              onQueryChange={(q) => { setSearchPageQuery(q); writeLocation('search', q || undefined, true); }}
              onOpenSource={(hit) => { openSearchHit(hit); }}
            />
          </Suspense>
        )}

        {/* TAB: Sınav spotları · Soru çözücü (/soru-cozucu) · En önemliler (/en-onemliler) — aynı bileşen, ayrı sayfa */}
        {(gorunenTab === 'spots' || gorunenTab === 'soru_cozucu' || gorunenTab === 'en_onemliler') && (
          <Suspense fallback={<ViewFallback />}>
            <ExamSpotsView key={activeTab} gorunum={gorunenTab === 'soru_cozucu' ? 'cozucu' : gorunenTab === 'en_onemliler' ? 'onem' : 'spot'} />
          </Suspense>
        )}

        {/* TAB: Patoloji alternatif sesli çözücü (/alternatif-cozucu) */}
        {gorunenTab === 'alternatif_cozucu' && !sayfaKapaliMi && (
          <Suspense fallback={<ViewFallback />}>
            <AlternatifCozucuView />
          </Suspense>
        )}

        {/* TAB: Glossary & Encyclopedia / Tıbbi Sözlük & Ansiklopedi */}
        {gorunenTab === 'glossary' && (
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

        {/* TAB: Sesli ders (eski Canlı ders) — sesli dersler, metin + PDF eşzamanlı (/canliders/<key>); oynatıcı aşağıda (CanliDersDockGate) */}
        {gorunenTab === 'canli_ders' && (
          <Suspense fallback={<ViewFallback />}>
            <CanliDersView dersKey={canliDersKey} />
          </Suspense>
        )}

        {/* v15 ders ayrıntısı (/dersler/ders/kurulN/<key>): içerikler + bölümler; v15 dışında sesli derse yönlenir */}
        {gorunenTab === 'ders_detay' && (
          <Suspense fallback={<ViewFallback />}>
            <DersDetayV15 />
          </Suspense>
        )}

        {/* TAB: Sağlık Bakanlığı — resmî halk sağlığı verileri + ders/sınav bağları (/saglik/<bölüm>) */}
        {gorunenTab === 'health_ministry' && (
          <Suspense fallback={<ViewFallback />}>
            <SaglikView />
          </Suspense>
        )}

        {/* TAB: Diseases Atlas / Tıbbi Hastalıklar & Klinik Atlas */}
        {gorunenTab === 'diseases' && (
          <Suspense fallback={<ViewFallback />}>
            <DiseasesView
              currentUser={currentUser}
              initialDiseaseId={selectedDiseaseId}
              onOpenReportModal={(t) => {
                toast.info('Hata Bildirimi Alındı', `${t.title} için bildiriminiz inceleme sırasına eklendi.`);
              }}
            />
          </Suspense>
        )}

        {/* TAB 1: Soru havuzu (v11: components/pool/PoolView) */}
        {gorunenTab === 'questions' && (
          <Suspense fallback={<ViewFallback />}>
          <PoolView
            loading={loading}
            allQuestions={standaloneQuestions}
            poolQuestions={poolQuestions}
            focusQuestion={poolFocusQuestion}
            onClearFocus={() => { setPoolFocusId(undefined); writeLocation('questions'); }}
            visibleCount={visibleCount}
            setVisibleCount={setVisibleCount}
            committees={committees}
            selectedCommitteeId={selectedCommitteeId}
            onSelectCommittee={setSelectedCommitteeId}
            selectedDiscipline={selectedDiscipline}
            onSelectDiscipline={setSelectedDiscipline}
            selectedStatus={selectedStatus}
            onSelectStatus={setSelectedStatus}
            searchQuery={searchQuery}
            onSearchChange={setSearchQuery}
            mineOnly={filterMyQuestionsOnly}
            onSetMineOnly={setFilterMyQuestionsOnly}
            myCount={myQuestions.length}
            stats={{
              target: targetCount,
              gathered: questions.filter((q) => q.fragments.length > 0).length,
              completed: completedQuestions.length,
              gathering: gatheringQuestions.length,
              empty: emptyQuestions.length,
            }}
            isAdmin={isAdmin}
            onGenerateSlots={handleGenerateSlots}
            isGeneratingSlots={isGeneratingSlots}
            onOpenClusters={(clusterId?: string) => { setClusterFocusId(clusterId || null); setShowClusterModal(true); }}
            onContribute={() => {
              setContributeDefaultNumber(undefined);
              setIsContributeModalOpen(true);
            }}
            currentUser={currentUser}
            reconstructingMap={reconstructingMap}
            card={{
              onEditQuestion: (targetQ) => {
                setSelectedQuestionToEdit(targetQ);
                setIsEditQuestionModalOpen(true);
              },
              onDeleteQuestion: handleDeleteQuestion,
              onOpenHistory: (targetQ) => {
                setSelectedQuestionForHistory(targetQ);
                setIsHistoryModalOpen(true);
              },
              onAddFragment: handleAddFragment,
              onUpvoteFragment: handleUpvoteFragment,
              onAddOption: handleAddOption,
              onUpvoteOption: handleUpvoteOption,
              onUpvoteQuestion: handleUpvoteQuestion,
              onReconstructWithAi: handleReconstructWithAi,
              onOpenAiOptimizer: (targetQ) => setOptimizeQuestion(targetQ),
              onSetClaimedAnswer: handleSetClaimedAnswer,
            }}
          />
          </Suspense>
        )}

        {/* Study workspace: solve, self-test, notes */}
        {gorunenTab === 'study' && (
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
        {gorunenTab === 'past_exams' && (
          <Suspense fallback={<ViewFallback />}>
            <PastExamsView
              currentUser={currentUser}
              initialSearchQuery={pastExamsSearchQuery}
              // Ders notları öğrenciye kapalı (merkezModel.KAPALI_SAYFALAR): bağlantı yalnız yöneticide
              onOpenNote={isAdmin ? (noteId, pageNumber) => {
                navigateTo(`${pathFor('notes')}?id=${encodeURIComponent(noteId)}${pageNumber ? `&page=${pageNumber}` : ''}`);
              } : undefined}
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
        {gorunenTab === 'ornek_sorular' && (
          <Suspense fallback={<ViewFallback />}>
            <PracticeQuestionsView
              initialLessonId={selectedOrnekLessonId}
              initialKazanimNo={selectedOrnekKazanimNo}
              initialQuestionId={ornekQuestionId}
            />
          </Suspense>
        )}

        {/* TAB: /sinav-calisma — Tüm kazanımlar ve sesli sınav asistanı */}
        {gorunenTab === 'sinav_calisma' && !sayfaKapaliMi && (
          <Suspense fallback={<ViewFallback />}>
            <SinavCalismaView />
          </Suspense>
        )}

        {/* TAB: /patoloji-check-up — patoloji karşılaştırma tabloları ve kısa notlar */}
        {gorunenTab === 'patoloji_checkup' && (
          <Suspense fallback={<ViewFallback />}>
            <PatolojiCheckUp />
          </Suspense>
        )}

        {/* TAB: /genetik-check-up — TBG sınav kalıbı, tablolar, tek satırlık spotlar, soru-cevap ve çıkmış/örnek sorular */}
        {gorunenTab === 'genetik_checkup' && (
          <Suspense fallback={<ViewFallback />}>
            <GenetikCheckUp />
          </Suspense>
        )}

        {/* TAB: /kmb (görünen /kamplar/kmb/…) — KMB görsel sesli asistan: önce öğret, sonra vaka sınavı */}
        {gorunenTab === 'kmb_asistan' && (
          <Suspense fallback={<ViewFallback />}>
            <KmbAsistan />
          </Suspense>
        )}

        {/* TAB: /basarimlar — hedefler, başarımlar, ATP ve kilitler */}
        {gorunenTab === 'basarimlar' && (
          <Suspense fallback={<ViewFallback />}>
            <BasarimView />
          </Suspense>
        )}

        {/* TAB: /yanlislarim (görünen /sorular/yanlislarim) — soru tekrar defteri (services/yanlislarim) */}
        {gorunenTab === 'yanlislarim' && (
          <Suspense fallback={<ViewFallback />}>
            <YanlislarimV15 />
          </Suspense>
        )}

        {/* TAB: /bildirimler — bildirim merkezi (tasarım A06): hesap bildirimleri + gerçek veriden türeyen hatırlatmalar */}
        {gorunenTab === 'bildirimler' && (
          <Suspense fallback={<ViewFallback />}>
            <BildirimlerV15 />
          </Suspense>
        )}

        {/* TAB: /zihin-haritasi (görünen /dersler/zihin-haritasi) — ders bölümleri + anahtar terimler */}
        {gorunenTab === 'zihin_haritasi' && (
          <Suspense fallback={<ViewFallback />}>
            <ZihinHaritasiV15 />
          </Suspense>
        )}

        {/* TAB: /hucrem — ATP ile 28 evrim basamağı (başarım kilitleri tur: hucre) */}
        {gorunenTab === 'hucrem' && (
          <Suspense fallback={<ViewFallback />}>
            <HucremV15 />
          </Suspense>
        )}

        {/* TAB: /topluluk — sohbet kanalları ve ders yorumları (services/topluluk.ts, SSE topluluk) */}
        {gorunenTab === 'topluluk' && (
          <Suspense fallback={<ViewFallback />}>
            <ToplulukV15 />
          </Suspense>
        )}

        {/* TAB: /kisi/<kimlik> açık profil, /arkadaslar arkadaş listesi (services/arkadaslik.ts) */}
        {gorunenTab === 'kisi' && (
          <Suspense fallback={<ViewFallback />}>
            <KisiProfilV15 />
          </Suspense>
        )}
        {gorunenTab === 'arkadaslar' && (
          <Suspense fallback={<ViewFallback />}>
            <ArkadaslarV15 />
          </Suspense>
        )}

        {/* TAB: /pdf-olustur — PDF oluştur sihirbazı (kaynak → kurul → dersler; ortak TopluPdf penceresi) */}
        {gorunenTab === 'pdf_olustur' && (
          <Suspense fallback={<ViewFallback />}>
            <PdfSihirbaziV15 />
          </Suspense>
        )}

        {/* TAB: /notlarim — kişisel notlar + kalem/fosforlu çizim (userKvSync ile hesaba eşitlenir) */}
        {gorunenTab === 'notlarim' && (
          <Suspense fallback={<ViewFallback />}>
            <NotlarimV15 />
          </Suspense>
        )}

        {/* TAB: /video-ders — hazır ders videoları (yönetici GPU kuyruğundan; oynat, tam ekran, resim içinde resim) */}
        {gorunenTab === 'video_ders' && (
          <Suspense fallback={<ViewFallback />}>
            <VideoDersV15 />
          </Suspense>
        )}

        <KampYonlendir />

        {/* TAB: /ek-moduller (görünen /dersler/ek-moduller/kurul<N>/<modül>/…) — seçmeli/geçici ders modülleri */}
        {gorunenTab === 'ek_moduller' && (
          <Suspense fallback={<ViewFallback />}>
            <EkModullerV15 />
          </Suspense>
        )}

        {/* TAB: /soru-aktar (görünen /sorular/disa-aktar) — soru dışa aktarıcı (PDF/DOCX/PPTX) */}
        {gorunenTab === 'soru_aktar' && (
          <Suspense fallback={<ViewFallback />}>
            <SoruAktarV15 />
          </Suspense>
        )}

        {/* TAB: /oyunlar (görünen /sorular/oyunlar) — canlı soru yarışması (/api/quiz/ws) */}
        {gorunenTab === 'oyunlar' && (
          <Suspense fallback={<ViewFallback />}>
            {/* Taş Masası (okey taşlı oyunlar + Uno) Oyunlar'ın ana içeriğidir; eski soru yarışmaları `oyun_eski` bayrağı ya da ?eski=1 ile */}
            {bayrak('oyun_eski', false) || new URLSearchParams(window.location.search).has('eski') ? <OyunlarV15 /> : <MasaView />}
          </Suspense>
        )}

        {/* TAB: /soru-haritasi (görünen /sorular/soru-haritasi) — kurul × ders × yıl çıkmış soru sayıları */}
        {gorunenTab === 'soru_haritasi' && (
          <Suspense fallback={<ViewFallback />}>
            <SoruHaritasiV15 />
          </Suspense>
        )}

        {/* TAB: /program (görünen /dersler/program) — kurulun ders programı: gün / hafta / liste */}
        {gorunenTab === 'ders_programi' && (
          <Suspense fallback={<ViewFallback />}>
            <DersProgramiV15 />
          </Suspense>
        )}

        {/* TAB: /program-ekle (görünen /dersler/program/ekle) — kişisel etkinlik ekleme + hazır sınıf programı */}
        {gorunenTab === 'program_ekle' && (<Suspense fallback={<ViewFallback />}><ProgramEkleV15 /></Suspense>)}
        {/* TAB: /arka-plan — süren indirmeler, video dışa aktarımı, eşitleme */}
        {/* H307: eski rota da birleşik sayfayı açar (adres siteHaritasi'nda /cevrimdisi#isler'e döner) */}
        {gorunenTab === 'arka_plan' && (<Suspense fallback={<ViewFallback />}><CevrimdisiView /></Suspense>)}
        {/* TAB: /dil-bolge — tarih/saat biçimi, haftanın ilk günü (cihaz tercihi) */}
        {gorunenTab === 'dil_bolge' && (<Suspense fallback={<ViewFallback />}><DilBolgeV15 /></Suspense>)}
        {/* TAB: /ilk-adimlar — başlangıç görevleri */}
        {gorunenTab === 'ilk_adimlar' && (<Suspense fallback={<ViewFallback />}><IlkAdimlarV15 /></Suspense>)}
        {/* TAB: /yardim — yardım merkezi */}
        {gorunenTab === 'yardim' && (<Suspense fallback={<ViewFallback />}><YardimV15 /></Suspense>)}

        {/* TAB: /takvim (görünen /kamplar/takvim) — kurul sınavları, final, bütünleme ve kalan gün */}
        {gorunenTab === 'sinav_takvimi' && (
          <Suspense fallback={<ViewFallback />}>
            <SinavTakvimiV15 />
          </Suspense>
        )}

        {/* TAB: /sinav-plani (görünen /kamplar/sinav-plani) — en az 60 için kişiye özel yol haritası */}
        {gorunenTab === 'sinav_plani' && (
          <Suspense fallback={<ViewFallback />}>
            <SinavPlaniView />
          </Suspense>
        )}

        {/* TAB: /bitirdiklerim — konu konu kontrol listesi, süre, soru ve kalan tahmini */}
        {gorunenTab === 'bitirdiklerim' && (
          <Suspense fallback={<ViewFallback />}>
            <BitirdiklerimView />
          </Suspense>
        )}

        {/* TAB: /olasi-sorular — sınav sonrası hatıralardan kurulan olası sorular (?kurul=N) */}
        {gorunenTab === 'olasi_sorular' && (
          <Suspense fallback={<ViewFallback />}>
            <OlasiSorularView uid={currentUser?.uid} />
          </Suspense>
        )}

        {/* TAB: /gecmis-kurullar — sınavı geçmiş kurulların içeriğine bağlantılar */}
        {gorunenTab === 'gecmis_kurullar' && (
          <Suspense fallback={<ViewFallback />}>
            <GecmisKurullarView />
          </Suspense>
        )}

        {/* TAB: /son-prova — Son Prova: kurulun tüm dersleri sesli özet partları, aşama soruları, check-up, 3 deneme (yolu kendisi okur) */}
        {gorunenTab === 'son_prova' && (
          <Suspense fallback={<ViewFallback />}>
            <SonProvaView />
          </Suspense>
        )}

        {/* TAB: /cikmis-cozucu — Sınava hazırlan › Çıkmış çözücü: branş başına sınav soru sayısı kadar çıkmış paketi, sesli çözücüyle */}
        {gorunenTab === 'cikmis_cozucu' && (
          <Suspense fallback={<ViewFallback />}>
            <CikmisCozucuView />
          </Suspense>
        )}

        {/* TAB: /kamp — kurul kampları; /kamp/<kurul>/<brans> tek kamp (yolu kendisi okur) */}
        {gorunenTab === 'kamp' && (
          <Suspense fallback={<ViewFallback />}>
            <KampView />
          </Suspense>
        )}

        {/* AB16: bilinmeyen adres — gerçek 404 ekranı */}
        {gorunenTab === 'bulunamadi' && (
          <Suspense fallback={<ViewFallback />}>
            <BulunamadiV15 />
          </Suspense>
        )}

        {/* TAB: /guncellemeler — sürüm sürüm eklenen / değişen / düzeltilen / kaldırılanlar + geliştirme notları */}
        {gorunenTab === 'guncellemeler' && (
          <Suspense fallback={<ViewFallback />}>
            <GuncellemeGunluguView />
          </Suspense>
        )}

        {/* TAB: /cevrimdisi — çevrimdışı merkezi: ders paketlerini indir, güncelle, sil */}
        {gorunenTab === 'cevrimdisi' && (
          <Suspense fallback={<ViewFallback />}>
            <CevrimdisiView />
          </Suspense>
        )}

        {/* TAB: /oncelikli-dersler — az ezber / mantık / çıkmış analizine göre sesli ders önceliği */}
        {gorunenTab === 'oncelikli_dersler' && (
          <Suspense fallback={<ViewFallback />}>
            <OncelikliDerslerView />
          </Suspense>
        )}

        {/* TAB: /kazanimlar — müfredat ve kazanımlar haritası */}
        {gorunenTab === 'kazanimlar' && (
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
        {gorunenTab === 'test_cikmis' && (
          <Suspense fallback={<ViewFallback />}>
            <TestCikmisView
              currentUser={currentUser}
              isAdmin={isAdmin}
              onBackToPastExams={() => setActiveTab('past_exams')}
            />
          </Suspense>
        )}

        {/* TAB: /tester/ozet — 2026-2027 Ders Notları Test Laboratuvarı */}
        {gorunenTab === 'tester_ozet' && (
          <Suspense fallback={<ViewFallback />}>
            <TesterOzetView />
          </Suspense>
        )}

        {/* TAB 2: 1-100 Question Matrix */}
        {gorunenTab === 'matrix' && (
          <Suspense fallback={<ViewFallback />}>
            <QuestionMatrix
              questions={questions}
              targetCount={targetCount}
              committee={currentCommittee}
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
        {gorunenTab === 'booklet' && (
          <Suspense fallback={<ViewFallback />}>
            <BookletView
              committee={currentCommittee}
              questions={questions}
              onOpenPdfModal={() => setIsPdfModalOpen(true)}
            />
          </Suspense>
        )}

        {/* TAB 5: Leaderboard / Katkı Sıralaması */}
        {/* /bugun — günlük giriş: kaldığın yer, hızlı erişim, günün spotu, haftalık çalışma */}
        {gorunenTab === 'today' && (
          <Suspense fallback={<ViewFallback />}>
            <V15Disinda>
              <KurulSeridi />
              <div className="mz-bugun"><NeYapmak kart /></div>
            </V15Disinda>
            <TodayView committeeLabel={currentCommittee ? committeeShortLabel(currentCommittee) : undefined} onGo={(r) => setActiveTab(r)} />
            <FavorilerBugun />
          </Suspense>
        )}
        {gorunenTab === 'stats' && (
          <Suspense fallback={<ViewFallback />}>
            <StatsView questions={questions} currentUser={currentUser} onGo={(r) => setActiveTab(r)} />
          </Suspense>
        )}
        {gorunenTab === 'leaderboard' && (
          <Suspense fallback={<ViewFallback />}>
            <V15Icinde><SiralamaV15 /></V15Icinde>
            <V15Disinda><LeaderboardView
              questions={questions}
              committees={committees}
              selectedCommitteeId={selectedCommitteeId}
              onSelectCommittee={(id) => setSelectedCommitteeId(id)}
              currentUser={currentUser}
              onOpenContributeModal={() => {
                setContributeDefaultNumber(undefined);
                setIsContributeModalOpen(true);
              }}
            /></V15Disinda>
          </Suspense>
        )}

        {/* Profil ve ayarlar: kimlik, tema × palet, yoğunluk, klasik tasarım */}
        {gorunenTab === 'settings' && (
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
        {gorunenTab === 'music' && (
          <Suspense fallback={<ViewFallback />}>
            <V15Icinde><MuzikV15 /></V15Icinde>
            <V15Disinda><MusicView isAdmin={isAdmin} /></V15Disinda>
          </Suspense>
        )}

        {/* TAB 6: Ders Notları & Slaytlar */}
        {gorunenTab === 'notes' && !sayfaKapaliMi && (
          <Suspense fallback={<ViewFallback />}>
            <LectureNotesView
              key={deepLinkNonce}
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
        {gorunenTab === 'summaries' && (
          <Suspense fallback={<ViewFallback />}>
            <LectureSummariesView onOpenPdfModal={() => setIsPdfModalOpen(true)} initialSummaryId={openSummaryId} />
          </Suspense>
        )}

        {/* TAB 8: Amfi Ses Kaydı Transkriptleri */}
        {gorunenTab === 'transcripts' && (
          <Suspense fallback={<ViewFallback />}>
            <TranscriptionsView />
          </Suspense>
        )}

        {/* /veri — MeDSor Core v2 Veri Merkezi (salt okunur) */}
        {gorunenTab === 'datacore' && (
          <Suspense fallback={<ViewFallback />}>
            <DataCoreView />
          </Suspense>
        )}

        {/* /kartlar — spaced-repetition flashcards (medical terms + lesson cards) */}
        {gorunenTab === 'flashcards' && (
          <Suspense fallback={<ViewFallback />}>
            <FlashcardsView key={deepLinkNonce} />
          </Suspense>
        )}

        {/* /asistan — Local AI & Cloud Medical Assistant / Question Detective */}
        {gorunenTab === 'ai_chat' && (
          <Suspense fallback={<ViewFallback />}>
            <LocalAiChatView
              currentUser={currentUser}
              isAdmin={isAdmin}
              onNavigateToQuestion={(qId) => navigateTo(`${pathFor('past_exams')}/${encodeURIComponent(qId)}`)}
            />
          </Suspense>
        )}


    </>
  );
}
