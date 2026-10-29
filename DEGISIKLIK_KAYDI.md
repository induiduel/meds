## 2026-10-29 — v15 üst çubuk arka plan göstergesi stilsizdi (H439)
- `ap15g` kuralları tembel yüklenen `kisisel.css`'ten kabuğun `shell.css`'ine taşındı; kart çerçeve/zemin ve etiket stili kendine yeterli. Yerel tarayıcı ekran görüntüsü alınamadı (yerel sekme açılışta takıldı); derlenmiş ana CSS'te kuralların varlığı doğrulandı.

## 2026-10-29 — Kurul 2 (2026-27) ara soruları üretildi: 7 ders, 77 soru (kural 27)
- k2-01 (5), k2-02 (9), k2-03 (13), k2-04 (12), k2-05-v2 (12), k2-07 (12), k2-08 (14); k2-06'nın sesli dersi yok. Branş `k2hocaara`, kodlar 2a01…2a08; veri `src/data/k2hocaara_cozucu/`, ses `data/k2hocaara_cozucu/ses/` (EMA, GPU).
- Tıbbi kaynak yalnız PDF sayfa metni (pymupdf); ders akış metni yalnız slayt eşlemesi için (Whisper hatası riski). Yazar alt ajan + bağımsız denetçi; 6 derste denetçi düzeltmesi, düzeltilen 21 soru ikinci denetimden GEÇER (H436). `kur.py dogrula --ses` 7/7 0 HATA.
- k2-05 için yalnız `k2-05-norolojik-muayene-v2` anahtarına bağlandı (eski anahtarda ara sayfa çıkmaz).

## 2026-10-29 — Sesli derste "Hocanın sorabileceği soru" ara sayfası + ünlem modu (AGENTS kural 27)
- Ön yüz: `canliDers/CdHocaAra.tsx` (slaytın son paragrafı bitince ders durur → yapay soru sayfası; EMA oku → 5 sn düşün → çöz `c/d` → slayttan anlat `a-N` → derse dön; PDF çubuğunda ünlem = tümü ardışık), `styles/v15/hoca_ara.css`; ders sayfasında "Hocanın sorabileceği sorular" kartı (`dersAraCozucu`), çözücü branşı `k<N>hocaara` (`brans.ts`), `CSoru.ara/anlatim`, `DersSoruTur 'hoca'`.
- Hat: `scripts/hoca_ara_soru/kur.py` (iskele/dogrula/birlestir; kapılar: ileriye sızıntı, dayanak, slayt atfı, şık/üslup, profil, `--ses` klip eksiksizliği), `TALIMAT.md`; `spot_cozucu/ses.py` `anlatim` → `a-N` klibi; `hat.json` `hoca_ara_soru`, el kitabı §19 11d, standart §2 13b.
- Yerelde deneme verisiyle sınandı (ünlem modu, ders içi otomatik açılış + sürdürme, ders dışı çözücü); deneme verisi silindi. Henüz hiçbir derste ara soru verisi yok (yeni derslerle üretilecek).

## 2026-10-28 — Sesli ders: adsız gönderme yasağı (H434)
- `metin_denetle.py` BAGLAMSIZ kapısı (paragraf başında "bu hastalıkta/durumda…", "burada", "bunlarda" → HATA); kural KURUL2_DERS_STANDARDI §8.13, ANLATIM_KURGU_STANDARDI, hata defteri H434. Mevcut dersler toplu değiştirilmedi. Commit/dağıtım yapılmadı.

## 2026-10-28 — Öğrenci yerleşim bulguları (H230–H241)
- H230 `dersler.css` d15-tools 4 sabit sütun → auto-fit (3 araçta sağ boşluk). H231 `v12/cards.css` kartlar başlığı telefonda tek satır + deste satırı soluk kenar.
- H232 `rebuild.css` ≤420 px soru kartı başlığı: araç 30 px, ders hapı içerik kadar. H233/H234 `test-builder.css` "Testi oluştur" yapışkan alt bilgi, ders hapı kaydırma ipucu.
- H235 `v15/soru.css` PC'de eylem çubuğu soru içeriğinin hemen altında. H236/H237 `baslangic.css` 4 ders kartı 4 sütun, "Nasıl çalışır?" hapı satırda.
- H238 `cevrimdisi15.css` ≥600 px kurul çipleri sarar, toplu indir çipleri sıkı. H239–H241 `DersProgramiV15.tsx`: sesli ders bağlantısı yalnız bu yılın anahtarı + `ders_id_tam` birebir; glob anahtarı yanlış olduğu için Kurul çipleri hiç çizilmiyordu (programVar); tarihsiz dersler "Invalid Date" yerine "Tarihi belirsiz".
- Commit/dağıtım yapılmadı.

