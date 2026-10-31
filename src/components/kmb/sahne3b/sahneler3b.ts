/**
 * KMB 3B sahne tanımları — SVG sahnelerle (sahneler.tsx) aynı kimlikler ve aynı gizli/etiket sözleşmesi.
 * Ölçek: 1 birim ≈ 1 cm (kateter 16 Fr ≈ 0,53 cm çap → yarıçap 0,27 görsel için ~0,22–0,3). Kamera +Z'den bakar; kesit
 * sahnelerinde X öne (anterior) / sağa, Y yukarı. Her tanım `kur()` ile ögelerini kurar; eylemler Sahne3B'de uygulanır.
 * Tıbbi düzen kaynağı: KMB belgesi + SVG sahneler (hoca kaydı ile doğrulanmış yerleşim); yeni sahne eklerken
 * SAHNE_OGELERI listesindeki kimliklerin tamamı kurulmalıdır (dogrula.py öge kapısı aynı listeyi kullanır).
 */
import * as THREE from 'three';
import type { Sahne3BTanim } from './Sahne3B';
import { SAHNELER3B_2 } from './sahneler3b_2';
import { SAHNELER3B_ORGANIK } from './sahneler3b_organik';
import { M, Oge3, V, akis, egri, halka, kapsul, kateter, kure, kutu, mesh, ok, silindir, torna, tornaYumusak, tup, yazi, yumru, yuvarlakKutu, puruz, derece } from './yardimci';

const o3 = (id: string) => new Oge3(id);
const kenarMHazir = () => { const m = M.mesane(); m.color.setHex(0xd98a82); return m; };

