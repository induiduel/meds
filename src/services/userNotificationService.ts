/**
 * Kullanıcı Bildirim ve AI Kuyruk Takip Servisi (User Notification & AI Queue Service)
 *
 * Kullanıcıların soruları, katkıları, yorumları ve AI geliştirme istekleri hakkındaki
 * tüm güncellemeleri yönetir.
 *
 * Bildirim geçmişi profile kayıtlıdır (userDataSyncService): uygulama içi her toast (kısa onaylar hariç) okunmuş
 * olarak, sunucunun öğrenciye yazdığı olaylar (raporun çözüldü, yorumuna yanıt…) okunmamış olarak gelir.
 * Silme/temizleme mezar taşıyla tüm cihazlara geçer.
 *
 * Deep Linking ile tam uyumludur: Her bildirimin tıklandığında hedef elemana
 * odaklanan bir deepLinkUrl'i vardır.
 */
import { setToastRecorder, toast, type ToastKind } from '../components/ui/Toast';

import { openDeepLink } from './universalRedirectService';

export interface UserNotification {
  id: string;
  userId?: string;
  userEmail?: string;
  type:
    | 'ai_reconstruction_complete'
    | 'ai_queued'
    | 'comment_added'
    | 'contribution_added'
    | 'report_filed'
    | 'report_resolved'
    | 'question_revised'
    | 'comment_deleted'
    | 'app_success'
    | 'app_info'
    | 'app_error';
  title: string;
  message: string;
  deepLinkUrl: string;
  targetType: 'pool_question' | 'past_question' | 'term' | 'flashcard' | 'app';
  targetId: string;
  read: boolean;
  createdAt: string;
  /** 'server': sunucunun öğrenciye yazdığı olay */
  source?: string;
}

const MAX_ITEMS = 300;
/** Geçmişe yazılmayan kısa onaylar (kopyalandı vb.) */
// Geçmişe yazılmayan anlık mesajlar: kopyalama/onay, çevrimdışı kuyruğun "sıraya alındı"/"Gönderildi"
// adımları (sunucu yeniden başlarken her işlem için ayrı satır biriktiriyordu) ve kendi işlemini doğrulayan iletiler.
const TRIVIAL_TOAST = /kopyaland|^bağlantı$|^tamam$|^bağlantı yok|^gönderildi$|olarak işaretlendi|^anlık bildirim açık$/i;

const STORAGE_KEY = 'medsoru_user_notifications_v1';
const PUSH_PERM_KEY = 'medsoru_push_notifications_enabled';
const EMAIL_PERM_KEY = 'medsoru_email_notifications_enabled';
const DELETED_KEY = 'medsoru_user_notifications_deleted_v1'; // userDataSyncService ile ortak

class UserNotificationService {
  private notifications: UserNotification[] = [];
  private listeners: Set<(notifs: UserNotification[]) => void> = new Set();

  constructor() {
    this.loadFromStorage();
    if (typeof window !== 'undefined') {
      // Başka sekmede okundu/silindi işaretlenirse bu sekme de güncellenir.
      window.addEventListener('storage', (e) => {
        if (e.key !== STORAGE_KEY) return;
        this.loadFromStorage();
        this.notifyListeners();
      });
      // Profil eşitlemesi (diğer cihaz / sunucu) bildirim getirdiyse: listeyi tazele, yeni okunmamışları duyur
      window.addEventListener('medsoru:user-data-applied', () => this.reloadFromSync());
      setToastRecorder((kind, title, message) => this.recordToast(kind, title, message));
    }
  }

  private reloadFromSync() {
    const before = new Set(this.notifications.map((n) => n.id));
    this.loadFromStorage();
    const fresh = this.notifications.filter(
      (n) => !before.has(n.id) && !n.read && Date.now() - new Date(n.createdAt).getTime() < 15 * 60_000
    );
    this.notifyListeners();
    for (const n of fresh.slice(0, 3)) {
      toast.show(n.type === 'app_error' ? 'error' : 'info', n.title.replace(/^✓\s*/, ''), n.message);
      this.triggerSystemPush(n);
    }
  }

  /** Uygulama içi toast'ı geçmişe yazar (görüldüğü için okunmuş; anlık tarayıcı bildirimi yok). */
  private recordToast(kind: ToastKind, title: string, message?: string) {
    if (!title || TRIVIAL_TOAST.test(title)) return;
    this.addNotification(
      {
        type: kind === 'error' ? 'app_error' : kind === 'success' ? 'app_success' : 'app_info',
        title,
        message: message || '',
        deepLinkUrl: '',
        targetType: 'app',
        targetId: typeof window !== 'undefined' ? window.location.pathname : '',
      },
      { read: true, silent: true }
    );
  }

  private tombstone(ids: string[], clearedAt?: string) {
    try {
      const raw = localStorage.getItem(DELETED_KEY);
      const t = (raw ? JSON.parse(raw) : {}) as { ids?: Record<string, string>; clearedAt?: string };
      const now = new Date().toISOString();
      const map = { ...(t.ids || {}) };
      for (const id of ids) map[id] = now;
      localStorage.setItem(DELETED_KEY, JSON.stringify({ ids: map, clearedAt: clearedAt || t.clearedAt || '' }));
    } catch {
      /* yoksay */
    }
  }

