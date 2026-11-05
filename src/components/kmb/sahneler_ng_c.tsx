/** KMB 01 Nazogastrik sonda 2B sahneleri — grup C: ng-malzeme (tepsi), ng-pozisyon (yan görünüm) (docs/KMB_2B_STIL.md).
 *  Öge kimlikleri sahneler.tsx SAHNE_OGELERI ile birebir. H462: nesneler iç içe geçmez, tepside ayrık yerleşim,
 *  el = avuç + 4 parmak + başparmak, parmak ucu dokuya değer (uç = temas − yarı kalınlık), kadraj kesmez. */
import React from 'react';
import { type Sahne, u } from './sahneOrtak';

void React;

type Pt = [number, number];
const YAZI = '#3e4a58';
const P_KOYU = '#6b7a90';
const PVC_K = '#8a96a6';
const PVC = '#eef3f8';
const DERI = 'url(#kmb-2b-deri)', TEN = '#f0bf9a', KONTUR_DERI = '#b9805a';
const ELD = '#9cc3e6', ELD_K = '#3f6f9c';

/** Şeffaf PVC tüp: koyu kontur + açık iç (silindir). */
const Tup = ({ d, w = 7, dis = PVC_K, ic = PVC, cls = 'boya-cizgi' }: { d: string; w?: number; dis?: string; ic?: string; cls?: string }) => (
  <>
    <path d={d} stroke={dis} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    <path className={cls} d={d} stroke={ic} strokeWidth={w - 3} fill="none" strokeLinecap="round" strokeLinejoin="round" />
  </>
);

/** Kalın çizgi uzuv (kol/bacak): kontur + düz dolgu. */
const Uzuv = ({ pts, w, dolgu, kontur, cls }: { pts: Pt[]; w: number; dolgu: string; kontur: string; cls?: string }) => {
  const d = pts.map((p, i) => `${i ? 'L' : 'M'}${p[0]} ${p[1]}`).join(' ');
  return (
    <>
      <path d={d} stroke={kontur} strokeWidth={w + 4} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path className={cls} d={d} stroke={dolgu} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </>
  );
};

/** El (yerel: bilek (0,0), parmaklar +x yönünde, başparmak −y tarafında): avuç + 4 parmak + başparmak. */
const El = ({ x, y, aci = 0, s = 1, dolgu = TEN, kontur = KONTUR_DERI, kivrik = false }: { x: number; y: number; aci?: number; s?: number; dolgu?: string; kontur?: string; kivrik?: boolean }) => (
  <g transform={`translate(${x} ${y}) rotate(${aci}) scale(${s})`}>
    {[-4.8, -1.6, 1.6, 4.8].map((py, i) => {
      const L = [10, 11.5, 11, 9][i];
      const d = kivrik ? `M14 ${py} L${14 + L * 0.6} ${py} L${14 + L * 0.6} ${py + 5}` : `M14 ${py} L${14 + L} ${py}`;
      return (
        <g key={i}>
          <path d={d} stroke={kontur} strokeWidth={4.6} fill="none" strokeLinecap="round" strokeLinejoin="round" />
          <path d={d} stroke={dolgu} strokeWidth={2.8} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        </g>
      );
    })}
    <ellipse className="boya" cx={8} cy={0} rx={9} ry={7.5} fill={dolgu} stroke={kontur} strokeWidth={1.6} />
    <path d="M5 -5 L13 -10" stroke={kontur} strokeWidth={5} strokeLinecap="round" />
    <path d="M5 -5 L13 -10" stroke={dolgu} strokeWidth={3.2} strokeLinecap="round" />
  </g>
);

