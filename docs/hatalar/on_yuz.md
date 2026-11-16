# Hata defteri — on_yuz (öğrenci arayüzü, düzen, dokunma, tema, sayfalar)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## Sesli ders PDF/DOCX dışa aktarımı (2026-10-20)

- **Yazıyla sayı:** konuşma metni okunuş için "iki virgül bir", "yüzde kırkına" yazar; öğrenciye verilen dosyada bunlar
  "2,1", "%40'ına" olmalı. Kural tek yerde: `src/services/sayiYazim.ts` (`sayilariYaz`), dışa aktarım
  (`components/canliDers/canliDersDisaAktar.ts`) ve ekran (`canliDersStore.ts` → `sayilariDuzelt`, vurgu konumları `sayilariYazEslemeli` ile taşınır) her derste uygular. Saklanan metin değiştirilmez (ses ve cümle zamanı ona bağlı).
- **Düz madde yığını yok:** paragraf tek madde olarak basılmaz; ilk cümle ana madde, sonrakiler alt madde, "Yani/Örneğin…"
  ve "2 ölçütü ayırın" gibi duyurulardan sonra gelenler ikinci düzey; kısa noktasız satır alt başlık olur.

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

## H82 — Çıkmış soru penceresi şık seçilince kayboldu, ders sürmedi (2026-10-27, sınamada yakalandı)
- **Belirti:** Slayt 3'teki chip'e basıp şık seçince pencere kapandı, görünüm slayt 1'e döndü, ses sürmedi.
- **Kök neden:** Pencere durumu slayt katmanındaki chip bileşenindeydi. Ses durunca görünüm canlı konuma döndü, PDF
  görüntüleyici ekran dışı slaytı (chip + pencere) kaldırdı; durum ve "çalıyordu" bilgisi kayboldu.
- **Çözüm / kural:** Durum modül düzeyinde (`useSyncExternalStore`), pencere `CdCikmisPencereKok` ile `document.body`'ye
  portal; sanal listede çizilen bileşen kalıcı durum tutmaz. Sınama: çalarken aç → ses durur, kapat → aynı saniyeden sürer.

## H86 — Sınav planı Kurul 2'de boş sayfa (2026-10-27)
- **Belirti:** `/kamplar/sinav-plani` yalnız başlık ve açıklamayı gösteriyor, altı bomboş.
- **Kök neden:** aktif kurul takvimden 2; `planVerisiYukle` `kurulDagilimi(2)` bulamayınca (sinav_dagilimi.json'da Kurul 2 yok)
  `null` dönüyor, `SinavPlani` da `if (!plan) return null` ile hiçbir şey çizmiyordu.
- **Çözüm:** boş durum iletisi ("Kurul N için sınav dağılımı henüz girilmedi"). Kurul 2 dağılımı girilince plan kendiliğinden kurulur.
- **Önleme kuralı:** kurula bağlı veriyle çizilen her ekran, veri yokken `null` değil nedenini söyleyen boş durum gösterir;
  yeni kurul açılırken `sinav_dagilimi.json`'a o kurulun dağılımı eklenir.

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

## H101 · Kronometre sayfa değişince kayboluyor, iki sayaç aynı anda açılıyor (2026-10-27)
- **Belirti:** Yüzen kronometre sesli ders / Öğren ekranına geçince kayboluyordu; "Odak" ayrı bir ikinci baloncuk olarak kronometreyle aynı anda çalışabiliyordu; sesli ders oynatıcısıyla üst üste biniyordu.
- **Kök neden:** `KronometreV15` ve `KapsulV15` `TopBarV15` içinde bağlanmıştı; odak ekranlarında üst bar `null` döndüğünden bileşenler sökülüyordu. Odak oturumu ayrı bileşen + ayrı portal olduğu için iki sayaç bağımsızdı. Oynatıcı konumunu bilen bir mekanizma yoktu.
- **Çözüm:** Kronometre uygulama kökünde (`App.tsx`, `V15Icinde`) tek kez bağlanır; Odak panelin sekmesidir (`KapsulV15 gomulu`), biri başlayınca öteki duraklar (`medsoru:sayac`). Baloncuk `.cd-dock`'u izler: mini oynatıcının sağ ucuna kaynaşır, tam oynatıcının sağ üstüne oturur.
- **Kural:** Sayfalar arası kalıcı olması gereken yüzen öğe (sayaç, oynatıcı) asla sayfaya/üst bara bağlı bileşenin içine konmaz; uygulama kökünde tek örnek olarak bağlanır. Aynı işlevin ikinci yüzen örneği eklenmez.

## H102 · Sınav planı Kurul 2'de yanlış puan/plan veriyor (2026-10-27)
- **Belirti:** Kurul 2 aktifken Bitirdiklerim › Sınav planı çok düşük beklenen puan ve gerçek dışı plan gösteriyordu; sesli dersler hiç hesaba girmiyordu.
- **Kök neden:** (1) `sinavPlani.ts` sesli dersi `CD_SPOT_BRANS` ile eşliyordu; bu tablo yalnız Kurul 1 branşlarını bilir, K2 dersleri (`k2noroloji` …) `!b` diye atlanıyordu. (2) İçeriği henüz olmayan branşta (psikiyatri, aile, ftr…) ders listesi boş olduğundan `bransP` = 0 çıkıyor, tüm sorular yanlış sayılıp baraj cezası (−n/2) yazılıyordu.
- **Çözüm:** K2+ için branş `k<kurul><slug>` olarak türetilir ve ders kurulu eşleşmelidir; içeriksiz branşın olasılığı çalışılmamış taban (0,30) alınır.
- **Kural:** Kurul 1 sabit tablolarına dayanan eşleme Kurul 2+ için kurul önekli türetilmeli; içeriği olmayan branş 0 olasılıkla değil taban olasılıkla modellenmeli.

## H102 · Tasarımdaki kayıt adımları (üniversite, sınıf, kurul, hedef) koda geçirilmemişti (2026-10-27)
- **Belirti:** Kullanıcının v15 tasarımında çizdiği giriş sonrası bilgi toplama akışı sitede yoktu.
- **Kök neden:** Ekran denetimi I07–I10'u "DOĞRULANMADI" diye bıraktı; iş yalnız kullanıcının sıraladığı öncelik listesinden yürüdü, denetim tablosundaki DOĞRULANMADI/KISMİ satırları hiçbir zaman iş listesine dönüştürülmedi.
- **Çözüm:** ProfilKurulumV15 (I07–I11) + Profil › Okul ve hedef; denetim belgesine "Değerlendirilmemiş ekranların değerlendirmesi" tablosu (her satıra karar).
- **Kural:** Tasarım geçişinde "DOĞRULANMADI" durumu iş sonu kabul edilmez; her ekran KURULDU / SIRADA / VAR / BİLİNÇLİ / altyapı yok kararından birini alır ve tur sonunda tablo güncellenir.


## Sesli derste geri oku "Ders çalış"a atıyordu (2026-10-27)
- **Belirti:** Sesli ders listesinden bir ders açılıp geri oka basılınca liste yerine "Ders çalış" sayfası açılıyordu.
- **Kök neden:** Ders içindeki geri oku her zaman ders ayrıntı sayfasına (`ders_detay`) gidiyordu; o sayfanın geri bağlantısı da kurul/branş merkezine çıkıyordu. Liste doğrudan derse açıldığı için ayrıntı sayfası hiç görülmeden araya girip yolu bozuyordu.
- **Çözüm / kural:** Uygulama içinden gelindiyse (`navigateTo` `__icGezinti` bayrağını koyar) ok `history.back()` yapar; doğrudan bağlantıyla açıldıysa ayrıntı sayfasına gider. Geri düğmeleri sabit hedefe değil, geldiği yere dönmelidir.

## Sesli derste canlı konum bazen çalışmıyor / bozuk çalışıyordu (2026-10-27)
- **Belirti:** Okunan cümle bazen izlenmiyor, bazen metin yanlış yere atlıyor, "Canlı konuma dön" kendiliğinden çıkıyordu.
- **Kök neden:** (1) Paragraf henüz çizilmemişken kaydırma tek denemeyle vazgeçiyordu. (2) Gizli (display:none) bölmede ölçüm sıfır çıkıp yanlış konuma kaydırıyordu. (3) Yerleşim kaynaklı küçük scroll olayları elle gezinme sayılıp takibi 8 sn durduruyordu.
- **Çözüm / kural:** Eksik öğede kısa aralıkla yeniden dene; sıfır boyutta kaydırma yapma; 3 px altı scroll farkını kullanıcı eylemi sayma. Yeni takip/kaydırma kodu bu üç durumu karşılamalı.

## H117 · Tam ekranda ayar düğmesi araç şeridini göstermiyordu (2026-10-27)
- **Belirti:** Sesli ders tam ekranda sağ üstteki ayar düğmesine basınca şerit açılmıyor, kenarda ince "s." şeridi kalıyordu.
- **Kök neden:** `.cd-pdf-bar` `container-type: inline-size` taşıyor; tam ekranda mutlak konumlanınca genişliği 0'a çöküyordu. Ayrıca `:is(> svg, …)` geçersiz seçiciydi, kural tümden atılıyordu.
- **Çözüm/kural:** tam ekran şeridinde `container-type: normal; width: max-content`; seçici düzeltildi. Mutlak konumlu öğeye `container-type: inline-size` verilirse genişlik açıkça verilir; `:is()` içinde başa combinator yazılmaz.

- **Geri düğmesi gelinen listeye dönmeli (2026-10-27):** Sayfa başlığındaki sabit `geri` hedefi her zaman push yapıp gezinme yığınını bozuyordu (liste→ders→Geri ≠ liste). Geri hedefi için `geriHedefe` kullanılır; sabit hedefe doğrudan `navigateTo` yok.

## H104 · Soru çöz sayfasında Araçlar görünmüyordu (2026-10-27)
- **Belirti:** Masaüstünde Araçlar listesi ekranın altında kesik kalıyor, üç satırdan fazlası görünmüyordu.
- **Kök neden:** `.d15.s15` ekran yüksekliğine sabitlenmişti (`height: calc(100dvh - …)`) ve araç listesi kalan alanda kendi içinde kayıyordu; Test oluştur kutusu büyüdükçe (yeni süzgeç satırları) listeye kalan alan birkaç piksele indi.
- **Çözüm:** Sabit yükseklik kaldırıldı (sayfa normal kayar); özet kartları tek satır, test kutusu sıkı, araçlar ızgara.
- **Kural:** İçerik sayfalarında ekrana sabit yükseklik + iç kaydırma kurma; büyüyebilen içerik (süzgeç, liste) başka bölümü görünmez kılar.

## H106 · Çalışma takvimi (ısı haritası) hücreleri dev görünüyordu (2026-10-27)
- **Belirti:** İstatistiklerim › Çalışma takvimi geniş ekranda ~80 px'lik kutularla sayfayı kaplıyordu.
- **Kök neden:** `.gf15-isi` sütunları `minmax(0, 1fr)` (kart genişliğini paylaşır) + hücre `aspect-ratio: 1` → hücre yüksekliği kart genişliğiyle büyüyor.
- **Çözüm:** Sütun `minmax(0, 16px)` + `justify-content: start`; hücre en çok 16 px.
- **Kural:** Kare hücreli ızgaralarda (ısı haritası, takvim) sütun genişliğine üst sınır koy; `1fr` + `aspect-ratio` birlikte kullanılmaz.

## H107 · "Günlük çözülen soru" çubukları çok genişti; ajan sınama verisi tarayıcıda kalmıştı (2026-10-27)
- **Belirti:** İstatistiklerim › Ayrıntılar'da 14 günlük çubuklar ~82 px genişliğinde; ayrıca 19–27 Ekim arası günde tam 4–5 soru (40 çözüm, 2 deneme) görünüyordu.
- **Kök neden (çubuk):** `.st-col` `flex: 1`, içindeki `.ok/.bad` çubuk sütunun tüm genişliğini alıyor. **Kök neden (veri):** istatistik alt ajanı boş ekranı sınamak için `medsoru_study_progress_v1` / `medsoru_selftest_history_v1`'e sahte kayıt yazdı, "geri aldım" dedi ama kayıtlar tarayıcıda kaldı (sunucuya ulaşmadı: yerel + Oracle `user_data`'da yok).
- **Çözüm:** çubuk `max-width: 24px; align-self: center`. Sahte kayıtlar (hepsi `20:11:00.929Z` damgalı) silindi, eşitleme sarmalayıcısıyla temiz hal yazıldı.
- **Kural:** Alt ajan/ajan, eşitlenen profil anahtarlarına (userKvSync izin listesi) sınama verisi YAZMAZ; sınama gerekiyorsa ayrı anahtar ya da `?demo` bayrağı kullanılır. Ajan raporunda "geri aldım" deniyorsa tarayıcıda doğrulanır.

## H108 · Tablo rozetleri harf harf dikey; Ders seçenekleri kartları uzayıp taşıyordu (2026-10-28)
- **Belirti:** Ders içerik tablolarında "Kayboldu/Azalır" gibi rozetli hücreler harf harf alt alta yazılıyordu. Sesli ders › Ders seçenekleri'nde "Metni dışa aktar" açılınca Cihazda/MP3 kartları dev boyuta uzayıp seçenekler sağa taşıyordu.
- **Kök neden (rozet):** başka bir oturum `dersIcerik.css`'e bir simge için aynı sınıf adıyla `.di15-ik{width:16px;height:16px}` ekledi; rozet `span.di15-ik` 16 px'e sıkıştı. **Kök neden (menü):** `.cd15-mliste > :not(.cd-btn) { display: contents }` sarmalayıcıyı çözünce dışa aktar alt listesi ve PDF düzeni ızgara hücresi oldu; satır `align-items: stretch` ile tüm kartları uzattı.
- **Çözüm:** eski kural `svg.di15-ik` ile kapsandı, rozete `white-space: nowrap; flex: none`. Menüde alt liste/düzen `grid-column: 1 / -1`, ızgara `align-items: start`.
- **Kural:** Yeni CSS sınıfı eklemeden önce aynı adın kullanılmadığını grep'le; kısa ortak adlara (`-ik`, `-ad`) element/üst seçici kapsamı ver. `display: contents` ile çözülen sarmalayıcının açılır alt parçaları tam satır olmalı.

## H122 · Paylaşılan çıkmış soruda süzgeç/kategori alanları öne çıkıyordu (2026-10-28)
- **Belirti:** Özel sohbette paylaşılan çıkmış soru `/cikmis/<id>` ile açılınca liste tek soruya iniyor ama araç çubuğu, yıl/konu giriş kartları ve v12 süzgeç sütunu da görünüyordu.
- **Kök neden:** `sharedId` yalnız soru listesini süzüyordu (`paginatedQuestions`); süzgeç alanları `sharedId`'ye bakmadan çiziliyordu.
- **Çözüm:** `PastExamsView.tsx`'te `sharedId` varken PageToolbar, v15 giriş kartları ve V12Frame gizlenir; "Tüm sorular" düğmesi paylaşım bandında kalır.
- **Kural:** Tek öğeye indirgenen (paylaşım/derin bağlantı) görünümde yeni süzgeç/giriş bileşeni eklenirse `sharedId` ile koşullanır.

