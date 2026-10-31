/**
 * KMB 3B — organik (marching cubes) sahneler: insan dokusu tek, kaynaşmış yüzey olarak kurulur (parça parça kapsül/küre
 * yok → iç içe geçme ve ek yeri yok). Islak alanlar yüzeyi saran ince parlak film (katı değil), açıklıklar oyularak açılır.
 * Bu küme sahneler3b_2'deki ilkel sürümlerin yerini alır (kayıt: SAHNELER3B_ORGANIK, sonra yüklenen kazanır).
 */
import * as THREE from 'three';
import type { Sahne3BTanim } from './Sahne3B';
import { M, Oge3, V, akis, egri, halka, kapsul, kateter, kure, kutu, mesh, organik, zincir, islakM, silindir, tup, yumru, yuvarlakKutu, derece, type Top } from './yardimci';

const o3 = (id: string) => new Oge3(id);
type P3 = [number, number, number];

/** Eldivenli el (organik): avuç + 4 parmak + başparmak; `kivrim` 0 düz … 1 yumruk; `ayna` sağ/sol. Yerel: avuç XY düzlemi, parmaklar +Y, avuç içi +Z. */
export function elOrganik(m: THREE.Material, kivrim = 0.5, ayna = 1, coz = 72) {
  const T: Top[] = [];
  // avuç: 2×3 yumuşak top ızgarası
  for (const [x, y] of [[-0.55, -0.1], [0.55, -0.1], [-0.6, 0.75], [0.6, 0.75], [0, 0.3], [0, -0.7], [-0.3, 0.3], [0.3, 0.3]] as const) T.push({ p: [x * ayna, y, 0], r: 0.78, k: 3.5 });
  // bilek
  T.push(...zincir([0, -1.2, 0], [0, -2.4, 0], 0.62, 4, 9));
  // parmaklar: kök (avuç üstü) → boğum → uç; kıvrım parmakları +Z'ye (avuç içine) doğru katlar
  const parmak = (x: number, boy: number) => {
    const a = kivrim * derece(80), b = kivrim * derece(95);
    const p0: P3 = [x * ayna, 1.35, 0];
    const p1: P3 = [x * ayna, p0[1] + Math.cos(a) * boy * 0.5, p0[2] + Math.sin(a) * boy * 0.5];
    const p2: P3 = [x * ayna, p1[1] + Math.cos(a + b) * boy * 0.5, p1[2] + Math.sin(a + b) * boy * 0.5];
    T.push(...zincir(p0, p1, 0.3, 4, 7, 0.27), ...zincir(p1, p2, 0.27, 4, 7, 0.24));
  };
  [[-0.72, 1.9], [-0.24, 2.2], [0.24, 2.1], [0.72, 1.7]].forEach(([x, boy]) => parmak(x, boy));
  // başparmak: avucun yanından, içe doğru
  const b0: P3 = [-1.15 * ayna, -0.3, 0.2], b1: P3 = [-1.55 * ayna, 0.5, 0.55 + kivrim * 0.5], b2: P3 = [-1.3 * ayna, 1.1 + kivrim * 0.2, 1.0 + kivrim * 1.1];
  T.push(...zincir(b0, b1, 0.36, 4, 6, 0.32), ...zincir(b1, b2, 0.32, 4, 7, 0.28));
  return organik(T, m, [0, 0.2, 0.9], 3.4, coz);
}

