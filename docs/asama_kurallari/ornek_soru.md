# Aşama kuralları — ornek_soru

> ÜRETİLMİŞ DOSYA: elle yazma. Kaynak `docs/KURUL2_YAPILMAYACAK_HATALAR.md`, üreteç `scripts/hat/tam_hat/kural_secici.py`. 32 madde. Tek satırlı maddeleri betik denetler (tam metin: `kural_secici.py --tam <H no|aşama>`).

- H1 — Geçiştirici şık açıklaması (2026-10-18) — betik denetler: `meds/scripts/sik_aciklama.py`
### H7 — Düzeltme tek kopyada kalıyor (çözücüde düzeltilen soru spot/asistan/örnekte eski)
- **Kural:** soru kimliği tek; denetçi düzeltmesi tüm kopyalara yayılır.
- **Kapı — EKLENDİ:** `ders_zinciri.kopya_tutarliligi` (birleştirme sonrası): aynı kökteki soru önem listesi (çıkmış +
  örnek) ile çözücüde farklı doğru şık METNİYLE duramaz (harf farkı serbest: şık sırası değişebilir) → kod 13. K1'in 6
  branşında 0 yanlış pozitif; sahte uyuşmazlık yakalandı.


### H21 — Soru çözücü sonradan genişleyince Son Prova soru kimlikleri kaydı (Kadın Doğum, 2026-10-21)
- **Düzeltme:** `dogrula.py` denetimde yeniden yazılmış soruyu (`duzelt/eslem.json` → yayındaki `t0N#…`) geçerli sayar; yalnız
  numarası kayan `k01-2#32` → `k01-1#32`. 14 part 0 HATA, yayındaki tüm kimlikler karşılıklı.

### [2026-10-21] Çıkmış soruda iç uyarı metni ve kalıp şık açıklaması (h06/19 Refik Saydam)
- **Hata:** Çözücüdeki çıkmış sorunun kökünde "[Dikkat — olası hatalı kayıt …]" iç notu kalmıştı; öğrenciye gösterildi ve EMA ile
  okundu. Aynı sorunun şık açıklamaları "bu soruda aranan özellik değildir ve elenir" kalıbıydı, ipucu konu dışıydı.

### H28 — Doğrulayıcı tıbbi "kaynaklı"yı süreç dili sanıyordu; önem ↔ çözücü şık uzunluğu uyumsuzdu (2026-10-23)


### H29 — "Burası önemli" kuralları birbiriyle çelişiyordu; OCR'lı sayıda sıfır kayıp yanlış alarmı (2026-10-23)


### H31 — Hesap sorusu yanlış alarmı + iç etiketin öğrenci metnine sızması (2026-10-23 K2 provası)


### H32 — Zorluk parça içinde yuvarlanınca ders toplamı hedefin altında kalıyordu (2026-10-23 K2 provası)


- H62 — Quiz Üretiminde Öncelik Sırasının İhlali, Çifte Analiz Maliyeti ve Yarış Durumu Hatası (2026-10-26) — betik denetler: `meds/scripts/hat/quiz_motoru/quiz_dogrula.py`
### H86 — Ders işçisi denetimi örnek soru şık açıklamalarını standart kapıdan geçirmiyordu (2026-10-27, k2-03)
- **Önleme kuralı:** örnek soru çeldiricisi de müfredattan (öğretilmiş komşu kavram) seçilir (AGENTS kural 4, 9).


### H119 · Örnek sorularda öznel/ders çağrıştıran kök ve rastgele slayt sorusu (2026-10-27)
- **Kural:** Kök bağımsız ve çıkmış-benzeri kalıpta; ders/slayt/bölüm göndermesi yok; her soru kazanım–konu bağlı, tıbbi ve sınav değerli. Kaynak: `TALIMAT.md` §4, `TALIMAT_ONEM.md`, `KURUL2_DERS_STANDARDI.md` §10.9.



### H120 · Dallanmalı soruda doğru/yanlış bayrağı ters işaretliydi (2026-10-27, k2-01)
- **Kalıcı çözüm:** doğrulayıcıya `klinik-karar-bayrak` HATA kapısı (geri bildirim "Doğru/Yanlış" ile başlıyor ve bayrakla çelişiyorsa). Önleme: bayrak ve geri bildirim tek yerden üretilir; denetçi kapı dışı tutarlılık taraması yapar; doğru şık hep ilk sırada olmaz.


