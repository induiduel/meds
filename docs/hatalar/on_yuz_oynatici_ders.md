# Hata defteri — on_yuz_oynatici_ders (sesli ders oynatıcısı, ders ekranı, ders hattı ön yüz kayıtları)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16; `hatalar/on_yuz.md` 4 konuya bölündü). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## H82 — Çıkmış soru penceresi şık seçilince kayboldu, ders sürmedi (2026-10-27, sınamada yakalandı)
- **Belirti:** Slayt 3'teki chip'e basıp şık seçince pencere kapandı, görünüm slayt 1'e döndü, ses sürmedi.
- **Kök neden:** Pencere durumu slayt katmanındaki chip bileşenindeydi. Ses durunca görünüm canlı konuma döndü, PDF
  görüntüleyici ekran dışı slaytı (chip + pencere) kaldırdı; durum ve "çalıyordu" bilgisi kayboldu.
- **Çözüm / kural:** Durum modül düzeyinde (`useSyncExternalStore`), pencere `CdCikmisPencereKok` ile `document.body`'ye
  portal; sanal listede çizilen bileşen kalıcı durum tutmaz. Sınama: çalarken aç → ses durur, kapat → aynı saniyeden sürer.

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

## H111g · İzleme hızı kaydırıcısı: dokunma hedefleri 10–19 px, boş durumda imleç metinle çelişiyordu (2026-10-28, Sınav planı/Bitirdiklerim)
- **Belirti:** Telefonda hız durakları (1×…2,5×) 19 px, kaydırıcı rayı 10 px yüksekti; seçim yokken metin "kalan süre 1× gösteriliyor" derken imleç 1,5×'te duruyordu.
- **Kök neden:** `IzlemeHizi.tsx` boş değer için `?? 1.5` kullanıyordu; `takip.css` rayın ve durakların görünür boyutu dokunma alanı olarak bırakılmıştı.
- **Çözüm:** boş durumda imleç 1×; ray `padding: 9px 0` + `background-clip: content-box` (görünüş aynı, 28 px dokunma), duraklara `::before` ile 40 px dikey alan + `min-width: 40px`. Bugün akışındaki "Tümü" bağlantısı (14 px) negatif kenar boşluklu 40 px alana alındı (`today.css .t15-more`). Takvim, kronometre ve tam ekran ayarlarındaki `kre-tgl` anahtarlarına `aria-label` eklendi (adsız düğme).
- **Kural:** Görünür öğe küçük olabilir ama dokunma alanı ≥40 px (dolgu/`::before`); yer tutucu değer ile açıklama metni aynı varsayımı göstermeli; her `role="switch"` düğmesinin erişilebilir adı olur (label içi olmak yetmez).

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

## H432 — Ders PDF ekranı kaydırırken "parçalanıp geri geliyordu" (2026-10-28, kullanıcı bildirdi)
- **Kök neden:** Önizleme iframe'i içerik boyunda (~89.000 px) ve telefonda en az 1000 px genişti; tarayıcı bu dev katmanı karo karo çizip ekran dışını atıyor, kaydırırken karolar boş/kırık görünüp yeniden çiziliyordu (iPhone'da katman belleği düşük). Telefonda belge yana da taşıyordu.
- **Çözüm/kural:** Çerçeve ekran boyunda, belge içinde kayar; dar ekranda belge çerçeve genişliğine `zoom` ile sığar, yazdırmadan önce ölçek kalkar (afterprint ile geri gelir). Ölçüm: telefonda çerçeve 358×642, ölçek 0,358, yatay taşma 0; masaüstünde 1010×694. Önizleme/gömülü belge iframe'i içerik boyuna büyütülmez.

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

### H507 — iPad'de sesli dersten geri çıkılamıyordu; "başlığa bas = geri" çalışmıyordu (2026-11-06)
- **Belirti:** iPad'de geri tuşu görünmüyor (sistem düğmeleri kapatıyor); sesli ders başlığına basınca da geri gidilmiyordu.
- **Kök neden:** (1) başlık-geri yalnız kabuk üst barındaki `.v15-top-h.is-geri`'ye bağlıydı; sesli ders odak ekranı kabuk barını çizmez, kendi `.cd15-baslik`'ını çizer → işleyici yoktu. (2) Alt "‹ Geri" hapı yalnız pencere kipi algılanınca (`data-pencere="dar"`) ya da 2 yedek kullanımdan sonra çıkıyordu; tam ekran Safari'de algı tutmadığı için hiç görünmüyordu.
- **Çözüm:** `shell/ipadPencere.tsx` — iPad'de `.cd15-baslik` tıklaması `geriTetikle()`; hap iPad'de her zaman (geri varken) gösterilir.
- **Kural:** Geri yolu eklerken odak ekranlarını (kabuk dışı başlıklar) ayrıca kapsa; "algılanırsa göster" türü güvenlik yollarını algının başarısız olduğu durumda da sına.

