# Aşama kuralları — ornek_soru

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/tam_hat/kural_secici.py`. 72 madde. Ayrıntı gerekirse madde başlığıyla defterde aç.

### H1 — Geçiştirici şık açıklaması (2026-10-18)
- **Kurul 2'de doğrusu:** Her şık (doğru dahil) için kavramın ne olduğu + ne işe yaradığı + bu soruda neden doğru/yanlış olduğu,
  2–3 cümle. Ayrıntı: `meds/docs/SIK_ACIKLAMA_STANDARDI.md`.
- **Kapı:** `meds/scripts/sik_aciklama.py`.


### Kurul 2 hattı için genel kural
- Her içerik türünde yazar + bağımsız denetçi geçişi; doğrulayıcı 0 HATA vermeden EMA seslendirmesine ve yayına geçilmez.
- Bu defterdeki her maddenin kapısı Kurul 2 hattının doğrulayıcılarına bağlıdır (2026-10-18):
  - Sınav asistanı, sesli çözücü, spot önem listesi doğrulayıcıları: her zaman HATA.
  - Öğren: `validate_learning_decks.py deck.json --oyun-zorunlu --kurul2`; sınav spotları: `sinav_spotlari/dogrula.py --kurul2`.
  - **Kurul 2 başlarken ders işçisinin denetimine (`meds/scripts/ders_isci/denetle.py`, Öğren çağrısı) `--kurul2` eklenmeli** ve
    işçi talimatına bu defter okutulmalı. Kurul 1 işçisi bayraksız çalıştığı için şimdilik etkilenmez.

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

### H30 — Çıkmış konu eşlemesi birebir olunca ders sessizce çıkmışsız kalıyordu (2026-10-23 K2 provası)
- Ders kayıt defterindeki konu "Gebelik Terminolojisi ve Kavramları", çıkmış bankasındaki müfredat konusu
  "Gebelik Terminolojisi/Kavramları" → `a_hazirla` 0 çıkmış buldu ve hata vermeden devam etti (önem listesi ve çözücü boş kalırdı).
- Düzeltme: `ders_zinciri.konu_eslesen_cikmislar` üç basamak: birebir → yazım farkı ("/", "&", "ve", noktalama) yok sayılarak →
  ≥0,92 benzerlik; hangi yolla eşlendiği günlüğe yazılır. Sınama: Gebelik 27 (yazım farkı), Sifilis 19 (birebir).

### H31 — Hesap sorusu yanlış alarmı + iç etiketin öğrenci metnine sızması (2026-10-23 K2 provası)
- Naegele tarih sorusunun doğru şıkkı ("10.02.2021") maddede yazmaz, kuraldan hesaplanır; önem görevinin çözülebilirlik kapısı
  "çözülemiyor" diyordu → doğru şık yalnız sayı/tarih/birimse kökteki kural terimlerinden ≥2'si maddede olması yeter.
- Ücretsiz model detay alanına "Q3 ve Q4'te verilen tarihler…" yazdı (öğrenci Q3'ü bilmez). Ortak kapı
  `cekirdek.etiket_sizintisi` (yönlendirici + `gorev.py dogrula`): pakette verilmiş kısa etiket öğrenci metninde kalırsa HATA;
  girdide tıbbi anlamda da geçen (S1 kalp sesi, L4 omur) muaf; iç veri görevleri `OGRENCI_METNI = False`. Kural `cikti_disiplini.md`.

### H32 — Zorluk parça içinde yuvarlanınca ders toplamı hedefin altında kalıyordu (2026-10-23 K2 provası)
- 6 parçanın 6'sı ücretsiz katmanda geçti ama birleştirme "zor %9 (hedef %15–25)" ile durdu: 3 soruluk parçada %20 zor → 0.
- Düzeltme: `_spot.zorluk_dagit` zorluğu ders düzeyinde dağıtıp parçalara dilimler; parça kapısı zor soruda plandan eksiği kabul etmez.

### H33 — Türkçe harfsiz metin kabul ediliyordu + kabul edilmiş iş yeni kapıdan geçirilmiyordu (2026-10-23 K2 provası)
- Gemini Flash-Lite bazı çözücü partilerini ve bir sesli bölümü baştan sona harfsiz yazdı ("dogum", "bagli", "oykusu");
  hiçbir kapı yakalamadı, partiler KABUL edildi (önceki e07 çözücü ve k1-64 sesli sınamalarında da vardı; yalnız geçici kopya).
- Ortak kapı `cekirdek.turkce_katlama`: sözlük paketin kendi girdisinden; girdide Türkçe harfle geçen kelimenin katlanmış
  biçimi ≥3 kelimelik bir alanda ≥2 kez varsa HATA (İngilizce alıntı, kimlik/tür alanı, büyük harfli OCR yanlış alarm vermez).
- Kabul edilmiş iş yeniden kullanılırken `yonlendir.kapi` ile güncel kapılardan geçirilir; geçemezse "yeniden" koşar.
- Betik onarımı `cekirdek.ses_onar` (SES_ONAR görevleri): ses alanlarında kısaltma/Roma rakamı `modul_okunus.donustur`
  ile ("MSH" → "mee see haa"); modelin üç turda düzeltemediği "büyük harfli kısaltma" hatası kalktı.
- Öncüllü soruda "kökle uzunluk uyumsuz" hatasına düzeltme ipucu eklendi (kok_ses öncüllerin hepsini okur).

### H34 — Ücretsiz katman zinciri: Gemini tavanı, Zen kapandı, OpenRouter eklendi (2026-10-23)
- Bir dersin önem + çözücü adımı ~50 Gemini çağrısı harcadı; ardından bütün Gemini anahtarları 429 ("quota" / "monthly
  spending cap"). "spending cap" dakikalık sınır sanılıp 20 sn bekleniyordu → artık anahtar tükenmiş sayılır.
- Zen: Muse Spark kaldırıldı (410), Zen ücretsiz katmanı yalnız OpenCode istemcisinden (403 FreeTierError) → zincirden çıktı
  (`MEDS_CLOUD_ZEN=1` ile geri açılır). 410 artık 404 gibi model atlatır.
- OpenRouter ücretsiz modeller zincire eklendi (`nvidia/nemotron-3-ultra-550b-a55b:free`, `google/gemma-4-31b-it:free`);
  görev defterinde `zen` yerine `openrouter`. Groq ücretsiz katmanında ~24 bin karakterlik düzeltme istemi 413 alıyor.

### H35 — Ücretsiz/yazılı içerikte betik kapılarından geçen tıbbi hatalar; denetim bulguları düzeltilmiyordu (2026-10-24)
- Betik kapılarından 0 HATA ile geçen 2x99 içeriğinde OpenCode GLM denetçisi gerçek hatalar buldu: gravida 8 yerine "7",
  çoğul gebelik minör iken "majör", VTE eşikleri ">4"/">2" yerine "4 ve üzeri"/"2 ve üzeri", ders dışı Leopold ayrıntısı.
- Düzeltme: denetim bulguları yazara geri döner (`yonlendir.bulgu_duzelt`), kapılar + önemde yapı sabit kalır
  (`onem_listesi.duzeltme_kisiti`: madde/örnek sayısı, puan), yeniden uygulanır ve yeniden denetlenir (iş başına ≤2 tur).
  2x99: 5 engelli işin 5'i OpenCode ile düzeldi, yeniden denetim 0 engelleyici.
- Yan hatalar: aynı W yolunda eski provaların işleri denetime karışıyordu → ders iş defteri `W/gorev/<kod>/isler.json`;
  çözücü `uygula` her çağrıda yeni numaralı dosya açıp kopya üretiyordu → dosya adı soru kimliklerinden, eski kopya temizlenir;
  önem değişince çözücü kaydı eski soruya göre kalabiliyordu → `cozucu_sorusu.eskiyen` kapısı (birleştirme HATA verir,
  çözücü adımı eskiyeni düşürüp yeniden üretir).

### H36 — Cümle sayacı sıra sayısı noktasını cümle sonu sayıyordu (2026-10-24, oturum kuyruğu sınaması)
- "8-10. haftalarda" iki cümle sayılıp "4 cümle (en çok 3)" yanlış alarmı veriyordu; yazar ifadeyi bozarak geçiyordu.
- `CUMLE_SINIRI` (cozucu_dogrula2.py, cozucu_dogrula.py, spot_cozucu/asistan_dogrula.py): rakamdan sonraki nokta ancak
  ardından büyük harfle başlayan cümle gelirse sınırdır. Sayım yalnız azalabilir; veri değişmedi.

### H54 — Benzer soru araması boş döndü, ders çıkmışsız üretildi (2026-10-24, k2-07 ikinci sınama)
- k2-07 Genel Anestezik İlaçlar: veritabanında bu konunun 19 çıkmışı varken `cikmis_adaylari` 30 sorguda da 200 + boş
  sonuç aldı (dizin o an hazır değildi). Hata sayılmadı: "0 çıkmış bağı", sesli metinde "0 önemli" vurgu.
  Birkaç dakika sonra aynı arama 40 aday verdi.
- Kapı: `isle.cikmis_adaylari` bütün sorgular boş gelirse 60 sn bekleyip bir kez yineler, yine boşsa iş durur (sonra
  yeniden dener). Çıkmışı gerçekten olmayan yeni konu yine üretilir; yalnız *hiçbir sorgu sonuç vermezse* durur.

### H55 — Görsel tablodan yanlış satır okundu; hocanın kendi çelişkisi kesin "sınav spotu" yapıldı (2026-10-24, k2-07)
- Bütün betik kapıları 0 HATA iken bağımsız tıbbi denetim (PDF ile satır satır) buldu:
  - s.63 Tablo 25.3 (görüntü): droperidol premedikasyon/sedasyon/antiemetik dozları **midazolama** yazılmış; kart, soru,
    checkpoint ve sesli metne yayılmış. Aynı tablonun opioid yarısı atlanmış.
  - s.6 "en zayıf desfluran" ↔ s.13 Tablo 25.1 MAK azot protoksit >100: iki zıt cevap öğretiliyordu. Kural: hocanın
    çelişkisi tek cümlede uzlaştırılır (halojenli uçucular içinde desfluran; tüm inhalerler içinde N₂O), kesin spot yapılmaz.
  - Tablodaki 0 değeri "seyrek" diye okunmuş (midazolam bradikardi); "(Katzung)", "standart kaynaklara göre" ekleri sızmış.
- Kural: Kurul 2+ her derste yayından önce PDF'le karşılaştıran bağımsız tıbbi denetim (ayrı oturum, yazar ≠ denetçi)
  zorunlu; görsel tablo satırı ilaç/değer eşlemesi görüntüden tek tek doğrulanır. Bulgular düzeltilip kapılar yeniden koşulur.

### H57 — Kurul 2 derslerinde çıkmışlar neredeyse hiç duyulmuyordu (2026-10-24, kullanıcı)
- Kurul 1'de derste 11–13 "Burası önemli", 33–40 çıkmış/sınav anışı vardı; k2-07'de 4/0, k2-02'de 1/2. Bilgi anlatılıyor,
  `cikmis` alanına bağlanıyordu ama sesli söylenmiyordu: H22 dolgu yasağı + `max(3, bölüm/2)` "Burası önemli" tavanı
  dayanaklı çıkmış uyarısını da sildi. k2-02'de ayrıca arama tek aday döndürmüştü (H54).
- Kural: çıkmış uyarısı dolgu DEĞİLDİR. Her `ilgili` çıkmışın bilgisi anlatılır ve ilk geçtiği cümlede sesli söylenir
  ("bu bilgi çıkmışta soruldu"); tavan yalnız çıkmış dayanağı olmayan "Burası önemli"ye uygulanır. Dayanaksız çıkmış anışı yasak.
- Kapı: `isle.cikmis_ses_kapsam` (sesli_kapsam'a bağlı, Kurul 2+): ilgili çıkmış anlatılmamış / sesli uyarısız → HATA;
  "çıkmış/sınavda soruldu" geçen cümlede `cikmis` boş → HATA. Arama kurul filtresiyle <10 aday dönerse filtresiz yedek arama.

### H62 — Quiz Üretiminde Öncelik Sırasının İhlali, Çifte Analiz Maliyeti ve Yarış Durumu Hatası (2026-10-26)
- **Çözüm & Kural:**
  1. **Öncelik Kilidi (Priority Lock):** Sesli Ders (Audio Lesson) `COMPLETED` (onaylı `konusma_v2.json` ve 0 HATA denetim) durumuna geçmeden Quiz soru üretim ajanları KESİNLİKLE tetiklenemez.
  2. **Kapsam Kilidi (Scope Lock):** Quiz üretimi şimdilik YALNIZCA `Farmakoloji` (`Tıbbi Farmakoloji`) dersi için aktiftir. Kod altyapısı ders-bağımsız (`course-agnostic`) kurulmuştur.
  3. **Single Source of Truth:** Sesli dersin ilk analiz adımında üretilen `atomik_bilgi_envanteri.json`, hem Sesli Dersi hem de ardından çalışacak Quiz Ajanını besler. İkinci bir LLM analizi yapılmaz; mükerrer araştırma yasaktır.
  4. **2x Çapraz Sorgulama ve Batch Processing:** $N$ atomik bilgi $\rightarrow$ en az $2N$ soru. Token limitine takılmamak için en fazla 25 atom (50 soru) partileri halinde döngüyle işlenir.
- **Kapı:** `meds/scripts/quiz_motoru/quiz_dogrula.py` (Öncelik kilidi, 2x soru kuralı, 5-15 sn okunma süresi, gerekçeli şık açıklamaları, sıfır halüsinasyon). Çıkış kod 0 olmadan yayın yapılamaz.


### H66 — İlgili çıkmış sorular sesli derste hiçbir cümleye bağlanmamış (2026-10-26, k2-24 epilepsi)
- **Çözüm / kural:** Yazar, `ilgili: true` her çıkmışı `kanit.sayfa`/`slideNumber` sayfasında bilgiyi taşıyan cümlenin `cikmis` listesine bağlar ve o cümlede sesli uyarı ("Bu bilgi çıkmış sorularda soruldu.") verir. Kapı (`isle.py::cikmis_ses_kapsam`) gevşetilmedi.


### H69 — `cikmis_baglantilari.json` liste yerine nesne sarmalayıcısıyla yazıldı (2026-10-26, k2-46 sempatomimetikler)
- **Çözüm / kural:** `cikmis_baglantilari.json` daima kökte bir liste (`[{"soru_id": ..., "soru": ..., "ilgili": bool, "aciklama": ...}]`) olarak yazılır. `denetle.py` ve `arsiv_yayinla.py` doğrudan liste formatı bekler. Dosya düzeltildi, 0 HATA ile Oracle'a dağıtıldı.


### H71 — PDF metnindeki ayrışık (decomposed) harfler terim eşleşmesini bozuyordu (2026-10-26, k2-07 genel anestezik ilaçlar)
- **Çözüm / kural:** `Sayfa` sınıfı PDF kelimelerini okurken `unicodedata.normalize("NFC", w)` uygular; `bul()` de terimi NFC'ye çevirip token'lara ayırır. Kapı gevşetilmedi. Yeni PDF okuyan her betik kelimeleri NFC'ye çevirmeden eşleştirme yapmamalıdır.


### H74 — Madde imi kelimeye yapışık gelince terim işaretlenemiyordu (2026-10-26, k1-35 prenatal tanı)
- **Çözüm / kural:** `Sayfa` kelimeyi okurken baştaki "o" yalnız **ardından büyük harf geliyorsa** (madde imi kalıbı) ayrılır; kutu aynı kalır. Madde başındaki terimler de artık işaretlenir. Kapı gevşetilmedi.


### H78 — Gece otomatik LLM hattı kullanıcının Claude limitini tüketti; Oracle ders işçisi manuel moda geçişin dışında kalmıştı (2026-10-27)
- **Çözüm:** Oracle işçisi durduruldu (`restart=no`, ayar duraklat/otomatik kapalı/günlük 0), `.env` anahtarı `#KAPALI`;
  `meds-hat-gece`, `meds-olasi-soru` maskelendi; `otomasyon/llm_kilit.py` (MEDS_LLM_ELLE=1 yoksa çıkış 75, systemd altında
  panel bayrağı şart) 11 betiğe ve `yonlendir._claude/_ajan`'a bağlandı; Gemini onarım işçisi duraklatılmış başlar, Faz14
  kuyruğu yalnız `POST /api/admin/faz14-kuyruk/baslat` ile.
