import { fetchMyAccess, setModeratorMode } from './services/moderatorSession';
import { guvenliLazy } from './utils/guvenliLazy';
import { Gorunumler } from './app/Gorunumler';
import { Modallar } from './app/Modallar';
import { manageKabugu, yonetimGirisineGec } from './app/rota';
import { getAppearance } from './utils/appearance';
import { useState, useEffect, useMemo, useCallback, useRef, useLayoutEffect, Suspense } from 'react';
import { startLiveDataSync } from './services/liveDataSync';
import { logActivity } from './services/activityLog';
import { getVoterId, toggledVote } from './utils/voterId';
import { foldTurkish } from './utils/fuzzyMatching';
import type { SearchHit } from './components/search/searchShared';
import { AppRoute, parseLocation, writeLocation, pathFor, icPathFor, ROUTE_TITLES, deepLinkIdFor, navigateTo } from './router';
import { icKonum, kanonik } from './siteHaritasi';
import { sayfaKapali, sayfaYonlendir, useSiteAyar, yoneticiAyarla } from './services/siteAyar';
import { ShieldCheck } from 'lucide-react';
import { Committee, QuestionItem, QuestionLectureMatch } from './types';
import { questionStemText } from './components/quickAddOrtak';
import { V15Icinde } from './components/v15/V15Disinda';
// Kronometre/kapsül yüzen penceresi kapalıyken hiçbir şey çizmez: kodu ve stili açılıştan sonra gelsin.
const KronometreTembel = guvenliLazy(() => import('./components/v15/KronometreV15'));
const KronometreV15 = () => <Suspense fallback={null}><KronometreTembel /></Suspense>;
import { ProfilKurulumKapisi } from './components/v15/ProfilKurulumV15';
import { MusicPlayerProvider } from './components/music/MusicPlayerContext';
import { MiniMusicPlayer } from './components/music/MiniMusicPlayer';
import { SideNav } from './components/shell/SideNav';
import { TopBar } from './components/shell/TopBar';
import { ScrollTopFab } from './components/shell/ScrollTopFab';
import { TamEkranGezinme } from './components/shell/TamEkranGezinme';
import { TabBar } from './components/shell/TabBar';
import { CanliDersDockGate } from './components/canliDers/CanliDersDockGate';
import { CdVideoRozet } from './components/canliDers/CdVideoRozet';
import { ConfirmHost, confirmDialog } from './components/ui/ConfirmDialog';
const WelcomeTour = guvenliLazy(() => import('./components/onboarding/WelcomeTour'));
const TanitimVideo = guvenliLazy(() => import('./components/onboarding/TanitimVideo'));
const GirisUyarisi = guvenliLazy(() => import('./components/onboarding/GirisUyarisi'));
import { PageLoader } from './components/ui/Animations';
import { ToastHost, toast } from './components/ui/Toast';
import { TooltipHost } from './components/ui/TooltipHost';
import { useCevrimiciDurum } from './app/hooks/useCevrimiciDurum';
import { useTurVeTanitim } from './app/hooks/useTurVeTanitim';
import { pwaService, PWA_WELCOME_STORAGE_KEY } from './services/pwaService';
import { userNotificationService } from './services/userNotificationService';
import { backupUserDataToDatabase } from './services/userDataSyncService';
import { syncNotes } from './services/notesSync';
import { buildDeepLinkUrl, executeDeepLinkFocus, initDeepLinkAutoScroll, openDeepLink } from './services/universalRedirectService';

// Lazy-loaded Views (Split into separate on-demand chunks)
// Test çöz: kurulum (kaynak/kurul/ders/zorluk/sayı ya da rastgele) + çözücü; havuz soruları girmez
const TestHub = guvenliLazy(() => import('./components/practice/TestHub').then(m => ({ default: m.TestHub })));
const BasarimKatmani = guvenliLazy(() => import('./components/basarim/BasarimKatmani'));
// Arzu'ya özel katman: yalnız arzuKimlik.ts'teki hesaplarda yüklenir (karşılama, gezinen tilki, kalpler)
import { arzuHesabiMi, useArzuAcik } from './components/arzu/arzuKimlik';
const ArzuKatmani = guvenliLazy(() => import('./components/arzu/ArzuKatmani'));
const DuyuruBandi = guvenliLazy(() => import('./components/system/DuyuruBandi'));

const ManageV16 = guvenliLazy(() => import('./components/manage16/ManageV16'));
const ManageConsole = guvenliLazy(() => import('./components/manage/ManageConsole').then(m => ({ default: m.ManageConsole })));
// Giriş kapısı (yalnız oturumsuz) ve kurulum rehberi (olayla açılır) açılış paketine girmez; ikisi OnboardingV12'yi de çeker.
const Onboarding = guvenliLazy(() => import('./components/onboarding/Onboarding').then(m => ({ default: m.Onboarding })));

