/**
 * Ders PDF'ini uygulamanın içinde çizen görüntüleyici (PDF.js). Tembel yüklenir (ayrı parça).
 *
 * Neden iframe değil: tarayıcının PDF eklentisi telefonlarda iframe içinde çalışmıyor, her sayfa değişiminde
 * belge baştan indiriliyordu ve sayfa/kaynak vurgusu uygulamadan kontrol edilemiyordu.
 *
 * Performans:
 *  - Sunucu Range (206) destekler; `disableAutoFetch` + `disableStream` ile yalnız çizilen sayfaların baytları gelir.
 *  - Sayfa yuvaları önceden boyutlanır (kaydırma çubuğu sabit), yalnız görünen ±1 sayfa çizilir; uzaktaki
 *    tuvaller bırakılır (telefon belleği). Yakınlaştırmada eski tuval yeni çizim bitene kadar ölçeklenerek kalır.
 *  - Metin katmanı (seçme/kopyalama) yalnız görünür sayfalarda kurulur.
 */
import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import * as pdfjs from 'pdfjs-dist';
import type { PDFDocumentProxy, PDFPageProxy, RenderTask } from 'pdfjs-dist';
import workerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import { getCustomApiUrl } from '../../../services/api';
import './pdfDoc.css';

pdfjs.GlobalWorkerOptions.workerSrc = workerUrl;

export interface PdfDocViewProps {
  /** Sunucu akış adresi ya da blob: (kullanıcının seçtiği dosya) */
  src: string;
  /** Hedef sayfa; değişince o sayfaya kaydırılır */
  page: number;
  /** Bu adımın kaynak sayfaları (vurgulanır) */
  highlight?: [number, number];
  /** 1 = sayfa genişliğine sığdır */
  zoom: number;
  onZoom?: (z: number) => void;
  onVisiblePage?: (p: number) => void;
  onLoaded?: (numPages: number) => void;
  onError?: (message: string) => void;
}

const GAP = 12;
const PAD = 12;
const MAX_CANVAS_PX = 12_000_000; // iOS tuval sınırının altında
const KEEP = 4; // görünür aralığın dışında tutulacak çizili sayfa

interface Slot {
  canvas?: HTMLCanvasElement;
  text?: HTMLDivElement;
  scale?: number; // çizildiği ölçek
  task?: RenderTask | null;
  textFor?: number; // metin katmanı kuruldu
}

