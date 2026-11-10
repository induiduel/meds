import React from 'react';
import type { UnoDeger, UnoKart, UnoRenk, UnoYuz } from '../../../services/masa/tipler';
import { UNO_DEGER_AD } from '../../../services/masa/motor/unoAsistan';
import { EtkiSimge, FigurG, Kedicik, Tavsan, Tay, Yarasa, YarasaAmblem, type FigurAd } from './figurler';
import { renkAl, temaAl, temaKod, UNO_SIRA, type UnoRenkTon, type UnoTemaTanim } from './temalar';
import '../../../styles/masa/uno-kart.css';

/** Renk körlüğü için renge özgü biçim: k daire, s üçgen, y kare, m baklava (merkez 0,0; yarıçap b) */
export function RenkBicimi({ renk, b = 5, fill = '#fff', stroke = 'rgba(0,0,0,.55)' }: { renk: UnoRenk; b?: number; fill?: string; stroke?: string }) {
  const o = { fill, stroke, strokeWidth: b * 0.28, strokeLinejoin: 'round' as const };
  if (renk === 'k') return <circle r={b} {...o} />;
  if (renk === 's') return <polygon points={`0,${-b * 1.1} ${b * 1.1},${b * 0.85} ${-b * 1.1},${b * 0.85}`} {...o} />;
  if (renk === 'y') return <rect x={-b * 0.9} y={-b * 0.9} width={b * 1.8} height={b * 1.8} rx={b * 0.15} {...o} />;
  return <polygon points={`0,${-b * 1.2} ${b * 1.05},0 0,${b * 1.2} ${-b * 1.05},0`} {...o} />;
}

const yuzAdi = (y: UnoYuz, tema: string): string =>
  `${y.fx ? 'Flex ' : ''}${y.renk ? renkAl(tema, y)[y.renk].ad + ' ' : ''}${UNO_DEGER_AD[y.deger] ?? y.deger}`;

/** Kartın sesli adı: "Mavi Yedi", "Joker", "Pembe Beş çek", "Flex Mavi Atlat", "Kapalı kart: Mavi Yedi dendi" */
export const kartAdi = (kart: UnoKart, tema: string): string => {
  if (kart.kp) return `Kapalı kart: ${yuzAdi({ renk: kart.renk, deger: kart.deger }, tema)} dendi`;
  const ek = [kart.yl ? 'yalancı kartı' : '', kart.cv ? 'güç çevirir' : '', kart.ps ? 'paslaşma simgeli' : ''].filter(Boolean).join(', ');
  return `${yuzAdi(kart, tema)}${ek ? ` (${ek})` : ''}`;
};

const FIGURLER: readonly string[] = ['kitty', 'batman', 'kuromi', 'pony'];
const figurMu = (d: UnoDeger): d is FigurAd => FIGURLER.includes(d);
/** Rengin maskotu (Sevimli Dostlar teması) */
const MASKOT: Record<UnoRenk, FigurAd> = { k: 'kitty', s: 'batman', y: 'pony', m: 'kuromi' };

/* ------------------------------------------------------------------ simge parçaları ------------------------------------------------------------------ */

interface SP { deger: UnoDeger; fill: string; stroke: string; yazi: string; egik: boolean; r4: string[]; ic: string }

function Yazi({ m, boy, fill, stroke, yazi, egik, y = 0, x = 0, sw = 3, golge }: { m: string; boy: number; fill: string; stroke: string; yazi: string; egik?: boolean; y?: number; x?: number; sw?: number; golge?: boolean }) {
  const o = { x, y, dy: '.36em', textAnchor: 'middle' as const, fontSize: boy, fontWeight: 900, fontFamily: yazi, fontStyle: egik ? 'italic' : 'normal' };
  return (
    <>
      {golge && <text {...o} x={x - boy * 0.045} y={y + boy * 0.05} fill={stroke} stroke={stroke} strokeWidth={sw} strokeLinejoin="round">{m}</text>}
      <text {...o} fill={fill} stroke={stroke} strokeWidth={sw} paintOrder="stroke" strokeLinejoin="round">{m}</text>
    </>
  );
}

/** Küçük kart silueti (16×24) */
const Sil = ({ x = 0, y = 0, a = 0, s = 1, fill, stroke }: { x?: number; y?: number; a?: number; s?: number; fill: string; stroke: string }) => (
  <rect x="-8" y="-12" width="16" height="24" rx="3" transform={`translate(${x} ${y}) rotate(${a}) scale(${s})`} fill={fill} stroke={stroke} strokeWidth={2.2 / s} strokeLinejoin="round" />
);

/** n kartlık yelpaze */
function Yelpaze({ n, renkler, stroke, s = 1, y = 0 }: { n: number; renkler: string[]; stroke: string; s?: number; y?: number }) {
  return (
    <g transform={`translate(0 ${y}) scale(${s})`}>
      {Array.from({ length: n }, (_, i) => {
        const u = i - (n - 1) / 2;
        return <Sil key={i} x={u * (n > 4 ? 6.500 : 8)} y={Math.abs(u) * 1.800} a={u * (n > 4 ? 11 : 14)} fill={renkler[i % renkler.length]} stroke={stroke} />;
      })}
    </g>
  );
}

