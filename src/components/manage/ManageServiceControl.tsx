import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Power, RefreshCw, Play, Square, RotateCcw, ScrollText, Copy } from 'lucide-react';
import { adminCall } from '../../services/peopleService';
import { ADMIN_EMAIL } from '../../services/auth';
import { Panel, EmptyState, Drawer } from './consoleUi';
import { Pill } from '../v14/pageKit';
import { BulkBar, useSelection, SelectAllBox } from '../v14/manageKit';

/**
 * Yönetim › Sistem › Servis denetimi. Sunucu: src/services/serviceControlRoutes.ts (beyaz liste, güçlü yönetici).
 * Yerel cihazda systemctl --user doğrudan; Oracle'da host işçisi (servis_isci.sh) istek dosyasını işler → sonuç yoklanır.
 * İzinli eylemler sunucudan gelir (meds-web/meds-app/meds-pg yalnız yeniden başlatma, GPU işçisi yalnız durdurma).
 */
type Action = 'restart' | 'stop' | 'start';
type Svc = {
  id: string;
  label: string;
  kind: string;
  actions: Action[];
  note?: string;
  self?: boolean;
  active: string;
  sub: string;
  enabled: string;
  since: string;
  loaded: boolean;
};
type ListRes = { machine: 'yerel' | 'oracle'; statusAt: string | null; helperOnline: boolean; services: Svc[] };
type ActRes = { ok?: boolean; pending?: boolean; requestId?: string; message?: string; delayed?: boolean };

const ACT_LABEL: Record<Action, string> = { restart: 'Yeniden başlat', stop: 'Durdur', start: 'Başlat' };
const ACT_ICON: Record<Action, React.ElementType> = { restart: RotateCcw, stop: Square, start: Play };
const headers = { 'x-admin-email': ADMIN_EMAIL };
const wait = (ms: number) => new Promise((r) => window.setTimeout(r, ms));

const tone = (s: Svc): 'ok' | 'bad' | 'warn' | '' => (!s.loaded ? 'warn' : s.active === 'active' ? 'ok' : s.active === 'failed' ? 'bad' : s.active === 'activating' || s.active === 'deactivating' ? 'warn' : '');
const stateLabel = (s: Svc) =>
  !s.loaded ? 'Bulunamadı' : s.active === 'active' ? (s.sub === 'waiting' ? 'Bekliyor' : 'Çalışıyor') : s.active === 'failed' ? 'Hata' : s.active === 'inactive' ? 'Durdu' : s.active === 'unknown' ? 'Bilinmiyor' : s.active;

