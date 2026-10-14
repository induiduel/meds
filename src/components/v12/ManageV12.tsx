import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft, Search, RefreshCw, Moon, Sun, ChevronDown, ChevronRight, AlignJustify, Inbox, Layers, BookOpenCheck,
  Terminal, HardDrive, UserSearch, Flag, Boxes,
} from 'lucide-react';
import type { Committee, QuestionItem, AdminNotification } from '../../types';
import type { ManageSection } from '../manage/ManageConsole';
import type { InboxReport, InboxComment } from '../../services/manageConsoleService';
import { fetchSystemServices, fetchWorkerHeartbeat } from '../../services/manageConsoleService';
import { systemHealthMonitor, type SystemOverallHealth } from '../../services/systemHealthMonitor';
import type { RealtimeConnectionStatus } from '../../services/realtimeEvents';
import '../../styles/v12/manage.css';

/**
 * Yönetim konsolu — v12 "Net" kabuğu ve "Genel bakış" (canvas: Manage.dc.html).
 * Yalnız v12'de ManageConsole buradan çizer; bölüm içerikleri, veri ve işlevler ManageConsole'da kalır.
 * Kabuk: gruplu sol menü (bekleyen sayılarıyla), üst çubuk (konum, Ctrl+K, Canlı|Yerel, yoğunluk), sayfa başlığı.
 */

export interface M12NavItem {
  id: ManageSection;
  label: string;
  hint: string;
  icon: React.ElementType;
  badge?: { n: number; alert?: boolean };
}
export interface M12NavGroup {
  /** null: grupsuz üst öge (Genel bakış) */
  label: string | null;
  items: M12NavItem[];
}

const LIVE_TEXT: Record<RealtimeConnectionStatus, string> = { connected: 'Bağlı', connecting: 'Bağlanıyor', disconnected: 'Bağlantı yok' };

