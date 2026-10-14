import { useEffect, useState, useSyncExternalStore } from 'react';

/**
 * Kabuğun ortak durum kancaları: klasik (v10/v11) ve v12 kabuğu aynı davranışı paylaşır.
 *  - useSideCollapse: kenar menüsünün daraltma tercihi (localStorage) + Akış/Odak düzeninde varsayılan daraltma;
 *    html[data-side] özniteliğini yazar (genişlik --sh-side-w buna göre değişir).
 *  - usePhone: <640px (hesap menüsü telefonda alt sayfa olarak açılır).
 *  - useSearchShortcut: "/" ya da Ctrl/⌘+K ve `medsoru:search` olayı arama paletini açar.
 */

const COLLAPSE_KEY = 'medsoru_rail_collapsed';

export function useSideCollapse() {
  // Kullanıcının seçimi (null: seçim yok). Seçim yoksa Akış/Odak düzeninde menü daralmış başlar; düzen
  // değişince seçim sıfırlanır. Eskiden bu düzenlerde CSS menüyü zorla daraltıyordu ve düğme işe yaramıyordu.
  const [pref, setPref] = useState<boolean | null>(() => {
    try {
      const v = localStorage.getItem(COLLAPSE_KEY);
      return v === '1' ? true : v === '0' ? false : null;
    } catch {
      return null;
    }
  });
  const [compactLayout, setCompactLayout] = useState(() => /^(akis|odak)$/.test(document.documentElement.dataset.layout || ''));
  useEffect(() => {
    const el = document.documentElement;
    let last = el.dataset.layout;
    const mo = new MutationObserver(() => {
      if (el.dataset.layout === last) return;
      last = el.dataset.layout;
      setCompactLayout(/^(akis|odak)$/.test(last || ''));
      setPref(null);
      try {
        localStorage.removeItem(COLLAPSE_KEY);
      } catch {
        /* ignore */
      }
    });
    mo.observe(el, { attributes: true, attributeFilter: ['data-layout'] });
    return () => mo.disconnect();
  }, []);
  const collapsed = pref ?? compactLayout;
  const setCollapsed = (f: (c: boolean) => boolean) => {
    const next = f(collapsed);
    setPref(next);
    try {
      localStorage.setItem(COLLAPSE_KEY, next ? '1' : '0');
    } catch {
      /* ignore */
    }
  };
  useEffect(() => {
    document.documentElement.dataset.side = collapsed ? 'collapsed' : 'open';
  }, [collapsed]);
  useEffect(() => () => void delete document.documentElement.dataset.side, []);
  return { collapsed, setCollapsed };
}

const PHONE_Q = '(max-width: 639px)';
export const usePhone = () =>
  useSyncExternalStore(
    (cb) => {
      const m = window.matchMedia(PHONE_Q);
      m.addEventListener('change', cb);
      return () => m.removeEventListener('change', cb);
    },
    () => window.matchMedia(PHONE_Q).matches,
    () => false
  );

export function useSearchShortcut(open: () => void) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      const isK = (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k';
      if (!isK && (e.key !== '/' || ['INPUT', 'TEXTAREA', 'SELECT'].includes(t.tagName) || t.isContentEditable)) return;
      e.preventDefault();
      open();
    };
    window.addEventListener('medsoru:search', open);
    document.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener('medsoru:search', open);
      document.removeEventListener('keydown', onKey);
    };
    // open: setState sarmalayıcısı; ilk değer yeterli
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
}
