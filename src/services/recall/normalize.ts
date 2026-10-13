/**
 * Öğrenci hatırlaması metin katmanı (soru havuzu motoru, aşama 1: temizleme).
 *
 * Ham metin ASLA değiştirilmez; buradaki çıktı yalnız eşleştirme/sınıflama/gruplama özellikleri içindir.
 * - Katlama (küçük harf, aksansız) → sözcükler
 * - Kısaltma/argo açma ("pato", "dgl", "tbc") ve sözlükle yazım düzeltme (aksansız + harf hatası:
 *   "otoimun gstrit" → "otoimmün gastrit"); sözlük çıkmış soru bankası + tıbbi sözlükten kurulur (lexicon.ts).
 * - Sohbet/üst söylem ayıklama ("arkadaşlar", "ben C yaptım", "iptal olur mu", "hoca slaytta…")
 * - Yapı çıkarımı: cevap iddiası (harf/metin), soru numarası, harfli/harfsiz şıklar, olumsuz kök ihtimali.
 */
import { fold } from '../questionIntake.ts';

export { fold };

export type Letter = 'A' | 'B' | 'C' | 'D' | 'E';
const LETTERS = new Set(['a', 'b', 'c', 'd', 'e']);

/** Soru dışı sözcükler: işlev sözcükleri + sınav/sohbet dili. Eşleştirmede yok sayılır. */
export const STOP = new Set(
  (
    // işlev sözcükleri + Romen rakamları / nicelik zarfları
    'a b c d e i ii iii iv v vi ve veya ile ya da de ki mi mu mı mü mii miydi muydu mıydı müydü midir mudur bu su o bir iki uc ' +
    'icin gibi kadar daha en cok az her hic hep tum butun bazi baska diger sonra once ise ama fakat yani cunku canku ' +
    'olan olarak olur olmaz oldu olmus olup olmasi olmayan olabilir olmali var yok vardi yoktu degil degildir dgl diil ' +
    'hangisi hangisidir hangi hangileri hangisinde asagidakilerden asagidaki asagidakiler seklinde sekilde durum durumda ' +
    'nedir neydi ne nasil neden niye kim kimin nerede ' +
    'yalniz yalnizca hepsi hicbiri birlikte arasinda ilgili olani olanlar birisi biri ikisi ucu ikili uclu dortlu ' +
    // sınav üst dili
    'soru sorusu sorusunu sorusunda sorudaki soruda sorulari sorular sorunun srs srsu sorudu sorulmus sormus sormustu ' +
    'sordu sordular soruldu soruluyor soruyordu sormuslardi ' +
    'sik sikki sikkiydi sikki siklarda siklar siklari sikkini sikta siklardaydi cevap cevabi cevapti cvp yanit dogru dogrudur yanlis yanlistir ' +
    'secenek secenekler seceneklerde kok koku ilk son sinav sinavda sinavin kurul komite ders derste hoca hocam hocanin hocalar slayt slaytta ' +
    'oncul onculu onculleri onculde onerme onermeler onermede ifade ifadeler ifadelerden ifadeleri celdirici celdiriciydi celdiriciler ' +
    'pato patoloji patolojide patoda farma farmada farmadan farmako farmakoloji mikro mikroda mikrobiyoloji biyokimya genetik genetikte urolojide norolojide dahiliyede ' +
    // sohbet / argo / öğrenci iç konuşması
    'arkadaslar arkadaslarim arkadas agalar aga abi abla kanka olm lan aq amk yaw ya yav be beyler millet gencler hocalar ' +
    'ben sen biz siz onlar bence sanirim galiba herhalde kesin kesinlikle emin eminim degilim bilmiyorum hatirlamiyorum ' +
    'hatirliyorum hatirlayan hatirlayamadim hatirladigim aklimda kalan aklimda kaldi falan filan felan sey bisey bi biseyler ' +
    'yaptim yaptik yaptiniz yapan yapti dedim dedik dediniz isaretledim isaretledik sectim salladim sallayan sallamis napti naptiniz nptnz ' +
    'dusun dusundum dusunuyorum dusunmustum karistirdim karisti karismis eledim elemistim sandim sanmistim kaldim kalmistim ' +
    'gecmis sonuc sonuclar sonuclari iptal itiraz iptali zor kolay zordu kolaydi sacma sacmaydi gicik yandi beynim offf off tuh insafsiz kim ne zaman ' +
    'diye diyen diyerek diyordu diyodu diyor dedi yaziyordu yazan yaziyor vardi geciyordu kaliyordu mesela tabi tabii tamam evet hayir dimi di mi degil mi ' +
    'gerisini gerisi hatirlarsaniz yazin yazsin bilen bilgisi net lutfen acaba mis mus miymis muymus daki deki taki teki'
  ).split(' '),
);

/** Ekli biçimleri de kapsayan sohbet/sınav dili kökleri ("sorusunda", "hatırlayamadım", "işaretlemiştim"). */
const STOP_PREFIX = /^(olsun|gelir|geldi|soru(?![nm])|srs|sru|anahtar|bitti|sukur|uzundu|agirdi|zordu|kolaydi|sikk|sıkk|cevab|cevap|cvp|hoca|arkadas|hatirl|hatrl|isaretl|yaptim|yaptin|yapmis|dedim|demist|dmst|iptal|itiraz|sinav|snv|naptin|naber|nasil|aciklan|bilmiyo|hatirlamiyo|hatirliyo|diyo|yaziyo|sanirim|galiba|celdiric|karistir|oncul|onerm)/;
export const isStop = (w: string) => STOP.has(w) || STOP_PREFIX.test(w);

