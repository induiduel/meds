import React, { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
import type { UnoRenk } from '../../../services/masa/tipler';
import { RenkBicimi } from './Kart';
import { temaAl, UNO_SIRA } from './temalar';
import type { Yerlesim } from './yerlesim';

/** Joker / +4 için dört renkli seçim çarkı. Dışına dokunmak ya da Esc = vazgeç. */
export default function RenkSecici({ yer, tema, onSec, onVazgec }: { yer: Yerlesim; tema: string; onSec: (r: UnoRenk) => void; onVazgec: () => void }) {
  const t = temaAl(tema);
  const kokRef = useRef<HTMLDivElement>(null);
  // Çarkı açan dokunuşun ardından gelen "hayalet tıklama" seçim / vazgeç sayılmasın
  const acildi = useRef(performance.now());
  const taze = () => performance.now() - acildi.current < 320;
  const sec = (r: UnoRenk) => { if (!taze()) onSec(r); };
  const vazgec = () => { if (!taze()) onVazgec(); };
  const cap = Math.round(Math.max(176, Math.min(300, Math.min(yer.W, yer.H) * 0.56, yer.H - 16)));
  const cy = Math.max(cap / 2 + 8, Math.min(yer.H - cap / 2 - 8, yer.atik.y));
  useEffect(() => {
    kokRef.current?.querySelector<HTMLButtonElement>('.um-cark-dilim')?.focus({ preventScroll: true });
    const tus = (e: KeyboardEvent) => { if (e.key === 'Escape') { e.stopPropagation(); onVazgec(); } };
    window.addEventListener('keydown', tus, true);
    return () => window.removeEventListener('keydown', tus, true);
  }, [onVazgec]);
  return (
    <div ref={kokRef} className="um-secici" role="dialog" aria-modal="true" aria-label="Renk seç">
      <button type="button" className="um-secici-perde" onClick={vazgec} aria-label="Vazgeç" tabIndex={-1} />
      <div className="um-cark-yer" style={{ transform: `translate3d(${yer.W / 2}px, ${cy}px, 0)` }}>
        <div className={`um-cark${cap < 210 ? ' um-cark-kucuk' : ''}`} style={{ width: cap, height: cap }}>
          {UNO_SIRA.map((r, i) => (
            <button key={r} type="button" className={`um-cark-dilim um-cark-${i}`} style={{ background: t.renk[r].ana, color: r === 's' ? '#1d1a16' : '#fff' }} onClick={() => sec(r)} aria-label={t.renk[r].ad}>
              <span className="um-cark-ic">
                <svg viewBox="-10 -10 20 20" className="um-cark-bicim" aria-hidden="true"><RenkBicimi renk={r} b={6} /></svg>
                <span className="um-cark-ad">{t.renk[r].ad}</span>
              </span>
            </button>
          ))}
          <button type="button" className="um-cark-vazgec" onClick={vazgec} aria-label="Vazgeç, kartı geri al"><X size={22} aria-hidden="true" /></button>
          <div className="um-cark-baslik">Renk seç</div>
        </div>
      </div>
    </div>
  );
}
