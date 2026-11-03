/**
 * Fısıltılar: sol alt köşeden katlanmış bir not kayar; sayfaya ve saate uygun bir sevgi cümlesi taşır.
 * İlk not 3 dakika sonra, sonrakiler 5–8 dakikada bir; `arzu:fisilti` olayı anında bir not açar.
 */
import React, { useEffect, useRef, useState } from 'react';
import type { AppRoute } from '../../router';
import { Kalp } from './cizimler';
import { fisiltiSec, type Fisilti } from './mesajlar';
import { kalpSuzul } from './kalpPatlamasi';

const rnd = (a: number, b: number) => a + Math.random() * (b - a);

export default function Fisiltilar({ rota, ilkGecikmeMs = 180_000 }: { rota: AppRoute; ilkGecikmeMs?: number }) {
  const [not, setNot] = useState<Fisilti | null>(null);
  const [kapaniyor, setKapaniyor] = useState(false);
  const rotaRef = useRef(rota);
  const sayac = useRef(0);
  const kapatT = useRef<number | undefined>(undefined);
  rotaRef.current = rota;

  const kapat = () => {
    setKapaniyor(true);
    window.setTimeout(() => { setNot(null); setKapaniyor(false); }, 380);
  };

  const goster = (e?: Event) => {
    if (document.visibilityState !== 'visible') return;
    const metin = (e as CustomEvent | undefined)?.detail?.metin;
    setKapaniyor(false);
    setNot(typeof metin === 'string' && metin ? { metin } : fisiltiSec(rotaRef.current, sayac.current++));
    window.clearTimeout(kapatT.current);
    kapatT.current = window.setTimeout(kapat, 11_000);
  };

  useEffect(() => {
    let t = window.setTimeout(function dongu() {
      goster();
      t = window.setTimeout(dongu, rnd(300_000, 480_000));
    }, ilkGecikmeMs);
    window.addEventListener('arzu:fisilti', goster as EventListener);
    return () => { window.clearTimeout(t); window.clearTimeout(kapatT.current); window.removeEventListener('arzu:fisilti', goster as EventListener); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!not) return null;
  return (
    <button
      type="button"
      className={`ar-not ${kapaniyor ? 'is-kapaniyor' : ''}`}
      onClick={(e) => {
        const r = (e.currentTarget as HTMLElement).getBoundingClientRect();
        kalpSuzul(r.left + 26, r.top + 10, 4);
        kapat();
      }}
      aria-label={`Not: ${not.metin}`}
    >
      <span className="ar-not-kat" aria-hidden="true" />
      <span className="ar-not-ikon" aria-hidden="true"><Kalp size={16} /></span>
      <span className="ar-not-metin">{not.metin}</span>
    </button>
  );
}
