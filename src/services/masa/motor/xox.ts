/**
 * XOX — saf kural motoru (2 oyuncu, 3×3 … 6×6). Kurallar (docs/TAHTA_OYUNLARI.md §3):
 *   - X başlar (her elde başlayan değişir, X hep başlayanındır). Sırayla boş kareye işaret konur.
 *   - Yatay, dikey ya da çapraz `XOX_HEDEF[boyut]` işaret yan yana gelen kazanır; tahta dolarsa berabere.
 * Bot: 3×3'te kusursuz (minimax), büyüklerde kazan → engelle → en iyi açık dizi.
 */
import { XOX_HEDEF, type ElSonuc, type Motor, type Olay, type XoxBoyut, type XoxGorunum } from '../tipler';

type Isaret = 'X' | 'O';
export interface XoxDurum {
  tur: 'xox';
  elNo: number;
  boyut: XoxBoyut;
  hedef: number;
  /** [X, O] */
  oyuncular: [string, string];
  tahta: ('' | Isaret)[];
  sira: Isaret;
  son: number | null;
  cizgi: number[] | null;
  sonuc: ElSonuc | null;
}

const BOYUTLAR: XoxBoyut[] = [3, 4, 5, 6];
const yollarOnbellek = new Map<string, number[][]>();

/** Tüm kazanma dizileri (hedef uzunlukta) */
export function yollar(n: number, h: number): number[][] {
  const a = `${n}:${h}`;
  if (yollarOnbellek.has(a)) return yollarOnbellek.get(a)!;
  const r: number[][] = [];
  for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
    for (const [dx, dy] of [[1, 0], [0, 1], [1, 1], [1, -1]]) {
      const ex = x + dx * (h - 1), ey = y + dy * (h - 1);
      if (ex < 0 || ex >= n || ey < 0 || ey >= n) continue;
      r.push(Array.from({ length: h }, (_, k) => (y + dy * k) * n + x + dx * k));
    }
  }
  yollarOnbellek.set(a, r);
  return r;
}

export function kazananYol(t: XoxDurum['tahta'], n: number, h: number): number[] | null {
  for (const yol of yollar(n, h)) { const v = t[yol[0]]; if (v && yol.every((i) => t[i] === v)) return yol; }
  return null;
}

const ad = (d: XoxDurum, i: Isaret) => d.oyuncular[i === 'X' ? 0 : 1];

function minimax(t: XoxDurum['tahta'], sira: Isaret, ben: Isaret, derinlik: number): number {
  const k = kazananYol(t, 3, 3);
  if (k) return t[k[0]] === ben ? 10 - derinlik : derinlik - 10;
  if (t.every((v) => v)) return 0;
  let en = sira === ben ? -Infinity : Infinity;
  for (let i = 0; i < 9; i++) {
    if (t[i]) continue;
    t[i] = sira;
    const p = minimax(t, sira === 'X' ? 'O' : 'X', ben, derinlik + 1);
    t[i] = '';
    en = sira === ben ? Math.max(en, p) : Math.min(en, p);
  }
  return en;
}

export function xoxBotSec(d: XoxDurum): number {
  const bos = d.tahta.map((v, i) => (v ? -1 : i)).filter((i) => i >= 0);
  const ben = d.sira, o: Isaret = ben === 'X' ? 'O' : 'X';
  if (d.boyut === 3) {
    let en = -Infinity, sec = bos[0];
    for (const i of bos) { const t = d.tahta.slice(); t[i] = ben; const p = minimax(t, o, ben, 1); if (p > en) { en = p; sec = i; } }
    return sec;
  }
  const dene = (isaret: Isaret) => bos.find((i) => { const t = d.tahta.slice(); t[i] = isaret; return !!kazananYol(t, d.boyut, d.hedef); });
  const kazan = dene(ben); if (kazan != null) return kazan;
  const engel = dene(o); if (engel != null) return engel;
  const ys = yollar(d.boyut, d.hedef), orta = (d.boyut - 1) / 2;
  let en = -Infinity, sec = bos[0];
  for (const i of bos) {
    let p = 0;
    for (const yol of ys) {
      if (!yol.includes(i)) continue;
      const benim = yol.filter((j) => d.tahta[j] === ben).length, onun = yol.filter((j) => d.tahta[j] === o).length;
      if (!onun) p += 1 + benim * benim * 3; // kendi açık dizim
      if (!benim) p += onun * onun * 2; // rakibin açık dizisini kes
    }
    p -= (Math.abs((i % d.boyut) - orta) + Math.abs(Math.floor(i / d.boyut) - orta)) * 0.1;
    if (p > en) { en = p; sec = i; }
  }
  return sec;
}

