/**
 * Yönetim konsolu otomasyon ayarları (yedekleme saatleri, AI anahtarları,
 * AI otomatik çalışma pencereleri). Önce yerel sunucuya yazmayı dener,
 * sunucu yoksa (statik barındırma) yalnızca tarayıcıda saklar.
 */
import { safeJsonFetch } from './api';

const STORAGE_KEY = 'medsoru_manage_automation_v1';

export interface AiRunWindow {
  start: string; // "HH:MM"
  end: string; // "HH:MM"
}

export interface ManageAutomationSettings {
  backupEnabled: boolean;
  backupHours: string[]; // ["03:00", ...]
  backupScope: 'all' | 'questions' | 'past' | 'notes';
  aiAutoRunEnabled: boolean;
  aiWindows: AiRunWindow[];
  aiModel: string;
  notifyOnError: boolean;
  updatedAt?: string;
}

export const DEFAULT_MANAGE_SETTINGS: ManageAutomationSettings = {
  backupEnabled: true,
  backupHours: ['03:00'],
  backupScope: 'all',
  aiAutoRunEnabled: false,
  aiWindows: [{ start: '02:00', end: '05:00' }],
  aiModel: 'gemini-3.8-flash',
  notifyOnError: true,
};

const GEMINI_KEY = 'medsoru_gemini_api_key';
const GROQ_KEY = 'medsoru_groq_api_key';
const GROQ_KEY_2 = 'medsoru_groq_api_key_2';
const MUSE_SPARK_KEY = 'medsoru_muse_spark_api_key';

const readLS = (k: string): string => {
  try {
    return localStorage.getItem(k) || '';
  } catch {
    return '';
  }
};

const writeLS = (k: string, v: string) => {
  try {
    if (v) localStorage.setItem(k, v);
    else localStorage.removeItem(k);
  } catch {
    /* yoksay */
  }
};

export const getAiKeys = (): { gemini: string; groq: string; groq2: string; museSpark: string } => ({
  gemini: readLS(GEMINI_KEY),
  groq: readLS(GROQ_KEY),
  groq2: readLS(GROQ_KEY_2),
  museSpark: readLS(MUSE_SPARK_KEY),
});

export const saveAiKeys = (keys: { gemini: string; groq: string; groq2: string; museSpark?: string }) => {
  writeLS(GEMINI_KEY, keys.gemini.trim());
  writeLS(GROQ_KEY, keys.groq.trim());
  writeLS(GROQ_KEY_2, keys.groq2.trim());
  if (keys.museSpark !== undefined) {
    writeLS(MUSE_SPARK_KEY, keys.museSpark.trim());
  }
};

export const loadManageSettings = async (): Promise<ManageAutomationSettings> => {
  let local: ManageAutomationSettings = { ...DEFAULT_MANAGE_SETTINGS };
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) local = { ...DEFAULT_MANAGE_SETTINGS, ...JSON.parse(raw) };
  } catch {
    /* yoksay */
  }
  try {
    const res = await safeJsonFetch<{ success: boolean; settings?: ManageAutomationSettings }>(
      '/api/admin/manage-settings'
    );
    if (res.ok && res.data?.settings) {
      const merged = { ...local, ...res.data.settings };
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(merged));
      } catch {
        /* yoksay */
      }
      return merged;
    }
  } catch {
    /* statik barındırmada sunucu olmayabilir */
  }
  return local;
};

export const saveManageSettings = async (
  adminEmail: string,
  settings: ManageAutomationSettings
): Promise<{ savedLocal: boolean; savedServer: boolean; message: string }> => {
  const payload = { ...settings, updatedAt: new Date().toISOString() };
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  } catch {
    /* yoksay */
  }
  try {
    const res = await safeJsonFetch<{ success: boolean }>( '/api/admin/manage-settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
      body: JSON.stringify(payload),
    });
    if (res.ok) return { savedLocal: true, savedServer: true, message: 'Ayarlar tarayıcıya ve sunucuya kaydedildi.' };
  } catch {
    /* yoksay */
  }
  return { savedLocal: true, savedServer: false, message: 'Sunucuya ulaşılamadı; ayarlar yalnızca bu tarayıcıda saklandı.' };
};

export const reportManageLog = async (entry: { level: string; source: string; message: string }) => {
  try {
    await safeJsonFetch('/api/admin/console-logs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...entry, ts: new Date().toISOString() }),
    });
  } catch {
    /* en iyi çaba */
  }
};
