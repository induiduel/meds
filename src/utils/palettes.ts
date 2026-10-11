/**
 * Palet kaydı — renk modlarının TEK doğruluk kaynağı (v9).
 *
 * Her tema (açık / sarı / koyu) için 4 palet (a, b, c, d) vardır. Her palet tam token setini taşır;
 * CSS çalışma anında üretilir ve <style id="palette-registry"> olarak eklenir. styles/appearance.css'teki
 * eski elle yazılmış bloklar yalnız yedektir; buradaki seçici daha özgül olduğu için her zaman kazanır.
 *  - Yeni palet = bu listeye bir nesne (tüm anahtarlar zorunlu, bkz. TOKEN_KEYS).
 *  - Kontrast kapısı: `node scripts/design/check-contrast.mjs` (bu dosyayı okur; her çift ≥4.5:1).
 *  - Ayarlar ekranı listeyi otomatik gösterir; silinmiş palet seçimi temanın ilk paletine döner.
 */
export type ThemeMode = 'light' | 'sepia' | 'dark';

export const TOKEN_KEYS = [
  'canvas', 'white', 'field', 'line', 'line-soft', 'line-2',
  'ink', 'ink-2', 'ink-3', 'ink-surface',
  'accent', 'accent-hover', 'accent-soft', 'on-accent',
  'clinic', 'clinic-soft', 'ok', 'ok-soft', 'ok-tint', 'ok-bright',
  'warn', 'warn-soft', 'bad', 'bad-text', 'bad-soft', 'ai', 'ai-soft',
  'brand', 'brand-soft', 'on-solid',
] as const;
export type TokenKey = (typeof TOKEN_KEYS)[number];

export interface PaletteDef {
  id: string;
  mode: ThemeMode;
  name: string;
  hint: string;
  /** [zemin, yüzey, vurgu] — ayarlardaki küçük önizleme */
  swatch: [string, string, string];
  /** --color-* token değerleri (anahtarlar "--" olmadan) */
  vars: Record<TokenKey, string>;
}