/** Enjektör (yerel: hazne x 0 → L, y −H/2 → H/2; uç sağda). `can`: geniş konik kateter (çan) ucu; aksi luer küçük uç. */
const Enjektor = ({ L, H, piston, can, yazi }: { L: number; H: number; piston: number; can: boolean; yazi?: string }) => (
  <g>
    <path d={`M${-piston} 0 L4 0`} stroke={P_KOYU} strokeWidth={Math.max(5, H * 0.34)} strokeLinecap="round" />
    <path d={`M${-piston + 1} 0 L4 0`} stroke="#dfe6ee" strokeWidth={Math.max(2.5, H * 0.34 - 3)} strokeLinecap="round" />
    <rect x={-piston - 5} y={-H / 2 - 3} width={6} height={H + 6} rx={2.5} fill="#c9d3de" stroke={P_KOYU} strokeWidth={2} />
    <rect className="boya" x={0} y={-H / 2} width={L} height={H} rx={3} fill="#f4f8fc" stroke={P_KOYU} strokeWidth={2} />
    <rect x={-3} y={-H / 2 - 6} width={6} height={H + 12} rx={2} fill="#c9d3de" stroke={P_KOYU} strokeWidth={2} />
    <rect x={7} y={-H / 2 + 2.5} width={Math.max(4, H * 0.25)} height={H - 5} rx={1.5} fill="#2b3340" />
    {Array.from({ length: 9 }, (_, i) => <path key={i} d={`M${18 + i * (L - 26) / 8} ${-H / 2} l0 ${i % 2 ? H * 0.2 : H * 0.34}`} stroke={YAZI} strokeWidth={1} />)}
    {yazi && <text x={L - 6} y={H / 2 - 5} fontSize={10} textAnchor="end" fill={YAZI} fontWeight={600}>{yazi}</text>}
    {can
      ? <path className="boya" d={`M${L} ${-H * 0.32} L${L + 42} ${-H * 0.13} L${L + 42} ${H * 0.13} L${L} ${H * 0.32} Z`} fill="#f4f8fc" stroke={P_KOYU} strokeWidth={2} strokeLinejoin="round" />
      : <><path d={`M${L} ${-H * 0.22} L${L + 5} ${-H * 0.16} L${L + 5} ${H * 0.16} L${L} ${H * 0.22} Z`} fill="#c9d3de" stroke={P_KOYU} strokeWidth={1.5} strokeLinejoin="round" />
        <rect x={L + 5} y={-1.8} width={7} height={3.6} rx={1} fill="#c9d3de" stroke={P_KOYU} strokeWidth={1.2} /></>}
  </g>
);

/** Eldiven (yerel: üst-orta, parmaklar yukarı; ayna = −1). */
const Eldiven = ({ x, y, ayna = 1 }: { x: number; y: number; ayna?: number }) => (
  <g transform={`translate(${x} ${y}) scale(${ayna} 1)`}>
    {[[-10, 8, 2], [-3.5, 4, 0], [3, 5, 1], [9.5, 12, 3]].map(([px, ty], i) => (
      <g key={i}>
        <path d={`M${px} 30 L${px} ${ty}`} stroke={ELD_K} strokeWidth={9} strokeLinecap="round" />
        <path d={`M${px} 30 L${px} ${ty}`} stroke={ELD} strokeWidth={6} strokeLinecap="round" />
      </g>
    ))}
    <path d="M-12 48 L-25 30" stroke={ELD_K} strokeWidth={10} strokeLinecap="round" />
    <path d="M-12 48 L-25 30" stroke={ELD} strokeWidth={7} strokeLinecap="round" />
    <path className="boya" d="M-15 24 L15 24 L15 62 C15 68 -15 68 -15 62 Z" fill={u('2b-eldiven')} stroke={ELD_K} strokeWidth={2} strokeLinejoin="round" />
    <path d="M-13 66 L13 66 L14 84 L-14 84 Z" fill={ELD} stroke={ELD_K} strokeWidth={2} strokeLinejoin="round" />
  </g>
);

// ————————————————————————————————————————————————————— NG MALZEME (tepsi)

/** Tüp üstünde dik uzunluk işareti (yol eğimine dik kısa çizgi). */
const isaret = (cx: number, cy: number, r: number, aci: number, n: number) => Array.from({ length: n }, (_, i) => {
  const t = (aci + (i - (n - 1) / 2) * 3.2) * Math.PI / 180;
  const x1 = cx + (r - 4) * Math.cos(t), y1 = cy + (r - 4) * Math.sin(t) * 0.86;
  const x2 = cx + (r + 4) * Math.cos(t), y2 = cy + (r + 4) * Math.sin(t) * 0.86;
  return <path key={`${aci}-${i}`} d={`M${x1} ${y1} L${x2} ${y2}`} stroke="#2b3340" strokeWidth={1.4} />;
});