const ViewFallback = () => <PageLoader />;
import { GlossaryProvider } from './components/learn/MedicalGlossaryPopover';
import { systemHealthMonitor } from './services/systemHealthMonitor';
import { ApiService } from './services/api';
import type { QuestionFocus } from './services/questionFocus';
import { multiDbManager } from './services/multiDbManager';
import {
  initAuth,
  logout,
  isAdminUser,
  ADMIN_EMAIL,
  getLocalAdminSession,
  setLocalAdminSession,
  clearLocalAdminSession,
  safeStorage,
  updateUserProfileData,
  AppUser,
} from './services/auth';
import { isAdminAppMode, getStoredPanelSecret, setStoredPanelSecret } from './config/deployment';
import { getDefaultActiveCommitteeId, filterCurrent2026_2027Committees } from './services/firestoreDb';
import { uploadBookletPdfToDrive, evaluateAutoBackupThreshold, ThresholdStatus } from './services/drive';

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
        if ((/^manage\./i.test(window.location.hostname) || isAdminAppMode()) && parsed.route === 'quick_add') {
          return { route: 'manage' as ValidAppTab, param: undefined as string | undefined };
        }
      }
    } catch {}
    return parsed;
  });
  const [activeTab, setActiveTabState] = useState<ValidAppTab>(initialRoute.route);
  // Havuz derin bağlantısı: /sorular/<soruId> — o soru listenin başında gösterilir ve odaklanır.
  const clearDeepLinkTargets = useRef<() => void>(() => {});
  const [poolFocusId, setPoolFocusId] = useState<string | undefined>(initialRoute.route === 'questions' ? initialRoute.param : undefined);
  // Canlı ders: /canliders/<key> (yoksa liste)
  const [canliDersKey, setCanliDersKey] = useState<string | undefined>(initialRoute.route === 'canli_ders' ? initialRoute.param : undefined);
  const setActiveTab = useCallback((tab: ValidAppTab) => {
    setActiveTabState(tab);
    // Menüden düz geçiş: önceki derin bağlantının hedefi (terim/hastalık/örnek soru) yeniden açılmasın.
    clearDeepLinkTargets.current();
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
  const [isDriveModalOpen, setIsDriveModalOpen] = useState(false);
  const [isPdfModalOpen, setIsPdfModalOpen] = useState(false);
  const [pdfSlideTarget, setPdfSlideTarget] = useState<{ deckId: string; slideNumber: number } | null>(null);
  const [isPastExamImporterOpen, setIsPastExamImporterOpen] = useState(false);
  const [isNotebookLMModalOpen, setIsNotebookLMModalOpen] = useState(false);
  const [isSubagentMonitorOpen, setIsSubagentMonitorOpen] = useState(false);
  const [isDiagnosticsOpen, setIsDiagnosticsOpen] = useState(false);
  const [isOfflineModalOpen, setIsOfflineModalOpen] = useState(false);
  const { isOnline } = useCevrimiciDurum();
  const [contributeDefaultNumber, setContributeDefaultNumber] = useState<number | undefined>(undefined);

  // User Auth & Profile Modals - İlk girişte kayıt/tanıtım ekranını zorunlu tut
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(() => {
    try {
      const existingAdmin = getLocalAdminSession();
      if (existingAdmin && existingAdmin.email?.toLowerCase() === ADMIN_EMAIL.toLowerCase()) {
        return false;
      }
      const savedUser = safeStorage.getItem('medsoru_user_registered');
      try { if (sessionStorage.getItem('medsoru_tanitim_kapatildi')) return false; } catch { /* özel pencere */ }
      return !savedUser;
    } catch {
      return false;
    }
  });
  // İlk açılış: HTML splash ekranı (metinsiz atan kalp + EKG "A") ilk andan itibaren görünür; React hazır olunca tek hamlede solar
  const [showOnboarding, setShowOnboarding] = useState(() => {
    try { if (sessionStorage.getItem('medsoru_tanitim_kapatildi')) return false; } catch { /* özel pencere */ }
    return isAuthModalOpen;
  });
  const [isPwaWelcomeOpen, setIsPwaWelcomeOpen] = useState(false);
  const [showClusterModal, setShowClusterModal] = useState(false);
  const [clusterFocusId, setClusterFocusId] = useState<string | null>(null);

  useEffect(() => {
    const el = document.getElementById('app-splash');
    if (el) {
      const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
      // H484 (2026-11-04): atan kalp her yeni sekmede 5 sn zorunlu bekletiyordu (sessionStorage) → açılış yavaş algılanıyordu.
      // Artık gösteri yalnız günün ilk açılışında ve en çok ~1,8 sn (imza çizimi görünür); o gün sonraki açılışlarda ve
      // yenilemede uygulama hazır olunca hemen kalkar. Klasik (v10) tasarım eski davranışı korur.
      let seen = false;
      const gun = new Date().toISOString().slice(0, 10);
      try { seen = localStorage.getItem('medsoru_splash_gun') === gun; localStorage.setItem('medsoru_splash_gun', gun); } catch { /* yok say */ }
      const klasik = getAppearance().design === 'v10';
      const wait = klasik ? Math.max(0, 5000 - performance.now()) : seen ? 0 : Math.max(0, 1800 - performance.now());
      let gitti = false;
      const kaldir = () => {
        if (gitti) return;
        gitti = true;
        el.classList.add('is-leaving');
        setTimeout(() => {
          try { el.remove(); } catch {}
        }, reduce ? 0 : 360);
      };
      const t = setTimeout(kaldir, wait);
      // Beklemek istemeyen dokunarak ya da bir tuşla geçer
      const gec = () => { clearTimeout(t); kaldir(); };
      el.addEventListener('pointerdown', gec, { once: true });
      window.addEventListener('keydown', gec, { once: true });
      return () => { clearTimeout(t); el.removeEventListener('pointerdown', gec); window.removeEventListener('keydown', gec); };
    }
  }, []);

  // Site açılışında PWA & Çevrimdışı Veritabanı Kurulum Önerisi
  useEffect(() => {
    if (showOnboarding) return;
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

    // İlk ziyarette hiç sorma (uygulama önce tanınsın); sonraki ziyaretlerde 20 sn kullanım sonra, ekran
    // boşken sor. Eskiden açılıştan 1.2 sn sonra her sayfada ekranın yarısını kaplıyordu.
    let visits = 0;
    try {
      visits = Number(localStorage.getItem('medsoru_visit_count') || 0) + 1;
      localStorage.setItem('medsoru_visit_count', String(visits));
    } catch {}
    if (visits < 2) return;
    const timer = setTimeout(() => {
      if (!document.querySelector('.sh-sheet-root, .ls-root, [role="dialog"]')) setIsPwaWelcomeOpen(true);
    }, 20000);

    return () => clearTimeout(timer);
  }, [showOnboarding]);
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
  // Aramadan / kavram çipinden açılacak hastalık profili
  const [selectedDiseaseId, setSelectedDiseaseId] = useState<string | undefined>(() =>
    initialRoute.route === 'diseases' ? deepLinkIdFor('diseases', initialRoute.param) : undefined
  );
  const [selectedGlossaryTermId, setSelectedGlossaryTermId] = useState<string | undefined>(() =>
    initialRoute.route === 'glossary' ? deepLinkIdFor('glossary', initialRoute.param) : undefined
  );
  // Örnek soru derin bağlantısı: /ornek-sorular/<soruId> (eski ?ornekId=)
  const [ornekQuestionId, setOrnekQuestionId] = useState<string | undefined>(() =>
    initialRoute.route === 'ornek_sorular' ? deepLinkIdFor('ornek_sorular', initialRoute.param) : undefined
  );
  // Kart / ders notu ekranları derin bağlantıyı açılışta okur; uygulama içi gezinmede yeniden kurulsunlar.
  const [deepLinkNonce, setDeepLinkNonce] = useState(0);
  const [learnLinkNonce, setLearnLinkNonce] = useState(0);
  clearDeepLinkTargets.current = () => {
    setSelectedGlossaryTermId(undefined);
    setSelectedDiseaseId(undefined);
    setOrnekQuestionId(undefined);
    setCanliDersKey(undefined);
  };

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
      if (getStoredPanelSecret().length >= 24) {
        return setLocalAdminSession(ADMIN_EMAIL);
      }
    } catch (e) {
      return null;
    }
    return null;
  });
  const [accessToken, setAccessToken] = useState<string | null>(null);
  // Zorunlu giriş kapısı: hesapsız (misafir) kullanım yok. Oturum durumu çözülünce kullanıcı yoksa giriş ekranı
  // kapatılamaz biçimde açılır. Tek istisna yapay zekâ test erişimi: sunucunun imzalı HttpOnly çerezi (aiTestErisim.ts).
  const [authHazir, setAuthHazir] = useState(false);
  const [aiTest, setAiTest] = useState<boolean | null>(null);
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

  // Push bildirimine tıklanınca servis çalışanı açık pencereye hedef yolu yollar (public/sw.js): sayfa
  // yenilenmeden rota kurulur ve öğeye odaklanılır. Yanıt portu, mesajın işlendiğini servis çalışanına bildirir.
  useEffect(() => {
    if (typeof navigator === 'undefined' || !('serviceWorker' in navigator)) return;
    const onMessage = (e: MessageEvent) => {
      if (e.data?.type !== 'MEDSORU_NAVIGATE' || typeof e.data.url !== 'string') return;
      e.ports?.[0]?.postMessage({ ok: true });
      openDeepLink(e.data.url);
    };
    navigator.serviceWorker.addEventListener('message', onMessage);
    return () => navigator.serviceWorker.removeEventListener('message', onMessage);
  }, []);

  // Normalise legacy #tab links to their path once, then follow back / forward
  useEffect(() => {
    // Yol normalleştirilirken derin bağlantının sorgu (?opt, ?sec, ?highlight) ve çapası (#…) korunur.
    // Karşılaştırma iç adreste yapılır (siteHaritasi): görünen adres iç içe olsa da sayfa/parametre aynıysa dokunulmaz.
    // AB16: bulunamayan adres olduğu gibi kalır (öğrenci yanlış yazdığı adresi görsün)
    if (initialRoute.route !== 'bulunamadi') try {
      const next = icPathFor(initialRoute.route, initialRoute.param);
      const ic = icKonum();
      const sp = new URLSearchParams(ic.search);
      sp.delete('questionId');
      const qs = sp.toString();
      // Yönetim alt derin bağlantısı (/manage/kisiler/<kişi>), kamp ve Son Prova alt yolları kırpılmaz
      const deeper = (initialRoute.route === 'manage' || initialRoute.route === 'kamp' || initialRoute.route === 'son_prova') && ic.pathname.startsWith(`${next}/`);
      const hedef = kanonik((deeper ? ic.pathname : next) + (qs ? `?${qs}` : '')) + window.location.hash;
      const simdi = window.location.pathname.replace(/^\/meds(?=\/|$)/, '') + window.location.search + window.location.hash;
      if (hedef !== simdi) {
        window.history.replaceState({ route: initialRoute.route, param: initialRoute.param }, '', hedef);
      }
    } catch {
      writeLocation(initialRoute.route, initialRoute.param, true);
    }
    const onPop = () => {
      const { route, param } = parseLocation();
      setActiveTabState(route);
      setPoolFocusId(route === 'questions' ? param : undefined);
      setCanliDersKey(route === 'canli_ders' ? param : undefined);
      if (route === 'search') setSearchPageQuery(param || '');
      // Derin bağlantı kimlikleri adres çubuğundan yeniden kurulur (yol parametresi ya da ?id=).
      const linkId = deepLinkIdFor(route, param);
      if (route === 'glossary') setSelectedGlossaryTermId(linkId);
      if (route === 'diseases') setSelectedDiseaseId(linkId);
      if (route === 'summaries') setOpenSummaryId(linkId);
      if (route === 'ornek_sorular') {
        setOrnekQuestionId(linkId);
        if (linkId) { setSelectedOrnekLessonId(null); setSelectedOrnekKazanimNo(null); }
      }
      // Çıkmış soru kimliği PastExamsView'de adresten okunur; eski arama metni onu ezmesin.
      if (route === 'past_exams' && param) setPastExamsSearchQuery('');
      if ((route === 'flashcards' || route === 'notes') && linkId) setDeepLinkNonce((n) => n + 1);
      if (route === 'learn') {
        setSelectedLearnDeckId(param);
        const sp = new URLSearchParams(window.location.search);
        const s = sp.get('slide');
        setSelectedLearnSlideNumber(s ? parseInt(s, 10) : undefined);
        // Aynı ders açıkken gelen adım/öğe bağlantısı (bildirim) oynatıcıyı o adımda yeniden kurar.
        if (/[?&](adim|hedef|slide|target)=/.test(window.location.search)) setLearnLinkNonce((n) => n + 1);
      }
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // v11: sayfa değişiminde yumuşak giriş (yalnız saydamlık + 4 px; styles/v11.css)
  const mainRef = useRef<HTMLElement>(null);
  useEffect(() => {
    const el = mainRef.current;
    if (!el) return;
    el.classList.remove('v11-enter');
    void el.offsetWidth;
    el.classList.add('v11-enter');
  }, [activeTab]);
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

  // Scroll Position Restoration: Save scroll position on scroll (throttled with rAF)
  useEffect(() => {
    let ticking = false;
    const handleScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          try {
            sessionStorage.setItem('medsoru_scroll_pos', window.scrollY.toString());
          } catch (e) {}
          ticking = false;
        });
        ticking = true;
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Restore scroll position after initial loading completes
  useEffect(() => {
    if (!loading) {
      // Derin bağlantıyla açılan sayfa kendi hedefine kayar; eski kaydırma konumu onu ezmesin.
      if (initialRoute.param || window.location.search || window.location.hash) return;
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

  useEffect(() => {
    let iptal = false;
    fetch('/api/ai-test/durum', { credentials: 'same-origin', cache: 'no-store' })
      .then((r) => (r.ok ? r.json() : { ok: false }))
      .then((d) => { if (!iptal) setAiTest(d?.ok === true); })
      .catch(() => { if (!iptal) setAiTest(false); });
    return () => { iptal = true; };
  }, []);

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
        setAuthHazir(true);
        // Oturum açılınca: cihazdaki notlar hesabın defterine birleşir, istatistikler hesap yedeğiyle birleştirilir
        // (sunucu birleştirir; yeni/boş cihaz hesabın verisini silmez, diğer cihazlardaki veri buraya gelir).
        setTimeout(() => {
          void syncNotes();
          backupUserDataToDatabase().catch(() => {});
        }, 3000);
      },
      () => {
        const local = getLocalAdminSession();
        if (local && local.email?.toLowerCase() === ADMIN_EMAIL.toLowerCase()) {
          setCurrentUser(local);
        } else {
          setCurrentUser(null);
          setAccessToken(null);
        }
        setAuthHazir(true);
      }
    );
    return () => unsubscribe();
  }, []);

  // Load committees on mount; canlı akıştan kurul değişikliği gelince yeniden çek
  useEffect(() => {
    fetchCommittees();
    startLiveDataSync();
    const onChange = () => fetchCommittees();
    window.addEventListener('medsoru:committees-changed', onChange);
    return () => window.removeEventListener('medsoru:committees-changed', onChange);
  }, []);

  // Load questions when selected committee changes or when switching to a question tab
  // Sekme değişimi yalnız ilk yüklemeyi öne çeker; aynı kurul için havuz yeniden indirilmez
  const loadedCommitteeRef = useRef<string | null>(null);
  useEffect(() => {
    if (!selectedCommitteeId || loadedCommitteeRef.current === selectedCommitteeId) return;
    const load = () => { loadedCommitteeRef.current = selectedCommitteeId; fetchQuestions(); };

    const isQuestionTab =
      activeTab === 'questions' ||
      activeTab === 'booklet' ||
      activeTab === 'practice' ||
      activeTab === 'quick_add' ||
      activeTab === 'stats';

    if (isQuestionTab) {
      load();
      return;
    }

    // Kullanıcı çıkmış, öğren, sözlük gibi farklı bir sekmedeyse ilk açılış bant genişliğini boğmamak
    // için soru havuzunu tarayıcı boşta kaldığında (idle) arka planda sessizce yükle.
    if (typeof window !== 'undefined' && 'requestIdleCallback' in window) {
      const id = (window as any).requestIdleCallback(load, { timeout: 3500 });
      return () => (window as any).cancelIdleCallback(id);
    } else {
      const timer = setTimeout(load, 2500);
      return () => clearTimeout(timer);
    }
  }, [selectedCommitteeId, activeTab]);

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

  // Toplu değişiklik / kaçan olay telafisi: açık kurulun havuzu sessizce yeniden çekilir (yükleniyor göstergesi yok)
  useEffect(() => {
    if (!selectedCommitteeId) return;
    let timer: ReturnType<typeof setTimeout> | null = null;
    const onResync = () => {
      if (timer) clearTimeout(timer);
      timer = setTimeout(() => {
        ApiService.getQuestions({ committeeId: selectedCommitteeId })
          .then((data) => { if (Array.isArray(data)) setQuestions(data); })
          .catch(() => {});
      }, 600);
    };
    window.addEventListener('medsoru:pool-resync', onResync);
    return () => {
      window.removeEventListener('medsoru:pool-resync', onResync);
      if (timer) clearTimeout(timer);
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

  // Google Logout
  const handleGoogleLogout = async () => {
    await logout();
    setCurrentUser(null);
    setAccessToken(null);
    setDriveUploadSuccess(null);
    // Bellekteki ekran durumları önceki öğrenciye ait: temiz açılış.
    window.location.reload();
  };

  const currentCommittee = (committees || []).find((c) => c.id === selectedCommitteeId);
  const targetCount = currentCommittee?.targetCount || 100;
  const isAdmin = isAdminUser(currentUser);
  // Çalışma anı site ayarı (yönetim v16): derleme sabitleri varsayılan, panel ayarı üstüne yazar (services/siteAyar.ts)
  const siteAyar = useSiteAyar();
  useLayoutEffect(() => { yoneticiAyarla(isAdmin); }, [isAdmin]);
  // H139: gizli / yalnız yönetici / bayrağı kapalı sayfa artık sessizce Bugün'e atmaz; nedenini söyleyen ekran gösterilir
  const sayfaGizliMi = !isAdmin && !isAdminAppMode() && sayfaYonlendir(activeTab, false);
  const sayfaKapaliMi = (sayfaKapali(activeTab) && !isAdmin) || sayfaGizliMi;
  // Kapalı sayfada içerik hiç kurulmaz: aşağıdaki sayfa blokları gorunenTab'a bakar (kapalı ekranı tek başına kalır)
  const gorunenTab = (sayfaKapaliMi ? '__kapali__' : activeTab) as typeof activeTab;
  // H485: kök adres (/) öğrenciye gizli "Soru ekle" sayfasına düşüyor ve açılışta "Bu sayfa şu an kapalı" görünüyordu.
  // Giriş sayfası kapalıysa Bugün'e geçilir (geçmişe kayıt yazılmaz); adresle girilen diğer gizli sayfalar H139 gereği ekranda kalır.
  useEffect(() => {
    if (sayfaKapaliMi && activeTab === 'quick_add') {
      try { window.history.replaceState(window.history.state, '', '/bugun'); } catch { /* yok say */ }
      navigateTo('/bugun');
    }
  }, [sayfaKapaliMi, activeTab]);
  // Moderatör: rol sunucudan (GET /api/me/access, Firebase jetonu) öğrenilir; yalnız moderasyon bölümleri açılır
  const [isModerator, setIsModerator] = useState(false);
  useEffect(() => {
    let cancelled = false;
    if (!currentUser || isAdmin) {
      setIsModerator(false);
      setModeratorMode(false);
      return;
    }
    void fetchMyAccess().then((a) => {
      if (cancelled) return;
      const on = !!a && a.role !== 'student' && !a.suspended;
      setModeratorMode(on);
      setIsModerator(on);
    });
    return () => {
      cancelled = true;
    };
  }, [currentUser?.uid, isAdmin]);

  // Hoş geldin turu: kayıt/girişten sonra bir kez (profilde `medsoru_tour_v1`); Ayarlar'dan `medsoru:tour` ile yeniden
  const { showTour, setShowTour, girisUyarisi, setGirisUyarisi, justAuthedRef, activeTabRef, showTanitim, setShowTanitim, tanitimGoruldu } =
    useTurVeTanitim(activeTab, currentUser, isAdmin, showOnboarding, setAuthModalInitialMode, setIsAuthModalOpen);

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

  // Google Drive'a otomatik yedek 2026-11-02'de kaldırıldı (Google girişi yok); yedekler Oracle'da tutulur.

  // Yönetim paneli › Kısayollar › Yönetici işlemleri: kabuktaki modalleri olayla açar
  useEffect(() => {
    const onAct = (e: Event) => {
      const k = (e as CustomEvent<string>).detail;
      if (k === 'diagnostics') setIsDiagnosticsOpen(true);
      else if (k === 'pastExam') setIsPastExamImporterOpen(true);
      else if (k === 'notebooklm') setIsNotebookLMModalOpen(true);
      else if (k === 'drive') void handleDriveUpload(false);
      else if (k === 'newCommittee') setIsNewCommitteeModalOpen(true);
      else if (k === 'subagents') setIsSubagentMonitorOpen(true);
      else if (k === 'faz14') setActiveTab('test_cikmis');
    };
    window.addEventListener('meds:admin-action', onAct);
    return () => window.removeEventListener('meds:admin-action', onAct);
  });

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

      // Öğrencinin yazdığı metin ayrıca ham kayıt olarak sunucuya gider; sunucu ücretsiz Gemini ile ayrıştırır.
      // Ayrıştırma başarısız olsa da katkı kaydedilmiş olur (hata yutulur).
      const intakePromise = (data.fragmentText?.trim() || data.options?.length)
        ? ApiService.submitQuestionIntake({
            rawText: data.fragmentText || '',
            committeeId: data.committeeId,
            questionNumber: data.questionNumber,
            discipline: data.discipline,
            questionId: savedQuestion?.id,
            uid: currentUser?.uid || data.authorUid,
            author: data.author,
            source: data.targetQuestionId ? 'katki-bagli' : 'hizli-ekle',
            options: data.options,
            claimedAnswer: data.claimedAnswer,
          }).catch(() => null)
        : Promise.resolve(null);

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
      return { intakeId: await intakePromise };
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
        (!q.contributedByUid && currentUser.displayName && q.contributedByName === currentUser.displayName) ||
        q.fragments.some((f) => f.authorUid === currentUser.uid || (!f.authorUid && currentUser.displayName && f.author === currentUser.displayName)) ||
        q.options.some((o) => o.suggestedByUid === currentUser.uid || (!o.suggestedByUid && currentUser.displayName && o.suggestedBy === currentUser.displayName)) ||
        (q.mergedSatellites && q.mergedSatellites.some((sat) =>
          sat.contributedByUid === currentUser.uid ||
          (!sat.contributedByUid && currentUser.displayName && sat.contributedByName === currentUser.displayName) ||
          sat.fragments?.some((f) => f.authorUid === currentUser.uid || (!f.authorUid && currentUser.displayName && f.author === currentUser.displayName)) ||
          sat.options?.some((o) => o.suggestedByUid === currentUser.uid || (!o.suggestedByUid && currentUser.displayName && o.suggestedBy === currentUser.displayName))
        )))
  );

  // Ultra-fast in-memory filtering: 0ms search & filter without network lag
  const filteredQuestions = useMemo(() => {
    let result = standaloneQuestions;
    if (selectedDiscipline && selectedDiscipline !== 'Tümü') {
      const discFold = foldTurkish(selectedDiscipline);
      result = result.filter((q) => foldTurkish(q.discipline || '') === discFold);
    }
    if (selectedStatus && selectedStatus !== 'Tümü') {
      result = result.filter((q) => q.status === selectedStatus);
    }
    if (searchQuery && searchQuery.trim()) {
      // Türkçe/aksansız: "sifiliz" = "Sifiliz", "ozofagus" = "özofagus"; "12", "#12", "s12" soru numarası
      const q = foldTurkish(searchQuery.trim());
      const numM = /^(?:#|s(?:oru)?\s*)?(\d{1,3})$/.exec(q);
      const words = q.split(/\s+/).filter(Boolean);
      const hit = (t?: string | null) => !!t && words.every((w) => foldTurkish(t).includes(w));
      result = result.filter((item) => {
        if (numM) return item.questionNumber?.toString() === numM[1];
        const hay = [
          item.topic, item.discipline, item.reconstruction?.stem, item.stem,
          ...(item.tags || []), ...(item.fragments || []).map((f) => f.text), ...(item.options || []).map((o) => o.text),
          ...(item.mergedSatellites || []).flatMap((sat) => [sat.topic, sat.reconstruction?.stem, sat.stem, ...(sat.fragments || []).map((f) => f.text), ...(sat.options || []).map((o) => o.text)]),
        ].filter(Boolean).join(' \n ');
        return hit(hay);
      });
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

  /** Arama sonucunu kendi sayfasında, derin bağlantısıyla açar; açılacak yeri yoksa false döner. */
  const openSearchHit = (hit: SearchHit): boolean => {
    const id = encodeURIComponent(hit.documentId);
    switch (hit.documentType) {
      case 'past_question':
      case 'deepseek_contribution':
        navigateTo(`${pathFor('past_exams')}/${id}`);
        return true;
      case 'summary':
        navigateTo(`${pathFor('summaries')}?noteId=${id}`);
        return true;
      case 'transcript':
        setActiveTab('transcripts');
        return true;
      case 'disease':
        // chunk-dis-<id> → hastalık kimliği documentId'dir
        navigateTo(`${pathFor('diseases')}?id=${id}`);
        return true;
      case 'glossary_term':
        // documentId terim adıdır; sözlük ada / eşanlamlıya göre eşler
        navigateTo(`${pathFor('glossary')}?id=${id}`);
        return true;
      case 'ornek_question':
        navigateTo(`${pathFor('ornek_sorular')}/${id}`);
        return true;
      case 'deck_slide':
        navigateTo(`${pathFor('learn')}/${id}${hit.pageNumber ? `?slide=${hit.pageNumber}` : ''}`);
        return true;
      case 'active_question':
      case 'user_contribution': {
        // Havuz sorusu ve öğrenci katkısı chunk'larında documentId soru kimliğidir
        if (questions.some((q) => q.id === hit.documentId)) navigateTo(`${pathFor('questions')}/${id}`);
        else { setSearchQuery(''); setActiveTab('questions'); }
        return true;
      }
      default:
        // Ders slaytı arama sayfasındaki okuyucuda açılır; AI yanıtı vb. yalnız sonuç listesinde okunur.
        return false;
    }
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
    justAuthedRef.current = true;
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

  // Hesapsız giriş yok: tanıtım/kayıt ekranı kapatılamaz; yapay zekâ test çerezi doğrulanana dek de açık kalır.
  // Yönetim konsolu (/manage, /yonetim) veya MeDSor Yönetim Android uygulaması açıkken öğrenci kayıt kapısı konsolu örtmez.
  const isManageRoute = activeTab === 'manage' || activeTab === 'admin';
  const girisKapisi = !isManageRoute && !isAdminAppMode() && !currentUser && aiTest !== true && (showOnboarding || (authHazir && aiTest === false));
  const arzuAcik = useArzuAcik();
  const arzuKatmani = !isManageRoute && !girisKapisi && !girisUyarisi && arzuAcik && arzuHesabiMi(currentUser);
  const gorunumBaglami = { activeTab, canliDersKey, committees, completedQuestions, congratsToast, currentCommittee, currentUser, deepLinkNonce, driveUploadSuccess, emptyQuestions, fetchQuestions, filterMyQuestionsOnly, gatheringQuestions, gorunenTab, handleAddFragment, handleAddOption, handleAddQuestionContribution, handleDeleteQuestion, handleGenerateSlots, handleGoogleLogout, handleReconstructWithAi, handleSetClaimedAnswer, handleUpdateQuestionReference, handleUpvoteFragment, handleUpvoteOption, handleUpvoteQuestion, isAdmin, isGeneratingSlots, learnLinkNonce, learnQuestionFocus, loading, myQuestions, openQuestion, openSearchHit, openSummaryId, ornekQuestionId, pastExamsSearchQuery, poolFocusQuestion, poolQuestions, questions, reconstructingMap, sayfaGizliMi, sayfaKapaliMi, searchFocusId, searchPageQuery, searchQuery, selectedCommitteeId, selectedDiscipline, selectedDiseaseId, selectedGlossaryTermId, selectedLearnDeckId, selectedLearnSlideNumber, selectedOrnekKazanimNo, selectedOrnekLessonId, selectedStatus, setActiveTab, setAuthModalInitialMode, setClusterFocusId, setCongratsToast, setContributeDefaultNumber, setCurrentUser, setDriveUploadSuccess, setFilterMyQuestionsOnly, setIsAuthModalOpen, setIsContributeModalOpen, setIsEditQuestionModalOpen, setIsHistoryModalOpen, setIsOfflineModalOpen, setIsPdfModalOpen, setLearnQuestionFocus, setOptimizeQuestion, setPastExamsSearchQuery, setPdfSlideTarget, setPoolFocusId, setSearchPageQuery, setSearchQuery, setSelectedCommitteeId, setSelectedDiscipline, setSelectedLearnDeckId, setSelectedLearnSlideNumber, setSelectedOrnekKazanimNo, setSelectedOrnekLessonId, setSelectedQuestionForHistory, setSelectedQuestionToEdit, setSelectedStatus, setShowClusterModal, setVisibleCount, standaloneQuestions, targetCount, visibleCount };
  const modalBaglami = { accessToken, activeTab, authModalInitialMode, clusterFocusId, committees, contributeDefaultNumber, currentCommittee, currentUser, fetchQuestions, handleAddCommittee, handleAddQuestionContribution, handleAuthSuccess, isAdmin, isAuthModalOpen, isContributeModalOpen, isDiagnosticsOpen, isDriveModalOpen, isEditQuestionModalOpen, isHistoryModalOpen, isNewCommitteeModalOpen, isNotebookLMModalOpen, isOfflineModalOpen, isPastExamImporterOpen, isPdfModalOpen, isPwaWelcomeOpen, isSubagentMonitorOpen, optimizeQuestion, pdfSlideTarget, questions, selectedCommitteeId, selectedQuestionForHistory, selectedQuestionToEdit, setActiveTab, setDriveUploadSuccess, setIsAuthModalOpen, setIsContributeModalOpen, setIsDiagnosticsOpen, setIsDriveModalOpen, setIsEditQuestionModalOpen, setIsHistoryModalOpen, setIsNewCommitteeModalOpen, setIsNotebookLMModalOpen, setIsOfflineModalOpen, setIsPastExamImporterOpen, setIsPdfModalOpen, setIsPwaWelcomeOpen, setIsSubagentMonitorOpen, setOptimizeQuestion, setPdfSlideTarget, setQuestions, setSelectedQuestionForHistory, setSelectedQuestionToEdit, setShowClusterModal, showClusterModal, showOnboarding };

  return (
    <GlossaryProvider>
    <MusicPlayerProvider>
      {girisUyarisi && !isManageRoute && (
        <Suspense fallback={null}>
          <GirisUyarisi onKabul={() => setGirisUyarisi(false)} />
        </Suspense>
      )}
      {girisKapisi && <Suspense fallback={<ViewFallback />}><Onboarding onAuthSuccess={handleAuthSuccess} /></Suspense>}
      {/* Başarım: dönem/kurul seçimi (girişte zorunlu) + ödül kutlamaları */}
      {(currentUser?.uid || aiTest) && !girisKapisi && !isManageRoute && (
        <Suspense fallback={null}>
          <BasarimKatmani uid={currentUser?.uid || 'ai-test'} ad={currentUser?.displayName} kapali={girisUyarisi} />
        </Suspense>
      )}
      {arzuKatmani && (
        <Suspense fallback={null}>
          <ArzuKatmani rota={activeTab} soruSor={!isAdmin} />
        </Suspense>
      )}
      {showTour && !isManageRoute && (
        <Suspense fallback={null}>
          <WelcomeTour name={currentUser?.displayName} onGo={setActiveTab} onClose={() => { setShowTour(false); if (!tanitimGoruldu()) setShowTanitim(true); }} />
        </Suspense>
      )}
      {showTanitim && !showTour && !isManageRoute && (
        <Suspense fallback={null}>
          <TanitimVideo onClose={() => setShowTanitim(false)} />
        </Suspense>
      )}
      <div className="min-h-dvh bg-canvas text-ink flex flex-col font-sans antialiased">
      <ToastHost />
      <CdVideoRozet />
      <ConfirmHost />
      <TooltipHost />
      {activeTab !== 'music' && activeTab !== 'practice' && activeTab !== 'manage' && (
        <MiniMusicPlayer onOpen={() => setActiveTab('music')} />
      )}
      {activeTab === 'practice' ? (
        <>
        <main className="contents">
          <Suspense fallback={<ViewFallback />}>
            <TestHub onExit={() => setActiveTab('study')} />
          </Suspense>
        </main>
        {/* Kronometre soru çözme ekranında da sürer (tasarım kronoSoru); dallar ayrık olduğundan tek örnek korunur */}
        <V15Icinde><KronometreV15 /></V15Icinde>
        </>
      ) : activeTab === 'manage' || activeTab === 'admin' ? (
        isAdmin && activeTab === 'manage' && manageKabugu() === 'v16' ? (
          yonetimGirisineGec() ? <ViewFallback /> : (
            <Suspense fallback={<ViewFallback />}>
              <ManageV16 adminEmail={ADMIN_EMAIL} onExit={() => setActiveTab('quick_add')} />
            </Suspense>
          )
        ) : isAdmin || isModerator ? (
          <Suspense fallback={<ViewFallback />}>
            <ManageConsole
              moderatorOnly={!isAdmin}
              key={activeTab}
              entry={activeTab === 'admin' ? 'admin' : 'manage'}
              initialSlug={parseLocation().param}
              adminEmail={isAdmin ? ADMIN_EMAIL : currentUser?.email || ''}
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
              <h1 className="m-0 font-display font-bold text-2xl tracking-[-0.02em]">MeDSor Yönetim</h1>
              <p className="m-0 text-md text-ink-2">Bu konsol yalnızca yöneticilere ve moderatörlere açık. Hesabınla veya kalıcı yönetici anahtarınla giriş yap.</p>
              <div className="flex flex-wrap justify-center gap-2 pt-1 w-full">
                <button
                  type="button"
                  onClick={() => setActiveTab('quick_add')}
                  className="h-11 px-4 rounded-xl border border-line-2 bg-white font-semibold text-md cursor-pointer"
                >
                  Siteyi Kullan
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setAuthModalInitialMode('admin');
                    setIsAuthModalOpen(true);
                  }}
                  className="h-11 px-5 rounded-xl bg-accent hover:bg-accent-hover text-white font-semibold text-md cursor-pointer"
                >
                  Yönetici Girişi
                </button>
              </div>
              <form
                className="w-full pt-3 mt-2 border-t border-line flex flex-col gap-2 text-left"
                onSubmit={(e) => {
                  e.preventDefault();
                  const fd = new FormData(e.currentTarget);
                  const sec = String(fd.get('panelSecret') || '').trim();
                  if (sec.length < 24) {
                    toast.error('Anahtar eksik', 'Geçerli bir MEDS_PANEL_SECRET (en az 24 karakter) girin.');
                    return;
                  }
                  setStoredPanelSecret(sec);
                  const adminUser = setLocalAdminSession(ADMIN_EMAIL);
                  setCurrentUser(adminUser);
                  safeStorage.setItem('medsoru_user_registered', 'true');
                  toast.success('Yönetici oturumu açıldı', 'Kalıcı yönetici anahtarı kaydedildi.');
                }}
              >
                <label className="text-xs font-semibold text-ink-2">
                  Kalıcı Yönetici Anahtarı (MEDS_PANEL_SECRET) ile Doğrudan Bağlan
                </label>
                <div className="flex gap-2">
                  <input
                    name="panelSecret"
                    type="password"
                    placeholder="MEDS_PANEL_SECRET değerini yapıştırın…"
                    className="flex-1 h-10 px-3 rounded-xl border border-line-2 bg-canvas text-sm font-mono"
                  />
                  <button
                    type="submit"
                    className="h-10 px-4 rounded-xl bg-ink text-white text-sm font-semibold cursor-pointer"
                  >
                    Bağlan
                  </button>
                </div>
              </form>
            </div>
          </div>
        )
      ) : (
      <>
      {/* v8 kabuğu: masaüstü/tablette yan menü, telefonda alt sekmeler */}
      <SideNav active={activeTab} onGo={setActiveTab} isAdmin={isAdmin} user={currentUser} />
      <div className="sh-app">
        <ScrollTopFab routeKey={activeTab} />
        <TamEkranGezinme active={activeTab} onGo={setActiveTab} />
        <TopBar
          active={activeTab}
          onGo={setActiveTab}
          user={currentUser}
          isAdmin={isAdmin}
          searchQuery={searchQuery}
          onSearch={(q, focusId, hit) => { if (!hit || !openSearchHit(hit)) openSearchPage(q, focusId); }}
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

      {!isOnline && (
        <div className="sh-offline" role="status">
          <i aria-hidden="true" />
          <span><b>Çevrimdışısın.</b> Sorular ve desteler cihazdaki kopyadan açılıyor.</span>
          <button type="button" onClick={() => setIsOfflineModalOpen(true)}>Veritabanı</button>
        </div>
      )}
      {/* Site duyurusu (Yönetim › Site › Duyurular; çalışma anı site ayarı) */}
      {siteAyar.duyuru?.acik && <Suspense fallback={null}><DuyuruBandi git={(y) => navigateTo(y)} /></Suspense>}
      {/* Main Container */}
      <main ref={mainRef} className={`sh-main ${activeTab === 'ai_chat' ? 'ms-chat-main' : ''}`}>
        <Gorunumler {...gorunumBaglami} />
      </main>

      {/* Canlı ders oynatıcısı: rota değişse de çalma sürer (ders ekranında tam çubuk, başka sayfada mini) */}
      <V15Icinde><KronometreV15 /><ProfilKurulumKapisi girisli={!!currentUser} yonetici={isAdmin} /></V15Icinde>
      <CanliDersDockGate activeTab={activeTab} dersKey={activeTab === 'canli_ders' ? canliDersKey : undefined} />

      {/* Alt gezinme (telefon) */}
      <TabBar
        active={activeTab}
        onGo={setActiveTab}
        isAdmin={isAdmin}
        onPdf={() => setIsPdfModalOpen(true)}
        onOffline={() => setIsOfflineModalOpen(true)}
      />
      </div>
      </>
      )}

      <Modallar {...modalBaglami} />
      </div>
    </MusicPlayerProvider>
    </GlossaryProvider>
  );
}