/** Yasak dairesi */
function Yasak({ fill, stroke, r = 19, x = 0, y = 0 }: { fill: string; stroke: string; r?: number; x?: number; y?: number }) {
  const k = r * 0.68, dis = r * 0.58, ic = r * 0.34;
  return (
    <g fill="none" strokeLinecap="round" transform={`translate(${x} ${y})`}>
      <circle r={r} stroke={stroke} strokeWidth={dis} />
      <line x1={-k} y1={k} x2={k} y2={-k} stroke={stroke} strokeWidth={dis} />
      <circle r={r} stroke={fill} strokeWidth={ic} />
      <line x1={-k} y1={k} x2={k} y2={-k} stroke={fill} strokeWidth={ic} />
    </g>
  );
}

const OK = '-21,-14 3,-14 3,-22 22,-8.5 3,5 3,-3 -21,-3';
/** Karşılıklı iki ok (yön) */
const Oklar = ({ fill, stroke, s = 1, y = 0 }: { fill: string; stroke: string; s?: number; y?: number }) => (
  <g transform={`translate(0 ${y}) scale(${s}) rotate(-38)`} fill={fill} stroke={stroke} strokeWidth="2.6" strokeLinejoin="round">
    <polygon points={OK} />
    <polygon points={OK} transform="rotate(180)" />
  </g>
);

/** Patlama yıldızı (fırlatıcı vuruşu) */
function Patlama({ r, fill, stroke, x = 0, y = 0, a = 0 }: { r: number; fill: string; stroke: string; x?: number; y?: number; a?: number }) {
  const p: string[] = [];
  for (let i = 0; i < 20; i++) { const q = i % 2 ? r * 0.66 : r; const t = (i / 20) * Math.PI * 2; p.push(`${(q * Math.sin(t)).toFixed(1)},${(-q * Math.cos(t)).toFixed(1)}`); }
  return <polygon points={p.join(' ')} transform={`translate(${x} ${y}) rotate(${a})`} fill={fill} stroke={stroke} strokeWidth="2.2" strokeLinejoin="round" />;
}

/** Oyuncu figürü: baş + gövde */
const Kisi = ({ x = 0, y = 0, s = 1, fill, stroke }: { x?: number; y?: number; s?: number; fill: string; stroke: string }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} fill={fill} stroke={stroke} strokeWidth={2 / s} strokeLinejoin="round">
    <path d="M-8 11 Q-8 -2 0 -2 Q8 -2 8 11 Z" />
    <circle cy="-8" r="5.200" />
  </g>
);

/** Nişangâh */
const Nisan = ({ r, fill, stroke }: { r: number; fill: string; stroke: string }) => (
  <g fill="none" strokeLinecap="round">
    <circle r={r} stroke={stroke} strokeWidth="6.500" />
    <path d={`M0 ${-r - 6} V${-r + 6} M0 ${r - 6} V${r + 6} M${-r - 6} 0 H${-r + 6} M${r - 6} 0 H${r + 6}`} stroke={stroke} strokeWidth="6.500" />
    <circle r={r} stroke={fill} strokeWidth="3.200" />
    <path d={`M0 ${-r - 6} V${-r + 6} M0 ${r - 6} V${r + 6} M${-r - 6} 0 H${-r + 6} M${r - 6} 0 H${r + 6}`} stroke={fill} strokeWidth="3.200" />
  </g>
);

/** Çember üstünde dönen iki ok (yarıçap r) */
function DonenOk({ r, fill, stroke, kal = 5 }: { r: number; fill: string; stroke: string; kal?: number }) {
  const yay = `M${(-r * 0.94).toFixed(1)} ${(-r * 0.34).toFixed(1)} A${r} ${r} 0 0 1 ${(r * 0.5).toFixed(1)} ${(-r * 0.87).toFixed(1)}`;
  const bas = `${(r * 0.5 - 2).toFixed(1)},${(-r * 0.87 - kal * 1.5).toFixed(1)} ${(r * 0.5 + kal * 2).toFixed(1)},${(-r * 0.87 + 2.5).toFixed(1)} ${(r * 0.5 - 4).toFixed(1)},${(-r * 0.87 + kal * 1.3).toFixed(1)}`;
  const yari = (
    <>
      <path d={yay} fill="none" stroke={stroke} strokeWidth={kal + 3.200} strokeLinecap="round" />
      <polygon points={bas} fill={stroke} stroke={stroke} strokeWidth="3.200" strokeLinejoin="round" />
      <path d={yay} fill="none" stroke={fill} strokeWidth={kal} strokeLinecap="round" />
      <polygon points={bas} fill={fill} />
    </>
  );
  return <g>{yari}<g transform="rotate(180)">{yari}</g></g>;
}

/** Flex dalgası: dört renkli kıvrım */
const FlexDalga = ({ r4, y = 0, s = 1 }: { r4: string[]; y?: number; s?: number }) => (
  <g transform={`translate(0 ${y}) scale(${s})`} fill="none" strokeLinecap="round">
    <path d="M-26 0 q6.500 -9 13 0 t13 0 t13 0 t13 0" stroke="#16161a" strokeWidth="8" />
    {r4.map((c, i) => <path key={i} d={`M${-26 + i * 13} 0 q6.500 ${i % 2 ? 9 : -9} 13 0`} stroke={c} strokeWidth="4.600" />)}
  </g>
);

