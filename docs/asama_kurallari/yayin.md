# Aşama kuralları — yayin

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/tam_hat/kural_secici.py`. 51 madde. Ayrıntı gerekirse madde başlığıyla defterde aç.

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

### H32 — Zorluk parça içinde yuvarlanınca ders toplamı hedefin altında kalıyordu (2026-10-23 K2 provası)
- 6 parçanın 6'sı ücretsiz katmanda geçti ama birleştirme "zor %9 (hedef %15–25)" ile durdu: 3 soruluk parçada %20 zor → 0.
- Düzeltme: `_spot.zorluk_dagit` zorluğu ders düzeyinde dağıtıp parçalara dilimler; parça kapısı zor soruda plandan eksiği kabul etmez.

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

### H37 — Oracle'da yayın/işaret yazamıyordu: sahiplik (2026-10-24)
- 16 Ekim'den beri hiçbir ders yayınlanamıyordu: `src/data` uid 1000 (`opc`, cihazdan `rsync -a` sahipliği), `data/sesli_anlatim`
  `root` (meds-app konteyneri ve `sudo rsync`); yayın ve işaret hizmetleri `ubuntu`. Düzeltme (kullanıcı onayı): `ubuntu` → `opc`
  grubu; sesli ders aktarımlarına `--chown=ubuntu:ubuntu`; `meds-ders-yayin` ve `meds-cumle-zaman` drop-in
  `ExecStartPre=+chown -R ubuntu:ubuntu data/sesli_anlatim` (konteyner root yazmaya devam eder).

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

### H56 — Yeni yayınlanan dersin PDF'i uygulamada açılmıyordu (2026-10-24, kullanıcı, k2-07)
- Deste → PDF eşlemesi (`build_deck_pdf_sources.py` → `meds_downloads/_deck_pdf_sources.json`) yalnız işçinin Drive
  taramasında (50 dk) yenileniyordu; k2-07 21:47'de yayınlandı, eşleme 21:14'tendi → ders PDF'siz. PDF sunucu diskinden
  verilir (`/api/lecture-pdf/deck/<deste>/<n>`); Drive yalnız sunucusuz yedek yoldur.
- Düzeltme: `yayinla.py` yeni ders yayınlayınca `_pdf_eslesme_yenile()` → işçi kapsayıcısında `izle.pdf_eslesme_guncelle()`
  (günlükte "PDF eşleşmesi: yenilendi"). Kapı: yayından sonra `/api/lecture-pdf/deck/<deste>/0` 200 dönmeli.
- `.medspak` öğrenci paketi PDF taşımaz (tasarım: `ek` yalnız `--ekler` yönetici dışa aktarımında); uygulama PDF'i paketten değil sunucudan açar.

### H62 — Quiz Üretiminde Öncelik Sırasının İhlali, Çifte Analiz Maliyeti ve Yarış Durumu Hatası (2026-10-26)
- **Çözüm & Kural:**
  1. **Öncelik Kilidi (Priority Lock):** Sesli Ders (Audio Lesson) `COMPLETED` (onaylı `konusma_v2.json` ve 0 HATA denetim) durumuna geçmeden Quiz soru üretim ajanları KESİNLİKLE tetiklenemez.
  2. **Kapsam Kilidi (Scope Lock):** Quiz üretimi şimdilik YALNIZCA `Farmakoloji` (`Tıbbi Farmakoloji`) dersi için aktiftir. Kod altyapısı ders-bağımsız (`course-agnostic`) kurulmuştur.
  3. **Single Source of Truth:** Sesli dersin ilk analiz adımında üretilen `atomik_bilgi_envanteri.json`, hem Sesli Dersi hem de ardından çalışacak Quiz Ajanını besler. İkinci bir LLM analizi yapılmaz; mükerrer araştırma yasaktır.
  4. **2x Çapraz Sorgulama ve Batch Processing:** $N$ atomik bilgi $\rightarrow$ en az $2N$ soru. Token limitine takılmamak için en fazla 25 atom (50 soru) partileri halinde döngüyle işlenir.
- **Kapı:** `meds/scripts/quiz_motoru/quiz_dogrula.py` (Öncelik kilidi, 2x soru kuralı, 5-15 sn okunma süresi, gerekçeli şık açıklamaları, sıfır halüsinasyon). Çıkış kod 0 olmadan yayın yapılamaz.


### H65 — Tablo sayfasında tabloyu anlatmayan cümleye şekil/tablo çapası (2026-10-26, k2-23 cinsel kimlik)
- **Çözüm / kural:** Şekil/tablo çapası yalnız görseli/satırı gerçekten anlatan cümleye yazılır; paragrafın sonraki cümlelerine kopyalanmaz. Tablo çapalı cümlede `satir` boşsa çapa yazılmaz. Düzeltme: o cümlenin `sekil`'i `null` yapıldı, `tablo` kaldırıldı (capa + v2 + taslak kopyaları, `sekil_cizim.py sus` ile aynı yöntem); kapı gevşetilmedi, yayın 0 HATA ile tamamlandı.


### H69 — `cikmis_baglantilari.json` liste yerine nesne sarmalayıcısıyla yazıldı (2026-10-26, k2-46 sempatomimetikler)
- **Çözüm / kural:** `cikmis_baglantilari.json` daima kökte bir liste (`[{"soru_id": ..., "soru": ..., "ilgili": bool, "aciklama": ...}]`) olarak yazılır. `denetle.py` ve `arsiv_yayinla.py` doğrudan liste formatı bekler. Dosya düzeltildi, 0 HATA ile Oracle'a dağıtıldı.


### H70 — Mekanik 2 Cümlelik Şablon ve Yüzeysel Anlatım Yasağı (Sıfır Bilgi Kaybı ve Amfi Derinliği Standardı) (2026-10-26, k2-48 lokal anestezikler)
- **Çözüm / kural:** Sayfa başına yüzeysel 2 cümlelik kopyala-yapıştır şablonlar KESİNLİKLE YASAKTIR. Her slayt için amfi ders notundaki tüm maddeleri, tabloları, spesifik ilaç isimlerini, maksimum dozları ve patofizyolojik mekanizmaları kapsayan 3 ila 6 zengin cümle yazılmalıdır (35–70 slaytlık dersler için 140–250+ cümle, ~2000–3500 kelime, 15–25 dakika anlatım derinliği). K48 bu standartla baştan üretildi (144 cümle, 2438 kelime, 68 atomik bilgi, 10/10 çizim, 6.23 MB .medspak) ve 0 HATA ile Oracle canlı ortamına alındı.



### H73 — `terim/` klasörü dağıtım betiğinin veri listesinde yoktu; terim dosyaları canlıya ulaşamıyordu (2026-10-26)
- **Çözüm / kural:** Listeye `terim` eklendi. `data/sesli_anlatim` altına yeni bir veri türü ekleyen her oturum, `deploy-code.sh` [1b] listesini de günceller; dağıtımdan sonra canlı API yanıtında alanın varlığı `curl` ile doğrulanır.


### H75 — Gündelik Türkçe sözcükler terim diye işaretlenmişti (2026-10-26, tüm dersler)
- **Kalıcı çözüm:** `terim_sozlugu.py ayikla [--yaz]` bütün terim dosyalarını (canlı + arşiv) tarayıp kapının reddettiği ögeleri çıkarır; terimi kalmayan sayfa/dosya kaydı silinir (hiçbir dosyada boş `t` dizisi bulunmaz). Bu turda 514 öge ayıklandı, kapı gevşetilmedi.
- **Önleme kuralı:** Terim kapısı kuralı değiştiğinde yalnız yeni dosya değil, **tüm mevcut dosyalar** yeni kuralla yeniden taranır (`ayikla`), sonuç canlıya dağıtılır.


### H77 — Kısaltma katmanı eklenirken üç ayrı tuzak: büyük harfli Türkçe sözcük, tireyle bitişik yazım, dağıtım listesi (2026-10-26, Kurul 2 · 60 ders)
- **Çözüm / kural:**
  1. `kisaltma_mi()` artık `/usr/share/hunspell/tr_TR.dic` köklerini (ek soyma ile) kullanır: sözlükte bulunan büyük harfli sözcük kısaltma sayılmaz. Bilinen/elle sözlükte (`kisaltma_bilinen.json`, `kisaltma_elle/`) açıkça tanımlı kısaltmalar (SAK, KS gibi Türkçe sözcüğe benzeyenler) bu filtreden muaftır.
  2. `kutular()` eklendi: tam eşleşme yoksa kısaltma, kelime içinde **önek/sonek sınırı** denetlenerek (ör. "o5-httlpr", "t12-l1", "dsm-iii-r", "gabaa-reseptor") karakter oranıyla daraltılmış kutuda işaretlenir. Kapı gevşetilmedi; yalnız doğru konum hesaplandı.
  3. Dağıtım listesine `kisaltma` eklendi; canlı API'de `kisaltma` alanı `curl` ile doğrulandı.
- **Önleme kuralı:** (i) Her yeni veri türü hem `canliDers.ts` yol tanımına hem `deploy-code.sh` [1b] listesine yazılır. (ii) Kısaltma/açılım **yalnız dersin kendi metninden ya da elle/bilinen sözlükten** alınır; metinde açılımı olmayan kısaltmaya tahminle açılım yazılmaz (yanlış açılım, eksik açılımdan kötüdür).


### H78 — Gece otomatik LLM hattı kullanıcının Claude limitini tüketti; Oracle ders işçisi manuel moda geçişin dışında kalmıştı (2026-10-27)
- **Çözüm:** Oracle işçisi durduruldu (`restart=no`, ayar duraklat/otomatik kapalı/günlük 0), `.env` anahtarı `#KAPALI`;
  `meds-hat-gece`, `meds-olasi-soru` maskelendi; `otomasyon/llm_kilit.py` (MEDS_LLM_ELLE=1 yoksa çıkış 75, systemd altında
  panel bayrağı şart) 11 betiğe ve `yonlendir._claude/_ajan`'a bağlandı; Gemini onarım işçisi duraklatılmış başlar, Faz14
  kuyruğu yalnız `POST /api/admin/faz14-kuyruk/baslat` ile.