/** 2 harfli geçerli tıbbi kısaltma ve element/immün belirteçler (`c.length < 3` filtresinde korunur). */
export const VALID_SHORT_MED = new Set([
  'ph', 'bt', 'mr', 'ms', 'lp', 'he', 'dm', 'ht', 'av', 'uv', 'qt', 'st', 'pr', 'rh',
  'ig', 'il', 'cd', 'nk', 'ca', 'mg', 'fe', 'na', 'zn', 'cu', 'li', 'al',
  'o1', 'c3', 'c4', 'b1', 'b2', 'b6', 'd3', 't3', 't4',
]);

/** Ders ipucu sözcükleri ("pato sorusu", "farmada") → ders adı parçası (sınıflayıcıya ön bilgi). */
export const DERS_HINT: [RegExp, RegExp][] = [
  [/^pato/, /patoloji/i], [/^farma/, /farmakoloji/i], [/^mikro/, /mikrobiyoloji/i], [/^genetik/, /genetik/i],
  [/^biyokim|^biyokm/, /biyokimya/i], [/^halk/, /halk sa/i], [/^enfeksiyon|^enfek/, /enfeksiyon/i], [/^dahili/, /iç hastalık/i],
  [/^uroloj/, /üroloji/i], [/^norolo/, /nöroloji/i], [/^psikiy/, /psikiyatri/i], [/^pediat|^cocuk/, /çocuk sağlığı/i],
  [/^kardiy/, /kardiyoloji/i], [/^gogus/, /göğüs/i], [/^kadin|^jinek/, /kadın hastalık/i], [/^ortoped/, /ortopedi/i],
];

/**
 * Kısaltma ve argo açılımları (katlanmış). Her tıbbi kısaltma TEK kanonik köke açılır ki:
 * 1) Kısaltma yazanla açık adını yazan aynı 5-harfli kökü paylaşsın ("TCA" ↔ "trisiklik", "VZV" ↔ "varicella"),
 * 2) Tek bir hastalık/kavram 4 ayrı köke şişip farklı soruları yanlış birleştirmesin.
 */
export const ABBREV: Record<string, string> = {
  tbc: 'tuberkuloz', tb: 'tuberkuloz', hst: 'hastalik', hstlk: 'hastalik', hastaligi: 'hastaligi',
  sdr: 'sendromu', snd: 'sendromu', sendr: 'sendromu', dm: 'diyabet', ht: 'hipertansiyon', koah: 'koah',
  ihk: 'immunohistokimya', ihc: 'immunohistokimya', zn: 'ziehl', inh: 'inhibitor', ab: 'antikor',
  ecoli: 'escherichia', 'e.coli': 'escherichia', vit: 'vitamin', bnce: 'bence', dgl: 'degil', diil: 'degil', dğl: 'degil',
  olmz: 'olmaz', olr: 'olur', ypr: 'yapar', ypmz: 'yapmaz', yksk: 'yuksek', dsk: 'dusuk', artr: 'artar', azlr: 'azalir',
  enf: 'enfeksiyon', enfek: 'enfeksiyon', tdv: 'tedavi', tani: 'tani', bulg: 'bulgu',
  tca: 'trisiklik', pae: 'postantibiyotik', vzv: 'varicella', gbs: 'guillain',
  hcc: 'hepatoselluler', hsk: 'hepatoselluler', fap: 'polipozis', hsp: 'schonlein', pan: 'poliarteritis',
  uti: 'uriner', iye: 'uriner', tdlu: 'lobuler', mrg: 'rezonans', bt: 'tomografi',
  losit: 'lokosit',
};

/**
 * Katlanmış metni sözcüklere ayırır; harf+rakam bitişiklerini ayırır ("pepsinojen1" → "pepsinojen 1")
 * ve çok sözcüklü eş anlamlı tıbbi kalıpları kısaltmalarıyla aynı kanonik biçime hizalar.
 */
const MULTIWORD_CANON_RE =
  /\b(?:e\.?\s*coli|ecoli|s\.?\s*aureus|s\.?\s*pneumonia|s\.?\s*pyogenes|c\.?\s*difficile|h\.?\s*pylori|p\.?\s*aeruginosa|suciceg|kafa\s+ici|aile(?:vi|sel)\s+akdeniz|idrar\s+yolu|terminal\s+duktal|bilgisayarli\s+tomografi|manyetik\s+rezonans|multipl\s+skleroz|tca|fap|sitokrom|p\s*450|cyp|otozomal)/;

