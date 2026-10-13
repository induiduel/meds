/**
 * Yönetim › Kişiler istemcisi. Uçlar kişisel veri döndürdüğü için başlıktaki e-postaya güvenmez:
 * canlı sitede Firebase yönetici jetonu, yerel panelde yerel sunucu (loopback) kullanılır. Yerel panel Oracle'a
 * bağlıyken yerel sunucu isteği gizli panel anahtarıyla Oracle'a iletir (x-panel-target: oracle).
 */
import { auth } from './auth';
import { getCustomApiUrl } from './api';
import { PANEL_ON_ORACLE_AT_BOOT } from '../config/deployment';

export type PersonKind = 'account' | 'guest';
export interface PersonRow {
  key: string;
  kind: PersonKind;
  uid: string | null;
  email: string | null;
  name: string;
  studentNumber: string | null;
  phone: string | null;
  role: string;
  photoURL: string | null;
  createdAt: string | null;
  lastSeen: string | null;
  online: boolean;
  deviceCount: number;
  deviceNames: string[];
  totalSeconds: number;
  weekSeconds: number;
  accuracy: number | null;
  testCount: number;
  counts: { comment: number; report: number; question: number; fragment: number; option: number; like: number; note: number; events: number };
}
export interface PeopleList {
  people: PersonRow[];
  totals: { people: number; accounts: number; online: number; devices: number; weekSeconds: number; openReports: number };
  database: boolean;
  at: string;
}
export interface PersonDevice {
  device_id: string;
  label: string;
  platform: string;
  browser: string;
  model: string;
  first_seen: string;
  last_seen: string;
  active_seconds: number;
  sessions: number;
  last_path: string;
  verified: boolean;
  online: boolean;
}
export interface PersonItem {
  kind: 'comment' | 'report' | 'question' | 'fragment' | 'option' | 'like' | 'vote' | 'note';
  action?: string;
  id: string;
  questionId?: string;
  source: 'past' | 'pool' | 'learn' | 'ornek' | 'notebook';
  title: string;
  body?: string;
  at: string | null;
  status?: string;
  link?: string;
  weak?: boolean;
  messageId?: string;
  deckId?: string;
}
export interface PersonEvent {
  id: number;
  kind: string;
  action: string;
  ref: string | null;
  label: string;
  body: string;
  link: string;
  device_id: string | null;
  at: string;
}
export interface PersonTest {
  id: string | null;
  at: string | null;
  title: string;
  total: number;
  correct: number;
  wrong: number;
  blank: number;
  durationSec: number;
  byDiscipline: Record<string, { total: number; correct: number }>;
}
export interface PersonDetail {
  person: {
    key: string;
    kind: PersonKind;
    uid: string | null;
    email: string | null;
    name: string;
    studentNumber: string | null;
    phone: string | null;
    role: string;
    photoURL: string | null;
    createdAt: string | null;
    lastLoginAt: string | null;
    lastBackupAt: string | null;
    verified: boolean;
  };
  devices: PersonDevice[];
  usage: { totalSeconds: number; studySeconds: number; daily: { day: string; seconds: number }[]; studyDaily: { day: string; seconds: number }[]; sessions: number };
  score: { tests: PersonTest[]; testCount: number; correct: number; wrong: number; total: number; net: number; accuracy: number | null; answeredAccuracy: number | null };
  study: { progress: number; review: number; favorites: number; flashcards: number; kvCount: number };
  activityLog: { kind: string; text: string; at: string }[];
  events: PersonEvent[];
  items: PersonItem[];
  notifications: { id: string; title: string; message: string; createdAt: string; read?: boolean; deepLinkUrl?: string; targetId?: string }[];
  at: string;
}

async function call<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set('Accept', 'application/json');
  if (init.body) headers.set('Content-Type', 'application/json');
  if (PANEL_ON_ORACLE_AT_BOOT) headers.set('x-panel-target', 'oracle');
  const user = auth.currentUser;
  if (user) {
    try {
      headers.set('Authorization', `Bearer ${await user.getIdToken()}`);
    } catch {
      /* jetonsuz: yerelde loopback yeterli */
    }
  }
  const base = (getCustomApiUrl(path) || '').replace(/\/$/, '');
  const res = await fetch(`${base}${path}`, { ...init, headers, cache: 'no-store' });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.error || `Sunucu hatası (HTTP ${res.status})`);
  return data as T;
}

export const loadPeople = () => call<PeopleList>('/api/admin/people');
export const loadPerson = (key: string) => call<PersonDetail>(`/api/admin/people/${encodeURIComponent(key)}`);
export const forgetDevice = (deviceId: string) => call<{ success: boolean }>(`/api/admin/people/devices/${encodeURIComponent(deviceId)}`, { method: 'DELETE' });
export const deletePersonEvent = (id: number) => call<{ success: boolean }>(`/api/admin/people/events/${id}`, { method: 'DELETE' });

/** Panelde kişinin derin bağlantısı (kopyalanabilir, yeni sekmede açılır) */
export const personDeepLink = (key: string, tab?: string) =>
  `${window.location.origin}/manage/kisiler/${encodeURIComponent(key)}${tab ? `?sekme=${encodeURIComponent(tab)}` : ''}`;

/** Sitedeki yol (/cikmis/… gibi) → tam adres; yerel panel Oracle'a bağlıysa canlı site adresi */
export const siteLink = (path?: string) => {
  if (!path) return '';
  if (/^https?:/i.test(path)) return path;
  const origin = PANEL_ON_ORACLE_AT_BOOT ? 'https://nofrostlife.com.tr' : window.location.origin;
  return `${origin}${path.startsWith('/') ? '' : '/'}${path}`;
};

export const fmtDuration = (sec: number) => {
  const s = Math.max(0, Math.round(sec || 0));
  if (s < 60) return `${s} sn`;
  const m = Math.round(s / 60);
  if (m < 60) return `${m} dk`;
  const h = Math.floor(m / 60);
  const r = m % 60;
  return r ? `${h} sa ${r} dk` : `${h} sa`;
};

export const relTime = (iso?: string | null) => {
  if (!iso) return '—';
  const t = new Date(iso).getTime();
  if (!Number.isFinite(t)) return '—';
  const d = (Date.now() - t) / 1000;
  if (d < 90) return 'şimdi';
  if (d < 3600) return `${Math.round(d / 60)} dk önce`;
  if (d < 86400) return `${Math.round(d / 3600)} sa önce`;
  if (d < 86400 * 7) return `${Math.round(d / 86400)} gün önce`;
  return new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', year: 'numeric' });
};