- **Önleme kuralı (AGENTS.md kural 20):** "kapat" kararı her makinede (yerel + Oracle konteyner ayarları + `.env` anahtarları)
  ayrı ayrı doğrulanır; yeni LLM betiği kilitsiz yazılmaz; zamanlayıcı/izleyici/setInterval ile LLM çağrısı yasak.


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


### H85 — Çizim önemli bölgeyi örtüyor, zoom yanlış/fazla, kelime ↔ kelime oku okumayı bozuyor (2026-10-27, kullanıcı bildirdi)
- **Çözüm:** kontur %8 dışa açılır, hale yok, dolgu %13 bulanık, karartma %10, kalınlık bölgeye göre 1–2,4 px; akış yalnız
  resim çiziminde (`yakin`); zoom ≤1,6×, ≥1,25× gerekmezse yok, bölge ≤%20; tabloda çizim yok (yalnız marker). Üretici
  (`cizim_uret.yakinlasma`) yalnız resimde ve ≤%20; kapı K10–K12; standart `KURUL2_DERS_STANDARDI.md` §4; metin takipçisi
  kapısı `takip_kapisi.py` (T1–T6).
- **Önleme kuralı:** okumayı bozan hiçbir çizim/zoom yayına girmez; yeni ders kapıları K10–K12 + `takip_kapisi.py` 0 HATA.
  Yayındaki eski derslerin verisi kapıda 36 ihlal gösteriyor; görüntüleyici aynı kuralları uygular, yeniden üretimde düzelir.


