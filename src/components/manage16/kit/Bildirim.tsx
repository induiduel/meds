import React, { useEffect, useState } from 'react';
import { PANEL_ON_ORACLE_AT_BOOT, isLocalHost } from '../../../config/deployment';

type Eylem = { etiket: string; yap: () => void };
type B = { id: number; metin: string; ton: 'iyi' | 'kotu' | 'bilgi'; eylem?: Eylem };
let ekle: ((b: Omit<B, 'id'>) => void) | null = null;

/** Kısa bildirim (kabuktaki BildirimHost gösterir). eylem verilirse ("Geri al") bildirim 8 sn kalır. */
export function bildir(metin: string, ton: B['ton'] = 'iyi', eylem?: Eylem) { ekle?.({ metin, ton, eylem }); }

/** Panelin yazdığı sunucu: yerel makinede Canlı/Yerel seçimine göre, uzakta her zaman canlı (onay metinlerinde gösterilir) */
export const yazimHedefi = (): string => (!isLocalHost() || PANEL_ON_ORACLE_AT_BOOT ? 'canlı site' : 'yerel sunucu');

export const BildirimHost: React.FC = () => {
  const [l, setL] = useState<B[]>([]);
  useEffect(() => {
    let n = 0;
    ekle = (b) => { const id = ++n; setL((x) => [...x.slice(-3), { ...b, id }]); setTimeout(() => setL((x) => x.filter((y) => y.id !== id)), b.eylem ? 8000 : 3500); };
    return () => { ekle = null; };
  }, []);
  return (
    <div className="m16-bildirimler" aria-live="polite">
      {l.map((b) => (
        <div key={b.id} className={`m16-bildirim t-${b.ton}`}>
          {b.metin}
          {b.eylem && (
            <button type="button" className="m16-bildirim-eylem" onClick={() => { setL((x) => x.filter((y) => y.id !== b.id)); b.eylem!.yap(); }}>{b.eylem.etiket}</button>
          )}
        </div>
      ))}
    </div>
  );
};
