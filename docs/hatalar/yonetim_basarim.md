# Hata defteri — yonetim_basarim (yönetim paneli ve ön yüz başarımı)

> Tam metin (kelimesi kelimesine taşındı, 2026-11-16). Dizin: `docs/KURUL2_YAPILMAYACAK_HATALAR.md`.
> Yeni madde bu dosyanın SONUNA `## H<n> — …` başlığıyla eklenir + dizinin sonuna tek satır.

## H111d · Yönetim betik kataloğu her açılışta ana pakete iniyordu (2026-10-28, başarım)
- **Belirti:** İlk açılışta inen ortak parça (`chunk-contentLive`) ~210 KB; içinde yalnız yönetim "Betikler" sekmesinin kullandığı yedek betik kataloğu (`bundledScripts.ts`, ~20 KB kaynak) vardı.
- **Kök neden:** `services/api.ts` (her ekranın kullandığı istemci) kataloğu statik içe aktarıyordu; rolldown onu api ile aynı ilk yükleme parçasına koydu.
- **Çözüm:** `getScriptsList` kataloğu `await import('../data/bundledScripts')` ile yalnız çağrıldığında yükler. Ölçüm: index.html'in indirdiği JS+CSS 2.747 KB → 2.719 KB (102 → 91 dosya). (`manualChunks` ile `deckStore`'u ayırma denendi: rolldown ortak bağımlılıkları o parçaya çekip 443 KB'lık yeni bir ilk yük parçası üretti → geri alındı; `manualChunks` ile paylaşılan modül ayırmak YASAK, statik içe aktarmayı kaldır.)
- **Kural:** Ortak istemci/servis dosyaları (api.ts, auth, realtimeEvents) yalnız tek ekranın kullandığı büyük veri/katalog modüllerini statik içe aktarmaz; dinamik `import()` kullanılır.

## H111e · Profil verisi dinleyicileri render sırasında setState yapıyordu (2026-10-28, Bugün/Arka plan)
- **Belirti:** Her sayfa açılışında konsolda React uyarısı: "Cannot update a component (`ArkaPlanGosterge` / `EsitlemeKarti`) while rendering a different component (`MusicPlayerProvider`)".
- **Kök neden:** `userKvSync.onWrite` profil anahtarı yazılınca `onProfileDataChange` dinleyicilerini **eşzamanlı** çağırıyordu. `MusicPlayerProvider`'ın `useState` başlatıcısı (`getVoterId` → `getDeviceToken`) ilk açılışta localStorage'a yazıyor; bu yazım render içinde olduğundan dinleyicideki `setKv`/`setBekleyen` başka bileşenin render'ında setState oldu.
- **Çözüm:** `userKvSync.ts` `bildir()` dinleyicileri `queueMicrotask` ile çağırır (tüm dinleyiciler zaten zamanlayıcı/setState yapıyor; eşzamanlılık gerekmiyordu). Sınama: sayfa_tarama /bugun, /arka-plan konsol hatası 1 → 0.
- **Kural:** localStorage/depo yazımına bağlı olay yayıcıları dinleyicileri eşzamanlı çağırmaz (mikro görev); render içinde (useState başlatıcısı, useMemo) yan etkili yazım yapılmaz.

## H111f · Deste kataloğu (~600 KB) her sayfada yalnız sayı için iniyordu (2026-10-28, başarım)
- **Belirti:** /kaynaklar, /topluluk, /saglik, /sozluk, /basarimlar gibi desteyle ilgisi olmayan sayfalarda `decks/catalog.json` (dev 3,4 MB, prod ~600 KB) indirilip ayrıştırılıyordu.
- **Kök neden:** (1) `offlineDatabaseService.loadStats` IndexedDB'de deste yoksa `decksCount` için `loadDeckCatalog()` çağırıyordu (açılışta her sayfada çalışır). (2) `deckStore.patchCatalog` açılıştaki içerik yeniden eşitlemesinde (değişen deste kimliği varsa) önce tüm kataloğu yüklüyordu.
- **Çözüm:** `loadStats` katalog yüklüyse uzunluğunu, değilse son kayıtlı istatistiği kullanır (`isDeckCatalogLoaded`); `patchCatalog` kataloğu yüklemez, değişen girdileri ekler — `loadDeckCatalog` sonradan bunları korur (mevcut "early" birleştirmesi). /kamplar, /istatistik ölçümde katalog artık inmiyor.
- **Kural:** Yalnız sayı/özet için büyük veri modülü tembel yüklenmez; özet meta veride tutulur. Canlı yama işlevleri ana veriyi zorla yüklemez, yüklemeyi bekleyen birleştirmeye bırakır.

