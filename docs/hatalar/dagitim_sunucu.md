# Hata defteri — dagitim_sunucu (dağıtım, Oracle, sunucu, önbellek/SW, çevrimdışı, kimlik)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

### H6 — Birleştirici ders/dosya siliyor
- **Kök:** toptan yeniden yazım; reddedilen ders siliniyordu (patoloji asistanı, s13/s15/s16).
- **Kural:** birleştirici yalnız ekler/günceller; reddedilen ders eski hâliyle kalır.
- **Kapı — EKLENDİ:** `ders_zinciri.korumali`: ders sayısı düşerse ya da öğe sayısı %10'dan fazla azalırsa yedek geri konur (kod 11). Silen, küçülten ve ekleyen durumlar sınandı.

### H14 — Sunucu kodu Oracle'da ama çalışan sunucu eski kodla (yeni uç sitenin ana sayfasını döndürüyor)
- **Kök:** yeniden başlatma kararı "bu dağıtımda değişen dosyalar"a bakıyordu; dosya Oracle'a başka yoldan (tek dosya rsync,
  başka oturum) yeniden başlatmasız gelmişti, rsync saat damgasını da koruyor (2026-10-20: kamp uçları yüklenmemişti).
- **Kapı — EKLENDİ:** `deploy-code.sh` Oracle'daki sunucu kodunun içerik karmasını, son yeniden başlatmada yazılan
  `.sunucu_kod_karma` ile karşılaştırır; farklıysa yeniden başlatır. Yeni uç ekleyen iş, dağıtımdan sonra ucu canlıda dener.

## H37 — Oracle'da yayın/işaret yazamıyordu: sahiplik (2026-10-24)
- 16 Ekim'den beri hiçbir ders yayınlanamıyordu: `src/data` uid 1000 (`opc`, cihazdan `rsync -a` sahipliği), `data/sesli_anlatim`
  `root` (meds-app konteyneri ve `sudo rsync`); yayın ve işaret hizmetleri `ubuntu`. Düzeltme (kullanıcı onayı): `ubuntu` → `opc`
  grubu; sesli ders aktarımlarına `--chown=ubuntu:ubuntu`; `meds-ders-yayin` ve `meds-cumle-zaman` drop-in
  `ExecStartPre=+chown -R ubuntu:ubuntu data/sesli_anlatim` (konteyner root yazmaya devam eder).

## H56 — Yeni yayınlanan dersin PDF'i uygulamada açılmıyordu (2026-10-24, kullanıcı, k2-07)
- Deste → PDF eşlemesi (`build_deck_pdf_sources.py` → `meds_downloads/_deck_pdf_sources.json`) yalnız işçinin Drive
  taramasında (50 dk) yenileniyordu; k2-07 21:47'de yayınlandı, eşleme 21:14'tendi → ders PDF'siz. PDF sunucu diskinden
  verilir (`/api/lecture-pdf/deck/<deste>/<n>`); Drive yalnız sunucusuz yedek yoldur.
- Düzeltme: `yayinla.py` yeni ders yayınlayınca `_pdf_eslesme_yenile()` → işçi kapsayıcısında `izle.pdf_eslesme_guncelle()`
  (günlükte "PDF eşleşmesi: yenilendi"). Kapı: yayından sonra `/api/lecture-pdf/deck/<deste>/0` 200 dönmeli.
- `.medspak` öğrenci paketi PDF taşımaz (tasarım: `ek` yalnız `--ekler` yönetici dışa aktarımında); uygulama PDF'i paketten değil sunucudan açar.

## H63 — Sesli Derslerde Arşiv PDF'lerinin Çok Geç Yüklenmesi veya Hiç Yüklenmemesi (AutoFetch, SW Range ve Linearization Hatası) (2026-10-26, kullanıcı)

- **Belirti:** Sesli derslerde 2025-2026 arşivi açıldığında slayt PDF'leri ya dakikalarca yüklenmiyor (uzun süre `%...` ilerleme çubuğunda bekliyor) ya da hiç yüklenmiyor (Cloudflare tunnel `context canceled`, zaman aşımı veya boş ekran).
- **Kök Neden:** 
  1. `PdfDocView.tsx` içinde `disableAutoFetch: !(boyut > 0 && boyut <= 15 * 1024 * 1024)` kuralı nedeniyle 15 MB altındaki tüm PDF dosyalarında autoFetch açık kalıyordu. PDF.js, ilk sayfa için range isteği atmak yerine arka planda bütün 5-15 MB'lık dosyanın stream indirmesini başlatıyor ve ilk sayfa çizimi bu dev stream bitene kadar bloke oluyordu.
  2. `public/sw.js` dosyasında ses akışları (`/api/canli-ders/ses/` vb.) Range/206 muafiyetindeyken `/api/lecture-pdf/` akışları bu listeye eklenmemişti. İstemci çevrimdışı paketini indirmediğinde istek SW'nin genel `/api/` Network-First bloğuna düşüyor; Service Worker Range isteklerini `fetch(req)` ile yakalayıp tarayıcının yerel Range motorunu bozuyor ve dönen yanıtları `DATA_CACHE`'e yazmaya çalışarak iş parçacığını kilitliyordu.
  3. Arşivdeki PDF dosyalarının hiçbiri linearize (Fast Web View) formatında değildi (0/65). Linearize olmayan PDF'lerde katalog ve xref tablosu dosyanın sonunda olduğu için autoFetch ile yarışan range istekleri zaman aşımına uğruyordu.
  4. Sunucu `Accept-Ranges: bytes` ve `public, max-age=604800, stale-while-revalidate=86400` başlıklarını eksik döndürdüğünden CDN ve ara katmanlar byte-range parçalarını önbellekleyemiyordu.
- **Çözüm & Kural:**
  1. `PdfDocView.tsx`: `disableAutoFetch: true` ve `rangeChunkSize: 256 * 1024` sabitlendi. PDF.js artık asla tüm dosyayı arka planda otomatik çekmez; yalnızca o an görüntülenen sayfanın 256 KB'lık dilimini çeker ve ilk sayfa 1 saniyenin altında ekrana gelir.
  2. `public/sw.js`: `/api/lecture-pdf/` akışları Service Worker tamponlama ve cache mekanizmasından tamamen muaf tutularak (`return;`) doğrudan tarayıcının yerel yüksek hızlı ağ motoruna bırakıldı (`SW v16`).
  3. `pikepdf` motoru ile tüm arşiv PDF'leri linearize edildi (Fast Web View); ilk sayfa ve xref tablosu dosyanın ilk kilobaytlarına taşındı.
  4. `server.ts`: `/api/lecture-pdf/deck/:deckId/:index` için `Accept-Ranges: bytes` ve `public, max-age=604800, stale-while-revalidate=86400` başlıkları eklendi.




## H73 — `terim/` klasörü dağıtım betiğinin veri listesinde yoktu; terim dosyaları canlıya ulaşamıyordu (2026-10-26)
- **Belirti:** Terim yardımcısı yerelde çalışıyor, canlıda `/api/canli-ders/...` yanıtında `terim` alanı hiç gelmiyordu (k2-02, k2-07 dahil tüm dersler).
- **Kök neden:** `deploy-code.sh` ana rsync'i `/data` klasörünü dışlıyor; `data/sesli_anlatim` altındaki klasörler [1b] adımındaki sabit listeden aktarılıyor. Liste `metin hizalama vurgu capa cizim ogrenci_not cikmis_konum` idi ve `terim` eklenmemişti; yeni bir veri türü eklenirken dağıtım listesi güncellenmemişti.
- **Çözüm / kural:** Listeye `terim` eklendi. `data/sesli_anlatim` altına yeni bir veri türü ekleyen her oturum, `deploy-code.sh` [1b] listesini de günceller; dağıtımdan sonra canlı API yanıtında alanın varlığı `curl` ile doğrulanır.

## H88 — Drive klasör adı değişince yayın PDF'in kaynak kimliğini bulamadı (2026-10-27, k2-03)
- **Belirti:** onaylanan k2-03 taslağı Oracle yayınında "PDF'in kaynak kimliği (manifest) bulunamadı" ile durdu (hiçbir şey yazılmadı).
- **Kök neden:** okul Drive'ında klasör "Patoloji" → "Tıbbi Patoloji" olarak yeniden adlandırılmış; dosya diskte eski yolda,
  manifest yeni yolda ("…/ Herniasyon .pdf", '/' içeren ad). Sunucu kipi yalnız birebir yol eşleyen `kaynak_kimligi`'ni kullanıyordu.
- **Çözüm / kural:** sunucu ve deneme kipi `kaynak_kimligi_esnek` kullanır; esnek eşleme klasör farkını yok sayıp `Kurul N/<branş>/`
  sonrası yol manifestte tekse onu kabul eder. Yayın denetim hatasında taslağın `yayin.json`'u silinip yeniden onaylanır.

## H95 — Yayın düzeltmesinde olmayan alan; PDF eşleyici durdurulan işçi kapsayıcısında (2026-10-27, k2-03/k2-04)
- **Belirti:** `meds-ders-yayin` her 10 dakikada `AttributeError: 'Yayin' object has no attribute 'ders_id'`; yayından sonra
  "PDF eşleşmesi: container … is not running" ve deste PDF'i 404.
- **Kök neden:** H88 düzeltmesindeki lambda `y.ders_id`'yi `denetle()` öncesi okuyordu (alan orada atanır); PDF eşleyici
  `docker exec meds-ders-isci` ile çalışıyor, LLM yasağıyla durdurulan kapsayıcıda koşamıyor.
