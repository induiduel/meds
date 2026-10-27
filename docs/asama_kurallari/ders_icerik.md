# Aşama kuralları — ders_icerik

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/tam_hat/kural_secici.py`. 32 madde. Ayrıntı gerekirse madde başlığıyla defterde aç.

### Diğer oturumlarda düzeltilen hatalardan çıkarılan dersler (tarama 2026-10-20)
- **Kural:** EMA'ya giden her Kurul 2+ metni uzun harf okunuşuyla ("dee nee aa", `patoloji_cozucu/kisaltma_ses.uzat`).
- **Kapı — EKLENDİ:** `ema_isci.uzun_kisaltma_ayarla` (anahtar `k[2-6]…` → uzun okunuş), Öğren sesi `ema-2`. Kurul 1 eski yolda (toplu yeniden üretim yok).

### H4 — Öğrenci metninde iç süreç dili ("PDF'te yok", "aday soru", "bağlanan çıkmış")
- **Kapı — EKLENDİ:** `turkce_uslup.py` kalıpları (Kurul 2+ HATA). **"Doğrusu: …" yasak DEĞİL**: şık açıklaması standardının parçası. "ajan" tıbbi terimdir.

### H5 — Kapının kendisi bozuk (her metin "999 HATA")
- **Kapı — EKLENDİ:** `otomasyon/saglik.py kapi_oz_sinama`: üslup, şık ve v2 kapıları iyi/kötü örnekle her gece; arıza panoda `kapi_ariza`.

### H6 — Birleştirici ders/dosya siliyor
- **Kural:** birleştirici yalnız ekler/günceller; reddedilen ders eski hâliyle kalır.
- **Kapı — EKLENDİ:** `ders_zinciri.korumali`: ders sayısı düşerse ya da öğe sayısı %10'dan fazla azalırsa yedek geri konur (kod 11). Silen, küçülten ve ekleyen durumlar sınandı.

### H7 — Düzeltme tek kopyada kalıyor (çözücüde düzeltilen soru spot/asistan/örnekte eski)
- **Kural:** soru kimliği tek; denetçi düzeltmesi tüm kopyalara yayılır.
- **Kapı — EKLENDİ:** `ders_zinciri.kopya_tutarliligi` (birleştirme sonrası): aynı kökteki soru önem listesi (çıkmış +
  örnek) ile çözücüde farklı doğru şık METNİYLE duramaz (harf farkı serbest: şık sırası değişebilir) → kod 13. K1'in 6
  branşında 0 yanlış pozitif; sahte uyuşmazlık yakalandı.

### H8 — Aynı PDF iki ders / yanlış PDF eşleşmesi
- **Kural:** PDF içerikle tanınır; mevcut dersle yüksek sayfa örtüşmesinde yeni ders açılmaz ("tekrar/kısım").
- **Kapı — EKLENDİ:** `isle.tekrar_denetle`: yeni dersin sayfalarının >%50'si aynı kuruldaki yayımlanmış tek bir derste
  neredeyse aynıysa (kelime kümesi Jaccard ≥0,8) uyarı → otomatik onay kapanır, yönetici karar verir. 19 yayımlanmış derste
  0 yanlış uyarı; aynı PDF'in yeniden gelişi %100 yakalandı.

### H9 — Görsel ya da bozuk OCR'lı sayfa içerikte yok
- **Kural:** metni zayıf sayfa görüntüden okunur; sayfa kapsaması ölçülür.
- **Kapı — EKLENDİ:** işçi denetleyicisi zaten her sayfayı haritada, her içerik sayfasını bir adım + bilgi maddesinde ve
  şekil/tablo sayfasını açıklamalı istiyor (%100 kapsama). Eklenen: görsel ağırlıklı ya da hoca vurgulu (≥3 renkli/kalın)
  sayfa "boş/kapak" diye atlanamaz (s.1–2 kapak muaf) — `denetle.py`, 2026-10-20.

### H10 — Başka dersin sayısı / genel bilgi; çıkmış anahtarı PDF ile çelişiyor
- **Kural:** her ürün yalnız kendi PDF'inin sayısını kullanır; anahtarı PDF ile çelişen çıkmış soru otomatik düzeltilmez, karantinaya alınır ve bildirilir.
- **Kapı — EKLENDİ:** önem yazarı çelişkiyi `elenen_cikmis` → `anahtar_celiskili` ile işaretler (soru o derste kullanılmaz);
  `ders_zinciri.karantina_onerileri` öneriyi `meds_database_v2/ders_isci/cikmis_karantina_onerileri.jsonl`'a yazar ve yöneticiye
  bildirim gönderir. Sitede otomatik gizleme/düzeltme YOK (geçmiş yıl verisi; karar yöneticinin).

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

### Kurul 2 içeriğinin karşılaması gereken sonradan eklenen özellikler
| Özellik | Durum |
|---|---|
| Konuşma v2, cümle zamanı, PDF işareti | hatta |
| Kelime zamanlaması | yalnız cihazda (`meds-kelime-zaman-hat`, GPU; Oracle ARM'de çalışmaz). **İZLENİYOR**: `saglik.py` Kurul 2+ derste kelime zamanı yoksa sorun → sabah bildirimi |
| Önemli cümle vurgusu | **EKLENDİ**: Kurul 2+'da yayın, `konusma_v2.vurgu_turet` ile `data/sesli_anlatim/vurgu/<anahtar>.json` yazar (çıkmışa bağlı cümle 3, tuzak/sayı/tanım 2, terimler). `vurgu_uret.py` Kurul 1'e bağlı kalır |
| "Öğren'de bu bilgi" (`ogren_esle.py`) | **EKLENDİ**: zincirin birleştirme adımında |
| Deste `versionGroup` / Bitirdiklerim konu kimliği | gerekmez: konu kimliği `versionGroup || id` (id her zaman var), K2 kimlikleri defterden |
| Patoloji Hızlı Check Up | **EKLENDİ** (Kurul 2+): `otomasyon/checkup_zinciri.py` (≥3 denetlenmiş ders, Claude `TALIMAT_CHECKUP.md`, `dogrula.py --kurul N`, geçmezse önceki sürüm) → `/patoloji-check-up?kurul=N` |
| Genetik TBG sınav kampı | Kurul 1'e özgü elle hazırlanmış içerik; K2 genetik dersleri spot/çözücü/asistan alır. Kamp eşdeğeri istenirse Check Up kalıbıyla eklenir |
| Test bankası | **EKLENDİ**: örnek/deste kaynakları öge kimliğinden kurula süzülür (Kurul 2+ içerik gelince kendiliğinden) |
| Örnek sorular K1–6, hastalıklar, sözlük, olası soru | hatta |

### H14 — Sunucu kodu Oracle'da ama çalışan sunucu eski kodla (yeni uç sitenin ana sayfasını döndürüyor)
- **Kapı — EKLENDİ:** `deploy-code.sh` Oracle'daki sunucu kodunun içerik karmasını, son yeniden başlatmada yazılan
  `.sunucu_kod_karma` ile karşılaştırır; farklıysa yeniden başlatır. Yeni uç ekleyen iş, dağıtımdan sonra ucu canlıda dener.

### H15 — Sesli ders + slayt ekranında slayt okunan bilgiye gitmiyor, kelime vurgusu yok (TBG kampı, 2026-10-20)
- **Kural:** `PdfDocView`'u saran kap `display: flex; flex-direction: column` ve yüksekliği sınırlı olur. Sesli metin + slayt
  ekranı yayına girmeden kelime dosyasının her cümlede kelime sayısı ekran bölmesiyle (`/\S+/g`, `**` silinmiş) birebir
  tuttuğu denetlenir (0 eksik); yeniden üretim: `meds_temp/spot_cozucu/genetik/g07_yeni/kelime_esle.py`.
- **Kapı — EKLENDİ:** `canliDers.ts bransBilgisi` K2+ için kayıt defterini kullanır; `otomasyon/saglik.py
  kayit_defteri_sorunlari` her kurulda kimlik/kod/branş numarası çiftini sorun sayar (gece sağlık → bildirim).

### H17 — EMA okunuş ayarı alt süreçte uygulanmıyordu (TBG kampı, 2026-10-20)
- **Kural:** sesi etkileyen her ayar iş dosyasından (`is.key`) sentez sürecinin İÇİNDE kurulur; genel değişkene üst süreçten
  güvenilmez. Kamp sesi (`scripts/kamp/ses.py`) süreç içi çalışır, anahtarı `kN-kamp` (K2+ uzun kısaltma yolu).
- **Kapı — EKLENDİ:** `sentezle` başta `uzun_kisaltma_ayarla(is.key)` çağırır; `saglik.py ema_alt_surec_okunusu` bu
  çağrı kalkarsa kapı arızası verir. Modül dersleri (birden çok dersin özeti) `modul_okunus.py MODUL_ANAHTARLAR`'a eklenir.

### H19 — Çıkmış cevap anahtarı tıbben hatalı / iki kaynakta çelişik (2026-10-21, TBG kampı)
- **Kural:** cevap anahtarını körü körüne kopyalama; her çıkmışın anahtarı ders kaynağına (slayt) karşı denetlenir, kaynakta yoksa
  tıbbi bilgiye göre. Anahtar değiştirilirse eski anahtar ve gerekçe **sorunun kendisinde** yazılır (açıklama + "Dikkat: sınavın cevap
  dosyasında X işaretli, tıbben hatalı"), çıkmış kaydında `anahtarDuzeltme {eski, yeni, tarih, gerekce}`, sesli anlatımda da söylenir.
  Aynı bilgiyi soran tekrar çiftleri şık METNİYLE karşılaştırılıp tek karara bağlanır (harf farkı şık sırasından olabilir).
- Kararlar: higroma → Turner şıkta varsa Turner, yoksa Down (g05 s30); over → FOXL2/RSPO1/WNT4 varsa o (g03 s30), yoksa WNT4+DAX1;
  nükleotid indel → C. Denetim raporları `meds_temp/spot_cozucu/genetik/celiski/`.
- K2–K6 taraması (2026-10-21): 51 anahtar düzeltildi; alt ajan denetiminde **soru başına kaynak araması + alıntı kaydı zorunlu** (`kanit_NN.jsonl`) — ilk turda ajanlar 76 soruyu ~6 aramayla "uygun" saydı. Araçlar `meds_temp/cikmis_celiski/`.

### H18 — Diğer oturumların 2026-10-20 düzeltmelerinden Kurul 2'ye taşınanlar (kayıt)
- Sesli ders alt madde kuralları (`CanliDersDers.tsx`: "şunlardır/ikiye ayrılır", "Birincisi/Diğeri", "Çünkü/Örneğin")
  istemcide ve tüm derslere (K2 dahil) uygulanır; v2 `duzey` alanı henüz istemcide okunmuyor. K2 yazarı alt maddeleri bu
  kalıplarla açar (liste açan cümle → sıralayan/açıklayan cümleler) ki madde düzeni doğru çıksın.
- Baştan üretme: `POST /kuyruk/<is>/yeniden-uret` (aynı gün ikinci kez 409, yeni is_id) — elle PDF yeniden işletme
  bundan başka yolla yapılmaz (el kitabı §hat panosu).
- PDF görüntüleyici kabı esnek sütun + sınırlı yükseklik (H15); tam ekran katmanı `body`'ye portal.

### H20 — Kurul 1'de elle kurulan Son Prova ve anlamsal çapa Kurul 2'de unutulmasın / K1'e sabit kalmasın (2026-10-21)
- **Kural:** kurul başına elle yapılan her yeni ürün, ertesi gün hat.json'a aşama olarak girer; betik kurul/branş/kod
  biçimini plandan ya da kayıt defterinden alır, talimatları depoda (`meds/scripts/...`) tutulur.
- **Kapı — EKLENDİ:** `son_prova` aşaması (plan_kurul.py + son_prova_zinciri.py), `ders_zinciri` `capa` adımı
  (capa_dogrula.py). Son Prova sınav dağılımı duyurusu yoksa bildirim gider.

### H21 — Soru çözücü sonradan genişleyince Son Prova soru kimlikleri kaydı (Kadın Doğum, 2026-10-21)

### [2026-10-21] Çıkmış soruda iç uyarı metni ve kalıp şık açıklaması (h06/19 Refik Saydam)
- **Kural:** ses okunuşla (“on dördüncü”, “doku plazminojen aktivatörü”), ekran yazımla (“14.”, “(t-PA)”, “β-hCG”, “12+6 hafta”).
- **Kapı — EKLENDİ:** ekran `ekranYazim.ts`, ses `okunus.SAYI_TTS`; yeni kısaltma/açılım `yazim_sozlugu.py` ile sözlüğe girer.

### H22 — Sesli derste dolgu ve asılsız "hoca vurguladı" cümleleri (kullanıcı kuralı, 2026-10-22, KALICI)
- **Kural:** Amaç bilgiyi en kısa yoldan, doğru, açıklayıcı ve eksiksiz iletmek. Kelime alt sınırı ve süre hedef DEĞİLDİR;
  kısa ama eksiksiz metin doğrudur. Önem vurgusu yalnız dayanağı varsa (çıkmış soru, öğrenci notu, slayttaki işaret) ve
  kritik noktada yapılır; dayanağı yazılmadan "hoca vurguladı/işaretledi/altını çizdi" denmez. Tekrar, geçiş ve özet
  dolgusu ("şimdi gelelim", "bir kez daha hatırlatalım", "daha önce de söylediğimiz gibi") yasak.
- **Kapı — EKLENDİ:** `scripts/sesli_anlatim/metin_denetle.py` → `DOLGU` kalıpları HATA; "Burası önemli/çok önemli/sınavda
  sık" bölüm sayısının yarısını (en az 3) aşarsa HATA; kelime alt sınırı artık yalnız uyarı. K1 metinlerine toplu müdahale yok.

### H23 — Öğrenci işaretli slayt yanlış yorumlandı + okunuşla yazılmış metin (İmmünofarmakoloji V2, kullanıcı, 2026-10-22)
- **Kural (kullanıcı tanımı):** sarı ya da mavi ÇAPRAZ şerit/çizgi = hoca okumadı (anlatılmaz); metin üzerindeki YATAY
  çizgi/vurgu = okundu; yıldız, daire, "önemli", "bil", ünlem, altı çizili = önemli. Öğrenci notlu PDF önce sayfa sayfa
  işaret dökümüne (okundu/okunmadı/önemli/el yazısı) çevrilir, metin dökümden yazılır.
- **Kural:** kısa sürüm slayt sırasını izler; önem listesinin (`src/data/<branş>_onem/`) TAMAMI ve her çıkmış konu içinde
  anlatılır; konu ne → neden/nasıl → sınav ayrıntısı sırasıyla kapanmadan geçilmez; soru dili ve şık yankısı yasak; uzunluk
  V1'in %45–65'i ("çok kısalt" diye madde atma). Yazar + bağımsız denetçi (kapsama dökümü + kaynak karşılaştırması) zorunlu.

### H31 — Hesap sorusu yanlış alarmı + iç etiketin öğrenci metnine sızması (2026-10-23 K2 provası)
- Naegele tarih sorusunun doğru şıkkı ("10.02.2021") maddede yazmaz, kuraldan hesaplanır; önem görevinin çözülebilirlik kapısı
  "çözülemiyor" diyordu → doğru şık yalnız sayı/tarih/birimse kökteki kural terimlerinden ≥2'si maddede olması yeter.
- Ücretsiz model detay alanına "Q3 ve Q4'te verilen tarihler…" yazdı (öğrenci Q3'ü bilmez). Ortak kapı
  `cekirdek.etiket_sizintisi` (yönlendirici + `gorev.py dogrula`): pakette verilmiş kısa etiket öğrenci metninde kalırsa HATA;
  girdide tıbbi anlamda da geçen (S1 kalp sesi, L4 omur) muaf; iç veri görevleri `OGRENCI_METNI = False`. Kural `cikti_disiplini.md`.

### H33 — Türkçe harfsiz metin kabul ediliyordu + kabul edilmiş iş yeni kapıdan geçirilmiyordu (2026-10-23 K2 provası)
- Gemini Flash-Lite bazı çözücü partilerini ve bir sesli bölümü baştan sona harfsiz yazdı ("dogum", "bagli", "oykusu");
  hiçbir kapı yakalamadı, partiler KABUL edildi (önceki e07 çözücü ve k1-64 sesli sınamalarında da vardı; yalnız geçici kopya).
- Ortak kapı `cekirdek.turkce_katlama`: sözlük paketin kendi girdisinden; girdide Türkçe harfle geçen kelimenin katlanmış
  biçimi ≥3 kelimelik bir alanda ≥2 kez varsa HATA (İngilizce alıntı, kimlik/tür alanı, büyük harfli OCR yanlış alarm vermez).
- Kabul edilmiş iş yeniden kullanılırken `yonlendir.kapi` ile güncel kapılardan geçirilir; geçemezse "yeniden" koşar.
- Betik onarımı `cekirdek.ses_onar` (SES_ONAR görevleri): ses alanlarında kısaltma/Roma rakamı `modul_okunus.donustur`
  ile ("MSH" → "mee see haa"); modelin üç turda düzeltemediği "büyük harfli kısaltma" hatası kalktı.
- Öncüllü soruda "kökle uzunluk uyumsuz" hatasına düzeltme ipucu eklendi (kok_ses öncüllerin hepsini okur).

### H40 — Canlı çizim çizgileri görünmüyor, amaçları anlaşılmıyordu (2026-10-24, kullanıcı ekran görüntüsü s.14 herniasyon)
- İnce (1,5 px) yarı saydam mavi çizgi resim/renkli zeminde kayboluyordu; okların çoğunda etiket yoktu (k2-02'de 34 okun 15'i),
  öğrenci okun neyi anlattığını çıkaramıyordu; resimdeki mevcut okları kopyalayan anlamsız dirsekler çiziliyordu.
- Düzeltme: her çizginin altında beyaz hale (5,5 px), çizgi 2,4 px tam opak, hedef çerçevesi 2 px; **etiketsiz ok reddedilir**
  (`cizim_uret`: "etiketsiz ok"); etikete boş yer yoksa yolun ortasına koyu hap olarak konur (gizlenmez).
- Birden çok terim aynı sonuca gidiyorsa tek ok değil, alt alta dizilip "}" ile toplanır (şema grubu, `CizimLayer.Sema`).

### H48 — Canlı sitede tasarım taraması bulguları (2026-10-24)
- Panel PDF yazı satırının kutusuna yapışıyordu (s.10 "Opioid overdozu ?", s.16 "Hipotermi?"): mürekkep eşiği harf
  gövdesini görür, satır kutusunu görmez → `yazi_kesisir` (panel ve etiket yazı satırı kutusundan 0,01 / 0,004 uzak).
- Dar PDF bölmesinde "Çiz" düğmesi harf harf alt alta kırılıyordu: ölçüt ekran genişliğiydi → bölme genişliği (container query).
- Oynatıcı, anlatılan satırları örtüyordu: görüntüleyici anlatılan satırlar oynatıcının altında kalırsa yetecek kadar kaydırır.
- Telefonda görünüm seçici (Metin / Metin + Slayt / Slayt) ayrı bir satır kaplıyordu → başlık satırında tek döngü düğmesi.
- Canlı tarama (telefon, Slayt, 4×): 46 panel/etiketin 45'i temiz; uzun etiket ("kollar fleksiyonda, bacaklar
  ekstansiyonda") kırpılıp yazıya biniyordu → etiket satıra iner, yerleşim satır sayısıyla. Hızlı dinlemede anlatılan satır
  oynatıcı altında kalıyordu (her cümlede sıfırlanan zamanlayıcı hiç çalışmıyordu) → iptal edilmeyen 600 ms kısıtlayıcı.
- Aynı paneldeki bağımsız "A → B" satırları farklı kırılıyordu (nalokson tek satır, flumazenil iki satır) → hizalı tablo
  (kaynak | ok | hedef sütunları, `is-tablo`); baskılama ucu ⊣ büyütüldü.
- Canlı tarama (telefon, Slayt, 2×, 8:08–16:07): etiket "tabloya uygun yaklaşım" (s.49) yazının üstüne konmuştu (yakında yer
  yokken yolun ortasına) → önce yakında yazısız yer, sonra yakında resmin ≤%25'ini örten ama yazıya değmeyen yer, sonra
  sayfada ≤0,35 uzaklıkta boş yer. Sonuç: 35 etiketin 0'ı yazı satırıyla kesişiyor. Sayfa geçişi kaydırması sürerken atlanan
  satır düzeltmesi kaydırma bitince yeniden denenir (masaüstü 2×'te s.11–19'da 2–13 sn örtme vardı).

### H50 — Panel tıbben yanlış okunuyordu; takip kaydırması sessizce boşa gidiyordu; ekran kalabalıktı (2026-10-24)
- "üremik ensefalopati → istenir → üre, kreatinin", "glukoz —hızla geri döndürür⊣ hipoglisemi": ok yönü/işareti anlamı
  bozuyordu. Düzeltme: anlam şablonu kütüphanesi (`scripts/cizim/sablonlar.json`, `sablon.py`), yönsüz eşleşmeler başlıklı
  tablo; yeni şablon önerisi kütüphaneye eklenir; bağımsız tıbbi anlam denetimi (tamam/düzelt/sil). Numaralı/madde imli
  liste, kesikli satır/sütun ayracı.
- Takip: tarayıcının `scroll-behavior: smooth` kaydırması PDF kapsayıcısında ilerlemiyordu; hesap sayfa geometrisinden
  yapılıp ölçek katmanında ekranla uyuşmuyordu; program kaydırması kullanıcı gezinmesi sayılıp takibi durduruyordu →
  kare kare kaydırma + süre dolunca doğrudan, ekrandaki gerçek konumdan ölçüm, program kaydırması bildirilmez. Ölçüm:
  2× hızda 7 dk'da örtme 8–16 sn → 0,6 sn.
- Ekran: izleme düzeni (anlatılmayan paragraflar soluk, özet kutuları kapalı; slayt %60).
- (2026-10-24) Şablonlu tablo, eski hizalı ilişki düzeninin `is-tablo` sınıfını paylaşıp ızgara düzenine giriyor, sabit düzenli
  tablo Chrome'da 1.000.000 px genişliğe çıkıp ikinci sütun panelin dışında kalıyordu (panel kutusu ölçümü bunu görmüyordu).
  Düzeltme: eski kural `:not(.pdv-sb)`, panel blok düzen, tablo/karşıta ayrılan genişlik doğrudan; sınamaya iç taşma (hücre
  sağ kenarı) eklendi. Telefonda kompakt sürüm 7,5 px sınırı yüzünden küçülemediği için boy tam ölçekle tahmin edilir (%32 pay).

### H55 — Görsel tablodan yanlış satır okundu; hocanın kendi çelişkisi kesin "sınav spotu" yapıldı (2026-10-24, k2-07)
- Bütün betik kapıları 0 HATA iken bağımsız tıbbi denetim (PDF ile satır satır) buldu:
  - s.63 Tablo 25.3 (görüntü): droperidol premedikasyon/sedasyon/antiemetik dozları **midazolama** yazılmış; kart, soru,
    checkpoint ve sesli metne yayılmış. Aynı tablonun opioid yarısı atlanmış.
  - s.6 "en zayıf desfluran" ↔ s.13 Tablo 25.1 MAK azot protoksit >100: iki zıt cevap öğretiliyordu. Kural: hocanın
    çelişkisi tek cümlede uzlaştırılır (halojenli uçucular içinde desfluran; tüm inhalerler içinde N₂O), kesin spot yapılmaz.
  - Tablodaki 0 değeri "seyrek" diye okunmuş (midazolam bradikardi); "(Katzung)", "standart kaynaklara göre" ekleri sızmış.
- Kural: Kurul 2+ her derste yayından önce PDF'le karşılaştıran bağımsız tıbbi denetim (ayrı oturum, yazar ≠ denetçi)
  zorunlu; görsel tablo satırı ilaç/değer eşlemesi görüntüden tek tek doğrulanır. Bulgular düzeltilip kapılar yeniden koşulur.

### H59 — Arşiv derslerinde lazer resim ve tabloları göstermiyordu (2026-10-25, kullanıcı, 2025-26 Kurul 2)
- **Kural:** şekil/tablo çapası maddeye üstündür; `madde`/`resim` dizini toplu betikle uydurulmaz; kapsama oranı
  çapayı düzelterek yükseltilir. Döküm (capa_dok, cizim dok) yalnız tekil R# ve yeşil T# kutularını gösterir.
- **Kapı:** `pdf_isaret.sekil_isareti` (şekil önceliği), `capa_dogrula.py` T# denetimi; `uygula_lazer_takip.py` çapa yazmaz.

### H63 — Sesli Derslerde Arşiv PDF'lerinin Çok Geç Yüklenmesi veya Hiç Yüklenmemesi (AutoFetch, SW Range ve Linearization Hatası) (2026-10-26, kullanıcı)
- **Çözüm & Kural:**
  1. `PdfDocView.tsx`: `disableAutoFetch: true` ve `rangeChunkSize: 256 * 1024` sabitlendi. PDF.js artık asla tüm dosyayı arka planda otomatik çekmez; yalnızca o an görüntülenen sayfanın 256 KB'lık dilimini çeker ve ilk sayfa 1 saniyenin altında ekrana gelir.
  2. `public/sw.js`: `/api/lecture-pdf/` akışları Service Worker tamponlama ve cache mekanizmasından tamamen muaf tutularak (`return;`) doğrudan tarayıcının yerel yüksek hızlı ağ motoruna bırakıldı (`SW v16`).
  3. `pikepdf` motoru ile tüm arşiv PDF'leri linearize edildi (Fast Web View); ilk sayfa ve xref tablosu dosyanın ilk kilobaytlarına taşındı.
  4. `server.ts`: `/api/lecture-pdf/deck/:deckId/:index` için `Accept-Ranges: bytes` ve `public, max-age=604800, stale-while-revalidate=86400` başlıkları eklendi.





### H65 — Tablo sayfasında tabloyu anlatmayan cümleye şekil/tablo çapası (2026-10-26, k2-23 cinsel kimlik)
- **Çözüm / kural:** Şekil/tablo çapası yalnız görseli/satırı gerçekten anlatan cümleye yazılır; paragrafın sonraki cümlelerine kopyalanmaz. Tablo çapalı cümlede `satir` boşsa çapa yazılmaz. Düzeltme: o cümlenin `sekil`'i `null` yapıldı, `tablo` kaldırıldı (capa + v2 + taslak kopyaları, `sekil_cizim.py sus` ile aynı yöntem); kapı gevşetilmedi, yayın 0 HATA ile tamamlandı.


### H70 — Mekanik 2 Cümlelik Şablon ve Yüzeysel Anlatım Yasağı (Sıfır Bilgi Kaybı ve Amfi Derinliği Standardı) (2026-10-26, k2-48 lokal anestezikler)
- **Çözüm / kural:** Sayfa başına yüzeysel 2 cümlelik kopyala-yapıştır şablonlar KESİNLİKLE YASAKTIR. Her slayt için amfi ders notundaki tüm maddeleri, tabloları, spesifik ilaç isimlerini, maksimum dozları ve patofizyolojik mekanizmaları kapsayan 3 ila 6 zengin cümle yazılmalıdır (35–70 slaytlık dersler için 140–250+ cümle, ~2000–3500 kelime, 15–25 dakika anlatım derinliği). K48 bu standartla baştan üretildi (144 cümle, 2438 kelime, 68 atomik bilgi, 10/10 çizim, 6.23 MB .medspak) ve 0 HATA ile Oracle canlı ortamına alındı.



### H71 — PDF metnindeki ayrışık (decomposed) harfler terim eşleşmesini bozuyordu (2026-10-26, k2-07 genel anestezik ilaçlar)
- **Çözüm / kural:** `Sayfa` sınıfı PDF kelimelerini okurken `unicodedata.normalize("NFC", w)` uygular; `bul()` de terimi NFC'ye çevirip token'lara ayırır. Kapı gevşetilmedi. Yeni PDF okuyan her betik kelimeleri NFC'ye çevirmeden eşleştirme yapmamalıdır.


### H72 — Çok sözcüklü terimin kısa son sözcüğü ek aldığında eşleşmiyordu (2026-10-26, k2-07 genel anestezik ilaçlar)
- **Çözüm / kural:** `ek_mi(..., kisa_izin=True)` yalnız **çok sözcüklü** terimin **son** sözcüğünde ve terim en az 8 karakterken kullanılır; tek sözcüklü kısa terimlerde (kısaltmalar) davranış değişmedi. Eşleşme gevşetilmedi, yalnız Türkçe ek kuralı bağlamla birlikte uygulandı.


### H73 — `terim/` klasörü dağıtım betiğinin veri listesinde yoktu; terim dosyaları canlıya ulaşamıyordu (2026-10-26)
- **Çözüm / kural:** Listeye `terim` eklendi. `data/sesli_anlatim` altına yeni bir veri türü ekleyen her oturum, `deploy-code.sh` [1b] listesini de günceller; dağıtımdan sonra canlı API yanıtında alanın varlığı `curl` ile doğrulanır.


### H74 — Madde imi kelimeye yapışık gelince terim işaretlenemiyordu (2026-10-26, k1-35 prenatal tanı)
- **Çözüm / kural:** `Sayfa` kelimeyi okurken baştaki "o" yalnız **ardından büyük harf geliyorsa** (madde imi kalıbı) ayrılır; kutu aynı kalır. Madde başındaki terimler de artık işaretlenir. Kapı gevşetilmedi.


### H75 — Gündelik Türkçe sözcükler terim diye işaretlenmişti (2026-10-26, tüm dersler)
- **Kalıcı çözüm:** `terim_sozlugu.py ayikla [--yaz]` bütün terim dosyalarını (canlı + arşiv) tarayıp kapının reddettiği ögeleri çıkarır; terimi kalmayan sayfa/dosya kaydı silinir (hiçbir dosyada boş `t` dizisi bulunmaz). Bu turda 514 öge ayıklandı, kapı gevşetilmedi.
- **Önleme kuralı:** Terim kapısı kuralı değiştiğinde yalnız yeni dosya değil, **tüm mevcut dosyalar** yeni kuralla yeniden taranır (`ayikla`), sonuç canlıya dağıtılır.


### H76 — Cümle sayısı kapısı kısaltma noktalarını cümle sonu sayıyordu (2026-10-26)
- **Kalıcı çözüm:** Cümle sonu ancak noktadan sonra **büyük harf** ya da metin sonu geliyorsa sayılır (`[.!?](?=\s+[A-ZÇĞİÖŞÜ]|\s*$)`). Gerçek üç cümleli açıklama hâlâ HATA alır; kural gevşemedi, yanlış sayım düzeldi. Ayrıca "frenler"/"çapası" gibi çeviri mecazları (8 terim) doğal Türkçeyle yeniden yazıldı.


### H77 — Kısaltma katmanı eklenirken üç ayrı tuzak: büyük harfli Türkçe sözcük, tireyle bitişik yazım, dağıtım listesi (2026-10-26, Kurul 2 · 60 ders)
- **Çözüm / kural:**
  1. `kisaltma_mi()` artık `/usr/share/hunspell/tr_TR.dic` köklerini (ek soyma ile) kullanır: sözlükte bulunan büyük harfli sözcük kısaltma sayılmaz. Bilinen/elle sözlükte (`kisaltma_bilinen.json`, `kisaltma_elle/`) açıkça tanımlı kısaltmalar (SAK, KS gibi Türkçe sözcüğe benzeyenler) bu filtreden muaftır.
  2. `kutular()` eklendi: tam eşleşme yoksa kısaltma, kelime içinde **önek/sonek sınırı** denetlenerek (ör. "o5-httlpr", "t12-l1", "dsm-iii-r", "gabaa-reseptor") karakter oranıyla daraltılmış kutuda işaretlenir. Kapı gevşetilmedi; yalnız doğru konum hesaplandı.
  3. Dağıtım listesine `kisaltma` eklendi; canlı API'de `kisaltma` alanı `curl` ile doğrulandı.
- **Önleme kuralı:** (i) Her yeni veri türü hem `canliDers.ts` yol tanımına hem `deploy-code.sh` [1b] listesine yazılır. (ii) Kısaltma/açılım **yalnız dersin kendi metninden ya da elle/bilinen sözlükten** alınır; metinde açılımı olmayan kısaltmaya tahminle açılım yazılmaz (yanlış açılım, eksik açılımdan kötüdür).


### H80 — Öğrenci Drive betiği uzantısız PDF'i not saymadı; kısaltma bulucu "HT+DM" yazımını kaçırdı (2026-10-27)
- **Çözüm / kural:** Tür MIME'den de belirlenir; bölme deseni `[/\-–+]`; EP `kisaltma_bilinen.json`'a eklendi.
  `degerlendirme_dogrula.py` slayttaki her kısaltmanın sözlükte olmasını HATA ile ister.


### H85 — Çizim önemli bölgeyi örtüyor, zoom yanlış/fazla, kelime ↔ kelime oku okumayı bozuyor (2026-10-27, kullanıcı bildirdi)
- **Çözüm:** kontur %8 dışa açılır, hale yok, dolgu %13 bulanık, karartma %10, kalınlık bölgeye göre 1–2,4 px; akış yalnız
  resim çiziminde (`yakin`); zoom ≤1,6×, ≥1,25× gerekmezse yok, bölge ≤%20; tabloda çizim yok (yalnız marker). Üretici
  (`cizim_uret.yakinlasma`) yalnız resimde ve ≤%20; kapı K10–K12; standart `KURUL2_DERS_STANDARDI.md` §4; metin takipçisi
  kapısı `takip_kapisi.py` (T1–T6).
- **Önleme kuralı:** okumayı bozan hiçbir çizim/zoom yayına girmez; yeni ders kapıları K10–K12 + `takip_kapisi.py` 0 HATA.
  Yayındaki eski derslerin verisi kapıda 36 ihlal gösteriyor; görüntüleyici aynı kuralları uygular, yeniden üretimde düzelir.


### H89 — Slayttaki yapışık madde imi glifi (U+F06E) kısaltmayı ve kanıt eşlemesini bozdu (2026-10-27, k2-02/k2-03)
- **Çözüm / kural:** `kisaltma_sozlugu.adaylar` ve `degerlendirme_dogrula.norm` U+F000–F8FF ve madde imi işaretlerini ayırıcı/boşluk
  sayar. Yeni metin işleyen her betik slayt metnini bu karakterlerden arındırarak karşılaştırır.


### H92 — Bilinen kısaltma sözlüğü bağlamsız: MSS "Muskuloskeletal sistem" diye açıldı (2026-10-27, k2-03/k2-04)
- **Çözüm:** derse özel `data/sesli_anlatim/kisaltma_elle/<key>.json` (`MSS: Merkezi sinir sistemi`), elle eşleme bilinenden önce gelir.
- **Önleme kuralı:** her derste kısaltma listesi (kısaltma = açılım) yazdırılıp slayt metniyle okunur; branşa göre anlamı değişen
  kısaltma (MSS, KB, BOS …) için derse özel eşleme yazılır, genel sözlüğe yeni anlam eklenmez.


### H102 · Sınav planı Kurul 2'de yanlış puan/plan veriyor (2026-10-27)
- **Çözüm:** K2+ için branş `k<kurul><slug>` olarak türetilir ve ders kurulu eşleşmelidir; içeriksiz branşın olasılığı çalışılmamış taban (0,30) alınır.
- **Kural:** Kurul 1 sabit tablolarına dayanan eşleme Kurul 2+ için kurul önekli türetilmeli; içeriği olmayan branş 0 olasılıkla değil taban olasılıkla modellenmeli.


### H102 · Tasarımdaki kayıt adımları (üniversite, sınıf, kurul, hedef) koda geçirilmemişti (2026-10-27)
- **Çözüm:** ProfilKurulumV15 (I07–I11) + Profil › Okul ve hedef; denetim belgesine "Değerlendirilmemiş ekranların değerlendirmesi" tablosu (her satıra karar).
- **Kural:** Tasarım geçişinde "DOĞRULANMADI" durumu iş sonu kabul edilmez; her ekran KURULDU / SIRADA / VAR / BİLİNÇLİ / altyapı yok kararından birini alır ve tur sonunda tablo güncellenir.



### H108 · Kısaltma kapısı slayttaki gen sembollerini ve slayt yazım hatalarını (LMXIB, WTI) Faz A'da HATA sayıyor (2026-10-27, k2-08)
- **Çözüm:** 17 anahtar yalnız bu ders için eklendi (açılım standart, slayttaki yazım hatası belirtilerek).
- **Kural:** Genetik derslerde Faz A'da slayttaki gen sembolleri + kısaltmalar sözlüğe önce eklenir; yazım hatalı sembol (LMXIB/WTI) aynen ayrı anahtar olur ve açılımında doğru gen belirtilir.


### H110 · Kısaltma kapısı `kisaltma_elle`deki OD/OR/ID/SED'i "kısaltma biçiminde değil" diye reddetti (2026-10-27, k2-08 Tıbbi Genetik)
- **Çözüm:** `ELLE_AKTIF` (işlenen dersin elle anahtarları) `kisaltma_mi`de kabul edilir; `k_adaylar/k_otomatik/k_dogrula` başında doldurulur. Çok anlamlı kısaltma (CVS: kardiyovasküler sistem s.49 / koryonik villus örneklemesi s.70) genel sözlüğe konmaz, sayfa bazlı yazar dosyasıyla verilir.
- **Kural:** branşa özgü, Türkçe sözcüğe benzeyen kısaltma (OD, OR, ID, SED) dersin `kisaltma_elle` dosyasına yazılır; genel `kisaltma_bilinen.json`a eklenmez.


### H105 · Sıralı tabloda adım atlanıyordu (k2-05, 2026-10-27)
- **Çözüm:** 3. satır (Motor sistem) parça, taslak deste ve `interactive_learning_decks.json`'a eklendi; ders içerik paketi yeniden yazıldı.
- **Kural:** Sıra/Adım sütunlu tablolarda numaralar 1'den kesintisiz olmalı ve slayt metnindeki sayımla eşleşmeli (`docs/DERS_ICERIK_BICIMI.md`). Kapı: `scripts/ders_icerik/sira_kapisi.py`.


### H118 · Anlamsız karşılaştırma tabloları (Öge / Sınıf / Gerekçe) (2026-10-27)
- **Çözüm:** swipe_matching tablo dışı bırakıldı; venn/feature_bidding yalnız ≥3 satır, her gerekçe ≥7 kelime ve benzersizse alınır.
- **Kural:** Karşılaştırma yalnız iki GERÇEK tıbbi kavramı (hastalık, yapı, ilaç, mekanizma) ayırt eder; "X mi Y başlığı mı" gibi meta sınıflama, tek cümlelik özdeş gerekçe, bozuk Türkçe yasak. Yazar parçalarında da yazılmaz; yazar/denetçi bunu kontrol eder.
- PDF/yazdırma: belge yalıtılmış iframe'de yazdırılır; uygulama DOM'unda yazdırma ve sayfa yüksekliğine eşit sabit yükseklik YASAK (boş sayfa/renk karışması).


### H108 · Tablo rozetleri harf harf dikey; Ders seçenekleri kartları uzayıp taşıyordu (2026-10-28)
- **Çözüm:** eski kural `svg.di15-ik` ile kapsandı, rozete `white-space: nowrap; flex: none`. Menüde alt liste/düzen `grid-column: 1 / -1`, ızgara `align-items: start`.
- **Kural:** Yeni CSS sınıfı eklemeden önce aynı adın kullanılmadığını grep'le; kısa ortak adlara (`-ik`, `-ad`) element/üst seçici kapsamı ver. `display: contents` ile çözülen sarmalayıcının açılır alt parçaları tam satır olmalı.


### H109 · Ders içerik kayıtlarında "Slayt s.N" kaynağı eksik (2026-10-28)
- **Çözüm:** `scripts/ders_icerik_kaynak.py` (adim→slayt→pdfSayfalari[0]) tüm paketlere uygulandı; kaynaksız iki terim silindi; `ders_icerik_dogrula.py` `s` eksikse ve iskelet terimde HATA verir.
- **Kural:** Ekranda gösterilen her kaynak alanı doğrulayıcıda zorunlu olur; sayfa uydurulmaz, bulunamayan kayıt silinir (el kitabı §19 11a).


### H125 · Ders içerik terimlerinde genel sözlükten bağlam dışı tanım, kopya terim, ipuçlu soru şıkkı (2026-10-28, k2-08)
- **Kural:** Terim tanımı dersin sayfasındaki bağlamla yazılır (genel sözlük yalnız yardımcıdır, ilk anlamı kopyalanmaz); kaynakta
  olmayan sayı/eşik yazılmaz. Terim eklemeden önce ad + `e` eşanlamları normalleştirilip kopya aranır; slayttaki yazım farkı
  (Gl13, FLBN, speksifikasyon) `e`'ye girer. Şekilden okunan kayıt `gorsel: true`. Doğru şık çeldiricilerle benzer uzunlukta yazılır.
- **Kapı — EKLENDİ:** `scripts/tam_hat/kaynak_kapisi.py` (terim adı sayfada mı → HATA; tanım az örtüşüyorsa UYARI, denetçi bağlamı okur),
  `soru_uslup.py` (≥6 kelimelik doğru şık en uzun ve 1,8× → HATA), `hazirlik.py` madde imi temizliği.
