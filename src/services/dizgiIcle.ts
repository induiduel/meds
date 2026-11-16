/**
 * Dizgi içe alma (interning, 2026-11-16): dev JSON'lardan ayrıştırılan tekrarlı KISA dizgiler (tür, kurul, branş,
 * tarih, durum, şık harfi…) tek kopyaya indirilir. Değer aynı dizgi olduğundan JSON.stringify çıktısı ve
 * karşılaştırmalar değişmez; yalnız yinelenen kopyalar bırakılır. Ölçüm: çıkmış listesi ~33 MB, RAG parçaları ~30 MB.
 * Nesneler YERİNDE değiştirilir; havuz çağrı sonunda bırakılır (kalıcı bellek tutmaz).
 */
export const ICLE_UZUNLUK_TAVANI = 96;

export function dizgiHavuzu(tavan = ICLE_UZUNLUK_TAVANI) {
  const havuz = new Map<string, string>();
  const icle = (v: any): any => {
    if (typeof v === 'string') {
      if (v.length > tavan) return v;
      const x = havuz.get(v);
      if (x !== undefined) return x;
      havuz.set(v, v);
      return v;
    }
    if (Array.isArray(v)) { for (let i = 0; i < v.length; i++) v[i] = icle(v[i]); return v; }
    if (v && typeof v === 'object') { for (const k of Object.keys(v)) v[k] = icle(v[k]); return v; }
    return v;
  };
  return { icle, birak: () => havuz.clear(), boyut: () => havuz.size };
}

/** Listeyi derinlemesine içe alır (yerinde); kısa yol. */
export function listeyiIcle<T>(liste: T[], tavan = ICLE_UZUNLUK_TAVANI): T[] {
  const h = dizgiHavuzu(tavan);
  for (const o of liste) h.icle(o);
  h.birak();
  return liste;
}
