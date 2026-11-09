/**
 * PDF ayar penceresinin canlı önizlemesi: örnek bir ders metni seçili ayarlarla gerçekten PDF'e dönüştürülür
 * (aynı motor: metinDisaAktar + pdfDuzen) ve ilk yaprak pdf.js ile çizilir. Ayar değişince 350 ms sonra yenilenir.
 */
import React, { useEffect, useRef, useState } from 'react';
import * as pdfjs from 'pdfjs-dist';
import workerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import type { AktarBelge } from '../../services/metinDisaAktar';
import type { PdfDuzen } from '../../services/pdfDuzen';

pdfjs.GlobalWorkerOptions.workerSrc = workerUrl;

const md = `### Hücre zedelenmesinin nedenleri
- **Oksijen eksikliği (hipoksi):** en sık nedendir; ==iskemi== kan akımının azalmasıyla oluşur.
- **Fiziksel etkenler:** travma, aşırı sıcak ya da soğuk, radyasyon.
- **Kimyasal maddeler ve ilaçlar:** küçük dozda bile hücreye zarar verebilir.

### Geri dönüşümlü zedelenme
1) Hücre şişmesi: zar pompaları bozulunca hücreye su girer.
2) Yağlı değişim: en çok ==karaciğerde== görülür.

> [!IMPORTANT] Sınavda sık sorulur: geri dönüşümsüz zedelenmenin en önemli bulgusu çekirdek değişiklikleridir.

| Bulgu | Geri dönüşümlü | Geri dönüşümsüz |
|---|---|---|
| Hücre şişmesi | Var | Var |
| Çekirdek parçalanması | Yok | Var |`;

const ORNEK: AktarBelge = {
  baslik: 'Hücre Hasarı ve Nekroz',
  alt: 'Tıbbi Patoloji · örnek sayfa',
  dersDuzeni: true,
  bolumler: [
    { baslik: 'Hücre zedelenmesi', md },
    { baslik: 'Nekroz türleri', md },
    { baslik: 'Apoptoz', md },
  ],
};

/** belge verilirse örnek yerine o belge çizilir (sesli ders dışa aktarma penceresi: dersin kendi metni) */
export default function PdfOnizleme({ d, belge }: { d: PdfDuzen; belge?: AktarBelge }) {
  const kap = useRef<HTMLDivElement>(null);
  const [sayfa, setSayfa] = useState(1);
  const [toplam, setToplam] = useState(0);
  const [yukleniyor, setYukleniyor] = useState(true);
  const anahtar = JSON.stringify(d);
  // Önizleme büyütülünce / tam ekranda kâğıt yeni genişlikte keskin çizilsin
  const [gen, setGen] = useState(0);
  useEffect(() => {
    const el = kap.current;
    if (!el || typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(([e]) => setGen(Math.round(e.contentRect.width / 40) * 40));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  useEffect(() => { setSayfa(1); }, [anahtar, belge]);

  useEffect(() => {
    let iptal = false;
    setYukleniyor(true);
    const t = setTimeout(async () => {
      try {
        const { metinDosyasi } = await import('../../services/metinDisaAktar');
        const { pdfDuzenle } = await import('../../services/pdfDuzen');
        // Sayfa aralığı önizlemede uygulanmaz (örnek belge kısa)
        const ayar = { ...d, sayfaAraligi: '' };
        const blob = await pdfDuzenle(await metinDosyasi(belge || ORNEK, 'pdf', ayar), ayar);
        const doc = await pdfjs.getDocument({ data: new Uint8Array(await blob.arrayBuffer()) }).promise;
        if (iptal) return;
        setToplam(doc.numPages);
        const p = await doc.getPage(Math.min(sayfa, doc.numPages));
        const el = kap.current;
        if (!el || iptal) return;
        const gen = el.clientWidth || 260;
        const v1 = p.getViewport({ scale: 1 });
        const oran = window.devicePixelRatio || 1;
        const vp = p.getViewport({ scale: (gen / v1.width) * oran });
        const c = document.createElement('canvas');
        c.width = vp.width; c.height = vp.height;
        c.style.width = '100%'; c.style.height = 'auto';
        await p.render({ canvasContext: c.getContext('2d')!, viewport: vp, canvas: c }).promise;
        if (iptal) return;
        el.replaceChildren(c);
        doc.destroy();
      } catch (e) { console.warn('pdf önizleme', e); }
      finally { if (!iptal) setYukleniyor(false); }
    }, 350);
    return () => { iptal = true; clearTimeout(t); };
  }, [anahtar, sayfa, belge, gen]);

  return (
    <figure className="pdo">
      <div className={`pdo-kagit${yukleniyor ? ' is-yuk' : ''}`} ref={kap} aria-label="Seçili ayarlarla örnek sayfa" role="img" />
      <figcaption className="pdo-alt">
        <button type="button" disabled={sayfa <= 1} onClick={() => setSayfa((s) => s - 1)} aria-label="Önceki sayfa">‹</button>
        <span>{toplam ? `${belge ? 'Sayfa' : 'Örnek sayfa'} ${sayfa} / ${toplam}` : 'Önizleme hazırlanıyor…'}</span>
        <button type="button" disabled={!toplam || sayfa >= toplam} onClick={() => setSayfa((s) => s + 1)} aria-label="Sonraki sayfa">›</button>
      </figcaption>
    </figure>
  );
}
