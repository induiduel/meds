/**
 * KMB 3B sahne tanımları — 2. küme: mesane/karın (yan kesit), kadın dış genital, yakın plan vestibül, steril el, glans ve jel,
 * malzeme tepsisi, kateter kesiti ve French ölçüsü, pelvis travması, hasta pozisyonu ve mahremiyet, eğitim maketi.
 * Kimlikler sahneler.tsx SAHNE_OGELERI ile birebir. Ölçek ve kamera sözleşmesi sahneler3b.ts ile aynı.
 */
import * as THREE from 'three';
import type { Sahne3BTanim } from './Sahne3B';
import { M, Oge3, V, akis, egri, halka, kapsul, kateter, kure, kutu, mesh, ok, silindir, tornaYumusak, tup, yazi, yumru, yuvarlakKutu, puruz, derece } from './yardimci';

const o3 = (id: string) => new Oge3(id);
const grup = (...o: THREE.Object3D[]) => { const g = new THREE.Group(); g.add(...o); return g; };

/** Stilize insan (Pixar oranları: büyük baş, yumuşak gövde). `yatan` → sırtüstü; bacak açıları dizi/kalça için radyan */
function insan(o: { deri?: THREE.Material; giysi?: THREE.Material; yatan?: boolean; bacak?: [number, number]; kol?: number; olcek?: number }) {
  const deri = o.deri || M.deri(), giysi = o.giysi || M.onluk();
  const g = new THREE.Group();
  const bas = kure(0.62, deri, 32); bas.position.y = 3.35; g.add(bas);
  const sac = mesh(new THREE.SphereGeometry(0.64, 32, 16, 0, Math.PI * 2, 0, derece(95)), M.koyu()); sac.position.y = 3.42; g.add(sac);
  const boyun = silindir(0.2, 0.22, 0.4, deri); boyun.position.y = 2.75; g.add(boyun);
  const govde = kapsul(0.75, 1.5, giysi); govde.position.y = 1.7; g.add(govde);
  const kalca = yumru(0.8, 0.55, 0.6, giysi); kalca.position.y = 0.75; g.add(kalca);
  for (const s of [-1, 1]) {
    const kol = kapsul(0.2, 1.3, deri); kol.position.set(s * 0.95, 1.6, 0); kol.rotation.z = s * (o.kol ?? derece(12)); g.add(kol);
    const el = kure(0.24, deri, 16); el.position.set(s * 1.05, 0.7, 0); g.add(el);
    const [kalcaA, dizA] = o.bacak || [0, 0];
    const uyluk = new THREE.Group(); uyluk.position.set(s * 0.38, 0.35, 0); uyluk.rotation.x = kalcaA; uyluk.rotation.z = s * (o.bacak ? derece(22) : derece(3));
    const uy = kapsul(0.3, 1.5, deri); uy.position.y = -0.9; uyluk.add(uy);
    const diz = new THREE.Group(); diz.position.y = -1.75; diz.rotation.x = dizA; uyluk.add(diz);
    const bal = kapsul(0.24, 1.5, deri); bal.position.y = -0.85; diz.add(bal);
    const ayak = yumru(0.26, 0.16, 0.45, deri); ayak.position.set(0, -1.75, 0.2); diz.add(ayak);
    g.add(uyluk);
  }
  if (o.yatan) { g.rotation.x = -Math.PI / 2; }
  g.scale.setScalar(o.olcek ?? 1);
  return g;
}
/** Eldivenli el: avuç + 5 parmak; `kivrim` parmak bükülmesi */
function el(m: THREE.Material, kivrim = 0.5, bas = 1) {
  const g = new THREE.Group();
  const avuc = yuvarlakKutu(1.7, 1.9, 0.55, 0.4, m); g.add(avuc);
  for (let i = 0; i < 4; i++) {
    const x = -0.6 + i * 0.4; const boy = [1.2, 1.45, 1.35, 1.05][i];
    const p1 = new THREE.Group(); p1.position.set(x, 0.95, 0); p1.rotation.x = -kivrim;
    const s1 = kapsul(0.17, boy * 0.55, m); s1.position.y = boy * 0.3; p1.add(s1);
    const p2 = new THREE.Group(); p2.position.y = boy * 0.6; p2.rotation.x = -kivrim * 1.2; const s2 = kapsul(0.15, boy * 0.45, m); s2.position.y = boy * 0.25; p2.add(s2); p1.add(p2);
    g.add(p1);
  }
  const bp = new THREE.Group(); bp.position.set(-0.95 * bas, 0.2, 0.1); bp.rotation.z = derece(35) * bas; bp.rotation.x = -kivrim * 0.6;
  const b1 = kapsul(0.19, 0.6, m); b1.position.y = 0.35; bp.add(b1); const b2 = kapsul(0.17, 0.5, m); b2.position.y = 0.95; b2.rotation.x = -0.4; bp.add(b2); g.add(bp);
  const bilek = silindir(0.42, 0.5, 0.9, m); bilek.position.y = -1.3; g.add(bilek);
  return g;
}
/** Sarmal (kateter halkası): r yarıçapında tur sayısı kadar dönen eğri */
const sarmal = (r: number, tur: number, yuk = 0.08, n = 120) => new THREE.CatmullRomCurve3(Array.from({ length: n }, (_, i) => { const a = (i / (n - 1)) * Math.PI * 2 * tur; return V(Math.cos(a) * r * (1 + 0.04 * Math.sin(a * 3)), (i / (n - 1)) * yuk * tur, Math.sin(a) * r); }));
/** Delikli örtü: dikdörtgen + elips pencere (ExtrudeGeometry, delikli şekil) */
function delikliOrtu(w: number, h: number, dx: number, dy: number, m: THREE.Material) {
  const s = new THREE.Shape(); s.moveTo(-w / 2, -h / 2); s.lineTo(w / 2, -h / 2); s.lineTo(w / 2, h / 2); s.lineTo(-w / 2, h / 2); s.closePath();
  const d = new THREE.Path(); d.absellipse(0, 0, dx, dy, 0, Math.PI * 2, false, 0); s.holes.push(d);
  const g = new THREE.ExtrudeGeometry(s, { depth: 0.08, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.03, bevelSegments: 2, curveSegments: 24 });
  return mesh(g, m);
}
/** Enjektör: gövde (saydam) + sıvı + piston + çubuk + uç; `boy` mL ölçeği */
function enjektor(boy: number, cap: number, ucGenis = false) {
  const g = new THREE.Group();
  const gov = silindir(cap, cap, boy, M.plastik()); gov.rotation.z = Math.PI / 2; gov.position.x = boy / 2; g.add(gov);
  const sivi = silindir(cap * 0.86, cap * 0.86, boy * 0.55, M.izotonik()); sivi.rotation.z = Math.PI / 2; sivi.position.x = boy * 0.33; sivi.castShadow = false; g.add(sivi);
  const piston = silindir(cap * 0.86, cap * 0.86, 0.18, M.koyu()); piston.rotation.z = Math.PI / 2; piston.position.x = boy * 0.62; g.add(piston);
  const cubuk = kutu(boy * 0.6, cap * 0.3, cap * 0.3, M.plastikMat()); cubuk.position.x = boy * 0.92; g.add(cubuk);
  const bas = kutu(0.08, cap * 2.1, cap * 2.1, M.plastikMat()); bas.position.x = boy * 1.22; g.add(bas);
  const flans = kutu(0.08, cap * 2.6, cap * 2.6, M.plastikMat()); flans.position.x = boy; g.add(flans);
  const uc = silindir(ucGenis ? cap * 0.45 : cap * 0.18, ucGenis ? cap * 0.3 : cap * 0.22, ucGenis ? 1.0 : 0.5, M.plastikMat()); uc.rotation.z = Math.PI / 2; uc.position.x = ucGenis ? -0.5 : -0.25; g.add(uc);
  for (let i = 1; i < 8; i++) { const c = kutu(0.025, 0.02, cap * 1.1, M.koyu()); c.position.set((boy * i) / 8, cap, 0); g.add(c); }
  return g;
}

