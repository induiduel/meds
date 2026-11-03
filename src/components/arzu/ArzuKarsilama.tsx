/**
 * Arzu'ya karşılama ekranı: pembe-krem zemin, süzülen kalpler, kalp tutan oturan tilki, günün cümlesi ve
 * Kitty & Batman çifti. Günde bir kez kendiliğinden (ArzuKatmani zamanlar), istenirse asılı kalbe üç kez dokununca.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Kalp, KittyVeBatman, TilkiOturan } from './cizimler';
import { gununCumlesi, karsilamaSelam } from './mesajlar';
import { kalpPatlat } from './kalpPatlamasi';

type Props = { onKapat: () => void };

const KALP_SAYISI = 16;

export default function ArzuKarsilama({ onKapat }: Props) {
  const [kapaniyor, setKapaniyor] = useState(false);
  const btnRef = useRef<HTMLButtonElement>(null);
  const selam = useMemo(() => karsilamaSelam(), []);
  const cumle = useMemo(() => {
    const d = new Date();
    if (d.getMonth() === 1 && d.getDate() === 14) return 'Sevgililer günün kutlu olsun. İyi ki seninleyim.';
    return gununCumlesi();
  }, []);
  const isiltilar = useMemo(() => Array.from({ length: 12 }, (_, i) => ({ x: (i * 83 + 7) % 100, y: (i * 47 + 11) % 100, g: (i * 0.37) % 3, s: 6 + (i % 3) * 3 })), []);
  const kalpler = useMemo(
    () => Array.from({ length: KALP_SAYISI }, (_, i) => ({
      x: (i * 61 + 13) % 100,
      s: 10 + ((i * 37) % 18),
      d: 9 + ((i * 53) % 9),
      g: (i * 1.7) % 9,
      o: 0.35 + ((i * 29) % 40) / 100,
    })),
    [],
  );

  const kapat = () => {
    if (kapaniyor) return;
    const b = btnRef.current?.getBoundingClientRect();
    if (b) kalpPatlat(b.left + b.width / 2, b.top + b.height / 2, 26, 200);
    setKapaniyor(true);
    window.setTimeout(onKapat, 520);
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') kapat(); };
    window.addEventListener('keydown', onKey);
    const t = window.setTimeout(() => btnRef.current?.focus({ preventScroll: true }), 1400);
    return () => { window.removeEventListener('keydown', onKey); window.clearTimeout(t); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return createPortal(
    <div className={`ar-kars ${kapaniyor ? 'is-kapaniyor' : ''}`} role="dialog" aria-modal="true" aria-label="Arzu'ya karşılama">
      <div className="ar-kars-zemin" aria-hidden="true">
        {kalpler.map((k, i) => (
          <span
            key={i}
            className="ar-kars-kalp"
            style={{ '--x': `${k.x}%`, '--s': `${k.s}px`, '--d': `${k.d}s`, '--g': `${k.g}s`, '--o': k.o } as React.CSSProperties}
          >
            <Kalp size={k.s} color={i % 3 === 0 ? '#FF8FB0' : i % 3 === 1 ? '#FF5C86' : '#FFC2D4'} parlak={false} />
          </span>
        ))}
        {isiltilar.map((p, i) => (
          <span key={`i${i}`} className="ar-kars-isilti" style={{ left: `${p.x}%`, top: `${p.y}%`, '--g': `${p.g}s`, '--s': `${p.s}px` } as React.CSSProperties} />
        ))}
        <span className="ar-kars-isik ar-kars-isik-1" />
        <span className="ar-kars-isik ar-kars-isik-2" />
      </div>

      <div className="ar-kars-kart">
        <div className="ar-kars-tilki">
          <TilkiOturan width={200} />
          <span className="ar-kars-tilki-golge" />
        </div>
        <p className="ar-kars-selam">{selam},</p>
        <h1 className="ar-kars-ad" aria-label="Arzu">
          {'Arzu'.split('').map((h, i) => (
            <span key={i} style={{ '--i': i } as React.CSSProperties}>{h}</span>
          ))}
        </h1>
        <p className="ar-kars-mesaj">{cumle}</p>

        <div className="ar-kars-cift" aria-hidden="true">
          <KittyVeBatman width={150} />
        </div>

        <button ref={btnRef} type="button" className="ar-kars-btn" onClick={kapat}>
          <span>Derslere dön</span>
          <Kalp size={18} color="#fff" parlak={false} />
        </button>
        <p className="ar-kars-alt">Sayfalarda arada bir tilki geçecek; ona dokunursan sana benden küçük bir not bırakır.</p>
      </div>
    </div>,
    document.body,
  );
}
