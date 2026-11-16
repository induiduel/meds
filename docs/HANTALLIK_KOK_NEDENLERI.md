# Hantallık, yavaşlık ve yanlış üretim — kök neden defteri

> Kayıt: 2026-11-16 · Kullanıcı bildirimi: "tam içerik oluşturucusu gibi oluşturucular ya da projenin kendisi çok hantal oldu;
> eskiden rahat yapılan işler artık çok limit harcıyor, yanlış yapılıyor ya da çok uzun sürüyor."
> Bu belge **suçlu aramaz**; ölçülen nedenleri, kanıtlarını ve önerilen kalıcı çözümleri toplar. Her madde bağımsız
> uygulanabilir. Yeni bir hantallık nedeni görüldüğünde buraya madde eklenir (silinmez).

Ölçüm tarihi: 2026-11-16. Ölçümler bu makinede (`/home/indu/medsor`) alındı; komutlar madde sonlarında verilir, tekrar
doğrulanabilir.

---

## 0. Tek sayfalık özet (en çok kanıtlanan 10 neden)

| # | Neden | En çarpıcı kanıt | Sonuç |
|---|---|---|---|
| 1 | **Talimat belgesi enflasyonu** | Oturum açılışında zorunlu 7 belge ≈ **205.000 kelime (~308k token)**; `DEGISIKLIK_KAYDI.md` tek başına 1,23 MB / 141k kelime | Ajan bağlamının büyük kısmı talimat okumaya gidiyor; asıl işe az yer kalıyor, talimatın bir kısmı hiç okunmuyor |
| 2 | **Aynı kural 4–6 yerde, farklı sürümde** | "Tasarruf kipi" AGENTS+hızlı akış+el kitabı+mod.py; Hoca tahmin rehberi AGENTS'te v5, hızlı akışta v6 | Ajan hangi sürümün geçerli olduğunu bilemiyor; yanlış sürümle üretim → yeniden üretim |
| 3 | **Tek doğruluk kaynağı yok: 4 ayrı "hat" listesi** | `hat.json` 33 aşama · `mod.py` 22 katman · `ders_zinciri.py` 11 adım · el kitabı §19 11 adım | Her oturum listeyi kafasında birleştiriyor; katman atlanıyor ya da iki kez yapılıyor |
| 4 | **E1–E6 adımlarının koşucusu yok** | `scripts/hat/tam_hat/` yalnız E0'ı (`hazirlik.py`) çalıştırıyor; sonrası insan sırası | Her ders "elle sıralanan 15–20 komut + alt ajan" demek; otomasyon hissi kayboldu |
| 5 | **Veri 3–4 köke dağılmış, tek ders 34–36 dosya** | `src/data`, `data`, `meds_database_v2`, `public`; k2-62 izi 36 dosya / 35 klasör | Bulma, senkron, dağıtım ve doğrulama maliyeti katlanıyor |
| 6 | **Kapı sayısı çok, kapsamı dağınık** | 34 `*dogrula*` + 9 `*kapi*` + 8 `*validate*` = **51**; 18'i aynı adı taşıyor; `cozucu_dogrula{1,2,3}` kopya | Hangi kapı neyi denetliyor belirsiz; yanlış pozitif ve sessiz atlama üretiyor |
| 7 | **Yeniden yazım kültürü** | Hata defterinde 53/241 madde "kapı gevşek/atlandı", 27/241 "baştan üretim gerekti", 332 kez "düzeltildi/yeniden yaz" | Tek hata tüm katmanı yeniden üretiyor → hem süre hem limit |
| 8 | **Oturum çakışması** | Günlükte **151** kez "başka/diğer oturum, çakışma"; 69 kez "commit/dağıtım yapılmadı" | Aynı ders iki oturumda işlendi (6. parti); biri diğerinin çıktısını ezdi |
| 9 | **Derleme/dağıtım çöpü birikiyor** | `dist` **950 MB**, `dist/assets` 16.150 dosya (%82'si eski derleme), 3×32 MB aynı kazanım parçası, 86 `chunk-glossary` kopyası | Vite build 33–35 sn + disk/rsync/yedek şişmesi; soğuk açılış ve dağıtım yavaş |
| 10 | **Ölçüm yok** | Aşama süresi, LLM çağrı sayısı, kapı HATA sayısı tek yerde toplanmıyor (yalnız E0 `hazirlik_durum.json`) | "Hantal" hissi kanıtlanamıyor, iyileştirme ölçülemiyor |

Aşağıda her neden ayrıntılı: **belirti → kanıt → kök mekanizma → kalıcı çözüm → önleme kuralı**.

---

## 1. Talimat ve doküman enflasyonu

**Belirti.** Yeni bir oturum işe başlamadan önce yüz binlerce kelime "zorunlu okuma" ile karşılaşıyor. Ajan ya hepsini
okuyup bağlamını tüketiyor ya da bir kısmını atlıyor ve kural hatası yapıyor. İkisi de maliyetli.

**Kanıt (ölçüldü).**

| Dosya | Kelime | ~Token |
|---|---|---|
| `AGENTS.md` (kök, 31 kural) | 5.335 | ~8.000 |
| `meds/AGENTS.md` | 279 | ~418 |
| `meds/CLAUDE.md` | 1.517 | ~2.275 |
| `PROJE_TANITIMI.md` | 1.319 | ~1.978 |
| `DEGISIKLIK_KAYDI.md` | **141.097** (536 bölüm, en büyüğü 7.979 kelime) | ~211.645 |
| `docs/KURUL2_YAPILMAYACAK_HATALAR.md` | **49.645** (241 madde, madde başına ~204 kelime) | ~74.467 |
| `docs/KURUL_OTOMASYON_EL_KITABI.md` | 6.323 | ~9.484 |
| **Toplam** | **205.515** | **~308.000** |

- `meds/docs/` altında 46 markdown; `scripts`+`otomasyon` altında 26 `TALIMAT*.md`.
- Aşama özetleri (`docs/asama_kurallari/`) da büyük: `anlatim.md` 11.5k kelime, `ornek_soru.md` 13.2k kelime.
  Bir alt ajanın istemine giren okuma listesi aşama başına **14.600–19.700 kelime (~22k–30k token)**; 9 aşamanın toplamı
  **139.308 kelime**.
- Aynı madde birden çok aşama özetinde: 275 benzersiz madde için **1.111 madde–aşama eşleşmesi** (H493 ve H494 on ayrı
  aşamada). `genel.md` (1.772 kelime) her aşamada yeniden okunuyor.
- Hata defterinin kendi yapısı bozulmuş: 241 madde başlığı var ama **207 benzersiz numara** → 17 numara çakışması
  (H86, H87, H102, H104–H110, H127, H131, H431, H435, H436, H491 iki farklı hat için kullanılmış), 13 madde başlıksız,
  1–496 aralığında 289 numara hiç kullanılmamış. Bu, atıf yapılan "H516" gibi maddelerin izini sürmeyi zorlaştırıyor.

**Kök mekanizma.** Kural yazma maliyeti sıfıra yakın olduğu için her oturum yeni kural/belge ekledi; hiçbir kural
emekliye ayrılmadı, hiçbir belge "tek kaynak" ilan edilip diğerleri kısaltılmadı. Belge sayısı zamanla **doğrusal** büyürken
okuma yükü **her oturumda baştan** ödeniyor.

**Kalıcı çözüm.**

1. **Tek "işletim kuralı" belgesi** (ör. `docs/KURALLAR.md` *(önerildi, yazılmadı — bugünkü yakın karşılığı `docs/KURALLAR_OGREN_QUIZ.md` + `docs/KURALLAR_ICERIK_HATTI.md`)*, ≤1.200 kelime): yalnız işi durduran kurallar, numaralı,
   her biri tek cümle + tek örnek. Diğer belgeler buna **referans** verir, kopyalamaz.
2. `DEGISIKLIK_KAYDI.md` arşive ayrılır: son 3 oturum kalır, gerisi `docs/arsiv/DEGISIKLIK_KAYDI_<yıl>.md`. Günlük
   tutarı **≤150 kelime/oturum** olur (şablon: istek / yapılan / kapı sonucu / açık).
3. Hata defteri **makine okunur** hâle gelir: madde başlığı `## H<n> — <başlık>` şablonu kapıya bağlanır
   (`kural_secici.py --denetle` numara çakışmasını, başlıksız maddeyi, eksik kapıyı HATA saysın).
4. Bir madde **kapıya bağlandıysa** defterdeki uzun anlatı `docs/arsiv/` altına iner; defterde yalnız
   `H<n> | belirti (1 cümle) | kapı komutu` kalır.

**Önleme kuralı.** Yeni kural yalnız (a) tek bir kapıya bağlanıyorsa ve (b) mevcut bir kuralı **değiştiriyorsa** yazılır;
değiştirdiği kural aynı düzenlemede **silinir**. "Ek olarak şunu da unutma" biçiminde kural eklenmez.

---

## 2. Aynı bilginin çok yerde, farklı sürümde tutulması

**Belirti.** Ajan bir konuda iki farklı sayı/ölçüt görüyor ve yanlış olanı seçiyor; sonra denetçi "sapma" diyor, iş
yeniden yazılıyor.

**Kanıt.**
- Hoca tahmin rehberi sürümü: `AGENTS.md` "v5" diyor, `TAM_HAT_HIZLI_AKIS.md` "v6" diyor. Aynı belgede başarı oranı
  AGENTS'te **%62,5–69**, hızlı akışta **%75–80**.
- Aşama başlıklandırması bozuk: `TAM_HAT_HIZLI_AKIS.md` içinde iki tane "## 6" var (PDF tasarım taraması ve Hoca
  profili adımı), ayrıca "## 7" ve ardından "## 6" tekrar.
- Aynı kural birden çok yerde kopya: "bağımsız denetçi" AGENTS'te 7, el kitabında 6; "EMA" AGENTS'te 9, el kitabında 15,
  hızlı akışta 5 kez geçiyor. Metinler birebir aynı değil.
- `kural_secici.py --denetle` şu anda **HATA veriyor**: 10 aşama özeti defterden eski (defter 2026-11-15, özetler
  2026-11-10). Yani "aşama başına güncel kural" mekanizması bir haftadır bayat veriyle çalışıyor.
- Katman durumu üç yerde ayrı yazılı: `mod.py` (22 katman), `AGENTS.md` kural 22, `TAM_HAT_HIZLI_AKIS.md` §0. Öğren destesi
  ve quiz her üçünde de "kapalı" ama kural 22 hâlâ "tüm katmanlar" listesinde sayıyor.

**Kök mekanizma.** Bilgi tek kaynakta tutulmuyor; "özet" belgeleri elle senkronlanıyor ve senkron denetimi (hat başında
`--denetle`) **bloklayıcı değil** (uyarı gibi geçiliyor).

**Kalıcı çözüm.**
1. Her ölçüt/sürüm **tek dosyada** (ör. `docs/standartlar.json` *(önerildi, yazılmadı)*: sürüm, eşik, oran). Belgeler bu dosyayı **okur**;
   metne sayı yazmak yasak.
2. `--denetle` hat başında **zorunlu adım** olur (0 değilse hat başlamaz).
3. Katman listesi tek kaynak: `mod.py`. `AGENTS.md` ve el kitabı yalnız "katmanlar `mod.py`'de" der, liste tekrarlamaz.

**Önleme kuralı.** Aynı bilgi ikinci kez yazılacaksa yazılmaz — bağlantı verilir. İkinci kez yazılmış bilgi bulunduğunda
kapı HATA verir.

---

## 3. Hat tanımının dört ayrı yerde olması ve koşucusunun bulunmaması

**Belirti.** "Tam içerik işçisini başlat" dendiğinde ajan önce hangi adımların zorunlu olduğunu belirlemeye çalışıyor;
bazen 11, bazen 14, bazen 20 katman çalıştırıyor. Aynı dersin iki oturumda farklı katman kümesiyle bitmesi buradan.

**Kanıt.**

| Kaynak | Adım sayısı | Kapsam |
|---|---|---|
| `otomasyon/hat.json` | 33 aşama | tüm sistem (sağlık, db göçü, kamp, checkup…) |
| `scripts/hat/tam_hat/mod.py` | 22 katman | ders hattı |
| `otomasyon/ders_zinciri.py` `ADIMLAR` | 11 | hazirla…terim |
| `docs/KURUL_OTOMASYON_EL_KITABI.md` §19 | 11 | adım 1–11 |

- `scripts/hat/tam_hat/` içinde **yalnız E0** var (`hazirlik.py`); E1–E6 için betik yok, sıralama el kitabında düz metin.
  Alt ajan istemleri de elle kuruluyor (`kural_secici.py --oku <aşama>` yalnız okuma listesi veriyor, görevi vermiyor).
- `hat.json`'daki 33 aşamanın 15'inin komutu **çalıştırılabilir değil** (dosya yolu yok ya da `ders_zinciri.py` gibi genel
  betiğe işaret ediyor). Yani defter "makine okunur" değil, "insan okur".
- `mod.py`'de "tam" kipinde bile `ogren_deste` ve `quiz` **False**; buna karşılık kullanıcı kararı metinleri 4 ayrı yerde
  tekrarlandığı için ajan bazen yine üretmeye çalışıyor (günlükte bu yönde uyarılar var).

**Kök mekanizma.** Her yeni katman (çapa, ara resim, ara soru, hoca soruları, ek modül, çıkmış analizi…) **kendi
belgesini ve kendi betiğini** getirdi, ama **tek bir koşucuya** bağlanmadı. Otomasyon yerine "talimat + elle komut"
tercih edildi (kural 20 gereği doğru), fakat bu kez sıralama bilgisi insana/ajana kaldı.

**Kalıcı çözüm.**
1. Tek koşucu: `python3 scripts/hat/tam_hat/hat.py <ders> --asama <aşama>|--sonraki|--durum` *(önerildi, yazılmadı — 2026-11-16)* — bugünkü karşılığı `scripts/hat/tam_hat/kosucu.py`. Her aşama `mod.py`'den okunur,
   her aşamanın **girişi/çıktısı/kapısı** JSON'da tanımlıdır (`hat.json` tek kaynak olur, `mod.py` ona delege eder).
2. Aşama atlanamaz: koşucu "önceki aşamanın kapısı 0 HATA mı" diye bakar; atlanan aşama `atlandi.json`'a **gerekçeyle**
   yazılır (tasarruf/askı), sessiz atlama imkânsız olur.
3. Alt ajan istemi de koşucudan gelir (görev + okuma listesi + çıktı şeması), elle kopyalanmaz.

**Önleme kuralı.** Yeni bir içerik katmanı, `hat.json`'a aşama olarak eklenmeden ve bir kapıya bağlanmadan "tamamlandı"
sayılmaz.

---

## 4. Verinin 3–4 köke dağılması, ders başına onlarca dosya

**Belirti.** Bir dersin verisi 20+ klasöre dağılıyor; güncelleme yapınca hangi dosyaların yenilendiği bilinmiyor, eski
sürüm bir köşede kalıyor, dağıtımda unutuluyor.

**Kanıt.**
- Kökler: `meds/src/data` (573 MB, 76 alt klasör), `meds/data` (**17 GB**, 124 klasör), `../meds_database_v2` (744 MB),
  `meds/public` (87 MB). Ayrıca `../meds_database` 1,1 GB, `../meds_temp` **15 GB**.
- Aynı isimli klasörler iki kökte: `data/*_cozucu` (3,5 GB ses) ile `src/data/*_cozucu` (12 MB açıklama) yan yana;
  `data/ogrenci_onem` ile `src/data/ogrenci_onem`; `pastQuestions.json` hem `data/` hem `src/data/` (ikisi de git dışı).
- Bir dersin izi (k2-62): **36 dosya / 35 klasör** — `src/data/{ogrenci_onem,ders_icerik,ders_analizi,ara_resim}`,
  `data/sesli_anlatim/{vurgu,v2,terim,metin,klip_zaman,kisaltma,kisaltma_elle,kelime_zaman,isaret,hizalama,gunluk,cizim,
  cikmis_konum,capa,.pdf_onbellek}`, `data/ogrenci_onem/analiz`, `public/ara_resim`, `meds_database_v2/ders_bilgi/…`.
- Branşa özel klasörler elle çoğaltılmış: `src/data/*_onem` (17 branş, 163 json) ve `*_cozucu` (196 json) — yeni branş
  = elle klasör açma + `MODUL_ANAHTARLAR`'a ekleme (H538'de bu yüzden 5 dersin okunuşu eksik kaldı).
