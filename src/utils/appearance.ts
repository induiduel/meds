import { useSyncExternalStore } from 'react';
import { PALETTES, findAccent, findPalette, installPaletteStyles, ozelVurgu, type AccentDef, type ThemeMode } from './palettes';
import { refreshZoomGuard } from './uiZoom';

/**
 * Görünüm tercihleri: tema (açık / sarı / koyu), her temada dört palet (a–d, utils/palettes.ts) ve yerleşim yoğunluğu.
 * Kök öğeye `data-mode`, `data-palette`, `data-density`, `data-layout` yazılır; koyu temada eski `theme-dark` sınıfı da kalır
 * (index.css ve health.css'teki koyu kurallar onu kullanır). Token değerleri styles/appearance.css'tedir.
 */
export type { ThemeMode } from './palettes';
/** Palet kimliği: utils/palettes.ts kaydındaki `id` (a, b, c, …) — yeni palet eklemek için o listeye bakın. */
export type Palette = string;
export type Density = 'compact' | 'normal' | 'wide';
/**
 * Görüntüleme modu (v10) — sayfa iskeleti: Akış (tek sütun, dar okuma genişliği, menü şeridi), Pano (geniş ızgara,
 * açık menü), Odak (tam genişlik, menü şeridi; liste + ayrıntı bölmeli sayfalar için). Telefonda üçü de tek sütundur.
 * Kök öğeye `data-layout` yazılır; kurallar styles/layout-modes.css.
 */
export type LayoutMode = 'akis' | 'pano' | 'odak';
/** v11 okuma ve kullanım tercihleri (kök öğeye data-* olarak yazılır; kurallar styles/v11.css) */
export type ReadingFont = 'serif' | 'sans' | 'kitap' | 'klasik' | 'roboto';
export const READING_ORDER: ReadingFont[] = ['serif', 'sans', 'kitap', 'klasik', 'roboto'];
/** Okuma yazısı boyutu (soru kökü, şıklar, ders anlatımı, kartlar, okuyucular): 14 → 20 px, beş adım */
export type TextSize = 'xs' | 's' | 'm' | 'l' | 'xl';
export const TEXT_SIZE_ORDER: TextSize[] = ['xs', 's', 'm', 'l', 'xl'];
export const TEXT_SIZE_PX: Record<TextSize, number> = { xs: 14, s: 15, m: 16, l: 18, xl: 20 };
/** Serbest yazı boyutu (profildeki kaydırıcı): 6–20 px, 1 px adım. `textSize` en yakın adımı tutar (eski kurallar için). */
export const TEXT_PX_MIN = 12; // v12'de tüm tasarımı ölçekler (px/16); 12 altı arayüzü kullanılamaz kılar
export const TEXT_PX_MAX = 20;
export const clampTextPx = (n: number) => Math.min(TEXT_PX_MAX, Math.max(TEXT_PX_MIN, Math.round(n)));
export const nearestTextSize = (px: number): TextSize =>
  TEXT_SIZE_ORDER.reduce((b, k) => (Math.abs(TEXT_SIZE_PX[k] - px) < Math.abs(TEXT_SIZE_PX[b] - px) ? k : b), 'xs' as TextSize);
/** Basit: yalnız hızlı süzgeç hapları; Gelişmiş: "Süzgeç" sayfası da görünür */
export type FilterMode = 'basit' | 'gelismis';
export type MotionPref = 'full' | 'reduced';
/** Tasarım dili: v12 Net (varsayılan), v11 Sade, v10 Klasik — eski tasarımlar silinmez, profilden geri dönülebilir.
 *  v12, v11'in sayfa yapısını devralır (CSS `:root:is([data-design='v11'],[data-design='v12'])`) ve üstüne styles/v12.css katmanını koyar. */
export type DesignVersion = 'v12' | 'v11' | 'v10';
export const DESIGN_ORDER: DesignVersion[] = ['v12', 'v11', 'v10'];
/** v11 yapısını kullanan tasarımlar (v11 ve v12) */
export const isSadeFamily = (d: DesignVersion) => d !== 'v10';
/**
 * v13 "Ada": v12'nin sayfa mantığını ve bileşenlerini kullanır (design = 'v12' kalır, v12 dalları çalışır) ama
 * iskeleti kendine aittir — yüzen kenar adası, sütun içi başlık kapsülü, telefonda yüzen alt ada; tam genişlik
 * şerit yok. Kök öğeye `data-v13="on"` yazılır; kurallar styles/v13/*.css, kabuk components/v13/ShellV13.tsx.
 * Seçim isteğe bağlıdır: ilk açılışta bir kez sorulur (components/v13/V13Invite.tsx), Ayarlar › Tasarım'dan değişir.
 */
