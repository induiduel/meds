/**
 * KMB 2B düz çizgi film sahneleri — grup A: foley, foley-kesit, malzeme, maket (docs/KMB_2B_STIL.md).
 * Sahne anahtarları ve öge kimlikleri sahneler.tsx `SAHNE_OGELERI` ile birebir aynı; bu kayıt eskinin ÜSTÜNE serilir.
 * Dil: pürüzsüz iki duraklı degrade (`kmb-2b-*`, sahneOrtak.tsx), 2–3 px sıcak kontur, filtre/gölge/parıltı yok, beyaz zemin.
 * Sözleşme: her öge `<g {...o(id)}>` + en az bir `.boya`/`.boya-cizgi`; çizilebilir yol `cz` + pathLength=1; `gizli` eski semantik.
 */
import React from 'react';
import { type Sahne, u } from './sahneOrtak';

void React;

/* ——— ortak küçük parçalar ——— */
const K_KOYU = '#b47a1a';
const P_KOYU = '#6b7a90';
const YAZI = '#3e4a58';

/** İki çizgili silindir boru (kateter/hortum): koyu kontur + açık gövde (+ tek beyaz vurgu). `cz` açık çizgiye biner. */
const Tup = ({ d, w = 11, renk = u('2b-kateter'), kontur = K_KOYU, cz = false, cls = 'boya-cizgi', vurgu = true }: {
  d: string; w?: number; renk?: string; kontur?: string; cz?: boolean; cls?: string; vurgu?: boolean;
}) => (
  <>
    <path d={d} stroke={kontur} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    <path className={`${cz ? 'cz ' : ''}${cls}`} pathLength={cz ? 1 : undefined} d={d} stroke={renk} strokeWidth={w - 4} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    {vurgu && <path d={d} stroke="#fff" strokeOpacity={0.55} strokeWidth={Math.max(1.2, (w - 4) / 4)} fill="none" strokeLinecap="round" strokeLinejoin="round" transform={`translate(0 ${-(w - 4) / 4})`} />}
  </>
);

/** Enjektör: hazne (sol uç = piston tarafı, sağ uç = uç) — yerel eksende x: 0 → L, y: −H/2 → H/2. `kateterUcu`: 50 mL uzun konik uç. */
const Enjektor = ({ L = 90, H = 18, kateterUcu = false, piston = 28, yazi = '', yaziTers = false }: { L?: number; H?: number; kateterUcu?: boolean; piston?: number; yazi?: string; yaziTers?: boolean }) => (
  <g>
    {/* piston çubuğu + başlık (haznenin solunda) */}
    <path d={`M${-piston} 0 L4 0`} stroke={P_KOYU} strokeWidth={Math.max(6, H * 0.4)} strokeLinecap="round" />
    <path d={`M${-piston + 1} 0 L4 0`} stroke="#dfe6ee" strokeWidth={Math.max(3, H * 0.4 - 3)} strokeLinecap="round" />
    <rect x={-piston - 5} y={-H / 2 - 4} width={7} height={H + 8} rx={2.5} fill="#c9d3de" stroke={P_KOYU} strokeWidth={2} />
    {/* hazne */}
    <rect className="boya" x={0} y={-H / 2} width={L} height={H} rx={3} fill={u('2b-plastik')} stroke={P_KOYU} strokeWidth={2} />
    {/* parmak dayanağı */}
    <rect x={-3} y={-H / 2 - 6} width={6} height={H + 12} rx={2} fill="#c9d3de" stroke={P_KOYU} strokeWidth={2} />
    {/* piston lastiği */}
    <rect x={8} y={-H / 2 + 3} width={7} height={H - 6} rx={1.5} fill="#2b3340" />
    {/* derece çizgileri */}
    {Array.from({ length: 9 }, (_, i) => <path key={i} d={`M${20 + i * (L - 30) / 8} ${-H / 2} l0 ${i % 2 ? H * 0.22 : H * 0.36}`} stroke={YAZI} strokeWidth={1} />)}
    {yazi && <text x={L - 6} y={H / 2 - 4} fontSize={Math.min(9, H * 0.45)} textAnchor="end" fill={YAZI} fontWeight={600} transform={yaziTers ? `rotate(180 ${L - 24} ${H / 2 - 7})` : undefined}>{yazi}</text>}
    {/* uç */}
    {kateterUcu
      ? <path d={`M${L} ${-H * 0.28} L${L + 30} ${-H * 0.1} L${L + 30} ${H * 0.1} L${L} ${H * 0.28} Z`} fill={u('2b-plastik')} stroke={P_KOYU} strokeWidth={2} strokeLinejoin="round" />
      : <><path d={`M${L} ${-H * 0.2} L${L + 8} ${-H * 0.15} L${L + 8} ${H * 0.15} L${L} ${H * 0.2} Z`} fill="#c9d3de" stroke={P_KOYU} strokeWidth={1.6} strokeLinejoin="round" /><rect x={L + 8} y={-H * 0.24} width={5} height={H * 0.48} rx={1} fill={P_KOYU} /></>}
  </g>
);

/** Boşaltma musluğu: çıkış borusu + kırmızı kol (yerel: boru ağzı (0,0)'da yukarıda, aşağı iner) */
const Musluk = ({ s = 1 }: { s?: number }) => (
  <g transform={`scale(${s})`}>
    <path className="boya" d="M-6 0 L6 0 L6 14 L-6 14 Z" fill="#9aa6b4" stroke="#3e4a58" strokeWidth={2} strokeLinejoin="round" />
    <path d="M-5 16 L5 16 L5 26 L-5 26 Z" fill="#c9d3de" stroke="#3e4a58" strokeWidth={2} strokeLinejoin="round" />
    <path d="M6 5 L22 0 L24 8 L6 11 Z" fill="#d23b3b" stroke="#8d1f1f" strokeWidth={2} strokeLinejoin="round" />
  </g>
);

