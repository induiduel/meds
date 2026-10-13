/**
 * Açılan bir bölüm (açıklama, yorumlar, çekmece) görünür alanın altına taşıyorsa onu yumuşakça görünüme getirir.
 * `block: 'nearest'`: yalnız gerektiği kadar kayar; zaten görünüyorsa hiç kıpırdamaz.
 * Hareketi azalt tercihinde anında kayar. Alt sekme çubuğu payı CSS'teki `scroll-margin-bottom` ile verilir.
 */
export const prefersReducedMotion = (): boolean => {
  try {
    return typeof window !== 'undefined' && !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  } catch {
    return false;
  }
};

/** `delay`: açılma canlandırması bitince ölç (yükseklik geçişi ~220 ms). */
export function revealInView(el: HTMLElement | null | undefined, delay = 240): void {
  if (!el || typeof window === 'undefined') return;
  const reduced = prefersReducedMotion();
  const run = () => {
    const r = el.getBoundingClientRect();
    const vh = window.innerHeight || document.documentElement.clientHeight;
    if (r.bottom <= vh - 8 && r.top >= 0) return;
    el.scrollIntoView({ block: 'nearest', behavior: reduced ? 'auto' : 'smooth' });
  };
  window.setTimeout(() => requestAnimationFrame(run), reduced ? 0 : delay);
}
