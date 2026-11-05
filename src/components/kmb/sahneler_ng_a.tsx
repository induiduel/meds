/** KMB 01 Nazogastrik sonda 2B sahneleri — grup A: baş-boyun sagital kesiti (`ng-kesit`) + burun yakın planı (`ng-burun`).
 *  Sözleşme: meds_temp/kmb/ng/SAHNE_SOZLESMESI.md §A–B, stil docs/KMB_2B_STIL.md (H462).
 *  Kesit: yüz SOLA, anterior = sol; baş hafif fleksiyonda (sert damak önde ~5° aşağı eğik). Burun tabanı F(x) = 212 − 0,082·(x − 150)
 *  (iç koordinat; çizim translate(60 0) ile sağa kaydırılır). Sonda merkez çizgisi tabanın 7 px üstünde, alt konkanın altında
 *  (alt meatus), nazofarinkste arka duvara 14 px kala aşağı kıvrılır, x = 460'ta (arka duvar 474) orofarinks → özofagusa iner.
 *  Hava yolu boşlukları yalnız dolgu (paylaşılan kenarda çizgi yok), duvar çizgileri ayrı → sonda hiçbir duvarı kesmez. */
import React from 'react';
import { type Sahne } from './sahneOrtak';

type Pt = [number, number];
const yol = (pts: Pt[]) => pts.map((p, i) => `${i ? 'L' : 'M'}${p[0]} ${p[1]}`).join(' ');

/** NG sonda: şeffaf-açık plastik boru (koyu kontur + açık gövde). İki çizgi de `cz` → çizim animasyonunda birlikte ilerler. */
function Sonda({ d, w = 7, kontur = '#6b7a90', govde = '#e9eef3', cz = true }: { d: string; w?: number; kontur?: string; govde?: string; cz?: boolean }) {
  const p = cz ? { pathLength: 1 } : {};
  return (
    <>
      <path className={cz ? 'cz' : undefined} {...p} d={d} stroke={kontur} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path className={`${cz ? 'cz ' : ''}boya-cizgi`} {...p} d={d} stroke={govde} strokeWidth={w * 0.62} fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </>
  );
}

