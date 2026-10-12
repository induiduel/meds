/**
 * Veri kataloğu (yönetim) — sunucu tarafı. Uygulamadaki her veri türü tek arayüzle:
 *  - listelenir, aranır, sınıflara (facet) göre süzülür ve sıralanır,
 *  - tek kayıt olarak açılır; izin verilen alanları düzenlenir (yedekli, atomik yazma),
 *  - ayrı ayrı DEĞERLENDİRİLİR ve SINIFLANDIRILIR: durum (onaylı / inceleme / sorunlu), etiketler, not.
 *    Bu "açıklama katmanı" kaynak veriyi değiştirmez; data/catalog_annotations.json'da tutulur.
 *  - ilişkileri gösterilir: deste ↔ kazanım ↔ örnek soru ↔ çıkmış soru ↔ sözlük terimi ↔ hastalık.
 *
 * Yeni kayıt / çoğaltma: CREATE'teki şablon (form alanları + kayıt iskeleti) olan türlerde açıktır; yeni kayıt
 * o türün mevcut kayıt biçimine uygun kurulur, çoğaltılan kayıt aslının hemen arkasına eklenir.
 * Yeni veri türü eklemek = ENTITIES listesine bir bağdaştırıcı. Ham dosya biçimi (girinti) korunarak yazılır.
 * server.ts yalnız registerDataCatalogRoutes(app, requireAdmin, deps) çağırır.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import type express from 'express';
import { mergeSiblings } from './questionMerge.ts';

type Any = Record<string, any>;

export interface CatalogDeps {
  rootDir: string;
  dataDir: string;
  getPastQuestions: () => any[];
  savePastQuestions: (list: any[]) => void;
  /** Sitede gösterilen çıkmış listesi (karantina + birleştirme katmanı uygulanmış) — kayıt sitede mi, hangi kopya görünüyor */
  getServedPast?: () => any[];
  getDecks: () => any[];
  /** Bellekte tutulan türlerin silme/geri yükleme yolları (server.ts sağlar; silinen kayıtları döndürür) */
  removePast?: (ids: string[]) => Promise<any[]>;
  restorePast?: (records: any[]) => Promise<void>;
  removePool?: (ids: string[]) => Promise<any[]>;
  restorePool?: (records: any[]) => Promise<void>;
  removeLearnFeedback?: (ids: string[]) => any[];
  restoreLearnFeedback?: (records: any[]) => void;
  /** Yönetici seçkisi dosyası (data/ altında, yoksa tohumlanır) */
  musicFile?: () => string;
  /** Bir türde kayıt eklendi/değişti/silindi → istemcilere canlı yayın */
  onChange?: (entity: string) => void;
}

export interface RelationRef { entity: string; id: string; title: string; why: string }

interface EntityDef {
  id: string;
  label: string;
  group: 'Sorular' | 'Öğrenme' | 'Kaynaklar' | 'Topluluk';
  source: string;
  /** Düzenlenebilir üst düzey alanlar (boşsa salt okunur; açıklama katmanı yine çalışır) */
  editable: string[];
  /** Dizi alanları (etiket gibi; virgülle girilir) */
  arrays?: string[];
  facets: { key: string; label: string }[];
  load: () => any[];
  key: (x: Any) => string;
  title: (x: Any) => string;
  subtitle?: (x: Any) => string;
  facet: (x: Any, key: string) => string | string[] | undefined;
  text: (x: Any) => string;
  save?: (id: string, patch: Any) => Any;
  relations?: (x: Any) => RelationRef[];
  /** Kayıtları kaynaktan kaldırır, kaldırılanları (çöp kutusu için tam haliyle) döndürür */
  remove?: (ids: string[]) => Any[] | Promise<Any[]>;
  /** Çöp kutusundaki kayıtları kaynağa geri koyar */
  restore?: (records: Any[]) => void | Promise<void>;
}

/** Çöp kutusu kaydı: silinen kaydın tamamı burada durur; geri yüklenebilir ya da kalıcı silinir. */
interface TrashEntry { key: string; entity: string; id: string; title: string; record: Any; deletedAt: string; by?: string }

const fold = (s: unknown) =>
  String(s ?? '')
    .toLocaleLowerCase('tr')
    .replace(/[çğıöşüâîû]/g, (c) => ({ ç: 'c', ğ: 'g', ı: 'i', ö: 'o', ş: 's', ü: 'u', â: 'a', î: 'i', û: 'u' } as Any)[c] || c);
const clip = (s: unknown, n = 140) => {
  const t = String(s ?? '').replace(/\s+/g, ' ').trim();
  return t.length > n ? t.slice(0, n - 1) + '…' : t;
};

/* ---------- dosya yardımcıları (mtime önbellekli okuma, girintiyi koruyan atomik yazma + yedek) ---------- */
const fileCache = new Map<string, { mtime: number; data: any }>();
function readJson(file: string, fallback: any) {
  try {
    const st = fs.statSync(file);
    const c = fileCache.get(file);
    if (c && c.mtime === st.mtimeMs) return c.data;
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));
    fileCache.set(file, { mtime: st.mtimeMs, data });
    return data;
  } catch {
    return fallback;
  }
}
/** Dosya boşalınca ("[]") girinti okunamaz; son bilinen girinti hatırlanır. */
const knownIndent = new Map<string, number>();
function detectIndent(file: string): number {
  const n = detectIndentRaw(file);
  if (n) knownIndent.set(file, n);
  return n || knownIndent.get(file) || (/^\s*[\[{]\s*[\]}]\s*$/.test(safeHead(file)) ? 2 : 0);
}
function safeHead(file: string): string {
  try { return fs.readFileSync(file, 'utf8').slice(0, 20); } catch { return ''; }
}
function detectIndentRaw(file: string): number {
  try {
    const fd = fs.openSync(file, 'r');
    const buf = Buffer.alloc(200);
    fs.readSync(fd, buf, 0, 200, 0);
    fs.closeSync(fd);
    const m = buf.toString('utf8').match(/\n( +)\S/);
    return m ? m[1].length : 0;
  } catch {
    return 2;
  }
}
function writeJsonAtomic(file: string, data: any, backupDir: string) {
  const indent = detectIndent(file);
  fs.mkdirSync(backupDir, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  if (fs.existsSync(file)) fs.copyFileSync(file, path.join(backupDir, `${path.basename(file)}.${stamp}.bak`));
  const tmp = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, indent || undefined) + (indent ? '\n' : ''), 'utf8');
  fs.renameSync(tmp, file);
  fileCache.delete(file);
  // Yedek klasörü şişmesin: dosya başına son 10 yedek kalır
  const prefix = path.basename(file) + '.';
  const olds = fs.readdirSync(backupDir).filter((f) => f.startsWith(prefix)).sort();
  for (const f of olds.slice(0, Math.max(0, olds.length - 10))) fs.unlinkSync(path.join(backupDir, f));
}

/** Yalnız izin verilen alanları uygular; dizi alanları virgüllü metinden diziye çevrilir. */
/** Çıkmış sorunun site metni önce `reconstruction`dan okunur: kök/cevap/açıklama düzeltmesi oraya da yazılmalı. */
const PAST_SHARED_FIELDS = ['stem', 'correctAnswer', 'explanation', 'topic', 'discipline', 'committeeId'];
function syncPastReconstruction(q: Any, patch: Any) {
  const rec = q.reconstruction;
  if (!rec || typeof rec !== 'object') return;
  if ('stem' in patch) rec.stem = q.stem;
  if ('explanation' in patch) rec.explanation = q.explanation;
  if ('correctAnswer' in patch) {
    rec.correctAnswer = q.correctAnswer;
    for (const list of [rec.options, q.options]) {
      if (Array.isArray(list)) for (const o of list) if (o && typeof o === 'object' && 'isCorrect' in o) o.isCorrect = o.key === q.correctAnswer;
    }
  }
  rec.updatedAt = q.updatedAt;
}

function applyPatch(target: Any, patch: Any, editable: string[], arrays: string[] = []) {
  for (const k of Object.keys(patch || {})) {
    if (!editable.includes(k)) continue;
    let v = patch[k];
    if (arrays.includes(k) && typeof v === 'string') v = v.split(',').map((s) => s.trim()).filter(Boolean);
    target[k] = v;
  }
  target.updatedAt = new Date().toISOString();
  return target;
}

