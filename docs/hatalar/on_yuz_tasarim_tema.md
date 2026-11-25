# Hata defteri — on_yuz_tasarim_tema (tasarım, tema, kabuk, düzen, cihaz güvenli alanı)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16; `hatalar/on_yuz.md` 4 konuya bölündü). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## H48 — Canlı sitede tasarım taraması bulguları (2026-10-24)
- Panel PDF yazı satırının kutusuna yapışıyordu (s.10 "Opioid overdozu ?", s.16 "Hipotermi?"): mürekkep eşiği harf
  gövdesini görür, satır kutusunu görmez → `yazi_kesisir` (panel ve etiket yazı satırı kutusundan 0,01 / 0,004 uzak).
- Dar PDF bölmesinde "Çiz" düğmesi harf harf alt alta kırılıyordu: ölçüt ekran genişliğiydi → bölme genişliği (container query).
- Oynatıcı, anlatılan satırları örtüyordu: görüntüleyici anlatılan satırlar oynatıcının altında kalırsa yetecek kadar kaydırır.
- Telefonda görünüm seçici (Metin / Metin + Slayt / Slayt) ayrı bir satır kaplıyordu → başlık satırında tek döngü düğmesi.
- Canlı tarama (telefon, Slayt, 4×): 46 panel/etiketin 45'i temiz; uzun etiket ("kollar fleksiyonda, bacaklar
  ekstansiyonda") kırpılıp yazıya biniyordu → etiket satıra iner, yerleşim satır sayısıyla. Hızlı dinlemede anlatılan satır
  oynatıcı altında kalıyordu (her cümlede sıfırlanan zamanlayıcı hiç çalışmıyordu) → iptal edilmeyen 600 ms kısıtlayıcı.
- Aynı paneldeki bağımsız "A → B" satırları farklı kırılıyordu (nalokson tek satır, flumazenil iki satır) → hizalı tablo
  (kaynak | ok | hedef sütunları, `is-tablo`); baskılama ucu ⊣ büyütüldü.
- Canlı tarama (telefon, Slayt, 2×, 8:08–16:07): etiket "tabloya uygun yaklaşım" (s.49) yazının üstüne konmuştu (yakında yer
  yokken yolun ortasına) → önce yakında yazısız yer, sonra yakında resmin ≤%25'ini örten ama yazıya değmeyen yer, sonra
  sayfada ≤0,35 uzaklıkta boş yer. Sonuç: 35 etiketin 0'ı yazı satırıyla kesişiyor. Sayfa geçişi kaydırması sürerken atlanan
  satır düzeltmesi kaydırma bitince yeniden denenir (masaüstü 2×'te s.11–19'da 2–13 sn örtme vardı).

## H87 — v15 katmanlarında tanımsız renk/yazı değişkenleri: saydam kartlar, varsayılan yazı tipi (2026-10-27)
- **Belirti:** Soru haritasında ısı hücreleri renksiz; v15 katmanlı sayfalarda bazı kartların zemini saydam, Newsreader okuma
  yazısı uygulanmıyor.
- **Kök neden:** v15 CSS'inde `--color-surface`, `--color-success(-soft)`, `--color-warning-soft`, `--v15-serif`, `--v15-font`
  kullanıldı; palet kaydında (`utils/palettes.ts`) bu adlar yok (gerçekleri `--color-white`, `--color-ok(-soft)`,
  `--color-warn-soft`, `--font-read`, `--font-sans`). Tanımsız değişken hesaplanınca özellik geçersiz → zemin saydam,
  `color-mix` boş, yazı tipi miras.
- **Çözüm:** `styles/v15/tokens.css`'e takma adlar (gerçek jetonlara bağlı).
- **Önleme kuralı:** yeni CSS'te renk/yazı değişkeni yazmadan önce `getComputedStyle(document.documentElement)` ile ya da
  palettes.ts/tokens.css'te var olduğu doğrulanır; yeni ad uydurulmaz.

### H90 — v15'te Toplu PDF penceresinin üstüne üst/alt çubuk biniyordu (2026-10-27)
- **Belirti:** Sesli dersler (ve PDF oluştur) › Toplu PDF açılınca pencerenin başlığı ve "indir" düğmesi v15 üst çubuğunun ve alt sekme çubuğunun altında kalıyordu.
- **Kök neden:** pencere (`.tp-perde`, z-index 120) sayfa kabının içinde çiziliyordu; kap kendi katman bağlamını kurduğu için z-index'i kabın dışına taşmıyor, sabit konumlu v15 çubukları (z 30/40) üstte kalıyordu.
- **Çözüm:** `TopluPdfDugme` pencereyi `createPortal(..., document.body)` ile çizer.
- **Kural:** tam ekran örtü/pencere bileşenleri daima body'ye portal ile çizilir; sayfa içi z-index'e güvenilmez.

### H99 — v15'te yeni ve bazı eski sayfalara menüden ulaşılamıyordu (2026-10-27)
- **Belirti:** Topluluk, PDF oluştur, Check Up, sıralama, müzik gibi sayfalar telefonda/tablette/masaüstünde menüde görünmüyordu; tam ekran gibi araçlar dağınıktı.
- **Kök neden:** v15 kabuğunda üç ayrı elle yazılmış liste vardı (telefon menüsü: yalnız Başvuru + MENU_SAYFALARI; kenar çubuğu: yalnız açık bölümün alt sayfaları + sabit 5 kişisel bağlantı; tablet rayı: yalnız 5 bölüm). NAV_TREE'ye eklenen sayfa bu listelere girmiyordu.
- **Çözüm:** `navV15.menuGruplari` tek kaynak; üç görünüm de ondan çizer. Araçlar ayrı kompakt sıra.
- **Kural:** yeni sayfa yalnız NAV_TREE'ye (ve gerekirse KISISEL'e) eklenir; kabukta elle sayfa listesi yazılmaz.

## H100 — Asklepios kutlama efekti görünmüyordu (2026-10-27)
- **Belirti:** "Asklepios Asası" kutlama efekti çalışmıyor; asa/yılan hiç görünmüyordu.
- **Kök neden:** `KutlamaKatmani.tsx` canvas'ı kartın ARKASINDA ve asayı tam merkeze (`cx`) çiziyordu; opak 380 px kart (`.bs-k-kart`) ortayı tamamen örtüyordu. Işıltılar da merkezden doğup kartın altında kalıyordu.
- **Kural:** ortada çizilen efekt kartın altında kalmaz; kartı örtmeyen konuma (iki yan) çizilir ve canvas kart üstüne (`is-ust-katman`) alınır. Yeni kutlama efektini canlı kartla birlikte gör.

