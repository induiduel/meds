import React from 'react';
import type { UnoDeger, UnoKart, UnoRenk } from '../../../services/masa/tipler';
import { UNO_DEGER_AD } from '../../../services/masa/motor/unoAsistan';
import { temaAl, temaKod, UNO_SIRA, type UnoTemaTanim } from './temalar';
import '../../../styles/masa/uno-kart.css';

/** Renk körlüğü için renge özgü biçim: k daire, s üçgen, y kare, m baklava (merkez 0,0; yarıçap b) */
export function RenkBicimi({ renk, b = 5, fill = '#fff', stroke = 'rgba(0,0,0,.55)' }: { renk: UnoRenk; b?: number; fill?: string; stroke?: string }) {
  const o = { fill, stroke, strokeWidth: b * 0.28, strokeLinejoin: 'round' as const };
  if (renk === 'k') return <circle r={b} {...o} />;
  if (renk === 's') return <polygon points={`0,${-b * 1.1} ${b * 1.1},${b * 0.85} ${-b * 1.1},${b * 0.85}`} {...o} />;
  if (renk === 'y') return <rect x={-b * 0.9} y={-b * 0.9} width={b * 1.8} height={b * 1.8} rx={b * 0.15} {...o} />;
  return <polygon points={`0,${-b * 1.2} ${b * 1.05},0 0,${b * 1.2} ${-b * 1.05},0`} {...o} />;
}

/** Kartın sesli adı: "Mavi Yedi", "Joker" */
export const kartAdi = (kart: UnoKart, tema: string): string =>
  `${kart.renk ? temaAl(tema).renk[kart.renk].ad + ' ' : ''}${UNO_DEGER_AD[kart.deger]}`;

/** Değer simgesi; merkez (0,0), yaklaşık ±26 birim */
function Simge({ deger, fill, stroke, yazi, egik }: { deger: UnoDeger; fill: string; stroke: string; yazi: string; egik: boolean }) {
  if (deger === 'pas') {
    return (
      <g fill="none" strokeLinecap="round">
        <circle r="19" stroke={stroke} strokeWidth="11" />
        <line x1="-13" y1="13" x2="13" y2="-13" stroke={stroke} strokeWidth="11" />
        <circle r="19" stroke={fill} strokeWidth="6.5" />
        <line x1="-13" y1="13" x2="13" y2="-13" stroke={fill} strokeWidth="6.5" />
      </g>
    );
  }
  if (deger === 'yon') {
    const ok = '-21,-14 3,-14 3,-22 22,-8.5 3,5 3,-3 -21,-3';
    return (
      <g transform="rotate(-38)" fill={fill} stroke={stroke} strokeWidth="2.6" strokeLinejoin="round">
        <polygon points={ok} />
        <polygon points={ok} transform="rotate(180)" />
      </g>
    );
  }
  const metin = deger === 'joker' ? '★' : deger;
  const boy = deger.length === 1 ? 60 : deger === 'joker' ? 40 : 42;
  return (
    <g>
      <text
        x="0" y="0" dy=".36em" textAnchor="middle" fontSize={boy} fontWeight="900" fontFamily={yazi}
        fontStyle={egik ? 'italic' : 'normal'} fill={fill} stroke={stroke} strokeWidth="3" paintOrder="stroke" strokeLinejoin="round"
      >{metin}</text>
      {(deger === '6' || deger === '9') && <rect x="-13" y="24" width="26" height="4.5" rx="2" fill={fill} stroke={stroke} strokeWidth="1.4" />}
    </g>
  );
}

/** Köşe değeri (küçük); merkez (0,0) */
function Kose({ deger, fill, stroke, yazi }: { deger: UnoDeger; fill: string; stroke: string; yazi: string }) {
  if (deger === 'pas' || deger === 'yon') return <g transform="scale(.36)"><Simge deger={deger} fill={fill} stroke={stroke} yazi={yazi} egik={false} /></g>;
  return (
    <text x="0" y="0" dy=".36em" textAnchor="middle" fontSize={deger.length === 1 ? 19 : 14.5} fontWeight="900" fontFamily={yazi} fill={fill} stroke={stroke} strokeWidth="2.2" paintOrder="stroke" strokeLinejoin="round">
      {deger === 'joker' ? '★' : deger}
    </text>
  );
}