- **Önleme kuralı (AGENTS.md kural 20):** "kapat" kararı her makinede (yerel + Oracle konteyner ayarları + `.env` anahtarları)
  ayrı ayrı doğrulanır; yeni LLM betiği kilitsiz yazılmaz; zamanlayıcı/izleyici/setInterval ile LLM çağrısı yasak.


### H79 — Otomatik çıkmış→cümle eşlemesi (vektör) derse ait olmayan soruları "çıkmış" diye bağladı (2026-10-27, y25-k2-01)
- **Çözüm:** Elle doğrulandı: 7 soru (4 doğrudan, 3 ilişkili), her birine `s` (slayt), birebir `kanit`, `seviye`,
  `dogrulandi:true`. Slayttaki yanıp sönen çıkmış chip'i yalnız `dogrulandi` kayıtları gösterir; `degerlendirme_dogrula.py`
  kanıtın slaytta birebir geçtiğini denetler.
- **Önleme kuralı:** "Çıkmışta soruldu" vurgusu ve chip yalnız doğrulanmış, slayt kanıtlı eşlemeye dayanır; vektör benzerliği
  yalnız aday listesidir. Metindeki "Bu bilgi çıkmış sınavda sorulmuştur" cümleleri de aynı kanıtla teyit edilir.


### H82 — Çıkmış soru penceresi şık seçilince kayboldu, ders sürmedi (2026-10-27, sınamada yakalandı)
- **Çözüm / kural:** Durum modül düzeyinde (`useSyncExternalStore`), pencere `CdCikmisPencereKok` ile `document.body`'ye
  portal; sanal listede çizilen bileşen kalıcı durum tutmaz. Sınama: çalarken aç → ses durur, kapat → aynı saniyeden sürer.


