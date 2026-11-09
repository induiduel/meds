/**
 * Go — saf kural motoru (2 oyuncu, 9/13/19). Kurallar (docs/TAHTA_OYUNLARI.md §1):
 *   - Siyah başlar; sırayla boş kesişime taş konur. Özgürlüğü kalmayan rakip grubu tahtadan alınır (esir).
 *   - İntihar yasak: konan taşın grubu, rakip taş almadan özgürlüksüz kalıyorsa hamle geçersiz.
 *   - Ko (basit): tek taş alıp tek taşla tek özgürlükte kalan hamleden hemen sonra rakip aynı noktaya geri alamaz.
 *   - Konumsal süperko: bu elde daha önce görülmüş bir tahta dizilişini yeniden doğuran hamle yasak (geçmiş özetleri `gecmis`).
 *   - Handikap (2–9): siyah taşlar yıldız noktalarına konur, beyaz başlar; handikaplı elde komi 0,5 (1 = taşsız, komi 0,5).
 *   - Süre (isteğe bağlı): ana süre + Japon byo-yomi. Saat hamle zamanıyla (`z`, sunucu basar) tutulur; süresi biten kaybeder.
 *   - Pas serbest; art arda iki pas → sayım aşaması: oyuncular ölü grupları işaretler, ikisi onaylayınca el biter.
 *     Anlaşamayan "devam" der, oyun sürer. Teslim her an.
 *   - Puan alan usulü (Çin): diri taş + yalnız kendi taşlarınca çevrili boş nokta (ölü taşların yeri rakibe) + beyaza komi.
 * Durum düz JSON; `uygula` girdiyi değiştirmez.
 */
import type { ElSonuc, GoBoyut, GoGorunum, GoTas, Motor, Olay, Rng } from '../tipler';
import { GO_SURELER } from '../tipler';

export interface GoDurum {
  tur: 'go';
  elNo: number;
  boyut: GoBoyut;
  /** [siyah, beyaz] oyuncu kimlikleri */
  oyuncular: [string, string];
  tahta: ('' | GoTas)[];
  sira: GoTas;
  esir: Record<GoTas, number>;
  komi: number;
  ko: number | null;
  son: { renk: GoTas; i: number } | null;
  paslar: number;
  asama: 'oyun' | 'sayim';
  olu: number[];
  onay: string[];
  hamleSayisi: number;
  sonuc: ElSonuc | null;
  /** Konumsal süperko: bu elde görülmüş tahta özetleri (ilk diziliş dahil) */
  gecmis: string[];
  handikap: number;
  /** Süre sınırı: kalan ana süre (ms) ve byo-yomi hakkı renge göre; sonZ = saatin son başladığı an */
  saat: { ana: Record<GoTas, number>; periyot: Record<GoTas, number>; byo: number; sonZ: number } | null;
}

const karsi = (r: GoTas): GoTas => (r === 'S' ? 'B' : 'S');
const BOYUTLAR: GoBoyut[] = [9, 13, 19];

export function komsular(i: number, n: number): number[] {
  const x = i % n, y = (i - x) / n, k: number[] = [];
  if (x > 0) k.push(i - 1);
  if (x < n - 1) k.push(i + 1);
  if (y > 0) k.push(i - n);
  if (y < n - 1) k.push(i + n);
  return k;
}

/** Grubu ve özgürlüklerini bul */
export function grup(tahta: GoDurum['tahta'], i: number, n: number): { taslar: number[]; ozgurluk: Set<number> } {
  const renk = tahta[i], taslar = [i], gor = new Set([i]), ozgurluk = new Set<number>();
  for (let k = 0; k < taslar.length; k++) {
    for (const j of komsular(taslar[k], n)) {
      if (tahta[j] === '') ozgurluk.add(j);
      else if (tahta[j] === renk && !gor.has(j)) { gor.add(j); taslar.push(j); }
    }
  }
  return { taslar, ozgurluk };
}

/** Tahta özeti (süperko): iki 32 bitlik karma (FNV-1a + djb2) — çakışma olasılığı ihmal edilir */
export function ozet(t: GoDurum['tahta']): string {
  let a = 0x811c9dc5, b = 5381;
  for (let i = 0; i < t.length; i++) {
    const c = t[i] === 'S' ? 1 : t[i] === 'B' ? 2 : 3;
    a = Math.imul(a ^ c, 0x01000193) >>> 0;
    b = ((Math.imul(b, 33) >>> 0) ^ (c + i)) >>> 0;
  }
  return a.toString(36) + '.' + b.toString(36);
}