/** Stilize insan (organik gövde + büyük gözlü yüz). Yerel: ayakta, +Y yukarı, yüz +Z'ye bakar; boy ≈ 7,2 birim. */
export function insanOrganik(o: { deri?: THREE.Material; giysi?: THREE.Material; kalca?: number; diz?: number; kolAcik?: number; coz?: number }) {
  const deri = o.deri || M.deri(), giysi = o.giysi || M.onluk();
  const g = new THREE.Group();
  const kalca = o.kalca ?? 0, diz = o.diz ?? 0;
  // gövde + giysi (giysi gövdeyi sarar: ayrı organik, biraz daha büyük)
  const gov: Top[] = [{ p: [0, 2.9, 0], r: 0.8, k: 7 }, { p: [0, 2.2, 0], r: 0.85, k: 7 }, { p: [0, 1.5, 0], r: 0.82, k: 7 }, { p: [0, 0.9, 0], r: 0.8, k: 7 }, { p: [-0.5, 0.75, 0], r: 0.55, k: 8 }, { p: [0.5, 0.75, 0], r: 0.55, k: 8 }];
  g.add(organik(gov.map((t) => ({ ...t, r: t.r * 1.08 })), giysi, [0, 1.8, 0], 2.4, 56));
  // baş + boyun (deri): yuvarlak, yanaklı
  const bas: Top[] = [{ p: [0, 4.35, 0], r: 0.78, k: 8 }, { p: [0, 4.05, 0.15], r: 0.62, k: 9 }, { p: [-0.35, 4.05, 0.3], r: 0.36, k: 12 }, { p: [0.35, 4.05, 0.3], r: 0.36, k: 12 }, { p: [0, 3.55, 0], r: 0.26, k: 12 }, { p: [0, 3.35, 0], r: 0.3, k: 10 }];
  g.add(organik(bas, deri, [0, 4.1, 0.1], 1.6, 56));
  // saç kabı
  const sac = mesh(new THREE.SphereGeometry(0.84, 32, 16, 0, Math.PI * 2, 0, derece(100)), M.koyu()); sac.position.set(0, 4.45, -0.05); g.add(sac);
  // gözler: büyük beyaz + iris + ışık
  for (const s of [-1, 1]) {
    const goz = kure(0.19, M.beyaz(), 20); goz.position.set(s * 0.3, 4.4, 0.66); goz.scale.set(1, 1.25, 0.6); g.add(goz);
    const iris = kure(0.1, (() => { const m = M.koyu(); m.color.setHex(0x3a5a8a); return m; })(), 16); iris.position.set(s * 0.3, 4.4, 0.77); iris.scale.set(1, 1.2, 0.5); g.add(iris);
    const isik = kure(0.035, M.beyaz(), 8); isik.position.set(s * 0.26, 4.46, 0.83); g.add(isik);
    const kas = kapsul(0.035, 0.24, M.koyu()); kas.position.set(s * 0.3, 4.72, 0.62); kas.rotation.z = Math.PI / 2 + s * derece(-8); g.add(kas);
  }
  const agiz = mesh(new THREE.TorusGeometry(0.14, 0.03, 8, 24, Math.PI), (() => { const m = M.kas(); m.color.setHex(0xb0564f); return m; })()); agiz.position.set(0, 3.98, 0.68); agiz.rotation.z = Math.PI; g.add(agiz);
  // kollar (deri) + eller
  for (const s of [-1, 1]) {
    const ac = o.kolAcik ?? derece(14);
    const omuz: P3 = [s * 0.95, 2.95, 0], dirsek: P3 = [s * (0.95 + Math.sin(ac) * 1.3), 2.95 - Math.cos(ac) * 1.3, 0.1], el: P3 = [s * (0.95 + Math.sin(ac) * 2.5), 2.95 - Math.cos(ac) * 2.5, 0.25];
    g.add(organik([...zincir(omuz, dirsek, 0.3, 5, 5, 0.26), ...zincir(dirsek, el, 0.26, 5, 5, 0.22), { p: el, r: 0.32, k: 6 }], deri, [s * 1.6, 1.9, 0.1], 1.9, 56));
  }
  // bacaklar: kalça ve diz açıları (litotomi için), ayaklar
  for (const s of [-1, 1]) {
    const k0: P3 = [s * 0.42, 0.45, 0];
    const d: P3 = [s * (0.42 + (kalca ? 0.3 : 0.02)), 0.45 - Math.cos(kalca) * 1.9, Math.sin(kalca) * 1.9];
    const a: P3 = [d[0], d[1] - Math.cos(kalca - diz) * 1.9, d[2] + Math.sin(kalca - diz) * 1.9];
    const ayak: P3 = [a[0], a[1] - 0.15, a[2] + 0.45];
    g.add(organik([...zincir(k0, d, 0.42, 6, 5, 0.34), { p: d, r: 0.36, k: 6 }, ...zincir(d, a, 0.32, 6, 5, 0.26), ...zincir(a, ayak, 0.24, 3, 6, 0.2)], deri, [s * 0.6, -1.4, 1.0], 3.2, 64));
  }
  return g;
}

