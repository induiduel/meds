## 2026-11-06 (5) — Ara resim kullanıcı tercihi (onem 656)
- `CdTerimKatman.tsx` PDF_GORUNUM'a `araResim` katmanı (`cd-pdf-araResim`, varsayılan açık); `CdV15` Görünüm › PDF katmanları satırı; `CdAraResim` kapalıyken kart açılmaz (galeri düğmesi kalır).

## 2026-11-06 (4) — PDF iki parmak kıstırma + kalıcı yakınlık (onem 655)
- `PdfDocView.tsx`: dokunmatik iki parmak kıstırma (hareket sırasında CSS ölçek önizlemesi, parmak kalkınca tek `onZoom`), iOS `gesture*` engeli; `pdfDoc.css` `.pdv { touch-action: pan-x pan-y }`.
- `CanliDersDers.tsx` `CdPdfBolme`: yakınlık `medsoru_cd_pdf_zoom_{genislik|sayfa}` anahtarında kalıcı.

## 2026-11-06 (3) — Sesli ders altyazı modu + ara soru otomatik çöz düğmesi (onem 654)
- `CanliDersDers.tsx`: Slayt + altyazı modunda `CdPdfBolme sigdir` → `PdfDocView fit="page"` (genişliğe sığınca slaytın altı kesiliyordu); altyazı şeridi en çok 22vh.
- `CdHocaAra.tsx`: "Otomatik çöz" onay kutusu (`medsoru_hoca_ara_coz_v1`, varsayılan açık); kapalıyken okuma sonrası geri sayım durur, öğrenci şık seçer ya da "Çözümü göster"e basar; düşünme sırasında açılırsa hemen çözer.

