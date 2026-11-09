/**
 * Taş Domino — saf kural motoru (2–4 oyuncu, 104 okey taşı, joker yok). Durum düz JSON, `uygula` girdiyi değiştirmez.
 *
 * Kurallar (kurallar/DominoKurallar.tsx ile birebir):
 *   - Herkese 7 taş; desteden 1 taş açılır, zincirin başlangıcıdır. Zincirin iki ucu var: 'bas' (ilk taş) ve 'son' (son taş).
 *   - Uyma: uçtaki taşla rengi ya da sayısı aynı olan her taş (aynı renk herhangi sayı, aynı sayı herhangi renk).
 *   - Sıra sende: uyan bir taşı bir uca koy ya da desteden 1 taş çek.
 *       · Koyabilecekken çekersen sıra geçer (çektiğin taşı koyamazsın).
 *       · Koyamazken çekersen uyan bir taş gelene dek (deste bitene dek) çekmeye devam edersin; gelen uyan taşı hemen koyabilir
 *         ya da pas diyebilirsin. Deste uyan taş gelmeden biterse sıra geçer (deste boşken koyamayanın pası sayılır).
 *       · Deste bittiyse ve koyamıyorsan pas; deste bittiyse ve koyabiliyorsan koymak zorunlu.
 *   - Ek hamle (ödül): koyduğun taş bağlandığı uçla AYNI RENKTEN ARDIŞIKSA (tam ±1; 13 ile 1 ardışık değil) ya da koyduktan sonra
 *     iki uç AYNI SAYI olursa bir taş daha koyma hakkı kazanırsın (çekme yok; istemezsen pas; uyan taşın yoksa hak doğmaz).
 *     Ek hamleyle koyduğun taş yeni bir ek hamle doğurmaz (turda en çok 2 taş).
 *   - Elini ilk bitiren kazanır: her rakip elindeki sayıların toplamı kadar eksi alır, kazanan bu toplamların hepsini artı alır.
 *   - Kilit: deste bitmiş ve koyamayan herkes art arda pas geçtiyse el biter; el toplamı en düşük olan(lar) kazanır.
 *     Diğerleri kendi toplamı kadar eksi alır, kazananlar bu eksilerin toplamını eşit paylaşır (aşağı yuvarlanır).
 */
import type { ElSatir, ElSonuc, Motor, Olay, Rng, Tas } from '../tipler';
import { karistir, tasSeti } from './okeyOrtak';

export type DominoUc = 'bas' | 'son';
export type DominoHamle = { t: 'koy'; tas: number; uc: DominoUc } | { t: 'cek' } | { t: 'pas' };

export interface DominoOyuncuGorunum { id: string; tasSayisi: number }
export interface DominoGorunum {
  tur: 'domino';
  elNo: number;
  sira: string;
  oyuncular: DominoOyuncuGorunum[];
  /** Bakanın eli (izleyicide boş) */
  elim: Tas[];
  /** Zincir soldan sağa: [0] = baş ucu, [son] = son ucu */
  zincir: Tas[];
  uclar: { bas: Tas; son: Tas };
  deste: number;
  /** Sıradakinin bu turdaki durumu. cekilen yalnız sırası olan bakana gösterilir. */
  tur_: { cekti: boolean; cekilen?: number; ek: boolean };
  /** Bakanın sırası ise koyabileceği (taş, uç) çiftleri; değilse boş */
  secenekler: { tas: number; uc: DominoUc }[];
  /** Bakan pas diyebilir mi / çekebilir mi (sırası değilse false) */
  pasOlur: boolean;
  cekOlur: boolean;
  /** Deste boşken art arda pas sayısı */
  pasSayisi: number;
  /** Son konan taş (vurgu için) */
  son?: { o: string; tas: number; uc: DominoUc };
  bitti: boolean;
}

export interface DominoOyuncu { id: string; el: Tas[] }
export interface DominoDurum {
  tur: 'domino';
  elNo: number;
  oyuncular: DominoOyuncu[];
  sira: number;
  /** Son eleman en üstte */
  deste: Tas[];
  zincir: Tas[];
  /** Bu turda koyamazken çekip uyan taş aldı: yalnız o taş konabilir ya da pas */
  cekilen: number | null;
  /** Ek hamle hakkı (yalnız koy ya da pas) */
  ek: boolean;
  /** Deste boşken art arda koyamayanların pası */
  pasSayisi: number;
  son: { o: string; tas: number; uc: DominoUc } | null;
  sonuc: ElSonuc | null;
}

export const EL_TAS = 7;

