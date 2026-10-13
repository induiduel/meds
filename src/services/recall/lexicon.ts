/**
 * Sözlük ve yazım düzeltici (soru havuzu motoru).
 *
 * Kaynak: çıkmış soru bankası (kök + şıklar) + tıbbi sözlük + hastalık listesi. Katlanmış sözcük → sıklık ve en sık
 * görülen aksanlı yazım. Düzeltme simetrik silme (SymSpell benzeri) ile: bir harf eksik/fazla/yanlış/yer değiştirmiş
 * yazımlar (uzun sözcükte iki) sözlükteki en yakın ve en sık sözcüğe çekilir. Türkçe ekli biçimler için kök + ek
 * ayrılarak yeniden denenir ("gstritte" → "gastrit" + "te").
 *
 * Tıbbi terim dizini: sözlük + hastalık adları (çok sözcüklü, en uzun eşleşme önce), düzeltilmiş sözcükler üzerinde.
 */
import { fold, ABBREV, STOP, isStop } from './normalize.ts';

export interface Lexicon {
  size: number;
  freq: (w: string) => number;
  /** Katlanmış sözcüğün aksanlı görünümü ("gastrit" → "gastrit", "otoimmun" → "otoimmün"). */
  display: (w: string) => string;
  /** Katlanmış sözcüğü düzeltir; düzeltme yoksa kendisi. */
  correct: (w: string) => string;
}

const SUFFIXES = [
  'larindaki', 'lerindeki', 'larinda', 'lerinde', 'larin', 'lerin', 'lari', 'leri', 'lardan', 'lerden', 'larda', 'lerde',
  'lar', 'ler', 'ndaki', 'ndeki', 'daki', 'deki', 'taki', 'teki', 'nda', 'nde', 'dan', 'den', 'tan', 'ten',
  'nin', 'nun', 'in', 'un', 'da', 'de', 'ta', 'te', 'yla', 'yle', 'la', 'le', 'si', 'su', 'i', 'u', 'e', 'a',
];

function damerau(a: string, b: string, max: number): number {
  if (Math.abs(a.length - b.length) > max) return max + 1;
  const n = a.length, m = b.length;
  let prev2 = new Array(m + 1).fill(0);
  let prev = Array.from({ length: m + 1 }, (_, j) => j);
  let cur = new Array(m + 1).fill(0);
  for (let i = 1; i <= n; i++) {
    cur[0] = i;
    let rowMin = cur[0];
    for (let j = 1; j <= m; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      let v = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) v = Math.min(v, prev2[j - 2] + 1);
      cur[j] = v;
      if (v < rowMin) rowMin = v;
    }
    if (rowMin > max) return max + 1;
    [prev2, prev, cur] = [prev, cur, prev2];
  }
  return prev[m];
}

const VOWELS = /[aeiou]/g;
const skeleton = (w: string) => w[0] + w.slice(1).replace(VOWELS, '').replace(/(.)\1+/g, '$1');

const deletes1 = (w: string) => {
  const out = new Set<string>();
  for (let i = 0; i < w.length; i++) out.add(w.slice(0, i) + w.slice(i + 1));
  return out;
};

/** Bankada az geçen gündelik sözcükler: düzeltme hedefi değil, bilinen sözcük ("buldu" → "bulgu" olmasın). */
export const COMMON_TR_LIST = (
  'buldu bulmus bulamadim bitti biter bitmedi sonunda sukur kimse herkes hepsi hepimiz geldi gelmis gitti gitmis aldim aldi ' +
  'verdi vermis cikti cikmis girdi girmis yazdi yazmis okudu okumus sordu sormus dedi demis gordu gormus bildi bilmis ' +
  'oldu olmus kaldi kalmis dustu dusmus sectim secti biliyor bilmiyor istiyor yapiyor geliyor gidiyor ' +
  'uzun kisa buyuk kucuk yeni eski guzel kotu iyi zor kolay agir hafif hizli yavas erken gec ' +
  'bugun yarin dun simdi sonra once hemen zaten tekrar yine bile sadece yalnizca belki aslinda ' +
  'sabah aksam gece hafta saat dakika saniye yil ay gun ' +
  'nasildi nasil neden niye cunku ama fakat ancak ayrica hatta oysa yoksa ' +
  'tane adet kez kere kisim kismi kisminda bolum bolumu yer yerde yeri sey seyi seyler ' +
  'anlat anlatti anladim anlamadim dusundum dusunuyorum sanmistim inandim diye diyen soruyordu soruyor yardim isaretlemisim'
).split(' ');

export const COMMON_TR = new Set(COMMON_TR_LIST);

/** Ham metinlerden sözlük kurar. `extra` (sözlük/hastalık terimleri) en az 3 sıklıkla eklenir. */
/** Olay döngüsünü kilitlememek için ~8 ms'de bir sıra verir (sunucuda motor kurulumu dilimli yapılır). */
export function makeTicker(budgetMs = 8) {
  let t = Date.now();
  return async () => {
    if (Date.now() - t < budgetMs) return;
    await new Promise((r) => setImmediate(r));
    t = Date.now();
  };
}