/**
 * v15: tasarım sistemi "MeDSor Tasarım Sistemi v15" (artifact D8pMJwGTeeGG5y9jwtpurR). v13 gibi v12 sayfa bileşenleri
 * üstünde çalışır (design = 'v12'); kök öğeye `data-v15="on"` yazılır. Kabuk components/v15/ShellV15.tsx, stiller
 * styles/v15/*.css; sayfalar aşama aşama v15 düzenine taşınır (docs/V15_PLAN.md). v13 ile birlikte açık olamaz.
 */
export type DesignChoice = 'v15' | 'v13' | DesignVersion;
export const DESIGN_CHOICES: DesignChoice[] = ['v15', 'v13', 'v12', 'v11', 'v10'];
export const DESIGN_CHOICE_LABELS: Record<DesignChoice, string> = { v15: 'Yalın (v15)', v13: 'Ada (v13)', v12: 'Net (v12)', v11: 'Sade (v11)', v10: 'Klasik (v10)' };
export const designChoiceOf = (a: Pick<Appearance, 'design' | 'v13' | 'v15'>): DesignChoice =>
  a.design === 'v12' && a.v15 ? 'v15' : a.design === 'v12' && a.v13 ? 'v13' : a.design;

/** Çıkmış soru kartı: tam (varsayılan) · katlanır (yalnız kök + künye, dokununca şıklar) · dar (sıkı şıklar) */
export type QCardMode = 'tam' | 'katlanir' | 'dar';
export const QCARD_MODE_LABELS: Record<QCardMode, string> = { tam: 'Tam', katlanir: 'Katlanır', dar: 'Dar şıklar' };
export interface QCardPrefs {
  mode: QCardMode;
  kurul: boolean;
  ders: boolean;
  yil: boolean;
  /** Açıklama düğmesi ve gövdesi */
  aciklama: boolean;
  /** Açıklamadaki şık şık analiz */
  sikAciklama: boolean;
}
export const QCARD_DEFAULTS: QCardPrefs = { mode: 'tam', kurul: true, ders: true, yil: true, aciklama: true, sikAciklama: true };
const readQCard = (v: any): QCardPrefs => {
  const o = v && typeof v === 'object' ? v : {};
  const b = (k: keyof QCardPrefs) => (typeof o[k] === 'boolean' ? o[k] : (QCARD_DEFAULTS[k] as boolean));
  return {
    mode: o.mode === 'katlanir' || o.mode === 'dar' ? o.mode : 'tam',
    kurul: b('kurul'), ders: b('ders'), yil: b('yil'), aciklama: b('aciklama'), sikAciklama: b('sikAciklama'),
  };
};

export interface Appearance {
  mode: ThemeMode;
  /** Her tema kendi palet seçimini hatırlar: koyuya geçip dönünce açık tema paleti kaybolmaz. */
  palettes: Record<ThemeMode, Palette>;
  density: Density;
  layout: LayoutMode;
  reading: ReadingFont;
  textSize: TextSize;
  /** Yazı boyutu, px (12–20); v12 tüm tasarımı px/16 oranında ölçekler; kök öğeye --read-size olarak yazılır */
  textPx: number;
  filters: FilterMode;
  /** Çıkmış/örnek soru kartlarında işaret etiketleri (varsayılan gizli) */
  qtags: boolean;
  /** Çıkmış soru kartı modu ve görünür alanları */
  qcard: QCardPrefs;
  motion: MotionPref;
  design: DesignVersion;
  /** Kullanıcı tasarımı Ayarlar'dan bilerek seçti mi (seçmediyse eski varsayılan 'v11' v12'ye taşınır) */
  designPicked?: boolean;
  /** v11 → v12 taşımasının zamanı (taşınan değerin profil eşitlemesiyle sunucuya gitmesi için kayıt değişir) */
  designMigratedAt?: number;
  /** v13 "Ada" iskeleti açık mı (design === 'v12' iken geçerli) */
  v13?: boolean;
  /** v13 daveti cevaplandı mı (bir kez sorulur) */
  v13Asked?: boolean;
  /** v15 kabuğu ve sayfaları açık mı (design === 'v12' iken geçerli; v13 ile birlikte açık olmaz) */
  v15?: boolean;
  /** Vurgu rengi seçimi, "<tema>:<palet>" anahtarıyla (yalnız `accents` tanımlı paletler; utils/palettes.ts) */
  accents?: Record<string, string>;
  /** W01 Paleti düzenle: "<tema>:<palet>" başına özel vurgu (#RRGGBB). Uygulanırken kontrast kapısından geçirilir (ozelVurgu). */
  customAccents?: Record<string, string>;
  /** V03 Tıbbi arka plan motifi (yalnız zemin dokusu, %6 opaklık; metnin altında kalır) */
  motif?: MotifId;
  /** V04 Yazı tipleri: arayüz ve okuma yazısı (FONT_LIST kimliği; boş = tasarımın varsayılanı) */
  fontUi?: string;
  fontRead?: string;
}