/** Uzuv / parmak (sahneler_2b_c ile aynı yapı): kontur + düz dolgu + boğum çizgisi */
function Uzuv({ pts, w, dolgu, kontur, cls }: { pts: Pt[]; w: number; dolgu: string; kontur: string; cls?: string }) {
  const d = yol(pts);
  return (
    <>
      <path d={d} stroke={kontur} strokeWidth={w + 5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path className={cls} d={d} stroke={dolgu} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      {pts.slice(1, -1).map(([x, y], i) => {
        const [ax, ay] = pts[i]; const [bx, by] = pts[i + 2];
        const dx = bx - ax, dy = by - ay; const L = Math.hypot(dx, dy) || 1;
        const nx = (-dy / L) * w * 0.34, ny = (dx / L) * w * 0.34;
        return <path key={i} d={`M${x + nx} ${y + ny} Q${x + (dx / L) * w * 0.14} ${y + (dy / L) * w * 0.14} ${x - nx} ${y - ny}`} stroke={kontur} strokeWidth={2} fill="none" opacity={0.7} strokeLinecap="round" />;
      })}
    </>
  );
}

const DERI = 'url(#kmb-2b-deri)', KONTUR_DERI = '#b9805a';
const KEMIK = 'url(#kmb-2b-kemik)', KEMIK_K = '#b9a479';
const LUMEN = '#fff7f2', MUKOZA_K = '#a85f5a';
const DOKU = 'url(#kmb-ng-doku)';

/** Küçük ok uçları (kmb-ok sahnede fazla iri kalıyordu) */
function NgDefs() {
  return (
    <defs>
      <linearGradient id="kmb-ng-doku" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#f6d3c0" /><stop offset="1" stopColor="#eab9a2" /></linearGradient>
      <linearGradient id="kmb-ng-beyin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#f3e3e3" /><stop offset="1" stopColor="#e7cfd1" /></linearGradient>
      <linearGradient id="kmb-ng-kikirdak" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stopColor="#f6efe6" /><stop offset="1" stopColor="#e6d8c6" /></linearGradient>
      <marker id="kmb-ng-ok" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 Z" fill="#2f6fd6" />
      </marker>
      <marker id="kmb-ng-ok-k" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 Z" fill="#c62828" />
      </marker>
    </defs>
  );
}

// ———————————————————————————————————————————————————— KESİT
// Ortak sonda başlangıcı: dışarıda üst dudağın önünde sarkar → burun deliği → vestibül → burun tabanı (F − 7) → koana
const BURUN_YOLU = 'M70 330 C68 290 74 244 92 210 C104 196 126 206 150 205 L345 189';
const SONDA_D = `${BURUN_YOLU} C410 186 452 200 456 250 L460 300 L460 650`;
const TRAKEA_D = `${BURUN_YOLU} C410 186 452 200 456 250 L456 318 C456 350 432 350 432 382 L432 650`;
const KIVRIM_D = `${BURUN_YOLU} C410 186 452 200 456 250 C458 288 424 296 408 284 C398 276 386 258 370 248 C350 236 322 227 300 226 L222 231 C198 233 194 243 216 242 L292 237`;

const NgKesit: Sahne = {
  ad: 'Baş-boyun sagital kesiti (nazogastrik sonda yolu)',
  gizli: ['nk-sonda', 'nk-sonda-trakea', 'nk-ok-duz', 'nk-ok-asagi', 'nk-epiglot-kapali', 'nk-su', 'nk-dil-kivrim', 'nk-kirik', 'nk-yanik', 'nk-varis', 'nk-kusmuk'],
  etiket: {
    'nk-bas': [100, 400, 'Baş-boyun'],
    'nk-burun-delik': [70, 80, 'Burun deliği'],
    'nk-yuz-kemik': [76, 30, 'Yüz kemikleri'],
    'nk-kafa-tabani': [430, 20, 'Kafa tabanı'],
    'nk-kirik': [180, 20, 'Kırık'],
    'nk-burun-bosluk': [262, 66, 'Burun boşluğu'],
    'nk-ok-duz': [420, 96, 'Damağa paralel'],
    'nk-sert-damak': [150, 180, 'Sert damak'],
    'nk-yumusak-damak': [436, 182, 'Yumuşak damak'],
    'nk-su': [300, 182, 'Su yudumu'],
    'nk-dil': [258, 230, 'Dil'],
    'nk-dil-kivrim': [300, 278, 'Dilde kıvrılma'],
    'nk-epiglot': [432, 260, 'Epiglot'],
    'nk-epiglot-kapali': [398, 308, 'Epiglot kapalı'],
    'nk-larinks': [380, 355, 'Larinks'],
    'nk-trakea': [392, 402, 'Trakea'],
    'nk-sonda-trakea': [236, 402, 'Trakeaya yanlış'],
    'nk-nazofarinks': [610, 90, 'Nazofarinks'],
    'nk-ok-asagi': [610, 135, 'Aşağı yönlendir'],
    'nk-yanik': [610, 180, 'Koroziv yanık'],
    'nk-orofarinks': [610, 225, 'Orofarinks'],
    'nk-kusmuk': [626, 270, 'Kusma / aspirasyon'],
    'nk-sonda': [610, 315, 'NG sonda'],
    'nk-ozofagus': [610, 360, 'Özofagus'],
    'nk-varis': [616, 405, 'Özofagus varisi'],
  },
  Ciz: ({ o }) => (
    <>
      <NgDefs />
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      <g transform="translate(60 -70)">
        {/* ——— baş-boyun dış hattı (deri) + iç yumuşak doku */}
        <g {...o('nk-bas')}>
          <path className="boya" d="M140 -10 C118 20 108 55 110 85 C111 95 114 100 112 104 C102 128 72 155 58 172 C51 182 58 192 72 193 C85 195 96 197 102 201 C98 212 93 222 97 231 C100 233 101 235 97 238 C92 246 94 256 102 262 C108 268 104 276 98 288 C94 300 104 314 122 318 C170 330 250 338 300 350 C330 358 355 372 366 400 C374 430 378 470 384 650 L612 650 C598 450 592 380 604 320 C640 250 655 140 615 60 C595 20 575 0 560 -10 Z" fill={DERI} stroke={KONTUR_DERI} strokeWidth={3} strokeLinejoin="round" />
          {/* deri altı doku (deri çizgisinin 6 px içinde) */}
          <path d="M146 -10 C126 20 116 55 118 85 C119 96 122 102 119 108 C110 128 84 154 70 172 C66 180 70 185 78 186 C90 188 100 191 108 196 C104 210 100 222 104 230 C108 236 106 242 103 246 C100 254 104 258 110 262 C116 270 112 280 106 290 C104 302 112 308 126 311 C172 322 252 330 304 343 C336 352 362 368 372 398 C381 430 385 470 391 650 L604 650 C591 450 585 380 597 318 C632 250 646 140 608 64 C590 26 570 4 553 -10 Z" fill={DOKU} />
          {/* omurga (servikal; dekoratif) */}
          <rect x={490} y={208} width={18} height={20} rx={6} fill={KEMIK} stroke={KEMIK_K} strokeWidth={2} />
          {[232, 298, 346, 394, 442, 490, 538, 586].map((y, i) => (
            <g key={y}>
              <rect x={494} y={y} width={48} height={i ? 40 : 58} rx={7} fill={KEMIK} stroke={KEMIK_K} strokeWidth={2.5} />
              <path d={`M548 ${y + 12} L582 ${y + 20} L578 ${y + 30} L548 ${y + 28} Z`} fill={KEMIK} stroke={KEMIK_K} strokeWidth={2} strokeLinejoin="round" />
            </g>
          ))}
          {/* beyin (kafa tabanının üstü) */}
          <path d="M140 -10 C128 30 126 66 132 92 C160 82 220 80 300 82 C348 84 374 96 412 110 C452 126 482 150 502 186 C540 188 576 176 592 156 C608 116 602 40 562 -10 Z" fill="url(#kmb-ng-beyin)" stroke={KEMIK_K} strokeWidth={7} strokeLinejoin="round" />
          {/* ağız boşluğu (hava; dudaklar kapalı, dil ile damak arası dar boşluk) */}
          <path d="M128 244 L124 232 L150 228 L345 212 C368 222 388 238 400 256 L404 270 L400 284 C382 264 350 248 300 244 C228 246 168 250 132 262 Z" fill={LUMEN} />
          {/* üst ve alt kesici dişler */}
          <path d="M110 222 L124 222 L126 246 C122 250 114 250 112 246 Z" fill="#ffffff" stroke="#9aa6b2" strokeWidth={2} strokeLinejoin="round" />
          <path d="M108 250 L122 250 L120 270 L110 270 Z" fill="#ffffff" stroke="#9aa6b2" strokeWidth={2} strokeLinejoin="round" />
          {/* hiyoid */}
          <ellipse cx={386} cy={372} rx={10} ry={5} fill={KEMIK} stroke={KEMIK_K} strokeWidth={2} />
        </g>

        {/* ——— yüz kemikleri: burun kemiği, maksilla alveolü, mandibula simfizi */}
        <g {...o('nk-yuz-kemik')}>
          <path className="boya" d="M114 98 L124 100 C116 118 104 132 92 142 L84 136 C96 124 108 112 114 98 Z" fill={KEMIK} stroke={KEMIK_K} strokeWidth={2.5} strokeLinejoin="round" />
          <path className="boya" d="M108 206 C116 206 124 208 130 212 L130 222 L108 222 C106 216 106 210 108 206 Z" fill={KEMIK} stroke={KEMIK_K} strokeWidth={2.5} strokeLinejoin="round" />
          <path className="boya" d="M108 272 L124 272 C140 274 150 286 150 300 C150 310 140 316 126 314 C114 312 106 304 104 292 C103 284 104 277 108 272 Z" fill={KEMIK} stroke={KEMIK_K} strokeWidth={2.5} strokeLinejoin="round" />
        </g>

        {/* ——— kafa tabanı (ön kafa çukuru tabanı → sfenoid → klivus) */}
        <g {...o('nk-kafa-tabani')}>
          <path className="boya" d="M128 98 C142 90 166 86 220 86 C300 88 346 92 370 106 C412 118 456 142 486 176 L500 198 L488 202 C470 176 440 152 405 132 C385 125 370 121 358 119 C340 102 300 96 220 96 C182 96 162 100 150 106 C140 108 134 106 128 102 Z" fill={KEMIK} stroke={KEMIK_K} strokeWidth={2.5} strokeLinejoin="round" />
        </g>

        {/* ——— burun boşluğu (hava) + konkalar */}
        <g {...o('nk-burun-bosluk')}>
          <path className="boya" d="M150 212 L345 196 L362 197 L362 124 C340 104 300 100 220 98 C182 98 162 102 152 108 C132 130 120 160 116 184 L150 194 Z" fill={LUMEN} />
          <path d="M152 108 C162 102 182 98 220 98 C300 100 340 104 362 124" stroke={MUKOZA_K} strokeWidth={2.5} fill="none" strokeLinecap="round" />
          <path d="M152 108 C132 130 120 160 116 184" stroke={MUKOZA_K} strokeWidth={2.5} fill="none" strokeLinecap="round" />
          {/* alt konka (alt kenarı F − 17), orta konka, üst konka */}
          <path className="boya" d="M182 191 C172 186 174 176 186 176 L332 164 C344 163 348 176 338 179 Z" fill="url(#kmb-2b-mukoza)" stroke={MUKOZA_K} strokeWidth={2.5} strokeLinejoin="round" />
          <path className="boya" d="M204 160 C194 156 196 146 208 146 L322 136 C334 135 338 147 328 150 Z" fill="url(#kmb-2b-mukoza)" stroke={MUKOZA_K} strokeWidth={2.5} strokeLinejoin="round" />
          <path d="M270 128 C262 124 266 117 276 117 L318 114 C328 114 330 124 322 125 Z" fill="url(#kmb-2b-mukoza)" stroke={MUKOZA_K} strokeWidth={2.5} strokeLinejoin="round" />
        </g>

        {/* ——— burun deliği + vestibül */}
        <g {...o('nk-burun-delik')}>
          <path className="boya" d="M80 192 C90 186 104 183 116 183 L150 194 L150 212 C130 210 112 204 100 199 Z" fill={LUMEN} />
          <path className="boya-cizgi" d="M72 193 C76 186 84 182 96 182 C106 182 114 184 118 186" stroke="#8a4f33" strokeWidth={3} fill="none" strokeLinecap="round" />
          <path d="M100 199 C112 204 130 210 150 212" stroke={MUKOZA_K} strokeWidth={2} fill="none" strokeLinecap="round" />
        </g>

        {/* ——— sert damak: burun tabanı (üst yüz = F) ve ağız tavanı */}
        <g {...o('nk-sert-damak')}>
          <path className="boya" d="M118 210 L150 212 L345 196 L345 211 L150 228 C136 230 126 228 118 222 Z" fill={KEMIK} stroke={KEMIK_K} strokeWidth={2.5} strokeLinejoin="round" />
        </g>

        {/* ——— nazofarinks (hava): koana arkası, kafa tabanının altı, yumuşak damağın üstü */}
        <g {...o('nk-nazofarinks')}>
          <path className="boya" d="M360 124 C405 128 445 148 466 182 C474 200 474 220 474 255 L413 255 C398 218 372 198 345 196 L360 196 Z" fill={LUMEN} />
          <path d="M360 124 C405 128 445 148 466 182 C474 200 474 220 474 255" stroke={MUKOZA_K} strokeWidth={2.5} fill="none" strokeLinecap="round" />
        </g>

        {/* ——— orofarinks + hipofarinks (hava/yemek ortak yolu) */}
        <g {...o('nk-orofarinks')}>
          <path className="boya" d="M404 262 L413 255 L474 255 L474 392 L450 392 L448 374 L422 372 L416 362 C416 335 412 305 400 284 L404 272 Z" fill={LUMEN} />
          <path d="M474 255 L474 392" stroke={MUKOZA_K} strokeWidth={2.5} fill="none" strokeLinecap="round" />
          <path d="M400 284 C412 305 416 335 416 362" stroke={MUKOZA_K} strokeWidth={2} fill="none" strokeLinecap="round" />
        </g>

        {/* ——— dil (ağız tabanında, kökü orofarinksin ön duvarı) */}
        <g {...o('nk-dil')}>
          <path className="boya" d="M132 262 C168 250 228 246 300 244 C350 248 382 264 400 284 C412 305 416 335 416 362 L410 368 C398 368 388 364 378 358 C330 340 250 326 176 314 C160 306 154 292 156 278 C148 272 138 268 132 262 Z" fill="url(#kmb-2b-kas)" stroke="#8d2f28" strokeWidth={2.5} strokeLinejoin="round" />
          <path d="M180 290 C240 284 310 290 380 330" stroke="#8d2f28" strokeWidth={1.5} fill="none" opacity={0.5} strokeLinecap="round" />
        </g>

        {/* ——— yumuşak damak + uvula (sert damağın arkasından aşağı-arkaya sarkar) */}
        <g {...o('nk-yumusak-damak')}>
          <path className="boya" d="M345 196 C372 198 398 218 412 252 C416 262 412 270 405 270 C399 268 396 262 392 252 C384 236 368 222 345 211 Z" fill="url(#kmb-2b-mukoza)" stroke={MUKOZA_K} strokeWidth={2.5} strokeLinejoin="round" />
        </g>

        {/* ——— özofagus (arkada, omurganın önünde; sahnenin altına uzar) */}
        <g {...o('nk-ozofagus')}>
          <path className="boya" d="M450 390 L474 390 L474 650 L450 650 Z" fill="#fbeee9" />
          <path className="boya-cizgi" d="M450 392 L450 650 M474 390 L474 650" stroke={MUKOZA_K} strokeWidth={3} fill="none" strokeLinecap="round" />
          {[408, 432, 456, 480, 504, 528, 552, 576, 600, 624].map((y) => <path key={y} d={`M452 ${y} q4 4 0 8 M472 ${y + 10} q-4 4 0 8`} stroke={MUKOZA_K} strokeWidth={1.5} fill="none" opacity={0.6} />)}
        </g>

        {/* ——— larinks: tiroid kıkırdak (önde), lümen + ses telleri, aritenoid/krikoid lamina (arkada) */}
        <g {...o('nk-larinks')}>
          <path d="M422 372 L446 372 L446 434 L420 434 Z" fill={LUMEN} />
          <path className="boya" d="M398 378 C404 374 412 373 420 374 L420 432 L404 432 C398 420 396 396 398 378 Z" fill="url(#kmb-ng-kikirdak)" stroke="#a88f72" strokeWidth={2.5} strokeLinejoin="round" />
          <path className="boya" d="M446 374 C450 374 452 378 451 384 L450 444 L444 444 L444 376 Z" fill="url(#kmb-ng-kikirdak)" stroke="#a88f72" strokeWidth={2} strokeLinejoin="round" />
          {/* ses telleri (gerçek + yalancı) */}
          <path d="M420 398 C424 400 426 404 420 408 M444 398 C440 400 438 404 444 408" stroke={MUKOZA_K} strokeWidth={2.5} fill="#e8a39b" strokeLinejoin="round" />
          <path d="M420 384 C423 386 423 389 420 391 M444 384 C441 386 441 389 444 391" stroke={MUKOZA_K} strokeWidth={2} fill="none" />
          <path d="M404 436 L420 436 L420 446 L408 446 Z" fill="url(#kmb-ng-kikirdak)" stroke="#a88f72" strokeWidth={2} strokeLinejoin="round" />
        </g>

        {/* ——— trakea (önde; C halkaları ön duvarda, membranöz arka duvar özofagusa komşu) */}
        <g {...o('nk-trakea')}>
          <path className="boya" d="M420 434 L443 434 L443 650 L420 650 Z" fill={LUMEN} />
          <path className="boya-cizgi" d="M420 434 L420 650 M444 444 L444 650" stroke={MUKOZA_K} strokeWidth={2.5} fill="none" />
          {[452, 466, 480, 494, 508, 522, 536, 550, 564, 578, 592, 606, 620, 634].map((y) => <rect key={y} x={408} y={y} width={12} height={8} rx={3} fill="url(#kmb-ng-kikirdak)" stroke="#a88f72" strokeWidth={1.8} />)}
        </g>

        {/* ——— epiglot (açık: dil kökünün arkasında yukarı kalkık) */}
        <g {...o('nk-epiglot')}>
          <path className="boya" d="M417 374 C419 352 426 330 435 316 C439 311 444 315 441 322 C434 338 429 356 426 374 Z" fill="url(#kmb-ng-kikirdak)" stroke="#a88f72" strokeWidth={2.5} strokeLinejoin="round" />
        </g>
        {/* epiglot kapalı (yutkunma): arkaya-aşağı yatar, larinks girişini örter */}
        <g {...o('nk-epiglot-kapali')}>
          <path className="boya" d="M416 374 C424 362 436 360 446 366 C450 368 449 372 445 372 C436 368 428 369 425 375 Z" fill="url(#kmb-ng-kikirdak)" stroke="#a88f72" strokeWidth={2.5} strokeLinejoin="round" />
        </g>

        {/* ——— patoloji ve yardımcı katmanlar */}
        <g {...o('nk-yanik')}>
          {[[470, 270, 470, 302], [470, 322, 470, 350], [470, 410, 470, 436], [454, 452, 454, 478], [419, 300, 420, 326]].map(([x1, y1, x2, y2], i) => (
            <path key={i} className="boya-cizgi" d={`M${x1} ${y1} C${x1 + (i === 3 || i === 4 ? 2 : -2)} ${(y1 + y2) / 2 - 4} ${x2 + (i === 3 || i === 4 ? 2 : -2)} ${(y1 + y2) / 2 + 4} ${x2} ${y2}`} stroke="#7a2a1a" strokeWidth={5} fill="none" strokeLinecap="round" opacity={0.85} />
          ))}
        </g>
        <g {...o('nk-varis')}>
          <path className="boya-cizgi" d="M453 432 C451 440 455 446 453 454 C451 462 455 468 453 476 C451 484 455 490 453 498 C451 506 455 512 453 520 C451 528 455 534 453 542 C451 550 455 556 453 564 C451 572 455 578 453 586 L453 600" stroke="#5a3f9e" strokeWidth={3} fill="none" strokeLinecap="round" />
          <path className="boya-cizgi" d="M471 440 C473 448 469 454 471 462 C473 470 469 476 471 484 C473 492 469 498 471 506 C473 514 469 520 471 528 C473 536 469 542 471 550 C473 558 469 564 471 572 C473 580 469 586 471 594 L471 600" stroke="#5a3f9e" strokeWidth={3} fill="none" strokeLinecap="round" />
          {[[453, 446], [471, 470], [453, 490], [471, 500], [453, 530], [471, 560], [453, 576]].map(([x, y], i) => <circle key={i} cx={x} cy={y} r={2.6} fill="#7d63c4" stroke="#5a3f9e" strokeWidth={1} />)}
        </g>
        <g {...o('nk-su')}>
          <path className="boya" d="M304 244 C340 246 372 256 392 274 L398 282 C380 268 350 258 304 252 C296 250 296 245 304 244 Z" fill="#8fc7ff" fillOpacity={0.6} stroke="#3f84c8" strokeWidth={1.5} strokeOpacity={0.8} />
        </g>
        <g {...o('nk-kusmuk')}>
          <path className="boya" d="M452 650 L452 394 C452 384 458 378 462 376 C466 378 472 384 472 394 L472 650 Z" fill="#c9c35a" fillOpacity={0.45} stroke="#8f8a2c" strokeWidth={1.5} strokeOpacity={0.7} />
          <path d="M462 560 L462 418" stroke="#8f8a2c" strokeWidth={2.5} fill="none" markerEnd="url(#kmb-ng-ok)" strokeLinecap="round" />
          <path className="cz boya-cizgi" pathLength={1} d="M466 372 C466 352 440 350 434 380 L432 600" stroke="#c62828" strokeWidth={2.5} strokeDasharray="6 5" fill="none" strokeLinecap="round" markerEnd="url(#kmb-ng-ok-k)" />
        </g>
        <g {...o('nk-kirik')}>
          <path className="boya-cizgi" d="M100 112 L108 118 L100 122 L108 128 L100 133" stroke="#c62828" strokeWidth={2.5} fill="none" strokeLinejoin="round" strokeLinecap="round" />
          <path className="boya-cizgi" d="M112 206 L118 212 L112 216 L119 221" stroke="#c62828" strokeWidth={2.5} fill="none" strokeLinejoin="round" strokeLinecap="round" />
          <path className="boya-cizgi" d="M236 84 L242 90 L236 94 L244 99 M306 86 L312 92 L306 96 L314 100 M418 124 L428 126 L422 132 L432 136" stroke="#c62828" strokeWidth={2.5} fill="none" strokeLinejoin="round" strokeLinecap="round" />
        </g>

        {/* ——— sonda yolları (yanlışlar ince kırmızı tonla) */}
        <g {...o('nk-dil-kivrim')}>
          <Sonda d={KIVRIM_D} kontur="#a3485a" govde="#f6e3e6" />
        </g>
        <g {...o('nk-sonda-trakea')}>
          <Sonda d={TRAKEA_D} kontur="#c62828" govde="#fbe3e3" />
        </g>
        <g {...o('nk-sonda')}>
          <Sonda d={SONDA_D} />
          {/* dış uçta renkli bağlantı ağzı */}
          <path className="boya" d="M62 330 L78 330 L80 352 L60 352 Z" fill="#2e9e5b" stroke="#1f6b3e" strokeWidth={2} strokeLinejoin="round" />
        </g>
        <g {...o('nk-ok-duz')}>
          <path className="cz boya-cizgi" pathLength={1} d="M200 168 L318 158" stroke="#2f6fd6" strokeWidth={2.5} fill="none" strokeLinecap="round" markerEnd="url(#kmb-ng-ok)" />
        </g>
        <g {...o('nk-ok-asagi')}>
          <path className="cz boya-cizgi" pathLength={1} d="M440 206 L440 290" stroke="#2f6fd6" strokeWidth={2.5} fill="none" strokeLinecap="round" markerEnd="url(#kmb-ng-ok)" />
        </g>
      </g>
    </>
  ),
};

// ———————————————————————————————————————————————————— BURUN YAKIN PLANI
const NR_SONDA = 'M362 306 C360 340 330 365 285 380 C230 398 190 430 165 520';
const NITRIL = '#cfe3f4', NITRIL_K = '#3f6f9c';

const NgBurun: Sahne = {
  ad: 'Burun yakın planı (önden, alttan hafif bakış)',
  gizli: ['nr-sonda', 'nr-jel', 'nr-parmak', 'nr-ok-yukari', 'nr-flaster-burun', 'nr-flaster-sarim', 'nr-ek-bant', 'nr-kanama', 'nr-sapma'],
  etiket: {
    'nr-yuz': [110, 70, 'Yüz'],
    'nr-burun': [300, 120, 'Burun'],
    'nr-flaster-burun': [470, 150, 'Burun flasteri'],
    'nr-ok-yukari': [590, 300, 'Ucu kaldır'],
    'nr-kanama': [292, 298, 'Kanama'],
    'nr-delik-sol': [600, 240, 'Sol burun deliği'],
    'nr-delik-sag': [225, 250, 'Sağ burun deliği'],
    'nr-flaster-sarim': [215, 338, 'Sondaya sarım'],
    'nr-septum': [485, 350, 'Septum'],
    'nr-ek-bant': [140, 380, 'Ek bant'],
    'nr-parmak': [670, 410, 'Eldivenli parmak'],
    'nr-sonda': [80, 432, 'NG sonda'],
    'nr-jel': [300, 410, 'Jel'],
    'nr-sapma': [300, 478, 'Septum deviasyonu'],
  },
  Ciz: ({ o }) => (
    <>
      <NgDefs />
      <g {...o('nr-yuz')}>
        <rect className="boya" x={0} y={0} width={800} height={500} fill={DERI} />
        {/* yanaklar ve nazolabial çizgiler */}
        <path d="M250 300 C238 350 250 400 290 440" stroke={KONTUR_DERI} strokeWidth={2.5} fill="none" strokeLinecap="round" opacity={0.7} />
        <path d="M550 300 C562 350 550 400 510 440" stroke={KONTUR_DERI} strokeWidth={2.5} fill="none" strokeLinecap="round" opacity={0.7} />
        {/* göz altları (üst kenar) */}
        <path d="M150 40 C200 70 270 70 320 40" stroke={KONTUR_DERI} strokeWidth={2.5} fill="none" strokeLinecap="round" opacity={0.6} />
        <path d="M480 40 C530 70 600 70 650 40" stroke={KONTUR_DERI} strokeWidth={2.5} fill="none" strokeLinecap="round" opacity={0.6} />
        {/* filtrum + dudaklar */}
        <path d="M388 326 L382 396 M412 326 L418 396" stroke={KONTUR_DERI} strokeWidth={2} fill="none" opacity={0.55} />
        <path d="M322 428 C350 408 380 400 400 410 C420 400 450 408 478 428 C450 436 420 440 400 438 C380 440 350 436 322 428 Z" fill="#d98b80" stroke="#a85f5a" strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M322 428 C360 470 440 470 478 428 C450 438 350 438 322 428 Z" fill="#cf7d73" stroke="#a85f5a" strokeWidth={2.5} strokeLinejoin="round" />
      </g>
      <g {...o('nr-burun')}>
        <path className="boya" d="M372 -5 C368 80 360 160 352 222 C318 240 300 270 302 298 C304 322 330 332 352 328 C370 326 386 322 400 324 C414 322 430 326 448 328 C470 332 496 322 498 298 C500 270 482 240 448 222 C440 160 432 80 428 -5 Z" fill="url(#kmb-2b-deri-koyu)" stroke={KONTUR_DERI} strokeWidth={3} strokeLinejoin="round" />
        {/* burun ucu + kanat (ala) kıvrımları */}
        <path d="M352 236 C356 270 376 290 400 290 C424 290 444 270 448 236" stroke={KONTUR_DERI} strokeWidth={2} fill="none" opacity={0.55} />
        <path d="M330 262 C318 280 320 304 336 316 M470 262 C482 280 480 304 464 316" stroke={KONTUR_DERI} strokeWidth={2.5} fill="none" strokeLinecap="round" />
        <path d="M384 200 C390 230 392 250 390 262" stroke="#ffffff" strokeWidth={3} fill="none" strokeLinecap="round" opacity={0.5} />
      </g>
      <g {...o('nr-delik-sag')}>
        <path className="boya" d="M340 308 C340 298 354 294 368 296 C382 298 388 306 384 314 C380 320 366 322 352 320 C344 318 340 314 340 308 Z" fill="#5a2c22" stroke="#3a1a14" strokeWidth={2} />
      </g>
      <g {...o('nr-delik-sol')}>
        <path className="boya" d="M460 308 C460 298 446 294 432 296 C418 298 412 306 416 314 C420 320 434 322 448 320 C456 318 460 314 460 308 Z" fill="#5a2c22" stroke="#3a1a14" strokeWidth={2} />
      </g>
      <g {...o('nr-septum')}>
        <path className="boya" d="M390 296 C394 292 406 292 410 296 L412 318 C406 324 394 324 388 318 Z" fill="url(#kmb-2b-deri)" stroke={KONTUR_DERI} strokeWidth={2.5} strokeLinejoin="round" />
      </g>
      <g {...o('nr-sapma')}>
        <path className="boya-cizgi" d="M397 291 C420 298 422 314 403 324" stroke="#24100b" strokeWidth={5} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('nr-kanama')}>
        <path className="boya" d="M340 312 C337 318 336 326 338 332 C340 336 344 334 343 328 C342 322 344 316 344 312 Z" fill="#c62828" stroke="#8d1f1f" strokeWidth={1.5} />
        <circle cx={339} cy={341} r={2.5} fill="#c62828" />
      </g>
      <g {...o('nr-flaster-burun')}>
        {/* burun sırtından burun ucuna inen şerit */}
        <path className="boya" d="M386 140 L414 140 L412 280 C408 288 396 290 390 286 Z" fill="#ffffff" stroke="#a7b1bc" strokeWidth={2} strokeLinejoin="round" />
        <path d="M390 160 L410 160 M390 200 L410 200 M390 240 L410 240" stroke="#d3d9e0" strokeWidth={1.5} />
      </g>
      <g {...o('nr-sonda')}>
        <Sonda d={NR_SONDA} w={11} cz={false} />
        <path d="M362 306 L362 300" stroke="#3a1a14" strokeWidth={8} strokeLinecap="round" opacity={0.5} />
      </g>
      <g {...o('nr-jel')}>
        <path className="boya-cizgi" d="M362 312 C360 340 330 365 300 375" stroke="#8fc7ff" strokeOpacity={0.55} strokeWidth={17} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('nr-flaster-sarim')}>
        {/* aynı şeridin alt ucu: burun ucundan sondaya inen bant + sondanın çevresinde 2 sarım */}
        <path d="M398 282 C394 304 374 320 356 332" stroke="#a7b1bc" strokeWidth={11} fill="none" strokeLinecap="round" />
        <path className="boya-cizgi" d="M398 282 C394 304 374 320 356 332" stroke="#ffffff" strokeWidth={8} fill="none" strokeLinecap="round" />
        <rect className="boya" x={348} y={324} width={10} height={22} rx={2} transform="rotate(37 353 335)" fill="#ffffff" stroke="#a7b1bc" strokeWidth={1.8} />
        <rect className="boya" x={341} y={333} width={10} height={22} rx={2} transform="rotate(37 347 343)" fill="#ffffff" stroke="#a7b1bc" strokeWidth={1.8} />
      </g>
      <g {...o('nr-ek-bant')}>
        <path className="boya" d="M212 372 L250 384 L242 410 L204 398 Z" fill="#ffffff" stroke="#a7b1bc" strokeWidth={2} strokeLinejoin="round" />
      </g>
      <g {...o('nr-parmak')}>
        {/* el kadrajın sağ altından girer; başparmak + avuç, işaret parmağı kolumellanın altına (burun ucunu alttan yukarı iter) */}
        <path d="M470 520 C478 470 520 440 580 446 C640 452 680 480 690 520 Z" fill={NITRIL} stroke={NITRIL_K} strokeWidth={2.5} strokeLinejoin="round" />
        <Uzuv pts={[[640, 520], [606, 478], [576, 466]]} w={26} dolgu={NITRIL} kontur={NITRIL_K} />
        <Uzuv cls="boya-cizgi" pts={[[540, 510], [495, 452], [452, 394], [409, 337]]} w={26} dolgu={NITRIL} kontur={NITRIL_K} />
        {/* eldiven altından seçilen tırnak (parmak sırtında, uca yakın) */}
        <ellipse cx={421} cy={355} rx={6} ry={10} transform="rotate(-37 421 355)" fill="#e6f1fb" stroke={NITRIL_K} strokeWidth={1.5} opacity={0.9} />
      </g>
      <g {...o('nr-ok-yukari')}>
        <path className="cz boya-cizgi" pathLength={1} d="M524 330 L524 256" stroke="#2f6fd6" strokeWidth={3} fill="none" strokeLinecap="round" markerEnd="url(#kmb-ng-ok)" />
      </g>
    </>
  ),
};

export const SAHNELER_NG_A: Record<string, Sahne> = { 'ng-kesit': NgKesit, 'ng-burun': NgBurun };