### H83 — "Çıkmış" diye gösterilen iki soru doğrulanamadı; biri sitede yüklenmedi (2026-10-27, kullanıcı bildirdi)
- **Çözüm:** Her soru ham belgede arandı (`meds_downloads/donem3/3. Sınıf/Kurul 2/2.Kurul-2021.pdf`, `21 22.txt`,
  `2. kurul .pdf`); kaynağı bulunan 5 soru kaldı, her kayda `kaynak` (belge + sayfa) yazıldı ve pencerede gösteriliyor.
- **Önleme kuralı:** Çıkmış eşlemesi yalnız **ham sınav belgesinde bulunan** soruyla yapılır; banka etiketi ("verified",
  "altin_standart") kanıt değildir. `kaynak` alanı olmayan kayıt `degerlendirme_dogrula.py`'de HATA. Gizli kopya
  (sunulmayan id) eşlenmez; hatırlama listesinden gelen sorunun şıkları "sonradan tamamlandı" diye belirtilir.


### H84 — Kaynağı olmayan 86 Kurul 2 "çıkmış"ı Check-Solve onayıyla görünür kalıyordu (2026-10-27)
- **Çözüm:** 86 soru `karantina.json`'a `neden: kaynak_bulunamadi` ile yazıldı (silme yok; yedek `meds_temp/karantina_yedek_oracle_20261027.json`).
  `kaynakBulunamadi()` onay muafiyetinden ÖNCE uygulanır; `canliDers.ts` çıkmış listesini aynı kuralla süzer.
- **Önleme kuralı:** Banka/çıkmış eklemeleri ham sınav belgesindeki yerle (belge + sayfa) gelir; kaynak gösterilemeyen soru
  "çıkmış" olarak yayınlanmaz. Bir onay katmanı (Check-Solve, Faz 14) kaynağın yokluğunu gidermez. Geri alma: soruyu
  `karantina.json`'dan çıkarmak.


### H86 — Ders işçisi denetimi örnek soru şık açıklamalarını standart kapıdan geçirmiyordu (2026-10-27, k2-03)
- **Çözüm:** `denetle.py` Kurul 2+ dersinde her şık açıklamasını `sik_aciklama.denetle` + `turkce_uslup.denetle` ile HATA verir.
  k2-03'ün 110 şık açıklaması yeniden yazıldı; q18 çeldiricileri dersin kendi kavramlarıyla değiştirildi.
- **Önleme kuralı:** örnek soru çeldiricisi de müfredattan (öğretilmiş komşu kavram) seçilir (AGENTS kural 4, 9).


### H89 — Slayttaki yapışık madde imi glifi (U+F06E) kısaltmayı ve kanıt eşlemesini bozdu (2026-10-27, k2-02/k2-03)
- **Çözüm / kural:** `kisaltma_sozlugu.adaylar` ve `degerlendirme_dogrula.norm` U+F000–F8FF ve madde imi işaretlerini ayırıcı/boşluk
  sayar. Yeni metin işleyen her betik slayt metnini bu karakterlerden arındırarak karşılaştırır.


### H94 — Çıkmış listesinde birleştirilmiş gizli kopya: çip 404 verdi (2026-10-27, k2-03)
- **Kural:** `cikmis_konum` yalnız sunulan soru kimliklerini içerir; canlı doğrulamada her kimlik `/tek` 200 vermeden ders tamam sayılmaz.


### H95 — Yayın düzeltmesinde olmayan alan; PDF eşleyici durdurulan işçi kapsayıcısında (2026-10-27, k2-03/k2-04)
- **Çözüm:** `y.b.get("ders_id")`; PDF eşleme tek seferlik `docker run --rm -u 1001:1001 --entrypoint python3 medsoru-isci:latest`
  (aynı bağlar, LLM anahtarı yok) ile; deste PDF'i 200 doğrulandı.
- **Önleme kuralı:** yayın betiği değişikliği Oracle'a gitmeden önce yerel taslakla `kaynak_kimligi_esnek` ve `--deneme` akışı
  çalıştırılır; yayından sonra `/api/lecture-pdf/deck/<deck>/0` 200 kontrolü zorunlu.


### H96 — Önem/çözücü zinciri ham belgede olmayan soruyu "çıkmış" diye kullandı (2026-10-27, k2-03)
- **Çözüm:** soru önemden `elenen_cikmis`e, çözücü ve `cikmis/2p01.json`'dan çıkarıldı (numaralar `numara.json`'da sabit).
- **Önleme kuralı:** zincirden sonra önem/çözücü/asistandaki her çıkmış kimliği ham belge taramasında `bulundu` ve `/tek` 200
  olmalı; değilse yayına girmez. `-rNN` türetilmiş kayıt hiçbir zaman çıkmış sayılmaz.