export function words(text: string): string[] {
  const raw = String(text || '');
  const pre = raw.includes('H')
    ? raw.replace(/\bH\s*[&-]\s*E\b/g, ' hematoksilen eozin ').replace(/\bHE\b/g, ' hematoksilen eozin ')
    : raw;
  let f = fold(pre);
  if (MULTIWORD_CANON_RE.test(f)) {
    f = f
      .replace(/\be\.?\s+coli\b/g, 'escherichia coli')
      .replace(/\becoli\b/g, 'escherichia coli')
      .replace(/\bs\.?\s+aureus\b/g, 'staphylococcus aureus')
      .replace(/\bs\.?\s+pneumonia\w*\b/g, 'streptococcus pneumoniae')
      .replace(/\bs\.?\s+pyogenes\b/g, 'streptococcus pyogenes')
      .replace(/\bc\.?\s+difficile\b/g, 'clostridium difficile')
      .replace(/\bh\.?\s+pylori\b/g, 'helicobacter pylori')
      .replace(/\bp\.?\s+aeruginosa\b/g, 'pseudomonas aeruginosa')
      .replace(/\bsuciceg(\w*)\b/g, 'su ciceg$1')
      .replace(/\bkafa\s+ici\s+basinc(?:\s+artis\w*)?(?:\s+sendrom\w*)?\b/g, 'kibas')
      .replace(/\baile(?:vi|sel)\s+akdeniz\s+ates\w*\b/g, 'fmf')
      .replace(/\bidrar\s+yolu\s+enfeksiyon(\w*)\b/g, 'uriner enfeksiyon$1')
      .replace(/\bterminal\s+duktal\s+lobuler(?:\s+unite\w*)?\b/g, 'tdlu')
      .replace(/\bbilgisayarli\s+tomografi\w*\b/g, 'tomografi')
      .replace(/\bmanyetik\s+rezonans\w*\b/g, 'mr rezonans')
      .replace(/\bmultipl\s+skleroz\w*\b/g, 'ms skleroz')
      .replace(/\btca\b/g, 'trisiklik antidepresan')
      .replace(/\bfap(\w*)\b/g, 'familyal adenomatoz polipozis')
      .replace(/\b(?:sitokrom\s+)?p\s*450\b|\bcyp\s*450\b/g, 'cyp p450')
      .replace(/\botozomal\s+dominant(\w*)\b/g, 'otodominant$1 dominant$1')
      .replace(/\botozomal\s+resesif(\w*)\b/g, 'otoresesif$1 resesif$1');
  }
  if (/\d/.test(f)) {
    f = f.replace(/([a-z]{3,})(\d)/g, '$1 $2').replace(/(\d)([a-z]{3,})/g, '$1 $2');
  }
  return f.split(' ').filter(Boolean);
}

// ---------------------------------------------------------------- yapı çıkarımı

const CLAIM_VERB = '(?:yaptim|yaptik|yaptiniz|yapan|dedim|dedik|isaretledim|isaretledik|isaretlemistim|sectim|salladim|verdim|' +
  'dogru|dogrudur|olmali|olmaliydi|olacakti|olcakti|cevapti|cevaptir|sikkiydi|sikki|sikkini|sikkina|siklari)';
const CLAIM_RES = [
  new RegExp(`\\b([a-e])\\s*(?:sikki(?:ydi|dir|ni|na)?\\s+)?${CLAIM_VERB}\\b`, 'g'),
  /\b(?:cevap|cevabi|cvp|yanit|yaniti|dogru cevap|dogrusu)\s*(?:da|de|ta|te)?\s*(?:[:=]\s*)?([a-e])\b(?!\s*[)\-:]\s*\w)/g,
  /\b([a-e])\s*(?:mi|mu)\s*(?:yaptiniz|dediniz|isaretlediniz)\b/g,
];

