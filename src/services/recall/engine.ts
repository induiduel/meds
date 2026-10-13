/**
 * Soru havuzu motoru: öğrenci hatırlamalarını temizler, sınıflar (kurul → ders → konu), tıbbi terimleri ayıklar,
 * aynı soruyu anlatanları gruplar ve kanıta dayalı bir taslak kök kurar. LLM yok, ağ yok; sunucu belleğinde çalışır.
 *
 * Bilgi kaynağı (yalnız okunur): data/pastQuestions.json (doğrulanmış çıkmış sorular: sözlük, IDF, ders sınıflayıcı,
 * benzer çıkmış soru), src/data/medical_glossary.json + disease_entities.json (terim dizini),
 * src/data/curriculum_disciplines.json (kurulun ders listesi).
 *
 * Ölçüm: `npm run eval:recall` (scripts/eval/recall-engine.mts) — gruplama F1/ARI, ders isabeti, terim duyarlılığı,
 * kök benzerliği; değişiklikten önce ve sonra çalıştırılır.
 */
import fs from 'fs';
import path from 'path';
import {
  fold, words, isStop, ABBREV, VALID_SHORT_MED, DERS_HINT, claimedLetter, claimedText, questionNumber, letteredOptions, unletteredOptions,
  negativeLikelihood, cleanSentence, classifyRecallRole, extractStemClause, type Letter, type RecallRole,
} from './normalize.ts';
import { buildLexicon, buildTermIndex, matchTermsInWords, makeTicker, COMMON_TR, phoneticFold, type Lexicon, type TermIndex } from './lexicon.ts';

export const RECALL_ENGINE_VERSION = 'hatirlama-v1';

export type Vec = Map<string, number>;

export interface BankDoc {
  id: string;
  committeeId: string;
  discipline: string;
  topic: string;
  number: number | null;
  stem: string;
  options: { key: string; text: string }[];
  correctAnswer: string;
  vec: Vec;
}

export interface Analysis {
  /** Düzeltilmiş içerik sözcükleri (katlanmış). */
  words: string[];
  /** Yalnız soru kökü cümlesinden gelen düzeltilmiş içerik sözcükleri (şık/iddia yorumu hariç). */
  stemWords: string[];
  /** Okunur temiz metin (aksanlı, sohbetsiz, düzeltilmiş). */
  clean: string;
  stems: string[];
  /** Yalnız soru kökü cümlesinin 5-harfli kökleri (çekirdek-çekirdek eşleştirmesi ve taslak kök seçimi için). */
  stemStems: string[];
  vec: Vec;
  stemVec: Vec;
  /** Birimin yapısal rolü: 'stem' | 'mixed' | 'options' | 'claim'. */
  role: RecallRole;
  /** Romen rakamlı öncül/şık ("I, II ve III", "yalnız II") içeriyor mu. */
  isRoman: boolean;
  terms: string[];
  number: number | null;
  claimedLetter: Letter | null;
  claimedText: string | null;
  options: { harf: Letter | null; metin: string }[];
  negative: number;
  /** Soru içeriği yok (yalnız sohbet / üst söylem). */
  isNoise: boolean;
  ders: { name: string; p: number }[];
  konu: { name: string; p: number } | null;
  /** En benzer doğrulanmış çıkmış sorular (aynı kurul). */
  bank: { id: string; score: number }[];
  corrections: [string, string][];
}

/** Ders/alan adları ("hematoloji soruları ağırdı") soru içeriği sayılmaz (yalnız gürültü ayıklamada). */
const AREA_RE = /^(acil|hematolo|geriatri|onkolo|nefrolo|gastro|endokrin|romatolo|kardiyo|halk|saglig|dahiliye|cerrahi|pediatri|noroloji|psikiyatri|ortopedi|radyoloji|anestezi|dermatoloji|uroloji|enfeksiyon|farmakoloji|patoloji|genetik|biyokimya|mikrobiyoloji|fizyoloji|anatomi|histoloji)/;
/**
 * Kök: fonetik hizalamadan sonra ilk 5 harf ("toxoplasma" ve "toksoplazma" → "tokso"),
 * ancak Greko-Latin bileşik ön ekleriyle ("hiper-", "hipo-", "osteo-", "makro-", "mikro-", "inter-", "intra-",
 * "gluta-", "aseta-", "strep-", "enter-", "anti-", "poli-" vb.) başlayan uzun tıbbi terimlerde ön ek sonrası
 * ayırt edici kökü korumak için 7–9 harf alınır ("glutaraldehit" ≠ "glutatyon", "hipertansiyon" ≠ "hipertrofi").
 * Yokluk eki (-sız/-siz/-suz/-süz) anlamı tersine çevirir → ayrı kök ("donus~").
 */
