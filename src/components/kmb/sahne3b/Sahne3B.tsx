/**
 * KMB 3B sahne bileşeni — three.js ile gerçek zamanlı, stüdyo ışıklı sahne. SVG `SahneCiz` ile aynı sözleşme: `durum`
 * (öge kimliği → vurgu / çiz / renk / gör / etiket) ve isteğe bağlı `odak` (kamera o ögeye ılımlı yaklaşır, geri kalanı
 * loşlaşmaz; ayrıntı kesilmez — H462). Etiketler HTML katmanında (Türkçe karakterler net), ögenin 3B konumuna izdüşümle
 * bağlanır ve çakışınca aşağı itilir. Tıklama (`onSec`) ışın atımıyla ögeyi bulur (sahnede bul / etiketle sınavları).
 * Başarım: yalnız ekrandayken çizer, DPR ≤ 2, sekme gizliyken durur; WebGL yoksa `onHata` ile SVG'ye dönülür.
 * Sahne tanımları: ./sahneler3b.ts (kimlikler SAHNE_OGELERI ile aynı; dogrula.py aynı kapı).
 */
import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import type { SahneDurum } from '../sahneler';
import { Oge3, RENK, fon, yumusak } from './yardimci';

export type Sahne3BTanim = {
  ad: string;
  gizli: string[];
  /** öge → etiket metni */
  etiket: Record<string, string>;
  kamera: { poz: [number, number, number]; hedef: [number, number, number] };
  /** gölge zemini yüksekliği (yoksa zemin çizilmez) */
  zeminY?: number;
  kur: () => Oge3[];
};

type Props = {
  tanim: Sahne3BTanim;
  durum: SahneDurum;
  odak?: string | null;
  /** bakış açısı sapması [yaw, pitch] derece (vuruş başına kamera yörüngesi) */
  aci?: [number, number] | null;
  onSec?: (id: string) => void;
  secilebilir?: boolean;
  isaret?: { id: string; dogru: boolean } | null;
  onHata?: () => void;
  className?: string;
};

type Canli = { vurguBas: number; cizBas: number; cizSayac: number; vurguSayac: number; gorHedef: number; gor: number };