export const PALETTES: PaletteDef[] = [
  // ── Açık ──
  {
    id: 'a', mode: 'light', name: 'Klinik mavi', hint: 'Steril beyaz zemin, net mavi vurgu',
    swatch: ['#F4F6F9', '#FFFFFF', '#1A5FB4'],
    vars: {
      canvas: '#F4F6F9', white: '#FFFFFF', field: '#ECF0F4', line: '#DDE3EA', 'line-soft': '#E9EDF2', 'line-2': '#C2CBD6',
      ink: '#121A24', 'ink-2': '#384554', 'ink-3': '#566475', 'ink-surface': '#1B2633', accent: '#1A5FB4', 'accent-hover': '#154E95',
      'accent-soft': '#E1EBF8', 'on-accent': '#FFFFFF', clinic: '#00706A', 'clinic-soft': '#D9F2EF', ok: '#1D6E3E', 'ok-soft': '#DFF0E5',
      'ok-tint': '#EEF8F1', 'ok-bright': '#1F9D55', warn: '#8C500C', 'warn-soft': '#F7E9D3', bad: '#BE3036', 'bad-text': '#A9282E',
      'bad-soft': '#F9E2E2', ai: '#7A3BA0', 'ai-soft': '#F1E6F8', brand: '#E0245E', 'brand-soft': '#FCE6ED', 'on-solid': '#FFFFFF',
    },
  },
  {
    id: 'b', mode: 'light', name: 'Nane', hint: 'Serin yeşil-gri zemin, camgöbeği vurgu',
    swatch: ['#F2F6F5', '#FFFFFF', '#00696B'],
    vars: {
      canvas: '#F2F6F5', white: '#FFFFFF', field: '#E9F0EE', line: '#D8E3E0', 'line-soft': '#E5EDEB', 'line-2': '#BACBC7',
      ink: '#10201D', 'ink-2': '#33463F', 'ink-3': '#4F625C', 'ink-surface': '#18302B', accent: '#00696B', 'accent-hover': '#005557',
      'accent-soft': '#D6EEEC', 'on-accent': '#FFFFFF', clinic: '#2C6B3F', 'clinic-soft': '#DDEFE2', ok: '#1D6E3E', 'ok-soft': '#DDEFE3',
      'ok-tint': '#EDF7F0', 'ok-bright': '#1F9D55', warn: '#895009', 'warn-soft': '#F5E8D2', bad: '#B9333A', 'bad-text': '#A42A30',
      'bad-soft': '#F7E1E1', ai: '#6E4396', 'ai-soft': '#EEE6F5', brand: '#D9285F', 'brand-soft': '#FAE5EB', 'on-solid': '#FFFFFF',
    },
  },
  {
    id: 'c', mode: 'light', name: 'Lavanta', hint: 'Serin lila zemin, çivit vurgu',
    swatch: ['#F5F4FA', '#FFFFFF', '#5146B8'],
    vars: {
      canvas: '#F5F4FA', white: '#FFFFFF', field: '#EDEBF6', line: '#E0DDEE', 'line-soft': '#EAE8F4', 'line-2': '#C4BFDC',
      ink: '#1A1730', 'ink-2': '#423E5A', 'ink-3': '#5F5A7A', 'ink-surface': '#24203D', accent: '#5146B8', 'accent-hover': '#41379A',
      'accent-soft': '#E6E3F8', 'on-accent': '#FFFFFF', clinic: '#0F6F66', 'clinic-soft': '#DAF1EE', ok: '#1F6D3F', 'ok-soft': '#DFEFE5',
      'ok-tint': '#EEF8F1', 'ok-bright': '#1F9D55', warn: '#8C510D', 'warn-soft': '#F7EAD5', bad: '#BD333A', 'bad-text': '#A82A30',
      'bad-soft': '#F8E2E3', ai: '#8A3B9E', 'ai-soft': '#F4E5F7', brand: '#E0245E', 'brand-soft': '#FCE6ED', 'on-solid': '#FFFFFF',
    },
  },
  {
    id: 'd', mode: 'light', name: 'Mercan', hint: 'Sıcak kırık beyaz zemin, mercan-gül vurgu',
    swatch: ['#F8F4F3', '#FFFFFF', '#B3364A'],
    vars: {
      canvas: '#F8F4F3', white: '#FFFFFF', field: '#F2ECEA', line: '#E7DFDC', 'line-soft': '#F0E9E7', 'line-2': '#D2C4C0',
      ink: '#231816', 'ink-2': '#4B3C38', 'ink-3': '#695853', 'ink-surface': '#2E201D', accent: '#B3364A', 'accent-hover': '#952B3C',
      'accent-soft': '#F8E1E4', 'on-accent': '#FFFFFF', clinic: '#1F6B67', 'clinic-soft': '#DCEFED', ok: '#2A6B3A', 'ok-soft': '#E2EFE4',
      'ok-tint': '#F0F7F1', 'ok-bright': '#1F9D55', warn: '#8A4E0A', 'warn-soft': '#F6E7D1', bad: '#B42F2F', 'bad-text': '#A02828',
      'bad-soft': '#F8E1DE', ai: '#7B3F96', 'ai-soft': '#F1E5F5', brand: '#D12B5C', 'brand-soft': '#FBE4EA', 'on-solid': '#FFFFFF',
    },
  },
  // ── Sarı (sepya) ──
  {
    id: 'a', mode: 'sepia', name: 'Parşömen', hint: 'Kemik rengi zemin, kahve vurgu (uzun okuma)',
    swatch: ['#F3ECDD', '#FAF6EC', '#7E5026'],
    vars: {
      canvas: '#F3ECDD', white: '#FAF6EC', field: '#ECE3D0', line: '#DFD3BA', 'line-soft': '#E8DECA', 'line-2': '#C9B99B',
      ink: '#32271D', 'ink-2': '#554535', 'ink-3': '#6A5846', 'ink-surface': '#3D3126', accent: '#7E5026', 'accent-hover': '#68411E',
      'accent-soft': '#EBDCC2', 'on-accent': '#FFF9F0', clinic: '#3C6253', 'clinic-soft': '#DFE5D3', ok: '#43602A', 'ok-soft': '#E1E3C9',
      'ok-tint': '#ECECD8', 'ok-bright': '#5A8A2E', warn: '#824D0C', 'warn-soft': '#EFDCBA', bad: '#9F3727', 'bad-text': '#8F3122',
      'bad-soft': '#F0DACB', ai: '#6B467B', 'ai-soft': '#E9DDE0', brand: '#B8324F', 'brand-soft': '#F1D9D4', 'on-solid': '#FFFFFF',
    },
  },
  {
    id: 'b', mode: 'sepia', name: 'Kehribar', hint: 'Bej-amber zemin, düşük mavi ışık',
    swatch: ['#EFE3C7', '#F8EFDA', '#874B09'],
    vars: {
      canvas: '#EFE3C7', white: '#F8EFDA', field: '#E8D9B8', line: '#DBC8A2', 'line-soft': '#E4D5B4', 'line-2': '#C4AD80',
      ink: '#30240E', 'ink-2': '#523D1E', 'ink-3': '#664F2E', 'ink-surface': '#3A2D16', accent: '#874B09', 'accent-hover': '#703C05',
      'accent-soft': '#ECD4A8', 'on-accent': '#FFF8EA', clinic: '#475D3D', 'clinic-soft': '#E1DFBC', ok: '#465B1D', 'ok-soft': '#E0DDB3',
      'ok-tint': '#EAE5C4', 'ok-bright': '#6A8A22', warn: '#7B4705', 'warn-soft': '#ECD2A0', bad: '#97331F', 'bad-text': '#882C1A',
      'bad-soft': '#EED1B7', ai: '#66426C', 'ai-soft': '#E6D4C9', brand: '#B02E45', 'brand-soft': '#EFD3C2', 'on-solid': '#FFFFFF',
    },
  },
  {
    id: 'c', mode: 'sepia', name: 'Zeytin', hint: 'Krem zemin, zeytin yeşili vurgu',
    swatch: ['#F2EEDC', '#F9F6EA', '#55621E'],
    vars: {
      canvas: '#F2EEDC', white: '#F9F6EA', field: '#EAE5CF', line: '#DCD5B9', 'line-soft': '#E6E0C8', 'line-2': '#C4BB98',
      ink: '#272817', 'ink-2': '#474832', 'ink-3': '#5C5D44', 'ink-surface': '#33341F', accent: '#55621E', 'accent-hover': '#454F18',
      'accent-soft': '#E2E4C3', 'on-accent': '#FBFAF0', clinic: '#3B6152', 'clinic-soft': '#DCE4D2', ok: '#3F6326', 'ok-soft': '#DEE4C6',
      'ok-tint': '#E9EDD6', 'ok-bright': '#5C8A2C', warn: '#7F4C0A', 'warn-soft': '#EEDCB8', bad: '#9C3628', 'bad-text': '#8C3022',
      'bad-soft': '#EFD8C8', ai: '#674678', 'ai-soft': '#E6DCDD', brand: '#AF3450', 'brand-soft': '#EFD9D2', 'on-solid': '#FFFFFF',
    },
  },
  {
    id: 'd', mode: 'sepia', name: 'Kiremit', hint: 'Kum zemin, kiremit-terrakota vurgu',
    swatch: ['#F4E9DC', '#FBF4EA', '#9A4426'],
    vars: {
      canvas: '#F4E9DC', white: '#FBF4EA', field: '#EDE0CF', line: '#E1D0BB', 'line-soft': '#EADCCA', 'line-2': '#CDB69B',
      ink: '#33231A', 'ink-2': '#573F31', 'ink-3': '#6C5243', 'ink-surface': '#3E2B20', accent: '#9A4426', 'accent-hover': '#80381F',
      'accent-soft': '#F0D9C9', 'on-accent': '#FFF8F2', clinic: '#3E6158', 'clinic-soft': '#DFE4D6', ok: '#47622A', 'ok-soft': '#E2E3C9',
      'ok-tint': '#EDECD9', 'ok-bright': '#5E8A2E', warn: '#83490B', 'warn-soft': '#F0D9B9', bad: '#A0302A', 'bad-text': '#902A24',
      'bad-soft': '#F2D7CB', ai: '#6E4578', 'ai-soft': '#EBDBDB', brand: '#B52F4C', 'brand-soft': '#F2D8D2', 'on-solid': '#FFFFFF',
    },
  },
  // ── Koyu ──
  {
    id: 'a', mode: 'dark', name: 'Gece mavisi', hint: 'Lacivert-arduvaz zemin, camgöbeği vurgu',
    swatch: ['#0D1420', '#151E2C', '#5CC6E4'],
    vars: {
      canvas: '#0D1420', white: '#151E2C', field: '#1C2738', line: '#263349', 'line-soft': '#1C2738', 'line-2': '#36465F',
      ink: '#E3E9F2', 'ink-2': '#B4BFCE', 'ink-3': '#8E9BAD', 'ink-surface': '#1C2738', accent: '#5CC6E4', 'accent-hover': '#80D4EC',
      'accent-soft': '#12313F', 'on-accent': '#04141A', clinic: '#4FD1C5', 'clinic-soft': '#0E2E2D', ok: '#5ED492', 'ok-soft': '#11291E',
      'ok-tint': '#0C2219', 'ok-bright': '#4ADE80', warn: '#F0B35C', 'warn-soft': '#2D2414', bad: '#F07C7C', 'bad-text': '#F49494',
      'bad-soft': '#351C22', ai: '#C9A2FF', 'ai-soft': '#271E3D', brand: '#FF4D78', 'brand-soft': '#3A1622', 'on-solid': '#06121A',
    },
  },
  {
    id: 'b', mode: 'dark', name: 'OLED siyah', hint: 'Saf siyah zemin, kılçizgi ayrımı, mavi vurgu',
    swatch: ['#000000', '#0E0E10', '#7AB4FF'],
    vars: {
      canvas: '#000000', white: '#0E0E10', field: '#18181B', line: '#252529', 'line-soft': '#18181B', 'line-2': '#3A3A40',
      ink: '#F2F2F4', 'ink-2': '#C5C5CB', 'ink-3': '#9A9AA2', 'ink-surface': '#18181B', accent: '#7AB4FF', 'accent-hover': '#9BC7FF',
      'accent-soft': '#0E1F36', 'on-accent': '#000000', clinic: '#4FD8C8', 'clinic-soft': '#0A2724', ok: '#4ADE80', 'ok-soft': '#0D2416',
      'ok-tint': '#08190F', 'ok-bright': '#4ADE80', warn: '#FBBF24', 'warn-soft': '#2A2008', bad: '#FF6B6B', 'bad-text': '#FF8A8A',
      'bad-soft': '#330F12', ai: '#D0A6FF', 'ai-soft': '#22163A', brand: '#FF4D78', 'brand-soft': '#33101B', 'on-solid': '#000000',
    },
  },
  {
    id: 'c', mode: 'dark', name: 'Orman', hint: 'Yeşil-grafit zemin, nane vurgu',
    swatch: ['#0E1513', '#151E1B', '#5FD3A8'],
    vars: {
      canvas: '#0E1513', white: '#151E1B', field: '#1C2824', line: '#26342F', 'line-soft': '#1C2824', 'line-2': '#36473F',
      ink: '#E2EDE8', 'ink-2': '#B2C3BC', 'ink-3': '#8DA097', 'ink-surface': '#1C2824', accent: '#5FD3A8', 'accent-hover': '#83DFBD',
      'accent-soft': '#11302A', 'on-accent': '#03140E', clinic: '#6CC9E0', 'clinic-soft': '#0F2A31', ok: '#7BDB8F', 'ok-soft': '#132A18',
      'ok-tint': '#0D2112', 'ok-bright': '#4ADE80', warn: '#EDB866', 'warn-soft': '#2C2414', bad: '#F28585', 'bad-text': '#F59C9C',
      'bad-soft': '#341C1F', ai: '#C8A8F5', 'ai-soft': '#251F37', brand: '#FF5C82', 'brand-soft': '#36181F', 'on-solid': '#05130E',
    },
  },
  {
    id: 'd', mode: 'dark', name: 'Ametist', hint: 'Mürdüm-grafit zemin, lavanta vurgu',
    swatch: ['#13111A', '#1B1824', '#B9A2FF'],
    vars: {
      canvas: '#13111A', white: '#1B1824', field: '#24202F', line: '#2F2A3D', 'line-soft': '#24202F', 'line-2': '#433C55',
      ink: '#ECE8F4', 'ink-2': '#C0B9D0', 'ink-3': '#9C94AE', 'ink-surface': '#24202F', accent: '#B9A2FF', 'accent-hover': '#CBB9FF',
      'accent-soft': '#2A2245', 'on-accent': '#140C2A', clinic: '#5ED0C4', 'clinic-soft': '#102C2B', ok: '#6CD99A', 'ok-soft': '#132A1F',
      'ok-tint': '#0E2118', 'ok-bright': '#4ADE80', warn: '#F0B865', 'warn-soft': '#2E2516', bad: '#F4828E', 'bad-text': '#F79AA4',
      'bad-soft': '#381C25', ai: '#F0A6E4', 'ai-soft': '#371E36', brand: '#FF5C8A', 'brand-soft': '#381926', 'on-solid': '#120B1E',
    },
  },
];

