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
  // ── Açık · X serisi (v10): zemin neredeyse beyaz, vurgu koyu ve doygun ──
  {
    id: 'e', mode: 'light', name: 'LavantaX', hint: 'Bembeyaz lila zemin, koyu çivit (canlı)',
    swatch: ['#FCFBFF', '#FFFFFF', '#3A2BB8'],
    vars: {
      canvas: '#FCFBFF', white: '#FFFFFF', field: '#F2F0FD', line: '#E6E3F7', 'line-soft': '#EFEDFA', 'line-2': '#C9C3EE',
      ink: '#15122B', 'ink-2': '#3D3958', 'ink-3': '#5B5778', 'ink-surface': '#1F1B3A', accent: '#3A2BB8',
      'accent-hover': '#2E2196', 'accent-soft': '#EBE8FF', 'on-accent': '#FFFFFF', clinic: '#0D6A62', 'clinic-soft': '#D9F2EE',
      ok: '#1A6A3B', 'ok-soft': '#DDF3E6', 'ok-tint': '#EEF9F2', 'ok-bright': '#1F9D55', warn: '#8A4E08', 'warn-soft': '#FBEBD3',
      bad: '#B8262F', 'bad-text': '#A21F28', 'bad-soft': '#FCE4E5', ai: '#7E2FA0', 'ai-soft': '#F4E6FA', brand: '#D61F57',
      'brand-soft': '#FDE5EC', 'on-solid': '#FFFFFF',
    },
  },
  {
    id: 'f', mode: 'light', name: 'MaviX', hint: 'Buz beyazı zemin, derin kobalt (canlı)',
    swatch: ['#FAFCFF', '#FFFFFF', '#0A4DBA'],
    vars: {
      canvas: '#FAFCFF', white: '#FFFFFF', field: '#EEF4FD', line: '#E0E9F6', 'line-soft': '#EBF1FA', 'line-2': '#C2D2EA',
      ink: '#0E1626', 'ink-2': '#334055', 'ink-3': '#526075', 'ink-surface': '#172238', accent: '#0A4DBA',
      'accent-hover': '#083E96', 'accent-soft': '#E1ECFF', 'on-accent': '#FFFFFF', clinic: '#006B65', 'clinic-soft': '#D6F3EF',
      ok: '#1A6A3B', 'ok-soft': '#DDF3E6', 'ok-tint': '#EEF9F2', 'ok-bright': '#1F9D55', warn: '#8A4E08', 'warn-soft': '#FBEBD3',
      bad: '#B8262F', 'bad-text': '#A21F28', 'bad-soft': '#FCE4E5', ai: '#7A33A6', 'ai-soft': '#F2E6FA', brand: '#D61F57',
      'brand-soft': '#FDE5EC', 'on-solid': '#FFFFFF',
    },
  },
  {
    id: 'g', mode: 'light', name: 'MercanX', hint: 'Pembe-beyaz zemin, koyu mercan (canlı)',
    swatch: ['#FFFBFA', '#FFFFFF', '#B11E3A'],
    vars: {
      canvas: '#FFFBFA', white: '#FFFFFF', field: '#FCF0EE', line: '#F3E1DE', 'line-soft': '#F8EAE8', 'line-2': '#E4C3BE',
      ink: '#24110F', 'ink-2': '#4D3532', 'ink-3': '#6C514D', 'ink-surface': '#301A17', accent: '#B11E3A',
      'accent-hover': '#8F152D', 'accent-soft': '#FFE2E6', 'on-accent': '#FFFFFF', clinic: '#186A64', 'clinic-soft': '#DAF0EC',
      ok: '#236A38', 'ok-soft': '#DFF1E3', 'ok-tint': '#F0F8F1', 'ok-bright': '#1F9D55', warn: '#8A4C08', 'warn-soft': '#FBE8D0',
      bad: '#B02A22', 'bad-text': '#9C221B', 'bad-soft': '#FCE1DC', ai: '#7A3594', 'ai-soft': '#F3E5F7', brand: '#C8215A',
      'brand-soft': '#FDE3EB', 'on-solid': '#FFFFFF',
    },
  },
  // ── Sarı (sepya) — v10: çamurlu bej yerine sıcak kâğıt zemin + tek doygun vurgu ──
  {
    id: 'a', mode: 'sepia', name: 'Kâğıt', hint: 'Fildişi zemin, kiremit vurgu (uzun okuma)',
    swatch: ['#FAF5E9', '#FFFDF7', '#A63D14'],
    vars: {
      canvas: '#FAF5E9', white: '#FFFDF7', field: '#F2EAD6', line: '#E6DCC6', 'line-soft': '#EFE7D6', 'line-2': '#D3C5A8',
      ink: '#24201A', 'ink-2': '#4A4236', 'ink-3': '#685D4C', 'ink-surface': '#2E2820', accent: '#A63D14',
      'accent-hover': '#86300F', 'accent-soft': '#F8E1D2', 'on-accent': '#FFFFFF', clinic: '#2F6458', 'clinic-soft': '#DDEADF',
      ok: '#2C6748', 'ok-soft': '#DCEBDD', 'ok-tint': '#ECF4EC', 'ok-bright': '#3E8F5E', warn: '#8A5208', 'warn-soft': '#F6E3BF',
      bad: '#A92F2A', 'bad-text': '#962824', 'bad-soft': '#F6DCD3', ai: '#6E4180', 'ai-soft': '#EDE0EE', brand: '#B8324F',
      'brand-soft': '#F6DCDF', 'on-solid': '#FFFFFF',
    },
  },
  {
    id: 'b', mode: 'sepia', name: 'Bal & lacivert', hint: 'Bal sarısı zemin, lacivert vurgu',
    swatch: ['#F8F0DA', '#FFFBF0', '#1F4E8C'],
    vars: {
      canvas: '#F8F0DA', white: '#FFFBF0', field: '#F0E5C8', line: '#E5D7B4', 'line-soft': '#EDE2C6', 'line-2': '#CFBD92',
      ink: '#1E2330', 'ink-2': '#454A57', 'ink-3': '#5C6069', 'ink-surface': '#2A2F3C', accent: '#1F4E8C',
      'accent-hover': '#183F72', 'accent-soft': '#DDE6F2', 'on-accent': '#FFFFFF', clinic: '#2D6359', 'clinic-soft': '#DCE8DD',
      ok: '#2F6A3F', 'ok-soft': '#DEEAD3', 'ok-tint': '#ECF2DF', 'ok-bright': '#4C8A3A', warn: '#855007', 'warn-soft': '#F3DDB0',
      bad: '#A3312A', 'bad-text': '#8F2A24', 'bad-soft': '#F3D8C8', ai: '#5E4486', 'ai-soft': '#E7DEEC', brand: '#B0304B',
      'brand-soft': '#F3D9D6', 'on-solid': '#FFFFFF',
    },
  },
  {
    id: 'c', mode: 'sepia', name: 'Adaçayı', hint: 'Krem zemin, orman yeşili vurgu',
    swatch: ['#F5F3E4', '#FDFCF3', '#2C6748'],
    vars: {
      canvas: '#F5F3E4', white: '#FDFCF3', field: '#ECE9D4', line: '#DEDAC0', 'line-soft': '#E8E5CF', 'line-2': '#C6C1A0',
      ink: '#1E251E', 'ink-2': '#424A40', 'ink-3': '#5A6157', 'ink-surface': '#283028', accent: '#2C6748',
      'accent-hover': '#22533A', 'accent-soft': '#DBEADD', 'on-accent': '#FFFFFF', clinic: '#2A6066', 'clinic-soft': '#D8E8E6',
      ok: '#2E6A35', 'ok-soft': '#DCEAD2', 'ok-tint': '#EBF2E2', 'ok-bright': '#4E8A3A', warn: '#855008', 'warn-soft': '#F1E0B9',
      bad: '#A3352B', 'bad-text': '#902E25', 'bad-soft': '#F2DACD', ai: '#66457A', 'ai-soft': '#E8E0EA', brand: '#AF3450',
      'brand-soft': '#F2DCD8', 'on-solid': '#FFFFFF',
    },
  },
  {
    id: 'd', mode: 'sepia', name: 'Mürdüm', hint: 'Kum beji zemin, mürdüm vurgu',
    swatch: ['#F9F2E8', '#FFFBF5', '#7D2C5C'],
    vars: {
      canvas: '#F9F2E8', white: '#FFFBF5', field: '#F1E7D9', line: '#E6D9C8', 'line-soft': '#EEE3D4', 'line-2': '#D0BFA8',
      ink: '#2A1E24', 'ink-2': '#4F4048', 'ink-3': '#67585E', 'ink-surface': '#352830', accent: '#7D2C5C',
      'accent-hover': '#65234A', 'accent-soft': '#F2DCE7', 'on-accent': '#FFFFFF', clinic: '#2F6158', 'clinic-soft': '#DCE8E2',
      ok: '#33663A', 'ok-soft': '#E0EAD6', 'ok-tint': '#EEF3E6', 'ok-bright': '#4E8A3A', warn: '#855008', 'warn-soft': '#F4E0BD',
      bad: '#A8302C', 'bad-text': '#942925', 'bad-soft': '#F4DAD1', ai: '#5D4693', 'ai-soft': '#E8E1F0', brand: '#B12F55',
      'brand-soft': '#F5DAE0', 'on-solid': '#FFFFFF',
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
  // ── Koyu · v10: sıcak tonlu iki yeni palet ──
  {
    id: 'e', mode: 'dark', name: 'Grafit', hint: 'Nötr kömür zemin, kehribar vurgu',
    swatch: ['#121212', '#1C1C1E', '#F2B55C'],
    vars: {
      canvas: '#121212', white: '#1C1C1E', field: '#26262A', line: '#2E2E33', 'line-soft': '#26262A', 'line-2': '#44444B',
      ink: '#ECECEE', 'ink-2': '#C4C4C9', 'ink-3': '#A1A1A8', 'ink-surface': '#26262A', accent: '#F2B55C',
      'accent-hover': '#F6C77F', 'accent-soft': '#3A2C14', 'on-accent': '#1A1206', clinic: '#5FCFC3', 'clinic-soft': '#10292A',
      ok: '#6CD99A', 'ok-soft': '#132A1F', 'ok-tint': '#0E2118', 'ok-bright': '#4ADE80', warn: '#FFB86B', 'warn-soft': '#33240F',
      bad: '#F28585', 'bad-text': '#F59C9C', 'bad-soft': '#361C1F', ai: '#C9A6FF', 'ai-soft': '#261F38', brand: '#FF5C82',
      'brand-soft': '#37161F', 'on-solid': '#121212',
    },
  },
  {
    id: 'f', mode: 'dark', name: 'Gece mercanı', hint: 'Mürdüm-siyah zemin, mercan vurgu',
    swatch: ['#150F12', '#1F171B', '#FF8F8F'],
    vars: {
      canvas: '#150F12', white: '#1F171B', field: '#2A1F25', line: '#33262D', 'line-soft': '#2A1F25', 'line-2': '#4A3841',
      ink: '#F3E9EC', 'ink-2': '#CDBDC3', 'ink-3': '#B7A3AA', 'ink-surface': '#2A1F25', accent: '#FF8F8F',
      'accent-hover': '#FFAAAA', 'accent-soft': '#3D1E22', 'on-accent': '#1E0809', clinic: '#5CCFC2', 'clinic-soft': '#0F2A29',
      ok: '#6CD99A', 'ok-soft': '#13291E', 'ok-tint': '#0E2017', 'ok-bright': '#4ADE80', warn: '#F2B865', 'warn-soft': '#33260F',
      bad: '#FF7A86', 'bad-text': '#FF9AA3', 'bad-soft': '#3D1A20', ai: '#D6A8FF', 'ai-soft': '#2B1E38', brand: '#FF6B95',
      'brand-soft': '#3E1726', 'on-solid': '#150F12',
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
