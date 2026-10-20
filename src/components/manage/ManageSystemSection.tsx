import React, { useEffect, useMemo, useState } from 'react';
import { Activity, RefreshCw, Radio, Server, Terminal, Copy, Check, AlertTriangle, Eraser } from 'lucide-react';
import { multiDbManager } from '../../services/multiDbManager';
import { systemHealthMonitor, SystemOverallHealth } from '../../services/systemHealthMonitor';
import { fetchSystemServices, fetchWorkerHeartbeat, ManageServiceItem } from '../../services/manageConsoleService';
import { consoleLogBuffer, ManageLogEntry } from './ConsoleLogBuffer';
import { Panel, EmptyState, Seg } from './consoleUi';
import { PageActions, StatRow, SearchField, Pill } from '../v14/pageKit';
import { BulkBar, useSelection, SelectAllBox } from '../v14/manageKit';

/**
 * Sistem (v14, canvas Sistem.dc.html): eylemler → durum sayıları → seçilebilir servis kartları (toplu çubuk) →
 * düzey süzgeçli ve aramalı günlük ekranı. Servis yeniden başlatma ucu yok; toplu işlem bilgiyi kopyalar.
 */
const STATUS_LABEL: Record<string, string> = {
  online: 'Çevrimiçi',
  offline: 'Çevrimdışı',
  ready: 'Hazır',
  degraded: 'Kısıtlı',
  all_exhausted: 'Tüm anahtarlar dolu',
  quota_exceeded: 'Kota doldu',
  spending_cap_exceeded: 'Harcama sınırı',
  permission_denied: 'Yetki yok',
  network_error: 'Ağ hatası',
  missing_tables: 'Tablo eksik',
  auth_error: 'Kimlik hatası',
  not_configured: 'Ayarlanmamış',
  high_demand: 'Yoğun',
  error: 'Hata',
  ok: 'Hazır',
};
const toneOf = (s: string) => (/^(online|ready|ok)$/.test(s) ? 'is-ok' : /offline|error|denied|exhausted|missing/.test(s) ? 'is-bad' : 'is-warn');
const CATEGORY_LABEL: Record<string, string> = {
  core: 'Çekirdek',
  network: 'Ağ',
  watcher: 'İzleyiciler',
  ai: 'Yapay zeka',
  sync: 'Eşitleme',
  data: 'Veri',
  worker: 'Arka plan işçileri',
  database: 'Veritabanı',
  pipeline: 'Veri hattı',
};
const isRunning = (s: ManageServiceItem) => /active|çalış|online|açık/i.test(s.status) || /active|çalış|online|açık/i.test(s.statusLabel);

type Level = 'all' | ManageLogEntry['level'];

