/**
 * Sorgu zekâsı — sunucu çalışma zamanı (server-only).
 *
 *  - Paket (data/search/query-intel.{json,bin}) açılıştan sonra gecikmeli ve asenkron okunur; hazır değilse uçlar
 *    boş/eskiye düşer, istek asla beklemez.
 *  - Paket dosyası değişince (en çok 30 sn'de bir stat) arka planda yeniden yüklenir.
 *  - Derleme sunucu sürecinde YAPILMAZ: `scripts/search/build-query-intel.mts` düşük öncelikli (nice 15) alt süreç
 *    olarak açılışta ve 6 saatte bir çağrılır; imza aynıysa ~1 sn'de çıkar. Kilit dosyasıyla tek kopya.
 *  - Öneri/anlamlandırma sonuçları küçük LRU önbellekte tutulur.
 */
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { QueryIntelEngine, decodeBins, type QueryUnderstanding, type Suggestion, type SpellResult } from './engine';

const ROOT = path.resolve(process.env.MEDS_APP_DIR || process.cwd());
const OUT_DIR = path.join(ROOT, 'data', 'search');
const JSON_PATH = path.join(OUT_DIR, 'query-intel.json');
const BIN_PATH = path.join(OUT_DIR, 'query-intel.bin');
const LOCK_PATH = path.join(OUT_DIR, '.build.lock');

let engine: QueryIntelEngine | null = null;
let loadedMtime = 0;
let loading: Promise<void> | null = null;
let lastStat = 0;
let lastError = '';
let building = false;
let lastBuild: { at: string; ok: boolean; ms: number; out: string } | null = null;

class Lru<V> {
  private m = new Map<string, V>();
  constructor(private max: number) {}
  get(k: string): V | undefined {
    const v = this.m.get(k);
    if (v !== undefined) { this.m.delete(k); this.m.set(k, v); }
    return v;
  }
  set(k: string, v: V): void {
    if (this.m.has(k)) this.m.delete(k);
    this.m.set(k, v);
    if (this.m.size > this.max) this.m.delete(this.m.keys().next().value as string);
  }
  clear(): void { this.m.clear(); }
}

const suggestCache = new Lru<SuggestPayload>(3000);
const analyzeCache = new Lru<QueryUnderstanding>(2000);

async function load(): Promise<void> {
  try {
    const st = await fs.promises.stat(JSON_PATH);
    const [jsonText, bin] = await Promise.all([fs.promises.readFile(JSON_PATH, 'utf-8'), fs.promises.readFile(BIN_PATH)]);
    const pack = JSON.parse(jsonText);
    const next = new QueryIntelEngine(pack, decodeBins(new Uint8Array(bin.buffer, bin.byteOffset, bin.byteLength)));
    engine = next;
    loadedMtime = st.mtimeMs;
    lastError = '';
    suggestCache.clear();
    analyzeCache.clear();
    console.log(`[query-intel] yüklendi: ${next.words.length} sözcük, ${next.concepts.length} kavram (${pack.builtAt})`);
  } catch (e: any) {
    lastError = e?.code === 'ENOENT' ? 'paket yok (derleme bekleniyor)' : String(e?.message || e);
  }
}

function maybeReload(): void {
  const now = Date.now();
  if (loading || now - lastStat < 30_000) return;
  lastStat = now;
  fs.stat(JSON_PATH, (err, st) => {
    if (err || st.mtimeMs === loadedMtime || loading) return;
    loading = load().finally(() => { loading = null; });
  });
}

/** Motor hazırsa döner; değilse null (yüklemeyi arka planda başlatır). */
export function getQueryIntel(): QueryIntelEngine | null {
  if (!engine && !loading) {
    lastStat = Date.now();
    loading = load().finally(() => { loading = null; });
  } else maybeReload();
  return engine;
}

