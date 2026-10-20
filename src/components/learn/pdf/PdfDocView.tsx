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
  /** Vurgulanan ilk sayfanın etiketi (varsayılan: "Bu adımın kaynağı") */
  highlightLabel?: string;
  /** 1 = sayfa genişliğine sığdır */
  zoom: number;
  onZoom?: (z: number) => void;
  onVisiblePage?: (p: number) => void;
  onLoaded?: (numPages: number) => void;
  onError?: (message: string) => void;
  /** width: sayfa genişliğe sığar; page: sayfanın tamamı görünür */
  fit?: 'width' | 'page';
  /** Ek döndürme (0/90/180/270) */
  rotation?: number;
  /** Solda küçük sayfa önizlemeleri */
  thumbs?: boolean;
  /** Metin araması (≥2 harf); eşleşen sayfalar onSearch ile bildirilir, görünen sayfalarda vurgulanır */
  query?: string;
  /** Okunan cümle: vurgulu sayfadaki metin katmanında kelime örtüşmesiyle hafifçe işaretlenir */
  follow?: string;
  onSearch?: (r: { hits: PdfSearchHit[]; done: boolean } | null) => void;
}

export interface PdfSearchHit {
  page: number;
  snippet: string;
}

const norm = (t: string) => t.toLocaleLowerCase('tr').replace(/\s+/g, ' ');

const GAP = 12;
const PAD = 12;
const MAX_CANVAS_PX = 12_000_000; // iOS tuval sınırının altında
const KEEP = 4; // görünür aralığın dışında tutulacak çizili sayfa

interface Slot {
  canvas?: HTMLCanvasElement;
  text?: HTMLDivElement;
  scale?: number; // çizildiği ölçek
  task?: RenderTask | null;
  textFor?: number; // metin katmanı kuruldu (döndürme)
}

