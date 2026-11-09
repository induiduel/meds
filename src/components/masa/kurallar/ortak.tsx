/** Kural sayfalarının ortak örnek bileşeni (MasaKurallar.tsx'teki `Taslar` ile aynı görünüm) */
import React from 'react';
import { Check, X } from 'lucide-react';
import { VARSAYILAN_RENKLER } from '../../../services/masa/tipler';
import { TasOrnek } from '../kabukOrtak';

export type T = [number, 0 | 1 | 2 | 3];
export const renkSec = (renkler?: string[]) => (renkler && renkler.length === 4 ? renkler : [...VARSAYILAN_RENKLER]);

export function Taslar({ t, ad, iyi, okey, rk }: { t: T[]; ad: string; iyi?: boolean; okey?: { s: number; r: 0 | 1 | 2 | 3 }; rk: string[] }) {
  return (
    <figure className={`mk-ornek${iyi === false ? ' is-kotu' : iyi ? ' is-iyi' : ''}`}>
      <div className="mk-ornek-sira">{t.map(([s, r], i) => <TasOrnek key={i} s={s} r={r} renkler={rk} boy={30} okey={okey} />)}</div>
      <figcaption>{iyi !== undefined && (iyi ? <Check size={15} /> : <X size={15} />)} {ad}</figcaption>
    </figure>
  );
}