const KOSE_YAZI: Partial<Record<UnoDeger, string>> = {
  '+1': '+1', '+2': '+2', '+5': '+5', '+6': '+6', '+10': '+10', 'r+4': '+4', '+4': '+4', jokerYon4: '+4', 'fx+4': '+4',
  'joker+2': '+2', jokerHedef2: '+2', fxHedef2: '+2', fxHerkes: '+2', jokerTakim4: '2+2', jokerRenk: '+?', vur1: 'V1', vur2: 'V2',
};

/** Değer simgesi; merkez (0,0), yaklaşık ±26 birim */
function Simge(p: SP) {
  const { deger, fill, stroke, yazi, egik, r4, ic } = p;
  const Y = (m: string, boy: number, y = 0, x = 0) => <Yazi m={m} boy={boy} y={y} x={x} fill={fill} stroke={stroke} yazi={yazi} egik={egik} />;
  switch (deger) {
    case 'pas': case 'jokerPas': return <Yasak fill={fill} stroke={stroke} />;
    case 'yon': case 'jokerYon': return <Oklar fill={fill} stroke={stroke} />;
    case 'joker': return null;
    case '+1': return <g><Sil s={1.700} a={10} fill={fill} stroke={stroke} /><Yazi m="1" boy={24} fill={ic} stroke={stroke} yazi={yazi} sw={2.4} /></g>;
    case '+2': return <g><Sil x={5} y={-6} a={10} s={1.450} fill={fill} stroke={stroke} /><Sil x={-5} y={6} a={10} s={1.450} fill={fill} stroke={stroke} /></g>;
    case 'joker+2': return <g><Sil x={5} y={-6} a={10} s={1.450} fill={r4[3]} stroke={stroke} /><Sil x={-5} y={6} a={10} s={1.450} fill={r4[0]} stroke={stroke} /></g>;
    case 'r+4': return <Yelpaze n={4} renkler={[fill]} stroke={stroke} s={1.300} y={-1} />;
    case '+4': return (
      <g>
        <Sil x={-9} y={3} a={-8} s={1.150} fill={r4[3]} stroke={stroke} /><Sil x={-2} y={-9} a={2} s={1.150} fill={r4[2]} stroke={stroke} />
        <Sil x={10} y={-3} a={12} s={1.150} fill={r4[0]} stroke={stroke} /><Sil x={2} y={9} a={5} s={1.150} fill={r4[1]} stroke={stroke} />
      </g>
    );
    case '+5': return <g><Yelpaze n={5} renkler={[fill]} stroke={stroke} s={1.100} y={-8} />{Y('5', 28, 15)}</g>;
    case '+6': return <g><Yelpaze n={4} renkler={r4} stroke={stroke} s={0.820} y={-15} />{Y('+6', 31, 12)}</g>;
    case '+10': return <g><Yelpaze n={4} renkler={r4} stroke={stroke} s={0.820} y={-15} />{Y('+10', 27, 12)}</g>;
    case 'fx+4': return <g><Yelpaze n={4} renkler={r4} stroke={stroke} s={0.780} y={-17} />{Y('+4', 25, 5)}<FlexDalga r4={r4} y={24} s={0.800} /></g>;
    case 'jokerYon4': return <g><Oklar fill={fill} stroke={stroke} s={0.560} y={-15} />{Y('+4', 29, 13)}</g>;
    case 'flip': return (
      <g>
        <g transform="rotate(14)">
          <rect x="-9.500" y="-14" width="19" height="28" rx="3.500" fill={fill} stroke={stroke} strokeWidth="2.200" />
          <path d="M-9.500 14 L9.500 -14 V10.500 Q9.500 14 6 14 Z" fill={stroke} />
        </g>
        <DonenOk r={24} fill={fill} stroke={stroke} />
      </g>
    );
    case 'pasHerkes': return <g><Yasak fill={fill} stroke={stroke} r={11.500} /><DonenOk r={24.500} fill={fill} stroke={stroke} kal={4.600} /></g>;
    case 'jokerPas2': return <g><Yasak fill={fill} stroke={stroke} r={13} x={-9} y={-7} /><Yasak fill={fill} stroke={stroke} r={13} x={9} y={8} /></g>;
    case 'jokerRenk': return (
      <g>
        <Yelpaze n={4} renkler={r4} stroke={stroke} s={1.050} y={-9} />
        <path d="M-9 13 L0 21 L9 13 M-9 21 L0 29 L9 21" fill="none" stroke={stroke} strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M-9 13 L0 21 L9 13 M-9 21 L0 29 L9 21" fill="none" stroke={fill} strokeWidth="3.400" strokeLinecap="round" strokeLinejoin="round" />
      </g>
    );
    case 'jokerHedef2': return <g><Nisan r={19} fill={fill} stroke={stroke} />{Y('+2', 19)}</g>;
    case 'fxHedef2': return <g transform="translate(0 -6)"><Nisan r={15.500} fill={fill} stroke={stroke} />{Y('+2', 15)}<FlexDalga r4={r4} y={30} s={0.800} /></g>;
    case 'fxHerkes': return (
      <g>
        <Kisi x={-15} y={-14} s={0.950} fill={r4[0]} stroke={stroke} /><Kisi x={0} y={-17} s={0.950} fill={r4[1]} stroke={stroke} /><Kisi x={15} y={-14} s={0.950} fill={r4[3]} stroke={stroke} />
        {Y('+2', 22, 7)}<FlexDalga r4={r4} y={25} s={0.800} />
      </g>
    );
    case 'jokerTakas': return (
      <g>
        <g transform="translate(-13 -8)"><Sil x={-3} a={-12} fill={r4[0]} stroke={stroke} /><Sil x={4} a={8} fill={r4[1]} stroke={stroke} /></g>
        <g transform="translate(13 9)"><Sil x={-4} a={-8} fill={r4[2]} stroke={stroke} /><Sil x={3} a={12} fill={r4[3]} stroke={stroke} /></g>
        <g fill={fill} stroke={stroke} strokeWidth="1.800" strokeLinejoin="round">
          <polygon points="2,-22 14,-22 14,-26 23,-18.500 14,-11 14,-15 2,-15" />
          <polygon points="-2,22 -14,22 -14,26 -23,18.500 -14,11 -14,15 -2,15" />
        </g>
      </g>
    );
    case 'hepsiAt': return (
      <g>
        <path d="M-20 -22 V-10 M-13 -25 V-15 M-6 -26 V-19" stroke={stroke} strokeWidth="3" strokeLinecap="round" opacity=".55" />
        <Sil x={-9} y={-11} a={-24} s={1.050} fill={fill} stroke={stroke} /><Sil x={3} y={1} a={8} s={1.050} fill={fill} stroke={stroke} /><Sil x={11} y={14} a={42} s={1.050} fill={fill} stroke={stroke} />
      </g>
    );
    case 'rulet': return (
      <g>
        <circle r="23" fill={stroke} />
        <g stroke={stroke} strokeWidth="1.600" transform="rotate(45)">
          <path d="M0 0 V-21 A21 21 0 0 1 21 0 Z" fill={r4[0]} /><path d="M0 0 H21 A21 21 0 0 1 0 21 Z" fill={r4[3]} />
          <path d="M0 0 V21 A21 21 0 0 1 -21 0 Z" fill={r4[1]} /><path d="M0 0 H-21 A21 21 0 0 1 0 -21 Z" fill={r4[2]} />
        </g>
        <circle r="5" fill={fill} stroke={stroke} strokeWidth="2" />
        <polygon points="-7,-29 7,-29 0,-15" fill={fill} stroke={stroke} strokeWidth="2.200" strokeLinejoin="round" />
      </g>
    );
    case 'vur1': case 'vur2': return <g><Patlama r={27} fill={fill} stroke={stroke} /><Yazi m={deger === 'vur1' ? '1' : '2'} boy={32} fill={ic} stroke={stroke} yazi={yazi} egik={egik} sw={2.6} /></g>;
    case 'jokerVur': return (
      <g>
        <Patlama r={18} x={-9} y={-8} fill={r4[0]} stroke={stroke} /><Patlama r={18} x={9} y={8} a={18} fill={r4[1]} stroke={stroke} />
        <g transform="scale(.62)"><Nisan r={13} fill={fill} stroke={stroke} /></g>
      </g>
    );
    case 'jokerTakim': return (
      <g>
        <path d="M-10 6 Q0 -2 10 6" fill="none" stroke={stroke} strokeWidth="6" strokeLinecap="round" />
        <path d="M-10 6 Q0 -2 10 6" fill="none" stroke={fill} strokeWidth="2.800" strokeLinecap="round" />
        <Kisi x={-13} y={2} s={1.650} fill={r4[3]} stroke={stroke} /><Kisi x={13} y={2} s={1.650} fill={r4[0]} stroke={stroke} />
      </g>
    );
    case 'jokerTakim4': return (
      <g>
        <Kisi x={-13} y={-11} s={1.150} fill={r4[3]} stroke={stroke} /><Kisi x={13} y={-11} s={1.150} fill={r4[0]} stroke={stroke} />
        {Y('+2', 17, 15, -14)}{Y('+2', 17, 15, 14)}
      </g>
    );
    case 'jokerCevir': return (
      <g>
        <g transform="rotate(20)">
          <path d="M0 -17 A17 17 0 0 0 0 17 Z" fill="#27a04b" stroke={stroke} strokeWidth="2" /><path d="M0 -17 A17 17 0 0 1 0 17 Z" fill="#e0242f" stroke={stroke} strokeWidth="2" />
          <path d="M-12 0 L-8 4.500 L-3 -4" fill="none" stroke="#fff" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M4 -4.500 L12 4.500 M12 -4.500 L4 4.500" fill="none" stroke="#fff" strokeWidth="3" strokeLinecap="round" />
        </g>
        <DonenOk r={25} fill={fill} stroke={stroke} kal={4.200} />
      </g>
    );
    case 'jokerMeydan': return (
      <g strokeLinejoin="round" strokeLinecap="round">
        <path d="M-22 -15 Q-6 -24 10 -15 Q12 6 -6 21 Q-24 6 -22 -15 Z" fill={fill} stroke={stroke} strokeWidth="2.600" />
        <path d="M-17 -8 Q-12 -12 -8 -7 Q-12 -4 -17 -8 Z M-2 -8 Q2 -12 7 -8 Q2 -4 -2 -8 Z" fill={stroke} />
        <path d="M-12 7 Q-6 12 0 7" fill="none" stroke={stroke} strokeWidth="2.400" />
        <path d="M-5 0 L21 6" stroke={stroke} strokeWidth="8.500" />
        <path d="M-5 0 L21 6" stroke={r4[1]} strokeWidth="4.800" />
        <Yazi m="?" boy={22} x={17} y={-14} fill={r4[0]} stroke={stroke} yazi={yazi} sw={2.6} />
      </g>
    );
    default: {
      const tek = deger.length === 1;
      return (
        <g>
          <Yazi m={deger} boy={tek ? 62 : 40} fill={fill} stroke={stroke} yazi={yazi} egik={egik} golge={tek} />
          {(deger === '6' || deger === '9') && <rect x="-13" y="25" width="26" height="4.500" rx="2" fill={fill} stroke={stroke} strokeWidth="1.400" />}
        </g>
      );
    }
  }
}

