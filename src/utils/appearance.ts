import { useSyncExternalStore } from 'react';

/**
 * Görünüm tercihleri: tema (açık / sarı / koyu), her temada iki palet (a / b) ve yerleşim yoğunluğu.
 * Kök öğeye `data-mode`, `data-palette`, `data-density` yazılır; koyu temada eski `theme-dark` sınıfı da kalır
 * (index.css ve health.css'teki koyu kurallar onu kullanır). Token değerleri styles/appearance.css'tedir.
 */
export type ThemeMode = 'light' | 'sepia' | 'dark';
export type Palette = 'a' | 'b';
export type Density = 'compact' | 'normal' | 'wide';

export interface Appearance {
  mode: ThemeMode;
  /** Her tema kendi palet seçimini hatırlar: koyuya geçip dönünce açık tema paleti kaybolmaz. */
  palettes: Record<ThemeMode, Palette>;
  density: Density;
}

export const MODE_LABELS: Record<ThemeMode, string> = { light: 'Açık', sepia: 'Sarı', dark: 'Koyu' };
export const DENSITY_LABELS: Record<Density, string> = { compact: 'Kompakt', normal: 'Normal', wide: 'Geniş' };
export const PALETTE_INFO: Record<ThemeMode, Record<Palette, { name: string; hint: string; swatch: [string, string, string] }>> = {
  light: {
    a: { name: 'Klinik mavi', hint: 'Steril beyaz zemin, mavi-camgöbeği vurgu', swatch: ['#F7F9FB', '#FFFFFF', '#0A6E8A'] },
    b: { name: 'Sıcak arduvaz', hint: 'Yumuşak gri zemin, arduvaz vurgu', swatch: ['#F3F3F1', '#FCFCFB', '#3E5468'] },
  },
  sepia: {
    a: { name: 'Parşömen', hint: 'Kemik rengi zemin, kahve-siyah yazı', swatch: ['#F6F0E3', '#FBF7EE', '#8A5A2B'] },
    b: { name: 'Kehribar', hint: 'Bej-amber zemin, düşük mavi ışık', swatch: ['#F1E4C8', '#F8EED9', '#9A5B12'] },
  },
  dark: {
    a: { name: 'Gece arduvazı', hint: 'Lacivert-arduvaz zemin, yumuşak neon odak', swatch: ['#0F1624', '#172131', '#5CC8E6'] },
    b: { name: 'OLED obsidyen', hint: 'Saf siyah zemin, net gri ayrım', swatch: ['#000000', '#0E0E10', '#7AB4FF'] },
  },
};

const KEY = 'medsoru_appearance';
const LEGACY_THEME_KEY = 'medsoru_theme';
const listeners = new Set<() => void>();

function systemDark() {
  return typeof window !== 'undefined' && !!window.matchMedia?.('(prefers-color-scheme: dark)').matches;
}

function read(): Appearance {
  const fallback: Appearance = { mode: systemDark() ? 'dark' : 'light', palettes: { light: 'a', sepia: 'a', dark: 'a' }, density: 'normal' };
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) {
      const p = JSON.parse(raw) as Partial<Appearance>;
      return {
        mode: p.mode === 'light' || p.mode === 'sepia' || p.mode === 'dark' ? p.mode : fallback.mode,
        palettes: { ...fallback.palettes, ...(p.palettes || {}) },
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
