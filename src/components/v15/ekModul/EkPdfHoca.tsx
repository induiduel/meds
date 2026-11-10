import React, { Suspense, lazy, useEffect, useState } from 'react';
import { ExternalLink } from 'lucide-react';
import { gorselUrl, hocaPdfKlip, type EkModul } from './ekVeri';
import type { Sira } from './ekOrtak';

const EkPdfBolum = lazy(() => import('./EkPdfBolum').then((x) => ({ default: x.EkPdfBolum })));

/**
 * Hoca soruları · "PDF ile" sesli çözüm: çözümlü soru kitapçığında çalan sorunun bloğu ekrana sığar, o an okunan cümlenin
 * satırı yanar (soru okunurken kök ve sırayla şıklar, çözümde doğru şık ve çözüm kutusunun satırları). Eşleme önceden
 * üretilir (hoca_pdf_esle.json; scripts/ek_modul/pdf_esle_hoca.py). Ses durmuşken ekrandaki sorunun bloğu açık durur.
 */
export const EkPdfHoca: React.FC<{ m: EkModul; klipler: string[]; soru: number; sira: Sira }> = ({ m, klipler, soru, sira }) => {
  const esle = m.hocaPdf!;
  const src = `${gorselUrl(m.ozet.id, esle.pdf)}?v=${esle.bayt}`;
  const [hata, setHata] = useState('');
  const [cumle, setCumle] = useState(0);
  const e = sira.i >= 0 ? hocaPdfKlip(m, klipler[sira.i]) : null;
  const durgun = hocaPdfKlip(m, klipler[soru * 2]);
  const goster = e || durgun;

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

  const satirlar = e ? e.l[e.c[Math.min(cumle, e.c.length - 1)][1]] || [] : [];
  const cozum = sira.i >= 0 && sira.i % 2 === 1;
  return (
    <section className="ekm-pdf-kutu is-bolum v15-card ekm-hoca-pdf" aria-label="Çözümlü soru kitapçığı">
      <div className="ekm-pdf-ust">
        <b>{goster ? `Sayfa ${goster.s} · ${e ? (cozum ? 'çözüm anlatılıyor' : 'soru okunuyor') : 'çözümlü kitapçık'}` : 'Çözümlü kitapçık'}</b>
        <a className="ekm-kucuk" href={src} target="_blank" rel="noreferrer" aria-label="Kitapçığı yeni sekmede aç"><ExternalLink aria-hidden /></a>
      </div>
      {hata || !goster ? (
        <p className="ekm-bos">{hata || 'Bu sorunun kitapçık eşlemesi yok.'} <a href={src} target="_blank" rel="noreferrer">Kitapçığı yeni sekmede aç</a></p>
      ) : (
        <Suspense fallback={<span className="v15-skel ekm-pdf-skel" aria-hidden />}>
          <EkPdfBolum src={src} sayfa={goster.s} kutu={goster.k} satirlar={satirlar} onError={setHata} />
        </Suspense>
      )}
    </section>
  );
};
