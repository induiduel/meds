import React from 'react';
import type { Ton } from './Rozet';

/** Sayı kartı. git verilirse tıklanır (düğme olur) */
export const IstatistikKart: React.FC<{ etiket: string; deger: React.ReactNode; alt?: React.ReactNode; ton?: Ton; ikon?: React.ReactNode; onClick?: () => void; yukleniyor?: boolean }> = ({ etiket, deger, alt, ton = 'notr', ikon, onClick, yukleniyor }) => {
  const ic = (
    <>
      <span className="m16-istat-etiket">{ikon}{etiket}</span>
      <span className="m16-istat-deger">{yukleniyor ? <span className="m16-iskelet-tek" /> : deger}</span>
      {alt && <span className="m16-istat-alt">{alt}</span>}
    </>
  );
  return onClick
    ? <button type="button" className={`m16-istat t-${ton}`} onClick={onClick}>{ic}</button>
    : <div className={`m16-istat t-${ton}`}>{ic}</div>;
};

export const IstatistikIzgara: React.FC<{ children: React.ReactNode }> = ({ children }) => <div className="m16-istat-izgara">{children}</div>;