export type MotifId = 'yok' | 'ekg' | 'hex' | 'hucre' | 'dna' | 'arti' | 'damar';
export const MOTIFS: { id: MotifId; name: string; hint: string }[] = [
  { id: 'yok', name: 'Motif yok', hint: 'Düz zemin' },
  { id: 'ekg', name: 'EKG çizgisi', hint: 'Kardiyoloji, başlıklar' },
  { id: 'hex', name: 'Molekül', hint: 'Biyokimya, farmakoloji' },
  { id: 'hucre', name: 'Hücre', hint: 'Hücre, patoloji' },
  { id: 'dna', name: 'DNA sarmalı', hint: 'Genetik' },
  { id: 'arti', name: 'Tıp artısı', hint: 'Acil, KMB' },
  { id: 'damar', name: 'Damar ağı', hint: 'Fizyoloji, dolaşım' },
];
const isMotif = (v: unknown): v is MotifId => MOTIFS.some((m) => m.id === v);

/** V04: seçilebilir yazı tipleri. g = Google Fonts aile parametresi (seçilince yüklenir; yerel/varsayılan olanlarda yok). */
export interface FontDef { id: string; name: string; hint: string; kind: 'ui' | 'read'; family: string; g?: string }
export const FONT_LIST: FontDef[] = [
  { id: 'jakarta', name: 'Plus Jakarta Sans', hint: 'Arayüz · varsayılan', kind: 'ui', family: "'Plus Jakarta Sans', 'Geist', system-ui, sans-serif", g: 'Plus+Jakarta+Sans:wght@400;500;600;700' },
  { id: 'inter', name: 'Inter', hint: 'Arayüz · nötr', kind: 'ui', family: 'Inter, system-ui, sans-serif', g: 'Inter:wght@400;500;600;700' },
  { id: 'plex', name: 'IBM Plex Sans', hint: 'Arayüz · teknik, tablolar', kind: 'ui', family: "'IBM Plex Sans', system-ui, sans-serif", g: 'IBM+Plex+Sans:wght@400;500;600;700' },
  { id: 'lexend', name: 'Lexend', hint: 'Okuma güçlüğü', kind: 'ui', family: 'Lexend, system-ui, sans-serif', g: 'Lexend:wght@400;500;600;700' },
  { id: 'atkinson', name: 'Atkinson Hyperlegible', hint: 'Az görme · ayırt edici', kind: 'ui', family: "'Atkinson Hyperlegible', system-ui, sans-serif", g: 'Atkinson+Hyperlegible:wght@400;700' },
  { id: 'nunito', name: 'Nunito', hint: 'Yuvarlak, sıcak', kind: 'ui', family: 'Nunito, system-ui, sans-serif', g: 'Nunito:wght@400;500;600;700' },
  { id: 'newsreader', name: 'Newsreader', hint: 'Okuma · varsayılan', kind: 'read', family: "'Newsreader', 'Literata', Georgia, serif", g: 'Newsreader:opsz,wght@6..72,400;6..72,600' },
  { id: 'sourceserif', name: 'Source Serif 4', hint: 'Okuma · uzun metin', kind: 'read', family: "'Source Serif 4', Georgia, serif", g: 'Source+Serif+4:opsz,wght@8..60,400;8..60,600' },
  { id: 'literata', name: 'Literata', hint: 'Okuma · e-kitap', kind: 'read', family: 'Literata, Georgia, serif' },
  { id: 'merriweather', name: 'Merriweather', hint: 'Okuma · küçük ekran', kind: 'read', family: 'Merriweather, Georgia, serif', g: 'Merriweather:wght@400;700' },
  { id: 'lora', name: 'Lora', hint: 'Notlar', kind: 'read', family: 'Lora, Georgia, serif', g: 'Lora:wght@400;600' },
  { id: 'plexmono', name: 'IBM Plex Mono', hint: 'Doz, değer, kod', kind: 'read', family: "'IBM Plex Mono', ui-monospace, monospace", g: 'IBM+Plex+Mono:wght@400;600' },
];
const findFont = (id: string | undefined, kind: 'ui' | 'read') => FONT_LIST.find((f) => f.id === id && f.kind === kind);
function loadFont(f: FontDef | undefined) {
  if (!f?.g || typeof document === 'undefined') return;
  const id = `font-${f.id}`;
  if (document.getElementById(id)) return;
  const l = document.createElement('link');
  l.id = id; l.rel = 'stylesheet'; l.href = `https://fonts.googleapis.com/css2?family=${f.g}&display=swap`;
  document.head.appendChild(l);
}

