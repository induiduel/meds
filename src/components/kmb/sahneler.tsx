/**
 * KMB görsel asistan — SVG sahne kitaplığı (v2, gerçekçi çizim: degrade hacim, anatomik katmanlar, gölge).
 * Her öge `o(id)` ile kimliklenir: asistan eylemleri (vurgula, çiz, renk, göster/gizle, etiket) ve sınavdaki
 * "sahnede bul" tıklamaları bu kimliklerle çalışır. Çizilebilir çizgiler `cz` sınıfı + pathLength=1 taşır;
 * renk eylemi `.boya` (dolgu) ve `.boya-cizgi` (çizgi) sınıflı parçaları boyar, diğer parçalar gerçek dokusunu korur.
 * Ortak degradeler <Ortak/> içinde (kimlikler kmb- önekli). Yeni sahne: docs/KMB_GORSEL_ASISTAN.md §5.
 */
import React from 'react';

export type OgeDurum = { gor?: boolean; renk?: string; vurgu?: number; etiket?: boolean; ciz?: number };
export type SahneDurum = Record<string, OgeDurum>;
export type OgeProps = (id: string) => Record<string, unknown>;

type Sahne = {
  ad: string;
  zemin?: string;
  gizli: string[];
  etiket: Record<string, [number, number, string]>;
  Ciz: React.FC<{ o: OgeProps }>;
};

const u = (id: string) => `url(#kmb-${id})`;

/** Ortak degrade ve süzgeçler — her sahne SVG'sine bir kez eklenir */
export function Ortak() {
  return (
    <defs>
      <radialGradient id="kmb-zemin-klinik" cx="50%" cy="40%" r="75%">
        <stop offset="0" stopColor="#fbfcfd" /><stop offset="1" stopColor="#e4e9ef" />
      </radialGradient>
      <linearGradient id="kmb-zemin-tepsi" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#dfe6ec" /><stop offset="1" stopColor="#c7d1da" />
      </linearGradient>
      <radialGradient id="kmb-deri" cx="45%" cy="35%" r="70%">
        <stop offset="0" stopColor="#f6d6bd" /><stop offset=".7" stopColor="#e9b896" /><stop offset="1" stopColor="#d49a76" />
      </radialGradient>
      <linearGradient id="kmb-deri-kesit" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#e8b493" /><stop offset="1" stopColor="#f3cdb1" />
      </linearGradient>
      <linearGradient id="kmb-yag" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#f6e3a6" /><stop offset="1" stopColor="#efd283" />
      </linearGradient>
      <linearGradient id="kmb-kas" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#b5524a" /><stop offset=".5" stopColor="#cf6b5f" /><stop offset="1" stopColor="#a8463f" />
      </linearGradient>
      <radialGradient id="kmb-kemik" cx="40%" cy="35%" r="75%">
        <stop offset="0" stopColor="#fbf6e9" /><stop offset=".75" stopColor="#eadfc4" /><stop offset="1" stopColor="#cdbd98" />
      </radialGradient>
      <radialGradient id="kmb-ilik" cx="50%" cy="50%" r="60%">
        <stop offset="0" stopColor="#e9c9a0" /><stop offset="1" stopColor="#d9b07e" />
      </radialGradient>
      <radialGradient id="kmb-mesane" cx="40%" cy="35%" r="75%">
        <stop offset="0" stopColor="#f6c2bb" /><stop offset=".7" stopColor="#e39a92" /><stop offset="1" stopColor="#c8746c" />
      </radialGradient>
      <radialGradient id="kmb-idrar" cx="45%" cy="40%" r="70%">
        <stop offset="0" stopColor="#fff3b8" /><stop offset="1" stopColor="#f2cf55" />
      </radialGradient>
      <linearGradient id="kmb-idrar-torba" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#f8dd6c" stopOpacity=".85" /><stop offset="1" stopColor="#e7b82e" stopOpacity=".95" />
      </linearGradient>
      <radialGradient id="kmb-prostat" cx="40%" cy="35%" r="75%">
        <stop offset="0" stopColor="#e7b3a0" /><stop offset="1" stopColor="#b97a66" />
      </radialGradient>
      <linearGradient id="kmb-rektum" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#b98a77" /><stop offset=".5" stopColor="#d6a995" /><stop offset="1" stopColor="#ad7c69" />
      </linearGradient>
      <linearGradient id="kmb-korpus" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#c9787a" /><stop offset=".5" stopColor="#e0999a" /><stop offset="1" stopColor="#b9686b" />
      </linearGradient>
      <linearGradient id="kmb-spongiosum" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#e8a9a6" /><stop offset="1" stopColor="#cf8784" />
      </linearGradient>
      <radialGradient id="kmb-glans" cx="40%" cy="35%" r="75%">
        <stop offset="0" stopColor="#f2b4ae" /><stop offset="1" stopColor="#c97c77" />
      </radialGradient>
      <radialGradient id="kmb-testis" cx="40%" cy="35%" r="70%">
        <stop offset="0" stopColor="#f3e0dc" /><stop offset="1" stopColor="#cfa7a1" />
      </radialGradient>
      <radialGradient id="kmb-mukoza" cx="50%" cy="40%" r="70%">
        <stop offset="0" stopColor="#f2a9a6" /><stop offset="1" stopColor="#c86e6c" />
      </radialGradient>
      <radialGradient id="kmb-bagirsak" cx="40%" cy="35%" r="70%">
        <stop offset="0" stopColor="#f3d0c3" /><stop offset="1" stopColor="#d9a594" />
      </radialGradient>
      {/* kateter: silindir ışığı */}
      <linearGradient id="kmb-lateks" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#c99a2c" /><stop offset=".3" stopColor="#f6d77a" /><stop offset=".55" stopColor="#e9bd47" /><stop offset="1" stopColor="#a87b1d" />
      </linearGradient>
      <linearGradient id="kmb-silikon" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#b9c3cf" /><stop offset=".3" stopColor="#ffffff" /><stop offset=".6" stopColor="#e6ebf1" /><stop offset="1" stopColor="#9aa6b4" />
      </linearGradient>
      <linearGradient id="kmb-plastik" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#eef3f8" stopOpacity=".95" /><stop offset=".5" stopColor="#ffffff" stopOpacity=".7" /><stop offset="1" stopColor="#c9d3de" stopOpacity=".95" />
      </linearGradient>
      <linearGradient id="kmb-torba" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#e9eef3" stopOpacity=".9" /><stop offset=".4" stopColor="#ffffff" stopOpacity=".75" /><stop offset="1" stopColor="#d3dbe4" stopOpacity=".9" />
      </linearGradient>
      <linearGradient id="kmb-metal" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#8b96a3" /><stop offset=".4" stopColor="#eef2f6" /><stop offset="1" stopColor="#6d7884" />
      </linearGradient>
      <linearGradient id="kmb-eldiven" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#d9e8f8" /><stop offset="1" stopColor="#9fbfe3" />
      </linearGradient>
      <linearGradient id="kmb-eldiven-steril" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#fbf3e6" /><stop offset="1" stopColor="#e7d3b3" />
      </linearGradient>
      <linearGradient id="kmb-ortu" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#5f9fd6" /><stop offset="1" stopColor="#3b7bb8" />
      </linearGradient>
      <linearGradient id="kmb-povidon" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stopColor="#7a3410" /><stop offset=".5" stopColor="#b5551d" /><stop offset="1" stopColor="#6d2c0c" />
      </linearGradient>
      <linearGradient id="kmb-us-isin" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#7fb8ff" stopOpacity=".55" /><stop offset="1" stopColor="#7fb8ff" stopOpacity="0" />
      </linearGradient>
      <linearGradient id="kmb-yatak" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#f4f7fa" /><stop offset="1" stopColor="#d6dee7" />
      </linearGradient>
      <linearGradient id="kmb-onluk" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#8fc1c9" /><stop offset="1" stopColor="#5e9aa5" />
      </linearGradient>
      <linearGradient id="kmb-beyaz-onluk" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#ffffff" /><stop offset="1" stopColor="#d5dde6" />
      </linearGradient>
      <filter id="kmb-golge" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="3" stdDeviation="3.5" floodColor="#1d2733" floodOpacity=".22" />
      </filter>
      <filter id="kmb-yumusak" x="-10%" y="-10%" width="120%" height="120%">
        <feGaussianBlur stdDeviation="1.2" />
      </filter>
      <pattern id="kmb-kil" width="9" height="9" patternUnits="userSpaceOnUse">
        <path d="M2 7 q1 -4 3 -5" stroke="#6b4a33" strokeWidth=".9" fill="none" opacity=".5" />
      </pattern>
      <marker id="kmb-ok" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 Z" fill="#2f6fd6" />
      </marker>
    </defs>
  );
}

/** Silindir boru (kateter, hortum): gövde + ince parlama */
const Boru = ({ d, g = 'lateks', w = 10, cz = false, cls = 'boya-cizgi' }: { d: string; g?: string; w?: number; cz?: boolean; cls?: string }) => (
  <>
    <path d={d} stroke="#5a4a2a" strokeOpacity={0.35} strokeWidth={w + 2} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    <path className={`${cz ? 'cz ' : ''}${cls}`} pathLength={cz ? 1 : undefined} d={d} stroke={g === 'lateks' ? '#e3b544' : g === 'silikon' ? '#eef2f6' : '#dfe6ee'} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    <path d={d} stroke="#fff" strokeOpacity={0.55} strokeWidth={Math.max(1.5, w / 4)} fill="none" strokeLinecap="round" strokeLinejoin="round" transform={`translate(0 ${-w / 4})`} />
  </>
);

/** Pelvis yan kesit zemini: sakrum, koksiks, rektum, pelvis tabanı, karın duvarı katmanları, bağırsak, simfiz */
const PelvisKesit = ({ erkek = false }: { erkek?: boolean }) => (
  <g>
    {/* karın-pelvis boşluğu */}
    <path d="M60 20 L470 20 C470 120 468 190 452 250 C440 300 420 340 390 380 L340 430 L240 440 C170 440 120 400 95 330 C70 260 60 140 60 20 Z" fill="#f4e4dc" />
    {/* bağırsak kıvrımları */}
    {[[170, 70, 48, 30], [255, 58, 52, 32], [345, 70, 50, 30], [215, 118, 46, 26], [310, 115, 44, 26]].map(([x, y, rx, ry], i) => (
      <g key={i}>
        <ellipse cx={x} cy={y} rx={rx} ry={ry} fill={u('bagirsak')} stroke="#c58b7a" strokeWidth={1.5} />
        <path d={`M${x - rx * 0.6} ${y} q${rx * 0.6} ${-ry * 0.5} ${rx * 1.2} 0`} stroke="#c58b7a" strokeWidth={1.2} fill="none" opacity={0.6} />
      </g>
    ))}
    {/* periton çizgisi */}
    <path d="M100 150 C180 160 240 150 300 150 C360 150 420 140 455 150" stroke="#b48a7a" strokeWidth={1.5} strokeDasharray="5 4" fill="none" opacity={0.7} />
    {/* sakrum + koksiks */}
    <path d="M60 30 C95 40 118 70 128 120 C138 175 138 230 130 280 C124 315 112 340 100 355 L82 350 C92 320 100 290 104 250 C108 200 104 140 92 100 C84 74 72 54 60 46 Z" fill={u('kemik')} stroke="#a8946b" strokeWidth={2} />
    {[85, 125, 165, 205, 245].map((y) => <path key={y} d={`M${96 + (y - 85) * 0.1} ${y} l26 6`} stroke="#b9a479" strokeWidth={1.5} />)}
    <path d="M100 355 C104 372 112 384 124 392" stroke="#a8946b" strokeWidth={7} strokeLinecap="round" fill="none" />
    {/* rektum + anal kanal */}
    <path d="M128 70 C160 110 168 170 170 220 C172 270 180 320 205 360 L238 410" stroke={u('rektum')} strokeWidth={34} fill="none" strokeLinecap="round" />
    <path d="M128 70 C160 110 168 170 170 220 C172 270 180 320 205 360 L238 410" stroke="#8f5f4f" strokeWidth={2} fill="none" strokeDasharray="2 6" opacity={0.5} />
    {/* pelvis tabanı (levator) */}
    <path d="M150 395 C200 360 260 330 330 322 C370 318 400 330 420 345" stroke="#b65a50" strokeWidth={9} fill="none" strokeLinecap="round" opacity={0.8} />
    <path d="M150 395 C200 360 260 330 330 322 C370 318 400 330 420 345" stroke="#e08f85" strokeWidth={3} fill="none" strokeLinecap="round" opacity={0.7} />
    {/* ön karın duvarı: deri, yağ, rektus kası */}
    <path d="M470 20 C470 120 468 190 452 250 C447 270 440 285 432 298 L452 304 C462 290 472 270 478 248 C494 190 496 120 496 20 Z" fill={u('kas')} />
    <path d="M496 20 C496 120 494 190 478 248 C472 270 462 290 452 304 L478 312 C490 296 500 276 506 252 C522 194 526 120 526 20 Z" fill={u('yag')} />
    <path d="M526 20 C526 120 522 194 506 252 C500 276 490 296 478 312 L490 316 C503 299 512 280 518 255 C534 196 538 120 538 20 Z" fill={u('deri-kesit')} />
    {erkek ? null : <path d="M490 316 C470 360 430 400 390 430 L345 450" stroke="#d49a76" strokeWidth={10} fill="none" strokeLinecap="round" />}
  </g>
);

/** Simfiz pubis kesiti */
const Simfiz = ({ x, y, r = 0 }: { x: number; y: number; r?: number }) => (
  <g transform={`translate(${x} ${y}) rotate(${r})`} filter={u('golge')}>
    <ellipse cx={0} cy={0} rx={22} ry={44} fill={u('kemik')} stroke="#a8946b" strokeWidth={2.5} />
    <ellipse cx={0} cy={0} rx={13} ry={32} fill={u('ilik')} opacity={0.55} />
    <path d="M-4 -40 L-4 40" stroke="#d8cbb0" strokeWidth={3} opacity={0.8} />
  </g>
);