const PRIVATIVE = /(?:siz|suz)(?:l[ae]r|l[iu]k|d[ae]n?|[iu]n|[iu])?$/;
const FOUR_CHAR_ROOT_RE = /^(gebe|meme|deri|doku|inme|koma|vaka|olgu|kafa|mide|kalp|risk|test|kist|ates|agri|odem|atak|ilac|urun|yara|renk|genc|uyku|hava|odak|ayak)(?:l[ae]r|l[iu]k|l[iu]|d[ae]n?|t[ae]n?|n?[iu]n|s?[iu]|y?[ae]|y?l[ae])/;
const SOFTENED_K_RE = /^(bebe|cocu|kemi|kiri|kope|kapa|kula|baca|kabu|yata|yure|solu)g[aeiou]/;
const COMPOUND_9_RE = /^(?:elektro[lfkm]|hip(?:er|o)kal[se])/;
const COMPOUND_8_RE = /^(?:strepto[km]|entero[kbtp]|immun[oghl])/;
const COMPOUND_7_RE = /^(?:hiper|hipo[tkgnp]|osteo|kondr|makro|mikro|inter|intra|ekstr|endok|gluta|aseta|pnomo|lenfo|paras|parat|hepat|antid|antip|antik|antib|antim|antih|polim|polin)/;
const stemCache = new Map<string, string>();
const stemOf = (w0: string): string => {
  const hit = stemCache.get(w0);
  if (hit !== undefined) return hit;
  const w = phoneticFold(w0);
  let out: string;
  if (/^\d/.test(w)) out = w;
  else if (w.length >= 7 && (w.includes('siz') || w.includes('suz')) && PRIVATIVE.test(w.slice(5))) out = `${w.slice(0, 5)}~`;
  else if (w.length >= 9 && COMPOUND_9_RE.test(w)) out = w.slice(0, 9);
  else if (w.length >= 8 && COMPOUND_8_RE.test(w)) out = w.slice(0, 8);
  else if (w.length >= 7 && COMPOUND_7_RE.test(w)) out = w.slice(0, 7);
  else {
    const m4 = w.length >= 5 ? w.match(FOUR_CHAR_ROOT_RE) : null;
    if (m4) out = m4[1];
    else {
      const mk = w.length >= 6 && w.charCodeAt(4) === 103 ? w.match(SOFTENED_K_RE) : null;
      if (mk) out = `${mk[1]}k`;
      else if (w.startsWith('boyan')) out = 'boyam';
      else out = w.slice(0, 5);
    }
  }
  if (stemCache.size < 60_000) stemCache.set(w0, out);
  return out;
};

const GENERIC_CONCEPT_STEM = new Set([
  'hasta', 'hastal', 'sendr', 'bulgu', 'belir', 'klini', 'tablo', 'tedav', 'tanis', 'tani', 'etken', 'neden',
  'hucre', 'doku', 'organ', 'akut', 'kroni', 'prime', 'sekon', 'benig', 'malig', 'tipi', 'grubu', 'oran',
  'test', 'testi', 'yonte', 'ilacl', 'ilac', 'etki', 'etkis', 'reaks', 'enfek', 'infla', 'neopl', 'karsi',
  'mekan', 'fakto', 'resep', 'prote', 'enzim', 'vitam', 'hormo', 'arter', 'venoz', 'sinir', 'kemik', 'eklem',
  'bolge', 'evre', 'derec', 'gorul', 'olusa', 'sonuc', 'artar', 'azali', 'yukse', 'dusuk', 'oneml', 'temel',
]);

function l2(v: Vec): Vec {
  let s = 0;
  for (const x of v.values()) s += x * x;
  const n = Math.sqrt(s) || 1;
  for (const [k, x] of v) v.set(k, x / n);
  return v;
}
export function dot(a: Vec, b: Vec): number {
  const [s, l] = a.size <= b.size ? [a, b] : [b, a];
  let t = 0;
  for (const [k, x] of s) { const y = l.get(k); if (y) t += x * y; }
  return t;
}