### H87 — Çizim doğrulayıcısının komut satırı Kurul 2 cümle kimliklerini ve resim kutularını tanımıyor; sarmalayıcı yanıltıcı 0 HATA verdi (2026-10-27, k2-02)
- **Çözüm / kural:** çizim için geçerli kapılar YALNIZ `cizim_uret.py` (yerleşim + doğrulama, gerçek kutu ve görüntüyle) →
  `cizim_kapisi.py` → `panel_sinama.mjs`. Parti ajanının kendi sarmalayıcı sonucu kanıt sayılmaz; reddedilen çizim
  yayına girmez (emin olunmayan yer çizilmez). CLI düzeltmesi açık iş.


### H88 — Drive klasör adı değişince yayın PDF'in kaynak kimliğini bulamadı (2026-10-27, k2-03)
- **Çözüm / kural:** sunucu ve deneme kipi `kaynak_kimligi_esnek` kullanır; esnek eşleme klasör farkını yok sayıp `Kurul N/<branş>/`
  sonrası yol manifestte tekse onu kabul eder. Yayın denetim hatasında taslağın `yayin.json`'u silinip yeniden onaylanır.


### H90 — Anlam denetimi önbellek anahtarı değişince denetim sessizce atlandı (2026-10-27, k2-02)
- **Çözüm / kural:** elle üretimde her yerleşimden sonra `rapor.anlam_denetimi.bakilan` panel sayısına eşit olmalı; değilse kararlar
  yeni girdi anahtarına (sıra korunarak) eşlenir ya da denetim yeniden yapılır. `bakilan: 0` ile çizim yayına girmez.


