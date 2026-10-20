/**
 * Sesli ders konuşma metnini dışa aktarımda (PDF/DOCX/MD/TXT) ders notu üslubuna çevirir.
 * Kural tabanlı, yalnız dışa aktarılan Markdown'a uygulanır: sitedeki metin, ses ve zamanlama değişmez.
 *  - Sıralama: "1.'si …", "Birincisi …", "İkinci olarak …" → numaralı madde "1) …" (PDF'de "1 -").
 *  - Konuşma girişleri atılır: "Şunu da not edin:", "Burası önemli:", "Peki,", "Şimdi", "Gördüğünüz gibi," …
 *  - Yönlendirme cümleleri atılır: "Sözcüğün kökenine bakalım.", "Şimdi … geçelim." ve kısa retorik sorular.
 *  - "Neden?" + "Çünkü …" → "Nedeni: …".
 *  - Birinci/ikinci kişi fiiller edilgen olur: "deriz" → "denir", "görürüz" → "görülür", "dikkat edin" → "dikkat edilmelidir".
 */

const H = '(?<!\\p{L})';
const S = '(?!\\p{L})';

const SIRA_SOZ: [RegExp, number][] = [
  [/^(?:Birincisi|İlki|İlk olarak|Birinci olarak)/u, 1],
  [/^(?:İkincisi|İkinci olarak)/u, 2],
  [/^(?:Üçüncüsü|Üçüncü olarak)/u, 3],
  [/^(?:Dördüncüsü|Dördüncü olarak)/u, 4],
  [/^(?:Beşincisi|Beşinci olarak)/u, 5],
  [/^(?:Altıncısı|Altıncı olarak)/u, 6],
  [/^(?:Yedincisi|Yedinci olarak)/u, 7],
];
const SIRA_RAKAM = /^(\d{1,2})\.?\s*'?\s*(?:si|sı|sü|su|nci(?:si)?|ncı(?:sı)?|ncü(?:sü)?|ncu(?:su)?|üncüsü|inci(?:si)?)(?!\p{L})/u;

/** Satır başında atılan konuşma girişleri (ardından gelen ilk harf büyütülür) */
const GIRIS = new RegExp(
  '^(?:' + [
    'Şunu da not edin', 'Şunu not edin', 'Not edin', 'Şunu da ekleyelim', 'Şunu ekleyelim', 'Dikkat edin', 'Şuna dikkat edin',
    'Burası çok önemli', 'Burası önemli', 'Bu çok önemli', 'Bunu unutmayın', 'Şunu unutmayın', 'Unutmayın',
    'Aklınızda tutun', 'Şunu aklınızda tutun', 'Önemli olan şu', 'Şöyle düşünün', 'Şöyle özetleyelim', 'Özetleyelim',
    'Toparlayalım', 'Toparlarsak', 'Kısaca söylemek gerekirse', 'Kısacası', 'Peki', 'Şimdi', 'Evet', 'Bakın',
    'Gördüğünüz gibi', 'Bildiğiniz gibi', 'Hatırlarsanız', 'Hatırlayacağınız gibi', 'Açıkçası', 'Aslında', 'Tabii ki', 'Tabii',
    'Şimdi de', 'Gelelim', 'Gelin', 'Şunu iyi ayırın', 'Şunu da ayırın', 'Şunu ayırın', 'Bunu ayırın', 'Şunu ayırt edin',
  ].join('|') + ')' + S + '\\s*[:,!]?\\s*',
  'u',
);

/** Yalnız yönlendirme olan kısa cümleler: tamamen atılır */
const YONLENDIRME = new RegExp(`${H}(bakalım|geçelim|başlayalım|devam edelim|toparlayalım|hatırlayalım|göz atalım|inceleyelim|açalım|ilerleyelim)[.!…]*$`, 'u');

const FIIL: [string, string][] = [
  ['diyoruz', 'denir'], ['deriz', 'denir'], ['diyebiliriz', 'denebilir'], ['söyleriz', 'söylenir'], ['söyleyebiliriz', 'söylenebilir'],
  ['görürüz', 'görülür'], ['görüyoruz', 'görülür'], ['görebiliriz', 'görülebilir'], ['buluruz', 'bulunur'], ['ayırırız', 'ayrılır'],
  ['ayırıyoruz', 'ayrılır'], ['inceleriz', 'incelenir'], ['inceliyoruz', 'incelenir'], ['kullanırız', 'kullanılır'],
  ['adlandırırız', 'adlandırılır'], ['sınıflandırırız', 'sınıflandırılır'], ['düşünürüz', 'düşünülür'], ['bekleriz', 'beklenir'],
  ['ararız', 'aranır'], ['yaparız', 'yapılır'], ['koyarız', 'konur'], ['veririz', 'verilir'], ['alırız', 'alınır'], ['tanırız', 'tanınır'],
  ['ölçeriz', 'ölçülür'], ['hesaplarız', 'hesaplanır'], ['uygularız', 'uygulanır'], ['izleriz', 'izlenir'], ['sorgularız', 'sorgulanır'],
  ['ederiz', 'edilir'], ['ediyoruz', 'edilir'], ['edebiliriz', 'edilebilir'],
  ['dikkat edin', 'dikkat edilmelidir'], ['unutmayın', 'unutulmamalıdır'], ['aklınızda tutun', 'akılda tutulmalıdır'],
  ['ayırt edin', 'ayırt edilmelidir'], ['ayırın', 'ayrılmalıdır'], ['hatırlayın', 'hatırlanmalıdır'], ['düşünün', 'düşünülmelidir'],
];
const FIIL_RE = FIIL.map(([a, b]) => [new RegExp(`${H}${a}${S}`, 'gu'), b] as const);

