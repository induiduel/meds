/**
 * MeDSor Realtime Events Service (SSE - Server-Sent Events)
 *
 * Sürekli ağ yoklaması (short polling) yerine HTTP/2 multiplexed tek yönlü
 * kalıcı akış kurar. Sunucu veya veritabanında yeni bildirim, hata raporu,
 * yorum veya otomasyon değişikliği olduğunda istemciye anında iletir.
 */

import { adminIdTokenForStream } from './adminFetchAuth';
import { AdminNotification } from '../types';
import { getLocalAdminSession } from './auth';
import { panelProxied } from '../config/deployment';

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
  // Kaçan olay telafisi: son alınan olay kimliği yeniden bağlanırken sunucuya verilir (sunucu aradakileri yollar)
  private lastEventId = '';
  private lastDataAt = 0;
  private watchdog: any = null;
  private everConnected = false;
  private connectedAdmin = false;

  constructor() {
    if (typeof window !== 'undefined') {
      // Sekme arka plandan ön plana geldiğinde bağlantıyı tazele
      document.addEventListener('visibilitychange', () => {
        if (document.hidden || this.isExplicitlyClosed) return;
        // Uykudan/arka plandan dönüş: bağlı görünen ama sessiz kalmış akış ölü sayılır
        if (this.status === 'connected' && Date.now() - this.lastDataAt > 30_000) this.restart();
        else if (this.status === 'disconnected') {
          this.reconnectAttempts = 0;
          this.connect();
        }
      });
      // Sayfadan ayrılırken (yenileme, başka adrese gitme, geri/ileri önbelleği) akış KAPATILIR: kapatılmazsa önbellekteki
      // eski sayfaların SSE'leri açık kalıyor, HTTP/1.1'in sunucu başına 6 bağlantı sınırı dolunca yeni sayfanın parçaları
      // kuyrukta bekleyip ekran "Yükleniyor"da kalıyordu. Sayfa önbellekten geri gelirse akış lastEventId ile yeniden kurulur.
      let resumeOnShow = false;
      window.addEventListener('pagehide', () => {
        resumeOnShow = !this.isExplicitlyClosed && !!this.eventSource;
        if (this.eventSource || this.reconnectTimer) this.disconnect();
      });
      window.addEventListener('pageshow', (e) => {
        if (!(e as PageTransitionEvent).persisted || !resumeOnShow) return;
        resumeOnShow = false;
        this.reconnectAttempts = 0;
        this.connect();
      });
      // Yönetici girişi/çıkışı: yönetici olayları için akış yeni yetkiyle yeniden kurulur
      window.addEventListener('medsoru:admin-session', () => this.refreshAuth());
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
      // Yerel panel Oracle'a bağlıysa olaylar da Oracle'dan (gelen kutusu, canlı içerik)
      // (EventSource başlık yollayamaz: yerel sunucunun Oracle vekiline sorgu işaretiyle gider)
      const base = '';
      const qs = new URLSearchParams();
      if (panelProxied('/api/realtime/events')) qs.set('panelProxy', 'oracle');
      if (adminSession?.email) qs.set('adminEmail', adminSession.email);
      const streamToken = adminIdTokenForStream();
      if (streamToken) qs.set('idToken', streamToken);
      if (this.lastEventId) qs.set('lastEventId', this.lastEventId);
      const url = `${base}/api/realtime/events${qs.toString() ? `?${qs}` : ''}`;
      // Sunucu yalnız doğrulanmış jetonla yönetici sayar: yerel oturum işareti tek başına yetmez
      this.connectedAdmin = Boolean(streamToken);

      const es = new EventSource(url);
      this.lastDataAt = Date.now();
      this.eventSource = es;
      this.boundGenericEvents.clear();
      for (const ev of this.genericListeners.keys()) this.bindGeneric(ev);

      es.addEventListener('connected', (e: MessageEvent) => {
        try {
          this.clientId = JSON.parse(e.data)?.clientId || null;
        } catch (_) {}
        // İlk bağlantıda kimlik yoksa sunucunun verdiği güncel kimlikten başlanır (telafi bundan sonrası için)
        if (!this.lastEventId && e.lastEventId) this.lastEventId = e.lastEventId;
        this.reconnectAttempts = 0;
        this.setStatus('connected');
        this.everConnected = true;
      });

      // Sunucu kaçan olayları telafi edemedi (yeniden başladı ya da kopukluk uzun sürdü): herkes tazelesin
      es.addEventListener('resync', (e: MessageEvent) => {
        let payload: any = null;
        try { if (e.data) payload = JSON.parse(e.data); } catch (_) {}
        this.emitResync(payload?.reason || 'gap');
      });
      es.addEventListener('hb', () => {
        this.lastDataAt = Date.now();
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
          // Yalnız bu cihazın defteri değiştiyse çek (olay tüm ziyaretçilere gider)
          const { pullDeltaNotes, isOwnNotebook } = await import('./notesSync');
          if (!(await isOwnNotebook(payload?.codeHash))) return;
          // Ekranlar notları çekme bittikten sonra yeniden okusun (önceden bitmeden haber veriliyordu)
          await pullDeltaNotes();
        } catch (_) {
          return;
        }
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

      // Son olay kimliği: dinleyicisi olmayan olaylar da kimliği ilerletsin
      for (const ev of KNOWN_EVENTS) es.addEventListener(ev, (e: MessageEvent) => this.track(e));

      es.onerror = () => {
        es.close();
        this.eventSource = null;
        this.setStatus('disconnected');
        this.scheduleReconnect();
      };
      this.startWatchdog();
    } catch (err) {
      console.warn('[RealtimeEvents] Bağlantı başlatılamadı:', err);
      this.setStatus('disconnected');
      this.scheduleReconnect();
    }
  }

  private track(e: MessageEvent) {
    this.lastDataAt = Date.now();
    if (e?.lastEventId) this.lastEventId = e.lastEventId;
  }

  /** 45 sn hiç veri (kalp atışı dahil) gelmezse akış ölüdür: kapat, yeniden kur. */
  private startWatchdog() {
    if (this.watchdog) return;
    this.watchdog = setInterval(() => {
      if (this.isExplicitlyClosed || !this.eventSource) return;
      if (typeof document !== 'undefined' && document.hidden) return;
      if (Date.now() - this.lastDataAt > 45_000) this.restart();
    }, 10_000);
  }

  private emitResync(reason: string) {
    if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent('medsoru:realtime-resync', { detail: { reason } }));
    this.genericListeners.get('resync')?.forEach((fn) => { try { fn({ reason }); } catch (_) {} });
  }

  /** Bağlantıyı hemen yeniden kur (kimlik/yetki değişti ya da akış sessiz kaldı); kaçanlar lastEventId ile gelir. */
  public restart() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    this.isExplicitlyClosed = false;
    this.setStatus('disconnected');
    this.reconnectAttempts = 0;
    this.connect();
  }

  /** Yönetici oturumu açıldı/kapandı: yönetici olaylarını almak için akış yeni yetkiyle kurulur. */
  public refreshAuth() {
    const isAdmin = Boolean(adminIdTokenForStream());
    if (isAdmin !== this.connectedAdmin && this.eventSource) this.restart();
  }

  public hasConnectedBefore(): boolean {
    return this.everConnected;
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
    // 'resync' sunucu olayı yukarıda emitResync ile dağıtılır (çift çağrı olmasın)
    if (!es || event === 'resync' || this.boundGenericEvents.has(event)) return;
    this.boundGenericEvents.add(event);
    es.addEventListener(event, (e: MessageEvent) => {
      this.track(e);
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

// Kimlik takibi için baştan dinlenen olaylar (dinleyicisi olmasa da son kimlik ilerlesin)
const KNOWN_EVENTS = [
  'questions_changed', 'past_questions_changed', 'database_sync', 'db_change', 'votes_changed', 'live', 'notes_changed',
  'user_data_changed', 'content_changed', 'learn_social', 'learn_feedback_changed', 'people_changed', 'admin_notification',
  'inbox_update', 'auto_repair_update', 'basarim_changed', 'siralama_changed', 'question_updated', 'past_question_updated',
];

export const realtimeEventService = new RealtimeEventService();