/** Cevap iddiası (harf). Ör. "C yaptım", "cevap B", "E şıkkıydı", "Renal agenezi C.", "dedim D". Son geçen kazanır. */
export function claimedLetter(text: string): Letter | null {
  // Sondaki sohbeti at ("brugada A valla", "C yazdım beynim yandı") ki son harf görünsün
  const TAIL_CHAT = /(?:\s+(?:valla|vallahi|aq|amk|yaw|ya|abi|galiba|sanirim|sanırım|bence|emin\s+de[gğ]ilim|kim\s+ne\s+yapt[ıi]|beynim\s+yand[ıi]|di\s*mi|dimi|degil\s+mi|değil\s+mi|yanl[ıi]?s?\s*m[ıi]|olabilir)[.!?,]*)+\s*$/iu;
  const raw = String(text || '').trim().replace(TAIL_CHAT, '').trim();
  const f = ` ${fold(raw)} `;
  // 1) Açık fiille iddia: "C yaptım", "dedim D", "B yazdım", "cevap E" — en güçlü kanıt, son geçen kazanır
  const after = /\b(?:dedim|dedik|yaptim|yazdim|yazdik|isaretledim|sectim|kesin|cevap|cvp|bence)\s+([a-e])\b(?!\s*[)\-:]\s*\w)/g;
  let last: { i: number; L: string } | null = null;
  for (const re of CLAIM_RES) {
    re.lastIndex = 0;
    let m: RegExpExecArray | null;
    while ((m = re.exec(f))) if (!last || m.index >= last.i) last = { i: m.index, L: m[1] };
  }
  after.lastIndex = 0;
  let m2: RegExpExecArray | null;
  while ((m2 = after.exec(f))) if (!last || m2.index >= last.i) last = { i: m2.index, L: m2[1] };
  if (last) return last.L.toUpperCase() as Letter;
  // 2) Mesaj sonunda tek büyük harf: "Renal agenezi C.", "MS D", "Su çiçeği sorusu C mi."
  const tail = /(?:^|[\s,])([A-E])\s*[.!?]*\s*(?:mi|mı|mu|mü)?\s*[.!?]*\s*$/.exec(raw);
  if (tail) return tail[1] as Letter;
  // 3) Numaradan ya da sohbetten hemen sonra tek büyük harf: "12 A e-kaderin", "9. soru A osler", "yaw E hepsi"
  const afterNo = /^\s*(?:\d{1,3}\s*(?:\.|'|’)?\s*(?:soru|sru|srs)?\s*|(?:yaw|aq|abi|hocam|ya)\s+)([A-E])\s+\S/u.exec(raw);
  if (afterNo) return afterNo[1] as Letter;
  // 4) Mesaj başında tek büyük harf: "C E148Q", "B serum yüksek doku düşük yanlış" ("A vitamini" değil)
  const head = /^\s*([A-E])\s+(?!(?:vitamin|vit|tipi|tip|grubu|grup|hepatit|antijen|kolu|bandı|bandi|bant|hücre|hucre|ve|ile)\b)\S/u.exec(raw);
  return head ? (head[1] as Letter) : null;
}

/** Cevap iddiası (metin): "cevap nistatin olmalı", "doğrusu kongo kırmızısı", "alkol dedim", "lizensefaliyi seçtim". */
export function claimedText(text: string): string | null {
  const f = fold(text);
  const said = /(?:^|\b)((?:[a-z0-9]+\s+){0,2}[a-z0-9]{3,})\s+(?:dedim|yaptim|yazdim|isaretledim|sectim|secmistim|demistim)\b/.exec(f);
  if (said) {
    const KEEP_CLAIM = new Set(['hepsi', 'hicbiri', 'yalniz']);
    const t = said[1].split(' ').filter((w) => (KEEP_CLAIM.has(w) || !STOP.has(w)) && !/^(ben|bence|soru|sorusu|sorusunda|\d+)$/.test(w)).join(' ');
    if (t.length >= 3 && !LETTERS.has(t)) return t;
  }
  const m = /\b(?:cevap|cevabi|cvp|dogru cevap|dogrusu|yanit)\s+(?:da|de\s+)?([a-z][a-z0-9 ]{2,40}?)\s+(?:olmali|olacakti|olcakti|dogru|olmaliydi|idi|ydi|di|olur)\b/.exec(f);
  if (!m) return null;
  const t = m[1].trim();
  return t.length >= 3 && !LETTERS.has(t) ? t : null;
}

/** Tıbbi birim/derece/kuşak/yaş belirten sayılar soru numarası değildir ("4. kuşak", "35 yaşında", "MİK 2"). */
const NON_QNO_BEFORE = /\b(?:mik|m[iı]k|tip|evre|evresi|derece|fakt[oö]r|il|cd|faz|ku[sş]ak|basamak|kromozom|sinir|ventrik[uü]l|doz|saat|g[uü]n|hafta|ay|y[iı]l|ya[sş]|ig|b|t|c|h|g\d*|s)\s*[-:]?\s*$/iu;
const NON_QNO_AFTER = /^(?:mg|g|gr|ml|mm|cm|kg|yas|yaş|yil|yıl|gun|gün|hafta|ay|saat|dk|dakika|sn|saniye|hz|ünite|unite|ü|u|%|x|tane|adet|kez|kat|mmhg|ve\b|ile\b|kuşak|kusak|basamak|derece|kromozom|ventrikül|ventrikul|kranial|kraniyal|sinir|evre|evresi|tip|tipi|grubu|grup|faktör|faktor|doz|oran|orani|-)/iu;

/** Soru numarası: "12. soru", "30'daki", "soru 7", "28 nolu". Yoksa null. */
export function questionNumber(text: string): number | null {
  const raw = String(text || '');
  const check = (m: RegExpExecArray | null, checkBefore = true, checkAfter = false): number | null => {
    if (!m) return null;
    const n = Number(m[1]);
    if (!(n >= 1 && n <= 200)) return null;
    const before = raw.slice(0, m.index);
    const after = raw.slice(m.index + m[0].length);
    if (checkBefore && NON_QNO_BEFORE.test(before)) return null;
    if (checkAfter && NON_QNO_AFTER.test(after.trim())) return null;
    return n;
  };
  const explicit = [
    /\b(\d{1,3})\s*(?:\.|'|’)?\s*(?:inci|ıncı|uncu|üncü|nci|ncı|ncu|ncü)?\s*(?:soru|sorusu|sorudaki|soruda|sorunun|srs|srsu|sru)\b/i,
    /\b(\d{1,3})\s*(?:'|’)?\s*(?:da|de|ta|te|daki|deki|taki|teki)\s+(?:ki\s+)?(?:\S+\s+){0,3}?(?:soru|sorusu|srs)/i,
    /\bsoru\s*(?:no|numarası|numarasi|#)?\s*[:.]?\s*(\d{1,3})\b/i,
    /\b(\d{1,3})\s*(?:nolu|numaralı|numarali)\b/i,
  ];
  for (const p of explicit) {
    const n = check(p.exec(raw), true, false);
    if (n) return n;
  }
  // Mesaj başında yalın numara: "30 prostatit etkeni", "4. birincil koruma" ("35 yaşında", "4. kuşak" hariç)
  const head = /^\s*(\d{1,3})\s*[.)]?\s+([\p{L}].*)$/u.exec(raw);
  if (head && !NON_QNO_AFTER.test(head[2].trim())) {
    const n = Number(head[1]);
    if (n >= 1 && n <= 200) return n;
  }
  // Mesaj sonunda virgül/noktalı virgülden sonra numara: "…, 14"
  const tail = check(/[,;]\s*(\d{1,3})\s*[.!?]*\s*$/.exec(raw), true, false);
  return tail;
}

/** Harfli şıklar: "A) koagülatif nekroz C) kazeöz", "b- kongo". Metin ham (öğrenci yazımı) kalır. */
export function letteredOptions(text: string): { harf: Letter; metin: string }[] {
  const out: { harf: Letter; metin: string }[] = [];
  const re = /(?:^|[\s,;(])([A-Ea-e])\s*[)\-:]\s*([^\n]+?)(?=(?:[\s,;]+[A-Ea-e]\s*[)\-:]\s)|\n|$)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text))) {
    const harf = m[1].toUpperCase() as Letter;
    const metin = m[2]
      .replace(/\s+(gerisini|gerisi|baska|başka|bi de|bir de|ben|galiba|sanırım|sanirim|cevap|cvp)\b.*$/i, '')
      .replace(/[,;.\s]+$/, '')
      .trim();
    if (!metin || metin.length > 120 || out.some((o) => o.harf === harf)) continue;
    out.push({ harf, metin });
  }
  return out;
}

