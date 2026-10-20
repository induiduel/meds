import React, { useEffect, useState } from 'react';
import { Clock, Key, Plus, Save, Trash2, X, Bot, Eye, EyeOff, DatabaseBackup, ArrowRight } from 'lucide-react';
import {
  DEFAULT_MANAGE_SETTINGS,
  ManageAutomationSettings,
  getAiKeys,
  saveAiKeys,
  loadManageSettings,
  saveManageSettings,
} from '../../services/manageSettingsService';
import { triggerBackupNow } from '../../services/manageConsoleService';
import { AdminDriveSyncSettings } from '../AdminDriveSyncSettings';
import { Panel, Switch, Field, Drawer } from './consoleUi';
import { PageActions, StatRow, Toolbar, SearchField, DataTable, Pill, DetailNav, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';

/** Zamanlanmış iş satırı: yedek saati ya da AI penceresi */
type Job = { id: string; kind: 'backup' | 'ai'; name: string; time: string; index: number; on: boolean };

/**
 * Otomasyon (v14, canvas Otomasyon.dc.html): eylemler → sayılar → zamanlanmış işler tablosu (seçim, toplu kaldır,
 * satır → tam sayfa düzenleme) → ayar panelleri, AI anahtarları ve Drive eşitlemesi.
 * Değişiklikler tek yerden kaydedilir; kaydedilmemiş değişiklik varsa alttaki çubuk belirir.
 */
const KEY_FIELDS = [
  ['gemini', 'Gemini API anahtarı'],
  ['groq', 'Groq anahtarı 1'],
  ['groq2', 'Groq anahtarı 2'],
  ['museSpark', 'Muse Spark 1.3 Free (kota kurtarıcı)'],
] as const;

const MODELS = [
  ['gemini-3.8-flash', 'gemini-3.8-flash'],
  ['openai/gpt-oss-120b', 'openai/gpt-oss-120b (Groq)'],
  ['qwen/qwen3.8-27b', 'qwen/qwen3.8-27b (Groq)'],
  ['muse-spark-1.3-contributor-free', 'muse-spark-1.3-contributor-free'],
] as const;

export const ManageAutomationSection: React.FC<{
  adminEmail: string;
  selectedCommitteeId: string;
  onRefreshData: () => Promise<void>;
  notify: (msg: string) => void;
}> = ({ adminEmail, selectedCommitteeId, onRefreshData, notify }) => {
  const [settings, setSettings] = useState<ManageAutomationSettings>({ ...DEFAULT_MANAGE_SETTINGS });
  const [saved, setSaved] = useState<string>(JSON.stringify({ ...DEFAULT_MANAGE_SETTINGS }));
  const [keys, setKeys] = useState(() => getAiKeys());
  const [savedKeys, setSavedKeys] = useState(() => JSON.stringify(getAiKeys()));
  const [reveal, setReveal] = useState<Record<string, boolean>>({});
  const [newHour, setNewHour] = useState('03:00');
  const [saving, setSaving] = useState(false);
  const [backingUp, setBackingUp] = useState(false);
  const [jq, setJq] = useState('');
  const [openJob, setOpenJob] = useState<string | null>(null);
  const jobSel = useSelection<string>();

  useEffect(() => {
    let alive = true;
    loadManageSettings().then((s) => {
      if (!alive) return;
      setSettings(s);
      setSaved(JSON.stringify(s));
    });
    return () => {
      alive = false;
    };
  }, []);

  const dirty = JSON.stringify(settings) !== saved || JSON.stringify(keys) !== savedKeys;
  const set = (patch: Partial<ManageAutomationSettings>) => setSettings((s) => ({ ...s, ...patch }));

  const save = async () => {
    setSaving(true);
    try {
      saveAiKeys(keys);
      setSavedKeys(JSON.stringify(keys));
      const res = await saveManageSettings(adminEmail, settings);
      setSaved(JSON.stringify(settings));
      notify(res.message);
    } finally {
      setSaving(false);
    }
  };

  const backupNow = async () => {
    setBackingUp(true);
    try {
      const res = await triggerBackupNow(adminEmail);
      notify(res.message);
    } finally {
      setBackingUp(false);
    }
  };

  const addHour = () => {
    if (newHour && !settings.backupHours.includes(newHour)) set({ backupHours: [...settings.backupHours, newHour].sort() });
  };

  const jobs: Job[] = [
    ...settings.backupHours.map((h, i) => ({ id: `b-${h}`, kind: 'backup' as const, name: 'Yedekleme', time: h, index: i, on: settings.backupEnabled })),
    ...settings.aiWindows.map((w, i) => ({ id: `a-${i}`, kind: 'ai' as const, name: 'AI çalışma penceresi', time: `${w.start} – ${w.end}`, index: i, on: settings.aiAutoRunEnabled })),
  ];
  const f = jq.toLocaleLowerCase('tr-TR').trim();
  const shownJobs = f ? jobs.filter((j) => `${j.name} ${j.time}`.toLocaleLowerCase('tr-TR').includes(f)) : jobs;
  const cur = jobs.find((j) => j.id === openJob) || null;
  const removeJobs = (ids: string[]) => {
    const bh = new Set(jobs.filter((j) => ids.includes(j.id) && j.kind === 'backup').map((j) => j.time));
    const ai = new Set(jobs.filter((j) => ids.includes(j.id) && j.kind === 'ai').map((j) => j.index));
    set({ backupHours: settings.backupHours.filter((h) => !bh.has(h)), aiWindows: settings.aiWindows.filter((_, i) => !ai.has(i)) });
    notify(`${ids.length} iş kaldırıldı; kaydetmeyi unutma.`);
  };
  const jobCols: Col<Job>[] = [
    { key: 'name', label: 'İş', main: true, render: (j) => j.name },
    { key: 'state', label: 'Durum', render: (j) => (j.on ? <Pill tone="ok">Etkin</Pill> : <Pill>Kapalı</Pill>) },
    { key: 'time', label: 'Zaman', mono: true, render: (j) => j.time },
    { key: 'scope', label: 'Ayrıntı', muted: true, render: (j) => (j.kind === 'backup' ? `Kapsam: ${settings.backupScope}` : `Model: ${settings.aiModel}`) },
  ];

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <PageActions>
        <button type="button" onClick={() => void save()} disabled={saving || !dirty} className="m14-btn primary">
          <Save aria-hidden="true" /> {saving ? 'Kaydediliyor…' : 'Ayarları kaydet'}
        </button>
        <button type="button" onClick={() => void backupNow()} disabled={backingUp} className="m14-btn">
          <DatabaseBackup aria-hidden="true" /> {backingUp ? 'Yedekleniyor…' : 'Yedeği şimdi al'}
        </button>
      </PageActions>
      <StatRow
        stats={[
          { label: 'Etkin zamanlayıcı', value: jobs.filter((j) => j.on).length, tone: 'acc' },
          { label: 'Yedek saati', value: settings.backupHours.length, tone: settings.backupEnabled ? 'ok' : undefined },
          { label: 'AI penceresi', value: settings.aiWindows.length, tone: settings.aiAutoRunEnabled ? 'ok' : undefined },
        ]}
      />
      <Toolbar>
        <SearchField value={jq} onChange={setJq} placeholder="Zamanlayıcı ya da iş ara" label="İş ara" />
      </Toolbar>
      <BulkBar
        count={jobSel.count}
        noun="iş"
        onClear={jobSel.clear}
        actions={[{ label: 'Kaldır', kind: 'danger', confirm: `${jobSel.count} işi kaldırmayı onayla`, run: () => { removeJobs([...jobSel.sel]); jobSel.clear(); } }]}
      />
      <DataTable rows={shownJobs} cols={jobCols} rowKey={(j) => j.id} onOpen={(j) => setOpenJob(j.id)} selection={jobSel} activeKey={openJob} minWidth={560} empty="Zamanlanmış iş yok. Aşağıdan saat ya da pencere ekle." />
      <Drawer
        open={!!cur}
        onClose={() => setOpenJob(null)}
        title={cur ? `${cur.name} · ${cur.time}` : 'İş'}
        head={<DetailNav list={shownJobs} current={cur} same={(a, b) => a.id === b.id} onGo={(j) => setOpenJob(j.id)} />}
        foot={
          cur && (
            <>
              <button type="button" className="m14-btn danger" onClick={() => { removeJobs([cur.id]); setOpenJob(null); }}>
                <Trash2 aria-hidden="true" /> Kaldır
              </button>
              <button type="button" className="m14-btn primary" onClick={() => void save()} disabled={saving || !dirty}>
                <Save aria-hidden="true" /> {saving ? 'Kaydediliyor…' : 'Kaydet'}
              </button>
            </>
          )
        }
      >
        {cur?.kind === 'backup' && (
          <>
            <Switch checked={settings.backupEnabled} onChange={(v) => set({ backupEnabled: v })} label="Otomatik yedekleme" hint="Kapalıyken hiçbir yedek saati çalışmaz." />
            <Field label="Saat">
              <input
                type="time"
                value={cur.time}
                className="ms-input !w-[128px] font-mono"
                onChange={(e) => {
                  const v = e.target.value;
                  if (!v || settings.backupHours.includes(v)) return;
                  set({ backupHours: settings.backupHours.map((h) => (h === cur.time ? v : h)).sort() });
                  setOpenJob(`b-${v}`);
                }}
              />
            </Field>
            <Field label="Kapsam" className="max-w-xs">
              <select value={settings.backupScope} onChange={(e) => set({ backupScope: e.target.value as ManageAutomationSettings['backupScope'] })} className="ms-input">
                <option value="all">Tüm veriler</option>
                <option value="questions">Soru havuzu</option>
                <option value="past">Çıkmış sorular</option>
                <option value="notes">Ders notları</option>
              </select>
            </Field>
          </>
        )}
        {cur?.kind === 'ai' && settings.aiWindows[cur.index] && (
          <>
            <Switch checked={settings.aiAutoRunEnabled} onChange={(v) => set({ aiAutoRunEnabled: v })} label="Zamanlanmış AI çalışması" />
            <div className="flex flex-wrap items-center gap-2">
              <input type="time" value={settings.aiWindows[cur.index].start} aria-label="Başlangıç" onChange={(e) => set({ aiWindows: settings.aiWindows.map((x, xi) => (xi === cur.index ? { ...x, start: e.target.value } : x)) })} className="ms-input !w-[128px] font-mono" />
              <ArrowRight className="w-4 h-4 text-ink-3 shrink-0" aria-hidden="true" />
              <input type="time" value={settings.aiWindows[cur.index].end} aria-label="Bitiş" onChange={(e) => set({ aiWindows: settings.aiWindows.map((x, xi) => (xi === cur.index ? { ...x, end: e.target.value } : x)) })} className="ms-input !w-[128px] font-mono" />
            </div>
            <Field label="Varsayılan model" className="max-w-sm">
              <select value={settings.aiModel} onChange={(e) => set({ aiModel: e.target.value })} className="ms-input">
                {MODELS.map(([v, l]) => (
                  <option key={v} value={v}>{l}</option>
                ))}
              </select>
            </Field>
          </>
        )}
        {dirty && <p className="pk14-note">Kaydedilmemiş değişiklik var.</p>}
      </Drawer>

      <div className="bento bento-host is-duo is-rhythm" style={{ '--bt-big': 7, '--bt-small': 5 } as React.CSSProperties}>
        <Panel
          title="Yedekleme"
          icon={DatabaseBackup}
          tools={
            <button type="button" onClick={() => void backupNow()} disabled={backingUp} className="m14-btn">
              <DatabaseBackup aria-hidden="true" /> {backingUp ? 'Yedekleniyor…' : 'Şimdi yedekle'}
            </button>
          }
        >
          <Switch checked={settings.backupEnabled} onChange={(v) => set({ backupEnabled: v })} label="Otomatik yedekleme" hint="Aşağıdaki saatlerde seçili kapsam yedeklenir." />
          <div className="ms-field">
            <span className="lbl">Yedek saatleri</span>
            <div className="flex flex-wrap gap-1.5">
              {settings.backupHours.length === 0 && <span className="text-sm text-ink-3">Saat eklenmedi.</span>}
              {settings.backupHours.map((h) => (
                <span key={h} className="ms-fchip is-removable font-mono tabular-nums !cursor-default">
                  <Clock className="w-3.5 h-3.5 text-ink-3" /> {h}
                  <button type="button" aria-label={`${h} saatini kaldır`} onClick={() => set({ backupHours: settings.backupHours.filter((x) => x !== h) })} className="w-6 h-6 rounded-full inline-flex items-center justify-center text-ink-3 hover:text-bad-text hover:bg-bad-soft cursor-pointer">
                    <X />
                  </button>
                </span>
              ))}
            </div>
            <div className="flex flex-wrap items-center gap-2 pt-1">
              <input type="time" value={newHour} onChange={(e) => setNewHour(e.target.value)} aria-label="Yeni yedek saati" className="ms-input !w-[128px] font-mono" />
              <button type="button" onClick={addHour} className="ms-btn">
                <Plus /> Saat ekle
              </button>
            </div>
          </div>
          <Field label="Kapsam" className="max-w-xs">
            <select value={settings.backupScope} onChange={(e) => set({ backupScope: e.target.value as ManageAutomationSettings['backupScope'] })} className="ms-input">
              <option value="all">Tüm veriler</option>
              <option value="questions">Soru havuzu</option>
              <option value="past">Çıkmış sorular</option>
              <option value="notes">Ders notları</option>
            </select>
          </Field>
        </Panel>

        <Panel title="AI çalışma pencereleri" icon={Bot}>
          <Switch checked={settings.aiAutoRunEnabled} onChange={(v) => set({ aiAutoRunEnabled: v })} label="Zamanlanmış AI çalışması" hint="Ajanlar yalnızca bu saat aralıklarında kendiliğinden çalışır." />
          <div className="ms-field">
            <span className="lbl">Pencereler</span>
            {settings.aiWindows.length === 0 && <span className="text-sm text-ink-3">Pencere yok; AI yalnızca elle başlatılır.</span>}
            <ul className="m-0 p-0 list-none flex flex-col gap-1.5">
              {settings.aiWindows.map((w, i) => (
                <li key={i} className="flex items-center gap-2">
                  <input type="time" value={w.start} aria-label="Başlangıç" onChange={(e) => set({ aiWindows: settings.aiWindows.map((x, xi) => (xi === i ? { ...x, start: e.target.value } : x)) })} className="ms-input !w-[128px] font-mono" />
                  <ArrowRight className="w-4 h-4 text-ink-3 shrink-0" aria-hidden="true" />
                  <input type="time" value={w.end} aria-label="Bitiş" onChange={(e) => set({ aiWindows: settings.aiWindows.map((x, xi) => (xi === i ? { ...x, end: e.target.value } : x)) })} className="ms-input !w-[128px] font-mono" />
                  <button type="button" aria-label="Pencereyi sil" onClick={() => set({ aiWindows: settings.aiWindows.filter((_, xi) => xi !== i) })} className="ms-btn is-icon is-danger">
                    <Trash2 />
                  </button>
                </li>
              ))}
            </ul>
            <button type="button" onClick={() => set({ aiWindows: [...settings.aiWindows, { start: '02:00', end: '05:00' }] })} className="ms-btn self-start mt-1">
              <Plus /> Pencere ekle
            </button>
          </div>
          <Field label="Varsayılan model" className="max-w-sm">
            <select value={settings.aiModel} onChange={(e) => set({ aiModel: e.target.value })} className="ms-input">
              {MODELS.map(([v, l]) => (
                <option key={v} value={v}>{l}</option>
              ))}
            </select>
          </Field>
          <Switch checked={settings.notifyOnError} onChange={(v) => set({ notifyOnError: v })} label="Hata olursa bildir" />
        </Panel>
      </div>

      <Panel title="AI anahtarları" icon={Key} desc="Anahtarlar yalnızca bu tarayıcıda saklanır. Muse Spark, Gemini ve Groq limitleri dolunca kendiliğinden devreye girer.">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {KEY_FIELDS.map(([k, label]) => (
            <Field key={k} label={label}>
              <span className="relative flex items-center">
                <input
                  type={reveal[k] ? 'text' : 'password'}
                  autoComplete="off"
                  spellCheck={false}
                  value={keys[k]}
                  onChange={(e) => setKeys({ ...keys, [k]: e.target.value })}
                  placeholder="Yapıştır"
                  className="ms-input is-mono !pr-11"
                />
                <button type="button" onClick={() => setReveal((r) => ({ ...r, [k]: !r[k] }))} className="ms-btn is-ghost is-icon is-sm absolute right-1" aria-label={reveal[k] ? 'Anahtarı gizle' : 'Anahtarı göster'}>
                  {reveal[k] ? <EyeOff /> : <Eye />}
                </button>
              </span>
            </Field>
          ))}
        </div>
      </Panel>

      <AdminDriveSyncSettings adminEmail={adminEmail} onRefreshData={onRefreshData} selectedCommitteeId={selectedCommitteeId} />

      {dirty && (
        <div className="ms-bulkbar" role="status">
          <b>Kaydedilmemiş değişiklikler var</b>
          <button
            type="button"
            onClick={() => {
              setSettings(JSON.parse(saved));
              setKeys(JSON.parse(savedKeys));
            }}
            className="ms-btn"
          >
            Geri al
          </button>
          <button type="button" onClick={() => void save()} disabled={saving} className="ms-btn is-primary">
            <Save /> {saving ? 'Kaydediliyor…' : 'Kaydet'}
          </button>
        </div>
      )}
    </div>
  );
};
