import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

/**
 * Hücrem · 3B evrim sahnesi. 28 basamağın her biri kendi renkli ve biçimli gövdesiyle çizilir (basamak n = o anki hücre):
 * Kimyasal köken (1–3) amber kesecik · Prokaryot (4–9) camgöbeği, arke kırmızı · Ökaryot (10–17) mavi, kloroplastlı yeşil ·
 * Çok hücreli (18–28) koloni → hekim hücresi (altın). Organeller basamağa göre eklenir; kamçı/sil/psödopod/akson sinyali/
 * kalp atımı hareketlidir. Glukoz parçacıkları hücreye akar (sayı = bakiye); glukoz < 20 ya da canlılık düşükse hücre solar.
 * Yalnız ekranda görünürken çizilir; "hareketi azalt" açıksa tek kare. Yalnız Hücrem sayfası yükler (React.lazy);
 * WebGL yoksa `onHata` ile SVG çizime dönülür.
 */
interface Props { n: number; glukoz: number; canlilik: number; onHata?: () => void }

type Tik = (t: number, e: number) => void;
type Parca = THREE.Group & { userData: { tiks?: Tik[] } };

const RENK = { amber: 0xf59e0b, cam: 0x06b6d4, kirmizi: 0xef4444, mavi: 0x3b82f6, yesil: 0x22c55e, altin: 0xfacc15, gul: 0xf472b6, kas: 0xdc2626, mor: 0x8b5cf6, kok: 0x2dd4bf, dut: 0xfb7185, kalp: 0xe11d48 };

const mat = (color: number, o: Partial<THREE.MeshStandardMaterialParameters> = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.35, metalness: 0.05, ...o });
const kure = (r: number, m: THREE.Material, w = 24) => new THREE.Mesh(new THREE.SphereGeometry(r, w, w), m);
const kap = (): Parca => { const g = new THREE.Group() as Parca; g.userData.tiks = []; return g; };
/** Çocuğu ekler, hareketini üst parçaya katar */
const ekle = (g: Parca, c: THREE.Object3D, tik?: Tik) => { g.add(c); if (tik) g.userData.tiks!.push(tik); if ((c as Parca).userData?.tiks) g.userData.tiks!.push(...(c as Parca).userData.tiks!); return c; };
const rastgele = (tohum: number) => () => { tohum = (tohum * 16807) % 2147483647; return (tohum - 1) / 2147483646; };
const ickure = (rnd: () => number, r0: number, r1: number) => {
  const u = rnd() * 2 - 1, th = rnd() * Math.PI * 2, r = r0 + (r1 - r0) * Math.cbrt(rnd()), s = Math.sqrt(1 - u * u);
  return new THREE.Vector3(r * s * Math.cos(th), r * u, r * s * Math.sin(th));
};
const yuzey = (rnd: () => number) => ickure(rnd, 1, 1);
const helis = (r: number, boy: number, tur: number, faz = 0, n = 80) =>
  new THREE.CatmullRomCurve3(Array.from({ length: n }, (_, i) => { const a = (i / (n - 1)) * Math.PI * 2 * tur + faz; return new THREE.Vector3(Math.cos(a) * r, (i / (n - 1) - 0.5) * boy, Math.sin(a) * r); }));
const tup = (c: THREE.Curve<THREE.Vector3>, yar: number, m: THREE.Material, seg = 80) => new THREE.Mesh(new THREE.TubeGeometry(c, seg, yar, 8, false), m);
const parla = (r: number, rengi: number, hl = 0.35) => { const s = kure(r * 0.13, new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.75 }), 10); s.position.set(-r * 0.42, r * 0.46, r * 0.6); void hl; return s; };

/** Dolu, gölgeli gövde: yarı saydam iç + koyu kenar (zarın kenarı) + parlama noktası */
function govdeKure(r: number, renk: number, sekil: [number, number, number] = [1, 1, 1]): Parca {
  const g = kap();
  const ic = kure(r, mat(renk, { transparent: true, opacity: 0.62, roughness: 0.25, depthWrite: false }), 40);
  const kenar = kure(r * 1.02, mat(renk, { transparent: true, opacity: 0.55, side: THREE.BackSide, emissive: renk, emissiveIntensity: 0.18, depthWrite: false }), 40);
  const grubu = new THREE.Group(); grubu.add(ic, kenar, parla(r, renk)); grubu.scale.set(...sekil); g.add(grubu);
  g.userData.tiks!.push((t, e) => { grubu.scale.set(sekil[0] * (1 + Math.sin(t * 1.5) * 0.012 * e), sekil[1] * (1 + Math.sin(t * 1.5) * 0.012 * e), sekil[2]); });
  return g;
}
function govdeBasil(boy: number, yar: number, renk: number): Parca {
  const g = kap(); const m = new THREE.Mesh(new THREE.CapsuleGeometry(yar, boy, 10, 24), mat(renk, { transparent: true, opacity: 0.66, roughness: 0.25, depthWrite: false }));
  m.rotation.z = Math.PI / 2; g.add(m);
  const kenar = new THREE.Mesh(new THREE.CapsuleGeometry(yar * 1.05, boy, 10, 24), mat(renk, { transparent: true, opacity: 0.5, side: THREE.BackSide, emissive: renk, emissiveIntensity: 0.2, depthWrite: false })); kenar.rotation.z = Math.PI / 2; g.add(kenar);
  const p = parla(yar, renk); p.position.set(-boy * 0.15, yar * 0.55, yar * 0.7); g.add(p);
  return g;
}

