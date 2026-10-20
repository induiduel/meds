/**
 * Sesli ders metnini dışa aktarma belgesine çevirir (motor: services/metinDisaAktar).
 * Metin birebir korunur, yalnız okunaklı dizilir: her bölüm başlık; kısa, noktasız paragraf alt başlık;
 * paragrafın ilk cümlesi ana madde, sonraki cümleler iç içe alt madde, "Yani/Örneğin…" açıklamaları bir düzey daha içte.
 * Önemli cümleler ==…==, terimler **…**; okunuş için yazıya dökülmüş sayılar ("iki virgül bir") rakama döner.
 */
import type { AktarBelge } from '../../services/metinDisaAktar';
import { sayilariYaz } from '../../services/sayiYazim';
import type { CdDetay } from './canliDersStore';

function vurgula(metin: string, v?: [number, number, 'c' | 't', number][]): string {
  if (!v?.length) return metin;
  // [konum, işaret, sıra]: aynı konumda eklenen sonra eklenen öne geçer; istenen dizilim "**==" kapanış, "==**" açılış
  const ek: [number, string, number][] = [];
  let son = 0;
  for (const [s, e, tur] of v) {
    if (tur === 'c' && s >= son) { ek.push([s, '==', 1], [e, '==', 2]); son = e; }
  }
  for (const [s, e, tur] of v) if (tur === 't') ek.push([s, '**', 0], [e, '**', 3]);
  ek.sort((x, y) => y[0] - x[0] || x[2] - y[2]);
  let t = metin;
  for (const [k, m] of ek) t = t.slice(0, k) + m + t.slice(k);
  return t;
}

/** Paragraf içindeki satır sonları tek boşluk olur: aksi hâlde her satır ayrı blok sayılır ve paragraf sayfa arasında bölünür. */
const tekSatir = (t: string) => t.replace(/[ \t]*\r?\n+[ \t]*/g, ' ').trim();

/** Cümlelere böler; açık kalan kalın ve vurgu işaretleri parça sonunda kapatılıp sonraki parçada yeniden açılır. */
function cumleler(t: string): string[] {
  const ham = t.split(/(?<=[.!?…](?:\*\*|==)*["”’)]?)\s+(?=(?:\*\*|==)*["“(]?[A-ZÇĞİÖŞÜ0-9%])/u);
  const out: string[] = [];
  let acik: string[] = [];
  for (const p of ham) {
    let s = acik.join('') + p;
    const yigin: string[] = [];
    for (const m of s.match(/\*\*|==/g) || []) {
      if (yigin[yigin.length - 1] === m) yigin.pop(); else yigin.push(m);
    }
    s += [...yigin].reverse().join('');
    acik = yigin;
    // işaretlerin yalnız sarmaladığı boş parça kalmasın
    if (s.replace(/\*\*|==/g, '').trim()) out.push(s.trim());
  }
  return out;
}

const duzMetin = (s: string) => s.replace(/\*\*|==/g, '');
/** Bir önceki cümleyi açıklayan/örnekleyen cümle: bir düzey daha içte durur. */
const ACIKLAMA = /^["“(]?(Yani|Örneğin|Mesela|Kısacası|Başka bir deyişle|Diğer bir deyişle|Bu da|Bu sayede|Bu nedenle|Bu yüzden|Bunun sonucunda|Sonuç olarak|Dolayısıyla)(?!\p{L})/u;

/** Ardından sayılacak maddeleri duyuran cümle ("… şunlardır:", "2 ölçütü iyi ayırın."): sonraki cümleler onun altına girer.
 *  Döner: kaç cümle altına girecek (sayı yoksa paragraf sonuna kadar), duyuru değilse 0. */
function duyuru(d: string): number {
  const kisa = d.split(/\s+/).length <= 14;
  const sayi = d.match(/(?:^|\s)([2-6])\s+\p{L}/u);
  if (/:$/.test(d) || /(?<!\p{L})(şunlardır|şöyledir|şöyle sıralanır|şunlar|ayırın|ayırt edin)(?!\p{L})/u.test(d)) return sayi ? +sayi[1] : 99;
  if (kisa && sayi && /(?<!\p{L})(ayrılır|dayan\p{L}*|vardır|bulunur|incelenir|görülür|sayılır|kullanılır)(?!\p{L})/u.test(d)) return +sayi[1];
  return 0;
}

/** Bir paragrafı Markdown maddelerine dizer. */
function paragrafMd(metin: string): string {
  const cs = cumleler(metin);
  const ilk = duzMetin(cs[0] || '').trim();
  // Kısa, noktalama ile bitmeyen tek satır: alt başlık
  if (cs.length === 1 && !/[.!?…:;]$/.test(ilk) && ilk.split(/\s+/).length <= 9) return `### ${ilk}`;
  if (cs.length === 1) return `- ${cs[0]}`;
  const sat = [`- ${cs[0]}`];
  let altVar = false, kalan = 0;
  for (const c of cs.slice(1)) {
    const d = duzMetin(c);
    const derin = altVar && (kalan > 0 || ACIKLAMA.test(d));
    sat.push(`${derin ? '    ' : '  '}- ${c}`);
    if (derin) { if (kalan > 0 && !ACIKLAMA.test(d)) kalan--; }
    else { altVar = true; kalan = duyuru(d); }
  }
  return sat.join('\n');
}

export function cdAktarBelgesi(detay: CdDetay, etiket: string, vurguAcik = true): AktarBelge {
  return {
    baslik: detay.baslik,
    alt: `${etiket} · Sesli ders metni${vurguAcik && detay.vurgu ? ' · işaretli yerler çıkmış, örnek soru ve spotlarla eşleşen önemli bilgiler' : ''}`,
    bolumler: detay.bolumler.map((b) => ({
      baslik: b.baslik.trim(),
      md: b.paragraflar.filter((p) => p.metin.trim())
        .map((p) => paragrafMd(sayilariYaz(tekSatir(vurgula(p.metin, vurguAcik ? detay.vurgu?.[p.i] : undefined)))))
        .join('\n'),
    })),
  };
}
