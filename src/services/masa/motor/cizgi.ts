/**
 * Çizgi Yarışı — saf kural motoru (2 oyuncu). Kurallar (docs/TAHTA_OYUNLARI.md §2):
 *   - Saha `uzunluk` satır × `genislik` sütun (32→3, 64/96→5, 128→7 sütun). 1. oyuncu 0. satırın ortasından r artarak,
 *     2. oyuncu son satırın ortasından r azalarak ilerler. Rakibin kale satırına (ilk satırına) ilk ulaşan kazanır.
 *   - Tur: zar at (1–6), sonra her adımı tek tek harca. Düz ilerleme önündeki hücre boşken; yandaki sütuna geçiş yalnız
 *     önü RAKİP ÇİZGİSİYLE kapalıyken, yandaki hücre boşsa ve yan hakkın varsa (1 adım). İlerleyemeyen kalanını yakar (bekle).
 *   - Kapışma: iki baş aynı sütunda yüz yüze geldiğinde ve en az biri kendi yarısını geçmişse çizgiler kapışır. Kapışmadaki
 *     turda sıradaki zar atar, iki zar birden atılır (sıradaki + rakip); büyük atan aradaki fark kadar ilerler, küçük atan o
 *     kadar geriler (çizgisi baştan kısalır, kale hücresi kalır). Eşitlikte bir şey olmaz. Mağlubun yalnız kale hücresi
 *     kaldıysa ve yine kaybederse galip kaleyi alır, el biter. Mağlup geri çekilirken çizgisi yan geçiş köşesini geçerse
 *     galibin önü açılır, kapışma kendiliğinden biter.
 *   - Yüz yüze gelme tam orta çizgide olursa (ikisi de kendi yarısında) kapışma yoktur; önü kapalı olan yana geçmelidir.
 * Durum düz JSON; `uygula` girdiyi değiştirmez.
 */
import type { CizgiAdim, CizgiGorunum, CizgiKare, ElSonuc, Hucre, Motor, Olay, Rng } from '../tipler';

export interface CizgiDurum {
  tur: 'cizgi';
  elNo: number;
  kare: CizgiKare;
  uzunluk: number;
  genislik: number;
  /** [aşağıdan yukarı (r artar), yukarıdan aşağı (r azalır)] */
  oyuncular: [string, string];
  cizgiler: Record<string, Hucre[]>;
  yanHak: Record<string, number>;
  kim: 0 | 1;
  zar: number | null;
  kalan: number;
  turNo: number;
  /** Bu turun birikmekte olan adımı */
  adim: CizgiAdim | null;
  gecmis: CizgiAdim[];
  sonuc: ElSonuc | null;
}

const KARELER: CizgiKare[] = [32, 64, 96, 128];
export const CIZGI_GENISLIK: Record<CizgiKare, number> = { 32: 3, 64: 5, 96: 5, 128: 7 };
export const CIZGI_YAN_HAK: Record<CizgiKare, number> = { 32: 2, 64: 3, 96: 4, 128: 5 };
const GECMIS = 4;

const zarAt = (rng: Rng) => 1 + Math.floor(rng() * 6);
const ayni = (a: Hucre, b: Hucre) => a.s === b.s && a.r === b.r;
const bas = (c: Hucre[]) => c[c.length - 1];
const yonu = (d: CizgiDurum, k: 0 | 1) => (k === 0 ? 1 : -1);
const rakipK = (k: 0 | 1): 0 | 1 => (k === 0 ? 1 : 0);
const dolu = (d: CizgiDurum, h: Hucre) => d.oyuncular.some((o) => d.cizgiler[o].some((x) => ayni(x, h)));
const icerde = (d: CizgiDurum, h: Hucre) => h.s >= 0 && h.s < d.genislik && h.r >= 0 && h.r < d.uzunluk;
/** Kendi kalesinden kaç satır ilerledi */
const ilerleme = (d: CizgiDurum, k: 0 | 1) => { const b = bas(d.cizgiler[d.oyuncular[k]]); return k === 0 ? b.r : d.uzunluk - 1 - b.r; };
const yariGecti = (d: CizgiDurum, k: 0 | 1) => ilerleme(d, k) >= d.uzunluk / 2;
const hedefSatir = (d: CizgiDurum, k: 0 | 1) => (k === 0 ? d.uzunluk - 1 : 0);

/** Başlar aynı sütunda yüz yüze mi */
export function yuzYuze(d: CizgiDurum): boolean {
  const a = bas(d.cizgiler[d.oyuncular[0]]), b = bas(d.cizgiler[d.oyuncular[1]]);
  return a.s === b.s && a.r + 1 === b.r;
}
export const kapismaMi = (d: CizgiDurum) => yuzYuze(d) && (yariGecti(d, 0) || yariGecti(d, 1));

