import React, { useState } from 'react';
import { Copy, LineChart, List } from 'lucide-react';
import { Sheet } from '../ui/Sheet';
import { Atif, CizgiGrafik, EkAtif, MaddeAgaci, MiniMetin, useMaddeKopyala } from './SaglikOrtak';
import { degerBirim, seriMaddeleri, yillikMi, type GecmisIstek, type MaddeOge } from './saglikBaglam';

/**
 * Geçmiş yıllar penceresi: gösterge kutusuna dokununca açılır. Üstte eğilim grafiği (yalnız tek yıllık noktalar),
 * altında yıl yıl madde listesi (değer, bir önceki yıla göre değişim, nokta başına kaynak). İki seri varsa
 * (ör. Karabük + Türkiye) liste yıl başına iki değer gösterir. "Kopyala" maddeleri kaynak numaralarıyla panoya yazar.
 * Pencere AtifSaglayici'nin içinde çizilir (portal React bağlamını korur) → atıf numaraları sayfadakiyle aynıdır.
 */
export const GecmisPencere: React.FC<{ istek: GecmisIstek | null; onClose: () => void }> = ({ istek, onClose }) => {
  const [gorunum, setGorunum] = useState<'ikisi' | 'liste'>('ikisi');
  const kopyala = useMaddeKopyala();
  const g = istek;
  const maddeler: MaddeOge[] = !g ? [] : g.seriler.length === 1
    ? seriMaddeleri(g.seriler[0].seri, g.birim, g.ondalik)
    : birlesikMaddeler(g);
  // Grafik en çok iki seri (vurgu + nötr); daha fazlası (ör. sektörler) yalnız listede
  const yillikVar = !!g && g.seriler.length <= 2 && g.seriler.some((s) => s.seri.filter(yillikMi).length >= 2);
  const tum = g ? g.seriler[0].seri.filter((p) => typeof p.deger === 'number') : [];
  const yillar = tum.map((p) => String(p.yil)).sort();
  return (
    <Sheet
      open={!!istek}
      onClose={onClose}
      title={g?.baslik}
      subtitle={g ? `${tum.length} değer · ${yillar[0]} – ${yillar[yillar.length - 1]}${g.birim ? ` · ${g.birim}` : ''}` : undefined}
      width={640}
      actions={g ? (
        <span className="sbk-gecmis-arac">
          {yillikVar && (
            <button type="button" className="sbk-ikon-btn" aria-pressed={gorunum === 'liste'} onClick={() => setGorunum((x) => (x === 'liste' ? 'ikisi' : 'liste'))} title={gorunum === 'liste' ? 'Grafiği de göster' : 'Yalnız madde listesi'}>
              {gorunum === 'liste' ? <LineChart aria-hidden /> : <List aria-hidden />}
            </button>
          )}
          <button type="button" className="sbk-ikon-btn" onClick={() => kopyala(g.baslik, maddeler)} title="Maddeleri kopyala" aria-label="Maddeleri kopyala"><Copy aria-hidden /></button>
        </span>
      ) : undefined}
    >
      {g && (
        <div className="sbk sbk-gecmis">
          {yillikVar && gorunum === 'ikisi' && (
            <CizgiGrafik
              baslik={g.baslik} birim={g.birim} ondalik={g.ondalik}
              seriler={g.seriler.map((s, i) => ({ ad: s.ad, seri: s.seri, ton: i === 0 ? 'vurgu' as const : 'notr' as const }))}
            />
          )}
          {g.tanim && <MiniMetin metin={g.tanim} className="sbk-muted sbk-gecmis-tanim" />}
          <h4 className="sbk-gecmis-h">Yıl yıl</h4>
          <MaddeAgaci ogeler={maddeler} />
          {g.not && <p className="sbk-not">{g.not}</p>}
          <p className="sbk-grafik-k">Kaynak <Atif id={g.kaynak} konum={g.konum} />{g.ek?.length ? <EkAtif ids={g.ek} /> : null}</p>
        </div>
      )}
    </Sheet>
  );
};

/** İki seri (il + Türkiye): yıl başına tek madde, alt maddede iki değer */
function birlesikMaddeler(g: GecmisIstek): MaddeOge[] {
  const yillar = [...new Set(g.seriler.flatMap((s) => s.seri.map((p) => String(p.yil))))].sort((a, b) => b.localeCompare(a));
  const ana = seriMaddeleri(g.seriler[0].seri, g.birim, g.ondalik);
  return yillar.map((y) => {
    const satirlar = g.seriler.map((s, i) => {
      const p = s.seri.find((x) => String(x.yil) === y);
      if (!p) return null;
      if (i === 0) {
        const m = ana.find((o) => typeof o !== 'string' && o.metin.startsWith(`**${y}**:`));
        const metin = m && typeof m !== 'string' ? m.metin.slice(y.length + 6) : String(p.deger);
        return { metin: `${s.ad}: ${metin}`, kaynak: p.kaynak, konum: p.konum } as MaddeOge;
      }
      return { metin: `${s.ad}: ${degerBirim(p.deger, g.birim, g.ondalik)}`, kaynak: p.kaynak, konum: p.konum } as MaddeOge;
    }).filter(Boolean) as MaddeOge[];
    return { metin: `**${y}**`, alt: satirlar };
  });
}