export default function PdfDocView({ src, page, highlight, highlightLabel = 'Bu adımın kaynağı', zoom, onZoom, onVisiblePage, onLoaded, onError, fit = 'width', rotation = 0, thumbs = false, query = '', onSearch, follow = '' }: PdfDocViewProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [doc, setDoc] = useState<PDFDocumentProxy | null>(null);
  const [sizes, setSizes] = useState<{ w: number; h: number }[]>([]);
  const [width, setWidth] = useState(0);
  const [height, setHeight] = useState(0);
  const [current, setCurrent] = useState(1);
  const rot = ((rotation % 360) + 360) % 360;
  const texts = useRef(new Map<number, string>());
  const q = query.trim().length >= 2 ? norm(query.trim()) : '';
  const qRef = useRef(q);
  qRef.current = q;
  const fRef = useRef({ page: 0, words: new Set<string>() });
  fRef.current = { page: highlight ? highlight[0] : 0, words: followWords(follow) };
  const [progress, setProgress] = useState<number | null>(0);
  const slots = useRef(new Map<number, Slot>());
  const slotEls = useRef(new Map<number, HTMLDivElement>());
  const pages = useRef(new Map<number, Promise<PDFPageProxy>>());
  const visible = useRef(1);
  const lastTarget = useRef<number | null>(null);
  /** Programatik kaydırma sürerken ara sayfalar "görünen sayfa" diye geri bildirilmez (hedefi ezmesin). */
  const seeking = useRef<{ page: number; until: number } | null>(null);
  const raf = useRef(0);
  const anchor = useRef<{ i: number; frac: number } | null>(null);
  const cb = useRef({ onVisiblePage, onLoaded, onError, onZoom, onSearch });
  cb.current = { onVisiblePage, onLoaded, onError, onZoom, onSearch };

  /* ---- belge ---- */
  useEffect(() => {
    let dead = false;
    setDoc(null);
    setSizes([]);
    setProgress(0);
    slots.current.clear();
    pages.current.clear();
    texts.current.clear();
    lastTarget.current = null;
    anchor.current = null;
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

  /* ---- yerleşim ---- */
  useLayoutEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    const ro = new ResizeObserver(() => {
      setWidth(el.clientWidth);
      setHeight(el.clientHeight);
    });
    ro.observe(el);
    setWidth(el.clientWidth);
    setHeight(el.clientHeight);
    return () => ro.disconnect();
  }, []);

  const avail = Math.max(120, width - PAD * 2);
  const availH = Math.max(120, height - PAD * 2);
  // Döndürülmüş boyutlar (90/270'te en ve boy yer değiştirir)
  const dims = rot % 180 ? sizes.map((s) => ({ w: s.h, h: s.w })) : sizes;
  const scaleOf = (i: number) => {
    const d = dims[i];
    if (!d) return 1;
    const base = fit === 'page' ? Math.min(avail / d.w, availH / d.h) : avail / d.w;
    return base * zoom;
  };
  const tops: number[] = [];
  let acc = PAD;
  dims.forEach((s, i) => {
    tops.push(acc);
    acc += s.h * scaleOf(i) + GAP;
  });
  const totalH = acc + PAD - GAP;
  const geo = useRef({ tops, sizes: dims, scaleOf, rot });
  geo.current = { tops, sizes: dims, scaleOf, rot };

  /* ---- çizim ---- */
  const renderSlot = useCallback(
    async (n: number, withText: boolean) => {
      const host = slotEls.current.get(n);
      if (!host || !doc) return;
      const scale = geo.current.scaleOf(n - 1);
      const r = geo.current.rot;
      const key = scale * 1000 + r; // ölçek + döndürme
      const slot = slots.current.get(n) || {};
      slots.current.set(n, slot);
      if (slot.scale !== key && !slot.task) {
        const pg = await getPage(n);
        if (slots.current.get(n) !== slot) return; // bu arada bırakıldı
        const rawVp = pg.getViewport({ scale: 1 });
        setSizes((old) => {
          const cur = old[n - 1];
          if (!cur || (Math.abs(cur.w - rawVp.width) < 0.5 && Math.abs(cur.h - rawVp.height) < 0.5)) return old;
          const next = old.slice();
          next[n - 1] = { w: rawVp.width, h: rawVp.height };
          return next;
        });
        const vp = pg.getViewport({ scale, rotation: (pg.rotate + r) % 360 });
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
          slot.scale = key;
          host.classList.add('is-drawn');
        } catch {
          canvas.width = 0; // iptal edildi
        } finally {
          slot.task = null;
        }
        // Ölçek bu arada değiştiyse yeniden
        if (geo.current.scaleOf(n - 1) * 1000 + geo.current.rot !== slot.scale) return renderSlot(n, withText);
      }
      // Metin katmanı döndürme başına bir kez kurulur: konumları yüzde, yazı boyutu --scale-factor ile ölçeklenir (yakınlaştırmada yeniden kurulmaz).
      if (withText && slot.textFor !== r && slot.scale) {
        slot.textFor = r;
        slot.text?.remove();
        slot.text = undefined;
        const pg = await getPage(n);
        const div = document.createElement('div');
        div.className = 'textLayer';
        try {
          await new pdfjs.TextLayer({ textContentSource: pg.streamTextContent(), container: div, viewport: pg.getViewport({ scale: 1, rotation: (pg.rotate + r) % 360 }) }).render();
          if (slots.current.get(n) !== slot || slot.textFor !== r) return;
          host.appendChild(div);
          slot.text = div;
          markHits(div, qRef.current);
          if (n === fRef.current.page) markFollow(div, fRef.current.words);
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
    const p = pages.current.get(n);
    if (p) {
      p.then((pg) => pg.cleanup()).catch(() => {});
      if (n !== 1) pages.current.delete(n);
    }
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
    const ph = (sz[first]?.h ?? 1) * geo.current.scaleOf(first);
    anchor.current = { i: first, frac: Math.max(0, (top - t[first]) / (ph + GAP)) };
    const atEnd = top + el.clientHeight >= el.scrollHeight - 4;
    const cur = atEnd ? t.length : find(top + el.clientHeight * 0.35) + 1;
    const sk = seeking.current;
    if (sk && (cur === sk.page || Date.now() > sk.until)) seeking.current = null;
    if (!seeking.current && cur !== visible.current) {
      visible.current = cur;
      setCurrent(cur);
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
  }, [schedule, width, height, zoom, sizes, fit, rot]);

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
    setCurrent(p);
    goTo(p, !far);
  }, [page, doc, goTo]);

  // Yakınlaştırma değişince görünen sayfa yerinde kalsın
  // Yakınlaştırma, sığdırma, döndürme ya da alan genişliği (yan yana ayraç) değişince okunan yer kaymasın:
  // en üstteki sayfa ve o sayfadaki oransal konum korunur.
  const prevGeo = useRef('');
  useLayoutEffect(() => {
    const k = `${zoom}|${fit}|${rot}|${width}|${height}|${sizes.length}`;
    const was = prevGeo.current;
    prevGeo.current = k;
    const el = scrollRef.current;
    const a = anchor.current;
    if (!was || was === k || !doc || !el || !a) return;
    const t = tops[a.i];
    if (t == null) return;
    const ph = dims[a.i].h * scaleOf(a.i);
    el.scrollTop = t + a.frac * (ph + GAP);
  });

  /* ---- okunan cümlenin slayttaki karşılığı ---- */
  const followKey = fRef.current.page + '|' + [...fRef.current.words].join(' ');
  useEffect(() => {
    const { page: fp, words } = fRef.current;
    for (const [n, s] of slots.current) if (s.text) markFollow(s.text, n === fp ? words : new Set());
  }, [followKey]);

  /* ---- arama ---- */
  useEffect(() => {
    for (const s of slots.current.values()) if (s.text) markHits(s.text, q);
    if (!doc || !q) {
      cb.current.onSearch?.(null);
      return;
    }
    let dead = false;
    (async () => {
      const hits: PdfSearchHit[] = [];
      for (let i = 1; i <= doc.numPages && !dead; i++) {
        let str = texts.current.get(i);
        if (str == null) {
          try {
            const tc = await (await getPage(i)).getTextContent();
            str = (tc.items as any[]).map((it) => ('str' in it ? it.str : '')).join(' ').replace(/\s+/g, ' ');
          } catch {
            str = '';
          }
          texts.current.set(i, str);
        }
        const at = norm(str).indexOf(q);
        if (at >= 0) {
          const a = Math.max(0, at - 36);
          hits.push({ page: i, snippet: (a > 0 ? '…' : '') + str.slice(a, at + q.length + 64).trim() });
        }
        if (i % 8 === 0 && !dead) cb.current.onSearch?.({ hits: [...hits], done: false });
      }
      if (!dead) cb.current.onSearch?.({ hits, done: true });
    })();
    return () => {
      dead = true;
    };
  }, [q, doc, getPage]);

  // Ctrl/⌘ + tekerlek (ve dokunmatik yüzey kıstırma) ile yakınlaştırma
  const zoomRef = useRef(zoom);
  zoomRef.current = zoom;
  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    const onWheel = (e: WheelEvent) => {
      if (!e.ctrlKey && !e.metaKey) return;
      e.preventDefault();
      const z = Math.max(0.5, Math.min(4, zoomRef.current * (e.deltaY < 0 ? 1.1 : 1 / 1.1)));
      cb.current.onZoom?.(Math.round(z * 100) / 100);
    };
    el.addEventListener('wheel', onWheel, { passive: false });
    return () => el.removeEventListener('wheel', onWheel);
  }, []);

  const [hs, he] = highlight || [0, -1];

  return (
    <>
    {thumbs && doc && (
      <PdfThumbs doc={doc} getPage={getPage} dims={dims} rot={rot} current={current} onPick={(p) => { lastTarget.current = p; visible.current = p; setCurrent(p); goTo(p, false); cb.current.onVisiblePage?.(p); }} />
    )}
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
              {src && n === hs && <span className="pdv-src-tag">{highlightLabel}</span>}
              <span className="pdv-no" aria-hidden>{n}</span>
            </div>
          );
        })}
      </div>
    </div>
    </>
  );
}