const STEM_PRED_RE =
  /\b(hangisi|hangisidir|hangileri|hangisinde|hangi|nedir|ne\s+ad\b|ne\s+yap[ıi]l|soru|sorusu|sorul|sormu[sş]|sordu|diyordu|dedi|veriliyor|verilmi[sş]tir|a[sş]a[gğ][ıi]daki|a[sş]a[gğ][ıi]dakilerden|hastada|olguda|ya[sş][ıi]nda|beklenmez|yer\s+almaz|de[gğ]ildir|yanl[ıi][sş]t[ıi]r)\b/i;

/**
 * Harfsiz şık listeleri:
 * 1) Açık etiketli: "şıklarda X, Y, Z vardı", "seçenekler: X / Y",
 * 2) Soru kökü/fiili taşımayan, virgül ya da "/" ile ayrılmış 4–5 paralel seçenek dizisi ("[siklar]" mesajları),
 * 3) İkinci cümlede "X, Y, Z vardı / şıklardaydı" biçiminde hatırlanan seçenekler.
 */
export function unletteredOptions(text: string): string[] {
  const raw = String(text || '').trim();
  const parseList = (s: string, minItems = 2) => {
    const items = s
      .replace(/\s+(şıklarda\s+vardı|siklarda\s+vardi|şıkları\s+vardı|siklari\s+vardi|şıklardaydı|siklardaydi|vardı|vardi|vardı\s+galiba|falan|filan|gibi|felan|vb)[.!?,;\s]*$/i, '')
      .replace(/[.!?,;\s]+$/, '')
      .split(/\s*(?:,|\/|;)\s*/)
      .map((x) => x.trim())
      .filter((x) => x.length >= 2 && x.length <= 85 && x.split(/\s+/).length <= 9);
    return items.length >= minItems ? items.slice(0, 6) : [];
  };
  const m = /(?:şıklarda|siklarda|şıklar|siklar|seçenekler|secenekler|şıklarda da|siklarda da)\s*[:\-]?\s*([^\n.?!]+)/i.exec(raw);
  if (m) {
    const items = m[1]
      .replace(/\s+(vardı|vardi|vardı galiba|falan|filan|gibi|felan|vb)\b.*$/i, '')
      .split(/\s*(?:,|\/|;|\bve\b|\bile\b)\s*/i)
      .map((x) => x.trim())
      .filter((x) => x.length >= 2 && x.length <= 80);
    if (items.length) return items.slice(0, 6);
  }
  // Soru kökü fiili/soru sözcüğü olmayan yalın 4–6'lı virgül veya "/" listesi ("Glutaraldehit, alkol, formalin, bouin, zenker")
  if (!/\?/.test(raw) && !STEM_PRED_RE.test(raw) && !/\b(?:dedim|yaptım|yaptim|seçtim|sectim|işaretledim|isaretledim)\b/i.test(raw)) {
    const bare = parseList(raw, 4);
    if (bare.length >= 4 && bare.length <= 6) return bare;
  }
  // İkinci cümlede "X, Y, Z vardı" şık listesi ("... diye sordu. Reflü, nörojenik mesane, üretra darlığı vardı")
  const trail = /[.?]\s+([^.?!]+?\s+(?:şıklarda\s+vardı|siklarda\s+vardi|şıklardaydı|siklardaydi|vardı|vardi|geçiyordu|geciyordu))[.?!\s]*$/i.exec(raw);
  if (trail && !STEM_PRED_RE.test(trail[1])) {
    const sub = trail[1].replace(/\s+(?:ve|ile)\s+/gi, ', ');
    const items = parseList(sub, 3);
    if (items.length >= 3) return items;
  }
  return [];
}

export type RecallRole = 'stem' | 'mixed' | 'options' | 'claim';

/**
 * Birimin yapısal rolü:
 * - 'options': yalnız şıkları sıralayan mesaj (taslak kök olarak seçilmez; uydu olarak bağlanır)
 * - 'claim': yalnız işaretlenen cevabı söyleyen kısa iddia ("İmipramin A", "TSM dedim B", "I ve III B")
 * - 'mixed': hem soru kökünü hem şık/cevap yorumunu birlikte içeren mesaj
 * - 'stem': doğrudan soru kökünü/konusunu anlatan mesaj
 */
