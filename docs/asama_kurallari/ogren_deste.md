# Aşama kuralları — ogren_deste

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/hat/tam_hat/kural_secici.py`. 56 madde. Ayrıntı gerekirse madde başlığıyla defterde aç.

### Kurul 2 hattı için genel kural


### Sesli ders PDF/DOCX dışa aktarımı (2026-10-20)
- **Yazıyla sayı:** konuşma metni okunuş için "iki virgül bir", "yüzde kırkına" yazar; öğrenciye verilen dosyada bunlar
  "2,1", "%40'ına" olmalı. Kural tek yerde: `src/services/sayiYazim.ts` (`sayilariYaz`), dışa aktarım
  (`components/canliDers/canliDersDisaAktar.ts`) ve ekran (`canliDersStore.ts` → `sayilariDuzelt`, vurgu konumları `sayilariYazEslemeli` ile taşınır) her derste uygular. Saklanan metin değiştirilmez (ses ve cümle zamanı ona bağlı).

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
  güvenilmez. Kamp sesi (`scripts/uretim/kamp/ses.py`) süreç içi çalışır, anahtarı `kN-kamp` (K2+ uzun kısaltma yolu).
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
- **Kapı — EKLENDİ:** `scripts/uretim/sesli_anlatim/metin_denetle.py` → `DOLGU` kalıpları HATA; "Burası önemli/çok önemli/sınavda
  sık" bölüm sayısının yarısını (en az 3) aşarsa HATA; kelime alt sınırı artık yalnız uyarı. K1 metinlerine toplu müdahale yok.

### H23 — Öğrenci işaretli slayt yanlış yorumlandı + okunuşla yazılmış metin (İmmünofarmakoloji V2, kullanıcı, 2026-10-22)
- **Kural (kullanıcı tanımı):** sarı ya da mavi ÇAPRAZ şerit/çizgi = hoca okumadı (anlatılmaz); metin üzerindeki YATAY
  çizgi/vurgu = okundu; yıldız, daire, "önemli", "bil", ünlem, altı çizili = önemli. Öğrenci notlu PDF önce sayfa sayfa
  işaret dökümüne (okundu/okunmadı/önemli/el yazısı) çevrilir, metin dökümden yazılır.
- **Kural:** kısa sürüm slayt sırasını izler; önem listesinin (`src/data/<branş>_onem/`) TAMAMI ve her çıkmış konu içinde
  anlatılır; konu ne → neden/nasıl → sınav ayrıntısı sırasıyla kapanmadan geçilmez; soru dili ve şık yankısı yasak; uzunluk
  V1'in %45–65'i ("çok kısalt" diye madde atma). Yazar + bağımsız denetçi (kapsama dökümü + kaynak karşılaştırması) zorunlu.

### H31 — Hesap sorusu yanlış alarmı + iç etiketin öğrenci metnine sızması (2026-10-23 K2 provası)


### H40 — Canlı çizim çizgileri görünmüyor, amaçları anlaşılmıyordu (2026-10-24, kullanıcı ekran görüntüsü s.14 herniasyon)


### H41 — Yazı satırları arasına çizilen oklar kötüydü; tek tip panel yetmiyordu (2026-10-24, kullanıcı s.18)


### H44 — Sayfaya sığmayan panel gizleniyordu (2026-10-24, kullanıcı kararı)


### H52 — Etiket çizimden kopuk; PDF'in kendi oku yeniden çiziliyordu (2026-10-24, s.14 ve s.27 görsel denetimi)


### H55 — Görsel tablodan yanlış satır okundu; hocanın kendi çelişkisi kesin "sınav spotu" yapıldı (2026-10-24, k2-07)


### H56 — Yeni yayınlanan dersin PDF'i uygulamada açılmıyordu (2026-10-24, kullanıcı, k2-07)


### H64 — Sayfa haritası adım numaraları tekrar sayfalarını saymıyordu; kısa/eksik kanıt (2026-10-26, k2-22 psikosomatik)
- **Çözüm / kural:** Harita `adimlar`ı daima son destenin içerik slaytlarının `pdfSayfalari`ndan türetilir (checkpoint/oyun hariç); başlık `adimlar` = kapsadığı sayfaların ilk/son içerik adımı. Metinsiz görsel sayfada `kanit: {sayfa, gorsel: "≥4 kelime görülen"}` kullanılır; alıntı kaynak.md'de birebir geçen ≥4 kelime olur.


### H67 — H64 tekrarı: harita adımları checkpoint'siz sayıldı + deste `bolum` alt başlık numarası (2026-10-26, k2-26 nörolojik hastalıklar genetiği)
- **Çözüm / kural:** Harita `adimlar` daima deste `slideNumber`'ıdır; `bolum` yalnız `basliklar[].no` değerlerinden biri olur (alt başlık yoksa ana no). Kayma görülürse hangi tarafın doğru olduğu sayfa `ne_anlatiliyor` ile slayt başlığı karşılaştırılarak seçilir; içindekiler/kapak sayfası hiçbir adımın `pdfSayfalari` aralığına girmez.


### H80 — Öğrenci Drive betiği uzantısız PDF'i not saymadı; kısaltma bulucu "HT+DM" yazımını kaçırdı (2026-10-27)
- **Çözüm / kural:** Tür MIME'den de belirlenir; bölme deseni `[/\-–+]`; EP `kisaltma_bilinen.json`'a eklendi.
  `degerlendirme_dogrula.py` slayttaki her kısaltmanın sözlükte olmasını HATA ile ister.


### H95 — Yayın düzeltmesinde olmayan alan; PDF eşleyici durdurulan işçi kapsayıcısında (2026-10-27, k2-03/k2-04)
- **Önleme kuralı:** yayın betiği değişikliği Oracle'a gitmeden önce yerel taslakla `kaynak_kimligi_esnek` ve `--deneme` akışı
  çalıştırılır; yayından sonra `/api/lecture-pdf/deck/<deck>/0` 200 kontrolü zorunlu.


### H96 — Önem/çözücü zinciri ham belgede olmayan soruyu "çıkmış" diye kullandı (2026-10-27, k2-03)
- **Önleme kuralı:** zincirden sonra önem/çözücü/asistandaki her çıkmış kimliği ham belge taramasında `bulundu` ve `/tek` 200
  olmalı; değilse yayına girmez. `-rNN` türetilmiş kayıt hiçbir zaman çıkmış sayılmaz.

### H89 — Canlı yarışma odası sorusuz kuruluyor, oyun hiç başlamıyordu (2026-10-27)
- **Kural:** realtime odası veri olmadan kurulamaz; sunucu her başarısız katılımı açık hata mesajıyla döner.

### H90 — v15'te Toplu PDF penceresinin üstüne üst/alt çubuk biniyordu (2026-10-27)
- **Kural:** tam ekran örtü/pencere bileşenleri daima body'ye portal ile çizilir; sayfa içi z-index'e güvenilmez.


### H104 · Hoca ses kaydı: tek model dökümü sınav vurgularını bozuyordu; kayıt dersin ortasından başlıyordu (2026-10-27, k2-08)
- **Kural:** Sınav vurgusu tek dökümden çıkarılmaz; alıntı birebir döküm, anlaşılmayan sözcük "düzeltilerek" yazılmaz (düzeltme `not`ta); gen adı/sayı yalnız slayt ve/veya öğrenci notu ile örtüşünce vurgu olur; kaydın hangi slayttan başladığı rapora yazılır.


### H105 · Harita `adimlar` = deste `slideNumber` (checkpoint dahil); iskelet ajanı içerik adımlarını 1..N saydı (2026-10-27, k2-08)
- **Kural:** Harita deste birleşmeden planlı sayıyla yazılır; birleştirmeden sonra slideNumber'a çevrilir ve `denetle.py` yeniden çalıştırılır (TALIMAT §1b'ye not eklendi).


### H112 · İlk anlatım taslağı öğrenci denetçide KALDI: aynı sözcük iki anlamda, kilit kavram tanımsız, gen sembolü okunuşu çözülemedi (2026-10-27, k2-08)
- **Kural:** sesle okunan metinde aynı sözcük iki ayrı kavramı gösteriyorsa yazım ayrıştırılır; sayısal/ekzon gibi kavram ancak tanımından sonra kullanılır; "hoca da ... söyledi" yalnız slaytın vermediği ek bilgi ya da sınav vurgusu içerdiğinde yazılır.


### H114 · Çizim ileri-sızıntı denetimi yalnız ses metnine bakıyordu: gen sembolleri (HOX, PAX6, FGFR3) panelde reddedildi (2026-10-27, k2-08)
- **Kural:** ileri-sızıntı, öğrencinin gördüğü (ekran) ve duyduğu (ses) metnin birleşimine göre denetlenir.


### H105 · Sıralı tabloda adım atlanıyordu (k2-05, 2026-10-27)
- **Kural:** Sıra/Adım sütunlu tablolarda numaralar 1'den kesintisiz olmalı ve slayt metnindeki sayımla eşleşmeli (`docs/DERS_ICERIK_BICIMI.md`). Kapı: `scripts/uretim/ders_icerik/sira_kapisi.py`.


### H121 · Sınama (test) Öğren dersi gerçek Kurul 2 dersleriyle aynı listede görünüyordu (2026-10-27, k2-07 Genel Anestezik İlaçlar)
- **Kalıcı çözüm:** kitaplıkta `sinama` işaretli desteler ayrı "Sınama — test verisi" bölümünde, en sonda gösterilir. Önleme: yeni listeleyen her ekran `sinama` alanını bölüm ayrımı için kullanır; gerçek PDF gelince `yayinla.py` aynı kimliği günceller ve `sinama` alanını bırakır (H97/H99 sırası).


### H111f · Deste kataloğu (~600 KB) her sayfada yalnız sayı için iniyordu (2026-10-28, başarım)
- **Kural:** Yalnız sayı/özet için büyük veri modülü tembel yüklenmez; özet meta veride tutulur. Canlı yama işlevleri ana veriyi zorla yüklemez, yüklemeyi bekleyen birleştirmeye bırakır.


### H111p · Sesli derste hatalı adreste sunucu hata kodu ham gösteriliyordu (2026-10-28, Ders çalış)
- **Kural:** Sunucu hata kodu (`error` alanı) öğrenci metni değildir; ekranda bilinen hatalar Türkçe açıklamaya çevrilir, bilinmeyen hata için genel cümle kullanılır.


### H111t · Ders çalış dokunma hedefleri: "Tüm dersler" 75×14, Öğren "▶ Dinle" 52×20 px (2026-10-28, Ders çalış)
- **Kural:** H111g kuralı: görünür öğe küçük kalabilir, dokunma alanı ≥40 px.


### H111v · Ana CSS 936 KB, tam katman sayaçsız, tam ekranda fazla yükseklik, kısa başlık, küçük yazı, çevrimdışı boş istekler (2026-10-28, kabuk/başarım)
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

### H131 — Yönetim öğrenci uygulamasının ortak girişiyle açılıyordu; ayrı giriş + SW önbellek zehirlenmesi riski (2026-10-28, Yönetim v16)
- **Kalıcı çözüm:** `manage.html` + `src/manage-main.tsx` (yalnız adminFetchAuth, Firebase kimlik, palettes.ts tokenları, `styles/yonetim-temel.css`, kit, kabuk). `vite.config.ts` çoklu giriş; `server.ts` SPA geri dönüşü `/manage*` için `dist/manage.html`; geliştirmede `scripts/altyapi/vite/yonetimGirisi.ts`. Yönetici değilse (moderatör) ya da `?kabuk=v14` ise `manage-main` tam uygulamayı (`import('./main')`) yükler. Uygulama içinden /manage'e geçiş (`App.tsx yonetimGirisineGec`) tam sayfa gezinmesi yapar (10 sn döngü koruması). Ölçüm: /manage 544+152 KB → 179+5 KB gzip; tarayıcıda 191 KB aktarım, FCP 164 ms.

### H131a — `/react-dom/` eşleşmesi react-dom/server'ı her sayfanın açılış parçasına sokuyordu (2026-10-28)
- **Çözüm/kural:** Paket kökü düzenli ifadesi (`/node_modules/(react|react-dom|scheduler)/`) ve `react-dom/server|static` hariç. `vendor-react` 65,9 KB gzip; öğrenci açılışı 544 → 475 KB gzip. Elle parça gruplarken paket adı alt dize ile değil kök yolla eşlenir.


### H133 — Kaynağı doğrulanamayan sorular gizlenerek kaybedilmişti; "Çıkmış–Örnek" sınıfı (2026-10-28)
- **Önleme:** Kaynağı doğrulanamayan ama doğru soru gizlenmez, `kaynakSinifi=cikmis_ornek` ile etiketlenip öğrenciye belirtilir; çıkmış vurgusu yalnız doğrulanmış kaynağa dayanır.


### H139 — Gizlenen sayfaya giden bağlantı öğrenciyi açıklamasız Bugün'e atıyordu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Sekmeler (`gorunenSekmeler`), takvim hazırlık adımları ve Günün spotu bağlantısı `menudeGorunur` ile süzülür; adresle girilen gizli sayfa "Bu sayfa şu an kapalı" ekranı + Ne yapmak istiyorsun kartlarını gösterir. Bir sayfaya bağlantı veren her yer `menudeGorunur(route)` denetler.


### H141 — Yönetimde görünürlük tek tıkla, onaysız ve geri alınamaz yazıyordu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Öğrenciden kaldıran değişiklik (gizli/kapalı/yalnız yönetici, menüden kaldırma) hedef sunucuyu (`yazimHedefi()`: canlı site / yerel sunucu) yazan onay ister; her yazım 8 sn "Geri al" bildirimi verir (`bildir(metin, ton, {etiket, yap})`).


### H147 — Öğrenci menüsünde hesap ve ders sayfaları yanlış gruplardaydı (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Öncelikli dersler + Geçmiş kurullar → Ders çalış (merkez, menü, alt sekme "Ders"); Başarımlar + Güncelleme günlüğü → Kişisel. Grup değişikliği `merkezModel.MERKEZ_HAM`, `navModel.NAV_TREE_HAM` ve `navV15` (OYUNLAR/KISISEL) birlikte yapılır; adresler değişmez.


### H150 — Güncelleme günlüğünde öğrenciye dosya yolları görünüyordu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Ekran öğrenci maddelerinden kod parçasını, dosya yolunu ve yollu parantezi siler; 3 kelimeden kısa kalan maddeyi göstermez. `guncelleme_notu.json` maddeleri öğrenci diliyle yazılır, dosya yolu içermez.


### H154–H169 — Sayfa denetimi dördüncü tur, öğrenci sitesi orta bulguları (2026-10-28)
- **H154/H155 Kutlama:** kuyruk hangi ekranda olursa olsun hemen açılıyordu → deneme, çıkmış testi, soru çözücü ve sesli ders ayrıntısında ertelenir. Rozetteki "3" ödül seviyesiydi, "Hepsini geç" sayısı bu ödülü saymıyordu → "3. seviye" ipucu, sayaç tüm kuyruk.

### H170–H185 — Sayfa denetimi dördüncü tur, yönetim paneli orta bulguları (2026-10-28)
- **H170 Kurul çipi "1 66":** etiket yalın rakam + aynı boyutta sayı → "Kurul N" + soluk sayı rozeti.

### H200–H212 — Sayfa denetimi beşinci tur, öğrenci sitesi kalan bulgular (2026-10-28)
- **H200/H201/H205/H210 Sınava hazırlan:** boş "Planlama" başlığı yalnız içerik varken; sınav ağırlığı kartı nereye gittiğini söylüyor; olası sorular kartı ATP kilidini önceden yazıyor; telefonda sekme şeridi kenarda solar.

### H300–H311 (öğrenci) — Çevrimdışı ve Arka plan işleri aynı işi iki sayfada yapıyordu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Tek sayfa "Çevrimdışı ve indirmeler" (`/cevrimdisi`): durum → indirme kuyruğu ve arka plan işleri (`#isler`, ArkaPlanV15 gömülü) → toplu indir → indirilenler ve depolama → ayarlar ve eşitleme (tek Wi-Fi denetimi, aynı `ayar.wifi` anahtarı). `/arka-plan`, `/arka-plan-isleri` → `/cevrimdisi#isler`. Bir ayar sitede tek yerde düzenlenir.