export async function buildLexicon(texts: Iterable<string>, extra: Iterable<string> = [], tick = makeTicker()): Promise<Lexicon> {
  const freq = new Map<string, number>();
  const forms = new Map<string, Map<string, number>>();
  const addWord = (raw: string, n = 1) => {
    // Kısaltmalar (INR, MALT, PKOS) büyük harfle görünür; "ınr" olmasın
    const lower = raw.length >= 2 && raw.length <= 6 && /^[A-ZÇĞİÖŞÜ0-9]+$/.test(raw) && /[A-Z]/.test(raw) ? raw : raw.toLocaleLowerCase('tr');
    const f = fold(lower);
    if (!f || f.includes(' ') || f.length < 2) return;
    freq.set(f, (freq.get(f) || 0) + n);
    let fm = forms.get(f);
    if (!fm) forms.set(f, (fm = new Map()));
    fm.set(lower, (fm.get(lower) || 0) + n);
  };
  const re = /[\p{L}][\p{L}\p{N}]*/gu;
  let n0 = 0;
  for (const t of texts) {
    for (const m of String(t || '').matchAll(re)) addWord(m[0]);
    if ((++n0 & 255) === 0) await tick();
  }
  for (const t of extra) for (const m of String(t || '').matchAll(re)) addWord(m[0], 3);
  for (const w of COMMON_TR_LIST) if (!freq.has(w)) freq.set(w, 3);

  // Düzeltme hedefleri: yeterince sık (≥2) ve ≥4 harfli sözcükler
  const dels = new Map<string, string[]>();
  let n1 = 0;
  for (const [w, c] of freq) {
    if ((++n1 & 1023) === 0) await tick();
    if (c < 2 || w.length < 4 || /\d/.test(w)) continue;
    for (const d of deletes1(w)) {
      const l = dels.get(d);
      if (l) { if (l.length < 12) l.push(w); } else dels.set(d, [w]);
    }
  }
  // Ünlüsüz yazım ("gstrt", "otimmn", "pnmn") için ünsüz iskeleti → en sık sözcük
  const skel = new Map<string, [string, number]>();
  for (const [w, c] of freq) {
    if (c < 3 || w.length < 5 || /\d/.test(w)) continue;
    const k = skeleton(w);
    if (k.length < 4) continue;
    const cur = skel.get(k);
    if (!cur || c > cur[1]) skel.set(k, [w, c]);
  }
  const disp = new Map<string, string>();
  for (const [f, fm] of forms) {
    let best = f, bc = -1;
    for (const [form, c] of fm) if (c > bc) { bc = c; best = form; }
    disp.set(f, best);
  }
  forms.clear();

  const cache = new Map<string, string>();
  const fq = (w: string) => freq.get(w) || 0;

  const lookup = (w: string): string | null => {
    const own = fq(w);
    const maxd = w.length >= 8 ? 2 : 1;
    const cands = new Set<string>();
    for (const x of dels.get(w) || []) cands.add(x); // öğrenci bir harf atlamış
    for (const d of deletes1(w)) {
      if (fq(d) >= 2 && d.length >= 4) cands.add(d); // fazladan harf
      for (const x of dels.get(d) || []) cands.add(x); // yanlış/yer değiştirmiş harf
    }
    let best: string | null = null, bd = maxd + 1, bf = 0;
    for (const c of cands) {
      if (c === w) continue;
      const dd = damerau(w, c, maxd);
      if (dd > maxd) continue;
      const cf = fq(c);
      // İlk harf hatası nadirdir; kısa sözcükte ilk harf değişmesin ("kist" ≠ "list")
      if (c[0] !== w[0] && w.length < 7) continue;
      if (dd < bd || (dd === bd && cf > bf)) { best = c; bd = dd; bf = cf; }
    }
    // Ünlüsü atılmış yazım: ünlü oranı düşükse ünsüz iskeletiyle dene (ilk harf aynı kalır)
    if (!best && own === 0 && w.length >= 4) {
      const vowels = (w.match(VOWELS) || []).length;
      if (vowels / w.length <= (w.length >= 6 ? 0.34 : 0.25)) {
        const hit = skel.get(skeleton(w));
        if (hit && hit[1] >= 3) return hit[0];
      }
    }
    // Sözlükte zaten olan bir sözcük yalnız çok daha sık bir yakın biçime çekilir (yaygın yazım hatası)
    if (best && own > 0 && !(bf >= 20 * own && own <= 2)) return null;
    return best;
  };

  const correct = (w0: string): string => {
    const w = ABBREV[w0] || w0;
    if (w.length < 4 || /\d/.test(w) || isStop(w)) return w;
    const hit = cache.get(w);
    if (hit !== undefined) return hit;
    let out = w;
    if (fq(w) < 3) {
      const direct = lookup(w);
      if (direct) out = direct;
      else {
        for (const s of SUFFIXES) {
          if (!w.endsWith(s) || w.length - s.length < 4) continue;
          const base = w.slice(0, -s.length);
          if (fq(base) >= 3) break; // kök sözlükte: ekli biçim doğru yazılmış
          const fixed = lookup(base);
          if (fixed) { out = fixed + s; break; }
        }
      }
    }
    if (cache.size > 50_000) cache.clear();
    cache.set(w, out);
    return out;
  };

  return {
    size: freq.size,
    freq: fq,
    display: (w) => disp.get(w) || w,
    correct,
  };
}

