/**
 * KMB görsel asistan — SVG sahne kitaplığı v3 — 2B düz vektör çizgi film (docs/KMB_2B_STIL.md, 2026-11-01). Erkek burada; öteki 13 sahne sahneler_2b_a/b/c.tsx.
 * Her öge `o(id)` ile kimliklenir: asistan eylemleri (vurgula, çiz, renk, göster/gizle, etiket) ve sınavdaki
 * "sahnede bul" tıklamaları bu kimliklerle çalışır. Çizilebilir çizgiler `cz` sınıfı + pathLength=1 taşır;
 * renk eylemi `.boya` (dolgu) ve `.boya-cizgi` (çizgi) sınıflı parçaları boyar, diğer parçalar gerçek dokusunu korur.
 * Ortak degradeler <Ortak/> içinde (kimlikler kmb- önekli). Yeni sahne: docs/KMB_GORSEL_ASISTAN.md §5.
 */
import React from 'react';
import { type OgeDurum, type SahneDurum, type OgeProps, type Sahne, u, Ortak, Boru } from './sahneOrtak';
export type { OgeDurum, SahneDurum, OgeProps, Sahne };
export { u, Ortak, Boru };
import { SAHNELER_2B_A, MALZEMELER } from './sahneler_2b_a';
import { SAHNELER_2B_B } from './sahneler_2b_b';
import { SAHNELER_2B_C } from './sahneler_2b_c';
import { SAHNELER_NG_A } from './sahneler_ng_a';
import { SAHNELER_NG_B } from './sahneler_ng_b';
import { SAHNELER_NG_C } from './sahneler_ng_c';

/** Erkek (sırtüstü, yandan; baş solda, ön yüz yukarıda, ayaklar sağda → inferior = sağ, anterior = yukarı).
 *  Üretra: mesane boynu → prostatik (aşağı-sağ) → membranöz → bulbar (perinede, simfizin arka-altında öne kıvrılır) → penil (dik tutulan peniste yukarı) → meatus. */
const URETRA = 'M408 326 C420 334 432 344 442 356 L448 368 C456 384 488 382 488 352 L486 262 L482 140';
/** Kateter: dış uç (küvet üstü) → meatus → penil → bulbar → prostatik → boyun → balon → uç (mesane içi). `ciz` dıştan içe çizer. */
const KATETER_E = 'M704 196 L702 140 C700 100 684 74 650 72 L524 70 C500 70 484 74 484 96 L482 140 L486 262 L488 352 C488 382 456 384 448 368 L442 356 C432 344 420 334 408 326 L378 312 L356 300';
/** Düz vektör çizgi film stili (2026-11-01 referans: Foley illüstrasyonu): pürüzsüz dolgular, 2–3 px sıcak kontur, filtre yok.
 *  H462 düzeltmesi (2026-11-01, kullanıcı "mantıksal hatalar"): iç anatomi gövdeyle AYNI yönde (önceki çizimde ayakta dizilimdeydi);
 *  mesane simfizin arka-üstünde, prostat simfizin arkasında, penis eldivenli elle dik tutulur (işlem standardı), skrotum penis kökünün
 *  arka-altında perinede, uyluklar sağda örtü altında, küvet örtü üstünde, idrar yalnız kateter yerleşince lümen→küvete akar.
 *  Ölçek 1 cm ≈ 12 px: mesane 10×8 cm, prostat 3,3 cm, penis 3,5 × ~10 cm (+glans), testis 4,5×3 cm, 16 Fr kateter 6,5 px, balon 10 mL r≈17. */