## 2026-11-06 (2) — iPad pencere kipinde geri dönüş (H502, onem 653)
- `components/shell/ipadPencere.tsx`: iPad pencere/bölünmüş ekran algısı (`:root[data-pencere='dar']`, üst çubuk 84 px sağa), alt yüzen geri hapı,
  sol kenar kaydırması + Esc/⌘[/Alt+←, yedek yollar 2 kez kullanılırsa hap cihazda kalıcı (`medsoru_ipad_geri_hap`). `ShellV15`: başlık = geri düğmesi.
- Arzu katmanı: bir kerelik "sürprizler açık kalsın mı" sorusu (`arzu/ArzuSoru.tsx`, `medsoru_arzu_soru_v1`, yöneticide sorulmaz). Sürüm notunda anılmaz.

## 2026-11-06 (1) — KMB 01 hoca kaydına göre tam denetim (H501)
- Kayıt large-v3 ile yeniden döküldü (`meds_temp/kmb/kaynak/nazogastrik_metin_l3.txt`); tüm anlatım, notlar, akış, vakalar, hedef kartları satır satır kıyaslandı (cümle sayıları korunarak): "kostik" terimi, sınav biçimi (malzeme seçtirme + basamaklar, 34:03), ölçüm son noktası "epigastrium (ksifoid hizası)", ölçümde "en sık hata" iddiası kaldırıldı (32:49), septum deviasyonu yaşlılarda, yutkunmada yarımşar mL su, idrar torbası, kayıtta olmayan iddialar çıkarıldı. Vazelin kullanıcı kararıyla "zor durumda az" (sarı, çarpı yok). 27 klip yeniden seslendirildi, 19 video yeniden üretildi, kapılar 0 HATA.
- `hoca_dokum_gpu.sh` ek argümanları aktarır (H501).

## 2026-11-05 (2) — KMB 01 Nazogastrik sonda dersi (H497–H500)
- Kaynak: hoca ses kaydı (Drive, 37 dk; GPU dökümü `meds_temp/kmb/kaynak/nazogastrik_dokum.json`) + TIS301.43.1 föyü. İçerik `src/data/kmb/01.json` (kurucu `meds_temp/kmb/ng/ders_kur.py`): 19 adım / 99 cümle, 14 föy hedefi kartı (6 vuruşlu film), 2 OSCE akışı (takma + dal "ses var/yok", çıkarma), 11 vaka (6'sı kime takılır/takılmaz), 5 "sahnede bul". Hoca sınav vurguları: kontrendikasyonlar (yüz/kafa tabanı kırığı, koroziv, bilinci kapalı + hava yolu korunmamış, özofagus varisi), ölçüm burun–kulak memesi–ksifoid, aniden hava + epigastrium dinleme. Bağımsız denetçi DÜZELTİLMELİ → 16 düzeltme uygulandı.
- 6 yeni 2B sahne (`sahneler_ng_a/b/c.tsx`: ng-kesit, ng-burun, ng-govde, ng-mide, ng-malzeme, ng-pozisyon; sözleşme `meds_temp/kmb/ng/SAHNE_SOZLESMESI.md`), 19 adım videosu (`scripts/kmb/lottie2b/adim2b_ng1/2/3.py`, öneki `ng-`), EMA 123 klip GPU'da (`data/kmb_cozucu/ses/01`, git dışı → Oracle rsync).
- Hat çok derse açıldı: `adim2b.py --kod=`, `ses.py`/`dogrula.py` 01 için `lottie2b` + `ng-` öneki, `uret2b.py` ses_01, `LottieVideo.LOTTILER` yalnız-2B videoları da alır, `svg_lottie.ON_EK` ng sahneleri.
- Kök neden düzeltmeleri: H497 `lottie_dsl.yol` çok alt yol (çarpı "Z" çiziyordu; 02 videoları yeniden üretildi), H498 bbox ata transform (`svg_disa.mjs`, `HedefFilmi.tsx`), H499 clipPath'li sıvı, H500 altyazı bandı (kesit 70 px yukarı).
- Kapı `dogrula.py 01` ve `02` 0 HATA; 19 videoda `kare_onizle` 0 otomatik bulgu + kare kare göz denetimi.

## 2026-11-05 (1) — Arayüz denetimi aşama 2–3: kaydırma kilidi, klavye, kesme noktası, Esc (H494–H496, dağıtılmadı)
- H494: 16 bileşen doğrudan `body.style.overflow` yazıyordu → sayaçlı `lockScroll/unlockScroll` (DraftDeduplicationModal, QuickAddHero, ContributeModal, AdminPanelModal, TopluPdf, PdfStudio, kmb/DersVideo, HedefFilmi, HikayeFilmi, KazanimSorulariView, SearchPalette, CanliDersView, LearnReview, AnnotationWorkspace, LessonPlayer, SpotsSureDiyalog).
- H495: çekmece/pencere eşiği 640 → 768 (`shell.css` + `Sheet.tsx`); klavyede `.pa.is-tam`, `.kr15e-arka`, `.teg-perde`, `.pt-pop`, `.sh-pop` görünür alana uyar (`katman-duzeni.css`); `.ms-chat-shell` 768+ zoom bölmesi; UpdatePrompt Esc belge düzeyinde.
- H496: sözlük bağlantısının dokunma alanı.
- Bilinçli bırakılan: `.teg` (tam ekran adası) tam ekran katmanların üstünde kalmalı; spot süre/istatistik modalları içinden diyalog açılmıyor.
- Hız ölçümü (4× CPU): `/sozluk` 0,66 sn; `/cikmis` sıcak 1,8 sn, soğuk 5,8 sn (ilk kez ~40 MB indirme, işçide; cihaz başına bir kez). Ayrı iş adayı: ince liste kaydı + ayrıntının tembel yüklenmesi.
- KMB (onem 647): `.kmb-serit` adım şeridinin `::before` dokunma alanı (−10 px) `overflow-x:auto` kabında kırpılıyordu (gerçek hedef ~16 px); dolgu 10 px + `margin-block:-6px`, görünüm aynı.
- Doğrulama: `tsc` bu dosyalarda temiz, `vite build` temiz, 10 sayfa × 4 görünüm taramasında taşma/hata yok. Klavye ve çekmece davranışı gerçek cihazda sınanmadı. Commit/dağıtım yok.

## 2026-11-04 (6) — Arayüz denetimi aşama 1: katman, klavye, dokunma (H491–H493, dağıtılmadı)
- Tarama: 20 sayfa × 7 görünüm (`sayfa_tarama.mjs`, başarım penceresi kapatılarak) + stil kodu katman/klavye denetimi. Bulgular ve sıradaki aşamalar: canvas https://claude.ai/artifact/VVyP72D9Bf6AwqbcQKLVnv
- Düzeltildi: başarım penceresi kesilmesi (H491), katman sırası + klavyede alt öğeler + dokunmatikte gizli denetimler + mini oynatıcı değişken adı (H492, yeni `src/styles/katman-duzeni.css`), Soru çöz özet kartı kesilmesi (H493).
- Açık (aşama 2–3): `.teg` katman çakışması, spot katmanları, Esc eksikleri, kaydırma kilidi sıfırlama, `100dvh` katmanlar, 640/768 kesme noktası farkı, `/cikmis` ve `/sozluk` açılış hızı.
- `npx vite build` temiz; commit/dağıtım yapılmadı.

## 2026-11-04 (5) — Sesli ders yerel ilerlemesini sıfırlama / temizleme (onem 643)
- Kullanıcı isteği: öğrenci sesli derslerde cihazındaki ilerlemeyi dilediği gibi sıfırlayıp yeniden çalışabilsin. Yalnız yerel kayıtlar: "kaldığın yer" (`medsoru_canli_ders_konum_v1`) ve çalışma takibi (`medsoru_calisma_takip_v1`: süre, bitti işareti, tekrar turu). Ses dosyaları, indirilenler, listem ve ayarlara dokunulmaz.
- Yeni `src/components/canliDers/CdIlerlemeTemizle.tsx`: `SifirlaDugme` (tek ders, iki adımlı onay, 6 sn'de kendiliğinden vazgeçer) ve `TemizleDiyalog` (görünen listenin dersleri için toplu; "kaldığın yer" ve "bitti + süre" ayrı onay kutuları, sayılarıyla; sonuç satırı). Yerler: v15 sesli ders listesi altı ("İlerlemeyi temizle"), v15 ders ayrıntısı kaldığın yer kartı ("İlerlemeyi sıfırla", kayıt yoksa gizli), klasik liste kenar çubuğu "Temizlik" + satır seçenekleri.
- Servis: `calismaTakip.ts` `konuSifirla(m, konu)` + `modulSifirla(m, konular?)`; `canliDersStore.ts` `cdKonumSil(key)` + `cdKonumlariTemizle(keys?)` (yüklü ders sıfırlanırsa ses durur ve başa alınır ki konum yeniden yazılmasın) + `CD_KONUM_OLAY` ('cd:konum'). `useCdKonumSurum()` ile `useIlerleme` (dersVeri.ts), `DersDetayV15` ve `CanliDersView` konum haritasını olayla yeniler (eskiden tek seferlik `useState` idi: silince ekran güncellenmiyordu).
- Sınama: localhost tarayıcı (masaüstü + 375 px): toplu temizlik 2 konum + 2 takip kaydını sildi, "1/35 bitti" → "0/35", ders ayrıntısı "Kaldığın yer 10:00" → "Henüz başlamadın" / "Sesli dersi başlat"; konsol hatası yok. Telefonda diyalog eylem satırı sekme çubuğunun altında kalıyordu → `--sh-tabs-h` kadar alt boşluk. Commit + dagit.sh ile dağıtıldı (onem 643).

## 2026-11-04 (5) — Diyalog açılırken titreme / ileri-geri zıplama (H490, onem 642)
- Belirti (kullanıcı): diyalog açılırken diyalog ya da arkadaki ekran "flashback gibi" git-gel yapıyor. Başsız Chrome'da (masaüstü + telefon, 7 senaryo: arama, kurul çipi, hesap menüsü, bildirim, kronometre, kart menüsü → Hakkında penceresi, ayarlar) kare kare kayıt (`scratchpad/film.mjs` + PIL kare farkı) ve kare başına yerleşim ölçümü (`titre.mjs`) ile **yeniden üretilemedi**; sayfa kayması, scroll sıçraması ya da geri dönüş deseni yok.
- Kök neden adayı (kod incelemesi, en güçlü): `main.tsx` görsel alan izleyicisi `--vvh/--vvt`'yi klavye kapalıyken de her karede yazıyordu; iOS/Android'de adres çubuğu açılıp kapanırken, sıçramalı kaydırmada ve yakınlaştırmada görsel alan sürekli değişir. Pencere (`.ms-overlay`), alt sayfa (`.sh-sheet`), arama, ders ve çözücü katmanlarının yüksekliği/konumu bu değişkenlere bağlı olduğundan diyalog açılır açılmaz (kilit → belge yüksekliği değişir → çubuk hareket eder) katman birkaç kez yukarı-aşağı zıplıyordu. Değişkenler artık yalnız bir yazı alanı odaktayken (klavye olasılığı) yazılır; odak yokken kaldırılır → katmanlar `100dvh`/`0px` yerleşim alanını kullanır (tarayıcı araç çubuğunu kendisi hesaba katar).
- Ek sertleştirme: `Dialog.tsx` kaydırma kilidi `useLayoutEffect`'e (Sheet ile aynı; masaüstünde kaydırma çubuğu bir kare sonra kalkınca sayfa kayıyordu), odak `preventScroll`; `ConfirmDialog` odak `preventScroll`; `QuickAddHero` tembel `AiQuestionOptimizerModal` kendi `React.Suspense` sınırına alındı (sayfa düzeyi Suspense'e düşünce tüm sayfa iskelete dönüp geri geliyordu — "flashback" deseni; diğer tembel pencereler zaten sarılıydı).
- Kullanıcıdan beklenen: hangi cihaz/tarayıcı ve hangi diyalogda sürdüğü; sürerse kayıt aracı o senaryoyla koşulur.

## 2026-11-04 (4) — Açılış ve geçiş hızı + tasarım hataları (H484–H489, onem 640)
- Ölçüm (4× CPU yavaşlatma, `scripts/perf/yukleme_olcum.mjs` artık `AI_COOKIE` ile zorunlu girişi geçer; soğuk açılış `acilis.mjs` ve splash ölçümü oturum geçici klasöründe): soğuk açılış 99 betik / 524 KB gz, hazır 2,4 sn; sıcak 1,5 sn (betik isteği yok, süre ayrıştırma/çalıştırma). Geçişler: /cikmis 8,6 sn (IndexedDB getAll 1,5 sn + arama alanı katlama 0,7 sn + GC), /sozluk 2,1 sn (3,4 MB ansiklopedi parçası ayrıştırma), diğer merkez sayfaları 0,6–1,6 sn.
- **H484 (kök neden: splash her yeni sekmede ≥5 sn zorunlu bekliyordu, `sessionStorage`):** `App.tsx` — gösteri yalnız günün ilk açılışında ve en çok 1,8 sn (`localStorage medsoru_splash_gun`), sonraki açılışlarda uygulama hazır olunca hemen kalkar; Klasik (v10) eski davranışı korur. Ölçüm: ilk açılış 2,9 sn (önce ≥5), sonrakiler 1,65 sn (uygulamanın hazır olma süresi).
- **H485:** kök adres `/` öğrenciye gizli "Soru ekle"ye düşüyor, açılış "Bu sayfa şu an kapalı" ekranıyla başlıyordu → kapalıysa Bugün'e geçer (`replaceState`, geçmişe kayıt yok); adresle girilen diğer gizli sayfalar H139 gereği ekranda kalır.
- **H486:** v15 jetonları `'Plus Jakarta Sans'` / `'Newsreader'` istiyordu, hiçbir yerde yüklenmiyordu (index.html yalnız Geist/Bricolage/Literata/JetBrains Mono indirir); tarayıcı sessizce Geist/Literata'ya düşüyordu → jetonlar yüklenen yazı tiplerini adlandırır (görünüm değişmedi, tasarım–kod uyumsuzluğu kalktı).
- **H487:** küçük dokunma hedefleri (tarama `sayfa_tarama.mjs`): "Kurul 1 derslerine geç" 150×19, üst çubuk kırıntısı "Soru çöz" 67×16, İstatistik "Tümünü aç" 86×19 → satır içi dolgu / telafili dolgu, görünüm aynı, tarama 0 küçük hedef.
- **H488:** 600–959 px kapsayıcıda (tablet 820, yarım ekran) Soru çöz özet kartları tek satır düzeninde taşıyordu (sayı kesik, "Karma test · 20 soru" kart dışına) → bu aralıkta kısa düğme adı (`.s15-kisa`) + dar dolgu (`dersler.css`).
- **H489:** telefonda üst başlık `overflow-wrap: break-word` ile tek kelimeyi hece ortasından bölüyordu ("İstatistikleri|m") → `normal` + kırpma (`shell.css`).
- Yapılmayan / aday: `/cikmis` açılışında 4.700 zengin kaydın IndexedDB'den okunması ana iş parçacığında ~1,5 sn (4×); liste için ince kayıt + ayrıntıyı açınca yükleme ayrı iş. `/sozluk` 3,4 MB veri parçası yerine JSON getirme ayrı iş. Rolldown `codeSplitting.minSize` ile parça birleştirme denenmedi (sıcak açılış istek değil ayrıştırma ağırlıklı).

## 2026-11-04 (3) — Çevrimdışı eksik giderici (H483)
- Yeni `src/services/cevrimdisi/eksikGider.ts` (açılışta + 'Eksikleri tamamla' düğmesi), `paketiDenetle` sesli derste PDF/eşleme sayar. Uçtan uca sınandı; dağıtıldı.

## 2026-11-04 (2) — İnternetsiz sesli derste PDF/slayt/çizim (H482)
- `sw.js` `ARAMA_SIRASI`: sesli ders ve eski PDF önbellekleri eklendi (toplu indirmenin pdf.js yardımcıları bulunamıyordu). Uçtan uca internetsiz sınama geçti; dağıtıldı.

## 2026-11-04 — Çevrimdışı ders PDF'leri internetsiz açılmıyordu (H481, dağıtıldı onem 637)
- `public/sw.js`: H63'ün `/api/lecture-pdf/` kısa devresi sesli ders (`medsoru-canli-ders-offline`) ve eski PDF indirme (`medsoru-pdf-offline`) önbelleklerini atlıyordu. Artık bu adresler kümede (`cihazPdfYukle`/`cihazPdfYaniti`) tutulup cihazdan (Range → 206) veriliyor; olmayan ağa bırakılır.
- `canliDersCevrimdisi.ts` ve `deviceStorage.ts::savePdfOffline` kayıttan sonra SW'ye `PAKET_CHANGED` gönderir. Sınama: headless Chrome internetsiz → 200 + 206. Commit/dağıtım yapılmadı.

## 2026-11-03 (3) — Arzu katmanı yöneticiye de açık (onem 635)
- `arzuKimlik.ts` izin listesine `ADMIN_EMAIL` eklendi: yönetici hesabı da karşılama/yaratık/kalp katmanını görür (kullanıcı kararı). Sürüm notu değişmedi.

## 2026-11-03 (2) — Arzu katmanı: yeni easter egg'ler, tek yaratık kuralı, tavşan (onem 632; sürüm notunda ANILMAZ)
- Yeni: `KucukDokunuslar.tsx` (boş yere çift dokunma → kalp; uzun sayfa sonunda "Buraya kadar okudun"; 11:11/22:22 notu; 40 dk aralıksız → mola tilkisi + not; sekme gizlenince başlık "Tilki seni bekliyor"), `Yoldas.tsx` (gece 23–05 uyuyan tilki "z z z", dokununca uyanır; koşan tilkiye ikinci dokunuş → 5 dk yanında kalan tilki), `ozelGunler.ts` (14 Şubat + doldurulacak doğum günü/yıl dönümü satırları → karşılamada özel cümle + kalp yağmuru), tilki patileri (`.ar-pati`).
- Kullanıcı kararı: yaratıklar aynı anda görünmez → `GezinenTilki.tsx` tek yaratık kuyruğu (geçit sırayla), yoldaş açıkken bekler (`arzu:yoldas-durum`); "selam" kipi: kenardan hızla gelir, pati sallar ("Selam!"), kaçar; tavşan eklendi (`TavsanZiplayan`, zıplama/kulak/arka ayak animasyonu, durup burun oynatma), klavye "tavsan".
- Çizim denetimi: `scripts/arzu/cizim_onizle.tsx` (çizimleri büyük boyutta statik HTML'e basar). Tilkinin yakın ön bacağı DOM'da başın önüne alındı (selamda pati yüzü kapatmasın). Kullanıcı `mesajlar.ts`'teki dört cümleyi kendi sözleriyle değiştirdi (korundu).

## 2026-11-03 — Arzu'ya özel katman: karşılama, gezinen tilki, kalpler, Kitty & Batman (onem 630; sürüm notunda ANILMAZ)
- Kullanıcı isteği: Arzu hesabına (arzuturk361@gmail.com / drarzuturk@gmail.com, uid'ler `arzuKimlik.ts`) özel, tilkili-kalpli sürpriz katmanı; güncelleme notunda yazılmaz (sürpriz). Başka hiçbir kullanıcı için parça yüklenmez (`App.tsx` → `arzuMu(currentUser)` + tembel `ArzuKatmani`).
- `src/components/arzu/`: `cizimler.tsx` (elle SVG: yürüyen tilki 4 eklemli bacak, oturan kalpli tilki, Kitty & Batman çifti, asılı kalp, sekme simgesi), `ArzuKarsilama.tsx` (günde bir kez, girişten 35 sn sonra; başka diyalog açıksa bekler; `medsoru_arzu_karsilama_v1`), `GezinenTilki.tsx` (WAAPI koşu, koklama durağı, dokununca kalp + balon; `arzu:tilki` geçidi), `KalpAskisi.tsx` (sarkaç; dokun → patlama + not; 3 dokunuş/uzun basış → karşılama), `CiftGizli.tsx` (sağ alttan bakan çift), `Fisiltilar.tsx` (sayfa/saate göre sade notlar, `mesajlar.ts`), `KalpAvi.tsx` (saklı kalp, sayaç `medsoru_arzu_kalpler`, 1/5/10/25/50/100 notu), `sallama.ts` (telefonu sallayınca geçit, iOS izni ilk dokunuşta), `kalpPatlamasi.ts` (WAAPI parçacık + halka). Klavye: metin alanı dışında "arzu"/"tilki"/"kalp".
- Stil `src/styles/arzu.css` (katman sırası, koyu tema, `prefers-reduced-motion` → durağan, `hover` yalnız fareli cihazda, güvenli alan). Marka simgesine kalp rozeti (`:root[data-arzu]`).
- Tuzaklar: (1) SVG `transform` özniteliği olan gruba CSS animasyonu uygulanınca öznitelik ezilir (baş sol üste kaydı) → dış `translate` grubu + iç animasyon grubu, `transform-box: fill-box`. (2) v11 genel `[role=dialog]` `max-height` kuralı (özgüllük 0,3,0) tam ekran karşılamayı kısıp alt çubuğu gösterdi → `.ar-kars.ar-kars.ar-kars { max-height:none }`.
- Kullanıcı düzeltmeleri: klişe/abartılı sözler sadeleştirildi, imza ve "tıpkı bizim gibi" kaldırıldı. Sınama: 5175 önizleme, yapay zekâ test oturumu + `medsoru_arzu_onizleme=1`; masaüstü/telefon/koyu tema ekran görüntüleriyle.

## 2026-11-02 (2) — Yönetici onaylı şifre, öğrenci numarasıyla giriş, Drive ve SMTP sağlamlaştırma (H467, onem 618)
- Şifre talebi: `deploy/pg/sql/kimlik.sql` (`auth_sifre_talepleri`, `auth_hesaplar.ogrenci_no`), `yerelKimlik.ts` (`POST /api/kimlik/sifre-talebi`, `.../durum`; yönetici `GET /api/admin/kimlik/sifre-talepleri`, `POST .../karar`), istemci `SifreTalebi.tsx` + `auth.ts` (`sifreTalebiGonder/Durumu`, `medsoru_sifre_talebi_v1`), yönetim `manage16/sayfalar/SifreTalepleri.tsx` (menü Kullanıcılar › Şifre talepleri, SSE `sifre_talebi`, yöneticiye web push). Eski hesapla giriş/kayıt denemesi talep formunu açar; onaylanınca talep eden cihaz kendiliğinden girer (durum 20 sn'de bir sorulur).
- Giriş alanı "E-posta ya da öğrenci no" (öğrenci, eski kart, yönetim girişi). Kayıtta aynı öğrenci no ikinci hesaba verilmez.
- Drive (alt ajan denetimi): okul + öğrenci Drive'ı herkese açık yolla yerelde ve Oracle'da çalışıyor; servis hesabı askıdaki projede (`invalid_grant`), Oracle'da hiç bağlı değildi. `02-download.mjs`: `free_uc` ikinci yol, uuid onay sayfası, servis hesabı hatası bir kez günlükte. `DriveSaveModal` yalnız PDF indirme; App otomatik Drive yedeği kalktı, `medsoru_drive_token` silinir. `ogrenciDriveRoutes /indir` hedef yolu izinli köklerle sınırlı.
- SMTP (Site › Bildirim kanalları): servis seçimi kalktı (sunucu adı belirler), port değişince `secure` porttan, `POST /api/admin/smtp-test {yalnizBaglanti}` göndermeden sınar, Google dışı hazır sağlayıcılar (Brevo, Resend, Mailjet, Zoho) + Gmail uyarısı; Google'a özgü hata metinleri genelleştirildi.
- Eski konsol metinleri: tanılama penceresi, eski yönetim paneli, alt ajan izleyici, çıkmış içe aktarıcı, v12/v14 sağlık satırlarından Firebase kartı/kip/aktarma bölümleri kaldırıldı; `multiDbManager` 'firebase' kipini kabul etmez; sağlık izleyici yalnız meds-pg'ye bakar.
- Sınama (yerel): curl ile talep → yanlış takip → onay öncesi giriş reddi → dışarıdan onay 403 → onay → ikinci onay 409 → cihaza tek seferlik oturum → e-posta ve öğrenci no ile giriş; tarayıcıda form → bekleme kartı → yönetici onayı → kendiliğinden giriş. tsc 0, vite build.
- Kullanıcıya kalan: Drive kimlikli yedeği (yeni GCP projesi + servis hesabı ya da `rclone config reconnect meds:`); `~/.config/rclone/rclone.conf` `client_id` alanında düz metin API anahtarı duruyor; iki `.env`'deki `GOOGLE_SERVICE_ACCOUNT_FILE` artık ölü.

## 2026-11-02 — Google/Firebase tamamen kaldırıldı: kendi kimlik sistemi (Oracle meds-pg) (H466, onem 617)
- Belirti: Google/Firebase projesi askıya alındı (`Consumer 'projects/990828780858' has been suspended`); giriş tamamen durdu, zorunlu giriş kapısı yüzünden site kullanılamadı. Veri zaten meds-pg'deydi; tek bağımlılık kimlikti (+ sunucuda Firestore dinleyen köprü).
- Sunucu: `src/services/yerelKimlik.ts` (`/api/kimlik/{kayit,giris,yenile,cikis,kod-gonder,kod-dogrula,sifre,profil,ben}`, yönetici `/api/admin/kimlik/{hesaplar,sifirlama-kodu,oturumlari-kapat}`), şema `deploy/pg/sql/kimlik.sql` (açılışta uygulanır; `auth_hesaplar`/`auth_oturumlar`/`auth_kodlar`), `src/services/kimlikDogrulama.ts` (eski `firebaseIdentity.ts` yerine; HMAC-SHA256 erişim jetonu 1 sa, ağsız doğrulama; anahtar `MEDS_AUTH_SECRET` ya da `data/.kimlik_anahtari`). Yenileme jetonu 180 gün, özetiyle saklanır; "oturumları sonlandır" yenilemeyi de reddeder. scrypt şifre özeti; kod 6 hane/15 dk/5 deneme; hız sınırları.
- Göç: `users` + doğrulanmış `user_data` e-postaları **aynı uid** ile `auth_hesaplar`'a (`kaynak='firebase-gocu'`, şifresiz). Giriş/kayıt denemesi `kod: 'sifre-belirle'` döner, istemci kod akışını açar; kod doğrulanınca şifre kaydedilir, uid değişmediği için tüm veri (user_data, notlar, yedekler, başarım) yerinde. Tarayıcıdaki eski yerel veri `userScope` stash'iyle aynı uid'ye geri gelir.
- Kimlik e-postası: `epostaGonder` genel `smtp_config.enabled` kapalı olsa da kayıtlı SMTP bilgisiyle gönderir (Oracle'da genel e-posta 8 Ekim'den beri kapalı; o ayar değiştirilmedi). SMTP gitmezse yönetici Kullanıcılar › Erişim › "Şifre kodu üret" (24 sa) — yeni "Şifre" sütunu belirlenmiş/bekliyor gösterir.
- İstemci: `src/services/auth.ts` yeniden yazıldı (Firebase benzeri `auth` nesnesi; `onAuthStateChanged` dışa açık, `firebase/auth` içe aktarmaları kalktı). Giriş kartı (`UserAuthModal`, `AuthV12`): Google düğmeleri kalktı; `EpostaBaglantiGiris.tsx` artık e-posta kodu akışı (Şifremi unuttum / Şifre belirle, şifresiz kodla giriş). Yönetim girişi (`manage-main.tsx`) e-posta+şifre + kod. Profil şifre metni güncellendi. `AuthErrorModal` + `AuthErrorV12` (Firebase alan adı uyarısı) silindi. `adminFetchAuth` `/api/kimlik/*`'ye jeton eklemez (yenileme kendini beklerdi).
- Kaldırılan: `firebase` paketi, `firebase*.json`, `firestore.rules`, `cloudNotificationBridge.ts` (Firestore dinleyicisi), vite `firebase/firestore` takma adı ve `vendor-firebase` parçası, Google Drive'a otomatik yedek. Firebase'e yazan eski betikler `scripts/archive/`'e (sync-all-to-*, start-*-tunnel, process-scanned-ocr, download-and-process-kurul-notes, background-ai-redactor, build_full_drive_slides, check-online-status; `check:*` npm komutları silindi). `firestoreDb.ts`/`api.ts`/`driveAutomation.ts` eski çağrıları `firestoreKapali.ts` boş modülüne bağlı (bayrakla zaten kapalı).
- Sınama (yerel): curl ile kayıt/giriş/yanlış şifre/yenile/çıkış/sahte jeton/göç hesabı/kod (yanlış, doğru, tekrar)/yönetici ucu dışarıdan 403; tarayıcıda kayıt → giriş → yenileme sonrası oturum kalıcı, yedek/not/başarım/varlık uçları 200. `tsc` 0, `vite build` tamam. Firestore günlük satırı yeniden başlatmadan sonra 0.
- Kalan (Google'a bağlı ama zorunlu olmayan): Google Fonts yazı tipleri (hesapsız CDN), Drive içerik hattı (`drive.ts`, öğrenci Drive, `drive_yeni_pdf`) ve Gemini anahtarları (kural 20 kilidi) yerinde; Gmail SMTP (nofrostlife@gmail.com) kimlik kodları için kullanılıyor — Google dışı bir SMTP'ye geçmek yalnız `data/smtp_config.json` ayarıdır.

## 2026-11-01 — KMB: Lottie 2B hattı (30 video) + Hikâye filmi (eski hat korunur; canlıya gönderilmedi)
- Kullanıcı kararı: Lottie videoları da tam 2B çizgi film diline geçsin, ESKİSİ KORUNSUN; tüm videolar kazanım ve öğretici bulgularla tek hikâye gibi tam ekran oynasın.
- Yeni hat `scripts/kmb/lottie2b/`: `svg_disa.mjs` (2B SVG sahneleri + öge kutuları, başsız Chrome) → `svg_lottie.py` (SVG → Lottie katmanları: tüm yol komutları, dönüşümler, objectBoundingBox degradeler, gs degrade çizgi, evenodd, ok ucu, pathLength dasharray) → `sahne2b.py` (`Sahne2B`) + `ortak2b.py` (koreografi yardımcıları, `ic_ekle2b`, `adim`) → `uret2b.py`/`uret2b_a.py`/`uret2b_b.py` (12 konu videosu) ve `adim2b.py`/`adim2b_a/b/c.py` (18 adım videosu) → `src/data/kmb/lottie2b/` (index.json, adimlar.json). Anatomi/el/araç 2B sahnelerden gelir (tek kaynak); üreticiler yalnız koreografi. Bölüm metinleri eskiyle birebir (ses klipleri değişmedi). `lottie_dsl.ic_ekle(modul=…)`, `kare_onizle.mjs LOT=…`, `lottie2b/kare.mjs` tek kare aracı.
- Üretim 1 referans (erkek-ilerleyis) + 5 paralel alt ajan; her video `kare_onizle` 360 px'te 0 otomatik bulgu + göz denetimi (30/30), `dogrula.py` 0 HATA. Düzeltilen tuzaklar: degrade çizgi `gs` olmadan ön kol koyu çıkıyordu; `uret2b_a._son` alt kompozisyonda (Ic) bölüm listesi olmadığı için çöküyordu → harita uzunluğu.
- Oynatıcı `LottieVideo.tsx`: aynı ad için `lottie2b/` varsa 2B, yoksa eski; `localStorage.medsoru_kmb_lottie_eski='1'` eski hattı zorlar. Eski üreticiler/çıktılar silinmedi.
- Yeni `HikayeFilmi.tsx` (+ `kmb.css .kmb-hk-*`, Öğret ve Videolar sekmelerinde "Hikâye filmi" düğmesi, `?hikaye=1`): açılış kartı (amaç + içindekiler) → her bölüm için kazanım kartı (hedef ilk geçtiği bölümde) → 2B adım videosu (EMA sesi) → öğretici bulgular (puf, dikkat, hedef kartının sık hatası) → bitişte 15 kazanım onay listesi; kartlar 6–14 sn geri sayım, video bitince otomatik geçiş, bölüm şeridi/klavye. Başsız Chrome'da masaüstü + 390 px sınandı, konsol hatasız.
- Belge: `docs/KMB_2B_STIL.md §4`, `KMB_GORSEL_ASISTAN.md` A8e. Commit edildi; kullanıcı onayıyla **canlıya dağıtıldı** (`dagit.sh`, sürüm 20261101021248, onem 616; yalnız ön yüz).

## 2026-11-01 — KMB: 2B düz çizgi film geçişi tamamlandı (14 SVG sahne + Lottie paleti; H465; canlıya gönderilmedi)
- Kullanıcı 2B stili onayladı, örnek karedeki mantık hatalarını bildirdi → **H465**: sırtüstü gövdede iç organlar "ayakta" dizilimindeydi. Erkek sahnesi tek yön sistemiyle (inferior = sağ, anterior = yukarı) yeniden kuruldu: simfiz derinin altında, mesane arka-üstte, prostat arkada, bulbar üretra perinede, penis eldivenli elle dik, skrotum kök arkasında, uyluk + örtü + küvet; idrar yalnız balon yerleşince akar.
- Kalan 13 sahne üç paralel alt ajanla sıfırdan çizildi: `sahneler_2b_a.tsx` (foley, foley-kesit, malzeme, maket), `sahneler_2b_b.tsx` (mesane, yakin-mesane, yakin-uretra, travma), `sahneler_2b_c.tsx` (kadin, yakin-kadin, yakin-erkek-jel, yakin-el, pozisyon). Ortak sözleşme `sahneOrtak.tsx` (tipler, `Ortak` degradeler + `kmb-2b-*` palet, `Boru`); `sahneler.tsx` yalnız Erkek + kayıt (eski gerçekçi çizimler kaldırıldı, 1269 → 233 satır). Öge kimlikleri/`gizli` semantiği değişmedi; `dogrula.py` MALZEMELER'i 2B dosyalarından da okur → 0 HATA.
- Stil ve doğruluk sözleşmesi: `docs/KMB_2B_STIL.md` (palet, kontur, 1 cm ≈ 12 px, H462 ①–⑦ + yön sistemi, kare denetimi komutları). Göz denetimi: her sahne `--goster --etiket` + gerçek vuruş kareleri (`sahne3b_onizle.mjs --film`, 90 kare temas sayfası `meds_temp/kmb/stil/film_sheet.png`); etiket çakışmaları, iç içe geçmeler ve örtülen ögeler düzeltildi (ilaç oku üretradan, levator/rektum sırası, travma kırık etiketi, meatus/jel etiketleri).
- Lottie (30 video): geometri doğru olduğundan korundu, palet 2B tonlarına alındı (`lottie_uret.py`, `adim_lottie.py`, `lottie_dsl.py`: deri, mesane, idrar, kemik, eldiven) ve videolar yeniden üretildi; `kare_onizle.mjs` 0 yeni bulgu (balon-sisme'deki 2 "10 mL altyazı bölgesi" bulgusu eskiden beri var).
- Commit edildi; kullanıcı onayıyla **canlıya dağıtıldı** (`dagit.sh`, sürüm 20261101011450, onem 615; yalnız ön yüz, sunucu yeniden başlatılmadı).

## 2026-11-01 — KMB: film yakınlaştırma düzeltmesi + 3B deneme ARŞİVE (H462–H464; canlıya gönderilmedi)
- `HedefFilmi`: yakınlaştırma ≤1,35 ve odak kutusu kadrajın en çok %70'i; veri zoom tavanı 1,35 (`dogrula.py` 1–1,4), vuruşlara isteğe bağlı `aci` (kamera açısı) alanı.
- 3B deneme (`components/kmb/sahne3b/`: `Sahne3B.tsx` motor, `yardimci.ts` malzeme/geometri/organik marching-cubes, `sahneler3b*.ts` 14 sahne; `SahneGoster` seçici; `scripts/kmb/sahne3b_onizle.mjs` başsız Chrome kare alıcı; `KmbAsistan` `?sahne=` önizleme rotası; `dogrula.py` 3B öge kapısı). Kullanıcı denetiminde kalite yetersiz bulundu (iç içe geçme, kesik kadraj, boncuklu yüzey, katı "antiseptik", insana benzemeyen anatomi) → **arşiv**: varsayılan kapalı, düğme yok, öğrenciye görünmez. Ders: H462 (2B yeniden çizim kuralları ①–⑦).
- Karar: ön yüz 2B'de sürer; hedef stil düz vektör çizgi film (referans Foley illüstrasyonu). Sonraki iş: SVG sahne kitaplığı + Lottie adım videoları bu stilde yeniden çizilir.
- Commit yapıldı, dağıtım YAPILMADI (kullanıcı kararı).
- **2B stil örneği:** `sahneler.tsx` Erkek sahnesi düz vektör çizgi film diliyle yeniden çizildi (sırtüstü hasta, alt karın kesit penceresi, mesane/prostat/sfinkter/üretra, penis yatay, kateter meatus→mesane, balon, Y bağlantı → böbrek küvet + enjektör; ölçek 1 cm ≈ 12 px). Önizleme `scripts/kmb/sahne3b_onizle.mjs` artık varsayılan SVG (`--uc` ile 3B), kare `meds_temp/kmb/stil/erkek_2b_ornek.png`. Kullanıcı stil onayı bekleniyor; onayla kalan 13 sahne + Lottie videoları aynı dille çizilecek.

## 2026-10-31 — KMB Hedefler filmi: öğrenim hedefleri tam ekran animasyon (H461)
- Yeni `components/kmb/HedefFilmi.tsx`: Hedefler sekmesindeki 15 KMB öğrenim hedefi ayrı bir tam ekran filmde art arda oynar. Lottie değil; SVG sahne kitaplığı gerçek zamanlı sürülür: her cümle bir vuruş (`hedefCalisma[].film[i]`: sahne değişimi, biriken eylem, `odak` + `zoom`), kamera odak ögesinin gerçek kutusuna (getBBox) CSS geçişiyle yaklaşır, odak dışı alan spotla loşlaşır, etiketler yakınlaşmada aynı boyda kalır (`SahneCiz olcek`). Evreler: başlık kartı (hedef no + belge metni) → Ne / Nasıl / Neden → Sık hata (kırmızı çerçeve + sarsıntı) → Hoca sorar (`h-N-s` sesi, 5 sn düşünme halkası, "Cevabı göster") → sonraki hedef; bitişte 15 hedefin onay listesi + Sınava geç. Ses `h-N` klipleri (cümle zamanlı), ses yoksa sessiz kip. Denetimler 3,2 sn'de gizlenir; hız, "Sorular" anahtarı, klavye (boşluk, ←/→ cümle, PgUp/PgDn/J/L hedef, f, Esc). İzlenen hedefler `medsoru_kmb_hedeffilm_02`.
- `02.json`: 15 kartın tümüne `film` koreografisi (6 vuruş; hedef 5/9/10/11/15'te sahne geçişleri: kadın↔erkek, yakın plan mesane↔üretra, malzeme↔kesit). `dogrula.py` film kapısı (vuruş sayısı = cümle, sahne/öge/odak kimliği, zoom 1–2) → 0 HATA. `kmbVeri.ts` `FilmVurus`.
- `kmb.css` `.kmb-hf-*`; Hedefler yan şeridinde `.kmb-hf-ac` düğmesi (yatay şeritte dar kart — width:100% tüm şeridi 950 px'e uzatıyordu, düzeltildi).
- Tuzaklar: klip gerçek süresi `ses_02.json sure`den birkaç ms kısa → `audio.ended` bölüm sonu sayılır (ilerleme %98'de asılı kalıyordu); hızlı hedef geçişinde eski klibin kesilen `play()` sözü AbortError verir → yalnız NotAllowedError duraklatır; dikeyde denetim satırı sığmayınca grid sütunu genişleyip sahneyi kesiyordu → `minmax(0,1fr)` + sarma.
- Yerel 3000'de sınandı (1280×800 ve 375×812): başlık kartı, cümle akışı, kamera/spot, sık hata, soru + düşünme, hedef geçişi, bitiş ekranı. Commit/dağıtım yapılmadı.

## 2026-10-31 — KMB Lottie videoları kare denetimi ve onarımı (H460)
- Yeni araç `scripts/kmb/kare_onizle.mjs`: başsız Chrome + lottie-web canvas ile her bölümün başı/ortası/sonundan kare,
  oynatıcının etiket katmanını taklit eder, cümle metniyle temas sayfası + `rapor.json` (kesik/taşan/çakışan etiket, boş kare).
- `lottie_dsl.py`: kamera hareket listesi + `kamera_coz` (kayan kamera hatası), `etiket_yerlestir`/`etiket_denetle`
  (kadraj, altyazı bölgesi, çakışma, ≤30 harf), `Ic` eşlenmeyen bölüm "olmuş bitmiş" (`'once'`), sahne sayacı → etiket.
- `adim_lottie.py`/`lottie_uret.py`: 45 etiket kısaltıldı; sistit küçük iltihaplı mesane, travma neden/kırık/yalnız kırık
  ayrımı + penis/kan yukarı, malzeme alt raf ve steril alan sınırı, kateter boyları, torba kamerası, vulva perine zemini,
  erkek temizlikte eldiven değişimi paneli, idrar gelmezse iki neden yan yana, yeni cümle metinlerine uyan etiketler.
- `dogrula.py` etiket kapısını çağırır (0 HATA). 02.json ve ses dosyalarına dokunulmadı; commit/dağıtım yapılmadı.

## 2026-10-31 — Soru dışa aktarıcı: çok katmanlı gruplama, ders renkleri, sayfaya sığdır, etiket görünümü, yalnız doğru şık (H456)
- `v15/soruAktar/ayar.ts`: `gruplar: Alan[]` (yıl/kurul/ders/konu/kaynak/tür/zorluk/etiket, en çok 4 iç içe katman; eski `grupla` kaydı katmana çevrilir), `grupSirasi` (olağan / soru sayısı), `grupStil` (alt çizgi, bant, kutu, sade), `grupSayi`; 12 sıralama kipi (`SIRALAMALAR`: yıl eski önce, zordan, kaynak numarası, kısa/uzun, A→Z …); `dersRenkleri` + `DERS_RENK`/`dersRengi` (sitedeki `health.css` ders renkleri; eşleşmeyen ders ad karmasıyla ek listeden); `sigdir` (kapalı / yalnız küçült / doldur) + `sigdirHedef`; etiket görünümü (`etiketBoyut`, `etiketDizilim`, `etiketSekil` hap/kutu/köşeli/çerçeve/düz, `etiketRenk` gri/türüne göre/dersin rengi/özel, `etiketZemin/Metin`, `etiketKalin`); `cozumIcerik.yalnizDogru`.
- `kaynak.ts`: `AQ.etiketler` (çıkmış `tags` + rozetler; süreç etiketleri `_`, `donem3-…`, yıl, dosya adı, ders/yıl kopyası ve Faz 14 rozeti ayıklanır), süzgeç `etiketler`, `secenekler('etiketler')`.
- `belge.ts`: `katmanla` (kararlı çok katmanlı kümeleme, katman sırası yıl yeni önce/metin yıllar sona, kurul no, zorluk, kaynak sırası, etiket sıklığı), `HS.gruplar/grupRenk/dersRenk`, başlık rengi mirası (ders başlığı dersin rengi, alt katman üstünden), `katmanBasliklari` → akışta başlık blokları (`.gb.s0–s3`), ızgarada yalnız en üst katman sayfa bandı + hücre içi `basliklar` (H456); `sayfala` → `sigdirarak` (seyrek bölüm sonu ölçütü `Sayfa.dolu/yeniBolum`, ikili arama 0,6–1,35, `Belge.olcek/sigdirNot`), `Olcer.sigdir(k0)` + `enBuyuk`; etiket rengi `etiketler().renk` (HTML/DOCX/PPTX ortak), `cozumIcerik` yalnız doğru şık (doğru seçeneğin gerekçesi, çeldirici satırı yok).
- `docx.ts`/`pptx.ts`: katman başlıkları (seviye puntosu, girinti, bant/kutu/çizgi), hücre içi alt başlıklar, etiket biçimleri (dolgu/`w:bdr` çerçeve/düz ayraçlı; PPTX vurgu dolgusu), akışta ölçek tabanı `belge.olcek` ile.
- `SoruAktarV15.tsx`: Sıralama/Gruplama (katman ekle-kaldır, hazır dizilimler, grup sırası, başlık biçimi), "Sayfaya sığdır" bölümü (hedef sayfa, ölçek bilgisi), Renk sekmesi (zorluk/etiket alanı, "Her dersin kendi rengi", etiket görünümü bölümü), Çözüm "Yalnız doğru şıkkı açıkla", süzgeçte Etiket; CSS `sx15-katman`.
- Sınama (yerel 3000, 40 çıkmış soru, yıl › kurul › ders › konu): önizleme 22 sayfa = sunucu PDF 22; DOCX LibreOffice 21 sayfa (çözüm akışı Word'de kendi sütun akışı), PPTX 26 slayt (16:9 geometri), tüm XML parçaları ayrıştı; hedef 10 sayfa → ölçek %77 ile 10 içerik sayfası; yalnız doğru şık 30 → 16 sayfa. Commit/dağıtım yapılmadı.

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
