/**
 * Palet kaydı — renk modlarının TEK doğruluk kaynağı (v9).
 *
 * Paletler: açık 9 (a–i), sarı 6 (a–f), koyu 8 (a–h); her biri ayrı renk ailesi, her temada bir "Yüksek kontrast". Her palet tam token setini taşır;
 * CSS çalışma anında üretilir ve <style id="palette-registry"> olarak eklenir. styles/appearance.css'teki
 * eski elle yazılmış bloklar yalnız yedektir; buradaki seçici daha özgül olduğu için her zaman kazanır.
 *  - Yeni palet = bu listeye bir nesne (tüm anahtarlar zorunlu, bkz. TOKEN_KEYS).
 *  - Kontrast kapısı: `npx tsx scripts/design/check-contrast.mjs` (her çift ≥4.5:1, ink-3 ≥5; vurgu seçenekleri;
 *    aynı temada zemin+vurgusu neredeyse aynı iki palet = kopya → HATA).
 *  - Yazıyı `opacity` ile soluklaştırma: bazı paletlerde eşiğin altına düşer; `--color-ink-3` kullan.
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
  /** İsteğe bağlı vurgu rengi seçenekleri (Ayarlar → "Vurgu rengi"). İlki paletin kendi rengidir.
   *  Seçim kök öğeye `data-accent` olarak yazılır; yalnız accent/accent-hover/accent-soft/on-accent değişir. */
  accents?: AccentDef[];
}

export interface AccentDef { id: string; name: string; accent: string; hover: string; soft: string; on: string }

