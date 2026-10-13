import React, { useEffect, useRef, useState } from 'react';
import { Search, SlidersHorizontal, X } from 'lucide-react';
import { findDockSearchInput, setReactInputValue } from './useDockAutoHide';

/**
 * Yuva saklıyken üst çubukta görünen sayfa araması. Kendi durumu yoktur: sayfadaki asıl arama alanını
 * yansıtır (değer okur, yazınca asıl alana aktarır). Süzgeç düğmesi yuvayı geri getirir.
 */
export const PageSearchProxy: React.FC<{ onReveal: () => void }> = ({ onReveal }) => {
  const [value, setValue] = useState('');
  const [placeholder, setPlaceholder] = useState('Bu sayfada ara');
  const ref = useRef<HTMLInputElement>(null);
  const t = useRef<number | undefined>(undefined);
  useEffect(() => () => window.clearTimeout(t.current), []);

  useEffect(() => {
    const src = findDockSearchInput();
    if (!src) return;
    setValue(src.value);
    if (src.placeholder) setPlaceholder(src.placeholder);
    // Sayfa alanı başka yoldan değişirse (sekme, süzgeç temizle) vekil de güncellenir.
    const sync = () => setValue(src.value);
    src.addEventListener('input', sync);
    return () => src.removeEventListener('input', sync);
  }, []);

  const push = (v: string) => {
    setValue(v);
    const src = findDockSearchInput();
    if (src) setReactInputValue(src, v);
    // Sonuçlar listenin başından gösterilir: liste yukarıda kaldıysa oraya kayılır (yuva saklı kalır).
    window.clearTimeout(t.current);
    t.current = window.setTimeout(() => {
      const first = document.querySelector<HTMLElement>('.cx-list, .qk') || (document.querySelector('.pt-root')?.nextElementSibling as HTMLElement | null);
      if (!first) return;
      const top = first.getBoundingClientRect().top + window.scrollY - 72;
      if (window.scrollY > top + 8) window.scrollTo({ top: Math.max(0, top), behavior: 'auto' });
    }, 380);
  };

  return (
    <div className="sh-pq" role="search">
      <Search aria-hidden />
      <input
        ref={ref}
        type="search"
        value={value}
        placeholder={placeholder}
        aria-label={placeholder}
        onChange={(e) => push(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') findDockSearchInput()?.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
          if (e.key === 'Escape') ref.current?.blur();
        }}
      />
      {value && (
        <button type="button" className="sh-pq-x" onClick={() => { push(''); ref.current?.focus(); }} aria-label="Aramayı temizle"><X aria-hidden /></button>
      )}
      <button type="button" className="sh-pq-f" onClick={onReveal} aria-label="Süzgeçleri göster" title="Süzgeçleri göster"><SlidersHorizontal aria-hidden /></button>
    </div>
  );
};
