/**
 * Köşeden bakan çift: Kitty & Batman sağ alt köşeden süzülüp bir süre durur, sonra geri çekilir.
 * Sayfa değişince ara sıra (en çok 4 dakikada bir) görünür; dokununca kalp bırakır ve küçük bir balon açar.
 */
import React, { useEffect, useRef, useState } from 'react';
import type { AppRoute } from '../../router';
import { KittyVeBatman } from './cizimler';
import { kalpPatlat } from './kalpPatlamasi';

const azalt = () => !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

export default function CiftGizli({ rota, ilkGecikmeMs = 110_000 }: { rota: AppRoute; ilkGecikmeMs?: number }) {
  const [gorunur, setGorunur] = useState(false);
  const [balon, setBalon] = useState<string | null>(null);
  const sonGosterim = useRef(0);
  const ilk = useRef(true);
  const kapatT = useRef<number | undefined>(undefined);

  const goster = () => {
    if (azalt()) return;
    sonGosterim.current = Date.now();
    setGorunur(true);
    window.clearTimeout(kapatT.current);
    kapatT.current = window.setTimeout(() => setGorunur(false), 9000);
  };

  useEffect(() => {
    const t = window.setTimeout(goster, ilkGecikmeMs);
    return () => { window.clearTimeout(t); window.clearTimeout(kapatT.current); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (ilk.current) { ilk.current = false; return; }
    if (Date.now() - sonGosterim.current < 240_000) return;
    if (Math.random() < 0.4) {
      const t = window.setTimeout(goster, 2500);
      return () => window.clearTimeout(t);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [rota]);

  const dokun = (e: React.MouseEvent) => {
    const r = (e.currentTarget as HTMLElement).getBoundingClientRect();
    kalpPatlat(r.left + r.width / 2, r.top + r.height * 0.3, 12, 90);
    const s = ['Bizim gibi.', 'Yan yana olmak güzel.', 'Seninle her şey daha kolay.', 'İyi ki birlikteyiz.'];
    setBalon(s[Math.floor(Math.random() * s.length)]);
    window.clearTimeout(kapatT.current);
    kapatT.current = window.setTimeout(() => { setBalon(null); setGorunur(false); }, 3200);
  };

  return (
    <button type="button" className={`ar-cift-kose ${gorunur ? 'is-gorunur' : ''}`} onClick={dokun} aria-label="Küçük bir çift" tabIndex={gorunur ? 0 : -1}>
      {balon && <span className="ar-cift-balon">{balon}</span>}
      <KittyVeBatman width={150} />
    </button>
  );
}