- `src/data/decks/items` (83 MB) derlemede üretiliyor, git dışı; ama `meds_export/deste_paketleri` (126 MB) ayrı
  türetilmiş kopya. Tek kaynak ilkesi kâğıtta var (kural 5), fiilen 3 türev var.

**Kök mekanizma.** Her katman kendi çıktısını "en uygun" köke yazdı (ses büyük diye `data/`, site verisi diye `src/data/`,
kaynak diye `meds_database_v2/`). Bir dersin tüm katmanlarını **tek bir manifest** altında toplayan bir yapı hiç kurulmadı.

**Kalıcı çözüm.**
1. Ders başına **tek manifest**: `ders_bilgi/<key>/manifest.json` → her katmanın yolu, sürümü, karması, kapı sonucu,
   ses klip sayısı. Koşucu ve dağıtım yalnız manifesti okur. Eksik katman manifestte görünür.
2. Branş klasörleri **veriden** üretilir (`branslar.json`), elle klasör açılmaz; okunuş anahtarları da oradan türer.
3. `data/` yalnız **ikili/ses** için, `src/data/` yalnız **siteye giden** veri için kalır; kural `.gitignore` ve
   koşucuda denetlenir (aynı ad iki kökte varsa HATA).
4. `pastQuestions.json` ikinci kopyası kaldırılır (ENVANTER E5 bunu 2026-10-11'de zaten işaretlemiş; hâlâ duruyor).

**Önleme kuralı.** Yeni bir katman çıktısı, manifeste yazılmadan "üretildi" sayılmaz; manifestte olmayan dosya dağıtıma
girmez.

---

## 5. Kapı mimarisi: çok sayıda, kopya ve dağınık doğrulayıcı

**Belirti.** İş bittikten sonra "hangi kapıları koşayım" sorusu var. Bazı kapılar yanlış HATA veriyor, bazıları hiçbir şeyi
denetlemiyor ama "0 HATA" diyor. Ajan kapıyı gevşetmekle suçlanıyor; gevşetme de bir süre sonra gerçekten oluyor.

**Kanıt.**
- **51** doğrulayıcı: 34 `*dogrula*.py`, 9 `*kapi*.py`, 8 `*validate*.py`. 18'i aynı adı taşıyor
  (`dogrula.py` 13 kez, `cozucu_dogrula.py` 3 ayrı klasörde).
- `scripts/uretim/patoloji_cozucu/cozucu_dogrula.py`, `cozucu_dogrula2.py`, `cozucu_dogrula3.py`: ilk 12 satırı neredeyse birebir
  aynı (aynı `CUMLE_SINIRI`, `YASAK_SES`, `KISALTMA`, `KARISIK`, `IC_DIL` regex'leri); içlerinde sabit
  `W = "/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu"` yolu var.
- Hata defterinin kendi sınıflaması: 241 maddenin **53'ü** "kapı gevşetildi/atlandı/denetlenmiyor", **6'sı** "kapı yanlış
  HATA verdi / geçilemez", **13'ü** "sessizce boş geçti". Yani kapılar hem çok sıkı hem çok gevşek, ikisi bir arada.
- Tek bir "tüm kapılar" koşucusu yok: `package.json`'da `lint` ve `decks:packages` var, ders kapıları için komut yok;
  sıralama el kitabında düz metin.
- Hat dışı bir betik hatta karışabiliyor: `scripts/hat/tam_hat/ornek_soru_kaynak.py` hattın zorunlu kapısı değil, ama
  çalıştırıldığında çok sayıda yanlış alarm üretti (2026-11-10 kaydı), oturumun bir kısmı buna gitti.
- Ölçüm: `ders_icerik_dogrula.py k2-62` → 0,02 sn "paket yok" (yol yanlışsa sessizce hızlı HATA; doğru çalıştığında
  aynı kapı manifest/JSON'ları yeniden okuyor).

**Kök mekanizma.** Her yeni içerik türü, kendi doğrulayıcısını **kopyalayarak** doğurdu (ortak kütüphane
`scripts/turkce_uslup.py` ve `scripts/sik_aciklama.py` var, 124 betik bunları kullanıyor — doğru yön; ama soru/çözücü/
çizim kapıları kopyalanmış). Üstüne "kapı gevşetme yasağı" kuralı geldi, kapıların **kendisi test edilmediği** için
yanlış pozitif ile gerçek HATA ayırt edilemiyor.

**Kalıcı çözüm.**
1. **Tek kapı matrisi**: `scripts/kapilar/matris.json` → `{katman: [kapı, girdi, çıkış_eşiği]}` ve tek koşucu
   `python3 scripts/kapilar/kos.py <ders> [--katman …]`. Çıktı: tek tablo (katman, kapı, sonuç, süre, HATA sayısı).
2. Ortak denetim kütüphanesi genişletilir: `scripts/ortak_denetim/` *(önerildi, yazılmadı — 2026-11-16)* (cümle sınırı, yasak ses, iç dil, kısaltma, şık
   açıklaması, Türkçe üslup). Kopya doğrulayıcılar tek satırlık sarmalayıcıya iner.
3. Her kapının **kendi sınaması** olur (`scripts/kapilar/sinama/<kapı>.json`: bilinen iyi + bilinen kötü örnek).
   Yanlış pozitif ancak bu sınama ile düzeltilir; kapı gevşetmek yerine sınama eklenir.
4. Kapıların hepsi **tek girdi biçimi** kullanır (`--json` + manifest), büyük dosyaları her seferinde yeniden ayrıştırmaz.

**Önleme kuralı.** Yeni kapı, ancak ortak kütüphaneye eklenen bir denetim + kendi sınaması + matris kaydı ile yazılır.
Mevcut bir kapıyı kopyalayarak yeni dosya açmak yasak.

---

## 6. "Yeniden yazma" refleksi (en pahalı kalem)

**Belirti.** Kullanıcı bir eksiği söylüyor; ajan tüm katmanı (ya da tüm dersin sesini) yeniden üretiyor. Hem limit
gidiyor hem yeni hatalar giriyor hem de süre 40–60 dk ses + yüzlerce klip oluyor.

**Kanıt.**
- `DEGISIKLIK_KAYDI.md` içinde **332** kez "düzeltildi / yeniden yaz / yeniden üret" geçiyor; 27/241 hata maddesi
  "baştan üretim gerekti" diye kayıtlı.
- Somut örnek: 6. partide dört ders önce hoca sesi olmadan üretildi, hoca kaydı gelince **kısmi revizyon** yapıldı ama
  yine de örnek sorular, önem/çözücü, sesler ve dağıtım yeniden koştu (k2-22/23/24/58 — dört ders, iki oturum).
- Ek modülde (Yürüyüş ve Kampçılık) hoca materyali sorulmadan 16 konu yazıldı; materyal gelince **16 konu baştan yazıldı**
  ve ilk taslak `eski/` altına atıldı (H544, ~531 klip yeniden seslendirildi).
- Ölçek: `data/patoloji_cozucu/ses` **16.001** mp3, `data/ogren_ses` **12.083** mp3, `data/sesli_anlatim` 3,4 GB.
  Metnin bir paragrafı değişince yalnız o klip üretilse bile cümle/kelime zamanı, PDF işareti, çapa, ara soru ve çizim
  bağımlılıkları **elle** yeniden koşuyor.
- LLM önbelleği yalnız **aynı `is_id`** için var (`otomasyon/llm/cekirdek.py`); "aynı dersin benzer işi" için yok.
  Model değişince (OpenDesign geçişi, 2026-11-13) tüm yazım çıktıları farklı üslupla üretilip yeniden denetleniyor.

**Kök mekanizma.** Katmanlar arasında **bağımlılık grafiği** yok. Her katman "kaynak metin değişti mi" sorusunu kendi
başına, çoğu zaman **dosya zamanına bakarak** cevaplıyor; bu yüzden üst katman değişince alt katmanlar ya hep ya hiç
yenileniyor.

**Kalıcı çözüm.**
1. **Bağımlılık grafiği + karmalar**: manifestte her katman `girdi_karmasi` taşır. `hat.py --etkilenen <değişen dosya>` *(önerildi, yazılmadı — 2026-11-16; bugün dosya bağımlılığı için `scripts/altyapi/bag.py etki <yol>`)*
   yalnız gerçekten etkilenen katmanları listeler. Kural: "yalnız etkilenen katman yeniden üretilir".
2. **Parça kimliği**: anlatım cümlesi `c<N>`, soru `q<N>`, önem maddesi `m<N>` kimliğiyle sabitlenir; kapı kimlik
   verir, düzeltme yalnız o kimliğe uygulanır (bu kural `TAM_HAT_HIZLI_AKIS.md` §3'te var — **uygulanmıyor**, koşucu yok).
3. **Önce kaynak, sonra yazım**: ek modülde olduğu gibi "hoca materyali var mı" sorusu ilk adım olur (hat aşaması),
   yoksa yazım başlamaz. Kaynak yoksa kullanıcıya **tek soru** sorulur.
4. **Üretim önbelleği**: aynı girdi karması + aynı istem şablonu → kayıtlı çıktı (model değişse bile "onaylı" çıktı
   korunur), yalnız onaylı düzeltme geçer.

**Önleme kuralı.** Bir katman yeniden üretilecekse manifest `etkilenen` listesinde olmalıdır; listede yoksa koşucu
reddeder ve gerekçe ister.

---

## 7. Oturum çakışması ve eşzamanlı çalışmanın bedeli

**Belirti.** İki oturum aynı dersi işliyor, biri diğerinin sesini/dosyasını eziyor. Sonuç: "hangisi geçerli" belirsizliği,
tekrar denetim, kullanıcıya iki kez sorma.

**Kanıt.**
- Günlükte **151** kez "başka oturum / diğer oturum / çakışma" geçiyor. 69 kez "commit/dağıtım YAPILMADI" notu var —
  yani iş bitmiş ama yayınlanmamış, sonraki oturum aynı işi yeniden yapmış.
- 2026-11-09/10: aynı dört ders (k2-22/23/24/58) iki oturumda işlendi; biri 60 soruluk seti üretti, diğeri 51 soruluk
  hoca dayanaklı setle **ezdi**; kullanıcı "diğer oturum bitsin, bekle" demek zorunda kaldı, 40 dk boşluk oluştu.
- Kilit mekanizması var ama dar kapsamlı: `deploy/oracle/dagit.sh` kilit bekliyor; ders üretiminde **ders bazlı kilit yok**.
- `git status` bu makinede **75 değişik dosya** (25 değişmiş, 47 izlenmeyen, 3 silinmiş); 28 dosya / −121.343 satır diff.
  Yani "başka oturumun commit'siz işi" olağan durum; `dagit.sh --kirli` reddi bu yüzden sık devreye giriyor.

**Kök mekanizma.** İş birimi "oturum" olarak tanımlı, "ders" olarak değil. İki oturum aynı derse girince kimse fark
etmiyor; uyarı yalnız commit aşamasında (çok geç) çıkıyor.

**Kalıcı çözüm.**
1. **Ders kilidi**: `meds_temp/hat/kilit/<key>.json` (`oturum_id`, `başlangıç`, `aşama`). Koşucu kilidi olmayan derse
   başlar, doluysa **durur ve kullanıcıya söyler**. `dagit.sh` de ders kilidi açıkken dağıtımı reddeder.
2. Oturum başında `git status` özeti + "başka oturumun işi" listesi otomatik gösterilir; commit'siz dosyaya dokunmadan
   önce sahibi sorulur.
3. Dağıtımı bitmemiş iş `acik_isler.json`'a yazılır (ders, katman, kalan adım); sonraki oturum "kaldığı yerden devam"
   eder, baştan başlamaz.

**Önleme kuralı.** Kilit alınmadan hiçbir katman yazılmaz; kilit sahibi olmayan oturum o dersin dosyasını değiştirmez.

---

## 8. Derleme/dağıtım çöpü ve depo şişmesi

**Belirti.** Her ön yüz düzeltmesinde 30+ sn build, `dist` 1 GB'a yaklaşıyor, rsync/yedek yavaşlıyor, disk sürekli
büyüyor.

**Kanıt (ölçüldü).**
- `dist` **950 MB**; `dist/assets` **16.150 dosya / 863 MB**. Dosyaların **%82'si** (13.500) 2026-11-15 öncesinden.
- `node scripts/prune-dist.mjs` (kuru çalışma) diyor ki: **13.587 dosya / 474,9 MB silinebilir**. `postbuild` bunu
  `--keep-hours 6 --apply` ile koşuyor; ama `emptyOutDir:false` + 6 saatlik tampon + çok sık build → birikim sürüyor.
- Aynı 32 MB'lık kazanım parçasından **3 kopya** (`chunk-local-data-kazanimlar-q-k1-*.js`), `chunk-glossary-*.js`
  dosyasından **86 kopya**.
- `npx vite build` = **33–35 sn** (4.967 modül). `npx tsc --noEmit` = **5,6 sn** (iyi). `meds-web` açılışı 20–30 sn.
- Depo: `.git` 1,3 GB; izlenen dosya 16.317; izlenen `src/data` 311 MB, izlenen `data` 37 MB. `meds_temp` **15 GB**,
  `meds_downloads` 824 MB, `meds_export` 284 MB, yedek klasörleri ayrıca.
- `src/data/interactive_learning_decks.json` **85 MB** (dosyanın kendi yorumu hâlâ "≈14 MB" diyor), `pastQuestions.json`
  97 MB, `kazanimlar/` 88 MB — tsc/vite her koşuda bu dosyaları işliyor.

**Kök mekanizma.** Derleme çıktısı "geçmiş sürümler için saklanır" mantığıyla budanmıyor; `emptyOutDir:false` kalıcı
kılınmış ve temizlik **zaman tabanlı** (6 saat), **derleme sayısı tabanlı** değil. Veri dosyaları tek parça JSON olarak
büyümeye devam ediyor (decke bölme eklentisi yalnız desteler için var).

**Kalıcı çözüm.**
1. `prune-dist` varsayılanı `--keep-builds 2 --keep-hours 0` + `postbuild`'de `--apply` (şu an 6 saat); build ledger'ı
   zaten var (`dist/.builds`), kural "son 2 derlemenin erişilebilir kümesi" olmalı.
2. Büyük veriler için **sayfa/parça bazlı bölme** (decke eklentisinin kazanım ve sözlük için de uygulanması):
   `kazanimlar/` 88 MB tek parça yerine soru/kazanım ayrı, `glossary` sayfa başına.
3. `meds_temp` için yaş politikası (ör. 14 günden eski ara çıktı `--temizle`); bugün 15 GB.
4. `dist` dağıtıma **artımlı** gönderilir (yalnız güncel manifest kümesi), tüm klasör rsync edilmez.

**Önleme kuralı.** Bir build "tamam" sayılmadan `prune-dist` raporu 50 MB'tan fazla artık göstermemelidir; kapı olarak
`build` sonuna eklenir.

---

## 9. Limit tüketimi: aynı kaynaktan türeyen çok sayıda ayrı LLM işi

**Belirti.** Bir ders için onlarca LLM çağrısı; limit/kota bitiyor, iş yarıda kalıyor, kullanıcı "çok limit harcıyor"
diyor.

**Kanıt.**
- Tek ders için LLM yazımı gereken katmanlar: anlatım (≈186 cümle), örnek sorular (50–80), önem listesi (36–42 madde),
  sesli çözücü (25–40 soru), ara sorular (12–15), çıkmış analizi (24–52 soru), ders analizi, hoca soruları (patoloji),
  terim/kısaltma. Her biri **ayrı istem + ayrı denetim turu**. 26 ayrı `TALIMAT*.md` bu işleri tarif ediyor.
- Denetim genellikle **1–2 tur** sürüyor (ör. "KALIR → düzeltmeler → GEÇER"); her tur tüm ders dosyalarının yeniden
  okunması demek.
- Limit gerçekten bittiği durumlar kayıtlı: alt ajan kotası `insufficient_balance` (2026-11-15, denetçi raporu hiç
  üretilemedi), k2-58 sorularının üç denemede de güvenlik sınıflandırıcısına takılması, günlük `claude -p` 266 çağrı
  olayı (kural 20'nin doğuş nedeni).
- Aynı kaynak metin her katmana **yeniden** veriliyor: anlatım, önem, örnek soru, çözücü, ara soru aynı `sayfalar.json`
  ve aynı hoca dökümünden türüyor, ama istemler ayrı ayrı kuruluyor.

**Kök mekanizma.** "Tek kaynak → tüm ürünler" hedefi (GELECEK_PLANLAMASI §1.3) **veri** düzeyinde var, **çağrı**
düzeyinde yok: her ürün kendi LLM çağrısını yapıyor, ortak bir "ders anlama" çıktısı paylaşılmıyor.

**Kalıcı çözüm.**
1. **Tek "ders anlama" çağrısı** (pahalı ama bir kez): slayt başına kavram, mekanizma, tanım, hoca vurgusu, çıkmış
   eşlemesi, önem adayı → `anlama.json`. Sonraki katmanlar (önem, soru, çözücü, terim) bu dosyadan **betikle** türetilir;
   LLM yalnız gerçekten yazım gerektiren yerde (anlatım cümlesi, soru kökü) çağrılır.
2. **Tek denetim turu, kimlik bazlı**: denetçi `{kimlik, sorun}` verir, düzeltme yalnız o kimliğe yapılır, denetçi yalnız
   o kimlikleri yeniden okur (kural yazılı, koşucu yok — §6 madde 2).
3. **Bütçe görünürlüğü**: `otomasyon/llm/butce.json` var; koşucu her aşama için "tahmini çağrı sayısı" gösterir, kullanıcı
   onaylar. Aşama baştan çağrı yapmaz, kaldığı yerden sürer.
4. **Önbellek anahtarı** girdi karması + istem şablonu sürümü olur (şu an `is_id`); onaylı çıktı model değişse de korunur.

**Önleme kuralı.** Aynı kaynaktan iki katman türeyecekse ikincisi LLM çağırmaz, birincinin çıktısını kullanır; kapı bunu
denetler (ikinci katmanın isteminde kaynak metin değil `anlama.json` olmalı).

---

## 10. Büyük tek dosyalar ve kırılgan mutlak yollar

**Belirti.** Değişiklik yapmak korkutucu; bir satırı düzeltmek 3.000 satırlık dosyada kayboluyor. Betik başka makinede
(Oracle, masaüstü) çalışmıyor.

**Kanıt.**
- `server.ts` **12.297 satır**; `src/services/api.ts` 2.989; `AdminPanelModal.tsx` 3.114; `PastExamsView.tsx` 2.839;
  `App.tsx` 2.763; `CanliDersDers.tsx` 2.213. `src/` toplam 176.730 satır / 1.016 dosya.
- Python: 1.271 betik, 82 alt klasör, `scripts` kökünde 116 betik (28'i `generate_deep_k2_*.py` gibi tek derse özel
  elle yazılmış üretici, 43'ü `fix_/apply_/auto_/batch_` ile başlıyor), proje kökünde 20 tek seferlik `.py/.mjs`.
- **108** satırda `/home/indu` mutlak yolu, **76** betikte. `cozucu_dogrula*.py` içinde sabit
  `/home/indu/medsor/meds_temp/patoloji_ornek26/cozucu`.
- Kök algılama iki farklı biçimde: `parents[2]` (`tam_hat/*`) ve `MEDS = parents[1]; KOK = MEDS.parent` (`otomasyon/*`).
- `meds_database_v2` referansı 149 yerde geçiyor; betik `meds/` içinden çalıştığında bu yol **yok** (kök `medsor/`).

**Kök mekanizma.** Dosya bölme/refactor hiç yapılmadı; her yeni özellik var olan büyük dosyanın sonuna eklendi. Yol
çözümü merkezîleşmedi.

**Kalıcı çözüm.**
1. `scripts/ortak/yol.py` *(önerildi, yazılmadı — 2026-11-16)* — yapılan karşılığı `scripts/kok.py` (tek `KOK`, `MEDS`, `DATA`, `DB`, `TEMP`); mutlak yol yasağı lint ile (`grep -rn "/home/"` → 0).
2. `server.ts` route gruplarına ayrılır (`src/routes/*.ts`), `api.ts` alan bazlı istemcilere.
3. `scripts` kökü tasfiye: tek derse özel üreticiler `scripts/arsiv/` altına; kökte yalnız genel araçlar.
4. `src/data` dev JSON'ları parçalı yüklemeye geçer (decke eklentisi genelleştirilir).

**Önleme kuralı.** 800 satırı geçen yeni dosya kabul edilmez; mutlak yol içeren betik kapıdan geçmez.

---

## 11. Ölçüm ve telemetri eksikliği (hantallığın ölçülemez olması)

**Belirti.** "Uzun sürüyor" ve "çok limit harcıyor" ifadeleri doğru ama hangi aşamanın ne kadar sürdüğü bilinmiyor;
iyileştirme yapıldığında kazanç görülemiyor.

**Kanıt.**
- Makine okunur tek süre kaydı E0: `hazirlik_durum.json` → 7–36 sn (sayfa metni 0–1 sn, görüntü 3–36 sn, çıkmış aday
  5–31 sn). E1–E6 için süre/kayıt yok.
- Oturum süreleri yalnız düz metin günlükte ("40 dk sessizlik", "143 sn döküm", "61 sn dağıtım") — sorgulanabilir değil.
- CI/test yok: `src` altında 9 `*.sinama.ts` var, `scripts/sinama` *(bu yol yok — 2026-11-16; sınama betikleri `scripts/uretim/cizim/sinama/` ve `scripts/asistan/sinama/` altında)* birkaç betik; ama hiçbiri kapı olarak koşmuyor.
  `package.json`'da `test` yok.
- LLM çağrı sayısı/bütçe tüketimi aşama bazında raporlanmıyor (`butce.json` var, rapor yok).

**Kök mekanizma.** Her oturum kendi işini bitirmeye odaklandı; "iş ne kadar sürdü, kaç çağrı yaptı, nerede tıkandı"
sorusu hiçbir yerde toplanmadı.

**Kalıcı çözüm.**
1. `hat.py` *(önerildi, yazılmadı — 2026-11-16; bugünkü koşucu `scripts/hat/tam_hat/kosucu.py`)* her aşama için `sure_sn`, `llm_cagri`, `kapı_hatasi`, `yeniden_yazim` alanlarını `manifest.json`'a yazar.
2. `python3 scripts/hat/tam_hat/rapor.py --son 10` *(önerildi, yazılmadı — 2026-11-16; bugünkü yakın karşılık `python3 scripts/altyapi/saglik_raporu.py` + `python3 scripts/gunluk.py son`)* → ders başına toplam süre, en pahalı aşama, en çok HATA veren kapı.
3. Haftalık tek sayfa "hattın sağlığı" raporu (ders sayısı, ortalama süre, tekrar oranı, açık iş sayısı).
4. Kapıların sınaması CI'ya benzer tek komutla (`python3 scripts/kapilar/kos.py --sinama`) koşar.

**Önleme kuralı.** Yeni aşama, süre ve kapı sayacı yazmadan eklenmez.

---

## 12. Karar belirsizliği ve askıya alınmış katmanların belgede zorunlu görünmesi

**Belirti.** Ajan bir katmanı üretmeye başlıyor, sonra "bu zaten kapalıydı" deniyor; ya da üretmiyor, "eksik" deniyor.

**Kanıt.**
- Askıya alınmış/iptal katmanlar hâlâ zorunlu kurallarda: Öğren destesi (kural 9/9b tam metin duruyor, kural 22 "askıda"
  diyor), quiz (kural 19 uzun metin + kural 19 başında "KAPALI"). Tasarruf kipi (22c) ayrı bir katman kümesi tanımlıyor.
  Aynı katman için 3 farklı "yapılır/yapılmaz" beyanı var.
- `mod.py` "tam" kipinde `ogren_deste`/`quiz` False; ama "tam" adı "her şey" izlenimi veriyor.
- "Hoca ses kaydı varsa/ yoksa" akışı belirsizdi: 6. partide dört ders hoca sesi olmadan üretildi, sonra ses gelince
  kısmi revizyon gerekti. Ek modülde tersi oldu (materyal sorulmadan yazıldı).
- Kullanıcı isteği tek cümle ("bugünkü dersleri de işleme al"), ajan 20+ katmanı kendi yorumluyor.

**Kök mekanizma.** "Hangi katmanlar bu ders için geçerli" sorusunun cevabı **ders bazında** tutulmuyor; global kurallar
ve kullanıcı kararları birbirine karışıyor.

**Kalıcı çözüm.**
1. Ders başında tek **kapsam onayı**: koşucu `mod.py` + kaynak envanterinden (hoca sesi var mı, öğrenci notu var mı,
   patoloji mi) yapılacak katman listesini üretir ve kullanıcıya **tek ekranda** gösterir; onay `kapsam.json`'a yazılır.
2. Askıya alınmış katmanların uzun kuralları `docs/arsiv/` altına; ana belgede tek satır "kapalı — kural 22c".
3. `mod.py` kip adları netleşir: `tam` → `standart`, `tasarruf` → `hizli`; "tam" kelimesi tüm katmanları ima etmesin.

**Önleme kuralı.** Kapsam onayı alınmadan hiçbir yazım aşaması başlamaz; onaylanmamış katman eksik sayılmaz.

---

## 13. Hızlı kazanç listesi (düşük maliyet, yüksek etki — sırayla)

| # | İş | Süre | Kazanç |
|---|---|---|---|
| 1 | `prune-dist --apply` çalıştır + `postbuild` eşiğini 0 saate indir | 10 dk | ~475 MB disk, dağıtım/rsync hızlanır |
| 2 | `kural_secici.py` çalıştır (özetler bayat) + `--denetle`'yi hat başında zorunlu yap | 10 dk | Ajanlar güncel kural okur, sürüm çelişkisi azalır |
| 3 | Hata defteri numara çakışmalarını düzelt (17 çakışma, 13 başlıksız) | 30 dk | Atıf/iz sürme çalışır |
| 4 | `pastQuestions.json` ikinci kopyasını kaldır (ENVANTER E5) | 15 dk | 72–97 MB fazladan yazma/rsync biter |
| 5 | Kök `scripts/*.py` (116 dosya) arşive taşı, kökte yalnız genel araçlar | 1 saat | Arama gürültüsü, yanlış betik çalıştırma riski düşer |
| 6 | `DEGISIKLIK_KAYDI.md` arşivle (son 3 oturum kalsın) | 20 dk | Oturum açılışında ~200k token tasarrufu |
| 7 | Tarama: `/home/indu` mutlak yollarını `ortak/yol.py` *(önerildi, yazılmadı — 2026-11-16)*'ye çevir (108 satır) | 2 saat | Oracle/masaüstü kırılganlığı biter |
| 8 | `kapilar/kos.py` matris koşucusu + tek tablo çıktı | 1 gün | "Hangi kapıyı koşayım" belirsizliği biter, süre ölçülür |
| 9 | `hat.py` *(önerildi, yazılmadı — 2026-11-16)* E0–E6 koşucusu (önce yalnız sıra + kapı denetimi, sonra üretim) | 2–3 gün | Elle 15–20 komut → tek komut; atlama imkânsız |
| 10 | Ders kilidi (`meds_temp/hat/kilit/<key>.json`) | yarım gün | Oturum çakışması ve ezme biter |

## 14. Yapısal (uzun vadeli) sıra

1. **Tek kural belgesi + makine okunur standartlar** (§1, §2) — diğer her şeyin önkoşulu.
2. **Manifest + bağımlılık grafiği + tek koşucu** (§3, §4, §6) — hantallığın asıl kaynağı.
3. **Kapı matrisi + ortak denetim kütüphanesi + kapı sınamaları** (§5).
4. **Tek "ders anlama" çağrısı + türetme** (§9) — limit tüketiminin en büyük kalemi.
5. **Ölçüm/rapor** (§11) — kazancı görünür kılar, geri kaymayı engeller.
6. **Refactor: sunucu/istemci bölme, mutlak yol temizliği, veri parçalama** (§8, §10).

## 15. Bu defterin bakımı

- Yeni bir hantallık nedeni görüldüğünde buraya **madde numarası** ile eklenir; çözüldüğünde madde silinmez, başına
  `✅ çözüldü (<tarih>, <kanıt>)` yazılır.
- Her maddenin bir **ölçümü** olmalıdır (sayı, komut). Ölçülemeyen madde "gözlem" olarak işaretlenir.
- Bu defter `KURUL2_YAPILMAYACAK_HATALAR.md`'nin yerini almaz: orası **içerik hatası**, burası **sistem borcu**.
