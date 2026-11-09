/**
 * Düz Okey (klasik okey) kural motoru. Saf: durum düz JSON, `uygula` girdiyi değiştirmez, kural dışı her hamle `{ hata }`.
 *
 * 106 taş (104 + 2 sahte okey), gösterge + okey (joker). Herkese 14 taş, başlayana 15. Sıra: desteden ya da soldaki oyuncunun
 * (senden önceki) son attığı taşı çek, sonra bir taş at. 14 taşın tamamı seri/gruplara ya da 7 çifte ayrılınca son (15.) taşı
 * atarak bitirilir (`bitir`). Puan: biten 0, diğerleri −2; okey atarak ya da çiftle bitince −4, ikisi birden −8.
 * İlk turunda göstergenin aynısını gösteren oyuncu diğerlerine −1 yazdırır (bir kez). Deste biterse el berabere.
 *
 * Taş kimliği: r*26 + (s-1)*2 + kopya (0–103); sahte okeyler 104–105 (s=0).
 */
import type { Ceza, ElSatir, ElSonuc, Motor, OkeyGorunum, Olay, Per, Renk, Rng, Tas } from '../tipler';
import { atisSec, gercek, jokerMi, okeyBul, perAra, perCoz, type Okey } from './yuzbirAsistan';

/** Düz Okey hamleleri (tipler.ts OkeyHamle'ye eklenecek; `cek`/`at` 101 ile ortak) */
export type DuzHamle =
  | { t: 'cek'; kaynak?: 'deste' | 'atik' }
  | { t: 'at'; tas: number }
  /** Son taşı atarak bitir: `gruplar` kalan 14 taşın tamamı (seri/grup ya da 7 çift) */
  | { t: 'bitir'; tas: number; gruplar: number[][] }
  /** İlk turda göstergenin aynısını göster */
  | { t: 'goster' };

export interface DuzOyuncu {
  id: string;
  el: Tas[];
  atiklar: Tas[];
  cezalar: Ceza[];
  /** Bu elde en az bir taş attı (ilk tur geçti) */
  attiMi: boolean;
  gosterdi: boolean;
}

export interface DuzDurum {
  tur: 'duz';
  elNo: number;
  oyuncular: DuzOyuncu[];
  sira: number;
  deste: Tas[];
  gosterge: Tas;
  okey: Okey;
  cekti: boolean;
  /** Bu turda yandan alınan taş (bot geri atmaz) */
  yandan?: number | null;
  /** Desteden çekilmeden art arda yandan alma sayısı (botun sonsuz alıp-atma döngüsünü keser) */
  yanSeri?: number;
  /** Biten oyuncunun açtığı gruplar (el sonunda masada gösterilir) */
  bitis?: Per[];
  sonuc: ElSonuc | null;
}

export const DUZ_KAYIP = 2;
const EL_TAS = 14;
const tam = (x: unknown): x is number => typeof x === 'number' && Number.isInteger(x);

function desteKur(rng: Rng): Tas[] {
  const deste: Tas[] = [];
  for (let r = 0; r < 4; r++) for (let s = 1; s <= 13; s++) for (let k = 0; k < 2; k++) deste.push({ id: r * 26 + (s - 1) * 2 + k, s, r: r as Renk });
  deste.push({ id: 104, s: 0, r: 0 }, { id: 105, s: 0, r: 0 });
  for (let i = deste.length - 1; i > 0; i--) {
    const j = Math.min(i, Math.floor(rng() * (i + 1)));
    [deste[i], deste[j]] = [deste[j], deste[i]];
  }
  return deste;
}

/** Gruplar bitiş için geçerli mi: hepsi seri/grup (≥3) ya da tam 7 çift. Geçerliyse tür. */
export function bitisTuru(gruplar: Tas[][], okey: Okey): 'per' | 'cift' | null {
  if (!gruplar.length) return null;
  const coz = gruplar.map((g) => perCoz(g, okey));
  if (coz.some((c) => !c)) return null;
  const cift = coz.filter((c) => c!.tur === 'cift').length;
  if (cift === coz.length) return cift === 7 ? 'cift' : null;
  return cift === 0 ? 'per' : null;
}