export const MODE_LABELS: Record<ThemeMode, string> = { light: 'Açık', sepia: 'Sarı', dark: 'Koyu' };
export const LAYOUT_LABELS: Record<LayoutMode, string> = { akis: 'Akış', pano: 'Pano', odak: 'Odak' };
export const READING_LABELS: Record<ReadingFont, string> = { serif: 'Tırnaklı', sans: 'Düz', kitap: 'Kitap', klasik: 'Klasik', roboto: 'Roboto' };
export const TEXT_SIZE_LABELS: Record<TextSize, string> = { xs: 'En küçük', s: 'Küçük', m: 'Orta', l: 'Büyük', xl: 'En büyük' };
export const FILTER_MODE_LABELS: Record<FilterMode, string> = { basit: 'Basit', gelismis: 'Gelişmiş' };
const V11_DEFAULTS = { v15: true, reading: 'serif' as ReadingFont, textSize: 'm' as TextSize, textPx: 16, filters: 'basit' as FilterMode, qtags: false, qcard: QCARD_DEFAULTS, motion: 'full' as MotionPref, design: 'v12' as DesignVersion };
export const DESIGN_LABELS: Record<DesignVersion, string> = { v12: 'Net (v12)', v11: 'Sade (v11)', v10: 'Klasik (v10)' };
export const DENSITY_LABELS: Record<Density, string> = { compact: 'Kompakt', normal: 'Normal', wide: 'Geniş' };
/** Geriye dönük uyumluluk: tema → palet kimliği → bilgi (kayıttan üretilir). */
export const PALETTE_INFO: Record<ThemeMode, Record<string, { name: string; hint: string; swatch: [string, string, string] }>> =
  PALETTES.reduce((acc, p) => {
    (acc[p.mode] ||= {})[p.id] = { name: p.name, hint: p.hint, swatch: p.swatch };
    return acc;
  }, {} as Record<ThemeMode, Record<string, { name: string; hint: string; swatch: [string, string, string] }>>);

const KEY = 'medsoru_appearance';
const LEGACY_THEME_KEY = 'medsoru_theme';
const listeners = new Set<() => void>();

/**
 * v11 önceki varsayılandı: bilerek seçilmemiş 'v11' v12'ye taşınır (Klasik v10 ve bilerek seçilen v11 kalır).
 * Taşıma bilgisi görünüm kaydının içindedir (designPicked); ayrı bir yerel bayrak tutulmaz — aksi halde profil
 * eşitlemesi sunucudaki eski 'v11' kaydını geri yazınca bayrak taşımayı engelliyor ve kullanıcı v11'de kalıyordu.
 */
let migratedThisLoad = false;
function migrateDesign(p: Partial<Appearance>): DesignVersion {
  const d = p.design;
  if (d === 'v10' || d === 'v12') return d;
  if (d === 'v11') {
    if (p.designPicked) return 'v11';
    migratedThisLoad = true;
    return 'v12';
  }
  return 'v12';
}

