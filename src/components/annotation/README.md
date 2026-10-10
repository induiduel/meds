# Not Üzerine Çizim (Annotation) Modülü

Ders notu (görsel / PDF sayfası / HTML) üzerine Goodnotes benzeri kalem, fosforlu kalem ve silgiyle
çizim. Çekirdek motor framework'süzdür (vanilla TS); React yalnızca ince bir kabuktur.

## Klasör yapısı

```
annotation/
├── types.ts                 Ortak tipler (Stroke, ToolSettings, EngineSnapshot, AnnotationDocument)
├── engine/
│   ├── AnnotationEngine.ts  Katmanlar, DPR ölçekleme, pointer olayları, palm rejection, zoom/pan, çizim döngüsü
│   ├── input.ts             Cihaz farkları: yan düğme/silgi ucu, basınç, coalesced olaylar
│   ├── renderer.ts          Basınçlı kalem, fosforlu (multiply), piksel silgi (destination-out)
│   ├── geometry.ts          Sınır kutusu, isabet testi (çizgi silgisi), basınç→kalınlık eğrisi
│   └── history.ts           Komut tabanlı Geri/İleri Al
├── AnnotationSurface.tsx    Katmanlı DOM + motoru bir kez kurar
├── AnnotationToolbar.tsx    Araç çubuğu
├── AnnotationWorkspace.tsx  Tam ekran çalışma alanı, kısayollar, localStorage kaydı
└── index.ts
```

## Katmanlar (alttan üste)

| Katman | Görev |
|---|---|
| `content` div | Ders notu. `docWidth` (1000) px genişlikte yerleşir, CSS `transform` ile ölçeklenir. |
| `highlightCanvas` | Fosforlu. CSS `mix-blend-mode: multiply` → siyah yazı fosforlunun altında okunur kalır. |
| `inkCanvas` | Kalem çizgileri. |
| `liveCanvas` | O an çizilen çizgi + silgi imleci (artımlı, hızlı). |

Canvas'lar **viewport boyutunda × `devicePixelRatio`** tutulur; zoom/pan `ctx.setTransform` ile
uygulanır. Böylece 8x yakınlaştırmada bile çizgi keskin kalır ve iOS'un canvas bellek sınırına
takılmaz. DPR değişimi (`matchMedia(resolution)`) ve boyut değişimi (`ResizeObserver`) izlenir.

Çizgiler **doküman koordinatında** (sayfa genişliği = 1000 birim) saklanır; ekran, zoom ve cihaz
değişse de notun aynı yerine oturur.

## Girdi politikası

| Girdi | Davranış |
|---|---|
| `pen` | Çizer. Yan düğme (`buttons & 2`) veya silgi ucu (`buttons & 32`, `button === 5`) basılıyken geçici silgi; bırakınca önceki araca döner (çizgi ortasında bile). |
| `mouse` | Sol tık çizer, sağ tık geçici silgi, orta tık kaydırır, tekerlek kaydırır, Ctrl/⌘+tekerlek ve trackpad pinch yakınlaştırır. |
| `touch` | **Asla çizmez.** 1 parmak kaydırır, 2 parmak yakınlaştırır, 2 parmakla kısa dokunuş geri alır. |

**Palm rejection:** kalem ekrandayken ya da son kalem olayından (hover dahil) 500 ms geçmeden
gelen dokunuşlar tamamen yok sayılır; kalem değdiği anda süren parmak hareketi iptal edilir.

## Cihaz uyumluluğu

- **iPad / Apple Pencil (Safari):** `pointerType === 'pen'` + basınç çalışır. `touch-action: none`
  tek başına yetmediği için `touchstart`/`touchmove` `preventDefault` edilir (büyüteç, Scribble ve
  sistem kaydırmasının çizgiyi `pointercancel` ile kesmesi önlenir). `gesture*` olayları engellenir.
  Apple Pencil'ın yan düğmesi yoktur; Pencil Pro sıkıştırma ve çift dokunma web'e açılmaz →
  silgi araç çubuğundan (veya `E`) seçilir. Hover destekli iPad'lerde silgi imleci havada görünür.
- **Samsung S-Pen (Chrome / Samsung Internet):** basınç + yan düğme (`buttons & 2`) → geçici silgi.
  Yan düğmenin açtığı `contextmenu` engellenir. Low-latency için `desynchronized` canvas.
- **Huawei M-Pen:** yan düğme `buttons & 2` veya `& 32` olarak gelir; ikisi de desteklenir.
  Kalemini `touch` bildiren eski WebView'lar için araç çubuğunda **"Parmakla çiz"** yedeği vardır
  (o oturumda hiç `pen` olayı görülmediyse gösterilir).
- Basınç ilk olayda 0 gelirse önceki değer / 0.5 kullanılır; titreme EMA ile yumuşatılır.
- 120–240 Hz kalem örnekleri `getCoalescedEvents()` ile toplanır.

## Araçlar ve geçmiş

- **Kalem:** basınçlı değişken kalınlık, orta nokta quadratic yumuşatma.
- **Fosforlu:** sabit kalınlık, tek yol (kendi üstüne binince koyulaşmaz), katman içi multiply.
- **Silgi:** *Çizgi silgisi* dokunduğu çizgiyi bütünüyle kaldırır; *Piksel silgisi* bir
  `erase` çizgisi olarak saklanır ve yeniden çizimde `destination-out` ile sırasıyla uygulanır.
- **Geri/İleri Al:** komut tabanlı (`add` / `remove`), 300 adım. Piksel verisi saklanmaz.

## Kullanım

```tsx
import { AnnotationWorkspace, ImageBackground } from './components/annotation';

<AnnotationWorkspace
  title="Akut Böbrek Hasarı"
  storageKey={`note:${noteId}`}            // tarayıcıda kaydet
  background={<ImageBackground src={pageUrl} />}
  onDocumentChange={(doc) => {/* sunucuya senkron (debounce önerilir) */}}
  onClose={() => setOpen(false)}
/>
```

Kısayollar: Ctrl/⌘+Z geri, Ctrl/⌘+Shift+Z veya Ctrl+Y ileri, `P` kalem, `H` fosforlu, `E` silgi, `Esc` kapat.

## Sonraki adımlar

- **PDF:** `pdfjs-dist` ile her sayfayı `background` içine canvas/img olarak alt alta render et;
  çok sayfalı belgede sayfa başına ayrı `AnnotationDocument` ya da sayfa ofsetli tek belge.
- **Sunucu senkronu:** `onDocumentChange` → `safeJsonFetch('/api/...')` (kullanıcı başına not çizimleri).
- Kement (lasso) seçimi, şekil tanıma, fosforluyu düz çizgiye yaslama.
