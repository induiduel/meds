import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  ShieldCheck,
  Inbox,
  Wrench,
  Users,
  Terminal,
  Activity,
  Settings,
  RefreshCw,
  Layers,
  Moon,
  Sun,
  ArrowLeft,
  Workflow,
  GitMerge,
  Table2,
  FlaskConical,
  Menu,
  ChevronDown,
  Database,
  Library,
  HardDrive,
  Search,
  CornerDownLeft,
  Brain,
  Clock,
  Boxes,
  BookOpenCheck,
  MessageSquareText,
  Archive,
  UserSearch,
} from 'lucide-react';
import type { QuestionItem, Committee, AdminNotification } from '../../types';
import { ApiService } from '../../services/api';
import { AdminScriptsTab } from '../AdminScriptsTab';
import { AdminPanelModal } from '../AdminPanelModal';
import { writeLocation } from '../../router';
import { AdminEditQuestionModal } from '../AdminEditQuestionModal';
import { DraftStudio } from './DraftStudio';
import { useTheme } from '../../utils/theme';
import { toast } from '../ui/Toast';
import { ManageDraftsSection } from './ManageDraftsSection';
import { ManageDataSection } from './ManageDataSection';
import { ManageCatalogSection } from './ManageCatalogSection';
import { ManagePhasesSection } from './ManagePhasesSection';
import { ManageMergesSection } from './ManageMergesSection';
import { ManageRawPoolSection } from './ManageRawPoolSection';
import { ManageDersIsciSection } from './ManageDersIsciSection';
import { ManageInboxSection } from './ManageInboxSection';
import { ManageIntakeSection } from './ManageIntakeSection';
import { ManageModerationSection } from './ManageModerationSection';
import { ManageUsersSection } from './ManageUsersSection';
import { ManagePeopleSection } from './ManagePeopleSection';
import { ManageSystemSection } from './ManageSystemSection';
import { ManageAutomationSection } from './ManageAutomationSection';
import { ManageDataCoreSection } from './ManageDataCoreSection';
import { ManageNotebookLMSection } from './ManageNotebookLMSection';
import { ManagePendingOperationsSection } from './ManagePendingOperationsSection';
import { consoleLogBuffer } from './ConsoleLogBuffer';
import { ManageMetrics } from './ManageMetrics';
import { useAppearance, DENSITY_LABELS, type Density as AppDensity } from '../../utils/appearance';
import { guardedInterval } from '../../services/net';
import { realtimeEventService, type RealtimeConnectionStatus } from '../../services/realtimeEvents';
import '../../styles/manage-v9.css';
import { Segmented } from '../ui/kit';
import { isLocalHost, getPanelTarget, PANEL_TARGET_KEY, PANEL_ON_ORACLE_AT_BOOT } from '../../config/deployment';
import { Drawer, SearchBox, classifyNotice } from './consoleUi';
import {
  InboxReport,
  InboxComment,
  ManageUser,
  loadManageInbox,
  loadManageUsers,
  computeUserActivity,
  resolveInboxReport,
  editInboxReport,
  deleteInboxReport,
  editPastComment,
  deletePastComment,
  publishDraft,
  deleteDraftEverywhere,
} from '../../services/manageConsoleService';

export type ManageSection = 'pending' | 'inbox' | 'intake' | 'pool' | 'catalog' | 'data' | 'phases' | 'merges' | 'raw_pool' | 'ders_isci' | 'drafts' | 'studio' | 'moderation' | 'people' | 'users' | 'scripts' | 'system' | 'automation' | 'datacore' | 'notebooklm' | 'database';

interface ManageConsoleProps {
  adminEmail: string;
  committees: Committee[];
  questions: QuestionItem[];
  selectedCommitteeId: string;
  onSelectCommittee: (id: string) => void;
  onRefreshData: () => Promise<void>;
  onExit: () => void;
  /** Tam ekran kipinde pencere tüm görünümü kaplar (manage alt alanı varsayılanı). */
  fullscreen?: boolean;
  /** Hangi adresten girildi: /manage ya da /yonetim. Bölüm adresi bu tabana yazılır. */
  entry?: 'manage' | 'admin';
  /** Adresteki bölüm (ikinci parça), örn. "taslaklar" */
  initialSlug?: string;
}