const Erkek: Sahne = {
  ad: 'Erkek alt üriner sistem (yan kesit)',
  gizli: ['e-jel', 'e-kateter', 'e-balon-dogru', 'e-kivrim', 'e-enjektor', 'e-balon-yanlis'],
  etiket: {
    'e-mesane': [344, 224, 'Mesane'],
    'e-prostat': [540, 352, 'Prostat'],
    'e-sfinkter': [300, 430, 'Eksternal sfinkter'],
    'e-uretra': [566, 392, 'Üretra (~1 cm çap)'],
    'e-penil': [596, 196, 'Penis (korpuslar)'],
    'e-glans': [590, 150, 'Glans / prepisyum'],
    'e-meatus': [590, 106, 'Eksternal meatus'],
    'e-testis': [560, 304, 'Testis / epididim'],
    'e-jel': [606, 258, 'Lidokainli jel üretrada'],
    'e-balon-dogru': [330, 378, 'Balon mesanede ✓'],
    'e-balon-yanlis': [470, 432, 'Balon üretrada ✗'],
  },
  Ciz: ({ o }) => (
    <>
      <defs>
        <linearGradient id="kmb-e-deri" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#f3c8a3" /><stop offset="1" stopColor="#e2a37c" /></linearGradient>
        <linearGradient id="kmb-e-ortu" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#5aa893" /><stop offset="1" stopColor="#3f8a76" /></linearGradient>
        <linearGradient id="kmb-e-yatak" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#9fd3d6" /><stop offset="1" stopColor="#6fb4b9" /></linearGradient>
        <radialGradient id="kmb-e-mesane" cx="45%" cy="40%" r="70%"><stop offset="0" stopColor="#c9655a" /><stop offset="1" stopColor="#a8433a" /></radialGradient>
        <radialGradient id="kmb-e-idrar" cx="45%" cy="35%" r="75%"><stop offset="0" stopColor="#fbe58a" /><stop offset="1" stopColor="#efc53f" /></radialGradient>
        <linearGradient id="kmb-e-kateter" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stopColor="#f7c75a" /><stop offset="1" stopColor="#d9962a" /></linearGradient>
        <radialGradient id="kmb-e-balon" cx="40%" cy="35%" r="70%"><stop offset="0" stopColor="#ffffff" /><stop offset="1" stopColor="#d7dee6" /></radialGradient>
        <linearGradient id="kmb-e-eldiven" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#dcedf9" /><stop offset="1" stopColor="#b3d4ec" /></linearGradient>
      </defs>
      <rect x={0} y={0} width={800} height={500} fill="#ffffff" />
      {/* yatak */}
      <path d="M0 418 L800 418 L800 500 L0 500 Z" fill="url(#kmb-e-yatak)" />
      <path d="M0 418 L800 418" stroke="#4f9aa0" strokeWidth={3} />
      {/* hekimin ön kolu (eldivenli; palmin arkasından sol-üste, kadraj dışına) */}
      <path d="M440 186 L352 0" stroke="#3f6f9c" strokeWidth={62} strokeLinecap="round" />
      <path d="M440 186 L352 0" stroke="url(#kmb-e-eldiven)" strokeWidth={56} strokeLinecap="round" />
      {/* gövde: karın solda, alt karın simfize iner, penis kökü (452–494), skrotum, kasık kıvrımı, uyluk sağa */}
      <path d="M0 150 C90 128 180 130 260 150 C330 168 392 206 436 250 L452 262 L494 262 C520 262 560 254 590 262 C604 242 640 228 700 228 L800 230 L800 418 L0 418 Z" fill="url(#kmb-e-deri)" stroke="#b9805a" strokeWidth={2.5} strokeLinejoin="round" />
      {/* göbek deliği */}
      <path d="M120 132 C126 138 134 138 140 132" stroke="#b9805a" strokeWidth={2} fill="none" strokeLinecap="round" />
      {/* steril örtü (yeşil) uylukların üstünde; dalgalı kenar + kıvrımlar */}
      <path d="M598 214 C620 206 640 220 664 210 C690 200 712 218 740 208 C764 198 784 214 800 206 L800 418 L602 418 C598 380 604 320 598 214 Z" fill="url(#kmb-e-ortu)" stroke="#2f6f5f" strokeWidth={2.5} strokeLinejoin="round" />
      {[640, 690, 742].map((x) => <path key={x} d={`M${x} 250 C${x - 8} 300 ${x + 6} 360 ${x - 4} 414`} stroke="#2f6f5f" strokeWidth={1.6} fill="none" opacity={0.5} />)}
      {/* böbrek küvet (mavi) örtü üstünde, drenaj ucunun altında */}
      <path d="M644 212 C660 204 750 204 768 212 C774 222 766 234 752 234 L660 234 C646 234 638 222 644 212 Z" fill="#3f86c9" stroke="#1f4e79" strokeWidth={2.5} strokeLinejoin="round" />
      <path d="M654 212 C680 206 736 206 760 212" stroke="#9fcaf0" strokeWidth={3} strokeLinecap="round" fill="none" />
      {/* kesit penceresi: pelvis — koyu kesit kenarı, içinde açık doku; deri konturunun ≥6 px içinde kalır */}
      <path d="M254 206 C254 190 290 184 330 190 C370 198 406 224 440 264 C456 282 476 288 494 296 C506 322 506 362 498 392 C490 408 470 410 450 410 L300 412 C270 412 254 386 254 350 Z" fill="#e9b893" stroke="#9a5f3f" strokeWidth={3} strokeLinejoin="round" />
      <path d="M264 208 C264 196 292 192 330 198 C368 206 402 232 434 270 C450 286 470 294 486 302 C496 324 496 360 488 388 C482 400 466 402 450 402 L302 404 C276 404 264 384 264 350 Z" fill="#f6d7bd" />
      {/* simfiz pubis: derinin hemen altında, mesanenin önünde, prostatın üstünde */}
      <ellipse cx={438} cy={290} rx={11} ry={24} fill="#f1e6cf" stroke="#b9a479" strokeWidth={2} transform="rotate(28 438 290)" />
      <g {...o('e-mesane')}>
        <ellipse className="boya" cx={350} cy={296} rx={62} ry={50} fill="url(#kmb-e-mesane)" stroke="#7a2e26" strokeWidth={3} transform="rotate(18 350 296)" />
        {/* boyun: prostata doğru daralır */}
        <path d="M392 318 L414 334" stroke="#a8433a" strokeWidth={18} strokeLinecap="round" />
        <ellipse cx={350} cy={296} rx={51} ry={40} fill="url(#kmb-e-idrar)" transform="rotate(18 350 296)" />
        <path d="M318 268 C332 258 350 256 366 262" stroke="#fff6cf" strokeWidth={5} fill="none" strokeLinecap="round" opacity={0.85} />
        {/* trigon (boyun çevresi) */}
        <path d="M376 300 L396 322 L380 334" stroke="#9a4a40" strokeWidth={2} fill="none" strokeLinecap="round" opacity={0.8} />
      </g>
      <g {...o('e-prostat')}>
        <ellipse className="boya" cx={428} cy={341} rx={20} ry={18} fill="#d8977e" stroke="#9a5a44" strokeWidth={2.5} transform="rotate(35 428 341)" />
      </g>
      <g {...o('e-sfinkter')}>
        <ellipse className="boya" cx={445} cy={362} rx={13} ry={8} fill="#cf5a4c" stroke="#8d2f28" strokeWidth={2} transform="rotate(55 445 362)" />
      </g>
      {/* el: palm şaftın arkasında (önce çizilir), parmak uçları sağ kenarda, başparmak sol kenarda (şafttan sonra) */}
      <path d="M436 180 C436 170 448 168 470 168 L498 170 C504 172 504 262 498 262 L436 262 Z" fill="url(#kmb-e-eldiven)" stroke="#3f6f9c" strokeWidth={2.5} strokeLinejoin="round" />
      {/* penis: dik tutulur; korpuslar şaft, alt (ventral = sağ) yüzde spongiozum/üretra kanalı; glans + prepisyum halkası */}
      <g {...o('e-penil')}>
        <path className="boya" d="M452 262 L452 176 C452 170 458 168 473 168 C488 168 494 170 494 176 L494 262 Z" fill="#edb08c" stroke="#b9805a" strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M460 182 L460 256" stroke="#f7d2b6" strokeWidth={5} strokeLinecap="round" opacity={0.9} />
      </g>
      <g {...o('e-glans')}>
        <path className="boya" d="M448 174 C446 156 456 138 473 136 C490 138 500 156 498 174 C488 170 458 170 448 174 Z" fill="#d98580" stroke="#a85f5a" strokeWidth={2.5} strokeLinejoin="round" />
        <path d="M446 176 C450 180 458 182 466 182 M500 176 C496 180 488 182 480 182" stroke="#b9805a" strokeWidth={4} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('e-meatus')}><path className="boya" d="M477 139 C480 136 485 136 488 139" stroke="#7d2f2a" strokeWidth={3} fill="none" strokeLinecap="round" /></g>
      {/* el: parmak uçları (sağ kenar) + başparmak (sol kenar) */}
      {[186, 208, 230].map((y) => <rect key={y} x={490} y={y} width={22} height={18} rx={9} fill="url(#kmb-e-eldiven)" stroke="#3f6f9c" strokeWidth={2} />)}
      <path d="M448 252 C446 232 446 212 452 196" stroke="#3f6f9c" strokeWidth={21} strokeLinecap="round" fill="none" />
      <path d="M448 252 C446 232 446 212 452 196" stroke="#bfdcf2" strokeWidth={16} strokeLinecap="round" fill="none" />
      {/* skrotum: penis kökünün arka-altında, perinede uyluğa yaslı; testis + epididim (arkada) */}
      <g {...o('e-testis')}>
        <path d="M494 262 C498 224 548 208 582 222 C602 230 604 252 590 262 Z" fill="#edb08c" stroke="#b9805a" strokeWidth={2.5} strokeLinejoin="round" />
        <ellipse className="boya" cx={538} cy={240} rx={26} ry={16} fill="#eed0c7" stroke="#b07f78" strokeWidth={2} transform="rotate(-8 538 240)" />
        <path d="M560 228 C570 236 570 248 558 254" stroke="#c48a84" strokeWidth={5} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('e-uretra')}>
        <path d={URETRA} stroke="#8a3b33" strokeOpacity={0.55} strokeWidth={13} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path className="cz boya-cizgi" pathLength={1} d={URETRA} stroke="#f2b7b0" strokeWidth={8} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      </g>
      <g {...o('e-jel')}>
        <path className="cz boya-cizgi" pathLength={1} d="M482 140 L486 262 L488 352 C488 382 456 384 448 368" stroke="#8fc7ff" strokeWidth={10} strokeOpacity={0.6} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('e-kateter')}>
        <path d={KATETER_E} stroke="#b47a1a" strokeWidth={9} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path className="cz boya-cizgi" pathLength={1} d={KATETER_E} stroke="url(#kmb-e-kateter)" strokeWidth={6.5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        {/* uç: yuvarlak, balonun 2 cm ötesinde drenaj gözü */}
        <circle cx={356} cy={300} r={4.5} fill="#f7c75a" stroke="#b47a1a" strokeWidth={1.6} /><circle cx={361} cy={304} r={1.6} fill="#5a3a10" />
        {/* Y bağlantı: drenaj kolu küvete iner; valfli balon kanalı sağ-yukarı */}
        <path d="M560 70 L594 56" stroke="#b47a1a" strokeWidth={6} strokeLinecap="round" /><path d="M560 70 L594 56" stroke="#f7c75a" strokeWidth={3.5} strokeLinecap="round" />
        <rect x={592} y={50} width={12} height={9} rx={2} fill="#2f6fd6" transform="rotate(-22 598 54)" />
      </g>
      <g {...o('e-kivrim')}>
        <path className="cz boya-cizgi" pathLength={1} d="M704 196 L702 140 C700 100 684 74 650 72 L524 70 C500 70 484 74 484 96 L482 140 L486 262 L488 352 C490 372 470 388 458 374 C448 360 470 352 480 366" stroke="#f7c75a" strokeWidth={6.5} fill="none" strokeLinecap="round" />
      </g>
      <g {...o('e-balon-dogru')}>
        <circle className="boya" cx={378} cy={312} r={17} fill="url(#kmb-e-balon)" stroke="#2e9e5b" strokeWidth={3} />
        <ellipse cx={373} cy={306} rx={5} ry={3} fill="#fff" />
        {/* yerleşince idrar: lümende ince sarı akış → küvete damla → küvette idrar filmi */}
        <path d="M361 304 L378 312 L408 326 C420 334 432 344 442 356 L448 368 C456 384 488 382 488 352 L486 262 L482 140 L484 96 C484 74 500 70 524 70 L650 72 C684 74 700 100 702 140 L704 196" stroke="#efc53f" strokeWidth={2.2} fill="none" strokeLinecap="round" strokeLinejoin="round" opacity={0.95} />
        <ellipse cx={704} cy={204} rx={2.6} ry={4} fill="#efc53f" />
        <path d="M656 226 C680 220 736 220 758 226 L752 232 L660 232 Z" fill="#efc53f" opacity={0.85} />
      </g>
      <g {...o('e-balon-yanlis')}>
        <ellipse className="boya" cx={470} cy={372} rx={18} ry={13} fill="#e05a5a" fillOpacity={0.85} stroke="#8d1f1f" strokeWidth={3} />
        {[0, 60, 120, 180, 240, 300].map((a) => <path key={a} d={`M${470 + Math.cos(a * Math.PI / 180) * 22} ${372 + Math.sin(a * Math.PI / 180) * 17} l${Math.cos(a * Math.PI / 180) * 8} ${Math.sin(a * Math.PI / 180) * 8}`} stroke="#d23b3b" strokeWidth={2.5} strokeLinecap="round" />)}
      </g>
      <g {...o('e-enjektor')}>
        <g transform="translate(606 50) rotate(-22)">
          <rect x={0} y={-8} width={62} height={16} rx={3} fill="#eef3f8" stroke="#6b7a90" strokeWidth={1.8} />
          <rect x={4} y={-5} width={34} height={10} fill="#cfe6ff" />
          <rect x={62} y={-3} width={18} height={6} fill="#c9d3de" stroke="#6b7a90" strokeWidth={1} /><rect x={78} y={-9} width={5} height={18} rx={1.5} fill="#6b7a90" />
        </g>
      </g>
    </>
  ),
};

