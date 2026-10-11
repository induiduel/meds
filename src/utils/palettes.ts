/**
 * Palet kaydı — yeni renk modu eklemek için tek yer.
 *
 * Her palet: kimlik (data-palette değeri), ait olduğu tema (light / sepia / dark), ad, kısa açıklama,
 * ayarlardaki renk örneği ve (isteğe bağlı) token değerleri.
 *  - `vars` VERİLMEZSE renkler styles/appearance.css'teki elle yazılmış bloktan gelir (a / b paletleri).
 *  - `vars` VERİLİRSE CSS çalışma anında üretilir ve <style id="palette-registry"> olarak eklenir;
 *    yani yeni palet = bu listeye bir nesne. Ayarlar ekranı listeyi otomatik gösterir.
 * Eksik bırakılan token'lar aynı temanın `a` paletinden miras alınır (seçici yalnız verilenleri ezer).
 */
export type ThemeMode = 'light' | 'sepia' | 'dark';

export interface PaletteDef {
  id: string;
  mode: ThemeMode;
  name: string;
  hint: string;
  /** [zemin, yüzey, vurgu] */
  swatch: [string, string, string];
  /** --color-* token değerleri (anahtarlar "--" olmadan, örn. "accent") */
  vars?: Record<string, string>;
}

export const PALETTES: PaletteDef[] = [
  // ── Açık ──
  { id: 'a', mode: 'light', name: 'Klinik mavi', hint: 'Steril beyaz zemin, mavi-camgöbeği vurgu', swatch: ['#F7F9FB', '#FFFFFF', '#0A6E8A'] },
  { id: 'b', mode: 'light', name: 'Sıcak arduvaz', hint: 'Yumuşak gri zemin, arduvaz vurgu', swatch: ['#F3F3F1', '#FCFCFB', '#3E5468'] },
  {
    id: 'c', mode: 'light', name: 'Lavanta', hint: 'Serin lila zemin, çivit vurgu', swatch: ['#F6F5FB', '#FFFFFF', '#5146B8'],
    vars: {
      'on-solid': '#FFFFFF',
      canvas: '#F6F5FB', white: '#FFFFFF', field: '#EEECF7',
      line: '#E2DFF0', 'line-soft': '#ECEAF5', 'line-2': '#C7C2DE',
      ink: '#1B1830', 'ink-2': '#43405C', 'ink-3': '#64607E', 'ink-surface': '#24203D',
      accent: '#5146B8', 'accent-hover': '#41379A', 'accent-soft': '#E7E4F8', 'on-accent': '#FFFFFF',
      clinic: '#0F7268', 'clinic-soft': '#DBF2EF',
      ok: '#1F7040', 'ok-soft': '#E0F1E6', 'ok-tint': '#EFF9F2',
      warn: '#8F530E', 'warn-soft': '#F8EBD6',
      bad: '#C0353A', 'bad-text': '#AD2C31', 'bad-soft': '#F9E3E3',
      ai: '#8A3FA0', 'ai-soft': '#F4E6F8',
      brand: '#E0245E',
    },
  },
  // ── Sarı (sepya) ──
  { id: 'a', mode: 'sepia', name: 'Parşömen', hint: 'Kemik rengi zemin, kahve-siyah yazı', swatch: ['#F6F0E3', '#FBF7EE', '#8A5A2B'] },
  { id: 'b', mode: 'sepia', name: 'Kehribar', hint: 'Bej-amber zemin, düşük mavi ışık', swatch: ['#F1E4C8', '#F8EED9', '#9A5B12'] },
  // ── Koyu ──
  { id: 'a', mode: 'dark', name: 'Gece arduvazı', hint: 'Lacivert-arduvaz zemin, yumuşak neon odak', swatch: ['#0F1624', '#172131', '#5CC8E6'] },
  { id: 'b', mode: 'dark', name: 'OLED obsidyen', hint: 'Saf siyah zemin, net gri ayrım', swatch: ['#000000', '#0E0E10', '#7AB4FF'] },
];

export const palettesFor = (mode: ThemeMode) => PALETTES.filter((p) => p.mode === mode);
export const findPalette = (mode: ThemeMode, id: string | undefined) =>
  PALETTES.find((p) => p.mode === mode && p.id === id) || palettesFor(mode)[0];

/** `vars` taşıyan paletlerin CSS'ini üretip belgeye bir kez ekler (yeniden çağrılırsa günceller). */
export function installPaletteStyles() {
  if (typeof document === 'undefined') return;
  const css = PALETTES.filter((p) => p.vars && Object.keys(p.vars).length)
    .map((p) => {
      const body = Object.entries(p.vars!).map(([k, v]) => `  --color-${k}: ${v};`).join('\n');
      // appearance.css bloklarıyla aynı özgüllük (0,3,1) + sonra eklendiği için onları ezer
      return `html.ui-v7[data-mode="${p.mode}"][data-palette="${p.id}"] {\n${body}\n  --ui-focus: ${p.vars!.accent || 'inherit'};\n}`;
    })
    .join('\n');
  let el = document.getElementById('palette-registry') as HTMLStyleElement | null;
  if (!el) {
    el = document.createElement('style');
    el.id = 'palette-registry';
    document.head.appendChild(el);
  }
  el.textContent = css;
}