## 2026-10-28 — Terim / kısaltma / bilgi paketi hazır sesleri (EMA GPU)
- `scripts/sesli_anlatim/terim_ses_uret.py` (başlatıcı `patoloji_cozucu/cozucu_ses_gpu.sh`, kural 10 ikinci istisna yolu): PDF terim yardımcısı (`sesli_anlatim/terim|kisaltma`), `ders_icerik` (terim/kısaltma/bilgi) ve iki genel sözlükten **5.615 benzersiz** "başlık + 1-2 cümle" klibi → `data/terim_ses/<h2>/<h>.mp3` (226 MB, ~10,3 sa, 0 hata) + `kayit.json`. Anahtar `h = sha1("terim-1|"+başlık+"|"+tanım)[:12]` (ekrandaki metinle; `anahtar()`); yeniden çalıştırma yalnız eksik/değişeni üretir.
- Kök neden/ders: Unicode simgeler (α, β, ⁺, ₂, ≥, µ, ²) EMA'da "unikod U artı 207A" diye okunuyordu; `konus()` okunuşu Türkçeleştirir (alfa, artı, büyük eşit, mikro, kare, yüzde, bölü, CYP 2 D 6). Başlık tek başına sentezlenince süre denetimi şaşıyordu → başlık+tanım tek paragraf. Yeni terim/bilgi kaynağı eklenirse simge içeriyorsa `konus()`'a kural eklenir.
- Henüz arayüze bağlanmadı ve Oracle'a taşınmadı (rsync + `anahtar()` ile arama gerekir). Commit/dağıtım yapılmadı.

## 2026-10-28 — Soru çözücü / En önemliler başlangıcı: kurul süzgeci hatası + sade tasarım (H124)
- `spots/BransBaslangic.tsx`: liste seçili kurula göre (`useSeciliKurul`), "Tümü" yok, "Kurul N" öneki atılır, başlanmışlar önde; başlık "Kurul N dersleri".
- `ui/Baslangic.tsx` v15 dalı + `styles/baslangic.css`: kurul şeridi ile özet tek satır, vurgulu devam kartı, halka yerine alt ilerleme çubuğu + yüzde, üzerine gelince yükselen kart/kayan ok/"Başla", basınca küçülme; alt bağlantılar ayraçlı tek satır.
- `olasi-sorular.css` `.ks` → `.ks.kseridi` (kurul seçicisine kutu çiziyordu). Canlıya gönderilmedi.