/** Taş, uçtaki taşa uyar mı: aynı renk ya da aynı sayı */
export const uyar = (tas: { s: number; r: number }, uc: { s: number; r: number }): boolean => tas.r === uc.r || tas.s === uc.s;

/** Ek hamle nedeni: aynı renkten ardışık bağlandı ya da iki uç aynı sayı oldu; yoksa null */
export function ekNedeni(tas: Tas, eskiUc: Tas, yeniZincir: Tas[]): 'ardisik' | 'esuc' | null {
  if (tas.r === eskiUc.r && Math.abs(tas.s - eskiUc.s) === 1) return 'ardisik';
  const u = uclar(yeniZincir);
  return yeniZincir.length > 1 && u.bas.s === u.son.s ? 'esuc' : null;
}

export const uclar = (zincir: Tas[]) => ({ bas: zincir[0], son: zincir[zincir.length - 1] });

/** Elin zincire konabilecek (taş, uç) çiftleri */
export function koyuslar(el: Tas[], zincir: Tas[]): { tas: number; uc: DominoUc }[] {
  const { bas, son } = uclar(zincir);
  const out: { tas: number; uc: DominoUc }[] = [];
  for (const t of el) {
    if (uyar(t, bas)) out.push({ tas: t.id, uc: 'bas' });
    if (uyar(t, son)) out.push({ tas: t.id, uc: 'son' });
  }
  return out;
}

export const elToplam = (el: Tas[]) => el.reduce((t, x) => t + x.s, 0);

function sonuclandir(d: DominoDurum, kazananlar: string[], neden: ElSonuc['neden']): ElSonuc {
  const kaz = new Set(kazananlar);
  const kayip = d.oyuncular.filter((o) => !kaz.has(o.id)).reduce((t, o) => t + elToplam(o.el), 0);
  const pay = Math.floor(kayip / Math.max(1, kazananlar.length));
  const satirlar: ElSatir[] = d.oyuncular.map((o) => {
    const top = elToplam(o.el);
    return kaz.has(o.id)
      ? { id: o.id, puan: pay, kalan: o.el.length, kazandi: true, cezalar: [], aciklama: neden === 'bitti' ? `Eli bitirdi (+${pay})` : `En düşük el ${top} (+${pay})` }
      : { id: o.id, puan: -top, kalan: o.el.length, kazandi: false, cezalar: [], aciklama: `${o.el.length} taş, toplam ${top} (−${top})` };
  });
  return { neden, kazananlar, satirlar };
}

/** Sırayı bir sonraki oyuncuya geçirir (tur bayrakları sıfırlanır) */
const siraGec = (d: DominoDurum, olaylar: Olay[]) => {
  d.sira = (d.sira + 1) % d.oyuncular.length;
  d.cekilen = null;
  d.ek = false;
  olaylar.push({ t: 'sira', o: d.oyuncular[d.sira].id });
};

/** Deste boşken pas: koyabilecek biri pas diyorsa (ek hakkını geri çevirme) sayaç sıfırlanır */
function pasIsle(d: DominoDurum, koyabilirdi: boolean, olaylar: Olay[]) {
  if (d.deste.length === 0) d.pasSayisi = koyabilirdi ? 0 : d.pasSayisi + 1;
  if (d.deste.length === 0 && d.pasSayisi >= d.oyuncular.length) {
    const en = Math.min(...d.oyuncular.map((o) => elToplam(o.el)));
    d.sonuc = sonuclandir(d, d.oyuncular.filter((o) => elToplam(o.el) === en).map((o) => o.id), 'berabere');
    olaylar.push({ t: 'kilit' }, { t: 'elBitti' });
    return;
  }
  siraGec(d, olaylar);
}

const kopya = (d: DominoDurum): DominoDurum => ({
  ...d, oyuncular: d.oyuncular.map((o) => ({ ...o, el: o.el.slice() })), deste: d.deste.slice(), zincir: d.zincir.slice(), son: d.son && { ...d.son },
});

/* ---------------- bot ---------------- */

