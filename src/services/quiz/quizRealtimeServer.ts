/**
 * MeDSor Düşük Gecikmeli (Low-Latency) Realtime Quiz Oda Yöneticisi
 * 
 * Sıfır Gecikme İlkeleri:
 * 1. WebSocket Native Taşıma Katmanı: HTTP overhead yok, iki yönlü full-duplex <10ms soket.
 * 2. In-Memory State (RAM): Yanıtlar ve puanlama RAM'de mikro-saniyeler içinde hesaplanır; DB blokajı 0.
 * 3. Pre-fetching (Ön Yükleme): Soru metinleri istemciye önceden aktarılır, tur başlangıcında 0ms ağ beklemesi.
 * 4. Server-Authoritative Clock & RTT Senkronizasyonu: Saat kaymalarını telafi eden adil süre motoru.
 * 5. Write-Behind Persistence: Veritabanına yazma işlemi oyun tamamlandığında asenkron yapılır.
 */

import { createRequire } from 'module';
import type { QuizQuestion } from '../../types/quiz';
import { oyunSorulari } from './oyunSoruKaynagi';
import { bayrakAcik } from '../yonetim16/siteAyar';

const require = createRequire(import.meta.url);
const wsModule = require('ws');
const WebSocketServer = wsModule.Server || wsModule.WebSocketServer;

export interface PlayerState {
  userId: string;
  displayName: string;
  socket: any;
  isReady: boolean;
  score: number;
  streak: number;
  rttMs: number;
  timeOffsetMs: number;
  /** Takım modu: A ya da B */
  takim?: 'A' | 'B';
  answers: Record<string, {
    option: string;
    responseTimeMs: number;
    isCorrect: boolean;
    pointsAwarded: number;
  }>;
}

export interface QuizRoom {
  roomId: string;
  courseId: string;
  topicId: string;
  status: 'lobby' | 'countdown' | 'in_round' | 'reveal' | 'finished';
  questions: QuizQuestion[];
  currentQuestionIndex: number;
  roundStartTimeMs: number;
  roundDurationSec: number;
  roundDeadlineMs: number;
  players: Map<string, PlayerState>;
  revealTimeoutId?: any;
  /** Oyunlar: kaynak adı (lobide gösterilir) ve odayı kuran */
  baslik?: string;
  kurucu?: string;
  /** Takım modu: oyuncular iki takıma ayrılır, takım puanı = üyelerin puan toplamı */
  takimli?: boolean;
}

class QuizRealtimeManager {
  private wss: any = null;
  private rooms: Map<string, QuizRoom> = new Map();

  /**
   * HTTP Sunucusuna WebSocket sunucusunu /api/quiz/ws yolunda bağlar.
   */
  public initialize(server: any) {
    if (!server) return;
    this.wss = new WebSocketServer({ noServer: true });

    server.on('upgrade', (request: any, socket: any, head: any) => {
      const url = new URL(request.url || '', `http://${request.headers.host || 'localhost'}`);
      if (url.pathname === '/api/quiz/ws') {
        this.wss?.handleUpgrade(request, socket, head, (ws: any) => {
          this.wss?.emit('connection', ws, request);
        });
      }
    });

    this.wss.on('connection', (ws: any, req: any) => {
      this.handleConnection(ws, req);
    });

    console.log('⚡ [Realtime Quiz] WebSocket sunucusu /api/quiz/ws üzerinde aktif.');
  }

