/**
 * Sorgu zekâsı çekirdeği — sunucu ve tarayıcıda ortak (Node API'si yok).
 *
 * Türkçe katlama, sözcük bölme, sınırlı Damerau-Levenshtein, 32-bit FNV özeti, SymSpell silme anahtarları,
 * Türkçe Q klavye komşuluğu, niyet (hastalık bölümü) sözlüğü ve çok sözcüklü kavram eşleyici burada.
 * Tüm fonksiyonlar ayırma (allocation) en aza indirilerek yazıldı: öneri ucu her tuş vuruşunda çağrılır.
 */

const FOLD: Record<string, string> = {
  ç: 'c', ğ: 'g', ı: 'i', ö: 'o', ş: 's', ü: 'u', ș: 's', ț: 't', ţ: 't', â: 'a', î: 'i', û: 'u', é: 'e', ä: 'a', ë: 'e', è: 'e', á: 'a', í: 'i', ó: 'o', ú: 'u',
};

/** Küçük harf (tr) + aksan katlama. "Böbreğİ" → "bobregi". Uzunluk korunmaz garantisi yok; vurgulama için searchText.foldText kullanılır. */
export function fold(s: string): string {
  const low = s.toLocaleLowerCase('tr-TR');
  let out = '';
  for (let i = 0; i < low.length; i++) {
    const ch = low[i];
    const code = ch.charCodeAt(0);
    if (code < 128) { out += ch; continue; }
    if (code === 0x307) continue; // birleşik nokta (İ → i̇)
    out += FOLD[ch] ?? ch;
  }
  return out;
}

export const TR_CHARS = /[çğıöşüÇĞİÖŞÜ]/;

export interface WordSpan {
  /** Özgün yazım */
  w: string;
  /** Katlanmış */
  f: string;
  s: number;
  e: number;
  /** Kesme işaretinden sonra gelen ek ("Wilms'in" → "in"): düzeltilmez, kavram aranmaz */
  suffix: boolean;
}

const WORD_RE = /[\p{L}\p{N}]+/gu;

export function splitWords(text: string): WordSpan[] {
  const out: WordSpan[] = [];
  WORD_RE.lastIndex = 0;
  let m: RegExpExecArray | null;
  while ((m = WORD_RE.exec(text))) {
    const prev = m.index > 0 ? text[m.index - 1] : '';
    out.push({ w: m[0], f: fold(m[0]), s: m.index, e: m.index + m[0].length, suffix: prev === "'" || prev === '’' });
  }
  return out;
}

/** 32-bit FNV-1a */
export function fnv1a(s: string): number {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return h >>> 0;
}

/** SymSpell önek uzunluğu: anahtarlar yalnız ilk 8 harften üretilir (bellek sabit kalır). */
export const SYM_PREFIX = 8;

/** Sözcüğün (önekinin) kendisi + tek harf silinmiş biçimleri. Dizinde ve sorguda aynı fonksiyon kullanılır. */
export function deleteKeys(word: string, out: Set<string> = new Set()): Set<string> {
  const p = word.length > SYM_PREFIX ? word.slice(0, SYM_PREFIX) : word;
  out.add(p);
  if (p.length > 1) for (let i = 0; i < p.length; i++) out.add(p.slice(0, i) + p.slice(i + 1));
  return out;
}

let rowA = new Int32Array(64);
let rowB = new Int32Array(64);
let rowC = new Int32Array(64);

/**
 * Sınırlı OSA Damerau-Levenshtein. Mesafe `max`'ı aşarsa `max + 1` döner (erken çıkış).
 * Bitişik yer değiştirme ("kayrotip" ↔ "karyotip") tek işlem sayılır.
 */
export function editDistance(a: string, b: string, max = 2): number {
  if (a === b) return 0;
  const al = a.length;
  const bl = b.length;
  if (Math.abs(al - bl) > max) return max + 1;
  if (al === 0) return bl;
  if (bl === 0) return al;
  if (bl + 1 > rowA.length) {
    rowA = new Int32Array(bl + 1); rowB = new Int32Array(bl + 1); rowC = new Int32Array(bl + 1);
  }
  let prev2 = rowA; let prev = rowB; let cur = rowC;
  for (let j = 0; j <= bl; j++) prev[j] = j;
  for (let i = 1; i <= al; i++) {
    cur[0] = i;
    let rowMin = i;
    const ac = a.charCodeAt(i - 1);
    for (let j = 1; j <= bl; j++) {
      const bc = b.charCodeAt(j - 1);
      const cost = ac === bc ? 0 : 1;
      let v = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
      if (i > 1 && j > 1 && ac === b.charCodeAt(j - 2) && a.charCodeAt(i - 2) === bc) v = Math.min(v, prev2[j - 2] + 1);
      cur[j] = v;
      if (v < rowMin) rowMin = v;
    }
    if (rowMin > max) return max + 1;
    const t = prev2; prev2 = prev; prev = cur; cur = t;
  }
  const d = prev[bl];
  return d > max ? max + 1 : d;
}

