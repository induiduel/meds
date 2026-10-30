# Aşama kuralları — genel

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/tam_hat/kural_secici.py`. 23 madde. Ayrıntı gerekirse madde başlığıyla defterde aç.

### H39 — Sesli metin kısaydı: sayfa atlanıyor, şekiller anlatılmıyordu (2026-10-24, kullanıcı "ders süresi az")
- k2-02'de 56 içerik sayfasının 12'si anlatılmamış, 19 sayfa tek cümleyle geçilmişti; "kısa ve öz" + paralel üretimde kapı yoktu.
  Kapı `isle.sesli_kapsam` (sayfa + derinlik). Kelime/dakika hedefi YOK; derinlik bilgi maddesi sayısından.

### H45 — Dar bölmede panel slayta göre büyüyor, yazının üstüne biniyor, kelimeler harf harf kırılıyordu (2026-10-24)
- Gerçek görüntüleyicide (Metin + Slayt, ~570 px sayfa) panel yazısı sabit px idi: panel slayta göre iki kat büyüyor,
  ayrılan boşluktan taşıp yazının üstüne biniyor, dar düğümde kelime harf harf kırılıyordu; panel yüksekliği tahmini de
  gerçeğin ~1,5 katı kısaydı. Düzeltme: panel/etiket boyu `cqw` (sayfa genişliğine oranlı), etiketler SVG'den HTML'e alındı
  (oransız ölçekte bozuluyordu), betikte `panel_boyu` (istemci diziliminin em kopyası). Sınama: 35 panelin hepsi 567 px ve
  1100 px sayfada ayrılan alana ve sayfa/ek alan sınırına sığıyor (sınama sayfası tarayıcı ölçümü).

### H47 — Kelime takipçisi küçük yazıyı okunmaz yapıyordu; ek alan gereğinden sık ve uzundu (2026-10-24)
- Telefon görüntüsü (s.54): konuşulan kelimenin iç gölgesi (3 px) ve koyu zemini "serebral" kelimesinin harflerini kapattı.
  Düzeltme: zemin .13, çizgi harflerin altında (2 px, dışarıda).
- Ek alan her sığmayan panelde baştan açılıyor ve panelin tamamı kadar oluyordu. Düzeltme: panel slaytın alt boşluğundan
  başlar, sayfa yalnız taşan kısım kadar uzar (en büyük ek 0,58 → 0,39 sayfa boyu; s.11'de ek alan hiç gerekmedi).
  Zincirde okun etiketi yanındaki düğümün altına girip kesiliyordu → etiket okun üstünde akış içinde, ok büzülmez.

### H68 — H66 tekrarı + süs bölüm sayfaları `sekil` türünde (2026-10-26, k2-27 periyodik muayeneler)
- **Çözüm / kural:** Çıkmışlar `kanit.sayfa` cümlelerine bağlandı (c0003, c0037, c0047, c0101, c0112, c0204, c0213, c0218, c0222) ve sesli uyarı eklendi; süs bölüm sayfaları `tur: kapak` yapıldı. Haritacı, bilgi taşımayan bölüm başlık/kapanış sayfalarını `kapak` yazar; sesli yazar H66 adımını atlamaz. Kapı gevşetilmedi.


### H100 — Asklepios kutlama efekti görünmüyordu (2026-10-27)
- **Kural:** ortada çizilen efekt kartın altında kalmaz; kartı örtmeyen konuma (iki yan) çizilir ve canvas kart üstüne (`is-ust-katman`) alınır. Yeni kutlama efektini canlı kartla birlikte gör.


### H106 · `baglam.kazanimlar` kapak metninden türetilmiş çöp şablon cümleler içeriyor (2026-10-27, k2-08)
- **Çözüm:** k2-08 kazanımları dersten elle yazıldı (8 ölçülebilir kazanım).
- **Kural:** Genel şablon ("temel kavramlarını … analiz eder") ya da kapak metni içeren kazanım kullanılmaz. Açık iş: `isle.kazanimlar` kayıt yoksa boş dönmeli (kod düzeltmesi bu turda yapılmadı).


### H109 · v2 cümlesinin `ses` alanında iç cümle sonu: sunucu cümle sayısı v2 ile tutmuyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Çözüm:** `konusma_v2.dogrula` her `ses`'in tek cümle olmasını HATA sayar (`_cumle_sayisi`, sunucu kuralıyla aynı); yazar iki cümleyi iki v2 cümlesine böler. k2-01…k2-05 veride ihlal yok.
- **Kural:** her v2 `ses` tam bir cümledir; yazım betiğinde ayrıca kendi sınır kontrolü (cümle sayısı = 1, ≤25 kelime) çalıştırılır.


### Sesli derste geri oku "Ders çalış"a atıyordu (2026-10-27)
- **Çözüm / kural:** Uygulama içinden gelindiyse (`navigateTo` `__icGezinti` bayrağını koyar) ok `history.back()` yapar; doğrudan bağlantıyla açıldıysa ayrıntı sayfasına gider. Geri düğmeleri sabit hedefe değil, geldiği yere dönmelidir.


### Sesli derste canlı konum bazen çalışmıyor / bozuk çalışıyordu (2026-10-27)
- **Çözüm / kural:** Eksik öğede kısa aralıkla yeniden dene; sıfır boyutta kaydırma yapma; 3 px altı scroll farkını kullanıcı eylemi sayma. Yeni takip/kaydırma kodu bu üç durumu karşılamalı.


### H117 · Tam ekranda ayar düğmesi araç şeridini göstermiyordu (2026-10-27)
- **Çözüm/kural:** tam ekran şeridinde `container-type: normal; width: max-content`; seçici düzeltildi. Mutlak konumlu öğeye `container-type: inline-size` verilirse genişlik açıkça verilir; `:is()` içinde başa combinator yazılmaz.


### H106 · Çalışma takvimi (ısı haritası) hücreleri dev görünüyordu (2026-10-27)
- **Çözüm:** Sütun `minmax(0, 16px)` + `justify-content: start`; hücre en çok 16 px.
- **Kural:** Kare hücreli ızgaralarda (ısı haritası, takvim) sütun genişliğine üst sınır koy; `1fr` + `aspect-ratio` birlikte kullanılmaz.


### H111e · Profil verisi dinleyicileri render sırasında setState yapıyordu (2026-10-28, Bugün/Arka plan)
- **Çözüm:** `userKvSync.ts` `bildir()` dinleyicileri `queueMicrotask` ile çağırır (tüm dinleyiciler zaten zamanlayıcı/setState yapıyor; eşzamanlılık gerekmiyordu). Sınama: sayfa_tarama /bugun, /arka-plan konsol hatası 1 → 0.
- **Kural:** localStorage/depo yazımına bağlı olay yayıcıları dinleyicileri eşzamanlı çağırmaz (mikro görev); render içinde (useState başlatıcısı, useMemo) yan etkili yazım yapılmaz.


### H129 — "Salt okunur" SQL konsolu süper kullanıcıyla çalışıyordu (2026-10-28, Yönetim v16)
- **Kalıcı çözüm:** `pgAdminRoutes.ts` `/api/admin/pg/sql`: ilk sözcük izin listesi (SELECT/WITH/EXPLAIN/VALUES/TABLE/SHOW), tehlikeli işlev/katalog yasak listesi, işlem içinde `set local role meds_salt_okur` (NOLOGIN, yalnız `pg_read_all_data`). Rol kurulamazsa konsol kapalı (503). `DELETE /api/admin/pg/row` ve `POST /api/admin/db/import` sunucuda onay sözcüğü ister.
- **Önleme:** "salt okunur" iddia eden her uç bağlantı rolünün yetkisiyle sınanır (COPY TO PROGRAM, pg_read_file, pg_authid, CTE içinde DELETE); tehlikeli uçlar istemci onayına ek olarak sunucuda onay sözcüğü ister.


### H130 — Canlı içerik katmanı tam kopyaydı, kaynaktaki yeni kayıtları gölgeliyordu (2026-10-28)
- **Kalıcı çözüm:** Katman kayıt düzeyinde farktır: `data/content/<rel>.fark.json` (`kayitlar`, `silinen`, kaynaktaki kaydın sha'sı `taban`). Okuma = kaynak + fark (`_birlesik/<rel>` önbelleği). Yazıcılar tam dosyayı yine `writableContent` yoluna yazar; kilit bırakılınca birleşik tabana göre farka çevrilir. Eski kopyalar `scripts/icerik_katman.py goc` ile `_ids.json` izine göre farka çevrildi (yedek `data/_yedek/content_goc_*`). `content-overlay-sync.sh` farkı kayıt kayıt uygular, `taban` tutmazsa durur, tam kopya görürse durur.
- **Önleme:** `python3 scripts/icerik_katman.py denetle` 0 HATA (tam kopya = HATA, birleşimde kaynak kaydı eksik = HATA). Katmana bütün dosya kopyalayan yeni yazıcı yazılmaz; başlangıç kopyası gerekiyorsa `resolveContent(file)` (birleşik) kopyalanır, ham kaynak değil.


### H131b — Kişiler listesi arka tazelemesi 2,5 sn olay döngüsünü kilitliyordu (2026-10-28)
- **Çözüm:** `contributionCountsAll(ps)` tek geçişte kimlik/ad dizinleriyle sayar (eşleşme kuralları birebir; 895 kişide sayılar önce/sonra aynı). `/api/admin/people` 2,5 sn → 0,05–0,15 sn. **Kural:** kişi × veri kümesi döngüsü yazılmaz; ters dizin bir kez kurulur.


### H131c — v16 kabuğu her alt yol değişiminde sayfayı yeniden kuruyordu (2026-10-28)
- **Çözüm/kural:** Aynı sayfa içinde yalnız alt yol değişirse sayfa yeniden kurulmaz, odak/kaydırma korunur (aynı adrese yeniden tıklama sıfırlar). Çekmece açma 1 istek (önce liste + ayrıntı).


### H138 — Sekmede açılan görsel/JSON yanıtı site kabuğu diye önbelleğe yazılıyordu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Yalnız `Content-Type: text/html` yanıt kabuğa yazılır; `CACHE_VERSION` v19 kirlenmiş eski kabuğu siler. Kabuk önbelleğine yazan her yol içerik türünü denetler.


### H149 — Aramada "Sesli derste geçen yerler" stilsiz görünüyordu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** İçe aktarma yorumun dışına alındı; depoda aynı kalıp tarandı (başka yok). Belge yorumunun içine kod satırı eklenmez; stil "kural var ama uygulanmıyor" görünüyorsa önce içe aktarmanın gerçekten çalıştığına bakılır.


### H151 — Sağlık Bakanlığı uzun bölümlerinde başa dönüş yoktu; geçmiş düğmesi küçüktü (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** 1200 px aşağıda "Başa dön" düğmesi (kaydırılan kabı olaydan bulur); geçmiş düğmesine `::after` ile ~57×34 dokunma alanı. Not: "Kaynak N" bağlantıları zaten `::after` ile büyütülmüştü, tarama aracı bunu göremez (yanlış bulgu).


### H239–H241 — Ders programı: import.meta.glob anahtarı + numara eşleşmesi (2026-10-28)
- **Kural:** glob kaydını başka dosyadan sorgulama, kaynağın yardımcısını (`programVar`) kullan; ders↔sesli bağlantısı yalnız `ders_id_tam` birebir başlangıcıyla; boş tarih ayrı etiketle.


### H430 — Video oluştur penceresi Ders seçenekleri panelinin altında kalıyordu (2026-10-28, kullanıcı bildirdi)
- **Çözüm/kural:** `Dialog` açılışta panel varsa z 85 (yoksa 70); `ActionMenu` açılır menü/eylem sayfası her zaman z 95 (geçici katmanlar en üstte); `Sheet`, odak panel dışında ve üstte bir `ms-overlay` varken Esc/Tab'ı bırakır. Katman kuralı: panel 80 < panel üstü pencere 85 < açılır menü 95; iç içe açılan katmanda klavye en üstteki katmanındır.


### H436 — Hata defteri tekrar ekranı yan rayın altında (2026-10-29)
- **Çözüm/önleme:** tam ekran katman `createPortal(..., document.body)` ile gövdeye taşındı; v15'te seçili segment vurgu karışımlı. Yeni tam ekran katman `.sh-main` içine değil gövdeye portal edilir.


### H440 — Arka plan işleri boşta da bellek, CPU, internet ve LLM kotası harcıyordu (sistem başarım turu, 2026-10-29)
- **Çözüm:** LLM kilidi `v2/core/llm.py` (`chat`, `vision_ocr`) ve `processQueueItemOtomatik` + zamanlayıcılı `questionIntake`/`poolClusterService` yolları (`MEDS_LLM_OTOMATIK=1` yoksa çalışmaz); `cycle.py` dosya özeti önbelleği (ad+boyut+mtime) + her tur ayrı alt süreç; panel istatistiği yalnız son 60 sn'de istenmişse, Ollama yoklaması kaldırıldı; bekçi 60 sn + yalnız başlık; arama servisleri sorgu vektörünü `meds-embed`'den (:8091, `MEDS_E5_EMBED_URL`) alır, boyut 384 değilse yerel modele düşer; `embed_server.py` model bırakınca `malloc_trim`; birimlere `HF_HUB_OFFLINE=1` (`*.service.d/20-cevrimdisi.conf`); query-intel ucuz ön imza (`data/search/query-intel.onimza`); RAG değişen parça yoksa dizin/dosya yeniden kurulmaz, bekleme 2 dk; Firestore yedek yoklaması canlı dinleyici varken 10 dk; istemci saat yalnız çalarken, bakım yoklaması yalnız görünür sekmede, SW mühürleme günde bir, başarım yoklaması 10 dk, müzik listesi ilk bağlanmada tekrar çekilmez. `meds-web` doğrudan `node --import tsx server.ts` (`30-dogrudan-node.conf`).
- **Önleme:** (a) Sürekli çalışan servis tur başına değişmeyen girdiyi baştan okumaz/özetlemez: önce ad+boyut+mtime ön imzası. (b) Ağır son işlemi olan uzun ömürlü Python döngüsü işi alt süreçte yapar (bellek tur sonunda iade). (c) Yalnız ekran açıkken anlamlı olan hesap (panel istatistiği, saat, yoklama) "son istek/görünürlük" koşuluna bağlanır. (d) LLM çağıran HER yol — en alt katmandaki ortak `chat` işlevi dahil — kilidi denetler; yalnız zamanlayıcıyı duraklatmak yetmez. (e) Aynı modeli taşıyan ikinci servis yazılmaz; ortak vektörleme servisine istek atılır. (f) Kaldırılan servisin (Ollama vb.) yoklaması panel/bekçi kodundan da silinir.

