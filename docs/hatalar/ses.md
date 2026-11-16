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
- **Çözüm / kural:** `hoca_dokum.py`: ham ses, VAD ve istem yok, 60 sn parça + 2 sn bindirme, sanrı süzgeci, her parçadan sonra
  `.yarim` yazılır ve kaldığı yerden sürer; birim `MemoryMax=4G`. Döküm sürerken `tsc --noEmit` çalıştırılmaz.

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
- **Kural:** Kullanıcıya gösterilen metin daima yazımla (HOX, OTX, PAX6), EMA'ya giden metin okunuşla olur. Tam içerik hattında her yeni v2 metni yazılınca `python3 scripts/uretim/sesli_anlatim/yazim_sozlugu.py` yeniden çalıştırılır ve ekran metni okunuş artığı için gözle denetlenir; `ekran` alanı her cümlede doldurulur (sembol içeren cümlede boş bırakılmaz).

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
- **Kural:** yeni ders seslendirmesinden önce `terim_okunus.py --denetle <anahtar>`; yanlış `KURAL` satırı sözlüğe eklenir.
  Anlatım yazarı önce `anlatim_plani.md` kurar; başlıksız konu geçişinde "burada konu değişiyor" cümlesi zorunlu.
  Çizimde birden çok resim varsa `resim: "R#"`, ayrı yapılar ayrı renk, hattı belirsiz bölge `boya: true`.

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
- **Önleme:** yayımlanmış dersin metni düzeltildiğinde `sesli_yayinla.py`'den SONRA yerel çapa (klip_tasi ile taşınmış + değişen paragraflar
  yazılmış) Oracle'a geri kopyalanır ve `pdf_isaret.py --key <key> --zorla` çalıştırılır (H93); `ders-ekle`'nin yazdığı kaba çapaya güvenilmez.

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
- **Önleme:** E0'dan önce `nvidia-smi --query-gpu=clocks.max.sm` ≤2500 denetlenir; döküm günlüğünde "bu oturum CPU" görülürse
  durdurulur. Hoca vurgusu en az iki dökümle çapraz okunur; yalnız bir dökümde geçen ve slayta bağlanamayan söz vurgu dayanağı olmaz.

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
- **Önleme:** Ses dosyası, PDF gibi, **içerikle** eşleşir (KURUL2_DERS_STANDARDI §1): hizada slayta düşmeyen ≥3 dk'lık blok "ders dışı" işaretlenir ve aynı kurulun diğer derslerinin slaytlarıyla karşılaştırılır; bir dersin başı/sonu sessizse öbür kayıtlar o derse ait olabilir diye taranır.

### H530 — Kısık amfi kaydında hoca dökümü uydurma cümlelerle doluyordu (2026-11-10, k2-22/23/24/58)
- **Belirti:** Kullanıcının yüklediği hoca kayıtlarının ilk dökümünde (turbo model, ham ses) metin "İzlediğiniz için teşekkür ederim", uydurma özel adlar ve anlamsız cümlelerle doluydu; hangi dersin kaydı olduğu bile zor seçiliyordu.
- **Kök neden:** kayıtların ortalama düzeyi −31 dB (telefon amfinin arkasında); `hoca_dokum.py` her kaydı ham sesle ve varsayılan `large-v3-turbo` ile çözüyordu. Kısık seste Whisper sessiz/gürültülü parçaları eğitim verisindeki altyazı kalıplarıyla dolduruyor. 3 dk'lık aynı parçada ham+turbo en kötü, süzgeç (90 Hz–7,5 kHz, afftdn, dynaudnorm) + `Systran/faster-whisper-large-v3` en anlaşılır sonucu verdi.
- **Çözüm/önleme:** `hoca_dokum.py` ilk 10 dk'nın ortalamasını ölçer; −28 dB'den kısıksa süzgeç + normalleştirme kendiliğinden uygulanır (normal kayıtta 2026-10-27 "ham ses en iyi" bulgusu geçerli kalır). Kısık kayıtta `--model Systran/faster-whisper-large-v3` verilir (35 dk ≈ 6 dk GPU). Döküm hangi derse ait diye dosya adına değil içeriğe bakılır: bu gece "Ses Klibi 1 (1)" adlı kayıt Psikiyatri değil Epilepsi çıktı.

