/**
 * Sayfa kodunu önden yükleme: sekmeye basılı tutunca (pointerdown) ve uygulama boştayken sık sayfaların
 * parçaları indirilir → sekme değişimi beklemesiz açılır. App.tsx'teki React.lazy içe aktarımlarıyla aynı
 * modüller; Vite aynı parçayı paylaşır, ikinci kez indirmez. Yavaş/kısıtlı bağlantıda boşta yükleme yapılmaz.
 */
import type { AppRoute } from './router';
import { getNetState } from './services/net';

const LOADERS: Partial<Record<AppRoute, () => Promise<unknown>>> = {
  learn: () => import('./components/learn/InteractiveDeckView'),
  flashcards: () => import('./components/flashcards/FlashcardsView'),
  past_exams: () => import('./components/PastExamsView'),
  study: () => import('./components/study/StudyHub'),
  glossary: () => import('./components/encyclopedia/MedicalEncyclopediaView'),
  ornek_sorular: () => import('./components/PracticeQuestionsView'),
  summaries: () => import('./components/LectureSummariesView'),
  kazanimlar: () => import('./components/KazanimlarView'),
  diseases: () => import('./components/diseases/DiseasesView'),
  practice: () => import('./components/PracticeMode'),
  stats: () => import('./components/stats/StatsView'),
  settings: () => import('./components/settings/ProfileSettingsView'),
  leaderboard: () => import('./components/LeaderboardView'),
};
const done = new Set<AppRoute>();

export function prefetchRoute(r: AppRoute) {
  if (done.has(r)) return;
  const l = LOADERS[r];
  if (!l) return;
  done.add(r);
  l().catch(() => done.delete(r));
}

/** Açılıştan sonra boşta: alt gezinmedeki sayfalar, ardından sık kullanılanlar (kısıtlı veri modunda yapılmaz). */
export function prefetchIdle() {
  const conn = (navigator as any).connection;
  if (conn?.saveData || /2g/.test(conn?.effectiveType || '') || getNetState() !== 'online') return;
  const order: AppRoute[] = ['learn', 'flashcards', 'past_exams', 'study', 'glossary', 'ornek_sorular', 'summaries'];
  const idle = (cb: () => void) => ((window as any).requestIdleCallback ? (window as any).requestIdleCallback(cb, { timeout: 4000 }) : window.setTimeout(cb, 1500));
  let i = 0;
  const step = () => {
    if (i >= order.length || getNetState() !== 'online') return;
    prefetchRoute(order[i++]);
    idle(step);
  };
  window.setTimeout(() => idle(step), 3500);
}
