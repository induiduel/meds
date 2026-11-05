/** KMB 01 Nazogastrik sonda 2B sahneleri — grup B: ng-govde (NEX ölçümü + yer kontrolü, yandan) ve ng-mide (mide, önden).
 *  docs/KMB_2B_STIL.md: iki duraklı degrade ya da düz renk, 2–3 px kontur, filtre yok; öge kimlikleri SAHNE_OGELERI ile birebir.
 *  H462: sonda yalnız burun boşluğu → farinks → özofagus → mide lümeninde; dış alet (enjektör, stetoskop, torba) gövdenin dışında,
 *  deriye değer ama gömülmez; oturan hastada mide sıvısı yatay yüzeyli ve altta, hava üstte. */
import React from 'react';
import { type Sahne } from './sahneOrtak';

type Pt = [number, number];
const yol = (pts: Pt[]) => pts.map((p, i) => `${i ? 'L' : 'M'}${p[0]} ${p[1]}`).join(' ');

const DERI = 'url(#kmb-2b-deri)', DERI_K = 'url(#kmb-2b-deri-koyu)', KONTUR_DERI = '#b9805a';
const SONDA_K = '#4f7590', SONDA_A = '#dcebf6';

/** PVC sonda: koyu kontur + açık gövde (silindir). `cz` ile çizilebilir; `op` ile vücut içi seyir yarı saydam. */
function Sonda({ d, w = 7, cz = false, op = 1 }: { d: string; w?: number; cz?: boolean; op?: number }) {
  return (
    <g opacity={op}>
      <path d={d} stroke={SONDA_K} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path className={`${cz ? 'cz ' : ''}boya-cizgi`} pathLength={cz ? 1 : undefined} d={d} stroke={SONDA_A} strokeWidth={w * 0.6} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </g>
  );
}

