import React, { useCallback, useState } from 'react';
import { LayoutList, Rows3 } from 'lucide-react';

/** Çıkmış sorular görünümü: "Kart" (zengin kart, varsayılan) | "Kompakt" (eski kart). Cihazda hatırlanır. */
export type CikmisGorunum = 'kart' | 'kompakt';
const KEY = 'medsoru_cikmis_gorunum';

export function useCikmisGorunum(): [CikmisGorunum, (v: CikmisGorunum) => void] {
  const [v, setV] = useState<CikmisGorunum>(() => {
    try { return localStorage.getItem(KEY) === 'kompakt' ? 'kompakt' : 'kart'; } catch { return 'kart'; }
  });
  const set = useCallback((next: CikmisGorunum) => {
    setV(next);
    try { localStorage.setItem(KEY, next); } catch { /* gizli pencere */ }
  }, []);
  return [v, set];
}

/** Araç bölmesindeki seçici (styles/toolbar.css → .pt-view) */
export const CikmisViewSwitch: React.FC<{ value: CikmisGorunum; onChange: (v: CikmisGorunum) => void }> = ({ value, onChange }) => (
  <div className="pt-view" role="radiogroup" aria-label="Görünüm">
    {([['kart', 'Kart', LayoutList], ['kompakt', 'Kompakt', Rows3]] as const).map(([id, label, Icon]) => (
      <button
        key={id}
        type="button"
        role="radio"
        aria-checked={value === id}
        className={value === id ? 'is-on' : ''}
        onClick={() => onChange(id)}
        title={id === 'kart' ? 'Kart: şıklar, açıklama ve işlemler doğrudan görünür' : 'Kompakt: sıkı liste'}
      >
        <Icon aria-hidden />
        <span className="ck-view-l">{label}</span>
      </button>
    ))}
  </div>
);
