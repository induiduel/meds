/**
 * v16 deneme katmanı (docs/V16_PLAN.md). Yalnız yönetici + v15 açıkken + kullanıcı "v16 (deneme)" seçtiyse kök öğeye
 * `data-v16="on"` yazılır; styles/v16/*.css yalnız bu öznitelik altında çalışır, öğrenci hiçbir şey görmez.
 * İstek cihazda saklanır; yönetici bilgisi App.tsx → siteAyar.yoneticiAyarla → v16Yonetici ile gelir.
 */
const KEY = 'medsor_v16_deneme';

let istek = (() => { try { return localStorage.getItem(KEY) === '1'; } catch { return false; } })();
let yonetici = false;
const dinleyiciler = new Set<() => void>();

export function v16Uygula() {
  if (typeof document === 'undefined') return;
  const el = document.documentElement;
  const acik = istek && yonetici && el.dataset.v15 === 'on';
  if (acik) el.dataset.v16 = 'on'; else delete el.dataset.v16;
}

export const v16Istek = () => istek;
export const v16Acik = () => istek && yonetici;

export function v16Ayarla(v: boolean) {
  istek = v;
  try { if (v) localStorage.setItem(KEY, '1'); else localStorage.removeItem(KEY); } catch { /* özel pencere */ }
  v16Uygula();
  dinleyiciler.forEach((f) => f());
}

export function v16Yonetici(v: boolean) {
  if (yonetici === v) return;
  yonetici = v;
  v16Uygula();
  dinleyiciler.forEach((f) => f());
}

export function v16Dinle(f: () => void) { dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; }

/**
 * Tarayıcı sınaması (ajan/yönetici): v16 yalnız görsel katmandır, yönetici verisine erişim vermez; test oturumu yönetici
 * olmadığı için `window.__v16Sinama()` ile o sekmede açılır (kalıcı değil, yenileyince kapanır).
 */
if (typeof window !== 'undefined') {
  (window as unknown as { __v16Sinama?: () => void }).__v16Sinama = () => { istek = true; v16Yonetici(true); };
}
