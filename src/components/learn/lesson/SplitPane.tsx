/**
 * Öğren · yan yana görünüm: ders ile PDF arasında sürüklenebilir ayraç. Oran (ders payı, %) cihazda saklanır.
 * Geniş ekranda sütunlar, <1024 px'te üst/alt satırlar. Ayraç: sürükle, ok tuşları (Shift ile 10'ar), çift tıkla eşitle;
 * üzerine gelince hazır oranlar görünür.
 */
import React, { useCallback, useEffect, useRef, useState } from 'react';
import '../../../styles/ogren-ders.css';

const KEY = 'medsoru_learn_split';
const MIN = 20;
const MAX = 80;
const PRESETS: { v: number; label: string; title: string }[] = [
  { v: 35, label: '35', title: 'PDF ağırlıklı (ders %35)' },
  { v: 50, label: '50', title: 'Eşit' },
  { v: 65, label: '65', title: 'Ders ağırlıklı (ders %65)' },
];
const clamp = (v: number) => Math.max(MIN, Math.min(MAX, Math.round(v * 10) / 10));

const load = () => {
  try {
    const v = Number(localStorage.getItem(KEY));
    return v >= MIN && v <= MAX ? v : 50;
  } catch {
    return 50;
  }
};

const useNarrow = () => {
  const q = '(max-width: 1023px)';
  const [m, setM] = useState(() => typeof window !== 'undefined' && window.matchMedia(q).matches);
  useEffect(() => {
    const mq = window.matchMedia(q);
    const on = () => setM(mq.matches);
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, []);
  return m;
};

export const SplitPane: React.FC<{ left: React.ReactNode; right: React.ReactNode }> = ({ left, right }) => {
  const [ratio, setRatio] = useState(load);
  const [drag, setDrag] = useState(false);
  const narrow = useNarrow();
  const rootRef = useRef<HTMLDivElement>(null);

  const save = useCallback((v: number) => {
    const c = clamp(v);
    setRatio(c);
    try {
      localStorage.setItem(KEY, String(c));
    } catch {
      /* ignore */
    }
  }, []);

  const fromPointer = (e: PointerEvent | React.PointerEvent) => {
    const r = rootRef.current?.getBoundingClientRect();
    if (!r) return;
    save(narrow ? ((e.clientY - r.top) / r.height) * 100 : ((e.clientX - r.left) / r.width) * 100);
  };

  const onDown = (e: React.PointerEvent) => {
    if (e.button !== 0 || (e.target as HTMLElement).closest('.ls-split-presets')) return;
    e.preventDefault();
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    setDrag(true);
  };
  const onMove = (e: React.PointerEvent) => {
    if (drag) fromPointer(e);
  };
  const onUp = (e: React.PointerEvent) => {
    if (!drag) return;
    (e.currentTarget as HTMLElement).releasePointerCapture?.(e.pointerId);
    setDrag(false);
  };
  const onKey = (e: React.KeyboardEvent) => {
    const step = e.shiftKey ? 10 : 2;
    const back = narrow ? 'ArrowUp' : 'ArrowLeft';
    const fwd = narrow ? 'ArrowDown' : 'ArrowRight';
    if (e.key === back) save(ratio - step);
    else if (e.key === fwd) save(ratio + step);
    else if (e.key === 'Home') save(MIN);
    else if (e.key === 'End') save(MAX);
    else if (e.key === 'Enter') save(50);
    else return;
    e.preventDefault();
    e.stopPropagation(); // dersin ok tuşu kısayolları çalışmasın
  };

  const tpl = `minmax(0, ${ratio}fr) 14px minmax(0, ${100 - ratio}fr)`;
  const style: React.CSSProperties = narrow
    ? { gridTemplateColumns: 'minmax(0, 1fr)', gridTemplateRows: tpl }
    : { gridTemplateColumns: tpl, gridTemplateRows: 'minmax(0, 1fr)' };

  return (
    <div ref={rootRef} className={`ls-split has-handle${drag ? ' is-dragging' : ''}${narrow ? ' is-rows' : ''}`} style={style}>
      {left}
      <div
        className="ls-split-handle"
        role="separator"
        aria-orientation={narrow ? 'horizontal' : 'vertical'}
        aria-valuemin={MIN}
        aria-valuemax={MAX}
        aria-valuenow={Math.round(ratio)}
        aria-valuetext={`Ders %${Math.round(ratio)}, PDF %${Math.round(100 - ratio)}`}
        aria-label="Ders ve PDF alanı oranı"
        title="Sürükle · çift tıkla eşitle · ok tuşları"
        tabIndex={0}
        onPointerDown={onDown}
        onPointerMove={onMove}
        onPointerUp={onUp}
        onPointerCancel={onUp}
        onDoubleClick={() => save(50)}
        onKeyDown={onKey}
      >
        <span className="ls-split-grip" aria-hidden />
        {drag && <span className="ls-split-val" aria-hidden>{Math.round(ratio)} · {100 - Math.round(ratio)}</span>}
        <div className="ls-split-presets" role="group" aria-label="Hazır oranlar">
          {PRESETS.map((p) => (
            <button key={p.v} type="button" className={Math.round(ratio) === p.v ? 'is-on' : ''} onClick={() => save(p.v)} title={p.title}>
              <i style={{ ['--r' as any]: `${p.v}%` }} aria-hidden />
              <span className="sr-only">{p.title}</span>
            </button>
          ))}
        </div>
      </div>
      {right}
    </div>
  );
};
