import { isScrollLocked } from '../../utils/scrollLock';
import './system.css';

/**
 * Aşağı çekip yenile — tüm dokunmatik cihazlarda tek ve tutarlı hareket. Ana ekrana yüklenmiş uygulamada
 * (PWA) tarayıcının kendi hareketi hiç yoktur; sekmede ise kök `overscroll-behavior-y: none` (iOS sıçraması ve
 * çekmece içi kaydırmanın sayfayı yenilemesini engellemek için) yerel hareketi kapatır. Bu bileşen ikisini de karşılar.
 *  - Yalnız sayfa en üstteyken, kilitli katman (sheet/pencere) yokken ve dokunulan öğenin kaydırılabilir bir
 *    atası yukarı kaydırılmışken DEĞİL başlar; tam ekran ders, çizim alanı ve form alanları hariçtir.
 *  - Dinleyiciler pasiftir (kaydırmayı asla engellemez); gösterge transform ile çizilir (kare başına bir kez).
 *  - 72px eşiğini geçip bırakınca sayfa yenilenir (service worker kabuğu önbellekten anında açar).
 */
const THRESHOLD = 72;
const MAX = 120;
const EXCLUDE = '.ls-root, .sh-sheet-root, .ms-am, [role="dialog"], canvas, input, textarea, select, [contenteditable="true"], .no-ptr';

function scrolledAncestor(el: Element | null): boolean {
  for (let n = el as HTMLElement | null; n && n !== document.body; n = n.parentElement) {
    if (n.scrollTop > 0) {
      const oy = getComputedStyle(n).overflowY;
      if (oy === 'auto' || oy === 'scroll') return true;
    }
  }
  return false;
}

let installed = false;
export function installPullToRefresh() {
  if (installed || typeof window === 'undefined') return;
  if (!('ontouchstart' in window) || !window.matchMedia('(pointer: coarse)').matches) return;
  installed = true;

  const el = document.createElement('div');
  el.className = 'ptr';
  el.setAttribute('aria-hidden', 'true');
  el.innerHTML = '<span class="ptr-ring"><svg viewBox="0 0 24 24"><path d="M12 4v10m0 0-4-4m4 4 4-4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>';
  document.body.appendChild(el);

  let startY = 0;
  let startX = 0;
  let pull = 0;
  let active = false;
  let raf = 0;
  let refreshing = false;

  const paint = () => {
    raf = 0;
    const p = Math.min(1, pull / THRESHOLD);
    el.style.transform = `translate3d(-50%, ${Math.round(pull * 0.9) - 48}px, 0)`;
    el.style.opacity = String(Math.min(1, pull / 24));
    el.style.setProperty('--ptr-p', String(p));
    el.classList.toggle('is-ready', pull >= THRESHOLD);
  };
  const schedule = () => { if (!raf) raf = requestAnimationFrame(paint); };

  document.addEventListener('touchstart', (e) => {
    if (refreshing || e.touches.length !== 1 || window.scrollY > 0 || isScrollLocked()) return;
    const t = e.target as Element;
    if (t.closest?.(EXCLUDE) || scrolledAncestor(t)) return;
    startY = e.touches[0].clientY;
    startX = e.touches[0].clientX;
    active = true;
    pull = 0;
    el.classList.remove('is-back');
  }, { passive: true });

  document.addEventListener('touchmove', (e) => {
    if (!active) return;
    const dy = e.touches[0].clientY - startY;
    const dx = Math.abs(e.touches[0].clientX - startX);
    if (window.scrollY > 0 || dy < 0 || dx > dy) {
      if (pull) { pull = 0; schedule(); }
      if (dy < -6 || dx > 16) active = false;
      return;
    }
    // Dirençli çekiş: parmak uzaklaştıkça gösterge yavaşlar
    pull = Math.min(MAX, dy * 0.55);
    schedule();
  }, { passive: true });

  const finish = () => {
    if (!active) return;
    active = false;
    if (pull >= THRESHOLD) {
      refreshing = true;
      el.classList.add('is-loading');
      pull = THRESHOLD;
      schedule();
      if (navigator.vibrate) try { navigator.vibrate(8); } catch { /* yok */ }
      window.setTimeout(() => window.location.reload(), 280);
    } else {
      pull = 0;
      el.classList.add('is-back');
      schedule();
    }
  };
  document.addEventListener('touchend', finish, { passive: true });
  document.addEventListener('touchcancel', finish, { passive: true });
}