export const palettesFor = (mode: ThemeMode) => PALETTES.filter((p) => p.mode === mode);
export const findPalette = (mode: ThemeMode, id: string | undefined) =>
  PALETTES.find((p) => p.mode === mode && p.id === id) || palettesFor(mode)[0];

const DISCIPLINES = ['pat', 'farm', 'enf', 'mikro', 'halk', 'ic', 'gen', 'cocuk', 'kadin', 'acil', 'biyo', 'ana', 'fiz', 'noro', 'psik', 'kardi', 'cerr', 'ftr', 'uro', 'onko', 'diger']
  .map((d) => `.d-${d}`)
  .join(', ');

/** Temaya bağlı (palet bağımsız) ortak kurallar: gölge, perde, ders renklerinin zemine karışması. */
const MODE_CSS = `
html:root.ui-v7[data-mode="light"] { --color-scrim: rgb(16 24 36 / .38); }
html:root.ui-v7[data-mode="sepia"] { --color-scrim: rgb(40 28 14 / .36);
  --shadow-sm: 0 1px 2px rgb(60 40 10 / .06); --shadow-md: 0 6px 18px rgb(60 40 10 / .10), 0 1px 3px rgb(60 40 10 / .06);
  --shadow-lg: 0 12px 32px rgb(60 40 10 / .14); --shadow-xl: 0 20px 56px rgb(60 40 10 / .20); }
html:root.ui-v7[data-mode="dark"] { --color-scrim: rgb(0 0 0 / .62);
  --shadow-sm: 0 1px 2px rgb(0 0 0 / .4); --shadow-md: 0 6px 18px rgb(0 0 0 / .45); --shadow-lg: 0 12px 32px rgb(0 0 0 / .55); --shadow-xl: 0 20px 56px rgb(0 0 0 / .65); }
html:root.ui-v7[data-mode="dark"][data-palette="b"] { --shadow-md: 0 0 0 1px #252529, 0 8px 24px rgb(0 0 0 / .8); --shadow-lg: 0 0 0 1px #2A2A2F, 0 14px 36px rgb(0 0 0 / .85); --shadow-xl: 0 0 0 1px #2A2A2F, 0 22px 60px rgb(0 0 0 / .9); }
html:root.ui-v7[data-mode="light"] :is(${DISCIPLINES}) { --d-soft: color-mix(in srgb, var(--d) 12%, var(--color-white)); }
html:root.ui-v7[data-mode="sepia"] :is(${DISCIPLINES}) { --d-soft: color-mix(in srgb, var(--d) 16%, var(--color-white)); --d-ink: color-mix(in srgb, var(--d-ink-base, var(--d)) 78%, var(--color-ink)); }
html:root.ui-v7[data-mode="dark"] :is(${DISCIPLINES}) { --d-soft: color-mix(in srgb, var(--d) 18%, var(--color-white)); --d-ink: color-mix(in srgb, var(--d) 70%, var(--color-ink)); }
`;

/** Palet CSS'ini üretir (Node betikleri ve tarayıcı aynı çıktıyı kullanır). */
export function buildPaletteCss(): string {
  const blocks = PALETTES.map((p) => {
    const body = TOKEN_KEYS.map((k) => `--color-${k}: ${p.vars[k]};`).join(' ');
    // (0,4,1): appearance.css (0,3,1) ve health.css/index.css eski token bloklarını her zaman ezer
    return `html:root.ui-v7[data-mode="${p.mode}"][data-palette="${p.id}"] { ${body} --ui-focus: ${p.vars.accent}; --color-teal-600: ${p.vars.accent}; }`;
  });
  return blocks.join('\n') + MODE_CSS;
}

/** Palet CSS'ini belgeye bir kez ekler (yeniden çağrılırsa dokunmaz). */
export function installPaletteStyles() {
  if (typeof document === 'undefined') return;
  if (document.getElementById('palette-registry')) return;
  const el = document.createElement('style');
  el.id = 'palette-registry';
  el.textContent = buildPaletteCss();
  document.head.appendChild(el);
}
