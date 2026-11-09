import React from 'react';
import { PISTI_RENK_SIMGE, degerYazi, kartAd, type PistiKart } from '../../../services/masa/motor/pisti';

const KIRMIZI = new Set(['kupa', 'karo']);

/** Klasik oyun kartı (özgün, sade): köşelerde değer + simge, ortada büyük simge ya da resimli kartta harf çerçevesi */
export function Kart({ kart, className = '', style, ...p }: { kart: PistiKart } & React.HTMLAttributes<HTMLDivElement>) {
  const s = PISTI_RENK_SIMGE[kart.renk];
  const y = degerYazi(kart.d);
  const resimli = kart.d >= 11;
  return (
    <div className={`pk-kart${KIRMIZI.has(kart.renk) ? ' is-kirmizi' : ''} ${className}`} style={style} aria-label={kartAd(kart)} role="img" {...p}>
      <span className="pk-kose"><b>{y}</b><i>{s}</i></span>
      {resimli
        ? <span className="pk-resim" aria-hidden="true"><b>{y}</b><i>{s}</i></span>
        : <span className="pk-orta" aria-hidden="true">{s}</span>}
      <span className="pk-kose pk-kose-alt"><b>{y}</b><i>{s}</i></span>
    </div>
  );
}

export function KartArka({ className = '', style }: { className?: string; style?: React.CSSProperties }) {
  return <div className={`pk-kart pk-arka ${className}`} style={style} aria-hidden="true" />;
}
