import React from 'react';

/**
 * Çıkmış sorunun kök ekleri: tablo ve görseller (kayıtta `tablo` / `tablolar`, `gorseller`).
 * Tablo hücreleri metindir; görseller `public/cikmis-gorsel/` altından gelir, dokununca tam boyut açılır.
 */
export interface SoruTablosu {
  baslik?: string | null;
  sutunlar: string[];
  satirlar: string[][];
}
export interface SoruGorseli {
  src: string;
  alt?: string;
  kaynak?: string;
}

function tablolar(q: any): SoruTablosu[] {
  const t = [q?.tablo, ...(Array.isArray(q?.tablolar) ? q.tablolar : [])];
  return t.filter((x): x is SoruTablosu => Boolean(x && Array.isArray(x.sutunlar) && Array.isArray(x.satirlar) && x.satirlar.length));
}
function gorseller(q: any): SoruGorseli[] {
  return (Array.isArray(q?.gorseller) ? q.gorseller : []).filter((g: any) => g && typeof g.src === 'string' && g.src);
}

export function soruEkiVar(q: any): boolean {
  return tablolar(q).length > 0 || gorseller(q).length > 0;
}

export const SoruEkleri: React.FC<{ q: any }> = ({ q }) => {
  const T = tablolar(q);
  const G = gorseller(q);
  if (!T.length && !G.length) return null;
  return (
    <div className="ck-ekler">
      {T.map((t, i) => (
        <div className="ck-tablo-kap" key={`t${i}`} role="region" aria-label={t.baslik || 'Soru tablosu'} tabIndex={0}>
          <table className="ck-tablo">
            {t.baslik ? <caption>{t.baslik}</caption> : null}
            <thead>
              <tr>{t.sutunlar.map((s, j) => <th key={j} scope="col">{s}</th>)}</tr>
            </thead>
            <tbody>
              {t.satirlar.map((r, j) => (
                <tr key={j}>{r.map((h, k) => <td key={k}>{h}</td>)}</tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
      {G.map((g, i) => (
        <figure className="ck-gorsel" key={`g${i}`}>
          <a href={g.src} target="_blank" rel="noopener noreferrer" aria-label="Görseli tam boyut aç">
            <img src={g.src} alt={g.alt || 'Soru görseli'} loading="lazy" decoding="async" />
          </a>
          {g.alt ? <figcaption>{g.alt}</figcaption> : null}
        </figure>
      ))}
    </div>
  );
};
