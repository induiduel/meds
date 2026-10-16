/** "⋯" menüsü: ikincil eylemleri (çevrimdışı, listem, ses, tekrar, indir, tanıtım) tek düğmenin arkasında toplar. */
import React, { useEffect, useRef, useState } from 'react';
import { MoreHorizontal } from 'lucide-react';

export function CdDaha({ etiket, yukari, className = '', children }: { etiket: string; yukari?: boolean; className?: string; children: React.ReactNode }) {
  const [acik, setAcik] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!acik) return;
    const dis = (e: PointerEvent) => {
      const h = e.target as Element;
      // İçteki pencereler (Dialog) gövdeye taşınır: onlara tıklamak menüyü kapatmasın
      if (!ref.current?.contains(h) && !h.closest?.('[role="dialog"]')) setAcik(false);
    };
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape' && !document.querySelector('.cd-tk-menu')) setAcik(false); };
    document.addEventListener('pointerdown', dis);
    document.addEventListener('keydown', esc);
    return () => { document.removeEventListener('pointerdown', dis); document.removeEventListener('keydown', esc); };
  }, [acik]);
  return (
    <div className={`cd-daha ${className}`} ref={ref}>
      <button type="button" className={`cd-btn is-ikon cd-daha-btn${acik ? ' is-on' : ''}`} aria-expanded={acik} aria-label={etiket} title={etiket} onClick={() => setAcik((x) => !x)}>
        <MoreHorizontal aria-hidden />
      </button>
      {acik && <div className={`cd-daha-menu${yukari ? ' is-yukari' : ''}`} role="group" aria-label={etiket}>{children}</div>}
    </div>
  );
}
