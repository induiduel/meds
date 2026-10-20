# v13 "Ada" — tam yeniden tasarım planı

Kullanıcı isteği (2026-10-20): tüm sayfalar, diyaloglar, toast'lar, açılır/kapanır pencereler, menüler, tam ekranlar,
kaplar ve bütün arayüz bileşenleri yeniden düzenlensin; sade, kompakt, anlaşılır, erişilebilir; telefon/tablet önce;
kayma/taşma/ekran altına kalma/okunmayan yazı yok; tam genişlik şerit yok; renkler sakin, tema geçişi sorunsuz.
v12 korunur, v13 isteğe bağlıdır (açılışta sorulur).

## Ortak ilkeler (her aşamanın kabul ölçütü)
1. **Ada:** her yüzey kenardan ayrık, yuvarlak (14–20 px), 1 px çizgi; gölge yalnız yüzen katmanlarda.
2. **Taşma 0:** 320 / 375 / 390 / 768 / 820 / 1024 / 1180 / 1440 / 1920 px'te yatay taşma yok; katmanlar görünür alana
   (`--vvh`, güvenli alan) sığar, sığmayan içerik kendi içinde kayar.
3. **Okunurluk:** gövde ≥ 14 px, ikincil ≥ 12 px; metin rengi yalnız `--color-ink*`; renkli zemin yalnız durum için.
4. **Erişilebilirlik:** dokunma ≥ 40 px (kaba işaretçi), görünür odak halkası, her katmanda Escape + odak geri dönüşü,
   `role`/`aria-*` doğru, hareket azaltma tercihine uyum.
5. **Tek vurgu rengi:** ders/branş renkleri yalnız küçük nokta/çizgi; geniş renkli zemin yok.
6. **Tema:** yalnız palet token'ları (`utils/palettes.ts`); açık/sarı/koyu × 4 palette elle bakılır.

## Aşamalar ve durum
| # | Kapsam | Durum |
|---|---|---|
| 0 | Seçim altyapısı (`appearance.v13`), açılış daveti, Ayarlar/Menü seçimi | ✅ |
| 1 | Kabuk: kenar adası, başlık kapsülü, alt ada, Menü, tam ekran çıkışı | ✅ |
| 2 | Temel katman: taşma kalkanı, araç çubuğu kapsülü, başlık tekrarı, çevrimdışı adası | ✅ |
| 3 | **Ortak katmanlar:** Sheet, Confirm, Toast, Tooltip, ActionMenu, AccountMenu, SearchPalette, Bildirim geçmişi, Tailwind `fixed inset-0` modalları (39 dosya), açılır listeler | ✅ ilk tur (styles/v13/components.css) |
| 4 | **Tam ekranlar:** Öğren ders oynatıcı (`ls-root`), okuyucular (`r12-root`), sesli ders (`cd-ders`), soru çözücü / alternatif çözücü (`sc`), asistan (`pa`), test (`p12`), kart oturumu | ✅ ilk tur: üst/alt çubuklar yüzen ada (styles/v13/fullscreen.css), alternatif çözücü taşması düzeltildi |
| 4b | **Yüzen alt kartlar:** alt oynatıcı/çubuklar içerikten alan kesmez; içerik altlarından kayar, kayan alana kart yüksekliği kadar iç boşluk (sesli ders `--cd-ortu`, çözücüler `.sc-alt`, ders oynatıcı `.lv-bottombar`); sesli ders oynatıcısı v13 alt adasının üstüne oturur | ✅ |
| 5 | Ana sayfalar: Soru ekle, Bugün, Öğren kitaplığı, Çıkmış, Havuz, Test, Kartlar | ✅ Bugün ✅ (gün planı), Öğren ✅ (dal şeridi, yüzde halkası, ad kırpılmaz), Çıkmış ✅ (iki satır araç, tek satır künye, kaydırılabilir diğer yıllar), Soru ekle hizası ✅, Havuz/Test/Kartlar sütun hizası + sakin kaynak kartları + tek satır sekmeler ✅ |
| 6 | Okuma sayfaları: Notlar, Özetler, Sesli ders listesi, Sözlük, Hastalıklar, Sağlık Bakanlığı, Kazanımlar | ✅ hizalama + sesli ders başı tek satır; Notlar/Özetler/Ses kayıtları geniş ekranda kart ızgarası; Sözlük/Hastalıklar/Kazanımlar iki ada (liste yapışkan, ayrıntı okunur genişlik); Sağlık blokları ada (`styles/v13/wide.css`) |
| 7 | Sınav sayfaları: Sınav çalışması, En önemliler, Spotlar, Check Up (patoloji/genetik), Olası sorular, Örnek sorular, Geçmiş kurullar | ✅ sütun hizası (dar ortalı kutular kalktı), cx-dock şeridi ada |
| 8 | Kişisel/topluluk: Profil ve ayarlar, İstatistik, Bitirdiklerim, Çevrimdışı, Çalışma masam, Sıralama, Harita, Müzik, Güncellemeler | ✅ sütun hizası, harita sakin |
| 9 | Giriş/kayıt, tanıtım turu, giriş uyarısı, hata/boş/yükleniyor durumları | ✅ temiz ziyaretçiyle 390/1440 denetlendi (giriş uyarısı, 5 adımlı tanıtım, boş durumlar); taşma yok |
| 10 | Yönetim konsolu (`/manage` tüm bölümler) | ✅ `styles/v13/manage.css`: menü yüzen ada, üst çubuk tek satır kapsül, telefonda 2 satır araç; 22 bölüm × 390/1440 taşma 0 |
| 11 | Son tarama: tüm rotalar × 9 boyut × 3 tema; dokunma/adsız düğme/kontrast raporu sıfır | ✅ 450 görünüm taşma 0, adsız düğme 0; kontrast 36 sayfa×tema: tek bulgu (koyu temada spot istatistik kartı, tanımsız --color-surface → beyaz zemin) düzeltildi; küçük hedef bulguları ::after genişletmeli (aracın bilinen yanlış alarmı) |

