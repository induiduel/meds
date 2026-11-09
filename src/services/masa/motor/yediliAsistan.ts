/** Yedili Okey / Takım Yedili: istemci ve motorun ortak saf yardımcıları (ipucu, zorunluluk, en iyi plan, ıstaka sıralama). */
import type { OkeyGorunum, OkeyHamle, Per, Tas } from '../tipler';
import { bolunmus, imza, islemeYerleri, islenmis, perDiz, perTuru, sonrakiPerId, type IslemeUcu } from './okeyOrtak';

export { perTuru, perDiz, islemeYerleri };

/** Elde açılabilecek tüm farklı perler (özdeş kopyalar tek sayılır; alt seriler ve 4'lüden çıkan 3'lüler dahil) */
export function eldekiPerler(el: Tas[]): Tas[][] {
  const ilk = new Map<number, Tas>();
  for (const t of el) if (!ilk.has(imza(t))) ilk.set(imza(t), t);
  const al = (s: number, r: number) => ilk.get(s * 4 + r)!;
  const out: Tas[][] = [];
  for (let r = 0; r < 4; r++) {
    let bas = 0;
    for (let s = 1; s <= 14; s++) {
      if (s <= 13 && ilk.has(s * 4 + r)) { if (!bas) bas = s; continue; }
      if (bas) for (let a = bas; a <= s - 3; a++) for (let b = a + 2; b < s; b++) out.push(Array.from({ length: b - a + 1 }, (_, i) => al(a + i, r)));
      bas = 0;
    }
  }
  for (let s = 1; s <= 13; s++) {
    const rr = [0, 1, 2, 3].filter((r) => ilk.has(s * 4 + r));
    if (rr.length < 3) continue;
    out.push(rr.map((r) => al(s, r)));
    if (rr.length === 4) for (const eksik of rr) out.push(rr.filter((r) => r !== eksik).map((r) => al(s, r)));
  }
  return out;
}

/** Çekirdek: görünüm kurmadan (motor da bunu çağırır) */
export function zorunluCekirdek(el: Tas[], perler: Per[], hak: boolean): { per: boolean; islek: boolean } {
  return { per: eldekiPerler(el).length > 0, islek: hak && el.some((t) => islemeYerleri(t, perler).length > 0) };
}

const hakVar = (g: OkeyGorunum, ben: string): boolean => {
  const o = g.oyuncular.find((x) => x.id === ben);
  return !!o && (o.acti || !!o.takimActi);
};

/** Elimde bekletilemeyecek hamle var mı (el bittiyse ikisi de false) */
export function zorunlu(g: OkeyGorunum, ben: string): { per: boolean; islek: boolean } {
  if (g.bitti) return { per: false, islek: false };
  return zorunluCekirdek(g.elim, g.perler, hakVar(g, ben));
}

export interface Ipucu { hamle: OkeyHamle; taslar: number[]; per?: number; aciklama: string }

/** Şu an yapılabilecek tüm ac/isle hamleleri (sıra bende değilse []) */
export function ipuclari(g: OkeyGorunum, ben: string): Ipucu[] {
  if (g.bitti || g.sira !== ben) return [];
  const out: Ipucu[] = [];
  for (const p of eldekiPerler(g.elim)) {
    const d = perDiz(p), taslar = d.map((t) => t.id);
    const aciklama = perTuru(d) === 'seri' ? `${d.length} taşlık seri aç (${d[0].s}–${d[d.length - 1].s})` : `${d.length} taşlık grup aç (${d[0].s})`;
    out.push({ hamle: { t: 'ac', taslar }, taslar, aciklama });
  }
  if (hakVar(g, ben)) for (const t of g.elim) for (const y of islemeYerleri(t, g.perler)) {
    const p = g.perler.find((x) => x.id === y.per)!.taslar;
    const aciklama = y.uc === 'bas' ? `${t.s} taşını serinin başına işle` : y.uc === 'son' ? `${t.s} taşını serinin sonuna işle`
      : y.uc === 'bol' ? `${t.s} taşını ${p[0].s}–${p[p.length - 1].s} serisini bölerek işle` : `${t.s} taşını gruba dördüncü taş olarak işle`;
    out.push({ hamle: { t: 'isle', tas: t.id, per: y.per }, taslar: [t.id], per: y.per, aciklama });
  }
  return out;
}

const DUGUM_TAVANI = 1500;

/** İşlemeden sonraki masa (girdi değişmez); bölmede üst parça yeni per olarak sona eklenir */
function islenmisMasa(m: Per[], perId: number, tas: Tas, uc: IslemeUcu, ben: string): Per[] {
  const p = m.find((x) => x.id === perId)!;
  if (uc !== 'bol') return m.map((x) => (x === p ? { ...x, taslar: islenmis(x, tas) } : x));
  const [alt, ust] = bolunmus(p, tas);
  return [...m.map((x) => (x === p ? { ...x, taslar: alt } : x)), { id: sonrakiPerId(m), tur: 'seri', taslar: ust, sahip: ben }];
}

