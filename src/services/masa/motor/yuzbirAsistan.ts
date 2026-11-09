/**
 * 101 Okey — saf yardımcılar (yan etkisiz). Motor (`yuzbir.ts`) kuralları buradan okur; istemci aynı işlevleri
 * ıstaka dizimi, "kaç puan var" göstergesi ve ipuçları için kullanır.
 *
 * Okey (joker) = göstergenin bir üstü; her taşın yerine geçer. Sahte okey (s=0) joker DEĞİLDİR: okeyin sayı+rengini taşır.
 */
import type { OkeyGorunum, OkeyHamle, Per, PerTur, Renk, Tas } from '../tipler';

export type Okey = { s: number; r: Renk };
type Deger = { s: number; r: Renk };

export const ACILIS_ESIK = 101;
export const ACILIS_CIFT = 5;

/** Göstergeden okey: aynı renk, sayı +1 (13 → 1) */
export const okeyBul = (gosterge: Tas): Okey => ({ s: (gosterge.s % 13) + 1, r: gosterge.r });

export function jokerMi(t: Tas, okey: Okey): boolean {
  return t.s !== 0 && t.s === okey.s && t.r === okey.r;
}

/** Taşın kendi değeri: sahte okey → okeyin değeri; joker → null */
export function gercek(t: Tas, okey: Okey): Deger | null {
  if (t.s === 0) return { s: okey.s, r: okey.r };
  return jokerMi(t, okey) ? null : { s: t.s, r: t.r };
}

/** Masadaki taşın temsil ettiği değer (joker → `yerine`) */
export function etkin(t: Tas, okey: Okey): Deger {
  return t.yerine ?? gercek(t, okey) ?? { s: okey.s, r: okey.r };
}

const sade = (t: Tas): Tas => ({ id: t.id, s: t.s, r: t.r });
const yerineKoy = (t: Tas, s: number, r: Renk): Tas => ({ id: t.id, s: t.s, r: t.r, yerine: { s, r } });
const ardisik = (a: number, b: number) => ((a + b) * (b - a + 1)) / 2;

/** Elde kalan taşların el-sonu değeri (okey 101 sayılır) */
export function elDegeri(el: Tas[], okey: Okey): number {
  let top = 0;
  for (const t of el) top += gercek(t, okey)?.s ?? 101;
  return top;
}

/**
 * Taş kümesini per olarak çözer: 2 taş → çift; ≥3 → seri ya da grup. Geçerliyse dizilmiş taşlar (jokerlerde `yerine` dolu) ve değer.
 * Seride boşta kalan joker en yüksek değeri veren uca gider (13'ü aşamaz, artanı alta).
 */
