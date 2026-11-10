/**
 * Düğmesiz masa düzenleme (yedili / takim / yuzbir): seçili el taşları tek başına per olmuyorsa masadan 1 (olmazsa 2) taş
 * ödünç alınarak per kurulur. Taşı verilen perler geçerli kalmalıdır: 4'lü grup 3'e iner, seri uçtan kısalır ya da iki
 * geçerli parçaya bölünür. Saf; tarayıcıda da çalışır. Dönen değer `duzenle` hamlesinin per listesidir (son eleman yeni per).
 */
import type { Per, Tas } from '../tipler';
import { perTuru } from './okeyOrtak';
import { etkin, gercek, perCoz, type Okey } from './yuzbirAsistan';

/** Masadaki seri/grup geçerli mi (yedili: jokersiz; 101: jokerli çözüm, çift sayılmaz) */
export function masaPerGecerli(ts: Tas[], okey: Okey | null | undefined): boolean {
  if (!okey) return !!perTuru(ts);
  if (ts.length < 3) return false;
  const c = perCoz(ts, okey);
  return !!c && c.tur !== 'cift';
}

/** `perler`: masadaki seri ve gruplar (çiftler verilmez). `zorunlu`: yalnız bu masa taşını kullanan çözümler. */
export function oduncBul(el: Tas[], perler: Per[], okey?: Okey | null, zorunlu?: number): number[][] | null {
  if (!el.length) return null;
  const gecerli = (ts: Tas[]) => masaPerGecerli(ts, okey);
  /** Perden taşlar çıkınca kalan parçalar (hepsi geçerliyse), değilse null */
  const kalan = (p: Per, cikan: Set<number>): number[][] | null => {
    const parca: Tas[][] = p.tur === 'seri' ? [[]] : [p.taslar.filter((t) => !cikan.has(t.id))];
    if (p.tur === 'seri') for (const t of p.taslar) { if (cikan.has(t.id)) parca.push([]); else parca[parca.length - 1].push(t); }
    const dolu = parca.filter((x) => x.length);
    return dolu.every(gecerli) ? dolu.map((x) => x.map((t) => t.id)) : null;
  };
  const dene = (al: { p: Per; t: Tas }[]): number[][] | null => {
    if (zorunlu !== undefined && !al.some((x) => x.t.id === zorunlu)) return null;
    if (!gecerli([...el, ...al.map((x) => x.t)])) return null;
    const out: number[][] = [];
    for (const p of perler) {
      const cikan = new Set(al.filter((x) => x.p === p).map((x) => x.t.id));
      const k = cikan.size ? kalan(p, cikan) : [p.taslar.map((t) => t.id)];
      if (!k) return null;
      out.push(...k);
    }
    return [...out, [...el, ...al.map((x) => x.t)].map((t) => t.id)];
  };
  // Aday: seçili taşlarla aynı renkte ya da aynı sayıda olan masa taşları (eldeki okey her taşla uyar)
  const aday = perler.flatMap((p) => p.taslar.map((t) => ({ p, t }))).filter(({ t }) => {
    const d = okey ? etkin(t, okey) : t;
    return el.some((e) => { const x = okey ? gercek(e, okey) : e; return !x || x.r === d.r || x.s === d.s; });
  });
  for (const a of aday) { const r = dene([a]); if (r) return r; }
  if (aday.length <= 60) for (let i = 0; i < aday.length; i++) for (let j = i + 1; j < aday.length; j++) { const r = dene([aday[i], aday[j]]); if (r) return r; }
  return null;
}