### H320–H329 — Görünürlük beş ayrı yerden düzenleniyordu (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Çözüm/kural:** Görünürlük YALNIZ Site › Görünürlük'te yazılır: "Sayfalar" (öğrenci sayfaları + menü) ve "İçerik" (kurul, ders, sesli, deste, paket, önem/asistan/çözücü; yeni uç `GET /api/admin/gorunurluk/icerik`, sayfalı, süzgeçli, katalogda olmayan ayar `sahipsiz`). Diğer sayfalarda `GorunurlukBaglantisi` (rozet + "Değiştir" → `site/gorunurluk?sekme=icerik&q=<anahtar>`). `site/menu` → Görünürlük. Gizleme onay + hedef, her yazım 8 sn Geri al, toplu değiştirme. Yerelde tıklanarak sınandı (tek + toplu, geri al sonrası ayar boş).


### H330–H334 — Sesli ders araç çubukları kalabalıktı (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Kural:** Sesli ders ekranına yeni düğme eklenirken önce sık/seyrek kararı verilir; seyrekse ⋯ menüsüne girer, durum taşıyorsa menüde ✓ ve çubukta etkin göstergesi olur.


### H380–H387 — Kalan küçük öğrenci bulguları (2026-10-28)


### H390–H392 — Veri tutarlılığı: yıldız işaretleri, soru haritası sayımı, deste kurul adları, yinelenen kazanım konuları (2026-10-28, kullanıcı onayıyla)
- **H390 Belirti:** Deneme ekranında soru/şık metninde `**değildir**`, `**Soru:**` ham görünüyordu. **Kök neden:** veri doğru (kasıtlı vurgu; çıkmışta 49 soru, Öğren klinik karar vakalarında 414 öge), `PracticeV15` metni işlemeden yazıyordu. **Çözüm:** `**…**` kalın yazıya çevrilir; veri değişmedi.

