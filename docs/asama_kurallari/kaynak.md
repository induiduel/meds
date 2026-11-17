# Aşama kuralları — kaynak

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/hat/tam_hat/kural_secici.py`. 53 madde. Tek satırlı maddeleri betik denetler (tam metin: `kural_secici.py --tam <H no|aşama>`).

### H8 — Aynı PDF iki ders / yanlış PDF eşleşmesi
- **Kural:** PDF içerikle tanınır; mevcut dersle yüksek sayfa örtüşmesinde yeni ders açılmaz ("tekrar/kısım").
- **Kapı — EKLENDİ:** `isle.tekrar_denetle`: yeni dersin sayfalarının >%50'si aynı kuruldaki yayımlanmış tek bir derste
  neredeyse aynıysa (kelime kümesi Jaccard ≥0,8) uyarı → otomatik onay kapanır, yönetici karar verir. 19 yayımlanmış derste
  0 yanlış uyarı; aynı PDF'in yeniden gelişi %100 yakalandı.


### H10 — Başka dersin sayısı / genel bilgi; çıkmış anahtarı PDF ile çelişiyor
- **Kural:** her ürün yalnız kendi PDF'inin sayısını kullanır; anahtarı PDF ile çelişen çıkmış soru otomatik düzeltilmez, karantinaya alınır ve bildirilir.
- **Kapı — EKLENDİ:** önem yazarı çelişkiyi `elenen_cikmis` → `anahtar_celiskili` ile işaretler (soru o derste kullanılmaz);
  `ders_zinciri.karantina_onerileri` öneriyi `meds_database_v2/ders_isci/cikmis_karantina_onerileri.jsonl`'a yazar ve yöneticiye
  bildirim gönderir. Sitede otomatik gizleme/düzeltme YOK (geçmiş yıl verisi; karar yöneticinin).


- H16 — Sesli ders listesinde iki ders aynı branş numarasını aldı (Meme Kanseri / Memenin Benign "33", 2026-10-20) — betik denetler: `canliDers.ts`
### H19 — Çıkmış cevap anahtarı tıbben hatalı / iki kaynakta çelişik (2026-10-21, TBG kampı)
- **Kural:** cevap anahtarı körü körüne kopyalanmaz; slayta, yoksa tıbbi bilgiye karşı denetlenir. Anahtar değişirse eski anahtar ve
  gerekçe soruda ("Dikkat: sınavın cevap dosyasında X işaretli, tıbben hatalı"), kayıtta `anahtarDuzeltme {eski, yeni, tarih, gerekce}`
  ve sesli anlatımda söylenir. Tekrar çiftleri şık METNİYLE karşılaştırılıp tek karara bağlanır.

### [2026-10-21] Çıkmış soruda iç uyarı metni ve kalıp şık açıklaması (h06/19 Refik Saydam)
- **Hata:** Çözücüdeki çıkmış sorunun kökünde "[Dikkat — olası hatalı kayıt …]" iç notu kalmıştı; öğrenciye gösterildi ve EMA ile
  okundu. Aynı sorunun şık açıklamaları "bu soruda aranan özellik değildir ve elenir" kalıbıydı, ipucu konu dışıydı.

### H30 — Çıkmış konu eşlemesi birebir olunca ders sessizce çıkmışsız kalıyordu (2026-10-23 K2 provası)


### H38 — Sesli ders v2 slayt adımı hiç gösterilmiyordu (2026-10-24)


### H54 — Benzer soru araması boş döndü, ders çıkmışsız üretildi (2026-10-24, k2-07 ikinci sınama)


### H57 — Kurul 2 derslerinde çıkmışlar neredeyse hiç duyulmuyordu (2026-10-24, kullanıcı)


### H64 — Sayfa haritası adım numaraları tekrar sayfalarını saymıyordu; kısa/eksik kanıt (2026-10-26, k2-22 psikosomatik)
- **Çözüm / kural:** Harita `adimlar`ı daima son destenin içerik slaytlarının `pdfSayfalari`ndan türetilir (checkpoint/oyun hariç); başlık `adimlar` = kapsadığı sayfaların ilk/son içerik adımı. Metinsiz görsel sayfada `kanit: {sayfa, gorsel: "≥4 kelime görülen"}` kullanılır; alıntı kaynak.md'de birebir geçen ≥4 kelime olur.


- H66 — İlgili çıkmış sorular sesli derste hiçbir cümleye bağlanmamış (2026-10-26, k2-24 epilepsi) — betik denetler: `isle.py`
### H68 — H66 tekrarı + süs bölüm sayfaları `sekil` türünde (2026-10-26, k2-27 periyodik muayeneler)
- **Çözüm / kural:** Çıkmışlar `kanit.sayfa` cümlelerine bağlandı (c0003, c0037, c0047, c0101, c0112, c0204, c0213, c0218, c0222) ve sesli uyarı eklendi; süs bölüm sayfaları `tur: kapak` yapıldı. Haritacı, bilgi taşımayan bölüm başlık/kapanış sayfalarını `kapak` yazar; sesli yazar H66 adımını atlamaz. Kapı gevşetilmedi.


### H69 — `cikmis_baglantilari.json` liste yerine nesne sarmalayıcısıyla yazıldı (2026-10-26, k2-46 sempatomimetikler)
- **Çözüm / kural:** `cikmis_baglantilari.json` daima kökte bir liste (`[{"soru_id": ..., "soru": ..., "ilgili": bool, "aciklama": ...}]`) olarak yazılır. `denetle.py` ve `arsiv_yayinla.py` doğrudan liste formatı bekler. Dosya düzeltildi, 0 HATA ile Oracle'a dağıtıldı.


### H79 — Otomatik çıkmış→cümle eşlemesi (vektör) derse ait olmayan soruları "çıkmış" diye bağladı (2026-10-27, y25-k2-01)
- **Önleme kuralı:** "Çıkmışta soruldu" vurgusu ve chip yalnız doğrulanmış, slayt kanıtlı eşlemeye dayanır; vektör benzerliği
  yalnız aday listesidir. Metindeki "Bu bilgi çıkmış sınavda sorulmuştur" cümleleri de aynı kanıtla teyit edilir.


### H83 — "Çıkmış" diye gösterilen iki soru doğrulanamadı; biri sitede yüklenmedi (2026-10-27, kullanıcı bildirdi)
- **Önleme kuralı:** Çıkmış eşlemesi yalnız **ham sınav belgesinde bulunan** soruyla yapılır; banka etiketi ("verified",
  "altin_standart") kanıt değildir. `kaynak` alanı olmayan kayıt `degerlendirme_dogrula.py`'de HATA. Gizli kopya
  (sunulmayan id) eşlenmez; hatırlama listesinden gelen sorunun şıkları "sonradan tamamlandı" diye belirtilir.


### H84 — Kaynağı olmayan 86 Kurul 2 "çıkmış"ı Check-Solve onayıyla görünür kalıyordu (2026-10-27)
- **Önleme kuralı:** Banka/çıkmış eklemeleri ham sınav belgesindeki yerle (belge + sayfa) gelir; kaynak gösterilemeyen soru
  "çıkmış" olarak yayınlanmaz. Bir onay katmanı (Check-Solve, Faz 14) kaynağın yokluğunu gidermez. Geri alma: soruyu
  `karantina.json`'dan çıkarmak.


### H94 — Çıkmış listesinde birleştirilmiş gizli kopya: çip 404 verdi (2026-10-27, k2-03)
- **Kural:** `cikmis_konum` yalnız sunulan soru kimliklerini içerir; canlı doğrulamada her kimlik `/tek` 200 vermeden ders tamam sayılmaz.


### H96 — Önem/çözücü zinciri ham belgede olmayan soruyu "çıkmış" diye kullandı (2026-10-27, k2-03)
- **Önleme kuralı:** zincirden sonra önem/çözücü/asistandaki her çıkmış kimliği ham belge taramasında `bulundu` ve `/tek` 200
  olmalı; değilse yayına girmez. `-rNN` türetilmiş kayıt hiçbir zaman çıkmış sayılmaz.


### H103 · Çıkmış adayı farklı dönem/ders sınavından geliyor; ham anahtar bankadaki cevapla çelişiyor; bankada olmayan çıkmışlar (2026-10-27, k2-05 Nörolojik Muayene)
- **Kural:** Çıkmış eşlemesi yalnız (a) ham belgenin DÖNEMİ ve DERSİ bu ders olan, (b) basılı anahtarı banka cevabıyla uyuşan, (c) slayt kanıtı birebir olan sorularla yapılır. Ham belgede olup bankada olmayan soru eşlenmez, `cikmis_taslak.json › bankada_yok_ham_belgede_var` listesine yazılıp bankaya ekleme kararı ana oturuma bırakılır. `-rNN` kayıt ham belgede doğrulansa bile karar ana oturumundur.


### H104 · Hoca ses kaydı: tek model dökümü sınav vurgularını bozuyordu; kayıt dersin ortasından başlıyordu (2026-10-27, k2-08)
- **Kural:** Sınav vurgusu tek dökümden çıkarılmaz; alıntı birebir döküm, anlaşılmayan sözcük "düzeltilerek" yazılmaz (düzeltme `not`ta); gen adı/sayı yalnız slayt ve/veya öğrenci notu ile örtüşünce vurgu olur; kaydın hangi slayttan başladığı rapora yazılır.


### H105 · Harita `adimlar` = deste `slideNumber` (checkpoint dahil); iskelet ajanı içerik adımlarını 1..N saydı (2026-10-27, k2-08)
- **Kural:** Harita deste birleşmeden planlı sayıyla yazılır; birleştirmeden sonra slideNumber'a çevrilir ve `denetle.py` yeniden çalıştırılır (TALIMAT §1b'ye not eklendi).


### H106 · `baglam.kazanimlar` kapak metninden türetilmiş çöp şablon cümleler içeriyor (2026-10-27, k2-08)
- **Kural:** Genel şablon ("temel kavramlarını … analiz eder") ya da kapak metni içeren kazanım kullanılmaz. Açık iş: `isle.kazanimlar` kayıt yoksa boş dönmeli (kod düzeltmesi bu turda yapılmadı).


### H107 · Çıkmış eşlemesi: banka yıl etiketi ham belgeyle çelişiyor, yeniden yazılmış kökler, basılı anahtar yok (2026-10-27, k2-08)
- **Kural:** `kaynak` ham belge adı + sayfa/soru no; çelişen yıl `yil_notu`na; basılı anahtar yoksa `anahtar_notu` ("tıbbi tutarlılık kontrol edildi"); kökü yeniden yazılmış sürüm ya da slayta ters doğru şık eşlenmez.


- H105 · Sıralı tabloda adım atlanıyordu (k2-05, 2026-10-27) — betik denetler: `scripts/uretim/ders_icerik/sira_kapisi.py`
### H118 · Anlamsız karşılaştırma tabloları (Öge / Sınıf / Gerekçe) (2026-10-27)
- **Kural:** Karşılaştırma yalnız iki GERÇEK tıbbi kavramı (hastalık, yapı, ilaç, mekanizma) ayırt eder; "X mi Y başlığı mı" gibi meta sınıflama, tek cümlelik özdeş gerekçe, bozuk Türkçe yasak. Yazar parçalarında da yazılmaz; yazar/denetçi bunu kontrol eder.
- PDF/yazdırma: belge yalıtılmış iframe'de yazdırılır; uygulama DOM'unda yazdırma ve sayfa yüksekliğine eşit sabit yükseklik YASAK (boş sayfa/renk karışması).


### H109 · Ders içerik kayıtlarında "Slayt s.N" kaynağı eksik (2026-10-28)
- **Kural:** Ekranda gösterilen her kaynak alanı doğrulayıcıda zorunlu olur; sayfa uydurulmaz, bulunamayan kayıt silinir (el kitabı §19 11a).


### H131 — Kurul 2 çıkmışlarında başka kurul soruları ve yanlış konu etiketleri (2026-10-28, kullanıcı bildirdi)
- **Önleme kuralı:** Yeni çıkmış eşlemesinde konu etiketi içerik ile doğrulanır; geri alma: karantina kaydını silmek / eskiKonu'yu geri yazmak. Açık: 86 "elle bakılmalı" soru.


### H132 — Karantina listesi eskimişti; OCR ikizleri ve parça kayıtlar karantinada duruyordu (2026-10-28)
- **Önleme:** Karantinaya almadan önce aynı soru/şık kümesine sahip sağlam kayıt aranır (stem+şık Jaccard); varsa karantina değil tekrar arşivi. Üretilmiş soru "çıkmış" etiketi taşımaz.


### H133 — Kaynağı doğrulanamayan sorular gizlenerek kaybedilmişti; "Çıkmış–Örnek" sınıfı (2026-10-28)
- **Önleme:** Kaynağı doğrulanamayan ama doğru soru gizlenmez, `kaynakSinifi=cikmis_ornek` ile etiketlenip öğrenciye belirtilir; çıkmış vurgusu yalnız doğrulanmış kaynağa dayanır.


### H393 — Canlı çıkmışlarda kazanım birleştirmesinden kalan eski konu adları / kimlikler (2026-10-28, kullanıcı onayıyla)
- **Kural:** Canlı çıkmış verisinde toplu değişiklik yalnız sunucu içinden, önizlemeli ve geri alınabilir yolla yapılır; geçmiş kayıt alanlarına toplu değiştirmede dokunulmaz.


### H450 — Çıkmış kayıtlarında uydurma ya da sınavdan sapmış şık/kök (D3K2 çıkmış PDF'leri, 2026-10-30)
- **Önleme:** Özgün belge varken şık metni ondan sapamaz; sapma yalnız tıbbi zorunlulukla ve `degisiklikler` + açıklamada `Not:` ile. Şık değiştiren her ajan çıktısı özgün şıkla benzerlik kapısından geçer.


### H451 — Aynı sınavın derleme kopyaları ayrı görünen sorular olarak kalmış, bazılarının cevabı yanlış (2026-10-30)
- **Önleme:** Yeni çıkmış belgesi işlenirken önce o sınavın TÜM derleme kopyaları belge adına göre toplanır; "aday listesinde yok" diye ATLA/YENI verilmez, ana oturuma bildirilir.


### H452 — Sınav yılı/kurul etiketi belge kanıtı olmadan tahmin edilmişti (2026-10-30)
- **Önleme:** Yıl yalnız belge kanıtıyla (resmî anahtar, sınav sitesi karnesi, belge başlığı) kesinleşir; aynı yıl + aynı kurul dışındaki kopyalar birleştirilmez, `similarPastQuestions` ile bağlanır (kullanıcı kararı 2026-10-30: her yıla ayrı kayıt).


### H453 — Çıkmış PDF ayıklama tuzakları (2026-10-30)
- **Önleme:** Ayıklamadan sonra kaynak içi tekrar taraması (aynı sınav yeni kayıt çifti) ve kişisel veri taraması zorunlu; her paralel ajana ayrı geçici klasör verilir.


### H454 — Aynı soru iki yılın hatırlamasında farklı ifadeyle geçince bağlanmadı; aynı sınavın iki hatırlaması iki ayrı soru sanıldı (2026-10-31)
- **Önleme:** Hatırlama belgeleri işlenirken farklı yılların YENİ kayıtları arasında da konu + cevap metni eşleşmesiyle tarama yapılır;
  aynı sınavda "aynı soru olabilir" notlu ögeler önce birleştirilir, ayrı soru kurulmaz (uydurma soru yasağı kurguda da geçerli).


### H455 — Çıkmış kayıtlarında sınav yılı çok yıllı aralık ("2021-2026") ya da yılsız etiket ("Geçmiş Yıllar Çıkmışı (Arşiv)", "Kategorisiz", "2026") kalmıştı (2026-10-31)
- **Önleme:** Yeni çıkmış kaydında `examYear` yalnız "YYYY-YYYY" (tek akademik yıl) ya da en çok iki yıl ("2021-2023") olabilir; kanıt yoksa
  `Yılı belirsiz` + `yil_belirsiz` etiketi yazılır, asla işlem yılı/geniş aralık/kategori adı yazılmaz. Derleme/toplu içe aktarımda soru notundaki
  yıl alana taşınır; belge yılı belge içi tarih/karne numarası/dosya adıyla doğrulanır ve `sinavKimligi.gerekce`'ye yazılır.
  Kapı: `python3 meds_temp/cikmis_yil_duzelt/yil_duzelt.py` kuru koşusunda "Geçersiz biçimde kalan: 0" olmalı.


### H468 — Hoca dökümü sessizce CPU'ya düştü; turbo dökümü konuşmanın üçte birini kaçırdı (2026-11-02, Kurul 2 2. parti)
- **Önleme:** E0 öncesi `nvidia-smi --query-gpu=clocks.max.sm` ≤2500; günlükte "bu oturum CPU" görülürse durdurulur. Vurgu iki dökümle çapraz okunur; tek dökümde kalan, slayta bağlanmayan söz dayanak olmaz.


### H472 — Hoca vurgusu `konu` alanı özetti, değerlendirme kapısı slayttan birebir istiyor (2026-11-02)
- **Önleme:** A1 şemasında iki alan ayrıdır: `konu` = slayttan birebir, `konu_ozet` = okunur özet. Tablo sayfasında alıntı tek hücre içinden.


### H476 — Ders analizi özeti "çözücü yok" diyerek düştü (setlere bölünmüş çözücü) (2026-11-03)
- **Önleme:** çözücü varlığını denetleyen yeni kod set biçimini (`<kod>-N`) de tanır; çözücü index.json'u (`dersler[].kod` önekiyle) tek doğru kaynaktır.


### H485
- **Önleme:** taslak iskeleti yalnız `taslak_kur.py` ile kurulur. Kanıt alıntısı yazan ajan alıntıyı `pymupdf` sayfa metninden alır ya da
  yazım sonunda `kanit_onar.py --yaz` + `degerlendirme_dogrula.py` çalıştırır.


### H490 — Öğrenci önem kapısı geçilemez yanlış HATA veriyordu (k2-15, k2-16, k2-11; 2026-11-05)
- **Kural:** kapı HATA'sı "eşleyici kaçırıyor" diye bırakılmaz: ya anlatım düzeltilir ya kapının kendisinin denetlediği kanıtlı eşleme yazılır.


### H492 — Hoca vurgu alıntısı bozuk CPU dökümünden kuruldu (2026-11-05)
- **Çözüm/önleme:** döküm `hoca_dokum_gpu.sh` (realpath) ile yeniden yapıldı, 54 alıntı ±60 sn pencerede dökümle karşılaştırıldı, 4'ü düzeltildi. Kural: `alinti` yalnız dökümde geçen sözdür; slayt bilgisi `konu`'ya yazılır, alıntıya karıştırılmaz.


### H493 — Saat kilidi kalktı, hoca dökümü sessizce CPU'da yapıldı (2026-11-05)
- **Çözüm/önleme:** `hoca_dokum_gpu.sh` başlamadan kilit servisini yeniden uygular. Döküm başlığında `cihaz: cpu` ise A1b'ye geçilmez; döküm GPU'da yeniden alınır (vurgu/alıntı CPU dökümünden kurulmaz).


### H508 — Drive'daki ses dosyasının adı başka dersi gösteriyordu: "TSSB Psikaytr 2" aslında EKT (Tedaviler) dersinin başıydı (2026-11-06)
- **Önleme:** Ses dosyası adla değil içerikle eşleşir (KURUL2_DERS_STANDARDI §1): slayta düşmeyen ≥3 dk blok "ders dışı" işaretlenip kurulun öbür dersleriyle karşılaştırılır.


### H530 — Kısık amfi kaydında hoca dökümü uydurma cümlelerle doluyordu (2026-11-10, k2-22/23/24/58)
- **Çözüm/önleme:** `hoca_dokum.py` ilk 10 dk −28 dB'den kısıksa süzgeç + normalleştirme uygular (normal kayıtta ham ses); kısıkta `--model Systran/faster-whisper-large-v3`. Kaydın dersi dosya adından değil içerikten belirlenir.


- H537 — A1a/A2 "kanıt" alanları birden çok satırı birleştiren özetler olduğundan değerlendirme kapısından geçmiyordu (2026-11-09/10, dört derste) — betik denetler: `kaynak_kapisi.py`
### H543 — İçi boş madde imi pymupdf metninde "o" harfi olarak geldi; değerlendirme kapısı birebir kanıtları reddetti, yazar bilgisiz kanıt satırına kaçtı (2026-11-10, k2-26)
- **Önleme:** Kapıyı geçmek için kanıtı bilgiyle ilgisiz bir satıra kaydırmak YASAK (kanıt bilgiyi göstermeli); iki kapının metni farklıysa kök neden kapıda/çıkarımda düzeltilir ve koordinatöre bildirilir.


### H547 — Gövdesi yalnız resim olan slayda dayanan doğrudan çıkmış, değerlendirme kapısından geçemiyordu (2026-11-10, k2-28 s.21)
- **Önleme:** görüntü sayfasına dayanan çıkmış eşlemesi `kanit` + `kanit_goruntu` ile yazılır ve denetçi sayfa görüntüsüne bakar; kanıt metni olan başka satıra kaydırılmaz, eşik gevşetilmez.



### H553 — Değerlendirme kapısı OCR'lı metinden alınan çok satırlı kanıtları PDF'te bulamadı (2026-11-12, k2-31)
- **Önleme:** A2'de kanıt alıntısı her zaman `pymupdf.open(pdf)[s-1].get_text()` satırlarından birebir kopyalanır; OCR/`sayfalar.json` yalnız metni okumak/anlamak içindir. Liste/tablo sayfasında birden çok satırı kapsayan alıntı yazılmaz. Metinsiz (<60 karakter) sayfaya dayanan çıkmışa `kanit_goruntu` zorunludur.


### H554 — Ders içerik paketinde "bilgiler boş": bilgi havuzu `tur` alanı içerik tipiyle dolduruldu (2026-11-12, k2-29)
- **Önleme:** `bilgi_havuzu.jsonl` `tur` yalnız TALIMAT §8 listesinden; içerik tipi `icerik_turu`'na. Yönergeye bir satır eklendi.



### H570 — Ders analizi betiği tam ders anahtarını "kayıt defterinde yok" sandı (2026-11-13, k2-62/k2-65)
- **Önleme:** Yeni bir betik yazarken **üç kimliği** ayrı tut: (a) sesli ders anahtarı (`k2-62-…`), (b) kayıt defteri id'si (`k2-62`), (c) alt klasör adı (`meds_database_v2/ders_bilgi/k2-62`). Betik hangisini beklediğini kullanım satırında yazsın; karşılaştırma ve dosya yolu **aynı** biçimden kurulsun. "kayıt defterinde yok" hatası görüldüğünde önce anahtarın hangi biçimde olduğu ve dizinin gerçek adı kontrol edilir, kayıt defterine madde eklenmez.


### H582 — "Ansiklopedi düzeltmesi Oracle'da dağıtımı durdurabilir / ekrana gelmez" (2026-11-16)
- **Önleme kuralı:** Kimlik üreten her slug çakışmayı sonekle çözer ve kimlik tekilliği doğrulanır. Panelden/hattan yazılan her src/data dosyası CONTENT_FILES'ta tür olarak kayıtlıdır ve ekran onu ortak yükleyiciden okur.


### H589 — Arama kalite ölçümü belgelenenin çok altında çıktı (hit@5 %95 → %75): ölçüm bozuktu (2026-11-16)
- **Önleme kuralı:** dizin süzgeci değişince değerlendirme örneklemi de aynı süzgeçle güncellenir; ölçüm tabanı tarih + havuz tanımıyla birlikte yazılır, eski tabanla kıyaslanmaz.