/** Ders sınıflayıcı birleşim ağırlıkları (scripts/eval/recall-engine.mts --fit-ders ile seçildi). */
export const CLASSIFY = { bankCentroid: 0.4, bankKnn: 0.4, lecCentroid: 0.2, lecKnn: 0, priorPenalty: 0, hint: 0.25, temperature: 0.06, numberPrior: 0.15 };
// numberPrior: scripts/eval/recall-number-prior.mts (15 gerçek sınav; 0 → %77,6, 0,15 → %81,3, 0,3 → %78,4)

export interface RecallEngine {
  version: string;
  bankSize: number;
  lexicon: Lexicon;
  terms: TermIndex;
  /**
   * `dersPrior`: sınavın kendi sırasından ders ön bilgisi (aynı sınavda bu numaranın komşu sorularının dersleri;
   * `numberDersPrior`). Toplamı ≤ 1.
   */
  analyze: (text: string, opts: { committeeId: string; options?: { key?: string | null; text: string }[]; claimed?: string | null; dersPrior?: Record<string, number> | null }) => Analysis;
  /** Öğrenci metnini okunur cümleye çevirir (sohbet/iddia/no atılır, yazım düzeltilir; bilgi eklenmez). */
  cleanSentence: (text: string) => string;
  /** Kurul içinde çıkmış soru araması (küme merkezi vb. için). */
  searchBank: (vec: Vec, committeeId: string, k?: number) => { id: string; score: number }[];
  disciplinesOf: (committeeId: string) => string[];
  bankDoc: (id: string) => BankDoc | undefined;
  idf: (stem: string) => number;
  /** Tıbbi kavram/hastalık/ilaç kökünün sözlük ve ders notu tanımında geçen ayırt edici kökler (kök ↔ cevap köprüsü). */
  conceptDefs: (stem: string) => Set<string> | undefined;
}

export interface LoadOptions {
  /** Değerlendirmede sızıntıyı önlemek için bankadan çıkarılacak soru kimlikleri. */
  excludeIds?: Set<string>;
  /** Bankayı dosya yerine doğrudan ver (sunucu belleğindeki liste). */
  pastQuestions?: any[];
  lectureSummaries?: any[];
}

function readJson<T>(f: string, fallback: T): T {
  try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return fallback; }
}

type BankRow = { id: string; committeeId: string; discipline: string; topic: string; number: number | null; stem: string; options: { key: string; text: string }[]; correctAnswer: string };
type SummaryRow = { committeeId: string; discipline: string; title: string; content: string };

/** Büyük kaynaklardan yalnız gereken alanları ince kopyalar (motor kapanışı 100 MB'lık bankayı tutmasın). */
function loadSources(rootDir: string, opts: LoadOptions) {
  const past: any[] = opts.pastQuestions || readJson<any[]>(path.join(rootDir, 'data/pastQuestions.json'), []);
  const ex = opts.excludeIds;
  const bank: BankRow[] = [];
  for (const q of past) {
    if (!q || !q.id || !q.committeeId || typeof q.stem !== 'string' || q.stem.length <= 10) continue;
    if (q.status === 'quarantined' || q.isSuspect || (ex && ex.has(q.id))) continue;
    bank.push({
      id: String(q.id), committeeId: String(q.committeeId), discipline: String(q.discipline || ''), topic: String(q.topic || ''),
      number: Number(q.questionNumber) > 0 ? Number(q.questionNumber) : null, stem: String(q.stem),
      options: (q.options || []).map((o: any) => ({ key: String(o?.key || ''), text: String(o?.text || '') })),
      correctAnswer: String(q.correctAnswer || ''),
    });
  }
  const glossary = readJson<Record<string, any>>(path.join(rootDir, 'src/data/medical_glossary.json'), {});
  const diseases = readJson<any[]>(path.join(rootDir, 'src/data/disease_entities.json'), []);
  const termNames: { name: string; latin?: string }[] = [];
  const conceptPairs: { head: string; body: string }[] = [];
  for (const v of Object.values<any>(glossary)) {
    if (!v?.term) continue;
    termNames.push({ name: String(v.term) });
    if (v.definition || v.clinicalPearl) conceptPairs.push({ head: String(v.term), body: `${v.definition || ''} ${v.clinicalPearl || ''}` });
  }
  for (const d of diseases) {
    if (!d?.name) continue;
    termNames.push({ name: String(d.name), latin: d.latinName ? String(d.latinName) : undefined });
    if (d.definition || d.morphologyOrMechanism || d.examSpotPearls) {
      conceptPairs.push({ head: `${d.name} ${d.latinName || ''}`, body: `${d.definition || ''} ${d.morphologyOrMechanism || ''} ${d.examSpotPearls || ''}` });
    }
  }
  const summaries: SummaryRow[] = (opts.lectureSummaries || readJson<any[]>(path.join(rootDir, 'data/lectureSummariesCatalog.json'), []))
    .filter((sm: any) => sm?.committeeId && sm.discipline && typeof sm.content === 'string')
    .map((sm: any) => ({ committeeId: String(sm.committeeId), discipline: String(sm.discipline), title: String(sm.title || ''), content: String(sm.content) }));
  const curriculum = readJson<Record<string, string[]>>(path.join(rootDir, 'src/data/curriculum_disciplines.json'), {});
  return { bank, termNames, conceptPairs, summaries, curriculum };
}

