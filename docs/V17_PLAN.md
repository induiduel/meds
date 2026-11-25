# v17 — Klinik editöryal (deneme, yalnız yönetici)

Tuval: https://claude.ai/artifact/CRx2hexkvDrnYoTb59dSSr (8 çalışma alanı, yorumlar işlendi).

## İlkeler
- Sıfırdan: v15/v16 dosyası kullanılmaz; kod `src/v17/`, stil yalnız `.k7` kökü altında (`v17.css`).
- H&E paleti (hematoksilen #33306B, eozin #F7D9E4, lam zemini #F5F7F7) + koyu/sepya; tema `html[data-mode]`'dan.
- Yazı: Fraunces (başlık), Instrument Sans (arayüz), Source Serif 4 (okuma); yalnız v17 açıkken yüklenir.
- Cihaz: telefon <700 yüzen şerit, tablet <1180 açılır ray, PC üst gezinme. Akılda kalan öge: bölüm şeridi.

## Bağlantı
- `bayrak.ts` (`medsor_v17_deneme`, `v17Yonetici`), `App.tsx` → `V17_ROTALAR` rotasında `Kok` tam ekran; v15 kabuğu `data-v17-ekran` ile gizli.
- PDF çekirdeği `CdPdfBolme` paylaşılır (kural 17/18 çizim/izleme aynen).

## Aşamalar
1. ✅ Kabuk + Bugün + sesli ders (onem 928).
2. Sesli soru çözücü (çözüm oynatıcısı dahil).
3. Kalan sayfalar; sonra herkese açılış.