const Foley: Sahne = {
  ad: 'Foley kateter ve idrar torbası',
  gizli: ['f-balon', 'f-torba', 'f-torba-bag', 'f-enjektor'],
  etiket: {
    'f-uc': [80, 150, 'Kateter ucu (yuvarlak)'],
    'f-delik': [95, 255, 'İdrar delikleri'],
    'f-balon-sonuk': [150, 140, 'Sabitleme balonu (sönük)'],
    'f-balon': [150, 118, 'Şişirilmiş balon'],
    'f-govde': [330, 160, 'Gövde: sarı lateks / beyaz silikon'],
    'f-drenaj': [665, 262, 'Drenaj kanalı → torba'],
    'f-balon-kanal': [590, 52, 'Valfli balon kanalı → enjektör'],
    'f-torba': [530, 340, 'İdrar torbası'],
    'f-musluk': [690, 490, 'Boşaltma musluğu'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      {/* steril örtü üzerinde */}
      <path d="M20 120 L560 120 L560 290 L20 290 Z" fill="#cfe2f3" opacity={0.45} />
      <g {...o('f-govde')}>
        <g filter={u('golge')}><Boru d="M78 200 L548 200" w={20} cz /></g>
        {/* boy ve hacim yazısı */}
        <text x={350} y={205} textAnchor="middle" fontSize={11} fill="#7a5a16" fontWeight={600} opacity={0.8}>16 Fr · 10 mL</text>
        {[260, 300, 340, 380].map((x) => <path key={x} d={`M${x} 191 l0 4`} stroke="#9b7420" strokeWidth={1} opacity={0.5} />)}
      </g>
      <g {...o('f-uc')}>
        <path className="boya" d="M78 190 C58 190 50 196 50 200 C50 204 58 210 78 210 Z" fill={u('lateks')} stroke="#a37a20" strokeWidth={1.5} />
      </g>
      <g {...o('f-delik')}>
        <ellipse cx={86} cy={198} rx={7} ry={4.5} fill="#5a4214" />
        <ellipse cx={86} cy={198} rx={5} ry={2.8} fill="#2e220a" />
        <ellipse cx={104} cy={203} rx={6} ry={3.5} fill="#5a4214" opacity={0.75} />
      </g>
      <g {...o('f-balon-sonuk')}>
        <rect className="boya" x={122} y={188} width={52} height={24} rx={11} fill={u('lateks')} stroke="#a37a20" strokeWidth={1.5} opacity={0.95} />
        <path d="M128 193 L168 193" stroke="#fff" strokeOpacity={0.6} strokeWidth={2} />
      </g>
      <g {...o('f-balon')}>
        <ellipse className="boya" cx={148} cy={200} rx={44} ry={38} fill="#f6e3a2" fillOpacity={0.55} stroke="#c9a03a" strokeWidth={2} />
        <ellipse cx={148} cy={210} rx={36} ry={20} fill="#e8f2fb" opacity={0.55} />
        <ellipse cx={132} cy={182} rx={12} ry={7} fill="#fff" opacity={0.7} />
      </g>
      {/* çatal */}
      <path d="M540 188 C565 186 580 180 600 176 L604 224 C584 220 565 214 540 212 Z" fill={u('lateks')} stroke="#a37a20" strokeWidth={1.5} />
      <g {...o('f-drenaj')}>
        <path className="boya" d="M600 172 L690 166 C700 166 704 172 704 178 L704 222 C704 228 700 234 690 234 L600 228 Z" fill={u('lateks')} stroke="#a37a20" strokeWidth={1.8} />
        <ellipse cx={704} cy={200} rx={8} ry={30} fill="#d9a83a" stroke="#a37a20" strokeWidth={1.5} />
        <ellipse cx={704} cy={200} rx={4.5} ry={18} fill="#4a3510" />
      </g>
      <g {...o('f-balon-kanal')}>
        <Boru d="M560 192 C590 160 612 130 636 104" w={11} />
        <g transform="translate(646 92) rotate(-42)" filter={u('golge')}>
          <rect className="boya" x={-14} y={-18} width={48} height={36} rx={7} fill="#e6ebf0" stroke="#6b7a90" strokeWidth={1.8} />
          <rect x={30} y={-12} width={16} height={24} rx={4} fill="#2f6fd6" />
          <path d="M-6 -10 L22 -10" stroke="#fff" strokeWidth={2} opacity={0.8} />
        </g>
      </g>
      <g {...o('f-enjektor')} filter={u('golge')}>
        <g transform="translate(684 58) rotate(-42)">
          <rect x={0} y={-15} width={120} height={30} rx={4} fill={u('plastik')} stroke="#6b7a90" strokeWidth={1.8} />
          <rect x={6} y={-11} width={70} height={22} fill="#e9f3fb" opacity={0.9} />
          {[20, 40, 60, 80, 100].map((x) => <path key={x} d={`M${x} -15 l0 8`} stroke="#4b5868" strokeWidth={1.2} />)}
          <rect x={120} y={-6} width={50} height={12} fill="#c9d3de" stroke="#6b7a90" />
          <rect x={168} y={-18} width={8} height={36} rx={2} fill="#6b7a90" />
          <path d="M-10 -3 L0 -3 L0 3 L-10 3 Z" fill="#6b7a90" />
        </g>
      </g>
      <g {...o('f-torba-bag')}>
        <path className="cz" pathLength={1} d="M712 200 C790 210 790 290 690 318" stroke="#cfd8e2" strokeWidth={12} fill="none" strokeLinecap="round" />
        <path d="M712 196 C786 206 786 286 690 314" stroke="#fff" strokeWidth={3} fill="none" opacity={0.7} />
      </g>
      <g {...o('f-torba')} filter={u('golge')}>
        {/* askı + damla odası */}
        <path d="M600 310 L600 296 C600 288 760 288 760 296 L760 310" stroke="#9aa6b4" strokeWidth={4} fill="none" />
        <rect className="boya" x={590} y={310} width={180} height={168} rx={14} fill={u('torba')} stroke="#9aa6b4" strokeWidth={2.5} />
        <path d="M600 410 C640 404 720 404 760 410 L760 466 C760 472 754 476 748 476 L612 476 C606 476 600 472 600 466 Z" fill={u('idrar-torba')} />
        <path d="M604 410 C640 404 720 404 756 410" stroke="#fff" strokeWidth={2} opacity={0.6} fill="none" />
        <rect x={670} y={316} width={18} height={30} rx={5} fill="#eef3f8" stroke="#9aa6b4" />
        <circle cx={679} cy={338} r={3} fill="#f2cf55" />
        {[340, 365, 390, 415, 440, 465].map((y, i) => (
          <g key={y}><path d={`M740 ${y} L760 ${y}`} stroke="#5b6676" strokeWidth={1.5} /><text x={736} y={y + 4} fontSize={9} fill="#5b6676" textAnchor="end">{(6 - i) * 250}</text></g>
        ))}
        <text x={612} y={336} fontSize={10} fill="#5b6676">mL</text>
        <path d="M612 322 L612 470" stroke="#fff" strokeWidth={4} opacity={0.5} />
        <g {...o('f-musluk')}>
          <rect className="boya" x={666} y={476} width={28} height={16} rx={4} fill="#6b7a90" stroke="#3e4a58" />
          <rect x={692} y={480} width={18} height={8} rx={3} fill="#c0392b" />
        </g>
      </g>
    </>
  ),
};

const Mesane: Sahne = {
  ad: 'Mesane, suprapubik bölge ve idrar takibi (yan kesit)',
  gizli: ['g-mesane-dolu', 'g-sisme', 'g-torba', 'g-akis', 'g-kultur', 'g-ilac', 'g-kucuk', 'g-el', 'g-us', 'g-us-dalga'],
  etiket: {
    'g-mesane-normal': [320, 205, 'Mesane'],
    'g-mesane-dolu': [300, 95, 'Dolu mesane (glob)'],
    'g-sisme': [640, 150, 'Suprapubik kabarıklık'],
    'g-torba': [680, 315, 'İdrar torbası'],
    'g-kultur': [545, 470, 'Steril kültür kabı'],
    'g-ilac': [300, 35, 'Mesane içine ilaç / opak madde'],
    'g-kucuk': [320, 205, 'Sistit: 15–20 mL, ödemli duvar'],
    'g-el': [650, 110, 'Suprapubik palpasyon'],
    'g-us': [650, 60, 'Ultrason probu'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      <PelvisKesit />
      <Simfiz x={420} y={300} r={-18} />
      <text x={438} y={360} fontSize={12} fill="#7d6a45">simfiz pubis</text>
      {/* üretra (kadın: kısa) */}
      <path d="M330 268 C340 300 352 330 360 360 L368 440" stroke="#d68c86" strokeWidth={9} fill="none" strokeLinecap="round" />
      <g {...o('g-mesane-normal')} filter={u('golge')}>
        <path className="boya" d="M260 250 C255 205 300 185 345 192 C390 198 405 230 396 255 C388 278 360 285 330 280 C300 276 263 272 260 250 Z" fill={u('mesane')} stroke="#a8554e" strokeWidth={6} />
        <path d="M272 248 C270 215 305 202 342 206 C378 211 388 234 381 252 C374 268 352 272 330 269 C305 266 274 264 272 248 Z" fill={u('idrar')} opacity={0.85} />
      </g>
      <g {...o('g-mesane-dolu')} filter={u('golge')}>
        <path className="boya" d="M235 250 C215 160 260 70 350 72 C440 74 470 150 455 225 C445 270 400 290 340 288 C280 286 243 282 235 250 Z" fill={u('mesane')} stroke="#a8554e" strokeWidth={4} />
        <path d="M248 247 C232 165 272 86 350 88 C428 90 452 158 440 222 C431 262 393 276 340 274 C286 272 255 270 248 247 Z" fill={u('idrar')} opacity={0.92} />
        <path d="M290 110 C320 96 360 96 390 108" stroke="#fff" strokeWidth={5} opacity={0.45} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('g-kucuk')} filter={u('golge')}>
        <path className="boya" d="M280 252 C276 225 302 210 334 214 C366 218 378 236 372 255 C366 270 348 276 328 274 C306 272 283 268 280 252 Z" fill={u('mukoza')} stroke="#9f3c38" strokeWidth={12} />
        <path d="M300 250 C300 236 316 230 332 232 C348 234 354 244 350 254 C346 262 336 264 326 263 C312 262 300 260 300 250 Z" fill={u('idrar')} />
        {['M286 232 q8 6 4 14', 'M362 232 q-6 8 0 16', 'M300 268 q10 -2 16 4', 'M346 266 q6 -6 14 -2'].map((d) => <path key={d} d={d} stroke="#7d1f1c" strokeWidth={1.6} fill="none" />)}
      </g>
      <g {...o('g-sisme')}>
        <path d="M538 70 C600 110 612 220 560 300 C548 316 532 326 520 330" fill="#efc7a8" opacity={0.85} />
        <path className="cz boya-cizgi" pathLength={1} d="M538 70 C600 110 612 220 560 300 C548 316 532 326 520 330" stroke="#e1a92e" strokeWidth={4} fill="none" strokeDasharray="1 0" />
      </g>
      <g {...o('g-el')} filter={u('golge')}>
        <path d="M560 175 C590 150 650 140 700 150 L780 160 L780 230 L700 236 C660 240 610 232 586 220 C570 212 556 196 560 175 Z" fill={u('deri')} stroke="#b9805a" strokeWidth={2} />
        {[0, 1, 2, 3].map((i) => <path key={i} d={`M${572 + i * 3} ${176 + i * 12} C${600} ${170 + i * 12} ${640} ${168 + i * 12} ${690} ${176 + i * 12}`} stroke="#c28a66" strokeWidth={1.6} fill="none" opacity={0.7} />)}
        <path d="M562 180 C566 168 578 162 590 164" stroke="#fff" strokeWidth={2} opacity={0.4} fill="none" />
      </g>
      <g {...o('g-us')} filter={u('golge')}>
        <path d="M720 20 C700 40 670 70 640 92" stroke="#3e4a58" strokeWidth={6} fill="none" strokeLinecap="round" />
        <g transform="translate(600 120) rotate(-35)">
          <path d="M-30 -60 L30 -60 L36 10 C36 26 -36 26 -36 10 Z" fill="#e8edf2" stroke="#5b6676" strokeWidth={2} />
          <path d="M-36 10 C-30 30 30 30 36 10" fill="#3e4a58" />
          <rect x={-18} y={-48} width={36} height={10} rx={3} fill="#2f6fd6" opacity={0.85} />
        </g>
        <ellipse cx={575} cy={150} rx={20} ry={6} fill="#bfe3ff" opacity={0.8} transform="rotate(-35 575 150)" />
      </g>
      <g {...o('g-us-dalga')}>
        <path d="M575 150 L360 70 L300 250 Z" fill={u('us-isin')} />
        {[0, 1, 2].map((i) => (
          <path key={i} className="cz" pathLength={1} d={`M${545 - i * 45} ${150 - i * 18} q-40 40 -10 ${80 + i * 20}`} stroke="#2f6fd6" strokeWidth={3} fill="none" opacity={0.8} />
        ))}
      </g>
      <g {...o('g-akis')}>
        <path d="M368 440 L372 470 C380 490 500 488 620 440 L660 380" stroke="#cfd8e2" strokeWidth={10} fill="none" strokeLinecap="round" />
        <path className="cz kmb-akis" pathLength={1} d="M368 440 L372 470 C380 490 500 488 620 440 L660 380" stroke="#f2cf55" strokeWidth={5} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('g-torba')} filter={u('golge')}>
        <rect className="boya" x={620} y={330} width={150} height={150} rx={12} fill={u('torba')} stroke="#9aa6b4" strokeWidth={2.5} />
        <path d="M630 405 C670 399 720 399 760 405 L760 466 C760 472 754 474 748 474 L642 474 C636 474 630 472 630 466 Z" fill={u('idrar-torba')} />
        {[350, 375, 400, 425, 450].map((y) => <path key={y} d={`M746 ${y} L766 ${y}`} stroke="#5b6676" strokeWidth={1.5} />)}
      </g>
      <g {...o('g-kultur')} filter={u('golge')}>
        <rect x={520} y={395} width={50} height={64} rx={8} fill={u('plastik')} stroke="#7d8aa0" strokeWidth={2} />
        <rect x={524} y={425} width={42} height={30} rx={4} fill={u('idrar')} opacity={0.85} />
        <rect x={514} y={384} width={62} height={16} rx={4} fill="#c0392b" />
        <rect x={528} y={404} width={34} height={14} fill="#fff" stroke="#c9d3de" />
        <text x={545} y={414} fontSize={7} textAnchor="middle" fill="#5b6676">STERİL</text>
      </g>
      <g {...o('g-ilac')}>
        <path className="cz" pathLength={1} d="M300 30 C320 80 330 150 330 230" stroke="#2f6fd6" strokeWidth={5} fill="none" markerEnd="url(#kmb-ok)" strokeDasharray="0.03 0.015" />
      </g>
    </>
  ),
};