function sonuclandir(d: XoxDurum, kazanan: string | null, aciklama: string): ElSonuc {
  return {
    neden: kazanan ? 'bitti' : 'berabere', kazananlar: kazanan ? [kazanan] : [],
    satirlar: d.oyuncular.map((id) => ({ id, puan: id === kazanan ? 1 : 0, kalan: 0, kazandi: id === kazanan, cezalar: [], aciklama })),
  };
}

export const xoxMotor: Motor = {
  tur: 'xox', min: 2, max: 2,

  elBaslat({ oyuncular, elNo, baslayan, ayar }) {
    const boyut = BOYUTLAR.includes(ayar?.xoxBoyut as XoxBoyut) ? (ayar!.xoxBoyut as XoxBoyut) : 3;
    const d: XoxDurum = {
      tur: 'xox', elNo, boyut, hedef: XOX_HEDEF[boyut], oyuncular: [oyuncular[baslayan % 2].id, oyuncular[(baslayan + 1) % 2].id],
      tahta: Array(boyut * boyut).fill(''), sira: 'X', son: null, cizgi: null, sonuc: null,
    };
    return d;
  },

  uygula(durum, oyuncu, hamle) {
    const d = durum as XoxDurum, h = hamle as { t?: string; i?: number };
    if (d.sonuc) return { hata: 'El bitti.' };
    const isaret: Isaret | null = d.oyuncular[0] === oyuncu ? 'X' : d.oyuncular[1] === oyuncu ? 'O' : null;
    if (!isaret) return { hata: 'Bu masada oyuncu değilsin.' };
    if (h?.t === 'teslim') {
      const k = ad(d, isaret === 'X' ? 'O' : 'X');
      return { durum: { ...d, sonuc: sonuclandir(d, k, `${isaret} teslim oldu`) }, olaylar: [{ t: 'teslim', o: oyuncu }, { t: 'elBitti' }] };
    }
    if (isaret !== d.sira) return { hata: 'Sıra sende değil.' };
    if (h?.t !== 'koy') return { hata: 'Geçersiz hamle.' };
    const i = Number(h.i);
    if (!Number.isInteger(i) || i < 0 || i >= d.tahta.length) return { hata: 'Tahta dışı.' };
    if (d.tahta[i]) return { hata: 'Bu kare dolu.' };
    const tahta = d.tahta.slice();
    tahta[i] = isaret;
    const y: XoxDurum = { ...d, tahta, son: i, sira: isaret === 'X' ? 'O' : 'X' };
    const olaylar: Olay[] = [{ t: 'koydu', o: oyuncu, i, isaret }];
    const yol = kazananYol(tahta, d.boyut, d.hedef);
    if (yol) { y.cizgi = yol; y.sonuc = sonuclandir(d, oyuncu, `${isaret} ${d.hedef}'lü dizdi`); olaylar.push({ t: 'elBitti' }); }
    else if (tahta.every((v) => v)) { y.sonuc = sonuclandir(d, null, 'Tahta doldu, berabere'); olaylar.push({ t: 'elBitti' }); }
    else olaylar.push({ t: 'sira', o: ad(d, y.sira) });
    return { durum: y, olaylar };
  },

  gorunum(durum) {
    const d = durum as XoxDurum;
    const g: XoxGorunum = {
      tur: 'xox', elNo: d.elNo, boyut: d.boyut, hedef: d.hedef, tahta: d.tahta, sira: ad(d, d.sira),
      isaretler: { [d.oyuncular[0]]: 'X', [d.oyuncular[1]]: 'O' }, son: d.son, cizgi: d.cizgi, bitti: !!d.sonuc,
    };
    return g;
  },

  botHamle(durum, bot) {
    const d = durum as XoxDurum;
    if (d.sonuc || ad(d, d.sira) !== bot) return null;
    return { t: 'koy', i: xoxBotSec(d) };
  },

  sonuc(durum) { return (durum as XoxDurum).sonuc; },
};
