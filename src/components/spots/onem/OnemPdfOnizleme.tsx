import React, { useEffect, useRef, useState } from 'react';
import * as pdfjs from 'pdfjs-dist';
import type { PDFDocumentProxy } from 'pdfjs-dist';
import workerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import { ChevronLeft, ChevronRight, LayoutGrid } from 'lucide-react';

pdfjs.GlobalWorkerOptions.workerSrc = workerUrl;

/**
 * Üretilen PDF'in uygulama içi önizlemesi (PDF.js; tarayıcının PDF eklentisi telefonda iframe içinde çalışmaz).
 * Izgara: küçük sayfalar yalnız görünür olunca çizilir (bellek). Sayfaya dokununca büyük görünüm; ‹ › ve ok tuşları.
 */
const Tuval: React.FC<{ doc: PDFDocumentProxy; no: number; genislik: number; root: HTMLElement | null; hemen?: boolean }> = ({ doc, no, genislik, root, hemen }) => {
  const ref = useRef<HTMLCanvasElement>(null);
  const kapRef = useRef<HTMLDivElement>(null);
  const [gorunur, setGorunur] = useState(!!hemen);
  const [oran, setOran] = useState(1.414);
  useEffect(() => {
    if (hemen) return;
    const el = kapRef.current; if (!el) return;
    const io = new IntersectionObserver((e) => { if (e.some((x) => x.isIntersecting)) { setGorunur(true); io.disconnect(); } }, { root, rootMargin: '300px' });
    io.observe(el);
    return () => io.disconnect();
  }, [root, hemen]);
  useEffect(() => {
    if (!gorunur || !genislik) return;
    let iptal = false; let gorev: { cancel: () => void } | null = null;
    doc.getPage(no).then((p) => {
      if (iptal) return;
      const v1 = p.getViewport({ scale: 1 });
      setOran(v1.height / v1.width);
      const dpr = Math.min(2.5, Math.max(1.5, window.devicePixelRatio || 1));
      const v = p.getViewport({ scale: (genislik * dpr) / v1.width });
      const c = ref.current; if (!c) return;
      c.width = Math.floor(v.width); c.height = Math.floor(v.height);
      const t = p.render({ canvas: c, viewport: v } as Parameters<typeof p.render>[0]);
      gorev = t;
      t.promise.catch(() => { /* iptal */ });
    });
    return () => { iptal = true; gorev?.cancel(); };
  }, [doc, no, genislik, gorunur]);
  return (
    <div ref={kapRef} className="op-tuval" style={{ aspectRatio: `1 / ${oran}` }}>
      <canvas ref={ref} aria-hidden />
    </div>
  );
};

export const OnemPdfOnizleme: React.FC<{ blob: Blob; sayfa: number }> = ({ blob, sayfa }) => {
  const [doc, setDoc] = useState<PDFDocumentProxy | null>(null);
  const [hata, setHata] = useState(false);
  const [buyuk, setBuyuk] = useState<number | null>(null);
  const [gen, setGen] = useState(0);
  const kapRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    let olu = false; let d: PDFDocumentProxy | null = null;
    setDoc(null); setHata(false); setBuyuk(null);
    blob.arrayBuffer().then((b) => pdfjs.getDocument({ data: new Uint8Array(b), isEvalSupported: false }).promise)
      .then((x) => { d = x; if (olu) x.destroy(); else setDoc(x); })
      .catch(() => !olu && setHata(true));
    return () => { olu = true; d?.destroy(); };
  }, [blob]);
  useEffect(() => {
    const el = kapRef.current; if (!el) return;
    let w = 0;
    const ro = new ResizeObserver((e) => { const nw = Math.round(e[0].contentRect.width); if (nw !== w) { w = nw; setGen(nw); } });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  useEffect(() => {
    if (buyuk === null) return;
    const f = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); setBuyuk((n) => Math.min(sayfa, (n || 1) + 1)); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); setBuyuk((n) => Math.max(1, (n || 1) - 1)); }
    };
    window.addEventListener('keydown', f);
    return () => window.removeEventListener('keydown', f);
  }, [buyuk, sayfa]);
  const sutun = gen >= 560 ? 3 : 2;
  const kucukW = Math.max(80, Math.floor((gen - (sutun - 1) * 12) / sutun));
  return (
    <div className="op-on" ref={kapRef}>
      {hata && <p className="op-bos">Önizleme çizilemedi; dosya yine de indirilebilir.</p>}
      {!hata && !doc && <p className="op-bos">Önizleme hazırlanıyor…</p>}
      {doc && buyuk === null && (
        <ol className="op-izgara" style={{ gridTemplateColumns: `repeat(${sutun}, minmax(0, 1fr))` }}>
          {Array.from({ length: sayfa }, (_, i) => (
            <li key={i}>
              <button type="button" onClick={() => setBuyuk(i + 1)} aria-label={`Sayfa ${i + 1}, büyüt`}>
                <Tuval doc={doc} no={i + 1} genislik={kucukW} root={kapRef.current?.closest('.op-onizleme') as HTMLElement | null} />
              </button>
              <span>{i + 1}</span>
            </li>
          ))}
        </ol>
      )}
      {doc && buyuk !== null && (
        <div className="op-buyuk">
          <div className="op-buyuk-bar">
            <button type="button" className="op-mini" onClick={() => setBuyuk(null)}><LayoutGrid aria-hidden />Tüm sayfalar</button>
            <span className="op-buyuk-no">{buyuk} / {sayfa}</span>
            <button type="button" className="op-ikon" disabled={buyuk <= 1} onClick={() => setBuyuk(buyuk - 1)} aria-label="Önceki sayfa"><ChevronLeft /></button>
            <button type="button" className="op-ikon" disabled={buyuk >= sayfa} onClick={() => setBuyuk(buyuk + 1)} aria-label="Sonraki sayfa"><ChevronRight /></button>
          </div>
          <Tuval key={buyuk} doc={doc} no={buyuk} genislik={gen} root={null} hemen />
        </div>
      )}
    </div>
  );
};

export default OnemPdfOnizleme;
