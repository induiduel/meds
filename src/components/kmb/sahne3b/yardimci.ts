/**
 * KMB 3B sahne motoru — ortak yardımcılar (three.js). Pixar tarzı yumuşak, stüdyo ışıklı, yuvarlak hatlı gerçekçilik:
 * fiziksel malzemeler (lateks sarısı yarı mat + vernik, silikon beyazı, doku/mukoza ipeğimsi parlaklık, idrar camsı geçirgen),
 * oda ortam ışığı (PMREM), üç nokta ışık + yumuşak gölge, ACES ton eşleme.
 * Her sahne ögesi (`Oge3`) SVG sahnelerle AYNI kimliği taşır (SAHNE_OGELERI) → aynı eylemler (vurgula / çiz / renk /
 * göster / gizle / etiket), aynı doğrulayıcı, aynı veri. Çizilebilir ögeler (`ciz`) tüp/akış boyunca aşama aşama belirir.
 */
import * as THREE from 'three';

export type Tik = (t: number, dt: number) => void;

/** Sahne ögesi: grup + isteğe bağlı çizim ilerlemesi + çerçeve kancası */
export class Oge3 {
  grup = new THREE.Group();
  /** çizim/akış ilerlemesi 0–1 uygulayıcısı (`ciz` eylemi) */
  cizici?: (f: number) => void;
  tik?: Tik;
  /** etiketin bağlandığı nokta (yerel; yoksa kutu üstü) */
  etiketNoktasi?: THREE.Vector3;
  /** renk eylemi uygulanacak malzemeler (`.boya` karşılığı) */
  boyalar: THREE.MeshPhysicalMaterial[] = [];
  /** varsayılan görünürlük (sahne `gizli` listesi) */
  gizli = false;
  constructor(public id: string) { this.grup.name = id; }
  ekle(...o: THREE.Object3D[]) { this.grup.add(...o); return this; }
  boya(...m: THREE.MeshPhysicalMaterial[]) { this.boyalar.push(...m); return this; }
}

// ——————————————————————————————————————————— malzemeler
type P = Partial<THREE.MeshPhysicalMaterialParameters>;
export const fiz = (color: number | string, o: P = {}) =>
  new THREE.MeshPhysicalMaterial({ color, roughness: 0.5, metalness: 0, ...o });
