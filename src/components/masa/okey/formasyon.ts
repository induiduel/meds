/**
 * Istaka formasyonları: eli anlamlı kümelere ayırır (her küme ıstakada boşlukla ayrı durur).
 * - akilli: hazır perler → yarım seriler (aynı renk, arası ≤2: 4-5, 4-6) → yarım gruplar (aynı sayı, farklı renk)
 *           → çiftler (birebir aynı taş) → kalan tekler (renge göre) → jokerler
 * - cift:   birebir aynı taş çiftleri önce (çifte gitmek için), sonra kalanlar renge göre
 * - yuksek: en değerli taşlar başta (açılış sayısı toplarken atılacakları sona iter)
 * Değer fonksiyonu jokeri null döndürür.
 */
export type Deger = { s: number; r: number } | null;
type T = { id: number; d: Deger };

const renkSira = (a: T, b: T) => a.d!.r - b.d!.r || a.d!.s - b.d!.s || a.id - b.id;

export function formasyon(ids: number[], deger: (id: number) => Deger, kip: 'akilli' | 'cift' | 'yuksek', hazir: number[][] = []): number[][] {
  const kul = new Set(hazir.flat());
  const taslar: T[] = ids.filter((id) => !kul.has(id)).map((id) => ({ id, d: deger(id) }));
  const jok = taslar.filter((t) => !t.d);
  let kalan = taslar.filter((t) => t.d);
  const out: number[][] = [...hazir.filter((g) => g.length)];
  const al = (l: T[]) => { const s = new Set(l.map((t) => t.id)); kalan = kalan.filter((t) => !s.has(t.id)); };

  const ciftler = () => {
    const by = new Map<string, T[]>();
    for (const t of kalan.slice().sort(renkSira)) { const k = `${t.d!.s}-${t.d!.r}`; by.set(k, [...(by.get(k) || []), t]); }
    const l: number[][] = [];
    for (const g of by.values()) if (g.length >= 2) { l.push([g[0].id, g[1].id]); al(g.slice(0, 2)); }
    return l;
  };

  if (kip === 'yuksek') {
    const s = kalan.slice().sort((a, b) => b.d!.s - a.d!.s || a.d!.r - b.d!.r || a.id - b.id);
    // Aynı sayıdakiler bir küme
    for (const t of s) { const son = out[out.length - 1]; if (son && out.length > hazir.length && deger(son[0])?.s === t.d!.s) son.push(t.id); else out.push([t.id]); }
    if (jok.length) out.unshift(jok.map((t) => t.id));
    return out;
  }

  if (kip === 'cift') {
    out.push(...ciftler());
  } else {
    // Yarım seriler: renk renk sırala, ardışık iki taş arası 1–2 ise eşleştir (aynı taşın ikizi atlanır)
    const seri: number[][] = [];
    for (let r = 0; r < 4; r++) {
      const l = kalan.filter((t) => t.d!.r === r).sort(renkSira);
      const tekil: T[] = [];
      for (const t of l) if (!tekil.length || tekil[tekil.length - 1].d!.s !== t.d!.s) tekil.push(t);
      for (let i = 0; i + 1 < tekil.length; i++) {
        const fark = tekil[i + 1].d!.s - tekil[i].d!.s;
        if (fark >= 1 && fark <= 2) { seri.push([tekil[i].id, tekil[i + 1].id]); i++; }
      }
      // 12/13 ile 1 (döngü) yarım serisi
      const bir = tekil.find((t) => t.d!.s === 1), on3 = tekil.find((t) => t.d!.s === 13);
      if (bir && on3 && !seri.flat().includes(bir.id) && !seri.flat().includes(on3.id)) seri.push([on3.id, bir.id]);
    }
    for (const g of seri) al(g.map((id) => kalan.find((t) => t.id === id)!).filter(Boolean));
    out.push(...seri);
    // Yarım gruplar: aynı sayı, farklı renk
    const by = new Map<number, T[]>();
    for (const t of kalan.slice().sort(renkSira)) by.set(t.d!.s, [...(by.get(t.d!.s) || []), t]);
    for (const g of [...by.values()].sort((a, b) => a[0].d!.s - b[0].d!.s)) {
      const fr: T[] = [];
      for (const t of g) if (!fr.some((x) => x.d!.r === t.d!.r)) fr.push(t);
      if (fr.length >= 2) { out.push(fr.map((t) => t.id)); al(fr); }
    }
    out.push(...ciftler());
  }
  // Tekler: renk renk birer küme
  const tekBlok = new Set<number[]>();
  const tek = kalan.slice().sort(renkSira);
  for (const t of tek) { const son = out[out.length - 1]; const o = son && deger(son[son.length - 1]); if (son && out.length > 0 && o && o.r === t.d!.r && tekBlok.has(son)) son.push(t.id); else { const y = [t.id]; tekBlok.add(y); out.push(y); } }
  if (jok.length) out.push(jok.map((t) => t.id));
  return out;
}
