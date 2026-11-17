# Hata defteri — soru_cozucu (örnek soru, şık açıklaması, sesli çözücü, önem listesi)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## H1 — Geçiştirici şık açıklaması (2026-10-18)

- **Görülen:** Sınav asistanı → Yardım al (Patoloji 08, IL-17 sorusu): "IL-2 bu sorunun cevabı değil.", "IL-10 nötrofil alımı
  yapmaz.", "IL-13 nötrofil toplayıcı olarak geçmez."
- **Neden hata:** Şıkkın ne olduğunu ve ne işe yaradığını söylemiyor; öğrenciye hiçbir şey öğretmiyor.
- **Kurul 2'de doğrusu:** Her şık (doğru dahil) için kavramın ne olduğu + ne işe yaradığı + bu soruda neden doğru/yanlış olduğu,
  2–3 cümle. Ayrıntı: `meds/docs/SIK_ACIKLAMA_STANDARDI.md`.
- **Kapı:** `meds/scripts/sik_aciklama.py`.

### H7 — Düzeltme tek kopyada kalıyor (çözücüde düzeltilen soru spot/asistan/örnekte eski)
- **Kural:** soru kimliği tek; denetçi düzeltmesi tüm kopyalara yayılır.
- **Kapı — EKLENDİ:** `ders_zinciri.kopya_tutarliligi` (birleştirme sonrası): aynı kökteki soru önem listesi (çıkmış +
  örnek) ile çözücüde farklı doğru şık METNİYLE duramaz (harf farkı serbest: şık sırası değişebilir) → kod 13. K1'in 6
  branşında 0 yanlış pozitif; sahte uyuşmazlık yakalandı.

### H21 — Soru çözücü sonradan genişleyince Son Prova soru kimlikleri kaydı (Kadın Doğum, 2026-10-21)
- **Görülen:** `k1-93-son-prova-kadin-dogum` doğrulaması 16 HATA "soru ref havuzda yok". Part 02:12'de yazıldı; 04:01–04:21'de
  Kadın Doğum çözücüsüne 15 soru eklendi, setler (`k02-1`/`k02-2`) yeniden numaralandı. Sitedeki Son Prova bozulmadı (sorular
  yayın dosyasında kendi kopyasıyla, denetimde yeniden yazılanlar `t06#…` kimliğiyle duruyordu).
- **Düzeltme:** `dogrula.py` denetimde yeniden yazılmış soruyu (`duzelt/eslem.json` → yayındaki `t0N#…`) geçerli sayar; yalnız
  numarası kayan `k01-2#32` → `k01-1#32`. 14 part 0 HATA, yayındaki tüm kimlikler karşılıklı.
- **Kurul 2 kuralı:** Son Prova yazıldıktan sonra çözücü değişirse part yeniden yazılır — `son_prova_zinciri.part_izi` ders
  başına havuz soru sayısını içerir, değişince part `_eski/`'ye alınıp baştan yazılır. Kurul 1'de `soru_dagit.py` elle yeniden
  çalıştırılmamalı (kayan 15 eski kimlik havuzda yok); gerekirse önce parça referansları güncellenir.

### H28 — Doğrulayıcı tıbbi "kaynaklı"yı süreç dili sanıyordu; önem ↔ çözücü şık uzunluğu uyumsuzdu (2026-10-23)
- `patoloji_cozucu/cozucu_dogrula2.py` `IC_DIL` `kaynak\w*` kalıbı "plazma kaynaklı", "endotelden kaynaklanır", "enfeksiyon
  kaynağı" ifadelerini HATA sayıyordu (çözücü ve asistan şık açıklamaları). Kalıp yalnız süreç biçimlerine daraltıldı
  (kaynakta, kaynağa göre, kaynakça, kaynak metin).
- Önem listesi talimatı örnek şıklara ≤14 kelime (uyarı) izin verirken çözücü kapısı örnek şıkta ≤6 kelime istiyor → önem
  aşamasından geçen soru çözücüde kalıyordu. Görev kuralı 6 kelimeye indirildi (`kurallar/ornek_soru_spot.md`).
- Not: Kurul 1 Claude çözücüleri (ör. e07) bugünkü kapıdan geçmez (486 HATA, 2026-10-18 şık standardından önce üretildi);
  K1 çıktısı kalite kıyasında referans alınırken bu bilinmeli.

