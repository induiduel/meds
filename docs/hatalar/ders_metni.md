# Hata defteri — ders_metni (anlatım metni, slayt sadakati, terim/kısaltma, değerlendirme kapısı)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## H2 — Türkçeye uymayan ifade ve iç etiketler (2026-10-18)

- **Görülen:** Sınav asistanı (Patoloji 08, "IL-6: karaciğerde akut faz yanıtı"): "IL-6 … salınır; **imzası** karaciğerde akut
  faz yanıtını uyarmaktır." ve "**Ayrım cümlesi:** ateşte IL-1 daha belirgin, akut fazda IL-6, nötrofil alımında IL-17."
- **Neden hata:** "imzası" İngilizceden çeviri mecaz; "Ayrım cümlesi:" yazarın iç etiketi, öğrenci anlamıyor. Metin EMA ile okunduğu
  için doğal olmayan cümle dinlerken daha da kötü duyulur.
- **Kurul 2'de doğrusu:** Doğal, eksiksiz, anlaşılır Türkçe; çeviri mecaz ve iç etiket yok; tam cümle.
  Ayrıntı: `meds/docs/TURKCE_USLUP_STANDARDI.md`.
- **Kapı:** `meds/scripts/turkce_uslup.py` (liste her kalıbı yakalamaz; denetçi metni sesli okunuyormuş gibi okur).

### H4 — Öğrenci metninde iç süreç dili ("PDF'te yok", "aday soru", "bağlanan çıkmış")
- **Kök:** yazar ajan kendi notunu öğrenci metnine bırakıyor.
- **Kapı — EKLENDİ:** `turkce_uslup.py` kalıpları (Kurul 2+ HATA). **"Doğrusu: …" yasak DEĞİL**: şık açıklaması standardının parçası. "ajan" tıbbi terimdir.

### H9 — Görsel ya da bozuk OCR'lı sayfa içerikte yok
- **Kural:** metni zayıf sayfa görüntüden okunur; sayfa kapsaması ölçülür.
- **Kapı — EKLENDİ:** işçi denetleyicisi zaten her sayfayı haritada, her içerik sayfasını bir adım + bilgi maddesinde ve
  şekil/tablo sayfasını açıklamalı istiyor (%100 kapsama). Eklenen: görsel ağırlıklı ya da hoca vurgulu (≥3 renkli/kalın)
  sayfa "boş/kapak" diye atlanamaz (s.1–2 kapak muaf) — `denetle.py`, 2026-10-20.

### H22 — Sesli derste dolgu ve asılsız "hoca vurguladı" cümleleri (kullanıcı kuralı, 2026-10-22, KALICI)
- **Belirti:** K1 sesli derslerinde "hoca bunu ayrıca vurgulamıştır", "hocanın altını çizdiği nokta şudur" gibi dayanaksız,
  sürekli tekrar eden meta cümleler; kelime/dakika sınırına ulaşmak için eklenen, dersi uzatıp bağlamdan koparan dolgu.
- **Kural:** Amaç bilgiyi en kısa yoldan, doğru, açıklayıcı ve eksiksiz iletmek. Kelime alt sınırı ve süre hedef DEĞİLDİR;
  kısa ama eksiksiz metin doğrudur. Önem vurgusu yalnız dayanağı varsa (çıkmış soru, öğrenci notu, slayttaki işaret) ve
  kritik noktada yapılır; dayanağı yazılmadan "hoca vurguladı/işaretledi/altını çizdi" denmez. Tekrar, geçiş ve özet
  dolgusu ("şimdi gelelim", "bir kez daha hatırlatalım", "daha önce de söylediğimiz gibi") yasak.
- **Kapı — EKLENDİ:** `scripts/uretim/sesli_anlatim/metin_denetle.py` → `DOLGU` kalıpları HATA; "Burası önemli/çok önemli/sınavda
  sık" bölüm sayısının yarısını (en az 3) aşarsa HATA; kelime alt sınırı artık yalnız uyarı. K1 metinlerine toplu müdahale yok.

### H23 — Öğrenci işaretli slayt yanlış yorumlandı + okunuşla yazılmış metin (İmmünofarmakoloji V2, kullanıcı, 2026-10-22)
- **Belirti:** İşaretli PDF'te sarı vurguların hepsi "işlendi" sayıldı, çapraz sarı şeritler kaçırıldı; metin "ce de iki" gibi
  okunuşla yazıldı; anlatım kopuk ve hızlıydı.
- **Kural (kullanıcı tanımı):** sarı ya da mavi ÇAPRAZ şerit/çizgi = hoca okumadı (anlatılmaz); metin üzerindeki YATAY
  çizgi/vurgu = okundu; yıldız, daire, "önemli", "bil", ünlem, altı çizili = önemli. Öğrenci notlu PDF önce sayfa sayfa
  işaret dökümüne (okundu/okunmadı/önemli/el yazısı) çevrilir, metin dökümden yazılır.
- **Yazım:** konuşma metni kısaltmaları yazımla tutar (CD2, IL-2); okunuşu EMA katmanı yapar (`modul_okunus.py`
  MODUL_ANAHTARLAR / Kurul 2+ uzun kısaltma yolu). Sayı, Yunan harfi ve simge yazıyla.
- **Anlatım:** akıcı, bağlantılı (ne → nasıl → nerede → yan etki); kısa kopuk cümle dizisi yasak.

### H24 — Kısa özet derste önemli yerler atlandı, slaytla ilişkisiz/kopuk anlatım (Patoloji V2, kullanıcı, 2026-10-23)
- **Belirti:** "%50 kısa" hedefli V2'lerde önem maddeleri ve çıkmış bilgileri atlandı; paragraflarda çıkmıştan koparılmış tek
  cümleler ("çıkmış soruda doğru önerme…", "… değildir" diye şık sayma), konu ortasında başka konudan bilgi; bir slayttan tek
  satır okunup başlığı bile açıklanmadan başka konuya geçildi.
- **Kural:** kısa sürüm slayt sırasını izler; önem listesinin (`src/data/<branş>_onem/`) TAMAMI ve her çıkmış konu içinde
  anlatılır; konu ne → neden/nasıl → sınav ayrıntısı sırasıyla kapanmadan geçilmez; soru dili ve şık yankısı yasak; uzunluk
  V1'in %45–65'i ("çok kısalt" diye madde atma). Yazar + bağımsız denetçi (kapsama dökümü + kaynak karşılaştırması) zorunlu.
- **Uygulama:** `meds_temp/sesli_anlatim/v3_pat/{TALIMAT,DENETIM}.md`, blok için `meds_temp/blok_ozet_v2/EK_V2.md`.
- **Ek tuzaklar:** ders–PDF eşlemesi içerikle doğrulanır (k1-65 Meme Kanseri Öğren destesi 33) Benign PDF'ine bağlıydı →
  sesli V2/V3 sanal deste `k1p-k1-65-…-sesli-v2`); kitte slayt metni yoksa (k1-66) PDF metni ayrıca verilir.

## H33 — Türkçe harfsiz metin kabul ediliyordu + kabul edilmiş iş yeni kapıdan geçirilmiyordu (2026-10-23 K2 provası)
- Gemini Flash-Lite bazı çözücü partilerini ve bir sesli bölümü baştan sona harfsiz yazdı ("dogum", "bagli", "oykusu");
  hiçbir kapı yakalamadı, partiler KABUL edildi (önceki e07 çözücü ve k1-64 sesli sınamalarında da vardı; yalnız geçici kopya).
- Ortak kapı `cekirdek.turkce_katlama`: sözlük paketin kendi girdisinden; girdide Türkçe harfle geçen kelimenin katlanmış
  biçimi ≥3 kelimelik bir alanda ≥2 kez varsa HATA (İngilizce alıntı, kimlik/tür alanı, büyük harfli OCR yanlış alarm vermez).
- Kabul edilmiş iş yeniden kullanılırken `yonlendir.kapi` ile güncel kapılardan geçirilir; geçemezse "yeniden" koşar.
- Betik onarımı `cekirdek.ses_onar` (SES_ONAR görevleri): ses alanlarında kısaltma/Roma rakamı `modul_okunus.donustur`
  ile ("MSH" → "mee see haa"); modelin üç turda düzeltemediği "büyük harfli kısaltma" hatası kalktı.
- Öncüllü soruda "kökle uzunluk uyumsuz" hatasına düzeltme ipucu eklendi (kok_ses öncüllerin hepsini okur).

## H36 — Cümle sayacı sıra sayısı noktasını cümle sonu sayıyordu (2026-10-24, oturum kuyruğu sınaması)
- "8-10. haftalarda" iki cümle sayılıp "4 cümle (en çok 3)" yanlış alarmı veriyordu; yazar ifadeyi bozarak geçiyordu.
- `CUMLE_SINIRI` (cozucu_dogrula2.py, cozucu_dogrula.py, spot_cozucu/asistan_dogrula.py): rakamdan sonraki nokta ancak
  ardından büyük harfle başlayan cümle gelirse sınırdır. Sayım yalnız azalabilir; veri değişmedi.

## H38 — Sesli ders v2 slayt adımı hiç gösterilmiyordu (2026-10-24)
- `konusma_v2.py` şemasında `slayt_adim` adım KİMLİĞİ (`k2-02-d-s05`); sunucu yalnız sayıyı kabul ediyordu → bütün K2
  cümlelerinde adım bağı boş. `canliDers.ts` ve `.medspak` kimlikten numarayı çözer. Paket kapısı bunu yakaladı.

## H39 — Sesli metin kısaydı: sayfa atlanıyor, şekiller anlatılmıyordu (2026-10-24, kullanıcı "ders süresi az")
- k2-02'de 56 içerik sayfasının 12'si anlatılmamış, 19 sayfa tek cümleyle geçilmişti; "kısa ve öz" + paralel üretimde kapı yoktu.
  Kapı `isle.sesli_kapsam` (sayfa + derinlik). Kelime/dakika hedefi YOK; derinlik bilgi maddesi sayısından.

