import type { Brans } from '../brans';

/**
 * Sesli çözücü sorusu / sesli asistan noktası → Öğren slaytı eşlemesi (branş başına tembel dosya).
 * Üretim: scripts/spot_cozucu/ogren_esle.py → src/data/cozucu_ogren/<brans>.json
 *  dersler[<kod>].s[<soruNo>] · dersler[<kod>].n[<noktaId>] = [[desteSırası, slaytNo, puan], …] (puan 0–100, iyi olan önce)
 */
export interface OgrenYer { deck: string; slayt: number; puan: number }
interface Dosya { desteler: string[]; dersler: Record<string, { s?: Record<string, [number, number, number][]>; n?: Record<string, [number, number, number][]> }> }

const DOSYA = import.meta.glob('../../../data/cozucu_ogren/*.json') as Record<string, () => Promise<{ default: Dosya }>>;
const bellek = new Map<Brans, Promise<Dosya | null>>();
const yukle = (brans: Brans) => {
  let p = bellek.get(brans);
  if (!p) {
    const f = DOSYA[`../../../data/cozucu_ogren/${brans}.json`];
    p = f ? f().then((m) => m.default).catch(() => { bellek.delete(brans); return null; }) : Promise.resolve(null);
    bellek.set(brans, p);
  }
  return p;
};
export const ogrenEslemeVar = (brans: Brans) => !!DOSYA[`../../../data/cozucu_ogren/${brans}.json`];

/** tur: s = çözücü sorusu (kod = çözücü dosyası, ör. "u04-1") · n = asistan noktası (kod = ders, ör. "u04") */
export const ogrenYerleri = async (brans: Brans, kod: string, tur: 's' | 'n', id: string | number): Promise<OgrenYer[]> => {
  const d = await yukle(brans);
  const l = d?.dersler[kod]?.[tur]?.[String(id)] || [];
  return l.map(([i, slayt, puan]) => ({ deck: d!.desteler[i], slayt, puan })).filter((x) => x.deck);
};