const NgMalzeme: Sahne = {
  ad: 'Nazogastrik sonda malzemeleri',
  gizli: [],
  etiket: {
    'nm-sonda': [110, 166, 'NG sonda'],
    'nm-kalinlik': [330, 166, 'Kalınlık: renkli uç'],
    'nm-beslenme': [630, 166, 'Beslenme sondası + tel'],
    'nm-enjektor-can': [150, 290, 'Çan uçlu 50 mL enjektör'],
    'nm-enjektor-normal': [338, 290, 'Luer enjektör'],
    'nm-jel': [480, 290, 'Su bazlı jel'],
    'nm-vazelin': [600, 290, 'Vazelin'],
    'nm-su': [712, 290, 'Su bardağı'],
    'nm-stetoskop': [80, 460, 'Stetoskop'],
    'nm-flaster': [205, 460, 'Flaster'],
    'nm-eldiven': [320, 460, 'Eldiven'],
    'nm-ortu': [430, 460, 'Emici örtü'],
    'nm-poset': [555, 460, 'Kusma poşeti'],
    'nm-torba': [705, 460, 'Drenaj torbası'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* paslanmaz tepsi */}
      <rect x={14} y={30} width={772} height={456} rx={18} fill={u('2b-metal')} opacity={0.18} stroke="#5b6676" strokeWidth={3} />
      <rect x={26} y={42} width={748} height={432} rx={12} fill="#f3f6f9" stroke="#9aa6b4" strokeWidth={1.5} />

      <g {...o('nm-sonda')}>
        {/* kıvrılmış sonda: iki halka, yan delikli uç sol-altta, renkli bağlantı ucu sağ-üstte */}
        <Tup d="M60 140 C42 130 46 96 66 82 C92 64 140 66 152 92 C164 120 136 146 104 144 C78 142 70 116 84 102 C98 88 128 90 132 108 C135 122 118 130 106 124" w={7} />
        <Tup d="M60 140 C52 146 46 150 42 150" w={7} />
        <circle cx={41} cy={150} r={3.4} fill={PVC} stroke={PVC_K} strokeWidth={1.6} />
        <ellipse cx={52} cy={146} rx={2.2} ry={1.4} fill="#5b6676" />
        <path d="M142 74 C150 68 156 64 162 60" stroke={PVC_K} strokeWidth={7} fill="none" strokeLinecap="round" />
        <path d="M142 74 C150 68 156 64 162 60" stroke={PVC} strokeWidth={4} fill="none" strokeLinecap="round" />
        <path className="boya" d="M160 62 L176 50 L184 60 L166 70 Z" fill="#2e9e5b" stroke="#1f6b3e" strokeWidth={2} strokeLinejoin="round" />
        {isaret(100, 104, 50, 200, 1)}{isaret(100, 104, 50, 260, 2)}{isaret(100, 104, 50, 320, 3)}
      </g>

      <g {...o('nm-kalinlik')}>
        {([[78, 7, '#2e9e5b', '#1f6b3e'], [104, 9, '#f08a24', '#a85a10'], [130, 11, '#d23b3b', '#8d1f1f']] as const).map(([y, w, r, rk]) => (
          <g key={y}>
            <Tup d={`M220 ${y} L440 ${y}`} w={w} />
            <circle cx={220} cy={y} r={w / 2} fill={PVC} stroke={PVC_K} strokeWidth={1.5} />
            <ellipse cx={232} cy={y} rx={2.6} ry={w / 4} fill="#5b6676" />
            <ellipse cx={248} cy={y} rx={2.6} ry={w / 4} fill="#5b6676" />
            {[300, 340, 380].map((x, k) => Array.from({ length: k + 1 }, (_, j) => <path key={`${x}${j}`} d={`M${x + j * 4} ${y - w / 2} l0 ${w}`} stroke="#2b3340" strokeWidth={1.3} />))}
            <path className="boya" d={`M438 ${y - w / 2} L466 ${y - w / 2 - 4} L466 ${y + w / 2 + 4} L438 ${y + w / 2} Z`} fill={r} stroke={rk} strokeWidth={2} strokeLinejoin="round" />
          </g>
        ))}
        <text x={300} y={70} fontSize={8} fill={YAZI} textAnchor="middle">50</text>
        <text x={344} y={70} fontSize={8} fill={YAZI} textAnchor="middle">60</text>
      </g>

      <g {...o('nm-beslenme')}>
        <path d="M520 112 C560 90 600 128 640 106 C672 90 700 100 724 102" stroke={PVC_K} strokeWidth={5} fill="none" strokeLinecap="round" />
        <path className="boya-cizgi" d="M520 112 C560 90 600 128 640 106 C672 90 700 100 724 102" stroke="#fbfdff" strokeWidth={2.6} fill="none" strokeLinecap="round" />
        {/* kılavuz tel: sondanın içinde, ucu bağlantıdan dışarı */}
        <path d="M524 110 C560 90 600 128 640 106 C672 90 700 100 768 102" stroke="#5b6676" strokeWidth={1.1} fill="none" />
        <ellipse className="boya" cx={516} cy={113} rx={7} ry={4} fill="#d6dde6" stroke={PVC_K} strokeWidth={1.6} transform="rotate(-25 516 113)" />
        <path d="M722 96 L744 94 L744 110 L722 108 Z" fill="#8e5bb5" stroke="#5c3a7a" strokeWidth={2} strokeLinejoin="round" />
        <circle cx={772} cy={102} r={4.5} fill="#dfe6ee" stroke="#5b6676" strokeWidth={1.6} />
      </g>

      <g {...o('nm-enjektor-can')}>
        <g transform="translate(86 240)"><Enjektor L={124} H={34} piston={34} can yazi="50 mL" /></g>
      </g>
      <g {...o('nm-enjektor-normal')}>
        <g transform="translate(302 240)"><Enjektor L={54} H={14} piston={18} can={false} /></g>
      </g>

      <g {...o('nm-jel')}>
        <rect x={430} y={226} width={9} height={28} rx={1.5} fill="#d6dde6" stroke={P_KOYU} strokeWidth={2} />
        {[232, 238, 244].map((y) => <path key={y} d={`M431 ${y + 4} L438 ${y + 4}`} stroke={P_KOYU} strokeWidth={1} />)}
        <path className="boya" d="M439 228 L510 230 L520 235 L520 245 L510 250 L439 252 Z" fill="#ffffff" stroke={P_KOYU} strokeWidth={2} strokeLinejoin="round" />
        <path d="M452 229 L452 251 M470 229.5 L470 250.5" stroke="#2f7fc8" strokeWidth={3} />
        <text x={490} y={244} fontSize={9} fill="#2f7fc8" fontWeight={700} textAnchor="middle">JEL</text>
        <rect x={520} y={233} width={16} height={14} rx={2} fill="#2f7fc8" stroke="#1f4e79" strokeWidth={2} />
      </g>

      <g {...o('nm-vazelin')}>
        <rect className="boya" x={572} y={228} width={56} height={44} rx={7} fill="#f3e3a0" stroke="#a88d3a" strokeWidth={2} />
        <rect x={570} y={214} width={60} height={14} rx={3} fill="#e8ecf0" stroke="#5b6676" strokeWidth={2} />
        <rect x={578} y={240} width={44} height={18} rx={2} fill="#ffffff" stroke="#a88d3a" strokeWidth={1} />
        <text x={600} y={252} fontSize={8} fill={YAZI} textAnchor="middle" fontWeight={600}>Vazelin</text>
      </g>

      <g {...o('nm-su')}>
        <path d="M694 226 L730 226 L726 270 L698 270 Z" fill="#bfe0f5" opacity={0.75} />
        <path className="boya" d="M690 204 L734 204 L728 272 L696 272 Z" fill="#eaf4fb" fillOpacity={0.35} stroke="#7d9ab5" strokeWidth={2} strokeLinejoin="round" />
        <path d="M694 226 L730 226" stroke="#5c9ccc" strokeWidth={1.5} />
        <path d="M697 210 L701 264" stroke="#fff" strokeWidth={2} strokeLinecap="round" />
      </g>

      <g {...o('nm-stetoskop')}>
        <path d="M58 338 C56 360 66 372 80 378 M102 338 C104 360 94 372 80 378" stroke="#5b6676" strokeWidth={4} fill="none" strokeLinecap="round" />
        <circle cx={58} cy={336} r={4} fill="#2b3340" /><circle cx={102} cy={336} r={4} fill="#2b3340" />
        <path className="boya-cizgi" d="M80 378 C80 410 60 420 70 434 C80 446 106 440 108 424" stroke="#2b3340" strokeWidth={5} fill="none" strokeLinecap="round" />
        <circle className="boya" cx={112} cy={412} r={13} fill={u('2b-metal')} stroke="#3e4a58" strokeWidth={2} />
        <circle cx={112} cy={412} r={7} fill="#dfe6ee" stroke="#5b6676" strokeWidth={1.5} />
      </g>

      <g {...o('nm-flaster')}>
        <circle className="boya" cx={200} cy={372} r={28} fill="#f4efe6" stroke="#9a8f7c" strokeWidth={2.5} />
        <circle cx={200} cy={372} r={20} fill="none" stroke="#d8cdb8" strokeWidth={1.5} />
        <circle cx={200} cy={372} r={12} fill="#ffffff" stroke="#9a8f7c" strokeWidth={2} />
        <rect x={168} y={414} width={78} height={9} rx={1.5} fill="#f4efe6" stroke="#9a8f7c" strokeWidth={1.8} transform="rotate(-4 207 418)" />
      </g>

      <g {...o('nm-eldiven')}>
        <Eldiven x={302} y={340} />
        <Eldiven x={346} y={340} ayna={-1} />
      </g>

      <g {...o('nm-ortu')}>
        <rect x={392} y={398} width={84} height={26} rx={4} fill="#d9efe6" stroke="#2f6f5f" strokeWidth={2} />
        <rect x={388} y={372} width={84} height={26} rx={4} fill="#c3e4d6" stroke="#2f6f5f" strokeWidth={2} />
        <rect className="boya" x={384} y={346} width={84} height={26} rx={4} fill={u('2b-ortu')} fillOpacity={0.45} stroke="#2f6f5f" strokeWidth={2} />
        <path d="M392 354 L460 354" stroke="#ffffff" strokeWidth={1.5} opacity={0.8} />
      </g>

      <g {...o('nm-poset')}>
        <path className="boya" d="M528 352 C524 384 528 412 540 432 L572 432 C584 412 588 384 584 352 Z" fill="#cfe0f5" fillOpacity={0.8} stroke="#2f5f9c" strokeWidth={2} strokeLinejoin="round" />
        <ellipse cx={556} cy={350} rx={30} ry={7} fill="#ffffff" stroke="#2f5f9c" strokeWidth={3} />
        {[380, 400, 420].map((y) => <path key={y} d={`M560 ${y} L572 ${y}`} stroke="#2f5f9c" strokeWidth={1.2} />)}
      </g>

      <g {...o('nm-torba')}>
        <path d="M705 346 C705 330 690 326 682 334 C676 340 684 348 694 344" stroke={PVC_K} strokeWidth={6} fill="none" strokeLinecap="round" />
        <path d="M705 346 C705 330 690 326 682 334 C676 340 684 348 694 344" stroke={PVC} strokeWidth={3} fill="none" strokeLinecap="round" />
        <rect className="boya" x={660} y={346} width={90} height={84} rx={10} fill={u('2b-plastik')} fillOpacity={0.35} stroke={P_KOYU} strokeWidth={2.5} />
        {[364, 384, 404].map((y) => <path key={y} d={`M732 ${y} L744 ${y}`} stroke={YAZI} strokeWidth={1.4} />)}
        <path d="M700 430 L710 430 L708 440 L702 440 Z" fill="#c9d3de" stroke={P_KOYU} strokeWidth={1.8} strokeLinejoin="round" />
      </g>
    </>
  ),
};

