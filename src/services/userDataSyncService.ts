/**
 * Kullanıcı Veri, İstatistik, Bildirim & Yorum Senkronizasyon Servisi
 * (User Data, Statistics, Notifications & Comments Database Sync Service)
 *
 * Kullanıcının tarayıcısında (localStorage / IndexedDB) biriken:
 * - Çözülen sorular & deneme sınavları geçmişi (medsoru_selftest_history_v1)
 * - Günlük çalışma süreleri & aktivite günlüğü (medsoru_study_seconds_v1, medsoru_activity_v1)
 * - Deste/ders adım ilerlemeleri & tekrar kuyruğu (medsoru_study_progress_v1, medsoru_study_review_v1)
 * - Flaş kart ezber durumları & favori kartlar (medsoru_flashcards_v1, medsoru_flashcard_favorites_v1)
 * - Kaydedilen sözlük maddeleri & soru favorileri (medsoru_bookmarked_encyclopedia, medsoru_study_favorites_v1)
 * - Kullanıcı içi bildirimler & bildirim izinleri (medsoru_user_notifications_v1, push/email)
 * - Not defteri (medsoru_notes_v1)
 * - Kullanıcı yorumları & katkıları
 * verilerinin sunucu veritabanına (Node.js/Express + Supabase PostgreSQL)
 * tam yedeklenmesini, kalıcı olarak saklanmasını ve cihazlar arası senkronizasyonunu sağlar.
 */

import { getCustomApiUrl } from './api';
import { getNetState } from './net';
import { getDeviceToken, getVoterId } from '../utils/voterId';
import { auth, SAVED_NAME_KEY, SAVED_STUDENT_NUMBER_KEY } from './auth';
import { replaceNotesFromSync, StudyNote } from './studyStore';

export interface UserStatsPayload {
  activityLog?: Array<{ kind: string; text: string; at: string }>;
  studySeconds?: Record<string, number>;
  selftestHistory?: unknown[];
  studyProgress?: Record<string, unknown>;
  studyReview?: unknown[];
  flashcards?: unknown;
  favorites?: unknown[];
  cardFavorites?: unknown[];
  bookmarkedEncyclopedia?: string[];
}

export interface UserNotificationItem {
  id: string;
  type: string;
  title: string;
  message: string;
  deepLinkUrl?: string;
  targetType?: string;
  targetId?: string;
  read: boolean;
  createdAt: string;
}

export interface FullUserDataBundle {
  uid: string;
  email?: string | null;
  displayName?: string | null;
  studentNumber?: string | null;
  stats: UserStatsPayload;
  notifications: UserNotificationItem[];
  notificationPrefs: {
    pushEnabled: boolean;
    emailEnabled: boolean;
  };
  notes: StudyNote[];
  /** Silinen notların mezar taşları (id → silinme zamanı); birleştirmede silinen not geri gelmesin */
  notesDeleted?: Record<string, string>;
  comments?: Array<{ questionId: string; text: string; at?: string }>;
  clientUpdatedAt: string;
  lastBackupAt?: string;
}

const LAST_BACKUP_KEY = 'medsoru_last_user_data_backup_at';
const LAST_RESTORE_KEY = 'medsoru_last_user_data_restore_at';
const NOTES_DELETED_KEY = 'medsoru_notes_deleted_v1'; // notesSync ile ortak

const readJson = <T>(key: string, fallback: T): T => {
  try {
    const raw = typeof localStorage !== 'undefined' ? localStorage.getItem(key) : null;
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
};

const writeJson = (key: string, val: unknown): void => {
  try {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(key, JSON.stringify(val));
    }
  } catch (err) {
    console.warn(`[UserDataSync] localStorage write failed for ${key}:`, err);
  }
};

/**
 * Tarayıcıdaki tüm kişisel kullanıcı verilerini tek bir paket haline getirir.
 */
