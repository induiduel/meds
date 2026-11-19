/**
 * Masayı yeniden diz: masadaki TÜM taşları (zorunlu) ve isteğe bağlı eldeki taşları geçerli perlere yeniden bölüştürür.
 * Tam örtü arar (her masa taşı tam bir perde); eldeki taşlardan olabildiğince çoğunu masaya katar.
 * Her aday per oyunun kendi doğrulayıcısıyla (gecerli) sınanır; tohum değişince farklı bir dizilim çıkar.
 * Joker (deger null) eksik yuvaya geçer.
 */
export type Deger = { s: number; r: number } | null;
interface T { id: number; d: Deger; zorunlu: boolean }

export interface CozSecenek {
  masa: number[];
  el: number[];
  /** Elden en çok kaç taş kullanılabilir (101'de atacak taş kalmalı) */
  elSinir: number;
  deger(id: number): Deger;
  gecerli(ids: number[]): boolean;
  tohum: number;
  /** Bu dizilimle aynı çıkan çözüm reddedilir (aynı perler, yalnız sıra farklıysa da aynıdır) */
  mevcut: number[][];
  adimSinir?: number;
}

const imza = (l: number[][]) => l.map((g) => g.slice().sort((a, b) => a - b).join(',')).sort().join('|');

export function masayiCoz(o: CozSecenek): { perler: number[][]; elden: number[] } | null {
  let rnd = (o.tohum * 2654435761) >>> 0 || 1;
  const rand = () => { rnd ^= rnd << 13; rnd >>>= 0; rnd ^= rnd >> 17; rnd ^= rnd << 5; rnd >>>= 0; return rnd / 4294967296; };
  const karistir = <X,>(l: X[]) => { for (let i = l.length - 1; i > 0; i--) { const j = Math.floor(rand() * (i + 1)); [l[i], l[j]] = [l[j], l[i]]; } return l; };

  const tum: T[] = [...o.masa.map((id) => ({ id, d: o.deger(id), zorunlu: true })), ...o.el.map((id) => ({ id, d: o.deger(id), zorunlu: false }))];
  const kul = new Set<number>();
  const cozum: number[][] = [];
  const mevcut = imza(o.mevcut);
  let en: { perler: number[][]; elden: number; } | null = null;
  let adim = 0;
  const sinir = o.adimSinir ?? 8000;
  const bitis = Date.now() + 700;
  const elKul = () => cozum.flat().filter((id) => !tum.find((t) => t.id === id)!.zorunlu).length;
  const gecerliOnbellek = new Map<string, boolean>();
  const gecerli = (ids: number[]) => { const k = ids.slice().sort((a, b) => a - b).join(','); let v = gecerliOnbellek.get(k); if (v === undefined) { v = o.gecerli(ids); gecerliOnbellek.set(k, v); } return v; };

  /** t taşını içeren aday perler (kullanılmamış taşlardan) */
  const adaylar = (t: T): number[][] => {
    const bos = tum.filter((x) => !kul.has(x.id) && x.id !== t.id);
    const jok = bos.filter((x) => !x.d);
    const out: number[][] = [];
    const sec = (l: T[]) => { const z = l.filter((x) => x.zorunlu); const e = l.filter((x) => !x.zorunlu); return [...karistir(z), ...karistir(e)][0]; };
    const d = t.d!;
    // Grup: aynı sayı, farklı renk (3 ya da 4); eksik renk jokerle
    const renkler = [0, 1, 2, 3].filter((r) => r !== d.r);
    for (const boy of karistir([3, 4])) {
      const kombin = (k: number, bas: number, acc: number[]): void => {
        if (acc.length === k) {
          const ids = [t.id]; let j = 0; let olur = true;
          for (const r of acc) { const x = sec(bos.filter((y) => y.d && y.d.s === d.s && y.d.r === r && !ids.includes(y.id))); if (x) ids.push(x.id); else if (j < jok.length) ids.push(jok[j++].id); else { olur = false; break; } }
          if (olur) out.push(ids);
          return;
        }
        for (let i = bas; i < renkler.length; i++) kombin(k, i + 1, [...acc, renkler[i]]);
      };
      kombin(boy - 1, 0, []);
    }
    // Seri: aynı renk ardışık, t'yi içeren [a..b]
    for (let a = Math.max(1, d.s - 12); a <= d.s; a++) for (let b = Math.max(d.s, a + 2); b <= Math.min(13, a + 12); b++) {
      const ids = [t.id]; let j = 0; let olur = true;
      for (let v = a; v <= b; v++) { if (v === d.s) continue; const x = sec(bos.filter((y) => y.d && y.d.s === v && y.d.r === d.r && !ids.includes(y.id))); if (x) ids.push(x.id); else if (j < jok.length) ids.push(jok[j++].id); else { olur = false; break; } }
      if (!olur) { if (b > d.s) break; continue; }
      out.push(ids);
    }
    return karistir(out.filter((ids) => ids.length >= 3 && gecerli(ids)));
  };

  const ara = (): boolean => {
    if (++adim > sinir || Date.now() > bitis) return true;
    const kalan = tum.filter((t) => t.zorunlu && !kul.has(t.id) && t.d);
    if (!kalan.length) {
      // Zorunlu jokerler: mevcut bir pere eklenebiliyorsa ekle
      const jk = tum.filter((t) => t.zorunlu && !kul.has(t.id));
      const ekle: [number, number][] = [];
      for (const j of jk) { const i = cozum.findIndex((p, k) => !ekle.some((e) => e[0] === k) && gecerli([...p, j.id])); if (i < 0) return false; ekle.push([i, j.id]); }
      const perler = cozum.map((p, k) => [...p, ...ekle.filter((e) => e[0] === k).map((e) => e[1])]);
      const elden = elKul();
      if (elden > o.elSinir) return false;
      if (elden === 0 && imza(perler) === mevcut) return false;
      if (!en || elden > en.elden) en = { perler, elden };
      return en.elden >= Math.min(o.elSinir, o.el.length);
    }
    // En az seçenekli taştan başla (dallanmayı küçültür)
    let secilen = kalan[0], secAday: number[][] | null = null;
    for (const t of kalan.slice(0, 6)) { const a = adaylar(t); if (!secAday || a.length < secAday.length) { secilen = t; secAday = a; } if (!a.length) return false; }
    void secilen;
    for (const p of secAday!) {
      if (p.filter((id) => !tum.find((t) => t.id === id)!.zorunlu).length + elKul() > o.elSinir) continue;
      p.forEach((id) => kul.add(id)); cozum.push(p);
      const bitti = ara();
      cozum.pop(); p.forEach((id) => kul.delete(id));
      if (bitti) return true;
    }
    return false;
  };
  ara();
  if (!en) return null;
  const sonuc = en as { perler: number[][]; elden: number };
  const elSet = new Set(o.el);
  return { perler: sonuc.perler, elden: sonuc.perler.flat().filter((id) => elSet.has(id)) };
}