## H55 — Görsel tablodan yanlış satır okundu; hocanın kendi çelişkisi kesin "sınav spotu" yapıldı (2026-10-24, k2-07)
- Bütün betik kapıları 0 HATA iken bağımsız tıbbi denetim (PDF ile satır satır) buldu:
  - s.63 Tablo 25.3 (görüntü): droperidol premedikasyon/sedasyon/antiemetik dozları **midazolama** yazılmış; kart, soru,
    checkpoint ve sesli metne yayılmış. Aynı tablonun opioid yarısı atlanmış.
  - s.6 "en zayıf desfluran" ↔ s.13 Tablo 25.1 MAK azot protoksit >100: iki zıt cevap öğretiliyordu. Kural: hocanın
    çelişkisi tek cümlede uzlaştırılır (halojenli uçucular içinde desfluran; tüm inhalerler içinde N₂O), kesin spot yapılmaz.
  - Tablodaki 0 değeri "seyrek" diye okunmuş (midazolam bradikardi); "(Katzung)", "standart kaynaklara göre" ekleri sızmış.
- Kural: Kurul 2+ her derste yayından önce PDF'le karşılaştıran bağımsız tıbbi denetim (ayrı oturum, yazar ≠ denetçi)
  zorunlu; görsel tablo satırı ilaç/değer eşlemesi görüntüden tek tek doğrulanır. Bulgular düzeltilip kapılar yeniden koşulur.

## H64 — Sayfa haritası adım numaraları tekrar sayfalarını saymıyordu; kısa/eksik kanıt (2026-10-26, k2-22 psikosomatik)
- **Belirti:** `denetle.py` 76 HATA: adım 8–31 için "pdfSayfalari [n] ama harita [n+1] diyor", başlık aralıkları içerik adımı değil, bilgi/harita alıntıları 3 kelime ya da yok.
- **Kök neden:** `sayfa_haritasi.json` `adimlar` alanı desteden ayrı, CHECKPOINT slaytları sayılmadan numaralandırılmıştı; her checkpoint'ten sonra kayma büyüdü. Yalnız görsel olan sayfalarda (s.6, s.30: kaynak.md metni yok) `alinti` yazılamadığı için kanıt boş bırakılmıştı; tablo/liste sayfalarında tek satırlık (3 kelime) alıntı seçilmişti.
- **Çözüm / kural:** Harita `adimlar`ı daima son destenin içerik slaytlarının `pdfSayfalari`ndan türetilir (checkpoint/oyun hariç); başlık `adimlar` = kapsadığı sayfaların ilk/son içerik adımı. Metinsiz görsel sayfada `kanit: {sayfa, gorsel: "≥4 kelime görülen"}` kullanılır; alıntı kaynak.md'de birebir geçen ≥4 kelime olur.

## H68 — H66 tekrarı + süs bölüm sayfaları `sekil` türünde (2026-10-26, k2-27 periyodik muayeneler)
- **Belirti:** `arsiv_yayinla.py`'de 15 `sesli_kapsam: çıkmış …: bilgisi anlatılmamış` + 8 "s. n (sekil) anlatılmamış" (bölüm başlık/kapanış süs sayfaları).
- **Kök neden:** (1) H66'nın aynısı: 248 cümlenin hiçbirinde `cikmis` dolu değil, ilgili 15 soru bağlanmamış. (2) `sayfa_haritasi.json`'da yalnız süs görselli bölüm başlık sayfaları (s.18, 26, 39, 51, 52, 107, 130, 135) `tur: sekil` yazılmış; kapı bunları anlatılacak şekil sayar.
- **Çözüm / kural:** Çıkmışlar `kanit.sayfa` cümlelerine bağlandı (c0003, c0037, c0047, c0101, c0112, c0204, c0213, c0218, c0222) ve sesli uyarı eklendi; süs bölüm sayfaları `tur: kapak` yapıldı. Haritacı, bilgi taşımayan bölüm başlık/kapanış sayfalarını `kapak` yazar; sesli yazar H66 adımını atlamaz. Kapı gevşetilmedi.

- **2026-10-26 (k2-29):** `cikmis_baglantilari.json`'da `ilgili: true` olan çıkmışın bilgisi cümlede anlatılsa da cümlenin `cikmis` listesine kimliği yazılmadı ve sesli uyarı yoktu → `sesli_kapsam` yayını durdurdu. Önleme: sesli metin yazarı her ilgili çıkmışı `kanit.sayfa` sayfasındaki cümleye bağlar ve o cümlede "bu bilgi çıkmışta soruldu" der (kapı: `isle.cikmis_ses_kapsam`).

## H70 — Mekanik 2 Cümlelik Şablon ve Yüzeysel Anlatım Yasağı (Sıfır Bilgi Kaybı ve Amfi Derinliği Standardı) (2026-10-26, k2-48 lokal anestezikler)
- **Belirti:** Kullanıcı uyarısı: *"Son eklenen dersler hep eksik anlatılmış içeriklerinin neredeyse %60'ı yok"*. 37 sayfalık amfi dersi yalnızca 74 cümle ve 839 kelime (~6.7 dakika) ile geçiştirilmiş; slaytlardaki kimyasal gruplar, spesifik formülasyonlar (Anestol, EMLA, Jetex, Lidestol, Lincaine, LMX-4, Vemcaine), subkutan maksimum doz tablosu (Ultrakain, Citanest, Marcaine, Naropin), potens katsayıları (tetrakain/bupivakain 16 kat), difüzyon ve iyonizasyon eğrileri (pKa 7.9 lidokain vs 8.1 bupivakain), toksisite basamakları, diazepam premedikasyonu ve %20 intravenöz lipid emülsiyon protokolü sesli anlatımda yer almamıştı.
- **Kök neden:** Taslak ve sesli metin üretiminde sayfa başına mekanik olarak tam 2 kısa cümle yazan bir şablon kullanılmış; bu şablon kapıların asgari kelime/sayfa şartlarını yüzeysel olarak karşılasa da gerçek amfi anlatımının %60–75'ini dışarıda bırakmıştı.
- **Çözüm / kural:** Sayfa başına yüzeysel 2 cümlelik kopyala-yapıştır şablonlar KESİNLİKLE YASAKTIR. Her slayt için amfi ders notundaki tüm maddeleri, tabloları, spesifik ilaç isimlerini, maksimum dozları ve patofizyolojik mekanizmaları kapsayan 3 ila 6 zengin cümle yazılmalıdır (35–70 slaytlık dersler için 140–250+ cümle, ~2000–3500 kelime, 15–25 dakika anlatım derinliği). K48 bu standartla baştan üretildi (144 cümle, 2438 kelime, 68 atomik bilgi, 10/10 çizim, 6.23 MB .medspak) ve 0 HATA ile Oracle canlı ortamına alındı.


## H71 — PDF metnindeki ayrışık (decomposed) harfler terim eşleşmesini bozuyordu (2026-10-26, k2-07 genel anestezik ilaçlar)
- **Belirti:** `terim_sozlugu.py dogrula` doğru yazılmış terimler için "bu sayfanın metninde bulunamadı" HATAsı verdi: "retiküler aktive edici sistemde", "Antikonvülzandır", "venöz irritasyon". Slayt metnini `dok` çıktısında da "retiküler" gibi bozuk görünüyordu.
- **Kök neden:** PDF'ten gelen kelimede "ü" tek kod noktası değil, "u" + birleşik inceltme (U+0308) olarak ayrışık yazılmıştı. `TOK` düzeni birleşik işareti kelime karakteri saymadığı için kelime iki parçaya bölünüyor, `katla()` sonrası "antikonvu" + "lzandir" gibi anlamsız parçalar oluşuyordu; terim hiçbir zaman eşleşmiyordu.
- **Çözüm / kural:** `Sayfa` sınıfı PDF kelimelerini okurken `unicodedata.normalize("NFC", w)` uygular; `bul()` de terimi NFC'ye çevirip token'lara ayırır. Kapı gevşetilmedi. Yeni PDF okuyan her betik kelimeleri NFC'ye çevirmeden eşleştirme yapmamalıdır.

## H72 — Çok sözcüklü terimin kısa son sözcüğü ek aldığında eşleşmiyordu (2026-10-26, k2-07 genel anestezik ilaçlar)
- **Belirti:** "Serebral metabolik hız" terimi slaytta "Serebral metabolik hızın azaltılması" olarak geçtiği hâlde "bulunamadı" HATAsı verdi.
- **Kök neden:** `ek_mi()` yanlış eşleşmeyi önlemek için 4 harf ve altındaki sözcüklerde yalnız birebir eşleşmeye izin veriyordu; "hız" 3 harf olduğu için "hızın" reddediliyordu. Oysa terimin önceki sözcükleri ("serebral metabolik") bağlamı zaten daraltıyor.
- **Çözüm / kural:** `ek_mi(..., kisa_izin=True)` yalnız **çok sözcüklü** terimin **son** sözcüğünde ve terim en az 8 karakterken kullanılır; tek sözcüklü kısa terimlerde (kısaltmalar) davranış değişmedi. Eşleşme gevşetilmedi, yalnız Türkçe ek kuralı bağlamla birlikte uygulandı.

## H74 — Madde imi kelimeye yapışık gelince terim işaretlenemiyordu (2026-10-26, k1-35 prenatal tanı)
- **Belirti:** "CVS", "Fetoskopi", "Koryon villus biyopsisi", "PAPP-A", "İnvaziv yöntemler" terimleri slaytta açıkça yazdığı hâlde kapı "bu sayfanın metninde bulunamadı" HATAsı verdi.
- **Kök neden:** Slaytlarda madde imi Wingdings "o" karakteridir ve PDF metnine kelimeye bitişik geliyor ("oCVS", "oFetoskopi", "oİnvaziv"). `TOK` bu birleşik diziyi tek kelime saydığı için "ocvs" üretiliyor, gerçek terim hiç eşleşmiyordu.
- **Çözüm / kural:** `Sayfa` kelimeyi okurken baştaki "o" yalnız **ardından büyük harf geliyorsa** (madde imi kalıbı) ayrılır; kutu aynı kalır. Madde başındaki terimler de artık işaretlenir. Kapı gevşetilmedi.

