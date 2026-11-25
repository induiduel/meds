/**
 * v17 "Klinik editöryal" (docs/V17_PLAN.md). Ayrı kod tabanı: src/v17/. Yalnız yönetici + "v17 (deneme)" seçiliyken,
 * v17'nin desteklediği sayfalarda App, v15 kabuğunun üstüne tam ekran V17Kok katmanını açar; öğrenci etkilenmez.
 * İstek cihazda saklanır; yönetici bilgisi siteAyar.yoneticiAyarla → v17Yonetici ile gelir.
 */
const KEY = 'medsor_v17_deneme';

let istek = (() => { try { return localStorage.getItem(KEY) === '1'; } catch { return false; } })();
let yonetici = false;
const dinleyiciler = new Set<() => void>();
const bildir = () => dinleyiciler.forEach((f) => f());

export const v17Istek = () => istek;
export const v17Acik = () => istek && yonetici;
export function v17Ayarla(v: boolean) {
  istek = v;
  try { if (v) localStorage.setItem(KEY, '1'); else localStorage.removeItem(KEY); } catch { /* özel pencere */ }
  bildir();
}
export function v17Yonetici(v: boolean) { if (yonetici !== v) { yonetici = v; bildir(); } }
export function v17Dinle(f: () => void) { dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; }

/** v17'nin kendi ekranı olan iç rotalar (geri kalanı v15 kabuğunda açılır) */
export const V17_ROTALAR = new Set(['today', 'canli_ders']);

/** Tarayıcı sınaması: test oturumu yönetici değil; o sekmede v17'yi açar (yalnız görünüm, veri açmaz). */
if (typeof window !== 'undefined') {
  (window as unknown as { __v17Sinama?: () => void }).__v17Sinama = () => { istek = true; v17Yonetici(true); };
}
