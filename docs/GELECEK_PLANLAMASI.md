# GELECEK PLANLAMASI — MeDSor tam otomatik içerik ve tahmin sistemi

> Kayıt: 2026-10-20 (Kurul 1 sınavına 3 gün). Kullanıcının hedefleri, mevcut altyapının gerçek durumu,
> yol haritası ve öneriler. Yeni oturumlar bu belgeyi `PROJE_TANITIMI.md` ve `DEGISIKLIK_KAYDI.md` ile birlikte okur.
> Aşama kayıt defteri (makine okunur): `meds/otomasyon/hat.json` — `python3 meds/otomasyon/hat.py --liste`.

## 1. Kullanıcının hedefleri (özgün istek, özetlenmiş)

1. **Olası soru tahmini (sınav günü ve sonrası):** Bir kurul sınavı 100 sorudur. Öğrencilerin eklediği kayıtlar
   (4000 olsa bile) bu 100 sorunun parçalarıdır. Her yeni veri eklendiğinde o gece (ya da komutla) tüm kayıtlar
   birlikte değerlendirilip her sorunun en olası hâli kurulacak.
2. **Ders materyalini erişilebilir kılmak:** Drive'a her yeni PDF (artık Kurul 2) düştüğünde otomatik okunacak;
   PDF'teki **her resim, tablo ve yazı** önemlidir. PDF içeriği **çıkmış sorularla birlikte** değerlendirilecek,
   böylece sınava konu olan yerler kendini belli edecek.
3. **Tek kaynak → tüm ürünler:** Hocanın PDF'inden üretilen temel dosya; interaktif ders, sesli ders, spot bilgiler,
   sınav asistanı, soru çözücü, örnek sorular, terimler, hastalıklar ve projedeki diğer tüm sayfalara kaynaklık
   edecek; her biri otomatik güncellenecek.
4. **EMA sesi zorunlu:** İnteraktif ders, sesli ders, soru çözücü vb. her sesli sayfa EMA ile seslendirilip
   veritabanına (Oracle) yüklenecek.
5. **Tam otomasyon:** Bilgisayar açılınca Claude kendiliğinden çalışacak: Drive kontrolü → OCR → üretim →
   doğrulama → seslendirme → Oracle'a yükleme. Sürekli kontrol gerekmeyecek; açık/hata/eksik olmayacak.
6. **Kalite:** Sınava yönelik, akılda kalıcı, mekanizma açıklayan, soruları doğru çözen, literatüre ve ders
   kaynağına uygun, müfredat dışına çıkmayan; sorular hem çıkmışlara hem slaytlara dayanan.
7. **Esnek mimari:** Bir düzenleme istendiğinde baştan kurmak yerine eldekini değiştirebilmek; her aşaması belirli,
   amacına uygun, genişletilebilir ve yeniliklere açık.
8. **Kurul geçişi:** Ders programından kurul günleri takip edilecek; Kurul 2 başlayınca site Kurul 2 içeriğiyle
   tam performans çalışacak; Kurul 1 verisi ayrı bir sayfadan erişilebilir kalacak.
9. **Kendini geliştiren sistem:** Sistem kendi kodunu, işlevini ve kapsamını sürekli ileri taşıyacak.
10. **Veritabanı:** Okunabilir, erişilebilir, düzenlenebilir; yeni site sürümü eski veriyle uyumlu.
11. **Kurul 2 sesli metinler:** Bir tıp doktorunun öğrenciye Türkçe anlatım üslubunda; ama ekranda okunduğu gibi değil,
    **madde madde** ve **vurgu yerleri kodlu**. Her cümlenin hangi slayta denk geldiği bilinecek, her cümlenin
    **kimliği (ID)** olacak; örnek ve çıkmış sorulardan bu cümlelere kolayca referans/deeplink verilecek.
    Genelleme: **veritabanındaki her bilgi kimlikli** olacak.

## 2. Mevcut durum (2026-10-20 incelemesi)