/** Türkçe Q klavye: komşu tuş hatası ("brbrek" ← "böbrek" değil ama "nefritik" ← "nefrotik" yakın) daha olası. */
const KEY_ROWS = ['qwertyuıopğü', 'asdfghjklşi', 'zxcvbnmöç'];
const KEY_POS = new Map<string, [number, number]>();
KEY_ROWS.forEach((row, r) => { for (let c = 0; c < row.length; c++) KEY_POS.set(fold(row[c]), [r, c + r * 0.5]); });

export function keysAdjacent(x: string, y: string): boolean {
  const a = KEY_POS.get(x);
  const b = KEY_POS.get(y);
  if (!a || !b) return false;
  return Math.abs(a[0] - b[0]) <= 1 && Math.abs(a[1] - b[1]) <= 1;
}

/** Tek ikame farkı komşu tuştan mı? (aynı uzunluk, tek fark) */
export function isAdjacentTypo(typed: string, cand: string): boolean {
  if (typed.length !== cand.length) return false;
  let diff = -1;
  for (let i = 0; i < typed.length; i++) {
    if (typed[i] !== cand[i]) {
      if (diff >= 0) return false;
      diff = i;
    }
  }
  return diff >= 0 && keysAdjacent(typed[diff], cand[diff]);
}

export function commonPrefix(a: string, b: string): number {
  let i = 0;
  while (i < a.length && i < b.length && a.charCodeAt(i) === b.charCodeAt(i)) i++;
  return i;
}

/** Sorgu niyeti → Hastalıklar sayfası bölümü (DiseaseSectionKey ile aynı adlar). */
export type IntentKey = 'treatment' | 'diagnosis' | 'imaging' | 'symptoms' | 'etiology' | 'pathology' | 'physiology' | 'epidemiology' | 'pathognomonic';

/**
 * Kanıt cümlesi ipuçları (hastalık grafiği): katlanmış cümlede sözcük başında geçen kök → bölüm puanı.
 * Genel sözcükler ("hücre", "klinik", "test") bilerek yok: her cümlede geçip sınıflamayı bulandırıyorlar.
 */
export const EVIDENCE_CUES: Array<{ k: IntentKey; stems: string[]; w: number }> = [
  { k: 'treatment', w: 3, stems: ['tedavi', 'ilk tercih', 'secilecek ilac', 'kullanilan ilac', 'rezeksiyon', 'nefrektomi', 'kemoterapi', 'radyoterapi', 'cerrahi', 'eksizyon', 'transplant', 'replasman', 'profilaksi', 'antibiyoterapi', 'steroid tedavi', 'kortikosteroid', 'diyaliz'] },
  { k: 'diagnosis', w: 3, stems: ['tani', 'tanida', 'tanisi', 'teshis', 'biyopsi', 'laboratuvar', 'serolojik', 'tarama test', 'belirtec', 'idrar tetkik', 'kultur', 'elisa', 'pcr', 'tani koy', 'tanisal'] },
  { k: 'imaging', w: 3, stems: ['goruntule', 'ultrason', 'usg', 'tomografi', 'manyetik rezonans', 'mrg', 'grafi', 'radyolojik', 'sintigrafi', 'anjiyografi', 'ekokardiyografi', 'doppler'] },
  { k: 'symptoms', w: 2, stems: ['belirti', 'bulgu', 'semptom', 'sikayet', 'prezentasyon', 'ile basvur', 'klinik tablo', 'klinik olarak', 'hematuri', 'proteinuri', 'oligouri', 'poliuri'] },
  { k: 'etiology', w: 2, stems: ['etiyoloji', 'nedeni', 'nedenleri', 'nedenidir', 'sebep', 'risk faktor', 'predispoz', 'mutasyon', 'kalitim', 'yol acar', 'neden olur'] },
  { k: 'pathology', w: 2, stems: ['patoloji', 'histoloji', 'histopatoloji', 'morfoloji', 'mikroskop', 'makroskop', 'boyanma', 'immunohistokimya', 'immunfloresan', 'elektron mikroskop', 'granulom', 'nekroz', 'infiltrasyon', 'proliferasyon'] },
  { k: 'physiology', w: 2, stems: ['mekanizma', 'patogenez', 'fizyopatoloji', 'patofizyoloji', 'aracili', 'aktivasyon', 'birikim', 'hasar olusur'] },
  { k: 'epidemiology', w: 1, stems: ['en sik', 'sikligi', 'insidans', 'prevalans', 'epidemiyoloji', 'yasta', 'cocukluk cag', 'eriskinlerde', 'gorulme'] },
  { k: 'pathognomonic', w: 3, stems: ['patognomonik', 'tipik', 'karakteristik', 'ayirici tani', 'klasik triad', 'ozgul', 'spesifik'] },
];

