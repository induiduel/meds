/**
 * v12 ölçek koruması ve ölçek farkındalıklı ölçüm yardımcıları.
 *
 * v12'de yazı boyutu tüm tasarımı CSS `zoom` ile ölçekler (styles/v12.css: --ui-zoom sayfa içeriği, --ch-zoom kabuk).
 * Zoom içindeki öğelerde CSS px ile görünür (ekran) px farklıdır; bu dosya iki sorunu çözer:
 *
 * 1) Dar alanda aşırı ölçek: 375 px telefonda 1.35 ölçek içeriği ~250 px'e sıkıştırıyor, tablette de masaüstü kuralları
 *    (@media viewport'a bakar) ölçek sonrası çok dar bir alana uygulanıyordu. Koruma, ölçek sonrası içerik genişliği
 *    PHONE_MIN / DESK_MIN altına inmeyecek bir tavan hesaplar (--ui-zoom-cap, telefonda kabuk için --ch-zoom-cap).
 *    Tavan devreye girince okuma yazısı (--read-size) aradaki farkı telafi eder: yazı yine seçilen boyutta kalır,
 *    yalnız düzen (düğme, boşluk, sütun) büyümeyi durdurur.
 * 2) JS ölçümleri: getBoundingClientRect görünür px, offsetWidth/style değerleri öğenin kendi (zoom'lu) px'idir.
 *    `elementZoom` ikisi arasındaki oranı, `topBarOffset` yapışkan üst çubuğun görünür yüksekliğini verir.
 */

/** Telefonda (<768 px) ölçek sonrası sayfa içeriğinin en dar genişliği (CSS px; 320 px telefonun içerik alanı ~288) */
const PHONE_MIN = 300;
/** Telefonda üst çubuk ve alt sekmelerin ölçek sonrası en dar genişliği */
const PHONE_CHROME_MIN = 320;
/** ≥768 px: masaüstü kuralları bu genişliğin altına sıkışmasın (768 px tablette ölçeksiz içerik ~664) */
const DESK_MIN = 600;

const num = (v: string) => parseFloat(v) || 0;

let installed = false;
let timer = 0;
let observed: Element | null = null;
let ro: ResizeObserver | null = null;
const last = { ui: '', ch: '' };

function setVar(name: '--ui-zoom-cap' | '--ch-zoom-cap', key: 'ui' | 'ch', value: string) {
  if (last[key] === value) return;
  last[key] = value;
  const st = document.documentElement.style;
  if (value) st.setProperty(name, value);
  else st.removeProperty(name);
}

function measure() {
  timer = 0;
  const root = document.documentElement;
  if (root.dataset.design !== 'v12') {
    setVar('--ui-zoom-cap', 'ui', '');
    setVar('--ch-zoom-cap', 'ch', '');
    return;
  }
  const isIos =
    root.classList.contains('is-ios') ||
    /iPhone|iPad|iPod/i.test(navigator.userAgent) ||
    (/Macintosh/i.test(navigator.userAgent) && navigator.maxTouchPoints > 1);
  if (isIos) {
    setVar('--ui-zoom-cap', 'ui', '1');
    setVar('--ch-zoom-cap', 'ch', '1');
    return;
  }
  const vw = root.clientWidth || window.innerWidth;
  if (!vw) return; // gizli çerçeve / henüz yerleşmemiş
  const phone = vw < 768;
  // Sayfa içeriğinin kullanabileceği genişlik: .sh-main'in kabı (ray boşluğu düşülmüş) − sayfa yan boşlukları.
  // .sh-main kendisi ölçeklenmez (çocukları ölçeklenir), bu yüzden ölçüm ölçekten bağımsızdır (döngü yok).
  const main = document.querySelector<HTMLElement>('.sh-main');
  let avail = vw - 32;
  if (main?.parentElement) {
    const p = main.parentElement;
    const ps = getComputedStyle(p);
    const ms = getComputedStyle(main);
    avail = p.clientWidth - num(ps.paddingLeft) - num(ps.paddingRight) - num(ms.paddingLeft) - num(ms.paddingRight);
    if (observed !== p) {
      ro?.disconnect();
      observed = p;
      observedW = -1;
      ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(onShellResize) : null;
      ro?.observe(p);
    }
  }
  if (avail <= 0) return;
  // Tavan 1'in altına inmez: küçük yazı seçimi (ölçek < 1) hiçbir zaman büyütülmez
  const ui = Math.max(1, avail / (phone ? PHONE_MIN : DESK_MIN));
  setVar('--ui-zoom-cap', 'ui', ui.toFixed(3));
  // Kabuk: telefonda üst çubuk + alt sekmeler ekran genişliğini kullanır; masaüstünde ray sabit genişlikte büyür
  setVar('--ch-zoom-cap', 'ch', phone ? Math.max(1, vw / PHONE_CHROME_MIN).toFixed(3) : '');
}