/** Uzuv (kol): kontur + düz dolgu kalın kırık çizgi. */
function Uzuv({ pts, w, dolgu, kontur }: { pts: Pt[]; w: number; dolgu: string; kontur: string }) {
  const d = yol(pts);
  return (
    <>
      <path d={d} stroke={kontur} strokeWidth={w + 5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path d={d} stroke={dolgu} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </>
  );
}

/** Dikey çan (kateter) uçlu 50 mL enjektör; uç yukarıda (x, y = uç ağzı). Hava dolu: piston geride. */
function Enjektor({ x, y }: { x: number; y: number }) {
  const b = y + 14; // gövde başı
  return (
    <>
      {/* çan (kateter) uç: konik */}
      <path className="boya" d={`M${x - 4} ${y} L${x + 4} ${y} L${x + 9} ${b} L${x - 9} ${b} Z`} fill="url(#kmb-2b-plastik)" stroke="#6b7a90" strokeWidth={2} strokeLinejoin="round" />
      {/* saydam gövde */}
      <rect x={x - 20} y={b} width={40} height={104} rx={5} fill="#eef4fa" fillOpacity={0.85} stroke="#6b7a90" strokeWidth={2.5} />
      {[0, 1, 2, 3, 4].map((i) => <path key={i} d={`M${x + 20} ${b + 14 + i * 18} L${x + 10} ${b + 14 + i * 18}`} stroke="#6b7a90" strokeWidth={1.5} />)}
      <text x={x - 2} y={b + 26} fontSize={10} fill="#3e4a58" textAnchor="middle">50</text>
      {/* piston lastiği (geride: gövde hava dolu) */}
      <rect x={x - 18} y={b + 86} width={36} height={10} rx={2} fill="#3e4a58" />
      {/* kanatlar + piston kolu + başparmak tablası */}
      <rect x={x - 30} y={b + 104} width={60} height={7} rx={3} fill="url(#kmb-2b-plastik)" stroke="#6b7a90" strokeWidth={2} />
      <rect x={x - 5} y={b + 96} width={10} height={44} fill="#c9d3df" stroke="#6b7a90" strokeWidth={2} />
      <rect x={x - 21} y={b + 140} width={42} height={8} rx={3} fill="url(#kmb-2b-plastik)" stroke="#6b7a90" strokeWidth={2} />
    </>
  );
}

// ———————————————————————————————————————————————————————— NG-GÖVDE (oturan hasta, yandan; yüz sola)

/** Ölçek ≈ 1 cm 7 px (baş ~23 cm). NEX: burun ucu (332,122) → kulak memesi (444,130) → ksifoid (388,338).
 *  Ksifoid sternumun alt ucu; epigastrium hemen altı; mide sol üst karında kaburga kenarının altında, fundus arkada-yukarıda. */
const NgGovde: Sahne = {
  ad: 'Oturan hasta, yandan: NEX ölçümü ve sonda yeri',
  gizli: ['nb-olcu-1', 'nb-olcu-2', 'nb-sonda-olcu', 'nb-isaret', 'nb-sonda', 'nb-ozofagus', 'nb-epigastr', 'nb-stetoskop', 'nb-enjektor', 'nb-ses'],
  etiket: {
    'nb-bas': [545, 70, 'Baş'],
    'nb-burun': [250, 130, 'Burun deliği'],
    'nb-kulak': [560, 135, 'Kulak memesi'],
    'nb-ksifoid': [262, 312, 'Ksifoid'],
    'nb-mide': [452, 445, 'Mide'],
    'nb-govde': [650, 420, 'Gövde (oturur)'],
    'nb-olcu-1': [390, 58, 'Burun → kulak memesi'],
    'nb-olcu-2': [560, 230, 'Kulak memesi → ksifoid'],
    'nb-sonda-olcu': [560, 180, 'Sonda ile NEX ölçümü'],
    'nb-isaret': [262, 360, 'Ksifoid hizası işareti'],
    'nb-sonda': [235, 185, 'Takılı sonda'],
    'nb-ozofagus': [530, 290, 'Özofagus'],
    'nb-epigastr': [282, 412, 'Epigastrium'],
    'nb-stetoskop': [300, 230, 'Stetoskop'],
    'nb-enjektor': [126, 462, 'Çan uçlu 50 mL enjektör'],
    'nb-ses': [560, 470, 'Fokurdama sesi'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* sandalye/yatak başı arkalığı (dik oturuş) */}
      <rect x={566} y={150} width={22} height={350} rx={8} fill="url(#kmb-2b-yatak)" stroke="#4f9aa0" strokeWidth={2.5} />
      <g {...o('nb-govde')}>
        <path className="boya" d="M414 210 C412 228 404 238 392 246 C378 258 374 290 377 320 C379 336 382 346 380 360 C376 390 372 430 376 470 L378 500 L560 500 C556 440 556 380 552 330 C548 290 542 262 528 244 C516 230 496 220 482 210 Z" fill="#eebb93" />
        <path d="M414 210 C412 228 404 238 392 246 C378 258 374 290 377 320 C379 336 382 346 380 360 C376 390 372 430 376 470 L378 500 L560 500 C556 440 556 380 552 330 C548 290 542 262 528 244 C516 230 496 220 482 210" fill="none" stroke={KONTUR_DERI} strokeWidth={2.5} strokeLinejoin="round" />
        {/* sternum + ksifoid, kaburga kenarı (arkus kostarum) */}
        <path d="M398 250 L390 330" stroke="#b9a479" strokeWidth={6} strokeLinecap="round" opacity={0.55} />
        <path d="M390 340 C410 360 440 376 470 384" stroke={KONTUR_DERI} strokeWidth={2} fill="none" opacity={0.6} strokeLinecap="round" />
        {/* göbek */}
        <path d="M378 452 q5 4 0 9" stroke={KONTUR_DERI} strokeWidth={2} fill="none" />
      </g>
      <g {...o('nb-mide')}>
        <path className="boya" d="M432 356 C452 336 480 348 478 375 C476 405 450 430 420 425 C400 420 394 400 402 388 C412 375 428 372 432 356 Z" fill="url(#kmb-2b-mesane)" fillOpacity={0.4} stroke="#7a2e26" strokeWidth={2} strokeOpacity={0.7} strokeDasharray="5 3" />
      </g>
      <g {...o('nb-epigastr')}>
        <circle className="boya" cx={402} cy={366} r={20} fill="#f2c14e" fillOpacity={0.35} stroke="#c9952b" strokeWidth={2} strokeDasharray="4 3" />
      </g>
      <g {...o('nb-ozofagus')}>
        <path className="boya-cizgi" d="M424 150 C424 200 430 240 434 280 C436 310 436 335 432 356" stroke="#c9736e" strokeWidth={13} strokeOpacity={0.4} fill="none" strokeLinecap="round" />
        <path d="M342 128 C370 126 400 124 412 130 C422 136 424 150 424 168" stroke="#c9736e" strokeWidth={10} strokeOpacity={0.25} fill="none" strokeLinecap="round" />
      </g>
      {/* kol (yanda, gövdenin önünde) */}
      <Uzuv pts={[[506, 252], [514, 360], [504, 448]]} w={32} dolgu="#e9b48e" kontur={KONTUR_DERI} />
      <g {...o('nb-bas')}>
        <path className="boya" d="M365 70 C372 40 410 28 440 30 C482 32 506 62 502 102 C499 132 490 152 480 170 C476 186 478 200 482 214 L414 214 C414 204 410 192 394 190 C374 190 360 184 356 172 C352 162 352 156 350 150 C348 146 352 142 352 140 C348 136 346 134 344 132 L336 128 C330 126 329 120 333 116 C342 110 350 104 356 98 C358 90 358 82 365 70 Z" fill="#eebb93" />
        <path d="M365 70 C372 40 410 28 440 30 C482 32 506 62 502 102 C499 132 490 152 480 170 C476 186 478 200 482 214 M414 214 C414 204 410 192 394 190 C374 190 360 184 356 172 C352 162 352 156 350 150 C348 146 352 142 352 140 C348 136 346 134 344 132 L336 128 C330 126 329 120 333 116 C342 110 350 104 356 98 C358 90 358 82 365 70" fill="none" stroke={KONTUR_DERI} strokeWidth={2.5} strokeLinejoin="round" />
        {/* saç */}
        <path d="M368 66 C376 38 412 26 442 28 C484 30 508 62 502 104 C496 92 488 80 476 74 C450 62 410 60 368 66 Z" fill="#5a3d2b" stroke="#3b2a1e" strokeWidth={2} strokeLinejoin="round" />
        <path d="M366 90 q6 -3 12 0" stroke="#3b2a1e" strokeWidth={2.2} fill="none" strokeLinecap="round" />
        <ellipse cx={372} cy={98} rx={3} ry={2.2} fill="#3b2a1e" />
        <path d="M352 146 q-4 2 -2 6" stroke="#a0674e" strokeWidth={2} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('nb-kulak')}>
        <path d="M440 92 C452 88 458 100 456 114 C455 124 450 132 444 134 C438 134 436 128 438 122 C434 112 434 98 440 92 Z" fill={DERI_K} stroke={KONTUR_DERI} strokeWidth={2.2} strokeLinejoin="round" />
        <path d="M444 100 C450 104 450 114 446 118" stroke={KONTUR_DERI} strokeWidth={1.6} fill="none" />
        <circle className="boya" cx={444} cy={130} r={4.5} fill="#2e9e5b" stroke="#ffffff" strokeWidth={1.5} />
      </g>
      <g {...o('nb-burun')}>
        <ellipse cx={342} cy={128} rx={4} ry={2.5} fill="#7d4a36" />
        <circle className="boya" cx={332} cy={121} r={4.5} fill="#2e9e5b" stroke="#ffffff" strokeWidth={1.5} />
      </g>
      <g {...o('nb-ksifoid')}>
        <path d="M391 330 L389 342" stroke="#b9a479" strokeWidth={6} strokeLinecap="round" />
        <circle className="boya" cx={388} cy={338} r={4.5} fill="#2e9e5b" stroke="#ffffff" strokeWidth={1.5} />
      </g>
      <g {...o('nb-olcu-1')}>
        <path className="cz boya-cizgi" pathLength={1} d="M332 121 L444 130" stroke="#1f4e79" strokeWidth={2.5} strokeDasharray="6 4" fill="none" strokeLinecap="round" />
      </g>
      <g {...o('nb-olcu-2')}>
        <path className="cz boya-cizgi" pathLength={1} d="M444 130 L388 338" stroke="#1f4e79" strokeWidth={2.5} strokeDasharray="6 4" fill="none" strokeLinecap="round" />
      </g>
      <g {...o('nb-sonda')}>
        {/* iç seyir: burun boşluğu → nazofarinks → özofagus → mide (yarı saydam) */}
        <Sonda op={0.55} d="M342 128 C370 126 400 124 412 130 C422 136 424 150 424 168 C424 200 430 240 434 280 C436 310 436 335 432 356 C430 375 428 392 424 408" />
        {/* dış uç: burundan çıkar, burun sırtına bantlı, aşağı sarkar; ucunda bağlantı hunisi */}
        <Sonda cz d="M340 130 C320 140 300 140 280 150 C240 170 190 196 172 236" />
        <path d="M166 236 L178 236 L183 254 L161 254 Z" fill="#c9d3df" stroke={SONDA_K} strokeWidth={2} strokeLinejoin="round" />
        <rect x={326} y={112} width={20} height={9} rx={2} fill="#ffffff" fillOpacity={0.9} stroke="#8a96a6" strokeWidth={1.5} transform="rotate(-38 336 116)" />
      </g>
      <g {...o('nb-sonda-olcu')}>
        <Sonda cz d="M330 119 C370 106 420 118 444 132 C430 200 400 280 388 338 C372 376 354 420 356 470" />
      </g>
      <g {...o('nb-isaret')}>
        <circle className="boya-cizgi" cx={388} cy={338} r={8} fill="none" stroke="#3e4a58" strokeWidth={3} />
      </g>
      <g {...o('nb-enjektor')}>
        <Enjektor x={172} y={250} />
      </g>
      <g {...o('nb-stetoskop')}>
        {/* diyafram yandan (deriye değer), sap, hortum yukarı, Y ayrımı, metal kulaklıklar */}
        <rect className="boya" x={367} y={349} width={10} height={32} rx={4} fill="url(#kmb-2b-metal)" stroke="#5b6676" strokeWidth={2} />
        <rect x={355} y={359} width={12} height={12} rx={3} fill="#c9d3df" stroke="#5b6676" strokeWidth={2} />
        <path d="M355 365 C330 365 314 342 312 300" stroke="#2b3440" strokeWidth={6} fill="none" strokeLinecap="round" />
        <path d="M312 300 C300 284 294 266 296 246 M312 300 C324 284 330 266 328 246" stroke="#8a96a6" strokeWidth={4} fill="none" strokeLinecap="round" />
        <circle cx={296} cy={244} r={5} fill="#2b3440" />
        <circle cx={328} cy={244} r={5} fill="#2b3440" />
      </g>
      <g {...o('nb-ses')}>
        {[12, 20, 28].map((r) => <path key={r} className="boya-cizgi" d={`M${426 + r * 0.7} ${404 - r * 0.7} Q${426 + r * 1.05} ${404} ${426 + r * 0.7} ${404 + r * 0.7}`} stroke="#2e9e5b" strokeWidth={2.5} fill="none" strokeLinecap="round" />)}
        {[[420, 398, 3], [428, 390, 2.5], [416, 388, 2]].map(([x, y, r]) => <circle key={`${x}${y}`} cx={x} cy={y} r={r} fill="#ffffff" stroke="#1f4e79" strokeWidth={1.2} />)}
      </g>
    </>
  ),
};