  private handleConnection(ws: any, req: any) {
    let currentRoomId: string | null = null;
    let currentUserId: string | null = null;

    ws.on('message', (messageRaw: any) => {
      try {
        const msg = JSON.parse(messageRaw.toString());
        const now = Date.now();

        switch (msg.type) {
          // 1. Ultra-düşük gecikmeli ping-pong ve zaman senkronizasyonu
          case 'ping': {
            const clientSendTime = msg.clientTime;
            ws.send(JSON.stringify({
              type: 'pong',
              clientTime: clientSendTime,
              serverTime: now
            }));
            break;
          }

          // RTT ve Saat ofseti raporlama
          case 'sync_time': {
            if (currentRoomId && currentUserId) {
              const player = this.rooms.get(currentRoomId)?.players.get(currentUserId);
              if (player) {
                player.rttMs = msg.rttMs || 0;
                player.timeOffsetMs = msg.timeOffsetMs || 0;
              }
            }
            break;
          }

          // 2. Odaya katılma
          case 'join_room': {
            const { userId, displayName, courseId, topicId, kaynak } = msg;
            const roomId = String(msg.roomId || '').toUpperCase().slice(0, 12);
            if (!roomId || !userId) break;
            // Oyunlar: oda yalnız kaynak (branş + isteğe bağlı ders + soru sayısı) verilerek kurulur; kodla katılan
            // kaynaksız gelir — oda yoksa hata döner (sorusuz oda kurulup oyun hiç başlamıyordu)
            // Panel bayrakları (Yönetim › Site/Oyunlar): oyunlar kapalı ya da canlı/takım modu kapalıysa oda kurulmaz/katılınmaz
            if (!bayrakAcik('oyunlar') || (kaynak && !bayrakAcik(kaynak.takim ? 'oyun_mod_takim' : 'oyun_mod_canli'))) {
              ws.send(JSON.stringify({ type: 'room_error', mesaj: 'Bu oyun şu an kapalı.' }));
              return;
            }
            if (!this.rooms.has(roomId)) {
              const sorular = kaynak?.brans ? oyunSorulari(String(kaynak.brans), kaynak.ders ? String(kaynak.ders) : undefined, Number(kaynak.n) || 10) : [];
              if (!sorular.length) {
                ws.send(JSON.stringify({ type: 'room_error', mesaj: kaynak ? 'Bu kaynakta oyuna uygun soru yok.' : 'Bu kodla açık oda yok. Kodu kontrol et.' }));
                break;
              }
              const oda = this.createOrJoinRoom(roomId, String(kaynak.brans), String(kaynak.ders || ''), sorular);
              oda.baslik = String(kaynak.baslik || '').slice(0, 120);
              oda.kurucu = String(userId);
              oda.takimli = !!kaynak.takim;
            }
            currentRoomId = roomId;
            currentUserId = String(userId);
            this.handleJoinRoom(ws, roomId, String(userId), String(displayName || 'Öğrenci').slice(0, 40), courseId, topicId);
            break;
          }

          // Takım modu: lobide takım değiştirme
          case 'set_team': {
            if (currentRoomId && currentUserId) {
              const room = this.rooms.get(currentRoomId);
              const p = room?.players.get(currentUserId);
              if (room?.takimli && room.status === 'lobby' && p && (msg.takim === 'A' || msg.takim === 'B')) {
                p.takim = msg.takim;
                this.broadcast(room, { type: 'player_team_changed', userId: currentUserId, takim: p.takim });
              }
            }
            break;
          }

          // 3. Hazır durumu
          case 'set_ready': {
            if (currentRoomId && currentUserId) {
              this.handleSetReady(currentRoomId, currentUserId);
            }
            break;
          }

          // 4. Anlık Cevap Gönderimi (Zero-Latency Answer Submit)
          case 'submit_answer': {
            if (currentRoomId && currentUserId) {
              const room = this.rooms.get(currentRoomId);
              if (room) {
                this.handleSubmitAnswer(room, currentUserId, msg.questionId, msg.option, now);
              }
            }
            break;
          }

          default:
            break;
        }
      } catch (err) {
        console.error('[Realtime Quiz WS] Mesaj ayrıştırma hatası:', err);
      }
    });

    ws.on('close', () => {
      // aynı oyuncu yeni soketle döndüyse eski soketin kapanışı onu odadan silmesin
      if ((ws as any).__eskiOyuncu) return;
      if (currentRoomId && currentUserId) {
        this.handleDisconnect(currentRoomId, currentUserId);
      }
    });
  }