## 2026-10-28 — Kaynak sayfa kapısı (H109) + Favoriler (★/↻, Bugün, PDF)
- `scripts/ders_icerik_kaynak.py` (adim→slayt→PDF sayfası `s`) k2-01..08 paketlerine uygulandı (650+ terim); kaynaksız 2 terim silindi; `ders_icerik_dogrula.py` `s` eksik/iskelet terimde HATA; el kitabı §19 11a + H109.
- Favoriler: `services/favoriStore.ts` (`medsoru_favoriler_v1`, userKvSync'te), `v15/FavDugme.tsx` (ders içerik kartlarında), `v15/FavorilerBugun.tsx` (Bugün, kaynağa gider, ders/slayt/sayfa bilgili maddeli PDF = iframe yazdır). Canlıya gönderilmedi (dagit.sh bekliyor).

## 2026-10-27 — Quiz her ders için açık + örnek soru kapsamı (k2-05, k2-08)
- Farmakoloji kapsam kilidi kalktı (`quiz_motoru/kapsam.py`, AGENTS kural 19); `quiz_dogrula.py` artık `sik_aciklama` standardını da denetler; elle üretilen ders yayınlı sesli dersle "tamamlandı" sayılır.
- `quiz_havuzu.json` (meds_database_v2/ders_isci/yayinlanan/elle-k2-05|k2-08/): k2-05 116 atom/232 soru, k2-08 205 atom/410 soru, 0 HATA. Kaynakta çelişkili/görsele bağlı/kanıtı eşleşmeyen atomlar havuza alınmadı (k2-05: 12, 33, 36; k2-08: 056, 057, 068, 083, 093, 131, 188, 198, 211). Quiz havuzu henüz sitede bir ekrana bağlı değil.
- Örnek soru kuralı (önem tamamı + ayrıntı ~%40, 50<n≤100; `KURUL2_DERS_STANDARDI.md` §10.8, bundan sonra her ders): k2-05 34→69, k2-08 43→95, canlıda (onem 484). `s16` kazanım tavanı `100-3*(kaz-1)`. k2-05'te monoparezi/stupor vb. tanımlar slaytta yalnız terim; açıklamalar genel tıp bilgisinden.

## 2026-10-27 — k2-05 Nörolojik Muayene Faz C: çizim, önem/çözücü/asistan
- Çizim 63 (52 kontur + 11 şablonlu panel; `data/sesli_anlatim/cizim/k2-05-norolojik-muayene.json`), kapılar 0 HATA; önem 42 madde, çözücü 20 soru, asistan 33 nokta (`src/data/k2noroloji_*/2n03.json`), EMA sesi (çözücü 181, asistan 183 klip); quiz envanteri 119 atom.
- Hata H116: birleştiriciler branştaki eski dersin dosyalarını da yeniden yazıyor; elle zincirde yalnız yeni ders dosyaları sahnelenir.



## 2026-10-27 — Kurul 2 k2-08 Beyin ve İskelet Sistemi Gelişimi Genetiği (Tıbbi Genetik 1) — Faz B (aşama 7–11) tamam
- Anlatım: 16 bölüm · 86 paragraf · 422 cümle · 5.611 kelime (≈50 dk); `metin_denetle` 0 HATA, `konusma_v2 --dogrula` 0 HATA, bağımsız öğrenci denetçi tur 1 KALIR → düzeltme → tur 2 GEÇER (H112).
- Hocanın sınav özeti (32:36–36:50): HOX/OTX/MSX/PAX6 (s10,12,13,15), holoprozensefali oluşum+hasar, trizomi 13/18, üç tip (s23–25), lizensefali (s26), somit/kraniyofasiyal hastalık adları (s31,34,35,37,39), kraniyosinostoz 3 tip (s41), displazi tip adları/FGFR3 (s50,51) ilgili paragrafta + son bölümde özetlendi; 1–44. slayt için "hoca anlattı" yok (kayıt s.45'ten başlıyor). Çıkmış `dogrudan`: HPE siklops (s24), DMD en sık MD (s80); chip 8 soru (6 ilişkili).
- Yayın: Öğren destesi (87 slayt, `--oyun-zorunlu --kurul2` 0 HATA), ders notu, 43 örnek soru, 160 sözlük terimi (`yayinla.py --yerel`), Oracle `ders-ekle` + EMA (21 parça, 2369 sn), cümle/kelime zamanı, anlamsal çapa 422 cümle %98 (0 HATA), PDF işareti kapsama %98, terim 242, kısaltma 75 (H110), `takip_kapisi` 0 HATA. Çizim, önem/çözücü/asistan, quiz, dağıtım Faz C'de.
- Yeni hatalar: H110 (kısaltma elle sözlüğü), H111 (alt ajan çapa indeks kayması), H112 (anlatım denetçi bulguları).

## 2026-10-27 — Yeni PDF standart akışı
- `docs/KURUL2_DERS_STANDARDI.md` §9: yeni PDF geldiğinde karşılama/sınıflandırma (sınama kuralı), üretim, yayın sırası (H97/H99), kayıt. AGENTS.md başına işaret eklendi (AGENTS.md git dışında).

## 2026-10-27 — Sesli ders: çizimsiz resimde zoom takılı kalıyordu
- Belirti: resimde çizim yokken sayfa yakınlaşmış (is-yakin) halde kalıyordu.
- Kök neden: `CizimLayer` kaldırılırken temizlik `kokRef.current` üzerinden sayfayı buluyordu; React ref'i o an boşalttığı için (null) yakınlaşma sınıfı/`--yakin-t` hiç silinmiyordu.
- Çözüm: sayfa öğesi bağlanırken yakalanır, kaldırmada doğrudan sınıf ve değişken silinir. Önleme: unmount temizliğinde `ref.current` okunmaz, öğe önceden yakalanır.

## 2026-10-27 — k2-08 Beyin ve İskelet Sistemi Gelişimi Genetiği Faz C (aşama 12–16)
- Çizim 37 (14 kontur, 1 odak oku, 22 şablonlu panel; yeni şablon `tip_ozellik`); anlam denetimi iki bağımsız geçiş (23 panel tamam, düzeltmeler uygulandı), `cizim_kapisi` 0 HATA, `panel_sinama` 366/567/1100 px 0 hata. Resim sayfaları 24, 27, 68, 73, 78, 81, 82; s.15 fotoğrafları (aniridi) emin olunamadığı için çizilmedi. P81.C2 çapası `madde`den `resim`e çevrildi (Gowers fotoğrafı), işaret yenilendi.
- Önem 44 madde (hoca sınav yerleri + çıkmış `dogrudan` HPE siklops/DMD en üst bant), çözücü 28 soru, asistan 38 nokta; üç doğrulayıcı 0 HATA, 2 bağımsız denetçi GEÇER; ses EMA GPU (çözücü 252, asistan 244 klip). Quiz envanteri 227 atom (slayt iç çelişkili 13 atom `quiz_kullanimi: yasak`); quiz sorusu yok (yalnız Farmakoloji).
- Yeni hatalar: H114, H115.

## 2026-10-27 · Ders içerik sayfaları (k2-05 ilk ders) — yerel; commit/dağıtım yok
- **EMA terim okunuşu + ses temizliği + anlatım kurgusu + çizim renk/zoom/panel (2026-10-28, H128):** `terim_okunus.py` + `okunus/terim_okunus.json` (~600 terim + Latince kural motoru, `--denetle`/`--tara`), `ema_isci.py` Kurul 2+/modül yoluna bağlı + `ses_temizle`; `docs/ANLATIM_KURGU_STANDARDI.md` (TALIMAT_SESLI, TAM_HAT_HIZLI_AKIS, kural_secici anlatim aşamasına bağlı); `CizimLayer.tsx`/`pdfDoc.css` çok renk + marker boyama + panel erken açılış + kısa zoom yok; `cizim_uret.py`/`cizim_dogrula.py` renk/boya/resim, ZOOM_EN_AZ. Var olan derslerin sesi/çizimi yeniden üretilmedi (yeni derslerde geçerli). Commit/dağıtım yok.

- **Sesli ders ekranında okunuş sızıntısı (2026-10-28, H126):** `yazim_sozlugu.py` v2 `ses`↔`ekran` çiftlerinden gen sembolü yazımlarını çıkarır (hoks→HOX, paks altı→PAX6); sözlük yeniden üretildi, onem 520, dağıtıldı.

- **Belirti:** Ders ayrıntısında yalnız sesli ders/Öğren/çıkmış/yorum vardı; dersin terim, hastalık, spot, tablo, soru, kart içeriği ayrı sayfalarda yoktu.
- **Kök neden:** Ders paketi (taslak) üretilmişti ama ders sayfasına bağlanan ders-bazlı içerik katmanı yoktu.
- **Çözüm:** `scripts/ders_icerik_uret.py <kod> <key> <önem kodu> <önem dizini>` → `src/data/ders_icerik/<key>.json`; `DersIcerikV15.tsx` + `dersIcerik.ts` (`?b=terimler|hastaliklar|bilgiler|tablolar|sorular|kartlar`), `DersDetayV15` satırları paket varsa görünür. Yeni derse: betiği çalıştır, başka kod gerekmez.
- **Açık:** hasta/hastalık alanları yalnız taslakta dolu olanları gösterir; commit/dağıtım için `onem`+1 gerekir.

## 2026-10-27 · Ders içerik paketi 6 Kurul 2 dersine + sesli soru çözücü erişimi
- 6 dersin (k2-01,02,03,04,07,08) paketi `scripts/ders_icerik_uret.py` ile yayındaki deste/havuz/terim katmanından üretildi; kapı `ders_icerik_dogrula.py` (çözücü yoksa HATA). **k2-01'in Öğren destesi, havuzu ve çözücüsü yok → paketi yalnız terim/kısaltma; kapı HATA verir, tam içerik işçisi üretmeli.**
- Yeni sayfalar: Sıralamalar ve listeler (sıra türü numara/alfa/azalan/madde), Mini sorular; karşılaştırma tablosunda terazi simgesi.
- Sesli soru çözücü erişimi: ders ayrıntısı satırı, oynatıcıda "Önce soru çözücüyle dene" (başlamadan), ders bitince "Ders bitti" kartı (`cd:bitti` olayı, `dersCozucu.ts` başlık eşlemesi).
- Talimatlar: AGENTS kural 23, el kitabı §19 11a/11b, `docs/DERS_ICERIK_BICIMI.md`.
- Önleme: yeni dersin çözücüsü `src/data/k*_cozucu/index.json`'a, başlığı ders başlığıyla birebir, eklenmeden erişim satırı görünmez.

## 2026-10-27 · k2-01 Nörolojik Hastaya Yaklaşım — tam hat (AGENTS kural 22), yayında
- Katmanlar: Öğren destesi (14 slayt + oyun sayfası), 51 örnek soru (kaynak 9 slayt: standart 50–100'e giriyor), sözlük, hastalıklar, bilgi havuzu, ders içerik paketi (`ders_icerik_dogrula` 0 HATA), önem listesi 2n01 (24 madde), sesli çözücü 2n01 (23 soru, 207 EMA klibi GPU), sınav asistanı 2n01 (23 soru, 190 klip). Sesli ders/çıkmış/terim/kısaltma/çizim önceden vardı. Quiz envanteri: Farmakoloji dışı (kural 19) — atomik envanter paket.json'da.
- Denetim: yazar + 2 bağımsız denetçi; ikincisi slayt 1 klinik kararda **ters bayrak** buldu (H120) → düzeltildi, `validate_learning_decks.py` `klinik-karar-bayrak` kapısı eklendi.
- `birlestir.py`/`asistan_birlestir.py` 2n02'yi değiştiriyordu (kaynak çıkmışlar yok) → 2n02/2n03 dosyaları korundu, yalnız 2n01 + index girdileri alındı. Önleme: tek ders eklerken birleştiriciyi tüm dizinde çalıştırıp farkı kontrol et, değişen eski dersi geri yükle.
- Açık/küçük (denetçi GEÇER-dışı notlar): örnek soru Q14 A şıkkı (epilepsi) ayırt ediciliği, Q25 D/kuyruk cümleleri, asistan 2n01-01 cümle 2 ("lokalizasyon ve nedeni" öykü unsuru gibi okunuyor), paket `medicalTerms` slayt 7 piramidal/serebellar. Slayt dışı çeldirici (Guillain-Barré, Alzheimer, ALS) açıklamaları ders kitabı düzeyinde tek cümle.
- Saat kilidi (`nvidia-smi -lgc`) bu oturumda uygulanamadı (sudo); koruyucu etkindi.

## 2026-10-27 — Sınama dersi Öğren kitaplığında ayrıldı
- `LearnLibraryV12`: `sinama` işaretli desteler "Sınama — test verisi" bölümüne taşındı (en sonda). `ornek_sorular/k2/index.json` k2-07 girdisine `sinama:true`. Dağıtılmadı (onem artmadı); `vite build` yapıldı.

## 2026-10-28 · Özel sohbet ayarları (paylaşım, bildirim, durum, ATP temaları) — yerel; commit/dağıtım yok
- **İstek:** özel sohbete paylaşım (sayfa, soru, favori, çıkmış soru, terim), anlık bildirim, son görülme/çevrimiçi/okunma saati ve ATP ile açılan 3 arka plan.
- **Sunucu** (`toplulukSohbet.ts`, `deploy/pg/sql/topluluk_sohbet.sql`): `topluluk_mesajlar.ek` (jsonb; `ekTemizle` yalnız uygulama içi `/…` adres kabul eder), `sohbet_uyeleri.okundu_zaman/sessiz/tema`, `sohbet_durum` (son görülme, `gizli` karşılıklı). Yeni uçlar: `POST /sohbet/nabiz`, `/sohbet/ayar`, `/sohbet/:id/ayar`. Mesajda diğer üyelere `notifyStudent` (dakikada tek, sessiz mod hariç). `okundu` yalnız işaret ilerlerse yayın yapar (yayın döngüsü olmasın).
- **Tema kilidi:** `tanim.json` › kilitler `sohbet_tema_kalp/tibbi/papatya` (tur `icerik`, 150/200/150 mol); sunucu tema kaydında `basarimMotor.kilitAcikMi` ister. **Oracle'da `data/basarim/tanim.json` üst katmanı varsa bu üç kilit oraya da eklenmeli**, yoksa tema "kilit yok" sayılıp bedava açılır.
- **Ön yüz:** `SohbetEkleri.tsx` (paylaşım paneli/kartı, tema seçici, `SohbetZemin` SVG desenleri; renkler paletin `--color-accent` belirteçlerinden), `ToplulukV15.tsx`, `styles/v15/sohbet-ayar.css`.
- **Açık:** `onem` 509 yapıldı; Oracle’da tanim.json üst katmanı YOK (src sürümü kullanılır); sunucu kodu değiştiği için `systemctl --user restart meds-web` gerekir; girişli tarayıcı sınaması yapılamadı.

## 2026-10-28 — Önbellek sınıfları + açılış hızlandırma
- sw.js v17: kalıcı sınıflı önbellekler `medsor-tasarim-v1` (CSS, yazı tipi, ikon, görsel, Google Fonts) ve `medsor-kod-v1` (JS parçaları, pdf.js). SW sürümü artınca silinmez; özetli adres değişince (yalnız o dosya değişince) yenilenir; etkinleşmede `cevrimdisi-manifest.json`'da olmayan /assets/ kayıtları budanır. Veri (`medsoru-data-*`) ve kabuk (`medsoru-static-*`) ayrı kalır.
- Kök neden (yavaş açılış): her SW sürümü/UpdatePrompt tüm runtime önbelleğini (CSS+JS+yazı tipi) siliyordu → her güncellemede tasarım baştan iniyordu.
- server.ts: kabuk ve dist JSON'ları `no-store` yerine `no-cache` (ETag/304); surum.json ve manifest yanlışlıkla 1 yıl önbellekleniyordu.
- Lottie: 8 animasyon JSON'u statik içe aktarılıyordu (açılışta 353 KB) → isteğe bağlı dinamik içe aktarma (1,5 KB).
- Doğrulanmadı: SW önbellek davranışı tarayıcı panelinde (SW kaydı ortamda reddedildi); canlıda bakılmalı.

## 2026-10-28 — Yıldızlı paragraflar (H127)
- Bugün sayfasına gruplu yıldızlı paragraflar bölümü; sesli derste "Bu ders" kapsamı; silme mezar taşı + en yeni kazanır birleştirmesi (userKvSync, whatsappService süzgeci).

## 2026-10-28 — H431 Kişi Etkinlik sekmesi
- `peopleInsights.ts` `/olaylar` uç noktası sayfa ziyaretlerini (`kv.medsoru_etkinlik_v1`) birleştirir; kök neden ve kural `KURUL2_YAPILMAYACAK_HATALAR.md` H431. onem +1, dağıtıldı.

## 2026-10-29 — Patoloji hocası soru mantığı analizi + Patoloji Soru İşçisi (yerel; commit/dağıtım yok)
- **İstek:** Kurul 1 2026-27 patoloji sınavı yeni/zor kalıpla geldi; hocanın seçim mantığı Kurul 2+ vurgu/örnek soru/çıkabilecek soru üretimine bağlansın.
- **Analiz:** `docs/PATOLOJI_HOCA_SORU_MANTIGI.md` (34 soru; 4'ü toplanmadı, 9'u kısmi — küçük örneklem uyarısı). Ana bulgular: genişlik (26 derse ~1'er soru), bileşik şık %14→%40, "en tipik/en olası" kökü %12→%45, tek geçen ad/eponim ters sorma, çeldirici = aynı dersin komşu kavramları. Slayt biçimi zayıf sinyal: kırmızı satırların %42'si (cevap satırlarında %62), sarı dolgu cevap satırlarında seyrek (%5), başlıktan soru çıkmadı.
- **İşçi:** `scripts/patoloji_soru_isci/` — `hazirla.py` (önem adayı + çeldirici havuzu, LLM yok), `dogrula.py` (≥2 soru/önem noktası, farklı kalıp, komşu-kavram çeldirici, ipucu sızıntısı kapısı), `profil.json`, `TALIMAT.md` (yazar+denetçi akışı). LLM adımı yalnız elle komutla (kural 20).
- **Açık:** henüz hiçbir Kurul 2 patoloji dersi için soru üretilmedi (kullanıcı komutu bekliyor); Kurul 2 çıkmışı gelince profil yeniden hesaplanmalı; 58/62/65/66 numaralı soruların metni toplanırsa analiz güncellenmeli.

## 2026-10-29 (2) — Patoloji hoca mantığı v2 + Kurul 2 ilk hoca-üslubu sorular (yerel; commit/dağıtım yok, UI'ya bağlanmadı)
- **Derin analiz:** 35 PDF biçim işaretli döküm (`scripts/patoloji_soru_isci/dokum.py`), 30 sorunun her biri için 4 ajanla kaynak slayt/dönüşüm/eski çıkmış ilişkisi (`docs/PATOLOJI_SORU_ESLEME_TABLOSU.md`). v1 düzeltildi: sarı dolgu satırlarının %72'si kısa yapı etiketi ("Ancak:/İstisna:/Sonuç:/Not:"), soru etiketin ALTINDAKİ satırdan çıkıyor; kalın/`***`/tekrar güçlü sinyal; hoca 3 dönüşüm kullanıyor (kopya+çevirme, birleştirme, ters yön/ad); 5/30 soru slayt dışı çıkarım içeriyor; her derse ~1 soru.
- **İşçi güncellendi:** `hazirla.py` (etiket altı, tekrar, `***`, üç biçim), `dogrula.py` (açıklama sonu kalıp tekrarı kapısı), `profil.json` (ters_yon, yanlis_bul), `TALIMAT.md`.
- **Üretim:** `src/data/hoca_uslubu_sorular/k2/` — k2-03: 12 önem noktası/24 soru, k2-04: 13 nokta/27 soru. Yazar + 2 tur bağımsız denetçi; ikinci tur sonrası düzeltmeler yalnız kapılardan geçti (üçüncü denetim yok).
- **Kurallar bağlandı:** AGENTS.md kural 25, `docs/SORU_USLUBU.md` Patoloji bölümü (kural_secici ornek_soru aşaması okur), el kitabı 11c.
- **Açık:** bu sorular henüz sitede/Öğren'de gösterilmiyor (ekran bağlantısı yok); dagıtım yok. Kalan Kurul 2 patoloji dersleri PDF'i gelince aynı akış çalıştırılır. `soru_uslup.py` bu şemayla uyumsuz (107 HATA) — bu katman için çalıştırılmadı.

## 2026-10-29 (3) — Hoca üslubu sorular Örnek sorular ekranına bağlandı (yerel; commit/dağıtım yok)
- `KazanimSorulariView.tsx`: `src/data/hoca_uslubu_sorular/k<N>/<ders>.json` dosyaları derse sentetik son kazanım olarak ("Hoca", no 900, "Hocanın üslubunda çıkabilecek sorular") eklenir; soru kimliği `<k2-NN>-qhNN` (ilerleme sayacı `-q` önekiyle sayar); ders listesi soru sayısına eklenir; "K900" yerine "Hoca üslubu" gösterilir. `tsc` 0 hata, `vite build` tamam; yerel 3000'de k2-04 (12+27=39 soru) çözme kipinde doğrulandı. Yalnız ön yüz: sunucu yeniden başlatma gerekmedi.
- **Açık:** dağıtım yok (onem artmadı); k2-03 aynı yolla görünür (ekranda ayrıca açılmadı); ders işçisinin canlı içerik yolu (`/api/content/ornek`) hoca katmanını bilmez, ders canlı içerikle değişirse katman istemcide yine eklenir.

## 2026-10-29 (4) — Hoca üslubu soruları görünür yapıldı (kullanıcı "göremedim" dedi)
- **Belirti:** canlıda "Hoca" etiketli sorular fark edilmedi. **Kök neden:** grup dersin en sonuna (K1–K3'ten sonra) eklenmişti ve ders kartında hiçbir ipucu yoktu; sayılar doğruydu (k2-04 39 soru) ama etiket yalnız ders içinde küçük rozetti. **Çözüm:** `KazanimSorulariView.tsx` — grup en üste, kartta "Hoca üslubu · N yeni soru", kazanım sayısına +1. **Önleme:** yeni içerik katmanı eklenince ders kartında ve ders içinde ilk görünümde işaretlenir.

## 2026-10-29 (5) — Hoca üslubu sorular ders sayfasının "içerikler" bölümüne (kullanıcı bildirdi)
- **Belirti:** sesli ders/ders sayfasında "Bu dersin içerikleri › Soru çöz › Örnek sorular" içinde hoca soruları yoktu; kart sayı bile göstermiyordu. **Kök neden:** hoca katmanını yalnız `KazanimSorulariView` (Örnek sorular ekranı) okuyordu; ders sayfası ayrı yoldan (`dersIcerik.ts › dersSorulariGetir`, `DersIcerikV15`, `DersDetayV15`) örnek soru okur. **Çözüm:** `dersSorulariGetir` hoca kazanımını (no 900, "Hoca") en üste ekler, `Soru` şık şık açıklama gösterir, içerik kartı "N hoca üslubu" yazar (`hocaSoruSayisi`). **Önleme:** yeni soru katmanı eklenince örnek sorunun TÜM okuma yolları (Örnek sorular ekranı + ders sayfası içerikleri + çözücü) kontrol edilir.

## 2026-10-29 (6) — Ayrı "Hoca soruları" kartı + Sesli hoca çözücü (EMA, GPU) — kullanıcı isteği
- **İstek:** ders sayfası "Bu dersin içerikleri" ekranından hoca soruları ayrı ulaşılsın; sesli çözücü + EMA sesi GPU'da.
- **Yapılan:** "Örnek sorular"dan ayrıldı; kartlar "Hoca soruları" (`?b=hoca`, `hocaSorulariGetir`) ve "Sesli hoca çözücü" (`dersHocaCozucu`, branş `k2patolojihoca`, kod 2h01/2h02; `brans.ts` SLUG_AD adı). Çözücü hattı `scripts/patoloji_soru_isci/cozucu_kur.py` (iskele → TALIMAT_COZUCU yazımı → dogrula → birlestir). EMA klipleri GPU'da üretildi (`cozucu_ses_gpu.sh … ses.py --brans k2patolojihoca`; 459 klip ≈ 1 dk; kart 77 °C'ye çıktı, koruyucu etkindi). 51 soru, bağımsız denetimde 24 KALIR → düzeltildi (ipucu sızıntısı 14, ders dışı bilgi, bozuk kelime).
- **Hata (kök neden):** yazar betiği "şık" → "seçenek" değiştirirken "yaklaşık" içindeki "şık"ı da bozmuştu ("yaklaseçenek"); sözcük sınırı olmadan toplu değiştirme yapılmaz — kapıya eklenmedi, bağımsız denetçi yakaladı. **Önleme:** metin dönüştüren betiklerde `\b` sözcük sınırı + sonrasında bozuk kelime taraması.
- **Not:** ders kodu `<kurul>h<sıra>` (2h01…) — normal patoloji çözücü kodlarıyla (2p01) karışmaz, ilerleme ayrı.