const buyut = (s: string) => {
  const m = s.match(/^((?:\*\*|==|["“(])*)(\p{Ll})/u);
  return m ? m[1] + m[2].toLocaleUpperCase('tr') + s.slice(m[0].length) : s;
};
const duz = (s: string) => s.replace(/\*\*|==/g, '');

/** Tek madde satırının metnini redakte eder; numara bulunursa döndürür. */
function satirRedakte(metin: string): { t: string; no?: number } {
  const m = metin.match(/^((?:\*\*|==)*)([\s\S]*)$/u)!;
  let on = m[1], t = m[2];
  let no: number | undefined;
  for (let i = 0; i < 3; i++) {
    const once = t;
    t = t.replace(GIRIS, '');
    if (t === once) break;
  }
  const r = t.match(SIRA_RAKAM);
  if (r) { no = +r[1]; t = t.slice(r[0].length).replace(/^[\s,:;-]+/, ''); }
  else for (const [re, n] of SIRA_SOZ) {
    const k = t.match(re);
    if (k) { no = n; t = t.slice(k[0].length).replace(/^[\s,:;-]+/, ''); break; }
  }
  // "1.'si nörojenik reflekslerdir; …" → "1) Nörojenik refleksler: …" (sıralı maddenin başındaki yüklem eki atılır)
  if (no) t = t.replace(/^([^;.,:]{2,60}?)'?[dt][ıiuü]r(\*\*|==)*([;.]|$)/u, (_, a, m = '', p) => `${a}${m}${p === ';' ? ':' : p}`);
  t = t.replace(/^Son olarak[,\s]+/u, '').replace(/^Çünkü\s+/u, 'Nedeni: ');
  t = t.replace(/^Buradaki temel ilke şudur:\s*/u, 'Temel ilke: ');
  // Edilgen yapı belirtme durumlu nesneyle bozulur ("Etiyolojiyi 2 gruba ayrılır"): öyle cümlede fiile dokunulmaz
  if (!/\p{L}{2,}[ıiuü](?!\p{L})/u.test(duz(t))) for (const [re, b] of FIIL_RE) t = t.replace(re, b);
  else t = t.replace(FIIL_RE[0][0], 'denir').replace(FIIL_RE[1][0], 'denir');
  return { t: buyut(on + t), no };
}

/** paragrafMd çıktısını (madde/alt başlık satırları) ders notu üslubuna çevirir. */
export function konusmaRedakte(md: string): string {
  const out: string[] = [];
  const sat = md.split('\n');
  for (let k = 0; k < sat.length; k++) {
    const l = sat[k];
    const li = l.match(/^(\s*)([-*]|\d+\))\s+(.*)$/);
    const bas = l.match(/^(#{1,6}\s+)(.*)$/);
    const govde = li ? li[3] : bas ? bas[2] : l;
    const d = duz(govde).trim();
    const sozcuk = d.split(/\s+/).length;
    // Yönlendirme cümlesi ("Sözcüğün kökenine bakalım.") ve kısa retorik soru ("Neden?", "Peki bu ne demek?") atılır;
    // ardındaki "Çünkü …" satırı "Nedeni: …" olur.
    if (li && sozcuk <= 9 && YONLENDIRME.test(d)) continue;
    if (li && /\?$/.test(d) && (sozcuk <= 3 || /^Peki/u.test(d))) continue;
    // Tek satırlık soru paragrafı ("Bu değişiklikler hangi düzeyde aranır?") alt başlık olur
    if (li && /\?$/.test(d) && sat.length === 1 && !li[1] && sozcuk <= 12) { out.push(`- **${duz(satirRedakte(govde).t)}**`); continue; }
    if (!li) { out.push(bas ? bas[1] + satirRedakte(govde).t : l); continue; }
    const { t, no } = satirRedakte(govde);
    if (!duz(t).trim()) continue;
    out.push(`${li[1]}${no ? `${no})` : li[2]} ${t}`);
  }
  return out.join('\n');
}
