/**
 * Uno — saf kural motoru (108 kart, 2–8 oyuncu). Resmî kurallar (klasik): üst üste ekleme yok, +4'e itiraz edilir, ilk açılan
 * kartın etkisi ilk oyuncuya uygulanır. Modlar (UNO_MODLAR): yigma (+2/+4 birikir), yediSifir (7 takas, 0 devir), cekCek.
 * Dengeli dağıtım: karma tamamen rastgeledir; yalnız bir ele dağıtımda 2'den çok joker/+4 (en çok 1 +4) ya da 3'ten çok aksiyon
 * kartı düşerse fazlası desteden rastgele bir sayı kartıyla değiştirilir; çekişte elinde 3 joker/+4 olan oyuncuya 4. gelirse
 * kart destedeki rastgele bir renkli kartla yer değiştirir (bir elin jokerle erken bitmesini önler).
 * Durum düz JSON; `uygula` girdiyi değiştirmez. Gizlilik: el yalnız `gorunum(bakan)` ve `kime`li olaylarla sahibine gider.
 */
import type { Ceza, ElSatir, ElSonuc, Motor, OdaAyar, Olay, Rng, UnoGorunum, UnoKart, UnoMod, UnoRenk } from '../tipler';
import { UNO_RENKLER, karma, kartDegeri, oynanabilirMi, sayiKartiMi, siraOnerisi } from './unoAsistan';

export interface UnoDurum {
  tur: 'uno';
  elNo: number;
  /** Oturma sırasıyla oyuncu kimlikleri */
  oyuncular: string[];
  /** Sırası olanın `oyuncular` dizini */
  kim: number;
  yon: 1 | -1;
  eller: Record<string, UnoKart[]>;
  /** Son eleman en üstte */
  deste: UnoKart[];
  /** Son eleman en üstte; joker/+4 burada da renksiz durur (seçilen renk `aktifRenk`) */
  atik: UnoKart[];
  aktifRenk: UnoRenk;
  cektiBuTur: boolean;
  cekilen: number | null;
  unoDedi: string[];
  yakalanabilir: string[];
  cezalar: Record<string, Ceza[]>;
  sonuc: ElSonuc | null;
  mod?: UnoMod;
  /** yigma: biriken çekme cezası */
  yigin?: number;
  /** +4 itirazı bekleniyor; haksiz: oynayanın elinde önceki aktif renkten kart vardı */
  dortBekle?: { oynayan: string; hedef: string; haksiz: boolean } | null;
  /** İlk kart joker: sıradaki oyuncu renk seçer */
  renkSec?: boolean;
}

const MODLAR: UnoMod[] = ['klasik', 'yigma', 'yediSifir', 'cekCek', 'atlama', 'hizli'];
/** Atlama modu: ortadaki kartın tıpkısı (renkli) sıra beklemeden atılabilir */
const tipki = (d: UnoDurum, k: UnoKart) => { const u = d.atik[d.atik.length - 1]; return d.mod === 'atlama' && k.renk !== null && k.renk === u.renk && k.deger === u.deger && !d.yigin && !d.dortBekle && !d.renkSec; };
const ELDE_EN_COK = { joker: 2, dort: 1, aksiyon: 3 };
const jokerMi = (k: UnoKart) => k.renk === null;
const aksiyonMu = (k: UnoKart) => k.renk !== null && !sayiKartiMi(k);

/** Dağıtım dengesi: sınırı aşan kart destedeki rastgele bir sayı kartıyla yer değiştirir (deste karışık kalır) */
function dengele(el: UnoKart[], deste: UnoKart[], rng: Rng): void {
  for (let guvenlik = 0; guvenlik < 20; guvenlik++) {
    const j = el.filter(jokerMi), d4 = el.filter((k) => k.deger === '+4'), ak = el.filter(aksiyonMu);
    const fazla = d4.length > ELDE_EN_COK.dort ? d4[0] : j.length > ELDE_EN_COK.joker ? j[0] : ak.length > ELDE_EN_COK.aksiyon ? ak[0] : null;
    if (!fazla) return;
    const adaylar = deste.map((k, i) => (sayiKartiMi(k) ? i : -1)).filter((i) => i >= 0);
    if (!adaylar.length) return;
    const di = adaylar[rs(rng, adaylar.length)];
    const ei = el.indexOf(fazla);
    [el[ei], deste[di]] = [deste[di], el[ei]];
  }
}