export default function Sahne3B({ tanim, durum, odak, aci, onSec, secilebilir, isaret, onHata, className }: Props) {
  const kap = useRef<HTMLDivElement>(null);
  const etiketKap = useRef<HTMLDivElement>(null);
  const durumRef = useRef(durum); durumRef.current = durum;
  const odakRef = useRef(odak); odakRef.current = odak;
  const aciRef = useRef(aci); aciRef.current = aci;
  const isaretRef = useRef(isaret); isaretRef.current = isaret;
  const onSecRef = useRef(onSec); onSecRef.current = onSec;
  const motor = useRef<{ uygula: () => void; odakla: () => void } | null>(null);

  useEffect(() => {
    const el = kap.current, ek = etiketKap.current;
    if (!el || !ek) return;
    let renderer: THREE.WebGLRenderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
    } catch { onHata?.(); return; }
    renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 0.95;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    el.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    scene.background = fon('#f8fafc', '#d9e2ec');
    const pmrem = new THREE.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.45;

    const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 200);
    const K0 = { poz: new THREE.Vector3(...tanim.kamera.poz), hedef: new THREE.Vector3(...tanim.kamera.hedef) };
    camera.position.copy(K0.poz);
    const bakis = K0.hedef.clone();
    camera.lookAt(bakis);

    // ışıklar: sıcak ana + soğuk dolgu + arka kenar + gök/zemin
    scene.add(new THREE.HemisphereLight(0xe3ecf6, 0xcdbcae, 0.55));
    const ana = new THREE.DirectionalLight(0xfff3e2, 2.3);
    ana.position.set(6, 11, 7); ana.castShadow = true;
    ana.shadow.mapSize.set(2048, 2048); ana.shadow.radius = 6; ana.shadow.bias = -0.0006; ana.shadow.normalBias = 0.02;
    const sc = ana.shadow.camera; sc.left = sc.bottom = -14; sc.right = sc.top = 14; sc.near = 1; sc.far = 40;
    scene.add(ana);
    const dolgu = new THREE.DirectionalLight(0xd6e4ff, 0.75); dolgu.position.set(-9, 5, -3); scene.add(dolgu);
    const kenar = new THREE.DirectionalLight(0xffffff, 0.9); kenar.position.set(-3, 7, -9); scene.add(kenar);
    if (tanim.zeminY !== undefined) {
      const z = new THREE.Mesh(new THREE.CircleGeometry(40, 48), new THREE.ShadowMaterial({ opacity: 0.2 }));
      z.rotation.x = -Math.PI / 2; z.position.y = tanim.zeminY; z.receiveShadow = true; scene.add(z);
    }

    // ögeler
    const ogeler = tanim.kur();
    const O = new Map<string, Oge3>();
    const C = new Map<string, Canli>();
    const gizli = new Set(tanim.gizli);
    for (const o of ogeler) {
      o.gizli = gizli.has(o.id);
      scene.add(o.grup);
      O.set(o.id, o);
      C.set(o.id, { vurguBas: -9, cizBas: -9, cizSayac: 0, vurguSayac: 0, gorHedef: o.gizli ? 0 : 1, gor: o.gizli ? 0 : 1 });
      o.grup.traverse((m) => { if ((m as THREE.Mesh).isMesh) (m as THREE.Mesh).userData.ogeId = o.id; });
    }
    // vurgu: ögenin kendi malzemelerinde mavi-beyaz ışıma nabzı (hale/kubbe YOK — sahneyi kaplıyordu, H463)
    const malzemeler = (o: Oge3) => { const L: THREE.MeshStandardMaterial[] = []; o.grup.traverse((m) => { const mt = (m as THREE.Mesh).material as THREE.MeshStandardMaterial | undefined; if (mt && 'emissive' in mt) L.push(mt); }); return L; };
    const vurguRenk = new THREE.Color(0x6aa8ff);
    const isaretK = new THREE.Mesh(new THREE.TorusGeometry(1, 0.06, 12, 48), new THREE.MeshBasicMaterial({ color: 0x2e9e5b, transparent: true, opacity: 0.95, depthTest: false }));
    isaretK.visible = false; isaretK.renderOrder = 6; scene.add(isaretK);

    // etiketler (HTML)
    const E = new Map<string, HTMLSpanElement>();
    for (const [id, metin] of Object.entries(tanim.etiket)) {
      const s = document.createElement('span'); s.className = 'kmb-3b-etiket'; s.textContent = metin; s.style.display = 'none'; ek.appendChild(s); E.set(id, s);
    }

    // ögenin görünür kutusu
    const kutu = new THREE.Box3();
    const kutuOlc = (o: Oge3) => { o.grup.updateWorldMatrix(true, true); kutu.setFromObject(o.grup); return kutu; };

    // durum → ögeler
    let simdi = 0;
    const uygula = () => {
      const d = durumRef.current;
      for (const [id, o] of O) {
        const c = C.get(id)!; const x = d[id] || {};
        const gor = x.gor ?? (x.ciz ? true : !o.gizli);
        c.gorHedef = gor ? 1 : 0;
        if ((x.vurgu || 0) !== c.vurguSayac) { c.vurguSayac = x.vurgu || 0; c.vurguBas = simdi; }
        if ((x.ciz || 0) !== c.cizSayac) { c.cizSayac = x.ciz || 0; c.cizBas = simdi; }
        const renk = x.renk ? RENK[x.renk] : undefined;
        for (const m of o.boyalar) {
          if (renk !== undefined) { m.emissive.setHex(renk); m.emissiveIntensity = 0.35; m.userData.renkli = true; }
          else if (m.userData.renkli) { m.emissive.setHex(0); m.emissiveIntensity = 0; m.userData.renkli = false; }
        }
        const e = E.get(id); if (e) e.style.display = x.etiket && gor ? '' : 'none';
      }
    };
    // kamera odağı: ögenin kutusunu kadrajın en çok ~%55'ine sığdıracak kadar yaklaş (ılımlı), yoksa başlangıç
    let kamHedef = { poz: K0.poz.clone(), bak: K0.hedef.clone() };
    let kamBas = { poz: K0.poz.clone(), bak: K0.hedef.clone() }, kamT0 = -9;
    const odakla = () => {
      const id = odakRef.current; const o = id ? O.get(id) : undefined;
      kamBas = { poz: camera.position.clone(), bak: bakis.clone() }; kamT0 = simdi;
      // bakış yönü: varsayılan yön + vuruşun açı sapması (yaw: Y ekseni etrafında, pitch: yana eksen etrafında)
      const yon = K0.poz.clone().sub(K0.hedef).normalize();
      const a = aciRef.current;
      if (a && (a[0] || a[1])) {
        yon.applyAxisAngle(new THREE.Vector3(0, 1, 0), (a[0] * Math.PI) / 180);
        const yan = new THREE.Vector3().crossVectors(new THREE.Vector3(0, 1, 0), yon).normalize();
        yon.applyAxisAngle(yan, (-a[1] * Math.PI) / 180).normalize();
      }
      const u0 = K0.poz.distanceTo(K0.hedef);
      if (!o || C.get(o.id)!.gorHedef === 0) { kamHedef = { poz: K0.hedef.clone().addScaledVector(yon, u0), bak: K0.hedef.clone() }; return; }
      const b = kutuOlc(o); if (b.isEmpty()) { kamHedef = { poz: K0.hedef.clone().addScaledVector(yon, u0), bak: K0.hedef.clone() }; return; }
      const merkez = b.getCenter(new THREE.Vector3()); const r = b.getSize(new THREE.Vector3()).length() / 2;
      const fov = (camera.fov * Math.PI) / 180;
      const gerekli = (r / Math.sin(fov / 2)) * 1.9; // kutu kadrajın ~%55'i
      const u = Math.max(u0 * 0.6, Math.min(u0, gerekli));
      // bakış, odakla başlangıç hedefi arasında: sahne bağlamı kaybolmasın
      const bak = K0.hedef.clone().lerp(merkez, 0.75);
      kamHedef = { poz: bak.clone().addScaledVector(yon, u), bak };
    };
    motor.current = { uygula, odakla };
    uygula(); odakla();

    // boyut
    const boyutla = () => {
      const w = el.clientWidth || 1, h = el.clientHeight || 1;
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
    };
    boyutla();
    const ro = new ResizeObserver(boyutla); ro.observe(el);

    // tıklama: ışın atımı
    const ray = new THREE.Raycaster(); const nokta = new THREE.Vector2();
    const tikla = (ev: MouseEvent) => {
      if (!onSecRef.current) return;
      const r = renderer.domElement.getBoundingClientRect();
      nokta.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
      ray.setFromCamera(nokta, camera);
      const hits = ray.intersectObjects(scene.children, true);
      for (const h of hits) {
        let m: THREE.Object3D | null = h.object; let id = '';
        while (m && !id) { id = m.userData?.ogeId || ''; m = m.parent; }
        if (id && C.get(id)!.gor > 0.5) { onSecRef.current(id); return; }
      }
    };
    renderer.domElement.addEventListener('click', tikla);

    // döngü
    let gorunur = true, id = 0, onceki = performance.now(), say = 0;
    const io = typeof IntersectionObserver !== 'undefined' ? new IntersectionObserver(([e]) => { gorunur = e.isIntersecting; }, { rootMargin: '200px' }) : null;
    io?.observe(el);
    const azalt = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    const tmpV = new THREE.Vector3();
    const yerler: [number, number][] = [];
    const dongu = (now: number) => {
      id = requestAnimationFrame(dongu);
      const dtHam = (now - onceki) / 1000; onceki = now;
      const dt = Number.isFinite(dtHam) ? Math.min(0.1, Math.max(0, dtHam)) : 0;
      if (!gorunur || document.hidden) return;
      simdi += dt;
      // kamera
      const f = yumusak(Math.min(1, (simdi - kamT0) / 1.1));
      camera.position.lerpVectors(kamBas.poz, kamHedef.poz, f);
      bakis.lerpVectors(kamBas.bak, kamHedef.bak, f);
      if (!azalt) { // nefes: çok hafif yörünge sallantısı
        const a = Math.sin(simdi * 0.35) * 0.012, b = Math.cos(simdi * 0.27) * 0.008;
        camera.position.applyAxisAngle(new THREE.Vector3(0, 1, 0), a);
        camera.position.y += b * 0.5;
      }
      camera.lookAt(bakis);
      // ögeler
      for (const [oid, o] of O) {
        const c = C.get(oid)!;
        c.gor += (c.gorHedef - c.gor) * Math.min(1, dt * 7);
        const gor = c.gor > 0.02;
        o.grup.visible = gor;
        if (gor) { const s = 0.9 + 0.1 * yumusak(c.gor); o.grup.scale.setScalar(s); }
        if (o.cizici) { const cf = c.cizSayac ? yumusak(Math.min(1, (simdi - c.cizBas) / 1.7)) : 1; o.cizici(cf); }
        o.tik?.(simdi, dt);
        const vt = simdi - c.vurguBas;
        if (vt >= 0 && vt < 2.8 && gor) {
          const nabiz = 0.5 + 0.5 * Math.sin(vt * Math.PI * 2 / 1.4);
          const guc = 0.55 * nabiz * (1 - vt / 2.8);
          for (const mt of malzemeler(o)) { if (mt.userData.renkli) continue; mt.emissive.copy(vurguRenk); mt.emissiveIntensity = guc; mt.userData.nabiz = true; }
          // hafif büyüme: öge "nefes alır"
          o.grup.scale.multiplyScalar(1 + 0.025 * nabiz);
        } else if (c.vurguSayac && vt >= 2.8 && vt < 2.9) {
          for (const mt of malzemeler(o)) if (mt.userData.nabiz && !mt.userData.renkli) { mt.emissive.setHex(0); mt.emissiveIntensity = 0; mt.userData.nabiz = false; }
        }
      }
      // sınav işareti
      const is = isaretRef.current;
      if (is && O.get(is.id)) {
        const b = kutuOlc(O.get(is.id)!); b.getCenter(isaretK.position); isaretK.scale.setScalar(b.getSize(tmpV).length() / 2 + 0.2);
        (isaretK.material as THREE.MeshBasicMaterial).color.setHex(is.dogru ? 0x2e9e5b : 0xd23b3b); isaretK.visible = true; isaretK.lookAt(camera.position);
      } else isaretK.visible = false;
      renderer.render(scene, camera);
      // etiketler (her 2 karede bir)
      if ((say++ & 1) === 0) {
        yerler.length = 0;
        const W = el.clientWidth, H = el.clientHeight;
        for (const [eid, s] of E) {
          if (s.style.display === 'none') continue;
          const o = O.get(eid); if (!o) continue;
          const b = kutuOlc(o);
          if (o.etiketNoktasi) tmpV.copy(o.etiketNoktasi).applyMatrix4(o.grup.matrixWorld); else { b.getCenter(tmpV); tmpV.y = b.max.y; }
          tmpV.project(camera);
          let x = (tmpV.x * 0.5 + 0.5) * W, y = (-tmpV.y * 0.5 + 0.5) * H - 18;
          x = Math.min(W - 60, Math.max(60, x)); y = Math.min(H - 24, Math.max(16, y));
          for (let n = 0; n < 6 && yerler.some(([a, b2]) => Math.abs(a - x) < 150 && Math.abs(b2 - y) < 30); n++) y -= 32;
          if (y < 16) y = 16;
          yerler.push([x, y]);
          s.style.transform = `translate(${x}px, ${y}px) translate(-50%, -100%)`;
        }
      }
    };
    id = requestAnimationFrame(dongu);

    return () => {
      cancelAnimationFrame(id); ro.disconnect(); io?.disconnect();
      renderer.domElement.removeEventListener('click', tikla);
      scene.traverse((m) => { const g = (m as THREE.Mesh).geometry; if (g) g.dispose(); const mt = (m as THREE.Mesh).material as THREE.Material | THREE.Material[] | undefined; if (mt) (Array.isArray(mt) ? mt : [mt]).forEach((x) => x.dispose()); });
      pmrem.dispose(); renderer.dispose();
      el.removeChild(renderer.domElement); ek.replaceChildren();
      motor.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tanim]);
  useEffect(() => { motor.current?.uygula(); motor.current?.odakla(); }, [durum, odak, aci]);

  return (
    <div className={`kmb-3b${secilebilir ? ' secilebilir' : ''}${className ? ` ${className}` : ''}`} role="img" aria-label={tanim.ad}>
      <div ref={kap} className="kmb-3b-tuval" />
      <div ref={etiketKap} className="kmb-3b-etiketler" aria-hidden />
    </div>
  );
}