const SECTIONS: { id: ManageSection; slug: string; label: string; hint: string; icon: React.ElementType; group: string; keywords?: string }[] = [
  { id: 'pending', slug: 'bekleyen-islemler', label: 'Bekleyen İşlemler', hint: 'Kullanıcı hata bildirimleri, Gemini AI inceleme kuyruğu, otomatik düzeltmeler ve geri alma (rollback) takibi.', icon: Clock, group: 'Genel', keywords: 'kuyruk bekleyen hata bildirim yapay zeka düzeltme rollback' },
  { id: 'inbox', slug: 'gelen-kutusu', label: 'Gelen kutusu', hint: 'Bildirim, yorum, taslak ve sistem uyarıları tek kuyrukta; en yenisi üstte.', icon: Inbox, group: 'Genel', keywords: 'bildirim yorum uyarı' },
  { id: 'moderation', slug: 'moderasyon', label: 'Moderasyon', hint: 'Şikâyet edilen soruyu gör, düzelt ya da kaldır.', icon: Wrench, group: 'Genel', keywords: 'şikayet hata bildirimi' },
  { id: 'pool', slug: 'soru-havuzu', label: 'Soru havuzu', hint: 'Kurul sorularını düzenle, sil, içe aktar; taslakları kümele.', icon: Library, group: 'İçerik', keywords: 'kurul soru içe aktar yükle çıkmış' },
  { id: 'catalog', slug: 'veri-katalogu', label: 'Veri kataloğu', hint: 'Her veri türü tek yerde: ara, sınıflara göre süz, kaydı düzenle, değerlendir (onaylı / inceleme / sorunlu), etiketle ve ilişkileri gez.', icon: Boxes, group: 'İçerik', keywords: 'katalog sınıflandır etiket değerlendir ilişki deste kazanım sözlük kart hastalık özet geri bildirim müzik' },
  { id: 'data', slug: 'tum-veriler', label: 'Tüm veriler', hint: 'Her veri kümesi tek tabloda: ara, sırala, seç, toplu işlem yap, CSV al.', icon: Table2, group: 'İçerik', keywords: 'tablo csv toplu' },
  { id: 'phases', slug: 'fazlar', label: 'Faz verileri', hint: 'Soru bazında faz çıktıları: gez, elle düzelt, arama testini çalıştır.', icon: FlaskConical, group: 'İçerik', keywords: 'faz 14 faz 15' },
  { id: 'ders_isci', slug: 'yeni-dersler', label: 'Yeni dersler', hint: 'Drive\'a eklenen ders PDF\'lerinden ders işçisinin ürettiği paketler: incele, önizle, onayla; 2026-27 checklist durumu.', icon: BookOpenCheck, group: 'İçerik', keywords: 'ders işçisi drive pdf onay taslak deste checklist yeni ders' },
  { id: 'raw_pool', slug: 'ham-havuz', label: 'Ham soru havuzu', hint: 'Kullanıcı soruları ve katkıları (ipucu, şık, itiraz, yorum, oy) soru başına tek kümede; silinmez. Görüntüle, sınıflandır, düzenle, JSON/CSV al.', icon: Archive, group: 'İçerik', keywords: 'ham veri defter küme kullanıcı katkı ipucu şık itiraz dışa aktar json' },
  { id: 'merges', slug: 'birlesenler', label: 'Birleştirilen sorular', hint: 'Kopya çıkmış sorular: yan yana karşılaştır, asıl soruyu seç ya da ayır.', icon: GitMerge, group: 'İçerik', keywords: 'kopya birleştir' },
  { id: 'datacore', slug: 'veri-merkezi', label: 'Veri Merkezi (v2)', hint: 'Bağımsız Core v2 hattı: sorular, kazanım, ders notu bağları, kavram grafı, toplu tamamlama.', icon: Database, group: 'İçerik', keywords: 'core kazanım graf' },
  { id: 'notebooklm', slug: 'notebooklm', label: 'NotebookLM Stüdyosu', hint: 'NotebookLM JSON/MD çıktılarını yükle, alternatif olarak sakla, orijinalle karşılaştır ve tercihi seç.', icon: Brain, group: 'İçerik', keywords: 'notebooklm ai json alternatif rag soru deste spot' },
  { id: 'intake', slug: 'serbest-girdiler', label: 'Serbest girdiler', hint: 'Öğrencilerin tek kutuya yazdığı metinler ve ücretsiz Gemini ajanlarının ayrıştırması: kanıt, güven, olumsuz kök, yeniden ayrıştır.', icon: MessageSquareText, group: 'İçerik', keywords: 'serbest metin girdi ayrıştır ajan gemini hatırlanan şık kök kanıt' },
  { id: 'drafts', slug: 'taslaklar', label: 'Taslaklar', hint: 'Öğrenci taslaklarını kümele, birleştir, düzenle ya da AI ile tam soruya dönüştür.', icon: Layers, group: 'İçerik', keywords: 'parça taslak' },
  { id: 'studio', slug: 'studyo', label: 'Taslak stüdyosu', hint: 'Parçaları elle eşle: ağaç, pano, akış ve terim görünümleri.', icon: Workflow, group: 'İçerik', keywords: 'eşle pano' },
  { id: 'people', slug: 'kisiler', label: 'Kişiler', hint: 'Her kullanıcının tüm izi: cihazlar, kullanım süresi, skorlar, etkinlik, yorumlar, notlar, sorular, şıklar, beğeniler ve bildirimler — canlı.', icon: UserSearch, group: 'Topluluk', keywords: 'kişi kullanıcı cihaz süre skor yorum not bildirim şikayet beğeni öneri etkinlik geçmiş çevrimiçi' },
  { id: 'users', slug: 'kullanicilar', label: 'Kullanıcılar', hint: 'Katkılar, hesaplar, roller ve e-posta.', icon: Users, group: 'Topluluk', keywords: 'öğrenci hesap rol smtp e-posta' },
  { id: 'scripts', slug: 'betikler', label: 'Betikler', hint: 'Veri hattı betiklerini ve zincirleri çalıştır, çıktıyı canlı izle.', icon: Terminal, group: 'Sistem', keywords: 'script görev zincir' },
  { id: 'system', slug: 'sistem', label: 'Sistem ve günlükler', hint: 'Veritabanı ve AI sağlığı, servisler, tarayıcı konsolu.', icon: Activity, group: 'Sistem', keywords: 'log sağlık servis' },
  { id: 'automation', slug: 'otomasyon', label: 'Otomasyon', hint: 'Zamanlanmış işler, AI pencereleri, anahtarlar; Drive eşitlemesi ve masaüstü servisleri.', icon: Settings, group: 'Sistem', keywords: 'drive yedek anahtar zamanla' },
  { id: 'database', slug: 'veritabani', label: 'Veritabanı ve yedek', hint: 'Etkin veritabanı, eşitleme, dışa ve içe aktarım.', icon: HardDrive, group: 'Sistem', keywords: 'supabase firebase yedek dışa aktar' },
];
/** v12 "Net": bölümler işe göre gruplanır (v10/v11 yukarıdaki sırayı ve grup adlarını korur). */
const V12_GROUPS: { label: string; ids: ManageSection[] }[] = [
  { label: 'Gelen', ids: ['inbox', 'pending', 'moderation'] },
  { label: 'Sorular', ids: ['pool', 'raw_pool', 'intake', 'drafts', 'studio', 'merges'] },
  { label: 'Öğrenme içeriği', ids: ['ders_isci', 'catalog', 'notebooklm'] },
  { label: 'Veri', ids: ['data', 'phases', 'datacore', 'database'] },
  { label: 'Kişiler ve denetim', ids: ['people', 'users'] },
  { label: 'Sistem', ids: ['system', 'automation', 'scripts'] },
];
const V12_SECTIONS = V12_GROUPS.flatMap((g) => g.ids.map((id) => {
  const sec = SECTIONS.find((x) => x.id === id)!;
  return { ...sec, group: g.label };
})).concat(SECTIONS.filter((x) => !V12_GROUPS.some((g) => g.ids.includes(x.id))));
const foldTr = (t: string) => t.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ı/g, 'i');
const sectionBySlug = (slug?: string) => SECTIONS.find((x) => x.slug === slug || x.id === slug);