// ───── Organeller ─────
function halkaDna(r = 0.28, renk = 0xfde047): Parca {
  const g = kap(); const t = new THREE.Mesh(new THREE.TorusGeometry(r, 0.022, 8, 40), mat(renk, { emissive: 0xca8a04, emissiveIntensity: 0.4 })); g.add(t);
  g.userData.tiks!.push((tm, e) => { t.rotation.x = tm * 0.6 * e; t.rotation.y = tm * 0.4 * e; });
  return g;
}
function cift(): Parca {
  const g = kap();
  const m1 = mat(0xef4444, { emissive: 0x7f1d1d, emissiveIntensity: 0.25 }), m2 = mat(0x3b82f6, { emissive: 0x1e3a8a, emissiveIntensity: 0.25 });
  g.add(tup(helis(0.22, 1.1, 2.5), 0.035, m1), tup(helis(0.22, 1.1, 2.5, Math.PI), 0.035, m2));
  const bm = mat(0xfacc15);
  for (let i = 0; i < 14; i++) { const a = (i / 13) * Math.PI * 2 * 2.5, c = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.44, 6), bm); c.position.y = (i / 13 - 0.5) * 1.1; c.rotation.z = Math.PI / 2; c.rotation.y = -a; g.add(c); }
  g.userData.tiks!.push((t, e) => { g.rotation.y = t * 0.9 * e; });
  return g;
}
function rnaSerit(): Parca {
  const g = kap(); const c = new THREE.CatmullRomCurve3(Array.from({ length: 40 }, (_, i) => new THREE.Vector3((i / 39 - 0.5) * 0.7, Math.sin(i * 0.7) * 0.1, Math.cos(i * 0.5) * 0.09)));
  g.add(tup(c, 0.025, mat(0xef4444, { emissive: 0x7f1d1d, emissiveIntensity: 0.35 }), 60));
  g.userData.tiks!.push((t, e) => { g.rotation.y = t * 0.7 * e; g.rotation.z = Math.sin(t) * 0.15 * e; });
  return g;
}
function ribozimler(rnd: () => number, adet: number, r1: number): Parca {
  const g = kap(); const m = mat(0x7c3aed, { emissive: 0x4c1d95, emissiveIntensity: 0.3 });
  const ps = Array.from({ length: adet }, () => { const s = kure(0.06, m, 10); s.position.copy(ickure(rnd, 0.1, r1)); g.add(s); return s; });
  g.userData.tiks!.push((t, e) => { ps.forEach((s, i) => { s.position.y += Math.sin(t * 2 + i) * 0.0014 * e; }); });
  return g;
}
function mitokondri(adet = 3, yaricap = 0.6): Parca {
  const g = kap(); const dis = mat(0xfb923c, { transparent: true, opacity: 0.88, emissive: 0x9a3412, emissiveIntensity: 0.35 }), ic = mat(0x9a3412, { transparent: true, opacity: 0.85 });
  const ms = Array.from({ length: adet }, (_, i) => {
    const m = kap(); m.add(new THREE.Mesh(new THREE.CapsuleGeometry(0.075, 0.2, 6, 12), dis));
    for (let j = -2; j <= 2; j++) { const r = new THREE.Mesh(new THREE.TorusGeometry(0.052, 0.008, 6, 12), ic); r.position.y = j * 0.055; r.rotation.x = Math.PI / 2; r.scale.set(j % 2 ? 1 : 0.8, j % 2 ? 0.7 : 1, 1); m.add(r); }
    g.add(m); return { m, f: i * 2.4 };
  });
  g.userData.tiks!.push((t, e) => ms.forEach(({ m, f }) => { const a = t * 0.3 * e + f; m.position.set(Math.cos(a) * yaricap, Math.sin(a * 0.8 + f) * yaricap * 0.5, Math.sin(a) * yaricap * 0.9); m.rotation.z = a; m.scale.setScalar(1 + Math.sin(t * 3 + f) * 0.07 * e); }));
  return g;
}
function er(): Parca {
  const g = kap(); const m = mat(0x38bdf8, { transparent: true, opacity: 0.8 });
  for (let i = 0; i < 2; i++) { const k = new THREE.Mesh(new THREE.TorusKnotGeometry(0.5 + i * 0.12, 0.03, 120, 8, 2, 3 + i), m); k.scale.set(1, 0.7, 1); g.add(k); }
  g.userData.tiks!.push((t, e) => { g.rotation.y = t * 0.15 * e; g.rotation.x = Math.sin(t * 0.3) * 0.1; });
  return g;
}
function golgi(): Parca {
  const g = kap(); const m = mat(0xf59e0b, { transparent: true, opacity: 0.92 }); const vez = mat(0xfcd34d, { emissive: 0xb45309, emissiveIntensity: 0.4 });
  for (let i = 0; i < 4; i++) { const t = new THREE.Mesh(new THREE.TorusGeometry(0.2 - i * 0.015, 0.028, 8, 28, Math.PI * 1.35), m); t.rotation.x = Math.PI / 2; t.position.y = i * 0.075 - 0.11; g.add(t); }
  const vs = Array.from({ length: 5 }, (_, i) => { const s = kure(0.03, vez, 8); g.add(s); return { s, f: i * 1.3 }; });
  g.userData.tiks!.push((t, e) => vs.forEach(({ s, f }) => { const k = ((t * 0.3 * e + f) % 1 + 1) % 1; s.position.set(0.2 + k * 0.55, 0.12 - k * 0.1, Math.sin(f + k * 5) * 0.12); s.scale.setScalar(1 - k * 0.3); }));
  return g;
}
function iskelet(rnd: () => number, renk = 0x94a3b8): Parca {
  const g = kap(); const p: number[] = [];
  for (let i = 0; i < 30; i++) { const a = ickure(rnd, 0.7, 0.95), b = ickure(rnd, 0.25, 0.95); p.push(a.x, a.y, a.z, b.x, b.y, b.z); }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(p, 3));
  g.add(new THREE.LineSegments(geo, new THREE.LineBasicMaterial({ color: renk, transparent: true, opacity: 0.45 })));
  return g;
}
function cekirdek(r = 0.38, dnaIc = true): Parca {
  const g = kap(); g.add(kure(r, mat(0xa78bfa, { transparent: true, opacity: 0.72, emissive: 0x4c1d95, emissiveIntensity: 0.3 }), 32));
  const k = kure(r * 0.3, mat(0x6d28d9)); k.position.set(r * 0.25, r * 0.15, r * 0.3); g.add(k);
  if (dnaIc) { const d = cift(); d.scale.setScalar(r); d.position.set(-r * 0.15, 0, -r * 0.2); ekle(g, d); }
  g.userData.tiks!.push((t, e) => { g.scale.setScalar(1 + Math.sin(t * 1.2) * 0.018 * e); });
  return g;
}
function kloroplast(adet = 3): Parca {
  const g = kap(); const m = mat(0x16a34a, { emissive: 0x14532d, emissiveIntensity: 0.3 }); const mi = mat(0x86efac, { emissive: 0x15803d, emissiveIntensity: 0.3 });
  const ks = Array.from({ length: adet }, (_, i) => { const k = kap(); const e = kure(0.14, m, 14); e.scale.set(1.5, 0.7, 1); k.add(e);
    for (let j = -1; j <= 1; j++) for (let l = 0; l < 2; l++) { const d = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.022, 10), mi); d.position.set(j * 0.065, 0.025 - l * 0.045, 0); k.add(d); }
    g.add(k); return { k, f: i * 2.1 }; });
  g.userData.tiks!.push((t, e) => ks.forEach(({ k, f }) => { const a = t * 0.25 * e + f; k.position.set(Math.cos(a) * 0.62, Math.sin(a * 1.3) * 0.25 - 0.2, Math.sin(a) * 0.5); k.rotation.y = a; }));
  return g;
}
function kamci(renk: number, kok = 1.0, boy = 12): Parca {
  const g = kap(); const m = mat(renk); const hal = Array.from({ length: boy }, (_, i) => { const s = kure(0.05 - i * 0.002, m, 8); g.add(s); return s; });
  g.userData.tiks!.push((t, e) => hal.forEach((s, i) => s.position.set(kok + i * 0.1, Math.sin(t * 5 * e - i * 0.7) * 0.02 * i, Math.cos(t * 5 * e - i * 0.7) * 0.012 * i)));
  return g;
}
function siller(renk: number, a = 1.05, b = 0.7): Parca {
  const g = kap(); const rnd = rastgele(3); const m = mat(renk);
  const ps = Array.from({ length: 34 }, () => { const v = yuzey(rnd); const piv = new THREE.Group(); const k = new THREE.Mesh(new THREE.CapsuleGeometry(0.014, 0.16, 3, 6), m); k.position.y = 0.09; piv.add(k);
    piv.position.set(v.x * a, v.y * b, v.z * b); piv.lookAt(piv.position.clone().multiplyScalar(2)); piv.rotateX(Math.PI / 2); g.add(piv); return { k, f: rnd() * 6 }; });
  g.userData.tiks!.push((t, e) => ps.forEach(({ k, f }) => { k.rotation.x = Math.sin(t * 9 * e - f) * 0.55; k.position.z = Math.sin(t * 9 * e - f + 0.5) * 0.02; }));
  return g;
}
function bakteri(boy = 0.18, renk = 0xfb923c): THREE.Mesh { const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.06, boy, 6, 12), mat(renk, { emissive: 0x9a3412, emissiveIntensity: 0.4 })); m.rotation.z = Math.PI / 2; return m; }

