# Aşama kuralları — anlatim

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/tam_hat/kural_secici.py`. 51 madde. Ayrıntı gerekirse madde başlığıyla defterde aç.

### H2 — Türkçeye uymayan ifade ve iç etiketler (2026-10-18)
- **Kurul 2'de doğrusu:** Doğal, eksiksiz, anlaşılır Türkçe; çeviri mecaz ve iç etiket yok; tam cümle.
  Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.
- **Kapı:** `meds/scripts/turkce_uslup.py` (liste her kalıbı yakalamaz; denetçi metni sesli okunuyormuş gibi okur).


### Kurul 2 hattı için genel kural
- Her içerik türünde yazar + bağımsız denetçi geçişi; doğrulayıcı 0 HATA vermeden EMA seslendirmesine ve yayına geçilmez.
- Bu defterdeki her maddenin kapısı Kurul 2 hattının doğrulayıcılarına bağlıdır (2026-10-18):
  - Sınav asistanı, sesli çözücü, spot önem listesi doğrulayıcıları: her zaman HATA.
  - Öğren: `validate_learning_decks.py deck.json --oyun-zorunlu --kurul2`; sınav spotları: `sinav_spotlari/dogrula.py --kurul2`.
  - **Kurul 2 başlarken ders işçisinin denetimine (`meds/scripts/ders_isci/denetle.py`, Öğren çağrısı) `--kurul2` eklenmeli** ve
    işçi talimatına bu defter okutulmalı. Kurul 1 işçisi bayraksız çalıştığı için şimdilik etkilenmez.

### Sesli ders PDF/DOCX dışa aktarımı (2026-10-20)
- **Yazıyla sayı:** konuşma metni okunuş için "iki virgül bir", "yüzde kırkına" yazar; öğrenciye verilen dosyada bunlar
  "2,1", "%40'ına" olmalı. Kural tek yerde: `src/services/sayiYazim.ts` (`sayilariYaz`), dışa aktarım
  (`components/canliDers/canliDersDisaAktar.ts`) ve ekran (`canliDersStore.ts` → `sayilariDuzelt`, vurgu konumları `sayilariYazEslemeli` ile taşınır) her derste uygular. Saklanan metin değiştirilmez (ses ve cümle zamanı ona bağlı).
- **Düz madde yığını yok:** paragraf tek madde olarak basılmaz; ilk cümle ana madde, sonrakiler alt madde, "Yani/Örneğin…"
  ve "2 ölçütü ayırın" gibi duyurulardan sonra gelenler ikinci düzey; kısa noktasız satır alt başlık olur.

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

### H33 — Türkçe harfsiz metin kabul ediliyordu + kabul edilmiş iş yeni kapıdan geçirilmiyordu (2026-10-23 K2 provası)
- Gemini Flash-Lite bazı çözücü partilerini ve bir sesli bölümü baştan sona harfsiz yazdı ("dogum", "bagli", "oykusu");
  hiçbir kapı yakalamadı, partiler KABUL edildi (önceki e07 çözücü ve k1-64 sesli sınamalarında da vardı; yalnız geçici kopya).
- Ortak kapı `cekirdek.turkce_katlama`: sözlük paketin kendi girdisinden; girdide Türkçe harfle geçen kelimenin katlanmış
  biçimi ≥3 kelimelik bir alanda ≥2 kez varsa HATA (İngilizce alıntı, kimlik/tür alanı, büyük harfli OCR yanlış alarm vermez).
- Kabul edilmiş iş yeniden kullanılırken `yonlendir.kapi` ile güncel kapılardan geçirilir; geçemezse "yeniden" koşar.
- Betik onarımı `cekirdek.ses_onar` (SES_ONAR görevleri): ses alanlarında kısaltma/Roma rakamı `modul_okunus.donustur`
  ile ("MSH" → "mee see haa"); modelin üç turda düzeltemediği "büyük harfli kısaltma" hatası kalktı.
- Öncüllü soruda "kökle uzunluk uyumsuz" hatasına düzeltme ipucu eklendi (kok_ses öncüllerin hepsini okur).

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

### H42 — Okun başlangıcı belirsizdi; resimdeki bölge vurgulanmıyordu (2026-10-24, genel kural)
- Kullanıcı: "okların başlangıç noktası belirsiz", "resimlerde marker ile boyama yapılıp hatlar belirginleştirilebilir";
  "bu derse özgü değil, genel kural". Düzeltme: her okun kaynağı çerçevelenir (kutu yoksa halkalı turuncu nokta); `kontur`
  yarı saydam sarı fosforlu dolgu + kırmızı hatla çizilir. Genel kurallar listesi: `scripts/cizim/TALIMAT_CIZIM.md`.

### H51 — Resim slaytında anlatım görselin yerine panelde; yatay zincirde kutular kırılıyordu; testler bunları görmüyordu (2026-10-24)
- Herniasyon şeması anlatılırken altta 5 öğeli yatay zincir paneli; kutular 3–4 satıra kırılıp panel sayfadan 333–692 px
  taşıyordu. Maske paneli "Görünen: Alkol" anlamsızdı. Grup panelinde numaralar basılmıyor, ok sözü kesiliyordu.
- Kök: sınama yalnız panel kutusunun taşmasını ölçüyordu (iç taşma, satır kırılması, kesik söz yoktu) ve elle yapılıyordu.
- Düzeltme: `resim_sayfasi` kapısı (görsel slaytta panel yok; 7 sayfa Claude ile görselin üstünde yeniden çizildi), yatay zincir
  tek satır yoksa dikey, maske "İlk izlenim / ⚠ maskeleyebilir / Atlanmaması gereken", liste numaraları, grup ızgarası.
  Kalıcı otomatik kapı `scripts/cizim/panel_sinama.mjs` (366/567/1100 px, 8 hata türü) ders zincirinde; düşen çizim yayına gitmez.

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

### H65 — Tablo sayfasında tabloyu anlatmayan cümleye şekil/tablo çapası (2026-10-26, k2-23 cinsel kimlik)
- **Çözüm / kural:** Şekil/tablo çapası yalnız görseli/satırı gerçekten anlatan cümleye yazılır; paragrafın sonraki cümlelerine kopyalanmaz. Tablo çapalı cümlede `satir` boşsa çapa yazılmaz. Düzeltme: o cümlenin `sekil`'i `null` yapıldı, `tablo` kaldırıldı (capa + v2 + taslak kopyaları, `sekil_cizim.py sus` ile aynı yöntem); kapı gevşetilmedi, yayın 0 HATA ile tamamlandı.


### H70 — Mekanik 2 Cümlelik Şablon ve Yüzeysel Anlatım Yasağı (Sıfır Bilgi Kaybı ve Amfi Derinliği Standardı) (2026-10-26, k2-48 lokal anestezikler)
- **Çözüm / kural:** Sayfa başına yüzeysel 2 cümlelik kopyala-yapıştır şablonlar KESİNLİKLE YASAKTIR. Her slayt için amfi ders notundaki tüm maddeleri, tabloları, spesifik ilaç isimlerini, maksimum dozları ve patofizyolojik mekanizmaları kapsayan 3 ila 6 zengin cümle yazılmalıdır (35–70 slaytlık dersler için 140–250+ cümle, ~2000–3500 kelime, 15–25 dakika anlatım derinliği). K48 bu standartla baştan üretildi (144 cümle, 2438 kelime, 68 atomik bilgi, 10/10 çizim, 6.23 MB .medspak) ve 0 HATA ile Oracle canlı ortamına alındı.



### H72 — Çok sözcüklü terimin kısa son sözcüğü ek aldığında eşleşmiyordu (2026-10-26, k2-07 genel anestezik ilaçlar)
- **Çözüm / kural:** `ek_mi(..., kisa_izin=True)` yalnız **çok sözcüklü** terimin **son** sözcüğünde ve terim en az 8 karakterken kullanılır; tek sözcüklü kısa terimlerde (kısaltmalar) davranış değişmedi. Eşleşme gevşetilmedi, yalnız Türkçe ek kuralı bağlamla birlikte uygulandı.


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


### H86 — Ders işçisi denetimi örnek soru şık açıklamalarını standart kapıdan geçirmiyordu (2026-10-27, k2-03)
- **Çözüm:** `denetle.py` Kurul 2+ dersinde her şık açıklamasını `sik_aciklama.denetle` + `turkce_uslup.denetle` ile HATA verir.
  k2-03'ün 110 şık açıklaması yeniden yazıldı; q18 çeldiricileri dersin kendi kavramlarıyla değiştirildi.
- **Önleme kuralı:** örnek soru çeldiricisi de müfredattan (öğretilmiş komşu kavram) seçilir (AGENTS kural 4, 9).


### H89 — Slayttaki yapışık madde imi glifi (U+F06E) kısaltmayı ve kanıt eşlemesini bozdu (2026-10-27, k2-02/k2-03)
- **Çözüm / kural:** `kisaltma_sozlugu.adaylar` ve `degerlendirme_dogrula.norm` U+F000–F8FF ve madde imi işaretlerini ayırıcı/boşluk
  sayar. Yeni metin işleyen her betik slayt metnini bu karakterlerden arındırarak karşılaştırır.


### H87 — v15 katmanlarında tanımsız renk/yazı değişkenleri: saydam kartlar, varsayılan yazı tipi (2026-10-27)
- **Çözüm:** `styles/v15/tokens.css`'e takma adlar (gerçek jetonlara bağlı).
- **Önleme kuralı:** yeni CSS'te renk/yazı değişkeni yazmadan önce `getComputedStyle(document.documentElement)` ile ya da
  palettes.ts/tokens.css'te var olduğu doğrulanır; yeni ad uydurulmaz.


### H92 — Bilinen kısaltma sözlüğü bağlamsız: MSS "Muskuloskeletal sistem" diye açıldı (2026-10-27, k2-03/k2-04)
- **Çözüm:** derse özel `data/sesli_anlatim/kisaltma_elle/<key>.json` (`MSS: Merkezi sinir sistemi`), elle eşleme bilinenden önce gelir.
- **Önleme kuralı:** her derste kısaltma listesi (kısaltma = açılım) yazdırılıp slayt metniyle okunur; branşa göre anlamı değişen
  kısaltma (MSS, KB, BOS …) için derse özel eşleme yazılır, genel sözlüğe yeni anlam eklenmez.


### H95 — Yayın düzeltmesinde olmayan alan; PDF eşleyici durdurulan işçi kapsayıcısında (2026-10-27, k2-03/k2-04)
- **Çözüm:** `y.b.get("ders_id")`; PDF eşleme tek seferlik `docker run --rm -u 1001:1001 --entrypoint python3 medsoru-isci:latest`
  (aynı bağlar, LLM anahtarı yok) ile; deste PDF'i 200 doğrulandı.
- **Önleme kuralı:** yayın betiği değişikliği Oracle'a gitmeden önce yerel taslakla `kaynak_kimligi_esnek` ve `--deneme` akışı
  çalıştırılır; yayından sonra `/api/lecture-pdf/deck/<deck>/0` 200 kontrolü zorunlu.


### v15 tam ekranda yan menü içeriğin üstüne biniyor (2026-10-27)
- **Kural:** Yeni kabuk (v13, v15…) eklenince `html.is-app-fullscreen` için o kabuğun yan menü/üst bar sınıfları da gizlenir ve `--sh-side-w` sıfırlanır (`styles/v15/shell.css` sonu).

### H100 — Koyu temada "beyaz" yazılar kayboluyordu; spinner/iskelet renkleri temaya uymuyordu (2026-10-27)
- **Çözüm:** `index.css`: `.text-white` → `var(--color-on-solid)` (katmansız kural utilities katmanını ezer), `.bg-ink-surface .text-white` → `--color-canvas`, koyu perde için `.on-perde`; iskelet `color-mix(accent)`; tanımsız değişkenler gerçek tokenlara bağlandı. Tam döküm `docs/V15_TEMA_DENETIMI.md`.
- **Kural:** Yazı rengi için `text-white` değil `text-on-accent`/`text-on-solid`; yeni CSS değişkeni yalnız `palettes.ts` TOKEN_KEYS ya da v15 tokens.css içindekilerden; sabit renk yalnız bilinçli süs (çerçeve, kâğıt üstü çizim) için.


### H103 · Çıkmış adayı farklı dönem/ders sınavından geliyor; ham anahtar bankadaki cevapla çelişiyor; bankada olmayan çıkmışlar (2026-10-27, k2-05 Nörolojik Muayene)
- **Kural:** Çıkmış eşlemesi yalnız (a) ham belgenin DÖNEMİ ve DERSİ bu ders olan, (b) basılı anahtarı banka cevabıyla uyuşan, (c) slayt kanıtı birebir olan sorularla yapılır. Ham belgede olup bankada olmayan soru eşlenmez, `cikmis_taslak.json › bankada_yok_ham_belgede_var` listesine yazılıp bankaya ekleme kararı ana oturuma bırakılır. `-rNN` kayıt ham belgede doğrulansa bile karar ana oturumundur.


### H108 · Kısaltma kapısı slayttaki gen sembollerini ve slayt yazım hatalarını (LMXIB, WTI) Faz A'da HATA sayıyor (2026-10-27, k2-08)
- **Çözüm:** 17 anahtar yalnız bu ders için eklendi (açılım standart, slayttaki yazım hatası belirtilerek).
- **Kural:** Genetik derslerde Faz A'da slayttaki gen sembolleri + kısaltmalar sözlüğe önce eklenir; yazım hatalı sembol (LMXIB/WTI) aynen ayrı anahtar olur ve açılımında doğru gen belirtilir.


### H110 · Kısaltma kapısı `kisaltma_elle`deki OD/OR/ID/SED'i "kısaltma biçiminde değil" diye reddetti (2026-10-27, k2-08 Tıbbi Genetik)
- **Çözüm:** `ELLE_AKTIF` (işlenen dersin elle anahtarları) `kisaltma_mi`de kabul edilir; `k_adaylar/k_otomatik/k_dogrula` başında doldurulur. Çok anlamlı kısaltma (CVS: kardiyovasküler sistem s.49 / koryonik villus örneklemesi s.70) genel sözlüğe konmaz, sayfa bazlı yazar dosyasıyla verilir.
- **Kural:** branşa özgü, Türkçe sözcüğe benzeyen kısaltma (OD, OR, ID, SED) dersin `kisaltma_elle` dosyasına yazılır; genel `kisaltma_bilinen.json`a eklenmez.


### H112 · İlk anlatım taslağı öğrenci denetçide KALDI: aynı sözcük iki anlamda, kilit kavram tanımsız, gen sembolü okunuşu çözülemedi (2026-10-27, k2-08)
- **Çözüm:** kollajen için "birinci/üçüncü tür", hastalık için "birinci tip" kullanıldı; okuma çerçevesi ve distrofin işlevi kısaca tanımlandı; somit türevleri, kraniyoraşizis tanımı düzeltildi; W harfi "duble ve" okunur; yalnız yeni bilgi (ayırt edici vurgu, klinik örnek, tedavi) taşıyan hoca atıfları kaldı. Tur 2 GEÇER (%90 yanıtlanabilirlik).
- **Kural:** sesle okunan metinde aynı sözcük iki ayrı kavramı gösteriyorsa yazım ayrıştırılır; sayısal/ekzon gibi kavram ancak tanımından sonra kullanılır; "hoca da ... söyledi" yalnız slaytın vermediği ek bilgi ya da sınav vurgusu içerdiğinde yazılır.


### H105 · Sıralı tabloda adım atlanıyordu (k2-05, 2026-10-27)
- **Çözüm:** 3. satır (Motor sistem) parça, taslak deste ve `interactive_learning_decks.json`'a eklendi; ders içerik paketi yeniden yazıldı.
- **Kural:** Sıra/Adım sütunlu tablolarda numaralar 1'den kesintisiz olmalı ve slayt metnindeki sayımla eşleşmeli (`docs/DERS_ICERIK_BICIMI.md`). Kapı: `scripts/ders_icerik/sira_kapisi.py`.


### H118 · Anlamsız karşılaştırma tabloları (Öge / Sınıf / Gerekçe) (2026-10-27)
- **Çözüm:** swipe_matching tablo dışı bırakıldı; venn/feature_bidding yalnız ≥3 satır, her gerekçe ≥7 kelime ve benzersizse alınır.
- **Kural:** Karşılaştırma yalnız iki GERÇEK tıbbi kavramı (hastalık, yapı, ilaç, mekanizma) ayırt eder; "X mi Y başlığı mı" gibi meta sınıflama, tek cümlelik özdeş gerekçe, bozuk Türkçe yasak. Yazar parçalarında da yazılmaz; yazar/denetçi bunu kontrol eder.
- PDF/yazdırma: belge yalıtılmış iframe'de yazdırılır; uygulama DOM'unda yazdırma ve sayfa yüksekliğine eşit sabit yükseklik YASAK (boş sayfa/renk karışması).


### H120 · Dallanmalı soruda doğru/yanlış bayrağı ters işaretliydi (2026-10-27, k2-01)
- **Kalıcı çözüm:** doğrulayıcıya `klinik-karar-bayrak` HATA kapısı (geri bildirim "Doğru/Yanlış" ile başlıyor ve bayrakla çelişiyorsa). Önleme: bayrak ve geri bildirim tek yerden üretilir; denetçi kapı dışı tutarlılık taraması yapar; doğru şık hep ilk sırada olmaz.


### H123 · Tam içerik hattı ders başına 4–6 saat sürüyor, soru/metin/PDF hataları geri dönüş yaratıyordu (2026-10-28)
- **Kural:** `docs/TAM_HAT_HIZLI_AKIS.md` — E0 `hazirlik.py` (döküm GPU ≤2500 MHz, AGENTS §10 altıncı istisna); alt ajana yalnız
  `kural_secici.py --oku <aşama>`; yalnız hatalı parça yeniden yazılır (sayısal hedefte ±%10, kalite hatasında tolerans yok);
  ders başına tek denetçi.
- **Kapı — EKLENDİ:** `scripts/tam_hat/soru_uslup.py` (ders çağrıştıran kök, ipuçlu uzun doğru şık, kazanım bağı, kalıp payı),
  `kaynak_kapisi.py` (kayıt içeriği `s` sayfasında mı), `pdf_tarama.py` (boş sayfa, taşma, üst üste, harf harf kırılma).


### H125 · Ders içerik terimlerinde genel sözlükten bağlam dışı tanım, kopya terim, ipuçlu soru şıkkı (2026-10-28, k2-08)
- **Kural:** Terim tanımı dersin sayfasındaki bağlamla yazılır (genel sözlük yalnız yardımcıdır, ilk anlamı kopyalanmaz); kaynakta
  olmayan sayı/eşik yazılmaz. Terim eklemeden önce ad + `e` eşanlamları normalleştirilip kopya aranır; slayttaki yazım farkı
  (Gl13, FLBN, speksifikasyon) `e`'ye girer. Şekilden okunan kayıt `gorsel: true`. Doğru şık çeldiricilerle benzer uzunlukta yazılır.
- **Kapı — EKLENDİ:** `scripts/tam_hat/kaynak_kapisi.py` (terim adı sayfada mı → HATA; tanım az örtüşüyorsa UYARI, denetçi bağlamı okur),
  `soru_uslup.py` (≥6 kelimelik doğru şık en uzun ve 1,8× → HATA), `hazirlik.py` madde imi temizliği.


### H126 · Sesli ders ekranında gen sembolleri okunuşla görünüyordu: "hoks, o te iks, me se iks, paks 6" (2026-10-28, k2-08)
- **Çözüm:** `yazim_sozlugu.py` artık her v2 dersinin `ses` ↔ `ekran` cümle çiftlerini hizalayıp okunuş → yazım eşlemesini kendisi çıkarır ("hoks" → HOX, "paks altı" → PAX6, "ce o le bir a bir" → COL1A1); Türkçe sözcük, Roma rakamı ve rakamsız okunuşa rakamlı yazım eşlemeleri elenir.
- **Kural:** Kullanıcıya gösterilen metin daima yazımla (HOX, OTX, PAX6), EMA'ya giden metin okunuşla olur. Tam içerik hattında her yeni v2 metni yazılınca `python3 scripts/sesli_anlatim/yazim_sozlugu.py` yeniden çalıştırılır ve ekran metni okunuş artığı için gözle denetlenir; `ekran` alanı her cümlede doldurulur (sembol içeren cümlede boş bırakılmaz).


### H128 · EMA yabancı terimleri yanlış okuyor; anlatım konu geçişini söylemiyor; panel geç, zoom kısa anlatımda, çizim tek renk (2026-10-28)
- **Kalıcı çözüm:** `scripts/sesli_anlatim/terim_okunus.py` + `data/sesli_anlatim/okunus/terim_okunus.json` (eponim, Latince,
  İngilizce, ticari ad + Latince kural motoru) EMA'ya giden Kurul 2+/modül metnine uygulanır (`ema_isci.paragraf_seslendir`);
  `ses_temizle` (DC, RMS eşitleme, yumuşak tepe sınırı, 12 ms geçiş). `docs/ANLATIM_KURGU_STANDARDI.md` (plan → metin,
  ±%20 sayısal tolerans). `CizimLayer.tsx` panel cümle başından, zoom ≥55 karakter; `cizim_uret.py` ZOOM_EN_AZ=70, `renk_ata`,
  `renk/boya/resim` alanları; `cizim_dogrula.py` renk/resim kutusu denetimi.
- **Kural:** yeni ders seslendirmesinden önce `terim_okunus.py --denetle <anahtar>`; yanlış `KURAL` satırı sözlüğe eklenir.
  Anlatım yazarı önce `anlatim_plani.md` kurar; başlıksız konu geçişinde "burada konu değişiyor" cümlesi zorunlu.
  Çizimde birden çok resim varsa `resim: "R#"`, ayrı yapılar ayrı renk, hattı belirsiz bölge `boya: true`.


### H111g · İzleme hızı kaydırıcısı: dokunma hedefleri 10–19 px, boş durumda imleç metinle çelişiyordu (2026-10-28, Sınav planı/Bitirdiklerim)
- **Çözüm:** boş durumda imleç 1×; ray `padding: 9px 0` + `background-clip: content-box` (görünüş aynı, 28 px dokunma), duraklara `::before` ile 40 px dikey alan + `min-width: 40px`. Bugün akışındaki "Tümü" bağlantısı (14 px) negatif kenar boşluklu 40 px alana alındı (`today.css .t15-more`). Takvim, kronometre ve tam ekran ayarlarındaki `kre-tgl` anahtarlarına `aria-label` eklendi (adsız düğme).
- **Kural:** Görünür öğe küçük olabilir ama dokunma alanı ≥40 px (dolgu/`::before`); yer tutucu değer ile açıklama metni aynı varsayımı göstermeli; her `role="switch"` düğmesinin erişilebilir adı olur (label içi olmak yetmez).


### H111p · Sesli derste hatalı adreste sunucu hata kodu ham gösteriliyordu (2026-10-28, Ders çalış)
- **Çözüm:** "geçersiz ders / bulunamadı / 400 / 404" öğrenciye "Bu adreste bir sesli ders yok. Bağlantı eski ya da hatalı olabilir; listeden dersi seçebilirsin." olarak çevrilir; liste düğmesi kalır.
- **Kural:** Sunucu hata kodu (`error` alanı) öğrenci metni değildir; ekranda bilinen hatalar Türkçe açıklamaya çevrilir, bilinmeyen hata için genel cümle kullanılır.


### H111t · Ders çalış dokunma hedefleri: "Tüm dersler" 75×14, Öğren "▶ Dinle" 52×20 px (2026-10-28, Ders çalış)
- **Çözüm:** `dersler.css .d15-more` 40 px dolgu + negatif kenar (H111g ile aynı desen); `LessonPlayer.tsx` düğmeye `ls-dinle` sınıfı, `v12/lesson.css` dokunmatikte `::before` ile 40 px alan.
- **Kural:** H111g kuralı: görünür öğe küçük kalabilir, dokunma alanı ≥40 px.


### H111v · Ana CSS 936 KB, tam katman sayaçsız, tam ekranda fazla yükseklik, kısa başlık, küçük yazı, çevrimdışı boş istekler (2026-10-28, kabuk/başarım)
- **Çözüm:** (1) `src/styles/ogren-ders.css` (index.css'in iki `ls-*` bölümü) yalnız ls-* çizen 13 bileşenden içe aktarılır; ana CSS 936,8 → 865,7 KB (151,2 → 139,9 KB gzip); hesaplanmış stil dökümü önce/sonra (375/1440, deste + 3 ders adımı) 0 fark. `html.ui-v3` ls katmanı, health/v12 ezmeleri yüksek özgüllükte olduğundan ana CSS'te kaldı. (2) `src/utils/tamKatman.ts` (`useTamKatman`, referans sayaçlı); beş bileşen ona geçti. (3) v15 tam ekranda (`:not(.cd-ders-acik)`) `--sh-top-h` ve `--sh-top-vis` = 44 px + güvenli alan; `.sh-main` artık tam görünüm yüksekliği. (4) Telefonda `.v15-top-h` iki satıra sarar (17 px, line-clamp 2); sesli derste Tam ekran düğmesi telefonda gizli (Görünüm çekmecesinde var); `v15-crumb::before` ile ≥40 px dokunma alanı. (5) `--v15-t-caption` 13 → 13,5 px; v15 stillerinde 95 font değeri (10–12 px, <.78rem) 12,5 px'e çekildi. (6) `net.ts` `cevrimdisiMi()` + fetch koruyucusunda arka plan uçları (`presence`, `user-data/backup`, `music/playlist`) çevrimdışıyken ağa çıkmadan reddedilir; `presence.ts` ve `UpdatePrompt` `/api/surum` denetimi çevrimdışıyken atlanır (bağlantı yoklaması `baglanti.ts`/probe `/api/surum`'u kullanmaya devam eder).
- **Kural:** Sayfaya özgü büyük stil bloğu `index.css`/`main.tsx`'e eklenmez, kullanan bileşenden içe aktarılır (sıra/özgüllük hesaplanmış stil dökümüyle doğrulanır). Kök sınıfı birden çok bileşen açıyorsa sayaçlı yardımcıdan geçer. Tam ekranda gizlenen çubuğun yerine dolgu konuyorsa ilgili yükseklik değişkeni de o dolguyu yansıtır. v15'te metin ≥12,5 px; istisnalar yalnız rozet/sayaç/kbd/kronometre mini saati/yazdırma belgesi (`dersPdf.css`)/ray etiketi. Arka plan eşitleme ucu ekleyen `net.ts` `BG_RE`'ye ekler.


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

### H133 — Kaynağı doğrulanamayan sorular gizlenerek kaybedilmişti; "Çıkmış–Örnek" sınıfı (2026-10-28)
- **Çözüm:** 4 bağımsız denetçi 104 soruyu müfredat + ders notu + tekrar taramasıyla değerlendirdi: 72 `cikmis_ornek` (hem Çıkmışlar'da hem `k2-cikmis-ornek` Örnek sorular dersinde, öğrenciye "çıkmış olduğu doğrulanmadı" rozetiyle; sesli ders çıkmış chip'inden hariç), 15 serbest çıkmış, 9 tekrar arşivi, 7 karantinada (`siniflama` alanıyla gerekçeli). 5 soru ders notuna göre düzeltildi (`duzeltmeOnceki` saklı).
- **Önleme:** Kaynağı doğrulanamayan ama doğru soru gizlenmez, `kaynakSinifi=cikmis_ornek` ile etiketlenip öğrenciye belirtilir; çıkmış vurgusu yalnız doğrulanmış kaynağa dayanır.


### H170–H185 — Sayfa denetimi dördüncü tur, yönetim paneli orta bulguları (2026-10-28)
- **H170 Kurul çipi "1 66":** etiket yalın rakam + aynı boyutta sayı → "Kurul N" + soluk sayı rozeti.
- **H171 Yüklenirken "0 kayıt":** sayaç yükleme durumuna bakmıyordu → "Yükleniyor…", seçeneksiz süzgeç satırı gizli.
- **H172 Açıklamalarda dosya yolu/jargon:** yönetici diline çevrildi; yol küçük ikincil etiket.
- **H173 Son yönetici işlemleri:** okuma kayıtlarıyla doluyordu → yalnız yazma (`sonDenetimler(8, true)` + istemci süzgeci).
- **H174 Bellek "1462 / 234 MB":** RSS ve yığın etiketsiz yan yanaydı → ayrı satırlar, `yiginToplamMb` eklendi.
- **H175 Gelen kartları:** sıfır kartlar gizli, hepsi sıfırsa "Bekleyen iş yok".
- **H176** Çıkmış "Cevap" başlığı 56→72 px. **H177** Birleşenler "Ayır" yazılı onay + Geri al. **H178** Taslaklar kendi çekmecesini açar, dönüşte süzgeç korunur.
- **H179 Askı gerekçesi `window.prompt`:** kit onay penceresine gerekçe alanı (`gerekceIste`, ≥3 karakter); Kişi 360, Erişim, Kişiler.
- **H180** Oyun odası "Kapat" satır çekmecesinde. **H181** Erişim, DB satır yazımı, duyuru onaylarında hedef sunucu (`yazimHedefi()`); duyuru yayınlama artık onaylı.
- **H182 Betik tehlikesi:** ad regex'i yerine izin listesi: yalnız bilinen salt okunur betikler onaysız, gerisi yazılı onay.
- **H183 Yedek içe aktarma:** ezmeden önce `/api/admin/db/export` ile mevcut havuz indirilir, başarısızsa iptal (kalıcı çözüm: sunucu import ucu kendi yedeğini almalı — açık).
- **H184 Çöp kutusu:** tek seçenekli "Tür" süzgeci gizleniyordu → gösterilir; Silinme süzgeci (bugün/7/30 gün/eski).
- **H185 Site › Menü:** erişimi kapalı sayfada anahtar kilitli + açıklamalı; menüden gizleme onaylı, her yazım Geri al.

### H250–H268 — Sayfa denetimi beşinci tur, yönetim paneli kalan bulgular (2026-10-28)
- Genel bakış kart adları ve hedefleri (topluluk şikâyeti, istemci hatası → Gelen süzgeci), yük renk eşiği, sürüm etiketi (H250–H253).
- Bağlantılar: Ctrl/orta tık yeni sekme (H254), `manageAdres` (H255), Çıkmış ve Birleşenler içi bağlantılar panel içi gezinme (H256, H266), Branşlar → derslere (H265).
- Metin/ad netliği: Ham defter dışa aktarım (H257), Faz 14 → "Çıkmış inceleme (Faz 14)" (H259), Kamplar → "Kamp tüyoları" (H260), benzer menü adları ayrıştırıldı (H261), Sözlük silinemez sekme açıklaması (H267), katalog form alanlarına Türkçe etiket (H268).
- Onaylarda hedef sunucu: bakım ve LLM işleri (H262, H263; kural 20 davranışı değişmedi). Faz 14'te kimliksiz satır bildirimi (H258).
- **H264 Boş tablo:** yalnız "Kayıt yok" diyordu → süzgeç mi kaynak mı boş söylenir, yerelde Canlı önerisi.
- Kapsam dışı bırakılan öneriler: menünün baştan düzenlenmesi, görünürlüğün tek yerde toplanması, Çıkmış/şikâyet toplu işlemleri, kirli kurul etiketlerinin veri temizliği, üç "bugün" sayfasının birleşmesi, oynatıcı araç çubuğu yeniden tasarımı, çıkmış listesinde sayfalama.

### H310–H314 (yönetim) — 69 sayfalık menüde bulunabilirlik (2026-10-28, sayfa denetimi)
- **Çözüm:** Sabitlenenler (`m16_sabit`), Son kullanılanlar (`m16_son`, 5), ilk açılışta yalnız Genel + etkin grup açık (`m16_kapali_grup` yoksa), menüde ara (etiket + `anahtar`, Türkçe harf duyarsız, Esc temizler), telefonda ≥32 px hedefler. Menü yapısı ve adresler değişmedi.


### H431 — Odak ekranlarında durum çubuğu ve ana ekran çizgisi payı yoktu (2026-10-28, kullanıcı bildirdi: iPhone)
- **Çözüm:** Kök sınıf `v15-odak` (ShellV15) + `.sh-main` üst dolgusu `env(safe-area-inset-top) + 4px`; `.cd-dock` alt dolgusu her kırılımda `+ env(safe-area-inset-bottom)`. Chrome'da `Emulation.setSafeAreaInsetsOverride` (üst 47 / alt 34) ile ölçüldü: başlık 51 px'te, oynatıcı tabandan 40 px yukarıda. **Gerçek iPhone'da sınanmadı**; kullanıcının gördüğü çakışma başka bir ekransa ayrıca bakılacak.
- **Kural:** Kendi üst/alt çubuğunu çizen her ekran güvenli alan payını kendisi alır; medya sorgusunda dolgu yeniden yazılırken `env(safe-area-inset-*)` korunur.


### H434 — Sesli derste "bu hastalıkta" gibi adsız göndermeler hangi hastalığın kastedildiğini karıştırıyordu (2026-10-28, kullanıcı bildirdi)
- **Çözüm/kural:** Her yeni paragraf/bölüm hastalığı veya kavramı adıyla anar; adsız gönderme (bu hastalıkta/durumda/tümörde, burada, bunlarda…) parça başında yasak. `metin_denetle.py` BAGLAMSIZ kapısı HATA verir; KURUL2_DERS_STANDARDI §8.13 ve ANLATIM_KURGU_STANDARDI'na yazıldı. Denetçi her paragrafı tek başına okuyup konuyu çıkarabilmeli.


### H435 — Örnek sorular hocanın yeni sınav kalıbını yansıtmıyordu (2026-10-29, kullanıcı bildirdi)
- **Kural / Önleme:** Patoloji örnek soru ve önem noktası `docs/PATOLOJI_HOCA_SORU_MANTIGI.md` + `scripts/patoloji_soru_isci/` kapısına göre yazılır: her önem noktasına ≥2 farklı kalıpta soru, çeldirici yalnız aynı dersin komşu kavramları, doğru şık en uzun olmaz. Sarı dolgu ve başlık önem sinyali sayılmaz; kırmızı tek başına "önemli" değildir (slaytların ~%42'si kırmızı).
- **Kapı:** `python3 scripts/patoloji_soru_isci/dogrula.py sorular.json paket.json` → 0 HATA.


### H436 — Ara soru şık açıklamalarında ileriye sızıntı ve kaynakta olmayan iddia (2026-10-29, bağımsız denetçi buldu)
- **Kural / önleme:** Şık açıklaması, ipucu ve çözüm de yalnız `ara.sayfa` ve öncesindeki slaytların bilgisini kullanır; tıbbi tanım slayt metninde yoksa yazılmaz. Bağımsız denetçi (TALIMAT adım 7) her soruda bunu slayt slayt arar; düzeltilen sorular ikinci kez denetlenir. Ders akış metni (Whisper dökümünden beslenmiş olabilir) tıbbi kaynak değildir; terim/sayı yalnız PDF sayfa metninden alınır.


### H438 — Anlatım slaytın söylediğini tersine çevirdi (k2-01, 2026-10-29)
- **Çözüm/önleme:** cümle slayt ifadesine döndürüldü ("tanının doğru olduğunu göstermek için çekilir"), açıklama sonraki cümlede ("başka yapısal nedeni dışlamak"). Anlatım slayttaki hükmü yorumlayabilir ama **yönünü tersine çeviremez**; denetçi her sayfada slayt cümlesi ↔ anlatım cümlesi olumsuzluk kıyası yapar. Değişen cümlenin EMA klibi yeniden üretilmelidir.


### H446 — Öğrencinin en çok çalıştığı ve çıkmışta sorulan bilgi anlatımda "ders yalnız adıyla sayar" diye geçiştirildi (2026-10-30)
- **Kural:** AGENTS 28 — geçmiş yıl öğrenci önem notu (`src/data/ogrenci_onem/`, `docs/OGRENCI_ONEM/<ders>.md`) her 2026-27 dersinde zorunlu
  malzemedir: A birimi anlatımda ayrıntılı (tanım → ayırt edici nokta → sayı/ölçüt → komşu kavram), önem listesinde `ogrenci` etiketli
  madde, ≥2 örnek soru; B birimi anlatımda açık + ≥1 soru. Slaytta yalnız adı geçen kavram, notta/çıkmışta tanımı soruluyorsa tanımıyla anlatılır.
- **Önleme:** "ders yalnız adını verir / yalnız adlarıyla sayar" türü geçiştirme, kavram öğrenci notunda ya da çıkmışta tanımıyla geçiyorsa yasaktır.
- **Kapı:** `python3 scripts/ogrenci_onem/kapi.py <ders>` 0 HATA — bilgi düzeyinde (el notu, vurgulu satır, çıkmış önermesi) anlatım ve önem
  listesi cümlelerinde arar (vektör + kelime kökü örtüşmesi; yalnız vektör "spastisite ve rijidite" cümlesini rijidite tanımı sanıyordu).