### H91 — Çizim PDF'i önbellekte olmayınca bütün konturlar sessizce reddedildi (2026-10-27, k2-03/k2-04)
- **Çözüm:** ikisine de aynı yedek yol (indirme klasörü → `pdf_isaret.pdf_indir`); `cizim_uret` PDF hiç bulunamazsa durur.
- **Önleme kuralı:** bir hattaki bütün betikler kaynak dosyayı aynı yardımcıyla bulur; ret sayacında tek bir nedenin tüm komutları
  ataması (ör. "görüntü yok" = kontur sayısı) kapı hatası sayılır, yayına geçilmez.


### H93 — Çapa değişince PDF işareti yenilenmedi (2026-10-27, k2-04)
- **Çözüm/kural:** çapa Oracle'a yüklendikten sonra `pdf_isaret.py --key <key> --zorla` çalıştırılır, ardından `takip_kapisi.py --api` 0 HATA.


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


### H97 — Dağıtım, yeni sesli ders metnini git'teki eski sürümle geri aldı; ses eski metinle üretildi (2026-10-27, k2-03/k2-04)
- **Kural:** yeni metin + v2 + vurgu + hizalama önce commit/push, sonra ders-ekle; ses tamamlanınca eski metne ait varyantlar silinir (`DELETE /api/sesli-anlatim/ses/<key>/<vid>`); `kayit.json` süre/özet ve `takip_kapisi --api` ile doğrulanır.


### H99 — Dağıtım sunucu servis değişikliğini "yalnız ön yüz" sandı; yeni data dosyası Oracle'a gitmedi (2026-10-27, sınama)
- **Kural:** sunucu kodu değişen dağıtımdan sonra `curl` ile yeni davranış doğrulanır; gerekirse `docker restart meds-app` ve sağlık kontrolü. Yeni `data/*.json` dosyası Oracle'a elle (`scp` + `sudo cp`) kopyalanıp canlıda okunduğu doğrulanır.


### H105 · Harita `adimlar` = deste `slideNumber` (checkpoint dahil); iskelet ajanı içerik adımlarını 1..N saydı (2026-10-27, k2-08)
- **Çözüm:** Deste birleştirildikten sonra haritadaki k. içerik adımı → k. içerik slaytının slideNumber'ına çevrildi (sayfa kayıtları ve ana başlık aralıkları).
- **Kural:** Harita deste birleşmeden planlı sayıyla yazılır; birleştirmeden sonra slideNumber'a çevrilir ve `denetle.py` yeniden çalıştırılır (TALIMAT §1b'ye not eklendi).


