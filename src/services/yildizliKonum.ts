/** Yıldızlı paragrafın kurul / ders (branş) / konu konumu. Kaynak: ders kayıt defteri (data/dersler/kN.json). */
import type { YildizliParagraf } from './yildizliParagrafStore';
import k1 from '../data/dersler/k1.json';
import k2 from '../data/dersler/k2.json';
import k3 from '../data/dersler/k3.json';
import k4 from '../data/dersler/k4.json';
import k5 from '../data/dersler/k5.json';
import k6 from '../data/dersler/k6.json';
import branslarVeri from '../data/dersler/branslar.json';

export interface YildizKonum { kurul: number; ders: string; konu: string }

interface Kayit { id: string; kod: string; kurul: number; brans: string; konu: string }
const KAYITLAR: Kayit[] = [k1, k2, k3, k4, k5, k6].flatMap((k: any) => k.dersler as Kayit[]);
const KOD = new Map(KAYITLAR.map((d) => [d.kod, d]));
const ID = new Map(KAYITLAR.map((d) => [d.id, d]));
const HARF_AD: Record<string, string> = Object.fromEntries(
  (branslarVeri as any).branslar.map((b: any) => [b.harf, b.ad]),
);
const K1_AD: Record<string, string> = {
  e: 'Enfeksiyon Hastalıkları', u: 'Üroloji', g: 'Tıbbi Genetik', h: 'Halk Sağlığı',
  k: 'Kadın Hastalıkları ve Doğum', f: 'Tıbbi Farmakoloji',
};

const konuAyir = (baslik: string) => {
  const t = baslik.split(/:\s|\s·\s/);
  return (t[1] ?? t[0]).trim() || baslik;
};

export function yildizKonum(p: YildizliParagraf): YildizKonum {
  const kod = p.meta?.dersKod;
  const key = p.meta?.dersKey;
  const kayit = (kod && KOD.get(kod)) || (key && ID.get(key.slice(0, 5))) || undefined;
  if (kayit) return { kurul: kayit.kurul, ders: kayit.brans, konu: konuAyir(p.baslik) };
  let kurul = 1;
  let ders = 'Diğer';
  const m = kod && /^(\d)([a-z])\d{2}/.exec(kod);
  const km = key && /^k(\d)-/.exec(key);
  if (m) { kurul = +m[1]; ders = HARF_AD[m[2]] || ders; }
  else if (km) kurul = +km[1];
  else if (kod) ders = K1_AD[kod[0]] || (/^\d/.test(kod) ? 'Tıbbi Patoloji' : ders);
  if (ders === 'Diğer' && p.meta?.brans) ders = p.meta.brans.replace(/^k\d/, '');
  return { kurul, ders, konu: konuAyir(p.baslik) };
}
