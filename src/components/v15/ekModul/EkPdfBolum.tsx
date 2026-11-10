import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import * as pdfjs from 'pdfjs-dist';
import type { PDFDocumentProxy } from 'pdfjs-dist';
import workerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import { getCustomApiUrl } from '../../../services/api';

pdfjs.GlobalWorkerOptions.workerSrc = workerUrl;

/**
 * Ders kitapçığının yalnız bir bölümünü (pdf_esle.json `k` kutusu) ekrana sığacak biçimde çizer.
 * Sayfa kırpılır: kutu + küçük pay, kabın hem genişliğine hem yüksekliğine sığan ölçekte. Kitapçığın içeriği
 * değişmez; tam sayfa görünümü (PdfDocView) ayrı kip olarak durur. Okunan satır kutunun üstünde yanar.
 */
const PAY = 0.02;
const belgeler = new Map<string, Promise<PDFDocumentProxy>>();
function belgeAl(src: string) {
  let p = belgeler.get(src);
  if (!p) {
    const base = `${getCustomApiUrl() || ''}/vendor/pdfjs/`;
    p = pdfjs.getDocument({
      url: src, rangeChunkSize: 256 * 1024, disableAutoFetch: true, disableStream: true, isEvalSupported: false,
      standardFontDataUrl: `${base}standard_fonts/`, wasmUrl: `${base}wasm/`, iccUrl: `${base}iccs/`, cMapUrl: `${base}cmaps/`, cMapPacked: true,
    }).promise;
    p.catch(() => belgeler.delete(src));
    belgeler.set(src, p);
  }
  return p;
}

export const EkPdfBolum: React.FC<{ src: string; sayfa: number; kutu: number[]; satirlar: number[][]; onError: (m: string) => void }> = ({ src, sayfa, kutu, satirlar, onError }) => {
  const kap = useRef<HTMLDivElement>(null);
  const tuval = useRef<HTMLCanvasElement>(null);
  const [olcu, setOlcu] = useState({ w: 0, h: 0 });
  const [boyut, setBoyut] = useState<{ w: number; h: number } | null>(null);
  // kırpılan bölge (sayfa oranı, 0–1)
  const x0 = Math.max(0, kutu[0] - PAY), y0 = Math.max(0, kutu[1] - PAY);
  const x1 = Math.min(1, kutu[2] + PAY), y1 = Math.min(1, kutu[3] + PAY);

  useLayoutEffect(() => {
    const el = kap.current;
    if (!el) return;
    // dar ekranda kap içeriğe göre uzar (CSS): yükseklik sınırı pencereden alınır, bölüm genişliğe tam oturur
    const olc = () => {
      const dar = el.clientWidth < 600;
      setOlcu({ w: Math.max(0, el.clientWidth - 24), h: Math.max(0, (dar ? window.innerHeight * 0.6 : el.clientHeight) - 24) });
    };
    const ro = new ResizeObserver(olc);
    ro.observe(el);
    window.addEventListener('resize', olc);
    return () => { ro.disconnect(); window.removeEventListener('resize', olc); };
  }, []);

  useEffect(() => {
    if (!olcu.w || !olcu.h) return;
    let dead = false;
    let gorev: { cancel: () => void } | null = null;
    belgeAl(src).then(async (d) => {
      const pg = await d.getPage(sayfa);
      if (dead) return;
      const v1 = pg.getViewport({ scale: 1 });
      const bw = (x1 - x0) * v1.width, bh = (y1 - y0) * v1.height;
      const olcek = Math.min(olcu.w / bw, olcu.h / bh);
      const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
      const vp = pg.getViewport({ scale: olcek * dpr });
      const c = tuval.current;
      if (!c) return;
      const cw = Math.round(bw * olcek), ch = Math.round(bh * olcek);
      const ara = document.createElement('canvas');
      ara.width = Math.round(cw * dpr);
      ara.height = Math.round(ch * dpr);
      const t = pg.render({ canvas: ara, viewport: vp, transform: [1, 0, 0, 1, -x0 * vp.width, -y0 * vp.height] });
      gorev = t;
      await t.promise;
      if (dead) return;
      c.width = ara.width;
      c.height = ara.height;
      c.getContext('2d')?.drawImage(ara, 0, 0);
      setBoyut({ w: cw, h: ch });
    }).catch((e) => { if (!dead && e?.name !== 'RenderingCancelledException') onError('Kitapçık açılamadı.'); });
    return () => { dead = true; gorev?.cancel(); };
  }, [src, sayfa, x0, y0, x1, y1, olcu.w, olcu.h, onError]);

  const yer = (b: number[]): React.CSSProperties => ({
    left: `${((b[0] - x0) / (x1 - x0)) * 100}%`, top: `${((b[1] - y0) / (y1 - y0)) * 100}%`,
    width: `${((b[2] - b[0]) / (x1 - x0)) * 100}%`, height: `${((b[3] - b[1]) / (y1 - y0)) * 100}%`,
  });
  return (
    <div className="ekm-pdfb" ref={kap}>
      <div className="ekm-pdfb-sayfa" style={boyut ? { width: boyut.w, height: boyut.h } : { visibility: 'hidden' }}>
        <canvas ref={tuval} style={boyut ? { width: boyut.w, height: boyut.h } : undefined} />
        {satirlar.map((b, i) => <span key={i} className="ekm-pdfb-satir" style={yer(b)} aria-hidden />)}
      </div>
      {!boyut && <span className="v15-skel ekm-pdf-skel" aria-hidden />}
    </div>
  );
};
