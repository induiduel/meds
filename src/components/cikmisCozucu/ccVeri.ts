import { cozucuDersYukle, cozucuDizinYukle, type CDers, type CDizin, type CSoru } from '../spots/cozucu/cozucuVeri';
import type { Brans } from '../spots/brans';

/**
 * Çıkmış çözücü (Sınava hazırlan): branş başına kurul sınavındaki soru sayısı kadar çıkmış sorudan paketler.
 * Paket tanımı src/data/cikmis_paket/k<N>.json (scripts/cikmis_paket/paketle.py) yalnız başvuru tutar (ders kodu + soru no);
 * metin, açıklama ve EMA sesleri sesli soru çözücünün ders dosyalarından okunur. Paket dersi SoruCozucu'ya `kaynak` ile
 * verilir: sorular 1..n yeniden numaralanır, her soru kendi ses klasörünü (`klasor`) ve asıl klip numarasını (`kn`) taşır.
 */
/** soru: [çözücü ders kodu, soru no, not türü, not dersi, not id] — a: sesli asistan noktası; y: slayttan yazılmış not (branşın `notlar`ı, anahtar "<kod>/<no>") */
export type PaketSoru = [string, number, ('a' | 'y')?, string?, string?];
type Klip = { v: string; sure: number; zaman: [number, number][] };
export interface YaziliNot { baslik: string; cumleler: string[]; sayfa: number[]; klip?: Klip }
export interface PaketTanim { no: number; sorular: PaketSoru[]; ders: number }
export interface BransPaket { brans: Brans; sinavSoru: number; soru: number; paketler: PaketTanim[]; notlar?: Record<string, YaziliNot> }
export interface KurulPaket { kurul: number; surum: string; branslar: BransPaket[] }

const DOSYA = import.meta.glob('../../data/cikmis_paket/k*.json') as Record<string, () => Promise<{ default: KurulPaket }>>;
export const ccKurullar = (): number[] =>
  Object.keys(DOSYA).map((k) => Number(/\/k(\d+)\.json$/.exec(k)?.[1])).filter(Boolean).sort((a, b) => a - b);

/** ek modül: çözücüde olmayan çıkmışlar (scripts/cikmis_paket/ek_uygula.py), çözücü ders biçiminde; paket başvurusu "ek:<klasör>" */
const EK_DOSYA = import.meta.glob('../../data/cikmis_paket/ek/*/*.json') as Record<string, () => Promise<{ default: CDers }>>;
const ekYukle = (brans: string, kl: string): Promise<CDers> => {
  const f = EK_DOSYA[`../../data/cikmis_paket/ek/${brans}/${kl}.json`];
  return f ? f().then((m) => m.default) : Promise.reject(new Error(`ek yok: ${kl}`));
};
const NOT_DOSYA = import.meta.glob('../../data/*_asistan/*.json') as Record<string, () => Promise<{ default: NotDosya }>>;
interface NotDosya {
  kod: string; baslik: string;
  noktalar?: { id: string; baslik: string; cumleler: string[] }[];
  klip?: Record<string, Klip>;
}
const notBellek = new Map<string, Promise<NotDosya | null>>();
const notYukle = (yol: string) => {
  let p = notBellek.get(yol);
  if (!p) { const f = NOT_DOSYA[yol]; p = f ? f().then((m) => m.default).catch(() => null) : Promise.resolve(null); notBellek.set(yol, p); }
  return p;
};

const bellek = new Map<number, Promise<KurulPaket>>();
export const ccKurulYukle = (kurul: number): Promise<KurulPaket> => {
  let p = bellek.get(kurul);
  if (!p) {
    const f = DOSYA[`../../data/cikmis_paket/k${kurul}.json`];
    p = f ? f().then((m) => m.default) : Promise.resolve({ kurul, surum: '', branslar: [] });
    p.catch(() => bellek.delete(kurul));
    bellek.set(kurul, p);
  }
  return p;
};

/** İlerleme ve adres kimliği: cp<kurul>-<branş>-<paket no> (çözücü ilerleme deposunda ders kodlarıyla çakışmaz) */
export const paketKod = (kurul: number, brans: string, no: number) => `cp${kurul}-${brans}-${no}`;
const kodCoz = (kod: string) => {
  const m = /^cp(\d+)-(.+)-(\d+)$/.exec(kod);
  return m ? { kurul: Number(m[1]), brans: m[2] as Brans, no: Number(m[3]) } : null;
};
export const paketAdi = (bp: BransPaket, p: PaketTanim) =>
  `Çıkmış paketi ${p.no}${p.sorular.length < bp.sinavSoru ? ' · kısa paket' : ''}`;