/** İdrar torbası (yerel: üst-orta (0,0); genişlik W, yükseklik Hh). Askı, damla odası, ölçek, boşaltma musluğu (`muslukId` dışarıdan sarılır). */
const Torba = ({ W = 180, Hh = 160, maxMl = 2000, dolu = 0, yazi = true }: { W?: number; Hh?: number; maxMl?: number; dolu?: number; yazi?: boolean }) => {
  const x0 = -W / 2, satir = 5;
  return (
    <g>
      {/* askı: iki kayış + halka */}
      <path d={`M${x0 + 24} 0 L${x0 + 40} -18 L${-x0 - 40} -18 L${-x0 - 24} 0`} stroke={P_KOYU} strokeWidth={4} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path d={`M${x0 + 40} -18 L${-x0 - 40} -18`} stroke="#dfe6ee" strokeWidth={1.5} />
      {/* gövde */}
      <rect className="boya" x={x0} y={0} width={W} height={Hh} rx={W * 0.08} fill={u('2b-plastik')} stroke={P_KOYU} strokeWidth={2.5} />
      {/* idrar filmi (yalnız dolu>0) */}
      {dolu > 0 && <path d={`M${x0 + 4} ${Hh - dolu} L${-x0 - 4} ${Hh - dolu} L${-x0 - 4} ${Hh - W * 0.08} Q${-x0 - 4} ${Hh - 3} ${-x0 - 4 - W * 0.08} ${Hh - 3} L${x0 + 4 + W * 0.08} ${Hh - 3} Q${x0 + 4} ${Hh - 3} ${x0 + 4} ${Hh - W * 0.08} Z`} fill={u('2b-idrar')} opacity={0.9} />}
      {/* damla odası (geri akış valfi) */}
      <rect x={-W * 0.07} y={2} width={W * 0.14} height={Hh * 0.2} rx={4} fill="#ffffff" stroke={P_KOYU} strokeWidth={2} />
      <path d={`M0 ${Hh * 0.08} l0 ${Hh * 0.06}`} stroke="#efc53f" strokeWidth={2.5} strokeLinecap="round" />
      {/* ölçek */}
      {Array.from({ length: satir }, (_, i) => {
        const y = Hh * 0.2 + i * (Hh * 0.74 / (satir - 1));
        return <g key={i}><path d={`M${-x0 - 22} ${y} L${-x0 - 8} ${y}`} stroke={YAZI} strokeWidth={1.5} />{yazi && <text x={-x0 - 26} y={y + 3.5} fontSize={W > 120 ? 10 : 7} textAnchor="end" fill={YAZI}>{Math.round(maxMl - i * (maxMl / satir))}</text>}</g>;
      })}
      {yazi && <text x={x0 + 10} y={Hh * 0.24} fontSize={W > 120 ? 10 : 7} fill={YAZI}>mL</text>}
      {/* alt çıkış boynu */}
      <path d={`M-8 ${Hh} L8 ${Hh} L6 ${Hh + 6} L-6 ${Hh + 6} Z`} fill="#c9d3de" stroke={P_KOYU} strokeWidth={2} strokeLinejoin="round" />
    </g>
  );
};

/* ——————————————————————————————— FOLEY ——————————————————————————————— */
/** Gövde: uç (sol) → düz tip bölümü → yumuşak dalga → Y bağlantı (600,200). Ölçek ≈ 1 cm 20 px: 16 Fr 5,3 mm ≈ 11 px, 10 mL balon ≈ 2,4 cm → r 24. */
const F_GOVDE = 'M74 200 L200 200 C300 200 320 292 420 292 C500 292 520 200 596 200';
const F_BAG = 'M716 200 C778 200 792 254 756 284 C734 304 700 290 672 300';

