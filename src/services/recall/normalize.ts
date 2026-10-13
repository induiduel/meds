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
    // işlev sözcükleri
    'a b c d e ve veya ile ya da de ki mi mu mı mü mii miydi muydu mıydı müydü midir mudur bu su o bir iki uc ' +
    'icin gibi kadar daha en cok az her hic hep tum butun bazi baska diger sonra once ise ama fakat yani ' +
    'olan olarak olur olmaz oldu olmus olup olmasi olmayan olabilir olmali var yok vardi yoktu degil degildir dgl diil ' +
    'hangisi hangisidir hangi asagidakilerden asagidaki asagidakiler seklinde sekilde durum durumda ' +
    'nedir neydi ne nasil neden niye kim kimin nerede ' +
    // sınav üst dili
    'soru sorusu sorusunu sorusunda sorudaki soruda sorulari sorular sorunun srs srsu sorudu sorulmus sormus sormustu ' +
    'sik sikki sikkiydi sikki siklarda siklar siklari sikkini cevap cevabi cevapti cvp yanit dogru yanlis yanlistir ' +
    'secenek secenekler kok koku ilk son sinav sinavda sinavin kurul komite ders derste hoca hocam hocanin hocalar slayt slaytta ' +
    'pato patoloji farma farmako farmakoloji mikro mikrobiyoloji biyokimya genetik ' +
    // sohbet / argo
    'arkadaslar arkadaslarim arkadas agalar aga abi abla kanka olm lan aq amk yaw ya yav be beyler millet gencler hocalar ' +
    'ben sen biz siz onlar bence sanirim galiba herhalde kesin kesinlikle emin eminim degilim bilmiyorum hatirlamiyorum ' +
    'hatirliyorum hatirlayan hatirlayamadim hatirladigim aklimda kalan aklimda kaldi falan filan sey bisey bi biseyler ' +
    'yaptim yaptik yaptiniz yapan yapti dedim dedik dediniz isaretledim isaretledik sectim salladim sallayan napti naptiniz nptnz ' +
    'iptal itiraz iptali zor kolay zordu kolaydi sacma sacmaydi gicik yandi beynim offf off tuh insafsiz kim ne zaman ' +
    'diyordu diyodu diyor dedi yaziyordu yazan yaziyor vardi mesela tabi tabii tamam evet hayir dimi di mi degil mi ' +
    'gerisini gerisi hatirlarsaniz yazin yazsin bilen bilgisi net lutfen acaba mis mus miymis muymus daki deki taki teki'
  ).split(' '),
);

/** Ekli biçimleri de kapsayan sohbet/sınav dili kökleri ("sorusunda", "hatırlayamadım", "işaretlemiştim"). */
const STOP_PREFIX = /^(gecmis|olsun|gelir|geldi|soru|sorus|srs|sru|anahtar|bitti|sukur|uzundu|agirdi|zordu|kolaydi|sikk|sıkk|cevab|cevap|cvp|hoca|arkadas|hatirl|hatrl|isaretl|yaptim|yaptin|yapmis|dedim|demist|dmst|salla|iptal|itiraz|sinav|snv|naptin|naber|nasil|sonuc|aciklan|bilmiyo|hatirlamiyo|hatirliyo|diyo|yaziyo|sanirim|galiba|emin)/;
export const isStop = (w: string) => STOP.has(w) || STOP_PREFIX.test(w);

/** Ders ipucu sözcükleri ("pato sorusu", "farmada") → ders adı parçası (sınıflayıcıya ön bilgi). */
export const DERS_HINT: [RegExp, RegExp][] = [
  [/^pato/, /patoloji/i], [/^farma/, /farmakoloji/i], [/^mikro/, /mikrobiyoloji/i], [/^genetik/, /genetik/i],
  [/^biyokim|^biyokm/, /biyokimya/i], [/^halk/, /halk sa/i], [/^enfeksiyon|^enfek/, /enfeksiyon/i], [/^dahili/, /iç hastalık/i],
  [/^uroloj/, /üroloji/i], [/^norolo/, /nöroloji/i], [/^psikiy/, /psikiyatri/i], [/^pediat|^cocuk/, /çocuk sağlığı/i],
  [/^kardiy/, /kardiyoloji/i], [/^gogus/, /göğüs/i], [/^kadin|^jinek/, /kadın hastalık/i], [/^ortoped/, /ortopedi/i],
];

/** Kısaltma ve argo açılımları (katlanmış). Yalnız tıbbi anlamı tartışmasız olanlar; "mi", "ab" gibi çok anlamlılar yok. */
export const ABBREV: Record<string, string> = {
  tbc: 'tuberkuloz', tb: 'tuberkuloz', hst: 'hastalik', hstlk: 'hastalik', hastaligi: 'hastaligi',
  sdr: 'sendromu', snd: 'sendromu', sendr: 'sendromu', dm: 'diyabet', ht: 'hipertansiyon', koah: 'koah',
  ihk: 'immunohistokimya', ihc: 'immunohistokimya', zn: 'ziehl', inh: 'inhibitor', ab: 'antikor',
  ecoli: 'escherichia', 'e.coli': 'escherichia', vit: 'vitamin', bnce: 'bence', dgl: 'degil', diil: 'degil', dğl: 'degil',
  olmz: 'olmaz', olr: 'olur', ypr: 'yapar', ypmz: 'yapmaz', yksk: 'yuksek', dsk: 'dusuk', artr: 'artar', azlr: 'azalir',
  enf: 'enfeksiyon', enfek: 'enfeksiyon', tdv: 'tedavi', tani: 'tani', bulg: 'bulgu',
};