/** Katlanmış cümle → bölüm puanları (yalnız sözcük başı eşleşmeleri sayılır). */
export function classifyEvidence(foldedSentence: string): Array<[IntentKey, number]> {
  const text = ` ${foldedSentence.replace(/[^a-z0-9]+/g, ' ')} `;
  const out: Array<[IntentKey, number]> = [];
  for (const cue of EVIDENCE_CUES) {
    let sc = 0;
    for (const st of cue.stems) if (text.includes(` ${st}`)) sc += cue.w;
    if (sc > 0) out.push([cue.k, sc]);
  }
  return out.sort((a, b) => b[1] - a[1]);
}

/**
 * Sorgu niyeti: yalnız açık soru sözcükleri ("tedavisi", "tanısı", "belirtileri", "patogenezi" …).
 * Dönen `words`: niyet sözcüklerinin dizinleri — kavram araması bunları içermez.
 */
const QUERY_INTENT: Array<{ k: IntentKey; re: RegExp }> = [
  { k: 'treatment', re: /^(tedavi|tedavisi|tedavisinde|tedavide|tedavileri|tedavinin|tedaviye)$/ },
  { k: 'diagnosis', re: /^(tani|tanisi|tanida|tanisinda|tanilari|taniya|tanisal|teshis|teshisi)$/ },
  { k: 'imaging', re: /^(goruntuleme|goruntulemesi|goruntulemede|radyoloji|radyolojisi|radyolojik)$/ },
  { k: 'symptoms', re: /^(belirti|belirtisi|belirtileri|bulgu|bulgusu|bulgulari|semptom|semptomu|semptomlari|klinigi)$/ },
  { k: 'etiology', re: /^(etiyoloji|etiyolojisi|nedeni|nedenleri|sebebi|sebepleri)$/ },
  { k: 'pathology', re: /^(patoloji|patolojisi|histoloji|histolojisi|histopatoloji|histopatolojisi|morfoloji|morfolojisi|mikroskobisi)$/ },
  { k: 'physiology', re: /^(patogenez|patogenezi|mekanizma|mekanizmasi|fizyopatoloji|fizyopatolojisi|patofizyoloji|patofizyolojisi)$/ },
  { k: 'epidemiology', re: /^(epidemiyoloji|epidemiyolojisi|sikligi|insidans|insidansi|prevalans|prevalansi)$/ },
  { k: 'pathognomonic', re: /^(patognomonik|ayirici)$/ },
];

export function detectIntent(foldedWords: string[]): { intent: IntentKey | null; words: Set<number> } {
  const used = new Set<number>();
  let best: IntentKey | null = null;
  for (let i = 0; i < foldedWords.length; i++) {
    const w = foldedWords[i];
    for (const q of QUERY_INTENT) {
      if (!q.re.test(w)) continue;
      used.add(i);
      if (!best) best = q.k;
      // "ayırıcı tanı" iki sözcük: ikincisi de niyet sözcüğü
      if (q.k === 'pathognomonic' && foldedWords[i + 1]?.startsWith('tani')) used.add(i + 1);
      break;
    }
  }
  return { intent: best, words: used };
}

/** Kavram türleri (sözlük kategorileri tek isim kümesine indirgenir). */
export type ConceptType = 'disease' | 'drug' | 'gene' | 'symptom' | 'anatomy' | 'pathogen' | 'procedure' | 'term' | 'topic';

export interface ConceptRef {
  kind: 'disease' | 'glossary' | 'term' | 'topic';
  id: string;
}

/** Paketlenmiş kavram: [etiket, tür, ref(kind:id veya ''), ağırlık, takma adlar, branş, güçlü takma ad bayrakları] */
export type PackedConcept = [string, ConceptType, string, number, string[], string, number];

