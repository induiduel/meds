/**
 * Tamamı BÜYÜK HARFLE yazılmış başlıkları (slayt/PDF adından gelen) okunur Türkçe başlık biçimine çevirir:
 * "DOĞUMSAL KADIN-ERKEK GENİTAL GELİŞİM ANOMALİLERİ" → "Doğumsal Kadın-Erkek Genital Gelişim Anomalileri".
 * Karışık yazılmış başlıklara dokunmaz. Romen rakamları, sayı içeren parçalar ve bilinen kısaltmalar büyük kalır;
 * bağlaçlar (ve, ile, veya…) küçük yazılır. Yalnız görüntüleme içindir; veri değişmez.
 */
const KISALTMA = new Set([
  'DNA', 'RNA', 'MRNA', 'HPV', 'HIV', 'HBV', 'HCV', 'PCR', 'EKG', 'EEG', 'MR', 'BT', 'USG', 'ATP', 'AIDS', 'TB', 'KOAH', 'SSS',
  'İYE', 'CYB', 'CMV', 'EBV', 'HSV', 'VZV', 'MRSA', 'TÜİK', 'DSÖ', 'WHO', 'ABO', 'RH', 'HLA', 'IGG', 'IGM', 'IGA', 'IGE', 'BPH', 'PSA',
]);
const BAGLAC = new Set(['ve', 'ile', 'veya', 'ya', 'da', 'de', 'ki', 'için', 'gibi']);
const ROMEN = /^(?=[IVXLC]+$)M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$/;

const kelime = (w: string, ilk: boolean): string => {
  const harf = w.replace(/[^\p{L}]/gu, '');
  if (!harf) return w;
  if (ROMEN.test(harf) || /\d/.test(w) || KISALTMA.has(harf.toLocaleUpperCase('tr-TR'))) return w;
  const kucuk = w.toLocaleLowerCase('tr-TR');
  if (!ilk && BAGLAC.has(harf.toLocaleLowerCase('tr-TR'))) return kucuk;
  // Tire/eğik çizgiyle birleşik parçaların her birinin baş harfi büyür
  return kucuk.replace(/(^|[-/(“"'])(\p{L})/gu, (_, a: string, b: string) => a + b.toLocaleUpperCase('tr-TR'));
};

export const okunurBaslik = (s: string): string => {
  if (!s) return s;
  const harfler = s.replace(/[^\p{L}]/gu, '');
  if (harfler.length < 6) return s;
  const buyuk = harfler.replace(/[^\p{Lu}]/gu, '').length;
  if (buyuk / harfler.length < 0.85) return s;
  return s.split(/(\s+)/).map((w, i) => (/^\s+$/.test(w) ? w : kelime(w, i === 0))).join('');
};
