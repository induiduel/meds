/**
 * KMB ders videosu — dersin 18 adım videosu (adim_lottie.py: her cümle bir bölüm) tam ekranda art arda oynar. Her adım kendi
 * EMA sesiyle (o-<adım>) kendi oynatıcısında çalar; bir sonraki önceden yüklenir, bitince kendiliğinden geçilir (geçişte boş
 * kare/ses kayması olmaz). Üstte adım şeridi (atla), altta oynatıcının altyazısı ve denetimleri; sağ/sol 10 sn.
 * İzlenen adımlar `izlendi` ile bildirilir (öğrenme yolu ilerlemesi).
 */
import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import LottieVideo, { KMB_DURDUR, LOTTILER, lottieOnYukle } from './LottieVideo';
import type { Ders, SesKayit } from './KmbAsistan';

export default function DersVideo({ ders, ses, bas = 0, onKapat, izlendi }: {
  ders: Ders; ses: SesKayit | null; bas?: number; onKapat: () => void; izlendi?: (adimId: string) => void;
}) {
  const kap = useRef<HTMLDivElement>(null);
  const adimlar = ders.adimlar.filter((a) => LOTTILER.some((x) => x.adim === a.id));
  const [i, setI] = useState(Math.max(0, adimlar.findIndex((a) => a.id === ders.adimlar[bas]?.id)));
  const [gecis, setGecis] = useState(true);
  const [uyanik, setUyanik] = useState(true);
  const zaman = useRef(0);
  const uyandir = () => { setUyanik(true); window.clearTimeout(zaman.current); zaman.current = window.setTimeout(() => setUyanik(false), 2800); };
  const a = adimlar[i];
  const sonraki = adimlar[i + 1];

  useEffect(() => {
    kap.current?.requestFullscreen?.().catch(() => { /* izin yoksa katman pencereyi kaplar */ });
    try { (screen.orientation as any)?.lock?.('landscape').catch(() => {}); } catch { /* yönlendirme kilidi yok */ }
    document.body.style.overflow = 'hidden';
    uyandir();
    return () => { document.body.style.overflow = ''; window.dispatchEvent(new CustomEvent(KMB_DURDUR, { detail: 'kapat' })); };
  }, []);
  useEffect(() => {
    setGecis(true);
    const z = window.setTimeout(() => setGecis(false), 1800);
    if (sonraki) lottieOnYukle(`adim-${sonraki.id}`).catch(() => {});
    return () => window.clearTimeout(z);
  }, [i, sonraki]);

  const kapat = () => { if (document.fullscreenElement) document.exitFullscreen().catch(() => {}); onKapat(); };
  const ileri = () => { izlendi?.(a.id); if (i < adimlar.length - 1) setI(i + 1); };
  if (!a) return null;

  // gövdeye portal: site içerik alanındaki CSS yakınlaştırması (uiZoom) sabit katmanı küçültmesin
  return createPortal(
    <div ref={kap} className={`kmb-dv kmb-kok${uyanik ? '' : ' uyku'}`} onMouseMove={uyandir} onTouchStart={uyandir} role="dialog" aria-label={`Ders videosu: ${ders.ad}`} onKeyDown={(e) => { if (e.key === 'Escape') kapat(); }}>
      <div className="kmb-dv-ust">
        <div className="kmb-dv-serit" role="tablist" aria-label="Adımlar">
          {adimlar.map((x, j) => (
            <button key={x.id} role="tab" aria-selected={j === i} title={`${j + 1}. ${x.baslik}`} className={`${j === i ? 'etkin' : ''}${j < i ? ' gecti' : ''}`} onClick={() => setI(j)} />
          ))}
        </div>
        <div className="kmb-dv-baslik"><span className="kmb-dv-no">{i + 1} / {adimlar.length}</span><b>{a.baslik}</b></div>
        <button className="kmb-dv-gec" onClick={() => setI(Math.max(0, i - 1))} disabled={i === 0} aria-label="Önceki adım">⏮</button>
        <button className="kmb-dv-gec" onClick={ileri} disabled={i === adimlar.length - 1} aria-label="Sonraki adım">⏭</button>
        <button className="kmb-dv-kapat" onClick={kapat} aria-label="Kapat">✕</button>
      </div>
      <div className="kmb-dv-govde">
        <LottieVideo key={a.id} ad={`adim-${a.id}`} kod={ders.kod} ses={ses} otomatik doldur
          onBitti={() => { izlendi?.(a.id); if (sonraki) window.setTimeout(() => setI((n) => n + 1), 900); }}
          sonraki={sonraki ? { ad: `adim-${sonraki.id}`, baslik: sonraki.baslik, git: ileri } : undefined} />
        {gecis && <div className="kmb-dv-kart" aria-hidden><span>Adım {i + 1}</span><b>{a.baslik}</b></div>}
      </div>
    </div>,
    document.body,
  );
}
