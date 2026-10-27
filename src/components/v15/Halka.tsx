import React from 'react';

/** v15 ilerleme halkası (bileşen kaydı: docs/V15_PLAN.md). Renk: vurgu; %100 iken dolu. Boyut CSS ile (--h15). */
export const Halka: React.FC<{ pct: number; etiket: string; boyut?: number; yazi?: React.ReactNode }> = ({ pct, etiket, boyut = 36, yazi }) => {
  const r = 15.5;
  const c = 2 * Math.PI * r;
  const p = Math.max(0, Math.min(100, Math.round(pct)));
  return (
    <span className={`v15-halka${p >= 100 ? ' is-tam' : ''}`} style={{ '--h15': `${boyut}px` } as React.CSSProperties} role="img" aria-label={etiket}>
      <svg viewBox="0 0 36 36" aria-hidden="true">
        <circle cx="18" cy="18" r={r} className="v15-halka-bg" />
        {p > 0 && <circle cx="18" cy="18" r={r} className="v15-halka-fg" strokeDasharray={`${(c * p) / 100} ${c}`} />}
      </svg>
      <span className="v15-halka-v" aria-hidden="true">{yazi ?? p}</span>
    </span>
  );
};
