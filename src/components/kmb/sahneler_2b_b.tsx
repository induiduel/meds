/**
 * KMB 2B düz çizgi film sahneleri — grup B: iç anatomi (docs/KMB_2B_STIL.md). Sahne adları SAHNELER anahtarlarıyla aynı;
 * sahneler.tsx bu kaydı eskinin ÜSTÜNE serer. Öge kimlikleri ve `gizli` semantiği SAHNE_OGELERI ile birebir aynıdır.
 *
 * Stil: pürüzsüz iki duraklı degrade (`kmb-2b-*`, sahneOrtak.tsx), 2–3 px sıcak kontur, filtre/gölge yok, beyaz zemin.
 * H462: nesneler iç içe geçmez (kateter yalnız lümende, balon duvara gömülmez), ölçek tam gövdede 1 cm ≈ 12 px,
 * yakın planlar kendi ölçeğini tutarlı uygular; sıvılar yarı saydam film/ince çizgi; etiketler çakışmaz.
 */
import React from 'react';
import { type Sahne, u } from './sahneOrtak';

void React;

const DERI_K = '#b9805a';
const KEMIK_K = '#b9a479';

/** İki çizgili silindir kateter: koyu kontur + açık gövde. `cz` açık gövdeyi çizilebilir yapar. */
const Kateter = ({ d, w = 6.5, cz = false, acik = u('2b-kateter'), koyu = '#b47a1a', cls = 'boya-cizgi' }: { d: string; w?: number; cz?: boolean; acik?: string; koyu?: string; cls?: string }) => (
  <>
    <path d={d} stroke={koyu} strokeWidth={w + 2.5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    <path className={`${cz ? 'cz ' : ''}${cls}`} pathLength={cz ? 1 : undefined} d={d} stroke={acik} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
  </>
);

/** Çıplak el (yandan, parmaklar −x yönüne uzanır, başparmak +y tarafında). Yerel uzunluk ≈ 190 px (bilek dahil). */
const El = ({ eldiven = false }: { eldiven?: boolean }) => {
  const dolgu = eldiven ? u('2b-eldiven') : u('2b-deri');
  const kontur = eldiven ? '#3f6f9c' : DERI_K;
  return (
    <g>
      {/* bilek + ön kol parçası */}
      <path d="M68 -24 L130 -30 L130 32 L68 30 Z" fill={dolgu} stroke={kontur} strokeWidth={2.5} strokeLinejoin="round" />
      {/* parmaklar (4): uçlar yuvarlak, boğum çizgileri */}
      {[[-26, 70], [-9, 80], [8, 78], [25, 66]].map(([y, uz], i) => (
        <g key={i}>
          <rect x={-uz} y={y - 7.5} width={uz + 10} height={15} rx={7.5} fill={dolgu} stroke={kontur} strokeWidth={2.5} />
          <path d={`M${-uz * 0.62} ${y - 6} q3 6 0 12 M${-uz * 0.3} ${y - 6} q3 6 0 12`} stroke={kontur} strokeWidth={1.4} fill="none" opacity={0.6} />
        </g>
      ))}
      {/* avuç: parmak köklerini örter */}
      <path className="boya" d="M4 -34 C26 -40 54 -38 70 -30 L70 30 C54 42 26 44 4 38 C-4 20 -4 -16 4 -34 Z" fill={dolgu} stroke={kontur} strokeWidth={2.5} strokeLinejoin="round" />
      {/* başparmak: avucun alt kenarından öne-aşağı */}
      <path d="M8 36 C-6 50 -24 58 -40 56 C-50 54 -52 44 -44 40 C-30 34 -14 28 2 20 Z" fill={dolgu} stroke={kontur} strokeWidth={2.5} strokeLinejoin="round" />
      <path d="M-20 52 q2 -6 -2 -10" stroke={kontur} strokeWidth={1.4} fill="none" opacity={0.6} />
    </g>
  );
};

// ———————————————————————————————————————————————————————————————————————————————————————————
/** Mesane (ayakta sagital şema; arka = sol, ön = sağ, alt = aşağı). Sakrum–rektum arkada, simfiz önde derinin hemen
 *  altında, mesane simfizin arka-üstünde, üretra aşağı perineye. Ölçek 1 cm ≈ 12 px: normal mesane ≈ 9×7 cm, glob
 *  umbilikusa (y≈90) dek, sistitli mesane küçük (≈6×5 cm) kalın ödemli duvarlı. İlaç/opak oku ÜRETRADAN girer. */
const URETRA_G = 'M436 326 C440 362 442 404 438 446';
const DRENAJ_G = 'M438 446 C436 478 456 492 500 492 L638 492 C656 492 666 484 666 466 L666 334';
const Mesane: Sahne = {
  ad: 'Mesane, suprapubik bölge ve idrar takibi (yan kesit)',
  gizli: ['g-mesane-dolu', 'g-sisme', 'g-torba', 'g-akis', 'g-kultur', 'g-ilac', 'g-kucuk', 'g-el', 'g-us', 'g-us-dalga'],
  etiket: {
    'g-mesane-normal': [420, 283, 'Mesane'],
    'g-mesane-dolu': [420, 150, 'Dolu mesane (glob)'],
    'g-sisme': [688, 250, 'Suprapubik kabarıklık'],
    'g-torba': [712, 312, 'İdrar torbası'],
    'g-kultur': [556, 382, 'Steril kültür kabı'],
    'g-ilac': [250, 430, 'Mesane içine ilaç / opak madde'],
    'g-kucuk': [280, 352, 'Sistit: 15–20 mL, ödemli duvar'],
    'g-el': [688, 120, 'Suprapubik palpasyon'],
    'g-us': [706, 60, 'Ultrason probu'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* gövde: deri (dış) + kesit yüzeyi (iç); ön karın duvarı sağda, sırt solda, perine altta */}
      <path d="M160 0 L560 0 L562 100 C576 160 576 240 540 320 C524 356 500 386 470 410 C450 426 440 440 440 452 L380 464 C340 472 300 472 262 468 L232 500 L160 500 Z" fill={u('2b-deri')} stroke={DERI_K} strokeWidth={2.5} strokeLinejoin="round" />
      <path d="M172 0 L548 0 L550 100 C563 160 563 240 528 316 C512 350 490 378 460 400 C442 416 430 430 428 442 L380 452 C340 460 300 460 266 456 L240 500 L172 500 Z" fill="#f6d7bd" />
      {/* göbek deliği */}
      <path d="M560 84 C554 90 554 98 560 104" stroke={DERI_K} strokeWidth={2.2} fill="none" strokeLinecap="round" />
      {/* bağırsak kıvrımları (glob dolunca arkasında kalır) */}
      {[[310, 60, 48, 28], [410, 48, 50, 28], [500, 90, 38, 24], [340, 126, 44, 24], [446, 132, 42, 24]].map(([x, y, rx, ry], i) => (
        <g key={i}>
          <ellipse cx={x} cy={y} rx={rx} ry={ry} fill="#f0c9b3" stroke="#c58b7a" strokeWidth={2} />
          <path d={`M${x - rx * 0.55} ${y + 2} q${rx * 0.55} ${-ry * 0.5} ${rx * 1.1} 0`} stroke="#c58b7a" strokeWidth={1.6} fill="none" opacity={0.6} />
        </g>
      ))}
      {/* sakrum + koksiks (arkada, öne içbükey) */}
      <path d="M200 26 C238 58 254 120 252 190 C250 250 242 310 228 360 C222 380 216 396 208 410 L188 404 C198 380 206 350 210 310 C216 250 214 170 200 110 C194 80 186 54 178 36 Z" fill={u('2b-kemik')} stroke={KEMIK_K} strokeWidth={2.5} strokeLinejoin="round" />
      {[90, 140, 190, 240, 290].map((y, i) => <path key={y} d={`M${208 + i * 2} ${y} l22 5`} stroke={KEMIK_K} strokeWidth={1.6} opacity={0.7} />)}
      <path d="M208 410 C212 420 218 428 226 434" stroke={KEMIK_K} strokeWidth={8} strokeLinecap="round" fill="none" />
      <path d="M208 410 C212 420 218 428 226 434" stroke="#efe3c6" strokeWidth={4} strokeLinecap="round" fill="none" />
      {/* pelvis tabanı (levator): koksiks → pubis alt kenarı; rektum ve üretra bu kası DELER (üstüne çizilir) */}
      <path d="M226 434 C290 416 400 394 490 372" stroke="#8d2f28" strokeWidth={11} fill="none" strokeLinecap="round" />
      <path d="M226 434 C290 416 400 394 490 372" stroke="#d26a5f" strokeWidth={7} fill="none" strokeLinecap="round" />
      {/* rektum + anal kanal (sakrumun önünde) */}
      <path d="M262 60 C292 120 298 200 296 280 C294 340 300 400 300 456" stroke="#9a6450" strokeWidth={36} fill="none" strokeLinecap="round" />
      <path d="M262 60 C292 120 298 200 296 280 C294 340 300 400 300 456" stroke="#dba58f" strokeWidth={31} fill="none" strokeLinecap="round" />
      <path d="M262 60 C292 120 298 200 296 280 C294 340 300 400 300 456" stroke="#b67e68" strokeWidth={2} fill="none" strokeDasharray="3 9" opacity={0.6} />
      {/* simfiz pubis: derinin hemen altında, mesanenin ön-altında */}
      <ellipse cx={500} cy={338} rx={12} ry={27} fill={u('2b-kemik')} stroke={KEMIK_K} strokeWidth={2.5} transform="rotate(22 500 338)" />
      <path d="M498 316 L500 360" stroke="#efe3c6" strokeWidth={3} strokeLinecap="round" />
      {/* üretra: mesane boynundan aşağı perineye (meatus 438,446) */}
      <path d={URETRA_G} stroke="#8a3b33" strokeOpacity={0.5} strokeWidth={13} fill="none" strokeLinecap="round" />
      <path d={URETRA_G} stroke="#f2b7b0" strokeWidth={8} fill="none" strokeLinecap="round" />
      {/* mesane: üç durum aynı yerde (biri görünür) */}
      <g {...o('g-mesane-normal')}>
        <path d="M426 318 L440 334" stroke="#a8433a" strokeWidth={16} strokeLinecap="round" />
        <ellipse className="boya" cx={420} cy={285} rx={52} ry={44} fill={u('2b-mesane')} stroke="#7a2e26" strokeWidth={3} />
        <ellipse cx={420} cy={285} rx={42} ry={35} fill={u('2b-idrar')} fillOpacity={0.9} />
        <path d="M394 262 C404 254 420 252 434 256" stroke="#fff6cf" strokeWidth={4} fill="none" strokeLinecap="round" opacity={0.85} />
      </g>
      <g {...o('g-mesane-dolu')}>
        <path d="M428 312 L438 332" stroke="#a8433a" strokeWidth={16} strokeLinecap="round" />
        <ellipse className="boya" cx={420} cy={200} rx={92} ry={112} fill={u('2b-mesane')} stroke="#7a2e26" strokeWidth={3} />
        <ellipse cx={420} cy={200} rx={80} ry={100} fill={u('2b-idrar')} fillOpacity={0.92} />
        <path d="M376 120 C392 106 420 102 448 110" stroke="#fff6cf" strokeWidth={5} fill="none" strokeLinecap="round" opacity={0.85} />
      </g>
      <g {...o('g-kucuk')}>
        <path d="M428 320 L438 334" stroke="#a8433a" strokeWidth={14} strokeLinecap="round" />
        <ellipse className="boya" cx={420} cy={292} rx={36} ry={30} fill={u('2b-mukoza')} stroke="#7a2e26" strokeWidth={12} />
        <ellipse cx={420} cy={292} rx={18} ry={13} fill={u('2b-idrar')} fillOpacity={0.9} />
        {/* ödemli kıvrımlar */}
        {['M396 280 q8 6 4 14', 'M446 280 q-6 8 0 14', 'M404 308 q8 -2 14 4', 'M438 306 q4 -6 10 -2'].map((d) => <path key={d} d={d} stroke="#7a2e26" strokeWidth={1.6} fill="none" opacity={0.8} />)}
      </g>
      {/* suprapubik kabarıklık: karın duvarı dolu mesanenin önünde öne bombeleşir */}
      <g {...o('g-sisme')}>
        <path d="M558 88 C616 150 618 250 556 336 L532 318 C568 240 568 160 552 100 Z" fill={u('2b-deri')} />
        <path d="M554 104 C604 152 606 250 548 326 L538 318 C564 244 562 160 546 110 Z" fill="#f6d7bd" />
        <path className="cz boya-cizgi" pathLength={1} d="M562 92 C616 150 618 250 556 334" stroke={DERI_K} strokeWidth={3} fill="none" strokeLinecap="round" />
      </g>
      {/* palpasyon eli: parmak uçları suprapubik deride */}
      <g {...o('g-el')}>
        <g transform="translate(640 170) rotate(10)">
          <El />
        </g>
      </g>
      {/* ultrason probu: yüzü deride, kablo sağ kenara */}
      <g {...o('g-us')}>
        <path d="M630 312 C690 290 740 268 800 258" stroke="#3e4a58" strokeWidth={5} fill="none" strokeLinecap="round" />
        <g transform="translate(548 312) rotate(-18)">
          <path className="boya" d="M8 -30 L70 -22 C78 -20 84 -12 84 -2 L84 2 C84 12 78 20 70 22 L8 30 C0 24 -4 12 -4 0 C-4 -12 0 -24 8 -30 Z" fill={u('2b-plastik')} stroke="#6b7a90" strokeWidth={2.5} strokeLinejoin="round" />
          <path d="M8 -30 C0 -24 -4 -12 -4 0 C-4 12 0 24 8 30 L14 30 C6 22 4 12 4 0 C4 -12 6 -22 14 -30 Z" fill="#3e4a58" />
          <rect x={30} y={-12} width={30} height={10} rx={3} fill="#2f6fd6" />
          <rect x={30} y={2} width={30} height={10} rx={3} fill="#2f6fd6" opacity={0.6} />
        </g>
        <path d="M548 292 C542 302 540 318 544 330" stroke="#bfe0ff" strokeWidth={5} strokeOpacity={0.85} fill="none" strokeLinecap="round" />
      </g>
      {/* ultrason ışını: prob yüzünden mesaneye (simfizin üstünden) */}
      <g {...o('g-us-dalga')}>
        <path d="M550 290 L540 328 L368 290 L372 170 Z" fill="#7fb8ff" fillOpacity={0.28} />
        {[0, 1, 2].map((i) => (
          <path key={i} className="cz" pathLength={1} d={`M${520 - i * 44} ${278 - i * 20} C${508 - i * 44} ${290 - i * 16} ${506 - i * 44} ${304 - i * 2} ${516 - i * 44} ${318 + i * 2}`} stroke="#2f6fd6" strokeWidth={3} fill="none" strokeLinecap="round" />
        ))}
      </g>
      {/* drenaj hortumu + idrar akışı: meatus → torba */}
      <g {...o('g-akis')}>
        <path d={DRENAJ_G} stroke="#6b7a90" strokeWidth={11} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d={DRENAJ_G} stroke="#eef3f8" strokeWidth={8} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path className="cz kmb-akis" pathLength={1} d={DRENAJ_G} stroke="#efc53f" strokeWidth={4} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </g>
      <g {...o('g-torba')}>
        <rect className="boya" x={650} y={334} width={120} height={130} rx={14} fill={u('2b-plastik')} stroke="#6b7a90" strokeWidth={2.5} />
        <path d="M660 408 L760 408 L760 446 C760 454 752 456 744 456 L676 456 C668 456 660 454 660 446 Z" fill="#efc53f" fillOpacity={0.75} />
        <path d="M660 408 L760 408" stroke="#fff" strokeWidth={2} opacity={0.7} />
        {[356, 380, 404, 428, 452].map((y) => <path key={y} d={`M748 ${y} L764 ${y}`} stroke="#5b6676" strokeWidth={1.5} />)}
        <rect x={700} y={460} width={20} height={14} rx={3} fill="#6b7a90" stroke="#3e4a58" strokeWidth={1.2} />
      </g>
      {/* steril kültür kabı: şeffaf kap, kırmızı kapak, idrar filmi altta */}
      <g {...o('g-kultur')}>
        <rect className="boya" x={532} y={414} width={48} height={62} rx={8} fill={u('2b-plastik')} stroke="#6b7a90" strokeWidth={2.5} />
        <rect x={536} y={448} width={40} height={24} rx={5} fill="#efc53f" fillOpacity={0.75} />
        <rect x={526} y={404} width={60} height={16} rx={5} fill="#c0392b" stroke="#8d1f1f" strokeWidth={2} />
        <rect x={540} y={426} width={32} height={12} rx={2} fill="#fff" stroke="#c9d3de" strokeWidth={1} />
        <text x={556} y={435} fontSize={7} textAnchor="middle" fill="#3e4a58" fontWeight={700}>STERİL</text>
      </g>
      {/* mesane içine ilaç/opak: ok ÜRETRADAN (kateter yolundan) mesaneye */}
      <g {...o('g-ilac')}>
        <path className="cz" pathLength={1} d="M520 492 C476 492 436 480 438 446 C442 404 440 362 436 326 L426 300" stroke="#2f6fd6" strokeWidth={5} fill="none" strokeLinecap="round" strokeDasharray="0.03 0.015" markerEnd="url(#kmb-ok)" />
      </g>
    </>
  ),
};

// ———————————————————————————————————————————————————————————————————————————————————————————
/** Yakın plan: mesane tabanı/boynu (koronal kesit). Ölçek 1 cm ≈ 30 px: boyun ≈ 2 cm, 16 Fr kateter 5,3 mm ≈ 16 px,
 *  10 mL balon ≈ 2,7 cm ≈ r 40. Kateter alttan (prostatik üretra) girer, ucu lümende; balon boynun hemen üstünde lümen içinde. */
const YakinMesane: Sahne = {
  ad: 'Yakın plan: kateter ucu mesane boynunda',
  gizli: ['y-kateter', 'y-delik', 'y-balon-sonuk', 'y-balon', 'y-idrar', 'y-cekme'],
  etiket: {
    'y-duvar': [150, 40, 'Mesane duvarı (detrüsör)'],
    'y-trigon': [530, 206, 'Trigon'],
    'y-ureter': [270, 206, 'Üreter ağzı'],
    'y-boyun': [548, 362, 'Mesane boynu'],
    'y-prostat': [170, 450, 'Prostat / prostatik üretra'],
    'y-delik': [580, 150, 'Uçtaki delikler: idrar girer'],
    'y-balon-sonuk': [250, 262, 'Sönük balon'],
    'y-balon': [604, 286, 'Balon: 10 mL izotonik'],
    'y-idrar': [250, 120, 'İdrar deliklerden kanala'],
    'y-cekme': [640, 470, 'Hafifçe çek: balon boyna oturur'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* detrüsör duvar: kalın, altta huni gibi boyna daralır */}
      <g {...o('y-duvar')}>
        <path className="boya" d="M20 20 L780 20 L780 300 C700 300 560 300 480 328 L470 345 L470 372 L330 372 L330 345 L320 328 C240 300 100 300 20 300 Z" fill={u('2b-mesane')} stroke="#7a2e26" strokeWidth={3} strokeLinejoin="round" />
        {/* rugalar: demet çizgileri duvar bandında */}
        {Array.from({ length: 8 }, (_, i) => <path key={i} d={`M${80 + i * 90} 28 q10 12 0 24`} stroke="#7a2e26" strokeWidth={2} fill="none" opacity={0.45} strokeLinecap="round" />)}
        {[100, 160, 220].map((y) => <g key={y}><path d={`M30 ${y} q8 10 0 22`} stroke="#7a2e26" strokeWidth={2} fill="none" opacity={0.45} /><path d={`M770 ${y} q-8 10 0 22`} stroke="#7a2e26" strokeWidth={2} fill="none" opacity={0.45} /></g>)}
      </g>
      {/* lümen: idrar (yarı saydam) */}
      <path d="M60 60 L740 60 L740 268 C660 268 540 268 452 300 L432 335 L368 335 L348 300 C260 268 140 268 60 268 Z" fill={u('2b-idrar')} fillOpacity={0.85} stroke="#a8433a" strokeWidth={2} strokeLinejoin="round" />
      <path d="M90 84 C200 72 600 72 710 84" stroke="#fff6cf" strokeWidth={5} fill="none" strokeLinecap="round" opacity={0.8} />
      {/* trigon: iki üreter ağzı + boyun üçgeni (arka duvarda) */}
      <g {...o('y-trigon')}>
        <path className="boya" d="M300 232 L500 232 L400 330 Z" fill="#f0a8a4" fillOpacity={0.8} stroke="#a85f5a" strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M312 240 L488 240" stroke="#a85f5a" strokeWidth={2} opacity={0.6} />
      </g>
      <g {...o('y-ureter')}>
        <ellipse className="boya" cx={300} cy={232} rx={16} ry={7} fill="#7a2e26" stroke="#5a1f1a" strokeWidth={2} />
        <ellipse cx={500} cy={232} rx={16} ry={7} fill="#7a2e26" stroke="#5a1f1a" strokeWidth={2} />
        <path d="M288 230 q12 -5 24 0 M488 230 q12 -5 24 0" stroke="#f3c6c2" strokeWidth={1.8} fill="none" />
      </g>
      {/* prostat lobları + prostatik üretra lümeni */}
      <g {...o('y-prostat')}>
        <path className="boya" d="M196 374 C250 362 330 364 380 374 L380 500 L176 500 C164 456 170 404 196 374 Z" fill={u('2b-prostat')} stroke="#9a5a44" strokeWidth={2.5} strokeLinejoin="round" />
        <path className="boya" d="M604 374 C550 362 470 364 420 374 L420 500 L624 500 C636 456 630 404 604 374 Z" fill={u('2b-prostat')} stroke="#9a5a44" strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M380 374 L380 500 L420 500 L420 374 Z" fill="#f2b7b0" />
        <path d="M380 374 L380 500 M420 374 L420 500" stroke="#a85f5a" strokeWidth={2} />
      </g>
      {/* boyun: hunide halka */}
      <g {...o('y-boyun')}>
        <path d="M348 300 C364 324 382 338 400 338 C418 338 436 324 452 300" stroke="#7a2e26" strokeWidth={11} fill="none" strokeLinecap="round" />
        <path className="boya-cizgi" d="M348 300 C364 324 382 338 400 338 C418 338 436 324 452 300" stroke="#f0a8a4" strokeWidth={7} fill="none" strokeLinecap="round" />
      </g>
      {/* kateter: alttan girer, ucu lümende */}
      <g {...o('y-kateter')}>
        <Kateter d="M400 500 L400 166" w={16} />
        <path d="M395 186 L395 500" stroke="#fff" strokeWidth={2} opacity={0.5} strokeLinecap="round" />
      </g>
      <g {...o('y-delik')}>
        <ellipse className="boya" cx={408} cy={182} rx={4} ry={7.5} fill="#3e2a10" />
        <ellipse cx={392} cy={206} rx={4} ry={7.5} fill="#3e2a10" />
      </g>
      <g {...o('y-balon-sonuk')}>
        <rect className="boya" x={386} y={236} width={28} height={54} rx={12} fill={u('2b-balon')} stroke="#8a96a6" strokeWidth={2.5} />
      </g>
      <g {...o('y-balon')}>
        <circle className="boya" cx={400} cy={262} r={40} fill={u('2b-balon')} stroke="#2e9e5b" strokeWidth={3} />
        <ellipse cx={388} cy={248} rx={10} ry={6} fill="#fff" />
      </g>
      {/* idrar: lümenden deliklere ince akış çizgileri */}
      <g {...o('y-idrar')}>
        {[[280, 110], [230, 170], [520, 120], [560, 180]].map(([x, y], i) => (
          <path key={i} className="cz kmb-akis" pathLength={1} d={`M${x} ${y} C${(x + 400) / 2} ${y + 14} ${400 + (x < 400 ? -24 : 24)} ${i % 2 ? 206 : 182} ${x < 400 ? 392 : 408} ${x < 400 ? 206 : 182}`} stroke="#d9a400" strokeWidth={3} fill="none" strokeLinecap="round" />
        ))}
      </g>
      <g {...o('y-cekme')}>
        <path className="cz" pathLength={1} d="M448 384 L448 444" stroke="#2f6fd6" strokeWidth={5} fill="none" strokeLinecap="round" markerEnd="url(#kmb-ok)" />
      </g>
    </>
  ),
};

// ———————————————————————————————————————————————————————————————————————————————————————————
/** Yakın plan: üretra boyuna kesiti. Mesane SAĞDA (ok → mesaneye). Soldan sağa: korpus spongiozum (bulbar/penil),
 *  eksternal sfinkter halkası (membranöz, kesitte lümenin üst-altında iki kas bloğu), prostatik üretra (prostat dokusu).
 *  Ölçek 1 cm ≈ 44 px: lümen 44 px, 16 Fr kateter ≈ 22 px (oran ½), 10 mL balon ≈ 2,7 cm → lümeni zorla gerer. */
const KAT_Z = 'M0 250 L800 250';
const KIVRIM_Z = 'M0 250 L236 250 C280 250 304 238 304 216 C304 198 278 196 272 212 C266 230 282 252 312 258 L326 258';
const YakinUretra: Sahne = {
  ad: 'Yakın plan: üretra boyuna kesiti',
  gizli: ['z-kivrim', 'z-balon', 'z-yirtik', 'z-kan', 'z-sivi', 'z-dogru'],
  etiket: {
    'z-mukoza': [96, 192, 'Üretra mukozası'],
    'z-spongiozum': [130, 340, 'Korpus spongiozum'],
    'z-sfinkter': [400, 60, 'Eksternal sfinkter'],
    'z-kivrim': [292, 110, 'Kateter takıldı, kıvrıldı'],
    'z-balon': [560, 440, 'Balon üretrada şişti'],
    'z-yirtik': [690, 360, 'Mukoza yırtığı'],
    'z-sivi': [200, 440, '30–40 mL izotonik geri gelmiyor'],
    'z-dogru': [660, 100, 'Serbest kateter → mesaneye'],
  },
  Ciz: ({ o }) => (
    <>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* korpus spongiozum: sol bölüm, süngerimsi sinüzoidler */}
      <g {...o('z-spongiozum')}>
        <path className="boya" d="M0 90 L340 90 L340 410 L0 410 Z" fill="#eaa9a5" stroke="#b9686b" strokeWidth={3} strokeLinejoin="round" />
        {[[40, 130], [120, 110], [210, 140], [290, 118], [70, 180], [180, 176], [260, 170], [60, 330], [140, 350], [230, 326], [300, 352], [100, 386], [200, 390], [290, 392]].map(([x, y], i) => (
          <ellipse key={i} cx={x} cy={y} rx={13} ry={8} fill="#d98a86" stroke="#b9686b" strokeWidth={1.4} opacity={0.75} />
        ))}
      </g>
      {/* prostat dokusu: sağ bölüm */}
      <path d="M460 90 L800 90 L800 410 L460 410 Z" fill={u('2b-prostat')} stroke="#9a5a44" strokeWidth={3} strokeLinejoin="round" />
      {[[520, 140], [620, 120], [720, 150], [560, 370], [680, 380], [760, 340]].map(([x, y], i) => <path key={i} d={`M${x} ${y} q12 -10 24 0`} stroke="#9a5a44" strokeWidth={1.6} fill="none" opacity={0.5} />)}
      {/* eksternal sfinkter: lümenin üstünde ve altında kas blokları (halkanın kesiti) */}
      <g {...o('z-sfinkter')}>
        <path className="boya" d="M340 90 L460 90 L460 228 L340 228 Z" fill={u('2b-kas')} stroke="#8d2f28" strokeWidth={3} strokeLinejoin="round" />
        <path className="boya" d="M340 272 L460 272 L460 410 L340 410 Z" fill={u('2b-kas')} stroke="#8d2f28" strokeWidth={3} strokeLinejoin="round" />
        {Array.from({ length: 5 }, (_, i) => <path key={i} d={`M${356 + i * 22} 100 L${356 + i * 22} 218 M${356 + i * 22} 282 L${356 + i * 22} 400`} stroke="#8d2f28" strokeWidth={1.6} opacity={0.5} />)}
      </g>
      {/* mukoza: tüm boyda bant, lümen ortada */}
      <g {...o('z-mukoza')}>
        <path className="boya" d="M0 200 L800 200 L800 300 L0 300 Z" fill={u('2b-mukoza')} stroke="#a85f5a" strokeWidth={2.5} />
        <path d="M0 228 L800 228 L800 272 L0 272 Z" fill="#f8dcd8" />
        {Array.from({ length: 16 }, (_, i) => <path key={i} d={`M${i * 50} 226 q25 10 50 0 M${i * 50} 274 q25 -10 50 0`} stroke="#a85f5a" strokeWidth={1.6} fill="none" opacity={0.55} />)}
      </g>
      {/* doğru: serbest ilerleyen kateter (lümende) + mesaneye ok */}
      <g {...o('z-dogru')}>
        <Kateter d={KAT_Z} w={22} cz />
        <path d="M0 244 L800 244" stroke="#fff" strokeWidth={2.4} opacity={0.5} />
        <path className="cz" pathLength={1} d="M600 140 L760 140" stroke="#2e9e5b" strokeWidth={5} strokeLinecap="round" markerEnd="url(#kmb-ok)" />
      </g>
      {/* kıvrım: sfinkter önünde takılır, lümen yerel gerilir, uç geri kıvrılır */}
      <g {...o('z-kivrim')}>
        <ellipse cx={285} cy={238} rx={52} ry={42} fill="#f8dcd8" stroke="#a85f5a" strokeWidth={2.5} />
        <Kateter d={KIVRIM_Z} w={22} cz />
      </g>
      {/* yanlış: balon üretrada (prostatik) şişti → mukoza gerilir */}
      <g {...o('z-balon')}>
        <ellipse cx={560} cy={250} rx={97} ry={86} fill={u('2b-mukoza')} stroke="#a85f5a" strokeWidth={2.5} />
        <ellipse className="boya" cx={560} cy={250} rx={90} ry={78} fill="#e05a5a" fillOpacity={0.8} stroke="#8d1f1f" strokeWidth={3.5} />
        <ellipse cx={530} cy={214} rx={22} ry={10} fill="#fff" opacity={0.6} />
        {[20, 70, 110, 160, 200, 250, 290, 340].map((a) => <path key={a} d={`M${560 + Math.cos(a * Math.PI / 180) * 104} ${250 + Math.sin(a * Math.PI / 180) * 92} l${Math.cos(a * Math.PI / 180) * 10} ${Math.sin(a * Math.PI / 180) * 10}`} stroke="#d23b3b" strokeWidth={2.5} strokeLinecap="round" />)}
      </g>
      <g {...o('z-yirtik')}>
        {['M506 168 l12 22 l-10 12 l14 22', 'M616 330 l-12 -22 l10 -12 l-14 -22', 'M636 190 l-6 18 l10 10'].map((d) => <path key={d} d={d} stroke="#5c0f0f" strokeWidth={4} fill="none" strokeLinecap="round" strokeLinejoin="round" />)}
      </g>
      {/* kan: yırtıktan damlalar + lümen boyunca meatusa (sola) geri akış */}
      <g {...o('z-kan')}>
        {[[518, 302], [604, 196], [650, 300]].map(([x, y], i) => <path key={i} d={`M${x} ${y} c-7 11 -5 18 0 18 c5 0 7 -7 0 -18 Z`} fill="#b3201f" />)}
        <path className="cz" pathLength={1} d="M470 266 L0 266" stroke="#b3201f" strokeWidth={5} strokeLinecap="round" strokeDasharray="0.03 0.02" />
      </g>
      {/* izotonik: kateter içinde sağa itilir, geri gelmez (kırmızı çarpı) */}
      <g {...o('z-sivi')}>
        <path className="cz" pathLength={1} d="M30 250 L214 250" stroke="#8fc7ff" strokeWidth={6} strokeLinecap="round" markerEnd="url(#kmb-ok)" />
        <path d="M196 170 L224 198 M224 170 L196 198" stroke="#d23b3b" strokeWidth={5} strokeLinecap="round" />
      </g>
    </>
  ),
};

