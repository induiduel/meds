/**
 * Tek kişilik oyunların (Blitz, Hayatta kal, Görselli) internetsiz soru kaynağı (H599).
 * Çevrimiçiyken sorular sunucudan gelir (/api/oyun/sorular; src/services/quiz/oyunSoruKaynagi.ts). Sunucuya ulaşılamazsa aynı
 * kural (kök ≤ 220 karakter, doğru şık metni var) cihazdaki soru çözücü setlerine uygulanır: çözücü paketi indirilmiş derslerin
 * soruları oyuna girer. Yeni soru üretilmez. Canlı oda (çok oyunculu) internet ister; bu dosya yalnız tek kişilik kipler içindir.
 */
import { BRANSLAR, type Brans } from '../components/spots/brans';
import { cozucuDersYukle, cozucuDizinYukle, cozucuVar, type CDers } from '../components/spots/cozucu/cozucuVeri';
import { durumAl } from './cevrimdisi/paketMotoru';

export interface YerelKaynak { brans: string; ad: string; kurul: number; ders: { kod: string; baslik: string; n: number }[]; n: number; gorselN?: number }
export interface YerelSoru { id: string; prompt: string; options: Record<string, string>; correct: string; aciklama: string; baslik: string; gorsel?: string }

const KOK_SINIR = 220;
const gorselli = (s: any) => typeof s?.gorsel === 'string' && /^(\/|https:\/\/)/.test(s.gorsel);
const uygun = (s: any) => !!s?.soru && s.soru.length <= KOK_SINIR && !!s.secenekler?.[s.dogru];
const cihazda = (brans: string, kod: string) => { const k = durumAl().kayitlar[`cozucu:${brans}:${kod}`]; return !!k && !k.yarim; };

/** Branşın cihazdan yüklenebilen dersleri: önce paketi inmiş olanlar; hiçbiri yoksa (parçalar tarayıcı önbelleğinde olabilir) hepsi denenir */
async function dersler(brans: Brans, ders?: string): Promise<CDers[]> {
  const dizin = await cozucuDizinYukle(brans).catch(() => null);
  let kodlar = (dizin?.dersler || []).map((d) => String(d.kod)).filter((k) => !ders || k === ders);
  const inmis = kodlar.filter((k) => cihazda(brans, k));
  if (inmis.length) kodlar = inmis;
  const r = await Promise.allSettled(kodlar.map((k) => cozucuDersYukle(k, brans)));
  return r.flatMap((x) => (x.status === 'fulfilled' && x.value?.sorular ? [x.value] : []));
}

/** Kaynak listesi: dizinler uygulama paketindedir; soru sayıları dizindeki toplamdan (yaklaşık) */
export async function yerelOyunKaynaklari(): Promise<YerelKaynak[]> {
  const out: YerelKaynak[] = [];
  for (const b of BRANSLAR) {
    if (!cozucuVar(b.id)) continue;
    const dizin = await cozucuDizinYukle(b.id).catch(() => null);
    const ds = (dizin?.dersler || []).filter((d) => cihazda(b.id, String(d.kod)));
    if (!ds.length) continue;
    const k = /^k(\d)/.exec(b.id);
    out.push({ brans: b.id, ad: b.ad, kurul: k ? Number(k[1]) : 1, ders: ds.map((d) => ({ kod: String(d.kod), baslik: d.baslik, n: d.soru })), n: ds.reduce((a, d) => a + (d.soru || 0), 0) });
  }
  return out.sort((a, b) => b.kurul - a.kurul || b.n - a.n);
}

export async function yerelOyunSorulari(brans: string, ders: string | undefined, n: number, yalnizGorselli = false): Promise<YerelSoru[]> {
  const ds = await dersler(brans as Brans, ders);
  const havuz = ds.flatMap((d) => (d.sorular || []).filter((s) => uygun(s) && (!yalnizGorselli || gorselli(s))).map((s) => ({ d, s })));
  for (let i = havuz.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [havuz[i], havuz[j]] = [havuz[j], havuz[i]]; }
  return havuz.slice(0, Math.max(3, Math.min(20, n))).map(({ d, s }) => ({
    id: `oy_${brans}_${d.kod}_${s.no}`, prompt: s.soru, options: s.secenekler, correct: s.dogru,
    aciklama: s.siklar?.[s.dogru] || '', baslik: d.baslik, ...(gorselli(s) ? { gorsel: (s as any).gorsel } : {}),
  }));
}
