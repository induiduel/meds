import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Printer } from 'lucide-react';
import { dersIcerikGetir, dersSlaytlariGetir, type DiPaket, type DiSlayt } from './dersIcerik';
import { dersPdfAkisi } from './dersPdfAkis';
import { dersPdfHtml } from './dersPdfHtml';
import css from '../../styles/v15/dersPdf.css?raw';
import '../../styles/v15/dersPdfEkran.css';

/** Ders PDF'i: belge uygulamadan yalıtılmış bir iframe'de (kendi HTML'i + stili) gösterilir ve oradan yazdırılır;
 *  böylece uygulama teması/kabuğu PDF'e karışmaz, sayfa kenar boşluğu ve sayfa boyutu (720×540 pt) @page ile korunur. */
/** Belgenin tasarlandığı genişlik (slayt boyutu 720 pt ≈ 960 px + kenar) */
const BELGE_EN = 1000;

export default function DersPdfEkranV15({ dersKey }: { dersKey: string }) {
  const [paket, setPaket] = useState<DiPaket | null>(null);
  const [deste, setDeste] = useState<{ slides: DiSlayt[]; title?: string } | null>(null);
  const [hata, setHata] = useState(false);
  const cerceve = useRef<HTMLIFrameElement>(null);
  useEffect(() => {
    Promise.all([dersIcerikGetir(dersKey), dersSlaytlariGetir(dersKey)]).then(([p, d]) => { if (p && d) { setPaket(p); setDeste(d); } else setHata(true); }).catch(() => setHata(true));
  }, [dersKey]);
  useEffect(() => {
    const f = cerceve.current; if (!f || typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(() => sigdirRef.current()); ro.observe(f); return () => ro.disconnect();
  });
  const sigdirRef = useRef<() => void>(() => {});
  const belge = useMemo(() => {
    if (!paket || !deste) return null;
    const akis = dersPdfAkisi({ ...paket, baslik: paket.baslik || deste.title }, deste.slides);
    return { akis, html: dersPdfHtml(akis, dersKey.split('-').slice(0, 2).join('-').toUpperCase(), css, true) };
  }, [paket, deste, dersKey]);
  if (hata) return <p className="v15-card" style={{ padding: 24 }}>Bu ders için PDF üretilemiyor: içerik paketi ya da Öğren destesi yok.</p>;
  if (!belge) return <p className="v15-card" style={{ padding: 24 }}>PDF hazırlanıyor…</p>;
  // H432: iframe eskiden içerik boyunda (~89.000 px) ve telefonda en az 1000 px genişti; tarayıcı bu kadar büyük katmanı
  // parça parça (karo) çizip ekran dışını atıyor, kaydırırken belge "parçalanıp geri geliyordu" (en çok iPhone). Çerçeve
  // artık ekran boyunda ve belge içinde kayıyor; dar ekranda belge çerçeve genişliğine ölçeklenir (yazdırmada ölçek kalkar).
  const sigdir = () => {
    const f = cerceve.current; const d = f?.contentDocument; if (!f || !d) return;
    const w = f.clientWidth; (d.documentElement.style as any).zoom = w && w < BELGE_EN ? String(w / BELGE_EN) : '';
  };
  sigdirRef.current = sigdir;
  const yazdir = () => {
    const f = cerceve.current; const win = f?.contentWindow; const d = f?.contentDocument; if (!win || !d) return;
    (d.documentElement.style as any).zoom = '';
    win.addEventListener('afterprint', sigdir, { once: true });
    win.focus(); win.print();
    setTimeout(sigdir, 1500); // afterprint gelmeyen tarayıcılar için
  };
  return (
    <div className="dpdf-ekran">
      <div className="dpdf-arac">
        <span>{belge.akis.adimlar.length} adım · slayt boyutunda sayfalar</span>
        <button type="button" className="v15-btn is-primary" onClick={yazdir}><Printer size={16} /> PDF olarak kaydet</button>
      </div>
      <iframe ref={cerceve} title="Ders PDF önizleme" className="dpdf-cerceve" srcDoc={belge.html} onLoad={sigdir} />
    </div>
  );
}
