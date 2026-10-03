import React, { useEffect, useMemo, useState } from 'react';
import {
  ShieldCheck,
  Inbox,
  Wrench,
  Users,
  Terminal,
  Activity,
  Settings,
  Search,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  Flag,
  MessageSquare,
  FileText,
  Bell,
  Eye,
  Layers,
  Mail,
  Save,
  Plus,
  Trash2,
  Key,
  Clock,
  Copy,
  Check,
  X,
  Send,
  Radio,
  Server,
} from 'lucide-react';
import type { QuestionItem, Committee, QuestionOption } from '../../types';
import { ApiService } from '../../services/api';
import { multiDbManager } from '../../services/multiDbManager';
import { systemHealthMonitor, SystemOverallHealth } from '../../services/systemHealthMonitor';
import { AdminScriptsTab } from '../AdminScriptsTab';
import { AdminDriveSyncSettings } from '../AdminDriveSyncSettings';
import { AdminEditQuestionModal } from '../AdminEditQuestionModal';
import { ManageDraftsSection } from './ManageDraftsSection';
import { consoleLogBuffer, ManageLogEntry } from './ConsoleLogBuffer';
import {
  DEFAULT_MANAGE_SETTINGS,
  ManageAutomationSettings,
  getAiKeys,
  saveAiKeys,
  loadManageSettings,
  saveManageSettings,
} from '../../services/manageSettingsService';
import {
  InboxReport,
  InboxComment,
  UserActivityRow,
  loadManageInbox,
  loadManageUsers,
  normKey,
  computeUserActivity,
  resolveInboxReport,
  deletePastComment,
  publishDraft,
  deleteDraftEverywhere,
  fetchSystemServices,
  fetchWorkerHeartbeat,
  triggerBackupNow,
  sendUserEmail,
  deleteManageUser,
  purgeAuthorContributions,
  ManageServiceItem,
} from '../../services/manageConsoleService';

export type ManageSection = 'inbox' | 'drafts' | 'moderation' | 'users' | 'scripts' | 'system' | 'automation';

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