export interface Concept {
  label: string;
  type: ConceptType;
  ref: ConceptRef | null;
  weight: number;
  aliases: string[];
  discipline: string;
  /** i. bit: aliases[i] sorgu yeniden yazımında kullanılabilir (küratörlü/eşanlamlı) */
  strongMask: number;
}

export function unpackConcept(p: PackedConcept): Concept {
  const [label, type, ref, weight, aliases, discipline, strongMask] = p;
  let r: ConceptRef | null = null;
  if (ref) {
    const i = ref.indexOf(':');
    r = { kind: ref.slice(0, i) as ConceptRef['kind'], id: ref.slice(i + 1) };
  }
  return { label, type, ref: r, weight, aliases, discipline, strongMask };
}

// ------------------------------------------------------------------ Türkçe ad çekimi (hafif)

/** Katlanmış sözcükten yaygın ad eklerini atar (çoğul, iyelik, tamlayan, durum). Kök ≥ 4 harf kalır. */
const NOUN_SUFFIXES = [
  'larindaki', 'lerindeki', 'larinin', 'lerinin', 'larina', 'lerine', 'larini', 'lerini', 'larinda', 'lerinde', 'larindan', 'lerinden',
  'lari', 'leri', 'larda', 'lerde', 'lardan', 'lerden', 'lar', 'ler', 'sinin', 'sunun', 'inin', 'unun', 'nin', 'nun', 'sinde', 'sunda',
  'sine', 'suna', 'sini', 'sunu', 'inde', 'unda', 'ine', 'una', 'ini', 'unu', 'dir', 'dur', 'tir', 'tur', 'si', 'su', 'da', 'de', 'ta', 'te', 'i', 'u', 'a', 'e',
];

export function lemma(f: string): string {
  for (const suf of NOUN_SUFFIXES) {
    // tek ünlülük ek yalnız uzun sözcükte (anemi ≠ anem + i)
    if (f.length - suf.length >= (suf.length === 1 ? 5 : 4) && f.endsWith(suf)) {
      let root = f.slice(0, f.length - suf.length);
      // ünsüz yumuşaması geri: böbreği → böbrek, kalbi → kalp
      if (/[aeiou]$/.test(suf) || suf.length > 1) {
        if (root.endsWith('g') && !root.endsWith('ng')) root = root.slice(0, -1) + 'k';
        else if (root.endsWith('b')) root = root.slice(0, -1) + 'p';
      }
      return root;
    }
  }
  return f;
}

/** Ek → büyük ünlü/ünsüz sınıfı ("ü" → "I", "si" → "I", "leri" → "lArI"): eki farklı köke taşımak için karşılaştırma anahtarı */
export function suffixClass(suf: string): string {
  return suf.replace(/^[sny](?=[aeiouıöü])/, '').replace(/[ıiuü]/g, 'I').replace(/[ae]/g, 'A').replace(/[dt](?=A)/g, 'D');
}

/**
 * Çok sözcüklü kavram eşleyici. Anahtar: katlanmış sözcüklerin boşlukla birleşimi.
 * Türkçe ek toleransı: son sözcük için kesme (≤4 harf, kök ≥4) ve k↔ğ yumuşaması denenir
 * ("nefrotik sendromu" → "nefrotik sendrom", "böbreği" → "böbrek").
 */
export class PhraseMatcher {
  private map = new Map<string, number[]>();
  /** İfadelerin ilk sözcükleri: taramada bu kümede (ya da ek kesilmiş hâli bu kümede) olmayan sözcük atlanır */
  private firsts = new Set<string>();
  maxWords = 1;

  add(phrase: string, id: number): void {
    const key = splitWords(phrase).map((x) => x.f).join(' ');
    if (!key || key.length < 2) return;
    const parts = key.split(' ');
    if (parts.length > 6) return;
    if (parts.length > this.maxWords) this.maxWords = parts.length;
    this.firsts.add(parts[0]);
    this.put(key, id);
    // Sözlük tarafında da ek toleransı: son sözcüğün kökü ("böbrek tümörleri" → "böbrek tümör"), böylece
    // sorgudaki farklı ek ("böbrek tümörü") aynı tamlamaya varır ve en uzun eşleşme tamlamanın kendisi olur.
    const last = parts[parts.length - 1];
    const lem = lemma(last);
    if (lem !== last) {
      parts[parts.length - 1] = lem;
      this.put(parts.join(' '), id);
      if (parts.length === 1) this.firsts.add(lem);
    }
  }