export async function createRecallEngine(rootDir: string, opts: LoadOptions = {}): Promise<RecallEngine> {
  const tick = makeTicker();
  // `src` kurulumdan sonra bırakılır; kapanışlar yalnız türetilmiş küçük yapıları tutar
  let src: ReturnType<typeof loadSources> | null = loadSources(rootDir, opts);
  const { termNames, curriculum } = src;
  const usable = src.bank;

  const lexicon = await buildLexicon(
    (function* () {
      for (const q of usable) {
        yield q.stem;
        for (const o of q.options) yield o.text;
      }
    })(),
    termNames.map((t) => `${t.name} ${t.latin || ''}`),
    tick,
  );
  const terms = buildTermIndex(termNames);
  termNames.length = 0;

  // ------------------------------------------------ özellik çıkarımı
  const contentWords = (text: string, corrections?: [string, string][]) => {
    const out: string[] = [];
    for (const w of words(text)) {
      if (isStop(w)) continue;
      const c = lexicon.correct(w);
      if (isStop(c) || (c.length < 3 && !/\d/.test(c) && !VALID_SHORT_MED.has(c))) continue;
      if (c !== w && corrections) corrections.push([w, c]);
      out.push(c);
    }
    return out;
  };

  // IDF bankadan (+ sözlük terimleri): küçük havuzda bile kararlı ağırlık
  const df = new Map<string, number>();
  const docStems: string[][] = [];
  for (const q of usable) {
    await tick();
    const st = [...new Set(contentWords(`${q.stem} ${q.options.map((o) => o.text).join(' ')}`).map(stemOf))];
    docStems.push(st);
    for (const s of st) df.set(s, (df.get(s) || 0) + 1);
  }
  const N = usable.length || 1;
  const maxIdf = Math.log(1 + N);
  const idf = (s: string) => {
    const d = df.get(s);
    return d ? Math.log(1 + N / d) : maxIdf;
  };
  const vectorize = (stems: string[]): Vec => {
    const tf = new Map<string, number>();
    for (const s of stems) tf.set(s, (tf.get(s) || 0) + 1);
    const v: Vec = new Map();
    for (const [s, c] of tf) v.set(s, (1 + Math.log(c)) * idf(s));
    return l2(v);
  };

  const docs: BankDoc[] = [];
  for (let i = 0; i < usable.length; i++) {
    const q = usable[i];
    if ((i & 127) === 0) await tick();
    docs.push({ ...q, vec: vectorize(docStems[i]) });
  }
  const byId = new Map(docs.map((d) => [d.id, d]));
  docStems.length = 0;

  // Tıbbi kavram–tanım köprü dizini (medical_glossary + disease_entities + ders özeti tanım satırları)
  const rawConcepts = new Map<string, Map<string, number>>();
  const linkConcept = (heads: string[], body: string[], weight: number) => {
    for (const h of heads) {
      let m = rawConcepts.get(h);
      if (!m) rawConcepts.set(h, (m = new Map()));
      for (const b of body) {
        if (b === h) continue;
        m.set(b, (m.get(b) || 0) + weight * idf(b));
      }
    }
  };
  const extractConceptStems = (txt: string): string[] => {
    const out = new Set<string>();
    const f = /\d/.test(txt) ? fold(txt).replace(/(\d)([a-z]{2,})/g, '$1 $2') : fold(txt);
    for (const w0 of f.split(' ')) {
      if (w0.length < 3 || isStop(w0) || COMMON_TR.has(w0) || /^\d+$/.test(w0)) continue;
      const w = ABBREV[w0] || w0;
      const st = stemOf(w);
      if (st.length >= 4 && !GENERIC_CONCEPT_STEM.has(st)) out.add(st);
    }
    return [...out];
  };
  for (let i = 0; i < src.conceptPairs.length; i++) {
    if ((i & 255) === 0) await tick();
    const cp = src.conceptPairs[i];
    const hs = extractConceptStems(cp.head).filter((s) => idf(s) >= 3.3);
    const bs = extractConceptStems(cp.body).slice(0, 28);
    if (hs.length && bs.length >= 2) linkConcept(hs, bs, 3);
  }
  src.conceptPairs.length = 0;

  // Ders özetleri: tek geçişte hem ders vektörü (LectureDoc) hem de nadir kavram tanım bağları çıkarılır.
  // Özet metni temiz müfredat verisi olduğu için tekil sözcük sıklığı üzerinden hızlı köklenir (1,4M sözcükte Levenshtein aranmaz).
  type LectureDoc = { discipline: string; title: string; vec: Vec };
  const lectures = new Map<string, LectureDoc[]>();
  for (const sm of src.summaries) {
    await tick();
    const tf = new Map<string, number>();
    let totalStems = 0;
    const foldedLines = sm.content
      .replace(/:\s*\n+\s*/g, ': ')
      .toLocaleLowerCase('tr')
      .replace(/[ığüşöç]/g, (ch) => ({ ı: 'i', ğ: 'g', ü: 'u', ş: 's', ö: 'o', ç: 'c' }[ch] || ch))
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/(\d)([a-z]{2,})/g, '$1 $2')
      .replace(/[^a-z0-9\n]+/g, ' ')
      .split('\n');
    for (const fl of foldedLines) {
      if (!fl) continue;
      const lineSet = new Set<string>();
      for (const w0 of fl.split(' ')) {
        if (w0.length < 2 || isStop(w0)) continue;
        const w = ABBREV[w0] || w0;
        if (w.length < 3 && !/\d/.test(w) && !VALID_SHORT_MED.has(w)) continue;
        const s = stemOf(w);
        tf.set(s, (tf.get(s) || 0) + 1);
        totalStems++;
        if (w.length >= 3 && !COMMON_TR.has(w) && !/^\d+$/.test(w) && s.length >= 4 && !GENERIC_CONCEPT_STEM.has(s)) {
          lineSet.add(s);
        }
      }
      if (fl.length >= 25 && fl.length <= 420 && lineSet.size >= 3 && lineSet.size <= 26) {
        const sts = [...lineSet];
        const heads = sts.filter((s) => idf(s) >= 4.2);
        if (heads.length >= 1 && heads.length <= 6) linkConcept(heads, sts, 1);
      }
    }
    if (totalStems < 20) continue;
    const v: Vec = new Map();
    for (const [s, c] of tf) v.set(s, (1 + Math.log(c)) * idf(s));
    const top = [...l2(v)].sort((a, b) => b[1] - a[1]).slice(0, 150);
    const list = lectures.get(sm.committeeId) || lectures.set(sm.committeeId, []).get(sm.committeeId)!;
    list.push({ discipline: sm.discipline, title: sm.title, vec: l2(new Map(top)) });
  }

  const conceptDefMap = new Map<string, Set<string>>();
  for (const [h, m] of rawConcepts) {
    const top = [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, 22).map(([k]) => k);
    if (top.length >= 3) conceptDefMap.set(h, new Set(top));
  }
  rawConcepts.clear();

  // Kurul başına ters dizinler + ders merkezleri
  type Postings = Map<string, [number, number][]>;
  type CommitteeModel = {
    docs: BankDoc[]; postings: Postings;
    lec: LectureDoc[]; lecPostings: Postings;
    centroids: Map<string, Vec>; lecCentroids: Map<string, Vec>;
    prior: Map<string, number>; disciplines: string[];
  };
  const committees = new Map<string, CommitteeModel>();
  const cmFor = (cid: string) => {
    let cm = committees.get(cid);
    if (!cm) committees.set(cid, (cm = { docs: [], postings: new Map(), lec: [], lecPostings: new Map(), centroids: new Map(), lecCentroids: new Map(), prior: new Map(), disciplines: [] }));
    return cm;
  };
  const addTo = (c: Map<string, Vec>, name: string, v: Vec) => {
    const m = c.get(name) || c.set(name, new Map()).get(name)!;
    for (const [s, w] of v) m.set(s, (m.get(s) || 0) + w);
  };
  for (const d of docs) {
    await tick();
    const cm = cmFor(d.committeeId);
    const i = cm.docs.push(d) - 1;
    for (const [s, w] of d.vec) (cm.postings.get(s) || cm.postings.set(s, []).get(s)!).push([i, w]);
    if (d.discipline) { addTo(cm.centroids, d.discipline, d.vec); cm.prior.set(d.discipline, (cm.prior.get(d.discipline) || 0) + 1); }
  }
  for (const [cid, list] of lectures) {
    const cm = cmFor(cid);
    for (const L of list) {
      const i = cm.lec.push(L) - 1;
      for (const [s, w] of L.vec) (cm.lecPostings.get(s) || cm.lecPostings.set(s, []).get(s)!).push([i, w]);
      addTo(cm.lecCentroids, L.discipline, L.vec);
    }
  }
  lectures.clear();
  src = null;
  for (const [cid, cm] of committees) {
    for (const c of cm.centroids.values()) l2(c);
    for (const c of cm.lecCentroids.values()) l2(c);
    const no = /kurul\s*-?(\d+)/i.exec(cid)?.[1];
    const fromCurr = (no && curriculum[no]) || [];
    cm.disciplines = [...new Set([...fromCurr, ...cm.centroids.keys(), ...cm.lecCentroids.keys()])];
  }

  const topK = (acc: Float64Array, k: number) => {
    const top: { i: number; s: number }[] = [];
    for (let i = 0; i < acc.length; i++) {
      const s = acc[i];
      if (s <= 0.05) continue;
      if (top.length < k) { top.push({ i, s }); top.sort((a, b) => b.s - a.s); }
      else if (s > top[k - 1].s) { top[k - 1] = { i, s }; top.sort((a, b) => b.s - a.s); }
    }
    return top;
  };
  const search = (n: number, postings: Postings, v: Vec, k: number) => {
    const acc = new Float64Array(n);
    for (const [s, w] of v) for (const [i, dw] of postings.get(s) || []) acc[i] += w * dw;
    return topK(acc, k);
  };

  const P = CLASSIFY;
  const classify = (cm: CommitteeModel | undefined, v: Vec, hintWords: string[], prior?: Record<string, number> | null) => {
    if (!cm || !v.size) return { ders: [] as { name: string; p: number }[], konu: null, bank: [] as { id: string; score: number }[] };
    const knn = search(cm.docs.length, cm.postings, v, 25);
    const lknn = search(cm.lec.length, cm.lecPostings, v, 5);
    const vote = (list: { i: number; s: number }[], name: (i: number) => string) => {
      const m = new Map<string, number>();
      let t = 0;
      for (const { i, s } of list) { const d = name(i); if (!d) continue; m.set(d, (m.get(d) || 0) + s * s); t += s * s; }
      for (const [k, x] of m) m.set(k, x / (t || 1));
      return m;
    };
    const bv = vote(knn, (i) => cm.docs[i].discipline);
    const lv = vote(lknn, (i) => cm.lec[i].discipline);
    const totalPrior = [...cm.prior.values()].reduce((a, b) => a + b, 0) || 1;
    const raw = new Map<string, number>();
    for (const name of cm.disciplines) {
      const bc = cm.centroids.get(name), lc = cm.lecCentroids.get(name);
      let sc = P.bankCentroid * (bc ? dot(v, bc) : 0)
        + P.bankKnn * (bv.get(name) || 0) * Math.max(0.2, knn[0]?.s || 0)
        + P.lecCentroid * (lc ? dot(v, lc) : 0)
        + P.lecKnn * (lv.get(name) || 0) * Math.max(0.2, lknn[0]?.s || 0);
      // Büyük derslerin (patoloji) çoğunluk yanlılığını hafiflet
      sc -= P.priorPenalty * ((cm.prior.get(name) || 0) / totalPrior);
      raw.set(name, sc);
    }
    if (prior) for (const [name, w] of Object.entries(prior)) if (raw.has(name)) raw.set(name, raw.get(name)! + P.numberPrior * w);
    for (const w of hintWords) for (const [wre, dre] of DERS_HINT) if (wre.test(w)) {
      for (const name of cm.disciplines) if (dre.test(name)) raw.set(name, (raw.get(name) || 0) + P.hint);
    }
    const arr = [...raw].sort((a, b) => b[1] - a[1]);
    const mx = arr[0]?.[1] || 0;
    const ex = arr.map(([n, s]) => [n, Math.exp((s - mx) / P.temperature)] as [string, number]);
    const z = ex.reduce((a, [, e]) => a + e, 0) || 1;
    const ders = ex.map(([name, e]) => ({ name, p: Math.round((e / z) * 1000) / 1000 })).filter((x) => x.p >= 0.02).slice(0, 4);
    // Konu: seçilen dersin özet bölümlerinden ders başlığı; özet yoksa çıkmış soruların konu etiketi
    let konu: { name: string; p: number } | null = null;
    if (ders[0]) {
      const tv = new Map<string, number>();
      let tot = 0;
      for (const { i, s } of lknn) { const L = cm.lec[i]; if (L.discipline !== ders[0].name || !L.title) continue; tv.set(L.title, (tv.get(L.title) || 0) + s * s); tot += s * s; }
      if (!tot) for (const { i, s } of knn) { const d = cm.docs[i]; if (d.discipline !== ders[0].name || !d.topic) continue; tv.set(d.topic, (tv.get(d.topic) || 0) + s * s); tot += s * s; }
      const best = [...tv].sort((a, b) => b[1] - a[1])[0];
      if (best && tot > 0) konu = { name: best[0], p: Math.round((best[1] / tot) * 100) / 100 };
    }
    const bank = knn.slice(0, 5).map(({ i, s }) => ({ id: cm.docs[i].id, score: Math.round(s * 1000) / 1000 }));
    return { ders, konu, bank };
  };

  const analyze: RecallEngine['analyze'] = (text, o) => {
    const corrections: [string, string][] = [];
    const lettered = letteredOptions(text);
    const unlettered = lettered.length ? [] : unletteredOptions(text);
    const formOpts = (o.options || []).filter((x) => x?.text?.trim());
    const options = [
      ...formOpts.map((x) => ({ harf: (/^[A-E]$/.test(String(x.key || '')) ? x.key : null) as Letter | null, metin: x.text.trim() })),
      ...lettered.filter((l) => !formOpts.some((f) => f.key === l.harf)),
      ...unlettered.map((m) => ({ harf: null, metin: m })),
    ];
    const all = `${text} ${formOpts.map((x) => x.text).join(' ')}`;
    const w = contentWords(all, corrections);
    const stems = w.map(stemOf);
    const vec = vectorize(stems);
    const role = classifyRecallRole(text);
    const stemClause = role === 'options' || role === 'claim' ? '' : extractStemClause(text);
    const stemWords = stemClause ? contentWords(stemClause) : role === 'stem' ? w : [];
    const stemStems = stemWords.map(stemOf);
    const stemVec = stemStems.length ? vectorize(stemStems) : new Map();
    const tset = matchTermsInWords(w, terms);
    // Bilgi taşıyan: bankada geçen (df ≥ 1), yaygın olmayan sözcük ya da tıbbi terim; bilinmeyen sözcük sayılmaz
    const informative = w.filter((x) => {
      const s = stemOf(x);
      return df.has(s) && idf(s) >= 2.2 && !/^\d+$/.test(x) && !COMMON_TR.has(x) && !AREA_RE.test(x) && !DERS_HINT.some(([re]) => re.test(x));
    }).length;
    // Yalnız cevap ("C dedim", "II ve IV C") ya da kısaltma ("MS sorusu") taşıyan mesaj gürültü değildir
    const hasAbbr = /\b[A-ZÇĞİÖŞÜ]{2,6}\b/.test(text.replace(/\b(?:I{1,3}|IV|V)\b/g, ''));
    const isRoman = /\b(?:I{1,3}|IV)\b(?:\s*(?:,|ve|veya|-|\.)\s*\b(?:I{1,3}|IV)\b)+|\b(?:yaln[ıi]z|yalniz)\s+(?:I{1,3}|IV)\b|\b(?:I\.\s+\S[\s\S]*II\.\s+\S)|\b(?:[uü][cç]l[uü]|d[oö]rtl[uü])\s+(?:[oö]nc[uü]l|[oö]nerme)\b/i.test(text);
    const claimAny = !!(claimedLetter(text) || claimedText(text) || isRoman);
    const isNoise = !tset.length && informative === 0 && !hasAbbr && !claimAny && !options.length && !questionNumber(text);
    const cm = committees.get(o.committeeId);
    const cls = isNoise ? { ders: [], konu: null, bank: [] } : classify(cm, vec, words(text), o.dersPrior);
    const claimL = (/^[A-E]$/.test(String(o.claimed || '')) ? (o.claimed as Letter) : null) || claimedLetter(text);
    return {
      words: w,
      stemWords,
      clean: w.map((x) => lexicon.display(x)).join(' '),
      stems,
      stemStems,
      vec,
      stemVec,
      role,
      isRoman,
      terms: tset,
      number: questionNumber(text),
      claimedLetter: claimL,
      claimedText: claimL ? null : claimedText(text),
      options,
      negative: negativeLikelihood(text),
      isNoise,
      ders: cls.ders,
      konu: cls.konu,
      bank: cls.bank,
      corrections,
    };
  };

  return {
    version: RECALL_ENGINE_VERSION,
    bankSize: docs.length,
    lexicon,
    terms,
    analyze,
    cleanSentence: (text) => cleanSentence(text, (f, raw) => {
      const c = lexicon.correct(f);
      const d = lexicon.display(c);
      // Büyük harfle başlayan özel adları koru ("Wilms", "Kongo")
      return /^[A-ZÇĞİÖŞÜ]/.test(raw) ? d.charAt(0).toLocaleUpperCase('tr') + d.slice(1) : d;
    }),
    searchBank: (vec, cid, k = 5) => {
      const cm = committees.get(cid);
      if (!cm || !vec.size) return [];
      return search(cm.docs.length, cm.postings, vec, k).map(({ i, s: sc }) => ({ id: cm.docs[i].id, score: Math.round(sc * 1000) / 1000 }));
    },
    disciplinesOf: (cid) => committees.get(cid)?.disciplines || [],
    bankDoc: (id) => byId.get(id),
    idf,
    conceptDefs: (stem) => conceptDefMap.get(stem),
  };
}