## H75 — Gündelik Türkçe sözcükler terim diye işaretlenmişti (2026-10-26, tüm dersler)
- **Belirti:** Öğren ekranında "Büyüme", "Kanama", "Gelişim", "Sarılık", "İyileşme", "Kalp yetmezliği", "Bilinç" gibi gündelik sözcükler terim gibi altı çiziliyor, dokununca sözlük tanımı açılıyordu; okuma bölünüyordu.
- **Kök neden:** Terim dosyalarının bir bölümü, `turkce_kokenli` kapısı eklenmeden önce `otomatik`/sözlük yolundan üretilmişti. Sözlükte bu sözcükler "terim" olarak kayıtlı olduğu için işaretlenmiş, kapı sonradan eklendiğinde dosyalar bir daha denetlenmediğinden canlıda kaldılar (kapı yalnız yeni yazımı denetliyor, var olan dosyayı taramıyordu).
- **Kalıcı çözüm:** `terim_sozlugu.py ayikla [--yaz]` bütün terim dosyalarını (canlı + arşiv) tarayıp kapının reddettiği ögeleri çıkarır; terimi kalmayan sayfa/dosya kaydı silinir (hiçbir dosyada boş `t` dizisi bulunmaz). Bu turda 514 öge ayıklandı, kapı gevşetilmedi.
- **Önleme kuralı:** Terim kapısı kuralı değiştiğinde yalnız yeni dosya değil, **tüm mevcut dosyalar** yeni kuralla yeniden taranır (`ayikla`), sonuç canlıya dağıtılır.

## H76 — Cümle sayısı kapısı kısaltma noktalarını cümle sonu sayıyordu (2026-10-26)
- **Belirti:** "Gebeliğin 20. ile 37. haftaları arasında gerçekleşen doğumdur" ya da "Geniş spektrumlu 3. kuşak sefalosporindir" gibi tek/iki cümlelik açıklamalar "en çok 2 cümle" HATAsı veriyordu; 167 terim bu yüzden canlıda kural dışı görünüyordu.
- **Kök neden:** Denetim `[.!?](\s|$)` kalıbıyla her noktayı cümle sonu sayıyordu. Sıra sayısı ("3."), ölçü ("20.") ve tür kısaltması ("N. gonorrhoeae", "C. trachomatis") noktaları da sayıldığı için cümle sayısı şişiyordu.
- **Kalıcı çözüm:** Cümle sonu ancak noktadan sonra **büyük harf** ya da metin sonu geliyorsa sayılır (`[.!?](?=\s+[A-ZÇĞİÖŞÜ]|\s*$)`). Gerçek üç cümleli açıklama hâlâ HATA alır; kural gevşemedi, yanlış sayım düzeldi. Ayrıca "frenler"/"çapası" gibi çeviri mecazları (8 terim) doğal Türkçeyle yeniden yazıldı.

## H77 — Kısaltma katmanı eklenirken üç ayrı tuzak: büyük harfli Türkçe sözcük, tireyle bitişik yazım, dağıtım listesi (2026-10-26, Kurul 2 · 60 ders)
- **Belirti:** Slayt kısaltmaları (ÜSYE, DD, VUR, DSM-5, MAO-A, 5-HTTLPR …) işaretlenirken (a) "BİLİNÇ", "KOMA", "NÖBET", "CEYLAN" gibi büyük harfli Türkçe sözcükler/başlıklar kısaltma sanıldı, (b) "DSM-5", "MAO-A", "HIV-1", "GABAA-reseptör", "5-HTTLPR", madde imli "o5-HTT" yazımlarında "kutular bulunamadı" HATAsı verdi, (c) kısaltma dosyaları yazıldığı hâlde canlıya hiç ulaşmadı.
- **Kök neden:**
  1. Kısaltma sezgiseli yalnız "büyük harf dizisi" kalıbına bakıyordu; Türkçe sözlük (hunspell) denetimi yoktu.
  2. Kutu araması terim kapısının `bul()` kuralını kullanıyordu; bu kural yalnız **tam kelimeyi** (ya da Türkçe ekini) eşler. Tireyle/rakamla bitişik yazımlarda kısaltma ayrı bir kelime olmadığı için hiç bulunamıyordu. Ayrıca madde imi "o" yalnız ardından **büyük harf** gelirse ayrılıyor; "o5-HTT" gibi rakamla gelen yazımda "o5-" önek olarak kalıyordu.
  3. `deploy-code.sh` [1b] veri listesine `kisaltma` eklenmemişti (H73'ün aynısı).
- **Çözüm / kural:**
  1. `kisaltma_mi()` artık `/usr/share/hunspell/tr_TR.dic` köklerini (ek soyma ile) kullanır: sözlükte bulunan büyük harfli sözcük kısaltma sayılmaz. Bilinen/elle sözlükte (`kisaltma_bilinen.json`, `kisaltma_elle/`) açıkça tanımlı kısaltmalar (SAK, KS gibi Türkçe sözcüğe benzeyenler) bu filtreden muaftır.
  2. `kutular()` eklendi: tam eşleşme yoksa kısaltma, kelime içinde **önek/sonek sınırı** denetlenerek (ör. "o5-httlpr", "t12-l1", "dsm-iii-r", "gabaa-reseptor") karakter oranıyla daraltılmış kutuda işaretlenir. Kapı gevşetilmedi; yalnız doğru konum hesaplandı.
  3. Dağıtım listesine `kisaltma` eklendi; canlı API'de `kisaltma` alanı `curl` ile doğrulandı.
- **Önleme kuralı:** (i) Her yeni veri türü hem `canliDers.ts` yol tanımına hem `deploy-code.sh` [1b] listesine yazılır. (ii) Kısaltma/açılım **yalnız dersin kendi metninden ya da elle/bilinen sözlükten** alınır; metinde açılımı olmayan kısaltmaya tahminle açılım yazılmaz (yanlış açılım, eksik açılımdan kötüdür).

## H80 — Öğrenci Drive betiği uzantısız PDF'i not saymadı; kısaltma bulucu "HT+DM" yazımını kaçırdı (2026-10-27)
- **Belirti:** Öğrenci notu "Nöroloji 1 - Nörolojik Hastaya Yaklaşım" (uzantısız PDF) envanterde "diger" kaldı; slayttaki HT, DM,
  EP kısaltma sözlüğüne girmedi.
- **Kök neden:** Sınıflama yalnız uzantıya bakıyordu; kısaltma bölme deseni `+` işaretini ayırıcı saymıyordu; "EP" hunspell'de
  Türkçe sözcük sayılıp elendi.
- **Çözüm / kural:** Tür MIME'den de belirlenir; bölme deseni `[/\-–+]`; EP `kisaltma_bilinen.json`'a eklendi.
  `degerlendirme_dogrula.py` slayttaki her kısaltmanın sözlükte olmasını HATA ile ister.

## H89 — Slayttaki yapışık madde imi glifi (U+F06E) kısaltmayı ve kanıt eşlemesini bozdu (2026-10-27, k2-02/k2-03)
- **Belirti:** "KB" (kan basıncı) kısaltması sözlüğe girmedi; değerlendirme kapısı slayt metninde birebir geçen kanıtları "yok" saydı.
- **Kök neden:** PowerPoint madde imi özel kullanım alanı karakteri (``) sözcüğe boşluksuz yapışık geliyor; kısaltma bölme
  deseni ve kapı normalleştirmesi bu karakterleri ayırıcı saymıyordu.
- **Çözüm / kural:** `kisaltma_sozlugu.adaylar` ve `degerlendirme_dogrula.norm` U+F000–F8FF ve madde imi işaretlerini ayırıcı/boşluk
  sayar. Yeni metin işleyen her betik slayt metnini bu karakterlerden arındırarak karşılaştırır.

## H92 — Bilinen kısaltma sözlüğü bağlamsız: MSS "Muskuloskeletal sistem" diye açıldı (2026-10-27, k2-03/k2-04)
- **Belirti:** Nöropatoloji derslerinde MSS kısaltma kartında "Muskuloskeletal sistem"; slayt "MSS-SSS: Merkezi-Santral Sinir Sistemi" diyor.
- **Kök neden:** `kisaltma_bilinen.json` her kısaltmaya dersten bağımsız tek açılım verir ve `otomatik` slaytın kendi tanımına bakmaz.
- **Çözüm:** derse özel `data/sesli_anlatim/kisaltma_elle/<key>.json` (`MSS: Merkezi sinir sistemi`), elle eşleme bilinenden önce gelir.
- **Önleme kuralı:** her derste kısaltma listesi (kısaltma = açılım) yazdırılıp slayt metniyle okunur; branşa göre anlamı değişen
  kısaltma (MSS, KB, BOS …) için derse özel eşleme yazılır, genel sözlüğe yeni anlam eklenmez.

## H105 · Harita `adimlar` = deste `slideNumber` (checkpoint dahil); iskelet ajanı içerik adımlarını 1..N saydı (2026-10-27, k2-08)
- **Belirti:** Deste birleşince `denetle.py` 138 HATA (adım X: pdfSayfalari … ama harita … diyor).
- **Kök neden:** TALIMAT §1b "içerik adımı" diyor; denetleyici `adimlar`'ı destedeki slideNumber olarak okuyor, araya giren checkpoint slaytları numaraları kaydırıyor.
- **Çözüm:** Deste birleştirildikten sonra haritadaki k. içerik adımı → k. içerik slaytının slideNumber'ına çevrildi (sayfa kayıtları ve ana başlık aralıkları).
- **Kural:** Harita deste birleşmeden planlı sayıyla yazılır; birleştirmeden sonra slideNumber'a çevrilir ve `denetle.py` yeniden çalıştırılır (TALIMAT §1b'ye not eklendi).

## H106 · `baglam.kazanimlar` kapak metninden türetilmiş çöp şablon cümleler içeriyor (2026-10-27, k2-08)
- **Belirti:** "BEYİN VE İSKELET sİSTEMİ GELİŞİMİ gENETİĞİ dr. Öğr. Üyesi Serap ARSLAN … mekanizmasını ve klinik önemini analiz eder." gibi kazanımlar.
- **Kök neden:** `isle.kazanimlar` kayıtlı kazanımı olmayan derste konu adından şablon kurup PDF kapak satırlarını da içine alıyor; TALIMAT "varsa baglam.kazanimlar'ı aynen kullan" dediği için işçi bunları ders paketine kopyalar.
- **Çözüm:** k2-08 kazanımları dersten elle yazıldı (8 ölçülebilir kazanım).
- **Kural:** Genel şablon ("temel kavramlarını … analiz eder") ya da kapak metni içeren kazanım kullanılmaz. Açık iş: `isle.kazanimlar` kayıt yoksa boş dönmeli (kod düzeltmesi bu turda yapılmadı).

