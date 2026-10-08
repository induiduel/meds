import React, { useEffect, useMemo, useState } from 'react';
import { Activity, RefreshCw, Radio, Server, Terminal, Copy, Check, AlertTriangle, Eraser } from 'lucide-react';
import { multiDbManager } from '../../services/multiDbManager';
import { systemHealthMonitor, SystemOverallHealth } from '../../services/systemHealthMonitor';
import { fetchSystemServices, fetchWorkerHeartbeat, ManageServiceItem } from '../../services/manageConsoleService';
import { consoleLogBuffer, ManageLogEntry } from './ConsoleLogBuffer';
import { Panel, EmptyState, Seg } from './consoleUi';

/**
 * Sistem: veritabanı ve AI sağlığı tek şeritte, arka plan servisleri kategoriye göre,
 * tarayıcı konsolu canlı günlük ekranında.
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
  const shownLogs = logs.filter((l) => level === 'all' || l.level === level).slice(-300);

  const status = [
    { name: 'Firebase', s: health.firebase.status, detail: health.firebase.details || '' },
    { name: 'Supabase', s: health.supabase.status, detail: health.supabase.details || '' },
    {
      name: 'Yapay zeka',
      s: health.ai.status,
      detail: health.ai.lastAiError ? `${health.ai.lastAiError.provider}: ${health.ai.lastAiError.message.slice(0, 90)}` : 'Hata kaydı yok',
    },
  ];

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <section className="ms-panel ms-statusgrid grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4" aria-label="Sistem durumu">
        {status.map((x) => (
          <div key={x.name} className="px-4 py-3.5 flex flex-col gap-1 min-w-0">
            <span className="text-[12.5px] font-medium text-ink-3">{x.name}</span>
            <span className="flex items-center gap-2 text-[15px] font-semibold text-ink">
              <span className={`ms-sdot ${toneOf(x.s)}`} aria-hidden="true" />
              {STATUS_LABEL[x.s] || x.s}
            </span>
            <span className="text-[12.5px] text-ink-3 truncate" title={x.detail}>{x.detail}</span>
          </div>
        ))}
        <div className="px-4 py-3.5 flex flex-col gap-1 min-w-0">
          <span className="text-[12.5px] font-medium text-ink-3">Arka plan işçisi</span>
          <span className="flex items-center gap-2 text-[15px] font-semibold text-ink">
            <span className={`ms-sdot ${heartbeat ? (heartbeat.isOnline ? 'is-ok is-live' : 'is-bad') : ''}`} aria-hidden="true" />
            {heartbeat ? (heartbeat.isOnline ? 'Çevrimiçi' : 'Çevrimdışı') : 'Bilinmiyor'}
          </span>
          <span className="text-[12.5px] text-ink-3 truncate" title={heartbeat?.message}>
            {heartbeat ? `${heartbeat.diffSeconds !== undefined ? `${heartbeat.diffSeconds} sn önce · ` : ''}${heartbeat.message}` : 'Servisler yüklenince görünür'}
          </span>
        </div>
      </section>

      {exhausted.length > 0 && (
        <div role="alert" className="ms-alert is-bad">
          <AlertTriangle aria-hidden="true" />
          <span>
            <b>Limite ulaşan AI anahtarları:</b> {exhausted.map((k) => `${k.label} (${STATUS_LABEL[k.status] || k.status})`).join(' · ')}
          </span>
        </div>
      )}

      <div className="flex flex-wrap items-center gap-2">
        <button type="button" onClick={() => void diagnose()} disabled={diagnosing} className="ms-btn is-primary">
          <Activity className={diagnosing ? 'animate-pulse' : ''} /> {diagnosing ? 'Teşhis sürüyor…' : 'Tam teşhis çalıştır'}
        </button>
        <button type="button" onClick={() => void realtimeTest()} disabled={realtime.running} className="ms-btn">
          <Radio /> {realtime.running ? 'Realtime test ediliyor…' : 'Realtime tur testi'}
        </button>
        {realtime.message && <span className="text-[13px] text-ink-2">{realtime.message}</span>}
      </div>

      <Panel
        flush
        title="Servisler"
        icon={Server}
        tools={
          <>
            {services.length > 0 && (
              <>
                <span className="ms-tag is-ok">{running} çalışıyor</span>
                <span className="ms-tag">{services.length - running} duruyor</span>
              </>
            )}
            <button type="button" onClick={() => void loadServices()} disabled={loadingServices} className="ms-btn is-sm is-ghost" aria-label="Servisleri yenile">
              <RefreshCw className={loadingServices ? 'animate-spin' : ''} /> Yenile
            </button>
          </>
        }
      >
        {services.length === 0 ? (
          <EmptyState icon={Server} title={loadingServices ? 'Servisler yükleniyor…' : 'Servis bilgisi yok'}>
            {loadingServices ? null : 'Yerel sunucu çevrimdışı olabilir.'}
          </EmptyState>
        ) : (
          <ul className="ms-rows">
            {groups.map(([cat, items]) => (
              <React.Fragment key={cat}>
                {groups.length > 1 && <li className="ms-day" aria-hidden="true">{CATEGORY_LABEL[cat.toLowerCase()] || cat}</li>}
                {items.map((s) => {
                  const on = isRunning(s);
                  return (
                    <li key={s.id} className="ms-row !py-2.5 items-center">
                      <span className={`ms-sdot ${on ? 'is-ok' : ''}`} aria-hidden="true" />
                      <div className="ms-row-main !gap-0.5">
                        <span className="text-[14px] font-medium text-ink truncate">{s.name}</span>
                        {s.description && <span className="text-[12.5px] text-ink-3 truncate" title={s.description}>{s.description}</span>}
                      </div>
                      <span className={`text-[12.5px] font-semibold shrink-0 ${on ? 'text-ok' : 'text-ink-3'}`}>{s.statusLabel || s.status}</span>
                    </li>
                  );
                })}
              </React.Fragment>
            ))}
          </ul>
        )}
      </Panel>

      <Panel
        title="Tarayıcı konsolu"
        icon={Terminal}
        count={logs.length}
        tools={
          <>
            <Seg
              label="Günlük seviyesi"
              value={level}
              onChange={setLevel}
              options={[
                { id: 'all', label: 'Tümü' },
                { id: 'error', label: 'Hata', n: levelCount('error') || undefined },
                { id: 'warn', label: 'Uyarı', n: levelCount('warn') || undefined },
                { id: 'info', label: 'Bilgi' },
                { id: 'log', label: 'Log' },
              ]}
            />
            <button
              type="button"
              onClick={() => {
                void navigator.clipboard.writeText(logs.map((l) => `[${l.ts}][${l.level}][${l.source}] ${l.message}`).join('\n'));
                setCopied(true);
                window.setTimeout(() => setCopied(false), 2000);
              }}
              className="ms-btn is-sm is-ghost"
            >
              {copied ? <Check /> : <Copy />} {copied ? 'Kopyalandı' : 'Kopyala'}
            </button>
            <button type="button" onClick={() => consoleLogBuffer.clear()} className="ms-btn is-sm is-ghost">
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