function read(): Appearance {
  // İlk açılış her zaman açık temadır (sistem koyu olsa bile); kullanıcı Ayarlar'dan değiştirir.
  const fallback: Appearance = { mode: 'light', palettes: { light: 'a', sepia: 'a', dark: 'a' }, density: 'normal', layout: 'pano', ...V11_DEFAULTS };
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) {
      const p = JSON.parse(raw) as Partial<Appearance>;
      const out: Appearance = {
        mode: p.mode === 'light' || p.mode === 'sepia' || p.mode === 'dark' ? p.mode : fallback.mode,
        // Kayıtta olmayan (silinmiş) palet seçimi temanın ilk paletine döner
        palettes: (['light', 'sepia', 'dark'] as ThemeMode[]).reduce((acc, m) => {
          acc[m] = findPalette(m, (p.palettes || {})[m]).id;
          return acc;
        }, {} as Record<ThemeMode, Palette>),
        density: p.density === 'compact' || p.density === 'wide' || p.density === 'normal' ? p.density : 'normal',
        layout: p.layout === 'akis' || p.layout === 'odak' || p.layout === 'pano' ? p.layout : 'pano',
        reading: (READING_ORDER as string[]).includes(String(p.reading)) ? (p.reading as ReadingFont) : 'serif',
        textSize: (TEXT_SIZE_ORDER as string[]).includes(String(p.textSize)) ? (p.textSize as TextSize) : 'm',
        textPx: typeof p.textPx === 'number' && isFinite(p.textPx)
          ? clampTextPx(p.textPx)
          : TEXT_SIZE_PX[(TEXT_SIZE_ORDER as string[]).includes(String(p.textSize)) ? (p.textSize as TextSize) : 'm'],
        filters: p.filters === 'gelismis' ? 'gelismis' : 'basit',
        qtags: p.qtags === true,
        qcard: readQCard(p.qcard),
        motion: p.motion === 'reduced' ? 'reduced' : 'full',
        design: migrateDesign(p),
        designPicked: p.designPicked === true,
        designMigratedAt: typeof p.designMigratedAt === 'number' ? p.designMigratedAt : undefined,
        accents: p.accents && typeof p.accents === 'object' ? { ...p.accents } : {},
        v13: p.v13 === true && p.v15 !== true,
        // v15 kullanıcılar için varsayılan (2026-10-27): tasarımı bilerek seçmeyen herkes v15'e geçer
        v15: p.v15 === true || (!p.designPicked && p.v15 !== false && p.v13 !== true && migrateDesign(p) === 'v12'),
        v13Asked: p.v13Asked === true,
        customAccents: p.customAccents && typeof p.customAccents === 'object'
          ? Object.fromEntries(Object.entries(p.customAccents).filter(([, v]) => typeof v === 'string' && /^#[0-9a-f]{6}$/i.test(v))) : {},
        motif: isMotif(p.motif) ? p.motif : 'yok',
        fontUi: findFont(p.fontUi, 'ui')?.id,
        fontRead: findFont(p.fontRead, 'read')?.id,
      };
      // Taşınan tasarım seçimi kalıcı olsun (aksi halde sonraki açılışta v11'e döner)
      if (out.design !== p.design) { try { localStorage.setItem(KEY, JSON.stringify(out)); } catch { /* ignore */ } }
      return out;
    }
    // Eski açık/koyu tercihi bir kez taşınır
    const legacy = localStorage.getItem(LEGACY_THEME_KEY);
    if (legacy === 'light' || legacy === 'dark') return { ...fallback, mode: legacy };
  } catch {
    /* ignore */
  }
  return fallback;
}

let current: Appearance = typeof window === 'undefined'
  ? { mode: 'light', palettes: { light: 'a', sepia: 'a', dark: 'a' }, density: 'normal', layout: 'pano', ...V11_DEFAULTS }
  : read();

if (typeof window !== 'undefined') {
  // Taşınan seçim, profil eşitleme izleyicisi kurulduktan sonra bir kez daha (farklı içerikle) yazılır ki "değişti"
  // sayılıp sunucuya gitsin; yoksa sunucudaki eski 'v11' her açılışta geri gelir.
  if (migratedThisLoad) {
    window.setTimeout(() => {
      try {
        current = { ...current, designMigratedAt: Date.now() };
        localStorage.setItem(KEY, JSON.stringify(current));
      } catch { /* gizli pencere */ }
    }, 4000);
  }
  // Başka sekme ya da profil eşitlemesi görünüm kaydını değiştirirse anında uygula
  window.addEventListener('storage', (e) => {
    if (e.key !== KEY) return;
    const next = read();
    if (JSON.stringify(next) === JSON.stringify(current)) return;
    current = next;
    applyAppearance(current);
    listeners.forEach((l) => l());
  });
}

