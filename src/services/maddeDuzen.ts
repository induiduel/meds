/**
 * Ders metnini dışa aktarım (PDF/DOCX/TXT/MD) için okunaklı maddelere dizer — Sesli ders ve Etkileşimli ders ortak kullanır.
 * Metin birebir korunur; yalnız dizilim değişir: çok cümleli paragraf/madde → ilk cümle ana madde, sonrakiler iç içe alt madde;
 * "Yani/Örneğin…" açıklamaları ve "2 ölçütü ayırın"/"…:" duyurularından sonra gelenler bir düzey daha içte;
 * kısa noktasız satır ya da "…:" ile biten kısa satır alt başlık. Yazıyla sayılar ("iki virgül bir") rakama döner.
 */
import { sayilariYaz } from './sayiYazim';

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
  if (kisa && sayi && /(?<!\p{L})(ayrıl\p{L}*|dayan\p{L}*|vardır|vardır\p{L}*|bulunur|incelenir|görülür|sayılır|kullanılır|toplanır|sınıflandırılır)(?!\p{L})/u.test(d)) return +sayi[1];
  return 0;
}

/** Bir paragrafı Markdown maddelerine dizer. */
export function paragrafMd(metin: string, isaret = '-', girinti = '', baslikOlabilir = true): string {
  const cs = cumleler(metin);
  const ilk = duzMetin(cs[0] || '').trim();
  // Kısa, noktalama ile bitmeyen tek satır: alt başlık
  if (baslikOlabilir && cs.length === 1 && !/[.!?…:;]$/.test(ilk) && ilk.split(/\s+/).length <= 9) return `### ${ilk}`;
  if (cs.length === 1) return `${girinti}${isaret} ${cs[0]}`;
  const sat = [`${girinti}${isaret} ${cs[0]}`];
  let altVar = false, kalan = 0;
  for (const c of cs.slice(1)) {
    const d = duzMetin(c);
    const derin = altVar && (kalan > 0 || ACIKLAMA.test(d));
    sat.push(`${girinti}${derin ? '    ' : '  '}- ${c}`);
    if (derin) { if (kalan > 0 && !ACIKLAMA.test(d)) kalan--; }
    else { altVar = true; kalan = duyuru(d); }
  }
  return sat.join('\n');
}

/** Hazır Markdown gövdesini (Öğren anlatımı) yeniden dizer: başlık, not kutusu, tablo olduğu gibi kalır. */
export function mdDuzenle(md: string): string {
  const out: string[] = [];
  let tablo = false;
  for (const ham of sayilariYaz(md.replace(/\r/g, '')).split('\n')) {
    const l = ham.replace(/\s+$/, '');
    tablo = /^\s*\|/.test(l);
    if (!l.trim() || tablo || /^\s*(#|>)/.test(l) || /^\s*[-*_]{3,}\s*$/.test(l)) { out.push(l); continue; }
    const li = l.match(/^(\s*)([-*•]|\d+[.)])\s+(.*)$/);
    if (li) {
      const isaret = /\d/.test(li[2]) ? li[2] : '-';
      out.push(cumleler(li[3]).length >= 3 ? paragrafMd(li[3], isaret, li[1], false) : `${li[1]}${isaret} ${li[3]}`);
      continue;
    }
    const t = l.trim();
    const d = duzMetin(t);
    // "Klinik Seyir ve Evreler:" gibi kısa duyuru satırı: alt başlık
    if (/:$/.test(d) && d.split(/\s+/).length <= 8 && cumleler(t).length === 1) { out.push(`### ${d.replace(/:$/, '').trim()}`); continue; }
    // 1–2 cümlelik giriş paragraf olarak kalır; daha uzunu maddelenir
    const cs = cumleler(t);
    // "Bu soru … ölçer." gibi tanıtım cümlesi giriş olarak kalır, ardındaki bilgi maddelenir
    if (cs.length >= 3 && /^Bu (soru|sorunun)/u.test(duzMetin(cs[0]))) { out.push(cs[0], paragrafMd(cs.slice(1).join(' '), '-', '', false)); continue; }
    out.push(cs.length >= 3 ? paragrafMd(t, '-', '', false) : t);
  }
  return out.join('\n');
}