// ———————————————————————————————————————— Foley kateter ve idrar torbası (steril örtü üstünde)
const Foley: Sahne3BTanim = {
  ad: 'Foley kateter ve idrar torbası',
  gizli: ['f-balon', 'f-torba', 'f-torba-bag', 'f-enjektor'],
  etiket: {
    'f-uc': 'Kateter ucu (yuvarlak)', 'f-delik': 'İdrar delikleri', 'f-balon-sonuk': 'Sabitleme balonu (sönük)', 'f-balon': 'Şişirilmiş balon',
    'f-govde': 'Gövde: sarı lateks / beyaz silikon', 'f-drenaj': 'Drenaj kanalı → torba', 'f-balon-kanal': 'Valfli balon kanalı → enjektör',
    'f-torba': 'İdrar torbası', 'f-musluk': 'Boşaltma musluğu',
  },
  kamera: { poz: [1.8, 10.5, 22.5], hedef: [1.8, 0.6, 0.2] },
  zeminY: -0.08,
  kur: () => {
    const L: Oge3[] = [];
    // steril örtü (mavi, hafif kırışık hissi için iki kat)
    const ortu = o3('_ortu');
    const d = yuvarlakKutu(17, 9.5, 0.12, 0.5, M.ortuAcik()); d.rotation.x = -Math.PI / 2; d.position.set(0.3, -0.07, 0.2); ortu.ekle(d);
    L.push(ortu);
    // kateter gövdesi: hafif S çizen yol
    const yol = egri([[-6.4, 0.24, 0.2], [-4.6, 0.24, -0.1], [-2.2, 0.24, -0.5], [0.4, 0.24, -0.2], [2.4, 0.24, 0.2], [3.6, 0.24, 0.3]]);
    const lateks = M.lateks();
    const govde = o3('f-govde').boya(lateks);
    const g = tup(yol, 0.24, lateks, 120, 20); govde.ekle(g); govde.cizici = (f) => g.ilerle(f);
    const y = yazi('16 Fr · 10 mL', 52, '#7a5a16'); y.scale.set(1.5, 0.38, 1); y.rotation.x = -Math.PI / 2; y.position.set(-0.6, 0.0, 0.5); govde.ekle(y);
    L.push(govde);
    const ucM = M.lateks();
    const uc = o3('f-uc').boya(ucM); const ucK = kure(0.245, ucM, 24); ucK.position.copy(yol.getPoint(0)); ucK.scale.set(1.25, 1, 1); uc.ekle(ucK); L.push(uc);
    const delik = o3('f-delik'); for (const [t, s] of [[0.03, 1], [0.055, -1]] as const) { const p = yol.getPoint(t); const e = mesh(new THREE.SphereGeometry(0.1, 12, 8), M.koyu(), false); e.scale.set(1.6, 0.9, 0.6); e.position.set(p.x, p.y + 0.12 * s, p.z + 0.2); delik.ekle(e); } L.push(delik);
    const bsM = M.lateks();
    const bs = o3('f-balon-sonuk').boya(bsM); const bsK = yumru(0.62, 0.3, 0.3, bsM); const pb = yol.getPoint(0.17); bsK.position.copy(pb); bs.ekle(bsK); L.push(bs);
    const bM = M.lateks(); bM.transmission = 0.45; bM.thickness = 0.6; bM.roughness = 0.2; bM.color.setHex(0xf3d98a);
    const b = o3('f-balon').boya(bM); const bK = kure(1.0, bM, 40); bK.position.copy(pb); bK.position.y += 0.5; b.ekle(bK); L.push(b);
    // çatal (Y bağlantı)
    const catal = o3('_catal'); const cK = mesh(new THREE.ConeGeometry(0.42, 1.1, 24), M.lateksKoyu()); cK.rotation.z = -Math.PI / 2; cK.position.set(4.05, 0.24, 0.32); catal.ekle(cK); L.push(catal);
    // drenaj kanalı: kalın, huniyle biter
    const drM = M.lateks();
    const dr = o3('f-drenaj').boya(drM);
    const drT = silindir(0.33, 0.3, 2.2, drM); drT.rotation.z = Math.PI / 2; drT.position.set(5.6, 0.3, 0.42); dr.ekle(drT);
    const huni = torna([[0.3, 0], [0.42, 0.5], [0.5, 0.75], [0.46, 0.8], [0.36, 0.55], [0.3, 0.1]], M.lateksKoyu()); huni.rotation.z = -Math.PI / 2; huni.position.set(6.7, 0.3, 0.42); dr.ekle(huni);
    dr.etiketNoktasi = V(6.0, 0.6, 0.4);
    L.push(dr);
    // balon kanalı: ince, valf + mavi kapak
    const bkM = M.lateks();
    const bk = o3('f-balon-kanal').boya(bkM);
    const bkYol = egri([[4.3, 0.26, 0.2], [5.0, 0.4, -0.6], [5.9, 0.6, -1.6], [6.5, 0.7, -2.3]]);
    bk.ekle(tup(bkYol, 0.11, bkM, 40, 12));
    const valf = yuvarlakKutu(0.9, 0.62, 0.5, 0.12, M.plastikMat()); valf.position.set(6.95, 0.72, -2.75); valf.rotation.y = derece(35); bk.ekle(valf);
    const kapak = silindir(0.16, 0.16, 0.36, M.mavi()); kapak.rotation.z = Math.PI / 2; kapak.rotation.y = derece(35); kapak.position.set(7.42, 0.72, -3.05); bk.ekle(kapak);
    L.push(bk);
    // enjektör (10 mL): saydam silindir + piston + çubuk
    const enj = o3('f-enjektor');
    const eg = new THREE.Group(); eg.position.set(7.75, 0.74, -3.3); eg.rotation.y = derece(35);
    const govE = silindir(0.42, 0.42, 3.2, M.plastik()); govE.rotation.z = Math.PI / 2; govE.position.x = 1.6; eg.add(govE);
    const sivi = silindir(0.36, 0.36, 1.8, M.izotonik()); sivi.rotation.z = Math.PI / 2; sivi.position.x = 1.1; eg.add(sivi);
    const piston = silindir(0.36, 0.36, 0.2, M.koyu()); piston.rotation.z = Math.PI / 2; piston.position.x = 2.05; eg.add(piston);
    const cubuk = kutu(1.9, 0.14, 0.14, M.plastikMat()); cubuk.position.x = 3.1; eg.add(cubuk);
    const baslik = kutu(0.1, 0.9, 0.9, M.plastikMat()); baslik.position.x = 4.1; eg.add(baslik);
    const flans = kutu(0.1, 1.2, 1.2, M.plastikMat()); flans.position.x = 3.2; eg.add(flans);
    for (let i = 0; i < 6; i++) { const c = kutu(0.03, 0.02, 0.5, M.koyu()); c.position.set(0.4 + i * 0.4, 0.42, 0.0); eg.add(c); }
    enj.ekle(eg); L.push(enj);
    // torbaya bağlantı hortumu + torba
    const bagM = M.plastikMat();
    const bag = o3('f-torba-bag').boya(bagM);
    const bagYol = egri([[7.15, 0.32, 0.42], [8.0, 0.3, 1.2], [8.7, 0.5, 2.2], [9.1, 1.2, 2.7], [9.3, 2.9, 2.4]]);
    const bagT = tup(bagYol, 0.19, bagM, 60, 12); bag.ekle(bagT); bag.cizici = (f) => bagT.ilerle(f);
    L.push(bag);
    const torba = o3('f-torba');
    const tg = new THREE.Group(); tg.position.set(9.7, 2.3, 1.6); tg.rotation.y = derece(-22); tg.rotation.x = derece(-8);
    const tM = M.plastik(); tM.transmission = 0.6; tM.roughness = 0.2;
    const tK = yuvarlakKutu(3.6, 4.4, 0.55, 0.35, tM); tg.add(tK);
    const idr = yuvarlakKutu(3.3, 1.9, 0.4, 0.25, M.idrarMat()); idr.position.y = -1.15; tg.add(idr);
    const damla = silindir(0.22, 0.22, 0.8, M.plastik()); damla.position.set(0.1, 2.35, 0); tg.add(damla);
    const aski = halka(0.45, 0.06, M.plastikMat(), 24); aski.position.set(0, 2.55, 0); tg.add(aski);
    const olcek = yazi('250 · 500 · 750 · 1000 mL', 40, '#5b6676'); olcek.scale.set(0.75, 0.19, 1); olcek.rotation.z = Math.PI / 2; olcek.position.set(1.45, 0.3, 0.3); tg.add(olcek);
    torba.ekle(tg); torba.boya(tM); L.push(torba);
    const musluk = o3('f-musluk');
    const mG = new THREE.Group(); mG.position.set(9.4, 0.12, 2.3); mG.rotation.y = derece(-22);
    const m1 = kutu(0.6, 0.4, 0.4, M.plastikMat()); mG.add(m1);
    const m2 = kutu(0.5, 0.16, 0.16, M.kirmizi()); m2.position.set(0.5, 0.05, 0); mG.add(m2);
    musluk.ekle(mG); L.push(musluk);
    return L;
  },
};