/** Metin katmanında aranan ifadeyi içeren parçaları işaretler (parça içi; satırlar arası eşleşmeler sayfa düzeyinde bulunur). */
function markHits(layer: HTMLElement, q: string) {
  let first: HTMLElement | null = null;
  layer.querySelectorAll<HTMLElement>('span').forEach((sp) => {
    const hit = !!q && !sp.children.length && norm(sp.textContent || '').includes(q);
    sp.classList.toggle('is-hit', hit);
    if (hit && !first) first = sp;
  });
  return first;
}

// Kelime kökü: Türkçe ekler için ilk 5 harf yeterince ayırt edici
const stem = (w: string) => w.slice(0, 5);
const STOP = new Set(['için', 'ancak', 'gibi', 'daha', 'olan', 'olarak', 'veya', 'yani', 'ise', 'ile', 'bir', 'her', 'bu', 'şu', 've', 'de', 'da']);
function wordsOf(t: string) {
  return (t.toLocaleLowerCase('tr').match(/[\p{L}\p{N}]+/gu) || []).filter((w) => w.length >= 3 && !STOP.has(w));
}
function followWords(t: string) {
  return new Set(wordsOf(t).map(stem));
}
/** Satır, kelimelerinin yarısı (en az 1, uzun satırda 2) okunan cümlede geçiyorsa işaretlenir */
function markFollow(layer: HTMLElement, words: Set<string>) {
  layer.querySelectorAll<HTMLElement>('span').forEach((sp) => {
    let on = false;
    if (words.size && !sp.children.length) {
      const ws = wordsOf(sp.textContent || '');
      const hit = ws.filter((w) => words.has(stem(w))).length;
      on = hit >= (ws.length > 3 ? 2 : 1) && hit / ws.length >= 0.5;
    }
    sp.classList.toggle('is-follow', on);
  });
}