export function perCoz(taslar: Tas[], okey: Okey): { tur: PerTur; taslar: Tas[]; deger: number } | null {
  const n = taslar.length;
  if (n < 2 || n > 13) return null;
  const jok: Tas[] = [];
  const ger: { t: Tas; s: number; r: Renk }[] = [];
  for (const t of taslar) {
    const g = gercek(t, okey);
    if (g) ger.push({ t: sade(t), s: g.s, r: g.r });
    else jok.push(t);
  }
  if (n === 2) {
    if (!ger.length) return { tur: 'cift', taslar: jok.map((j) => yerineKoy(j, okey.s, okey.r)), deger: 2 * okey.s };
    const a = ger[0];
    if (ger.length === 1) return { tur: 'cift', taslar: [a.t, yerineKoy(jok[0], a.s, a.r)], deger: 2 * a.s };
    return a.s === ger[1].s && a.r === ger[1].r ? { tur: 'cift', taslar: [a.t, ger[1].t], deger: 2 * a.s } : null;
  }
  if (ger.length < 2) return null; // bir perde en az 2 gerçek taş
  const s0 = ger[0].s;
  const r0 = ger[0].r;
  if (ger.every((g) => g.s === s0)) {
    if (n > 4) return null;
    const yer: (Tas | null)[] = [null, null, null, null];
    for (const g of ger) {
      if (yer[g.r]) return null;
      yer[g.r] = g.t;
    }
    let j = 0;
    for (let r = 0; r < 4 && j < jok.length; r++) if (!yer[r]) yer[r] = yerineKoy(jok[j++], s0, r as Renk);
    return { tur: 'grup', taslar: yer.filter((t): t is Tas => !!t), deger: s0 * n };
  }
  if (!ger.every((g) => g.r === r0)) return null;
  ger.sort((a, b) => a.s - b.s);
  for (let i = 1; i < ger.length; i++) if (ger[i].s === ger[i - 1].s) return null;
  const alt = ger[0].s;
  const ust = ger[ger.length - 1].s;
  const ic = ust - alt + 1 - ger.length;
  if (ic > jok.length) return null;
  const bos = jok.length - ic;
  const yukari = Math.min(bos, 13 - ust);
  const asagi = bos - yukari;
  if (alt - asagi < 1) return null;
  const dizi: Tas[] = [];
  let gi = 0;
  let ji = 0;
  for (let v = alt - asagi; v <= ust + yukari; v++) {
    if (gi < ger.length && ger[gi].s === v) dizi.push(ger[gi++].t);
    else dizi.push(yerineKoy(jok[ji++], v, r0));
  }
  return { tur: 'seri', taslar: dizi, deger: ardisik(alt - asagi, ust + yukari) };
}

/** Taşın masada işlenebileceği yerler (`per` = per kimliği). Seride uç her zaman dolu, grupta null. Çifte işlenmez. */
export function islemeYerleri(tas: Tas, perler: Per[], okey: Okey): { per: number; uc: 'bas' | 'son' | null }[] {
  const out: { per: number; uc: 'bas' | 'son' | null }[] = [];
  const g = gercek(tas, okey);
  for (const p of perler) {
    if (p.tur === 'seri' && p.taslar.length) {
      const a = etkin(p.taslar[0], okey);
      const alt = a.s;
      const ust = etkin(p.taslar[p.taslar.length - 1], okey).s;
      if (!g) {
        if (alt > 1) out.push({ per: p.id, uc: 'bas' });
        if (ust < 13) out.push({ per: p.id, uc: 'son' });
      } else if (g.r === a.r) {
        if (g.s === alt - 1) out.push({ per: p.id, uc: 'bas' });
        else if (g.s === ust + 1) out.push({ per: p.id, uc: 'son' });
      }
    } else if (p.tur === 'grup' && p.taslar.length === 3) {
      if (!g) out.push({ per: p.id, uc: null });
      else if (g.s === etkin(p.taslar[0], okey).s && p.taslar.every((t) => etkin(t, okey).r !== g.r)) out.push({ per: p.id, uc: null });
    }
  }
  return out;
}

/* ------------------------------------------------------------------ arama ------------------------------------------------------------------ */

export interface AraSecenek {
  /** Bu taş (kimlik) mutlaka bir perde yer alsın (yandan alınan taş) */
  zorunlu?: number;
  /** Elde en az bu kadar taş kalsın (atış için 1) */
  birak?: number;
  /** Düğüm tavanı: aşılınca o ana dek bulunan en iyi döner */
  tavan?: number;
}

interface Secim { h: number[]; j: number; d: number }

/**
 * Elden çıkarılabilecek en yüksek toplamlı ayrık seri/grup kümesi (geri izlemeli, dal-sınır).
 * Hücre = (sayı, renk) → adet (özdeş taşlar birbirinin yerine geçer); taşlar en küçük hücreden başlanarak ya bir pere girer ya atlanır.
 */
