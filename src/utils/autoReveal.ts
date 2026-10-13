/**
 * Evrensel otomatik odak (scroll-to-view).
 *
 * Bir soru kartında ya da Öğren etkileşiminde bir şeye dokunulup içerik açıldığında (açıklama,
 * şık detayı, geçmiş, boşluk doldurma cevabı …) yeni içerik çoğu zaman ekranın altında kalıyordu.
 * Bu modül tek bir belge düzeyinde dinleyiciyle çalışır: tıklanan öğenin kartı tıklamadan sonra
 * büyüdüyse ve alt kenarı görünür alanın dışına taştıysa kart, görünür alanın ortasına kaydırılır.
 * Kart ekrandan uzunsa başı üst çubuğun hemen altına getirilir.
 *
 * Kapsam: `.ms-qcard`, `.ls-ix`, `[data-auto-reveal]` kapları ve (v10) sitedeki her açılır öğe:
 * `aria-expanded` taşıyan düğmeler, `<summary>`, `aria-controls` hedefleri. Kullanıcı Ayarlar'dan kapatabilir
 * (`medsoru_auto_reveal = '0'`). "Hareketi azalt" açıkken kaydırma anlık yapılır.
 */
const ROOTS = '.ms-qcard, .ls-ix, [data-auto-reveal]';
const TRIGGERS = 'button, [role="button"], [role="radio"], [role="checkbox"], label, summary';
let installed = false;

export function autoRevealEnabled(): boolean {
  try { return localStorage.getItem('medsoru_auto_reveal') !== '0'; } catch { return true; }
}

export function setAutoRevealEnabled(on: boolean) {
  try { localStorage.setItem('medsoru_auto_reveal', on ? '1' : '0'); } catch { /* yoksay */ }
}

function topOffset(): number {
  const v = getComputedStyle(document.documentElement).getPropertyValue('--sh-top-h');
  const n = parseFloat(v);
  return (Number.isFinite(n) ? n : 56) + 12;
}

/** Bir öğeyi görünür alana getirir; zaten tamamen görünüyorsa dokunmaz. */
export function revealIntoView(el: Element | null, opts: { force?: boolean } = {}) {
  if (!el || typeof window === 'undefined') return;
  const r = el.getBoundingClientRect();
  const vh = window.innerHeight;
  const top = topOffset();
  const fullyVisible = r.top >= top && r.bottom <= vh - 12;
  if (fullyVisible && !opts.force) return;
  const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  const behavior: ScrollBehavior = reduce ? 'auto' : 'smooth';
  const goal = r.height > vh - top - 24
    ? window.scrollY + r.top - top
    : window.scrollY + r.top + r.height / 2 - vh / 2;
  const target = Math.max(0, Math.round(goal));
  const start = window.scrollY;
  window.scrollTo({ top: target, behavior });
  // Bazı gömülü görünümlerde ve arka plan sekmelerinde yumuşak kaydırma hiç başlamaz: yedek olarak atla.
  if (behavior === 'smooth') {
    window.setTimeout(() => {
      if (Math.abs(window.scrollY - start) < 2 && Math.abs(target - start) > 2) window.scrollTo({ top: target, behavior: 'auto' });
    }, 450);
  }
}

/** Kart dışı açılır öğeler (v10): aria-expanded taşıyan her düğme, <summary> ve aria-controls hedefi. */
const EXPANDERS = '[aria-expanded], summary';
const CONTAINERS = 'li, article, details, [role="region"], [data-reveal-root], .ui-card, .ui-group, section';

/** Tıklamadan sonra büyüyen ya da yeni beliren içeriği bulur: önce aria-controls, sonra en yakın kap. */
function resolveRoot(trigger: Element): { root: () => HTMLElement | null; lazy: boolean } | null {
  const fixedRoot = trigger.closest(ROOTS) as HTMLElement | null;
  if (fixedRoot) return { root: () => fixedRoot, lazy: false };
  if (!trigger.matches(EXPANDERS)) return null;
  // Menü/açılır pencere (aria-haspopup) konumlu katmandadır; sayfayı kaydırmak çapayı da kaydırır.
  if (trigger.getAttribute('aria-haspopup') && trigger.getAttribute('aria-haspopup') !== 'false') return null;
  const controls = trigger.getAttribute('aria-controls');
  if (controls) return { root: () => document.getElementById(controls) || (trigger.closest(CONTAINERS) as HTMLElement | null), lazy: true };
  const box = (trigger.closest(CONTAINERS) as HTMLElement | null) || trigger.parentElement;
  return box ? { root: () => box, lazy: false } : null;
}

export function installAutoReveal() {
  if (installed || typeof document === 'undefined') return;
  installed = true;
  document.addEventListener(
    'click',
    (e) => {
      if (!autoRevealEnabled()) return;
      const target = e.target as Element | null;
      const trigger = target?.closest?.(TRIGGERS);
      if (!trigger) return;
      // Yazı alanlarında, bağlantılarda ve kendi kaydırma alanı olan pencerelerde tetiklenmez.
      if (target?.closest('input[type="text"], input[type="search"], textarea, [contenteditable="true"], a[href], [role="dialog"], [role="menu"]')) return;
      const found = resolveRoot(trigger);
      if (!found) return;
      // Kapanan bir öğe (aria-expanded="true" → false) kaydırma gerektirmez.
      const wasOpen = trigger.getAttribute('aria-expanded') === 'true' || (trigger.tagName === 'SUMMARY' && (trigger.parentElement as HTMLDetailsElement | null)?.open);
      if (wasOpen && !trigger.closest(ROOTS)) return;
      const first = found.root();
      const before = first ? first.getBoundingClientRect().height : 0;
      // İçerik gecikmeli (animasyonlu ya da tembel) açılabilir: 900 ms boyunca izlenir,
      // büyüyüp/belirip alt kenarı ekrandan taşarsa bir kez kaydırılır.
      let done = false;
      let observed: HTMLElement | null = null;
      const check = () => {
        if (done) return;
        const root = found.root();
        if (!root || !root.isConnected) return;
        if (ro && observed !== root) { ro.observe(root); observed = root; }
        const r = root.getBoundingClientRect();
        const grew = found.lazy && root !== first ? r.height > 0 : r.height - before > 24;
        if (grew && r.bottom > window.innerHeight - 12) {
          done = true;
          revealIntoView(root);
        }
      };
      const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(check) : null;
      if (first && ro) { ro.observe(first); observed = first; }
      // aria-controls hedefi tıklamadan sonra DOM'a eklenebilir: birkaç karede yeniden ara.
      if (found.lazy) [60, 180, 360].forEach((ms) => window.setTimeout(check, ms));
      window.setTimeout(() => { check(); ro?.disconnect(); }, 900);
    },
    // Yakalama evresi: React kökündeki işleyiciler DOM'u güncellemeden önce yükseklik ölçülür.
    { passive: true, capture: true },
  );
}
