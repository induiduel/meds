/** Klip sesinde o an okunan kelimeyi bulur (H655 ek 5, 2026-11-25).
 *  Klibin zaman kaydı CÜMLE başınadır (scripts/uretim/ses_ortak/ses_klip.py::cumlele); ekran ise metin PARÇASI gösterir
 *  (kök, şık, açıklama). Kayıt → (parça, cümle) eşlenir; kelime yalnız okunan cümlenin içinde, hece ağırlığıyla aranır. */

/** ses_klip.cumlele ile aynı kural ([.!?] + boşluk); ancak klip SESİN okuduğu metinden bölünür: "13. slayt" seste
 *  "on üçüncü slayt" (noktasız) olduğundan rakamdan sonraki nokta cümle sonu sayılmaz. */
/*  Klipler iki üretim kuralıyla bölünmüş olabilir (sıra sayısından sonra bölen / bölmeyen): ikisi de denenir, kayıt
 *  sayısını tutturan seçilir. */
const KURALLAR = [/(?<=(?:^|[^\d])[.!?])\s+/, /(?<=[.!?])\s+/];
export const cumleBol = (s: string, kural = 0) => s.trim().split(KURALLAR[kural]).filter((c) => c.trim());
const cumleSonuMu = (w: string, kural = 0) => /[.!?]$/.test(w) && (kural === 1 || !/^\d+\.$/.test(w));

export interface KayitYeri { m: number; s: number; ns: number }

/** zaman kayıtlarını metin parçalarına eşler: kayıt sayısı = parça sayısı → bire bir; = toplam cümle → cümle cümle */
export function kayitHaritasi(Z: number, metinler: string[]): KayitYeri[] {
  const M = metinler.length;
  if (Z === M) return metinler.map((_, m) => ({ m, s: 0, ns: 1 }));
  const sayim = (k: number) => metinler.map((c) => Math.max(1, cumleBol(c, k).length));
  let say = sayim(0);
  if (say.reduce((x, y) => x + y, 0) !== Z) say = sayim(1);
  if (say.reduce((x, y) => x + y, 0) !== Z) {
    // sayım tutmadı: tek parçaysa bütün kayıtlar o parçanın (vurgu parçanın toplam süresinde bir kez ilerler; eskiden her
    // kayıt bütün paragrafı yeniden tarıyordu), çok parçalıysa sırayla
    if (M === 1) return Array.from({ length: Z }, (_, q) => ({ m: 0, s: q, ns: Z }));
    return Array.from({ length: Z }, (_, q) => ({ m: Math.min(q, M - 1), s: 0, ns: 1 }));
  }
  const out: KayitYeri[] = [];
  say.forEach((ns, m) => { for (let q = 0; q < ns; q++) out.push({ m, s: q, ns }); });
  return out;
}

const hece = (w: string) => Math.max(1, (w.match(/[aeıioöuüâîû]/gi) || []).length + (/\d/.test(w) ? w.replace(/\D/g, '').length * 1.5 : 0));

/** kap içinde (atla seçicisine uyan alt ögeler hariç) t anında okunan kelimenin aralığı.
 *  b/e: okunan cümlenin zamanı; mb/me: parçanın zamanı; s/ns: cümlenin parçadaki sırası / parçanın cümle sayısı. */
export function okunanAralik(kap: Element, t: number, z: { b: number; e: number; s: number; ns: number; mb: number; me: number }, atla?: string): Range | null {
  const kel: { n: Text; b: number; e: number; h: number }[] = [];
  const tw = document.createTreeWalker(kap, NodeFilter.SHOW_TEXT, atla ? { acceptNode: (n) => (n.parentElement?.closest(atla) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT) } : undefined);
  for (let n = tw.nextNode() as Text | null; n; n = tw.nextNode() as Text | null) {
    for (const m of n.data.matchAll(/\S+/g)) kel.push({ n, b: m.index!, e: m.index! + m[0].length, h: hece(m[0]) });
  }
  if (!kel.length) return null;
  const grupla = (k: number) => { const g: number[] = [0]; kel.forEach((x, q) => { if (q + 1 < kel.length && cumleSonuMu(x.n.data.slice(x.b, x.e), k)) g.push(q + 1); }); return g; };
  let gruplar = grupla(0);
  if (gruplar.length !== z.ns) gruplar = grupla(1);
  let b0 = 0, b1 = kel.length, tb = z.mb, te = z.me;
  if (z.ns > 1 && gruplar.length === z.ns) { b0 = gruplar[z.s]; b1 = gruplar[z.s + 1] ?? kel.length; tb = z.b; te = z.e; }
  else if (z.ns === 1) { tb = z.b; te = z.e; }
  const dilim = kel.slice(b0, b1);
  const top = dilim.reduce((a, k) => a + k.h, 0);
  const oran = Math.min(1, Math.max(0, (t + 0.08 - tb) / Math.max(0.2, te - tb)));
  let acc = 0, w = 0;
  for (; w < dilim.length - 1; w++) { if (acc + dilim[w].h > oran * top) break; acc += dilim[w].h; }
  const k = dilim[w];
  const r = document.createRange();
  r.setStart(k.n, k.b); r.setEnd(k.n, k.e);
  return r;
}
