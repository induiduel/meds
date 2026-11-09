/** Jokersiz okey taşı yardımcıları (yedili/takim): taş seti, per geçerliliği, işleme uçları. Saf; tarayıcıda da çalışır. */
import type { Per, Renk, Rng, Tas } from '../tipler';

export const TAS_SAYISI = 104;
/** id 0–103: kopya × 52 + renk × 13 + (sayı − 1) */
export const tasYap = (id: number): Tas => ({ id, s: (id % 13) + 1, r: (Math.floor(id / 13) % 4) as Renk });
export const tasSeti = (): Tas[] => Array.from({ length: TAS_SAYISI }, (_, i) => tasYap(i));

/** Fisher–Yates, yerinde */
export function karistir<T>(d: T[], rng: Rng): T[] {
  for (let i = d.length - 1; i > 0; i--) {
    const j = Math.min(i, Math.floor(rng() * (i + 1)));
    [d[i], d[j]] = [d[j], d[i]];
  }
  return d;
}

/** Özdeş kopyaları eşleyen imza (sayı, renk) */
export const imza = (t: { s: number; r: number }): number => t.s * 4 + t.r;

const tasGecerli = (t: Tas): boolean => !!t && Number.isInteger(t.s) && t.s >= 1 && t.s <= 13 && Number.isInteger(t.r) && t.r >= 0 && t.r <= 3;

/** seri: aynı renk ardışık (1 yalnız altta) · grup: aynı sayı farklı renk (3–4) · değilse null */
export function perTuru(taslar: Tas[]): 'seri' | 'grup' | null {
  if (!Array.isArray(taslar) || taslar.length < 3 || taslar.length > 13 || !taslar.every(tasGecerli)) return null;
  if (new Set(taslar.map((t) => t.id)).size !== taslar.length) return null;
  const { s, r } = taslar[0];
  if (taslar.length <= 4 && taslar.every((t) => t.s === s) && new Set(taslar.map((t) => t.r)).size === taslar.length) return 'grup';
  if (!taslar.every((t) => t.r === r)) return null;
  const ss = taslar.map((t) => t.s).sort((a, b) => a - b);
  return ss.every((x, i) => i === 0 || x === ss[i - 1] + 1) ? 'seri' : null;
}

/** Geçerli peri saklama sırasına dizer (seri: küçükten büyüğe, grup: renk dizini) */
export function perDiz(taslar: Tas[]): Tas[] {
  const grup = perTuru(taslar) === 'grup';
  return [...taslar].sort((a, b) => (grup ? a.r - b.r : a.s - b.s) || a.id - b.id);
}

export type IslemeUcu = 'bas' | 'son' | 'bol' | null;

/** Taş bu pere işlenebiliyor mu: seri ucu ('bas' | 'son'), seriyi bölme ('bol': iç sayının kopyası, iki parça ≥3), grup (null); uymuyorsa undefined */
export function islemeUcu(tas: Tas, per: Per): IslemeUcu | undefined {
  const t = per.taslar;
  if (per.tur === 'seri') {
    if (tas.r !== t[0].r) return undefined;
    if (tas.s === t[0].s - 1 && tas.s >= 1) return 'bas';
    if (tas.s === t[t.length - 1].s + 1 && tas.s <= 13) return 'son';
    const x = tas.s - t[0].s;
    if (x >= 2 && t.length - 1 - x >= 2) return 'bol';
    return undefined;
  }
  if (per.tur === 'grup' && t.length === 3 && tas.s === t[0].s && t.every((x) => x.r !== tas.r)) return null;
  return undefined;
}

/** Taşın işlenebileceği perler (per = Per.id) */
export function islemeYerleri(tas: Tas, perler: Per[]): { per: number; uc: IslemeUcu }[] {
  const out: { per: number; uc: IslemeUcu }[] = [];
  for (const p of perler) {
    const uc = islemeUcu(tas, p);
    if (uc !== undefined) out.push({ per: p.id, uc });
  }
  return out;
}

/** İşlenmiş perin yeni taş dizisi (girdi değişmez; uygunluk çağırana aittir) */
export function islenmis(per: Per, tas: Tas): Tas[] {
  if (per.tur === 'seri') return tas.s < per.taslar[0].s ? [tas, ...per.taslar] : [...per.taslar, tas];
  return [...per.taslar, tas].sort((a, b) => a.r - b.r);
}

/** Bölme: alt parça [baş … s] işlenen taşla biter (eski per kimliğinde kalır), üst parça [s … son] eski s taşıyla başlar (yeni per) */
export function bolunmus(per: Per, tas: Tas): [Tas[], Tas[]] {
  const x = tas.s - per.taslar[0].s;
  return [[...per.taslar.slice(0, x), tas], per.taslar.slice(x)];
}

/** Yeni açılan (ya da bölmeyle doğan) perin kimliği: masadaki en büyük kimlik + 1 (motor ve istemci planı aynı kuralı kullanır) */
export const sonrakiPerId = (perler: Per[]): number => perler.reduce((m, p) => Math.max(m, p.id), -1) + 1;