/** Koyu zeminde ≥4.5:1 kontrastlı açık tonlar; `on` vurgu zemininde yazı rengi. */
const OLED_ACCENTS: AccentDef[] = [
  { id: 'mavi', name: 'Mavi', accent: '#7AB4FF', hover: '#9BC7FF', soft: '#0E1F36', on: '#000000' },
  { id: 'turkuaz', name: 'Turkuaz', accent: '#4FD8E0', hover: '#7BE3E9', soft: '#082A2D', on: '#000000' },
  { id: 'yesil', name: 'Yeşil', accent: '#5EE08F', hover: '#84E9AA', soft: '#0B2617', on: '#000000' },
  { id: 'mor', name: 'Mor', accent: '#B49CFF', hover: '#C9B8FF', soft: '#1E1638', on: '#000000' },
  { id: 'pembe', name: 'Pembe', accent: '#FF7EB6', hover: '#FF9DC8', soft: '#33101F', on: '#000000' },
  { id: 'turuncu', name: 'Turuncu', accent: '#FFA54F', hover: '#FFBB78', soft: '#2E1B08', on: '#000000' },
  { id: 'sari', name: 'Sarı', accent: '#F5D04A', hover: '#F8DC74', soft: '#2A2306', on: '#000000' },
  { id: 'beyaz', name: 'Beyaz', accent: '#E8E8EC', hover: '#FFFFFF', soft: '#1E1E22', on: '#000000' },
];
const GECE_MERCAN_ACCENTS: AccentDef[] = [
  { id: 'mercan', name: 'Mercan', accent: '#FF8F8F', hover: '#FFAAAA', soft: '#3D1E22', on: '#1E0809' },
  { id: 'gul', name: 'Gül', accent: '#FF7FAE', hover: '#FF9EC2', soft: '#3D1828', on: '#1E0810' },
  { id: 'seftali', name: 'Şeftali', accent: '#FFB088', hover: '#FFC6A8', soft: '#3A2218', on: '#1E0D06' },
  { id: 'altin', name: 'Altın', accent: '#F4C76A', hover: '#F7D68F', soft: '#352812', on: '#1A1204' },
  { id: 'nane', name: 'Nane', accent: '#6FDDB5', hover: '#93E7C8', soft: '#12302A', on: '#04140F' },
  { id: 'gok', name: 'Gök', accent: '#8EC5FF', hover: '#AED5FF', soft: '#172638', on: '#06101C' },
  { id: 'lavanta', name: 'Lavanta', accent: '#C7A6FF', hover: '#D8C0FF', soft: '#2A1E40', on: '#140A24' },
  { id: 'fusya', name: 'Fuşya', accent: '#F08BE6', hover: '#F5AAEE', soft: '#3A1838', on: '#1C0619' },
];

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
    id: 'c', mode: 'light', name: 'Lavanta', hint: 'Serin lila zemin, menekşe vurgu',
    swatch: ['#F5F4FA', '#FFFFFF', '#6233C2'],
    vars: {
      canvas: '#F5F4FA', white: '#FFFFFF', field: '#EDEBF6', line: '#E0DDEE', 'line-soft': '#EAE8F4', 'line-2': '#C4BFDC',
      ink: '#1A1730', 'ink-2': '#423E5A', 'ink-3': '#5F5A7A', 'ink-surface': '#24203D', accent: '#6233C2', 'accent-hover': '#4F27A0',
      'accent-soft': '#ECE4FB', 'on-accent': '#FFFFFF', clinic: '#0F6F66', 'clinic-soft': '#DAF1EE', ok: '#1F6D3F', 'ok-soft': '#DFEFE5',
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
  // ── Açık · v15: her palet ayrı renk ailesi (eski X serisi a/c/d'nin kopyasıydı) ──
  {
    id: 'e', mode: 'light', name: 'Zümrüt', hint: 'Yeşilimsi beyaz zemin, zümrüt yeşili vurgu',
    swatch: ['#F3F7F3', '#FFFFFF', '#1B6B34'],
    vars: { canvas: '#F3F7F3', white: '#FFFFFF', field: '#E8F0E9', line: '#D6E4D8', 'line-soft': '#E4EDE5', 'line-2': '#B5CDB9', ink: '#0F1F14', 'ink-2': '#2F4636', 'ink-3': '#4A604F', 'ink-surface': '#17301F', accent: '#1B6B34', 'accent-hover': '#14562A', 'accent-soft': '#DCEFE0', 'on-accent': '#FFFFFF', clinic: '#00626B', 'clinic-soft': '#D7EEF0', ok: '#1D6E3E', 'ok-soft': '#DDF0E3', 'ok-tint': '#EEF8F1', 'ok-bright': '#1F9D55', warn: '#8A4E08', 'warn-soft': '#F7E9D3', bad: '#B8262F', 'bad-text': '#A21F28', 'bad-soft': '#FCE4E5', ai: '#7A33A6', 'ai-soft': '#F2E6FA', brand: '#D61F57', 'brand-soft': '#FDE5EC', 'on-solid': '#FFFFFF' },
  },
  {
    id: 'f', mode: 'light', name: 'Kehribar', hint: 'Kremsi beyaz zemin, koyu kehribar vurgu',
    swatch: ['#F9F6F0', '#FFFFFF', '#8F4A00'],
    vars: { canvas: '#F9F6F0', white: '#FFFFFF', field: '#F2ECE1', line: '#E6DCCB', 'line-soft': '#EFE8DC', 'line-2': '#D0C1A6', ink: '#221A0E', 'ink-2': '#4A3D2A', 'ink-3': '#665641', 'ink-surface': '#2C2214', accent: '#8F4A00', 'accent-hover': '#733B00', 'accent-soft': '#F8E7CF', 'on-accent': '#FFFFFF', clinic: '#0F6A64', 'clinic-soft': '#D9F0EC', ok: '#1F6B3A', 'ok-soft': '#DFF0E4', 'ok-tint': '#EFF7F0', 'ok-bright': '#1F9D55', warn: '#9A3D0A', 'warn-soft': '#FBE3D3', bad: '#B8262F', 'bad-text': '#A21F28', 'bad-soft': '#FCE4E5', ai: '#6E3FA0', 'ai-soft': '#EFE6F8', brand: '#C8215A', 'brand-soft': '#FDE3EB', 'on-solid': '#FFFFFF' },
  },
  {
    id: 'g', mode: 'light', name: 'Mürekkep', hint: 'Nötr gri zemin, siyah-grafit vurgu (renksiz, odaklı)',
    swatch: ['#F5F5F6', '#FFFFFF', '#1F2937'],
    vars: { canvas: '#F5F5F6', white: '#FFFFFF', field: '#EDEDEF', line: '#DEDEE2', 'line-soft': '#EAEAED', 'line-2': '#BDBDC4', ink: '#0B0B0E', 'ink-2': '#2E2E35', 'ink-3': '#4B4B54', 'ink-surface': '#18181C', accent: '#1F2937', 'accent-hover': '#111827', 'accent-soft': '#E5E7EB', 'on-accent': '#FFFFFF', clinic: '#006B65', 'clinic-soft': '#D6F3EF', ok: '#1A6A3B', 'ok-soft': '#DDF3E6', 'ok-tint': '#EEF9F2', 'ok-bright': '#1F9D55', warn: '#8A4E08', 'warn-soft': '#FBEBD3', bad: '#B8262F', 'bad-text': '#A21F28', 'bad-soft': '#FCE4E5', ai: '#7A33A6', 'ai-soft': '#F2E6FA', brand: '#D61F57', 'brand-soft': '#FDE5EC', 'on-solid': '#FFFFFF' },
  },
  {
    id: 'h', mode: 'light', name: 'Erik', hint: 'Pembemsi beyaz zemin, erik moru vurgu',
    swatch: ['#FAF5F9', '#FFFFFF', '#8E1F74'],
    vars: { canvas: '#FAF5F9', white: '#FFFFFF', field: '#F3EAF1', line: '#E8DAE5', 'line-soft': '#F1E7EF', 'line-2': '#D3BCCD', ink: '#22121E', 'ink-2': '#4A3245', 'ink-3': '#684E62', 'ink-surface': '#2E1A29', accent: '#8E1F74', 'accent-hover': '#731760', 'accent-soft': '#F6E1F0', 'on-accent': '#FFFFFF', clinic: '#0F6A64', 'clinic-soft': '#D9F0EC', ok: '#1F6B3A', 'ok-soft': '#DFF0E4', 'ok-tint': '#EFF7F0', 'ok-bright': '#1F9D55', warn: '#8A4E08', 'warn-soft': '#F7E9D3', bad: '#B8262F', 'bad-text': '#A21F28', 'bad-soft': '#FCE4E5', ai: '#5B3FB0', 'ai-soft': '#ECE7FA', brand: '#C8215A', 'brand-soft': '#FDE3EB', 'on-solid': '#FFFFFF' },
  },
  {
    id: 'i', mode: 'light', name: 'Yüksek kontrast', hint: 'Saf beyaz zemin, siyah metin, koyu mavi vurgu (en okunaklı)',
    swatch: ['#FFFFFF', '#FFFFFF', '#0040B0'],
    vars: { canvas: '#FFFFFF', white: '#FFFFFF', field: '#F2F2F2', line: '#C8C8C8', 'line-soft': '#E0E0E0', 'line-2': '#8A8A8A', ink: '#000000', 'ink-2': '#1F1F1F', 'ink-3': '#3D3D3D', 'ink-surface': '#111111', accent: '#0040B0', 'accent-hover': '#00308A', 'accent-soft': '#DCE6FA', 'on-accent': '#FFFFFF', clinic: '#005A55', 'clinic-soft': '#D6F0EC', ok: '#0F5A2C', 'ok-soft': '#D9EFE0', 'ok-tint': '#ECF7EF', 'ok-bright': '#1A8A48', warn: '#7A4100', 'warn-soft': '#F7E6CF', bad: '#A3121C', 'bad-text': '#8F0F18', 'bad-soft': '#FBDDDF', ai: '#64208A', 'ai-soft': '#EFE1F7', brand: '#B0103F', 'brand-soft': '#FBDCE6', 'on-solid': '#FFFFFF' },
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
  {
    id: 'e', mode: 'sepia', name: 'Petrol', hint: 'Kum zemin, petrol mavisi vurgu',
    swatch: ['#F7F1E3', '#FFFCF4', '#006E80'],
    vars: { canvas: '#F7F1E3', white: '#FFFCF4', field: '#EFE6D2', line: '#E2D6BC', 'line-soft': '#EBE2CD', 'line-2': '#CDBD9C', ink: '#1C2422', 'ink-2': '#404A47', 'ink-3': '#5A625E', 'ink-surface': '#283030', accent: '#006E80', 'accent-hover': '#005766', 'accent-soft': '#D6EAEC', 'on-accent': '#FFFFFF', clinic: '#2F6448', 'clinic-soft': '#DCEADD', ok: '#2C6748', 'ok-soft': '#DCEBDD', 'ok-tint': '#ECF4EC', 'ok-bright': '#3E8F5E', warn: '#8A5208', 'warn-soft': '#F6E3BF', bad: '#A92F2A', 'bad-text': '#962824', 'bad-soft': '#F6DCD3', ai: '#6E4180', 'ai-soft': '#EDE0EE', brand: '#B8324F', 'brand-soft': '#F6DCDF', 'on-solid': '#FFFFFF' },
  },
  {
    id: 'f', mode: 'sepia', name: 'Sepya kontrast', hint: 'Açık kâğıt zemin, koyu kahve metin ve vurgu (en okunaklı)',
    swatch: ['#FBF6EA', '#FFFDF6', '#3A2E1C'],
    vars: { canvas: '#FBF6EA', white: '#FFFDF6', field: '#F2EAD6', line: '#D9CBAE', 'line-soft': '#EAE0CA', 'line-2': '#A8987A', ink: '#140E06', 'ink-2': '#2E2618', 'ink-3': '#463C2C', 'ink-surface': '#221A10', accent: '#3A2E1C', 'accent-hover': '#241C10', 'accent-soft': '#EADFC9', 'on-accent': '#FFFFFF', clinic: '#1F5148', 'clinic-soft': '#D8E8DE', ok: '#205A36', 'ok-soft': '#D8E9D9', 'ok-tint': '#EAF3EA', 'ok-bright': '#2E7A4A', warn: '#704000', 'warn-soft': '#F3DDB5', bad: '#931F1A', 'bad-text': '#7F1A16', 'bad-soft': '#F4D6CC', ai: '#592F6B', 'ai-soft': '#E9DCEB', brand: '#9A2440', 'brand-soft': '#F4D8DC', 'on-solid': '#FFFFFF' },
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
    accents: OLED_ACCENTS,
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
    accents: GECE_MERCAN_ACCENTS,
    vars: {
      canvas: '#150F12', white: '#1F171B', field: '#2A1F25', line: '#33262D', 'line-soft': '#2A1F25', 'line-2': '#4A3841',
      ink: '#F3E9EC', 'ink-2': '#CDBDC3', 'ink-3': '#B7A3AA', 'ink-surface': '#2A1F25', accent: '#FF8F8F',
      'accent-hover': '#FFAAAA', 'accent-soft': '#3D1E22', 'on-accent': '#1E0809', clinic: '#5CCFC2', 'clinic-soft': '#0F2A29',
      ok: '#6CD99A', 'ok-soft': '#13291E', 'ok-tint': '#0E2017', 'ok-bright': '#4ADE80', warn: '#F2B865', 'warn-soft': '#33260F',
      bad: '#FF7A86', 'bad-text': '#FF9AA3', 'bad-soft': '#3D1A20', ai: '#D6A8FF', 'ai-soft': '#2B1E38', brand: '#FF6B95',
      'brand-soft': '#3E1726', 'on-solid': '#150F12',
    },
  },
  {
    id: 'g', mode: 'dark', name: 'Okyanus', hint: 'Derin petrol zemin, pembe vurgu',
    swatch: ['#0A171A', '#112226', '#FF9EDB'],
    vars: { canvas: '#0A171A', white: '#112226', field: '#182D32', line: '#21393F', 'line-soft': '#182D32', 'line-2': '#30505A', ink: '#E0EEF0', 'ink-2': '#B0C6CA', 'ink-3': '#8CA4A9', 'ink-surface': '#182D32', accent: '#FF9EDB', 'accent-hover': '#FFB9E5', 'accent-soft': '#3A1630', 'on-accent': '#1E0618', clinic: '#7AB4FF', 'clinic-soft': '#0F2238', ok: '#6CD99A', 'ok-soft': '#12291E', 'ok-tint': '#0D2018', 'ok-bright': '#4ADE80', warn: '#F0B865', 'warn-soft': '#2E2516', bad: '#F28585', 'bad-text': '#F59C9C', 'bad-soft': '#361C1F', ai: '#C9A6FF', 'ai-soft': '#261F38', brand: '#FF5C82', 'brand-soft': '#37161F', 'on-solid': '#061416' },
  },
  {
    id: 'h', mode: 'dark', name: 'Yüksek kontrast', hint: 'Siyaha yakın zemin, beyaz metin, sarı vurgu (en okunaklı)',
    swatch: ['#050505', '#121212', '#FFD24A'],
    vars: { canvas: '#050505', white: '#121212', field: '#1E1E1E', line: '#3A3A3A', 'line-soft': '#262626', 'line-2': '#5C5C5C', ink: '#FFFFFF', 'ink-2': '#E6E6E6', 'ink-3': '#C4C4C4', 'ink-surface': '#1E1E1E', accent: '#FFD24A', 'accent-hover': '#FFE07A', 'accent-soft': '#2E2608', 'on-accent': '#000000', clinic: '#5EEAD4', 'clinic-soft': '#0A2A26', ok: '#6EE7A0', 'ok-soft': '#0E2A1A', 'ok-tint': '#0A1F14', 'ok-bright': '#4ADE80', warn: '#FFB45C', 'warn-soft': '#33240C', bad: '#FF8080', 'bad-text': '#FF9C9C', 'bad-soft': '#3A1414', ai: '#D8B4FE', 'ai-soft': '#28183D', brand: '#FF6B95', 'brand-soft': '#3A1424', 'on-solid': '#000000' },
  },
];

/** Paletin geçerli vurgu seçeneği (yoksa/silinmişse ilk seçenek); vurgu seçeneği olmayan palette undefined. */
export const findAccent = (p: PaletteDef, id: string | undefined) => (p.accents ? p.accents.find((a) => a.id === id) || p.accents[0] : undefined);

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

/* ——— W01 Paleti düzenle: özel vurgu + kontrast kapısı ———
 * Kullanıcının seçtiği renk olduğu gibi kullanılmaz: vurgu, paletin üç zemininde (white/canvas/field) ve kendi yumuşak
 * zemininde ≥4.5:1 okunana dek açıklığı (OKLCH L) kaydırılır; üstündeki yazı (on) siyah/beyazdan kontrastı yüksek olan.
 * scripts/design/check-contrast.mjs bu işlevi de tarar (her ton × tema × palet). */
const lin = (c: number) => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
const hexRgb = (h: string) => { const n = parseInt(h.slice(1), 16); return [n >> 16, (n >> 8) & 255, n & 255]; };
const lumHex = (h: string) => { const [r, g, b] = hexRgb(h).map(lin); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
export const kontrastOrani = (a: string, b: string) => { const [x, y] = [lumHex(a), lumHex(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
const toOklch = (h: string) => {
  const [r, g, b] = hexRgb(h).map((c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; });
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b), m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b), s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  const L = 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s, A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s, B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;
  return [L, Math.hypot(A, B), Math.atan2(B, A)];
};
const fromOklch = (L: number, C: number, H: number): string => {
  // gamut dışına taşarsa kroma azaltılır
  for (let c = C; c >= 0; c -= 0.005) {
    const A = c * Math.cos(H), B = c * Math.sin(H);
    const l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3, m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3, s = (L - 0.0894841775 * A - 1.291485548 * B) ** 3;
    const rgb = [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s, -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s];
    if (rgb.every((v) => v >= -0.0005 && v <= 1.0005)) {
      return '#' + rgb.map((v) => { v = Math.min(1, Math.max(0, v)); const e = v <= 0.0031308 ? 12.92 * v : 1.055 * v ** (1 / 2.4) - 0.055; return Math.round(e * 255).toString(16).padStart(2, '0'); }).join('').toUpperCase();
    }
  }
  return L > 0.5 ? '#FFFFFF' : '#000000';
};
const karis = (a: string, b: string, t: number) => { const x = hexRgb(a), y = hexRgb(b); return '#' + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, '0')).join('').toUpperCase(); };
export function ozelVurgu(hex: string, v: Pick<Record<TokenKey, string>, 'white' | 'canvas' | 'field'>, mode: ThemeMode): AccentDef {
  const koyu = mode === 'dark';
  const [L0, C, H] = toOklch(/^#[0-9a-f]{6}$/i.test(hex) ? hex : '#2F6FED');
  const zeminler = [v.white, v.canvas, v.field];
  let accent = fromOklch(L0, C, H), L = L0;
  const gecer = (a: string, soft: string) => zeminler.every((z) => kontrastOrani(a, z) >= 4.6) && kontrastOrani(a, soft) >= 4.6;
  const softOf = (a: string) => karis(v.white, a, koyu ? 0.2 : 0.12);
  for (let i = 0; i < 120 && !gecer(accent, softOf(accent)); i++) { L = koyu ? Math.min(0.99, L + 0.005) : Math.max(0.05, L - 0.005); accent = fromOklch(L, C, H); }
  const soft = softOf(accent);
  const hover = fromOklch(koyu ? Math.min(0.99, L + 0.05) : Math.max(0.05, L - 0.05), C, H);
  const on = [kontrastOrani('#FFFFFF', accent), kontrastOrani('#000000', accent)];
  // on: hover zemininde de okunmalı
  const onRenk = Math.min(on[0], kontrastOrani('#FFFFFF', hover)) >= Math.min(on[1], kontrastOrani('#000000', hover)) ? '#FFFFFF' : '#000000';
  return { id: 'ozel', name: 'Özel', accent, hover, soft, on: onRenk };
}

/** Palet CSS'ini üretir (Node betikleri ve tarayıcı aynı çıktıyı kullanır). */
export function buildPaletteCss(): string {
  const blocks = PALETTES.map((p) => {
    const body = TOKEN_KEYS.map((k) => `--color-${k}: ${p.vars[k]};`).join(' ');
    // (0,4,1): appearance.css (0,3,1) ve health.css/index.css eski token bloklarını her zaman ezer
    return `html:root.ui-v7[data-mode="${p.mode}"][data-palette="${p.id}"] { ${body} --ui-focus: ${p.vars.accent}; --color-teal-600: ${p.vars.accent}; }`;
  });
  // Vurgu seçenekleri (0,5,1): palet bloğunu ezer; ilk seçenek paletin kendisi olduğu için blok üretilmez
  const accents = PALETTES.flatMap((p) => (p.accents || []).slice(1).map((a) =>
    `html:root.ui-v7[data-mode="${p.mode}"][data-palette="${p.id}"][data-accent="${a.id}"] { --color-accent: ${a.accent}; --color-accent-hover: ${a.hover}; --color-accent-soft: ${a.soft}; --color-on-accent: ${a.on}; --ui-focus: ${a.accent}; --color-teal-600: ${a.accent}; }`));
  return [...blocks, ...accents].join('\n') + MODE_CSS;
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
