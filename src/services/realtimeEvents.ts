/**
 * MedSoru Realtime Events Service (SSE - Server-Sent Events)
 *
 * Sürekli ağ yoklaması (short polling) yerine HTTP/2 multiplexed tek yönlü
 * kalıcı akış kurar. Sunucu veya veritabanında yeni bildirim, hata raporu,
 * yorum veya otomasyon değişikliği olduğunda istemciye anında iletir.
 */

import { AdminNotification } from '../types';
import { getLocalAdminSession } from './auth';

export type RealtimeConnectionStatus = 'disconnected' | 'connecting' | 'connected';

class RealtimeEventService {
  private eventSource: EventSource | null = null;
  private status: RealtimeConnectionStatus = 'disconnected';
  private statusListeners = new Set<(status: RealtimeConnectionStatus) => void>();
  private notificationListeners = new Set<(notif: AdminNotification) => void>();
  private inboxUpdateListeners = new Set<(data?: any) => void>();
  private autoRepairUpdateListeners = new Set<(data?: any) => void>();
  private questionChangeListeners = new Set<(data?: any) => void>();
  private questionUpdateListeners = new Set<(data?: any) => void>();
  private pastQuestionsChangeListeners = new Set<(data?: any) => void>();
  private pastQuestionUpdateListeners = new Set<(data?: any) => void>();
  private reconnectTimer: any = null;
  private reconnectAttempts = 0;
  private isExplicitlyClosed = false;
  private clientId: string | null = null;
  // Genel olay dinleyicileri (db_change, live, pong, votes_changed): olay adı → işleyiciler
  private genericListeners = new Map<string, Set<(data: any) => void>>();
  private boundGenericEvents = new Set<string>();

  constructor() {
    if (typeof window !== 'undefined') {
      // Sekme arka plandan ön plana geldiğinde bağlantıyı tazele
      document.addEventListener('visibilitychange', () => {
        if (!document.hidden && this.status === 'disconnected' && !this.isExplicitlyClosed) {
          this.connect();
        }
      });
      // Ağ çevrimiçi olduğunda anında bağlan
      window.addEventListener('online', () => {
        if (this.status === 'disconnected' && !this.isExplicitlyClosed) {
          this.reconnectAttempts = 0;
          this.connect();
        }
      });
    }
  }

  public connect() {
    if (typeof window === 'undefined' || !('EventSource' in window)) {
      return;
    }
    if (this.eventSource && (this.status === 'connected' || this.status === 'connecting')) {
      return;
    }

    this.isExplicitlyClosed = false;
    this.setStatus('connecting');

    try {
      // Yalnız oturum açmış yönetici kendi e-postasını yollar; ziyaretçiler yönetici olaylarını almaz.
      const adminSession = getLocalAdminSession();
      const url = adminSession?.email
        ? `/api/realtime/events?adminEmail=${encodeURIComponent(adminSession.email)}`
        : '/api/realtime/events';

      const es = new EventSource(url);
      this.eventSource = es;
      this.boundGenericEvents.clear();
      for (const ev of this.genericListeners.keys()) this.bindGeneric(ev);

      es.addEventListener('connected', (e: MessageEvent) => {
        try {
          this.clientId = JSON.parse(e.data)?.clientId || null;
        } catch (_) {}
        this.reconnectAttempts = 0;
        this.setStatus('connected');
      });

      es.addEventListener('admin_notification', (e: MessageEvent) => {
        try {
          const item = JSON.parse(e.data);
          const notif: AdminNotification = {
            id: item.id || `notif-${Date.now()}`,
            type: item.type || 'test',
            title: item.title || 'Bildirim',
            message: item.message || '',
            author: item.author || 'Sistem',
            timestamp: item.timestamp || new Date().toISOString(),
            isRead: Boolean(item.read ?? item.isRead ?? false),
            questionId: item.questionId,
            url: item.url,
          };
          this.notificationListeners.forEach((fn) => {
            try {
              fn(notif);
            } catch (err) {
              console.error('[RealtimeEvents] onNotification callback hatası:', err);
            }
          });
        } catch (err) {
          console.warn('[RealtimeEvents] Bildirim ayrıştırma hatası:', err);
        }
      });

      es.addEventListener('inbox_update', (e: MessageEvent) => {
        let payload: any = null;
        try {
          if (e.data) payload = JSON.parse(e.data);
        } catch (_) {}
        this.inboxUpdateListeners.forEach((fn) => {
          try {
            fn(payload);
          } catch (err) {
            console.error('[RealtimeEvents] onInboxUpdate callback hatası:', err);
          }
        });
      });

      es.addEventListener('auto_repair_update', (e: MessageEvent) => {
        let payload: any = null;
        try {
          if (e.data) payload = JSON.parse(e.data);
        } catch (_) {}
        this.autoRepairUpdateListeners.forEach((fn) => {
          try {
            fn(payload);
          } catch (err) {
            console.error('[RealtimeEvents] onAutoRepairUpdate callback hatası:', err);
          }
        });
      });

      // ================= Oracle Veritabanı Canlı Olayları (Realtime Database Events) =================

      // 1. Soru Havuzu Değişiklikleri
      es.addEventListener('questions_changed', (e: MessageEvent) => {
        let payload: any = null;
        try { if (e.data) payload = JSON.parse(e.data); } catch (_) {}
        this.questionChangeListeners.forEach((fn) => { try { fn(payload); } catch (_) {} });
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('medsoru:questions-changed', { detail: payload }));
        }
      });

