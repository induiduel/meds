/**
 * MeDSor İstemci Tarafı Düşük Gecikmeli Realtime Quiz Soket İstemcisi
 * 
 * Görevleri:
 * 1. WebSocket bağlantı yönetimi ve otomatik yeniden bağlanma (reconnection).
 * 2. Ping-pong ile RTT (Round Trip Time) ve saat ofseti hesaplama (Server Time Sync).
 * 3. Pre-fetching ile soru metinlerinin yerel belleğe alınması ve 0ms arayüz render'ı.
 * 4. Milisaniye hassasiyetinde anlık cevap iletimi.
 */

import { getCustomApiUrl } from '../api';

export type QuizClientEventType =
  | 'room_joined'
  | 'player_joined'
  | 'player_left'
  | 'player_ready_changed'
  | 'game_countdown'
  | 'round_started'
  | 'answer_ack'
  | 'player_answered'
  | 'round_revealed'
  | 'game_finished'
  | 'room_error'
  | 'baglanti';

export interface PreFetchedQuestion {
  id: string;
  prompt: string;
  options: Record<string, string>;
  estimated_reading_sec: number;
  archetype: string;
}

export class QuizSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private roomId: string = '';
  private userId: string = '';
  private displayName: string = '';
  private isConnected: boolean = false;
  
  // Saat senkronizasyonu
  public rttMs: number = 0;
  public timeOffsetMs: number = 0; // serverTime - clientTime
  private pingIntervalId?: any;

  // Önceden yüklenmiş sorular (Zero-latency render)
  public preFetchedQuestions: Map<string, PreFetchedQuestion> = new Map();

  // Olay dinleyicileri
  private listeners: Map<QuizClientEventType, ((data: any) => void)[]> = new Map();

  constructor() {
    this.url = '';
  }

  /** Kullanıcının ayarladığı API adresine (getCustomApiUrl) uyar; yoksa sayfanın kendi kökü */
  private adres() {
    const ozel = getCustomApiUrl('/api/quiz/ws');
    const kok = ozel ? new URL(ozel, window.location.href) : new URL(window.location.href);
    return `${kok.protocol === 'https:' ? 'wss:' : 'ws:'}//${kok.host}/api/quiz/ws`;
  }

  /** kaynak: yalnız odayı kuran verir (branş, ders, soru sayısı, başlık); kodla katılan vermez */
  public connect(roomId: string, userId: string, displayName: string, courseId?: string, topicId?: string, kaynak?: Record<string, unknown>) {
    this.roomId = roomId;
    this.userId = userId;
    this.displayName = displayName;

    if (this.ws) {
      this.ws.onclose = null;
      this.ws.close();
    }

    this.url = this.adres();
    const ws = new WebSocket(this.url);
    this.ws = ws;

    ws.onopen = () => {
      this.isConnected = true;
      this.startClockSync();

      // Odaya katılma mesajı
      this.send({
        type: 'join_room',
        roomId,
        userId,
        displayName,
        courseId,
        topicId,
        kaynak
      });
      this.emit('baglanti', { bagli: true });
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        this.handleServerMessage(msg);
      } catch (e) {
        console.error('[QuizSocketClient] Mesaj ayrıştırma hatası:', e);
      }
    };

    ws.onclose = () => {
      if (this.ws !== ws) return;
      this.isConnected = false;
      this.stopClockSync();
      this.emit('baglanti', { bagli: false });
      // Yeniden bağlanma denemesi (3 sn sonra)
      setTimeout(() => {
        if (!this.isConnected && this.roomId) {
          this.connect(this.roomId, this.userId, this.displayName);
        }
      }, 3000);
    };

    ws.onerror = (err) => {
      console.warn('[QuizSocketClient] Hata:', err);
    };
  }

  public disconnect() {
    this.stopClockSync();
    // oda kimliği silinmezse onclose kendiliğinden yeniden bağlanıyordu
    this.roomId = '';
    if (this.ws) {
      this.ws.onclose = null;
      this.ws.close();
      this.ws = null;
    }
  }

  public on(event: QuizClientEventType, callback: (data: any) => void) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(callback);
  }

  public off(event: QuizClientEventType, callback: (data: any) => void) {
    const arr = this.listeners.get(event);
    if (!arr) return;
    this.listeners.set(event, arr.filter(cb => cb !== callback));
  }

  private emit(event: QuizClientEventType, data: any) {
    const cbs = this.listeners.get(event);
    if (cbs) {
      for (const cb of cbs) {
        cb(data);
      }
    }
  }

  public setReady() {
    this.send({ type: 'set_ready' });
  }

  public submitAnswer(questionId: string, option: string) {
    this.send({
      type: 'submit_answer',
      questionId,
      option
    });
  }

  /**
   * Sunucu saati ile senkronizasyon (NTP benzeri Ping-Pong RTT ölçümü)
   */
  private startClockSync() {
    this.stopClockSync();
    this.pingIntervalId = setInterval(() => {
      if (this.isConnected && this.ws?.readyState === WebSocket.OPEN) {
        this.send({
          type: 'ping',
          clientTime: Date.now()
        });
      }
    }, 5000); // 5 saniyede bir saat kontrolü
  }

  private stopClockSync() {
    if (this.pingIntervalId) {
      clearInterval(this.pingIntervalId);
      this.pingIntervalId = undefined;
    }
  }

  private handleServerMessage(msg: any) {
    switch (msg.type) {
      case 'pong': {
        const now = Date.now();
        const rtt = now - msg.clientTime;
        this.rttMs = rtt;
        // Server time offset = serverTime - (clientTime + RTT/2)
        this.timeOffsetMs = msg.serverTime - (msg.clientTime + Math.round(rtt / 2));
        
        // Sunucuya ölçülen değerleri raporla
        this.send({
          type: 'sync_time',
          rttMs: this.rttMs,
          timeOffsetMs: this.timeOffsetMs
        });
        break;
      }

      case 'room_error': {
        this.roomId = '';
        this.emit('room_error', msg);
        break;
      }

      case 'room_joined': {
        // Önceden yüklenmiş soruları kaydet
        if (msg.questions && Array.isArray(msg.questions)) {
          this.preFetchedQuestions.clear();
          for (const q of msg.questions) {
            this.preFetchedQuestions.set(q.id, q);
          }
        }
        this.emit('room_joined', msg);
        break;
      }

      case 'round_started': {
        // Yerel bellekten soruyu çek ve anında göster
        const qData = this.preFetchedQuestions.get(msg.questionId);
        this.emit('round_started', {
          ...msg,
          question: qData
        });
        break;
      }

      default: {
        this.emit(msg.type, msg);
        break;
      }
    }
  }

  public getServerTime(): number {
    return Date.now() + this.timeOffsetMs;
  }

  private send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }
}

export const quizSocketClient = new QuizSocketClient();
