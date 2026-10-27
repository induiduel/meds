import React, { useEffect, useMemo, useState } from 'react';
import { Printer } from 'lucide-react';
import { dersIcerikGetir, dersSlaytlariGetir, type DiPaket, type DiSlayt } from './dersIcerik';
import { dersPdfAkisi } from './dersPdfAkis';
import DersPdfBelge from './DersPdfBelge';
import '../../styles/v15/dersPdf.css';
import '../../styles/v15/dersPdfEkran.css';

/** Ders PDF'i: slayt sırasıyla anlatım + her adımın özeti. "PDF olarak kaydet" tarayıcı yazdırma penceresini açar
 *  (sayfa boyutu @page ile 720×540 pt slayt boyutuna ayarlıdır; hedef olarak "PDF olarak kaydet" seçilir). */
export default function DersPdfEkranV15({ dersKey }: { dersKey: string }) {
  const [paket, setPaket] = useState<DiPaket | null>(null);
  const [deste, setDeste] = useState<{ slides: DiSlayt[]; title?: string } | null>(null);
  const [hata, setHata] = useState(false);
  useEffect(() => {
    Promise.all([dersIcerikGetir(dersKey), dersSlaytlariGetir(dersKey)]).then(([p, d]) => { if (p && d) { setPaket(p); setDeste(d); } else setHata(true); }).catch(() => setHata(true));
  }, [dersKey]);
  const akis = useMemo(() => (paket && deste ? dersPdfAkisi({ ...paket, baslik: paket.baslik || deste.title }, deste.slides) : null), [paket, deste]);
  if (hata) return <p className="v15-card" style={{ padding: 24 }}>Bu ders için PDF üretilemiyor: içerik paketi ya da Öğren destesi yok.</p>;
  if (!akis) return <p className="v15-card" style={{ padding: 24 }}>PDF hazırlanıyor…</p>;
  return (
    <div className="dpdf-ekran">
      <div className="dpdf-arac">
        <span>{akis.adimlar.length} adım · slayt boyutunda sayfalar</span>
        <button type="button" className="v15-btn is-primary" onClick={() => window.print()}><Printer size={16} /> PDF olarak kaydet</button>
      </div>
      <DersPdfBelge akis={akis} kod={dersKey.split('-').slice(0, 2).join('-').toUpperCase()} />
    </div>
  );
}