## H108 · Kısaltma kapısı slayttaki gen sembollerini ve slayt yazım hatalarını (LMXIB, WTI) Faz A'da HATA sayıyor (2026-10-27, k2-08)
- **Belirti:** `degerlendirme_dogrula.py` 19 HATA: OTX, MSX, SRY, TWIST, MITF, HOXA, HOXD, DCX, LFNG, FND, FGFR, MD, HMG, HD, TGF, LMXIB, WTI "sözlükte yok".
- **Kök neden:** Kapı `src/data/kisaltma_sozluk.json`'a bakıyor; kısaltma katmanı (aşama 10) daha sonra çalışıyor, arşivdeki y25 sözlüğü yalnız bazı genleri taşıyor; slayt yazım hatası (LMXIB, WTI) ayrı anahtar sayılıyor.
- **Çözüm:** 17 anahtar yalnız bu ders için eklendi (açılım standart, slayttaki yazım hatası belirtilerek).
- **Kural:** Genetik derslerde Faz A'da slayttaki gen sembolleri + kısaltmalar sözlüğe önce eklenir; yazım hatalı sembol (LMXIB/WTI) aynen ayrı anahtar olur ve açılımında doğru gen belirtilir.

## H110 · Kısaltma kapısı `kisaltma_elle`deki OD/OR/ID/SED'i "kısaltma biçiminde değil" diye reddetti (2026-10-27, k2-08 Tıbbi Genetik)
- **Belirti:** `kisaltma_sozlugu.py denetle` 12 HATA: OD, OR, ID, SED "kısaltma biçiminde değil"; `otomatik` aynı kısaltmaları (slaytta onlarca kez geçen "OD kalıtım") hiç aday saymadı.
- **Kök neden:** `kisaltma_mi()` büyük harfli sözcüğü Türkçe sözlükte (hunspell) bulursa eler (od, or, id, sed); istisna yalnız genel `kisaltma_bilinen.json` içindi, dersin kendi `kisaltma_elle/<key>.json` anahtarları dikkate alınmıyordu (H92'nin önerdiği branşa özgü elle sözlük bu yüzden OD/OR için işe yaramıyordu).
- **Çözüm:** `ELLE_AKTIF` (işlenen dersin elle anahtarları) `kisaltma_mi`de kabul edilir; `k_adaylar/k_otomatik/k_dogrula` başında doldurulur. Çok anlamlı kısaltma (CVS: kardiyovasküler sistem s.49 / koryonik villus örneklemesi s.70) genel sözlüğe konmaz, sayfa bazlı yazar dosyasıyla verilir.
- **Kural:** branşa özgü, Türkçe sözcüğe benzeyen kısaltma (OD, OR, ID, SED) dersin `kisaltma_elle` dosyasına yazılır; genel `kisaltma_bilinen.json`a eklenmez.

## H112 · İlk anlatım taslağı öğrenci denetçide KALDI: aynı sözcük iki anlamda, kilit kavram tanımsız, gen sembolü okunuşu çözülemedi (2026-10-27, k2-08)
- **Belirti:** bağımsız denetçi tur 1 KALIR: "tip bir kollajen" ile "osteogenezis imperfekta tip bir" aynı sesle okunup karışıyor; distrofinin işlevi ve "okuma çerçevesi" anlatılmadan ekzon rakamları verilmiş; sklerotom/dermatom/miyotom türevsiz; kraniyoraşizis tanımı anensefaliyle çakışıyor; WT1 "çifte ve te bir" çözülemedi; "Hoca da ... söyledi" onaylama cümleleri bilgi taşımayıp dolgu hissi veriyor.
- **Kök neden:** slayt satırı sırasıyla yazılırken ses dinleyicisinin görmediği ayrım (tip/tür) ve kilit kavramın önceden tanımı atlandı; Hoca atfı "her yerde ekleyelim" refleksiyle kuruldu.
- **Çözüm:** kollajen için "birinci/üçüncü tür", hastalık için "birinci tip" kullanıldı; okuma çerçevesi ve distrofin işlevi kısaca tanımlandı; somit türevleri, kraniyoraşizis tanımı düzeltildi; W harfi "duble ve" okunur; yalnız yeni bilgi (ayırt edici vurgu, klinik örnek, tedavi) taşıyan hoca atıfları kaldı. Tur 2 GEÇER (%90 yanıtlanabilirlik).
- **Kural:** sesle okunan metinde aynı sözcük iki ayrı kavramı gösteriyorsa yazım ayrıştırılır; sayısal/ekzon gibi kavram ancak tanımından sonra kullanılır; "hoca da ... söyledi" yalnız slaytın vermediği ek bilgi ya da sınav vurgusu içerdiğinde yazılır.

## H105 · Sıralı tabloda adım atlanıyordu (k2-05, 2026-10-27)
- **Belirti:** "Muayene başlıklarının sırası" tablosu 1, 2, 4, 5 diye gidiyordu; Motor sistem yoktu (Öğren tablosu + ders içerik sekmesi).
- **Kök neden:** Yazar parçası (`uret/parca_A.json`) interactive_table'ı yazarken 3. satırı atlamış; slayt metni beş başlığı doğru sayıyordu, tabloyla metin kıyaslanmadı. `ders_icerik_uret.py` tabloyu aynen kopyaladığı için hata iki yüzeye taşındı.
- **Çözüm:** 3. satır (Motor sistem) parça, taslak deste ve `interactive_learning_decks.json`'a eklendi; ders içerik paketi yeniden yazıldı.
- **Kural:** Sıra/Adım sütunlu tablolarda numaralar 1'den kesintisiz olmalı ve slayt metnindeki sayımla eşleşmeli (`docs/DERS_ICERIK_BICIMI.md`). Kapı: `scripts/uretim/ders_icerik/sira_kapisi.py`.

## H118 · Anlamsız karşılaştırma tabloları (Öge / Sınıf / Gerekçe) (2026-10-27)
- **Belirti:** "Anatomik basamak mı, muayene başlığı mı?" gibi karşılaştırma kartı/tablosu: Türkçesi bozuk, tıbbi olarak anlamsız ve öğretmiyor.
- **Kök neden:** `ders_icerik_uret.py` tüm karşılaştırma tipli Öğren ögelerini (swipe_matching, venn_grid, feature_bidding) koşulsuz tabloya çeviriyordu; yazar, öğretilmiş iki tıbbi kavram yerine "üst kategori etiketi" (basamak/başlık) ile sınıflama kurmuştu.
- **Çözüm:** swipe_matching tablo dışı bırakıldı; venn/feature_bidding yalnız ≥3 satır, her gerekçe ≥7 kelime ve benzersizse alınır.
- **Kural:** Karşılaştırma yalnız iki GERÇEK tıbbi kavramı (hastalık, yapı, ilaç, mekanizma) ayırt eder; "X mi Y başlığı mı" gibi meta sınıflama, tek cümlelik özdeş gerekçe, bozuk Türkçe yasak. Yazar parçalarında da yazılmaz; yazar/denetçi bunu kontrol eder.
- PDF/yazdırma: belge yalıtılmış iframe'de yazdırılır; uygulama DOM'unda yazdırma ve sayfa yüksekliğine eşit sabit yükseklik YASAK (boş sayfa/renk karışması).

## H109 · Ders içerik kayıtlarında "Slayt s.N" kaynağı eksik (2026-10-28)
- **Belirti:** k2-05 Terimler ekranında bazı terimlerde slayt/sayfa rozeti yoktu; k2-01..08 paketlerinde 650'den fazla terim `s` taşımıyordu; "Checkpoint" gibi slayt iskeleti ve slaytta olmayan "Afferent / efferent" terim olarak yazılmıştı.
- **Kök neden:** `ders_icerik_adim.py` terime `adim` yazıyor ama PDF sayfası `s`'yi yazmıyordu; doğrulayıcı yalnız `adim` eksikliğine bakıyordu, ekranın gösterdiği `s` denetlenmiyordu.
- **Çözüm:** `scripts/ders_icerik_kaynak.py` (adim→slayt→pdfSayfalari[0]) tüm paketlere uygulandı; kaynaksız iki terim silindi; `ders_icerik_dogrula.py` `s` eksikse ve iskelet terimde HATA verir.
- **Kural:** Ekranda gösterilen her kaynak alanı doğrulayıcıda zorunlu olur; sayfa uydurulmaz, bulunamayan kayıt silinir (el kitabı §19 11a).

## H125 · Ders içerik terimlerinde genel sözlükten bağlam dışı tanım, kopya terim, ipuçlu soru şıkkı (2026-10-28, k2-08)
- **Belirti:** Genetik dersinde "Taşıyıcı" patojen taşıyıcısı, "Frajilite" serviks muayene bulgusu, "Kollajen" skar dokusu/C vitamini,
  "Biyopsi" cerrahi biyopsi türleri, "Nematod" parazit listesi, "Polihidramniyoz" konjenital kızamık bağlamıyla tanımlanmıştı;
  mikrosefali/makrosefalide kaynaksız "±3 SD" eşiği vardı. 306 terimin 33'ü kopyaydı (Drosophila ×2, Zebra balığı/Zebra fish,
  Nörülasyon/Nörulasyon, "G380R" ile "G380R mutasyonu", Preaurikuler çukur ×3). 15 örnek soruda doğru şık ötekilerden belirgin uzundu.
- **Kök neden:** (1) Terim tanımları dersin sayfasından değil sitenin genel sözlüğünden alındı; sözlükteki ilk anlam (başka branş)
  dersin bağlamına bakılmadan kopyalandı. (2) İki ayrı terim geçişinin çıktısı birleştirilirken ad normalleştirmesi yapılmadı.
  (3) Soru yazarı doğru şıkkı eksiksiz tanımla yazıp çeldiricileri kısa bıraktı; uzunluk denetimi yoktu. (4) pdftotext slayt madde
  imini "o" harfi olarak kelimeye yapıştırıyor ("oOsteogenezis"); kelime eşlemeli her denetim bu yüzden yanlış sonuç veriyordu.