## H111u · Çıkmış sorular kart görünümü sınırsız büyüyor, Odak ızgarası 4.372 düğme çiziyordu (2026-10-28, Soru çöz, başarım)
- **Belirti:** `/sorular/cikmis` Kart görünümünde aşağı kaydırdıkça DOM 2.700 → 34.000 düğüme (300 kart) çıkıyor, uzun oturumda sayfa ağırlaşıyordu; Odak modunda sağdaki numara ızgarası süzgeç sonucunun tamamını (4.372 düğme) çiziyor, her Önceki/Sonraki'de hepsi yeniden render oluyordu.
- **Kök neden:** `PastExamsView` `filteredQuestions.slice(0, richLimit)` ile her "daha fazla"da baştan sona tüm kartları tutuyordu; `CikmisModGorunum.Odak` `sorular.map` ile tüm numaraları çiziyordu.
- **Çözüm:** Kart görünümü kayan pencere: yalnız son 60 kart (`RICH_WINDOW`) çizilir, üstte düşenler tarayıcının kaydırma çapasıyla görünen kartı oynatmaz, üstte "Önceki soruları göster (n)" düğmesi; sayaçlar `richLimit` ile gösterilir. Odak ızgarası geçerli sorunun 100'lük bloğunu çizer, ‹ › ile blok değişir. Ölçüm: 8 kaydırmada DOM 34.226 → ~7.100 (sabit); Odak açılışı ~650 düğüm.
- **Kural:** Kaydırdıkça yüklenen listeler sınırsız büyümez (pencere ya da sanal liste); yüzlerce öğelik gezinme ızgarası bloklara bölünür.

