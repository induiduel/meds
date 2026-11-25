import { useRef, useState, type KeyboardEvent, type PointerEvent } from 'react';

export type SeritDurum = 'd' | 'd2' | 'y' | '';

const DURUM_ADI: Record<SeritDurum, string> = { d: 'ilk denemede doğru', d2: 'çözüldü', y: 'dinlendi', '': '' };

/**
 * Çözücü ilerleme şeridi (H670). Eskiden her soru ayrı <button> idi: 215 soruda parça 3×6 px'e iniyor,
 * telefonda dokunulamıyor, klavyede 215 sekme durağı oluşuyordu. Şerit tek kaydırıcıdır: parçalar yalnız görsel,
 * dokunma/sürükleme konumdan soruyu seçer (bırakınca geçer), ←/→ ±1, PgUp/PgDn ±10, Home/End uçlar.
 */
export function IlerlemeSeridi({ durumlar, simdi, onSec }: { durumlar: SeritDurum[]; simdi: number; onSec: (n: number) => void }) {
  const ref = useRef<HTMLDivElement>(null);
  const [onizleme, setOnizleme] = useState<number | null>(null);
  const son = durumlar.length - 1;
  const konumdan = (x: number) => {
    const r = ref.current?.getBoundingClientRect();
    if (!r || son < 0) return 0;
    const st = getComputedStyle(ref.current!);
    const sol = r.left + parseFloat(st.paddingLeft), gen = r.width - parseFloat(st.paddingLeft) - parseFloat(st.paddingRight);
    return Math.max(0, Math.min(son, Math.floor(((x - sol) / Math.max(1, gen)) * durumlar.length)));
  };
  const indir = (e: PointerEvent<HTMLDivElement>) => {
    e.currentTarget.setPointerCapture(e.pointerId);
    setOnizleme(konumdan(e.clientX));
  };
  const tasi = (e: PointerEvent<HTMLDivElement>) => {
    if (e.currentTarget.hasPointerCapture(e.pointerId)) setOnizleme(konumdan(e.clientX));
  };
  const birak = (e: PointerEvent<HTMLDivElement>) => {
    if (!e.currentTarget.hasPointerCapture(e.pointerId)) return;
    e.currentTarget.releasePointerCapture(e.pointerId);
    const n = konumdan(e.clientX);
    setOnizleme(null);
    if (n !== simdi) onSec(n);
  };
  const tus = (e: KeyboardEvent<HTMLDivElement>) => {
    const adim: Record<string, number> = { ArrowRight: 1, ArrowUp: 1, ArrowLeft: -1, ArrowDown: -1, PageUp: 10, PageDown: -10 };
    let n: number | null = null;
    if (e.key in adim) n = Math.max(0, Math.min(son, Math.max(0, simdi) + adim[e.key]));
    else if (e.key === 'Home') n = 0;
    else if (e.key === 'End') n = son;
    if (n === null) return;
    e.preventDefault();
    e.stopPropagation();
    if (n !== simdi) onSec(n);
  };
  const gost = onizleme ?? Math.max(0, simdi);
  const d = durumlar[gost] ?? '';
  return (
    <div
      ref={ref}
      className="sc-ilerleme"
      role="slider"
      tabIndex={0}
      aria-label="Soru seç"
      aria-valuemin={1}
      aria-valuemax={durumlar.length}
      aria-valuenow={gost + 1}
      aria-valuetext={`${gost + 1}. soru / ${durumlar.length}${d ? `, ${DURUM_ADI[d]}` : ''}`}
      onPointerDown={indir}
      onPointerMove={tasi}
      onPointerUp={birak}
      onPointerCancel={() => setOnizleme(null)}
      onKeyDown={tus}
      style={{ gap: durumlar.length > 100 ? 0 : durumlar.length > 50 ? 1 : 3 }}
    >
      {durumlar.map((r, n) => (
        <span
          key={n}
          aria-hidden="true"
          className={`sc-seg${n === simdi ? ' is-simdi' : ''}${n === onizleme ? ' is-onizle' : ''}${r ? ` is-${r}` : ''}`}
        />
      ))}
      {onizleme !== null && (
        <span className="sc-ilerleme-ip" aria-hidden="true" style={{ left: `clamp(36px, ${((onizleme + 0.5) / durumlar.length) * 100}%, calc(100% - 36px))` }}>
          {onizleme + 1}. soru
        </span>
      )}
    </div>
  );
}