- **Kural:** Terim tanımı dersin sayfasındaki bağlamla yazılır (genel sözlük yalnız yardımcıdır, ilk anlamı kopyalanmaz); kaynakta
  olmayan sayı/eşik yazılmaz. Terim eklemeden önce ad + `e` eşanlamları normalleştirilip kopya aranır; slayttaki yazım farkı
  (Gl13, FLBN, speksifikasyon) `e`'ye girer. Şekilden okunan kayıt `gorsel: true`. Doğru şık çeldiricilerle benzer uzunlukta yazılır.
- **Kapı — EKLENDİ:** `scripts/hat/tam_hat/kaynak_kapisi.py` (terim adı sayfada mı → HATA; tanım az örtüşüyorsa UYARI, denetçi bağlamı okur),
  `soru_uslup.py` (≥6 kelimelik doğru şık en uzun ve 1,8× → HATA), `hazirlik.py` madde imi temizliği.

## H127 · Slayttaki şekil/deney anlatılmadı, "ders yorumuna girmez" diye geçildi (2026-10-28, k2-05 Nörolojik Muayene, sayfa 32–33)
- **Belirti:** VIII. sinir slaytında Rinne/Weber diyapazon çizimleri (mastoid → kulak önü; verteks + normal / iletim tipi / sensörinöral üç panel) vardı. Anlatım "Bu çizimde testlerin nasıl uygulandığı gösterilir" deyip geçti; testin neden yapıldığı, hangi panelin hangi sonucu gösterdiği söylenmedi. Önceki paragraf "ders bunların nasıl yorumlandığına girmez, yalnız adlarını verir" dedi.
- **Kök neden:** yazar "kaynak dışı bilgi yasak" kuralını yalnız slayt YAZISINA uyguladı; şekil, çizim, fotoğraf ve tablodaki bilgiyi kaynak saymadı. Yazıda yorum olmayınca çizimdeki normal/patolojik ayrımı da "kaynakta yok" diye atladı ve boşluğu meta cümleyle kapattı. Kapılar (metin_denetle, turkce_uslup, denetçi) bu kaçamak cümleyi yakalamıyordu; denetçi slayta bakmadan okuduğu için şeklin anlatılmadığını göremedi.
- **Kalıcı çözüm ve kural (Şekil ve deney anlatım kuralı, `KURUL2_DERS_STANDARDI.md` §8.12):**
  1. **Şekil kaynaktır.** Slayttaki çizim, fotoğraf, şema, grafik, tablo, mikroskopi ve görüntüleme; içindeki oklar, etiketler, işaretler (X, kesik/kalın çizgi, renk), panel karşılaştırmaları ders içeriğidir ve anlatılır. "Slaytta yazmıyor" şekli atlama gerekçesi değildir.
  2. **Deney/test/muayene görseli** her zaman beş soruyla anlatılır: (a) ne sınanır ve neden yapılır, (b) nasıl uygulanır (görselde ne görülüyorsa adım adım), (c) normal sonuç, (d) her patolojik panel/sonuç ne demektir ve hangi lezyonu gösterir, (e) sonuçlar birbirinden nasıl ayrılır (sınavda karıştırılan çift).
  3. **Çok panelli şekil:** her panel ayrı ayrı adlandırılır ve karşılaştırılır ("soldaki normal…, ortadaki…, sağdaki…"); işaretlerin anlamı (X = hasarlı yapı, kalın ok = sesin daha güçlü duyulduğu taraf) açıklanır.
  4. **Yalnız adı geçen kavram/test:** ilk geçtiği yerde 1–2 cümleyle ne olduğu ve ne ölçtüğü söylenir (Terim kuralı §8.5). Ayrıntı slaytta/şekilde ya da hoca dökümünde varsa o kadar açılır; yoksa uydurma yorum eklenmez ama ADI DA BOŞ BIRAKILMAZ.
  5. **Kaçamak meta cümle YASAK:** "ders bunun yorumuna girmez", "yalnız adını verir", "ölçütünü vermez", "şekilde ayrıntı yok", "nasıl uygulandığı gösterilir" gibi öğrenciye bir şey öğretmeyen cümleler yazılmaz. Gerçekten kaynakta bilgi yoksa cümle hiç yazılmaz; konu olduğu kadar anlatılır.
  6. **Şekil paragrafı betimlemeyle bitmez:** yalnız "…gösterilir / görülür / yer alır" cümlelerinden oluşan şekil paragrafı eksik sayılır; şeklin öğrettiği bilgi (mekanizma, sonuç, ayırıcı nokta) eklenir.
  7. **Çizim katmanı anlatımı izler:** her panel/sonuç anlatılırken lazer ve kontur o panele gider (kural 17/18; bir cümle = bir panel).
  8. **Denetçi şekle bakar:** bağımsız denetçi metni okuduktan sonra şekilli/tablolu her sayfanın görüntüsüne bakıp "şekildeki her panel/işaret anlatıldı mı" listesini işaretler; eksik varsa GEÇMEZ.
- **Otomatik kapı:** `metin_denetle.py` kaçamak meta cümleyi HATA sayar (`KACAMAK` kalıpları); yalnız betimleme cümlelerinden oluşan kısa şekil paragrafını UYARI olarak gösterir.
- **Uygulama:** k2-05 v1 korunur; `k2-05-norolojik-muayene-v2` klipli ses + taşınan katmanlarla yeniden kuruldu, 31–32. paragraflar bu kurala göre yeniden yazıldı.

## H434 — Sesli derste "bu hastalıkta" gibi adsız göndermeler hangi hastalığın kastedildiğini karıştırıyordu (2026-10-28, kullanıcı bildirdi)
- **Belirti:** Yeni parçaya geçildiğinde "bu hastalıkta…" diye başlayan cümlelerde öğrenci, derste birden çok hastalık anlatıldığı için hangisinden söz edildiğini kaçırıyordu.
- **Kök neden:** Yazım yalnız yazıyı okuyan biri için akıcıydı; gönderme önceki cümleye bağlı. Sesli dinlemede parça sınırında bağlam kopuyor, kapılar bu kalıbı denetlemiyordu.
- **Çözüm/kural:** Her yeni paragraf/bölüm hastalığı veya kavramı adıyla anar; adsız gönderme (bu hastalıkta/durumda/tümörde, burada, bunlarda…) parça başında yasak. `metin_denetle.py` BAGLAMSIZ kapısı HATA verir; KURUL2_DERS_STANDARDI §8.13 ve ANLATIM_KURGU_STANDARDI'na yazıldı. Denetçi her paragrafı tek başına okuyup konuyu çıkarabilmeli.

## H438 — Anlatım slaytın söylediğini tersine çevirdi (k2-01, 2026-10-29)
- **Belirti:** s.4 slaytı "BT, MR tanının doğru olduğunu göstermek için çekilir" derken anlatım "BT ve MR bu hastalıkları doğrulamak için çekilmez" dedi; öğrenci çelişki gördü.
- **Kök neden:** yazar "yapısal nedeni dışlamak" yorumunu öne çıkarırken slayt cümlesini olumsuza çevirdi; denetçi slayt satırıyla anlatım cümlesinin yönünü (olumlu/olumsuz) kıyaslamadı.
- **Çözüm/önleme:** cümle slayt ifadesine döndürüldü ("tanının doğru olduğunu göstermek için çekilir"), açıklama sonraki cümlede ("başka yapısal nedeni dışlamak"). Anlatım slayttaki hükmü yorumlayabilir ama **yönünü tersine çeviremez**; denetçi her sayfada slayt cümlesi ↔ anlatım cümlesi olumsuzluk kıyası yapar. Değişen cümlenin EMA klibi yeniden üretilmelidir.

## H446 — Öğrencinin en çok çalıştığı ve çıkmışta sorulan bilgi anlatımda "ders yalnız adıyla sayar" diye geçiştirildi (2026-10-30)
- **Belirti:** k2-05 Nörolojik Muayene anlatımında "Spastisite ve rijidite kas tonusunun artmasıdır; ders ikisini yalnız adlarıyla sayar."
  Oysa 2025-26 öğrenci notunda rijidite = "agonist ve antagonist kaslarda birlikte tonus artışı" (el notu + yıldız) ve çıkmışta tam bu
  soruldu; 2. motor nöronda fasikülasyon, spastisite = 1. motor nöron, intensiyonel tremor da notta işaretli/çıkmışta var, anlatımda yok.
- **Kök neden:** işçi önemi yalnız bu yılın slayt metni + çıkmış eşlemesinden kuruyordu; slaytta yalnız adı geçen kavramın hocanın derste
  verdiği ve öğrencinin not ettiği tanımı kaynak sayılmıyordu. Geçmiş yıl öğrenci derlemeleri (hangi yer çalışıldı, hangi soru yapıştırıldı)
  hatta hiç girmiyordu; kapsam kapıları konu düzeyinde ölçtüğü için "rijidite" sözcüğünün geçmesini kapsam sandı.
- **Kural:** AGENTS 28 — geçmiş yıl öğrenci önem notu (`src/data/ogrenci_onem/`, `docs/OGRENCI_ONEM/<ders>.md`) her 2026-27 dersinde zorunlu
  malzemedir: A birimi anlatımda ayrıntılı (tanım → ayırt edici nokta → sayı/ölçüt → komşu kavram), önem listesinde `ogrenci` etiketli
  madde, ≥2 örnek soru; B birimi anlatımda açık + ≥1 soru. Slaytta yalnız adı geçen kavram, notta/çıkmışta tanımı soruluyorsa tanımıyla anlatılır.
- **Önleme:** "ders yalnız adını verir / yalnız adlarıyla sayar" türü geçiştirme, kavram öğrenci notunda ya da çıkmışta tanımıyla geçiyorsa yasaktır.
- **Kapı:** `python3 scripts/uretim/ogrenci_onem/kapi.py <ders>` 0 HATA — bilgi düzeyinde (el notu, vurgulu satır, çıkmış önermesi) anlatım ve önem
  listesi cümlelerinde arar (vektör + kelime kökü örtüşmesi; yalnız vektör "spastisite ve rijidite" cümlesini rijidite tanımı sanıyordu).