### H532 — CPU'lu `meds-ema` birimi açıkken ders EMA işi GPU yerine CPU'ya düşebiliyordu (2026-11-10)
- **Belirti:** GPU'lu EMA işçisi beklerken `meds-ema.service` (yalnız CPU, aynı `ema-yerel` kuyruğu) da etkindi; kuyruğa giren işi hangisinin alacağı belirsizdi (kullanıcı kararı 2026-10-24: EMA DAİMA GPU).
- **Kök neden:** iki işçi aynı sağlayıcı adıyla `/yerel/al` soruyor; birim hâlâ açılışta başlıyor.
- **Çözüm/önleme:** ders sesi üretmeden önce `systemctl --user stop meds-ema` + `cozucu_ses_gpu.sh scripts/uretim/sesli_anlatim/ema_isci.py bekle`; günlükte "EMA Lightning hazır: cuda" görülür. İş bitince birim yeniden başlatılır. Kalıcı çözüm (birimi kaldırmak ya da GPU başlatıcısına çevirmek) kullanıcı kararı bekliyor.

### H538 — 5. parti derslerinin anahtarları `MODUL_ANAHTARLAR`'da yoktu: yazımla tutulan kısaltmalar (DSM, EEG, SSRI) harf harf okunmamış olabilir (2026-11-09)
- **Belirti:** `ema_isci.tts_metni("DSM beş TR …")` k2-21 anahtarıyla metni değiştirmeden döndürdü; k2-22 anahtarı (eklendikten sonra) "dee see mee beş tee ree" verdi.
- **Kök neden:** H469 önlemi ("yeni ders anahtarı seslendirmeden ÖNCE `MODUL_ANAHTARLAR`'a eklenir") 5. partide (k2-19, 20, 21, 37, 38) uygulanmadı; kontrol listesinde yoktu.
- **Çözüm:** 6. parti anahtarları eklendi (k2-22, 23, 24, 58). **Açık:** k2-19/20/21/37/38 sesleri bu yolla üretildiği için kısaltma okunuşu dinlenip gerekiyorsa anahtar eklenip yalnız ilgili klipler yeniden üretilmeli (kullanıcı kararı).
- **Önleme:** `sesli_yayinla.py` yeni anahtarı `modul_okunus.modul_mu` ile denetleyip değilse uyarır (yapılacak); el kitabı §19 adım 8'e madde.

### H539 — EMA tam MP3 yüklemesi Oracle'daki başka bir dağıtımın sunucu yeniden başlatmasına denk gelince iş "hata"ya düştü (2026-11-09, k2-22)
- **Belirti:** 50 klip üretildi, `PUT …/tam` 23:33:24'te bağlantı hatası aldı; Oracle kuyruğunda iş `durum: hata`, ders sessiz kaldı; işçi günlüğü systemd scope'ta olduğundan `journalctl -u meds-ema` boştu.
- **Kök neden:** aynı dakikada başka oturum `dagit.sh` ile konteyneri yeniden başlattı; işçi tek denemeyle bırakıyor.
- **Çözüm:** `POST /api/sesli-anlatim/uret {key, saglayici: ema-yerel, ses: Ema}` ile yeniden kuyruklandı; klipler yeniden kullanıldı (0 yeni klip).
- **Önleme:** dağıtım öncesi `dagit.sh` kuyrukta `calisiyor` EMA işi varsa beklemeli ya da işçi `tam/bitir` adımını 3 kez yinelemeli (yapılacak). İşçi günlüğü: `journalctl --user -o cat | grep <key>` (birim değil, scope).

