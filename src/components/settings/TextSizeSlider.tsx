import React from 'react';
import { Minus, Plus } from 'lucide-react';
import { TEXT_PX_MAX, TEXT_PX_MIN, TEXT_SIZE_ORDER, TEXT_SIZE_PX, useAppearance } from '../../utils/appearance';

/**
 * Okuma yazısı boyutu: 12–20 px arası 1 px adımlı kaydırıcı + küçült/büyüt düğmeleri + hazır adımlar.
 * Profil (v12) ve Ayarlar (v10/v11) aynı bileşeni kullanır; değer appearance.textPx'e yazılır.
 */
export const TextSizeSlider: React.FC<{ className?: string }> = ({ className }) => {
  const look = useAppearance();
  const px = look.textPx;
  const set = (n: number) => look.set({ textPx: n });
  return (
    <div className={`tss ${className || ''}`}>
      <div className="tss-row">
        <button type="button" className="tss-btn" onClick={() => set(px - 1)} disabled={px <= TEXT_PX_MIN} aria-label="Yazıyı 1 px küçült"><Minus aria-hidden /></button>
        <input
          type="range" className="tss-range" min={TEXT_PX_MIN} max={TEXT_PX_MAX} step={1} value={px}
          onChange={(e) => set(Number(e.target.value))} aria-label="Yazı boyutu" aria-valuetext={`${px} piksel`}
        />
        <button type="button" className="tss-btn" onClick={() => set(px + 1)} disabled={px >= TEXT_PX_MAX} aria-label="Yazıyı 1 px büyüt"><Plus aria-hidden /></button>
        <output className="tss-val" aria-live="polite">{px} px</output>
      </div>
      <div className="tss-steps" role="group" aria-label="Hazır boyutlar">
        {[TEXT_PX_MIN, ...TEXT_SIZE_ORDER.map((k) => TEXT_SIZE_PX[k])].filter((v, i, a) => a.indexOf(v) === i).map((v) => (
          <button key={v} type="button" className={`tss-step ${v === px ? 'is-on' : ''}`} aria-pressed={v === px} onClick={() => set(v)}>{v}</button>
        ))}
      </div>
    </div>
  );
};