/** Taşların tamamını seri/gruplara ayırır (geri izleme); olmazsa null */
export function tamBol(taslar: Tas[], okey: Okey): Tas[][] | null {
  const ger = taslar.filter((t) => gercek(t, okey)).sort((a, b) => gercek(a, okey)!.s - gercek(b, okey)!.s || gercek(a, okey)!.r - gercek(b, okey)!.r);
  const jok = taslar.filter((t) => !gercek(t, okey));
  const git = (ger: Tas[], jok: Tas[]): Tas[][] | null => {
    if (!ger.length) return jok.length ? null : [];
    const a = ger[0];
    const ga = gercek(a, okey)!;
    const kalan = ger.slice(1);
    const aday: { g: Tas[]; j: number }[] = [];
    // grup: a + aynı sayının diğer renkleri (+ joker)
    const renk = new Map<number, Tas>();
    for (const t of kalan) { const g = gercek(t, okey)!; if (g.s === ga.s && g.r !== ga.r && !renk.has(g.r)) renk.set(g.r, t); }
    const diger = [...renk.values()];
    for (let m = 0; m < 1 << diger.length; m++) {
      const g = [a, ...diger.filter((_, b) => m & (1 << b))];
      for (let e = 0; e <= jok.length; e++) if (g.length + e >= 3 && g.length + e <= 4) aday.push({ g, j: e });
    }
    // seri: a en küçük gerçek taş; yukarı doğru gerçek taş ya da joker
    const zincir = (g: Tas[], v: number, j: number) => {
      if (g.length + j >= 3) aday.push({ g: g.slice(), j });
      if (v > 13) return;
      const t = kalan.find((x) => { const q = gercek(x, okey)!; return q.s === v && q.r === ga.r && !g.includes(x); });
      if (t) { g.push(t); zincir(g, v + 1, j); g.pop(); }
      if (j < jok.length) zincir(g, v + 1, j + 1);
    };
    zincir([a], ga.s + 1, 0);
    for (const c of aday) {
      const per = [...c.g, ...jok.slice(0, c.j)];
      if (!perCoz(per, okey) || perCoz(per, okey)!.tur === 'cift') continue;
      const sonra = git(kalan.filter((t) => !c.g.includes(t)), jok.slice(c.j));
      if (sonra) return [per, ...sonra];
    }
    return null;
  };
  return git(ger, jok);
}

/** 7 çift (joker eşin yerine geçer); olmazsa null */
export function yediCift(taslar: Tas[], okey: Okey): Tas[][] | null {
  if (taslar.length !== 14) return null;
  const hucre = new Map<string, Tas[]>();
  const jok: Tas[] = [];
  for (const t of taslar) {
    const g = gercek(t, okey);
    if (!g) { jok.push(t); continue; }
    const k = `${g.s}:${g.r}`;
    hucre.set(k, [...(hucre.get(k) ?? []), t]);
  }
  const out: Tas[][] = [];
  const tek: Tas[] = [];
  for (const l of hucre.values()) {
    for (let i = 0; i + 1 < l.length; i += 2) out.push([l[i], l[i + 1]]);
    if (l.length % 2) tek.push(l[l.length - 1]);
  }
  for (const t of tek) { const j = jok.shift(); if (!j) return null; out.push([t, j]); }
  if (jok.length === 2) out.push(jok.splice(0));
  return out.length === 7 && !jok.length ? out : null;
}

/** Bu 15 taştan bitiş: atılacak taş + gruplar (okey atarak bitmek öncelikli) */
export function bitisBul(el: Tas[], okey: Okey): { tas: number; gruplar: number[][] } | null {
  if (el.length !== EL_TAS + 1) return null;
  const sirali = [...el].sort((a, b) => Number(jokerMi(b, okey)) - Number(jokerMi(a, okey)));
  const denendi = new Set<string>();
  for (const t of sirali) {
    const anahtar = `${t.s}:${t.r}`;
    if (denendi.has(anahtar)) continue;
    denendi.add(anahtar);
    const kalan = el.filter((x) => x.id !== t.id);
    const b = yediCift(kalan, okey) ?? tamBol(kalan, okey); // çift ×2 öncelikli
    if (b) return { tas: t.id, gruplar: b.map((g) => g.map((x) => x.id)) };
  }
  return null;
}

