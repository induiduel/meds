# Hata defteri — ders_metni_terim_kisaltma (terim ve kısaltma katmanı, PDF metin ayrıştırma, cümle sayacı)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16; `hatalar/ders_metni.md` 3 konuya bölündü). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## H36 — Cümle sayacı sıra sayısı noktasını cümle sonu sayıyordu (2026-10-24, oturum kuyruğu sınaması)
- "8-10. haftalarda" iki cümle sayılıp "4 cümle (en çok 3)" yanlış alarmı veriyordu; yazar ifadeyi bozarak geçiyordu.
- `CUMLE_SINIRI` (cozucu_dogrula2.py, cozucu_dogrula.py, spot_cozucu/asistan_dogrula.py): rakamdan sonraki nokta ancak
  ardından büyük harfle başlayan cümle gelirse sınırdır. Sayım yalnız azalabilir; veri değişmedi.

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

## H487 — `kisaltma_sozlugu.py sozluk_disa` elle eklenmiş kısaltmaları siliyor (2026-11-04)
- **Belirti:** k2-16 kısaltmalarını dışa aktarınca `src/data/kisaltma_sozluk.json` 347 → 317 kayda düştü; ASIC, CGRP, IHH, NEADL, LSD… gibi 30+ kayıt (elle ya da başka oturumca eklenmiş) kayboldu.
- **Kök neden:** `sozluk_disa` dosyayı yalnız `data/sesli_anlatim/kisaltma/*.json` derslerinden YENİDEN KURUYOR; o katmanda olmayan (elle eklenen, arşiv/y25 dersleri) kayıtları korumuyor.
- **Çözüm:** dosya geri alındı, yalnız kendi derslerin yeni kısaltmaları ve deste bağları birleştirme ile eklendi (4 yeni, 16 bağ).
- **Kural:** `sozluk_disa` sonrası daima kayıt sayısını HEAD ile karşılaştır; düşüş varsa yazma, birleştir. (Betik birleştirme kipine geçirilmeli — açık iş.)

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

### H536 — Değerlendirme kapısı tasarım PDF'inin harf aralıklı başlıklarını ("Y A N I TL A R", "KAYN AKLAR") kısaltma sanıyordu (2026-11-09, k2-22)
- **Belirti:** `degerlendirme_dogrula.py k2-22` 24 "kısaltma sözlükte yok" HATA'sı verdi: ITLAR, ÜRÜLE, ŞLEME, FREUD, GP…; hiçbiri kısaltma değildi.
- **Kök neden:** Psikiyatri slaytları tasarım şablonunda büyük harfli, harf aralığı açılmış başlık kullanıyor; pymupdf metni harf gruplarını ayrı jeton veriyor; kaynakça sayfası da "KAYN AKLAR" diye başladığı için H510 istisnası tutmuyordu; atıf satırındaki yazar baş harfleri (Yates GP) de aday sayılıyordu.
- **Kalıcı çözüm:** kapı tamamı büyük harf olan satırları (başlık/üst yazı) kısaltma taramasından çıkarır, ilk satırı boşluksuz birleştirip KAYNAK/REFERENCES ile başlayan sayfayı kaynakça sayar, "Soyad GP," atıf baş harflerini eler. Eski derslerde (k2-20/21/38) sonuç değişmedi (0 HATA).
- **Önleme:** Kapıyı geçmek için sözlüğe anlamsız kısaltma yazılmaz (H510); yeni biçim tuzağı kapının kendisinde düzeltilir.

### H548 — Slayt altındaki kaynak satırının dergi adı "sözlükte olmayan kısaltma" sayıldı (2026-11-10, k2-28 s.31)
- **Belirti:** `s31: kısaltma 'BMJ' sözlükte yok` HATA'sı; satır "Guan B, et al. BMJ Open. 2023;13:e075049." (şeklin kaynak künyesi).
- **Kök neden:** H510/H536 yalnız kaynakça SAYFALARINI ve "Soyad GP," atıf baş harflerini eliyordu; içerik slaydının altındaki tek satırlık künye taranıyordu.
- **Kalıcı çözüm:** "et al" ve "yıl;cilt" kalıbını birlikte taşıyan satır kısaltma taramasından çıkarıldı.
- **Önleme:** kapıyı geçmek için sözlüğe dergi adı ya da anlamsız kısaltma yazılmaz (H510); yeni biçim tuzağı kapının kendisinde düzeltilir.