const KALKAN = 'M21 36 H79 V80 C79 104 62 117 50 123 C38 117 21 104 21 80 Z';

/** Orta amblem: tek renk kartta tema zemini, jokerde dört renk */
function Amblem({ tema, t, renk }: { tema: string; t: UnoTemaTanim; renk: UnoRenk | null }) {
  const r4 = UNO_SIRA.map((r) => t.renk[r].ana);
  if (tema === 'stitch') {
    // Hibiskus: beş yaprak + orta
    return (
      <g transform="translate(50 75)">
        {[0, 72, 144, 216, 288].map((a, i) => (
          <ellipse key={a} cx="0" cy="-27" rx="19" ry="27" transform={`rotate(${a})`} fill={renk ? t.amblem : r4[i % 4]} stroke={renk ? t.renk[renk].koyu : '#fff4e0'} strokeOpacity={renk ? 0.25 : 0.9} strokeWidth="1.2" />
        ))}
        <circle r="23" fill={t.amblem} />
        {!renk && <circle r="23" fill="none" stroke="#3b2a6b" strokeOpacity=".25" strokeWidth="1.5" />}
      </g>
    );
  }
  if (tema === 'buyucu') {
    if (!renk) {
      return (
        <g stroke="#c9a24a" strokeWidth="1.6" strokeLinejoin="round">
          <path d="M21 36 H50 V80 H21 Z" fill={r4[0]} />
          <path d="M50 36 H79 V80 H50 Z" fill={r4[1]} />
          <path d="M21 80 H50 V123 C38 117 21 104 21 80 Z" fill={r4[2]} />
          <path d="M50 80 H79 C79 104 62 117 50 123 Z" fill={r4[3]} />
          <path d={KALKAN} fill="none" strokeWidth="2.6" />
        </g>
      );
    }
    const c = t.renk[renk];
    return (
      <g>
        <path d={KALKAN} fill={c.ana} />
        <rect x="21" y="36" width="58" height="11" fill={c.ikincil} />
        <path d={KALKAN} fill="none" stroke="#c9a24a" strokeWidth="2.6" strokeLinejoin="round" />
        <path d="M26 52 H74 V80 C74 100 60 111 50 116.500 C40 111 26 100 26 80 Z" fill="none" stroke={c.ikincil} strokeOpacity=".55" strokeWidth="1" />
      </g>
    );
  }
  // Klasik: eğik oval
  if (!renk) {
    return (
      <g transform="translate(50 75) rotate(28)" stroke="#fff" strokeWidth="2">
        <path d="M0 0 V-57 A35 57 0 0 1 35 0 Z" fill={r4[0]} />
        <path d="M0 0 H35 A35 57 0 0 1 0 57 Z" fill={r4[3]} />
        <path d="M0 0 V57 A35 57 0 0 1 -35 0 Z" fill={r4[1]} />
        <path d="M0 0 H-35 A35 57 0 0 1 0 -57 Z" fill={r4[2]} />
      </g>
    );
  }
  return <ellipse cx="50" cy="75" rx="35" ry="57" transform="rotate(28 50 75)" fill={t.amblem} />;
}

