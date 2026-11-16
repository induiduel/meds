# Aşama kuralları — ses

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/hat/tam_hat/kural_secici.py`. 24 madde. Tek satırlı maddeleri betik denetler (tam metin: `kural_secici.py --tam <H no|aşama>`).

### H3 — Kısaltma kelime gibi okunuyor ("DNA" → "deneye")
- **Kural:** EMA'ya giden her Kurul 2+ metni uzun harf okunuşuyla ("dee nee aa", `patoloji_cozucu/kisaltma_ses.uzat`).
- **Kapı — EKLENDİ:** `ema_isci.uzun_kisaltma_ayarla` (anahtar `k[2-6]…` → uzun okunuş), Öğren sesi `ema-2`. Kurul 1 eski yolda (toplu yeniden üretim yok).


### H11 — Ses Oracle'a gitmiyor, tarayıcı sesine düşüyor (404)
- **Kapı — EKLENDİ:** zincirin `oracle` adımı canlıda dersin rastgele 5 çözücü/asistan klibini yokluyor (200/206 değilse kod 12).


- H12 — Türev veri (cümle/kelime zamanı, işaret, vurgu) metnin başka sürümünden üretilmiş — betik denetler: `saglik.py`
### H13 — Sesli ders bütünlüğü (yönerge okunması, kapanış patlaması, paragraf/süre uyuşmazlığı)
- **Kural:** EMA için de aynı: modele yalnız okunacak metin gider; eşleşme kapısı korunur.
- **Kapı — VAR:** `metin_denetle` + eşleşme kapısı + v2 kapısı.


- H17 — EMA okunuş ayarı alt süreçte uygulanmıyordu (TBG kampı, 2026-10-20) — betik denetler: `saglik.py`
- H — Okunuş ekrana, rakam sese sızıyordu (kullanıcı, 2026-10-22) — betik denetler: `ekranYazim.ts`
### H58 — EMA cümle ortasında sesi düşürüp es veriyordu (2026-10-24, kullanıcı)


### H81 — Amfi kaydı tek parça + VAD ile verilince Whisper "Altyazı M.K." sanrısıyla erken bitti; eşzamanlı tsc OOM'a yol açtı (2026-10-27)
- **Çözüm / kural:** `hoca_dokum.py`: ham ses, VAD ve istem yok, 60 sn parça + 2 sn bindirme, sanrı süzgeci, her parçadan sonra
  `.yarim` yazılır ve kaldığı yerden sürer; birim `MemoryMax=4G`. Döküm sürerken `tsc --noEmit` çalıştırılmaz.


### H104 · Hoca ses kaydı: tek model dökümü sınav vurgularını bozuyordu; kayıt dersin ortasından başlıyordu (2026-10-27, k2-08)
- **Kural:** Sınav vurgusu tek dökümden çıkarılmaz; alıntı birebir döküm, anlaşılmayan sözcük "düzeltilerek" yazılmaz (düzeltme `not`ta); gen adı/sayı yalnız slayt ve/veya öğrenci notu ile örtüşünce vurgu olur; kaydın hangi slayttan başladığı rapora yazılır.


### H109 · v2 cümlesinin `ses` alanında iç cümle sonu: sunucu cümle sayısı v2 ile tutmuyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Kural:** her v2 `ses` tam bir cümledir; yazım betiğinde ayrıca kendi sınır kontrolü (cümle sayısı = 1, ≤25 kelime) çalıştırılır.


### H126 · Sesli ders ekranında gen sembolleri okunuşla görünüyordu: "hoks, o te iks, me se iks, paks 6" (2026-10-28, k2-08)
- **Kural:** Kullanıcıya gösterilen metin daima yazımla (HOX, OTX, PAX6), EMA'ya giden metin okunuşla olur. Tam içerik hattında her yeni v2 metni yazılınca `python3 scripts/uretim/sesli_anlatim/yazim_sozlugu.py` yeniden çalıştırılır ve ekran metni okunuş artığı için gözle denetlenir; `ekran` alanı her cümlede doldurulur (sembol içeren cümlede boş bırakılmaz).


### H128 · EMA yabancı terimleri yanlış okuyor; anlatım konu geçişini söylemiyor; panel geç, zoom kısa anlatımda, çizim tek renk (2026-10-28)
- **Kural:** yeni ders seslendirmesinden önce `terim_okunus.py --denetle <anahtar>`; yanlış `KURAL` satırı sözlüğe eklenir.
  Anlatım yazarı önce `anlatim_plani.md` kurar; başlıksız konu geçişinde "burada konu değişiyor" cümlesi zorunlu.
  Çizimde birden çok resim varsa `resim: "R#"`, ayrı yapılar ayrı renk, hattı belirsiz bölge `boya: true`.


### H448 — `klip_tasi.py` metinle birlikte düzenlenmiş v2'yi eski metne göre yeniden kurup değişen paragrafları boşaltıyordu; `ders-ekle` elle iyileştirilmiş çapayı ezdi (2026-10-30)
- **Önleme:** yayımlanmış dersin metni düzeltildiğinde `sesli_yayinla.py`'den SONRA yerel çapa (klip_tasi ile taşınmış + değişen paragraflar
  yazılmış) Oracle'a geri kopyalanır ve `pdf_isaret.py --key <key> --zorla` çalıştırılır (H93); `ders-ekle`'nin yazdığı kaba çapaya güvenilmez.


### H468 — Hoca dökümü sessizce CPU'ya düştü; turbo dökümü konuşmanın üçte birini kaçırdı (2026-11-02, Kurul 2 2. parti)
- **Önleme:** E0'dan önce `nvidia-smi --query-gpu=clocks.max.sm` ≤2500 denetlenir; döküm günlüğünde "bu oturum CPU" görülürse
  durdurulur. Hoca vurgusu en az iki dökümle çapraz okunur; yalnız bir dökümde geçen ve slayta bağlanamayan söz vurgu dayanağı olmaz.


### H469 — Kurul 2 EMA yolu büyük harfli kısaltmayı okumuyordu (NMDA, GABA, IP3) (2026-11-02)
- **Önleme:** Yeni Kurul 2 dersinin metni yazımla tutuluyorsa anahtarı seslendirmeden ÖNCE `MODUL_ANAHTARLAR`'a eklenir ve
  `ema_isci.tts_metni` ile örnek paragraf okunuşu denetlenir; okunuş sözlüğü değişince `meds-ema` yeniden başlatılır.


### H501 — Hoca dökümü sarmalayıcısı model seçimini yutuyordu; turbo dökümüyle hocanın sözü yanlış okundu (2026-11-06)
- **Çözüm/önleme:** sarmalayıcı kalan argümanları aktarır (`"$@"`). Hocanın sınav vurgusu içeren ders kayıtları `--model Systran/faster-whisper-large-v3` ile dökülür; belirsiz pasaj içerikte iddiaya çevrilmez, zaman damgasıyla "emin değil" listesine yazılır.


### H508 — Drive'daki ses dosyasının adı başka dersi gösteriyordu: "TSSB Psikaytr 2" aslında EKT (Tedaviler) dersinin başıydı (2026-11-06)
- **Önleme:** Ses dosyası, PDF gibi, **içerikle** eşleşir (KURUL2_DERS_STANDARDI §1): hizada slayta düşmeyen ≥3 dk'lık blok "ders dışı" işaretlenir ve aynı kurulun diğer derslerinin slaytlarıyla karşılaştırılır; bir dersin başı/sonu sessizse öbür kayıtlar o derse ait olabilir diye taranır.


### H530 — Kısık amfi kaydında hoca dökümü uydurma cümlelerle doluyordu (2026-11-10, k2-22/23/24/58)
- **Çözüm/önleme:** `hoca_dokum.py` ilk 10 dk'nın ortalamasını ölçer; −28 dB'den kısıksa süzgeç + normalleştirme kendiliğinden uygulanır (normal kayıtta 2026-10-27 "ham ses en iyi" bulgusu geçerli kalır). Kısık kayıtta `--model Systran/faster-whisper-large-v3` verilir (35 dk ≈ 6 dk GPU). Döküm hangi derse ait diye dosya adına değil içeriğe bakılır: bu gece "Ses Klibi 1 (1)" adlı kayıt Psikiyatri değil Epilepsi çıktı.


### H532 — CPU'lu `meds-ema` birimi açıkken ders EMA işi GPU yerine CPU'ya düşebiliyordu (2026-11-10)
- **Çözüm/önleme:** ders sesi üretmeden önce `systemctl --user stop meds-ema` + `cozucu_ses_gpu.sh scripts/uretim/sesli_anlatim/ema_isci.py bekle`; günlükte "EMA Lightning hazır: cuda" görülür. İş bitince birim yeniden başlatılır. Kalıcı çözüm (birimi kaldırmak ya da GPU başlatıcısına çevirmek) kullanıcı kararı bekliyor.


### H538 — 5. parti derslerinin anahtarları `MODUL_ANAHTARLAR`'da yoktu: yazımla tutulan kısaltmalar (DSM, EEG, SSRI) harf harf okunmamış olabilir (2026-11-09)
- **Önleme:** `sesli_yayinla.py` yeni anahtarı `modul_okunus.modul_mu` ile denetleyip değilse uyarır (yapılacak); el kitabı §19 adım 8'e madde.


### H539 — EMA tam MP3 yüklemesi Oracle'daki başka bir dağıtımın sunucu yeniden başlatmasına denk gelince iş "hata"ya düştü (2026-11-09, k2-22)
- **Önleme:** dağıtım öncesi `dagit.sh` kuyrukta `calisiyor` EMA işi varsa beklemeli ya da işçi `tam/bitir` adımını 3 kez yinelemeli (yapılacak). İşçi günlüğü: `journalctl --user -o cat | grep <key>` (birim değil, scope).


### H540 — `kelime_zaman.py --gpu` elle çağrıda `libcublas.so.12` bulamayıp sessizce CPU'ya düştü (2026-11-10)
- **Önleme:** `kelime_zaman.py` başında `nvidia/*/lib` yollarını `LD_LIBRARY_PATH`'e kendisi ekler (yapılacak); CPU'ya düşüş UYARI değil, belirgin HATA satırı olmalı.


### H586 — Çözücü/asistan/Öğren/terim/ek modül seslerinde terim okunuşu ve kısaltma yolu uygulanmıyordu; okunuş 9 yerde, `seslendir` 4 kopya (2026-11-16)
- **Önleme kuralı:** yeni ses betiği okunuşu yalnız `ses_metin.hazirla`, klibi yalnız `ses_klip` ile üretir; `E.*` genel ayarı ezilmez. Okunuş yolu değişikliğinden sonra toplu üretimden ÖNCE 10 kliplik dinleme sınaması yapılır (harf harf kısaltma, şık etiketi "A,", "O" zamiri, ek modülde "dede"). Sesli ders okunuşu ortak yola `MEDS_OKUNUS_ORTAK=1` ile geçer (karma okunan metni içerdiği için 1.032 paragraf yeniden üretilir — kullanıcı kararı).


- H587 — Öğren destesinde 16 klip 14–22 dakika sürüyordu; ses için kalite kapısı yoktu (2026-11-16) — betik denetler: `ses_kapisi.py`