// ———————————————————————————————————————— Mesane, suprapubik bölge ve idrar takibi (yan kesit)
const Mesane: Sahne3BTanim = {
  ad: 'Mesane, suprapubik bölge ve idrar takibi (yan kesit)',
  gizli: ['g-mesane-dolu', 'g-sisme', 'g-torba', 'g-akis', 'g-kultur', 'g-ilac', 'g-kucuk', 'g-el', 'g-us', 'g-us-dalga'],
  etiket: {
    'g-mesane-normal': 'Mesane', 'g-mesane-dolu': 'Dolu mesane (glob)', 'g-sisme': 'Suprapubik kabarıklık', 'g-torba': 'İdrar torbası', 'g-kultur': 'Steril kültür kabı',
    'g-ilac': 'Mesane içine ilaç / opak madde', 'g-kucuk': 'Sistit: 15–20 mL, ödemli duvar', 'g-el': 'Suprapubik palpasyon', 'g-us': 'Ultrason probu',
  },
  kamera: { poz: [1.6, 1.2, 27], hedef: [1.6, -0.6, 0] },
  kur: () => {
    const L: Oge3[] = [];
    const zemin = o3('_zemin');
    const deri = yuvarlakKutu(16, 12, 1.0, 0.9, M.deriKesit()); deri.position.set(0.5, 0.5, -1.2); deri.receiveShadow = true; zemin.ekle(deri);
    const yagM = M.yag(); yagM.color.setHex(0xf3e2b8); const yag = yuvarlakKutu(15.2, 11.2, 0.3, 0.8, yagM); yag.position.set(0.5, 0.5, -0.6); zemin.ekle(yag);
    // karın ön duvarı (sağda, dikey kalın şerit: deri + kas) ve simfiz
    const duvar = yuvarlakKutu(1.3, 9.5, 1.4, 0.5, M.deri()); duvar.position.set(4.6, 1.2, 0); zemin.ekle(duvar);
    const kas = yuvarlakKutu(0.6, 8.6, 1.2, 0.3, M.kas()); kas.position.set(3.75, 1.0, 0); zemin.ekle(kas);
    const simfiz = yumru(0.7, 1.05, 0.75, M.kemik()); simfiz.position.set(3.9, -3.6, 0); zemin.ekle(simfiz);
    const sakrum = tup(egri([[-5.2, 5.4, 0], [-5.8, 3.0, 0], [-5.6, 0.4, 0], [-4.8, -2.2, 0]]), 0.62, M.kemik(), 32, 14); zemin.ekle(sakrum);
    const rekM = M.korpus(); rekM.color.setHex(0xc0917d); const rektum = tup(egri([[-4.0, 5.4, -0.2], [-4.0, 2.0, -0.2], [-3.7, -1.2, -0.2], [-3.3, -3.6, -0.2]]), 0.7, rekM, 24, 14); zemin.ekle(rektum);
    // üretra + prostat (alt)
    const prostat = yumru(1.0, 0.85, 0.9, M.prostat()); prostat.position.set(0.0, -3.6, 0); zemin.ekle(prostat);
    const uretra = tup(egri([[0, -2.6, 0], [0, -3.8, 0], [0.3, -4.9, 0], [1.4, -5.4, 0]]), 0.2, M.mukoza(), 24, 10); zemin.ekle(uretra);
    L.push(zemin);
    const normM = M.mesane(); const norm = o3('g-mesane-normal').boya(normM);
    const nK = tornaYumusak([[0, -1.3], [0.9, -1.25], [1.6, -0.6], [1.85, 0.3], [1.6, 1.2], [0.9, 1.7], [0, 1.8]], normM); nK.position.set(0, -1.1, 0); norm.ekle(nK);
    const nI = tornaYumusak([[0, -1.1], [0.8, -1.05], [1.4, -0.5], [1.6, 0.3], [1.35, 1.0], [0, 1.4]], M.idrar()); nI.position.set(0, -1.1, 0); nI.castShadow = false; norm.ekle(nI);
    norm.etiketNoktasi = V(0, 0.9, 0.8); L.push(norm);
    const doluM = M.mesane(); doluM.color.setHex(0xe8a69c); const dolu = o3('g-mesane-dolu').boya(doluM);
    const dK = tornaYumusak([[0, -1.4], [1.6, -1.3], [2.9, -0.2], [3.3, 1.6], [3.0, 3.6], [1.9, 5.0], [0, 5.3]], doluM); dK.position.set(0.2, -1.0, 0); dolu.ekle(dK);
    const dI = tornaYumusak([[0, -1.2], [1.4, -1.1], [2.6, -0.1], [3.0, 1.6], [2.7, 3.4], [1.6, 4.6], [0, 4.9]], M.idrar()); dI.position.set(0.2, -1.0, 0); dI.castShadow = false; dolu.ekle(dI);
    dolu.etiketNoktasi = V(0.2, 4.6, 0.8); L.push(dolu);
    const sisM = M.deri(); const sis = o3('g-sisme').boya(sisM); const sK = yumru(0.9, 2.6, 1.2, sisM); sK.position.set(5.1, 1.6, 0); sis.ekle(sK); sis.etiketNoktasi = V(5.9, 1.6, 0.8); L.push(sis);
    const kucM = M.mesane(); kucM.color.setHex(0xd87a74); const kuc = o3('g-kucuk').boya(kucM);
    const kK = tornaYumusak([[0, -0.9], [0.7, -0.85], [1.2, -0.3], [1.3, 0.3], [1.1, 0.9], [0.6, 1.25], [0, 1.3]], kucM); kK.position.set(0, -1.1, 0); kuc.ekle(kK);
    const kI = yumru(0.45, 0.3, 0.45, M.idrar()); kI.position.set(0, -1.6, 0); kuc.ekle(kI); kuc.etiketNoktasi = V(0, 0.4, 0.9); L.push(kuc);
    // kateter + akış + torba
    const kat = tup(egri([[0, -0.2, 0.2], [0, -3.0, 0.2], [0.3, -4.9, 0.2], [1.4, -5.6, 0.2], [3.5, -5.9, 0.6], [6.2, -5.6, 1.2], [7.6, -4.6, 1.4]]), 0.16, M.silikon(), 80, 10); zemin.ekle(kat);
    const ak = o3('g-akis'); const akA = akis(egri([[0, -0.6, 0.25], [0, -3.0, 0.25], [0.3, -4.9, 0.25], [1.4, -5.6, 0.25], [3.5, -5.9, 0.65], [6.2, -5.6, 1.25], [7.6, -4.6, 1.45]]), 16, 0.1, M.idrarMat()); ak.ekle(akA); ak.cizici = (f) => akA.ilerle(f); ak.tik = (t) => akA.tik(t, 0); L.push(ak);
    const torba = o3('g-torba'); const tg = new THREE.Group(); tg.position.set(8.6, -3.2, 1.4); tg.rotation.y = derece(-20);
    const tM = M.plastik(); tM.transmission = 0.6; const tK = yuvarlakKutu(3.0, 3.8, 0.5, 0.3, tM); tg.add(tK);
    const idr = yuvarlakKutu(2.7, 1.5, 0.36, 0.2, M.idrarMat()); idr.position.y = -1.05; tg.add(idr);
    const ol = yazi('250 · 500 · 750', 44, '#5b6676'); ol.scale.set(0.7, 0.18, 1); ol.rotation.z = Math.PI / 2; ol.position.set(1.2, 0.3, 0.3); tg.add(ol);
    torba.ekle(tg); torba.boya(tM); L.push(torba);
    const kul = o3('g-kultur'); const kg = new THREE.Group(); kg.position.set(6.4, -6.0, 2.4);
    const kap = silindir(0.55, 0.5, 1.2, M.plastik()); kap.position.y = 0.6; kg.add(kap); const kapak = silindir(0.6, 0.6, 0.22, M.kirmizi()); kapak.position.y = 1.3; kg.add(kapak);
    const ornek = silindir(0.48, 0.44, 0.5, M.idrarMat()); ornek.position.y = 0.3; kg.add(ornek); kul.ekle(kg); kul.etiketNoktasi = V(0, 1.7, 0.4); L.push(kul);
    const ilac = o3('g-ilac'); const ilA = akis(egri([[0, 2.4, 0.3], [0, 1.2, 0.3], [0, -0.2, 0.3], [0.2, -1.2, 0.3]]), 8, 0.12, M.mavi()); ilac.ekle(ilA); ilac.cizici = (f) => ilA.ilerle(f); ilac.tik = (t) => ilA.tik(t, 0); ilac.etiketNoktasi = V(0, 2.6, 0.5); L.push(ilac);
    const elO = o3('g-el'); const elG = el(M.eldiven(), 0.15, 1); elG.scale.setScalar(0.9); elG.position.set(6.0, 1.8, 1.0); elG.rotation.set(derece(-80), derece(0), derece(90)); elO.ekle(elG); elO.etiketNoktasi = V(6.4, 2.9, 1.0); L.push(elO);
    const us = o3('g-us'); const usG = new THREE.Group(); usG.position.set(5.9, 1.4, 0.6); usG.rotation.z = derece(-90);
    const prob = yuvarlakKutu(1.1, 2.4, 0.9, 0.35, M.plastikMat()); usG.add(prob); const probUc = yuvarlakKutu(1.3, 0.5, 1.0, 0.2, M.koyu()); probUc.position.y = -1.4; usG.add(probUc);
    const kablo = tup(egri([[0, 1.2, 0], [0.3, 2.6, 0.2], [1.2, 3.8, 0.4]]), 0.08, M.koyu(), 16, 8); usG.add(kablo); us.ekle(usG); L.push(us);
    const dal = o3('g-us-dalga'); const dM = M.mavi(); dM.transparent = true; dM.opacity = 0.28; dM.depthWrite = false; dal.boya(dM);
    const kama = mesh(new THREE.ConeGeometry(2.6, 5.2, 24, 1, true), dM); kama.rotation.z = derece(90); kama.position.set(2.0, 1.2, 0.3); kama.castShadow = false; dal.ekle(kama); L.push(dal);
    return L;
  },
};