export const ManageSystemSection: React.FC<{ notify: (msg: string) => void }> = ({ notify }) => {
  const [health, setHealth] = useState<SystemOverallHealth>(() => systemHealthMonitor.getHealth());
  const [diagnosing, setDiagnosing] = useState(false);
  const [services, setServices] = useState<ManageServiceItem[]>([]);
  const [loadingServices, setLoadingServices] = useState(false);
  const [heartbeat, setHeartbeat] = useState<{ isOnline: boolean; diffSeconds?: number; message: string } | null>(null);
  const [logs, setLogs] = useState<ManageLogEntry[]>(() => consoleLogBuffer.getEntries());
  const [level, setLevel] = useState<Level>('all');
  const [copied, setCopied] = useState(false);
  const [realtime, setRealtime] = useState<{ running: boolean; message?: string }>({ running: false });
  const [logQ, setLogQ] = useState('');
  const [live, setLive] = useState(true);
  const [frozen, setFrozen] = useState<ManageLogEntry[] | null>(null);
  const svcSel = useSelection<string>();

  useEffect(() => {
    consoleLogBuffer.install();
    const a = consoleLogBuffer.subscribe(setLogs);
    const b = systemHealthMonitor.subscribe(setHealth);
    void loadServices();
    return () => {
      a();
      b();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadServices = async () => {
    setLoadingServices(true);
    try {
      const [svc, hb] = await Promise.all([fetchSystemServices(), fetchWorkerHeartbeat()]);
      setServices(svc.services);
      setHeartbeat(hb);
      if (!svc.ok) notify(svc.message);
    } finally {
      setLoadingServices(false);
    }
  };

  const diagnose = async () => {
    setDiagnosing(true);
    try {
      await systemHealthMonitor.runFullDiagnostic(true, true);
    } finally {
      setDiagnosing(false);
    }
  };

  const realtimeTest = async () => {
    setRealtime({ running: true });
    try {
      const res = await multiDbManager.testRealtimeRoundtrip(4500);
      setRealtime({ running: false, message: res.message });
    } catch (e) {
      setRealtime({ running: false, message: e instanceof Error ? e.message : 'Test başarısız.' });
    }
  };

  const exhausted = health.ai.keys.filter((k) => k.status === 'quota_exceeded' || k.status === 'spending_cap_exceeded');
  const running = services.filter(isRunning).length;
  const groups = useMemo(() => {
    const m = new Map<string, ManageServiceItem[]>();
    for (const s of services) {
      const k = s.category || 'Diğer';
      m.set(k, [...(m.get(k) || []), s]);
    }
    return [...m.entries()];
  }, [services]);

  const levelCount = (lv: ManageLogEntry['level']) => logs.filter((l) => l.level === lv).length;
  const lq = logQ.toLocaleLowerCase('tr-TR').trim();
  const shownLogs = (live ? logs : frozen || logs)
    .filter((l) => (level === 'all' || l.level === level) && (!lq || `${l.source} ${l.message}`.toLocaleLowerCase('tr-TR').includes(lq)))
    .slice(-300);
  const svcKeys = services.map((s) => s.id);
  const pickedSvc = services.filter((s) => svcSel.has(s.id));
  const copySvc = () => {
    void navigator.clipboard.writeText(pickedSvc.map((s) => `${s.name}\t${s.statusLabel || s.status}\t${s.description || ''}`).join('\n'));
    notify(`${pickedSvc.length} servis bilgisi kopyalandı.`);
  };

  const status = [
    { name: 'Firebase', s: health.firebase.status, detail: health.firebase.details || '' },
    { name: 'Veritabanı (meds-pg)', s: health.supabase.status, detail: health.supabase.details || '' },
    {
      name: 'Yapay zeka',
      s: health.ai.status,
      detail: health.ai.lastAiError ? `${health.ai.lastAiError.provider}: ${health.ai.lastAiError.message.slice(0, 90)}` : 'Hata kaydı yok',
    },
  ];

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <PageActions note={realtime.message}>
        <button type="button" onClick={() => void diagnose()} disabled={diagnosing} className="m14-btn primary">
          <Activity className={diagnosing ? 'animate-pulse' : ''} aria-hidden="true" /> {diagnosing ? 'Teşhis sürüyor…' : 'Tam teşhis çalıştır'}
        </button>
        <button type="button" onClick={() => void realtimeTest()} disabled={realtime.running} className="m14-btn">
          <Radio aria-hidden="true" /> {realtime.running ? 'Canlı bağlantı sınanıyor…' : 'Canlı bağlantı tur testi'}
        </button>
        <button type="button" onClick={() => void loadServices()} disabled={loadingServices} className="m14-btn">
          <RefreshCw className={loadingServices ? 'animate-spin' : ''} aria-hidden="true" /> Servisleri yenile
        </button>
      </PageActions>

      <StatRow
        stats={[
          ...status.map((x) => ({ label: x.name, value: STATUS_LABEL[x.s] || x.s, tone: (toneOf(x.s) === 'is-ok' ? 'ok' : toneOf(x.s) === 'is-bad' ? 'bad' : 'warn') as 'ok' | 'bad' | 'warn', hint: x.detail })),
          {
            label: 'Arka plan işçisi',
            value: heartbeat ? (heartbeat.isOnline ? 'Çevrim içi' : 'Çevrim dışı') : 'Bilinmiyor',
            tone: heartbeat ? (heartbeat.isOnline ? 'ok' : 'bad') : undefined,
            hint: heartbeat ? `${heartbeat.diffSeconds !== undefined ? `${heartbeat.diffSeconds} sn önce · ` : ''}${heartbeat.message}` : 'Servisler yüklenince görünür',
          },
        ]}
      />

      {exhausted.length > 0 && (
        <div role="alert" className="ms-alert is-bad">
          <AlertTriangle aria-hidden="true" />
          <span>
            <b>Limite ulaşan yapay zekâ anahtarları:</b> {exhausted.map((k) => `${k.label} (${STATUS_LABEL[k.status] || k.status})`).join(' · ')}
          </span>
        </div>
      )}

      <BulkBar
        count={pickedSvc.length}
        noun="servis"
        onClear={svcSel.clear}
        actions={[{ label: 'Bilgilerini kopyala', kind: 'main', run: copySvc }]}
      />

      <Panel
        flush
        title="Servisler"
        icon={Server}
        tools={
          services.length > 0 ? (
            <>
              <Pill tone="ok">{running} çalışıyor</Pill>
              <Pill>{services.length - running} duruyor</Pill>
              <SelectAllBox all={svcSel.allOf(svcKeys)} some={svcSel.someOf(svcKeys)} onChange={() => svcSel.toggleAll(svcKeys)} label="Tüm servisleri seç" />
            </>
          ) : undefined
        }
      >
        {services.length === 0 ? (
          <EmptyState icon={Server} title={loadingServices ? 'Servisler yükleniyor…' : 'Servis bilgisi yok'}>
            {loadingServices ? null : 'Yerel sunucu çevrimdışı olabilir.'}
          </EmptyState>
        ) : (
          <div className="flex flex-col gap-3 p-3">
            {groups.map(([cat, items]) => (
              <section key={cat} className="flex flex-col gap-2" aria-label={CATEGORY_LABEL[cat.toLowerCase()] || cat}>
                {groups.length > 1 && <h3 className="m-0 text-sm font-semibold text-ink-3">{CATEGORY_LABEL[cat.toLowerCase()] || cat}</h3>}
                <div className="grid gap-2" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(min(100%, 260px), 1fr))' }}>
                  {items.map((s) => {
                    const on = isRunning(s);
                    const picked = svcSel.has(s.id);
                    return (
                      <label
                        key={s.id}
                        className="flex items-start gap-3 p-3 rounded-xl cursor-pointer min-w-0"
                        style={{ border: `1px solid ${picked ? 'var(--color-accent)' : 'var(--color-line)'}`, background: picked ? 'var(--color-accent-soft)' : 'transparent' }}
                      >
                        <input type="checkbox" checked={picked} onChange={() => svcSel.toggle(s.id)} aria-label={`Seç: ${s.name}`} style={{ width: 18, height: 18, accentColor: 'var(--color-accent)', flex: 'none', marginTop: 2 }} />
                        <span className="flex flex-col gap-0.5 min-w-0 flex-1">
                          <span className="text-base font-medium text-ink truncate">{s.name}</span>
                          {s.description && <span className="text-sm text-ink-3 truncate" title={s.description}>{s.description}</span>}
                        </span>
                        <Pill tone={on ? 'ok' : ''}>{s.statusLabel || s.status}</Pill>
                      </label>
                    );
                  })}
                </div>
              </section>
            ))}
          </div>
        )}
      </Panel>

      <Panel
        title="Günlük"
        icon={Terminal}
        count={logs.length}
        tools={
          <>
            <SearchField value={logQ} onChange={setLogQ} placeholder="Günlükte ara" label="Günlükte ara" />
            <label className="flex items-center gap-1.5 text-sm text-ink-2">
              <input
                type="checkbox"
                checked={live}
                onChange={(e) => {
                  setFrozen(e.target.checked ? null : logs);
                  setLive(e.target.checked);
                }}
              />
              Canlı akış
            </label>
            <Seg
              label="Günlük seviyesi"
              value={level}
              onChange={setLevel}
              options={[
                { id: 'all', label: 'Tümü' },
                { id: 'error', label: 'Hata', n: levelCount('error') || undefined },
                { id: 'warn', label: 'Uyarı', n: levelCount('warn') || undefined },
                { id: 'info', label: 'Bilgi' },
                { id: 'log', label: 'Kayıt' },
              ]}
            />
            <button
              type="button"
              onClick={() => {
                void navigator.clipboard.writeText(logs.map((l) => `[${l.ts}][${l.level}][${l.source}] ${l.message}`).join('\n'));
                setCopied(true);
                window.setTimeout(() => setCopied(false), 2000);
              }}
              className="m14-btn ghost"
            >
              {copied ? <Check /> : <Copy />} {copied ? 'Kopyalandı' : 'Kopyala'}
            </button>
            <button type="button" onClick={() => consoleLogBuffer.clear()} className="m14-btn ghost">
              <Eraser /> Temizle
            </button>
          </>
        }
      >
        <pre className="ms-term" aria-live="polite">
          {shownLogs.length === 0 ? (
            <span className="t">Henüz kayıt yok.</span>
          ) : (
            shownLogs.map((l) => (
              <div key={l.id} className={l.level === 'error' ? 'is-error' : l.level === 'warn' ? 'is-warn' : l.level === 'info' ? 'is-info' : ''}>
                <span className="t">{l.ts.slice(11, 19)} {l.source}</span> {l.message}
              </div>
            ))
          )}
        </pre>
      </Panel>
    </div>
  );
};