export const ManageServiceControl: React.FC<{ notify: (msg: string) => void }> = ({ notify }) => {
  const [data, setData] = useState<ListRes | null>(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState<Record<string, string>>({});
  const [armed, setArmed] = useState<string>('');
  const [logFor, setLogFor] = useState<Svc | null>(null);
  const [log, setLog] = useState<{ text: string; at: string | null; note?: string; loading: boolean }>({ text: '', at: null, loading: false });
  const sel = useSelection<string>();
  const alive = useRef(true);
  useEffect(() => () => void (alive.current = false), []);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setData(await adminCall<ListRes>('/api/admin/servis/list'));
      setErr('');
    } catch (e) {
      setErr(e instanceof Error ? e.message : 'Servis listesi alınamadı.');
    } finally {
      setLoading(false);
    }
  }, []);
  useEffect(() => void load(), [load]);

  useEffect(() => {
    if (!armed) return;
    const t = window.setTimeout(() => setArmed(''), 4000);
    return () => window.clearTimeout(t);
  }, [armed]);

  /** Oracle isteği: host işçisi sonucu yazana dek yokla (en çok ~3 dk) */
  const pollResult = async (id: string): Promise<{ ok: boolean; message: string }> => {
    for (let i = 0; i < 90 && alive.current; i++) {
      await wait(2000);
      try {
        const r = await adminCall<{ done: boolean; ok?: boolean; message?: string }>(`/api/admin/servis/result/${encodeURIComponent(id)}`);
        if (r.done) return { ok: !!r.ok, message: r.message || '' };
      } catch {
        /* meds-app yeniden başlarken kısa kesinti olabilir */
      }
    }
    return { ok: false, message: 'Host işçisi yanıt vermedi (meds-servis-isci.path kurulu mu?).' };
  };

  const act = async (s: Svc, action: Action): Promise<boolean> => {
    setBusy((b) => ({ ...b, [s.id]: action }));
    try {
      const r = await adminCall<ActRes>('/api/admin/servis/action', { method: 'POST', headers, body: JSON.stringify({ service: s.id, action }) });
      if (r.pending && r.requestId) {
        notify(r.message || `${s.label}: istek iletildi, işleniyor…`);
        const out = await pollResult(r.requestId);
        notify(out.message || `${s.label}: tamam.`);
        return out.ok;
      }
      notify(r.message || `${s.label}: tamam.`);
      return true;
    } catch (e) {
      notify(e instanceof Error ? e.message : `${s.label}: işlem başarısız.`);
      return false;
    } finally {
      if (alive.current) setBusy((b) => {
        const n = { ...b };
        delete n[s.id];
        return n;
      });
    }
  };

  const onAct = async (s: Svc, action: Action) => {
    const key = `${s.id}:${action}`;
    if (armed !== key) return setArmed(key); // ikinci dokunuşta uygula
    setArmed('');
    await act(s, action);
    await wait(data?.machine === 'oracle' ? 500 : 800);
    void load();
  };

  const services = data?.services || [];
  const keys = services.map((s) => s.id);
  const picked = services.filter((s) => sel.has(s.id));
  const restartable = picked.filter((s) => s.actions.includes('restart') && !s.self);
  const selfPicked = picked.find((s) => s.self && s.actions.includes('restart'));

  const bulkRestart = async () => {
    // Sırayla; panelin kendi sunucusu (seçildiyse) en sona
    for (const s of restartable) {
      await act(s, 'restart');
      await wait(400);
    }
    if (selfPicked) await act(selfPicked, 'restart');
    sel.clear();
    void load();
  };

  const loadLog = useCallback(async (s: Svc) => {
    setLog((l) => ({ ...l, loading: true }));
    try {
      const r = await adminCall<{ lines: string; at: string | null; note?: string }>(`/api/admin/servis/logs?service=${encodeURIComponent(s.id)}&lines=300`);
      setLog({ text: r.lines || '', at: r.at, note: r.note, loading: false });
    } catch (e) {
      setLog({ text: e instanceof Error ? e.message : 'Günlük alınamadı.', at: null, loading: false });
    }
  }, []);
  const openLog = (s: Svc) => {
    setLogFor(s);
    setLog({ text: '', at: null, loading: true });
    void loadLog(s);
  };

  const running = services.filter((s) => s.active === 'active').length;
  const nRestart = restartable.length + (selfPicked ? 1 : 0);

  return (
    <>
      <BulkBar
        count={picked.length}
        noun="servis"
        onClear={sel.clear}
        busy={Object.keys(busy).length > 0}
        actions={[
          {
            label: nRestart ? `Yeniden başlat (${nRestart})` : 'Yeniden başlatılabilir servis yok',
            kind: 'danger',
            confirm: `${nRestart} servisi yeniden başlatmayı onayla${selfPicked ? ' (panel sunucusu en sonda)' : ''}`,
            disabled: nRestart === 0,
            run: bulkRestart,
          },
        ]}
      />
      <Panel
        flush
        title={`Servis denetimi · ${data?.machine === 'oracle' ? 'Oracle' : data ? 'Yerel cihaz' : '…'}`}
        icon={Power}
        desc={
          data?.machine === 'oracle'
            ? data.helperOnline
              ? `Host işçisi çevrim içi · durum ${data.statusAt ? new Date(data.statusAt).toLocaleTimeString('tr-TR') : '—'} (dakikada bir yenilenir)`
              : 'Host işçisi çevrim dışı: durum ve günlükler eski olabilir, eylemler uygulanmaz (meds-servis-isci kurulumu gerekli).'
            : 'Eylemler iki dokunuşla uygulanır. Panel sunucusu ve veritabanı yalnız yeniden başlatılır; GPU işçisi yalnız durdurulur.'
        }
        tools={
          <>
            {services.length > 0 && (
              <>
                <Pill tone="ok">{running} çalışıyor</Pill>
                <SelectAllBox all={sel.allOf(keys)} some={sel.someOf(keys)} onChange={() => sel.toggleAll(keys)} label="Tüm servisleri seç" />
              </>
            )}
            <button type="button" className="m14-btn ghost" onClick={() => void load()} disabled={loading}>
              <RefreshCw className={loading ? 'animate-spin' : ''} aria-hidden="true" /> Yenile
            </button>
          </>
        }
      >
        {services.length === 0 ? (
          <EmptyState icon={Power} title={loading ? 'Servisler yükleniyor…' : 'Servis denetimi kullanılamıyor'}>
            {loading ? null : err || 'Sunucu servis listesi döndürmedi.'}
          </EmptyState>
        ) : (
          <div className="grid gap-2 p-3" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(min(100%, 300px), 1fr))' }}>
            {services.map((s) => {
              const isPicked = sel.has(s.id);
              const doing = busy[s.id];
              return (
                <div
                  key={s.id}
                  className="flex flex-col gap-2 p-3 rounded-xl min-w-0"
                  style={{ border: `1px solid ${isPicked ? 'var(--color-accent)' : 'var(--color-line)'}`, background: isPicked ? 'var(--color-accent-soft)' : 'transparent' }}
                >
                  <label className="flex items-start gap-3 cursor-pointer min-w-0">
                    <input type="checkbox" checked={isPicked} onChange={() => sel.toggle(s.id)} aria-label={`Seç: ${s.label}`} style={{ width: 18, height: 18, accentColor: 'var(--color-accent)', flex: 'none', marginTop: 2 }} />
                    <span className="flex flex-col gap-0.5 min-w-0 flex-1">
                      <span className="text-base font-medium text-ink truncate">{s.label}</span>
                      <span className="text-sm text-ink-3 truncate" title={s.id}>
                        {s.id}
                        {s.since && s.active === 'active' ? ` · ${s.since}` : ''}
                      </span>
                      {s.note && <span className="text-sm text-ink-3">{s.note}</span>}
                    </span>
                    <Pill tone={doing ? 'acc' : tone(s)}>{doing ? 'İşleniyor…' : stateLabel(s)}</Pill>
                  </label>
                  <div className="flex flex-wrap gap-1.5">
                    {s.actions.map((a) => {
                      const Icon = ACT_ICON[a];
                      const isArmed = armed === `${s.id}:${a}`;
                      return (
                        <button
                          key={a}
                          type="button"
                          className={`m14-btn ${isArmed || a === 'stop' ? 'danger' : ''}`}
                          disabled={!!doing || (data?.machine === 'oracle' && !data.helperOnline)}
                          onClick={() => void onAct(s, a)}
                          aria-label={`${ACT_LABEL[a]}: ${s.label}`}
                        >
                          <Icon aria-hidden="true" /> {isArmed ? 'Onayla' : ACT_LABEL[a]}
                        </button>
                      );
                    })}
                    <button type="button" className="m14-btn ghost" onClick={() => openLog(s)}>
                      <ScrollText aria-hidden="true" /> Günlük
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </Panel>

      <Drawer
        open={!!logFor}
        onClose={() => setLogFor(null)}
        wide
        title={logFor ? `Günlük · ${logFor.label}` : 'Günlük'}
        head={
          logFor ? (
            <>
              <button type="button" className="m14-btn ghost" onClick={() => void loadLog(logFor)} disabled={log.loading}>
                <RefreshCw className={log.loading ? 'animate-spin' : ''} aria-hidden="true" /> Yenile
              </button>
              <button
                type="button"
                className="m14-btn ghost"
                onClick={() => {
                  void navigator.clipboard.writeText(log.text);
                  notify('Günlük kopyalandı.');
                }}
              >
                <Copy aria-hidden="true" /> Kopyala
              </button>
            </>
          ) : undefined
        }
      >
        <p className="text-sm text-ink-3 m-0 mb-2">
          {logFor?.id}
          {log.at ? ` · ${new Date(log.at).toLocaleString('tr-TR')}` : ''}
          {log.note ? ` · ${log.note}` : ''}
        </p>
        <pre className="ms-term" style={{ maxHeight: 'none', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
          {log.loading && !log.text ? 'Yükleniyor…' : log.text || 'Kayıt yok.'}
        </pre>
      </Drawer>
    </>
  );
};