export function perAra(el: Tas[], okey: Okey, sec: AraSecenek = {}): { perler: Tas[][]; toplam: number } {
  const cnt = new Int8Array(52);
  const hucre: Tas[][] = Array.from({ length: 52 }, () => []);
  const jok: Tas[] = [];
  let zorH = -1;
  let zorJ = false;
  for (const t of el) {
    const g = gercek(t, okey);
    const zor = t.id === sec.zorunlu;
    if (!g) {
      if (zor) { zorJ = true; jok.unshift(t); } else jok.push(t);
      continue;
    }
    const i = (g.s - 1) * 4 + g.r;
    cnt[i]++;
    if (zor) { zorH = i; hucre[i].unshift(t); } else hucre[i].push(t);
  }
  const J0 = jok.length;
  const birak = sec.birak ?? 0;
  const tavan = sec.tavan ?? 30000;
  const var_ = (s: number, r: number) => s >= 1 && s <= 13 && cnt[(s - 1) * 4 + r] > 0;
  // Hiçbir pere giremeyecek taşlar üst sınıra katılmaz (budama sıkılaşır)
  const yarar = new Uint8Array(52);
  let kalan0 = 0;
  for (let i = 0; i < 52; i++) {
    if (!cnt[i]) continue;
    const s = (i >> 2) + 1;
    const r = i & 3;
    let ayni = 0;
    for (let q = 0; q < 4; q++) if (q !== r && var_(s, q)) ayni++;
    let ok: boolean;
    if (J0 === 0) ok = ayni >= 2 || (var_(s - 2, r) && var_(s - 1, r)) || (var_(s - 1, r) && var_(s + 1, r)) || (var_(s + 1, r) && var_(s + 2, r));
    else {
      ok = ayni >= 1;
      for (let k = 1; k <= J0 + 1 && !ok; k++) ok = var_(s - k, r) || var_(s + k, r);
    }
    if (ok) { yarar[i] = 1; kalan0 += cnt[i] * s; }
  }

  const yigin: Secim[] = [];
  let enIyi = -1;
  let enIyiY: Secim[] = [];
  let dugum = 0;
  let kesildi = false;

  const git = (i0: number, J: number, top: number, kalan: number, artik: number, zorKaldi: boolean): void => {
    if (++dugum > tavan) { kesildi = true; return; }
    let i = i0;
    while (i < 52 && !cnt[i]) i++;
    if (i === 52) {
      if (artik + J >= birak && !zorKaldi && (!zorJ || J < J0) && top > enIyi) { enIyi = top; enIyiY = yigin.slice(); }
      return;
    }
    if (top + kalan + J * 13 <= enIyi) return;
    const s = (i >> 2) + 1;
    const r = i & 3;
    if (yarar[i]) {
      const secenek: Secim[] = [];
      // seri: en küçük gerçek taşı bu hücre; aradaki boşluklar ve uçlar jokerle
      const uzat = (h: number[], son: number, ic: number): void => {
        if (h.length >= 2) {
          for (let e = 0; ic + e <= J; e++) {
            const n = son - s + 1 + e;
            if (n < 3) continue;
            const yukari = Math.min(e, 13 - son);
            const asagi = e - yukari;
            if (n > 13 || s - asagi < 1) break;
            secenek.push({ h: h.slice(), j: ic + e, d: ardisik(s - asagi, son + yukari) });
          }
        }
        for (let k = 0; ic + k <= J; k++) {
          const v = son + 1 + k;
          if (v > 13) break;
          const c = (v - 1) * 4 + r;
          if (cnt[c] > 0) { h.push(c); uzat(h, v, ic + k); h.pop(); }
        }
      };
      uzat([i], s, 0);
      // grup: bu hücre + aynı sayının sonraki renkleri (+ joker)
      const diger: number[] = [];
      for (let q = r + 1; q < 4; q++) if (cnt[(s - 1) * 4 + q] > 0) diger.push((s - 1) * 4 + q);
      for (let m = 1; m < 1 << diger.length; m++) {
        const h = [i];
        for (let b = 0; b < diger.length; b++) if (m & (1 << b)) h.push(diger[b]);
        for (let e = 0; e <= J; e++) {
          const n = h.length + e;
          if (n >= 3 && n <= 4) secenek.push({ h, j: e, d: s * n });
        }
      }
      secenek.sort((a, b) => b.d - a.d);
      for (const o of secenek) {
        let dus = 0;
        for (const c of o.h) { cnt[c]--; dus += (c >> 2) + 1; }
        yigin.push(o);
        git(i, J - o.j, top + o.d, kalan - dus, artik, zorKaldi && !o.h.includes(zorH));
        yigin.pop();
        for (const c of o.h) cnt[c]++;
        if (kesildi) return;
      }
    }
    if (zorKaldi && i === zorH && cnt[i] === 1) return; // zorunlu taş atlanamaz
    cnt[i]--;
    git(i, J, top, kalan - (yarar[i] ? s : 0), artik + 1, zorKaldi);
    cnt[i]++;
  };
  git(0, J0, 0, kalan0, 0, zorH >= 0);

  const perler: Tas[][] = [];
  let toplam = 0;
  for (const o of enIyiY) {
    const ts = o.h.map((c) => hucre[c].shift() as Tas);
    for (let k = 0; k < o.j; k++) ts.push(jok.shift() as Tas);
    const c = perCoz(ts, okey);
    if (!c) continue;
    perler.push(c.taslar);
    toplam += c.deger;
  }
  return { perler, toplam };
}