### H89 — Canlı yarışma odası sorusuz kuruluyor, oyun hiç başlamıyordu (2026-10-27)
- **Çözüm:** oda yalnız `kaynak` (branş/ders/n) ile kurulur, sorular `oyunSoruKaynagi.ts`'ten; kaynaksız katılımda oda yoksa `room_error`. Yeniden bağlanan aynı kimlik puanını korur; istemci `disconnect` oda kimliğini siler.
- **Kural:** realtime odası veri olmadan kurulamaz; sunucu her başarısız katılımı açık hata mesajıyla döner.

### H90 — v15'te Toplu PDF penceresinin üstüne üst/alt çubuk biniyordu (2026-10-27)
- **Çözüm:** `TopluPdfDugme` pencereyi `createPortal(..., document.body)` ile çizer.
- **Kural:** tam ekran örtü/pencere bileşenleri daima body'ye portal ile çizilir; sayfa içi z-index'e güvenilmez.


### Tasarımdaki animasyon/3B ögesini "yok" diye atlamak (2026-10-27, Hücrem)
- **Kural:** Tasarımda olan animasyon/3B atlanamaz; zor ya da bağımlılık gerektiriyorsa kullanıcıya sorulur, plana "yok" diye yazılmaz.


### H101 · Kronometre sayfa değişince kayboluyor, iki sayaç aynı anda açılıyor (2026-10-27)
- **Çözüm:** Kronometre uygulama kökünde (`App.tsx`, `V15Icinde`) tek kez bağlanır; Odak panelin sekmesidir (`KapsulV15 gomulu`), biri başlayınca öteki duraklar (`medsoru:sayac`). Baloncuk `.cd-dock`'u izler: mini oynatıcının sağ ucuna kaynaşır, tam oynatıcının sağ üstüne oturur.
- **Kural:** Sayfalar arası kalıcı olması gereken yüzen öğe (sayaç, oynatıcı) asla sayfaya/üst bara bağlı bileşenin içine konmaz; uygulama kökünde tek örnek olarak bağlanır. Aynı işlevin ikinci yüzen örneği eklenmez.


### H103 · Çıkmış adayı farklı dönem/ders sınavından geliyor; ham anahtar bankadaki cevapla çelişiyor; bankada olmayan çıkmışlar (2026-10-27, k2-05 Nörolojik Muayene)
- **Kural:** Çıkmış eşlemesi yalnız (a) ham belgenin DÖNEMİ ve DERSİ bu ders olan, (b) basılı anahtarı banka cevabıyla uyuşan, (c) slayt kanıtı birebir olan sorularla yapılır. Ham belgede olup bankada olmayan soru eşlenmez, `cikmis_taslak.json › bankada_yok_ham_belgede_var` listesine yazılıp bankaya ekleme kararı ana oturuma bırakılır. `-rNN` kayıt ham belgede doğrulansa bile karar ana oturumundur.


### H107 · Çıkmış eşlemesi: banka yıl etiketi ham belgeyle çelişiyor, yeniden yazılmış kökler, basılı anahtar yok (2026-10-27, k2-08)
- **Kural:** `kaynak` ham belge adı + sayfa/soru no; çelişen yıl `yil_notu`na; basılı anahtar yoksa `anahtar_notu` ("tıbbi tutarlılık kontrol edildi"); kökü yeniden yazılmış sürüm ya da slayta ters doğru şık eşlenmez.


### H104 · Soru çöz sayfasında Araçlar görünmüyordu (2026-10-27)
- **Çözüm:** Sabit yükseklik kaldırıldı (sayfa normal kayar); özet kartları tek satır, test kutusu sıkı, araçlar ızgara.
- **Kural:** İçerik sayfalarında ekrana sabit yükseklik + iç kaydırma kurma; büyüyebilen içerik (süzgeç, liste) başka bölümü görünmez kılar.


### H119 · Örnek sorularda öznel/ders çağrıştıran kök ve rastgele slayt sorusu (2026-10-27)
- **Kural:** Kök bağımsız ve çıkmış-benzeri kalıpta; ders/slayt/bölüm göndermesi yok; her soru kazanım–konu bağlı, tıbbi ve sınav değerli. Kaynak: `TALIMAT.md` §4, `TALIMAT_ONEM.md`, `KURUL2_DERS_STANDARDI.md` §10.9.



### H107 · "Günlük çözülen soru" çubukları çok genişti; ajan sınama verisi tarayıcıda kalmıştı (2026-10-27)
- **Çözüm:** çubuk `max-width: 24px; align-self: center`. Sahte kayıtlar (hepsi `20:11:00.929Z` damgalı) silindi, eşitleme sarmalayıcısıyla temiz hal yazıldı.
- **Kural:** Alt ajan/ajan, eşitlenen profil anahtarlarına (userKvSync izin listesi) sınama verisi YAZMAZ; sınama gerekiyorsa ayrı anahtar ya da `?demo` bayrağı kullanılır. Ajan raporunda "geri aldım" deniyorsa tarayıcıda doğrulanır.


### H120 · Dallanmalı soruda doğru/yanlış bayrağı ters işaretliydi (2026-10-27, k2-01)
- **Kalıcı çözüm:** doğrulayıcıya `klinik-karar-bayrak` HATA kapısı (geri bildirim "Doğru/Yanlış" ile başlıyor ve bayrakla çelişiyorsa). Önleme: bayrak ve geri bildirim tek yerden üretilir; denetçi kapı dışı tutarlılık taraması yapar; doğru şık hep ilk sırada olmaz.


### H122 · Paylaşılan çıkmış soruda süzgeç/kategori alanları öne çıkıyordu (2026-10-28)
- **Çözüm:** `PastExamsView.tsx`'te `sharedId` varken PageToolbar, v15 giriş kartları ve V12Frame gizlenir; "Tüm sorular" düğmesi paylaşım bandında kalır.
- **Kural:** Tek öğeye indirgenen (paylaşım/derin bağlantı) görünümde yeni süzgeç/giriş bileşeni eklenirse `sharedId` ile koşullanır.


### H109 · Aynı cihazda iki sekme açıkken profil eşitleme fırtınası (2026-10-28)
- **Çözüm:** `ORIGIN` cihaz düzeyinde (`medsoru_sync_origin_v1`), son gönderilen parmak izi `localStorage`'da (`medsoru_sync_fp_v1`); ikisi de eşitleme izin listesinde değil. Sınama: iki yeni kodlu sekmede ikinci sekme açılınca ilk sekme 25 sn'de 1 not çekme + 1 yedek (önce 55 istek).
- **Kural:** Sekmeler arası ortak olan duruma (localStorage) bağlı karar verilerini sekme belleğinde tutma; yayın kaynağı kimliği cihaz düzeyinde olmalı. Sınamada eski kodlu açık sekmeleri kapat (yeni/eski sürüm karışımı ölçümü bozar).


### H123 · Tam içerik hattı ders başına 4–6 saat sürüyor, soru/metin/PDF hataları geri dönüş yaratıyordu (2026-10-28)
- **Kural:** `docs/TAM_HAT_HIZLI_AKIS.md` — E0 `hazirlik.py` (döküm GPU ≤2500 MHz, AGENTS §10 altıncı istisna); alt ajana yalnız
  `kural_secici.py --oku <aşama>`; yalnız hatalı parça yeniden yazılır (sayısal hedefte ±%10, kalite hatasında tolerans yok);
  ders başına tek denetçi.
- **Kapı — EKLENDİ:** `scripts/tam_hat/soru_uslup.py` (ders çağrıştıran kök, ipuçlu uzun doğru şık, kazanım bağı, kalıp payı),
  `kaynak_kapisi.py` (kayıt içeriği `s` sayfasında mı), `pdf_tarama.py` (boş sayfa, taşma, üst üste, harf harf kırılma).