/** Köşe değeri (küçük); merkez (0,0) */
function Kose({ deger, fill, stroke, yazi, r4 }: { deger: UnoDeger; fill: string; stroke: string; yazi: string; r4: string[] }) {
  if (figurMu(deger)) return <g transform="scale(.95)"><circle r="9.500" fill="#fff" stroke={stroke} strokeWidth="1.200" /><g transform="scale(.78)"><EtkiSimge ad={deger} /></g></g>;
  const m = deger.length === 1 ? deger : KOSE_YAZI[deger];
  if (m) {
    return (
      <text x="0" y="0" dy=".36em" textAnchor="middle" fontSize={m.length === 1 ? 19 : m.length === 2 ? 14.500 : 11} fontWeight="900" fontFamily={yazi} fill={fill} stroke={stroke} strokeWidth="2.2" paintOrder="stroke" strokeLinejoin="round">{m}</text>
    );
  }
  if (deger === 'joker') {
    return (
      <g transform="rotate(28)" stroke="#fff" strokeWidth=".9">
        <path d="M0 0 V-10 A6.500 10 0 0 1 6.500 0 Z" fill={r4[0]} /><path d="M0 0 H6.500 A6.500 10 0 0 1 0 10 Z" fill={r4[3]} />
        <path d="M0 0 V10 A6.500 10 0 0 1 -6.500 0 Z" fill={r4[1]} /><path d="M0 0 H-6.500 A6.500 10 0 0 1 0 -10 Z" fill={r4[2]} />
      </g>
    );
  }
  return <g transform="scale(.36)"><Simge deger={deger} fill={fill} stroke={stroke} yazi={yazi} egik={false} r4={r4} ic="#fff" /></g>;
}

