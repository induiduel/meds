/**
 * Ders özeti — "öğrendim" işaretleri (madde başına). Profil eşitlemesinde (`medsoru_ders_ozet_isaret_v1`):
 * { ders: { <öğe id>: '2026-11-23T…' } }. Klasik ekranda da kullanılır.
 */
import { useSyncExternalStore } from 'react';

const KEY = 'medsoru_ders_ozet_isaret_v1';
export type IsaretHaritasi = Record<string, Record<string, string>>;

let onbellek: IsaretHaritasi | null = null;
const abone = new Set<() => void>();

export function isaretOku(): IsaretHaritasi {
  if (onbellek) return onbellek;
  try { onbellek = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch { onbellek = {}; }
  return onbellek!;
}

function yay() { abone.forEach((f) => f()); }

export function isaretToggle(ders: string, oge: string): boolean {
  const t = { ...isaretOku() };
  const d = { ...(t[ders] || {}) };
  const acik = !d[oge];
  if (acik) d[oge] = new Date().toISOString(); else delete d[oge];
  if (Object.keys(d).length) t[ders] = d; else delete t[ders];
  onbellek = t;
  try { localStorage.setItem(KEY, JSON.stringify(t)); } catch { /* özel pencere */ }
  yay();
  return acik;
}

export function isaretTemizle(ders: string) {
  const t = { ...isaretOku() };
  delete t[ders];
  onbellek = t;
  try { localStorage.setItem(KEY, JSON.stringify(t)); } catch { /* */ }
  yay();
}

if (typeof window !== 'undefined') window.addEventListener('storage', (e) => {
  if (e.key === KEY || e.key === null) { onbellek = null; yay(); }
});

export const useOzetIsaret = () => useSyncExternalStore((f) => { abone.add(f); return () => abone.delete(f); }, isaretOku, isaretOku);