// ---------------------------------------------------------------- tıbbi terim dizini

export type TermEntry = { tokens: string[]; canonical: string };
export type TermIndex = { byHead: Map<string, TermEntry[]>; size: number };

const TERM_STOP = new Set(
  ('primer sekonder benign malign evre evresi derece tipik atipik lokal yaygin diffuz fokal sinir tumor tumoru ' +
    'enfeksiyon enfeksiyonu yetmezlik yetmezligi bozuklugu anomali anomalisi hastaligi hastaliklari hastalik ' +
    'sendrom sendromu tani tanisi tedavi tedavisi hucre hucreli doku kronik akut tip tipi neden nedeni bulgu bulgusu ' +
    'genel klinik tibbi').split(' '),
);

export function buildTermIndex(names: { name: string; latin?: string }[]): TermIndex {
  const byHead = new Map<string, TermEntry[]>();
  const seen = new Set<string>();
  const push = (tk: string[], canonical: string) => {
    const key = tk.join(' ');
    if (seen.has(key)) return;
    seen.add(key);
    const head = tk[0].slice(0, 3);
    (byHead.get(head) || byHead.set(head, []).get(head)!).push({ tokens: tk, canonical });
  };
  const add = (label: string, canonical: string) => {
    const tk = fold(label).split(' ').filter(Boolean);
    if (!tk.length) return;
    if (tk.length === 1 && (tk[0].length < 5 || TERM_STOP.has(tk[0]) || STOP.has(tk[0]))) return;
    if (tk.every((t) => TERM_STOP.has(t) || STOP.has(t))) return;
    push(tk, canonical);
  };
  for (const { name, latin } of names) {
    const canonical = name.replace(/\s*\(.*?\)\s*/g, ' ').trim() || name;
    add(canonical, canonical);
    if (latin) add(latin, canonical);
    // Parantez içi eş ad: büyük harfli kısaltma ("ccRCC", "PKOS") birebir; çok sözcüklü eş ad olduğu gibi
    for (const m of name.matchAll(/\(([^)]+)\)/g)) for (const part of m[1].split(/[\/,;]/)) {
      const p = part.trim();
      if (/^[A-Za-zÇĞİÖŞÜçğıöşü][\w-]{1,7}$/.test(p) && /[A-Z].*[A-Z]/.test(p)) {
        const f = fold(p).replace(/ /g, '');
        if (f.length >= 3) push([f], canonical);
        continue;
      }
      const tk = fold(p).split(' ').filter((t) => t && !TERM_STOP.has(t));
      if (tk.length >= 2 || (tk.length === 1 && tk[0].length >= 7)) add(p, canonical);
    }
  }
  for (const list of byHead.values()) list.sort((a, b) => b.tokens.length - a.tokens.length);
  return { byHead, size: seen.size };
}

/** Metin sözcüğü terim sözcüğünün ekli hali mi ("amiloidozda" ← "amiloidoz", "yumrugu" ← "yumruk"). */
const SOFTEN: Record<string, string> = { k: 'g', p: 'b', t: 'd', c: 'c' };
const tokenMatches = (textTok: string, termTok: string) => {
  if (textTok === termTok || (termTok.length >= 4 && textTok.startsWith(termTok))) return true;
  // Yalnız ünsüz yumuşaması: "yumruğu" ← "yumruk", "kitabı" ← "kitap" ("gastrit" ≠ "gastrik")
  const last = termTok[termTok.length - 1];
  return termTok.length >= 5 && !!SOFTEN[last] && textTok.length > termTok.length - 1 &&
    textTok.startsWith(termTok.slice(0, -1)) && textTok[termTok.length - 1] === SOFTEN[last];
};

/** Düzeltilmiş sözcük dizisindeki terimler (en uzun eşleşme önce, kanonik adlarıyla). */
export function matchTermsInWords(tk: string[], idx: TermIndex): string[] {
  const out = new Set<string>();
  for (let i = 0; i < tk.length; i++) {
    const cands = idx.byHead.get(tk[i].slice(0, 3));
    if (!cands) continue;
    for (const c of cands) {
      if (i + c.tokens.length > tk.length) continue;
      const ok = c.tokens.length === 1 && c.tokens[0].length <= 4
        ? tk[i] === c.tokens[0]
        : c.tokens.every((t, k) => tokenMatches(tk[i + k], t));
      if (!ok) continue;
      out.add(c.canonical);
      i += c.tokens.length - 1;
      break;
    }
  }
  return [...out];
}