### H432 — Ders PDF ekranı kaydırırken "parçalanıp geri geliyordu" (2026-10-28, kullanıcı bildirdi)
- **Çözüm/kural:** Çerçeve ekran boyunda, belge içinde kayar; dar ekranda belge çerçeve genişliğine `zoom` ile sığar, yazdırmadan önce ölçek kalkar (afterprint ile geri gelir). Ölçüm: telefonda çerçeve 358×642, ölçek 0,358, yatay taşma 0; masaüstünde 1010×694. Önizleme/gömülü belge iframe'i içerik boyuna büyütülmez.


### H446 — Öğrencinin en çok çalıştığı ve çıkmışta sorulan bilgi anlatımda "ders yalnız adıyla sayar" diye geçiştirildi (2026-10-30)
- **Kural:** AGENTS 28 — geçmiş yıl öğrenci önem notu (`src/data/ogrenci_onem/`, `docs/OGRENCI_ONEM/<ders>.md`) her 2026-27 dersinde zorunlu
  malzemedir: A birimi anlatımda ayrıntılı (tanım → ayırt edici nokta → sayı/ölçüt → komşu kavram), önem listesinde `ogrenci` etiketli
  madde, ≥2 örnek soru; B birimi anlatımda açık + ≥1 soru. Slaytta yalnız adı geçen kavram, notta/çıkmışta tanımı soruluyorsa tanımıyla anlatılır.
- **Önleme:** "ders yalnız adını verir / yalnız adlarıyla sayar" türü geçiştirme, kavram öğrenci notunda ya da çıkmışta tanımıyla geçiyorsa yasaktır.
- **Kapı:** `python3 scripts/uretim/ogrenci_onem/kapi.py <ders>` 0 HATA — bilgi düzeyinde (el notu, vurgulu satır, çıkmış önermesi) anlatım ve önem
  listesi cümlelerinde arar (vektör + kelime kökü örtüşmesi; yalnız vektör "spastisite ve rijidite" cümlesini rijidite tanımı sanıyordu).

### H449 — Ders/ses sürümleri (V1/V2/V3) sitede görünmüyordu; Nörolojik Muayene V2'ye branş listesinden ulaşılamıyordu (2026-10-30)
- **Önleme:** yeni bir ders/ses sürümü yayımlandığında canlıda öğrencinin GİRDİĞİ sayfalarda (branş listesi + ders sayfası) görünürlüğü
  tarayıcıyla denetlenir; yalnız API alanını görmek yetmez. Denetim öncesi sayfa yeni pakete yenilenir (yüklü `chunk-main` = sunucudaki).


### H459 — KMB (Üretral kateter): küçük video, tekrar eden altyazı, iptal edilemeyen otomatik geçiş, metin hataları, hata takibi yok (2026-10-31)
- **Önleme:** KMB'de yeni ekran düzeni viewport değil `@container kmb` ile seçilir; otomatik geçiş yalnız oynatıcının
  iptal edilebilir `otoSonraki`'si ile yapılır. Hocanın sözü cümleye çevrilirken derecelendirme ("en önemli", "göreceli",
  "hata ama sorun değil") korunur; anlatımda vurgulanan her uygulama eylemi OSCE akışında ayrı basamaktır. Her yeni sınav
  ögesi `adim` taşır (yoksa dogrula.py HATA). Şık açıklamaları `sik_aciklama.denetle` ile 0 HATA.


### H460 — KMB Lottie videoları: kesik/taşan etiketler, kayan kamera, yanlış durumdan başlayan sahneler, sonsuz sayaç (2026-10-31)
- **Önleme:** Video değişikliğinden sonra `node meds/scripts/uretim/kmb/kare_onizle.mjs [ad…]` ile temas sayfası üretilir ve her
  cümle karesi metinle karşılaştırılır (rapor.json otomatik bulgu 0 olmalı). Etiket ≤30 harf; önemli öge (torba, meatus,
  kan) sahnenin alt %24'üne konmaz; alt kompozisyonda "son durum" gerekiyorsa `'once'` kullanılır, None değil.


