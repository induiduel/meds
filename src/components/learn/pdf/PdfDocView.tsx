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
import React, { memo, useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { CizimLayer, type CizimKomut } from './CizimLayer';
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
  /** Okunan cümlenin slayttaki karşılığı (önceden hizalanmış kutular, sayfa oranı 0–1): satırlar hafif, okunan kelime/resim lazerle */
  marks?: PdfMarks | null;
  /** Yakında gösterilecek sayfalar (canlı derste sıradaki cümlelerin slaytları): önceden çizilir, atlamada hazırdır */
  preload?: number[];
  /** Sayfa başına kalıcı vurgu (öğrenci notunda işaretli yerler): kırmızı marker kutuları + köşede tek yıldız */
  notes?: Record<string, { l: number[][]; y?: number[]; b?: number[][] }> | null;
  onSearch?: (r: { hits: PdfSearchHit[]; done: boolean } | null) => void;
  /** Sayfa üstü katman (ör. çizim tuvali); yalnız görünen sayfa ±2 için kurulur */
  pageOverlay?: (page: number) => React.ReactNode;
  /** sayfa altına eklenecek boş alan (sayfa yüksekliği oranı) ve zemin rengi: sayfaya sığmayan çizim paneli buraya
   *  konur (cizim_uret ek_alt). Sayfanın kendi kutusu ve işaret koordinatları değişmez; alan sayfanın altına eklenir. */
  ekAlt?: Record<number, { h: number; renk?: string }> | null;
}

export interface PdfMarks {
  page: number;
  kind: 'metin' | 'tablo' | 'kelime' | 'resim' | 'sayfa';
  /** ≥%80'i okunan madde satırları / resim kutusu [x0, y0, x1, y1] (sayfa oranı) */
  lines: number[][];
  /** slaytta karşılığı olan kelimelerin kutuları */
  words: number[][];
  /** o an konuşulan kelimenin words dizini (-1: yok). Yalnız işaret katmanını yeniden çizer. */
  useFocus?: () => number;
  /** hareketli imleç: [[cümle içi karakter, x, y]]; useChar o an konuşulan karakteri verir */
  path?: number[][];
  useChar?: () => number;
  /** canlı çizim komutları (R6, CizimLayer): kontur / akış / eğri fazı / şema; ilerleme useChar'dan */
  cizim?: CizimKomut[];
}

/** İmleç: konuşulan karakter iki yol noktası arasında ilerledikçe akıcı biçimde kayar (anlatan hocanın eli gibi);
 *  noktaya varınca bölgeyi (r) elle çizer gibi çevreler — geniş/alçak bölgenin altını çizer —, beklerken küçük daireler atar. */
function imlecDurum(path: number[][], c: number): { x: number; y: number; i: number } {
  if (c < 0 || c <= path[0][0]) return { x: path[0][1], y: path[0][2], i: 0 };
  for (let i = 0; i + 1 < path.length; i++) {
    const a = path[i], b = path[i + 1];
    if (c < b[0]) {
      // noktada kısa duruş (çevreleme), sonra bir sonraki noktaya erkenden süzülme
      const span = Math.max(1, b[0] - a[0]);
      const o = Math.max(0, Math.min(1, ((c - a[0]) / span - 0.55) / 0.45));
      const e = o * o * (3 - 2 * o);
      return { x: a[1] + (b[1] - a[1]) * e, y: a[2] + (b[2] - a[2]) * e, i: e > 0.5 ? i + 1 : i };
    }
  }
  const z = path[path.length - 1];
  return { x: z[1], y: z[2], i: path.length - 1 };
}

/** Halka bölgeyi içten kesmesin: dikdörtgeni dıştan saran elips kutusu (√2 büyütme + küçük pay) */
const halka = (r: number[]) => {
  const w = r[2] - r[0], h = r[3] - r[1], ex = w * 0.23 + 0.006, ey = h * 0.23 + 0.006;
  return [r[0] - ex, r[1] - ey, r[2] + ex, r[3] + ey];
};

const Imlec = memo(function Imlec({ path, useChar }: { path: number[][]; useChar: () => number }) {
  const { x, y, i } = imlecDurum(path, useChar());
  const n = path[i];
  const r = n && n.length >= 7 ? n.slice(3, 7) : null;
  const alt = r ? (r[2] - r[0]) > 3.2 * (r[3] - r[1]) : false; // geniş, alçak bölge (satır) → altını çiz
  return (
    <>
      {r && (
        <svg key={`c${i}`} className={`pdv-cizim${alt ? ' is-alt' : ''}`} style={alt ? pct(r) : pct(halka(r))} viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden>
          {alt
            ? <path d="M-1 112 Q 30 108, 55 112 T 101 110" pathLength={1} />
            : <path d="M50 1 C 78 1, 99 22, 99 50 C 99 78, 78 99, 50 99 C 22 99, 1 78, 1 50 C 1 22, 22 1, 54 2" pathLength={1} />}
        </svg>
      )}
      <span className="pdv-imlec-kap" style={{ left: `${x * 100}%`, top: `${y * 100}%` }}>
        <svg key={`i${i}`} className="pdv-imlec" width="11" height="11" viewBox="0 0 24 24" aria-hidden>
          <path d="M3 2l7.5 19 2.6-7.9L21 10.5z" />
        </svg>
      </span>
    </>
  );
});

