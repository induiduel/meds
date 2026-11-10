/**
 * İyimser hamle tahmini (istemci): oyuncunun kendi hamlesi sunucu yanıtı beklenmeden ekrana yansır.
 * Ağ gidiş-dönüşü (Cloudflare tüneli üstünden ~100 ms, ara ara 0,5–2 sn) her hamlede ekranı dondurmasın diye.
 *
 * - Yalnız sonucu istemcide kesin bilinen kısım tahmin edilir (taş/kart elden çıkar, tahtaya konur); gizli bilgi
 *   (çekilen taş, zar, sıradaki oyuncu) tahmin edilmez — sıra bilinmiyorsa '' yazılır, böylece ekran ikinci hamleyi kilitler.
 * - Sunucu her zaman son sözü söyler: gelen `durum` tahmini ezer, `hata` gelirse son onaylı görünüme dönülür.
 * - Tahmin edilemeyen hamle için null döner (eski davranış: "Hamlen gönderiliyor" beklemesi).
 */
import type { CizgiGorunum, GoGorunum, GoTas, Hamle, OdaGorunum, OkeyGorunum, UnoGorunum, XoxGorunum } from './tipler';
import type { PistiGorunum } from './motor/pisti';
import type { DominoGorunum } from './motor/domino';

const kopya = <T>(x: T): T => JSON.parse(JSON.stringify(x));

export function hamleTahmini(oda: OdaGorunum, h: Hamle): OdaGorunum | null {
  const g = oda.oyun;
  if (!g || oda.asama !== 'oyun' || oda.durdu || oda.izliyor || g.bitti || g.sira !== oda.ben) return null;
  const ben = oda.ben;
  try {
    const oyun = tahmin(g as any, h as any, ben);
    return oyun ? { ...oda, oyun } : null;
  } catch { return null; }
}

function tahmin(g: any, h: any, ben: string) {
  switch (g.tur) {
    case 'xox': return h.t === 'koy' ? xox(g, h.i, ben) : null;
    case 'go': return h.t === 'koy' ? go(g, h.i, ben) : null;
    case 'uno': return h.t === 'oyna' ? uno(g, h, ben) : null;
    case 'pisti': return h.t === 'oyna' ? pisti(g, h.kart, ben) : null;
    case 'domino': return h.t === 'koy' ? domino(g, h, ben) : null;
    case 'cizgi': return h.t === 'ilerle' ? cizgi(g, h.yon, ben) : null;
    case 'yuzbir': return h.t === 'at' ? okeyAt(g, h.tas, ben) : null;
    default: return null;
  }
}

function xox(g0: XoxGorunum, i: number, ben: string): XoxGorunum | null {
  if (g0.tahta[i] !== '' || !g0.isaretler[ben]) return null;
  const g = kopya(g0);
  g.tahta[i] = g.isaretler[ben];
  g.son = i;
  g.sira = Object.keys(g.isaretler).find((k) => k !== ben) || '';
  return g;
}

function go(g0: GoGorunum, i: number, ben: string): GoGorunum | null {
  if (g0.asama !== 'oyun' || !g0.yasal.includes(i)) return null;
  const renk = g0.renkler[ben];
  if (!renk) return null;
  const g = kopya(g0);
  const n = g.boyut, rakip: GoTas = renk === 'S' ? 'B' : 'S';
  g.tahta[i] = renk;
  const komsu = (p: number) => {
    const x = p % n, y = (p - x) / n, r: number[] = [];
    if (x > 0) r.push(p - 1); if (x < n - 1) r.push(p + 1); if (y > 0) r.push(p - n); if (y < n - 1) r.push(p + n);
    return r;
  };
  const grup = (p: number) => {
    const c = g.tahta[p], gor = new Set([p]), yig = [p];
    let nefes = false;
    while (yig.length) for (const q of komsu(yig.pop()!)) {
      if (g.tahta[q] === '') nefes = true;
      else if (g.tahta[q] === c && !gor.has(q)) { gor.add(q); yig.push(q); }
    }
    return { taslar: [...gor], nefes };
  };
  let esir = 0;
  for (const q of komsu(i)) if (g.tahta[q] === rakip) {
    const gr = grup(q);
    if (!gr.nefes) for (const t of gr.taslar) { g.tahta[t] = ''; esir++; }
  }
  g.esir[renk] += esir;
  g.son = { renk, i };
  g.ko = null;
  g.yasal = [];
  g.hamleSayisi += 1;
  g.sira = Object.keys(g.renkler).find((k) => k !== ben) || '';
  return g;
}