/** Tema süsleri (zemin üstü, amblem altı) */
function Sus({ tema, renk, t }: { tema: string; renk: UnoRenk | null; t: UnoTemaTanim }) {
  if (tema === 'stitch') {
    const koyu = renk ? t.renk[renk].koyu : '#22184a';
    const yaprak = 'M0 0 C6 -10 20 -14 30 -8 C22 -6 18 -2 14 4 C10 2 4 1 0 0 Z';
    return (
      <g fill={koyu} fillOpacity=".38">
        <path d={yaprak} transform="translate(8 148) rotate(-58) scale(1.25)" />
        <path d={yaprak} transform="translate(4 136) rotate(-20) scale(.95)" />
        <path d={yaprak} transform="translate(92 2) rotate(122) scale(1.25)" />
        <path d={yaprak} transform="translate(96 14) rotate(160) scale(.95)" />
        <path d="M6 100 q10 -6 20 0 t20 0 t20 0 t20 0 t20 0" fill="none" stroke="#fff" strokeOpacity=".16" strokeWidth="2" />
      </g>
    );
  }
  if (tema === 'buyucu') {
    const yildiz = 'M0 -5 L1.300 -1.300 L5 0 L1.300 1.300 L0 5 L-1.300 1.300 L-5 0 L-1.300 -1.300 Z';
    const c = renk ? t.renk[renk].koyu : '#c9a24a';
    return (
      <g>
        <rect x="9" y="9" width="82" height="132" rx="4" fill="none" stroke="#b08d3c" strokeWidth=".9" />
        <g fill={c} fillOpacity=".6">
          <path d={yildiz} transform="translate(50 22) scale(.9)" />
          <path d={yildiz} transform="translate(33 26) scale(.5)" />
          <path d={yildiz} transform="translate(67 26) scale(.5)" />
          {/* şimşek */}
          <path d="M-2 -6 L3 -6 L0.500 -1 L4 -1 L-3 7 L-1 1 L-4 1 Z" transform="translate(15 76) scale(.8)" />
          <path d="M-2 -6 L3 -6 L0.500 -1 L4 -1 L-3 7 L-1 1 L-4 1 Z" transform="translate(85 76) scale(.8)" />
        </g>
      </g>
    );
  }
  return null;
}

function Yuz({ kart, tema }: { kart: UnoKart; tema: string }) {
  const t = temaAl(tema);
  const c = kart.renk ? t.renk[kart.renk] : null;
  const buyucu = tema === 'buyucu';
  const zemin = buyucu ? (c ? '#f1e3bf' : t.joker) : c ? c.ana : t.joker;
  const jokerMi = !c;
  // Orta simge rengi: klasik/tropik amblem açık → renkli simge; büyücüde kalkan koyu → parşömen simge
  const simgeFill = jokerMi ? '#fff' : buyucu ? (kart.renk === 's' ? '#1d1a16' : '#f6ecd0') : c!.ana;
  const simgeStroke = jokerMi ? '#16161a' : buyucu ? (kart.renk === 's' ? '#f6ecd0' : c!.koyu) : tema === 'stitch' ? c!.koyu : '#16161a';
  const koseFill = buyucu && c ? c.ana : '#fff';
  const koseStroke = buyucu && c ? '#f6ecd0' : jokerMi ? '#000' : c!.koyu;
  const alt = t.altYazi?.[kart.deger];
  return (
    <svg className="um-kart-svg" viewBox="0 0 100 150" aria-hidden="true" focusable="false">
      <rect x=".5" y=".5" width="99" height="149" rx="10.500" fill={t.kenar} stroke="rgba(0,0,0,.28)" strokeWidth="1" />
      <rect x="5.500" y="5.500" width="89" height="139" rx="7" fill={zemin} />
      {buyucu && c && <rect x="5.500" y="5.500" width="89" height="139" rx="7" fill="none" stroke={c.ana} strokeWidth="2.4" />}
      <Sus tema={tema} renk={kart.renk} t={t} />
      <Amblem tema={tema} t={t} renk={kart.renk} />
      <g transform={`translate(50 ${buyucu ? 79 : 75})`}>
        <Simge deger={kart.deger} fill={simgeFill} stroke={simgeStroke} yazi={t.yazi} egik={tema === 'klasik'} />
      </g>
      <g transform="translate(17 22)"><Kose deger={kart.deger} fill={koseFill} stroke={koseStroke} yazi={t.yazi} /></g>
      <g transform="translate(83 128) rotate(180)"><Kose deger={kart.deger} fill={koseFill} stroke={koseStroke} yazi={t.yazi} /></g>
      {kart.renk && (
        <>
          <g transform="translate(84.500 17)"><RenkBicimi renk={kart.renk} b={4.6} fill={buyucu ? c!.ana : '#fff'} stroke={buyucu ? '#f6ecd0' : 'rgba(0,0,0,.5)'} /></g>
          <g transform="translate(15.500 133) rotate(180)"><RenkBicimi renk={kart.renk} b={4.6} fill={buyucu ? c!.ana : '#fff'} stroke={buyucu ? '#f6ecd0' : 'rgba(0,0,0,.5)'} /></g>
        </>
      )}
      {alt && (
        <text x="50" y="137" textAnchor="middle" fontSize="8.500" fontWeight="700" fontFamily={t.yazi} letterSpacing=".6" fill={c ? '#4a3a1e' : '#e7cf8d'}>{alt.toLocaleUpperCase('tr')}</text>
      )}
    </svg>
  );
}

