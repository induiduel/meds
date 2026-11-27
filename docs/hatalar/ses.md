# Hata defteri — ses (EMA sesi, okunuş, hoca dökümü, cümle/kelime zamanı)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

### H3 — Kısaltma kelime gibi okunuyor ("DNA" → "deneye")
- **Kök:** `okunus.duzelt` harf adlarını bitişik yazıyordu ("denea"); EMA bunu kelime gibi okur.
- **Kural:** EMA'ya giden her Kurul 2+ metni uzun harf okunuşuyla ("dee nee aa", `patoloji_cozucu/kisaltma_ses.uzat`).
- **Kapı — EKLENDİ:** `ema_isci.uzun_kisaltma_ayarla` (anahtar `k[2-6]…` → uzun okunuş), Öğren sesi `ema-2`. Kurul 1 eski yolda (toplu yeniden üretim yok).

### H11 — Ses Oracle'a gitmiyor, tarayıcı sesine düşüyor (404)
- **Kapı — EKLENDİ:** zincirin `oracle` adımı canlıda dersin rastgele 5 çözücü/asistan klibini yokluyor (200/206 değilse kod 12).

### H12 — Türev veri (cümle/kelime zamanı, işaret, vurgu) metnin başka sürümünden üretilmiş
- **Kural:** türev veri yayındaki metinden ve aynı makinede üretilir; hash uyuşmazlığı sessizce boş gelmez.
- **Kapı — EKLENDİ:** `saglik.py turev_eksikleri`: canlıda sesi olan her derste cümle zamanı + PDF işareti var mı (sunucu
  karma tutmayanı göndermez → sessiz kayıp görünür olur). Kurul 2+ eksik = sorun, Kurul 1 = rapor. İlk ölçüm (2026-10-20):
  15 Kurul 1 dersinde cümle zamanı yok (metin aynı gün değişmiş; Oracle zamanlama işi yetişmeli).

### H13 — Sesli ders bütünlüğü (yönerge okunması, kapanış patlaması, paragraf/süre uyuşmazlığı)
- **Kural:** EMA için de aynı: modele yalnız okunacak metin gider; eşleşme kapısı korunur.
- **Kapı — VAR:** `metin_denetle` + eşleşme kapısı + v2 kapısı.

### H17 — EMA okunuş ayarı alt süreçte uygulanmıyordu (TBG kampı, 2026-10-20)
- **Kök:** `ema_isci.sentezle` ayrı süreçte çalışır; üst süreçte `uzun_kisaltma_ayarla` ile kurulan genel ayar (H3 uzun
  kısaltma, modül okunuşu) oraya taşınmıyordu → kısaltmalar eski yolla okundu.
- **Kural:** sesi etkileyen her ayar iş dosyasından (`is.key`) sentez sürecinin İÇİNDE kurulur; genel değişkene üst süreçten
  güvenilmez. Kamp sesi (`scripts/uretim/kamp/ses.py`) süreç içi çalışır, anahtarı `kN-kamp` (K2+ uzun kısaltma yolu).
- **Kapı — EKLENDİ:** `sentezle` başta `uzun_kisaltma_ayarla(is.key)` çağırır; `saglik.py ema_alt_surec_okunusu` bu
  çağrı kalkarsa kapı arızası verir. Modül dersleri (birden çok dersin özeti) `modul_okunus.py MODUL_ANAHTARLAR`'a eklenir.

### H — Okunuş ekrana, rakam sese sızıyordu (kullanıcı, 2026-10-22)
- **Belirti:** ekranda “yirminci ile yirmi dördüncü hafta”, “beta ha ce ge”; seste “14. … hafta” (rakam + nokta duraklamalı).
- **Kural:** ses okunuşla (“on dördüncü”, “doku plazminojen aktivatörü”), ekran yazımla (“14.”, “(t-PA)”, “β-hCG”, “12+6 hafta”).
- **Kapı — EKLENDİ:** ekran `ekranYazim.ts`, ses `okunus.SAYI_TTS`; yeni kısaltma/açılım `yazim_sozlugu.py` ile sözlüğe girer.

## H58 — EMA cümle ortasında sesi düşürüp es veriyordu (2026-10-24, kullanıcı)
- Kök: `ema_lightning/chunker.py` ~10 sn'yi (hız 1'de 180 harf) aşan metni son virgülde ya da düz boşlukta kesip parça
  sonuna "." ekliyor, araya 0,12–0,25 sn es koyuyordu → cümle bitmiş gibi kapanış tonu. Virgülde de virgülsüz yerde de oluyordu.
- Düzeltme: `ema_isci.model_yukle()` `chunker.MAX_SECONDS=30`, `MAX_LETTERS=750` (bütün EMA betikleri bu yoldan geçer);
  kesim yalnız gerçek cümle sonunda. Kurul 1 sesleri bilerek yeniden üretilmedi (kullanıcı kararı); K2'de etkilenen tek
  klip (k2farmakoloji 2f01 q-26) yenilendi.
- Kural: bu sınır geri çekilmez; tek cümle 30 sn'yi aşıyorsa metin aşamasında bölünür. Sayım betiği: kütüphanenin
  `chunker.chunk` çıktısında `SENTENCE_PAUSE` dışı kesim = hata.

## H81 — Amfi kaydı tek parça + VAD ile verilince Whisper "Altyazı M.K." sanrısıyla erken bitti; eşzamanlı tsc OOM'a yol açtı (2026-10-27)
- **Belirti:** 28 dk hoca kaydından 1 segment ("Altyazı M.K.") ya da istem cümlesi tekrarları çıktı; sonra iş OOM ile öldü.
- **Kök neden:** Kısık/yankılı amfi sesinde VAD konuşmayı eliyor, `initial_prompt` sanrı tekrarına yol açıyor; tüm dosya tek
  çağrıda verilince model ilk sanrıdan sonra susuyor. Aynı anda iki `tsc --noEmit` (5,6 + 3,5 GB) belleği bitirdi.
- **Çözüm / kural:** `hoca_dokum.py`: ham ses, VAD/istem yok, 60 sn parça + 2 sn bindirme, sanrı süzgeci, `.yarim` ile kaldığı yerden sürer; `MemoryMax=4G`. Döküm sürerken `tsc --noEmit` yok.

## H104 · Hoca ses kaydı: tek model dökümü sınav vurgularını bozuyordu; kayıt dersin ortasından başlıyordu (2026-10-27, k2-08)
- **Belirti:** large-v3-turbo dökümünde hocanın dersin sonunda saydığı sınav yerleri gen adlarını bozuyordu (HOX "koks/COX", PAX6 "faksa altı", holoprozensefali tipleri "Dövar, övar, sevdövar"); kayıt 45. slayt civarından başlıyor, 1–44. slaytlar dökümde yoktu; "Altyazı M.K." sanrıları arada segment kapatıyordu.
- **Kök neden:** Kısık amfi sesi + tek model; sınav özeti hızlı konuşulduğu için en çok bozulan bölüm tam da en önemli bölüm.
- **Çözüm:** Son 7 dk Systran medium ile 30 sn parçalarla ikinci kez döküldü (CPU, systemd-run MemoryMax=4G); iki dökümün ortak anlaşılan kısmı alındı; her vurguya `kaynak_dokum`, `not` ve (öğrenci notuyla örtüşme) yazıldı; anlaşılmayan/slayta ters (Becker kardiyak tutulum) kayıtlar `hoca_vurgulari_dusuk_guven.md`'ye ayrıldı, pakete alınmadı.
- **Kural:** Sınav vurgusu tek dökümden çıkarılmaz; alıntı birebir döküm, anlaşılmayan sözcük "düzeltilerek" yazılmaz (düzeltme `not`ta); gen adı/sayı yalnız slayt ve/veya öğrenci notu ile örtüşünce vurgu olur; kaydın hangi slayttan başladığı rapora yazılır.

