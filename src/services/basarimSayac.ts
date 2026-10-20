/**
 * Başarım soru sayacı (2026-10-20): gün başına çözülen soru, cihaz başına ayrı tutulur → `medsoru_basarim_sayac_v1`
 * `{ c: { <cihaz>: { 'YYYY-AA-GG': n } } }`. Cihazlar profil eşitlemesinde birleşir (userKvSync: cihaz/gün başına en
 * büyük), sunucu tüm cihazları toplar (services/basarim/basarimMotor). Aynı soru aynı açılışta iki kez sayılmaz.
 */
export const SAYAC_KEY = 'medsoru_basarim_sayac_v1';
const CIHAZ_KEY = 'medsoru_basarim_cihaz';
const GUN_SAKLA = 120;

const gun = (d = new Date()) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const cihaz = () => {
  try {
    let c = localStorage.getItem(CIHAZ_KEY);
    if (!c) { c = Math.random().toString(36).slice(2, 10); localStorage.setItem(CIHAZ_KEY, c); }
    return c;
  } catch { return 'x'; }
};
const sayilan = new Set<string>();

/** Çözülen soru(lar)ı sayar. `kimlik` verilirse bu açılışta o soru bir kez sayılır. */
export function soruSay(kimlik?: string, n = 1) {
  if (typeof window === 'undefined' || n <= 0) return;
  if (kimlik) { if (sayilan.has(kimlik)) return; sayilan.add(kimlik); }
  try {
    const v = JSON.parse(localStorage.getItem(SAYAC_KEY) || '{}') || {};
    const c = (v.c ||= {});
    const id = cihaz();
    const m = (c[id] ||= {});
    const g = gun();
    m[g] = (m[g] || 0) + n;
    const gunler = Object.keys(m).sort();
    if (gunler.length > GUN_SAKLA) for (const x of gunler.slice(0, gunler.length - GUN_SAKLA)) delete m[x];
    localStorage.setItem(SAYAC_KEY, JSON.stringify(v));
  } catch { /* kota / özel pencere */ }
}

/** İki cihazdan gelen sayaçları kaybetmeden birleştirir (cihaz/gün başına en büyük). */
export function sayacBirlestir(eski: string, yeni: string): string {
  const a = JSON.parse(eski), b = JSON.parse(yeni);
  const c: Record<string, Record<string, number>> = {};
  for (const src of [a?.c || {}, b?.c || {}]) for (const [d, gunler] of Object.entries<any>(src)) {
    const m = (c[d] ||= {});
    for (const [g, n] of Object.entries<any>(gunler || {})) m[g] = Math.max(m[g] || 0, Number(n) || 0);
  }
  return JSON.stringify({ c });
}