/** Oynanabilirlik (mod ve biriken ceza dahil) */
function uyar(d: UnoDurum, kart: UnoKart): boolean {
  const ust = d.atik[d.atik.length - 1];
  if (d.yigin) return kart.deger === '+4' || (kart.deger === '+2' && ust.deger === '+2');
  return oynanabilirMi(kart, ust, d.aktifRenk);
}

const EL = 7;
const UNO_CEZA = 2;

/** 108 kart, kimlik 0–107 (karılmamış) */
export function unoDeste(): UnoKart[] {
  const d: UnoKart[] = [];
  const ekle = (renk: UnoRenk | null, deger: UnoKart['deger']) => d.push({ id: d.length, renk, deger });
  for (const r of UNO_RENKLER) {
    ekle(r, '0');
    for (const v of ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'pas', 'yon', '+2'] as const) { ekle(r, v); ekle(r, v); }
  }
  for (let i = 0; i < 4; i++) ekle(null, 'joker');
  for (let i = 0; i < 4; i++) ekle(null, '+4');
  return d;
}

/** [0,n) tam sayı; bozuk rng'de 0 */
const rs = (rng: Rng, n: number): number => { const x = Math.floor(rng() * n); return x >= 0 && x < n ? x : 0; };

function kar<T>(a: T[], rng: Rng): T[] {
  for (let i = a.length - 1; i > 0; i--) { const j = rs(rng, i + 1); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}

const renkMi = (x: unknown): x is UnoRenk => typeof x === 'string' && (UNO_RENKLER as readonly string[]).includes(x);
const sonraki = (d: UnoDurum, adim = 1): number => { const n = d.oyuncular.length; return (((d.kim + d.yon * adim) % n) + n) % n; };

/** Deste biterse atık (üstteki hariç) karılıp deste olur; ikisi de boşsa çekilebildiği kadar çekilir. */
function cek(d: UnoDurum, kime: string, adet: number, neden: string, rng: Rng, olaylar: Olay[]): UnoKart[] {
  const kartlar: UnoKart[] = [];
  for (let i = 0; i < adet; i++) {
    if (!d.deste.length) {
      if (d.atik.length < 2) break;
      d.deste = kar(d.atik.splice(0, d.atik.length - 1), rng);
      olaylar.push({ t: 'karildi', deste: d.deste.length });
    }
    let k = d.deste.pop()!;
    if (jokerMi(k) && d.eller[kime].filter(jokerMi).length + kartlar.filter(jokerMi).length >= 3) {
      const adaylar = d.deste.map((x, i) => (x.renk !== null ? i : -1)).filter((i) => i >= 0);
      if (adaylar.length) { const di = adaylar[rs(rng, adaylar.length)]; [k, d.deste[di]] = [d.deste[di], k]; }
    }
    kartlar.push(k);
  }
  d.eller[kime].push(...kartlar);
  olaylar.push({ t: 'cekti', o: kime, adet: kartlar.length, neden });
  if (kartlar.length) olaylar.push({ t: 'cektim', kime, kartlar });
  return kartlar;
}

function elSonucu(d: UnoDurum, kazanan: string): ElSonuc {
  const deger = (id: string) => d.eller[id].reduce((t, k) => t + kartDegeri(k), 0);
  const toplam = d.oyuncular.reduce((t, id) => t + deger(id), 0);
  const satirlar: ElSatir[] = d.oyuncular.map((id) => {
    const kazandi = id === kazanan;
    const kalan = d.eller[id].length;
    const cezalar = d.cezalar[id] ?? [];
    const cz = cezalar.length ? ` · ${cezalar.length} UNO cezası` : '';
    return kazandi
      ? { id, puan: toplam, kalan, kazandi, cezalar, aciklama: `Eli bitirdi (+${toplam})${cz}` }
      : { id, puan: 0 - deger(id), kalan, kazandi, cezalar, aciklama: `${kalan} kart (−${deger(id)})${cz}` };
  });
  return { neden: 'bitti', kazananlar: [kazanan], satirlar };
}

function elBaslat(g: { oyuncular: { id: string }[]; elNo: number; baslayan: number; rng: Rng; ayar?: Partial<OdaAyar> }): UnoDurum {
  const oyuncular = g.oyuncular.map((o) => o.id);
  const n = oyuncular.length;
  if (n < 2 || n > 8 || new Set(oyuncular).size !== n) throw new Error('Uno 2–8 farklı oyuncuyla oynanır.');
  const deste = kar(unoDeste(), g.rng);
  const elKart = g.ayar?.unoMod === 'hizli' ? 5 : EL;
  const eller: Record<string, UnoKart[]> = {};
  const cezalar: Record<string, Ceza[]> = {};
  for (const id of oyuncular) { eller[id] = deste.splice(deste.length - elKart, elKart); cezalar[id] = []; dengele(eller[id], deste, g.rng); }
  // Resmî kural: ilk açılan kart +4 ise desteye geri konur, yeni kart açılır; diğer kartların etkisi ilk oyuncuya uygulanır
  let ilk = deste.pop()!;
  for (let i = 0; ilk.deger === '+4' && i < 200; i++) { deste.splice(rs(g.rng, deste.length), 0, ilk); ilk = deste.pop()!; }
  if (ilk.deger === '+4') { deste.push(ilk); ilk = deste.splice(deste.findIndex(sayiKartiMi), 1)[0]; } // bozuk rng güvencesi
  const b = Number.isInteger(g.baslayan) ? ((g.baslayan % n) + n) % n : 0;
  const mod = MODLAR.includes(g.ayar?.unoMod as UnoMod) ? (g.ayar!.unoMod as UnoMod) : 'klasik';
  const d: UnoDurum = {
    tur: 'uno', elNo: g.elNo, oyuncular, kim: b, yon: 1, eller, deste, atik: [ilk], aktifRenk: ilk.renk ?? 'k',
    cektiBuTur: false, cekilen: null, unoDedi: [], yakalanabilir: [], cezalar, sonuc: null, mod, yigin: 0, dortBekle: null, renkSec: ilk.renk === null,
  };
  if (ilk.deger === 'pas') d.kim = sonraki(d);
  else if (ilk.deger === 'yon') { d.yon = -1; d.kim = sonraki({ ...d, yon: -1 }); } // dağıtan (ilk oyuncunun solundaki) başlar, sıra ters döner; 2 kişide atlat
  else if (ilk.deger === '+2') { cek(d, oyuncular[b], 2, '+2', g.rng, []); d.kim = sonraki(d); }
  return d;
}

function uygula(durum: unknown, oyuncu: string, hamle: unknown, rng: Rng): { durum: unknown; olaylar: Olay[] } | { hata: string } {
  try {
    const d = structuredClone(durum) as UnoDurum;
    if (!d || d.tur !== 'uno' || !Array.isArray(d.oyuncular)) return { hata: 'Oyun durumu okunamadı.' };
    if (d.sonuc) return { hata: 'El bitti.' };
    if (typeof oyuncu !== 'string' || !d.oyuncular.includes(oyuncu)) return { hata: 'Bu oyunda değilsin.' };
    if (!hamle || typeof hamle !== 'object') return { hata: 'Geçersiz hamle.' };
    const h = hamle as { t?: unknown; kart?: unknown; renk?: unknown; uno?: unknown; hedef?: unknown };
    const olaylar: Olay[] = [];
    const siraBende = d.oyuncular[d.kim] === oyuncu;
    const el = d.eller[oyuncu];

    if ((d.renkSec || d.dortBekle) && siraBende && (h.t === 'oyna' || h.t === 'cek' || h.t === 'pas')) {
      return { hata: d.renkSec ? 'Önce rengi seç: ilk açılan kart joker.' : '+4 sana oynandı: kabul et ya da itiraz et.' };
    }

    if (h.t === 'renk') {
      if (!siraBende || !d.renkSec) return { hata: 'Şu an renk seçilmez.' };
      if (!renkMi(h.renk)) return { hata: 'Geçersiz renk.' };
      d.aktifRenk = h.renk; d.renkSec = false;
      olaylar.push({ t: 'renk', renk: h.renk, o: oyuncu });
    } else if (h.t === 'kabul' || h.t === 'itiraz') {
      const db = d.dortBekle;
      if (!db || db.hedef !== oyuncu || !siraBende) return { hata: 'İtiraz edilecek bir +4 yok.' };
      d.dortBekle = null;
      if (h.t === 'kabul') {
        cek(d, oyuncu, 4, '+4', rng, olaylar);
        d.kim = sonraki(d);
        olaylar.push({ t: 'sira', o: d.oyuncular[d.kim] });
      } else if (db.haksiz) {
        // İtiraz haklı: +4'ü kuralsız oynayan 4 çeker, itiraz eden normal oynar
        olaylar.push({ t: 'itiraz', o: oyuncu, hedef: db.oynayan, hakli: true });
        cek(d, db.oynayan, 4, 'itiraz', rng, olaylar);
      } else {
        olaylar.push({ t: 'itiraz', o: oyuncu, hedef: db.oynayan, hakli: false });
        cek(d, oyuncu, 6, 'itiraz', rng, olaylar);
        d.kim = sonraki(d);
        olaylar.push({ t: 'sira', o: d.oyuncular[d.kim] });
      }
    } else if (h.t === 'uno') {
      if (!d.yakalanabilir.includes(oyuncu)) return { hata: 'UNO diyecek durumda değilsin.' };
      d.yakalanabilir = d.yakalanabilir.filter((x) => x !== oyuncu);
      d.unoDedi.push(oyuncu);
      olaylar.push({ t: 'uno', o: oyuncu });
    } else if (h.t === 'yakala') {
      const hedef = h.hedef;
      if (typeof hedef !== 'string' || !d.oyuncular.includes(hedef)) return { hata: 'Yakalanacak oyuncu bulunamadı.' };
      if (hedef === oyuncu) return { hata: 'Kendini yakalayamazsın.' };
      if (!d.yakalanabilir.includes(hedef)) return { hata: 'Yakalanacak kimse yok.' };
      d.cezalar[hedef].push({ tur: 'uno', puan: 0, aciklama: 'UNO demedi' });
      olaylar.push({ t: 'yakalandi', o: hedef, yakalayan: oyuncu });
      cek(d, hedef, UNO_CEZA, 'yakalandi', rng, olaylar);
      d.yakalanabilir = d.yakalanabilir.filter((x) => x !== hedef); // deste boşsa kart gelmeyebilir; yine de bir kez yakalanır
    } else if (h.t === 'cek') {
      if (!siraBende) return { hata: 'Sıra sende değil.' };
      if (d.cektiBuTur) return { hata: 'Bu turda zaten çektin.' };
      d.yakalanabilir = [];
      if (d.yigin) {
        // Yığma: biriken cezayı çeken oyuncunun sırası geçer
        cek(d, oyuncu, d.yigin, 'yigin', rng, olaylar);
        d.yigin = 0;
        d.kim = sonraki(d);
        olaylar.push({ t: 'sira', o: d.oyuncular[d.kim] });
      } else {
        let kart = cek(d, oyuncu, 1, 'cek', rng, olaylar)[0];
        // Çek-çek: uyan kart gelene dek
        for (let i = 0; d.mod === 'cekCek' && kart && !uyar(d, kart) && i < 40; i++) kart = cek(d, oyuncu, 1, 'cek', rng, olaylar)[0];
        d.cektiBuTur = true;
        d.cekilen = kart ? kart.id : null;
      }
    } else if (h.t === 'pas') {
      if (!siraBende) return { hata: 'Sıra sende değil.' };
      if (!d.cektiBuTur) return { hata: 'Önce kart çekmelisin.' };
      olaylar.push({ t: 'pas', o: oyuncu });
      d.kim = sonraki(d);
      d.cektiBuTur = false; d.cekilen = null;
      olaylar.push({ t: 'sira', o: d.oyuncular[d.kim] });
    } else if (h.t === 'oyna') {
      const i = typeof h.kart === 'number' ? el.findIndex((k) => k.id === h.kart) : -1;
      if (!siraBende && !(i >= 0 && tipki(d, el[i]))) return { hata: d.mod === 'atlama' ? 'Sıra sende değil; sıra dışında yalnız ortadaki kartın tıpkısını atabilirsin.' : 'Sıra sende değil.' };
      if (i < 0) return { hata: 'Bu kart elinde yok.' };
      const kart = el[i];
      if (!siraBende) {
        // Atlama: sıra atlayan oyuncuya geçer, oynanan kartın etkisi ondan sayılır
        d.kim = d.oyuncular.indexOf(oyuncu);
        d.cektiBuTur = false; d.cekilen = null;
        olaylar.push({ t: 'atladi', o: oyuncu });
      }
      if (d.cektiBuTur && kart.id !== d.cekilen) return { hata: 'Çektikten sonra yalnız çektiğin kartı oynayabilirsin.' };
      if (!uyar(d, kart)) return { hata: d.yigin ? `Biriken ${d.yigin} kartın üstüne yalnız ${d.atik[d.atik.length - 1].deger === '+2' ? '+2 ya da +4' : '+4'} eklenir; ekleyemiyorsan çek.` : 'Bu kart şu an oynanamaz.' };
      const renk = kart.renk ?? h.renk;
      if (!renkMi(renk)) return { hata: 'Joker için renk seçmelisin.' };

      d.yakalanabilir = [];
      // +4 yalnız elinde aktif renkten kart yokken kurala uygundur (itirazda bakılır)
      const haksiz = kart.deger === '+4' && el.some((k) => k.id !== kart.id && k.renk === d.aktifRenk);
      el.splice(i, 1);
      d.atik.push(kart);
      d.aktifRenk = renk;
      olaylar.push(kart.renk === null ? { t: 'oynadi', o: oyuncu, kart, renk } : { t: 'oynadi', o: oyuncu, kart });
      if (kart.renk === null) olaylar.push({ t: 'renk', renk });
      if (el.length === 1) {
        if (h.uno === true) { d.unoDedi.push(oyuncu); olaylar.push({ t: 'uno', o: oyuncu }); }
        else d.yakalanabilir.push(oyuncu);
      }
      const bitti = el.length === 0;
      let adim = 1;
      if (kart.deger === 'yon') {
        d.yon = d.yon === 1 ? -1 : 1;
        olaylar.push({ t: 'yon', yon: d.yon });
        if (d.oyuncular.length === 2) { adim = 2; if (!bitti) olaylar.push({ t: 'atlandi', o: d.oyuncular[sonraki(d)] }); }
      } else if (kart.deger === 'pas') {
        adim = 2;
        if (!bitti) olaylar.push({ t: 'atlandi', o: d.oyuncular[sonraki(d)] });
      } else if (kart.deger === '+2' || kart.deger === '+4') {
        const adet = kart.deger === '+2' ? 2 : 4;
        if (d.mod === 'yigma' && !bitti) { d.yigin = (d.yigin || 0) + adet; olaylar.push({ t: 'yigin', adet: d.yigin }); }
        else if (kart.deger === '+4' && !bitti && d.mod !== 'yigma') {
          adim = 1; // sıradaki kabul ya da itiraz eder
          d.dortBekle = { oynayan: oyuncu, hedef: d.oyuncular[sonraki(d)], haksiz };
        } else {
          adim = 2; // son kart olsa da sıradaki çeker (puan için)
          cek(d, d.oyuncular[sonraki(d)], adet + (d.yigin || 0), kart.deger, rng, olaylar);
          d.yigin = 0;
        }
      } else if (d.mod === 'yediSifir' && !bitti && kart.deger === '7') {
        const rakip = [...d.oyuncular.keys()].filter((j) => j !== d.kim)
          .map((j) => ({ j, n: d.eller[d.oyuncular[j]].length, s: (((j - d.kim) * d.yon) % d.oyuncular.length + d.oyuncular.length) % d.oyuncular.length }))
          .sort((a, b) => a.n - b.n || a.s - b.s)[0];
        const hid = d.oyuncular[rakip.j];
        [d.eller[oyuncu], d.eller[hid]] = [d.eller[hid], d.eller[oyuncu]];
        olaylar.push({ t: 'takas', o: oyuncu, hedef: hid });
      } else if (d.mod === 'yediSifir' && !bitti && kart.deger === '0') {
        const n = d.oyuncular.length, eski = d.oyuncular.map((id) => d.eller[id]);
        d.oyuncular.forEach((id, j) => { d.eller[d.oyuncular[(((j + d.yon) % n) + n) % n]] = eski[j]; });
        olaylar.push({ t: 'devir', o: oyuncu, yon: d.yon });
      }
      d.cektiBuTur = false; d.cekilen = null;
      if (bitti) {
        d.sonuc = elSonucu(d, oyuncu);
        olaylar.push({ t: 'elBitti', kazanan: oyuncu });
      } else {
        d.kim = sonraki(d, adim);
        olaylar.push({ t: 'sira', o: d.oyuncular[d.kim] });
      }
    } else return { hata: 'Geçersiz hamle.' };

    // Kart sayısı 1'den farklı olunca UNO durumu sıfırlanır
    const tek = (id: string) => d.eller[id].length === 1;
    d.unoDedi = d.unoDedi.filter(tek);
    d.yakalanabilir = d.yakalanabilir.filter(tek);
    return { durum: d, olaylar };
  } catch {
    return { hata: 'Hamle işlenemedi.' };
  }
}

function gorunum(durum: unknown, bakan: string | null): UnoGorunum {
  const d = durum as UnoDurum;
  const sira = d.oyuncular[d.kim];
  const ust = d.atik[d.atik.length - 1];
  const elim = bakan !== null && d.oyuncular.includes(bakan) ? d.eller[bakan] : [];
  const siraBende = !d.sonuc && bakan === sira;
  const g: UnoGorunum = {
    tur: 'uno', elNo: d.elNo, sira, yon: d.yon,
    oyuncular: d.oyuncular.map((id) => ({ id, kartSayisi: d.eller[id].length, unoDedi: d.unoDedi.includes(id) })),
    elim: elim.map((k) => ({ ...k })),
    ust: { ...ust }, aktifRenk: d.aktifRenk, deste: d.deste.length, atikSayisi: d.atik.length,
    cektiBuTur: d.cektiBuTur,
    oynanabilir: siraBende && !d.renkSec && !d.dortBekle
      ? elim.filter((k) => (!d.cektiBuTur || k.id === d.cekilen) && uyar(d, k)).map((k) => k.id)
      : !d.sonuc && bakan !== null ? elim.filter((k) => tipki(d, k)).map((k) => k.id) : [],
    yakalanabilir: d.sonuc ? [] : [...d.yakalanabilir],
    bitti: !!d.sonuc,
    mod: d.mod ?? 'klasik',
    yigin: d.yigin || 0,
  };
  if (d.dortBekle) g.dortBekle = { oynayan: d.dortBekle.oynayan, hedef: d.dortBekle.hedef };
  if (d.renkSec) g.renkSec = true;
  if (siraBende && d.cekilen !== null) g.cekilen = d.cekilen;
  return g;
}

function botHamle(durum: unknown, bot: string, _rng: Rng): unknown | null {
  const d = durum as UnoDurum;
  if (d.sonuc || !d.oyuncular.includes(bot)) return null;
  if (d.yakalanabilir.includes(bot)) return { t: 'uno' }; // insandan devralınan el
  // Yakalama kararı belirlenimci: aynı durumda yeniden sorulunca değişmez (≈ %50)
  const hedef = d.yakalanabilir.find((h) => karma(`${bot}|${h}|${d.atik.length}`) < 0.5);
  if (hedef) return { t: 'yakala', hedef };
  // Atlama: sıra dışındaki bot tıpkı kartını (belirlenimci ≈ %60) hemen atar
  if (d.oyuncular[d.kim] !== bot) {
    const t = d.eller[bot].find((k) => tipki(d, k));
    if (t && karma(`${bot}|${d.atik.length}|atla`) < 0.6) return { t: 'oyna', kart: t.id, ...(d.eller[bot].length === 2 ? { uno: true } : {}) };
  }
  // +4 itirazı: bot, oynayanın elinde çok kart varsa (renk tutma olasılığı yüksek) itiraz eder
  if (d.dortBekle?.hedef === bot && d.oyuncular[d.kim] === bot) {
    const n = d.eller[d.dortBekle.oynayan].length;
    return { t: karma(`${bot}|${d.atik.length}|itiraz`) < Math.min(0.6, n / 12) ? 'itiraz' : 'kabul' };
  }
  return siraOnerisi(gorunum(d, bot), bot)?.hamle ?? null;
}

export const unoMotor: Motor = {
  tur: 'uno',
  min: 2,
  max: 8,
  elBaslat,
  uygula,
  gorunum,
  botHamle,
  sonuc: (durum) => (durum as UnoDurum).sonuc,
};