// ———————————————————————————————————————— Yakın plan: kateter ucu mesane boynunda (mesane içi)
const YakinMesane: Sahne3BTanim = {
  ad: 'Yakın plan: kateter ucu mesane boynunda',
  gizli: ['y-kateter', 'y-delik', 'y-balon-sonuk', 'y-balon', 'y-idrar', 'y-cekme'],
  etiket: {
    'y-duvar': 'Mesane duvarı (detrüsör)', 'y-trigon': 'Trigon', 'y-ureter': 'Üreter ağzı', 'y-boyun': 'Mesane boynu', 'y-prostat': 'Prostat / prostatik üretra',
    'y-delik': 'Uçtaki delikler: idrar girer', 'y-balon-sonuk': 'Sönük balon', 'y-balon': 'Balon: 10 mL izotonik', 'y-idrar': 'İdrar deliklerden kanala', 'y-cekme': 'Hafifçe çek: balon boyna oturur',
  },
  kamera: { poz: [0, 12.5, 12.0], hedef: [0, -1.4, 0] },
  kur: () => {
    const L: Oge3[] = [];
    const bump = puruz(11, 256, 0.35);
    // kubbe: içten görünen mesane duvarı (arka yüzler), tabanı açık (boyun hunisi oradan iner)
    const duvM = M.mesane(); duvM.side = THREE.DoubleSide; duvM.bumpMap = bump; duvM.bumpScale = 0.04;
    const duvar = o3('y-duvar').boya(duvM);
    // çanak: kürenin alt kesimi (üstü kesilmiş → içine bakılır), kalın kenar halkasıyla duvar kalınlığı
    // ön dilim (kameraya bakan 100°) kesilmiş: boyun hunisi ve prostat kesitten görünür
    const kub = mesh(new THREE.SphereGeometry(5, 64, 48, derece(140), derece(260), derece(58), derece(122)), duvM, false); kub.position.y = 2.9; kub.receiveShadow = true; duvar.ekle(kub);
    // kesit kenarları: duvar kalınlığı (iki dik yarım halka)
    for (const a of [derece(140), derece(400)]) { const kg = new THREE.TorusGeometry(5, 0.26, 10, 48, derece(122)); kg.rotateZ(-Math.PI / 2 - derece(58)); kg.rotateY(a + Math.PI / 2); const kk = mesh(kg, kenarMHazir()); kk.position.y = 2.9; duvar.ekle(kk); }
    const kenarM = M.mesane(); kenarM.color.setHex(0xd98a82);
    const kenarH = mesh(new THREE.TorusGeometry(5 * Math.sin(derece(58)), 0.28, 12, 72, derece(260)), kenarM); kenarH.rotation.x = Math.PI / 2; kenarH.rotation.z = derece(140 - 90); kenarH.position.y = 2.9 + 5 * Math.cos(derece(58)); duvar.ekle(kenarH);
    // detrüsör demetleri: iç yüzeyde kabarık yaylar
    const demM = M.mesane(); demM.color.setHex(0xd98a82);
    for (let i = 0; i < 10; i++) {
      const a = derece(150) + (i / 10) * derece(240);
      // meridyen demeti: çanak iç yüzeyinde kenardan tabana inen kabarık yay (tek düzlemde, Y ekseni etrafında döndürülür)
      const yg = new THREE.TorusGeometry(4.86, 0.11, 10, 48, derece(100)); yg.rotateZ(derece(-170)); yg.rotateY(a);
      const yay = mesh(yg, demM, false); yay.position.y = 2.9; duvar.ekle(yay);
    }
    duvar.etiketNoktasi = V(-3.2, 4.5, 1.0);
    L.push(duvar);
    // idrar: kubbe içinde sıvı yüzeyi (geniş, basık mercek)
    const idM = M.idrar(); idM.transmission = 0.92; idM.thickness = 0.5; idM.color.setHex(0xf6dc7a);
    const idrar = o3('_idrar'); const iK = yumru(4.25, 0.38, 4.25, idM, 48); iK.position.y = 0.35; iK.castShadow = false; idrar.ekle(iK); L.push(idrar);
    // taban: boyun hunisi + trigon + üreter ağızları
    const boyunM = M.mukoza();
    const taban = torna([[1.7, 0.1], [1.3, -0.5], [0.85, -1.2], [0.7, -2.4], [0.72, -3.6]], boyunM, 48); taban.position.y = -1.0;
    const tabanM2 = M.mukoza(); tabanM2.side = THREE.DoubleSide; taban.material = tabanM2;
    const tabanOge = o3('_taban'); tabanOge.ekle(taban); L.push(tabanOge);
    const trigon = o3('y-trigon'); const tM = M.mukoza(); tM.color.setHex(0xf0b3ac); trigon.boya(tM);
    const sh = new THREE.Shape(); sh.moveTo(-2.1, -1.6); sh.lineTo(2.1, -1.6); sh.lineTo(0, 1.4); sh.closePath();
    const tG = new THREE.ExtrudeGeometry(sh, { depth: 0.12, bevelEnabled: true, bevelSize: 0.1, bevelThickness: 0.08, bevelSegments: 3 });
    const tK = mesh(tG, tM); tK.rotation.x = -Math.PI / 2; tK.position.set(0, -0.95, 0.3); trigon.ekle(tK); L.push(trigon);
    const ureter = o3('y-ureter'); const uM = M.kas(); uM.color.setHex(0x8f3c3a); ureter.boya(uM);
    for (const x of [-1.9, 1.9]) { const u = yumru(0.42, 0.14, 0.26, uM); u.position.set(x, -0.82, -1.1); ureter.ekle(u); } L.push(ureter);
    const boyun = o3('y-boyun'); const bM = M.kas(); boyun.boya(bM); const bH = halka(1.45, 0.2, bM, 64); bH.rotation.x = Math.PI / 2; bH.position.y = -1.05; boyun.ekle(bH); L.push(boyun);
    const prostat = o3('y-prostat'); const pM = M.prostat(); prostat.boya(pM);
    for (const x of [-1.25, 1.25]) { const p = yumru(1.0, 1.4, 1.1, pM); p.position.set(x, -3.0, 0); prostat.ekle(p); } prostat.etiketNoktasi = V(-2.2, -2.2, 0.6); L.push(prostat);
    // kateter: alttan girer, ucu mesane içinde
    const kYol = egri([[0, -7.5, 0], [0, -4, 0], [0, -1.5, 0], [0, 0.6, 0], [0, 1.9, 0.05]]);
    const kM = M.silikon();
    const kat = o3('y-kateter').boya(kM); const kK = kateter(kYol, 0.36, kM, 60); kat.ekle(kK); kat.cizici = (f) => kK.ilerle(f); kat.etiketNoktasi = V(0, 1.6, 0.4); L.push(kat);
    const delik = o3('y-delik'); for (const [yy, s] of [[1.55, 1], [1.1, -1]] as const) { const e = mesh(new THREE.SphereGeometry(0.15, 12, 8), M.koyu(), false); e.scale.set(0.7, 1.4, 1); e.position.set(0.36 * s, yy, 0.1); delik.ekle(e); } delik.etiketNoktasi = V(0, 2.1, 0.3); L.push(delik);
    const bsM = M.silikon(); const bs = o3('y-balon-sonuk').boya(bsM); const bsK = yumru(0.5, 0.75, 0.5, bsM); bsK.position.set(0, -0.2, 0); bs.ekle(bsK); L.push(bs);
    const balM = M.izotonik(); balM.transmission = 0.75; balM.color.setHex(0xe8f1fb);
    const bal = o3('y-balon').boya(balM); const balK = kure(1.25, balM, 48); balK.position.set(0, -0.1, 0); bal.ekle(balK); bal.etiketNoktasi = V(0.9, 0.9, 0.6); L.push(bal);
    // idrar akışı: sıvıdan uçtaki deliklere damlalar
    const id = o3('y-idrar');
    const yollar = [egri([[-3.4, 0.9, 1.2], [-1.8, 1.2, 0.8], [-0.4, 1.55, 0.3]]), egri([[3.2, 0.9, -1.0], [1.6, 1.2, -0.4], [0.4, 1.1, 0.2]]), egri([[-2.6, 1.5, -1.8], [-1.2, 1.7, -0.8], [-0.35, 1.55, 0.2]]), egri([[2.8, 1.6, 1.6], [1.4, 1.5, 0.9], [0.38, 1.1, 0.15]])];
    const aks = yollar.map((yl) => { const a = akis(yl, 7, 0.11, M.idrarMat()); id.ekle(a); return a; });
    id.cizici = (f) => aks.forEach((a) => a.ilerle(f)); id.tik = (t) => aks.forEach((a) => a.tik(t, 0)); id.etiketNoktasi = V(-2.4, 2.0, 0.8);
    L.push(id);
    const cek = o3('y-cekme'); const okK = ok(V(1.3, -1.3, 0.9), V(1.3, -3.6, 0.9), 0.1, M.mavi()); cek.ekle(okK); cek.cizici = (f) => okK.ilerle(f); cek.etiketNoktasi = V(1.3, -1.2, 0.9); L.push(cek);
    return L;
  },
};