// ───── Basamak gövdeleri ─────
function amipGovde(): Parca {
  const g = kap(); const geo = new THREE.SphereGeometry(0.85, 48, 48); const orj = geo.attributes.position.array.slice() as Float32Array;
  const m = new THREE.Mesh(geo, mat(RENK.mavi, { transparent: true, opacity: 0.66, roughness: 0.25, depthWrite: false })); g.add(m);
  const v = new THREE.Vector3(); const pos = geo.attributes.position;
  g.userData.tiks!.push((t, e) => {
    for (let i = 0; i < pos.count; i++) {
      v.set(orj[i * 3], orj[i * 3 + 1], orj[i * 3 + 2]).normalize();
      const u1 = Math.max(0, v.dot(new THREE.Vector3(Math.cos(t * 0.7), 0.2, Math.sin(t * 0.7)).normalize()) - 0.55), u2 = Math.max(0, v.dot(new THREE.Vector3(Math.cos(t * 0.5 + 2.1), -0.3, Math.sin(t * 0.5 + 2.1)).normalize()) - 0.6), u3 = Math.max(0, v.dot(new THREE.Vector3(-0.4, Math.sin(t * 0.6), Math.cos(t * 0.8)).normalize()) - 0.6);
      const k = 0.85 * (1 + (u1 * 1.9 + u2 * 1.6 + u3 * 1.5) * (0.6 + 0.4 * Math.sin(t * 1.1 + 1)) * e);
      pos.setXYZ(i, v.x * k, v.y * k, v.z * k);
    }
    pos.needsUpdate = true; geo.computeVertexNormals();
  });
  return g;
}
function kasLifi(renk: number): Parca {
  const g = kap(); const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.34, 1.9, 10, 24), mat(renk, { transparent: true, opacity: 0.75, roughness: 0.3 })); m.rotation.z = Math.PI / 2; g.add(m);
  const r = mat(0x7f1d1d, { transparent: true, opacity: 0.7 });
  for (let i = -8; i <= 8; i++) { const t = new THREE.Mesh(new THREE.TorusGeometry(0.345, 0.012, 6, 28), r); t.position.x = i * 0.12; t.rotation.y = Math.PI / 2; g.add(t); }
  [-0.6, 0.1, 0.8].forEach((x, i) => { const c = kure(0.1, mat(0xa78bfa), 12); c.position.set(x, 0.1 - i * 0.05, 0.12); c.scale.set(1.4, 0.8, 0.8); g.add(c); });
  g.userData.tiks!.push((t, e) => { const k = (Math.sin(t * 3) * 0.5 + 0.5) * e; g.scale.set(1 - 0.14 * k, 1 + 0.12 * k, 1 + 0.12 * k); });
  return g;
}
function noronGovde(olcek = 1): Parca {
  const g = kap(); const m = mat(RENK.mor, { emissive: 0x4c1d95, emissiveIntensity: 0.35 });
  const so = kure(0.3, m, 24); so.position.set(-0.9, 0, 0); g.add(so);
  const k = kure(0.1, mat(0xc4b5fd), 12); k.position.set(-0.9, 0, 0.12); g.add(k);
  const rnd = rastgele(13);
  for (let i = 0; i < 6; i++) { const a = rnd() * Math.PI * 2, u = new THREE.Vector3(-1.3 + Math.cos(a) * 0.55, Math.sin(a) * 0.7, (rnd() - 0.5) * 0.5); g.add(tup(new THREE.CatmullRomCurve3([so.position.clone(), so.position.clone().lerp(u, 0.5).add(new THREE.Vector3(0, 0.06, 0.05)), u]), 0.02, m, 12)); }
  const aks = new THREE.CatmullRomCurve3([so.position.clone(), new THREE.Vector3(-0.3, 0.12, 0), new THREE.Vector3(0.5, -0.1, 0.1), new THREE.Vector3(1.3, 0.05, 0)]);
  g.add(tup(aks, 0.04, m, 40));
  for (let i = 0; i < 6; i++) { const p = aks.getPoint(0.2 + i * 0.13); const my = new THREE.Mesh(new THREE.CapsuleGeometry(0.06, 0.12, 4, 10), mat(0xf5f5f4, { roughness: 0.6 })); my.position.copy(p); my.rotation.z = Math.PI / 2; g.add(my); }
  const t1 = kure(0.1, m, 10); t1.position.copy(aks.getPoint(1)); g.add(t1);
  const im = kure(0.06, new THREE.MeshBasicMaterial({ color: 0xfef08a }), 8); g.add(im);
  g.userData.tiks!.push((t, e) => { const k = ((t * 0.4 * e) % 1 + 1) % 1; im.position.copy(aks.getPoint(k)); t1.scale.setScalar(1 + Math.max(0, k - 0.9) * 6); });
  g.scale.setScalar(olcek);
  return g;
}
function koloni(): Parca {
  const g = kap(); const m = mat(RENK.kok, { transparent: true, opacity: 0.7 }); const rnd = rastgele(11);
  const pos = [[0, 0, 0], ...Array.from({ length: 6 }, (_, i) => [Math.cos((i / 6) * Math.PI * 2) * 0.75, Math.sin((i / 6) * Math.PI * 2) * 0.75, (i % 2 ? 1 : -1) * 0.2])];
  const ks = pos.map(([x, y, z]) => { const c = kap(); c.add(kure(0.4, m, 24), parla(0.4, 0), kure(0.14, mat(0x0f766e), 10)); c.position.set(x, y, z); g.add(c); return { c, f: rnd() * 6 }; });
  g.userData.tiks!.push((t, e) => { g.rotation.z = t * 0.2 * e; ks.forEach(({ c, f }) => c.scale.setScalar(1 + Math.sin(t * 1.5 + f) * 0.04 * e)); });
  return g;
}
function epitel(): Parca {
  const g = kap(); const rnd = rastgele(17);
  for (let x = -2; x <= 2; x++) for (let z = -2; z <= 2; z++) {
    const h = 0.55 + rnd() * 0.08; const c = new THREE.Mesh(new THREE.BoxGeometry(0.34, h, 0.34), mat(RENK.gul, { transparent: true, opacity: 0.85 })); c.position.set(x * 0.38, 0, z * 0.38); g.add(c);
    const n = kure(0.07, mat(0x9d174d), 8); n.position.set(x * 0.38, -h * 0.1, z * 0.38); g.add(n);
  }
  const bm = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.06, 2.1), mat(0xfecdd3)); bm.position.y = -0.34; g.add(bm);
  g.rotation.x = 0.5; g.userData.tiks!.push((t, e) => { g.rotation.y = Math.sin(t * 0.4) * 0.35 * e; });
  return g;
}
function kok(): Parca {
  const g = kap(); const govde = govdeKure(0.8, RENK.kok); ekle(g, govde); const c = cekirdek(0.28, false); ekle(g, c);
  const hale = new THREE.Mesh(new THREE.TorusGeometry(1.05, 0.015, 8, 64), new THREE.MeshBasicMaterial({ color: 0x99f6e4, transparent: true, opacity: 0.6 })); hale.rotation.x = Math.PI / 2; g.add(hale);
  const kiz = govdeKure(0.5, RENK.kok); kiz.position.set(1.15, 0, 0); g.add(kiz); const kc = kure(0.14, mat(0x0f766e), 10); kc.position.copy(kiz.position); g.add(kc);
  g.userData.tiks!.push((t, e) => { hale.scale.setScalar(1 + Math.sin(t * 2) * 0.04 * e); const k = (Math.sin(t * 0.8) * 0.5 + 0.5) * e; kiz.position.x = 1.0 + k * 0.45; kiz.scale.setScalar(0.5 + k * 0.5); kc.position.x = kiz.position.x; });
  return g;
}
function kureTopu(adet: number, bosluk: boolean, renk: number, r: number): Parca {
  const g = kap(); const m = mat(renk, { transparent: true, opacity: 0.8 });
  const gold = 2.399963; // altın açı: eşit dağılım
  for (let i = 0; i < adet; i++) {
    const y = 1 - (i + 0.5) / adet * 2, rr = Math.sqrt(Math.max(0, 1 - y * y)), a = i * gold;
    const hy = bosluk ? 1 : (0.25 + 0.75 * Math.cbrt((i + 1) / adet));
    const c = kure(r, m, 14); c.position.set(Math.cos(a) * rr * hy, y * hy, Math.sin(a) * rr * hy); g.add(c);
    if (i % 3 === 0) { const n = kure(r * 0.35, mat(0x9f1239), 8); n.position.copy(c.position).multiplyScalar(0.92); g.add(n); }
  }
  if (bosluk) { const ic = kure(0.62, mat(0xfff1f2, { transparent: true, opacity: 0.15, depthWrite: false }), 20); g.add(ic); const ihk = kure(0.2, mat(0xfda4af), 12); ihk.position.set(0.5, 0.4, 0); g.add(ihk); }
  g.userData.tiks!.push((t, e) => { g.rotation.y = t * 0.3 * e; });
  return g;
}
function kalpKasi(): Parca {
  const g = kap(); const m = mat(RENK.kalp, { transparent: true, opacity: 0.85, emissive: 0x7f1d1d, emissiveIntensity: 0.25 });
  const rnd = rastgele(29); const lifler: THREE.Object3D[] = [];
  for (let i = 0; i < 7; i++) { const a = (i / 7) * Math.PI * 2; const c = new THREE.Mesh(new THREE.CapsuleGeometry(0.2, 0.55, 8, 16), m); c.position.set(Math.cos(a) * 0.55, Math.sin(a) * 0.55, (rnd() - 0.5) * 0.3); c.rotation.z = a + Math.PI / 2 + 0.3 * (rnd() - 0.5); g.add(c); lifler.push(c); }
  const c0 = new THREE.Mesh(new THREE.CapsuleGeometry(0.22, 0.4, 8, 16), m); g.add(c0);
  const disk = mat(0xfecaca, { emissive: 0xfca5a5, emissiveIntensity: 0.6 });
  for (let i = 0; i < 7; i++) { const a = (i / 7) * Math.PI * 2 + 0.3; const d = kure(0.05, disk, 8); d.position.set(Math.cos(a) * 0.28, Math.sin(a) * 0.28, 0.1); g.add(d); }
  g.userData.tiks!.push((t, e) => { const ph = (t * 1.6) % 1; const at = e * (ph < 0.15 ? Math.sin((ph / 0.15) * Math.PI) : 0); g.scale.setScalar(1 + at * 0.14); });
  return g;
}
function sinirAgi(): Parca {
  const g = kap(); const rnd = rastgele(41); const dugum = Array.from({ length: 16 }, () => ickure(rnd, 0.15, 1.35));
  const nm = mat(RENK.mor, { emissive: 0x4c1d95, emissiveIntensity: 0.45 }); const kenarlar: [number, number][] = [];
  const dm = dugum.map((p) => { const s = kure(0.09, nm, 12); s.position.copy(p); g.add(s); return s; });
  const pts: number[] = [];
  dugum.forEach((a, i) => dugum.forEach((b, j) => { if (j > i && a.distanceTo(b) < 0.85) { kenarlar.push([i, j]); pts.push(a.x, a.y, a.z, b.x, b.y, b.z); } }));
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
  g.add(new THREE.LineSegments(geo, new THREE.LineBasicMaterial({ color: 0xc4b5fd, transparent: true, opacity: 0.55 })));
  const imp = Array.from({ length: 7 }, (_, i) => { const s = kure(0.045, new THREE.MeshBasicMaterial({ color: 0xfef08a }), 8); g.add(s); return { s, k: kenarlar[Math.floor(rnd() * kenarlar.length)], f: i * 0.37 }; });
  g.userData.tiks!.push((t, e) => {
    imp.forEach(({ s, k, f }) => { const u = ((t * 0.5 * e + f) % 1 + 1) % 1; s.position.copy(dugum[k[0]]).lerp(dugum[k[1]], u); });
    dm.forEach((d, i) => d.scale.setScalar(1 + (Math.sin(t * 4 + i * 1.7) * 0.5 + 0.5) * 0.28 * e));
    g.rotation.y = t * 0.2 * e;
  });
  return g;
}
function organoid(): Parca {
  const g = kap(); const rnd = rastgele(53); const rm = [RENK.gul, RENK.kok, RENK.mor, RENK.dut, RENK.mavi];
  for (let i = 0; i < 46; i++) { const p = ickure(rnd, 0.1, 1.0); const c = kure(0.16 + rnd() * 0.1, mat(rm[Math.floor((p.length() + rnd() * 0.2) * 3.2) % rm.length], { transparent: true, opacity: 0.82 }), 12); c.position.copy(p); g.add(c); }
  const lm = new THREE.Mesh(new THREE.TorusGeometry(0.35, 0.05, 8, 24), mat(0xffffff, { transparent: true, opacity: 0.35 })); g.add(lm);
  g.userData.tiks!.push((t, e) => { g.rotation.y = t * 0.25 * e; g.rotation.x = Math.sin(t * 0.3) * 0.2 * e; });
  return g;
}
function hekim(): Parca {
  const g = kap(); const govde = govdeKure(0.9, RENK.altin); ekle(g, govde);
  const c = cekirdek(0.42, true); ekle(g, c); ekle(g, mitokondri(3, 0.55)); ekle(g, er()); ekle(g, golgi());
  const hale = new THREE.Mesh(new THREE.TorusGeometry(1.2, 0.02, 8, 64), new THREE.MeshBasicMaterial({ color: 0xfde047, transparent: true, opacity: 0.7 })); g.add(hale);
  const kruvaz = new THREE.Group(); const km = mat(0xffffff, { emissive: 0xfde68a, emissiveIntensity: 0.7 });
  kruvaz.add(new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.34, 0.06), km), new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.1, 0.06), km)); kruvaz.position.set(0, 1.45, 0); g.add(kruvaz);
  g.userData.tiks!.push((t, e) => { hale.rotation.x = Math.PI / 2 + Math.sin(t * 0.6) * 0.3 * e; hale.rotation.y = t * 0.5 * e; kruvaz.rotation.y = t * 1.2 * e; });
  return g;
}

