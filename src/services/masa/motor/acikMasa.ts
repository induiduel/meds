/**
 * Açık masa okeyleri: Kastet ve Remi (tek motor, yapılandırma farkı). Saf: durum düz JSON, `uygula` girdiyi değiştirmez,
 * kural dışı her hamle `{ hata }`.
 *
 * Ortak: 106 taş (104 + 2 sahte okey), herkese 14 taş, taş atma yok. Sıra sende: ya masayı düzenlersin (elden taş koyarak; istediğin
 * kadar), ya taş çekersin. Taş çeken açamaz (çekince sıra geçer), açan çekemez (Pas ile sırayı geçirir). Masadaki taşlar herkesindir:
 * `duzenle` hamlesi masadaki seri/grup taşlarının TAMAMINI + elden seçilen taşları yeni per listesine dağıtır; her per geçerli olmalı.
 *
 * Kastet: gösterge + okey (joker), sahte okey okeyin sayı/rengini taşır. En çok 26 seri/grup alanı; 26 dolunca özdeş çiftler ayrı çift
 *         alanına açılır (yerinden oynamaz). Elde en çok 22 taş. Tüm taşlar yere inince el boşken Pas → el biter.
 * Remi:   gösterge yok, 2 sahte okey jokerdir. İlk açılış yalnız elden en az 30 sayı (açılıştan önce masaya dokunulmaz). El boşalınca biter.
 *
 * Taş kimliği: r*26 + (s-1)*2 + kopya (0–103); sahte okeyler 104–105 (s=0).
 */
import type { Ceza, ElSatir, ElSonuc, Motor, OkeyGorunum, Olay, Per, Renk, Rng, Tas } from '../tipler';
import { gercek, jokerMi, okeyBul, perAra, perCoz, type Okey } from './yuzbirAsistan';

export type AcikTur = 'kastet' | 'remi';

/** Açık masa hamleleri (tipler.ts OkeyHamle'ye eklenecek) */
export type AcikHamle =
  /** Masadaki seri/grup taşlarının tamamı + elden seçilenler yeni perlere; `ciftler` (yalnız Kastet, 26 alan doluyken) elden çiftler */
  | { t: 'duzenle'; perler: number[][]; ciftler?: number[][] }
  /** Desteden taş çek (sıra geçer) */
  | { t: 'cek' }
  /** Sırayı geçir (açtıysan, çekemiyorsan ya da Kastet'te elin boşsa: el biter) */
  | { t: 'pas' };

export interface AcikOyuncu {
  id: string;
  el: Tas[];
  /** Yere en az bir kez taş açtı (Remi: 30 ile açılış yaptı) */
  acti: boolean;
  cezalar: Ceza[];
}

export interface AcikDurum {
  tur: AcikTur;
  elNo: number;
  oyuncular: AcikOyuncu[];
  sira: number;
  /** Son eleman en üstte */
  deste: Tas[];
  /** Kastet: gösterge ve okey; Remi: yok */
  gosterge: Tas | null;
  okey: Okey | null;
  /** Seri / grup alanı */
  perler: Per[];
  /** Kastet çift alanı */
  ciftler: Per[];
  perNo: number;
  /** Sıradaki bu turda yere taş açtı (artık çekemez) */
  hamleYapti: boolean;
  /** Art arda, hiç taş açılmadan geçen pas sayısı (deste bitince herkes pas → el kazanansız) */
  pasSeri: number;
  sonuc: ElSonuc | null;
}

export const KASTET_ALAN = 26;
export const KASTET_EL_TAVAN = 22;
export const KASTET_BITEN = 50;
/** Kastet: elde kalan okey; sahte okey okeyin sayısıyla sayılır */
export const KASTET_OKEY_DEGER = 25;
export const REMI_ACILIS = 30;
export const REMI_JOKER_DEGER = 30;
const EL_TAS = 14;

/* ------------------------------------------------------------------ jokerli per çözümü ------------------------------------------------------------------ */

