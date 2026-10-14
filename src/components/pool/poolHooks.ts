import { useEffect, useMemo, useState } from 'react';
import { ApiService } from '../../services/api';
import type { QuestionItem } from '../../types';

/**
 * Soru havuzu ekranlarının (PoolView klasik + v12/PoolV12) paylaştığı küçük kancalar.
 * Veri mantığı tek yerde: iki görünüm aynı birleştirme önerilerini ve ders seçeneklerini görür.
 */

const GENERIC_DISC = /^(belirtilmedi|genel|belirsiz|)$/i;

export function useMedia(query: string): boolean {
  const get = () => typeof window !== 'undefined' && !!window.matchMedia?.(query).matches;
  const [m, setM] = useState(get);
  useEffect(() => {
    const mq = window.matchMedia?.(query);
    if (!mq) return;
    const on = () => setM(mq.matches);
    on();
    mq.addEventListener?.('change', on);
    return () => mq.removeEventListener?.('change', on);
  }, [query]);
  return m;
}

export type PoolCluster = { id: string; committeeId: string; sourceQuestionIds: string[]; mergedQuestionCount: number; clusterTitle: string };

/** Birleştirme önerileri (sunucu motoru: aynı soruyu anlatan kayıtlar) + soru → küme eşlemi */
export function usePoolClusters(committeeId: string, questionCount: number) {
  const [clusters, setClusters] = useState<PoolCluster[]>([]);
  useEffect(() => {
    let alive = true;
    const t = window.setTimeout(() => {
      ApiService.getPoolQuestionClusters()
        .then((list: any[]) => { if (alive) setClusters((list || []).filter((c) => c.committeeId === committeeId && c.mergedQuestionCount >= 2)); })
        .catch(() => {});
    }, 400);
    return () => { alive = false; window.clearTimeout(t); };
  }, [committeeId, questionCount]);
  const clusterOf = useMemo(() => {
    const m = new Map<string, { id: string; size: number }>();
    for (const c of clusters) for (const qid of c.sourceQuestionIds || []) m.set(qid, { id: c.id, size: c.mergedQuestionCount });
    return m;
  }, [clusters]);
  return { clusters, clusterOf };
}

/** Ders süzgeci kurulun gerçek derslerinden (sayılarıyla, çoktan aza) */
export function poolDisciplineOptions(all: QuestionItem[]): { id: string; label: string; count?: number }[] {
  const m = new Map<string, number>();
  for (const q of all) {
    const d = (q.discipline || '').trim();
    if (d && !GENERIC_DISC.test(d)) m.set(d, (m.get(d) || 0) + 1);
  }
  return [{ id: 'Tümü', label: 'Tümü' }, ...[...m].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'tr')).map(([d, c]) => ({ id: d, label: d, count: c }))];
}