// ———————————————————————————————————————— Kadın dış genital bölge (litotomide, önden)
const Kadin: Sahne3BTanim = {
  ad: 'Kadın dış genital bölge (litotomide, önden)',
  gizli: ['k-temizlik', 'k-ortu', 'k-halka', 'k-kateter', 'k-idrar'],
  etiket: { 'k-majus': 'Labium majus', 'k-minus': 'Labium minus', 'k-klitoris': 'Klitoris', 'k-meatus': 'Eksternal üretra ağzı (meatus)', 'k-vajina': 'Vajina girişi', 'k-ortu': 'Steril delikli örtü' },
  kamera: { poz: [0, 3.0, 18.5], hedef: [0, 0.2, 0] },
  zeminY: -6,
  kur: () => {
    const L: Oge3[] = [];
    const bump = puruz(3, 256, 0.25);
    const zemin = o3('_zemin');
    // perine ve uyluk içleri: yumuşak deri yüzeyi
    const periM = M.deri(); periM.bumpMap = bump; periM.bumpScale = 0.02;
    const peri = yumru(7.5, 6.5, 2.2, periM, 48); peri.position.set(0, -0.6, -1.9); peri.receiveShadow = true; zemin.ekle(peri);
    for (const s of [-1, 1]) { const uyluk = kapsul(2.0, 6, M.deri()); uyluk.position.set(s * 7.6, 2.2, -0.6); uyluk.rotation.z = s * derece(-30); uyluk.rotation.x = derece(-72); zemin.ekle(uyluk); }
    L.push(zemin);
    const majM = M.deri(); majM.color.setHex(0xe6b394); const maj = o3('k-majus').boya(majM);
    for (const s of [-1, 1]) { const m = yumru(1.15, 3.3, 1.1, majM); m.position.set(s * 2.3, -0.2, 0); m.rotation.z = s * derece(-6); maj.ekle(m); } maj.etiketNoktasi = V(-2.6, 3.0, 0.8); L.push(maj);
    const minM = M.mukoza(); minM.color.setHex(0xd98a86); const min = o3('k-minus').boya(minM);
    for (const s of [-1, 1]) { const m = yumru(0.55, 2.6, 0.7, minM); m.position.set(s * 1.1, -0.4, 0.55); m.rotation.z = s * derece(-4); min.ekle(m); } min.etiketNoktasi = V(1.3, 2.0, 1.2); L.push(min);
    const kliM = M.glans(); const kli = o3('k-klitoris').boya(kliM); const kK = kure(0.3, kliM, 24); kK.position.set(0, 2.05, 0.9); kli.ekle(kK);
    const kapu = yumru(0.42, 0.5, 0.35, M.deri()); kapu.position.set(0, 2.25, 0.75); kli.ekle(kapu); L.push(kli);
    // vestibül zemini (mukoza), meatus (küçük), vajina (geniş)
    const vest = yumru(0.75, 2.2, 0.4, M.mukoza()); vest.position.set(0, -0.4, 0.5); zemin.ekle(vest);
    const meaM = M.koyu(); meaM.color.setHex(0x7a2f2c); const mea = o3('k-meatus').boya(meaM); const meK = yumru(0.16, 0.28, 0.12, meaM); meK.position.set(0, 1.1, 0.9); mea.ekle(meK); mea.etiketNoktasi = V(0, 1.3, 1.0); L.push(mea);
    const vajM = M.koyu(); vajM.color.setHex(0x8a3836); const vaj = o3('k-vajina').boya(vajM); const vK = yumru(0.42, 0.85, 0.2, vajM); vK.position.set(0, -0.9, 0.85); vaj.ekle(vK); vaj.etiketNoktasi = V(0, -1.9, 1.0); L.push(vaj);
    // temizlik: meatustan dışa dairesel silme yolu (povidon), 3 halka
    const tem = o3('k-temizlik'); const temM = M.povidon(); tem.boya(temM);
    const temT = tup(sarmal(1.0, 3, 0.0, 180).clone(), 0.12, temM, 180, 8); temT.scale.set(1.6, 1.2, 1); temT.rotation.x = Math.PI / 2; temT.position.set(0, 0.6, 1.05);
    // sarmal yarıçapı tur ilerledikçe büyüsün: eğriyi yeniden kur
    const spiral = new THREE.CatmullRomCurve3(Array.from({ length: 200 }, (_, i) => { const u = i / 199; const a = u * Math.PI * 2 * 3; const r = 0.35 + u * 2.0; return V(Math.cos(a) * r * 1.1, 1.1 + Math.sin(a) * r * 1.3, 1.0 + 0.1 * Math.sin(a)); }));
    const temT2 = tup(spiral, 0.13, temM, 200, 8); tem.ekle(temT2); tem.cizici = (f) => temT2.ilerle(f); void temT; tem.etiketNoktasi = V(2.4, 3.4, 1.2); L.push(tem);
    const ortu = o3('k-ortu'); const oM = M.ortu(); ortu.boya(oM); const oK = delikliOrtu(18, 14, 3.9, 4.9, oM); oK.position.set(0, 0.1, 1.3); ortu.ekle(oK); ortu.etiketNoktasi = V(-5, 4.5, 1.5); L.push(ortu);
    // kateter halkası (steril elde), kateter meatusa, idrar
    const hal = o3('k-halka'); const halM = M.silikon(); hal.boya(halM); const halT = tup(sarmal(1.0, 2.6, 0.12), 0.17, halM, 160, 12); halT.position.set(3.6, 3.0, 2.4); halT.rotation.x = derece(70); hal.ekle(halT); L.push(hal);
    const kat = o3('k-kateter'); const katM = M.silikon(); kat.boya(katM); const katK = kateter(egri([[4.0, 3.8, 3.0], [2.6, 2.6, 2.4], [1.2, 1.6, 1.6], [0.2, 1.15, 1.1], [0, 1.1, 0.6]]), 0.17, katM, 60); kat.ekle(katK); kat.cizici = (f) => katK.ilerle(f); L.push(kat);
    const idr = o3('k-idrar'); const idA = akis(egri([[0, 1.1, 0.8], [0.2, 1.15, 1.2], [1.2, 1.6, 1.7], [2.6, 2.6, 2.5], [4.0, 3.8, 3.1]]), 10, 0.1, M.idrarMat()); idr.ekle(idA); idr.cizici = (f) => idA.ilerle(f); idr.tik = (t) => idA.tik(t, 0); L.push(idr);
    return L;
  },
};

