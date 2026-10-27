import React, { useCallback, useState } from 'react';
import { Focus, LayoutList, PanelLeft, Rows3, Table2 } from 'lucide-react';

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

/**
 * Çıkmış sorular yerleşim modu (docs/tasarim/cikmis-alternatifler.html):
 *  liste (A, varsayılan) · panel (B, yan panel) · tablo (C, yoğun satır) · odak (D, tek soru).
 * Cihaz tercihi: userKvSync DEVICE_PREFS'te (profil eşitlemesine girmez).
 */
export type CikmisMod = 'liste' | 'panel' | 'tablo' | 'odak';
const MOD_KEY = 'medsoru_cikmis_mod';
const MODLAR: CikmisMod[] = ['liste', 'panel', 'tablo', 'odak'];

export function useCikmisMod(): [CikmisMod, (v: CikmisMod) => void] {
  const [v, setV] = useState<CikmisMod>(() => {
    try { const s = localStorage.getItem(MOD_KEY) as CikmisMod; return MODLAR.includes(s) ? s : 'liste'; } catch { return 'liste'; }
  });
  const set = useCallback((next: CikmisMod) => {
    setV(next);
    try { localStorage.setItem(MOD_KEY, next); } catch { /* gizli pencere */ }
  }, []);
  return [v, set];
}

const MOD_ADI: Record<CikmisMod, [string, string, React.FC<{ 'aria-hidden'?: boolean }>]> = {
  liste: ['Liste', 'Liste: yıl çipleri ve kart akışı', LayoutList],
  panel: ['Panel', 'Panel: solda yıl/konu paneli, sağda sorular', PanelLeft],
  tablo: ['Tablo', 'Tablo: her soru bir satır, dokununca açılır', Table2],
  odak: ['Odak', 'Odak: tek soru, önceki/sonraki', Focus],
};

/** Yerleşim seçici (simgeli segment). Etiketler dar ekranda gizlenir (.ck-view-l). */
export const CikmisModSwitch: React.FC<{ value: CikmisMod; onChange: (v: CikmisMod) => void }> = ({ value, onChange }) => (
  <div className="pt-view ck-mod" role="radiogroup" aria-label="Yerleşim">
    {MODLAR.map((id) => {
      const [label, title, Icon] = MOD_ADI[id];
      return (
        <button key={id} type="button" role="radio" aria-checked={value === id} className={value === id ? 'is-on' : ''} onClick={() => onChange(id)} title={title} aria-label={label}>
          <Icon aria-hidden />
          <span className="ck-view-l">{label}</span>
        </button>
      );
    })}
  </div>
);
