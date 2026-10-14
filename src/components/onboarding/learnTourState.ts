/** Öğren turlarının durumu (profilde eşitlenir: userKvSync `medsoru_learn_tour_*`). Tur bileşeni tembel yüklenir; bu dosya küçük kalır. */
import { navigateTo, ROUTE_PATHS } from '../../router';

export type LearnTourKind = 'library' | 'lesson';

export const LEARN_TOUR_KEYS: Record<LearnTourKind, string> = {
  library: 'medsoru_learn_tour_library_v1',
  lesson: 'medsoru_learn_tour_lesson_v1',
};

export const learnTourSeen = (kind: LearnTourKind) => {
  try {
    return !!localStorage.getItem(LEARN_TOUR_KEYS[kind]);
  } catch {
    return true;
  }
};

export const markLearnTourSeen = (kind: LearnTourKind, how: 'done' | 'skipped') => {
  try {
    localStorage.setItem(LEARN_TOUR_KEYS[kind], `${how}:${new Date().toISOString()}`);
  } catch {
    /* özel pencere */
  }
};

/** Turu yeniden başlat (InteractiveDeckView dinler). `catalog: true` → doğrudan etkileşim rehberi */
export const startLearnTour = (kind: LearnTourKind, catalog = false) =>
  window.dispatchEvent(new CustomEvent('medsoru:learn-tour', { detail: { kind, catalog } }));

/** Profil › "Öğren turu": Öğren sayfasına git, kitaplık turunu baştan aç */
export const onLearnTour = () => {
  try {
    localStorage.removeItem(LEARN_TOUR_KEYS.library);
  } catch {
    /* özel pencere */
  }
  // Kitaplık açılınca tur kendiliğinden başlar (InteractiveDeckView, anahtar silindi)
  navigateTo(ROUTE_PATHS.learn);
};