/** Sıradakinin şu anki geçerli yönleri (zar atılmış, adım varken) */
export function yonler(d: CizgiDurum): ('duz' | 'sol' | 'sag')[] {
  if (d.sonuc || d.zar == null || d.kalan <= 0) return [];
  const k = d.kim, o = d.oyuncular[k], b = bas(d.cizgiler[o]), dy = yonu(d, k);
  const on = { s: b.s, r: b.r + dy };
  if (icerde(d, on) && !dolu(d, on)) return ['duz'];
  const rakipCizgi = d.cizgiler[d.oyuncular[rakipK(k)]];
  if (!icerde(d, on) || !rakipCizgi.some((x) => ayni(x, on)) || d.yanHak[o] <= 0) return [];
  const r: ('sol' | 'sag')[] = [];
  for (const [ad, ds] of [['sol', -1], ['sag', 1]] as const) {
    const y = { s: b.s + ds, r: b.r };
    if (icerde(d, y) && !dolu(d, y)) r.push(ad);
  }
  return r;
}

function sonuclandir(d: CizgiDurum, kazanan: string, aciklama: string): ElSonuc {
  return {
    neden: 'bitti', kazananlar: [kazanan],
    satirlar: d.oyuncular.map((id) => ({ id, puan: id === kazanan ? 1 : 0, kalan: 0, kazandi: id === kazanan, cezalar: [], aciklama })),
  };
}

/** Turu kapat: adımı geçmişe yaz, sıra karşıya */
function turBitir(d: CizgiDurum, olaylar: Olay[]) {
  if (d.adim) { d.gecmis = [...d.gecmis, d.adim].slice(-GECMIS); d.adim = null; }
  d.zar = null; d.kalan = 0;
  if (d.sonuc) { olaylar.push({ t: 'elBitti' }); return; }
  d.kim = rakipK(d.kim); d.turNo += 1;
  olaylar.push({ t: 'sira', o: d.oyuncular[d.kim] });
}

const kopya = (d: CizgiDurum): CizgiDurum => ({
  ...d, cizgiler: Object.fromEntries(Object.entries(d.cizgiler).map(([k, v]) => [k, v.slice()])), yanHak: { ...d.yanHak },
  adim: d.adim ? { ...d.adim, eklenen: d.adim.eklenen.slice(), silinen: d.adim.silinen.slice() } : null,
});

