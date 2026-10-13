import { useEffect, useState } from 'react';
import { REVIEW_EVENT, REVIEW_KEY, reviewCounts } from '../services/learnReview';

/** Hata defteri sayıları (deste → açık / vadesi gelmiş); defter değişince ya da başka cihazdan eşitlenince tazelenir */
export function useReviewCounts() {
  const [counts, setCounts] = useState(() => reviewCounts());
  useEffect(() => {
    const refresh = () => setCounts(reviewCounts());
    const onStorage = (e: StorageEvent) => e.key === REVIEW_KEY && refresh();
    window.addEventListener(REVIEW_EVENT, refresh);
    window.addEventListener('storage', onStorage);
    const t = window.setInterval(refresh, 10 * 60_000); // gün dönümünde vadesi gelenler
    return () => {
      window.removeEventListener(REVIEW_EVENT, refresh);
      window.removeEventListener('storage', onStorage);
      window.clearInterval(t);
    };
  }, []);
  const total = Object.values(counts).reduce((a, c) => ({ open: a.open + c.open, due: a.due + c.due }), { open: 0, due: 0 });
  return { counts, total };
}