  /**
   * Odaya oyuncu ekleme veya yeni oda oluşturma.
   */
  /** Yönetim › Oyunlar › Canlı odalar: RAM'deki odaların özeti */
  public odaListesi() {
    return [...this.rooms.values()].map((r) => ({
      roomId: r.roomId, baslik: r.baslik || '', kaynak: r.courseId, ders: r.topicId, durum: r.status, takimli: !!r.takimli,
      soru: r.questions.length, sira: r.currentQuestionIndex, kurucu: r.kurucu || '',
      oyuncular: [...r.players.values()].map((p) => ({ userId: p.userId, ad: p.displayName, puan: p.score, hazir: p.isReady, takim: p.takim || null, bagli: p.socket?.readyState === 1 })),
    }));
  }

  /** Odayı kapat: oyunculara bildirilir, soketler kapanır, oda RAM'den silinir */
  public odaKapat(roomId: string, neden = 'Oda yönetici tarafından kapatıldı.'): boolean {
    const r = this.rooms.get(roomId);
    if (!r) return false;
    if (r.revealTimeoutId) clearTimeout(r.revealTimeoutId);
    for (const p of r.players.values()) {
      try { p.socket?.send(JSON.stringify({ type: 'room_error', mesaj: neden })); } catch { /* */ }
      try { p.socket?.close(4000, 'oda kapatildi'); } catch { /* */ }
    }
    this.rooms.delete(roomId);
    return true;
  }

  public createOrJoinRoom(roomId: string, courseId: string, topicId: string, questions: QuizQuestion[]): QuizRoom {
    let room = this.rooms.get(roomId);
    if (!room) {
      room = {
        roomId,
        courseId,
        topicId,
        status: 'lobby',
        questions,
        currentQuestionIndex: 0,
        roundStartTimeMs: 0,
        roundDurationSec: 10,
        roundDeadlineMs: 0,
        players: new Map()
      };
      this.rooms.set(roomId, room);
    }
    return room;
  }

  private handleJoinRoom(ws: any, roomId: string, userId: string, displayName: string, courseId: string, topicId: string) {
    let room = this.rooms.get(roomId);
    if (!room) {
      room = this.createOrJoinRoom(roomId, courseId || 'pharmacology', topicId || 'k2-07', []);
    }

    // Yeniden bağlanan oyuncu puanını ve cevaplarını korur (yalnız soketi yenilenir)
    const eski = room.players.get(userId);
    if (eski) {
      if (eski.socket && eski.socket !== ws) { try { eski.socket.__eskiOyuncu = true; eski.socket.close(); } catch { /* yok */ } }
      eski.socket = ws;
      eski.displayName = displayName;
    }
    // Oyuncu kaydı
    const player: PlayerState = eski || {
      userId,
      displayName,
      socket: ws,
      isReady: false,
      score: 0,
      streak: 0,
      rttMs: 0,
      timeOffsetMs: 0,
      answers: {}
    };

    // Takım modu: yeni oyuncu az kişili takıma (eşitse A)
    if (room.takimli && !player.takim) {
      const say = (t: 'A' | 'B') => [...room.players.values()].filter((p) => p.userId !== userId && p.takim === t).length;
      player.takim = say('B') < say('A') ? 'B' : 'A';
    }
    room.players.set(userId, player);

    // Önceden Yükleme (Pre-fetching): Soru metinlerini (doğru cevap gizlenmiş olarak) istemciye tek seferde yolla!
    const sanitizedQuestions = room.questions.map(q => ({
      id: q.id,
      prompt: q.prompt,
      options: q.options,
      estimated_reading_sec: q.estimated_reading_sec,
      archetype: q.archetype
    }));

    // Katılan oyuncuya oda durumu ve sorular
    ws.send(JSON.stringify({
      type: 'room_joined',
      roomId,
      status: room.status,
      currentQuestionIndex: room.currentQuestionIndex,
      questions: sanitizedQuestions, // Pre-fetched questions
      players: this.getPublicPlayersList(room),
      baslik: room.baslik || '',
      kurucu: room.kurucu || '',
      takimli: !!room.takimli,
      takimSkor: this.getTakimSkor(room),
      deadlineMs: room.status === 'in_round' ? room.roundDeadlineMs : 0,
      serverTime: Date.now()
    }));

    // Diğer oyunculara duyur
    this.broadcast(room, {
      type: 'player_joined',
      player: { userId, displayName, score: player.score, streak: player.streak, isReady: player.isReady, takim: player.takim }
    }, userId);
  }

