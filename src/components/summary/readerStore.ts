import { useSyncExternalStore } from 'react';

/**
 * Özet okuyucusunun cihaz tercihleri ve okuma ilerlemesi (yalnız bu tarayıcıda; kaybolursa okuyucu
 * varsayılanlarla açılır). Renk/tema burada DEĞİL: okuyucu uygulamanın temasını ve paletini kullanır
 * (utils/appearance.ts), Aa panelindeki tema düğmesi de onu değiştirir.
 */

export type Measure = 'narrow' | 'normal' | 'wide';
export interface ReaderPrefs {
  /** Yazı ölçeği (%) */
  scale: number;
  serif: boolean;
  markers: boolean;
  measure: Measure;
}
export interface ReadingMark {
  /** 0–100 */
  p: number;
  /** Kaydırma konumu (px) */
  y: number;
  /** Son okuma zamanı (ms) */
  t: number;
}

const PREFS_KEY = 'medsoru_reader_prefs';
const PROGRESS_KEY = 'medsoru_summary_progress';
const DEFAULT_PREFS: ReaderPrefs = { scale: 100, serif: false, markers: true, measure: 'normal' };

const load = <T,>(key: string, fallback: T): T => {
  try {
    const raw = localStorage.getItem(key);
    return raw ? { ...fallback, ...JSON.parse(raw) } : fallback;
  } catch {
    return fallback;
  }
};
const save = (key: string, v: unknown) => {
  try {
    localStorage.setItem(key, JSON.stringify(v));
  } catch {
    /* gizli pencere / kota: tercih bu oturumla sınırlı kalır */
  }
};

function createStore<T>(initial: T) {
  let value = initial;
  const subs = new Set<() => void>();
  return {
    get: () => value,
    set(next: T) {
      value = next;
      subs.forEach((s) => s());
    },
    subscribe(cb: () => void) {
      subs.add(cb);
      return () => subs.delete(cb);
    },
  };
}

const prefs = createStore<ReaderPrefs>(typeof window === 'undefined' ? DEFAULT_PREFS : load(PREFS_KEY, DEFAULT_PREFS));
const progress = createStore<Record<string, ReadingMark>>(typeof window === 'undefined' ? {} : load(PROGRESS_KEY, {}));

export const useReaderPrefs = () => {
  const p = useSyncExternalStore(prefs.subscribe, prefs.get, prefs.get);
  const set = (patch: Partial<ReaderPrefs>) => {
    const next = { ...prefs.get(), ...patch };
    next.scale = Math.min(150, Math.max(80, next.scale));
    prefs.set(next);
    save(PREFS_KEY, next);
  };
  return [p, set] as const;
};

export const useReadingProgress = () => useSyncExternalStore(progress.subscribe, progress.get, progress.get);

let saveTimer = 0;
export function markReading(id: string, p: number, y: number) {
  const cur = progress.get()[id];
  // Bitmiş özet yeniden açılıp yukarıda gezinilince "bitti" kaybolmasın
  const pct = Math.max(cur?.p && cur.p >= 97 ? cur.p : 0, Math.round(p));
  progress.set({ ...progress.get(), [id]: { p: pct, y: Math.round(y), t: Date.now() } });
  window.clearTimeout(saveTimer);
  saveTimer = window.setTimeout(() => save(PROGRESS_KEY, progress.get()), 400);
}
