# Aşama kuralları — genel

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/hat/tam_hat/kural_secici.py`. 29 madde. Ayrıntı gerekirse madde başlığıyla defterde aç.

### H39 — Sesli metin kısaydı: sayfa atlanıyor, şekiller anlatılmıyordu (2026-10-24, kullanıcı "ders süresi az")


### H45 — Dar bölmede panel slayta göre büyüyor, yazının üstüne biniyor, kelimeler harf harf kırılıyordu (2026-10-24)


### H47 — Kelime takipçisi küçük yazıyı okunmaz yapıyordu; ek alan gereğinden sık ve uzundu (2026-10-24)


### H68 — H66 tekrarı + süs bölüm sayfaları `sekil` türünde (2026-10-26, k2-27 periyodik muayeneler)
- **Çözüm / kural:** Çıkmışlar `kanit.sayfa` cümlelerine bağlandı (c0003, c0037, c0047, c0101, c0112, c0204, c0213, c0218, c0222) ve sesli uyarı eklendi; süs bölüm sayfaları `tur: kapak` yapıldı. Haritacı, bilgi taşımayan bölüm başlık/kapanış sayfalarını `kapak` yazar; sesli yazar H66 adımını atlamaz. Kapı gevşetilmedi.


### H100 — Asklepios kutlama efekti görünmüyordu (2026-10-27)
- **Kural:** ortada çizilen efekt kartın altında kalmaz; kartı örtmeyen konuma (iki yan) çizilir ve canvas kart üstüne (`is-ust-katman`) alınır. Yeni kutlama efektini canlı kartla birlikte gör.


### H106 · `baglam.kazanimlar` kapak metninden türetilmiş çöp şablon cümleler içeriyor (2026-10-27, k2-08)
- **Kural:** Genel şablon ("temel kavramlarını … analiz eder") ya da kapak metni içeren kazanım kullanılmaz. Açık iş: `isle.kazanimlar` kayıt yoksa boş dönmeli (kod düzeltmesi bu turda yapılmadı).


### H109 · v2 cümlesinin `ses` alanında iç cümle sonu: sunucu cümle sayısı v2 ile tutmuyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Kural:** her v2 `ses` tam bir cümledir; yazım betiğinde ayrıca kendi sınır kontrolü (cümle sayısı = 1, ≤25 kelime) çalıştırılır.


### Sesli derste geri oku "Ders çalış"a atıyordu (2026-10-27)
- **Çözüm / kural:** Uygulama içinden gelindiyse (`navigateTo` `__icGezinti` bayrağını koyar) ok `history.back()` yapar; doğrudan bağlantıyla açıldıysa ayrıntı sayfasına gider. Geri düğmeleri sabit hedefe değil, geldiği yere dönmelidir.


### Sesli derste canlı konum bazen çalışmıyor / bozuk çalışıyordu (2026-10-27)
- **Çözüm / kural:** Eksik öğede kısa aralıkla yeniden dene; sıfır boyutta kaydırma yapma; 3 px altı scroll farkını kullanıcı eylemi sayma. Yeni takip/kaydırma kodu bu üç durumu karşılamalı.


### H117 · Tam ekranda ayar düğmesi araç şeridini göstermiyordu (2026-10-27)
- **Çözüm/kural:** tam ekran şeridinde `container-type: normal; width: max-content`; seçici düzeltildi. Mutlak konumlu öğeye `container-type: inline-size` verilirse genişlik açıkça verilir; `:is()` içinde başa combinator yazılmaz.


### H106 · Çalışma takvimi (ısı haritası) hücreleri dev görünüyordu (2026-10-27)
- **Kural:** Kare hücreli ızgaralarda (ısı haritası, takvim) sütun genişliğine üst sınır koy; `1fr` + `aspect-ratio` birlikte kullanılmaz.


### H111e · Profil verisi dinleyicileri render sırasında setState yapıyordu (2026-10-28, Bugün/Arka plan)
- **Kural:** localStorage/depo yazımına bağlı olay yayıcıları dinleyicileri eşzamanlı çağırmaz (mikro görev); render içinde (useState başlatıcısı, useMemo) yan etkili yazım yapılmaz.


### H129 — "Salt okunur" SQL konsolu süper kullanıcıyla çalışıyordu (2026-10-28, Yönetim v16)
- **Önleme:** "salt okunur" iddia eden her uç bağlantı rolünün yetkisiyle sınanır (COPY TO PROGRAM, pg_read_file, pg_authid, CTE içinde DELETE); tehlikeli uçlar istemci onayına ek olarak sunucuda onay sözcüğü ister.


### H130 — Canlı içerik katmanı tam kopyaydı, kaynaktaki yeni kayıtları gölgeliyordu (2026-10-28)
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
- **Önleme:** (a) Sürekli çalışan servis tur başına değişmeyen girdiyi baştan okumaz/özetlemez: önce ad+boyut+mtime ön imzası. (b) Ağır son işlemi olan uzun ömürlü Python döngüsü işi alt süreçte yapar (bellek tur sonunda iade). (c) Yalnız ekran açıkken anlamlı olan hesap (panel istatistiği, saat, yoklama) "son istek/görünürlük" koşuluna bağlanır. (d) LLM çağıran HER yol — en alt katmandaki ortak `chat` işlevi dahil — kilidi denetler; yalnız zamanlayıcıyı duraklatmak yetmez. (e) Aynı modeli taşıyan ikinci servis yazılmaz; ortak vektörleme servisine istek atılır. (f) Kaldırılan servisin (Ollama vb.) yoklaması panel/bekçi kodundan da silinir.


### H457 — Sesli ders "İndir" düğmesi indirmeyi hiç başlatmıyordu (çevrimdışı, 2026-10-31)
- **Önleme:** tarayıcıya devredilen bir indirme/iş, ilerleme gelmezse zaman aşımıyla sayfa içi yola düşmeden kullanılmaz;
  çevrimdışı içerik kullanıcının dosya sistemine değil uygulama önbelleğine yazılır.


### H478 — LLM kilidi masaüstü Claude oturumunu zamanlayıcı sandı (2026-11-03)
- **Önleme:** ajan kilidi kendi başına aşmaz; takılırsa ana oturum kullanıcıya sorar. Kalıcı çözüm kullanıcı kararı bekler: kilidin yalnız
  `claude()`/`anlam_denetimi()` çağrısına taşınması ya da masaüstü oturumunu tanıyan ayrı bayrak (kilit gevşetme sayılır → kullanıcı onayı şart).


### H481
- **Önleme:** bir isteği SW'den "ağa bırakan" her kısa devre, o adresi yazan TÜM önbellekleri (paket, sesli ders, eski PDF) önce denetlemelidir;
  çevrimdışı düzeltmesi internetsiz gerçek sınamayla doğrulanmadan bitmiş sayılmaz.


### H484
- **Önleme:** systemd-run ile geçici birim açan her betik adı süreçten tekil kurar (pid ya da uuid); zaman damgası tek başına kimlik sayılmaz.


### H493
- **Önleme:** tek bilgi taşıyan satır asla tek satır üç noktaya düşürülmez; en dar kapsayıcı genişliğinde ekran görüntüsüyle denetlenir.


### H494
- **Önleme:** `body/documentElement.style.overflow`'a doğrudan yazmak yasak; yalnız `utils/scrollLock`. Denetim: `grep -rn "body.style.overflow\s*=" src` boş dönmeli.