### H467 — Taşınan hesaplar için e-postaya bağlı şifre belirleme tek yoldu; Drive'da ölü servis hesabı yedeği (2026-11-02)
- **Önleme:** Hesap kurtarmanın en az bir yolu hiçbir dış hesaba bağlı olmamalı (yönetici onayı). Bir dış servisin yedeği
  çalışmıyorsa sessiz geçilmez, günlüğe bir kez yazılır. İçerik alımı herkese açık Drive yoluyla çalışır; kimlikli yedek
  için kullanıcı askıda olmayan bir hesapta yeni servis hesabı ya da `rclone config reconnect meds:` kurmalıdır.


### H471 — Yeni Kurul 2 derslerinde PDF açılmadı, PDF işareti atlandı (2026-11-02)
- **Önleme:** Elle hatta yayın sırası: PDF → manifest + iki drive_root → `yayinla.py --yerel` → `build_deck_pdf_sources.py`
  (bütün desteler yayınlandıktan sonra) → commit/dağıtım → `ders-ekle`. Dağıtımdan sonra `/api/lecture-pdf/deck/<deste>/0` 200
  denetlenir.


### H472 — Hoca vurgusu `konu` alanı özetti, değerlendirme kapısı slayttan birebir istiyor (2026-11-02)
- **Önleme:** A1 şemasında iki alan ayrıdır: `konu` = slayttan birebir, `konu_ozet` = okunur özet. Tablo sayfasında alıntı tek hücre içinden.


### H474 — Bu yılın PDF'inden üretilen Farmakoloji dersi öğrenciye görünmedi (2026-11-02)
- **Önleme:** Sınama yalnız anahtar listesiyle verilir (branş kuralı yok). Yeni ders yayınında §6 doğrulaması güncel listede
  (`/api/canli-ders`, `donem` yok) dersin anahtarını arar; yoksa yayın bitmiş sayılmaz. `data/*.json` değişikliği Oracle'a
  `scp + sudo cp + chown ubuntu` ile ayrıca konur ve canlı uçtan okunarak doğrulanır.


### H475 — Yeni sürüm penceresi kartsız (düz madde) göründü (2026-11-02)
- **Önleme:** öğrencinin gördüğü yeni özellik/ders içeren her dağıtımda `yenilikler` en az bir kart taşır ({ad, nerede:{ad,yol},
  amac, islevler}); yalnız küçük düzeltmede `maddeler` yeterlidir.


### H487 — `kisaltma_sozlugu.py sozluk_disa` elle eklenmiş kısaltmaları siliyor (2026-11-04)
- **Kural:** `sozluk_disa` sonrası daima kayıt sayısını HEAD ile karşılaştır; düşüş varsa yazma, birleştir. (Betik birleştirme kipine geçirilmeli — açık iş.)


### H490 — Öğrenci önem kapısı geçilemez yanlış HATA veriyordu (k2-15, k2-16, k2-11; 2026-11-05)
- **Kural:** kapı HATA'sı "eşleyici kaçırıyor" diye bırakılmaz: ya anlatım düzeltilir ya kapının kendisinin denetlediği kanıtlı eşleme yazılır.


### H491 — Ara soru kodu başka dersin numarasını aldı (2a17 = k2-07; 2026-11-05)
- **Kural:** ara soru kodunu elle seçme; `kur.py iskele` atar.

### H492 — Hoca vurgu alıntısı bozuk CPU dökümünden kuruldu (2026-11-05)
- **Önleme:** Yeni ara resim kapıdan 0 HATA geçmeden yayına girmez; ölçü örneği k2-07 r01.

### H507 — iPad'de sesli dersten geri çıkılamıyordu; "başlığa bas = geri" çalışmıyordu (2026-11-06)
- **Kural:** Geri yolu eklerken odak ekranlarını (kabuk dışı başlıklar) ayrıca kapsa; "algılanırsa göster" türü güvenlik yollarını algının başarısız olduğu durumda da sına.

### H508 — Drive'daki ses dosyasının adı başka dersi gösteriyordu: "TSSB Psikaytr 2" aslında EKT (Tedaviler) dersinin başıydı (2026-11-06)
- **Önleme:** Ses dosyası, PDF gibi, **içerikle** eşleşir (KURUL2_DERS_STANDARDI §1): hizada slayta düşmeyen ≥3 dk'lık blok "ders dışı" işaretlenir ve aynı kurulun diğer derslerinin slaytlarıyla karşılaştırılır; bir dersin başı/sonu sessizse öbür kayıtlar o derse ait olabilir diye taranır.

### H509 — Destesiz derste ders içerik paketinin kısaltmaları "Ek"e düşüyordu (adim 0), kapı %5 sınırında HATA verdi (2026-11-06)
- **Önleme:** Biçim değişen ara dosyayı okuyan betik, beklenen biçim gelmezse sessizce boş sözlükle sürmez; destesiz her derste paketten sonra `ders_icerik_adim.py` çıktısındaki "eşlenemeyen" sayısı 0 değilse nedeni bulunur (eşik altı olsa da).

### H510 — Değerlendirme kapısı kaynakça sayfasındaki yazar baş harflerini "sözlükte yok kısaltma" sayıyordu (2026-11-06)
- **Önleme:** Kapıyı geçmek için sözlüğe anlamı bilinmeyen kısaltma eklemek YASAK; yanlış pozitifin kökü kapıda düzeltilir.

### H511 — Şık açıklamalarına betikle yeni geçiştirme kalıpları eklendi, kapı yakalamadı (2026-11-06)
- **Önleme:** Şık açıklamasına betikle sabit cümle eklemek YASAK; kısa açıklama elle, şıkka özgü gerekçeyle uzatılır. Denetçi aynı cümlenin ≥3 şıkta geçmesini bulgu sayar.

### H512 — Anlatım parçalara bölünerek yazdırılınca ara resim adımı düştü (k2-21)
- **Önleme:** B1 bölünürse ara resim ayrı bir alt görev olarak MUTLAKA açılır; yayın öncesi kontrol listesinde `python3 scripts/uretim/ara_resim/dogrula.py <key>` çalıştırılır ve `src/data/ara_resim/<key>.json` yoksa ders tamamlandı sayılmaz.