### H116 · Birleştiriciler yeni ders eklerken branştaki eski dersin dosyalarını da yeniden yazıyor (2026-10-27, k2-05 Nörolojik Muayene)
- **Kural:** elle zincirde her birleştirmeden sonra `git diff --stat`; yalnız yeni dersin dosyaları ve indeksteki yeni ders satırı sahnelenir;
  eski dersin dosyaları `git checkout` ile geri alınır, indekste eski ders satırı HEAD'den korunur (bilerek yapılan toplu yenileme hariç).


### H119 · Örnek sorularda öznel/ders çağrıştıran kök ve rastgele slayt sorusu (2026-10-27)
- **Kural:** Kök bağımsız ve çıkmış-benzeri kalıpta; ders/slayt/bölüm göndermesi yok; her soru kazanım–konu bağlı, tıbbi ve sınav değerli. Kaynak: `TALIMAT.md` §4, `TALIMAT_ONEM.md`, `KURUL2_DERS_STANDARDI.md` §10.9.



### H109 · Aynı cihazda iki sekme açıkken profil eşitleme fırtınası (2026-10-28)
- **Çözüm:** `ORIGIN` cihaz düzeyinde (`medsoru_sync_origin_v1`), son gönderilen parmak izi `localStorage`'da (`medsoru_sync_fp_v1`); ikisi de eşitleme izin listesinde değil. Sınama: iki yeni kodlu sekmede ikinci sekme açılınca ilk sekme 25 sn'de 1 not çekme + 1 yedek (önce 55 istek).
- **Kural:** Sekmeler arası ortak olan duruma (localStorage) bağlı karar verilerini sekme belleğinde tutma; yayın kaynağı kimliği cihaz düzeyinde olmalı. Sınamada eski kodlu açık sekmeleri kapat (yeni/eski sürüm karışımı ölçümü bozar).


### H127 — Yıldızlı paragraflar: Bugün'de yok, silinen geri geliyor, sesli derste tüm dersler listeleniyor (2026-10-28)
- **Çözüm/kural:** Bugün'e kurul→ders→konu gruplu yıldızlı paragraflar bölümü eklendi; silme artık `silindi` mezar taşıyla yazılır ve birleştirmede aynı kimlikte en yeni `tarih` kazanır; sesli ders paneli `dersKey` ile varsayılan "Bu ders" kapsamında açılır ("Tüm dersler" seçilebilir). Yeni bir kişisel liste deposu eklenirken: (a) Bugün/Listeler erişimi, (b) silme mezar taşı + en yeni kazanır birleştirmesi, (c) bağlam içinden açılan panelde bağlam süzgeci zorunludur.


### H111f · Deste kataloğu (~600 KB) her sayfada yalnız sayı için iniyordu (2026-10-28, başarım)
- **Çözüm:** `loadStats` katalog yüklüyse uzunluğunu, değilse son kayıtlı istatistiği kullanır (`isDeckCatalogLoaded`); `patchCatalog` kataloğu yüklemez, değişen girdileri ekler — `loadDeckCatalog` sonradan bunları korur (mevcut "early" birleştirmesi). /kamplar, /istatistik ölçümde katalog artık inmiyor.
- **Kural:** Yalnız sayı/özet için büyük veri modülü tembel yüklenmez; özet meta veride tutulur. Canlı yama işlevleri ana veriyi zorla yüklemez, yüklemeyi bekleyen birleştirmeye bırakır.


### H148 — Ders çalış merkezinde "hepsini bitirdin ya da henüz ders yok" ikili mesajı (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Kurulda ders var ve hepsi bitti → "hepsini bitirdin" + tüm dersler bağlantısı; ders yok → "henüz eklenmedi" + önceki kurula geçiş. Boş durum metni iki ayrı durumu tek cümlede birleştirmez, bir eylem verir.


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

