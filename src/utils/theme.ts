import { useEffect, useState } from 'react';

/** Uygulama teması: açık / koyu. Tercih localStorage'da, ilk açılışta sistem ayarı. */
export type AppTheme = 'light' | 'dark';
const KEY = 'medsoru_theme';

export function readTheme(): AppTheme {
  try {
    const v = localStorage.getItem(KEY);
    if (v === 'light' || v === 'dark') return v;
  } catch {
    /* ignore */
  }
  return typeof window !== 'undefined' && window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

export function applyTheme(t: AppTheme) {
  const el = document.documentElement;
  el.classList.add('theme-switching');
  el.classList.toggle('theme-dark', t === 'dark');
  el.style.colorScheme = t;
  window.setTimeout(() => el.classList.remove('theme-switching'), 300);
}

export function useTheme() {
  const [theme, setTheme] = useState<AppTheme>(readTheme);
  useEffect(() => {
    applyTheme(theme);
    try {
      localStorage.setItem(KEY, theme);
    } catch {
      /* ignore */
    }
  }, [theme]);
  return { theme, toggle: () => setTheme((t) => (t === 'dark' ? 'light' : 'dark')) };
}
