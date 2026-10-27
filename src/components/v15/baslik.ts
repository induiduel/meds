import { useEffect, useSyncExternalStore } from 'react';

/**
 * v15 üst bar başlığı: sayfa kendi başlığını, alt satırını ve geri adresini buraya yazar (TopBarV15 okur).
 * Yazılmazsa üst bar rota başlığını (ROUTE_TITLES) gösterir. Sayfa kapanınca kayıt silinir.
 */
export interface V15Baslik {
  baslik: string;
  alt?: string;
  /** Geri düğmesinin gideceği görünen adres (yoksa düğme çizilmez) */
  geri?: string;
}

let cur: V15Baslik | null = null;
const subs = new Set<() => void>();
const yay = () => subs.forEach((f) => f());

export const useV15BaslikOku = () =>
  useSyncExternalStore(
    (f) => {
      subs.add(f);
      return () => subs.delete(f);
    },
    () => cur,
    () => null,
  );

/** Sayfa bileşeninde çağrılır; değerler değiştikçe güncellenir. `null` verilirse yazmaz. */
export function useV15Baslik(b: V15Baslik | null) {
  const k = b ? `${b.baslik}|${b.alt || ''}|${b.geri || ''}` : '';
  useEffect(() => {
    if (!b) return;
    cur = b;
    yay();
    return () => {
      if (cur === b || (cur && `${cur.baslik}|${cur.alt || ''}|${cur.geri || ''}` === k)) {
        cur = null;
        yay();
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [k]);
}
