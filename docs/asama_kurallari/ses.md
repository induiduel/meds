# Aşama kuralları — ses

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/hat/tam_hat/kural_secici.py`. 38 madde. Tek satırlı maddeleri betik denetler (tam metin: `kural_secici.py --tam <H no|aşama>`).

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
- **Çözüm / kural:** `hoca_dokum.py`: ham ses, VAD/istem yok, 60 sn parça + 2 sn bindirme, sanrı süzgeci, `.yarim` ile kaldığı yerden sürer; `MemoryMax=4G`. Döküm sürerken `tsc --noEmit` yok.


### H104 · Hoca ses kaydı: tek model dökümü sınav vurgularını bozuyordu; kayıt dersin ortasından başlıyordu (2026-10-27, k2-08)
- **Kural:** Sınav vurgusu tek dökümden çıkarılmaz; alıntı birebir döküm, anlaşılmayan sözcük "düzeltilerek" yazılmaz (düzeltme `not`ta); gen adı/sayı yalnız slayt ve/veya öğrenci notu ile örtüşünce vurgu olur; kaydın hangi slayttan başladığı rapora yazılır.


### H109 · v2 cümlesinin `ses` alanında iç cümle sonu: sunucu cümle sayısı v2 ile tutmuyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Kural:** her v2 `ses` tam bir cümledir; yazım betiğinde ayrıca kendi sınır kontrolü (cümle sayısı = 1, ≤25 kelime) çalıştırılır.


### H126 · Sesli ders ekranında gen sembolleri okunuşla görünüyordu: "hoks, o te iks, me se iks, paks 6" (2026-10-28, k2-08)
- **Kural:** Ekran metni daima yazımla (HOX, PAX6), EMA metni okunuşla. Her yeni v2 metninden sonra `scripts/uretim/sesli_anlatim/yazim_sozlugu.py` çalıştırılır; sembollü cümlede `ekran` alanı boş kalmaz.


### H128 · EMA yabancı terimleri yanlış okuyor; anlatım konu geçişini söylemiyor; panel geç, zoom kısa anlatımda, çizim tek renk (2026-10-28)
- **Kural:** seslendirmeden önce `terim_okunus.py --denetle <anahtar>`, yanlış okunuş sözlüğe. Anlatım önce `anlatim_plani.md`; başlıksız konu geçişi söylenir. Çok resimde `resim: "R#"`, ayrı yapı ayrı renk, belirsiz bölge `boya: true`.


### H448 — `klip_tasi.py` metinle birlikte düzenlenmiş v2'yi eski metne göre yeniden kurup değişen paragrafları boşaltıyordu; `ders-ekle` elle iyileştirilmiş çapayı ezdi (2026-10-30)
- **Önleme:** yayımlanmış ders metni düzeltilince `sesli_yayinla.py`'den SONRA yerel çapa Oracle'a kopyalanır, `pdf_isaret.py --key <key> --zorla` (H93); `ders-ekle` çapasına güvenilmez.


### H468 — Hoca dökümü sessizce CPU'ya düştü; turbo dökümü konuşmanın üçte birini kaçırdı (2026-11-02, Kurul 2 2. parti)
- **Önleme:** E0 öncesi `nvidia-smi --query-gpu=clocks.max.sm` ≤2500; günlükte "bu oturum CPU" görülürse durdurulur. Vurgu iki dökümle çapraz okunur; tek dökümde kalan, slayta bağlanmayan söz dayanak olmaz.


### H469 — Kurul 2 EMA yolu büyük harfli kısaltmayı okumuyordu (NMDA, GABA, IP3) (2026-11-02)
- **Önleme:** Yeni Kurul 2 dersinin metni yazımla tutuluyorsa anahtarı seslendirmeden ÖNCE `MODUL_ANAHTARLAR`'a eklenir ve
  `ema_isci.tts_metni` ile örnek paragraf okunuşu denetlenir; okunuş sözlüğü değişince `meds-ema` yeniden başlatılır.


### H501 — Hoca dökümü sarmalayıcısı model seçimini yutuyordu; turbo dökümüyle hocanın sözü yanlış okundu (2026-11-06)
- **Çözüm/önleme:** sarmalayıcı kalan argümanları aktarır (`"$@"`). Hocanın sınav vurgusu içeren ders kayıtları `--model Systran/faster-whisper-large-v3` ile dökülür; belirsiz pasaj içerikte iddiaya çevrilmez, zaman damgasıyla "emin değil" listesine yazılır.


### H508 — Drive'daki ses dosyasının adı başka dersi gösteriyordu: "TSSB Psikaytr 2" aslında EKT (Tedaviler) dersinin başıydı (2026-11-06)
- **Önleme:** Ses dosyası adla değil içerikle eşleşir (KURUL2_DERS_STANDARDI §1): slayta düşmeyen ≥3 dk blok "ders dışı" işaretlenip kurulun öbür dersleriyle karşılaştırılır.


### H530 — Kısık amfi kaydında hoca dökümü uydurma cümlelerle doluyordu (2026-11-10, k2-22/23/24/58)
- **Çözüm/önleme:** `hoca_dokum.py` ilk 10 dk −28 dB'den kısıksa süzgeç + normalleştirme uygular (normal kayıtta ham ses); kısıkta `--model Systran/faster-whisper-large-v3`. Kaydın dersi dosya adından değil içerikten belirlenir.


### H532 — CPU'lu `meds-ema` birimi açıkken ders EMA işi GPU yerine CPU'ya düşebiliyordu (2026-11-10)
- **Çözüm/önleme:** ders sesinden önce `systemctl --user stop meds-ema` + `cozucu_ses_gpu.sh scripts/uretim/sesli_anlatim/ema_isci.py bekle`; günlükte "EMA Lightning hazır: cuda" görülür, bitince birim yeniden başlatılır.


### H538 — 5. parti derslerinin anahtarları `MODUL_ANAHTARLAR`'da yoktu: yazımla tutulan kısaltmalar (DSM, EEG, SSRI) harf harf okunmamış olabilir (2026-11-09)
- **Önleme:** `sesli_yayinla.py` yeni anahtarı `modul_okunus.modul_mu` ile denetleyip değilse uyarır (yapılacak); el kitabı §19 adım 8'e madde.


### H539 — EMA tam MP3 yüklemesi Oracle'daki başka bir dağıtımın sunucu yeniden başlatmasına denk gelince iş "hata"ya düştü (2026-11-09, k2-22)
- **Önleme:** `dagit.sh` kuyrukta `calisiyor` EMA işi varken beklemeli ya da işçi `tam/bitir`'i 3 kez yinelemeli (yapılacak).


### H540 — `kelime_zaman.py --gpu` elle çağrıda `libcublas.so.12` bulamayıp sessizce CPU'ya düştü (2026-11-10)
- **Önleme:** `kelime_zaman.py` başında `nvidia/*/lib` yollarını `LD_LIBRARY_PATH`'e kendisi ekler (yapılacak); CPU'ya düşüş UYARI değil, belirgin HATA satırı olmalı.


### H586 — Çözücü/asistan/Öğren/terim/ek modül seslerinde terim okunuşu ve kısaltma yolu uygulanmıyordu; okunuş 9 yerde, `seslendir` 4 kopya (2026-11-16)
- **Önleme kuralı:** ses betiği okunuşu yalnız `ses_metin.hazirla`, klibi yalnız `ses_klip` ile üretir; `E.*` ezilmez. Okunuş yolu değişince toplu üretimden önce 10 kliplik dinleme sınaması (kısaltma, şık etiketi, "O", "dede"). Sesli ders ortak yola yalnız `MEDS_OKUNUS_ORTAK=1` ile (kullanıcı kararı).


- H587 — Öğren destesinde 16 klip 14–22 dakika sürüyordu; ses için kalite kapısı yoktu (2026-11-16) — betik denetler: `ses_kapisi.py`
### H595 — Öğren sesinde tek başına sıra imi ("2.") ayrı cümle → bütün adım reddedildi (2026-11-17)
- **Önleme kuralı:** ses cümle bölücüsü sıra/madde imini ayrı cümle bırakmaz; bölme değişikliği tüm gerçek metinlerde eski/yeni karşılaştırmasıyla kanıtlanır. Süre eşiği gevşetilmez.


- H605 — Son derslerde PDF ↔ metin takibi zayıftı: cümlelerin %19–24'ü yalnız sayfa vurgusu alıyordu (2026-11-17, kullanıcı bildirdi) — betik denetler: `scripts/uretim/sesli_anlatim/artik_capa.py`
### H606 — Kurul 3 arşivinde işaret "çapa sayfasından kayıyor", tablo/şema cümleleri yalnız sayfaya düşüyordu (2026-11-17)
- **Önleme kuralı:** İşaret yalnız çapanın sayfasında üretilir (komşu sayfa yalnız çapa sayfası yoksa, `capali` içinde); eşleşmeyen cümle madde/kutuya bağlanır, "sayfa"ya düşmez; eşik gevşetilmez.


### H607 — Arşiv metin üretimi görsel/şema sayfalarında "yanıt yok" verip sayfayı anlatımsız bırakıyordu; ders yayına giremiyordu (2026-11-17)
- **Önleme kuralı:** Üretim adımı yayın kapısı denetimlerini kendi içinde koşmadan "0 HATA" demez; boş yanıt = yeniden dene + kısa istem; yazısız görselde yalnız bölüm/komşu başlık bağlamı, kaynak dışı bilgi yok.


### H609 — Zengin transkript tablo ayrıştırıcısı sayı sözcüğünü kesiyordu (2026-11-17, geliştirme sırasında)
- **Önleme:** yapı (tablo/sıra) çıkaran betik emin değilse yapı kurmaz, cümleyi korur; tıbbi sayı kesilmez.

### H612 — k2-33/34/35 kelime zamanı yoktu; izleyici yanlış alarm verdi (2026-11-17)
- **Önleme:** yayından sonra `kelime_zaman.py --hepsi --saglayici ema-yerel --oracle --gpu` elle (`zaman_isaret`; zamanlayıcı kapalı, kural 20); Oracle katmanı yerelde "yok" sayılmaz.



### H629 — Eski ses varyantı yalnız yerelde silinince dagit.sh Oracle'dan geri getirdi; yedek dosyaları kayıt kapısını kilitledi (2026-11-18)
- **Kural:** Ses varyantı kaldırırken önce Oracle'da, sonra yerelde sil ve `meds-server`'ı yeniden başlat; yedeği `_arsiv_veri/` altında `.zst` olarak sakla, `data/` içinde `.yedek` bırakma.


### H655 · Sesli ders ve örnek soruda metin takibi yanlış yeri gösteriyor / geç kalıyor (2026-11-24)
- **Önleme:** Anlatım ↔ slayt/metin eşlemesinde birebir metin beklenmez; sözcük eşleşmesi tek ölçüt olamaz (anlam + sıra). Seste olmayan metin için zaman uydurulmaz: metni değişen ses varyantı ya yeniden seslendirilir ya da sunulmaz.

### H657 — Kurul 3 arşivinde metin üretimi "0/75 sayfa, hata:metin" oluyordu: kelime tavanı kapıda ölçeklenmiyordu (2026-11-25)
- **Önleme kuralı:** bir dersin kapıları **iki ayrı betikte** koşuyorsa eşik/ortam değişkenleri tek yerden türetilir; üretim kapısı ile
  yayın kapısı aynı ortamı kurar. "Kapı 0 HATA" diyen her yol, ölçeklenen eşiği kendisi hesaplamak zorunda.


### H684 — Sesli ders ekranında "M bir, M üç" yazıyordu; doğrusu M1, M3 (2026-11-25)
- **Önleme kuralı:** Özel terim/kod ekranda daima yazıldığı gibi (M1, H2, CD4) görünür; okunuş yalnız EMA metnindedir. Yeni kod biçimi görülünce `ekranYazim.ts` geçişine örnek cümleyle eklenir, sözlüğe tek tek yama yapılmaz.


### H692 — Sesli ders ekranında kısaltmalar okunuşla kalıyordu: "o ka be", "te se se be", "ka el pe", "dee see mee" (2026-11-26)
- **Önleme kuralı:** Sözlük her yenilendiğinde tüm ders metinleri eski/yeni ekran çıktısıyla karşılaştırılır; önceden büyük harfli kod olan yerin değişmesi gerileme sayılır ve tek tek bakılır. Harf adı kalıntı taraması 0 olmalı. Okunuş sınaması `ses_ortak/sinama_okunus.py` 0 HATA.


### H696 — Betik anahtar/gönderim tuzakları: kısa anahtar 400, anonim Oracle 500, kelime zamanı gönderilmedi (2026-11-26)
- **Kural:** Terim/kısaltma/ders_icerik betiklerine TAM anahtar verilir; `--oracle` sonrası kelime zamanı `betik_tamamla --denetle` ile doğrulanır. Açık iş: kelime_zaman güncel olsa da göndermeli.

### H698 — Drive ses eşlemesi: ad yanıltıcı, kayıt birden çok ders, eski ses yeni sanıldı (2026-11-26)
- **Kural:** Yeni ses tespiti adla değil md5 ile; kısa döküm + 5 dk dilim eşlemesiyle ders(ler) belirlenir.


### H699 — EMA okunuşunda yazılı kalıntılar: α1A, beta2, 7q, Xq27.3, Gq/Go, 3P, "Ödem / Herniasyon" (2026-11-26)
- **Önleme kuralı:** Kurul 2+ ses metni değişince ya da yeni ders eklenince tüm derslerin `hazirla` çıktısı yazılı kalıntı için taranır (büyük harf dizisi, harf+sayı, w/q/x, Yunan/simge); eski/yeni çıktı karşılaştırılır, yalnız amaçlanan satırlar değişmeli. Mevcut klipler kendiliğinden yeniden üretilmez — aday listesi `okunus_farki.py`, ses GPU'da yalnız kullanıcı komutuyla.