### H519 — Sesli ders › Oynatıcı çekmecesinde "Hız" başlığı ve hız hapları içeriden/ortadan başlıyordu (2026-11-09)
- **Belirti:** Çekmecede "Ses", "Tekrar", "Bölüm sonunda dur" satırları sola dayalıyken "Hız" başlığı ~28 px içeride, yatay telefonda hız hapları ortada ve dar duruyordu.
- **Kök neden:** `sesli.css` sonundaki `.cd15-sat.cd15-sat-blok { align-items: stretch }` kök öneksiz (özgüllük 0,2,0); dosyanın başındaki iç içe `:root[data-v15='on'] { & .cd15-sat { align-items: center } }` (0,2,1) kazanıyordu. Yön (`column`) çakışmadığı için uygulanıyor, hizalama uygulanmıyor, hata yarım göründüğünden fark edilmemişti.
- **Çözüm/önleme:** üç kurala `:root[data-v15='on']` öneki. Kural: v15 iç içe bloktaki bir sınıfı sonradan ezen kural aynı kök önekini taşır; öneksiz "ek" kural yazılmaz.

### H520 — Sesli ders listesinde süzgeç hapları sıralama düğmesinin altına giriyordu (telefonda "Arşiv" üstüne simge, tablette "Bitti" yarım) (2026-11-09)
- **Belirti:** `/dersler/canliders` üst satırında "Bu yıl · Arşiv" seçicisinin "Arşiv" yazısının üstüne sıralama (⇅) simgesi biniyor; tablette son hap yarım kesiliyordu.
- **Kök neden:** `.v15-hscroll` kenardan kenara kaysın diye `margin-inline: calc(var(--v15-pad) * -1)` ile iki yana taşar; bu satır tam genişlikte tek başına durduğunda doğrudur. Sesli liste, Öğren kitaplığı, Özetler gibi ekranlarda aynı satırın **sağında** sıralama/arama düğmesi var; sağ eksi boşluk hapları 16 px düğmenin altına sokuyordu.
- **Çözüm/önleme:** `dersler.css`: `.o15-ust > .o15-cipler.v15-hscroll:not(:last-child) { margin-right: 0 }` (aynı kalıbı kullanan bütün ekranları kapsar). Kural: `.v15-hscroll` yanında kardeş öge varsa o yandaki taşma kapatılır.


### H602 — Sesli ders telefon/tablet: oynatıcı düğmeleri 30–34 px, konum çubuğu 16 px, tablette başlık kesik; PDF parçası geç isteniyordu (2026-11-17)
- **Belirti:** Telefonda (375 px) alt oynatıcıda ileri/geri/bölüm düğmeleri 34×30, hız 31×28, konum çubuğu 16 px yüksekti; düğmeler sola yığılı, hız yazısı düğme gibi görünmüyordu. Tablette (768 px) başlık "Tümör Biyolojisi ve…" diye kesiliyordu. Paragraf yıldız/kopya 30 px, "örnek sorular" çipi 26 px. Açılışta slaytlar sesten ~2 sn sonra geliyordu.
- **Kök neden:** (1) "Minimal alt çubuk" (2026-10-29) ölçüleri medya sorgusuz, yani masaüstü fare ölçüsü dokunmatik ekrana da gidiyordu; üstüne `max-width: 380px` kuralı düğmeleri 30 px'e daha da küçültüyordu (en dar ekranda en küçük hedef). (2) H111q başlık sarması yalnız `max-width: 767px` içindi; 768–1099 px'te görünüm seçici (250 px) + 3 simge başlığa ~210 px bırakıyor. (3) `PdfDocView` (pdfjs) tembel parçası ancak ders JSON'u gelip PDF bölmesi çizilince isteniyordu: ders verisi → bölme → parça → worker → sayfa sıralı zincir.
- **Çözüm:** `styles/v15/sesli.css` sonu: `@media (pointer: coarse), (max-width: 1024px)` altında taşıma düğmeleri 44, oynat 48, hız kenarlıklı hap 48×36 (+`::after`), ⋯ 44, `.cd-cubuk` dokunma yüksekliği 28 (iz ince kalır); ≤380/≤340 px'te genişlik daralır, yükseklik 44 kalır; paragraf yıldız/kopya ve çıkmış/örnek çipine `::after` dokunma alanı; 768–1099 px'te başlık iki satır. `CanliDersDers.tsx`: modül yüklenirken `import('../learn/pdf/PdfDocView')` koşut başlatılır. Çizim/zamanlama mantığına dokunulmadı (kural 17/18).
- **Kural:** Oynatıcıya "küçült/minimal" ölçüsü verilirken dokunmatik karşılığı aynı değişiklikte yazılır; dar ekran kuralı dokunma hedefini 44 px altına indirmez (genişlik daralır, yükseklik kalmaz). Başlık sarma kuralının eşiği, yanındaki sabit genişlikli ögelerin göründüğü aralığı da kapsar. Her derste gereken tembel parça, verisi beklenirken koşut istenir.

