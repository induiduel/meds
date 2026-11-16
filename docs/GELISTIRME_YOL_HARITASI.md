# Geliştirme Yol Haritası — veri, site sağlığı, içerik hattı, ses (2026-11-16)

> Dört hattın tek sıralı planı. Her madde ölçümle gerekçelidir; ayrıntı ve kanıt ilgili belgede:
> veri → `docs/VERI_MODELI.md`, kök nedenler → `docs/HANTALLIK_KOK_NEDENLERI.md`, ses kuralları → `docs/GPU_KULLANIM.md`.
> Durum: ✅ yapıldı (2026-11-16) · ⏳ sıradaki · 🙋 kullanıcı kararı gerekir.

## A. Veri katmanı (ayrıntı `VERI_MODELI.md` §5)

| # | İş | Durum |
|---|---|---|
| A1 | Sorgu aracı `veri.py`, günlük, yazım frenleri, doğrulamalı arşiv, kapı D10 | ✅ (onem 761) |
| A2 | Çıkmış soru `src/data` aynası kaldırıldı; okuyucular `data/` + `kok.CIKMIS` | ✅ |
| A3 | RAG parça deposu JSONL (`ragParcaDeposu.ts`, okuma belleği 872 → 384 MB) | ✅ |
| A4 | Özet kataloğu tek kaynak (`src/data` + katman); `data/` kopyası Oracle karşılaştırmasından sonra arşivlenir. `summaries/kurul*.json` ayrı temsil (293 kayıtta farklı) — birleştirme ⏳ | ✅ kısmi |
| A5 | Ders manifesti (`manifest.py uret/goster/denetle/fark` → `ders_bilgi/<key>/katman_manifest.json`; 65 Kurul 2 dersi) | ✅ araç; koşucu/dağıtım bağlaması ⏳ |
| A6 | Deste monoliti → deste başına dosya (içerik katmanı + Oracle eşitleme + derleme eklentisi birlikte) | ⏳ ayrı tur: çift yazım → 0 fark kapısı → okuma parçaya |
| A7 | Kazanım soru parçası (31,9 MB tek tembel parça) kurul/ders başına bölünür | ⏳ |
| A8 | ~7 GB alan: `meds_temp` iş artıkları, Supabase öncesi yedek, varsayılan olmayan ses varyantları | 🙋 |

## B. Site sağlığı: hata, performans, bellek, kod şişmesi

Ölçüm (2026-11-16): `meds-web` tepe 2,2 GB / takas 1,3 GB; ilk yükleme 2,36 MB ham / 647 KB gzip, tek CSS 733 KB;
süre/bellek telemetrisi ve web-vitals yok; yerel istemci hata dosyası canlıyı yansıtmıyor; 18 dosya > 1500 satır.

| # | İş | Etki | Durum |
|---|---|---|---|
| B1 | `autoErrorRepairEngine` / `questionCrossAuditService` çıkmış dosyasını önbelleği atlayarak yazıyor (yarış, veri kaybı riski) → sunucunun okuma/kaydetme yolu enjekte edilir | yüksek | ✅ |
| B2 | `pastListCache` ikinci tam kopya + dev JSON metni → yalnız serileştirilmiş + gzip tutulur | yüksek | ✅ |
| B3 | Sunucu telemetrisi: istek süresi histogramı, > 1 sn istek kaydı, 5 dk'da bir bellek örneği → `data/gunluk/` | orta | ✅ |
| B4 | İstemci web-vitals (LCP/CLS/INP/TTFB) + canlı istemci hatalarının yerelden okunması | orta | ✅ |
| B5 | Sayfa stilleri rota parçalarına: yalnız −%4 (751 → 720 KB); büyük sayfa stilleri zaten ayrıymış. Asıl kazanç için kabuğa statik giren bileşenler (PoolView, AsistanPanel, CdSesliEk) tembel yüklenmeli | orta | ✅ kısmi, kalan ⏳ |
| B6 | Tavansız önbelleklere LRU, `unref` eksik zamanlayıcılar, SSE istemci tavanı | düşük–orta | ✅ |
| B7 | Dev dosyaları bölme: `api.ts`, `AdminPanelModal.tsx`, `App.tsx`, `server.ts` rota grupları | bakım | ⏳ dosya başına ayrı iş + sayfa taraması |
| B8 | Klasik v10 dalı ve `*-v10.css` kaldırma | düşük | 🙋 (kullanım verisine göre) |

## C. İçerik üretim hattı: daha az token, daha yüksek kalite

Ölçüm (k2-28): ilk geçiş girdisi ≈ 175 bin kelime (≈ 280 bin token); kural dosyaları toplam 67 bin kelime, 1171 madde
başlığının yalnız 343'ü benzersiz; `baglam/kaynak.md` 8,5 bin kelime ve 3 aşamada bütün okunuyor; düzeltme turu tüm
dosyayı baştan yazdırıyor; denetçi her şeyi okuyor ve yazarla aynı model ailesinde.