// ———————————————————————————————————————— Kadın dış genital bölge (litotomide, önden)
function kadinDokusu(olcek = 1) {
  // deri: mons (üst), iki labium majus, perine (alt), yanlarda geniş gövde — orta hatta kütle YOK (vestibül aralığı doğal kalır)
  const deri: Top[] = [
    { p: [0, 3.9, -0.3], r: 2.1, k: 5 }, { p: [-1.3, 3.3, -0.4], r: 1.4, k: 6 }, { p: [1.3, 3.3, -0.4], r: 1.4, k: 6 }, // mons pubis
    ...zincir([-1.75, 2.5, 0.5], [-1.5, -2.6, 0.3], 0.95, 14, 6, 0.8), ...zincir([1.75, 2.5, 0.5], [1.5, -2.6, 0.3], 0.95, 14, 6, 0.8), // labia majora
    { p: [0, -3.6, -0.1], r: 0.95, k: 6 }, { p: [0, -4.6, -0.6], r: 1.6, k: 5 }, // posterior komissür + perine
    ...[-4.2, -2.4, 2.4, 4.2].flatMap((x) => [-3.2, -0.6, 2.0].map((y) => ({ p: [x, y, -2.1] as P3, r: 2.3, k: 2.5 }))), // yan gövde: yumuşak, sürekli deri zemini
    { p: [0, 0.0, -2.6], r: 2.3, k: 3 }, { p: [0, -2.6, -2.6], r: 2.2, k: 3 }, // arka zemin (aralığın dibi, derinde)
    { p: [0, 2.55, 0.65], r: 0.5, k: 8 }, // klitoris başlığı
  ];
  // mukoza: labia minora (ince, kıvrımlı) + vestibül tabanı; meatus ve vajina girişi oyulur
  const muk: Top[] = [
    ...zincir([-0.6, 2.0, 0.55], [-0.5, -2.2, 0.45], 0.34, 16, 6, 0.26), ...zincir([0.6, 2.0, 0.55], [0.5, -2.2, 0.45], 0.34, 16, 6, 0.26),
    ...zincir([0, 1.8, 0.15], [0, -2.6, 0.05], 0.55, 16, 5, 0.5),
    { p: [0, 1.05, 0.75], r: 0.24, k: 20, oy: true }, // meatus
    ...zincir([0, -0.5, 0.75], [0, -1.7, 0.7], 0.42, 4, 16).map((t) => ({ ...t, oy: true })), // vajina girişi
  ];
  const s = (t: Top): Top => ({ ...t, p: [t.p[0] * olcek, t.p[1] * olcek, t.p[2] * olcek], r: t.r * olcek });
  return { deri: deri.map(s), muk: muk.map(s) };
}
const Kadin: Sahne3BTanim = {
  ad: 'Kadın dış genital bölge (litotomide, önden)',
  gizli: ['k-temizlik', 'k-ortu', 'k-halka', 'k-kateter', 'k-idrar'],
  etiket: { 'k-majus': 'Labium majus', 'k-minus': 'Labium minus', 'k-klitoris': 'Klitoris', 'k-meatus': 'Eksternal üretra ağzı (meatus)', 'k-vajina': 'Vajina girişi', 'k-ortu': 'Steril delikli örtü', 'k-temizlik': 'Antiseptik: merkezden dışa, nemli alan' },
  kamera: { poz: [0, 1.6, 11.5], hedef: [0, -0.2, 0.2] },
  kur: () => {
    const L: Oge3[] = [];
    const { deri, muk } = kadinDokusu();
    const dM = M.deri(); const maj = o3('k-majus').boya(dM); maj.ekle(organik(deri, dM, [0, -0.3, -1.2], 7.4, 112)); maj.etiketNoktasi = V(-2.4, 2.6, 0.9); L.push(maj);
    const mM = M.mukoza(); const min = o3('k-minus').boya(mM); const mukK = organik(muk, mM, [0, -0.3, 0.3], 3.2, 104); min.ekle(mukK); min.etiketNoktasi = V(1.0, 2.0, 1.1); L.push(min);
    const kM = M.glans(); const kli = o3('k-klitoris').boya(kM); const kK = kure(0.22, kM, 20); kK.position.set(0, 2.08, 0.9); kli.ekle(kK); kli.etiketNoktasi = V(0, 2.5, 1.1); L.push(kli);
    // açıklıkların iç astarı (oyuğun içinde koyu mukoza): oyuk boşluğa bakmasın
    const icM = M.mukoza(); icM.color.setHex(0x8a3836); icM.roughness = 0.35;
    const mea = o3('k-meatus').boya(icM); const meK = yumru(0.2, 0.26, 0.2, icM); meK.position.set(0, 1.05, 0.55); mea.ekle(meK); mea.etiketNoktasi = V(0, 1.35, 1.1); L.push(mea);
    const vaj = o3('k-vajina').boya(icM); const vK = yumru(0.38, 0.9, 0.3, icM); vK.position.set(0, -1.1, 0.5); vaj.ekle(vK); vaj.etiketNoktasi = V(0, -2.3, 1.1); L.push(vaj);
    // antiseptik: mukozayı ve iç labiaları saran ıslak kahverengi film (yüzeyi birebir izler) + gazlı bez/pens
    const tem = o3('k-temizlik'); const tM = islakM(0x9a4a14, 0.5); tem.boya(tM);
    const film = organik(muk.filter((t) => !t.oy).map((t) => ({ ...t, r: t.r * 1.06 })), tM, [0, -0.3, 0.3], 3.2, 88); film.castShadow = false; tem.ekle(film);
    const bez = new THREE.Group(); const gaz = yumru(0.42, 0.36, 0.3, M.beyaz()); bez.add(gaz); const pens = kapsul(0.07, 3.0, M.metal()); pens.position.set(0.9, 0.9, 1.4); pens.rotation.z = derece(-50); pens.rotation.x = derece(-40); bez.add(pens);
    bez.position.set(0.0, 1.1, 1.25); tem.ekle(bez);
    tem.cizici = (f) => { tM.opacity = 0.5 * Math.min(1, f * 1.4); const a = f * Math.PI * 2 * 3; const r = 0.3 + f * 1.4; bez.position.set(Math.cos(a) * r * 1.1, 1.1 + Math.sin(a) * r * 1.3, 1.25); bez.visible = f < 0.999; };
    tem.etiketNoktasi = V(2.0, 3.2, 1.3); L.push(tem);
    const ortu = o3('k-ortu'); const oM = M.ortu(); ortu.boya(oM);
    const sh = new THREE.Shape(); sh.moveTo(-9, -7); sh.lineTo(9, -7); sh.lineTo(9, 7); sh.lineTo(-9, 7); sh.closePath();
    const d = new THREE.Path(); d.absellipse(0, 0, 3.6, 4.8, 0, Math.PI * 2, false, 0); sh.holes.push(d);
    const oK = mesh(new THREE.ExtrudeGeometry(sh, { depth: 0.06, bevelEnabled: false, curveSegments: 32 }), oM); oK.position.set(0, 0.0, 1.35); ortu.ekle(oK); ortu.etiketNoktasi = V(-5.2, 4.8, 1.5); L.push(ortu);
    const hal = o3('k-halka'); const halM = M.silikon(); hal.boya(halM);
    const sarmal = new THREE.CatmullRomCurve3(Array.from({ length: 140 }, (_, i) => { const a = (i / 139) * Math.PI * 2 * 2.5; return V(3.8 + Math.cos(a) * 1.0, 3.2 + Math.sin(a) * 0.95 * 0.3 + (i / 139) * 0.3, 2.4 + Math.sin(a) * 1.0); }));
    hal.ekle(tup(sarmal, 0.17, halM, 140, 12)); L.push(hal);
    const kat = o3('k-kateter'); const katM = M.silikon(); kat.boya(katM); const katK = kateter(egri([[4.0, 3.4, 3.2], [2.6, 2.6, 2.4], [1.2, 1.5, 1.6], [0.2, 1.1, 1.15], [0, 1.05, 0.6]]), 0.17, katM, 60); kat.ekle(katK); kat.cizici = (f) => katK.ilerle(f); L.push(kat);
    const idr = o3('k-idrar'); const idA = akis(egri([[0, 1.05, 0.85], [0.2, 1.1, 1.25], [1.2, 1.5, 1.7], [2.6, 2.6, 2.5], [4.0, 3.4, 3.3]]), 10, 0.1, M.idrarMat()); idr.ekle(idA); idr.cizici = (f) => idA.ilerle(f); idr.tik = (t) => idA.tik(t, 0); L.push(idr);
    return L;
  },
};