// ———————————————————————————————————————— Erkek alt üriner sistem (sagittal kesit, kesit yüzeyi arkada)
const URETRA_E = egri([[-2.5, 1.35, 0], [-2.5, 0.2, 0], [-2.5, -1.1, 0], [-2.2, -2.1, 0], [-1.1, -2.25, 0], [0.4, -1.95, 0], [2.4, -1.6, 0], [4.4, -1.38, 0], [6.3, -1.15, 0]]);
const uretraTers = (uzat: [number, number, number] = [7.6, -1.12, 0]) => egri([uzat, [6.3, -1.15, 0], [4.4, -1.38, 0], [2.4, -1.6, 0], [0.4, -1.95, 0], [-1.1, -2.25, 0], [-2.2, -2.1, 0], [-2.5, -1.1, 0], [-2.5, 0.2, 0], [-2.5, 1.35, 0], [-2.5, 2.7, 0]]);
const Erkek: Sahne3BTanim = {
  ad: 'Erkek alt üriner sistem (yan kesit)',
  gizli: ['e-jel', 'e-kateter', 'e-balon-dogru', 'e-kivrim', 'e-enjektor', 'e-balon-yanlis'],
  etiket: {
    'e-mesane': 'Mesane', 'e-prostat': 'Prostat', 'e-sfinkter': 'Eksternal sfinkter', 'e-uretra': 'Üretra (~1 cm çap)', 'e-penil': 'Penis (korpuslar)', 'e-glans': 'Glans / prepisyum',
    'e-meatus': 'Eksternal meatus', 'e-testis': 'Testis / epididim', 'e-jel': 'Lidokainli jel üretrada', 'e-balon-dogru': 'Balon mesanede ✓', 'e-balon-yanlis': 'Balon üretrada ✗',
  },
  kamera: { poz: [1.9, 1.6, 24], hedef: [1.9, 0.1, 0] },
  kur: () => {
    const L: Oge3[] = [];
    // kesit zemini: deri/yağ/kas katmanları (arkada, gölge alır)
    const zemin = o3('_zemin');
    const deri = yuvarlakKutu(15, 11, 1.0, 0.8, M.deriKesit()); deri.position.set(0.8, -0.6, -1.2); deri.receiveShadow = true; zemin.ekle(deri);
    const yagM = M.yag(); yagM.color.setHex(0xf3e2b8);
    const yag = yuvarlakKutu(14.2, 10.2, 0.3, 0.7, yagM); yag.position.set(0.8, -0.6, -0.6); zemin.ekle(yag);
    // pelvis kemikleri: simfiz pubis (önde) + sakrum (arkada)
    const simfiz = yumru(0.62, 0.95, 0.7, M.kemik()); simfiz.position.set(-0.3, 0.9, 0); simfiz.rotation.z = derece(-18); zemin.ekle(simfiz);
    // sakrum + koksiks: öne kavisli, aşağı incelen kemik (omur gövdeleri hissi için boğumlu)
    const sakrum = tup(egri([[-5.4, 5.2, 0], [-5.9, 3.2, 0], [-5.8, 1.2, 0], [-5.2, -0.6, 0], [-4.6, -1.8, 0]]), 0.62, M.kemik(), 32, 14); zemin.ekle(sakrum);
    for (const [x, y] of [[-5.75, 3.6], [-5.85, 2.2], [-5.6, 0.6], [-5.0, -0.9]] as const) { const bog = yumru(0.8, 0.5, 0.75, M.kemik()); bog.position.set(x, y, 0); zemin.ekle(bog); }
    // rektum (arka)
    const rekM = M.korpus(); rekM.color.setHex(0xc0917d);
    const rektum = tup(egri([[-4.4, 4.8, -0.2], [-4.3, 2.2, -0.2], [-4.1, -0.4, -0.2], [-3.8, -2.4, -0.2]]), 0.7, rekM, 24, 14); zemin.ekle(rektum);
    L.push(zemin);
    // mesane: torna profiliyle armut biçimi, içinde idrar
    const mesM = M.mesane();
    const mes = o3('e-mesane').boya(mesM);
    const mK = tornaYumusak([[0.0, -1.5], [0.9, -1.45], [1.7, -0.9], [2.1, 0.0], [2.0, 1.0], [1.5, 1.8], [0.7, 2.25], [0.0, 2.3]], mesM); mK.position.set(-2.5, 2.9, 0); mK.scale.set(1, 1, 0.9); mes.ekle(mK);
    const idr = tornaYumusak([[0.0, -1.3], [0.8, -1.25], [1.5, -0.8], [1.85, 0.0], [1.75, 0.9], [1.3, 1.6], [0.0, 1.95]], M.idrar()); idr.position.set(-2.5, 2.9, 0); idr.scale.set(1, 1, 0.9); idr.castShadow = false; mes.ekle(idr);
    L.push(mes);
    const prM = M.prostat(); const pr = o3('e-prostat').boya(prM); const prK = yumru(1.25, 1.05, 1.15, prM); prK.position.set(-2.5, -0.05, 0); pr.ekle(prK); L.push(pr);
    const sfM = M.kas(); const sf = o3('e-sfinkter').boya(sfM); const sfK = halka(0.5, 0.22, sfM, 40); sfK.rotation.x = Math.PI / 2; sfK.position.set(-2.5, -1.15, 0); sf.ekle(sfK); L.push(sf);
    // penis: korpus kavernozum (üstte) + spongiozum (üretrayı sarar) + deri kılıf (yarı saydam)
    const pen = o3('e-penil'); const korM = M.korpus(); pen.boya(korM);
    const kor = kapsul(0.78, 4.6, korM); kor.rotation.z = Math.PI / 2; kor.position.set(2.5, -0.95, 0); kor.rotation.x = derece(0); pen.ekle(kor);
    const spong = tup(egri([[-1.3, -2.25, 0], [0.4, -1.95, 0], [2.4, -1.6, 0], [4.4, -1.38, 0], [5.6, -1.2, 0]]), 0.5, M.spongiosum(), 40, 14); pen.ekle(spong);
    const bulb = yumru(0.9, 0.65, 0.8, M.spongiosum()); bulb.position.set(-1.3, -2.25, 0); pen.ekle(bulb);
    const kilifM = M.deri(); kilifM.transparent = true; kilifM.opacity = 0.45; kilifM.depthWrite = false;
    const kilif = kapsul(1.05, 4.9, kilifM); kilif.rotation.z = Math.PI / 2; kilif.position.set(2.6, -1.2, 0); kilif.castShadow = false; pen.ekle(kilif);
    pen.etiketNoktasi = V(2.5, 0.1, 0.6); L.push(pen);
    const glM = M.glans(); const gl = o3('e-glans').boya(glM); const glK = yumru(1.0, 0.92, 0.9, glM); glK.position.set(5.55, -1.1, 0); gl.ekle(glK);
    const prep = halka(0.95, 0.22, M.deri(), 40); prep.rotation.y = Math.PI / 2; prep.position.set(4.9, -1.1, 0); gl.ekle(prep); L.push(gl);
    const me = o3('e-meatus'); const meK = yumru(0.08, 0.26, 0.16, M.koyu()); meK.position.set(6.5, -1.13, 0.05); me.ekle(meK); me.etiketNoktasi = V(6.5, -0.6, 0.3); L.push(me);
    const teM = M.testis(); const te = o3('e-testis').boya(teM);
    const sak = yumru(1.5, 1.9, 1.3, (() => { const m = M.deri(); m.transparent = true; m.opacity = 0.55; m.depthWrite = false; return m; })()); sak.position.set(2.0, -3.9, 0); sak.castShadow = false; te.ekle(sak);
    const teK = yumru(0.85, 1.1, 0.75, teM); teK.position.set(2.0, -3.9, 0); te.ekle(teK);
    const epi = tup(egri([[2.75, -3.0, 0.2], [2.95, -3.8, 0.2], [2.7, -4.7, 0.2]]), 0.2, M.korpus(), 20, 10); te.ekle(epi);
    te.etiketNoktasi = V(2.0, -5.6, 0.6); L.push(te);
    const urM = M.mukoza(); const ur = o3('e-uretra').boya(urM); const urT = tup(URETRA_E, 0.2, urM, 100, 14); ur.ekle(urT); ur.cizici = (f) => urT.ilerle(f); ur.etiketNoktasi = V(1.6, -2.45, 0.4); L.push(ur);
    // jel: meatustan geriye üretrayı dolduran saydam mavi
    const jel = o3('e-jel'); const jT = tup(uretraTers([6.6, -1.14, 0]), 0.3, M.jel(), 80, 12); jel.ekle(jT); jel.cizici = (f) => jT.ilerle(f * 0.72); jel.etiketNoktasi = V(3.0, -0.9, 0.6); L.push(jel);
    // kateter: dışarıdan meatusa, üretra boyunca mesaneye
    const kM = M.silikon(); const kat = o3('e-kateter').boya(kM); const kK = kateter(uretraTers(), 0.17, kM, 120); kat.ekle(kK); kat.cizici = (f) => kK.ilerle(f); kat.etiketNoktasi = V(7.2, -0.7, 0.4); L.push(kat);
    // kıvrım: bulbusta kıvrılan kateter
    const kiv = o3('e-kivrim'); const kivT = tup(egri([[7.6, -1.12, 0], [6.3, -1.15, 0], [4.4, -1.38, 0], [2.4, -1.6, 0], [0.4, -1.95, 0], [-1.0, -2.3, 0.1], [-1.7, -1.6, 0.2], [-1.0, -1.1, 0.25], [-0.4, -1.7, 0.2], [-1.2, -2.3, 0.15]]), 0.17, M.silikon(), 100, 12); kiv.ekle(kivT); kiv.cizici = (f) => kivT.ilerle(f); L.push(kiv);
    const bdM = M.izotonik(); const bd = o3('e-balon-dogru').boya(bdM); const bdK = kure(0.7, bdM, 32); bdK.position.set(-2.5, 2.3, 0); bd.ekle(bdK); const bdH = halka(0.8, 0.05, M.yesil(), 40); bdH.position.copy(bdK.position); bd.ekle(bdH); L.push(bd);
    const byM = M.kirmizi(); byM.transparent = true; byM.opacity = 0.8; const by = o3('e-balon-yanlis').boya(byM); const byK = yumru(0.85, 0.6, 0.6, byM); byK.position.set(-1.6, -2.2, 0); by.ekle(byK); L.push(by);
    const enj = o3('e-enjektor'); const eg = new THREE.Group(); eg.position.set(8.2, -1.12, 0);
    const govE = silindir(0.32, 0.32, 1.6, M.plastik()); govE.rotation.z = Math.PI / 2; govE.position.x = 0.8; eg.add(govE);
    const lu = silindir(0.1, 0.14, 0.5, M.plastikMat()); lu.rotation.z = Math.PI / 2; lu.position.x = -0.2; eg.add(lu);
    const cub = kutu(1.0, 0.1, 0.1, M.plastikMat()); cub.position.x = 2.0; eg.add(cub);
    enj.ekle(eg); L.push(enj);
    return L;
  },
};