/** Eldeki en çok sayıda çift (joker eksik eşin yerine; iki joker de çift). `birak`: elde taş kalsın diye gerekirse son çift bırakılır. */
export function ciftBul(el: Tas[], okey: Okey, sec: AraSecenek = {}): Tas[][] {
  const hucre = new Map<number, Tas[]>();
  const jok: Tas[] = [];
  for (const t of el) {
    const g = gercek(t, okey);
    if (!g) { if (t.id === sec.zorunlu) jok.unshift(t); else jok.push(t); continue; }
    const k = g.s * 4 + g.r;
    const l = hucre.get(k);
    if (l) l.push(t); else hucre.set(k, [t]);
  }
  const ham: Tas[][] = [];
  const tek: Tas[] = [];
  for (const l of hucre.values()) {
    if (l.length >= 2) ham.push([l[0], l[1]]);
    else tek.push(l[0]);
  }
  const sv = (t: Tas) => gercek(t, okey)?.s ?? 0;
  tek.sort((a, b) => (a.id === sec.zorunlu ? -1 : b.id === sec.zorunlu ? 1 : sv(b) - sv(a)));
  while (jok.length && tek.length) ham.push([tek.shift() as Tas, jok.shift() as Tas]);
  if (jok.length >= 2) ham.push([jok[0], jok[1]]);
  const birak = sec.birak ?? 0;
  while (ham.length && el.length - ham.length * 2 < birak) {
    // zorunlu taşı içermeyen bir çift bırakılır
    let k = ham.length - 1;
    while (k > 0 && ham[k].some((t) => t.id === sec.zorunlu)) k--;
    ham.splice(k, 1);
  }
  const out: Tas[][] = [];
  for (const p of ham) {
    const c = perCoz(p, okey);
    if (c) out.push(c.taslar);
  }
  return out;
}

const icerir = (perler: Tas[][], id: number | undefined) => id === undefined || perler.some((p) => p.some((t) => t.id === id));
const perDeger = (p: Tas[], okey: Okey) => p.reduce((a, t) => a + etkin(t, okey).s, 0);

/** Açılış araması (kısıtlı): önce seri/grup ≥ 101, olmazsa ≥ 5 çift */
export function acilisAra(el: Tas[], okey: Okey, sec: AraSecenek = {}): { perler: Tas[][]; toplam: number; cift: boolean } | null {
  const a = perAra(el, okey, sec);
  if (a.toplam >= ACILIS_ESIK && icerir(a.perler, sec.zorunlu)) return { ...a, cift: false };
  const c = ciftBul(el, okey, sec);
  if (c.length >= ACILIS_CIFT && icerir(c, sec.zorunlu)) return { perler: c, toplam: c.reduce((x, p) => x + perDeger(p, okey), 0), cift: true };
  return null;
}

