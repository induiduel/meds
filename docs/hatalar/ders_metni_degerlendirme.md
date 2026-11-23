# Hata defteri — ders_metni_degerlendirme (değerlendirme kapısı, sayfa haritası, ders içerik paketi, ders analizi)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16; `hatalar/ders_metni.md` 3 konuya bölündü). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## H38 — Sesli ders v2 slayt adımı hiç gösterilmiyordu (2026-10-24)
- `konusma_v2.py` şemasında `slayt_adim` adım KİMLİĞİ (`k2-02-d-s05`); sunucu yalnız sayıyı kabul ediyordu → bütün K2
  cümlelerinde adım bağı boş. `canliDers.ts` ve `.medspak` kimlikten numarayı çözer. Paket kapısı bunu yakaladı.

## H64 — Sayfa haritası adım numaraları tekrar sayfalarını saymıyordu; kısa/eksik kanıt (2026-10-26, k2-22 psikosomatik)
- **Belirti:** `denetle.py` 76 HATA: adım 8–31 için "pdfSayfalari [n] ama harita [n+1] diyor", başlık aralıkları içerik adımı değil, bilgi/harita alıntıları 3 kelime ya da yok.
- **Kök neden:** `sayfa_haritasi.json` `adimlar` alanı desteden ayrı, CHECKPOINT slaytları sayılmadan numaralandırılmıştı; her checkpoint'ten sonra kayma büyüdü. Yalnız görsel olan sayfalarda (s.6, s.30: kaynak.md metni yok) `alinti` yazılamadığı için kanıt boş bırakılmıştı; tablo/liste sayfalarında tek satırlık (3 kelime) alıntı seçilmişti.
- **Çözüm / kural:** Harita `adimlar`ı daima son destenin içerik slaytlarının `pdfSayfalari`ndan türetilir (checkpoint/oyun hariç); başlık `adimlar` = kapsadığı sayfaların ilk/son içerik adımı. Metinsiz görsel sayfada `kanit: {sayfa, gorsel: "≥4 kelime görülen"}` kullanılır; alıntı kaynak.md'de birebir geçen ≥4 kelime olur.

## H68 — H66 tekrarı + süs bölüm sayfaları `sekil` türünde (2026-10-26, k2-27 periyodik muayeneler)
- **Belirti:** `arsiv_yayinla.py`'de 15 `sesli_kapsam: çıkmış …: bilgisi anlatılmamış` + 8 "s. n (sekil) anlatılmamış" (bölüm başlık/kapanış süs sayfaları).
- **Kök neden:** (1) H66'nın aynısı: 248 cümlenin hiçbirinde `cikmis` dolu değil, ilgili 15 soru bağlanmamış. (2) `sayfa_haritasi.json`'da yalnız süs görselli bölüm başlık sayfaları (s.18, 26, 39, 51, 52, 107, 130, 135) `tur: sekil` yazılmış; kapı bunları anlatılacak şekil sayar.
- **Çözüm / kural:** Çıkmışlar `kanit.sayfa` cümlelerine bağlandı (c0003, c0037, c0047, c0101, c0112, c0204, c0213, c0218, c0222) ve sesli uyarı eklendi; süs bölüm sayfaları `tur: kapak` yapıldı. Haritacı, bilgi taşımayan bölüm başlık/kapanış sayfalarını `kapak` yazar; sesli yazar H66 adımını atlamaz. Kapı gevşetilmedi.

- **2026-10-26 (k2-29):** `cikmis_baglantilari.json`'da `ilgili: true` olan çıkmışın bilgisi cümlede anlatılsa da cümlenin `cikmis` listesine kimliği yazılmadı ve sesli uyarı yoktu → `sesli_kapsam` yayını durdurdu. Önleme: sesli metin yazarı her ilgili çıkmışı `kanit.sayfa` sayfasındaki cümleye bağlar ve o cümlede "bu bilgi çıkmışta soruldu" der (kapı: `isle.cikmis_ses_kapsam`).

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

## H472 — Hoca vurgusu `konu` alanı özetti, değerlendirme kapısı slayttan birebir istiyor (2026-11-02)

- **Belirti:** `degerlendirme_dogrula.py` k2-11'de 40+ "hoca vurgusu: konu slaytta yok" HATA.
- **Kök neden:** A1 görev şeması `konu`yu "slayttaki karşılığı" diye tanımladı ama yazar ajan okunur özet yazdı; kapı birebir arıyor.
- **Çözüm:** `meds_temp/ogrenci_ders/hv_konu_duzelt.py`: özet `konu_ozet`'e taşınır (öğrenci ekranı bunu gösterir), `konu` sayfadaki en
  yakın birebir satıra bağlanır. Aynı aileden öğrenci notu `hedef` ve tablo hücresi alıntıları `kanit_kirp.py` ile kırpıldı.
- **Önleme:** A1 şemasında iki alan ayrıdır: `konu` = slayttan birebir, `konu_ozet` = okunur özet. Tablo sayfasında alıntı tek hücre içinden.