export function collectLocalUserData(): FullUserDataBundle {
  const firebaseUser = auth.currentUser;
  const cachedProfile = readJson<Record<string, string>>('medsoru_user_profile_cache', {});

  const uid = firebaseUser?.uid || cachedProfile?.uid || getDeviceToken();
  const email = firebaseUser?.email || cachedProfile?.email || null;
  const displayName =
    firebaseUser?.displayName ||
    cachedProfile?.displayName ||
    (typeof localStorage !== 'undefined' ? localStorage.getItem(SAVED_NAME_KEY) : null) ||
    'Öğrenci';
  const studentNumber =
    (cachedProfile?.studentNumber as string) ||
    (typeof localStorage !== 'undefined' ? localStorage.getItem(SAVED_STUDENT_NUMBER_KEY) : null) ||
    null;

  // İstatistikler ve Çalışma Geçmişi
  const activityLog = readJson<Array<{ kind: string; text: string; at: string }>>('medsoru_activity_v1', []);
  const studySeconds = readJson<Record<string, number>>('medsoru_study_seconds_v1', {});
  const selftestHistory = readJson<unknown[]>('medsoru_selftest_history_v1', []);
  const studyProgress = readJson<Record<string, unknown>>('medsoru_study_progress_v1', {});
  const studyReview = readJson<unknown[]>('medsoru_study_review_v1', []);
  const flashcards = readJson<unknown>('medsoru_flashcards_v1', null);
  const favorites = readJson<unknown[]>('medsoru_study_favorites_v1', []);
  const cardFavorites = readJson<unknown[]>('medsoru_flashcard_favorites_v1', []);
  const bookmarkedEncyclopedia = readJson<string[]>('medsoru_bookmarked_encyclopedia', []);

  // Bildirimler & Tercihler
  const notifications = readJson<UserNotificationItem[]>('medsoru_user_notifications_v1', []);
  const pushEnabled = (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_push_notifications_enabled') : 'false') === 'true';
  const emailEnabled = (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_email_notifications_enabled') : 'false') === 'true';

  // Notlar
  const notes = readJson<StudyNote[]>('medsoru_notes_v1', []);
  const notesDeleted = readJson<Record<string, string>>(NOTES_DELETED_KEY, {});

  return {
    uid,
    email,
    displayName,
    studentNumber,
    stats: {
      activityLog,
      studySeconds,
      selftestHistory,
      studyProgress,
      studyReview,
      flashcards,
      favorites,
      cardFavorites,
      bookmarkedEncyclopedia,
    },
    notifications,
    notificationPrefs: {
      pushEnabled,
      emailEnabled,
    },
    notes,
    notesDeleted,
    clientUpdatedAt: new Date().toISOString(),
  };
}

/**
 * Sunucudan gelen (birleştirilmiş) paketi yerel veriye uygular. Hiçbir şey ezilmez:
 * listeler birleşir, sayaçlarda büyük olan, kayıtlarda yeni olan kazanır; silinen notlar geri gelmez,
 * cihazda daha yeni düzenlenmiş not korunur. Hem yedek yanıtında hem elle geri yüklemede kullanılır.
 */
export function applyBundleToLocal(bundle: FullUserDataBundle): void {
  const st = bundle?.stats || {};
  const keyOf = (x: any) => (x && typeof x === 'object' ? String(x.id ?? x.at ?? x.date ?? x.timestamp ?? JSON.stringify(x)) : String(x));
  const union = (local: any[], remote: any[], pick: (l: any, r: any) => any = (l) => l) => {
    const m = new Map<string, any>();
    for (const x of remote || []) if (x != null) m.set(keyOf(x), x);
    for (const x of local || []) {
      if (x == null) continue;
      const k = keyOf(x);
      m.set(k, m.has(k) ? pick(x, m.get(k)) : x);
    }
    return Array.from(m.values());
  };

  if (Array.isArray(st.activityLog)) {
    const k = (a: any) => `${a?.at}|${a?.kind}|${a?.text}`;
    const m = new Map<string, any>();
    for (const a of [...st.activityLog, ...readJson<any[]>('medsoru_activity_v1', [])]) if (a) m.set(k(a), a);
    writeJson('medsoru_activity_v1', Array.from(m.values()).sort((x, y) => String(x.at).localeCompare(String(y.at))).slice(-600));
  }
  if (st.studySeconds) {
    const sec = readJson<Record<string, number>>('medsoru_study_seconds_v1', {});
    for (const [day, v] of Object.entries(st.studySeconds)) sec[day] = Math.max(Number(sec[day]) || 0, Number(v) || 0);
    writeJson('medsoru_study_seconds_v1', sec);
  }
  if (Array.isArray(st.selftestHistory)) {
    writeJson(
      'medsoru_selftest_history_v1',
      union(readJson<any[]>('medsoru_selftest_history_v1', []), st.selftestHistory).sort((x, y) => String(x?.at || '').localeCompare(String(y?.at || '')))
    );
  }
  if (st.studyProgress) {
    const prog = readJson<Record<string, any>>('medsoru_study_progress_v1', {});
    for (const [id, r] of Object.entries(st.studyProgress as Record<string, any>)) {
      if (!prog[id] || String(r?.at || '') > String(prog[id]?.at || '')) prog[id] = r;
    }
    writeJson('medsoru_study_progress_v1', prog);
  }
  if (Array.isArray(st.studyReview)) writeJson('medsoru_study_review_v1', union(readJson<any[]>('medsoru_study_review_v1', []), st.studyReview));
  if (st.flashcards && typeof st.flashcards === 'object') {
    const cards = readJson<Record<string, any>>('medsoru_flashcards_v1', {});
    for (const [id, r] of Object.entries(st.flashcards as Record<string, any>)) {
      const l = cards[id];
      if (!l || (Number(r?.seen) || 0) > (Number(l?.seen) || 0)) cards[id] = r;
    }
    writeJson('medsoru_flashcards_v1', cards);
  }
  if (Array.isArray(st.favorites)) writeJson('medsoru_study_favorites_v1', union(readJson<any[]>('medsoru_study_favorites_v1', []), st.favorites).filter(Boolean));
  if (Array.isArray(st.cardFavorites)) writeJson('medsoru_flashcard_favorites_v1', union(readJson<any[]>('medsoru_flashcard_favorites_v1', []), st.cardFavorites));
  if (Array.isArray(st.bookmarkedEncyclopedia)) {
    writeJson('medsoru_bookmarked_encyclopedia', union(readJson<any[]>('medsoru_bookmarked_encyclopedia', []), st.bookmarkedEncyclopedia).filter(Boolean));
  }

  if (Array.isArray(bundle.notifications)) {
    const merged = union(readJson<UserNotificationItem[]>('medsoru_user_notifications_v1', []), bundle.notifications, (l, r) => ({ ...r, ...l, read: Boolean(l?.read || r?.read) }));
    writeJson('medsoru_user_notifications_v1', merged.sort((a, b) => String(b.createdAt || '').localeCompare(String(a.createdAt || ''))));
  }

  // Notlar: mezar taşlarıyla birleşim (silinen geri gelmez, yerelde daha yeni düzenlenen korunur)
  if (Array.isArray(bundle.notes)) {
    const deleted = { ...readJson<Record<string, string>>(NOTES_DELETED_KEY, {}) };
    for (const [id, at] of Object.entries(bundle.notesDeleted || {})) if (!deleted[id] || deleted[id] < at) deleted[id] = at;
    const byId = new Map<string, StudyNote>();
    for (const n of bundle.notes) if (n?.id) byId.set(n.id, n);
    for (const n of readJson<StudyNote[]>('medsoru_notes_v1', [])) {
      const r = byId.get(n.id);
      if (!r || n.updatedAt > r.updatedAt) byId.set(n.id, n);
    }
    for (const [id, at] of Object.entries(deleted)) {
      const n = byId.get(id);
      if (n && n.updatedAt <= at) byId.delete(id);
    }
    replaceNotesFromSync(Array.from(byId.values()).sort((a, b) => b.updatedAt.localeCompare(a.updatedAt)));
    writeJson(NOTES_DELETED_KEY, deleted);
  }

  if (bundle.displayName && typeof localStorage !== 'undefined' && !localStorage.getItem(SAVED_NAME_KEY)) {
    localStorage.setItem(SAVED_NAME_KEY, bundle.displayName);
  }
  if (bundle.studentNumber && typeof localStorage !== 'undefined' && !localStorage.getItem(SAVED_STUDENT_NUMBER_KEY)) {
    localStorage.setItem(SAVED_STUDENT_NUMBER_KEY, bundle.studentNumber);
  }
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent('medsoru:notes-synced'));
    window.dispatchEvent(new Event('storage'));
  }
}

