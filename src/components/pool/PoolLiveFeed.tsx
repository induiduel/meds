import React, { useMemo } from 'react';
import { Sheet } from '../ui/Sheet';
import { DAY, HOUR, PoolSummary, activityIn, initials, shortName, toneOf } from './poolModel';
import { PoolEventItem } from './PoolContribs';

/** Araç çubuğundaki "Etkinlik" düğmesinin özeti: son 1 saat, yoksa son 24 saat */
export function usePoolActivity(sums: PoolSummary[], now: number) {
  return useMemo(() => {
    const h = activityIn(sums, HOUR, now);
    if (h.parts || h.newQ) return { label: 'Son 1 saat', recent: true, ...h };
    const d = activityIn(sums, DAY, now);
    if (d.parts || d.newQ) return { label: 'Son 24 saat', recent: false, ...d };
    return null;
  }, [sums, now]);
}

/**
 * Havuz etkinliği (sayfa yerine tek bir sessiz düğmenin arkasında, Sheet):
 * dönem özeti · tüm sorulardaki son katkılar · haftanın katkıcıları. Bir olaya dokunmak o soruyu açar.
 */
export const PoolLiveFeed: React.FC<{
  open: boolean;
  onClose: () => void;
  sums: PoolSummary[];
  now: number;
  activity: ReturnType<typeof usePoolActivity>;
  onOpen: (id: string) => void;
}> = ({ open, onClose, sums, now, activity, onOpen }) => {
  const { feed, top } = useMemo(() => {
    if (!open) return { feed: [], top: [] as [string, { name: string; n: number }][] };
    const all = sums.flatMap((s) => s.events.filter((e) => e.at > 0));
    all.sort((a, b) => b.at - a.at);
    const weekFrom = now - 7 * DAY;
    const tally = new Map<string, { name: string; n: number }>();
    for (const e of all) {
      if (e.at < weekFrom) break;
      const k = e.uid || e.who.toLocaleLowerCase('tr-TR');
      const t = tally.get(k) || { name: e.who, n: 0 };
      t.n++;
      tally.set(k, t);
    }
    const top = [...tally.entries()].filter(([, t]) => t.name !== 'Anonim').sort((a, b) => b[1].n - a[1].n).slice(0, 3);
    return { feed: all.slice(0, 30), top };
  }, [open, sums, now]);

  return (
    <Sheet open={open} onClose={onClose} title="Havuz etkinliği" subtitle={activity ? `${activity.label}: ${activity.newQ} yeni soru · ${activity.parts} parça · ${activity.people} kişi` : 'Son 24 saatte etkinlik yok'} width={480}>
      <div className="pv-feed">
        {feed.length === 0 ? (
          <p className="pv-note">Henüz zamanı belli katkı yok.</p>
        ) : (
          <>
            <h3 className="pv-feed-h">Son katkılar</h3>
            <ol className="pv-ev-list">
              {feed.map((e) => (
                <li key={e.id}>
                  <button type="button" className="pv-ev is-btn" onClick={() => onOpen(e.qid)} aria-label={`${e.who}, soru ${e.qno}: ${e.action}. Soruyu aç`}>
                    <PoolEventItem e={e} now={now} showQ />
                  </button>
                </li>
              ))}
            </ol>
          </>
        )}
        {top.length > 0 && (
          <>
            <h3 className="pv-feed-h">Bu hafta en çok katkı</h3>
            <ol className="pv-top">
              {top.map(([k, t], i) => (
                <li key={k}>
                  <span className="pv-top-r">{i + 1}</span>
                  <span className={`pv-av t${toneOf(k)}`} aria-hidden>{initials(t.name)}</span>
                  <span className="pv-top-n">{shortName(t.name)}</span>
                  <span className="pv-top-p">{t.n} katkı</span>
                </li>
              ))}
            </ol>
          </>
        )}
      </div>
    </Sheet>
  );
};
