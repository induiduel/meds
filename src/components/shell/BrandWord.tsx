import React, { useEffect, useRef, useState } from 'react';

/**
 * MeDSor marka yazısı — "DS" = Doktora Sor.
 * 10 dakikada bir (ve oturumun ilk açılışında bir kez) harfler kayarak açılır:
 *   MeDSor → "Me" kapanır, D'nin ardından "oktora" açılır, araya boşluk girer → "Doktora Sor"
 *   kısa bekleme → tersine kayıp kapanır → MeDSor.
 * Yalnız sekme görünürken oynar; "hareketi azalt" (sistem ya da Görünüm › Hareket) seçiliyse hiç oynamaz.
 * Genişlik geçişi max-width ile; yerleşimi bir kez etkiler, sürekli çizim yükü yok.
 */
const EVERY_MS = 10 * 60 * 1000;
const HOLD_MS = 2600;
const FIRST_KEY = 'medsoru_brand_anim_seen';

const reducedMotion = () =>
  (typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) ||
  (typeof document !== 'undefined' && document.documentElement.dataset.motion === 'reduced');

export const BrandWord: React.FC<{ className?: string }> = ({ className = '' }) => {
  const [open, setOpen] = useState(false);
  const holdRef = useRef<number | undefined>(undefined);

  useEffect(() => {
    const play = () => {
      if (document.visibilityState !== 'visible' || reducedMotion()) return;
      setOpen(true);
      window.clearTimeout(holdRef.current);
      holdRef.current = window.setTimeout(() => setOpen(false), HOLD_MS);
    };
    let first: number | undefined;
    try {
      if (!sessionStorage.getItem(FIRST_KEY)) {
        sessionStorage.setItem(FIRST_KEY, '1');
        first = window.setTimeout(play, 3500);
      }
    } catch { /* gizli pencere: yalnız aralıklı */ }
    const timer = window.setInterval(play, EVERY_MS);
    return () => {
      window.clearInterval(timer);
      window.clearTimeout(first);
      window.clearTimeout(holdRef.current);
    };
  }, []);

  return (
    <span className={`sh-brand-word bw ${open ? 'is-open' : ''} ${className}`} aria-label="MeDSor — Doktora Sor">
      <span className="bw-me" aria-hidden="true">Me</span>
      <b aria-hidden="true">D</b>
      <span className="bw-x bw-oktora" aria-hidden="true">oktora</span>
      <span className="bw-x bw-sp" aria-hidden="true">{' '}</span>
      <b aria-hidden="true">S</b>
      <span aria-hidden="true">or</span>
    </span>
  );
};

export default BrandWord;