- **Çözüm:** `y.b.get("ders_id")`; PDF eşleme tek seferlik `docker run --rm -u 1001:1001 --entrypoint python3 medsoru-isci:latest`
  (aynı bağlar, LLM anahtarı yok) ile; deste PDF'i 200 doğrulandı.
- **Önleme kuralı:** yayın betiği değişikliği Oracle'a gitmeden önce yerel taslakla `kaynak_kimligi_esnek` ve `--deneme` akışı
  çalıştırılır; yayından sonra `/api/lecture-pdf/deck/<deck>/0` 200 kontrolü zorunlu.

## H97 — Dağıtım, yeni sesli ders metnini git'teki eski sürümle geri aldı; ses eski metinle üretildi (2026-10-27, k2-03/k2-04)
- **Belirti:** ders-ekle "metinDegisti" döndü ama Oracle'da metin 08:18'deki eski sürümdü; k2-04'ün yeni EMA varyantı eski metnin süresiyle (1609 sn) çıktı; doğrulayıcı eski 65 paragrafı gördü.
- **Kök neden:** `dagit.sh` git'teki sesli_anlatim verisini Oracle'a eşitler; yeni metin git'e işlenmeden ders-ekle yapılınca (başka oturumun dağıtımı dahil) canlı metin eski commit'e döner. EMA işi metni çalışırken Oracle'dan okur.
- **Kural:** yeni metin + v2 + vurgu + hizalama önce commit/push, sonra ders-ekle; ses tamamlanınca eski metne ait varyantlar silinir (`DELETE /api/sesli-anlatim/ses/<key>/<vid>`); `kayit.json` süre/özet ve `takip_kapisi --api` ile doğrulanır.

## H99 — Dağıtım sunucu servis değişikliğini "yalnız ön yüz" sandı; yeni data dosyası Oracle'a gitmedi (2026-10-27, sınama)
- **Belirti:** `src/services/canliDers.ts` değişikliği ve `data/sinama.json` dağıtıldıktan sonra canlı API eski davranışı sürdürdü.
- **Kök neden:** `dagit.sh` bu değişiklikte uygulamayı yeniden başlatmadı ("yalnız ön yüz/statik"); `data/` altındaki yeni dosya eşitlenmedi.
- **Kural:** sunucu kodu değişen dağıtımdan sonra `curl` ile yeni davranış doğrulanır; gerekirse `docker restart meds-app` ve sağlık kontrolü. Yeni `data/*.json` dosyası Oracle'a elle (`scp` + `sudo cp`) kopyalanıp canlıda okunduğu doğrulanır.

## H116 · Birleştiriciler yeni ders eklerken branştaki eski dersin dosyalarını da yeniden yazıyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Belirti:** `birlestir.py k2noroloji --taslak` ve `asistan_birlestir.py k2noroloji` sonrası `git status`ta k2-02'nin (2n02) önem/çözücü/asistan
  dosyaları ve indeks satırları değişmişti (önem `cikmis`, çözücü/asistan `klip` alanı, asistan indeksinde `ses`/`sure`); k2-02'ye dokunulmamıştı.
- **Kök neden:** birleştiriciler branştaki TÜM dersleri çalışma klasöründen ve yerel ses dosyalarının o anki durumundan yeniden üretir.
  `korumali` yalnız içerik küçülmesini (%10) yakalar, başka dersin içerik farkını değil.
- **Kural:** elle zincirde her birleştirmeden sonra `git diff --stat`; yalnız yeni dersin dosyaları ve indeksteki yeni ders satırı sahnelenir;
  eski dersin dosyaları `git checkout` ile geri alınır, indekste eski ders satırı HEAD'den korunur (bilerek yapılan toplu yenileme hariç).

## H129 — "Salt okunur" SQL konsolu süper kullanıcıyla çalışıyordu (2026-10-28, Yönetim v16)
- **Belirti:** Yönetim › Veritabanı gezgini SQL konsolu "salt okunur" diye sunuluyordu; READ ONLY işlem içinde `COPY … TO PROGRAM`, `pg_read_file`, `pg_authid` (parola özetleri) okunabilir durumdaydı.
- **Kök neden:** `DATABASE_URL` kullanıcısı `meds` süper kullanıcı; `begin read only` yalnız tablo yazımını engeller, COPY TO / dosya ve süreç işlevleri READ ONLY işlemde serbesttir.
- **Kalıcı çözüm:** `pgAdminRoutes.ts` `/api/admin/pg/sql`: ilk sözcük izin listesi (SELECT/WITH/EXPLAIN/VALUES/TABLE/SHOW), tehlikeli işlev/katalog yasak listesi, işlem içinde `set local role meds_salt_okur` (NOLOGIN, yalnız `pg_read_all_data`). Rol kurulamazsa konsol kapalı (503). `DELETE /api/admin/pg/row` ve `POST /api/admin/db/import` sunucuda onay sözcüğü ister.
- **Önleme:** "salt okunur" iddia eden her uç bağlantı rolünün yetkisiyle sınanır (COPY TO PROGRAM, pg_read_file, pg_authid, CTE içinde DELETE); tehlikeli uçlar istemci onayına ek olarak sunucuda onay sözcüğü ister.