### H340–H347, H360–H374 — Sayfa denetimi düşük önemli bulgular (2026-10-28)
- **Kural:** Tehlikeli işlem ad kalıbıyla değil açık listeyle belirlenir (H182, H372). Açık çekmece/sekme adreste tutulur ki yenileme ve paylaşım aynı görünümü açsın.
- Açık öneriler (yapı): menü/başlık ad eşleşmeleri, `kurul_2` adres biçimi, yinelenen girişler (KMB, Sözlük/Hastalıklar, takvim), havuz dondurmanın Bayraklar'a taşınması, ses kuyruğunun sesli ders sekmesi olması, sürüm notu + dağıtım bilgisinin birleşmesi. Veri: kazanımlarda yinelenen konu 31, soru haritası 498 / çıkmış 502 farkı.


### H390–H392 — Veri tutarlılığı: yıldız işaretleri, soru haritası sayımı, deste kurul adları, yinelenen kazanım konuları (2026-10-28, kullanıcı onayıyla)
- **H390 Belirti:** Deneme ekranında soru/şık metninde `**değildir**`, `**Soru:**` ham görünüyordu. **Kök neden:** veri doğru (kasıtlı vurgu; çıkmışta 49 soru, Öğren klinik karar vakalarında 414 öge), `PracticeV15` metni işlemeden yazıyordu. **Çözüm:** `**…**` kalın yazıya çevrilir; veri değişmedi.
- **H391 Belirti:** Soru haritası Kurul 2'de 498, çıkmış sayfası 571+ gösteriyordu. **Kök neden:** 178 çıkmış soruda `isPastExam` alanı yok (kaynakları çıkmış PDF'leri); harita betiği yalnız `true` olanları sayıyordu. **Çözüm:** `scripts/v15/soru_haritasi.py` yalnız açıkça false ve gizli soruları dışlar; harita yeniden üretildi (K2 574).
- **H392a Deste kurul adları:** Kurul 1 için 12 yazım vardı; boş/"Ürogenital Sistem Komitesi" yazılı 4 deste öğrenci tarafında "Diğer"e düşüyordu. 74 destenin `committee` alanı "Kurul 1 - Ürogenital ve Obstetrik Kurulu" yapıldı (kaynak `interactive_learning_decks.json`, biçim birebir korundu; doğrulayıcı 0 HATA, paketler yeniden üretildi).
- **H392b Kazanım konu çiftleri:** Aynı dersin kesik/tam başlıklı iki kazanım kümesi (7 çift: K1 Genetik, K1 Üroloji ÜSE, K5 Demir, K5 Spondilodiskit, K6 Histamin, K6 Yaşlılıkta beslenme, K6 Biyokimya) tam başlıkta birleştirildi; yalnız birebir aynı 13 kazanım atıldı, kimlikleri taşındı (kazanım soruları, sınav çalışması, müfredat paketi, eşleme dizini byDeck yeniden üretildi; artık başvuru 0), slayt kanıtları birleşti. 25 konu başlığından hoca adı / "UZM." eki temizlendi. Ders kayıt defterine (`dersler/kN.json`) dokunulmadı: K5/K6 çiftleri orada iki ayrı ders kimliğidir (kural: kimlikler kalıcı). Betik: oturum yedeğiyle `kz/birlestir.py`.
- **Tuzaklar:** (1) `lite/`, `questions/`, `pastQuestions.json`, `sinav_calisma_k*.json` git dışıdır; dağıtım temiz `meds-dagitim` ağacından derler, bu dosyaların güncel kopyası oraya elle konmazsa canlı derleme eski veriyi gömer. (2) Çıkmışların canlı asıl kopyası Oracle `data/pastQuestions.json`'dır (sunucu bellekte tutup üzerine yazar); yerel `src/data/pastQuestions.json` yalnız yansıdır. Canlı çıkmış konu/kimlik güncellemesi ayrı, sunucu uçlarıyla yapılmalı (yapılmadı, açık).