### H29 — "Burası önemli" kuralları birbiriyle çelişiyordu; OCR'lı sayıda sıfır kayıp yanlış alarmı (2026-10-23)
- `TALIMAT_SESLI.md` her ilgili çıkmışta "Burası önemli" isterken `metin_denetle.py` (H22) toplamı `max(3, bölüm/2)` ile sınırlar
  → çok çıkmışlı derste ikisi birden sağlanamaz. Karar: H22 (daha yeni kullanıcı kuralı) esas; her çıkmış `vurgu tur=cikmis` ile
  işaretlenir, "Burası önemli" sınır içinde en çok sorulanlarda. Talimat güncellendi (Oracle'da sonraki dağıtımla); görev yolunda
  `sesli_bolum` bölüm başına en çok 1, birleştirici ders sınırını betikle uygular (`onem_sinirla`).
- Sesli metin ekranında sayılar yazıyla yazılmıştı ("iki yüz seksen gün") — okunuş ekrana sızması (önceki H "Okunuş ekrana");
  görev kuralı: ekran rakamla, okunuş yalnız `ses`te; sıfır kayıp kapısı bunu yakalar.
- OCR'lı tablo sayfasında bozuk sayılar ("185-249 kg/m" = 18,5–24,9) düzeltilerek anlatılınca sıfır kayıp kapısı yanlış alarm
  veriyordu → `baglam.ocr_sayfalar` sayfaları ve ondalık ayracı düşmüş eşdeğerler muaf.

## H31 — Hesap sorusu yanlış alarmı + iç etiketin öğrenci metnine sızması (2026-10-23 K2 provası)
- Naegele tarih sorusunun doğru şıkkı ("10.02.2021") maddede yazmaz, kuraldan hesaplanır; önem görevinin çözülebilirlik kapısı
  "çözülemiyor" diyordu → doğru şık yalnız sayı/tarih/birimse kökteki kural terimlerinden ≥2'si maddede olması yeter.
- Ücretsiz model detay alanına "Q3 ve Q4'te verilen tarihler…" yazdı (öğrenci Q3'ü bilmez). Ortak kapı
  `cekirdek.etiket_sizintisi` (yönlendirici + `gorev.py dogrula`): pakette verilmiş kısa etiket öğrenci metninde kalırsa HATA;
  girdide tıbbi anlamda da geçen (S1 kalp sesi, L4 omur) muaf; iç veri görevleri `OGRENCI_METNI = False`. Kural `cikti_disiplini.md`.

## H32 — Zorluk parça içinde yuvarlanınca ders toplamı hedefin altında kalıyordu (2026-10-23 K2 provası)
- 6 parçanın 6'sı ücretsiz katmanda geçti ama birleştirme "zor %9 (hedef %15–25)" ile durdu: 3 soruluk parçada %20 zor → 0.
- Düzeltme: `_spot.zorluk_dagit` zorluğu ders düzeyinde dağıtıp parçalara dilimler; parça kapısı zor soruda plandan eksiği kabul etmez.

## H62 — Quiz Üretiminde Öncelik Sırasının İhlali, Çifte Analiz Maliyeti ve Yarış Durumu Hatası (2026-10-26)

- **Belirti (Risk):** Drive'a yeni ders geldiğinde Quiz ajanlarının Sesli Ders süreci tamamlanmadan devreye girmesi, sesli dersin analiziyle quiz analizinin mükerrer yapılması (duplikasyon), dosya ezilmesi (overwrite) veya henüz onaylanmamış sesli ders taslağı üzerinden tutarsız soru havuzu üretilmesi.
- **Kök Neden:** Pipeline adımları arasında katı bir durum bağımlılığı (state dependency) ve tekil analiz deposu (Single Source of Truth) olmaması; modüllerin asenkron veya paralel başlatılması durumunda yarış durumu (race condition) doğması.
- **Çözüm & Kural:**
  1. **Öncelik Kilidi (Priority Lock):** Sesli Ders (Audio Lesson) `COMPLETED` (onaylı `konusma_v2.json` ve 0 HATA denetim) durumuna geçmeden Quiz soru üretim ajanları KESİNLİKLE tetiklenemez.
  2. **Kapsam Kilidi (Scope Lock):** Quiz üretimi şimdilik YALNIZCA `Farmakoloji` (`Tıbbi Farmakoloji`) dersi için aktiftir. Kod altyapısı ders-bağımsız (`course-agnostic`) kurulmuştur.
  3. **Single Source of Truth:** Sesli dersin ilk analiz adımında üretilen `atomik_bilgi_envanteri.json`, hem Sesli Dersi hem de ardından çalışacak Quiz Ajanını besler. İkinci bir LLM analizi yapılmaz; mükerrer araştırma yasaktır.
  4. **2x Çapraz Sorgulama ve Batch Processing:** $N$ atomik bilgi $\rightarrow$ en az $2N$ soru. Token limitine takılmamak için en fazla 25 atom (50 soru) partileri halinde döngüyle işlenir.
- **Kapı:** `meds/scripts/hat/quiz_motoru/quiz_dogrula.py` (Öncelik kilidi, 2x soru kuralı, 5-15 sn okunma süresi, gerekçeli şık açıklamaları, sıfır halüsinasyon). Çıkış kod 0 olmadan yayın yapılamaz.

## H86 — Ders işçisi denetimi örnek soru şık açıklamalarını standart kapıdan geçirmiyordu (2026-10-27, k2-03)
- **Belirti:** k2-03 taslağı `denetle.py` ile 0 HATA verdi, ama örnek soruların şık açıklamalarında `sik_aciklama.py` 98 hata
  buldu (20 kelimenin altında, "ne/ne işe yarar/neden" eksik); q18'de müfredat dışı iki çeldirici (oligoklonal bant, LP basıncı).
- **Kök neden:** `denetle.py` yalnız ≥20 karakter uzunluk denetliyordu; şık açıklama standardı (kural 14) yalnız asistan/çözücü
  doğrulayıcılarına bağlıydı, ders paketinin örnek sorularına bağlı değildi.
- **Çözüm:** `denetle.py` Kurul 2+ dersinde her şık açıklamasını `sik_aciklama.denetle` + `turkce_uslup.denetle` ile HATA verir.
  k2-03'ün 110 şık açıklaması yeniden yazıldı; q18 çeldiricileri dersin kendi kavramlarıyla değiştirildi.
- **Önleme kuralı:** örnek soru çeldiricisi de müfredattan (öğretilmiş komşu kavram) seçilir (AGENTS kural 4, 9).

## H119 · Örnek sorularda öznel/ders çağrıştıran kök ve rastgele slayt sorusu (2026-10-27)
- **Belirti:** Soru kökleri "dersin bölümüne göre…" gibi ifadeler içeriyor, çıkmış soru kalıplarına uymuyor, bazı sorular müfredat/kazanım dışı rastgele ayrıntı soruyordu.
- **Kök neden:** Talimat kaynak sadakatini ve şık standardını söylüyordu ama soru kökü üslubunu ve "her soru bir kazanıma hizmet etmeli" şartını söylemiyordu; yazar slayttan çıkan her bilgiyi soruya çevirdi.
- **Kural:** Kök bağımsız ve çıkmış-benzeri kalıpta; ders/slayt/bölüm göndermesi yok; her soru kazanım–konu bağlı, tıbbi ve sınav değerli. Kaynak: `TALIMAT.md` §4, `TALIMAT_ONEM.md`, `KURUL2_DERS_STANDARDI.md` §10.9.


## H120 · Dallanmalı soruda doğru/yanlış bayrağı ters işaretliydi (2026-10-27, k2-01)
- **Belirti:** Öğren destesi slayt 1 klinik karar sorusunda, Merritt'e uyan şık `isCorrect:false` ama geri bildirimi "Doğru…", ters şık `isCorrect:true` ama "Yanlış…". Öğrenci doğruyu yanlış öğrenirdi.
- **Kök neden:** Yazar ajan şıkları ve bayrakları ayrı yazdı; `validate_learning_decks.py` yalnız "tek isCorrect var mı" bakıyordu, bayrak ↔ geri bildirim yönünü karşılaştırmıyordu. İlk bağımsız denetçi bunu yakalamadı; ikincisi betikle taradı.
- **Kalıcı çözüm:** doğrulayıcıya `klinik-karar-bayrak` HATA kapısı (geri bildirim "Doğru/Yanlış" ile başlıyor ve bayrakla çelişiyorsa). Önleme: bayrak ve geri bildirim tek yerden üretilir; denetçi kapı dışı tutarlılık taraması yapar; doğru şık hep ilk sırada olmaz.

## H435 — Örnek sorular hocanın yeni sınav kalıbını yansıtmıyordu (2026-10-29, kullanıcı bildirdi)
- **Belirti:** Kurul 1 2026-27 patoloji sınavı kısa tek-kavram şıkları yerine bileşik/kombinasyon şıklı, "en tipik/en olası" köklü sorularla geldi; hazırlanan örnek sorular bunu karşılamıyordu.
- **Kök neden:** Üslup yalnız eski çıkmışlardan (2018–25: bileşik şık %14, üstünlük kökü %12) örneklenmişti; yeni sınav ve slayt biçimi (kırmızı/sarı/kalın) hiç ölçülmemişti, önem puanı biçime ve tekrar edilen eski konulara dayanıyordu.
- **Kural / Önleme:** Patoloji örnek soru ve önem noktası `docs/PATOLOJI_HOCA_SORU_MANTIGI.md` + `scripts/uretim/patoloji_soru_isci/` kapısına göre yazılır: her önem noktasına ≥2 farklı kalıpta soru, çeldirici yalnız aynı dersin komşu kavramları, doğru şık en uzun olmaz. Sarı dolgu ve başlık önem sinyali sayılmaz; kırmızı tek başına "önemli" değildir (slaytların ~%42'si kırmızı).
- **Kapı:** `python3 scripts/uretim/patoloji_soru_isci/dogrula.py sorular.json paket.json` → 0 HATA.

## H436 — Ara soru şık açıklamalarında ileriye sızıntı ve kaynakta olmayan iddia (2026-10-29, bağımsız denetçi buldu)
- **Belirti:** Kurul 2 ara sorularının ilk yazımında kapılar 0 HATA verdiği hâlde denetçi 7 dersin 6'sında düzeltme istedi: şık açıklamaları sorunun açıldığı slayttan SONRA anlatılan bilgiyi kullanıyordu (ör. 2. slayttaki soruda 9–11. slaytın kan şekeri/O2/elektroliti), kaynakta olmayan tanım ekleniyordu (Alzheimer plağı "nöron içi inklüzyon", Goldenhar'da "kalp bulgusu yok", kontraktilite baskısı beş ajanın yerine ikisine bağlanmış), bir GKS çeldiricisinin toplamı yanlıştı.
- **Kök neden:** `kur.py` ileriye sızıntıyı yalnız `dayanak` listesi ve `anlatim`'daki numaralı slayt atfıyla denetliyor; şık açıklamalarındaki serbest metin (hangi bilgi hangi slaytta) betikle ölçülemiyor. Yazar konuyu bütün dersten bildiği için açıklamaya ileriki bilgiyi doğal olarak katıyor.
- **Kural / önleme:** Şık açıklaması, ipucu ve çözüm de yalnız `ara.sayfa` ve öncesindeki slaytların bilgisini kullanır; tıbbi tanım slayt metninde yoksa yazılmaz. Bağımsız denetçi (TALIMAT adım 7) her soruda bunu slayt slayt arar; düzeltilen sorular ikinci kez denetlenir. Ders akış metni (Whisper dökümünden beslenmiş olabilir) tıbbi kaynak değildir; terim/sayı yalnız PDF sayfa metninden alınır.

## H490 — Öğrenci önem kapısı geçilemez yanlış HATA veriyordu (k2-15, k2-16, k2-11; 2026-11-05)
- **Belirti:** `ogrenci_onem/kapi.py` anlatımda bulunan bilgiler için HATA verdi (anterior singulat, temporal lob, kısa psikotikte tam dönüş, rehabilitasyon ana ilkeleri) ve bu yılın slaytında olmayan çıkmışları (LSD/izoniazid/MAO, görüşme, kalıtım %20) anlatımda istedi. Kural 28 bunları anlatıma yazmayı yasakladığı için kapı hiçbir yoldan geçilemiyordu.
- **Kök neden:** (1) öncüllü çıkmışın cevabı ("I, II, III ve IV") cümlede aranıyordu — Romen rakamı anlatımda geçemez; (2) kısa not ↔ uzun liste cümlesi benzerliği doğal olarak düşük (0,3–0,5); (3) bilgi parçasının bu yılın slaytında olup olmadığına bakılmıyordu.
- **Çözüm (eşik gevşetilmedi):** öncüllü cevap seçilen öncüllerin metnine açılır; bilgi slaytta AÇIKÇA yoksa (sayfa benzerliği < 0,55 VE kök örtüşmesi < 0,4) kapsamdan çıkar ve BİLGİ olarak listelenir; doğrulanmış eşleme dosyası `src/data/ogrenci_onem/esleme/<ders>.json` (`anlatim`: cümle anlatımda birebir + benzerlik ≥ 0,55 ya da anahtar terim cümlede birebir/notta ≥ 0,8; `celiski`: slayt alıntısı sayfada birebir; `slayt_disi`: terimlerin hiçbir sayfada geçmediği denetlenir). Uydurma kayıt HATA verir (sınandı). Gerçek eksik (yaz mevsimi tuzağı, k2-15) anlatıma eklendi.
- **Kural:** kapı HATA'sı "eşleyici kaçırıyor" diye bırakılmaz: ya anlatım düzeltilir ya kapının kendisinin denetlediği kanıtlı eşleme yazılır.

### H511 — Şık açıklamalarına betikle yeni geçiştirme kalıpları eklendi, kapı yakalamadı (2026-11-06)
- **Belirti:** k2-38 çözücüsünde 78 yanlış şık açıklaması "bu soruda seçilecek ifade bu değildir" ile; k2-37 örnek sorularında 80 açıklama "kökte tarif edilen duruma uyan seçenek ise …" ile bitiyordu. Bağımsız denetçi yakaladı.
- **Kök neden:** Alt ajan kelime alt sınırını tutturmak için açıklamaların sonuna betikle sabit bir cümle ekledi; `sik_aciklama.py` `BOS_KALIP` yalnız bilinen kalıpları tanıyordu, yeni ifadeyle aynı geçiştirme geçti.
- **Kalıcı çözüm:** İki kalıp `BOS_KALIP`'e eklendi; açıklamalar şık şık yeniden yazıldı.
- **Önleme:** Şık açıklamasına betikle sabit cümle eklemek YASAK; kısa açıklama elle, şıkka özgü gerekçeyle uzatılır. Denetçi aynı cümlenin ≥3 şıkta geçmesini bulgu sayar.

### H541 — Destesiz derslerin örnek soruları k2-12'den beri siteye yayınlanmıyordu (2026-11-10)
- **Belirti:** `src/data/ornek_sorular/k2/index.json` yalnız k2-01…k2-11; k2-12…k2-21, k2-37, k2-38 örnek soruları yalnız `taslak/ornek_sorular.json`'da ve çözücüdeki 20 örnekte kaldı; "Örnek sorular" kartı bu derslerde boş.
- **Kök neden:** `yayinla.py` örnek soruları deste doğrulayıcısından sonra s16 ile yayınlıyor; destesiz akış (`yayin_hazirla_destesiz.sh`) `yayinla.py`'yi atlıyor, s16 adımı başka yerde yoktu.
- **Çözüm:** `meds_temp/ogrenci_ders/arac/ornek_yayinla.py <kimlik> <anahtar>` (ders paketi → `kurul2_ders_paketleri`, sorular → s16 build (kurul 2) → `disa_aktar`); 6. partide 4 ders yayınlandı. **Açık:** k2-12…k2-21, k2-37, k2-38 için koşulmalı (kullanıcı kararı; s16 denetimi yazarların bıraktığı eksikleri gösterebilir). s16 K2 index'inde k2-01/02/05/08 yazım dosyaları boş olduğu için sorunlu görünüyor (site dosyaları korunuyor).
- **Önleme:** destesiz yayın betiğine s16 adımı eklenir; `ders_icerik_dogrula.py` sitede örnek soru dosyası yoksa HATA versin (yapılacak).

### H549 — Önem maddesinin alıntısı olarak slayttaki kaynak künyesi yazıldı (2026-11-10, k2-28 2t02-23)
- **Belirti:** "Nöroplastisite ve iyileşmenin üç kavramı" maddesinin `alinti` alanı "Langhorne P, Bernhardt J, Kwakkel G. Lancet" idi; asıl tanım cümlesi doğrulayıcının okumadığı `alinti_gorsel` alanına konmuştu. Öğrenciye alıntı diye künye gösterilecekti.
- **Kök neden:** s.9 tümüyle görüntü; metin katmanında yalnız künye satırı var. `onem_dogrula.py` alıntıyı PDF metninde birebir arıyor, görsel sayfa için yol yoktu; yazar kapıdan geçen tek satırı alıntı yaptı (H543 ile aynı kaçış).
- **Kalıcı çözüm:** `onem_dogrula.py`: alıntı `gorsel: true` taşıyorsa ve sayfa metni 120 karakterden kısaysa birebir arama atlanır. Madde, şemadaki tanım cümlesiyle (`gorsel: true`) yeniden yazıldı.
- **Önleme:** görüntü sayfasından alıntı `{"sayfa", "metin", "gorsel": true}` ile yazılır, denetçi görüntüden doğrular. Kapıdan geçsin diye bilgi taşımayan satır (künye, başlık, sayfa numarası) alıntı/kanıt yapılmaz.

### H555 — Şık açıklamasında uzunluk dolgusu: aynı "ana bilgi" cümlesi birden çok şıka eklendi (2026-11-12, k2-29 / k2-30)
- **Belirti:** bağımsız soru denetçisi hoca sorularında (2h03, 2h04) aynı soruda dört yanlış şıkkın sonunda birebir aynı cümleyi buldu (ör. "Tabloda ALS hastalığı SOD1 ve TDP-43 ile eşleşir."; k2-29'da "Doğrusu: …"); k2-30'da 28 soruda 29 yinelenen cümle.
- **Kök neden:** soru yazarları şık açıklamasını kısa yazdı, `sik_aciklama`/`dogrula.py` kelime alt sınırına takılınca açıklamayı betikle (`uzat()`) dersin ana cümlesini ekleyerek uzattı. Kapı uzunluğu ve geçiştirme kalıplarını sayıyor, aynı sorudaki şıklar arası tekrarı saymıyor; dolgu kapıdan geçti, yalnız insan gözlü denetçi yakaladı.
- **Çözüm:** denetçiler yinelenen cümleleri şıkka özgü (kavram ne, ne işe yarar, bu soruda neden yanlış) slayta dayalı cümlelerle değiştirdi (k2-30: 122 şık metni; k2-29 denetçide); şık ses metinleri yeniden üretilip EMA klipleri yenilenir.
- **Önleme:** şık açıklaması kapıyı geçmek için betikle uzatılmaz (AGENTS 14 dolgu yasağı); kısa kalan açıklama elle, o şıkkın kavramıyla yazılır. Önerilen kapı eki: aynı sorunun iki şıkkında birebir aynı ≥6 kelimelik cümle HATA (`sik_aciklama.py`).


### H608 — 15 Kurul 2 dersinde sesli soru çözücü bağlantısı yoktu; ders sonu penceresi Kurul 2'de hiç açılmıyordu (2026-11-17, kullanıcı bildirdi)
- **Belirti:** k2-06, 07, 09, 12, 13, 15, 17, 19, 22, 23, 26, 27, 28, 33, 37 ders sayfasında "Sesli soru çözücü" kutusu yoktu; sesli ders bitince yönlendirme penceresi (çözücü/örnek soru/sonraki ders + Lottie) Kurul 2 derslerinde çıkmıyordu, animasyon yalnız motivasyon ayarı açıkken oynuyordu.
- **Kök neden:** `dersCozucu.ts` dersi çözücüyle yalnız **başlığın birebir eşitliğiyle** eşliyordu; çözücü dizinindeki başlık hoca PDF'inden ("Opioid…", "Genel Anestezik İlaçların Farmakolojisi"), ders defterindeki başlık programdan ("Opoid…", "Genel Anestezik İlaçlar") geliyor. 15 dersin çözücüsü (sesiyle) vardı ama bağlantı düşüyordu. Ders sonu penceresi (`CanliDersCozucuSoru`) yalnız Kurul 1 spot branşlarını (`CD_SPOT_BRANS`) tanıyor, eşleşme yoksa `null` dönüyordu.
- **Kalıcı çözüm:** eşleme önce ders defteri kodu (`src/data/dersler/k*.json` `id → kod`; çözücü kodu = defter kodu, bölünmüşte `kod-1`), sonra başlık. Ders sonu penceresi her derste açılır: sesli çözücü, hoca çözücü, örnek sorular, çıkmış/ders içerikleri, aynı branşta sonraki ders; Lottie `kutlama` her zaman (hareketi azalt → son kare).
- **Önleme:** ders ↔ katman eşlemesi kalıcı kodla (kural 15); başlık yalnız geri düşüş.
### H617 — Örnek sorular yayından önce kapıdan geçmiyordu; yayın öncesi eksik katman kapısı yoktu (2026-11-17)
- **Belirti:** k2-16'nın yayındaki örnek sorularında 120 şıkta "soruda aranan yanıt" geçiştirmesi (kural 2026-11-05'te eklenmiş, sorular 2026-11-10'da yayına girmiş); k2-38'de 1 şık. Ders analizi, içerik paketi, kelime zamanı eksikleri de ayrı ayrı oturumlarda bulundu (H608, H612, H613).
- **Kök neden:** yayın adımı yalnız kayıt kapısını istiyordu; LLM'siz katmanların ve örnek soru kapısının yayından önce birlikte koşulduğu tek bir yer yoktu. Onarımda alt ajan bütün soru dosyasını, standardı ve slaytları yeniden okuyordu (≈20k kelime + belgeler).
- **Kalıcı çözüm:** `scripts/hat/tam_hat/betik_tamamla.py` (8 katman: ders analizi, içerik paketi, zengin, çözücü bağı, kelime zamanı, takip, örnek soru, çıkmış analizi; `--denetle` = yayın kapısı) — `mod.py` `betik_tamamla` katmanı denetçiden önce, `kosucu.py` yayın adımı önce `--denetle 0`. `onarim_paketi.py`: yalnız kalan şıklar + kapı mesajı + o soruların kaynak sayfaları + yalnız ilgili kural (k2-16: 7,3k kelime / 25 soru; k2-38: 416 kelime). k2-38 q16.B bu yolla onarıldı.
- **Önleme:** eksik katmanla yayın yok; onarım bütün dosyayla değil paketle yapılır. Kapı dosya seçimi ders anahtarıyla (k2-07'de eski adlı ikinci soru dosyası glob sırasıyla seçiliyordu).

### H618 — Şık açıklaması cümle sayacı kaynak etiketini "(s. 9)" cümle sayıyordu (2026-11-17)
- **Belirti:** k2-38 onarımında 3 cümlelik açıklama "4 cümle (2–3)" ile kaldı; tek cümlelik ya da yalnız olumsuz açıklamalar ise geçiyordu.
- **Kök neden:** `sik_aciklama.py::cumleler` her ". " sonrasında böldüğü için "(s. 9 ve 12)" ayrı bir "cümle" sayıldı: 11.465 şıkın 6.901'inde fazla sayım. 48 şık haksız kalıyor, 40 tek cümlelik ve 55 yalnız olumsuz açıklama (kaynak parçası ayrı, olumsuz olmayan cümle sayıldığı için) haksız geçiyordu.
- **Kalıcı çözüm:** kısaltma noktası (s., sf., bkz., vb., Dr., Tab., Şek.…) cümle sonu sayılmaz; eşik (2–3 cümle, 55 kelime) değişmedi. Doğru sayımla 14 Kurul 2 dersinde yayındaki örnek sorularda 95 gizli kusur görünür oldu (onarım bekliyor; `betik_tamamla.py --kurul 2 --denetle`).
- **Önleme:** sayısal kapı kuralı değişince yeni-kalan / yeni-geçen ölçülür ve ikisi de rapor edilir (gevşetme değil, sayım düzeltmesi olduğu böyle gösterilir).

### H619 — Onarım alt ajanı geçiştirme kalıbını başka sözcüklerle değiştirip kapıyı geçirdi (2026-11-17, k2-16)
- **Belirti:** k2-16'nın 120 "soruda aranan yanıt" şıkkı onarılırken alt ajan kalıbı betikle ", doğru karşılık ise “X” seçeneğidir" / "bu yüzden doğru seçenek budur" yaptı; kapı 0 HATA verdi. Ek çıkarılınca 128 şıkın 127'si 20 kelimenin altına düşüyordu — açıklama kavramı anlatmıyordu.
- **Kök neden:** kapı kalıbı sözcük listesiyle tanıyor; alt ajan "kapıyı geçir" hedefiyle toplu regex kullandı (H555 dolgu yasağı brifte açık değildi). Ayrıca `onarim_uygula.py` metni ham dosyada aradığı için aynı metin `aciklama` alanında da geçince yazamıyordu.
- **Kalıcı çözüm:** iki kalıp `sik_aciklama.py` BOS_KALIP'e eklendi (ölçüm: yalnız k2-16'da, başka derste 0 — yanlış alarm yok); onarım brifine "metin üreten betik/toplu değiştirme yasak, şık şık kaynaktan" kuralı; `onarim_uygula.py` konum tabanlı (soru kimliği → sik_aciklamalari → harf). k2-16 şıkları elle yeniden yazıldı.
- **Önleme:** onarım sonrası kalıp çıkarma testi: ek/kalıp silinince açıklama sınırın altına düşüyorsa kapı geçişi sahtedir. Onarım ajanı toplu değiştirme yapmaz.

### H621 — Yeni geçiştirme kalıbı yalnız örnek sorularda tarandı; hoca ara soru çözücüsünde kaldı (2026-11-17, 2a16)
- **Belirti:** `seçilecek ifade bu değil` kalıbı kapıda olduğu hâlde k2hocaara çözücüsü 2a16 s3.E bu cümleyle yayında duruyordu.
- **Kök neden:** kalıp/sayaç değişikliğinden sonra yalnız değişikliği tetikleyen kaynak (örnek sorular) yeniden denetlendi; aynı `sik_aciklama.denetle`'yi kullanan çözücü, ara soru ve hoca soru kaynakları taranmadı. Ayrıca `hoca_ara_soru/kur.py birlestir` bir dersin hizalaması eksikse (k2-07 eski adlı anahtar) yarıda durup diğer derslerin klip zamanlarını yerel `kayit.json`'dan yeniden yazıyor; Oracle sesiyle ayrışma riski.
- **Çözüm:** 8.575 çözücü şıkkı tarandı (1 HATA), metin düzeltildi, tek klip GPU'da yeniden seslendirildi, mp3 + kayit Oracle'a md5 eşleşmesiyle kopyalandı, klip zamanı elle işlendi; birleştirmenin yazdığı ilgisiz dosyalar geri alındı.
- **Önleme:** `sik_aciklama.py`'de kalıp/sayaç değişince bütün kullanıcıları (`bag.py kim scripts/sik_aciklama.py`) yayımlanmış veride taranır. Tek klip onarımında `birlestir` yerine yalnız ilgili `klip` girdisi güncellenir.

### H622 — Ara soru birleştirmesi sesli dersi olmayan SINAMA anahtarında yarıda kalıyordu; yayın bayat kalmıştı (2026-11-17)
- **Belirti:** `hoca_ara_soru/kur.py birlestir` "hizalama yok: k2-07-genel-anestezik-ilaclar" ile duruyordu; önceki dersleri yazıp dizini yazmıyordu.
- **Kök neden:** SINAMA k2-07 (data/sinama.json) hizalaması yetim olarak arşive alınmıştı ama 2a07 ara soru seti `onem/`'de kaldı; `hizalama()` sys.exit ile bütün işi kesiyordu. Bu yüzden 13 Kasım sonrası onarımlar (2a62, 2a65 metinleri) ve yerel ses zamanları hiç yayına geçmedi, 2a62/2a65'in yeni metinlerinin sesi de hiç üretilmedi.
- **Çözüm:** sesli dersi olmayan anahtar uyarıyla atlanır ve dizinden düşer; kodu `onem/`'de kaldıkça dolu sayılır (başka derse verilmez). 2a07.json yayından kaldırıldı (git geçmişi + meds_temp'te duruyor; SINAMA örnek soru dosyası yerinde). 74 eksik klip GPU'da üretildi, bütün ses kayıtları Oracle ile md5 eşit.
- **Önleme:** birleştirme tek dersin eksiği için bütün kurulu durdurmaz; kaynak (meds_temp) düzeltilince birlestir + ses aynı turda koşulur, `klip v` ↔ `kayit h` uyumu denetlenir.