let shared: { root: string; key: string; builtAt: number; engine: Promise<RecallEngine> } | null = null;
/**
 * Sunucu için paylaşılan motor. Banka değişince (anahtar: kayıt sayısı + dosya zamanı) en geç 10 dk sonra yeniden
 * kurulur; kurulum dilimlidir (olay döngüsü kilitlenmez), kurulurken eski motor kullanılmaya devam eder.
 */
export function getRecallEngine(rootDir: string, getPastQuestions?: () => any[]): Promise<RecallEngine> {
  let mtime = 0;
  try { mtime = fs.statSync(path.join(rootDir, 'data/pastQuestions.json')).mtimeMs; } catch { /* yok */ }
  const list = getPastQuestions?.();
  const key = `${list?.length ?? -1}:${mtime}`;
  if (shared && shared.root === rootDir && (shared.key === key || Date.now() - shared.builtAt < 10 * 60_000)) return shared.engine;
  const prev = shared?.engine;
  const next = createRecallEngine(rootDir, list ? { pastQuestions: list } : {});
  shared = { root: rootDir, key, builtAt: Date.now(), engine: prev ? next.catch(() => prev) : next };
  // Kurulum bitene kadar eskisi
  if (prev) return prev.then((p) => p, () => next);
  return shared.engine;
}

