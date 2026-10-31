/** KMB 2B düz çizgi film sahneleri — grup C: dış görünüm, eller, pozisyon (docs/KMB_2B_STIL.md).
 *  Sahne anahtarları ve öge kimlikleri SAHNE_OGELERI ile birebir aynı; sahneler.tsx bu kaydı eskinin ÜSTÜNE serer.
 *  Dil: iki duraklı yumuşak degrade (`kmb-2b-…`, sahneOrtak Ortak) ya da düz renk, 2–3 px sıcak kontur, filtre/gölge yok.
 *  H462: nesneler iç içe geçmez (parmak ucu dokuya DEĞER, gömülmez: uç noktası = temas noktası − yarı kalınlık), el "el" gibi
 *  (avuç + 4 parmak + başparmak + boğum çizgileri), kateter iki çizgili silindir, sıvılar yarı saydam film. */
import React from 'react';
import { type Sahne } from './sahneOrtak';

type Pt = [number, number];
const yol = (pts: Pt[]) => pts.map((p, i) => `${i ? 'L' : 'M'}${p[0]} ${p[1]}`).join(' ');

/** Uzuv / parmak: yuvarlak uçlu kalın kırık çizgi — kontur + düz dolgu + iç noktalarda boğum çizgisi.
 *  (Çizgi tabanlı olduğu için düz renk; bbox'ı sıfır olan düz çizgide degrade çalışmaz.) */