/** En yüksek toplamlı seri/grup açılışı (≥ 101) ya da ≥ 5 çift; yoksa null. (Atacak taş bırakma kısıtı için `acilisAra`.) */
export function acilisBul(el: Tas[], okey: Okey): { perler: Tas[][]; toplam: number; cift: boolean } | null {
  return acilisAra(el, okey);
}

/** Açılışa en yakın dizilim: en yüksek toplamlı seri/grup kümesi + (ayrıca, tüm elden) çiftler */
export function enIyiDizilim(el: Tas[], okey: Okey): { perler: Tas[][]; toplam: number; ciftler: Tas[][] } {
  return { ...perAra(el, okey), ciftler: ciftBul(el, okey) };
}

/** Açmış oyuncunun elden açabileceği tek ek per (elde ≥ 1 taş kalır); çiftle açan için çift */
export function ekPer(el: Tas[], okey: Okey, ciftActi: boolean, zorunlu?: number): Tas[] | null {
  const sec = { birak: 1, zorunlu };
  const perler = ciftActi ? ciftBul(el, okey, sec) : perAra(el, okey, sec).perler;
  if (zorunlu === undefined) return perler[0] ?? null;
  return perler.find((p) => p.some((t) => t.id === zorunlu)) ?? null;
}

/** Istaka sıralaması (taş kimlikleri). 'per': en iyi dizilimin perleri yan yana, artanlar sonda. */
export function elSirala(el: Tas[], okey: Okey, kip: 'seri' | 'grup' | 'per'): number[] {
  const anahtar = (t: Tas): [number, number] => {
    const g = gercek(t, okey);
    return g ? [g.s, g.r] : [99, 9]; // jokerler sonda
  };
  const sirali = (l: Tas[], renkOnce: boolean) =>
    l.slice().sort((a, b) => {
      const [as, ar] = anahtar(a);
      const [bs, br] = anahtar(b);
      return (renkOnce ? ar - br || as - bs : as - bs || ar - br) || a.id - b.id;
    });
  if (kip !== 'per') return sirali(el, kip === 'seri').map((t) => t.id);
  const ids: number[] = [];
  for (const p of perAra(el, okey).perler) for (const t of p) ids.push(t.id);
  const kullanildi = new Set(ids);
  for (const t of sirali(el.filter((x) => !kullanildi.has(x.id)), true)) ids.push(t.id);
  return ids;
}

/* ------------------------------------------------------------------ bot + ipucu ------------------------------------------------------------------ */

/** Sırası olan oyuncunun karar bağlamı (durumdan ya da görünümden kurulur; başkasının eli yok) */
export interface BotBaglam {
  el: Tas[];
  okey: Okey;
  perler: Per[];
  acti: boolean;
  ciftActi: boolean;
  cekti: boolean;
  yandanAlinan: number | null;
  /** Önceki oyuncunun son attığı taş */
  oncekiAtik: Tas | null;
  deste: number;
}

/** Yandaki taş alınırsa bu turda kesin kullanılabilir mi */
export function yandanIseYarar(b: BotBaglam): boolean {
  const t = b.oncekiAtik;
  if (!t) return false;
  const el = [...b.el, t];
  if (!b.acti) return !!acilisAra(el, b.okey, { zorunlu: t.id, birak: 1 });
  return islemeYerleri(t, b.perler, b.okey).length > 0 || !!ekPer(el, b.okey, b.ciftActi, t.id);
}