export const ManageShellV12: React.FC<{
  groups: M12NavGroup[];
  section: ManageSection;
  currentLabel: string;
  currentGroup: string;
  currentHint: React.ReactNode;
  headCount?: { n: number; alert?: boolean };
  onPick: (id: ManageSection) => void;
  onOpenPalette: () => void;
  onExit: () => void;
  adminEmail: string;
  sourceLive: boolean;
  canSwitchSource: boolean;
  onChooseSource: (t: 'oracle' | 'yerel') => void;
  liveStatus: RealtimeConnectionStatus;
  syncLabel: string;
  dense: boolean;
  onToggleDense: () => void;
  committees: Committee[];
  selectedCommitteeId: string;
  onSelectCommittee: (id: string) => void;
  loading: boolean;
  onRefresh: () => void;
  theme: string;
  onToggleTheme: () => void;
  bodyDensity: string;
  wide?: boolean;
  fullscreen: boolean;
  children: React.ReactNode;
}> = (p) => {
  const navRef = useRef<HTMLElement>(null);
  useEffect(() => {
    navRef.current?.querySelector('.m12-nav-i.on')?.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }, [p.section]);
  const committeeName = p.committees.find((c) => c.id === p.selectedCommitteeId)?.name;
  const liveText = LIVE_TEXT[p.liveStatus] || 'Bağlantı yok';

  const navButton = (it: M12NavItem) => {
    const on = it.id === p.section;
    const Icon = it.icon;
    return (
      <button
        key={it.id}
        type="button"
        className={`m12-nav-i ${on ? 'on' : ''}`}
        aria-current={on ? 'page' : undefined}
        onClick={() => p.onPick(it.id)}
        title={it.hint}
      >
        <Icon aria-hidden="true" />
        <span className="l">{it.label}</span>
        {it.badge && it.badge.n > 0 && (
          <span className={`c ${it.badge.alert && !on ? 'hot' : ''}`} aria-label={`${it.badge.n} bekleyen`}>
            {it.badge.n.toLocaleString('tr-TR')}
          </span>
        )}
      </button>
    );
  };

  return (
    <div className={`ms-console m12-app ${p.fullscreen ? 'is-full' : 'is-inline'}`} data-m12-dense={p.dense ? 'tight' : 'cozy'}>
      <aside className="m12-side" aria-label="Yönetim menüsü">
        <button type="button" className="m12-brand" onClick={p.onExit} title="Öğrenci sitesine dön">
          <i aria-hidden="true">M</i>
          <span className="w">MeDSor</span>
          <span className="m12-badge">Yönetim</span>
        </button>
        <nav className="m12-nav" aria-label="Yönetim bölümleri" ref={navRef}>
          {p.groups.map((g, gi) => {
            if (!g.label) return <React.Fragment key={`g${gi}`}>{g.items.map(navButton)}</React.Fragment>;
            const sum = g.items.reduce((a, it) => a + (it.badge?.n || 0), 0);
            const hot = g.items.some((it) => it.badge?.alert && it.badge.n > 0);
            return (
              <div key={g.label} className="m12-grp" role="group" aria-labelledby={`m12-g-${gi}`}>
                <div className="m12-grp-h" id={`m12-g-${gi}`}>
                  <span>{g.label}</span>
                  {sum > 0 && <span className={`c ${hot ? 'hot' : ''}`} aria-label={`${sum} bekleyen`}>{sum.toLocaleString('tr-TR')}</span>}
                </div>
                {g.items.map(navButton)}
              </div>
            );
          })}
        </nav>
        <p className="m12-legend">Sayılar, ilgilenmeni bekleyen ögelerdir; toplam kayıt değil.</p>
        <button type="button" className="m12-nav-i m12-exit" onClick={p.onExit}>
          <ArrowLeft aria-hidden="true" />
          <span className="l">Öğrenci sitesine dön</span>
        </button>
      </aside>

      <div className="m12-main">
        <header className={`m12-top ${p.sourceLive ? 'is-live' : ''}`}>
          <nav className="m12-crumb" aria-label="Konum">
            <span>Yönetim</span>
            <ChevronRight aria-hidden="true" />
            <span>{p.currentGroup}</span>
            <ChevronRight aria-hidden="true" />
            <b aria-current="page">{p.currentLabel}</b>
          </nav>
          <button type="button" className="m12-field m12-search" onClick={p.onOpenPalette} aria-haspopup="dialog" aria-label="Yönetimde ara (Ctrl+K)">
            <Search aria-hidden="true" />
            <span className="ph">Bölüm ya da iş ara</span>
            <kbd className="m12-kbd" aria-hidden="true">⌘K</kbd>
          </button>
          {p.canSwitchSource ? (
            <div className="m12-seg m12-env" role="group" aria-label="Veri kaynağı">
              <button
                type="button"
                className={p.sourceLive ? 'on live' : ''}
                aria-pressed={p.sourceLive}
                onClick={() => !p.sourceLive && p.onChooseSource('oracle')}
                title="Panel canlı siteye (Oracle) bağlı: değişiklikler doğrudan canlıya yazılır"
              >
                <span className="d" aria-hidden="true" />
                Canlı
              </button>
              <button
                type="button"
                className={!p.sourceLive ? 'on' : ''}
                aria-pressed={!p.sourceLive}
                onClick={() => p.sourceLive && p.onChooseSource('yerel')}
                title="Panel bu bilgisayardaki sunucuya bağlı (deneme için)"
              >
                Yerel
              </button>
            </div>
          ) : (
            <span className={`m12-badge ${p.sourceLive ? 'warn' : ''}`} title={p.sourceLive ? 'Değişiklikler canlı siteye yazılır' : 'Yerel sunucu'}>
              {p.sourceLive ? 'Canlı' : 'Yerel'}
            </span>
          )}
          <label className="m12-field m12-kurul" title={committeeName}>
            <span className="sr-only">Kurul</span>
            <select value={p.selectedCommitteeId} onChange={(e) => p.onSelectCommittee(e.target.value)}>
              {p.committees.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
            <ChevronDown aria-hidden="true" />
          </label>
          <span className={`m12-live is-${p.liveStatus}`} role="status" title={`Canlı kanal: ${liveText.toLocaleLowerCase('tr-TR')}${p.syncLabel ? ` · son eşitleme ${p.syncLabel}` : ''}`}>
            <i aria-hidden="true" />
            <span>{liveText}</span>
            {p.syncLabel && <small className="m12-num">{p.syncLabel}</small>}
          </span>
          <button type="button" className="m12-btn sm ghost m12-dense" onClick={p.onToggleDense} aria-pressed={p.dense} aria-label={`Yoğunluk: ${p.dense ? 'Sıkı' : 'Rahat'}`}>
            <AlignJustify aria-hidden="true" />
            <span>{p.dense ? 'Sıkı' : 'Rahat'}</span>
          </button>
          <button type="button" className="m12-btn sm ghost icon" onClick={p.onRefresh} disabled={p.loading} aria-label="Verileri yenile" title="Verileri yenile">
            <RefreshCw className={p.loading ? 'm12-spin' : ''} aria-hidden="true" />
          </button>
          <button type="button" className="m12-btn sm ghost icon" onClick={p.onToggleTheme} aria-label={p.theme === 'dark' ? 'Açık temaya geç' : 'Koyu temaya geç'} title="Temayı değiştir">
            {p.theme === 'dark' ? <Sun aria-hidden="true" /> : <Moon aria-hidden="true" />}
          </button>
          <span className="m12-me" role="img" aria-label={`Yönetici hesabı: ${p.adminEmail || 'Yönetici'}`} title={p.adminEmail}>
            {(p.adminEmail || 'Y').charAt(0).toLocaleUpperCase('tr-TR')}
          </span>
        </header>

        <main key={p.section} className="ms-console-body m12-body" data-density={p.bodyDensity} aria-label={p.currentLabel}>
          <div className={`ms-cinner m12-inner ${p.wide ? 'is-wide' : ''}`}>
            <div className="m12-head">
              <h1>
                {p.currentLabel}
                {p.headCount && p.headCount.n > 0 && (
                  <span className={`m12-badge ${p.headCount.alert ? 'bad' : ''}`}>{p.headCount.n.toLocaleString('tr-TR')}</span>
                )}
              </h1>
              <p className="m12-meta">{p.currentHint}</p>
            </div>
            {p.children}
          </div>
        </main>
      </div>
    </div>
  );
};

/* ============================================================================
 * Genel bakış
 * ========================================================================== */

type QGroup = 'content' | 'people' | 'system';
interface QItem {
  key: string;
  g: QGroup;
  prio: number;
  type: string;
  tone: '' | 'bad' | 'warn' | 'acc';
  title: string;
  meta: string;
  at?: string;
  action: string;
  run: () => void;
}
type Dot = 'ok' | 'warn' | 'bad' | 'idle';
interface HealthCell { name: string; dot: Dot; text: string }

const toMs = (iso?: string) => {
  const t = iso ? new Date(iso).getTime() : NaN;
  return Number.isFinite(t) ? t : 0;
};
/** "12 dk", "3 sa", "dün", "5 gün", "12 Eki" */
const ageOf = (iso?: string) => {
  const t = toMs(iso);
  if (!t) return '—';
  const s = (Date.now() - t) / 1000;
  if (s < 90) return 'şimdi';
  if (s < 3600) return `${Math.round(s / 60)} dk`;
  if (s < 86400) return `${Math.round(s / 3600)} sa`;
  if (s < 86400 * 2) return 'dün';
  if (s < 86400 * 7) return `${Math.floor(s / 86400)} gün`;
  return new Date(t).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};
const clockOf = (iso?: string) => {
  const t = toMs(iso);
  if (!t) return '—';
  const d = new Date(t);
  const today = new Date();
  const same = d.toDateString() === today.toDateString();
  const hm = d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
  return same ? hm : `${d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })} ${hm}`;
};
const NOTICE_TYPE: Record<string, string> = { new_fragment: 'Parça', unassigned_question: 'Numarasız', batch_cluster_ready: 'Küme', report: 'Bildirim', comment: 'Yorum', test: 'Deneme' };
const DB_TEXT: Record<string, string> = {
  online: 'çevrimiçi', missing_tables: 'tablo eksik', auth_error: 'kimlik hatası', network_error: 'ağ hatası', not_configured: 'ayarlanmamış',
  offline: 'çevrimdışı', quota_exceeded: 'kota doldu', permission_denied: 'yetki yok',
};
const AI_TEXT: Record<string, string> = { ready: 'hazır', degraded: 'kısıtlı', all_exhausted: 'anahtarlar dolu' };

export const ManageOverviewV12: React.FC<{
  pendingReports: InboxReport[];
  comments: InboxComment[];
  drafts: QuestionItem[];
  notifications: AdminNotification[];
  usersCount: number;
  questionsCount: number;
  liveStatus: RealtimeConnectionStatus;
  onGo: (id: ManageSection) => void;
  onReviewReport: (r: InboxReport) => void;
  onEditDraft: (d: QuestionItem) => void;
  onOpenQuestion: (questionId: string) => void;
}> = ({ pendingReports, comments, drafts, notifications, usersCount, questionsCount, liveStatus, onGo, onReviewReport, onEditDraft, onOpenQuestion }) => {
  const [health, setHealth] = useState<SystemOverallHealth>(() => systemHealthMonitor.getHealth());
  const [svc, setSvc] = useState<{ total: number; running: number } | null>(null);
  const [beat, setBeat] = useState<{ isOnline: boolean; message: string } | null>(null);
  const [qf, setQf] = useState<'all' | QGroup>('all');
  const [af, setAf] = useState<'all' | 'report' | 'comment' | 'notice'>('all');

  useEffect(() => systemHealthMonitor.subscribe(setHealth), []);
  useEffect(() => {
    let live = true;
    void Promise.all([fetchSystemServices(), fetchWorkerHeartbeat()]).then(([s, hb]) => {
      if (!live) return;
      if (s.ok) {
        const running = s.services.filter((x) => /active|çalış|online|açık/i.test(`${x.status} ${x.statusLabel}`)).length;
        setSvc({ total: s.services.length, running });
      }
      setBeat({ isOnline: hb.isOnline, message: hb.message });
    });
    return () => {
      live = false;
    };
  }, []);

  const cells = useMemo<HealthCell[]>(() => {
    const db = health.supabase;
    const fb = health.firebase;
    const ai = health.ai;
    const out: HealthCell[] = [
      { name: 'meds-pg', dot: !db.lastChecked ? 'idle' : db.status === 'online' ? 'ok' : 'bad', text: db.lastChecked ? DB_TEXT[db.status] || db.status : 'denetlenmedi' },
      { name: 'Firebase', dot: !fb.lastChecked ? 'idle' : fb.status === 'online' ? 'ok' : fb.status === 'quota_exceeded' ? 'warn' : 'bad', text: fb.lastChecked ? DB_TEXT[fb.status] || fb.status : 'denetlenmedi' },
      { name: 'Yapay zeka', dot: !ai.lastChecked ? 'idle' : ai.status === 'ready' ? 'ok' : ai.status === 'degraded' ? 'warn' : 'bad', text: ai.lastChecked ? AI_TEXT[ai.status] || ai.status : 'denetlenmedi' },
      { name: 'Canlı kanal', dot: liveStatus === 'connected' ? 'ok' : liveStatus === 'connecting' ? 'warn' : 'bad', text: liveStatus === 'connected' ? 'bağlı' : liveStatus === 'connecting' ? 'bağlanıyor' : 'kopuk' },
    ];
    out.push(beat ? { name: 'Arka plan işçisi', dot: beat.isOnline ? 'ok' : 'warn', text: beat.isOnline ? 'çalışıyor' : 'yanıt yok' } : { name: 'Arka plan işçisi', dot: 'idle', text: 'yükleniyor' });
    if (svc) out.push({ name: 'Servisler', dot: svc.running === svc.total ? 'ok' : svc.running === 0 ? 'bad' : 'warn', text: `${svc.running}/${svc.total} çalışıyor` });
    return out;
  }, [health, liveStatus, beat, svc]);

  const queue = useMemo<QItem[]>(() => {
    const out: QItem[] = [];
    for (const r of pendingReports) {
      out.push({
        key: `r-${r.id}`, g: 'content', prio: 0, type: 'Bildirim', tone: 'bad',
        title: r.reason || 'Hata bildirimi',
        meta: [r.questionTopic || `Soru #${r.questionId}`, r.discipline, r.reportedBy ? `Gönderen: ${r.reportedBy}` : 'Anonim'].filter(Boolean).join(' · '),
        at: r.createdAt, action: 'İncele', run: () => onReviewReport(r),
      });
    }
    for (const c of cells) {
      if (c.dot === 'bad' || (c.dot === 'warn' && c.name !== 'Servisler')) {
        out.push({ key: `h-${c.name}`, g: 'system', prio: 1, type: 'Sistem', tone: c.dot === 'bad' ? 'bad' : 'warn', title: `${c.name}: ${c.text}`, meta: 'Servis durumu', action: 'Sistem', run: () => onGo('system') });
      }
    }
    for (const d of drafts) {
      const x = d as QuestionItem & { updatedAt?: string; createdAt?: string };
      out.push({
        key: `d-${d.id}`, g: 'content', prio: 2, type: 'Taslak', tone: 'acc',
        title: d.topic || d.discipline || 'Konusuz taslak',
        meta: [d.isUnassignedNumber ? 'Numarasız' : d.questionNumber ? `S.${d.questionNumber}` : 'Numarasız', d.discipline, `${d.fragments?.length || 0} parça`, `${d.options?.length || 0} şık`].filter(Boolean).join(' · '),
        at: x.updatedAt || x.createdAt, action: 'Düzenle', run: () => onEditDraft(d),
      });
    }
    for (const n of notifications) {
      if (n.isRead) continue;
      out.push({
        key: `n-${n.id}`, g: n.type === 'comment' ? 'people' : 'content', prio: 3, type: NOTICE_TYPE[n.type] || 'Bildirim', tone: '',
        title: n.title || n.message, meta: [n.message !== n.title ? n.message : '', n.author].filter(Boolean).join(' · '),
        at: n.timestamp, action: 'Gelen kutusu', run: () => onGo('inbox'),
      });
    }
    for (const c of comments) {
      out.push({
        key: `c-${c.id}`, g: 'people', prio: 4, type: 'Yorum', tone: '',
        title: c.text, meta: [c.author || 'Öğrenci', c.questionTopic || `Soru #${c.questionId}`].join(' · '),
        at: c.createdAt, action: 'Moderasyon', run: () => onGo('inbox'),
      });
    }
    return out.sort((a, b) => a.prio - b.prio || toMs(b.at) - toMs(a.at));
  }, [pendingReports, drafts, notifications, comments, cells, onGo, onReviewReport, onEditDraft]);

  const qCount = (g: 'all' | QGroup) => (g === 'all' ? queue.length : queue.filter((x) => x.g === g).length);
  const shownQ = (qf === 'all' ? queue : queue.filter((x) => x.g === qf)).slice(0, 8);

  const acts = useMemo(() => {
    type A = { key: string; kind: 'report' | 'comment' | 'notice'; at?: string; who: string; what: string; target: string; qid?: string };
    const out: A[] = [];
    for (const r of pendingReports) out.push({ key: `r${r.id}`, kind: 'report', at: r.createdAt, who: r.reportedBy || 'Anonim', what: `Hata bildirdi: ${r.reason}`, target: r.questionTopic || `Soru #${r.questionId}`, qid: r.questionId });
    for (const c of comments) out.push({ key: `c${c.id}`, kind: 'comment', at: c.createdAt, who: c.author || 'Öğrenci', what: `Yorum: ${c.text}`, target: c.questionTopic || `Soru #${c.questionId}`, qid: c.questionId });
    for (const n of notifications) {
      const qid = n.questionId && !/[:·\s]/.test(n.questionId) ? n.questionId : undefined;
      out.push({ key: `n${n.id}`, kind: 'notice', at: n.timestamp, who: n.author || 'Sistem', what: n.title || n.message, target: qid ? `Soru #${qid}` : n.message && n.message !== n.title ? n.message : '—', qid });
    }
    return out.sort((a, b) => toMs(b.at) - toMs(a.at));
  }, [pendingReports, comments, notifications]);
  const shownActs = (af === 'all' ? acts : acts.filter((a) => a.kind === af)).slice(0, 8);

  const quick: { id: ManageSection; label: string; icon: React.ElementType; pri?: boolean }[] = [
    { id: 'moderation', label: pendingReports.length ? `Bildirimleri incele (${pendingReports.length})` : 'Moderasyon', icon: Flag, pri: pendingReports.length > 0 },
    { id: 'inbox', label: 'Gelen kutusu', icon: Inbox },
    { id: 'drafts', label: 'Taslakları kümele', icon: Layers },
    { id: 'ders_isci', label: 'Yeni dersleri onayla', icon: BookOpenCheck },
    { id: 'scripts', label: 'Betik çalıştır', icon: Terminal },
    { id: 'catalog', label: 'Veri kataloğu', icon: Boxes },
    { id: 'people', label: 'Kişiler', icon: UserSearch },
    { id: 'database', label: 'Veritabanı ve yedek', icon: HardDrive },
  ];

  return (
    <div className="m12-ov">
      <section className="m12-panel" aria-label="Servis durumu">
        <div className="m12-health">
          {cells.map((c) => (
            <span key={c.name} className="m12-hc">
              <span className={`m12-dot ${c.dot}`} aria-hidden="true" />
              <b>{c.name}</b>
              <span className="t">{c.text}</span>
            </span>
          ))}
          <button type="button" className="m12-link m12-hc-more" onClick={() => onGo('system')}>
            Sistem durumu <ChevronRight aria-hidden="true" />
          </button>
        </div>
      </section>

      <div className="m12-cols">
        <section className="m12-panel m12-col-main" aria-labelledby="m12-q-h">
          <div className="m12-panel-h">
            <h2 id="m12-q-h" className="m12-h2">
              Şimdi ilgilen <span className="m12-num m12-meta">{queue.length}</span>
            </h2>
            <div className="m12-seg" role="group" aria-label="Kuyruk süzgeci">
              {([['all', 'Tümü'], ['content', 'İçerik'], ['people', 'Kişiler'], ['system', 'Sistem']] as const).map(([k, l]) => (
                <button key={k} type="button" className={qf === k ? 'on' : ''} aria-pressed={qf === k} onClick={() => setQf(k)}>
                  {l}
                  {qCount(k) > 0 && <span className="m12-num n">{qCount(k)}</span>}
                </button>
              ))}
            </div>
          </div>
          {shownQ.length === 0 ? (
            <p className="m12-empty">Şu an bekleyen iş yok. Yeni bildirim, taslak ya da yorum geldiğinde burada sıralanır.</p>
          ) : (
            <ul className="m12-queue">
              {shownQ.map((it) => (
                <li key={it.key} className="m12-q">
                  <span className="tp"><span className={`m12-badge ${it.tone}`}>{it.type}</span></span>
                  <span className="mid">
                    <span className="tt m12-clamp1">{it.title}</span>
                    <span className="mt m12-clamp1">{it.meta}</span>
                  </span>
                  <span className="ag m12-num">{it.at ? ageOf(it.at) : ''}</span>
                  <button type="button" className="m12-btn sm act" onClick={it.run} aria-label={`${it.action}: ${it.title}`}>
                    {it.action}
                  </button>
                </li>
              ))}
            </ul>
          )}
          <div className="m12-panel-f">
            <span className="m12-meta">Önceliğe göre sıralı: bildirimler ve sistem sorunları önce, sonra taslaklar, sonra yorumlar.</span>
            <button type="button" className="m12-link" onClick={() => onGo('inbox')}>
              Tüm bekleyenler <ChevronRight aria-hidden="true" />
            </button>
          </div>
        </section>

        <aside className="m12-col-side">
          <section className="m12-panel" aria-labelledby="m12-hq-h">
            <div className="m12-panel-h"><h2 id="m12-hq-h" className="m12-h2">Hızlı işlemler</h2></div>
            <div className="m12-quick">
              {quick.map((a) => {
                const Icon = a.icon;
                return (
                  <button key={a.id} type="button" className={`m12-btn sm ${a.pri ? 'pri' : ''}`} onClick={() => onGo(a.id)}>
                    <Icon aria-hidden="true" />
                    {a.label}
                  </button>
                );
              })}
            </div>
          </section>
          <section className="m12-panel" aria-labelledby="m12-rc-h">
            <div className="m12-panel-h"><h2 id="m12-rc-h" className="m12-h2">Kayıtlar</h2></div>
            <dl className="m12-dl">
              <dt>Bekleyen bildirim</dt><dd className="m12-num">{pendingReports.length.toLocaleString('tr-TR')}</dd>
              <dt>Taslak</dt><dd className="m12-num">{drafts.length.toLocaleString('tr-TR')}</dd>
              <dt>Yorum</dt><dd className="m12-num">{comments.length.toLocaleString('tr-TR')}</dd>
              <dt>Kayıtlı kullanıcı</dt><dd className="m12-num">{usersCount.toLocaleString('tr-TR')}</dd>
              <dt>Havuz sorusu</dt><dd className="m12-num">{questionsCount.toLocaleString('tr-TR')}</dd>
            </dl>
          </section>
        </aside>
      </div>

      <section className="m12-panel" aria-labelledby="m12-act-h">
        <div className="m12-panel-h">
          <h2 id="m12-act-h" className="m12-h2">Son hareketler</h2>
          <div className="m12-seg" role="group" aria-label="Hareket türü">
            {([['all', 'Tümü'], ['report', 'Bildirim'], ['comment', 'Yorum'], ['notice', 'Sistem']] as const).map(([k, l]) => (
              <button key={k} type="button" className={af === k ? 'on' : ''} aria-pressed={af === k} onClick={() => setAf(k)}>{l}</button>
            ))}
          </div>
          <button type="button" className="m12-btn sm ghost" onClick={() => onGo('inbox')}>
            Gelen kutusu <ChevronRight aria-hidden="true" />
          </button>
        </div>
        {shownActs.length === 0 ? (
          <p className="m12-empty">Kayıtlı hareket yok.</p>
        ) : (
          <div className="m12-tbl-box">
            <table className="m12-tbl">
              <thead>
                <tr><th className="w-t">Zaman</th><th className="w-k">Kim</th><th>İşlem</th><th>Hedef</th></tr>
              </thead>
              <tbody>
                {shownActs.map((a) => (
                  <tr key={a.key}>
                    <td><span className="m12-num">{clockOf(a.at)}</span></td>
                    <td className="k"><span className="m12-clamp1">{a.who}</span></td>
                    <td><span className="m12-clamp1">{a.what}</span></td>
                    <td>
                      {a.qid ? (
                        <button type="button" className="m12-link m12-clamp1" onClick={() => onOpenQuestion(a.qid!)} title="Veri tablosunda aç">{a.target}</button>
                      ) : (
                        <span className="m12-clamp1">{a.target}</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
};