// ———————————————————————————————————————— Yakın plan: vestibül ve meatus (parmaklar labiaları ayırıyor)
const YakinKadin: Sahne3BTanim = {
  ad: 'Yakın plan: vestibül ve meatus (eldivenli parmaklar labiaları ayırıyor)',
  gizli: ['v-kateter', 'v-jel', 'v-idrar', 'v-parmak'],
  etiket: { 'v-klitoris': 'Klitoris', 'v-meatus': 'Meatus: üstteki küçük açıklık', 'v-vajina': 'Vajina: alttaki geniş açıklık', 'v-minus': 'Labium minus', 'v-parmak': 'Başparmak + işaret parmağı ayırır', 'v-jel': 'Uçta ~2 mL jel' },
  kamera: { poz: [0, 3.0, 13.5], hedef: [0, -0.3, 0] },
  kur: () => {
    const L: Oge3[] = [];
    const { deri, muk } = kadinDokusu(1.9);
    const zemin = o3('_zemin'); zemin.ekle(organik(deri, M.deri(), [0, -0.6, -2.3], 14.0, 112)); L.push(zemin);
    // ayrılmış labia minora (parmaklar açmış): daha geniş aralık
    const mukAcik = muk.map((t) => (t.oy ? t : { ...t, p: [t.p[0] * (Math.abs(t.p[0]) > 0.5 ? 1.35 : 1), t.p[1], t.p[2]] as P3 }));
    const mM = M.mukoza(); const min = o3('v-minus').boya(mM); min.ekle(organik(mukAcik, mM, [0, -0.6, 0.6], 6.2, 112)); min.etiketNoktasi = V(-2.2, 3.4, 1.4); L.push(min);
    const kM = M.glans(); const kli = o3('v-klitoris').boya(kM); const kK = kure(0.42, kM, 24); kK.position.set(0, 3.95, 1.7); kli.ekle(kK); kli.etiketNoktasi = V(0, 4.7, 1.9); L.push(kli);
    const icM = M.mukoza(); icM.color.setHex(0x8a3836);
    const mea = o3('v-meatus').boya(icM); const meK = yumru(0.36, 0.5, 0.3, icM); meK.position.set(0, 2.0, 1.05); mea.ekle(meK); mea.etiketNoktasi = V(0, 2.6, 2.0); L.push(mea);
    const vaj = o3('v-vajina').boya(icM); const vK = yumru(0.7, 1.7, 0.5, icM); vK.position.set(0, -2.1, 0.95); vaj.ekle(vK); vaj.etiketNoktasi = V(0, -4.2, 2.0); L.push(vaj);
    // sol elin başparmak + işaret parmağı: labia majora'yı yanlara açar (organik, steril eldiven)
    const par = o3('v-parmak'); const pM = M.eldivenSteril(); par.boya(pM);
    const parmaklar: Top[] = [...zincir([-7.5, -3.5, 3.6], [-3.4, 0.4, 2.5], 0.62, 16, 9, 0.5), ...zincir([7.5, -3.5, 3.6], [3.4, 0.4, 2.5], 0.62, 16, 9, 0.5)];
    par.ekle(organik(parmaklar, pM, [0, -1.5, 3.0], 9, 96)); par.etiketNoktasi = V(4.2, -2.6, 3.8); L.push(par);
    const kat = o3('v-kateter'); const katM = M.silikon(); kat.boya(katM); const katK = kateter(egri([[6.5, 6.5, 5.5], [3.4, 4.2, 3.8], [1.2, 2.6, 2.6], [0.2, 2.05, 2.0], [0, 2.0, 1.2]]), 0.3, katM, 60); kat.ekle(katK); kat.cizici = (f) => katK.ilerle(f); L.push(kat);
    const jel = o3('v-jel'); const jM = islakM(0x8fc7ff, 0.75); jel.boya(jM); const jK = yumru(0.5, 0.5, 0.5, jM); jK.position.set(0.1, 2.05, 1.85); jel.ekle(jK); jel.etiketNoktasi = V(0.7, 2.7, 2.1); L.push(jel);
    const idr = o3('v-idrar'); const idA = akis(egri([[0, 2.0, 1.4], [0.2, 2.05, 2.1], [1.2, 2.6, 2.8], [3.4, 4.2, 4.0], [6.5, 6.5, 5.7]]), 10, 0.15, M.idrarMat()); idr.ekle(idA); idr.cizici = (f) => idA.ilerle(f); idr.tik = (t) => idA.tik(t, 0); L.push(idr);
    return L;
  },
};

