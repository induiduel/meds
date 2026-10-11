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
  comments?: Array<{ questionId: string; text: string; at?: string }>;
  clientUpdatedAt: string;
  lastBackupAt?: string;
}

const LAST_BACKUP_KEY = 'medsoru_last_user_data_backup_at';
const LAST_RESTORE_KEY = 'medsoru_last_user_data_restore_at';

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
    clientUpdatedAt: new Date().toISOString(),
  };
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

  const payload = collectLocalUserData();
  const base = (getCustomApiUrl() || '').replace(/\/$/, '');

  try {
    const res = await fetch(`${base}/api/user-data/backup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-user-id': payload.uid,
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errJson = await res.json().catch(() => ({}));
      throw new Error(errJson.error || `Sunucu hatası: HTTP ${res.status}`);
    }

    const data = await res.json();
    const nowIso = data.backedUpAt || new Date().toISOString();

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

  const firebaseUser = auth.currentUser;
  const uid = firebaseUser?.uid || getDeviceToken();
  const email = firebaseUser?.email || '';
  const base = (getCustomApiUrl() || '').replace(/\/$/, '');

  try {
    const query = new URLSearchParams({ uid });
    if (email) query.set('email', email);

    const res = await fetch(`${base}/api/user-data/backup?${query.toString()}`, {
      headers: { 'x-user-id': uid },
    });

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    const json = await res.json();
    if (!json.success || !json.found || !json.data) {
      return { success: false, error: json.message || 'Veritabanında kayıtlı kullanıcı yedeği bulunamadı.' };
    }

    const bundle: FullUserDataBundle = json.data;

    // 1. İstatistikleri ve Çalışma Sürelerini Birleştir
    if (bundle.stats) {
      // Aktivite günlüğü (birleştir ve tarihe göre sırala)
      if (Array.isArray(bundle.stats.activityLog)) {
        const localAct = readJson<Array<{ kind: string; text: string; at: string }>>('medsoru_activity_v1', []);
        const actMap = new Map<string, { kind: string; text: string; at: string }>();
        bundle.stats.activityLog.forEach((a) => {
          const k = `${a.at}_${a.text}`;
          actMap.set(k, a);
        });
        localAct.forEach((a) => {
          const k = `${a.at}_${a.text}`;
          actMap.set(k, a);
        });
        const mergedAct = Array.from(actMap.values())
          .sort((x, y) => x.at.localeCompare(y.at))
          .slice(-600);
        writeJson('medsoru_activity_v1', mergedAct);
      }

      // Çalışma süreleri (en yüksek olanı koru)
      if (bundle.stats.studySeconds) {
        const localSec = readJson<Record<string, number>>('medsoru_study_seconds_v1', {});
        const mergedSec: Record<string, number> = { ...localSec };
        for (const [day, sec] of Object.entries(bundle.stats.studySeconds)) {
          mergedSec[day] = Math.max(Number(mergedSec[day]) || 0, Number(sec) || 0);
        }
        writeJson('medsoru_study_seconds_v1', mergedSec);
      }

      // Deneme sınavı geçmişi
      if (Array.isArray(bundle.stats.selftestHistory)) {
        const localTests = readJson<any[]>('medsoru_selftest_history_v1', []);
        const testMap = new Map<string, any>();
        bundle.stats.selftestHistory.forEach((rawT) => {
          const t = rawT as Record<string, any>;
          if (t && (t.id || t.date || t.timestamp)) {
            testMap.set(String(t.id || t.date || t.timestamp), t);
          }
        });
        localTests.forEach((t) => {
          if (t && (t.id || t.date || t.timestamp)) {
            testMap.set(String(t.id || t.date || t.timestamp), t);
          }
        });
        writeJson('medsoru_selftest_history_v1', Array.from(testMap.values()));
      }

      // Deste ilerlemeleri
      if (bundle.stats.studyProgress) {
        const localProg = readJson<Record<string, any>>('medsoru_study_progress_v1', {});
        const mergedProg = { ...bundle.stats.studyProgress, ...localProg };
        writeJson('medsoru_study_progress_v1', mergedProg);
      }

      // Flaş kartlar
      if (bundle.stats.flashcards) {
        writeJson('medsoru_flashcards_v1', bundle.stats.flashcards);
      }

      // Favoriler
      if (Array.isArray(bundle.stats.favorites)) {
        const localFav = new Set(readJson<string[]>('medsoru_study_favorites_v1', []));
        bundle.stats.favorites.forEach((f: any) => localFav.add(typeof f === 'string' ? f : f?.id));
        writeJson('medsoru_study_favorites_v1', Array.from(localFav).filter(Boolean));
      }

      // Sözlük imleri
      if (Array.isArray(bundle.stats.bookmarkedEncyclopedia)) {
        const localBmk = new Set(readJson<string[]>('medsoru_bookmarked_encyclopedia', []));
        bundle.stats.bookmarkedEncyclopedia.forEach((id) => localBmk.add(id));
        writeJson('medsoru_bookmarked_encyclopedia', Array.from(localBmk).filter(Boolean));
      }
    }

    // 2. Bildirimleri Birleştir
    if (Array.isArray(bundle.notifications)) {
      const localNotifs = readJson<UserNotificationItem[]>('medsoru_user_notifications_v1', []);
      const notifMap = new Map<string, UserNotificationItem>();
      bundle.notifications.forEach((n) => {
        if (n && n.id) notifMap.set(n.id, n);
      });
      localNotifs.forEach((n) => {
        if (n && n.id) notifMap.set(n.id, n);
      });
      const mergedNotifs = Array.from(notifMap.values()).sort((a, b) => b.createdAt.localeCompare(a.createdAt));
      writeJson('medsoru_user_notifications_v1', mergedNotifs);
    }

    // 3. Notları Birleştir
    if (Array.isArray(bundle.notes) && bundle.notes.length > 0) {
      replaceNotesFromSync(bundle.notes);
    }

    // 4. Profil Bilgilerini Güncelle (eğer yerelde eksikse)
    if (bundle.displayName && typeof localStorage !== 'undefined' && !localStorage.getItem(SAVED_NAME_KEY)) {
      localStorage.setItem(SAVED_NAME_KEY, bundle.displayName);
    }
    if (bundle.studentNumber && typeof localStorage !== 'undefined' && !localStorage.getItem(SAVED_STUDENT_NUMBER_KEY)) {
      localStorage.setItem(SAVED_STUDENT_NUMBER_KEY, bundle.studentNumber);
    }

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

/**
 * Kullanıcı verileri değiştiğinde sessiz arka plan yedekleme zamanlayıcısı.
 */
let autoBackupTimer: number | undefined;

export function triggerAutoBackup(): void {
  if (typeof window === 'undefined') return;
  if (autoBackupTimer) clearTimeout(autoBackupTimer);

  autoBackupTimer = window.setTimeout(() => {
    backupUserDataToDatabase().catch(() => {});
  }, 10_000); // 10 saniye boşta bekleme sonrası sessiz yedekleme
}