## H109 · Aynı cihazda iki sekme açıkken profil eşitleme fırtınası (2026-10-28)
- **Belirti:** İkinci sekme açılınca iki sekme ~25–30 sn boyunca saniyede birden fazla `/api/user-data/backup` + `/api/notes` isteği attı (ölçüm: 25 sn'de 55 istek, her sekmede 17–19 yedek); sunucu 429 döndü, bekleyen gerçek değişikliğin gönderimi reddedilebiliyordu.
- **Kök neden:** (1) `userDataSyncService` yayın kaynağı `ORIGIN` sekme başına üretiliyordu; aynı cihazın öteki sekmesinin gönderimi `user_data_changed` ile "başka cihaz" sayılıp `pullFromServer` başlatıyordu. (2) `lastBackedUpFingerprint` sekme belleğindeydi ama `localStorage` sekmeler arasında ortak: öteki sekmenin yazdıkları bu sekmenin parmak izini değiştirdiği için `pullFromServer` çekmek yerine yeniden yedek gönderiyor, bu da öteki sekmeyi tetikliyordu (ping-pong).
- **Çözüm:** `ORIGIN` cihaz düzeyinde (`medsoru_sync_origin_v1`), son gönderilen parmak izi `localStorage`'da (`medsoru_sync_fp_v1`); ikisi de eşitleme izin listesinde değil. Sınama: iki yeni kodlu sekmede ikinci sekme açılınca ilk sekme 25 sn'de 1 not çekme + 1 yedek (önce 55 istek).
- **Kural:** Sekmeler arası ortak olan duruma (localStorage) bağlı karar verilerini sekme belleğinde tutma; yayın kaynağı kimliği cihaz düzeyinde olmalı. Sınamada eski kodlu açık sekmeleri kapat (yeni/eski sürüm karışımı ölçümü bozar).

## H124 · Soru çözücüde Kurul 2 seçili görünürken Kurul 1 dersleri listeleniyordu (2026-10-28)
- **Belirti:** `/sorular/soru-cozucu` açılınca kurul şeridinde "Kurul 2 · şimdi" vurgulu, ama liste 11 dersi (Kurul 1 + "Kurul 2 …" önekli) birlikte gösteriyordu; şeridin etrafında da boş, geniş bir kutu vardı.
- **Kök neden:** `KurulSecici` adreste kurul yokken vurguyu `varsayilanKurul()`'dan alıyor, `BransBaslangic` ise süzgeci `useKurulParam()`'dan (adres → null = süzgeçsiz) alıyordu; vurgu ve liste iki ayrı kaynaktan besleniyordu. Kutu: `olasi-sorular.css` içindeki kapsamsız `.ks` kuralı aynı sınıf adını taşıyan kurul seçicisine kenarlık/zemin/860 px veriyordu.
- **Çözüm:** çözücü ve En önemliler başlangıcı `useSeciliKurul()` kullanır (vurgulanan kurul = listelenen kurul), "Tümü" kaldırıldı, ad önekindeki "Kurul N" atılır, başlanmış dersler önde sıralanır. Olası sorular şeridi `.ks.kseridi` olarak kapsamlandı.
- **Kural:** seçili durum gösteren bir bileşen ile içeriği süzen kod AYNI kaynaktan (aynı kanca) okur; görsel vurgu için ayrı varsayılan hesaplanmaz. Ortak bileşenlerin sınıf önekleri (`.ks`, `.kh`) başka sayfa CSS'inde kapsamsız kullanılmaz.

## H110 · Çıkmış sorular yıl çipi 21, listede 20 soru (2026-10-28)
- **Belirti:** 2025–2026 çipi "21" gösteriyor, çipe basınca liste 20 soru veriyordu.
- **Kök neden:** `PastExamsView.girisGruplari` (yıl/ders çipleri) yalnız kurul süzgecini uyguluyordu; liste ise `facetPass` zincirinin tamamından geçiyor (varsayılan `quarantineFilter='standard'` karantina, Dönem 3 dışı ve gizli soruları eler; arama ve diğer süzgeçler de). Çip, listenin hiç göstermeyeceği soruyu sayıyordu.
- **Çözüm:** çip sayımı aynı `facetPass` + arama ile; yalnız çipin kendi boyutu (yıl çipinde `year`, ders çipinde `discipline`) hariç tutulur (yönlü süzgeç kuralı). Sınama: 12 yıl çipinin toplamı 502 = liste; 2023-2024 çipi 26 → liste 26.
- **Kural:** Süzgeç çipi/rozetindeki sayı, o çip seçilince listenin göstereceği sayıyla aynı yoldan (aynı süzgeç zinciri) hesaplanır; ayrı, eksik bir sayım yazılmaz.

## H127 — Yıldızlı paragraflar: Bugün'de yok, silinen geri geliyor, sesli derste tüm dersler listeleniyor (2026-10-28)
- **Belirti:** Öğrenci yıldızladığı paragrafları Bugün sayfasında göremedi ("internete kaydedilmiyor" sandı); sesli ders içindeki panel 108 kaydın tamamını (başka kurul/derslerin asistan kayıtları dahil) gösterdi.
- **Kök neden:** (1) Bugün sayfası (`FavorilerBugun`) yalnız `favoriStore`'u okuyordu; `medsoru_yildizli_paragraflar_v1` hiç bağlanmamıştı — kayıt eşitleniyordu ama erişim yolu yoktu. (2) `userKvSync` birleştirmesi iki cihazın listesini birleşim (union) ile kuruyordu; silme iz bırakmadığı için çıkarılan yıldız öbür cihazdan geri diriliyordu. (3) `CanliDersDers` paneli ders süzgeci olmadan açılıyordu.
- **Çözüm/kural:** Bugün'e kurul→ders→konu gruplu yıldızlı paragraflar bölümü eklendi; silme artık `silindi` mezar taşıyla yazılır ve birleştirmede aynı kimlikte en yeni `tarih` kazanır; sesli ders paneli `dersKey` ile varsayılan "Bu ders" kapsamında açılır ("Tüm dersler" seçilebilir). Yeni bir kişisel liste deposu eklenirken: (a) Bugün/Listeler erişimi, (b) silme mezar taşı + en yeni kazanır birleştirmesi, (c) bağlam içinden açılan panelde bağlam süzgeci zorunludur.

## H111c · Esc uygulama tam ekranından çıkarmıyordu (2026-10-28, ortak kabuk)
- **Belirti:** Kabuktaki "Tam ekran" düğmesine basılınca üst çubuk gizleniyor; native tam ekranın açılmadığı durumlarda (dokunmatik/klavyeli cihaz — iPad + klavye, dokunmatik dizüstü — ya da tarayıcı isteği reddettiğinde) Esc'e basmak hiçbir şey yapmıyordu, kullanıcı çıkışı yalnız küçük "Tam ekrandan çık" hapında arıyordu.
- **Kök neden:** Uygulama tam ekranı = `html.is-app-fullscreen`. Kaldırılması yalnız düğmeye ya da native `fullscreenchange` olayına bağlıydı; native katman yoksa Esc'i dinleyen hiçbir kod yoktu.
- **Çözüm:** `src/utils/fullscreen.ts` › `installEscExit` — tek genel `keydown` (bubble, `defaultPrevented`/yazı alanı/açık pencere-menü/sayfa içi tam ekran katmanı/`tam-katman`/`cd-tam-ekran` varken dokunmaz) sınıfı kaldırır ve `medsor:fullscreenchange` yayar. Tarayıcıda sınandı: aç → Esc → kapandı, düğme "Tam ekran"a döndü.
- **Kural:** Native tam ekranın yedeği olan her CSS kipi kendi Esc çıkışını taşır; Esc önce açık pencereye/katmana aittir.

## H111g · İzleme hızı kaydırıcısı: dokunma hedefleri 10–19 px, boş durumda imleç metinle çelişiyordu (2026-10-28, Sınav planı/Bitirdiklerim)
- **Belirti:** Telefonda hız durakları (1×…2,5×) 19 px, kaydırıcı rayı 10 px yüksekti; seçim yokken metin "kalan süre 1× gösteriliyor" derken imleç 1,5×'te duruyordu.
- **Kök neden:** `IzlemeHizi.tsx` boş değer için `?? 1.5` kullanıyordu; `takip.css` rayın ve durakların görünür boyutu dokunma alanı olarak bırakılmıştı.
- **Çözüm:** boş durumda imleç 1×; ray `padding: 9px 0` + `background-clip: content-box` (görünüş aynı, 28 px dokunma), duraklara `::before` ile 40 px dikey alan + `min-width: 40px`. Bugün akışındaki "Tümü" bağlantısı (14 px) negatif kenar boşluklu 40 px alana alındı (`today.css .t15-more`). Takvim, kronometre ve tam ekran ayarlarındaki `kre-tgl` anahtarlarına `aria-label` eklendi (adsız düğme).
- **Kural:** Görünür öğe küçük olabilir ama dokunma alanı ≥40 px (dolgu/`::before`); yer tutucu değer ile açıklama metni aynı varsayımı göstermeli; her `role="switch"` düğmesinin erişilebilir adı olur (label içi olmak yetmez).

## H111h · PC'de açıklama metinleri 120–160 karakter satır uzunluğunda (2026-10-28, okunabilirlik)
- **Belirti:** 1440 px'te Sınav planı açıklamaları (`sp-acikla`, `ss-acik`, "Bu sayılar nasıl hesaplanıyor?" listesi) ~130, Sağlık kaynakçası ~160, Topluluk kuralı ~116, Arka plan notu ~108 karakter satır.
- **Kök neden:** metin blokları kart genişliğini dolduruyor, ölçü (`max-width: ..ch`) yoktu; bir kısmı 12,5–13,5 px idi.
- **Çözüm:** `takip.css` `.sp-acikla/.ss-acik` 14 px + 72ch, `.sp-nasil ul` 75ch (özet 40 px), `cevrimdisi.css .cv-not` 14 px + 72ch, `saglik.css` kaynakça 90ch, `topluluk.css .tp15-kural` 75ch.
- **Kural:** Gövde/açıklama metni ≥14 px ve satır ≤ ~75ch; geniş kartın içindeki paragraf `max-width` ile sınırlanır.

## H111p · Sesli derste hatalı adreste sunucu hata kodu ham gösteriliyordu (2026-10-28, Ders çalış)
- **Belirti:** `/dersler/canliders/kurul1/<eski/hatalı anahtar>` açılınca ekranın ortasında yalnız küçük harfle "geçersiz ders" yazıyordu.
- **Kök neden:** `CanliDersDers.tsx` hata durumunda `fetch` hatasının `message` alanını (sunucunun iç kodu `{error:'geçersiz ders'}`) olduğu gibi basıyordu.
- **Çözüm:** "geçersiz ders / bulunamadı / 400 / 404" öğrenciye "Bu adreste bir sesli ders yok. Bağlantı eski ya da hatalı olabilir; listeden dersi seçebilirsin." olarak çevrilir; liste düğmesi kalır.
- **Kural:** Sunucu hata kodu (`error` alanı) öğrenci metni değildir; ekranda bilinen hatalar Türkçe açıklamaya çevrilir, bilinmeyen hata için genel cümle kullanılır.

## H111q · Sesli ders telefonda: başlık 75 px'e sıkışıyor, Kalem düğmesi eziliyor, bölme hızlı düğmeleri 23×21 px (2026-10-28, Ders çalış)
- **Belirti:** 375 px'te üst bar başlığı "Tümör …" (75 px), PDF şeridinde Kalem düğmesi 25 px'e ezilip boş daire görünüyor, dosya adı 18 px'e inip "1…" kalıyordu; Metin/PDF ayracının hızlı düğmeleri (35/50/65, yön, sıfırla) dokunmatikte 23×21 px.
- **Kök neden:** `.cd15-ad` tek satır `nowrap` + yanında 4–5 sabit simge düğmesi; `.cd15-pb` `flex: none` almadığı için `flex-shrink` ile küçülüyordu; `.cd-pdf-ad` dar kapta gizlenmiyordu; `.cd-ayrac-hizli button` için dokunmatik boyutu yoktu.
- **Çözüm:** `styles/v15/sesli.css` telefonda başlık iki satıra sarılır (16 px, line-clamp 2); `.cd15-pb { flex: none; min-width: 32px }`; `@container (max-width: 460px)` dosya adı gizli. `canli-ders.css` `(pointer: coarse)` hızlı düğmeler 36×36.
- **Kural:** Esnek şeritteki simge/düğmeler `flex: none` alır, yalnız metin öğesi küçülür; metin öğesi 40 px altına inecekse gizlenir ya da sarılır.

## H111r · Soru haritası hücrelerinde yazı kontrastı 2.6–4.0 (2026-10-28, Soru çöz)
- **Belirti:** `/sorular/soru-haritasi` ısı tablosunda orta yoğunluktaki hücrelerin sayıları zor okunuyordu (WCAG AA altında, açık ve koyu temada).
- **Kök neden:** renk yoğunluğu %12–90 arası sürekli ölçekti; %40–85 aralığında zemin orta mavi olduğundan ne koyu (`ink`) ne açık (`on-accent`, eşik %55) yazı 4.5'i geçebiliyordu.
- **Çözüm:** `SoruHaritasiV15.tsx` ölçeği iki banda ayırır: açık bant %10–40 (koyu yazı), koyu bant %90–100 (açık yazı); ara ton kullanılmaz. DOM kontrast ölçümü: 7 ihlal → 0.
- **Kural:** Yoğunluğa göre boyanan hücrede yazı rengi tek eşikle seçiliyorsa, eşiğin iki yanındaki zemin tonları her iki yazı rengiyle de 4.5'i geçmelidir; geçmiyorsa ara tonlar atlanır.

## H111s · Zihin haritası numaraları koyu temada okunmuyordu (2026-10-28, Ders çalış)
- **Belirti:** Koyu temada `/dersler/zihin-haritasi` liste numaraları (1, 2, 3…) koyu zemin üstünde 1.7–2.0 kontrastla neredeyse görünmüyordu.
- **Kök neden:** `.zh15-no` yazı rengi tema bağımsız sabit `oklch(0.45 …)`; zemin `--color-white` ile karıştığı için koyu temada koyulaşıyor, yazı koyu kalıyordu.
- **Çözüm:** `zihin.css` `:root.theme-dark .zh15-no { color: oklch(0.84 0.09 var(--t)) }`.
- **Kural:** Sabit `oklch()/hex` yazı rengi yalnız token zeminiyle birlikte koyu tema karşılığı yazılarak kullanılır.

## H111t · Ders çalış dokunma hedefleri: "Tüm dersler" 75×14, Öğren "▶ Dinle" 52×20 px (2026-10-28, Ders çalış)
- **Belirti:** Dersler merkezinde "Tüm dersler" bağlantısı ve Öğren adımındaki "▶ Dinle" düğmesi telefonda parmakla zor seçiliyordu.
- **Kök neden:** `.d15-more` yalnız metin yüksekliğindeydi (line-height 1); `.ls-tag` 20 px rozet stili düğmeye de uygulanıyordu.
- **Çözüm:** `dersler.css .d15-more` 40 px dolgu + negatif kenar (H111g ile aynı desen); `LessonPlayer.tsx` düğmeye `ls-dinle` sınıfı, `v12/lesson.css` dokunmatikte `::before` ile 40 px alan.
- **Kural:** H111g kuralı: görünür öğe küçük kalabilir, dokunma alanı ≥40 px.

## H131c — v16 kabuğu her alt yol değişiminde sayfayı yeniden kuruyordu (2026-10-28)
- **Belirti:** Satır çekmecesi açıp kapatınca liste baştan çekiliyor, kaydırma/sayfa kayboluyor, odak satıra değil `<main>`'e dönüyordu.
- **Kök neden:** `ManageV16.git()` her çağrıda `gezinti` sayacını artırıyordu; sayfa `key`'i buna bağlı olduğundan alt yol (`/sorular/cikmis/<id>`) değişimi de yeniden bağlama demekti; ardından `<main>` odaklanıyordu.
- **Çözüm/kural:** Aynı sayfa içinde yalnız alt yol değişirse sayfa yeniden kurulmaz, odak/kaydırma korunur (aynı adrese yeniden tıklama sıfırlar). Çekmece açma 1 istek (önce liste + ayrıntı).

## H131d — Dar ekranda süzgeç çipleri tabloyu ekran dışına itiyordu; kesik süre hücreleri (2026-10-28)
- **Belirti:** 375 px'te Çıkmış sayfasında süzgeçler (Ders ~40, Yıl ~20 seçenek) 1,5 ekran kaplıyordu; 1440 px'te Kişiler "7 gün/Çalışma" hücreleri "3 sa 14 …" diye kesiliyordu; dokunmatikte düğme/çip 22–30 px, iOS'ta 13,5 px girdiler odakta yakınlaştırıyordu.
- **Kök neden:** `.m16-cip-grup` `flex-wrap: wrap`; sabit 80–96 px sütunlar "N sa M dk" biçimine dar; kit dokunmatik ölçüsü tanımlamıyordu.
- **Çözüm/kural:** Her süzgeç grubu tek satır yatay kaydırılır (etiket sabit); süre sütunları ≥100 px, kesilen düz metin hücresi `title` taşır; `@media (pointer: coarse)` düğme/ara/girdi 40 px, çip 32 px, alan yazısı 16 px. Kısa değer (≤14 karakter) hücrede kesilmez — tarama betiği bunu denetler.

## H139 — Gizlenen sayfaya giden bağlantı öğrenciyi açıklamasız Bugün'e atıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** /kamplar'daki "Kamplar" sekmesi, takvimdeki T-5 adımı, Bugün'deki "Günün spotu", `/olasi-sorular` tıklanınca Bugün açılıyordu; öğrenci neden olduğunu anlamıyordu.
- **Kök neden:** Merkez kartları `menudeGorunur` ile süzülüyordu ama sekmeler, takvim adımları ve Bugün bağlantıları süzülmüyordu; App.tsx gizli sayfayı sessizce `setActiveTab('today')` ile değiştiriyordu.
- **Çözüm/kural:** Sekmeler (`gorunenSekmeler`), takvim hazırlık adımları ve Günün spotu bağlantısı `menudeGorunur` ile süzülür; adresle girilen gizli sayfa "Bu sayfa şu an kapalı" ekranı + Ne yapmak istiyorsun kartlarını gösterir. Bir sayfaya bağlantı veren her yer `menudeGorunur(route)` denetler.

## H140 — Bazı sayfalar aktif kurul yerine Kurul 1 ya da "Tümü" ile açılıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Aktif kurul 2 iken Kazanımlar Kurul 1, Örnek sorular tüm kurulları karışık (sayaçlar yalnız k1-), Test oluştur "Tümü" ile açılıyordu; Öncelikli dersler Kurul 1 olduğunu söylemiyordu.
- **Kök neden:** Sayfalar varsayılanı sabit `1`/`'all'` yazmıştı; `varsayilanKurul()` (son seçim → takvim) kullanılmıyordu.
- **Çözüm/kural:** Kazanımlar, Örnek sorular (kurul seçici + kurul önekli sayaçlar), Test oluştur (kayıtlı ölçüt yoksa) `varsayilanKurul()` ile açılır; yalnız Kurul 1 verisi olan Öncelikli dersler bunu başlıkta yazar. Yeni kurul bağımlı sayfa varsayılanını `varsayilanKurul()`dan alır.

## H144 — Deneme ekranında soru numarası çubuğuna dokunulamıyordu; telefonda süre gizliydi (2026-10-28, sayfa denetimi)
- **Belirti:** 20 soruluk denemede soru düğmeleri 6 px yüksekliğindeydi (telefonda 7×6 px); 420 px altında süre göstergesi tamamen kayboluyordu.
- **Kök neden:** Görünen çizgi ile dokunma alanı aynı öğeydi (`button { height: 6px }`); dar ekranda yer açmak için süre gizlenmişti.
- **Çözüm/kural:** Düğme 24 px dokunma alanı, görünen çizgi `::before`; telefonda süre kalır, doğru/yanlış sayaçları kalkar (soru numarası çubukta). İnce göstergelerde dokunma alanı görsel çizgiden ayrı tutulur.

## H145 — Örnek sorularda "Başla" düğmesi harf harf dikey yazılıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Masaüstü ders listesinde her satırda B-a-ş-l-a alt alta, satır ~160 px uzuyordu.
- **Kök neden:** v15 kart eylemi (`.ks15-eylem`) v12 satır ızgarasında alan (`grid-area`) almadığı için kendiliğinden 30 px'lik numara sütununa yerleşiyordu.
- **Çözüm/kural:** Izgaraya `ey` alanı eklendi (masaüstü sağ sütun, telefonda ayrı satır). Izgara satırına yeni öğe ekleyen her katman ona alan tanımlar.

## H147 — Öğrenci menüsünde hesap ve ders sayfaları yanlış gruplardaydı (2026-10-28, sayfa denetimi)
- **Belirti:** Başarımlar Oyunlar'da, Güncelleme günlüğü Başvuru'da aranıyordu; Öncelikli dersler ve Geçmiş kurullar Başvuru'daydı ve telefonda alt sekmede "Menü" yanıyordu.
- **Çözüm/kural:** Öncelikli dersler + Geçmiş kurullar → Ders çalış (merkez, menü, alt sekme "Ders"); Başarımlar + Güncelleme günlüğü → Kişisel. Grup değişikliği `merkezModel.MERKEZ_HAM`, `navModel.NAV_TREE_HAM` ve `navV15` (OYUNLAR/KISISEL) birlikte yapılır; adresler değişmez.

## H148 — Ders çalış merkezinde "hepsini bitirdin ya da henüz ders yok" ikili mesajı (2026-10-28, sayfa denetimi)
- **Belirti:** Kurul 2'de hiç sesli ders yokken öğrenciye "hepsini bitirdin ya da henüz ders yok" deniyordu; yapılacak bir şey önerilmiyordu.
- **Çözüm/kural:** Kurulda ders var ve hepsi bitti → "hepsini bitirdin" + tüm dersler bağlantısı; ders yok → "henüz eklenmedi" + önceki kurula geçiş. Boş durum metni iki ayrı durumu tek cümlede birleştirmez, bir eylem verir.

## H149 — Aramada "Sesli derste geçen yerler" stilsiz görünüyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Ders adı ile cümle parçası bitişik ("Patolojiye GirişFormalin…"), zaman damgası metne yapışık.
- **Kök neden:** `SesliYerler.tsx`'te `import '../../styles/sesli-yer.css'` satırı dosya başındaki `/** … */` yorum bloğunun içine düşmüştü; stil dosyası hiç yüklenmiyordu (derleme hata vermez).
- **Çözüm/kural:** İçe aktarma yorumun dışına alındı; depoda aynı kalıp tarandı (başka yok). Belge yorumunun içine kod satırı eklenmez; stil "kural var ama uygulanmıyor" görünüyorsa önce içe aktarmanın gerçekten çalıştığına bakılır.

## H150 — Güncelleme günlüğünde öğrenciye dosya yolları görünüyordu (2026-10-28, sayfa denetimi)
- **Belirti:** "Geliştirme notları" kapalıyken bile öğrenci maddelerinde `meds/scripts/...`, `*.json` gibi yollar vardı.
- **Kök neden:** Öğrenci maddeleri (`ogrenci`) sürüm notlarından üretilirken teknik ayrıntı temizlenmiyordu; ekran olduğu gibi basıyordu.
- **Çözüm/kural:** Ekran öğrenci maddelerinden kod parçasını, dosya yolunu ve yollu parantezi siler; 3 kelimeden kısa kalan maddeyi göstermez. `guncelleme_notu.json` maddeleri öğrenci diliyle yazılır, dosya yolu içermez.

## H151 — Sağlık Bakanlığı uzun bölümlerinde başa dönüş yoktu; geçmiş düğmesi küçüktü (2026-10-28, sayfa denetimi)
- **Belirti:** Aşı bölümü telefonda ~17.000 px; yukarı dönmenin tek yolu kaydırmaktı. "N yılın geçmişini göster" düğmesi 49×18 px.
- **Çözüm/kural:** 1200 px aşağıda "Başa dön" düğmesi (kaydırılan kabı olaydan bulur); geçmiş düğmesine `::after` ile ~57×34 dokunma alanı. Not: "Kaynak N" bağlantıları zaten `::after` ile büyütülmüştü, tarama aracı bunu göremez (yanlış bulgu).

## H154–H169 — Sayfa denetimi dördüncü tur, öğrenci sitesi orta bulguları (2026-10-28)
- **H154/H155 Kutlama:** kuyruk hangi ekranda olursa olsun hemen açılıyordu → deneme, çıkmış testi, soru çözücü ve sesli ders ayrıntısında ertelenir. Rozetteki "3" ödül seviyesiydi, "Hepsini geç" sayısı bu ödülü saymıyordu → "3. seviye" ipucu, sayaç tüm kuyruk.
- **H156 Bugün:** halka öğrencinin çalışmasını, alt kart okul programını gösteriyordu (farklı veri, aynı dil) → "bugün çalışma yok" / "Okuldaki bugünkü 2 ders sona erdi".
- **H157 Deste sayısı:** merkez yayında olmayan desteleri de sayıyordu → kitaplıkla aynı ölçüt (`isPublished`, `kurulOf`).
- **H158 Sesli ders süzgeci:** "2026–27/2025–26" etiketleri telefonda satırı taşırıyordu → "Bu yıl/Arşiv"; boş listede "Geçen yılın derslerini aç".
- **H159/H160 Soru çöz kartları, Yanlışlarım:** uzun etiket/kırılan düğme → kısa ad, tek satır; boş Yanlışlarım'da "Soru çözmeye başla".
- **H161 Boş Check Up:** düz metin → başka kurulun check-up'ı ve hazırlık araçlarına düğme.
- **H162 Kazanım "8/2":** veri doğruydu ("0/2"); sabit genişlikli yazı tipinin çizgili sıfırı 8 okunuyordu → normal yazı tipi + tabular rakam. Sayaçta mono yazı tipi kullanılmaz.
- **H163 Sınav planı hız çipleri:** 40×19 px → ≥32 px.
- **H164 /profil:** /ayarlar ile aynı ekran → adres /ayarlar'a döner (eski bağlantı çalışır).
- **H165–H167 Boş durumlar:** İstatistik (çalışmaya başla), Sıralama (Üniversiteni seç), Arkadaşlar (Giriş yap: App.tsx `medsoru:giris-ac` olayı).
- **H168 Bildirimler:** eylem satırı kırılmıyordu ("Ok" kesik); silinemeyen okunmuşlar "temizle"yi etkin tutuyordu → satır sarar, düğme yalnız silinebilir varken etkin.
- **H169 Telefonda kurul:** üst çubukta kurul yolu yoktu → kompakt "K2" çipi.
- Masaüstü 24 px alt şerit uygulamada yeniden üretilemedi (tarama aracının boyut geçişi kalıntısı); değiştirilmedi.

## H200–H212 — Sayfa denetimi beşinci tur, öğrenci sitesi kalan bulgular (2026-10-28)
- **H200/H201/H205/H210 Sınava hazırlan:** boş "Planlama" başlığı yalnız içerik varken; sınav ağırlığı kartı nereye gittiğini söylüyor; olası sorular kartı ATP kilidini önceden yazıyor; telefonda sekme şeridi kenarda solar.
- **H202/H203 Soru haritası:** yılı belirsiz "?" sütunu renk ölçeğine katılıp en koyu hücreleri alıyordu → "Yılsız", sona alındı, ölçek dışı; telefonda yana kaydırma ipucu. Kural: belirsiz/eksik kategori renk ölçeğini belirlemez.
- **H204** Çıkmış arama yer tutucusu telefonda kesikti → anahtar sözcük önde.
- **H206/H207 Sesli ders:** küçült düğmesi `::after` ile ~44 px; bölme hap düğmeleri ≥28 px + aria-label.
- **H208** Hastalık dipnotları `::after` dokunma alanı.
- **H209 Çift başlık:** v15'te sayfa adı hem üst çubukta hem `PageHeader` h1'de görünüyordu → v15'te PageHeader başlığı görsel olarak gizli (ekran okuyucu için h1 kalır). Site geneli kural; yeni sayfa başlığı v15'te üst çubuktan gelir.
- **H211/H212 Sağlık:** açıklamasız sayı rozetleri dipnot biçiminde ("[14]"); "15 yıl" → "15 yıllık geçmiş".

## H220 — Üç sayfa aynı "bugün ne yapayım" işini bölüyordu (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Belirti:** Bugün (plan halkası, akış, hafta çubukları), Çalışma masam (hafta şeridi, günün etkinlik akışı, bugünkü süre, seri + soru çalışma alanı) ve Ders çalış merkezi (devam et) aynı soruya üç ayrı yerden cevap veriyordu; iki ayrı hafta görünümü vardı.
- **Kök neden:** Çalışma masamın v15 üst bölümü (`MasaGunV15`) Bugün'den bağımsız tasarlanmış, sonra Bugün'e hafta çubukları eklenmişti; sayfaların görev sınırı tanımlı değildi.
- **Çözüm/kural (görev sınırı):**
  - **Bugün** = günün tek sayfası: plan halkası → Kaldığın yerler (araçlar arası devam) → hafta şeridi + Bugün yaptıkların (`MasaGunV15 gomulu`; yan kartlar gizli, süre/seri halkada ve şeritte). Hafta çubukları kaldırıldı.
  - **Listelerim ve notlar** (eski Çalışma masam, `/calis` aynı) = yalnız kişisel soru çalışma alanı (Soru çöz, Test, Listelerim, Notlar).
  - **Ders çalış merkezi** = ders araçları merkezi; "Devam et" yalnız sesli ders içindir.
  - Yeni "günlük özet" öğesi yalnız Bugün'e eklenir; diğer sayfalar kendi aracının durumunu gösterir.

## H239–H241 — Ders programı: import.meta.glob anahtarı + numara eşleşmesi (2026-10-28)
- **Belirti:** /dersler/program'da Kurul çipleri hiç yoktu; Kurul 1 açılınca "Invalid Date" başlığı.
- **Kök neden:** `import.meta.glob` anahtarları globu çağıran dosyaya göredir (`services/programVeri.ts` → `../data/…`); bileşen `../../data/…` arıyordu. Sesli ders eşlemesi arşiv önekini atıp yalnız `kN-NN` numarasına bakıyordu (yıllar arası numara kesin değil). Tarihi boş kayıt `tarihYaz('')`'a gidiyordu.
- **Kural:** glob kaydını başka dosyadan sorgulama, kaynağın yardımcısını (`programVar`) kullan; ders↔sesli bağlantısı yalnız `ders_id_tam` birebir başlangıcıyla; boş tarih ayrı etiketle.

## H242 — Çıkmış listesinde konum yoktu; geri dönünce liste baştan açılıyordu (2026-10-28, kullanıcı isteği)
- **Belirti:** Varsayılan Kart görünümü sonsuz kaydırmaydı (20'şer yükleme, en çok 60 kart penceresi); kaçıncı soruda olunduğu görünmüyor, bir soruya ya da başka sayfaya gidip dönünce liste ilk 20 soruyla açılıyordu. Kompakt görünümde yalnız "3 / 26" vardı.
- **Kök neden:** Konum yalnız bileşen durumunda (richLimit/currentPage) tutuluyordu; bileşen kalkınca kayboluyordu. Kaydırmayla ilerleyen pencere sayfa kavramı taşımıyordu.
- **Çözüm/kural:** Liste/Panel yerleşiminde iki görünüm de sayfalı (Kart 20, Kompakt 25): üstte "41–60 / 571 soru · sayfa 3/29", altta Önceki · sayfa seçici · Sonraki (`cikmis/CikmisSayfa.tsx`). Konum (süzgeç imzası + sayfa + sayfadaki sıra) `sessionStorage cikmis_konum`'a yazılır; dönüşte aynı sayfa açılır ve aynı soru yapışkan üst çubuğun altına yerleşir. Tuzaklar: rotadan çıkarken yapılan "başa kaydır" kaydı bozar (kayıt yalnız çıkmış adresindeyken), `scrollIntoView` yapışkan çubuğun altına gizler (ölçüm ve yerleştirme `.v15-top` alt çizgisine göre), geri yükleme birkaç kez yerleştirilir ve bitene dek kaydedilmez. Uzun liste ekranlarında konum sayfa + sıra olarak saklanır.

## H300–H311 (öğrenci) — Çevrimdışı ve Arka plan işleri aynı işi iki sayfada yapıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** "Yalnız Wi-Fi" iki sayfada iki farklı denetimle (anahtar / onay kutusu), eşitleme kartı ve indirilenler iki kez; Arka plan işlerinin menüde belirsiz karşılığı.
- **Çözüm/kural:** Tek sayfa "Çevrimdışı ve indirmeler" (`/cevrimdisi`): durum → indirme kuyruğu ve arka plan işleri (`#isler`, ArkaPlanV15 gömülü) → toplu indir → indirilenler ve depolama → ayarlar ve eşitleme (tek Wi-Fi denetimi, aynı `ayar.wifi` anahtarı). `/arka-plan`, `/arka-plan-isleri` → `/cevrimdisi#isler`. Bir ayar sitede tek yerde düzenlenir.

## H330–H334 — Sesli ders araç çubukları kalabalıktı (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Belirti:** Masaüstünde üst çubukta 11 düğme (görünüm, A−/A+, yıldız, bilgi, tam ekran, ayar, ⋯), PDF çubuğunda Çıkmış/Kalem/tema/zoom; telefonda üstte 4 simge.
- **Çözüm/kural:** Görünür kalanlar ders boyunca sık dokunulanlar: görünüm kipi, tam ekran (masaüstü), Çıkmış, Kalem, yakınlaştırma (masaüstü). Seyrekler `CdTasmaMenu` ⋯ menüsünde: yazı boyutu (menü açık kalır, değer yazar), yıldızlı paragraflar, terim yardımcısı (✓; açıkken çubukta etkin göstergesi), görünüm ayarları, tüm ders seçenekleri, tam ekran; PDF ⋯: sayfa teması, yakınlaştır/uzaklaştır/sığdır. Menü erişilebilir (aria-haspopup, ↑/↓/Home/End, Esc/dışarı/Tab kapatır, odak düğmeye döner), kısayollar değişmedi, tanıtım turu yeni hedeflere bağlandı (9/8 durak). Çizim/zamanlama mantığına dokunulmadı (kural 17/18). Açık: TV kipinde menü ok tuşları TV katmanına takılabilir; telefonda Kalem 33 px, küçült düğmesi 36×22 px.
- **Kural:** Sesli ders ekranına yeni düğme eklenirken önce sık/seyrek kararı verilir; seyrekse ⋯ menüsüne girer, durum taşıyorsa menüde ✓ ve çubukta etkin göstergesi olur.

## H335–H337 — TV kipinde ⋯ menüsü ve ders ekranında TV kumandası (2026-10-28)
- **H335 Belirti:** TV kipinde ⋯ menüsü açıkken Esc menüyü kapatmıyor, odak menüden düşüyordu; Geri tuşu (GoBack/461/10009) menüyü hiç kapatmıyordu.
- **Kök neden:** TV kumanda dinleyicisi pencere düzeyinde yakalama aşamasında (capture) Esc/Geri'yi alıp odağı bırakıyordu (menünün belge düzeyi dinleyicisinden önce çalışır); menü yalnız `Escape`'i tanıyordu.
- **Çözüm/kural:** Odak `[role="menu"]` içindeyse TV katmanı tuşu menüye bırakır; menü Geri tuş kodlarını da kapatma sayar. Düzeltmeli/düzeltmesiz karşılaştırmayla doğrulandı. Kural: pencere düzeyinde capture dinleyici yazan her katman açık menü/diyalog içindeki tuşları bırakır.
- **H337 Belirti:** Ders ekranında TV kumanda gezinmesi ve kumanda tanıtımı hiç çalışmıyordu.
- **Kök neden:** `cbff0844`'te başlık yeniden yazılırken `<CdTvKumanda />` kaldırılmış, `import` kalmıştı (derleme uyarı vermez).
- **Çözüm/kural:** Bileşen ders ekranına geri bağlandı (TV dışında hiçbir şey çizmez), Kumanda düğmesi köşeye sabit. Kullanılmayan içe aktarma, kaybolmuş bir özellik işareti olabilir; büyük başlık yeniden yazımlarında eski bileşenlerin hâlâ çizildiği kontrol edilir.
- **H336:** PDF şeridindeki Kalem ve Çıkmış düğmeleri dokunmatikte `::after` ile ~44 px dokunma yüksekliği (görünüm aynı). "Oynatıcıyı küçült" zaten H206 ile 44 px'ti; tarama `::after`'ı göremediği için küçük ölçüyordu.

## H340–H347, H360–H374 — Sayfa denetimi düşük önemli bulgular (2026-10-28)
- **Öğrenci (H340–H347):** boş Notlarım'da arama kutusu gizli; bildirim yokken toplu eylemler gizli; müzik ilerleme çubuğu 28 px; Bugün şerit etiketi tek satır; arama sıralama seçici 36 px; sınav planında gereksiz "· K2" eki; topluluk ders yorumları boş durumuna "Derslere git"; İlk adımlar ilerleme çubuğu belirgin.
- **Yönetim (H360–H374):** serbest girdiden soruya, olası sorudan ayrıntıya, ses işinden sesli derse, desteden derse, oyuncudan kişiye bağlantı; Gelen kırıntısı "Yönetim › Gelen"; ders sekmesi (`?sekme=`), kurul ve kamp çekmecesi (`?ac=`) adreste; kurul takvimi bildirimi "dağıtımda yansır"; çöp kalıcı silme onayında hedef; görünürlükte "bayrağa git"; Puan/ATP tehlikeli işlemler açık listeyle (`ozel_kaldir` artık uyarılı); şikâyet sayfasında "Gizlenen mesajlar" kartı; Gelen "Ek" sütunu varsayılan gizli.
- **Kural:** Tehlikeli işlem ad kalıbıyla değil açık listeyle belirlenir (H182, H372). Açık çekmece/sekme adreste tutulur ki yenileme ve paylaşım aynı görünümü açsın.
- Açık öneriler (yapı): menü/başlık ad eşleşmeleri, `kurul_2` adres biçimi, yinelenen girişler (KMB, Sözlük/Hastalıklar, takvim), havuz dondurmanın Bayraklar'a taşınması, ses kuyruğunun sesli ders sekmesi olması, sürüm notu + dağıtım bilgisinin birleşmesi. Veri: kazanımlarda yinelenen konu 31, soru haritası 498 / çıkmış 502 farkı.

## H388/H389 — Sınıf adı çakışması: Ders çalış çip şeridi ortaya/sağa kayıyordu (2026-10-28, kullanıcı bildirdi)
- **Belirti:** Ders çalış merkezinde "Kurul 2" düğmesi ekranın ortasında, branş çipleri en sağda duruyordu (kullanıcı ekran görüntüsü, canlı).
- **Kök neden:** Herkese açık profil/Arkadaşlar stili (`styles/v15/kisi.css`) kök sınıf olarak `.ks15` kullanıyordu (`display:grid; max-width:720px; margin:0 auto`); kurul seçici `KurulSecV15` de `.ks15`. Profil ya da Arkadaşlar sayfası bir kez açılınca stil kalıcı yüklenir ve seçiciye bulaşır: otomatik kenar boşlukları satırdaki boşluğu yutup düğmeyi ortaya, çipleri sağa iter. Yalnız o sayfalardan sonra görüldüğü için tek başına açılan sayfada üretilemiyordu. Aynı tür çakışma `.bd15` (Bildirimler ↔ Bitirdiklerim) için de vardı.
- **Çözüm:** `kisi.css` öneki `apr15`, Bitirdiklerim öneki `btr15`. Canlıda Arkadaşlar → Ders çalış geçişiyle önce/sonra ölçüldü (seçici sol boşluğu 427 px → 0).
- **Kural:** Her v15 ekranının kök sınıf öneki sitede tektir; yeni önek seçmeden önce `grep -rn "\.<önek>\b" src/styles` ile denetlenir (bu oturumda yazılan tarama: aynı kök sınıfı iki dosyada tanımlayan stil yok olmalı). Stil "yalnız bazı gezinme sıralarından sonra" bozuluyorsa önce sınıf çakışması aranır.

## H380–H387 — Kalan küçük öğrenci bulguları (2026-10-28)
- Menü etiketi, sayfa başlığı ve ROUTE_TITLES tek ada eşitlendi (Etkileşimli dersler, Sesli dersler, KMB dersleri, Müzik, Patoloji/TBG Check Up, Havuz doluluğu, Çevrimdışı ve indirmeler); içeriksiz kurul sekmeleri kesikli + "henüz yok"; telefonda kurul şeridi kenar soluklaştırma; sayaçlarda mono yerine tabular rakam; "Karma test · 20 soru" etiketi; testten çıkışta cevap varsa onay; KMB "Hazır/Yakında" ayrımı.

## H400–H406, H420–H424 — Yapı sadeleştirme: yinelenen sayfa ve girişler (2026-10-28, kullanıcı kararı)
- **Öğrenci:** Geçmiş kurullar ayrı sayfası menü/merkezden kalktı; kurul seçicilerde sınavı geçmiş kurul "Geçmiş" etiketli (sınav tarihi ipucu). `/gecmis-kurullar` (+ `/arsiv`…) → `/dersler` (`?kurul=N` → `/dersler/kurulN`). KMB tek kanonik `/dersler/kmb`. Sözlük ↔ Hastalıklar sekme çifti yerine tek "…'a git" bağlantısı. Başvuru'daki yinelenen "Kurul takvimi" kartı kalktı (Sınav takvimi kanonik). Adres okuyucu eski `kurul_N` biçimini `kurulN`/`?kurul=N`'e çevirir (replaceState).
- **Yönetim:** Ses kuyruğu → Sesli ders sekmesi (`ogrenme/sesli?sekme=kuyruk`); Sürüm notu + Dağıtım bilgisi → tek sayfa `site/surum` (dağıtım bölümü `?bolum=dagitim`); Havuz dondurma → Özellik bayrakları bölümü (`site/bayraklar?bolum=dondurma`). Tam yol yönlendirme tablosu `ESKI_YOL` (menu.ts), sabit/son kullanılan listeleri açılışta yeni yola çevrilir, `?bolum=` ile bölüme kaydırma.
- **Kural:** Aynı işi gören ikinci giriş/sayfa açılmaz; birleştirmede bileşen silinmez (yönlendirme + menüden kaldırma), eski adres yeni yere yönlenir ve SITE_HARITASI_KURALLARI.md'ye yazılır.
- **Not:** Kazanımlar ve Kurul kampı artık Geçmiş kurullar sayfasından kurula süzülmüş açılmıyor; kendi kurul seçicileriyle açılıyor.

## H430 — Video oluştur penceresi Ders seçenekleri panelinin altında kalıyordu (2026-10-28, kullanıcı bildirdi)
- **Belirti:** Sesli ders › ⋯ › Tüm ders seçenekleri › "Video oluştur" açılınca pencere panelin arkasında kalıyordu; Esc paneli kapatıp pencereyi de götürüyordu.
- **Kök neden:** Panel ortak `Sheet` (`.sh-sheet-root`, z-index 80), pencere ortak `Dialog` (`ms-overlay`, z-[70]); ikisi de body'ye portal, düşük z'li pencere sonra açılsa da altta kalır. Ayrıca iki bileşen Esc/Tab'ı belgede dinliyordu; önce açılan panel önce tepki verip kapanıyor, içinde çizilen pencere de gidiyordu.
- **Çözüm/kural:** `Dialog` açılışta panel varsa z 85 (yoksa 70); `ActionMenu` açılır menü/eylem sayfası her zaman z 95 (geçici katmanlar en üstte); `Sheet`, odak panel dışında ve üstte bir `ms-overlay` varken Esc/Tab'ı bırakır. Katman kuralı: panel 80 < panel üstü pencere 85 < açılır menü 95; iç içe açılan katmanda klavye en üstteki katmanındır.

## H431 — Odak ekranlarında durum çubuğu ve ana ekran çizgisi payı yoktu (2026-10-28, kullanıcı bildirdi: iPhone)
- **Belirti:** iPhone'da (viewport-fit=cover + black-translucent) açık sesli ders ve açık Öğren destesi başlığı saatin altına giriyordu; sesli ders oynatıcısı ana ekran çizgisine biniyordu.
- **Kök neden:** Kabuk odak ekranlarında kendi üst barını (güvenli alanlı) çizmiyor; ekranların kendi başlığı `.sh-main` 4 px dolgusundan başlıyordu. `.cd-dock` taban kuralındaki `env(safe-area-inset-bottom)` telefon/tablet kurallarında düz 6/10 px ile eziliyordu.
- **Çözüm:** Kök sınıf `v15-odak` (ShellV15) + `.sh-main` üst dolgusu `env(safe-area-inset-top) + 4px`; `.cd-dock` alt dolgusu her kırılımda `+ env(safe-area-inset-bottom)`. Chrome'da `Emulation.setSafeAreaInsetsOverride` (üst 47 / alt 34) ile ölçüldü: başlık 51 px'te, oynatıcı tabandan 40 px yukarıda. **Gerçek iPhone'da sınanmadı**; kullanıcının gördüğü çakışma başka bir ekransa ayrıca bakılacak.
- **Kural:** Kendi üst/alt çubuğunu çizen her ekran güvenli alan payını kendisi alır; medya sorgusunda dolgu yeniden yazılırken `env(safe-area-inset-*)` korunur.

## H432 — Ders PDF ekranı kaydırırken "parçalanıp geri geliyordu" (2026-10-28, kullanıcı bildirdi)
- **Kök neden:** Önizleme iframe'i içerik boyunda (~89.000 px) ve telefonda en az 1000 px genişti; tarayıcı bu dev katmanı karo karo çizip ekran dışını atıyor, kaydırırken karolar boş/kırık görünüp yeniden çiziliyordu (iPhone'da katman belleği düşük). Telefonda belge yana da taşıyordu.
- **Çözüm/kural:** Çerçeve ekran boyunda, belge içinde kayar; dar ekranda belge çerçeve genişliğine `zoom` ile sığar, yazdırmadan önce ölçek kalkar (afterprint ile geri gelir). Ölçüm: telefonda çerçeve 358×642, ölçek 0,358, yatay taşma 0; masaüstünde 1010×694. Önizleme/gömülü belge iframe'i içerik boyuna büyütülmez.

## H433 — iPhone: panel başlıkları ve durum çubuğu çakışması (2026-10-28)
- **Belirti:** Sesli derste "Ders seçenekleri", "Oynatıcı" vb. paneller ve diyaloglar iPhone'da saat/pil çubuğunun altına giriyordu; açık temada saat yazısı beyaz başlıkta görünmüyordu.
- **Kök neden:** (1) `v11.css` genel `[role=dialog]` max-height kuralı (özgüllük 0,3,0) `.sh-sheet`'i eziyor ve güvenli alanı düşmüyordu (panel 820 px, başlık y=43 < 47). (2) `appearance.ts syncPwaChrome` her temada `black-translucent` zorluyordu → beyaz durum yazısı.
- **Çözüm/önleme:** genel kurala `.sh-sheet` istisnası + `env(safe-area-inset-top)` düşümü; `.cd-dlg-kart` aynı. Durum çubuğu stili açık temada `default`, koyuda `black-translucent` (index.html erken betik + syncPwaChrome). Yeni tam yükseklikli katman yazan her kural üst güvenli alanı düşer; SAFE öykünmesiyle (üst 47) başlık ≥47 sınanır.

## H435 — Sıralama: ölçü değişince eski veri yanlış birimle görünüyor, tepki geç (2026-10-29)
- **Belirti:** Sıralamada ölçü/süzgeç değiştirince başka sütunun verileri görünüyor, tepki geç geliyordu.
- **Kök neden:** yeni istek giderken önceki yanıt (`veri`) ekranda kalıyor ve YENİ ölçünün biçimleyicisiyle yazılıyordu (puan sayıları "soru"/"basamak" diye); "Yükleniyor" yalnız liste boşken çıkıyordu. Her geçiş ağ gidiş-dönüşü bekliyordu (sunucu 2–11 ms, gecikme ağ). 
- **Çözüm/önleme:** yanıt istek anahtarını taşır (`anahtar`), yalnız güncel anahtarla eşleşen yanıt çizilir, yoksa iskelet; sayfa ömürlü önbellek + eşzamanlı istek birleştirme + diğer ölçülerin arka planda önden yüklenmesi; SSE değişiminde önbellek temizlenir. Kural: süzgeçli listede yanıt, isteğin anahtarıyla etiketlenmeden ekrana basılmaz.

## H436 — Hata defteri tekrar ekranı yan rayın altında (2026-10-29)
- **Belirti:** Öğren › Tekrar ekranında geri düğmesi ve başlık ("Hata defteri · …", "Tekrar") soldan kesik; seçili sekme koyu temada görünmüyor.
- **Kök neden:** `LearnReview` `.ls-root` sabit katmanı `.sh-main` içinde çiziliyordu; `.sh-main`'in zoom/yığınlama bağlamı sabit katmanı v15 yan rayının (z 40, uygulama düzeyi) altına itti. Seçili segment `--color-white` zemini koyu temada alan rengiyle aynıydı.
- **Çözüm/önleme:** tam ekran katman `createPortal(..., document.body)` ile gövdeye taşındı; v15'te seçili segment vurgu karışımlı. Yeni tam ekran katman `.sh-main` içine değil gövdeye portal edilir.

## H439 — Üst çubuk arka plan göstergesi stilsiz çiziliyordu (v15, 2026-10-29)
- **Belirti:** /dersler üst çubuğunda çevrimdışı hapının yanında dönen simge ile "1" alt alta taşıyor, "ARKA PLANDA 1 İŞ" ve "1 paket sıradaTümünü gör" çerçevesiz, bitişik yığılıyordu.
- **Kök neden:** `ArkaPlanGosterge` her sayfada `ShellV15` içinde çizilir, ama `ap15g-*` kuralları yalnız tembel yüklenen sayfa bileşenlerinin (ArkaPlanV15, Yardım, Dil…) içe aktardığı `kisisel.css`'teydi. O sayfalardan biri açılmadan gelinen her rotada CSS hiç yüklenmiyor, açılır kart ve rozet tarayıcı varsayılanıyla çiziliyordu.
- **Çözüm/önleme:** `ap15g` kuralları (+ kendi `@keyframes ap15g-don`, kart çerçevesi/zemini, `v15-label`) kabukla birlikte yüklenen `styles/v15/shell.css`'e taşındı. Kural: kabukta (ShellV15) her sayfada çizilen bileşenin stili sayfa CSS'ine değil `shell.css`/`tokens.css`'e yazılır; bir bileşenin sınıfları yalnız onu içe aktaran (ya da kabuğun) CSS dosyasında yaşar.

## H442 — Yeni sayfanın CSS öneki başka bileşenle çakıştı; sekmeler dev daire, düzen tek sütun (soru dışa aktarıcı, 2026-10-30)
- **Belirti:** `/sorular/disa-aktar` masaüstünde sekme düğmeleri 95 px'lik daireler hâlinde, simgeler kocaman; iki sütunlu düzen (ayarlar | önizleme) tek sütuna düşmüş, önizleme hiç görünmüyordu.
- **Kök neden:** sayfa öneki `sa15` seçildi, oysa `styles/v15/ek15.css` aynı adı "Sınav ağırlığı" bileşeni için kullanıyor (`.sa15 { display: flex }`, `.sa15 svg { width: 100%; max-width: 520px }`). Genel kural sayfanın kapsayıcısını flex yaptı, her simgeyi tam genişliğe çekti.
- **Çözüm:** önek `sx15` yapıldı (CSS + bileşen).
- **Önleme:** yeni v15 sayfası/bileşeni için önek seçmeden önce `grep -rn "\.<önek>[ {.:-]" src/styles src/components` ile boş olduğu doğrulanır; kısa (3–4 harf) önekler çakışmaya en açık olanlardır.

## H443 — Önizleme iframe'i genel `max-width: 100%` kuralıyla daraldı, sayfanın sağı kesildi (soru dışa aktarıcı, 2026-10-30)
- **Belirti:** "Sığdır" önizlemesinde A4 sayfasının sağ yarısı kesik, metinler sayfa kenarında yarım kalıyordu.
- **Kök neden:** önizleme, doğal genişlikte (822 px) bir iframe'i `transform: scale()` ile küçültür; sitenin genel `iframe { max-width: 100% }` kuralı iframe'i ölçekten önce sarmalayıcının küçültülmüş genişliğine (652 px) kıstı, belge iframe içinde 652 px'e sığmaya çalışıp taştı.
- **Çözüm/önleme:** ölçekle küçültülen iframe/canvas'a satır içi `max-width: none` verilir; ölçekli öğenin doğal genişliği `getBoundingClientRect` ile doğrulanır (stil genişliği ≠ gerçek genişlik).

## H444 — DOCX ızgara sayfaları LibreOffice/Word'de ikiye bölündü; 26 sayfa 52 oldu (soru dışa aktarıcı, 2026-10-30)
- **Belirti:** 4'lü kart düzeninde indirilen Word belgesinde her sayfanın ikinci satırı yeni sayfaya geçiyor, çözüm hücrelerinin son satırı kesiliyordu.
- **Kök neden:** (1) her bölüme boş bir üst bilgi bağlanmıştı; LibreOffice bunu gövdeden yer alan alan olarak içe aktarıyor. (2) Sabit yükseklikli (`hRule=exact`) satırlarda LibreOffice hücrenin üst/alt iç boşluğunu (`tcMar`) satır yüksekliğine ekliyor (Word içine sayar). (3) Word'ün "auto" satır aralığı yazı tipinin tek satır yüksekliğiyle (≈1,15–1,22 em) çarpılır, CSS `line-height` ise puntoyla: aynı ayar Word'de ~%20 daha uzun metin verir.
- **Çözüm:** boş üst bilgi kaldırıldı (yalnız "her sayfada başlık" açıkken başlık üst bilgisi); hücrelere yalnız sağ/sol iç boşluk, üst boşluk hücre içi sabit paragrafla; satır aralığı yazı tipine göre bölünür (`TEK_SATIR`); sabit sayfa kipinde yazı ölçeği ×0,93, satır yüksekliği ×0,97 güvenlik payı. 26 model sayfası → 26 DOCX sayfası.
- **Önleme:** DOCX/PPTX üreten her değişiklik LibreOffice ile PDF'e çevrilip sayfa sayısı önizlemeyle kıyaslanır (`soffice --headless --convert-to pdf` + `pdfinfo`) ve her XML parçası ayrıştırılarak denetlenir; sabit yükseklikli tablo satırına üst/alt `tcMar` verilmez.

## H445 — Veride boolean `false` metin olarak "false" yazdı (soru dışa aktarıcı, 2026-10-30)
- **Belirti:** hoca üslubu soruların çözümünde "Cevap: B" altında "false" satırı.
- **Kök neden:** `hoca_uslubu_sorular` kayıtlarında `cikarim` alanı bazen `false`; `String(v ?? '')` bunu "false" metnine çevirdi.
- **Çözüm/önleme:** soru verisini metne çeviren yardımcı yalnız string/sayı kabul eder (`kaynak.ts::s`); başka kaynaklardan alan okurken `String(x ?? '')` yerine tür denetimli dönüşüm kullanılır.

## H449 — Ders/ses sürümleri (V1/V2/V3) sitede görünmüyordu; Nörolojik Muayene V2'ye branş listesinden ulaşılamıyordu (2026-10-30)
- **Belirti:** kullanıcı eski/yeni seslere v1/v2/v3 adı verilmesini istedi; adlar API'ye ve oynatıcıya eklendi ama "sitede canlıda göremedim".
- **Kök neden:** (1) v15 kabuğunda branş listesi (`BransV15`) ve ders sayfası (`DersDetayV15`) hiç sürüm çizmiyordu; ses seçici yalnız oynatıcının
  "Oynatıcı" panelinde (⋯ menüsü) vardı. `SesliListeV15`'teki V1/V2 bağlantıları öğrencinin girdiği branş sayfasında yoktu → `k2-05-…-v2`
  dersi (öğrenci önem geliştirmeleri orada) listeden açılamıyordu. (2) Dağıtımdan sonra açık sekme service worker önbelleğindeki eski paketi
  çalıştırır; yeni ekran ancak "Site güncellendi" ile yenilenince gelir.
- **Çözüm:** `SurumSecV15` + `dersSurumleri` (ders sürümü …-v2 ve `kayit.json surumAd` tek sırada V1…Vn, en yenisi "güncel"); branş listesi,
  sesli ders listesi ve ders sayfasında seçici; seçim ders başına cihazda hatırlanır (`cdDersSesSurumu`), `cdOynat` o sesi çalar.
- **Önleme:** yeni bir ders/ses sürümü yayımlandığında canlıda öğrencinin GİRDİĞİ sayfalarda (branş listesi + ders sayfası) görünürlüğü
  tarayıcıyla denetlenir; yalnız API alanını görmek yetmez. Denetim öncesi sayfa yeni pakete yenilenir (yüklü `chunk-main` = sunucudaki).

## H456 — Izgara düzeninde her alt grup değişiminde sayfa kırılıyor, sayfada tek soru kalıyordu; seyrek son sayfa (soru dışa aktarıcı, 2026-10-31)
- **Belirti:** Gruplama açıkken 4'lü/8'li ızgarada bazı sayfalarda tek soru (konu değişince yeni sayfa); akışta belgenin son sayfası çoğu kez 1–2 soruyla yarım kalıyordu.
- **Kök neden:** (1) ızgara sayfası tam grup yoluna (`h.grup`, en iç katman dahil) göre kesiliyordu; çok katmanlı gruplamada her konu değişimi yeni sayfa demekti. (2) Yazı ölçeği sabitti; sayfalama yalnız sığmayan tek bloğu küçültüyordu, belgenin bütünü için bir ölçek seçilmiyordu.
- **Çözüm:** ızgarada yalnız en üst katman sayfa bandı + sayfa kırılımıdır, alt katmanlar hücre içinde küçük başlık (`Blok.basliklar`, HTML/DOCX/PPTX). "Sayfaya sığdır" (`Ayar.sigdir`: kucult/doldur, `sigdirHedef`): `belge.ts::sigdirarak` seyrek (gövdesinin %45'inden azı dolu) bölüm sonu sayfalarını sayar, hedef sayfa sayısına sığan en büyük genel ölçeği ikili aramayla bulur (0,6–1,35); ızgarada "doldur" sayfadaki hücrelere sığan ortak en büyük ölçeği uygular.
- **Önleme:** Sayfa kırılım ölçütü hiçbir zaman en iç gruplama katmanı olmaz; gruplama katmanı ekleyen değişiklik ızgara ve akışta sayfa sayısını 40 soruluk örnekle ölçer (önizleme `.pg` sayısı ile sunucu PDF `pdfinfo` eşit olmalı; bu turda 22 = 22). DOCX/PPTX H444 kapısı (LibreOffice sayfa sayısı + XML ayrıştırma) her sürümde yeniden koşulur.


## H458
- **Belirti:** sunucunun reddettiği (4xx) ya da 8 denemede gidemeyen yorum/beğeni/bildirim, kısa bir "kuyruktan çıkarıldı"
  bildirimiyle kayboluyordu; öğrenci nedenini bilmiyor, yeniden deneyemiyordu. Profil eşitleme hatası yalnız konsola yazılıyordu.
- **Kök neden:** `offlineDatabaseService.drain()` düşen işlemi hiçbir yerde saklamadan siliyordu; `backupUserDataToDatabase` hata
  metnini arayüze iletmiyordu; depolama doluluğu, IndexedDB, service worker ve cihaz saati sapması hiç denetlenmiyordu.
- **Çözüm:** `src/services/hataDenetci.ts` (Sorun denetçisi): düşen işlem `medsoru:islem-dustu`, eşitleme hatası
  `medsoru:esitleme-hatasi` olayıyla denetçiye gider; denetçi 90 sn'de bir / bağlantı dönünce / sekme öne gelince ağ, takılı kuyruk,
  gönderilmemiş ilerleme, depolama, IDB, SW ve saat sapmasını yoklar, güvenli onarımları (kuyruğu yeniden gönder, eşitlemeyi yeniden
  çalıştır, kalıcı depolama iste, SW'yi yeniden kur) kendisi yapar. Panel `HataDenetciSheet` (bağlantı şeridi "Sorun bulundu",
  v15 menü "Sorunlar", eşitleme kartı düğmesi), HTTP koduna göre sade açıklama + "Yeniden dene" + kopyalanabilir teknik ayrıntı.
- **Önleme:** kullanıcının işlemi hiçbir yerde sessizce silinmez; kuyruktan düşen her şey denetçiye bildirilir. Yeni eşitleme/çevrimdışı
  hatası eklenirken hataDenetci'ye `bildir()` ile sade dilde başlık + açıklama + çözüm yazılır, ham hata yalnız `teknik` alanına.

## H475 — Yeni sürüm penceresi kartsız (düz madde) göründü (2026-11-02)
- **Belirti:** kullanıcı: "yeni sürümlerin tasarımı farklı gösterilmeliydi, gösterilmiyor" (Site güncellendi / Yenilikler penceresi).
- **Kök neden:** `UpdatePrompt.tsx` yenilikleri yalnız `guncelleme_notu.json › yenilikler` doluysa özellik kartlarıyla (yer, amaç,
  işlevler) gösterir; onem 619/624/625 notları `yenilikler: []` ve yalnız `maddeler` ile yazıldı → pencere düz listeye düştü.
- **Çözüm:** onem 626 notuna 4 yeni ders + "Hocanın vurguladıkları" kartları (`nerede.yol` ders sayfası) ve `eklenen/duzeltilen` yazıldı.
- **Önleme:** öğrencinin gördüğü yeni özellik/ders içeren her dağıtımda `yenilikler` en az bir kart taşır ({ad, nerede:{ad,yol},
  amac, islevler}); yalnız küçük düzeltmede `maddeler` yeterlidir.

## H491
- **Belirti (2026-11-04):** "Hedef tamamlandı" başarım penceresi yatay telefonda / yarım ekranda (yükseklik ≤420) madalyası ekranın üstünden kesik açılıyordu.
- **Kök neden:** `.bs-k-madalya` kartın üstüne `margin-top:-76px` ile taşıyor; kap (`.bs-k`) kartı dikeyde ortalıyor, üst boşluk 16 px ve kaydırma yok.
- **Çözüm:** `.bs-k` üst boşluğu madalya payı kadar (84 px + güvenli alan), `overflow-y:auto`, kart `margin-block:auto`; `max-height:480px`'te küçük madalya; perde `fixed`.
- **Önleme:** negatif kenar boşluğuyla kartın dışına taşan süs, kapta o kadar iç boşluk ister; ortalanan katman her zaman kaydırılabilir olur. Yeni katman 390×420 ve 844×390'da taranır.

## H492
- **Belirti (2026-11-04):** asistan düğmesi çekmece/diyalog/aramanın üstünde; tostlar KMB/Son Prova tam ekranının altında; kronometre çekmece perdesinin üstünde; klavye açıkken alt sekme çubuğu yazı alanını kapatıyor; mobilde mini oynatıcı sekme çubuğuyla çakışıyor.
- **Kök neden:** z-index değerleri dosya dosya rastgele seçilmiş (900, 100000, 2147483000); `shell.css` yorumundaki "klavyede sekme çubuğu gizlenir" kuralı hiç yazılmamış; `rebuild.css` tanımsız `--sh-tab-h` değişkenine bağlıydı (doğrusu `--sh-tabs-h`).
- **Çözüm:** `styles/katman-duzeni.css` (kb-open gizleme, scroll-locked'ta asistan gizli, hover:none'da görünür denetimler); asistan 55, kronometre 64, tost 2147483050/51; çekmece `--vvh/--vvt`'ye uyar; değişken adı düzeltildi.
- **Önleme:** katman sırası: sabit çubuk 30–40 < yüzen düğme 45–64 < çekmece 70–80 < diyalog 85 < tam ekran 1000–2000 < tost. Yeni yüzen öğe bu aralıktan değer alır ve `html.kb-open` gizleme listesine eklenir.

## H493
- **Belirti (2026-11-04):** Soru çöz özet kartlarında yatay telefonda ve yarım ekranda açıklama "He…", "Yanlı…", "Kurul …" diye okunmaz kesiliyordu.
- **Kök neden:** 600 px+ kompakt düzende etiket gizlenip tek açıklama satırı `nowrap + ellipsis` yapıldı; 600–959 px'te sütun ~60 px kalıyordu.
- **Çözüm:** bu aralıkta süs ikonu gizlenir, açıklama iki satıra sarar (`line-clamp:2`).
- **Önleme:** tek bilgi taşıyan satır asla tek satır üç noktaya düşürülmez; en dar kapsayıcı genişliğinde ekran görüntüsüyle denetlenir.

## H494
- **Belirti (2026-11-04):** bir pencere kapandıktan sonra sayfa kaydırılamaz kalabiliyor ya da diyalog açıkken arka sayfa kayıyordu (ör. spot süre diyaloğu, arama + diyalog, KMB filmi + pencere).
- **Kök neden:** 16 bileşen sayaçlı `utils/scrollLock`'u atlayıp `body.style.overflow`'u kendisi yazıyordu. Üst üste açılan iki katman birbirinin "eski değerini" saklıyordu (`hidden` geri yazılıyordu); KMB filmleri kapanırken `overflow`'u koşulsuz boşaltıp açık diyaloğun kilidini kaldırıyordu. `SpotsSureDiyalog` efekti `[onKapat]`'a bağlı olduğundan her yeniden çalışmada `hidden`'ı "eski" olarak saklıyordu.
- **Çözüm:** hepsi `lockScroll()/unlockScroll()`'a geçirildi (LessonPlayer'daki `documentElement` yazımı dahil).
- **Önleme:** `body/documentElement.style.overflow`'a doğrudan yazmak yasak; yalnız `utils/scrollLock`. Denetim: `grep -rn "body.style.overflow\s*=" src` boş dönmeli.

## H495
- **Belirti (2026-11-04):** 640–767 px'te (büyük telefon yatay, yarım ekran) alt sekme çubuğu görünürken çekmece ortada pencere olarak açılıyordu; klavye açıkken patoloji asistanı tam ekranı, kurulum çekmecesi, tam ekran menü perdesi ve açılır menüler klavyenin altında kalıyordu; sohbet kabuğu yakınlaştırmada yanlış yükseklik alıyordu; güncelleme penceresinde Esc yalnız odak içerideyken çalışıyordu.
- **Kök neden:** çekmece kesme noktası (640) kabuğun kesme noktasından (768) ayrıydı (`Sheet.tsx` JS 639 da); `.pa.is-tam` `100dvh` kuralı klavye kuralından özgüldü; diğer katmanlar `--vvh`'yi hiç kullanmıyordu; `.ms-chat-shell` 768+ kuralında `/ var(--in-zoom)` unutulmuştu; Esc dinleyicisi perdenin `onKeyDown`'ındaydı.
- **Çözüm:** çekmece/pencere eşiği 768 (CSS + `Sheet.tsx isSheet`); `katman-duzeni.css` kb-open kuralları; zoom bölmesi eklendi; Esc belge düzeyinde.
- **Önleme:** kabuğa bağlı her bileşen kabuğun 768 eşiğini kullanır; sabit konumlu tam yükseklik katmanı `--vvh/--vvt` kalıbıyla yazılır; Esc dinleyicisi `document` üzerinde olur.

## H496
- **Belirti (2026-11-04):** sözlükte "Hastalıklar'a git" bağlantısı telefonda 17 px yükseklikte, dokunması zor.
- **Kök neden:** satır içi bağlantı, dokunma alanı yazı yüksekliği kadar.
- **Çözüm:** `pointer: coarse`'ta dikey dolgu + eksi kenar boşluğu (görünüm aynı, alan 43 px).
- **Önleme:** dokunmatik hedef ≥44 px (tasarım sistemi kuralı); `sayfa_tarama.mjs` `small` listesi her turda süzülür.

## H491 — Ara soru kodu başka dersin numarasını aldı (2a17 = k2-07; 2026-11-05)
- **Belirti:** yeni k2-07 dersinin ara soruları 2a17 koduyla yayınlandı; gelecekteki k2-17 dersi aynı kodu isteyecekti.
- **Kök neden:** `hoca_ara_soru/kur.py kimlik()` kodu yalnız ders numarasından türetiyordu; aynı numaralı eski SINAMA dersi 2a07'yi tuttuğu için ajan elle "sıradaki boş" kodu seçti.
- **Çözüm:** `kimlik()` önce dizinde bu anahtara kayıtlı kodu kullanır; numara başka anahtarla doluysa HARF EKİ verir (2a07b, 2a07c…). 2a17 → 2a07b taşındı (veri, ses, kaynak, Oracle).
- **Kural:** ara soru kodunu elle seçme; `kur.py iskele` atar.

### H492 — Hoca vurgu alıntısı bozuk CPU dökümünden kuruldu (2026-11-05)
- **Belirti:** k2-07/k2-15 vurgularında hocanın söylemediği ayrıntılar ("yüzde 2-3", "kaçıngan", "renarkotizasyon") hoca alıntısı gibi duruyordu.
- **Kök neden:** ilk döküm göreli yol hatasıyla GPU'da koşmadı; düşük kaliteli dökümün boşlukları yazar tarafından slayt bilgisiyle dolduruldu.
- **Çözüm/önleme:** döküm `hoca_dokum_gpu.sh` (realpath) ile yeniden yapıldı, 54 alıntı ±60 sn pencerede dökümle karşılaştırıldı, 4'ü düzeltildi. Kural: `alinti` yalnız dökümde geçen sözdür; slayt bilgisi `konu`'ya yazılır, alıntıya karıştırılmaz.

### H493 — Saat kilidi kalktı, hoca dökümü sessizce CPU'da yapıldı (2026-11-05)
- **Belirti:** k2-17/k2-18 hoca dökümü CPU'da; ~35 "İzlediğiniz için teşekkür ederim" türü uydurma cümle, resim anlatılan aralıklar boş.
- **Kök neden:** `nvidia-clock-lock` (300–1500) etkin görünürken `nvidia-clocks` servisi tavanı 3000'e açmış; `hoca_dokum.py` saati >2500 ölçünce kural gereği CPU'ya döndü, hazırlık bunu "OK" saydı.
- **Çözüm/önleme:** `hoca_dokum_gpu.sh` başlamadan kilit servisini yeniden uygular. Döküm başlığında `cihaz: cpu` ise A1b'ye geçilmez; döküm GPU'da yeniden alınır (vurgu/alıntı CPU dökümünden kurulmaz).

### H494 — Boş çapa satırı ("‖") çapasız cümleyi çapalı gösterdi (2026-11-05)
- **Belirti:** k2-06 (6), k2-09 (6), k2-16 (11) cümlede PDF işareti boş satıra gidiyordu.
- **Kök neden:** v2 üreteci (`_uret.py`, dersten derse kopyalandı) çapasız cümleye `satir: ["‖"]` yazdı; `konusma_v2.dogrula` katlanmış boş dize her metinde "geçtiği" için yakalamadı.
- **Çözüm/önleme:** `konusma_v2.dogrula` 3 harften kısa çapa satırını HATA sayar; yayındaki 23 kayıt `slayt: null` yapıldı. Çapasız cümle her zaman `slayt: null` yazılır.

### H495 — Ok glifi (↓ ⟸ ←) ve "Gpi/ SNr" boşluğu kanıt eşleşmesini bozdu (2026-11-05)
- **Belirti:** k2-18 şema slaytlarında (s8) doğru alıntılar "kanıt s8'de yok" HATA'sı verdi.
- **Kök neden:** `degerlendirme_dogrula.norm` yalnız → okunu siliyordu; pymupdf metni ↓/⟸/← ve "/ " boşluğu taşıyor.
- **Çözüm/önleme:** doğrulayıcı ve `kanit_onar.py` aynı norm: tüm ok blokları (U+2190–21FF, U+27F0–27FF, U+2794–27BF) ve noktalama çevresi boşluk yok sayılır. Kanıt düzeltilince `cikmis_konum_yaz.py` yeniden çalıştırılır (konum dosyası eski kanıtı tutar).

### H496 — Kısa şık açıklaması betikle kalıp ekle uzatıldı (2026-11-05)
- **Belirti:** k2-17 örnek sorularda 93, çözücüde 36 şıkta "; soruda aranan yanıt ise X (s. N)" eki; seste her yanlış şıkta aynı cümle.
- **Kök neden:** yazar 20 kelime alt sınırını geçmek için açıklamaları betikle doldurdu (k2-16'dan kopyalanan yol); `sik_aciklama.py` bu kalıbı tanımıyordu.
- **Çözüm/önleme:** kalıp `BOS_KALIP`'a eklendi (HATA); sayısal alt sınır ancak şıkka özgü bilgiyle aşılır, betikle ek yazılmaz. k2-16 dahil yayındakiler taranır.
- **H496 ek (2026-11-05, temizlik):** yayınlanmış 59 dosyada 111 eşleşme tarandı; 109'u yeniden yazıldı (2 meşru tıbbi ifade gerekçeyle bırakıldı). Kök neden 2: src/data'daki düzeltme sesi yenilemez — ses `meds_temp/.../cikti_tam` ve `asistan/cikti` içindeki `ses` alanından üretilir; metni değişen her açıklamada `ses` alanı da güncellenmeli, sonra ses.py/asistan_ses.py. Not: `patoloji_onem/asistan_ses.py` CUDA'yı kendisi kapatır (GPU sarmalayıcıda bile CPU'da çalışır).

### H502 — iPad pencere kipinde sistem düğmeleri geri tuşunu kapatıyordu; kullanıcı geri çıkamıyordu (2026-11-06)
- **Belirti:** iPad'de bölünmüş ekran / Stage Manager penceresinde sol üstteki kapat-küçült-tam ekran düğmeleri uygulamanın geri tuşunun üstüne biniyor, dokunuşu sistem yutuyordu.
- **Kök neden:** tek çıkış yolu sol üst köşedeki geri tuşuydu; iPadOS bu bölgeyi sayfaya bildirmez (Safari'de `env(safe-area-inset-*)` / `titlebar-area-*` yok), sayfa katmanı göremez.
- **Çözüm/önleme:** `components/shell/ipadPencere.tsx`: pencere kipi algısı (`:root[data-pencere='dar']` → üst çubuk 84 px sağa), başlık = geri düğmesi, alt yüzen geri hapı, sol kenar kaydırması + Esc/⌘[/Alt+←, yedek yollar 2 kez kullanılırsa hap cihazda kalıcı. Kural: hiçbir ekranda tek çıkış yolu sol üst köşe olamaz; görünürlük denetiminde `offsetParent` değil `getClientRects()` kullanılır (yapışkan/sabit atada null döner).

### H504 — Ayarlarda "Küçük sürprizler" satırı görünmüyordu (2026-11-06)
- **Belirti:** sürpriz katmanını kapatma düğmesi ayarlarda yoktu.
- **Kök neden:** v12 ayarlar (`ProfileV12` › Veri) `<ArzuRow />`'u kullanıcı geçirmeden çağırıyordu; satır `auth.currentUser`'a düşüyor, yerel kimlik sisteminde (H466) bu nesne hesabı tanıtmadığından satır gizleniyordu.
- **Çözüm/önleme:** `DataPanel`'e `currentUser` geçirildi. Kural: hesap koşullu satırlar kullanıcıyı prop olarak alır, `auth.currentUser` yedeğine güvenilmez.

### H507 — iPad'de sesli dersten geri çıkılamıyordu; "başlığa bas = geri" çalışmıyordu (2026-11-06)
- **Belirti:** iPad'de geri tuşu görünmüyor (sistem düğmeleri kapatıyor); sesli ders başlığına basınca da geri gidilmiyordu.
- **Kök neden:** (1) başlık-geri yalnız kabuk üst barındaki `.v15-top-h.is-geri`'ye bağlıydı; sesli ders odak ekranı kabuk barını çizmez, kendi `.cd15-baslik`'ını çizer → işleyici yoktu. (2) Alt "‹ Geri" hapı yalnız pencere kipi algılanınca (`data-pencere="dar"`) ya da 2 yedek kullanımdan sonra çıkıyordu; tam ekran Safari'de algı tutmadığı için hiç görünmüyordu.
- **Çözüm:** `shell/ipadPencere.tsx` — iPad'de `.cd15-baslik` tıklaması `geriTetikle()`; hap iPad'de her zaman (geri varken) gösterilir.
- **Kural:** Geri yolu eklerken odak ekranlarını (kabuk dışı başlıklar) ayrıca kapsa; "algılanırsa göster" türü güvenlik yollarını algının başarısız olduğu durumda da sına.

### H514 — Örnek sorular ders listesinde "Hoca üslubu · N yeni soru" rozeti öğretim üyesi adının üstüne biniyordu (tablet/masaüstü, 2026-11-09)
- **Belirti:** 768–1024 px tablette (ve masaüstünde) `/sorular/ornek` ders satırlarında rozet ile "Prof. Dr. …" yazısı aynı yere çizilip okunmaz oluyordu; telefonda alt alta göründüğü için fark edilmemişti.
- **Kök neden:** `KazanimSorulariView.tsx` iki ayrı `.ks-lesson-who` span yazıyordu; `secondary.css` ≥720 px ızgarasında ikisi de `grid-area: who` alanına düşüyor (ızgara aynı alana iki öge koyunca üst üste bindirir). ≤719 px düzeninde alanlar satır satır aktığı için sorun yalnız geniş ekranda çıkıyordu.
- **Çözüm/önleme:** tek `.ks-lesson-who` içinde yazar + ` · ` + rozet (`<b>`); alan `white-space: normal` ile sığmazsa sarar. Kural: adlandırılmış ızgara alanına (`grid-area`) birden çok kardeş öge yazılmaz; koşullu ek satır aynı kabın içine girer. Düzen değişikliği telefon + tablet (768/820) + masaüstü üçünde birden denetlenir (`scripts/altyapi/perf/sayfa_tarama.mjs` taşma raporu üst üste binmeyi GÖREMEZ, ekran görüntüsüne bakılır).

### H517 — Üst bar başlığı bölünmüş ekranda ve yan ray açıkken kırpılıyordu ("Sesli dersler" → "Sesli …", "Tam ekran ve kısayollar" → "Tam ek…") (2026-11-09)
- **Belirti:** 600–839 px (iPad bölünmüş ekran, dar pencere) ve yan menüsü açık 1024–1280 px'te sayfa başlığı üç nokta ile kesiliyor, alt başlık okunmuyordu.
- **Kök neden:** `shell.css` üst bar ölçülerini **pencere** genişliğine (`@media`) bağlıyor; başlığa kalan yer ise ray/yan menü düştükten sonraki alandır. ≥1024'te arama kutusu sabit 260 px ve araç grubu `flex: none` olduğu için daralan tek öge başlıktı; 600–839'da tam "Kurul N ›" çipi + yükle düğmesi + 5 simge başlığa ~100 px bırakıyordu.
- **Çözüm/önleme:** ≥1024'te araç grubu başlıktan 1000 kat istekli küçülür ve içinde yalnız arama kutusu daralabilir (`flex: 0 1 260px; min-width: 44px`); 600–839'da kompakt "K2" çipi, yükle düğmesi hesap menüsünde, başlık telefondaki gibi iki satıra sarar. Kural: üst bara yeni araç eklerken başlık 600, 768 ve yan menülü 1024'te ölçülür; sabit genişlikli araç `flex: none` bırakılmaz.

### H518 — Ayarlar: gruplar karışık, alt sayfalar iki ayrı anahtar görünümü kullanıyor, geniş ekranda tek dar sütun (2026-11-09)
- **Belirti:** "Ben / Ayarlar / Diğer" grupları ilgisiz satırları yan yana koyuyordu (Hesap ile Görünüm aynı grupta, turlar hem listede hem Hesap sayfasında); Erişilebilirlik ve Görünüm'deki anahtar (38×22, koyu düğme) ile Tam ekran'daki (44×26, beyaz düğme) farklıydı; Erişilebilirlik › Hareket segmenti panel kenarına yapışıktı; telefonda "Profil ve ayarlar" başlığı iki satıra sarıyor, "Erişilebilirlik" kırpılıyordu; masaüstünde 1440 px'in 720'si kullanılıyordu; başlıklar "Veritabanı Eşitleme & Yedekleme" gibi İngilizce büyük harf düzenindeydi.
- **Kök neden:** v15 dalı v12 panellerini olduğu gibi sarıyordu (`.pf15-panel.u12-pf`); v12 anahtarı ve satır boşlukları v15 kart diline uyarlanmamış, liste tek düz dizi olarak büyümüştü. Geniş düzen hiç yoktu (`.pf15 { max-width: 720px }`).
- **Çözüm/önleme:** `ProfileV12.tsx` v15 dalı veri tablosundan kurulur (Profilim · İçeriklerim · Görünüm ve okuma · Uygulama · Hesap ve veri · Yardım · Oturum), "Ayarlarda ara" + tek dokunuşla tema; kabın **üst öğesi** ≥ 860 px ise (ResizeObserver; `.pf15` kendisi 720 ile sınırlı olduğundan kendi genişliği ölçülmez) liste solda yapışkan, bölüm sağda. Anahtar ve dokunma alanı `profil.css`'te tek tip. Yükseklik sınırlı esnek sütunda çocuklar `flex: none` olmalı (yoksa `overflow: hidden` liste tek satıra çöker — ilk denemede görüldü). Kural: Ayarlar'a yeni satır `gruplar` tablosuna, doğru gruba ve `ek` arama sözcükleriyle eklenir; aynı satır ikinci bir sayfada yinelenmez.

### H519 — Sesli ders › Oynatıcı çekmecesinde "Hız" başlığı ve hız hapları içeriden/ortadan başlıyordu (2026-11-09)
- **Belirti:** Çekmecede "Ses", "Tekrar", "Bölüm sonunda dur" satırları sola dayalıyken "Hız" başlığı ~28 px içeride, yatay telefonda hız hapları ortada ve dar duruyordu.
- **Kök neden:** `sesli.css` sonundaki `.cd15-sat.cd15-sat-blok { align-items: stretch }` kök öneksiz (özgüllük 0,2,0); dosyanın başındaki iç içe `:root[data-v15='on'] { & .cd15-sat { align-items: center } }` (0,2,1) kazanıyordu. Yön (`column`) çakışmadığı için uygulanıyor, hizalama uygulanmıyor, hata yarım göründüğünden fark edilmemişti.
- **Çözüm/önleme:** üç kurala `:root[data-v15='on']` öneki. Kural: v15 iç içe bloktaki bir sınıfı sonradan ezen kural aynı kök önekini taşır; öneksiz "ek" kural yazılmaz.

### H520 — Sesli ders listesinde süzgeç hapları sıralama düğmesinin altına giriyordu (telefonda "Arşiv" üstüne simge, tablette "Bitti" yarım) (2026-11-09)
- **Belirti:** `/dersler/canliders` üst satırında "Bu yıl · Arşiv" seçicisinin "Arşiv" yazısının üstüne sıralama (⇅) simgesi biniyor; tablette son hap yarım kesiliyordu.
- **Kök neden:** `.v15-hscroll` kenardan kenara kaysın diye `margin-inline: calc(var(--v15-pad) * -1)` ile iki yana taşar; bu satır tam genişlikte tek başına durduğunda doğrudur. Sesli liste, Öğren kitaplığı, Özetler gibi ekranlarda aynı satırın **sağında** sıralama/arama düğmesi var; sağ eksi boşluk hapları 16 px düğmenin altına sokuyordu.
- **Çözüm/önleme:** `dersler.css`: `.o15-ust > .o15-cipler.v15-hscroll:not(:last-child) { margin-right: 0 }` (aynı kalıbı kullanan bütün ekranları kapsar). Kural: `.v15-hscroll` yanında kardeş öge varsa o yandaki taşma kapatılır.

### H551 — Giriş yapmış öğrenci kendi profilini ve arkadaşlık isteklerini göremiyordu (2026-11-10)
- **Belirti:** girişli kullanıcıda Arkadaşlar listesi ve gelen/giden istekler boş, açık profil "Profilleri görmek için giriş yapmalısın", gizlilik anahtarı yüklenmiyor.
- **Kök neden:** `adminFetchAuth.ts::ogrenciJetonu` öğrenci jetonunu GET isteklerinde yalnız `/api/(basarim|olasi-sorular|topluluk)/` yollarına ekliyordu. Arkadaşlık okuma uçları (`GET /api/arkadas`, `/api/kisi/ben|ara|siralama|:kimlik`) jetonsuz gidiyor, sunucuda `verifiedUid` boş kalıyor → `{girisli:false, arkadaslar:[]}` ya da 401. Yazma uçları (POST) jeton taşıdığı için istek gönderilebiliyor ama görülemiyordu. Ayrıca açılışta oturum geri yüklenmeden giden öğrenci isteği jetonu beklemiyordu (bekleme yalnız yöneticideydi).
- **Çözüm:** izin listesine `kisi/` ve `arkadas` eklendi; jeton gerektiren öğrenci isteği de `auth.authStateReady()`'yi (≤4 sn) bekler.
- **Önleme:** `verifiedUid` okuyan yeni bir GET ucu eklenince `ogrenciJetonu` listesine de eklenir; uç yazıldığında girişli kullanıcıyla tarayıcıdan GET sınanır (curl'deki jetonsuz yanıt "çalışıyor" sayılmaz).

### H572 — Soru dışa aktarıcı çöküyordu ("sayfayı yenile"); PDF'te logo alt bilgiyle üst üste biniyor, alt bilgi/başlık kesiliyor, ızgarada soru kayboluyordu (2026-11-14, kullanıcı bildirdi)
- **Belirti (üç ayrı kullanıcı şikâyeti, aynı turda):** (1) dışa aktarıcıda "bir şeyler ters gitti / sayfayı yenile" ekranı; (2) PDF'te "sayfanın altında içerik kesik kesik yazılıyor, tam verilmiyor, kayboluyor"; (3) "alt bilgilendirme yeri ile üst üste biniyor".
- **Kök neden 1 (çökme, kanıt canlı günlükten):** Canlı `data/istemci_hatalari.jsonl`'de `/sorular/disa-aktar` için iki gerçek çökme: `undefined is not an object (evaluating 'xt[t.palet].renk')`, yığın `chunk-belge…` → `useMemo` → `chunk-SoruAktarV15…`. `renkHaritasi` (belge.ts) paleti doğrudan `PALETLER[a.palet].renk` ile okuyordu. `a.palet` localStorage'daki eski ayardan/bozuk şablondan tanınmayan bir değerse (`ayarNormal` yalnız `!!PALETLER[...]` kontrolü yapıyordu, `'ozel'` ve boş palet listesini kapsamıyordu) tek bir eksik anahtar **tüm ekranı** düşürüyordu → React #306 → "sayfayı yenile". Ekran görsel olarak açıldığı için hata "bazen" görünüyordu; kullanıcı "sayfayı yenile" istemini tam bu çökme üretiyordu.
- **Kök neden 2 (üst üste binme):** `govde()` gövde yüksekliğini **sabit** `BASLIK_MM = 16` ve `ALT_MM = 7` ile hesaplıyordu; CSS'te `.pg-bas{height:16mm}` sabitti. `logoYuk` 4–24 mm seçilebilir olduğundan 16 mm'den yüksek logo başlık kutusundan taşıyordu (ölçüm: 24 mm logo → 91 px, kutu 60 px, 9 px taşma) ve gövdenin üstüne biniyordu. `.pg-alt` `.pg-in`in son çocuğu olduğundan üst üste binme yerine **gövdeyi alttan taşırıyor**, `overflow:hidden` da içeriği kırpıyordu.
- **Kök neden 3 (kesik/kayıp metin):** (a) `.pg-alt>span` `white-space:nowrap; text-overflow:ellipsis` idi: uzun alt metin **tek satırda kesiliyordu** (ölçüm: üç bölgenin üçü de `scrollWidth > clientWidth`). (b) `.pg-bas h1` de `nowrap` idi; uzun başlık kutu dışına 438 px taşıyordu. (c) Izgarada hücreye en küçük ölçekte de sığmayan soru `tasma` işaretlenip hücreye **konuyor**, `overflow:hidden` ile sessizce kırpılıyordu — PDF'te sorunun son şıkları kayboluyordu (ölçüm: 8'li düzende 371 px kesik).
- **Kalıcı çözüm:** (1) Palet erişimi tek yere alındı: `paletRenkleri` tanınmayan değeri Canlı'ya düşürür, `paletNormal` ile `ayarNormal` paleti doğrular; `renkHaritasi` boş palette bile `a.vurgu`ya düşer. (2) `baslikYukMm(a, var)` ve `altYukMm(a)` gerçek yüksekliği hesaplar (logo 10 mm üstü + alt başlık payı; alt bilgi iki satır); `govde()` ve CSS `min-height` aynı ölçüyü kullanır. DOCX (`baslikTablo`, `sectPr` üst/alt marj) ve PPTX (başlık kutusu, alt bilgi kutusu) aynı fonksiyonlara bağlandı. (3) Alt bilgi iki satıra kadar sarar (line-clamp), başlık iki satıra kadar sarar, kapak `justify-content:center` taşması `overflow:auto` ile güvene alındı, çerçevesiz kapağa 8 mm iç boşluk verildi. (4) **Izgarada sığmayan soru kırpılmıyor**: ızgaradan çıkarılıp belgenin sonunda tam genişlik "Sığmayan sorular" akış koridoruna yerleştirilir (`zorunluAkis`); tamamen boş kalan ızgara sayfası hiç üretilmez; önizleme uyarısı "kırpıldı" yerine "ayrı sayfaya alındı" der.
- **Doğrulama:** `npm run lint` 0 hata, `npx vite build` başarılı. Tarayıcıda beş senaryo (varsayılan, 24 mm logo + uzun alt bilgi, uzun başlık, 40 mm not alanı + şerit, sade kapak) render edilip ölçüldü: `hatalar: []` (alt bilgi kesiği yok, gövde alttan taşmıyor, logo başlıktan taşmıyor). Logo senaryosunda yerleşim: başlık 0–98, gövde 98–977, alt bilgi 977–1009 (çakışma yok). Bozuk palet (`palet: 'yokolan-palet'` ve elle `'BOZUK'`) artık çökmeden Canlı paletine düşüyor. 200 gerçek soruda sayfa sayıları değişmedi (akış 42, 2'li 120, 4'lü 70, 8'li 45), boş sayfa 0.
- **Önleme:** (a) `PALETLER[...]` doğrudan indekslenmez; her yerde `paletRenkleri`/`paletNormal` kullanılır. (b) Sayfa geometrisinde sabit mm **yalnız** kullanıcıdan bağımsız ögeler için; logo, alt başlık, alt metin gibi kullanıcı ayarlarına bağlı yükseklikler `baslikYukMm`/`altYukMm`den gelir ve HTML/DOCX/PPTX aynı fonksiyonu çağırır (üç çıktı ayrışmaz). (c) `overflow:hidden` bir soru/çözüm kutusunda **kırpma** anlamına gelir; ızgarada sığmayan blok taşınmalı (ayrı akış), kırpılmamalı. (d) Yeni bir palet/kapak/başlık seçeneği eklerken "en büyük değer" ile ölçüm yapılır (logo 24 mm, alt bilgi en uzun metin, 40 mm not alanı); yalnız varsayılan değerle bakmak hatayı gizler. (e) Kullanıcı "sayfayı yenile" ekranı bildirdiğinde ilk bakılacak yer canlı `data/istemci_hatalari.jsonl` (Oracle: `docker exec meds-app`), çünkü o ekranı üreten gerçek yığın orada ve `?adres=` alanı hangi sayfa olduğunu söyler.

### H573 — "Sayfayı yenile" ekranı yenilemeyi öneriyor ama kurtarmıyordu: eski kabuk + eksik parça döngüsü (2026-11-14, H572 ile aynı tur)
- **Belirti:** Kullanıcılar tembel parça (chunk) hatasında "Yeni sürüm hazır / Sayfayı yenile" ekranında kalıyordu; canlı günlükte 30+ `Minified React error #306` (React: önbelleğe alınmış tembel bileşen; yığın hep `chunk-vendor-react-*`) ve `Unable to preload CSS for …/asset-*.css` (yeni derlemenin CSS'i cihazda yok).
- **Kök neden:** Service worker gezinme isteğinde ağı 400 ms yarıştırıp önbellekteki `/index.html`e düşer; önbellekteki kabuk **eski** derlemenin parça adlarını ister. Parça önbellekte yoksa (budandı/yer açıldı/yeni cihaz) import düşer. Hata sınırı yalnız `location.reload()` diyordu; SW yine eski kabuğu verince aynı ekran geri geliyordu. `sw.js` PRECACHE listesi yalnız 10 sabit dosya; derleme parçalarını önbelleğe **almıyor** (asıl sorun bu değil, kabuğun bayat olması).
- **Kalıcı çözüm:** `main.tsx`'te tek bir `kabukOnbelleginiTazele()`: (1) bekleyen/indirilen service worker'ı `SKIP_WAITING` ile etkinleştirir ve `update()` dener, (2) çevrimdışı ders/PDF paketleri **korunarak** kabuk ve sürümsüz çalışma zamanı kopyalarını önbellekten siler. Hata sınırı ve `vite:preloadError` yolunda yenilemeden **önce** bu çalışır; iki yol da aynı 8 sn döngü sınırını paylaşır ve `vite:preloadError` artık `event.preventDefault()` ile Vite'ın kendi reload'uyla çakışmaz.
- **Önleme:** Bayat kabuk + eksik parça hatasında çözüm "reload" değil "önce önbelleği tazele, sonra yükle"dir; önbellek temizliği çevrimdışı içerik paketlerine dokunmaz (`canli-ders|pdf-offline|paket|bekleyen|paylasim` korunur). `preloadError` dinleyicisine dokunulursa `preventDefault()` korunur; kaldırılırsa iki reload yarışır ve döngü sınırı işlemez.

### H575 — "PDF'te alt kısımda soru/şık metni kesik kalıyor" bildirimi H572 sonrası da geldi: sıfır boşluklu sayfa geometrisi baskı kaymasına karşı savunmasız (2026-11-15, kullanıcı bildirdi)
- **Belirti:** Kullanıcı H572/H573 düzeltmelerinden sonra da "PDF oluştururken sayfanın alt kısmında soruların veya şıkların metinlerinin kesik kalması veya görüntülenmemesi sorunu devam etmekte" dedi.
- **Kanıt araması (gerçek kullanıcı akışıyla):** Canlı sitede ai-test oturumuyla `/sorular/disa-aktar` açıldı, "PDF indir" düğmesine basıldı, sunucuya giden **tam ihracat HTML'i** fetch yakalayıcıyla alındı ve bağımsız başsız Chrome'da aynı hattan basıldı. Dört kip sınandı: varsayılan akış (2.345 sayfa), 4'lü ızgara (2.953), kitapçık yaprak (1.174), `cozumYeri: sayfaAlti` (672). Her koşuda: (a) DOM ölçümü `.pg-gv`/`.hc`/`.kol`/`.pg-serit` taşması 0, (b) `pdftotext` boşluk temizliğinde önizlemedeki 60 sorunun kök ve şık metinlerinin tamamı PDF'te bulundu, (c) `-bbox` ile sayfa alt 30 pt'sine giren tek sözcük yok. Yani yayındaki üretim bu kiplerde metin kaybetmiyor; kalan risk **sınıfsal**: Chrome'un baskı dizgisi, ölçüm çerçevesinden 1–2 px farklı dizebilir (mm→pt yuvarlama, ipuçlama). `govde()` gövdeyi tam doluya kuruyordu; sıfır boşlukta bu tür birkaç piksellik artış, `.pg-gv`/`.hc`'nin `overflow:hidden` kırpma altına denk gelir ve son satır/şık sessizce kaybolur — ayara, yazı tipine ve yazıcıya göre "bazen" görünür.
- **Kalıcı çözüm:** `ayar.ts`'e `BASKI_PAY_MM = 1.2` eklendi; `govde()` gövde yüksekliğinden bu baskı toleransını düşer. Baskı tarafındaki küçük artışlar payı yer; metin asla kırpılma sınırına değmez. Önizleme aynı fonksiyonu kullandığından üç çıktı (HTML/PDF, DOCX, PPTX) ayrışmaz.
- **Önleme:** (a) "Tam dolu sayfa + `overflow:hidden`" kombinasyonu kırpma demektir; sabit ölçülü her gövde baskı toleransı taşır. (b) Bu sınıf hatayı sınama yöntemi: canlı sayfada gerçek indirme akışı → ihracat HTML'ini yakala → bağımsız Chrome'da bas → `pdftotext` boşluksuz karşılaştırma + `-bbox` ile alt kenara yapışık sözcük taraması; ekranda "önbellek/eski sayfa" tuzağına düşmeden kullanıcı akışının birebir aynısı budur. (c) pdftotext eşleşmesinde boşluklar ve madde imleri biçimden geldiği için karşılaştırma her zaman `\s` temizlenmiş metinle yapılır; sıralı karşılaştırma sırası kolon yerleşimiyle değişebilir, "eksik" sanmadan tam metinde aranır.

### H576 — "PDF'te alt bilgi (sayfa numaralı satır) diğer metnin üstünü kapatıyor": sayfa kutusu kâğıttan kısa basılmıyordu (2026-11-15, kullanıcı bildirdi)
- **Belirti:** Kullanıcı PDF çıktısında alt bilgi satırının (sayfa sayısı dahil) bir katman gibi davranıp diğer metnin üstünü kapladığını bildirdi.
- **Kanıt araması:** Canlı akışta uzun alt metin + sayfa numarası ayarıyla ihracat HTML'i yakalanıp bağımsız Chrome'da basıldı: üç bölge kutusu çakışması 0, `clamp` baskıda tutuyor (2 satır + üç nokta), 2.347 `.pg` = 2.347 PDF sayfası, alt kenara yapışık sözcük 0. Yani HTML kutu modelinde alt bilgi akış içindedir ve üstüne binemez; kalan mekanizma **baskı parçalaması**: `.pg` kutusu `@page` ölçüsüne eşit kuruluyordu. Kutu kâğıda eşit/büyükse Chrome, baskı dizgisindeki yarım piksellik büyümeyi kutuyu parçalayarak telafi eder ve taşan parçayı SONRAKİ basılı sayfanın içeriğinin üstüne basar; sayfa sayısı değişmediği için fark edilmez. Alt bilgi en altta durduğundan en çok o taşar → "üstüne binen katman".
- **Kalıcı çözüm:** `belge.ts` CSS'inde `.pg` ve `.yp` yüksekliği kâğıttan **0,25 mm kısa** basılır. Kutu her koşulda kâğıda sığar; parçalama (ve üstüne basma) yapısal olarak olanaksızlaşır. 0,25 mm boşluk `govde()`'nin 1,2 mm'lik `BASKI_PAY_MM` toleransı içinde olduğundan içerik kırpılmaz.
- **Yineleme (2026-11-15, kullanıcı yeniden bildirdi):** 0,25 mm kısaltma baskı çözünürlüğünde (mm→nokta yuvarlaması) ~1 px'e indiğinden bazı kâğıt/yazıcı bileşimlerinde parçalama/üstüne basma sürüyordu. Kutu kısaltması tek bir sabite alındı (`ayar.ts::BASKI_KUTU_KISA_MM`) ve **1 mm**'ye çıkarıldı (`.pg`/`.yp` yüksekliği `h - BASKI_KUTU_KISA_MM`); içerik yine kırpılmasın diye gövde toleransı `BASKI_PAY_MM` 1,2 → **2 mm** yapıldı (kutu içi boşluk = 2 − 1 = 1 mm ≈ 3,8 px, hem baskı sürüklenmesini hem parçalamayı kapsar). Kutu kısaltması her zaman `BASKI_PAY_MM`'den küçük tutulur.
- **ASIL KÖK NEDEN (2026-11-15, canlıda doğrulandı — YAZI TİPİ UYUŞMAZLIĞI):** PDF düzeni (bir sayfaya kaç soru sığdığı) **istemci tarayıcısında** `Olcer` ile, o makinenin yazı tipiyle ölçülür; PDF ise **Oracle `meds-app` konteynerinin Chromium'uyla** basılır. Konteynerde yalnız **DejaVu Serif** yüklüydü (`fonts-dejavu-core`); `'Times New Roman','Liberation Serif',Times,'DejaVu Serif',serif` yığını orada DejaVu'ya düşüyordu. DejaVu Serif, kullanıcının tarayıcısındaki Times New Roman'dan **belirgin biçimde geniş ve uzun**; aynı metin sunucuda ölçülenden FAZLA dikey yer kaplayıp sabit yükseklikli `.pg-gv`'den (overflow:hidden) taşıyor, son soru(lar) alt kenarda kesiliyor ve alt bilgi şeridi tam o kesiğin hizasında kalıyordu ("beyaz katman üstünü kaplıyor ve kesiliyor"). Yerel sınama temiz çıkıyordu çünkü yerel tarayıcı (Olcer) ile yerel/konteyner Chromium AYNI Linux yazı tiplerini kullanıyor; uyuşmazlık yalnız kullanıcının (Windows/Mac, Times New Roman) tarayıcısı ile Oracle (yalnız DejaVu) arasında oluşuyordu. "PDF indir" (sunucu render) kullananlar bunu görüyordu.
- **KALICI ÇÖZÜM 3 (asıl düzeltme):** Render konteynerine **`fonts-liberation`** (Liberation Serif/Sans/Mono) eklendi (`deploy/oracle/Dockerfile.oracle`). Liberation ailesi Times New Roman/Arial/Courier New ile **metrik uyumludur**; yığın artık DejaVu yerine Liberation Serif'e düşer ve sunucu basımı, kullanıcının tarayıcısının Times New Roman ölçümüyle **aynı yüksekliği** verir → taşma/kesilme yok. Doğrulama: Oracle konteynerinde `fc-match "Times New Roman"` → Liberation Serif; canlı `/api/pdf/render` PDF'i `pdffonts` ile `LiberationSerif` gömüyor (eskiden DejaVu). Canlı konteyner anında yamalandı (`apt-get install fonts-liberation` + `fc-cache`), imaj yeniden derlemesi kalıcı kılar (`Dockerfile.oracle` değişince `deploy-code.sh` imajı yeniden kurar).
- **Ek sağlamlaştırma:** "Yazdır" da ham HTML'i native print'e vermez; önce **sunucuda PDF üretip** (`renderPdfOnServer`) o PDF'i gizli iframe'de bastırır (`printPdfBlob`, `src/components/pdf/pdfDocument.ts`) — native `window.print()` yazdırma kutusunun kenar boşluğuyla `@page margin:0`'ı ezip sabit sayfa kutularını parçalayabildiğinden. Sunucu üretimi başarısızsa eski `printDocument` yedeğe düşer.
- **Önleme:** (a) **İstemcide ölçülüp sunucuda basılan her belgede ölçüm yazı tipi ile basım yazı tipi AYNI aileye düşmelidir.** Render ortamına yazı tipi eklerken/çıkarırken `fc-match` ile yığının gerçekte hangi dosyaya düştüğü denetlenir; metrik uyumlu aile (Liberation↔MS core) şarttır. Yeni bir yazı tipi seçeneği eklenince hem istemcide (web font / sistem) hem Oracle konteynerinde karşılığı bulunmalı. (b) Yerel sınama konteynerle aynı yazı tiplerini kullandığından bu sınıf hatayı GİZLER; PDF düzeni hatalarında önce `docker exec meds-app fc-match "<yığının ilk adı>"` ve çıktı PDF'inde `pdffonts` bakılır. (c) Sabit yükseklikli kutuyla kurulan yazdırılabilir belgede native `window.print()` kullanıcının kenar boşluğuna bağımlıdır; deterministik çıktı için hep sunucu PDF'i bastırılır.
- **Önleme:** Sabit sayfa kutusu (`height: kâğıt ölçüsü`) + `break-after:page` kombinasyonunda kutu asla kâğıda eşit ölçülmez; "eşit" ölçü yuvarlamada "büyük" demektir ve Chrome bunu sonraki sayfaya taşıyarak çözer. Bu sınıfın sınaması: ihracat HTML'i bağımsız Chrome'da basılır, `.pg` sayısı ile PDF sayfa sayısı ve sayfa başına alt bilgi metni karşılaştırılır; sayfa sayıları eşit olsa bile parçalama sayfa sayısını değiştirmeden üstüne basabildiğinden kesin kanıt için kutu yüksekliği kâğıttan kısa tutulmalıdır.