// ———————————————————————————————————————— Yakın plan: glans, meatus, antiseptik ve lidokainli jel
const YakinErkekJel: Sahne3BTanim = {
  ad: 'Yakın plan: glans, meatus ve lidokainli jelin verilmesi',
  gizli: ['j-temizlik', 'j-siringa', 'j-dolum', 'j-parmak'],
  etiket: { 'j-glans': 'Glans penis', 'j-prepisyum': 'Prepisyum geri çekilir', 'j-meatus': 'Meatus', 'j-temizlik': 'Antiseptik: meatustan dışa, 3 kez (nemli)', 'j-siringa': 'Jel tüpü meatusta', 'j-dolum': 'Jel üretrayı doldurur', 'j-parmak': 'Ucu sık, 2–3 dk bekle' },
  kamera: { poz: [3.5, 4.0, 14], hedef: [0.5, 0, 0] },
  zeminY: -3.4,
  kur: () => {
    const L: Oge3[] = [];
    const zemin = o3('_zemin'); const ortu = yuvarlakKutu(24, 16, 0.1, 0.5, M.ortu()); ortu.rotation.x = -Math.PI / 2; ortu.position.y = -3.4; ortu.receiveShadow = true; zemin.ekle(ortu); L.push(zemin);
    // glans + korona + gövde ucu: tek organik yüzey; meatus oyulur (dikey yarık)
    const glansT: Top[] = [{ p: [0.6, 0, 0], r: 1.85, k: 9 }, { p: [1.3, 0, 0], r: 1.45, k: 10 }, { p: [1.95, 0, 0], r: 0.95, k: 12 },
      ...Array.from({ length: 40 }, (_, i) => { const a = (i / 40) * Math.PI * 2; return { p: [-0.75, Math.cos(a) * 1.5, Math.sin(a) * 1.5] as P3, r: 0.5, k: 8 }; }), // korona
      ...zincir([-1.6, -0.05, 0], [-7.5, -0.1, 0], 1.45, 16, 6, 1.5),
      { p: [2.5, 0.22, 0], r: 0.2, k: 24, oy: true }, { p: [2.5, -0.22, 0], r: 0.2, k: 24, oy: true }, { p: [2.5, 0, 0], r: 0.22, k: 24, oy: true }]; // meatus yarığı
    const gM = M.glans(); const gl = o3('j-glans').boya(gM); gl.ekle(organik(glansT, gM, [-2.5, 0, 0], 6.0, 104)); gl.etiketNoktasi = V(0.6, 2.0, 0.8); L.push(gl);
    const meM = M.mukoza(); meM.color.setHex(0x7a2f2c); const me = o3('j-meatus').boya(meM); const mK = yumru(0.12, 0.42, 0.2, meM); mK.position.set(2.42, 0, 0); me.ekle(mK); me.etiketNoktasi = V(2.6, 0.7, 0.5); L.push(me);
    // geri çekilmiş prepisyum: gövdeyi saran kıvrımlı deri bileziği (organik halka)
    const pT: Top[] = Array.from({ length: 44 }, (_, i) => { const a = (i / 44) * Math.PI * 2; return { p: [-2.3 + 0.12 * Math.sin(a * 3), Math.cos(a) * 1.6, Math.sin(a) * 1.6] as P3, r: 0.6, k: 7 }; });
    const pM = M.deri(); const pr = o3('j-prepisyum').boya(pM); pr.ekle(organik(pT, pM, [-2.3, 0, 0], 3.2, 80)); pr.etiketNoktasi = V(-2.3, 2.5, 0.4); L.push(pr);
    // antiseptik: glansı saran ıslak film (yüzeyi izler) + gazlı bez dairesel siler
    const tem = o3('j-temizlik'); const tM = islakM(0x9a4a14, 0.5); tem.boya(tM);
    const film = organik(glansT.filter((t) => !t.oy && t.p[0] > -1.2).map((t) => ({ ...t, r: t.r * 1.045 })), tM, [-2.5, 0, 0], 6.0, 88); film.castShadow = false; tem.ekle(film);
    const bez = new THREE.Group(); const gaz = yumru(0.5, 0.4, 0.4, M.beyaz()); bez.add(gaz); const pens = kapsul(0.07, 3.2, M.metal()); pens.position.set(1.2, 1.0, 1.0); pens.rotation.z = derece(-35); pens.rotation.x = derece(-30); bez.add(pens);
    tem.ekle(bez);
    tem.cizici = (f) => { tM.opacity = 0.5 * Math.min(1, f * 1.4); const a = f * Math.PI * 2 * 3; const r = 0.3 + f * 1.4; bez.position.set(2.45 - r * r * 0.3, Math.cos(a) * r, Math.sin(a) * r); bez.visible = f < 0.999; };
    tem.etiketNoktasi = V(2.2, 2.1, 1.0); L.push(tem);
    const sir = o3('j-siringa'); const sg = new THREE.Group(); sg.position.set(2.75, 0, 0);
    const tupG = silindir(0.55, 0.55, 3.2, M.plastik()); tupG.rotation.z = Math.PI / 2; tupG.position.x = 2.1; sg.add(tupG);
    const jelIc = silindir(0.46, 0.46, 2.0, M.jel()); jelIc.rotation.z = Math.PI / 2; jelIc.position.x = 1.6; jelIc.castShadow = false; sg.add(jelIc);
    const ucG = mesh(new THREE.ConeGeometry(0.42, 0.9, 24), M.plastikMat()); ucG.rotation.z = Math.PI / 2; ucG.position.x = 0.1; sg.add(ucG);
    const pis = kutu(1.6, 0.18, 0.18, M.plastikMat()); pis.position.x = 4.4; sg.add(pis); const pb = kutu(0.1, 1.0, 1.0, M.plastikMat()); pb.position.x = 5.2; sg.add(pb);
    sir.ekle(sg); sir.etiketNoktasi = V(4.8, 0.9, 0.3); L.push(sir);
    // jel dolumu: üretra boyunca (gövde yarı saydam değil → üretra izdüşümü gövde yüzeyinin hemen önünde, hafif mavi parıltı)
    const dol = o3('j-dolum'); const dM = islakM(0x8fc7ff, 0.6); dol.boya(dM); const dT = tup(egri([[2.4, 0, 0.2], [0.9, -0.3, 1.5], [-1.3, -0.5, 1.55], [-4, -0.6, 1.6], [-7.4, -0.6, 1.6]]), 0.3, dM, 60, 10); dT.castShadow = false; dol.ekle(dT); dol.cizici = (f) => dT.ilerle(f); dol.etiketNoktasi = V(-3.5, 0.2, 2.0); L.push(dol);
    // ucu sıkan parmaklar (organik, steril eldiven): glansın altından ve üstünden
    const par = o3('j-parmak'); const prM = M.eldivenSteril(); par.boya(prM);
    const parT: Top[] = [...zincir([1.6, 4.2, 2.6], [2.0, 1.9, 1.0], 0.55, 14, 9, 0.5), ...zincir([1.6, -4.2, 2.6], [2.0, -1.9, 1.0], 0.55, 14, 9, 0.5)];
    par.ekle(organik(parT, prM, [1.8, 0, 2.0], 5.5, 80)); par.etiketNoktasi = V(1.8, 3.2, 2.4); L.push(par);
    return L;
  },
};