/** Erkek: üretra yolu (mesane boynu → prostatik → membranöz → bulbar → penil → meatus) */
const URETRA = 'M300 236 L300 305 C300 345 330 362 372 352 L470 320 L700 302';

const Erkek: Sahne = {
  ad: 'Erkek alt üriner sistem (yan kesit)',
  gizli: ['e-jel', 'e-kateter', 'e-balon-dogru', 'e-kivrim', 'e-enjektor', 'e-balon-yanlis'],
  etiket: {
    'e-mesane': [300, 120, 'Mesane'],
    'e-prostat': [215, 262, 'Prostat'],
    'e-sfinkter': [215, 312, 'Eksternal sfinkter'],
    'e-uretra': [430, 375, 'Üretra (~1 cm çap)'],
    'e-penil': [560, 250, 'Penis (korpuslar)'],
    'e-glans': [660, 250, 'Glans / prepisyum'],
    'e-meatus': [700, 350, 'Eksternal meatus'],
    'e-testis': [520, 470, 'Testis / epididim'],
    'e-jel': [560, 352, 'Lidokainli jel üretrada'],
    'e-balon-dogru': [400, 150, 'Balon mesanede ✓'],
    'e-balon-yanlis': [300, 410, 'Balon üretrada ✗'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      <PelvisKesit erkek />
      {/* seminal vezikül */}
      <path d="M240 235 C222 222 222 205 238 200 C252 196 262 212 266 228 Z" fill="#e9c5a8" stroke="#b58b6a" strokeWidth={1.5} />
      <Simfiz x={412} y={236} r={-20} />
      <text x={432} y={300} fontSize={12} fill="#7d6a45">simfiz</text>
      {/* ürogenital diyafram */}
      <path d="M250 300 L360 300" stroke="#b65a50" strokeWidth={10} strokeLinecap="round" opacity={0.75} />
      <g {...o('e-mesane')} filter={u('golge')}>
        <path className="boya" d="M228 160 C222 100 270 70 320 72 C372 74 400 110 392 160 C386 200 352 228 306 236 C266 228 232 200 228 160 Z" fill={u('mesane')} stroke="#a8554e" strokeWidth={7} />
        <path d="M242 160 C238 110 278 88 320 90 C362 92 382 120 376 160 C371 192 345 212 306 220 C272 213 246 192 242 160 Z" fill={u('idrar')} opacity={0.88} />
        <path d="M270 100 C292 90 320 88 345 94" stroke="#fff" strokeWidth={4} opacity={0.45} fill="none" strokeLinecap="round" />
        {/* trigon */}
        <path d="M282 214 L306 236 L330 214" stroke="#b85f58" strokeWidth={2} fill="none" opacity={0.7} />
      </g>
      <g {...o('e-prostat')} filter={u('golge')}>
        <path className="boya" d="M262 262 C258 240 280 232 300 232 C322 232 342 242 338 264 C334 284 318 292 300 292 C280 292 266 282 262 262 Z" fill={u('prostat')} stroke="#94594a" strokeWidth={2} />
        {['M272 254 q10 -8 22 -4', 'M310 252 q12 2 18 10', 'M276 276 q14 6 26 0'].map((d) => <path key={d} d={d} stroke="#9a604f" strokeWidth={1.2} fill="none" opacity={0.6} />)}
      </g>
      <g {...o('e-sfinkter')}>
        <rect className="boya" x={282} y={294} width={36} height={18} rx={7} fill="#c5534a" stroke="#8d2f28" strokeWidth={1.5} />
        {[288, 296, 304, 312].map((x) => <path key={x} d={`M${x} 296 l0 14`} stroke="#8d2f28" strokeWidth={1} opacity={0.6} />)}
      </g>
      {/* penis: korpus kavernozumlar + spongiozum */}
      <g {...o('e-penil')} filter={u('golge')}>
        <path d="M392 300 C420 278 460 270 500 270 L640 270 C650 270 650 334 640 334 L500 334 C450 336 412 336 380 352 Z" fill={u('deri')} stroke="#b9805a" strokeWidth={2} />
        <path className="boya" d="M420 288 C450 280 480 280 500 280 L636 280 L636 302 L500 302 C470 302 440 304 420 308 Z" fill={u('korpus')} opacity={0.95} />
        <path d="M440 294 L630 291" stroke="#a85558" strokeWidth={1} opacity={0.6} />
        <path d="M460 312 L636 304 L636 324 L460 330 Z" fill={u('spongiosum')} />
      </g>
      {/* bulbus spongiozum */}
      <ellipse cx={392} cy={352} rx={34} ry={18} fill={u('spongiosum')} transform="rotate(-18 392 352)" />
      {/* skrotum + testis */}
      <g {...o('e-testis')} filter={u('golge')}>
        <path d="M440 336 C420 360 420 430 470 450 C520 468 572 440 570 392 C568 356 540 336 510 334 Z" fill={u('deri')} stroke="#b9805a" strokeWidth={2} />
        <path d="M470 352 C460 370 462 420 495 430" stroke="#c28a66" strokeWidth={1.2} fill="none" opacity={0.6} />
        <ellipse className="boya" cx={505} cy={395} rx={36} ry={28} fill={u('testis')} stroke="#a77d76" strokeWidth={2} />
        <path d="M535 372 C552 380 552 412 532 420" stroke="#b9746d" strokeWidth={8} fill="none" strokeLinecap="round" opacity={0.85} />
      </g>
      <g {...o('e-uretra')}>
        <path d={URETRA} stroke="#a8554e" strokeWidth={13} fill="none" strokeLinecap="round" opacity={0.5} />
        <path className="cz boya-cizgi" pathLength={1} d={URETRA} stroke="#f0b8b2" strokeWidth={8} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('e-glans')} filter={u('golge')}>
        <path className="boya" d="M630 268 C680 262 712 282 712 302 C712 322 680 342 630 336 C622 320 622 284 630 268 Z" fill={u('glans')} stroke="#a85f5a" strokeWidth={2} />
        <path d="M626 266 C640 262 648 268 652 276 M626 338 C640 342 648 336 652 328" stroke="#c28a66" strokeWidth={5} fill="none" strokeLinecap="round" />
        <path d="M650 278 C672 276 690 284 698 294" stroke="#fff" strokeWidth={2.5} opacity={0.5} fill="none" />
      </g>
      <g {...o('e-meatus')}><ellipse className="boya" cx={710} cy={302} rx={4} ry={8} fill="#7d2f2a" /></g>
      <g {...o('e-jel')}>
        <path className="cz boya-cizgi" pathLength={1} d="M710 302 L470 320 L372 352" stroke="#8fc7ff" strokeWidth={14} strokeOpacity={0.65} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('e-kateter')}>
        <path className="cz boya-cizgi" pathLength={1} d="M728 302 L700 302 L470 320 L372 352 C330 362 300 345 300 305 L300 140" stroke="#eef2f6" strokeWidth={7} fill="none" strokeLinecap="round" />
        <circle cx={300} cy={140} r={5} fill="#eef2f6" stroke="#5b6676" strokeWidth={1.2} /><circle cx={300} cy={146} r={1.8} fill="#2e3540" />
        <rect x={728} y={292} width={26} height={20} rx={5} fill="#e3e8ee" stroke="#6b7a90" strokeWidth={1.5} /><rect x={732} y={280} width={8} height={12} rx={2} fill="#ef7d22" />
        <path d="M728 299 L700 299 L470 317 L372 349 C330 359 297 342 297 305 L297 140" stroke="#fff" strokeWidth={2} fill="none" opacity={0.7} />
      </g>
      <g {...o('e-kivrim')}>
        <path className="cz boya-cizgi" pathLength={1} d="M728 302 L700 302 L470 320 L405 340 C350 362 332 318 375 316 C418 314 408 362 352 358" stroke="#eef2f6" strokeWidth={7} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('e-balon-dogru')}>
        <ellipse className="boya" cx={300} cy={170} rx={22} ry={17} fill="#ffffff" fillOpacity={0.7} stroke="#2e9e5b" strokeWidth={3} />
        <ellipse cx={293} cy={164} rx={7} ry={4} fill="#fff" />
      </g>
      <g {...o('e-balon-yanlis')}>
        <ellipse className="boya" cx={350} cy={354} rx={26} ry={18} fill="#d23b3b" fillOpacity={0.75} stroke="#8d1f1f" strokeWidth={3} />
        {[0, 60, 120, 180, 240, 300].map((a) => <path key={a} d={`M${350 + Math.cos(a * Math.PI / 180) * 30} ${354 + Math.sin(a * Math.PI / 180) * 22} l${Math.cos(a * Math.PI / 180) * 10} ${Math.sin(a * Math.PI / 180) * 10}`} stroke="#d23b3b" strokeWidth={2.5} />)}
      </g>
      <g {...o('e-enjektor')} filter={u('golge')}>
        <rect x={772} y={292} width={28} height={20} rx={3} fill={u('plastik')} stroke="#6b7a90" strokeWidth={1.5} />
        <path d="M758 298 L772 296 L772 308 L758 306 Z" fill="#9aa6b4" />
        <text x={786} y={330} fontSize={10} textAnchor="middle" fill="#3e4a58">50 mL</text>
      </g>
    </>
  ),
};

const Travma: Sahne = {
  ad: 'Pelvis kırığı ve üretra yaralanması (önden)',
  gizli: ['t-kirik', 't-kan', 't-yirtik'],
  etiket: {
    't-pelvis': [130, 40, 'Pelvis halkası'],
    't-kirik': [250, 345, 'Pubis kolu kırığı'],
    't-simfiz': [470, 225, 'Simfiz ayrılması'],
    't-uretra': [470, 390, 'Üretra'],
    't-kan': [470, 486, 'Meatusta taze kan'],
    't-yirtik': [300, 420, 'Kısmi yırtık'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      {/* röntgen hissi veren hafif gölge alan */}
      <ellipse cx={400} cy={230} rx={350} ry={210} fill="#dfe5ec" opacity={0.6} />
      <g {...o('t-pelvis')} filter={u('golge')}>
        {/* sakrum */}
        <path d="M350 60 L450 60 C452 100 446 140 432 170 L410 196 L390 196 L368 170 C354 140 348 100 350 60 Z" fill={u('kemik')} stroke="#a8946b" strokeWidth={2} />
        {[85, 115, 145].map((y) => <g key={y}><circle cx={378} cy={y} r={5} fill="#cdbd98" /><circle cx={422} cy={y} r={5} fill="#cdbd98" /></g>)}
        {[0, 1].map((s) => {
          const m = s ? -1 : 1;
          const X = (x: number) => 400 - m * (400 - x);
          return (
            <g key={s}>
              {/* ilium kanadı */}
              <path className="boya" d={`M${X(352)} 66 C${X(300)} 40 ${X(190)} 30 ${X(130)} 70 C${X(100)} 92 ${X(96)} 140 ${X(118)} 180 C${X(140)} 214 ${X(176)} 226 ${X(200)} 236 L${X(250)} 232 C${X(300)} 210 ${X(340)} 180 ${X(366)} 160 Z`} fill={u('kemik')} stroke="#a8946b" strokeWidth={2} />
              <path d={`M${X(140)} 70 C${X(190)} 46 ${X(280)} 50 ${X(340)} 72`} stroke="#fff" strokeWidth={3} opacity={0.6} fill="none" />
              {/* asetabulum + femur başı */}
              <circle cx={X(220)} cy={262} r={40} fill="#d9cba9" stroke="#a8946b" strokeWidth={2} />
              <circle cx={X(220)} cy={262} r={30} fill={u('kemik')} stroke="#a8946b" strokeWidth={1.5} />
              <path d={`M${X(200)} 290 C${X(196)} 330 ${X(186)} 380 ${X(176)} 470`} stroke="#e8dcc0" strokeWidth={42} strokeLinecap="round" fill="none" />
              <path d={`M${X(200)} 290 C${X(196)} 330 ${X(186)} 380 ${X(176)} 470`} stroke="#a8946b" strokeWidth={1.5} fill="none" opacity={0.5} />
              {/* pubis kolları + obturator foramen */}
              <path className="boya" d={`M${X(250)} 240 C${X(300)} 236 ${X(350)} 236 ${X(386)} 230 L${X(388)} 300 C${X(350)} 318 ${X(300)} 336 ${X(262)} 330 C${X(240)} 320 ${X(238)} 280 ${X(250)} 240 Z`} fill={u('kemik')} stroke="#a8946b" strokeWidth={2} />
              <ellipse cx={X(315)} cy={282} rx={34} ry={24} fill="#dfe5ec" stroke="#a8946b" strokeWidth={1.5} />
            </g>
          );
        })}
      </g>
      <g {...o('t-simfiz')}>
        <rect className="boya" x={386} y={228} width={28} height={74} rx={6} fill="#c9d7e6" stroke="#6b7a90" strokeWidth={2} />
        <path d="M400 232 L400 298" stroke="#6b7a90" strokeWidth={1.5} strokeDasharray="4 4" />
      </g>
      <g {...o('t-kirik')}>
        <path className="cz" pathLength={1} d="M292 248 L304 266 L296 280 L312 300 L304 318" stroke="#d23b3b" strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M296 246 L308 264 L300 278 L316 298 L308 316" stroke="#fff" strokeWidth={1.5} fill="none" opacity={0.8} />
      </g>
      {/* penis (önden) */}
      <path d="M368 400 C368 390 432 390 432 400 L428 470 C424 490 376 490 372 470 Z" fill={u('deri')} stroke="#b9805a" strokeWidth={2} filter={u('golge')} />
      <path d="M372 455 C380 446 420 446 428 455 L426 472 C420 490 380 490 374 472 Z" fill={u('glans')} />
      <g {...o('t-uretra')}>
        <path className="cz boya-cizgi" pathLength={1} d="M400 304 L400 480" stroke="#f0b8b2" strokeWidth={9} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('t-yirtik')}>
        <path d="M386 352 L414 342 M386 366 L414 356" stroke="#d23b3b" strokeWidth={4} strokeLinecap="round" />
        <ellipse cx={400} cy={356} rx={16} ry={10} fill="#d23b3b" opacity={0.35} />
      </g>
      <g {...o('t-kan')}>
        <path d="M400 482 C391 492 392 500 400 500 C408 500 409 492 400 482 Z" fill="#b3201f" />
        <path d="M398 486 C396 490 396 493 398 495" stroke="#fff" strokeWidth={1} opacity={0.7} />
      </g>
    </>
  ),
};