export function classifyRecallRole(text: string): RecallRole {
  const raw = String(text || '').trim();
  const f = fold(raw);
  const letOpts = letteredOptions(raw);
  if (letOpts.length >= 3) {
    const firstIdx = raw.search(/[A-Ea-e]\s*[)\-:]/);
    const before = firstIdx > 0 ? raw.slice(0, firstIdx) : '';
    const cw = words(before).filter((w) => !isStop(w) && (w.length >= 3 || VALID_SHORT_MED.has(w)));
    return cw.length >= 3 ? 'mixed' : 'options';
  }
  const unlet = unletteredOptions(raw);
  if (unlet.length >= 4 && !STEM_PRED_RE.test(raw)) return 'options';
  if (/^(?:şıklarda|siklarda|şıklar|siklar|seçenekler|secenekler)\b/i.test(raw)) return 'options';
  if (!/\?/.test(raw) && !STEM_PRED_RE.test(raw) && /\b(?:şıklarda|siklarda|şıkları|siklari|şıklar|siklar)(?:\s+vard[ıi])?\s*[.!?]*$/iu.test(raw)) {
    return 'options';
  }
  // Yalnız Romen rakamı / nicelik şıkları veya iddiası ("I ve III B", "yalnız I, yalnız III, hepsi", "hepsi doğru E")
  const contentToks = words(raw).filter((w) => !isStop(w) && !/^\d+$/.test(w) && (w.length >= 3 || VALID_SHORT_MED.has(w)));
  if (contentToks.length === 0) return unlet.length >= 3 ? 'options' : 'claim';
  const hasClaim = !!(claimedLetter(raw) || claimedText(raw));
  const hasStemMarker = STEM_PRED_RE.test(raw) || /\?/.test(raw);
  if (!hasStemMarker && hasClaim && contentToks.length <= 4) return 'claim';
  if (!hasStemMarker && contentToks.length <= 2 && /\b(?:kesin|dogru|yanlis|yanls|dedim|yaptim|sikki)\b/.test(f)) return 'claim';
  if (hasStemMarker && (unlet.length >= 2 || hasClaim || /\b(?:siklarda|sikki|celdirici|karistirdim|karisti|eledim|dusundum)\b/.test(f))) {
    return 'mixed';
  }
  return 'stem';
}

const NEGATIVE_RE =
  /\b(yanlistir|yanlis olan|yanlis olani|degildir|degil olan|hangisi degil|dgl|diil|beklenmez|beklenmeyen|gorulmez|gorulmeyen|haric|disinda|olamaz|bulunmaz|icermez|yer almaz|yer almayan|olmaz|olmayan|yoktur|uymayan|uymaz|ait olmayan|ozelliklerinden degil)\b/;

/** Olumsuz kök ihtimali (0–1). Öğrenciler "değildir"i sık atlar; işaret varsa yüksek, yoksa düşük. */
export function negativeLikelihood(text: string): number {
  const f = fold(text);
  if (NEGATIVE_RE.test(f)) return 0.8;
  if (/\byanlis\b/.test(f)) return 0.5;
  return 0.1;
}

/**
 * Çok sorulu mesajı birimlere böler ("bi de 30'da down sorusu vardı", "ayrıca farmada…", "X sorusu 85 ve Y sorusu", satır/";" ayrımı).
 * Parça ancak kendi içinde en az 2 içerik sözcüğü (veya 1 içerik sözcüğü + açık soru/numara belirteci) taşıyorsa ayrılır.
 */
export function splitRecall(text: string): string[] {
  const raw = String(text || '').trim();
  if (!raw) return [];
  const normalized = raw.replace(
    /(\b(?:soru|sorusu|srs|sru)(?:\s+\d{1,3})?|\b[\p{L}]{4,}\s+\d{1,3})\s+ve\s+(?=[^\n.;]*?\b(?:soru|sorusu|srs|sru)\b)/giu,
    '$1; ',
  );
  const parts = normalized
    .split(/\n+|;\s*|,?\s+(?=(?:bi\s*de|bir\s*de|bide|birde|ayrıca|ayrica|ayrca|bir\s+de\s+de|(?:öbür|obur|diğer|diger|başka\s+bir|baska\s+bir)\s+(?:soru|sorusu|sru|srs))\b)/i)
    .map((p) => p.trim())
    .filter(Boolean);
  if (parts.length < 2) return [raw];
  const content = (p: string) => {
    const cw = words(p).filter((w) => !isStop(w) && (w.length >= 3 || VALID_SHORT_MED.has(w)) && !/^(bide|birde|ayrica|ayrca|obur|diger|baska)$/.test(w));
    if (cw.length >= 2) return cw.length;
    if (cw.length === 1 && (/\b(soru|sorusu|srs|sru)\b/i.test(p) || questionNumber(p) !== null)) return 2;
    return cw.length;
  };
  const out: string[] = [];
  for (const p of parts) {
    if (out.length && content(p) < 2) out[out.length - 1] += ` ${p}`;
    else if (!out.length || content(out[out.length - 1]) >= 2) out.push(p);
    else out[out.length - 1] += ` ${p}`;
  }
  return out.length > 1 && out.every((p) => content(p) >= 2) ? out : [raw];
}

/** Okunur cümleden atılacak sohbet/üst söylem sözcükleri (soru sözcükleri — hangisi, değildir, mi — korunur). */
export const CHATTER = new Set(
  ('arkadaslar arkadaslarim arkadas agalar aga abi abla kanka olm lan aq amk yaw yav beyler millet gencler hocam hocalar ' +
    'ben bence sanirim galiba herhalde kesin kesinlikle eminim emin degilim bilmiyorum hatirlamiyorum hatirliyorum ' +
    'hatirlayan hatirlayamadim aklimda falan filan felan bisey biseyler yaptim yaptik yaptiniz dedim dedik dediniz ' +
    'isaretledim isaretledik sectim salladim napti naptiniz nptnz iptal itiraz zordu kolaydi sacma beynim yandi offf off tuh ' +
    'diyordu diyodu diyo dedi yaziyordu sormustu sormuslar sormus sorulmustu soruluyordu sordu soru sorusu sorusunu sorusunda sorudaki soruda srs srsu sru ' +
    'vardi vardiydi geciyordu miydi muydu mıydı neydi hoca hocanin slaytta derste dimi diye soruyordu soruyor isaretlemisim yazdim yazdım ya ' +
    'bedava kolay').split(' '),
);