function uno(g0: UnoGorunum, h: { kart: number; renk?: any }, ben: string): UnoGorunum | null {
  if (!g0.oynanabilir.includes(h.kart) || g0.dortBekle || g0.renkSec) return null;
  const kart = g0.elim.find((k) => k.id === h.kart);
  if (!kart || (!kart.renk && !h.renk)) return null;
  const g = kopya(g0);
  g.elim = g.elim.filter((k) => k.id !== h.kart);
  g.ust = kart;
  g.aktifRenk = kart.renk || h.renk;
  g.atikSayisi += 1;
  const o = g.oyuncular.find((x) => x.id === ben);
  if (o) o.kartSayisi = g.elim.length;
  g.oynanabilir = []; g.cekilen = undefined;
  g.sira = ''; // pas/yön/atlama modları sırayı değiştirir: sunucu söyler
  return g;
}

function pisti(g0: PistiGorunum, kartId: number, ben: string): PistiGorunum | null {
  const kart = g0.elim.find((k) => k.id === kartId);
  if (!kart) return null;
  const g = kopya(g0);
  g.elim = g.elim.filter((k) => k.id !== kartId);
  g.ust = kart; g.yerSayisi += 1; // yeri alıp almadığını sunucu söyler
  const o = g.oyuncular.find((x) => x.id === ben) as any;
  if (o && typeof o.kartSayisi === 'number') o.kartSayisi -= 1;
  g.sira = '';
  return g;
}

function domino(g0: DominoGorunum, h: { tas: number; uc: 'bas' | 'son' }, ben: string): DominoGorunum | null {
  if (!g0.secenekler.some((s) => s.tas === h.tas && s.uc === h.uc)) return null;
  const tas = g0.elim.find((t) => t.id === h.tas);
  if (!tas) return null;
  const g = kopya(g0);
  g.elim = g.elim.filter((t) => t.id !== h.tas);
  if (h.uc === 'bas') g.zincir.unshift(tas); else g.zincir.push(tas);
  g.son = { o: ben, tas: h.tas, uc: h.uc };
  const o = g.oyuncular.find((x) => x.id === ben);
  if (o) o.tasSayisi = g.elim.length;
  g.secenekler = []; g.pasOlur = false; g.cekOlur = false;
  g.sira = '';
  return g;
}

function cizgi(g0: CizgiGorunum, yon: 'duz' | 'sol' | 'sag', ben: string): CizgiGorunum | null {
  if (g0.zar == null || g0.kalan <= 0 || g0.kapisma || !g0.yonler.includes(yon)) return null;
  const sira = Object.keys(g0.cizgiler);
  const k = sira.indexOf(ben);
  const cz = g0.cizgiler[ben];
  if (k < 0 || !cz?.length) return null;
  const g = kopya(g0);
  const b = cz[cz.length - 1], ileri = k === 0 ? 1 : -1;
  const yeni = yon === 'duz' ? { s: b.s, r: b.r + ileri } : { s: b.s + (yon === 'sol' ? -1 : 1), r: b.r };
  g.cizgiler[ben].push(yeni);
  if (yon !== 'duz') g.yanHak[ben] -= 1;
  g.kalan -= 1;
  // Bir sonraki düz adım yalnız açıkça boşsa tahmin edilir; yan geçiş ve kapışma kararını sunucu verir
  const on = { s: yeni.s, r: yeni.r + ileri };
  const dolu = Object.values(g.cizgiler).some((c) => c.some((x) => x.s === on.s && x.r === on.r));
  const kaleye = yeni.r === (k === 0 ? g.uzunluk - 1 : 0);
  g.yonler = g.kalan > 0 && !kaleye && on.r >= 0 && on.r < g.uzunluk && !dolu ? ['duz'] : [];
  if (!g.yonler.length) g.sira = '';
  return g;
}

function okeyAt(g0: OkeyGorunum, tasId: number, ben: string): OkeyGorunum | null {
  if (!g0.tur_.cekti || g0.yandanAlinan != null) return null;
  const tas = g0.elim.find((t) => t.id === tasId);
  if (!tas) return null;
  const g = kopya(g0);
  g.elim = g.elim.filter((t) => t.id !== tasId);
  const o = g.oyuncular.find((x) => x.id === ben);
  if (o) { o.tasSayisi = g.elim.length; if (o.atiklar) o.atiklar.push(tas); }
  g.sira = '';
  return g;
}