/** Her çağrı yeni örnek döner (renk eylemi bir ögeyi boyarken diğerleri etkilenmesin) */
export const M = {
  lateks: () => fiz(0xe9bf4e, { roughness: 0.42, clearcoat: 0.35, clearcoatRoughness: 0.35, sheen: 0.4, sheenColor: new THREE.Color(0xfff1b0) }),
  lateksKoyu: () => fiz(0xc99a2c, { roughness: 0.5 }),
  silikon: () => fiz(0xf3f5f7, { roughness: 0.3, clearcoat: 0.6, clearcoatRoughness: 0.25, transmission: 0.08, thickness: 0.3 }),
  plastik: () => fiz(0xe9f1f8, { roughness: 0.15, transmission: 0.55, thickness: 0.6, ior: 1.45, clearcoat: 0.8 }),
  plastikMat: () => fiz(0xd9e1ea, { roughness: 0.35 }),
  mavi: () => fiz(0x2f6fd6, { roughness: 0.4 }),
  turuncu: () => fiz(0xef7d22, { roughness: 0.45 }),
  metal: () => fiz(0xb9c2cc, { roughness: 0.25, metalness: 0.9 }),
  deri: () => fiz(0xf0c4a2, { roughness: 0.62, sheen: 0.5, sheenColor: new THREE.Color(0xffd9c0), sheenRoughness: 0.6 }),
  deriKesit: () => fiz(0xe9b08c, { roughness: 0.7 }),
  yag: () => fiz(0xf3dc8a, { roughness: 0.75 }),
  kas: () => fiz(0xc25b52, { roughness: 0.6, sheen: 0.35, sheenColor: new THREE.Color(0xff9a90) }),
  kemik: () => fiz(0xf1e9d4, { roughness: 0.55 }),
  mesane: () => fiz(0xe59a92, { roughness: 0.48, sheen: 0.6, sheenColor: new THREE.Color(0xffc9c0), clearcoat: 0.15, clearcoatRoughness: 0.5 }),
  mukoza: () => fiz(0xe88f88, { roughness: 0.38, sheen: 0.8, sheenColor: new THREE.Color(0xffd0c8), clearcoat: 0.3, clearcoatRoughness: 0.3 }),
  prostat: () => fiz(0xcf8b72, { roughness: 0.55, sheen: 0.4 }),
  korpus: () => fiz(0xd98688, { roughness: 0.5, sheen: 0.5, sheenColor: new THREE.Color(0xffb8b8) }),
  spongiosum: () => fiz(0xe3a3a0, { roughness: 0.5, sheen: 0.5 }),
  glans: () => fiz(0xd98580, { roughness: 0.4, sheen: 0.7, sheenColor: new THREE.Color(0xffc0b8), clearcoat: 0.3 }),
  testis: () => fiz(0xe8cfc8, { roughness: 0.55 }),
  idrar: () => fiz(0xf2cf55, { roughness: 0.08, transmission: 0.85, thickness: 1.2, ior: 1.33, attenuationColor: new THREE.Color(0xe0b020), attenuationDistance: 3 }),
  idrarMat: () => fiz(0xf2cf55, { roughness: 0.2, transparent: true, opacity: 0.85 }),
  jel: () => fiz(0x8fc7ff, { roughness: 0.1, transmission: 0.7, thickness: 0.5, ior: 1.4, transparent: true, opacity: 0.85 }),
  izotonik: () => fiz(0xcfe6ff, { roughness: 0.05, transmission: 0.92, thickness: 0.8, ior: 1.33 }),
  kan: () => fiz(0xb3161c, { roughness: 0.25, clearcoat: 0.6 }),
  eldiven: () => fiz(0x9fbfe3, { roughness: 0.45, sheen: 0.3 }),
  eldivenSteril: () => fiz(0xeedcb9, { roughness: 0.55 }),
  ortu: () => fiz(0x3b7bb8, { roughness: 0.85 }),
  ortuAcik: () => fiz(0x8fb6dd, { roughness: 0.9 }),
  povidon: () => fiz(0x8a3c12, { roughness: 0.3, clearcoat: 0.5 }),
  koyu: () => fiz(0x2e3540, { roughness: 0.6 }),
  beyaz: () => fiz(0xffffff, { roughness: 0.6 }),
  yesil: () => fiz(0x2e9e5b, { roughness: 0.45 }),
  kirmizi: () => fiz(0xd23b3b, { roughness: 0.45 }),
  tepsi: () => fiz(0xaab4bf, { roughness: 0.28, metalness: 0.75 }),
  yatak: () => fiz(0xf1f4f7, { roughness: 0.9 }),
  onluk: () => fiz(0x8fc1c9, { roughness: 0.8 }),
};
export const RENK: Record<string, number> = { yesil: 0x2e9e5b, kirmizi: 0xd23b3b, mavi: 0x3a7bd5, sari: 0xe1a92e };

// ——————————————————————————————————————————— geometri yardımcıları
export const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
export const egri = (p: [number, number, number][], kapali = false) => new THREE.CatmullRomCurve3(p.map(([x, y, z]) => V(x, y, z)), kapali, 'centripetal');

