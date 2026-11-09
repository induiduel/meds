/** Uno masası yerleşimi: kabın boyutundan tüm konumlar (px, kap köşesine göre). Uçuş animasyonları da bu noktaları kullanır. */

export interface Nokta { x: number; y: number }
export interface KartYer extends Nokta { a: number; z: number }

export interface Yerlesim {
  W: number; H: number;
  yatay: boolean;
  bosluk: number;
  /** El kartı genişliği / yüksekliği */
  kw: number; kh: number;
  /** Orta (atık, deste) kart genişliği */
  pk: number;
  /** Rakip koltuğu ölçeği ve kapalı mini kart genişliği */
  olcek: number; mk: number;
  /** Yelpazesiz küçük koltuk (dar ekranda kalabalık masa) */
  kucukKoltuk: boolean;
  atik: Nokta; deste: Nokta;
  halka: number;
  /** El alanının üst sınırı (y) ve eylem düğmeleri */
  elUst: number;
  yanGen: number;
  eylemAlt: number;
  renkEtiketi: boolean;
  koltuk: Record<string, Nokta>;
  /** El dizilişi: satır sayısı, adım */
  satir: number; adim: number; elGen: number;
}

const sik = (v: number, a: number, b: number) => Math.max(a, Math.min(b, v));

/** Elin sığması: önce sıkışır, sonra iki sıra, en son kademeli küçülür (hiç taşmaz) */
function elSigdir(n: number, gen: number, kw0: number, ikiSira: boolean) {
  const adimBul = (adet: number, kw: number) => (adet <= 1 ? 0 : Math.min(kw * 0.66, (gen - kw * 1.34) / (adet - 1)));
  let kw = kw0;
  let satir = 1;
  if (ikiSira && n > 3 && adimBul(n, kw) < kw * 0.36) satir = 2;
  const sirada = Math.ceil(n / satir);
  while (kw > kw0 * 0.6 && adimBul(sirada, kw) < kw * 0.3) kw -= 1;
  return { kw, satir, adim: Math.max(2, adimBul(sirada, kw)) };
}