## Tasarımdaki animasyon/3B ögesini "yok" diye atlamak (2026-10-27, Hücrem)
- **Belirti:** Kullanıcının canvas'ta çizdiği evrim animasyonları sayfaya girmedi, düz SVG yapıldı.
- **Kök neden:** Plana "3B yok" yazıp geçmek; tasarım kapsamı onaysız daraltıldı.
- **Kural:** Tasarımda olan animasyon/3B atlanamaz; zor ya da bağımlılık gerektiriyorsa kullanıcıya sorulur, plana "yok" diye yazılmaz.

## v15 tam ekranda yan menü içeriğin üstüne biniyor (2026-10-27)
- **Belirti:** Tam ekran modunda 76 px ray açık kalıyor, "Günler, Dr" başlığı ve akış kartlarının solu menünün altında kesiliyor; çıkış hapı üst barın sağındaki simgelerin üstüne biniyor.
- **Kök neden:** `v12.css` tam ekranda `.sh-app` dolgusunu ve `--sh-side-w`'yi sıfırlıyor, `.sh-side/.sh-top`'u gizliyor; v15 kabuğu `.v15-side/.v15-top` kullandığı için gizlenmedi, dolgu kalktı ama ray `position: fixed` kaldı.
- **Kural:** Yeni kabuk (v13, v15…) eklenince `html.is-app-fullscreen` için o kabuğun yan menü/üst bar sınıfları da gizlenir ve `--sh-side-w` sıfırlanır (`styles/v15/shell.css` sonu).

### H100 — Koyu temada "beyaz" yazılar kayboluyordu; spinner/iskelet renkleri temaya uymuyordu (2026-10-27)
- **Belirti:** Koyu temada renkli düğmelerdeki, koyu başlık şeritlerindeki ve perde üstündeki "beyaz" yazılar okunmuyordu; yükleme iskeleti her temada sabit maviydi; bazı ekranlarda doğru şık/zor etiketi renksizdi.
- **Kök neden:** Tailwind `white` rengi `--color-white` = palet **yüzeyine** bağlı; koyu temada `text-white` koyu lacivert çıkıyordu. `.ms-shimmer` sabit `rgba(30,79,216,…)`; `--color-good`, `--color-danger`, `--color-text(-sub)`, `--color-bg/border/text-dim` hiçbir yerde tanımlı değildi.
- **Çözüm:** `index.css`: `.text-white` → `var(--color-on-solid)` (katmansız kural utilities katmanını ezer), `.bg-ink-surface .text-white` → `--color-canvas`, koyu perde için `.on-perde`; iskelet `color-mix(accent)`; tanımsız değişkenler gerçek tokenlara bağlandı. Tam döküm `docs/V15_TEMA_DENETIMI.md`.
- **Kural:** Yazı rengi için `text-white` değil `text-on-accent`/`text-on-solid`; yeni CSS değişkeni yalnız `palettes.ts` TOKEN_KEYS ya da v15 tokens.css içindekilerden; sabit renk yalnız bilinçli süs (çerçeve, kâğıt üstü çizim) için.

## H111c · Esc uygulama tam ekranından çıkarmıyordu (2026-10-28, ortak kabuk)
- **Belirti:** Kabuktaki "Tam ekran" düğmesine basılınca üst çubuk gizleniyor; native tam ekranın açılmadığı durumlarda (dokunmatik/klavyeli cihaz — iPad + klavye, dokunmatik dizüstü — ya da tarayıcı isteği reddettiğinde) Esc'e basmak hiçbir şey yapmıyordu, kullanıcı çıkışı yalnız küçük "Tam ekrandan çık" hapında arıyordu.
- **Kök neden:** Uygulama tam ekranı = `html.is-app-fullscreen`. Kaldırılması yalnız düğmeye ya da native `fullscreenchange` olayına bağlıydı; native katman yoksa Esc'i dinleyen hiçbir kod yoktu.
- **Çözüm:** `src/utils/fullscreen.ts` › `installEscExit` — tek genel `keydown` (bubble, `defaultPrevented`/yazı alanı/açık pencere-menü/sayfa içi tam ekran katmanı/`tam-katman`/`cd-tam-ekran` varken dokunmaz) sınıfı kaldırır ve `medsor:fullscreenchange` yayar. Tarayıcıda sınandı: aç → Esc → kapandı, düğme "Tam ekran"a döndü.
- **Kural:** Native tam ekranın yedeği olan her CSS kipi kendi Esc çıkışını taşır; Esc önce açık pencereye/katmana aittir.

## H111h · PC'de açıklama metinleri 120–160 karakter satır uzunluğunda (2026-10-28, okunabilirlik)
- **Belirti:** 1440 px'te Sınav planı açıklamaları (`sp-acikla`, `ss-acik`, "Bu sayılar nasıl hesaplanıyor?" listesi) ~130, Sağlık kaynakçası ~160, Topluluk kuralı ~116, Arka plan notu ~108 karakter satır.
- **Kök neden:** metin blokları kart genişliğini dolduruyor, ölçü (`max-width: ..ch`) yoktu; bir kısmı 12,5–13,5 px idi.
- **Çözüm:** `takip.css` `.sp-acikla/.ss-acik` 14 px + 72ch, `.sp-nasil ul` 75ch (özet 40 px), `cevrimdisi.css .cv-not` 14 px + 72ch, `saglik.css` kaynakça 90ch, `topluluk.css .tp15-kural` 75ch.
- **Kural:** Gövde/açıklama metni ≥14 px ve satır ≤ ~75ch; geniş kartın içindeki paragraf `max-width` ile sınırlanır.

## H111s · Zihin haritası numaraları koyu temada okunmuyordu (2026-10-28, Ders çalış)
- **Belirti:** Koyu temada `/dersler/zihin-haritasi` liste numaraları (1, 2, 3…) koyu zemin üstünde 1.7–2.0 kontrastla neredeyse görünmüyordu.
- **Kök neden:** `.zh15-no` yazı rengi tema bağımsız sabit `oklch(0.45 …)`; zemin `--color-white` ile karıştığı için koyu temada koyulaşıyor, yazı koyu kalıyordu.
- **Çözüm:** `zihin.css` `:root.theme-dark .zh15-no { color: oklch(0.84 0.09 var(--t)) }`.
- **Kural:** Sabit `oklch()/hex` yazı rengi yalnız token zeminiyle birlikte koyu tema karşılığı yazılarak kullanılır.

## H131c — v16 kabuğu her alt yol değişiminde sayfayı yeniden kuruyordu (2026-10-28)
- **Belirti:** Satır çekmecesi açıp kapatınca liste baştan çekiliyor, kaydırma/sayfa kayboluyor, odak satıra değil `<main>`'e dönüyordu.
- **Kök neden:** `ManageV16.git()` her çağrıda `gezinti` sayacını artırıyordu; sayfa `key`'i buna bağlı olduğundan alt yol (`/sorular/cikmis/<id>`) değişimi de yeniden bağlama demekti; ardından `<main>` odaklanıyordu.
- **Çözüm/kural:** Aynı sayfa içinde yalnız alt yol değişirse sayfa yeniden kurulmaz, odak/kaydırma korunur (aynı adrese yeniden tıklama sıfırlar). Çekmece açma 1 istek (önce liste + ayrıntı).

