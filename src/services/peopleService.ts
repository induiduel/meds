/**
 * Yönetim › Kişiler istemcisi. Uçlar kişisel veri döndürdüğü için başlıktaki e-postaya güvenmez:
 * canlı sitede Firebase yönetici jetonu, yerel panelde yerel sunucu (loopback) kullanılır. Yerel panel Oracle'a
 * bağlıyken yerel sunucu isteği gizli panel anahtarıyla Oracle'a iletir (x-panel-target: oracle).
 */
import { auth } from './auth';
import { getCustomApiUrl } from './api';
import { PANEL_ON_ORACLE_AT_BOOT, getStoredPanelSecret } from '../config/deployment';

export type PersonKind = 'account' | 'guest';
/** insan: gerçek kişi; bot: arama motoru vb.; otomasyon: bizim tarama/sınama araçlarımız; bos: cihazı/etkinliği olmayan yedek */
export type AgentKind = 'insan' | 'bot' | 'otomasyon' | 'bos';
export interface GuestDevice { platform: string; browser: string; userAgent: string; firstSeen: string | null; sessions: number; lastPath: string }
export interface PersonRow {
  key: string;
  kind: PersonKind;
  agent: AgentKind;
  agentNote: string;
  /** yalnız hesaba bağlanmamış cihaz satırlarında */
  device?: GuestDevice | null;
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
  /** Konu bazlı çalışma takibi özeti (profil yedeği yoksa null) */
  study?: StudySummary | null;
  accuracy: number | null;
  testCount: number;
  counts: { comment: number; report: number; question: number; fragment: number; option: number; like: number; note: number; events: number };
}
export interface StudySummary {
  sn: number;
  haftaSn: number;
  konu: number;
  bitti: number;
  soru: number;
  modul: Record<string, number>;
  son: string | null;
}
export type StudyModule = 'sesli' | 'ogren' | 'cozucu' | 'onem';
export interface StudyTopic {
  id: string;
  modul: StudyModule | 'diger';
  konu: string;
  sn: number;
  soru: number;
  durum: 'bitti' | 'tekrar' | 'acik' | null;
  tur: number;
  ilkAt: string | null;
  sonAt: string | null;
  bittiAt: string | null;
  adm: string | null;
}
export interface StudyDetail {
  ozet: StudySummary;
  konular: StudyTopic[];
  gunluk: ({ day: string; toplam: number } & Partial<Record<StudyModule, number>>)[];
  /** sayfa ziyaretleri: p yol, t başlık, g giriş (ms), c son (ms), s etkin sn, k kaydırma % */
  ziyaret: { p: string; t: string; g: number; c: number; s: number; k: number }[];
  /** sayfa başına son konum: at (ms), t başlık, s toplam sn, n ziyaret, k kaydırma % */
  konum: { p: string; at: number; t: string; s: number; n: number; k: number }[];
  son: string | null;
  kvAt: string | null;
  /** 60 planı sınav senaryosu (profil kv medsoru_sinav_senaryo_v1) */
  senaryo?: {
    g: Record<string, { a: number; b: number; salla: number; isabet: number }>;
    s: null | {
      kaynak: 'simdi' | 'plan'; kendi: number; at?: string;
      kotu: SenaryoSonuc; mantik: SenaryoSonuc; iyi: SenaryoSonuc;
    };
    at: string | null;
  } | null;
  planSaat?: number | null;
}
export interface SenaryoSonuc { ort: number; alt: number; ust: number; p60: number; satir: { brans: string; ad: string; n: number; d: number; puan: number }[] }
export interface StudyEditOp {
  id: string;
  durum?: 'bitti' | 'acik' | 'tekrar' | null;
  sn?: number;
  soru?: number;
  sifirla?: boolean;
}

export interface PeopleList {
  people: PersonRow[];
  totals: { people: number; accounts: number; guests?: number; machines?: number; online: number; devices: number; weekSeconds: number; openReports: number };
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
  user_agent?: string;
  agent?: AgentKind;
  note?: string;
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
  calisma?: StudyDetail;
  study: { progress: number; review: number; favorites: number; flashcards: number; kvCount: number };
  activityLog: { kind: string; text: string; at: string }[];
  events: PersonEvent[];
  items: PersonItem[];
  notifications: { id: string; title: string; message: string; createdAt: string; read?: boolean; deepLinkUrl?: string; targetId?: string }[];
  at: string;
}

/** Güçlü yönetici yetkili uçlar (Kişiler, Veritabanı gezgini) için ortak çağrı */
export async function adminCall<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set('Accept', 'application/json');
  if (init.body) headers.set('Content-Type', 'application/json');
  if (PANEL_ON_ORACLE_AT_BOOT) headers.set('x-panel-target', 'oracle');
  const secret = getStoredPanelSecret();
  if (secret && !headers.has('x-panel-secret')) {
    headers.set('x-panel-secret', secret);
  }
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

export const loadPeople = () => adminCall<PeopleList>('/api/admin/people');
export const loadPerson = (key: string) => adminCall<PersonDetail>(`/api/admin/people/${encodeURIComponent(key)}`);
export const forgetDevice = (deviceId: string) => adminCall<{ success: boolean }>(`/api/admin/people/devices/${encodeURIComponent(deviceId)}`, { method: 'DELETE' });
export const deletePersonEvent = (id: number) => adminCall<{ success: boolean }>(`/api/admin/people/events/${id}`, { method: 'DELETE' });

export const editPersonStudy = (key: string, body: { ops?: StudyEditOp[]; hepsiniSifirla?: boolean }) =>
  adminCall<{ success: boolean; changed: number }>(`/api/admin/people/${encodeURIComponent(key)}/calisma`, { method: 'PATCH', body: JSON.stringify(body) });

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

/** Ders ilerlemesi: tüm kişilerin konu kayıtları (çalışma takibi) */
export interface StudyMatrixPerson {
  key: string; kind: string; ad: string; email: string | null;
  ozet: { sn: number; haftaSn: number; konu: number; bitti: number; soru: number; son: string | null };
  konular: Record<string, { sn: number; soru: number; durum: string | null; sonAt: string | null; bittiAt: string | null }>;
}
export const loadStudyMatrix = () => adminCall<{ at: string; kisiler: StudyMatrixPerson[] }>('/api/admin/people/calisma-matris');

/** Hesap birleştirme: ikinci hesap sıralamadan çıkar, istenirse çalışma takibi asıl hesaba aktarılır */
export interface MergeInfo {
  uid: string | null; kind: string;
  bag: { uid: string; key: string | null; ad: string } | null;
  adaylar: { key: string; ad: string; email: string | null }[];
  onizleme: { eklenen: number; artan: number; durumFarki: number; kaynakKonu: number; hedefKonu: number } | null;
}
export const loadMergeInfo = (key: string, hedef?: string) =>
  adminCall<MergeInfo>(`/api/admin/people/${encodeURIComponent(key)}/birlestir${hedef ? `?hedef=${encodeURIComponent(hedef)}` : ''}`);
export const mergeAccount = (key: string, body: { hedef?: string; calismaAktar?: boolean; geriAl?: boolean }) =>
  adminCall<{ success: boolean; aktarim: { eklenen: number; artan: number } | null }>(`/api/admin/people/${encodeURIComponent(key)}/birlestir`, { method: 'POST', body: JSON.stringify(body) });