const Foley: Sahne = {
  ad: 'Foley kateter ve idrar torbası',
  gizli: ['f-balon', 'f-torba', 'f-torba-bag', 'f-enjektor'],
  etiket: {
    'f-uc': [110, 150, 'Kateter ucu (yuvarlak)'],
    'f-delik': [84, 250, 'İdrar delikleri'],
    'f-balon-sonuk': [160, 100, 'Sabitleme balonu (sönük)'],
    'f-balon': [160, 300, 'Şişirilmiş balon'],
    'f-govde': [420, 340, 'Gövde: sarı lateks / beyaz silikon'],
    'f-drenaj': [630, 250, 'Drenaj kanalı → torba'],
    'f-balon-kanal': [500, 70, 'Valfli balon kanalı → enjektör'],
    'f-torba': [500, 400, 'İdrar torbası'],
    'f-musluk': [520, 470, 'Boşaltma musluğu'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* torba bağı önce (torbanın ve hunin arkasında kalır) */}
      <g {...o('f-torba-bag')}>
        <Tup d={F_BAG} w={10} renk="#eef3f8" kontur={P_KOYU} cz vurgu={false} />
      </g>
      <g {...o('f-govde')}>
        <Tup d={F_GOVDE} w={11} cz />
      </g>
      <g {...o('f-uc')}>
        <path className="boya" d="M78 194.5 L70 194.5 A5.5 5.5 0 0 0 70 205.5 L78 205.5 Z" fill={u('2b-kateter')} stroke={K_KOYU} strokeWidth={2} strokeLinejoin="round" />
      </g>
      <g {...o('f-delik')}>
        <ellipse className="boya" cx={86} cy={197} rx={5} ry={3} fill="#5a3a10" stroke="#3a2608" strokeWidth={1} />
        <ellipse className="boya" cx={100} cy={203} rx={5} ry={3} fill="#5a3a10" stroke="#3a2608" strokeWidth={1} />
      </g>
      <g {...o('f-balon-sonuk')}>
        <rect className="boya" x={112} y={192} width={44} height={16} rx={8} fill={u('2b-kateter')} stroke={K_KOYU} strokeWidth={2} />
        <path d="M120 196 L148 196" stroke="#fff" strokeOpacity={0.6} strokeWidth={1.5} strokeLinecap="round" />
      </g>
      <g {...o('f-balon')}>
        <circle className="boya" cx={134} cy={200} r={24} fill={u('2b-balon')} stroke="#2e9e5b" strokeWidth={3} />
        <ellipse cx={126} cy={191} rx={6} ry={3.5} fill="#fff" />
      </g>
      {/* Y bağlantı gövdesi */}
      <path d="M590 194 L604 190 L614 190 L614 210 L604 210 L590 206 Z" fill={u('2b-kateter')} stroke={K_KOYU} strokeWidth={2} strokeLinejoin="round" />
      <g {...o('f-drenaj')}>
        <Tup d="M610 200 L680 200" w={11} />
        {/* huni bağlantı ucu */}
        <path className="boya" d="M678 193 L706 188 C710 188 712 190 712 194 L712 206 C712 210 710 212 706 212 L678 207 Z" fill={u('2b-kateter')} stroke={K_KOYU} strokeWidth={2} strokeLinejoin="round" />
        <ellipse cx={712} cy={200} rx={4} ry={10} fill="#8a5f12" stroke={K_KOYU} strokeWidth={1.5} />
        <ellipse cx={712} cy={200} rx={2} ry={5.5} fill="#3a2608" />
      </g>
      <g {...o('f-balon-kanal')}>
        <Tup d="M606 195 L658 146" w={9} />
        {/* valf: 16 Fr renk kodu turuncu + mavi luer kapak */}
        <g transform="translate(664 140) rotate(-43)">
          <rect className="boya" x={-12} y={-12} width={30} height={24} rx={6} fill="#f08a2e" stroke="#9a4a0e" strokeWidth={2} />
          <path d="M-6 -6 L10 -6" stroke="#fff" strokeOpacity={0.6} strokeWidth={1.6} strokeLinecap="round" />
          <rect x={18} y={-7} width={10} height={14} rx={2} fill="#2f6fd6" stroke="#1d4ea0" strokeWidth={1.5} />
        </g>
      </g>
      <g {...o('f-enjektor')}>
        {/* 10 mL enjektör, ucu valfe oturur (eksen kanal doğrultusunda, uç valfte) */}
        <g transform="translate(750 62) rotate(137)">
          <Enjektor L={76} H={18} piston={26} yazi="10 mL" yaziTers />
        </g>
      </g>
      <g {...o('f-torba')}>
        <g transform="translate(670 300)">
          <Torba W={180} Hh={156} maxMl={2000} />
        </g>
        <g {...o('f-musluk')}>
          <g transform="translate(670 462)"><Musluk /></g>
        </g>
      </g>
    </>
  ),
};

/* ——————————————————————————— FOLEY KESİT ——————————————————————————— */
/** Enine kesit (büyük): 16 Fr; drenaj lümeni geniş, balon lümeni ince, duvar kalın. Ölçek dairelerinde 1 mm = 6 px (1 Fr = 1/3 mm → r = Fr px). */
const FoleyKesit: Sahne = {
  ad: 'Kateter kesiti ve French ölçüsü',
  gizli: [],
  etiket: {
    'c-drenaj-lumen': [200, 470, 'Drenaj lümeni (geniş)'],
    'c-balon-lumen': [200, 40, 'Balon lümeni (ince)'],
    'c-olcek-eriskin': [590, 60, 'Erişkin: 12–24 Fr, boy sabit'],
    'c-olcek-cocuk': [590, 330, 'Çocuk: 6–8–10 Fr, daha kısa'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* büyük kesit: dış duvar */}
      <circle cx={210} cy={250} r={165} fill={u('2b-kateter')} stroke={K_KOYU} strokeWidth={3} />
      <path d="M118 150 C150 112 200 100 250 108" stroke="#fff" strokeOpacity={0.55} strokeWidth={4} fill="none" strokeLinecap="round" />
      <g {...o('c-drenaj-lumen')}>
        <circle className="boya" cx={190} cy={272} r={100} fill="#fff6dc" stroke={K_KOYU} strokeWidth={2.5} />
        <text x={190} y={276} textAnchor="middle" fontSize={11} fill={YAZI}>idrar</text>
      </g>
      <g {...o('c-balon-lumen')}>
        <circle className="boya" cx={262} cy={140} r={22} fill="#dbe9fa" stroke="#2f6fd6" strokeWidth={2.5} />
        <text x={262} y={144} textAnchor="middle" fontSize={9} fill={YAZI}>su</text>
      </g>
      <text x={210} y={440} textAnchor="middle" fontSize={11} fill={YAZI}>16 Fr enine kesit (5,3 mm)</text>
      {/* sağ: ölçek daireleri */}
      <g {...o('c-olcek-eriskin')}>
        {[12, 14, 16, 18, 20, 22, 24].map((f, i) => {
          const cx = 440 + i * 50;
          return (
            <g key={f}>
              <circle className="boya" cx={cx} cy={150} r={f} fill={u('2b-kateter')} stroke={K_KOYU} strokeWidth={2} />
              <circle cx={cx - f * 0.12} cy={150 + f * 0.14} r={f * 0.56} fill="#fff6dc" stroke={K_KOYU} strokeWidth={1.2} />
              <circle cx={cx + f * 0.42} cy={150 - f * 0.5} r={f * 0.16} fill="#dbe9fa" stroke="#2f6fd6" strokeWidth={1} />
              <text x={cx} y={200} fontSize={11} textAnchor="middle" fill={YAZI} fontWeight={600}>{f}</text>
            </g>
          );
        })}
        <text x={590} y={218} fontSize={10} textAnchor="middle" fill={YAZI}>Fr</text>
        {/* cetvel: 1 mm = 6 px */}
        <path d="M440 250 L740 250" stroke={YAZI} strokeWidth={1.5} />
        {Array.from({ length: 11 }, (_, i) => <path key={i} d={`M${440 + i * 30} ${i % 5 ? 246 : 242} L${440 + i * 30} 254`} stroke={YAZI} strokeWidth={1.2} />)}
        <text x={440} y={268} fontSize={10} textAnchor="middle" fill={YAZI}>0</text>
        <text x={590} y={268} fontSize={10} textAnchor="middle" fill={YAZI}>5 mm</text>
        <text x={740} y={268} fontSize={10} textAnchor="middle" fill={YAZI}>10 mm</text>
        <text x={590} y={286} fontSize={11} textAnchor="middle" fill={YAZI}>1 Fr = 1/3 mm dış çap · 16 Fr = 5,3 mm</text>
      </g>
      <g {...o('c-olcek-cocuk')}>
        {[6, 8, 10].map((f, i) => {
          const cx = 500 + i * 60;
          return (
            <g key={f}>
              <circle className="boya" cx={cx} cy={400} r={f} fill={u('2b-silikon')} stroke="#8a96a6" strokeWidth={2} />
              <circle cx={cx - f * 0.12} cy={400 + f * 0.14} r={f * 0.52} fill="#fff6dc" stroke="#8a96a6" strokeWidth={1} />
              <text x={cx} y={440} fontSize={11} textAnchor="middle" fill={YAZI} fontWeight={600}>{f}</text>
            </g>
          );
        })}
        <text x={620} y={458} fontSize={10} textAnchor="middle" fill={YAZI}>Fr</text>
      </g>
    </>
  ),
};