// ————————————————————————————————————————————————————— NG POZİSYON (yan görünüm)
/* Hasta yüzü sola; yatak başı ~75° kalkık. Hekim hastanın SAĞ tarafında (görüntünün uzak yanı → yatağın baş ucunda,
   arkada); uzak kolu (np-el-bas) başın arkasına uzanır. Baş merkezi (456,166) r 26. */
const BX = 456, BY = 166, BR = 26;
const kafa = (aDer: number, pay: number): Pt => { const a = aDer * Math.PI / 180; return [BX + (BR + pay) * Math.cos(a), BY + (BR + pay) * Math.sin(a)]; };

const Lavabo = () => (
  <g>
    <rect x={34} y={150} width={70} height={56} rx={6} fill="#eef5fb" stroke="#7d8aa0" strokeWidth={2} />
    <path d="M66 236 L66 222 C66 214 80 214 80 222" stroke="#5b6676" strokeWidth={5} fill="none" strokeLinecap="round" />
    <path className="boya" d="M24 236 L116 236 L110 262 C106 272 34 272 30 262 Z" fill="#ffffff" stroke="#5b6676" strokeWidth={2.5} strokeLinejoin="round" />
    <path d="M58 270 L82 270 L76 450 L64 450 Z" fill="#ffffff" stroke="#5b6676" strokeWidth={2.5} strokeLinejoin="round" />
  </g>
);