// ———————————————————————————————————————— Yakın plan: vestibül ve meatus (eldivenli parmaklar labiaları ayırıyor)
const YakinKadin: Sahne3BTanim = {
  ad: 'Yakın plan: vestibül ve meatus (eldivenli parmaklar labiaları ayırıyor)',
  gizli: ['v-kateter', 'v-jel', 'v-idrar', 'v-parmak'],
  etiket: { 'v-klitoris': 'Klitoris', 'v-meatus': 'Meatus: üstteki küçük açıklık', 'v-vajina': 'Vajina: alttaki geniş açıklık', 'v-minus': 'Labium minus', 'v-parmak': 'Başparmak + işaret parmağı ayırır', 'v-jel': 'Uçta ~2 mL jel' },
  kamera: { poz: [0, 2.5, 15], hedef: [0, 0.2, 0] },
  kur: () => {
    const L: Oge3[] = [];
    const bump = puruz(4, 256, 0.25);
    const zemin = o3('_zemin'); const zM = M.deri(); zM.bumpMap = bump; zM.bumpScale = 0.02; const z = yumru(9, 7, 2.5, zM, 48); z.position.set(0, 0, -2.3); z.receiveShadow = true; zemin.ekle(z);
    const vestM = M.mukoza(); vestM.bumpMap = bump; vestM.bumpScale = 0.015; const vest = yumru(1.6, 3.6, 0.8, vestM); vest.position.set(0, -0.3, 0.2); zemin.ekle(vest);
    L.push(zemin);
    const minM = M.mukoza(); minM.color.setHex(0xd98a86); const min = o3('v-minus').boya(minM);
    for (const s of [-1, 1]) { const m = yumru(0.8, 3.6, 0.9, minM); m.position.set(s * 2.3, -0.2, 0.3); m.rotation.z = s * derece(-10); min.ekle(m); } min.etiketNoktasi = V(-2.6, 3.0, 1.0); L.push(min);
    const kli = o3('v-klitoris'); const kM = M.glans(); kli.boya(kM); const kK = kure(0.42, kM, 24); kK.position.set(0, 2.9, 0.9); kli.ekle(kK); const kap = yumru(0.6, 0.65, 0.45, M.deri()); kap.position.set(0, 3.15, 0.75); kli.ekle(kap); L.push(kli);
    const meaM = M.koyu(); meaM.color.setHex(0x7a2f2c); const mea = o3('v-meatus').boya(meaM); const meK = yumru(0.26, 0.42, 0.15, meaM); meK.position.set(0, 1.4, 1.0); mea.ekle(meK); const meHalka = halka(0.4, 0.09, M.mukoza(), 32); meHalka.position.set(0, 1.4, 0.98); mea.ekle(meHalka); mea.etiketNoktasi = V(0, 1.75, 1.1); L.push(mea);
    const vajM = M.koyu(); vajM.color.setHex(0x8a3836); const vaj = o3('v-vajina').boya(vajM); const vK = yumru(0.75, 1.35, 0.25, vajM); vK.position.set(0, -1.2, 0.95); vaj.ekle(vK); vaj.etiketNoktasi = V(0, -2.7, 1.1); L.push(vaj);
    // parmaklar: sol elin başparmak ve işaret parmağı labiaları yanlara açar
    const par = o3('v-parmak'); const pM = M.eldivenSteril(); par.boya(pM);
    for (const s of [-1, 1]) { const p = kapsul(0.48, 2.6, pM); p.position.set(s * 3.3, -1.4, 1.6); p.rotation.z = s * derece(35); p.rotation.x = derece(-25); par.ekle(p); const t = kure(0.5, pM, 20); t.position.set(s * 2.55, -0.3, 1.9); par.ekle(t); }
    par.etiketNoktasi = V(3.6, -2.6, 2.0); L.push(par);
    const kat = o3('v-kateter'); const katM = M.silikon(); kat.boya(katM); const katK = kateter(egri([[5.5, 5.0, 4.0], [3.2, 3.2, 2.8], [1.2, 1.9, 1.8], [0.2, 1.45, 1.3], [0, 1.4, 0.7]]), 0.26, katM, 60); kat.ekle(katK); kat.cizici = (f) => katK.ilerle(f); L.push(kat);
    const jel = o3('v-jel'); const jM = M.jel(); jel.boya(jM); const jK = yumru(0.42, 0.42, 0.42, jM); jK.position.set(0.1, 1.45, 1.25); jK.castShadow = false; jel.ekle(jK); jel.etiketNoktasi = V(0.6, 2.0, 1.4); L.push(jel);
    const idr = o3('v-idrar'); const idA = akis(egri([[0, 1.4, 0.9], [0.2, 1.45, 1.5], [1.2, 1.9, 2.0], [3.2, 3.2, 3.0], [5.5, 5.0, 4.2]]), 10, 0.14, M.idrarMat()); idr.ekle(idA); idr.cizici = (f) => idA.ilerle(f); idr.tik = (t) => idA.tik(t, 0); L.push(idr);
    return L;
  },
};

// ———————————————————————————————————————— Yakın plan: steril eldivenle kateteri avuçta toplamak
const YakinEl: Sahne3BTanim = {
  ad: 'Yakın plan: steril eldivenle kateteri avuçta toplamak',
  gizli: ['h-yanlis', 'h-jel'],
  etiket: { 'h-el': 'Steril eldivenli el', 'h-halka': 'Kateter avuçta halka halinde', 'h-uc': 'Yalnız uç dışarıda, steril', 'h-yanlis': 'Sarkan kateter dokunur → steril değil', 'h-jel': 'Uca jel' },
  kamera: { poz: [0.5, 5.0, 13.5], hedef: [0.5, 0.0, 0.5] },
  zeminY: -2.4,
  kur: () => {
    const L: Oge3[] = [];
    const zemin = o3('_zemin'); const ortu = yuvarlakKutu(20, 14, 0.1, 0.5, M.ortuAcik()); ortu.rotation.x = -Math.PI / 2; ortu.position.y = -2.4; ortu.receiveShadow = true; zemin.ekle(ortu); L.push(zemin);
    const eM = M.eldivenSteril(); const elO = o3('h-el').boya(eM); const eG = el(eM, 1.15, 1); eG.scale.setScalar(1.6); eG.rotation.set(derece(-28), derece(-8), derece(12)); eG.position.set(0.3, -0.8, 0); elO.ekle(eG); elO.etiketNoktasi = V(-2.4, 0.4, 0.6); L.push(elO);
    const hM = M.silikon(); const hal = o3('h-halka').boya(hM); const hT = tup(sarmal(1.3, 2.8, 0.14), 0.19, hM, 180, 12); hT.position.set(0.3, 0.3, 1.2); hT.rotation.x = derece(-62); hal.ekle(hT); hal.etiketNoktasi = V(0.3, 1.9, 1.2); L.push(hal);
    const ucM = M.silikon(); const uc = o3('h-uc').boya(ucM); const ucK = kateter(egri([[1.6, 0.6, 1.4], [2.9, 1.0, 1.8], [4.2, 1.4, 2.2]]), 0.19, ucM, 30); uc.ekle(ucK); uc.etiketNoktasi = V(4.2, 2.0, 2.2); L.push(uc);
    const yan = o3('h-yanlis'); const yM = M.silikon(); yan.boya(yM); const yT = tup(egri([[-1.2, -0.2, 1.2], [-2.6, -1.4, 2.2], [-3.6, -2.3, 3.0], [-5.2, -2.35, 3.4]]), 0.19, yM, 60, 12); yan.ekle(yT); yan.cizici = (f) => yT.ilerle(f);
    const leke = yumru(0.9, 0.05, 0.6, M.kirmizi()); leke.position.set(-4.4, -2.34, 3.2); yan.ekle(leke); yan.etiketNoktasi = V(-4.4, -1.6, 3.2); L.push(yan);
    const jel = o3('h-jel'); const jM = M.jel(); jel.boya(jM); const jK = yumru(0.36, 0.3, 0.36, jM); jK.position.set(4.25, 1.42, 2.25); jK.castShadow = false; jel.ekle(jK); L.push(jel);
    return L;
  },
};

