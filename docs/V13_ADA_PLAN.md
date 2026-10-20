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
| 5 | Ana sayfalar: Soru ekle, Bugün, Öğren kitaplığı, Çıkmış, Havuz, Test, Kartlar | ⏳ |
| 6 | Okuma sayfaları: Notlar, Özetler, Sesli ders listesi, Sözlük, Hastalıklar, Sağlık Bakanlığı, Kazanımlar | ⏳ |
| 7 | Sınav sayfaları: Sınav çalışması, En önemliler, Spotlar, Check Up (patoloji/genetik), Olası sorular, Örnek sorular, Geçmiş kurullar | ⏳ |
| 8 | Kişisel/topluluk: Profil ve ayarlar, İstatistik, Bitirdiklerim, Çevrimdışı, Çalışma masam, Sıralama, Harita, Müzik, Güncellemeler | ⏳ |
| 9 | Giriş/kayıt, tanıtım turu, giriş uyarısı, hata/boş/yükleniyor durumları | ⏳ |
| 10 | Yönetim konsolu (`/manage` tüm bölümler) | ⏳ |
| 11 | Son tarama: tüm rotalar × 9 boyut × 3 tema; dokunma/adsız düğme/kontrast raporu sıfır | ⏳ |

Her aşama sonunda: `npx tsc --noEmit`, `npx vite build`, başsız Chrome taraması (`scripts/perf/sayfa_tarama.mjs`, SEED v13),
gerekiyorsa `scripts/perf/yazma_olcum.mjs` (CSS başarımı). v12 dosyaları değişmez; v13 kuralları `:root[data-v13='on']`
kapsamında ya da `a.v13` dalında.

## Durum notu (2026-10-20)
Aşama 5–10 için ilk tur yapıldı: 30 rota telefon (390), 18 rota tablet (820) + masaüstü (1280), açık/sarı/koyu temada
yatay taşma 0; sayfa içi başlık tekrarları kaldırıldı. Sayfa gövdeleri hâlâ v12 bileşenleri + v13 katmanı. Sıradaki tur:
her sayfanın gövdesini TSX düzeyinde v13 anatomisine taşımak (Bugün, Öğren, Çıkmış ile başlayarak), Soru haritası renkleri,
Yönetim konsolu (yönetici oturumuyla), dokunma hedefi/kontrast raporunun sıfırlanması.