/** Tüm sahneler 2B düz çizgi film stilinde (eski gerçekçi çizimler 2026-11-01'de kaldırıldı; git geçmişinde). */
export const SAHNELER: Record<string, Sahne> = { erkek: Erkek, ...SAHNELER_2B_A, ...SAHNELER_2B_B, ...SAHNELER_2B_C, ...SAHNELER_NG_A, ...SAHNELER_NG_B, ...SAHNELER_NG_C };

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
  // Nazogastrik sonda (01, 2026-11-05) — sözleşme meds_temp/kmb/ng/SAHNE_SOZLESMESI.md
  'ng-kesit': ['nk-bas', 'nk-burun-delik', 'nk-burun-bosluk', 'nk-sert-damak', 'nk-yumusak-damak', 'nk-nazofarinks', 'nk-orofarinks', 'nk-dil', 'nk-epiglot', 'nk-larinks', 'nk-trakea', 'nk-ozofagus', 'nk-kafa-tabani', 'nk-yuz-kemik', 'nk-sonda', 'nk-sonda-trakea', 'nk-ok-duz', 'nk-ok-asagi', 'nk-epiglot-kapali', 'nk-su', 'nk-dil-kivrim', 'nk-kirik', 'nk-yanik', 'nk-varis', 'nk-kusmuk'],
  'ng-burun': ['nr-yuz', 'nr-burun', 'nr-delik-sag', 'nr-delik-sol', 'nr-septum', 'nr-sonda', 'nr-jel', 'nr-parmak', 'nr-ok-yukari', 'nr-flaster-burun', 'nr-flaster-sarim', 'nr-ek-bant', 'nr-kanama', 'nr-sapma'],
  'ng-govde': ['nb-govde', 'nb-bas', 'nb-burun', 'nb-kulak', 'nb-ksifoid', 'nb-mide', 'nb-olcu-1', 'nb-olcu-2', 'nb-sonda-olcu', 'nb-isaret', 'nb-sonda', 'nb-ozofagus', 'nb-epigastr', 'nb-stetoskop', 'nb-enjektor', 'nb-ses'],
  'ng-mide': ['nd-karin', 'nd-ozofagus', 'nd-mide', 'nd-mide-sivi', 'nd-duodenum', 'nd-epigastr', 'nd-sonda', 'nd-hava', 'nd-ses', 'nd-stetoskop', 'nd-enjektor', 'nd-su', 'nd-torba', 'nd-akis', 'nd-beslenme', 'nd-tipa'],
  'ng-malzeme': ['nm-sonda', 'nm-kalinlik', 'nm-beslenme', 'nm-jel', 'nm-vazelin', 'nm-enjektor-can', 'nm-enjektor-normal', 'nm-stetoskop', 'nm-flaster', 'nm-eldiven', 'nm-ortu', 'nm-poset', 'nm-torba', 'nm-su'],
  'ng-pozisyon': ['np-yatak', 'np-hasta', 'np-hekim', 'np-lavabo', 'np-ortu', 'np-poset', 'np-eldiven', 'np-el-bas', 'np-ok-egim', 'np-sonda', 'np-yardimci'],
};

