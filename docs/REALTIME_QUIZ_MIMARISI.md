# Düşük Gecikmeli (Low-Latency) Realtime Quiz ve Rekabet Mimarisi

Bu belge; 5-15 saniyelik active recall sorularının eşzamanlı (multiplayer) veya bireysel yarışmalarda **ağ gecikmesini (latency) mutlak minimuma indirmek (<50 ms)** için tasarlanmış uçtan uca mimariyi, protokolleri ve çalışma prensiplerini açıklar.

---

## 1. TEMEL MİMARİ İLKELERİ: SIFIR GECİKME YAKLAŞIMI

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                 OYUNCU TARAYICISI                                │
│  (QuizSocketClient · Pre-fetched Question Map · Local Timer · Millisecond Clock) │
└───────────────────▲──────────────────────────────────────────────▲───────────────┘
                    │                                              │
           (1) WebSocket Full-Duplex                      (2) NTP Ping-Pong Sync
             (/api/quiz/ws - Native)                          (RTT & Offset)
                    │                                              │
┌───────────────────▼──────────────────────────────────────────────▼───────────────┐
│                          ORACLE NODE.JS EXPRESS SUNUCUSU                         │
│                           (quizRealtimeServer - In-Memory)                       │
│                                                                                  │
│  • Oda Yöneticisi (Map<RoomId, QuizRoom>) — RAM İçi İşlem (0 ms DB Wait)         │
│  • Server-Authoritative Saat ve Milisaniye Puanlama Motoru                       │
│  • Anlık Round Trigger & Broadcast                                               │
│  • Write-Behind Asenkron Kalıcılık (PostgreSQL DDL 0002_quiz_motoru.sql)         │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 1. HTTP/Polling ve SSE Yerine Native WebSocket (`/api/quiz/ws`)
- **Neden:** HTTP istekleri her seferinde TCP/TLS el sıkışması, başlık (header) ek yükü (1-2 KB) ve tek yönlü istek-cevap döngüsü yaratır. SSE ise tek yönlüdür; istemciden gelen cevabın HTTP POST ile gitmesi 50-150 ms gecikme ekler.
- **Çözüm:** `ws` kütüphanesi ile doğrudan TCP üzerinde tam çift yönlü (full-duplex) kalıcı soket kurulur. Veri paketleri başlık yükünden arındırılmış hafif JSON olarak <5 ms içinde taşınır.

### 2. Önceden Yükleme (Zero-Latency Pre-fetching)
- **Neden:** Tur başladığı anda soru metnini ve şıklarını ağdan çekmek; mobil veya zayıf ağlarda 200-800 ms render gecikmesine yol açar ve 10 saniyelik bir sorunun %10'unu yer.
- **Çözüm:** Odaya katılma (`join_room`) anında veya lobi aşamasında, tura ait tüm soruların metinleri, şıkları ve tahmini süreleri **doğru cevap şıkkı hariç tutularak** istemcinin yerel belleğine (`preFetchedQuestions`) aktarılır.
- **Sonuç:** Tur başladığında sunucu yalnızca 64 baytlık tetikleyici yollar:
  ```json
  {"type": "round_started", "questionIndex": 2, "questionId": "qz_k2-07_005_p", "deadlineMs": 1729904523000}
  ```
  İstemci soruyu yerel RAM'den okuyup **0 ms gecikmeyle ekrana basar**.

### 3. Server-Authoritative Saat Senkronizasyonu (Clock Drift Sync)
- **Neden:** Farklı telefon ve bilgisayarların sistem saatleri gerçek zamandan 1-3 saniye farklı olabilir. İstemci saatine güvenilirse hile veya adaletsiz süre kayıpları oluşur.
- **Çözüm:** NTP protokolü benzeri hafif bir `ping-pong` mekanizması çalışır:
  $$\text{RTT} = T_{\text{client\_recv}} - T_{\text{client\_send}}$$
  $$T_{\text{offset}} = T_{\text{server}} - \left(T_{\text{client\_send}} + \frac{\text{RTT}}{2}\right)$$
- Sunucu her tur için mutlak bir bitiş zamanı (`roundDeadlineMs`) belirler. İstemcinin yerel geri sayım çubuğu bu ofset ile sunucu saatine tam senkronize akar.

### 4. RAM İçi Oda Durumu (In-Memory State - 0 ms DB Blokajı)
- **Neden:** Her soru yanıtında veritabanına `INSERT`/`UPDATE` sorgusu atmak, disk I/O ve transaction kilitleri yüzünden 10-50 ms gecikme ve sunucu darboğazı yaratır.
- **Çözüm:** Tüm aktif yarışmalar, oyuncuların cevapları, anlık skorları ve streak'leri Node.js sunucu belleğinde (`Map<string, QuizRoom>`) mikrosaniye hızında işlenir.
- **Write-Behind:** Yarışma tamamen bittiğinde sonuçlar arka planda toplu (batch insert) olarak `quiz_solo_oturumlar` veya `quiz_multiplayer_odalar` tablolarına kaydedilir.

---

## 2. PUANLAMA VE REKABET DİNAMİĞİ

Kısa active recall sorularında (5-15 sn) adil bir yarışma için formül:

$$\text{Puan} = \text{Doğruluk Puanı (1000)} + \text{Hız Bonusu (maks 500)} + \text{Streak Bonusu (maks 250)}$$

- **Doğruluk Puanı:** Soru doğru yanıtlandığında sabit 1000 puan.
- **Hız Bonusu:** Kalan süre oranına göre doğrusal azalır:
  $$\text{Hız Bonusu} = \text{Kalan Oran} \times 500$$
  *(Örn: 10 saniyelik soruyu 2 saniyede çözen öğrenci 400 puan hız bonusu alır).*
- **Streak Bonusu:** Art arda doğru cevaplar serisinde her doğru için $+50$ puan (maksimum 250 puan). Yanlış cevapta seri sıfırlanır.
- **Erken Tur Bitirme:** Odadaki tüm oyuncular yanıt verdiğinde süre bitimi beklenmez; tur anında `reveal` aşamasına geçer.

---

## 3. BAĞLANTI KOPMASI VE YENİDEN BAĞLANMA (FAST RECONNECT)

1. İstemci soket bağlantısı kesildiğinde (WiFi/Hücresel geçişi vb.) 3 saniyelik üstel geri çekilmeyle otomatik bağlanır.
2. `roomId` ve `userId` ile odaya yeniden bağlandığında; sunucu oda durumunu (`status`, `currentQuestionIndex`, `deadlineMs`) anında geri yükler.
3. Oyuncu aktif sorunun kalan süresinden kesintisiz yarışmaya devam eder.

---

## 4. KAPILAR VE ENTEGRASYON

- Sunucu modülü: [`meds/src/services/quiz/quizRealtimeServer.ts`](file:///home/indu/medsor/meds/src/services/quiz/quizRealtimeServer.ts)
- İstemci modülü: [`meds/src/services/quiz/quizSocketClient.ts`](file:///home/indu/medsor/meds/src/services/quiz/quizSocketClient.ts)
- Sunucu bağlayıcısı: [`meds/server.ts`](file:///home/indu/medsor/meds/server.ts) (`httpServerRef.on('upgrade')` / `/api/quiz/ws`)
- `AGENTS.md` ve `GEMINI.md` kurallarına "Düşük Gecikmeli Realtime WebSocket Standardı" olarak işlenmiştir.