export const mesh = (g: THREE.BufferGeometry, m: THREE.Material, golge = true) => { const o = new THREE.Mesh(g, m); o.castShadow = golge; o.receiveShadow = golge; return o; };
export const kure = (r: number, m: THREE.Material, w = 32) => mesh(new THREE.SphereGeometry(r, w, Math.max(8, w / 2)), m);
export const kapsul = (r: number, boy: number, m: THREE.Material) => mesh(new THREE.CapsuleGeometry(r, boy, 8, 24), m);
export const silindir = (r1: number, r2: number, h: number, m: THREE.Material, w = 32) => mesh(new THREE.CylinderGeometry(r1, r2, h, w), m);
export const kutu = (x: number, y: number, z: number, m: THREE.Material) => mesh(new THREE.BoxGeometry(x, y, z), m);
export const halka = (r: number, t: number, m: THREE.Material, w = 48) => mesh(new THREE.TorusGeometry(r, t, 16, w), m);
export const yuvarlakKutu = (x: number, y: number, z: number, r: number, m: THREE.Material) => {
  // köşeleri yuvarlatılmış kutu: ekstrüde edilmiş yuvarlak dikdörtgen
  const s = new THREE.Shape();
  const w = x / 2, h = y / 2;
  s.moveTo(-w + r, -h); s.lineTo(w - r, -h); s.quadraticCurveTo(w, -h, w, -h + r); s.lineTo(w, h - r); s.quadraticCurveTo(w, h, w - r, h);
  s.lineTo(-w + r, h); s.quadraticCurveTo(-w, h, -w, h - r); s.lineTo(-w, -h + r); s.quadraticCurveTo(-w, -h, -w + r, -h);
  const g = new THREE.ExtrudeGeometry(s, { depth: z, bevelEnabled: true, bevelThickness: Math.min(r, z / 4), bevelSize: Math.min(r, z / 4) * 0.8, bevelSegments: 4, curveSegments: 12 });
  g.translate(0, 0, -z / 2);
  return mesh(g, m);
};
/** Torna (lathe): profil [yarıçap, yükseklik] noktaları → dönel cisim (mesane, prostat, glans, şişe) */
export const torna = (profil: [number, number][], m: THREE.Material, w = 48) => mesh(new THREE.LatheGeometry(profil.map(([r, y]) => new THREE.Vector2(r, y)), w), m);
/** Yumuşatılmış torna: kaba profil noktaları Catmull-Rom ile 32 noktaya açılır (faset halkaları görünmesin) */
export const tornaYumusak = (profil: [number, number][], m: THREE.Material, w = 56, n = 32) => {
  const c = new THREE.CatmullRomCurve3(profil.map(([r, y]) => V(r, y, 0)), false, 'catmullrom', 0.5);
  const pts = c.getPoints(n).map((p) => new THREE.Vector2(Math.max(0, p.x), p.y));
  return mesh(new THREE.LatheGeometry(pts, w), m);
};
/** Elips benzeri yumuşak gövde: küreyi ölçekler */
export const yumru = (rx: number, ry: number, rz: number, m: THREE.Material, w = 40) => { const k = kure(1, m, w); k.scale.set(rx, ry, rz); return k; };

