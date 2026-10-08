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
import { Panel, Switch, Field } from './consoleUi';

/**
 * Otomasyon: yedek saatleri, AI çalışma pencereleri, AI anahtarları ve Drive eşitlemesi.
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

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-3 items-start">
        <Panel
          title="Yedekleme"
          icon={DatabaseBackup}
          tools={
            <button type="button" onClick={() => void backupNow()} disabled={backingUp} className="ms-btn is-sm">
              <DatabaseBackup /> {backingUp ? 'Yedekleniyor…' : 'Şimdi yedekle'}
            </button>
          }
        >
          <Switch checked={settings.backupEnabled} onChange={(v) => set({ backupEnabled: v })} label="Otomatik yedekleme" hint="Aşağıdaki saatlerde seçili kapsam yedeklenir." />
          <div className="ms-field">
            <span className="lbl">Yedek saatleri</span>
            <div className="flex flex-wrap gap-1.5">
              {settings.backupHours.length === 0 && <span className="text-[13px] text-ink-3">Saat eklenmedi.</span>}
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
            {settings.aiWindows.length === 0 && <span className="text-[13px] text-ink-3">Pencere yok; AI yalnızca elle başlatılır.</span>}
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