### Olan
- **Ders işçisi (Oracle, `meds-ders-isci`):** Drive tarama (`izle.py`, sha256 farkı) → metin/OCR (`cikar.py`,
  PyMuPDF + tesseract) → bağlam (`isle.py`: program eşleşmesi, sözlük, hastalıklar, kazanımlar, **çıkmış soru
  adayları** bge-m3+BM25 ile) → Claude (`TALIMAT.md`) → kapı (`denetle.py`) → yönetici onayı → `yayinla.py`
  (10 dk zamanlayıcı). Üretir: Öğren destesi, ders notu/özet, örnek sorular, sözlük, çıkmış bağları, bilgi havuzu,
  sesli ders metni + Emel/EMA iş kuyruğu.
- **Elle çalışan ama hatta bağlı olmayan üreticiler:** sınav spotları / önem listesi, sesli sınav asistanı, soru
  çözücü (branş başına), Öğren adım sesi (`ogren_ses_uret.py`), hastalık birleştirme, cihaz eşitleme.
- **Kalite kapıları:** `validate_learning_decks.py (--oyun-zorunlu --kurul2)`, `sik_aciklama.py`,
  `turkce_uslup.py`, `sinav_spotlari/dogrula.py --kurul2`, asistan/çözücü doğrulayıcıları.
- **Veritabanı:** meds-pg (Postgres 17 + pgvector), `typed kolon + data jsonb` deseni, NOTIFY → SSE canlı katman,
  `data/content` panel katmanı, append-only **ham soru defteri** (`data/question_ledger/`).

### Eksik (bu planın konusu)
| # | Eksik | Etki |
|---|---|---|
| E1 | Spot, asistan, çözücü, adım sesi, hastalık birleştirme yeni PDF'ten otomatik üretilmiyor | Kurul 2'de elle iş |
| E2 | `denetle.py`/`yayinla.py` `--kurul2` kapılarını çağırmıyor | Kurul 2 kalite kuralı uygulanmıyor |
| E3 | Önem puanı yok: çıkmış soru sıklığı/yakınlığı/tekrar ailesi PDF sayfalarına puan olarak işlenmiyor | "Sınava konu olan yerler" görünmüyor |
| E4 | Görsel ve tablolar ayrı veri olarak çıkarılmıyor (yalnız metin + OCR) | Resim/tablo bilgisi kayboluyor |
| E5 | Olası soru tahmini yoktu | **Bu oturumda kuruldu (v1)** |
| E6 | Kurul tarihleri istemcide sabit kodluydu; sunucuda "aktif kurul" kavramı yok | **Bu oturumda takvime bağlandı** |
| E7 | Slayt/adım, sözlük terimi, çözücü sorusu, sesli metin cümlesi kararlı kimlik taşımıyor | Deeplink/referans kırılgan |
| E8 | Şema sürümü / göç (migration) koşucusu yok; içerik setleri sürümsüz | Eski veri ↔ yeni sürüm uyumu elle |
| E9 | Yönetici onayı elle; bilgisayar açılınca otomatik başlatma yok | "Kendiliğinden çalışma" yok |
| E10 | Kurul kimliği biçimleri karışık (`donem3-kurul1`, `kurul: 1`, `k1`, serbest metin) | Süzme hataları |
| E11 | Hata/eksik raporu tek yerde değil; sessiz başarısızlık (ör. benzer soru araması DNS hatasında boş liste) | "Açık kalmasın" hedefi |

## 3. Mimari ilkeler (tüm yeni işler bunlara uyar)

