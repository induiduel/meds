/**
 * Evrensel otomatik odak (scroll-to-view).
 *
 * Bir soru kartında ya da Öğren etkileşiminde bir şeye dokunulup içerik açıldığında (açıklama,
 * şık detayı, geçmiş, boşluk doldurma cevabı …) yeni içerik çoğu zaman ekranın altında kalıyordu.
 * Bu modül tek bir belge düzeyinde dinleyiciyle çalışır: tıklanan öğenin kartı tıklamadan sonra
 * büyüdüyse ve alt kenarı görünür alanın dışına taştıysa kart, görünür alanın ortasına kaydırılır.
 * Kart ekrandan uzunsa başı üst çubuğun hemen altına getirilir.
 *
 * Kapsam: `.ms-qcard`, `.ls-ix`, `[data-auto-reveal]` kapları. Kullanıcı Ayarlar'dan kapatabilir
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

export function installAutoReveal() {
  if (installed || typeof document === 'undefined') return;
  installed = true;
  document.addEventListener(
    'click',
    (e) => {
      if (!autoRevealEnabled()) return;
      const target = e.target as Element | null;
      const trigger = target?.closest?.(TRIGGERS);
      const root = trigger?.closest?.(ROOTS) as HTMLElement | null;
      if (!trigger || !root) return;
      // Yazı alanlarında ve bağlantılarda tetiklenmez.
      if (target?.closest('input[type="text"], textarea, [contenteditable="true"], a[href]')) return;
      const before = root.getBoundingClientRect().height;
      // İçerik gecikmeli (animasyonlu) açılabilir: kartın yüksekliği 900 ms boyunca izlenir,
      // büyüyüp alt kenarı ekrandan taşarsa bir kez kaydırılır.
      let done = false;
      const check = () => {
        if (done || !root.isConnected) return;
        const r = root.getBoundingClientRect();
        if (r.height - before > 24 && r.bottom > window.innerHeight - 12) {
          done = true;
          revealIntoView(root);
        }
      };
      const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(check) : null;
      ro?.observe(root);
      window.setTimeout(() => { check(); ro?.disconnect(); }, 900);
    },
    // Yakalama evresi: React kökündeki işleyiciler DOM'u güncellemeden önce yükseklik ölçülür.
    { passive: true, capture: true },
  );
}
