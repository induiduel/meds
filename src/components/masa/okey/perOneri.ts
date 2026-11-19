/**
 * 1–2 seçili taştan per önerisi: seçili taşları içeren 3'lü seriler ve gruplar; her öneride eldeki taşlar (id'li) ve
 * eksik taşlar (id'siz) ayrı işaretlenir. Eldeki joker sayısı eksiği kapatabilir. Eksik az olan önce gelir.
 */
export type Deger = { s: number; r: number } | null;
export interface OneriTas { s: number; r: number; id?: number }
export interface Oneri { tur: 'seri' | 'grup'; taslar: OneriTas[]; eksik: number; jokerle: boolean }

export function perOnerileri(secili: number[], el: { id: number }[], deger: (id: number) => Deger, enCok = 3): Oneri[] {
  if (secili.length < 1 || secili.length > 2) return [];
  const sec = secili.map((id) => ({ id, d: deger(id) }));
  if (sec.some((x) => !x.d)) return [];
  const sd = sec.map((x) => x.d!);
  const seciliSet = new Set(secili);
  const diger = el.filter((t) => !seciliSet.has(t.id)).map((t) => ({ id: t.id, d: deger(t.id) }));
  const joker = diger.filter((x) => !x.d).length;
  const bul = (s: number, r: number, kul: Set<number>) => diger.find((x) => x.d && x.d.s === s && x.d.r === r && !kul.has(x.id));
  const out: Oneri[] = [];
  const kur = (tur: Oneri['tur'], hedef: { s: number; r: number }[]) => {
    const kul = new Set<number>(), kalanSec = [...sec];
    const taslar: OneriTas[] = hedef.map(({ s, r }) => {
      const i = kalanSec.findIndex((x) => x.d!.s === s && x.d!.r === r);
      if (i >= 0) return { s, r, id: kalanSec.splice(i, 1)[0].id };
      const e = bul(s, r, kul);
      if (e) { kul.add(e.id); return { s, r, id: e.id }; }
      return { s, r };
    });
    if (kalanSec.length) return;
    const eksik = taslar.filter((t) => t.id === undefined).length;
    out.push({ tur, taslar, eksik, jokerle: eksik > 0 && eksik <= joker });
  };
  // Seri: aynı renk, farklı sayılar, 3'lü pencere
  if (sd.every((d) => d.r === sd[0].r) && new Set(sd.map((d) => d.s)).size === sd.length) {
    const min = Math.min(...sd.map((d) => d.s)), max = Math.max(...sd.map((d) => d.s));
    const boy = Math.max(3, max - min + 1);
    if (boy <= 5) for (let bas = Math.max(1, max - boy + 1); bas <= Math.min(min, 14 - boy); bas++) kur('seri', Array.from({ length: boy }, (_, k) => ({ s: bas + k, r: sd[0].r })));
  }
  // Grup: aynı sayı, farklı renkler; eksik renklerden eldekiler önce
  if (sd.every((d) => d.s === sd[0].s) && new Set(sd.map((d) => d.r)).size === sd.length) {
    const s = sd[0].s, var_ = new Set(sd.map((d) => d.r));
    const diger4 = [0, 1, 2, 3].filter((r) => !var_.has(r)).sort((a, b) => (bul(s, b, new Set()) ? 1 : 0) - (bul(s, a, new Set()) ? 1 : 0));
    const eldeOlan = diger4.filter((r) => bul(s, r, new Set()));
    const hedefR = [...sd.map((d) => d.r), ...diger4.slice(0, Math.max(3 - sd.length, Math.min(4 - sd.length, eldeOlan.length)))];
    kur('grup', hedefR.map((r) => ({ s, r })));
  }
  return out.sort((a, b) => a.eksik - b.eksik || b.taslar.length - a.taslar.length).slice(0, enCok);
}