### H393 — Canlı çıkmışlarda kazanım birleştirmesinden kalan eski konu adları / kimlikler (2026-10-28, kullanıcı onayıyla)
- **Çözüm:** Yeni yönetim ucu `POST /api/admin/sorular/cikmis/esleme-uygula` (varsayılan önizleme; `uygula:true, onay:"ESLE"` ile tam yedek `data/_yedek/pastQuestions.esleme-oncesi.<zaman>.json` + değişim dosyası `data/_yedek/cikmis_esleme_<zaman>.json`, sunucunun kendi kaydetme/yansıtma/canlı olay yolu, denetim kaydı) ve `POST …/esleme-geri {dosya, onay:"GERI"}`. Geçmiş kayıtlar (`checkSolveOriginal`, `eskiSurum`, `phase14Original`, revizyonlar) atlanır. Yerelde önizle→uygula→geri al denendi, yerel dosya birebir geri yüklendi; canlıda önizleme 56 soru/57 değer (plan ile aynı) → uygulandı, diskte kalan 0, geçmiş kayıtlardaki 82 değer dokunulmadan. Canlı değişim dosyası: `cikmis_esleme_2026-10-28T17-37-02-423Z.json`.
- **Kural:** Canlı çıkmış verisinde toplu değişiklik yalnız sunucu içinden, önizlemeli ve geri alınabilir yolla yapılır; geçmiş kayıt alanlarına toplu değiştirmede dokunulmaz.


### H400–H406, H420–H424 — Yapı sadeleştirme: yinelenen sayfa ve girişler (2026-10-28, kullanıcı kararı)
- **Kural:** Aynı işi gören ikinci giriş/sayfa açılmaz; birleştirmede bileşen silinmez (yönlendirme + menüden kaldırma), eski adres yeni yere yönlenir ve SITE_HARITASI_KURALLARI.md'ye yazılır.

### H431 — Kişi 360° › Etkinlik sekmesi hep "Olay yok" gösteriyordu (2026-10-28, kullanıcı bildirdi)
- **Çözüm/kural:** Uç nokta ilk sayfada ziyaretleri `kind:'page'` olay olarak birleştirir (Tümü 100, Sayfa süzgeci 300). Yeni bir olay kaynağı eklenince yönetim ekranının o kaynağı gerçekten okuduğu canlı veriyle doğrulanır.


### H435 — Sıralama: ölçü değişince eski veri yanlış birimle görünüyor, tepki geç (2026-10-29)
- **Çözüm/önleme:** yanıt istek anahtarını taşır (`anahtar`), yalnız güncel anahtarla eşleşen yanıt çizilir, yoksa iskelet; sayfa ömürlü önbellek + eşzamanlı istek birleştirme + diğer ölçülerin arka planda önden yüklenmesi; SSE değişiminde önbellek temizlenir. Kural: süzgeçli listede yanıt, isteğin anahtarıyla etiketlenmeden ekrana basılmaz.


### H437 — Çevrimdışı indirme "sırada" takılıyor, her açılışta uygulama dosyası iniyor (2026-10-29)
- **Çözüm:** bekleme yalnız uçuşan ön plan isteğine ve en çok 2 sn; uygulama paketi yalnız cihazda yokken içerikle birlikte başa, güncellemesi yalnız çevrimdışı mod + otomatik güncelleme açıkken kuyruğun sonuna.
- **Önleme:** arka plan indirmesinde dosya başına bekleme süresi toplam süreyi paket boyuyla çarpar — bekleme paket başına değil dosya başınaysa üst sınır saniyeler düzeyinde tutulur; sürüm değişimi her dağıtımda olan bir paket kuyruğun önüne zorla alınmaz.


