# Aşama kuralları — anlatim

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/tam_hat/kural_secici.py`. 66 madde. Ayrıntı gerekirse madde başlığıyla defterde aç.

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

### H458
- **Çözüm:** `src/services/hataDenetci.ts` (Sorun denetçisi): düşen işlem `medsoru:islem-dustu`, eşitleme hatası
  `medsoru:esitleme-hatasi` olayıyla denetçiye gider; denetçi 90 sn'de bir / bağlantı dönünce / sekme öne gelince ağ, takılı kuyruk,
  gönderilmemiş ilerleme, depolama, IDB, SW ve saat sapmasını yoklar, güvenli onarımları (kuyruğu yeniden gönder, eşitlemeyi yeniden
  çalıştır, kalıcı depolama iste, SW'yi yeniden kur) kendisi yapar. Panel `HataDenetciSheet` (bağlantı şeridi "Sorun bulundu",
  v15 menü "Sorunlar", eşitleme kartı düğmesi), HTTP koduna göre sade açıklama + "Yeniden dene" + kopyalanabilir teknik ayrıntı.
- **Önleme:** kullanıcının işlemi hiçbir yerde sessizce silinmez; kuyruktan düşen her şey denetçiye bildirilir. Yeni eşitleme/çevrimdışı
  hatası eklenirken hataDenetci'ye `bildir()` ile sade dilde başlık + açıklama + çözüm yazılır, ham hata yalnız `teknik` alanına.


### H459 — KMB (Üretral kateter): küçük video, tekrar eden altyazı, iptal edilemeyen otomatik geçiş, metin hataları, hata takibi yok (2026-10-31)
- **Çözüm:** Öğren yeniden kuruldu (`KmbAsistan.tsx::Ogret`): üstte adım başlığı + önceki/sonraki + 18 parçalı adım şeridi
  (izlenen yeşil, sınavda eksik kırmızı), tüm adımlar açılır panelde; video + eşzamanlı metin `@container kmb` ile dar
  alanda alt alta, ≥860 px içerikte yan yana (video yapışkan); cümleye dokununca video o cümleden oynar
  (`LottieVideo` `ref.bolumeGit`). Oynatıcı: tek dokunuş oynat/duraklat, kenarda çift dokunuş ±10 sn, önceki/sonraki cümle
  düğmesi ve ↑/↓, hız değişiminde saat yeniden tabanlanır, altyazı/hız `medsoru_kmb_oynatici_v1`'de, bitişte geri sayımlı
  `otoSonraki` (Yeniden izle / Burada kal / konumlama iptal eder), etiketler iki satıra iner. Hata istatistiği
  `kmbHata.ts` + "Eksikler" sekmesi (`Eksikler.tsx`): her deneme kavram anahtarına (OSCE basamağı, vaka, yapı, hedef)
  yazılır, iki kez üst üste doğru yapılana dek zayıf sayılır; öğretim adımına göre gruplanır ("Adımı yeniden çalış"),
  hedefli tekrar (unutulan basamak için "bundan sonra ne yaparsın?", vaka, sahnede bul, hedefi anlat + öz değerlendirme).
  Sınav ögelerine `adim` alanı eklendi (dogrula.py denetler). `medsoru_kmb_*` hesapla eşitlenir (userKvSync).
  İçerik: kayda dayanan 11 cümle/açıklama düzeltmesi, kadın akışına `ilerlet2`, 11 şık açıklaması genişletildi.
- **Önleme:** KMB'de yeni ekran düzeni viewport değil `@container kmb` ile seçilir; otomatik geçiş yalnız oynatıcının
  iptal edilebilir `otoSonraki`'si ile yapılır. Hocanın sözü cümleye çevrilirken derecelendirme ("en önemli", "göreceli",
  "hata ama sorun değil") korunur; anlatımda vurgulanan her uygulama eylemi OSCE akışında ayrı basamaktır. Her yeni sınav
  ögesi `adim` taşır (yoksa dogrula.py HATA). Şık açıklamaları `sik_aciklama.denetle` ile 0 HATA.


### H461 — KMB video oynatıcı: tek dokunuş oynatmayı durduruyor ya da 10 sn sarıyordu (tam ekran dahil) (2026-10-31)
- **Çözüm:** tek jest katmanı (`LottieVideo.tsx` `jestBas/jestKay/jestBit`, pointer olayları): DOKUNMATİK tek dokunuş
  yalnız denetimleri gösterir/gizler (280 ms çift dokunuş beklenir), kenarda çift dokunuş ±10 sn ve 700 ms içinde aynı
  kenara her dokunuş +10 (toplam rozetle), ortada çift dokunuş oynat/duraklat, basılı tutma 2×, yatay kaydırma sarar
  (hedef süre + cümle balonu; dikey kaydırma sayfaya kalır, `touch-action: pan-y`). FARE tık oynat/duraklat, çift tık
  tam ekran. Denetimler her kipte görüntünün üstünde yüzer, oynarken 3 sn sonra gizlenir (ince ilerleme çizgisi kalır);
  ders videosunun üst şeridi aynı duruma bağlı (`onGoster`). Orta sıra: önceki cümle · oynat · sonraki cümle (±10 yok).
  Cümle listesi menüsü, hız menüsü (0,75–2×), cümle parçalı zaman çubuğu + üzerinde süre/cümle önizlemesi, 0–9 tuşları,
  dokunmatikte ilk oynatmada bir kez jest ipucu. Adım videosu bitince altında o adıma bağlı tek soru (`HizliKontrol`);
  yanıtlanana dek geri sayım bekler, cevap Eksikler istatistiğine "Video sonu soruları" olarak yazılır. Sarma otomatik
  geçişi iptal etmez (yalnız "Burada kal"). `.kmb-dv[role=dialog] { max-height: none }`.
- **Önleme:** oynatıcıda görünmez tıklama bölgesi tek dokunuşta oynatma durumunu ya da konumu değiştirmez; konum/oynatma
  değiştiren tek dokunuş yalnız görünür düğmededir ve görünür düğme çift dokunuş bölgesine (kenar %35) taşmaz. Jest
  kuralları başsız Chrome dokunma olaylarıyla sınanır (26 senaryo: tek/çift/üçlü dokunuş, basılı tutma, kaydırma,
  tam ekran, fare). Tam ekran/sabit katmanlar `[role=dialog]` taşıyorsa genel max-height'ı kapatır (H461, hucrem.css örneği).


### H462 — KMB Hedefler filmi: yakınlaştırma ayrıntıyı kesiyordu; 3B deneme (Pixar/organik) kalite eşiğini geçemedi → ARŞİV (2026-11-01)
- **Çözüm:** yakınlaştırma tavanı 1,35 ve odak kutusu + etiket payı kadrajın en çok %70'i (`HedefFilmi` kamera; veri zoom
  1–1,4 kapısı `dogrula.py`). 3B küme (`components/kmb/sahne3b/`, `SahneGoster`) **arşivde**: varsayılan KAPALI
  (`localStorage.medsoru_kmb_3b='1'` ile yalnız geliştirici açar), "3B" düğmesi kaldırıldı, canlıya gönderilmedi.
  Ön yüz 2B (SVG + Lottie) hattında sürer; hedef stil: düz vektör çizgi film (referans: Foley kateter illüstrasyonu —
  pürüzsüz dolgular, temiz kontur, sınırlı palet).
- **Önleme (2B yeniden çizim için KESİN kurallar):** ① hiçbir parça diğerinin içine girmez (katmanlar kesişmez, önde olan
  arkadakini düzgün örter); ② ölçekler anatomiye uyar (16 Fr ≈ 5 mm; üretra ~1 cm; balon 10 mL ≈ 2,7 cm); ③ sıvılar
  (idrar, izotonik, jel, antiseptik) yarı saydam/parlak ve yüzeye yapışık gösterilir, katı halka/boncuk olmaz; ④ bakış
  açısı anatomiye göre seçilir (sagittal kesit yandan, vulva önden litotomi, mesane içi üstten) ve kadraj hiçbir anlatılan
  ögeyi kesmez; ⑤ her öge adıyla ayırt edilir (neyin ne olduğu belirsizse çizim yeniden yapılır); ⑥ önizleme
  gerçek vuruş durumuyla alınır (`sahne3b_onizle.mjs --film`, SVG için de çalışır), "tüm ögeler açık" karesi yalnız
  kimlik denetimi içindir; ⑦ her sahne yayından önce kare temas sayfasıyla göz denetiminden geçer.


### H468 — Hoca dökümü sessizce CPU'ya düştü; turbo dökümü konuşmanın üçte birini kaçırdı (2026-11-02, Kurul 2 2. parti)
- **Çözüm:** saat kilidi kuruldu, döküm GPU'da yeniden alındı (≈2–3 dk/ders); her derse ikinci döküm (Systran medium,
  `hoca_dokum_medium.json`, `meds_temp/ogrenci_ders/dokum_medium.sh`) alındı ve vurgu/anlatım kayıtları iki dökümle çapraz okundu
  (k2-10'da 23 yeni kayıt, 2 yeni sınav vurgusu; anlaşılmayan "her hafta olan ağrı daha önemli" kaydı düşük güvene alındı,
  ona dayanan anlatım cümlesi silindi).
- **Önleme:** E0'dan önce `nvidia-smi --query-gpu=clocks.max.sm` ≤2500 denetlenir; döküm günlüğünde "bu oturum CPU" görülürse
  durdurulur. Hoca vurgusu en az iki dökümle çapraz okunur; yalnız bir dökümde geçen ve slayta bağlanamayan söz vurgu dayanağı olmaz.


### H469 — Kurul 2 EMA yolu büyük harfli kısaltmayı okumuyordu (NMDA, GABA, IP3) (2026-11-02)
- **Çözüm:** bu partinin yazımla yazılmış anahtarları `modul_okunus.MODUL_ANAHTARLAR`'a eklendi; `KELIME`'ye GABA/GABAA/GABAB/AMPA/
  DOPA/VMAT/VGLUT/mGluR/HANDLE/SUNCT/KİBAS; `okunus.FONETIK_TTS`'e GABA/AMPA/L-DOPA; `terim_okunus.json`'a Schneider, Renshaw,
  Wall, Head, Graham, Leao, locus coeruleus, substantia gelatinosa, déjà vu ailesi. EMA işçisi yeniden başlatıldı (modüller
  açılışta yüklenir).
- **Önleme:** Yeni Kurul 2 dersinin metni yazımla tutuluyorsa anahtarı seslendirmeden ÖNCE `MODUL_ANAHTARLAR`'a eklenir ve
  `ema_isci.tts_metni` ile örnek paragraf okunuşu denetlenir; okunuş sözlüğü değişince `meds-ema` yeniden başlatılır.


### H473 — Ders notu sadakati eşiğin altında: "Ek bilgi" etiketleri ve meta cümleler (2026-11-02)
- **Çözüm:** etiketler ve meta cümleler kaldırıldı, anekdotlar kısaltıldı, slayt sözcükleri kullanıldı → 0.855 (eşik gevşetilmedi).
- **Önleme:** Ders notu yalnız slayt bilgisinin redaksiyonudur; hoca açıklamaları sesli anlatımda ve hoca vurguları listesinde yer
  alır. Ders notunda süreç/meta cümlesi ("çıkmışta şu sorulmuştur", "slaytta yazılı değildir") yazılmaz.


### H477 — Asıl hoca derse girmediğinde sınav kaynağı (2026-11-03, Beyin ve Sinir Cerrahisi k2-12/13/14)
- **Kural:** sınavı hazırlayan hocanın slaytı tek kaynaktır (anlatım, soru, önem); derse giren hocanın slaytı/sesi yalnız önem ipucudur,
  metinde "hoca vurguladı" denmez, onun slaytında olup sınav hocasının slaytında olmayan bilgi eklenmez. Kullanıcının bildirdiği geçmiş
  sorudan slaytta karşılığı olmayan (servikal travmada immobilizasyon) anlatıma uydurulmaz, kullanıcıya bildirilir.


### H485
- **Çözüm:** `meds_temp/ogrenci_ders/arac/taslak_kur.py` artık `sayfa_varliklari` üretir; `arac/kanit_onar.py` her başarısız alıntıyı sayfanın
  pymupdf metninde birebir geçen en uzun (≥3 kelime) diziye indirir (bilgi metni değişmez, uydurma yok); taslak + çıkmış eşlemesi onarıldı,
  üç paket 0 HATA.
- **Önleme:** taslak iskeleti yalnız `taslak_kur.py` ile kurulur. Kanıt alıntısı yazan ajan alıntıyı `pymupdf` sayfa metninden alır ya da
  yazım sonunda `kanit_onar.py --yaz` + `degerlendirme_dogrula.py` çalıştırır.


### H486
- **Çözüm:** anlatım düzeltildi + yeniden denetim GEÇER; örnek sorularda 6 ifade düzeltildi; k2-15 önem/çözücü maddesi yeniden yazıldı.
- **Önleme:** anlatım denetiminin `denetim.json` tıbbi bulguları ve `rapor.md` "slayt çelişkisi" listesi her sonraki katman yazarının istemine
  zorunlu girdi olarak konur; ders başına soru katmanı denetçisi (`GOREV_DENETCI_SORU_K2_B3.md`) bu listeyi tek tek arar.


### H487 — `kisaltma_sozlugu.py sozluk_disa` elle eklenmiş kısaltmaları siliyor (2026-11-04)
- **Çözüm:** dosya geri alındı, yalnız kendi derslerin yeni kısaltmaları ve deste bağları birleştirme ile eklendi (4 yeni, 16 bağ).
- **Kural:** `sozluk_disa` sonrası daima kayıt sayısını HEAD ile karşılaştır; düşüş varsa yazma, birleştir. (Betik birleştirme kipine geçirilmeli — açık iş.)


### H488 — Slayt fotoğrafı ters yorumlandı: hipotonik bebek "tonus artışı" diye anlatıldı (k2-16 s.9, 2026-11-05)
- **Çözüm:** cümle, ekran, çapa `sekil`, envanter tanımı düzeltildi; kısmi yeniden yayın (değişen paragraf EMA + cümle/kelime zamanı + çapa/çizim).
- **Kural:** fotoğraf/klinik görünüm anlatan her cümlede yazar ve denetçi sayfa görüntüsüne bakar; görsel yorumu hoca dökümüyle çelişirse hoca + görüntü kazanır, envanter tanımı tek başına dayanak değildir. Denetçi yönergesine "görsel–anlatım yön kontrolü (artış/azalma, sağ/sol, normal/patolojik)" maddesi eklenir.


### H496
- **Çözüm:** `pointer: coarse`'ta dikey dolgu + eksi kenar boşluğu (görünüm aynı, alan 43 px).
- **Önleme:** dokunmatik hedef ≥44 px (tasarım sistemi kuralı); `sayfa_tarama.mjs` `small` listesi her turda süzülür.


### H490 — Öğrenci önem kapısı geçilemez yanlış HATA veriyordu (k2-15, k2-16, k2-11; 2026-11-05)
- **Çözüm (eşik gevşetilmedi):** öncüllü cevap seçilen öncüllerin metnine açılır; bilgi slaytta AÇIKÇA yoksa (sayfa benzerliği < 0,55 VE kök örtüşmesi < 0,4) kapsamdan çıkar ve BİLGİ olarak listelenir; doğrulanmış eşleme dosyası `src/data/ogrenci_onem/esleme/<ders>.json` (`anlatim`: cümle anlatımda birebir + benzerlik ≥ 0,55 ya da anahtar terim cümlede birebir/notta ≥ 0,8; `celiski`: slayt alıntısı sayfada birebir; `slayt_disi`: terimlerin hiçbir sayfada geçmediği denetlenir). Uydurma kayıt HATA verir (sınandı). Gerçek eksik (yaz mevsimi tuzağı, k2-15) anlatıma eklendi.
- **Kural:** kapı HATA'sı "eşleyici kaçırıyor" diye bırakılmaz: ya anlatım düzeltilir ya kapının kendisinin denetlediği kanıtlı eşleme yazılır.


### H491 — Ara soru kodu başka dersin numarasını aldı (2a17 = k2-07; 2026-11-05)
- **Çözüm:** `kimlik()` önce dizinde bu anahtara kayıtlı kodu kullanır; numara başka anahtarla doluysa HARF EKİ verir (2a07b, 2a07c…). 2a17 → 2a07b taşındı (veri, ses, kaynak, Oracle).
- **Kural:** ara soru kodunu elle seçme; `kur.py iskele` atar.

### H492 — Hoca vurgu alıntısı bozuk CPU dökümünden kuruldu (2026-11-05)
- **Çözüm/önleme:** döküm `hoca_dokum_gpu.sh` (realpath) ile yeniden yapıldı, 54 alıntı ±60 sn pencerede dökümle karşılaştırıldı, 4'ü düzeltildi. Kural: `alinti` yalnız dökümde geçen sözdür; slayt bilgisi `konu`'ya yazılır, alıntıya karıştırılmaz.

### H493 — Saat kilidi kalktı, hoca dökümü sessizce CPU'da yapıldı (2026-11-05)
- **Çözüm/önleme:** `hoca_dokum_gpu.sh` başlamadan kilit servisini yeniden uygular. Döküm başlığında `cihaz: cpu` ise A1b'ye geçilmez; döküm GPU'da yeniden alınır (vurgu/alıntı CPU dökümünden kurulmaz).

### H494 — Boş çapa satırı ("‖") çapasız cümleyi çapalı gösterdi (2026-11-05)
- **Çözüm/önleme:** `konusma_v2.dogrula` 3 harften kısa çapa satırını HATA sayar; yayındaki 23 kayıt `slayt: null` yapıldı. Çapasız cümle her zaman `slayt: null` yazılır.

### H495 — Ok glifi (↓ ⟸ ←) ve "Gpi/ SNr" boşluğu kanıt eşleşmesini bozdu (2026-11-05)
- **Çözüm/önleme:** doğrulayıcı ve `kanit_onar.py` aynı norm: tüm ok blokları (U+2190–21FF, U+27F0–27FF, U+2794–27BF) ve noktalama çevresi boşluk yok sayılır. Kanıt düzeltilince `cikmis_konum_yaz.py` yeniden çalıştırılır (konum dosyası eski kanıtı tutar).

### H496 — Kısa şık açıklaması betikle kalıp ekle uzatıldı (2026-11-05)
- **Çözüm/önleme:** kalıp `BOS_KALIP`'a eklendi (HATA); sayısal alt sınır ancak şıkka özgü bilgiyle aşılır, betikle ek yazılmaz. k2-16 dahil yayındakiler taranır.
- **Çözüm/önleme:** `yol` çok-M yolu alt yol başına ayrı `sh` listesi döndürür, `G` listeleri düzleştirir; `carpi` iki ayrı kol çizer. 02 (eski + 2B) videoları yeniden üretildi.

### H498 — KMB: ata grupta transform olan sahnede kutular (bbox) 60 px kaydı (2026-11-05)
- **Çözüm/önleme:** ikisi de kutuyu `svg.getCTM()⁻¹ · el.getCTM()` ile sahne köküne çevirir. Sahnede grup kaydırması serbest; kutular hep kök koordinatında.

### H499 — KMB: clipPath'li sıvı Lottie'de dikdörtgen olarak organ dışına taştı (2026-11-05)
- **Çözüm/önleme:** sıvı organ biçiminde açık yol olarak çizildi. Kural: Lottie'ye gidecek KMB sahnelerinde `clipPath`/`mask`/`filter` kullanılmaz; biçim yolla verilir.

### H500 — KMB: altyazı bandı (alt %24) kesitteki ana yapıları örtüyordu (2026-11-05)
- **Çözüm/önleme:** anatomi 70 px yukarı taşındı, alt yapılar kadraj altına uzatıldı. Yeni KMB sahnesinde anlatılacak yapılar y ≤ 380 içinde çizilir.

### H501 — Hoca dökümü sarmalayıcısı model seçimini yutuyordu; turbo dökümüyle hocanın sözü yanlış okundu (2026-11-06)
- **Çözüm/önleme:** sarmalayıcı kalan argümanları aktarır (`"$@"`). Hocanın sınav vurgusu içeren ders kayıtları `--model Systran/faster-whisper-large-v3` ile dökülür; belirsiz pasaj içerikte iddiaya çevrilmez, zaman damgasıyla "emin değil" listesine yazılır.

### H502 — iPad pencere kipinde sistem düğmeleri geri tuşunu kapatıyordu; kullanıcı geri çıkamıyordu (2026-11-06)
- **Çözüm/önleme:** `components/shell/ipadPencere.tsx`: pencere kipi algısı (`:root[data-pencere='dar']` → üst çubuk 84 px sağa), başlık = geri düğmesi, alt yüzen geri hapı, sol kenar kaydırması + Esc/⌘[/Alt+←, yedek yollar 2 kez kullanılırsa hap cihazda kalıcı. Kural: hiçbir ekranda tek çıkış yolu sol üst köşe olamaz; görünürlük denetiminde `offsetParent` değil `getClientRects()` kullanılır (yapışkan/sabit atada null döner).

### H503 — "Güncelle"ye basınca eski sürüm açılıyor, sürekli güncelleme varmış gibi görünüyordu (2026-11-06)
- **Çözüm/önleme:** `UpdatePrompt.tsx`: güncellemede çevrimdışı ders/paket önbellekleri dışındaki tüm önbelleklerden HTML/rota kabuğu kayıtları silinir; sürüm kayıtları yalnız ileri yazılır. Kural: cihaz sürüm kaydı asla geriye yazılmaz; kabuk silme, SW'nin aradığı bütün önbellekleri kapsar.

### H504 — Ayarlarda "Küçük sürprizler" satırı görünmüyordu (2026-11-06)
- **Çözüm/önleme:** `DataPanel`'e `currentUser` geçirildi. Kural: hesap koşullu satırlar kullanıcıyı prop olarak alır, `auth.currentUser` yedeğine güvenilmez.

### H505 — Polinöropati ve Bazal Ganglionlar sesli derslerinde PDF açılmıyor, yalnız "Drive'da aç" çıkıyordu (2026-11-06)
- **Çözüm/önleme:** iki kayıt eklendi, sunucu yeniden başlatıldı, dağıtıldı. Yeni kapı `python3 scripts/kapilar/ders_pdf_kapisi.py [--sunucu …]`: her `data/sesli_anlatim/hizalama/k2-*.json` deckId'si sunucu kataloğunda açılabilir PDF'le bulunmalı (0 HATA). Kural: `ders-ekle`/hizalama sonrası SANAL_DESTELER kaydı + `meds-web` restart + bu kapı (yerel ve Oracle) — kapı geçmeden ders yayında sayılmaz.

### H506 — Ara resimler kısa kelime öbekli kutu şemasıydı, öğretmiyordu (2026-11-06)
- **Kalıcı çözüm:** Üst sınır kaldırıldı; standart "Ayrıntı ve akademik çizim" bölümü (yapı çizimi, paneller, kılavuzlu etiket, slayt kaynaklı doğruluk, isteğe bağlı Lottie `lottie` alanı). Slaytta resim olmasa da mekanizma/sıralı aşama/görselleştirilebilir konu resimlenir; slayttaki mevcut resmi yeniden çizmek yasak. Kapı (`dogrula.py`): <45 kelime, <12 etiket, <15 çizim ögesi, <2 eğrili yol → HATA. Ekran `CdAraResim` Lottie oynatır (SVG yedek).
- **Önleme:** Yeni ara resim kapıdan 0 HATA geçmeden yayına girmez; ölçü örneği k2-07 r01.

### H507 — iPad'de sesli dersten geri çıkılamıyordu; "başlığa bas = geri" çalışmıyordu (2026-11-06)
- **Çözüm:** `shell/ipadPencere.tsx` — iPad'de `.cd15-baslik` tıklaması `geriTetikle()`; hap iPad'de her zaman (geri varken) gösterilir.
- **Kural:** Geri yolu eklerken odak ekranlarını (kabuk dışı başlıklar) ayrıca kapsa; "algılanırsa göster" türü güvenlik yollarını algının başarısız olduğu durumda da sına.

### H508 — Drive'daki ses dosyasının adı başka dersi gösteriyordu: "TSSB Psikaytr 2" aslında EKT (Tedaviler) dersinin başıydı (2026-11-06)
- **Kalıcı çözüm:** 2. kayıt k2-20'nin başı ("ek" kayıt, s1–8) olarak hizalandı; TSSB yalnız 1. kayıttan işlendi.
- **Önleme:** Ses dosyası, PDF gibi, **içerikle** eşleşir (KURUL2_DERS_STANDARDI §1): hizada slayta düşmeyen ≥3 dk'lık blok "ders dışı" işaretlenir ve aynı kurulun diğer derslerinin slaytlarıyla karşılaştırılır; bir dersin başı/sonu sessizse öbür kayıtlar o derse ait olabilir diye taranır.

### H509 — Destesiz derste ders içerik paketinin kısaltmaları "Ek"e düşüyordu (adim 0), kapı %5 sınırında HATA verdi (2026-11-06)
- **Kalıcı çözüm:** liste biçiminde ders klasöründeki `meds_temp/ogrenci_ders/<ders>/sayfalar.json` (düz sayfa metni) kullanılır; k2-20'de eşlenemeyen 22 → 0.
- **Önleme:** Biçim değişen ara dosyayı okuyan betik, beklenen biçim gelmezse sessizce boş sözlükle sürmez; destesiz her derste paketten sonra `ders_icerik_adim.py` çıktısındaki "eşlenemeyen" sayısı 0 değilse nedeni bulunur (eşik altı olsa da).

### H510 — Değerlendirme kapısı kaynakça sayfasındaki yazar baş harflerini "sözlükte yok kısaltma" sayıyordu (2026-11-06)
- **Kalıcı çözüm:** "Kaynaklar/Kaynakça/Kaynak/References" başlıklı sayfa kısaltma denetiminden çıkarıldı.
- **Önleme:** Kapıyı geçmek için sözlüğe anlamı bilinmeyen kısaltma eklemek YASAK; yanlış pozitifin kökü kapıda düzeltilir.

### H511 — Şık açıklamalarına betikle yeni geçiştirme kalıpları eklendi, kapı yakalamadı (2026-11-06)
- **Kalıcı çözüm:** İki kalıp `BOS_KALIP`'e eklendi; açıklamalar şık şık yeniden yazıldı.
- **Önleme:** Şık açıklamasına betikle sabit cümle eklemek YASAK; kısa açıklama elle, şıkka özgü gerekçeyle uzatılır. Denetçi aynı cümlenin ≥3 şıkta geçmesini bulgu sayar.

### H512 — Anlatım parçalara bölünerek yazdırılınca ara resim adımı düştü (k2-21)
- **Kalıcı çözüm:** Ara resimler v2 yayımlandıktan sonra ayrı adımda üretildi (paragraf dizini yayındaki v2'den).
- **Önleme:** B1 bölünürse ara resim ayrı bir alt görev olarak MUTLAKA açılır; yayın öncesi kontrol listesinde `python3 scripts/ara_resim/dogrula.py <key>` çalıştırılır ve `src/data/ara_resim/<key>.json` yoksa ders tamamlandı sayılmaz.

### H513 — dist/assets hiç budanmıyordu: cihazda 473 derleme (3 GB), Oracle'da 92 bin parça (5,2 GB) + 5,9 GB arşiv (2026-11-09)
- **Kalıcı çözüm:** `vite.config.ts` `build.manifest: true` → `dist/.vite/manifest.json`; `server.ts` açılışta `readDistManifestFiles` ile güncel kümeyi okur, `pruneDistAssets` manifest dışı ve 7 günden eski parçaları `dist/assets`'ten siler; arşiv budaması da güncel kümeyi manifestten alır. Oracle'da `docker builder prune -af` (49,9 GB; disk 109 → 64 GB).
- **Önleme:** Hash'li çıktı biriktiren her klasöre (dist, arşiv, ses klipleri) yazan kod, "güncel küme + yaş" kuralıyla budama da yazar; "sonra temizleriz" diye bırakılmaz. Oracle'da imaj yeniden kurulduğunda `docker builder prune` dağıtım sonrası adımıdır (`dagit.sh`'a eklenmedi; elle).

### H514 — Örnek sorular ders listesinde "Hoca üslubu · N yeni soru" rozeti öğretim üyesi adının üstüne biniyordu (tablet/masaüstü, 2026-11-09)
- **Çözüm/önleme:** tek `.ks-lesson-who` içinde yazar + ` · ` + rozet (`<b>`); alan `white-space: normal` ile sığmazsa sarar. Kural: adlandırılmış ızgara alanına (`grid-area`) birden çok kardeş öge yazılmaz; koşullu ek satır aynı kabın içine girer. Düzen değişikliği telefon + tablet (768/820) + masaüstü üçünde birden denetlenir (`scripts/perf/sayfa_tarama.mjs` taşma raporu üst üste binmeyi GÖREMEZ, ekran görüntüsüne bakılır).

### H516 — Dağıtım yeniden başlatması sırasında açılan sayfa açılış ekranında sessizce takılıyordu (2026-11-09)
- **Çözüm/önleme:** `index.html` H516 bekçisi: 7 sn'de açılmazsa `/api/surum` yoklar, durum yazısı gösterir, sunucu dönünce kendiliğinden yeniler. Kural: öğrencinin bekleyebileceği her "sunucu yok / ağ yok / eski kabuk" durumu ekranda bir yazı + kendiliğinden kurtulma yolu taşır; sessiz bekleme yasak. Dağıtım saatinde gelen "site açılmıyor" bildiriminde önce Oracle `docker events`/uptime'a bakılır (bu kez `uptime: 18 s` ile doğrulandı).

### H517 — Üst bar başlığı bölünmüş ekranda ve yan ray açıkken kırpılıyordu ("Sesli dersler" → "Sesli …", "Tam ekran ve kısayollar" → "Tam ek…") (2026-11-09)
- **Çözüm/önleme:** ≥1024'te araç grubu başlıktan 1000 kat istekli küçülür ve içinde yalnız arama kutusu daralabilir (`flex: 0 1 260px; min-width: 44px`); 600–839'da kompakt "K2" çipi, yükle düğmesi hesap menüsünde, başlık telefondaki gibi iki satıra sarar. Kural: üst bara yeni araç eklerken başlık 600, 768 ve yan menülü 1024'te ölçülür; sabit genişlikli araç `flex: none` bırakılmaz.

### H518 — Ayarlar: gruplar karışık, alt sayfalar iki ayrı anahtar görünümü kullanıyor, geniş ekranda tek dar sütun (2026-11-09)
- **Çözüm/önleme:** `ProfileV12.tsx` v15 dalı veri tablosundan kurulur (Profilim · İçeriklerim · Görünüm ve okuma · Uygulama · Hesap ve veri · Yardım · Oturum), "Ayarlarda ara" + tek dokunuşla tema; kabın **üst öğesi** ≥ 860 px ise (ResizeObserver; `.pf15` kendisi 720 ile sınırlı olduğundan kendi genişliği ölçülmez) liste solda yapışkan, bölüm sağda. Anahtar ve dokunma alanı `profil.css`'te tek tip. Yükseklik sınırlı esnek sütunda çocuklar `flex: none` olmalı (yoksa `overflow: hidden` liste tek satıra çöker — ilk denemede görüldü). Kural: Ayarlar'a yeni satır `gruplar` tablosuna, doğru gruba ve `ek` arama sözcükleriyle eklenir; aynı satır ikinci bir sayfada yinelenmez.

### H519 — Sesli ders › Oynatıcı çekmecesinde "Hız" başlığı ve hız hapları içeriden/ortadan başlıyordu (2026-11-09)
- **Çözüm/önleme:** üç kurala `:root[data-v15='on']` öneki. Kural: v15 iç içe bloktaki bir sınıfı sonradan ezen kural aynı kök önekini taşır; öneksiz "ek" kural yazılmaz.

### H520 — Sesli ders listesinde süzgeç hapları sıralama düğmesinin altına giriyordu (telefonda "Arşiv" üstüne simge, tablette "Bitti" yarım) (2026-11-09)
- **Çözüm/önleme:** `dersler.css`: `.o15-ust > .o15-cipler.v15-hscroll:not(:last-child) { margin-right: 0 }` (aynı kalıbı kullanan bütün ekranları kapsar). Kural: `.v15-hscroll` yanında kardeş öge varsa o yandaki taşma kapatılır.

### H523 — Taş Masası: "Oyunu başlat / masa kur" bazen hiçbir şey yapmıyor, hata da görünmüyordu (2026-11-10)
- **Çözüm/önleme:** `istemci.ts`: `gir`/`ping` dışındaki mesaj yalnız `baglanti === 'hazir'` iken gider; hazır değilse kur/katıl/başlat/sonraki el kuyruğa girer, `girdi` gelince (gerekirse önce masaya geri oturularak) gönderilir; hamle gönderilemezse hata bildirilir. Yanıt beklenen her istek `bekliyor` durumuna yazılır → `MasaBekleme` (kurma/katılma/dağıtım tam ekran, hamle küçük hap) ve 15 sn yanıtsızlıkta hata + soket yenileme. `sunucu.ts`: kimliksiz mesaja `kimlik-bekle` hatası döner. Kural: istemci–sunucu sözleşmesinde **hiçbir istek yanıtsız düşmez**; sunucu ya durum ya hata döner, istemci her bekleyen isteği görünür kılar ve zaman aşımına bağlar.

### H524 — Taş Masası: Taş Domino masası açılır açılmaz "Cannot read properties of undefined (reading 'length')" ile çöküyordu (2026-11-10)
- **Çözüm/önleme:** erişim `o.cezalar?.length` yapıldı (cezası olmayan oyun = boş liste). Kural: yeni oyun türü eklenirken `tasMi`/`as OkeyGorunum` geçen her yer gözden geçirilir; ortak kabuk bileşenleri oyuna özgü görünüm alanlarını (`cezalar`, `atiklar`, `acti`) yalnız isteğe bağlı erişimle okur, `as` dökümüyle alan varsayılmaz.

### H525 — Taş Masası: başlamış masaya gelen arkadaş geri çevriliyor, kopmalar görünmüyordu (2026-11-10)
- **Çözüm/önleme:** `sunucu.ts`: oyun sürerken gelen bağlantı izleyici olur (`izleyici` haritası, `gorunum(…, null)` ile gizli bilgi açılmaz), `koltukIste`/`koltukVer`/`koltukRed`; koltuk devri `oda.devir` (bağlantı kimliği → koltuk kimliği, motor durumu değişmez, her kimlik okuması `sid()` üzerinden); kopan koltuğun anı `kopZ` → görünümde `kopSn`; yanlış yazılan kod (O/0→D, I/1→L/J/T) var olan odaya eşlenir. İstemci: davet kodu `sessionStorage`'da girişe dek saklanır; `deneme`/`sonrakiDeneme` → `MasaBaglanti.tsx` katmanları. Kural: masaya gelen hiçbir kişi açıklamasız geri çevrilmez; bekleyen her durum (kim, ne kadar, ne yapılabilir) ekranda yazılır. Sınama kancası `window.__masaTest` yalnız `?masatest` kipinde.

### H526 — Taş Masası: Remi/Kastet düzenlemede elden taslağa konan taş geri alınamıyordu (2026-11-10)
- **Çözüm/önleme:** `OkeyMasa.tsx` `duzen.onTas`: el taşına (`elMap`) dokununca gruplardan çıkar → ıstakaya döner; masa taşı seçilir. Taslak araçlarında her eklemenin tek tek geri alma yolu olmalı.

### H527 — Taş Masası: dar ekranda eylem düğmeleri 3–4 satıra yığılıyor, durum yazısı "Sıra…" diye kesiliyordu (2026-11-10)
- **Çözüm/önleme:** dar kipte tek satır, simge üstte kısa yazılı, yatay kaydırılan düğmeler; durum yazısı sarar ve en az 150 px; oyun sırasında `html.mk-oyunda .nb-wrap` gizli (bağlantıyı masa gösterir). Yeni eylem eklerken 375×740'ta sayfa_tarama/senaryo ile bakılır.

### H528 — Taş Masası: lobide mod seçenekleri "NormalZorlu", "KlasikYığma7-0AtlamaHızlıÇek-çek" diye bitişik yazı olarak görünüyordu (2026-11-10)
- **Çözüm/önleme:** ortak `ModSecici.tsx` (`OyunModu`, `UnoModu`: başlık + kısa tanıtım kartları, seçili işaret) hem lobide hem kurulum yaprağında; bot kurulumu `asistan`/`unoMod`/`tasSayisi` gönderir. `lobi.css` + `kurallar-gorsel.css` (liste imleri açık, numaralı `mk-adimlar`). Kategoriler ve sıra tek kaynakta: `oyunKatalog.ts` (merkez kartları, kural sekmeleri, kısayollar). Kural: TSX'e yeni `mk-*` sınıfı yazınca aynı işte CSS'i de yazılır; `grep -rn "<sınıf>" src/styles` boşsa iş bitmemiştir. Yeni ayar lobiye eklenirken bota karşı kurulum yaprağına da eklenir.

### H529 — Taş Masası: tüm oyunlarda hamleler gecikmeli görünüyordu (2026-11-10)
- **Çözüm:** `src/services/masa/tahmin.ts` iyimser tahmin: oyuncunun kendi hamlesinin istemcide kesin bilinen sonucu (XOX/Go işareti + Go esir alma, Uno/Pişti kartı, Domino taşı, Çizgi adımı, 101 taş atma) anında ekrana yazılır; gizli bilgi tahmin edilmez (sıra bilinmiyorsa `''` → ikinci hamle kilitli). `istemci.ts`: `onayli` son sunucu görünümü; `durum` tahmini ezer, `hata` ya da 15 sn yanıtsızlıkta onaylıya dönülür. Sınama: 7 motorda bot oyunlarıyla 11.700 tahmin sunucu sonucuyla karşılaştırıldı (tahta/el birebir; yalnız Pişti yeni dağıtımı ve Çizgi tur sonu `kalan` farkı, sunucu düzeltir); tarayıcıda 1,6 sn yapay gecikmede işaret anında çizildi.
- **Önleme:** Yeni oyun/hamle eklenince `tahmin.ts`'e kesin bilinen kısmı eklenir ve aynı karşılaştırma koşulur; ekran hiçbir zaman ağ yanıtına kilitlenmez. Okey per açma/işleme/çekme hâlâ sunucuyu bekler (ıstaka düzeni + gizli taş). Ağ tarafındaki sıçramalar için kalıcı çözüm ancak WS'yi tünelden ayırmaktır (ayrı alt alan, Cloudflare/Oracle erişimi kullanıcıda).

### H530 — Kısık amfi kaydında hoca dökümü uydurma cümlelerle doluyordu (2026-11-10, k2-22/23/24/58)
- **Çözüm/önleme:** `hoca_dokum.py` ilk 10 dk'nın ortalamasını ölçer; −28 dB'den kısıksa süzgeç + normalleştirme kendiliğinden uygulanır (normal kayıtta 2026-10-27 "ham ses en iyi" bulgusu geçerli kalır). Kısık kayıtta `--model Systran/faster-whisper-large-v3` verilir (35 dk ≈ 6 dk GPU). Döküm hangi derse ait diye dosya adına değil içeriğe bakılır: bu gece "Ses Klibi 1 (1)" adlı kayıt Psikiyatri değil Epilepsi çıktı.

### H531 — Hoca sesi sonradan gelen yayımlanmış derste anlatım baştan yazılmaz; kısmi revizyon ve tekrar dolgusu tuzağı (2026-11-10)
- **Çözüm/önleme:** Akış: A1b (ses_hizasi + hoca_vurgulari + "Anlatıma eklenecekler") → `yayinla.py kimlik` → yalnız var olan paragraflara ekleme (yeni paragraf/silme/sıra değişikliği yok) → birleştirme sonrası eski kimlikleri metinle geri yazma (`meds_temp/ogrenci_ders/k2-58/is/hoca_rev.py kimlik`) → bağımsız denetçi (yalnız değişen cümleler) → `yayin_hazirla_destesiz.sh` → `klip_tasi.py <key> --eski <eski.md>` → `sesli_yayinla.py` (EMA yalnız değişen klipleri üretir: 4–9 klip) → Oracle `meds-cumle-zaman` + `meds-kelime-zaman-hat`. `hoca` alanına yalnız `tur: sinav` bağlanır (`yayinla.py yaz` dogrulaması HATA verir); bilgiyi tekrar eden vurgu cümlesi yazılmaz, yalnız alan bağlanır; hocanın "sınavda çıkar" demesi doğrulanmış çıkmış değildir.

### H532 — CPU'lu `meds-ema` birimi açıkken ders EMA işi GPU yerine CPU'ya düşebiliyordu (2026-11-10)
- **Çözüm/önleme:** ders sesi üretmeden önce `systemctl --user stop meds-ema` + `cozucu_ses_gpu.sh scripts/sesli_anlatim/ema_isci.py bekle`; günlükte "EMA Lightning hazır: cuda" görülür. İş bitince birim yeniden başlatılır. Kalıcı çözüm (birimi kaldırmak ya da GPU başlatıcısına çevirmek) kullanıcı kararı bekliyor.

### H533 — Taş Masası: dar ıstakada grup toplamı yanlış; Go/XOX botu hiç hata yapmıyordu (2026-11-10)
- **Çözüm:** `uzlas` boyut değişince `diz(yeni, gruplar(eski))` ile grupları taşır; `diz` önce boşluklu, sonra satır sonunda bölerek (yapıştırmadan) dener; `OkeyMasa` sütun payı `max(4, %35·n) + kat`. `OdaAyar.botZorluk` (kolay/orta/zor, varsayılan orta): XOX hata olasılıkları (rastgele kare / kazancı / engeli kaçırma), Go gürültü + ara sıra tahmini hamle + tehlikeyi görmeme; zor = eski bot. Bota karşı Go/XOX'ta "Geri al" (insan hamlesi + bot yanıtı; süreli Go'da yok). Sırala + Masayı diz iki modda; "Istakayı otomatik sırala" tercihi (varsayılan açık): ele yeni taş girince son dizme biçimine göre dizilir.
- **Önleme:** Istaka düzeni değiştiren her işlev grupları korumalı; grup toplamını gösteren her ekran dar boyutta (`yuva_t` sınaması: 21 taş 6 grup, sütun 16/14) denenir. Bot ekleyen her oyuna zorluk seçeneği verilir; "kusursuz bot" yalnız Zor'da. Sınama `tahta.sinama.ts` (kolay bot 40 elde ≥5 kayıp).

### H534 — Taş Masası: masadaki taş eldeki taşlarla yeni pere katılamıyordu (2026-11-10)
- **Çözüm:** `duzenle` üç motorda da masadaki taşların tamamı + elden taş alır; her per geçerli olmalı, masadan ele taş dönmez. Elden taş katıldıysa hamle sayılır (`hamleYapti`, yedilide el biterse kazanır, takımda elden taşla 4'lenen grup hediye verdirir; 101'de atacak taş kalmalı, çiftlere dokunulmaz, çiftle açan elden katamaz, masadaki okey `perCoz` ile yeniden değer alır). `OkeyMasa.tsx`: düzenleme kipinde ıstaka taşı seçilip/sürüklenip taslağa girer, 101'e "Masayı düzenle" düğmesi. Düz Okey'de masaya per açılmadığı için uygulanmaz.
- **Önleme:** Masaya taş koyan her oyunda "masadan taş + elden taş = yeni per" senaryosu motor sınamasında bulunur (`yedili.sinama.ts`, `yuzbir.sinama.ts` düzenle bölümleri). Bir hamle türü bir oyuna eklenince aynı masa modelini paylaşan öteki oyunlar (yedili/takım/101/kastet/remi) birlikte gözden geçirilir.
- **Çözüm:** Taslak ekrandaki sırayla başlar (`taslakBasla`), boşalan per yer tutucu olarak kalır (`om-per--bos`, kesikli çerçeve), her per düzenleme başındaki piksel genişliğini en az genişlik olarak korur (`PerAlani enAz`); yeni per sona eklenir, yalnız sondaki sonradan eklenmiş boş perler atılır (`kirp`). Onayda boş perler hamleye girmez.
- **Önleme:** Kullanıcının elle düzenlediği alanda (masa taslağı, ıstaka) öğeler kendiliğinden yer değiştirmez; düzen yalnız kullanıcının açık isteğiyle (Sırala, Masayı diz) değişir. Sınama: düzenlemede taş alıp per boşaltınca komşu perin `getBoundingClientRect().left/top` değeri değişmemeli.

### H542 — Uno'ya 10 yeni mod eklenirken motor sınamasının yakaladığı dört kural hatası (2026-11-10)
- **Çözüm:** (1) Biriken ceza varken yalnız `yiginUyar` geçerli. (2) `sonIslem` her hamlenin sonunda eli 1'e düşen herkesi (oynarken UNO diyen hariç) `yakalanabilir` yapar. (3) Uyan kart kalmadıysa çekme serbest: jokeri oynayan 2 kart çeker, sıra geçer. (4) `bekle.tur === 'yalan'` iken atıkta iki kart bırakılır.
- **Önleme:** Uno'ya kural/kart ekleyen her değişiklikte `npx tsx src/services/masa/motor/uno.sinama.ts` ve `unoMod.sinama.ts` 0 hata vermeli: her mod için birim senaryolar + bütün oyuncu sayılarında hepsi-bot rastgele eller (kart korunumu, tıkanmama, gizlilik, puan toplamı) + bulanık hamle. Yeni bir "bekleyen karar" ya da el sayısını değiştiren etki eklenince korunum denetimine (`korunum`) ve `sonIslem` UNO taramasına dahil edilir. Arayüz: `meds_temp/uno_ui/uno_ui.mjs` (başsız Chrome, `?masatest`, 12 mod × telefon dikey/yatay, tablet, masaüstü; taşma, dokunma hedefi, konsol hatası). Başsız sınama çıktısı `/tmp/claude-1000` kotasına yazılmaz (EDQUOT ile yarıda kesildi), `meds_temp` altına yazılır.


### H536 — Değerlendirme kapısı tasarım PDF'inin harf aralıklı başlıklarını ("Y A N I TL A R", "KAYN AKLAR") kısaltma sanıyordu (2026-11-09, k2-22)
- **Kalıcı çözüm:** kapı tamamı büyük harf olan satırları (başlık/üst yazı) kısaltma taramasından çıkarır, ilk satırı boşluksuz birleştirip KAYNAK/REFERENCES ile başlayan sayfayı kaynakça sayar, "Soyad GP," atıf baş harflerini eler. Eski derslerde (k2-20/21/38) sonuç değişmedi (0 HATA).
- **Önleme:** Kapıyı geçmek için sözlüğe anlamsız kısaltma yazılmaz (H510); yeni biçim tuzağı kapının kendisinde düzeltilir.

### H537 — A1a/A2 "kanıt" alanları birden çok satırı birleştiren özetler olduğundan değerlendirme kapısından geçmiyordu (2026-11-09/10, dört derste)
- **Kalıcı çözüm:** her kayıt tek satır/tek hücrelik birebir alıntıya indirildi; açıklama `neden`'e taşındı.
- **Önleme:** A1a/A2 yönergesine kural: `kanit` = TEK birebir satır ya da tablo hücresi; yazar üretim sırasında pymupdf normuyla doğrular (`kaynak_kapisi.py` + `degerlendirme_dogrula.py` paket kurulmadan önce koşulur).

### H538 — 5. parti derslerinin anahtarları `MODUL_ANAHTARLAR`'da yoktu: yazımla tutulan kısaltmalar (DSM, EEG, SSRI) harf harf okunmamış olabilir (2026-11-09)
- **Çözüm:** 6. parti anahtarları eklendi (k2-22, 23, 24, 58). **Açık:** k2-19/20/21/37/38 sesleri bu yolla üretildiği için kısaltma okunuşu dinlenip gerekiyorsa anahtar eklenip yalnız ilgili klipler yeniden üretilmeli (kullanıcı kararı).
- **Önleme:** `sesli_yayinla.py` yeni anahtarı `modul_okunus.modul_mu` ile denetleyip değilse uyarır (yapılacak); el kitabı §19 adım 8'e madde.

### H539 — EMA tam MP3 yüklemesi Oracle'daki başka bir dağıtımın sunucu yeniden başlatmasına denk gelince iş "hata"ya düştü (2026-11-09, k2-22)
- **Çözüm:** `POST /api/sesli-anlatim/uret {key, saglayici: ema-yerel, ses: Ema}` ile yeniden kuyruklandı; klipler yeniden kullanıldı (0 yeni klip).
- **Önleme:** dağıtım öncesi `dagit.sh` kuyrukta `calisiyor` EMA işi varsa beklemeli ya da işçi `tam/bitir` adımını 3 kez yinelemeli (yapılacak). İşçi günlüğü: `journalctl --user -o cat | grep <key>` (birim değil, scope).

### H540 — `kelime_zaman.py --gpu` elle çağrıda `libcublas.so.12` bulamayıp sessizce CPU'ya düştü (2026-11-10)
- **Çözüm:** elle koşuda birimdeki `LD_LIBRARY_PATH` dışa aktarıldı (k2-24/58 GPU'da 345–351 sn).
- **Önleme:** `kelime_zaman.py` başında `nvidia/*/lib` yollarını `LD_LIBRARY_PATH`'e kendisi ekler (yapılacak); CPU'ya düşüş UYARI değil, belirgin HATA satırı olmalı.

### H541 — Destesiz derslerin örnek soruları k2-12'den beri siteye yayınlanmıyordu (2026-11-10)
- **Çözüm:** `meds_temp/ogrenci_ders/arac/ornek_yayinla.py <kimlik> <anahtar>` (ders paketi → `kurul2_ders_paketleri`, sorular → s16 build (kurul 2) → `disa_aktar`); 6. partide 4 ders yayınlandı. **Açık:** k2-12…k2-21, k2-37, k2-38 için koşulmalı (kullanıcı kararı; s16 denetimi yazarların bıraktığı eksikleri gösterebilir). s16 K2 index'inde k2-01/02/05/08 yazım dosyaları boş olduğu için sorunlu görünüyor (site dosyaları korunuyor).
- **Önleme:** destesiz yayın betiğine s16 adımı eklenir; `ders_icerik_dogrula.py` sitede örnek soru dosyası yoksa HATA versin (yapılacak).

### H543 — İçi boş madde imi pymupdf metninde "o" harfi olarak geldi; değerlendirme kapısı birebir kanıtları reddetti, yazar bilgisiz kanıt satırına kaçtı (2026-11-10, k2-26)
- **Kalıcı çözüm:** kapı satır başında büyük harf/rakam/% önündeki "o"yu siler; dört atomun kanıtı yeniden bilgiyi gösteren birebir satıra döndü (k2-21/22/24/38 kapıları değişmedi, 0 HATA).
- **Önleme:** Kapıyı geçmek için kanıtı bilgiyle ilgisiz bir satıra kaydırmak YASAK (kanıt bilgiyi göstermeli); iki kapının metni farklıysa kök neden kapıda/çıkarımda düzeltilir ve koordinatöre bildirilir.

### H544 — Ek modül içeriği hocanın materyali sorulmadan yazıldı; çalışma soruları gelince 16 konunun tamamı yeniden yazıldı (2026-11-10, Yürüyüş ve Kampçılık)
- **Kalıcı çözüm:** içerik `meds_temp/ek_modul/<modül>/hoca_calisma_sorulari.txt` esas alınarak yeniden kuruldu (`GOREV.md`: konu başına hoca soru numaraları + hocanın kendi içinde çeliştiği yerlerde verilen kararlar); ilk taslak `eski/` altında kaynak olarak kaldı. `scripts/ek_modul/TALIMAT.md`'ye "Hocanın çalışma soruları varsa ESAS KAYNAK odur" bölümü eklendi; iki bağımsız denetçi hoca kapsamını soru soru yeniden eşledi.
- **Önleme:** yeni ek modülde ilk iş hocanın materyalini istemektir (AGENTS kural 30). Hocanın kendi içinde çeliştiği cevaplar (kazık 45°/90°, tuvalet 50/150 m) sessizce "düzeltilmez": en çok yinelenen değer esas alınır, ekrana "ikisini de bil" notu düşülür ve kullanıcıya raporlanır. Hocanın bilimsel olarak tartışmalı ifadesi (baştan %50 ısı kaybı, gnays kristalleri) hocanın dediği gibi kalır; metin ona aykırı yeni iddia eklemez.

### H545 — `git add server.ts` başka oturumun commit'lenmemiş iki satırını da commit'e aldı; depoda olmayan dosyayı içe aktaran sunucu kodu origin/main'e gitti (2026-11-10)
- **Çözüm:** iki satır ayrı bir commit ile depodan çıkarıldı (çalışma ağacında o oturum için bırakıldı), Oracle'daki `server.ts` commit'lenmiş sürüme geri yazıldı, dağıtım yeniden koşuldu.
- **Önleme:** ortak dosya sahnelenmeden önce `git diff <dosya>` okunur; yabancı satır varsa yalnız kendi parçaların sahnelenir (`git apply --cached` / `git update-index --cacheinfo`). Commit'ten sonra `git show --stat` satır sayıları beklenenle karşılaştırılır. Oracle'da `server.ts`'in kirli sürümle bulunmasının kaynağı saptanamadı (dağıtım temiz worktree'den yapılır); yinelenirse o dakikada Oracle'a yazan öteki süreç aranır.

### H546 — Ek modülde sesli ders PDF'le birlikte ilerlemiyordu; eşleme kurulurken iki ölçüm tuzağı (2026-11-10, Yürüyüş ve Kampçılık)
- **Kalıcı çözüm:** `scripts/ek_modul/pdf_esle.py` → `src/data/ek_moduller/<modül>/pdf_esle.json` (klip başına sayfa, bölüm kutusu, satır kutuları, cümle zamanı, cümle → not maddesi); ekranda "PDF ile" kipi (`EkPdfDers.tsx`, `PdfDocView` işaret katmanı). LLM ve GPU yok; ses yeniden üretilmedi.
- **Önleme:** ek modülde ses ya da ders kitapçığı yeniden üretilince `pdf_esle.py` yeniden çalıştırılır; `dogrula.py --modul` eşleme eskimişse (klip özeti ya da PDF boyutu tutmuyorsa) HATA verir, ekran da özeti tutmayan klibin eşlemesini kullanmaz. Karşılığı bulunamayan cümleye madde uydurulmaz (yalnız bölüm çerçevesi; kural 17'deki "çapa uydurma" yasağıyla aynı ilke).

### H547 — Gövdesi yalnız resim olan slayda dayanan doğrudan çıkmış, değerlendirme kapısından geçemiyordu (2026-11-10, k2-28 s.21)
- **Kalıcı çözüm:** kapıya atom kuralının eşi eklendi: çıkmış kaydı `kanit_goruntu` (görüntüden okunan cümle) taşıyorsa ve sayfa metni 60 karakterden kısaysa birebir arama atlanır; `cikmis_konum_yaz.py` bu alanı yayın dosyasına taşır. k2-16/24/26'da sonuç değişmedi (0 HATA).
- **Önleme:** görüntü sayfasına dayanan çıkmış eşlemesi `kanit` + `kanit_goruntu` ile yazılır ve denetçi sayfa görüntüsüne bakar; kanıt metni olan başka satıra kaydırılmaz, eşik gevşetilmez.

### H548 — Slayt altındaki kaynak satırının dergi adı "sözlükte olmayan kısaltma" sayıldı (2026-11-10, k2-28 s.31)
- **Kalıcı çözüm:** "et al" ve "yıl;cilt" kalıbını birlikte taşıyan satır kısaltma taramasından çıkarıldı.
- **Önleme:** kapıyı geçmek için sözlüğe dergi adı ya da anlamsız kısaltma yazılmaz (H510); yeni biçim tuzağı kapının kendisinde düzeltilir.

### H549 — Önem maddesinin alıntısı olarak slayttaki kaynak künyesi yazıldı (2026-11-10, k2-28 2t02-23)
- **Kalıcı çözüm:** `onem_dogrula.py`: alıntı `gorsel: true` taşıyorsa ve sayfa metni 120 karakterden kısaysa birebir arama atlanır. Madde, şemadaki tanım cümlesiyle (`gorsel: true`) yeniden yazıldı.
- **Önleme:** görüntü sayfasından alıntı `{"sayfa", "metin", "gorsel": true}` ile yazılır, denetçi görüntüden doğrular. Kapıdan geçsin diye bilgi taşımayan satır (künye, başlık, sayfa numarası) alıntı/kanıt yapılmaz.

### H550 — Canlı çizimde kontur doğru, etiketi yanlış figüre düşüyor ya da slayt yazısını kapatıyordu (2026-11-10, k2-28)
- **Çözüm:** yanlış yere düşen ve yazı kapatan etiketler kaldırıldı (etiketli kontur 72 → 20), konus/kauda konturları ayrıldı, eksik okkulta konturu eklendi; denetçi kararları `denetim_<hash>.json` ile uygulandı.
- **Önleme:** (1) yazı parçasını boyayan konturda etiket yazılmaz (boyanan yazı zaten etikettir); (2) kendi yazısını taşıyan figür/kutu konturunda etiket yalnız slaytta olmayan bilgiyi ekliyorsa yazılır; (3) yazar yayından önce bindirmeyi ETİKETLERİYLE üretip bakar (`etiket_konum` + `pdfDoc.css` yazı boyutu; k2-28 `cizim/bindir2.py`); (4) yanlış yerde etiket, etiketsizlikten kötüdür — güvenle oturmayan etiket kaldırılır.

### H551 — Giriş yapmış öğrenci kendi profilini ve arkadaşlık isteklerini göremiyordu (2026-11-10)
- **Çözüm:** izin listesine `kisi/` ve `arkadas` eklendi; jeton gerektiren öğrenci isteği de `auth.authStateReady()`'yi (≤4 sn) bekler.
- **Önleme:** `verifiedUid` okuyan yeni bir GET ucu eklenince `ogrenciJetonu` listesine de eklenir; uç yazıldığında girişli kullanıcıyla tarayıcıdan GET sınanır (curl'deki jetonsuz yanıt "çalışıyor" sayılmaz).

### H552 — Sesli çalışma sorularında boşluk doldurma "boşluk" diye okunuyordu (2026-11-10, ek modül)
- **Çözüm:** 100 boşluk sorusunun her birine soru biçimli `okunus` alanı yazıldı ("Uyku tulumu, vücudun ne kaybını önlemek için kullanılır?"); ses yalnız onu okur, ekran ve kitapçık `metin`'i göstermeye devam eder. Sesler GPU'da yeniden üretildi, `pdf_esle_hoca.py` ile takipçi yeni seslere eşlendi (okunuş sorunun kitapçıktaki satırlarını yakar).
- **Önleme:** `dogrula.py --modul` boşluklu (`__`) her hoca sorusunda `okunus` yoksa ya da soru işaretiyle bitmiyorsa HATA verir. Yeni boşluklu soru eklenirken (her modülde) okunuş elle, doğal soru cümlesi olarak yazılır; mekanik "boşluk/ne" değişimi yapılmaz.

### H553 — Değerlendirme kapısı OCR'lı metinden alınan çok satırlı kanıtları PDF'te bulamadı (2026-11-12, k2-31)
- **Çözüm:** `taslak/bilgi_havuzu.jsonl`'da a44/a53/a81/a84/a110 alıntıları bilgiyi destekleyen TEK pymupdf satırına indirildi (bilgi metni değişmedi); üç görsel çıkmışa sayfa görüntüsünden okunan `kanit_goruntu` eklendi; beş kısaltma `kisaltma_sozluk.json`'a eklendi (slayt yazımı "IGM"). Kapı 0 HATA.
- **Önleme:** A2'de kanıt alıntısı her zaman `pymupdf.open(pdf)[s-1].get_text()` satırlarından birebir kopyalanır; OCR/`sayfalar.json` yalnız metni okumak/anlamak içindir. Liste/tablo sayfasında birden çok satırı kapsayan alıntı yazılmaz. Metinsiz (<60 karakter) sayfaya dayanan çıkmışa `kanit_goruntu` zorunludur.

### H554 — Ders içerik paketinde "bilgiler boş": bilgi havuzu `tur` alanı içerik tipiyle dolduruldu (2026-11-12, k2-29)
- **Çözüm:** havuzda şema dışı `tur` değerleri `icerik_turu` alanına taşındı; `patogenez` → `mekanizma`, diğerleri → `spot` (tani/tedavi/epidemiyoloji olduğu gibi). Bilgi metni ve kanıtlar değişmedi. Üretici 125 bilgi çıkardı; kaynak kapısı 0 HATA, denetle.py 0 HATA.
- **Önleme:** `bilgi_havuzu.jsonl` `tur` yalnız TALIMAT §8 listesinden; içerik tipi `icerik_turu`'na. Yönergeye bir satır eklendi.


### H555 — Şık açıklamasında uzunluk dolgusu: aynı "ana bilgi" cümlesi birden çok şıka eklendi (2026-11-12, k2-29 / k2-30)
- **Çözüm:** denetçiler yinelenen cümleleri şıkka özgü (kavram ne, ne işe yarar, bu soruda neden yanlış) slayta dayalı cümlelerle değiştirdi (k2-30: 122 şık metni; k2-29 denetçide); şık ses metinleri yeniden üretilip EMA klipleri yenilenir.
- **Önleme:** şık açıklaması kapıyı geçmek için betikle uzatılmaz (AGENTS 14 dolgu yasağı); kısa kalan açıklama elle, o şıkkın kavramıyla yazılır. Önerilen kapı eki: aynı sorunun iki şıkkında birebir aynı ≥6 kelimelik cümle HATA (`sik_aciklama.py`).

### H556 — "PDF indir" herkese "X-API-Password başlığı gereklidir" diyordu; canlıda başsız tarayıcı da yoktu (2026-11-13, kullanıcı bildirdi)
- **Kalıcı çözüm:** (1) `STUDENT_WRITE_ROUTES`'a `['POST', /^\/api\/pdf\/render$/, 'belge']` eklendi; yeni `belge` sınıfı IP başına dakikada 20 / saatte 300 (`STUDENT_WRITE_LIMITS`), ağır Chrome işi zaten sunucuda kuyruklu (2 koşut + 8 kuyruk, sıra doluysa 429). (2) `Dockerfile.oracle`'a `chromium` + `fonts-dejavu-core` eklendi (ARM'de `chromium 156` paketi var; geçici konteynerde uçtan uca sınandı: `%PDF-1.4`, 13.595 bayt). (3) `docs/API_KATALOG.md` parolasız uçlar bölümü eklendi.
- **Önleme:** yeni bir parolasız uç gerektiğinde önce "veri yazıyor mu?" sorusu sorulur: yazmıyorsa `readOnlyPosts`/`STUDENT_WRITE_ROUTES`'a **sınırıyla** eklenir, yazıyorsa parola ister. Kapı: `python3 scripts/kapilar/pdf_basim_kapisi.py` (yerelde ve canlıda) `/api/pdf/status` `available:true` + parolasız 200 ve `%PDF` imzası arar; 401'de "uç beyaz listede değil", tarayıcı yoksa "imaja chromium eklenmeli" der.
- **Kalıcı çözüm:** (1) `~/.local/bin/opendesign-kopru.py` + `opendesign-kopru.service` (systemd --user, `Restart=always`, `MemoryMax=256M`, `CPUQuota=50%`): uygulamanın `claude-od-01…14` rota adlarını geçit kimliklerine çevirir, SSE/`tool_use` aynen akıtılır, eşlenmemiş ad olduğu gibi geçer. (2) Gerçek geçit adresi `~/.claude/opendesign-kopru.json` → `upstream` alanında (settings'ten okunmaz; kendine işaret ederse betik açılışta durur). (3) `settings.json` `env.ANTHROPIC_BASE_URL` = `http://127.0.0.1:8787`. (4) Masaüstü 3P yapılandırması `~/.config/Claude-3p/configLibrary/<id>.json`: `inferenceProvider: gateway`, `inferenceGatewayBaseUrl: http://127.0.0.1:8787`, `inferenceModels` = `claude-od-NN` + `labelOverride` (gerçek ad), `deploymentMode: "3p"`. Doğrulama: uygulama günlüğü `picker = 14 (inferenceModels)` + `ConfigHealth … healthy`; köprü günlüğü `POST /v1/messages -> 200`.
- **Önleme:** 3P `inferenceModels` rota adında üçüncü taraf işareti (`deepseek/glm/kimi/mimo/minimax/gpt/…`) kullanılmaz; ad `claude-od-NN` gibi nötr olur, gerçek model `labelOverride` ve köprü eşlemesinde tutulur. `settings.json` `env` değerleri komut satırından ezilemez — ortam değişikliği sanılıyorsa önce bu dosyaya bakılır. Köprü `upstream`'i asla kendi adresini göstermez (açılışta kapı var). Ayrıntı: `~/.claude/OPENDESIGN_KULLANIM.md`.

### H558 — Bash aracı hiç açılmıyordu: `apply-seccomp: write /proc/self/setgroups … Permission denied` (2026-11-13, kullanıcı bildirdi)
- **Kalıcı çözüm:** `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0` + `/etc/sysctl.d/99-userns.conf` içine `kernel.apparmor_restrict_unprivileged_userns=0` (açılışta kalıcı) ve `sudo ln -sf /etc/apparmor.d/bwrap-userns-restrict /etc/apparmor.d/disable/` + `sudo apparmor_parser -R /etc/apparmor.d/bwrap-userns-restrict`. Doğrulama: `echo`, `git status`, `git log` çalıştı.
- **Önleme:** Aynı hata görülürse önce `sudo dmesg | grep -E "apparmor|userns" | tail` bakılır; `unpriv_bwrap` + `sys_admin` satırı varsa profil bir paket güncellemesiyle geri gelmiştir, iki komut yinelenir (`aa-complain` çözüm değildir). **Ayrı katman:** sandbox ağ kapısı (`sandbox.network.allowedDomains: []`, `allowManagedDomainsOnly: true`) bu düzeltmeden sonra da kapalıdır; `git fetch/push`, `ssh`, `curl` Bash'te çalışmaz — ağ işleri Terminal panelinden yapılır ya da kullanıcı Ayarlar → Claude Code'dan ağ iznini açar. İki katmanı karıştırıp "kabuk açıldı, ağ da açıldı" sanmak yeni bir yanlış kök neden avına yol açar.

### H559 — İçerik katmanı toplu "silinen" yazdı: sözlükte 750 terim, Öğren'de 11 deste sunucuda görünmüyordu (2026-11-13, kullanıcı bildirmedi — tur sırasında bulundu)
- **Kalıcı çözüm:** (1) İki fark dosyasında `silinen` boşaltıldı, önce `data/_yedek/*.fark.<zaman>.bak` yedeği alındı, yazım `tmp` + `os.replace` ile atomik yapıldı. Doğrulama (meds-web yeniden başlatıldıktan sonra canlı uçlardan): sözlük **4368** (`bilinç` var), deste **186** (11 k2p deste de listede). (2) `src/services/contentOverlay.ts` `donustur()` içine **toplu silme freni** eklendi: bir dönüşümde yeni silme adayı sayısı `max(5, kaynak kaydı sayısının %5'i)` eşiğini aşarsa kopya bayat/eksik sayılır; silme yazılmaz, bekleyen kayıt değişiklikleri düşürülmez, kimlikler `data/content/_karantina_silinen.json`'a (son 20 olay) yazılır ve `console.warn` ile günlüğe düşer. `npx tsc --noEmit` 0 hata.
- **Önleme:** `data/content/` altına elle, başka araçla ya da eski yedekten **tam kopya bırakılmaz** (yalnız `.fark.json`). Sözlük/deste/soru sayısı beklenenden az görünürse ilk bakılacak yer `data/content/<dosya>.fark.json` → `silinen`dır; `python3 scripts/icerik_katman.py denetle` ile katman düzenli denetlenir. Günlükte "toplu silme sayılmadı, karantinaya alındı" uyarısı görülürse `_karantina_silinen.json` açılır: silme gerçekten yönetici kararıysa kimlikler fark dosyasına elle yazılır; değilse hiçbir şey yapılmaz — kayıtlar görünür kalır. Katmanı mtime'a göre "taze" saymak yetmez: bir kopya yeni damgalı ama içeriği eski olabilir.

### H560 — Ajan hattı OpenDesign geçidine taşınırken roller tek modelde birleşti, eşlenmemiş adlar sessizce geçide gitti (2026-11-13, kullanıcı istedi)
- **Kalıcı çözüm:** (1) **Tek kaynak** `otomasyon/llm/model_sec.py::ajan_model(rol)` — yazar/denetci/hizli rolleri ayrı: `butce.json` → `claude.model`, `claude.model_denetci` (`claude-opus-4-7` → `glm-5.3-flashx`, farklı aile), `claude.model_hizli`. Bütün zincirler (ders, son prova, hastalık, checkup, kamp, olası soru, çizim, arşiv, ders işçisi) buradan beslenir; koda model adı yazılmaz. (2) Köprü haritası `scripts/opendesign/rotalar.json` (tek kaynak, 14 görünen + 18 alias) ve `otomasyon/llm/opendesign.py::ESLEME` aynı olmak zorunda: `python3 scripts/opendesign/kopru.py --doctor` ikisini karşılaştırır, eksik eşlemede HATA verir. (3) CLI'sız makineler (Oracle) için `opendesign.py` doğrudan `/v1/messages` gönderir ve adı `ESLEME` ile çevirir; tanınmayan ad gönderilmez, açık hata yazılır. (4) `llm_kilit.py` bütün yollarda korunur — taşıma, kurallı 20'yi gevşetmez.
- **Önleme:** Yeni bir model/ad eklenirken **iki** yere yazılır: `rotalar.json` ve `opendesign.ESLEME`; sonra `kopru.py --doctor` koşulur (0 HATA). Bir betiğe `--model <sabit ad>` yazılmaz, `ajan_model()` çağrılır. Aynı aile iki rolde görünüyorsa (yazar = denetçi) denetim bağımsızlığı yoktur: denetçi rolü ayrı aileye (`glm-*`/`gpt-*`) bakar. `claude` CLI çağrısı eklerken önce `llm_kilit` + `model_sec` çifti eklenir, sonra çağrı yazılır.

### H561 — Artifact stüdyosu: önizleme sunucusu bulunamadı, grafikte iki farklı büyüklük tek eksende ezildi, `.claude/launch.json` `/dev/null` ile maskelendi (2026-11-13, kullanıcı istedi)
- **Kalıcı çözüm:** (1) `kur.sh` artık `LAUNCH="$(dirname "$MEDS")/.claude/launch.json"` kullanır (`ARTIFACT_LAUNCH` ile değiştirilebilir); `--kontrol` hangi dosyaya baktığını yazar. (2) `studyo.py::_olcek` yuvarlak adım (1·2·2,5·5×10ⁿ) ve sütunlarda sıfır tabanı verir; `"eksen": "sag"` verilen seri sağ eksende **kendi** ölçeğiyle çizilir, sağ etiketler `_izgara` içinde ayrı basılır. (3) Maskeleme kalktıktan sonra `git checkout -- .claude/launch.json` ile izlenen dosya geri yüklendi.
- **Önleme:** Önizleme sunucusu eklerken **önce** `mcp__Claude_Browser__preview_list`/`preview_start` ile yolun doğruluğu sınanır; `launch.json` yazımı oturum köküne yapılır. Bir dosyada `git diff`, `rm` ya da `cat` "desteklenmeyen tür / meşgul" derse **dosyanın kendisi değil üstündeki mount** sorgulanır: `findmnt -T <yol>` + `grep <yol> /proc/self/mountinfo`. Maskeleme biter beklemeden `git rm`/`rm -f` denenmez — `rm -f` **başarılı görünüp** izlenen dosyayı silebilir (bu turda oldu; geri yükleme `git checkout --` ile yapıldı). Grafikte büyüklük farkı ~10× ise çift eksen zorunlu; tek eksende "küçük seri görünmüyor" bir tasarım tercihi değil hatadır.

### H562 — Canlıda yeni anahtar "yok" göründü: `env_file` yalnız konteyner oluşturulurken okunur, loopback da konteynerde loopback değildir (2026-11-13)
- **Kalıcı çözüm:** doğrulama `printenv` ile değil **uçtan uca** yapılır: geçide doğrudan `POST /v1/messages` (200) + konteynerde `grep -c "^MEDS_OPENDESIGN_KEY=" /app/.env` (1) + canlı `POST /api/ai/generate` (`providerUsed: "OpenDesign (…)`). Yazma parolası gereken canlı sınamalarda `X-API-Password` `.env`'deki `MEDSORU_API_PASSWORD`'dan okunur (değer ekrana yazılmaz; `scp` edilen küçük betikle).
- **Önleme:** `.env`'e yalnız dotenv'in okuyacağı yeni anahtar ekleniyorsa konteyner yeniden başlatma yeterlidir; **compose `environment:` listesine eklenmesi gereken** bir değişken söz konusuysa `docker compose up -d --force-recreate` gerekir (bu tur gerekmedi). "Container env'de yok" tek başına "uygulama görmüyor" demek değildir; kanıt uygulamanın kendi ucundan alınır. Konteyner içinden atılan istek yönetici/loopback muamelesi görmez.

### H570 — Ders analizi betiği tam ders anahtarını "kayıt defterinde yok" sandı (2026-11-13, k2-62/k2-65)
- **Kalıcı çözüm:** `kayit_bul` gelen anahtarı `k2-62` biçimine normalleştirir (`"-".join(key.split("-")[:2])`); paket yolu ve çıktı adı kısa kimlikle kurulur, MEtin/hizalama dosyaları `glob` ile tam anahtar üzerinden bulunur. Doğrulama: `uret.py k2-62` ve `uret.py k2-65` → 6 analiz bölümü + özet, `--dogrula` 0 HATA.
- **Önleme:** Yeni bir betik yazarken **üç kimliği** ayrı tut: (a) sesli ders anahtarı (`k2-62-…`), (b) kayıt defteri id'si (`k2-62`), (c) alt klasör adı (`meds_database_v2/ders_bilgi/k2-62`). Betik hangisini beklediğini kullanım satırında yazsın; karşılaştırma ve dosya yolu **aynı** biçimden kurulsun. "kayıt defterinde yok" hatası görüldüğünde önce anahtarın hangi biçimde olduğu ve dizinin gerçek adı kontrol edilir, kayıt defterine madde eklenmez.

### H571 — Ders içerik paketinde kısaltmaların hepsi `adim: 0` kaldı: `sayfalar.json` yedeği hiç çalışmadı (2026-11-13, k2-65 ders içerik paketi)
- **Kalıcı çözüm:** Koşul `if not sayfa or not isinstance(sayfa, dict)` yapıldı: taslak dosyası yoksa ya da boşsa ders klasöründeki düz metin `sayfalar.json` okunur. Yeniden üretimde eşlenemeyen kayıt 33 → 0, kapı 0 HATA; kısaltmalar doğru sayfaya bağlandı (`BDH`→2, `GİA`→2, `CRP`→9, `BT`→15, `MRG`→15, `MCA`→17, `TND`→23, `TPA`→23, `İV`→25).
- **Önleme:** Bir yedek/ikinci kaynak yolu yazarken "dosya var mı" ile "içerik boş mu" ayrı sınanır — boş varsayılan (`{}`/`[]`) yedeği **atlatır**, `isinstance` kontrolü bunu yakalamaz. Kapı çıktısında `adim eşlenemeyen %N` görülürse önce kaynak dosyanın gerçekten okunduğu (`J(sp)` sonrası `len(sayfa)`), sonra hangi kayıt türünün 0 kaldığı (bu turda yalnız `kisaltmalar`) kontrol edilir; kapı 0 HATA verse bile paket körü körüne kabul edilmez.

### H572 — Soru dışa aktarıcı çöküyordu ("sayfayı yenile"); PDF'te logo alt bilgiyle üst üste biniyor, alt bilgi/başlık kesiliyor, ızgarada soru kayboluyordu (2026-11-14, kullanıcı bildirdi)
- **Kalıcı çözüm:** (1) Palet erişimi tek yere alındı: `paletRenkleri` tanınmayan değeri Canlı'ya düşürür, `paletNormal` ile `ayarNormal` paleti doğrular; `renkHaritasi` boş palette bile `a.vurgu`ya düşer. (2) `baslikYukMm(a, var)` ve `altYukMm(a)` gerçek yüksekliği hesaplar (logo 10 mm üstü + alt başlık payı; alt bilgi iki satır); `govde()` ve CSS `min-height` aynı ölçüyü kullanır. DOCX (`baslikTablo`, `sectPr` üst/alt marj) ve PPTX (başlık kutusu, alt bilgi kutusu) aynı fonksiyonlara bağlandı. (3) Alt bilgi iki satıra kadar sarar (line-clamp), başlık iki satıra kadar sarar, kapak `justify-content:center` taşması `overflow:auto` ile güvene alındı, çerçevesiz kapağa 8 mm iç boşluk verildi. (4) **Izgarada sığmayan soru kırpılmıyor**: ızgaradan çıkarılıp belgenin sonunda tam genişlik "Sığmayan sorular" akış koridoruna yerleştirilir (`zorunluAkis`); tamamen boş kalan ızgara sayfası hiç üretilmez; önizleme uyarısı "kırpıldı" yerine "ayrı sayfaya alındı" der.
- **Önleme:** (a) `PALETLER[...]` doğrudan indekslenmez; her yerde `paletRenkleri`/`paletNormal` kullanılır. (b) Sayfa geometrisinde sabit mm **yalnız** kullanıcıdan bağımsız ögeler için; logo, alt başlık, alt metin gibi kullanıcı ayarlarına bağlı yükseklikler `baslikYukMm`/`altYukMm`den gelir ve HTML/DOCX/PPTX aynı fonksiyonu çağırır (üç çıktı ayrışmaz). (c) `overflow:hidden` bir soru/çözüm kutusunda **kırpma** anlamına gelir; ızgarada sığmayan blok taşınmalı (ayrı akış), kırpılmamalı. (d) Yeni bir palet/kapak/başlık seçeneği eklerken "en büyük değer" ile ölçüm yapılır (logo 24 mm, alt bilgi en uzun metin, 40 mm not alanı); yalnız varsayılan değerle bakmak hatayı gizler. (e) Kullanıcı "sayfayı yenile" ekranı bildirdiğinde ilk bakılacak yer canlı `data/istemci_hatalari.jsonl` (Oracle: `docker exec meds-app`), çünkü o ekranı üreten gerçek yığın orada ve `?adres=` alanı hangi sayfa olduğunu söyler.

### H573 — "Sayfayı yenile" ekranı yenilemeyi öneriyor ama kurtarmıyordu: eski kabuk + eksik parça döngüsü (2026-11-14, H572 ile aynı tur)
- **Kalıcı çözüm:** `main.tsx`'te tek bir `kabukOnbelleginiTazele()`: (1) bekleyen/indirilen service worker'ı `SKIP_WAITING` ile etkinleştirir ve `update()` dener, (2) çevrimdışı ders/PDF paketleri **korunarak** kabuk ve sürümsüz çalışma zamanı kopyalarını önbellekten siler. Hata sınırı ve `vite:preloadError` yolunda yenilemeden **önce** bu çalışır; iki yol da aynı 8 sn döngü sınırını paylaşır ve `vite:preloadError` artık `event.preventDefault()` ile Vite'ın kendi reload'uyla çakışmaz.
- **Önleme:** Bayat kabuk + eksik parça hatasında çözüm "reload" değil "önce önbelleği tazele, sonra yükle"dir; önbellek temizliği çevrimdışı içerik paketlerine dokunmaz (`canli-ders|pdf-offline|paket|bekleyen|paylasim` korunur). `preloadError` dinleyicisine dokunulursa `preventDefault()` korunur; kaldırılırsa iki reload yarışır ve döngü sınırı işlemez.

### H574 — Oyun masasında 13 kez çökme: `oyuncu.cezalar` olmayan eski oyun durumu (2026-11-14, kullanıcı "bu tarz hataları da çöz" dedi)
- **Kalıcı çözüm:** `Array.isArray(oyuncular)` önce sınanır, `cezalar` alanı `Array.isArray` ile doğrulanır; `MasaSonuc` (`satirlar`, `s.cezalar`), `okey/Rakipler` ve `okey/OkeyMasa` aynı korumaya alındı.
- **Önleme:** `?.` **alan** korur, **dizi metotlarını** korumaz: `X.filter(...)` öncesi `Array.isArray(X)` sınanır. Sunucudan gelen oyun durumu eski biçimli olabileceği için istemci her dizi alanını varsaymak yerine doğrular.

### H575 — "PDF'te alt kısımda soru/şık metni kesik kalıyor" bildirimi H572 sonrası da geldi: sıfır boşluklu sayfa geometrisi baskı kaymasına karşı savunmasız (2026-11-15, kullanıcı bildirdi)
- **Kalıcı çözüm:** `ayar.ts`'e `BASKI_PAY_MM = 1.2` eklendi; `govde()` gövde yüksekliğinden bu baskı toleransını düşer. Baskı tarafındaki küçük artışlar payı yer; metin asla kırpılma sınırına değmez. Önizleme aynı fonksiyonu kullandığından üç çıktı (HTML/PDF, DOCX, PPTX) ayrışmaz.
- **Önleme:** (a) "Tam dolu sayfa + `overflow:hidden`" kombinasyonu kırpma demektir; sabit ölçülü her gövde baskı toleransı taşır. (b) Bu sınıf hatayı sınama yöntemi: canlı sayfada gerçek indirme akışı → ihracat HTML'ini yakala → bağımsız Chrome'da bas → `pdftotext` boşluksuz karşılaştırma + `-bbox` ile alt kenara yapışık sözcük taraması; ekranda "önbellek/eski sayfa" tuzağına düşmeden kullanıcı akışının birebir aynısı budur. (c) pdftotext eşleşmesinde boşluklar ve madde imleri biçimden geldiği için karşılaştırma her zaman `\s` temizlenmiş metinle yapılır; sıralı karşılaştırma sırası kolon yerleşimiyle değişebilir, "eksik" sanmadan tam metinde aranır.

### H576 — "PDF'te alt bilgi (sayfa numaralı satır) diğer metnin üstünü kapatıyor": sayfa kutusu kâğıttan kısa basılmıyordu (2026-11-15, kullanıcı bildirdi)
- **Kalıcı çözüm:** `belge.ts` CSS'inde `.pg` ve `.yp` yüksekliği kâğıttan **0,25 mm kısa** basılır. Kutu her koşulda kâğıda sığar; parçalama (ve üstüne basma) yapısal olarak olanaksızlaşır. 0,25 mm boşluk `govde()`'nin 1,2 mm'lik `BASKI_PAY_MM` toleransı içinde olduğundan içerik kırpılmaz.
- **KALICI ÇÖZÜM 3 (asıl düzeltme):** Render konteynerine **`fonts-liberation`** (Liberation Serif/Sans/Mono) eklendi (`deploy/oracle/Dockerfile.oracle`). Liberation ailesi Times New Roman/Arial/Courier New ile **metrik uyumludur**; yığın artık DejaVu yerine Liberation Serif'e düşer ve sunucu basımı, kullanıcının tarayıcısının Times New Roman ölçümüyle **aynı yüksekliği** verir → taşma/kesilme yok. Doğrulama: Oracle konteynerinde `fc-match "Times New Roman"` → Liberation Serif; canlı `/api/pdf/render` PDF'i `pdffonts` ile `LiberationSerif` gömüyor (eskiden DejaVu). Canlı konteyner anında yamalandı (`apt-get install fonts-liberation` + `fc-cache`), imaj yeniden derlemesi kalıcı kılar (`Dockerfile.oracle` değişince `deploy-code.sh` imajı yeniden kurar).
- **Önleme:** (a) **İstemcide ölçülüp sunucuda basılan her belgede ölçüm yazı tipi ile basım yazı tipi AYNI aileye düşmelidir.** Render ortamına yazı tipi eklerken/çıkarırken `fc-match` ile yığının gerçekte hangi dosyaya düştüğü denetlenir; metrik uyumlu aile (Liberation↔MS core) şarttır. Yeni bir yazı tipi seçeneği eklenince hem istemcide (web font / sistem) hem Oracle konteynerinde karşılığı bulunmalı. (b) Yerel sınama konteynerle aynı yazı tiplerini kullandığından bu sınıf hatayı GİZLER; PDF düzeni hatalarında önce `docker exec meds-app fc-match "<yığının ilk adı>"` ve çıktı PDF'inde `pdffonts` bakılır. (c) Sabit yükseklikli kutuyla kurulan yazdırılabilir belgede native `window.print()` kullanıcının kenar boşluğuna bağımlıdır; deterministik çıktı için hep sunucu PDF'i bastırılır.
- **Önleme:** Sabit sayfa kutusu (`height: kâğıt ölçüsü`) + `break-after:page` kombinasyonunda kutu asla kâğıda eşit ölçülmez; "eşit" ölçü yuvarlamada "büyük" demektir ve Chrome bunu sonraki sayfaya taşıyarak çözer. Bu sınıfın sınaması: ihracat HTML'i bağımsız Chrome'da basılır, `.pg` sayısı ile PDF sayfa sayısı ve sayfa başına alt bilgi metni karşılaştırılır; sayfa sayıları eşit olsa bile parçalama sayfa sayısını değiştirmeden üstüne basabildiğinden kesin kanıt için kutu yüksekliği kâğıttan kısa tutulmalıdır.

### H572 — Etiketleri görselin içinde olan slayt şeması "resim" sayılmıyordu: lazer sayfaya düşüyor, üstüne çizim yapılamıyordu (2026-11-15, k2-65 s.40)
- **Kalıcı çözüm:** `sekil_isareti`, zemin yedeği de yoksa ve sayfa yazısının neredeyse **tümü** en büyük görsel kutusunun
  içindeyse (dışarıda ≤3 kelime, sayfa ≤24 kelime) o kutuyu şekil kabul eder. `cizim_uret.dok_uret` de `tekil_resim`
  boşken sayfadaki görsel kutularını döküme çizer (R# numarası doğrulayıcının beklediği sıra).
- **Önleme kuralı:** "İçinde çok yazı var" tek başına zemin göstergesi DEĞİL; ayırt edici ölçüt yazının **nerede** olduğudur
  (kutunun dışında kalan kelime sayısı). Yeni bir görsel/görsel-içi-etiket slaytı eklendiğinde: `sekil_isareti` çıktısı
  `t: resim` olmalı, dökümde `R#` satırı bulunmalı; bulunmuyorsa şablon zemin değil şema kabul edilir. Kapı gevşetilmez.
