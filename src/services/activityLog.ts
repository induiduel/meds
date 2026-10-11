/**
 * Kişisel etkinlik günlüğü ve çalışma süresi sayacı (yalnız bu cihazda, localStorage).
 *
 * - `logActivity` her önemli işlemi (soru çözme, not, favori, test, katkı …) kaydeder; en çok 600 olay.
 * - `installStudyTimer` sekme görünür ve son 60 sn içinde etkileşim varken her 30 sn'yi o günün
 *   çalışma süresine ekler. Böylece boşta açık kalan sekme süreyi şişirmez.
 * İstatistiklerim sayfası bu iki kaynağı ve çalışma deposunu (studyStore) okur.
 */
export type ActivityKind = 'coz' | 'yanlis' | 'not' | 'begen' | 'kaydet' | 'katki' | 'test' | 'bitir';

export interface ActivityEvent {
  kind: ActivityKind;
  text: string;
  at: string;
}

const EVENTS_KEY = 'medsoru_activity_v1';
const MINUTES_KEY = 'medsoru_study_seconds_v1';
const MAX_EVENTS = 600;

const read = <T,>(key: string, fallback: T): T => {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
};
const write = (key: string, v: unknown) => {
  try { localStorage.setItem(key, JSON.stringify(v)); } catch { /* yoksay */ }
};

export const dayKey = (d = new Date()) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

export function logActivity(kind: ActivityKind, text: string) {
  const list = read<ActivityEvent[]>(EVENTS_KEY, []);
  list.push({ kind, text: String(text || '').slice(0, 160), at: new Date().toISOString() });
  write(EVENTS_KEY, list.slice(-MAX_EVENTS));
}

export const getActivity = (): ActivityEvent[] => read<ActivityEvent[]>(EVENTS_KEY, []);

/** Gün → saniye */
export const getStudySeconds = (): Record<string, number> => read<Record<string, number>>(MINUTES_KEY, {});

let timerInstalled = false;
export function installStudyTimer() {
  if (timerInstalled || typeof window === 'undefined') return;
  timerInstalled = true;
  let lastInput = Date.now();
  const bump = () => { lastInput = Date.now(); };
  ['pointerdown', 'keydown', 'scroll', 'touchstart'].forEach((ev) => window.addEventListener(ev, bump, { passive: true, capture: true }));
  const TICK = 30;
  window.setInterval(() => {
    if (document.visibilityState !== 'visible' || Date.now() - lastInput > 60_000) return;
    const all = getStudySeconds();
    const k = dayKey();
    all[k] = (all[k] || 0) + TICK;
    // 400 günden eskileri at
    const keys = Object.keys(all).sort();
    while (keys.length > 400) delete all[keys.shift()!];
    write(MINUTES_KEY, all);
  }, TICK * 1000);
}