/** Eldeki perlere giren taş sayısı (yandan alma kararı için) */
const kapsam = (el: Tas[], okey: Okey) => perAra(el, okey, { tavan: 8000 }).perler.reduce((a, p) => a + p.length, 0);

/** Yandan alınan taş elimi ilerletir mi: bitiş olur ya da perlere giren taş sayısı artar */
export function yandanAl(el: Tas[], tas: Tas | undefined, okey: Okey): boolean {
  if (!tas) return false;
  if (jokerMi(tas, okey)) return true;
  const yeni = [...el, tas];
  if (bitisBul(yeni, okey)) return true;
  return kapsam(yeni, okey) >= kapsam(el, okey) + 2;
}

function elBitir(d: DuzDurum, kazanan: number, carpan: number, aciklama: string, olaylar: Olay[]): void {
  const neden: ElSonuc['neden'] = kazanan >= 0 ? 'bitti' : 'deste';
  const satirlar: ElSatir[] = d.oyuncular.map((o, i) => {
    const cezaTop = o.cezalar.reduce((a, c) => a + c.puan, 0);
    const kayip = kazanan < 0 || i === kazanan ? 0 : DUZ_KAYIP * carpan;
    const parca = kazanan < 0 ? ['Deste bitti (berabere)'] : i === kazanan ? [`Bitirdi${aciklama ? ` (${aciklama})` : ''}`] : [`Kaybetti (−${kayip})`];
    if (o.cezalar.length) parca.push(`gösterge (${cezaTop})`.replace('-', '−'));
    return { id: o.id, puan: -kayip + cezaTop, kalan: o.el.length, kazandi: i === kazanan, cezalar: o.cezalar, aciklama: parca.join(' · ') };
  });
  d.sonuc = { neden, kazananlar: kazanan >= 0 ? [d.oyuncular[kazanan].id] : [], satirlar };
  olaylar.push({ t: 'elBitti', neden, kazananlar: d.sonuc.kazananlar });
}