### H513 — dist/assets hiç budanmıyordu: cihazda 473 derleme (3 GB), Oracle'da 92 bin parça (5,2 GB) + 5,9 GB arşiv (2026-11-09)
- **Önleme:** Hash'li çıktı biriktiren her klasöre (dist, arşiv, ses klipleri) yazan kod, "güncel küme + yaş" kuralıyla budama da yazar; "sonra temizleriz" diye bırakılmaz. Oracle'da imaj yeniden kurulduğunda `docker builder prune` dağıtım sonrası adımıdır (`dagit.sh`'a eklenmedi; elle).

### H514 — Örnek sorular ders listesinde "Hoca üslubu · N yeni soru" rozeti öğretim üyesi adının üstüne biniyordu (tablet/masaüstü, 2026-11-09)
- **Önleme:** Yeni oyun/hamle eklenince `tahmin.ts`'e kesin bilinen kısmı eklenir ve aynı karşılaştırma koşulur; ekran hiçbir zaman ağ yanıtına kilitlenmez. Okey per açma/işleme/çekme hâlâ sunucuyu bekler (ıstaka düzeni + gizli taş). Ağ tarafındaki sıçramalar için kalıcı çözüm ancak WS'yi tünelden ayırmaktır (ayrı alt alan, Cloudflare/Oracle erişimi kullanıcıda).

### H530 — Kısık amfi kaydında hoca dökümü uydurma cümlelerle doluyordu (2026-11-10, k2-22/23/24/58)
- **Önleme:** Istaka düzeni değiştiren her işlev grupları korumalı; grup toplamını gösteren her ekran dar boyutta (`yuva_t` sınaması: 21 taş 6 grup, sütun 16/14) denenir. Bot ekleyen her oyuna zorluk seçeneği verilir; "kusursuz bot" yalnız Zor'da. Sınama `tahta.sinama.ts` (kolay bot 40 elde ≥5 kayıp).

### H534 — Taş Masası: masadaki taş eldeki taşlarla yeni pere katılamıyordu (2026-11-10)
- **Önleme:** Masaya taş koyan her oyunda "masadan taş + elden taş = yeni per" senaryosu motor sınamasında bulunur (`yedili.sinama.ts`, `yuzbir.sinama.ts` düzenle bölümleri). Bir hamle türü bir oyuna eklenince aynı masa modelini paylaşan öteki oyunlar (yedili/takım/101/kastet/remi) birlikte gözden geçirilir.
- **Önleme:** Kullanıcının elle düzenlediği alanda (masa taslağı, ıstaka) öğeler kendiliğinden yer değiştirmez; düzen yalnız kullanıcının açık isteğiyle (Sırala, Masayı diz) değişir. Sınama: düzenlemede taş alıp per boşaltınca komşu perin `getBoundingClientRect().left/top` değeri değişmemeli.

### H542 — Uno'ya 10 yeni mod eklenirken motor sınamasının yakaladığı dört kural hatası (2026-11-10)
- **Önleme:** Uno'ya kural/kart ekleyen her değişiklikte `npx tsx src/services/masa/motor/uno.sinama.ts` ve `unoMod.sinama.ts` 0 hata vermeli: her mod için birim senaryolar + bütün oyuncu sayılarında hepsi-bot rastgele eller (kart korunumu, tıkanmama, gizlilik, puan toplamı) + bulanık hamle. Yeni bir "bekleyen karar" ya da el sayısını değiştiren etki eklenince korunum denetimine (`korunum`) ve `sonIslem` UNO taramasına dahil edilir. Arayüz: `meds_temp/uno_ui/uno_ui.mjs` (başsız Chrome, `?masatest`, 12 mod × telefon dikey/yatay, tablet, masaüstü; taşma, dokunma hedefi, konsol hatası). Başsız sınama çıktısı `/tmp/claude-1000` kotasına yazılmaz (EDQUOT ile yarıda kesildi), `meds_temp` altına yazılır.


### H536 — Değerlendirme kapısı tasarım PDF'inin harf aralıklı başlıklarını ("Y A N I TL A R", "KAYN AKLAR") kısaltma sanıyordu (2026-11-09, k2-22)
- **Önleme:** Kapıyı geçmek için sözlüğe anlamsız kısaltma yazılmaz (H510); yeni biçim tuzağı kapının kendisinde düzeltilir.

### H537 — A1a/A2 "kanıt" alanları birden çok satırı birleştiren özetler olduğundan değerlendirme kapısından geçmiyordu (2026-11-09/10, dört derste)
- **Önleme:** A1a/A2 yönergesine kural: `kanit` = TEK birebir satır ya da tablo hücresi; yazar üretim sırasında pymupdf normuyla doğrular (`kaynak_kapisi.py` + `degerlendirme_dogrula.py` paket kurulmadan önce koşulur).

### H538 — 5. parti derslerinin anahtarları `MODUL_ANAHTARLAR`'da yoktu: yazımla tutulan kısaltmalar (DSM, EEG, SSRI) harf harf okunmamış olabilir (2026-11-09)
- **Önleme:** `sesli_yayinla.py` yeni anahtarı `modul_okunus.modul_mu` ile denetleyip değilse uyarır (yapılacak); el kitabı §19 adım 8'e madde.

### H539 — EMA tam MP3 yüklemesi Oracle'daki başka bir dağıtımın sunucu yeniden başlatmasına denk gelince iş "hata"ya düştü (2026-11-09, k2-22)
- **Önleme:** dağıtım öncesi `dagit.sh` kuyrukta `calisiyor` EMA işi varsa beklemeli ya da işçi `tam/bitir` adımını 3 kez yinelemeli (yapılacak). İşçi günlüğü: `journalctl --user -o cat | grep <key>` (birim değil, scope).

### H540 — `kelime_zaman.py --gpu` elle çağrıda `libcublas.so.12` bulamayıp sessizce CPU'ya düştü (2026-11-10)
- **Önleme:** `kelime_zaman.py` başında `nvidia/*/lib` yollarını `LD_LIBRARY_PATH`'e kendisi ekler (yapılacak); CPU'ya düşüş UYARI değil, belirgin HATA satırı olmalı.

### H541 — Destesiz derslerin örnek soruları k2-12'den beri siteye yayınlanmıyordu (2026-11-10)
- **Önleme:** destesiz yayın betiğine s16 adımı eklenir; `ders_icerik_dogrula.py` sitede örnek soru dosyası yoksa HATA versin (yapılacak).

### H543 — İçi boş madde imi pymupdf metninde "o" harfi olarak geldi; değerlendirme kapısı birebir kanıtları reddetti, yazar bilgisiz kanıt satırına kaçtı (2026-11-10, k2-26)
- **Önleme:** Kapıyı geçmek için kanıtı bilgiyle ilgisiz bir satıra kaydırmak YASAK (kanıt bilgiyi göstermeli); iki kapının metni farklıysa kök neden kapıda/çıkarımda düzeltilir ve koordinatöre bildirilir.

### H544 — Ek modül içeriği hocanın materyali sorulmadan yazıldı; çalışma soruları gelince 16 konunun tamamı yeniden yazıldı (2026-11-10, Yürüyüş ve Kampçılık)
- **Önleme:** yeni ek modülde ilk iş hocanın materyalini istemektir (AGENTS kural 30). Hocanın kendi içinde çeliştiği cevaplar (kazık 45°/90°, tuvalet 50/150 m) sessizce "düzeltilmez": en çok yinelenen değer esas alınır, ekrana "ikisini de bil" notu düşülür ve kullanıcıya raporlanır. Hocanın bilimsel olarak tartışmalı ifadesi (baştan %50 ısı kaybı, gnays kristalleri) hocanın dediği gibi kalır; metin ona aykırı yeni iddia eklemez.

### H545 — `git add server.ts` başka oturumun commit'lenmemiş iki satırını da commit'e aldı; depoda olmayan dosyayı içe aktaran sunucu kodu origin/main'e gitti (2026-11-10)
- **Önleme:** ortak dosya sahnelenmeden önce `git diff <dosya>` okunur; yabancı satır varsa yalnız kendi parçaların sahnelenir (`git apply --cached` / `git update-index --cacheinfo`). Commit'ten sonra `git show --stat` satır sayıları beklenenle karşılaştırılır. Oracle'da `server.ts`'in kirli sürümle bulunmasının kaynağı saptanamadı (dağıtım temiz worktree'den yapılır); yinelenirse o dakikada Oracle'a yazan öteki süreç aranır.