/* ——————————————————————————————— MALZEME ——————————————————————————————— */
export const MALZEMELER: [string, string, number, number][] = [
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

/** Soyulur paket: kâğıt arka + şeffaf ön film, soyma köşesi, içinde kıvrılmış kateter + Fr renk kodlu valf + etiket */
const KateterPaket = ({ lateks }: { lateks: boolean }) => {
  const renk = lateks ? u('2b-kateter') : u('2b-silikon');
  const kontur = lateks ? K_KOYU : '#8a96a6';
  const d = 'M-58 28 C-30 28 -34 -24 10 -24 C44 -24 54 2 36 14 C20 24 -2 14 0 -4';
  return (
    <g>
      <rect x={-82} y={-46} width={166} height={92} rx={4} fill="#f4efe4" stroke="#a89a7c" strokeWidth={2} />
      <rect x={-76} y={-40} width={110} height={80} rx={3} fill="#e8f2fb" stroke="#9fb6cc" strokeWidth={1.5} />
      {/* soyma köşesi (açılmış kâğıt ucu) */}
      <path d="M-82 -46 L-56 -46 L-82 -22 Z" fill="#e2d8c3" stroke="#a89a7c" strokeWidth={1.5} strokeLinejoin="round" />
      {/* kateter kıvrımı */}
      <path d={d} stroke={kontur} strokeWidth={8} fill="none" strokeLinecap="round" />
      <path className="boya-cizgi" d={d} stroke={renk} strokeWidth={5} fill="none" strokeLinecap="round" />
      {/* uç + göz */}
      <circle cx={0} cy={-6} r={3.6} fill={renk} stroke={kontur} strokeWidth={1.4} />
      <ellipse cx={3} cy={-9} rx={2} ry={1.3} fill="#5a3a10" />
      {/* çatal: huni + valf (16 Fr turuncu) */}
      <path d="M-58 28 L-70 22 L-70 34 Z" fill={renk} stroke={kontur} strokeWidth={1.4} strokeLinejoin="round" />
      <path d="M-62 24 L-70 12" stroke={kontur} strokeWidth={5} strokeLinecap="round" /><path d="M-62 24 L-70 12" stroke={renk} strokeWidth={2.5} strokeLinecap="round" />
      <rect x={-76} y={2} width={10} height={9} rx={2.5} fill="#f08a2e" stroke="#9a4a0e" strokeWidth={1.4} />
      {/* etiket */}
      <rect x={40} y={-36} width={40} height={30} rx={3} fill="#fff" stroke="#c9d3de" strokeWidth={1.2} />
      <rect x={40} y={-36} width={6} height={30} fill="#f08a2e" />
      <text x={62} y={-24} fontSize={8} textAnchor="middle" fill="#2f3b4b" fontWeight={700}>16 Fr</text>
      <text x={62} y={-13} fontSize={6.5} textAnchor="middle" fill={YAZI}>{lateks ? 'Lateks' : 'Silikon'}</text>
      <text x={62} y={-6} fontSize={6.5} textAnchor="middle" fill={YAZI}>10 mL</text>
    </g>
  );
};

/** Eldiven (düz): avuç + 4 parmak + başparmak, boğum çizgileri, manşet. Yerel: bilek (0,40) altta, parmaklar yukarı. */
const Eldiven = ({ dolgu, kontur, x = 0, y = 0, r = 0, s = 1 }: { dolgu: string; kontur: string; x?: number; y?: number; r?: number; s?: number }) => (
  <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}>
    <path className="boya" d="M-22 40 L-24 4 C-34 -4 -42 -14 -36 -20 C-30 -26 -24 -16 -18 -8 L-18 -40 C-18 -48 -8 -48 -8 -40 L-8 -12 L-6 -52 C-6 -60 6 -60 6 -52 L6 -12 L9 -46 C9 -54 20 -54 20 -46 L17 -8 L22 -34 C23 -42 33 -40 32 -32 L26 4 L24 40 Z" fill={dolgu} stroke={kontur} strokeWidth={2} strokeLinejoin="round" />
    <path d="M-22 30 L24 30" stroke={kontur} strokeWidth={1.5} opacity={0.6} />
    {[[-13, -28], [0, -36], [14, -32], [27, -20]].map(([px, py]) => <path key={px} d={`M${px - 3} ${py} q3 2 6 0`} stroke={kontur} strokeWidth={1.2} fill="none" opacity={0.6} />)}
  </g>
);