/** Basamak n (1–28) için hücre */
function kurHucre(n: number): Parca {
  const g = kap(); const rnd = rastgele(n * 31 + 7);
  switch (n) {
    case 1: { ekle(g, govdeKure(0.8, RENK.amber)); const bm = mat(0xfde68a); for (let i = 0; i < 6; i++) { const b = kure(0.05, bm, 8); b.position.copy(ickure(rnd, 0.9, 1.3)); g.add(b); } break; }
    case 2: ekle(g, govdeKure(0.85, RENK.amber)); ekle(g, rnaSerit()); break;
    case 3: { ekle(g, govdeKure(0.9, RENK.amber)); ekle(g, rnaSerit()); ekle(g, ribozimler(rnd, 5, 0.55)); break; }
    case 4: ekle(g, govdeKure(0.8, RENK.cam)); ekle(g, halkaDna(0.3)); break;
    case 5: ekle(g, govdeBasil(1.0, 0.45, RENK.cam)); ekle(g, halkaDna(0.25)); break;
    case 6: { ekle(g, govdeBasil(0.9, 0.42, RENK.cam)); ekle(g, halkaDna(0.24)); const k = kamci(0x0e7490, 0.95, 13); ekle(g, k); break; }
    case 7: { ekle(g, govdeBasil(1.0, 0.45, 0x14b8a6)); const tm = mat(0x16a34a, { transparent: true, opacity: 0.8 }); for (let i = -2; i <= 2; i++) { const r = new THREE.Mesh(new THREE.TorusGeometry(0.34, 0.025, 6, 24), tm); r.position.x = i * 0.2; r.rotation.y = Math.PI / 2; g.add(r); } break; }
    case 8: { ekle(g, govdeKure(0.8, RENK.kirmizi)); ekle(g, halkaDna(0.28, 0xfca5a5)); const pm = mat(0x991b1b); for (let i = 0; i < 12; i++) { const v = yuzey(rnd); const p = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.28, 5), pm); p.position.copy(v).multiplyScalar(0.95); p.lookAt(v.clone().multiplyScalar(3)); p.rotateX(Math.PI / 2); g.add(p); } break; }
    case 9: { ekle(g, govdeKure(0.85, RENK.cam)); ekle(g, halkaDna(0.22)); const f = new THREE.Mesh(new THREE.TorusKnotGeometry(0.45, 0.04, 100, 8, 2, 5), mat(0x0891b2, { transparent: true, opacity: 0.85 })); g.add(f); g.userData.tiks!.push((t, e) => { f.rotation.y = t * 0.25 * e; }); break; }
    case 10: { ekle(g, govdeKure(0.95, RENK.mavi)); const ic = kure(0.4, mat(0xa78bfa, { transparent: true, opacity: 0.5, depthWrite: false }), 20); g.add(ic); ekle(g, halkaDna(0.22)); break; }
    case 11: { ekle(g, govdeKure(1.0, RENK.mavi)); ekle(g, cekirdek(0.34)); const b = bakteri(); g.add(b); g.userData.tiks!.push((t, e) => { const k = (Math.sin(t * 0.7) * 0.5 + 0.5) * e; b.position.set(1.5 - k * 0.95, 0.1, 0.2); b.rotation.y = 0; }); break; }
    case 12: ekle(g, govdeKure(1.0, RENK.mavi)); ekle(g, cekirdek(0.36)); ekle(g, mitokondri(3)); ekle(g, er()); break;
    case 13: ekle(g, govdeKure(1.0, RENK.mavi)); ekle(g, cekirdek(0.34)); ekle(g, mitokondri(2)); ekle(g, er()); { const go = golgi(); go.position.set(0.42, 0.42, -0.3); go.rotation.z = 0.5; ekle(g, go); } break;
    case 14: ekle(g, govdeKure(1.0, RENK.mavi)); ekle(g, iskelet(rnd)); ekle(g, cekirdek(0.34)); ekle(g, mitokondri(3)); ekle(g, er()); { const go = golgi(); go.position.set(0.42, 0.42, -0.3); ekle(g, go); } break;
    case 15: ekle(g, amipGovde()); ekle(g, cekirdek(0.28, false)); ekle(g, mitokondri(2, 0.45)); break;
    case 16: ekle(g, govdeKure(1.0, RENK.mavi, [1.05, 0.7, 0.7])); ekle(g, cekirdek(0.3)); ekle(g, mitokondri(2, 0.45)); ekle(g, siller(0x1d4ed8)); break;
    case 17: ekle(g, govdeKure(1.0, RENK.yesil)); ekle(g, cekirdek(0.32)); ekle(g, mitokondri(2)); ekle(g, kloroplast(4)); ekle(g, iskelet(rnd, 0x86efac)); break;
    case 18: ekle(g, koloni()); break;
    case 19: ekle(g, epitel()); break;
    case 20: ekle(g, kasLifi(RENK.kas)); break;
    case 21: ekle(g, noronGovde()); break;
    case 22: ekle(g, kok()); break;
    case 23: ekle(g, kureTopu(16, false, RENK.dut, 0.3)); break;
    case 24: ekle(g, kureTopu(44, true, 0xfda4af, 0.2)); break;
    case 25: ekle(g, kalpKasi()); break;
    case 26: ekle(g, sinirAgi()); break;
    case 27: ekle(g, organoid()); break;
    default: ekle(g, hekim());
  }
  return g;
}