### H124 · Soru çözücüde Kurul 2 seçili görünürken Kurul 1 dersleri listeleniyordu (2026-10-28)
- **Çözüm:** çözücü ve En önemliler başlangıcı `useSeciliKurul()` kullanır (vurgulanan kurul = listelenen kurul), "Tümü" kaldırıldı, ad önekindeki "Kurul N" atılır, başlanmış dersler önde sıralanır. Olası sorular şeridi `.ks.kseridi` olarak kapsamlandı.
- **Kural:** seçili durum gösteren bir bileşen ile içeriği süzen kod AYNI kaynaktan (aynı kanca) okur; görsel vurgu için ayrı varsayılan hesaplanmaz. Ortak bileşenlerin sınıf önekleri (`.ks`, `.kh`) başka sayfa CSS'inde kapsamsız kullanılmaz.


### H125 · Ders içerik terimlerinde genel sözlükten bağlam dışı tanım, kopya terim, ipuçlu soru şıkkı (2026-10-28, k2-08)
- **Kural:** Terim tanımı dersin sayfasındaki bağlamla yazılır (genel sözlük yalnız yardımcıdır, ilk anlamı kopyalanmaz); kaynakta
  olmayan sayı/eşik yazılmaz. Terim eklemeden önce ad + `e` eşanlamları normalleştirilip kopya aranır; slayttaki yazım farkı
  (Gl13, FLBN, speksifikasyon) `e`'ye girer. Şekilden okunan kayıt `gorsel: true`. Doğru şık çeldiricilerle benzer uzunlukta yazılır.
- **Kapı — EKLENDİ:** `scripts/tam_hat/kaynak_kapisi.py` (terim adı sayfada mı → HATA; tanım az örtüşüyorsa UYARI, denetçi bağlamı okur),
  `soru_uslup.py` (≥6 kelimelik doğru şık en uzun ve 1,8× → HATA), `hazirlik.py` madde imi temizliği.


### H110 · Çıkmış sorular yıl çipi 21, listede 20 soru (2026-10-28)
- **Çözüm:** çip sayımı aynı `facetPass` + arama ile; yalnız çipin kendi boyutu (yıl çipinde `year`, ders çipinde `discipline`) hariç tutulur (yönlü süzgeç kuralı). Sınama: 12 yıl çipinin toplamı 502 = liste; 2023-2024 çipi 26 → liste 26.
- **Kural:** Süzgeç çipi/rozetindeki sayı, o çip seçilince listenin göstereceği sayıyla aynı yoldan (aynı süzgeç zinciri) hesaplanır; ayrı, eksik bir sayım yazılmaz.


### H111r · Soru haritası hücrelerinde yazı kontrastı 2.6–4.0 (2026-10-28, Soru çöz)
- **Çözüm:** `SoruHaritasiV15.tsx` ölçeği iki banda ayırır: açık bant %10–40 (koyu yazı), koyu bant %90–100 (açık yazı); ara ton kullanılmaz. DOM kontrast ölçümü: 7 ihlal → 0.
- **Kural:** Yoğunluğa göre boyanan hücrede yazı rengi tek eşikle seçiliyorsa, eşiğin iki yanındaki zemin tonları her iki yazı rengiyle de 4.5'i geçmelidir; geçmiyorsa ara tonlar atlanır.


### H111u · Çıkmış sorular kart görünümü sınırsız büyüyor, Odak ızgarası 4.372 düğme çiziyordu (2026-10-28, Soru çöz, başarım)
- **Çözüm:** Kart görünümü kayan pencere: yalnız son 60 kart (`RICH_WINDOW`) çizilir, üstte düşenler tarayıcının kaydırma çapasıyla görünen kartı oynatmaz, üstte "Önceki soruları göster (n)" düğmesi; sayaçlar `richLimit` ile gösterilir. Odak ızgarası geçerli sorunun 100'lük bloğunu çizer, ‹ › ile blok değişir. Ölçüm: 8 kaydırmada DOM 34.226 → ~7.100 (sabit); Odak açılışı ~650 düğüm.
- **Kural:** Kaydırdıkça yüklenen listeler sınırsız büyümez (pencere ya da sanal liste); yüzlerce öğelik gezinme ızgarası bloklara bölünür.


### H127 · Slayttaki şekil/deney anlatılmadı, "ders yorumuna girmez" diye geçildi (2026-10-28, k2-05 Nörolojik Muayene, sayfa 32–33)
- **Kalıcı çözüm ve kural (Şekil ve deney anlatım kuralı, `KURUL2_DERS_STANDARDI.md` §8.12):**
  1. **Şekil kaynaktır.** Slayttaki çizim, fotoğraf, şema, grafik, tablo, mikroskopi ve görüntüleme; içindeki oklar, etiketler, işaretler (X, kesik/kalın çizgi, renk), panel karşılaştırmaları ders içeriğidir ve anlatılır. "Slaytta yazmıyor" şekli atlama gerekçesi değildir.
  2. **Deney/test/muayene görseli** her zaman beş soruyla anlatılır: (a) ne sınanır ve neden yapılır, (b) nasıl uygulanır (görselde ne görülüyorsa adım adım), (c) normal sonuç, (d) her patolojik panel/sonuç ne demektir ve hangi lezyonu gösterir, (e) sonuçlar birbirinden nasıl ayrılır (sınavda karıştırılan çift).
  3. **Çok panelli şekil:** her panel ayrı ayrı adlandırılır ve karşılaştırılır ("soldaki normal…, ortadaki…, sağdaki…"); işaretlerin anlamı (X = hasarlı yapı, kalın ok = sesin daha güçlü duyulduğu taraf) açıklanır.
  4. **Yalnız adı geçen kavram/test:** ilk geçtiği yerde 1–2 cümleyle ne olduğu ve ne ölçtüğü söylenir (Terim kuralı §8.5). Ayrıntı slaytta/şekilde ya da hoca dökümünde varsa o kadar açılır; yoksa uydurma yorum eklenmez ama ADI DA BOŞ BIRAKILMAZ.
  5. **Kaçamak meta cümle YASAK:** "ders bunun yorumuna girmez", "yalnız adını verir", "ölçütünü vermez", "şekilde ayrıntı yok", "nasıl uygulandığı gösterilir" gibi öğrenciye bir şey öğretmeyen cümleler yazılmaz. Gerçekten kaynakta bilgi yoksa cümle hiç yazılmaz; konu olduğu kadar anlatılır.
  6. **Şekil paragrafı betimlemeyle bitmez:** yalnız "…gösterilir / görülür / yer alır" cümlelerinden oluşan şekil paragrafı eksik sayılır; şeklin öğrettiği bilgi (mekanizma, sonuç, ayırıcı nokta) eklenir.
  7. **Çizim katmanı anlatımı izler:** her panel/sonuç anlatılırken lazer ve kontur o panele gider (kural 17/18; bir cümle = bir panel).
  8. **Denetçi şekle bakar:** bağımsız denetçi metni okuduktan sonra şekilli/tablolu her sayfanın görüntüsüne bakıp "şekildeki her panel/işaret anlatıldı mı" listesini işaretler; eksik varsa GEÇMEZ.

### H131 — Kurul 2 çıkmışlarında başka kurul soruları ve yanlış konu etiketleri (2026-10-28, kullanıcı bildirdi)
- **Çözüm:** 574 soru ders programı + kazanım + 25-26 ders metni ile tarandı (`meds_temp/kurul2_soru_tespit/`, rapor `meds_database/derived/quarantine/kurul2_konu_tespit.csv`). 19 soru `karantina.json`'a `neden: kurul2_disi` ile yazıldı (`kaynakBulunamadi` bu nedeni de onay muafiyetinden önce uygular); 52 soruda konu/ders etiketi düzeltildi (`eskiKonu`/`eskiDers` saklı). 9 Primer Myelin önerisi 2026 programında ders olmadığı için uygulanmadı. Yedekler aynı klasörde.
- **Önleme kuralı:** Yeni çıkmış eşlemesinde konu etiketi içerik ile doğrulanır; geri alma: karantina kaydını silmek / eskiKonu'yu geri yazmak. Açık: 86 "elle bakılmalı" soru.