// ———————————————————————————————————————— Yakın plan: glans, meatus ve lidokainli jelin verilmesi
const YakinErkekJel: Sahne3BTanim = {
  ad: 'Yakın plan: glans, meatus ve lidokainli jelin verilmesi',
  gizli: ['j-temizlik', 'j-siringa', 'j-dolum', 'j-parmak'],
  etiket: { 'j-glans': 'Glans penis', 'j-prepisyum': 'Prepisyum geri çekilir', 'j-meatus': 'Meatus', 'j-temizlik': 'Meatustan dışa, 3 kez', 'j-siringa': 'Jel tüpü meatusta', 'j-dolum': 'Jel üretrayı doldurur', 'j-parmak': 'Ucu sık, 2–3 dk bekle' },
  kamera: { poz: [2.5, 3.5, 13], hedef: [1.5, 0, 0] },
  zeminY: -3.2,
  kur: () => {
    const L: Oge3[] = [];
    const bump = puruz(9, 256, 0.2);
    const zemin = o3('_zemin'); const ortu = yuvarlakKutu(22, 16, 0.1, 0.5, M.ortu()); ortu.rotation.x = -Math.PI / 2; ortu.position.y = -3.2; ortu.receiveShadow = true; zemin.ekle(ortu);
    // gövde (sol), yarı saydam kılıf içinde üretra görünür
    const govM = M.deri(); govM.bumpMap = bump; govM.bumpScale = 0.01; govM.transparent = true; govM.opacity = 0.92;
    const gov = kapsul(1.55, 6, govM); gov.rotation.z = Math.PI / 2; gov.position.set(-4.2, 0, 0); zemin.ekle(gov);
    const ure = tup(egri([[-7.5, -0.6, 0.3], [-4, -0.6, 0.3], [-1.3, -0.5, 0.3], [0.9, -0.3, 0.3]]), 0.24, M.mukoza(), 40, 10); zemin.ekle(ure);
    L.push(zemin);
    const glM = M.glans(); glM.bumpMap = bump; glM.bumpScale = 0.015; const gl = o3('j-glans').boya(glM); const gK = yumru(2.0, 1.75, 1.75, glM, 48); gK.position.set(0.5, 0, 0); gl.ekle(gK); gl.etiketNoktasi = V(0.5, 1.9, 0.6); L.push(gl);
    const prM = M.deri(); const pr = o3('j-prepisyum').boya(prM); const pK = halka(1.75, 0.45, prM, 48); pK.rotation.y = Math.PI / 2; pK.position.set(-1.6, 0, 0); pr.ekle(pK); pr.etiketNoktasi = V(-1.6, 2.3, 0.4); L.push(pr);
    const meM = M.koyu(); meM.color.setHex(0x7a2f2c); const me = o3('j-meatus').boya(meM); const mK = yumru(0.1, 0.42, 0.18, meM); mK.position.set(2.48, 0, 0); me.ekle(mK); me.etiketNoktasi = V(2.6, 0.6, 0.4); L.push(me);
    const tem = o3('j-temizlik'); const tM = M.povidon(); tem.boya(tM);
    const spiral = new THREE.CatmullRomCurve3(Array.from({ length: 160 }, (_, i) => { const u = i / 159; const a = u * Math.PI * 2 * 3; const r = 0.3 + u * 1.5; const yy = Math.cos(a) * r, zz = Math.sin(a) * r; const x = 2.4 - (yy * yy + zz * zz) * 0.33; return V(x, yy, zz); }));
    const tT = tup(spiral, 0.1, tM, 160, 8); tem.ekle(tT); tem.cizici = (f) => tT.ilerle(f); tem.etiketNoktasi = V(2.2, 2.1, 0.8); L.push(tem);
    const sir = o3('j-siringa'); const sg = new THREE.Group(); sg.position.set(2.75, 0, 0);
    const tupG = silindir(0.55, 0.55, 3.2, M.plastik()); tupG.rotation.z = Math.PI / 2; tupG.position.x = 2.1; sg.add(tupG);
    const jelIc = silindir(0.46, 0.46, 2.0, M.jel()); jelIc.rotation.z = Math.PI / 2; jelIc.position.x = 1.6; jelIc.castShadow = false; sg.add(jelIc);
    const ucG = mesh(new THREE.ConeGeometry(0.42, 0.9, 24), M.plastikMat()); ucG.rotation.z = Math.PI / 2; ucG.position.x = 0.1; sg.add(ucG);
    const pis = kutu(1.6, 0.18, 0.18, M.plastikMat()); pis.position.x = 4.4; sg.add(pis); const pb = kutu(0.1, 1.0, 1.0, M.plastikMat()); pb.position.x = 5.2; sg.add(pb);
    sir.ekle(sg); sir.etiketNoktasi = V(4.8, 0.9, 0.3); L.push(sir);
    const dol = o3('j-dolum'); const dT = tup(egri([[2.4, 0, 0.3], [0.9, -0.3, 0.3], [-1.3, -0.5, 0.3], [-4, -0.6, 0.3], [-7.4, -0.6, 0.3]]), 0.3, M.jel(), 60, 10); dol.ekle(dT); dol.cizici = (f) => dT.ilerle(f); dol.etiketNoktasi = V(-3.5, 0.2, 0.9); L.push(dol);
    const par = o3('j-parmak'); const pM = M.eldivenSteril(); par.boya(pM);
    for (const s of [-1, 1]) { const p = kapsul(0.5, 2.4, pM); p.position.set(1.9, s * 1.9, 1.6); p.rotation.x = s * derece(-40); p.rotation.z = derece(0); par.ekle(p); const t = kure(0.52, pM, 20); t.position.set(1.95, s * 1.75, 0.95); par.ekle(t); }
    par.etiketNoktasi = V(1.9, 2.8, 1.2); L.push(par);
    return L;
  },
};

