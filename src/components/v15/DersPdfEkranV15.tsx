import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Printer } from 'lucide-react';
import { dersIcerikGetir, dersSlaytlariGetir, type DiPaket, type DiSlayt } from './dersIcerik';
import { dersPdfAkisi } from './dersPdfAkis';
import { dersPdfHtml } from './dersPdfHtml';
import css from '../../styles/v15/dersPdf.css?raw';
import '../../styles/v15/dersPdfEkran.css';

/** Ders PDF'i: belge uygulamadan yalıtılmış bir iframe'de (kendi HTML'i + stili) gösterilir ve oradan yazdırılır;
 *  böylece uygulama teması/kabuğu PDF'e karışmaz, sayfa kenar boşluğu ve sayfa boyutu (720×540 pt) @page ile korunur. */
export default function DersPdfEkranV15({ dersKey }: { dersKey: string }) {
  const [paket, setPaket] = useState<DiPaket | null>(null);
  const [deste, setDeste] = useState<{ slides: DiSlayt[]; title?: string } | null>(null);
  const [hata, setHata] = useState(false);
  const cerceve = useRef<HTMLIFrameElement>(null);
  const [yuk, setYuk] = useState(720);
  useEffect(() => {
    Promise.all([dersIcerikGetir(dersKey), dersSlaytlariGetir(dersKey)]).then(([p, d]) => { if (p && d) { setPaket(p); setDeste(d); } else setHata(true); }).catch(() => setHata(true));
  }, [dersKey]);
  const belge = useMemo(() => {
    if (!paket || !deste) return null;
    const akis = dersPdfAkisi({ ...paket, baslik: paket.baslik || deste.title }, deste.slides);
    return { akis, html: dersPdfHtml(akis, dersKey.split('-').slice(0, 2).join('-').toUpperCase(), css, true) };
  }, [paket, deste, dersKey]);
  if (hata) return <p className="v15-card" style={{ padding: 24 }}>Bu ders için PDF üretilemiyor: içerik paketi ya da Öğren destesi yok.</p>;
  if (!belge) return <p className="v15-card" style={{ padding: 24 }}>PDF hazırlanıyor…</p>;
  const olc = () => { const d = cerceve.current?.contentDocument; if (d) setYuk(d.documentElement.scrollHeight); };
  return (
    <div className="dpdf-ekran">
      <div className="dpdf-arac">
        <span>{belge.akis.adimlar.length} adım · slayt boyutunda sayfalar</span>
        <button type="button" className="v15-btn is-primary" onClick={() => { cerceve.current?.contentWindow?.focus(); cerceve.current?.contentWindow?.print(); }}><Printer size={16} /> PDF olarak kaydet</button>
      </div>
      <iframe ref={cerceve} title="Ders PDF önizleme" className="dpdf-cerceve" srcDoc={belge.html} onLoad={olc} style={{ height: yuk }} />
    </div>
  );
}