### H132 — Karantina listesi eskimişti; OCR ikizleri ve parça kayıtlar karantinada duruyordu (2026-10-28)
- **Çözüm:** 53 kopya `birlestirmeler.json` grubuna (tekrar arşivi) alındı, `tekrarArsivi{asil,eslesen,onceki}` ile geri alınabilir; `karantina` etiketi ve `karantina.json` girdisi kaldırıldı. Yedek: `yedek/karantina_20261028/`.
- **Önleme:** Karantinaya almadan önce aynı soru/şık kümesine sahip sağlam kayıt aranır (stem+şık Jaccard); varsa karantina değil tekrar arşivi. Üretilmiş soru "çıkmış" etiketi taşımaz.


### H133 — Kaynağı doğrulanamayan sorular gizlenerek kaybedilmişti; "Çıkmış–Örnek" sınıfı (2026-10-28)
- **Çözüm:** 4 bağımsız denetçi 104 soruyu müfredat + ders notu + tekrar taramasıyla değerlendirdi: 72 `cikmis_ornek` (hem Çıkmışlar'da hem `k2-cikmis-ornek` Örnek sorular dersinde, öğrenciye "çıkmış olduğu doğrulanmadı" rozetiyle; sesli ders çıkmış chip'inden hariç), 15 serbest çıkmış, 9 tekrar arşivi, 7 karantinada (`siniflama` alanıyla gerekçeli). 5 soru ders notuna göre düzeltildi (`duzeltmeOnceki` saklı).
- **Önleme:** Kaynağı doğrulanamayan ama doğru soru gizlenmez, `kaynakSinifi=cikmis_ornek` ile etiketlenip öğrenciye belirtilir; çıkmış vurgusu yalnız doğrulanmış kaynağa dayanır.


### H140 — Bazı sayfalar aktif kurul yerine Kurul 1 ya da "Tümü" ile açılıyordu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Kazanımlar, Örnek sorular (kurul seçici + kurul önekli sayaçlar), Test oluştur (kayıtlı ölçüt yoksa) `varsayilanKurul()` ile açılır; yalnız Kurul 1 verisi olan Öncelikli dersler bunu başlıkta yazar. Yeni kurul bağımlı sayfa varsayılanını `varsayilanKurul()`dan alır.


### H144 — Deneme ekranında soru numarası çubuğuna dokunulamıyordu; telefonda süre gizliydi (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Düğme 24 px dokunma alanı, görünen çizgi `::before`; telefonda süre kalır, doğru/yanlış sayaçları kalkar (soru numarası çubukta). İnce göstergelerde dokunma alanı görsel çizgiden ayrı tutulur.


### H145 — Örnek sorularda "Başla" düğmesi harf harf dikey yazılıyordu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Izgaraya `ey` alanı eklendi (masaüstü sağ sütun, telefonda ayrı satır). Izgara satırına yeni öğe ekleyen her katman ona alan tanımlar.


### H152 — Yönetimde ders ayrıntısından o dersin sorularına geçiş yoktu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Sorular kartında örnek sorular, çıkmış sorular ve havuz için ders konusuyla süzülmüş (`?q=<konu>`) bağlantılar. Sayı gösteren her özet, o kayıtların listesine bağlanır.


### H153 — Yönetimde Yerel kipte hangi veriye bakıldığı belli değildi; birleştirmede asıl soru görünmüyordu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Yerel bandı + sekme adında `[Canlı]`/`[Yerel]`; birleştirme onayında asıl soru açılır listeden seçilir; `.m16-liste` satırı sarar, seçici alt satıra iner.


### H154–H169 — Sayfa denetimi dördüncü tur, öğrenci sitesi orta bulguları (2026-10-28)
- **H154/H155 Kutlama:** kuyruk hangi ekranda olursa olsun hemen açılıyordu → deneme, çıkmış testi, soru çözücü ve sesli ders ayrıntısında ertelenir. Rozetteki "3" ödül seviyesiydi, "Hepsini geç" sayısı bu ödülü saymıyordu → "3. seviye" ipucu, sayaç tüm kuyruk.
- **H156 Bugün:** halka öğrencinin çalışmasını, alt kart okul programını gösteriyordu (farklı veri, aynı dil) → "bugün çalışma yok" / "Okuldaki bugünkü 2 ders sona erdi".
- **H157 Deste sayısı:** merkez yayında olmayan desteleri de sayıyordu → kitaplıkla aynı ölçüt (`isPublished`, `kurulOf`).
- **H158 Sesli ders süzgeci:** "2026–27/2025–26" etiketleri telefonda satırı taşırıyordu → "Bu yıl/Arşiv"; boş listede "Geçen yılın derslerini aç".
- **H159/H160 Soru çöz kartları, Yanlışlarım:** uzun etiket/kırılan düğme → kısa ad, tek satır; boş Yanlışlarım'da "Soru çözmeye başla".
- **H161 Boş Check Up:** düz metin → başka kurulun check-up'ı ve hazırlık araçlarına düğme.
- **H162 Kazanım "8/2":** veri doğruydu ("0/2"); sabit genişlikli yazı tipinin çizgili sıfırı 8 okunuyordu → normal yazı tipi + tabular rakam. Sayaçta mono yazı tipi kullanılmaz.
- **H163 Sınav planı hız çipleri:** 40×19 px → ≥32 px.
- **H164 /profil:** /ayarlar ile aynı ekran → adres /ayarlar'a döner (eski bağlantı çalışır).
- **H165–H167 Boş durumlar:** İstatistik (çalışmaya başla), Sıralama (Üniversiteni seç), Arkadaşlar (Giriş yap: App.tsx `medsoru:giris-ac` olayı).
- **H168 Bildirimler:** eylem satırı kırılmıyordu ("Ok" kesik); silinemeyen okunmuşlar "temizle"yi etkin tutuyordu → satır sarar, düğme yalnız silinebilir varken etkin.
- **H169 Telefonda kurul:** üst çubukta kurul yolu yoktu → kompakt "K2" çipi.
- Masaüstü 24 px alt şerit uygulamada yeniden üretilemedi (tarama aracının boyut geçişi kalıntısı); değiştirilmedi.

### H200–H212 — Sayfa denetimi beşinci tur, öğrenci sitesi kalan bulgular (2026-10-28)
- **H200/H201/H205/H210 Sınava hazırlan:** boş "Planlama" başlığı yalnız içerik varken; sınav ağırlığı kartı nereye gittiğini söylüyor; olası sorular kartı ATP kilidini önceden yazıyor; telefonda sekme şeridi kenarda solar.
- **H202/H203 Soru haritası:** yılı belirsiz "?" sütunu renk ölçeğine katılıp en koyu hücreleri alıyordu → "Yılsız", sona alındı, ölçek dışı; telefonda yana kaydırma ipucu. Kural: belirsiz/eksik kategori renk ölçeğini belirlemez.
- **H204** Çıkmış arama yer tutucusu telefonda kesikti → anahtar sözcük önde.
- **H206/H207 Sesli ders:** küçült düğmesi `::after` ile ~44 px; bölme hap düğmeleri ≥28 px + aria-label.
- **H208** Hastalık dipnotları `::after` dokunma alanı.
- **H209 Çift başlık:** v15'te sayfa adı hem üst çubukta hem `PageHeader` h1'de görünüyordu → v15'te PageHeader başlığı görsel olarak gizli (ekran okuyucu için h1 kalır). Site geneli kural; yeni sayfa başlığı v15'te üst çubuktan gelir.
- **H211/H212 Sağlık:** açıklamasız sayı rozetleri dipnot biçiminde ("[14]"); "15 yıl" → "15 yıllık geçmiş".