const SECTIONS: { id: ManageSection; label: string; hint: string; icon: React.ElementType }[] = [
  { id: 'inbox', label: 'Gelen Kutusu', hint: 'Bildirim, yorum, taslak ve uyarılar', icon: Inbox },
  { id: 'drafts', label: 'Taslaklar', hint: 'Topla, birleştir, sil, düzenle, AI ile dönüştür', icon: Layers },
  { id: 'moderation', label: 'Moderasyon', hint: 'Hatalı soruyu gör ve düzelt', icon: Wrench },
  { id: 'users', label: 'Kullanıcılar', hint: 'Kim ne kadar işlem yaptı', icon: Users },
  { id: 'scripts', label: 'Scriptler', hint: 'İstediğin betiği çalıştır', icon: Terminal },
  { id: 'system', label: 'Sistem & Loglar', hint: 'Hatalar, AI limitleri, konsol', icon: Activity },
  { id: 'automation', label: 'Otomasyon', hint: 'Yedek saati, AI anahtarı, çalışma penceresi', icon: Settings },
];

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
  const [section, setSection] = useState<ManageSection>('inbox');
  const [loading, setLoading] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  // Inbox data
  const [reports, setReports] = useState<InboxReport[]>([]);
  const [comments, setComments] = useState<InboxComment[]>([]);
  const [pastQuestions, setPastQuestions] = useState<QuestionItem[]>([]);
  const [notifications, setNotifications] = useState<import('../../types').AdminNotification[]>([]);
  const [drafts, setDrafts] = useState<QuestionItem[]>([]);
  const [resolvedIds, setResolvedIds] = useState<Set<string>>(new Set());
  const [inboxFilter, setInboxFilter] = useState<'all' | 'reports' | 'comments' | 'drafts' | 'notifications'>('all');
  const [reportStatus, setReportStatus] = useState<'pending' | 'resolved' | 'all'>('pending');
  const [inboxQuery, setInboxQuery] = useState('');
  const [busyAction, setBusyAction] = useState<string | null>(null);

  // Moderation
  const [selectedReportId, setSelectedReportId] = useState<string>('');
  const [modStem, setModStem] = useState('');
  const [modAnswer, setModAnswer] = useState('A');
  const [modExplanation, setModExplanation] = useState('');
  const [isSavingMod, setIsSavingMod] = useState(false);
  const [editingDraft, setEditingDraft] = useState<QuestionItem | null>(null);

  // Users
  const [registeredUsers, setRegisteredUsers] = useState<Array<{ uid?: string; email?: string; displayName?: string; studentNumber?: string; role?: string; createdAt?: string; lastLoginAt?: string }>>([]);
  const [userQuery, setUserQuery] = useState('');
  const [selectedUserKey, setSelectedUserKey] = useState<string | null>(null);
  const [mailUserKey, setMailUserKey] = useState<string | null>(null);
  const [mailSubject, setMailSubject] = useState('');
  const [mailBody, setMailBody] = useState('');
  const [sendingMail, setSendingMail] = useState(false);
  const [confirmDeleteUserKey, setConfirmDeleteUserKey] = useState<string | null>(null);
  const [confirmPurgeKey, setConfirmPurgeKey] = useState<string | null>(null);

  // Kayıt defteri eşleşmesi: e-posta, uid veya görünen ad.
  const regOf = (u: UserActivityRow) =>
    registeredUsers.find(
      (r) =>
        (r.email && normKey(r.email) === u.key) ||
        (r.uid && normKey(r.uid) === u.key) ||
        (r.displayName && normKey(r.displayName) === u.key) ||
        (u.email && r.email && normKey(r.email) === normKey(u.email))
    );

  // System
  const [health, setHealth] = useState<SystemOverallHealth>(() => systemHealthMonitor.getHealth());
  const [isDiagnosing, setIsDiagnosing] = useState(false);
  const [services, setServices] = useState<ManageServiceItem[]>([]);
  const [servicesSummary, setServicesSummary] = useState<{ totalServices: number; activeServicesCount: number; stoppedServicesCount: number } | undefined>(undefined);
  const [isLoadingServices, setIsLoadingServices] = useState(false);
  const [heartbeat, setHeartbeat] = useState<{ isOnline: boolean; diffSeconds?: number; message: string } | null>(null);
  const [logs, setLogs] = useState<ManageLogEntry[]>(() => consoleLogBuffer.getEntries());
  const [logLevel, setLogLevel] = useState<'all' | ManageLogEntry['level']>('all');
  const [copiedLogs, setCopiedLogs] = useState(false);
  const [realtimeResult, setRealtimeResult] = useState<{ running: boolean; message?: string }>({ running: false });

  // Automation
  const [settings, setSettings] = useState<ManageAutomationSettings>({ ...DEFAULT_MANAGE_SETTINGS });
  const [aiKeys, setAiKeys] = useState(() => getAiKeys());
  const [isSavingSettings, setIsSavingSettings] = useState(false);
  const [isBackingUp, setIsBackingUp] = useState(false);
  const [newBackupHour, setNewBackupHour] = useState('03:00');

  useEffect(() => {
    consoleLogBuffer.install();
    const unsubLogs = consoleLogBuffer.subscribe(setLogs);
    const unsubHealth = systemHealthMonitor.subscribe(setHealth);
    return () => {
      unsubLogs();
      unsubHealth();
    };
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
      const users = await loadManageUsers(adminEmail).catch(() => []);
      setRegisteredUsers(users || []);
      const auto = await loadManageSettings();
      setSettings(auto);
      setAiKeys(getAiKeys());
    } catch (e) {
      setNotice(e instanceof Error ? e.message : 'Gelen kutusu yüklenemedi.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    reloadInbox();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCommitteeId]);

  useEffect(() => {
    if (section === 'system' && services.length === 0 && !isLoadingServices) {
      void handleLoadServices();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [section]);

  const pendingReports = useMemo(
    () => reports.filter((r) => !resolvedIds.has(r.id) && (r.status || 'pending') === 'pending'),
    [reports, resolvedIds]
  );
  const resolvedReports = useMemo(
    () => reports.filter((r) => resolvedIds.has(r.id) || (r.status || 'pending') !== 'pending'),
    [reports, resolvedIds]
  );
  const visibleReports = reportStatus === 'pending' ? pendingReports : reportStatus === 'resolved' ? resolvedReports : reports;

  const activity = useMemo(
    () => computeUserActivity(questions, pastQuestions, reports, comments, registeredUsers),
    [questions, pastQuestions, reports, comments, registeredUsers]
  );

  const filteredUsers = useMemo(() => {
    const q = userQuery.toLowerCase().trim();
    if (!q) return activity;
    return activity.filter(
      (u) => u.name.toLowerCase().includes(q) || (u.email || '').toLowerCase().includes(q)
    );
  }, [activity, userQuery]);

  const selectedReport = useMemo(
    () => reports.find((r) => r.id === (selectedReportId || pendingReports[0]?.id)) || null,
    [reports, selectedReportId, pendingReports]
  );

  const moderatedQuestion: QuestionItem | null = useMemo(() => {
    if (!selectedReport) return null;
    return (
      pastQuestions.find((q) => q.id === selectedReport.questionId) ||
      questions.find((q) => q.id === selectedReport.questionId) ||
      null
    );
  }, [selectedReport, pastQuestions, questions]);

  useEffect(() => {
    if (moderatedQuestion) {
      setModStem(
        moderatedQuestion.reconstruction?.stem ||
          moderatedQuestion.stem ||
          moderatedQuestion.fragments?.[0]?.text ||
          ''
      );
      setModAnswer(
        moderatedQuestion.reconstruction?.correctAnswer || moderatedQuestion.claimedAnswer || 'A'
      );
      setModExplanation(moderatedQuestion.reconstruction?.explanation || '');
      if (!selectedReportId && selectedReport) setSelectedReportId(selectedReport.id);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [moderatedQuestion?.id]);

  const qLower = inboxQuery.toLowerCase().trim();
  const matchQ = (s: string | undefined) => !qLower || (s || '').toLowerCase().includes(qLower);

  const handleResolve = async (report: InboxReport) => {
    setBusyAction(`resolve-${report.id}`);
    try {
      const res = await resolveInboxReport(adminEmail, report);
      setResolvedIds((prev) => new Set(prev).add(report.id));
      setNotice(res.message);
    } finally {
      setBusyAction(null);
    }
  };

  const handleDeleteComment = async (c: InboxComment) => {
    setComments((prev) => prev.filter((x) => x.id !== c.id));
    setBusyAction(`comment-${c.id}`);
    try {
      const res = await deletePastComment(adminEmail, c.questionId, c.id);
      if (!res.ok) {
        setComments((prev) => [...prev, c]);
      }
      setNotice(res.message);
    } finally {
      setBusyAction(null);
    }
  };

  const handlePublishDraft = async (d: QuestionItem) => {
    setBusyAction(`publish-${d.id}`);
    try {
      const res = await publishDraft(adminEmail, d);
      if (res.ok) {
        setDrafts((prev) => prev.filter((x) => x.id !== d.id));
      }
      setNotice(res.message);
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
      if (!res.ok) {
        setDrafts((prev) => [...prev, d]);
      }
      setNotice(res.message);
      if (res.ok) await onRefreshData();
    } finally {
      setBusyAction(null);
    }
  };

  const handleLoadServices = async () => {
    setIsLoadingServices(true);
    try {
      const [svc, hb] = await Promise.all([fetchSystemServices(), fetchWorkerHeartbeat()]);
      setServices(svc.services);
      setServicesSummary(svc.summary);
      setHeartbeat(hb);
      if (!svc.ok) setNotice(svc.message);
    } finally {
      setIsLoadingServices(false);
    }
  };

  const handleBackupNow = async () => {
    setIsBackingUp(true);
    try {
      const res = await triggerBackupNow(adminEmail);
      setNotice(res.message);
    } finally {
      setIsBackingUp(false);
    }
  };

  const handleDeleteUser = async (u: UserActivityRow) => {
    // Kayıt defteri eşleşmesi: e-posta, uid veya görünen ad (katkılar isimle de yazılır).
    const reg = regOf(u);
    if (!reg?.uid) {
      setNotice('Bu kullanıcı kayıt defterinde bulunamadı. Yalnızca isimsiz katkı izi olabilir; önce listeyi yenileyin.');
      return;
    }
    setBusyAction(`deluser-${u.key}`);
    try {
      const res = await deleteManageUser(adminEmail, reg.uid);
      if (res.ok) {
        setRegisteredUsers((prev) => prev.filter((r) => r.uid !== reg.uid));
        if (selectedUserKey === u.key) setSelectedUserKey(null);
      }
      setNotice(res.message);
    } finally {
      setBusyAction(null);
      setConfirmDeleteUserKey(null);
    }
  };

  const handlePurgeAuthor = async (u: UserActivityRow) => {
    setBusyAction(`purge-${u.key}`);
    try {
      const res = await purgeAuthorContributions(committees, u.key);
      setNotice(res.message);
      if (res.ok) {
        setConfirmPurgeKey(null);
        if (selectedUserKey === u.key) setSelectedUserKey(null);
        await onRefreshData();
        await reloadInbox();
      }
    } finally {
      setBusyAction(null);
    }
  };

  const handleSendMail = async () => {
    const u = activity.find((x) => x.key === mailUserKey);
    const to = u?.email || '';
    if (!to || !mailSubject.trim() || !mailBody.trim()) {
      setNotice('Alıcı, konu ve mesaj zorunludur.');
      return;
    }
    setSendingMail(true);
    try {
      const res = await sendUserEmail(to, mailSubject.trim(), mailBody.trim());
      setNotice(res.message);
      if (res.ok) {
        setMailUserKey(null);
        setMailSubject('');
        setMailBody('');
      }
    } finally {
      setSendingMail(false);
    }
  };

  const handleSaveModeration = async () => {
    if (!moderatedQuestion || !selectedReport) return;
    setIsSavingMod(true);
    try {
      if (moderatedQuestion.isPastExam || pastQuestions.some((q) => q.id === moderatedQuestion.id)) {
        const updated: QuestionItem = {
          ...moderatedQuestion,
          reconstruction: {
            stem: modStem.trim(),
            options:
              moderatedQuestion.reconstruction?.options ||
              (moderatedQuestion.options || []).map((o: QuestionOption) => ({ key: o.key, text: o.text })),
            correctAnswer: modAnswer as 'A' | 'B' | 'C' | 'D' | 'E',
            explanation: modExplanation.trim(),
            confidenceScore: moderatedQuestion.reconstruction?.confidenceScore ?? 90,
            lastUpdated: new Date().toISOString(),
          },
          claimedAnswer: modAnswer as 'A' | 'B' | 'C' | 'D' | 'E',
          status: 'completed',
          updatedAt: new Date().toISOString(),
        };
        await ApiService.saveApprovedPastQuestion(updated);
        setPastQuestions((prev) => prev.map((q) => (q.id === updated.id ? updated : q)));
      } else {
        const updated = await ApiService.adminUpdateQuestion(adminEmail, moderatedQuestion.id, {
          reconstruction: {
            stem: modStem.trim(),
            options:
              moderatedQuestion.reconstruction?.options ||
              (moderatedQuestion.options || []).map((o: QuestionOption) => ({ key: o.key, text: o.text })),
            correctAnswer: modAnswer as 'A' | 'B' | 'C' | 'D' | 'E',
            explanation: modExplanation.trim(),
            confidenceScore: moderatedQuestion.reconstruction?.confidenceScore ?? 90,
            lastUpdated: new Date().toISOString(),
          },
          claimedAnswer: modAnswer as 'A' | 'B' | 'C' | 'D' | 'E',
          status: 'completed',
        });
        void updated;
      }
      setResolvedIds((prev) => new Set(prev).add(selectedReport.id));
      setNotice(`Soru düzeltildi ve "${selectedReport.reason}" bildirimi kapatıldı.`);
      await onRefreshData();
      await reloadInbox();
    } catch (e) {
      setNotice(e instanceof Error ? e.message : 'Düzeltme kaydedilemedi.');
    } finally {
      setIsSavingMod(false);
    }
  };

  const handleRunDiagnostics = async () => {
    setIsDiagnosing(true);
    try {
      await systemHealthMonitor.runFullDiagnostic(true, true);
    } finally {
      setIsDiagnosing(false);
    }
  };

  const handleRealtimeTest = async () => {
    setRealtimeResult({ running: true });
    try {
      const res = await multiDbManager.testRealtimeRoundtrip(4500);
      setRealtimeResult({ running: false, message: res.message });
    } catch (e) {
      setRealtimeResult({ running: false, message: e instanceof Error ? e.message : 'Test başarısız.' });
    }
  };

  const handleSaveAutomation = async () => {
    setIsSavingSettings(true);
    try {
      saveAiKeys(aiKeys);
      const res = await saveManageSettings(adminEmail, settings);
      setNotice(res.message);
    } finally {
      setIsSavingSettings(false);
    }
  };

  const current = SECTIONS.find((s) => s.id === section) || SECTIONS[0];

  return (
    <div className={`w-full bg-white overflow-hidden grid text-ink ${
      fullscreen
        ? 'h-dvh min-h-dvh grid-cols-[minmax(0,1fr)] grid-rows-[auto_minmax(0,1fr)] lg:grid-rows-1 lg:grid-cols-[264px_minmax(0,1fr)]'
        : 'rounded-[18px] border border-line min-h-[560px] h-[calc(100dvh-150px)] lg:h-[calc(100dvh-120px)] grid-cols-[minmax(0,1fr)] grid-rows-[auto_minmax(0,1fr)] lg:grid-rows-1 lg:grid-cols-[248px_minmax(0,1fr)]'
    }`}>
      <aside className="bg-canvas border-b lg:border-b-0 lg:border-r border-line flex lg:flex-col min-w-0">
        <div className="hidden lg:flex items-center gap-2.5 px-5 pt-5 pb-4">
          <span className="w-9 h-9 rounded-[10px] bg-ink text-white flex items-center justify-center shrink-0">
            <ShieldCheck className="w-[18px] h-[18px]" />
          </span>
          <div className="min-w-0">
            <div className="font-display font-bold text-[17px] tracking-[-0.02em] leading-tight">Yönetim Konsolu</div>
            <div className="text-[12px] text-ink-3 truncate" title={adminEmail}>manage · {adminEmail}</div>
          </div>
        </div>
        <nav aria-label="Yönetim bölümleri" className="flex lg:flex-col gap-1 px-2 py-2 lg:px-3 lg:py-0 overflow-x-auto flex-1 min-w-0">
          {SECTIONS.map((sec) => {
            const on = section === sec.id;
            const Icon = sec.icon;
            const badge =
              sec.id === 'inbox'
                ? pendingReports.length + comments.length
                : sec.id === 'drafts'
                  ? drafts.length
                  : sec.id === 'users'
                    ? activity.length
                    : undefined;
            return (
              <button
                key={sec.id}
                type="button"
                onClick={() => setSection(sec.id)}
                aria-current={on ? 'page' : undefined}
                className={`shrink-0 lg:w-full min-h-10 px-3 rounded-[10px] flex items-center gap-2.5 text-left cursor-pointer transition-colors ${
                  on ? 'bg-white text-ink font-semibold shadow-[0_1px_2px_rgba(14,26,38,0.08)]' : 'text-ink-2 hover:text-ink hover:bg-white/60'
                }`}
              >
                <Icon className={`w-[18px] h-[18px] shrink-0 ${on ? 'text-accent' : ''}`} />
                <span className="text-[14px] whitespace-nowrap flex-1">{sec.label}</span>
                {badge !== undefined && badge > 0 && (
                  <span className="hidden lg:inline font-mono text-[12px] text-ink-3">{badge}</span>
                )}
              </button>
            );
          })}
        </nav>
        <button
          type="button"
          onClick={onExit}
          className="shrink-0 m-2 h-10 px-3 rounded-[10px] border border-line text-ink-2 hover:text-ink text-[13px] font-semibold cursor-pointer"
        >
          Siteye dön
        </button>
      </aside>

      <div className="flex flex-col min-h-0 min-w-0">
        <header className="flex items-center gap-3 px-4 sm:px-6 py-3 sm:py-4 border-b border-line shrink-0">
          <div className="min-w-0 flex-1">
            <h2 className="m-0 font-display font-bold text-[20px] sm:text-[22px] tracking-[-0.02em] leading-tight">{current.label}</h2>
            <p className="m-0 text-[13px] text-ink-2 truncate">{current.hint}</p>
          </div>
          <label className="sr-only" htmlFor="manage-committee">Kurul</label>
          <select
            id="manage-committee"
            value={selectedCommitteeId}
            onChange={(e) => onSelectCommittee(e.target.value)}
            className="h-10 border border-line-2 rounded-[10px] px-2.5 text-[13px] bg-white cursor-pointer max-w-[220px]"
          >
            {committees.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
          <button
            type="button"
            onClick={() => { void reloadInbox(); void onRefreshData(); }}
            disabled={loading}
            className="h-10 w-10 rounded-[10px] border border-line inline-flex items-center justify-center text-ink-2 hover:text-ink cursor-pointer disabled:opacity-50"
            title="Yenile"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </header>

        {notice && (
          <div role="status" className="mx-4 sm:mx-6 mt-3 px-4 py-2.5 rounded-xl bg-ok-soft text-[14px] text-ink flex items-center justify-between gap-3 shrink-0">
            <span className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-ok shrink-0" />
              {notice}
            </span>
            <button type="button" onClick={() => setNotice(null)} className="h-8 px-2 rounded-lg text-ok font-semibold text-[13px] cursor-pointer">Kapat</button>
          </div>
        )}

        <div className="flex-1 min-h-0 overflow-y-auto px-4 sm:px-6 py-4">
          {section === 'inbox' && (
            <div className="flex flex-col gap-3">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {[
                  { label: 'Bekleyen bildirim', n: pendingReports.length, icon: Flag },
                  { label: 'Yorum', n: comments.length, icon: MessageSquare },
                  { label: 'Taslak', n: drafts.length, icon: FileText },
                  { label: 'Sistem uyarısı', n: notifications.filter((x) => !x.isRead).length, icon: Bell },
                ].map((s) => (
                  <div key={s.label} className="rounded-xl border border-line px-3 py-2.5 flex items-center gap-2">
                    <s.icon className="w-4 h-4 text-ink-3 shrink-0" />
                    <div>
                      <div className="text-[12px] text-ink-2">{s.label}</div>
                      <div className="font-mono text-[20px] leading-tight">{s.n}</div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex flex-col md:flex-row gap-2">
                <label className="flex items-center gap-2 h-10 px-3 border border-line-2 rounded-[10px] bg-field flex-1 min-w-0">
                  <Search className="w-4 h-4 text-ink-2 shrink-0" />
                  <span className="sr-only">Gelen kutusunda ara</span>
                  <input value={inboxQuery} onChange={(e) => setInboxQuery(e.target.value)} placeholder="Bildirim, yorum, taslak ara" className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[14px]" />
                </label>
                <div role="radiogroup" aria-label="Kutu filtresi" className="inline-flex gap-1 bg-canvas rounded-[10px] p-[3px] shrink-0 overflow-x-auto">
                  {([['all', 'Tümü'], ['reports', 'Bildirim'], ['comments', 'Yorum'], ['drafts', 'Taslak'], ['notifications', 'Uyarı']] as const).map(([id, label]) => (
                    <button key={id} type="button" role="radio" aria-checked={inboxFilter === id} onClick={() => setInboxFilter(id)}
                      className={`h-8 px-2.5 rounded-lg text-[13px] cursor-pointer whitespace-nowrap ${inboxFilter === id ? 'bg-white font-semibold shadow text-ink' : 'text-ink-2'}`}>{label}</button>
                  ))}
                </div>
              </div>

              {(inboxFilter === 'all' || inboxFilter === 'reports') && (
                <section className="rounded-xl border border-line overflow-hidden">
                  <header className="px-3 py-2 bg-canvas flex items-center gap-2">
                    <Flag className="w-4 h-4" />
                    <span className="text-[13px] font-semibold flex-1">Hata bildirimleri ({visibleReports.length})</span>
                    <div role="radiogroup" aria-label="Bildirim durumu" className="inline-flex gap-1 bg-white rounded-[10px] p-[3px] border border-line-soft">
                      {([['pending', 'Bekleyen'], ['resolved', 'Çözülen'], ['all', 'Tümü']] as const).map(([id, label]) => (
                        <button key={id} type="button" role="radio" aria-checked={reportStatus === id} onClick={() => setReportStatus(id)}
                          className={`h-7 px-2 rounded-lg text-[12px] cursor-pointer ${reportStatus === id ? 'bg-ink text-white font-semibold' : 'text-ink-2'}`}>{label}</button>
                      ))}
                    </div>
                  </header>
                  {visibleReports.filter((r) => matchQ(r.reason + ' ' + (r.details || '') + ' ' + (r.questionTopic || ''))).slice(0, 30).map((r) => {
                    const done = resolvedIds.has(r.id) || (r.status || 'pending') !== 'pending';
                    return (
                      <div key={r.id} className="px-3 py-2.5 border-t border-line-soft flex flex-col sm:flex-row sm:items-center gap-2">
                        <div className="flex-1 min-w-0">
                          <div className="text-[14px] font-semibold truncate">{r.reason} · {r.questionTopic || r.questionId}</div>
                          <div className="text-[13px] text-ink-2 line-clamp-2">{r.details || 'Detay yok'}</div>
                          <div className="text-[12px] text-ink-3">{r.reportedBy || 'Anonim'} · {r.createdAt ? new Date(r.createdAt).toLocaleString('tr-TR') : ''}{done ? ' · çözüldü' : ''}</div>
                        </div>
                        <div className="flex gap-1.5 shrink-0">
                          <button type="button" onClick={() => { setSelectedReportId(r.id); setSection('moderation'); }} className="h-9 px-3 rounded-[10px] border border-line text-[13px] font-semibold inline-flex items-center gap-1 cursor-pointer"><Eye className="w-3.5 h-3.5" /> İncele & Düzelt</button>
                          {!done && (
                            <button type="button" onClick={() => { void handleResolve(r); }} disabled={busyAction === `resolve-${r.id}`} className="h-9 px-3 rounded-[10px] bg-ok text-white text-[13px] font-semibold cursor-pointer disabled:opacity-50">Çözüldü</button>
                          )}
                        </div>
                      </div>
                    );
                  })}
                  {visibleReports.length === 0 && <p className="m-0 px-3 py-6 text-center text-[14px] text-ink-2">Bu filtrede bildirim yok.</p>}
                </section>
              )}

              {(inboxFilter === 'all' || inboxFilter === 'comments') && (
                <section className="rounded-xl border border-line overflow-hidden">
                  <header className="px-3 py-2 bg-canvas text-[13px] font-semibold flex items-center gap-2"><MessageSquare className="w-4 h-4" /> Yorumlar ({comments.length})</header>
                  {comments.filter((c) => matchQ(c.text + ' ' + c.author)).slice(0, 30).map((c) => (
                    <div key={c.id} className="px-3 py-2.5 border-t border-line-soft flex items-start gap-2">
                      <div className="flex-1 min-w-0">
                        <div className="text-[14px] leading-snug">{c.text}</div>
                        <div className="text-[12px] text-ink-3 mt-0.5">{c.author} · {c.questionTopic || c.questionId}</div>
                      </div>
                      <button type="button" onClick={() => { void handleDeleteComment(c); }} disabled={busyAction === `comment-${c.id}`} title="Yorumu sil"
                        className="h-8 px-2.5 rounded-lg border border-line text-[12px] font-semibold text-ink-2 hover:text-[#B4233C] hover:border-[#FECDCA] cursor-pointer shrink-0 disabled:opacity-50">Sil</button>
                    </div>
                  ))}
                  {comments.length === 0 && <p className="m-0 px-3 py-6 text-center text-[14px] text-ink-2">Yorum yok.</p>}
                </section>
              )}

              {(inboxFilter === 'all' || inboxFilter === 'drafts') && (
                <section className="rounded-xl border border-line overflow-hidden">
                  <header className="px-3 py-2 bg-canvas text-[13px] font-semibold flex items-center gap-2"><FileText className="w-4 h-4" /> Taslak sorular ({drafts.length})</header>
                  {drafts.filter((d) => matchQ(d.topic + ' ' + d.discipline)).slice(0, 30).map((d) => (
                    <div key={d.id} className="px-3 py-2.5 border-t border-line-soft flex items-center gap-2">
                      <span className="font-mono text-[13px] text-ink-2 w-12 shrink-0">{d.isUnassignedNumber ? '—' : d.questionNumber || '?'}</span>
                      <div className="flex-1 min-w-0">
                        <div className="text-[14px] font-medium truncate">{d.topic || d.discipline}</div>
                        <div className="text-[12px] text-ink-3 truncate">{d.discipline} · {d.fragments?.length || 0} parça · {d.options?.length || 0} şık</div>
                      </div>
                      <div className="flex gap-1.5 shrink-0">
                        <button type="button" onClick={() => setEditingDraft(d)} className="h-9 px-3 rounded-[10px] border border-line text-[13px] font-semibold cursor-pointer">Düzenle</button>
                        <button type="button" onClick={() => { void handlePublishDraft(d); }} disabled={busyAction === `publish-${d.id}`} title="Taslağı onayla ve yayınla"
                          className="h-9 px-3 rounded-[10px] bg-ok text-white text-[13px] font-semibold inline-flex items-center gap-1 cursor-pointer disabled:opacity-50"><Send className="w-3.5 h-3.5" /> Yayınla</button>
                        <button type="button" onClick={() => { void handleDeleteDraft(d); }} disabled={busyAction === `deldraft-${d.id}`} title="Taslağı her yerden sil"
                          className="h-9 px-3 rounded-[10px] border border-[#FDA29B] bg-[#FEF3F2] text-[#B4233C] text-[13px] font-semibold cursor-pointer disabled:opacity-50">Sil</button>
                      </div>
                    </div>
                  ))}
                  {drafts.length === 0 && <p className="m-0 px-3 py-6 text-center text-[14px] text-ink-2">Taslak yok.</p>}
                </section>
              )}

              {(inboxFilter === 'all' || inboxFilter === 'notifications') && (
                <section className="rounded-xl border border-line overflow-hidden">
                  <header className="px-3 py-2 bg-canvas text-[13px] font-semibold flex items-center gap-2"><Bell className="w-4 h-4" /> Bildirimler ({notifications.length})</header>
                  {notifications.slice(0, 30).map((n) => (
                    <div key={n.id} className="px-3 py-2.5 border-t border-line-soft">
                      <div className="text-[14px] font-semibold">{n.title}</div>
                      <div className="text-[13px] text-ink-2">{n.message}</div>
                      <div className="text-[12px] text-ink-3">{n.author} · {n.timestamp ? new Date(n.timestamp).toLocaleString('tr-TR') : ''}</div>
                    </div>
                  ))}
                  {notifications.length === 0 && <p className="m-0 px-3 py-6 text-center text-[14px] text-ink-2">Bildirim yok.</p>}
                </section>
              )}
            </div>
          )}

          {section === 'drafts' && (
            <ManageDraftsSection
              adminEmail={adminEmail}
              adminName="Yönetici"
              committeeId={selectedCommitteeId}
              committeeName={committees.find((c) => c.id === selectedCommitteeId)?.name}
              questions={questions}
              onRefreshData={async () => {
                await onRefreshData();
                await reloadInbox();
              }}
              notify={setNotice}
            />
          )}

          {section === 'moderation' && (
            <div className="flex flex-col gap-3">
              <div className="flex flex-col sm:flex-row gap-2">
                <label className="flex-1 min-w-0">
                  <span className="sr-only">İncelenecek bildirim</span>
                  <select value={selectedReport?.id || ''} onChange={(e) => setSelectedReportId(e.target.value)} className="w-full h-11 border border-line-2 rounded-[10px] px-3 text-[14px] bg-white cursor-pointer">
                    {pendingReports.length === 0 && <option value="">Bekleyen bildirim yok</option>}
                    {pendingReports.map((r) => (
                      <option key={r.id} value={r.id}>{r.reason} · {r.questionTopic || r.questionId}</option>
                    ))}
                  </select>
                </label>
                {selectedReport && (
                  <button type="button" onClick={() => { void handleResolve(selectedReport); }} className="h-11 px-4 rounded-[10px] border border-line-2 text-[14px] font-semibold cursor-pointer shrink-0">Hatasız — Kapat</button>
                )}
              </div>

              {!selectedReport && (
                <div className="rounded-xl border border-line px-4 py-10 text-center text-[14px] text-ink-2">İncelenecek bildirim seç.</div>
              )}

              {selectedReport && (
                <div className="rounded-xl border border-line overflow-hidden">
                  <div className="px-4 py-3 bg-[#FFF5F7] border-b border-line-soft">
                    <div className="text-[15px] font-bold flex items-center gap-2"><Flag className="w-4 h-4 text-[#B4233C]" /> {selectedReport.reason}</div>
                    <p className="m-0 mt-1 text-[14px] text-ink-2">{selectedReport.details || 'Detay girilmemiş.'}</p>
                    <div className="text-[12px] text-ink-3 mt-1">{selectedReport.reportedBy || 'Anonim'} · {selectedReport.createdAt ? new Date(selectedReport.createdAt).toLocaleString('tr-TR') : ''}</div>
                  </div>
                  {!moderatedQuestion ? (
                    <p className="m-0 px-4 py-8 text-center text-[14px] text-ink-2">Bağlı soru bulunamadı (silinmiş olabilir).</p>
                  ) : (
                    <div className="p-4 flex flex-col gap-3">
                      <div className="text-[13px] text-ink-2">{moderatedQuestion.discipline} · {moderatedQuestion.topic} · S.{moderatedQuestion.questionNumber || '?'}</div>
                      <label className="flex flex-col gap-1.5">
                        <span className="text-[13px] font-semibold">Soru kökü</span>
                        <textarea value={modStem} onChange={(e) => setModStem(e.target.value)} rows={4} className="rounded-[12px] bg-field border border-transparent px-3.5 py-3 text-[15px] leading-relaxed outline-0 focus:border-accent focus:bg-white resize-y" />
                      </label>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <label className="flex flex-col gap-1.5">
                          <span className="text-[13px] font-semibold">Doğru cevap</span>
                          <select value={modAnswer} onChange={(e) => setModAnswer(e.target.value)} className="h-11 border border-line-2 rounded-[10px] px-3 text-[14px] bg-white cursor-pointer">
                            {['A', 'B', 'C', 'D', 'E'].map((k) => <option key={k} value={k}>{k}</option>)}
                          </select>
                        </label>
                      </div>
                      <label className="flex flex-col gap-1.5">
                        <span className="text-[13px] font-semibold">Açıklama</span>
                        <textarea value={modExplanation} onChange={(e) => setModExplanation(e.target.value)} rows={3} className="rounded-[12px] bg-field border border-transparent px-3.5 py-3 text-[14px] leading-relaxed outline-0 focus:border-accent focus:bg-white resize-y" />
                      </label>
                      <div className="flex gap-2">
                        <button type="button" onClick={() => { void handleSaveModeration(); }} disabled={isSavingMod || !modStem.trim()} className="h-11 px-5 rounded-[10px] bg-accent hover:bg-accent-hover text-white font-semibold text-[14px] inline-flex items-center gap-2 cursor-pointer disabled:opacity-50">
                          <Save className="w-4 h-4" /> {isSavingMod ? 'Kaydediliyor…' : 'Düzelt ve bildirimi kapat'}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {section === 'users' && (
            <div className="flex flex-col gap-3">
              <label className="flex items-center gap-2 h-10 px-3 border border-line-2 rounded-[10px] bg-field max-w-md">
                <Search className="w-4 h-4 text-ink-2 shrink-0" />
                <span className="sr-only">Kullanıcı ara</span>
                <input value={userQuery} onChange={(e) => setUserQuery(e.target.value)} placeholder="İsim veya e-posta ara" className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[14px]" />
              </label>
              <div className="rounded-xl border border-line overflow-x-auto">
                <table className="w-full text-[14px] border-collapse min-w-[760px]">
                  <thead className="bg-canvas text-[12px] text-ink-2">
                    <tr>
                      <th scope="col" className="text-left font-semibold px-3 py-2">Kullanıcı</th>
                      <th scope="col" className="text-right font-semibold px-3 py-2">Soru</th>
                      <th scope="col" className="text-right font-semibold px-3 py-2">Parça</th>
                      <th scope="col" className="text-right font-semibold px-3 py-2">Şık</th>
                      <th scope="col" className="text-right font-semibold px-3 py-2">Bildirim</th>
                      <th scope="col" className="text-right font-semibold px-3 py-2">Yorum</th>
                      <th scope="col" className="text-right font-semibold px-3 py-2">Toplam</th>
                      <th scope="col" className="text-right font-semibold px-3 py-2"><span className="sr-only">İşlemler</span></th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredUsers.slice(0, 100).map((u) => {
                      const isSelfAdmin = (u.email || '').toLowerCase() === adminEmail.toLowerCase();
                      const confirming = confirmDeleteUserKey === u.key;
                      const confirmingPurge = confirmPurgeKey === u.key;
                      const deleting = busyAction === `deluser-${u.key}`;
                      const purging = busyAction === `purge-${u.key}`;
                      const hasAccount = Boolean(regOf(u));
                      return (
                      <tr key={u.key} onClick={() => { setSelectedUserKey(selectedUserKey === u.key ? null : u.key); setConfirmDeleteUserKey(null); }}
                        className={`border-t border-line-soft cursor-pointer ${selectedUserKey === u.key ? 'bg-accent-soft/40' : 'hover:bg-[#FAFBFC]'}`}>
                        <td className="px-3 py-2">
                          <div className="font-semibold truncate max-w-[240px]">{u.name}</div>
                          {u.email && <div className="text-[12px] text-ink-3 truncate max-w-[240px]">{u.email}</div>}
                        </td>
                        <td className="px-3 py-2 text-right font-mono">{u.questions}</td>
                        <td className="px-3 py-2 text-right font-mono">{u.fragments}</td>
                        <td className="px-3 py-2 text-right font-mono">{u.options}</td>
                        <td className="px-3 py-2 text-right font-mono">{u.reports}</td>
                        <td className="px-3 py-2 text-right font-mono">{u.comments}</td>
                        <td className="px-3 py-2 text-right font-mono font-bold">{u.total}</td>
                        <td className="px-3 py-2 text-right whitespace-nowrap" onClick={(e) => e.stopPropagation()}>
                          {u.email && (
                            <button type="button" title={`${u.name} kullanıcısına e-posta gönder`}
                              onClick={() => { setMailUserKey(u.key); setMailSubject(''); setMailBody(''); }}
                              className="h-8 px-2.5 mr-1.5 rounded-lg border border-line bg-white text-[12px] font-semibold text-ink-2 hover:text-accent hover:border-accent/50 cursor-pointer inline-flex items-center gap-1">
                              <Mail className="w-3.5 h-3.5" /> Mail
                            </button>
                          )}
                          {!isSelfAdmin && hasAccount && (
                            <button type="button" title={confirming ? 'Onaylamak için tekrar bas' : `${u.name} kullanıcısını sil`}
                              onClick={() => (confirming ? void handleDeleteUser(u) : setConfirmDeleteUserKey(u.key))}
                              disabled={deleting}
                              className={`h-8 px-2.5 rounded-lg text-[12px] font-semibold cursor-pointer inline-flex items-center gap-1 disabled:opacity-50 ${confirming ? 'bg-[#B4233C] text-white' : 'border border-[#FDA29B] bg-[#FEF3F2] text-[#B4233C] hover:bg-[#FEE4E2]'}`}>
                              <Trash2 className="w-3.5 h-3.5" /> {deleting ? 'Siliniyor…' : confirming ? 'Emin misin?' : 'Sil'}
                            </button>
                          )}
                          {!hasAccount && u.total > 0 && (
                            <button type="button" title={confirmingPurge ? 'Onaylamak için tekrar bas' : `${u.name} isminin tüm katkı izlerini temizle (parça, şık, yorum, bildirim)`}
                              onClick={() => (confirmingPurge ? void handlePurgeAuthor(u) : setConfirmPurgeKey(u.key))}
                              disabled={purging}
                              className={`h-8 px-2.5 rounded-lg text-[12px] font-semibold cursor-pointer inline-flex items-center gap-1 disabled:opacity-50 ${confirmingPurge ? 'bg-[#B4233C] text-white' : 'border border-[#FDA29B] bg-[#FEF3F2] text-[#B4233C] hover:bg-[#FEE4E2]'}`}>
                              <Trash2 className="w-3.5 h-3.5" /> {purging ? 'Temizleniyor…' : confirmingPurge ? 'Emin misin?' : 'Temizle'}
                            </button>
                          )}
                        </td>
                      </tr>
                      );
                    })}
                    {filteredUsers.length === 0 && (
                      <tr><td colSpan={8} className="px-3 py-8 text-center text-ink-2">Kayıtlı işlem yok.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
              {selectedUserKey && (() => {
                const u = activity.find((x) => x.key === selectedUserKey);
                if (!u) return null;
                const reg = registeredUsers.find(
                  (r) => (r.email || '').toLowerCase() === u.key || (r.uid || '').toLowerCase() === u.key
                );
                const allQs = [...questions, ...pastQuestions];
                const userQuestions = allQs.filter((q) =>
                  normKey(q.contributedByUid || q.contributedByName) === u.key ||
                  (q.fragments || []).some((f) => normKey(f.authorUid || f.author) === u.key)
                ).slice(0, 20);
                const userMessages: { label: string; text: string }[] = [];
                for (const q of allQs) {
                  for (const f of q.fragments || []) {
                    if (normKey(f.authorUid || f.author) === u.key) {
                      userMessages.push({ label: `S.${q.questionNumber || '?'} · ${q.topic || q.discipline}`, text: f.text });
                    }
                  }
                  if (userMessages.length >= 15) break;
                }
                const userReports = reports.filter((r) => normKey(r.reportedBy) === u.key).slice(0, 20);
                const userComments = comments.filter((c) => normKey(c.author) === u.key).slice(0, 20);
                const isAdmin = (reg?.email || u.email || '').toLowerCase() === adminEmail.toLowerCase();
                return (
                  <section className="rounded-xl border border-accent/40 bg-accent-soft/20 p-4 flex flex-col gap-3">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-[15px] font-bold flex-1 min-w-[180px]">{u.name} — her bilgi</span>
                      {u.email && (
                        <button type="button" onClick={() => { setMailUserKey(u.key); setMailSubject(''); setMailBody(''); }}
                          className="h-9 px-3 rounded-[10px] bg-accent text-white text-[13px] font-semibold inline-flex items-center gap-1.5 cursor-pointer">
                          <Mail className="w-3.5 h-3.5" /> Mail gönder
                        </button>
                      )}
                      {!isAdmin && reg?.uid && (
                        <button type="button"
                          onClick={() => (confirmDeleteUserKey === u.key ? void handleDeleteUser(u) : setConfirmDeleteUserKey(u.key))}
                          disabled={busyAction === `deluser-${u.key}`}
                          className={`h-9 px-3 rounded-[10px] text-[13px] font-semibold cursor-pointer disabled:opacity-50 ${confirmDeleteUserKey === u.key ? 'bg-[#B4233C] text-white' : 'border border-[#FDA29B] bg-[#FEF3F2] text-[#B4233C]'}`}>
                          {confirmDeleteUserKey === u.key ? 'Emin misin? Sil' : 'Kullanıcıyı sil'}
                        </button>
                      )}
                      {!reg && u.total > 0 && (
                        <button type="button" title="Kayıtlı hesabı yok; bu ismin katkı izlerini temizler"
                          onClick={() => (confirmPurgeKey === u.key ? void handlePurgeAuthor(u) : setConfirmPurgeKey(u.key))}
                          disabled={busyAction === `purge-${u.key}`}
                          className={`h-9 px-3 rounded-[10px] text-[13px] font-semibold cursor-pointer disabled:opacity-50 ${confirmPurgeKey === u.key ? 'bg-[#B4233C] text-white' : 'border border-[#FDA29B] bg-[#FEF3F2] text-[#B4233C]'}`}>
                          {confirmPurgeKey === u.key ? 'Emin misin? Temizle' : 'Katkıları temizle'}
                        </button>
                      )}
                      <button type="button" onClick={() => { setSelectedUserKey(null); setConfirmDeleteUserKey(null); }} className="h-9 px-3 rounded-[10px] border border-line bg-white text-[13px] font-semibold cursor-pointer">Kapat</button>
                    </div>
                    <div className="flex flex-wrap gap-x-4 gap-y-1 text-[12.5px] text-ink-2">
                      {!reg && <span className="text-warn font-semibold">Kayıtlı hesabı yok — yalnızca katkı izi. "Katkıları temizle" ile izleri silebilirsiniz.</span>}
                      {u.email && <span>E-posta: <strong className="text-ink">{u.email}</strong></span>}
                      {u.studentNumber && <span>Numara: <strong className="text-ink">{u.studentNumber}</strong></span>}
                      {reg?.role && <span>Rol: <strong className="text-ink">{reg.role}</strong></span>}
                      {reg?.createdAt && <span>Kayıt: {new Date(reg.createdAt).toLocaleDateString('tr-TR')}</span>}
                      {reg?.lastLoginAt && <span>Son giriş: {new Date(reg.lastLoginAt).toLocaleString('tr-TR')}</span>}
                      <span>Toplam işlem: <strong className="text-ink font-mono">{u.total}</strong> (soru {u.questions} · parça {u.fragments} · şık {u.options} · bildirim {u.reports} · yorum {u.comments})</span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-2">
                      <div className="rounded-lg bg-white border border-line p-2.5">
                        <div className="text-[12px] font-semibold text-ink-2 mb-1">Katkı verdiği sorular ({userQuestions.length})</div>
                        {userQuestions.map((q) => (
                          <div key={q.id} className="text-[13px] truncate">S.{q.questionNumber || '?'} · {q.topic || q.discipline}</div>
                        ))}
                        {userQuestions.length === 0 && <div className="text-[12px] text-ink-3">Yok</div>}
                      </div>
                      <div className="rounded-lg bg-white border border-line p-2.5">
                        <div className="text-[12px] font-semibold text-ink-2 mb-1">Attığı mesajlar/parçalar ({userMessages.length})</div>
                        {userMessages.map((m, i) => (
                          <div key={i} className="text-[13px] mb-1"><span className="text-ink-3 text-[11.5px]">{m.label}: </span>{m.text.length > 120 ? m.text.slice(0, 120) + '…' : m.text}</div>
                        ))}
                        {userMessages.length === 0 && <div className="text-[12px] text-ink-3">Yok</div>}
                      </div>
                      <div className="rounded-lg bg-white border border-line p-2.5">
                        <div className="text-[12px] font-semibold text-ink-2 mb-1">Hata bildirimleri ({userReports.length})</div>
                        {userReports.map((r) => (
                          <div key={r.id} className="text-[13px] truncate">{r.reason} · {r.questionTopic || r.questionId}</div>
                        ))}
                        {userReports.length === 0 && <div className="text-[12px] text-ink-3">Yok</div>}
                      </div>
                      <div className="rounded-lg bg-white border border-line p-2.5">
                        <div className="text-[12px] font-semibold text-ink-2 mb-1">Yorumlar ({userComments.length})</div>
                        {userComments.map((c) => (
                          <div key={c.id} className="text-[13px] truncate">{c.text}</div>
                        ))}
                        {userComments.length === 0 && <div className="text-[12px] text-ink-3">Yok</div>}
                      </div>
                    </div>
                  </section>
                );
              })()}
              {mailUserKey && (() => {
                const u = activity.find((x) => x.key === mailUserKey);
                if (!u?.email) return null;
                return (
                  <section className="rounded-xl border border-line bg-white p-4 flex flex-col gap-2.5">
                    <div className="flex items-center gap-2">
                      <Mail className="w-4 h-4 text-accent" />
                      <span className="text-[15px] font-bold flex-1">{u.name} &lt;{u.email}&gt; — e-posta gönder</span>
                      <button type="button" onClick={() => setMailUserKey(null)} className="h-8 px-3 rounded-lg border border-line text-[12px] font-semibold cursor-pointer">Vazgeç</button>
                    </div>
                    <label className="flex flex-col gap-1">
                      <span className="text-[12px] font-semibold text-ink-2">Konu</span>
                      <input value={mailSubject} onChange={(e) => setMailSubject(e.target.value)} placeholder="Konu başlığı" className="h-10 border border-line-2 rounded-[10px] px-3 text-[14px] outline-0 focus:border-accent" />
                    </label>
                    <label className="flex flex-col gap-1">
                      <span className="text-[12px] font-semibold text-ink-2">Mesaj</span>
                      <textarea value={mailBody} onChange={(e) => setMailBody(e.target.value)} rows={4} placeholder="Mesajınızı yazın…" className="border border-line-2 rounded-[10px] px-3 py-2.5 text-[14px] leading-relaxed outline-0 focus:border-accent resize-y" />
                    </label>
                    <div>
                      <button type="button" onClick={() => { void handleSendMail(); }} disabled={sendingMail || !mailSubject.trim() || !mailBody.trim()}
                        className="h-11 px-5 rounded-[10px] bg-accent hover:bg-accent-hover text-white font-semibold text-[14px] inline-flex items-center gap-2 cursor-pointer disabled:opacity-50">
                        <Send className="w-4 h-4" /> {sendingMail ? 'Gönderiliyor…' : 'Gönder'}
                      </button>
                    </div>
                  </section>
                );
              })()}
              <p className="m-0 text-[12px] text-ink-3">Soru havuzu + çıkmış sorular + bildirim/yorum katkılarından hesaplanır. Kayıtlı kullanıcı bilgileriyle eşleştirilir.</p>
            </div>
          )}

          {section === 'scripts' && (
            <div className="rounded-xl overflow-hidden border border-line min-h-[480px]">
              <AdminScriptsTab adminEmail={adminEmail} onRefreshAllData={onRefreshData} />
            </div>
          )}

          {section === 'system' && (
            <div className="flex flex-col gap-3">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                <div className="rounded-xl border border-line px-3 py-2.5">
                  <div className="text-[12px] text-ink-2">Firebase</div>
                  <div className="font-mono text-[15px] font-semibold">{health.firebase.status}</div>
                  <div className="text-[12px] text-ink-3 truncate">{health.firebase.details || ''}</div>
                </div>
                <div className="rounded-xl border border-line px-3 py-2.5">
                  <div className="text-[12px] text-ink-2">Supabase</div>
                  <div className="font-mono text-[15px] font-semibold">{health.supabase.status}</div>
                  <div className="text-[12px] text-ink-3 truncate">{health.supabase.details || ''}</div>
                </div>
                <div className="rounded-xl border border-line px-3 py-2.5">
                  <div className="text-[12px] text-ink-2">Yapay zeka</div>
                  <div className="font-mono text-[15px] font-semibold">{health.ai.status}</div>
                  <div className="text-[12px] text-ink-3 truncate">
                    {health.ai.lastAiError ? `${health.ai.lastAiError.provider}: ${health.ai.lastAiError.message.slice(0, 80)}` : 'Hata kaydı yok'}
                  </div>
                </div>
              </div>

              {health.ai.keys.filter((k) => k.status === 'quota_exceeded' || k.status === 'spending_cap_exceeded').length > 0 && (
                <div role="alert" className="rounded-xl border border-[#FECDCA] bg-[#FEF3F2] px-4 py-3 text-[14px] flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-[#B4233C] shrink-0 mt-0.5" />
                  <span>Limite ulaşan AI anahtarları: {health.ai.keys.filter((k) => k.status !== 'ok').map((k) => `${k.label} (${k.status})`).join(' · ')}</span>
                </div>
              )}

              <div className="flex flex-wrap gap-2">
                <button type="button" onClick={() => { void handleRunDiagnostics(); }} disabled={isDiagnosing} className="h-10 px-4 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-[14px] font-semibold inline-flex items-center gap-2 cursor-pointer disabled:opacity-50">
                  <Activity className={`w-4 h-4 ${isDiagnosing ? 'animate-spin' : ''}`} /> {isDiagnosing ? 'Test çalışıyor…' : 'Tam teşhis çalıştır'}
                </button>
                <button type="button" onClick={() => { void handleRealtimeTest(); }} disabled={realtimeResult.running} className="h-10 px-4 rounded-[10px] border border-line-2 text-[14px] font-semibold cursor-pointer disabled:opacity-50">
                  {realtimeResult.running ? 'Realtime test…' : 'Realtime tur testi'}
                </button>
                <button type="button" onClick={() => { void handleLoadServices(); }} disabled={isLoadingServices} className="h-10 px-4 rounded-[10px] border border-line-2 text-[14px] font-semibold inline-flex items-center gap-2 cursor-pointer disabled:opacity-50">
                  <RefreshCw className={`w-4 h-4 ${isLoadingServices ? 'animate-spin' : ''}`} /> Servisleri yenile
                </button>
                {realtimeResult.message && <span className="text-[13px] text-ink-2 self-center">{realtimeResult.message}</span>}
              </div>

              <section className="rounded-xl border border-line overflow-hidden">
                <header className="px-3 py-2 bg-canvas flex items-center gap-2">
                  <Server className="w-4 h-4" />
                  <span className="text-[13px] font-semibold flex-1">Servisler — hangisi çalışıyor, hangisi duruyor</span>
                  {servicesSummary && (
                    <span className="text-[12px] text-ink-2 font-mono">{servicesSummary.activeServicesCount} aktif / {servicesSummary.stoppedServicesCount} duruyor</span>
                  )}
                </header>
                {heartbeat && (
                  <div className={`px-3 py-2 border-b border-line-soft text-[13px] flex items-center gap-2 ${heartbeat.isOnline ? 'bg-[#F6FEF9]' : 'bg-[#FEF3F2]'}`}>
                    <Radio className={`w-4 h-4 ${heartbeat.isOnline ? 'text-ok' : 'text-[#B4233C]'}`} />
                    <span>Arka plan işçisi: <strong>{heartbeat.isOnline ? 'çevrimiçi' : 'çevrimdışı'}</strong>{heartbeat.diffSeconds !== undefined ? ` (${heartbeat.diffSeconds} sn önce)` : ''} · {heartbeat.message}</span>
                  </div>
                )}
                {services.length === 0 && (
                  <p className="m-0 px-3 py-6 text-center text-[14px] text-ink-2">{isLoadingServices ? 'Servisler yükleniyor…' : 'Servis bilgisi yok — sunucu çevrimdışı olabilir.'}</p>
                )}
                {services.map((s) => {
                  const running = /active|çalış|online|açık/i.test(s.status) || /active|çalış|online|açık/i.test(s.statusLabel);
                  return (
                    <div key={s.id} className="px-3 py-2 border-t border-line-soft flex items-center gap-2">
                      <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${running ? 'bg-ok' : 'bg-line-2'}`} aria-hidden="true" />
                      <div className="flex-1 min-w-0">
                        <div className="text-[14px] font-medium truncate">{s.name}</div>
                        {s.description && <div className="text-[12px] text-ink-3 truncate">{s.description}</div>}
                      </div>
                      <span className={`text-[12px] font-semibold shrink-0 ${running ? 'text-ok' : 'text-ink-3'}`}>{s.statusLabel || s.status}</span>
                    </div>
                  );
                })}
              </section>

              <section className="rounded-xl border border-line overflow-hidden">
                <header className="px-3 py-2 bg-canvas flex items-center gap-2">
                  <Terminal className="w-4 h-4" />
                  <span className="text-[13px] font-semibold flex-1">Canlı konsol ({logs.length})</span>
                  <div role="radiogroup" aria-label="Log seviyesi" className="inline-flex gap-1 bg-white rounded-[10px] p-[3px] border border-line-soft">
                    {(['all', 'log', 'info', 'warn', 'error'] as const).map((lv) => (
                      <button key={lv} type="button" role="radio" aria-checked={logLevel === lv} onClick={() => setLogLevel(lv)}
                        className={`h-7 px-2 rounded-lg text-[12px] cursor-pointer ${logLevel === lv ? 'bg-ink text-white font-semibold' : 'text-ink-2'}`}>{lv}</button>
                    ))}
                  </div>
                  <button type="button" onClick={() => { void navigator.clipboard.writeText(logs.map((l) => `[${l.ts}][${l.level}][${l.source}] ${l.message}`).join('\n')); setCopiedLogs(true); setTimeout(() => setCopiedLogs(false), 2000); }} className="h-8 px-2.5 rounded-lg border border-line bg-white text-[12px] font-semibold inline-flex items-center gap-1 cursor-pointer">
                    {copiedLogs ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />} {copiedLogs ? 'Kopyalandı' : 'Kopyala'}
                  </button>
                  <button type="button" onClick={() => consoleLogBuffer.clear()} className="h-8 px-2.5 rounded-lg border border-line bg-white text-[12px] font-semibold cursor-pointer">Temizle</button>
                </header>
                <div className="max-h-[320px] overflow-y-auto bg-[#0B1220] text-slate-200 font-mono text-[12px] leading-relaxed p-3">
                  {logs.filter((l) => logLevel === 'all' || l.level === logLevel).slice(-200).map((l) => (
                    <div key={l.id} className={`whitespace-pre-wrap break-all ${l.level === 'error' ? 'text-rose-400' : l.level === 'warn' ? 'text-amber-300' : 'text-slate-300'}`}>
                      [{l.ts.slice(11, 19)}][{l.level}][{l.source}] {l.message}
                    </div>
                  ))}
                  {logs.length === 0 && <div className="text-slate-500">Henüz kayıt yok.</div>}
                </div>
              </section>
            </div>
          )}

          {section === 'automation' && (
            <div className="flex flex-col gap-3">
              <section className="rounded-xl border border-line p-4 flex flex-col gap-3">
                <h3 className="m-0 text-[16px] font-bold flex items-center gap-2"><Clock className="w-4 h-4" /> Yedekleme saatleri</h3>
                <div className="flex flex-wrap items-center gap-2">
                  <label className="flex items-center gap-2 text-[14px] cursor-pointer">
                    <input type="checkbox" checked={settings.backupEnabled} onChange={(e) => setSettings({ ...settings, backupEnabled: e.target.checked })} className="w-4 h-4" />
                    Otomatik yedekleme aktif
                  </label>
                  <span className="flex-1" />
                  <button type="button" onClick={() => { void handleBackupNow(); }} disabled={isBackingUp} className="h-10 px-4 rounded-[10px] bg-ink text-white text-[14px] font-semibold cursor-pointer disabled:opacity-50">
                    {isBackingUp ? 'Yedekleniyor…' : 'Hemen yedekle'}
                  </button>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {settings.backupHours.map((h) => (
                    <span key={h} className="h-9 px-3 rounded-[10px] bg-canvas border border-line font-mono text-[14px] inline-flex items-center gap-2">
                      {h}
                      <button type="button" aria-label={`${h} saatini sil`} onClick={() => setSettings({ ...settings, backupHours: settings.backupHours.filter((x) => x !== h) })} className="text-ink-3 hover:text-[#B4233C] cursor-pointer"><X className="w-3.5 h-3.5" /></button>
                    </span>
                  ))}
                </div>
                <div className="flex gap-2 items-center">
                  <input type="time" value={newBackupHour} onChange={(e) => setNewBackupHour(e.target.value)} className="h-10 border border-line-2 rounded-[10px] px-3 text-[14px] bg-white" />
                  <button type="button" onClick={() => { if (newBackupHour && !settings.backupHours.includes(newBackupHour)) setSettings({ ...settings, backupHours: [...settings.backupHours, newBackupHour].sort() }); }} className="h-10 px-4 rounded-[10px] border border-line-2 text-[14px] font-semibold inline-flex items-center gap-1.5 cursor-pointer"><Plus className="w-4 h-4" /> Saat ekle</button>
                  <label className="flex items-center gap-1.5 text-[13px]">Kapsam
                    <select value={settings.backupScope} onChange={(e) => setSettings({ ...settings, backupScope: e.target.value as ManageAutomationSettings['backupScope'] })} className="h-10 border border-line-2 rounded-[10px] px-2 text-[13px] bg-white cursor-pointer">
                      <option value="all">Tümü</option>
                      <option value="questions">Soru havuzu</option>
                      <option value="past">Çıkmış sorular</option>
                      <option value="notes">Ders notları</option>
                    </select>
                  </label>
                </div>
              </section>

              <section className="rounded-xl border border-line p-4 flex flex-col gap-3">
                <h3 className="m-0 text-[16px] font-bold flex items-center gap-2"><Key className="w-4 h-4" /> AI API anahtarları</h3>
                {([['gemini', 'Gemini API anahtarı'], ['groq', 'Groq anahtarı 1'], ['groq2', 'Groq anahtarı 2'], ['museSpark', 'Muse Spark 1.3 Free anahtarı (Kota Kurtarıcı)']] as const).map(([k, label]) => (
                  <label key={k} className="flex flex-col gap-1.5">
                    <span className="text-[13px] font-semibold">{label}</span>
                    <input type="password" autoComplete="off" value={aiKeys[k]} onChange={(e) => setAiKeys({ ...aiKeys, [k]: e.target.value })} placeholder="Yapıştır…" className="h-11 border border-line-2 rounded-[10px] px-3 text-[14px] font-mono bg-white outline-0 focus:border-accent" />
                  </label>
                ))}
                <p className="m-0 text-[12px] text-ink-3">Anahtarlar yalnızca bu tarayıcıda saklanır (mevcut uygulamanın kullandığı anahtarlarla aynı). Muse Spark 1.3, Gemini ve Groq limitleri dolduğunda otomatik devreye girer.</p>
              </section>

              <section className="rounded-xl border border-line p-4 flex flex-col gap-3">
                <h3 className="m-0 text-[16px] font-bold">AI otomatik çalışma pencereleri</h3>
                <label className="flex items-center gap-2 text-[14px] cursor-pointer">
                  <input type="checkbox" checked={settings.aiAutoRunEnabled} onChange={(e) => setSettings({ ...settings, aiAutoRunEnabled: e.target.checked })} className="w-4 h-4" />
                  Zamanlanmış AI çalışması aktif
                </label>
                {settings.aiWindows.map((w, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <input type="time" value={w.start} onChange={(e) => setSettings({ ...settings, aiWindows: settings.aiWindows.map((x, xi) => (xi === i ? { ...x, start: e.target.value } : x)) })} className="h-10 border border-line-2 rounded-[10px] px-3 text-[14px] bg-white" />
                    <span className="text-ink-3">→</span>
                    <input type="time" value={w.end} onChange={(e) => setSettings({ ...settings, aiWindows: settings.aiWindows.map((x, xi) => (xi === i ? { ...x, end: e.target.value } : x)) })} className="h-10 border border-line-2 rounded-[10px] px-3 text-[14px] bg-white" />
                    <button type="button" aria-label="Pencereyi sil" onClick={() => setSettings({ ...settings, aiWindows: settings.aiWindows.filter((_, xi) => xi !== i) })} className="h-10 w-10 rounded-[10px] border border-line inline-flex items-center justify-center text-ink-3 hover:text-[#B4233C] cursor-pointer"><Trash2 className="w-4 h-4" /></button>
                  </div>
                ))}
                <button type="button" onClick={() => setSettings({ ...settings, aiWindows: [...settings.aiWindows, { start: '02:00', end: '05:00' }] })} className="self-start h-10 px-4 rounded-[10px] border border-line-2 text-[14px] font-semibold inline-flex items-center gap-1.5 cursor-pointer"><Plus className="w-4 h-4" /> Pencere ekle</button>
                <label className="flex flex-col gap-1.5 max-w-xs">
                  <span className="text-[13px] font-semibold">Varsayılan model</span>
                  <select value={settings.aiModel} onChange={(e) => setSettings({ ...settings, aiModel: e.target.value })} className="h-11 border border-line-2 rounded-[10px] px-3 text-[14px] bg-white cursor-pointer">
                    <option value="gemini-3.8-flash">gemini-3.8-flash</option>
                    <option value="openai/gpt-oss-120b">openai/gpt-oss-120b (Groq)</option>
                    <option value="qwen/qwen3.8-27b">qwen/qwen3.8-27b (Groq)</option>
                    <option value="muse-spark-1.3-contributor-free">muse-spark-1.3-contributor-free (Muse Spark 1.3 Free)</option>
                  </select>
                </label>
                <label className="flex items-center gap-2 text-[14px] cursor-pointer">
                  <input type="checkbox" checked={settings.notifyOnError} onChange={(e) => setSettings({ ...settings, notifyOnError: e.target.checked })} className="w-4 h-4" />
                  Hata olursa beni bilgilendir
                </label>
                <div>
                  <button type="button" onClick={() => { void handleSaveAutomation(); }} disabled={isSavingSettings} className="h-11 px-5 rounded-[10px] bg-accent hover:bg-accent-hover text-white font-semibold text-[14px] inline-flex items-center gap-2 cursor-pointer disabled:opacity-50">
                    <Save className="w-4 h-4" /> {isSavingSettings ? 'Kaydediliyor…' : 'Otomasyon ayarlarını kaydet'}
                  </button>
                </div>
              </section>

              <AdminDriveSyncSettings adminEmail={adminEmail} onRefreshData={onRefreshData} selectedCommitteeId={selectedCommitteeId} />
            </div>
          )}
        </div>
      </div>

      {editingDraft && (
        <AdminEditQuestionModal
          isOpen
          question={editingDraft}
          adminEmail={adminEmail}
          onClose={() => setEditingDraft(null)}
          onSaveQuestion={async (updated) => {
            await ApiService.adminUpdateQuestion(adminEmail, editingDraft.id, updated);
            setEditingDraft(null);
            setNotice('Taslak güncellendi.');
            await onRefreshData();
            await reloadInbox();
          }}
        />
      )}
    </div>
  );
};