### H546 — Ek modülde sesli ders PDF'le birlikte ilerlemiyordu; eşleme kurulurken iki ölçüm tuzağı (2026-11-10, Yürüyüş ve Kampçılık)
- **Önleme:** ek modülde ses ya da ders kitapçığı yeniden üretilince `pdf_esle.py` yeniden çalıştırılır; `dogrula.py --modul` eşleme eskimişse (klip özeti ya da PDF boyutu tutmuyorsa) HATA verir, ekran da özeti tutmayan klibin eşlemesini kullanmaz. Karşılığı bulunamayan cümleye madde uydurulmaz (yalnız bölüm çerçevesi; kural 17'deki "çapa uydurma" yasağıyla aynı ilke).

### H547 — Gövdesi yalnız resim olan slayda dayanan doğrudan çıkmış, değerlendirme kapısından geçemiyordu (2026-11-10, k2-28 s.21)
- **Önleme:** görüntü sayfasına dayanan çıkmış eşlemesi `kanit` + `kanit_goruntu` ile yazılır ve denetçi sayfa görüntüsüne bakar; kanıt metni olan başka satıra kaydırılmaz, eşik gevşetilmez.

### H548 — Slayt altındaki kaynak satırının dergi adı "sözlükte olmayan kısaltma" sayıldı (2026-11-10, k2-28 s.31)
- **Önleme:** kapıyı geçmek için sözlüğe dergi adı ya da anlamsız kısaltma yazılmaz (H510); yeni biçim tuzağı kapının kendisinde düzeltilir.

### H549 — Önem maddesinin alıntısı olarak slayttaki kaynak künyesi yazıldı (2026-11-10, k2-28 2t02-23)
- **Önleme:** görüntü sayfasından alıntı `{"sayfa", "metin", "gorsel": true}` ile yazılır, denetçi görüntüden doğrular. Kapıdan geçsin diye bilgi taşımayan satır (künye, başlık, sayfa numarası) alıntı/kanıt yapılmaz.

### H550 — Canlı çizimde kontur doğru, etiketi yanlış figüre düşüyor ya da slayt yazısını kapatıyordu (2026-11-10, k2-28)
- **Önleme:** (1) yazı parçasını boyayan konturda etiket yazılmaz (boyanan yazı zaten etikettir); (2) kendi yazısını taşıyan figür/kutu konturunda etiket yalnız slaytta olmayan bilgiyi ekliyorsa yazılır; (3) yazar yayından önce bindirmeyi ETİKETLERİYLE üretip bakar (`etiket_konum` + `pdfDoc.css` yazı boyutu; k2-28 `cizim/bindir2.py`); (4) yanlış yerde etiket, etiketsizlikten kötüdür — güvenle oturmayan etiket kaldırılır.

### H551 — Giriş yapmış öğrenci kendi profilini ve arkadaşlık isteklerini göremiyordu (2026-11-10)
- **Önleme:** `verifiedUid` okuyan yeni bir GET ucu eklenince `ogrenciJetonu` listesine de eklenir; uç yazıldığında girişli kullanıcıyla tarayıcıdan GET sınanır (curl'deki jetonsuz yanıt "çalışıyor" sayılmaz).

### H552 — Sesli çalışma sorularında boşluk doldurma "boşluk" diye okunuyordu (2026-11-10, ek modül)
- **Önleme:** `dogrula.py --modul` boşluklu (`__`) her hoca sorusunda `okunus` yoksa ya da soru işaretiyle bitmiyorsa HATA verir. Yeni boşluklu soru eklenirken (her modülde) okunuş elle, doğal soru cümlesi olarak yazılır; mekanik "boşluk/ne" değişimi yapılmaz.

### H553 — Değerlendirme kapısı OCR'lı metinden alınan çok satırlı kanıtları PDF'te bulamadı (2026-11-12, k2-31)
- **Önleme:** A2'de kanıt alıntısı her zaman `pymupdf.open(pdf)[s-1].get_text()` satırlarından birebir kopyalanır; OCR/`sayfalar.json` yalnız metni okumak/anlamak içindir. Liste/tablo sayfasında birden çok satırı kapsayan alıntı yazılmaz. Metinsiz (<60 karakter) sayfaya dayanan çıkmışa `kanit_goruntu` zorunludur.

### H554 — Ders içerik paketinde "bilgiler boş": bilgi havuzu `tur` alanı içerik tipiyle dolduruldu (2026-11-12, k2-29)
- **Önleme:** `bilgi_havuzu.jsonl` `tur` yalnız TALIMAT §8 listesinden; içerik tipi `icerik_turu`'na. Yönergeye bir satır eklendi.


### H555 — Şık açıklamasında uzunluk dolgusu: aynı "ana bilgi" cümlesi birden çok şıka eklendi (2026-11-12, k2-29 / k2-30)
- **Önleme:** şık açıklaması kapıyı geçmek için betikle uzatılmaz (AGENTS 14 dolgu yasağı); kısa kalan açıklama elle, o şıkkın kavramıyla yazılır. Önerilen kapı eki: aynı sorunun iki şıkkında birebir aynı ≥6 kelimelik cümle HATA (`sik_aciklama.py`).

### H556 — "PDF indir" herkese "X-API-Password başlığı gereklidir" diyordu; canlıda başsız tarayıcı da yoktu (2026-11-13, kullanıcı bildirdi)
- **Önleme:** yeni bir parolasız uç gerektiğinde önce "veri yazıyor mu?" sorusu sorulur: yazmıyorsa `readOnlyPosts`/`STUDENT_WRITE_ROUTES`'a **sınırıyla** eklenir, yazıyorsa parola ister. Kapı: `python3 scripts/kapilar/pdf_basim_kapisi.py` (yerelde ve canlıda) `/api/pdf/status` `available:true` + parolasız 200 ve `%PDF` imzası arar; 401'de "uç beyaz listede değil", tarayıcı yoksa "imaja chromium eklenmeli" der.
- **Önleme:** 3P `inferenceModels` rota adında üçüncü taraf işareti (`deepseek/glm/kimi/mimo/minimax/gpt/…`) kullanılmaz; ad `claude-od-NN` gibi nötr olur, gerçek model `labelOverride` ve köprü eşlemesinde tutulur. `settings.json` `env` değerleri komut satırından ezilemez — ortam değişikliği sanılıyorsa önce bu dosyaya bakılır. Köprü `upstream`'i asla kendi adresini göstermez (açılışta kapı var). Ayrıntı: `~/.claude/OPENDESIGN_KULLANIM.md`.

### H558 — Bash aracı hiç açılmıyordu: `apply-seccomp: write /proc/self/setgroups … Permission denied` (2026-11-13, kullanıcı bildirdi)
- **Önleme:** Aynı hata görülürse önce `sudo dmesg | grep -E "apparmor|userns" | tail` bakılır; `unpriv_bwrap` + `sys_admin` satırı varsa profil bir paket güncellemesiyle geri gelmiştir, iki komut yinelenir (`aa-complain` çözüm değildir). **Ayrı katman:** sandbox ağ kapısı (`sandbox.network.allowedDomains: []`, `allowManagedDomainsOnly: true`) bu düzeltmeden sonra da kapalıdır; `git fetch/push`, `ssh`, `curl` Bash'te çalışmaz — ağ işleri Terminal panelinden yapılır ya da kullanıcı Ayarlar → Claude Code'dan ağ iznini açar. İki katmanı karıştırıp "kabuk açıldı, ağ da açıldı" sanmak yeni bir yanlış kök neden avına yol açar.

### H559 — İçerik katmanı toplu "silinen" yazdı: sözlükte 750 terim, Öğren'de 11 deste sunucuda görünmüyordu (2026-11-13, kullanıcı bildirmedi — tur sırasında bulundu)
- **Önleme:** `data/content/` altına elle, başka araçla ya da eski yedekten **tam kopya bırakılmaz** (yalnız `.fark.json`). Sözlük/deste/soru sayısı beklenenden az görünürse ilk bakılacak yer `data/content/<dosya>.fark.json` → `silinen`dır; `python3 scripts/icerik_katman.py denetle` ile katman düzenli denetlenir. Günlükte "toplu silme sayılmadı, karantinaya alındı" uyarısı görülürse `_karantina_silinen.json` açılır: silme gerçekten yönetici kararıysa kimlikler fark dosyasına elle yazılır; değilse hiçbir şey yapılmaz — kayıtlar görünür kalır. Katmanı mtime'a göre "taze" saymak yetmez: bir kopya yeni damgalı ama içeriği eski olabilir.

### H560 — Ajan hattı OpenDesign geçidine taşınırken roller tek modelde birleşti, eşlenmemiş adlar sessizce geçide gitti (2026-11-13, kullanıcı istedi)
- **Önleme:** Yeni bir model/ad eklenirken **iki** yere yazılır: `rotalar.json` ve `opendesign.ESLEME`; sonra `kopru.py --doctor` koşulur (0 HATA). Bir betiğe `--model <sabit ad>` yazılmaz, `ajan_model()` çağrılır. Aynı aile iki rolde görünüyorsa (yazar = denetçi) denetim bağımsızlığı yoktur: denetçi rolü ayrı aileye (`glm-*`/`gpt-*`) bakar. `claude` CLI çağrısı eklerken önce `llm_kilit` + `model_sec` çifti eklenir, sonra çağrı yazılır.

### H561 — Artifact stüdyosu: önizleme sunucusu bulunamadı, grafikte iki farklı büyüklük tek eksende ezildi, `.claude/launch.json` `/dev/null` ile maskelendi (2026-11-13, kullanıcı istedi)
- **Önleme:** Önizleme sunucusu eklerken **önce** `mcp__Claude_Browser__preview_list`/`preview_start` ile yolun doğruluğu sınanır; `launch.json` yazımı oturum köküne yapılır. Bir dosyada `git diff`, `rm` ya da `cat` "desteklenmeyen tür / meşgul" derse **dosyanın kendisi değil üstündeki mount** sorgulanır: `findmnt -T <yol>` + `grep <yol> /proc/self/mountinfo`. Maskeleme biter beklemeden `git rm`/`rm -f` denenmez — `rm -f` **başarılı görünüp** izlenen dosyayı silebilir (bu turda oldu; geri yükleme `git checkout --` ile yapıldı). Grafikte büyüklük farkı ~10× ise çift eksen zorunlu; tek eksende "küçük seri görünmüyor" bir tasarım tercihi değil hatadır.

### H562 — Canlıda yeni anahtar "yok" göründü: `env_file` yalnız konteyner oluşturulurken okunur, loopback da konteynerde loopback değildir (2026-11-13)
- **Önleme:** `.env`'e yalnız dotenv'in okuyacağı yeni anahtar ekleniyorsa konteyner yeniden başlatma yeterlidir; **compose `environment:` listesine eklenmesi gereken** bir değişken söz konusuysa `docker compose up -d --force-recreate` gerekir (bu tur gerekmedi). "Container env'de yok" tek başına "uygulama görmüyor" demek değildir; kanıt uygulamanın kendi ucundan alınır. Konteyner içinden atılan istek yönetici/loopback muamelesi görmez.

### H570 — Ders analizi betiği tam ders anahtarını "kayıt defterinde yok" sandı (2026-11-13, k2-62/k2-65)
- **Önleme:** Yeni bir betik yazarken **üç kimliği** ayrı tut: (a) sesli ders anahtarı (`k2-62-…`), (b) kayıt defteri id'si (`k2-62`), (c) alt klasör adı (`meds_database_v2/ders_bilgi/k2-62`). Betik hangisini beklediğini kullanım satırında yazsın; karşılaştırma ve dosya yolu **aynı** biçimden kurulsun. "kayıt defterinde yok" hatası görüldüğünde önce anahtarın hangi biçimde olduğu ve dizinin gerçek adı kontrol edilir, kayıt defterine madde eklenmez.

### H571 — Ders içerik paketinde kısaltmaların hepsi `adim: 0` kaldı: `sayfalar.json` yedeği hiç çalışmadı (2026-11-13, k2-65 ders içerik paketi)
- **Önleme:** Bir yedek/ikinci kaynak yolu yazarken "dosya var mı" ile "içerik boş mu" ayrı sınanır — boş varsayılan (`{}`/`[]`) yedeği **atlatır**, `isinstance` kontrolü bunu yakalamaz. Kapı çıktısında `adim eşlenemeyen %N` görülürse önce kaynak dosyanın gerçekten okunduğu (`J(sp)` sonrası `len(sayfa)`), sonra hangi kayıt türünün 0 kaldığı (bu turda yalnız `kisaltmalar`) kontrol edilir; kapı 0 HATA verse bile paket körü körüne kabul edilmez.

### H572 — Soru dışa aktarıcı çöküyordu ("sayfayı yenile"); PDF'te logo alt bilgiyle üst üste biniyor, alt bilgi/başlık kesiliyor, ızgarada soru kayboluyordu (2026-11-14, kullanıcı bildirdi)
- **Önleme:** (a) `PALETLER[...]` doğrudan indekslenmez; her yerde `paletRenkleri`/`paletNormal` kullanılır. (b) Sayfa geometrisinde sabit mm **yalnız** kullanıcıdan bağımsız ögeler için; logo, alt başlık, alt metin gibi kullanıcı ayarlarına bağlı yükseklikler `baslikYukMm`/`altYukMm`den gelir ve HTML/DOCX/PPTX aynı fonksiyonu çağırır (üç çıktı ayrışmaz). (c) `overflow:hidden` bir soru/çözüm kutusunda **kırpma** anlamına gelir; ızgarada sığmayan blok taşınmalı (ayrı akış), kırpılmamalı. (d) Yeni bir palet/kapak/başlık seçeneği eklerken "en büyük değer" ile ölçüm yapılır (logo 24 mm, alt bilgi en uzun metin, 40 mm not alanı); yalnız varsayılan değerle bakmak hatayı gizler. (e) Kullanıcı "sayfayı yenile" ekranı bildirdiğinde ilk bakılacak yer canlı `data/istemci_hatalari.jsonl` (Oracle: `docker exec meds-app`), çünkü o ekranı üreten gerçek yığın orada ve `?adres=` alanı hangi sayfa olduğunu söyler.

### H573 — "Sayfayı yenile" ekranı yenilemeyi öneriyor ama kurtarmıyordu: eski kabuk + eksik parça döngüsü (2026-11-14, H572 ile aynı tur)
- **Önleme:** Bayat kabuk + eksik parça hatasında çözüm "reload" değil "önce önbelleği tazele, sonra yükle"dir; önbellek temizliği çevrimdışı içerik paketlerine dokunmaz (`canli-ders|pdf-offline|paket|bekleyen|paylasim` korunur). `preloadError` dinleyicisine dokunulursa `preventDefault()` korunur; kaldırılırsa iki reload yarışır ve döngü sınırı işlemez.

### H574 — Oyun masasında 13 kez çökme: `oyuncu.cezalar` olmayan eski oyun durumu (2026-11-14, kullanıcı "bu tarz hataları da çöz" dedi)
- **Önleme:** `?.` **alan** korur, **dizi metotlarını** korumaz: `X.filter(...)` öncesi `Array.isArray(X)` sınanır. Sunucudan gelen oyun durumu eski biçimli olabileceği için istemci her dizi alanını varsaymak yerine doğrular.

### H575 — "PDF'te alt kısımda soru/şık metni kesik kalıyor" bildirimi H572 sonrası da geldi: sıfır boşluklu sayfa geometrisi baskı kaymasına karşı savunmasız (2026-11-15, kullanıcı bildirdi)
- **Önleme:** (a) "Tam dolu sayfa + `overflow:hidden`" kombinasyonu kırpma demektir; sabit ölçülü her gövde baskı toleransı taşır. (b) Bu sınıf hatayı sınama yöntemi: canlı sayfada gerçek indirme akışı → ihracat HTML'ini yakala → bağımsız Chrome'da bas → `pdftotext` boşluksuz karşılaştırma + `-bbox` ile alt kenara yapışık sözcük taraması; ekranda "önbellek/eski sayfa" tuzağına düşmeden kullanıcı akışının birebir aynısı budur. (c) pdftotext eşleşmesinde boşluklar ve madde imleri biçimden geldiği için karşılaştırma her zaman `\s` temizlenmiş metinle yapılır; sıralı karşılaştırma sırası kolon yerleşimiyle değişebilir, "eksik" sanmadan tam metinde aranır.

### H576 — "PDF'te alt bilgi (sayfa numaralı satır) diğer metnin üstünü kapatıyor": sayfa kutusu kâğıttan kısa basılmıyordu (2026-11-15, kullanıcı bildirdi)
- **Önleme:** (a) **İstemcide ölçülüp sunucuda basılan her belgede ölçüm yazı tipi ile basım yazı tipi AYNI aileye düşmelidir.** Render ortamına yazı tipi eklerken/çıkarırken `fc-match` ile yığının gerçekte hangi dosyaya düştüğü denetlenir; metrik uyumlu aile (Liberation↔MS core) şarttır. Yeni bir yazı tipi seçeneği eklenince hem istemcide (web font / sistem) hem Oracle konteynerinde karşılığı bulunmalı. (b) Yerel sınama konteynerle aynı yazı tiplerini kullandığından bu sınıf hatayı GİZLER; PDF düzeni hatalarında önce `docker exec meds-app fc-match "<yığının ilk adı>"` ve çıktı PDF'inde `pdffonts` bakılır. (c) Sabit yükseklikli kutuyla kurulan yazdırılabilir belgede native `window.print()` kullanıcının kenar boşluğuna bağımlıdır; deterministik çıktı için hep sunucu PDF'i bastırılır.
- **Önleme:** Sabit sayfa kutusu (`height: kâğıt ölçüsü`) + `break-after:page` kombinasyonunda kutu asla kâğıda eşit ölçülmez; "eşit" ölçü yuvarlamada "büyük" demektir ve Chrome bunu sonraki sayfaya taşıyarak çözer. Bu sınıfın sınaması: ihracat HTML'i bağımsız Chrome'da basılır, `.pg` sayısı ile PDF sayfa sayısı ve sayfa başına alt bilgi metni karşılaştırılır; sayfa sayıları eşit olsa bile parçalama sayfa sayısını değiştirmeden üstüne basabildiğinden kesin kanıt için kutu yüksekliği kâğıttan kısa tutulmalıdır.

### H572 — Etiketleri görselin içinde olan slayt şeması "resim" sayılmıyordu: lazer sayfaya düşüyor, üstüne çizim yapılamıyordu (2026-11-15, k2-65 s.40)
- **Önleme kuralı:** "İçinde çok yazı var" tek başına zemin göstergesi DEĞİL; ayırt edici ölçüt yazının **nerede** olduğudur
  (kutunun dışında kalan kelime sayısı). Yeni bir görsel/görsel-içi-etiket slaytı eklendiğinde: `sekil_isareti` çıktısı
  `t: resim` olmalı, dökümde `R#` satırı bulunmalı; bulunmuyorsa şablon zemin değil şema kabul edilir. Kapı gevşetilmez.

### H577 — "Toplu yol süpürmesi bazı betikleri sessizce atladı": Türkçe yerel ayarda sed/grep `[a-z]` aralığı "i" harfini eşleştirmiyor (2026-11-16, yeniden yapılandırma)
- **Önleme kuralı:** (a) Bu projede aralık içeren her sed/grep/awk süpürmesi (`[a-z]`, `[A-Z]`, `[a-zA-Z0-9]`)
  **`LC_ALL=C` önekiyle** çalıştırılır. (b) Süpürmenin kendi doğrulaması da `LC_ALL=C` ile yapılır — tr_TR altında yapılan
  denetim aynı kör noktayı tekrarlar ve "0 kaldı" yanılsaması verir. (c) Taşıma/silme **güvenlik kapılarında** aralık değil
  birebir dosya adı (`grep -F` / sabit dize) kullanılır; bu turdaki kapılar böyle olduğundan etkilenmedi. (d) Büyük/küçük
  harf duyarsız eşleşmede (`-i`) de aynı i/İ katlama tuzağı vardır; yol/dosya adında `-i` yerine birebir eşleşme tercih edilir.

### H578 — Betik dizini taşırken sessiz kırılma sınıfları: yeniden yapılandırmada yakalanan 7 tuzak (2026-11-16)
- **Önleme kuralı (dizin taşıma/yeniden adlandırma kontrol listesi):** (a) önce yol-çözümleme envanteri (`__file__`, `parents`, `dirname`,
  `os.path.join(...'..')`, değişken zincirleri); (b) `meds_temp`'te aynı adlı kopya var mı → varsa önce kod/veri ayrımı; (c) kum havuzu
  diferansiyeli YETMEZ — ayrıca AST ile "taşınan modülü paket adıyla import eden dış dosya" taraması ve `-m <modül>` / `WorkingDirectory`
  taraması; (d) py-dışı göreli atıf yalnız dosyaya-göreli bağlamda değiştirilir, tüm uzantılar (.tsx dahil) listelenir; (e) gerçek kapılar
  gerçek ÇALIŞMA girdileriyle koşulur (yayınlanmış kopya değil); (f) taşınan her yol `tasinan_yollar.txt`'ye; birim değişince repo kopyası
  da değişir; (g) liste/süpürme Python ile (yerel ayardan bağımsız).

### H579 — "Oracle'da kok'u import eden her betik çöküyor": kök markerı yalnız geliştirme makinesinde vardı (2026-11-16, dağıtım sonrası canlı sınama)
- **Önleme kuralı:** Kök çözümü yalnız REPO İÇİNDE izlenen dosyalara dayanır (git'te olmayan, makineye özgü dosya marker olamaz).
  Yol/altyapı değişikliği dağıtıldıktan sonra Oracle'da en az bir zamanlayıcı birimi GERÇEKTEN çalıştırılıp günlüğü okunur; sağlık uç
  noktası ve birim "success" durumu yeterli kanıt değildir (boru hattı çıkış kodunu yutabilir).


### H580 — "Otomatik onarım / NotebookLM ile düzelen deste dağıtımda geri dönüyor" (2026-11-16)
- **Önleme kuralı:** Sunucu tarafında `src/data` altına yazan her kod `writableContent()` ile yazar, `resolveContent()` ile okur; türetilmiş dosyalara (`decks/items`, paketler) elle yazılmaz.