const COMMENTARY_SENT_RE =
  /\b(dedim|yaptim|yazdim|sectim|isaretledim|dusundum|dusunuyorum|karistirdim|karisti|eledim|sandim|kaldim|celdirici|celdiriciydi|siklarda|siklardaydi|sikki|sikkini|sikta|seceneklerde|bence|sanirim|galiba|emin\s+degilim|aklimda\s+kaldi|geciyordu|kaliyordu|diyen\s+sik|yazan\s+sik)\b/;

/**
 * Çok cümleli veya "diye sordu / sorulmuştu" kalıplı öğrenci mesajından yalnız soru kökü cümlesini ayıklar;
 * arkadan gelen şık dökümü, çeldirici tartışması ("X ile karıştırdım", "X mi Y mi") ve cevap iddialarını keser.
 */
export function extractStemClause(text: string): string {
  let s = String(text || '').trim();
  if (!s) return '';
  // Yalnız şık listesi olan mesajlarda kesme yapma
  if (classifyRecallRole(s) === 'options') return s;

  // 1) Çok cümleli mesaj: ilk cümle soru kökü taşır ve sonraki cümle(ler) şık/iddia yorumuysa yalnız kök cümlelerini tut
  const sents = s
    .split(/(?<![\b\s](?:\d{1,3}|[IVX]{1,4}|[a-zA-Z]))[.!?]+\s+/u)
    .map((x) => x.trim())
    .filter(Boolean);
  if (sents.length >= 2) {
    const kept: string[] = [sents[0]];
    const firstFold = fold(sents[0]);
    const firstHasPred = STEM_PRED_RE.test(sents[0]) || /\b(en\s+s[iı]k|en\s+y[uü]ksek|hangisi|yanl[iı][sş]|de[gğ]il)\b/.test(firstFold);
    for (let i = 1; i < sents.length; i++) {
      const cur = sents[i];
      const cf = fold(cur);
      // Romen rakamlı öncüller ("I. ... II. ...") kökün parçasıdır
      if (/^[IVX]{1,4}[.)\s]/.test(cur)) { kept.push(cur); continue; }
      const isComm =
        COMMENTARY_SENT_RE.test(cf) ||
        /\bm[iıuü]\b.*\bm[iıuü]\b/.test(cf) ||
        /\bvard[iı]\s*$/.test(cf) ||
        (firstHasPred && !STEM_PRED_RE.test(cur));
      if (isComm) break;
      kept.push(cur);
    }
    s = kept.join('. ');
  }

  // 2) "... diye sordu / sormuştu / sorulmuştu / soruyordu / diyordu / dedi [,] <şık/iddia yorumu>"
  const repMatch = /^(.{12,}?)\s+(?:diye\s+)?(?:sordu|sormu[sş]tu|sorulmu[sş]tu|soruyordu|soruluyordu|diyordu|dedi)\b[,;:.]*\s+(.*)$/iu.exec(s);
  if (repMatch) {
    const before = repMatch[1].trim();
    const cw = words(before).filter((w) => !isStop(w) && (w.length >= 3 || VALID_SHORT_MED.has(w)));
    if (cw.length >= 2) s = before;
  }

  // 3) Kök soru yüklemiyle bittikten sonra virgülden sonra gelen ikili tahmin veya şık/iddia ("... hangisi, ecoli mi pseudomonas mi")
  const postInterrog = /^(.{10,}?\b(?:hangisi|hangisidir|hangileri|hangisinde|hangileri\s+do[gğ]rudur|yanl[ıi][sş]t[ıi]r|yanl[ıi][sş]\s+olan[ıi]?|yanl[ıi][sş]|do[gğ]ru\s+de[gğ]ildir|de[gğ]ildir|olmayan\s+hangisi|riski\s+en\s+y[uü]ksek(?:tir)?|en\s+s[ıi]k\s+hangisi(?:dir)?|nedir))\s*[,;]\s*(.+)$/iu.exec(s);
  if (postInterrog) {
    const before = postInterrog[1].trim();
    const cw = words(before).filter((w) => !isStop(w) && (w.length >= 3 || VALID_SHORT_MED.has(w)));
    if (cw.length >= 2) s = before;
  }

  // 4) Virgülden sonra veya kök belirtecinden sonra gelen açık iddia veya ikili şık tahmini ("..., juvenil polip dedim", "Piyuri sorusu losit esteraz dedim")
  s = s
    .replace(/,\s*[^,]+?\s+m[ıiuü]\s+[^,]+?\s+m[ıiuü](?:\s+diye\s+d[uü][sş][uü]nd[uü]m|\s+d[uü][sş][uü]nd[uü]m|\s+aras[ıi]nda\s+kald[ıi]m)?\s*[.!?]*$/iu, '')
    .replace(/,\s*(?:ben\s+|bence\s+)?[^,]{2,40}?\s+(?:dedim|yapt[ıi]m|se[cç]tim|i[sş]aretledim|gibi\s+duruyordu)(?:\s+ama\b.*)?\s*[.!?]*$/iu, '')
    .replace(/\b(soru|sorusu|srs|sru|ad[ıi]|hangisi|nedir)\s+(?:ben\s+|bence\s+)?(?:\S+\s+){1,3}(?:dedim|yapt[ıi]m|se[cç]tim|i[sş]aretledim)(?:\s+ama\b.*)?\s*[.!?]*$/iu, '$1')
    .replace(/\s+\b(?:soru|sorusu|srs|sru)\s+[^,.?]{2,30}\s+m[ıiuü]\s*[.!?]*$/iu, '')
    .replace(/^\s*(?:arkada[sş]lar\s+|hocam\s+|agalar\s+|beyler\s+)*(?:patolojide(?:\s+giri[sş]|\s+h[uü]cre\s+hasar[ıi]\s+k[ıi]sm[ıi]ndan)?|farmakolojide|farmada|mikrobiyolojide|mikroda|genetikte|biyokimyada|halk\s+sa[gğ]l[ıi][gğ][ıi]nda|dahiliyede|[uü]rolojide|n[oö]rolojide|pediatride|enfeksiyonda)\s+(?=(?:\S+\s+){2,})/iu, '');

  return s.trim();
}

