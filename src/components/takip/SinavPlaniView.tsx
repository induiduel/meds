/**
 * Sınav planı (/kamplar/sinav-plani, iç /sinav-plani): en az 60 için kişiye özel yol haritası (SinavPlani) ayrı sayfada.
 * Hızlar Bitirdiklerim ile aynı hesaptan gelir (bitirdiklerimVeri + calismaTakip.hizHesapla). Stil: styles/takip.css.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { Target } from 'lucide-react';
import { IZLEME_HIZI_MODULLER, hizHesapla, onOran, useIzlemeHizi, useTakip, type Hiz, type TakipModul } from '../../services/calismaTakip';
import { MODUL_YUKLE, kurulaGore, type BdDers } from './bitirdiklerimVeri';
import SinavPlani from './SinavPlani';
import { KurulSecici, useSeciliKurul } from '../kurul/KurulSecici';
import { icKonum } from '../../siteHaritasi';
import '../../styles/takip.css';
import V15BaslikYaz from '../v15/V15BaslikYaz';
import '../../styles/v15/kamp.css';

const MODULLER: TakipModul[] = ['sesli', 'ogren', 'cozucu', 'onem', 'kamp'];

export default function SinavPlaniView() {
  const [veriler, setVeriler] = useState<Partial<Record<TakipModul, BdDers[]>>>({});
  const takip = useTakip();
  const izHiz = useIzlemeHizi();
  const kurul = useSeciliKurul();

  useEffect(() => { document.title = 'Sınav planı · MeDSor'; }, []);
  useEffect(() => {
    let canli = true;
    for (const id of MODULLER) MODUL_YUKLE[id]().then((v) => canli && setVeriler((d) => ({ ...d, [id]: v })), () => {});
    return () => { canli = false; };
  }, []);

  const hizlar = useMemo(() => {
    const r: Partial<Record<TakipModul, Hiz>> = {};
    for (const id of MODULLER) { const v0 = veriler[id]; if (!v0) continue;
      const v = kurulaGore(v0, kurul);
      const h = hizHesapla(id, v.flatMap((d) => d.konular), takip);
      // izleme hızı girildiyse sesli modüllerin süresi yalnız o hızla (onOran zaten seçilen hızı kullanır)
      r[id] = izHiz != null && IZLEME_HIZI_MODULLER.includes(id) ? { ...h, oran: onOran(id), kaynak: 'icerik' } : h;
    }
    return r;
  }, [veriler, takip, izHiz, kurul]);
  // plan hızı değişmedikçe yeniden hesaplamasın
  const anahtar = MODULLER.map((id) => hizlar[id]?.oran.toFixed(3) ?? '-').join('|');
  const planHiz = useMemo(() => hizlar, [anahtar]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="bd">
      <header className="bd-bas">
        <span className="bd-ic" aria-hidden><Target /></span>
        <div>
          <h1>Sınav planı</h1><V15BaslikYaz baslik="Sınav planı" alt="60 için gün gün yol haritası" />
          <p>Bitirdiklerine bakarak sınavda kaç puan alacağını tahmin eder ve 60 için bugün neyi çalışman gerektiğini sıralar.</p>
        </div>
      </header>
      <KurulSecici secili={kurul} yol={(k) => `${icKonum().pathname}?kurul=${k}`} />
      <SinavPlani hiz={planHiz} kurul={kurul} />
    </div>
  );
}