/** Remi'de sahte okeyler joker: perCoz'a "sanal okey" (s=14) olarak verilir, dönüşte geri çevrilir */
const SANAL: Okey = { s: 14, r: 0 };
const ice = (t: Tas, okey: Okey | null): Tas => (okey ? { id: t.id, s: t.s, r: t.r } : t.s === 0 ? { id: t.id, s: 14, r: 0 } : { id: t.id, s: t.s, r: t.r });
const disa = (t: Tas, okey: Okey | null): Tas => (okey || t.s !== 14 ? t : { ...t, s: 0, r: 0 });

/** Bu oyunda joker mi (Kastet: okey; Remi: sahte okey) */
export const acikJoker = (t: Tas, okey: Okey | null): boolean => (okey ? jokerMi(t, okey) : t.s === 0);

/** Taş kümesi geçerli seri/grup mu (≥3 taş, en az 2 gerçek taş; 12-13-1 yok). Geçerliyse dizilmiş taşlar (joker `yerine` dolu) + değer. */
export function acikPer(taslar: Tas[], okey: Okey | null): { tur: 'seri' | 'grup'; taslar: Tas[]; deger: number } | null {
  if (!Array.isArray(taslar) || taslar.length < 3) return null;
  const c = perCoz(taslar.map((t) => ice(t, okey)), okey ?? SANAL);
  if (!c || c.tur === 'cift') return null;
  return { tur: c.tur, taslar: c.taslar.map((t) => disa(t, okey)), deger: c.deger };
}

/** Kastet çifti: sayısı ve rengi özdeş iki taş (iki sahte okey de çifttir) */
export const ciftMi = (a?: Tas, b?: Tas): boolean => !!a && !!b && a.id !== b.id && a.s === b.s && a.r === b.r;

/** Elde kalan taşların ceza değeri */
export function kalanDeger(el: Tas[], okey: Okey | null): number {
  let top = 0;
  for (const t of el) {
    if (!okey) top += t.s === 0 ? REMI_JOKER_DEGER : t.s;
    else top += gercek(t, okey)?.s ?? KASTET_OKEY_DEGER;
  }
  return top;
}

/** Eldeki en yüksek toplamlı ayrık seri/grup kümesi (taş listeleri; Remi jokerleri doğru çevrilir) */
export function elPerleri(el: Tas[], okey: Okey | null): { perler: Tas[][]; toplam: number } {
  const harita = new Map(el.map((t) => [t.id, t]));
  const a = perAra(el.map((t) => ice(t, okey)), okey ?? SANAL, { tavan: 20000 });
  return { perler: a.perler.map((p) => p.map((t) => harita.get(t.id)!)), toplam: a.toplam };
}

/* ------------------------------------------------------------------ yardımcılar ------------------------------------------------------------------ */

const tam = (x: unknown): x is number => typeof x === 'number' && Number.isInteger(x);
const eksi = (n: number) => `−${n}`;

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

function elBitir(d: AcikDurum, kazanan: number, olaylar: Olay[]): void {
  const neden: ElSonuc['neden'] = kazanan >= 0 ? 'bitti' : 'deste';
  const kalanlar = d.oyuncular.map((o) => kalanDeger(o.el, d.okey));
  const digerTop = kalanlar.reduce((a, x, i) => (i === kazanan ? a : a + x), 0);
  const satirlar: ElSatir[] = d.oyuncular.map((o, i) => {
    const cezaTop = o.cezalar.reduce((a, c) => a + c.puan, 0);
    let puan: number;
    let aciklama: string;
    if (i === kazanan) {
      puan = d.tur === 'kastet' ? KASTET_BITEN : digerTop;
      aciklama = d.tur === 'kastet' ? `Bitirdi (+${KASTET_BITEN})` : `Bitirdi: rakiplerin kalanı (+${digerTop})`;
    } else {
      puan = -kalanlar[i];
      aciklama = `${o.el.length} taş (${eksi(kalanlar[i])})`;
    }
    return { id: o.id, puan: puan + cezaTop, kalan: o.el.length, kazandi: i === kazanan, cezalar: o.cezalar, aciklama };
  });
  d.sonuc = { neden, kazananlar: kazanan >= 0 ? [d.oyuncular[kazanan].id] : [], satirlar };
  olaylar.push({ t: 'elBitti', neden, kazananlar: d.sonuc.kazananlar });
}