const THUMB_W = 92;

/** Küçük sayfa önizlemeleri: görünür olanlar düşük çözünürlükte bir kez çizilir. */
function PdfThumbs({ doc, getPage, dims, rot, current, onPick }: {
  doc: PDFDocumentProxy;
  getPage: (n: number) => Promise<PDFPageProxy>;
  dims: { w: number; h: number }[];
  rot: number;
  current: number;
  onPick: (p: number) => void;
}) {
  const listRef = useRef<HTMLDivElement>(null);
  const drawn = useRef(new Map<number, number>()); // sayfa → çizildiği döndürme

  useEffect(() => {
    const list = listRef.current;
    if (!list) return;
    const io = new IntersectionObserver(
      (ents) => {
        for (const e of ents) {
          if (!e.isIntersecting) continue;
          const host = e.target as HTMLElement;
          const n = Number(host.dataset.page);
          if (drawn.current.get(n) === rot) continue;
          drawn.current.set(n, rot);
          getPage(n).then(async (pg) => {
            const vp1 = pg.getViewport({ scale: 1, rotation: (pg.rotate + rot) % 360 });
            const dpr = Math.min(window.devicePixelRatio || 1, 2);
            const vp = pg.getViewport({ scale: (THUMB_W / vp1.width) * dpr, rotation: (pg.rotate + rot) % 360 });
            const c = document.createElement('canvas');
            c.width = Math.floor(vp.width);
            c.height = Math.floor(vp.height);
            try {
              await pg.render({ canvas: c, viewport: vp }).promise;
              host.querySelector('canvas')?.remove();
              host.prepend(c);
            } catch {
              drawn.current.delete(n);
            }
          });
        }
      },
      { root: list, rootMargin: '200px 0px' },
    );
    list.querySelectorAll('.pdv-thumb-c').forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, [doc, getPage, rot, dims.length]);

  // Geçerli sayfa önizlemesi görünür kalsın
  useEffect(() => {
    const el = listRef.current?.querySelector<HTMLElement>(`[data-thumb="${current}"]`);
    const list = listRef.current;
    if (!el || !list) return;
    const top = el.offsetTop - list.offsetTop;
    if (top < list.scrollTop || top + el.offsetHeight > list.scrollTop + list.clientHeight) list.scrollTo({ top: top - list.clientHeight / 3 });
  }, [current]);

  return (
    <div className="pdv-thumbs" ref={listRef} aria-label="Sayfa önizlemeleri">
      {dims.map((d, i) => {
        const n = i + 1;
        return (
          <button key={n} type="button" data-thumb={n} className={`pdv-thumb${n === current ? ' is-on' : ''}`} onClick={() => onPick(n)} aria-label={`Sayfa ${n}`} aria-current={n === current ? 'page' : undefined}>
            <span className="pdv-thumb-c" data-page={n} style={{ width: THUMB_W, height: Math.round((THUMB_W * d.h) / d.w) }} />
            <small>{n}</small>
          </button>
        );
      })}
    </div>
  );
}