export function SahneCiz({ sahne, durum, onSec, secilebilir, isaret, olcek = 1 }: {
  sahne: string;
  durum: SahneDurum;
  onSec?: (id: string) => void;
  secilebilir?: boolean;
  isaret?: { id: string; dogru: boolean } | null;
  /** kamera yakınlaşması (Hedefler filmi): etiketler bu kadar küçültülür ki ekranda aynı boyda kalsın */
  olcek?: number;
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
      {Object.entries(S.etiket).map(([id, [x0, y0, metin]]) => {
        if (!durum[id]?.etiket) return null;
        // etiket sahne kenarından taşmasın (kenardaki yapıların etiketi yarım görünüyordu): kutu çerçeve içine itilir
        const k = 1 / olcek;
        const yari = (metin.length * 4.6 + 10) * k;
        const x = Math.min(800 - 6 - yari, Math.max(6 + yari, x0));
        const y = Math.min(500 - 14, Math.max(20, y0));
        return (
          <g key={`e-${id}`} className="kmb-etiket">
            <rect x={x - yari} y={y - 17 * k} width={yari * 2} height={28 * k} rx={14 * k} />
            <text x={x} y={y + 3 * k} textAnchor="middle" style={olcek !== 1 ? { fontSize: `${16 * k}px` } : undefined}>{metin}</text>
          </g>
        );
      })}
    </svg>
  );
}
