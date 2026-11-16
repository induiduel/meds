# V15 Tema / Renk Denetimi (2026-10-27)

Yalnız okuma denetimi; kod değiştirilmedi. Tarayıcı doğrulaması: 5175, `data-v15="on"`, koyu tema (`theme-dark`).

## Kritik bulgu (tarayıcıda ölçüldü)

- Tailwind `white` = `--color-white` = palet **yüzeyi**. Koyu temada `--color-white: #151E2C`.
  - `text-white` → **rgb(21,30,44)** (koyu lacivert). Koyu zemin/görsel/overlay üstündeki beyaz yazı kaybolur.
    (`bg-accent` ile birlikte kullanılınca başka bir kural koyu-yazı veriyor: rgb(4,20,26) — o durum okunur.)
  - `bg-white` → yüzey (doğru davranış, sorun değil).
  - `bg-slate-900` + `text-slate-300` → slate skalası koyu temada ters çevrildiği için açık zemin + koyu yazı olur
    (index.css ~106–125). "Hep koyu" tasarlanmış paneller koyu temada açık görünür.
  - `border-indigo-500` gibi skalası ters çevrilmeyen renkler palette uymaz (oklch indigo).
- Önerilen genel kural: beyaz yazı için `text-on-accent` / `var(--color-on-solid)`; hep-koyu panel için
  `bg-ink-surface` + `text-on-solid`; `text-white` yalnız `bg-accent`/`bg-ok`/`bg-bad` gibi dolu zeminlerde.

## 1. Spinner'lar / yükleme göstergeleri

Token kullanan, sorunsuz: `.bd-spin` (takip.css:156), `.cd-spin` (canli-ders.css:34), `.os-spin` (olasi-sorular.css:134),
`.pdv-spin` (pdfDoc.css:79), `.ui-skel` (appearance.css:~272), `.sr-skel`, `.on-iskelet`, TranscriptionsView.tsx:177
(`border-accent`). Lucide `RefreshCw/Loader2 animate-spin` sınıfsız olanlar `currentColor` alır (sorun yok).