function Arka({ tema }: { tema: string }) {
  if (tema === 'stitch') {
    return (
      <svg className="um-kart-svg" viewBox="0 0 100 150" aria-hidden="true" focusable="false">
        <rect x=".5" y=".5" width="99" height="149" rx="10.500" fill="#fff8ea" stroke="rgba(0,0,0,.28)" />
        <rect x="5.500" y="5.500" width="89" height="139" rx="7" fill="#1787c2" />
        <path d="M5.500 104 q11 -8 22 0 t22 0 t22 0 t23 0 V137.500 a7 7 0 0 1 -7 7 H12.500 a7 7 0 0 1 -7 -7 Z" fill="#0f6ea6" />
        <path d="M5.500 118 q11 -8 22 0 t22 0 t22 0 t23 0 V137.500 a7 7 0 0 1 -7 7 H12.500 a7 7 0 0 1 -7 -7 Z" fill="#b79be8" fillOpacity=".55" />
        {/* özgün yaratık: yuvarlak gövde, iri yuvarlak kulaklar, tepede filiz, kapalı gülen gözler */}
        <g>
          <ellipse cx="22" cy="52" rx="13" ry="20" transform="rotate(-32 22 52)" fill="#0b4f7c" />
          <ellipse cx="78" cy="52" rx="13" ry="20" transform="rotate(32 78 52)" fill="#0b4f7c" />
          <ellipse cx="23" cy="53" rx="6.500" ry="12" transform="rotate(-32 23 53)" fill="#c9b2f2" />
          <ellipse cx="77" cy="53" rx="6.500" ry="12" transform="rotate(32 77 53)" fill="#c9b2f2" />
          <ellipse cx="50" cy="76" rx="27" ry="25" fill="#0b4f7c" />
          <ellipse cx="50" cy="84" rx="17" ry="13" fill="#7fd0f0" fillOpacity=".85" />
          <path d="M36 70 q5 -6 10 0 M54 70 q5 -6 10 0" fill="none" stroke="#eafaff" strokeWidth="2.6" strokeLinecap="round" />
          <path d="M44 84 q6 6 12 0" fill="none" stroke="#0b4f7c" strokeWidth="2.200" strokeLinecap="round" />
          <ellipse cx="50" cy="78.500" rx="3.200" ry="2.200" fill="#0b4f7c" />
          <path d="M50 51 C49 44 44 41 40 42 C43 45 46 47 50 51 Z M50 51 C52 43 58 40 62 42 C58 44 54 47 50 51 Z" fill="#35c58a" />
        </g>
        {/* hibiskus */}
        <g transform="translate(79 24)">
          {[0, 72, 144, 216, 288].map((a) => <ellipse key={a} cx="0" cy="-6" rx="4.400" ry="6.500" transform={`rotate(${a})`} fill="#ff8a7d" />)}
          <circle r="2.600" fill="#ffd45e" />
        </g>
        <g transform="translate(20 128) scale(.8)">
          {[0, 72, 144, 216, 288].map((a) => <ellipse key={a} cx="0" cy="-6" rx="4.400" ry="6.500" transform={`rotate(${a})`} fill="#fff4e0" />)}
          <circle r="2.600" fill="#ffd45e" />
        </g>
      </svg>
    );
  }
  if (tema === 'buyucu') {
    const y = 'M0 -5 L1.300 -1.300 L5 0 L1.300 1.300 L0 5 L-1.300 1.300 L-5 0 L-1.300 -1.300 Z';
    return (
      <svg className="um-kart-svg" viewBox="0 0 100 150" aria-hidden="true" focusable="false">
        <rect x=".5" y=".5" width="99" height="149" rx="10.500" fill="#c9a24a" stroke="rgba(0,0,0,.4)" />
        <rect x="5.500" y="5.500" width="89" height="139" rx="7" fill="#151a36" />
        <rect x="9.500" y="9.500" width="81" height="131" rx="4.500" fill="none" stroke="#c9a24a" strokeWidth="1" />
        <g fill="#e7cf8d">
          <path d={y} transform="translate(22 28)" />
          <path d={y} transform="translate(78 34) scale(.7)" />
          <path d={y} transform="translate(72 120) scale(.9)" />
          <path d={y} transform="translate(24 112) scale(.6)" />
          <path d={y} transform="translate(50 20) scale(.5)" />
        </g>
        {/* özgün baykuş: asa üstünde */}
        <g fill="#c9a24a">
          <path d="M32 50 L38 60 Q50 54 62 60 L68 50 Q72 68 70 84 Q68 104 50 106 Q32 104 30 84 Q28 68 32 50 Z" />
          <circle cx="41" cy="72" r="8.500" fill="#151a36" />
          <circle cx="59" cy="72" r="8.500" fill="#151a36" />
          <circle cx="41" cy="72" r="4.200" />
          <circle cx="59" cy="72" r="4.200" />
          <path d="M50 78 L46.500 84 H53.500 Z" fill="#151a36" />
          <path d="M40 92 q5 4 10 0 q5 4 10 0" fill="none" stroke="#151a36" strokeWidth="1.600" />
          <rect x="20" y="105" width="62" height="3.600" rx="1.800" transform="rotate(-6 50 107)" />
          <path d={y} transform="translate(84 102) scale(1.100)" fill="#fff3c4" />
        </g>
      </svg>
    );
  }
  return (
    <svg className="um-kart-svg" viewBox="0 0 100 150" aria-hidden="true" focusable="false">
      <rect x=".5" y=".5" width="99" height="149" rx="10.500" fill="#ffffff" stroke="rgba(0,0,0,.28)" />
      <rect x="5.500" y="5.500" width="89" height="139" rx="7" fill="#141417" />
      <ellipse cx="50" cy="75" rx="33" ry="55" transform="rotate(28 50 75)" fill="#e0242f" />
      <ellipse cx="50" cy="75" rx="27" ry="48" transform="rotate(28 50 75)" fill="none" stroke="#ffd21f" strokeWidth="2.200" />
      <g transform="translate(50 75) rotate(28)">
        <circle cx="0" cy="-24" r="6.500" fill="#f5c400" />
        <circle cx="0" cy="-8" r="6.500" fill="#fff" />
        <circle cx="0" cy="8" r="6.500" fill="#27a04b" />
        <circle cx="0" cy="24" r="6.500" fill="#1a66d6" />
      </g>
    </svg>
  );
}

export interface KartGorselProps {
  kart?: UnoKart;
  tema: string;
  /** px genişlik (yoksa CSS `--um-kw`, o da yoksa 72 px) */
  boy?: number;
  kapali?: boolean;
  className?: string;
  style?: React.CSSProperties;
}

/** Tek başına çizilebilen Uno kartı. `kart` yoksa ya da `kapali` ise kart arkası. */
export const KartGorsel = React.memo(function KartGorsel({ kart, tema, boy, kapali, className, style }: KartGorselProps) {
  const kod = temaKod(tema);
  const acik = !!kart && !kapali;
  return (
    <div
      className={`um-kart um-kart-${kod}${acik ? '' : ' um-kart-kapali'}${className ? ' ' + className : ''}`}
      style={boy ? { width: boy, ...style } : style}
      role="img"
      aria-label={acik ? kartAdi(kart!, kod) : 'Kapalı kart'}
    >
      {acik ? <Yuz kart={kart!} tema={kod} /> : <Arka tema={kod} />}
    </div>
  );
});

export default KartGorsel;
