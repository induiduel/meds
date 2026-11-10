import { useSyncExternalStore } from 'react';
import dizinHam from '../../../data/ek_moduller/index.json';

/**
 * Ek modüller (Ders çalış › Ek modüller): kurul müfredatı dışındaki seçmeli/geçici derslerin verisi.
 * Kaynak: src/data/ek_moduller/index.json (modül listesi) + <modül>/b<N>.json (başlık: 2 konu), sinav_oncesi.json,
 * genel_sorular.json, klip.json (EMA klip dizini; scripts/ek_modul/ses.py yazar). Yazım kuralları: scripts/ek_modul/TALIMAT.md.
 * Ekran metni (`ekran`, `metin`, `cozum`) ile okuma metni (`ses`, `ses_cozum`) ayrıdır; ekranda okuma metni gösterilmez.
 */
export interface EkModulOzet {
  id: string;
  kurul: number;
  ad: string;
  tur: string;
  aciklama: string;
  kapak: string;
  sinavSoru: number;
  pdf: { id: string; ad: string; aciklama: string; dosya: string }[];
}
export interface EkSoru {
  no: number;
  zorluk: 'kolay' | 'orta' | 'zor';
  kok: string;
  secenekler: Record<string, string>;
  dogru: string;
  cozum: string;
  siklar: Record<string, string>;
  ses_cozum: string;
  /** genel sorularda sorunun dayandığı konu (ör. "4b") */
  konu?: string;
}
export type EkEtkinlik =
  | { tur: 'dogru_yanlis'; baslik: string; ifadeler: { metin: string; dogru: boolean; aciklama: string }[] }
  | { tur: 'sirala'; baslik: string; soru: string; adimlar: string[]; aciklama: string }
  | { tur: 'esle'; baslik: string; ciftler: { sol: string; sag: string }[] };
export interface EkKonu {
  id: string;
  baslik: string;
  ozet: string;
  gorsel: string;
  gorsel_alt: string;
  ek_gorseller?: { dosya: string; alt: string }[];
  bolumler: { baslik: string; ekran: string; ses: string[] }[];
  akilda: { kod: string; acilim: string; not: string };
  yap: string[];
  yapma: string[];
  spotlar: { metin: string; ses: string }[];
  etkinlikler: EkEtkinlik[];
  sorular: EkSoru[];
}
export interface EkBaslik { no: number; baslik: string; ozet: string; konular: EkKonu[] }
export interface EkPart { baslik: string; ekran: string; ses: string[] }
/** Hocanın verdiği çalışma soruları (hoca_sorulari.json): boşluk doldurma, doğru–yanlış, çoktan seçmeli setleri */
/** cozum: sesli çözüm metni (h-/hc- klipleri) · k: föyde yeniden numaralanan sorunun asıl kimliği "<set>-<no>" */
export type HocaSoru = { cozum?: string; k?: string; tur?: 'bosluk' | 'dy' | 'cs' } & (
  | { no: number; metin: string; cevap: string }
  | { no: number; metin: string; dogru: boolean }
  | { no: number; kok: string; secenekler: Record<string, string>; dogru: string; belirsiz?: boolean });
export interface HocaSet { id: string; ad: string; tur: 'bosluk' | 'dy' | 'cs'; aciklama: string; anahtarsiz?: boolean; sorular: HocaSoru[] }
export interface EkKlip { v: string; sure: number }
/** "PDF ile dinle" kipi (pdf_esle.json; scripts/ek_modul/pdf_esle.py yazar): ders klibinin kitapçıktaki yeri ve cümle zamanları.
 *  s: sayfa · k: bölüm kutusu · l: satır kutuları (0 başlık, 1… not maddeleri; sayfa oranı) · c: [cümlenin başladığı saniye, madde | -1] */
