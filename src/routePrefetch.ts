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
  spots: () => import('./components/spots/ExamSpotsView'),
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

/** Açılıştan sonra boşta: kullanıcı etkileşimini boğmadan, uzun aralıklarla ve tarayıcı boştayken önden yükler. */
export function prefetchIdle() {
  if (typeof window === 'undefined') return;
  const conn = (navigator as any).connection;
  if (conn?.saveData || /2g/.test(conn?.effectiveType || '') || getNetState() !== 'online') return;
  const order: AppRoute[] = [
    'past_exams',
    'learn',
    'flashcards',
    'diseases',
    'glossary',
    'study',
    'summaries',
    'kazanimlar',
    'practice',
    'stats',
    'settings',
  ];
  let i = 0;
  const step = () => {
    if (i >= order.length || getNetState() !== 'online') return;
    const nextRoute = order[i++];
    const runner = () => {
      prefetchRoute(nextRoute);
      window.setTimeout(step, 4500);
    };
    if ('requestIdleCallback' in window) {
      (window as any).requestIdleCallback(runner, { timeout: 4000 });
    } else {
      runner();
    }
  };
  window.setTimeout(step, 8000);
}
