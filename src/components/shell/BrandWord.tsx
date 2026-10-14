import React, { useEffect, useRef, useState } from 'react';

/**
 * MeDSor marka yazısı — "DS" = Doktora Sor.
 * İmleç üstüne gelince ve dakikada bir kez harfler kayarak açılır:
 *   MeDSor → "Me" kapanır, D'nin ardından "oktora" açılır, araya boşluk girer → "Doktora Sor"
 *   kısa bekleme → tersine kayıp kapanır → MeDSor.
 * Yalnız sekme görünürken oynar; "hareketi azalt" (sistem ya da Görünüm › Hareket) seçiliyse hiç oynamaz.
 * Genişlik geçişi max-width ile; yerleşimi bir kez etkiler, sürekli çizim yükü yok.
 */
const EVERY_MS = 60 * 1000;
const HOLD_MS = 2600;

const reducedMotion = () =>
  (typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) ||
  (typeof document !== 'undefined' && document.documentElement.dataset.motion === 'reduced');

export const BrandWord: React.FC<{ className?: string }> = ({ className = '' }) => {
  const [open, setOpen] = useState(false);
  const holdRef = useRef<number | undefined>(undefined);
  const hoverRef = useRef(false);

  const play = () => {
    if (document.visibilityState !== 'visible' || reducedMotion()) return;
    setOpen(true);
    window.clearTimeout(holdRef.current);
    holdRef.current = window.setTimeout(() => { if (!hoverRef.current) setOpen(false); }, HOLD_MS);
  };

  useEffect(() => {
    const timer = window.setInterval(play, EVERY_MS);
    return () => {
      window.clearInterval(timer);
      window.clearTimeout(holdRef.current);
    };
  }, []);

  // Üstüne gelince açılır, imleç durdukça açık kalır; ayrılınca (en az HOLD_MS dolmuşsa) kapanır.
  const onEnter = () => { hoverRef.current = true; play(); };
  const onLeave = () => {
    hoverRef.current = false;
    window.clearTimeout(holdRef.current);
    holdRef.current = window.setTimeout(() => setOpen(false), 600);
  };

  return (
    <span className={`sh-brand-word bw ${open ? 'is-open' : ''} ${className}`} aria-label="MeDSor — Doktora Sor" onMouseEnter={onEnter} onMouseLeave={onLeave}>
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