/** Belirlenimci sezgisel: ek hamle fırsatı, devamı olan, rakibe az seçenek bırakan, büyük sayılı taşı seç */
export function dominoBotSec(d: DominoDurum, ben: number, secenekler: { tas: number; uc: DominoUc }[]) {
  const el = d.oyuncular[ben].el;
  const elMap = new Map(el.map((t) => [t.id, t]));
  // görülen taşlar: zincir + elim → görülmeyen kopyalar rakiplerde ya da destede olabilir
  const gorulen = new Map<number, number>();
  for (const t of [...d.zincir, ...el]) gorulen.set(t.s * 4 + t.r, (gorulen.get(t.s * 4 + t.r) ?? 0) + 1);
  const gorunmeyenUyan = (u: Tas) => {
    let n = 0;
    for (let s = 1; s <= 13; s++) for (let r = 0; r < 4; r++) if (uyar({ s, r }, u)) n += 2 - (gorulen.get(s * 4 + r) ?? 0);
    return n;
  };
  const rakipAz = Math.min(...d.oyuncular.filter((_, i) => i !== ben).map((o) => o.el.length));
  const baski = rakipAz <= 2 ? 3 : rakipAz <= 4 ? 1.5 : 0.6;
  let en = -Infinity, sec = secenekler[0];
  for (const k of secenekler) {
    const t = elMap.get(k.tas)!;
    const z = k.uc === 'bas' ? [t, ...d.zincir] : [...d.zincir, t];
    const u = uclar(z);
    const kalan = el.filter((x) => x.id !== t.id);
    const devam = kalan.filter((x) => uyar(x, u.bas) || uyar(x, u.son)).length;
    const yeni = gorunmeyenUyan(u.bas) + gorunmeyenUyan(u.son);
    let p = devam * 3 + t.s * 0.4 - yeni * baski * 0.5;
    if (!d.ek && devam > 0 && ekNedeni(t, k.uc === 'bas' ? d.zincir[0] : d.zincir[d.zincir.length - 1], z)) p += 8;
    if (!kalan.length) p += 1000;
    if (p > en || (p === en && (k.tas < sec.tas || (k.tas === sec.tas && k.uc < sec.uc)))) { en = p; sec = k; }
  }
  return sec;
}

/* ---------------- motor ---------------- */