const GLUKOZ_AZ = 40;
const SOLGUN_ESIK = 20;

export default function Hucre3D({ n, glukoz, canlilik, onHata }: Props) {
  const kapEl = useRef<HTMLDivElement>(null);
  const pr = useRef({ n, glukoz, canlilik });
  const kirli = useRef(true);
  pr.current = { n, glukoz, canlilik }; kirli.current = true;

  useEffect(() => {
    const el = kapEl.current; if (!el) return;
    let renderer: THREE.WebGLRenderer;
    try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' }); }
    catch { onHata?.(); return; }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.domElement.className = 'hc15-3d-tuval';
    el.appendChild(renderer.domElement);

    const sahne = new THREE.Scene();
    const kamera = new THREE.PerspectiveCamera(38, 1, 0.1, 50); kamera.position.set(0, 0.4, 7.2); kamera.lookAt(0, 0, 0);
    sahne.add(new THREE.AmbientLight(0xffffff, 1.0));
    const isik = new THREE.DirectionalLight(0xffffff, 2.4); isik.position.set(3, 4, 5); sahne.add(isik);
    const arka = new THREE.PointLight(0x93c5fd, 18, 14); arka.position.set(-3, -2, -3); sahne.add(arka);
    const kok = new THREE.Group(); sahne.add(kok);

    const gGeo = new THREE.OctahedronGeometry(0.07, 0);
    const gMat = new THREE.MeshStandardMaterial({ color: 0xfbbf24, emissive: 0xf59e0b, emissiveIntensity: 0.8, roughness: 0.3 });
    const gluk = new THREE.InstancedMesh(gGeo, gMat, GLUKOZ_AZ); gluk.instanceMatrix.setUsage(THREE.DynamicDrawUsage); sahne.add(gluk);
    const gr = rastgele(99);
    const gp = Array.from({ length: GLUKOZ_AZ }, () => ({ faz: gr(), a: gr() * Math.PI * 2, y: (gr() - 0.5) * 3, hiz: 0.05 + gr() * 0.06 }));

    let halka: THREE.Mesh | null = null; let halkaT = -1;
    const mm = new THREE.Matrix4(), q = new THREE.Quaternion(), pos = new THREE.Vector3(), sc = new THREE.Vector3();
    const azHareket = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;

    let sar: THREE.Group | null = null, parca: Parca | null = null, born = -10, sonN = -1, ilk = true;
    const senkron = (simdi: number) => {
      const nn = Math.max(0, Math.min(28, pr.current.n));
      if (nn === sonN) return;
      if (sar) { kok.remove(sar); atKaldir(sar); sar = null; parca = null; }
      sonN = nn;
      if (nn >= 1) {
        parca = kurHucre(nn); sar = new THREE.Group(); sar.add(parca); kok.add(sar);
        born = ilk || azHareket ? -10 : simdi; if (!ilk && !azHareket) halkaT = simdi;
        // Geniş basamaklar (doku, ağ, koloni) kameraya sığsın
        sar.userData.boy = nn >= 18 ? 1.0 : 1.35;
      }
      ilk = false; kirli.current = true;
    };

    let sonBoy = '';
    const boyutla = () => {
      const w = el.clientWidth || 1, h = el.clientHeight || 1; const anahtar = `${w}x${h}`; if (anahtar === sonBoy) return; sonBoy = anahtar;
      renderer.setSize(w, h, false); kamera.aspect = w / h; kamera.position.z = w / h < 1 ? 7.2 / Math.max(0.6, w / h) * 0.85 : 7.2; kamera.updateProjectionMatrix(); kirli.current = true;
    };
    const ro = new ResizeObserver(boyutla); ro.observe(el); boyutla();

    let surukle = false, sx = 0, yaw = 0;
    const d = renderer.domElement;
    const ptrDown = (e: PointerEvent) => { surukle = true; sx = e.clientX; d.setPointerCapture(e.pointerId); };
    const ptrMove = (e: PointerEvent) => { if (!surukle) return; yaw += (e.clientX - sx) * 0.01; sx = e.clientX; kirli.current = true; };
    const ptrUp = () => { surukle = false; };
    d.addEventListener('pointerdown', ptrDown); d.addEventListener('pointermove', ptrMove); d.addEventListener('pointerup', ptrUp); d.addEventListener('pointercancel', ptrUp);

    let gorunur = true;
    const io = new IntersectionObserver(([e]) => { gorunur = !!e?.isIntersecting; if (gorunur) kirli.current = true; }, { threshold: 0 }); io.observe(el);

    let raf = 0; let t = 0; let son = performance.now();
    const dongu = (now: number) => {
      raf = requestAnimationFrame(dongu);
      if (!gorunur) { son = now; return; } // yalnız ekranda görünen hücre canlandırılır
      const dt = Math.min(0.05, (now - son) / 1000); son = now;
      const { canlilik: can, glukoz: gl } = pr.current;
      const e = azHareket ? 0 : can <= 0 ? 0.08 : 0.35 + 0.65 * (can / 100);
      senkron(t);
      if (e === 0 && !kirli.current && halkaT < 0) return; // hareketi azalt: tek kare
      t += dt;
      if (!surukle) yaw += dt * 0.25 * e;
      kok.rotation.y = yaw; kok.rotation.x = Math.sin(t * 0.25) * 0.12 * e;
      if (sar && parca) {
        const dogum = t - born; const bs = (sar.userData.boy as number) || 1;
        sar.scale.setScalar(bs * (dogum < 1.4 ? Math.max(0.001, easeOutBack(Math.max(0, dogum) / 1.4)) : 1));
        parca.userData.tiks?.forEach((f) => f(t, e));
      }
      const adet = Math.min(GLUKOZ_AZ, Math.ceil(gl / 8));
      for (let i = 0; i < GLUKOZ_AZ; i++) {
        const o = gp[i];
        if (i >= adet) { sc.set(0, 0, 0); mm.compose(pos.set(0, 0, 0), q, sc); gluk.setMatrixAt(i, mm); continue; }
        o.faz = (o.faz + dt * o.hiz * (0.2 + e * 1.6)) % 1;
        const r = 3.0 - o.faz * 2.05, a = o.a + o.faz * 3.2;
        pos.set(Math.cos(a) * r, o.y * (1 - o.faz) * 0.9, Math.sin(a) * r);
        sc.setScalar((o.faz > 0.93 ? (1 - o.faz) / 0.07 : 1) * 0.9 + 0.1);
        mm.compose(pos, q, sc); gluk.setMatrixAt(i, mm);
      }
      gluk.instanceMatrix.needsUpdate = true;
      if (halkaT >= 0) {
        const k = (t - halkaT) / 1.3;
        if (!halka) { halka = new THREE.Mesh(new THREE.TorusGeometry(1, 0.012, 8, 64), new THREE.MeshBasicMaterial({ color: 0x34d399, transparent: true, opacity: 0.8 })); halka.rotation.x = Math.PI / 2; sahne.add(halka); }
        if (k >= 1) { sahne.remove(halka); atKaldir(halka); halka = null; halkaT = -1; }
        else { halka.scale.setScalar(1 + k * 2.2); (halka.material as THREE.MeshBasicMaterial).opacity = 0.8 * (1 - k); }
      }
      // Soluklaşma: glukoz 20'nin altı (stres) ve düşük canlılık
      const sol = Math.max(1 - can / 100, gl < SOLGUN_ESIK ? (1 - Math.max(0, gl) / SOLGUN_ESIK) * 0.7 : 0);
      d.style.filter = sol < 0.01 ? '' : `grayscale(${Math.min(0.95, sol * 1.1).toFixed(2)}) brightness(${(1 - sol * 0.3).toFixed(2)})`;
      renderer.render(sahne, kamera);
      kirli.current = false;
    };
    raf = requestAnimationFrame(dongu);

    return () => {
      cancelAnimationFrame(raf); ro.disconnect(); io.disconnect();
      d.removeEventListener('pointerdown', ptrDown); d.removeEventListener('pointermove', ptrMove); d.removeEventListener('pointerup', ptrUp); d.removeEventListener('pointercancel', ptrUp);
      atKaldir(sahne); gGeo.dispose(); gMat.dispose(); gluk.dispose(); renderer.dispose(); d.remove();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return <div ref={kapEl} className="hc15-3d" role="img" aria-label={`Üç boyutlu hücre: ${n}. basamak, canlılık %${Math.round(canlilik)}${glukoz < SOLGUN_ESIK ? ', glukoz az' : ''}`} />;
}

const easeOutBack = (x: number) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };

function atKaldir(o: THREE.Object3D) {
  o.traverse((x: any) => {
    x.geometry?.dispose?.();
    const m = x.material; if (Array.isArray(m)) m.forEach((y) => y.dispose?.()); else m?.dispose?.();
  });
}