function siraGec(d: AcikDurum, olaylar: Olay[]): void {
  d.sira = (d.sira + 1) % d.oyuncular.length;
  d.hamleYapti = false;
  olaylar.push({ t: 'sira', o: d.oyuncular[d.sira].id });
}

/** Sıradaki çekebilir mi (deste var, Kastet'te 22 taş tavanı) */
export function cekebilir(d: Pick<AcikDurum, 'tur' | 'deste' | 'hamleYapti'> & { el: Tas[] }): boolean {
  if (d.hamleYapti) return false;
  if (!d.deste.length) return false;
  return !(d.tur === 'kastet' && d.el.length >= KASTET_EL_TAVAN);
}

/* ------------------------------------------------------------------ düzenle doğrulaması ------------------------------------------------------------------ */

type DuzenSonuc = { perler: Per[]; ciftler: Per[]; elden: number[]; acilis: number } | { hata: string };

/** Hamleyi doğrular ve yeni masa alanlarını kurar (girdi değişmez) */
export function duzenCoz(d: AcikDurum, oi: number, perlerHam: unknown, ciftlerHam: unknown): DuzenSonuc {
  const o = d.oyuncular[oi];
  const okey = d.okey;
  if (!Array.isArray(perlerHam) || !perlerHam.every((x) => Array.isArray(x) && x.every(tam))) return { hata: 'Geçersiz hamle.' };
  const ciftGir = ciftlerHam === undefined ? [] : ciftlerHam;
  if (!Array.isArray(ciftGir) || !ciftGir.every((x) => Array.isArray(x) && x.every(tam))) return { hata: 'Geçersiz hamle.' };
  const gr = perlerHam as number[][];
  const cg = ciftGir as number[][];
  if (d.tur === 'remi' && cg.length) return { hata: 'Remi’de çift açılmaz.' };
  const masada = new Map(d.perler.flatMap((p) => p.taslar.map((t) => [t.id, t] as const)));
  const ciftMasa = new Set(d.ciftler.flatMap((p) => p.taslar.map((t) => t.id)));
  const elde = new Map(o.el.map((t) => [t.id, t]));
  const ids = [...gr.flat(), ...cg.flat()];
  if (new Set(ids).size !== ids.length) return { hata: 'Aynı taş iki yere konamaz.' };
  if (ids.some((id) => ciftMasa.has(id))) return { hata: 'Çift alanındaki taşların yeri değiştirilemez.' };
  if (ids.some((id) => !masada.has(id) && !elde.has(id))) return { hata: 'Seçtiğin taşlardan biri ne masada ne elinde.' };
  if (cg.flat().some((id) => masada.has(id))) return { hata: 'Çift alanına yalnız elindeki taşlar açılır.' };
  const kullanilan = new Set(ids);
  if ([...masada.keys()].some((id) => !kullanilan.has(id))) return { hata: 'Masadaki taşlar ele geri alınamaz; her taş bir perde kalmalı.' };
  const elden = ids.filter((id) => elde.has(id));
  if (!elden.length) return { hata: 'Elinden en az bir taş koymalısın.' };

  // Remi açılış: masa olduğu gibi kalır, yeni perler yalnız elden ve toplamı ≥ 30
  let acilis = 0;
  if (d.tur === 'remi' && !o.acti) {
    const eskiler = new Map(d.perler.map((p) => [p.taslar.map((t) => t.id).sort((a, b) => a - b).join(','), p]));
    for (const g of gr) {
      const anahtar = g.slice().sort((a, b) => a - b).join(',');
      if (eskiler.has(anahtar)) { eskiler.delete(anahtar); continue; }
      if (g.some((id) => masada.has(id))) return { hata: `Açılıştan önce masadaki taşlara dokunamazsın; önce elinden en az ${REMI_ACILIS} sayı aç.` };
      const c = acikPer(g.map((id) => elde.get(id)!), okey);
      if (!c) return { hata: `${g.map((id) => elde.get(id)!.s || '★').join('-')} geçerli bir per değil.` };
      acilis += c.deger;
    }
    if (eskiler.size) return { hata: 'Açılıştan önce masadaki perler değiştirilemez.' };
    if (acilis < REMI_ACILIS) return { hata: `İlk açılış için elinden açtığın perlerin toplamı en az ${REMI_ACILIS} olmalı (şu an ${acilis}).` };
  }

  const yeni: Per[] = [];
  const korunan = new Set<number>();
  for (const g of gr) {
    const taslar = g.map((id) => masada.get(id) ?? elde.get(id)!);
    const c = acikPer(taslar, okey);
    if (!c) return { hata: `${taslar.map((t) => t.s || '★').join('-')} geçerli bir per değil: aynı renk ardışık (12-13-1 olmaz) ya da aynı sayı farklı renk, en az 3 taş; perde en az 2 gerçek taş.` };
    // Taşlarının çoğu aynı kalan per kimliğini ve sahibini korur
    const eski = d.perler.filter((p) => !korunan.has(p.id)).map((p) => ({ p, ortak: p.taslar.filter((t) => g.includes(t.id)).length })).sort((x, y) => y.ortak - x.ortak)[0];
    const koru = eski && eski.ortak > 0 ? eski.p : null;
    if (koru) korunan.add(koru.id);
    yeni.push({ id: koru ? koru.id : -1, tur: c.tur, taslar: c.taslar, sahip: koru ? koru.sahip : o.id });
  }
  if (d.tur === 'kastet' && yeni.length > KASTET_ALAN) return { hata: `Masada en çok ${KASTET_ALAN} seri alanı var.` };
  const ciftler: Per[] = d.ciftler.map((p) => ({ ...p, taslar: p.taslar.slice() }));
  if (cg.length) {
    if (yeni.length < KASTET_ALAN) return { hata: `Çift ancak ${KASTET_ALAN} seri alanının hepsi dolunca açılır (şu an ${yeni.length}).` };
    for (const c of cg) {
      const [a, b] = c.map((id) => elde.get(id));
      if (c.length !== 2 || !ciftMi(a, b)) return { hata: 'Çift, sayısı ve rengi özdeş iki taştır.' };
      ciftler.push({ id: -1, tur: 'cift', taslar: [a!, b!], sahip: o.id });
    }
  }
  let no = d.perNo;
  for (const p of [...yeni, ...ciftler]) if (p.id < 0) p.id = no++;
  return { perler: yeni, ciftler, elden, acilis };
}