// rAF değil zamanlayıcı: arka plandaki sekmede/gizli çerçevede rAF durur, tavan eski boyutta kalıyordu
function schedule() {
  if (!timer) timer = window.setTimeout(measure, 16);
}

// Yalnız genişlik önemli: kabın yüksekliği her içerik değişiminde (arama sonuçları, liste yüklenmesi) değişir;
// her seferinde ölçmek getComputedStyle + clientWidth ile zorunlu yerleşim yaptırıp yazarken takılma üretiyordu.
let observedW = -1;
function onShellResize(entries: ResizeObserverEntry[]) {
  const w = entries[entries.length - 1]?.contentRect.width ?? -1;
  if (w === observedW) return;
  observedW = w;
  schedule();
}

/** Ölçek korumasını kurar (bir kez). Görünüm değişince applyAppearance `refreshZoomGuard` çağırır. */
export function installZoomGuard() {
  if (installed || typeof window === 'undefined') return;
  installed = true;
  window.addEventListener('resize', schedule, { passive: true });
  window.visualViewport?.addEventListener('resize', schedule, { passive: true });
  // Ray genişliği (.sh-app padding-left) geçişle değişir; geçiş bitince son genişlikle yeniden ölç
  document.addEventListener('transitionend', (e) => { if (e.propertyName === 'padding-left') schedule(); }, { passive: true });
  // Ray daralt/genişlet, tasarım/yoğunluk değişimi, kabuğun ilk yerleşimi
  new MutationObserver(schedule).observe(document.documentElement, { attributes: true, attributeFilter: ['data-side', 'data-design', 'data-density', 'data-layout'] });
  const watchShell = () => {
    const mo = new MutationObserver(() => {
      if (document.querySelector('.sh-main')) { schedule(); mo.disconnect(); }
    });
    mo.observe(document.body, { childList: true, subtree: true });
  };
  if (document.body) watchShell();
  else document.addEventListener('DOMContentLoaded', watchShell, { once: true });
  schedule();
}

export function refreshZoomGuard() {
  if (typeof window === 'undefined') return;
  if (!installed) installZoomGuard();
  else schedule();
}

/**
 * Öğenin etkin CSS zoom'u (ataların zoom'ları çarpılmış). getBoundingClientRect / clientX gibi görünür px değerlerini
 * öğenin kendi px'ine çevirmek için bölen olarak kullanılır.
 */
export function elementZoom(el: Element | null | undefined): number {
  if (!el) return 1;
  const z = (el as Element & { currentCSSZoom?: number }).currentCSSZoom;
  if (typeof z === 'number' && z > 0) return z;
  const h = el as HTMLElement;
  if (h.offsetWidth > 0) {
    const r = el.getBoundingClientRect().width / h.offsetWidth;
    if (r > 0 && Number.isFinite(r)) return r;
  }
  return 1;
}

/** Yapışkan üst çubuğun görünür alt kenarı (px): kaydırma hedefleri bunun altında kalmalı. */
export function topBarOffset(fallback = 52): number {
  const bar = document.querySelector('.s12-top, .sh-top');
  if (bar) {
    const r = bar.getBoundingClientRect();
    if (r.height > 0) return Math.max(0, r.bottom);
  }
  const n = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--sh-top-h'));
  return Number.isFinite(n) ? n : fallback;
}
