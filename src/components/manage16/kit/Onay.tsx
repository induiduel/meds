import React, { useEffect, useRef, useState } from 'react';
import { AlertTriangle } from 'lucide-react';

export type OnaySecenek = {
  baslik: string;
  aciklama?: React.ReactNode;
  /** Kullanıcının aynen yazması gereken sözcük (tehlikeli işlem). Verilirse düğme yalnız eşleşince açılır */
  yazilacak?: string;
  onayMetni?: string;
  iptalMetni?: string;
  tehlikeli?: boolean;
};

type Bekleyen = OnaySecenek & { coz: (v: boolean) => void };
let goster: ((b: Bekleyen) => void) | null = null;

/** Onay penceresi açar; true = onaylandı. Kabukta <OnayHost/> takılıdır. */
export function onayIste(o: OnaySecenek): Promise<boolean> {
  return new Promise((coz) => {
    if (!goster) { coz(window.confirm(o.baslik)); return; }
    goster({ ...o, coz });
  });
}

export const OnayHost: React.FC = () => {
  const [b, setB] = useState<Bekleyen | null>(null);
  const [yazi, setYazi] = useState('');
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => { goster = (x) => { setYazi(''); setB(x); }; return () => { goster = null; }; }, []);
  useEffect(() => {
    if (!b) return;
    const once = document.activeElement as HTMLElement | null;
    setTimeout(() => ref.current?.querySelector<HTMLElement>('input, .m16-btn')?.focus(), 0);
    return () => once?.focus?.();
  }, [b]);
  if (!b) return null;
  const kapat = (v: boolean) => { b.coz(v); setB(null); };
  const hazir = !b.yazilacak || yazi.trim() === b.yazilacak;
  return (
    <div className="m16-perde" onMouseDown={(e) => { if (e.target === e.currentTarget) kapat(false); }}>
      <div ref={ref} className="m16-onay" role="alertdialog" aria-modal="true" aria-labelledby="m16-onay-b"
        onKeyDown={(e) => { if (e.key === 'Escape') kapat(false); }}>
        <h2 id="m16-onay-b">{b.tehlikeli && <AlertTriangle aria-hidden="true" />}{b.baslik}</h2>
        {b.aciklama && <div className="m16-onay-aciklama">{b.aciklama}</div>}
        {b.yazilacak && (
          <label className="m16-alan">
            <span>Onaylamak için <code>{b.yazilacak}</code> yazın</span>
            <input className="m16-girdi" value={yazi} onChange={(e) => setYazi(e.target.value)} autoComplete="off" spellCheck={false}
              onKeyDown={(e) => { if (e.key === 'Enter' && hazir) kapat(true); }} />
          </label>
        )}
        <div className="m16-onay-eylem">
          <button type="button" className="m16-btn hayalet" onClick={() => kapat(false)}>{b.iptalMetni || 'Vazgeç'}</button>
          <button type="button" className={`m16-btn ${b.tehlikeli ? 'tehlike' : 'birincil'}`} disabled={!hazir} onClick={() => kapat(true)}>{b.onayMetni || 'Onayla'}</button>
        </div>
      </div>
    </div>
  );
};
