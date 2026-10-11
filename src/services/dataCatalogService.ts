/**
 * Veri kataloğu (yönetim) — sunucu tarafı. Uygulamadaki her veri türü tek arayüzle:
 *  - listelenir, aranır, sınıflara (facet) göre süzülür ve sıralanır,
 *  - tek kayıt olarak açılır; izin verilen alanları düzenlenir (yedekli, atomik yazma),
 *  - ayrı ayrı DEĞERLENDİRİLİR ve SINIFLANDIRILIR: durum (onaylı / inceleme / sorunlu), etiketler, not.
 *    Bu "açıklama katmanı" kaynak veriyi değiştirmez; data/catalog_annotations.json'da tutulur.
 *  - ilişkileri gösterilir: deste ↔ kazanım ↔ örnek soru ↔ çıkmış soru ↔ sözlük terimi ↔ hastalık.
 *
 * Yeni veri türü eklemek = ENTITIES listesine bir bağdaştırıcı. Ham dosya biçimi (girinti) korunarak yazılır.
 * server.ts yalnız registerDataCatalogRoutes(app, requireAdmin, deps) çağırır.
 */
import fs from 'fs';
import path from 'path';
import type express from 'express';

type Any = Record<string, any>;

export interface CatalogDeps {
  rootDir: string;
  dataDir: string;
  getPastQuestions: () => any[];
  savePastQuestions: (list: any[]) => void;
  getDecks: () => any[];
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
}

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
function detectIndent(file: string): number {
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
  const musicFile = path.join(SRC, 'musicTracks.json');
  const decksFile = path.join(SRC, 'interactive_learning_decks.json');

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
    },
    {
      id: 'pool', label: 'Soru havuzu', group: 'Sorular', source: 'data/questions.json',
      editable: [],
      facets: [{ key: 'committeeId', label: 'Kurul' }, { key: 'status', label: 'Durum' }],
      load: () => (readJson(path.join(deps.dataDir, 'questions.json'), {}).questions || []),
      key: (x) => String(x.id), title: (x) => clip(x.stem || x.text || x.title || (x.fragments || [])[0]?.text), subtitle: (x) => [x.committeeId, x.status].filter(Boolean).join(' · '),
      facet: (x, k) => (x[k] == null ? undefined : String(x[k])),
      text: (x) => `${x.id} ${x.stem || ''} ${x.text || ''} ${(x.fragments || []).map((f: Any) => f?.text).join(' ')}`,
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
            return { ...r, kind: 'Örnek soru', field: r.reason, _id: `ornek:${r.soru_id}:${r.timestamp || i}` };
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
    },
    {
      id: 'music', label: 'Müzik listesi', group: 'Topluluk', source: 'src/data/musicTracks.json',
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
        writeJsonAtomic(musicFile, list, BACKUP);
        return t;
      },
    },
  ];
  const byId = (id: string) => ENTITIES.find((e) => e.id === id);

  /* ---------- uçlar ---------- */
  app.get('/api/admin/catalog', requireAdmin, (_req, res) => {
    const ann = annAll();
    res.json({
      entities: ENTITIES.map((e) => {
        let count = 0;
        try { count = e.load().length; } catch { /* okunamadı */ }
        const a = Object.values(ann[e.id] || {});
        return {
          id: e.id, label: e.label, group: e.group, source: e.source, editable: e.editable, arrays: e.arrays || [], facets: e.facets, count,
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
    const total = rows.length;
    const items = rows.slice(page * size, page * size + size).map((x) => ({ id: e.key(x), title: e.title(x), subtitle: e.subtitle?.(x) || '', ann: ann[e.key(x)] || null }));
    res.json({ total, page, size, items, facets });
  });

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
    res.json({ id: e.key(x), title: e.title(x), record, relations, ann: annOf(e.id, e.key(x)) || null, editable: e.save ? e.editable : [] });
  });

  app.put('/api/admin/catalog/:entity/:id', requireAdmin, (req, res) => {
    const e = byId(req.params.entity);
    if (!e?.save) return res.status(400).json({ error: 'Bu veri türü buradan düzenlenemez (salt okunur).' });
    try {
      const saved = e.save(req.params.id, req.body?.patch || {});
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
    fs.mkdirSync(path.dirname(ANN_FILE), { recursive: true });
    const tmp = `${ANN_FILE}.${process.pid}.tmp`;
    fs.writeFileSync(tmp, JSON.stringify(all, null, 1), 'utf8');
    fs.renameSync(tmp, ANN_FILE);
    fileCache.delete(ANN_FILE);
    res.json({ success: true, updated: ids.length });
  });
}