/** Böbrek küvet (düz mavi) — yerel merkez (0,0), genişlik ~100 */
const Kuvet = ({ s = 1 }: { s?: number }) => (
  <g transform={`scale(${s})`}>
    <path d="M-50 -2 C-52 -22 48 -22 50 -2 C52 14 36 24 14 20 C4 12 -4 12 -14 20 C-36 24 -52 14 -50 -2 Z" fill={u('2b-kuvet')} stroke="#1f4e79" strokeWidth={2.5} strokeLinejoin="round" />
    <path d="M-40 -6 C-30 -14 30 -14 40 -6" stroke="#9fcaf0" strokeWidth={3} fill="none" strokeLinecap="round" />
  </g>
);

const ikon = (id: string) => {
  switch (id) {
    case 'm-lateks': return <KateterPaket lateks />;
    case 'm-silikon': return <KateterPaket lateks={false} />;
    case 'm-nonsteril':
      return (
        <g>
          {/* eldiven kutusu: ön yüz + üst yüz + ağız; eldiven ağızdan çıkar */}
          <path d="M-70 -6 L64 -6 L64 48 L-70 48 Z" fill="#eaf1f8" stroke="#3f6f9c" strokeWidth={2} strokeLinejoin="round" />
          <path d="M-70 -6 L-54 -24 L80 -24 L64 -6 Z" fill="#f6f9fc" stroke="#3f6f9c" strokeWidth={2} strokeLinejoin="round" />
          <path d="M64 -6 L80 -24 L80 30 L64 48 Z" fill="#cfdceb" stroke="#3f6f9c" strokeWidth={2} strokeLinejoin="round" />
          <ellipse cx={8} cy={-15} rx={34} ry={5} fill="#3f6f9c" />
          <rect x={-60} y={10} width={74} height={16} rx={3} fill="#2f6fd6" />
          <text x={-23} y={21} fontSize={8.5} fill="#fff" textAnchor="middle" fontWeight={700}>NİTRİL · M</text>
          <text x={34} y={40} fontSize={7} fill={YAZI} textAnchor="middle">100 adet</text>
          <Eldiven dolgu={u('2b-eldiven')} kontur="#3f6f9c" x={10} y={-36} r={-10} s={0.62} />
        </g>
      );
    case 'm-steril':
      return (
        <g>
          {/* açılmış steril kâğıt sargı, iki eldiven (manşet katlı), SOL/SAĞ */}
          <path d="M-84 -46 L84 -46 L84 50 L-84 50 Z" fill="#fbf7ee" stroke="#b59c72" strokeWidth={2} strokeLinejoin="round" />
          <path d="M0 -46 L0 50 M-84 -46 L-60 -30 M84 -46 L60 -30" stroke="#dccfb3" strokeWidth={1.5} />
          <text x={-42} y={-32} fontSize={7.5} textAnchor="middle" fill="#8a6f3f" fontWeight={700}>SOL</text>
          <text x={42} y={-32} fontSize={7.5} textAnchor="middle" fill="#8a6f3f" fontWeight={700}>SAĞ</text>
          <Eldiven dolgu={u('2b-eldiven-steril')} kontur="#b59c72" x={-42} y={10} s={0.62} />
          <Eldiven dolgu={u('2b-eldiven-steril')} kontur="#b59c72" x={42} y={10} s={0.62} />
          <rect x={-56} y={28} width={28} height={9} fill="#efe3c9" stroke="#b59c72" strokeWidth={1.4} />
          <rect x={28} y={28} width={28} height={9} fill="#efe3c9" stroke="#b59c72" strokeWidth={1.4} />
        </g>
      );
    case 'm-jel':
      return (
        <g>
          {/* hazır dolu jel aplikatörü: körüklü gövde, konik uç, mavi kopartma kapağı; yanında tüp */}
          <rect className="boya" x={-70} y={-16} width={92} height={32} rx={4} fill={u('2b-plastik')} stroke={P_KOYU} strokeWidth={2} />
          <rect x={-64} y={-10} width={80} height={20} rx={2} fill={u('2b-jel')} />
          {[-54, -42, -30, -18, -6, 6].map((x) => <path key={x} d={`M${x} -16 l0 32`} stroke="#8fb0d6" strokeWidth={1.2} />)}
          <path d="M22 -10 L62 -4 L62 4 L22 10 Z" fill={u('2b-plastik')} stroke={P_KOYU} strokeWidth={2} strokeLinejoin="round" />
          <rect x={62} y={-6} width={14} height={12} rx={2.5} fill="#2f6fd6" stroke="#1d4ea0" strokeWidth={1.5} />
          <rect x={-82} y={-20} width={12} height={40} rx={3} fill="#9aa6b4" stroke={P_KOYU} strokeWidth={2} />
          <rect x={-56} y={22} width={74} height={18} rx={3} fill="#fff" stroke="#c9d3de" strokeWidth={1.2} />
          <text x={-19} y={34} fontSize={8} textAnchor="middle" fill="#2f4f6f" fontWeight={700}>Lidokain %2 · 11 mL</text>
        </g>
      );
    case 'm-izotonik':
      return (
        <g>
          {/* bükerek açılan 3 plastik ampul */}
          {[-34, 0, 34].map((x, i) => (
            <g key={x} transform={`translate(${x} 2) rotate(${(i - 1) * 5})`}>
              <path className="boya" d="M-12 -28 L12 -28 L14 34 C14 42 -14 42 -14 34 Z" fill={u('2b-plastik')} stroke={P_KOYU} strokeWidth={2} strokeLinejoin="round" />
              <path d="M-7 -28 L-4 -40 L4 -40 L7 -28 Z" fill="#dfe6ee" stroke={P_KOYU} strokeWidth={1.6} strokeLinejoin="round" />
              <rect x={-9} y={-50} width={18} height={10} rx={3} fill="#e9eef3" stroke={P_KOYU} strokeWidth={1.6} />
              <rect x={-9} y={-20} width={18} height={44} rx={1} fill="#e3f0fb" opacity={0.9} />
              <text x={0} y={2} fontSize={5.5} textAnchor="middle" fill="#2f4f6f" fontWeight={700}>NaCl</text>
              <text x={0} y={10} fontSize={5.5} textAnchor="middle" fill="#2f4f6f">%0,9</text>
              <text x={0} y={18} fontSize={5.5} textAnchor="middle" fill="#2f4f6f">10 mL</text>
            </g>
          ))}
        </g>
      );
    case 'm-enjektor':
      return <g transform="translate(-28 0)"><Enjektor L={92} H={20} piston={30} yazi="10 mL" /></g>;
    case 'm-genis':
      return (
        <g>
          <g transform="translate(-40 -6)"><Enjektor L={96} H={32} piston={30} kateterUcu yazi="50 mL" /></g>
          <text x={0} y={34} fontSize={7.5} textAnchor="middle" fill={YAZI}>kateter ucu (Luer değil)</text>
        </g>
      );
    case 'm-antiseptik':
      return (
        <g>
          {/* povidon şişe (sol), böbrek küvet (sağ) içinde gazlı bezler + iyot, pens (üstte) */}
          <rect className="boya" x={-82} y={-26} width={38} height={66} rx={8} fill="#a84a1c" stroke="#6b2c0c" strokeWidth={2} />
          <path d="M-72 -26 L-72 -36 L-54 -36 L-54 -26" fill="#e9eef3" stroke={P_KOYU} strokeWidth={2} strokeLinejoin="round" />
          <rect x={-70} y={-46} width={14} height={11} rx={2.5} fill="#e9eef3" stroke={P_KOYU} strokeWidth={2} />
          <rect x={-78} y={-6} width={30} height={26} rx={2} fill="#fff" />
          <text x={-63} y={5} fontSize={6} textAnchor="middle" fill="#7a3410" fontWeight={700}>POVİDON</text>
          <text x={-63} y={14} fontSize={6} textAnchor="middle" fill="#7a3410">İYOT %10</text>
          <g transform="translate(28 16)"><Kuvet s={1.05} /></g>
          {[[6, 4], [24, 0], [42, 6]].map(([x, y]) => <rect key={x} x={x - 8} y={y - 6} width={16} height={12} rx={1.5} fill="#ffffff" stroke="#c9d3de" strokeWidth={1.4} />)}
          <path d="M-2 4 L46 4" stroke="#a84a1c" strokeWidth={3} strokeLinecap="round" opacity={0.75} />
          {/* pens: iki kol + halkalar + kilit */}
          <path d="M-20 -40 L72 -22 M-20 -34 L72 -26" stroke="#5b6676" strokeWidth={4} strokeLinecap="round" />
          <path d="M-20 -40 L72 -22 M-20 -34 L72 -26" stroke="#dfe6ee" strokeWidth={1.6} strokeLinecap="round" />
          <circle cx={-24} cy={-42} r={5} fill="none" stroke="#5b6676" strokeWidth={2.5} />
          <circle cx={-24} cy={-31} r={5} fill="none" stroke="#5b6676" strokeWidth={2.5} />
          <path d="M14 -36 L14 -28" stroke="#5b6676" strokeWidth={2} />
        </g>
      );
    case 'm-ortu':
      return (
        <g>
          <path className="boya" d="M-84 -46 L84 -46 L84 50 L-84 50 Z M0 -16 C-18 -16 -18 20 0 20 C18 20 18 -16 0 -16 Z" fill={u('2b-ortu')} fillRule="evenodd" stroke="#2f6f5f" strokeWidth={2} strokeLinejoin="round" />
          <path d="M-84 -14 L-24 -14 M24 -14 L84 -14 M-84 18 L-26 18 M26 18 L84 18" stroke="#2f6f5f" strokeWidth={1.3} opacity={0.5} />
          <circle cx={0} cy={2} r={22} fill="none" stroke="#bfe6d8" strokeWidth={2} strokeDasharray="3 3" />
          <text x={0} y={42} fontSize={7} textAnchor="middle" fill="#e6f4ee">delikli (fenestre)</text>
        </g>
      );
    default:
      return (
        <g>
          {/* 2000 mL torba (küçük): giriş hortumu + askı + damla odası + ölçek + musluk */}
          <g transform="translate(0 -30)"><Torba W={90} Hh={70} maxMl={2000} yazi={false} /></g>
          <path d="M0 -30 C0 -42 30 -46 56 -40" stroke={P_KOYU} strokeWidth={7} fill="none" strokeLinecap="round" />
          <path d="M0 -30 C0 -42 30 -46 56 -40" stroke="#eef3f8" strokeWidth={4} fill="none" strokeLinecap="round" />
          <rect x={54} y={-46} width={14} height={12} rx={2.5} fill="#dfe6ee" stroke={P_KOYU} strokeWidth={1.6} transform="rotate(12 61 -40)" />
          <g transform="translate(0 46) scale(0.5)"><Musluk /></g>
          <text x={-28} y={14} fontSize={7} textAnchor="middle" fill={YAZI} fontWeight={700}>2000</text>
          <text x={-28} y={23} fontSize={6.5} textAnchor="middle" fill={YAZI}>mL</text>
        </g>
      );
  }
};