/* ------------------------------------------------------------------ bot ------------------------------------------------------------------ */

/** Botun bu durumdaki tek düzenleme hamlesi (yoksa null): açılış / elden per / işleme / masadan taş alarak per */
export function botDuzen(d: AcikDurum, oi: number): AcikHamle | null {
  const o = d.oyuncular[oi];
  const okey = d.okey;
  const masaIds = d.perler.map((p) => p.taslar.map((t) => t.id));
  const dene = (h: AcikHamle): AcikHamle | null => {
    const r = duzenCoz(d, oi, h.t === 'duzenle' ? h.perler : [], h.t === 'duzenle' ? h.ciftler : undefined);
    return 'hata' in r ? null : h;
  };
  const alanVar = d.tur !== 'kastet' || d.perler.length < KASTET_ALAN;

  if (d.tur === 'remi' && !o.acti) {
    const a = elPerleri(o.el, okey);
    if (a.toplam < REMI_ACILIS || !a.perler.length) return null;
    return dene({ t: 'duzenle', perler: [...masaIds, ...a.perler.map((p) => p.map((t) => t.id))] });
  }
  // 1) Elden yeni per(ler)
  if (alanVar) {
    const a = elPerleri(o.el, okey);
    const yer = d.tur === 'kastet' ? KASTET_ALAN - d.perler.length : 99;
    if (a.perler.length) {
      const h = dene({ t: 'duzenle', perler: [...masaIds, ...a.perler.slice(0, yer).map((p) => p.map((t) => t.id))] });
      if (h) return h;
    }
  }
  // 2) Tek taş işleme (ucuna / gruba)
  for (const t of o.el) {
    for (let k = 0; k < d.perler.length; k++) {
      if (!acikPer([...d.perler[k].taslar, t], okey)) continue;
      const perler = masaIds.map((ids, i) => (i === k ? [...ids, t.id] : ids));
      const h = dene({ t: 'duzenle', perler });
      if (h) return h;
    }
  }
  // 3) Seriyi bölerek işleme: elde serinin iç sayısının kopyası
  for (const t of o.el) {
    for (let k = 0; k < d.perler.length && alanVar; k++) {
      const p = d.perler[k];
      if (p.tur !== 'seri') continue;
      for (let x = 2; x <= p.taslar.length - 3; x++) {
        const alt = [...p.taslar.slice(0, x), t];
        const ust = p.taslar.slice(x);
        if (!acikPer(alt, okey) || !acikPer(ust, okey)) continue;
        const perler = masaIds.map((ids, i) => (i === k ? alt.map((q) => q.id) : ids));
        perler.push(ust.map((q) => q.id));
        const h = dene({ t: 'duzenle', perler });
        if (h) return h;
      }
    }
  }
  // 4) Masadan serbest taş (uzun serinin ucu / dörtlü grubun bir taşı) + elden iki taş = yeni per
  if (alanVar && o.el.length >= 2) {
    const serbest: { k: number; tas: Tas; kalan: Tas[] }[] = [];
    d.perler.forEach((p, k) => {
      if (p.taslar.length < 4) return;
      const adaylar = p.tur === 'seri' ? [0, p.taslar.length - 1] : p.taslar.map((_, i) => i);
      for (const i of adaylar) {
        const kalan = p.taslar.filter((_, j) => j !== i);
        if (acikPer(kalan, okey)) serbest.push({ k, tas: p.taslar[i], kalan });
      }
    });
    for (const s of serbest) {
      for (let i = 0; i < o.el.length; i++) for (let j = i + 1; j < o.el.length; j++) {
        if (!acikPer([s.tas, o.el[i], o.el[j]], okey)) continue;
        const perler = masaIds.map((ids, q) => (q === s.k ? s.kalan.map((t) => t.id) : ids));
        perler.push([s.tas.id, o.el[i].id, o.el[j].id]);
        const h = dene({ t: 'duzenle', perler });
        if (h) return h;
      }
    }
  }
  // 5) Kastet: alanlar dolu, çiftler
  if (d.tur === 'kastet' && d.perler.length >= KASTET_ALAN) {
    const ciftler: number[][] = [];
    const kul = new Set<number>();
    for (const a of o.el) {
      if (kul.has(a.id)) continue;
      const b = o.el.find((x) => !kul.has(x.id) && ciftMi(a, x));
      if (b) { kul.add(a.id); kul.add(b.id); ciftler.push([a.id, b.id]); }
    }
    if (ciftler.length) return dene({ t: 'duzenle', perler: masaIds, ciftler });
  }
  return null;
}