export const ccDizin = async (kurul: number, brans: Brans): Promise<CDizin> => {
  const [k, d] = await Promise.all([ccKurulYukle(kurul), cozucuDizinYukle(brans)]);
  const bp = k.branslar.find((b) => b.brans === brans);
  return {
    surum: k.surum, ortak: d.ortak, sesler: undefined,
    dersler: (bp?.paketler || []).map((p) => ({
      kod: paketKod(kurul, brans, p.no), no: p.no, baslik: bp ? paketAdi(bp, p) : `Çıkmış paketi ${p.no}`,
      soru: p.sorular.length, cikmis: p.sorular.length, ses: true,
    })),
  };
};

const KLIP = /^[a-z]-(\d+)(?:-[A-E])?$/;
export const ccDers = async (kod: string): Promise<CDers> => {
  const c = kodCoz(kod);
  if (!c) throw new Error(`paket yok: ${kod}`);
  const [k, dizin] = await Promise.all([ccKurulYukle(c.kurul), cozucuDizinYukle(c.brans)]);
  const bp = k.branslar.find((b) => b.brans === c.brans);
  const p = bp?.paketler.find((x) => x.no === c.no);
  if (!bp || !p) throw new Error(`paket yok: ${kod}`);
  const kaynaklar = new Map<string, CDers>();
  await Promise.all([...new Set(p.sorular.map((r) => r[0]))].map(async (dk) => {
    kaynaklar.set(dk, await (dk.startsWith('ek:') ? ekYukle(c.brans, dk.slice(3)) : cozucuDersYukle(dk, c.brans)));
  }));
  const notYol = (r: PaketSoru) => (r[2] === 'a' ? `../../data/${c.brans}_asistan/${r[3]}.json` : '');
  const notlar = new Map<string, NotDosya | null>();
  await Promise.all([...new Set(p.sorular.map(notYol).filter(Boolean))].map(async (y) => { notlar.set(y, await notYukle(y)); }));
  const sorular: CSoru[] = [];
  const klip: CDers['klip'] = {};
  p.sorular.forEach((r, i) => {
    const [dk, no] = r;
    const d = kaynaklar.get(dk);
    const q = d?.sorular.find((x) => x.no === no);
    if (!d || !q) return; // çözücüde silinmiş soru: paket yeniden üretilene dek atlanır
    const klasor = d.klasor || d.kod;
    const dersNo = dizin.dersler.find((x) => x.kod === dk)?.no ?? d.no;
    const asilKod = dk.startsWith('ek:') ? (dizin.dersler.find((x) => x.no === d.no)?.kod ?? d.kod) : d.kod;
    const nd = notlar.get(notYol(r));
    let not: CSoru['not'];
    if (nd && r[2] === 'a') {
      const n = nd.noktalar?.find((x) => x.id === r[4]);
      const k = nd.klip?.[`a-${r[4]}`];
      if (n) {
        not = { baslik: n.baslik, cumleler: n.cumleler, kaynak: `Sesli sınav asistanı · ${nd.baslik}`, klasor: k ? `@a/${nd.kod}` : undefined, klip: k ? `a-${r[4]}` : undefined };
        if (k) klip[`@a/${nd.kod}/a-${r[4]}`] = k;
      }
    } else if (r[2] === 'y') {
      const y = bp.notlar?.[`${dk}/${no}`];
      if (y) {
        not = { baslik: y.baslik, cumleler: y.cumleler, kaynak: `${d.baslik} slaytları${y.sayfa.length ? ` · s. ${y.sayfa.join(', ')}` : ''}`, klasor: y.klip ? klasor : undefined, klip: y.klip ? `n-${no}` : undefined };
        if (y.klip) klip[`${klasor}/n-${no}`] = y.klip;
      }
    }
    sorular.push({ ...q, no: i + 1, kn: q.no, klasor, kaynak: { kod: asilKod, no: q.no, baslik: d.baslik, dersNo }, not });
    for (const [ad, v] of Object.entries(d.klip)) {
      const m = KLIP.exec(ad);
      if (m && Number(m[1]) === no) klip[`${klasor}/${ad}`] = v;
    }
  });
  return { kod, no: p.no, baslik: paketAdi(bp, p), sorular, klip };
};