/** Kök öğeye tercihleri yazar (anında, geçişsiz). Açılışta ve örtü altındaki geçişte kullanılır. */
export function applyAppearance(a: Appearance = current) {
  installPaletteStyles();
  const el = document.documentElement;
  el.dataset.mode = a.mode;
  el.dataset.palette = a.palettes[a.mode];
  const acc = findAccent(findPalette(a.mode, a.palettes[a.mode]), a.accents?.[`${a.mode}:${a.palettes[a.mode]}`]);
  if (acc) el.dataset.accent = acc.id; else delete el.dataset.accent;
  el.dataset.density = a.density;
  el.dataset.layout = a.layout;
  el.dataset.reading = a.reading;
  el.dataset.textSize = a.textSize;
  // Serbest boyut: satır içi değişken data-text-size kurallarını ezer (6–20 px)
  const px = clampTextPx(a.textPx ?? TEXT_SIZE_PX[a.textSize]);
  // v12: yazı boyutu tüm tasarımı ölçekler (zoom = px/16, styles/v12.css); okuma yazısı tabanda kalır, çifte büyümesin
  el.style.setProperty('--read-size', a.design === 'v12' ? '16px' : `${px}px`);
  el.style.setProperty('--txt-zoom', a.design === 'v12' ? String(px / 16) : '1');
  el.dataset.filters = a.filters;
  el.dataset.qtags = a.qtags ? 'on' : 'off';
  el.dataset.motion = a.motion;
  el.dataset.design = a.design;
  if (a.design === 'v12' && a.v13 && !a.v15) el.dataset.v13 = 'on'; else delete el.dataset.v13;
  if (a.design === 'v12' && a.v15) el.dataset.v15 = 'on'; else delete el.dataset.v15;
  // W01 özel vurgu: kontrast kapısından geçmiş değerler satır içi yazılır (palet/vurgu bloklarını ezer)
  const ozelKey = `${a.mode}:${a.palettes[a.mode]}`;
  const ozel = a.customAccents?.[ozelKey] ? ozelVurgu(a.customAccents[ozelKey], findPalette(a.mode, a.palettes[a.mode]).vars, a.mode) : null;
  const OZEL_VARS: [string, keyof AccentDef][] = [['--color-accent', 'accent'], ['--color-accent-hover', 'hover'], ['--color-accent-soft', 'soft'], ['--color-on-accent', 'on'], ['--ui-focus', 'accent'], ['--color-teal-600', 'accent']];
  for (const [v, k] of OZEL_VARS) { if (ozel) el.style.setProperty(v, ozel[k]); else el.style.removeProperty(v); }
  if (ozel) el.dataset.ozelVurgu = 'on'; else delete el.dataset.ozelVurgu;
  // V03 motif
  if (a.motif && a.motif !== 'yok') el.dataset.motif = a.motif; else delete el.dataset.motif;
  // V04 yazı tipleri (seçilmediyse tasarımın kendi değişkenleri geçerli)
  const fu = findFont(a.fontUi, 'ui'), fr = findFont(a.fontRead, 'read');
  loadFont(fu); loadFont(fr);
  for (const v of ['--font-sans', '--font-display']) { if (fu) el.style.setProperty(v, fu.family); else el.style.removeProperty(v); }
  for (const v of ['--font-read', '--read-font']) { if (fr) el.style.setProperty(v, fr.family); else el.style.removeProperty(v); }
  el.classList.toggle('theme-dark', a.mode === 'dark');
  el.style.colorScheme = a.mode === 'dark' ? 'dark' : 'light';
  syncPwaChrome(a);
  // Ölçek tavanı: dar alanda zoom düzeni kırmasın (utils/uiZoom.ts)
  refreshZoomGuard();
}

/*
 * PWA kromu temayı izler: tarayıcı/durum çubuğu (meta theme-color) üst çubuğun rengini alır, kurulu uygulamanın
 * manifestosu (theme_color = çubuk, background_color = açılış ekranı zemini) sunucuda bu renklerle üretilir
 * (server.ts serveManifest ?tc=&bg=), iOS durum çubuğu yazısı koyu temada açık, açık/sarı temada koyu olur.
 * Son renkler PWA_KEY'e yazılır; index.html'deki erken betik bunları boyamadan önce uygular (açılışta renk sıçraması yok).
 */