/* ------------------------------------------------------------------ motor ------------------------------------------------------------------ */

function motorKur(tur: AcikTur): Motor {
  const ad = tur === 'kastet' ? 'Kastet' : 'Remi';
  const motor: Motor = {
    tur: tur as Motor['tur'],
    min: 2,
    max: 4,

    elBaslat({ oyuncular, elNo, baslayan, rng }): AcikDurum {
      const n = oyuncular.length;
      if (n < 2 || n > 4) throw new Error(`${ad} 2–4 oyuncuyla oynanır.`);
      const deste = desteKur(rng);
      let gosterge: Tas | null = null;
      if (tur === 'kastet') {
        let gi = deste.length - 1;
        while (deste[gi].s === 0) gi--;
        [gosterge] = deste.splice(gi, 1);
      }
      const liste: AcikOyuncu[] = oyuncular.map((o) => ({ id: o.id, el: deste.splice(deste.length - EL_TAS), acti: false, cezalar: [] }));
      return {
        tur, elNo, oyuncular: liste, sira: ((baslayan % n) + n) % n, deste, gosterge, okey: gosterge ? okeyBul(gosterge) : null,
        perler: [], ciftler: [], perNo: 1, hamleYapti: false, pasSeri: 0, sonuc: null,
      };
    },

    uygula(durum, oyuncu, hamle) {
      const d0 = durum as AcikDurum;
      if (d0.sonuc) return { hata: 'El bitti.' };
      const oi = d0.oyuncular.findIndex((o) => o.id === oyuncu);
      if (oi < 0) return { hata: 'Bu masada oyuncu değilsin.' };
      if (oi !== d0.sira) return { hata: 'Sıra sende değil.' };
      if (!hamle || typeof hamle !== 'object' || Array.isArray(hamle)) return { hata: 'Geçersiz hamle.' };
      const h = hamle as Record<string, unknown>;
      const d = structuredClone(d0);
      const o = d.oyuncular[oi];
      const olaylar: Olay[] = [];
      const bitti = () => ({ durum: d, olaylar });

      switch (h.t) {
        case 'duzenle': {
          const r = duzenCoz(d, oi, h.perler, h.ciftler);
          if ('hata' in r) return { hata: r.hata };
          const elden = new Set(r.elden);
          const eskiCift = new Set(d.ciftler.map((p) => p.id));
          o.el = o.el.filter((t) => !elden.has(t.id));
          d.perler = r.perler;
          d.ciftler = r.ciftler;
          d.perNo = Math.max(d.perNo, ...r.perler.map((p) => p.id + 1), ...r.ciftler.map((p) => p.id + 1));
          const ilk = !o.acti;
          o.acti = true;
          d.hamleYapti = true;
          d.pasSeri = 0;
          olaylar.push({ t: 'duzenledi', o: o.id, adet: elden.size, ...(ilk && tur === 'remi' ? { acilis: r.acilis } : null) });
          const yeniCift = r.ciftler.filter((p) => !eskiCift.has(p.id));
          if (yeniCift.length) olaylar.push({ t: 'acti', o: o.id, perler: yeniCift });
          if (tur === 'remi' && !o.el.length) elBitir(d, oi, olaylar);
          return bitti();
        }

        case 'cek': {
          if (d.hamleYapti) return { hata: 'Bu turda yere taş açtın; taş çekemezsin. Pas ile sırayı geçir.' };
          if (!d.deste.length) return { hata: 'Deste bitti; pas geçmelisin.' };
          if (tur === 'kastet' && o.el.length >= KASTET_EL_TAVAN) return { hata: `Elinde ${KASTET_EL_TAVAN} taş var; daha fazla çekemezsin. Aç ya da pas geç.` };
          const tas = d.deste.pop()!;
          o.el.push(tas);
          d.pasSeri = 0;
          olaylar.push({ t: 'cekti', o: o.id, kaynak: 'deste' }, { t: 'cektim', kime: o.id, tas });
          siraGec(d, olaylar);
          return bitti();
        }

        case 'pas': {
          if (tur === 'kastet' && !o.el.length) { elBitir(d, oi, olaylar); return bitti(); }
          if (!d.hamleYapti && cekebilir({ tur, deste: d.deste, hamleYapti: false, el: o.el })) {
            return { hata: tur === 'remi' && !o.acti ? `Açamıyorsan taş çekmelisin (açılış en az ${REMI_ACILIS}).` : 'Yere taş açmadan pas geçemezsin: aç ya da taş çek.' };
          }
          if (!d.hamleYapti) d.pasSeri++;
          olaylar.push({ t: 'pas', o: o.id });
          if (!d.hamleYapti && d.pasSeri >= d.oyuncular.length) { elBitir(d, -1, olaylar); return bitti(); }
          siraGec(d, olaylar);
          return bitti();
        }

        default:
          return { hata: 'Bu oyunda böyle bir hamle yok.' };
      }
    },

    gorunum(durum, bakan): OkeyGorunum {
      const d = durum as AcikDurum;
      return {
        tur: tur as OkeyGorunum['tur'],
        elNo: d.elNo,
        sira: d.oyuncular[d.sira].id,
        oyuncular: d.oyuncular.map((o) => ({ id: o.id, tasSayisi: o.el.length, acti: o.acti, cezalar: o.cezalar.slice() })),
        elim: d.oyuncular.find((o) => o.id === bakan)?.el.slice() ?? [],
        perler: [...d.perler, ...d.ciftler].map((p) => ({ ...p, taslar: p.taslar.slice() })),
        deste: d.deste.length,
        tur_: { cekti: false, hamleYapti: d.hamleYapti },
        ...(d.gosterge && d.okey ? { gosterge: d.gosterge, okey: d.okey } : null),
        bitti: !!d.sonuc,
      };
    },

    botHamle(durum, bot) {
      const d = durum as AcikDurum;
      if (d.sonuc) return null;
      const oi = d.sira;
      const o = d.oyuncular[oi];
      if (o.id !== bot) return null;
      if (tur === 'kastet' && !o.el.length) return { t: 'pas' };
      let h: AcikHamle | null = null;
      try { h = botDuzen(d, oi); } catch { h = null; }
      if (h && !('hata' in motor.uygula(d, bot, h, Math.random))) return h;
      if (!d.hamleYapti && cekebilir({ tur, deste: d.deste, hamleYapti: false, el: o.el })) return { t: 'cek' };
      return { t: 'pas' };
    },

    sonuc(durum) {
      return (durum as AcikDurum).sonuc;
    },
  };
  return motor;
}

