/**
 * Çıkmış soru → sesli ders konumu (tasarım C03 "Derste 04:18"). Sunucu dizini GET /api/canli-ders/cikmis-dizin
 * (bütün derslerin cikmis_konum eşleşmeleri; metni değişmiş ders hariç) bir kez çekilir, oturum boyunca bellekte.
 */
import { useEffect, useState } from 'react';
import { safeJsonFetch } from './api';

export interface DersKonum { k: string; b: string; p: number; c: number; t?: number }
let dizin: Record<string, DersKonum> | null = null;
let istek: Promise<Record<string, DersKonum>> | null = null;
const yukle = () => (istek ||= safeJsonFetch<{ q: Record<string, DersKonum> }>('/api/canli-ders/cikmis-dizin')
  .then((r) => (dizin = r.ok && r.data?.q ? r.data.q : {}))
  .catch(() => (dizin = {})));

export function useDersKonum(soruId: string | undefined): DersKonum | null {
  const [, tik] = useState(0);
  useEffect(() => { if (!dizin) void yukle().then(() => tik((n) => n + 1)); }, []);
  if (!soruId || !dizin) return null;
  // test bankası kimlikleri "cikmis:<id>" biçiminde: önek ayıklanır
  return dizin[soruId] || dizin[soruId.replace(/^[a-z]+:/, '')] || null;
}
export const dkSn = (t: number) => `${String(Math.floor(t / 60)).padStart(2, '0')}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