// ———————————————————————————————————————— Yakın plan: steril eldivenle kateteri avuçta toplamak
const YakinEl: Sahne3BTanim = {
  ad: 'Yakın plan: steril eldivenle kateteri avuçta toplamak',
  gizli: ['h-yanlis', 'h-jel'],
  etiket: { 'h-el': 'Steril eldivenli el', 'h-halka': 'Kateter avuçta halka halinde', 'h-uc': 'Yalnız uç dışarıda, steril', 'h-yanlis': 'Sarkan kateter dokunur → steril değil', 'h-jel': 'Uca jel' },
  kamera: { poz: [0.5, 5.0, 12], hedef: [0.0, 0.0, 0.6] },
  zeminY: -2.6,
  kur: () => {
    const L: Oge3[] = [];
    const zemin = o3('_zemin'); const ortu = yuvarlakKutu(20, 14, 0.1, 0.5, M.ortuAcik()); ortu.rotation.x = -Math.PI / 2; ortu.position.y = -2.6; ortu.receiveShadow = true; zemin.ekle(ortu); L.push(zemin);
    // el: avuç yukarı-kameraya dönük, parmaklar halkanın üstüne kıvrık
    const eM = M.eldivenSteril(); const elO = o3('h-el').boya(eM); const eG = elOrganik(eM, 0.78, 1, 96); eG.scale.setScalar(1.3); eG.rotation.set(derece(-42), derece(0), derece(0)); eG.position.set(-0.3, -1.3, -0.2); elO.ekle(eG); elO.etiketNoktasi = V(-3.4, 0.0, 1.4); L.push(elO);
    // halka: avucun içinde (kıvrık parmakların altında), eğik düzlemde
    const hM = M.silikon(); const hal = o3('h-halka').boya(hM);
    // halka avuç düzleminde (el -42° eğik → düzlem normali kameraya doğru): y ve z eğimle birlikte
    const sarmal = new THREE.CatmullRomCurve3(Array.from({ length: 160 }, (_, i) => { const a = (i / 159) * Math.PI * 2 * 2.6; const r = 0.85 + 0.04 * Math.sin(a * 2); const u = Math.sin(a) * r, h = (i / 159) * 0.3; return V(-0.3 + Math.cos(a) * r, 0.0 + u * 0.72 + h * 0.74, 1.0 + u * 0.67 - h * 0.67); }));
    hal.ekle(tup(sarmal, 0.18, hM, 160, 12)); hal.etiketNoktasi = V(-0.2, 1.4, 1.6); L.push(hal);
    const ucM = M.silikon(); const uc = o3('h-uc').boya(ucM); const ucK = kateter(egri([[0.7, 0.2, 1.5], [2.2, 0.5, 2.0], [3.8, 0.9, 2.6]]), 0.18, ucM, 30); uc.ekle(ucK); uc.etiketNoktasi = V(3.8, 1.5, 2.6); L.push(uc);
    const yan = o3('h-yanlis'); const yM = M.silikon(); yan.boya(yM); const yT = tup(egri([[-1.1, 0.1, 1.5], [-2.6, -1.0, 2.3], [-3.6, -2.2, 3.0], [-5.2, -2.55, 3.4]]), 0.18, yM, 60, 12); yan.ekle(yT); yan.cizici = (f) => yT.ilerle(f);
    const leke = yumru(0.9, 0.04, 0.6, M.kirmizi()); leke.position.set(-4.5, -2.56, 3.3); yan.ekle(leke); yan.etiketNoktasi = V(-4.4, -1.8, 3.3); L.push(yan);
    const jel = o3('h-jel'); const jM = islakM(0x8fc7ff, 0.7); jel.boya(jM); const jK = yumru(0.34, 0.3, 0.34, jM); jK.position.set(3.85, 0.92, 2.65); jK.castShadow = false; jel.ekle(jK); L.push(jel);
    return L;
  },
};

