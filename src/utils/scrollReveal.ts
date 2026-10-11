/**
 * Kaydırınca beliren içerik (scroll-reveal) — IntersectionObserver ile, yalnız transform/opaklık.
 *
 * Gözlem başladığında zaten görünür olan öğelere dokunulmaz (ilk boyamada yanıp sönme olmaz);
 * yalnız görünür alanın altında kalanlar `is-pending` alır ve görünür alana girince `is-in` olur.
 * Yeni eklenen öğeler (adım değişimi) MutationObserver ile yakalanır. "Hareketi azalt" açıkken çalışmaz.
 */
export function observeScrollReveal(root: HTMLElement | null, selector: string): () => void {
  if (!root || typeof IntersectionObserver === 'undefined') return () => {};
  if (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) return () => {};

  const scrollRoot = getComputedStyle(root).overflowY.match(/auto|scroll/) ? root : null;
  const io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        const el = e.target as HTMLElement;
        el.classList.remove('is-pending');
        el.classList.add('is-in');
        io.unobserve(el);
      }
    },
    { root: scrollRoot, rootMargin: '0px 0px -8% 0px', threshold: 0.05 },
  );

  const viewBottom = () => (scrollRoot ? scrollRoot.getBoundingClientRect().bottom : window.innerHeight);
  const arm = (el: HTMLElement) => {
    if (el.dataset.rbSeen) return;
    el.dataset.rbSeen = '1';
    el.classList.add('rb-reveal');
    if (el.getBoundingClientRect().top < viewBottom()) return; // zaten görünür
    el.classList.add('is-pending');
    io.observe(el);
  };
  const scan = () => root.querySelectorAll<HTMLElement>(selector).forEach(arm);
  scan();
  const mo = new MutationObserver(() => scan());
  mo.observe(root, { childList: true, subtree: true });

  return () => {
    io.disconnect();
    mo.disconnect();
    root.querySelectorAll<HTMLElement>('.rb-reveal.is-pending').forEach((el) => el.classList.remove('is-pending'));
  };
}