export const kastetMotor: Motor = motorKur('kastet');
export const remiMotor: Motor = motorKur('remi');

/* ------------------------------------------------------------------ istemci yardımcıları ------------------------------------------------------------------ */

/** Görünümden: bakanın şu an yapabileceği bir düzenleme önerisi (asistan / ipucu). Durum yalnız görünür bilgiden kurulur. */
export function acikOneri(g: OkeyGorunum, ben: string): { hamle: AcikHamle; taslar: number[]; aciklama: string } | null {
  if ((g.tur as string) !== 'kastet' && (g.tur as string) !== 'remi') return null;
  if (g.bitti || g.sira !== ben) return null;
  const oi = g.oyuncular.findIndex((o) => o.id === ben);
  if (oi < 0) return null;
  const d: AcikDurum = {
    tur: g.tur as unknown as AcikTur, elNo: g.elNo, sira: oi, deste: [], gosterge: g.gosterge ?? null, okey: g.okey ?? null,
    oyuncular: g.oyuncular.map((o) => ({ id: o.id, el: o.id === ben ? g.elim : [], acti: o.acti, cezalar: [] })),
    perler: g.perler.filter((p) => p.tur !== 'cift'), ciftler: g.perler.filter((p) => p.tur === 'cift'),
    perNo: g.perler.reduce((m, p) => Math.max(m, p.id + 1), 1), hamleYapti: g.tur_.hamleYapti, pasSeri: 0, sonuc: null,
  };
  const h = botDuzen(d, oi);
  if (!h || h.t !== 'duzenle') return null;
  const elIds = new Set(g.elim.map((t) => t.id));
  const taslar = [...h.perler.flat(), ...(h.ciftler ?? []).flat()].filter((id) => elIds.has(id));
  const acilis = (g.tur as string) === 'remi' && !g.oyuncular[oi].acti;
  return { hamle: h, taslar, aciklama: h.ciftler?.length ? 'Çift alanına çift açabilirsin.' : acilis ? `${REMI_ACILIS} ve üstüyle açabilirsin.` : 'Elindeki taşları masaya koyabilirsin.' };
}
