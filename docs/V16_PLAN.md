# v16 — koda geçiş planı

Kaynak: Design tuvali **MeDSor v16** (https://claude.ai/artifact/9a2DjyipmJqsAhFFVACVN6) — 36 ekran, 8 tema,
ortak katman `project/v16.css` (token + bileşen + SVG ikon). Tasarım sistemi v15'in renkleri korunur; v16 yapıyı,
yoğunluğu, ikonları ve bileşenleri yeniler.

## Kurallar
- **Eski dosyalar silinmez.** v15 bileşenleri ve `styles/v15/*` yerinde kalır; v16 ayrı katmandır.
- **İlk etapta yalnız yönetici:** v16 yalnız `isAdmin` olan oturumda ve Ayarlar › Tasarım'da "v16 (deneme)" seçiliyken
  açılır. Herkese açma ayrı karar (son aşama), `DESIGN_CHOICES`'a eklenerek yapılır.
- Her aşama ayrı onaydır (v15 planındaki gibi); aşama bitince `npm run lint` + `npx vite build` + canlı tarayıcı
  sınaması (telefon 390, tablet 820, PC 1366; açık + koyu tema).
- Renk yalnız `--color-*` palet kaydından; yeni renk adı uydurulmaz. İkon yalnız `components/v16/Ikon.tsx` (çizgi SVG,
  1.8 kalınlık); unicode/emoji ikon yok.

## Altyapı (aşama 1)
- `utils/appearance.ts`: `Appearance.v16?: boolean`; kök `data-v16="on"` yalnız `v15 && v16 && yönetici` iken yazılır
  (`siteAyar.yoneticiAyarla` ile bağlanır). `index.html` erken betiği v16'yı **yazmaz** (yönetici bilgisi yok, FOUC kabul).
- `styles/v16/tokens.css`: `:root[data-v16='on']` altında `--v16-*` ölçüleri ve v15 değişkenlerinin v16 değerleri
  (yoğunluk: üst bar 56, oynatıcı 8/10, alt sekme 4/8, kart sınırı line-soft + sh-1).
- `styles/v16/bilesen.css`: v16.css'teki bileşenlerin (`.chip .tag .btn .seg .list .li .opt .toast .sheet`) sitedeki
  `.v15-*` karşılıklarına uyarlaması. **Ders:** taban öğe kuralları `:where()` içinde yazılır (tuvalde `.scr button`
  sınıf kurallarını ezdi — iç boşluk, yazı boyutu ve renk kayboldu).
- `components/v16/Ikon.tsx`: 50 ikon; `components/v16/lucideV16.ts` + `vite.config.ts › v16LucideEklentisi` uygulamadaki tüm `lucide-react` içe aktarmalarını buraya yönlendirir (57 lucide adı eşlenir, gerisi aynen). Eşlenmeyenler bilinçli: Flag, Layers, Sparkles, dolu daireler, Loader2. `bilesen.css` yazılmadı.

## Aşamalar
| # | Sayfa / grup | Tuval ekranları | Durum |
|---|---|---|---|
| 1 | Altyapı + yönetici anahtarı + kabuk (üst bar, alt sekme, PC yan menü) | Kabuk, Bugün | Kuruldu (2026-11-25): v16.ts, V16Secici, styles/v16/temel.css |
| 2 | **Sesli ders** (telefon/tablet/PC, çıkmış, terim, seçim, görünüm, yükleniyor, ara soru, bölüm sonu, mini oynatıcı) | Main, Sesli* | Kuruldu (2026-11-25): PDF sayfa/sürekli kipi, köşe etiketi, küçültülebilir soru kartı (styles/v16/sesli.css) |
| 3 | Ders çalış merkezi, ders ayrıntısı, özet, Öğren, Notlarım, sözlük | Dersler, DersDetay, Ozet, Ogren, Notlarim, Sozluk | Kısmen (2026-11-25): merkez araç kartları telefonda tek gruplu satır listesi (sayfalar.css); ders özeti gruplu liste; ders ayrıntısı, Notlarım (boş durum), sözlük (ayraçlı düz liste) tarayıcıda uygun bulundu, dokunulmadı; Öğren askıda (kural 22) |
| 4 | Soru çöz, Yanlışlarım, deneme sonucu | Soru, Yanlislarim, DenemeSonuc | Kuruldu (2026-11-25): çözücü satır sarma, üst bar (styles/v16/soru.css) |
| 5 | Sınava hazırlan, program + kronometre | Sinav, Program | Kısmen: Kamplar kartları gruplu liste, 4 sekme kaydırmasız sığar; program: branş rengi 4 px şerit yerine nokta |
| 6 | Başvuru, ayarlar, profil, bildirimler, giriş/kayıt | Basvuru, Ayarlar, Profil, Bildirimler, Giris, Kayit | Kısmen: Başvuru gruplu liste; Ayarlar ikonları sabit hex yerine nötr palet kutusu, başlıklar normal yazı; giriş/kayıt test oturumunda görülemedi (oturum açık) |
| 7 | Oyunlar, KMB, Hücrem, istatistik, topluluk | Oyunlar, KMB, Hucrem, Istatistik, Topluluk | Genel katman (temel.css: sınır/gölge, taşma, sekme sarma) + taşma taraması 0; tuvaldeki yapısal yeniden kurulum yapılmadı |
| 8 | Katmanlar: menü, toast, diyalog, çekmece, boş/yükleniyor durumları | Katmanlar | Kuruldu: ortak alt çekmece (ui/Sheet.tsx) ve çıkmış/örnek soru kartı küçültülür (perde kalkar, sekme çubuğu üstünde hap). Kutlama ve ortalı diyaloglar (Dialog.tsx) küçültülmez — kısa onay/kapat katmanları |
| 9 | Tüm sayfa taraması (tuvalde olmayan v15 sayfaları v16 bileşenleriyle) + herkese açma kararı | — | Taşma taraması 16 rota × 3 boyut = 0 (2026-11-25); kalan: tema tek tek göz, herkese açma kararı |

## Sınama
Test oturumu yönetici değildir; tarayıcıda `window.__v16Sinama()` o sekmede v16'yı açar (yalnız görsel katman, yenileyince kapanır).
