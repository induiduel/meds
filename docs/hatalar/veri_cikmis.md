# Hata defteri — veri_cikmis (çıkmış soru verisi, eşleme, yıl/kurul etiketi)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

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

### H16 — Sesli ders listesinde iki ders aynı branş numarasını aldı (Meme Kanseri / Memenin Benign "33", 2026-10-20)
- **Kök:** branş içi numara Drive dosya adındaki `NN)` önekinden okunuyordu; Drive'da iki PDF aynı numarayla gelmişti,
  elle düzeltme tablosu (`BRANS_DUZELT`) gerekti.
- **Kurul 2 kuralı:** K2+ derslerinde branş ve numara YALNIZ ders kayıt defterinden (`src/data/dersler/kN.json`, kod
  `2n07` → 7) alınır; Drive adı numara kaynağı değildir. Elle tablo K1'e özgüdür, K2'ye satır eklenmez.
- **Kapı — EKLENDİ:** `canliDers.ts bransBilgisi` K2+ için kayıt defterini kullanır; `otomasyon/saglik.py
  kayit_defteri_sorunlari` her kurulda kimlik/kod/branş numarası çiftini sorun sayar (gece sağlık → bildirim).

### H19 — Çıkmış cevap anahtarı tıbben hatalı / iki kaynakta çelişik (2026-10-21, TBG kampı)
- **Görülen:** (1) 2018-2019 K1 `past-q-18-84` "nükleotid delesyon ve insersiyonları hangi yöntemlerle?" — cevap dosyası E
  (Southern blot + PCR + prometafaz bantlaması + dizi analizi); tıbben C (PCR ve dizi analizi): bantlama megabaz, Southern kilobaz
  düzeyindedir. Site açıklaması da "boyut yelpazesi" yorumuyla E'yi savunuyordu. (2) Kistik higroma + ASD/VSD aynı soru iki kaynakta
  Down / Edwards / Turner. (3) Over yönü genleri iki sürümde aynı üçlü bir yerde doğru, bir yerde yanlış.
