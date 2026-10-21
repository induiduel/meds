/**
 * Sınav planı (/kamplar/sinav-plani, iç /sinav-plani): en az 60 için kişiye özel yol haritası (SinavPlani) ayrı sayfada.
 * Hızlar Bitirdiklerim ile aynı hesaptan gelir (bitirdiklerimVeri + calismaTakip.hizHesapla). Stil: styles/takip.css.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { Target } from 'lucide-react';
import { hizHesapla, useTakip, type Hiz, type TakipModul } from '../../services/calismaTakip';
import { MODUL_YUKLE, type BdDers } from './bitirdiklerimVeri';
import SinavPlani from './SinavPlani';
import '../../styles/takip.css';

const MODULLER: TakipModul[] = ['sesli', 'ogren', 'cozucu', 'onem', 'kamp'];

export default function SinavPlaniView() {
  const [veriler, setVeriler] = useState<Partial<Record<TakipModul, BdDers[]>>>({});
  const takip = useTakip();

  useEffect(() => { document.title = 'Sınav planı · MeDSor'; }, []);
  useEffect(() => {
    let canli = true;
    for (const id of MODULLER) MODUL_YUKLE[id]().then((v) => canli && setVeriler((d) => ({ ...d, [id]: v })), () => {});
    return () => { canli = false; };
  }, []);

  const hizlar = useMemo(() => {
    const r: Partial<Record<TakipModul, Hiz>> = {};
    for (const id of MODULLER) { const v = veriler[id]; if (v) r[id] = hizHesapla(id, v.flatMap((d) => d.konular), takip); }
    return r;
  }, [veriler, takip]);
  // plan hızı değişmedikçe yeniden hesaplamasın
  const anahtar = MODULLER.map((id) => hizlar[id]?.oran.toFixed(2) ?? '-').join('|');
  const planHiz = useMemo(() => hizlar, [anahtar]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="bd">
      <header className="bd-bas">
        <span className="bd-ic" aria-hidden><Target /></span>
        <div>
          <h1>Sınav planı</h1>
          <p>Bitirdiklerine ve çalışma hızına göre en az 60 için gün gün yol haritası; her adım ilgili sayfayı açar.</p>
        </div>
      </header>
      <SinavPlani hiz={planHiz} />
    </div>
  );
}