/* ------------------------------------------------------------------ amblem + süs ------------------------------------------------------------------ */

const KALKAN = 'M21 36 H79 V80 C79 104 62 117 50 123 C38 117 21 104 21 80 Z';

/** Orta amblem: tek renk kartta tema zemini, jokerde dört renk */
function Amblem({ tema, t, renk, c, r4, dolgu }: { tema: string; t: UnoTemaTanim; renk: UnoRenk | null; c: UnoRenkTon | null; r4: string[]; dolgu: string }) {
  if (tema === 'stitch') {
    // Hibiskus: beş yaprak + orta
    return (
      <g transform="translate(50 75)">
        {[0, 72, 144, 216, 288].map((a, i) => (
          <ellipse key={a} cx="0" cy="-27" rx="19" ry="27" transform={`rotate(${a})`} fill={renk ? dolgu : r4[i % 4]} stroke={c ? c.koyu : '#fff4e0'} strokeOpacity={renk ? 0.25 : 0.9} strokeWidth="1.2" />
        ))}
        <circle r="23" fill={dolgu} />
        {!renk && <circle r="23" fill="none" stroke="#3b2a6b" strokeOpacity=".25" strokeWidth="1.5" />}
      </g>
    );
  }
  if (tema === 'buyucu') {
    if (!c) {
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
    return (
      <g>
        <path d={KALKAN} fill={dolgu === '#17171b' ? dolgu : c.ana} />
        <rect x="21" y="36" width="58" height="11" fill={dolgu === '#17171b' ? c.acik : c.ikincil} />
        <path d={KALKAN} fill="none" stroke="#c9a24a" strokeWidth="2.6" strokeLinejoin="round" />
        <path d="M26 52 H74 V80 C74 100 60 111 50 116.500 C40 111 26 100 26 80 Z" fill="none" stroke={c.ikincil} strokeOpacity=".55" strokeWidth="1" />
      </g>
    );
  }
  // Klasik / Sevimli Dostlar: 28° eğik oval
  if (!renk) {
    return (
      <g transform="translate(50 75) rotate(28)" stroke="#fff" strokeWidth="2.200">
        <path d="M0 0 V-58 A36 58 0 0 1 36 0 Z" fill={r4[0]} />
        <path d="M0 0 H36 A36 58 0 0 1 0 58 Z" fill={r4[3]} />
        <path d="M0 0 V58 A36 58 0 0 1 -36 0 Z" fill={r4[1]} />
        <path d="M0 0 H-36 A36 58 0 0 1 0 -58 Z" fill={r4[2]} />
      </g>
    );
  }
  return <ellipse cx="50" cy="75" rx="36" ry="58" transform="rotate(28 50 75)" fill={dolgu} />;
}

/** Tema süsleri (zemin üstü, amblem altı) */
function Sus({ tema, c }: { tema: string; c: UnoRenkTon | null }) {
  if (tema === 'stitch') {
    const koyu = c ? c.koyu : '#22184a';
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
    const renk = c ? c.koyu : '#c9a24a';
    return (
      <g>
        <rect x="9" y="9" width="82" height="132" rx="4" fill="none" stroke="#b08d3c" strokeWidth=".9" />
        <g fill={renk} fillOpacity=".6">
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
  if (tema === 'dostlar') {
    // Puantiye + minik kalpler
    const renk = c ? c.koyu : '#ffffff';
    const kalp = 'M0 3 C-5 -1 -3 -5 0 -2.500 C3 -5 5 -1 0 3 Z';
    return (
      <g fill={renk} fillOpacity={c ? 0.3 : 0.16}>
        {[[14, 50], [10, 74], [14, 98], [86, 52], [90, 76], [86, 100], [36, 12], [64, 138]].map(([x, y]) => <circle key={`${x}-${y}`} cx={x} cy={y} r="2.200" />)}
        <path d={kalp} transform="translate(62 13) scale(1.300)" />
        <path d={kalp} transform="translate(38 138) scale(1.300)" />
      </g>
    );
  }
  return null;
}

/* ------------------------------------------------------------------ yüz ------------------------------------------------------------------ */

function Yuz({ kart, tema }: { kart: UnoYuz; tema: string }) {
  const t = temaAl(tema);
  const palet = renkAl(tema, kart);
  const r4 = UNO_SIRA.map((r) => palet[r].ana);
  const c = kart.renk ? palet[kart.renk] : null;
  const koyuYuz = kart.t === 'k';
  const buyucu = tema === 'buyucu';
  const dostlar = tema === 'dostlar';
  const figur = figurMu(kart.deger) ? kart.deger : null;
  const jokerMi = !c;
  const zemin = buyucu && !koyuYuz ? (c ? '#f1e3bf' : t.joker) : c ? c.ana : koyuYuz ? '#0d0d10' : t.joker;
  const amblemDolgu = koyuYuz ? '#17171b' : t.amblem;
  // Orta simge: açık ovalde kart rengi + koyu kontur; koyu yüzde/büyücü kalkanında açık renk
  const simgeFill = jokerMi ? '#fff' : koyuYuz ? c!.ana : buyucu ? (kart.renk === 's' ? '#1d1a16' : '#f6ecd0') : c!.ana;
  const simgeStroke = jokerMi ? '#16161a' : koyuYuz ? '#ffffff' : buyucu ? (kart.renk === 's' ? '#f6ecd0' : c!.koyu) : tema === 'stitch' ? c!.koyu : '#16161a';
  const simgeIc = koyuYuz && !jokerMi ? '#17171b' : buyucu && !jokerMi ? c!.ana : '#fff';
  const koseFill = kart.yl ? (c ? c.ana : '#16161a') : buyucu && c && !koyuYuz ? c.ana : '#fff';
  const koseStroke = kart.yl ? '#fff' : buyucu && c && !koyuYuz ? '#f6ecd0' : jokerMi ? '#000' : c!.koyu;
  const alt = !koyuYuz ? t.altYazi?.[kart.deger] : undefined;
  const bicimFill = buyucu && c && !koyuYuz ? c.ana : '#fff';
  const bicimStroke = buyucu && c && !koyuYuz ? '#f6ecd0' : 'rgba(0,0,0,.5)';
  const fxRenk = kart.fx && kart.fx !== 'j' ? palet[kart.fx] : null;
  const fxJoker = kart.fx === 'j' || kart.deger === 'fxHerkes' || kart.deger === 'fxHedef2' || kart.deger === 'fx+4';
  const maskot = dostlar && c && !figur && !koyuYuz ? MASKOT[kart.renk!] : null;
  const simgeY = (buyucu ? 79 : 75) - (maskot ? 9 : 0);
  return (
    <svg className="um-kart-svg" viewBox="0 0 100 150" aria-hidden="true" focusable="false">
      <rect x=".5" y=".5" width="99" height="149" rx="10.500" fill={koyuYuz ? '#0d0d10' : t.kenar} stroke={koyuYuz ? 'rgba(255,255,255,.35)' : 'rgba(0,0,0,.28)'} strokeWidth="1" />
      <rect x="5.500" y="5.500" width="89" height="139" rx="7" fill={zemin} />
      {buyucu && c && !koyuYuz && <rect x="5.500" y="5.500" width="89" height="139" rx="7" fill="none" stroke={c.ana} strokeWidth="2.4" />}
      {koyuYuz && <rect x="8" y="8" width="84" height="134" rx="5" fill="none" stroke="rgba(255,255,255,.4)" strokeWidth=".9" strokeDasharray="1.500 3" />}
      {!koyuYuz && <Sus tema={tema} c={c} />}
      {/* Flex: sağ üst ve sol alt köşede ikinci renk şeridi */}
      {(fxRenk || fxJoker) && [0, 180].map((a) => (
        <g key={a} transform={`rotate(${a} 50 75)`}>
          {fxRenk
            ? <path d="M58 5.500 H87.500 a7 7 0 0 1 7 7 V42 Z" fill={fxRenk.ana} stroke="#fff" strokeWidth="1.600" strokeLinejoin="round" />
            : r4.map((x, i) => <path key={i} d={`M${58 + i * 9} 5.500 H87.500 a7 7 0 0 1 7 7 V${42 - i * 9} Z`} fill={x} />)}
          {fxJoker && !fxRenk && <path d="M58 5.500 L94.500 42" stroke="#fff" strokeWidth="1.600" />}
        </g>
      ))}
      {figur ? (
        <>
          <g transform="translate(50 75) rotate(28)" stroke="#fff" strokeWidth="1.600" opacity=".95">
            <path d="M0 0 V-58 A36 58 0 0 1 36 0 Z" fill={r4[0]} /><path d="M0 0 H36 A36 58 0 0 1 0 58 Z" fill={r4[3]} />
            <path d="M0 0 V58 A36 58 0 0 1 -36 0 Z" fill={r4[1]} /><path d="M0 0 H-36 A36 58 0 0 1 0 -58 Z" fill={r4[2]} />
          </g>
          <circle cx="50" cy="68" r="37" fill="#fff7fb" stroke="#16161a" strokeWidth="2.200" />
          <g transform="translate(50 70) scale(.96)"><FigurG ad={figur} /></g>
          <g transform="translate(50 119)"><circle r="12.500" fill="#fff" stroke="#16161a" strokeWidth="1.800" /><EtkiSimge ad={figur} /></g>
        </>
      ) : (
        <>
          <Amblem tema={tema} t={t} renk={kart.renk} c={c} r4={r4} dolgu={amblemDolgu} />
          {koyuYuz && c && (tema === 'klasik' || dostlar) && <ellipse cx="50" cy="75" rx="36" ry="58" transform="rotate(28 50 75)" fill="none" stroke={c.acik} strokeWidth="1.600" />}
          <g transform={`translate(50 ${simgeY})`}>
            <Simge deger={kart.deger} fill={simgeFill} stroke={simgeStroke} yazi={t.yazi} egik={tema === 'klasik'} r4={r4} ic={simgeIc} />
          </g>
          {maskot && <g transform="translate(50 117) scale(.5)"><FigurG ad={maskot} /></g>}
        </>
      )}
      {kart.yl && <><circle cx="17" cy="22" r="11.500" fill="#fff" stroke="rgba(0,0,0,.45)" strokeWidth="1" /><circle cx="83" cy="128" r="11.500" fill="#fff" stroke="rgba(0,0,0,.45)" strokeWidth="1" /></>}
      <g transform="translate(17 22)"><Kose deger={kart.deger} fill={koseFill} stroke={koseStroke} yazi={t.yazi} r4={r4} /></g>
      <g transform="translate(83 128) rotate(180)"><Kose deger={kart.deger} fill={koseFill} stroke={koseStroke} yazi={t.yazi} r4={r4} /></g>
      {kart.renk && (fxRenk ? (
        <>
          {/* Flex: köşe şeridinde flex renginin biçimi; ana rengin biçimi indeksin altında */}
          <g transform="translate(84 16.500)"><RenkBicimi renk={kart.fx as UnoRenk} b={4.6} /></g>
          <g transform="translate(16 133.500) rotate(180)"><RenkBicimi renk={kart.fx as UnoRenk} b={4.6} /></g>
          <g transform="translate(17 39)"><RenkBicimi renk={kart.renk} b={3.800} fill={bicimFill} stroke={bicimStroke} /></g>
          <g transform="translate(83 111) rotate(180)"><RenkBicimi renk={kart.renk} b={3.800} fill={bicimFill} stroke={bicimStroke} /></g>
        </>
      ) : (
        <>
          <g transform="translate(84.500 17)"><RenkBicimi renk={kart.renk} b={4.6} fill={bicimFill} stroke={bicimStroke} /></g>
          <g transform="translate(15.500 133) rotate(180)"><RenkBicimi renk={kart.renk} b={4.6} fill={bicimFill} stroke={bicimStroke} /></g>
        </>
      ))}
      {kart.cv && [0, 180].map((a) => (
        <g key={a} transform={`rotate(${a} 50 75) translate(84 ${fxRenk ? 52 : 37})`}>
          <circle r="8.500" fill="#fff" stroke="#16161a" strokeWidth="1.400" />
          <g transform="scale(.24)"><DonenOk r={24} fill="#16161a" stroke="#16161a" kal={7} /></g>
        </g>
      ))}
      {kart.ps && (
        <g transform="translate(50 136.500)">
          <rect x="-13" y="-6" width="26" height="12" rx="6" fill="#16161a" stroke="#fff" strokeWidth="1.200" />
          <path d="M-8 -2 H5 M2 -4.500 L5.500 -2 L2 0.500 M8 2.300 H-5 M-2 -0.200 L-5.500 2.300 L-2 4.800" fill="none" stroke="#fff" strokeWidth="1.500" strokeLinecap="round" strokeLinejoin="round" />
        </g>
      )}
      {alt && !kart.ps && (
        <text x="50" y="137" textAnchor="middle" fontSize="8.500" fontWeight="700" fontFamily={t.yazi} letterSpacing=".6" fill={c ? '#4a3a1e' : '#e7cf8d'}>{alt.toLocaleUpperCase('tr')}</text>
      )}
    </svg>
  );
}

/* ------------------------------------------------------------------ arka ------------------------------------------------------------------ */

function ArkaIc({ tema }: { tema: string }) {
  if (tema === 'stitch') {
    return (
      <>
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
      </>
    );
  }
  if (tema === 'buyucu') {
    const y = 'M0 -5 L1.300 -1.300 L5 0 L1.300 1.300 L0 5 L-1.300 1.300 L-5 0 L-1.300 -1.300 Z';
    return (
      <>
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
      </>
    );
  }
  if (tema === 'dostlar') {
    const kalp = 'M0 3 C-5 -1 -3 -5 0 -2.500 C3 -5 5 -1 0 3 Z';
    return (
      <>
        <rect x=".5" y=".5" width="99" height="149" rx="10.500" fill="#ffffff" stroke="rgba(0,0,0,.28)" />
        <rect x="5.500" y="5.500" width="89" height="139" rx="7" fill="#ff8fb8" />
        <path d="M5.500 75 H94.500 V137.500 a7 7 0 0 1 -7 7 H12.500 a7 7 0 0 1 -7 -7 Z" fill="#b99bf5" />
        <path d="M5.500 75 q11.100 -9 22.200 0 t22.300 0 t22.200 0 t22.300 0" fill="#b99bf5" />
        <g fill="#fff" fillOpacity=".5">
          {[[14, 14], [86, 14], [14, 136], [86, 136], [50, 12], [50, 138]].map(([x, y]) => <circle key={`${x}-${y}`} cx={x} cy={y} r="2.400" />)}
        </g>
        <g transform="translate(29 44) scale(.5)"><Kedicik /></g>
        <g transform="translate(71 45) scale(.5)"><Yarasa /></g>
        <g transform="translate(29 108) scale(.5)"><Tay /></g>
        <g transform="translate(71 108) scale(.5)"><Tavsan /></g>
        <circle cx="50" cy="75" r="11.500" fill="#fff" stroke="#e8437c" strokeWidth="1.800" />
        <path d={kalp} transform="translate(50 75.500) scale(2.300)" fill="#ef3b5d" />
      </>
    );
  }
  return (
    <>
      <rect x=".5" y=".5" width="99" height="149" rx="10.500" fill="#ffffff" stroke="rgba(0,0,0,.28)" />
      <rect x="5.500" y="5.500" width="89" height="139" rx="7" fill="#141417" />
      <ellipse cx="50" cy="75" rx="36" ry="58" transform="rotate(28 50 75)" fill="#e0242f" />
      <ellipse cx="50" cy="75" rx="31" ry="52" transform="rotate(28 50 75)" fill="none" stroke="#ffd21f" strokeWidth="1.600" strokeOpacity=".7" />
      <g transform="translate(50 75) rotate(-22)" fontFamily='"Arial Black", "Helvetica Neue", Impact, system-ui, sans-serif' fontWeight="900" fontStyle="italic" fontSize="27" textAnchor="middle">
        <text x="-2.200" y="2.600" dy=".36em" fill="#141417" stroke="#141417" strokeWidth="5" strokeLinejoin="round">MeDS</text>
        <text x="0" y="0" dy=".36em" fill="#ffd21f" stroke="#141417" strokeWidth="3.200" paintOrder="stroke" strokeLinejoin="round">MeDS</text>
      </g>
    </>
  );
}

/** Kapalı kart; `beyan` varsa (Yalancı) üstünde söylenen kimlik etiketi */
function Arka({ tema, beyan }: { tema: string; beyan?: UnoYuz }) {
  const t = temaAl(tema);
  const c = beyan?.renk ? renkAl(tema, beyan)[beyan.renk] : null;
  const r4 = UNO_SIRA.map((r) => t.renk[r].ana);
  return (
    <svg className="um-kart-svg" viewBox="0 0 100 150" aria-hidden="true" focusable="false">
      <ArkaIc tema={tema} />
      {beyan && (
        <g transform="translate(50 75)">
          <rect x="-36" y="-21" width="72" height="42" rx="10" fill="#fff" stroke="#16161a" strokeWidth="2.400" />
          <rect x="-32" y="-17" width="64" height="34" rx="7" fill={c ? c.ana : '#17171b'} />
          {beyan.renk && <g transform="translate(-19 0)"><RenkBicimi renk={beyan.renk} b={7} /></g>}
          <g transform={`translate(${beyan.renk ? 11 : 0} 0) scale(1.350)`}><Kose deger={beyan.deger} fill="#fff" stroke={c ? c.koyu : '#000'} yazi={t.yazi} r4={r4} /></g>
          <g transform="translate(27 -21)"><circle r="8" fill="#ffd21f" stroke="#16161a" strokeWidth="1.800" /><text y="0" dy=".36em" textAnchor="middle" fontSize="11" fontWeight="900" fontFamily={t.yazi} fill="#16161a">?</text></g>
        </g>
      )}
    </svg>
  );
}

export interface KartGorselProps {
  kart?: UnoKart | UnoYuz;
  tema: string;
  /** px genişlik (yoksa CSS `--um-kw`, o da yoksa 72 px) */
  boy?: number;
  kapali?: boolean;
  className?: string;
  style?: React.CSSProperties;
}

/** Tek başına çizilebilen Uno kartı. `kart` yoksa ya da `kapali` ise kart arkası; `kart.kp` ise kapalı + söylenen kimlik etiketi. */
export const KartGorsel = React.memo(function KartGorsel({ kart, tema, boy, kapali, className, style }: KartGorselProps) {
  const kod = temaKod(tema);
  const beyanli = !!kart && !kapali && !!kart.kp;
  const acik = !!kart && !kapali && !kart.kp;
  return (
    <div
      className={`um-kart um-kart-${kod}${acik ? '' : ' um-kart-kapali'}${kart?.t === 'k' && acik ? ' um-kart-koyu' : ''}${className ? ' ' + className : ''}`}
      style={boy ? { width: boy, ...style } : style}
      role="img"
      aria-label={acik || beyanli ? kartAdi(kart as UnoKart, kod) : 'Kapalı kart'}
    >
      {acik ? <Yuz kart={kart!} tema={kod} /> : <Arka tema={kod} beyan={beyanli ? kart! : undefined} />}
    </div>
  );
});

export default KartGorsel;