/** Atılacak taş: işlek ve joker olmayan, per kurmaya en az yarayan en yüksek değerli taş (yalnız cezalılar kaldıysa önce işlek, en son okey) */
export function atisSec(el: Tas[], perler: Per[], okey: Okey, acti: boolean, ciftActi: boolean): number {
  const diz = enIyiDizilim(el, okey);
  const ciftYolu = ciftActi || (!acti && diz.ciftler.length >= 4 && diz.toplam < 81);
  const korunan = new Set<number>();
  for (const p of ciftYolu ? diz.ciftler : diz.perler) for (const t of p) korunan.add(t.id);
  let sec = el[0]?.id ?? -1;
  let enAz = Infinity;
  for (const t of el) {
    const g = gercek(t, okey);
    let puan: number;
    if (!g) puan = 1e6;
    else {
      let y = korunan.has(t.id) ? 100 : 0;
      for (const u of el) {
        if (u.id === t.id) continue;
        const h = gercek(u, okey);
        if (!h) continue;
        const fark = Math.abs(h.s - g.s);
        if (h.r === g.r) y += fark === 0 ? (ciftYolu ? 40 : 0) : !ciftYolu && fark === 1 ? 10 : !ciftYolu && fark === 2 ? 6 : 0;
        else if (fark === 0 && !ciftYolu) y += 8;
      }
      puan = (islemeYerleri(t, perler, okey).length ? 1e5 : 0) + y * 20 - g.s;
    }
    if (puan < enAz) { enAz = puan; sec = t.id; }
  }
  return sec;
}

const isleHamle = (tas: number, y: { per: number; uc: 'bas' | 'son' | null }): OkeyHamle => (y.uc ? { t: 'isle', tas, per: y.per, uc: y.uc } : { t: 'isle', tas, per: y.per });

/** Botun (ve "benim yerime oyna"nın) tek hamlesi: cezasız, kurala uygun */
export function botSec(b: BotBaglam): OkeyHamle {
  const { el, okey, perler } = b;
  if (!b.cekti) return { t: 'cek', kaynak: yandanIseYarar(b) ? 'atik' : 'deste' };
  const y = b.yandanAlinan;
  const at = (): OkeyHamle => (y !== null ? { t: 'geriKoy' } : { t: 'at', tas: atisSec(el, perler, okey, b.acti, b.ciftActi) });
  if (!b.acti) {
    const a = acilisAra(el, okey, { birak: 1, zorunlu: y ?? undefined });
    return a ? { t: 'ac101', perler: a.perler.map((p) => p.map((t) => t.id)) } : at();
  }
  if (el.length < 2) return at();
  if (y !== null) {
    const t = el.find((x) => x.id === y);
    const yer = t ? islemeYerleri(t, perler, okey)[0] : undefined;
    if (yer) return isleHamle(y, yer);
    const p = ekPer(el, okey, b.ciftActi, y);
    return p ? { t: 'ac', taslar: p.map((x) => x.id) } : at();
  }
  const p = ekPer(el, okey, b.ciftActi);
  if (p) return { t: 'ac', taslar: p.map((x) => x.id) };
  const jok: Tas[] = [];
  for (const t of el) {
    if (jokerMi(t, okey)) { jok.push(t); continue; }
    const yer = islemeYerleri(t, perler, okey)[0];
    if (yer) return isleHamle(t.id, yer);
  }
  // Okey elde 101 yazar: bitişe bir taş kaldıysa ya da deste azaldıysa masaya işlenir
  if (jok.length && (el.length - jok.length <= 1 || b.deste <= 8)) {
    const yerler = islemeYerleri(jok[0], perler, okey);
    const yer = yerler.find((x) => x.uc !== 'bas') ?? yerler[0];
    if (yer) return isleHamle(jok[0].id, yer);
  }
  return at();
}

