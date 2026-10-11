/**
 * Kullanıcı Bildirim ve AI Kuyruk Takip Servisi (User Notification & AI Queue Service)
 * 
 * Kullanıcıların soruları, katkıları, yorumları ve AI geliştirme istekleri hakkındaki
 * tüm güncellemeleri yönetir.
 * 
 * Deep Linking ile tam uyumludur: Her bildirimin tıklandığında hedef elemana
 * odaklanan bir deepLinkUrl'i vardır.
 */

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
    | 'comment_deleted';
  title: string;
  message: string;
  deepLinkUrl: string;
  targetType: 'pool_question' | 'past_question' | 'term' | 'flashcard';
  targetId: string;
  read: boolean;
  createdAt: string;
}

const STORAGE_KEY = 'medsoru_user_notifications_v1';
const PUSH_PERM_KEY = 'medsoru_push_notifications_enabled';
const EMAIL_PERM_KEY = 'medsoru_email_notifications_enabled';

class UserNotificationService {
  private notifications: UserNotification[] = [];
  private listeners: Set<(notifs: UserNotification[]) => void> = new Set();

  constructor() {
    this.loadFromStorage();
    // Başka sekmede okundu/silindi işaretlenirse bu sekme de güncellenir.
    if (typeof window !== 'undefined') {
      window.addEventListener('storage', (e) => {
        if (e.key !== STORAGE_KEY) return;
        this.loadFromStorage();
        this.notifyListeners();
      });
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
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.notifications.slice(0, 100)));
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
    if (this.notifications.length !== before) this.saveToStorage();
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
    this.notifications = [];
    this.saveToStorage();
  }

  /**
   * Yeni bir bildirim ekle ve izin verildiyse sistem anlık bildirimi (Web Push / Notification) fırlat
   */
  public addNotification(notification: Omit<UserNotification, 'id' | 'createdAt' | 'read'>) {
    const newNotif: UserNotification = {
      ...notification,
      id: 'notif-' + Date.now() + '-' + Math.random().toString(36).substring(2, 7),
      createdAt: new Date().toISOString(),
      read: false,
    };

    // Başa ekle
    this.notifications.unshift(newNotif);
    this.saveToStorage();

    // Sistem anlık bildirimi tetikle
    this.triggerSystemPush(newNotif);

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
        if (notif.deepLinkUrl) {
          window.location.href = notif.deepLinkUrl;
        }
      };
    } catch (e) {
      console.warn('System notification error:', e);
    }
  }
}

export const userNotificationService = new UserNotificationService();