/** Malzeme tepsisi v3 (referans: ürün fotoğrafları — soyulur paket, Fr renk kodlu valf, 2000 mL torba, kateter uçlu 50 mL enjektör) */
const MALZEMELER: [string, string, number, number][] = [
  ['m-lateks', 'Lateks Foley kateter (sarı, kısa süreli)', 105, 100],
  ['m-silikon', 'Silikon Foley kateter (beyaz, uzun süreli)', 300, 100],
  ['m-nonsteril', 'Steril olmayan eldiven (temizlik)', 495, 100],
  ['m-steril', 'Steril eldiven (yerleştirme)', 690, 100],
  ['m-jel', 'Lidokainli kayganlaştırıcı jel', 105, 262],
  ['m-izotonik', 'Steril izotonik 10 mL (balon)', 300, 262],
  ['m-enjektor', '10 mL enjektör (balon kanalı)', 495, 262],
  ['m-genis', '50 mL kateter uçlu enjektör', 690, 262],
  ['m-antiseptik', 'Povidon iyot, böbrek küvet, gazlı bez, pens', 105, 420],
  ['m-ortu', 'Steril delikli örtü', 300, 420],
  ['m-torba', 'İdrar torbası 2000 mL', 495, 420],
];

/** Soyulur kateter paketi: kâğıt arka + şeffaf ön, V soyma ucu, etiket */
const KateterPaket = ({ lateks }: { lateks: boolean }) => (
  <g>
    <path d="M-82 -48 L74 -48 L86 -36 L86 46 L-82 46 Z" fill="#f4f1ea" stroke="#b9b1a0" strokeWidth={1.2} />
    <path d="M-82 -48 L74 -48 L86 -36 L86 46 L-82 46 Z" fill="url(#kmb-plastik)" opacity={0.55} />
    <path d="M-82 -48 L-66 -48 L-74 -30 Z M-82 46 L-66 46 L-74 28 Z" fill="#d8d0bd" />
    {[-40, -20, 0, 20, 40].map((y) => <path key={y} d={`M-80 ${y} l6 -4 l6 4`} stroke="#c9c0ab" fill="none" strokeWidth={0.8} />)}
    {/* kateter kıvrımı */}
    <path d="M-60 26 C-30 26 -20 -30 20 -30 C50 -30 60 -6 40 6 C24 16 0 4 4 -10" stroke="#5a4a2a" strokeOpacity={0.25} strokeWidth={10} fill="none" strokeLinecap="round" />
    <path className="boya-cizgi" d="M-60 26 C-30 26 -20 -30 20 -30 C50 -30 60 -6 40 6 C24 16 0 4 4 -10" stroke={lateks ? '#e2b13f' : '#f2f5f8'} strokeWidth={8} fill="none" strokeLinecap="round" />
    <path d="M-60 23 C-30 23 -20 -33 20 -33 C48 -33 56 -12 42 0" stroke="#fff" strokeWidth={2} fill="none" opacity={0.7} />
    {/* uç, delik, sönük balon */}
    <ellipse cx={5} cy={-13} rx={5} ry={4} fill={lateks ? '#e2b13f' : '#f2f5f8'} stroke="#9a8a5a" strokeWidth={0.8} />
    <ellipse cx={10} cy={-17} rx={2.6} ry={1.6} fill="#4a3510" />
    {/* çatal + Fr renk kodlu valf (16 Fr turuncu) */}
    <path d="M-60 26 L-72 18 L-74 26 L-72 34 Z" fill={lateks ? '#d9a83a' : '#e3e8ee'} stroke="#8a7a4a" strokeWidth={0.8} />
    <path d="M-64 20 L-76 8" stroke={lateks ? '#d9a83a' : '#e3e8ee'} strokeWidth={5} strokeLinecap="round" />
    <rect x={-82} y={2} width={10} height={9} rx={2} fill="#ef7d22" stroke="#9a4a0e" strokeWidth={0.8} />
    {/* etiket */}
    <rect x={30} y={18} width={52} height={24} rx={3} fill="#fff" stroke="#c9d3de" />
    <rect x={30} y={18} width={8} height={24} fill="#ef7d22" />
    <text x={60} y={28} fontSize={8} textAnchor="middle" fill="#2f3b4b" fontWeight={700}>16 Fr</text>
    <text x={60} y={38} fontSize={6.5} textAnchor="middle" fill="#5b6676">{lateks ? 'Lateks · 10 mL' : 'Silikon · 10 mL'}</text>
  </g>
);

/** Eldiven: parmak boğumları, bilek manşeti, ışık */
const Eldiven = ({ g, x = 0, y = 0, r = 0, s = 1 }: { g: string; x?: number; y?: number; r?: number; s?: number }) => (
  <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}>
    <path className="boya" d="M-24 44 L-26 6 C-34 0 -44 -12 -38 -18 C-32 -24 -26 -14 -20 -8 L-20 -44 C-20 -52 -9 -52 -9 -44 L-9 -14 L-7 -54 C-7 -62 5 -62 5 -54 L5 -14 L9 -50 C9 -58 20 -58 20 -50 L17 -10 L23 -38 C23 -46 33 -44 32 -36 L27 4 L26 44 Z" fill={u(g)} stroke="#7d8aa0" strokeWidth={1.2} />
    <path d="M-24 34 L26 34" stroke="#7d8aa0" strokeWidth={1} opacity={0.6} />
    {[[-14, -30], [-1, -38], [14, -34], [27, -22]].map(([px, py]) => <path key={px} d={`M${px - 3} ${py} q3 2 6 0`} stroke="#7d8aa0" strokeWidth={0.8} fill="none" opacity={0.6} />)}
    <path d="M-16 -40 L-16 -14 M-2 -50 L-2 -16" stroke="#fff" strokeWidth={1.6} opacity={0.6} />
  </g>
);

const ikon = (id: string) => {
  switch (id) {
    case 'm-lateks': return <KateterPaket lateks />;
    case 'm-silikon': return <KateterPaket lateks={false} />;
    case 'm-nonsteril':
      return (
        <g>
          {/* dispenser kutusu, ağzından eldiven çıkıyor */}
          <path d="M-70 -10 L70 -10 L70 48 L-70 48 Z" fill="#eaf1f8" stroke="#8a9bb0" strokeWidth={1.2} />
          <path d="M-70 -10 L-56 -24 L84 -24 L70 -10 Z" fill="#f6f9fc" stroke="#8a9bb0" strokeWidth={1.2} />
          <path d="M70 -10 L84 -24 L84 34 L70 48 Z" fill="#d3deea" stroke="#8a9bb0" strokeWidth={1.2} />
          <ellipse cx={7} cy={-17} rx={36} ry={5} fill="#b8c8da" />
          <rect x={-60} y={6} width={70} height={14} rx={3} fill="#2f6fd6" />
          <text x={-25} y={16} fontSize={8} fill="#fff" textAnchor="middle" fontWeight={700}>NİTRİL · M</text>
          <Eldiven g="eldiven" x={10} y={-40} r={-8} s={0.7} />
        </g>
      );
    case 'm-steril':
      return (
        <g>
          {/* açılmış steril kâğıt sargı, manşeti katlanmış iki eldiven */}
          <path d="M-84 -46 L84 -46 L84 50 L-84 50 Z" fill="#fbfaf6" stroke="#c9b48a" strokeWidth={1.2} />
          <path d="M0 -46 L0 50" stroke="#e5dcc8" strokeWidth={1.5} />
          <text x={-42} y={-34} fontSize={7} textAnchor="middle" fill="#a08a5a">SOL</text>
          <text x={42} y={-34} fontSize={7} textAnchor="middle" fill="#a08a5a">SAĞ</text>
          <Eldiven g="eldiven-steril" x={-42} y={8} s={0.68} />
          <Eldiven g="eldiven-steril" x={42} y={8} s={0.68} />
          <rect x={-58} y={30} width={32} height={10} fill="#f2e6cf" stroke="#c9b48a" strokeWidth={0.8} />
          <rect x={26} y={30} width={32} height={10} fill="#f2e6cf" stroke="#c9b48a" strokeWidth={0.8} />
        </g>
      );
    case 'm-jel':
      return (
        <g>
          {/* hazır dolu jel uygulayıcı: körük gövde, konik uç, kopartılan kapak */}
          <path className="boya" d="M-74 -14 L22 -14 L22 14 L-74 14 Z" fill={u('plastik')} stroke="#6b7a90" strokeWidth={1.2} />
          <rect x={-70} y={-9} width={88} height={18} fill="#cfe6ff" opacity={0.9} />
          {[-62, -50, -38, -26, -14, -2, 10].map((x) => <path key={x} d={`M${x} -14 l0 28`} stroke="#8fb0d6" strokeWidth={1} />)}
          <path d="M22 -10 L66 -3 L66 3 L22 10 Z" fill={u('plastik')} stroke="#6b7a90" strokeWidth={1.2} />
          <rect x={66} y={-5} width={12} height={10} rx={2} fill="#2f6fd6" />
          <rect x={-86} y={-20} width={12} height={40} rx={3} fill="#6b7a90" />
          <rect x={-58} y={20} width={72} height={18} rx={3} fill="#fff" stroke="#c9d3de" />
          <text x={-22} y={32} fontSize={8} textAnchor="middle" fill="#2f4f6f" fontWeight={700}>Lidokain %2 · 11 mL</text>
        </g>
      );
    case 'm-izotonik':
      return (
        <g>
          {/* plastik ampul (bükerek açılan) */}
          {[-30, 0, 30].map((x, i) => (
            <g key={x} transform={`translate(${x} 0) rotate(${(i - 1) * 6})`}>
              <path className="boya" d="M-12 -30 L12 -30 L14 36 C14 44 -14 44 -14 36 Z" fill={u('plastik')} stroke="#6b7a90" strokeWidth={1.2} />
              <path d="M-8 -30 L-4 -42 L4 -42 L8 -30 Z" fill="#dfe6ee" stroke="#6b7a90" />
              <rect x={-9} y={-50} width={18} height={9} rx={2} fill="#e9eef3" stroke="#6b7a90" />
              <rect x={-11} y={0} width={22} height={24} fill="#fff" opacity={0.9} />
              <text x={0} y={10} fontSize={5.5} textAnchor="middle" fill="#2f4f6f">%0,9</text>
              <text x={0} y={18} fontSize={5.5} textAnchor="middle" fill="#2f4f6f">10 mL</text>
            </g>
          ))}
        </g>
      );
    case 'm-enjektor':
    case 'm-genis': {
      const g = id === 'm-genis';
      const L = g ? 120 : 92, H = g ? 34 : 20;
      return (
        <g>
          {/* hazne, derece çizgileri, piston lastiği, sap; 50 mL'de uzun konik kateter ucu */}
          <rect className="boya" x={-L / 2} y={-H / 2} width={L} height={H} rx={3} fill={u('plastik')} stroke="#6b7a90" strokeWidth={1.2} />
          {Array.from({ length: g ? 10 : 10 }, (_, i) => (
            <path key={i} d={`M${-L / 2 + 6 + i * (L - 12) / 9} ${-H / 2} l0 ${i % 2 ? 4 : 7}`} stroke="#3e4a58" strokeWidth={0.9} />
          ))}
          <text x={L / 2 - 10} y={H / 2 - 4} fontSize={7} textAnchor="end" fill="#3e4a58">{g ? '50 mL' : '10 mL'}</text>
          <rect x={-L / 2 + 10} y={-H / 2 + 2} width={8} height={H - 4} rx={1.5} fill="#2b2f36" />
          <path d={`M${-L / 2 + 10} 0 L${-L / 2 - 30} 0`} stroke="#cfd8e2" strokeWidth={g ? 9 : 6} />
          <rect x={-L / 2 - 38} y={-H / 2 - 4} width={8} height={H + 8} rx={2} fill="#c9d3de" stroke="#6b7a90" />
          <path d={`M${-L / 2} ${-H / 2 - 5} L${-L / 2} ${H / 2 + 5}`} stroke="#6b7a90" strokeWidth={4} strokeLinecap="round" />
          {g ? <path d={`M${L / 2} -9 L${L / 2 + 34} -3 L${L / 2 + 34} 3 L${L / 2} 9 Z`} fill={u('plastik')} stroke="#6b7a90" strokeWidth={1.2} />
            : <g><path d={`M${L / 2} -4 L${L / 2 + 10} -3 L${L / 2 + 10} 3 L${L / 2} 4 Z`} fill="#c9d3de" stroke="#6b7a90" /><rect x={L / 2 + 10} y={-5} width={6} height={10} fill="#9aa6b4" /></g>}
          {g && <text x={0} y={H / 2 + 14} fontSize={7} textAnchor="middle" fill="#5b6676">kateter ucu ≠ Luer ucu</text>}
        </g>
      );
    }
    case 'm-antiseptik':
      return (
        <g>
          {/* böbrek küvet + pamuk/gazlı bez + povidon şişe + pens */}
          <path d="M-20 10 C-20 -14 80 -14 80 10 C80 40 52 50 30 36 C8 50 -20 40 -20 10 Z" fill={u('metal')} stroke="#5b6676" strokeWidth={1.2} />
          <path d="M-10 12 C-10 -4 70 -4 70 12 C70 30 50 38 30 28 C10 38 -10 30 -10 12 Z" fill="#c5cdd6" />
          {[[8, 10], [24, 4], [40, 12], [56, 6]].map(([x, y]) => <circle key={x} cx={x} cy={y} r={7} fill="#fff" stroke="#d6dde5" />)}
          <circle cx={46} cy={20} r={7} fill="#a74b17" opacity={0.85} />
          <rect className="boya" x={-80} y={-36} width={40} height={74} rx={9} fill={u('povidon')} />
          <path d="M-72 -36 L-72 -46 L-48 -46 L-48 -36" fill="#e9eef3" stroke="#9aa6b4" />
          <rect x={-66} y={-54} width={12} height={9} rx={2} fill="#e9eef3" stroke="#9aa6b4" />
          <rect x={-76} y={-8} width={32} height={26} fill="#fff" opacity={0.88} />
          <text x={-60} y={3} fontSize={6} textAnchor="middle" fill="#7a3410" fontWeight={700}>POVİDON</text>
          <text x={-60} y={12} fontSize={6} textAnchor="middle" fill="#7a3410">İYOT %10</text>
          <path d="M-14 -40 L74 -22 M-14 -36 L74 -26" stroke={u('metal')} strokeWidth={3.5} strokeLinecap="round" />
          <circle cx={-14} cy={-38} r={6} fill="none" stroke="#6d7884" strokeWidth={2.5} />
        </g>
      );
    case 'm-ortu':
      return (
        <g>
          <path className="boya" d="M-84 -48 L84 -48 L84 50 L-84 50 Z M0 -16 C-20 -16 -20 18 0 18 C20 18 20 -16 0 -16 Z" fill={u('ortu')} fillRule="evenodd" stroke="#2c5f91" strokeWidth={1.2} />
          <path d="M-84 -12 L-20 -12 M20 -12 L84 -12 M-84 16 L-22 16 M22 16 L84 16" stroke="#2c5f91" strokeWidth={1} opacity={0.5} />
          <path d="M-84 -48 L84 -48" stroke="#fff" strokeWidth={2} opacity={0.4} />
          <circle cx={0} cy={1} r={20} fill="none" stroke="#9cc6ec" strokeWidth={2} strokeDasharray="3 3" />
        </g>
      );
    default:
      return (
        <g>
          {/* askı, giriş hortumu + geri akış valfi, derece, boşaltma musluğu */}
          <path d="M-46 -56 C-46 -66 46 -66 46 -56" stroke="#9aa6b4" strokeWidth={3} fill="none" />
          <rect className="boya" x={-50} y={-54} width={100} height={104} rx={10} fill={u('torba')} stroke="#9aa6b4" strokeWidth={1.6} />
          <path d="M-44 10 C-20 6 20 6 44 10 L44 42 C44 46 40 48 36 48 L-36 48 C-40 48 -44 46 -44 42 Z" fill={u('idrar-torba')} />
          {[-40, -26, -12, 2, 16, 30].map((y, i) => <g key={y}><path d={`M30 ${y} L44 ${y}`} stroke="#5b6676" strokeWidth={1} /><text x={27} y={y + 3} fontSize={5.5} textAnchor="end" fill="#5b6676">{(6 - i) * 300}</text></g>)}
          <rect x={-10} y={-54} width={14} height={20} rx={4} fill="#eef3f8" stroke="#9aa6b4" />
          <path d="M-3 -54 C-3 -76 50 -80 80 -66" stroke="#cfd8e2" strokeWidth={6} fill="none" strokeLinecap="round" />
          <rect x={74} y={-72} width={14} height={10} rx={2} fill="#eef3f8" stroke="#9aa6b4" />
          <rect x={-8} y={50} width={16} height={12} rx={3} fill="#6b7a90" />
          <rect x={6} y={53} width={12} height={6} rx={2} fill="#c0392b" />
        </g>
      );
  }
};

