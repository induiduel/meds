/**
 * Ders PDF görünümü adreste tutulur: ?pdf=1 (yalnız PDF) | ?pdf=yan (yan yana), ?pdfs=<sayfa>, büyütülmüş PDF ?pdftam=1.
 * Başka sayfaya gidip Geri ile dönünce ders aynı PDF görünümünde, aynı sayfada açılır. replaceState kullanılır
 * (geçmişe kayıt eklenmez); Safari'nin sık replaceState sınırı için yazımlar birleştirilip ertelenir.
 */
export type PdfAdresMod = 'pdf' | 'split';

export const pdfAdresOku = (): { mode?: PdfAdresMod; page?: number; tam: boolean } => {
  try {
    const sp = new URLSearchParams(window.location.search);
    const v = sp.get('pdf');
    return { mode: v === 'yan' ? 'split' : v === '1' ? 'pdf' : undefined, page: Number(sp.get('pdfs')) || undefined, tam: sp.get('pdftam') === '1' };
  } catch {
    return { tam: false };
  }
};

let bekleyen: Record<string, string | null> = {};
let zaman = 0;
let yol = '';
export const pdfAdresYaz = (degis: Record<string, string | null>) => {
  if (typeof window === 'undefined') return;
  if (yol !== window.location.pathname) bekleyen = {};
  yol = window.location.pathname;
  bekleyen = { ...bekleyen, ...degis };
  window.clearTimeout(zaman);
  zaman = window.setTimeout(() => {
    const d = bekleyen;
    bekleyen = {};
    try {
      if (window.location.pathname !== yol) return; // bu arada başka sayfaya geçildi
      const sp = new URLSearchParams(window.location.search);
      for (const [k, v] of Object.entries(d)) (v === null ? sp.delete(k) : sp.set(k, v));
      const q = sp.toString();
      const next = yol + (q ? `?${q}` : '') + window.location.hash;
      if (next !== yol + window.location.search + window.location.hash) window.history.replaceState(window.history.state, '', next);
    } catch {
      /* korumalı çerçeve */
    }
  }, 300);
};
