/** Pointer sürükleme motoru (fare + dokunma + kalem). Hedef bulma: elementsFromPoint + data-om-hedef; hayalet rAF + transform ile izler. */
import { useCallback, useEffect, useRef, useState } from 'react';
import { azHareket, titret } from '../ortak';

export type Kaynak = 'el' | 'deste' | 'atik';
export interface Hedef { tur: 'yuva' | 'uc' | 'per' | 'yeni' | 'atik' | 'istaka'; i?: number; per?: number; uc?: 'bas' | 'son' | 'bol' | null; el: HTMLElement }
export interface Surukleme { src: Kaynak; id: number; ids: number[]; durum: 'surukle' | 'asili' | 'donus' }
export interface Rect { x: number; y: number; w: number; h: number }
export interface SurukleSecenek {
  kilit: boolean;
  /** Sürüklenecek taşlar; null = sürüklenemez */
  idsAl(src: Kaynak, id: number): number[] | null;
  dokun(src: Kaynak, id: number): void;
  uzunBas(src: Kaynak, id: number): void;
  /** tamam: bitti · bekle: hayalet sunucu yanıtına dek bırakıldığı yerde asılı · red: yaylanarak döner */
  birak(hedef: Hedef | null, s: { src: Kaynak; ids: number[]; nokta: Rect }): 'tamam' | 'bekle' | 'red';
}

export function hedefBul(x: number, y: number): Hedef | null {
  for (const el of document.elementsFromPoint(x, y) as HTMLElement[]) {
    const tur = el.dataset?.omHedef as Hedef['tur'] | undefined;
    if (!tur) continue;
    if (tur === 'istaka') { // yuvalar arası boşluk: en yakın yuvaya say
      let en: HTMLElement | null = null, enUzak = Infinity;
      el.querySelectorAll<HTMLElement>('[data-om-hedef="yuva"]').forEach((yv) => { const r = yv.getBoundingClientRect(); const u = Math.hypot(r.left + r.width / 2 - x, r.top + r.height / 2 - y); if (u < enUzak && u < r.height) { enUzak = u; en = yv; } });
      if (en) return { tur: 'yuva', el: en, i: +(en as HTMLElement).dataset.i! };
    }
    const uc = el.dataset.uc;
    return { tur, el, i: el.dataset.i ? +el.dataset.i : undefined, per: el.dataset.per ? +el.dataset.per : undefined, uc: uc === 'bas' || uc === 'son' || uc === 'bol' ? uc : null };
  }
  return null;
}

interface Basis { pid: number; tip: string; x0: number; y0: number; x: number; y: number; src: Kaynak; id: number; el: HTMLElement; kok: HTMLElement; surukle: boolean; uzun: boolean; zaman: any; raf: number; egim: number; sonX: number; hedef: Hedef | null; bx: number; by: number; kaldir: number; temizle: () => void }

