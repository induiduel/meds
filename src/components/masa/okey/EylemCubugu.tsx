/** Eylem çubuğu: yalnız geçerli düğmeler etkin; sıra bende değilken "Sıra: <ad>" yazar. */
import React from 'react';

export interface Eylem { ad: string; etiket: string; ikon: React.ReactNode; etkin: boolean; birincil?: boolean; asistan?: boolean; ipucu?: string; calis(): void }

export default function EylemCubugu({ eylemler, durum, kisa, children }: { eylemler: Eylem[]; durum: string; kisa: boolean; children?: React.ReactNode }) {
  return (
    <div className={`om-eylem${kisa ? ' om-eylem--kisa' : ''}`} role="toolbar" aria-label="Hamleler">
      <div className="om-eylem-bilgi"><span className="om-eylem-durum" aria-live="polite">{durum}</span>{children}</div>
      <div className="om-eylem-dugmeler">
        {eylemler.map((e) => (
          <button key={e.ad} type="button" className={`om-dugme${e.birincil && e.etkin ? ' om-dugme--birincil' : ''}${e.asistan ? ' om-dugme--asistan' : ''}`} disabled={!e.etkin} onClick={e.calis} title={e.ipucu || e.etiket} aria-label={e.etiket} data-om-eylem={e.ad}>
            {e.ikon}<span className="om-dugme-yazi">{e.etiket}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