// ———————————————————————————————————————— Üretral kateter malzeme tepsisi
const Malzeme: Sahne3BTanim = {
  ad: 'Üretral kateter malzeme tepsisi',
  gizli: ['m-steril-alan'],
  etiket: {
    'm-lateks': 'Lateks Foley kateter (sarı, kısa süreli)', 'm-silikon': 'Silikon Foley kateter (beyaz, uzun süreli)', 'm-nonsteril': 'Steril olmayan eldiven (temizlik)', 'm-steril': 'Steril eldiven (yerleştirme)',
    'm-jel': 'Lidokainli kayganlaştırıcı jel', 'm-izotonik': 'Steril izotonik 10 mL (balon)', 'm-enjektor': '10 mL enjektör (balon kanalı)', 'm-genis': '50 mL kateter uçlu enjektör',
    'm-antiseptik': 'Povidon iyot, böbrek küvet, gazlı bez, pens', 'm-ortu': 'Steril delikli örtü', 'm-torba': 'İdrar torbası 2000 mL',
  },
  kamera: { poz: [0, 19, 17], hedef: [0, 0, -0.8] },
  zeminY: -0.02,
  kur: () => {
    const L: Oge3[] = [];
    const zemin = o3('_zemin'); const tepsi = yuvarlakKutu(21, 14, 0.6, 0.8, M.tepsi()); tepsi.rotation.x = -Math.PI / 2; tepsi.position.y = -0.3; tepsi.receiveShadow = true; zemin.ekle(tepsi);
    const kenar = mesh(new THREE.TorusGeometry(1, 0.18, 8, 4), M.tepsi()); kenar.visible = false; zemin.ekle(kenar);
    L.push(zemin);
    // ızgara: 4 sütun × 3 sıra (SVG düzeniyle aynı sıra)
    const yer = (sut: number, sira: number) => V(-7.5 + sut * 5, 0, -4.2 + sira * 4.2);
    const paket = (p: THREE.Vector3, sarmalM: THREE.Material, yazim: string) => {
      const g = new THREE.Group(); g.position.copy(p);
      // steril paket: beyaz kâğıt sırt + kenarı görünen saydam film; kateter halkası üstte okunur
      const kart = yuvarlakKutu(4.2, 3.0, 0.08, 0.3, M.beyaz()); kart.rotation.x = -Math.PI / 2; kart.position.y = 0.04; g.add(kart);
      const filmM = M.plastik(); filmM.transmission = 0.3; filmM.opacity = 0.35; filmM.transparent = true; filmM.roughness = 0.1;
      const film = yuvarlakKutu(4.2, 3.0, 0.5, 0.3, filmM); film.rotation.x = -Math.PI / 2; film.position.y = 0.3; film.castShadow = false; g.add(film);
      const coil = tup(sarmal(0.95, 2.4, 0.03), 0.17, sarmalM, 140, 10); coil.position.set(0.3, 0.2, 0); g.add(coil);
      const uc = tup(egri([[1.2, 0.2, 0.3], [1.7, 0.2, 0.9], [1.9, 0.2, 1.3]]), 0.17, sarmalM, 20, 8); g.add(uc);
      const et = yazi(yazim, 54, '#3e4a58', '#ffffff'); et.scale.set(1.3, 0.33, 1); et.rotation.x = -Math.PI / 2; et.position.set(-1.1, 0.45, 1.05); g.add(et);
      return g;
    };
    const lat = o3('m-lateks'); const latM = M.lateks(); lat.boya(latM); lat.ekle(paket(yer(0, 0), latM, '16 Fr · lateks')); L.push(lat);
    const sil = o3('m-silikon'); const silM = M.silikon(); sil.boya(silM); sil.ekle(paket(yer(1, 0), silM, '16 Fr · silikon')); L.push(sil);
    const ns = o3('m-nonsteril'); const nsM = M.plastikMat(); ns.boya(nsM); const nsG = new THREE.Group(); nsG.position.copy(yer(2, 0));
    nsM.color.setHex(0x4f8fb5);
    const kutuG = yuvarlakKutu(3.0, 1.6, 2.2, 0.15, nsM); kutuG.position.y = 0.8; nsG.add(kutuG); const etik = yazi('NİTRİL · M', 56, '#1f4e79', '#ffffff'); etik.scale.set(0.6, 0.15, 1); etik.position.set(0, 0.8, 1.12); nsG.add(etik);
    const eld = yuvarlakKutu(1.2, 0.08, 1.6, 0.2, M.eldiven()); eld.position.set(0.3, 1.7, 0); eld.rotation.z = derece(12); nsG.add(eld); ns.ekle(nsG); ns.etiketNoktasi = V(0, 2.2, 0); L.push(ns);
    const st = o3('m-steril'); const stM = M.eldivenSteril(); st.boya(stM); const stG = new THREE.Group(); stG.position.copy(yer(3, 0));
    const zarfM = M.ortuAcik(); zarfM.color.setHex(0xbfd6ea);
    const zarf = yuvarlakKutu(3.4, 2.6, 0.12, 0.2, zarfM); zarf.rotation.x = -Math.PI / 2; zarf.position.y = 0.06; stG.add(zarf);
    const elG = el(stM, 0.1, 1); elG.scale.setScalar(0.55); elG.rotation.x = -Math.PI / 2; elG.position.set(-0.2, 0.2, 0.3); stG.add(elG);
    const elG2 = el(stM, 0.1, -1); elG2.scale.setScalar(0.55); elG2.rotation.x = -Math.PI / 2; elG2.position.set(0.9, 0.2, 0.3); stG.add(elG2); st.ekle(stG); st.etiketNoktasi = V(0, 1.2, 0); L.push(st);
    const jel = o3('m-jel'); const jM = M.plastikMat(); jel.boya(jM); const jG = new THREE.Group(); jG.position.copy(yer(0, 1));
    const tupJ = kapsul(0.55, 2.4, jM); tupJ.rotation.z = Math.PI / 2; tupJ.position.set(0, 0.55, 0); jG.add(tupJ); const kapJ = silindir(0.3, 0.3, 0.6, M.mavi()); kapJ.rotation.z = Math.PI / 2; kapJ.position.set(2.0, 0.55, 0); jG.add(kapJ);
    const jet = yazi('Lidokain %2 jel', 50, '#2f6fd6', '#ffffff'); jet.scale.set(0.9, 0.22, 1); jet.rotation.x = -Math.PI / 2; jet.position.set(0, 1.12, 0); jG.add(jet); jel.ekle(jG); jel.etiketNoktasi = V(0, 1.4, 0); L.push(jel);
    const izo = o3('m-izotonik'); const iM = M.plastik(); izo.boya(iM); const iG = new THREE.Group(); iG.position.copy(yer(1, 1));
    for (const x of [-1.1, 0, 1.1]) { const amp = tornaYumusak([[0, 0], [0.42, 0.02], [0.45, 1.3], [0.3, 1.7], [0.2, 1.9], [0.22, 2.3], [0, 2.32]], iM); amp.position.set(x, 0, 0); iG.add(amp); const siv = silindir(0.38, 0.38, 1.1, M.izotonik()); siv.position.set(x, 0.6, 0); siv.castShadow = false; iG.add(siv); const e = yazi('%0,9 · 10 mL', 52, '#3e4a58', '#ffffff'); e.scale.set(0.32, 0.12, 1); e.position.set(x, 0.75, 0.46); iG.add(e); }
    izo.ekle(iG); izo.etiketNoktasi = V(0, 2.5, 0); L.push(izo);
    const enj = o3('m-enjektor'); const enjG = enjektor(2.8, 0.42); enjG.position.copy(yer(2, 1)).add(V(-1.6, 0.45, 0)); enj.ekle(enjG); enj.etiketNoktasi = V(0, 1.0, 0); L.push(enj);
    const gen = o3('m-genis'); const genG = enjektor(3.6, 0.72, true); genG.position.copy(yer(3, 1)).add(V(-2.2, 0.75, 0)); gen.ekle(genG);
    const ge = yazi('kateter ucu ≠ Luer ucu', 44, '#3e4a58'); ge.scale.set(1.1, 0.26, 1); ge.rotation.x = -Math.PI / 2; ge.position.copy(yer(3, 1)).add(V(0, 0.02, 1.5)); gen.ekle(ge); gen.etiketNoktasi = V(0, 1.6, 0); L.push(gen);
    const ant = o3('m-antiseptik'); const antM = M.metal(); ant.boya(antM); const aG = new THREE.Group(); aG.position.copy(yer(0, 2));
    const kuvet = tornaYumusak([[0, 0], [1.6, 0.02], [2.0, 0.5], [2.1, 0.9], [1.95, 0.95], [1.5, 0.5], [0, 0.45]], antM); kuvet.scale.set(1, 1, 0.65); aG.add(kuvet);
    const pov = silindir(1.5, 1.4, 0.3, M.povidon()); pov.scale.set(1, 1, 0.65); pov.position.y = 0.5; pov.castShadow = false; aG.add(pov);
    const gaz = yuvarlakKutu(1.3, 0.25, 1.3, 0.1, M.beyaz()); gaz.position.set(-1.0, 0.7, 0); gaz.rotation.y = derece(15); aG.add(gaz);
    const pens = kapsul(0.08, 2.8, antM); pens.rotation.z = derece(80); pens.position.set(1.0, 0.95, 0.4); aG.add(pens); ant.ekle(aG); ant.etiketNoktasi = V(0, 1.6, 0); L.push(ant);
    const ort = o3('m-ortu'); const oM = M.ortu(); ort.boya(oM); const oG = yuvarlakKutu(3.6, 0.5, 2.8, 0.2, oM); oG.position.copy(yer(1, 2)).add(V(0, 0.25, 0)); ort.ekle(oG);
    const ortKat = yuvarlakKutu(3.3, 0.3, 2.5, 0.15, oM); ortKat.position.copy(yer(1, 2)).add(V(0.15, 0.62, 0.1)); ortKat.rotation.y = derece(-6); ort.ekle(ortKat); ort.etiketNoktasi = V(0, 1.1, 0); L.push(ort);
    const tor = o3('m-torba'); const tM = M.plastik(); tM.transmission = 0.55; tor.boya(tM); const tG = yuvarlakKutu(3.0, 0.4, 3.6, 0.3, tM); tG.position.copy(yer(2, 2)).add(V(0, 0.2, 0)); tor.ekle(tG);
    const hortum = tup(sarmal(0.9, 1.8, 0.02), 0.13, M.plastikMat(), 100, 8); hortum.position.copy(yer(2, 2)).add(V(0.2, 0.45, 0)); tor.ekle(hortum);
    const te = yazi('2000 mL', 54, '#5b6676'); te.scale.set(0.9, 0.22, 1); te.rotation.x = -Math.PI / 2; te.position.copy(yer(2, 2)).add(V(-0.3, 0.45, 1.2)); tor.ekle(te); tor.etiketNoktasi = V(0, 1.0, 0); L.push(tor);
    // steril alan: tepsinin sağ alt köşesinde yeşil steril örtü, kenarı çizilebilir
    const sa = o3('m-steril-alan'); const saM = M.ortu(); saM.color.setHex(0x3f9a6b); sa.boya(saM); const saK = yuvarlakKutu(4.6, 3.8, 0.06, 0.2, saM); saK.rotation.x = -Math.PI / 2; saK.position.copy(yer(3, 2)).add(V(0, 0.04, 0)); sa.ekle(saK);
    const cer = new THREE.Shape(); cer.moveTo(-2.3, -1.9); cer.lineTo(2.3, -1.9); cer.lineTo(2.3, 1.9); cer.lineTo(-2.3, 1.9); cer.closePath();
    const cerT = tup(new THREE.CatmullRomCurve3([V(-2.3, 0.1, 1.9), V(2.3, 0.1, 1.9), V(2.3, 0.1, -1.9), V(-2.3, 0.1, -1.9), V(-2.3, 0.1, 1.9)], false, 'catmullrom', 0), 0.08, M.yesil(), 80, 8); cerT.position.copy(yer(3, 2)); sa.ekle(cerT); sa.cizici = (f) => cerT.ilerle(f);
    sa.etiketNoktasi = V(0, 0.8, 0); L.push(sa);
    return L;
  },
};