/** Eğri boyunca tüp; `ilerle(f)` tüpün yalnız ilk f kısmını çizer (çizim eylemi) */
export function tup(c: THREE.Curve<THREE.Vector3>, r: number, m: THREE.Material, seg = 96, radyal = 16, kapali = false) {
  const g = new THREE.TubeGeometry(c, seg, r, radyal, kapali);
  const o = mesh(g, m);
  const toplam = g.index ? g.index.count : g.attributes.position.count;
  const ilerle = (f: number) => { g.setDrawRange(0, Math.max(0, Math.min(toplam, Math.round(toplam * f)))); };
  return Object.assign(o, { ilerle, egri: c });
}
/** Kateter: tüp + yuvarlak uç (uç noktada küre) + yan gözler; `ilerle` ile uç ilerler (uç küre de eğri boyunca kayar) */
export function kateter(c: THREE.Curve<THREE.Vector3>, r: number, m: THREE.Material, seg = 120) {
  const g = new THREE.Group();
  const govde = tup(c, r, m, seg, 18);
  const uc = kure(r * 1.02, m, 20);
  const goz = mesh(new THREE.SphereGeometry(r * 0.42, 12, 8), M.koyu(), false);
  const goz2 = goz.clone();
  const son = c.getPoint(1);
  const yerlestir = (f: number) => {
    const p = c.getPoint(f);
    const t = c.getTangent(Math.min(1, f)).normalize();
    uc.position.copy(p).addScaledVector(t, r * 0.05);
    // gözler: ucun 1,5 r ve 3 r gerisinde, karşılıklı yanlarda
    const n = new THREE.Vector3(0, 1, 0).cross(t).normalize();
    if (n.lengthSq() < 0.01) n.set(1, 0, 0);
    goz.position.copy(c.getPoint(Math.max(0, f - 0.03))).addScaledVector(n, r * 0.92);
    goz2.position.copy(c.getPoint(Math.max(0, f - 0.06))).addScaledVector(n, -r * 0.92);
  };
  yerlestir(1);
  g.add(govde, uc, goz, goz2);
  const ilerle = (f: number) => { govde.ilerle(f); yerlestir(Math.max(0.001, f)); };
  void son;
  return Object.assign(g, { ilerle, govde, uc });
}
/** Eğri boyunca akan parçacıklar (idrar damlaları, jel); `ilerle(f)` akışın ne kadarının dolduğunu, `tik` kaymayı verir */
export function akis(c: THREE.Curve<THREE.Vector3>, adet: number, r: number, m: THREE.Material) {
  const g = new THREE.Group();
  const ps = Array.from({ length: adet }, () => { const s = kure(r, m, 10); s.castShadow = false; g.add(s); return s; });
  let f = 1;
  const yerlestir = (t: number) => {
    if (!Number.isFinite(t)) t = 0;
    ps.forEach((s, i) => {
      const u = ((i / adet) + t * 0.18) % 1;
      s.visible = u <= f;
      s.position.copy(c.getPoint(u));
      const sc = 0.7 + 0.3 * Math.sin(u * Math.PI);
      s.scale.setScalar(sc);
    });
  };
  yerlestir(0);
  return Object.assign(g, { ilerle: (x: number) => { f = x; }, tik: ((t: number) => yerlestir(t)) as Tik });
}
/** Ok: gövde silindir + koni (yön ve hareket gösterimi) */
export function ok(bas: THREE.Vector3, son: THREE.Vector3, r: number, m: THREE.Material) {
  const g = new THREE.Group();
  const d = son.clone().sub(bas); const L = d.length(); const yon = d.clone().normalize();
  const gov = silindir(r, r, Math.max(0.01, L - r * 4), m, 12); gov.position.y = (L - r * 4) / 2; g.add(gov);
  const uc = mesh(new THREE.ConeGeometry(r * 2.2, r * 4, 16), m); uc.position.y = L - r * 2; g.add(uc);
  g.position.copy(bas); g.quaternion.setFromUnitVectors(V(0, 1, 0), yon);
  const ilerle = (f: number) => { g.scale.set(1, Math.max(0.001, f), 1); };
  return Object.assign(g, { ilerle });
}
/** Düz yüzeye yazı (küçük yazı etiketleri: "16 Fr", "mL") — tuvale çizilir */
export function yazi(metin: string, px = 64, renk = '#3e4a58', zemin?: string) {
  const c = document.createElement('canvas'); c.width = 512; c.height = 128;
  const x = c.getContext('2d')!;
  if (zemin) { x.fillStyle = zemin; x.fillRect(0, 0, 512, 128); }
  x.fillStyle = renk; x.font = `600 ${px}px system-ui, sans-serif`; x.textAlign = 'center'; x.textBaseline = 'middle';
  x.fillText(metin, 256, 64);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  const m = new THREE.MeshBasicMaterial({ map: t, transparent: !zemin, depthWrite: false });
  const p = new THREE.Mesh(new THREE.PlaneGeometry(4, 1), m);
  return p;
}
/** Hafif pürüz dokusu (mukoza/deri için bump) — tuvalde gürültü */
export function puruz(tohum = 7, boy = 256, guc = 0.5) {
  const c = document.createElement('canvas'); c.width = c.height = boy;
  const x = c.getContext('2d')!; const img = x.createImageData(boy, boy);
  let s = tohum;
  const r = () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  for (let i = 0; i < img.data.length; i += 4) { const v = 128 + (r() - 0.5) * 255 * guc; img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255; }
  x.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(3, 3);
  return t;
}
/** Gradyan arka plan dokusu (stüdyo fonu) */
export function fon(ust: string, alt: string) {
  const c = document.createElement('canvas'); c.width = 4; c.height = 256;
  const x = c.getContext('2d')!; const g = x.createLinearGradient(0, 0, 0, 256); g.addColorStop(0, ust); g.addColorStop(1, alt);
  x.fillStyle = g; x.fillRect(0, 0, 4, 256);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
export const derece = (d: number) => (d * Math.PI) / 180;
export const yumusak = (f: number) => (f <= 0 ? 0 : f >= 1 ? 1 : f * f * (3 - 2 * f));

// ——————————————————————————————————————————— organik yüzeyler (marching cubes): parçalar tek, kaynaşmış yüzey olur
import { MarchingCubes } from 'three/examples/jsm/objects/MarchingCubes.js';
export type Top = { p: [number, number, number]; r: number; /** negatif: oyar (açıklık, oluk) */ oy?: boolean; /** keskinlik: büyük = daha az kaynaşma (varsayılan 12) */ k?: number };
/**
 * Topların (ve oyucuların) birleşiminden pürüzsüz organik gövde. `merkez` + `yari` (küp yarı kenarı) dünya kutusunu
 * verir; toplar bu kutunun içinde kalmalı. Çözünürlük 64–112 (bir kez hesaplanır, statik).
 */
export function organik(toplar: Top[], m: THREE.Material, merkez: [number, number, number], yari: number, coz = 88) {
  const mc = new MarchingCubes(coz, m, false, false, 400000);
  mc.isolation = 1;
  const n = (v: number, c: number) => (v - (c - yari)) / (2 * yari);
  for (const t of toplar) {
    const k = t.k ?? 12;
    const rn = t.r / (2 * yari);
    const guc = rn * rn * (k + mc.isolation);
    mc.addBall(n(t.p[0], merkez[0]), n(t.p[1], merkez[1]), n(t.p[2], merkez[2]), t.oy ? -guc : guc, k);
  }
  mc.update();
  mc.position.set(...merkez); mc.scale.setScalar(yari);
  mc.castShadow = true; mc.receiveShadow = true;
  // sarmalayıcı grup: çağıran taraf konum/ölçek verdiğinde MC'nin iç ölçeği (yari) ezilmesin (H464)
  const g = new THREE.Group(); g.add(mc);
  return g;
}
/** Zincir: iki nokta arasında eşit aralıklı toplar (parmak, labium, kol gibi uzun yumuşak parçalar) */
export function zincir(a: [number, number, number], b: [number, number, number], r: number, adet = 6, k = 6, rSon = r): Top[] {
  // pürüzsüz tüp: top aralığı ≤ 0,4·r olacak kadar sıklaştırılır (boncuk görünümü olmasın)
  const L = Math.hypot(b[0] - a[0], b[1] - a[1], b[2] - a[2]); adet = Math.max(adet, Math.ceil(L / (Math.min(r, rSon) * 0.4)) + 1);
  return Array.from({ length: adet }, (_, i) => { const u = adet === 1 ? 0 : i / (adet - 1); return { p: [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u] as [number, number, number], r: r + (rSon - r) * u, k }; });
}
/** Islak film: yüzeye yakın ince, parlak, yarı saydam katman (antiseptik ya da jel ile nemlenmiş alan) */
export const islakM = (renk: number, saydamlik = 0.55) => fiz(renk, { transparent: true, opacity: saydamlik, roughness: 0.06, clearcoat: 1, clearcoatRoughness: 0.08, depthWrite: false, side: THREE.DoubleSide });
