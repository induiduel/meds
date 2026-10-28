/**
 * `tam-katman` kök sınıfı (alt sekme çubuğunu gizler, kurulum.css / kronometre.css / basarim.css) — referans sayaçlı.
 *
 * Kök neden (2026-10-28): bileşenler sınıfı doğrudan classList.add/remove ediyordu; iki tam katman üst üste açılıp
 * biri kapanınca sınıf silinir, alttaki katman hâlâ açıkken alt sekme geri gelirdi. Sınıf artık yalnız son katman
 * kapanınca kalkar. Yeni tam ekran katmanı bu kancayı kullanır; classList'e doğrudan dokunmaz.
 */
import { useEffect } from 'react';

let sayac = 0;

/** Bir tam katman açar; dönen işlev kapatır (bir kez çalışır). */
export function tamKatmanAc(): () => void {
  sayac += 1;
  if (typeof document !== 'undefined') document.documentElement.classList.add('tam-katman');
  let kapandi = false;
  return () => {
    if (kapandi) return;
    kapandi = true;
    sayac = Math.max(0, sayac - 1);
    if (sayac === 0 && typeof document !== 'undefined') document.documentElement.classList.remove('tam-katman');
  };
}

/** Bileşen bağlıyken (ve `acik` doğruyken) tam katman sayacını tutar. */
export function useTamKatman(acik = true): void {
  useEffect(() => (acik ? tamKatmanAc() : undefined), [acik]);
}
