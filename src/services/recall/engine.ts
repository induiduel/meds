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
  fold, words, isStop, DERS_HINT, claimedLetter, claimedText, questionNumber, letteredOptions, unletteredOptions,
  negativeLikelihood, cleanSentence, type Letter,
} from './normalize.ts';
import { buildLexicon, buildTermIndex, matchTermsInWords, makeTicker, COMMON_TR, type Lexicon, type TermIndex } from './lexicon.ts';

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
  /** Okunur temiz metin (aksanlı, sohbetsiz, düzeltilmiş). */
  clean: string;
  stems: string[];
  vec: Vec;
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
const stemOf = (w: string) => (/^\d/.test(w) ? w : w.slice(0, 5));

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
export const CLASSIFY = { bankCentroid: 0.4, bankKnn: 0.4, lecCentroid: 0.2, lecKnn: 0, priorPenalty: 0, hint: 0.25, temperature: 0.06 };

export interface RecallEngine {
  version: string;
  bankSize: number;
  lexicon: Lexicon;
  terms: TermIndex;
  analyze: (text: string, opts: { committeeId: string; options?: { key?: string | null; text: string }[]; claimed?: string | null }) => Analysis;
  /** Öğrenci metnini okunur cümleye çevirir (sohbet/iddia/no atılır, yazım düzeltilir; bilgi eklenmez). */
  cleanSentence: (text: string) => string;
  /** Kurul içinde çıkmış soru araması (küme merkezi vb. için). */
  searchBank: (vec: Vec, committeeId: string, k?: number) => { id: string; score: number }[];
  disciplinesOf: (committeeId: string) => string[];
  bankDoc: (id: string) => BankDoc | undefined;
  idf: (stem: string) => number;
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
  for (const v of Object.values<any>(glossary)) if (v?.term) termNames.push({ name: String(v.term) });
  for (const d of diseases) if (d?.name) termNames.push({ name: String(d.name), latin: d.latinName ? String(d.latinName) : undefined });
  const summaries: SummaryRow[] = (opts.lectureSummaries || readJson<any[]>(path.join(rootDir, 'data/lectureSummariesCatalog.json'), []))
    .filter((sm: any) => sm?.committeeId && sm.discipline && typeof sm.content === 'string')
    .map((sm: any) => ({ committeeId: String(sm.committeeId), discipline: String(sm.discipline), title: String(sm.title || ''), content: String(sm.content) }));
  const curriculum = readJson<Record<string, string[]>>(path.join(rootDir, 'src/data/curriculum_disciplines.json'), {});
  return { bank, termNames, summaries, curriculum };
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
      if (isStop(c) || (c.length < 3 && !/\d/.test(c))) continue;
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

  // Ders özetleri (her ders bir belge: ders + kurul + ders başlığı = konu). Sınıflayıcının ikinci bilgi kaynağı.
  type LectureDoc = { discipline: string; title: string; vec: Vec };
  const lectures = new Map<string, LectureDoc[]>();
  for (const sm of src.summaries) {
    // Ders başına tek vektör (en ağırlıklı 150 kök): sınıflama için ders merkezi, konu için ders başlığı
    await tick();
    const st = contentWords(sm.content).map(stemOf);
    if (st.length < 20) continue;
    const top = [...vectorize(st)].sort((a, b) => b[1] - a[1]).slice(0, 150);
    const list = lectures.get(sm.committeeId) || lectures.set(sm.committeeId, []).get(sm.committeeId)!;
    list.push({ discipline: sm.discipline, title: sm.title, vec: l2(new Map(top)) });
  }

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
  const classify = (cm: CommitteeModel | undefined, v: Vec, hintWords: string[]) => {
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
    const tset = matchTermsInWords(w, terms);
    // Bilgi taşıyan: bankada geçen (df ≥ 1), yaygın olmayan sözcük ya da tıbbi terim; bilinmeyen sözcük sayılmaz
    const informative = w.filter((x) => {
      const s = stemOf(x);
      return df.has(s) && idf(s) >= 2.2 && !/^\d+$/.test(x) && !COMMON_TR.has(x) && !AREA_RE.test(x) && !DERS_HINT.some(([re]) => re.test(x));
    }).length;
    // Yalnız cevap ("C dedim", "II ve IV C") ya da kısaltma ("MS sorusu") taşıyan mesaj gürültü değildir
    const hasAbbr = /\b[A-ZÇĞİÖŞÜ]{2,6}\b/.test(text.replace(/\b(?:I{1,3}|IV|V)\b/g, ''));
    const claimAny = !!(claimedLetter(text) || claimedText(text) || /\b(?:I{1,3}|IV|V)\b(?:\s*(?:,|ve)\s*(?:I{1,3}|IV|V)\b)+/.test(text));
    const isNoise = !tset.length && informative === 0 && !hasAbbr && !claimAny && !questionNumber(text);
    const cm = committees.get(o.committeeId);
    const cls = isNoise ? { ders: [], konu: null, bank: [] } : classify(cm, vec, words(text));
    const claimL = (/^[A-E]$/.test(String(o.claimed || '')) ? (o.claimed as Letter) : null) || claimedLetter(text);
    return {
      words: w,
      clean: w.map((x) => lexicon.display(x)).join(' '),
      stems,
      vec,
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