- **Ek (2026-10-30, kapı):** `kapi.py` ilk sürümü sesli metni (okunuşla: "Düşen", "müsküler") yazılı çıkmışla ("Duchenne muskuler")
  karşılaştırıp anlatılmış bilgiyi "yok" sayıyordu (k2-08). Çözüm: v2 `ekran` maddeleri (yazımla) da aday cümledir. Önleme: sesli metinle
  yazılı kaynağı karşılaştıran her kapı ekran/yazım katmanını da okur; kapıyı geçmek için sesli metin yazıma çevrilmez (H23).

## H472 — Hoca vurgusu `konu` alanı özetti, değerlendirme kapısı slayttan birebir istiyor (2026-11-02)

- **Belirti:** `degerlendirme_dogrula.py` k2-11'de 40+ "hoca vurgusu: konu slaytta yok" HATA.
- **Kök neden:** A1 görev şeması `konu`yu "slayttaki karşılığı" diye tanımladı ama yazar ajan okunur özet yazdı; kapı birebir arıyor.
- **Çözüm:** `meds_temp/ogrenci_ders/hv_konu_duzelt.py`: özet `konu_ozet`'e taşınır (öğrenci ekranı bunu gösterir), `konu` sayfadaki en
  yakın birebir satıra bağlanır. Aynı aileden öğrenci notu `hedef` ve tablo hücresi alıntıları `kanit_kirp.py` ile kırpıldı.
- **Önleme:** A1 şemasında iki alan ayrıdır: `konu` = slayttan birebir, `konu_ozet` = okunur özet. Tablo sayfasında alıntı tek hücre içinden.

## H473 — Ders notu sadakati eşiğin altında: "Ek bilgi" etiketleri ve meta cümleler (2026-11-02)

- **Belirti:** k2-10 yayını "ders notu sadakati 0.757 < 0.8" ile reddedildi.
- **Kök neden:** Ders notu yazarı slayt dışı hoca açıklamalarını "Ek bilgi:" etiketleriyle ve "Çıkmış sorularda … cevabıdır;
  çeldiriciler …" gibi süreç cümleleriyle ekledi; sadakat ölçütü (s14.fidelity: not köklerinin slaytta geçme oranı) bunları kaynak
  dışı sayar. Kısa (26 sayfa) slaytta oran hızla düşer.
- **Çözüm:** etiketler ve meta cümleler kaldırıldı, anekdotlar kısaltıldı, slayt sözcükleri kullanıldı → 0.855 (eşik gevşetilmedi).
- **Önleme:** Ders notu yalnız slayt bilgisinin redaksiyonudur; hoca açıklamaları sesli anlatımda ve hoca vurguları listesinde yer
  alır. Ders notunda süreç/meta cümlesi ("çıkmışta şu sorulmuştur", "slaytta yazılı değildir") yazılmaz.

## H476 — Ders analizi özeti "çözücü yok" diyerek düştü (setlere bölünmüş çözücü) (2026-11-03)
- **Belirti:** k2-12 ve k2-14 (Beyin ve Sinir Cerrahisi) için `ders_analizi/uret.py` "özet yok: sesli örnek soru çözücü" verdi; çözücü canlıdaydı.
- **Kök neden:** `birlestir.py` 40'tan çok sorulu dersin çözücüsünü ardışık setlere böler (`2b01-1.json`, `2b01-2.json`); `uret.py` yalnız
  `<kod>.json` dosyasını arıyordu → setli her derste özet sessizce eksik kalıyordu.
- **Çözüm:** `uret.py` `<kod>.json` ya da `<kod>-1.json` varsa çözücüyü var sayar.
- **Önleme:** çözücü varlığını denetleyen yeni kod set biçimini (`<kod>-N`) de tanır; çözücü index.json'u (`dersler[].kod` önekiyle) tek doğru kaynaktır.

## H477 — Asıl hoca derse girmediğinde sınav kaynağı (2026-11-03, Beyin ve Sinir Cerrahisi k2-12/13/14)
- **Durum:** derse başka hoca (Zeynep) kendi slaytlarıyla girdi; sınavı asıl hoca (Sinan Apaydın) kendi slaytlarından hazırlıyor.
- **Kural:** sınavı hazırlayan hocanın slaytı tek kaynaktır (anlatım, soru, önem); derse giren hocanın slaytı/sesi yalnız önem ipucudur,
  metinde "hoca vurguladı" denmez, onun slaytında olup sınav hocasının slaytında olmayan bilgi eklenmez. Kullanıcının bildirdiği geçmiş
  sorudan slaytta karşılığı olmayan (servikal travmada immobilizasyon) anlatıma uydurulmaz, kullanıcıya bildirilir.

## H485
- **Belirti (2026-11-04):** destesiz taslakta `denetle.py` sayfa haritası denetiminde çöktü; değerlendirme kapısı atom/çıkmış kanıtlarının
  yüzlercesini "slaytta yok" diye reddetti (k2-07: 153 HATA).
- **Kök neden:** (1) taslak iskeleti elle kurulurken `taslak/sayfalar.json` olarak sayfa METNİ (sözlük) kopyalandı; ders işçisi burada
  `cikar.sayfa_varliklari` listesini bekler. (2) Yazar ajanlar kanıtı `pdftotext -layout` metninden alıntıladı; iki sütunlu slaytta bu metin
  satırları karıştırır, kapı ise pymupdf metninde birebir arar.
- **Çözüm:** `meds_temp/ogrenci_ders/arac/taslak_kur.py` artık `sayfa_varliklari` üretir; `arac/kanit_onar.py` her başarısız alıntıyı sayfanın
  pymupdf metninde birebir geçen en uzun (≥3 kelime) diziye indirir (bilgi metni değişmez, uydurma yok); taslak + çıkmış eşlemesi onarıldı,
  üç paket 0 HATA.
- **Önleme:** taslak iskeleti yalnız `taslak_kur.py` ile kurulur. Kanıt alıntısı yazan ajan alıntıyı `pymupdf` sayfa metninden alır ya da
  yazım sonunda `kanit_onar.py --yaz` + `degerlendirme_dogrula.py` çalıştırır.

## H486
- **Belirti (2026-11-04):** k2-07 (genel anestezik) anlatımı ve örnek soruları bağımsız denetimde KALIR: remifentanil "plazma kolinesterazıyla"
  yıkılıyor, sugammadex için iki farklı derin blok dozu, süksinilkolin "asetilkolin reseptörünü taklit eder", sugammadex reseptör antagonisti gibi.
  k2-15'te önem yazarı anlatımda zaten ayıklanmış çelişkili slayt satırından ("kısa psikotikte takipte çoğunlukla şizofreni") madde ve soru kurdu.
- **Kök neden:** yazar slayttaki yanlış/çelişkili satırı (s34 remifentanil, s48–s56 doz, s45 kısa psikotik) olduğu gibi aktardı; anlatım
  denetiminde düzeltilen hata listesi sonraki katmanların (soru, önem, çözücü) yazarlarına verilmedi.
- **Çözüm:** anlatım düzeltildi + yeniden denetim GEÇER; örnek sorularda 6 ifade düzeltildi; k2-15 önem/çözücü maddesi yeniden yazıldı.
- **Önleme:** anlatım denetiminin `denetim.json` tıbbi bulguları ve `rapor.md` "slayt çelişkisi" listesi her sonraki katman yazarının istemine
  zorunlu girdi olarak konur; ders başına soru katmanı denetçisi (`GOREV_DENETCI_SORU_K2_B3.md`) bu listeyi tek tek arar.

## H487 — `kisaltma_sozlugu.py sozluk_disa` elle eklenmiş kısaltmaları siliyor (2026-11-04)
- **Belirti:** k2-16 kısaltmalarını dışa aktarınca `src/data/kisaltma_sozluk.json` 347 → 317 kayda düştü; ASIC, CGRP, IHH, NEADL, LSD… gibi 30+ kayıt (elle ya da başka oturumca eklenmiş) kayboldu.
- **Kök neden:** `sozluk_disa` dosyayı yalnız `data/sesli_anlatim/kisaltma/*.json` derslerinden YENİDEN KURUYOR; o katmanda olmayan (elle eklenen, arşiv/y25 dersleri) kayıtları korumuyor.
- **Çözüm:** dosya geri alındı, yalnız kendi derslerin yeni kısaltmaları ve deste bağları birleştirme ile eklendi (4 yeni, 16 bağ).
- **Kural:** `sozluk_disa` sonrası daima kayıt sayısını HEAD ile karşılaştır; düşüş varsa yazma, birleştir. (Betik birleştirme kipine geçirilmeli — açık iş.)

## H488 — Slayt fotoğrafı ters yorumlandı: hipotonik bebek "tonus artışı" diye anlatıldı (k2-16 s.9, 2026-11-05)
- **Belirti:** sesli derste "Slayttaki fotoğraflarda tonus artışının görünümü vardır: bükülü ekstremitelerle yatan bir bebek…" cümlesi; fotoğraf aslında karın üstünden tutulunca sarkan (gevşek) bebek = hipotoni. Hoca kaydı da "tonus azsa hipotonik bebek" diyor.
- **Kök neden:** A1a sayfa envanterinde `gorsel_aciklama` görüntü tahminle yazıldı ("fleksiyon postüründe bebek, spastik tutum örnekleri"); anlatım yazarı ve çapa bu tanımı slayta yeniden BAKMADAN kullandı; anlatım denetçisi görseli hoca dökümüyle karşılaştırmadı. Yanlışı ancak çizim ajanı fotoğrafa kontur çizerken gördü.
- **Çözüm:** cümle, ekran, çapa `sekil`, envanter tanımı düzeltildi; kısmi yeniden yayın (değişen paragraf EMA + cümle/kelime zamanı + çapa/çizim).
- **Kural:** fotoğraf/klinik görünüm anlatan her cümlede yazar ve denetçi sayfa görüntüsüne bakar; görsel yorumu hoca dökümüyle çelişirse hoca + görüntü kazanır, envanter tanımı tek başına dayanak değildir. Denetçi yönergesine "görsel–anlatım yön kontrolü (artış/azalma, sağ/sol, normal/patolojik)" maddesi eklenir.

