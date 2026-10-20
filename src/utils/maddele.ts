/**
 * Düz anlatım paragrafını madde düzeylerine ayırır (sesli ders metni ve ders notları ortak).
 * Metin değiştirilmez; yalnız her cümlenin düzeyi (0 giriş, 1 madde, 2 alt madde) hesaplanır.
 */

const SAYI_SOZ: Record<string, number> = { iki: 2, üç: 3, dört: 4, beş: 5, altı: 6, yedi: 7 };
const SAYIM_RE = /(?:^|\s)(\d|iki|üç|dört|beş|altı|yedi)\s+(?:\S+\s+){0,2}?(?:temel\s+|ana\s+|alt\s+)?(bilgi|tip|tür|grup|grub|aşama|evre|dönem|faz|özellik|neden|bulgu|basamak|kategori|bileşen|komponent|öge|öğe|madde|yol|yöntem|sınıf|faktör|etken|mekanizma|kriter|belirti|form|şekil|şekl|parça|bölüm|katman|tabaka|kısım|kısm|unsur|ilke|kural|risk|sonuç|komplikasyon|alan|bölge|hücre|organ)/i;
/** Sayı vermeden liste açan cümleler ("şunlardır", "ikiye ayrılır", "başlıcaları") */
const LISTE_ACAN_RE = /(şunlardır|şunlar|şöyledir|şöyle sıralanır|sıralanabilir|başlıcaları|başlıca\s+\S+\s+(?:şunlar|şöyle)|(?:ikiye|üçe|dörde|beşe|gruba|gruplara|tipe|tiplere|türe|türlere|alt tiplere)\s+ayrılır|olarak (?:ikiye|üçe|dörde) ayrılır)/i;
/** Bir önceki maddeyi açan ya da gerekçelendiren cümleler */
const AYRINTI_RE = /^(Yani|Örneğin|Mesela|Başka bir deyişle|Bir başka deyişle|Diğer bir deyişle|Bu da|Bu sayede|Bunun anlamı|Bunun nedeni|Bunun sebebi|Çünkü|Zira|Nitekim|Özellikle|Bu durumda|Bu tabloda|Bu hastalarda|Burada|Bunlardan|Bunlar arasında|Bunların|Bu grupta|Bu tipte|Bu evrede|Bu aşamada|Söz gelimi|Tipik örneği|En sık örneği|Klasik örneği)(?=[\s,:;]|$)/;
/** Sıralayan cümleler (ilk/ikinci/son öge): kendinden önce 1. düzey bir madde varsa alt madde olur */
const SIRA_RE = /^(\d+\.'?(?:si|sı|sü|su|ncisi|ncısı)|Birincisi|İlki|İlk olarak|İlk tip|İlk grup|İkincisi|İkinci olarak|İkinci tip|İkinci grup|Üçüncüsü|Üçüncü olarak|Dördüncüsü|Beşincisi|Son olarak|Sonuncusu|Diğeri|Bir diğeri|Diğer bir|Öteki|Ötekisi)(?=[\s,:;]|$)/;
/** Önceki ögeleri toparlayan sayım ("Bu 3 yol…") yeni liste açmaz */
const GERI_SAYIM_RE = /^(Bu|Bunlar|Her|Hepsi|Tüm|Bütün|Söz konusu)\s/;
const TOPLAM_RE = /^(Bu |Bunlar |Böylece|Sonuç olarak|Özetle|Kısacası|Ancak|Fakat|Öte yandan|Buna karşılık|Genel olarak|Toplamda|Hepsinde|Her (?:iki|üç)\S*)/;

/** Cümle düzeyleri (0 giriş, 1 madde, 2 alt madde): sayım cümlesinin ("4 temel bilgi içerir") ardındaki N cümle,
 *  liste açan cümlenin (iki nokta, "şunlardır", "ikiye ayrılır") ardındakiler toparlayan cümleye dek, sıralayan
 *  ("Birincisi", "Diğeri", "Son olarak") ve açıklayan ("Yani", "Örneğin", "Çünkü") cümleler alt maddedir; sıralayan cümle yalnız alt madde dizisini sürdürür. */
export function cumleDuzeyleri(cumleler: string[]): number[] {
  const d: number[] = cumleler.map((_, c) => (c ? 1 : 0));
  let kalan = 0, acik = false;
  cumleler.forEach((t, c) => {
    if (!c) { /* giriş */ }
    else if (kalan > 0) { d[c] = 2; kalan--; }
    else if (acik && !TOPLAM_RE.test(t)) d[c] = 2;
    else if (AYRINTI_RE.test(t) && c > 1) d[c] = 2;
    else if (SIRA_RE.test(t) && d[c - 1] === 2) d[c] = 2; // sıralama önceki alt maddelerin kardeşidir
    acik = acik && d[c] === 2 && !TOPLAM_RE.test(t);
    if (d[c] < 2 || kalan === 0) {
      const m = t.match(SAYIM_RE);
      const n = m ? (SAYI_SOZ[m[1].toLocaleLowerCase('tr')] ?? +m[1]) : 0;
      if (n >= 2 && n <= 7 && c + 1 < cumleler.length && !SIRA_RE.test(t) && !GERI_SAYIM_RE.test(t)) { kalan = n; acik = false; }
      else if (/:\s*$/.test(t) || LISTE_ACAN_RE.test(t)) { acik = true; kalan = 0; }
    }
  });
  // Üst maddesi olmayan alt madde (girişin hemen ardı) 1. düzeye çekilir
  return d.map((x, c) => (x === 2 && c > 0 && d[c - 1] === 0 ? 1 : x));
}

/** Nokta sonrası bölünmeyen kısaltmalar (unvan, "vb.", "örn.", tek harf) */
const KISALTMA_RE = /(?:^|[\s(])(?:Prof|Doç|Dr|Uzm|Op|Yrd|Arş|Gör|Öğr|vb|vs|örn|bkz|yy|No|St|Tel|[A-ZÇĞİÖŞÜ])\.$/;

/** Cümle sınırları (sesli ders `cumleSinirlari` ile aynı kural): [.!?…] + boşluk; ardı küçük harfse sınır değil. */
export function cumleSonlari(metin: string): number[] {
  const out: number[] = [];
  const re = /[.!?…]+["'”’)\]]*(?:\s+|$)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(metin))) {
    if (!m[0]) { re.lastIndex++; continue; }
    const e = m.index + m[0].length;
    const n = metin.charAt(e);
    if (n && n !== n.toLocaleUpperCase('tr') && n === n.toLocaleLowerCase('tr')) continue;
    if (KISALTMA_RE.test(metin.slice(Math.max(0, m.index - 8), m.index + 1))) continue;
    if (e > (out[out.length - 1] || 0)) out.push(e);
    if (re.lastIndex >= metin.length) break;
  }
  if (!out.length || out[out.length - 1] < metin.length) out.push(metin.length);
  return out;
}

/** Paragrafı [cümle, düzey] listesine çevirir; 3 cümleden kısaysa null (düz paragraf kalır). */
export function maddele(metin: string): { t: string; d: number }[] | null {
  const s = cumleSonlari(metin);
  if (s.length < 3) return null;
  const c = s.map((e, i) => metin.slice(i ? s[i - 1] : 0, e).trim());
  // Slayt parçası / OCR kırıntısı: cümlelerden biri 4 sözcükten kısaysa düz paragraf kalır
  if (c.some((t) => t.split(/\s+/).length < 4)) return null;
  const d = cumleDuzeyleri(c);
  return c.map((t, i) => ({ t, d: d[i] }));
}