| # | İş | Beklenen kazanç (tahmin) | Durum |
|---|---|---|---|
| C1 | Kural seçici: madde → tek aşama, kapısı olan madde tek satır, `--ozet` (en sık 5–7 hata ≤ 300 kelime) | aşama kuralı −%40–50 | ✅ |
| C2 | Bağlam dilimleri: aşama yalnız kendi dilimini okur | önem/çıkmış 8,5k → 2–4k kelime | ✅ |
| C3 | Önbellek dostu paket sırası (sabit önek → değişken girdi) + girdi karmalı önbellek anahtarı | tekrar turunda girdi maliyeti ↓ | ✅ |
| C4 | Denetçi gerçekten ayrı model ailesinde; kısa işler hızlı modelde | kalite ↑ (kural 31) | ✅ |
| C5 | Kimlik bazlı yama (`MEDS_HAT_YAMA=1`) ve dar denetim (`MEDS_HAT_DAR_DENETIM=1`) | düzeltme turu tüm dosya → %5–15 | ✅ kod; ilk gerçek derste doğrulanınca varsayılan olur |
| C6 | Hoca dökümünü (360 KB) slayt hizasıyla kırpma | değerlendirmede −50–70 bin token | ⏳ |
| C7 | Atom envanteri, kimlik/numara, şema iskeleti betikle; model yalnız alan doldurur | çıktı −%20 | ⏳ |
| C8 | Otomatik yol (`otomasyon/llm/gorevler`) da `baglam/` dilimlerini okur (iki yol teke) | çift bakım biter | ⏳ |
| C9 | Aşama başına bir altın örnek (elle seçilir) | yeniden yazım −1 tur | 🙋 örnek seçimi |
| C10 | Tek "ders anlama" çağrısından önem/çözücü/terim türetme | kaynak okuma −%70 | ⏳ tasarım |

C1–C5 LLM çağrısı olmadan kodlandı; gerçek etkileri ilk elle koşulan derste ölçülür (kural 20: üretim yalnız kullanıcı komutuyla).

## D. Ses üretimi

Ölçüm: 12 ayrı ses girişi, 4 `seslendir` kopyası, okunuş 9 yerde; çözücü/asistan/ek modül yollarında terim okunuşu
uygulanmıyor; ses kalite kapısı yok (sesli dersler arası 9 dB fark); aktarımda doğrulama yok; 89.711 klip kayıt–disk tutarlı.

| # | İş | Durum |
|---|---|---|
| D1 | Ortak okunuş girişi `ses_ortak/ses_metin.py` (yol veriden seçilir, sessiz eski yola düşüş yok) | ✅ |
| D2 | Ortak klip kütüphanesi `ses_ortak/ses_klip.py`; global ayar ezme biter. Mevcut klip karmaları DEĞİŞMEZ | ✅ |
| D3 | Okunuş farkı raporu: 101.970 klipten 17.225'inin okunuşu değişir (`meds_temp/ses_ortak/okunus_farki.jsonl`); kalite kapısının bulduğu 16 bozuk Öğren klibi | ✅ rapor; yeniden üretim 🙋 (GPU, önce 10 kliplik dinleme sınaması) |
| D4 | Ses kalite kapısı `ses_ortak/ses_kapisi.py` (bozuk/yarım/sessiz klip, düzey, kırpılma, sessizlik, kayıt↔disk) | ✅ |
| D5 | Aktarım doğrulaması (yerel ↔ Oracle boyut), tam MP3 yüklemesinde 3 deneme | ✅ |
| D6 | GPU ses işlerinde tek kilit | ✅ |
| D7 | CPU'da EMA çalıştıran betikler: `patoloji_cozucu/ses_kuyruk.sh`, `cikmis_paket/{ek,asistan,sik}_uygula.sh`, `not_ses.sh` (kural 10 ile çelişir; `meds-ema-yerel` zaten devre dışı) | 🙋 |
| D8 | ASR geri-dökümüyle yanlış okunan terim / atlama denetimi | ⏳ (GPU gerekir) |
| D9 | Opus 24k'ya geçiş (≈ 6,5 GB) ve PCM önbelleğinin FLAC'a çevrilmesi (≈ 1,6 GB) | 🙋 (iOS uyumu + zaman ölçeği riski) |

## Sıra ve kapılar

1. Her dalga: ajanlar ayrık dosya kümelerinde → `npm run lint` 0 → `yapi_koruma.py` 0 HATA → `npx vite build` → `meds-web` yeniden başlatma + sağlık.
2. Dağıtım yalnız `dagit.sh`, onem +1; kod ve veri biçimi değişiklikleri aynı turda gider (RAG JSONL).
3. Bayrak arkasındaki davranışlar (C5) ve GPU isteyen işler (D3, D8) kullanıcı komutu olmadan açılmaz/başlamaz.
