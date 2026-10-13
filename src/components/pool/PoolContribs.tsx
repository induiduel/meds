import React, { useState } from 'react';
import { PoolEvent, PoolSummary, fullTime, initials, relTime, shortName, toneOf } from './poolModel';

/** Tek katkı satırı: baş harf · kim · ne yaptı · ne zaman · metin */
export const PoolEventItem: React.FC<{ e: PoolEvent; now: number; showQ?: boolean }> = ({ e, now, showQ }) => {
  const key = e.uid || e.who.toLocaleLowerCase('tr-TR');
  return (
    <>
      <span className={`pv-av t${toneOf(key)}`} aria-hidden>{initials(e.who)}</span>
      <span className="pv-ev-main">
        <span className="pv-ev-line">
          <b>{shortName(e.who)}</b> {showQ && e.qno ? <span className="pv-ev-q">#{e.qno} · </span> : null}
          <span className="pv-ev-act">{e.action}</span>
          {e.at > 0 && <time className="pv-ev-t" dateTime={new Date(e.at).toISOString()} title={fullTime(e.at)}> · {relTime(e.at, now)}</time>}
        </span>
        {e.text && <span className="pv-ev-txt">{e.text}</span>}
      </span>
    </>
  );
};

/**
 * Katkılar şeridi: sorunun kimden, ne zaman, hangi parçayla büyüdüğü.
 * Varsayılan son 3 katkı; "Tümü" ile hepsi. Metinler QuestionCard'ın üstünde, kısa ve okunur.
 */
export const PoolContribs: React.FC<{ sum: PoolSummary; now: number }> = ({ sum, now }) => {
  const [all, setAll] = useState(false);
  const ev = sum.events;
  if (!ev.length) {
    return <p className="pv-contrib-empty">Henüz katkı yok. İlk parçayı aşağıdan ekleyebilirsin.</p>;
  }
  const list = all ? ev : ev.slice(0, 3);
  const listId = `pv-contrib-${sum.q.id}`;
  return (
    <section className="pv-contrib" aria-label="Katkılar">
      <div className="pv-contrib-h">
        <h3>Katkılar <span>{ev.length}</span></h3>
        <span className="pv-contrib-sub">{sum.people.length} kişi</span>
        {ev.length > 3 && (
          <button type="button" className="pv-link" aria-expanded={all} aria-controls={listId} onClick={() => setAll((v) => !v)}>
            {all ? 'Daralt' : `Tümü (${ev.length})`}
          </button>
        )}
      </div>
      <ol className="pv-ev-list" id={listId}>
        {list.map((e) => (
          <li key={e.id} className="pv-ev"><PoolEventItem e={e} now={now} /></li>
        ))}
      </ol>
    </section>
  );
};