// ———————————————————————————————————————— Eğitim maketi (fotoğraf referansı: kare kesitli genital modül, mavi eldivenli eller)
const Maket: Sahne3BTanim = {
  ad: 'Kateter uygulama eğitim maketi',
  gizli: ['mk-hazne-dolu', 'mk-erkek'],
  etiket: { 'mk-govde': 'Pelvis gövdesi + uyluklar', 'mk-kadin': 'Kadın genital modülü', 'mk-erkek': 'Erkek genital modülü', 'mk-hazne': 'Mesane haznesi (su doldurulur)', 'mk-hazne-dolu': 'Dolu hazne: kateterden "idrar" gelir' },
  kamera: { poz: [10, 8, 14], hedef: [2.0, 2.2, 0.3] },
  zeminY: 0,
  kur: () => {
    const L: Oge3[] = [];
    const zemin = o3('_zemin'); const masa = yuvarlakKutu(28, 0.4, 18, 0.4, M.yatak()); masa.position.y = -0.2; masa.receiveShadow = true; zemin.ekle(masa); L.push(zemin);
    const gM = M.deri(); gM.color.setHex(0xefc6a6); gM.roughness = 0.5;
    const gov = o3('mk-govde').boya(gM);
    // pelvis gövdesi: karın alt bölümü + kalçalar + bükülü uyluklar (fotoğraftaki gibi açık bacaklı maket), tek organik yüzey
    // fotoğraf: pelvis bloğu + bükülü, açık uyluklar; ön yüzde kare modül yuvası
    const govT: Top[] = [{ p: [-3.0, 2.2, 0], r: 2.7, k: 6 }, { p: [-1.2, 2.0, -1.5], r: 2.1, k: 7 }, { p: [-1.2, 2.0, 1.5], r: 2.1, k: 7 }, { p: [-3.8, 2.9, 0], r: 2.1, k: 7 }, { p: [-0.4, 1.4, 0], r: 1.6, k: 8 },
      ...zincir([0.3, 1.9, -2.2], [4.6, 2.3, -3.8], 1.45, 12, 7, 1.3), ...zincir([0.3, 1.9, 2.2], [4.6, 2.3, 3.8], 1.45, 12, 7, 1.3)];
    gov.ekle(organik(govT, gM, [0.5, 2.0, 0], 8.0, 104)); gov.etiketNoktasi = V(-3.0, 5.2, 0); L.push(gov);
    // kare modül yuvası (koyu kenarlı çerçeve) — modül önden takılır
    const cerM = M.deri(); cerM.color.setHex(0xd8ad8f); const cer = yuvarlakKutu(3.2, 3.2, 0.4, 0.25, cerM); cer.position.set(1.6, 2.2, 0); cer.rotation.y = Math.PI / 2; zemin.ekle(cer);
    const hM = M.plastik(); hM.transmission = 0.75; const haz = o3('mk-hazne').boya(hM); const hK = yuvarlakKutu(3.2, 2.2, 3.8, 0.4, hM); hK.position.set(-4.0, 6.4, 0); haz.ekle(hK); const kapak = silindir(0.6, 0.6, 0.4, M.mavi()); kapak.position.set(-4.0, 7.7, 0); haz.ekle(kapak);
    const hort = tup(egri([[-4.0, 5.3, 0], [-3.0, 4.2, 0.3], [-0.5, 2.5, 0.2], [1.6, 2.3, 0]]), 0.18, M.plastikMat(), 30, 8); haz.ekle(hort); haz.etiketNoktasi = V(-4.0, 8.0, 0); L.push(haz);
    const dol = o3('mk-hazne-dolu'); const dK = yuvarlakKutu(2.9, 1.5, 3.5, 0.3, M.idrarMat()); dK.position.set(-4.0, 6.05, 0); dK.castShadow = false; dol.ekle(dK); dol.etiketNoktasi = V(-4.0, 8.0, 0); L.push(dol);
    // kadın modülü: yumuşak tümsek + labia + yarık (organik), yuvanın içinde
    const kadM = M.deri(); kadM.color.setHex(0xe8b89a); const kad = o3('mk-kadin').boya(kadM);
    const kadT: Top[] = [{ p: [1.8, 2.2, 0], r: 1.25, k: 8 }, ...zincir([2.2, 3.1, -0.42], [2.2, 1.3, -0.38], 0.4, 10, 10), ...zincir([2.2, 3.1, 0.42], [2.2, 1.3, 0.38], 0.4, 10, 10), ...zincir([2.6, 2.8, 0], [2.6, 1.6, 0], 0.24, 8, 16).map((t) => ({ ...t, oy: true }))];
    kad.ekle(organik(kadT, kadM, [2.0, 2.2, 0], 2.4, 80)); kad.etiketNoktasi = V(2.0, 3.9, 0); L.push(kad);
    // erkek modülü: gövde + glans (organik), yuvadan öne çıkar
    const erM = M.deri(); erM.color.setHex(0xe8b89a); const er = o3('mk-erkek').boya(erM);
    const erT: Top[] = [...zincir([1.7, 2.2, 0], [4.6, 2.4, 0], 0.7, 14, 7, 0.68), { p: [5.2, 2.45, 0], r: 0.82, k: 10 }, { p: [5.95, 2.5, 0.1], r: 0.14, k: 24, oy: true }];
    er.ekle(organik(erT, erM, [3.8, 2.3, 0], 3.2, 80)); er.etiketNoktasi = V(4.2, 3.7, 0); L.push(er);
    // mavi eldivenli eller: sol el modülü tutar, sağ el sarı kateteri meatusa yönlendirir (fotoğraf 1)
    const elM = M.eldiven(); elM.color.setHex(0x3d8fd6); elM.roughness = 0.42;
    // sol el üstten modülü tutar (parmaklar aşağı, avuç -Y'ye bakar); sağ el sağ-önden kateteri meatusa yönlendirir
    const sol = elOrganik(elM, 0.6, 1, 88); sol.scale.setScalar(0.95); sol.rotation.set(derece(100), derece(0), derece(180)); sol.position.set(2.4, 4.3, -0.7); zemin.ekle(sol);
    const sag = elOrganik(elM, 0.85, -1, 88); sag.scale.setScalar(0.95); sag.rotation.set(derece(-20), derece(-125), derece(0)); sag.position.set(7.6, 2.0, 2.6); zemin.ekle(sag);
    const katM = M.lateks(); katM.color.setHex(0xf0b43a); const kat = kateter(egri([[10.2, 1.3, 4.4], [7.9, 2.0, 2.6], [7.0, 2.4, 1.1], [6.1, 2.5, 0.1]]), 0.17, katM, 40); zemin.ekle(kat);
    return L;
  },
};

