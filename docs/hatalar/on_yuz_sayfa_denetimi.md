# Hata defteri — on_yuz_sayfa_denetimi (sayfa denetimi bulguları, öğrenci sayfaları, veri/eşitleme ekranları)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16; `hatalar/on_yuz.md` 4 konuya bölündü). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## H86 — Sınav planı Kurul 2'de boş sayfa (2026-10-27)
- **Belirti:** `/kamplar/sinav-plani` yalnız başlık ve açıklamayı gösteriyor, altı bomboş.
- **Kök neden:** aktif kurul takvimden 2; `planVerisiYukle` `kurulDagilimi(2)` bulamayınca (sinav_dagilimi.json'da Kurul 2 yok)
  `null` dönüyor, `SinavPlani` da `if (!plan) return null` ile hiçbir şey çizmiyordu.
- **Çözüm:** boş durum iletisi ("Kurul N için sınav dağılımı henüz girilmedi"). Kurul 2 dağılımı girilince plan kendiliğinden kurulur.
- **Önleme kuralı:** kurula bağlı veriyle çizilen her ekran, veri yokken `null` değil nedenini söyleyen boş durum gösterir;
  yeni kurul açılırken `sinav_dagilimi.json`'a o kurulun dağılımı eklenir.

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

## H111r · Soru haritası hücrelerinde yazı kontrastı 2.6–4.0 (2026-10-28, Soru çöz)
- **Belirti:** `/sorular/soru-haritasi` ısı tablosunda orta yoğunluktaki hücrelerin sayıları zor okunuyordu (WCAG AA altında, açık ve koyu temada).
- **Kök neden:** renk yoğunluğu %12–90 arası sürekli ölçekti; %40–85 aralığında zemin orta mavi olduğundan ne koyu (`ink`) ne açık (`on-accent`, eşik %55) yazı 4.5'i geçebiliyordu.
- **Çözüm:** `SoruHaritasiV15.tsx` ölçeği iki banda ayırır: açık bant %10–40 (koyu yazı), koyu bant %90–100 (açık yazı); ara ton kullanılmaz. DOM kontrast ölçümü: 7 ihlal → 0.
- **Kural:** Yoğunluğa göre boyanan hücrede yazı rengi tek eşikle seçiliyorsa, eşiğin iki yanındaki zemin tonları her iki yazı rengiyle de 4.5'i geçmelidir; geçmiyorsa ara tonlar atlanır.

## H111t · Ders çalış dokunma hedefleri: "Tüm dersler" 75×14, Öğren "▶ Dinle" 52×20 px (2026-10-28, Ders çalış)
- **Belirti:** Dersler merkezinde "Tüm dersler" bağlantısı ve Öğren adımındaki "▶ Dinle" düğmesi telefonda parmakla zor seçiliyordu.
- **Kök neden:** `.d15-more` yalnız metin yüksekliğindeydi (line-height 1); `.ls-tag` 20 px rozet stili düğmeye de uygulanıyordu.
- **Çözüm:** `dersler.css .d15-more` 40 px dolgu + negatif kenar (H111g ile aynı desen); `LessonPlayer.tsx` düğmeye `ls-dinle` sınıfı, `v12/lesson.css` dokunmatikte `::before` ile 40 px alan.
- **Kural:** H111g kuralı: görünür öğe küçük kalabilir, dokunma alanı ≥40 px.

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

## H340–H347, H360–H374 — Sayfa denetimi düşük önemli bulgular (2026-10-28)
- **Öğrenci (H340–H347):** boş Notlarım'da arama kutusu gizli; bildirim yokken toplu eylemler gizli; müzik ilerleme çubuğu 28 px; Bugün şerit etiketi tek satır; arama sıralama seçici 36 px; sınav planında gereksiz "· K2" eki; topluluk ders yorumları boş durumuna "Derslere git"; İlk adımlar ilerleme çubuğu belirgin.
- **Yönetim (H360–H374):** serbest girdiden soruya, olası sorudan ayrıntıya, ses işinden sesli derse, desteden derse, oyuncudan kişiye bağlantı; Gelen kırıntısı "Yönetim › Gelen"; ders sekmesi (`?sekme=`), kurul ve kamp çekmecesi (`?ac=`) adreste; kurul takvimi bildirimi "dağıtımda yansır"; çöp kalıcı silme onayında hedef; görünürlükte "bayrağa git"; Puan/ATP tehlikeli işlemler açık listeyle (`ozel_kaldir` artık uyarılı); şikâyet sayfasında "Gizlenen mesajlar" kartı; Gelen "Ek" sütunu varsayılan gizli.
- **Kural:** Tehlikeli işlem ad kalıbıyla değil açık listeyle belirlenir (H182, H372). Açık çekmece/sekme adreste tutulur ki yenileme ve paylaşım aynı görünümü açsın.
- Açık öneriler (yapı): menü/başlık ad eşleşmeleri, `kurul_2` adres biçimi, yinelenen girişler (KMB, Sözlük/Hastalıklar, takvim), havuz dondurmanın Bayraklar'a taşınması, ses kuyruğunun sesli ders sekmesi olması, sürüm notu + dağıtım bilgisinin birleşmesi. Veri: kazanımlarda yinelenen konu 31, soru haritası 498 / çıkmış 502 farkı.

## H380–H387 — Kalan küçük öğrenci bulguları (2026-10-28)
- Menü etiketi, sayfa başlığı ve ROUTE_TITLES tek ada eşitlendi (Etkileşimli dersler, Sesli dersler, KMB dersleri, Müzik, Patoloji/TBG Check Up, Havuz doluluğu, Çevrimdışı ve indirmeler); içeriksiz kurul sekmeleri kesikli + "henüz yok"; telefonda kurul şeridi kenar soluklaştırma; sayaçlarda mono yerine tabular rakam; "Karma test · 20 soru" etiketi; testten çıkışta cevap varsa onay; KMB "Hazır/Yakında" ayrımı.

## H400–H406, H420–H424 — Yapı sadeleştirme: yinelenen sayfa ve girişler (2026-10-28, kullanıcı kararı)
- **Öğrenci:** Geçmiş kurullar ayrı sayfası menü/merkezden kalktı; kurul seçicilerde sınavı geçmiş kurul "Geçmiş" etiketli (sınav tarihi ipucu). `/gecmis-kurullar` (+ `/arsiv`…) → `/dersler` (`?kurul=N` → `/dersler/kurulN`). KMB tek kanonik `/dersler/kmb`. Sözlük ↔ Hastalıklar sekme çifti yerine tek "…'a git" bağlantısı. Başvuru'daki yinelenen "Kurul takvimi" kartı kalktı (Sınav takvimi kanonik). Adres okuyucu eski `kurul_N` biçimini `kurulN`/`?kurul=N`'e çevirir (replaceState).
- **Yönetim:** Ses kuyruğu → Sesli ders sekmesi (`ogrenme/sesli?sekme=kuyruk`); Sürüm notu + Dağıtım bilgisi → tek sayfa `site/surum` (dağıtım bölümü `?bolum=dagitim`); Havuz dondurma → Özellik bayrakları bölümü (`site/bayraklar?bolum=dondurma`). Tam yol yönlendirme tablosu `ESKI_YOL` (menu.ts), sabit/son kullanılan listeleri açılışta yeni yola çevrilir, `?bolum=` ile bölüme kaydırma.
- **Kural:** Aynı işi gören ikinci giriş/sayfa açılmaz; birleştirmede bileşen silinmez (yönlendirme + menüden kaldırma), eski adres yeni yere yönlenir ve SITE_HARITASI_KURALLARI.md'ye yazılır.
- **Not:** Kazanımlar ve Kurul kampı artık Geçmiş kurullar sayfasından kurula süzülmüş açılmıyor; kendi kurul seçicileriyle açılıyor.

## H435 — Sıralama: ölçü değişince eski veri yanlış birimle görünüyor, tepki geç (2026-10-29)
- **Belirti:** Sıralamada ölçü/süzgeç değiştirince başka sütunun verileri görünüyor, tepki geç geliyordu.
- **Kök neden:** yeni istek giderken önceki yanıt (`veri`) ekranda kalıyor ve YENİ ölçünün biçimleyicisiyle yazılıyordu (puan sayıları "soru"/"basamak" diye); "Yükleniyor" yalnız liste boşken çıkıyordu. Her geçiş ağ gidiş-dönüşü bekliyordu (sunucu 2–11 ms, gecikme ağ). 
- **Çözüm/önleme:** yanıt istek anahtarını taşır (`anahtar`), yalnız güncel anahtarla eşleşen yanıt çizilir, yoksa iskelet; sayfa ömürlü önbellek + eşzamanlı istek birleştirme + diğer ölçülerin arka planda önden yüklenmesi; SSE değişiminde önbellek temizlenir. Kural: süzgeçli listede yanıt, isteğin anahtarıyla etiketlenmeden ekrana basılmaz.

## H436 — Hata defteri tekrar ekranı yan rayın altında (2026-10-29)
- **Belirti:** Öğren › Tekrar ekranında geri düğmesi ve başlık ("Hata defteri · …", "Tekrar") soldan kesik; seçili sekme koyu temada görünmüyor.
- **Kök neden:** `LearnReview` `.ls-root` sabit katmanı `.sh-main` içinde çiziliyordu; `.sh-main`'in zoom/yığınlama bağlamı sabit katmanı v15 yan rayının (z 40, uygulama düzeyi) altına itti. Seçili segment `--color-white` zemini koyu temada alan rengiyle aynıydı.
- **Çözüm/önleme:** tam ekran katman `createPortal(..., document.body)` ile gövdeye taşındı; v15'te seçili segment vurgu karışımlı. Yeni tam ekran katman `.sh-main` içine değil gövdeye portal edilir.

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

### H514 — Örnek sorular ders listesinde "Hoca üslubu · N yeni soru" rozeti öğretim üyesi adının üstüne biniyordu (tablet/masaüstü, 2026-11-09)
- **Belirti:** 768–1024 px tablette (ve masaüstünde) `/sorular/ornek` ders satırlarında rozet ile "Prof. Dr. …" yazısı aynı yere çizilip okunmaz oluyordu; telefonda alt alta göründüğü için fark edilmemişti.
- **Kök neden:** `KazanimSorulariView.tsx` iki ayrı `.ks-lesson-who` span yazıyordu; `secondary.css` ≥720 px ızgarasında ikisi de `grid-area: who` alanına düşüyor (ızgara aynı alana iki öge koyunca üst üste bindirir). ≤719 px düzeninde alanlar satır satır aktığı için sorun yalnız geniş ekranda çıkıyordu.
- **Çözüm/önleme:** tek `.ks-lesson-who` içinde yazar + ` · ` + rozet (`<b>`); alan `white-space: normal` ile sığmazsa sarar. Kural: adlandırılmış ızgara alanına (`grid-area`) birden çok kardeş öge yazılmaz; koşullu ek satır aynı kabın içine girer. Düzen değişikliği telefon + tablet (768/820) + masaüstü üçünde birden denetlenir (`scripts/altyapi/perf/sayfa_tarama.mjs` taşma raporu üst üste binmeyi GÖREMEZ, ekran görüntüsüne bakılır).

### H551 — Giriş yapmış öğrenci kendi profilini ve arkadaşlık isteklerini göremiyordu (2026-11-10)
- **Belirti:** girişli kullanıcıda Arkadaşlar listesi ve gelen/giden istekler boş, açık profil "Profilleri görmek için giriş yapmalısın", gizlilik anahtarı yüklenmiyor.
- **Kök neden:** `adminFetchAuth.ts::ogrenciJetonu` öğrenci jetonunu GET isteklerinde yalnız `/api/(basarim|olasi-sorular|topluluk)/` yollarına ekliyordu. Arkadaşlık okuma uçları (`GET /api/arkadas`, `/api/kisi/ben|ara|siralama|:kimlik`) jetonsuz gidiyor, sunucuda `verifiedUid` boş kalıyor → `{girisli:false, arkadaslar:[]}` ya da 401. Yazma uçları (POST) jeton taşıdığı için istek gönderilebiliyor ama görülemiyordu. Ayrıca açılışta oturum geri yüklenmeden giden öğrenci isteği jetonu beklemiyordu (bekleme yalnız yöneticideydi).
- **Çözüm:** izin listesine `kisi/` ve `arkadas` eklendi; jeton gerektiren öğrenci isteği de `auth.authStateReady()`'yi (≤4 sn) bekler.
- **Önleme:** `verifiedUid` okuyan yeni bir GET ucu eklenince `ogrenciJetonu` listesine de eklenir; uç yazıldığında girişli kullanıcıyla tarayıcıdan GET sınanır (curl'deki jetonsuz yanıt "çalışıyor" sayılmaz).

## H588 — Dağıtımdan hemen sonra tembel ekran "e._result.default" / React #306 ile çöküyor (2026-11-16)
- **Belirti:** canlı istemci hata kaydı: dağıtımdan ~90 sn sonra iPhone Safari'de `/dersler/canliders` → `undefined is not an object (evaluating 'e._result.default')` (6 kez); 15 Kasım'da `/dersler/interaktif/...` → `Minified React error #306`. Öğrenci boş/çökmüş ekran görüyor.
- **Kök neden:** `index.html` ve `main.tsx`'teki `vite:preloadError` dinleyicisi kendi yenileme kurtarması için `event.preventDefault()` çağırıyor (H572). Vite'ın `__vitePreload` sarıcısı bu durumda başarısız `import()`'u reddetmek yerine `undefined` ile ÇÖZER; `React.lazy` boş modülü geçerli sayıp `default`'a erişirken çöker. Yenileme 8 sn kısıtlı olduğundan ikinci denemede kullanıcı çökmüş ekranda kalır. `wrapLazy` yalnız REDDEDİLEN içe aktarmayı ele alıyordu; ~60 tembel bileşen sarıcısızdı.
- **Kalıcı çözüm:** `src/utils/guvenliLazy.tsx` — modül yoksa ya da `default` yoksa bunu yükleme hatası sayar (çevrimiçi + sunucuya ulaşılıyorsa tek yenileme, çevrimdışıysa bilgi ekranı, aksi hâlde "Yeniden Dene" kartı); tüm `React.lazy` kullanımları buna geçirildi.
- **Önleme kuralı:** `src` altında `guvenliLazy` dışında `React.lazy(` kullanılmaz (kapı `scripts/kapilar/lazy_denetim.py`). Canlı istemci hataları `python3 scripts/altyapi/saglik_raporu.py --canli` ile her dağıtımdan sonra okunur.

## H590 — Sesli ders: bağlantı gelince "Ağ bağlantısı yok" kartında kalıyor (2026-11-17)
- **Belirti:** çevrimdışıyken indirilmemiş sesli ders açılır, hata kartı çıkar; bağlantı geri gelince kart kalır, ders yüklenmez.
- **Kök neden:** `src/components/canliDers/CanliDersDers.tsx` yükleme etkisi yalnız ders anahtarı değişince çalışıyordu; istek bir kez hata verince aynı ders için yeniden deneme yolu yoktu (ne `online` dinleyicisi ne düğme).
- **Çözüm:** deneme sayacı etki bağımlılığında; kart görünürken `online` olayı + 6 sn'de bir `sunucuyaUlasilir()` yoklaması (sekme gizliyken durur), yanıt gelince kendiliğinden yeniden yükler; "Yeniden dene" düğmesi. Kalıcı hatalarda (404/400, sesi yok) yoklama yok.
- **Kural:** ağ isteğine bağlı her "yüklenemedi" kartı yeniden deneme yolu (düğme + bağlantı dönüşü) taşır; yükleme etkisi yalnız kimliğe bağlanıp hata durumunda kilitlenmez.

## H591 — Yönetim girişinde `au-*` stilleri yok ("Şifremi unuttum" stilsiz) (2026-11-17)
- **Belirti:** `/manage` giriş ekranında düğmeler, ileti kutusu ve yükleniyor simgesi stilsiz.
- **Kök neden:** `au-*` kuralları yalnız `src/styles/rebuild.css` §44'teydi; o dosyayı yalnız `src/main.tsx` içe aktarır. `src/manage-main.tsx` aynı giriş bileşenini (`EpostaBaglantiGiris`) çizer ama yalnız `yonetim-temel.css` alır; `ui-spin` animasyonu da `appearance.css`'te kalıyordu.
- **Çözüm:** §44 değişmeden `src/styles/giris-au.css`'e taşındı (+ `@keyframes ui-spin`); iki giriş dosyası da içe aktarır. Ana sitede kural sırası aynı.
- **Kural:** iki girişin (index/manage) ortak kullandığı bileşenin stili ortak, kendi başına bir CSS dosyasında durur ve iki girişten de içe aktarılır; yalnız ana sitenin toplu CSS'ine gömülmez.

## H603 — Bilinmeyen adres 200 dönüyordu; ekranda "Sayfa bulunamadı" çıksa da sunucu sayfayı var sayıyordu (2026-11-17)
- **Belirti:** `curl /yokboylesayfa` → 200 + boş SPA kabuğu. Ön yüz `BulunamadiV15` ekranını gösteriyordu, ama arama motoru, bağlantı denetleyicisi ve izleme bozuk adresi gerçek sayfa sayıyordu.
- **Kök neden:** `server.ts` SPA geri dönüşü (`app.get('*')`) her yola koşulsuz `index.html` + 200 gönderiyordu. "Bu adres var mı" kararı yalnız istemcideki `src/router.ts::parseLocation` içindeydi; sunucunun bu bilgiye erişimi yoktu.
- **Kalıcı çözüm:** Sunucu aynı çözücüyü tembel `import('./src/router')` ile yükler (`spaDurumKodu`); `route === 'bulunamadi'` ise durum 404, gövde yine `index.html` (ekran aynı). Çözücü yüklenemezse 200 (site kırılmaz, günlüğe uyarı). Yerel sınama: kaynak koddaki 107 iç bağlantının hiçbiri 404'e düşmedi; `/yokboylesayfa`, `/x/y/z`, `/meds/yokboyle` → 404; `/manage*` ve varlık 404'ü değişmedi.
- **Önleme kuralı:** Sunucuda ikinci bir rota listesi YAZILMAZ; yeni sayfa `router.ts`'e (BY_SEGMENT/ALIASES) ya da `siteHaritasi.ts` çevirisine eklenince sunucu da kendiliğinden 200 verir. `router.ts`/`siteHaritasi.ts` modül yüklenirken `window`/`import.meta.glob` çağırmamalı (sunucu tsx ile içe aktarıyor; bu çağrılar yalnız fonksiyon içinde, try ile).
