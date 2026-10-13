import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * Liste ekranlarındaki yapışkan kontrol yuvası (`.cx-dock`: arama + süzgeç + sekmeler) için ortak davranış.
 *
 * - Aşağı kaydırınca yuva transform ile üst çubuğun arkasına kayar (yerleşim değişmez → scroll anchoring
 *   döngüsü/titreme olmaz); `html[data-dock="hidden"]` ile CSS canlandırır.
 * - Yukarı kaydırınca (≥ 40px gerçek hareket) ya da sayfanın tepesine dönünce geri gelir.
 * - Yuvanın içinde odak varken (arama yazılıyor, öneri açık) ya da açık bir sheet/menü varken saklanmaz.
 * Dönüş: yuva saklı mı (üst çubuk bu durumda sayfa aramasını kendisi gösterir).
 */
/** Kaydırınca saklanan yapışkan kontrol şeritleri: liste yuvaları ve `data-autohide` işaretli şeritler. */
export const DOCK_SEL = '.cx-dock, .pt-root, [data-autohide]';

export function useDockAutoHide(routeKey: string) {
  const [hidden, setHidden] = useState(false);
  const revealRef = useRef<() => void>(() => {});

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const root = document.documentElement;
    let state = false;
    let extreme = window.scrollY;
    let raf = 0;
    const DOWN = 24;
    const UP = 40;

    // Kaydırılmış ama yuva görünürken `data-dock="compact"`: telefonda PageToolbar başlık satırını bırakır
    // (başlık üst çubukta zaten yazar), yalnız arama + süzgeç + segment kalır.
    let compact = false;
    const sync = () => {
      if (state) root.dataset.dock = 'hidden';
      else if (compact) root.dataset.dock = 'compact';
      else delete root.dataset.dock;
    };
    const apply = (v: boolean) => {
      if (state === v) return;
      state = v;
      sync();
      setHidden(v);
    };
    const setCompact = (v: boolean) => {
      if (compact === v) return;
      compact = v;
      sync();
    };

    const check = () => {
      raf = 0;
      const dock = document.querySelector<HTMLElement>(DOCK_SEL);
      const y = window.scrollY;
      if (!dock) { apply(false); setCompact(false); extreme = y; return; }
      // Sayfanın ilk ekranında (başlık + yuva) saklama. Yapışkan öğenin offsetTop'u kaydırmayla değiştiği için sabit eşik.
      const threshold = 220;
      setCompact(y >= threshold);
      const ae = document.activeElement;
      // Üst çubuktaki vekil aramaya yazılırken yuva geri gelip vekili kaldırmasın.
      if (ae && ae.closest('.sh-pq')) { extreme = y; return; }
      const busy = (ae && dock.contains(ae) && ae.matches('input, textarea, select')) || document.querySelector('.ms-suggest, [role="dialog"][aria-modal="true"]');
      // Yuva henüz yapışmadıysa (başlık altında akışta) saklama: transform yerini boş bırakır,
      // başlık ile liste arasında boşluk görünür. Yapışma, önceki kardeşin üst çubuğun altına geçmesiyle anlaşılır.
      const prev = dock.previousElementSibling;
      const barBottom = document.querySelector('.sh-top')?.getBoundingClientRect().bottom ?? 0;
      const stuck = !prev || prev.getBoundingClientRect().bottom <= barBottom + 1;
      if (y < threshold || busy || !stuck) { apply(false); extreme = y; return; }
      if (state) {
        extreme = Math.max(extreme, y);
        if (extreme - y > UP) { apply(false); extreme = y; }
      } else {
        extreme = Math.min(extreme, y);
        if (y - extreme > DOWN) { apply(true); extreme = y; }
      }
    };
    const onScroll = () => { if (!raf) raf = requestAnimationFrame(check); };
    // "Süzgeçleri göster": yuva geri gelir; yeniden saklanması için yeni bir aşağı kaydırma gerekir.
    revealRef.current = () => { apply(false); extreme = window.scrollY; };

    apply(false);
    extreme = window.scrollY;
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => {
      window.removeEventListener('scroll', onScroll);
      if (raf) cancelAnimationFrame(raf);
      delete root.dataset.dock;
    };
  }, [routeKey]);

  const reveal = useCallback(() => revealRef.current(), []);
  return { hidden, reveal };
}

/** Sayfa yuvasındaki ilk arama alanı (üst çubuk vekili bunu yansıtır). */
export const findDockSearchInput = (): HTMLInputElement | null =>
  document.querySelector<HTMLInputElement>('.cx-dock input[type="search"], .cx-dock .cx-search input, .cx-dock input[type="text"], .pt-root input[data-page-search]');

/** React kontrollü input'a dışarıdan değer yazar (native setter + input olayı). */
export function setReactInputValue(el: HTMLInputElement, value: string) {
  const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value')?.set;
  setter?.call(el, value);
  el.dispatchEvent(new Event('input', { bubbles: true }));
}
