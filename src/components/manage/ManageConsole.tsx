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
  GraduationCap,
  Database,
  Library,
  HardDrive,
  Search,
  CornerDownLeft,
  Brain,
  Clock,
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
import { ManagePhasesSection } from './ManagePhasesSection';
import { ManageMergesSection } from './ManageMergesSection';
import { ManageInboxSection } from './ManageInboxSection';
import { ManageModerationSection } from './ManageModerationSection';
import { ManageUsersSection } from './ManageUsersSection';
import { ManageSystemSection } from './ManageSystemSection';
import { ManageAutomationSection } from './ManageAutomationSection';
import { ManageDataCoreSection } from './ManageDataCoreSection';
import { ManageNotebookLMSection } from './ManageNotebookLMSection';
import { ManagePendingOperationsSection } from './ManagePendingOperationsSection';
import { consoleLogBuffer } from './ConsoleLogBuffer';
import { ManageMetrics } from './ManageMetrics';
import { useAppearance, DENSITY_LABELS, type Density as AppDensity } from '../../utils/appearance';
import { Segmented } from '../ui/kit';
import { Drawer, classifyNotice } from './consoleUi';
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

export type ManageSection = 'pending' | 'inbox' | 'pool' | 'data' | 'phases' | 'merges' | 'drafts' | 'studio' | 'moderation' | 'users' | 'scripts' | 'system' | 'automation' | 'datacore' | 'notebooklm' | 'database';

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
  { id: 'data', slug: 'tum-veriler', label: 'Tüm veriler', hint: 'Her veri kümesi tek tabloda: ara, sırala, seç, toplu işlem yap, CSV al.', icon: Table2, group: 'İçerik', keywords: 'tablo csv toplu' },
  { id: 'phases', slug: 'fazlar', label: 'Faz verileri', hint: 'Soru bazında faz çıktıları: gez, elle düzelt, arama testini çalıştır.', icon: FlaskConical, group: 'İçerik', keywords: 'faz 14 faz 15' },
  { id: 'merges', slug: 'birlesenler', label: 'Birleştirilen sorular', hint: 'Kopya çıkmış sorular: yan yana karşılaştır, asıl soruyu seç ya da ayır.', icon: GitMerge, group: 'İçerik', keywords: 'kopya birleştir' },
  { id: 'datacore', slug: 'veri-merkezi', label: 'Veri Merkezi (v2)', hint: 'Bağımsız Core v2 hattı: sorular, kazanım, ders notu bağları, kavram grafı, toplu tamamlama.', icon: Database, group: 'İçerik', keywords: 'core kazanım graf' },
  { id: 'notebooklm', slug: 'notebooklm', label: 'NotebookLM Stüdyosu', hint: 'NotebookLM JSON/MD çıktılarını yükle, alternatif olarak sakla, orijinalle karşılaştır ve tercihi seç.', icon: Brain, group: 'İçerik', keywords: 'notebooklm ai json alternatif rag soru deste spot' },
  { id: 'drafts', slug: 'taslaklar', label: 'Taslaklar', hint: 'Öğrenci taslaklarını kümele, birleştir, düzenle ya da AI ile tam soruya dönüştür.', icon: Layers, group: 'İçerik', keywords: 'parça taslak' },
  { id: 'studio', slug: 'studyo', label: 'Taslak stüdyosu', hint: 'Parçaları elle eşle: ağaç, pano, akış ve terim görünümleri.', icon: Workflow, group: 'İçerik', keywords: 'eşle pano' },
  { id: 'users', slug: 'kullanicilar', label: 'Kullanıcılar', hint: 'Katkılar, hesaplar, roller ve e-posta.', icon: Users, group: 'Topluluk', keywords: 'öğrenci hesap rol smtp e-posta' },
  { id: 'scripts', slug: 'betikler', label: 'Betikler', hint: 'Veri hattı betiklerini ve zincirleri çalıştır, çıktıyı canlı izle.', icon: Terminal, group: 'Sistem', keywords: 'script görev zincir' },
  { id: 'system', slug: 'sistem', label: 'Sistem ve günlükler', hint: 'Veritabanı ve AI sağlığı, servisler, tarayıcı konsolu.', icon: Activity, group: 'Sistem', keywords: 'log sağlık servis' },
  { id: 'automation', slug: 'otomasyon', label: 'Otomasyon', hint: 'Zamanlanmış işler, AI pencereleri, anahtarlar; Drive eşitlemesi ve masaüstü servisleri.', icon: Settings, group: 'Sistem', keywords: 'drive yedek anahtar zamanla' },
  { id: 'database', slug: 'veritabani', label: 'Veritabanı ve yedek', hint: 'Etkin veritabanı, eşitleme, dışa ve içe aktarım.', icon: HardDrive, group: 'Sistem', keywords: 'supabase firebase yedek dışa aktar' },
];
const sectionBySlug = (slug?: string) => SECTIONS.find((x) => x.slug === slug || x.id === slug);