/**
 * Öğrenci hatırlamasından okunur cümle: sohbet, cevap iddiası, şık yorumu ve soru numarası atılır; sözcük sırası korunur;
 * her sözcük `fix` ile (sözlük düzeltmesi + aksan) yazılır.
 */
export function cleanSentence(text: string, fix: (folded: string, raw: string) => string): string {
  const extracted = extractStemClause(text);
  let t = String(extracted || text || '')
    .replace(/\b\d{1,3}\s*(?:\.|'|’)?\s*(?:inci|ıncı|uncu|üncü|nci|ncı)?\s*(?:soru(?:su|daki|da|nun)?|sru|srsu|srs)\b/giu, ' ')
    .replace(/\b\d{1,3}\s*(?:'|’)?\s*(?:da|de|ta|te)(?:ki)?\b/giu, ' ')
    .replace(/\b(?:cevap|cevabı|cevabi|cvp|yanıt)\s*(?:[:=]\s*)?[A-Ea-e]\b(?!\s*[)\-:])/gu, ' ')
    .replace(/\b[A-Ea-e]\s*(?:şıkkı(?:ydı|dır)?|sikki(?:ydi)?)?\s*(?:yaptım|yaptim|dedim|işaretledim|isaretledim|seçtim|sectim)\b/giu, ' ')
    .replace(/(?:^|\s)[A-E]\s*[.!?]*\s*(?:mi|mı|mu)?\s*[.!?]*\s*$/u, ' ')
    .replace(/[!]+/g, ' ');
  const toks = t.split(/\s+/).filter(Boolean);
  const out: string[] = [];
  for (const tok of toks) {
    const m = /^([("'“]*)(.*?)([)"'”.,;:?]*)$/u.exec(tok)!;
    const core = m[2];
    if (!core) continue;
    const f = fold(core);
    if (!f) { out.push(tok); continue; }
    if (f.split(' ').every((x) => CHATTER.has(x))) continue;
    const keepRaw = /\d/.test(core) || /^[A-ZÇĞİÖŞÜ0-9]{2,}[a-zçğıöşü0-9-]*$/u.test(core) || /^[IVX]+$/.test(core);
    out.push(`${m[1]}${keepRaw ? core : fix(f, core)}${m[3].replace(/[.;:]+$/, m[3].includes('?') ? '?' : '')}`);
  }
  let s = out.join(' ').replace(/\s+([,?])/g, '$1').replace(/,+/g, ',').replace(/^[,\s]+|[,\s]+$/g, '').trim();
  if (!s) return '';
  // Soru kökü dilbilgisel tamamlaması (şıklardan oluşan dizilere dokunulmaz)
  if (classifyRecallRole(text) !== 'options') {
    s = s
      .replace(/\bhangisi\s+yanl[ıi][sş](?:t[ıi]r)?\??$/iu, 'aşağıdakilerden hangisi yanlıştır?')
      .replace(/\byanl[ıi][sş]\s+olan[ıi]?(?:\s+hangisi(?:dir)?)?\??$/iu, 'aşağıdakilerden hangisi yanlıştır?')
      .replace(/\bdo[gğ]ru\s+olmayan(?:\s+ifade)?(?:\s+hangisi(?:dir)?)?\??$/iu, 'aşağıdakilerden hangisi doğru değildir?')
      .replace(/\bhangisi\s+do[gğ]ru\s+de[gğ]il(?:dir)?\??$/iu, 'aşağıdakilerden hangisi doğru değildir?')
      .replace(/\bolmayan\s+hangisi(?:dir)?\??$/iu, 'değildir?')
      .replace(/\bhangisi\s+de[gğ]il(?:dir)?\??$/iu, 'değildir?');
    if (/\bde[gğ]ildir\??$/iu.test(s) && !/\b(?:hangisi|hangisidir|aşağıdaki|aşağıdakilerden)\b/iu.test(s)) {
      s = `Aşağıdakilerden hangisi ${s.charAt(0).toLocaleLowerCase('tr')}${s.slice(1)}`;
    } else if (/\bhangisi\??$/iu.test(s) && !/\başağıdaki/iu.test(s)) {
      s = s.replace(/\bhangisi\??$/iu, 'aşağıdakilerden hangisidir?');
    }
  }
  s = s.charAt(0).toLocaleUpperCase('tr') + s.slice(1);
  if (!/[?.]$/.test(s)) s += /\b(hangisi|hangisidir|nedir|ne|nelerdir|hangileri|hangisinde|değildir|yanlıştır|beklenmez|almaz|mi|mı|mu|mü|midir|mıdır)\b/i.test(s) ? '?' : '';
  return s;
}