// ———————————————————————————————————————— Kateter kesiti ve French ölçüsü
const FoleyKesit: Sahne3BTanim = {
  ad: 'Kateter kesiti ve French ölçüsü',
  gizli: [],
  etiket: { 'c-drenaj-lumen': 'Drenaj lümeni (geniş)', 'c-balon-lumen': 'Balon lümeni (ince)', 'c-olcek-eriskin': 'Erişkin: 12–24 Fr, boy sabit', 'c-olcek-cocuk': 'Çocuk: 6–8–10 Fr, daha kısa' },
  kamera: { poz: [0.5, 7, 15], hedef: [0.5, 0, 0] },
  zeminY: -2.6,
  kur: () => {
    const L: Oge3[] = [];
    const zemin = o3('_zemin'); const z = yuvarlakKutu(24, 16, 0.1, 0.5, M.ortuAcik()); z.rotation.x = -Math.PI / 2; z.position.y = -2.6; z.receiveShadow = true; zemin.ekle(z); L.push(zemin);
    // büyütülmüş kesit: lateks disk, iki lümen (geniş drenaj + ince balon kanalı)
    const kes = new THREE.Shape(); kes.absarc(0, 0, 2.2, 0, Math.PI * 2, false);
    const dr = new THREE.Path(); dr.absarc(0.25, -0.15, 1.25, 0, Math.PI * 2, true); kes.holes.push(dr);
    const bl = new THREE.Path(); bl.absarc(-1.35, 0.95, 0.32, 0, Math.PI * 2, true); kes.holes.push(bl);
    const kesG = new THREE.ExtrudeGeometry(kes, { depth: 3.0, bevelEnabled: true, bevelThickness: 0.12, bevelSize: 0.12, bevelSegments: 4, curveSegments: 48 });
    const kesM = M.lateks(); const kesO = o3('_kesit'); const kesK = mesh(kesG, kesM); kesK.rotation.y = derece(35); kesK.position.set(-5.5, 0.0, 0.5); kesK.scale.setScalar(0.8); kesO.ekle(kesK); L.push(kesO);
    const drM = M.koyu(); drM.color.setHex(0x5a4214); const drO = o3('c-drenaj-lumen').boya(drM); const drK = silindir(1.2, 1.2, 3.1, drM); drK.rotation.x = Math.PI / 2; drK.rotation.z = 0; drK.position.set(-4.5 + 0.25 * Math.cos(derece(35)), -0.15, 0.5 + 1.5 - 0.25 * Math.sin(derece(35)));
    drK.rotation.set(Math.PI / 2, derece(35), 0); drK.scale.setScalar(0.8); drK.position.set(-5.5 + 0.2 * Math.cos(derece(35)), -0.12, 0.5 + 1.2 - 0.2 * Math.sin(derece(35))); drO.ekle(drK); drO.etiketNoktasi = V(0, 1.4, 0.3); L.push(drO);
    const blO = o3('c-balon-lumen'); const blM = M.mavi(); blO.boya(blM); const blK = silindir(0.28, 0.28, 3.1, blM); blK.rotation.set(Math.PI / 2, derece(35), 0); blK.scale.setScalar(0.8); blK.position.set(-5.5 - 1.08 * Math.cos(derece(35)), 0.76, 0.5 + 1.2 + 1.08 * Math.sin(derece(35))); blO.ekle(blK); blO.etiketNoktasi = V(0, 1.2, 0); L.push(blO);
    // ölçek: erişkin 12–24 Fr (aynı boy, kalınlaşan), çocuk 6–8–10 Fr (kısa)
    const er = o3('c-olcek-eriskin'); const erM = M.lateks(); er.boya(erM);
    [12, 14, 16, 18, 20, 22, 24].forEach((fr, i) => { const r = (fr / 3) * 0.055; const k = kateter(egri([[1.2 + i * 0.9, -2.3, -3.0], [1.2 + i * 0.9, -2.3, 0.0], [1.2 + i * 0.9, -2.3, 3.0]]), r, erM, 20); er.ekle(k); const y = yazi(`${fr}`, 60, '#5b6676'); y.scale.set(0.5, 0.14, 1); y.rotation.x = -Math.PI / 2; y.position.set(1.2 + i * 0.9, -2.5, 3.6); er.ekle(y); });
    er.etiketNoktasi = V(4.0, -1.2, 0); L.push(er);
    const co = o3('c-olcek-cocuk'); const coM = M.silikon(); co.boya(coM);
    [6, 8, 10].forEach((fr, i) => { const r = (fr / 3) * 0.055; const k = kateter(egri([[-1.6 + i * 0.7, -2.3, -1.6], [-1.6 + i * 0.7, -2.3, 0.0], [-1.6 + i * 0.7, -2.3, 1.6]]), r, coM, 16); co.ekle(k); const y = yazi(`${fr}`, 60, '#5b6676'); y.scale.set(0.45, 0.13, 1); y.rotation.x = -Math.PI / 2; y.position.set(-1.6 + i * 0.7, -2.5, 2.2); co.ekle(y); });
    co.etiketNoktasi = V(-0.9, -1.5, 0); L.push(co);
    return L;
  },
};

// ———————————————————————————————————————— Pelvis kırığı ve üretra yaralanması (önden)
const Travma: Sahne3BTanim = {
  ad: 'Pelvis kırığı ve üretra yaralanması (önden)',
  gizli: ['t-kirik', 't-kan', 't-yirtik'],
  etiket: { 't-pelvis': 'Pelvis halkası', 't-kirik': 'Pubis kolu kırığı', 't-simfiz': 'Simfiz ayrılması', 't-uretra': 'Üretra', 't-kan': 'Meatusta taze kan', 't-yirtik': 'Kısmi yırtık' },
  kamera: { poz: [0, 1.5, 19], hedef: [0, -0.5, 0] },
  kur: () => {
    const L: Oge3[] = [];
    const zemin = o3('_zemin'); const deri = yuvarlakKutu(16, 13, 1.0, 0.9, M.deriKesit()); deri.position.set(0, -0.2, -1.5); deri.receiveShadow = true; zemin.ekle(deri); L.push(zemin);
    // pelvis halkası: iliak kanatlar (yumru) + pubis kolları (tüp) + sakrum
    const pM = M.kemik(); const pel = o3('t-pelvis').boya(pM);
    for (const s of [-1, 1]) { const kanat = yumru(2.4, 2.9, 0.9, pM); kanat.position.set(s * 3.6, 2.6, 0); kanat.rotation.z = s * derece(-18); pel.ekle(kanat); }
    const sakrum = tornaYumusak([[0, 0], [1.6, 0.05], [1.2, 2.0], [0.7, 3.8], [0.3, 4.6], [0, 4.7]], pM); sakrum.scale.set(1, 1, 0.5); sakrum.position.set(0, 0.6, -0.6); pel.ekle(sakrum);
    const kolSol = tup(egri([[-3.2, 0.2, 0.2], [-2.8, -1.6, 0.4], [-1.6, -2.8, 0.6], [-0.35, -3.1, 0.7]]), 0.42, pM, 40, 14); pel.ekle(kolSol);
    const kolSag = tup(egri([[3.2, 0.2, 0.2], [2.8, -1.6, 0.4], [1.6, -2.8, 0.6], [0.35, -3.1, 0.7]]), 0.42, pM, 40, 14); pel.ekle(kolSag);
    for (const s of [-1, 1]) { const isk = tup(egri([[s * 3.0, -1.0, 0.1], [s * 3.0, -3.4, 0.2], [s * 1.8, -4.6, 0.4], [s * 0.6, -4.2, 0.6]]), 0.38, pM, 30, 12); pel.ekle(isk); }
    pel.etiketNoktasi = V(-4.6, 4.6, 0.5); L.push(pel);
    const simM = M.kemik(); simM.color.setHex(0xe3d9c6); const sim = o3('t-simfiz').boya(simM); const simK = yuvarlakKutu(0.9, 0.9, 0.7, 0.2, simM); simK.position.set(0, -3.1, 0.75); sim.ekle(simK); sim.etiketNoktasi = V(0, -2.4, 1.2); L.push(sim);
    const kirM = M.koyu(); kirM.color.setHex(0x3a1f1a); const kir = o3('t-kirik').boya(kirM);
    const catlak = tup(egri([[-2.4, -1.4, 0.4], [-2.0, -2.0, 0.7], [-2.3, -2.5, 0.9], [-1.7, -2.9, 1.0]]), 0.07, kirM, 30, 6); kir.ekle(catlak);
    const parca = yumru(0.5, 0.35, 0.35, M.kemik()); parca.position.set(-2.1, -2.2, 1.05); parca.rotation.z = derece(25); kir.ekle(parca);
    const kan2 = yumru(0.6, 0.45, 0.2, M.kan()); kan2.position.set(-2.0, -2.2, 1.1); kir.ekle(kan2); kir.etiketNoktasi = V(-2.6, -1.6, 1.3); L.push(kir);
    const urM = M.mukoza(); const ur = o3('t-uretra').boya(urM); const urT = tup(egri([[0, -1.6, 0.9], [0, -3.2, 1.0], [0, -4.6, 1.1], [0, -6.0, 1.2]]), 0.3, urM, 40, 12); ur.ekle(urT);
    const mes = yumru(1.7, 1.3, 0.9, M.mesane()); mes.position.set(0, -0.6, 0.4); ur.ekle(mes); ur.etiketNoktasi = V(0.6, -4.6, 1.4); L.push(ur);
    const yirM = M.kan(); const yir = o3('t-yirtik').boya(yirM); const yK = yumru(0.42, 0.55, 0.42, yirM); yK.position.set(0.1, -3.6, 1.15); yir.ekle(yK); const ucuk = kutu(0.5, 0.08, 0.3, M.koyu()); ucuk.position.set(0.1, -3.6, 1.45); ucuk.rotation.z = derece(30); yir.ekle(ucuk); yir.etiketNoktasi = V(0.9, -3.4, 1.5); L.push(yir);
    const kanO = o3('t-kan'); const kanM = M.kan(); kanO.boya(kanM); const d1 = yumru(0.3, 0.42, 0.3, kanM); d1.position.set(0, -6.2, 1.25); kanO.ekle(d1); const d2 = yumru(0.18, 0.26, 0.18, kanM); d2.position.set(0.2, -6.7, 1.3); kanO.ekle(d2); kanO.etiketNoktasi = V(0, -5.9, 1.4); L.push(kanO);
    return L;
  },
};