export interface EkPdfKlip { v: string; s: number; k: number[]; l: number[][][]; c: [number, number][] }
export interface EkPdfEsle { pdf: string; bayt: number; klip: Record<string, EkPdfKlip> }
export interface EkModul {
  ozet: EkModulOzet;
  basliklar: EkBaslik[];
  sinavOncesi: { giris?: string; partlar: EkPart[] } | null;
  genel: EkSoru[];
  klip: Record<string, EkKlip>;
  hoca: { kaynak: string; setler: HocaSet[] } | null;
  /** Çalışma föyü: hoca sorularının konuya göre düzeni (set id → soru no listesi) + konu bilgi özeti */
  foy: { konular: { id: string; bilgiler: string[]; sorular: Record<string, number[]> }[] } | null;
  pdfEsle: EkPdfEsle | null;
}

  /** Hoca soruları · "PDF ile" sesli çözüm (hoca_pdf_esle.json; scripts/ek_modul/pdf_esle_hoca.py): h-/hc- klibinin çözümlü
   *  kitapçıktaki soru bloğu, l cümle başına satırlar, c [cümlenin başladığı saniye, l sırası] */
  hocaPdf: EkPdfEsle | null;
export const EK_MODULLER = (dizinHam as { moduller: EkModulOzet[] }).moduller;
export const ekKurullar = () => [...new Set(EK_MODULLER.map((m) => m.kurul))].sort();

const DOSYA = import.meta.glob('../../../data/ek_moduller/*/*.json');
const bellek = new Map<string, Promise<EkModul | null>>();

export function ekModulYukle(id: string): Promise<EkModul | null> {
  const ozet = EK_MODULLER.find((m) => m.id === id);
  if (!ozet) return Promise.resolve(null);
  let p = bellek.get(id);
  if (!p) {
    const al = async <T,>(ad: string): Promise<T | null> => {
      const f = DOSYA[`../../../data/ek_moduller/${id}/${ad}.json`];
      if (!f) return null;
      const m = (await f()) as { default: T };
      return m.default;
    };
    p = (async () => {
      const adlar = Object.keys(DOSYA).map((k) => new RegExp(`/${id}/(b\\d+)\\.json$`).exec(k)?.[1]).filter(Boolean) as string[];
      const basliklar = (await Promise.all(adlar.map((a) => al<EkBaslik>(a)))).filter(Boolean) as EkBaslik[];
      basliklar.sort((a, b) => a.no - b.no);
      const [so, g, klip, hoca, foy, pdfEsle, hocaPdf] = await Promise.all([
        al<EkModul['sinavOncesi']>('sinav_oncesi'), al<{ sorular: EkSoru[] }>('genel_sorular'), al<Record<string, EkKlip>>('klip'),
        al<EkModul['hoca']>('hoca_sorulari'), al<EkModul['foy']>('foy'), al<EkPdfEsle>('pdf_esle'), al<EkPdfEsle>('hoca_pdf_esle'),
      ]);
      return { ozet, basliklar, sinavOncesi: so, genel: g?.sorular || [], klip: klip || {}, hoca, foy: hoca ? foy : null, pdfEsle, hocaPdf: hoca ? hocaPdf : null };
    })();
    bellek.set(id, p);
  }
  return p;
}

export const konulariAl = (m: EkModul) => m.basliklar.flatMap((b) => b.konular.map((k) => ({ ...k, baslikNo: b.no, baslikAd: b.baslik })));

/** Klip adresi; klip üretilmemişse null (düğme "ses hazırlanıyor" gösterir) */
export function klipUrl(m: EkModul, klip: string): string | null {
  const k = m.klip[klip];
  return k ? `/api/ek-modul/ses/${m.ozet.id}/${klip}.mp3?v=${k.v}` : null;
}
export const gorselUrl = (modul: string, dosya: string) => `/ek_moduller/${modul}/${dosya}`;
/** Klibin PDF eşlemesi; ses eşlemeden sonra yeniden üretildiyse (özet tutmuyor) cümle zamanları geçersizdir → null */
export function pdfKlip(m: EkModul, klip: string): EkPdfKlip | null {
  const e = m.pdfEsle?.klip[klip];
  return e && m.klip[klip]?.v === e.v ? e : null;
}