### H571 — Ders içerik paketinde kısaltmaların hepsi `adim: 0` kaldı: `sayfalar.json` yedeği hiç çalışmadı (2026-11-13, k2-65 ders içerik paketi)
- **Belirti:** `python3 scripts/ders_icerik_uret.py k2-65-serebrovaskuler-hastaliklar` 0 HATA dedi, ama `ders_icerik_dogrula.py` "adim eşlenemeyen kayıt %10 (>%5)" verdi. Bakıldığında 311 kaydın 33'ü — kısaltmaların **tamamı** — `adim: 0` taşıyordu (`BDH`, `GİA`, `BT`, `MRG`, `TPA` …); spotlar/tablolar/listeler/kartlar/quiz (n taşıyanlar) sorunsuzdu.
- **Kök neden:** `scripts/ders_icerik_adim.py::destesiz()` kısaltmanın `adim`ini önce `taslak/sayfalar.json` içinde arıyor; bu dersin taslağında dosya **yok** (düz metin `meds_temp/ogrenci_ders/k2-65/sayfalar.json` ve `taslak/` altında yalnız `bilgi_havuzu.jsonl` var). Yedek yol yalnız `if not isinstance(sayfa, dict)` koşulunda çalışıyordu; dosya yokken `sayfa = {}` olduğu için koşul **False** kalıyor, 60 sayfalık gerçek `sayfalar.json` hiç okunmuyor ve her kısaltma 0'a düşüyordu. Yani boş sözlük "geçerli dict" sayıldığı için sessizce boş arama yapıldı; kapı hatayı yakalamasa paket yanlış adımlarla yayına girecekti.
- **Kalıcı çözüm:** Koşul `if not sayfa or not isinstance(sayfa, dict)` yapıldı: taslak dosyası yoksa ya da boşsa ders klasöründeki düz metin `sayfalar.json` okunur. Yeniden üretimde eşlenemeyen kayıt 33 → 0, kapı 0 HATA; kısaltmalar doğru sayfaya bağlandı (`BDH`→2, `GİA`→2, `CRP`→9, `BT`→15, `MRG`→15, `MCA`→17, `TND`→23, `TPA`→23, `İV`→25).
- **Önleme:** Bir yedek/ikinci kaynak yolu yazarken "dosya var mı" ile "içerik boş mu" ayrı sınanır — boş varsayılan (`{}`/`[]`) yedeği **atlatır**, `isinstance` kontrolü bunu yakalamaz. Kapı çıktısında `adim eşlenemeyen %N` görülürse önce kaynak dosyanın gerçekten okunduğu (`J(sp)` sonrası `len(sayfa)`), sonra hangi kayıt türünün 0 kaldığı (bu turda yalnız `kisaltmalar`) kontrol edilir; kapı 0 HATA verse bile paket körü körüne kabul edilmez.

## H613 — 5 Kurul 2 dersinde ders içerik paketi yoktu (2026-11-17)
- **Belirti:** k2-33/34/35/49/50'de "Bu dersin içerikleri" kartları (spot, tablo, liste, kart, kavram) yoktu; kapı 9 HATA veriyordu.
- **Kök neden:** destesiz derste paket `taslak/ders_icerik_ek.json` + `bilgi_havuzu.jsonl` ister, bunları yazan betik yoktu (önceki derslerde elle yazıldı); tasarruf koşularında atlanmıştı. Kapı, 2026-11-17'de kapatılan quiz'i zorunlu sayıyor; çözücü ve önem listesi başlıkla eşleniyordu (H608).
- **Kalıcı çözüm:** `scripts/uretim/ders_icerik/paketten_ek.py` (LLM yok): kapıdan geçmiş değerlendirme paketinden spot/liste/kart/kavram, PDF metin tablolarından tablo; görüntü tablo `taslak/tablolar_gorsel.json`'a slayttan birebir (k2-33 s.5). Kaynakta tablo yoksa gerekçe (≥12 kelime) → kapı UYARI (k2-49, k2-50: sayfalar tek tek incelendi). Kapıdan quiz çıkarıldı, eşleme defter koduyla.
- **Önleme:** paket girdisi elle değil `paketten_ek.py` ile; tablo muafiyeti yalnız yazılı gerekçeyle.