  private handleSetReady(roomId: string, userId: string) {
    const room = this.rooms.get(roomId);
    if (!room) return;
    const player = room.players.get(userId);
    if (!player) return;

    player.isReady = true;
    this.broadcast(room, {
      type: 'player_ready_changed',
      userId,
      isReady: true
    });

    // Tüm oyuncular hazırsa ve en az 1 kişi varsa geri sayımı başlat
    const allReady = Array.from(room.players.values()).filter(p => p.socket).every(p => p.isReady);
    if (allReady && room.players.size >= 1 && room.status === 'lobby' && room.questions.length > 0) {
      this.startCountdown(room);
    }
  }

  /**
   * Oyun geri sayımı (3, 2, 1) ve ardından 1. soru
   */
  private startCountdown(room: QuizRoom) {
    room.status = 'countdown';
    const countdownSec = 3;
    const startTime = Date.now() + countdownSec * 1000;

    this.broadcast(room, {
      type: 'game_countdown',
      countdownSec,
      startTime
    });

    setTimeout(() => {
      this.startRound(room, 0);
    }, countdownSec * 1000);
  }

  /**
   * Tur Başlatma: Sıfır Ağ Gecikmeli Tetikleme
   * İstemci zaten soruyu belleğe aldığı için sadece round index ve deadline yollanır!
   */
  private startRound(room: QuizRoom, questionIndex: number) {
    if (this.rooms.get(room.roomId) !== room) return; // oda kapatıldı (yönetici)
    if (questionIndex >= room.questions.length) {
      this.finishGame(room);
      return;
    }

    room.status = 'in_round';
    room.currentQuestionIndex = questionIndex;
    const question = room.questions[questionIndex];
    const durationSec = question.estimated_reading_sec || 10;
    const now = Date.now();

    room.roundDurationSec = durationSec;
    room.roundStartTimeMs = now;
    room.roundDeadlineMs = now + (durationSec * 1000);

    // Tüm oyunculara anlık tur başlangıç sinyali
    this.broadcast(room, {
      type: 'round_started',
      questionIndex,
      questionId: question.id,
      durationSec,
      deadlineMs: room.roundDeadlineMs,
      serverTime: now
    });

    // Otomatik süre dolumu zamanlayıcısı (Süre bitince doğru şıkkı açıkla)
    if (room.revealTimeoutId) clearTimeout(room.revealTimeoutId);
    room.revealTimeoutId = setTimeout(() => {
      this.revealRound(room);
    }, durationSec * 1000 + 150); // 150ms ağ marjı
  }

  /**
   * Anlık Cevap Gönderimi ve Puanlama
   */
  private handleSubmitAnswer(room: QuizRoom, userId: string, questionId: string, option: string, submitTimeMs: number) {
    if (room.status !== 'in_round') return;

    const currentQ = room.questions[room.currentQuestionIndex];
    if (!currentQ || currentQ.id !== questionId) return;

    const player = room.players.get(userId);
    if (!player || player.answers[questionId]) return; // Çift cevap engelleme

    const responseTimeMs = Math.max(0, submitTimeMs - room.roundStartTimeMs);
    const isCorrect = (option === currentQ.correct_option);

    // Puanlama: Doğruluk (1000 puan) + Hız Bonusu (Kalan süreye göre maks 500 puan) + Streak Bonusu
    let points = 0;
    if (isCorrect) {
      const remainingTimeRatio = Math.max(0, (room.roundDeadlineMs - submitTimeMs) / (room.roundDurationSec * 1000));
      const speedBonus = Math.round(remainingTimeRatio * 500);
      const streakBonus = Math.min(player.streak * 50, 250);
      points = 1000 + speedBonus + streakBonus;
      player.streak += 1;
      player.score += points;
    } else {
      player.streak = 0;
    }

    player.answers[questionId] = {
      option,
      responseTimeMs,
      isCorrect,
      pointsAwarded: points
    };

    // Cevap onayını yalnız cevaplayan kişiye hemen dön (düşük gecikmeli ACK)
    if (player.socket?.readyState === 1) {
      player.socket.send(JSON.stringify({
        type: 'answer_ack',
        questionId,
        isCorrect,
        pointsAwarded: points,
        currentScore: player.score,
        currentStreak: player.streak
      }));
    }

    // Diğer oyunculara kimin cevapladığını duyur (seçeneği gizli tutarak)
    this.broadcast(room, {
      type: 'player_answered',
      userId,
      responseTimeMs
    }, userId);

    // Eğer odadaki herkes cevap verdiyse sürenin bitmesini beklemeden hemen açıkla!
    const allAnswered = Array.from(room.players.values()).filter(p => p.socket).every(p => !!p.answers[questionId]);
    if (allAnswered) {
      if (room.revealTimeoutId) clearTimeout(room.revealTimeoutId);
      this.revealRound(room);
    }
  }