function Uzuv({ pts, w, dolgu, kontur, bogum = true, cls }: { pts: Pt[]; w: number; dolgu: string; kontur: string; bogum?: boolean; cls?: string }) {
  const d = yol(pts);
  return (
    <>
      <path d={d} stroke={kontur} strokeWidth={w + 5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path className={cls} d={d} stroke={dolgu} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      {bogum && pts.slice(1, -1).map(([x, y], i) => {
        const [ax, ay] = pts[i]; const [bx, by] = pts[i + 2];
        const dx = bx - ax, dy = by - ay; const L = Math.hypot(dx, dy) || 1;
        const nx = (-dy / L) * w * 0.34, ny = (dx / L) * w * 0.34;
        return <path key={i} d={`M${x + nx} ${y + ny} Q${x + (dx / L) * w * 0.14} ${y + (dy / L) * w * 0.14} ${x - nx} ${y - ny}`} stroke={kontur} strokeWidth={2} fill="none" opacity={0.7} strokeLinecap="round" />;
      })}
    </>
  );
}

/** İki çizgili lateks kateter (koyu kontur + açık gövde = silindir). `cz` ile çizilebilir. */
function Kateter2({ d, w = 9, cz = false, cls = 'boya-cizgi', renk = '#f3bd4e' }: { d: string; w?: number; cz?: boolean; cls?: string; renk?: string }) {
  return (
    <>
      <path d={d} stroke="#b47a1a" strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path className={`${cz ? 'cz ' : ''}${cls}`} pathLength={cz ? 1 : undefined} d={d} stroke={renk} strokeWidth={w * 0.7} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </>
  );
}

/** Dıştan içe değil, merkezden DIŞA tek yönlü spiral (antiseptik silme izi). sx: yatay basıklık. */
function spiral(cx: number, cy: number, r0: number, dr: number, tur: number, sx: number, n = 140): string {
  const pts: Pt[] = [];
  for (let i = 0; i <= n; i++) {
    const t = (i / n) * tur; const r = r0 + dr * t; const a = -Math.PI / 2 + t * Math.PI * 2;
    pts.push([Math.round((cx + sx * r * Math.cos(a)) * 10) / 10, Math.round((cy + r * Math.sin(a)) * 10) / 10]);
  }
  return yol(pts);
}

const DERI = 'url(#kmb-2b-deri)', DERI_K = 'url(#kmb-2b-deri-koyu)', KONTUR_DERI = '#b9805a';
const STERIL = '#f6ecda', STERIL_K = '#b59c72';
const NITRIL = '#cfe3f4', NITRIL_K = '#3f6f9c';

// ———————————————————————————————————————————————————————— KADIN (litotomide, önden)

/** Kadın dış genital bölge: hasta litotomide, kamera perineye önden bakar (üst = simfiz/mons, alt = anüs).
 *  Dizilim yukarıdan aşağı: mons → klitoris (başlık altında) → meatus (küçük, üstte) → vajina girişi (geniş, altta) → perine → anüs.
 *  Ölçek ≈ 1 cm 26 px (vulva ~14 cm uzun). Eller/küvet örtü ve uyluğun ÜSTÜNDE katmanlanır, dokuya gömülmez. */
const Kadin: Sahne = {
  ad: 'Kadın dış genital bölge (litotomide, önden)',
  gizli: ['k-temizlik', 'k-ortu', 'k-halka', 'k-kateter', 'k-idrar'],
  etiket: {
    'k-majus': [150, 130, 'Labium majus'],
    'k-minus': [190, 230, 'Labium minus'],
    'k-klitoris': [560, 118, 'Klitoris'],
    'k-meatus': [575, 205, 'Eksternal üretra ağzı (meatus)'],
    'k-vajina': [560, 300, 'Vajina girişi'],
    'k-ortu': [150, 470, 'Steril delikli örtü'],
  },
  Ciz: ({ o }) => (
    <>
      {/* zemin: alt karın / perine derisi (açık tek renk); uyluklar iki yandan üstüne biner */}
      <rect x={0} y={0} width={800} height={500} fill={DERI} />
      {/* uyluklar (iç yüzleri perineye bakar; kasık kıvrımı kontur) */}
      <path d="M0 30 C140 40 240 150 268 300 C284 390 268 460 250 500 L0 500 Z" fill={DERI} stroke={KONTUR_DERI} strokeWidth={2.5} strokeLinejoin="round" />
      <path d="M800 30 C660 40 560 150 532 300 C516 390 532 460 550 500 L800 500 Z" fill={DERI} stroke={KONTUR_DERI} strokeWidth={2.5} strokeLinejoin="round" />
      {/* mons pubis */}
      <path d="M290 40 C330 8 470 8 510 40 C530 70 512 100 482 108 L318 108 C288 100 270 70 290 40 Z" fill={DERI_K} stroke={KONTUR_DERI} strokeWidth={2.5} strokeLinejoin="round" />
      <g {...o('k-majus')}>
        <path className="boya" d="M400 86 C318 90 280 180 284 300 C288 390 334 450 400 454 C466 450 512 390 516 300 C520 180 482 90 400 86 Z" fill={DERI_K} stroke={KONTUR_DERI} strokeWidth={3} strokeLinejoin="round" />
        <path d="M326 150 C306 220 306 320 330 400" stroke={KONTUR_DERI} strokeWidth={2} fill="none" opacity={0.45} />
        <path d="M474 150 C494 220 494 320 470 400" stroke={KONTUR_DERI} strokeWidth={2} fill="none" opacity={0.45} />
      </g>
      {/* vestibül zemini (mukoza) */}
      <path d="M400 128 C352 134 336 220 344 310 C350 370 374 404 400 406 C426 404 450 370 456 310 C464 220 448 134 400 128 Z" fill="url(#kmb-2b-mukoza)" stroke="#a85f5a" strokeWidth={2} />
      <g {...o('k-minus')}>
        <path className="boya" d="M400 126 C360 130 336 200 338 290 C340 350 362 396 392 406 C372 376 362 330 362 280 C362 210 376 160 400 142 Z" fill="#e49a93" stroke="#a85f5a" strokeWidth={2.2} strokeLinejoin="round" />
        <path className="boya" d="M400 126 C440 130 464 200 462 290 C460 350 438 396 408 406 C428 376 438 330 438 280 C438 210 424 160 400 142 Z" fill="#e49a93" stroke="#a85f5a" strokeWidth={2.2} strokeLinejoin="round" />
        <path d="M350 200 C346 250 348 300 356 350 M450 200 C454 250 452 300 444 350" stroke="#f6c9c3" strokeWidth={2} fill="none" opacity={0.85} />
      </g>
      <g {...o('k-klitoris')}>
        {/* başlık (prepisyum) üstte, glans altından görünür */}
        <path d="M378 146 C384 126 416 126 422 146 C412 154 388 154 378 146 Z" fill="#d9928c" stroke="#a85f5a" strokeWidth={2} strokeLinejoin="round" />
        <circle className="boya" cx={400} cy={156} r={7.5} fill="#c9736e" stroke="#a85f5a" strokeWidth={2} />
      </g>
      <g {...o('k-meatus')}>
        <ellipse cx={400} cy={212} rx={11} ry={9} fill="#f0b4ae" stroke="#d08a85" strokeWidth={1.5} />
        <path className="boya" d="M400 204 C396 207 396 217 400 220 C404 217 404 207 400 204 Z" fill="#7d2f2a" />
      </g>
      <g {...o('k-vajina')}>
        <path className="boya" d="M400 250 C372 256 364 300 368 334 C372 362 388 378 400 378 C412 378 428 362 432 334 C436 300 428 256 400 250 Z" fill="#8f3c3a" stroke="#c9827c" strokeWidth={4} />
        {[[384, 290], [416, 290], [380, 322], [420, 322], [390, 352], [410, 352]].map(([x, y]) => <path key={`${x}${y}`} d={`M${x - 5} ${y} q5 5 10 0`} stroke="#d9928c" strokeWidth={2} fill="none" />)}
      </g>
      {/* perine (fourchette altı) + anüs */}
      <path d="M386 416 C394 422 406 422 414 416" stroke={KONTUR_DERI} strokeWidth={2} fill="none" strokeLinecap="round" />
      <circle cx={400} cy={468} r={11} fill="#a0674e" stroke="#7d4a36" strokeWidth={2} />
      {[0, 45, 90, 135, 180, 225, 270, 315].map((a) => <path key={a} d={`M${400 + Math.cos(a * Math.PI / 180) * 6} ${468 + Math.sin(a * Math.PI / 180) * 6} l${Math.cos(a * Math.PI / 180) * 7} ${Math.sin(a * Math.PI / 180) * 7}`} stroke="#7d4a36" strokeWidth={1.4} strokeLinecap="round" />)}
      <g {...o('k-temizlik')}>
        {/* antiseptik filmi (yarı saydam, geniş) + meatustan dışa tek yönlü silme yolu (ok) */}
        <path d={spiral(400, 240, 26, 48, 2.5, 0.72)} stroke="#c9772b" strokeOpacity={0.3} strokeWidth={16} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path className="cz boya-cizgi" pathLength={1} d={spiral(400, 240, 26, 48, 2.5, 0.72)} stroke="#2e9e5b" strokeWidth={3.5} fill="none" strokeLinecap="round" strokeLinejoin="round" markerEnd="url(#kmb-ok)" />
      </g>
      <g {...o('k-ortu')}>
        <path className="boya" d="M0 0 H800 V500 H0 Z M400 60 C290 66 262 200 266 300 C270 400 320 476 400 480 C480 476 530 400 534 300 C538 200 510 66 400 60 Z" fill="url(#kmb-2b-ortu)" fillRule="evenodd" stroke="#2f6f5f" strokeWidth={2.5} />
        {/* kıvrımlar */}
        {[90, 170, 630, 710].map((x) => <path key={x} d={`M${x} 40 C${x - 10} 180 ${x + 8} 320 ${x - 6} 470`} stroke="#2f6f5f" strokeWidth={1.6} fill="none" opacity={0.45} />)}
        <path d="M400 60 C290 66 262 200 266 300 C270 400 320 476 400 480 C480 476 530 400 534 300 C538 200 510 66 400 60 Z" fill="none" stroke="#dff1ea" strokeWidth={3} />
      </g>
      <g {...o('k-halka')}>
        {/* steril eldivenli el (avuç yukarı), sağ kenardan; avuçta halka hâlinde kateter, altından drenaj ucu sarkar */}
        <path d="M800 288 L742 282" stroke={STERIL_K} strokeWidth={75} strokeLinecap="butt" />
        <path d="M800 288 L742 282" stroke={STERIL} strokeWidth={70} strokeLinecap="butt" />
        <path d="M652 292 C662 268 698 258 738 266 L748 268 C772 274 778 306 772 340 C768 372 744 394 708 398 C676 400 652 384 646 356 C640 334 642 312 652 292 Z" fill="url(#kmb-2b-eldiven-steril)" stroke={STERIL_K} strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M672 300 C690 290 720 290 740 300 M662 350 C690 340 720 342 752 352" stroke={STERIL_K} strokeWidth={1.6} fill="none" opacity={0.5} />
        {/* parmaklar: avucun sol-üst kenarından dışa, hafif kıvrık */}
        <Uzuv pts={[[668, 288], [640, 252], [630, 218]]} w={22} dolgu={STERIL} kontur={STERIL_K} />
        <Uzuv pts={[[692, 272], [672, 232], [668, 198]]} w={23} dolgu={STERIL} kontur={STERIL_K} />
        <Uzuv pts={[[718, 266], [708, 226], [712, 194]]} w={23} dolgu={STERIL} kontur={STERIL_K} />
        <Uzuv pts={[[744, 270], [746, 236], [756, 210]]} w={20} dolgu={STERIL} kontur={STERIL_K} />
        {/* halka (ciz): iki tur */}
        <circle cx={700} cy={334} r={36} stroke="#b47a1a" strokeWidth={9} fill="none" />
        <circle className="cz boya-cizgi" pathLength={1} cx={700} cy={334} r={36} stroke="#f3bd4e" strokeWidth={6.3} fill="none" />
        <circle cx={700} cy={334} r={26} stroke="#b47a1a" strokeWidth={9} fill="none" />
        <circle className="cz boya-cizgi" pathLength={1} cx={700} cy={334} r={26} stroke="#f3bd4e" strokeWidth={6.3} fill="none" />
        {/* drenaj ucu avuç kenarından aşağı sarkar */}
        <Kateter2 d="M700 370 C702 404 724 424 736 452" />
        {/* başparmak avucun alt-sol kenarından halkanın üstüne basar (halkadan SONRA çizilir → üstte) */}
        <Uzuv pts={[[652, 372], [640, 336], [664, 312]]} w={24} dolgu={STERIL} kontur={STERIL_K} />
      </g>
      <g {...o('k-kateter')}>
        <Kateter2 d="M672 306 C620 244 520 212 403 212" cz />
      </g>
      <g {...o('k-idrar')}>
        {/* böbrek küvet (drenaj ucunun altında) */}
        <path d="M690 462 C704 454 776 454 790 462 C796 472 788 484 774 484 L706 484 C692 484 684 472 690 462 Z" fill="url(#kmb-2b-kuvet)" stroke="#1f4e79" strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M700 474 C720 470 760 470 780 474 L776 480 L704 480 Z" fill="#efc53f" opacity={0.85} />
        {/* lümende ince sarı akış: meatus → halka → drenaj ucu → damla */}
        <path className="cz kmb-akis boya-cizgi" pathLength={1} d="M403 212 C520 212 620 244 672 306 A36 36 0 1 1 700 370 C702 404 724 424 736 452" stroke="#efc53f" strokeWidth={2.4} fill="none" strokeLinecap="round" />
        <ellipse cx={737} cy={458} rx={2.6} ry={4} fill="#efc53f" />
      </g>
    </>
  ),
};

// ———————————————————————————————————————————————————————— YAKIN KADIN (vestibül)

/** Vestibül yakın planı: labia minora iki yandan eldivenli başparmak + işaret parmağıyla ayrılmış; üstte klitoris,
 *  altında küçük meatus, en altta geniş vajina girişi. Ölçek ≈ 1 cm 70 px (meatus ~6 mm → slit 40 px; 16 Fr kateter 13 px gövde). */
const YakinKadin: Sahne = {
  ad: 'Yakın plan: vestibül ve meatus (eldivenli parmaklar labiaları ayırıyor)',
  gizli: ['v-kateter', 'v-jel', 'v-idrar', 'v-parmak'],
  etiket: {
    'v-klitoris': [400, 40, 'Klitoris'],
    'v-meatus': [580, 215, 'Meatus: üstteki küçük açıklık'],
    'v-vajina': [570, 330, 'Vajina: alttaki geniş açıklık'],
    'v-minus': [140, 250, 'Labium minus'],
    'v-parmak': [140, 450, 'Başparmak + işaret parmağı ayırır'],
    'v-jel': [600, 60, 'Uçta ~2 mL jel'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill={DERI} />
      {/* labia majora iç yüzleri (iki yanda koyu deri kıvrımı) */}
      <path d="M0 0 L200 0 C150 120 150 300 210 500 L0 500 Z" fill={DERI_K} stroke={KONTUR_DERI} strokeWidth={2.5} />
      <path d="M800 0 L600 0 C650 120 650 300 590 500 L800 500 Z" fill={DERI_K} stroke={KONTUR_DERI} strokeWidth={2.5} />
      {/* vestibül zemini */}
      <path d="M400 0 C250 20 200 200 215 330 C228 440 300 500 400 500 C500 500 572 440 585 330 C600 200 550 20 400 0 Z" fill="url(#kmb-2b-mukoza)" />
      <g {...o('v-minus')}>
        <path className="boya" d="M400 0 C330 10 262 120 248 240 C236 350 270 440 330 500 L250 500 C196 410 188 240 236 118 C272 44 330 0 400 0 Z" fill="#e49a93" stroke="#a85f5a" strokeWidth={3} strokeLinejoin="round" />
        <path className="boya" d="M400 0 C470 10 538 120 552 240 C564 350 530 440 470 500 L550 500 C604 410 612 240 564 118 C528 44 470 0 400 0 Z" fill="#e49a93" stroke="#a85f5a" strokeWidth={3} strokeLinejoin="round" />
        <path d="M262 120 C222 220 222 340 270 450 M538 120 C578 220 578 340 530 450" stroke="#f6c9c3" strokeWidth={3} fill="none" opacity={0.85} />
      </g>
      <g {...o('v-klitoris')}>
        <path d="M335 0 C345 44 455 44 465 0 Z" fill="#d9928c" stroke="#a85f5a" strokeWidth={2.5} strokeLinejoin="round" />
        <ellipse className="boya" cx={400} cy={62} rx={16} ry={14} fill="#c9736e" stroke="#a85f5a" strokeWidth={2.5} />
      </g>
      <g {...o('v-meatus')}>
        <ellipse cx={400} cy={170} rx={34} ry={26} fill="#f3bfb9" stroke="#d08a85" strokeWidth={2} />
        <path className="boya" d="M400 150 C390 158 390 182 400 190 C410 182 410 158 400 150 Z" fill="#6e2420" />
      </g>
      <g {...o('v-vajina')}>
        <path className="boya" d="M400 240 C320 246 300 330 310 400 C320 460 360 490 400 492 C440 490 480 460 490 400 C500 330 480 246 400 240 Z" fill="#7d2f2d" stroke="#d08a85" strokeWidth={6} />
        {Array.from({ length: 8 }, (_, i) => <path key={i} d={`M${338 + (i % 4) * 36} ${300 + Math.floor(i / 4) * 80} q10 14 0 28`} stroke="#a64c48" strokeWidth={2.5} fill="none" />)}
      </g>
      <g {...o('v-parmak')}>
        {/* başparmak (sol alt) ve işaret parmağı (sağ alt): uç, labium minusun dış kenarına basar (temas, gömülme yok) */}
        <Uzuv pts={[[60, 500], [150, 410], [222, 334]]} w={76} dolgu={STERIL} kontur={STERIL_K} cls="boya-cizgi" />
        <Uzuv pts={[[740, 500], [650, 410], [578, 334]]} w={70} dolgu={STERIL} kontur={STERIL_K} cls="boya-cizgi" />
      </g>
      <g {...o('v-kateter')}>
        <Kateter2 d="M800 70 C690 86 540 130 408 168" w={18} cz />
      </g>
      <g {...o('v-jel')}>
        <ellipse className="boya" cx={446} cy={158} rx={46} ry={17} fill="url(#kmb-2b-jel)" transform="rotate(-16 446 158)" />
      </g>
      <g {...o('v-idrar')}>
        <path className="cz kmb-akis boya-cizgi" pathLength={1} d="M408 168 C540 130 690 86 800 70" stroke="#efc53f" strokeWidth={4} fill="none" strokeLinecap="round" />
      </g>
    </>
  ),
};

// ———————————————————————————————————————————————————————— YAKIN ERKEK JEL (glans, yandan)

/** Glans yakın planı (yandan; şaft solda, meatus sağ uçta). Ölçek ≈ 1 cm 85 px. Prepisyum korona arkasına geri çekilmiş,
 *  jel aplikatörü (şırınga: konik uç + gövde + piston) meatusta; baş + işaret parmağı glansı meatusun arkasından sıkar
 *  (parmak uçları glans konturuna DEĞER, içine girmez). */
const YakinErkekJel: Sahne = {
  ad: 'Yakın plan: glans, meatus ve lidokainli jelin verilmesi',
  gizli: ['j-temizlik', 'j-siringa', 'j-dolum', 'j-parmak'],
  etiket: {
    'j-glans': [290, 60, 'Glans penis'],
    'j-prepisyum': [110, 120, 'Prepisyum geri çekilir'],
    'j-meatus': [560, 160, 'Meatus'],
    'j-temizlik': [620, 420, 'Meatustan dışa, 3 kez'],
    'j-siringa': [660, 90, 'Jel tüpü meatusta'],
    'j-dolum': [160, 450, 'Jel üretrayı doldurur'],
    'j-parmak': [400, 470, 'Ucu sık, 2–3 dk bekle'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* şaft (silindir: üstte açık, altta koyu) */}
      <path d="M0 150 L230 146 L230 354 L0 350 Z" fill={DERI} stroke={KONTUR_DERI} strokeWidth={2.5} strokeLinejoin="round" />
      <path d="M8 176 L222 172" stroke="#f9ddc4" strokeWidth={6} strokeLinecap="round" opacity={0.9} />
      <g {...o('j-prepisyum')}>
        <path className="boya" d="M198 132 C240 116 286 124 292 150 L292 350 C286 376 240 384 198 368 C214 330 214 170 198 132 Z" fill={DERI_K} stroke={KONTUR_DERI} strokeWidth={2.5} strokeLinejoin="round" />
        {[170, 212, 254, 296, 338].map((y) => <path key={y} d={`M214 ${y} q22 7 56 0`} stroke={KONTUR_DERI} strokeWidth={1.6} fill="none" opacity={0.6} />)}
      </g>
      <g {...o('j-glans')}>
        <path className="boya" d="M268 118 C420 86 562 158 572 250 C562 342 420 414 268 382 C248 330 248 170 268 118 Z" fill="url(#kmb-2b-mukoza)" stroke="#a85f5a" strokeWidth={3} strokeLinejoin="round" />
        <path d="M278 136 C298 200 298 300 278 364" stroke="#a85f5a" strokeWidth={2.5} fill="none" opacity={0.6} />
        <path d="M310 144 C400 118 490 150 536 206" stroke="#f8d5d1" strokeWidth={5} fill="none" strokeLinecap="round" opacity={0.9} />
      </g>
      <g {...o('j-dolum')}>
        <path className="cz boya-cizgi" pathLength={1} d="M556 250 L0 250" stroke="#8fc7ff" strokeOpacity={0.6} strokeWidth={22} fill="none" />
      </g>
      <g {...o('j-meatus')}>
        <path className="boya" d="M566 226 C556 238 556 262 566 274 C574 262 574 238 566 226 Z" fill="#6e2420" />
      </g>
      <g {...o('j-temizlik')}>
        {/* üç silme: meatustan dışa (yukarı, geriye, aşağı); yarı saydam antiseptik filmi + yön çizgisi */}
        {['M556 236 C520 180 460 140 380 128', 'M552 248 C500 218 420 206 330 212', 'M556 264 C520 320 460 360 380 372'].map((d) => <path key={d} d={d} stroke="#c9772b" strokeOpacity={0.3} strokeWidth={18} fill="none" strokeLinecap="round" />)}
        {['M556 236 C520 180 460 140 380 128', 'M552 248 C500 218 420 206 330 212', 'M556 264 C520 320 460 360 380 372'].map((d) => <path key={d} className="cz boya-cizgi" pathLength={1} d={d} stroke="#2e9e5b" strokeWidth={3.5} fill="none" strokeLinecap="round" markerEnd="url(#kmb-ok)" />)}
      </g>
      <g {...o('j-siringa')}>
        {/* konik uç meatusta → gövde (içinde jel) → flanş → piston */}
        <path className="boya" d="M568 244 L606 234 L606 266 L568 256 Z" fill="#c9d3de" stroke="#6b7a90" strokeWidth={2} strokeLinejoin="round" />
        <rect x={604} y={230} width={144} height={40} rx={6} fill="url(#kmb-2b-plastik)" stroke="#6b7a90" strokeWidth={2.2} />
        <rect x={610} y={236} width={94} height={28} rx={3} fill="#bfe0ff" opacity={0.75} />
        <rect x={704} y={234} width={6} height={32} fill="#6b7a90" />
        <rect x={744} y={218} width={8} height={64} rx={2} fill="#6b7a90" />
        <rect x={752} y={243} width={36} height={14} rx={2} fill="#c9d3de" stroke="#6b7a90" strokeWidth={1.6} />
        <rect x={786} y={228} width={8} height={44} rx={2} fill="#6b7a90" />
        <text x={657} y={254} fontSize={11} textAnchor="middle" fill="#3e4a58">lidokain jel</text>
      </g>
      <g {...o('j-parmak')}>
        {/* başparmak üstten, işaret parmağı alttan: uçlar glans konturuna değer (kontur y≈150 / 350 @x≈510, yarı kalınlık 33) */}
        <Uzuv pts={[[522, -40], [514, 50], [510, 117]]} w={66} dolgu={NITRIL} kontur={NITRIL_K} cls="boya-cizgi" />
        <Uzuv pts={[[522, 540], [514, 450], [510, 383]]} w={66} dolgu={NITRIL} kontur={NITRIL_K} cls="boya-cizgi" />
      </g>
    </>
  ),
};

// ———————————————————————————————————————————————————————— YAKIN EL (steril eldiven, avuçta halka)

/** Steril eldivenli (sol) el avuç yukarı; avuçta halka hâlinde kateter, yalnız uç parmakların üstünden dışarı.
 *  Ölçek ≈ 1 cm 28 px (avuç ~10 cm, 16 Fr kateter 15 px gövde). Sağ-alt yeşil steril alan; sarkan kateter sola, alanın dışına değer. */
const YakinEl: Sahne = {
  ad: 'Yakın plan: steril eldivenle kateteri avuçta toplamak',
  gizli: ['h-yanlis', 'h-jel'],
  etiket: {
    'h-el': [120, 60, 'Steril eldivenli el'],
    'h-halka': [400, 60, 'Kateter avuçta halka halinde'],
    'h-uc': [660, 350, 'Yalnız uç dışarıda, steril'],
    'h-yanlis': [470, 470, 'Sarkan kateter dokunur → steril değil'],
    'h-jel': [690, 232, 'Uca jel'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* masa + steril örtü (sağ alt) */}
      <rect x={0} y={380} width={800} height={120} fill="#e6ecf2" />
      <path d="M330 384 C390 376 450 392 520 384 C590 376 650 392 720 384 C760 378 780 388 800 384 L800 500 L330 500 Z" fill="url(#kmb-2b-ortu)" stroke="#2f6f5f" strokeWidth={2.5} strokeLinejoin="round" />
      <path d="M330 384 L330 500" stroke="#2f6f5f" strokeWidth={2.5} />
      <g {...o('h-el')}>
        {/* ön kol (eldiven manşeti) sol alttan */}
        <Uzuv pts={[[40, 500], [190, 392]]} w={108} dolgu={STERIL} kontur={STERIL_K} bogum={false} />
        <path d="M150 412 L198 348" stroke={STERIL_K} strokeWidth={2} opacity={0.5} />
        {/* avuç */}
        <path className="boya" d="M190 380 C170 330 190 250 250 220 C300 196 360 196 400 226 C440 250 470 300 470 340 C470 380 440 410 400 420 C330 436 240 440 190 380 Z" fill="url(#kmb-2b-eldiven-steril)" stroke={STERIL_K} strokeWidth={3} strokeLinejoin="round" />
        <path d="M232 262 C280 300 330 340 380 400 M214 300 C250 340 300 380 340 416" stroke={STERIL_K} strokeWidth={1.8} fill="none" opacity={0.45} />
        {/* 4 parmak (işaret → serçe) avucun sağ-üst kenarından, hafif kıvrık; boğum çizgileri */}
        <Uzuv pts={[[400, 228], [470, 170], [540, 128]]} w={46} dolgu={STERIL} kontur={STERIL_K} />
        <Uzuv pts={[[430, 250], [510, 196], [588, 162]]} w={46} dolgu={STERIL} kontur={STERIL_K} />
        <Uzuv pts={[[450, 290], [530, 256], [606, 232]]} w={44} dolgu={STERIL} kontur={STERIL_K} />
        <Uzuv pts={[[456, 330], [520, 320], [574, 314]]} w={38} dolgu={STERIL} kontur={STERIL_K} />
        {/* başparmak avucun solundan yukarı */}
        <Uzuv pts={[[232, 250], [216, 180], [236, 118]]} w={54} dolgu={STERIL} kontur={STERIL_K} />
      </g>
      <g {...o('h-halka')}>
        {[62, 47, 32].map((r) => <circle key={r} cx={330} cy={322} r={r} stroke="#b47a1a" strokeWidth={15} fill="none" />)}
        {[62, 47, 32].map((r) => <circle key={r} className="cz boya-cizgi" pathLength={1} cx={330} cy={322} r={r} stroke="#f3bd4e" strokeWidth={10.5} fill="none" />)}
      </g>
      <g {...o('h-uc')}>
        {/* uç halkadan çıkar, parmakların üstünden sağa uzanır; yuvarlak uç + drenaj gözü */}
        <Kateter2 d="M388 296 C470 262 560 262 652 280" w={15} />
        <circle className="boya" cx={652} cy={280} r={7.5} fill="#f3bd4e" stroke="#b47a1a" strokeWidth={2.2} />
        <ellipse cx={632} cy={274} rx={5} ry={3} fill="#5a3a10" />
      </g>
      <g {...o('h-jel')}>
        <ellipse className="boya" cx={626} cy={280} rx={42} ry={16} fill="url(#kmb-2b-jel)" transform="rotate(8 626 280)" />
      </g>
      <g {...o('h-yanlis')}>
        {/* sarkan kateter avuç kenarından aşağı sola, örtünün dışındaki masaya değer → kırmızı çarpı */}
        <Kateter2 d="M318 384 C304 424 284 448 254 468" w={15} />
        <path d="M236 450 L272 486 M272 450 L236 486" stroke="#d23b3b" strokeWidth={7} strokeLinecap="round" />
        <circle cx={254} cy={468} r={28} stroke="#d23b3b" strokeWidth={4} fill="none" strokeDasharray="8 6" />
      </g>
    </>
  ),
};

// ———————————————————————————————————————————————————————— POZİSYON (üstten)

/** Yatan hasta üstten: baş solda, önlüklü gövde, kollar iki yanda, bacaklar sağa (sahne özelinde eklenir). */
function YatanHasta({ y, kadin = false }: { y: number; kadin?: boolean }) {
  return (
    <g>
      {/* kollar (gövdenin altında kalan kısımları gizlenir: önce çizilir) */}
      <Uzuv pts={[[246, y - 36], [396, y - 40]]} w={14} dolgu="#f0bf9a" kontur={KONTUR_DERI} bogum={false} />
      <Uzuv pts={[[246, y + 36], [396, y + 40]]} w={14} dolgu="#f0bf9a" kontur={KONTUR_DERI} bogum={false} />
      <circle cx={404} cy={y - 40} r={8} fill="#f0bf9a" stroke={KONTUR_DERI} strokeWidth={2} />
      <circle cx={404} cy={y + 40} r={8} fill="#f0bf9a" stroke={KONTUR_DERI} strokeWidth={2} />
      {/* boyun + baş */}
      <rect x={222} y={y - 10} width={16} height={20} fill="#f0bf9a" stroke={KONTUR_DERI} strokeWidth={2} />
      <circle cx={205} cy={y} r={24} fill={DERI} stroke={KONTUR_DERI} strokeWidth={2.5} />
      <path d={kadin ? `M181 ${y - 4} C182 ${y - 34} 228 ${y - 34} 229 ${y - 4} C222 ${y - 20} 190 ${y - 20} 181 ${y - 4} Z M181 ${y - 4} C176 ${y + 10} 178 ${y + 24} 186 ${y + 28} C182 ${y + 14} 182 ${y + 4} 181 ${y - 4} Z` : `M182 ${y - 8} C186 ${y - 32} 224 ${y - 32} 228 ${y - 8} C218 ${y - 20} 192 ${y - 20} 182 ${y - 8} Z`} fill={kadin ? '#5a3a24' : '#3b2a1e'} />
      {/* önlük */}
      <path className="boya" d={`M234 ${y - 30} L420 ${y - 32} C432 ${y - 32} 436 ${y + 32} 420 ${y + 32} L234 ${y + 30} C224 ${y + 20} 224 ${y - 20} 234 ${y - 30} Z`} fill="url(#kmb-2b-onluk)" stroke="#3f7680" strokeWidth={2.5} strokeLinejoin="round" />
      <path d={`M240 ${y - 20} C250 ${y - 6} 250 ${y + 6} 240 ${y + 20}`} stroke="#3f7680" strokeWidth={1.8} fill="none" opacity={0.6} />
    </g>
  );
}

/** Ayakta figür (önden), başı (0,0)'da; toplam yükseklik ≈ 242 (−28 … +214). `olcek` ile küçültülür. */
function Figur({ x, y, olcek = 1, giysi, kontur, sac, stetoskop = false }: { x: number; y: number; olcek?: number; giysi: string; kontur: string; sac: string; stetoskop?: boolean }) {
  return (
    <g transform={`translate(${x} ${y}) scale(${olcek})`}>
      {/* kollar (giysiyle aynı renk kol, uçta el) */}
      <Uzuv pts={[[-34, 54], [-44, 130]]} w={20} dolgu={giysi} kontur={kontur} bogum={false} />
      <Uzuv pts={[[34, 54], [44, 130]]} w={20} dolgu={giysi} kontur={kontur} bogum={false} />
      <circle cx={-46} cy={142} r={9} fill="#f0bf9a" stroke={KONTUR_DERI} strokeWidth={2} />
      <circle cx={46} cy={142} r={9} fill="#f0bf9a" stroke={KONTUR_DERI} strokeWidth={2} />
      {/* pantolon */}
      <path d="M-28 150 L28 150 L24 214 L5 214 L0 172 L-5 214 L-24 214 Z" fill="#4a5566" stroke="#2f3744" strokeWidth={2} strokeLinejoin="round" />
      {/* gövde (giysi) */}
      <path className="boya" d="M-36 56 C-36 36 36 36 36 56 L30 152 L-30 152 Z" fill={giysi} stroke={kontur} strokeWidth={2.5} strokeLinejoin="round" />
      <path d="M0 50 L0 150" stroke={kontur} strokeWidth={1.6} opacity={0.6} />
      {/* boyun + baş + saç */}
      <rect x={-7} y={22} width={14} height={16} fill="#f0bf9a" stroke={KONTUR_DERI} strokeWidth={2} />
      <circle cx={0} cy={0} r={24} fill={DERI} stroke={KONTUR_DERI} strokeWidth={2.5} />
      <path d="M-24 -4 C-22 -30 22 -30 24 -4 C14 -16 -14 -16 -24 -4 Z" fill={sac} />
      {stetoskop && (
        <>
          <path d="M-14 44 C-22 80 -8 104 8 108" stroke="#5b6676" strokeWidth={2.5} fill="none" strokeLinecap="round" />
          <path d="M14 44 C16 70 14 84 8 92" stroke="#5b6676" strokeWidth={2.5} fill="none" strokeLinecap="round" />
          <circle cx={10} cy={112} r={6} fill="#dfe6ee" stroke="#5b6676" strokeWidth={2} />
        </>
      )}
    </g>
  );
}

const Pozisyon: Sahne = {
  ad: 'Mahremiyet ve hasta pozisyonu (üstten)',
  gizli: ['p-paravan', 'p-yardimci', 'p-v'],
  etiket: {
    'p-hekim': [90, 40, 'Hekim: tanıt, anlat, onam al'],
    'p-paravan': [700, 36, 'Paravan / perde'],
    'p-yardimci': [712, 290, 'Yardımcı personel'],
    'p-erkek': [390, 78, 'Erkek: supin'],
    'p-kadin': [390, 278, 'Kadın: modifiye litotomi'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* iki yatak (üstten): çerçeve, döşek, yastık */}
      {[[150, 70, 120], [150, 270, 200]].map(([x, y, h]) => (
        <g key={y}>
          <rect x={x} y={y} width={480} height={h} rx={14} fill="url(#kmb-2b-yatak)" stroke="#4f9aa0" strokeWidth={3} />
          <rect x={x + 14} y={y + h / 2 - 30} width={56} height={60} rx={14} fill="#ffffff" stroke="#4f9aa0" strokeWidth={2} />
        </g>
      ))}
      <g {...o('p-erkek')}>
        {/* supin: iki bacak düz, ayaklar sağda */}
        <Uzuv pts={[[418, 138], [612, 136]]} w={18} dolgu="#f0bf9a" kontur={KONTUR_DERI} bogum={false} />
        <Uzuv pts={[[418, 166], [612, 168]]} w={18} dolgu="#f0bf9a" kontur={KONTUR_DERI} bogum={false} />
        <ellipse cx={624} cy={136} rx={7} ry={11} fill="#e4a57e" stroke={KONTUR_DERI} strokeWidth={2} />
        <ellipse cx={624} cy={168} rx={7} ry={11} fill="#e4a57e" stroke={KONTUR_DERI} strokeWidth={2} />
        <YatanHasta y={152} />
      </g>
      <g {...o('p-kadin')}>
        {/* modifiye litotomi: kalçadan dizler dışa-öne bükük (V), topuklar yatakta */}
        <Uzuv pts={[[418, 356], [516, 296], [598, 350]]} w={20} dolgu="#f0bf9a" kontur={KONTUR_DERI} />
        <Uzuv pts={[[418, 384], [516, 444], [598, 390]]} w={20} dolgu="#f0bf9a" kontur={KONTUR_DERI} />
        <ellipse cx={606} cy={352} rx={8} ry={11} fill="#e4a57e" stroke={KONTUR_DERI} strokeWidth={2} transform="rotate(20 606 352)" />
        <ellipse cx={606} cy={388} rx={8} ry={11} fill="#e4a57e" stroke={KONTUR_DERI} strokeWidth={2} transform="rotate(-20 606 388)" />
        <YatanHasta y={370} kadin />
      </g>
      <g {...o('p-v')}>
        <path className="cz boya-cizgi" pathLength={1} d="M516 296 L438 370 L516 444" stroke="#2f6fd6" strokeWidth={4} fill="none" strokeDasharray="0.03 0.015" strokeLinecap="round" />
        <text x={462} y={376} fontSize={16} fill="#2f6fd6" fontWeight={700}>V</text>
      </g>
      <g {...o('p-hekim')}>
        <Figur x={90} y={120} olcek={0.9} giysi="#ffffff" kontur="#7d8aa0" sac="#3b2a1e" stetoskop />
      </g>
      <g {...o('p-paravan')}>
        {[0, 1, 2].map((i) => (
          <g key={i}>
            <rect className="boya" x={652 + i * 36} y={60 + (i % 2) * 6} width={34} height={190} rx={4} fill="#e8f0f8" stroke="#7d8aa0" strokeWidth={2.5} />
            {[100, 150, 200].map((y) => <path key={y} d={`M${656 + i * 36} ${y} L${682 + i * 36} ${y}`} stroke="#c3cfdc" strokeWidth={1.5} />)}
            <circle cx={660 + i * 36} cy={254} r={4} fill="#7d8aa0" /><circle cx={678 + i * 36} cy={254} r={4} fill="#7d8aa0" />
          </g>
        ))}
        <path className="cz boya-cizgi" pathLength={1} d="M652 60 L758 60 L758 254 L652 254 Z" stroke="#7d8aa0" strokeWidth={2.5} fill="none" />
      </g>
      <g {...o('p-yardimci')}>
        <Figur x={712} y={334} olcek={0.75} giysi="url(#kmb-2b-onluk)" kontur="#3f7680" sac="#5a3a24" />
      </g>
    </>
  ),
};

export const SAHNELER_2B_C: Record<string, Sahne> = { kadin: Kadin, 'yakin-kadin': YakinKadin, 'yakin-erkek-jel': YakinErkekJel, 'yakin-el': YakinEl, pozisyon: Pozisyon };
