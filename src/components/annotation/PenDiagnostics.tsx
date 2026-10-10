import React, { useEffect, useState } from 'react';

/**
 * Kalem tanılama paneli: cihazın gerçekte hangi değerleri bildirdiğini gösterir.
 * Yan düğme / silgi ucu algılanmıyorsa, düğmeye basarak çizip buradaki
 * `pointerType`, `button`, `buttons` değerlerine bakılır.
 *
 * Kendi dinleyicilerini capture aşamasında ekler; motoru etkilemez.
 */
export function PenDiagnostics({ target }: { target: HTMLElement | null }) {
  const [lines, setLines] = useState<string[]>([]);
  const [seen, setSeen] = useState<string[]>([]);

  useEffect(() => {
    if (!target) return;
    let lastMoveKey = '';
    const push = (line: string, key?: string) => {
      setLines((prev) => [line, ...prev].slice(0, 14));
      if (key) setSeen((prev) => (prev.includes(key) ? prev : [...prev, key]));
    };

    const onPointer = (e: PointerEvent) => {
      const key = `${e.pointerType} buttons=${e.buttons}`;
      // pointermove çok sık gelir; yalnızca düğme durumu değişince yaz.
      if (e.type === 'pointermove') {
        if (key === lastMoveKey) return;
        lastMoveKey = key;
      }
      push(
        `${e.type.replace('pointer', '')} · ${e.pointerType || '""'} · button=${e.button} · buttons=${e.buttons} · p=${e.pressure.toFixed(2)}`,
        key,
      );
    };
    const onOther = (e: Event) => {
      const m = e as MouseEvent;
      push(`${e.type} · button=${m.button ?? '-'} · buttons=${m.buttons ?? '-'}`, e.type);
    };
    const onTouch = (e: TouchEvent) => {
      const t = e.changedTouches[0] as Touch & { touchType?: string };
      push(`${e.type} · touchType=${t?.touchType ?? '-'} · force=${t?.force?.toFixed(2) ?? '-'}`);
    };

    const pointerTypes = ['pointerdown', 'pointermove', 'pointerup', 'pointercancel'] as const;
    const otherTypes = ['contextmenu', 'auxclick', 'mousedown'] as const;
    pointerTypes.forEach((t) => target.addEventListener(t, onPointer, true));
    otherTypes.forEach((t) => target.addEventListener(t, onOther, true));
    target.addEventListener('touchstart', onTouch, { capture: true, passive: true });
    return () => {
      pointerTypes.forEach((t) => target.removeEventListener(t, onPointer, true));
      otherTypes.forEach((t) => target.removeEventListener(t, onOther, true));
      target.removeEventListener('touchstart', onTouch, true);
    };
  }, [target]);

  return (
    <div className="pointer-events-auto absolute bottom-2 left-2 z-10 max-h-[45%] w-[min(26rem,calc(100%-1rem))] overflow-auto rounded-lg bg-slate-900/90 p-2 font-mono text-[11px] leading-snug text-slate-100 shadow-lg">
      <div className="mb-1 flex items-center justify-between font-sans text-xs font-semibold text-amber-300">
        <span>Kalem tanılama</span>
        <button type="button" className="rounded bg-slate-700 px-1.5 py-0.5 text-slate-100" onClick={() => { setLines([]); setSeen([]); }}>
          Temizle
        </button>
      </div>
      <div className="mb-1 text-slate-300">Görülen: {seen.length ? seen.join(' | ') : '—'}</div>
      {lines.map((l, i) => (
        <div key={i} className={i === 0 ? 'text-white' : 'text-slate-400'}>
          {l}
        </div>
      ))}
    </div>
  );
}