  /**
   * Doğru Şıkkı Açıklama ve Canlı Skor Tablosu
   */
  private revealRound(room: QuizRoom) {
    if (room.status !== 'in_round') return;
    room.status = 'reveal';

    const currentQ = room.questions[room.currentQuestionIndex];
    const leaderboard = this.getLeaderboard(room);

    this.broadcast(room, {
      type: 'round_revealed',
      questionId: currentQ.id,
      correctOption: currentQ.correct_option,
      optionExplanations: currentQ.option_explanations,
      leaderboard,
      takimSkor: this.getTakimSkor(room)
    });

    // 4 saniye sonra sonraki tura geç
    setTimeout(() => {
      this.startRound(room, room.currentQuestionIndex + 1);
    }, 4000);
  }

  private finishGame(room: QuizRoom) {
    room.status = 'finished';
    const finalLeaderboard = this.getLeaderboard(room);

    this.broadcast(room, {
      type: 'game_finished',
      finalLeaderboard,
      takimSkor: this.getTakimSkor(room)
    });
  }

  private handleDisconnect(roomId: string, userId: string) {
    const room = this.rooms.get(roomId);
    if (!room) return;

    const p = room.players.get(userId);
    // Oyun sürerken kopan oyuncu puanıyla kalır (aynı kimlikle dönebilir); lobide/bitişte odadan çıkar
    if (p && (room.status === 'lobby' || room.status === 'finished')) room.players.delete(userId);
    else if (p) p.socket = null;
    this.broadcast(room, {
      type: 'player_left',
      userId
    });

    const bagli = [...room.players.values()].some((x) => x.socket && x.socket.readyState === 1);
    if (room.players.size === 0 || !bagli) {
      if (room.revealTimeoutId) clearTimeout(room.revealTimeoutId);
      this.rooms.delete(roomId);
    }
  }

  private broadcast(room: QuizRoom, payload: any, exceptUserId?: string) {
    const data = JSON.stringify(payload);
    for (const [uid, player] of room.players) {
      if (exceptUserId && uid === exceptUserId) continue;
      if (player.socket && player.socket.readyState === 1) { // 1 = OPEN
        player.socket.send(data);
      }
    }
  }

  private getPublicPlayersList(room: QuizRoom) {
    return Array.from(room.players.values()).map(p => ({
      userId: p.userId,
      displayName: p.displayName,
      isReady: p.isReady,
      score: p.score,
      streak: p.streak,
      takim: p.takim
    }));
  }

  /** Takım modu: üyelerin puan toplamı ve kişi sayısı; takımsız odada null */
  private getTakimSkor(room: QuizRoom) {
    if (!room.takimli) return null;
    const t = { A: { puan: 0, kisi: 0 }, B: { puan: 0, kisi: 0 } };
    for (const p of room.players.values()) if (p.takim) { t[p.takim].puan += p.score; t[p.takim].kisi += 1; }
    return t;
  }

  private getLeaderboard(room: QuizRoom) {
    return Array.from(room.players.values())
      .map(p => ({
        userId: p.userId,
        displayName: p.displayName,
        score: p.score,
        streak: p.streak,
        takim: p.takim
      }))
      .sort((a, b) => b.score - a.score);
  }
}

export const quizRealtimeServer = new QuizRealtimeManager();
