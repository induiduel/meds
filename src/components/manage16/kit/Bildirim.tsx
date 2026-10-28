import React, { useEffect, useState } from 'react';

type B = { id: number; metin: string; ton: 'iyi' | 'kotu' | 'bilgi' };
let ekle: ((b: Omit<B, 'id'>) => void) | null = null;

/** Kısa bildirim (kabuktaki BildirimHost gösterir) */
export function bildir(metin: string, ton: B['ton'] = 'iyi') { ekle?.({ metin, ton }); }

export const BildirimHost: React.FC = () => {
  const [l, setL] = useState<B[]>([]);
  useEffect(() => {
    let n = 0;
    ekle = (b) => { const id = ++n; setL((x) => [...x.slice(-3), { ...b, id }]); setTimeout(() => setL((x) => x.filter((y) => y.id !== id)), 3500); };
    return () => { ekle = null; };
  }, []);
  return <div className="m16-bildirimler" aria-live="polite">{l.map((b) => <div key={b.id} className={`m16-bildirim t-${b.ton}`}>{b.metin}</div>)}</div>;
};