### H636 — KMB videolarında bazen ses gelmiyor, ancak ekrana dokununca başlıyor (2026-11-18)

- **Belirti:** KMB ders videosu/hedef filmi oynarken görüntü sürüyor ama ses yok; ekrana dokununca ses geliyor (özellikle iOS/Safari, ses henüz inmemişken ve otomatik sıradaki videoda).
- **Kök neden:** `LottieVideo` sesi blob olarak `fetch` sonrası src'ye koyup `play()`'i rAF döngüsünden, `HedefFilmi.sesBaslat` ise `await sesOnYukle(...)` sonrasında her klip için YENİ `Audio` öğesiyle çağırıyordu → `play()` kullanıcı dokunuşunun dışında kalıyor, tarayıcı NotAllowedError veriyordu; hata `catch(() => {})` ile yutulup görüntü sessiz sürüyordu.
- **Çözüm:** `kmb/sesKilit.ts::sesKilidiAc` dokunuş anında (eşzamanlı, await'ten önce) öğeyi sessizce oynatıp kilidini açar; blob inmediyse ağ adresiyle başlanır; `HedefFilmi` tek kalıcı ses öğesi + çağrı sayacı kullanır; engel yine olursa görüntü sessiz sürmez, film durup ▶ gösterilir.
- **Kural:** Ses `play()`'i asla yalnız `await`/zamanlayıcı/rAF sonrasında ilk kez çağrılmaz; öğe dokunuş işleyicisinde eşzamanlı açılır ve yeniden kullanılır. NotAllowedError yutulmaz, oynatıcı durdurulup kullanıcıya ▶ gösterilir.

### H637 — KMB seslerinde başta 1-2 sn ve cümle başlarında kesikler (2026-11-18)

- **Belirti:** KMB videosu açılışında 1-2 sn ses kesiliyor, bazı cümlelerin başı yutuluyor.
- **Kök neden:** (1) H636 düzeltmesi blob inmeden ses öğesine AĞ adresini koydu; akışta her cümle başı konumlaması tampon bekletti. (2) Döngü, duraklamış sesi `play()` ederken söz çözülene dek görüntü saatini ilerletiyordu; ses geride kalınca >0,3 sn farkla ileri konumlanıp cümle başını atlıyordu.
- **Çözüm:** Kilit kısa sessiz WAV ile açılır, gerçek ses yalnız blob inince konur (`sesKilit.ts::sesYok`); `play()` sözü beklerken görüntü de bekler.
- **Kural:** Kilit açmak için gerçek klip ağdan akıtılmaz; ses başlatılırken görüntü saati sesin hazır olmasını bekler, sesi ileri konumlayarak "yetiştirmek" yasak.

### H638 — KMB video oynatıcıda tam ekrana girip çıkamama, tam ekranda dokunma sorunları (2026-11-18)

- **Belirti:** Tam ekran bazen açılmıyor/kapanmıyor; tam ekrandan sonra telefon yatayda kalıyor; tam ekranda dokunuşlar yanlış yere gidiyor, sağ kenarda arkadaki sayfa dokunulabiliyor.
- **Kök neden:** (1) Telefonda satır içi oynatıcıya verilen `margin: 0 -12px` sahte (iOS) tam ekran katmanını 12 px sola kaydırıyordu; sağda sayfa açıkta kalıyor, arkadaki sayfa da kaydırma kilidi olmadığı için kayıyordu. (2) Ders videosu katmanı (DersVideo) zaten tam ekranken iç oynatıcının düğmesi kendi öğesini ayrıca tam ekrana alıyordu (iç içe): üst çubuk ve Kapat düğmesi kayboluyor, düğme durumu yanlış ("Tam ekran" görünüyor) kalıyordu. (3) Girişte `screen.orientation.lock('landscape')` konuyor, hiçbir çıkışta `unlock` edilmiyordu. (4) Site yazı boyutu (uiZoom, ata öğede CSS zoom) tam ekran katmanını da büyütüp denetimleri ekrandan taşırıyordu.
- **Çözüm:** Tam ekran/sahte kipte kenar payı sıfır; sahte kipte kaydırma kilidi; doldur kipinde tam ekran hedefi Kapat çubuğunu da içeren katman, durum `fullscreenElement.contains(...)`; her çıkışta ve film kapanışında `yonKilidiAc()`; tam ekranda ata zoom'u tersiyle nötrlenir; Fullscreen API yoksa film katmanlarında işe yaramayan tam ekran düğmesi gizlenir.
- **Kural:** Tam ekran katmanına satır içi düzenin kenar payı/zoom'u taşınmaz; iç içe tam ekran istenmez (katman varsa onu hedefle); her yön kilidi çıkışta kaldırılır; sahte tam ekranda sayfa kaydırması kilitlenir.

## Sesli ders "İlerlemeyi temizle" yenileyince eski ilerleme geri geliyordu (2026-11-21)
- **Belirti:** Temizle/sıfırla sonrası sayfa yenilenince (ya da öteki cihaz eşitlenince) süre, bitti işareti ve soru sayıları geri geliyordu.
- **Kök neden:** `medsoru_calisma_takip_v1` korumalı birikimli anahtar (mezar taşıyla silinmez); `mergeKvJsonValue` sn/soru'da `max`, konu kayıtlarında birleşim alır. Yerelde kaydı silmek sunucudaki eski kaydı ezemiyor, eşitlemede geri yazılıyordu.
- **Çözüm:** `konuSifirla`/`modulSifirla` kaydı silmek yerine `sif` zamanlı boş kayıt bırakır; birleşme bunu yönetici düzeltmesi (`adm`) gibi, kendinden eski kayıtlara üstün sayar. Listeler `sifirlanmisMi` ile bu kaydı "yok" sayar.
- **Önleme:** Birikimli (max/birleşim) eşitlenen bir anahtarda silme = kayıt silmek değil, zaman damgalı sıfır kaydı yazmaktır.

### Sesli ders listesinde V2/V3 sürümleri yanlış numaraya düşüyordu (2026-11-24)
- **Belirti:** Mesane V2/V3 "Patoloji 26" (Böbrek'in yanında), İnvaziv Serviks V2/V3 "Patoloji 39" (listenin en sonunda) görünüyordu.
- **Kök neden:** Kurul 1 numarası PDF'in Drive dosya adındaki "26)" gibi sayıdan okunuyor; çakışan numaralar `canliDers.ts › BRANS_DUZELT` ile yalnız V1 anahtarına düzeltilmişti. `…-v2/-v3` anahtarları düzeltmeyi bulamayıp aynı PDF'in hatalı numarasına düşüyordu.
- **Çözüm/önleme:** `bransBilgisi` elle düzeltme ve yedek tabloda sürüm ekini (`-v\d+`) atıp V1 kaydına da bakar. Yeni sürüm anahtarı eklerken V1 düzeltmesi kendiliğinden geçer; ayrı kayıt yazma.

## H652 — Sesli derste "Derste kendiliğinden göster" ayarı bulunamıyordu (2026-11-24)
- **Belirti:** Kullanıcı ara soruların derste kendiliğinden çıkmasını açıp kapatacak yeri göremedi.
- **Kök neden:** Ayar yalnız ara soru sayfasının alt çubuğundaydı; varsayılan kapalı olduğu için sayfa ancak elle açılınca görünüyordu, "hepsini çöz" (ünlem) akışında ise hiç gösterilmiyordu. Ayar ile ayara ulaşmanın tek yolu aynı kapalı kapının arkasındaydı.
- **Çözüm:** `CdHocaAra.tsx › useHocaAraTercih` (abone olunabilir ortak tercih) eklendi; Görünüm çekmecesi › Okuma sekmesinde "Soruları derste kendiliğinden göster" ve "Soruyu otomatik çöz" anahtarları her zaman görünür. Soru sayfasındaki kutular aynı tercihi okur/yazar.
- **Önleme:** Bir özelliği açan/kapatan ayar, o özellik kapalıyken de ulaşılabilir kalıcı bir yerde (ayar çekmecesi) durur; yalnız özelliğin kendi ekranına konmaz.

## H653 · Ses yüklenirken sessizlik "ses yok" sanılıyor (2026-11-24)
- **Belirti:** Örnek soru çözücü, sesli ders, terim sesi vb. ilk tıklamada bir süre sessiz; öğrenci sesin olmadığını sanıyor.
- **Kök neden:** Her oynatıcı kendi `Audio`'sunu açıyor; dosya inene/arabelleğe alınana kadar hiçbiri durum göstermiyordu.
- **Çözüm:** `src/services/sesYukleniyor.ts` (`main.tsx`'te kurulur) `HTMLMediaElement.prototype.play`'i sarar; `HTMLAudioElement` `readyState<3` iken ya da `waiting`'de 250 ms sonra alt ortada "Ses yükleniyor…" gösterir, `playing/pause/ended/error`'da kaldırır. Stil `styles/motion.css`.
- **Önleme:** Yeni sesli işlev ayrıca gösterge yazmaz; `play()`'i atlayan (Web Audio API) oynatıcı eklenirse aynı gösterge ona da bağlanır.

## H654 · Ders analizi `ozetEksik.join is not a function` (2026-11-24)
- **Belirti:** canlı derste analiz sekmesi açılınca sayfa çöker.
- **Kök neden:** `src/data/ders_analizi/k2-41.json` içinde `ozetEksik` elle düz metin yazıldı (cfc10441); `CdDersAnaliz.tsx` liste bekleyip `.join` çağırır; `uret.py --dogrula` alanın türüne bakmıyordu.
- **Çözüm:** veri listeye çevrildi; doğrulayıcı tür denetimi ekledi; ekran metin/listeyi kabul eder.
- **Önleme:** şemadaki liste alanı elle yazılırken tür korunur; `uret.py --dogrula` 0 HATA olmadan yayın yok.

## H655 · Sesli ders ve örnek soruda metin takibi yanlış yeri gösteriyor / geç kalıyor (2026-11-24)
- **Belirti:** Sesli derste konuşulan cümlenin PDF'teki karşılığı işaretlenmiyor, yanlış maddeye gidiyor ya da vurgu geç yanıyor; örnek soru çözücüde okunan yer cümle değişiminde gecikiyor, cümle içinde kelime takibi yok.
- **Kök neden 1 (PDF yeri):** `pdf_isaret.eslestir` slayt maddesini yalnız ortak 5 harf kökle arıyordu, yani anlatımın slaytı birebir okumasını bekliyordu. Hocanın anlatımı slaytı başka sözcüklerle anlatır → ~6.000 cümle "sayfa"/"kelime"ye düştü ya da tek yaygın kelimeyle yanlış maddeye gitti.
- **Kök neden 2 (geç vurgu):** Kelime kutusu yalnız slaytta birebir geçen kelimeye veriliyordu; istemci `useFocus` yalnız tam eşleşen kelimede yanıyordu → aradaki (hocanın kendi) kelimelerde vurgu sönüyor, ortak kelime gelene dek bekliyordu.
- **Kök neden 3 (çözücü):** Etkin cümle `t < e + 0,4` kuyruğuyla seçiliyordu → yeni cümleye 0,4 sn geç geçiş; cümle içi kelime takibi yoktu.
- **Kök neden 4 (kelime zamanı, eski varyantlar):** Hizalama ekran metniyle yapılıyordu (ses EMA okunuşunu söyler: "5 mg" → "beş miligram"), 2 harflik rastgele bloklar çapa sayılıyordu. Ayrıca metni sonradan genişletilmiş ESKİ ses varyantlarında (23 varyant, 11 ders) metnin bir kısmı seste hiç yok → kelimeler paragraf sonuna yığılıyor. Varsayılan (en yeni) varyantların hepsi sağlam.
- **Çözüm:** `scripts/uretim/sesli_anlatim/anlam_esle.py` (bge-m3 CPU vektörü + kelime kanıtı, eşik 0,52 / fark 0,025) kelime kanıtı zayıf cümlede atanan sayfa ±1'deki maddeyi anlamca seçer; `w_doldur` ortak kökleri çapa alıp aradaki konuşma kelimelerini maddenin kelimelerine sırayla dağıtır. `pdf_isaret` SURUM 9, tüm dersler yeniden üretildi. İstemci: vurgu son karşılıkta kalır (`CanliDersDers.tsx`); çözücü başlamış son cümleyi alır ve okunan kelimeyi CSS Highlight API ile işaretler (`SoruCozucu.tsx`, `vurgu-kalemi.css`). `kelime_zaman.py`: okunuşla hizalama, ≥3 harf blok, hız sınırlı tutarlı çapa zinciri, ASR önbelleği (`meds_temp/kelime_zaman/asr/`).
- **Önleme:** Anlatım ↔ slayt/metin eşlemesinde birebir metin beklenmez; sözcük eşleşmesi tek ölçüt olamaz (anlam + sıra). Seste olmayan metin için zaman uydurulmaz: metni değişen ses varyantı ya yeniden seslendirilir ya da sunulmaz.