const Malzeme: Sahne = {
  ad: 'Üretral kateter malzeme tepsisi',
  gizli: ['m-steril-alan'],
  etiket: { 'm-jel': [105, 200, 'Kayganlaştırır + anestezi'] },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* düz tepsi: kenar + iç yüzey */}
      <rect x={8} y={8} width={784} height={484} rx={24} fill="#c7d2dd" stroke={P_KOYU} strokeWidth={3} />
      <rect x={22} y={22} width={756} height={462} rx={16} fill="#e6edf3" stroke="#aebbc8" strokeWidth={2} />
      <g {...o('m-steril-alan')}>
        <rect x={200} y={20} width={580} height={330} rx={14} fill="#cfe7d8" opacity={0.45} />
        <rect className="cz boya-cizgi" pathLength={1} x={200} y={20} width={580} height={330} rx={14} fill="none" stroke="#2e9e5b" strokeWidth={4} strokeDasharray="0.02 0.01" />
      </g>
      {MALZEMELER.map(([id, ad, x, y]) => (
        <g key={id} {...o(id)}>
          <g transform={`translate(${x} ${y - 8})`}>{ikon(id)}</g>
          {(() => {
            const [bas, ...kalan] = ad.split(/ (?=\()|, (?=[a-zçğıöşü])/);
            return (
              <text x={x} y={y + 54} textAnchor="middle" fontSize={11.5} fill="#2f3b4b" fontWeight={600}>
                {bas}{kalan.length > 0 && <tspan x={x} dy={12} fontSize={10} fontWeight={400} fill={YAZI}>{kalan.join(', ')}</tspan>}
              </text>
            );
          })()}
        </g>
      ))}
      {/* boş köşe: Fr renk kodu kartı */}
      <g transform="translate(690 420)">
        <rect x={-86} y={-56} width={172} height={104} rx={8} fill="#fff" stroke="#c9d3de" strokeWidth={1.5} />
        <text x={0} y={-40} fontSize={9.5} textAnchor="middle" fill="#2f3b4b" fontWeight={700}>Valf renkleri (Fr)</text>
        {[['12', '#ffffff'], ['14', '#2e9e5b'], ['16', '#f08a2e'], ['18', '#d23b3b'], ['20', '#f2d000'], ['22', '#8e44ad']].map(([f, c], i) => (
          <g key={f} transform={`translate(${-76 + (i % 3) * 54} ${-20 + Math.floor(i / 3) * 34})`}>
            <rect x={0} y={0} width={16} height={14} rx={3} fill={c} stroke={P_KOYU} strokeWidth={1.2} />
            <text x={20} y={11} fontSize={9.5} fill="#2f3b4b">{f} Fr</text>
          </g>
        ))}
      </g>
    </>
  ),
};