### H509 — Destesiz derste ders içerik paketinin kısaltmaları "Ek"e düşüyordu (adim 0), kapı %5 sınırında HATA verdi (2026-11-06)
- **Belirti:** k2-20 `ders_icerik_dogrula.py` → "adim eşlenemeyen kayıt %5"; 22 kısaltmanın hepsi `adim: 0` (PDF akışında ders sonuna "Ek" olarak atılır). k2-19'da da kısaltmalar 0'dı, oran düşük kaldığı için fark edilmedi.
- **Kök neden:** `ders_icerik_adim.py::destesiz` kısaltmanın sayfasını `taslak/sayfalar.json`'dan `{"1": metin}` biçiminde arıyordu; yeni hatta bu dosya sayfa nesnelerinden oluşan **liste** (tablolar/görsel/vurgulu) ve düz metin yok → sözlük boş, her kısaltma 0.
- **Kalıcı çözüm:** liste biçiminde ders klasöründeki `meds_temp/ogrenci_ders/<ders>/sayfalar.json` (düz sayfa metni) kullanılır; k2-20'de eşlenemeyen 22 → 0.
- **Önleme:** Biçim değişen ara dosyayı okuyan betik, beklenen biçim gelmezse sessizce boş sözlükle sürmez; destesiz her derste paketten sonra `ders_icerik_adim.py` çıktısındaki "eşlenemeyen" sayısı 0 değilse nedeni bulunur (eşik altı olsa da).

### H510 — Değerlendirme kapısı kaynakça sayfasındaki yazar baş harflerini "sözlükte yok kısaltma" sayıyordu (2026-11-06)
- **Belirti:** k2-37 değerlendirme paketi `s23: kısaltma 'MG'/'DS'/'RP'/'MB' sözlükte yok` HATA'ları verdi; s23 "Kaynaklar" sayfası (Craske MG, Baldwin DS…).
- **Kök neden:** `degerlendirme_dogrula.py` her sayfadaki 2–5 büyük harfli öbeği kısaltma adayı sayıyordu; kaynakça sayfaları ayrılmıyordu. Ders atlamamak için uydurma kısaltma anlamı yazmak tek yol gibi görünüyordu.
- **Kalıcı çözüm:** "Kaynaklar/Kaynakça/Kaynak/References" başlıklı sayfa kısaltma denetiminden çıkarıldı.
- **Önleme:** Kapıyı geçmek için sözlüğe anlamı bilinmeyen kısaltma eklemek YASAK; yanlış pozitifin kökü kapıda düzeltilir.