/**
 * Çekirdek plan: her plan "önce açılacak perler, sonra işlemeler" biçimine sokulabilir (işleme el taşını azaltır, per açmayı etkinleştirmez).
 * İşleme, seriyi bölmeyi de kapsar (üst parça yeni per; kimliği motorla aynı kuralla verilir).
 * 1. evre: ayrık per kümeleri (büyükten küçüğe; ilk yol açgözlü); her kümede 2. evre: bellekli işleme araması. Tavan aşılırsa eldeki en iyi.
 */
export function planCekirdek(el: Tas[], perler: Per[], hak: boolean, ben = ''): OkeyHamle[] {
  let dugum = 0;
  const adaylar = eldekiPerler(el).map((p) => p.map(imza)).sort((a, b) => b.length - a.length);
  const kalan = new Map<number, Tas[]>();
  for (const t of [...el].sort((a, b) => a.id - b.id)) kalan.set(imza(t), [...(kalan.get(imza(t)) ?? []), t]);
  const masa: Per[] = perler.map((p) => ({ ...p, taslar: p.taslar.slice() }));
  const bellek = new Map<string, OkeyHamle[]>();
  const BOS: OkeyHamle[] = [];

  const isle = (elK: Tas[], m: Per[]): OkeyHamle[] => {
    dugum++; // yaprak taramaları da iş sayılır
    const hamleler: { t: Tas; per: number; uc: IslemeUcu }[] = [];
    const gorulen = new Set<number>();
    for (const t of elK) {
      if (gorulen.has(imza(t))) continue;
      gorulen.add(imza(t));
      for (const y of islemeYerleri(t, m)) hamleler.push({ t, per: y.per, uc: y.uc });
    }
    if (!hamleler.length) return BOS;
    const anahtar = elK.map((t) => t.id).join(',') + '|' + m.map((p) => p.taslar.map((t) => t.id).join('.')).join('/');
    const onceki = bellek.get(anahtar);
    if (onceki) return onceki;
    let eni = BOS;
    for (const h of hamleler) {
      const alt = isle(elK.filter((x) => x !== h.t), islenmisMasa(m, h.per, h.t, h.uc, ben));
      if (alt.length + 1 > eni.length) eni = [{ t: 'isle', tas: h.t.id, per: h.per }, ...alt];
      if (dugum > DUGUM_TAVANI) break; // tavan: ilk (açgözlü) yol
    }
    bellek.set(anahtar, eni);
    return eni;
  };

  let eniN = 0, eniPlan: OkeyHamle[] = [];
  const acilan: OkeyHamle[] = [];
  let acilanTas = 0;
  const ara = (i0: number): void => {
    const islemeler = hak || acilan.length ? isle([...kalan.values()].flat().sort((a, b) => a.id - b.id), masa) : BOS;
    const n = acilanTas + islemeler.length, k = acilan.length + islemeler.length;
    if (n > eniN || (n === eniN && k < eniPlan.length)) { eniN = n; eniPlan = [...acilan, ...islemeler]; }
    for (let i = i0; i < adaylar.length; i++) {
      if (dugum > DUGUM_TAVANI) return;
      const a = adaylar[i];
      if (!a.every((im) => kalan.get(im)!.length)) continue;
      dugum++;
      const taslar = a.map((im) => kalan.get(im)!.shift()!);
      masa.push({ id: sonrakiPerId(masa), tur: perTuru(taslar)!, taslar: perDiz(taslar), sahip: ben });
      acilan.push({ t: 'ac', taslar: taslar.map((t) => t.id) });
      acilanTas += a.length;
      ara(i);
      acilanTas -= a.length;
      acilan.pop();
      masa.pop();
      a.forEach((im, j) => kalan.get(im)!.unshift(taslar[j]));
    }
  };
  ara(0);
  return eniPlan;
}

/** Bu turda en çok taşı eriten ac/isle dizisi (açılan pere işleme dahil); eşitlikte daha az hamle. Sıra bende değilse [] */
export function enIyiPlan(g: OkeyGorunum, ben: string): OkeyHamle[] {
  if (g.bitti || g.sira !== ben) return [];
  return planCekirdek(g.elim, g.perler, hakVar(g, ben), ben);
}

/** Istaka otomatik sıralama: 'seri' renk→sayı, 'grup' sayı→renk; taş kimlikleri */
export function elSirala(el: Tas[], kip: 'seri' | 'grup'): number[] {
  return [...el].sort((a, b) => (kip === 'seri' ? a.r - b.r || a.s - b.s : a.s - b.s || a.r - b.r) || a.id - b.id).map((t) => t.id);
}