- **Kural:** cevap anahtarını körü körüne kopyalama; her çıkmışın anahtarı ders kaynağına (slayt) karşı denetlenir, kaynakta yoksa
  tıbbi bilgiye göre. Anahtar değiştirilirse eski anahtar ve gerekçe **sorunun kendisinde** yazılır (açıklama + "Dikkat: sınavın cevap
  dosyasında X işaretli, tıbben hatalı"), çıkmış kaydında `anahtarDuzeltme {eski, yeni, tarih, gerekce}`, sesli anlatımda da söylenir.
  Aynı bilgiyi soran tekrar çiftleri şık METNİYLE karşılaştırılıp tek karara bağlanır (harf farkı şık sırasından olabilir).
- Kararlar: higroma → Turner şıkta varsa Turner, yoksa Down (g05 s30); over → FOXL2/RSPO1/WNT4 varsa o (g03 s30), yoksa WNT4+DAX1;
  nükleotid indel → C. Denetim raporları `meds_temp/spot_cozucu/genetik/celiski/`.
- K2–K6 taraması (2026-10-21): 51 anahtar düzeltildi; alt ajan denetiminde **soru başına kaynak araması + alıntı kaydı zorunlu** (`kanit_NN.jsonl`) — ilk turda ajanlar 76 soruyu ~6 aramayla "uygun" saydı. Araçlar `meds_temp/cikmis_celiski/`.

## [2026-10-21] Çıkmış soruda iç uyarı metni ve kalıp şık açıklaması (h06/19 Refik Saydam)

- **Hata:** Çözücüdeki çıkmış sorunun kökünde "[Dikkat — olası hatalı kayıt …]" iç notu kalmıştı; öğrenciye gösterildi ve EMA ile
  okundu. Aynı sorunun şık açıklamaları "bu soruda aranan özellik değildir ve elenir" kalıbıydı, ipucu konu dışıydı.
- **Karar (kullanıcı):** cevap anahtarı çelişkisinde tıbben/tarihen doğru olan esas alınır (224 sayılı Kanun 1961; Refik Saydam
  1942'de öldü → E). Not kökten çıkarıldı, şıklar ne/ne işe yarar/neden standardıyla yeniden yazılıp seslendirildi.
- **Kurul 2 kuralı:** soru kökü, şık ve seçeneklerde köşeli parantezli iç not ("Dikkat", "olası hatalı", "öğrenci notundan")
  yayına giremez; kaynak çelişkisi denetçi tarafından tıbbi doğruya göre çözülür ve gerekçesi kayda yazılır.

## H30 — Çıkmış konu eşlemesi birebir olunca ders sessizce çıkmışsız kalıyordu (2026-10-23 K2 provası)
- Ders kayıt defterindeki konu "Gebelik Terminolojisi ve Kavramları", çıkmış bankasındaki müfredat konusu
  "Gebelik Terminolojisi/Kavramları" → `a_hazirla` 0 çıkmış buldu ve hata vermeden devam etti (önem listesi ve çözücü boş kalırdı).
- Düzeltme: `ders_zinciri.konu_eslesen_cikmislar` üç basamak: birebir → yazım farkı ("/", "&", "ve", noktalama) yok sayılarak →
  ≥0,92 benzerlik; hangi yolla eşlendiği günlüğe yazılır. Sınama: Gebelik 27 (yazım farkı), Sifilis 19 (birebir).

## H54 — Benzer soru araması boş döndü, ders çıkmışsız üretildi (2026-10-24, k2-07 ikinci sınama)
- k2-07 Genel Anestezik İlaçlar: veritabanında bu konunun 19 çıkmışı varken `cikmis_adaylari` 30 sorguda da 200 + boş
  sonuç aldı (dizin o an hazır değildi). Hata sayılmadı: "0 çıkmış bağı", sesli metinde "0 önemli" vurgu.
  Birkaç dakika sonra aynı arama 40 aday verdi.
- Kapı: `isle.cikmis_adaylari` bütün sorgular boş gelirse 60 sn bekleyip bir kez yineler, yine boşsa iş durur (sonra
  yeniden dener). Çıkmışı gerçekten olmayan yeni konu yine üretilir; yalnız *hiçbir sorgu sonuç vermezse* durur.

## H57 — Kurul 2 derslerinde çıkmışlar neredeyse hiç duyulmuyordu (2026-10-24, kullanıcı)
- Kurul 1'de derste 11–13 "Burası önemli", 33–40 çıkmış/sınav anışı vardı; k2-07'de 4/0, k2-02'de 1/2. Bilgi anlatılıyor,
  `cikmis` alanına bağlanıyordu ama sesli söylenmiyordu: H22 dolgu yasağı + `max(3, bölüm/2)` "Burası önemli" tavanı
  dayanaklı çıkmış uyarısını da sildi. k2-02'de ayrıca arama tek aday döndürmüştü (H54).
- Kural: çıkmış uyarısı dolgu DEĞİLDİR. Her `ilgili` çıkmışın bilgisi anlatılır ve ilk geçtiği cümlede sesli söylenir
  ("bu bilgi çıkmışta soruldu"); tavan yalnız çıkmış dayanağı olmayan "Burası önemli"ye uygulanır. Dayanaksız çıkmış anışı yasak.
- Kapı: `isle.cikmis_ses_kapsam` (sesli_kapsam'a bağlı, Kurul 2+): ilgili çıkmış anlatılmamış / sesli uyarısız → HATA;
  "çıkmış/sınavda soruldu" geçen cümlede `cikmis` boş → HATA. Arama kurul filtresiyle <10 aday dönerse filtresiz yedek arama.

## H66 — İlgili çıkmış sorular sesli derste hiçbir cümleye bağlanmamış (2026-10-26, k2-24 epilepsi)
- **Belirti:** `arsiv_yayinla.py` 1/6'da 8 adet `sesli_kapsam: çıkmış …: bilgisi anlatılmamış (cümlenin cikmis listesine bağla)`.
- **Kök neden:** Bilgiler anlatılmıştı (s.5, 15, 33, 45, 50), ama `cikmis_baglantilari.json`'da `ilgili: true` olan sorular `konusma_v2.json` cümlelerinin `cikmis` listesine yazılmamıştı (tüm cümlelerde `cikmis: []`); sesli çıkmış uyarısı da yoktu.
- **Çözüm / kural:** Yazar, `ilgili: true` her çıkmışı `kanit.sayfa`/`slideNumber` sayfasında bilgiyi taşıyan cümlenin `cikmis` listesine bağlar ve o cümlede sesli uyarı ("Bu bilgi çıkmış sorularda soruldu.") verir. Kapı (`isle.py::cikmis_ses_kapsam`) gevşetilmedi.

## H69 — `cikmis_baglantilari.json` liste yerine nesne sarmalayıcısıyla yazıldı (2026-10-26, k2-46 sempatomimetikler)
- **Belirti:** `arsiv_yayinla.py` 5/6'da `AttributeError: 'str' object has no attribute 'get'` hatası vererek durdu (`bag_sayisi = len([x for x in json.loads(...) if x.get("ilgili")])`).
- **Kök neden:** `cikmis_baglantilari.json` dosyası doğrudan liste (`list[dict]`) olmak yerine `{"baglantilar": [...]}` şeklinde sözlük olarak yazılmıştı. Sözlük üzerinde iterasyon yapıldığında string anahtarlar dönmüş ve `.get()` patlamıştı.
- **Çözüm / kural:** `cikmis_baglantilari.json` daima kökte bir liste (`[{"soru_id": ..., "soru": ..., "ilgili": bool, "aciklama": ...}]`) olarak yazılır. `denetle.py` ve `arsiv_yayinla.py` doğrudan liste formatı bekler. Dosya düzeltildi, 0 HATA ile Oracle'a dağıtıldı.

## H79 — Otomatik çıkmış→cümle eşlemesi (vektör) derse ait olmayan soruları "çıkmış" diye bağladı (2026-10-27, y25-k2-01)
- **Belirti:** "Nörolojik Hastaya Yaklaşım" çıkmış listesinde hasta merkezli klinik yöntem, SVO prognozu, konversiyon bozukluğu,
  angular gyrus gibi bu derste geçmeyen 10 soru 0,92 puanla slayt 1'e bağlıydı.
- **Kök neden:** `cikmis_konum.py` her soruyu bge-m3 ile dersin en benzer cümlesine eşleyip eşik üstünü yazıyordu; "soru bu
  slayttaki bilgiyi mi soruyor" denetimi yoktu. Genel giriş cümlesi her nöroloji/psikiyatri sorusuna yüksek benzerlik verdi.
- **Çözüm:** Elle doğrulandı: 7 soru (4 doğrudan, 3 ilişkili), her birine `s` (slayt), birebir `kanit`, `seviye`,
  `dogrulandi:true`. Slayttaki yanıp sönen çıkmış chip'i yalnız `dogrulandi` kayıtları gösterir; `degerlendirme_dogrula.py`
  kanıtın slaytta birebir geçtiğini denetler.
- **Önleme kuralı:** "Çıkmışta soruldu" vurgusu ve chip yalnız doğrulanmış, slayt kanıtlı eşlemeye dayanır; vektör benzerliği
  yalnız aday listesidir. Metindeki "Bu bilgi çıkmış sınavda sorulmuştur" cümleleri de aynı kanıtla teyit edilir.

## H83 — "Çıkmış" diye gösterilen iki soru doğrulanamadı; biri sitede yüklenmedi (2026-10-27, kullanıcı bildirdi)
- **Belirti:** k2-01 slayt 3 chip'inde 2/2. soru "Soru yüklenemedi"; kullanıcı soruların orijinalini veritabanında bulamadı.
- **Kök neden:** (1) `4ba07c308e35`, `4c4eb178b88b`'nin yeniden yazılmış gizli kopyasıydı (sunulan listede yok → `/tek` 404).
  (2) `d3-k2-nor-014`'ün kaynak dosyası (`Noroloji_Kurul2_Cikmis_Sorular.json`) hiçbir ham klasörde yok; banka kaydı
  "doğrulanmış" etiketli olsa da özgün sınav belgesi bulunamadı. Eşlemede banka etiketine güvenildi, ham belge açılmadı.
  (3) Aşil sorusu bankada "2020-2021 / Kurul 1" etiketli; ham metinde 2021-2022 Kurul 5.
- **Çözüm:** Her soru ham belgede arandı (`meds_downloads/donem3/3. Sınıf/Kurul 2/2.Kurul-2021.pdf`, `21 22.txt`,
  `2. kurul .pdf`); kaynağı bulunan 5 soru kaldı, her kayda `kaynak` (belge + sayfa) yazıldı ve pencerede gösteriliyor.
- **Önleme kuralı:** Çıkmış eşlemesi yalnız **ham sınav belgesinde bulunan** soruyla yapılır; banka etiketi ("verified",
  "altin_standart") kanıt değildir. `kaynak` alanı olmayan kayıt `degerlendirme_dogrula.py`'de HATA. Gizli kopya
  (sunulmayan id) eşlenmez; hatırlama listesinden gelen sorunun şıkları "sonradan tamamlandı" diye belirtilir.

## H84 — Kaynağı olmayan 86 Kurul 2 "çıkmış"ı Check-Solve onayıyla görünür kalıyordu (2026-10-27)
- **Belirti:** Ham sınav belgesi taramasında 574 Kurul 2 sorusundan 86'sının özgün kaynağı bulunamadı (91/92 `d3-` önekli);
  76'sı 57 sesli dersin çıkmış listesindeydi. Rapor: `meds_database/derived/quarantine/kurul2_cikmis_kaynak_raporu.{md,csv}`.
- **Kök neden:** (1) `d3-*` kayıtları kaynak dosyası olmayan türetilmiş JSON'lardan (`*_Kurul2_Cikmis_Sorular.json`) geldi;
  "altin_standart/denetleyici_onayi" etiketleri özgünlüğü kanıtlamadı. (2) `applyQuarantine` Check-Solve ve Faz 14 onaylı
  soruları karantinadan muaf tutuyordu; 86'nın 86'sı Check-Solve onaylı olduğundan karantinaya yazmak hiçbirini gizlemezdi.
  (3) Sesli ders `cikmisKonum` listesi karantinayı hiç okumuyordu.
- **Çözüm:** 86 soru `karantina.json`'a `neden: kaynak_bulunamadi` ile yazıldı (silme yok; yedek `meds_temp/karantina_yedek_oracle_20261027.json`).
  `kaynakBulunamadi()` onay muafiyetinden ÖNCE uygulanır; `canliDers.ts` çıkmış listesini aynı kuralla süzer.
- **Önleme kuralı:** Banka/çıkmış eklemeleri ham sınav belgesindeki yerle (belge + sayfa) gelir; kaynak gösterilemeyen soru
  "çıkmış" olarak yayınlanmaz. Bir onay katmanı (Check-Solve, Faz 14) kaynağın yokluğunu gidermez. Geri alma: soruyu
  `karantina.json`'dan çıkarmak.

## H94 — Çıkmış listesinde birleştirilmiş gizli kopya: çip 404 verdi (2026-10-27, k2-03)
- **Belirti:** `/api/past-exams/tek/ea1ab6a5b61d` 404 (çip açılınca "Soru yüklenemedi").
- **Kök neden:** aynı kökün iki kopyası eşlendi; biri birleştirme katmanında gizli (`applyMergeOverlay`), sunulan listede yok.
- **Kural:** `cikmis_konum` yalnız sunulan soru kimliklerini içerir; canlı doğrulamada her kimlik `/tek` 200 vermeden ders tamam sayılmaz.

## H96 — Önem/çözücü zinciri ham belgede olmayan soruyu "çıkmış" diye kullandı (2026-10-27, k2-03)
- **Belirti:** k2patoloji 2p01 önem maddesi ve çözücüde "2020-2021 Final" etiketli `q-2021final_230619_142600-3-r68`; kaynak
  PDF'inde (`meds_sorular/2021final_230619_142600.pdf`) bu soru yok.
- **Kök neden:** `ders_zinciri` `hazirla` adımı çıkmış adaylarını bankadan konu eşlemesiyle seçer; ders için elle doğrulanan
  liste (`cikmis_konum`, kaynak taraması) ile karşılaştırılmaz. Bankadaki türetilmiş (`-rNN`) kayıtlar da aday olur.
- **Çözüm:** soru önemden `elenen_cikmis`e, çözücü ve `cikmis/2p01.json`'dan çıkarıldı (numaralar `numara.json`'da sabit).
- **Önleme kuralı:** zincirden sonra önem/çözücü/asistandaki her çıkmış kimliği ham belge taramasında `bulundu` ve `/tek` 200
  olmalı; değilse yayına girmez. `-rNN` türetilmiş kayıt hiçbir zaman çıkmış sayılmaz.

## H103 · Çıkmış adayı farklı dönem/ders sınavından geliyor; ham anahtar bankadaki cevapla çelişiyor; bankada olmayan çıkmışlar (2026-10-27, k2-05 Nörolojik Muayene)
- **Belirti:** Bankada "Nörolojik Muayene / Kraniyal Sinir Muayenesi" konulu 32 kayıt vardı; ham belgelerde yeri açıldığında: laterale bakış (abdusens) sorusu Dönem 2 Anatomi sınavından (`tüm sorular.pdf` s.544), Broca/Brodmann 44 sorusunun ham anahtarı "İdeomotor apraksi" (banka "Broca"), dil sapması sorusunun üç varyantında anahtarlar çelişkili. Buna karşılık dersin slayt bilgisini birebir ölçen sorular (kornea refleksi V–VII, Babinski patolojik, kas gücü 3/5 profili; `2.Kurul-2021.pdf` s.18, s.22) bankada hiç yoktu.
- **Kök neden:** Banka konu etiketi başka kaynaktan (Dönem 2 anatomi kitapçığı, FTR bölümü, türetilmiş `-rNN` kayıt) gelen soruyu bu derse atamış; etiket ham belgenin dönemini/dersini/anahtarını doğrulamıyor. Öte yandan banka, ham Kurul 2 sınavındaki tüm soruları taşımıyor.
- **Kural:** Çıkmış eşlemesi yalnız (a) ham belgenin DÖNEMİ ve DERSİ bu ders olan, (b) basılı anahtarı banka cevabıyla uyuşan, (c) slayt kanıtı birebir olan sorularla yapılır. Ham belgede olup bankada olmayan soru eşlenmez, `cikmis_taslak.json › bankada_yok_ham_belgede_var` listesine yazılıp bankaya ekleme kararı ana oturuma bırakılır. `-rNN` kayıt ham belgede doğrulansa bile karar ana oturumundur.

## H107 · Çıkmış eşlemesi: banka yıl etiketi ham belgeyle çelişiyor, yeniden yazılmış kökler, basılı anahtar yok (2026-10-27, k2-08)
- **Belirti:** `past-1790877040110-917236` etiketi 2020-2021, ham belge `22 23.pdf` = 2022-2023 Kurul 5; `past-q-18-85` etiketi 2018-2019 Kurul 1, ham belge `2016GKurul 5 soruları…pdf`; `d3-b-053` (Marfan) ham eşlemesi güvenilmez ve doğru şık (pektus karinatum) slayttaki pektus excavatum ile çelişiyor; `e07675f936c7`, `dea0348ff630` kökleri ham belgeden farklı yazılmış; `d3-k2-pat-008`/`d3-k2-tbg-008`/`d3-k5-pat-023` ham belgede yok. `22 23.pdf`, `İSKENDERUN…pdf`, `KURUL 2 ÇIKMIŞ 3.pdf` basılı anahtar taşımıyor.
- **Kök neden:** H83/H103 ile aynı: banka etiketi (yıl, kurul, "doğrulanmış") ham belgenin yılını/anahtarını kanıtlamıyor.
- **Kural:** `kaynak` ham belge adı + sayfa/soru no; çelişen yıl `yil_notu`na; basılı anahtar yoksa `anahtar_notu` ("tıbbi tutarlılık kontrol edildi"); kökü yeniden yazılmış sürüm ya da slayta ters doğru şık eşlenmez.

## H131 — Kurul 2 çıkmışlarında başka kurul soruları ve yanlış konu etiketleri (2026-10-28, kullanıcı bildirdi)
- **Belirti:** Kurul 2 çıkmışları arasında Kurul 1/3/5 konusu sorular (genel farmakoloji, tetanoz, Negri, halk sağlığı, pediatrik kabızlık, C8 kökü) ve komşu derse etiketlenmiş Kurul 2 soruları vardı.
- **Kök neden:** Soru kurulu sınav belgesinin kurul etiketinden geldi, ders/konu etiketi ise içerikle doğrulanmadı; Check-Solve/Faz 14 onayı da konu uygunluğunu kanıtlamaz.
- **Çözüm:** 574 soru ders programı + kazanım + 25-26 ders metni ile tarandı (`meds_temp/kurul2_soru_tespit/`, rapor `meds_database/derived/quarantine/kurul2_konu_tespit.csv`). 19 soru `karantina.json`'a `neden: kurul2_disi` ile yazıldı (`kaynakBulunamadi` bu nedeni de onay muafiyetinden önce uygular); 52 soruda konu/ders etiketi düzeltildi (`eskiKonu`/`eskiDers` saklı). 9 Primer Myelin önerisi 2026 programında ders olmadığı için uygulanmadı. Yedekler aynı klasörde.
- **Önleme kuralı:** Yeni çıkmış eşlemesinde konu etiketi içerik ile doğrulanır; geri alma: karantina kaydını silmek / eskiKonu'yu geri yazmak. Açık: 86 "elle bakılmalı" soru.

## H132 — Karantina listesi eskimişti; OCR ikizleri ve parça kayıtlar karantinada duruyordu (2026-10-28)
- **Belirti:** Karantinada 513 (eski `karantina.json`) + 47 `status=quarantined` + 86 `kaynak_bulunamadi` kayıt görünüyordu; çoğu aslında düzelmişti.
- **Kök neden:** (1) `karantina.json` 2026-10-07'den kalmaydı; 314+109 kayıt sonradan Check-Solve/Faz 14 ile onaylanmıştı, 43'ü Faz 17'de çöpe alınmıştı, 29'u kayıttan düşmüştü. (2) 53 karantina kaydı temiz bir ikizi olan OCR/site-kalıntısı kopyaydı (örn. `past-q-22_final_…-117` ↔ `q-22_final_…-117`; `ff640ee5472c` CYBE sorusunun parçası) — yanlış kümeleme/OCR bunları "bozuk soru" yaptı; bazılarında cevap bile yanlıştı (PBS sorusunda A işaretli, temiz ikizde D). (3) 84 `d3-k2-*`/türev kayıt çıkmış değil, ders notundan üretilmiş geçerli sorular; "Çıkmış Sınav / 2021-2026" etiketi yanlıştı.
- **Çözüm:** 53 kopya `birlestirmeler.json` grubuna (tekrar arşivi) alındı, `tekrarArsivi{asil,eslesen,onceki}` ile geri alınabilir; `karantina` etiketi ve `karantina.json` girdisi kaldırıldı. Yedek: `yedek/karantina_20261028/`.
- **Önleme:** Karantinaya almadan önce aynı soru/şık kümesine sahip sağlam kayıt aranır (stem+şık Jaccard); varsa karantina değil tekrar arşivi. Üretilmiş soru "çıkmış" etiketi taşımaz.

## H133 — Kaynağı doğrulanamayan sorular gizlenerek kaybedilmişti; "Çıkmış–Örnek" sınıfı (2026-10-28)
- **Belirti:** 104 soru (85 `kaynak_bulunamadi` + 19 `kurul2_disi`) karantinada duruyordu; çoğu tıbben doğru, müfredata uygun veya gerçek sınav sorusuydu.
- **Kök neden:** "Özgün belgede bulunamadı" ile "yanlış/bozuk" aynı kovaya konmuştu; gerçek çıkmış olma ihtimali olan sorular da gizlendi. Kurul 2 dışı tespiti Santral Sinir Sistemi Enfeksiyonları gibi Kurul 2 derslerini kaçırdı.
- **Çözüm:** 4 bağımsız denetçi 104 soruyu müfredat + ders notu + tekrar taramasıyla değerlendirdi: 72 `cikmis_ornek` (hem Çıkmışlar'da hem `k2-cikmis-ornek` Örnek sorular dersinde, öğrenciye "çıkmış olduğu doğrulanmadı" rozetiyle; sesli ders çıkmış chip'inden hariç), 15 serbest çıkmış, 9 tekrar arşivi, 7 karantinada (`siniflama` alanıyla gerekçeli). 5 soru ders notuna göre düzeltildi (`duzeltmeOnceki` saklı).
- **Önleme:** Kaynağı doğrulanamayan ama doğru soru gizlenmez, `kaynakSinifi=cikmis_ornek` ile etiketlenip öğrenciye belirtilir; çıkmış vurgusu yalnız doğrulanmış kaynağa dayanır.

## H390–H392 — Veri tutarlılığı: yıldız işaretleri, soru haritası sayımı, deste kurul adları, yinelenen kazanım konuları (2026-10-28, kullanıcı onayıyla)
- **H390 Belirti:** Deneme ekranında soru/şık metninde `**değildir**`, `**Soru:**` ham görünüyordu. **Kök neden:** veri doğru (kasıtlı vurgu; çıkmışta 49 soru, Öğren klinik karar vakalarında 414 öge), `PracticeV15` metni işlemeden yazıyordu. **Çözüm:** `**…**` kalın yazıya çevrilir; veri değişmedi.
- **H391 Belirti:** Soru haritası Kurul 2'de 498, çıkmış sayfası 571+ gösteriyordu. **Kök neden:** 178 çıkmış soruda `isPastExam` alanı yok (kaynakları çıkmış PDF'leri); harita betiği yalnız `true` olanları sayıyordu. **Çözüm:** `scripts/altyapi/v15/soru_haritasi.py` yalnız açıkça false ve gizli soruları dışlar; harita yeniden üretildi (K2 574).
- **H392a Deste kurul adları:** Kurul 1 için 12 yazım vardı; boş/"Ürogenital Sistem Komitesi" yazılı 4 deste öğrenci tarafında "Diğer"e düşüyordu. 74 destenin `committee` alanı "Kurul 1 - Ürogenital ve Obstetrik Kurulu" yapıldı (kaynak `interactive_learning_decks.json`, biçim birebir korundu; doğrulayıcı 0 HATA, paketler yeniden üretildi).
- **H392b Kazanım konu çiftleri:** Aynı dersin kesik/tam başlıklı iki kazanım kümesi (7 çift: K1 Genetik, K1 Üroloji ÜSE, K5 Demir, K5 Spondilodiskit, K6 Histamin, K6 Yaşlılıkta beslenme, K6 Biyokimya) tam başlıkta birleştirildi; yalnız birebir aynı 13 kazanım atıldı, kimlikleri taşındı (kazanım soruları, sınav çalışması, müfredat paketi, eşleme dizini byDeck yeniden üretildi; artık başvuru 0), slayt kanıtları birleşti. 25 konu başlığından hoca adı / "UZM." eki temizlendi. Ders kayıt defterine (`dersler/kN.json`) dokunulmadı: K5/K6 çiftleri orada iki ayrı ders kimliğidir (kural: kimlikler kalıcı). Betik: oturum yedeğiyle `kz/birlestir.py`.
- **Tuzaklar:** (1) `lite/`, `questions/`, `pastQuestions.json`, `sinav_calisma_k*.json` git dışıdır; dağıtım temiz `meds-dagitim` ağacından derler, bu dosyaların güncel kopyası oraya elle konmazsa canlı derleme eski veriyi gömer. (2) Çıkmışların canlı asıl kopyası Oracle `data/pastQuestions.json`'dır (sunucu bellekte tutup üzerine yazar); yerel `src/data/pastQuestions.json` yalnız yansıdır. Canlı çıkmış konu/kimlik güncellemesi ayrı, sunucu uçlarıyla yapılmalı (yapılmadı, açık).

## H393 — Canlı çıkmışlarda kazanım birleştirmesinden kalan eski konu adları / kimlikler (2026-10-28, kullanıcı onayıyla)
- **Belirti:** H392 sonrası canlı çıkmışlarda 56 soruda eski konu adı (`denetleyiciSurumu.topic`: K1 kesik başlık 2, hoca adlı 53) ve atılmış kazanım kimliği (`kazanim.id`, `checkSolve.mufredat.kazanimId`) kalmıştı.
- **Kök neden:** Canlı asıl kopya Oracle `data/pastQuestions.json`; sunucu bellekte tutup üzerine yazar, dağıtım dokunmaz. Dosyayı dışarıdan düzenlemek bellek kopyasıyla çakışır; panel ucu bu alanlara izin vermez.
- **Çözüm:** Yeni yönetim ucu `POST /api/admin/sorular/cikmis/esleme-uygula` (varsayılan önizleme; `uygula:true, onay:"ESLE"` ile tam yedek `data/_yedek/pastQuestions.esleme-oncesi.<zaman>.json` + değişim dosyası `data/_yedek/cikmis_esleme_<zaman>.json`, sunucunun kendi kaydetme/yansıtma/canlı olay yolu, denetim kaydı) ve `POST …/esleme-geri {dosya, onay:"GERI"}`. Geçmiş kayıtlar (`checkSolveOriginal`, `eskiSurum`, `phase14Original`, revizyonlar) atlanır. Yerelde önizle→uygula→geri al denendi, yerel dosya birebir geri yüklendi; canlıda önizleme 56 soru/57 değer (plan ile aynı) → uygulandı, diskte kalan 0, geçmiş kayıtlardaki 82 değer dokunulmadan. Canlı değişim dosyası: `cikmis_esleme_2026-10-28T17-37-02-423Z.json`.
- **Not:** Cloudflare, betikten gelen istekleri 1010 ile reddeder; yönetim ucu sunucuda `localhost:3000` üzerinden çağrılır. Yerel `src/data/pastQuestions.json` yansısında H392'de yanlışlıkla değişen 82 geçmiş kayıt değeri yedekten geri getirildi.
- **Kural:** Canlı çıkmış verisinde toplu değişiklik yalnız sunucu içinden, önizlemeli ve geri alınabilir yolla yapılır; geçmiş kayıt alanlarına toplu değiştirmede dokunulmaz.

## H450 — Çıkmış kayıtlarında uydurma ya da sınavdan sapmış şık/kök (D3K2 çıkmış PDF'leri, 2026-10-30)
- **Belirti:** D3K2 belgeleriyle karşılaştırınca mevcut kayıtlarda sınavda olmayan şıklar (ör. YAB'de "Endişeyi denetim altında tutmakta güçlük", SMA'da tip V yerine tip III, Joubert yerine "Polimikrogiri", MS plaklarında kayıp şık), olumsuza çevrilmiş kökler (palyatif bakım) ve bu yüzden yanlış cevaplar (ör. dd00370e9106, 151c7258613c, 73bb9a7a3782, 7d9098ad526e) çıktı.
- **Kök neden:** Faz 16 check-solve ve ders bazlı derlemeler (d3-k2-*) özgün sınav kâğıdını görmeden eksik/bozuk şıkları "tek doğru cevap" kuralını sağlamak için yeniden yazmış; özgünle benzerlik denetimi yoktu.
- **Çözüm:** 2020-21 karneleri (✓ = resmî), 2018-19 Kurul 4 resmî anahtarı ve 2019-20 kâğıt fotoğraflarıyla 122 kayıt özgüne döndürüldü (`meds_temp/d3k2_tum`, `araclar/dogrula.py` özgün şık benzerlik kapısı).
- **Önleme:** Özgün belge varken şık metni ondan sapamaz; sapma yalnız tıbbi zorunlulukla ve `degisiklikler` + açıklamada `Not:` ile. Şık değiştiren her ajan çıktısı özgün şıkla benzerlik kapısından geçer.

## H451 — Aynı sınavın derleme kopyaları ayrı görünen sorular olarak kalmış, bazılarının cevabı yanlış (2026-10-30)
- **Belirti:** 2025-26 Kurul 2'de aynı soru üç kaynaktan üç kez görünüyordu (d3-k2-* ders derlemesi, "25-26 dönem 3 kurul 2.pdf", aynı PDF'ten "2025-2026 Kurul 1" etiketli kayıtlar); 2019-20 kâğıdı "KURUL 2 ÇIKMIŞ 3" ve "dnm33snfkrl23snf2" içinde iki kez; kopyaların bir kısmında farklı (yanlış) cevap.
- **Kök neden:** Tekrar analizi yalnız aynı etiketli kayıtları birleştiriyordu; kaynak belgeleri farklı etiketlenen kopyalar (yılı belirsiz / yanlış kurul) hiç aday olmadı. Ajan aday listesi de benzerlik + etiketle kurulduğu için bazı kopyalar listeye düşmedi.
- **Çözüm:** Kopyalar birleştirildi (görünen = PDF'le doğrulanmış kayıt) ve içerik eşitlendi; yanlış "Kurul 1" etiketleri düzeltildi; ajanın aday dışı bulduğu kopyalar `girdi/manuel_kararlar.json` ile bağlandı.
- **Önleme:** Yeni çıkmış belgesi işlenirken önce o sınavın TÜM derleme kopyaları belge adına göre toplanır; "aday listesinde yok" diye ATLA/YENI verilmez, ana oturuma bildirilir.

## H452 — Sınav yılı/kurul etiketi belge kanıtı olmadan tahmin edilmişti (2026-10-30)
- **Belirti:** "KURUL 2 ÇIKMIŞ 3" kayıtlarının bir kısmı "2025-2026 Final", 2024-25 WhatsApp dökümü ("2. kurul .pdf") "Yılı belirsiz"; bir birleştirme grubu 2023-24 ve 2024-25 kopyalarını birlikte tutuyordu. Öğrencinin "D3K2 2021-2022-2023" adlı kâğıdı aslında 2018-2019 Kurul 4 sınavıydı (meds_downloads/…/Kurul 4/Kurul IV Sınavı.pdf, resmî anahtar 04.03.2019).
- **Kök neden:** Yıl dosya adından/çevre kayıtlardan çıkarılıyordu; gruba yıl yazılırken üyelerin kendi belge yılı denetlenmiyordu.
- **Çözüm:** Belge yılı haritası (`05_uygula.py` BELGE_YILI), farklı yıllı grup üyesi ayrılıp bantla bağlandı; 183 kaydın yılı belgeyle kesinleşti; 2018-19 K4 resmî anahtarla eklendi (78 cevabın 75'i ajanların bağımsız sonucuyla aynıydı).
- **Önleme:** Yıl yalnız belge kanıtıyla (resmî anahtar, sınav sitesi karnesi, belge başlığı) kesinleşir; aynı yıl + aynı kurul dışındaki kopyalar birleştirilmez, `similarPastQuestions` ile bağlanır (kullanıcı kararı 2026-10-30: her yıla ayrı kayıt).

## H453 — Çıkmış PDF ayıklama tuzakları (2026-10-30)
- **Belirti/kök neden:** (1) Karne çıktısında soru sonraki sayfaya taşınınca aynı soru iki kümeye bölündü ve iki yeni kayıt oluştu; (2) daktilo metinde sonraki sorunun kökü önceki E şıkkına yapıştı; (3) karne sayfa altlığındaki öğrenci adları şık metnine karıştı; (4) paralel ajanlar aynı geçici betik adını kullandı.
- **Çözüm:** Karne kopyaları birleştirildi; kök/şık el ile ayrıldı; sayfa üst/alt bilgisi ve adlar ayıklamada siliniyor; ajan betikleri `/tmp/claude-1000/<parti>/` altında.
- **Önleme:** Ayıklamadan sonra kaynak içi tekrar taraması (aynı sınav yeni kayıt çifti) ve kişisel veri taraması zorunlu; her paralel ajana ayrı geçici klasör verilir.

## H454 — Aynı soru iki yılın hatırlamasında farklı ifadeyle geçince bağlanmadı; aynı sınavın iki hatırlaması iki ayrı soru sanıldı (2026-10-31)
- **Belirti:** 2024-25 "okülomotor sinir tutulumunda etkilenen komşuluk" (#11a) ile "CR3 çiftleri tutulunca hasar nerede" (#27) aynı sınavın
  aynı sorusuydu; 2025-26 hatırlamasında aynı soru ("okülomotor sinirler → sinüs kavernozus", h31) ve "anterior hasar → spinal iskemik
  hasar" (h32) vardı. İlk turda hiçbiri birbirine bağlanmadı; kurgu turunda ajan #11a için uydurma bir herniasyon sorusu kurmuştu.
- **Kök neden:** Aday listeleri işe başlarken alınan veritabanından üretildi; aynı koşuda oluşan yeni kayıtlar birbirine aday olamadı.
  Veritabanı bağlantı taraması (token_sort ≥ 88 + aynı cevap) hatırlamaların farklı ifadesini yakalamıyor.
- **Çözüm:** #11a, #27 grubuna katıldı (`_birlestir`); #27 ↔ h31 ve #11c ↔ h32 `_bagla` ile bantlandı.
- **Önleme:** Hatırlama belgeleri işlenirken farklı yılların YENİ kayıtları arasında da konu + cevap metni eşleşmesiyle tarama yapılır;
  aynı sınavda "aynı soru olabilir" notlu ögeler önce birleştirilir, ayrı soru kurulmaz (uydurma soru yasağı kurguda da geçerli).

## H455 — Çıkmış kayıtlarında sınav yılı çok yıllı aralık ("2021-2026") ya da yılsız etiket ("Geçmiş Yıllar Çıkmışı (Arşiv)", "Kategorisiz", "2026") kalmıştı (2026-10-31)
- **Belirti:** Yıl filtresinde "2021-2026" (692 kayıt), "Geçmiş Yıllar Çıkmışı (Arşiv)" (310), "Kategorisiz" (134), "2026" (25),
  "2025-2026 (Geçen Sene)" (5) grupları vardı; öğrenci bir sorunun hangi yılın sınavı olduğunu göremiyordu, aynı soru farklı yıllarda
  farklı etiketlerle duruyordu.
- **Kök neden:** Ders derlemesi üretim betikleri (`scripts/arsiv/archive/generate_kurul*_redakte_sorular.mjs`) `examYear: '2021-2026'` sabitini
  yazdı; soru notundaki gerçek yıl (`sourceNote`) alana taşınmadı. Eski içe aktarımlar yıl bulamayınca "Geçmiş Yıllar…"/"Kategorisiz"
  koydu; mega kayıt parçalama "2026" (işlem yılı) yazdı. Belge düzeyi yıl kanıtı (karne tarihi, belge içi tarih, dosya adı) hiç kullanılmadı.
- **Çözüm:** `meds_temp/cikmis_yil_duzelt/yil_duzelt.py` kural zinciri (soru notu → D3K1 PDF eşlemesi → tekrar analizi kimliği → belge
  tablosu → benzer tarihli kayıt → belirsiz) ile 1.169 kayıt tek yıla/≤2 yıla indirildi, 404'ü `Yılı belirsiz` + `yil_belirsiz`; her kararın
  gerekçesi `yilDuzeltmesi` + `evidence`'ta. Türev dosyalar kimlikle eşitlendi.
- **Önleme:** Yeni çıkmış kaydında `examYear` yalnız "YYYY-YYYY" (tek akademik yıl) ya da en çok iki yıl ("2021-2023") olabilir; kanıt yoksa
  `Yılı belirsiz` + `yil_belirsiz` etiketi yazılır, asla işlem yılı/geniş aralık/kategori adı yazılmaz. Derleme/toplu içe aktarımda soru notundaki
  yıl alana taşınır; belge yılı belge içi tarih/karne numarası/dosya adıyla doğrulanır ve `sinavKimligi.gerekce`'ye yazılır.
  Kapı: `python3 meds_temp/cikmis_yil_duzelt/yil_duzelt.py` kuru koşusunda "Geçersiz biçimde kalan: 0" olmalı.

### H547 — Gövdesi yalnız resim olan slayda dayanan doğrudan çıkmış, değerlendirme kapısından geçemiyordu (2026-11-10, k2-28 s.21)
- **Belirti:** `degerlendirme_dogrula.py k2-28` iki doğrudan çıkmış için "kanıt s21'de yok" HATA'sı verdi (`past-q-karma-38`, `d3-b-034`: sakral korunma yoksa yaralanma komplettir).
- **Kök neden:** s.21 (komplet/inkomplet şeması) tümüyle görüntü, metin katmanı boş. Kapı çıkmış kanıtını pymupdf metninde birebir arıyor; metinsiz görsel sayfa istisnası yalnız atomlar için yazılmıştı (`gorsel` + sayfa metni < 60 karakter), çıkmış kanıtı için yoktu. Tek çıkış yolu kanıtı ilgisiz bir satıra kaydırmak gibi görünüyordu (H543'teki kaçış).
- **Kalıcı çözüm:** kapıya atom kuralının eşi eklendi: çıkmış kaydı `kanit_goruntu` (görüntüden okunan cümle) taşıyorsa ve sayfa metni 60 karakterden kısaysa birebir arama atlanır; `cikmis_konum_yaz.py` bu alanı yayın dosyasına taşır. k2-16/24/26'da sonuç değişmedi (0 HATA).
- **Önleme:** görüntü sayfasına dayanan çıkmış eşlemesi `kanit` + `kanit_goruntu` ile yazılır ve denetçi sayfa görüntüsüne bakar; kanıt metni olan başka satıra kaydırılmaz, eşik gevşetilmez.

