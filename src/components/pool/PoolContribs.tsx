import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';
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
 * Katkılar: varsayılan kapalı tek satırlık açılır öğe ("Katkılar · 3 kişi · 7 kayıt").
 * Açılınca yeniden eskiye tüm katkılar. Soru kartının önünde yer kaplamaz.
 */
export const PoolContribs: React.FC<{ sum: PoolSummary; now: number }> = ({ sum, now }) => {
  const [open, setOpen] = useState(false);
  const ev = sum.events;
  const listId = `pv-contrib-${sum.q.id}`;
  if (!ev.length) return <p className="pv-note">Henüz katkı yok — ilk parçayı aşağıdaki karttan ekleyebilirsin.</p>;
  return (
    <section className={`pv-contrib ${open ? 'is-open' : ''}`} aria-label="Katkılar">
      <button type="button" className="pv-contrib-h" aria-expanded={open} aria-controls={listId} onClick={() => setOpen((v) => !v)}>
        <span className="pv-contrib-t">Katkılar</span>
        <span className="pv-contrib-sub">{sum.people.length} kişi · {ev.length} kayıt</span>
        <ChevronDown className="pv-chev" aria-hidden />
      </button>
      {open && (
        <ol className="pv-ev-list" id={listId}>
          {ev.map((e) => (
            <li key={e.id} className="pv-ev"><PoolEventItem e={e} now={now} /></li>
          ))}
        </ol>
      )}
    </section>
  );
};