// ———————————————————————————————————————————————————————— NG-MİDE (önden; görüntünün sağı = hastanın solu)

/** Önden görünüm: fundus hastanın solunda (görüntüde sağ üst), pilor ve duodenum hastanın sağında (görüntüde sol).
 *  Hasta oturur → sıvı altta yatay yüzeyle (y 236), hava fundusta. Torba mide hizasının (alt sınır y ≈ 330) altında. */
const MIDE_D = 'M456 122 C470 78 540 66 562 116 C584 170 576 256 524 298 C476 336 396 332 352 302 C334 290 318 272 304 264 L292 262 L292 238 L304 238 C336 240 372 250 404 236 C432 222 438 170 432 122 Z';
const IC_SONDA = 'M443 0 L443 122 C444 170 446 230 448 292';
const DIS_UC = 'M680 0 C680 60 682 110 680 150';

const NgMide: Sahne = {
  ad: 'Mide ve sonda ucu (önden)',
  gizli: ['nd-sonda', 'nd-hava', 'nd-ses', 'nd-stetoskop', 'nd-enjektor', 'nd-su', 'nd-torba', 'nd-akis', 'nd-beslenme', 'nd-tipa'],
  etiket: {
    'nd-karin': [95, 470, 'Karın ön duvarı'],
    'nd-ozofagus': [520, 30, 'Özofagus'],
    'nd-mide': [520, 180, 'Mide'],
    'nd-mide-sivi': [400, 350, 'Mide içeriği (sıvı)'],
    'nd-duodenum': [230, 412, 'Duodenum'],
    'nd-epigastr': [400, 215, 'Epigastrium'],
    'nd-sonda': [560, 250, 'Nazogastrik sonda'],
    'nd-hava': [575, 300, 'Hava kabarcıkları'],
    'nd-ses': [260, 150, 'Fokurdama sesi'],
    'nd-stetoskop': [210, 90, 'Stetoskop'],
    'nd-enjektor': [712, 120, 'Çan uçlu enjektör'],
    'nd-su': [520, 80, 'Lavaj suyu'],
    'nd-torba': [720, 486, 'Drenaj torbası'],
    'nd-akis': [705, 375, 'Sifonla boşalma'],
    'nd-beslenme': [250, 290, 'Beslenme sondası (kılavuz telli)'],
    'nd-tipa': [740, 170, 'Tıpa'],
  },
  Ciz: ({ o }) => (
    <>
      <defs>
        <clipPath id="kmb-ngb-mide-klip"><path d={MIDE_D} /></clipPath>
      </defs>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      <g {...o('nd-karin')}>
        <path className="boya" d="M180 0 C170 120 160 260 170 500 L620 500 C630 260 622 120 612 0 Z" fill={DERI} fillOpacity={0.55} stroke={KONTUR_DERI} strokeWidth={3} strokeLinejoin="round" />
        {/* ksifoid + kaburga kenarları (ters V), göbek */}
        <path d="M400 60 L400 92 M396 92 C340 140 290 180 220 214 M404 92 C460 140 510 180 580 214" stroke="#b9a479" strokeWidth={4} fill="none" strokeLinecap="round" opacity={0.7} />
        <path d="M394 452 q6 6 12 0 q-6 -6 -12 0" stroke={KONTUR_DERI} strokeWidth={2} fill="none" />
      </g>
      <text x={186} y={492} fontSize={11} fill="#3e4a58">Hastanın sağı</text>
      <text x={604} y={492} fontSize={11} fill="#3e4a58" textAnchor="end">Hastanın solu</text>
      <g {...o('nd-epigastr')}>
        <circle className="boya" cx={400} cy={150} r={46} fill="#f2c14e" fillOpacity={0.25} stroke="#c9952b" strokeWidth={2} strokeDasharray="5 4" />
      </g>
      <g {...o('nd-ozofagus')}>
        <path className="boya" d="M430 0 L456 0 L458 122 L432 122 Z" fill="url(#kmb-2b-mukoza)" stroke="#a85f5a" strokeWidth={2.5} strokeLinejoin="round" />
      </g>
      <g {...o('nd-duodenum')}>
        <path d="M292 250 C268 250 244 254 236 280 C230 310 232 350 240 384" stroke="#a85f5a" strokeWidth={26} fill="none" strokeLinecap="round" />
        <path className="boya-cizgi" d="M292 250 C268 250 244 254 236 280 C230 310 232 350 240 384" stroke="#e49a93" strokeWidth={21} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('nd-mide')}>
        <path className="boya" d={MIDE_D} fill="url(#kmb-2b-mukoza)" fillOpacity={0.55} stroke="#7a2e26" strokeWidth={3} strokeLinejoin="round" />
        {/* rugalar */}
        {[[360, 280, 420, 300], [440, 280, 510, 270], [500, 140, 550, 200]].map(([a, b, c, d]) => <path key={a} d={`M${a} ${b} Q${(a + c) / 2} ${Math.min(b, d) - 10} ${c} ${d}`} stroke="#a85f5a" strokeWidth={1.6} fill="none" opacity={0.6} />)}
        {/* pilor halkası */}
        <path d="M296 238 L296 262" stroke="#7a2e26" strokeWidth={5} strokeLinecap="round" />
      </g>
      <g {...o('nd-mide-sivi')}>
        {/* sıvı mide biçiminde açık yol (clipPath Lottie'ye geçmiyor, dikdörtgen taşıyordu — 2026-11-05); yüzey yatay y 256 */}
        <path className="boya" d="M560 256 C554 272 542 286 524 298 C476 336 396 332 352 302 C334 290 318 272 304 264 L294 262 L294 256 Z" fill="#d9a441" fillOpacity={0.45} />
        <path d="M294 256 L560 256" stroke="#a87a22" strokeWidth={2.5} />
      </g>
      <g {...o('nd-beslenme')}>
        {/* ince yumuşak sonda + içinde kılavuz tel; uç pilorun hemen ötesinde, duodenum başlangıcında */}
        <path d="M437 0 L437 122 C430 190 420 270 380 290 C350 300 320 270 296 252 L278 250" stroke="#6b7a90" strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path className="cz boya-cizgi" pathLength={1} d="M437 0 L437 122 C430 190 420 270 380 290 C350 300 320 270 296 252 L278 250" stroke="#f3f6fa" strokeWidth={3} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M437 0 L437 122 C430 190 420 270 380 290 C350 300 320 270 296 252 L282 250.5" stroke="#2b3440" strokeWidth={1.1} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('nd-sonda')}>
        <Sonda w={9} cz d={IC_SONDA} />
        {[262, 276].map((y) => <ellipse key={y} cx={447.6} cy={y} rx={1.6} ry={3} fill={SONDA_K} />)}
        {/* aynı sondanın burundan sarkan dış ucu (karın dışında) + bağlantı hunisi */}
        <Sonda w={9} d={DIS_UC} />
        <path d="M674 150 L686 150 L690 168 L670 168 Z" fill="#c9d3df" stroke={SONDA_K} strokeWidth={2} strokeLinejoin="round" />
      </g>
      <g {...o('nd-su')}>
        <path className="cz kmb-akis boya-cizgi" pathLength={1} d={`M680 168 L680 0 M${IC_SONDA.slice(1)}`} stroke="#3b8fd6" strokeWidth={3} fill="none" strokeLinecap="round" />
        <path d="M448 294 C444 304 452 312 448 320" stroke="#3b8fd6" strokeWidth={3} fill="none" strokeLinecap="round" opacity={0.8} />
      </g>
      <g {...o('nd-hava')}>
        {[[452, 270, 4], [458, 252, 3.2], [442, 258, 2.6], [462, 286, 2.4]].map(([x, y, r]) => <circle className="boya" key={`${x}${y}`} cx={x} cy={y} r={r} fill="#ffffff" fillOpacity={0.85} stroke="#1f4e79" strokeWidth={1.2} />)}
      </g>
      <g {...o('nd-stetoskop')}>
        <path d="M400 126 C392 92 346 92 312 64" stroke="#2b3440" strokeWidth={6} fill="none" strokeLinecap="round" />
        <path d="M312 64 C298 52 290 36 290 16 M312 64 C324 50 332 34 334 16" stroke="#8a96a6" strokeWidth={4} fill="none" strokeLinecap="round" />
        <circle cx={290} cy={14} r={5} fill="#2b3440" />
        <circle cx={334} cy={14} r={5} fill="#2b3440" />
        <circle className="boya" cx={400} cy={150} r={24} fill="url(#kmb-2b-metal)" stroke="#5b6676" strokeWidth={2.5} />
        <circle cx={400} cy={150} r={17} fill="#eef1f5" stroke="#8a96a6" strokeWidth={1.5} />
      </g>
      <g {...o('nd-ses')}>
        {[36, 48, 60].map((r) => <path key={r} className="boya-cizgi" d={`M${400 - r * 0.6} ${150 - r * 0.8} Q${400 - r * 1.25} 150 ${400 - r * 0.6} ${150 + r * 0.8}`} stroke="#2e9e5b" strokeWidth={2.5} fill="none" strokeLinecap="round" />)}
      </g>
      <g {...o('nd-torba')}>
        <Sonda w={8} d="M680 166 C682 190 730 190 750 230 C760 260 752 300 748 340" />
        <path className="boya" d="M712 340 L784 340 C790 340 792 346 792 352 L790 458 C790 466 784 472 776 472 L720 472 C712 472 706 466 706 458 L704 352 C704 346 706 340 712 340 Z" fill="#eef4fa" fillOpacity={0.9} stroke="#6b7a90" strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M708 420 L790 420 L790 458 C790 466 784 472 776 472 L720 472 C712 472 706 466 706 458 Z" fill="#d9a441" fillOpacity={0.5} />
        <path d="M707 420 L790 420" stroke="#a87a22" strokeWidth={2} />
        {[360, 380, 400].map((y) => <path key={y} d={`M776 ${y} L788 ${y}`} stroke="#6b7a90" strokeWidth={1.4} />)}
      </g>
      <g {...o('nd-akis')}>
        <path className="cz kmb-akis boya-cizgi" pathLength={1} d={`M448 292 C446 230 444 170 443 122 L443 0 M680 0 L680 150 C682 190 730 190 750 230 C760 260 752 300 748 340`} stroke="#d9a441" strokeWidth={3} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('nd-enjektor')}>
        <Enjektor x={680} y={164} />
      </g>
      <g {...o('nd-tipa')}>
        <rect className="boya" x={671} y={164} width={18} height={14} rx={4} fill="#3f6f9c" stroke="#24476a" strokeWidth={2} />
        <path d="M689 170 C700 170 702 160 694 154" stroke="#3f6f9c" strokeWidth={2.5} fill="none" strokeLinecap="round" />
      </g>
    </>
  ),
};

export const SAHNELER_NG_B: Record<string, Sahne> = {
  'ng-govde': NgGovde,
  'ng-mide': NgMide,
};