/* ——————————————————————————————— MAKET ——————————————————————————————— */
/** Eğitim maketi (üstten, sırtüstü): pelvis gövdesi + uyluk kütükleri, üstte mesane haznesi, ortada değiştirilebilir modül yuvası.
 *  Kadın ve erkek modülü aynı yuvaya oturur; biri görünürken öteki gizli (mk-erkek gizli başlar). */
const Maket: Sahne = {
  ad: 'Sınav maketi: değiştirilebilir kadın / erkek modülü',
  gizli: ['mk-erkek', 'mk-hazne-dolu'],
  etiket: {
    'mk-govde': [400, 40, 'Pelvis gövdesi + uyluklar'],
    'mk-kadin': [640, 250, 'Kadın genital modülü'],
    'mk-erkek': [640, 250, 'Erkek genital modülü'],
    'mk-hazne': [160, 100, 'Mesane haznesi (su doldurulur)'],
    'mk-hazne-dolu': [160, 150, 'Dolu hazne: kateterden "idrar" gelir'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* taban plakası (düz) */}
      <rect x={90} y={440} width={620} height={30} rx={8} fill="#dfe6ee" stroke={P_KOYU} strokeWidth={2.5} />
      <g {...o('mk-govde')}>
        {/* uyluk kütükleri (gövdenin arkasında) + kesit yüzleri */}
        <path className="boya" d="M212 236 C168 262 128 322 122 400 C120 430 150 446 184 440 C236 430 290 390 322 320 Z" fill={u('2b-deri')} stroke="#b9805a" strokeWidth={2.5} strokeLinejoin="round" />
        <path className="boya" d="M588 236 C632 262 672 322 678 400 C680 430 650 446 616 440 C564 430 510 390 478 320 Z" fill={u('2b-deri')} stroke="#b9805a" strokeWidth={2.5} strokeLinejoin="round" />
        <ellipse cx={154} cy={420} rx={34} ry={22} fill="#e2a37c" stroke="#b9805a" strokeWidth={2.5} transform="rotate(-30 154 420)" />
        <ellipse cx={646} cy={420} rx={34} ry={22} fill="#e2a37c" stroke="#b9805a" strokeWidth={2.5} transform="rotate(30 646 420)" />
        {/* pelvis gövdesi */}
        <path className="boya" d="M204 72 C260 50 540 50 596 72 L616 212 C620 244 598 266 574 274 L226 274 C202 266 180 244 184 212 Z" fill={u('2b-deri')} stroke="#b9805a" strokeWidth={2.5} strokeLinejoin="round" />
        {/* kasık kıvrımları */}
        <path d="M250 240 C290 254 330 262 352 268 M550 240 C510 254 470 262 448 268" stroke="#b9805a" strokeWidth={2} fill="none" strokeLinecap="round" opacity={0.6} />
        {/* kapak vidaları */}
        <circle cx={262} cy={134} r={10} fill="#f08a8a" stroke="#b55c5c" strokeWidth={2} /><circle cx={538} cy={134} r={10} fill="#f08a8a" stroke="#b55c5c" strokeWidth={2} />
        <path d="M256 134 L268 134 M532 134 L544 134" stroke="#b55c5c" strokeWidth={2} strokeLinecap="round" />
      </g>
      <g {...o('mk-hazne')}>
        {/* saydam hazne: silindir, kapak, doldurma ağzı */}
        <path className="boya" d="M340 86 C340 72 460 72 460 86 L458 150 C458 162 342 162 342 150 Z" fill="#edf4fb" stroke={P_KOYU} strokeWidth={2.5} strokeLinejoin="round" />
        <ellipse cx={400} cy={86} rx={60} ry={14} fill="#f7fafd" stroke={P_KOYU} strokeWidth={2.5} />
        <rect x={386} y={60} width={28} height={16} rx={4} fill="#2f6fd6" stroke="#1d4ea0" strokeWidth={2} />
        <path d="M354 100 L354 146" stroke="#fff" strokeWidth={3} strokeLinecap="round" opacity={0.8} />
        {/* seviye çizgileri */}
        {[110, 128, 146].map((y) => <path key={y} d={`M444 ${y} L452 ${y}`} stroke={YAZI} strokeWidth={1.5} />)}
      </g>
      <g {...o('mk-hazne-dolu')}>
        <path className="boya" d="M345 118 L455 118 L457 150 C457 160 343 160 343 150 Z" fill={u('2b-idrar')} opacity={0.9} stroke="none" />
        <ellipse cx={400} cy={118} rx={55} ry={9} fill="#fbe58a" stroke="#d9a91f" strokeWidth={1.5} opacity={0.95} />
      </g>
      {/* modül yuvası (çerçeve + kilit tırnakları) */}
      <path d="M338 188 C338 176 462 176 462 188 L470 334 C470 352 330 352 330 334 Z" fill="#d18f68" stroke="#9a5f3f" strokeWidth={2.5} strokeLinejoin="round" />
      <rect x={344} y={192} width={16} height={9} rx={2} fill="#dfe6ee" stroke={P_KOYU} strokeWidth={1.5} /><rect x={440} y={192} width={16} height={9} rx={2} fill="#dfe6ee" stroke={P_KOYU} strokeWidth={1.5} />
      <g {...o('mk-kadin')}>
        {/* kadın modülü: labia majora, labia minora, klitoris (üst), meatus (ortada üst), vajina (altta) */}
        <path className="boya" d="M400 204 C360 208 348 258 352 300 C356 336 380 344 400 344 C420 344 444 336 448 300 C452 258 440 208 400 204 Z" fill="#e7a3a0" stroke="#a85f5a" strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M400 224 C384 228 378 266 384 300 C388 322 395 330 400 330 C405 330 412 322 416 300 C422 266 416 228 400 224 Z" fill="#d07f7b" stroke="#a85f5a" strokeWidth={1.6} />
        <circle cx={400} cy={236} r={5} fill="#b35a55" stroke="#7d2f2a" strokeWidth={1.5} />
        <ellipse cx={400} cy={262} rx={4.5} ry={6} fill="#7d2f2a" />
        <ellipse cx={400} cy={302} rx={9} ry={16} fill="#8a3b36" stroke="#7d2f2a" strokeWidth={1.5} />
      </g>
      <g {...o('mk-erkek')}>
        {/* erkek modülü: taban plakası, penis aşağı (ayak yönü) uzanır, glans + meatus, skrotum iki yanda */}
        <path className="boya" d="M400 204 C360 208 348 258 352 300 C356 336 380 344 400 344 C420 344 444 336 448 300 C452 258 440 208 400 204 Z" fill={u('2b-deri')} stroke="#b9805a" strokeWidth={2.5} strokeLinejoin="round" />
        {/* skrotum (arkada) */}
        <ellipse cx={382} cy={276} rx={19} ry={22} fill="#e9b48d" stroke="#b9805a" strokeWidth={2.5} />
        <ellipse cx={418} cy={276} rx={19} ry={22} fill="#e9b48d" stroke="#b9805a" strokeWidth={2.5} />
        {/* penis (önde, ayak yönüne uzanır) + glans + meatus */}
        <path className="boya" d="M387 228 L413 228 L415 302 C415 306 385 306 385 302 Z" fill="#edb08c" stroke="#b9805a" strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M392 236 L392 296" stroke="#f7d2b6" strokeWidth={4} strokeLinecap="round" opacity={0.9} />
        <path d="M383 302 C381 320 389 330 400 330 C411 330 419 320 417 302 Z" fill="#d98580" stroke="#a85f5a" strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M397 325 L403 325" stroke="#7d2f2a" strokeWidth={2.5} strokeLinecap="round" />
      </g>
    </>
  ),
};

export const SAHNELER_2B_A: Record<string, Sahne> = { foley: Foley, 'foley-kesit': FoleyKesit, malzeme: Malzeme, maket: Maket };