/** Handikap yerleşimi (standart sıra): köşeler, sonra orta / yan yıldızlar */
export function handikapNoktalari(n: GoBoyut, h: number): number[] {
  if (h < 2) return [];
  const k = n === 9 ? 2 : 3, u = n - 1 - k, m = (n - 1) / 2, P = (x: number, y: number) => y * n + x;
  const kose = [P(u, k), P(k, u), P(u, u), P(k, k)];
  const yan = [P(k, m), P(u, m)], ust = [P(m, k), P(m, u)], orta = P(m, m);
  const tablo: Record<number, number[]> = {
    2: kose.slice(0, 2), 3: kose.slice(0, 3), 4: kose, 5: [...kose, orta], 6: [...kose, ...yan],
    7: [...kose, ...yan, orta], 8: [...kose, ...yan, ...ust], 9: [...kose, ...yan, ...ust, orta],
  };
  return tablo[Math.min(9, h)];
}

export function yildizlar(n: GoBoyut): number[] {
  const a = n === 9 ? [2, 4, 6] : n === 13 ? [3, 6, 9] : [3, 9, 15];
  const s = a.flatMap((y) => a.map((x) => y * n + x));
  return n === 9 ? s.filter((i) => [20, 24, 40, 56, 60].includes(i)) : s;
}

/** Taş koymayı dene: geçersizse hata, geçerliyse yeni tahta + alınanlar + yeni ko */
export function koy(d: GoDurum, i: number): { hata: string } | { tahta: GoDurum['tahta']; alinan: number[]; ko: number | null } {
  const n = d.boyut;
  if (!Number.isInteger(i) || i < 0 || i >= n * n) return { hata: 'Tahta dışı.' };
  if (d.tahta[i] !== '') return { hata: 'Bu nokta dolu.' };
  if (d.ko === i) return { hata: 'Ko: bu taşı hemen geri alamazsın, önce başka yere oyna.' };
  const t = d.tahta.slice(), renk = d.sira, rakip = karsi(renk);
  t[i] = renk;
  const alinan: number[] = [];
  for (const j of komsular(i, n)) {
    if (t[j] !== rakip) continue;
    const g = grup(t, j, n);
    if (g.ozgurluk.size === 0) for (const k of g.taslar) { t[k] = ''; alinan.push(k); }
  }
  const benim = grup(t, i, n);
  if (benim.ozgurluk.size === 0) return { hata: 'İntihar yasak: bu taş hiç özgürlüğü olmadan kalır.' };
  if (d.gecmis?.includes(ozet(t))) return { hata: 'Süperko: bu hamle tahtayı daha önceki bir dizilişe döndürür.' };
  const ko = alinan.length === 1 && benim.taslar.length === 1 && benim.ozgurluk.size === 1 ? alinan[0] : null;
  return { tahta: t, alinan, ko };
}

export function yasallar(d: GoDurum): number[] {
  if (d.asama !== 'oyun' || d.sonuc) return [];
  const r: number[] = [];
  for (let i = 0; i < d.tahta.length; i++) if (d.tahta[i] === '' && !('hata' in koy(d, i))) r.push(i);
  return r;
}

/** Alan sayımı: ölü taşlar kaldırılmış sayılır */
export function say(d: GoDurum): { alan: { S: number[]; B: number[] }; puan: Record<GoTas, number> } {
  const n = d.boyut, olu = new Set(d.olu);
  const t = d.tahta.map((v, i) => (olu.has(i) ? '' : v));
  const alan = { S: [] as number[], B: [] as number[] };
  const gor = new Set<number>();
  for (let i = 0; i < t.length; i++) {
    if (t[i] !== '' || gor.has(i)) continue;
    const bolge = [i], sinir = new Set<GoTas>();
    gor.add(i);
    for (let k = 0; k < bolge.length; k++) {
      for (const j of komsular(bolge[k], n)) {
        if (t[j] === '') { if (!gor.has(j)) { gor.add(j); bolge.push(j); } } else sinir.add(t[j] as GoTas);
      }
    }
    if (sinir.size === 1) alan[[...sinir][0]].push(...bolge);
  }
  const tas = (r: GoTas) => t.filter((v) => v === r).length;
  return { alan, puan: { S: tas('S') + alan.S.length, B: tas('B') + alan.B.length + d.komi } };
}

const renkOf = (d: GoDurum, o: string): GoTas | null => (d.oyuncular[0] === o ? 'S' : d.oyuncular[1] === o ? 'B' : null);