// Yoğunluk: uygulamanın görünüm ayarından gelir (Profil ve ayarlar → Kompakt/Normal/Geniş)
type Density = 'comfy' | 'compact' | 'tight';
const SECTION_KEY = 'medsoru_manage_section';
const RECENT_KEY = 'medsoru_manage_recent';
const readRecent = (): ManageSection[] => {
  try {
    const v = JSON.parse(localStorage.getItem(RECENT_KEY) || '[]');
    return Array.isArray(v) ? v.filter((x) => SECTIONS.some((s) => s.id === x)).slice(0, 5) : [];
  } catch {
    return [];
  }
};
const pushRecent = (id: ManageSection) => {
  try {
    localStorage.setItem(RECENT_KEY, JSON.stringify([id, ...readRecent().filter((x) => x !== id)].slice(0, 5)));
  } catch {
    /* gizli pencere */
  }
};
const SYNC_STALE_MS = 60_000;
const readSection = (entry: 'manage' | 'admin', slug?: string): ManageSection => {
  const fromUrl = sectionBySlug(slug);
  if (fromUrl) return fromUrl.id;
  if (entry === 'admin') return 'pool';
  try {
    const v = localStorage.getItem(SECTION_KEY) as ManageSection | null;
    return v && SECTIONS.some((s) => s.id === v) ? v : 'inbox';
  } catch {
    return 'inbox';
  }
};