// ———————————————————————————————————————— Yakın plan: üretra boyuna kesiti (oluk, içine bakılır)
const YakinUretra: Sahne3BTanim = {
  ad: 'Yakın plan: üretra boyuna kesiti',
  gizli: ['z-kivrim', 'z-balon', 'z-yirtik', 'z-kan', 'z-sivi', 'z-dogru'],
  etiket: {
    'z-mukoza': 'Üretra mukozası', 'z-spongiozum': 'Korpus spongiozum', 'z-sfinkter': 'Eksternal sfinkter', 'z-kivrim': 'Kateter takıldı, kıvrıldı',
    'z-balon': 'Balon üretrada şişti', 'z-yirtik': 'Mukoza yırtığı', 'z-sivi': '30–40 mL izotonik geri gelmiyor', 'z-dogru': 'Serbest kateter → mesaneye',
  },
  kamera: { poz: [0, 9.5, 12.5], hedef: [0, -0.8, 0] },
  zeminY: -2.6,
  kur: () => {
    const L: Oge3[] = [];
    const bump = puruz(5, 256, 0.3);
    // spongiozum: kalın yarım boru (dış), mukoza: iç yarım boru (oluk); açıklık kameraya (+Z) bakar
    const spM = M.spongiosum(); spM.color.setHex(0xc97d78); spM.side = THREE.DoubleSide; spM.bumpMap = bump; spM.bumpScale = 0.03;
    const sp = o3('z-spongiozum').boya(spM);
    // yarım boru: eksen X (Z ekseni etrafında 90°), alt yarı (θ π–2π) kalır → oluk yukarı açık
    // katı kesit: alt yarım halka (dış 2,4 / iç 1,1) X boyunca ekstrüde → üstte düz kesit yüzeyleri
    const yarimHalka = (ic: number, dis: number, boy: number) => {
      const sh = new THREE.Shape(); sh.absarc(0, 0, dis, Math.PI, Math.PI * 2, false); sh.absarc(0, 0, ic, Math.PI * 2, Math.PI, true); sh.closePath();
      const g = new THREE.ExtrudeGeometry(sh, { depth: boy, bevelEnabled: false, curveSegments: 48 }); g.rotateY(Math.PI / 2); g.translate(-boy / 2, 0, 0); return g;
    };
    const spK = mesh(yarimHalka(1.1, 2.4, 14), spM); sp.ekle(spK);
    // kesit kenar düzlemleri (kalınlık hissi)
    const kenarM = M.spongiosum(); kenarM.color.setHex(0xd98f8c);
    void kenarM;
    sp.etiketNoktasi = V(-4.5, 2.2, 0); L.push(sp);
    const muM = M.mukoza(); muM.side = THREE.DoubleSide; muM.bumpMap = bump; muM.bumpScale = 0.02;
    const mu = o3('z-mukoza').boya(muM);
    const muG = new THREE.CylinderGeometry(1.12, 1.12, 14.02, 48, 1, true, Math.PI, Math.PI); muG.rotateZ(Math.PI / 2);
    const muK = mesh(muG, muM); muK.castShadow = false; mu.ekle(muK);
    mu.etiketNoktasi = V(3.5, 1.0, 0.2); L.push(mu);
    // sfinkter: oluğu saran yarım halka (alt yarı, YZ düzleminde)
    const sfM = M.kas(); const sf = o3('z-sfinkter').boya(sfM); const sfK = mesh(yarimHalka(1.08, 2.75, 1.6), sfM); sfK.position.x = -3.2; sf.ekle(sfK); sf.etiketNoktasi = V(-3.2, 0.3, 2.4); L.push(sf);
    // doğru: serbest kateter oluk boyunca (sağdan sola, mesaneye)
    const kM = M.silikon(); const dg = o3('z-dogru').boya(kM); const dK = kateter(egri([[8, -0.35, 0.3], [4, -0.4, 0.3], [0, -0.45, 0.3], [-4, -0.45, 0.3], [-7.6, -0.4, 0.3]]), 0.42, kM, 80); dg.ekle(dK); dg.cizici = (f) => dK.ilerle(f); dg.etiketNoktasi = V(-5, 0.6, 0.6); L.push(dg);
    // kıvrım: takılıp katlanan kateter
    const kv = o3('z-kivrim'); const kvM = M.silikon(); kv.boya(kvM); const kvK = tup(egri([[8, -0.35, 0.3], [4, -0.4, 0.3], [1.0, -0.4, 0.3], [-0.4, -0.2, 0.35], [-0.8, 0.5, 0.5], [0.0, 0.7, 0.6], [0.9, 0.3, 0.6], [1.0, -0.4, 0.55], [0.0, -0.6, 0.6]]), 0.42, kvM, 100, 14); kv.ekle(kvK); kv.cizici = (f) => kvK.ilerle(f); kv.etiketNoktasi = V(0.2, 1.4, 0.6); L.push(kv);
    // balon üretrada: mukozayı geren küre (kırmızımsı saydam)
    const bM = M.izotonik(); bM.color.setHex(0xffd6d6); bM.attenuationColor = new THREE.Color(0xff8080); const b = o3('z-balon').boya(bM); const bK = kure(1.35, bM, 40); bK.position.set(0.5, -0.1, 0.2); b.ekle(bK); b.etiketNoktasi = V(0.5, 1.2, 0.8); L.push(b);
    // yırtık: mukozada kırmızı çatlak + kan damlaları
    const yrM = M.kan(); const yr = o3('z-yirtik').boya(yrM); const yrK = kutu(1.8, 0.12, 0.5, yrM); yrK.position.set(2.6, -0.95, 0.4); yrK.rotation.z = derece(12); yr.ekle(yrK); const yr2 = kutu(1.0, 0.1, 0.4, yrM); yr2.position.set(3.4, -0.75, 0.5); yr2.rotation.z = derece(-20); yr.ekle(yr2); yr.etiketNoktasi = V(2.8, -0.5, 0.8); L.push(yr);
    const kan = o3('z-kan'); const kanA = akis(egri([[2.8, -0.9, 0.5], [4.5, -0.6, 0.6], [6.5, -0.4, 0.6], [8.2, -0.3, 0.6]]), 10, 0.14, M.kan()); kan.ekle(kanA); kan.cizici = (f) => kanA.ilerle(f); kan.tik = (t) => kanA.tik(t, 0); L.push(kan);
    // sıvı: geri gelmeyen izotonik (oluğu dolduran saydam mavi silindir)
    const svM = M.izotonik(); const sv = o3('z-sivi').boya(svM); const svG = new THREE.CylinderGeometry(1.0, 1.0, 5.5, 32, 1, false, Math.PI, Math.PI); svG.rotateZ(Math.PI / 2);
    const svK = mesh(svG, svM); svK.position.set(-3.8, 0, 0); svK.castShadow = false; sv.ekle(svK); sv.etiketNoktasi = V(-3.8, 1.2, 0.5); L.push(sv);
    return L;
  },
};

export const SAHNELER3B: Record<string, Sahne3BTanim> = {
  foley: Foley, 'yakin-mesane': YakinMesane, erkek: Erkek, 'yakin-uretra': YakinUretra, ...SAHNELER3B_2, ...SAHNELER3B_ORGANIK,
};
