import { applyAppearance, getAppearance, useAppearance } from './appearance';

/**
 * Geriye dönük tema API'si. Asıl depo utils/appearance.ts'tedir (açık / sarı / koyu + palet + yoğunluk).
 * Hızlı düğme koyu ↔ aydınlık arasında gider; "aydınlık" son kullanılan açık ya da sarı temadır.
 */
export type AppTheme = 'light' | 'dark';
const LAST_LIGHT_KEY = 'medsoru_last_light_mode';

export function readTheme(): AppTheme {
  return getAppearance().mode === 'dark' ? 'dark' : 'light';
}

export function applyTheme(_t?: AppTheme) {
  applyAppearance();
}

export function useTheme() {
  const { mode, set } = useAppearance();
  const theme: AppTheme = mode === 'dark' ? 'dark' : 'light';
  const toggle = () => {
    if (mode === 'dark') {
      let back: 'light' | 'sepia' = 'light';
      try {
        if (localStorage.getItem(LAST_LIGHT_KEY) === 'sepia') back = 'sepia';
      } catch {
        /* ignore */
      }
      set({ mode: back });
    } else {
      try {
        localStorage.setItem(LAST_LIGHT_KEY, mode);
      } catch {
        /* ignore */
      }
      set({ mode: 'dark' });
    }
  };
  return { theme, mode, toggle };
}
