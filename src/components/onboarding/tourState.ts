/** Hoş geldin turunun durumu (profilde eşitlenir: userKvSync `medsoru_tour_v1`). Tur bileşeni tembel yüklenir; bu dosya küçük kalır. */
export const TOUR_KEY = 'medsoru_tour_v1';

export const tourSeen = () => {
  try {
    return !!localStorage.getItem(TOUR_KEY);
  } catch {
    return true;
  }
};

export const markTourSeen = (how: 'done' | 'skipped') => {
  try {
    localStorage.setItem(TOUR_KEY, `${how}:${new Date().toISOString()}`);
  } catch {
    /* özel pencere */
  }
};

/** Turu yeniden başlat (App dinler) */
export const startWelcomeTour = () => window.dispatchEvent(new CustomEvent('medsoru:tour'));