### H220 — Üç sayfa aynı "bugün ne yapayım" işini bölüyordu (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Çözüm/kural (görev sınırı):**
  - **Bugün** = günün tek sayfası: plan halkası → Kaldığın yerler (araçlar arası devam) → hafta şeridi + Bugün yaptıkların (`MasaGunV15 gomulu`; yan kartlar gizli, süre/seri halkada ve şeritte). Hafta çubukları kaldırıldı.
  - **Listelerim ve notlar** (eski Çalışma masam, `/calis` aynı) = yalnız kişisel soru çalışma alanı (Soru çöz, Test, Listelerim, Notlar).
  - **Ders çalış merkezi** = ders araçları merkezi; "Devam et" yalnız sesli ders içindir.
  - Yeni "günlük özet" öğesi yalnız Bugün'e eklenir; diğer sayfalar kendi aracının durumunu gösterir.


### H242 — Çıkmış listesinde konum yoktu; geri dönünce liste baştan açılıyordu (2026-10-28, kullanıcı isteği)
- **Çözüm/kural:** Liste/Panel yerleşiminde iki görünüm de sayfalı (Kart 20, Kompakt 25): üstte "41–60 / 571 soru · sayfa 3/29", altta Önceki · sayfa seçici · Sonraki (`cikmis/CikmisSayfa.tsx`). Konum (süzgeç imzası + sayfa + sayfadaki sıra) `sessionStorage cikmis_konum`'a yazılır; dönüşte aynı sayfa açılır ve aynı soru yapışkan üst çubuğun altına yerleşir. Tuzaklar: rotadan çıkarken yapılan "başa kaydır" kaydı bozar (kayıt yalnız çıkmış adresindeyken), `scrollIntoView` yapışkan çubuğun altına gizler (ölçüm ve yerleştirme `.v15-top` alt çizgisine göre), geri yükleme birkaç kez yerleştirilir ve bitene dek kaydedilmez. Uzun liste ekranlarında konum sayfa + sıra olarak saklanır.


### H290–H295 — Yönetimde iş akışı uzundu: Gelen yalnız yönlendiriyordu, toplu işlem yoktu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Gelen'de satır ve çekmece işlemleri (Çözüldü / Yok say / Mesajı gizle / Kapat + iç not / Görüldü), aynı türde toplu işlem; `gelenOnbellekSil()` işlem uçlarında; yeni uç `POST /api/admin/gelen/hata/goruldu` (işaret `data/istemci_hata_goruldu.json`, hata yinelenirse geri düşer); VeriTablosu `dusur(t)` ile işlenen satır süzgeç/sayfa korunarak düşer. Soru şikâyetlerinde çekmeceden Çözüldü + toplu; çıkmışlarda toplu Gizle/Göster (onay + hedef + 8 sn Geri al). Not: "Yok say" şikâyeti `resolved` yapar (ayrı red durumu yok).


### H296 — Gelen'de tek satır işlemleri onaysız ve geri alınamazdı (2026-10-28, ajan sınaması)
- **Çözüm/kural:** Tersi olan işlemler (soru şikâyeti → yeniden aç, mesaj gizle → göster, geri bildirim kapat → aç) 8 sn "Geri al" verir, geri alınan satır listeye döner; tersi olmayan (topluluk şikâyetini yok say: şikâyet kayıtları silinir) tek işlem de "geri alınamaz" diyen onay ister. Yerelde tıklanarak sınandı (Çözüldü → Geri al, çıkmış toplu Gizle → Geri al; veri eski hâline döndü).

### H320–H329 — Görünürlük beş ayrı yerden düzenleniyordu (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Çözüm/kural:** Görünürlük YALNIZ Site › Görünürlük'te yazılır: "Sayfalar" (öğrenci sayfaları + menü) ve "İçerik" (kurul, ders, sesli, deste, paket, önem/asistan/çözücü; yeni uç `GET /api/admin/gorunurluk/icerik`, sayfalı, süzgeçli, katalogda olmayan ayar `sahipsiz`). Diğer sayfalarda `GorunurlukBaglantisi` (rozet + "Değiştir" → `site/gorunurluk?sekme=icerik&q=<anahtar>`). `site/menu` → Görünürlük. Gizleme onay + hedef, her yazım 8 sn Geri al, toplu değiştirme. Yerelde tıklanarak sınandı (tek + toplu, geri al sonrası ayar boş).


### H340–H347, H360–H374 — Sayfa denetimi düşük önemli bulgular (2026-10-28)
- **Kural:** Tehlikeli işlem ad kalıbıyla değil açık listeyle belirlenir (H182, H372). Açık çekmece/sekme adreste tutulur ki yenileme ve paylaşım aynı görünümü açsın.
- Açık öneriler (yapı): menü/başlık ad eşleşmeleri, `kurul_2` adres biçimi, yinelenen girişler (KMB, Sözlük/Hastalıklar, takvim), havuz dondurmanın Bayraklar'a taşınması, ses kuyruğunun sesli ders sekmesi olması, sürüm notu + dağıtım bilgisinin birleşmesi. Veri: kazanımlarda yinelenen konu 31, soru haritası 498 / çıkmış 502 farkı.


### H380–H387 — Kalan küçük öğrenci bulguları (2026-10-28)
- Menü etiketi, sayfa başlığı ve ROUTE_TITLES tek ada eşitlendi (Etkileşimli dersler, Sesli dersler, KMB dersleri, Müzik, Patoloji/TBG Check Up, Havuz doluluğu, Çevrimdışı ve indirmeler); içeriksiz kurul sekmeleri kesikli + "henüz yok"; telefonda kurul şeridi kenar soluklaştırma; sayaçlarda mono yerine tabular rakam; "Karma test · 20 soru" etiketi; testten çıkışta cevap varsa onay; KMB "Hazır/Yakında" ayrımı.

### H390–H392 — Veri tutarlılığı: yıldız işaretleri, soru haritası sayımı, deste kurul adları, yinelenen kazanım konuları (2026-10-28, kullanıcı onayıyla)
- **H390 Belirti:** Deneme ekranında soru/şık metninde `**değildir**`, `**Soru:**` ham görünüyordu. **Kök neden:** veri doğru (kasıtlı vurgu; çıkmışta 49 soru, Öğren klinik karar vakalarında 414 öge), `PracticeV15` metni işlemeden yazıyordu. **Çözüm:** `**…**` kalın yazıya çevrilir; veri değişmedi.
- **H391 Belirti:** Soru haritası Kurul 2'de 498, çıkmış sayfası 571+ gösteriyordu. **Kök neden:** 178 çıkmış soruda `isPastExam` alanı yok (kaynakları çıkmış PDF'leri); harita betiği yalnız `true` olanları sayıyordu. **Çözüm:** `scripts/v15/soru_haritasi.py` yalnız açıkça false ve gizli soruları dışlar; harita yeniden üretildi (K2 574).
- **H392a Deste kurul adları:** Kurul 1 için 12 yazım vardı; boş/"Ürogenital Sistem Komitesi" yazılı 4 deste öğrenci tarafında "Diğer"e düşüyordu. 74 destenin `committee` alanı "Kurul 1 - Ürogenital ve Obstetrik Kurulu" yapıldı (kaynak `interactive_learning_decks.json`, biçim birebir korundu; doğrulayıcı 0 HATA, paketler yeniden üretildi).
- **H392b Kazanım konu çiftleri:** Aynı dersin kesik/tam başlıklı iki kazanım kümesi (7 çift: K1 Genetik, K1 Üroloji ÜSE, K5 Demir, K5 Spondilodiskit, K6 Histamin, K6 Yaşlılıkta beslenme, K6 Biyokimya) tam başlıkta birleştirildi; yalnız birebir aynı 13 kazanım atıldı, kimlikleri taşındı (kazanım soruları, sınav çalışması, müfredat paketi, eşleme dizini byDeck yeniden üretildi; artık başvuru 0), slayt kanıtları birleşti. 25 konu başlığından hoca adı / "UZM." eki temizlendi. Ders kayıt defterine (`dersler/kN.json`) dokunulmadı: K5/K6 çiftleri orada iki ayrı ders kimliğidir (kural: kimlikler kalıcı). Betik: oturum yedeğiyle `kz/birlestir.py`.
- **Tuzaklar:** (1) `lite/`, `questions/`, `pastQuestions.json`, `sinav_calisma_k*.json` git dışıdır; dağıtım temiz `meds-dagitim` ağacından derler, bu dosyaların güncel kopyası oraya elle konmazsa canlı derleme eski veriyi gömer. (2) Çıkmışların canlı asıl kopyası Oracle `data/pastQuestions.json`'dır (sunucu bellekte tutup üzerine yazar); yerel `src/data/pastQuestions.json` yalnız yansıdır. Canlı çıkmış konu/kimlik güncellemesi ayrı, sunucu uçlarıyla yapılmalı (yapılmadı, açık).

