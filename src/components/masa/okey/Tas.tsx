/** Okey taşı: masa dışında (ayar önizlemesi) da tek başına çizilebilir. Renk = `renkler[tas.r]`; her rengin ayrı biçimi var. */
import React from 'react';
import type { Renk, Tas } from '../../../services/masa/tipler';
import '../../../styles/masa/okey-tas.css';

/** Taşın yükseklik / genişlik oranı */
export const TAS_ORAN = 1.38;

const KLASIK_ISARET = [
  <circle key="0" cx="12" cy="12" r="7" />,
  <path key="1" d="M12 3.5 20.5 12 12 20.5 3.5 12Z" />,
  <path key="2" d="M12 4.5 20.5 19.5h-17Z" />,
  <rect key="3" x="5" y="5" width="14" height="14" rx="2" />,
];
/* kitty: fiyonk, kalp, çiçek, pati (özgün çizim) */
const KITTY_ISARET = [
  <g key="0"><path d="M11 12 3.5 6.5c-1-.7-2 .1-2 1.2v8.6c0 1.1 1 1.9 2 1.2Z" /><path d="M13 12l7.5-5.500c1-.7 2 .1 2 1.2v8.6c0 1.1-1 1.9-2 1.200Z" /><circle cx="12" cy="12" r="2.8" /></g>,
  <path key="1" d="M12 20.500C5.5 15.8 2.5 12.5 2.5 8.8 2.5 6 4.6 4 7.2 4c1.9 0 3.7 1 4.8 2.700C13.1 5 14.9 4 16.8 4c2.6 0 4.7 2 4.7 4.8 0 3.7-3 7-9.5 11.700Z" />,
  <g key="2"><circle cx="12" cy="6" r="3.6" /><circle cx="17.7" cy="10.2" r="3.6" /><circle cx="15.5" cy="16.9" r="3.6" /><circle cx="8.5" cy="16.9" r="3.6" /><circle cx="6.3" cy="10.2" r="3.6" /><circle cx="12" cy="12" r="2.6" fill="#fff" fillOpacity=".85" /></g>,
  <g key="3"><ellipse cx="12" cy="15.5" rx="5.2" ry="4.3" /><circle cx="5.3" cy="10.5" r="2.3" /><circle cx="9.5" cy="6.3" r="2.3" /><circle cx="14.5" cy="6.3" r="2.3" /><circle cx="18.7" cy="10.5" r="2.3" /></g>,
];

function Isaret({ r, tema }: { r: number; tema: string }) {
  return <svg className="om-tas-isaret" viewBox="0 0 24 24" aria-hidden="true">{(tema === 'kitty' ? KITTY_ISARET : KLASIK_ISARET)[r] ?? KLASIK_ISARET[0]}</svg>;
}
const Yildiz = () => <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2.5 2.9 6 6.6.900-4.8 4.6 1.2 6.5-5.9-3.2-5.9 3.2 1.2-6.500L2.5 9.400l6.6-.900Z" /></svg>;
/* sahte okey: klasikte dört yapraklı yonca, kitty'de kedi yüzü */
const Yonca = () => (
  <svg className="om-tas-sahte" viewBox="0 0 24 24" aria-hidden="true">
    <circle cx="12" cy="6.8" r="4.3" /><circle cx="12" cy="17.2" r="4.3" /><circle cx="6.8" cy="12" r="4.3" /><circle cx="17.2" cy="12" r="4.3" /><circle cx="12" cy="12" r="2.2" fill="#fff" fillOpacity=".8" />
  </svg>
);
export const KediYuzu = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 48 44" aria-hidden="true">
    <path d="M6 20 4.5 5.5 17 10.500a20 16 0 0 1 14 0L43.5 5.5 42 20a20 16.5 0 1 1-36 0Z" fill="#fff" stroke="#5b3a46" strokeWidth="2" strokeLinejoin="round" />
    <ellipse cx="16" cy="25" rx="1.8" ry="2.6" fill="#5b3a46" /><ellipse cx="32" cy="25" rx="1.8" ry="2.6" fill="#5b3a46" />
    <ellipse cx="24" cy="29.5" rx="2.2" ry="1.5" fill="#f2b632" />
    <path d="M4 26h7M5 31l6-1.500M44 26h-7M43 31l-6-1.5" stroke="#5b3a46" strokeWidth="1.5" strokeLinecap="round" />
    <g fill="#e8456b" stroke="#a82547" strokeWidth="1"><path d="m35 9-7-4.500v9Z" /><path d="m35 9 7-4.500v9Z" /><circle cx="35" cy="9" r="2.6" /></g>
  </svg>
);

export interface TasGorselProps {
  tas: Tas;
  renkler: string[];
  tema: string;
  /** px genişlik */
  boy?: number;
  /** 101: okey bilgisi verilirse okey taşı yıldızla, sahte okey temsil ettiği sayıyla işaretlenir */
  okey?: { s: number; r: Renk };
  kapali?: boolean;
  className?: string;
  style?: React.CSSProperties;
}

export function TasGorsel({ tas, renkler, tema, boy, okey, kapali, className, style }: TasGorselProps) {
  const t = tema === 'kitty' ? 'kitty' : 'klasik';
  const sahte = tas.s === 0;
  const joker = !!okey && !sahte && tas.s === okey.s && tas.r === okey.r;
  const renk = renkler[sahte && okey ? okey.r : tas.r] || '#1d1d1f';
  const st = { ...(boy ? { '--om-b': `${boy}px` } : null), '--om-renk': renk, ...style } as React.CSSProperties;
  const sinif = `om-tas om-tas--${t}${kapali ? ' om-tas--kapali' : ''}${joker ? ' om-tas--okey' : ''}${sahte ? ' om-tas--sahteokey' : ''}${className ? ` ${className}` : ''}`;
  if (kapali) {
    return <span className={sinif} style={st}><span className="om-tas-yuz">{t === 'kitty' ? <KediYuzu className="om-tas-arka" /> : <span className="om-tas-arka om-tas-arka--klasik" />}</span></span>;
  }
  const ad = sahte ? 'Sahte okey' : `${['1.', '2.', '3.', '4.'][tas.r]} renk ${tas.s}${joker ? ' (okey)' : ''}`;
  return (
    <span className={sinif} style={st} role="img" aria-label={ad}>
      <span className="om-tas-yuz">
        {sahte ? (
          <>
            {t === 'kitty' ? <KediYuzu className="om-tas-sahte om-tas-sahte--kedi" /> : <Yonca />}
            {okey && <span className="om-tas-alt">{okey.s}</span>}
          </>
        ) : (
          <>
            <span className={`om-tas-sayi${tas.s > 9 ? ' om-tas-sayi--iki' : ''}`}>{tas.s}</span>
            <Isaret r={tas.r} tema={t} />
          </>
        )}
        {joker && <span className="om-tas-rozet" title="Okey"><Yildiz /></span>}
        {tas.yerine && <span className="om-tas-yerine" style={{ color: renkler[tas.yerine.r] }}>{tas.yerine.s}</span>}
      </span>
    </span>
  );
}
export default TasGorsel;