/* ---------- yeni kayıt / çoğaltma şablonu ---------- */
export interface FormField {
  key: string;
  label: string;
  /** text: tek satır · long: çok satır · number · options: A–E şıkları · choice: seçenekli · list: virgüllü dizi */
  kind?: 'text' | 'long' | 'number' | 'options' | 'choice' | 'list';
  required?: boolean;
  choices?: string[] | (() => string[]);
  /** choice alanında listede olmayan değer de yazılabilir mi */
  free?: boolean;
  hint?: string;
}
interface CreateDef {
  fields: FormField[];
  /** kayıt → form değerleri (çoğaltmada formu doldurur) */
  toForm: (x: Any) => Any;
  /** form değerleri (+ çoğaltılan asıl kayıt) → türün biçimine uygun yeni kayıt; hatalı girişte Error fırlatır */
  build: (v: Any, base?: Any) => Any;
  /** yazar; afterId verilirse yeni kayıt aslının arkasına konur */
  insert: (rec: Any, afterId?: string) => void;
}
const OPTION_KEYS = ['A', 'B', 'C', 'D', 'E'];
const str = (v: unknown) => String(v ?? '').trim();
const hexId = (n = 12) => crypto.randomBytes(Math.ceil(n / 2)).toString('hex').slice(0, n);
const slug = (s: string) => fold(s).replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60) || 'kayit';
const uniqueKey = (base: string, taken: (k: string) => boolean) => {
  if (!taken(base)) return base;
  for (let i = 2; ; i++) if (!taken(`${base}-${i}`)) return `${base}-${i}`;
};
const listOf = (v: unknown) => (Array.isArray(v) ? v : String(v ?? '').split(',')).map((x) => String(x).trim()).filter(Boolean);
const clone = <T,>(x: T): T => JSON.parse(JSON.stringify(x));
/** A–E şıkları: boşluksuz A'dan başlamalı; cevap doldurulmuş bir şıkkı göstermeli */
function readOptions(v: Any, answerKey: string, min = 2) {
  const raw = (v.options || {}) as Any;
  const opts = OPTION_KEYS.map((k) => ({ key: k, text: str(raw[k]) }));
  const lastFilled = opts.map((o) => !!o.text).lastIndexOf(true);
  const filled = opts.slice(0, lastFilled + 1);
  if (filled.some((o) => !o.text)) throw new Error("Şıklar A'dan başlayıp arada boşluk bırakmadan doldurulmalı.");
  if (filled.length < min) throw new Error(`En az ${min} şık gerekli.`);
  const ans = str(v[answerKey]).toUpperCase();
  if (ans && !filled.some((o) => o.key === ans)) throw new Error(`Doğru cevap (${ans}) doldurulmuş şıklardan biri olmalı.`);
  return { opts: filled, ans };
}
function checkRequired(fields: FormField[], v: Any) {
  for (const f of fields) {
    if (!f.required || f.kind === 'options') continue;
    const val = v[f.key];
    if (f.kind === 'list' ? !listOf(val).length : !str(val)) throw new Error(`"${f.label}" boş bırakılamaz.`);
  }
}
/** YouTube paylaşım / watch / embed / shorts bağlantısından videoId + listId */
function parseYouTubeUrl(input: string): { videoId?: string; listId?: string } | null {
  const raw = input.trim();
  if (/^[A-Za-z0-9_-]{11}$/.test(raw)) return { videoId: raw };
  let u: URL;
  try { u = new URL(/^https?:\/\//i.test(raw) ? raw : `https://${raw}`); } catch { return null; }
  if (!/(^|\.)(youtube\.com|youtu\.be|youtube-nocookie\.com)$/i.test(u.hostname)) return null;
  const listId = u.searchParams.get('list') || undefined;
  let videoId: string | undefined;
  if (/youtu\.be$/i.test(u.hostname)) videoId = u.pathname.split('/')[1];
  else videoId = u.searchParams.get('v') || (u.pathname.match(/\/(?:embed|shorts|live)\/([A-Za-z0-9_-]{11})/) || [])[1];
  if (videoId && !/^[A-Za-z0-9_-]{11}$/.test(videoId)) videoId = undefined;
  return videoId || listId ? { videoId, listId } : null;
}

/* ---------- açıklama katmanı ---------- */
export type ReviewStatus = '' | 'onayli' | 'inceleme' | 'sorunlu';
export interface Annotation { status: ReviewStatus; tags: string[]; note: string; updatedAt: string; by?: string }

export function registerDataCatalogRoutes(app: express.Express, requireAdmin: express.RequestHandler, deps: CatalogDeps) {
  const SRC = path.join(deps.rootDir, 'src', 'data');
  const BACKUP = path.join(deps.dataDir, 'backups', 'catalog');
  const ANN_FILE = path.join(deps.dataDir, 'catalog_annotations.json');
  const annAll = (): Record<string, Record<string, Annotation>> => readJson(ANN_FILE, {});
  const annOf = (entity: string, id: string): Annotation | undefined => annAll()[entity]?.[id];

  /* --- türetilmiş dizinler (ilişkiler için; kaynak değişince yenilenir) --- */
  let kazCache: { at: number; list: Any[] } | null = null;
  const kazanimlar = (): Any[] => {
    if (kazCache && Date.now() - kazCache.at < 60_000) return kazCache.list;
    const out: Any[] = [];
    for (let k = 1; k <= 6; k++) {
      const d = readJson(path.join(SRC, 'kazanimlar', `k${k}.json`), null);
      for (const ders of d?.dersler || []) {
        for (const konu of ders.konular || []) {
          for (const kz of konu.kazanimlar || []) {
            const deckIds = Array.from(new Set((kz.slaytlar || []).map((s: Any) => s.deckId).filter(Boolean))) as string[];
            out.push({ id: kz.id, metin: kz.metin, kurul: `Kurul ${k}`, ders: ders.ders, konu: konu.konu, deckIds, slaytSayisi: (kz.slaytlar || []).length });
          }
        }
      }
    }
    kazCache = { at: Date.now(), list: out };
    return out;
  };

  let ornekCache: { at: number; list: Any[] } | null = null;
  const ornekSorular = (): Any[] => {
    if (ornekCache && Date.now() - ornekCache.at < 60_000) return ornekCache.list;
    const out: Any[] = [];
    const dir = path.join(SRC, 'ornek_sorular');
    for (const kurul of fs.existsSync(dir) ? fs.readdirSync(dir) : []) {
      const kd = path.join(dir, kurul);
      if (!fs.statSync(kd).isDirectory()) continue;
      for (const f of fs.readdirSync(kd)) {
        if (!f.endsWith('.json') || f === 'index.json') continue;
        const lesson = readJson(path.join(kd, f), null);
        if (!lesson) continue;
        for (const kz of lesson.kazanimlar || []) {
          for (const q of kz.sorular || []) {
            out.push({ ...q, _ders: lesson.ders, _konu: lesson.konu, _lesson: lesson.id, _kurul: `Kurul ${lesson.kurul || kurul.replace(/\D/g, '')}`, _kazanimMetin: kz.metin, _file: path.join(kd, f) });
          }
        }
      }
    }
    ornekCache = { at: Date.now(), list: out };
    return out;
  };

  let termIdx: { at: number; map: Map<string, Set<string>> } | null = null;
  /** sözlük terimi (katlanmış) → onu kullanan desteler */
  const termDecks = () => {
    if (termIdx && Date.now() - termIdx.at < 120_000) return termIdx.map;
    const map = new Map<string, Set<string>>();
    for (const d of deps.getDecks()) {
      for (const s of d.slides || []) {
        for (const t of s.medicalTerms || []) {
          const k = fold(t?.term);
          if (!k) continue;
          if (!map.has(k)) map.set(k, new Set());
          map.get(k)!.add(d.id);
        }
      }
    }
    termIdx = { at: Date.now(), map };
    return map;
  };

  const linksFile = path.join(process.env.MEDS_DATABASE_DIR || path.resolve(deps.rootDir, '..', 'meds_database'), 'derived', 'learn_links.json');
  const learnLinks = (): Record<string, Any> => readJson(linksFile, {}).baglantilar || {};
  const deckById = (id: string) => deps.getDecks().find((d) => d.id === id);
  const deckRef = (id: string, why: string): RelationRef | null => {
    const d = deckById(id) || deckById(`k1p-${id}`);
    return d ? { entity: 'decks', id: d.id, title: d.shortTitle || d.title, why } : null;
  };
  const committeeNo = (s: unknown) => (String(s ?? '').match(/kurul\s*-?\s*(\d)/i) || [])[1] || '';
  const discKey = (s: unknown) => fold(String(s ?? '').split(/[\/,]/)[0]).trim();

  /* ---------- bağdaştırıcılar ---------- */
  const glossaryFile = path.join(SRC, 'medical_glossary.json');
  const cardsFile = path.join(SRC, 'question_cards.json');
  const musicFile = deps.musicFile ? deps.musicFile() : path.join(SRC, 'musicTracks.json');
  const decksFile = path.join(SRC, 'interactive_learning_decks.json');

  /** Dizi tutan JSON dosyası için ortak silme/geri yükleme */
  const listFileOps = (file: string, keyOf: (x: Any) => string) => ({
    remove: (ids: string[]) => {
      const set = new Set(ids);
      const list: Any[] = readJson(file, []);
      const removed = list.filter((x) => set.has(keyOf(x)));
      if (removed.length) writeJsonAtomic(file, list.filter((x) => !set.has(keyOf(x))), BACKUP);
      return removed;
    },
    restore: (records: Any[]) => {
      const list: Any[] = [...readJson(file, [])];
      const have = new Set(list.map(keyOf));
      for (const r of records) if (!have.has(keyOf(r))) list.push(r);
      writeJsonAtomic(file, list, BACKUP);
    },
  });
  const ornekFeedbackFile = path.join(deps.dataDir, 'ornek_soru_bildirimleri.jsonl');
  const ornekFeedbackId = (r: Any, i: number) => `ornek:${r.soru_id}:${r.timestamp || i}`;

  const ENTITIES: EntityDef[] = [
    {
      id: 'past', label: 'Çıkmış sorular', group: 'Sorular', source: 'data/pastQuestions.json',
      editable: ['stem', 'correctAnswer', 'explanation', 'topic', 'discipline', 'committeeId', 'examYear', 'tags'], arrays: ['tags'],
      facets: [{ key: 'committeeId', label: 'Kurul' }, { key: 'discipline', label: 'Ders' }, { key: 'examYear', label: 'Yıl' }, { key: 'answerStatus', label: 'Cevap durumu' }, { key: 'qualityTier', label: 'Kalite' }],
      load: () => deps.getPastQuestions(),
      key: (x) => String(x.id), title: (x) => clip(x.stem), subtitle: (x) => [x.discipline, x.committeeId, x.examYear].filter(Boolean).join(' · '),
      facet: (x, k) => (x[k] == null ? undefined : String(x[k])),
      text: (x) => `${x.id} ${x.stem} ${x.topic || ''} ${x.discipline || ''} ${(x.options || []).map((o: Any) => (typeof o === 'string' ? o : o?.text)).join(' ')}`,
      save: (id, patch) => {
        const list = deps.getPastQuestions();
        const q = list.find((x) => String(x.id) === id);
        if (!q) throw new Error('Soru bulunamadı');
        applyPatch(q, patch, ENTITIES[0].editable, ENTITIES[0].arrays);
        syncPastReconstruction(q, patch);
        // Birleştirilmiş kopyalar aynı sorudur, sitede yalnız biri görünür: içerik düzeltmesi hepsine yazılır
        // (sınav yılı ve etiketler kopyaya özgüdür, onlar aktarılmaz).
        const content = Object.fromEntries(Object.entries(patch || {}).filter(([k]) => PAST_SHARED_FIELDS.includes(k)));
        if (Object.keys(content).length) {
          for (const sid of mergeSiblings(id)) {
            const sq = list.find((x) => String(x.id) === sid);
            if (!sq) continue;
            applyPatch(sq, content, PAST_SHARED_FIELDS);
            syncPastReconstruction(sq, content);
          }
        }
        deps.savePastQuestions(list);
        return q;
      },
      relations: (x) => {
        const out: RelationRef[] = [];
        // 1) Doğrulanmış bağlantı (learn_links.py: BM25 + e5 + çapraz kodlayıcı, eşikli) — en güvenilir
        const link = learnLinks()[x.id];
        if (link?.deckId) out.push({ entity: 'decks', id: link.deckId, title: `${link.deckTitle} · adım ${link.slideNumber}`, why: `Doğrulanmış slayt bağlantısı (${link.guven || 'orta'} güven, skor ${link.skor})` });
        const no = committeeNo(x.committeeId) || committeeNo(x.kurul);
        const dk = discKey(x.discipline);
        const topic = fold(x.topic || '');
        for (const d of deps.getDecks()) {
          if (no && committeeNo(d.committee) && committeeNo(d.committee) !== no) continue;
          if (dk && !fold(d.discipline).includes(dk)) continue;
          const t = fold(`${d.title} ${d.shortTitle || ''}`);
          const hit = topic && topic.split(/\s+/).filter((w) => w.length > 4 && t.includes(w.slice(0, 5))).length;
          if (Number(hit) >= 2 && d.id !== link?.deckId) out.push({ entity: 'decks', id: d.id, title: d.shortTitle || d.title, why: `Aynı ders + konu kelimesi (${hit}) — öneri` });
        }
        for (const o of ornekSorular()) if ((o.benzer_cikmis || []).includes(x.id)) out.push({ entity: 'ornek', id: o.id, title: clip(o.soru, 90), why: 'Örnek soru bu çıkmışa benziyor' });
        return out.slice(0, 20);
      },
      remove: deps.removePast,
      restore: deps.restorePast,
    },
    {
      id: 'pool', label: 'Soru havuzu', group: 'Sorular', source: 'data/questions.json',
      editable: [],
      facets: [{ key: 'committeeId', label: 'Kurul' }, { key: 'status', label: 'Durum' }],
      load: () => (readJson(path.join(deps.dataDir, 'questions.json'), {}).questions || []),
      key: (x) => String(x.id), title: (x) => clip(x.stem || x.text || x.title || (x.fragments || [])[0]?.text), subtitle: (x) => [x.committeeId, x.status].filter(Boolean).join(' · '),
      facet: (x, k) => (x[k] == null ? undefined : String(x[k])),
      text: (x) => `${x.id} ${x.stem || ''} ${x.text || ''} ${(x.fragments || []).map((f: Any) => f?.text).join(' ')}`,
      remove: deps.removePool,
      restore: deps.restorePool,
    },
    {
      id: 'decks', label: 'Öğren desteleri', group: 'Öğrenme', source: 'src/data/interactive_learning_decks.json',
      editable: ['title', 'shortTitle', 'discipline', 'committee', 'instructor', 'category'],
      facets: [{ key: 'committee', label: 'Kurul' }, { key: 'discipline', label: 'Ders' }, { key: 'category', label: 'Kategori' }],
      load: () => deps.getDecks(),
      key: (x) => String(x.id), title: (x) => x.shortTitle || x.title, subtitle: (x) => `${(x.slides || []).length} adım · ${x.discipline || ''}`,
      facet: (x, k) => (x[k] == null ? undefined : String(x[k])),
      text: (x) => `${x.id} ${x.title} ${x.shortTitle || ''} ${x.discipline || ''} ${x.instructor || ''}`,
      save: (id, patch) => {
        const list = readJson(decksFile, []);
        const d = list.find((x: Any) => x.id === id);
        if (!d) throw new Error('Deste bulunamadı');
        applyPatch(d, patch, ['title', 'shortTitle', 'discipline', 'committee', 'instructor', 'category']);
        writeJsonAtomic(decksFile, list, BACKUP);
        return d;
      },
      relations: (x) => {
        const out: RelationRef[] = [];
        for (const k of kazanimlar()) if (k.deckIds.includes(x.id) || k.deckIds.includes(String(x.id).replace(/^k1p-/, ''))) out.push({ entity: 'kazanim', id: k.id, title: clip(k.metin, 90), why: 'Kazanım bu destenin slaytlarına bağlı' });
        const lesson = String(x.id).replace(/^k1p-/, '');
        const ornekN = ornekSorular().filter((o) => o._lesson === lesson).length;
        if (ornekN) out.push({ entity: 'ornek', id: `ders:${lesson}`, title: `${ornekN} örnek soru`, why: 'Aynı dersin örnek soruları' });
        const terms = new Set<string>();
        for (const s of x.slides || []) for (const t of s.medicalTerms || []) if (t?.term) terms.add(t.term);
        for (const t of Array.from(terms).slice(0, 12)) out.push({ entity: 'glossary', id: fold(t), title: t, why: 'Destede geçen terim' });
        return out;
      },
      ...listFileOps(decksFile, (x) => String(x.id)),
    },
    {
      id: 'kazanim', label: 'Kazanımlar', group: 'Öğrenme', source: 'src/data/kazanimlar/k*.json',
      editable: [],
      facets: [{ key: 'kurul', label: 'Kurul' }, { key: 'ders', label: 'Ders' }],
      load: kazanimlar,
      key: (x) => x.id, title: (x) => clip(x.metin, 160), subtitle: (x) => `${x.ders} · ${x.konu} · ${x.slaytSayisi} slayt`,
      facet: (x, k) => x[k], text: (x) => `${x.id} ${x.metin} ${x.ders} ${x.konu}`,
      relations: (x) => (x.deckIds as string[]).map((id) => deckRef(id, 'Kazanımın kaynak slaytları')).filter(Boolean) as RelationRef[],
    },
    {
      id: 'ornek', label: 'Örnek sorular', group: 'Sorular', source: 'src/data/ornek_sorular/k*/',
      editable: [],
      facets: [{ key: '_kurul', label: 'Kurul' }, { key: '_ders', label: 'Ders' }, { key: 'zorluk', label: 'Zorluk' }],
      load: ornekSorular,
      key: (x) => x.id, title: (x) => clip(x.soru), subtitle: (x) => `${x._ders} · ${x._konu} · ${x.zorluk}`,
      facet: (x, k) => x[k], text: (x) => `${x.id} ${x.soru} ${x._konu} ${x._kazanimMetin}`,
      relations: (x) => {
        const out: RelationRef[] = [];
        const r = deckRef(x._lesson, 'Aynı dersin Öğren destesi');
        if (r) out.push(r);
        const k = kazanimlar().find((kz) => kz.metin === x._kazanimMetin);
        if (k) out.push({ entity: 'kazanim', id: k.id, title: clip(k.metin, 90), why: 'Sorunun ölçtüğü kazanım' });
        const past = deps.getPastQuestions();
        for (const pid of x.benzer_cikmis || []) {
          const p = past.find((q) => q.id === pid);
          if (p) out.push({ entity: 'past', id: p.id, title: clip(p.stem, 90), why: 'Editör onaylı benzer çıkmış' });
        }
        return out;
      },
      remove: (ids) => {
        const set = new Set(ids);
        const hits = ornekSorular().filter((o) => set.has(o.id));
        for (const file of new Set(hits.map((o) => o._file as string))) {
          const lesson = readJson(file, null);
          if (!lesson) continue;
          for (const kz of lesson.kazanimlar || []) kz.sorular = (kz.sorular || []).filter((q: Any) => !set.has(q.id));
          writeJsonAtomic(file, lesson, BACKUP);
        }
        ornekCache = null;
        return hits;
      },
      restore: (records) => {
        const byFile = new Map<string, Any[]>();
        for (const r of records) byFile.set(r._file, [...(byFile.get(r._file) || []), r]);
        for (const [file, rs] of byFile) {
          const lesson = readJson(file, null);
          if (!lesson) throw new Error(`Ders dosyası bulunamadı: ${path.basename(file)}`);
          for (const r of rs) {
            const { _ders, _konu, _lesson, _kurul, _kazanimMetin, _file, ...q } = r;
            const kz = (lesson.kazanimlar || []).find((k: Any) => k.metin === _kazanimMetin) || lesson.kazanimlar?.[0];
            if (!kz) continue;
            kz.sorular = kz.sorular || [];
            if (!kz.sorular.some((x: Any) => x.id === q.id)) kz.sorular.push(q);
          }
          writeJsonAtomic(file, lesson, BACKUP);
        }
        ornekCache = null;
      },
    },
    {
      id: 'glossary', label: 'Sözlük', group: 'Kaynaklar', source: 'src/data/medical_glossary.json',
      editable: ['term', 'category', 'definition', 'description', 'clinicalPearl', 'discipline', 'aliases'], arrays: ['aliases'],
      facets: [{ key: 'category', label: 'Tür' }, { key: 'discipline', label: 'Ders' }, { key: 'committee', label: 'Kurul' }],
      load: () => Object.entries(readJson(glossaryFile, {})).map(([k, v]) => ({ ...(typeof v === 'string' ? { term: k, definition: v } : (v as Any)), _key: k })),
      key: (x) => x._key, title: (x) => x.term || x._key, subtitle: (x) => clip(x.definition, 110),
      facet: (x, k) => (x[k] == null ? undefined : String(x[k])), text: (x) => `${x.term} ${(x.aliases || []).join(' ')} ${x.definition || ''}`,
      save: (id, patch) => {
        const all = readJson(glossaryFile, {});
        if (!(id in all)) throw new Error('Terim bulunamadı');
        const cur = typeof all[id] === 'string' ? { term: id, definition: all[id] } : all[id];
        all[id] = applyPatch({ ...cur }, patch, ['term', 'category', 'definition', 'description', 'clinicalPearl', 'discipline', 'aliases'], ['aliases']);
        writeJsonAtomic(glossaryFile, all, BACKUP);
        return { ...all[id], _key: id };
      },
      relations: (x) => {
        const ids = termDecks().get(fold(x.term || x._key)) || new Set<string>();
        const out = Array.from(ids).map((id) => deckRef(id, 'Terim bu destede geçiyor')).filter(Boolean) as RelationRef[];
        const dz = readJson(path.join(SRC, 'diseases.json'), []).find((d: Any) => fold(d.name) === fold(x.term));
        if (dz) out.push({ entity: 'diseases', id: dz.id, title: dz.name, why: 'Aynı adlı hastalık kaydı' });
        return out;
      },
      remove: (ids) => {
        const all = { ...readJson(glossaryFile, {}) };
        const removed = ids.filter((id) => id in all).map((id) => ({ _key: id, _value: all[id] }));
        for (const r of removed) delete all[r._key];
        if (removed.length) writeJsonAtomic(glossaryFile, all, BACKUP);
        termIdx = null;
        return removed;
      },
      restore: (records) => {
        const all = { ...readJson(glossaryFile, {}) };
        for (const r of records) if (!(r._key in all)) all[r._key] = r._value;
        writeJsonAtomic(glossaryFile, all, BACKUP);
      },
    },
    {
      id: 'cards', label: 'Ezber kartları', group: 'Öğrenme', source: 'src/data/question_cards.json',
      editable: ['front', 'back', 'note', 'answer', 'konu', 'group'],
      facets: [{ key: 'kurul', label: 'Kurul' }, { key: 'group', label: 'Grup' }, { key: 'konu', label: 'Konu' }],
      load: () => readJson(cardsFile, []),
      key: (x) => x.id, title: (x) => clip(x.front), subtitle: (x) => [x.kurul, x.konu].filter(Boolean).join(' · '),
      facet: (x, k) => (x[k] == null ? undefined : String(x[k])), text: (x) => `${x.id} ${x.front} ${x.back || ''} ${x.konu || ''}`,
      save: (id, patch) => {
        const list = readJson(cardsFile, []);
        const c = list.find((x: Any) => x.id === id);
        if (!c) throw new Error('Kart bulunamadı');
        applyPatch(c, patch, ['front', 'back', 'note', 'answer', 'konu', 'group']);
        writeJsonAtomic(cardsFile, list, BACKUP);
        return c;
      },
      ...listFileOps(cardsFile, (x) => String(x.id)),
    },
    {
      id: 'diseases', label: 'Hastalıklar', group: 'Kaynaklar', source: 'src/data/diseases.json',
      editable: [],
      facets: [{ key: 'category', label: 'Kategori' }, { key: 'kind', label: 'Tür' }],
      load: () => readJson(path.join(SRC, 'diseases.json'), []),
      key: (x) => String(x.id), title: (x) => x.name, subtitle: (x) => [x.latinName, x.icd_code].filter(Boolean).join(' · '),
      facet: (x, k) => (x[k] == null ? undefined : String(x[k])),
      text: (x) => `${x.name} ${x.latinName || ''} ${x.icd_code || ''} ${(x.altNames || []).join(' ')} ${(x.hallmarks || []).map((h: Any) => h?.text || '').join(' ')}`,
      relations: (x) => {
        const ids = termDecks().get(fold(x.name)) || new Set<string>();
        return Array.from(ids).map((id) => deckRef(id, 'Hastalık bu destede terim olarak geçiyor')).filter(Boolean) as RelationRef[];
      },
      ...listFileOps(path.join(SRC, 'diseases.json'), (x) => String(x.id)),
    },
    {
      id: 'summaries', label: 'Ders özetleri', group: 'Kaynaklar', source: 'src/data/summaries_meta.json',
      editable: [],
      facets: [{ key: 'kurul', label: 'Kurul' }, { key: 'discipline', label: 'Ders' }],
      load: () => readJson(path.join(SRC, 'summaries_meta.json'), []),
      key: (x) => String(x.id), title: (x) => x.title, subtitle: (x) => [x.discipline, x.instructor, x.readingTimeMinutes ? `${x.readingTimeMinutes} dk` : ''].filter(Boolean).join(' · '),
      facet: (x, k) => (x[k] == null ? undefined : String(x[k])), text: (x) => `${x.title} ${x.discipline || ''} ${x.instructor || ''} ${(x.keyPoints || []).join(' ')}`,
    },
    {
      id: 'feedback', label: 'Geri bildirimler', group: 'Topluluk', source: 'data/learn_feedback.json + ornek_soru_bildirimleri.jsonl',
      editable: [],
      facets: [{ key: 'kind', label: 'Kaynak' }, { key: 'field', label: 'Konu' }],
      load: () => {
        const learn: Any[] = (readJson(path.join(deps.dataDir, "learn_feedback.json"), []) as Any[]).map((f) => ({ ...f, kind: "Öğren", _id: `learn:${f.id}` }));
        let ornek: Any[] = [];
        try {
          ornek = fs.readFileSync(path.join(deps.dataDir, 'ornek_soru_bildirimleri.jsonl'), 'utf8').split('\n').filter((l) => l.trim()).map((l, i) => {
            const r = JSON.parse(l);
            return { ...r, kind: 'Örnek soru', field: r.reason, _id: ornekFeedbackId(r, i) };
          });
        } catch { /* dosya yok */ }
        return ([...learn, ...ornek] as Any[]).sort((a, b) => String(b.createdAt || b.timestamp || '').localeCompare(String(a.createdAt || a.timestamp || '')));
      },
      key: (x) => x._id, title: (x) => clip(x.reason || x.details || x.field, 140), subtitle: (x) => [x.kind, x.deckTitle || x.soru_id, x.createdAt || x.timestamp].filter(Boolean).join(' · '),
      facet: (x, k) => (x[k] == null ? undefined : String(x[k])), text: (x) => `${x.reason || ''} ${x.details || ''} ${x.deckTitle || ''} ${x.soru_id || ''}`,
      relations: (x) => {
        if (x.kind === 'Öğren') { const r = deckRef(x.deckId, `Bildirilen deste (adım ${x.slideNumber ?? '?'})`); return r ? [r] : []; }
        const o = ornekSorular().find((q) => q.id === x.soru_id);
        return o ? [{ entity: 'ornek', id: o.id, title: clip(o.soru, 90), why: 'Bildirilen örnek soru' }] : [];
      },
      remove: (ids) => {
        const set = new Set(ids);
        const out: Any[] = [];
        const learnIds = ids.filter((id) => id.startsWith('learn:')).map((id) => id.slice(6));
        if (learnIds.length && deps.removeLearnFeedback) out.push(...deps.removeLearnFeedback(learnIds).map((f) => ({ ...f, kind: 'Öğren', _id: `learn:${f.id}` })));
        if (ids.some((id) => id.startsWith('ornek:')) && fs.existsSync(ornekFeedbackFile)) {
          const keep: string[] = [];
          fs.readFileSync(ornekFeedbackFile, 'utf8').split('\n').filter((l) => l.trim()).forEach((l, i) => {
            const r = JSON.parse(l);
            const id = ornekFeedbackId(r, i);
            if (set.has(id)) out.push({ ...r, kind: 'Örnek soru', _id: id, _line: l });
            else keep.push(l);
          });
          fs.writeFileSync(ornekFeedbackFile, keep.map((l) => l + '\n').join(''), 'utf8');
        }
        return out;
      },
      restore: (records) => {
        const learn = records.filter((r) => r.kind === 'Öğren').map(({ kind, _id, ...f }) => f);
        if (learn.length) deps.restoreLearnFeedback?.(learn);
        const lines = records.filter((r) => r.kind === 'Örnek soru' && r._line).map((r) => r._line + '\n');
        if (lines.length) fs.appendFileSync(ornekFeedbackFile, lines.join(''), 'utf8');
      },
    },
    {
      id: 'music', label: 'Müzik listesi', group: 'Topluluk', source: deps.musicFile ? 'data/music_shared.json' : 'src/data/musicTracks.json',
      editable: ['title', 'artist', 'url'],
      facets: [{ key: 'artist', label: 'Sanatçı' }],
      load: () => readJson(musicFile, []),
      key: (x) => x.id, title: (x) => x.title, subtitle: (x) => x.artist,
      facet: (x, k) => (x[k] == null ? undefined : String(x[k])), text: (x) => `${x.title} ${x.artist}`,
      save: (id, patch) => {
        const list = readJson(musicFile, []);
        const t = list.find((x: Any) => x.id === id);
        if (!t) throw new Error('Parça bulunamadı');
        applyPatch(t, patch, ['title', 'artist', 'url']);
        if ('url' in (patch || {})) {
          const yt = parseYouTubeUrl(String(t.url || ''));
          if (!yt) throw new Error('Geçerli bir YouTube bağlantısı girin.');
          if (yt.videoId) t.videoId = yt.videoId; else delete t.videoId;
          if (yt.listId) t.listId = yt.listId; else delete t.listId;
        }
        writeJsonAtomic(musicFile, list, BACKUP);
        return t;
      },
      ...listFileOps(musicFile, (x) => String(x.id)),
    },
  ];

  /* ---------- çöp kutusu (silinenler; geri yüklenebilir) ---------- */
  const TRASH_FILE = path.join(deps.dataDir, 'catalog_trash.json');
  const TRASH_MAX = 20_000;
  const trashAll = (): TrashEntry[] => readJson(TRASH_FILE, []);
  const writeTrash = (list: TrashEntry[]) => {
    fs.mkdirSync(path.dirname(TRASH_FILE), { recursive: true });
    const tmp = `${TRASH_FILE}.${process.pid}.tmp`;
    fs.writeFileSync(tmp, JSON.stringify(list.slice(-TRASH_MAX)), 'utf8');
    fs.renameSync(tmp, TRASH_FILE);
    fileCache.delete(TRASH_FILE);
  };
  const labelOf = (id: string) => ENTITIES.find((e) => e.id === id)?.label || id;
  ENTITIES.push({
    id: 'trash', label: 'Çöp kutusu', group: 'Topluluk', source: 'data/catalog_trash.json',
    editable: [],
    facets: [{ key: 'entity', label: 'Tür' }],
    load: () => [...trashAll()].reverse(),
    key: (x) => x.key, title: (x) => x.title || x.id,
    subtitle: (x) => `${labelOf(x.entity)} · ${new Date(x.deletedAt).toLocaleString('tr-TR')}${x.by ? ` · ${x.by}` : ''}`,
    facet: (x, k) => (k === 'entity' ? labelOf(x.entity) : undefined),
    text: (x) => `${x.id} ${x.title} ${labelOf(x.entity)}`,
    remove: (ids) => {
      const set = new Set(ids);
      const list = trashAll();
      const removed = list.filter((t) => set.has(t.key));
      writeTrash(list.filter((t) => !set.has(t.key)));
      return removed;
    },
  });
  const byId = (id: string) => ENTITIES.find((e) => e.id === id);

  /* ---------- şablonlar: yeni kayıt + çoğaltma (yalnız düzenlenebilir kaynaklar) ---------- */
  const facetValues = (entity: string, k: string) => () => {
    const e = ENTITIES.find((x) => x.id === entity)!;
    const m = new Map<string, number>();
    for (const x of e.load()) { const v = e.facet(x, k); for (const one of Array.isArray(v) ? v : [v]) if (one) m.set(one, (m.get(one) || 0) + 1); }
    return Array.from(m).sort((a, b) => b[1] - a[1]).map(([v]) => v);
  };
  const optionsToForm = (o: unknown) => {
    const out: Any = {};
    if (Array.isArray(o)) for (const x of o) { const k = str(x?.key || x?.label).toUpperCase(); if (k) out[k] = typeof x === 'string' ? x : x?.text ?? ''; }
    else if (o && typeof o === 'object') Object.assign(out, o);
    return out;
  };
  const insertInto = (list: Any[], rec: Any, afterIdx: number) => {
    if (afterIdx >= 0) list.splice(afterIdx + 1, 0, rec);
    else list.push(rec);
  };

  const CREATE: Record<string, CreateDef> = {
    past: {
      fields: [
        { key: 'committeeId', label: 'Kurul', kind: 'choice', required: true, choices: facetValues('past', 'committeeId'), free: true, hint: 'ör. donem3-kurul1' },
        { key: 'examYear', label: 'Sınav yılı', kind: 'choice', choices: facetValues('past', 'examYear'), free: true },
        { key: 'discipline', label: 'Ders', kind: 'choice', required: true, choices: facetValues('past', 'discipline'), free: true },
        { key: 'topic', label: 'Konu' },
        { key: 'stem', label: 'Soru kökü', kind: 'long', required: true },
        { key: 'options', label: 'Şıklar', kind: 'options', required: true },
        { key: 'correctAnswer', label: 'Doğru cevap', kind: 'choice', required: true, choices: OPTION_KEYS },
        { key: 'explanation', label: 'Açıklama', kind: 'long' },
        { key: 'tags', label: 'Etiketler', kind: 'list' },
      ],
      toForm: (x) => ({ committeeId: x.committeeId, examYear: x.examYear, discipline: x.discipline, topic: x.topic, stem: x.stem, options: optionsToForm(x.options), correctAnswer: x.correctAnswer, explanation: x.explanation, tags: (x.tags || []).join(', ') }),
      build: (v, base) => {
        checkRequired(CREATE.past.fields, v);
        const { opts, ans } = readOptions(v, 'correctAnswer');
        const now = new Date().toISOString();
        const taken = new Set(deps.getPastQuestions().map((q) => String(q.id)));
        const committeeId = str(v.committeeId);
        const rec: Any = base
          ? clone(base)
          : { status: 'verified', isSuspect: false, isAmbiguous: false, isPastExam: true, sourceNote: 'Veri kataloğundan elle eklendi', qualityIssues: [] };
        // Kişisel/oy alanları kopyalanmaz
        for (const k of ['reports', 'comments', 'notes', 'checkSolve', 'checkSolveOriginal', 'phase14', 'phase14Original', 'eskiSurum', 'denetleyiciSurumu']) if (base) delete rec[k];
        Object.assign(rec, {
          id: uniqueKey(hexId(), (k) => taken.has(k)),
          committeeId,
          kurul: Number((committeeId.match(/kurul\s*-?\s*(\d)/i) || [])[1]) || rec.kurul,
          donem: (committeeId.match(/donem\s*(\d)/i) || [])[1] ? `Dönem ${(committeeId.match(/donem\s*(\d)/i) || [])[1]}` : rec.donem,
          discipline: str(v.discipline), topic: str(v.topic), examYear: str(v.examYear),
          stem: str(v.stem), explanation: str(v.explanation),
          options: opts.map((o) => ({ key: o.key, label: o.key, text: o.text, isCorrect: o.key === ans, upvotes: 0, likedBy: [] })),
          correctAnswer: ans, claimedAnswer: ans,
          tags: listOf(v.tags), upvotes: 0, likedBy: [], createdAt: now, updatedAt: now,
        });
        if (base) rec.copiedFrom = String(base.id);
        return { id: rec.id, ...rec };
      },
      insert: (rec, afterId) => {
        const list = deps.getPastQuestions();
        insertInto(list, rec, afterId ? list.findIndex((q) => String(q.id) === afterId) : -1);
        deps.savePastQuestions(list);
      },
    },
    glossary: {
      fields: [
        { key: 'term', label: 'Terim', required: true },
        { key: 'category', label: 'Tür', kind: 'choice', required: true, choices: facetValues('glossary', 'category'), free: true },
        { key: 'discipline', label: 'Ders', kind: 'choice', choices: facetValues('glossary', 'discipline'), free: true },
        { key: 'definition', label: 'Tanım', kind: 'long', required: true },
        { key: 'description', label: 'Açıklama', kind: 'long', hint: 'Boşsa tanım kullanılır' },
        { key: 'clinicalPearl', label: 'Klinik inci', kind: 'long' },
        { key: 'aliases', label: 'Eş anlamlılar', kind: 'list' },
      ],
      toForm: (x) => ({ term: x.term, category: x.category, discipline: x.discipline, definition: x.definition, description: x.description, clinicalPearl: x.clinicalPearl, aliases: (x.aliases || []).join(', ') }),
      build: (v, base) => {
        checkRequired(CREATE.glossary.fields, v);
        const all = readJson(glossaryFile, {});
        const term = str(v.term);
        const key = term.toLocaleLowerCase('tr');
        if (key in all || Object.values(all).some((g: any) => fold(g?.term) === fold(term))) throw new Error(`"${term}" sözlükte zaten var; terim adını değiştirin.`);
        const rec: Any = base ? clone(base) : { committee: '', kaynaklar: [] };
        delete rec._key;
        Object.assign(rec, {
          term, category: str(v.category), discipline: str(v.discipline), definition: str(v.definition),
          description: str(v.description) || str(v.definition), dogrulama: { durum: 'elle_eklendi', uretici: 'veri_katalogu' },
        });
        if (str(v.clinicalPearl)) rec.clinicalPearl = str(v.clinicalPearl); else delete rec.clinicalPearl;
        if (listOf(v.aliases).length) rec.aliases = listOf(v.aliases); else delete rec.aliases;
        return { ...rec, _key: key };
      },
      insert: (rec, afterId) => {
        const all = readJson(glossaryFile, {});
        const { _key, ...val } = rec;
        // Sözlük nesnedir: asıl terimin hemen arkasına yerleştir (sıra korunur)
        const next: Any = {};
        let placed = false;
        for (const [k, x] of Object.entries(all)) { next[k] = x; if (k === afterId) { next[_key] = val; placed = true; } }
        if (!placed) next[_key] = val;
        writeJsonAtomic(glossaryFile, next, BACKUP);
      },
    },
    cards: {
      fields: [
        { key: 'kurul', label: 'Kurul', kind: 'choice', required: true, choices: ['1', '2', '3', '4', '5', '6'] },
        { key: 'group', label: 'Ders (grup)', kind: 'choice', required: true, choices: facetValues('cards', 'group'), free: true },
        { key: 'konu', label: 'Konu', kind: 'choice', choices: facetValues('cards', 'konu'), free: true },
        { key: 'front', label: 'Ön yüz (soru)', kind: 'long', required: true },
        { key: 'options', label: 'Şıklar', kind: 'options', hint: 'Klasik kartta boş bırakılabilir' },
        { key: 'answer', label: 'Doğru şık', kind: 'choice', choices: OPTION_KEYS },
        { key: 'back', label: 'Arka yüz (cevap)', kind: 'long', hint: 'Boşsa doğru şıktan üretilir' },
        { key: 'note', label: 'Not', kind: 'long' },
      ],
      toForm: (x) => ({ kurul: x.kurul == null ? '' : String(x.kurul), group: x.group, konu: x.konu, front: x.front, options: optionsToForm(x.options), answer: x.answer, back: x.back, note: x.note }),
      build: (v, base) => {
        checkRequired(CREATE.cards.fields, v);
        const hasOpts = OPTION_KEYS.some((k) => str(v.options?.[k]));
        const { opts, ans } = hasOpts ? readOptions(v, 'answer') : { opts: [], ans: '' };
        if (hasOpts && !ans) throw new Error('Şıklı kartta doğru şık seçilmeli.');
        const back = str(v.back) || (ans ? `${ans}) ${opts.find((o) => o.key === ans)?.text}` : '');
        if (!back) throw new Error('Arka yüz boş bırakılamaz (ya da şık + doğru şık girin).');
        const taken = new Set(readJson(cardsFile, []).map((c: Any) => c.id));
        const rec: Any = base ? clone(base) : { tekrar: 0, cikis: [], kaynak: null };
        Object.assign(rec, {
          id: uniqueKey(`q:${hexId()}`, (k) => taken.has(k)),
          front: str(v.front), answer: ans, back, note: str(v.note), group: str(v.group),
          kurul: Number(v.kurul) || null, konu: str(v.konu) || null,
          dogrulama: { durum: 'elle_eklendi', editor: true },
        });
        if (hasOpts) rec.options = Object.fromEntries(opts.map((o) => [o.key, o.text])); else delete rec.options;
        return { id: rec.id, ...rec };
      },
      insert: (rec, afterId) => {
        const list = readJson(cardsFile, []).slice();
        insertInto(list, rec, afterId ? list.findIndex((c: Any) => c.id === afterId) : -1);
        writeJsonAtomic(cardsFile, list, BACKUP);
      },
    },
    music: {
      fields: [
        { key: 'title', label: 'Başlık', required: true },
        { key: 'artist', label: 'Sanatçı', kind: 'choice', choices: facetValues('music', 'artist'), free: true, hint: 'Boşsa "Admin seçkisi"' },
        { key: 'url', label: 'YouTube bağlantısı', required: true, hint: 'Video ya da oynatma listesi bağlantısı' },
      ],
      toForm: (x) => ({ title: x.title, artist: x.artist, url: x.url }),
      build: (v, base) => {
        checkRequired(CREATE.music.fields, v);
        const yt = parseYouTubeUrl(str(v.url));
        if (!yt) throw new Error('Geçerli bir YouTube bağlantısı girin.');
        const list = readJson(musicFile, []);
        const rec: Any = base ? clone(base) : {};
        delete rec.videoId; delete rec.listId;
        Object.assign(rec, {
          id: uniqueKey(slug(str(v.title)), (k) => list.some((t: Any) => t.id === k)),
          title: str(v.title), artist: str(v.artist) || 'Admin seçkisi', url: str(v.url),
          ...(yt.videoId ? { videoId: yt.videoId } : {}), ...(yt.listId ? { listId: yt.listId } : {}),
        });
        return rec;
      },
      insert: (rec, afterId) => {
        const list = readJson(musicFile, []).slice();
        insertInto(list, rec, afterId ? list.findIndex((t: Any) => t.id === afterId) : -1);
        writeJsonAtomic(musicFile, list, BACKUP);
      },
    },
  };
  /** Çoğaltma formu: ayırt edici alan benzersiz olmalı (sözlükte terim, müzikte başlık) → "(kopya)" eki */
  const dupForm = (entity: string, x: Any) => {
    const v = CREATE[entity].toForm(x);
    if (entity === 'glossary') v.term = `${v.term} (kopya)`;
    if (entity === 'music') v.title = `${v.title} (kopya)`;
    return v;
  };
  const serializeFields = (fields: FormField[]) => fields.map((f) => ({ ...f, choices: typeof f.choices === 'function' ? f.choices().slice(0, 200) : f.choices }));
  const forget = (entity: string, ids: string[]) => {
    const all = { ...annAll() };
    if (!all[entity]) return;
    const bucket = { ...all[entity] };
    for (const id of ids) delete bucket[id];
    all[entity] = bucket;
    writeAnn(all);
  };
  const writeAnn = (all: Record<string, Record<string, Annotation>>) => {
    fs.mkdirSync(path.dirname(ANN_FILE), { recursive: true });
    const tmp = `${ANN_FILE}.${process.pid}.tmp`;
    fs.writeFileSync(tmp, JSON.stringify(all, null, 1), 'utf8');
    fs.renameSync(tmp, ANN_FILE);
    fileCache.delete(ANN_FILE);
  };

  /* ---------- uçlar ---------- */
  app.get('/api/admin/catalog', requireAdmin, (_req, res) => {
    const ann = annAll();
    res.json({
      entities: ENTITIES.map((e) => {
        let count = 0;
        try { count = e.load().length; } catch { /* okunamadı */ }
        const a = Object.values(ann[e.id] || {});
        return {
          id: e.id, label: e.label, group: e.group, source: e.source, editable: e.editable, creatable: !!CREATE[e.id], deletable: !!e.remove, restorable: !!e.restore, arrays: e.arrays || [], facets: e.facets, count,
          reviewed: { onayli: a.filter((x) => x.status === 'onayli').length, inceleme: a.filter((x) => x.status === 'inceleme').length, sorunlu: a.filter((x) => x.status === 'sorunlu').length },
        };
      }),
    });
  });

  app.get('/api/admin/catalog/:entity', requireAdmin, (req, res) => {
    const e = byId(req.params.entity);
    if (!e) return res.status(404).json({ error: 'Bilinmeyen veri türü' });
    const q = fold(req.query.q || '');
    const page = Math.max(0, Number(req.query.page) || 0);
    const size = Math.min(200, Math.max(10, Number(req.query.size) || 50));
    const filters: Record<string, string> = {};
    for (const [k, v] of Object.entries(req.query)) if (k.startsWith('f.') && v) filters[k.slice(2)] = String(v);
    const ann = annAll()[e.id] || {};
    let rows = e.load();
    // "ders:<id>" gibi ilişki kısa yolları (örnek soruların ders bazlı listesi)
    const lessonFilter = String(req.query.lesson || '');
    if (lessonFilter) rows = rows.filter((x) => x._lesson === lessonFilter);
    rows = rows.filter((x) => {
      for (const [k, v] of Object.entries(filters)) {
        if (k === 'status') { if ((ann[e.key(x)]?.status || '') !== (v === 'yok' ? '' : v)) return false; continue; }
        if (k === 'tag') { if (!(ann[e.key(x)]?.tags || []).includes(v)) return false; continue; }
        const fv = e.facet(x, k);
        if (Array.isArray(fv) ? !fv.includes(v) : fv !== v) return false;
      }
      return !q || fold(e.text(x)).includes(q);
    });
    // Sınıflar (süzülmüş küme üzerinde sayılır)
    const facets: Record<string, { value: string; n: number }[]> = {};
    for (const f of e.facets) {
      const m = new Map<string, number>();
      for (const x of rows) {
        const v = e.facet(x, f.key);
        for (const one of Array.isArray(v) ? v : [v]) if (one) m.set(one, (m.get(one) || 0) + 1);
      }
      facets[f.key] = Array.from(m, ([value, n]) => ({ value, n })).sort((a, b) => b.n - a.n).slice(0, 40);
    }
    const st = new Map<string, number>();
    const tags = new Map<string, number>();
    for (const x of rows) {
      const a = ann[e.key(x)];
      st.set(a?.status || 'yok', (st.get(a?.status || 'yok') || 0) + 1);
      for (const t of a?.tags || []) tags.set(t, (tags.get(t) || 0) + 1);
    }
    facets.status = Array.from(st, ([value, n]) => ({ value, n }));
    facets.tag = Array.from(tags, ([value, n]) => ({ value, n })).sort((a, b) => b.n - a.n).slice(0, 40);
    const sort = String(req.query.sort || '');
    if (sort === 'title') rows = [...rows].sort((a, b) => e.title(a).localeCompare(e.title(b), 'tr'));
    if (sort === 'updated') rows = [...rows].sort((a, b) => String(b.updatedAt || ann[e.key(b)]?.updatedAt || '').localeCompare(String(a.updatedAt || ann[e.key(a)]?.updatedAt || '')));
    // Toplu seçim: süzgece uyan TÜM kayıtların kimlikleri (sayfadan bağımsız)
    if (req.query.idsOnly) return res.json({ total: rows.length, ids: rows.map((x) => e.key(x)) });
    const total = rows.length;
    const items = rows.slice(page * size, page * size + size).map((x) => ({ id: e.key(x), title: e.title(x), subtitle: e.subtitle?.(x) || '', ann: ann[e.key(x)] || null }));
    res.json({ total, page, size, items, facets });
  });

  /** Yeni kayıt şablonu: form alanları (seçenekleriyle) */
  app.get('/api/admin/catalog/:entity/template', requireAdmin, (req, res) => {
    const c = CREATE[req.params.entity];
    if (!c) return res.status(400).json({ error: 'Bu veri türüne buradan kayıt eklenemez.' });
    res.json({ fields: serializeFields(c.fields) });
  });

  /** Yeni kayıt (body.values = form değerleri). Kayıt türün şablonuna göre kurulur. */
  app.post('/api/admin/catalog/:entity', requireAdmin, (req, res) => {
    const e = byId(req.params.entity);
    const c = CREATE[req.params.entity];
    if (!e || !c) return res.status(400).json({ error: 'Bu veri türüne buradan kayıt eklenemez.' });
    try {
      const rec = c.build(req.body?.values || {});
      c.insert(rec);
      deps.onChange?.(e.id);
      res.json({ success: true, id: e.key(rec), record: rec, note: e.source.startsWith('src/') ? 'Eklendi. Uygulamadaki paket bir sonraki derlemede güncellenir.' : 'Eklendi.' });
    } catch (err: any) {
      res.status(400).json({ error: err.message });
    }
  });

  /** Çoğalt: asıl kayıt kopyalanır, (varsa) body.values ile değiştirilir, yeni kimlikle aslının arkasına eklenir.
   *  Toplu: body.ids[] (values yok sayılır; ayırt edici alan otomatik "(kopya)" alır). */
  app.post('/api/admin/catalog/:entity/duplicate', requireAdmin, (req, res) => {
    const e = byId(req.params.entity);
    const c = CREATE[req.params.entity];
    if (!e || !c) return res.status(400).json({ error: 'Bu veri türü buradan çoğaltılamaz.' });
    const ids: string[] = (Array.isArray(req.body?.ids) ? req.body.ids : [req.body?.id]).filter(Boolean).map(String);
    if (!ids.length) return res.status(400).json({ error: 'id gerekli' });
    const created: string[] = [];
    try {
      for (const id of ids) {
        const base = e.load().find((x) => e.key(x) === id);
        if (!base) throw new Error(`Kayıt bulunamadı: ${id}`);
        const values = ids.length === 1 && req.body?.values ? req.body.values : dupForm(e.id, base);
        const rec = c.build(values, base);
        c.insert(rec, id);
        created.push(e.key(rec));
      }
      deps.onChange?.(e.id);
      res.json({ success: true, ids: created, id: created[0], note: e.source.startsWith('src/') ? 'Çoğaltıldı. Uygulamadaki paket bir sonraki derlemede güncellenir.' : 'Çoğaltıldı.' });
    } catch (err: any) {
      if (created.length) deps.onChange?.(e.id);
      res.status(400).json({ error: err.message, ids: created });
    }
  });

  /** Çıkmış soru sitede nasıl görünüyor: kendisi mi, birleştirildiği başka kopya mı, hiç mi (karantina/silinmiş) */
  const pastSiteState = (id: string): { status: 'shown' | 'merged' | 'hidden'; shownId?: string } | undefined => {
    if (!deps.getServedPast) return undefined;
    const served = deps.getServedPast();
    if (served.some((q) => String(q.id) === id)) return { status: 'shown' };
    const host = served.find((q) => Array.isArray(q.mergedFrom) && q.mergedFrom.map(String).includes(id));
    return host ? { status: 'merged', shownId: String(host.id) } : { status: 'hidden' };
  };

  app.get('/api/admin/catalog/:entity/:id', requireAdmin, (req, res) => {
    const e = byId(req.params.entity);
    if (!e) return res.status(404).json({ error: 'Bilinmeyen veri türü' });
    const x = e.load().find((r) => e.key(r) === req.params.id);
    if (!x) return res.status(404).json({ error: 'Kayıt bulunamadı' });
    let relations: RelationRef[] = [];
    try { relations = e.relations?.(x) || []; } catch (err: any) { relations = []; console.warn('[catalog] ilişki hatası:', err?.message); }
    // Büyük iç alanlar (deste slaytları) özetlenir; ayrıntı ilgili ekrandan açılır
    const record = e.id === 'decks'
      ? { ...x, slides: undefined, _slides: (x.slides || []).map((s: Any, i: number) => ({ n: s.slideNumber ?? i + 1, title: s.title, elements: (s.interactiveElements || s.elements || []).length })) }
      : x;
    res.json({ id: e.key(x), title: e.title(x), record, relations, ann: annOf(e.id, e.key(x)) || null, editable: e.save ? e.editable : [], form: CREATE[e.id] ? dupForm(e.id, x) : null, site: e.id === 'past' ? pastSiteState(e.key(x)) : undefined });
  });

  app.put('/api/admin/catalog/:entity/:id', requireAdmin, (req, res) => {
    const e = byId(req.params.entity);
    if (!e?.save) return res.status(400).json({ error: 'Bu veri türü buradan düzenlenemez (salt okunur).' });
    try {
      const saved = e.save(req.params.id, req.body?.patch || {});
      deps.onChange?.(e.id);
      res.json({ success: true, record: saved, note: e.source.startsWith('src/') ? 'Kaydedildi. Uygulamadaki paket bir sonraki derlemede güncellenir.' : 'Kaydedildi.' });
    } catch (err: any) {
      res.status(400).json({ error: err.message });
    }
  });

  /** Değerlendirme/sınıflandırma: tek ya da toplu (ids[]). Kaynak veri değişmez. */
  app.post('/api/admin/catalog/:entity/annotate', requireAdmin, (req, res) => {
    const e = byId(req.params.entity);
    if (!e) return res.status(404).json({ error: 'Bilinmeyen veri türü' });
    const ids: string[] = Array.isArray(req.body?.ids) ? req.body.ids.map(String) : [];
    if (!ids.length) return res.status(400).json({ error: 'ids gerekli' });
    const { status, tags, addTags, removeTags, note } = req.body || {};
    const all = { ...annAll() };
    const bucket = { ...(all[e.id] || {}) };
    const now = new Date().toISOString();
    for (const id of ids) {
      const cur: Annotation = bucket[id] || { status: '', tags: [], note: '', updatedAt: now };
      const next: Annotation = { ...cur, updatedAt: now, by: String(req.headers['x-admin-email'] || 'yönetici') };
      if (status !== undefined) next.status = (['', 'onayli', 'inceleme', 'sorunlu'].includes(status) ? status : cur.status) as ReviewStatus;
      if (Array.isArray(tags)) next.tags = Array.from(new Set(tags.map((t: unknown) => String(t).trim()).filter(Boolean)));
      if (Array.isArray(addTags)) next.tags = Array.from(new Set([...next.tags, ...addTags.map((t: unknown) => String(t).trim()).filter(Boolean)]));
      if (Array.isArray(removeTags)) next.tags = next.tags.filter((t) => !removeTags.includes(t));
      if (note !== undefined) next.note = String(note).slice(0, 2000);
      if (!next.status && !next.tags.length && !next.note) delete bucket[id];
      else bucket[id] = next;
    }
    all[e.id] = bucket;
    writeAnn(all);
    res.json({ success: true, updated: ids.length });
  });

  /**
   * Toplu silme. Varsayılan: kayıt kaynaktan çıkar ve ÇÖP KUTUSUNA gider (geri yüklenebilir).
   * permanent: true → çöp kutusuna gitmez, değerlendirmesi de silinir. Çöp kutusu türünde silme her zaman kalıcıdır.
   */
  app.post('/api/admin/catalog/:entity/delete', requireAdmin, async (req, res) => {
    const e = byId(req.params.entity);
    if (!e) return res.status(404).json({ error: 'Bilinmeyen veri türü' });
    if (!e.remove) return res.status(400).json({ error: `${e.label} buradan silinemez.` });
    const ids: string[] = Array.isArray(req.body?.ids) ? Array.from(new Set(req.body.ids.map(String))) : [];
    if (!ids.length) return res.status(400).json({ error: 'ids gerekli' });
    const permanent = e.id === 'trash' || req.body?.permanent === true;
    try {
      const removed = await e.remove(ids);
      if (e.id === 'trash') {
        // Çöp kutusundan kalıcı silme: kaydın değerlendirmesi de gider
        const byEnt = new Map<string, string[]>();
        for (const t of removed as TrashEntry[]) byEnt.set(t.entity, [...(byEnt.get(t.entity) || []), t.id]);
        for (const [ent, list] of byEnt) forget(ent, list);
      } else if (permanent) {
        forget(e.id, removed.map((x) => e.key(x)));
      } else if (removed.length) {
        const now = new Date().toISOString();
        const by = String(req.headers['x-admin-email'] || 'yönetici');
        const keys = new Set(removed.map((x) => `${e.id}:${e.key(x)}`));
        writeTrash([...trashAll().filter((t) => !keys.has(t.key)), ...removed.map((x) => ({ key: `${e.id}:${e.key(x)}`, entity: e.id, id: e.key(x), title: e.title(x), record: x, deletedAt: now, by }))]);
      }
      if (removed.length && e.id !== 'trash') deps.onChange?.(e.id);
      console.log(`[catalog] ${e.id}: ${removed.length}/${ids.length} kayıt ${permanent ? 'kalıcı olarak silindi' : 'çöp kutusuna taşındı'}`);
      res.json({ success: true, deleted: removed.length, requested: ids.length, permanent });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });

  /** Çöp kutusundan geri yükleme (anahtarlar: "<tür>:<id>") */
  app.post('/api/admin/catalog/trash/restore', requireAdmin, async (req, res) => {
    const keys = new Set<string>(Array.isArray(req.body?.ids) ? req.body.ids.map(String) : []);
    if (!keys.size) return res.status(400).json({ error: 'ids gerekli' });
    const list = trashAll();
    const picked = list.filter((t) => keys.has(t.key));
    const byEnt = new Map<string, TrashEntry[]>();
    for (const t of picked) byEnt.set(t.entity, [...(byEnt.get(t.entity) || []), t]);
    const done = new Set<string>();
    const errors: string[] = [];
    for (const [ent, entries] of byEnt) {
      const e = byId(ent);
      if (!e?.restore) { errors.push(`${labelOf(ent)} geri yüklenemez`); continue; }
      try {
        await e.restore(entries.map((t) => t.record));
        entries.forEach((t) => done.add(t.key));
        deps.onChange?.(ent);
      } catch (err: any) {
        errors.push(`${labelOf(ent)}: ${err.message}`);
      }
    }
    writeTrash(trashAll().filter((t) => !done.has(t.key)));
    res.status(errors.length && !done.size ? 500 : 200).json({ success: done.size > 0, restored: done.size, errors });
  });
}