| Öncelik | Yer | Mevcut | Öneri |
|---|---|---|---|
| Yüksek | src/index.css:419 `.ms-shimmer` (ui/Animations.tsx:131-132 iskelet satırları, ManageIntakeSection:465) | sabit `rgba(30,79,216,.10/.22)` mavi | `color-mix(in srgb, var(--color-accent) 10%/22%, transparent)` veya `.ui-skel` gradyanı (field→white) |
| Orta | src/styles/basarim.css:~220 (bs-don halkası) | `conic-gradient(#F97316,#FACC15,#22C55E)` | `var(--color-warn)`, `var(--color-accent)`, `var(--color-ok)` |
| Orta | src/styles/basarim.css:~404 | `repeating-conic-gradient(#6366F1,#EC4899)` | `var(--color-accent)` / `var(--color-brand)` |
| Düşük | src/styles/basarim.css:~312 `.bs-k-halka` | `color-mix(... #fff)` | `var(--color-white)` (koyuda parlama azalır) — ya da bilinçli, bırak |
| Düşük | src/styles/basarim.css:~319 `.bs-k.is-ust` altın | `#E5B000,#FFF3B0,#FFD60A` | kasıtlı madalya rengi; bırakılabilir |
| Düşük | components/AdminCustomRedactModal.tsx:473 | `animate-spin text-white` → koyuda koyu | `text-on-accent` |
| Düşük | AiQuestionOptimizerModal.tsx:477, AdminCustomRedactModal.tsx:327 | `text-ok-soft` (soluk, açık temada zor görünür) | `text-ok` |
| Düşük | components/system/system.css:127 `.up-btn.is-1` (güncelle düğmesi spinner'ı) | `var(--color-on-solid, #fff)` | sorun yok (on-solid palette tanımlı) |

## 2. Sabit renkler

### Öncelik yüksek (öğrenci ekranları)

| Yer | Mevcut | Öneri |
|---|---|---|
| components/learn/pathway/AnimatedPathwayPlayer.tsx (344 Tailwind renk sınıfı; en sık `border-slate-800`×27, `border-slate-200`×25, `text-slate-300`×14, `bg-slate-900`×9, `border-rose-500`×8) | hep-koyu tasarım; koyuda ters slate ile açık panel + karışık kontrast | `bg-ink-surface`, `text-on-solid`, `border-line`, `text-bad` vb.; ya da kök elemana açık "sabit koyu" kapsam |
| components/SlideReaderModal.tsx:77,88,105,114 | `text-white`, `bg-white/10`, `border-white/20`, `text-white/70` overlay üstünde → koyuda koyu yazı | `text-on-solid`, `bg-[color-mix(var(--color-on-solid)_10%,transparent)]` |
| components/learn/InteractiveDeckView.tsx:447,627,639 | `text-white` | zemin dolu vurgu ise `text-on-accent`; değilse `text-on-solid` |
| components/learn/InteractiveDeckView.tsx:610 | `bg-white/80` (cam) | `bg-[color-mix(in_srgb,var(--color-white)_80%,transparent)]` — çalışıyor, düşük |
| components/QuestionCard.tsx:590,637,677,797 | `text-white` | zemine göre `text-on-accent` / `text-on-solid` |
| components/BookletView.tsx:54 | `bg-teal-50 border-teal-300 text-teal-800` | `bg-accent-soft border-accent text-accent` (veya `clinic-soft/clinic`) |
| components/learn/pdf/pdfDoc.css:279-294 (`.pdv-sb-*` bilgi kutuları/tablo) | `#475569`, `#0f172a`, `#eef2ff`, `#c7d2fe`, `#cbd5e1`, `#1d4ed8` | PDF kâğıdı üstündeyse kasıtlı (kâğıt hep beyaz) — gece kipi `.dpv.is-night` (pdfDoc.css:150 `#1b1b1b`) açıkken koyu yazı koyu sayfada kalır → is-night için ayrı renk |

### Orta

| Yer | Mevcut | Öneri |
|---|---|---|
| components/learn/pdf/pdfDoc.css:202-236 canlı çizim okları | `#2563eb`, `#dc2626`, `#7c3aed`, `#d97706`, `#ea580c`, `#0284c7`, `#64748b` | PDF üstü anlam renkleri (akış/inhibe/dönüşüm); kasıtlı. Paletle uyum istenirse `--cz-akis: var(--color-accent)` vb. değişkenlere al |
| components/ui/OptionsEditor.tsx:87,139 | `text-white` | `text-on-accent` |
| components/KazanimSorulariView.tsx:478; TranscriptionsView.tsx:152,164,291; BookletView.tsx:78 | `text-white` | `text-on-accent` / `text-on-solid` |
| components/annotation/AnnotationToolbar.tsx (22), SlideDrawingCanvas.tsx (14), MechanismVideoModal.tsx (13) | Tailwind renk sınıfları | kalem renk örnekleri kasıtlı olabilir; araç çubuğu zemini/yazısı token'a |
| components/v15/navV15.ts:65 | Yönetim `tint: '#64748B'` | `var(--color-ink-3)` |
| src/styles/v15/sesli.css:122 | `color-mix(#0a1018 22%)` | `var(--color-ink-surface)` |
| src/styles/canli-ders-liste.css:210,212 | `var(--color-warn, #d97706)` yedekli | sorun yok |

### Düşük (yönetim / modallar)

DraftDeduplicationModal (24), SystemDiagnosticsModal (22), AiQuestionOptimizerModal (20), QuestionAiChatDrawer (18),
QuickAddHero (17), LocalAiChatView (17), TestCikmisView (14), NotebookLMSyncModal (14), DriveSaveModal (14),
AuthErrorModal (12), AiQuotaAlertModal (12), ErrorReportHistoryModal (11), EditMyQuestionModal (11).
Hepsinde aynı kalıp: `text-white` ve Tailwind renk skalası → token'a çevir.

`bg-white` kullanımı (QuestionCard, KazanimSorulariView, OptionsEditor, TranscriptionsView…) koyu temada yüzeye döner — **sorun değil**.

## 3. Tanımsız CSS değişkenleri (yedeksiz kullanılanlar)

Palette anahtarları (`on-solid`, `ok-tint`, `bad-text`, `ink-surface`…) JS ile tanımlanır; onlar sorun değil.
`--color-surface` artık styles/v15/tokens.css:10'da tanımlı (yalnız v15 altında).

| Öncelik | Değişken | Yer | Öneri |
|---|---|---|---|
| Yüksek | `--color-text`, `--color-text-sub` | src/styles/spot-istatistik.css:52,58,75,134,160,223 | `--color-ink`, `--color-ink-2` (şu an miras renge düşüyor) |
| Yüksek | `--color-good` | src/styles/canli-ders.css:1215,1219 (çıkmış soru doğru şık) | `--color-ok` — şu an doğru şık rengi/kenarı görünmüyor |
| Yüksek | `--color-danger` | src/styles/oncelikli.css:71,86 | `--color-bad` |
| Orta | `--color-bg`, `--color-border`, `--color-text-dim`, `--color-neutral-subtle` + sabit `#25D366`/`#ffffff` | components/settings/WhatsAppDailyDigestRow.tsx:133-368 | `--color-field`, `--color-line`, `--color-ink-3`, `--color-field` |
| Orta | `--color-surface` (v15 dışında tanımsız) | src/styles/baslangic.css:122, styles/v15/sozluk.css:6-7 | `--color-white` kullan (kök v15 olmasa da çalışsın) |
| Düşük | `--color-surface-2`, `--color-warning-soft` (yedek zinciri ikisi de tanımsız) | styles/v15/spot.css:27, genetik-kamp.css:329 | `--color-warn-soft` / `--color-field` |
| Düşük | `--color-bg-subtle`, `--color-line-strong`, `--color-muted`, `--color-ok-ink`, `--color-ok-text`, `--color-text-muted`, `--color-warn-ink`, `--danger`, `--ink*`, `--line`, `--muted`, `--accent*` | çeşitli (çoğu yedekli; tek tek kontrol) | `--color-line-2`, `--color-ink-3`, `--color-ok`, `--color-warn`, `--color-bad` |

## 4. Koyu tema sorunları (özet)

1. `text-white` = koyu yüzey (ölçüldü #151E2C) → overlay/görsel/koyu panel üstündeki beyaz yazılar kaybolur (Yüksek).
2. Ters çevrilen slate skalası "hep koyu" panelleri (AnimatedPathwayPlayer) açık yapar; ters çevrilmeyen renklerle
   (rose/indigo) karışınca kontrast bozulur (Yüksek).
3. `.ms-shimmer` sabit mavi iskelet; koyu temada ve mavi olmayan paletlerde uyumsuz (Yüksek) — kullanıcının
   "renk uyuşmazlığı olan spinner" şikâyetinin en olası kaynağı (ui/Animations.tsx iskeleti), başarım halkaları ikinci.
4. PDF gece kipi (`.dpv.is-night`) üstünde canlı çizim kutularının sabit koyu yazısı (#0f172a) okunmaz (Orta).
5. Tanımsız `--color-good/--color-danger/--color-text` → durum renkleri hiç görünmüyor (Yüksek, iki temada da).