## H111v · Ana CSS 936 KB, tam katman sayaçsız, tam ekranda fazla yükseklik, kısa başlık, küçük yazı, çevrimdışı boş istekler (2026-10-28, kabuk/başarım)
- **Belirti:** (1) her açılışta 936 KB (151 KB gzip) ana CSS iniyordu; (2) iki tam katman (ör. Başarımlar rozet ayrıntısı + kronometre) üst üste açılıp biri kapanınca alttaki açıkken alt sekme çubuğu geri geliyordu; (3) uygulama tam ekranında `.sh-main` 20–28 px uzun, boş sayfada bile kaydırma; (4) telefonda ders ayrıntısı/sesli ders başlığı "Tümör Biyoloji…" diye kesiliyor, `v15-crumb` dokunma alanı 61×16 px; (5) v15'te 13 px açıklama ve 10–12 px metinler; (6) çevrimdışıyken `/api/presence`, `/api/user-data/backup`, `/api/surum`, `/api/music/playlist` boşuna atılıyordu.
- **Kök neden:** (1) Öğren ders ekranı `ls-*` stilleri (~800 satır) `index.css` içindeydi, `main.tsx` onu ilk yükte veriyordu; (2) beş bileşen `tam-katman` kök sınıfını doğrudan `classList.add/remove` ediyordu — ilk kapanan sınıfı siler; (3) v12 tam ekranda `--sh-top-h`/`--sh-top-vis`'i 0 yapıp `.sh-main`'e 48 px üst dolgu veriyor, v15 "ekrana sığan" sayfa yükseklikleri (`100dvh - --sh-top-h - --sh-tabs-h - 48px`) bu dolguyu bilmiyordu; (4) telefonda geri + 4–5 simge düğmesi başlığa ~120/75 px bırakıyor, başlık tek satır `nowrap`; (5) eski sayfalar 11–12 px ile yazılmış, alt sınır yoktu; (6) bu uçlar `getNetState()`/`navigator.onLine` denetlemiyordu (yalnız `userDataSyncService` denetliyordu; fetch koruyucusu bilmediği için hepsi ağa gidip SW 503/zaman aşımı üretiyordu).
- **Çözüm:** (1) `src/styles/ogren-ders.css` (index.css'in iki `ls-*` bölümü) yalnız ls-* çizen 13 bileşenden içe aktarılır; ana CSS 936,8 → 865,7 KB (151,2 → 139,9 KB gzip); hesaplanmış stil dökümü önce/sonra (375/1440, deste + 3 ders adımı) 0 fark. `html.ui-v3` ls katmanı, health/v12 ezmeleri yüksek özgüllükte olduğundan ana CSS'te kaldı. (2) `src/utils/tamKatman.ts` (`useTamKatman`, referans sayaçlı); beş bileşen ona geçti. (3) v15 tam ekranda (`:not(.cd-ders-acik)`) `--sh-top-h` ve `--sh-top-vis` = 44 px + güvenli alan; `.sh-main` artık tam görünüm yüksekliği. (4) Telefonda `.v15-top-h` iki satıra sarar (17 px, line-clamp 2); sesli derste Tam ekran düğmesi telefonda gizli (Görünüm çekmecesinde var); `v15-crumb::before` ile ≥40 px dokunma alanı. (5) `--v15-t-caption` 13 → 13,5 px; v15 stillerinde 95 font değeri (10–12 px, <.78rem) 12,5 px'e çekildi. (6) `net.ts` `cevrimdisiMi()` + fetch koruyucusunda arka plan uçları (`presence`, `user-data/backup`, `music/playlist`) çevrimdışıyken ağa çıkmadan reddedilir; `presence.ts` ve `UpdatePrompt` `/api/surum` denetimi çevrimdışıyken atlanır (bağlantı yoklaması `baglanti.ts`/probe `/api/surum`'u kullanmaya devam eder).
- **Kural:** Sayfaya özgü büyük stil bloğu `index.css`/`main.tsx`'e eklenmez, kullanan bileşenden içe aktarılır (sıra/özgüllük hesaplanmış stil dökümüyle doğrulanır). Kök sınıfı birden çok bileşen açıyorsa sayaçlı yardımcıdan geçer. Tam ekranda gizlenen çubuğun yerine dolgu konuyorsa ilgili yükseklik değişkeni de o dolguyu yansıtır. v15'te metin ≥12,5 px; istisnalar yalnız rozet/sayaç/kbd/kronometre mini saati/yazdırma belgesi (`dersPdf.css`)/ray etiketi. Arka plan eşitleme ucu ekleyen `net.ts` `BG_RE`'ye ekler.