// ———————————————————————————————————————— Mahremiyet ve hasta pozisyonu (üstten)
const Pozisyon: Sahne3BTanim = {
  ad: 'Mahremiyet ve hasta pozisyonu (üstten)',
  gizli: ['p-paravan', 'p-yardimci', 'p-v'],
  etiket: { 'p-hekim': 'Hekim: tanıt, anlat, onam al', 'p-paravan': 'Paravan / perde', 'p-yardimci': 'Yardımcı personel', 'p-erkek': 'Erkek: supin', 'p-kadin': 'Kadın: modifiye litotomi' },
  kamera: { poz: [1.0, 24, 19], hedef: [1.0, 0, -0.5] },
  zeminY: 0,
  kur: () => {
    const L: Oge3[] = [];
    const zemin = o3('_zemin'); const yer = yuvarlakKutu(30, 22, 0.2, 0.6, M.tepsi()); yer.rotation.x = -Math.PI / 2; yer.position.y = -0.1; yer.receiveShadow = true; zemin.ekle(yer);
    const yatak = (z: number) => { const g = new THREE.Group(); const sase = yuvarlakKutu(11, 1.2, 4.2, 0.3, M.plastikMat()); sase.position.set(0, 0.6, z); g.add(sase); const dosek = yuvarlakKutu(10.6, 0.7, 3.9, 0.3, M.yatak()); dosek.position.set(0, 1.5, z); g.add(dosek); const yastik = yuvarlakKutu(1.6, 0.5, 2.6, 0.25, M.beyaz()); yastik.position.set(-4.5, 2.05, z); g.add(yastik); for (const [x, zz] of [[-5, -1.8], [5, -1.8], [-5, 1.8], [5, 1.8]] as const) { const bacak = silindir(0.12, 0.12, 1.0, M.metal()); bacak.position.set(x, 0.0, z + zz); g.add(bacak); } return g; };
    zemin.ekle(yatak(-4.2), yatak(4.2)); L.push(zemin);
    const erk = o3('p-erkek'); const eG = insan({ yatan: true, giysi: M.onluk() }); eG.rotation.z = -Math.PI / 2; eG.position.set(-4.6, 2.3, -4.2); eG.scale.setScalar(1.15); erk.ekle(eG); erk.etiketNoktasi = V(0.0, 1.0, -4.2 - 2.6); L.push(erk);
    const kad = o3('p-kadin'); const kG = insan({ yatan: true, giysi: M.onluk(), bacak: [derece(-70), derece(95)] }); kG.rotation.z = -Math.PI / 2; kG.position.set(-4.6, 2.3, 4.2); kG.scale.setScalar(1.1); kad.ekle(kG); kad.etiketNoktasi = V(0.0, 1.0, 4.2 + 2.6); L.push(kad);
    const v = o3('p-v'); const vM = M.mavi(); vM.transparent = true; vM.opacity = 0.35; vM.depthWrite = false; v.boya(vM);
    const vS = new THREE.Shape(); vS.moveTo(0, 0); vS.lineTo(3.8, -2.4); vS.lineTo(3.8, 2.4); vS.closePath(); const vK = mesh(new THREE.ShapeGeometry(vS), vM); vK.rotation.x = -Math.PI / 2; vK.position.set(1.4, 2.0, 4.2); vK.castShadow = false; v.ekle(vK); L.push(v);
    const hek = o3('p-hekim'); const hG = insan({ giysi: M.beyaz() }); hG.position.set(-8.6, 0, 0.0); hG.rotation.y = derece(90); hG.scale.setScalar(1.15); hek.ekle(hG); hek.etiketNoktasi = V(-8.6, 5.0, 0); L.push(hek);
    const par = o3('p-paravan'); const pM = M.plastikMat(); par.boya(pM);
    for (let i = 0; i < 4; i++) { const pan = yuvarlakKutu(0.15, 6.2, 3.6, 0.1, M.ortuAcik()); pan.position.set(8.4 + (i % 2) * 0.6, 3.1, -6.2 + i * 3.9); pan.rotation.y = (i % 2 ? -1 : 1) * derece(14); par.ekle(pan); }
    par.etiketNoktasi = V(8.6, 6.6, 0); L.push(par);
    const yar = o3('p-yardimci'); const yG = insan({ giysi: M.onluk() }); yG.position.set(3.0, 0, 8.6); yG.rotation.y = derece(180); yG.scale.setScalar(1.1); yar.ekle(yG); yar.etiketNoktasi = V(3.0, 5.0, 8.6); L.push(yar);
    return L;
  },
};

// ———————————————————————————————————————— Eğitim maketi
const Maket: Sahne3BTanim = {
  ad: 'Kateter uygulama eğitim maketi',
  gizli: ['mk-hazne-dolu', 'mk-erkek'],
  etiket: { 'mk-govde': 'Pelvis gövdesi + uyluklar', 'mk-kadin': 'Kadın genital modülü', 'mk-erkek': 'Erkek genital modülü', 'mk-hazne': 'Mesane haznesi (su doldurulur)', 'mk-hazne-dolu': 'Dolu hazne: kateterden "idrar" gelir' },
  kamera: { poz: [6, 13, 20], hedef: [0, 1.6, 0] },
  zeminY: 0,
  kur: () => {
    const L: Oge3[] = [];
    const zemin = o3('_zemin'); const masa = yuvarlakKutu(26, 0.4, 16, 0.4, M.yatak()); masa.position.y = -0.2; masa.receiveShadow = true; zemin.ekle(masa); L.push(zemin);
    const gM = M.deri(); gM.color.setHex(0xf2c9a8); const gov = o3('mk-govde').boya(gM);
    const bel = yuvarlakKutu(6.4, 4.0, 6.0, 1.4, gM); bel.position.set(-2.5, 2.0, 0); gov.ekle(bel);
    const karin = yumru(3.2, 1.4, 2.8, gM); karin.position.set(-3.0, 4.0, 0); gov.ekle(karin);
    for (const s of [-1, 1]) { const uy = kapsul(1.5, 3.6, gM); uy.rotation.z = Math.PI / 2; uy.rotation.y = s * derece(22); uy.position.set(2.0, 1.6, s * 2.6); gov.ekle(uy); }
    gov.etiketNoktasi = V(-2.5, 4.6, 0); L.push(gov);
    const hM = M.plastik(); hM.transmission = 0.75; const haz = o3('mk-hazne').boya(hM); const hK = yuvarlakKutu(3.0, 2.0, 3.6, 0.4, hM); hK.position.set(-2.5, 5.4, 0); haz.ekle(hK); const kapak = silindir(0.6, 0.6, 0.4, M.mavi()); kapak.position.set(-2.5, 6.6, 0); haz.ekle(kapak); haz.etiketNoktasi = V(-2.5, 6.9, 0); L.push(haz);
    const dol = o3('mk-hazne-dolu'); const dK = yuvarlakKutu(2.7, 1.3, 3.3, 0.3, M.idrarMat()); dK.position.set(-2.5, 5.1, 0); dK.castShadow = false; dol.ekle(dK); const akT = tup(egri([[1.6, 1.4, 0], [3.0, 1.1, 0.2], [4.6, 0.4, 0.4]]), 0.14, M.idrarMat(), 20, 8); dol.ekle(akT); dol.etiketNoktasi = V(-2.5, 6.9, 0); L.push(dol);
    const kadM = M.glans(); const kad = o3('mk-kadin').boya(kadM); const kK = yuvarlakKutu(1.8, 2.6, 1.8, 0.5, kadM); kK.position.set(1.2, 1.9, 0); kad.ekle(kK); const kAc = yumru(0.25, 0.5, 0.15, M.koyu()); kAc.position.set(2.1, 2.2, 0); kad.ekle(kAc); kad.etiketNoktasi = V(1.2, 3.4, 0); L.push(kad);
    const erM = M.glans(); const er = o3('mk-erkek').boya(erM); const eK = kapsul(0.75, 3.0, erM); eK.rotation.z = Math.PI / 2; eK.position.set(2.8, 2.0, 0); er.ekle(eK); const eU = yumru(0.9, 0.85, 0.85, erM); eU.position.set(4.6, 2.0, 0); er.ekle(eU); er.etiketNoktasi = V(3.6, 3.2, 0); L.push(er);
    return L;
  },
};

export const SAHNELER3B_2: Record<string, Sahne3BTanim> = {
  mesane: Mesane, malzeme: Malzeme, 'foley-kesit': FoleyKesit, travma: Travma,
};
/** İlkel (kapsül/küre) sürümler — organik küme (sahneler3b_organik.ts) bunların yerini aldı; başvuru için tutulur, kayıtta değil */
export const SAHNELER3B_ESKI: Record<string, Sahne3BTanim> = { kadin: Kadin, 'yakin-kadin': YakinKadin, 'yakin-el': YakinEl, 'yakin-erkek-jel': YakinErkekJel, pozisyon: Pozisyon, maket: Maket };
void grup; void ok; void kutu;