  private put(key: string, id: number): void {
    const cur = this.map.get(key);
    if (!cur) this.map.set(key, [id]);
    else if (!cur.includes(id)) cur.push(id);
  }

  get(key: string): number[] | undefined {
    return this.map.get(key);
  }

  get size(): number {
    return this.map.size;
  }

  /** Son sözcüğe ek toleranslı arama */
  lookupInflected(head: string, last: string): { ids: number[]; exact: boolean } | null {
    const pre = head ? `${head} ` : '';
    const exact = this.map.get(pre + last);
    if (exact) return { ids: exact, exact: true };
    if (last.length < 5) return null;
    for (let cut = 1; cut <= 4 && last.length - cut >= 4; cut++) {
      const stem = last.slice(0, last.length - cut);
      const hit = this.map.get(pre + stem);
      if (hit) return { ids: hit, exact: false };
      if (stem.endsWith('g')) {
        const soft = this.map.get(pre + stem.slice(0, -1) + 'k');
        if (soft) return { ids: soft, exact: false };
      }
      if (stem.endsWith('b')) {
        const soft = this.map.get(pre + stem.slice(0, -1) + 'p');
        if (soft) return { ids: soft, exact: false };
      }
    }
    return null;
  }

  private canStart(f: string): boolean {
    if (this.firsts.has(f)) return true;
    if (f.length < 5) return false;
    for (let cut = 1; cut <= 4 && f.length - cut >= 4; cut++) {
      const st = f.slice(0, f.length - cut);
      if (this.firsts.has(st)) return true;
      const last = st[st.length - 1];
      if ((last === 'g' && this.firsts.has(st.slice(0, -1) + 'k')) || (last === 'b' && this.firsts.has(st.slice(0, -1) + 'p'))) return true;
    }
    return false;
  }

  /**
   * Metindeki en uzun kavram eşleşmeleri (soldan sağa, açgözlü, örtüşmesiz).
   * words: splitWords çıktısı. Dönen: [başlangıç sözcük, bitiş sözcük (dahil değil), kavram id'leri, tam mı]
   */
  scan(words: WordSpan[], maxWords = this.maxWords): Array<{ from: number; to: number; ids: number[]; exact: boolean }> {
    const out: Array<{ from: number; to: number; ids: number[]; exact: boolean }> = [];
    let i = 0;
    while (i < words.length) {
      if (!this.canStart(words[i].f)) { i++; continue; }
      let found: { from: number; to: number; ids: number[]; exact: boolean } | null = null;
      const lim = Math.min(maxWords, words.length - i);
      for (let n = lim; n >= 1; n--) {
        let head = '';
        for (let j = i; j < i + n - 1; j++) head += (head ? ' ' : '') + words[j].f;
        const hit = this.lookupInflected(head, words[i + n - 1].f);
        if (hit) { found = { from: i, to: i + n, ids: hit.ids, exact: hit.exact }; break; }
      }
      if (found) { out.push(found); i = found.to; } else i++;
    }
    return out;
  }
}

/**
 * Sözcük düzeyi eşdeğerlik kümeleri (tamlama başı / niteleyici). Kavram eşanlamlılığından farklıdır:
 * "böbrek tümörü" içinde "tümör" bir kavram değil, tamlamanın başıdır — yerine "Neoplazi" konmaz,
 * arama yuvası {tümör, neoplazm, neoplazi} olarak genişletilir. Organ sıfatları da böyle: böbrek ≡ renal.
 */
export const WORD_EQUIV: string[][] = [
  ['tümör', 'neoplazm', 'neoplazi'],
  ['böbrek', 'renal'], ['karaciğer', 'hepatik'], ['akciğer', 'pulmoner'], ['kalp', 'kardiyak'], ['beyin', 'serebral'],
  ['mide', 'gastrik'], ['bağırsak', 'intestinal'], ['deri', 'kutanöz'], ['damar', 'vasküler'], ['idrar', 'üriner'],
  ['böbreküstü', 'adrenal'], ['rahim', 'uterus', 'uterin'], ['yumurtalık', 'over', 'ovaryen'], ['kemik', 'osseöz'],
  ['kansızlık', 'anemi'], ['ishal', 'diyare'], ['kabızlık', 'konstipasyon'], ['kaşıntı', 'pruritus'], ['sarılık', 'ikter'],
  ['iltihap', 'inflamasyon'], ['enfarktüs', 'infarkt'], ['ödem', 'şişlik'],
];