const PWA_KEY = 'medsoru_pwa_chrome';
const hex6 = (v: string) => {
  const m = v.trim().match(/^#([0-9a-f]{6})$/i) || v.trim().match(/^#([0-9a-f])([0-9a-f])([0-9a-f])$/i);
  if (!m) return '';
  return m.length === 4 ? `${m[1]}${m[1]}${m[2]}${m[2]}${m[3]}${m[3]}`.toUpperCase() : m[1].toUpperCase();
};
export const pwaManifestHref = (tc: string, bg: string) => `/manifest.json?v=9&tc=${tc}&bg=${bg}`;

function syncPwaChrome(a: Appearance) {
  const cs = getComputedStyle(document.documentElement);
  // v12 üst/alt çubuğu yüzey rengindedir (--color-white); Klasik/Sade üst çubuğu zemin rengindedir
  // v13'te tam genişlik çubuk yok: tarayıcı kromu zemin rengini alır
  const tc = hex6(cs.getPropertyValue(a.design === 'v12' && !a.v13 && !a.v15 ? '--color-white' : '--color-canvas'));
  const bg = hex6(cs.getPropertyValue('--color-canvas'));
  if (!tc || !bg) return;
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', `#${tc}`);
  const isIos =
    /iPhone|iPad|iPod/i.test(navigator.userAgent) ||
    (/Macintosh/i.test(navigator.userAgent) && navigator.maxTouchPoints > 1);
  // iOS Ana Ekran PWA'da black-translucent + viewport-fit=cover tam ekran (edge-to-edge) görünüm sağlar;
  // manifest href'in dinamik değiştirilmesi ise WebKit'in "Ana Ekrana Ekle" sırasında manifest okumasını kesebilir.
  document.querySelector('meta[name="apple-mobile-web-app-status-bar-style"]')
    ?.setAttribute('content', 'black-translucent');
  if (!isIos) {
    const link = document.querySelector<HTMLLinkElement>('link[rel="manifest"]');
    const href = pwaManifestHref(tc, bg);
    if (link && link.getAttribute('href') !== href) link.setAttribute('href', href);
  }
  try { localStorage.setItem(PWA_KEY, JSON.stringify({ tc, bg, dark: a.mode === 'dark' })); } catch { /* ignore */ }
}

/*
 * Tema geçişi: eskiden her öğeye (`*`) renk geçişi veriliyordu; binlerce öğede aynı anda geçiş hem takılıyor hem de
 * kendi geçişi olan / satır içi renkli öğeler yarım kalıyordu. Şimdi: örtü (yükleniyor ekranı) eski zeminle açılır →
 * altında tema geçişsiz, tek seferde uygulanır ve React dinleyicileri o anda bildirilir → örtünün zemini yeni temaya
 * akar → örtü söner. Dönen halka transform animasyonu olduğundan stil hesabı sırasında da akıcı kalır.
 */
const COVER_IN = 180;
const COVER_HOLD = 340;
const COVER_OUT = 280;
let pendingApply: Appearance | null = null;
let switching = false;
const wait = (ms: number) => new Promise<void>((r) => window.setTimeout(r, ms));
// Arka plan sekmesinde/gizli görünümde rAF durur: 120 ms sonra yine de devam et (yoksa tema geçişi yarıda takılır
// ve sonraki tema seçimleri kuyrukta kalırdı)
const nextFrame = () => new Promise<void>((r) => {
  let done = false;
  const fin = () => { if (!done) { done = true; r(); } };
  requestAnimationFrame(() => requestAnimationFrame(fin));
  window.setTimeout(fin, 120);
});

function coverLabel(a: Appearance) {
  return `${MODE_LABELS[a.mode]} · ${findPalette(a.mode, a.palettes[a.mode]).name}`;
}

function ensureCover(): HTMLElement {
  let cover = document.getElementById('theme-cover');
  if (cover) return cover;
  cover = document.createElement('div');
  cover.id = 'theme-cover';
  cover.className = 'theme-cover';
  cover.setAttribute('role', 'status');
  cover.setAttribute('aria-live', 'polite');
  cover.innerHTML = '<div class="theme-cover-box"><span class="theme-cover-ring" aria-hidden="true"></span><b>Tema uygulanıyor</b><small></small></div>';
  document.body.appendChild(cover);
  return cover;
}

function commit(a: Appearance) {
  const el = document.documentElement;
  el.classList.add('theme-switching');
  applyAppearance(a);
  listeners.forEach((l) => l());
}

async function switchAppearance(next: Appearance) {
  pendingApply = next;
  if (switching) return; // Sürmekte olan geçiş en son seçimi örtü altında uygular
  const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !document.body) {
    pendingApply = null;
    commit(next);
    requestAnimationFrame(() => document.documentElement.classList.remove('theme-switching'));
    return;
  }
  switching = true;
  const el = document.documentElement;
  const cover = ensureCover();
  const small = cover.querySelector('small');
  try {
    if (small) small.textContent = coverLabel(next);
    cover.hidden = false;
    void cover.offsetWidth;
    cover.classList.add('is-on');
    await wait(COVER_IN);
    while (pendingApply) {
      const a = pendingApply;
      pendingApply = null;
      if (small) small.textContent = coverLabel(a);
      commit(a);
      void getComputedStyle(el).getPropertyValue('--color-canvas'); // stil hesabını örtü altında bitir
      await nextFrame();
      await wait(COVER_HOLD);
    }
    el.classList.remove('theme-switching');
    cover.classList.remove('is-on');
    await wait(COVER_OUT);
    if (!pendingApply) cover.hidden = true;
  } finally {
    switching = false;
    el.classList.remove('theme-switching');
    if (pendingApply) void switchAppearance(pendingApply);
  }
}