export default function PdfDocView({ src, page, highlight, zoom, onZoom, onVisiblePage, onLoaded, onError }: PdfDocViewProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [doc, setDoc] = useState<PDFDocumentProxy | null>(null);
  const [sizes, setSizes] = useState<{ w: number; h: number }[]>([]);
  const [width, setWidth] = useState(0);
  const [progress, setProgress] = useState<number | null>(0);
  const slots = useRef(new Map<number, Slot>());
  const slotEls = useRef(new Map<number, HTMLDivElement>());
  const pages = useRef(new Map<number, Promise<PDFPageProxy>>());
  const visible = useRef(1);
  const lastTarget = useRef<number | null>(null);
  /** Programatik kaydırma sürerken ara sayfalar "görünen sayfa" diye geri bildirilmez (hedefi ezmesin). */
  const seeking = useRef<{ page: number; until: number } | null>(null);
  const raf = useRef(0);
  const cb = useRef({ onVisiblePage, onLoaded, onError, onZoom });
  cb.current = { onVisiblePage, onLoaded, onError, onZoom };

  /* ---- belge ---- */
  useEffect(() => {
    let dead = false;
    setDoc(null);
    setSizes([]);
    setProgress(0);
    slots.current.clear();
    pages.current.clear();
    lastTarget.current = null;
    const base = `${getCustomApiUrl() || ''}/vendor/pdfjs/`;
    const task = pdfjs.getDocument({
      url: src,
      rangeChunkSize: 512 * 1024,
      disableAutoFetch: true,
      disableStream: true,
      isEvalSupported: false,
      standardFontDataUrl: `${base}standard_fonts/`,
      wasmUrl: `${base}wasm/`,
      iccUrl: `${base}iccs/`,
      cMapUrl: `${base}cmaps/`,
      cMapPacked: true,
    });
    let opened = false; // açıldıktan sonraki parça indirmeleri yükleme katmanını geri getirmesin
    task.onProgress = ({ loaded, total }: { loaded: number; total: number }) => {
      if (!dead && !opened && total) setProgress(Math.min(99, Math.round((loaded / total) * 100)));
    };
    task.promise.then(
      async (d) => {
        if (dead) return void d.destroy();
        const first = await d.getPage(1);
        if (dead) return;
        opened = true;
        pages.current.set(1, Promise.resolve(first));
        const v = first.getViewport({ scale: 1 });
        setSizes(Array.from({ length: d.numPages }, () => ({ w: v.width, h: v.height })));
        setDoc(d);
        setProgress(null);
        cb.current.onLoaded?.(d.numPages);
      },
      (err: any) => {
        if (dead) return;
        setProgress(null);
        cb.current.onError?.(err?.name === 'PasswordException' ? 'PDF parolalı.' : err?.message || 'PDF açılamadı.');
      },
    );
    return () => {
      dead = true;
      for (const s of slots.current.values()) s.task?.cancel();
      task.destroy();
    };
  }, [src]);

  const getPage = useCallback(
    (n: number) => {
      if (!doc) return Promise.reject(new Error('belge yok'));
      let p = pages.current.get(n);
      if (!p) {
        p = doc.getPage(n);
        pages.current.set(n, p);
      }
      return p;
    },
    [doc],
  );

  // Sayfa boyutları: slayt PDF'lerinde hepsi aynıdır; farklı olanlar boşta düzeltilir (yerleşim kaymasın diye toplu).
  useEffect(() => {
    if (!doc || doc.numPages < 2) return;
    let dead = false;
    const idle = (window as any).requestIdleCallback || ((f: () => void) => setTimeout(f, 200));
    idle(async () => {
      const next: { w: number; h: number }[] = [];
      for (let i = 1; i <= doc.numPages && !dead; i++) {
        const v = (await getPage(i)).getViewport({ scale: 1 });
        next.push({ w: v.width, h: v.height });
      }
      if (!dead) setSizes((old) => (old.length === next.length && old.every((o, i) => o.w === next[i].w && o.h === next[i].h) ? old : next));
    });
    return () => {
      dead = true;
    };
  }, [doc, getPage]);

  /* ---- yerleşim ---- */
  useLayoutEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    const ro = new ResizeObserver(() => setWidth(el.clientWidth));
    ro.observe(el);
    setWidth(el.clientWidth);
    return () => ro.disconnect();
  }, []);

  const avail = Math.max(120, width - PAD * 2);
  const scaleOf = (i: number) => (sizes[i] ? (avail / sizes[i].w) * zoom : 1);
  const tops: number[] = [];
  let acc = PAD;
  sizes.forEach((s, i) => {
    tops.push(acc);
    acc += s.h * scaleOf(i) + GAP;
  });
  const totalH = acc + PAD - GAP;
  const geo = useRef({ tops, sizes, scaleOf });
  geo.current = { tops, sizes, scaleOf };

  /* ---- çizim ---- */
  const renderSlot = useCallback(
    async (n: number, withText: boolean) => {
      const host = slotEls.current.get(n);
      if (!host || !doc) return;
      const scale = geo.current.scaleOf(n - 1);
      const slot = slots.current.get(n) || {};
      slots.current.set(n, slot);
      if (slot.scale !== scale && !slot.task) {
        const pg = await getPage(n);
        if (slots.current.get(n) !== slot) return; // bu arada bırakıldı
        const vp = pg.getViewport({ scale });
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const out = Math.min(dpr, Math.sqrt(MAX_CANVAS_PX / (vp.width * vp.height)));
        const canvas = document.createElement('canvas');
        canvas.width = Math.floor(vp.width * out);
        canvas.height = Math.floor(vp.height * out);
        canvas.className = 'pdv-canvas';
        const task = pg.render({ canvas, viewport: vp, transform: out !== 1 ? [out, 0, 0, out, 0, 0] : undefined });
        slot.task = task;
        try {
          await task.promise;
          if (slotEls.current.get(n) !== host || slots.current.get(n) !== slot) {
            canvas.width = 0;
            return;
          }
          slot.canvas?.remove();
          if (slot.canvas) slot.canvas.width = 0;
          host.prepend(canvas);
          slot.canvas = canvas;
          slot.scale = scale;
          host.classList.add('is-drawn');
        } catch {
          canvas.width = 0; // iptal edildi
        } finally {
          slot.task = null;
        }
        // Ölçek bu arada değiştiyse yeniden
        if (geo.current.scaleOf(n - 1) !== slot.scale) return renderSlot(n, withText);
      }
      // Metin katmanı bir kez kurulur: konumları yüzde, yazı boyutu --scale-factor ile ölçeklenir (yakınlaştırmada yeniden kurulmaz).
      if (withText && slot.textFor == null && slot.scale) {
        slot.textFor = slot.scale;
        const pg = await getPage(n);
        const div = document.createElement('div');
        div.className = 'textLayer';
        try {
          await new pdfjs.TextLayer({ textContentSource: pg.streamTextContent(), container: div, viewport: pg.getViewport({ scale: 1 }) }).render();
          if (slots.current.get(n) !== slot) return;
          host.appendChild(div);
          slot.text = div;
        } catch {
          /* metinsiz sayfa */
        }
      }
    },
    [doc, getPage],
  );

  const evict = (n: number) => {
    const s = slots.current.get(n);
    if (!s) return;
    s.task?.cancel();
    if (s.canvas) {
      s.canvas.width = 0;
      s.canvas.remove();
    }
    s.text?.remove();
    slotEls.current.get(n)?.classList.remove('is-drawn');
    slots.current.delete(n);
    pages.current.get(n)?.then((p) => p.cleanup());
  };

  const update = useCallback(() => {
    const el = scrollRef.current;
    const { tops: t, sizes: sz } = geo.current;
    if (!el || !doc || !t.length) return;
    const top = el.scrollTop;
    const bottom = top + el.clientHeight;
    const find = (y: number) => {
      let lo = 0;
      let hi = t.length - 1;
      while (lo < hi) {
        const mid = (lo + hi + 1) >> 1;
        if (t[mid] <= y) lo = mid;
        else hi = mid - 1;
      }
      return lo;
    };
    const first = find(top);
    const last = find(bottom);
    const atEnd = top + el.clientHeight >= el.scrollHeight - 4;
    const cur = atEnd ? t.length : find(top + el.clientHeight * 0.35) + 1;
    const sk = seeking.current;
    if (sk && (cur === sk.page || Date.now() > sk.until)) seeking.current = null;
    if (!seeking.current && cur !== visible.current) {
      visible.current = cur;
      lastTarget.current = cur;
      cb.current.onVisiblePage?.(cur);
    }
    // Görünenler önce (metinle), sonra bir önceki/sonraki
    for (let i = first; i <= last; i++) renderSlot(i + 1, true);
    if (last + 1 < sz.length) renderSlot(last + 2, false);
    if (first > 0) renderSlot(first, false);
    for (const n of [...slots.current.keys()]) if (n < first + 1 - KEEP || n > last + 1 + KEEP) evict(n);
  }, [doc, renderSlot]);

  const schedule = useCallback(() => {
    cancelAnimationFrame(raf.current);
    raf.current = requestAnimationFrame(update);
  }, [update]);

  // Ölçek/genişlik değişince yeniden çiz (eski tuval yeni çizim bitene dek CSS ile ölçeklenir).
  useEffect(() => {
    schedule();
  }, [schedule, width, zoom, sizes]);

  /* ---- hedef sayfaya git ---- */
  const goTo = useCallback((p: number, smooth: boolean) => {
    const el = scrollRef.current;
    const t = geo.current.tops[p - 1];
    if (!el || t == null) return;
    seeking.current = { page: p, until: Date.now() + (smooth ? 900 : 250) };
    el.scrollTo({ top: Math.max(0, t - PAD), behavior: smooth ? 'smooth' : 'auto' });
  }, []);

  useEffect(() => {
    if (!doc) return;
    const p = Math.max(1, Math.min(doc.numPages, page || 1));
    if (lastTarget.current === p) return; // kullanıcının kaydırmasından gelen geri bildirim
    const far = Math.abs(p - visible.current) > 2 || lastTarget.current == null || !!seeking.current;
    lastTarget.current = p;
    visible.current = p;
    goTo(p, !far);
  }, [page, doc, goTo]);

  // Yakınlaştırma değişince görünen sayfa yerinde kalsın
  const prevZoom = useRef(zoom);
  useLayoutEffect(() => {
    if (prevZoom.current === zoom || !doc) return;
    prevZoom.current = zoom;
    goTo(visible.current, false);
  }, [zoom, doc, goTo]);

  // Ctrl/⌘ + tekerlek (ve dokunmatik yüzey kıstırma) ile yakınlaştırma
  const zoomRef = useRef(zoom);
  zoomRef.current = zoom;
  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    const onWheel = (e: WheelEvent) => {
      if (!e.ctrlKey && !e.metaKey) return;
      e.preventDefault();
      const z = Math.max(0.5, Math.min(3, zoomRef.current * (e.deltaY < 0 ? 1.1 : 1 / 1.1)));
      cb.current.onZoom?.(Math.round(z * 100) / 100);
    };
    el.addEventListener('wheel', onWheel, { passive: false });
    return () => el.removeEventListener('wheel', onWheel);
  }, []);

  const [hs, he] = highlight || [0, -1];

  return (
    <div className="pdv" ref={scrollRef} onScroll={schedule} tabIndex={0} aria-label="PDF sayfaları">
      {progress !== null && (
        <div className="pdv-loading" role="status">
          <span className="pdv-spin" aria-hidden />
          <span>PDF açılıyor{progress > 0 ? ` · %${progress}` : '…'}</span>
        </div>
      )}
      <div className="pdv-track" style={{ height: sizes.length ? totalH : undefined }}>
        {sizes.map((s, i) => {
          const n = i + 1;
          const sc = scaleOf(i);
          const src = n >= hs && n <= he;
          return (
            <div
              key={n}
              ref={(el) => {
                if (el) slotEls.current.set(n, el);
                else slotEls.current.delete(n);
              }}
              className={`pdv-page${src ? ' is-src' : ''}`}
              data-page={n}
              style={{ top: tops[i], width: s.w * sc, height: s.h * sc, ['--scale-factor' as any]: sc }}
            >
              {src && n === hs && <span className="pdv-src-tag">Bu adımın kaynağı</span>}
              <span className="pdv-no" aria-hidden>{n}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