## H131 — Yönetim öğrenci uygulamasının ortak girişiyle açılıyordu; ayrı giriş + SW önbellek zehirlenmesi riski (2026-10-28, Yönetim v16)
- **Belirti:** /manage ilk yükü 544 KB gzip JS + 152 KB gzip CSS (öğrenci App.tsx girişi, Tailwind index.css, splash, tüm kabuk yardımcıları); yönetim yavaş açılıyordu.
- **Kök neden:** v16 kabuğu `App.tsx` içinde `React.lazy` ile açılıyordu; yönetim için ayrı Vite girişi yoktu, bu yüzden öğrenci girişinin statik içe aktardığı her şey önce iniyordu.
- **Kalıcı çözüm:** `manage.html` + `src/manage-main.tsx` (yalnız adminFetchAuth, Firebase kimlik, palettes.ts tokenları, `styles/yonetim-temel.css`, kit, kabuk). `vite.config.ts` çoklu giriş; `server.ts` SPA geri dönüşü `/manage*` için `dist/manage.html`; geliştirmede `scripts/altyapi/vite/yonetimGirisi.ts`. Yönetici değilse (moderatör) ya da `?kabuk=v14` ise `manage-main` tam uygulamayı (`import('./main')`) yükler. Uygulama içinden /manage'e geçiş (`App.tsx yonetimGirisineGec`) tam sayfa gezinmesi yapar (10 sn döngü koruması). Ölçüm: /manage 544+152 KB → 179+5 KB gzip; tarayıcıda 191 KB aktarım, FCP 164 ms.
- **SW kuralı:** `public/sw.js` gezinme yanıtını `/` ve `/index.html` olarak da önbelleğe yazar; /manage artık farklı HTML döndürdüğünden yönetim gezinmesi SW'de atlanır (ağdan gelir) ve `CACHE_VERSION` v18'e çıktı (eski SW'nin bir kez zehirleyebileceği önbellek etkinleşmede silinir). **Önleme:** Sunucu bir yol için farklı HTML kabuğu döndürmeye başlarsa sw.js gezinme önbelleğinden o yol çıkarılır ve sürüm artırılır.

## H131a — `/react-dom/` eşleşmesi react-dom/server'ı her sayfanın açılış parçasına sokuyordu (2026-10-28)
- **Belirti:** `vendor-react` parçası 137 KB gzip (react + react-dom istemci ~60 KB olmalı); öğrenci ve yönetim açılışı gereksiz 70 KB taşıyordu.
- **Kök neden:** `manualChunks` `includes('/react-dom/')` ile eşleşiyordu: yalnız PDF dışa aktarımında (`v15/dersPdfHtml.ts`) dinamik kullanılan `react-dom/server` ve `@floating-ui/react-dom` aynı açılış parçasına zorlanıyordu.
- **Çözüm/kural:** Paket kökü düzenli ifadesi (`/node_modules/(react|react-dom|scheduler)/`) ve `react-dom/server|static` hariç. `vendor-react` 65,9 KB gzip; öğrenci açılışı 544 → 475 KB gzip. Elle parça gruplarken paket adı alt dize ile değil kök yolla eşlenir.

## H131b — Kişiler listesi arka tazelemesi 2,5 sn olay döngüsünü kilitliyordu (2026-10-28)
- **Belirti:** Panelde sayfa geçişlerinde ilgisiz istekler (people-access, basarim/kisiler, calisma-matris) aynı anda ~2 sn bekliyordu; tek başına çağrıldıklarında 5 ms.
- **Kök neden:** `peopleInsights.buildList` kişi başına `contributions(p)` çağırıyordu: her kişi için bütün çıkmış/havuz soruları taranıyor ve `learn_feedback.json` + `ornek_soru_bildirimleri.jsonl` yeniden okunuyordu (≈900 kişi × 6.000 soru). SWR liste her istekte arka planda yeniden hesaplandığından eşzamanlı her yönetim isteği bekliyordu.
- **Çözüm:** `contributionCountsAll(ps)` tek geçişte kimlik/ad dizinleriyle sayar (eşleşme kuralları birebir; 895 kişide sayılar önce/sonra aynı). `/api/admin/people` 2,5 sn → 0,05–0,15 sn. **Kural:** kişi × veri kümesi döngüsü yazılmaz; ters dizin bir kez kurulur.

## H141 — Yönetimde görünürlük tek tıkla, onaysız ve geri alınamaz yazıyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Site › Görünürlük ve ders/deste/önem görünürlük çiplerinde yanlış tık sayfayı/dersi tüm öğrencilere anında kapatıyordu; hangi sunucuya yazıldığı da yazmıyordu.
- **Kök neden:** Çip `onClick` doğrudan `siteAyarYaz`/PUT çağırıyordu; kit bildiriminde eylem yoktu.
- **Çözüm/kural:** Öğrenciden kaldıran değişiklik (gizli/kapalı/yalnız yönetici, menüden kaldırma) hedef sunucuyu (`yazimHedefi()`: canlı site / yerel sunucu) yazan onay ister; her yazım 8 sn "Geri al" bildirimi verir (`bildir(metin, ton, {etiket, yap})`).

## H142 — Mesaj/şikâyet yazarından kişiye geçilemiyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Topluluk mesaj çekmecesi yazarı yalnız uid kodu olarak gösteriyordu; kişinin diğer mesajlarını görmenin yolu yoktu.
- **Çözüm/kural:** `MesajTablosu` `git` alır; Yazan sütunu ve çekmece Kişi 360'a, "Tüm mesajları" `topluluk/mesaj?s.uid=` süzgecine bağlanır; Kişi 360'ta "Mesajları" düğmesi. Kişiye ait her kayıt panelde kişiye bağlantı verir.

## H143 — Yönetim tablolarında uzun içerikli satırın sütunları kayıyordu (2026-10-28)
- **Belirti:** Mesajlar'da oda mesajı satırlarında Mesaj/Kanal/Şikâyet sütunları başlıktan sağa kaymış, Durum ekran dışındaydı.
- **Kök neden:** Her satır ayrı ızgara ve `.m16-satir { min-width: max-content }`: uzun içerikli satır kendi genişliğine büyüyüp fr sütunlarını başlıktan farklı dağıtıyordu.
- **Çözüm/kural:** VeriTablosu sütun px alt sınırlarının toplamını `--m16-tablo-en` olarak verir; tüm satırlar aynı en küçük genişliği paylaşır (telefonda yatay kaydırma korunur). Satır ızgarası içeriğe göre genişlemez.

## H146 — Yönetim tabloları telefonda okunmuyordu (2026-10-28, sayfa denetimi)
- **Belirti:** 375 px'te tablolar yatay kayıyor, ilk ekranda 2-3 sütun görünüyor, durum/görünürlük/eylem sütunları ekran dışında kalıyordu.
- **Çözüm/kural:** VeriTablosu ≤640 px'te kart görünümüne geçer: başlık satırı gizli, ilk hücre kart başlığı, diğerleri "Sütun adı · değer" (`data-baslik`), seçim kutusu sağ üstte; kart yüksekliği değiştiği için sanal kaydırma kapanır. Yeni tablo sütunlarına düz metin `baslik` verilir (kart etiketi buradan gelir).

## H152 — Yönetimde ders ayrıntısından o dersin sorularına geçiş yoktu (2026-10-28, sayfa denetimi)
- **Çözüm/kural:** Sorular kartında örnek sorular, çıkmış sorular ve havuz için ders konusuyla süzülmüş (`?q=<konu>`) bağlantılar. Sayı gösteren her özet, o kayıtların listesine bağlanır.

## H153 — Yönetimde Yerel kipte hangi veriye bakıldığı belli değildi; birleştirmede asıl soru görünmüyordu (2026-10-28, sayfa denetimi)
- **Belirti:** Yalnız Canlı kipte bant vardı; Yerel'de hiçbir işaret yoktu. Havuz birleştirmede asıl soru görünmeyen seçim sırasına bağlıydı. Ders ayrıntısında görünürlük seçicisi kartın dışına taşıyordu.
- **Çözüm/kural:** Yerel bandı + sekme adında `[Canlı]`/`[Yerel]`; birleştirme onayında asıl soru açılır listeden seçilir; `.m16-liste` satırı sarar, seçici alt satıra iner.

## H170–H185 — Sayfa denetimi dördüncü tur, yönetim paneli orta bulguları (2026-10-28)
- **H170 Kurul çipi "1 66":** etiket yalın rakam + aynı boyutta sayı → "Kurul N" + soluk sayı rozeti.
- **H171 Yüklenirken "0 kayıt":** sayaç yükleme durumuna bakmıyordu → "Yükleniyor…", seçeneksiz süzgeç satırı gizli.
- **H172 Açıklamalarda dosya yolu/jargon:** yönetici diline çevrildi; yol küçük ikincil etiket.
- **H173 Son yönetici işlemleri:** okuma kayıtlarıyla doluyordu → yalnız yazma (`sonDenetimler(8, true)` + istemci süzgeci).
- **H174 Bellek "1462 / 234 MB":** RSS ve yığın etiketsiz yan yanaydı → ayrı satırlar, `yiginToplamMb` eklendi.
- **H175 Gelen kartları:** sıfır kartlar gizli, hepsi sıfırsa "Bekleyen iş yok".
- **H176** Çıkmış "Cevap" başlığı 56→72 px. **H177** Birleşenler "Ayır" yazılı onay + Geri al. **H178** Taslaklar kendi çekmecesini açar, dönüşte süzgeç korunur.
- **H179 Askı gerekçesi `window.prompt`:** kit onay penceresine gerekçe alanı (`gerekceIste`, ≥3 karakter); Kişi 360, Erişim, Kişiler.
- **H180** Oyun odası "Kapat" satır çekmecesinde. **H181** Erişim, DB satır yazımı, duyuru onaylarında hedef sunucu (`yazimHedefi()`); duyuru yayınlama artık onaylı.
- **H182 Betik tehlikesi:** ad regex'i yerine izin listesi: yalnız bilinen salt okunur betikler onaysız, gerisi yazılı onay.
- **H183 Yedek içe aktarma:** ezmeden önce `/api/admin/db/export` ile mevcut havuz indirilir, başarısızsa iptal (kalıcı çözüm: sunucu import ucu kendi yedeğini almalı — açık).
- **H184 Çöp kutusu:** tek seçenekli "Tür" süzgeci gizleniyordu → gösterilir; Silinme süzgeci (bugün/7/30 gün/eski).
- **H185 Site › Menü:** erişimi kapalı sayfada anahtar kilitli + açıklamalı; menüden gizleme onaylı, her yazım Geri al.

## H250–H268 — Sayfa denetimi beşinci tur, yönetim paneli kalan bulgular (2026-10-28)
- Genel bakış kart adları ve hedefleri (topluluk şikâyeti, istemci hatası → Gelen süzgeci), yük renk eşiği, sürüm etiketi (H250–H253).
- Bağlantılar: Ctrl/orta tık yeni sekme (H254), `manageAdres` (H255), Çıkmış ve Birleşenler içi bağlantılar panel içi gezinme (H256, H266), Branşlar → derslere (H265).
- Metin/ad netliği: Ham defter dışa aktarım (H257), Faz 14 → "Çıkmış inceleme (Faz 14)" (H259), Kamplar → "Kamp tüyoları" (H260), benzer menü adları ayrıştırıldı (H261), Sözlük silinemez sekme açıklaması (H267), katalog form alanlarına Türkçe etiket (H268).
- Onaylarda hedef sunucu: bakım ve LLM işleri (H262, H263; kural 20 davranışı değişmedi). Faz 14'te kimliksiz satır bildirimi (H258).
- **H264 Boş tablo:** yalnız "Kayıt yok" diyordu → süzgeç mi kaynak mı boş söylenir, yerelde Canlı önerisi.
- Kapsam dışı bırakılan öneriler: menünün baştan düzenlenmesi, görünürlüğün tek yerde toplanması, Çıkmış/şikâyet toplu işlemleri, kirli kurul etiketlerinin veri temizliği, üç "bugün" sayfasının birleşmesi, oynatıcı araç çubuğu yeniden tasarımı, çıkmış listesinde sayfalama.

## H290–H295 — Yönetimde iş akışı uzundu: Gelen yalnız yönlendiriyordu, toplu işlem yoktu (2026-10-28, sayfa denetimi)
- **Belirti:** Gelen'deki her iş için başka sayfaya gidip dönmek gerekiyordu (soru şikâyeti en az 4 tıklama); soru şikâyetleri ve çıkmışlarda toplu işlem yoktu; gizlenen topluluk mesajı Gelen'de kalıyordu; istemci hatası için hiç işlem yoktu.
- **Kök neden:** Satır yalnız `git(hedef)` çağırıyordu; Gelen 15 sn önbelleği işlem uçlarınca temizlenmiyordu; Gelen sorgusu `silindi`'ye bakmıyordu.
- **Çözüm/kural:** Gelen'de satır ve çekmece işlemleri (Çözüldü / Yok say / Mesajı gizle / Kapat + iç not / Görüldü), aynı türde toplu işlem; `gelenOnbellekSil()` işlem uçlarında; yeni uç `POST /api/admin/gelen/hata/goruldu` (işaret `data/istemci_hata_goruldu.json`, hata yinelenirse geri düşer); VeriTablosu `dusur(t)` ile işlenen satır süzgeç/sayfa korunarak düşer. Soru şikâyetlerinde çekmeceden Çözüldü + toplu; çıkmışlarda toplu Gizle/Göster (onay + hedef + 8 sn Geri al). Not: "Yok say" şikâyeti `resolved` yapar (ayrı red durumu yok).

## H296 — Gelen'de tek satır işlemleri onaysız ve geri alınamazdı (2026-10-28, ajan sınaması)
- **Belirti:** Gelen'de "Çözüldü"/"Yok say"/"Mesajı gizle"/"Kapat" tek tıkla canlıya yazılıyor, yanlış tık geri alınamıyordu; Soru şikâyetlerinde tek çözme de geri alınamıyordu.
- **Kök neden:** H290'da onay yalnız toplu işleme konmuştu; işlemlerin tersi tanımlanmamıştı.
- **Çözüm/kural:** Tersi olan işlemler (soru şikâyeti → yeniden aç, mesaj gizle → göster, geri bildirim kapat → aç) 8 sn "Geri al" verir, geri alınan satır listeye döner; tersi olmayan (topluluk şikâyetini yok say: şikâyet kayıtları silinir) tek işlem de "geri alınamaz" diyen onay ister. Yerelde tıklanarak sınandı (Çözüldü → Geri al, çıkmış toplu Gizle → Geri al; veri eski hâline döndü).
- **Sınama notu:** Sınama betiği satır düğmesini sayfa genelinde ararsa yanlış satıra basar; düğme her zaman ilgili satırın/çekmecenin içinde aranır.

## H310–H314 (yönetim) — 69 sayfalık menüde bulunabilirlik (2026-10-28, sayfa denetimi)
- **Çözüm:** Sabitlenenler (`m16_sabit`), Son kullanılanlar (`m16_son`, 5), ilk açılışta yalnız Genel + etkin grup açık (`m16_kapali_grup` yoksa), menüde ara (etiket + `anahtar`, Türkçe harf duyarsız, Esc temizler), telefonda ≥32 px hedefler. Menü yapısı ve adresler değişmedi.

## H320–H329 — Görünürlük beş ayrı yerden düzenleniyordu (2026-10-28, sayfa denetimi; kullanıcı isteği)
- **Belirti:** Site › Görünürlük, Site › Menü, Kurullar, Dersler ayrıntısı, Sesli dersler, Önem ve çözücü, İçerik paketleri ve Desteler aynı `site_ayar.gorunurluk`/`sayfalar`/`menu` verisini satır içi seçicilerle yazıyordu; hangisinin geçerli olduğu ve nereden değiştiği belirsizdi.
- **Kök neden:** Paylaşılan `GorunurlukSecici` her sayfaya düzenleme yetkisiyle gömülmüştü; tek doğruluk yeri tanımlı değildi.
- **Çözüm/kural:** Görünürlük YALNIZ Site › Görünürlük'te yazılır: "Sayfalar" (öğrenci sayfaları + menü) ve "İçerik" (kurul, ders, sesli, deste, paket, önem/asistan/çözücü; yeni uç `GET /api/admin/gorunurluk/icerik`, sayfalı, süzgeçli, katalogda olmayan ayar `sahipsiz`). Diğer sayfalarda `GorunurlukBaglantisi` (rozet + "Değiştir" → `site/gorunurluk?sekme=icerik&q=<anahtar>`). `site/menu` → Görünürlük. Gizleme onay + hedef, her yazım 8 sn Geri al, toplu değiştirme. Yerelde tıklanarak sınandı (tek + toplu, geri al sonrası ayar boş).

## H431 — Kişi 360° › Etkinlik sekmesi hep "Olay yok" gösteriyordu (2026-10-28, kullanıcı bildirdi)
- **Belirti:** Yönetim › Kişiler › kişi › Etkinlik sekmesi her öğrencide boş.
- **Kök neden:** `/api/admin/people/:key/olaylar` yalnız `user_events` okuyordu (38 kayıt, hepsi uid'siz "report"); sayfa ziyaretleri ise `user_data.data.kv.medsoru_etkinlik_v1.v` (JSON metni) içinde, sekme oraya bakmıyordu.
- **Çözüm/kural:** Uç nokta ilk sayfada ziyaretleri `kind:'page'` olay olarak birleştirir (Tümü 100, Sayfa süzgeci 300). Yeni bir olay kaynağı eklenince yönetim ekranının o kaynağı gerçekten okuduğu canlı veriyle doğrulanır.