## H130 — Canlı içerik katmanı tam kopyaydı, kaynaktaki yeni kayıtları gölgeliyordu (2026-10-28)
- **Belirti:** Kaynakta (`src/data/interactive_learning_decks.json`) duran yeni k2p desteleri (7 deste) yerel sunucunun kataloğunda/ders ayrıntısında görünmüyordu; sözlükte kaynağa sonradan eklenen 383 terim de sunucudan gelmiyordu.
- **Kök neden:** `contentOverlay.ts` panel yazımında dosyanın TAMAMINI `data/content/<rel>`'e kopyalıyor, `resolveContent` katman dosyası varsa kaynağa hiç bakmıyordu. 20.10'daki tek alanlık panel düzenlemeleri (yalnız `updatedAt`) 81 MB'lık deste kopyası bıraktı; sonraki tüm kaynak güncellemeleri (yeni desteler, sözlük terimleri, 44 güncellenen terim) gölgede kaldı. Dağıtım eşitlemesi de tam kopya varsayıyordu.
- **Kalıcı çözüm:** Katman kayıt düzeyinde farktır: `data/content/<rel>.fark.json` (`kayitlar`, `silinen`, kaynaktaki kaydın sha'sı `taban`). Okuma = kaynak + fark (`_birlesik/<rel>` önbelleği). Yazıcılar tam dosyayı yine `writableContent` yoluna yazar; kilit bırakılınca birleşik tabana göre farka çevrilir. Eski kopyalar `scripts/icerik_katman.py goc` ile `_ids.json` izine göre farka çevrildi (yedek `data/_yedek/content_goc_*`). `content-overlay-sync.sh` farkı kayıt kayıt uygular, `taban` tutmazsa durur, tam kopya görürse durur.
- **Önleme:** `python3 scripts/icerik_katman.py denetle` 0 HATA (tam kopya = HATA, birleşimde kaynak kaydı eksik = HATA). Katmana bütün dosya kopyalayan yeni yazıcı yazılmaz; başlangıç kopyası gerekiyorsa `resolveContent(file)` (birleşik) kopyalanır, ham kaynak değil.

## H138 — Sekmede açılan görsel/JSON yanıtı site kabuğu diye önbelleğe yazılıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Önizleme tarayıcısında `/` ve `/bugun` site yerine yalnız favicon gösterdi; bir dosya adresini doğrudan açan öğrencide yavaş ağda sonraki açılışlar site yerine o dosyayı verir.
- **Kök neden:** `sw.js` gezinme işleyicisi 200 dönen her `navigate` yanıtını içerik türüne bakmadan `/` ve `/index.html` olarak yazıyordu; 0,4 sn içinde ağ yanıtı gelmezse kabuk diye o kayıt veriliyordu.
- **Çözüm/kural:** Yalnız `Content-Type: text/html` yanıt kabuğa yazılır; `CACHE_VERSION` v19 kirlenmiş eski kabuğu siler. Kabuk önbelleğine yazan her yol içerik türünü denetler.

## H437 — Çevrimdışı indirme "sırada" takılıyor, her açılışta uygulama dosyası iniyor (2026-10-29)
- **Belirti:** Çevrimdışı ekranında paketler sürekli "sırada" bekliyor ya da hiç inmiyor; her açılışta "Uygulama dosyaları iniyor".
- **Kök neden:** (1) `net.ts::onPlanBosalinca` her dosyadan önce "uçuşan ön plan isteği yok VE son 1,5 sn'de istek başlamadı" koşulunu 20 sn'ye dek bekliyordu; saniyede yoklayan ekranlar (varlık, SSE telafisi, sayaçlar) yüzünden her dosya ~20 sn bekledi — yüzlerce dosyalı paket saatler sürdü. (2) `paketMotoru.otomatikTur` cihazda herhangi paket varsa ve `kuyrugaEkle` içerik eklenirken uygulama paketi `guncelleme` durumundaysa onu kuyruğun BAŞINA koyuyordu; her dağıtımda (onem+1) sürüm değiştiği için her açılışta uygulama yeniden indi, içerik onun arkasında bekledi.
- **Çözüm:** bekleme yalnız uçuşan ön plan isteğine ve en çok 2 sn; uygulama paketi yalnız cihazda yokken içerikle birlikte başa, güncellemesi yalnız çevrimdışı mod + otomatik güncelleme açıkken kuyruğun sonuna.
- **Önleme:** arka plan indirmesinde dosya başına bekleme süresi toplam süreyi paket boyuyla çarpar — bekleme paket başına değil dosya başınaysa üst sınır saniyeler düzeyinde tutulur; sürüm değişimi her dağıtımda olan bir paket kuyruğun önüne zorla alınmaz.

## H441 — Sesli ders listesi (`/api/canli-ders`) canlıda her açılışta 1,2 sn (2026-10-29)
- **Belirti:** Canlı sitede açılışta `/api/canli-ders` dışarıdan 1,7–1,9 sn, Oracle içinde bile 1,18 sn; öteki uçlar 2–15 ms.
- **Kök neden:** `src/services/canliDers.ts` liste ucu her ders için `varyantlar()` → `oku(kayit.json)` çağırıyordu: 810 KB'lık kayıt defteri 153 kez baştan ayrıştırılıyordu (istek başına ~120 MB JSON). `sinama.json` ve `dersler/kN.json` de ders başına yeniden okunuyordu.
- **Çözüm:** salt okunur kayıt defterleri için boyut+mtime önbellekli `okuSabit` (dersler, dersBul, varyantlar, sinamaKonfig, branş kaydı). Dört sorgu biçiminde çıktı önce/sonra bayt bayt aynı; yerelde 270–380 ms → 4 ms.
- **Önleme:** İstek başına döngü içinde dosya okuyup ayrıştırma yapılmaz; değişmeyen kayıt defteri bir kez okunur, imza (boyut+mtime) değişince tazelenir. Önbellekten dönen nesne değiştirilmez (yazan kod taze `oku` kullanır). Yeni liste ucu eklerken Oracle içinden `curl -w %{time_total}` ile ölçülür (hedef < 50 ms).

## H457 — Sesli ders "İndir" düğmesi indirmeyi hiç başlatmıyordu (çevrimdışı, 2026-10-31)

- **Belirti:** Çevrimdışı merkezinde ya da derste "İndir" denince ilerleme %0'da kalıyor, ders cihaza inmiyordu.
- **Kök neden:** `cdCevrimdisiAyarla` önce tarayıcının Background Fetch indiricisini deniyordu. Chrome bu işi tarayıcının
  "İndirilenler" akışına koyar; otomatik indirme izni beklenirken kayıt `result: ''` hâlinde sonsuza dek bekler, hiç
  `progress` gelmez. Kod bu sözü zaman aşımsız bekliyor, sayfa içi indirmeye düşmüyordu; `bf.get(id)` aynı takılı kaydı
  her yeni denemede geri verdiği için tekrar basmak da işe yaramıyordu.
- **Çözüm:** Background Fetch kapatıldı (`BF_ETKIN = false`, `canliDersCevrimdisi.ts`); ses, metin ve PDF yalnız sayfa içi
  `fetch` ile uygulamanın önbelleğine (Cache Storage, `CD_OFFLINE_CACHE`) yazılır; indirilenler klasörüne dosya düşmez.
  `cdTakiliArkaPlanIptal()` eski takılı `cd|…` kayıtlarını açılışta ve her indirmede iptal eder.
- **Önleme:** tarayıcıya devredilen bir indirme/iş, ilerleme gelmezse zaman aşımıyla sayfa içi yola düşmeden kullanılmaz;
  çevrimdışı içerik kullanıcının dosya sistemine değil uygulama önbelleğine yazılır.

## H466 — Google/Firebase projesi askıya alındı: kimse giriş yapamadı, site fiilen kapandı (2026-11-02)

- **Belirti:** Kullanıcı girişi (Google ile ve e-posta+şifre) çalışmıyordu; site zorunlu giriş kapısında kaldığı için
  öğrenciler hiçbir sayfayı açamadı. Oracle `meds-app` günlüğünde her dakika
  `PERMISSION_DENIED: Consumer 'projects/990828780858' has been suspended` (Firestore dinleyicisi) satırı vardı.
- **Kök neden:** Veriler 2026-10-12'de meds-pg'ye taşınmış, Firestore bayrakla kapatılmıştı; ama **kimlik** hâlâ tamamen
  Google'a bağlıydı: istemci Firebase Auth SDK'sıyla giriş yapıyor, sunucu her jetonu Google Identity Toolkit
  (`accounts:lookup`) ile doğruluyordu (`firebaseIdentity.ts`). Ayrıca sunucuda `CloudNotificationBridge` Firestore'u
  dinlemeye devam ediyordu. Tek dış sağlayıcının askıya alınması tek hata noktasıydı.
- **Çözüm:** Kendi kimlik sistemi: `src/services/yerelKimlik.ts` (hesap/oturum/kod uçları `/api/kimlik/*`, şema
  `deploy/pg/sql/kimlik.sql`, scrypt şifre özeti, özetli yenileme jetonu, 6 haneli e-posta kodu, hız sınırı),
  `src/services/kimlikDogrulama.ts` (HMAC-SHA256 erişim jetonu, ağsız doğrulama), istemci `src/services/auth.ts`
  (Firebase Auth benzeri `auth` nesnesi; çağıranlar değişmedi). Eski hesaplar **aynı uid** ile taşındı (users +
  doğrulanmış user_data e-postaları); şifreleri bilinmediği için kullanıcı bir kez kodla şifre belirler. Firestore köprüsü,
  `firebase` paketi, Firebase yapılandırma dosyaları ve Firebase'e yazan eski betikler (arşive) kaldırıldı; Google girişi,
  Firebase alan adı uyarısı ve Drive'a otomatik yedek kalktı.
- **Önleme:** Kimlik, veri, yedek ve canlı yayın yalnız Oracle'da (meds-pg + sunucu). Yeni özellik dış bir hesaba bağlı
  **zorunlu** bir yol (giriş, veri yazımı, yedek) açamaz; dış servis yalnız kesilince sitenin çalışmaya devam ettiği
  isteğe bağlı ek olabilir (yazı tipi, LLM gibi). Jeton doğrulaması ağ çağrısı yapmaz. Kimlik e-postası (kod) SMTP'ye
  bağlıdır; SMTP gitmezse yönetici Kullanıcılar › Erişim › "Şifre kodu üret" ile 24 saatlik kod verir.

## H467 — Taşınan hesaplar için e-postaya bağlı şifre belirleme tek yoldu; Drive'da ölü servis hesabı yedeği (2026-11-02)

- **Belirti:** Kullanıcı: şifresi Google'da kalan öğrenci yeni şifreyi e-posta olmadan, yönetici onayıyla belirleyebilmeli;
  e-posta ya da öğrenci no + şifreyle girebilmeli. Drive denetiminde: servis hesabı yedeği `invalid_grant: account not
  found` (askıdaki `gen-lang-client-0056595657` projesi), sınav kitapçığını Drive'a yükleme Google girişi olmadan çalışmıyor.
- **Kök neden:** H466'daki ilk çözüm şifre belirlemeyi yalnız e-posta koduna bağladı; e-posta da bir Google hesabından
  (Gmail SMTP) gidiyordu, yani aynı tek hata noktası. Giriş yalnız e-postayla yapılıyordu. Drive indirmesinin yedeği
  askıdaki projeye bağlıydı ve hata sessiz geçiyordu.
- **Çözüm:** `auth_sifre_talepleri` + `/api/kimlik/sifre-talebi(/durum)` + yönetim › Kullanıcılar › **Şifre talepleri**
  (talepteki ad/no kayıtlı profille yan yana, eşleşme rozetleri; onay talepteki şifre özetini hesaba yazar, talep eden cihaz
  bir kez kendiliğinden oturum alır, uid değişmez). Girişte e-posta ya da öğrenci no (`auth_hesaplar.ogrenci_no`, yoksa
  `users.student_number`; numara birden çok hesaptaysa e-posta istenir). Drive: `02-download.mjs` ikinci herkese açık yol
  (`drive.google.com/uc`) + virüs taraması onay sayfası (uuid) + servis hesabı hatası bir kez açıkça yazılır; Drive'a
  yükleme kaldırıldı (PDF indirme kaldı), eski `medsoru_drive_token` silinir; `/api/admin/ogrenci-drive/indir` hedef yolu
  izinli kökle sınırlı. SMTP ekranı: sağlayıcıyı sunucu adı belirler, port değişince `secure` porttan çıkarılır,
  "Bağlantıyı sına" e-posta göndermez, Google dışı hazır sağlayıcılar.
- **Önleme:** Hesap kurtarmanın en az bir yolu hiçbir dış hesaba bağlı olmamalı (yönetici onayı). Bir dış servisin yedeği
  çalışmıyorsa sessiz geçilmez, günlüğe bir kez yazılır. İçerik alımı herkese açık Drive yoluyla çalışır; kimlikli yedek
  için kullanıcı askıda olmayan bir hesapta yeni servis hesabı ya da `rclone config reconnect meds:` kurmalıdır.

## H471 — Yeni Kurul 2 derslerinde PDF açılmadı, PDF işareti atlandı (2026-11-02)

- **Belirti:** `/api/lecture-pdf/deck/<deste>/0` 404; Oracle'da `pdf_isaret.py` "atlandı (hizalama/PDF/metin uyuşmuyor)"; yerel
  `yayinla.py --yerel` "PDF'in kaynak kimliği (manifest) bulunamadı".
- **Kök neden:** Elle (işçisiz) üretimde PDF'ler `meds_temp/ogrenci_ders/<ders>/` altına indiriliyor; ders işçisinin yaptığı üç
  adım atlanıyor: `meds_downloads/_manifest.json` kaydı, `drive_root/<yol>` kopyası (yerel + Oracle) ve `deckPdfSources.json`
  yeniden üretimi (yeni deste yayından SONRA). Ayrıca Oracle `data/sesli_anlatim/isaret/` root sahipliğindeydi; `pdf_isaret`
  ubuntu kullanıcısıyla yazamadı.
- **Çözüm:** dört PDF manifeste (source_id = sha1(drive_id)[:12]) ve iki drive_root'a eklendi; `build_deck_pdf_sources.py` deste
  yayınından sonra çalıştırıldı (k2-06 ilk koşuda destesinden önce koştuğu için ikinci kez); isaret dizini ubuntu'ya verildi.
- **Önleme:** Elle hatta yayın sırası: PDF → manifest + iki drive_root → `yayinla.py --yerel` → `build_deck_pdf_sources.py`
  (bütün desteler yayınlandıktan sonra) → commit/dağıtım → `ders-ekle`. Dağıtımdan sonra `/api/lecture-pdf/deck/<deste>/0` 200
  denetlenir.

## H474 — Bu yılın PDF'inden üretilen Farmakoloji dersi öğrenciye görünmedi (2026-11-02)
- **Belirti:** kullanıcı: "farma dersi erişilebilir değil, kullanıcılar göremiyor". `k2-09-sss-ilaclari` sesli ders listesinde yoktu,
  yalnız `?donem=sinama`'da "SINAMA — test verisi" etiketiyle duruyordu.
- **Kök neden:** `data/sinama.json` branş kuralı (`brans: ["Tıbbi Farmakoloji"], kurulMin: 2`) geçen yılın slaytından kurulan
  k2-07 için konmuştu; kural branş düzeyinde olduğu için bu yılın PDF'inden tam hatla üretilen k2-09'u da kendiliğinden sınamaya
  aldı. §9-A3 sınıflandırması yayından önce sorgulanmadı. İkinci tuzak: `data/` git'te olsa da `dagit.sh` onu Oracle'a taşımaz
  (konteyner `data/`yı ayrı bağlar) — commit sonrası canlı değişmedi, dosya elle kopyalandı.
- **Çözüm:** branş kuralı kaldırıldı, sınama yalnız `anahtarlar: ["k2-07-genel-anestezik-ilaclar"]`; dosya Oracle'a kopyalandı,
  `/api/canli-ders` listesinde k2-09 var, `sinama` alanı yok (onem 625).
- **Önleme:** Sınama yalnız anahtar listesiyle verilir (branş kuralı yok). Yeni ders yayınında §6 doğrulaması güncel listede
  (`/api/canli-ders`, `donem` yok) dersin anahtarını arar; yoksa yayın bitmiş sayılmaz. `data/*.json` değişikliği Oracle'a
  `scp + sudo cp + chown ubuntu` ile ayrıca konur ve canlı uçtan okunarak doğrulanır.

## H479 — Yönetim › Quiz havuzu Oracle'da boştu (Docker'da rootDir/.. yanlış kök) (2026-11-03)
- **Belirti:** `/api/admin/quiz/havuz` Oracle'da `toplam: 0` (k2-10/k2-11 dahil); dosyalar `meds_database_v2/ders_isci/yayinlanan/elle-*/` altında vardı.
- **Kök neden:** Oracle'da uygulama Docker'da `/app`'te; `ekSayfalar.ts` yolu `path.resolve(rootDir,'..','meds_database_v2')` = `/meds_database_v2`
  kuruyordu (yalnız phase14 kalıntısı olan boş bir kök klasör). Asıl bağlama `/home/ubuntu/medsor/meds_database_v2`. Yerelde iki yol çakıştığı için fark edilmedi.
  `sistemEk.ts`'de `meds_temp` (RAG günlüğü, hat durumu) aynı hatayı taşıyordu.
- **Çözüm:** `meds_database_v2` = `dirname(MEDS_DATABASE_DIR)/meds_database_v2` (phase14Overlay.ts kuralı), `meds_temp` = `MEDS_TEMP_DIR`.
- **Önleme:** Sunucu kodunda kardeş veri klasörleri `rootDir/..`'dan değil ortam değişkeninden (MEDS_DATABASE_DIR, MEDS_TEMP_DIR, MEDS_DOWNLOADS_DIR) türetilir;
  yeni uç canlıda (Oracle) bir kez çağrılarak boş olmadığı doğrulanır.

## H480 — Canlı damgası yeni commit'i gösterirken sunucu kodu eski kaldı (2026-11-03)
- **Belirti:** onem 633 dağıtımından sonra `dist/dagitim.json` 67ab8ccf (H479) diyordu ama `/api/admin/quiz/havuz` hâlâ boştu, sunucu dosyası eski,
  meds-app yeniden başlamamıştı; `dagit.sh` "Canlı zaten güncel" deyip ikinci dağıtımı reddetti (onem+1 ile zorla yeniden dağıtıldı).
- **Kök neden:** (1) damga kodla AYNI rsync'te ve önce (`dist/` < `src/`) gidiyor, kodun hedefle eşleştiği hiç doğrulanmıyordu — kod eksik inerse
  damga yine yeni commit'i söylüyor, sonraki dağıtımlar da "güncel" sanıp atlıyordu. (2) Aktarılan dosya listesi `^>f` ile süzülüyordu; gönderimde
  rsync `<f` yazar → liste her dağıtımda "0 dosya" idi, yeniden başlatma yalnız kod karmasına kalmıştı. Kodun neden eksik indiği (eşzamanlı oturum
  dağıtımı 19:05–19:07) tam yeniden kurulamadı.
- **Çözüm:** `deploy-code.sh` damgayı ana rsync'ten çıkarır, en sonda yalnız sunucu kodu karması (yerel dosya listesi üzerinden; Oracle'daki eski
  artık dosyalar sayılmaz) Oracle diskiyle eşleşirse gönderir, eşleşmezse DURDU (çıkış 1). Dosya listesi kalıbı `^[<>]f`.