export function yerlesimHesapla(W: number, H: number, rakipler: string[], elAdet: number): Yerlesim {
  const kisa = Math.min(W, H);
  const yatay = W >= H * 1.15;
  const bosluk = sik(kisa * 0.02, 8, 18);
  const yanGen = yatay ? sik(W * 0.125, 92, 150) : 0;
  const eylemAlt = yatay ? 0 : 54;
  const elGen = Math.max(120, W - 2 * yanGen - 2 * bosluk);
  const sig = elSigdir(elAdet, elGen, sik(Math.min(W * (yatay ? 0.17 : 0.21), H * (H < 420 ? 0.175 : 0.2)), 50, 112), H >= 560);
  const kw = sig.kw, kh = kw * 1.5;
  const elYuk = bosluk + kw * 0.12 + kh * (sig.satir === 2 ? 1.52 : 1) + kw * 0.34;
  const elUst = H - elYuk - eylemAlt;

  const m = rakipler.length;
  const cx = W / 2, cy = elUst / 2;
  // Yay: az oyuncuda yalnız üst, çok oyuncuda yanlara iner. Koltuklar yay uzunluğuna eşit aralıkla dizilir.
  const tasma = m <= 3 ? -32 : !yatay ? 16 : m === 4 ? -12 : 6;
  const a0 = (180 + tasma) * (Math.PI / 180), a1 = -tasma * (Math.PI / 180);
  const yay = (olcek: number) => {
    // Çok küçülünce yelpaze çizilmez: yalnız avatar + kart sayısı + ad
    const kucuk = olcek < 0.6;
    const mk = kucuk ? 0 : Math.round(30 * olcek);
    const sw = kucuk ? 64 : 116 * olcek;
    // Koltuğun gerçek yüksekliği: yelpaze + avatar + ad (alt sınırlar dahil) + sayı rozeti payı
    const sh = kucuk ? 54 : mk * 1.5 + Math.max(26, 38 * olcek) - 13 * olcek + Math.max(11, 12.5 * olcek) * 1.25 + 4 + 14;
    const rx = Math.max(10, W / 2 - sw / 2 - bosluk * 0.6);
    const ry = Math.max(10, elUst / 2 - sh / 2 - bosluk * 0.5);
    const N = 240;
    const pts: Nokta[] = [];
    const uz: number[] = [0];
    for (let i = 0; i <= N; i++) {
      const t = a0 + ((a1 - a0) * i) / N;
      pts.push({ x: cx + rx * Math.cos(t), y: cy - ry * Math.sin(t) });
      if (i) uz.push(uz[i - 1] + Math.hypot(pts[i].x - pts[i - 1].x, pts[i].y - pts[i - 1].y));
    }
    const koltuk: Record<string, Nokta> = {};
    rakipler.forEach((id, i) => {
      const hedef = (uz[N] * (i + 0.5)) / m;
      let j = 0;
      while (j < N && uz[j] < hedef) j++;
      koltuk[id] = { x: Math.round(pts[j].x), y: Math.round(pts[j].y) };
    });
    return { olcek, mk, sw, sh, koltuk, aralik: m ? uz[N] / m : Infinity };
  };
  // Yay dar gelirse (küçük telefon + kalabalık masa) koltuklar küçülür
  let ky = yay(sik(kisa / 720, 0.62, 1.12));
  if (ky.aralik < ky.sw * 0.94) ky = yay(Math.max(0.46, (ky.olcek * ky.aralik) / (ky.sw * 0.94)));
  const { olcek, mk, sw, sh, koltuk } = ky;

  // Orta: el ile (üstünde koltuk varsa) koltukların altı arasındaki boşluk. Önce koltuksuz dene; ortaya koltuk düşüyorsa altına in.
  const icGen = m >= 4 ? W - 2 * sw - 2 * bosluk : W - 2 * bosluk;
  const ortaKur = (ust: number) => {
    const yuk = Math.max(60, elUst - ust);
    const pk = Math.round(sik(Math.min(yuk / 2.5, icGen / 3.7, 104), 30, 104));
    const oy = ust + yuk / 2 - (yuk > pk * 3.6 ? pk * 0.1 : 0);
    return { pk, oy, sol: cx - pk * 1.8, sag: cx + pk * 1.8, ustY: oy - pk * 1.22 };
  };
  let o = ortaKur(bosluk);
  // Yalnız üstteki koltuklar ortayı aşağı iter; yandakiler iç genişlikle zaten ayrıktır
  const ustte = Object.values(koltuk).filter((k) => k.y < elUst * 0.45 && k.x + sw / 2 > o.sol && k.x - sw / 2 < o.sag && k.y + sh / 2 > o.ustY - 4);
  if (ustte.length) o = ortaKur(Math.max(...ustte.map((k) => k.y + sh / 2)) + 2);
  const { pk, oy } = o;
  const atik = { x: cx + pk * 0.58, y: oy };
  const deste = { x: cx - pk * 1.24, y: oy };
  const halka = pk * 2.36;
  return {
    W, H, yatay, bosluk, kw, kh, pk, olcek, mk, kucukKoltuk: mk === 0, atik, deste, halka, elUst, yanGen, eylemAlt,
    renkEtiketi: elUst - (oy + halka / 2) > 30,
    koltuk, satir: sig.satir, adim: sig.adim, elGen,
  };
}

/** El kartlarının konumu (kart merkezi). İki sırada ilk yarı arkada (üstte). */
export function elDiz(idler: number[], yer: Yerlesim): Map<number, KartYer> {
  const out = new Map<number, KartYer>();
  const n = idler.length;
  const arka = yer.satir === 2 ? Math.ceil(n / 2) : 0;
  const onY = yer.H - yer.eylemAlt - yer.bosluk - yer.kw * 0.12 - yer.kh / 2;
  const diz = (liste: number[], y: number, z0: number) => {
    const c = liste.length;
    const egim = Math.min(13, c * 1.7);
    liste.forEach((id, j) => {
      const u = c > 1 ? (j / (c - 1)) * 2 - 1 : 0;
      out.set(id, { x: yer.W / 2 + (j - (c - 1) / 2) * yer.adim, y: y + u * u * yer.kw * 0.11, a: u * egim, z: z0 + j });
    });
  };
  if (arka) diz(idler.slice(0, arka), onY - yer.kh * 0.52, 1);
  diz(idler.slice(arka), onY, 100);
  return out;
}

/** Oyuncunun kartlarının uçtuğu / geldiği nokta */
export function oyuncuNokta(yer: Yerlesim, id: string, ben: string): Nokta {
  if (id === ben || !yer.koltuk[id]) return { x: yer.W / 2, y: yer.H - yer.eylemAlt - yer.bosluk - yer.kh / 2 };
  return yer.koltuk[id];
}
/** Oyuncunun üstünde damga (＋2, Atlandı…) noktası */
export function damgaNokta(yer: Yerlesim, id: string, ben: string): Nokta {
  if (id === ben || !yer.koltuk[id]) return { x: yer.W / 2, y: yer.elUst + yer.kh * 0.2 };
  return yer.koltuk[id];
}
