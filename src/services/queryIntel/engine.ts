/**
 * Sorgu zekâsı motoru (sunucu + tarayıcı ortak).
 *
 * Girdi: derlemden çıkarılmış paket (sözcükler, sıklıklar, kavramlar) + ikili dizinler (SymSpell, n-gram).
 * Yaptıkları:
 *  - correct(): bağlamlı yazım düzeltme + Türkçe karakter geri kazanımı ("bobrek tumoru" → "böbrek tümörü")
 *  - complete(): sözcük / kavram / sonraki sözcük önerileri (her tuşta, ~0.1-1 ms)
 *  - completeSentence(): n-gram ile soluk "hayalet" cümle devamı
 *  - analyze(): kavramlar (hastalık, ilaç, gen…), niyet (tedavi/tanı…), eşanlamlı yeniden yazımlar
 *
 * Bellek: dizinler typed array'dir (80k sözcük ≈ 6 MB SymSpell, n-gram ≈ 10 MB). Map yalnız sözcük→id ve kavram adları için.
 */
import {
  type Concept, type IntentKey, type PackedConcept, type WordSpan,
  PhraseMatcher, SYM_PREFIX, TR_CHARS, WORD_EQUIV, commonPrefix, lemma, suffixClass, deleteKeys, detectIntent, editDistance, fnv1a, fold,
  isAdjacentTypo, splitWords, unpackConcept,
} from './core';

export const PACK_VERSION = 1;

export interface QueryIntelPackJson {
  v: number;
  builtAt: string;
  signature: string;
  /** Yüzey biçimi (derlemde en sık Türkçe yazım), katlanmış anahtara göre sıralı */
  words: string[];
  /** Belge sıklığı (df) */
  freq: number[];
  /** Yüzey biçiminin aynı katlanmış anahtardaki payı (0-100); düşükse (sık/şık) karakter geri kazanımı yapılmaz */
  share: number[];
  /** Kısaltma olarak (hep büyük harf) yazılan sözcük id'leri: VHL, ANCA, HPV */
  acr: number[];
  concepts: PackedConcept[];
  stats?: Record<string, number>;
}

export interface QueryIntelBins {
  symHash: Uint32Array;
  symId: Int32Array;
  ngHash: Uint32Array;
  ngStart: Uint32Array;
  ngNext: Int32Array;
  ngCount: Uint16Array;
}

export interface SpellChange { from: string; to: string; conf: number }
export interface SpellResult { text: string | null; changes: SpellChange[] }

export type SuggestionKind = 'concept' | 'word' | 'next' | 'fix';
export interface Suggestion {
  kind: SuggestionKind;
  /** Kutudaki metnin yeni hâli (öneri seçilince) */
  value: string;
  /** Gösterilecek etiket */
  label: string;
  /** Kavram önerisi: tür + bağlantı */
  type?: string;
  ref?: { kind: string; id: string } | null;
  /** Eşleşen takma ad (etiketten farklıysa) */
  via?: string;
  score: number;
}

export interface ConceptHit {
  label: string;
  type: string;
  ref: { kind: string; id: string } | null;
  discipline: string;
  /** Metinde eşleşen parça */
  matched: string;
  start: number;
  end: number;
  /** Takma addan (eşanlamlı / kısaltma / Latince) bulunduysa true */
  viaAlias: boolean;
  /** Eşleşen ad güçlü (etiket ya da küratörlü takma ad) — yalnız bunlar sorguyu yeniden yazar */
  strong?: boolean;
}

export interface QueryUnderstanding {
  query: string;
  /** Yazım düzeltilmiş sorgu (değişiklik yoksa null) */
  corrected: string | null;
  changes: SpellChange[];
  concepts: ConceptHit[];
  intent: IntentKey | null;
  /** Eşanlamlıları kanonik ada çevrilmiş ek sorgular ("kansızlık tedavisi" → "anemi tedavisi") */
  rewrites: string[];
  /** Katlanmış odak terimleri (niyet sözcükleri ve stopword'ler hariç) */
  focus: string[];
  /**
   * Arama yuvaları: her odak sözcüğü için kabul edilen kök biçimleri (kendisi + eşdeğerleri).
   * Belge her yuvadan herhangi bir kökü içeriyorsa kapsanmış sayılır ("böbrek tümörü" ≈ "renal neoplazm").
   */
  slots: Array<{ w: string; alts: string[] }>;
}

const INTENT_HEADS = ['tedavi', 'tani', 'teshis', 'belirti', 'bulgu', 'semptom', 'etiyoloji', 'neden', 'sebep', 'patoloji', 'patogenez', 'histoloji',
  'histopatoloji', 'morfoloji', 'mekanizma', 'fizyopatoloji', 'patofizyoloji', 'goruntuleme', 'radyoloji', 'epidemiyoloji', 'siklik', 'ayirici', 'komplikasyon', 'prognoz', 'klinik'];

const STOP = new Set(['ve', 'ile', 'veya', 'bir', 'bu', 'su', 'da', 'de', 'ki', 'mi', 'mu', 'icin', 'gibi', 'olan', 'en', 'hangisi', 'hangisidir', 'nedir', 'asagidakilerden', 'ne', 'nasil']);

