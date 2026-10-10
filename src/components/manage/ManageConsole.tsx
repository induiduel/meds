import React, { useEffect, useMemo, useState } from 'react';
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
  Plus,
  Menu,
  ChevronDown,
  GraduationCap,
  Database,
} from 'lucide-react';
import type { QuestionItem, Committee, AdminNotification } from '../../types';
import { ApiService } from '../../services/api';
import { AdminScriptsTab } from '../AdminScriptsTab';
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
import { consoleLogBuffer } from './ConsoleLogBuffer';
import { Drawer, classifyNotice } from './consoleUi';
import {
  InboxReport,
  InboxComment,
  ManageUser,
  loadManageInbox,
  loadManageUsers,
  computeUserActivity,
  resolveInboxReport,
  deletePastComment,
  publishDraft,
  deleteDraftEverywhere,
} from '../../services/manageConsoleService';

export type ManageSection = 'inbox' | 'data' | 'phases' | 'merges' | 'drafts' | 'studio' | 'moderation' | 'users' | 'scripts' | 'system' | 'automation' | 'datacore';

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
}

const SECTIONS: { id: ManageSection; label: string; hint: string; icon: React.ElementType; group: string }[] = [
  { id: 'inbox', label: 'Gelen kutusu', hint: 'Bildirim, yorum, taslak ve sistem uyarıları tek kuyrukta; en yenisi üstte.', icon: Inbox, group: 'Genel' },
  { id: 'moderation', label: 'Moderasyon', hint: 'Şikâyet edilen soruyu gör, düzelt ya da kaldır.', icon: Wrench, group: 'Genel' },
  { id: 'data', label: 'Tüm veriler', hint: 'Her veri kümesi tek tabloda: ara, sırala, seç, toplu işlem yap, CSV al.', icon: Table2, group: 'İçerik' },
  { id: 'phases', label: 'Faz verileri', hint: 'Soru bazında faz çıktıları: gez, elle düzelt, arama testini çalıştır.', icon: FlaskConical, group: 'İçerik' },
  { id: 'merges', label: 'Birleştirilen sorular', hint: 'Kopya çıkmış sorular: yan yana karşılaştır, asıl soruyu seç ya da ayır.', icon: GitMerge, group: 'İçerik' },
  { id: 'datacore', label: 'Veri Merkezi (v2)', hint: 'Bağımsız Core v2 hattı: sorular, kazanım, ders notu bağları, kavram grafı, toplu tamamlama.', icon: Database, group: 'İçerik' },
  { id: 'drafts', label: 'Taslaklar', hint: 'Öğrenci taslaklarını kümele, birleştir, düzenle ya da AI ile tam soruya dönüştür.', icon: Layers, group: 'İçerik' },
  { id: 'studio', label: 'Taslak stüdyosu', hint: 'Parçaları elle eşle: ağaç, pano, akış ve terim görünümleri.', icon: Workflow, group: 'İçerik' },
  { id: 'users', label: 'Kullanıcılar', hint: 'Kayıtlı hesaplar ve kim ne kadar katkı verdi.', icon: Users, group: 'Topluluk' },
  { id: 'scripts', label: 'Betikler', hint: 'Veri hattı betiklerini ve zincirleri çalıştır, çıktıyı canlı izle.', icon: Terminal, group: 'Sistem' },
  { id: 'system', label: 'Sistem ve günlükler', hint: 'Veritabanı ve AI sağlığı, servisler, tarayıcı konsolu.', icon: Activity, group: 'Sistem' },
  { id: 'automation', label: 'Otomasyon', hint: 'Yedek saatleri, AI çalışma pencereleri, anahtarlar ve Drive eşitlemesi.', icon: Settings, group: 'Sistem' },
];

// Yoğunluk: tek ayar konsoldaki tüm liste ve kartları küçültür (cihaz başına hatırlanır)
type Density = 'comfy' | 'compact' | 'tight';
const DENSITY_ZOOM: Record<Density, number> = { comfy: 1, compact: 0.92, tight: 0.84 };
const DENSITY_LABEL: Record<Density, string> = { comfy: 'Rahat', compact: 'Kompakt', tight: 'Sıkı' };
const readDensity = (): Density => {
  try {
    const v = localStorage.getItem('medsoru_manage_density');
    return v === 'compact' || v === 'tight' ? v : 'comfy';
  } catch {
    return 'comfy';
  }
};
const SECTION_KEY = 'medsoru_manage_section';
const readSection = (): ManageSection => {
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
}) => {
  const [section, setSectionState] = useState<ManageSection>(readSection);
  const [density, setDensityState] = useState<Density>(readDensity);
  const [menuOpen, setMenuOpen] = useState(false);
  const setSection = (s: ManageSection) => {
    setSectionState(s);
    setMenuOpen(false);
    try {
      localStorage.setItem(SECTION_KEY, s);
    } catch {
      /* gizli pencere: bu ziyaretlik */
    }
  };
  const setDensity = (d: Density) => {
    setDensityState(d);
    try {
      localStorage.setItem('medsoru_manage_density', d);
    } catch {
      /* gizli pencere: bu ziyaretlik */
    }
  };
  const [loading, setLoading] = useState(false);

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
      <span className="w-[34px] h-[34px] rounded-[10px] bg-accent text-white flex items-center justify-center shrink-0">
        <Plus className="w-[18px] h-[18px]" strokeWidth={2.8} />
      </span>
      <span className="font-display font-bold text-[19px] tracking-[-0.02em] text-ink">
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
            <span className="truncate text-[14px]">{current.label}</span>
            <ChevronDown className="!w-3.5 !h-3.5 text-ink-3" />
          </button>
          <span className="flex-1" />
          <label className="ms-select-chip !h-9 min-w-0 max-w-[46vw] sm:max-w-[300px]" title={committeeName}>
            <span className="sr-only">Kurul</span>
            <select value={selectedCommitteeId} onChange={(e) => onSelectCommittee(e.target.value)} className="!text-[13px]">
              {committees.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
            <ChevronDown className="w-3.5 h-3.5 text-ink-3 shrink-0 pointer-events-none" aria-hidden="true" />
          </label>
          <div role="radiogroup" aria-label="Yoğunluk" className="ms-seg ms-density shrink-0">
            {(['comfy', 'compact', 'tight'] as Density[]).map((d) => (
              <button key={d} type="button" role="radio" aria-checked={density === d} onClick={() => setDensity(d)}>
                {DENSITY_LABEL[d]}
              </button>
            ))}
          </div>
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
          style={{ zoom: DENSITY_ZOOM[density] } as React.CSSProperties}
        >
          <div className={`ms-cinner ${section === 'studio' ? '!max-w-none' : ''}`}>
            <div className="ms-chead">
              <div className="min-w-0">
                <h1 className="ms-page-title m-0 text-ink">{current.label}</h1>
                <p>{current.hint}</p>
              </div>
            </div>

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

            {section === 'users' && (
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
            {section === 'automation' && (
              <ManageAutomationSection adminEmail={adminEmail} selectedCommitteeId={selectedCommitteeId} onRefreshData={onRefreshData} notify={notify} />
            )}
          </div>
        </main>
      </div>

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