const NgPozisyon: Sahne = {
  ad: 'Nazogastrik sonda: hasta pozisyonu (yandan)',
  gizli: ['np-ortu', 'np-poset', 'np-eldiven', 'np-el-bas', 'np-ok-egim', 'np-sonda', 'np-yardimci'],
  etiket: {
    'np-hasta': [210, 70, 'Hasta dik oturur'],
    'np-ok-egim': [300, 116, 'Çene göğse eğik'],
    'np-ortu': [250, 160, 'Emici örtü göğüste'],
    'np-sonda': [320, 204, 'Sonda buruna bantlı'],
    'np-poset': [330, 250, 'Kusma poşeti'],
    'np-el-bas': [476, 96, 'El başın arkasında'],
    'np-hekim': [610, 46, 'Hekim hastanın sağında'],
    'np-eldiven': [560, 296, 'Eldiven'],
    'np-yatak': [300, 420, 'Yatak başı 45–90°'],
    'np-lavabo': [70, 128, 'Lavabo'],
    'np-yardimci': [705, 474, 'Yardımcı personel'],
  },
  Ciz: ({ o }) => {
    const ucler: Pt[] = [kafa(-62, 2.6), kafa(-48, 2.6), kafa(-34, 2.6), kafa(-20, 2.6)];
    const kok: Pt[] = [[497, 150], [500, 156], [502, 162], [503, 168]];
    return (
      <>
        <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
        <path d="M0 452 L800 452" stroke="#c9d3de" strokeWidth={2} />
        <g {...o('np-lavabo')}><Lavabo /></g>

        {/* hekim (uzak tarafta, yatak başında): yüzü sola */}
        <g {...o('np-hekim')}>
          <path d="M580 300 L594 300 L592 444 L578 444 Z M600 300 L614 300 L614 444 L600 444 Z" fill="#4a5566" stroke="#2f3744" strokeWidth={2} strokeLinejoin="round" />
          <path d="M570 444 L594 444 L594 452 L566 452 Z M596 444 L620 444 L620 452 L592 452 Z" fill="#2b3340" />
          <path className="boya" d="M576 150 C580 140 612 140 616 150 L624 306 L570 306 Z" fill="#ffffff" stroke="#7d8aa0" strokeWidth={2.5} strokeLinejoin="round" />
          <rect x={589} y={132} width={14} height={14} fill={TEN} stroke={KONTUR_DERI} strokeWidth={2} />
          <circle cx={596} cy={118} r={24} fill={DERI} stroke={KONTUR_DERI} strokeWidth={2.5} />
          <path d="M573 112 L566 122 L574 126" fill={TEN} stroke={KONTUR_DERI} strokeWidth={2} strokeLinejoin="round" />
          <path d="M574 106 C576 90 616 86 620 112 C616 106 610 104 604 104 C592 100 582 102 574 106 Z" fill="#3b2a1e" />
          <circle cx={582} cy={112} r={2} fill="#2b3340" />
          <circle cx={604} cy={120} r={4} fill={TEN} stroke={KONTUR_DERI} strokeWidth={1.5} />
          {/* yakın kol: dirsek bükük, el önde */}
          <Uzuv pts={[[594, 160], [588, 228], [568, 250]]} w={16} dolgu="#ffffff" kontur="#7d8aa0" />
          <El x={566} y={252} aci={160} s={1.1} kivrik />
        </g>

        {/* yatak: arka dayanak (sırt) önce, döşek, şasi */}
        <g {...o('np-yatak')}>
          <path className="boya" d="M480 344 L498 204 L518 207 L512 344 Z" fill={u('2b-yatak')} stroke="#4f9aa0" strokeWidth={2.5} strokeLinejoin="round" />
          <rect className="boya" x={130} y={340} width={384} height={28} rx={8} fill={u('2b-yatak')} stroke="#4f9aa0" strokeWidth={2.5} />
          <rect x={126} y={368} width={402} height={12} rx={3} fill="#c9d3de" stroke="#5b6676" strokeWidth={2} />
          {[150, 500].map((x) => <g key={x}><rect x={x - 4} y={380} width={8} height={54} fill="#9aa6b4" stroke="#5b6676" strokeWidth={1.5} /><circle cx={x} cy={442} r={9} fill="#3e4a58" /></g>)}
          <path d="M520 300 A84 84 0 0 0 504 262" stroke="#4f9aa0" strokeWidth={1.5} fill="none" strokeDasharray="4 3" />
        </g>

        <g {...o('np-poset')}>
          <path className="boya" d="M396 258 C392 274 396 288 404 296 L426 296 C432 288 436 274 432 258 Z" fill="#cfe0f5" fillOpacity={0.85} stroke="#2f5f9c" strokeWidth={2} strokeLinejoin="round" />
          <ellipse cx={414} cy={257} rx={19} ry={4.5} fill="#ffffff" stroke="#2f5f9c" strokeWidth={2.5} />
        </g>

        <g {...o('np-hasta')}>
          {/* bacaklar (döşek üstünde uzanır) */}
          <Uzuv pts={[[462, 322], [312, 314]]} w={34} dolgu="#7fb3c0" kontur="#3f7680" />
          <Uzuv pts={[[312, 316], [180, 326]]} w={26} dolgu="#7fb3c0" kontur="#3f7680" />
          <path d="M178 312 C170 300 160 300 158 310 L158 336 L180 338 Z" fill={TEN} stroke={KONTUR_DERI} strokeWidth={2} strokeLinejoin="round" />
          {/* gövde (önlük) — sırt dayanağa yaslı */}
          <path className="boya" d="M448 196 C436 214 434 250 434 290 C434 312 444 332 466 340 L480 340 L496 210 C484 198 462 192 448 196 Z" fill="url(#kmb-2b-onluk)" stroke="#3f7680" strokeWidth={2.5} strokeLinejoin="round" />
          {/* boyun + baş (hafif öne eğik) */}
          <path d="M452 184 L472 186 L476 204 L454 204 Z" fill={TEN} stroke={KONTUR_DERI} strokeWidth={2} strokeLinejoin="round" />
          <circle cx={BX} cy={BY} r={BR} fill={DERI} stroke={KONTUR_DERI} strokeWidth={2.5} />
          <path d="M434 154 L421 173 L431 178" fill={TEN} stroke={KONTUR_DERI} strokeWidth={2} strokeLinejoin="round" />
          <ellipse cx={425} cy={176} rx={2.4} ry={1.4} fill="#7a4a30" />
          <path d="M434 186 C438 188 442 188 444 186" stroke="#8d4a3a" strokeWidth={1.8} fill="none" strokeLinecap="round" />
          <circle cx={440} cy={158} r={2.2} fill="#2b3340" />
          <path d="M436 150 L444 148" stroke="#3b2a1e" strokeWidth={1.8} strokeLinecap="round" />
          <path d="M434 146 C438 128 476 128 482 160 C482 172 478 180 474 184 C474 170 470 156 456 150 C448 146 440 146 434 146 Z" fill="#3b2a1e" />
          <ellipse cx={464} cy={168} rx={4.5} ry={6} fill={TEN} stroke={KONTUR_DERI} strokeWidth={1.5} />
          {/* yakın kol: üst kol gövde boyunca, ön kol öne; el poşeti tutar */}
          <Uzuv pts={[[474, 216], [472, 280], [432, 266]]} w={15} dolgu="#7fb3c0" kontur="#3f7680" />
          <El x={430} y={262} aci={200} s={0.95} kivrik />
        </g>

        <g {...o('np-ortu')}>
          {/* göğse yemek peçetesi gibi: boyundan ön kola kadar + ön kolun altından kucağa */}
          <path className="boya" d="M446 200 L470 204 L468 250 L440 254 C436 236 438 214 446 200 Z" fill={u('2b-ortu')} fillOpacity={0.55} stroke="#2f6f5f" strokeWidth={2} strokeLinejoin="round" />
          <path d="M438 284 L464 286 L462 318 L444 322 C438 308 436 296 438 284 Z" fill={u('2b-ortu')} fillOpacity={0.55} stroke="#2f6f5f" strokeWidth={2} strokeLinejoin="round" />
        </g>

        <g {...o('np-sonda')}>
          <Tup d="M425 178 C420 190 424 200 434 210 C444 220 452 230 450 244" w={6} />
          <path d="M445 244 L455 244 L454 252 L446 252 Z" fill="#2e9e5b" stroke="#1f6b3e" strokeWidth={1.6} strokeLinejoin="round" />
          {/* burun sırtında bant */}
          <path className="boya" d="M431 157 L437 160 L428 176 L422 173 Z" fill="#f4efe6" stroke="#9a8f7c" strokeWidth={1.6} strokeLinejoin="round" />
        </g>

        <g {...o('np-ok-egim')}>
          <path className="cz boya-cizgi" pathLength={1} d="M412 128 C390 148 392 186 418 206" stroke="#2f6fd6" strokeWidth={3} fill="none" strokeLinecap="round" markerEnd="url(#kmb-ok)" />
        </g>

        {/* uzak kol: hekimin omzundan başın arkasına; eldivenli avuç + 4 parmak başın arka kavsine değer */}
        <g {...o('np-el-bas')}>
          <Uzuv pts={[[606, 158], [556, 172], [510, 164]]} w={15} dolgu="#ffffff" kontur="#7d8aa0" />
          {ucler.map(([tx, ty], i) => (
            <g key={i}>
              <path d={`M${kok[i][0]} ${kok[i][1]} L${tx} ${ty}`} stroke={ELD_K} strokeWidth={5.2} strokeLinecap="round" />
              <path d={`M${kok[i][0]} ${kok[i][1]} L${tx} ${ty}`} stroke={ELD} strokeWidth={3.4} strokeLinecap="round" />
            </g>
          ))}
          <ellipse className="boya" cx={498} cy={164} rx={9} ry={12} fill={ELD} stroke={ELD_K} strokeWidth={1.8} />
          <path d={`M498 174 L${kafa(18, 2.6)[0]} ${kafa(18, 2.6)[1]}`} stroke={ELD_K} strokeWidth={5.6} strokeLinecap="round" />
          <path d={`M498 174 L${kafa(18, 2.6)[0]} ${kafa(18, 2.6)[1]}`} stroke={ELD} strokeWidth={3.8} strokeLinecap="round" />
        </g>

        <g {...o('np-eldiven')}>
          <El x={566} y={252} aci={160} s={1.1} kivrik dolgu={ELD} kontur={ELD_K} />
        </g>

        {/* yardımcı personel: hekimin arkasında, elinde çan uçlu enjektör */}
        <g {...o('np-yardimci')}>
          <path d="M690 300 L704 300 L702 444 L688 444 Z M710 300 L724 300 L724 444 L710 444 Z" fill="#4a5566" stroke="#2f3744" strokeWidth={2} strokeLinejoin="round" />
          <path d="M680 444 L704 444 L704 452 L676 452 Z M706 444 L730 444 L730 452 L702 452 Z" fill="#2b3340" />
          <path className="boya" d="M686 160 C690 150 722 150 726 160 L732 306 L680 306 Z" fill="url(#kmb-2b-onluk)" stroke="#3f7680" strokeWidth={2.5} strokeLinejoin="round" />
          <rect x={699} y={142} width={14} height={14} fill={TEN} stroke={KONTUR_DERI} strokeWidth={2} />
          <circle cx={706} cy={128} r={23} fill={DERI} stroke={KONTUR_DERI} strokeWidth={2.5} />
          <path d="M684 122 L677 131 L685 135" fill={TEN} stroke={KONTUR_DERI} strokeWidth={2} strokeLinejoin="round" />
          <path d="M684 118 C686 98 730 98 730 128 C730 140 726 150 722 152 C722 136 718 120 704 114 C696 112 690 114 684 118 Z" fill="#5a3a24" />
          <circle cx={692} cy={122} r={2} fill="#2b3340" />
          <g transform="translate(662 232) rotate(-90)"><Enjektor L={44} H={20} piston={14} can /></g>
          <Uzuv pts={[[704, 170], [698, 236], [676, 244]]} w={15} dolgu="#7fb3c0" kontur="#3f7680" />
          <El x={676} y={246} aci={200} s={0.95} kivrik />
        </g>
      </>
    );
  },
};

export const SAHNELER_NG_C: Record<string, Sahne> = { 'ng-malzeme': NgMalzeme, 'ng-pozisyon': NgPozisyon };