- **Önleme:** dağıtım "bitti" ancak canlının diskindeki kod hedef commit'le eşleşince sayılır; damga doğrulamadan önce yazılmaz.

## H481
- **Belirti (2026-11-04):** çevrimdışına indirilen ders PDF'leri internetsiz açılmıyor; kullanıcıya "PDF indirilip kaydedilmiyor" gibi görünüyor.
- **Kök neden:** H63'te `sw.js` paket önbelleğinde (`medsor-paket-v1`) olmayan her `/api/lecture-pdf/` isteğini Range/206 kilidinden kaçmak için
  doğrudan ağa bırakır oldu (`return`). Sesli dersin (`medsoru-canli-ders-offline`) ve eski "çevrimdışı için indir"in (`medsoru-pdf-offline`)
  yazdığı PDF + eşleme kopyaları cihazda vardı ama hiç okunmuyordu; ağ yokken istek düşüyordu.
- **Çözüm:** SW bu iki önbellekteki lecture-pdf adreslerini kümede tutar (`cihazPdfYukle`, PAKET_CHANGED ile tazelenir; sesli ders ve
  `savePdfOffline` kayıttan sonra bildirir). Kümede olan istek cihazdan (`aralikYaniti`, Range → 206) verilir; olmayan yine ağa bırakılır.
  Sınama: headless Chrome, internetsiz → tam yanıt + 206.
- **Önleme:** bir isteği SW'den "ağa bırakan" her kısa devre, o adresi yazan TÜM önbellekleri (paket, sesli ders, eski PDF) önce denetlemelidir;
  çevrimdışı düzeltmesi internetsiz gerçek sınamayla doğrulanmadan bitmiş sayılmaz.