export function setAppearance(patch: Partial<Omit<Appearance, 'palettes' | 'accents' | 'qcard' | 'customAccents'>> & { qcard?: Partial<QCardPrefs>; palette?: Palette; accent?: string; customAccent?: string | null; choice?: DesignChoice }) {
  const next: Appearance = { ...current, palettes: { ...current.palettes }, accents: { ...(current.accents || {}) } };
  if (patch.mode) next.mode = patch.mode;
  if (patch.density) next.density = patch.density;
  if (patch.layout) next.layout = patch.layout;
  if (patch.reading) { next.reading = patch.reading; next.fontRead = undefined; }
  if (patch.motif) next.motif = patch.motif;
  if ('fontUi' in patch) next.fontUi = findFont(patch.fontUi, 'ui')?.id;
  if ('fontRead' in patch && !patch.reading) next.fontRead = findFont(patch.fontRead, 'read')?.id;
  if (patch.textSize) { next.textSize = patch.textSize; next.textPx = TEXT_SIZE_PX[patch.textSize]; }
  if (typeof patch.textPx === 'number' && isFinite(patch.textPx)) { next.textPx = clampTextPx(patch.textPx); next.textSize = nearestTextSize(next.textPx); }
  if (patch.filters) next.filters = patch.filters;
  if (typeof patch.qtags === 'boolean') next.qtags = patch.qtags;
  if (patch.qcard) next.qcard = readQCard({ ...next.qcard, ...patch.qcard });
  if (patch.motion) next.motion = patch.motion;
  if (patch.design) { next.design = patch.design; next.designPicked = true; if (patch.design !== 'v12') { next.v13 = false; next.v15 = false; } }
  if (patch.choice) {
    next.design = patch.choice === 'v13' || patch.choice === 'v15' ? 'v12' : patch.choice;
    next.v13 = patch.choice === 'v13';
    next.v15 = patch.choice === 'v15';
    next.designPicked = true;
    next.v13Asked = true;
  }
  if (typeof patch.v13 === 'boolean') { next.v13 = patch.v13; if (patch.v13) next.v15 = false; }
  if (typeof patch.v15 === 'boolean') { next.v15 = patch.v15; if (patch.v15) next.v13 = false; }
  if (typeof patch.v13Asked === 'boolean') next.v13Asked = patch.v13Asked;
  if (patch.palette) next.palettes[next.mode] = patch.palette;
  // Vurgu rengi: örtüsüz, anında (yalnız 4 token değişir). Hazır vurgu seçilince o paletin özel rengi kalkar.
  // customAccent: '#RRGGBB' özel renk, null = sıfırla
  if (patch.accent || patch.customAccent !== undefined) {
    const k = `${next.mode}:${next.palettes[next.mode]}`;
    next.customAccents = { ...(current.customAccents || {}) };
    if (patch.accent) { next.accents![k] = patch.accent; delete next.customAccents[k]; }
    if (patch.customAccent === null) delete next.customAccents[k];
    else if (typeof patch.customAccent === 'string' && /^#[0-9a-f]{6}$/i.test(patch.customAccent)) next.customAccents[k] = patch.customAccent.toUpperCase();
    current = next;
    try { localStorage.setItem(KEY, JSON.stringify(next)); } catch { /* ignore */ }
    applyAppearance(next);
    listeners.forEach((l) => l());
    return;
  }
  // Yoğunluk renk değiştirmez: örtüsüz, anında uygulanır (eskiden tam ekran "tema uygulanıyor" örtüsü açılıyordu)
  const same = next.mode === current.mode && next.palettes[next.mode] === current.palettes[current.mode];
  current = next;
  try {
    localStorage.setItem(KEY, JSON.stringify(next));
    localStorage.setItem(LEGACY_THEME_KEY, next.mode === 'dark' ? 'dark' : 'light');
  } catch {
    /* ignore */
  }
  // Renk değişmediyse örtü açılmaz; düzen/okuma/süzgeç tercihleri anında uygulanır
  if (same) {
    applyAppearance(next);
    listeners.forEach((l) => l());
  }
  else void switchAppearance(next);
}

export function getAppearance() {
  return current;
}

export function useAppearance() {
  const a = useSyncExternalStore(
    (cb) => {
      listeners.add(cb);
      return () => listeners.delete(cb);
    },
    () => current,
    () => current
  );
  const pal = findPalette(a.mode, a.palettes[a.mode]);
  const custom = a.customAccents?.[`${a.mode}:${pal.id}`];
  return { ...a, palette: a.palettes[a.mode], accent: custom ? undefined : findAccent(pal, a.accents?.[`${a.mode}:${pal.id}`])?.id, customAccent: custom, set: setAppearance };
}