      es.addEventListener('question_updated', async (e: MessageEvent) => {
        let payload: any = null;
        try { if (e.data) payload = JSON.parse(e.data); } catch (_) {}
        if (payload?.question) {
          try {
            const { clientCache } = await import('./clientCache');
            await clientCache.updateItemInList('questions', (q: any) => q.id === payload.id, () => payload.question);
          } catch (_) {}
        }
        this.questionUpdateListeners.forEach((fn) => { try { fn(payload); } catch (_) {} });
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('medsoru:question-updated', { detail: payload }));
        }
      });

      // 2. Çıkmış Soru Veritabanı Değişiklikleri
      es.addEventListener('past_questions_changed', (e: MessageEvent) => {
        let payload: any = null;
        try { if (e.data) payload = JSON.parse(e.data); } catch (_) {}
        this.pastQuestionsChangeListeners.forEach((fn) => { try { fn(payload); } catch (_) {} });
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('medsoru:past-questions-changed', { detail: payload }));
        }
      });

      es.addEventListener('past_question_updated', async (e: MessageEvent) => {
        let payload: any = null;
        try { if (e.data) payload = JSON.parse(e.data); } catch (_) {}
        if (payload?.question) {
          try {
            const { pastQuestionsCache } = await import('./pastQuestionsCache');
            await pastQuestionsCache.saveQuestion(payload.question);
          } catch (_) {}
        }
        this.pastQuestionUpdateListeners.forEach((fn) => { try { fn(payload); } catch (_) {} });
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('medsoru:past-question-updated', { detail: payload }));
        }
      });

      // 3. Not Defteri Eşitleme Olayı
      es.addEventListener('notes_changed', async (e: MessageEvent) => {
        let payload: any = null;
        try { if (e.data) payload = JSON.parse(e.data); } catch (_) {}
        try {
          const { pullDeltaNotes } = await import('./notesSync');
          void pullDeltaNotes();
        } catch (_) {}
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('medsoru:notes-synced', { detail: payload }));
        }
      });

      // 4. Genel Veritabanı Senkronizasyon Olayı
      es.addEventListener('database_sync', (e: MessageEvent) => {
        let payload: any = null;
        try { if (e.data) payload = JSON.parse(e.data); } catch (_) {}
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new CustomEvent('medsoru:database-sync', { detail: payload }));
        }
      });

      es.onerror = () => {
        es.close();
        this.eventSource = null;
        this.setStatus('disconnected');
        this.scheduleReconnect();
      };
    } catch (err) {
      console.warn('[RealtimeEvents] Bağlantı başlatılamadı:', err);
      this.setStatus('disconnected');
      this.scheduleReconnect();
    }
  }

  private scheduleReconnect() {
    if (this.isExplicitlyClosed || this.reconnectTimer) return;
    const delay = Math.min(30000, 1000 * Math.pow(1.5, this.reconnectAttempts) + Math.random() * 800);
    this.reconnectAttempts++;
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.connect();
    }, delay);
  }

  private setStatus(s: RealtimeConnectionStatus) {
    if (this.status !== s) {
      this.status = s;
      this.statusListeners.forEach((fn) => {
        try {
          fn(s);
        } catch (_) {}
      });
    }
  }

  private bindGeneric(event: string) {
    const es = this.eventSource;
    if (!es || this.boundGenericEvents.has(event)) return;
    this.boundGenericEvents.add(event);
    es.addEventListener(event, (e: MessageEvent) => {
      let payload: any = null;
      try { if (e.data) payload = JSON.parse(e.data); } catch (_) {}
      this.genericListeners.get(event)?.forEach((fn) => { try { fn(payload); } catch (_) {} });
    });
  }

  /** Herhangi bir SSE olayına abone ol (db_change, live, pong, votes_changed...). */
  public on(event: string, fn: (data: any) => void): () => void {
    let set = this.genericListeners.get(event);
    if (!set) this.genericListeners.set(event, (set = new Set()));
    set.add(fn);
    this.bindGeneric(event);
    this.ensureConnected();
    return () => {
      set!.delete(fn);
    };
  }

  /** Sunucunun bu bağlantıya verdiği kimlik (kendi canlı mesajını geri almamak için). */
  public getClientId(): string | null {
    return this.status === 'connected' ? this.clientId : null;
  }

  public getStatus(): RealtimeConnectionStatus {
    return this.status;
  }

  public isConnected(): boolean {
    return this.status === 'connected';
  }

  public onNotification(fn: (notif: AdminNotification) => void): () => void {
    this.notificationListeners.add(fn);
    this.ensureConnected();
    return () => {
      this.notificationListeners.delete(fn);
    };
  }

  public onInboxUpdate(fn: (data?: any) => void): () => void {
    this.inboxUpdateListeners.add(fn);
    this.ensureConnected();
    return () => {
      this.inboxUpdateListeners.delete(fn);
    };
  }

  public onAutoRepairUpdate(fn: (data?: any) => void): () => void {
    this.autoRepairUpdateListeners.add(fn);
    this.ensureConnected();
    return () => {
      this.autoRepairUpdateListeners.delete(fn);
    };
  }

  public onQuestionChange(fn: (data?: any) => void): () => void {
    this.questionChangeListeners.add(fn);
    this.ensureConnected();
    return () => {
      this.questionChangeListeners.delete(fn);
    };
  }

  public onQuestionUpdate(fn: (data?: any) => void): () => void {
    this.questionUpdateListeners.add(fn);
    this.ensureConnected();
    return () => {
      this.questionUpdateListeners.delete(fn);
    };
  }

  public onPastQuestionsChange(fn: (data?: any) => void): () => void {
    this.pastQuestionsChangeListeners.add(fn);
    this.ensureConnected();
    return () => {
      this.pastQuestionsChangeListeners.delete(fn);
    };
  }

  public onPastQuestionUpdate(fn: (data?: any) => void): () => void {
    this.pastQuestionUpdateListeners.add(fn);
    this.ensureConnected();
    return () => {
      this.pastQuestionUpdateListeners.delete(fn);
    };
  }

  public onStatusChange(fn: (status: RealtimeConnectionStatus) => void): () => void {
    this.statusListeners.add(fn);
    fn(this.status);
    return () => {
      this.statusListeners.delete(fn);
    };
  }

  private ensureConnected() {
    if (this.status === 'disconnected' && !this.eventSource && !this.isExplicitlyClosed) {
      this.connect();
    }
  }

  public disconnect() {
    this.isExplicitlyClosed = true;
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
    this.setStatus('disconnected');
  }
}

export const realtimeEventService = new RealtimeEventService();
