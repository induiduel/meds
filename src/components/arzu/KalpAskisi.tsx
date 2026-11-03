/**
 * Asılı kalp: üst çubuğun altından ipiyle sarkar, sarkaç gibi salınır. Dokununca patlar ve bir not bırakır,
 * birkaç saniye sonra yeniden büyür. Üç kez art arda dokunmak ya da uzun basmak (600 ms) karşılama ekranını yeniden açar.
 * Dokunmatik cihazda ilk dokunuşta iOS hareket izni istenir (sallayınca tilki geçidi için).
 */
import React, { useRef, useState } from 'react';
import { KalpAskisiCizim } from './cizimler';
import { kalpPatlat } from './kalpPatlamasi';
import { hareketIzniIste } from './sallama';

export default function KalpAskisi({ onUcKez }: { onUcKez: () => void }) {
  const [patladi, setPatladi] = useState(false);
  const tiklar = useRef<number[]>([]);
  const uzun = useRef<number | undefined>(undefined);
  const uzunOldu = useRef(false);

  const patlat = (el: HTMLElement) => {
    const r = el.getBoundingClientRect();
    kalpPatlat(r.left + r.width / 2, r.top + r.height * 0.78, 16, 120);
    window.dispatchEvent(new CustomEvent('arzu:fisilti'));
    setPatladi(true);
    window.setTimeout(() => setPatladi(false), 6500);
  };

  const basla = () => {
    uzunOldu.current = false;
    void hareketIzniIste();
    window.clearTimeout(uzun.current);
    uzun.current = window.setTimeout(() => { uzunOldu.current = true; tiklar.current = []; onUcKez(); }, 600);
  };
  const birak = () => window.clearTimeout(uzun.current);

  const dokun = (e: React.MouseEvent) => {
    if (uzunOldu.current) { uzunOldu.current = false; return; }
    const now = Date.now();
    tiklar.current = [...tiklar.current.filter((t) => now - t < 1300), now];
    if (tiklar.current.length >= 3) {
      tiklar.current = [];
      onUcKez();
      return;
    }
    if (!patladi) patlat(e.currentTarget as HTMLElement);
  };

  return (
    <button
      type="button"
      className={`ar-aski ${patladi ? 'is-patladi' : ''}`}
      onClick={dokun}
      onPointerDown={basla}
      onPointerUp={birak}
      onPointerCancel={birak}
      onPointerLeave={birak}
      onContextMenu={(e) => e.preventDefault()}
      aria-label="Küçük bir kalp"
      title="♥"
    >
      <KalpAskisiCizim />
    </button>
  );
}