## H388/H389 — Sınıf adı çakışması: Ders çalış çip şeridi ortaya/sağa kayıyordu (2026-10-28, kullanıcı bildirdi)
- **Belirti:** Ders çalış merkezinde "Kurul 2" düğmesi ekranın ortasında, branş çipleri en sağda duruyordu (kullanıcı ekran görüntüsü, canlı).
- **Kök neden:** Herkese açık profil/Arkadaşlar stili (`styles/v15/kisi.css`) kök sınıf olarak `.ks15` kullanıyordu (`display:grid; max-width:720px; margin:0 auto`); kurul seçici `KurulSecV15` de `.ks15`. Profil ya da Arkadaşlar sayfası bir kez açılınca stil kalıcı yüklenir ve seçiciye bulaşır: otomatik kenar boşlukları satırdaki boşluğu yutup düğmeyi ortaya, çipleri sağa iter. Yalnız o sayfalardan sonra görüldüğü için tek başına açılan sayfada üretilemiyordu. Aynı tür çakışma `.bd15` (Bildirimler ↔ Bitirdiklerim) için de vardı.
- **Çözüm:** `kisi.css` öneki `apr15`, Bitirdiklerim öneki `btr15`. Canlıda Arkadaşlar → Ders çalış geçişiyle önce/sonra ölçüldü (seçici sol boşluğu 427 px → 0).
- **Kural:** Her v15 ekranının kök sınıf öneki sitede tektir; yeni önek seçmeden önce `grep -rn "\.<önek>\b" src/styles` ile denetlenir (bu oturumda yazılan tarama: aynı kök sınıfı iki dosyada tanımlayan stil yok olmalı). Stil "yalnız bazı gezinme sıralarından sonra" bozuluyorsa önce sınıf çakışması aranır.

## H431 — Odak ekranlarında durum çubuğu ve ana ekran çizgisi payı yoktu (2026-10-28, kullanıcı bildirdi: iPhone)
- **Belirti:** iPhone'da (viewport-fit=cover + black-translucent) açık sesli ders ve açık Öğren destesi başlığı saatin altına giriyordu; sesli ders oynatıcısı ana ekran çizgisine biniyordu.
- **Kök neden:** Kabuk odak ekranlarında kendi üst barını (güvenli alanlı) çizmiyor; ekranların kendi başlığı `.sh-main` 4 px dolgusundan başlıyordu. `.cd-dock` taban kuralındaki `env(safe-area-inset-bottom)` telefon/tablet kurallarında düz 6/10 px ile eziliyordu.
- **Çözüm:** Kök sınıf `v15-odak` (ShellV15) + `.sh-main` üst dolgusu `env(safe-area-inset-top) + 4px`; `.cd-dock` alt dolgusu her kırılımda `+ env(safe-area-inset-bottom)`. Chrome'da `Emulation.setSafeAreaInsetsOverride` (üst 47 / alt 34) ile ölçüldü: başlık 51 px'te, oynatıcı tabandan 40 px yukarıda. **Gerçek iPhone'da sınanmadı**; kullanıcının gördüğü çakışma başka bir ekransa ayrıca bakılacak.
- **Kural:** Kendi üst/alt çubuğunu çizen her ekran güvenli alan payını kendisi alır; medya sorgusunda dolgu yeniden yazılırken `env(safe-area-inset-*)` korunur.

## H433 — iPhone: panel başlıkları ve durum çubuğu çakışması (2026-10-28)
- **Belirti:** Sesli derste "Ders seçenekleri", "Oynatıcı" vb. paneller ve diyaloglar iPhone'da saat/pil çubuğunun altına giriyordu; açık temada saat yazısı beyaz başlıkta görünmüyordu.
- **Kök neden:** (1) `v11.css` genel `[role=dialog]` max-height kuralı (özgüllük 0,3,0) `.sh-sheet`'i eziyor ve güvenli alanı düşmüyordu (panel 820 px, başlık y=43 < 47). (2) `appearance.ts syncPwaChrome` her temada `black-translucent` zorluyordu → beyaz durum yazısı.
- **Çözüm/önleme:** genel kurala `.sh-sheet` istisnası + `env(safe-area-inset-top)` düşümü; `.cd-dlg-kart` aynı. Durum çubuğu stili açık temada `default`, koyuda `black-translucent` (index.html erken betik + syncPwaChrome). Yeni tam yükseklikli katman yazan her kural üst güvenli alanı düşer; SAFE öykünmesiyle (üst 47) başlık ≥47 sınanır.

## H439 — Üst çubuk arka plan göstergesi stilsiz çiziliyordu (v15, 2026-10-29)
- **Belirti:** /dersler üst çubuğunda çevrimdışı hapının yanında dönen simge ile "1" alt alta taşıyor, "ARKA PLANDA 1 İŞ" ve "1 paket sıradaTümünü gör" çerçevesiz, bitişik yığılıyordu.
- **Kök neden:** `ArkaPlanGosterge` her sayfada `ShellV15` içinde çizilir, ama `ap15g-*` kuralları yalnız tembel yüklenen sayfa bileşenlerinin (ArkaPlanV15, Yardım, Dil…) içe aktardığı `kisisel.css`'teydi. O sayfalardan biri açılmadan gelinen her rotada CSS hiç yüklenmiyor, açılır kart ve rozet tarayıcı varsayılanıyla çiziliyordu.
- **Çözüm/önleme:** `ap15g` kuralları (+ kendi `@keyframes ap15g-don`, kart çerçevesi/zemini, `v15-label`) kabukla birlikte yüklenen `styles/v15/shell.css`'e taşındı. Kural: kabukta (ShellV15) her sayfada çizilen bileşenin stili sayfa CSS'ine değil `shell.css`/`tokens.css`'e yazılır; bir bileşenin sınıfları yalnız onu içe aktaran (ya da kabuğun) CSS dosyasında yaşar.

## H475 — Yeni sürüm penceresi kartsız (düz madde) göründü (2026-11-02)
- **Belirti:** kullanıcı: "yeni sürümlerin tasarımı farklı gösterilmeliydi, gösterilmiyor" (Site güncellendi / Yenilikler penceresi).
- **Kök neden:** `UpdatePrompt.tsx` yenilikleri yalnız `guncelleme_notu.json › yenilikler` doluysa özellik kartlarıyla (yer, amaç,
  işlevler) gösterir; onem 619/624/625 notları `yenilikler: []` ve yalnız `maddeler` ile yazıldı → pencere düz listeye düştü.