### H435 — Örnek sorular hocanın yeni sınav kalıbını yansıtmıyordu (2026-10-29, kullanıcı bildirdi)
- **Kural / Önleme:** Patoloji örnek soru ve önem noktası `docs/PATOLOJI_HOCA_SORU_MANTIGI.md` + `scripts/uretim/patoloji_soru_isci/` kapısına göre yazılır: her önem noktasına ≥2 farklı kalıpta soru, çeldirici yalnız aynı dersin komşu kavramları, doğru şık en uzun olmaz. Sarı dolgu ve başlık önem sinyali sayılmaz; kırmızı tek başına "önemli" değildir (slaytların ~%42'si kırmızı).
- **Kapı:** `python3 scripts/uretim/patoloji_soru_isci/dogrula.py sorular.json paket.json` → 0 HATA.


### H436 — Ara soru şık açıklamalarında ileriye sızıntı ve kaynakta olmayan iddia (2026-10-29, bağımsız denetçi buldu)
- **Kural / önleme:** Şık açıklaması, ipucu ve çözüm de yalnız `ara.sayfa` ve öncesindeki slaytların bilgisini kullanır; tıbbi tanım slayt metninde yoksa yazılmaz. Bağımsız denetçi (TALIMAT adım 7) her soruda bunu slayt slayt arar; düzeltilen sorular ikinci kez denetlenir. Ders akış metni (Whisper dökümünden beslenmiş olabilir) tıbbi kaynak değildir; terim/sayı yalnız PDF sayfa metninden alınır.


### H490 — Öğrenci önem kapısı geçilemez yanlış HATA veriyordu (k2-15, k2-16, k2-11; 2026-11-05)
- **Kural:** kapı HATA'sı "eşleyici kaçırıyor" diye bırakılmaz: ya anlatım düzeltilir ya kapının kendisinin denetlediği kanıtlı eşleme yazılır.


### H511 — Şık açıklamalarına betikle yeni geçiştirme kalıpları eklendi, kapı yakalamadı (2026-11-06)
- **Önleme:** Şık açıklamasına betikle sabit cümle eklemek YASAK; kısa açıklama elle, şıkka özgü gerekçeyle uzatılır. Denetçi aynı cümlenin ≥3 şıkta geçmesini bulgu sayar.


### H541 — Destesiz derslerin örnek soruları k2-12'den beri siteye yayınlanmıyordu (2026-11-10)
- **Önleme:** destesiz yayın betiğine s16 adımı eklenir; `ders_icerik_dogrula.py` sitede örnek soru dosyası yoksa HATA versin (yapılacak).


### H549 — Önem maddesinin alıntısı olarak slayttaki kaynak künyesi yazıldı (2026-11-10, k2-28 2t02-23)
- **Önleme:** görüntü sayfasından alıntı `{"sayfa", "metin", "gorsel": true}` ile yazılır, denetçi görüntüden doğrular. Kapıdan geçsin diye bilgi taşımayan satır (künye, başlık, sayfa numarası) alıntı/kanıt yapılmaz.


### H555 — Şık açıklamasında uzunluk dolgusu: aynı "ana bilgi" cümlesi birden çok şıka eklendi (2026-11-12, k2-29 / k2-30)
- **Önleme:** şık açıklaması kapıyı geçmek için betikle uzatılmaz (AGENTS 14 dolgu yasağı); kısa kalan açıklama elle, o şıkkın kavramıyla yazılır. Önerilen kapı eki: aynı sorunun iki şıkkında birebir aynı ≥6 kelimelik cümle HATA (`sik_aciklama.py`).



### H608 — 15 Kurul 2 dersinde sesli soru çözücü bağlantısı yoktu; ders sonu penceresi Kurul 2'de hiç açılmıyordu (2026-11-17, kullanıcı bildirdi)
- **Önleme:** ders ↔ katman eşlemesi kalıcı kodla (kural 15); başlık yalnız geri düşüş.

### H617 — Örnek sorular yayından önce kapıdan geçmiyordu; yayın öncesi eksik katman kapısı yoktu (2026-11-17)
- **Önleme:** eksik katmanla yayın yok; onarım bütün dosyayla değil paketle yapılır. Kapı dosya seçimi ders anahtarıyla (k2-07'de eski adlı ikinci soru dosyası glob sırasıyla seçiliyordu).


### H618 — Şık açıklaması cümle sayacı kaynak etiketini "(s. 9)" cümle sayıyordu (2026-11-17)
- **Önleme:** sayısal kapı kuralı değişince yeni-kalan / yeni-geçen ölçülür ve ikisi de rapor edilir (gevşetme değil, sayım düzeltmesi olduğu böyle gösterilir).


### H619 — Onarım alt ajanı geçiştirme kalıbını başka sözcüklerle değiştirip kapıyı geçirdi (2026-11-17, k2-16)
- **Önleme:** onarım sonrası kalıp çıkarma testi: ek/kalıp silinince açıklama sınırın altına düşüyorsa kapı geçişi sahtedir. Onarım ajanı toplu değiştirme yapmaz.


### H621 — Yeni geçiştirme kalıbı yalnız örnek sorularda tarandı; hoca ara soru çözücüsünde kaldı (2026-11-17, 2a16)
- **Önleme:** `sik_aciklama.py`'de kalıp/sayaç değişince bütün kullanıcıları (`bag.py kim scripts/sik_aciklama.py`) yayımlanmış veride taranır. Tek klip onarımında `birlestir` yerine yalnız ilgili `klip` girdisi güncellenir.


### H622 — Ara soru birleştirmesi sesli dersi olmayan SINAMA anahtarında yarıda kalıyordu; yayın bayat kalmıştı (2026-11-17)
- **Önleme:** birleştirme tek dersin eksiği için bütün kurulu durdurmaz; kaynak (meds_temp) düzeltilince birlestir + ses aynı turda koşulur, `klip v` ↔ `kayit h` uyumu denetlenir.


### H625 — Ara soruda şık metni çözücü dosyasında kaymış, kapı 0 HATA verdi (2026-11-18, k2-49)
- **Kural:** Ara soru düzeltmesi `kaynak/`, `cozucu/`, `onem/` üçünde aynı anda yapılır; bağımsız denetçi turu atlanmaz; kapı komutunda tam ders anahtarı kullanılır.


### H626 — Çıkmış soru kökü 90 kelimeyi aşınca çözücü kapısı kaldı; çıkmış kök kısaltılamaz (2026-11-18, k2-39)
- **Kural:** Çıkmış kökü asla kısaltılmaz ya da gerekçe uydurularak elenmez; sınırı aşıyorsa kapı çıkmış için ayrı sınırı kullanır. Çözücü ayrı bir yazım turu olarak planlanır, açıklama alt sınırı 18 kelimedir.



### H646 — Ders özeti kapısının "en çok %20 çıkmış atlanabilir" sınırı yazarları sahte kapsama itti; Yunan harfi ses kapısını düşürdü (2026-11-23, Ders özeti)
- **Kural:** Kapı eşiği, kaynakta olmayan bilgiyi zorla "kapsatmaya" iten biçimde konmaz; kapsam oranı uyarıdır, doğruluk denetçidedir.
  Seslendirilen metinde Yunan harfi ve iki noktalı oran yazılmaz.

### H650 — Branş birleştiricileri: tam birleştirme başka dersleri yeniden yazıyor; ara soru birleştirmesinde onay listesi yok (2026-11-23)
- **Kural:** Spot birleştirici HER ZAMAN `--kod`. Ara soru birleştirmesi sonrası `git status src/data/k<N>hocaara_cozucu/` ile yalnız onaylı kodların girdiği doğrulanır; denetlenmemiş set varken commit yapılmaz. Kalıcı çözüm (2026-11-24): `kur.py birlestir` artık `k<N>hocaara/onayli.json` listesindeki kodları birleştirir (yayındaki 59 setle başlatıldı); TALIMAT 8. adım güncellendi.


### H651 — Alt ajan çözücü kodunu defterden almadı, uydurdu (k2-56: 2s56 ≠ defter 2s19) (2026-11-23)
- **Kural:** Brif çözücü/önem kodunu AÇIKÇA verir (defterden). Çözücü yayınından önce `betik_tamamla.py <ders>` `cozucu_bag` satırı ✓ olmalı.

### H655 · Sesli ders ve örnek soruda metin takibi yanlış yeri gösteriyor / geç kalıyor (2026-11-24)
- **Önleme:** Anlatım ↔ slayt/metin eşlemesinde birebir metin beklenmez; sözcük eşleşmesi tek ölçüt olamaz (anlam + sıra). Seste olmayan metin için zaman uydurulmaz: metni değişen ses varyantı ya yeniden seslendirilir ya da sunulmaz.

### H670 — Çözücü ilerleme şeridi: 215 ayrı düğme, telefonda dokunulamıyor ve sağ yarısı kırpılıyordu (2026-11-25)
- **Kural:** soru sayısıyla çoğalan öge tek tek etkileşimli yapılmaz; 200+ öğede 375 px'te son öğenin `right` değeri kapsayıcıyla karşılaştırılır.