### H393 — Canlı çıkmışlarda kazanım birleştirmesinden kalan eski konu adları / kimlikler (2026-10-28, kullanıcı onayıyla)
- **Çözüm:** Yeni yönetim ucu `POST /api/admin/sorular/cikmis/esleme-uygula` (varsayılan önizleme; `uygula:true, onay:"ESLE"` ile tam yedek `data/_yedek/pastQuestions.esleme-oncesi.<zaman>.json` + değişim dosyası `data/_yedek/cikmis_esleme_<zaman>.json`, sunucunun kendi kaydetme/yansıtma/canlı olay yolu, denetim kaydı) ve `POST …/esleme-geri {dosya, onay:"GERI"}`. Geçmiş kayıtlar (`checkSolveOriginal`, `eskiSurum`, `phase14Original`, revizyonlar) atlanır. Yerelde önizle→uygula→geri al denendi, yerel dosya birebir geri yüklendi; canlıda önizleme 56 soru/57 değer (plan ile aynı) → uygulandı, diskte kalan 0, geçmiş kayıtlardaki 82 değer dokunulmadan. Canlı değişim dosyası: `cikmis_esleme_2026-10-28T17-37-02-423Z.json`.
- **Kural:** Canlı çıkmış verisinde toplu değişiklik yalnız sunucu içinden, önizlemeli ve geri alınabilir yolla yapılır; geçmiş kayıt alanlarına toplu değiştirmede dokunulmaz.


### H435 — Örnek sorular hocanın yeni sınav kalıbını yansıtmıyordu (2026-10-29, kullanıcı bildirdi)
- **Kural / Önleme:** Patoloji örnek soru ve önem noktası `docs/PATOLOJI_HOCA_SORU_MANTIGI.md` + `scripts/patoloji_soru_isci/` kapısına göre yazılır: her önem noktasına ≥2 farklı kalıpta soru, çeldirici yalnız aynı dersin komşu kavramları, doğru şık en uzun olmaz. Sarı dolgu ve başlık önem sinyali sayılmaz; kırmızı tek başına "önemli" değildir (slaytların ~%42'si kırmızı).
- **Kapı:** `python3 scripts/patoloji_soru_isci/dogrula.py sorular.json paket.json` → 0 HATA.


### H436 — Ara soru şık açıklamalarında ileriye sızıntı ve kaynakta olmayan iddia (2026-10-29, bağımsız denetçi buldu)
- **Kural / önleme:** Şık açıklaması, ipucu ve çözüm de yalnız `ara.sayfa` ve öncesindeki slaytların bilgisini kullanır; tıbbi tanım slayt metninde yoksa yazılmaz. Bağımsız denetçi (TALIMAT adım 7) her soruda bunu slayt slayt arar; düzeltilen sorular ikinci kez denetlenir. Ders akış metni (Whisper dökümünden beslenmiş olabilir) tıbbi kaynak değildir; terim/sayı yalnız PDF sayfa metninden alınır.


### H442 — Yeni sayfanın CSS öneki başka bileşenle çakıştı; sekmeler dev daire, düzen tek sütun (soru dışa aktarıcı, 2026-10-30)
- **Çözüm:** önek `sx15` yapıldı (CSS + bileşen).
- **Önleme:** yeni v15 sayfası/bileşeni için önek seçmeden önce `grep -rn "\.<önek>[ {.:-]" src/styles src/components` ile boş olduğu doğrulanır; kısa (3–4 harf) önekler çakışmaya en açık olanlardır.


### H443 — Önizleme iframe'i genel `max-width: 100%` kuralıyla daraldı, sayfanın sağı kesildi (soru dışa aktarıcı, 2026-10-30)
- **Çözüm/önleme:** ölçekle küçültülen iframe/canvas'a satır içi `max-width: none` verilir; ölçekli öğenin doğal genişliği `getBoundingClientRect` ile doğrulanır (stil genişliği ≠ gerçek genişlik).


### H444 — DOCX ızgara sayfaları LibreOffice/Word'de ikiye bölündü; 26 sayfa 52 oldu (soru dışa aktarıcı, 2026-10-30)
- **Çözüm:** boş üst bilgi kaldırıldı (yalnız "her sayfada başlık" açıkken başlık üst bilgisi); hücrelere yalnız sağ/sol iç boşluk, üst boşluk hücre içi sabit paragrafla; satır aralığı yazı tipine göre bölünür (`TEK_SATIR`); sabit sayfa kipinde yazı ölçeği ×0,93, satır yüksekliği ×0,97 güvenlik payı. 26 model sayfası → 26 DOCX sayfası.
- **Önleme:** DOCX/PPTX üreten her değişiklik LibreOffice ile PDF'e çevrilip sayfa sayısı önizlemeyle kıyaslanır (`soffice --headless --convert-to pdf` + `pdfinfo`) ve her XML parçası ayrıştırılarak denetlenir; sabit yükseklikli tablo satırına üst/alt `tcMar` verilmez.


### H445 — Veride boolean `false` metin olarak "false" yazdı (soru dışa aktarıcı, 2026-10-30)
- **Çözüm/önleme:** soru verisini metne çeviren yardımcı yalnız string/sayı kabul eder (`kaynak.ts::s`); başka kaynaklardan alan okurken `String(x ?? '')` yerine tür denetimli dönüşüm kullanılır.


### H446 — Öğrencinin en çok çalıştığı ve çıkmışta sorulan bilgi anlatımda "ders yalnız adıyla sayar" diye geçiştirildi (2026-10-30)
- **Kural:** AGENTS 28 — geçmiş yıl öğrenci önem notu (`src/data/ogrenci_onem/`, `docs/OGRENCI_ONEM/<ders>.md`) her 2026-27 dersinde zorunlu
  malzemedir: A birimi anlatımda ayrıntılı (tanım → ayırt edici nokta → sayı/ölçüt → komşu kavram), önem listesinde `ogrenci` etiketli
  madde, ≥2 örnek soru; B birimi anlatımda açık + ≥1 soru. Slaytta yalnız adı geçen kavram, notta/çıkmışta tanımı soruluyorsa tanımıyla anlatılır.
- **Önleme:** "ders yalnız adını verir / yalnız adlarıyla sayar" türü geçiştirme, kavram öğrenci notunda ya da çıkmışta tanımıyla geçiyorsa yasaktır.
- **Kapı:** `python3 scripts/ogrenci_onem/kapi.py <ders>` 0 HATA — bilgi düzeyinde (el notu, vurgulu satır, çıkmış önermesi) anlatım ve önem
  listesi cümlelerinde arar (vektör + kelime kökü örtüşmesi; yalnız vektör "spastisite ve rijidite" cümlesini rijidite tanımı sanıyordu).