/**
 * Sınavın kendi sırasından ders ön bilgisi. Kurullar soruları ders blokları hâlinde sorar ama blok sırası yıldan yıla
 * değişir; bu yüzden aynı sınavın (havuzun) numarası bilinen sorularına bakılır. Ölçüm (15 gerçek sınav dökümü,
 * numaralı soruların yalnız %20'si biliniyorken): komşu oyu %74, iki yandaki en yakın komşu aynı dersse %90 isabet.
 */
export function numberDersPrior(known: { number: number; ders: string }[], n: number | null | undefined): Record<string, number> | null {
  if (!n || !known.length) return null;
  let lo: { number: number; ders: string } | null = null, hi: { number: number; ders: string } | null = null;
  const w = new Map<string, number>();
  for (const k of known) {
    const d = Math.abs(k.number - n);
    if (!d || d > 3) continue;
    w.set(k.ders, (w.get(k.ders) || 0) + 1 / d);
    if (k.number < n && (!lo || k.number > lo.number)) lo = k;
    if (k.number > n && (!hi || k.number < hi.number)) hi = k;
  }
  if (lo && hi && lo.ders === hi.ders) return { [lo.ders]: 1 };
  const tot = [...w.values()].reduce((a, b) => a + b, 0);
  if (!tot) return null;
  // Tek yandan ya da karışık komşuluk: daha zayıf (ölçümde %74)
  return Object.fromEntries([...w].map(([d, x]) => [d, (0.6 * x) / tot]));
}