## H476 — Ders analizi özeti "çözücü yok" diyerek düştü (setlere bölünmüş çözücü) (2026-11-03)
- **Belirti:** k2-12 ve k2-14 (Beyin ve Sinir Cerrahisi) için `ders_analizi/uret.py` "özet yok: sesli örnek soru çözücü" verdi; çözücü canlıdaydı.
- **Kök neden:** `birlestir.py` 40'tan çok sorulu dersin çözücüsünü ardışık setlere böler (`2b01-1.json`, `2b01-2.json`); `uret.py` yalnız
  `<kod>.json` dosyasını arıyordu → setli her derste özet sessizce eksik kalıyordu.
- **Çözüm:** `uret.py` `<kod>.json` ya da `<kod>-1.json` varsa çözücüyü var sayar.
- **Önleme:** çözücü varlığını denetleyen yeni kod set biçimini (`<kod>-N`) de tanır; çözücü index.json'u (`dersler[].kod` önekiyle) tek doğru kaynaktır.

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


### H620 — Öğrenci sentez PDF'i (jsPDF) MarkItDown'da boş/eksik çıktı; OCR boş satırı hoca vurgusunu yarıda kesti (2026-11-17)
- **Belirti:** Arkadaş Drive'ındaki 25 Kurul 2 sentez PDF'i MarkItDown ile çevrildiğinde Markdown boş geldi; OCR sonrası da sözcüklerin %5–8'i kayıp, "HOCA VURGUSU… FAS" birimi cümle ortasında bitiyordu.
- **Kök neden:** (1) PDF'ler jsPDF/html2canvas ile sayfa RESMİ olarak basılmış, metin katmanı yok. (2) MarkItDown (pdfminer) OCR katmanında satır sonlarını boşluksuz birleştiriyor ("olmayanbireylerde"), sayfayı tek satıra döküyor — sözcük ve blok sınırı kayboluyor. (3) OCR'ın boş satırı/sayfa sonu cümle ortasına düşüyor; büyük harfle süren devam satırı başlık sanılıyordu. (4) `tus` deseni "rektus/status" içinde eşleşiyordu.
- **Kalıcı çözüm:** `scripts/uretim/ogrenci_sentez/sentez.py`: metin katmanı yoksa `ocrmypdf -l tur+eng` (CPU); MarkItDown birincil, sözcük kapsaması <%98 ise okuma sıralı `pdftotext`→Markdown (`motor` defterde). Blok bölücü cümle bitmeden kapatmaz (boş satır/sayfa sonu), devam satırı başlık sayılmaz; sözlük `\b` sınırlı. Vurgulu başlığın tüm bölümü birime girer.
- **Önleme/Kapı:** `sentez.py calistir` kapısı: kapsama ≥%98 (pdftotext'e karşı), md'deki tetik sayısı == birimlerdeki tetik sayısı, blok bölücü metin düşürürse HATA, eşlemesiz PDF HATA. Önbellek yalnız kapıdan geçmiş çeviriyi atlar. Sentez notunun "çıkmış/hoca söyledi" iddiası doğrulanmış kanıt DEĞİLDİR (çıkmış damgası/"hoca vurguladı" yalnız slayt+ses/çıkmış eşlemesiyle).

### H648 — Değerlendirme paketinin kazanım başlığı ilk maddeyle örtüşmüyor; hata ancak çıkmış analizi kapısında yakalanıyor (2026-11-23, k2-47…k2-56)

- **Belirti:** 8 yeni dersin hepsinde `ders_analizi/uret.py --dogrula` 4–38 "kazanim N: metin başlıkla örtüşmüyor" HATA'sı verdi; E2b yazarları her seferinde "E1'e ait" diye bıraktı.
- **Kök neden:** Kazanım metni bilgi paketinin İLK maddesinden türetiliyor ve başlıkla ≥2 ortak kök isteniyor; `degerlendirme_dogrula.py` bu kuralı denetlemiyor. E1 yazarı başlığı konu etiketi gibi ("Huntington hastalığı", "Dersin hedefleri"), ilk maddeyi ayrıntı cümlesi olarak yazıyor. Bir derste (k2-52 bp21) ilk madde slaytın şüpheli "%50" iddiasıydı → kazanım metni olarak öne çıkacaktı.
- **Çözüm:** Başlıkla en çok örtüşen madde başa alındı; yoksa başlık ilk maddenin içeriğini tarif edecek biçimde yeniden yazıldı (içerik değişmedi). Şüpheli madde başa alınmadı.
- **Kural:** E1 yazımında her bilgi paketinin ilk maddesi başlığın özetidir (≥2 ortak kök) ve slayt_supheli satırı olamaz. Kalıcı çözüm açık iş: `degerlendirme_dogrula.py`'ye aynı örtüşme denetimini eklemek (hata E1'de yakalansın).