1. **Aşama kayıt defteri:** Her üretim adımı `otomasyon/hat.json`'da bir aşamadır: `id, kapsam (ders/kurul/genel),
   gerekir, tetik, komut, kapi, cikti, durum`. Yeni ürün = yeni aşama; eski aşamalar değişmez. Çalıştırıcı
   `otomasyon/hat.py` sırayı bağımlılıktan kurar, durumu `meds_temp/hat/durum.json`'a yazar.
2. **Tek kaynak, türetilmiş ürünler:** Hocanın PDF'i → `ders_paketi.json` (+ önem haritası) temel kayıttır. Diğer
   her ürün buradan türetilir ve kaynağın **karmasını** (`kaynak_sha`) taşır; kaynak değişince yalnız etkilenen
   ürünler yeniden üretilir (artımlı).
3. **Kapı olmadan yayın yok:** Her aşamanın doğrulayıcısı 0 HATA vermeden sonraki aşamaya geçilmez (AGENTS.md 14).
   Kapı geçen Kurul 2 içeriği yönetici onayı beklemeden yayınlanabilir (P1.2), ama her yayın geri alınabilir.
4. **Sessiz başarısızlık yasak:** Boş girdi, servis hatası, kota hatası → aşama `kod≠0` + `hat.log` + yönetici
   bildirimi. "Boş liste ile devam" yok.
5. **Kimlik her yerde (§5).** Kimlikler kararlıdır; yeniden üretimde değişmez.
6. **Geri uyum:** Şema değişikliği yalnız ekleme yapar (alan silinmez, anlamı değişmez); okuyucular bilinmeyen
   alanı yok sayar; her JSON üst düzeyde `surum` taşır; DB değişikliği numaralı göç dosyasıdır (§6).
7. **Kurul boyutu:** Her içerik kaydı `kurul` (tamsayı) taşır; görüntü katmanı aktif kurulu takvimden alır.
8. **Donanım kuralları** (AGENTS.md 10): yerel GPU yok (izinli 3 istisna hariç), CPU vektör servisleri, ücretsiz bulut
   LLM zinciri ya da Claude; systemd birimlerinde `MemoryMax/CPUQuota/OOMScoreAdjust`.

## 4. Yol haritası

### P0 — Kurul 1 sınav haftası (20–25 Ekim) ✅ kısmen bu oturumda
- [x] **Kurul takvimi:** `scripts/takvim/kurul_takvimi.py` ders programı PDF'inden 6 kurulu, sınav/final/bütünleme
  tarihlerini ve ders listesini çıkarır → `src/data/kurul_takvimi.json` (+ istemci özeti `kurul_takvimi_ozet.json`).
  Kurul 1 sınavı **23 Ekim**, Kurul 2 **26 Ekim–4 Aralık**.
- [x] **Aktif kurul tek kural:** `src/services/kurulTakvimi.ts` + `scripts/takvim/aktif_kurul.py`;
  `getDefaultActiveCommitteeId()` artık takvimden.
- [x] **Olası soru motoru v1:** `scripts/olasi_soru/` — `topla.py` (kanıt toplama: kök, sürüm, parça, şık, uydu,
  cevap iddiası, yorum, defter katkısı; numaralı → yuva, numarasız → bge-m3 ile en yakın yuva; uzlaşı özeti;
  parmak izi), `TALIMAT.md` (Claude sentezi, kanıt > ders > çıkmış), `dogrula.py` (şema, kararlı kimlik
  `k1-os-001`, kanıt bağı, şık açıklama + Türkçe üslup kapıları), `gece.sh` (yeni kanıt yoksa atlar).
- [x] **Gece zamanlayıcısı (2026-10-20 kuruldu, kullanıcı onayı: LLM işleri yalnız Claude):** birim dosyaları hazır (`otomasyon/systemd/meds-hat-gece.{service,timer}`, 02:30, `Persistent=true` → kapalıyken kaçırılan iş açılışta). Kurulum kullanıcı onayı bekliyor.
- [ ] **Olası sorular ekranı:** `/olasi-sorular?kurul=1` — yuva başına soru, güven rozeti, kanıt sayısı, ders
  bağlantısı; öğrenci "bu soru böyleydi / değildi" geri bildirimi defterle beslenir.
- [ ] **Sınav günü hızlandırma:** 23 Ekim akşamı ilk sentez; 24–26 Ekim her gece.

### P1 — Kurul 2 açılışı (26 Ekim'e kadar, sonra sürekli)
1. **Kurul geçişi:** Ana ekranlar aktif kurulu takvimden süzer; **"Geçmiş kurullar"** sayfası (`/arsiv/kurul/1`)
   Kurul 1 destelerini, spotlarını, çözücüyü, olası soruları salt-okunur sunar. Kişisel ilerleme korunur.
2. **Otomatik onay:** Kurul 2'de tüm kapılar 0 HATA ise `yayinla.py` yönetici onayı beklemeden yayınlar;
   yönetici panelinde "geri al" ve günlük özet bildirimi.
3. **Kurul 2 kapıları ders işçisine:** `denetle.py` → `validate_learning_decks.py --oyun-zorunlu --kurul2`,
   `sik_aciklama.py`, `turkce_uslup.py`; `yayinla.py` da aynı bayrakla.
4. **Sesli metin şeması v2 (cümle kimliği):** her cümle `{id, slayt, sayfa, metin_ses, metin_ekran (madde),
   vurgu: [{bas, son, tur}], kanit}`. Ekranda madde madde + vurgulu, seste doğal doktor anlatımı. Kimlik §5.
5. **Zincirin tamamlanması:** `spot_onem → sinav_asistani → soru_cozucu → ses_ema` aşamaları ders başına çalışır
   hâle getirilir (TALIMAT'lar hazır; branşa bağımlı sabit listeler ders kimliğine çevrilir). EMA seslerinin
   tamamı Oracle'a yüklenir; eksik ses = kapı hatası.
6. **RAG tetiklemesi:** yayından sonra `rag_vektor` aşaması (3 saatlik cron yerine/yanında).
7. **Hastalık birleştirme** ve **cihaz eşitleme** otomatik aşama.
8. **Kurul kimliği normalizasyonu:** tek biçim `kurul: int` + `committeeId: donem3-kurulN`; okuyucular eskiyi de kabul eder.

### P2 — Kalite ve önem (Kasım)
1. **Görsel ve tablo çıkarımı:** sayfa görüntüsü (PNG), tablolar (`find_tables` → satır/sütun JSON), görsel alt yazısı
   (OCR + Claude görsel betimleme, yalnız slayttaki bilgi). `kaynak.md` yanında `sayfalar.json`.
2. **Önem haritası:** sayfa/cümle başına puan = çıkmış soru yakınlığı (bge-m3) × sıklık (yıl sayısı) × yakınlık
   (son yıllar ağır) + tekrar ailesi (`tekrar_analizi`) + hocanın vurgusu (kalın/renk/"önemli"). Tüm üreticiler
   (spot, çözücü, örnek soru, deste) bu haritayı girdi alır; ekranlarda "sınavda çıktı ×3" rozeti.
3. **Örnek soru üretimi:** hem ders cümlesine (`cumle_id`) hem benzer çıkmışa bağlı; soru başına kaynak deeplink.
4. **Kalite karnesi:** her ders için kapsam (sayfaların % kaçı en az bir ürüne girdi), çıkmış kapsamı, ses
   tamamlığı, kapı sonuçları → `/manage/hat` paneli.

### P3 — Veritabanı ve kimlik (Kasım–Aralık)
1. Numaralı göç koşucusu + `schema_migrations` tablosu (§6).
2. Kimliksiz varlıklara kimlik: deste adımı, sözlük terimi, çözücü sorusu, sesli cümle (§5); eski erişim yolları
   (dizi sırası, terim adı) okuyucuda takma ad olarak korunur.
3. **İçerik seti sürümü:** `content_sets(id, kurul, tur, surum, kaynak_sha, uretildi)`; istemci "bu ders güncellendi".
4. **Evrensel deeplink:** `/k/<kimlik>` → çözücü yönlendirme (deste adımı, cümle, spot, soru, terim, hastalık).
5. Veri kataloğu (`/manage/veri`) kimlikle arama + satır içi düzenleme + değişiklik geçmişi.

### P4 — Kendini geliştiren döngü (sürekli)
- **Haftalık iyileştirme turu (gece, Claude):** `hat.log` hataları, kapı uyarıları, öğrenci hata bildirimleri
  (`learn_feedback`), olası soru geri bildirimi ve kullanım günlüğü (etkinlik günlüğü) okunur → önerilen
  düzeltmeler **ayrı dalda** yapılır, testler + kapılar + `vite build` geçerse yönetici paneline "önerilen
  güncelleme" olarak düşer. **Kod dağıtımı kullanıcı onayıyla** (güvenlik: kendi kendini kontrolsüz değiştiren
  sistem yok). İçerik düzeltmeleri kapılardan geçerse otomatik.
- Yeni kapı: kullanıcının bildirdiği her hata türü `KURUL2_YAPILMAYACAK_HATALAR.md`'ye + mümkünse otomatik kapıya.

## 5. Kimlik (ID) standardı

Biçim: `<kurul>-<ders>-<tür>-<sıra>`; küçük harf, ASCII, kararlı. Yeniden üretimde aynı içerik aynı kimliği alır
(kimlik sıra numarasıdır, içerik karması değildir; içerik değişse de kimlik korunur, `kaynak_sha` değişir).

| Varlık | Örnek | Not |
|---|---|---|
| Kurul | `k2` / `donem3-kurul2` | iki biçim eşlenir |
| Ders | `k2-07` | ders programı sırası |
| PDF sayfası | `k2-07-p12` | |
| Görsel / tablo | `k2-07-p12-g1`, `k2-07-p12-t1` | P2.1 |
| Bilgi paketi maddesi | `k2-07-b034` | `ders_paketi.bilgi_paketi[].no` |
| Sesli ders cümlesi | `k2-07-c0142` | `slayt`, `sayfa`, `vurgu` alanlarıyla |
| Öğren destesi / adım | `k2-07-d` / `k2-07-d-s05` | |
| Etkileşim ögesi | `k2-07-d-s05-i3` | |
| Spot | `k2-07-s01` | mevcut `k1-01-s01` ile uyumlu |
| Asistan noktası | `k2-07-a13` | mevcut `01-13` takma ad |
| Çözücü sorusu | `k2-07-q05` | |
| Örnek soru | `k2-07-os-012` | |
| Olası soru | `k2-os-037` | yuva numarası |
| Terim / hastalık | `t-<slug>` / `h-<slug>` | ad değişse de slug sabit |

Deeplink: `/k/k2-07-c0142` → ilgili sayfada o cümleye kaydırıp vurgular. Soru açıklamaları `[[k2-07-c0142]]`
biçiminde referans verir; ekran bunu "Derste: …" bağlantısına çevirir.

## 6. Veritabanı uyumu

- `deploy/pg/sql/goc/NNNN_ad.sql` numaralı, idempotent göçler; `schema_migrations(no, ad, uygulandi)` tablosu;
  `scripts/db/goc.py` hem yerelde hem Oracle'da (tünel) sırayla uygular. Göç yalnız ekler; ad değişikliği =
  yeni kolon + geçiş dönemi.
- JSON içerik dosyaları: üst düzey `surum`; okuyucu `surum`'a göre dönüştürücü (`normalize_vN`) çalıştırır.
- Yeni site sürümü eski veriyi okuyabilmeli: istemci bilinmeyen alanı yok sayar, eksik alana varsayılan verir.

## 7. "Bilgisayar açılınca kendiliğinden" çalışma

- **Önerilen yol (sağlam):** Claude Desktop'a bağımlı olmadan `systemd --user` zamanlayıcıları: `meds-hat-gece.timer`
  (02:30, `Persistent=true` → kapalıyken kaçırılan iş açılışta çalışır). LLM gereken aşamalar başsız `claude -p`
  ile çalışır (ders işçisinin Oracle'da yaptığı gibi). Masaüstü uygulaması açık olmasa da çalışır.
- **İsteğe bağlı:** Claude Desktop'ın açılışta başlaması (oturum açma uygulaması) + uygulamanın zamanlanmış görevi;
  ama sürekli kontrol istenmediği için systemd yolu birincil.
- Drive taraması Oracle'da sürekli çalışıyor (bilgisayar kapalıyken de); yerel işler yalnız seslendirme/GPU izni
  olanlar ve olası soru sentezidir.

## 8. Ek öneriler (kullanıcıya sunuldu)

1. **Sınav günü toplama ekranı:** sınavdan çıkınca hızlı giriş — "Soru 37: kök … / şıklar … / benim cevabım …",
   numara zorunlu alanla yuvalama doğruluğu büyük artar.
2. **Güven kalibrasyonu:** sonraki yıl resmî anahtar gelince olası soruların doğruluğu ölçülür; motor ağırlıkları
   (oy, kişi sayısı, ders uyumu) buna göre ayarlanır.
3. **Hocaya göre çıkmış profili:** aynı öğretim üyesinin geçmiş soru tarzı (tanı, mekanizma, sayı) önem haritasına girer.
4. **Kişisel tekrar planı:** sınava kalan gün + önem haritası + kişinin yanlışları → günlük çalışma listesi.
5. **Yayın öncesi örneklem denetimi:** her otomatik yayından rastgele 5 öge "denetçi" Claude'a ikinci kez okutulur.
6. **Tek sağlık panosu:** `/manage/hat` — aşama durumları, son başarı, kuyruk, kota, eksik ses, kapı hataları.
7. **Yedek ve geri alma:** her yayın öncesi içerik anlık görüntüsü (Oracle `meds-pg-yedek` + dosya), tek tık geri alma.

## 9. Bu oturumda kurulanlar (2026-10-20)

| Dosya | Görev |
|---|---|
| `meds/scripts/takvim/kurul_takvimi.py` | Ders programı PDF → kurul takvimi JSON |
| `meds/scripts/takvim/aktif_kurul.py` | Aktif / son sınav / arşiv kurul (Python) |
| `meds/src/services/kurulTakvimi.ts` | Aynı kural (TS); `firestoreDb.getDefaultActiveCommitteeId` buna bağlı |
| `meds/src/data/kurul_takvimi.json`, `kurul_takvimi_ozet.json` | Üretilmiş takvim |
| `meds/scripts/olasi_soru/{topla,dogrula}.py`, `gece.sh`, `TALIMAT.md` | Olası soru motoru v1 |
| `meds/otomasyon/hat.json`, `hat.py` | Aşama kayıt defteri + çalıştırıcı |
| `meds/docs/GELECEK_PLANLAMASI.md` | Bu belge |

## 10. 2. tur (2026-10-20, kullanıcı onayıyla)

| Ne | Dosya | Durum |
|---|---|---|
| Gece zamanlayıcısı kuruldu (02:30, `Persistent`, 10 sa, 4G, LLM = `claude -p` dar izin listesi) | `~/.config/systemd/user/meds-hat-gece.{service,timer}` | etkin, uçtan uca denendi |
| Sağlık denetimi (canlı API, Oracle SSH, 3000, vektör, EMA, disk) | `meds/otomasyon/saglik.py` | hatta |
| Olası soru uçları + yayın (kapı → `data/olasi_sorular/kN.json` → Oracle) + öğrenci geri bildirimi kanıta döner | `src/services/olasiSoruRoutes.ts`, `scripts/olasi_soru/gece.sh`, `topla.py` | hazır |
| **Ders kayıt defteri** (Kurul 2–6, 289 ders; kimlik `k2-07`, kod `2f01`, kararlı; K2 çıkmışlarının 684/684'ü derse bağlı) | `scripts/dersler/ders_kaydi.py` → `src/data/dersler/kN.json` | hazır |
| Ders işçisi K2 numarası/kodu defterden | `scripts/ders_isci/isle.py` `ders_kaydi_eslesmesi` | Oracle dağıtımı bekliyor |
| **Ders zinciri** (hazirla → onem → cozucu → bağımsız denetim → birlestir → asistan → EMA ses → Oracle; kapılı, durumlu, kaynak değişince baştan) | `meds/otomasyon/ders_zinciri.py` | hatta (gece 3 ders) |
| `aday_hazirla.py` fonksiyonlara ayrıldı (K1 çıktısı birebir aynı, ölçüldü) | `scripts/spot_cozucu/aday_hazirla.py` | hazır |
| **Sesli metin v2** (cümle kimliği, ses/ekran iki yüz, madde düzeyi, vurgu kodu, sayfa + slayt + çıkmış bağı; eski biçim türetilir) | `scripts/sesli_anlatim/konusma_v2.py`, `TALIMAT_SESLI.md §v2`, `isle.py`, `yayinla.py` | K2 için zorunlu; Oracle dağıtımı bekliyor |
| K1 geri doldurma: 69 ders, 21.272 cümle kimliği (metin değişmedi, kayıpsız) | `data/sesli_anlatim/v2/` | yerel; Oracle'a gönderilmedi |
| Evrensel kimlik çözücü | `GET /api/k/:id` (`src/services/kimlikRoutes.ts`) | yerel |

Açık: `/k/<id>` ön yüz yönlendirmesi ve `#kimlik` kaydırması (sesli ders, olası sorular); otomatik onay (P1.2); K2 branşlarının
ön yüz kaydı (`components/spots/brans.ts`: `k2noroloji` …, kod düzenli ifadeleri `2n03` biçimini kabul etmeli); önem haritası (P2.2);
görsel/tablo çıkarımı (P2.1); göç koşucusu (P3).