Her aşama sonunda: `npx tsc --noEmit`, `npx vite build`, başsız Chrome taraması (`scripts/perf/sayfa_tarama.mjs`, SEED v13),
gerekiyorsa `scripts/perf/yazma_olcum.mjs` (CSS başarımı). v12 dosyaları değişmez; v13 kuralları `:root[data-v13='on']`
kapsamında ya da `a.v13` dalında.

## Durum notu (2026-10-20)
Aşama 5–10 için ilk tur yapıldı: 30 rota telefon (390), 18 rota tablet (820) + masaüstü (1280), açık/sarı/koyu temada
yatay taşma 0; sayfa içi başlık tekrarları kaldırıldı. Sayfa gövdeleri hâlâ v12 bileşenleri + v13 katmanı. Sıradaki tur:
her sayfanın gövdesini TSX düzeyinde v13 anatomisine taşımak (Bugün, Öğren, Çıkmış ile başlayarak), Soru haritası renkleri,
Yönetim konsolu (yönetici oturumuyla), dokunma hedefi/kontrast raporunun sıfırlanması.

## Hizalama kuralı (2026-10-20, kullanıcı bildirimi)
Başlık kapsülü, kurul şeridi ve sayfa içeriği aynı sütun kutusunu paylaşır: `.a13-top` = `.sh-main` ile aynı en büyük
genişlik ve yan boşluk; sayfa içi tam genişlik şeritler (`.ks`) sütunu doldurur; içerik kutuları sütunun sol kenarından başlar.
Yeni sayfada bu kenar dışına taşan ya da içeride kalan kutu hata sayılır.

## Bulunan ve düzeltilen hatalar
- Genetik Check Up: yapışkan aşama listesi alttaki ders kartlarıyla aynı ızgaradaydı, kaydırınca kartların üstüne biniyordu (tüm tasarımlar) → kartlar ızgara dışına.
- Sesli ders: oynatıcı v13 telefonda alt adanın üstüne biniyordu (gezinme kapanıyordu) → ada ölçülür, oynatıcı üstüne oturur.
- Soru haritası: 100 turuncu karo → beyaz karo + durum noktası.

- Hizalama ölçümü: 30 rota × 1440/390, içerik kutusu kenarı − kapsül kenarı = 0 (Havuz sağ sütunu kutusuz, 10 px). Öğren yüzde halkası geniş ekranda elipsti → daire.
- Açık: Yönetim konsolu (yönetici oturumu gerekir), Test/deneme kurucu kendi tam ekranında.

- Sesli ders oynatıcısı: YouTube tarzı bölüm çubuğu (parçalı, üstüne gelince bölüm adı + zaman, Shift+ok bölüm atlar).
