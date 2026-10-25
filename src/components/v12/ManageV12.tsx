import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft, Search, RefreshCw, Moon, Sun, ChevronDown, ChevronRight, AlignJustify,
} from 'lucide-react';
import type { Committee, QuestionItem, AdminNotification } from '../../types';
import type { ManageSection } from '../manage/ManageConsole';
import type { InboxReport, InboxComment } from '../../services/manageConsoleService';
import { fetchSystemServices, fetchWorkerHeartbeat } from '../../services/manageConsoleService';
import { loadPeople, type PeopleList, fmtDuration } from '../../services/peopleService';
import { systemHealthMonitor, type SystemOverallHealth } from '../../services/systemHealthMonitor';
import type { RealtimeConnectionStatus } from '../../services/realtimeEvents';
import { StatRow, Card14, Tabs14, Pill, type Stat } from '../v14/pageKit';
import '../../styles/v12/manage.css';
import '../../styles/v14/manage.css';
import '../../styles/v13/manage.css';

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
  const [peopleSnap, setPeopleSnap] = useState<PeopleList | null>(null);
  const [qf, setQf] = useState<'all' | QGroup>('all');
  const [af, setAf] = useState<'all' | 'report' | 'comment' | 'notice'>('all');
  const touchStartX = useRef<number | null>(null);

  useEffect(() => systemHealthMonitor.subscribe(setHealth), []);
  useEffect(() => {
    let live = true;
    void Promise.all([fetchSystemServices(), fetchWorkerHeartbeat(), loadPeople().catch(() => null)]).then(([s, hb, ppl]) => {
      if (!live) return;
      if (s.ok) {
        const running = s.services.filter((x) => /active|çalış|online|açık/i.test(`${x.status} ${x.statusLabel}`)).length;
        setSvc({ total: s.services.length, running });
      }
      setBeat({ isOnline: hb.isOnline, message: hb.message });
      if (ppl) setPeopleSnap(ppl);
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

  const dotTone = (d: HealthCell['dot']) => (d === 'ok' ? 'ok' : d === 'bad' ? 'bad' : d === 'warn' ? 'warn' : '');
  const onlinePeople = useMemo(() => (peopleSnap?.people || []).filter((p) => p.online).slice(0, 6), [peopleSnap]);
  const stats: Stat[] = [
    { label: 'Anlık çevrimiçi', value: peopleSnap ? peopleSnap.totals.online.toLocaleString('tr-TR') : '—', tone: peopleSnap?.totals.online ? 'ok' : undefined, onClick: () => onGo('people'), hint: 'Canlı Kişileri aç' },
    { label: 'Moderasyon bekleyen', value: pendingReports.length.toLocaleString('tr-TR'), tone: pendingReports.length ? 'bad' : undefined, onClick: () => onGo('moderation'), hint: 'Moderasyonu aç' },
    { label: 'Havuz sorusu', value: questionsCount.toLocaleString('tr-TR'), onClick: () => onGo('pool'), hint: 'Soru havuzunu aç' },
    { label: 'Kayıtlı kullanıcı', value: (peopleSnap?.totals.accounts || usersCount).toLocaleString('tr-TR'), onClick: () => onGo('people'), hint: 'Kişileri aç' },
    { label: 'Bekleyen taslak', value: drafts.length.toLocaleString('tr-TR'), tone: drafts.length ? 'acc' : undefined, onClick: () => onGo('drafts'), hint: 'Taslakları aç' },
    { label: 'Haftalık çalışma', value: peopleSnap ? fmtDuration(peopleSnap.totals.weekSeconds) : comments.length.toLocaleString('tr-TR'), onClick: () => onGo('study'), hint: 'Ders ilerlemesini aç' },
  ];

  return (
    <div className="ov14">
      <StatRow stats={stats} />

      {/* Hızlı Mobil Yönetim Kısayolları */}
      <Card14
        title="Hızlı Müdahale & Uzaktan Denetim"
        tools={<button type="button" className="m14-btn ghost" onClick={() => onGo('shortcuts')}>Tüm kısayollar <ChevronRight aria-hidden="true" /></button>}
      >
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          <button type="button" onClick={() => onGo('people')} className="m14-btn !justify-start !h-10 !px-3">
            <span className="ov14-dot ok" /> Kişiler (Canlı)
          </button>
          <button type="button" onClick={() => onGo('study')} className="m14-btn !justify-start !h-10 !px-3">
            <span className="ov14-dot ok" /> Ders İlerlemesi
          </button>
          <button type="button" onClick={() => onGo('dbexplorer')} className="m14-btn !justify-start !h-10 !px-3">
            <span className="ov14-dot acc" /> meds-pg Gezgini
          </button>
          <button type="button" onClick={() => onGo('hat')} className="m14-btn !justify-start !h-10 !px-3">
            <span className="ov14-dot warn" /> Hat Panosu (K2+)
          </button>
          <button type="button" onClick={() => onGo('system')} className="m14-btn !justify-start !h-10 !px-3">
            Servis Denetimi
          </button>
          <button type="button" onClick={() => onGo('scripts')} className="m14-btn !justify-start !h-10 !px-3">
            Betikler & Zincir
          </button>
          <button type="button" onClick={() => onGo('intake')} className="m14-btn !justify-start !h-10 !px-3">
            Serbest Girdiler
          </button>
          <button type="button" onClick={() => onGo('kamp')} className="m14-btn !justify-start !h-10 !px-3">
            Kamp Tüyoları
          </button>
        </div>
      </Card14>

      <div className="ov14-grid">
        <Card14
          title={<>Sıradaki işler <span className="ov14-n">{queue.length.toLocaleString('tr-TR')}</span></>}
          tools={<button type="button" className="m14-btn ghost" onClick={() => onGo('inbox')}>Tümünü aç <ChevronRight aria-hidden="true" /></button>}
          flush
        >
          <div className="ov14-tabs">
            <Tabs14
              label="Kuyruk süzgeci"
              value={qf}
              onChange={setQf}
              options={([['all', 'Tümü'], ['content', 'İçerik'], ['people', 'Kişiler'], ['system', 'Sistem']] as const).map(([id, l]) => ({ id, label: l, n: qCount(id) }))}
            />
          </div>
          {shownQ.length === 0 ? (
            <p className="ov14-empty">Şu an bekleyen iş yok. Yeni bildirim, taslak ya da yorum geldiğinde burada sıralanır.</p>
          ) : (
            <ul className="ov14-list">
              {shownQ.map((it) => (
                <li
                  key={it.key}
                  className="ov14-row"
                  onTouchStart={(e) => { touchStartX.current = e.touches[0]?.clientX ?? null; }}
                  onTouchEnd={(e) => {
                    if (touchStartX.current == null) return;
                    const dx = (e.changedTouches[0]?.clientX ?? touchStartX.current) - touchStartX.current;
                    touchStartX.current = null;
                    if (dx > 64) it.run();
                  }}
                >
                  <Pill tone={it.tone}>{it.type}</Pill>
                  <span className="ov14-mid">
                    <span className="tt">{it.title}</span>
                    <span className="mt">{[it.meta, it.at ? ageOf(it.at) : ''].filter(Boolean).join(' · ')}</span>
                  </span>
                  <button type="button" className="m14-btn" onClick={it.run} aria-label={`${it.action}: ${it.title}`}>{it.action}</button>
                </li>
              ))}
            </ul>
          )}
        </Card14>

        <Card14
          title="Servis durumu & Canlı Öğrenciler"
          tools={<button type="button" className="m14-btn ghost" onClick={() => onGo('system')}>Sistem <ChevronRight aria-hidden="true" /></button>}
          flush
        >
          <ul className="ov14-list">
            {cells.map((c) => (
              <li key={c.name} className="ov14-row svc">
                <span className={`ov14-dot ${c.dot}`} aria-hidden="true" />
                <span className="ov14-name">{c.name}</span>
                <Pill tone={dotTone(c.dot)}>{c.text}</Pill>
              </li>
            ))}
            {onlinePeople.length > 0 && (
              <li className="ov14-row">
                <span className="ov14-dot ok" aria-hidden="true" />
                <span className="ov14-mid">
                  <span className="tt">Şu an çevrimiçi ({peopleSnap?.totals.online || onlinePeople.length})</span>
                  <span className="mt">{onlinePeople.map((p) => p.name || p.email || 'Öğrenci').join(', ')}</span>
                </span>
                <button type="button" className="m14-btn" onClick={() => onGo('people')}>İzle</button>
              </li>
            )}
          </ul>
        </Card14>
      </div>

      <Card14
        title="Son hareketler"
        tools={<button type="button" className="m14-btn ghost" onClick={() => onGo('inbox')}>Gelen kutusu <ChevronRight aria-hidden="true" /></button>}
        flush
      >
        <div className="ov14-tabs">
          <Tabs14
            label="Hareket türü"
            value={af}
            onChange={setAf}
            options={([['all', 'Tümü'], ['report', 'Bildirim'], ['comment', 'Yorum'], ['notice', 'Sistem']] as const).map(([id, l]) => ({ id, label: l }))}
          />
        </div>
        {shownActs.length === 0 ? (
          <p className="ov14-empty">Kayıtlı hareket yok.</p>
        ) : (
          <ul className="ov14-list">
            {shownActs.map((a) => (
              <li key={a.key} className="ov14-row act">
                <span className="ov14-time">{clockOf(a.at)}</span>
                <span className="ov14-mid">
                  <span className="tt">{a.what}</span>
                  <span className="mt">
                    {a.who} ·{' '}
                    {a.qid ? (
                      <button type="button" className="ov14-link" onClick={() => onOpenQuestion(a.qid!)} title="Veri tablosunda aç">{a.target}</button>
                    ) : (
                      a.target
                    )}
                  </span>
                </span>
              </li>
            ))}
          </ul>
        )}
      </Card14>
    </div>
  );
};