const Malzeme: Sahne = {
  ad: 'Üretral kateter malzeme tepsisi',
  gizli: ['m-steril-alan'],
  etiket: { 'm-jel': [105, 335, 'Kayganlaştırır + anestezi'] },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      {/* paslanmaz tepsi: kenar, iç yüzey yansıması */}
      <rect x={8} y={8} width={784} height={484} rx={24} fill={u('metal')} filter={u('golge')} />
      <rect x={18} y={18} width={764} height={464} rx={18} fill={u('zemin-tepsi')} />
      <path d="M30 30 L770 30" stroke="#fff" strokeOpacity={0.6} strokeWidth={2} />
      <g {...o('m-steril-alan')}>
        <rect x={200} y={20} width={580} height={330} rx={14} fill="#cfe7d8" opacity={0.45} />
        <rect className="cz" pathLength={1} x={200} y={20} width={580} height={330} rx={14} fill="none" stroke="#2e9e5b" strokeWidth={4} strokeDasharray="0.02 0.01" />
      </g>
      {MALZEMELER.map(([id, ad, x, y]) => (
        <g key={id} {...o(id)}>
          <g transform={`translate(${x} ${y - 8})`} filter={u('golge')}>{ikon(id)}</g>
          {(() => {
            const [bas, ...kalan] = ad.split(/ (?=\()|, (?=[a-zçğıöşü])/);
            return (
              <text x={x} y={y + 60} textAnchor="middle" fontSize={11.5} fill="#2f3b4b" fontWeight={600}>
                {bas}{kalan.length > 0 && <tspan x={x} dy={13} fontSize={10} fontWeight={400} fill="#5b6676">{kalan.join(', ')}</tspan>}
              </text>
            );
          })()}
        </g>
      ))}
      {/* boş köşe: Fr renk kodu kartı */}
      <g transform="translate(690 420)">
        <rect x={-86} y={-56} width={172} height={104} rx={8} fill="#fff" stroke="#c9d3de" />
        <text x={0} y={-40} fontSize={9} textAnchor="middle" fill="#2f3b4b" fontWeight={700}>Valf renkleri (Fr)</text>
        {[['12', '#ffffff'], ['14', '#2e9e5b'], ['16', '#ef7d22'], ['18', '#d23b3b'], ['20', '#f2d000'], ['22', '#8e44ad']].map(([f, c], i) => (
          <g key={f} transform={`translate(${-76 + (i % 3) * 54} ${-20 + Math.floor(i / 3) * 34})`}>
            <rect x={0} y={0} width={16} height={14} rx={3} fill={c} stroke="#5b6676" strokeWidth={0.8} />
            <text x={20} y={11} fontSize={9.5} fill="#2f3b4b">{f} Fr</text>
          </g>
        ))}
      </g>
    </>
  ),
};