- **Çözüm:** onem 626 notuna 4 yeni ders + "Hocanın vurguladıkları" kartları (`nerede.yol` ders sayfası) ve `eklenen/duzeltilen` yazıldı.
- **Önleme:** öğrencinin gördüğü yeni özellik/ders içeren her dağıtımda `yenilikler` en az bir kart taşır ({ad, nerede:{ad,yol},
  amac, islevler}); yalnız küçük düzeltmede `maddeler` yeterlidir.

### H502 — iPad pencere kipinde sistem düğmeleri geri tuşunu kapatıyordu; kullanıcı geri çıkamıyordu (2026-11-06)
- **Belirti:** iPad'de bölünmüş ekran / Stage Manager penceresinde sol üstteki kapat-küçült-tam ekran düğmeleri uygulamanın geri tuşunun üstüne biniyor, dokunuşu sistem yutuyordu.
- **Kök neden:** tek çıkış yolu sol üst köşedeki geri tuşuydu; iPadOS bu bölgeyi sayfaya bildirmez (Safari'de `env(safe-area-inset-*)` / `titlebar-area-*` yok), sayfa katmanı göremez.
- **Çözüm/önleme:** `components/shell/ipadPencere.tsx`: pencere kipi algısı (`:root[data-pencere='dar']` → üst çubuk 84 px sağa), başlık = geri düğmesi, alt yüzen geri hapı, sol kenar kaydırması + Esc/⌘[/Alt+←, yedek yollar 2 kez kullanılırsa hap cihazda kalıcı. Kural: hiçbir ekranda tek çıkış yolu sol üst köşe olamaz; görünürlük denetiminde `offsetParent` değil `getClientRects()` kullanılır (yapışkan/sabit atada null döner).

### H504 — Ayarlarda "Küçük sürprizler" satırı görünmüyordu (2026-11-06)
- **Belirti:** sürpriz katmanını kapatma düğmesi ayarlarda yoktu.
- **Kök neden:** v12 ayarlar (`ProfileV12` › Veri) `<ArzuRow />`'u kullanıcı geçirmeden çağırıyordu; satır `auth.currentUser`'a düşüyor, yerel kimlik sisteminde (H466) bu nesne hesabı tanıtmadığından satır gizleniyordu.
- **Çözüm/önleme:** `DataPanel`'e `currentUser` geçirildi. Kural: hesap koşullu satırlar kullanıcıyı prop olarak alır, `auth.currentUser` yedeğine güvenilmez.

### H517 — Üst bar başlığı bölünmüş ekranda ve yan ray açıkken kırpılıyordu ("Sesli dersler" → "Sesli …", "Tam ekran ve kısayollar" → "Tam ek…") (2026-11-09)
- **Belirti:** 600–839 px (iPad bölünmüş ekran, dar pencere) ve yan menüsü açık 1024–1280 px'te sayfa başlığı üç nokta ile kesiliyor, alt başlık okunmuyordu.
- **Kök neden:** `shell.css` üst bar ölçülerini **pencere** genişliğine (`@media`) bağlıyor; başlığa kalan yer ise ray/yan menü düştükten sonraki alandır. ≥1024'te arama kutusu sabit 260 px ve araç grubu `flex: none` olduğu için daralan tek öge başlıktı; 600–839'da tam "Kurul N ›" çipi + yükle düğmesi + 5 simge başlığa ~100 px bırakıyordu.
- **Çözüm/önleme:** ≥1024'te araç grubu başlıktan 1000 kat istekli küçülür ve içinde yalnız arama kutusu daralabilir (`flex: 0 1 260px; min-width: 44px`); 600–839'da kompakt "K2" çipi, yükle düğmesi hesap menüsünde, başlık telefondaki gibi iki satıra sarar. Kural: üst bara yeni araç eklerken başlık 600, 768 ve yan menülü 1024'te ölçülür; sabit genişlikli araç `flex: none` bırakılmaz.

### H518 — Ayarlar: gruplar karışık, alt sayfalar iki ayrı anahtar görünümü kullanıyor, geniş ekranda tek dar sütun (2026-11-09)
- **Belirti:** "Ben / Ayarlar / Diğer" grupları ilgisiz satırları yan yana koyuyordu (Hesap ile Görünüm aynı grupta, turlar hem listede hem Hesap sayfasında); Erişilebilirlik ve Görünüm'deki anahtar (38×22, koyu düğme) ile Tam ekran'daki (44×26, beyaz düğme) farklıydı; Erişilebilirlik › Hareket segmenti panel kenarına yapışıktı; telefonda "Profil ve ayarlar" başlığı iki satıra sarıyor, "Erişilebilirlik" kırpılıyordu; masaüstünde 1440 px'in 720'si kullanılıyordu; başlıklar "Veritabanı Eşitleme & Yedekleme" gibi İngilizce büyük harf düzenindeydi.
- **Kök neden:** v15 dalı v12 panellerini olduğu gibi sarıyordu (`.pf15-panel.u12-pf`); v12 anahtarı ve satır boşlukları v15 kart diline uyarlanmamış, liste tek düz dizi olarak büyümüştü. Geniş düzen hiç yoktu (`.pf15 { max-width: 720px }`).
- **Çözüm/önleme:** `ProfileV12.tsx` v15 dalı veri tablosundan kurulur (Profilim · İçeriklerim · Görünüm ve okuma · Uygulama · Hesap ve veri · Yardım · Oturum), "Ayarlarda ara" + tek dokunuşla tema; kabın **üst öğesi** ≥ 860 px ise (ResizeObserver; `.pf15` kendisi 720 ile sınırlı olduğundan kendi genişliği ölçülmez) liste solda yapışkan, bölüm sağda. Anahtar ve dokunma alanı `profil.css`'te tek tip. Yükseklik sınırlı esnek sütunda çocuklar `flex: none` olmalı (yoksa `overflow: hidden` liste tek satıra çöker — ilk denemede görüldü). Kural: Ayarlar'a yeni satır `gruplar` tablosuna, doğru gruba ve `ek` arama sözcükleriyle eklenir; aynı satır ikinci bir sayfada yinelenmez.


### H659 — Tasarım katmanında taban öğe kuralı bileşen sınıflarını ezdi: çip/düğme iç boşluğu, yazı boyutu, renk kayboldu (2026-11-25, v16)
- **Belirti:** v16 tuvalinde çiplerin yazısı kenara yapışık, düğmeler sıkışık, "Derse dön" yazısı görünmez, liste bağlantıları mavi.
- **Kök neden:** `.scr button { padding:0; font:inherit }` ve `.scr a { color }` (öncelik 0,1,1) `.chip`/`.btn` (0,1,0) kurallarını eziyordu.
- **Çözüm:** taban öğe kuralları `:where(.scr) …` içine alındı (öncelik 0).
- **Kural:** stil katmanında öğe seçicili taban kuralı her zaman `:where()` içinde yazılır; bileşen sınıfı kazanmalı.

### H660 — Geç yüklenen v15 sayfa CSS'i aynı öncelikteki v16 kuralını ezdi (2026-11-25)
- **Belirti:** v16 ders satırı düzeltmesi derlemede vardı ama sayfada etkisizdi (Soru çözücü "Bitirdim" kesik kaldı).
- **Kök neden:** `styles/v15/cozucu.css` sayfa parçasıyla sonradan yüklenir; `:root[data-v15]` ile `:root[data-v16]` aynı öncelikte, son gelen kazanır.
- **Çözüm:** v16 kök seçicisi `:root[data-v16='on'][data-v15='on']` (bir kademe öncelikli).
- **Kural:** üst katman eklerken yükleme sırasına güvenme; katman seçicisi alttakinden öncelikli kurulur.

### H661 — Gizli kaydırma çubuklu tek satır düğme grubu telefonda kesik görünüyordu (2026-11-25)
- **Belirti:** Sesli soru çözücü ders satırında son düğme ("Bitirdim") yarım; İstatistik 4. sekme, Kamplar "En önemliler" sığmıyor.
- **Kök neden:** `flex-wrap:nowrap; overflow-x:auto; scrollbar-width:none` ve eşit sütunlu `.v15-seg` (minmax(0,1fr)); kaydırılabilirlik görünmüyor.
- **Çözüm:** v16'da eylem satırları ve sekmeler sarar; seçici sütunları içeriğe göre, telefonda dolgu daraltıldı.
- **Kural:** `scrollWidth > clientWidth` olan `overflow` kutusu (bilinçli `hscroll` dışında) 375/820/1366 taramasında sıfır olmalı.

### H662 — Dar bölmedeki etiket ekran genişliğine göre gizlendi; üç bölmeli PC'de düğme altına kaçtı (2026-11-25)
- **Belirti:** Sesli ders PDF çubuğunda "Sayfa" etiketi 1366 px'te yakınlaştırma düğmesinin altında kaldı.
- **Kök neden:** `@media (max-width:…)` ekranı ölçer; PDF çubuğu üç bölmeli düzende ~350 px.
- **Çözüm:** kip düğmesi her boyutta yalnız ikon + `aria-label`.
- **Kural:** bölme içi öğede ekran sorgusu değil, kap sorgusu (`container`) ya da ikon + etiket kullan.

### H663 — PDF "sayfa sayfa" kipi sürekli kipten ayırt edilmiyordu (2026-11-25, v16)
- **Belirti:** kullanıcı "PDF sürekli ve sayfa sayfa özelliği çalışmıyor" dedi; düğme değişiyor, ekran aynı kalıyordu.
- **Kök neden:** kip yalnız `scroll-snap` idi; sayfa 550 px, bölme 704 px → ekranda yine iki sayfa. Sınama yalnız sınıfı ve snap değerini ölçmüştü, görüntüyü değil.
- **Çözüm:** `PdfDocView` şu anki sayfaya `is-cur` verir; sayfa kipinde yalnız o görünür, önceki/sonraki düğmeleri PDF'in sağ altında yüzer.
- **Kural:** görsel kip özelliği "öznitelik yazıldı" ile değil, ekranda görünen sayfa sayısı/içerik değişimiyle doğrulanır.

### H664 — Telefonda mini oynatıcı alt sekme çubuğunu örtüyordu (2026-11-25, v15'te de)
- **Belirti:** sesli ders çalarken telefonda Bugün/Ders/Soru/Sınav/Menü sekmeleri görünmüyor, sayfalar arası geçilemiyordu.
- **Kök neden:** `CanliDersDock` alt boşluğu `.a13-island-wrap, .s12-tabs, .sh-tabs` ile ölçüyordu; v15 sekme çubuğu `.v15-tabs` listede yoktu → boşluk 0.
- **Çözüm:** seçicilere `.v15-tabs` eklendi (ölçüm + ResizeObserver); oynatıcı 691–751, sekmeler 751–812.
- **Kural:** kabuk sınıf adı değişince onu ölçen yerleri `bag.py kim` / grep ile tara; sabit sınıf listesi yeni kabuğu kapsamalı.

### H665 — v17 başlıkları Fraunces yerine Geist ile çiziliyordu (2026-11-25, v17)
- **Belirti:** v17 sesli ders ve Bugün başlıkları tasarımdaki serif yerine eski sans yazı tipiyle göründü.
- **Kök neden:** eski genel kural `html.ui-v7 :is(h1,h2)` (özgüllük 0,1,2) `--font-display` veriyordu; `.k7-bas` (0,1,0) yeniliyordu.
- **Çözüm:** `.k7` içinde `--font-display` serif'e eşlendi, yazı rolleri `.k7 :is(...)` (0,2,0) ile tanımlandı.
- **Kural:** eski kabuğun üstüne binen yeni katmanda başlık/öğe etiketlerine düşen genel kurallar sayılır; yazı tipi hesaplanmış değerle doğrulanır.

### H666 — v17 telefonda PDF çubuğu araç menüsünü ekran dışına itiyordu (2026-11-25, v17)
- **Belirti:** 375 px'te PDF çubuğunun sonundaki araç menüsü (401 px) 351 px çubuğun dışında kaldı, dokunulamıyordu.
- **Kök neden:** paylaşılan `CdPdfBolme` çubuğu 13 öge ve `nowrap`; v17 telefon düzeni daha dar sütun veriyor.
- **Çözüm:** v17'de çubuk `flex-wrap`; telefonda yakınlaştırma düğmeleri gizli (parmakla yakınlaştırma var).
- **Kural:** paylaşılan bileşen yeni kabuğa konunca her cihazda çocukların `right` değeri pencere/kapsayıcı genişliğiyle taranır.

### H668 — v15 telefonda Soru çöz "Kip" seçicisi kartı taşıyor, Bugün halkasında "günlük hedef" kesiliyordu (2026-11-25)
- **Belirti:** 375 px'te Test oluştur kartında Kip seçicisinin sağ ucu 369 px'e taşıyordu (kart 359 px), "Testi başlat" yarım genişlikte kalıyordu; Bugün'de 96 px halkadaki "günlük hedef" yazısı halkanın kenarına biniyordu.
- **Kök neden:** `dersler.css`'te sonradan gelen katman `.s15-test-alt`'ı `flex-wrap`'a çevirmiş, satırlar ve `.v15-seg` içerik genişliğinde (min-width:auto) kalıyordu; 78 px sabit etiket + 3 nowrap düğme dar kaba sığmıyordu. Halka alt yazısının genişlik sınırı yoktu, iç çaptan genişti.
- **Çözüm:** `d15` ≤479 px kapta seçici satırları etiket üstte, seçici ve başlat düğmesi tam genişlik; seçici düğmeleri `min-width:0` + üç nokta. Halka yazısı `max-width:74%`, dar kapta 11 px.
- **Kural:** sonradan eklenen düzen katmanı (grid→flex gibi) öncekinin dar ekran kurallarını geçersiz kılabilir; her kırılım değişikliğinde 375/768/1440 px'te kart içi öğelerin `right` değeri kapsayıcıyla karşılaştırılır.

### H669 — v15 ders detayında bölüm listesi küçük iç kaydırmaya sıkışıyor, telefonda ders adı 95 px'e iniyordu (2026-11-25)
- **Belirti:** telefonda 736 px'lik "Bölümler" listesi sayfa altında ~116 px'lik ayrı kaydırılan kutudaydı (tablette 248 px); üst çubukta ders adı "SSS Hücresel…" diye 95 px'e sıkışıyordu. Sürüm penceresinde "Tüm sürüm notları" iki satıra kırılıp sola yaslanıyordu.
- **Kök neden:** tek sütunda `.dd15` ekran yüksekliğine sabitlenip listeye "kalan alan" veriliyordu; üstteki kartlar (çalışman, içerikler, yorumlar) eklendikçe kalan alan küçüldü. Telefonda alt sayfa üst çubuğu 5 araç (204 px) taşıyordu. `a.up-btn` dolgusuzdu, 1:1,6 oranla 113 px'e iniyordu.
- **Çözüm:** `dd15` <860 px kapta sayfa doğal akar, liste tek kaydırmada tam görünür (iki sütunda yapışkan liste aynen); telefonda geri düğmeli sayfalarda kurul çipi gizli (başlık 139 px); `up-btn` içerik genişliğinden başlar, tek satır, ortalı.
- **Kural:** "kalan alanda kayan" liste, üstüne yeni kart eklenen her değişiklikte 375/768 px'te `clientHeight` ile ölçülür; içerik listesini iç kaydırmaya sıkıştıran sabit yükseklik telefon/tablette kullanılmaz.

### H670 — Çözücü ilerleme şeridi: 215 ayrı düğme, telefonda dokunulamıyor ve sağ yarısı kırpılıyordu (2026-11-25)
- **Belirti:** check-up çözücüde (215 soru) her parça 3×6 px'lik `<button>`: telefonda seçilemiyor, klavyede 215 sekme durağı; 215 × (3 px en küçük genişlik + 3 px boşluk) = 1290 px, 347 px şeritte ~58 parçadan sonrası kırpılıyor, 200. soru şeritte görünmüyordu.
- **Kök neden:** şerit soru başına düğme olarak kurulmuştu (`SoruCozucu.tsx`, kopyası `AlternatifCozucuView.tsx`); `min-width:3px` + sabit `gap:3px` soru sayısıyla ölçeklenmiyordu.
- **Çözüm:** ortak `spots/cozucu/IlerlemeSeridi.tsx`: tek `role="slider"` (24 px dokunma alanı), parçalar yalnız görsel; dokun/sürükle konumdan seçer, bırakınca geçer (önizleme balonu); ←/→ ±1, PgUp/PgDn ±10, Home/End. Boşluk soru sayısına göre 3/1/0 px, şimdiki parça en az 4 px.
- **Kural:** soru sayısıyla çoğalan öge tek tek etkileşimli yapılmaz; 200+ öğede 375 px'te son öğenin `right` değeri kapsayıcıyla karşılaştırılır.

### H671 — Giriş/tanıtım ana uygulamanın üstüne açılan katmandı; altında kabuk ve sayfa verisi kuruluyordu (2026-11-25)
- **Belirti:** oturumsuz açılışta tanıtım+giriş `role="dialog"` katmanı olarak ana sayfanın üstünü kaplıyordu; adres değişmiyor, altta kabuk ve sayfa istekleri çalışıyordu; iki ayrı tasarım dalı (ms-onboard / OnboardingV12).
- **Kök neden:** `App.tsx` `girisKapisi` iken `<Onboarding>`'i ana ağacın İÇİNE ekliyordu (erken dönüş yoktu). Giriş sayfasının adresi yoktu; yönlendirici `/giris`'i tanımadığından sunucu 404 dönüyordu.
- **Çözüm:** `components/giris/GirisSayfasi.tsx` + `styles/giris.css` (ayrı parça); `App` `girisKapisi` iken yalnız onu döndürür (`erisimEngelli` kalıbı); adres `/giris?sonra=<önceki>`, girişten sonra `navigateTo(sonra)` (`app/girisYolu.ts`, açık yönlendirme yok); yönlendiricide `/giris` → today, sunucu 200. Doğrudan açılışta kanonik `/bugun?sonra=` iç içe sarılmaz. Başlık `html.ui-v7 :is(h1,h2)` (0,2,1) yazı tipini eziyordu → `.gr h1.gr-baslik`.
- **Kural:** tam ekran kapı (giriş, erişim) ana ağaca katman olarak eklenmez, erken dönüşle tek başına kurulur ve kendi adresi olur; yardımcılar bileşen dosyasından dışa açılmaz (App içe aktarınca parça ana pakete girer).

### H672 — Bugün'de 817 KB Kurul 1 spot dosyası ilk çizimle yarışıyordu (2026-11-25)
- **Belirti:** Bugün açılışında en büyük JS parçası `exam_spots_k1` (817 KB) idi.
- **Kök neden:** `TodayView` günün spotu için dosyayı ilk `useEffect`'te koşulsuz `import()` ediyordu.
- **Çözüm:** yükleme `requestIdleCallback` ile ilk çizimden sonraya (yoksa 400 ms); günün spotu menü kapalıyken de gösterildiği (H139) için koşul konmadı.
- **Kural:** sayfanın ikincil kartı için büyük veri ilk çizimden sonra, boşta yüklenir.

### H673 — v15 klinik editöryal adım: Bugün iskeleti ve başlık belirteçleri (2026-11-25)
- **Belirti:** Bugün halka + kart ızgarasıydı; tek `h1` görünmezdi (sr-only); halka yazısı sığmıyordu (H668).
- **Kök neden / karar:** kullanıcı "daha sade, klinik editöryal" yön istedi; tasarım kaynağı Framer "MeDSor v15 · Klinik Editöryal".
- **Çözüm:** `TodayView` v15 dalı JSX olarak yeniden: görünür `h1` özet başlık (sınava kalan gün), plan cümlesi, hedef çubuğu, koyu "sürdür" bloğu, kartsız ince ayraçlı listeler, düz yan sütun (kısayol, `dl` durum, `figure/blockquote` spot). `styles/v15/editoryal.css`: başlık belirteçleri Literata (zaten yüklü), `.ed-*` sınıfları, tutarlı `:focus-visible`. Tur seçicisi `.t15-ring` → `.t15-lead`.
- **Kural:** tasarım belirteci değişince eski seçicilere bağlı turlar (`CanliDersTur.tsx`) aynı anda güncellenir; yeni yazı tipi indirilmeden önce `index.html`'de yüklü olanlar kullanılır.

### H674 — Kabukta "içeriğe geç" bağlantısı yoktu (2026-11-25)
- **Belirti:** klavye kullanıcısı her sayfada tüm menüyü sekmeyle geçmek zorundaydı (WCAG 2.4.1).
- **Kök neden:** `App` ana kabuğunda atlama bağlantısı ve odaklanabilir ana içerik hedefi yoktu.
- **Çözüm:** `.ed-atla` bağlantısı (yalnız odakta görünür, `erisilebilirlik.css`), `<main id="ana-icerik" tabIndex={-1}>`; uygulama `#` bağlantılarını kendi yönlendirdiği için odak tıklama işleyicisiyle elle taşınır.
- **Kural:** uygulama içi çapa bağlantısında tarayıcının çapa odağına güvenilmez, odak elle taşınır ve klavyeyle sınanır.

### H675 — Editöryal Bugün ve giriş fazla büyük/ağırdı; kompakt, hareketli sürüm (2026-11-25)
- **Belirti:** kullanıcı "daha küçük, minimalist, kompakt, animasyonlu" istedi; 44 px başlık ve koyu tam genişlik "sürdür" bloğu ekranın üst yarısını kaplıyordu.
- **Kök neden:** H673 ölçeği büyük ekran editöryal düzenine göre seçilmişti; telefonda ilk ekrana sığan bilgi azaldı.
- **Çözüm:** Figma "MeDSor v15 · Minimal" (https://www.figma.com/design/xBn39OuJbTgz87O26f33UK) → başlık clamp(22–28 px), 3 px hedef çubuğu (değer yanında, plan cümlesi yalnız hedef yoksa), çerçeveli hafif "sürdür" satırı + aksan oynat, 52 px liste satırı, hap kısayollar, satır içi durum, 14 px alıntı, PC yan sütun 280/300 px. Hareket: bölümler sırayla belirir, çubuk dolar, satır/kısayol/oynat üzerine gelme ve basma geçişleri; "hareketi azalt" erisilebilirlik.css ile kapanır. Giriş başlığı clamp(24–34 px), boşluklar sıkı.
- **Kural:** ölçü kararı önce 375 px'te "ilk ekranda ne görünüyor" sorusuyla verilir; animasyon yalnız transform/opacity ile ve azaltılmış hareket kipinde kapanacak biçimde eklenir.

### H676 — v15 klinik bileşen dili: ortak parçalar ve merkez sayfaların iskeleti (2026-11-25)
- **Belirti / istek:** kullanıcı tasarımın baştan sona, bileşen bileşen ve daha klinik/özgün değişmesini istedi; merkezler simge karosu + kart ızgarasıydı, etiketler dolgulu hap, sekmeler dolgulu kutu.
- **Kök neden / karar:** v15 sayfaları ortak parçaları (`tokens.css`: kart, karo, etiket, düğme, sekme, çubuk) 78 dosyada kullanıyor; tek tek boyamak yerine ortak dil değiştirildi, merkezlerin yapısı JSX'te yeniden kuruldu. Kaynak: Figma "MeDSor v15 · Minimal" › Klinik sistem.
- **Çözüm:** `styles/v15/klinik.css` (ShellV15 içe aktarır): gölgesiz 10 px kart, dolgusuz çerçeveli karo, mono noktalı etiket, koyu 8 px düğme, alt çizgili sekme, 3 px çubuk, mono üst etiket/sayaç, kurul/branş çipleri. `v15/klinik/KlinikDizin.tsx` (harfli bölüm, 01… numaralı satır, mono meta); Başvuru, Sınava hazırlan, Soru çöz araçları, Ders çalış araçları dizine geçti; Ders çalış "Diğer araçlar" alt penceresi kaldırıldı (araçlar doğrudan görünür).
- **Kural:** görünüm değişikliği önce ortak parçada yapılır; sayfaya özgü kural yalnız yapı farkı varsa yazılır. Geri dönüş noktası: etiket `v15-yedek-2026-11-25` / dal `yedek/v15-2026-11-25`. Gizli önizleme panelinde `document.timeline` durur; animasyonlu ekran görüntüsü soluk çıkarsa önce panelin görünürlüğüne bakılır.

### H677 — Kalan v15 iskeletleri klinik dile geçti; giriş animasyonları içeriği gizliyordu (2026-11-25)
- **Belirti:** ders detayı (açılır kutulu gruplar), sesli liste, çözücü, Bugün "Şimdi"/"İlk adımlar" eski kart dilindeydi. Doğrulamada, animasyonlu bölümler ve hedef çubuğu zaman çizelgesi durunca (gizli/arka plan sekme, ekran görüntüsü) görünmez kalıyordu.
- **Kök neden:** giriş animasyonları içeriği `opacity:0` + `fill: both` ile başlatıyordu; `document.timeline` ilerlemezse içerik ilk karede (görünmez) kalır. Aynı kalıp `sl15-ac`'ta da vardı.
- **Çözüm:** animasyonlar yalnız `transform` (t15-gel, kl-gel, gr-gel, sl15-ac); hedef çubuğu dolma animasyonu kaldırıldı. Ders detayı içerikleri `KlinikDizin` (A–D, kesintisiz numara, meta tekrarı açıklamadan atılır), kayıt başlığı ve mono numaralı bölüm çizelgesi; `ProgramSimdiKarti` mono saatli zaman satırı (sürüyorsa nabız noktası); İlk adımlar kare onay kutulu kontrol listesi; sesli listede kartsız branş + CSS sayaçlı mono sıra; çözücüde serif kök, mono harf kutusu, 8 px şık (`soru-cozucu.css`, v15 kapsamı).
- **Kural:** giriş animasyonu içeriği asla gizlemez (opacity ile başlamaz); yalnız konum/ölçek. Açık iş: `ara_resim`, `hoca_ara`, `profil`, `oyun` giriş animasyonları hâlâ opacity 0 ile başlıyor.

### H678 — 48 v15 sayfasında eski kart dili kalmıştı; genel kural seçici hatasıyla etkisizdi (2026-11-25)
- **Belirti:** menüdeki 48 sayfanın taramasında ~1000 öğe eski dildeydi (14–24 px köşeli dolgulu kart, gölge): güncelleme günlüğü `gg-kart` 759, ders özeti `dz-kart` 50, başarımlar `sn-kart`/`bs-hedef`, oyunlar `mk-oyun-kart`, öncelikli dersler `od-*`, sınav planı `sp-kutu`, KMB, gün seçici. Dört giriş animasyonu (`ar-gir`, `ha-gir`, `pf15-gir`, `og15-gir`) içeriği opacity 0 ile başlatıyordu.
- **Kök neden:** sayfa dosyaları ortak `v15-card` yerine kendi kart sınıflarını tanımlıyor; ortak bileşen değişikliği onlara ulaşmıyordu. İlk genel kuralda `:is(...)` ile `:not(...)` arasında satır sonu kaldığı için seçici kartın kendisini değil alt öğelerini seçti, kural etkisiz kaldı (tarama ikinci kez aynı sayıyı verdi).
- **Çözüm:** `klinik.css`: `#ana-icerik` kapsamında `-kart/-card/-kutu/-panel/-pano` sınıfları 10 px + gölgesiz (yuvarlak öğeler hariç), kalan parçalar (od-*, cx-tab, gün seçici, sınıfsız düğme 8 px, girdi 8 px); dört animasyon yalnız transform. Figma (Klinik sistem: 5 yeni ekran) ve Framer ("v15 · Klinik dil": 4 ekran) eklendi.
- **Ek:** health.css `html.ui-v7 :is(.cx-tab, .ms-chip…)` köşeyi `99px !important` zorluyordu (aynı önemle ezildi); Deneme sınavı (`.tb`) ve PracticeV15 (`.q15`) kabuk dışında olduğundan kendi köklerinde kural aldı. Ortak içerik/sayfa giriş animasyonları da (ui-in, ui-fade, bs-gir, bs-sol, cd-gir, au-in, mo-reveal, kmb-belir, m-page-in, lf-fade) yalnız transform oldu; kutlama/konfeti animasyonları bilinçli bırakıldı. Son tarama: 46 sayfada eski dil 0, kalanlar yalnız avatar/anahtar (bilinçli yuvarlak); taşma 0. Açık: başarımlar ve oyunlar sayfalarının kapsül sekme/tema dili (tarama kapsül öğeleri saymıyordu).
- **Kural:** tasarım değişikliği "her sayfa" iddiasıyla bitirilmeden menüdeki tüm adresler hesaplanmış stil taramasıyla sayılır; genel seçicide bileşik sözde sınıflar arasına boşluk konmaz ve kural yazıldıktan sonra tarama yeniden çalıştırılır.

### H679 — Kapsül haplar ve dolgulu simge kutuları taramada görünmüyordu; oyunlar lobisi keçe temasındaydı (2026-11-25)
- **Belirti:** başarımlar sekmeleri, dışa aktarıcı/öğren/öncelikli ders çipleri, sınav planı ve güncelleme günlüğü hapları, başarım seviye numaraları eski dilde kaldı; H678 taraması bunları saymadı.
- **Kök neden:** tarama köşe ≥200 px (kapsül) öğeleri ve dolgulu simge kutularını dışarıda tutuyordu; sayfa dosyaları kendi çip/hap sınıflarını (`sx15-cip`, `ks15-eylem`, `o15-cip`, `od-cip`, `f12-pill`, `sn-meta > span`, `bs-sv-no`, `*-ic`) tanımlıyor.
- **Çözüm:** `klinik.css` H679: çip/hap/sekme sınıfları 8 px (`!important`, eski `99px !important` kuralları yüzünden), seçili başarım sekmesi mürekkep dolgu, `-ic` simge kutuları dolgusuz çerçeve (oynat düğmesi hariç), oyunlar lobisi (`.mk-merkez`) kâğıt zemin + ince çerçeveli kartlar; oyun masası ve kullanıcı oyun temaları bilinçli bırakıldı.
- **Kural:** tasarım taraması kart + kapsül + simge kutusu üç türünü birlikte sayar. Not: başka oturumun commit edilmemiş "Tasarruf kipi" (`src/tasarruf/`, App.tsx) öğrenciyi 4 sayfalık sade kabuğa yönlendiriyor; bu kipte v15 sayfaları öğrenciye görünmez ve öğrenci hesabıyla tarama yapılamaz.

### H680 — Klinik dil "yeterince yenilikçi değil, hatlar belirgin değil": klinik çizelge katmanı (2026-11-25)
- **Belirti / istek:** ince gri çizgiler (1 px `--color-line`), gölgesiz kartlar ve küçük farklar ekranda belirgin değildi.
- **Kök neden:** H676 dili kontrastı bilinçli düşük tutuyordu (ince hat, yumuşak gri); yüzey ile zemin arasında ayrım zayıftı.
- **Çözüm:** `styles/v15/cizelge.css` (klinik.css'ten sonra, ShellV15): milimetrik ızgara zemin (ana içerik, en az ekran boyu), 1.5 px mürekkep hat, bulanıksız 4 px sert baskı gölgesi (iç içe yüzeyde yalnız dıştaki), 2 px köşe, KlinikDizin koyu ters bant başlık + kutulu numara hücresi, mono köşeli çipler (seçili mürekkep dolgu), basınca gölgeye oturan düğmeler, çıkmışlar kartı/öncülleri/oy satırları, Tasarruf kabuğunun (başka oturum) sekme ve satırlarına yalnız hat dili (sade/hareketsiz kararı korunarak, dosyalarına dokunmadan). Figma "Klinik çizelge (v2)" ve Framer "v15 · Klinik çizelge" sayfaları.
- **Kural:** belirgin hat istendiğinde kontrast yüzey çerçevesi ve ofset gölgeyle kurulur, renkle değil; geri dönüş tek içe aktarım satırıdır (cizelge.css).

### H681 — Çizelge katmanı reddedildi; v18 "Canlı minimal" seçmeli arayüz, bot tasarruf geçişi (2026-11-25)
- **Belirti / istek:** kalın hatlı çizelge dili "aşırı kötü"; Figma'da çizilen üç modern yöndeki C (Canlı minimal) seçildi; v15 varsayılan kalmalı, v18 arayüzden açılmalı; botlar tasarruf/normal mod arasında geçebilmeli.
- **Kök neden:** (1) cizelge.css v15'in tamamına kapsamsız uygulanıyordu, seçmeli değildi; (2) genel çip kuralı `.ks15-dug`'a beyaz zemin verip kurul seçicide beyaz-üstüne-beyaz yazı üretti; (3) `?tasarruf=` parametresi aiTest yanıtı gelmeden kanonik yönlendirmeyle siliniyordu.
- **Çözüm:** cizelge içe aktarımı kaldırıldı; `styles/v15/canli.css` yalnız `:root[data-v18='on']` altında (appearance `v18`, Ayarlar › Görünüm ve Tasarruf Ayarlar'da seçici); `.ks15-dug` çip listesinden çıkarıldı, siyah hap; sesli liste grupları kart (flex-shrink 0, kırpılma yok); `tasarruf/bayrak.ts` parametreyi modül yüklenirken okuyup `medsor_tasarruf_bot`'a yazar, yalnız aiTest oturumunda uygulanır.
- **Kural:** yeni görünüm dili önce seçmeli katman olarak (`data-vNN`) gelir, varsayılanı ezmez; genel çip/kart seçicisi koyu zeminli denetimleri dışlar; adres parametresi okuyan bayrak yönlendirmeden önce, modül yüklenirken okur.
