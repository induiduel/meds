import { useSyncExternalStore } from 'react';
import { PALETTES, findAccent, findPalette, installPaletteStyles, type ThemeMode } from './palettes';

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
export type ReadingFont = 'serif' | 'sans';
export type TextSize = 's' | 'm' | 'l';
/** Basit: yalnız hızlı süzgeç hapları; Gelişmiş: "Süzgeç" sayfası da görünür */
export type FilterMode = 'basit' | 'gelismis';
export type MotionPref = 'full' | 'reduced';
/** Tasarım dili: v12 Net (varsayılan), v11 Sade, v10 Klasik — eski tasarımlar silinmez, profilden geri dönülebilir.
 *  v12, v11'in sayfa yapısını devralır (CSS `:root:is([data-design='v11'],[data-design='v12'])`) ve üstüne styles/v12.css katmanını koyar. */
export type DesignVersion = 'v12' | 'v11' | 'v10';
export const DESIGN_ORDER: DesignVersion[] = ['v12', 'v11', 'v10'];
/** v11 yapısını kullanan tasarımlar (v11 ve v12) */
export const isSadeFamily = (d: DesignVersion) => d !== 'v10';

export interface Appearance {
  mode: ThemeMode;
  /** Her tema kendi palet seçimini hatırlar: koyuya geçip dönünce açık tema paleti kaybolmaz. */
  palettes: Record<ThemeMode, Palette>;
  density: Density;
  layout: LayoutMode;
  reading: ReadingFont;
  textSize: TextSize;
  filters: FilterMode;
  /** Çıkmış/örnek soru kartlarında işaret etiketleri (varsayılan gizli) */
  qtags: boolean;
  motion: MotionPref;
  design: DesignVersion;
  /** Vurgu rengi seçimi, "<tema>:<palet>" anahtarıyla (yalnız `accents` tanımlı paletler; utils/palettes.ts) */
  accents?: Record<string, string>;
}

export const MODE_LABELS: Record<ThemeMode, string> = { light: 'Açık', sepia: 'Sarı', dark: 'Koyu' };
export const LAYOUT_LABELS: Record<LayoutMode, string> = { akis: 'Akış', pano: 'Pano', odak: 'Odak' };
export const READING_LABELS: Record<ReadingFont, string> = { serif: 'Serif', sans: 'Sans' };
export const TEXT_SIZE_LABELS: Record<TextSize, string> = { s: 'Küçük', m: 'Orta', l: 'Büyük' };
export const FILTER_MODE_LABELS: Record<FilterMode, string> = { basit: 'Basit', gelismis: 'Gelişmiş' };
const V11_DEFAULTS = { reading: 'serif' as ReadingFont, textSize: 'm' as TextSize, filters: 'basit' as FilterMode, qtags: false, motion: 'full' as MotionPref, design: 'v12' as DesignVersion };
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

/** v11 önceki varsayılandı: kayıtlı 'v11' bir kez v12'ye taşınır (bilerek Klasik seçen v10'da kalır). */
const DESIGN_MIGRATION_KEY = 'medsoru_design_v12_migrated';
function migrateDesign(d: unknown): DesignVersion {
  if (d === 'v10' || d === 'v12') return d;
  if (d === 'v11') {
    try {
      if (localStorage.getItem(DESIGN_MIGRATION_KEY)) return 'v11';
      localStorage.setItem(DESIGN_MIGRATION_KEY, '1');
    } catch { return 'v11'; }
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
        reading: p.reading === 'sans' ? 'sans' : 'serif',
        textSize: p.textSize === 's' || p.textSize === 'l' ? p.textSize : 'm',
        filters: p.filters === 'gelismis' ? 'gelismis' : 'basit',
        qtags: p.qtags === true,
        motion: p.motion === 'reduced' ? 'reduced' : 'full',
        design: migrateDesign(p.design),
        accents: p.accents && typeof p.accents === 'object' ? { ...p.accents } : {},
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
  el.dataset.filters = a.filters;
  el.dataset.qtags = a.qtags ? 'on' : 'off';
  el.dataset.motion = a.motion;
  el.dataset.design = a.design;
  el.classList.toggle('theme-dark', a.mode === 'dark');
  el.style.colorScheme = a.mode === 'dark' ? 'dark' : 'light';
  // Tarayıcı çubuğu rengi zemine uysun
  const meta = document.querySelector('meta[name="theme-color"]');
  const bg = getComputedStyle(el).getPropertyValue('--color-canvas').trim();
  if (meta && bg) meta.setAttribute('content', bg);
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
const nextFrame = () => new Promise<void>((r) => requestAnimationFrame(() => requestAnimationFrame(() => r())));

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

export function setAppearance(patch: Partial<Omit<Appearance, 'palettes' | 'accents'>> & { palette?: Palette; accent?: string }) {
  const next: Appearance = { ...current, palettes: { ...current.palettes }, accents: { ...(current.accents || {}) } };
  if (patch.mode) next.mode = patch.mode;
  if (patch.density) next.density = patch.density;
  if (patch.layout) next.layout = patch.layout;
  if (patch.reading) next.reading = patch.reading;
  if (patch.textSize) next.textSize = patch.textSize;
  if (patch.filters) next.filters = patch.filters;
  if (typeof patch.qtags === 'boolean') next.qtags = patch.qtags;
  if (patch.motion) next.motion = patch.motion;
  if (patch.design) next.design = patch.design;
  if (patch.palette) next.palettes[next.mode] = patch.palette;
  // Vurgu rengi: örtüsüz, anında (yalnız 4 token değişir)
  if (patch.accent) {
    next.accents![`${next.mode}:${next.palettes[next.mode]}`] = patch.accent;
    current = next;
    try { localStorage.setItem(KEY, JSON.stringify(next)); } catch { /* ignore */ }
    applyAppearance(next);
    listeners.forEach((l) => l());
    return;
  }
  const same = next.mode === current.mode && next.density === current.density && next.palettes[next.mode] === current.palettes[current.mode];
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
  return { ...a, palette: a.palettes[a.mode], accent: findAccent(pal, a.accents?.[`${a.mode}:${pal.id}`])?.id, set: setAppearance };
}
