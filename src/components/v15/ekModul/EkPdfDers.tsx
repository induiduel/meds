import React, { Suspense, lazy, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ExternalLink, Minus, Plus, Volume2 } from 'lucide-react';
import type { PdfMarks } from '../../learn/pdf/PdfDocView';
import { gorselUrl, pdfKlip, type EkKonu, type EkModul } from './ekVeri';
import { EkMd, type Sira } from './ekOrtak';

const PdfDocView = lazy(() => import('../../learn/pdf/PdfDocView'));

/**
 * Sesli ders · "PDF ile" kipi: ders kitapçığı sesle birlikte ilerler (klasik sesli dersteki gibi).
 * Çalan bölümün sayfası açılır, bölüm çerçevelenir, o an anlatılan cümlenin not satırı PDF'te ve yandaki notta yanar.
 * Eşleme önceden üretilir (pdf_esle.json; scripts/ek_modul/pdf_esle.py): cümle zamanı sesteki duraklamalardan, cümle → madde
 * sözcük köküyle. Karşılığı bulunamayan cümlede satır yanmaz, yalnız bölüm çerçevesi kalır (madde uydurulmaz).
 */
const Z_MIN = 0.6, Z_MAX = 3;
const pct = (b: number[]): React.CSSProperties => ({ left: `${b[0] * 100}%`, top: `${b[1] * 100}%`, width: `${(b[2] - b[0]) * 100}%`, height: `${(b[3] - b[1]) * 100}%` });

export const EkPdfDers: React.FC<{ m: EkModul; konu: EkKonu; klipler: string[]; sira: Sira }> = ({ m, konu, klipler, sira }) => {
  const esle = m.pdfEsle!;
  const src = `${gorselUrl(m.ozet.id, esle.pdf)}?v=${esle.bayt}`;
  const [zoom, setZoom] = useState(1);
  const [hata, setHata] = useState('');
  const [gorunen, setGorunen] = useState(0);
  const [cumle, setCumle] = useState(0);
  const yan = useRef<HTMLOListElement>(null);

  // çalan klibin eşlemesi; ses durmuşken konunun ilk bölümünün sayfası açık durur
  const e = sira.i >= 0 ? pdfKlip(m, klipler[sira.i]) : null;
  const ilk = useMemo(() => klipler.map((k) => pdfKlip(m, k)).find(Boolean) || null, [m, klipler]);

  // cümle takibi: sesin anı kare kare okunur, cümle değişince bir kez çizilir
  useEffect(() => {
    setCumle(0);
    if (!e) return;
    let kare = 0;
    const tik = () => {
      const t = sira.an();
      let j = 0;
      while (j + 1 < e.c.length && t >= e.c[j + 1][0]) j++;
      setCumle(j);
      kare = requestAnimationFrame(tik);
    };
    kare = requestAnimationFrame(tik);
    return () => cancelAnimationFrame(kare);
  }, [e, sira.an]);

  const madde = e ? e.c[Math.min(cumle, e.c.length - 1)][1] : -1;
  const marks = useMemo<PdfMarks | null>(
    () => (e ? { page: e.s, kind: 'metin', lines: madde >= 0 ? e.l[madde] || [] : [], words: [] } : null),
    [e, madde],
  );
  const pageOverlay = useCallback((p: number) => (e && p === e.s ? <span className="ekm-pdf-cerceve" style={pct(e.k)} aria-hidden /> : null), [e]);

  // yandaki notlar: çalan bölüm kendi kayan alanında görünür kalır (sayfanın kendisi kaydırılmaz)
  useEffect(() => {
    const kap = yan.current, el = kap?.children[sira.i] as HTMLElement | undefined;
    if (!kap || !el || kap.scrollHeight <= kap.clientHeight) return;
    kap.scrollTo({ top: Math.max(0, el.offsetTop - kap.offsetTop - 8), behavior: 'smooth' });
  }, [sira.i]);

  const sayfa = e?.s ?? ilk?.s ?? 1;
  return (
    <div className="ekm-pdf-bolme">
      <section className="ekm-pdf-kutu v15-card" aria-label="Ders kitapçığı">
        <div className="ekm-pdf-ust">
          <b>{e ? `Sayfa ${e.s} · şu an anlatılan` : `Sayfa ${gorunen || sayfa}`}</b>
          <button type="button" className="ekm-kucuk" onClick={() => setZoom((z) => Math.max(Z_MIN, +(z - 0.2).toFixed(2)))} aria-label="Uzaklaştır"><Minus aria-hidden /></button>
          <button type="button" className="ekm-kucuk" onClick={() => setZoom((z) => Math.min(Z_MAX, +(z + 0.2).toFixed(2)))} aria-label="Yakınlaştır"><Plus aria-hidden /></button>
          <a className="ekm-kucuk" href={src} target="_blank" rel="noreferrer" aria-label="Kitapçığı yeni sekmede aç"><ExternalLink aria-hidden /></a>
        </div>
        {hata ? (
          <p className="ekm-bos">{hata} <a href={src} target="_blank" rel="noreferrer">Kitapçığı yeni sekmede aç</a></p>
        ) : (
          <Suspense fallback={<span className="v15-skel ekm-pdf-skel" aria-hidden />}>
            <PdfDocView
              key={src}
              src={src}
              page={sayfa}
              highlight={e ? [e.s, e.s] : undefined}
              highlightLabel="Şu an anlatılan"
              marks={marks}
              zoom={zoom}
              onZoom={setZoom}
              zoomMin={Z_MIN}
              zoomMax={Z_MAX}
              onVisiblePage={setGorunen}
              onError={setHata}
              pageOverlay={pageOverlay}
            />
          </Suspense>
        )}
      </section>

      <ol className="ekm-bolumler ekm-pdf-yan" role="list" ref={yan}>
        {konu.bolumler.map((b, i) => {
          const es = pdfKlip(m, klipler[i]);
          const aktif = sira.i === i;
          return (
            <li key={i} className={`v15-card${aktif ? ' is-aktif' : ''}`}>
              <div className="ekm-bolum-ust">
                <i>{i + 1}</i><h3 className={aktif && madde === 0 ? 'is-okunan' : undefined}>{b.baslik}</h3>
                {es && <small>s. {es.s}</small>}
                {sira.sesVar && (
                  <button type="button" className="ekm-kucuk" onClick={() => (aktif ? sira.dugme() : sira.cal(i))} aria-label={`${b.baslik}: buradan dinle`}>
                    <Volume2 aria-hidden />
                  </button>
                )}
              </div>
              <EkMd md={b.ekran} okunan={aktif && madde > 0 ? madde : undefined} />
            </li>
          );
        })}
      </ol>
    </div>
  );
};