/** Derleyiciyi düşük öncelikli alt süreç olarak çalıştırır (imza aynıysa hemen çıkar). */
export function runQueryIntelBuild(opts: { force?: boolean; graph?: boolean } = {}): Promise<{ ok: boolean; out: string }> {
  if (building) return Promise.resolve({ ok: false, out: 'zaten derleniyor' });
  try {
    fs.mkdirSync(OUT_DIR, { recursive: true });
    // Başka bir süreç (ör. ikinci sunucu kopyası) derliyorsa ve kilit 20 dk'dan yeni ise atla
    const st = fs.existsSync(LOCK_PATH) ? fs.statSync(LOCK_PATH) : null;
    if (st && Date.now() - st.mtimeMs < 20 * 60_000) return Promise.resolve({ ok: false, out: 'kilitli' });
    fs.writeFileSync(LOCK_PATH, String(process.pid));
  } catch { /* kilit yazılamazsa yine de dene */ }
  building = true;
  const t0 = Date.now();
  const tsx = path.join(ROOT, 'node_modules', '.bin', 'tsx');
  const args = [tsx, path.join(ROOT, 'scripts', 'search', 'build-query-intel.mts')];
  if (opts.force) args.push('--force');
  if (opts.graph === false) args.push('--no-graph');
  return new Promise((resolve) => {
    let out = '';
    const child = spawn('nice', ['-n', '15', process.execPath, '--max-old-space-size=3072', ...args], {
      cwd: ROOT,
      env: { ...process.env, CUDA_VISIBLE_DEVICES: '' },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    const take = (b: Buffer) => { out = (out + b.toString()).slice(-4000); };
    child.stdout.on('data', take);
    child.stderr.on('data', take);
    const done = (ok: boolean) => {
      building = false;
      try { fs.unlinkSync(LOCK_PATH); } catch { /* yok */ }
      lastBuild = { at: new Date().toISOString(), ok, ms: Date.now() - t0, out: out.slice(-1500) };
      if (ok) { lastStat = 0; maybeReload(); }
      if (!ok) console.warn('[query-intel] derleme başarısız:', out.slice(-600));
      resolve({ ok, out });
    };
    child.on('error', () => done(false));
    child.on('exit', (code) => done(code === 0));
  });
}

/** Açılışta: önce var olan paketi yükle, sonra (derlem yeniden yazımı bitsin diye) gecikmeli imza kontrolü + 6 saatte bir. */
export function startQueryIntel(): void {
  setTimeout(() => getQueryIntel(), 5_000);
  if (process.env.MEDS_QUERY_INTEL_AUTOBUILD === '0') return;
  setTimeout(() => { runQueryIntelBuild().catch(() => {}); }, 120_000).unref?.();
  setInterval(() => { runQueryIntelBuild().catch(() => {}); }, 6 * 3600_000).unref?.();
}

export function queryIntelStatus() {
  return {
    ready: Boolean(engine),
    builtAt: engine?.builtAt || null,
    words: engine?.words.length || 0,
    concepts: engine?.concepts.length || 0,
    building,
    lastBuild,
    error: lastError || null,
  };
}

// ------------------------------------------------------------------ uç yardımcıları

export interface SuggestPayload {
  q: string;
  ready: boolean;
  suggestions: Suggestion[];
  correction: SpellResult | null;
  concepts: QueryUnderstanding['concepts'];
  intent: QueryUnderstanding['intent'];
  /** Soluk devam metni (yalnız güvenli devamlar) */
  ghost: string;
}

export function suggestFor(q: string, limit = 8): SuggestPayload {
  const text = q.slice(0, 300);
  const key = `${limit}|${text}`;
  const hit = suggestCache.get(key);
  if (hit) return hit;
  const eng = getQueryIntel();
  if (!eng || !text.trim()) return { q: text, ready: Boolean(eng), suggestions: [], correction: null, concepts: [], intent: null, ghost: '' };
  const a = analyzeFor(text);
  // Yazarken yarım son sözcük düzeltilmez (kullanıcı yazmayı bitirmedi); düzeltme yalnız tamamlanmış sözcüklerde
  const typingLast = !/\s$/.test(text);
  const changes = typingLast ? a.changes.filter((c) => !text.trimEnd().endsWith(c.from)) : a.changes;
  let corrected: string | null = null;
  if (changes.length) {
    corrected = text;
    for (const c of changes) corrected = corrected.replace(c.from, c.to);
  }
  const payload: SuggestPayload = {
    q: text,
    ready: true,
    // Tamamlanmış sözcüklerde düzeltme varsa öneriler düzeltilmiş metin üzerinden ("bobrek tumoru ted" → "böbrek tümörü tedavisi")
    suggestions: [
      // Diğer öğrencilerin sık yaptığı (≥3 kez, sonuçlu) aramalar başta
      ...popularFor(text).map((pq) => ({ kind: 'word' as const, value: pq, label: pq, score: 99 })),
      ...eng.complete(corrected ?? text, limit),
    ].slice(0, limit),
    correction: corrected ? { text: corrected, changes } : null,
    concepts: a.concepts.slice(0, 4),
    intent: a.intent,
    ghost: eng.completeSentence(text, 5),
  };
  suggestCache.set(key, payload);
  return payload;
}

export function analyzeFor(q: string): QueryUnderstanding {
  const text = q.slice(0, 500);
  const hit = analyzeCache.get(text);
  if (hit) return hit;
  const eng = getQueryIntel();
  const res: QueryUnderstanding = eng
    ? eng.analyze(text)
    : { query: text, corrected: null, changes: [], concepts: [], intent: null, rewrites: [], focus: [], slots: [] };
  if (eng) analyzeCache.set(text, res);
  return res;
}

/** Soru yazma yardımcısı: soluk cümle devamı + sonraki sözcük önerileri + yazım düzeltmesi */
export function composeAssist(text: string): { ready: boolean; ghost: string; next: string[]; correction: SpellResult | null } {
  const eng = getQueryIntel();
  if (!eng) return { ready: false, ghost: '', next: [], correction: null };
  const t = text.slice(-600);
  const ghost = eng.completeSentence(t, 8);
  const next = eng.complete(t, 5).map((s) => s.value.slice(t.length - (t.length - t.trimEnd().length))).filter(Boolean);
  const spell = eng.correct(text.slice(0, 2000), 0.6);
  return { ready: true, ghost, next: next.slice(0, 5), correction: spell.text ? spell : null };
}

// ------------------------------------------------------------------ anonim sorgu günlüğü
/**
 * Yalnız sorgu metni + sonuç sayısı + zaman (kimlik/IP yok). Amaç: sonuçsuz / az sonuçlu aramaları veri eksiği olarak
 * görmek ve sık aranan (≥3 kez, sonuç veren) sorguları öneri olarak sunmak. data/search/query_log.json, en çok 5000 kayıt,
 * 5 dk'da bir ve yalnız değişince yazılır.
 */
interface LogEntry { q: string; n: number; total: number; zero: number; last: string }
const LOG_PATH = path.join(OUT_DIR, 'query_log.json');
let qlog: Map<string, LogEntry> | null = null;
let qlogDirty = false;
let popular: Array<{ k: string; e: LogEntry }> = [];

function loadLog(): Map<string, LogEntry> {
  if (qlog) return qlog;
  qlog = new Map();
  try {
    for (const e of JSON.parse(fs.readFileSync(LOG_PATH, 'utf-8')) as LogEntry[]) qlog.set(logKey(e.q), e);
  } catch { /* ilk çalışma */ }
  rebuildPopular();
  return qlog;
}
const logKey = (q: string) => q.toLocaleLowerCase('tr-TR').replace(/\s+/g, ' ').trim();
function rebuildPopular(): void {
  popular = [...(qlog?.entries() || [])]
    .filter(([, e]) => e.n >= 3 && e.total > 0)
    .map(([k, e]) => ({ k, e }))
    .sort((a, b) => (a.k < b.k ? -1 : a.k > b.k ? 1 : 0));
}

export function logSearch(q: string, total: number): void {
  const text = q.trim().slice(0, 120);
  if (text.length < 2 || /^".*"$/.test(text)) return;
  const m = loadLog();
  const k = logKey(text);
  const e = m.get(k) || { q: text, n: 0, total: 0, zero: 0, last: '' };
  e.n++;
  e.total = total;
  if (total === 0) e.zero++;
  e.last = new Date().toISOString();
  m.set(k, e);
  if (m.size > 5000) {
    // en eski ve en az aranan kayıtlar atılır
    const drop = [...m.entries()].sort((a, b) => a[1].n - b[1].n || (a[1].last < b[1].last ? -1 : 1)).slice(0, 500);
    for (const [dk] of drop) m.delete(dk);
  }
  qlogDirty = true;
}

setInterval(() => {
  if (!qlogDirty || !qlog) return;
  qlogDirty = false;
  rebuildPopular();
  fs.promises.mkdir(OUT_DIR, { recursive: true })
    .then(() => fs.promises.writeFile(LOG_PATH + '.tmp', JSON.stringify([...qlog!.values()])))
    .then(() => fs.promises.rename(LOG_PATH + '.tmp', LOG_PATH))
    .catch(() => { qlogDirty = true; });
}, 5 * 60_000).unref?.();

/** Öneri: sık aranan (≥3, sonuçlu) ve yazılanla başlayan sorgular */
export function popularFor(text: string, limit = 2): string[] {
  loadLog();
  const k = logKey(text);
  if (k.length < 3) return [];
  let lo = 0;
  let hi = popular.length;
  while (lo < hi) { const mid = (lo + hi) >>> 1; if (popular[mid].k < k) lo = mid + 1; else hi = mid; }
  const out: LogEntry[] = [];
  for (let i = lo; i < popular.length && popular[i].k.startsWith(k); i++) if (popular[i].k !== k) out.push(popular[i].e);
  return out.sort((a, b) => b.n - a.n).slice(0, limit).map((e) => e.q);
}

/** Yönetici özeti: en çok arananlar, sonuçsuzlar (veri eksiği adayı), az sonuçlular */
export function searchLogSummary() {
  const all = [...loadLog().values()];
  const by = (f: (e: LogEntry) => boolean, sort: (a: LogEntry, b: LogEntry) => number) => all.filter(f).sort(sort).slice(0, 50);
  return {
    distinct: all.length,
    searches: all.reduce((a, e) => a + e.n, 0),
    top: by(() => true, (a, b) => b.n - a.n),
    zeroResult: by((e) => e.zero > 0 && e.total === 0, (a, b) => b.zero - a.zero),
    lowResult: by((e) => e.total > 0 && e.total < 3, (a, b) => b.n - a.n),
  };
}