export const duzMotor: Motor = {
  tur: 'duz' as Motor['tur'],
  min: 2,
  max: 4,

  elBaslat({ oyuncular, elNo, baslayan, rng }): DuzDurum {
    const n = oyuncular.length;
    if (n < 2 || n > 4) throw new Error('Düz Okey 2–4 oyuncuyla oynanır.');
    const deste = desteKur(rng);
    let gi = deste.length - 1;
    while (deste[gi].s === 0) gi--;
    const [gosterge] = deste.splice(gi, 1);
    const ilk = ((baslayan % n) + n) % n;
    const liste: DuzOyuncu[] = oyuncular.map((o, i) => ({ id: o.id, el: deste.splice(deste.length - (i === ilk ? EL_TAS + 1 : EL_TAS)), atiklar: [], cezalar: [], attiMi: false, gosterdi: false }));
    return { tur: 'duz', elNo, oyuncular: liste, sira: ilk, deste, gosterge, okey: okeyBul(gosterge), cekti: true, sonuc: null };
  },

  uygula(durum, oyuncu, hamle) {
    const d0 = durum as DuzDurum;
    if (d0.sonuc) return { hata: 'El bitti.' };
    const oi = d0.oyuncular.findIndex((o) => o.id === oyuncu);
    if (oi < 0) return { hata: 'Bu masada oyuncu değilsin.' };
    if (oi !== d0.sira) return { hata: 'Sıra sende değil.' };
    if (!hamle || typeof hamle !== 'object' || Array.isArray(hamle)) return { hata: 'Geçersiz hamle.' };
    const h = hamle as Record<string, unknown>;
    const d = structuredClone(d0);
    const o = d.oyuncular[oi];
    const n = d.oyuncular.length;
    const okey = d.okey;
    const olaylar: Olay[] = [];
    const bitti = () => ({ durum: d, olaylar });

    switch (h.t) {
      case 'goster': {
        if (o.attiMi) return { hata: 'Gösterge yalnız ilk turunda, taş atmadan önce gösterilir.' };
        if (o.gosterdi) return { hata: 'Göstergeyi zaten gösterdin.' };
        const tas = o.el.find((t) => t.s === d.gosterge.s && t.r === d.gosterge.r);
        if (!tas) return { hata: 'Elinde göstergenin aynısı yok.' };
        o.gosterdi = true;
        const kimler: string[] = [];
        for (const x of d.oyuncular) {
          if (x === o) continue;
          const ceza: Ceza = { tur: 'gosterge', puan: -1, aciklama: 'Gösterge gösterildi' };
          x.cezalar.push(ceza);
          kimler.push(x.id);
          olaylar.push({ t: 'ceza', o: x.id, ceza });
        }
        olaylar.push({ t: 'gosterdi', o: o.id, tas, kimler });
        return bitti();
      }

      case 'cek': {
        if (d.cekti) return { hata: 'Bu turda zaten taş çektin.' };
        const kaynak = h.kaynak ?? 'deste';
        if (kaynak === 'deste') {
          const tas = d.deste.pop();
          if (!tas) { elBitir(d, -1, 0, '', olaylar); return bitti(); }
          o.el.push(tas);
          d.cekti = true;
          d.yandan = null;
          d.yanSeri = 0;
          olaylar.push({ t: 'cekti', o: o.id, kaynak: 'deste' }, { t: 'cektim', kime: o.id, tas });
          return bitti();
        }
        if (kaynak !== 'atik') return { hata: 'Taş desteden ya da yandan (önceki oyuncunun attığı taş) çekilir.' };
        const tas = d.oyuncular[(oi - 1 + n) % n].atiklar.pop();
        if (!tas) return { hata: 'Yanında alınacak taş yok; desteden çek.' };
        o.el.push(tas);
        d.cekti = true;
        d.yandan = tas.id;
        d.yanSeri = (d.yanSeri ?? 0) + 1;
        olaylar.push({ t: 'cekti', o: o.id, kaynak: 'atik', tas });
        return bitti();
      }

      case 'at': {
        if (!d.cekti) return { hata: 'Önce taş çekmelisin.' };
        if (!tam(h.tas)) return { hata: 'Atılacak taşı seçmelisin.' };
        const tas = o.el.find((t) => t.id === h.tas);
        if (!tas) return { hata: 'Bu taş elinde değil.' };
        o.el = o.el.filter((t) => t.id !== tas.id);
        o.atiklar.push(tas);
        o.attiMi = true;
        olaylar.push({ t: 'atti', o: o.id, tas });
        if (!d.deste.length) { elBitir(d, -1, 0, '', olaylar); return bitti(); }
        d.sira = (oi + 1) % n;
        d.cekti = false;
        olaylar.push({ t: 'sira', o: d.oyuncular[d.sira].id });
        return bitti();
      }

      case 'bitir': {
        if (!d.cekti) return { hata: 'Önce taş çekmelisin.' };
        if (!tam(h.tas)) return { hata: 'Bitirmek için atacağın taşı seçmelisin.' };
        const tas = o.el.find((t) => t.id === h.tas);
        if (!tas) return { hata: 'Bu taş elinde değil.' };
        const gr = h.gruplar;
        if (!Array.isArray(gr) || !gr.every((g) => Array.isArray(g) && g.every(tam))) return { hata: 'Geçersiz hamle.' };
        const ids = (gr as number[][]).flat();
        const kalan = o.el.filter((t) => t.id !== tas.id);
        if (new Set(ids).size !== ids.length || ids.length !== kalan.length || ids.some((id) => !kalan.some((t) => t.id === id))) {
          return { hata: 'Bitirmek için atılan taş dışındaki 14 taşın hepsi gruplara girmeli.' };
        }
        const gruplar = (gr as number[][]).map((g) => g.map((id) => kalan.find((t) => t.id === id)!));
        const bt = bitisTuru(gruplar, okey);
        if (!bt) return { hata: 'Elin bitmiyor: her grup seri (aynı renk ardışık, 12-13-1 yok) ya da grup (aynı sayı farklı renk, 3–4 taş) olmalı, ya da tam 7 çift.' };
        o.el = kalan;
        o.atiklar.push(tas);
        const okeyle = jokerMi(tas, okey);
        const carpan = (okeyle ? 2 : 1) * (bt === 'cift' ? 2 : 1);
        const ac = [okeyle ? 'okey atarak' : '', bt === 'cift' ? 'çiftle' : ''].filter(Boolean).join(', ');
        d.bitis = gruplar.map((g, i) => { const c = perCoz(g, okey)!; return { id: i + 1, tur: c.tur, taslar: c.taslar, sahip: o.id }; });
        olaylar.push({ t: 'atti', o: o.id, tas }, { t: 'bitirdi', o: o.id, okeyle, cift: bt === 'cift' });
        elBitir(d, oi, carpan, ac, olaylar);
        return bitti();
      }

      default:
        return { hata: 'Bu oyunda böyle bir hamle yok.' };
    }
  },

  gorunum(durum, bakan): OkeyGorunum {
    const d = durum as DuzDurum;
    return {
      tur: 'duz' as OkeyGorunum['tur'],
      elNo: d.elNo,
      sira: d.oyuncular[d.sira].id,
      oyuncular: d.oyuncular.map((o) => ({ id: o.id, tasSayisi: o.el.length, acti: o.gosterdi, cezalar: o.cezalar.slice(), atiklar: o.atiklar.slice() })),
      elim: d.oyuncular.find((o) => o.id === bakan)?.el.slice() ?? [],
      perler: (d.bitis ?? []).map((p) => ({ ...p, taslar: p.taslar.slice() })),
      deste: d.deste.length,
      tur_: { cekti: d.cekti, hamleYapti: d.oyuncular[d.sira].attiMi },
      gosterge: d.gosterge,
      okey: d.okey,
      bitti: !!d.sonuc,
    };
  },

  botHamle(durum, bot) {
    const d = durum as DuzDurum;
    if (d.sonuc) return null;
    const o = d.oyuncular[d.sira];
    if (o.id !== bot) return null;
    const n = d.oyuncular.length;
    if (!o.attiMi && !o.gosterdi && o.el.some((t) => t.s === d.gosterge.s && t.r === d.gosterge.r)) return { t: 'goster' };
    if (!d.cekti) {
      const atik = d.oyuncular[(d.sira - 1 + n) % n].atiklar;
      const yanTas = atik[atik.length - 1];
      const al = (d.yanSeri ?? 0) < n * 2 && yandanAl(o.el, yanTas, d.okey);
      return { t: 'cek', kaynak: al || (!d.deste.length && yanTas) ? 'atik' : 'deste' };
    }
    const b = bitisBul(o.el, d.okey);
    if (b) return { t: 'bitir', ...b };
    // Yandan alınan taş geri atılmaz (yalnız tek seçenekse)
    const aday = o.el.filter((t) => t.id !== d.yandan);
    return { t: 'at', tas: atisSec(aday.length ? aday : o.el, [], d.okey, false, false) };
  },

  sonuc(durum) {
    return (durum as DuzDurum).sonuc;
  },
};

/** Görünümden göstergeyi gösterebilir miyim (ilk tur, aynısı elde) */
export function gosterebilir(g: OkeyGorunum, ben: string, gosterdi: boolean): boolean {
  if (!g.gosterge || g.sira !== ben || g.bitti || gosterdi || g.tur_.hamleYapti) return false;
  return g.elim.some((t) => t.s === g.gosterge!.s && t.r === g.gosterge!.r);
}