// ———————————————————————————————————————— Mahremiyet ve hasta pozisyonu (üstten, Pixar yüzlü figürler)
const Pozisyon: Sahne3BTanim = {
  ad: 'Mahremiyet ve hasta pozisyonu (üstten)',
  gizli: ['p-paravan', 'p-yardimci', 'p-v'],
  etiket: { 'p-hekim': 'Hekim: tanıt, anlat, onam al', 'p-paravan': 'Paravan / perde', 'p-yardimci': 'Yardımcı personel', 'p-erkek': 'Erkek: supin', 'p-kadin': 'Kadın: modifiye litotomi' },
  kamera: { poz: [4, 20, 20], hedef: [1.0, 1.0, -0.5] },
  zeminY: 0,
  kur: () => {
    const L: Oge3[] = [];
    const zemin = o3('_zemin'); const yer = yuvarlakKutu(32, 24, 0.2, 0.6, (() => { const m = M.tepsi(); m.color.setHex(0xc9d3dc); m.metalness = 0.1; return m; })()); yer.rotation.x = -Math.PI / 2; yer.position.y = -0.1; yer.receiveShadow = true; zemin.ekle(yer);
    const yatak = (z: number) => { const g = new THREE.Group(); const sase = yuvarlakKutu(11, 1.2, 4.2, 0.3, M.plastikMat()); sase.position.set(0, 0.6, z); g.add(sase); const dosek = yuvarlakKutu(10.6, 0.7, 3.9, 0.3, M.yatak()); dosek.position.set(0, 1.5, z); g.add(dosek); const yastik = yuvarlakKutu(1.6, 0.5, 2.6, 0.25, M.beyaz()); yastik.position.set(-4.5, 2.05, z); g.add(yastik); for (const [x, zz] of [[-5, -1.8], [5, -1.8], [-5, 1.8], [5, 1.8]] as const) { const bacak = silindir(0.12, 0.12, 1.0, M.metal()); bacak.position.set(x, 0.0, z + zz); g.add(bacak); } return g; };
    zemin.ekle(yatak(-4.4), yatak(4.4)); L.push(zemin);
    // yatan figür: ayakta kurulan insan -X ekseni etrafında 90° yatırılır (yüz yukarı), baş yastıkta (-X)
    const yatir = (g: THREE.Group, z: number) => { g.rotation.set(-Math.PI / 2, 0, -Math.PI / 2); g.position.set(-4.6, 1.95, z); g.scale.setScalar(1.15); return g; };
    const erk = o3('p-erkek'); erk.ekle(yatir(insanOrganik({ giysi: M.onluk() }), -4.4)); erk.etiketNoktasi = V(0.5, 3.4, -4.4); L.push(erk);
    const kad = o3('p-kadin'); kad.ekle(yatir(insanOrganik({ giysi: M.onluk(), kalca: derece(75), diz: derece(100) }), 4.4)); kad.etiketNoktasi = V(0.5, 3.4, 4.4); L.push(kad);
    const v = o3('p-v'); const vM = M.mavi(); vM.transparent = true; vM.opacity = 0.35; vM.depthWrite = false; v.boya(vM);
    const vS = new THREE.Shape(); vS.moveTo(0, 0); vS.lineTo(3.6, -2.4); vS.lineTo(3.6, 2.4); vS.closePath(); const vK = mesh(new THREE.ShapeGeometry(vS), vM); vK.rotation.x = -Math.PI / 2; vK.position.set(0.6, 2.0, 4.4); vK.castShadow = false; v.ekle(vK); L.push(v);
    const hek = o3('p-hekim'); const hG = insanOrganik({ giysi: M.beyaz(), kolAcik: derece(22) }); hG.position.set(-8.8, 0, 0.0); hG.rotation.y = derece(90); hG.scale.setScalar(1.15); hek.ekle(hG); hek.etiketNoktasi = V(-8.8, 6.2, 0); L.push(hek);
    const par = o3('p-paravan'); const pM = M.plastikMat(); par.boya(pM);
    for (let i = 0; i < 4; i++) { const pan = yuvarlakKutu(0.15, 6.2, 3.6, 0.1, M.ortuAcik()); pan.position.set(8.6 + (i % 2) * 0.6, 3.1, -6.2 + i * 3.9); pan.rotation.y = (i % 2 ? -1 : 1) * derece(14); par.ekle(pan); }
    par.etiketNoktasi = V(8.8, 6.6, 0); L.push(par);
    const yar = o3('p-yardimci'); const yG = insanOrganik({ giysi: M.onluk() }); yG.position.set(3.0, 0, 9.0); yG.rotation.y = derece(180); yG.scale.setScalar(1.1); yar.ekle(yG); yar.etiketNoktasi = V(3.0, 6.0, 9.0); L.push(yar);
    return L;
  },
};

export const SAHNELER3B_ORGANIK: Record<string, Sahne3BTanim> = {
  kadin: Kadin, 'yakin-kadin': YakinKadin, 'yakin-erkek-jel': YakinErkekJel, 'yakin-el': YakinEl, maket: Maket, pozisyon: Pozisyon,
};
void halka;