function bitir(d: GoDurum, kazananRenk: GoTas, aciklama: string): ElSonuc {
  const kazanan = d.oyuncular[kazananRenk === 'S' ? 0 : 1];
  return {
    neden: 'bitti', kazananlar: [kazanan],
    satirlar: d.oyuncular.map((id) => ({ id, puan: id === kazanan ? 1 : 0, kalan: 0, kazandi: id === kazanan, cezalar: [], aciklama })),
  };
}

/** Hamleyi yapan rengin saatini z anına göre düşür; süre bittiyse null */
function saatDus(s: NonNullable<GoDurum['saat']>, renk: GoTas, z: number): NonNullable<GoDurum['saat']> | null {
  const gecen = Math.max(0, z - s.sonZ);
  const ana = { ...s.ana }, periyot = { ...s.periyot };
  if (gecen <= ana[renk]) ana[renk] -= gecen;
  else {
    const asim = gecen - ana[renk];
    ana[renk] = 0;
    if (!s.byo || asim >= periyot[renk] * s.byo) return null;
    periyot[renk] -= Math.floor(asim / s.byo); // bir byo-yomi aralığını aşan her hamle bir hak yer
  }
  return { ...s, ana, periyot, sonZ: z };
}

/** Sıradaki oyuncunun süresinin biteceği an (ms); süre yoksa null */
export function goSureSonu(d: GoDurum): number | null {
  if (!d.saat || d.sonuc || d.asama !== 'oyun') return null;
  return d.saat.sonZ + d.saat.ana[d.sira] + d.saat.periyot[d.sira] * d.saat.byo;
}

const zOf = (h: { z?: unknown }) => (typeof h?.z === 'number' && Number.isFinite(h.z) ? h.z : Date.now());

const RENK_AD: Record<GoTas, string> = { S: 'Siyah', B: 'Beyaz' };

