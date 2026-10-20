/**
 * Okunuş için yazıya dökülmüş sayıları yazılı biçime geri çevirir:
 *   "iki virgül bir" → "2,1", "sıfır virgül sıfır beşe" → "0,05'e", "yüzde kırkına" → "%40'ına", "yüzde on iki virgül beş" → "%12,5".
 * Yalnız ondalık (virgül) ve yüzde kalıplarına dokunur; "üç yılda" gibi düz sayı sözcükleri metinde kalır.
 * Ekran/PDF/DOCX dışa aktarımı ve Python denetim kapısı (scripts/sesli_anlatim/metin_denetle.py) aynı kuralı kullanır.
 */
const DEGER: Record<string, number> = {
  sıfır: 0, bir: 1, iki: 2, üç: 3, dört: 4, beş: 5, altı: 6, yedi: 7, sekiz: 8, dokuz: 9,
  on: 10, yirmi: 20, otuz: 30, kırk: 40, elli: 50, altmış: 60, yetmiş: 70, seksen: 80, doksan: 90,
  yüz: 100, bin: 1000, milyon: 1e6,
};
// "İki" gibi cümle başı büyük harfler: JS'in i bayrağı İ/ı eşlemesini yapmaz
const KOK = Object.keys(DEGER).flatMap((k) => [k, k[0].toLocaleUpperCase('tr') + k.slice(1)])
  .sort((a, b) => b.length - a.length).join('|');
// Sayının son sözcüğüne bitişik çekim eki (kaynaştırma harfi dahil okunduğu gibi yazılır: "bire" → "1'e", "ikiye" → "2'ye")
const EK = "(?:y?[dt][ıiuü]r|y?[aeıiuü]|n?[dt][ae]n?|n?[ıiuü]n|s?[ıiuü](?:n[ae]|nd[ae]n?|n[ıiuü]n)?|y?l[ae]|l[ae]r[ıi]?|y?[ıiuü]n[ae])?";
const SOZ = `(?:${KOK})`;
const DIZI = `${SOZ}(?:\\s+${SOZ})*`;
const ON_EK = '(?<![\\p{L}\\d])';
const SON = '(?![\\p{L}\\d])';

function deger(sozler: string[]): number {
  let toplam = 0, cur = 0;
  for (const w of sozler) {
    const v = DEGER[w];
    if (v === 100) cur = (cur || 1) * 100;
    else if (v >= 1000) { toplam += (cur || 1) * v; cur = 0; }
    else cur += v;
  }
  return toplam + cur;
}
/** ondalık kısım: baştaki "sıfır"lar sıfır basamağıdır ("sıfır sıfır beş" → "005") */
function ondalik(sozler: string[]): string {
  let i = 0, z = '';
  while (i < sozler.length - 1 && sozler[i] === 'sıfır') { z += '0'; i++; }
  return z + String(deger(sozler.slice(i)));
}
const kelimeler = (s: string) => s.trim().split(/\s+/);
const ekli = (n: string, ek: string) => (ek ? `${n}'${ek}` : n);

const R_ONDALIK = new RegExp(`${ON_EK}([yY]üzde\\s+)?(${DIZI})\\s+virgül\\s+(${DIZI})(${EK})${SON}`, 'giu');
const R_YUZDE = new RegExp(`${ON_EK}[yY]üzde\\s+(${DIZI})(${EK})${SON}`, 'giu');

const ondalikYaz = (_m: string, yuzde: string | undefined, tam: string, kesir: string, ek: string) => {
  const n = `${deger(kelimeler(tam.toLocaleLowerCase('tr')))},${ondalik(kelimeler(kesir.toLocaleLowerCase('tr')))}`;
  return ekli(yuzde ? `%${n}` : n, ek);
};
const yuzdeYaz = (_m: string, dizi: string, ek: string) => ekli(`%${deger(kelimeler(dizi.toLocaleLowerCase('tr')))}`, ek);

export function sayilariYaz(metin: string): string {
  if (!/virgül|üzde/i.test(metin)) return metin;
  return metin.replace(R_ONDALIK, ondalikYaz as any).replace(R_YUZDE, yuzdeYaz as any);
}

/** sayilariYaz + eski karakter konumunu yeni metne çeviren işlev (vurgu / cümle aralıkları kaymasın diye).
 *  Dönüşen parçanın içine düşen konum parçanın başına (başlangıç) ya da sonuna (bitiş) yapışır. */
export function sayilariYazEslemeli(metin: string): { metin: string; konum: (k: number, bitis?: boolean) => number } {
  if (!/virgül|üzde/i.test(metin)) return { metin, konum: (k) => k };
  // [eski baş, eski son, yeni baş, yeni son] — iki geçiş art arda uygulanır
  const gecis = (t: string, re: RegExp, fn: (...a: any[]) => string) => {
    const d: [number, number, number, number][] = [];
    let kay = 0;
    const yeni = t.replace(re, (...a: any[]) => {
      const m = a[0] as string, i = a[a.length - 2] as number;
      const r = fn(...a);
      d.push([i, i + m.length, i + kay, i + kay + r.length]);
      kay += r.length - m.length;
      return r;
    });
    const f = (k: number, bitis = false) => {
      let off = 0;
      for (const [os, oe, ns, ne] of d) {
        if (k < os || (k === os && !bitis)) break;
        if (k < oe || (k === oe && bitis && k === os)) return bitis ? ne : ns;
        off = ne - oe;
      }
      return k + off;
    };
    return { yeni, f };
  };
  const a = gecis(metin, R_ONDALIK, ondalikYaz);
  const b = gecis(a.yeni, R_YUZDE, yuzdeYaz);
  return { metin: b.yeni, konum: (k, bitis) => b.f(a.f(k, bitis), bitis) };
}