### H441 — Sesli ders listesi (`/api/canli-ders`) canlıda her açılışta 1,2 sn (2026-10-29)
- **Çözüm:** salt okunur kayıt defterleri için boyut+mtime önbellekli `okuSabit` (dersler, dersBul, varyantlar, sinamaKonfig, branş kaydı). Dört sorgu biçiminde çıktı önce/sonra bayt bayt aynı; yerelde 270–380 ms → 4 ms.
- **Önleme:** İstek başına döngü içinde dosya okuyup ayrıştırma yapılmaz; değişmeyen kayıt defteri bir kez okunur, imza (boyut+mtime) değişince tazelenir. Önbellekten dönen nesne değiştirilmez (yazan kod taze `oku` kullanır). Yeni liste ucu eklerken Oracle içinden `curl -w %{time_total}` ile ölçülür (hedef < 50 ms).


### H446 — Öğrencinin en çok çalıştığı ve çıkmışta sorulan bilgi anlatımda "ders yalnız adıyla sayar" diye geçiştirildi (2026-10-30)
- **Kural:** AGENTS 28 — geçmiş yıl öğrenci önem notu (`src/data/ogrenci_onem/`, `docs/OGRENCI_ONEM/<ders>.md`) her 2026-27 dersinde zorunlu
  malzemedir: A birimi anlatımda ayrıntılı (tanım → ayırt edici nokta → sayı/ölçüt → komşu kavram), önem listesinde `ogrenci` etiketli
  madde, ≥2 örnek soru; B birimi anlatımda açık + ≥1 soru. Slaytta yalnız adı geçen kavram, notta/çıkmışta tanımı soruluyorsa tanımıyla anlatılır.
- **Önleme:** "ders yalnız adını verir / yalnız adlarıyla sayar" türü geçiştirme, kavram öğrenci notunda ya da çıkmışta tanımıyla geçiyorsa yasaktır.
- **Kapı:** `python3 scripts/ogrenci_onem/kapi.py <ders>` 0 HATA — bilgi düzeyinde (el notu, vurgulu satır, çıkmış önermesi) anlatım ve önem
  listesi cümlelerinde arar (vektör + kelime kökü örtüşmesi; yalnız vektör "spastisite ve rijidite" cümlesini rijidite tanımı sanıyordu).

### H447 — Metni değişen paragrafların v2 cümleleri boş kaldı, ders ekranı ve çapası o paragraflarda eksik yayında (2026-10-30)
- **Çözüm:** 9 paragraf metin değişmeden dolduruldu (eski v2'de birebir aynı kalan 17 cümle kimliğiyle geri alındı, kalanlar yeni
  kimlikle yazıldı; paragraf kimlikleri `k2-05-pNNN` biçimine döndü); `konusma_v2.py --dogrula` 0 HATA.
- **Önleme:** `klip_tasi.py` "v2: N paragraf boş" raporu verdiyse o ders, boş paragraflar `konusma_v2` biçiminde yazılıp
  `konusma_v2.py --dogrula <dizin>` (kaynak.md ile) 0 HATA verene dek dağıtılmaz; açık iş olarak not düşmek yerine aynı oturumda kapatılır.


### H448 — `klip_tasi.py` metinle birlikte düzenlenmiş v2'yi eski metne göre yeniden kurup değişen paragrafları boşaltıyordu; `ders-ekle` elle iyileştirilmiş çapayı ezdi (2026-10-30)
- **Çözüm:** `klip_tasi` cümle seslerinin birleşimi yeni paragraf metniyle aynıysa v2'ye dokunmaz. Çapa: yereldeki taşınmış çapa esas alındı,
  değişen paragraflarda değişmeyen cümleler eski çapayı (git HEAD) geri aldı, yeni cümleler satırdan `pdf_isaret.capa_maddeleri` ile madde
  dizinine çevrildi; `capa_dogrula` %98, 0 HATA; çapa Oracle'a yeniden yazıldı.
- **Önleme:** yayımlanmış dersin metni düzeltildiğinde `sesli_yayinla.py`'den SONRA yerel çapa (klip_tasi ile taşınmış + değişen paragraflar
  yazılmış) Oracle'a geri kopyalanır ve `pdf_isaret.py --key <key> --zorla` çalıştırılır (H93); `ders-ekle`'nin yazdığı kaba çapaya güvenilmez.