### H512 — Anlatım parçalara bölünerek yazdırılınca ara resim adımı düştü (k2-21)
- **Belirti:** Kullanıcı: "hipnotik dersinde neden ara resim yok?" — k2-21 sesli derste hiç ara resim yoktu.
- **Kök neden:** k2-21 anlatımı güvenlik filtresine takıldığı için B1 görevi (anlatım + ara resim tek ajan) yerine sayfa aralıklarına bölünmüş üç ajana yalnız anlatım yazdırıldı; koordinatör ara resim adımını parçalara vermedi ve yayın öncesi `ara_resim/dogrula.py` çalıştırılmadı.
- **Kalıcı çözüm:** Ara resimler v2 yayımlandıktan sonra ayrı adımda üretildi (paragraf dizini yayındaki v2'den).
- **Önleme:** B1 bölünürse ara resim ayrı bir alt görev olarak MUTLAKA açılır; yayın öncesi kontrol listesinde `python3 scripts/uretim/ara_resim/dogrula.py <key>` çalıştırılır ve `src/data/ara_resim/<key>.json` yoksa ders tamamlandı sayılmaz.

### H531 — Hoca sesi sonradan gelen yayımlanmış derste anlatım baştan yazılmaz; kısmi revizyon ve tekrar dolgusu tuzağı (2026-11-10)
- **Belirti:** Dört ders "hoca sesi yok" diye yayımlanıp EMA'lanmışken ses geldi. İlk revizyonda yazar ajanlar (k2-58, k2-22) bilgiyi zaten veren cümlenin ardından "Hoca bunu da saydı/tekrar etti" cümlesi ekledi; k2-58'de doğrulanmış çıkmışı olmayan fetal alkol sendromu için "sınavda soruldu" dendi; k2-24'te bozuk dökümdeki "okuyla" sözcüğü "görme yolları" diye tahmin edildi; k2-23/k2-58'de `tur: anlatim` kaydı uydurma kategoriyle `hoca` alanına bağlandı.
- **Kök neden:** "hoca katmanını ekle" görevi vurgu cümlesini amaç sanıyor; `hoca` alanının yalnız sınav vurgusu için olduğu ve dayanaksız/yinelenen vurgu cümlesinin H22 dolgusu sayıldığı istemde yoktu. `v2_birlestir.py` cümle kimliklerini her koşuda sıfırdan numaralıyor; kimlik korunmazsa klip/çapa/çıkmış bağları kayar.
- **Çözüm/önleme:** Akış: A1b (ses_hizasi + hoca_vurgulari + "Anlatıma eklenecekler") → `yayinla.py kimlik` → yalnız var olan paragraflara ekleme (yeni paragraf/silme/sıra değişikliği yok) → birleştirme sonrası eski kimlikleri metinle geri yazma (`meds_temp/ogrenci_ders/k2-58/is/hoca_rev.py kimlik`) → bağımsız denetçi (yalnız değişen cümleler) → `yayin_hazirla_destesiz.sh` → `klip_tasi.py <key> --eski <eski.md>` → `sesli_yayinla.py` (EMA yalnız değişen klipleri üretir: 4–9 klip) → Oracle `meds-cumle-zaman` + `meds-kelime-zaman-hat`. `hoca` alanına yalnız `tur: sinav` bağlanır (`yayinla.py yaz` dogrulaması HATA verir); bilgiyi tekrar eden vurgu cümlesi yazılmaz, yalnız alan bağlanır; hocanın "sınavda çıkar" demesi doğrulanmış çıkmış değildir.

### H536 — Değerlendirme kapısı tasarım PDF'inin harf aralıklı başlıklarını ("Y A N I TL A R", "KAYN AKLAR") kısaltma sanıyordu (2026-11-09, k2-22)
- **Belirti:** `degerlendirme_dogrula.py k2-22` 24 "kısaltma sözlükte yok" HATA'sı verdi: ITLAR, ÜRÜLE, ŞLEME, FREUD, GP…; hiçbiri kısaltma değildi.
- **Kök neden:** Psikiyatri slaytları tasarım şablonunda büyük harfli, harf aralığı açılmış başlık kullanıyor; pymupdf metni harf gruplarını ayrı jeton veriyor; kaynakça sayfası da "KAYN AKLAR" diye başladığı için H510 istisnası tutmuyordu; atıf satırındaki yazar baş harfleri (Yates GP) de aday sayılıyordu.
- **Kalıcı çözüm:** kapı tamamı büyük harf olan satırları (başlık/üst yazı) kısaltma taramasından çıkarır, ilk satırı boşluksuz birleştirip KAYNAK/REFERENCES ile başlayan sayfayı kaynakça sayar, "Soyad GP," atıf baş harflerini eler. Eski derslerde (k2-20/21/38) sonuç değişmedi (0 HATA).
- **Önleme:** Kapıyı geçmek için sözlüğe anlamsız kısaltma yazılmaz (H510); yeni biçim tuzağı kapının kendisinde düzeltilir.

### H537 — A1a/A2 "kanıt" alanları birden çok satırı birleştiren özetler olduğundan değerlendirme kapısından geçmiyordu (2026-11-09/10, dört derste)
- **Belirti:** k2-22 5 çıkmış + 3 atom, k2-23 5 + 10, k2-58 4 + 1, k2-24 1 + 34 kayıt "kanıt sN'de yok" HATA'sı verdi.
- **Kök neden:** yazarlar `kanit`'i birden çok slayt satırını " · " ile birleştirerek ya da tablo hücrelerini yan yana koyarak yazdı; kapı `kanit`'i (" (" ve " → " öncesi) sayfa metninde BİREBİR arar. Yönerge "birebir alıntı" diyor ama "tek satır/tek hücre" demiyordu.
- **Kalıcı çözüm:** her kayıt tek satır/tek hücrelik birebir alıntıya indirildi; açıklama `neden`'e taşındı.
- **Önleme:** A1a/A2 yönergesine kural: `kanit` = TEK birebir satır ya da tablo hücresi; yazar üretim sırasında pymupdf normuyla doğrular (`kaynak_kapisi.py` + `degerlendirme_dogrula.py` paket kurulmadan önce koşulur).

### H543 — İçi boş madde imi pymupdf metninde "o" harfi olarak geldi; değerlendirme kapısı birebir kanıtları reddetti, yazar bilgisiz kanıt satırına kaçtı (2026-11-10, k2-26)
- **Belirti:** k2-26 değerlendirme kapısı 6 atomda "kanıt yok" dedi; A2 yazarı kapıyı geçmek için dört atomun kanıtını aynı sayfadaki BAŞKA bir satırla değiştirdi (ör. "MZ %62 DZ %18" bilgisinin kanıtı "Genetik epilepsi genel popülasyonda %0,3-0,5" oldu) — kanıt bilgiyi göstermez hâle geldi.
- **Kök neden:** slaytlarda Wingdings "o" madde imi; pymupdf bunu satır başında harf olarak verir ("oMZ %62", "oPPP2R2B geni"), pdftotext vermez. `denetle.py` (pdftotext) ile `degerlendirme_dogrula.py` (pymupdf) farklı metin gördüğü için iki satıra yayılan hiçbir kanıt ikisinden birden geçemedi; H495'teki im temizliği bu imi kapsamıyordu.
- **Kalıcı çözüm:** kapı satır başında büyük harf/rakam/% önündeki "o"yu siler; dört atomun kanıtı yeniden bilgiyi gösteren birebir satıra döndü (k2-21/22/24/38 kapıları değişmedi, 0 HATA).
- **Önleme:** Kapıyı geçmek için kanıtı bilgiyle ilgisiz bir satıra kaydırmak YASAK (kanıt bilgiyi göstermeli); iki kapının metni farklıysa kök neden kapıda/çıkarımda düzeltilir ve koordinatöre bildirilir.

### H548 — Slayt altındaki kaynak satırının dergi adı "sözlükte olmayan kısaltma" sayıldı (2026-11-10, k2-28 s.31)
- **Belirti:** `s31: kısaltma 'BMJ' sözlükte yok` HATA'sı; satır "Guan B, et al. BMJ Open. 2023;13:e075049." (şeklin kaynak künyesi).
- **Kök neden:** H510/H536 yalnız kaynakça SAYFALARINI ve "Soyad GP," atıf baş harflerini eliyordu; içerik slaydının altındaki tek satırlık künye taranıyordu.
- **Kalıcı çözüm:** "et al" ve "yıl;cilt" kalıbını birlikte taşıyan satır kısaltma taramasından çıkarıldı.
- **Önleme:** kapıyı geçmek için sözlüğe dergi adı ya da anlamsız kısaltma yazılmaz (H510); yeni biçim tuzağı kapının kendisinde düzeltilir.

### H553 — Değerlendirme kapısı OCR'lı metinden alınan çok satırlı kanıtları PDF'te bulamadı (2026-11-12, k2-31)
- **Belirti:** `degerlendirme_dogrula.py k2-31` 21 HATA: 13 atom "kanıt sNN'de yok" (ör. a44 "A. Mycoplasma pneumoniae B. Lyme hastalığı C. Piyojenik miyelit …"), 3 çıkmış "kanıt s10/s2'de yok", 5 kısaltma (HSV, IGM, TPHA, TPI, FTA) sözlükte yok.
- **Kök neden:** taranmış/karma PDF'te A2 (bilgi havuzu) alıntıları OCR'lı/düzeltilmiş `sayfalar.json`'dan alındı; orada satırlar birleşik, boşluklar düzeltilmiş ("ve huzursuzluktur"). Kapı ise pymupdf metninde birebir arar; pymupdf'te liste maddeleri ayrı satırdır ve bazı sözcükler bitişiktir ("vehuzursuzluktur", "CAvb."), bu yüzden satır sınırını aşan alıntı eşleşmez. Çıkmışların s2/s10 kanıtı yalnız şekildeydi ama eşlemede `kanit_goruntu` (H547) yazılmamıştı.
- **Çözüm:** `taslak/bilgi_havuzu.jsonl`'da a44/a53/a81/a84/a110 alıntıları bilgiyi destekleyen TEK pymupdf satırına indirildi (bilgi metni değişmedi); üç görsel çıkmışa sayfa görüntüsünden okunan `kanit_goruntu` eklendi; beş kısaltma `kisaltma_sozluk.json`'a eklendi (slayt yazımı "IGM"). Kapı 0 HATA.
- **Önleme:** A2'de kanıt alıntısı her zaman `pymupdf.open(pdf)[s-1].get_text()` satırlarından birebir kopyalanır; OCR/`sayfalar.json` yalnız metni okumak/anlamak içindir. Liste/tablo sayfasında birden çok satırı kapsayan alıntı yazılmaz. Metinsiz (<60 karakter) sayfaya dayanan çıkmışa `kanit_goruntu` zorunludur.

### H554 — Ders içerik paketinde "bilgiler boş": bilgi havuzu `tur` alanı içerik tipiyle dolduruldu (2026-11-12, k2-29)
- **Belirti:** `ders_icerik_dogrula.py k2-29-santral-sinir-sistemi-enfeksiyonlari` → "bilgiler boş" HATA; ders sayfasında Bilgi spotları bölümü yok.
- **Kök neden:** `ders_icerik_uret.py` Bilgi spotlarını yalnız `tur == "spot"` kayıtlarından kurar (TALIMAT §8 şeması: `tur` ∈ spot|ilac|tedavi|tani|mekanizma|epidemiyoloji). A2 yazarı k2-29'da `tur`'a içerik tipini (morfoloji, etiyoloji, klinik, patogenez, tanim…) yazdı; tek bir `spot` kalmadı. Faz A yönergesi (`GOREV_A2_K2_B5.md`) havuz şemasını tekrar etmiyor, yalnız dosya adını sayıyordu; şema yalnız `ders_isci/TALIMAT.md` §8'deydi.
- **Çözüm:** havuzda şema dışı `tur` değerleri `icerik_turu` alanına taşındı; `patogenez` → `mekanizma`, diğerleri → `spot` (tani/tedavi/epidemiyoloji olduğu gibi). Bilgi metni ve kanıtlar değişmedi. Üretici 125 bilgi çıkardı; kaynak kapısı 0 HATA, denetle.py 0 HATA.
- **Önleme:** `bilgi_havuzu.jsonl` `tur` yalnız TALIMAT §8 listesinden; içerik tipi `icerik_turu`'na. Yönergeye bir satır eklendi.


### H570 — Ders analizi betiği tam ders anahtarını "kayıt defterinde yok" sandı (2026-11-13, k2-62/k2-65)
- **Belirti:** `python3 scripts/uretim/ders_analizi/uret.py k2-62-kraniyal-sinir-muayenesi` → "k2-62-kraniyal-sinir-muayenesi: ders kayıt defterinde yok" ve çıktı yazılmadı. Aynı derste `--dogrula` → "çıktı yok, 1 HATA". Oysa ders kayıt defterinde (`src/data/dersler/k2.json`) k2-62 vardı ve `meds_database_v2/ders_bilgi/k2-62/degerlendirme/paket.json` hazırdı.
- **Kök neden:** İki kimlik biçimi karıştı. Sesli ders **anahtarı** `k2-62-kraniyal-sinir-muayenesi` (tam), kayıt defterindeki **id** `k2-62` (kısa), değerlendirme klasörü de kısa kimlikle (`meds_database_v2/ders_bilgi/k2-62/`). `uret.py::kayit_bul` gelen anahtarı doğrudan `d["id"] == key` ile karşılaştırıyordu; `uret.py::uret` de paket yolunu tam anahtarla kuruyordu. Bu yüzden tam anahtarla çağrı hiçbir zaman eşleşmiyor, kısa anahtarla çağrı ise `ders_analizi/k2-62.json` gibi farklı dosya adı üretiyordu (eski dersler kısa adla üretilmişti, yeni dersler için çelişki doğdu).
- **Kalıcı çözüm:** `kayit_bul` gelen anahtarı `k2-62` biçimine normalleştirir (`"-".join(key.split("-")[:2])`); paket yolu ve çıktı adı kısa kimlikle kurulur, MEtin/hizalama dosyaları `glob` ile tam anahtar üzerinden bulunur. Doğrulama: `uret.py k2-62` ve `uret.py k2-65` → 6 analiz bölümü + özet, `--dogrula` 0 HATA.
- **Önleme:** Yeni bir betik yazarken **üç kimliği** ayrı tut: (a) sesli ders anahtarı (`k2-62-…`), (b) kayıt defteri id'si (`k2-62`), (c) alt klasör adı (`meds_database_v2/ders_bilgi/k2-62`). Betik hangisini beklediğini kullanım satırında yazsın; karşılaştırma ve dosya yolu **aynı** biçimden kurulsun. "kayıt defterinde yok" hatası görüldüğünde önce anahtarın hangi biçimde olduğu ve dizinin gerçek adı kontrol edilir, kayıt defterine madde eklenmez.

### H571 — Ders içerik paketinde kısaltmaların hepsi `adim: 0` kaldı: `sayfalar.json` yedeği hiç çalışmadı (2026-11-13, k2-65 ders içerik paketi)
- **Belirti:** `python3 scripts/ders_icerik_uret.py k2-65-serebrovaskuler-hastaliklar` 0 HATA dedi, ama `ders_icerik_dogrula.py` "adim eşlenemeyen kayıt %10 (>%5)" verdi. Bakıldığında 311 kaydın 33'ü — kısaltmaların **tamamı** — `adim: 0` taşıyordu (`BDH`, `GİA`, `BT`, `MRG`, `TPA` …); spotlar/tablolar/listeler/kartlar/quiz (n taşıyanlar) sorunsuzdu.
- **Kök neden:** `scripts/ders_icerik_adim.py::destesiz()` kısaltmanın `adim`ini önce `taslak/sayfalar.json` içinde arıyor; bu dersin taslağında dosya **yok** (düz metin `meds_temp/ogrenci_ders/k2-65/sayfalar.json` ve `taslak/` altında yalnız `bilgi_havuzu.jsonl` var). Yedek yol yalnız `if not isinstance(sayfa, dict)` koşulunda çalışıyordu; dosya yokken `sayfa = {}` olduğu için koşul **False** kalıyor, 60 sayfalık gerçek `sayfalar.json` hiç okunmuyor ve her kısaltma 0'a düşüyordu. Yani boş sözlük "geçerli dict" sayıldığı için sessizce boş arama yapıldı; kapı hatayı yakalamasa paket yanlış adımlarla yayına girecekti.
- **Kalıcı çözüm:** Koşul `if not sayfa or not isinstance(sayfa, dict)` yapıldı: taslak dosyası yoksa ya da boşsa ders klasöründeki düz metin `sayfalar.json` okunur. Yeniden üretimde eşlenemeyen kayıt 33 → 0, kapı 0 HATA; kısaltmalar doğru sayfaya bağlandı (`BDH`→2, `GİA`→2, `CRP`→9, `BT`→15, `MRG`→15, `MCA`→17, `TND`→23, `TPA`→23, `İV`→25).
- **Önleme:** Bir yedek/ikinci kaynak yolu yazarken "dosya var mı" ile "içerik boş mu" ayrı sınanır — boş varsayılan (`{}`/`[]`) yedeği **atlatır**, `isinstance` kontrolü bunu yakalamaz. Kapı çıktısında `adim eşlenemeyen %N` görülürse önce kaynak dosyanın gerçekten okunduğu (`J(sp)` sonrası `len(sayfa)`), sonra hangi kayıt türünün 0 kaldığı (bu turda yalnız `kisaltmalar`) kontrol edilir; kapı 0 HATA verse bile paket körü körüne kabul edilmez.