/**
 * Yedek isteği kimliği: oturum açıksa Firebase ID jetonu (sunucu uid/e-postayı ondan alır), değilse
 * cihazın gizli jetonu (`dev-…`). Önbellekteki eski profil uid'si jetonsuz kullanılamaz; sunucu reddeder.
 */
async function backupIdentity(): Promise<{ uid: string; headers: Record<string, string> }> {
  const user = auth.currentUser;
  if (user) {
    try {
      const token = await user.getIdToken();
      return { uid: user.uid, headers: { Authorization: `Bearer ${token}`, 'x-user-id': user.uid } };
    } catch (_) {
      /* jeton alınamazsa cihaz kimliğine düş */
    }
  }
  const uid = getDeviceToken();
  return { uid, headers: { 'x-user-id': uid } };
}

/**
 * Tüm kullanıcı verilerini sunucuya ve Supabase veritabanına aktarıp yedekler.
 */
export async function backupUserDataToDatabase(): Promise<{
  success: boolean;
  message?: string;
  backedUpAt?: string;
  summary?: Record<string, number>;
  error?: string;
}> {
  if (getNetState() === 'offline') {
    return { success: false, error: 'Çevrimdışısınız. Bağlantı kurulduğunda otomatik eşitlenecektir.' };
  }

  const base = (getCustomApiUrl() || '').replace(/\/$/, '');

  try {
    const who = await backupIdentity();
    const payload = { ...collectLocalUserData(), uid: who.uid };
    const res = await fetch(`${base}/api/user-data/backup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...who.headers },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errJson = await res.json().catch(() => ({}));
      throw new Error(errJson.error || `Sunucu hatası: HTTP ${res.status}`);
    }

    const data = await res.json();
    const nowIso = data.backedUpAt || new Date().toISOString();
    // Sunucu birleştirdi: diğer cihazlardan gelenleri de buraya uygula (cihazlar yakınsar)
    if (data?.data) {
      try {
        applyBundleToLocal(data.data);
        lastBackedUpFingerprint = fingerprint();
      } catch (e) {
        console.warn('[UserDataSync] Birleştirilmiş paket uygulanamadı:', e);
      }
    }

    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(LAST_BACKUP_KEY, nowIso);
    }

    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('medsoru:user-data-synced', { detail: { backedUpAt: nowIso } }));
    }

    return {
      success: true,
      message: data.message || 'Tüm veriler veritabanına başarıyla kaydedildi.',
      backedUpAt: nowIso,
      summary: data.summary,
    };
  } catch (err: any) {
    console.error('[UserDataSync] Backup failed:', err);
    return { success: false, error: err.message || 'Veritabanı yedekleme hatası' };
  }
}

/**
 * Veritabanındaki yedeği çeker ve yerel depolama ile birleştirir (Restore).
 */
export async function restoreUserDataFromDatabase(): Promise<{
  success: boolean;
  message?: string;
  restoredAt?: string;
  error?: string;
}> {
  if (getNetState() === 'offline') {
    return { success: false, error: 'Çevrimdışısınız. Bağlantı kurulduğunda yeniden deneyin.' };
  }

  const base = (getCustomApiUrl() || '').replace(/\/$/, '');

  try {
    const who = await backupIdentity();
    const query = new URLSearchParams({ uid: who.uid });
    const res = await fetch(`${base}/api/user-data/backup?${query.toString()}`, {
      headers: who.headers,
    });

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    const json = await res.json();
    if (!json.success || !json.found || !json.data) {
      return { success: false, error: json.message || 'Veritabanında kayıtlı kullanıcı yedeği bulunamadı.' };
    }

    const bundle: FullUserDataBundle = json.data;
    applyBundleToLocal(bundle);

    const nowIso = new Date().toISOString();
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(LAST_RESTORE_KEY, nowIso);
    }

    // Olayları tetikle ki UI anında güncellensin
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('medsoru:user-data-restored', { detail: { bundle } }));
      window.dispatchEvent(new CustomEvent('medsoru:notes-synced'));
      window.dispatchEvent(new Event('storage'));
    }

    return {
      success: true,
      message: 'Tüm kullanıcı verileri veritabanından başarıyla yüklendi ve birleştirildi.',
      restoredAt: nowIso,
    };
  } catch (err: any) {
    console.error('[UserDataSync] Restore failed:', err);
    return { success: false, error: err.message || 'Veritabanı geri yükleme hatası' };
  }
}

/**
 * Son yedekleme zamanını döndürür.
 */
export function getLastBackupTime(): string {
  try {
    return (typeof localStorage !== 'undefined' && localStorage.getItem(LAST_BACKUP_KEY)) || '';
  } catch {
    return '';
  }
}

/** Yerel verinin parmak izi (zaman damgası hariç): değişmediyse otomatik yedek gönderilmez. */
let lastBackedUpFingerprint = '';
function fingerprint(): string {
  try {
    const { clientUpdatedAt: _t, ...rest } = collectLocalUserData();
    const str = JSON.stringify(rest);
    let h = 0;
    for (let i = 0; i < str.length; i++) h = (Math.imul(31, h) + str.charCodeAt(i)) | 0;
    return `${str.length}:${h}`;
  } catch {
    return '';
  }
}

let autoBackupRunning = false;
async function autoBackupIfChanged(): Promise<void> {
  if (autoBackupRunning || getNetState() === 'offline') return;
  const fp = fingerprint();
  if (!fp || fp === lastBackedUpFingerprint) return;
  autoBackupRunning = true;
  try {
    const r = await backupUserDataToDatabase();
    if (r.success) lastBackedUpFingerprint = fingerprint();
  } finally {
    autoBackupRunning = false;
  }
}

/**
 * Kullanıcı verileri değiştiğinde sessiz arka plan yedekleme zamanlayıcısı.
 */
let autoBackupTimer: number | undefined;

export function triggerAutoBackup(): void {
  if (typeof window === 'undefined') return;
  if (autoBackupTimer) clearTimeout(autoBackupTimer);

  autoBackupTimer = window.setTimeout(() => {
    void autoBackupIfChanged();
  }, 10_000); // 10 saniye boşta bekleme sonrası sessiz yedekleme
}

let autoInstalled = false;
/**
 * İstatistik ve notların sürekli yedeklenmesi: sekme arka plana geçince ve açıkken 15 dk'da bir, yalnız veri
 * değiştiyse. Sunucu birleştirdiği için sık yedek veri kaybettirmez; yanıt diğer cihazların verisini de getirir.
 */
export function installUserDataAutoBackup(): void {
  if (autoInstalled || typeof window === 'undefined') return;
  autoInstalled = true;
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') void autoBackupIfChanged();
  });
  window.setInterval(() => {
    if (document.visibilityState === 'visible') void autoBackupIfChanged();
  }, 15 * 60 * 1000);
}