const pct = (b: number[]) => ({ left: `${b[0] * 100}%`, top: `${b[1] * 100}%`, width: `${(b[2] - b[0]) * 100}%`, height: `${(b[3] - b[1]) * 100}%` });
const noFocus = () => -1;

/** Metin: madde zemini + konuşulan kelimenin zemini/altı. Lazer yalnız metni olmayan yerde (resim/şekil). */
/** Öğrenci notu katmanı: işaretli yerlerin üstünde kırmızı marker, sayfada önemli bir yer olduğunu gösteren tek yıldız */
const NotLayer = memo(function NotLayer({ n }: { n: { l: number[][]; y?: number[]; b?: number[][] } }) {
  return (
    <div className="pdv-not" aria-hidden>
      {n.l.map((b, i) => <span key={i} className="pdv-not-m" style={pct(b)} />)}
      {n.b?.map((p, i) => <span key={`b${i}`} className="pdv-not-b" style={{ left: `${p[0] * 100}%`, top: `${p[1] * 100}%` }}>★</span>)}
      {n.y && <span className="pdv-not-y" style={{ left: `${n.y[0] * 100}%`, top: `${n.y[1] * 100}%` }} title="Öğrenci notunda önemli işaretli">★</span>}
    </div>
  );
});

const MarkLayer = memo(function MarkLayer({ m }: { m: PdfMarks }) {
  const fi = (m.useFocus || noFocus)();
  const f = fi >= 0 ? m.words[fi] : null;
  const r = m.kind === 'resim' && !m.path ? m.lines[0] : null;
  return (
    <div className={`pdv-marks is-${m.kind}${m.path ? ' has-yol' : ''}`} aria-hidden>
      {m.lines.map((b, i) => <span key={i} className="pdv-mark-line" style={pct(b)} />)}
      {f && <span className="pdv-mark-word" style={pct(f)} />}
      {m.path && m.useChar && <Imlec path={m.path} useChar={m.useChar} />}
      {m.cizim?.length && m.useChar ? <CizimLayer z={m.cizim} useChar={m.useChar} /> : null}
      {r && <span className="pdv-laser" style={{ left: `${((r[0] + r[2]) / 2) * 100}%`, top: `${((r[1] + r[3]) / 2) * 100}%` }} />}
    </div>
  );
});

export interface PdfSearchHit {
  page: number;
  snippet: string;
}

const norm = (t: string) => t.toLocaleLowerCase('tr').replace(/\s+/g, ' ');

const GAP = 12;
const PAD = 12;
// Telefon/az bellekli cihaz: her tuval GPU belleğinde piksel × 4 bayt tutar; yakınlaştırmada 12 MP × 10 tuval
// (~500 MB) telefonda GPU sürecini düşürüp ekranı simsiyah bırakıyordu. Orada tuval tavanı ve tutulan sayfa az.
const LOW_END =
  typeof window !== 'undefined' &&
  (window.matchMedia?.('(pointer: coarse)').matches || ((navigator as any).deviceMemory ?? 8) <= 4);
const MAX_CANVAS_PX = LOW_END ? 3_000_000 : 12_000_000; // iOS tuval sınırının altında
const KEEP = LOW_END ? 1 : 4; // görünür aralığın dışında tutulacak çizili sayfa
const MAX_PRELOAD = LOW_END ? 2 : Infinity; // ön çizim (preload) tavanı

interface Slot {
  canvas?: HTMLCanvasElement;
  text?: HTMLDivElement;
  scale?: number; // çizildiği ölçek
  task?: RenderTask | null;
  textFor?: number; // metin katmanı kuruldu (döndürme)
}