/** Tür bazlı öneri ağırlığı (aramada hastalık ve terim önce gelir) */
const TYPE_BOOST: Record<string, number> = { disease: 1.6, drug: 1.2, gene: 1.0, pathogen: 1.0, symptom: 0.9, procedure: 0.8, anatomy: 0.5, term: 0.6, topic: 0.7 };

function applyCase(typed: string, to: string): string {
  if (typed.length > 1 && typed === typed.toLocaleUpperCase('tr-TR') && typed !== typed.toLocaleLowerCase('tr-TR')) return to.toLocaleUpperCase('tr-TR');
  const c = typed[0];
  if (c && c === c.toLocaleUpperCase('tr-TR') && c !== c.toLocaleLowerCase('tr-TR')) return to.charAt(0).toLocaleUpperCase('tr-TR') + to.slice(1);
  return to;
}

function lowerBound(arr: string[], key: string): number {
  let lo = 0;
  let hi = arr.length;
  while (lo < hi) {
    const mid = (lo + hi) >>> 1;
    if (arr[mid] < key) lo = mid + 1; else hi = mid;
  }
  return lo;
}

function lowerBoundU32(arr: Uint32Array, key: number): number {
  let lo = 0;
  let hi = arr.length;
  while (lo < hi) {
    const mid = (lo + hi) >>> 1;
    if (arr[mid] < key) lo = mid + 1; else hi = mid;
  }
  return lo;
}

export class QueryIntelEngine {
  readonly builtAt: string;
  readonly signature: string;
  readonly words: string[];
  readonly folded: string[];
  readonly freq: Int32Array;
  private share: Uint8Array;
  private acr: Set<number>;
  private wordId = new Map<string, number>();
  readonly concepts: Concept[];
  private matcher = new PhraseMatcher();
  /** Kavram önek dizini: katlanmış takma ad (ve sözcük başından kesitleri) → [kavram, takma ad sırası, kesit mi] */
  private cKeys: string[] = [];
  private cRefs: Int32Array = new Int32Array(0);
  private bins: QueryIntelBins;
  /** Sözcük eşdeğerlik kümeleri: kök → küme no; küme → kökler (katlanmış) + yüzey biçimleri */
  private equivOf = new Map<string, number>();
  private equiv: Array<{ roots: string[]; surfaces: string[] }> = [];
  /** 2 harfli önek → en sık 24 sözcük (kısa öneklerde tüm aralığı taramamak için) */
  private topByPrefix2 = new Map<string, number[]>();

  constructor(pack: QueryIntelPackJson, bins: QueryIntelBins | null) {
    this.builtAt = pack.builtAt;
    this.signature = pack.signature;
    this.words = pack.words;
    this.folded = pack.words.map((w) => fold(w));
    this.freq = Int32Array.from(pack.freq);
    this.share = Uint8Array.from(pack.share || []);
    this.acr = new Set(pack.acr || []);
    for (let i = 0; i < this.folded.length; i++) this.wordId.set(this.folded[i], i);
    this.concepts = pack.concepts.map(unpackConcept);
    this.bins = bins || this.buildBins();
    this.buildConceptIndex();
    this.buildPrefixTops();
    this.buildEquivalence();
  }