/** Görünümden karar bağlamı (sıra `ben`de değilse null) */
export function baglamKur(g: OkeyGorunum, ben: string): BotBaglam | null {
  if (g.tur !== 'yuzbir' || g.bitti || g.sira !== ben || !g.okey) return null;
  const n = g.oyuncular.length;
  const i = g.oyuncular.findIndex((o) => o.id === ben);
  if (i < 0) return null;
  const o = g.oyuncular[i];
  const atik = g.oyuncular[(i - 1 + n) % n].atiklar ?? [];
  return {
    el: g.elim, okey: g.okey, perler: g.perler, acti: o.acti, ciftActi: !!o.ciftActi, cekti: g.tur_.cekti,
    yandanAlinan: g.yandanAlinan ?? null, oncekiAtik: atik[atik.length - 1] ?? null, deste: g.deste,
  };
}

export interface Ipucu { hamle: OkeyHamle; taslar: number[]; per?: number; aciklama: string }

/** Şu an yapılabilecek anlamlı hamleler: çekme seçenekleri, açılış, ek per, işlemeler, önerilen atış */
export function ipuclari(g: OkeyGorunum, ben: string): Ipucu[] {
  const b = baglamKur(g, ben);
  if (!b) return [];
  const { el, okey, perler } = b;
  const out: Ipucu[] = [];
  if (!b.cekti) {
    if (b.oncekiAtik && yandanIseYarar(b)) {
      out.push({
        hamle: { t: 'cek', kaynak: 'atik' }, taslar: [b.oncekiAtik.id],
        aciklama: b.acti ? 'Yandaki taşı al: bu turda perde ya da işlemede kullanabilirsin.' : 'Yandaki taşı al: bu taşla açabilirsin.',
      });
    }
    out.push({ hamle: { t: 'cek', kaynak: 'deste' }, taslar: [], aciklama: b.deste ? 'Desteden taş çek.' : 'Deste bitti: çekersen el biter.' });
    return out;
  }
  const y = b.yandanAlinan;
  if (!b.acti) {
    const a = acilisAra(el, okey, { birak: 1, zorunlu: y ?? undefined });
    if (a) {
      out.push({
        hamle: { t: 'ac101', perler: a.perler.map((p) => p.map((t) => t.id)) }, taslar: a.perler.flat().map((t) => t.id),
        aciklama: a.cift ? `${a.perler.length} çiftle açabilirsin.` : `${a.toplam} ile açabilirsin.`,
      });
    }
  } else if (el.length > 1) {
    const p = ekPer(el, okey, b.ciftActi, y ?? undefined);
    if (p) out.push({ hamle: { t: 'ac', taslar: p.map((t) => t.id) }, taslar: p.map((t) => t.id), aciklama: b.ciftActi ? 'Yeni çift açabilirsin.' : 'Yeni per açabilirsin.' });
    for (const t of el) {
      const yerler = islemeYerleri(t, perler, okey);
      const joker = jokerMi(t, okey);
      for (const yer of joker ? yerler.slice(0, 2) : yerler) {
        out.push({ hamle: isleHamle(t.id, yer), taslar: [t.id], per: yer.per, aciklama: joker ? 'Okeyi masadaki pere işleyebilirsin.' : 'Bu taş masadaki pere işlenir.' });
      }
    }
  }
  if (y !== null) out.push({ hamle: { t: 'geriKoy' }, taslar: [y], aciklama: 'Yandan aldığın taşı kullanamıyorsan geri koyup desteden çek.' });
  else {
    const tas = atisSec(el, perler, okey, b.acti, b.ciftActi);
    const t = el.find((x) => x.id === tas);
    if (t) {
      const cezali = el.length > 1 && (jokerMi(t, okey) || islemeYerleri(t, perler, okey).length > 0);
      out.push({ hamle: { t: 'at', tas }, taslar: [tas], aciklama: el.length === 1 ? 'Son taşını at: el biter.' : cezali ? 'Cezasız atılacak taş kalmadı (−101).' : 'Önerilen atış: işlek olmayan, en az işe yarayan taş.' });
    }
  }
  return out;
}
