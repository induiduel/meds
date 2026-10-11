# Oracle VM Üzerinde Realtime Veritabanı Mimarisi ve Çözüm Rehberi

Bu belge, Oracle Cloud Always Free VM (Ubuntu 24.04 ARM, IP: 92.5.55.109) üzerinde çalışan MedSoru platformunda **gerçek zamanlı (Realtime) veritabanı** senkronizasyonunun nasıl çalıştığını, mimari katmanlarını ve yönetim adımlarını açıklar.

---

## 1. Mimari Genel Bakış (Çift Katmanlı Realtime)

Oracle sunucusu üzerindeki gerçek zamanlı veri akışı **iki tamamlayıcı katman** ile kusursuz ve kesintisiz çalışır:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 KULLANICI TARAYICISI                                   │
│  (React + TanStack Query + clientCache + pastQuestionsCache + realtimeEventService)    │
└───────────────────▲──────────────────────────────────────────────▲─────────────────────┘
                    │                                              │
         (1) SSE Kalıcı Akış                               (2) WebSocket WAL Akışı
       (/api/realtime/events)                               (Supabase Realtime :8000)
                    │                                              │
┌───────────────────▼──────────────────────────┐  ┌────────────────▼─────────────────────┐
│          Oracle Express API                  │  │     Oracle Yerel Supabase Yığını     │
│   (meds-app / meds-server Caddy :3000)       │  │          (supabase-server)           │
│                                              │  │                                      │
│ • broadcastRealtimeEvent()                   │  │ • PostgreSQL 15 (:5432)              │
│ • Soru ekleme/güncelleme/onay                │  │ • supabase/realtime (:4000)          │
│ • Beğeni, yorum ve hata bildirimleri         │  │ • envoy / kong API ağ geçidi (:8000) │
│ • Cihazlar arası not defteri eşitlemesi      │  │ • WAL (Write-Ahead-Log) yayınları    │
└──────────────────────────────────────────────┘  └──────────────────────────────────────┘
```

---

## 2. Katman 1: Oracle Native HTTP/2 SSE Realtime Dağıtıcı (0 ms Gecikme)

### Çalışma Prensibi
- **Uç Nokta:** `GET /api/realtime/events`
- **Tünel & Güvenlik:** Cloudflare Tunnel üzerinden doğrudan Caddy (`meds-server`) ve Express (`meds-app`) konteynerine ulaşır. Dışarıya port açılması gerekmez.
- **Keep-Alive Koruması:** Caddy ve Cloudflare'in boşta kalan bağlantıları kapatmasını önlemek için her 25 saniyede bir `: keep-alive` sinyali basılır.
- **Yayınlanan Olaylar:**
  1. `questions_changed`: Havuz soruları değiştiğinde.
  2. `question_updated`: Belirli bir soru yama (PATCH) aldığında veya güncellendiğinde (soru verisi gövdede iletilir, 0ms arayüz güncellemesi).
  3. `past_questions_changed`: Çıkmış soru veritabanı değiştiğinde.
  4. `past_question_updated`: Bir çıkmış soru onaylandığında, yapay zeka redaksiyonu yapıldığında veya oy aldığında.
  5. `notes_changed`: Kullanıcının başka bir cihazdan not eklemesi veya düzenlemesi durumunda.
  6. `database_sync`: Genel veritabanı senkronizasyon sinyali.
  7. `admin_notification` & `inbox_update`: Yöneticiye anlık bildirimler.

### İstemci Tarafı Entegrasyonu
`src/services/realtimeEvents.ts` bu akışı otomatik dinler:
- Yeni bir soru veya çıkmış soru güncellemesi geldiğinde `clientCache` ve `pastQuestionsCache` veriyi bellek ve IndexedDB içinde yerinde günceller.
- Sayfayı yeniden yükleme veya tüm listeyi tekrar indirme ihtiyacı **tamamen ortadan kalkar**.

---

## 3. Katman 2: Oracle Yerel Supabase PostgreSQL Realtime Motoru

Oracle VM'de `~/medsor/meds/supabase-server` dizininde 11 servislik yerel Supabase konteyner yığını bulunmaktadır. PostgreSQL veritabanındaki doğrudan satır değişikliklerini (INSERT, UPDATE, DELETE) WebSocket üzerinden gerçek zamanlı istemcilere akıtmak için:

### Veritabanı WAL Yayını Kurulum Komutları (Oracle PostgreSQL)
Oracle VM'e SSH ile bağlandıktan sonra:
```bash
ssh -i ~/.ssh/medsor-oracle.key ubuntu@92.5.55.109

# PostgreSQL içine gir
docker exec -it supabase-db psql -U postgres
```

Ardından şu SQL komutlarını çalıştırın:
```sql
-- 1. supabase_realtime yayınını kontrol et veya oluştur
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_publication WHERE pubname = 'supabase_realtime') THEN
    CREATE PUBLICATION supabase_realtime;
  END IF;
END $$;

-- 2. Gerçek zamanlı izlenecek tabloları yayına ekle
ALTER PUBLICATION supabase_realtime ADD TABLE past_questions;
ALTER PUBLICATION supabase_realtime ADD TABLE questions;
ALTER PUBLICATION supabase_realtime ADD TABLE lecture_notes;
ALTER PUBLICATION supabase_realtime ADD TABLE committees;
ALTER PUBLICATION supabase_realtime ADD TABLE users;
ALTER PUBLICATION supabase_realtime ADD TABLE system_status;

-- 3. Güncellemelerde eski ve yeni tüm satır verisini yayına dahil et (REPLICA IDENTITY FULL)
ALTER TABLE past_questions REPLICA IDENTITY FULL;
ALTER TABLE questions REPLICA IDENTITY FULL;
ALTER TABLE lecture_notes REPLICA IDENTITY FULL;
ALTER TABLE users REPLICA IDENTITY FULL;
```

---

## 4. Oracle Caddy Ters Proxy Yapılandırması (WebSocket Desteği)

Oracle'da çalışan `deploy/oracle/Caddyfile` dosyasında SSE ve WebSocket bağlantılarının tamponlanmadan (buffering olmadan) akması sağlanmıştır:

```caddyfile
:3000 {
    # SSE ve WebSocket akışlarının Cloudflare/Caddy tarafından kesilmemesi için
    reverse_proxy meds-app:3000 {
        flush_interval -1
    }
}
```

---

## 5. Sağlık ve Performans Ölçümü

Realtime bağlantı durumunu test etmek için:
1. Yönetici Paneli (`/manage`) -> **Sistem ve Veritabanı** sekmesine gidin.
2. **"Realtime Canlı Test Et"** butonuna basın.
3. Test, Oracle sunucusuna bir ping paketi gönderir; hem WebSocket broadcast hem de PostgreSQL WAL değişikliği tetiklenerek gidiş-dönüş (roundtrip) gecikmesi milisaniye cinsinden ölçülür (ideal süre: **15 - 45 ms**).