  /**
   * Eşdeğerlik kümeleri: küratörlü WORD_EQUIV + tek sözcüklük kavram adı ile güçlü tek sözcüklük takma adları
   * (Neoplazi ↔ Neoplazm ↔ Tümör). Kısaltmalar küme kurmaz (kısaltma kavram düzeyinde ele alınır).
   */
  private buildEquivalence(): void {
    const addGroup = (surfaces: string[]) => {
      const uniq = [...new Map(surfaces.map((x) => [lemma(fold(x)), x.toLocaleLowerCase('tr-TR')])).entries()].filter(([r]) => r.length >= 3);
      if (uniq.length < 2) return;
      // Mevcut bir kümeyle kesişiyorsa birleştir
      let gid = -1;
      for (const [r] of uniq) { const g = this.equivOf.get(r); if (g !== undefined) { gid = g; break; } }
      if (gid < 0) { gid = this.equiv.length; this.equiv.push({ roots: [], surfaces: [] }); }
      const grp = this.equiv[gid];
      for (const [r, surf] of uniq) {
        if (grp.roots.includes(r)) continue;
        grp.roots.push(r);
        grp.surfaces.push(surf);
        this.equivOf.set(r, gid);
      }
    };
    for (const g of WORD_EQUIV) addGroup(g);
    this.concepts.forEach((c) => {
      const label = c.label.replace(/\s*\([^)]*\)/g, '').trim();
      if (label.includes(' ') || c.type === 'topic') return;
      const singles = c.aliases.filter((a, i) => (c.strongMask & (1 << i)) && !a.includes(' ') && a.length >= 4 && a !== a.toLocaleUpperCase('tr-TR'));
      if (singles.length) addGroup([label, ...singles]);
    });
  }

  /** Sözcüğün eşdeğerlik kümesi: kök (ek kesilerek) bulunur. Dönen: küme no + sözcükteki kök uzunluğu */
  private equivFor(f: string): { gid: number; root: string } | null {
    const l = lemma(f);
    for (const cand of l === f ? [f] : [f, l]) {
      const g = this.equivOf.get(cand);
      if (g !== undefined) return { gid: g, root: cand };
    }
    for (let cut = 1; cut <= 4 && f.length - cut >= 4; cut++) {
      const st = f.slice(0, f.length - cut);
      const g = this.equivOf.get(st);
      if (g !== undefined) return { gid: g, root: st };
      // ünsüz yumuşaması: böbreğin → böbreg → böbrek
      if (st.endsWith('g') || st.endsWith('b')) {
        const hard = st.slice(0, -1) + (st.endsWith('g') ? 'k' : 'p');
        const g2 = this.equivOf.get(hard);
        if (g2 !== undefined) return { gid: g2, root: st };
      }
    }
    return null;
  }

  /**
   * Eki koruyarak eşdeğer köke taşır: "tümörü" (tümör + ü) → "neoplazmı" / "neoplazisi".
   * Aday biçim sözlükte (derlemde) bulunmalı; komşu sözcükle birlikte geçiyorsa (ikili sayım) öncelik alır.
   * Dönen: yüzey biçimi + doğrulama (komşuyla geçiyor mu) ya da null.
   */
  inflectLike(typedF: string, ownRoot: string, targetRoot: string, prev?: string, next?: string): { word: string; attested: boolean; score: number } | null {
    const suf = typedF.length > ownRoot.length ? typedF.slice(ownRoot.length) : '';
    const cls = suffixClass(suf);
    let best: { word: string; attested: boolean; score: number } | null = null;
    const lo = lowerBound(this.folded, targetRoot);
    for (let i = lo, n = 0; i < this.folded.length && n < 400 && this.folded[i].startsWith(targetRoot); i++, n++) {
      const cf = this.folded[i];
      if (cf.length > targetRoot.length + 6) continue;
      if (suffixClass(cf.slice(targetRoot.length)) !== cls) continue;
      const withPrev = prev ? this.pairCount(prev, i) : 0;
      let withNext = 0;
      if (next) { const nid = this.idOf(next); if (nid >= 0) for (const x of this.nextWords([cf], 16)) if (x.id === nid) { withNext = x.count; break; } }
      const attested = withPrev + withNext > 0;
      const score = (withPrev + withNext) * 10 + Math.log1p(this.freq[i]);
      if (!best || score > best.score) best = { word: this.words[i], attested, score };
    }
    return best;
  }

  // ---------------------------------------------------------------- dizinler

  /** İkili dizin yoksa (tarayıcı paketi) sözcüklerden SymSpell kurulur; n-gram boş kalır. */
  private buildBins(): QueryIntelBins {
    const pairs: number[] = [];
    const keys = new Set<string>();
    for (let i = 0; i < this.folded.length; i++) {
      if (this.folded[i].length < 3) continue;
      keys.clear();
      deleteKeys(this.folded[i], keys);
      for (const k of keys) pairs.push(fnv1a(k) * 0x100000 + i);
    }
    const all = Float64Array.from(pairs).sort();
    const symHash = new Uint32Array(all.length);
    const symId = new Int32Array(all.length);
    for (let j = 0; j < all.length; j++) {
      symHash[j] = Math.floor(all[j] / 0x100000);
      symId[j] = all[j] - symHash[j] * 0x100000;
    }
    return { symHash, symId, ngHash: new Uint32Array(0), ngStart: new Uint32Array(1), ngNext: new Int32Array(0), ngCount: new Uint16Array(0) };
  }

  private buildConceptIndex(): void {
    const entries: Array<[string, number]> = [];
    this.concepts.forEach((c, ci) => {
      const names = [c.label, ...c.aliases];
      // Parantezsiz yalın ad da etiket sayılır: "Fournier Gangreni (Perine Nekrotizan Fasiiti)" → "Fournier Gangreni"
      const bare = c.label.replace(/\s*\([^)]*\)/g, ' ').replace(/\s+/g, ' ').trim();
      if (bare.length >= 3 && bare !== c.label) {
        this.matcher.add(bare, ci * 16);
        const bw = splitWords(bare).map((x) => x.f).join(' ');
        if (bw) entries.push([bw, ci << 13]);
      }
      names.forEach((name, ai) => {
        if (ai < 16) this.matcher.add(name, ci * 16 + ai);
        const ws = splitWords(name);
        if (!ws.length) return;
        const full = ws.map((x) => x.f).join(' ');
        // ai: 0 = etiket; kesit (sözcük ortasından başlayan) bayrağı 1<<12
        entries.push([full, (ci << 13) | (Math.min(ai, 4095))]);
        for (let k = 1; k < ws.length && k < 4; k++) {
          const tail = ws.slice(k).map((x) => x.f).join(' ');
          if (tail.length >= 3) entries.push([tail, (ci << 13) | 4096 | Math.min(ai, 4095)]);
        }
      });
    });
    entries.sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0));
    this.cKeys = entries.map((e) => e[0]);
    this.cRefs = Int32Array.from(entries.map((e) => e[1]));
  }

  private buildPrefixTops(): void {
    const buckets = new Map<string, number[]>();
    for (let i = 0; i < this.folded.length; i++) {
      const f = this.folded[i];
      if (f.length < 3 || !/^[a-z]/.test(f)) continue;
      const p = f.slice(0, 2);
      let b = buckets.get(p);
      if (!b) { b = []; buckets.set(p, b); }
      b.push(i);
    }
    for (const [p, ids] of buckets) {
      ids.sort((a, b) => this.freq[b] - this.freq[a]);
      this.topByPrefix2.set(p, ids.slice(0, 24));
    }
  }

  // ---------------------------------------------------------------- temel sorgular

  idOf(folded: string): number {
    return this.wordId.get(folded) ?? -1;
  }

  df(folded: string): number {
    const id = this.idOf(folded);
    return id >= 0 ? this.freq[id] : 0;
  }

  /** Bağlam (önceki 1-2 katlanmış sözcük) → olası sonraki sözcükler. Önce üçlü, sonra ikili bağlam. */
  nextWords(prev: string[], limit = 8): Array<{ id: number; count: number; order: number }> {
    const out: Array<{ id: number; count: number; order: number }> = [];
    const seen = new Set<number>();
    const tryCtx = (ctx: string, order: number) => {
      const h = fnv1a(ctx);
      const { ngHash, ngStart, ngNext, ngCount } = this.bins;
      const at = lowerBoundU32(ngHash, h);
      if (at >= ngHash.length || ngHash[at] !== h) return;
      for (let j = ngStart[at]; j < ngStart[at + 1]; j++) {
        const id = ngNext[j];
        if (seen.has(id)) continue;
        seen.add(id);
        out.push({ id, count: ngCount[j], order });
      }
    };
    const n = prev.length;
    if (n >= 2) tryCtx(`${prev[n - 2]} ${prev[n - 1]}`, 2);
    if (n >= 1) tryCtx(prev[n - 1], 1);
    return out.slice(0, limit);
  }

  /** prev → cand ikili sayımı (bağlamlı düzeltme puanı için) */
  private pairCount(prev: string | undefined, candId: number): number {
    if (!prev) return 0;
    for (const n of this.nextWords([prev], 16)) if (n.id === candId) return n.count;
    return 0;
  }

  /** SymSpell adayları: sorgunun silme anahtarları ile dizin anahtarlarının kesişimi, sonra gerçek mesafe. */
  candidates(foldedWord: string, maxDist: number): Array<{ id: number; dist: number }> {
    const { symHash, symId } = this.bins;
    const keys = deleteKeys(foldedWord);
    const seen = new Set<number>();
    const out: Array<{ id: number; dist: number }> = [];
    for (const k of keys) {
      const h = fnv1a(k);
      for (let j = lowerBoundU32(symHash, h); j < symHash.length && symHash[j] === h; j++) {
        const id = symId[j];
        if (seen.has(id)) continue;
        seen.add(id);
        const cand = this.folded[id];
        // önek dışı kısım: tam sözcük mesafesi
        const d = editDistance(foldedWord, cand, maxDist);
        if (d <= maxDist) out.push({ id, dist: d });
      }
    }
    // Uzun sözcüklerde hata öneğin içindeyse ve 2 hata varsa ilk 8 harfle bulunamayabilir; o durumda
    // aynı ilk 3 harfle başlayan yakın uzunluktaki sık sözcükleri de dene (sınırlı tarama).
    if (out.length === 0 && foldedWord.length > SYM_PREFIX && maxDist >= 2) {
      const lo = lowerBound(this.folded, foldedWord.slice(0, 3));
      for (let i = lo, n = 0; i < this.folded.length && n < 4000 && this.folded[i].startsWith(foldedWord.slice(0, 3)); i++, n++) {
        const cand = this.folded[i];
        if (Math.abs(cand.length - foldedWord.length) > maxDist) continue;
        const d = editDistance(foldedWord, cand, maxDist);
        if (d <= maxDist) out.push({ id: i, dist: d });
      }
    }
    return out;
  }

  // ---------------------------------------------------------------- yazım düzeltme

  /**
   * Tek sözcük düzeltmesi. prev/next: katlanmış komşu sözcükler (bağlam puanı).
   * Dönen `to` yüzey biçimidir (kullanıcının büyük harf düzeni uygulanmış).
   */
  correctWord(span: WordSpan, prev?: string, next?: string): SpellChange | null {
    const typed = span.w;
    const f = span.f;
    if (span.suffix || f.length < 3 || /\d/.test(f)) return null;
    if (STOP.has(f)) return null;
    const isUpper = typed.length > 1 && typed === typed.toLocaleUpperCase('tr-TR') && typed !== typed.toLocaleLowerCase('tr-TR');
    const id = this.idOf(f);
    const own = id >= 0 ? this.freq[id] : 0;
    if (isUpper && typed.length <= 6) return null; // kısaltma: dokunma
    // 1) Bilinen sözcük: yalnız Türkçe karakter geri kazanımı (kullanıcı hiç Türkçe harf yazmadıysa)
    if (own >= 4) {
      if (TR_CHARS.test(typed) || this.acr.has(id)) return null;
      const surface = this.words[id];
      if (surface === typed.toLocaleLowerCase('tr-TR') || (this.share[id] ?? 100) < 80) return null;
      if (!TR_CHARS.test(surface)) return null;
      return { from: typed, to: applyCase(typed, surface), conf: 0.95 };
    }
    // 2) Yarım yazılmış sözcük ("böbr", "nefropatis"): çok daha yaygın bir sözcüğün öneki ise düzeltme yapılmaz
    if (own === 0 && f.length >= 3 && this.hasFrequentExtension(f)) return null;
    // 3) Bilinmeyen / çok nadir: yakın ve çok daha yaygın aday
    const maxDist = f.length >= 7 ? 2 : 1;
    const cands = this.candidates(f, maxDist).filter((c) => c.id !== id && this.freq[c.id] >= Math.max(5, own * 30));
    let best: { id: number; s: number; dist: number } | null = null;
    let second = -Infinity;
    for (const c of cands) {
      const cf = this.folded[c.id];
      let s = Math.log1p(this.freq[c.id]) - 3.2 * c.dist;
      if (c.dist === 1 && isAdjacentTypo(f, cf)) s += 1.2;
      s += 0.25 * Math.min(4, commonPrefix(f, cf));
      s += cf[0] === f[0] ? 0.8 : -1.2;
      s += 1.5 * Math.log1p(this.pairCount(prev, c.id));
      if (next) {
        const nid = this.idOf(next);
        if (nid >= 0) for (const n of this.nextWords([cf], 16)) if (n.id === nid) { s += Math.log1p(n.count); break; }
      }
      if (!best || s > best.s) { if (best) second = Math.max(second, best.s); best = { id: c.id, s, dist: c.dist }; }
      else if (s > second) second = s;
    }
    // 4) Bitişik yazılmış iki sözcük: "nefrotiksendrom" → "nefrotik sendrom"
    if (!best && own === 0 && f.length >= 8) {
      let split: { a: number; b: number; s: number } | null = null;
      for (let k = 3; k <= f.length - 3; k++) {
        const a = this.idOf(f.slice(0, k));
        const b = this.idOf(f.slice(k));
        if (a < 0 || b < 0 || this.freq[a] < 20 || this.freq[b] < 20) continue;
        const s = Math.log1p(this.freq[a]) + Math.log1p(this.freq[b]) + 2 * Math.log1p(this.pairCount(this.folded[a], b));
        if (!split || s > split.s) split = { a, b, s };
      }
      if (split) return { from: typed, to: applyCase(typed, `${this.words[split.a]} ${this.words[split.b]}`), conf: 0.7 };
    }
    if (!best) return null;
    const margin = best.s - second;
    const conf = Math.max(0.3, Math.min(0.99, 0.55 + margin / 6 - (best.dist - 1) * 0.1));
    if (own > 0 && conf < 0.7) return null; // nadir ama gerçek sözcük olabilir
    return { from: typed, to: applyCase(typed, this.words[best.id]), conf: Math.round(conf * 100) / 100 };
  }

  private hasFrequentExtension(f: string): boolean {
    const lo = lowerBound(this.folded, f);
    for (let i = lo, n = 0; i < this.folded.length && n < 2000 && this.folded[i].startsWith(f); i++, n++) {
      if (this.freq[i] >= 20) return true;
    }
    return false;
  }

  /** Metnin tamamı: { text: düzeltilmiş | null, changes } — /api/search/spell ile aynı biçim */
  correct(text: string, minConf = 0.5): SpellResult {
    const spans = splitWords(text);
    const changes: SpellChange[] = [];
    let out = '';
    let last = 0;
    for (let i = 0; i < spans.length; i++) {
      const sp = spans[i];
      const ch = this.correctWord(sp, spans[i - 1]?.f, spans[i + 1]?.f);
      if (!ch || ch.conf < minConf) continue;
      out += text.slice(last, sp.s) + ch.to;
      last = sp.e;
      changes.push(ch);
    }
    if (!changes.length) return { text: null, changes };
    return { text: out + text.slice(last), changes };
  }

  // ---------------------------------------------------------------- kavramlar

  private conceptHit(ci: number, matched: string, start: number, end: number, viaAlias: boolean): ConceptHit {
    const c = this.concepts[ci];
    return { label: c.label, type: c.type, ref: c.ref, discipline: c.discipline, matched, start, end, viaAlias };
  }

  /** Aynı ifadeye birden çok kavram bağlıysa: hastalık > ilaç > … ve ağırlık */
  /** Eşleşen ad güçlü mü: etiketin kendisi ya da küratörlü/kaynak takma adı (zayıf: sözlükteki gevşek eşanlamlılar) */
  private slotStrong(ci: number, slot: number): boolean {
    return slot === 0 || (this.concepts[ci].strongMask & (1 << (slot - 1))) !== 0;
  }

  /** Aynı ifadeye birden çok kavram bağlıysa: güçlü ad > hastalık > ilaç > … > ağırlık. Dönen: [kavram, yuva] */
  private pickConcept(ids: number[]): [number, number] {
    let best: [number, number] = [ids[0] >> 4, ids[0] & 15];
    let bs = -Infinity;
    for (const id of ids) {
      const ci = id >> 4;
      const slot = id & 15;
      const c = this.concepts[ci];
      const s = (TYPE_BOOST[c.type] || 0.5) * 2 + c.weight + (this.slotStrong(ci, slot) ? 3 : 0) + (slot === 0 ? 0.5 : 0);
      if (s > bs) { bs = s; best = [ci, slot]; }
    }
    return best;
  }

  detectConcepts(text: string, spans = splitWords(text), skip?: Set<number>): ConceptHit[] {
    const usable = spans.map((s, i) => (skip?.has(i) || s.suffix ? { ...s, f: '\u0000' } : s));
    const hits: ConceptHit[] = [];
    for (const m of this.matcher.scan(usable)) {
      const [ci, slot] = this.pickConcept(m.ids);
      const start = spans[m.from].s;
      const end = spans[m.to - 1].e;
      const matched = text.slice(start, end);
      const key = spans.slice(m.from, m.to).map((s) => s.f).join(' ');
      const strong = this.slotStrong(ci, slot);
      const single = m.to - m.from === 1;
      // Zayıf eşanlamlı tek sözcük ("tümör" → Neoplazi) gürültüdür; kısa (≤3) sözcük yalnız güçlü kısaltmaysa
      if (single && !strong) continue;
      // Tamlama başı: takma ad önündeki içerik sözcüğüyle derlemde birlikte geçiyorsa ("karaciğer tümörü")
      // ya da önündeki sözcük bir organ/niteleyici eşdeğerlik kümesindeyse, tek sözcük kavramın kendisi değildir.
      if (single && slot !== 0 && m.from > 0) {
        const pv = spans[m.from - 1];
        if (!STOP.has(pv.f) && pv.f.length >= 3) {
          const wid = this.idOf(spans[m.from].f);
          if ((wid >= 0 && this.pairCount(pv.f, wid) >= 2) || this.equivFor(pv.f)) continue;
        }
      }
      if (single && key.length <= 3 && !strong) continue;
      if (single && key.length <= 2) continue;
      hits.push({ ...this.conceptHit(ci, matched, start, end, slot !== 0), strong } as ConceptHit);
    }
    return hits;
  }

  /** Kavram önek araması: katlanmış metin (bir ya da birkaç sözcük) ile başlayan kavramlar */
  private conceptsByPrefix(prefix: string, limit: number): Array<{ ci: number; ai: number; infix: boolean }> {
    const out: Array<{ ci: number; ai: number; infix: boolean }> = [];
    if (prefix.length < 2) return out;
    const seen = new Set<number>();
    for (let i = lowerBound(this.cKeys, prefix); i < this.cKeys.length && this.cKeys[i].startsWith(prefix); i++) {
      const r = this.cRefs[i];
      const ci = r >>> 13;
      if (seen.has(ci)) continue;
      seen.add(ci);
      out.push({ ci, ai: r & 4095, infix: (r & 4096) !== 0 });
      if (out.length >= limit * 6) break;
    }
    return out;
  }

  // ---------------------------------------------------------------- tamamlama

  /**
   * Yazarken öneriler. Metin boşlukla bitiyorsa sonraki sözcük; değilse son sözcüğün tamamlanması +
   * son 1-3 sözcükle başlayan kavramlar. Önerinin `value`su kutunun yeni hâlidir.
   */
  complete(text: string, limit = 8): Suggestion[] {
    const spans = splitWords(text);
    const endsWithSpace = /\s$/.test(text);
    const out: Suggestion[] = [];
    const seen = new Set<string>();
    const push = (s: Suggestion) => {
      const k = fold(s.value).replace(/\s+/g, ' ').trim();
      if (seen.has(k) || k === fold(text).replace(/\s+/g, ' ').trim()) return;
      seen.add(k);
      out.push(s);
    };
    if (!spans.length) return out;

    if (endsWithSpace) {
      const prev = spans.slice(-2).map((s) => s.f);
      const nexts = this.nextWords(prev, limit);
      const total = nexts.reduce((a, n) => a + n.count, 0) || 1;
      for (const n of nexts) {
        const w = this.words[n.id];
        if (w === '?') continue;
        push({ kind: 'next', value: text + w, label: w, score: (n.count / total) * 10 + n.order });
      }
      return out.slice(0, limit);
    }

    const lastSpan = spans[spans.length - 1];
    const partial = lastSpan.f;
    const before = text.slice(0, lastSpan.s);
    const prevF = spans.slice(-3, -1).map((s) => s.f);

    // 1) Kavramlar: son k sözcük (k=3..1) ile başlayan kavram adları.
    //    Sorgunun ortasından başlayan tek sözcüklük eşleşme ("…en sık" → "Sık kanser") yalnız güçlü türlerde;
    //    ad ortasından eşleşme (infix: "renal hüc" → "Berrak Hücreli Renal…") yalnız k ≥ 2 ya da tek sözcüklük sorguda.
    const intentIdx = detectIntent(spans.map((s) => s.f)).words;
    for (let k = Math.min(3, spans.length); k >= 1; k--) {
      const fromIdx = spans.length - k;
      const from = spans[fromIdx];
      if (intentIdx.has(fromIdx) || STOP.has(from.f)) continue;
      const key = spans.slice(-k).map((s) => s.f).join(' ');
      if (key.length < 2 || (k === 1 && key.length < 3 && !/^[A-Z]/.test(from.w))) continue;
      const midQuery = fromIdx > 0;
      // Sorgu ortasında niyet sözcüğü yazılıyorsa ("…teda" → tedavi) kavram değil sözcük tamamlanır
      if (midQuery && k === 1 && INTENT_HEADS.some((h) => h.startsWith(key) || key.startsWith(h))) continue;
      for (const h of this.conceptsByPrefix(key, limit)) {
        const c = this.concepts[h.ci];
        if (h.infix && k < 2 && spans.length > 1) continue;
        if (midQuery && k === 1 && (key.length < 4 || !['disease', 'drug', 'gene', 'pathogen', 'symptom'].includes(c.type))) continue;
        const alias = h.ai === 0 ? c.label : c.aliases[h.ai - 1];
        // Kısaltma ya da etiketle eşleşmede kutuya kanonik ad (parantezsiz), uzun takma adda (Latince) takma ad yazılır
        const head = text.slice(0, from.s);
        const insert = (h.ai === 0 || fold(alias).length <= 6 ? c.label : alias).replace(/\s*\([^)]*\)/g, '').trim();
        const exactLen = fold(alias).length === key.length;
        const score = 4 + k * 1.5 + c.weight * 1.2 + (TYPE_BOOST[c.type] || 0.5) * 2 - (h.infix ? 1.5 : 0) - (midQuery ? 1 : 0) - (exactLen ? 0 : fold(alias).length / 40);
        push({
          kind: 'concept',
          value: head + insert,
          label: c.label,
          type: c.type,
          ref: c.ref,
          via: h.ai === 0 ? undefined : alias,
          score,
        });
      }
    }

    // 2) Sözcük tamamlama: önek aralığı (kısa önekte en sık sözcükler + bağlam adayları)
    const ctxNext = this.nextWords(prevF, 24);
    const ctxCount = new Map<number, number>();
    for (const n of ctxNext) ctxCount.set(n.id, n.count);
    const cand = new Set<number>();
    for (const n of ctxNext) if (this.folded[n.id].startsWith(partial) && this.folded[n.id] !== partial) cand.add(n.id);
    if (partial.length === 2) {
      for (const id of this.topByPrefix2.get(partial) || []) cand.add(id);
    } else if (partial.length > 2) {
      const lo = lowerBound(this.folded, partial);
      const ids: number[] = [];
      for (let i = lo; i < this.folded.length && this.folded[i].startsWith(partial) && ids.length < 6000; i++) if (this.folded[i] !== partial) ids.push(i);
      if (ids.length > 400) ids.sort((a, b) => this.freq[b] - this.freq[a]);
      for (const id of ids.slice(0, 400)) cand.add(id);
    }
    // 3) Önekte yazım hatası: öneki eşleşen sözcük yoksa yakın sözcükler
    if (cand.size === 0 && partial.length >= 4) {
      for (const c of this.candidates(partial, partial.length >= 7 ? 2 : 1)) if (this.freq[c.id] >= 5) cand.add(c.id);
    }
    for (const id of cand) {
      const w = this.words[id];
      if (w === '?') continue;
      const ctx = ctxCount.get(id) || 0;
      const score = Math.log1p(this.freq[id]) * 0.6 + Math.log1p(ctx) * 2.2 - (this.folded[id].length - partial.length) * 0.03;
      push({ kind: 'word', value: before + applyCase(lastSpan.w, w), label: applyCase(lastSpan.w, w), score });
    }
    out.sort((a, b) => b.score - a.score);
    return out.slice(0, limit);
  }

  /**
   * Soluk cümle devamı: en olası sonraki sözcükler (açgözlü), en çok maxWords sözcük ya da "?".
   * Yalnız güvenli devam: her adımda en iyi aday payı ≥ %30 ve sayımı ≥ 3.
   */
  completeSentence(text: string, maxWords = 8): string {
    const spans = splitWords(text);
    if (spans.length === 0) return '';
    const endsWithSpace = /\s$/.test(text);
    const ctx = spans.map((s) => s.f);
    let out = '';
    // Son sözcük yarımsa önce onu tamamla
    if (!endsWithSpace) {
      const last = ctx[ctx.length - 1];
      const nexts = this.nextWords(ctx.slice(0, -1), 24).filter((n) => this.folded[n.id].startsWith(last) && this.folded[n.id] !== last);
      if (nexts.length && last.length >= 2) {
        const w = this.words[nexts[0].id];
        out += w.slice(last.length);
        ctx[ctx.length - 1] = this.folded[nexts[0].id];
      } else if (this.idOf(last) < 0) {
        return '';
      }
    }
    for (let step = 0; step < maxWords; step++) {
      const nexts = this.nextWords(ctx.slice(-2), 6);
      if (!nexts.length) break;
      const total = nexts.reduce((a, n) => a + n.count, 0);
      const top = nexts[0];
      if (top.count < 3 || top.count / total < 0.3) break;
      const w = this.words[top.id];
      if (w === '?') { out += '?'; break; }
      if (/^(sayfa|slayt)$/i.test(w)) break;
      out += (out.length === 0 && endsWithSpace ? '' : ' ') + w;
      ctx.push(this.folded[top.id]);
    }
    // Bağlaçla biten devam yarımdır: sondaki "ve / ile / bir …" atılır
    const TAIL = /\s+(ve|ile|veya|bir|için|olarak|da|de|ya|bu|şu|en|daha|çok|gibi|olan|sayfa)$/iu;
    while (TAIL.test(out)) out = out.replace(TAIL, '');
    return out;
  }

  // ---------------------------------------------------------------- anlamlandırma

  analyze(query: string): QueryUnderstanding {
    const q = query.trim().slice(0, 500);
    const spell = this.correct(q, 0.55);
    const base = spell.text ?? q;
    const spans = splitWords(base);
    const { intent, words: intentWords } = detectIntent(spans.map((s) => s.f));
    const concepts = this.detectConcepts(base, spans, intentWords);
    const rewrites: string[] = [];
    const addRw = (rw: string) => { rw = rw.replace(/\s*\([^)]*\)/g, '').replace(/\s+/g, ' ').trim(); if (rw && fold(rw) !== fold(base) && !rewrites.includes(rw)) rewrites.push(rw); };
    // (1) Kavram düzeyi: yalnız çok sözcüklü eşanlamlı ("yüksek tansiyon" → Hipertansiyon) ya da kısaltma (TTP)
    for (const c of concepts) {
      if (!c.viaAlias || !c.strong) continue;
      const multi = splitWords(c.matched).length > 1;
      const acronym = /^[A-ZÇĞİÖŞÜ0-9]{2,6}$/.test(c.matched);
      if (multi || acronym) addRw(`${base.slice(0, c.start)}${c.label}${base.slice(c.end)}`);
    }
    // (2) Sözcük düzeyi: eşdeğer köke eki taşıyarak; yalnız derlemde komşusuyla birlikte geçen biçim yazılır
    //     (tek sözcüklük sorguda komşu yoksa biçimin sözlükte bulunması yeter)
    const slots: Array<{ w: string; alts: string[] }> = [];
    spans.forEach((sp, i) => {
      if (intentWords.has(i) || STOP.has(sp.f) || sp.f.length < 2) return;
      const eq = this.equivFor(sp.f);
      const alts = eq ? this.equiv[eq.gid].roots.filter((r) => r !== eq.root) : [];
      slots.push({ w: sp.f, alts });
      if (!eq) return;
      const prev = spans[i - 1]?.f;
      const next = spans[i + 1]?.f;
      const hasNeighbor = Boolean(prev || next);
      for (const alt of alts) {
        const inf = this.inflectLike(sp.f, eq.root, alt, prev, next);
        if (!inf || (hasNeighbor && !inf.attested)) continue;
        addRw(base.slice(0, sp.s) + applyCase(sp.w, inf.word) + base.slice(sp.e));
      }
    });
    const focus = slots.map((x) => x.w);
    return { query: q, corrected: spell.text, changes: spell.changes, concepts, intent, rewrites: rewrites.slice(0, 4), focus, slots };
  }
}