/* ——— soru setleri ——— */
export interface SetSoru extends EkSoru { anahtar: string; qKlip: string; cKlip: string; konuId: string }
export function hocaPdfKlip(m: EkModul, klip: string): EkPdfKlip | null {
  const e = m.hocaPdf?.klip[klip];
  return e && m.klip[klip]?.v === e.v ? e : null;
}


const setle = (sorular: EkSoru[], konuId: string, onek: string): SetSoru[] =>
  sorular.map((q) => ({ ...q, anahtar: `${onek}-${q.no}`, qKlip: `q-${onek}-${q.no}`, cKlip: `c-${onek}-${q.no}`, konuId: q.konu || konuId }));
export const konuSorulari = (m: EkModul, konuId: string): SetSoru[] => {
  const k = konulariAl(m).find((x) => x.id === konuId);
  return k ? setle(k.sorular, k.id, k.id) : [];
};
export const genelSorular = (m: EkModul): SetSoru[] => setle(m.genel, 'g', 'g');
export const tumSorular = (m: EkModul): SetSoru[] => [...konulariAl(m).flatMap((k) => setle(k.sorular, k.id, k.id)), ...genelSorular(m)];

/** Sınav denemesi: sınavdaki soru sayısı kadar; her başlıktan dengeli + genel sorulardan, her açılışta yeniden karılır */
export function denemeKur(m: EkModul, n = m.ozet.sinavSoru): SetSoru[] {
  const kar = <T,>(a: T[]) => { const b = [...a]; for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; };
  const secilen: SetSoru[] = [];
  const genel = kar(genelSorular(m));
  const yari = Math.min(genel.length, Math.floor(n / 2));
  secilen.push(...genel.slice(0, yari));
  const gruplar = m.basliklar.map((b) => kar(b.konular.flatMap((k) => setle(k.sorular, k.id, k.id))));
  let i = 0;
  while (secilen.length < n && gruplar.some((g) => g.length)) {
    const g = gruplar[i++ % gruplar.length];
    const q = g.pop();
    if (q) secilen.push(q);
  }
  return kar(secilen).slice(0, n);
}

/* ——— ilerleme (cihazda; profil eşitleme izin listesine eklenmedi) ——— */
const KEY = 'medsoru_ek_modul_v1';
interface Ilerleme { dinlenen: Record<string, 1>; soru: Record<string, 0 | 1>; deneme?: { puan: number; n: number; t: number }[] }
type Depo = Record<string, Ilerleme>;
let depo: Depo | null = null;
const abone = new Set<() => void>();
const oku = (): Depo => {
  if (depo) return depo;
  try { depo = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch { depo = {}; }
  return depo as Depo;
};
const yaz = (d: Depo) => {
  depo = { ...d };
  try { localStorage.setItem(KEY, JSON.stringify(depo)); } catch { /* kota */ }
  abone.forEach((f) => f());
};
const bos = (): Ilerleme => ({ dinlenen: {}, soru: {} });
export const useEkIlerleme = (modul: string): Ilerleme => {
  const d = useSyncExternalStore((f) => { abone.add(f); return () => abone.delete(f); }, oku, oku);
  return d[modul] || BOS;
};
const BOS = bos();
export function ekDinlendi(modul: string, anahtar: string) {
  const d = oku(), m = d[modul] || bos();
  if (m.dinlenen[anahtar]) return;
  yaz({ ...d, [modul]: { ...m, dinlenen: { ...m.dinlenen, [anahtar]: 1 } } });
}
export function ekSoruYaz(modul: string, anahtar: string, dogru: boolean) {
  const d = oku(), m = d[modul] || bos();
  yaz({ ...d, [modul]: { ...m, soru: { ...m.soru, [anahtar]: dogru ? 1 : 0 } } });
}
export function ekDenemeYaz(modul: string, puan: number, n: number) {
  const d = oku(), m = d[modul] || bos();
  yaz({ ...d, [modul]: { ...m, deneme: [...(m.deneme || []).slice(-9), { puan, n, t: Date.now() }] } });
}
