/**
 * Oynatma listesi denemesi: listedeki derslerin sesli çözücü sorularından tek bir deneme kurar (çıkmış paketleriyle aynı
 * yol: her soru kendi dersinin ses klasörünü ve kliplerini taşır, SoruCozucu `kaynak` ile açılır). Ses yolu branşa bağlı
 * olduğundan (`/api/cozucu-ses/<branş>/…`) deneme branş başına ayrı kurulur.
 */
import type { Brans } from '../spots/brans';
import { cozucuDersYukle, cozucuDizinYukle, ilerlemeOku, ozet, type CDers, type CSoru } from '../spots/cozucu/cozucuVeri';
import { dersCozucu } from './dersCozucu';
import type { CdListeDers } from './canliDersStore';

/** Ders başına en çok soru; deneme toplamı en çok */
const DERS_BASINA = 5;
const EN_COK = 40;
const KLIP = /^[a-z]-(\d+)(?:-[A-E])?$/;

export interface DenemeGrup { brans: Brans; kodlar: { kod: string; baslik: string }[]; soru: number }

/** Listedeki dersleri çözücü branşlarına gruplar (sorusu olmayan ders atlanır) */
export function denemeGruplari(dersler: CdListeDers[]): DenemeGrup[] {
  const m = new Map<Brans, DenemeGrup>();
  for (const d of dersler) {
    const c = dersCozucu(d.baslik, d.key);
    if (!c || !c.soru) continue;
    const u = new URLSearchParams(c.url.split('?')[1] || '');
    const brans = u.get('brans') as Brans | null;
    const kod = u.get('ders');
    if (!brans || !kod) continue;
    const g = m.get(brans) || { brans, kodlar: [], soru: 0 };
    if (!g.kodlar.some((x) => x.kod === kod)) {
      g.kodlar.push({ kod, baslik: d.baslik });
      g.soru += Math.min(DERS_BASINA, c.soru);
    }
    m.set(brans, g);
  }
  return [...m.values()].map((g) => ({ ...g, soru: Math.min(EN_COK, g.soru) }));
}

export const denemeKod = (listeId: string, brans: Brans) => `liste-${listeId}-${brans}`;

/** Deneme sonucu (çözücünün ilerleme deposundan) */
export function denemeSonuc(listeId: string, brans: Brans, toplam: number) {
  return ozet(ilerlemeOku()[denemeKod(listeId, brans)], toplam);
}

/** Örnek sorular önce, sonra benzer/çıkmış; derslerin sırası listedeki sıradır */
const sec = (sorular: CSoru[], n: number) => {
  const pay = (q: CSoru) => (q.tur === 'ornek' || !q.tur ? 0 : q.tur === 'benzer' ? 1 : 2);
  return sorular.slice().sort((a, b) => pay(a) - pay(b) || a.no - b.no).slice(0, n);
};

export async function denemeKur(listeId: string, ad: string, g: DenemeGrup): Promise<CDers> {
  const yuklu = await Promise.all(g.kodlar.map((k) => cozucuDersYukle(k.kod, g.brans).catch(() => null)));
  const dizin = await cozucuDizinYukle(g.brans).catch(() => null);
  const sorular: CSoru[] = [];
  const klip: CDers['klip'] = {};
  for (const d of yuklu) {
    if (!d) continue;
    const klasor = d.klasor || d.kod;
    const dersNo = dizin?.dersler.find((x) => x.kod === d.kod)?.no ?? d.no;
    for (const q of sec(d.sorular, DERS_BASINA)) {
      if (sorular.length >= EN_COK) break;
      sorular.push({ ...q, no: sorular.length + 1, kn: q.kn ?? q.no, klasor: q.klasor || klasor, kaynak: q.kaynak || { kod: d.kod, no: q.no, baslik: d.baslik, dersNo } });
      for (const [k, v] of Object.entries(d.klip)) {
        const m = KLIP.exec(k);
        if (m && Number(m[1]) === (q.kn ?? q.no)) klip[`${q.klasor || klasor}/${k}`] = v;
      }
    }
  }
  if (!sorular.length) throw new Error('Bu listedeki dersler için soru bulunamadı');
  return { kod: denemeKod(listeId, g.brans), no: 1, baslik: `${ad} · deneme`, sorular, klip };
}
