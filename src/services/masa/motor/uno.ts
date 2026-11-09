/**
 * Uno — saf kural motoru (108 kart, 2–8 oyuncu). Üst üste ekleme ve +4 itirazı YOK.
 * Durum düz JSON; `uygula` girdiyi değiştirmez. Gizlilik: el yalnız `gorunum(bakan)` ve `kime`li olaylarla sahibine gider.
 */
import type { Ceza, ElSatir, ElSonuc, Motor, Olay, Rng, UnoGorunum, UnoKart, UnoRenk } from '../tipler';
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
    kartlar.push(d.deste.pop()!);
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

function elBaslat(g: { oyuncular: { id: string }[]; elNo: number; baslayan: number; rng: Rng }): UnoDurum {
  const oyuncular = g.oyuncular.map((o) => o.id);
  const n = oyuncular.length;
  if (n < 2 || n > 8 || new Set(oyuncular).size !== n) throw new Error('Uno 2–8 farklı oyuncuyla oynanır.');
  const deste = kar(unoDeste(), g.rng);
  const eller: Record<string, UnoKart[]> = {};
  const cezalar: Record<string, Ceza[]> = {};
  for (const id of oyuncular) { eller[id] = deste.splice(deste.length - EL, EL); cezalar[id] = []; }
  // İlk açık kart sayı olana dek çevir; aksiyon/joker desteye rastgele yere döner (üst hariç)
  let ilk = deste.pop()!;
  for (let i = 0; !sayiKartiMi(ilk) && i < 200; i++) { deste.splice(rs(g.rng, deste.length), 0, ilk); ilk = deste.pop()!; }
  if (!sayiKartiMi(ilk)) { // bozuk rng güvencesi
    deste.push(ilk);
    ilk = deste.splice(deste.findIndex(sayiKartiMi), 1)[0];
  }
  const b = Number.isInteger(g.baslayan) ? ((g.baslayan % n) + n) % n : 0;
  return {
    tur: 'uno', elNo: g.elNo, oyuncular, kim: b, yon: 1, eller, deste, atik: [ilk], aktifRenk: ilk.renk!,
    cektiBuTur: false, cekilen: null, unoDedi: [], yakalanabilir: [], cezalar, sonuc: null,
  };
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

    if (h.t === 'uno') {
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
      const [kart] = cek(d, oyuncu, 1, 'cek', rng, olaylar);
      d.cektiBuTur = true;
      d.cekilen = kart ? kart.id : null;
    } else if (h.t === 'pas') {
      if (!siraBende) return { hata: 'Sıra sende değil.' };
      if (!d.cektiBuTur) return { hata: 'Önce kart çekmelisin.' };
      olaylar.push({ t: 'pas', o: oyuncu });
      d.kim = sonraki(d);
      d.cektiBuTur = false; d.cekilen = null;
      olaylar.push({ t: 'sira', o: d.oyuncular[d.kim] });
    } else if (h.t === 'oyna') {
      if (!siraBende) return { hata: 'Sıra sende değil.' };
      const i = typeof h.kart === 'number' ? el.findIndex((k) => k.id === h.kart) : -1;
      if (i < 0) return { hata: 'Bu kart elinde yok.' };
      const kart = el[i];
      if (d.cektiBuTur && kart.id !== d.cekilen) return { hata: 'Çektikten sonra yalnız çektiğin kartı oynayabilirsin.' };
      if (!oynanabilirMi(kart, d.atik[d.atik.length - 1], d.aktifRenk)) return { hata: 'Bu kart şu an oynanamaz.' };
      const renk = kart.renk ?? h.renk;
      if (!renkMi(renk)) return { hata: 'Joker için renk seçmelisin.' };

      d.yakalanabilir = [];
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
        adim = 2; // son kart olsa da sıradaki çeker (puan için)
        cek(d, d.oyuncular[sonraki(d)], kart.deger === '+2' ? 2 : 4, kart.deger, rng, olaylar);
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
    oynanabilir: siraBende
      ? elim.filter((k) => (!d.cektiBuTur || k.id === d.cekilen) && oynanabilirMi(k, ust, d.aktifRenk)).map((k) => k.id)
      : [],
    yakalanabilir: d.sonuc ? [] : [...d.yakalanabilir],
    bitti: !!d.sonuc,
  };
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