// ———————————————————————————————————————————————————————————————————————————————————————————
/** Travma: pelvis halkası önden (AP), ölçek 1 cm ≈ 17 px. İlium kanatları, sakrum, asetabulum + femur başı, pubis kolları,
 *  obturator foramen, simfiz. Penis simfizin altında aşağı sarkar (skrotum arkasında); üretra simfiz altı (membranöz) → bulbar → penil → meatus. */
const Travma: Sahne = {
  ad: 'Pelvis kırığı ve üretra yaralanması (önden)',
  gizli: ['t-kirik', 't-kan', 't-yirtik'],
  etiket: {
    't-pelvis': [130, 40, 'Pelvis halkası'],
    't-kirik': [250, 395, 'Pubis kolu kırığı'],
    't-simfiz': [530, 318, 'Simfiz ayrılması'],
    't-uretra': [480, 420, 'Üretra'],
    't-kan': [520, 480, 'Meatusta taze kan'],
    't-yirtik': [300, 400, 'Kısmi yırtık'],
  },
  Ciz: ({ o }) => {
    const kemik = u('2b-kemik');
    return (
      <>
        <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
        <g {...o('t-pelvis')}>
          {/* sakrum */}
          <path className="boya" d="M352 56 L448 56 C452 100 446 150 428 190 L410 214 L390 214 L372 190 C354 150 348 100 352 56 Z" fill={kemik} stroke={KEMIK_K} strokeWidth={2.5} strokeLinejoin="round" />
          {[84, 112, 140, 168].map((y) => <g key={y}><ellipse cx={380} cy={y} rx={5} ry={4} fill="#d8c8a0" /><ellipse cx={420} cy={y} rx={5} ry={4} fill="#d8c8a0" /></g>)}
          {[0, 1].map((s) => {
            const X = (x: number) => (s ? 800 - x : x);
            return (
              <g key={s}>
                {/* femur: boyun + şaft (asetabulumun arkasından aşağı-dışa) */}
                <path d={`M${X(206)} 284 C${X(200)} 330 ${X(190)} 390 ${X(178)} 470`} stroke={KEMIK_K} strokeWidth={46} strokeLinecap="round" fill="none" />
                <path d={`M${X(206)} 284 C${X(200)} 330 ${X(190)} 390 ${X(178)} 470`} stroke="#f0e6cf" strokeWidth={40} strokeLinecap="round" fill="none" />
                {/* ilium kanadı */}
                <path d={`M${X(352)} 66 C${X(300)} 40 ${X(190)} 30 ${X(130)} 70 C${X(100)} 92 ${X(96)} 140 ${X(118)} 180 C${X(140)} 214 ${X(176)} 226 ${X(200)} 236 L${X(250)} 232 C${X(300)} 210 ${X(340)} 180 ${X(366)} 160 Z`} fill={kemik} stroke={KEMIK_K} strokeWidth={2.5} strokeLinejoin="round" />
                <path d={`M${X(142)} 72 C${X(190)} 50 ${X(280)} 54 ${X(338)} 76`} stroke="#fff" strokeWidth={3} opacity={0.7} fill="none" strokeLinecap="round" />
                {/* asetabulum + femur başı */}
                <circle cx={X(220)} cy={262} r={40} fill="#e3d2ae" stroke={KEMIK_K} strokeWidth={2.5} />
                <circle cx={X(220)} cy={262} r={30} fill={kemik} stroke={KEMIK_K} strokeWidth={2} />
                <ellipse cx={X(210)} cy={250} rx={8} ry={5} fill="#fff" opacity={0.7} />
                {/* pubis kolları (üst + alt) + obturator foramen; simfiz ayrıldığı için gövde x 380'de biter */}
                <path d={`M${X(250)} 240 C${X(300)} 236 ${X(350)} 234 ${X(380)} 230 L${X(380)} 302 C${X(350)} 318 ${X(300)} 336 ${X(262)} 330 C${X(240)} 320 ${X(238)} 280 ${X(250)} 240 Z`} fill={kemik} stroke={KEMIK_K} strokeWidth={2.5} strokeLinejoin="round" />
                <ellipse cx={X(314)} cy={282} rx={34} ry={24} fill="#ffffff" stroke={KEMIK_K} strokeWidth={2} />
              </g>
            );
          })}
        </g>
        {/* simfiz: kıkırdak disk iki parçaya ayrılmış (diastaz) */}
        <g {...o('t-simfiz')}>
          <rect className="boya" x={380} y={228} width={40} height={74} rx={6} fill="#c9d7e6" fillOpacity={0.55} stroke="#6b7a90" strokeWidth={2} />
          <rect x={382} y={234} width={11} height={62} rx={4} fill="#dfe6ee" stroke="#6b7a90" strokeWidth={1.5} />
          <rect x={407} y={234} width={11} height={62} rx={4} fill="#dfe6ee" stroke="#6b7a90" strokeWidth={1.5} />
          <path d="M400 232 L400 298" stroke="#6b7a90" strokeWidth={1.5} strokeDasharray="4 4" />
        </g>
        {/* kırık: sol pubis kolu, kırmızı zikzak */}
        <g {...o('t-kirik')}>
          <path className="cz" pathLength={1} d="M276 234 L292 244 L282 254 L298 262 M272 302 L288 310 L280 322 L296 330" stroke="#d23b3b" strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M279 232 L295 242 L285 252 L301 260 M275 300 L291 308 L283 320 L299 328" stroke="#fff" strokeWidth={1.5} fill="none" opacity={0.8} />
        </g>
        {/* skrotum (arkada) + penis (önde, simfizin altından aşağı) */}
        <path d="M340 360 C340 330 460 330 460 360 L458 420 C456 448 344 448 342 420 Z" fill={u('2b-deri-koyu')} stroke={DERI_K} strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M400 372 L400 436" stroke={DERI_K} strokeWidth={1.6} opacity={0.6} />
        <path d="M376 306 L424 306 L424 452 C424 460 376 460 376 452 Z" fill={u('2b-deri')} stroke={DERI_K} strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M374 452 C374 440 426 440 426 452 L424 470 C420 486 380 486 376 470 Z" fill="#d98580" stroke="#a85f5a" strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M384 316 L384 440" stroke="#f7d2b6" strokeWidth={4} strokeLinecap="round" opacity={0.9} />
        {/* üretra: membranöz (simfiz altı) → bulbar → penil → meatus */}
        <g {...o('t-uretra')}>
          <path d="M400 304 L400 480" stroke="#a85f5a" strokeWidth={12} fill="none" strokeLinecap="round" />
          <path className="cz boya-cizgi" pathLength={1} d="M400 304 L400 480" stroke="#f2b7b0" strokeWidth={8} fill="none" strokeLinecap="round" />
        </g>
        {/* kısmi yırtık: membranöz/bulbar düzeyde */}
        <g {...o('t-yirtik')}>
          <ellipse cx={400} cy={346} rx={18} ry={12} fill="#d23b3b" fillOpacity={0.35} />
          <path d="M386 340 L414 332 M386 354 L414 346" stroke="#d23b3b" strokeWidth={4} strokeLinecap="round" />
        </g>
        {/* meatusta taze kan damlası */}
        <g {...o('t-kan')}>
          <path className="boya" d="M400 480 C391 490 391 499 400 499 C409 499 409 490 400 480 Z" fill="#b3201f" stroke="#7a1414" strokeWidth={1.5} />
          <path d="M397 488 C396 491 396 494 398 496" stroke="#fff" strokeWidth={1} opacity={0.7} />
        </g>
      </>
    );
  },
};

export const SAHNELER_2B_B: Record<string, Sahne> = { mesane: Mesane, 'yakin-mesane': YakinMesane, 'yakin-uretra': YakinUretra, travma: Travma };