export const goMotor: Motor = {
  tur: 'go', min: 2, max: 2,

  elBaslat({ oyuncular, elNo, baslayan, ayar }) {
    const boyut = BOYUTLAR.includes(ayar?.goBoyut as GoBoyut) ? (ayar!.goBoyut as GoBoyut) : 9;
    const handikap = Number.isInteger(ayar?.goHandikap) ? Math.max(0, Math.min(9, ayar!.goHandikap as number)) : 0;
    const komi = handikap > 0 ? 0.5
      : typeof ayar?.komi === 'number' && ayar.komi >= 0 && ayar.komi <= 15 ? Math.round(ayar.komi * 2) / 2 : 6.5;
    const s = oyuncular[baslayan % 2].id, b = oyuncular[(baslayan + 1) % 2].id;
    const tahta: GoDurum['tahta'] = Array(boyut * boyut).fill('');
    const hn = handikapNoktalari(boyut, handikap);
    for (const i of hn) tahta[i] = 'S';
    const sure = GO_SURELER.find((x) => x.id === ayar?.goSure && x.ana > 0);
    const d: GoDurum = {
      tur: 'go', elNo, boyut, oyuncular: [s, b], tahta, sira: hn.length ? 'B' : 'S',
      esir: { S: 0, B: 0 }, komi, ko: null, son: null, paslar: 0, asama: 'oyun', olu: [], onay: [], hamleSayisi: 0, sonuc: null,
      gecmis: [ozet(tahta)], handikap,
      saat: sure ? { ana: { S: sure.ana * 1000, B: sure.ana * 1000 }, periyot: { S: sure.periyot, B: sure.periyot }, byo: sure.byo * 1000, sonZ: Date.now() } : null,
    };
    return d;
  },

  uygula(durum, oyuncu, hamle) {
    const d = durum as GoDurum, h = hamle as { t?: string; i?: number; z?: number };
    if (d.sonuc) return { hata: 'El bitti.' };
    const renk = renkOf(d, oyuncu);
    if (!renk) return { hata: 'Bu masada oyuncu değilsin.' };
    const olaylar: Olay[] = [];
    if (h?.t === 'teslim') {
      const y = { ...d, sonuc: bitir(d, karsi(renk), `${RENK_AD[renk]} teslim oldu`) };
      return { durum: y, olaylar: [{ t: 'teslim', o: oyuncu }, { t: 'elBitti' }] };
    }
    if (h?.t === 'sureBitti') {
      // Sunucu zamanlayıcısı ya da herhangi bir istemci yollayabilir; motor saati kendisi doğrular
      const sonu = goSureSonu(d);
      if (sonu == null || zOf(h) < sonu) return { hata: 'Süre henüz bitmedi.' };
      const kaybeden = d.sira;
      const y = { ...d, sonuc: bitir(d, karsi(kaybeden), `${RENK_AD[kaybeden]} süreyi aştı`) };
      return { durum: y, olaylar: [{ t: 'sureBitti', o: d.oyuncular[kaybeden === 'S' ? 0 : 1] }, { t: 'elBitti' }] };
    }
    if (d.asama === 'sayim') {
      if (h?.t === 'olu') {
        const i = Number(h.i);
        if (!Number.isInteger(i) || i < 0 || i >= d.tahta.length || d.tahta[i] === '') return { hata: 'Bir taşa dokun.' };
        const g = grup(d.tahta, i, d.boyut).taslar;
        const olu = new Set(d.olu), oluMu = olu.has(i);
        for (const k of g) { if (oluMu) olu.delete(k); else olu.add(k); }
        return { durum: { ...d, olu: [...olu], onay: [] }, olaylar: [{ t: 'olu', o: oyuncu, taslar: g, olu: !oluMu }] };
      }
      if (h?.t === 'onayla') {
        if (d.onay.includes(oyuncu)) return { hata: 'Zaten onayladın.' };
        const y: GoDurum = { ...d, onay: [...d.onay, oyuncu] };
        olaylar.push({ t: 'onayladi', o: oyuncu });
        if (y.onay.length === 2) {
          const { puan } = say(y);
          y.sonuc = bitir(y, puan.S > puan.B ? 'S' : 'B', `Siyah ${puan.S} – Beyaz ${puan.B}`);
          olaylar.push({ t: 'elBitti' });
        }
        return { durum: y, olaylar };
      }
      if (h?.t === 'devam') {
        // Anlaşmazlık: oyun sürer, sıra devam diyenin rakibinde (pas yapan sıradaydı; adil olsun diye karşıya geçer)
        const saat = d.saat ? { ...d.saat, sonZ: zOf(h) } : null; // sayımda saat durur
        return { durum: { ...d, asama: 'oyun', olu: [], onay: [], paslar: 0, sira: karsi(renk), saat }, olaylar: [{ t: 'devam', o: oyuncu }] };
      }
      return { hata: 'Sayım sürüyor: ölü taşları işaretle ya da onayla.' };
    }
    if (renk !== d.sira) return { hata: 'Sıra sende değil.' };
    let saat = d.saat;
    if (saat && (h?.t === 'pas' || h?.t === 'koy')) {
      const yeni = saatDus(saat, renk, zOf(h));
      if (!yeni) return { hata: 'Süren bitti.' };
      saat = yeni;
    }
    if (h?.t === 'pas') {
      const y: GoDurum = { ...d, saat, paslar: d.paslar + 1, sira: karsi(renk), ko: null, son: { renk, i: -1 }, hamleSayisi: d.hamleSayisi + 1 };
      olaylar.push({ t: 'pas', o: oyuncu });
      if (y.paslar >= 2) { y.asama = 'sayim'; y.olu = []; y.onay = []; olaylar.push({ t: 'sayim' }); }
      else olaylar.push({ t: 'sira', o: d.oyuncular[y.sira === 'S' ? 0 : 1] });
      return { durum: y, olaylar };
    }
    if (h?.t !== 'koy') return { hata: 'Geçersiz hamle.' };
    const r = koy(d, Number(h.i));
    if ('hata' in r) return r;
    const y: GoDurum = {
      ...d, saat, tahta: r.tahta, ko: r.ko, gecmis: [...(d.gecmis || []), ozet(r.tahta)], sira: karsi(renk), paslar: 0, son: { renk, i: Number(h.i) }, hamleSayisi: d.hamleSayisi + 1,
      esir: { ...d.esir, [renk]: d.esir[renk] + r.alinan.length },
    };
    olaylar.push({ t: 'koydu', o: oyuncu, i: h.i, renk });
    if (r.alinan.length) olaylar.push({ t: 'aldi', o: oyuncu, taslar: r.alinan });
    olaylar.push({ t: 'sira', o: d.oyuncular[y.sira === 'S' ? 0 : 1] });
    return { durum: y, olaylar };
  },

  gorunum(durum) {
    const d = durum as GoDurum;
    const sayim = d.asama === 'sayim' || !!d.sonuc ? say(d) : null;
    const g: GoGorunum = {
      tur: 'go', elNo: d.elNo, boyut: d.boyut, tahta: d.tahta, sira: d.oyuncular[d.sira === 'S' ? 0 : 1],
      renkler: { [d.oyuncular[0]]: 'S', [d.oyuncular[1]]: 'B' }, esir: d.esir, komi: d.komi, son: d.son, ko: d.ko,
      yasal: yasallar(d), yildiz: yildizlar(d.boyut), asama: d.asama, olu: d.olu, onay: d.onay,
      alan: sayim?.alan, puan: sayim?.puan, hamleSayisi: d.hamleSayisi, bitti: !!d.sonuc, handikap: d.handikap || 0,
      saat: d.saat ? { ana: d.saat.ana, periyot: d.saat.periyot, byo: d.saat.byo, gecen: d.asama === 'oyun' && !d.sonuc ? Math.max(0, Date.now() - d.saat.sonZ) : 0 } : null,
    };
    return g;
  },

  botHamle(durum, bot, rng) {
    const d = durum as GoDurum;
    if (d.sonuc) return null;
    const renk = renkOf(d, bot);
    if (!renk) return null;
    if (d.asama === 'sayim') {
      // Kendi diri grubu ölü işaretlendiyse önce işareti geri al; sonra onayla
      const yanlis = d.olu.find((i) => d.tahta[i] === renk && diriMi(d, i));
      if (yanlis !== undefined) return { t: 'olu', i: yanlis };
      return d.onay.includes(bot) ? null : { t: 'onayla' };
    }
    if (renk !== d.sira) return null;
    return { ...goBotSec(d, rng) };
  },

  sonuc(durum) { return (durum as GoDurum).sonuc; },

  sureSonu(durum) { return goSureSonu(durum as GoDurum); },

  saatKaydir(durum, ms) {
    const d = durum as GoDurum;
    return d.saat ? { ...d, saat: { ...d.saat, sonZ: d.saat.sonZ + ms } } : d;
  },
};

