import React, { useEffect, useRef, useState } from 'react';
import { Info } from 'lucide-react';

/**
 * Değişikliğin olduğu yerdeki bilgi simgesi: tıklayınca o değişikliğin ayrıntısı (önce / sonra / not) açılır.
 * Esc ya da dışarı tıklama kapatır. Faz 14 düzeltmeleri için hem /cikmis hem /test/cikmis kullanır.
 */
export function ChangeInfo({ title, before, after, note, align = 'right' }: { title: string; before?: string; after?: string; note?: string; align?: 'left' | 'right' }) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    if (!open) return;
    const close = (e: MouseEvent | KeyboardEvent) => {
      if (e instanceof KeyboardEvent ? e.key === 'Escape' : !ref.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener('mousedown', close);
    document.addEventListener('keydown', close);
    return () => {
      document.removeEventListener('mousedown', close);
      document.removeEventListener('keydown', close);
    };
  }, [open]);
  return (
    <span ref={ref} className="relative inline-flex align-middle shrink-0">
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          setOpen((v) => !v);
        }}
        className="w-7 h-7 inline-flex items-center justify-center rounded-full text-violet-600 hover:bg-violet-100 cursor-pointer"
        aria-label={`${title}: ayrıntıyı göster`}
        aria-expanded={open}
      >
        <Info className="w-4 h-4" />
      </button>
      {open && (
        <span
          role="dialog"
          className={`absolute z-30 top-7 ${align === 'right' ? 'right-0' : 'left-0'} w-[min(22rem,80vw)] p-3 rounded-lg bg-white border border-line shadow-lg text-[12.5px] font-normal normal-case tracking-normal text-ink-2 flex flex-col gap-1.5 text-left leading-snug`}
        >
          <b className="text-ink">{title}</b>
          {before !== undefined && (
            <span>
              <span className="text-ink-3">Önce:</span>{' '}
              {before ? <del className="bg-rose-50 text-rose-800 decoration-rose-400">{before}</del> : <i>(yoktu)</i>}
            </span>
          )}
          {after !== undefined && (
            <span>
              <span className="text-ink-3">Sonra:</span> <ins className="no-underline bg-emerald-50 text-emerald-900">{after}</ins>
            </span>
          )}
          {note && <span className="text-ink-3">{note}</span>}
        </span>
      )}
    </span>
  );
}