## H109 · v2 cümlesinin `ses` alanında iç cümle sonu: sunucu cümle sayısı v2 ile tutmuyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Belirti:** `konusma_v2.py --dogrula` 0 HATA verirken 4 cümlenin `ses` alanı ("Optik disk … çukurdur. Makula ise …") iki cümle içeriyordu; sunucu ve istemci bunu iki cümle sayar, v2/çapa/cümle zamanı/işaret/çıkmış konumu (`p`, `c`) tek cümle varsayar → çapa ve işaret bir cümle kayardı (`capa_baslangic` cümle sayısı tutmayan paragrafta v2 sayfasını kullanmaz).
- **Kök neden:** v2 doğrulayıcı `ses` içeriğini yalnız işaretleme/uzunluk bakımından denetliyordu; cümle sınırı kuralı (`pdf_hizala.cumle_sinirlari` = `canliDersStore.ts::cumleSinirlari`) v2 şemasında zorunlu değildi.
- **Çözüm:** `konusma_v2.dogrula` her `ses`'in tek cümle olmasını HATA sayar (`_cumle_sayisi`, sunucu kuralıyla aynı); yazar iki cümleyi iki v2 cümlesine böler. k2-01…k2-05 veride ihlal yok.
- **Kural:** her v2 `ses` tam bir cümledir; yazım betiğinde ayrıca kendi sınır kontrolü (cümle sayısı = 1, ≤25 kelime) çalıştırılır.