  private loadFromStorage() {
    try {
      if (typeof window !== 'undefined') {
        const raw = localStorage.getItem(STORAGE_KEY);
        const list = raw ? JSON.parse(raw) : [];
        // Bozuk kayıtlar (eksik alan) listeyi kırmasın.
        this.notifications = Array.isArray(list)
          ? list.filter((n) => n && typeof n.id === 'string' && typeof n.title === 'string')
          : [];
      }
    } catch (e) {
      console.error('Bildirimler yüklenirken hata:', e);
    }
  }

  private saveToStorage() {
    try {
      if (typeof window !== 'undefined') {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.notifications.slice(0, MAX_ITEMS)));
      }
    } catch (e) {
      console.error('Bildirimler kaydedilirken hata:', e);
    }
    this.notifyListeners();
  }

  private notifyListeners() {
    this.listeners.forEach((fn) => {
      try {
        fn([...this.notifications]);
      } catch {}
    });
  }

  public subscribe(fn: (notifs: UserNotification[]) => void) {
    this.listeners.add(fn);
    fn([...this.notifications]);
    return () => {
      this.listeners.delete(fn);
    };
  }

  public getAll(): UserNotification[] {
    return [...this.notifications];
  }

  public getUnreadCount(): number {
    return this.notifications.filter((n) => !n.read).length;
  }

  public markAsRead(id: string) {
    const item = this.notifications.find((n) => n.id === id);
    if (item && !item.read) {
      item.read = true;
      this.saveToStorage();
    }
  }

  public markAsUnread(id: string) {
    const item = this.notifications.find((n) => n.id === id);
    if (item && item.read) {
      item.read = false;
      this.saveToStorage();
    }
  }

  public remove(id: string) {
    const before = this.notifications.length;
    this.notifications = this.notifications.filter((n) => n.id !== id);
    if (this.notifications.length !== before) {
      this.tombstone([id]);
      this.saveToStorage();
    }
  }

  public markAllAsRead() {
    let changed = false;
    this.notifications.forEach((n) => {
      if (!n.read) {
        n.read = true;
        changed = true;
      }
    });
    if (changed) {
      this.saveToStorage();
    }
  }

  public clearAll() {
    const newest = this.notifications.reduce((m, n) => (n.createdAt > m ? n.createdAt : m), new Date().toISOString());
    this.notifications = [];
    this.tombstone([], newest);
    this.saveToStorage();
  }

  /**
   * Yeni bir bildirim ekle ve izin verildiyse sistem anlık bildirimi (Web Push / Notification) fırlat
   */
  public addNotification(
    notification: Omit<UserNotification, 'id' | 'createdAt' | 'read'>,
    opts: { read?: boolean; silent?: boolean } = {}
  ) {
    const newNotif: UserNotification = {
      ...notification,
      id: 'notif-' + Date.now() + '-' + Math.random().toString(36).substring(2, 7),
      createdAt: new Date().toISOString(),
      read: Boolean(opts.read),
    };

    // Başa ekle
    this.notifications.unshift(newNotif);
    this.saveToStorage();

    // Sistem anlık bildirimi tetikle
    if (!opts.silent) this.triggerSystemPush(newNotif);

    return newNotif;
  }

  public isPushEnabled(): boolean {
    if (typeof window === 'undefined' || !('Notification' in window)) return false;
    return localStorage.getItem(PUSH_PERM_KEY) === 'true' && Notification.permission === 'granted';
  }

  public async requestPushPermission(): Promise<boolean> {
    if (typeof window === 'undefined' || !('Notification' in window)) return false;
    try {
      const permission = await Notification.requestPermission();
      const granted = permission === 'granted';
      localStorage.setItem(PUSH_PERM_KEY, granted ? 'true' : 'false');
      return granted;
    } catch {
      return false;
    }
  }

  public setPushEnabled(enabled: boolean) {
    localStorage.setItem(PUSH_PERM_KEY, enabled ? 'true' : 'false');
    this.notifyListeners();
  }

  public isEmailEnabled(): boolean {
    return localStorage.getItem(EMAIL_PERM_KEY) === 'true';
  }

  public setEmailEnabled(enabled: boolean) {
    localStorage.setItem(EMAIL_PERM_KEY, enabled ? 'true' : 'false');
    this.notifyListeners();
  }

  private triggerSystemPush(notif: UserNotification) {
    if (typeof window === 'undefined' || !('Notification' in window)) return;
    if (Notification.permission !== 'granted' || !this.isPushEnabled()) return;

    try {
      const systemNotif = new Notification(notif.title, {
        body: notif.message,
        icon: '/icons/icon-192x192.png?v=9',
        badge: '/favicon.png?v=9',
        tag: notif.targetId || 'medsoru-notification',
      });

      systemNotif.onclick = () => {
        window.focus();
        systemNotif.close();
        this.markAsRead(notif.id);
        // Sayfayı yenilemeden hedef ekrana geç ve öğeye odaklan
        if (notif.deepLinkUrl) openDeepLink(notif.deepLinkUrl);
      };
    } catch (e) {
      console.warn('System notification error:', e);
    }
  }
}

export const userNotificationService = new UserNotificationService();