export const ManageConsole: React.FC<ManageConsoleProps> = ({
  adminEmail,
  committees,
  questions,
  selectedCommitteeId,
  onSelectCommittee,
  onRefreshData,
  onExit,
  fullscreen = true,
  entry = 'manage',
  initialSlug,
}) => {
  const [section, setSectionState] = useState<ManageSection>(() => readSection(entry, initialSlug));
  const sectionRef = useRef(section);
  sectionRef.current = section;
  // v8: konsol uygulamanın tek yoğunluk ayarını kullanır (Profil ve ayarlar ile aynı)
  const look = useAppearance();
  const density: Density = look.density === 'compact' ? 'tight' : 'comfy';
  const [menuOpen, setMenuOpen] = useState(false);
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [usersTab, setUsersTab] = useState<'activity' | 'accounts'>('activity');
  const [autoTab, setAutoTab] = useState<'schedule' | 'services'>('schedule');
  const setSection = (s: ManageSection, opts: { replace?: boolean } = {}) => {
    setSectionState(s);
    setMenuOpen(false);
    setPaletteOpen(false);
    writeLocation(entry, SECTIONS.find((x) => x.id === s)?.slug, opts.replace);
    pushRecent(s);
    try {
      localStorage.setItem(SECTION_KEY, s);
    } catch {
      /* gizli pencere: bu ziyaretlik */
    }
  };
  const [lastSync, setLastSync] = useState<number | null>(null);
  const lastSyncRef = useRef(0);
  const markSynced = () => {
    lastSyncRef.current = Date.now();
    setLastSync(lastSyncRef.current);
  };
  const [liveStatus, setLiveStatus] = useState<RealtimeConnectionStatus>(() => realtimeEventService.getStatus());

  // v9 görünümü: konsol açıkken <html> ms-v9 taşır (manage-v9.css bu sınıfa bağlı)
  useEffect(() => {
    document.documentElement.classList.add('ms-v9');
    return () => document.documentElement.classList.remove('ms-v9');
  }, []);
  const [loading, setLoading] = useState(false);

  // Yerel panel → Oracle: sayfadaki tüm veri tek kaynaktan gelsin diye kaynak açılışta seçilir. Panele uygulama
  // içinden girilip hedef açılıştakinden farklıysa ya da panelden çıkılınca sayfa bir kez yenilenir.
  // Oracle hedefi yalnız /manage girişinde geçerli (PANEL_ON_ORACLE_AT_BOOT yolu /manage ister); /yonetim hep yereldir,
  // yoksa açılış bayrağı hiç tutmaz ve sayfa sonsuz yenilenir.
  const localHost = isLocalHost() && entry === 'manage';
  const panelTarget = getPanelTarget();
  useEffect(() => {
    if (!localHost) return;
    if ((panelTarget === 'oracle') !== PANEL_ON_ORACLE_AT_BOOT) window.location.reload();
    return () => {
      if (PANEL_ON_ORACLE_AT_BOOT) setTimeout(() => { if (!/^\/manage(\/|$)/.test(window.location.pathname)) window.location.reload(); }, 0);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const choosePanelTarget = (t: 'oracle' | 'yerel') => {
    try { localStorage.setItem(PANEL_TARGET_KEY, t); } catch { /* gizli pencere */ }
    window.location.reload();
  };

  // Adres bölümü taşır: açılışta normalize et, geri/ileri ile bölüm değişsin
  useEffect(() => {
    // Alt derin bağlantı (/manage/kisiler/<kişi>) korunur; yalnız bölüm adresi normalize edilir
    const slug = SECTIONS.find((x) => x.id === section)?.slug;
    if (!(slug && window.location.pathname.startsWith(`/manage/${slug}/`))) setSection(section, { replace: true });
    const onPop = () => {
      const hit = sectionBySlug(window.location.pathname.split('/').filter(Boolean)[1]);
      if (hit) setSectionState(hit.id);
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  // Ctrl/⌘ + K: bölüme atla
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setPaletteOpen((v) => !v);
        return;
      }
      // Alt + ↑/↓: önceki / sonraki bölüm (yazı alanındayken de çalışır; Alt+ok metinde iş görmez)
      if (e.altKey && !e.ctrlKey && !e.metaKey && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) {
        e.preventDefault();
        const i = SECTIONS.findIndex((x) => x.id === sectionRef.current);
        setSection(SECTIONS[(i + (e.key === 'ArrowDown' ? 1 : SECTIONS.length - 1)) % SECTIONS.length].id);
      }
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);

  // Bildirimler: tonuna göre toast (hata metni kırmızı, diğerleri yeşil)
  const notify = (msg: string) => {
    if (!msg) return;
    if (classifyNotice(msg) === 'error') toast.error(msg);
    else toast.success(msg);
  };

  // Ortak veri: gelen kutusu, moderasyon ve kullanıcılar aynı kaynağı okur
  const [reports, setReports] = useState<InboxReport[]>([]);
  const [comments, setComments] = useState<InboxComment[]>([]);
  const [pastQuestions, setPastQuestions] = useState<QuestionItem[]>([]);
  const [notifications, setNotifications] = useState<AdminNotification[]>([]);
  const [drafts, setDrafts] = useState<QuestionItem[]>([]);
  const [registeredUsers, setRegisteredUsers] = useState<ManageUser[]>([]);
  const [resolvedIds, setResolvedIds] = useState<Set<string>>(new Set());
  const [busyAction, setBusyAction] = useState<string | null>(null);
  const [focusReportId, setFocusReportId] = useState('');
  const [editingDraft, setEditingDraft] = useState<QuestionItem | null>(null);
  const [dataJump, setDataJump] = useState<{ id: string; dsId: 'questions' | 'past' } | null>(null);

  useEffect(() => {
    consoleLogBuffer.install();
  }, []);

  const reloadInbox = async () => {
    setLoading(true);
    try {
      const data = await loadManageInbox(selectedCommitteeId);
      setReports(data.reports);
      setComments(data.comments);
      setPastQuestions(data.pastQuestions);
      setNotifications(data.notifications);
      setDrafts(data.drafts.length > 0 ? data.drafts : questions.filter((q) => q.status !== 'completed'));
      setRegisteredUsers((await loadManageUsers(adminEmail).catch(() => [])) || []);
      markSynced();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Gelen kutusu yüklenemedi.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void reloadInbox();

    // 1. SSE (Server-Sent Events) Kalıcı Kanal Dinleyicileri (Anlık 0ms Gecikme)
    const unsubInbox = realtimeEventService.onInboxUpdate(() => {
      loadManageInbox(selectedCommitteeId)
        .then((data) => {
          setReports(data.reports);
          setComments(data.comments);
          setNotifications(data.notifications);
          if (data.drafts.length > 0) setDrafts(data.drafts);
          markSynced();
        })
        .catch(() => {});
    });

    const unsubNotif = realtimeEventService.onNotification((newNotif) => {
      setNotifications((prev) => [newNotif, ...prev.filter((n) => n.id !== newNotif.id)]);
    });

    // 2. Güvenlik ve yedek yoklama: 6 saniyeden 60 saniyeye çekildi (SSE ile %90 ağ/sunucu tasarrufu)
    const stopInterval = guardedInterval(async () => {
      try {
        const data = await loadManageInbox(selectedCommitteeId);
        setReports(data.reports);
        setComments(data.comments);
        setNotifications(data.notifications);
        if (data.drafts.length > 0) setDrafts(data.drafts);
        markSynced();
      } catch (_) {}
    }, 60000);

    // 3. Canlı kanal durumu: kopup yeniden bağlanınca arada kaçan olaylar için kuyruğu tazele
    // (durum her zaman 'connecting' üzerinden geçer: bir kez bağlandıktan sonra düşüp yeniden bağlanmak aranır)
    let seenUp = realtimeEventService.getStatus() === 'connected';
    let wentDown = false;
    setLiveStatus(realtimeEventService.getStatus());
    const unsubStatus = realtimeEventService.onStatusChange((st) => {
      setLiveStatus(st);
      if (st === 'connected') {
        if (seenUp && wentDown) void reloadInbox();
        seenUp = true;
        wentDown = false;
      } else if (seenUp) wentDown = true;
    });
    const unsubResync = realtimeEventService.on('resync', () => void reloadInbox());

    // 4. Sekmeye geri dönülünce veri bayatsa tazele
    const onVisible = () => {
      if (!document.hidden && Date.now() - lastSyncRef.current > SYNC_STALE_MS) void reloadInbox();
    };
    document.addEventListener('visibilitychange', onVisible);

    return () => {
      unsubInbox();
      unsubNotif();
      stopInterval();
      unsubResync();
      unsubStatus();
      document.removeEventListener('visibilitychange', onVisible);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCommitteeId]);

  const pendingReports = useMemo(
    () => reports.filter((r) => !resolvedIds.has(r.id) && (r.status || 'pending') === 'pending'),
    [reports, resolvedIds],
  );
  const activity = useMemo(
    () => computeUserActivity(questions, pastQuestions, reports, comments, registeredUsers),
    [questions, pastQuestions, reports, comments, registeredUsers],
  );

  const handleResolve = async (report: InboxReport) => {
    setBusyAction(`resolve-${report.id}`);
    try {
      const res = await resolveInboxReport(adminEmail, report);
      setResolvedIds((prev) => new Set(prev).add(report.id));
      notify(res.message);
    } finally {
      setBusyAction(null);
    }
  };

  const handleEditReport = async (r: InboxReport, updates: { reason: string; details: string }) => {
    setBusyAction(`editreport-${r.id}`);
    try {
      const res = await editInboxReport(adminEmail, r.id, updates, r.questionId);
      if (res.ok) {
        setReports((prev) => prev.map((item) => (item.id === r.id ? { ...item, reason: updates.reason, details: updates.details } : item)));
      }
      notify(res.message);
    } finally {
      setBusyAction(null);
    }
  };

  const handleDeleteReport = async (r: InboxReport) => {
    setReports((prev) => prev.filter((x) => x.id !== r.id));
    setBusyAction(`delreport-${r.id}`);
    try {
      const res = await deleteInboxReport(adminEmail, r.id, r.questionId);
      if (!res.ok) setReports((prev) => [r, ...prev]);
      notify(res.message);
    } finally {
      setBusyAction(null);
    }
  };

  const handleEditComment = async (c: InboxComment, text: string) => {
    setBusyAction(`editcomment-${c.id}`);
    try {
      const res = await editPastComment(adminEmail, c.questionId, c.id, text);
      if (res.ok) {
        setComments((prev) => prev.map((item) => (item.id === c.id ? { ...item, text } : item)));
      }
      notify(res.message);
    } finally {
      setBusyAction(null);
    }
  };

  const handleDeleteComment = async (c: InboxComment) => {
    setComments((prev) => prev.filter((x) => x.id !== c.id));
    setBusyAction(`comment-${c.id}`);
    try {
      const res = await deletePastComment(adminEmail, c.questionId, c.id);
      if (!res.ok) setComments((prev) => [...prev, c]);
      notify(res.message);
    } finally {
      setBusyAction(null);
    }
  };

  const handlePublishDraft = async (d: QuestionItem) => {
    setBusyAction(`publish-${d.id}`);
    try {
      const res = await publishDraft(adminEmail, d);
      if (res.ok) setDrafts((prev) => prev.filter((x) => x.id !== d.id));
      notify(res.message);
      await onRefreshData();
    } finally {
      setBusyAction(null);
    }
  };

  const handleDeleteDraft = async (d: QuestionItem) => {
    setDrafts((prev) => prev.filter((x) => x.id !== d.id));
    setBusyAction(`deldraft-${d.id}`);
    try {
      const res = await deleteDraftEverywhere(adminEmail, d);
      if (!res.ok) setDrafts((prev) => [...prev, d]);
      notify(res.message);
      if (res.ok) await onRefreshData();
    } finally {
      setBusyAction(null);
    }
  };

  const { theme, toggle: toggleTheme } = useTheme();
  const current = SECTIONS.find((s) => s.id === section) || SECTIONS[0];
  const committeeName = committees.find((c) => c.id === selectedCommitteeId)?.name;
  const refreshAll = async () => {
    await onRefreshData();
    await reloadInbox();
  };

  const badgeOf = (id: ManageSection): { n: number; alert?: boolean } | undefined => {
    if (id === 'inbox') return { n: pendingReports.length + comments.length, alert: pendingReports.length > 0 };
    if (id === 'moderation') return pendingReports.length ? { n: pendingReports.length, alert: true } : undefined;
    if (id === 'drafts') return { n: drafts.length };
    if (id === 'users') return { n: registeredUsers.length };
    return undefined;
  };

  // Rozet artınca kısa bir sıçrama (yeni öge geldi)
  const prevBadges = useRef<Partial<Record<ManageSection, number>>>({});
  const bumped = (id: ManageSection, n: number) => {
    const prev = prevBadges.current[id];
    return prev !== undefined && n > prev;
  };
  useEffect(() => {
    for (const s of SECTIONS) {
      const b = badgeOf(s.id);
      prevBadges.current[s.id] = b?.n ?? 0;
    }
  });

  // Sekme başlığı: bölüm + bekleyen bildirim sayısı
  useEffect(() => {
    const prev = document.title;
    return () => {
      document.title = prev;
    };
  }, []);
  useEffect(() => {
    const n = pendingReports.length;
    document.title = `${n ? `(${n}) ` : ''}${current.label} · Yönetim`;
  }, [current.label, pendingReports.length]);

  const syncLabel = lastSync ? new Date(lastSync).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }) : '';
  const liveText = liveStatus === 'connected' ? 'Canlı' : liveStatus === 'connecting' ? 'Bağlanıyor' : 'Bağlantı yok';
  const headBadge = badgeOf(section);

  const renderNav = (filter = '', grid = false) => {
    const q = foldTr(filter.trim());
    const source = look.design === 'v12' ? V12_SECTIONS : SECTIONS;
    const list = source.filter((x) => !q || foldTr(`${x.label} ${x.hint} ${x.keywords || ''} ${x.group}`).includes(q));
    if (!list.length) return <span className="msv-mgrid-empty">Eşleşen bölüm yok</span>;
    return list.map((sec, i) => {
      const on = section === sec.id;
      const groupStart = i === 0 || list[i - 1].group !== sec.group;
      const Icon = sec.icon;
      const badge = badgeOf(sec.id);
      return (
        <React.Fragment key={sec.id}>
          {groupStart && <span className="ms-side-group">{sec.group}</span>}
          <button
            type="button"
            onClick={() => setSection(sec.id)}
            aria-current={on ? 'page' : undefined}
            className={`ms-side-item ${on ? 'is-on' : ''}`}
            title={grid ? undefined : sec.hint}
          >
            <Icon strokeWidth={on ? 2.3 : 1.9} aria-hidden="true" />
            <span className="truncate">{sec.label}</span>
            {badge && badge.n > 0 && (
              <span key={`${sec.id}-${badge.n}`} className={`n ${badge.alert && !on ? 'is-alert' : ''} ${bumped(sec.id, badge.n) ? 'is-bump' : ''}`}>
                {badge.n}
              </span>
            )}
          </button>
        </React.Fragment>
      );
    });
  };
  const [menuQuery, setMenuQuery] = useState('');
  const sideNavRef = useRef<HTMLElement>(null);
  useEffect(() => {
    sideNavRef.current?.querySelector('.ms-side-item.is-on')?.scrollIntoView({ block: 'nearest' });
  }, [section]);

  return (
    <div className={`ms-console w-full bg-canvas overflow-hidden flex text-ink ${fullscreen ? 'h-[var(--vvh,100dvh)]' : 'rounded-2xl min-h-[560px] h-[calc(100dvh-150px)] lg:h-[calc(100dvh-120px)]'}`}>
      {/* Kenar menüsü (v9): marka, bölüm arama, gruplu bölümler */}
      <aside className="ms-side" aria-label="Yönetim menüsü" ref={sideNavRef}>
        <button type="button" onClick={onExit} className="msv-brand" title="Öğrenci sitesine dön">
          <span className="msv-logo" aria-hidden="true">M</span>
          <span className="msv-word">MedSoru</span>
          <span className="msv-role"><ShieldCheck aria-hidden="true" /> Yönetim</span>
        </button>
        <button type="button" onClick={() => setPaletteOpen(true)} className="ms-cpal-btn" aria-label="Bölüme git (Ctrl+K)">
          <Search aria-hidden />
          <span>Bölüme git…</span>
          <kbd>Ctrl K</kbd>
        </button>
        <nav aria-label="Yönetim bölümleri" className="flex flex-col gap-px">
          {renderNav()}
        </nav>
        <span className="flex-1 min-h-4" aria-hidden="true" />
        <button type="button" onClick={onExit} className="ms-side-item">
          <ArrowLeft aria-hidden="true" /> Öğrenci sitesine dön
        </button>
        <div className="msv-me" title={adminEmail}>
          <span className="ms-avatar is-accent !w-6 !h-6 !text-[11px]">{(adminEmail || 'Y').charAt(0).toUpperCase()}</span>
          <span>{adminEmail || 'Yönetici'}</span>
        </div>
      </aside>

      <div className="flex-1 flex flex-col min-h-0 min-w-0">
        <header className="ms-ctop">
          <button type="button" onClick={() => setMenuOpen(true)} className="ms-btn is-ghost ms-menu-btn min-w-0" aria-label={`Bölüm menüsünü aç · ${current.label}`} aria-expanded={menuOpen}>
            <Menu />
            <span className="msv-title truncate">{current.label}</span>
            <ChevronDown className="!w-3.5 !h-3.5 text-ink-3" />
          </button>
          <div className="msv-titlebox">
            <h1 className="msv-title">{current.label}</h1>
            {headBadge && headBadge.n > 0 && <span className={`msv-count ${headBadge.alert ? 'is-alert' : ''}`}>{headBadge.n.toLocaleString('tr-TR')}</span>}
            <span className="msv-hint" title={current.hint}>{current.hint}</span>
          </div>
          <span className="flex-1" />
          <button type="button" onClick={() => setPaletteOpen(true)} className="ms-cpal-btn" aria-label="Bölüm ara (Ctrl+K)">
            <Search aria-hidden />
            <span>Bölüme git…</span>
            <kbd>Ctrl K</kbd>
          </button>
          <span
            className={`msv-live is-${liveStatus}`}
            role="status"
            title={`Canlı kanal: ${liveText}${syncLabel ? ` · son eşitleme ${syncLabel}` : ''}`}
          >
            <i aria-hidden="true" />
            <span>{liveText}</span>
            {syncLabel && <small>{syncLabel}</small>}
          </span>
          {localHost && (
            <Segmented<'oracle' | 'yerel'>
              className="msv-src shrink-0"
              label="Veri kaynağı"
              value={panelTarget}
              onChange={choosePanelTarget}
              options={[
                { value: 'oracle', label: 'Canlı', title: 'Panel canlı siteye (Oracle) bağlı: değişiklikler doğrudan canlıya yazılır' },
                { value: 'yerel', label: 'Yerel', title: 'Panel bu bilgisayardaki sunucuya bağlı (deneme için)' },
              ]}
            />
          )}
          <label className="ms-select-chip min-w-0 max-w-[40vw] sm:max-w-[280px]" title={committeeName}>
            <span className="sr-only">Kurul</span>
            <select value={selectedCommitteeId} onChange={(e) => onSelectCommittee(e.target.value)} className="!text-sm">
              {committees.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
            <ChevronDown className="w-3.5 h-3.5 text-ink-3 shrink-0 pointer-events-none" aria-hidden="true" />
          </label>
          <Segmented<AppDensity>
            className="ms-density shrink-0"
            label="Yoğunluk"
            value={look.density}
            onChange={(d) => look.set({ density: d })}
            options={(['compact', 'normal', 'wide'] as AppDensity[]).map((d) => ({ value: d, label: DENSITY_LABELS[d] }))}
          />
          <button type="button" onClick={() => void refreshAll()} disabled={loading} className="ms-btn is-ghost is-icon shrink-0" title="Verileri yenile" aria-label="Verileri yenile">
            <RefreshCw className={loading ? 'animate-spin' : ''} />
          </button>
          <button type="button" onClick={toggleTheme} className="ms-btn is-ghost is-icon shrink-0 msv-theme" title={theme === 'dark' ? 'Açık tema' : 'Koyu tema'} aria-label="Temayı değiştir">
            {theme === 'dark' ? <Sun /> : <Moon />}
          </button>
          <span className="ms-avatar is-accent ms-me" title={adminEmail}>
            {(adminEmail || 'Y').charAt(0).toUpperCase()}
          </span>
        </header>

        <main
          key={section}
          className="ms-console-body ms-view-enter overscroll-contain flex-1 min-h-0 overflow-y-auto"
          data-density={density}
          aria-label={current.label}
        >
          <div className={`ms-cinner ${section === 'studio' ? '!max-w-none' : ''}`}>
            {/* Telefon/tablet: başlık üst çubukta menü düğmesinde; kısa açıklama burada */}
            <div className="msv-mhead">
              <p>{current.hint}</p>
            </div>

            {section === 'pending' && (
              <ManagePendingOperationsSection />
            )}

            {section === 'inbox' && (
              <ManageMetrics
                loading={loading && !reports.length}
                items={[
                  { id: 'reports', label: 'Bekleyen bildirim', value: pendingReports.length, dates: reports.map((r) => r.createdAt), tone: 'alert', onClick: () => setSection('moderation') },
                  { id: 'drafts', label: 'Taslak', value: drafts.length, dates: drafts.map((d: any) => d.createdAt || d.updatedAt), upIsGood: true, onClick: () => setSection('drafts') },
                  { id: 'comments', label: 'Yorum', value: comments.length, dates: comments.map((c) => c.createdAt), upIsGood: true },
                  { id: 'users', label: 'Kayıtlı kullanıcı', value: registeredUsers.length, dates: registeredUsers.map((u: any) => u.createdAt), upIsGood: true, onClick: () => setSection('users') },
                  { id: 'pool', label: 'Havuz sorusu', value: questions.length, onClick: () => setSection('pool') },
                ]}
              />
            )}

            {section === 'inbox' && (
              <ManageInboxSection
                reports={reports}
                comments={comments}
                drafts={drafts}
                notifications={notifications}
                resolvedIds={resolvedIds}
                busyAction={busyAction}
                loading={loading}
                onReview={(r) => {
                  setFocusReportId(r.id);
                  setSection('moderation');
                }}
                onResolve={(r) => void handleResolve(r)}
                onEditReport={(r, updates) => void handleEditReport(r, updates)}
                onDeleteReport={(r) => void handleDeleteReport(r)}
                onEditComment={(c, text) => void handleEditComment(c, text)}
                onDeleteComment={(c) => void handleDeleteComment(c)}
                onEditDraft={setEditingDraft}
                onPublishDraft={(d) => void handlePublishDraft(d)}
                onDeleteDraft={(d) => void handleDeleteDraft(d)}
                onNavigateToData={(qId, ds) => {
                  const resolvedDs = ds || (qId.startsWith('past-') ? 'past' : 'questions');
                  setDataJump({ id: qId, dsId: resolvedDs });
                  setSection('data');
                }}
              />
            )}

            {section === 'moderation' && (
              <ManageModerationSection
                adminEmail={adminEmail}
                selectedCommitteeId={selectedCommitteeId}
                reports={reports}
                questions={questions}
                pastQuestions={pastQuestions}
                setPastQuestions={setPastQuestions}
                resolvedIds={resolvedIds}
                focusReportId={focusReportId}
                setFocusReportId={setFocusReportId}
                onResolve={handleResolve}
                notify={notify}
                onRefreshData={onRefreshData}
                reloadInbox={reloadInbox}
              />
            )}

            {section === 'catalog' && <ManageCatalogSection adminEmail={adminEmail} />}
            {section === 'data' && (
              <ManageDataSection
                adminEmail={adminEmail}
                questions={questions}
                committees={committees}
                onRefreshData={onRefreshData}
                initialFocusId={dataJump?.id}
                initialDsId={dataJump?.dsId}
                onClearFocus={() => setDataJump(null)}
              />
            )}
            {section === 'phases' && <ManagePhasesSection adminEmail={adminEmail} />}
            {section === 'merges' && <ManageMergesSection adminEmail={adminEmail} />}
            {section === 'raw_pool' && <ManageRawPoolSection adminEmail={adminEmail} />}
            {section === 'intake' && <ManageIntakeSection adminEmail={adminEmail} />}
            {section === 'ders_isci' && <ManageDersIsciSection adminEmail={adminEmail} />}

            {section === 'drafts' && (
              <ManageDraftsSection
                adminEmail={adminEmail}
                adminName="Yönetici"
                committeeId={selectedCommitteeId}
                committeeName={committeeName}
                questions={questions}
                onRefreshData={refreshAll}
                notify={notify}
              />
            )}

            {section === 'studio' && (
              <DraftStudio
                adminEmail={adminEmail}
                committeeId={selectedCommitteeId}
                committeeName={committeeName}
                questions={questions}
                onRefreshData={refreshAll}
                notify={notify}
              />
            )}

            {section === 'pool' && (
              <AdminPanelModal
                variant="embedded"
                tab="questions"
                isOpen
                onClose={onExit}
                adminEmail={adminEmail}
                committees={committees}
                questions={questions}
                selectedCommitteeId={selectedCommitteeId}
                onRefreshData={onRefreshData}
              />
            )}
            {section === 'database' && (
              <AdminPanelModal
                variant="embedded"
                tab="database"
                isOpen
                onClose={onExit}
                adminEmail={adminEmail}
                committees={committees}
                questions={questions}
                selectedCommitteeId={selectedCommitteeId}
                onRefreshData={onRefreshData}
              />
            )}
            {section === 'users' && <SubTabs value={usersTab} onChange={setUsersTab} items={[['activity', 'Katkılar'], ['accounts', 'Hesaplar ve e-posta']]} />}
            {section === 'users' && usersTab === 'accounts' && (
              <AdminPanelModal
                variant="embedded"
                tab="users"
                isOpen
                onClose={onExit}
                adminEmail={adminEmail}
                committees={committees}
                questions={questions}
                selectedCommitteeId={selectedCommitteeId}
                onRefreshData={onRefreshData}
              />
            )}
            {section === 'users' && usersTab === 'activity' && (
              <ManageUsersSection
                adminEmail={adminEmail}
                committees={committees}
                questions={questions}
                pastQuestions={pastQuestions}
                reports={reports}
                comments={comments}
                registeredUsers={registeredUsers}
                setRegisteredUsers={setRegisteredUsers}
                activity={activity}
                notify={notify}
                onRefreshData={onRefreshData}
                reloadInbox={reloadInbox}
              />
            )}

            {section === 'people' && <ManagePeopleSection adminEmail={adminEmail} notify={notify} />}
            {section === 'scripts' && <AdminScriptsTab adminEmail={adminEmail} onRefreshAllData={onRefreshData} />}
            {section === 'system' && <ManageSystemSection notify={notify} />}
            {section === 'datacore' && <ManageDataCoreSection notify={notify} />}
            {section === 'notebooklm' && <ManageNotebookLMSection />}
            {section === 'automation' && <SubTabs value={autoTab} onChange={setAutoTab} items={[['schedule', 'Zamanlama ve anahtarlar'], ['services', 'Drive ve servisler']]} />}
            {section === 'automation' && autoTab === 'schedule' && (
              <ManageAutomationSection adminEmail={adminEmail} selectedCommitteeId={selectedCommitteeId} onRefreshData={onRefreshData} notify={notify} />
            )}
            {section === 'automation' && autoTab === 'services' && (
              <AdminPanelModal
                variant="embedded"
                tab="automations"
                isOpen
                onClose={onExit}
                adminEmail={adminEmail}
                committees={committees}
                questions={questions}
                selectedCommitteeId={selectedCommitteeId}
                onRefreshData={onRefreshData}
              />
            )}
          </div>
        </main>
      </div>

      {paletteOpen && <SectionPalette current={section} onPick={(id) => setSection(id)} onClose={() => setPaletteOpen(false)} badgeOf={badgeOf} />}

      {/* Telefon ve tablet: bölüm menüsü alttan açılır */}
      <Drawer open={menuOpen} onClose={() => { setMenuOpen(false); setMenuQuery(''); }} title="Yönetim" label="Yönetim bölümleri">
        <div className="-mt-1 mb-2">
          <SearchBox value={menuQuery} onChange={setMenuQuery} placeholder="Bölüm ara" label="Bölüm ara" />
        </div>
        <nav aria-label="Yönetim bölümleri" className="msv-mgrid">
          {renderNav(menuQuery, true)}
        </nav>
        <div className="msv-drawer-tools">
          {localHost && (
            <Segmented<'oracle' | 'yerel'>
              label="Veri kaynağı"
              value={panelTarget}
              onChange={choosePanelTarget}
              options={[
                { value: 'oracle', label: 'Canlı' },
                { value: 'yerel', label: 'Yerel' },
              ]}
            />
          )}
          <button type="button" onClick={toggleTheme} className="ms-btn is-sm">
            {theme === 'dark' ? <Sun /> : <Moon />} {theme === 'dark' ? 'Açık tema' : 'Koyu tema'}
          </button>
        </div>
        <button type="button" onClick={onExit} className="ms-side-item mt-2">
          <ArrowLeft aria-hidden="true" /> Öğrenci sitesine dön
        </button>
      </Drawer>

      {editingDraft && (
        <AdminEditQuestionModal
          isOpen
          question={editingDraft}
          adminEmail={adminEmail}
          onClose={() => setEditingDraft(null)}
          onSaveQuestion={async (updated) => {
            await ApiService.adminUpdateQuestion(adminEmail, editingDraft.id, updated);
            setEditingDraft(null);
            notify('Taslak güncellendi.');
            await refreshAll();
          }}
        />
      )}
    </div>
  );
};

/** Bölüm içi alt sekmeler (segment) */
function SubTabs<T extends string>({ value, onChange, items }: { value: T; onChange: (v: T) => void; items: [T, string][] }) {
  return (
    <div role="tablist" className="ds-seg self-start">
      {items.map(([id, label]) => (
        <button key={id} type="button" role="tab" aria-selected={value === id} onClick={() => onChange(id)}>
          {label}
        </button>
      ))}
    </div>
  );
}

/** Ctrl/⌘+K bölüm paleti: yaz, ok tuşlarıyla seç, Enter ile git. Boşken son açılanlar üstte. */
const SectionPalette: React.FC<{
  current: ManageSection;
  onPick: (id: ManageSection) => void;
  onClose: () => void;
  badgeOf: (id: ManageSection) => { n: number; alert?: boolean } | undefined;
}> = ({ current, onPick, onClose, badgeOf }) => {
  const [q, setQ] = useState('');
  const [idx, setIdx] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLUListElement>(null);
  const query = foldTr(q.trim());
  const recent = query ? [] : readRecent().filter((id) => id !== current).slice(0, 4);
  const rows: { sec: (typeof SECTIONS)[number]; head?: string }[] = query
    ? SECTIONS.filter((x) => foldTr(`${x.label} ${x.hint} ${x.keywords || ''} ${x.group}`).includes(query)).map((sec) => ({ sec }))
    : [
        ...recent.map((id, i) => ({ sec: SECTIONS.find((x) => x.id === id)!, head: i === 0 ? 'Son açılanlar' : undefined })),
        ...SECTIONS.filter((x) => !recent.includes(x.id)).map((sec, i, arr) => ({ sec, head: i === 0 || arr[i - 1].group !== sec.group ? sec.group : undefined })),
      ];
  useEffect(() => inputRef.current?.focus(), []);
  useEffect(() => setIdx(0), [q]);
  useEffect(() => {
    listRef.current?.querySelector('button.is-on')?.scrollIntoView({ block: 'nearest' });
  }, [idx]);
  return (
    <div className="ms-overlay ms-cpal-wrap fixed inset-0 z-[90] flex items-start justify-center p-4 pt-[12vh]" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className="ms-cpal ms-keep-shell" role="dialog" aria-modal="true" aria-label="Bölüme git">
        <label className="ms-cpal-in">
          <Search aria-hidden />
          <input
            ref={inputRef}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Bölüm ya da iş ara: taslak, yedek, e-posta…"
            aria-label="Bölüm ara"
            aria-controls="msv-cpal-list"
            aria-activedescendant={rows[idx] ? `msv-cpal-${rows[idx].sec.id}` : undefined}
            onKeyDown={(e) => {
              if (e.key === 'Escape') onClose();
              if (e.key === 'ArrowDown') { e.preventDefault(); setIdx((i) => Math.min(rows.length - 1, i + 1)); }
              if (e.key === 'ArrowUp') { e.preventDefault(); setIdx((i) => Math.max(0, i - 1)); }
              if (e.key === 'Enter' && rows[idx]) onPick(rows[idx].sec.id);
            }}
          />
          <kbd>Esc</kbd>
        </label>
        <ul ref={listRef} id="msv-cpal-list" className="ms-cpal-list" role="listbox" aria-label="Bölümler">
          {rows.map(({ sec: x, head }, i) => {
            const Icon = x.icon;
            const b = badgeOf(x.id);
            return (
              <React.Fragment key={`${head || ''}${x.id}`}>
                {head && <li role="presentation" className="msv-cpal-group">{head}</li>}
                <li role="option" id={`msv-cpal-${x.id}`} aria-selected={i === idx}>
                  <button type="button" tabIndex={-1} onMouseEnter={() => setIdx(i)} onClick={() => onPick(x.id)} className={i === idx ? 'is-on' : ''}>
                    <span className="hk-tile is-sm"><Icon aria-hidden /></span>
                    <span className="ms-cpal-t"><b>{x.label}</b><small>{x.hint}</small></span>
                    {b && b.n > 0 && <span className={`ms-cpal-n ${b.alert ? 'is-alert' : ''}`}>{b.n}</span>}
                    {x.id === current ? <span className="msv-cpal-g">Açık</span> : query ? <span className="msv-cpal-g">{x.group}</span> : null}
                    {i === idx && <CornerDownLeft className="ms-cpal-enter" aria-hidden />}
                  </button>
                </li>
              </React.Fragment>
            );
          })}
          {rows.length === 0 && <li className="ms-cpal-empty">Eşleşen bölüm yok</li>}
        </ul>
        <div className="msv-cpal-foot" aria-hidden="true">
          <span><kbd>↑</kbd><kbd>↓</kbd>seç</span>
          <span><kbd>Enter</kbd>git</span>
          <span><kbd>Alt</kbd><kbd>↑↓</kbd>bölümler arası</span>
          <span><kbd>Ctrl</kbd><kbd>K</kbd>aç/kapat</span>
        </div>
      </div>
    </div>
  );
};