// Yoğunluk: uygulamanın görünüm ayarından gelir (Profil ve ayarlar → Kompakt/Normal/Geniş)
type Density = 'comfy' | 'compact' | 'tight';
const SECTION_KEY = 'medsoru_manage_section';
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
    try {
      localStorage.setItem(SECTION_KEY, s);
    } catch {
      /* gizli pencere: bu ziyaretlik */
    }
  };
  const [loading, setLoading] = useState(false);

  // Adres bölümü taşır: açılışta normalize et, geri/ileri ile bölüm değişsin
  useEffect(() => {
    setSection(section, { replace: true });
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
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Gelen kutusu yüklenemedi.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void reloadInbox();
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

  const nav = (
    <>
      {SECTIONS.map((sec, i) => {
        const on = section === sec.id;
        const groupStart = i === 0 || SECTIONS[i - 1].group !== sec.group;
        const Icon = sec.icon;
        const badge = badgeOf(sec.id);
        return (
          <React.Fragment key={sec.id}>
            {groupStart && <span className="ms-side-group">{sec.group}</span>}
            <button type="button" onClick={() => setSection(sec.id)} aria-current={on ? 'page' : undefined} className={`ms-side-item ${on ? 'is-on' : ''}`}>
              <Icon strokeWidth={on ? 2.3 : 2} aria-hidden="true" />
              <span className="truncate">{sec.label}</span>
              {badge && badge.n > 0 && <span className={`n ${badge.alert && !on ? 'is-alert' : ''}`}>{badge.n}</span>}
            </button>
          </React.Fragment>
        );
      })}
    </>
  );

  const brand = (
    <>
      <span className="ms-rail-mark w-[28px] h-[28px] flex items-center justify-center shrink-0">
        <Activity className="w-[17px] h-[17px]" strokeWidth={2.4} />
      </span>
      <span className="ms-rail-word font-display font-bold text-lg tracking-[-0.02em] text-ink">
        Me<span className="text-accent">DS</span>or
      </span>
      <span className="ms-tag is-accent">
        <ShieldCheck /> Yönetim
      </span>
    </>
  );

  return (
    <div className={`ms-console w-full bg-canvas overflow-hidden flex text-ink ${fullscreen ? 'h-[var(--vvh,100dvh)]' : 'rounded-2xl min-h-[560px] h-[calc(100dvh-150px)] lg:h-[calc(100dvh-120px)]'}`}>
      {/* Kenar menüsü: öğrenci sayfalarındaki gibi beyaz, gruplu */}
      <aside className="ms-side" aria-label="Yönetim menüsü">
        <button type="button" onClick={onExit} className="ms-side-brand hover:bg-canvas" title="Siteye dön">
          {brand}
        </button>
        <nav aria-label="Yönetim bölümleri" className="flex flex-col gap-0.5">
          {nav}
        </nav>
        <span className="flex-1 min-h-4" aria-hidden="true" />
        <button type="button" onClick={onExit} className="ms-side-item">
          <GraduationCap aria-hidden="true" /> Öğrenci sitesine dön
        </button>
      </aside>

      <div className="flex-1 flex flex-col min-h-0 min-w-0">
        <header className="ms-ctop">
          <button type="button" onClick={() => setMenuOpen(true)} className="ms-btn is-ghost ms-menu-btn !px-2.5 min-w-0" aria-label="Bölüm menüsünü aç" aria-expanded={menuOpen}>
            <Menu />
            <span className="truncate text-base">{current.label}</span>
            <ChevronDown className="!w-3.5 !h-3.5 text-ink-3" />
          </button>
          <button type="button" onClick={() => setPaletteOpen(true)} className="ms-cpal-btn" aria-label="Bölüm ara (Ctrl+K)">
            <Search aria-hidden />
            <span>Bölüme git…</span>
            <kbd>Ctrl K</kbd>
          </button>
          <span className="flex-1" />
          <label className="ms-select-chip !h-9 min-w-0 max-w-[46vw] sm:max-w-[300px]" title={committeeName}>
            <span className="sr-only">Kurul</span>
            <select value={selectedCommitteeId} onChange={(e) => onSelectCommittee(e.target.value)} className="!text-sm">
              {committees.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
            <ChevronDown className="w-3.5 h-3.5 text-ink-3 shrink-0 pointer-events-none" aria-hidden="true" />
          </label>
          {(
            <Segmented<AppDensity>
              className="ms-density shrink-0"
              label="Yoğunluk"
              value={look.density}
              onChange={(d) => look.set({ density: d })}
              options={(['compact', 'normal', 'wide'] as AppDensity[]).map((d) => ({ value: d, label: DENSITY_LABELS[d] }))}
            />
          )}
          <button type="button" onClick={() => void refreshAll()} disabled={loading} className="ms-btn is-ghost is-icon shrink-0" title="Verileri yenile" aria-label="Verileri yenile">
            <RefreshCw className={loading ? 'animate-spin' : ''} />
          </button>
          <button type="button" onClick={toggleTheme} className="ms-btn is-ghost is-icon shrink-0" title={theme === 'dark' ? 'Açık tema' : 'Koyu tema'} aria-label="Temayı değiştir">
            {theme === 'dark' ? <Sun /> : <Moon />}
          </button>
          <span className="ms-avatar ms-me" title={adminEmail}>
            {(adminEmail || 'Y').charAt(0).toUpperCase()}
          </span>
        </header>

        <main
          key={section}
          className="ms-console-body ms-view-enter overscroll-contain flex-1 min-h-0 overflow-y-auto"
          data-density={density}
        >
          <div className={`ms-cinner ${section === 'studio' ? '!max-w-none' : ''}`}>
            <div className="ms-chead">
              <div className="min-w-0">
                <h1 className="ms-page-title m-0 text-ink">{current.label}</h1>
                <p>{current.hint}</p>
              </div>
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

      {paletteOpen && <SectionPalette onPick={(id) => setSection(id)} onClose={() => setPaletteOpen(false)} badgeOf={badgeOf} />}

      {/* Telefon ve tablet: bölüm menüsü alttan açılır */}
      <Drawer open={menuOpen} onClose={() => setMenuOpen(false)} title="Yönetim" label="Yönetim bölümleri">
        <nav aria-label="Yönetim bölümleri" className="ms-msec -mt-2">
          {nav}
        </nav>
        <button type="button" onClick={onExit} className="ms-side-item">
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

/** Ctrl/⌘+K bölüm paleti: yaz, ok tuşlarıyla seç, Enter ile git */
const SectionPalette: React.FC<{
  onPick: (id: ManageSection) => void;
  onClose: () => void;
  badgeOf: (id: ManageSection) => { n: number; alert?: boolean } | undefined;
}> = ({ onPick, onClose, badgeOf }) => {
  const [q, setQ] = useState('');
  const [idx, setIdx] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const fold = (t: string) => t.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
  const list = SECTIONS.filter((x) => !q.trim() || fold(`${x.label} ${x.hint} ${x.keywords || ''} ${x.group}`).includes(fold(q.trim())));
  useEffect(() => inputRef.current?.focus(), []);
  useEffect(() => setIdx(0), [q]);
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
            onKeyDown={(e) => {
              if (e.key === 'Escape') onClose();
              if (e.key === 'ArrowDown') { e.preventDefault(); setIdx((i) => Math.min(list.length - 1, i + 1)); }
              if (e.key === 'ArrowUp') { e.preventDefault(); setIdx((i) => Math.max(0, i - 1)); }
              if (e.key === 'Enter' && list[idx]) onPick(list[idx].id);
            }}
          />
          <kbd>Esc</kbd>
        </label>
        <ul className="ms-cpal-list" role="listbox" aria-label="Bölümler">
          {list.map((x, i) => {
            const Icon = x.icon;
            const b = badgeOf(x.id);
            return (
              <li key={x.id} role="option" aria-selected={i === idx}>
                <button type="button" onMouseEnter={() => setIdx(i)} onClick={() => onPick(x.id)} className={i === idx ? 'is-on' : ''}>
                  <span className="hk-tile is-sm"><Icon aria-hidden /></span>
                  <span className="ms-cpal-t"><b>{x.label}</b><small>{x.hint}</small></span>
                  {b && b.n > 0 && <span className={`ms-cpal-n ${b.alert ? 'is-alert' : ''}`}>{b.n}</span>}
                  {i === idx && <CornerDownLeft className="ms-cpal-enter" aria-hidden />}
                </button>
              </li>
            );
          })}
          {list.length === 0 && <li className="ms-cpal-empty">Eşleşen bölüm yok</li>}
        </ul>
      </div>
    </div>
  );
};