## 11. 3. tur (2026-10-20, Oracle yeniden başlatıldıktan sonra; dağıtıldı)

- **Kesinti nedeni:** iki oturumun eşzamanlı dağıtımı Oracle'da belleği tüketti (deploy-code.sh'a kilit eklendi). Sağlık aşaması bunu artık gece yakalar.
- **Canlıda:** ders işçisi K2 defter numarası, `--kurul2` kapıları (denetle + yayinla), sesli metin v2 kapısı, **otomatik onay** (Kurul 2+, panel ayarı `otomatik_onay`), PDF tablo/görsel/hoca vurgusu çıkarımı + görsel kanıt türü; `/k/<kimlik>` 302 kısa bağlantı (servis çalışanı dışında); ses uçları `2n03` kodlarını ve `k2<brans>` klasörlerini kabul eder; K1 cümle kimlikleri Oracle'da.
- **Göç koşucusu:** `scripts/db/goc.py` + `schema_migrations`; `0001_icerik_setleri` iki makinede uygulandı; gece `db_goc` aşaması. Üreticiler `scripts/db/icerik_kaydi.py` ile sürüm yazar.
- **Önem haritası:** `scripts/onem/onem_haritasi.py` (sayfa başı 0–100), zincirin hazirla adımında; sınamada 3 K1 dersinde bağlanamayan çıkmış 0.
- **Branş tek kaynak:** `src/data/dersler/branslar.json`; `brans.ts` Kurul 2+ klasörlerini kendiliğinden sekmeye çevirir (derleme ile sınandı).
- **Tuzak:** `dist` `emptyOutDir:false` → eski parçalar kalır; derleme sınamasında yalnız güncel parçaya bak. rsync saat damgasını koruduğu için "değişen dosya → yeniden başlat" kararı yanılabilir; sunucu kodu gönderilince sağlık + uç denemesiyle doğrula.
- **Açık:** sesli ders/olası soru ekranında `#kimlik` kaydırması; Sesli ders · En önemliler · Spotlar · Soru çözücü · Çıkmış ekranlarına `?kurul=` süzgeci; ders zincirinin ilk gerçek Kurul 2 dersiyle uçtan uca koşusu (ilk K2 PDF'i gelince).

## 12. 4. tur (2026-10-20) — kalan işler kapatıldı

- **Hastalık zinciri** `otomasyon/hastalik_zinciri.py`: Oracle önerileri → Claude şema 2 (`scripts/diseases/TALIMAT_SEMA2.md`) →
  `yayinla.hastaliklari_uygula` (kapılı, geri alınır) → Oracle `data/content/diseases.json` + `POST /api/admin/icerik/diseases/degisti`
  (`src/services/icerikYayinRoutes.ts`, panel sırrı; x-admin-email'e güvenmez) → SSE. Uçtan uca koşuldu: 3 profil (k1-40), denetim 0→0, canlıda.
- **Gece içerik dağıtımı** `otomasyon/icerik_dagit.py`: Oracle'da ön yüz derlenmediği için yayımlanan deste/zincir çıktıları dist
  gönderilmeden görünmez. origin/main temiz worktree + Oracle src/data + zincir çıktıları → vite build → yalnız dist. Koruma: çalışma
  ağacında commit'lenmemiş ön yüz kodu varsa ATLAR (çıkış 3, panoda kırmızı) — başka oturumun ağaçtan yaptığı canlı dağıtımı geri almasın.
- **Kimlik kaydırma + kurul süzgeci:** sesli ders `#k1-03-c0142` → paragrafa kaydırır, cümleyi işaretler, "Buradan dinle"; olası soru kartı;
  `/?kimlik_yok=` bilgisi; `?kurul=N` Sesli ders, En önemliler, Spotlar, Soru çözücü, Çıkmış (+ Geçmiş kurullar bağları). Tarayıcıda sınandı.
- Elle kalan tek aşama: kod dağıtımı (`esitle_dagit`) — bilinçli olarak kullanıcı/oturum kararında.
- **Çok oturum tuzağı:** oturumlar ortak ağaçta toplu commit atıyor; karışık dosyada yalnız kendi parçanı `git apply --cached` ile sahnele,
  sahnelenmiş ağacı `git checkout-index` ile ayrı klasöre çıkarıp `tsc` ile sına.

## 13. Bağımsız denetim + düzeltmeler (2026-10-20, commit 5e597dc; Oracle'a gönderildi)

Bulunan ve kapatılan hatalar:
| # | Hata | Düzeltme |
|---|---|---|
| K1 | yayinla.py yalnız Kurul 1 yayınlıyordu → K2 zinciri sessizce boş | s14/s16 `kurul_ayarla`, yayinla `kurula_bagla`; uygula() tur başına tek kurul (en küçük önce); K1 gerileme testi TAMAM |
| K2 | hastalık zinciri K1 kayıtlarını değiştirebilirdi (k1-40 koşusu: 2 kayda yalnız madde EKLENDİ, kayıp 0) | yalnız `k[2-6]-*` öneriler; geri alma/zaman aşımı raporlanır |
| K3 | denetimden geçmemiş ders branş birleştirmesiyle yayına sızabilirdi | `onayli.json` (denetim + denetçi raporu şart); kaynak değişince ara dosyalar `_eski/`e |
| Y1 | başarısız aşamanın bağımlıları çalışıyordu | hat.py bağımlılık engeli (kod 10), kod 3 = atlandı, kilitli durum yazımı |
| Y2 | içerik dağıtımı origin/main'den → dağıtılmamış kod canlıya çıkabilirdi | deploy-code.sh `dist/dagitim.json` damgası; içerik dağıtımı yalnız o commit'ten, canlı kirliyse atlar; Oracle src/data birebir + panel katmanı; uzak rsync yayın kilidiyle |
| Y4 | olası soru: sentez başarısızsa yeniden denenmiyordu | `yayinlanan_iz.txt` yalnız yayından sonra; claude hatası betiği kesmez |
| — | olası soru yerel veriyi okuyordu (öğrenci kayıtları Oracle'da) | gece.sh Oracle'dan salt-okunur çeker, çekemezse durur |
| — | sınav akşamı işlenmiyordu | `meds-olasi-soru.timer` 20:00 + 23:30 (kilitli) |
| — | tarih süzgeci UTC | TR saatiyle sınav 10:00 sonrası |
| Y5 | sürekli hata veren ders kotayı tıkıyordu; önceki kurul terk ediliyordu | geri çekilme 1-2-4-7 gün; Kurul 2..aktif |
| Y6 | `4q01`/`5q01` çift ders kodu | branslar.json +5 branş, sayaç harfe göre, bilinmeyen/çift = HATA |
| Y7 | defter eşleşmesi yoksa yanlış derse bağlanabilirdi | uyarı → otomatik onay kapanır; defter konusu kimliğe |
| — | örnek sorular ekranı/dizin yalnız k1 | K1–6 klasörleri (ekran, PDF kaynakları, yönetim, RAG) |
| orta | claude zaman aşımı yok, birleştirme sessiz 0, sürüm kaydı yolu, göç commit'siz/işlemsiz, takvim boş yazım, geri bildirim sınırsız, Türkçe kurul adı | hepsi düzeltildi |

`claude -p` gözetimsiz ortamda (systemd, dar izin listesi) sınandı: izinli araçlar çalışır, izin dışı komut takılmadan reddedilir.
