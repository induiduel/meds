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
  useEffect(() => { if (sonraki) lottieOnYukle(`adim-${sonraki.id}`).catch(() => {}); }, [sonraki]);

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
        <div className="kmb-dv-dugmeler">
          <button onClick={() => setI(Math.max(0, i - 1))} disabled={i === 0} aria-label="Önceki adım"><svg viewBox="0 0 24 24"><path d="M6 5h2v14H6zM20 5v14L9 12z" /></svg></button>
          <button onClick={ileri} disabled={i === adimlar.length - 1} aria-label="Sonraki adım"><svg viewBox="0 0 24 24"><path d="M16 5h2v14h-2zM4 5v14l11-7z" /></svg></button>
          <button onClick={kapat} aria-label="Kapat"><svg viewBox="0 0 24 24"><path d="M6.4 5 5 6.4 10.6 12 5 17.6 6.4 19l5.6-5.6 5.6 5.6 1.4-1.4-5.6-5.6L19 6.4 17.6 5 12 10.6z" /></svg></button>
        </div>
      </div>
      <div className="kmb-dv-govde">
        <LottieVideo key={a.id} ad={`adim-${a.id}`} kod={ders.kod} ses={ses} otomatik doldur
          onBitti={() => { izlendi?.(a.id); if (sonraki) window.setTimeout(() => setI((n) => n + 1), 250); }}
          sonraki={sonraki ? { ad: `adim-${sonraki.id}`, baslik: sonraki.baslik, git: ileri } : undefined} />
      </div>
    </div>,
    document.body,
  );
}
