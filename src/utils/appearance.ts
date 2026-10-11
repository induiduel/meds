import { useSyncExternalStore } from 'react';
import { PALETTES, findPalette, installPaletteStyles, type ThemeMode } from './palettes';

/**
 * Görünüm tercihleri: tema (açık / sarı / koyu), her temada dört palet (a–d, utils/palettes.ts) ve yerleşim yoğunluğu.
 * Kök öğeye `data-mode`, `data-palette`, `data-density` yazılır; koyu temada eski `theme-dark` sınıfı da kalır
 * (index.css ve health.css'teki koyu kurallar onu kullanır). Token değerleri styles/appearance.css'tedir.
 */
export type { ThemeMode } from './palettes';
/** Palet kimliği: utils/palettes.ts kaydındaki `id` (a, b, c, …) — yeni palet eklemek için o listeye bakın. */
export type Palette = string;
export type Density = 'compact' | 'normal' | 'wide';

export interface Appearance {
  mode: ThemeMode;
  /** Her tema kendi palet seçimini hatırlar: koyuya geçip dönünce açık tema paleti kaybolmaz. */
  palettes: Record<ThemeMode, Palette>;
  density: Density;
}

export const MODE_LABELS: Record<ThemeMode, string> = { light: 'Açık', sepia: 'Sarı', dark: 'Koyu' };
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

function read(): Appearance {
  // İlk açılış her zaman açık temadır (sistem koyu olsa bile); kullanıcı Ayarlar'dan değiştirir.
  const fallback: Appearance = { mode: 'light', palettes: { light: 'a', sepia: 'a', dark: 'a' }, density: 'normal' };
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) {
      const p = JSON.parse(raw) as Partial<Appearance>;
      return {
        mode: p.mode === 'light' || p.mode === 'sepia' || p.mode === 'dark' ? p.mode : fallback.mode,
        // Kayıtta olmayan (silinmiş) palet seçimi temanın ilk paletine döner
        palettes: (['light', 'sepia', 'dark'] as ThemeMode[]).reduce((acc, m) => {
          acc[m] = findPalette(m, (p.palettes || {})[m]).id;
          return acc;
        }, {} as Record<ThemeMode, Palette>),
        density: p.density === 'compact' || p.density === 'wide' || p.density === 'normal' ? p.density : 'normal',
      };
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
  ? { mode: 'light', palettes: { light: 'a', sepia: 'a', dark: 'a' }, density: 'normal' }
  : read();

export function applyAppearance(a: Appearance = current) {
  installPaletteStyles();
  const el = document.documentElement;
  el.classList.add('theme-switching');
  el.dataset.mode = a.mode;
  el.dataset.palette = a.palettes[a.mode];
  el.dataset.density = a.density;
  el.classList.toggle('theme-dark', a.mode === 'dark');
  el.style.colorScheme = a.mode === 'dark' ? 'dark' : 'light';
  // Tarayıcı çubuğu rengi zemine uysun
  const meta = document.querySelector('meta[name="theme-color"]');
  const bg = getComputedStyle(el).getPropertyValue('--color-canvas').trim();
  if (meta && bg) meta.setAttribute('content', bg);
  window.setTimeout(() => el.classList.remove('theme-switching'), 300);
}

export function setAppearance(patch: Partial<Omit<Appearance, 'palettes'>> & { palette?: Palette }) {
  const next: Appearance = { ...current, palettes: { ...current.palettes } };
  if (patch.mode) next.mode = patch.mode;
  if (patch.density) next.density = patch.density;
  if (patch.palette) next.palettes[next.mode] = patch.palette;
  current = next;
  try {
    localStorage.setItem(KEY, JSON.stringify(next));
    localStorage.setItem(LEGACY_THEME_KEY, next.mode === 'dark' ? 'dark' : 'light');
  } catch {
    /* ignore */
  }
  applyAppearance(next);
  listeners.forEach((l) => l());
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
  return { ...a, palette: a.palettes[a.mode], set: setAppearance };
}
