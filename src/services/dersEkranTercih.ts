/**
 * Sesli ders ekran tercihleri (tasarım O10 tamEkranAyar). Cihazda kalır (userKvSync DEVICE_PREFS, profil eşitlemesine girmez).
 *  - otoTam: ders açılınca kendiliğinden tam ekran. Fullscreen API kullanıcı hareketi istediği için ilk dokunuşta/tuşta açılır.
 *  - yatayYan: yatay tutulan telefon/tablette PDF + metin yan yana (görünüm ne seçili olursa olsun).
 */
import { useEffect, useState } from 'react';

const ANAHTAR = { otoTam: 'medsoru_canli_ders_oto_tam', yatayYan: 'medsoru_canli_ders_yatay_yan' } as const;
export type DersEkranTercih = keyof typeof ANAHTAR;
const OLAY = 'medsoru:ders-ekran-tercih';

export const dersEkranTercih = (k: DersEkranTercih): boolean => { try { return localStorage.getItem(ANAHTAR[k]) === '1'; } catch { return false; } };
export function dersEkranTercihYaz(k: DersEkranTercih, v: boolean) {
  try { if (v) localStorage.setItem(ANAHTAR[k], '1'); else localStorage.removeItem(ANAHTAR[k]); } catch { /* yok */ }
  window.dispatchEvent(new CustomEvent(OLAY));
}
export function useDersEkranTercih(k: DersEkranTercih): [boolean, (v: boolean) => void] {
  const [v, setV] = useState(() => dersEkranTercih(k));
  useEffect(() => {
    const f = () => setV(dersEkranTercih(k));
    window.addEventListener(OLAY, f);
    window.addEventListener('storage', f);
    return () => { window.removeEventListener(OLAY, f); window.removeEventListener('storage', f); };
  }, [k]);
  return [v, (x: boolean) => dersEkranTercihYaz(k, x)];
}

/** Yatay tutulan dokunmatik cihaz (telefon/tablet) */
export const YATAY_DOKUNMATIK = '(orientation: landscape) and (pointer: coarse)';
export function useYatayDokunmatik(): boolean {
  const [v, setV] = useState(() => typeof window !== 'undefined' && window.matchMedia(YATAY_DOKUNMATIK).matches);
  useEffect(() => {
    const m = window.matchMedia(YATAY_DOKUNMATIK);
    const f = () => setV(m.matches);
    m.addEventListener('change', f);
    return () => m.removeEventListener('change', f);
  }, []);
  return v;
}