/** Katlanmış metni sözcüklere ayırır; harf+rakam bitişiklerini ayırır ("pepsinojen1" → "pepsinojen 1"). */
export function words(text: string): string[] {
  return fold(text)
    .replace(/([a-z]{3,})(\d)/g, '$1 $2')
    .replace(/(\d)([a-z]{3,})/g, '$1 $2')
    .split(' ')
    .filter(Boolean);
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
    const t = said[1].split(' ').filter((w) => !STOP.has(w) && !/^(ben|bence|soru|sorusu|sorusunda|\d+)$/.test(w)).join(' ');
    if (t.length >= 3 && !LETTERS.has(t)) return t;
  }
  const m = /\b(?:cevap|cevabi|cvp|dogru cevap|dogrusu|yanit)\s+(?:da|de\s+)?([a-z][a-z0-9 ]{2,40}?)\s+(?:olmali|olacakti|olcakti|dogru|olmaliydi|idi|ydi|di|olur)\b/.exec(f);
  if (!m) return null;
  const t = m[1].trim();
  return t.length >= 3 && !LETTERS.has(t) ? t : null;
}

/** Soru numarası: "12. soru", "30'daki", "soru 7", "28 nolu". Yoksa null. */
export function questionNumber(text: string): number | null {
  const raw = String(text || '');
  const pats = [
    /\b(\d{1,3})\s*(?:\.|'|’)?\s*(?:inci|ıncı|uncu|üncü|nci|ncı|ncu|ncü)?\s*(?:soru|sorusu|sorudaki|soruda|sorunun|srs|srsu)\b/i,
    /\b(\d{1,3})\s*(?:'|’)?\s*(?:da|de|ta|te|daki|deki|taki|teki)\s+(?:ki\s+)?(?:\S+\s+){0,3}?(?:soru|sorusu|srs)/i,
    /\bsoru\s*(?:no|numarası|numarasi|#)?\s*[:.]?\s*(\d{1,3})\b/i,
    /\b(\d{1,3})\s*(?:nolu|numaralı|numarali)\b/i,
    /\b(\d{1,3})\s*(?:\.|'|’)?\s*(?:sru|srsu|srs)\b/i,
    // Mesaj başında ya da sonunda yalın numara: "30 prostatit etkeni", "4. birincil koruma", "…, 14"
    /^\s*(\d{1,3})\s*[.)]?\s+(?!(?:mg|g|gr|ml|mm|cm|kg|yas|yaş|yil|yıl|gun|gün|hafta|ay|saat|dk|hz|ünite|unite|ü|u|%|x|tane|adet|kez|kat|mmhg|ve|ile|-)\b)[\p{L}]/iu,
    /[,;]\s*(\d{1,3})\s*[.!?]*\s*$/,
    /\s(\d{1,3})\s*[.!?]*\s*$/,
  ];
  for (const p of pats) {
    const m = p.exec(raw);
    if (m) {
      const n = Number(m[1]);
      if (n >= 1 && n <= 200) return n;
    }
  }
  return null;
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

/** Harfsiz şık listeleri: "şıklarda X, Y, Z vardı", "seçenekler: X / Y". */
export function unletteredOptions(text: string): string[] {
  const m = /(?:şıklarda|siklarda|şıklar|siklar|seçenekler|secenekler|şıklarda da|siklarda da)\s*[:\-]?\s*([^\n.?!]+)/i.exec(text);
  if (!m) return [];
  return m[1]
    .replace(/\s+(vardı|vardi|vardı galiba|falan|filan|gibi|felan|vb)\b.*$/i, '')
    .split(/\s*(?:,|\/|;|\bve\b|\bile\b)\s*/i)
    .map((x) => x.trim())
    .filter((x) => x.length >= 3 && x.length <= 80)
    .slice(0, 6);
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
 * Çok sorulu mesajı birimlere böler ("bi de 30'da down sorusu vardı", "ayrıca farmada…", satır/";" ayrımı).
 * Parça ancak kendi içinde en az 2 içerik sözcüğü taşıyorsa ayrılır; aksi hâlde mesaj bütün kalır.
 */
export function splitRecall(text: string): string[] {
  const raw = String(text || '').trim();
  if (!raw) return [];
  const parts = raw
    .split(/\n+|;\s*|\s+(?=(?:bi\s*de|bir\s*de|bide|birde|ayrıca|ayrica|ayrca|bir\s+de\s+de|öbür|obur|diğer|diger|başka\s+bir|baska\s+bir)\b)/i)
    .map((p) => p.trim())
    .filter(Boolean);
  if (parts.length < 2) return [raw];
  const content = (p: string) => words(p).filter((w) => !isStop(w) && w.length >= 4 && !/^(bide|birde|ayrica|ayrca|obur|diger|baska)$/.test(w)).length;
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
    'diyordu diyodu diyo yaziyordu sormustu sormuslar sormus sorulmustu soru sorusu sorusunu sorusunda sorudaki soruda srs srsu sru ' +
    'vardi vardiydi miydi muydu mıydı neydi hoca hocanin slaytta derste dimi diye soruyordu soruyor isaretlemisim yazdim yazdım ya').split(' '),
);

/**
 * Öğrenci hatırlamasından okunur cümle: sohbet, cevap iddiası ve soru numarası atılır; sözcük sırası korunur;
 * her sözcük `fix` ile (sözlük düzeltmesi + aksan) yazılır. Bilgi EKLENMEZ.
 */
export function cleanSentence(text: string, fix: (folded: string, raw: string) => string): string {
  let t = String(text || '')
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
  s = s.charAt(0).toLocaleUpperCase('tr') + s.slice(1);
  if (!/[?.]$/.test(s)) s += /\b(hangisi|hangisidir|nedir|ne|nelerdir|hangileri|mi|mı|mu|mü|midir|mıdır)\b/i.test(s) ? '?' : '';
  return s;
}