// ------------------------------------------------------------------ ikili paket biçimi

const MAGIC = 0x31424951; // "QIB1"

/** Bölümler 4 bayta hizalı: [magic, n, m, k] + symHash[n] + symId[n] + ngHash[m] + ngStart[m+1] + ngNext[k] + ngCount[k] (+dolgu) */
export function encodeBins(b: QueryIntelBins): Uint8Array {
  const n = b.symHash.length;
  const m = b.ngHash.length;
  const k = b.ngNext.length;
  const countBytes = Math.ceil((k * 2) / 4) * 4;
  const total = 16 + n * 8 + m * 4 + (m + 1) * 4 + k * 4 + countBytes;
  const buf = new ArrayBuffer(total);
  const head = new Uint32Array(buf, 0, 4);
  head.set([MAGIC, n, m, k]);
  let off = 16;
  new Uint32Array(buf, off, n).set(b.symHash); off += n * 4;
  new Int32Array(buf, off, n).set(b.symId); off += n * 4;
  new Uint32Array(buf, off, m).set(b.ngHash); off += m * 4;
  new Uint32Array(buf, off, m + 1).set(b.ngStart); off += (m + 1) * 4;
  new Int32Array(buf, off, k).set(b.ngNext); off += k * 4;
  new Uint16Array(buf, off, k).set(b.ngCount);
  return new Uint8Array(buf);
}

export function decodeBins(bytes: Uint8Array): QueryIntelBins {
  // typed array görünümleri hizalı tampon ister
  const buf = bytes.byteOffset % 4 === 0 ? bytes.buffer : bytes.slice().buffer;
  const base = bytes.byteOffset % 4 === 0 ? bytes.byteOffset : 0;
  const [magic, n, m, k] = new Uint32Array(buf, base, 4);
  if (magic !== MAGIC) throw new Error('query-intel.bin: geçersiz başlık');
  let off = base + 16;
  const symHash = new Uint32Array(buf, off, n); off += n * 4;
  const symId = new Int32Array(buf, off, n); off += n * 4;
  const ngHash = new Uint32Array(buf, off, m); off += m * 4;
  const ngStart = new Uint32Array(buf, off, m + 1); off += (m + 1) * 4;
  const ngNext = new Int32Array(buf, off, k); off += k * 4;
  const ngCount = new Uint16Array(buf, off, k);
  return { symHash, symId, ngHash, ngStart, ngNext, ngCount };
}