/** Grup açıkça diri mi: ≥2 göz (yalnız bu grubun taşlarıyla çevrili boş bölge) ya da ≥5 özgürlük */
export function diriMi(d: GoDurum, i: number): boolean {
  const n = d.boyut, renk = d.tahta[i];
  if (!renk) return false;
  const g = grup(d.tahta, i, n);
  if (g.ozgurluk.size >= 5) return true;
  const benim = new Set(g.taslar), gor = new Set<number>();
  let goz = 0;
  for (const o of g.ozgurluk) {
    if (gor.has(o)) continue;
    const bolge = [o];
    gor.add(o);
    let kapali = true;
    for (let k = 0; k < bolge.length && bolge.length <= 12; k++) {
      for (const j of komsular(bolge[k], n)) {
        if (d.tahta[j] === '') { if (!gor.has(j)) { gor.add(j); bolge.push(j); } }
        else if (!benim.has(j)) kapali = false;
      }
    }
    if (kapali && bolge.length <= 12) goz++;
  }
  return goz >= 2;
}

/** Basit bot: alır, atarideki grubunu kurtarır, kendi gözünü doldurmaz, kendini atariye sokmaz; iyi hamle yoksa pas */
export function goBotSec(d: GoDurum, rng: Rng): { t: 'koy'; i: number } | { t: 'pas' } {
  const n = d.boyut, renk = d.sira, rakip = karsi(renk);
  let en: { i: number; p: number } | null = null;
  for (const i of yasallar(d)) {
    const k = komsular(i, n);
    if (k.every((j) => d.tahta[j] === renk)) continue; // kendi gözü
    const r = koy(d, i);
    if ('hata' in r) continue;
    let p = r.alinan.length * 10 + rng();
    const yeni = grup(r.tahta, i, n);
    if (yeni.ozgurluk.size === 1) p -= 8;
    for (const j of k) {
      if (d.tahta[j] === renk && grup(d.tahta, j, n).ozgurluk.size === 1 && yeni.ozgurluk.size > 1) p += 8;
      if (d.tahta[j] === rakip && grup(r.tahta, j, n).ozgurluk.size === 1) p += 3;
    }
    const x = i % n, y = (i - x) / n, kenar = Math.min(x, y, n - 1 - x, n - 1 - y);
    if (d.hamleSayisi < n) p += kenar === 2 || (n > 9 && kenar === 3) ? 2 : kenar === 0 ? -2 : 0;
    if (d.son && d.son.i >= 0 && Math.abs((d.son.i % n) - x) + Math.abs(Math.floor(d.son.i / n) - y) <= 2) p += 1;
    if (!en || p > en.p) en = { i, p };
  }
  // Oyun olgunlaştıysa ve anlamlı hamle yoksa pas (rakip pas dediyse daha kolay pas)
  const esik = d.paslar ? 2 : d.hamleSayisi > n * n * 0.6 ? 1.5 : -100;
  return en && en.p > esik ? { t: 'koy', i: en.i } : { t: 'pas' };
}