## H126 · Sesli ders ekranında gen sembolleri okunuşla görünüyordu: "hoks, o te iks, me se iks, paks 6" (2026-10-28, k2-08)
- **Belirti:** Beyin ve İskelet Sistemi Gelişimi Genetiği sesli dersinde ana metin "hoks, o te iks ve me se iks genleri ile göz geni paks 6" yazıyordu; doğrusu HOX, OTX, MSX, PAX6.
- **Kök neden:** Ders metni iki katmanlıdır: `ses` (EMA'nın okuduğu) ve `ekran` (v2 `cumleler[].ekran`, doğru yazımla). Ana paragraf ise `ses` metninden `ekranYazim.ts` ile geri çevrilerek gösterilir; bu geri çeviri sözlüğü (`yazim_sozlugu.json`) yalnız kaynak md'den türetiliyordu ve harf harf okunmayan / kelime gibi okunan gen sembollerini (hoks, paks, soks) hiç tanımıyordu. Sayı geçişi "altı"yı "6" yaptığı için "paks 6" gibi karma yazım çıktı. Sözlük ayrıca uzun süre yeniden üretilmediği için yeni derslerin kısaltmaları hiç girmemişti.
- **Çözüm:** `yazim_sozlugu.py` artık her v2 dersinin `ses` ↔ `ekran` cümle çiftlerini hizalayıp okunuş → yazım eşlemesini kendisi çıkarır ("hoks" → HOX, "paks altı" → PAX6, "ce o le bir a bir" → COL1A1); Türkçe sözcük, Roma rakamı ve rakamsız okunuşa rakamlı yazım eşlemeleri elenir.
- **Kural:** Ekran metni daima yazımla (HOX, PAX6), EMA metni okunuşla. Her yeni v2 metninden sonra `scripts/uretim/sesli_anlatim/yazim_sozlugu.py` çalıştırılır; sembollü cümlede `ekran` alanı boş kalmaz.

## H128 · EMA yabancı terimleri yanlış okuyor; anlatım konu geçişini söylemiyor; panel geç, zoom kısa anlatımda, çizim tek renk (2026-10-28)

- **Belirti:** EMA "Wernicke", "Staphylococcus", "locked-in", "Xanax" gibi yazımları Türkçe harf kuralıyla okuyordu. Başlıksız
  slaytta yeni konuya geçilince anlatım söylemediği için öğrenci önceki konuyla ilişkili sanıyordu. Liste/sıralama paneli
  anlatım başladıktan sonra açılıyordu; kısa değinmede zoom bitmeden slayt değişiyordu; resimden resme hızlı geçişte işaretler
  karışıyor, çizimler hep kırmızı ve hat tam izlenemiyordu.
- **Kök neden:** (1) EMA yolunda yalnız kısaltma katmanı vardı (okunus/kisaltma_ses); eponim/Latince/İngilizce terim
  sözlüğü yoktu. (2) Sesli ders talimatında kurgu (amaç, hiyerarşi, bölüm geçişinin ilişki türü, örnek) kuralı ve ön plan adımı
  yoktu. (3) Panel ilerlemesi `k0` = terimin söylendiği kelimeden başlıyordu. (4) Zoom yalnız bölge boyutuna bakıyordu,
  anlatım süresine bakmıyordu. (5) Kontur rengi CSS'te sabit kırmızıydı, boyama yalnız %13 sarı ışıltıydı, çizim hangi
  resim kutusuna ait olduğunu taşımıyordu.
- **Kalıcı çözüm:** `scripts/uretim/sesli_anlatim/terim_okunus.py` + `data/sesli_anlatim/okunus/terim_okunus.json` (eponim, Latince,
  İngilizce, ticari ad + Latince kural motoru) EMA'ya giden Kurul 2+/modül metnine uygulanır (`ema_isci.paragraf_seslendir`);
  `ses_temizle` (DC, RMS eşitleme, yumuşak tepe sınırı, 12 ms geçiş). `docs/ANLATIM_KURGU_STANDARDI.md` (plan → metin,
  ±%20 sayısal tolerans). `CizimLayer.tsx` panel cümle başından, zoom ≥55 karakter; `cizim_uret.py` ZOOM_EN_AZ=70, `renk_ata`,
  `renk/boya/resim` alanları; `cizim_dogrula.py` renk/resim kutusu denetimi.
- **Kural:** seslendirmeden önce `terim_okunus.py --denetle <anahtar>`, yanlış okunuş sözlüğe. Anlatım önce `anlatim_plani.md`; başlıksız konu geçişi söylenir. Çok resimde `resim: "R#"`, ayrı yapı ayrı renk, belirsiz bölge `boya: true`.

## H447 — Metni değişen paragrafların v2 cümleleri boş kaldı, ders ekranı ve çapası o paragraflarda eksik yayında (2026-10-30)
- **Belirti:** `k2-05-norolojik-muayene-v2` yayındaki sesli derste 9 paragrafın (Rinne/Weber çizimli 31–37, refleks türleri 59,
  duyu terimleri 65) v2 cümlesi yoktu (`cumleler: []`, kimlik `…-v2-yeni-pNNN`, `sayfa` yok); `konusma_v2.py --dogrula` 27 HATA veriyordu.
  Ses klipleri metinden üretildiği için ders çalıyordu ama bu paragraflarda ekran maddesi, vurgu ve v2 slayt çapası yoktu.
- **Kök neden:** `klip_tasi.py` metni değişen paragrafı v2'de bilerek boş bırakır ("konusma_v2 ile yazılmalı"); 2026-10-28 dağıtımında
  bu adım atlandı (DEGISIKLIK_KAYDI'nda "yazılmadı" diye not düşüldü) ve yayın hattında v2 doğrulaması zorunlu kapı değildi.
- **Çözüm:** 9 paragraf metin değişmeden dolduruldu (eski v2'de birebir aynı kalan 17 cümle kimliğiyle geri alındı, kalanlar yeni
  kimlikle yazıldı; paragraf kimlikleri `k2-05-pNNN` biçimine döndü); `konusma_v2.py --dogrula` 0 HATA.
- **Önleme:** `klip_tasi.py` "v2: N paragraf boş" raporu verdiyse o ders, boş paragraflar `konusma_v2` biçiminde yazılıp
  `konusma_v2.py --dogrula <dizin>` (kaynak.md ile) 0 HATA verene dek dağıtılmaz; açık iş olarak not düşmek yerine aynı oturumda kapatılır.

## H448 — `klip_tasi.py` metinle birlikte düzenlenmiş v2'yi eski metne göre yeniden kurup değişen paragrafları boşaltıyordu; `ders-ekle` elle iyileştirilmiş çapayı ezdi (2026-10-30)
- **Belirti:** k2-05-v2'de 9 paragraf metni ve v2'si birlikte düzeltildi; `klip_tasi.py --kuru` "v2: 17 bölüm yeniden kuruldu, 9 paragraf boş" dedi
  (çalışsaydı yeni yazılan cümleler silinecekti). Ardından `sesli_yayinla.py` → Oracle `ders-ekle`, `capa/<key>.json`'ı v2 satırlarından
  türeyen kaba çapayla değiştirdi; oturumda elle yazılmış madde/resim/kutu/yol çapaları (78 paragraf) Oracle'da kayboldu.
- **Kök neden:** (1) `klip_tasi` v2 için yalnız paragraf SAYISINA bakıyordu: sayı eski metinle aynıysa "eski metinle tutarlı" sayıp yeniden
  kuruyordu; paragraf sayısı değişmeyen düzeltmede v2'nin zaten yeni metne uyduğu anlaşılmıyordu. (2) `ders-ekle` `capalar` gelince çapa
  dosyasının tamamını yazar; değişmeyen paragrafların daha iyi çapası korunmaz.
- **Çözüm:** `klip_tasi` cümle seslerinin birleşimi yeni paragraf metniyle aynıysa v2'ye dokunmaz. Çapa: yereldeki taşınmış çapa esas alındı,
  değişen paragraflarda değişmeyen cümleler eski çapayı (git HEAD) geri aldı, yeni cümleler satırdan `pdf_isaret.capa_maddeleri` ile madde
  dizinine çevrildi; `capa_dogrula` %98, 0 HATA; çapa Oracle'a yeniden yazıldı.
- **Önleme:** yayımlanmış ders metni düzeltilince `sesli_yayinla.py`'den SONRA yerel çapa Oracle'a kopyalanır, `pdf_isaret.py --key <key> --zorla` (H93); `ders-ekle` çapasına güvenilmez.

## H468 — Hoca dökümü sessizce CPU'ya düştü; turbo dökümü konuşmanın üçte birini kaçırdı (2026-11-02, Kurul 2 2. parti)

- **Belirti:** k2-10 dökümü "GPU saati 2500 MHz'i aştı; bu oturum CPU" ile çok yavaş ilerledi; tamamlanınca turbo modeli 48,6 dk
  kaydın yalnız ~2000 sn'sinde konuşma buldu, "İzlediğiniz için teşekkür ederim" sanrıları ve bozuk terimler vardı; hocanın vurgu
  ifadelerinin bir kısmı hiç dökülmedi.
- **Kök neden:** (1) Kalıcı saat kilidi (`nvidia-smi -lgc 300,2500`) yeniden başlatmada kalkıyor; `hoca_dokum.py` kilit yoksa doğru
  davranıp CPU'ya düşüyor ama hat bunu uyarı olarak göstermiyor. (2) Tek model (large-v3-turbo) amfi kaydında tıbbi terimleri ve
  kısık konuşmayı kaçırıyor; vurgu kaydı tek dökümden çıkarılıyordu.
- **Çözüm:** saat kilidi kuruldu, döküm GPU'da yeniden alındı (≈2–3 dk/ders); her derse ikinci döküm (Systran medium,
  `hoca_dokum_medium.json`, `meds_temp/ogrenci_ders/dokum_medium.sh`) alındı ve vurgu/anlatım kayıtları iki dökümle çapraz okundu
  (k2-10'da 23 yeni kayıt, 2 yeni sınav vurgusu; anlaşılmayan "her hafta olan ağrı daha önemli" kaydı düşük güvene alındı,
  ona dayanan anlatım cümlesi silindi).
- **Önleme:** E0 öncesi `nvidia-smi --query-gpu=clocks.max.sm` ≤2500; günlükte "bu oturum CPU" görülürse durdurulur. Vurgu iki dökümle çapraz okunur; tek dökümde kalan, slayta bağlanmayan söz dayanak olmaz.

## H469 — Kurul 2 EMA yolu büyük harfli kısaltmayı okumuyordu (NMDA, GABA, IP3) (2026-11-02)

- **Belirti:** k2-09 farmakoloji metni kısaltmaları yazımla tutuyordu (NMDA, AMPA, MSS, IP3); `ema_isci.tts_metni` Kurul 2 yolunda
  bunları olduğu gibi EMA'ya veriyordu (sınamada "NMDA reseptörü" → çevrilmemiş); GABA/AMPA hoca gibi kelime olarak okunmuyordu.
- **Kök neden:** Kurul 2 uzun-kısaltma yolu (`kisaltma_ses.uzat`) yalnız okunuşla yazılmış hece dizilerini ("de ne a") tanır; H23
  "metin yazımla, okunuşu EMA katmanı yapar" kuralı yalnız modül/ajan anahtarlarında (`modul_okunus.modul_mu`) uygulanıyordu.
  Önceki Kurul 2 dersleri metni okunuşla yazdığı için fark edilmedi.
- **Çözüm:** bu partinin yazımla yazılmış anahtarları `modul_okunus.MODUL_ANAHTARLAR`'a eklendi; `KELIME`'ye GABA/GABAA/GABAB/AMPA/
  DOPA/VMAT/VGLUT/mGluR/HANDLE/SUNCT/KİBAS; `okunus.FONETIK_TTS`'e GABA/AMPA/L-DOPA; `terim_okunus.json`'a Schneider, Renshaw,
  Wall, Head, Graham, Leao, locus coeruleus, substantia gelatinosa, déjà vu ailesi. EMA işçisi yeniden başlatıldı (modüller
  açılışta yüklenir).
- **Önleme:** Yeni Kurul 2 dersinin metni yazımla tutuluyorsa anahtarı seslendirmeden ÖNCE `MODUL_ANAHTARLAR`'a eklenir ve
  `ema_isci.tts_metni` ile örnek paragraf okunuşu denetlenir; okunuş sözlüğü değişince `meds-ema` yeniden başlatılır.

### H501 — Hoca dökümü sarmalayıcısı model seçimini yutuyordu; turbo dökümüyle hocanın sözü yanlış okundu (2026-11-06)
- **Belirti:** KMB 01'de "ölçüm sınavda en çok hata yapılan basamak" yazıldı; hoca aslında öğrencilerin farklı sırayla ölçtüğünü, bunun teorik olarak aynı olduğunu, burundan başlamanın kolay olduğunu söylüyordu. Sınav biçimi (34:03 "malzeme seçtiririm, basamakları sorarım") dökümde hiç yoktu.
- **Kök neden:** `hoca_dokum_gpu.sh` yalnız iki argüman aktarıyordu; `--model large-v3` sessizce yok sayıldı, turbo modeli bozuk/eksik döküm verdi; yazar belirsiz pasajı yorumla doldurdu.
- **Çözüm/önleme:** sarmalayıcı kalan argümanları aktarır (`"$@"`). Hocanın sınav vurgusu içeren ders kayıtları `--model Systran/faster-whisper-large-v3` ile dökülür; belirsiz pasaj içerikte iddiaya çevrilmez, zaman damgasıyla "emin değil" listesine yazılır.

### H508 — Drive'daki ses dosyasının adı başka dersi gösteriyordu: "TSSB Psikaytr 2" aslında EKT (Tedaviler) dersinin başıydı (2026-11-06)
- **Belirti:** Kullanıcı "psikiyatri için bazı derslerden ikişer ses var" dedi; TSSB iki kayıt birleştirildi, k2-20 (Tedaviler) ise s1–7 için "kayıtta yok" görünüyordu.
- **Kök neden:** Öğrenci Drive'ında dosya adı içerikle eşleştirilmeden derse bağlandı (ad = "TSSB … 2"). Döküm hizalanınca 2. kaydın EKT tarihçe/etki kuramları/hazırlık/endikasyon anlattığı ve TSSB slaytlarının hiçbirine düşmediği görüldü; k2-20 ana kaydı s8 sonundan başlıyordu.
- **Kalıcı çözüm:** 2. kayıt k2-20'nin başı ("ek" kayıt, s1–8) olarak hizalandı; TSSB yalnız 1. kayıttan işlendi.
- **Önleme:** Ses dosyası adla değil içerikle eşleşir (KURUL2_DERS_STANDARDI §1): slayta düşmeyen ≥3 dk blok "ders dışı" işaretlenip kurulun öbür dersleriyle karşılaştırılır.

### H530 — Kısık amfi kaydında hoca dökümü uydurma cümlelerle doluyordu (2026-11-10, k2-22/23/24/58)
- **Belirti:** Kullanıcının yüklediği hoca kayıtlarının ilk dökümünde (turbo model, ham ses) metin "İzlediğiniz için teşekkür ederim", uydurma özel adlar ve anlamsız cümlelerle doluydu; hangi dersin kaydı olduğu bile zor seçiliyordu.
- **Kök neden:** kayıtların ortalama düzeyi −31 dB (telefon amfinin arkasında); `hoca_dokum.py` her kaydı ham sesle ve varsayılan `large-v3-turbo` ile çözüyordu. Kısık seste Whisper sessiz/gürültülü parçaları eğitim verisindeki altyazı kalıplarıyla dolduruyor. 3 dk'lık aynı parçada ham+turbo en kötü, süzgeç (90 Hz–7,5 kHz, afftdn, dynaudnorm) + `Systran/faster-whisper-large-v3` en anlaşılır sonucu verdi.
- **Çözüm/önleme:** `hoca_dokum.py` ilk 10 dk −28 dB'den kısıksa süzgeç + normalleştirme uygular (normal kayıtta ham ses); kısıkta `--model Systran/faster-whisper-large-v3`. Kaydın dersi dosya adından değil içerikten belirlenir.

### H532 — CPU'lu `meds-ema` birimi açıkken ders EMA işi GPU yerine CPU'ya düşebiliyordu (2026-11-10)
- **Belirti:** GPU'lu EMA işçisi beklerken `meds-ema.service` (yalnız CPU, aynı `ema-yerel` kuyruğu) da etkindi; kuyruğa giren işi hangisinin alacağı belirsizdi (kullanıcı kararı 2026-10-24: EMA DAİMA GPU).
- **Kök neden:** iki işçi aynı sağlayıcı adıyla `/yerel/al` soruyor; birim hâlâ açılışta başlıyor.
- **Çözüm/önleme:** ders sesinden önce `systemctl --user stop meds-ema` + `cozucu_ses_gpu.sh scripts/uretim/sesli_anlatim/ema_isci.py bekle`; günlükte "EMA Lightning hazır: cuda" görülür, bitince birim yeniden başlatılır.

### H538 — 5. parti derslerinin anahtarları `MODUL_ANAHTARLAR`'da yoktu: yazımla tutulan kısaltmalar (DSM, EEG, SSRI) harf harf okunmamış olabilir (2026-11-09)
- **Belirti:** `ema_isci.tts_metni("DSM beş TR …")` k2-21 anahtarıyla metni değiştirmeden döndürdü; k2-22 anahtarı (eklendikten sonra) "dee see mee beş tee ree" verdi.
- **Kök neden:** H469 önlemi ("yeni ders anahtarı seslendirmeden ÖNCE `MODUL_ANAHTARLAR`'a eklenir") 5. partide (k2-19, 20, 21, 37, 38) uygulanmadı; kontrol listesinde yoktu.
- **Çözüm:** 6. parti anahtarları eklendi (k2-22, 23, 24, 58). **Açık:** k2-19/20/21/37/38 sesleri bu yolla üretildiği için kısaltma okunuşu dinlenip gerekiyorsa anahtar eklenip yalnız ilgili klipler yeniden üretilmeli (kullanıcı kararı).
- **Önleme:** `sesli_yayinla.py` yeni anahtarı `modul_okunus.modul_mu` ile denetleyip değilse uyarır (yapılacak); el kitabı §19 adım 8'e madde.

### H539 — EMA tam MP3 yüklemesi Oracle'daki başka bir dağıtımın sunucu yeniden başlatmasına denk gelince iş "hata"ya düştü (2026-11-09, k2-22)
- **Belirti:** 50 klip üretildi, `PUT …/tam` 23:33:24'te bağlantı hatası aldı; Oracle kuyruğunda iş `durum: hata`, ders sessiz kaldı; işçi günlüğü systemd scope'ta olduğundan `journalctl -u meds-ema` boştu.
- **Kök neden:** aynı dakikada başka oturum `dagit.sh` ile konteyneri yeniden başlattı; işçi tek denemeyle bırakıyor.
- **Çözüm:** `POST /api/sesli-anlatim/uret {key, saglayici: ema-yerel, ses: Ema}` ile yeniden kuyruklandı; klipler yeniden kullanıldı (0 yeni klip).
- **Önleme:** `dagit.sh` kuyrukta `calisiyor` EMA işi varken beklemeli ya da işçi `tam/bitir`'i 3 kez yinelemeli (yapılacak).

### H540 — `kelime_zaman.py --gpu` elle çağrıda `libcublas.so.12` bulamayıp sessizce CPU'ya düştü (2026-11-10)
- **Belirti:** k2-22/23 kelime zamanı 1179 sn (CPU); günlükte tek satır "CUDA hatası … bu oturum CPU".
- **Kök neden:** CUDA kitaplıkları `.venv-hizala` pip `nvidia-*` paketlerinde; `LD_LIBRARY_PATH` yalnız `meds-kelime-zaman-hat.service` biriminde tanımlı, betik kendisi eklemiyor.
- **Çözüm:** elle koşuda birimdeki `LD_LIBRARY_PATH` dışa aktarıldı (k2-24/58 GPU'da 345–351 sn).
- **Önleme:** `kelime_zaman.py` başında `nvidia/*/lib` yollarını `LD_LIBRARY_PATH`'e kendisi ekler (yapılacak); CPU'ya düşüş UYARI değil, belirgin HATA satırı olmalı.

### H586 — Çözücü/asistan/Öğren/terim/ek modül seslerinde terim okunuşu ve kısaltma yolu uygulanmıyordu; okunuş 9 yerde, `seslendir` 4 kopya (2026-11-16)
- **Belirti:** Kurul 2 çözücü ve asistan kliplerinde eponimler düz okunuyor (Williams), kısaltmalar bitişik okunuyor (H3 tekrarı); yeni branşta okunuş eksik kalıyor (H538 tekrarı). Sıradan "engel" sözcüğü "Engıl" okunuyordu; 1000 ve üstü sayıda `modul_okunus` IndexError veriyordu.
- **Kök neden:** okunuş yolu içerikten değil elle tutulan `MODUL_ANAHTARLAR` listesinden seçiliyordu; çözücü/asistan/ek modül yolları `uzun_kisaltma_ayarla`'yı hiç çağırmıyordu; her modül `seslendir`'i kopyalayıp ortak durumu (`E.KBPS`, `E.okunus.duzelt`) çalışırken eziyordu. Eponim sözlüğünde küçük harfli genel sözcükle çakışan giriş (`engel`) vardı.
- **Kalıcı çözüm:** `scripts/uretim/ses_ortak/ses_metin.py::hazirla` (tek okunuş girişi; kurul ders kayıt defterinden/klasörden; bilinmeyen modülde uyarı yazar, sessiz eski yola düşmez), `ses_klip.py` (tek `seslendir/klasor/cumlele`; bit hızı ve okunuş parametre), altı betik ortak modüle bağlandı. Klip karma formülü DEĞİŞMEDİ (sahte motorla eşdeğerlik: karma farkı 0). Yeni klip kaydına `okunus_surum` yazılır. Eski kliplerde okunuşu değişecek 17.225 klip `meds_temp/ses_ortak/okunus_farki.jsonl`'de (yeniden üretim yalnız kullanıcı komutuyla, GPU).
- **Güncelleme (aynı gün):** kurul seçimi yalnız ders defterine bakıyordu → Öğren desteleri (`learn-*`, `deck-*`) ve defterde olmayan `k1-67…69` 93 kez "kurul bulunamadı" uyarısıyla Kurul 2 uzun yoluna düşüyordu. Kök: anahtar biçiminin ve deste kaydının kurulu taşıdığı yok sayılmıştı. Çözüm: `ders_kurulu` = defter → deste kaydı `committee` ("Kurul 1 - …", `deste_deposu.hepsi()`, süreçte bir kez) → biçim kuralı (`k1-67-…`, `k2p-…`, `y25-k2-…`); `kmb` Kurul 1 klasörü. Uyarı 93 → 0; okunuşu değişecek klip 17.225 → 16.969 (Öğren 6.731 → 6.480; kalan fark Kurul 1 destelerine eklenen terim okunuşu). Metin düzeyi denetimde düzeltilen hatalı dönüşümler: TAMAMI BÜYÜK Türkçe başlık harf harf ("[SINAV SPOTU]", "TOPUK KANI…"), "LGV'de de" → "dee dee", "B)"/"C." şık etiketi, "I ve III" → "ıı", küçük harfli "sperm" → "spörm", "In vivo", "checkpoint" → "kekpoint", girdideki simge (PUA) karakteri çökmesi. Sınama `ses_ortak/sinama_okunus.py` (54 satır, 0 HATA) — okunuş kuralı değişince önce o çalıştırılır.
- **Önleme kuralı:** ses betiği okunuşu yalnız `ses_metin.hazirla`, klibi yalnız `ses_klip` ile üretir; `E.*` ezilmez. Okunuş yolu değişince toplu üretimden önce 10 kliplik dinleme sınaması (kısaltma, şık etiketi, "O", "dede"). Sesli ders ortak yola yalnız `MEDS_OKUNUS_ORTAK=1` ile (kullanıcı kararı).

### H587 — Öğren destesinde 16 klip 14–22 dakika sürüyordu; ses için kalite kapısı yoktu (2026-11-16)
- **Belirti:** `ogren_ses/learn-tumor-biyolojisi-terminolojisi` destesinde 16 klip 865–1355 sn (normalin 5–9 katı); tek cümle 811 sn. Öğrenci bildirimi gelmeden, taramada bulundu.
- **Kök neden:** motor tablo metninde durmayıp konuşmaya devam etmiş; üretimdeki tek denetim süre/karakter oranının 3 tohumla yeniden denenmesiydi ve üçü de başarısız olunca klip yine yazılıyordu. Üretim sonrası hiçbir denetim (bozuk/yarım/sessiz klip, düzey, kırpılma, kayıt↔disk, Oracle boyutu) yoktu. H539: tam MP3 yüklemesi tek denemeydi.
- **Kalıcı çözüm:** `scripts/uretim/ses_ortak/ses_kapisi.py <modül|ders>` / `tara --hepsi` / `oracle` / `artik` (ffprobe + volumedetect/silencedetect; 91.399 seste yanlış alarm 0), `scripts/kapilar/matris.json` `ses` aşaması; `yerel_sesleri_tasi.py --dogrula` (Oracle boyut karşılaştırması, her aktarım sonunda); `ema_isci.py` tam yükleme 3 deneme; GPU ses işleri tek kilit (`cozucu_ses_gpu.sh`).
- **Güncelleme (aynı gün):** 16 klibin tamamı `learn-tumor-biyolojisi-terminolojisi` (2026-10-22 üretimi), oran 3,2–9,3; kök girdi: slayt metnindeki kutu çizimi tablolar (┌─│└, tek "cümle" 77–1.086 karakter, cümle oranı 12–39) motoru durmadan konuşturmuş; `paragraf_seslendir` üç tohumda da tutmayınca en iyi kötü sesi döndürüyor, `ogren_ses_uret` notu yalnız ekrana basıp klibi ve kaydı yazıyordu (kayıtta `not` alanı da yoktu). Çözüm: `ses_klip.seslendir` üç tohum da eşik dışıysa `BozukKlip` fırlatır; `klasor`/Öğren/kamp/çözücü-alt klibi YAZMAZ, `meds_temp/ses_ortak/uretim_bozuk.jsonl`'e yazar, süreç çıkışı 3 (sahte motorla sınandı); `ses_metin` kutu çizimi karakterlerini temizler ve >400 karakterlik parçayı motora bölerek verir (karma değişmez). Liste: `meds_temp/ses_ortak/bozuk_klipler.json`. `.parca/` (14 günden eski) ve kayıtsız sesli ders MP3'ü `veri_bakim.py` arşiv adayı. Kalan kopyalar (kamp, çözücü-alt, kmb, motivasyon) ortak modüle bağlandı; karma farkı 0.
- **Önleme kuralı:** ses üreten her iş yayından önce `ses_kapisi.py` 0 HATA verir; süre/karakter oranı üç tohumda da tutmayan klip yazılmaz, hata olarak raporlanır. Bozuk 16 klip yeniden üretilecek (GPU, kullanıcı komutu).

## H595 — Öğren sesinde tek başına sıra imi ("2.") ayrı cümle → bütün adım reddedildi (2026-11-17)

- **Belirti:** `ogren_ses_uret.py learn-tumor-biyolojisi-terminolojisi --force` 35 adımdan 3'ünü üretti, 32'si "süre oranı 0.48 (3 denemede düzelmedi): 2." ile reddedildi; H587'deki 16 bozuk klibin 14'ü kapıda HATA kaldı.
- **Kök neden:** `scripts/uretim/ogren_ses/ogren_ses_uret.py:95` `cumlelere_ayir` (eski hâli satır 92–93) `(?<=[.!?])\s+` ile böldüğü için numaralı listedeki "1." / "2." TEK BAŞINA cümle oluyordu; `ses_klip.seslendir` bu ~0,5 sn'lik parçada süre/karakter oranını eşik dışı görüp `BozukKlip` fırlatıyor, adım bütünüyle yazılmıyordu (H587 koruması doğru çalıştı; girdi bölmesi yanlıştı).
- **Kalıcı çözüm:** `_SIRA_IMI` (sayı/harf/Roma + `.`/`)`, ya da `- – — • * · ▪ ►`) ile tam eşleşen parça sonraki cümleye yapıştırılır; okunuş (`ses_metin`) ve denetim eşiği değişmedi. Önce/sonra: 12.232 Öğren slayt metninde 2.186 fark, farkların tamamı tek başına sıra imi içeren metinlerde (iki yönlü assert); geri kalan metinlerde cümle listesi (dolayısıyla klip karması) birebir aynı. Yeniden üretim: 32/35 adım üretildi; kalan 3 (adım 18, 24: kutu çizimi tablo; adım 32: "<%0.1") ayrı kök, kapıda 3 HATA.
- **Önleme kuralı:** ses cümle bölücüsü sıra/madde imini ayrı cümle bırakmaz; bölme değişikliği tüm gerçek metinlerde eski/yeni karşılaştırmasıyla kanıtlanır. Süre eşiği gevşetilmez.

### H605 — Son derslerde PDF ↔ metin takibi zayıftı: cümlelerin %19–24'ü yalnız sayfa vurgusu alıyordu (2026-11-17, kullanıcı bildirdi)
- **Belirti:** k2-49, k2-50, k2-62 gibi son derslerde okunan cümle slaytta işaretlenmiyor, yalnız sayfa yanıyordu; k2-49/50'de kelime takibi de yoktu.
- **Kök neden (üç katman):**
  1. **Hat kapıyı çağırmıyordu:** `kosucu.py` `zaman_isaret` adımı yalnız `cumle_zaman`/`kelime_zaman`'ı anıyordu; `pdf_isaret.py` ve
     `takip_kapisi.py` adımda yoktu → k2-49/50 kelime zamanı olmadan, k2-26/27/29/62/65 cümle zamanı olmadan yayına girdi; kimse fark etmedi.
  2. **OCR'lı/şemalı sayfada yanlış geri düşüş:** çapa satırı görselin içindeki etiketse ("Oculomotor nerve (III)") metin eşleşmez;
     geri düşüş `not sy.ocr` koşulu yüzünden görsele gidemiyor, "sayfa"ya düşüyordu (k2-62: 166 cümlenin 40'ı).
  3. **Tasarruf kipi çapasız:** E4 (çapa+çizim) tümüyle atlanınca genişletilmiş anlatım slayttaki maddeye yalnız sözcük eşlemesiyle
     bağlanır; LCS ≥2 ortak kök ister, "en az beş" ↔ "en az 5" gibi sayılar bile tutmuyordu.
- **Çözüm:** `pdf_isaret.py` SURUM 8 — yazıyla sayı = rakam (`SAYI_SOZ`); çapalı/çapasız cümlede eşleşme yoksa görselli sayfada
  (OCR, satır çapası ya da <15 kelime) lazer görsele; çapasız cümlede `zayif_esle` (atanan sayfada yalnız TEK maddede geçen ≥2 kök
  ya da bir sayı; eşitlikte işaret yok). Tüm dersler yeniden üretildi: 40.170 cümlede yalnız-sayfa 2.780 → 1.775, kötüleşen ders 0.
  `kosucu.py` adımına `pdf_isaret.py` + `takip_kapisi.py` 0 HATA kapısı yazıldı.
- **Denenip bırakılan:** bge-m3 vektör eşlemesi (CPU) çapasız cümlede 1. ve 2. aday farkı 0,01–0,1 → tahmin; kullanılmadı.
- **Önleme kuralı:** (a) Takip kapısı yayından önce atlanamaz; kelime/cümle zamanı eksik ders yayına girmez. (b) Çapasız ders T5 ≤%5'i
  sözcük eşlemesiyle TUTTURAMAZ (k2-49/50 ≈%18: giriş/özet/açıklama cümleleri) — eşiği gevşetmek ya da tek genel kelimeyle işaret
  uydurmak YASAK; çözüm çapadır. Tasarruf kipinde çizim atlanır ama çapa için yalnız eşleşmeyen cümleler (metin-only M# listesi,
  görüntüsüz) yazılır: `artik_capa` katmanı (her kipte; `scripts/uretim/sesli_anlatim/artik_capa.py hazirla|birlestir`). k2-50 denemesi:
  13 artık cümle, iş dosyası ~1.000 kelime (≈1,6k token) → yalnız-sayfa 13/66 → 3/66 (%4,5), T5 geçti.

### H606 — Kurul 3 arşivinde işaret "çapa sayfasından kayıyor", tablo/şema cümleleri yalnız sayfaya düşüyordu (2026-11-17)
- **Belirti:** `y25-k3-11-sindirim-sistemi-kanserleri` takip kapısı T5'te 12 HATA ("işaret s.13 ≠ çapa s.12", "işaretlerin %9'u yalnız
  sayfa"), `y25-k3-16-primer-biliyer-kolanjit` %5 sınırında HATA; bu dersler yayına giremiyordu.
- **Kök neden (iki katman):**
  1. **Komşu sayfadan görsel ödünç alma:** `pdf_isaret.capali` şekil çapasında çapanın sayfasında görsel bulamazsa ±1 komşu sayfaya
     bakıp oradaki resmi işaretliyordu. Çapa s.12, görsel s.13 → oynatıcı yanlış slaytı gösterir, T5 haklı olarak HATA verir.
  2. **Türkçe anlatım / İngilizce slayt:** tablo sayfalarında slayt metni İngilizce ("Combination"), anlatım Türkçe olduğu için kelime
     eşleşmesi tutmuyor; çapa satırı PDF'te tek simgeye ("≥1:40" → `#1`/`#40`) ayrışınca `capa_maddeleri` %80 eşiğini geçemiyor ve
     cümle "yalnız sayfa" işaretine düşüyordu.
- **Çözüm:** `arsiv_yayinla.pdf_isaret_yerel` — işaret her zaman ÇAPA sayfasında üretilir (`_ayni_sayfa`: satır→madde→kelime→resim
  sırası), çapa eşiği tutmazsa en yakın madde (`_yakin_madde`, ≥%40 kök) kullanılır, kalan `sayfa` işaretleri `_doldur` ile o
  sayfanın tablo/resim bölgesine bağlanır. Sonuç: iki ders T1–T5 **0 HATA** ile yayına girdi.
- **Önleme kuralı:** İşaret yalnız çapanın sayfasında üretilir (komşu sayfa yalnız çapa sayfası yoksa, `capali` içinde); eşleşmeyen cümle madde/kutuya bağlanır, "sayfa"ya düşmez; eşik gevşetilmez.

### H607 — Arşiv metin üretimi görsel/şema sayfalarında "yanıt yok" verip sayfayı anlatımsız bırakıyordu; ders yayına giremiyordu (2026-11-17)
- **Belirti:** k3 parti işlerinde derslerin çoğu `hata:metin` ile duruyordu; kapsam kapısı "s.9: anlatılmamış (görsel var)" diyordu.
  Aynı sayfa tek başına sorulduğunda model doğru JSON üretiyordu.
- **Kök neden (üç katman):**
  1. **Uzun istem + büyük çıktı sınırı:** 9 bin tokenlık kural bloğu + `max_tokens=9000` ile geçit modeli (`deepseek-v4.1-flash`)
     görsel/şema sayfasında **boş yanıt** dönüyordu; kod bunu "sayfa üretilemedi" sayıp geçiyordu. Tek başına kısa istemde aynı sayfa
     sorunsuz üretiliyordu (ölçüldü: 3151 karakter istem → boş, 2092 karakter → dolu).
  2. **Yazısız klinik fotoğraf:** metin katmanı ve OCR boş olduğu için modelin elinde hiç bilgi yoktu (k3-36 s.6/13/14/20/21).
  3. **Gate kendi kendini doğrulamıyordu:** tek-cümle (H109), Türkçe üslup ve bağlamsız açılış (H434) denetimleri yalnız **yayın**
     kapısında vardı; tur içinde yakalanmadığı için üretim "0 HATA" sanılıp yayında patlıyordu.
- **Çözüm:** `k3_uret.py` — (a) boş yanıtta 3 kez yineleme, (b) görsel/az-yazılı sayfada **önce kısa istem** (`istek_kisa`),
  (c) yazısız görselde bölüm başlığı ve komşu sayfalarla ilişkilendiren `gorsel_yedek`, (d) görsel sayfada OCR katmanı (`ocr_metni`,
  Tesseract tur+eng, önbellekli), (e) `denetle_sayfa`'ya H109/üslup/H434 denetimi, (f) H109'u kodla garanti eden `cumlelere_bol`,
  (g) H494 kısa çapa filtresi (`capa_bul`), (h) `--tsv-yenile` (LLM'siz biçim onarımı). Ayrıca `k3_onar.py`: kapının bildirdiği
  eksik sayfaları tek tek üretir.
- **Önleme kuralı:** Üretim adımı yayın kapısı denetimlerini kendi içinde koşmadan "0 HATA" demez; boş yanıt = yeniden dene + kısa istem; yazısız görselde yalnız bölüm/komşu başlık bağlamı, kaynak dışı bilgi yok.

### H609 — Zengin transkript tablo ayrıştırıcısı sayı sözcüğünü kesiyordu (2026-11-17, geliştirme sırasında)
- **Belirti:** ilk sürümde "yüzde kırk dokuz" tabloda "yüzde kırk", "beş yaşında" satırı "yalnızca" olarak çıktı.
- **Kök neden:** oran, gevşek ek kalıbıyla (`ikisi|ine|e|…`) yakalanıyordu; Türkçe çok sözcüklü sayı ilk sözcükte kesildi, koşul sütunu yaş ifadesi yerine rastgele ilk sözcükten alındı.
- **Kalıcı çözüm:** `zengin_transkript.py` oranı sayı sözcüğü listesiyle tam yakalar, koşul sütunu yaş ifadesi ister; herhangi bir satır eksikse tablo hiç kurulmaz, cümle madde olarak kalır.
- **Önleme:** yapı (tablo/sıra) çıkaran betik emin değilse yapı kurmaz, cümleyi korur; tıbbi sayı kesilmez.
### H612 — k2-33/34/35 kelime zamanı yoktu; izleyici yanlış alarm verdi (2026-11-17)
- **Belirti:** sesli derste kelime kelime takip k2-33, k2-34, k2-35'te çalışmıyordu; hata izleyicisi 12 derste "cumle_zaman dosyası yok" dedi.
- **Kök neden:** kelime zamanını üreten yerel `meds-kelime-zaman-hat.timer` devre dışıydı (Kurul 2 sesleri yalnız Oracle'da; kelime zamanı yerel GPU ile çözülüp gönderiliyor). Cümle zamanı ve işaret ise Oracle'da `meds-cumle-zaman.timer` ile üretiliyor, yerelde kopyası yok; takip kapısı yerel dosyaya bakınca 12 sağlam dersi "yok" saydı.
- **Kalıcı çözüm:** üç ders `kelime_zaman.py --key <ders> --oracle --gpu` ile (gpuguard açık) çözüldü, canlıda 64/64, 39/39, 39/39 paragraf. `hata_izleyici.py` takipte yerel dosya yoksa canlı API'de paragraf başına kelime zamanını denetler.
- **Önleme:** yayından sonra `kelime_zaman.py --hepsi --saglayici ema-yerel --oracle --gpu` elle (`zaman_isaret`; zamanlayıcı kapalı, kural 20); Oracle katmanı yerelde "yok" sayılmaz.


### H629 — Eski ses varyantı yalnız yerelde silinince dagit.sh Oracle'dan geri getirdi; yedek dosyaları kayıt kapısını kilitledi (2026-11-18)

- **Belirti:** k2-36/k2-39'da silinen eski ses varyantları dağıtımdan sonra yerelde yeniden belirdi; ayrıca `kos.py kayit` 6 K4 HATA verip başka oturumların commit'lerini engelledi.
- **Kök neden:** Sesli ders kaydının (`kayit.json`, MP3, `cumle_zaman`/`kelime_zaman` varyantları) kaynağı Oracle; `dagit.sh` "Oracle → yerel" adımı eksik kayıtları yerele geri yazar. Arşivlemede bırakılan `.yedek` dosyaları da K4 kuralına takıldı.
- **Çözüm:** Varyant önce Oracle'dan (kayıt + MP3 + zaman dosyaları, yedekle) sonra yerelden çıkarıldı, `meds-server` yeniden başlatıldı; yedekler `_arsiv_veri/`'ye sıkıştırıldı.
- **Kural:** Ses varyantı kaldırırken önce Oracle'da, sonra yerelde sil ve `meds-server`'ı yeniden başlat; yedeği `_arsiv_veri/` altında `.zst` olarak sakla, `data/` içinde `.yedek` bırakma.

### H657 — Kurul 3 arşivinde metin üretimi "0/75 sayfa, hata:metin" oluyordu: kelime tavanı kapıda ölçeklenmiyordu (2026-11-25)
- **Belirti:** `k3_parti.py` ile 60+ sayfalık arşiv dersleri (k3-52 76, k3-53 58, k3-54 46, k3-56 49, k3-57 67 …) `hata:metin` ile
  düşüyordu; ayrıca `k3-01` 133/133 sayfası üretildiği hâlde kapı "kelime 12754 > 6000" diyerek derdi reddediyordu.
- **Kök neden:** kelime tavanı `metin_denetle.py` içinde `MEDS_METIN_MAX_W` ile sayfa sayısına göre ölçeklenir (H618) ve bunu
  `k3_yayinla.kapilar` ortama koyuyor; ama üretim yolunun kapısı (`k3_uret` → `k3_metin.kapilar`) bu değişkeni **hiç koymuyordu**.
  Aynı ders iki yolda iki farklı tavana çarpıyordu; uzun derste metin doğru üretilse bile kapı onu kesik sayıp "hata:metin" yazıyor,
  yayın kuyruğuna hiç girmiyordu.
- **Kalıcı çözüm:** `k3_metin.kapilar` da `MEDS_METIN_MAX_W = max(6000, sayfa × 140)` kuralını uygular (tek kaynak: `metin_denetle.MAX_W`).
  `k3-01` yeniden kapıdan geçirildi (0 HATA, yalnız uyarılar) ve yayın kuyruğuna alındı.
- **Önleme kuralı:** bir dersin kapıları **iki ayrı betikte** koşuyorsa eşik/ortam değişkenleri tek yerden türetilir; üretim kapısı ile
  yayın kapısı aynı ortamı kurar. "Kapı 0 HATA" diyen her yol, ölçeklenen eşiği kendisi hesaplamak zorunda.

## H684 — Sesli ders ekranında "M bir, M üç" yazıyordu; doğrusu M1, M3 (2026-11-25)
- **Belirti:** Kolinoseptör/otonom farmakoloji derslerinde metin takipçisi ve zengin transkript "M bir ile M beş", "M iki ve M dört reseptörleri" gösteriyordu.
- **Kök neden:** Ekran metni `ses` okunuşundan `src/services/ekranYazim.ts` ile geri çevrilir. Tek harf + sayı birleştirmesi yalnız C (kompleman) için vardı; ayrıca tek başına "bir" belgisiz sıfat sayıldığından rakama dönmüyordu. M1, H2, T4, B12 gibi tek harfli kodlar okunuşta kaldı.
- **Kalıcı çözüm:** `R_TEK_HARF`: tek başına büyük harf (O hariç, zamir) + sayı/"bir" → bitişik kod ("M bir" → M1, "B on iki" → B12). Sınama: "O bir ilaçtır", "Bir hasta" değişmiyor. **Ek (2026-11-26, canlı tarama):** çekim ekli biçim de birleşir ("M üçtür" → M3'tür, "B on ikiyi" → B12'yi); sıra sayısı ("hepatit A on sekizinci" → A 18.), "on"+ek zamiri ("protein C onu") ve X/Y + belgisiz "bir" ("Frajil X bir mutasyon") birleşmez. Tüm ders metinleri tek harf + sayı için tarandı.
- **Önleme kuralı:** Özel terim/kod ekranda daima yazıldığı gibi (M1, H2, CD4) görünür; okunuş yalnız EMA metnindedir. Yeni kod biçimi görülünce `ekranYazim.ts` geçişine örnek cümleyle eklenir, sözlüğe tek tek yama yapılmaz.

## H692 — Sesli ders ekranında kısaltmalar okunuşla kalıyordu: "o ka be", "te se se be", "ka el pe", "dee see mee" (2026-11-26)
- **Belirti:** Kurul 2 derslerinde (psikiyatri, nöropatoloji, farmakoloji) metin takipçisi OKB, TSSB, KLP, EEG, ACTH, CRH, DSM-5, BRAF, MGMT, NAT, KOMT gibi kısaltmaları harf adlarıyla gösteriyordu; tüm derslerde 320+ yer.
- **Kök neden:** `yazim_sozlugu.py` okunuş → yazım eşlemesini yalnız (1) eski kaynak md'de geçen biçimlerden ve (2) tek bir hece bölme sezgisinden kuruyordu. Kurul 2 kısaltmaları o kaynakta az/hiç yoktu, uzatılmış okunuş ("dee", "haa") tanınmıyordu, sözlük de uzun süredir yeniden üretilmemişti. Yeniden üretim ise v2 hizalamasından çöp eşleme getiriyordu ("ve" → OD, "alan" → CST, "e ka ge de es te" → ST); bu yüzden sözlük bayat kalmış ama yenilenmesi de tehlikeliydi.
- **Kalıcı çözüm:** `dizi_kisaltmalari`: harf adı dizisini (kısa ve uzatılmış) bilinen kısaltma kümesiyle (`kisaltma_sozluk.json` + kaynak + ders metinleri) en uzun eşleşmeyle bağlar. Her eşlemeye `_harf_tutar` süzgeci: okunuşun harfleri yazımla birebir tutmalı (hoks→HOX gibi sözcük okunuşu dahil); yazımda rakam varsa okunuşta sayı olmalı. Yeni eşleme sayıdan/başka harf adından hemen önce-sonra geçiyorsa ya da "ve"+tek harf ise alınmaz (CD28, PITX3, "ve Th2" bozulmasın). `ekranYazim.ts`: kısaltma kesme işareti/tireden sonra aranmaz ("S5'te ne", "e-ka-te"), "-deki" eki tanınır. Harfi tutup yanlış olanlar `ELE_KISALTMA`, özel biçimler (Gs/Gi/Go/Gq, DSM-5-TR, SERT, MTHFR, "protein C ve S") `EL_KISALTMA`.
- **Önleme kuralı:** Sözlük her yenilendiğinde tüm ders metinleri eski/yeni ekran çıktısıyla karşılaştırılır; önceden büyük harfli kod olan yerin değişmesi gerileme sayılır ve tek tek bakılır. Harf adı kalıntı taraması 0 olmalı. Okunuş sınaması `ses_ortak/sinama_okunus.py` 0 HATA.

### H698 — Drive ses eşlemesi: ad yanıltıcı, kayıt birden çok ders, eski ses yeni sanıldı (2026-11-26)
- **Belirti:** "3+ yeni ses" için ad eşlemesi 4 aday verdi; "Pato s34/s35" yeni sanılıp k2-03/04'e bağlandı; "Psikiyatri.m4a" tek ders gibi görünüyordu.
- **Kök neden:** Envanterde zaman/boyut yok, eski kayıtlar başka adla (`pato/ses_K2_1.m4a`) saklanmış; ad içerik değil.
- **Çözüm:** Drive'daki tüm sesler indirilip yereldeki bütün `.m4a`'larla md5 karşılaştırıldı → gerçekten yeni 3 ses (Nikotin→k2-61, GenetikSon→k2-59, Psikiyatri→k2-54/55/56 ortak kayıt; dilim dilim slayt kelimesi eşlemesiyle bölündü). Yayınlı derslere H531 ekleme akışı uygulandı.
- **Kural:** Yeni ses tespiti adla değil md5 ile; kısa döküm + 5 dk dilim eşlemesiyle ders(ler) belirlenir.

## H699 — EMA okunuşunda yazılı kalıntılar: α1A, beta2, 7q, Xq27.3, Gq/Go, 3P, "Ödem / Herniasyon" (2026-11-26)
- **Belirti:** Kurul 2+ derslerin `ses_metin.hazirla` çıktısında (çoğu slayt başlığı) Yunan harfi (α, β, ε), bitişik harf+sayı (alfa1, β1, 3P, 5A, 7q), kromozom bandı ("Xq27.3", "on beş q on üç"), G proteini (Gq, Gi, Go) ve eğik çizgi ham kalıyordu; motor bunları atlıyor ya da yanlış okuyordu. 15 ders, 61 satır.
- **Kök neden:** `uzun_yol` yalnız büyük harfli kısaltmayı (modul_okunus) ve sayıyı (FONETIK_TTS) çeviriyordu; küçük harf ya da Yunan harfi içeren kod, rakamla bitişik tek harf ve noktalı bant ondalığı hiçbir geçişin kapsamında değildi. Kurul 2 ses metni okunuş biçiminde yazıldığından gövde temizdi; kalıntı ekran başlığından gelen yazılı biçimdeydi.
- **Kalıcı çözüm:** `ses_metin._kalinti` (uzun yol, `_terim`'den sonra): Yunan harfi → ad, "alfa1A" → "alfa bir aa", "3P"/"7q" → "üç pee"/"yedi kuu", bant "q13.3" → "on üç nokta üç", tek "p"/"q" → pee/kuu (p<0.05 hariç), G+s/q/i/o → "gee see/kuu/ıı/oo" (Go'daki O zamir korumasına takılmasın diye doğrudan harf adı), "CD4+" → "pozitif", " / " ve sözcük/sözcük → virgül; down/walker `EK_OKUNUS`'ta. Sınama `sinama_okunus.py` 73 satır 0 HATA.
- **Ek (2026-11-27, ses yeniden üretimi):** Sesli ders işçisi varsayılan olarak `hazirla` değil `eski_ders_okunus` kullanır (klip karması korunsun diye); `_kalinti` bu yolun Kurul 2+ dalına da eklendi. `@@` bölüm başlıkları seslendirilmez: kalıntıların çoğu başlıktaydı, seslendirilen paragrafta yalnız 7 (k2-47, k2-51 Gq/Gi/Gs/Go; k2-52, k2-53 tek p/q). Yalnız bu 7 klip GPU'da yeniden üretildi; yeni varyantlar `/api/sesli-anlatim/varsayilan` ile öne alındı (iş `varsayilanYap:false` ile eklenir, yoksa öğrenci eski sesi dinler), cümle/kelime zamanı yenilenip Oracle'a gönderildi, `takip_kapisi --varyant` 0 HATA.
- **Önleme kuralı:** Kurul 2+ ses metni değişince ya da yeni ders eklenince tüm derslerin `hazirla` çıktısı yazılı kalıntı için taranır (büyük harf dizisi, harf+sayı, w/q/x, Yunan/simge); eski/yeni çıktı karşılaştırılır, yalnız amaçlanan satırlar değişmeli. Mevcut klipler kendiliğinden yeniden üretilmez — aday listesi `okunus_farki.py`, ses GPU'da yalnız kullanıcı komutuyla.

### H712 — Ortak okunuş "mg/gün"ü "mg, gün", "mmol/L"yi "mmol/lee" diye çeviriyor (2026-11-27, k2-63 tespiti)
- **Belirti:** `ses_metin.hazirla("Sertralin 100-150 mg/gün")` sonucu "yüz ile yüz elli mg, gün"; "0.4-1.0 mmol/L" sonucu "0.4-1.0 mmol/lee". Birim kısaltması açılmıyor, eğik çizgi virgüle dönüyor.
- **Kök neden:** `ses_metin` birim tablosunda "mg/gün" ve "mmol/L" bileşik birimleri yok; eğik çizgi genel kuralla ayırıcıya çevriliyor. k2-63 sesli anlatımında sayılar elle yazıyla yazıldığı için etkilenmedi; çözücüde ses alanları elle düzeltildi.
- **Çözüm:** Bu derste veride düzeltildi (doz aralığı seste "X ile Y miligram"). Kod düzeltmesi bekliyor: başka bir oturum `ses_metin.py`'yi düzenliyor (H699), aynı dosyaya eşzamanlı dokunulmadı.
- **Kural:** Bileşik birimler (mg/gün, mg/kg, mmol/L, mL/dk) `ses_metin` birim tablosuna tek okunuşla girer ("miligram bölü gün" ya da "günde … miligram"); eklenince `sinama_okunus.py`'ye örnek konur.
