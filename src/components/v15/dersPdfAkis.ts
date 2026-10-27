/** Ders PDF akışı: Öğren slaytlarını ders sırasıyla dizer; her slaytın ardına paketteki `adim` anahtarı o slayta eşit kayıtları
 *  (terim, kısaltma, hastalık, sıralama, tablo, spot, kart) özet olarak ekler. Yapay zeka yok; saf gruplama.
 *  Hem tarayıcı (DersPdfEkranV15) hem Node (scripts/ders_pdf.mjs) kullanır — DOM/Vite bağımlılığı koyma. */
import type { DiPaket, DiSlayt } from './dersIcerik';

export interface PdfAdim {
  slayt: DiSlayt;
  terimler: DiPaket['terimler']; kisaltmalar: DiPaket['kisaltmalar']; hastaliklar: DiPaket['hastaliklar'];
  listeler: DiPaket['listeler']; tablolar: DiPaket['tablolar']; bilgiler: DiPaket['bilgiler']; onemli: DiPaket['onemli'];
  spotlar: DiPaket['spotlar']; kartlar: DiPaket['kartlar'];
}
export interface PdfAkis { baslik: string; adimlar: PdfAdim[]; ek: Omit<PdfAdim, 'slayt'> | null; quiz: { adim: number; q: DiPaket['quiz'][number] }[] }

type Ozet = Omit<PdfAdim, 'slayt'>;
const bos = (): Ozet => ({ terimler: [], kisaltmalar: [], hastaliklar: [], listeler: [], tablolar: [], bilgiler: [], onemli: [], spotlar: [], kartlar: [] });
const KALEMLER = Object.keys(bos()) as (keyof Ozet)[];
const doluMu = (o: Ozet) => KALEMLER.some((k) => o[k].length > 0);

export function dersPdfAkisi(paket: DiPaket, slaytlar: DiSlayt[]): PdfAkis {
  const sirali = slaytlar.filter((s) => !s.isGameFinale).sort((a, b) => a.slideNumber - b.slideNumber);
  const no = new Set(sirali.map((s) => s.slideNumber));
  const kovalar = new Map<number, Ozet>(sirali.map((s) => [s.slideNumber, bos()]));
  const ek = bos();
  for (const k of KALEMLER) {
    for (const x of (paket[k] || []) as (DiPaket['terimler'][number] & { adim?: number })[]) {
      const hedef = x.adim && no.has(x.adim) ? kovalar.get(x.adim)! : ek;
      (hedef[k] as unknown[]).push(x);
    }
  }
  const sinir = (l: PdfAdim['onemli']) => [...l].sort((a, b) => b.p - a.p);
  for (const o of [...kovalar.values(), ek]) o.onemli = sinir(o.onemli);
  return {
    baslik: paket.baslik || '',
    adimlar: sirali.map((slayt) => ({ slayt, ...kovalar.get(slayt.slideNumber)! })),
    ek: doluMu(ek) ? ek : null,
    quiz: paket.quiz.map((q) => ({ adim: q.adim || 0, q })).sort((a, b) => a.adim - b.adim),
  };
}
