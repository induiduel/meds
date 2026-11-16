# src/components/ — React ekranları

- `v15/` güncel kabuk ve sayfalar (`ShellV15`, `DersDetayV15`, merkez sayfaları); `v12`–`v14` eski tasarımlar.
- `learn/` Öğren ekranı; `manage16/` yönetim konsolu; `merkez/` site haritası modeli (`merkezModel.ts`); `ui/` ortak parçalar.
- Özellik klasörleri: `cikmis/`, `spots/`, `kamp/`, `sonProva/`, `masa/` (oyunlar), `kmb/`, `pdf/` …

## Kurallar
- Ön yüz değişikliğinde sunucuyu yeniden başlatma; `npx vite build` yeter (3000 `dist/`'i sunar). Kapı: `npm run lint` 0 hata.
- API çağrısı `safeJsonFetch('/api/...')` ile (`src/services/api.ts`); çıplak `fetch('/api/...')` API adresi ayarını yok sayar.
- Kullanıcıya görünen metin Türkçe; renk palet tokenından (`palettes.ts`), sabit renk yok.
- Yeni sayfa/adres: `src/siteHaritasi.ts` + `merkez/merkezModel.ts`, kurallar `docs/SITE_HARITASI_KURALLARI.md`.
- Öğren (`learn/lesson/`) değişikliği öncesi `docs/OGREN_ETKILESIM_REHBERI.md`; sesli ders çizimi yalnız aktif cümlenin çizimi (AGENTS kural 18).
- Ayrıntı: `docs/hatalar/on_yuz_*.md`.