## H482
- **Belirti (2026-11-04):** Kurul 2 toplu indirmeden sonra internetsiz sesli derste PDF görünmüyor, slayt/çizim takibi yok.
- **Kök neden:** H481 (SW cihazdaki ders PDF'ini okumuyordu) + `onbellekte()` arama sırası sesli ders önbelleğini (`medsoru-canli-ders-offline`)
  içermiyordu: toplu indirmenin oraya yazdığı pdf.js yardımcıları (yazı tipi, wasm) ve eşlemeler internetsiz bulunamıyordu.
- **Çözüm:** `ARAMA_SIRASI`na `CD_OFFLINE_CACHE` ve `medsoru-pdf-offline` eklendi. Uçtan uca sınama (headless Chrome, tarayıcı önbelleği kapalı):
  ders indir → internetsiz aç → PDF 206 cihazdan, 8 sayfa çizildi; indirmeden aynı sınama PDF açmıyor.
- **Önleme:** yeni bir çevrimdışı önbellek adı eklenince `ARAMA_SIRASI` ve lecture-pdf kısa devresi birlikte güncellenir.

## H483
- **Belirti (2026-11-04):** H481/H482 öncesinde indirilmiş derslerde PDF ya da eşleme eksik kalmış olabilir; "Sına" bunları sağlam gösteriyordu.
- **Kök neden:** `paketiDenetle` sesli derste yalnız ses + konuşma metnine bakıyordu; PDF, deste eşlemesi ve PDF'siz indirilmiş dersler denetlenmiyordu.
  Eksiği kendiliğinden tamamlayan bir adım da yoktu.
- **Çözüm:** `src/services/cevrimdisi/eksikGider.ts`: açılışta (internet varken, 12 saatte bir, `ONARIM_SURUM` değişince hemen)
  tüm indirilenleri tarar. Sesli derste eksik PDF/eşleme/ayrıntı ya da PDF'siz kayıt varsa aynı seslerle `cdCevrimdisiAyarla` (yalnız eksikler iner),
  pdf.js yardımcıları, merkez paketlerinde `paketiDenetle` → `paketOnar`. "İndirilenler"de "Eksikleri tamamla" düğmesi; `paketiDenetle` PDF'i de sayar.
  Sınama: ders indir → PDF'i sil → `eksikleriGider` → 2 dosya geri geldi → internetsiz 206 + 8 sayfa.
- **Önleme:** çevrimdışı indirmeye yeni bir parça eklenince denetim (`paketiDenetle`) ve `eksikGider` aynı commit'te güncellenir; `ONARIM_SURUM` artırılır.

### H503 — "Güncelle"ye basınca eski sürüm açılıyor, sürekli güncelleme varmış gibi görünüyordu (2026-11-06)
- **Belirti:** güncelleme diyaloğu/Yenilikler penceresi tekrar tekrar çıkıyor, sırası karışıyor; onaylayınca site eski sürüme dönüyordu.
- **Kök neden:** (1) SW gezinmede ağ 400 ms'de yanıtlamazsa kabuğu `ARAMA_SIRASI`'ndaki TÜM önbelleklerde arıyor; `guncelle()` yalnız `medsoru-static/runtime-*` siliyordu, başka önbellekte kalan eski `/`/rota kabuğu yeniden açılıyordu. (2) Eski kabuk açılınca `medsoru_yenilik_goruldu_v1` daha küçük ONEM ile geri yazılıyor, yeni sürümde Yenilikler her açılışta yeniden çıkıyordu.
- **Çözüm/önleme:** `UpdatePrompt.tsx`: güncellemede çevrimdışı ders/paket önbellekleri dışındaki tüm önbelleklerden HTML/rota kabuğu kayıtları silinir; sürüm kayıtları yalnız ileri yazılır. Kural: cihaz sürüm kaydı asla geriye yazılmaz; kabuk silme, SW'nin aradığı bütün önbellekleri kapsar.

### H505 — Polinöropati ve Bazal Ganglionlar sesli derslerinde PDF açılmıyor, yalnız "Drive'da aç" çıkıyordu (2026-11-06)
- **Belirti:** sesli ders görüntüleyicisi "Bu dersin PDF'i uygulama içinde açılamıyor" + "Drive'da aç" gösteriyordu (k2-17, k2-18; canlıda k2-19 de).
- **Kök neden:** destesiz (Öğren askıda) yeni derslerin PDF'i yalnız `src/services/lecturePdfLocator.ts::SANAL_DESTELER` kaydıyla bulunur. (1) k2-17/k2-18 hizalaması yazılmış ama kayıt eklenmemişti → `/api/lecture-pdf/deck/<id>` boş dosya listesi. (2) k2-15/16 kaydı eklenmiş, `meds-web` yeniden başlatılmadığı için yerel sunucuda görünmüyordu (AGENTS 12); k2-19/20/21 kaydı commit/dağıtım bekliyordu.
- **Çözüm/önleme:** iki kayıt eklendi, sunucu yeniden başlatıldı, dağıtıldı. Yeni kapı `python3 scripts/kapilar/ders_pdf_kapisi.py [--sunucu …]`: her `data/sesli_anlatim/hizalama/k2-*.json` deckId'si sunucu kataloğunda açılabilir PDF'le bulunmalı (0 HATA). Kural: `ders-ekle`/hizalama sonrası SANAL_DESTELER kaydı + `meds-web` restart + bu kapı (yerel ve Oracle) — kapı geçmeden ders yayında sayılmaz.

### H513 — dist/assets hiç budanmıyordu: cihazda 473 derleme (3 GB), Oracle'da 92 bin parça (5,2 GB) + 5,9 GB arşiv (2026-11-09)
- **Belirti:** Kullanıcı "optimizasyon problemlerini çöz" dedi; ölçümde `meds/dist/assets` 65.794 dosya / 3,0 GB, Oracle `dist/assets` 92.674 dosya / 5,2 GB, `data/asset-archive` 101.057 dosya / 5,9 GB; Oracle diski %63 (Docker derleme önbelleği 49,9 GB ayrıca).
- **Kök neden:** `vite.config.ts` `emptyOutDir: false` (açık sekmeler eski parçayı isteyebilsin diye) + `deploy-code.sh` rsync'i `--delete`siz → eski hash'li parça hiçbir yerde silinmiyor. `server.ts::archiveDistAssets` 21 günlük budamayı yalnız "dist'te olmayan" arşiv dosyalarına uyguluyordu; dist'te her şey kaldığı için hiçbir şey budanmıyordu. Günde ~30 derleme (çok oturum) birikimi hızlandırdı.
- **Kalıcı çözüm:** `vite.config.ts` `build.manifest: true` → `dist/.vite/manifest.json`; `server.ts` açılışta `readDistManifestFiles` ile güncel kümeyi okur, `pruneDistAssets` manifest dışı ve 7 günden eski parçaları `dist/assets`'ten siler; arşiv budaması da güncel kümeyi manifestten alır. Oracle'da `docker builder prune -af` (49,9 GB; disk 109 → 64 GB).
- **Önleme:** Hash'li çıktı biriktiren her klasöre (dist, arşiv, ses klipleri) yazan kod, "güncel küme + yaş" kuralıyla budama da yazar; "sonra temizleriz" diye bırakılmaz. Oracle'da imaj yeniden kurulduğunda `docker builder prune` dağıtım sonrası adımıdır (`dagit.sh`'a eklenmedi; elle).

### H516 — Dağıtım yeniden başlatması sırasında açılan sayfa açılış ekranında sessizce takılıyordu (2026-11-09)
- **Belirti:** Kullanıcı "site açılmıyor, splash'tan geçmiyor" dedi; tam o dakikada başka oturumun `dagit.sh` dağıtımı Oracle `meds-app`'i yeniden başlatmıştı (RAG yükü 1-2 dk). Sunucu dönünce site sorunsuzdu ama kullanıcı elle yenilemeden kurtulamamıştı.
- **Kök neden:** Service worker kabuğu kesintide de verildiğinden sayfa "açılıyor" ama uygulama veri alamıyor; splash yalnız React hazır olunca kalkıyor ve `__medsoruTazeYukle` sunucu 200 vermeden yenilemiyor. "Sunucu yok" durumunun ekranda karşılığı yoktu.
- **Çözüm/önleme:** `index.html` H516 bekçisi: 7 sn'de açılmazsa `/api/surum` yoklar, durum yazısı gösterir, sunucu dönünce kendiliğinden yeniler. Kural: öğrencinin bekleyebileceği her "sunucu yok / ağ yok / eski kabuk" durumu ekranda bir yazı + kendiliğinden kurtulma yolu taşır; sessiz bekleme yasak. Dağıtım saatinde gelen "site açılmıyor" bildiriminde önce Oracle `docker events`/uptime'a bakılır (bu kez `uptime: 18 s` ile doğrulandı).

### H545 — `git add server.ts` başka oturumun commit'lenmemiş iki satırını da commit'e aldı; depoda olmayan dosyayı içe aktaran sunucu kodu origin/main'e gitti (2026-11-10)
- **Belirti:** Ek modüller commit'inde `server.ts` farkı 2 yerine 4 satırdı: benim `registerEkModulSesRoutes` satırlarımın yanında başka bir oturumun `registerAsistanRoutes` içe aktarımı ve çağrısı (`src/services/asistan/` depoda yok). Dağıtım sırasında Oracle'daki `server.ts` de çalışma ağacındaki bu kirli sürümle bulundu; bütünlük adımı durdu, sunucu yeniden başlatılmadı (başlatılsaydı açılışta çökerdi).
- **Kök neden:** ortak dosya (`server.ts`, `App.tsx`, `router.ts`) bütün olarak sahnelendi; "dosyadaki bütün değişiklik benim" varsayıldı. Çalışma ağacında başka oturumların yarım işi vardı.
- **Çözüm:** iki satır ayrı bir commit ile depodan çıkarıldı (çalışma ağacında o oturum için bırakıldı), Oracle'daki `server.ts` commit'lenmiş sürüme geri yazıldı, dağıtım yeniden koşuldu.
- **Önleme:** ortak dosya sahnelenmeden önce `git diff <dosya>` okunur; yabancı satır varsa yalnız kendi parçaların sahnelenir (`git apply --cached` / `git update-index --cacheinfo`). Commit'ten sonra `git show --stat` satır sayıları beklenenle karşılaştırılır. Oracle'da `server.ts`'in kirli sürümle bulunmasının kaynağı saptanamadı (dağıtım temiz worktree'den yapılır); yinelenirse o dakikada Oracle'a yazan öteki süreç aranır.

### H556 — "PDF indir" herkese "X-API-Password başlığı gereklidir" diyordu; canlıda başsız tarayıcı da yoktu (2026-11-13, kullanıcı bildirdi)
- **Belirti:** soru çıktısı / soru dışa aktarımı / ek modül föyünde "PDF indir" → `Veri göndermek veya değiştirmek için X-API-Password başlığı gereklidir.` (HTTP 401). Girişli öğrenci de yönetici olmayan herkes de aynı hatayı alıyordu.
- **Kök neden:** PDF basımı `/api/pdf/render` (POST) ucundan yapılır; bu uç **veri yazmaz**, yalnız istemcinin gönderdiği HTML'i başsız Chrome'da PDF'e basar. `server.ts::requireWritePassword` ara katmanı bütün POST'lara yazma parolası arıyor, parolasız izin verilenler iki listede: `readOnlyPosts` (sabit yol listesi) ve `STUDENT_WRITE_ROUTES` (öğrenci beyaz listesi). `/api/pdf/render` **ikisinde de yoktu** → öğrenciye hiç verilmeyen parola istendi. İkinci, daha sinsi engel: canlı Oracle imajı (`deploy/oracle/Dockerfile.oracle`, node:24-bookworm-slim + yalnız python3) içinde Chrome/Chromium yoktu; canlıda `GET /api/pdf/status` `{"available":false}` dönüyordu, yani parola verilse bile basım `503` verecekti. Yerelde Chrome kurulu olduğu ve istekler loopback'ten (yönetici) geldiği için hata geliştirmede görünmüyordu.
- **Kalıcı çözüm:** (1) `STUDENT_WRITE_ROUTES`'a `['POST', /^\/api\/pdf\/render$/, 'belge']` eklendi; yeni `belge` sınıfı IP başına dakikada 20 / saatte 300 (`STUDENT_WRITE_LIMITS`), ağır Chrome işi zaten sunucuda kuyruklu (2 koşut + 8 kuyruk, sıra doluysa 429). (2) `Dockerfile.oracle`'a `chromium` + `fonts-dejavu-core` eklendi (ARM'de `chromium 156` paketi var; geçici konteynerde uçtan uca sınandı: `%PDF-1.4`, 13.595 bayt). (3) `docs/API_KATALOG.md` parolasız uçlar bölümü eklendi.
- **Önleme:** yeni bir parolasız uç gerektiğinde önce "veri yazıyor mu?" sorusu sorulur: yazmıyorsa `readOnlyPosts`/`STUDENT_WRITE_ROUTES`'a **sınırıyla** eklenir, yazıyorsa parola ister. Kapı: `python3 scripts/kapilar/pdf_basim_kapisi.py` (yerelde ve canlıda) `/api/pdf/status` `available:true` + parolasız 200 ve `%PDF` imzası arar; 401'de "uç beyaz listede değil", tarayıcı yoksa "imaja chromium eklenmeli" der.
- **Kök neden 3 (kapının kendisi):** canlı sınamada kapı `cf-connecting-ip: 203.0.113.9` başlığını elle basıyordu; Cloudflare istemcinin yazdığı bu başlığı sahte sayıp `403 error code: 1000` veriyor (tarayıcı User-Agent'ı olmadan da bot koruması 403 veriyordu). Yerelde bu başlık gerekli (yoksa istek loopback yönetici sayılır ve öğrenci yolu sınanmaz), canlıda ise zararlı: Cloudflare gerçek istemci IP'sini kendisi ekler, sunucu isteği loopback saymaz. Kapı artık hedefe göre başlık seçer: yerelde `cf-connecting-ip`, canlıda yalnız tarayıcı User-Agent'ı. Canlı sonuç: `0 HATA` (`available:true`, `POST /api/pdf/render` → 200, 7.218 bayt `%PDF-1.4`).
- **Ders:** **loopback'te çalışan uç, canlıda öğrenciye kapalı olabilir** — yetki değişikliği hem yerelde hem canlıda sınanır (canlıda dış istemci başlığı taklit edilmez, gerçek tarayıcı gibi gidilir); canlı imajda dış araç (Chrome) var mı diye `pdf/status` gibi bir uçtan bakılır.

### H559 — İçerik katmanı toplu "silinen" yazdı: sözlükte 750 terim, Öğren'de 11 deste sunucuda görünmüyordu (2026-11-13, kullanıcı bildirmedi — tur sırasında bulundu)
- **Belirti:** Sözlük sayfasında tanıdık terimler yoktu: `/api/content/glossary` **3618** kayıt dönüyordu (kaynakta 4368); `bilinç`, `koma`, `somnolans`, `stupor`, `ARAS` gibi temel nöroloji terimleri eksikti. Aynı biçimde `/api/decks` **175** deste dönüyordu (kaynakta 186): `k2p-k2-01…k2p-k2-11` (Nörolojik Hastaya Yaklaşım, Bilinç Bozukluğu, SSS Hücresel Reaksiyonları ve Ödem/Herniasyon, Serebrovasküler Hastalıklar ve İnme, Nörolojik Muayene, Ağrı Fizyopatolojisi, Genel Anestezik İlaçlar, Beyin ve İskelet Sistemi Gelişimi Genetiği, SSS İlaçları, Baş Ağrısına Yaklaşım, Psikiyatrik Semiyoloji) Öğren listesinde yoktu. Hata vermiyordu; veri sessizce eksikti.
- **Kök neden:** `data/content/` altında eski bir birleşimden üretilmiş **TAM KOPYA** kalmıştı (H130'un kayıt-düzeyi fark öncesi biçimi). Sunucu açılışında `initContentOverlay → donustur()` bu kopyayı farka çevirirken, kopyada BULUNMAYAN her kaynak kaydını "yönetici sildi" saydı ve `f.silinen`'e yazdı: 750 sözlük terimi + 11 deste. Var olan `bayat` (kopya kaynaktan eski mi) koruması yalnız **mtime**'a bakıyordu; kaynak dosya 2026-11-02, kopya 2026-11-12 23:44 damgalı olduğu için "kopya yeni" sayıldı ve toplu silme engellenmedi. Yani gölgeleme sorunu (H130) çözülmüş gibi görünürken aynı sonuç `silinen` listesinden geri geliyordu — mtime, içeriğin yaşını göstermez.
- **Kalıcı çözüm:** (1) İki fark dosyasında `silinen` boşaltıldı, önce `data/_yedek/*.fark.<zaman>.bak` yedeği alındı, yazım `tmp` + `os.replace` ile atomik yapıldı. Doğrulama (meds-web yeniden başlatıldıktan sonra canlı uçlardan): sözlük **4368** (`bilinç` var), deste **186** (11 k2p deste de listede). (2) `src/services/contentOverlay.ts` `donustur()` içine **toplu silme freni** eklendi: bir dönüşümde yeni silme adayı sayısı `max(5, kaynak kaydı sayısının %5'i)` eşiğini aşarsa kopya bayat/eksik sayılır; silme yazılmaz, bekleyen kayıt değişiklikleri düşürülmez, kimlikler `data/content/_karantina_silinen.json`'a (son 20 olay) yazılır ve `console.warn` ile günlüğe düşer. `npx tsc --noEmit` 0 hata.
- **Aynı kökün ikinci belirtisi (bayat metin):** Aynı dönüşüm, kopyadaki ESKİ kayıt sürümlerini de "yönetici düzenlemesi" saymıştı. Yerelde sözlüğün 53 kaydı kaynaktaki zenginleştirilmiş metnin **kısaltılmış eski hâlini** gösteriyordu (ör. `hipertelorizm` 144 karakter/1 madde; kaynakta 315 karakter/2 madde) ve destelerin 74 kaydı normalize edilmiş komite adları yerine eski serbest adları (`Kurul 1`, `Dönem 3 Kurul 1`, `Ürogenital Sistem Komitesi`…) taşıyordu; 7 destede de kaldırılmış çok yıllı `examYear` biçimi (`2021-2026` — H455 ile tek yıl kuralı gelmişti) duruyordu. Canlı site temizdi (2 komite değeri, 315 karakter); yani bayat katman yalnız yerelde sunuluyordu, ama dağıtımda `content-overlay-sync.sh` farkları `src/data`'ya uyguladığı için canlıya sızma riski gerçekti. Bulgu: katman kaydı ile kaynak kaydı çelişiyorsa ve katman değeri eski bir biçimde (çok yıllı `examYear`, normalize olmamış komite adı, kaynağın öneki olan kısa metin) ise **kaynak yeni sayılır**. Temizlik: sözlük 53 + deste 75 + kart 2 bayat kayıt silindi (hepsi `data/_yedek/*.bayat.<zaman>.bak`), boşalan fark dosyaları ve birleşik önbellekleri kaldırıldı; yerel artık canlıyla aynı (sözlük 4368 / `hipertelorizm` 315, deste 186 / 2 komite değeri). `question_cards` kayıtlarından biri de yalnız `updatedAt`, diğeri eski `konu` etiketiydi. `site_ayar.json` farkı ise GERÇEK yönetici düzenlemesi (kaynaktan yeni: sürüm 6) — silinmedi.
- **Önleme:** `data/content/` altına elle, başka araçla ya da eski yedekten **tam kopya bırakılmaz** (yalnız `.fark.json`). Sözlük/deste/soru sayısı beklenenden az görünürse ilk bakılacak yer `data/content/<dosya>.fark.json` → `silinen`dır; `python3 scripts/icerik_katman.py denetle` ile katman düzenli denetlenir. Günlükte "toplu silme sayılmadı, karantinaya alındı" uyarısı görülürse `_karantina_silinen.json` açılır: silme gerçekten yönetici kararıysa kimlikler fark dosyasına elle yazılır; değilse hiçbir şey yapılmaz — kayıtlar görünür kalır. Katmanı mtime'a göre "taze" saymak yetmez: bir kopya yeni damgalı ama içeriği eski olabilir.

### H562 — Canlıda yeni anahtar "yok" göründü: `env_file` yalnız konteyner oluşturulurken okunur, loopback da konteynerde loopback değildir (2026-11-13)
- **Belirti:** Oracle `.env`'ine `MEDS_OPENDESIGN_KEY` eklendikten ve `dagit.sh` konteyneri yeniden başlattıktan sonra `docker exec meds-app printenv MEDS_OPENDESIGN_KEY` **boş** döndü (0 bayt). İlk bakışta "anahtar canlıya geçmedi" sanılıyordu. Ayrıca canlı sunucuya `127.0.0.1:3001` üzerinden atılan `POST /api/ai/generate` isteği `X-API-Password başlığı gereklidir` (401) verdi — oysa istek makinenin kendi loopback'inden çıkıyordu.
- **Kök neden:** (1) `docker-compose.oracle.yml` içindeki `env_file: ../../.env` **konteyner oluşturulurken** okunur; `docker restart`/`up -d` var olan konteynerin ortamını `.env` değişikliğiyle tazelemez (yeni değişken için konteyner yeniden **oluşturulmalı**). (2) Buna karşın uygulama `server.ts:219`'da `dotenv.config()` çağırıyor ve `../..:/app` bağıyla `.env` dosyası konteynerin içinde `/app/.env` olarak duruyor — yani anahtar, konteyner ortamında görünmese de **sunucu sürecine** dotenv üzerinden geçiyor (GEMINI anahtarları da aynı yoldan geliyor). (3) `isRequestAdmin` gerçek loopback arıyor; Docker köprüsünden gelen istek konteynerde `172.x` kaynaklı görünür, bu yüzden yönetici sayılmaz ve yazma parolası istenir.
- **Kalıcı çözüm:** doğrulama `printenv` ile değil **uçtan uca** yapılır: geçide doğrudan `POST /v1/messages` (200) + konteynerde `grep -c "^MEDS_OPENDESIGN_KEY=" /app/.env` (1) + canlı `POST /api/ai/generate` (`providerUsed: "OpenDesign (…)`). Yazma parolası gereken canlı sınamalarda `X-API-Password` `.env`'deki `MEDSORU_API_PASSWORD`'dan okunur (değer ekrana yazılmaz; `scp` edilen küçük betikle).
- **Önleme:** `.env`'e yalnız dotenv'in okuyacağı yeni anahtar ekleniyorsa konteyner yeniden başlatma yeterlidir; **compose `environment:` listesine eklenmesi gereken** bir değişken söz konusuysa `docker compose up -d --force-recreate` gerekir (bu tur gerekmedi). "Container env'de yok" tek başına "uygulama görmüyor" demek değildir; kanıt uygulamanın kendi ucundan alınır. Konteyner içinden atılan istek yönetici/loopback muamelesi görmez.

### H579 — "Oracle'da kok'u import eden her betik çöküyor": kök markerı yalnız geliştirme makinesinde vardı (2026-11-16, dağıtım sonrası canlı sınama)
- **Belirti:** c02db09f dağıtımı sağlık 200 ve "BİTTİ" verdi; ama Oracle'da `meds-cumle-zaman` günlüğü `RuntimeError: kök markerı
  'PROJE_TANITIMI.md' bulunamadı` yazıyordu. Birim "success" görünüyordu (`sh -c '… | grep >> log'` boru hattı çıkış kodunu yutuyor).
- **Kök neden:** `scripts/kok.py` `PROJE`'yi modül yüklenirken `PROJE_TANITIMI.md` markerıyla arıyordu. Bu dosya yalnız geliştirme
  makinesindeki repo-DIŞI kökte (/home/indu/medsor) bulunur; Oracle (/home/ubuntu/medsor) ve Docker (/app) taşımaz. Sonuç: `kok`
  import eden her betik (cumle_zaman, yayinla --sunucu, sunucunun başlattığı Python işleri) import anında çöker. Yerel sınamalar ve
  kum havuzu bunu gösteremezdi — hepsi markerın olduğu makinede koştu.
- **Kalıcı çözüm:** `PROJE = MEDS.parent` (eski `parents[3]` ile birebir aynı anlam, marker yok); `MEDS` markerı yoksa `SCRIPTS.parent`.
  Yerel + Oracle taklidi (kök belgesi yok) + Docker taklidi (server.ts da yok) düzenlerinde sınandı.
- **Önleme kuralı:** Kök çözümü yalnız REPO İÇİNDE izlenen dosyalara dayanır (git'te olmayan, makineye özgü dosya marker olamaz).
  Yol/altyapı değişikliği dağıtıldıktan sonra Oracle'da en az bir zamanlayıcı birimi GERÇEKTEN çalıştırılıp günlüğü okunur; sağlık uç
  noktası ve birim "success" durumu yeterli kanıt değildir (boru hattı çıkış kodunu yutabilir).


### H596 — Kimliksiz her istek 100 MB gövde gönderebiliyordu; aynı uç iki kez tanımlıydı, ikincisi yetkisiz süreç başlatıyordu (2026-11-17)
- **Belirti:** Denetimde `server.ts` `express.json({limit:'100mb'})` + `urlencoded 100mb` genel ara katman; `POST /api/automation/run-full-local-sync` iki kez tanımlı (ilki `requireAdmin`, ikincisi yetkisiz ve `meds-local-sync.mjs` başlatıyor).
- **Kök neden:** (1) Yönetim panelinin büyük içe aktarmaları için tavan bir kez 100 MB yapıldı ve gövde ayrıştırıcı kimlik ara katmanından ÖNCE kayıtlı olduğu için herkes aynı tavanı aldı; kimliksiz tek istek 100 MB'ı belleğe aldırabiliyordu. (2) Express ilk eşleşen tanımı çalıştırır, ikincisi sessizce ölü kalır; hiçbir kapı mükerrer ucu aramıyordu. İlk tanım kaldırılsa yetkisiz kopya canlanırdı.
- **Kalıcı çözüm:** `adminAuthMiddleware` gövde ayrıştırıcının önüne alındı (yalnız başlık/sorgu okur); tavan `govdeKademesi` ile seçilir: yönetici (gizli anahtar/gerçek loopback/yönetici jetonu) 100 MB, doğrulanmış üye 30 MB, kimliksiz 2 MB (`MEDS_GOVDE_YONETICI/UYE/ANONIM` ile değişir). Yetkisiz mükerrer uç silindi. Sınama: vekil başlıklı kimliksiz 3 MB → 413, 0,5 MB → uca ulaşır, loopback 3 MB → geçer.
- **Önleme kuralı:** Genel gövde ayrıştırıcıya kimlik kademesiz >10 MB tavan konmaz; büyük ham yükleme gereken uç kendi `express.raw` ayrıştırıcısını yetki ara katmanından SONRA kullanır. Yeni uç eklerken aynı yöntem+yol ikinci kez yazılmaz. Kapı: `python3 scripts/kapilar/kos.py uc` (`uc_denetim.py`, 606 uç, 0 HATA; eski `server.ts`'te mükerrerliği yakalar).

## H599 — Kurul 2 soru çözücü / en önemliler, ek modüller, KMB ve PDF notlar çevrimdışına indirilemiyordu (2026-11-17)
- **Belirti:** Çevrimdışı merkezinde Kurul 2 derslerinin yalnız sesli dersi vardı; çözücü, en önemliler, hoca soruları paketi yoktu. Ek modül ve KMB internetsiz sessizdi; PDF notlar ve tek kişilik oyunlar açılmıyordu.
- **Kök neden:** `cevrimdisiKatalog.ts` branşları koda yazılı 7 Kurul 1 listesinden (`BRANS`) alıyordu, ön yüz ise klasörden keşfediyor (`brans.ts`); yeni kurul sitede göründü, kataloğa girmedi. Ek modül/KMB/`public/pdf` için katalog paketi, `sw.js` dalı ve ses ucu yoktu; sınama rota listesi eskiydi.
- **Kalıcı çözüm:** `tumBranslar()` veri klasörlerinden keşfeder; yeni paketler `ekmodul:<id>`, `sayfa:kmb`, `veri:pdfnot`; ses kalıbı üç yerde eşitlendi; `sw.js` `/ek_moduller/` + `/pdf/` (Range/206); oyunlar çevrimdışı `services/oyunYerel.ts`; `envanter.mjs`/`sinama.mjs` güncellendi.
- **Önleme kuralı:** Katalog, ön yüzle AYNI kaynaktan keşfeder; koda yazılı branş/kurul listesi YASAK. Yeni sayfa türü/ses ucu dört yere birlikte eklenir: katalog paketi, `sayfaPaketleri.ts`, ses kalıbı + `sw.js` dalı, sınama rotası (`docs/CEVRIMDISI_YOL_HARITASI.md` §6). Çevrimdışı kanıtı ağ kesilerek `sinama.mjs` ile alınır.


## H615 — Commit başka oturumun sahnelediği silmeyi içerdi, canlı derleme kırıldı (2026-11-17)
- **Belirti:** `581dbc5b` (kayıt kapısı) `CdZenginMetin.tsx` + `cd-zengin.css` silmesini de taşıdı; `dagit.sh` "Could not resolve './CdZenginMetin'" ile durdu.
- **Kök neden:** `git add -- <yollar>` ardından düz `git commit` bütün index'i işler; sahne denetimi ile commit arasında başka oturum `git rm` yapmıştı.
- **Kalıcı çözüm:** iki dosya çalışma ağacına dokunmadan geçici index ile geri getirildi (`ee721f54`), dağıtım 0 hatayla bitti.
- **Kural:** Paylaşılan ağaçta commit YALNIZ `git commit --only -- <yollar>` (ya da geçici `GIT_INDEX_FILE`) ile; commit sonrası `git show --stat HEAD` beklenmeyen yol içeriyorsa push edilmez.

### H624 — SSS Tümörleri, OSS Farmakolojisi, Nörogelişimsel Bozukluklar: "Bu dersin PDF'i uygulama içinde açılamıyor" (2026-11-18, kullanıcı; H505 tekrarı)
- **Belirti:** k2-40/41/42 sesli derslerinde görüntüleyici PDF yerine "Drive'da aç" gösteriyordu.
- **Kök neden:** H505'teki kapı (`ders_pdf_kapisi.py`) yazılmış ama hiçbir yere bağlanmamıştı; yeni destesiz derslerin `SANAL_DESTELER` kaydı yine unutuldu (PDF'ler drive_root'ta md5 eşitti, yalnız kayıt yoktu). Kural belgede kalınca uygulanmıyor.
- **Kalıcı çözüm:** üç kayıt eklendi. Kapıya sunucusuz `--statik` kipi (kayıt + drive_root dosyası) eklendi ve `deploy/oracle/dagit.sh` dağıtımdan önce bunu zorunlu çalıştırıyor (çıkış 74): hizalaması olup PDF kaydı olmayan ders artık canlıya çıkamaz.
- **Kural:** yeni sesli ders = SANAL_DESTELER kaydı + `meds-web` restart; kapı dağıtımda zorunlu, atlanamaz.

### H627 — k2-36/k2-39 dağıtımı PDF kapısında durdu: SANAL_DESTELER kaydı ve drive_root dosyası unutuldu (2026-11-18)

- **Belirti:** `dagit.sh` "PDF'i kayıtsız sesli ders var (H624)" ile 74 çıkışıyla durdu; iki yeni ders deckId'si için "sunucuda açılabilir PDF yok".
- **Kök neden:** Yeni sesli dersin görüntüleyici PDF'i iki ayrı yerden gelir: `src/services/lecturePdfLocator.ts` `SANAL_DESTELER` kaydı ve `meds_downloads/drive_root/Kurul N/<branş> /<dosya>.pdf`. Tam hat runbook'unda (`ders_ekle`) bu adım yok, H624 yalnız dağıtım kapısında yakalıyor.
- **Çözüm:** İki ders için kayıt eklendi, okul Drive'ından inen PDF'ler drive_root'a (klasör adındaki sondaki boşlukla) kopyalandı; kapı 0 HATA.
- **Kural:** Yeni ders için `ders_ekle`'den hemen sonra SANAL_DESTELER kaydı + drive_root dosyası + `meds-web` restart; commit'ten önce `python3 scripts/kapilar/ders_pdf_kapisi.py --statik --kok "$PWD"` 0 HATA.


### H647 — Site herkese açıktı; "yalnız Arzu Türk + yönetici" isteği yalnız ekranla karşılanamazdı (2026-11-23)
- **Belirti (istek):** "Site yalnızca Arzu Türk ve yönetici tarafından kullanılabilir olsun, diğerlerine hata sayfası göster; veritabanı yüklenmesin, içeriklere erişemesinler."
- **Kök neden riski:** Uygulamada yalnız giriş kapısı vardı (`girisKapisi`); giriş yapan herkes tüm `/api/*` verisini (committees, questions, past-exams, ses, PDF) alabiliyordu. İstemcide tek ekran kapamak yetmez: jetonla doğrudan API çağrısı veriyi yine indirir. Ayrıca izinli liste kodun beş yerine dağılsaydı H320–H329'daki "aynı kural çok yerden düzenleniyor" hatası tekrarlanırdı.
- **Kalıcı çözüm (iki katman, TEK liste):**
  - `src/services/erisimSiniri.ts` — izinli e-posta listesi (`ERISIM_EPOSTALARI`: 3 Arzu Türk adresi + yönetici), `erisimEpostasiIzinli`, ortak mesaj, `erisimEngelliMi()` (senkron localStorage okuması). Arzu katmanı (`arzuKimlik.ts`) de aynı listeyi kullanır.
  - Sunucu: `src/services/erisimKapisi.ts`, `server.ts`'de gövde ayrıştırıcıdan sonra/veri uçlarından önce. İzinli olmayan oturum → 403 `{ code: 'ERISIM_KAPALI' }`. Yönetici (anahtar/loopback/jeton), yapay zekâ test çerezi ve kimlik/bakım/sağlık/sürüm/site-ayar uçları muaf; `/api/admin/*` kendi kapısını uygular. Kayıt AÇIK kalır (kullanıcı kararı): hesap açılır, giriş yapılır, uygulamaya girilemez.
  - İstemci: `main.tsx` engelli oturumda eşitleme/presence/çevrimdışı paket/veritabanı istatistiği kurmaz; `App.tsx` kabuk yerine `components/system/ErisimKapali.tsx` (kapatılamaz hata ekranı, "Çıkış yap") çizer; kurul/soru/canlı abonelik efektleri `erisimEngelli` ile erken döner. Giriş başarısında izinsiz hesap sayfayı yeniler ki açılış kurulumları hiç başlamasın.
  - Jeton: `adminFetchAuth.ts` artık oturum açmış her kullanıcının jetonunu kendi `/api/*` isteklerine ekler (sunucu artık jeton istiyor); çevrimdışıyken eklemez (SW önbelleği çalışsın). SSE için `oturumTokenForStream()`.
- **Doğrulama:** uzak IP + anonim `/api/committees` → 403; izinli Arzu jetonuyla → 200 (committees/questions/SSE); izinsiz kayıtlı deneme hesabıyla tarayıcı → "Bu hesaba site kapalı" ekranı; loopback panel → 200. Test hesabı meds-pg'den silindi.
- **Kural:** Erişim sınırı yalnız istemci ekranıyla kurulmaz; veri ucu sunucuda kapı olmadan yayına çıkmaz. İzinli liste tek dosyada (`erisimSiniri.ts`) yaşar — yeni istisna oraya eklenir, başka yere kopyalanmaz. Giriş jetonu gerektiren yeni bir okuma ucu eklenirse `adminFetchAuth.jetonEklenir()` kapsamı kontrol edilir.

### Erişim kapısı sonrası ses/slayt/çevrimdışı indirme 403 ("Ses dosyası açılamadı") (2026-11-24)
- **Belirti:** İzinli hesapta sesli ders "Ses dosyası açılamadı", slaytlar yüklenmiyor, çevrimdışı indirme yarıda kalıyor.
- **Kök neden:** 2026-11-23 erişim kapısı (`erisimKapisi.ts`) kimliği yalnız `Authorization` başlığından okuyordu. `<audio src>`, `<img>`, Background Fetch ve service worker istekleri bu başlığı taşıyamaz; global `fetch` sarmalayıcısı (`adminFetchAuth.ts`) yalnız sayfa içi `fetch`'e jeton ekler → bu istekler 403.
- **Çözüm:** `auth.ts` erişim jetonunu `medsor_jeton` çerezine de yazar (ömrü jetonla, canlıda `Domain=nofrostlife.com.tr`, 4 dk'da bir yenileme); kapı başlık yoksa çerezi **yalnız GET/HEAD**'de kabul eder (CSRF). CORS kendi alan adlarına kökeni yansıtıp `Allow-Credentials` verir; Background Fetch istekleri `credentials: 'include'`.
- **Daraltma (aynı gün):** JS çerezindeki erişim jetonu sızarsa Bearer olarak yazmada kullanılabilirdi → yerine sunucunun `POST /api/kimlik/medya-cerezi` ile yazdığı HttpOnly, yalnız API alanlı, `typ: 'medya'` jetonu (`medsor_medya`); Bearer yolu bunu reddeder, kapı yalnız GET/HEAD'de kabul eder.
- **Çevrimdışı paket (aynı gün, canlı sınamada):** `net.ts › arkaPlanFetch` bilerek ham `fetch` kullanır (jeton eklenmez) ve çapraz kökende varsayılan `credentials: 'same-origin'` çerezi göndermez → paket dosyaları reddedilip 4 denemeden sonra "Bağlantı sorunu: dosya inmedi". Çözüm: `credentials: 'include'`.
- **Önleme:** Erişim/kimlik kapısı eklerken başlık taşıyamayan istekleri (ses, görsel, PDF, arka plan indirmesi, SW) ayrıca sına; yazma uçlarına çerezle kimlik verme.

### H688 — `betik_tamamla` yeni dersi "yayında değil" sandı; kelime zamanı canlıya gitmemişti (2026-11-26, k2-25/k2-59)
- **Belirti:** `betik_tamamla.py k2-25` "kelime_zaman: canlı API okunamadı (ders yayında değil mi?)" dedi; ders Oracle'da yayındaydı.
- **Kök neden:** (1) `canli()` canlı API'ye panel anahtarı göndermiyordu; erişim kapısından (H647) beri anahtarsız istek reddediliyor (anonim istek 403 değil 500 `INTERNAL_ERROR` dönüyor — ayrı açık iş). (2) Kelime zamanı yerelde `--oracle` olmadan üretilmişti; `kelime_zaman.py --oracle` yerel dosyayı "güncel" sayınca `oracle_gonder()`'i hiç çağırmıyordu, canlı varyantta `kelimeZaman` boş kaldı.
- **Çözüm:** `canli()` isteğine `_kok.panel_basligi()` eklendi; kelime zamanı `oracle_gonder()` ile gönderildi, iki ders 0 eksik.
- **Kural:** Yeni derste kelime zamanı doğrudan `kelime_zaman.py --key <key> --oracle --gpu` ile üretilir (ya da `betik_tamamla.py <kod> --gpu`); canlı API'yi okuyan her betik `_kok.panel_basligi()` gönderir. Yayın öncesi `betik_tamamla.py <kod>` ✓ kelime_zaman şart.