export function useSurukle(sec: SurukleSecenek) {
  const [sur, setSur] = useState<Surukleme | null>(null);
  const hayalet = useRef<HTMLDivElement | null>(null);
  const b = useRef<Basis | null>(null);
  const secRef = useRef(sec);
  secRef.current = sec;
  const sonBitis = useRef(0);
  const asiliZaman = useRef<any>(null);

  const isaretSil = (h: Hedef | null) => h?.el.classList.remove('om-uzerinde');
  const yerlestir = (s: Basis) => {
    const g = hayalet.current;
    if (!g) return;
    const k = s.kok.getBoundingClientRect();
    const w = g.offsetWidth, h = g.offsetHeight;
    g.style.transform = `translate3d(${s.x - k.left - w / 2}px,${s.y + s.kaldir - k.top - h / 2}px,0) rotate(${s.egim.toFixed(2)}deg) scale(1.12)`;
    g.style.opacity = '1';
  };
  const bitir = useCallback(() => { clearTimeout(asiliZaman.current); sonBitis.current = performance.now(); setSur(null); }, []);
  const geriDon = useCallback(() => {
    clearTimeout(asiliZaman.current);
    const g = hayalet.current, s = b.current;
    if (!g || !s || azHareket()) { bitir(); return; }
    const k = s.kok.getBoundingClientRect();
    const hedef = `translate3d(${s.bx - k.left - g.offsetWidth / 2}px,${s.by - k.top - g.offsetHeight / 2}px,0) rotate(0deg) scale(1)`;
    setSur((x) => (x ? { ...x, durum: 'donus' } : x));
    const a = g.animate([{ transform: g.style.transform }, { transform: hedef }], { duration: 300, easing: 'cubic-bezier(.34,1.4,.64,1)', fill: 'forwards' });
    a.onfinish = a.oncancel = () => bitir();
  }, [bitir]);

  const son = (iptal: boolean) => {
    const s = b.current;
    if (!s) return;
    clearTimeout(s.zaman);
    cancelAnimationFrame(s.raf);
    s.temizle();
    try { s.kok.releasePointerCapture(s.pid); } catch { /* yok */ }
    const hedef = s.hedef;
    isaretSil(hedef);
    s.pid = -1;
    if (!s.surukle) { if (!iptal && !s.uzun) secRef.current.dokun(s.src, s.id); b.current = null; return; }
    sonBitis.current = performance.now();
    if (iptal) return geriDon();
    const g = hayalet.current;
    const r = g ? g.getBoundingClientRect() : null;
    const nokta: Rect = r ? { x: r.left, y: r.top, w: r.width, h: r.height } : { x: s.x, y: s.y, w: 0, h: 0 };
    const sonuc = secRef.current.birak(hedef, { src: s.src, ids: idsRef.current, nokta });
    if (sonuc === 'tamam') bitir();
    else if (sonuc === 'red') geriDon();
    else {
      setSur((x) => (x ? { ...x, durum: 'asili' } : x));
      if (g) g.style.transform = g.style.transform.replace(/rotate\([^)]*\) scale\([^)]*\)/, 'rotate(0deg) scale(1)');
      asiliZaman.current = setTimeout(geriDon, 2600);
    }
  };
  const idsRef = useRef<number[]>([]);

  const onPointerDown = useCallback((e: React.PointerEvent<HTMLElement>) => {
    if (secRef.current.kilit || b.current?.pid !== undefined && b.current.pid !== -1) return;
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    const el = (e.target as HTMLElement).closest?.('[data-om-src]') as HTMLElement | null;
    if (!el || sur) return;
    const kok = e.currentTarget;
    const r = el.getBoundingClientRect();
    const s: Basis = {
      pid: e.pointerId, tip: e.pointerType, x0: e.clientX, y0: e.clientY, x: e.clientX, y: e.clientY, src: el.dataset.omSrc as Kaynak, id: +(el.dataset.omId ?? -1), el, kok,
      surukle: false, uzun: false, zaman: null, raf: 0, egim: 0, sonX: e.clientX, hedef: null, bx: r.left + r.width / 2, by: r.top + r.height / 2, kaldir: 0, temizle: () => {},
    };
    b.current = s;
    try { kok.setPointerCapture(e.pointerId); } catch { /* yok */ }
    s.zaman = setTimeout(() => { if (b.current === s && !s.surukle) { s.uzun = true; titret(18); secRef.current.uzunBas(s.src, s.id); } }, 350);
    const dongu = () => {
      if (b.current !== s || s.pid === -1) return;
      const hiz = s.x - s.sonX;
      s.sonX = s.x;
      s.egim += (Math.max(-14, Math.min(14, hiz * 0.9)) - s.egim) * 0.22;
      yerlestir(s);
      const h = hedefBul(s.x, s.y + s.kaldir);
      if (h?.el !== s.hedef?.el) { isaretSil(s.hedef); h?.el.classList.add('om-uzerinde'); }
      s.hedef = h;
      s.raf = requestAnimationFrame(dongu);
    };
    const hareket = (ev: PointerEvent) => {
      if (ev.pointerId !== s.pid) return;
      s.x = ev.clientX; s.y = ev.clientY;
      if (s.surukle) { ev.preventDefault(); return; }
      if (Math.hypot(s.x - s.x0, s.y - s.y0) < (s.tip === 'touch' ? 9 : 5)) return;
      clearTimeout(s.zaman);
      const ids = secRef.current.idsAl(s.src, s.id);
      if (!ids?.length) { s.uzun = true; return; }
      s.surukle = true;
      idsRef.current = ids;
      s.kaldir = s.tip === 'mouse' ? 0 : -Math.min(64, r.height * 0.8);
      setSur({ src: s.src, id: s.id, ids, durum: 'surukle' });
      s.raf = requestAnimationFrame(dongu);
    };
    const birak = (ev: PointerEvent) => { if (ev.pointerId === s.pid) son(false); };
    const iptal = (ev: PointerEvent) => { if (ev.pointerId === s.pid) son(true); };
    window.addEventListener('pointermove', hareket, { passive: false });
    window.addEventListener('pointerup', birak);
    window.addEventListener('pointercancel', iptal);
    s.temizle = () => { window.removeEventListener('pointermove', hareket); window.removeEventListener('pointerup', birak); window.removeEventListener('pointercancel', iptal); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sur]);

  useEffect(() => () => { const s = b.current; if (s) { clearTimeout(s.zaman); cancelAnimationFrame(s.raf); s.temizle(); isaretSil(s.hedef); } clearTimeout(asiliZaman.current); }, []);

  return { sur, hayalet, onPointerDown, bitir, geriDon, /** Sürükleme az önce bitti mi (ardından gelen click'i yutmak için) */ azOnce: () => performance.now() - sonBitis.current < 350 };
}