export default function PdfDocView({ src, page, highlight, highlightLabel = 'Bu adımın kaynağı', zoom, onZoom, onVisiblePage, onLoaded, onError, fit = 'width', rotation = 0, thumbs = false, query = '', onSearch, marks = null, preload, notes = null, pageOverlay, ekAlt = null }: PdfDocViewProps) {
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
    // Küçük dosya (≤15 MB, boyut akış adresindeki ?v= değerinde): ilk sayfa aralık isteğiyle hemen açılır, kalanı arka
    // planda iner — sonraki sayfalar ağ gidiş-dönüşü beklemeden çizilir. Büyük dosyada yalnız çizilen sayfaların baytları.
    let boyut = 0;
    try { boyut = Number(new URL(src, location.href).searchParams.get('v')) || 0; } catch { /* blob: */ }
    const task = pdfjs.getDocument({
      url: src,
      rangeChunkSize: 512 * 1024,
      disableAutoFetch: !(boyut > 0 && boyut <= 15 * 1024 * 1024),
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
  const ekOf = (i: number) => (!rot && ekAlt?.[i + 1]?.h) || 0;
  const tops: number[] = [];
  let acc = PAD;
  dims.forEach((s, i) => {
    tops.push(acc);
    acc += s.h * scaleOf(i) * (1 + ekOf(i)) + GAP;
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
          host.dataset.drawn = '1'; // sınıf değil: React className'i yeniden yazınca silinmesin
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
    { const h = slotEls.current.get(n); if (h) delete h.dataset.drawn; }
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
    // Ön çizim: görünenler bittikten sonra sıradaki slaytlar (metin katmanı görünür olunca kurulur)
    const on = new Set((preloadRef.current || []).filter((n) => n >= 1 && n <= sz.length).slice(0, MAX_PRELOAD));
    for (const n of on) renderSlot(n, false);
    for (const n of [...slots.current.keys()]) if ((n < first + 1 - KEEP || n > last + 1 + KEEP) && !on.has(n)) evict(n);
  }, [doc, renderSlot]);

  // Kare döngüsü kısılırsa (gömülü pencere, güç tasarrufu) çizim planı 120 ms sonra zamanlayıcıyla yine çalışır
  const tmo = useRef(0);
  const schedule = useCallback(() => {
    cancelAnimationFrame(raf.current);
    clearTimeout(tmo.current);
    raf.current = requestAnimationFrame(() => { clearTimeout(tmo.current); update(); });
    tmo.current = window.setTimeout(() => { cancelAnimationFrame(raf.current); update(); }, 120);
  }, [update]);
  useEffect(() => () => clearTimeout(tmo.current), []);
  // Sekmeye dönülünce (arka planda dinlenirken sayfa değişmiş olabilir) hemen yeniden planla
  useEffect(() => {
    const f = () => { if (document.visibilityState === 'visible') schedule(); };
    document.addEventListener('visibilitychange', f);
    return () => document.removeEventListener('visibilitychange', f);
  }, [schedule]);
  const preloadRef = useRef(preload);
  preloadRef.current = preload;
  const preloadKey = (preload || []).join(',');
  useEffect(() => { if (preloadKey) schedule(); }, [preloadKey, schedule]);

  // Ölçek/genişlik değişince yeniden çiz (eski tuval yeni çizim bitene dek CSS ile ölçeklenir).
  useEffect(() => {
    schedule();
  }, [schedule, width, height, zoom, sizes, fit, rot]);

  // Anlatılan satırlar alttaki oynatıcının (kayan alanın scroll-padding-bottom'u) ya da görünür alanın altında kalmasın:
  // gerekirse yalnız yetecek kadar kaydır (kullanıcı 2026-10-24: oynatıcı "monitörizasyon" satırını örtüyordu)
  const isaretAnahtar = marks && !rot ? `${marks.page}|${marks.lines.map((b) => b.join(',')).join(';')}` : '';
  useEffect(() => {
    const el = scrollRef.current;
    if (!el || !marks || rot || !marks.lines.length) return;
    const i = marks.page - 1;
    const t = geo.current.tops[i];
    const d = geo.current.sizes[i];
    if (t == null || !d) return;
    const h = d.h * geo.current.scaleOf(i);
    const ust = t + Math.min(...marks.lines.map((b) => b[1])) * h;
    const alt = t + Math.max(...marks.lines.map((b) => b[3])) * h;
    const altPay = parseFloat(getComputedStyle(el).scrollPaddingBottom) || 0;
    // sayfa geçişindeki yumuşak kaydırma (goTo, ≤900 ms) bitince ölç
    const id = window.setTimeout(() => {
      const gorAlt = el.scrollTop + el.clientHeight - altPay - 12;
      if (alt > gorAlt) el.scrollTo({ top: Math.max(0, Math.min(ust - 24, el.scrollTop + (alt - gorAlt))), behavior: 'smooth' });
      else if (ust < el.scrollTop + 8) el.scrollTo({ top: Math.max(0, ust - 24), behavior: 'smooth' });
    }, 950);
    return () => window.clearTimeout(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isaretAnahtar]);

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
              className={`pdv-page${src ? ' is-src' : ''}${ekOf(i) ? ' has-ek' : ''}`}
              data-page={n}
              style={{ top: tops[i], width: s.w * sc, height: s.h * sc, ['--scale-factor' as any]: sc,
                       ...(ekOf(i) ? { ['--ek-h' as any]: `${s.h * sc * ekOf(i)}px`, ['--ek-renk' as any]: ekAlt?.[n]?.renk || '#fff' } : null) }}
            >
              {ekOf(i) ? <span className="pdv-page-ek" aria-hidden /> : null}
              {src && n === hs && <span className="pdv-src-tag">{highlightLabel}</span>}
              {notes?.[n] && !rot && <NotLayer n={notes[n]} />}
              {marks && marks.page === n && !rot && <MarkLayer m={marks} />}
              {pageOverlay && !rot && Math.abs(n - current) <= 2 && pageOverlay(n)}
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