/** Sınav maketi (referans: kadın/erkek değiştirilebilir kateter eğitim maketi) — öğrenci sınavda bununla uygular */
const Maket: Sahne = {
  ad: 'Sınav maketi: değiştirilebilir kadın / erkek modülü',
  gizli: ['mk-erkek', 'mk-hazne-dolu'],
  etiket: {
    'mk-govde': [400, 40, 'Pelvis gövdesi + uyluklar'],
    'mk-kadin': [640, 250, 'Kadın genital modülü'],
    'mk-erkek': [640, 250, 'Erkek genital modülü'],
    'mk-hazne': [160, 110, 'Mesane haznesi (su doldurulur)'],
    'mk-hazne-dolu': [160, 110, 'Dolu hazne: kateterden "idrar" gelir'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      <ellipse cx={400} cy={470} rx={320} ry={20} fill="#1d2733" opacity={0.12} />
      <g {...o('mk-govde')} filter={u('golge')}>
        <path className="boya" d="M200 60 C260 40 540 40 600 60 L620 210 C622 240 600 260 580 270 L220 270 C200 260 178 240 180 210 Z" fill="#f0c3a4" stroke="#c98f6b" strokeWidth={2} />
        {/* uyluklar */}
        <path className="boya" d="M190 230 C150 260 110 330 110 400 C110 440 190 460 250 440 C300 420 330 360 340 300 Z" fill="#f0c3a4" stroke="#c98f6b" strokeWidth={2} />
        <path className="boya" d="M610 230 C650 260 690 330 690 400 C690 440 610 460 550 440 C500 420 470 360 460 300 Z" fill="#f0c3a4" stroke="#c98f6b" strokeWidth={2} />
        <ellipse cx={180} cy={415} rx={66} ry={34} fill="#e7b392" stroke="#c98f6b" strokeWidth={2} />
        <ellipse cx={620} cy={415} rx={66} ry={34} fill="#e7b392" stroke="#c98f6b" strokeWidth={2} />
        <path d="M230 70 C300 58 500 58 570 70" stroke="#fff" strokeWidth={4} opacity={0.4} fill="none" />
        {/* üst kapak vidaları */}
        <circle cx={300} cy={100} r={12} fill="#f08c8c" stroke="#b55c5c" strokeWidth={2} /><circle cx={500} cy={100} r={12} fill="#f08c8c" stroke="#b55c5c" strokeWidth={2} />
      </g>
      <g {...o('mk-hazne')}>
        <path className="boya" d="M340 80 C340 64 460 64 460 80 L456 140 C454 152 346 152 344 140 Z" fill="#8f3c3a" stroke="#5c1f1d" strokeWidth={2} />
        <path d="M352 86 C380 78 420 78 448 86" stroke="#c9827c" strokeWidth={3} fill="none" />
      </g>
      <g {...o('mk-hazne-dolu')}>
        <path d="M346 104 C380 98 420 98 454 104 L452 138 C450 146 350 146 348 138 Z" fill={u('idrar')} opacity={0.9} />
      </g>
      {/* modül yuvası */}
      <path d="M340 200 C340 186 460 186 460 200 L470 330 C470 360 330 360 330 330 Z" fill="#e6b190" stroke="#c98f6b" strokeWidth={2} />
      <g {...o('mk-kadin')}>
        <path className="boya" d="M400 205 C362 208 350 260 354 300 C358 336 380 350 400 350 C420 350 442 336 446 300 C450 260 438 208 400 205 Z" fill="#e7a3a0" stroke="#b56c62" strokeWidth={2} />
        <path d="M400 222 C382 226 376 270 382 304 C386 326 394 334 400 334 C406 334 414 326 418 304 C424 270 418 226 400 222 Z" fill="#c56e6a" />
        <circle cx={400} cy={236} r={5} fill="#7d2f2a" />
        <ellipse cx={400} cy={300} rx={10} ry={20} fill="#6e2420" />
        <rect x={360} y={200} width={14} height={10} rx={2} fill="#dfe6ee" /><rect x={426} y={200} width={14} height={10} rx={2} fill="#dfe6ee" />
      </g>
      <g {...o('mk-erkek')}>
        <path className="boya" d="M360 220 C360 200 440 200 440 220 L436 300 C436 330 364 330 364 300 Z" fill="#e6b190" stroke="#c98f6b" strokeWidth={2} />
        <path className="boya" d="M384 250 L416 250 L418 380 C418 404 382 404 382 380 Z" fill={u('deri')} stroke="#b9805a" strokeWidth={2} />
        <ellipse cx={400} cy={392} rx={20} ry={16} fill={u('glans')} stroke="#a85f5a" />
        <ellipse cx={400} cy={404} rx={3} ry={5} fill="#6e2420" />
        <ellipse cx={372} cy={330} rx={22} ry={26} fill="#e2a783" /><ellipse cx={428} cy={330} rx={22} ry={26} fill="#e2a783" />
      </g>
    </>
  ),
};

/** Yatan hasta (üstten): baş, gövde örtüsü, kollar, bacaklar */
const Hasta = ({ y, kadin = false }: { y: number; kadin?: boolean }) => (
  <g>
    <ellipse cx={205} cy={y} rx={26} ry={24} fill={u('deri')} stroke="#b9805a" strokeWidth={1.5} />
    <path d={`M182 ${y - 10} C186 ${y - 30} 224 ${y - 30} 228 ${y - 10}`} fill={kadin ? '#5a3a24' : '#3b2a1e'} />
    <path d={`M232 ${y - 28} L420 ${y - 30} C432 ${y - 30} 436 ${y + 30} 420 ${y + 30} L232 ${y + 28} C222 ${y + 20} 222 ${y - 20} 232 ${y - 28} Z`} fill={u('onluk')} stroke="#4c8590" strokeWidth={1.5} />
    <path d={`M250 ${y - 34} L400 ${y - 36} M250 ${y + 34} L400 ${y + 36}`} stroke={u('deri')} strokeWidth={12} strokeLinecap="round" />
  </g>
);

const Pozisyon: Sahne = {
  ad: 'Mahremiyet ve hasta pozisyonu (üstten)',
  gizli: ['p-paravan', 'p-yardimci', 'p-v'],
  etiket: {
    'p-hekim': [90, 40, 'Hekim: tanıt, anlat, onam al'],
    'p-paravan': [712, 40, 'Paravan / perde'],
    'p-yardimci': [660, 485, 'Yardımcı personel'],
    'p-erkek': [390, 78, 'Erkek: supin'],
    'p-kadin': [390, 278, 'Kadın: modifiye litotomi'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      {/* yataklar */}
      {[[150, 92, 120], [150, 290, 190]].map(([x, y, h]) => (
        <g key={y} filter={u('golge')}>
          <rect x={x} y={y} width={480} height={h} rx={14} fill="#9aa6b4" />
          <rect x={x + 6} y={y + 6} width={468} height={h - 12} rx={10} fill={u('yatak')} />
          <rect x={x + 14} y={y + h / 2 - 30} width={56} height={60} rx={14} fill="#ffffff" stroke="#d6dee7" />
        </g>
      ))}
      <g {...o('p-erkek')}>
        <Hasta y={152} />
        <path className="boya" d="M420 128 L612 132 C620 132 620 146 612 146 L420 148 Z" fill={u('deri')} stroke="#b9805a" />
        <path className="boya" d="M420 156 L612 158 C620 158 620 172 612 172 L420 176 Z" fill={u('deri')} stroke="#b9805a" />
        <rect x={416} y={126} width={22} height={52} rx={6} fill="#ffffff" opacity={0.9} />
      </g>
      <g {...o('p-kadin')}>
        <Hasta y={385} kadin />
        {/* bükülü dizler, V açılmış bacaklar, topuklar yatakta */}
        <path className="boya" d="M420 362 L520 312 C530 306 540 318 532 326 L436 380 Z" fill={u('deri')} stroke="#b9805a" />
        <path className="boya" d="M520 312 L604 332 C614 334 612 348 602 348 L524 330 Z" fill={u('deri')} stroke="#b9805a" />
        <path className="boya" d="M420 408 L520 458 C530 464 540 452 532 444 L436 390 Z" fill={u('deri')} stroke="#b9805a" />
        <path className="boya" d="M520 458 L604 438 C614 436 612 422 602 422 L524 440 Z" fill={u('deri')} stroke="#b9805a" />
        <ellipse cx={522} cy={318} rx={12} ry={10} fill="#e2a783" /><ellipse cx={522} cy={452} rx={12} ry={10} fill="#e2a783" />
        <ellipse cx={606} cy={340} rx={9} ry={12} fill="#d9946c" /><ellipse cx={606} cy={430} rx={9} ry={12} fill="#d9946c" />
      </g>
      <g {...o('p-v')}>
        <path className="cz" pathLength={1} d="M612 322 L440 385 L612 448" stroke="#2f6fd6" strokeWidth={4} fill="none" strokeDasharray="0.03 0.015" />
        <text x={470} y={390} fontSize={14} fill="#2f6fd6" fontWeight={700}>V</text>
      </g>
      <g {...o('p-hekim')} filter={u('golge')}>
        <path className="boya" d="M50 150 C50 120 130 120 130 150 L138 270 L42 270 Z" fill={u('beyaz-onluk')} stroke="#9aa6b4" strokeWidth={1.5} />
        <path d="M90 128 L90 270" stroke="#c9d3de" />
        <circle cx={90} cy={104} r={24} fill={u('deri')} stroke="#b9805a" />
        <path d="M66 98 C68 76 112 76 114 98 C104 90 76 90 66 98 Z" fill="#3b2a1e" />
        <path d="M76 140 C70 170 84 190 96 196" stroke="#5b6676" strokeWidth={2.5} fill="none" />
        <circle cx={97} cy={198} r={5} fill="#5b6676" />
      </g>
      <g {...o('p-paravan')} filter={u('golge')}>
        {[0, 1, 2].map((i) => (
          <g key={i}>
            <rect x={662 + i * 34} y={70 + (i % 2) * 6} width={32} height={390} rx={4} fill="#e6eef7" fillOpacity={0.85} stroke="#7d8aa0" strokeWidth={2} />
            {[130, 200, 270, 340, 410].map((y) => <path key={y} d={`M${664 + i * 34} ${y} L${692 + i * 34} ${y}`} stroke="#c3cfdc" />)}
          </g>
        ))}
        <path className="cz" pathLength={1} d="M662 70 L764 70 L764 466 L662 466 Z" stroke="#7d8aa0" strokeWidth={2} fill="none" />
      </g>
      <g {...o('p-yardimci')} filter={u('golge')}>
        <path className="boya" d="M640 380 C640 356 700 356 700 380 L706 468 L634 468 Z" fill={u('onluk')} stroke="#4c8590" />
        <circle cx={670} cy={340} r={20} fill={u('deri')} stroke="#b9805a" />
        <path d="M650 334 C652 316 688 316 690 334 C682 328 658 328 650 334 Z" fill="#5a3a24" />
      </g>
    </>
  ),
};

const Kadin: Sahne = {
  ad: 'Kadın dış genital bölge (litotomide, önden)',
  gizli: ['k-temizlik', 'k-ortu', 'k-halka', 'k-kateter', 'k-idrar'],
  etiket: {
    'k-majus': [150, 130, 'Labium majus'],
    'k-minus': [190, 230, 'Labium minus'],
    'k-klitoris': [540, 118, 'Klitoris'],
    'k-meatus': [575, 205, 'Eksternal üretra ağzı (meatus)'],
    'k-vajina': [560, 300, 'Vajina girişi'],
    'k-ortu': [150, 470, 'Steril delikli örtü'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      {/* uyluklar */}
      <path d="M0 60 C120 70 220 150 260 300 C280 380 270 460 250 500 L0 500 Z" fill={u('deri')} />
      <path d="M800 60 C680 70 580 150 540 300 C520 380 530 460 550 500 L800 500 Z" fill={u('deri')} />
      <path d="M40 90 C150 110 230 190 252 320" stroke="#c28a66" strokeWidth={2} fill="none" opacity={0.4} />
      <path d="M760 90 C650 110 570 190 548 320" stroke="#c28a66" strokeWidth={2} fill="none" opacity={0.4} />
      {/* mons pubis */}
      <path d="M260 20 C320 0 480 0 540 20 C560 50 540 80 520 90 L280 90 C260 80 240 50 260 20 Z" fill={u('deri')} />
      <rect x={270} y={8} width={260} height={78} fill="url(#kmb-kil)" opacity={0.7} rx={30} />
      <g {...o('k-majus')} filter={u('golge')}>
        <path className="boya" d="M400 62 C300 66 252 170 262 300 C270 390 320 452 400 456 C480 452 530 390 538 300 C548 170 500 66 400 62 Z" fill={u('deri')} stroke="#b9805a" strokeWidth={2} />
        <path d="M320 110 C290 170 288 290 318 380" stroke="#c28a66" strokeWidth={3} fill="none" opacity={0.5} />
        <path d="M480 110 C510 170 512 290 482 380" stroke="#c28a66" strokeWidth={3} fill="none" opacity={0.5} />
      </g>
      {/* vestibül zemini */}
      <path d="M400 112 C350 120 334 220 346 320 C352 370 376 400 400 402 C424 400 448 370 454 320 C466 220 450 120 400 112 Z" fill={u('mukoza')} />
      <g {...o('k-minus')}>
        <path className="boya" d="M400 112 C356 118 330 200 336 300 C340 360 366 400 392 404 C366 380 356 330 358 280 C360 210 372 150 400 130 Z" fill="#d9928c" stroke="#a85f5a" strokeWidth={1.8} />
        <path className="boya" d="M400 112 C444 118 470 200 464 300 C460 360 434 400 408 404 C434 380 444 330 442 280 C440 210 428 150 400 130 Z" fill="#d9928c" stroke="#a85f5a" strokeWidth={1.8} />
        <path d="M350 200 C346 250 348 300 360 350 M450 200 C454 250 452 300 440 350" stroke="#f2b8b2" strokeWidth={1.5} fill="none" opacity={0.8} />
      </g>
      {/* klitoral başlık */}
      <path d="M372 128 C380 112 420 112 428 128 C420 140 380 140 372 128 Z" fill="#d49a8e" stroke="#a8705f" strokeWidth={1.2} />
      <g {...o('k-klitoris')}><ellipse className="boya" cx={400} cy={142} rx={8} ry={9} fill={u('glans')} stroke="#a85f5a" strokeWidth={1.2} /></g>
      <g {...o('k-meatus')}>
        <ellipse cx={400} cy={208} rx={10} ry={8} fill="#e8a7a2" />
        <path className="boya" d="M400 201 C396 204 396 212 400 215 C404 212 404 204 400 201 Z" fill="#7d2f2a" />
      </g>
      <g {...o('k-vajina')}>
        <path className="boya" d="M400 252 C374 256 368 300 372 330 C376 356 390 370 400 370 C410 370 424 356 428 330 C432 300 426 256 400 252 Z" fill="#8f3c3a" stroke="#c9827c" strokeWidth={5} />
        {[[376, 300], [424, 300], [384, 350], [416, 350]].map(([x, y]) => <circle key={`${x}${y}`} cx={x} cy={y} r={3.5} fill="#d9928c" />)}
      </g>
      {/* perine + anüs */}
      <path d="M392 406 L408 406" stroke="#c28a66" strokeWidth={2} />
      <circle cx={400} cy={470} r={12} fill="#9a5f48" />
      {[0, 45, 90, 135, 180, 225, 270, 315].map((a) => <path key={a} d={`M${400 + Math.cos(a * Math.PI / 180) * 7} ${470 + Math.sin(a * Math.PI / 180) * 7} l${Math.cos(a * Math.PI / 180) * 7} ${Math.sin(a * Math.PI / 180) * 7}`} stroke="#7d4a36" strokeWidth={1.2} />)}
      <g {...o('k-temizlik')}>
        <path className="cz" pathLength={1} d="M400 208 c22 0 28 26 0 34 c-40 9 -50 -54 0 -62 c64 -9 78 108 0 126 c-82 14 -100 -154 0 -176 c100 -18 128 208 0 236" stroke="#2e9e5b" strokeWidth={4} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('k-ortu')}>
        <path d="M140 30 L660 30 L660 490 L140 490 Z M400 100 C330 104 320 360 400 380 C480 360 470 104 400 100 Z" fill={u('ortu')} fillOpacity={0.82} fillRule="evenodd" stroke="#2c5f91" strokeWidth={2} />
        <path d="M160 60 L640 60 M160 460 L640 460" stroke="#fff" opacity={0.25} />
      </g>
      <g {...o('k-halka')} filter={u('golge')}>
        {/* steril eldivenli avuç + halka */}
        <path d="M640 280 C620 300 618 360 650 384 C690 410 760 396 780 360 L790 300 C770 270 690 262 640 280 Z" fill={u('eldiven-steril')} stroke="#b59c72" strokeWidth={1.5} />
        <circle className="cz" pathLength={1} cx={700} cy={335} r={40} stroke="#e3b544" strokeWidth={7} fill="none" />
        <circle className="cz" pathLength={1} cx={700} cy={335} r={28} stroke="#e3b544" strokeWidth={7} fill="none" />
        <path d="M672 318 C690 300 720 300 736 316" stroke="#fff" strokeWidth={2} fill="none" opacity={0.6} />
      </g>
      <g {...o('k-kateter')}>
        <path d="M700 295 C650 235 520 208 404 208" stroke="#5a4a2a" strokeOpacity={0.3} strokeWidth={9} fill="none" strokeLinecap="round" />
        <path className="cz boya-cizgi" pathLength={1} d="M700 295 C650 235 520 208 404 208" stroke="#e3b544" strokeWidth={7} fill="none" strokeLinecap="round" />
        <path d="M700 292 C650 232 520 205 404 205" stroke="#fff" strokeWidth={1.8} fill="none" opacity={0.6} />
      </g>
      <g {...o('k-idrar')}>
        <path className="cz kmb-akis" pathLength={1} d="M600 230 C650 260 690 300 740 380 L760 470" stroke="#f2cf55" strokeWidth={4} fill="none" strokeLinecap="round" />
      </g>
    </>
  ),
};

// ———————————————————— Yakın plan sahneleri (adımda ana sahnenin yanında 2.–3. görsel)

const YakinMesane: Sahne = {
  ad: 'Yakın plan: kateter ucu mesane boynunda',
  gizli: ['y-kateter', 'y-delik', 'y-balon-sonuk', 'y-balon', 'y-idrar', 'y-cekme'],
  etiket: {
    'y-duvar': [130, 40, 'Mesane duvarı (detrüsör)'],
    'y-trigon': [400, 160, 'Trigon'],
    'y-ureter': [215, 205, 'Üreter ağzı'],
    'y-boyun': [560, 360, 'Mesane boynu'],
    'y-prostat': [130, 450, 'Prostat / prostatik üretra'],
    'y-delik': [560, 215, 'Uçtaki delikler: idrar girer'],
    'y-balon-sonuk': [565, 285, 'Sönük balon'],
    'y-balon': [590, 285, 'Balon: 10 mL izotonik'],
    'y-idrar': [250, 120, 'İdrar deliklerden kanala'],
    'y-cekme': [640, 440, 'Hafifçe çek: balon boyna oturur'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      <g {...o('y-duvar')}>
        <path className="boya" d="M20 20 L780 20 L780 330 C700 330 560 330 470 360 L470 500 L330 500 L330 360 C240 330 100 330 20 330 Z" fill={u('mesane')} />
        {/* rugalar: detrüsör demetleri */}
        {Array.from({ length: 9 }, (_, i) => (
          <path key={i} d={`M${40 + i * 85} 40 C${60 + i * 85} 120 ${20 + i * 85} 200 ${50 + i * 85} 300`} stroke="#c06a63" strokeWidth={6} fill="none" opacity={0.35} strokeLinecap="round" />
        ))}
        <path d="M60 30 C200 60 600 60 740 30" stroke="#fff" strokeWidth={4} opacity={0.25} fill="none" />
      </g>
      {/* lümen: idrar */}
      <path d="M60 50 L740 50 L740 300 C650 300 540 305 455 335 L345 335 C260 305 150 300 60 300 Z" fill={u('idrar')} opacity={0.75} />
      <g {...o('y-trigon')}>
        <path className="boya" d="M220 220 L580 220 L400 330 Z" fill="#f3b3ac" opacity={0.85} stroke="#c06a63" strokeWidth={2} />
        <path d="M240 228 L560 228" stroke="#c06a63" strokeWidth={3} opacity={0.5} />
      </g>
      <g {...o('y-ureter')}>
        <ellipse className="boya" cx={222} cy={222} rx={14} ry={7} fill="#8f3c3a" />
        <ellipse cx={578} cy={222} rx={14} ry={7} fill="#8f3c3a" />
      </g>
      <g {...o('y-boyun')}>
        <path className="boya-cizgi" d="M345 335 C360 350 380 356 400 356 C420 356 440 350 455 335" stroke="#a8554e" strokeWidth={8} fill="none" />
      </g>
      <g {...o('y-prostat')}>
        <path className="boya" d="M200 360 C240 345 300 345 345 360 L345 500 L180 500 C170 450 175 390 200 360 Z" fill={u('prostat')} stroke="#94594a" strokeWidth={2} />
        <path className="boya" d="M600 360 C560 345 500 345 455 360 L455 500 L620 500 C630 450 625 390 600 360 Z" fill={u('prostat')} stroke="#94594a" strokeWidth={2} />
      </g>
      {/* üretra lümeni */}
      <path d="M345 356 L345 500 L455 500 L455 356 C430 366 370 366 345 356 Z" fill="#e8a7a2" />
      <g {...o('y-kateter')}>
        <rect x={376} y={150} width={48} height={350} fill="#6b7a90" opacity={0.25} />
        <rect className="boya" x={378} y={150} width={44} height={350} fill={u('silikon')} stroke="#8a96a6" strokeWidth={1.5} />
        <path d="M378 150 C378 118 422 118 422 150 Z" fill={u('silikon')} stroke="#8a96a6" strokeWidth={1.5} />
        {/* iç kanallar */}
        <path d="M392 170 L392 500" stroke="#c9d3de" strokeWidth={10} opacity={0.6} />
        <path d="M413 260 L413 500" stroke="#9fc4ef" strokeWidth={4} opacity={0.8} />
      </g>
      <g {...o('y-delik')}>
        <ellipse className="boya" cx={400} cy={168} rx={13} ry={8} fill="#3e4a58" />
        <ellipse cx={400} cy={196} rx={11} ry={7} fill="#3e4a58" opacity={0.8} />
      </g>
      <g {...o('y-balon-sonuk')}>
        <rect className="boya" x={372} y={250} width={56} height={40} rx={14} fill="#eef3f8" stroke="#8a96a6" strokeWidth={2} />
      </g>
      <g {...o('y-balon')}>
        <ellipse className="boya" cx={400} cy={290} rx={78} ry={46} fill="#e6f1fc" fillOpacity={0.85} stroke="#5b8fc9" strokeWidth={3} />
        <ellipse cx={400} cy={300} rx={64} ry={28} fill="#b9d8f7" opacity={0.6} />
        <ellipse cx={372} cy={272} rx={18} ry={8} fill="#fff" opacity={0.85} />
      </g>
      <g {...o('y-idrar')}>
        {[[300, 110], [250, 160], [500, 120], [540, 170]].map(([x, y], i) => (
          <path key={i} className="cz kmb-akis" pathLength={1} d={`M${x} ${y} C${(x + 400) / 2} ${y + 10} ${400 + (x < 400 ? -16 : 16)} 170 400 172`} stroke="#d9a400" strokeWidth={3} fill="none" strokeLinecap="round" />
        ))}
      </g>
      <g {...o('y-cekme')}>
        <path className="cz" pathLength={1} d="M520 380 L520 470" stroke="#2f6fd6" strokeWidth={5} fill="none" markerEnd="url(#kmb-ok)" />
      </g>
    </>
  ),
};

const YakinUretra: Sahne = {
  ad: 'Yakın plan: üretra boyuna kesiti',
  gizli: ['z-kivrim', 'z-balon', 'z-yirtik', 'z-kan', 'z-sivi', 'z-dogru'],
  etiket: {
    'z-mukoza': [130, 60, 'Üretra mukozası'],
    'z-spongiozum': [130, 450, 'Korpus spongiozum'],
    'z-sfinkter': [400, 60, 'Eksternal sfinkter'],
    'z-kivrim': [610, 120, 'Kateter takıldı, kıvrıldı'],
    'z-balon': [400, 440, 'Balon üretrada şişti'],
    'z-yirtik': [520, 440, 'Mukoza yırtığı'],
    'z-sivi': [150, 120, '30–40 mL izotonik geri gelmiyor'],
    'z-dogru': [650, 440, 'Serbest kateter → mesaneye'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      <g {...o('z-spongiozum')}>
        <rect className="boya" x={0} y={90} width={800} height={320} rx={40} fill={u('spongiosum')} />
        {Array.from({ length: 30 }, (_, i) => <circle key={i} cx={20 + (i * 53) % 780} cy={110 + ((i * 37) % 280)} r={5} fill="#b9686b" opacity={0.35} />)}
      </g>
      <g {...o('z-mukoza')}>
        <rect className="boya" x={0} y={200} width={800} height={100} fill={u('mukoza')} />
        {Array.from({ length: 16 }, (_, i) => <path key={i} d={`M${i * 52} 205 q26 14 52 0 M${i * 52} 295 q26 -14 52 0`} stroke="#a8554e" strokeWidth={2} fill="none" opacity={0.6} />)}
      </g>
      <path d="M0 225 L800 225 L800 275 L0 275 Z" fill="#f6cfc9" />
      <g {...o('z-sfinkter')}>
        <rect className="boya" x={340} y={90} width={120} height={320} rx={18} fill="#c5534a" opacity={0.85} />
        {Array.from({ length: 10 }, (_, i) => <path key={i} d={`M${348 + i * 11} 100 L${348 + i * 11} 400`} stroke="#8d2f28" strokeWidth={1.5} opacity={0.6} />)}
        <path d="M340 225 L460 225 L460 275 L340 275 Z" fill="#f6cfc9" />
      </g>
      <g {...o('z-dogru')}>
        <Boru d="M0 250 L800 250" g="silikon" w={22} />
        <path className="cz" pathLength={1} d="M600 380 L760 380" stroke="#2e9e5b" strokeWidth={5} markerEnd="url(#kmb-ok)" />
      </g>
      <g {...o('z-kivrim')}>
        <Boru d="M0 250 L520 250 C600 250 640 230 640 200 C640 160 560 160 560 210 C560 260 620 280 680 260" g="silikon" w={22} cz />
      </g>
      <g {...o('z-balon')}>
        <ellipse className="boya" cx={400} cy={250} rx={110} ry={95} fill="#d23b3b" fillOpacity={0.55} stroke="#8d1f1f" strokeWidth={4} />
        <ellipse cx={370} cy={210} rx={30} ry={14} fill="#fff" opacity={0.5} />
      </g>
      <g {...o('z-yirtik')}>
        {['M300 160 l20 30 l-14 14 l18 26', 'M500 340 l-18 -26 l14 -14 l-20 -30', 'M410 150 l-6 26 l10 12'].map((d) => <path key={d} d={d} stroke="#5c0f0f" strokeWidth={4} fill="none" strokeLinecap="round" />)}
      </g>
      <g {...o('z-kan')}>
        {[[280, 300], [520, 210], [470, 320], [320, 190]].map(([x, y], i) => <path key={i} d={`M${x} ${y} c-8 12 -6 20 0 20 c6 0 8 -8 0 -20 Z`} fill="#b3201f" />)}
        <path className="cz" pathLength={1} d="M200 250 L0 250" stroke="#b3201f" strokeWidth={6} strokeDasharray="0.02 0.02" />
      </g>
      <g {...o('z-sivi')}>
        <path className="cz" pathLength={1} d="M20 150 L300 150" stroke="#2f6fd6" strokeWidth={5} markerEnd="url(#kmb-ok)" />
        <path d="M300 130 L270 110 M300 130 L270 150" stroke="#d23b3b" strokeWidth={5} />
      </g>
    </>
  ),
};

const YakinKadin: Sahne = {
  ad: 'Yakın plan: vestibül ve meatus (eldivenli parmaklar labiaları ayırıyor)',
  gizli: ['v-kateter', 'v-jel', 'v-idrar', 'v-parmak'],
  etiket: {
    'v-klitoris': [400, 40, 'Klitoris'],
    'v-meatus': [560, 170, 'Meatus: üstteki küçük açıklık'],
    'v-vajina': [570, 330, 'Vajina: alttaki geniş açıklık'],
    'v-minus': [140, 250, 'Labium minus'],
    'v-parmak': [140, 450, 'Başparmak + işaret parmağı ayırır'],
    'v-jel': [600, 60, 'Uçta ~2 mL jel'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('mukoza')} />
      <g {...o('v-minus')}>
        <path className="boya" d="M0 20 C140 40 240 160 250 260 C260 360 200 440 120 500 L0 500 Z" fill="#d9928c" stroke="#a85f5a" strokeWidth={3} />
        <path className="boya" d="M800 20 C660 40 560 160 550 260 C540 360 600 440 680 500 L800 500 Z" fill="#d9928c" stroke="#a85f5a" strokeWidth={3} />
        <path d="M30 60 C150 90 220 180 228 270 M770 60 C650 90 580 180 572 270" stroke="#f2b8b2" strokeWidth={3} fill="none" opacity={0.8} />
      </g>
      <g {...o('v-klitoris')}>
        <path d="M330 -10 C350 50 450 50 470 -10" fill="#d49a8e" stroke="#a8705f" strokeWidth={2} />
        <ellipse className="boya" cx={400} cy={42} rx={18} ry={16} fill={u('glans')} stroke="#a85f5a" strokeWidth={2} />
      </g>
      {/* vestibül kıvrımları */}
      <path d="M320 120 C350 140 450 140 480 120" stroke="#b96b67" strokeWidth={2} fill="none" opacity={0.6} />
      <g {...o('v-meatus')}>
        <ellipse cx={400} cy={160} rx={30} ry={22} fill="#eaa7a2" />
        <path className="boya" d="M400 142 C390 150 390 172 400 180 C410 172 410 150 400 142 Z" fill="#6e2420" />
        <path d="M374 156 C380 148 388 146 394 148 M426 156 C420 148 412 146 406 148" stroke="#c97c77" strokeWidth={2} fill="none" />
      </g>
      <g {...o('v-vajina')}>
        <path className="boya" d="M400 240 C330 246 312 330 322 390 C332 450 372 480 400 480 C428 480 468 450 478 390 C488 330 470 246 400 240 Z" fill="#7d2f2d" stroke="#c9827c" strokeWidth={10} />
        {Array.from({ length: 8 }, (_, i) => <path key={i} d={`M${340 + i * 15} ${300 + (i % 2) * 20} q8 12 0 24`} stroke="#a64c48" strokeWidth={2} fill="none" />)}
      </g>
      <g {...o('v-parmak')} filter={u('golge')}>
        <path d="M0 380 C80 360 170 330 230 280 C250 262 270 280 258 300 C220 360 120 430 0 470 Z" fill={u('eldiven-steril')} stroke="#b59c72" strokeWidth={2} />
        <path d="M800 380 C720 360 630 330 570 280 C550 262 530 280 542 300 C580 360 680 430 800 470 Z" fill={u('eldiven-steril')} stroke="#b59c72" strokeWidth={2} />
        <path d="M220 286 C232 276 246 278 250 288 M580 286 C568 276 554 278 550 288" stroke="#fff" strokeWidth={3} fill="none" opacity={0.6} />
      </g>
      <g {...o('v-kateter')}>
        <Boru d="M800 40 C680 60 520 120 404 160" g="lateks" w={16} cz />
      </g>
      <g {...o('v-jel')}>
        <ellipse cx={430} cy={152} rx={30} ry={14} fill="#cfe9ff" opacity={0.75} transform="rotate(-18 430 152)" />
        <ellipse cx={420} cy={148} rx={10} ry={4} fill="#fff" opacity={0.9} transform="rotate(-18 420 148)" />
      </g>
      <g {...o('v-idrar')}>
        <path className="cz kmb-akis" pathLength={1} d="M520 118 C640 80 720 60 800 56" stroke="#e1b300" strokeWidth={6} fill="none" strokeLinecap="round" />
      </g>
    </>
  ),
};

const YakinEl: Sahne = {
  ad: 'Yakın plan: steril eldivenle kateteri avuçta toplamak',
  gizli: ['h-yanlis', 'h-jel'],
  etiket: {
    'h-el': [140, 60, 'Steril eldivenli el'],
    'h-halka': [560, 120, 'Kateter avuçta halka halinde'],
    'h-uc': [690, 300, 'Yalnız uç dışarıda, steril'],
    'h-yanlis': [200, 460, 'Sarkan kateter dokunur → steril değil'],
    'h-jel': [690, 420, 'Uca jel'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      <rect x={0} y={330} width={800} height={170} fill={u('ortu')} opacity={0.7} />
      <g {...o('h-halka')}>
        {[70, 52, 34].map((r, i) => <circle key={r} className={i === 0 ? 'cz' : undefined} pathLength={1} cx={400} cy={220} r={r * 1.6} stroke="#5a4a2a" strokeOpacity={0.25} strokeWidth={14} fill="none" />)}
        {[70, 52, 34].map((r) => <circle key={r} className="boya-cizgi" cx={400} cy={220} r={r * 1.6} stroke="#e3b544" strokeWidth={11} fill="none" />)}
        {[70, 52, 34].map((r) => <circle key={`p${r}`} cx={400} cy={216} r={r * 1.6} stroke="#fff" strokeWidth={2.5} fill="none" opacity={0.5} strokeDasharray="40 60" />)}
      </g>
      <g {...o('h-el')} filter={u('golge')}>
        {/* avuç ve parmaklar halkanın üstünü kavrar */}
        <path className="boya" d="M180 140 C230 90 330 70 420 80 C500 90 560 120 590 170 C610 210 600 250 570 280 C540 310 470 320 420 312 L380 360 C340 380 280 370 250 330 C210 290 160 210 180 140 Z" fill={u('eldiven-steril')} stroke="#b59c72" strokeWidth={2.5} />
        {[0, 1, 2, 3].map((i) => <path key={i} d={`M${300 + i * 60} ${92 - i * 2} C${320 + i * 60} 150 ${330 + i * 55} 220 ${300 + i * 60} 290`} stroke="#c9b08a" strokeWidth={2.5} fill="none" />)}
        <path d="M250 330 C230 290 236 250 270 240 C300 234 320 260 330 300" fill="#f3e5cf" stroke="#b59c72" strokeWidth={2} />
        <path d="M200 140 C240 100 320 86 400 90" stroke="#fff" strokeWidth={4} opacity={0.5} fill="none" />
      </g>
      <g {...o('h-uc')}>
        <Boru d="M560 270 C620 290 660 300 720 300" w={11} />
        <path className="boya" d="M720 290 C740 290 746 296 746 300 C746 304 740 310 720 310 Z" fill={u('lateks')} />
        <ellipse cx={728} cy={298} rx={4} ry={2.5} fill="#5a4214" />
      </g>
      <g {...o('h-jel')}>
        <ellipse cx={725} cy={300} rx={26} ry={13} fill="#cfe9ff" opacity={0.75} />
      </g>
      <g {...o('h-yanlis')}>
        <path d="M260 340 C230 400 160 420 120 470" stroke="#d23b3b" strokeWidth={9} fill="none" strokeLinecap="round" strokeDasharray="14 10" />
        <path d="M90 440 L150 500 M150 440 L90 500" stroke="#d23b3b" strokeWidth={7} strokeLinecap="round" />
      </g>
    </>
  ),
};

const YakinErkekJel: Sahne = {
  ad: 'Yakın plan: glans, meatus ve lidokainli jelin verilmesi',
  gizli: ['j-temizlik', 'j-siringa', 'j-dolum', 'j-parmak'],
  etiket: {
    'j-glans': [290, 60, 'Glans penis'],
    'j-prepisyum': [110, 120, 'Prepisyum geri çekilir'],
    'j-meatus': [560, 160, 'Meatus'],
    'j-temizlik': [480, 440, 'Meatustan dışa, 3 kez'],
    'j-siringa': [660, 90, 'Jel tüpü meatusta'],
    'j-dolum': [160, 450, 'Jel üretrayı doldurur'],
    'j-parmak': [300, 470, 'Ucu sık, 2–3 dk bekle'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      {/* şaft */}
      <path d="M0 150 L260 140 L260 360 L0 350 Z" fill={u('deri')} stroke="#b9805a" strokeWidth={2} />
      <g {...o('j-prepisyum')}>
        <path className="boya" d="M200 130 C240 120 270 130 280 150 L280 350 C270 370 240 380 200 370 C215 330 215 170 200 130 Z" fill="#dca386" stroke="#b9805a" strokeWidth={2} />
        {[160, 200, 240, 280, 320].map((y) => <path key={y} d={`M215 ${y} q20 6 50 0`} stroke="#b9805a" strokeWidth={1.5} fill="none" opacity={0.6} />)}
      </g>
      <g {...o('j-glans')} filter={u('golge')}>
        <path className="boya" d="M270 120 C420 90 560 160 570 250 C560 340 420 410 270 380 C250 330 250 170 270 120 Z" fill={u('glans')} stroke="#a85f5a" strokeWidth={2.5} />
        <path d="M300 140 C400 120 500 160 540 210" stroke="#fff" strokeWidth={5} opacity={0.4} fill="none" strokeLinecap="round" />
        <path d="M280 140 C300 200 300 300 280 360" stroke="#a85f5a" strokeWidth={3} fill="none" opacity={0.6} />
      </g>
      <g {...o('j-dolum')}>
        <path className="cz" pathLength={1} d="M560 250 L0 252" stroke="#8fc7ff" strokeWidth={22} strokeOpacity={0.7} fill="none" />
      </g>
      <g {...o('j-meatus')}>
        <path className="boya" d="M566 222 C556 236 556 264 566 278 C574 264 574 236 566 222 Z" fill="#6e2420" />
      </g>
      <g {...o('j-temizlik')}>
        <path className="cz" pathLength={1} d="M566 250 c-20 0 -30 -30 -10 -50 c40 -40 -60 -80 -120 -40 c-80 50 -60 200 30 210 c80 10 130 -40 120 -110" stroke="#2e9e5b" strokeWidth={4} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('j-siringa')} filter={u('golge')}>
        <path d="M566 250 L600 244 L600 256 Z" fill="#9aa6b4" />
        <rect x={600} y={232} width={150} height={36} rx={6} fill={u('plastik')} stroke="#6b7a90" strokeWidth={2} />
        <rect x={606} y={238} width={110} height={24} fill="#cfe6ff" opacity={0.9} />
        <rect x={750} y={226} width={14} height={48} rx={3} fill="#6b7a90" />
        <text x={660} y={254} fontSize={11} textAnchor="middle" fill="#2f4f6f">lidokain jel</text>
      </g>
      <g {...o('j-parmak')} filter={u('golge')}>
        <path d="M300 60 C340 40 400 60 420 110 C430 140 400 160 370 150 C340 140 320 120 300 110 Z" fill={u('eldiven')} stroke="#7d8aa0" strokeWidth={2} />
        <path d="M300 440 C340 460 400 440 420 390 C430 360 400 340 370 350 C340 360 320 380 300 390 Z" fill={u('eldiven')} stroke="#7d8aa0" strokeWidth={2} />
      </g>
    </>
  ),
};

const FoleyKesit: Sahne = {
  ad: 'Kateter kesiti ve French ölçüsü',
  gizli: [],
  etiket: {
    'c-drenaj-lumen': [200, 470, 'Drenaj lümeni (geniş)'],
    'c-balon-lumen': [200, 40, 'Balon lümeni (ince)'],
    'c-olcek-eriskin': [580, 60, 'Erişkin: 12–24 Fr, boy sabit'],
    'c-olcek-cocuk': [580, 330, 'Çocuk: 6–8–10 Fr, daha kısa'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={u('zemin-klinik')} />
      <g filter={u('golge')}>
        <circle cx={200} cy={250} r={170} fill={u('lateks')} stroke="#a37a20" strokeWidth={3} />
        <circle cx={200} cy={250} r={150} fill="#f2d27a" opacity={0.5} />
      </g>
      <g {...o('c-drenaj-lumen')}><circle className="boya" cx={190} cy={275} r={105} fill="#fbf7ea" stroke="#a37a20" strokeWidth={3} /></g>
      <g {...o('c-balon-lumen')}><circle className="boya" cx={240} cy={118} r={22} fill="#dbe9fa" stroke="#2f6fd6" strokeWidth={3} /></g>
      <text x={200} y={290} textAnchor="middle" fontSize={14} fill="#7a5a16">idrar</text>
      <g {...o('c-olcek-eriskin')}>
        {[12, 14, 16, 18, 20, 22, 24].map((f, i) => (
          <g key={f}>
            <circle className="boya" cx={440 + i * 50} cy={150} r={f * 0.9} fill={u('silikon')} stroke="#8a96a6" />
            <text x={440 + i * 50} y={200} fontSize={12} textAnchor="middle" fill="#3e4a58">{f}</text>
          </g>
        ))}
        <path d="M420 230 L780 230" stroke="#9aa6b4" strokeWidth={2} />
        <text x={600} y={252} fontSize={12} textAnchor="middle" fill="#5b6676">1 Fr = 1/3 mm dış çap</text>
      </g>
      <g {...o('c-olcek-cocuk')}>
        {[6, 8, 10].map((f, i) => (
          <g key={f}>
            <circle className="boya" cx={500 + i * 60} cy={400} r={f * 0.9} fill={u('silikon')} stroke="#8a96a6" />
            <text x={500 + i * 60} y={440} fontSize={12} textAnchor="middle" fill="#3e4a58">{f}</text>
          </g>
        ))}
      </g>
    </>
  ),
};

export const SAHNELER: Record<string, Sahne> = {
  foley: Foley, mesane: Mesane, erkek: Erkek, travma: Travma, malzeme: Malzeme, pozisyon: Pozisyon, kadin: Kadin,
  'yakin-mesane': YakinMesane, 'yakin-uretra': YakinUretra, 'yakin-kadin': YakinKadin, 'yakin-el': YakinEl,
  'yakin-erkek-jel': YakinErkekJel, 'foley-kesit': FoleyKesit, maket: Maket,
};

/** Bir sahnedeki tüm öge kimlikleri (doğrulayıcı ve hotspot için) */
export const SAHNE_OGELERI: Record<string, string[]> = {
  foley: ['f-govde', 'f-uc', 'f-delik', 'f-balon-sonuk', 'f-balon', 'f-drenaj', 'f-balon-kanal', 'f-enjektor', 'f-torba', 'f-musluk', 'f-torba-bag'],
  mesane: ['g-sisme', 'g-mesane-normal', 'g-mesane-dolu', 'g-kucuk', 'g-akis', 'g-torba', 'g-kultur', 'g-ilac', 'g-el', 'g-us', 'g-us-dalga'],
  erkek: ['e-mesane', 'e-prostat', 'e-sfinkter', 'e-uretra', 'e-penil', 'e-glans', 'e-meatus', 'e-testis', 'e-jel', 'e-kateter', 'e-kivrim', 'e-balon-dogru', 'e-balon-yanlis', 'e-enjektor'],
  travma: ['t-pelvis', 't-simfiz', 't-kirik', 't-uretra', 't-yirtik', 't-kan'],
  malzeme: ['m-steril-alan', ...MALZEMELER.map((m) => m[0])],
  pozisyon: ['p-erkek', 'p-kadin', 'p-v', 'p-hekim', 'p-paravan', 'p-yardimci'],
  kadin: ['k-majus', 'k-minus', 'k-klitoris', 'k-meatus', 'k-vajina', 'k-temizlik', 'k-ortu', 'k-halka', 'k-kateter', 'k-idrar'],
  'yakin-mesane': ['y-duvar', 'y-trigon', 'y-ureter', 'y-boyun', 'y-prostat', 'y-kateter', 'y-delik', 'y-balon-sonuk', 'y-balon', 'y-idrar', 'y-cekme'],
  'yakin-uretra': ['z-spongiozum', 'z-mukoza', 'z-sfinkter', 'z-dogru', 'z-kivrim', 'z-balon', 'z-yirtik', 'z-kan', 'z-sivi'],
  'yakin-kadin': ['v-minus', 'v-klitoris', 'v-meatus', 'v-vajina', 'v-parmak', 'v-kateter', 'v-jel', 'v-idrar'],
  'yakin-el': ['h-halka', 'h-el', 'h-uc', 'h-jel', 'h-yanlis'],
  'yakin-erkek-jel': ['j-prepisyum', 'j-glans', 'j-dolum', 'j-meatus', 'j-temizlik', 'j-siringa', 'j-parmak'],
  maket: ['mk-govde', 'mk-hazne', 'mk-hazne-dolu', 'mk-kadin', 'mk-erkek'],
  'foley-kesit': ['c-drenaj-lumen', 'c-balon-lumen', 'c-olcek-eriskin', 'c-olcek-cocuk'],
};

export function SahneCiz({ sahne, durum, onSec, secilebilir, isaret }: {
  sahne: string;
  durum: SahneDurum;
  onSec?: (id: string) => void;
  secilebilir?: boolean;
  isaret?: { id: string; dogru: boolean } | null;
}) {
  const S = SAHNELER[sahne];
  if (!S) return null;
  const gizli = new Set(S.gizli);
  const o: OgeProps = (id) => {
    const d = durum[id] || {};
    const gor = d.gor ?? (d.ciz ? true : !gizli.has(id));
    const cls = ['kmb-oge'];
    if (!gor) cls.push('kmb-gizli');
    // sayaç teki/çifti ayrı animasyon adı: aynı eylem yeniden gelince animasyon baştan oynar (yeniden bağlamadan)
    if (d.vurgu) cls.push(d.vurgu % 2 ? 'kmb-vurgu-a' : 'kmb-vurgu-b');
    if (d.ciz) cls.push(d.ciz % 2 ? 'kmb-ciz-a' : 'kmb-ciz-b');
    if (secilebilir) cls.push('kmb-secilebilir');
    if (isaret?.id === id) cls.push(isaret.dogru ? 'kmb-isaret-dogru' : 'kmb-isaret-yanlis');
    return {
      'data-id': id,
      'data-renk': d.renk || undefined,
      className: cls.join(' '),
    };
  };
  const tikla = (e: React.MouseEvent) => {
    if (!onSec) return;
    let el = e.target as Element | null;
    while (el && el !== e.currentTarget) {
      const id = el.getAttribute('data-id');
      if (id && !el.classList.contains('kmb-gizli')) { onSec(id); return; }
      el = el.parentElement;
    }
  };
  return (
    <svg viewBox="0 0 800 500" className="kmb-sahne" role="img" aria-label={S.ad} onClick={tikla}>
      <Ortak />
      <S.Ciz o={o} />
      {Object.entries(S.etiket).map(([id, [x, y, metin]]) => durum[id]?.etiket ? (
        <g key={`e-${id}`} className="kmb-etiket">
          <rect x={x - metin.length * 4.6 - 10} y={y - 17} width={metin.length * 9.2 + 20} height={28} rx={14} />
          <text x={x} y={y + 3} textAnchor="middle">{metin}</text>
        </g>
      ) : null)}
    </svg>
  );
}