### H540 — `kelime_zaman.py --gpu` elle çağrıda `libcublas.so.12` bulamayıp sessizce CPU'ya düştü (2026-11-10)
- **Belirti:** k2-22/23 kelime zamanı 1179 sn (CPU); günlükte tek satır "CUDA hatası … bu oturum CPU".
- **Kök neden:** CUDA kitaplıkları `.venv-hizala` pip `nvidia-*` paketlerinde; `LD_LIBRARY_PATH` yalnız `meds-kelime-zaman-hat.service` biriminde tanımlı, betik kendisi eklemiyor.
- **Çözüm:** elle koşuda birimdeki `LD_LIBRARY_PATH` dışa aktarıldı (k2-24/58 GPU'da 345–351 sn).
- **Önleme:** `kelime_zaman.py` başında `nvidia/*/lib` yollarını `LD_LIBRARY_PATH`'e kendisi ekler (yapılacak); CPU'ya düşüş UYARI değil, belirgin HATA satırı olmalı.

### H586 — Çözücü/asistan/Öğren/terim/ek modül seslerinde terim okunuşu ve kısaltma yolu uygulanmıyordu; okunuş 9 yerde, `seslendir` 4 kopya (2026-11-16)
- **Belirti:** Kurul 2 çözücü ve asistan kliplerinde eponimler düz okunuyor (Williams), kısaltmalar bitişik okunuyor (H3 tekrarı); yeni branşta okunuş eksik kalıyor (H538 tekrarı). Sıradan "engel" sözcüğü "Engıl" okunuyordu; 1000 ve üstü sayıda `modul_okunus` IndexError veriyordu.
- **Kök neden:** okunuş yolu içerikten değil elle tutulan `MODUL_ANAHTARLAR` listesinden seçiliyordu; çözücü/asistan/ek modül yolları `uzun_kisaltma_ayarla`'yı hiç çağırmıyordu; her modül `seslendir`'i kopyalayıp ortak durumu (`E.KBPS`, `E.okunus.duzelt`) çalışırken eziyordu. Eponim sözlüğünde küçük harfli genel sözcükle çakışan giriş (`engel`) vardı.
- **Kalıcı çözüm:** `scripts/uretim/ses_ortak/ses_metin.py::hazirla` (tek okunuş girişi; kurul ders kayıt defterinden/klasörden; bilinmeyen modülde uyarı yazar, sessiz eski yola düşmez), `ses_klip.py` (tek `seslendir/klasor/cumlele`; bit hızı ve okunuş parametre), altı betik ortak modüle bağlandı. Klip karma formülü DEĞİŞMEDİ (sahte motorla eşdeğerlik: karma farkı 0). Yeni klip kaydına `okunus_surum` yazılır. Eski kliplerde okunuşu değişecek 17.225 klip `meds_temp/ses_ortak/okunus_farki.jsonl`'de (yeniden üretim yalnız kullanıcı komutuyla, GPU).
- **Önleme kuralı:** yeni ses betiği okunuşu yalnız `ses_metin.hazirla`, klibi yalnız `ses_klip` ile üretir; `E.*` genel ayarı ezilmez. Okunuş yolu değişikliğinden sonra toplu üretimden ÖNCE 10 kliplik dinleme sınaması yapılır (harf harf kısaltma, şık etiketi "A,", "O" zamiri, ek modülde "dede"). Sesli ders okunuşu ortak yola `MEDS_OKUNUS_ORTAK=1` ile geçer (karma okunan metni içerdiği için 1.032 paragraf yeniden üretilir — kullanıcı kararı).

### H587 — Öğren destesinde 16 klip 14–22 dakika sürüyordu; ses için kalite kapısı yoktu (2026-11-16)
- **Belirti:** `ogren_ses/learn-tumor-biyolojisi-terminolojisi` destesinde 16 klip 865–1355 sn (normalin 5–9 katı); tek cümle 811 sn. Öğrenci bildirimi gelmeden, taramada bulundu.
- **Kök neden:** motor tablo metninde durmayıp konuşmaya devam etmiş; üretimdeki tek denetim süre/karakter oranının 3 tohumla yeniden denenmesiydi ve üçü de başarısız olunca klip yine yazılıyordu. Üretim sonrası hiçbir denetim (bozuk/yarım/sessiz klip, düzey, kırpılma, kayıt↔disk, Oracle boyutu) yoktu. H539: tam MP3 yüklemesi tek denemeydi.
- **Kalıcı çözüm:** `scripts/uretim/ses_ortak/ses_kapisi.py <modül|ders>` / `tara --hepsi` / `oracle` / `artik` (ffprobe + volumedetect/silencedetect; 91.399 seste yanlış alarm 0), `scripts/kapilar/matris.json` `ses` aşaması; `yerel_sesleri_tasi.py --dogrula` (Oracle boyut karşılaştırması, her aktarım sonunda); `ema_isci.py` tam yükleme 3 deneme; GPU ses işleri tek kilit (`cozucu_ses_gpu.sh`).
- **Önleme kuralı:** ses üreten her iş yayından önce `ses_kapisi.py` 0 HATA verir; süre/karakter oranı üç tohumda da tutmayan klip yazılmaz, hata olarak raporlanır. Bozuk 16 klip yeniden üretilecek (GPU, kullanıcı komutu).
