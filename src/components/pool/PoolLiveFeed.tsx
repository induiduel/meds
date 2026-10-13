import React, { useMemo } from 'react';
import { DAY, PoolSummary, initials, shortName, toneOf } from './poolModel';
import { PoolEventItem } from './PoolContribs';

/**
 * Canlı akış (≥1440px, bölmeli görünüm): tüm sorulardaki son katkılar + haftanın katkıcıları.
 * Bir olaya dokunmak o soruyu ayrıntı bölmesinde açar.
 */
export const PoolLiveFeed: React.FC<{ sums: PoolSummary[]; now: number; onOpen: (id: string) => void }> = ({ sums, now, onOpen }) => {
  const { feed, top } = useMemo(() => {
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
  }, [sums, now]);

  return (
    <aside className="pv-feed" aria-label="Canlı akış">
      <h2 className="pv-feed-h"><span className="pv-dot" aria-hidden />Canlı akış</h2>
      {feed.length === 0 ? (
        <p className="pv-contrib-empty">Henüz zamanı belli katkı yok.</p>
      ) : (
        <ol className="pv-ev-list">
          {feed.map((e) => (
            <li key={e.id}>
              <button type="button" className="pv-ev is-btn" onClick={() => onOpen(e.qid)} aria-label={`${e.who}, soru ${e.qno}: ${e.action}. Soruyu aç`}>
                <PoolEventItem e={e} now={now} showQ />
              </button>
            </li>
          ))}
        </ol>
      )}
      {top.length > 0 && (
        <>
          <h2 className="pv-feed-h">Bu hafta en çok katkı</h2>
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
    </aside>
  );
};