export const cizgiMotor: Motor = {
  tur: 'cizgi', min: 2, max: 2,

  elBaslat({ oyuncular, elNo, baslayan, ayar }) {
    const kare = KARELER.includes(ayar?.cizgiKare as CizgiKare) ? (ayar!.cizgiKare as CizgiKare) : 64;
    const genislik = CIZGI_GENISLIK[kare], orta = (genislik - 1) / 2;
    const ids: [string, string] = [oyuncular[0].id, oyuncular[1].id];
    const d: CizgiDurum = {
      tur: 'cizgi', elNo, kare, uzunluk: kare, genislik, oyuncular: ids,
      cizgiler: { [ids[0]]: [{ s: orta, r: 0 }], [ids[1]]: [{ s: orta, r: kare - 1 }] },
      yanHak: { [ids[0]]: CIZGI_YAN_HAK[kare], [ids[1]]: CIZGI_YAN_HAK[kare] },
      kim: (baslayan % 2) as 0 | 1, zar: null, kalan: 0, turNo: 1, adim: null, gecmis: [], sonuc: null,
    };
    return d;
  },

  uygula(durum, oyuncu, hamle, rng) {
    const d0 = durum as CizgiDurum, h = hamle as { t?: string; yon?: string };
    if (d0.sonuc) return { hata: 'El bitti.' };
    if (d0.oyuncular[d0.kim] !== oyuncu) return { hata: 'Sıra sende değil.' };
    const d = kopya(d0), k = d.kim, o = oyuncu, rk = rakipK(k), ro = d.oyuncular[rk];
    const olaylar: Olay[] = [];

    if (h?.t === 'zar') {
      if (d.zar != null) return { hata: 'Zarı zaten attın.' };
      const zar = zarAt(rng);
      d.adim = { tur: d.turNo, o, zar, fark: 0, eklenen: [], silinen: [] };
      if (kapismaMi(d)) {
        const rakipZar = zarAt(rng), fark = Math.abs(zar - rakipZar);
        const kazananK: 0 | 1 | null = zar > rakipZar ? k : zar < rakipZar ? rk : null;
        d.adim.kapisma = { rakipZar, kazanan: kazananK == null ? null : d.oyuncular[kazananK] };
        olaylar.push({ t: 'kapisma', o, zar, rakipZar, kazanan: d.adim.kapisma.kazanan, fark });
        if (kazananK != null && fark > 0) {
          const g = d.oyuncular[kazananK], m = d.oyuncular[rakipK(kazananK)];
          const mc = d.cizgiler[m], gc = d.cizgiler[g];
          // Mağlup geriler (kale hücresi kalır); kaleden fazlası istenirse galip kaleyi alır
          let geri = 0;
          while (geri < fark && mc.length > 1) { d.adim.silinen.push(mc.pop()!); geri++; }
          const kaleAlindi = geri < fark && mc.length === 1;
          // Galip aynı kadar ilerler (önü boş olduğu sürece)
          let ileri = 0;
          const dy = yonu(d, kazananK);
          while (ileri < fark) {
            const b = bas(gc), on = { s: b.s, r: b.r + dy };
            if (!icerde(d, on) || dolu(d, on)) break;
            gc.push(on); d.adim.eklenen.push(on); ileri++;
            if (on.r === hedefSatir(d, kazananK)) break;
          }
          d.adim.fark = kazananK === k ? ileri : -geri;
          olaylar.push({ t: 'geriledi', o: m, adet: geri }, { t: 'ilerledi', o: g, adet: ileri });
          if (kaleAlindi || bas(gc).r === hedefSatir(d, kazananK)) d.sonuc = sonuclandir(d, g, kaleAlindi ? 'Kapışmada kale alındı' : 'Rakip kaleye ulaştı');
        }
        turBitir(d, olaylar);
        return { durum: d, olaylar };
      }
      d.zar = zar; d.kalan = zar;
      olaylar.push({ t: 'zar', o, zar });
      if (!yonler(d).length) { olaylar.push({ t: 'bekledi', o, adet: d.kalan }); turBitir(d, olaylar); }
      return { durum: d, olaylar };
    }

    if (d.zar == null) return { hata: 'Önce zar at.' };
    // Koş: düz yol açık oldukça adımları tek hamlede harca; yan seçimi gerekince ya da tur bitince durur
    if (h?.t === 'kos') {
      if (!yonler(d).includes('duz')) return { hata: 'Önün kapalı.' };
      let cur: CizgiDurum = d0;
      const tum: Olay[] = [];
      while (!cur.sonuc && cur.oyuncular[cur.kim] === oyuncu && cur.zar != null && yonler(cur).includes('duz')) {
        const r = cizgiMotor.uygula(cur, oyuncu, { t: 'ilerle', yon: 'duz' }, rng);
        if ('hata' in r) break;
        cur = r.durum as CizgiDurum; tum.push(...r.olaylar);
      }
      return { durum: cur, olaylar: tum };
    }
    if (h?.t === 'bekle') { olaylar.push({ t: 'bekledi', o, adet: d.kalan }); turBitir(d, olaylar); return { durum: d, olaylar }; }
    if (h?.t !== 'ilerle') return { hata: 'Geçersiz hamle.' };
    const yon = h.yon as 'duz' | 'sol' | 'sag';
    if (!yonler(d).includes(yon)) return { hata: yon === 'duz' ? 'Önün kapalı.' : 'Yana yalnız önün rakip çizgisiyle kapalıyken, yan hakkın varsa ve yan hücre boşsa geçebilirsin.' };
    const b = bas(d.cizgiler[o]);
    const yeni = yon === 'duz' ? { s: b.s, r: b.r + yonu(d, k) } : { s: b.s + (yon === 'sol' ? -1 : 1), r: b.r };
    d.cizgiler[o].push(yeni);
    d.adim!.eklenen.push(yeni);
    if (yon === 'duz') d.adim!.fark += 1; else d.yanHak[o] -= 1;
    d.kalan -= 1;
    olaylar.push({ t: 'ilerledi', o, h: yeni, yon });
    if (yeni.r === hedefSatir(d, k)) { d.sonuc = sonuclandir(d, o, 'Rakip kaleye ulaştı'); turBitir(d, olaylar); return { durum: d, olaylar }; }
    if (kapismaMi(d)) { olaylar.push({ t: 'karsilasti', o, rakip: ro }); turBitir(d, olaylar); return { durum: d, olaylar }; }
    if (d.kalan <= 0 || !yonler(d).length) { if (d.kalan > 0) olaylar.push({ t: 'bekledi', o, adet: d.kalan }); turBitir(d, olaylar); }
    return { durum: d, olaylar };
  },

  gorunum(durum) {
    const d = durum as CizgiDurum;
    const g: CizgiGorunum = {
      tur: 'cizgi', elNo: d.elNo, kare: d.kare, uzunluk: d.uzunluk, genislik: d.genislik, sira: d.oyuncular[d.kim],
      cizgiler: d.cizgiler, yanHak: d.yanHak, zar: d.zar, kalan: d.kalan, kapisma: kapismaMi(d),
      gecmis: d.adim ? [...d.gecmis, d.adim].slice(-GECMIS) : d.gecmis, yonler: yonler(d), bitti: !!d.sonuc,
    };
    return g;
  },

  botHamle(durum, bot) {
    const d = durum as CizgiDurum;
    if (d.sonuc || d.oyuncular[d.kim] !== bot) return null;
    if (d.zar == null) return { t: 'zar' };
    const y = yonler(d);
    if (!y.length) return { t: 'bekle' };
    if (y.includes('duz')) return { t: 'kos' };
    // Yan: orta sütuna yakın olanı seç (kenara sıkışmasın)
    const b = bas(d.cizgiler[bot]), orta = (d.genislik - 1) / 2;
    const sec = y.slice().sort((p, q) => Math.abs(b.s + (p === 'sol' ? -1 : 1) - orta) - Math.abs(b.s + (q === 'sol' ? -1 : 1) - orta))[0];
    return { t: 'ilerle', yon: sec };
  },

  sonuc(durum) { return (durum as CizgiDurum).sonuc; },
};