export const dominoMotor: Motor = {
  tur: 'domino' as any, min: 2, max: 4,

  elBaslat({ oyuncular, elNo, baslayan, rng }) {
    const deste = karistir(tasSeti(), rng);
    const os: DominoOyuncu[] = oyuncular.map((o) => ({ id: o.id, el: deste.splice(deste.length - EL_TAS, EL_TAS) }));
    const ilk = deste.pop()!;
    const d: DominoDurum = {
      tur: 'domino', elNo, oyuncular: os, sira: ((baslayan % os.length) + os.length) % os.length, deste, zincir: [ilk],
      cekilen: null, ek: false, pasSayisi: 0, son: null, sonuc: null,
    };
    return d;
  },

  uygula(durum, oyuncu, hamle) {
    const g = durum as DominoDurum, h = hamle as Partial<DominoHamle> & { tas?: unknown; uc?: unknown };
    if (g.sonuc) return { hata: 'El bitti.' };
    const i = g.oyuncular.findIndex((o) => o.id === oyuncu);
    if (i < 0) return { hata: 'Bu masada oyuncu değilsin.' };
    if (i !== g.sira) return { hata: 'Sıra sende değil.' };
    const el = g.oyuncular[i].el;
    const olabilir = koyuslar(el, g.zincir);
    const olaylar: Olay[] = [];

    if (h?.t === 'koy') {
      const t = el.find((x) => x.id === h.tas);
      if (!t) return { hata: 'Bu taş elinde değil.' };
      if (h.uc !== 'bas' && h.uc !== 'son') return { hata: 'Uç seçilmedi.' };
      if (g.cekilen != null && t.id !== g.cekilen) return { hata: 'Çektikten sonra yalnız çektiğin taşı koyabilirsin.' };
      if (!uyar(t, uclar(g.zincir)[h.uc])) return { hata: 'Bu taş o uca uymuyor.' };
      const d = kopya(g);
      const o = d.oyuncular[i];
      o.el = o.el.filter((x) => x.id !== t.id);
      const eskiUc = uclar(g.zincir)[h.uc];
      if (h.uc === 'bas') d.zincir.unshift(t); else d.zincir.push(t);
      d.son = { o: oyuncu, tas: t.id, uc: h.uc };
      d.pasSayisi = 0;
      olaylar.push({ t: 'koydu', o: oyuncu, tas: t, uc: h.uc, ek: g.ek });
      if (!o.el.length) {
        d.sonuc = sonuclandir(d, [oyuncu], 'bitti');
        olaylar.push({ t: 'elBitti' });
        return { durum: d, olaylar };
      }
      const neden = g.ek ? null : ekNedeni(t, eskiUc, d.zincir);
      if (neden && koyuslar(o.el, d.zincir).length) {
        d.ek = true; d.cekilen = null;
        olaylar.push({ t: 'ekHamle', o: oyuncu, neden });
        return { durum: d, olaylar };
      }
      siraGec(d, olaylar);
      return { durum: d, olaylar };
    }

    if (h?.t === 'cek') {
      if (g.ek) return { hata: 'Ek hamlede çekilmez: koy ya da pas de.' };
      if (g.cekilen != null) return { hata: 'Bu turda zaten çektin.' };
      if (!g.deste.length) return { hata: 'Deste bitti.' };
      const d = kopya(g);
      const ucs = uclar(d.zincir);
      if (olabilir.length) {
        // koyabilecekken çekmek: 1 taş, sıra geçer
        const t = d.deste.pop()!;
        d.oyuncular[i].el.push(t);
        olaylar.push({ t: 'cekti', o: oyuncu, adet: 1 }, { t: 'cektim', kime: oyuncu, tas: t, taslar: [t] });
        siraGec(d, olaylar);
        return { durum: d, olaylar };
      }
      // koyamıyorken: uyan taş gelene (ya da deste bitene) dek çekilir
      const cekilen: Tas[] = [];
      let uyan: Tas | null = null;
      while (d.deste.length && !uyan) {
        const t = d.deste.pop()!;
        cekilen.push(t);
        if (uyar(t, ucs.bas) || uyar(t, ucs.son)) uyan = t;
      }
      d.oyuncular[i].el.push(...cekilen);
      olaylar.push({ t: 'cekti', o: oyuncu, adet: cekilen.length }, { t: 'cektim', kime: oyuncu, tas: cekilen[cekilen.length - 1], taslar: cekilen });
      if (uyan) { d.cekilen = uyan.id; return { durum: d, olaylar }; }
      pasIsle(d, false, olaylar); // deste bitti, uyan gelmedi: koyamayanın pası sayılır
      return { durum: d, olaylar };
    }

    if (h?.t === 'pas') {
      if (!(g.ek || g.cekilen != null || (!g.deste.length && !olabilir.length))) {
        return { hata: g.deste.length ? 'Pas yok: koy ya da çek.' : 'Koyabileceğin taş var; deste bittiği için koymalısın.' };
      }
      const d = kopya(g);
      olaylar.push({ t: 'pas', o: oyuncu });
      pasIsle(d, olabilir.length > 0, olaylar);
      return { durum: d, olaylar };
    }
    return { hata: 'Geçersiz hamle.' };
  },

  gorunum(durum, bakan) {
    const d = durum as DominoDurum;
    const bi = d.oyuncular.findIndex((o) => o.id === bakan);
    const siram = bi >= 0 && bi === d.sira && !d.sonuc;
    const el = bi >= 0 ? d.oyuncular[bi].el : [];
    let secenekler = siram ? koyuslar(el, d.zincir) : [];
    if (siram && d.cekilen != null) secenekler = secenekler.filter((k) => k.tas === d.cekilen);
    const g: DominoGorunum = {
      tur: 'domino', elNo: d.elNo, sira: d.oyuncular[d.sira].id,
      oyuncular: d.oyuncular.map((o) => ({ id: o.id, tasSayisi: o.el.length })),
      elim: el.slice(), zincir: d.zincir.slice(), uclar: uclar(d.zincir), deste: d.deste.length,
      tur_: { cekti: d.cekilen != null, ek: d.ek, ...(siram && d.cekilen != null ? { cekilen: d.cekilen } : {}) },
      secenekler,
      pasOlur: siram && (d.ek || d.cekilen != null || (!d.deste.length && !secenekler.length)),
      cekOlur: siram && !d.ek && d.cekilen == null && d.deste.length > 0,
      pasSayisi: d.pasSayisi, ...(d.son ? { son: { ...d.son } } : {}), bitti: !!d.sonuc,
    };
    return g as any;
  },

  botHamle(durum, bot) {
    const d = durum as DominoDurum;
    if (d.sonuc || d.oyuncular[d.sira].id !== bot) return null;
    let s = koyuslar(d.oyuncular[d.sira].el, d.zincir);
    if (d.cekilen != null) s = s.filter((k) => k.tas === d.cekilen);
    if (s.length) { const k = dominoBotSec(d, d.sira, s); return { t: 'koy', tas: k.tas, uc: k.uc }; }
    if (!d.ek && d.cekilen == null && d.deste.length) return { t: 'cek' };
    return { t: 'pas' };
  },

  sonuc(durum) { return (durum as DominoDurum).sonuc; },
};
export default dominoMotor;
