/**
 * Soru karantinası (server-only): $MEDS_DATABASE_DIR/derived/quarantine/karantina.json
 * (scripts/advanced_ai/quarantine_questions.py üretir). Okuma uçlarında karantinadaki sorular gösterilmez,
 * onarılanlar temiz kök/şıklarla döner. Kaynak dosyalar DEĞİŞTİRİLMEZ (yazma yolları filtrelenmemiş listeyi kullanır).
 */
import fs from 'fs';
import path from 'path';

type QOpt = { key: string; text: string };
type QFile = { sorular: Record<string, { neden: string[] }>; onarim: Record<string, { stem: string; options: QOpt[] }> };
let cache: QFile | null = null;
let cacheMtime = 0;

const qFile = () =>
  path.join(process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database'), 'derived', 'quarantine', 'karantina.json');

function load(): QFile | null {
  try {
    const stat = fs.statSync(qFile());
    if (!cache || stat.mtimeMs !== cacheMtime) {
      cache = JSON.parse(fs.readFileSync(qFile(), 'utf-8')) as QFile;
      cacheMtime = stat.mtimeMs;
    }
  } catch {
    // liste yoksa filtre uygulanmaz
  }
  return cache;
}

// Doğrulanmış cevap anahtarı (hakem: slayt alıntılı, "emin") — derived/curriculum_links/cevap_anahtari.jsonl
const UNVERIFIED_SOURCES = new Set(['c4259dc9087e']); // sınav sitesi çıktısı: kayıtlı cevap = öğrencinin işaretlediği şık
let keyCache: Map<string, { cevap_metni: string; alinti?: string }> | null = null;
let keyMtime = 0;
const keyFile = () =>
  path.join(process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database'), 'derived', 'curriculum_links', 'cevap_anahtari.jsonl');

function loadKeys() {
  try {
    const stat = fs.statSync(keyFile());
    if (!keyCache || stat.mtimeMs !== keyMtime) {
      const m = new Map<string, { cevap_metni: string; alinti?: string }>();
      for (const line of fs.readFileSync(keyFile(), 'utf-8').split('\n')) {
        if (!line.trim()) continue;
        try {
          const r = JSON.parse(line);
          if (r.soru_id && r.cevap_metni) m.set(String(r.soru_id), { cevap_metni: r.cevap_metni, alinti: r.alinti });
        } catch { /* bozuk satır atlanır */ }
      }
      keyCache = m;
      keyMtime = stat.mtimeMs;
    }
  } catch { /* dosya yoksa */ }
  return keyCache;
}

/** combinepdf sorularında: doğrulanmış anahtar varsa onu uygula, yoksa cevabı "doğrulanmadı" olarak işaretle. */
function applyAnswerKey<T extends Record<string, any>>(item: T): T {
  if (!UNVERIFIED_SOURCES.has(String(item.sourceFile || ''))) return item;
  const k = loadKeys()?.get(String(item.id));
  const opts = (item.options || []) as any[];
  const rec = item.reconstruction && typeof item.reconstruction === 'object' ? item.reconstruction : null;
  const withRec = (key: string | undefined) =>
    rec ? { ...rec, correctAnswer: key, options: (rec.options || []).map((o: any) => ({ ...o, isCorrect: !!key && o.key === key })) } : rec;
  if (k) {
    const key = opts.find((o) => String(o?.text || '').trim() === k.cevap_metni.trim())?.key;
    if (key) {
      return { ...item, correctAnswer: key, claimedAnswer: key, reconstruction: withRec(key),
        options: opts.map((o) => ({ ...o, isCorrect: o.key === key })),
        answerStatus: 'dogrulandi', answerEvidence: k.alinti, updatedAt: new Date(Math.max(Date.parse(item.updatedAt || '') || 0, keyMtime)).toISOString() };
    }
  }
  // site cevabı reconstruction.correctAnswer → correctAnswer → claimedAnswer sırasıyla okur: üçü de boşaltılır
  return { ...item, correctAnswer: undefined, claimedAnswer: undefined, studentAnswer: item.correctAnswer,
    reconstruction: withRec(undefined), options: opts.map((o) => ({ ...o, isCorrect: false })),
    answerStatus: 'dogrulanmadi', answerNote: 'Cevap anahtarı doğrulanmadı (kaynak: sınav sistemi çıktısı, kayıtlı şık öğrencinin cevabıydı).',
    updatedAt: new Date(Math.max(Date.parse(item.updatedAt || '') || 0, keyMtime || cacheMtime)).toISOString() };
}

// Güvenilir müfredat bağlantısı (Faz 8 yüksek güven + hakem) — derived/curriculum_links/soru_kazanim.jsonl
type Link = { kurul?: number; ders?: string; konu?: string; kazanim?: string; guven?: string };
let linkCache: Map<string, Link> | null = null;
let linkMtime = 0;
const linkFile = () =>
  path.join(process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database'), 'derived', 'curriculum_links', 'soru_kazanim.jsonl');

// Kesin müfredat ataması (curriculum_resolve.py): sınav başlığı > kaynak dersi + Faz 8 kurulu > Faz 8 yüksek
let resolved: Map<string, Link & { kaynak?: string }> | null = null;
let resolvedMtime = 0;
const resolvedFile = () =>
  path.join(process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database'), 'derived', 'curriculum_links', 'soru_mufredat.json');

function loadResolved() {
  try {
    const stat = fs.statSync(resolvedFile());
    if (!resolved || stat.mtimeMs !== resolvedMtime) {
      const d = JSON.parse(fs.readFileSync(resolvedFile(), 'utf-8'));
      resolved = new Map(Object.entries(d.sorular || {}).map(([k, v]: [string, any]) => [k, { kurul: v.kurul, ders: v.ders, konu: v.konu || undefined, kazanim: v.kazanim, guven: v.kaynak, kaynak: v.kaynak }]));
      resolvedMtime = stat.mtimeMs;
    }
  } catch { /* dosya yoksa */ }
  return resolved;
}

function loadLinks() {
  try {
    const stat = fs.statSync(linkFile());
    if (!linkCache || stat.mtimeMs !== linkMtime) {
      const m = new Map<string, Link>();
      for (const line of fs.readFileSync(linkFile(), 'utf-8').split('\n')) {
        if (!line.trim()) continue;
        try {
          const r = JSON.parse(line);
          const k = (r.kazanimlar || [])[0] || {};
          if (r.soru_id && k.kurul) m.set(String(r.soru_id), { kurul: Number(k.kurul), ders: k.ders, konu: k.konu, kazanim: k.kazanim, guven: r.guven });
        } catch { /* bozuk satır */ }
      }
      linkCache = m;
      linkMtime = stat.mtimeMs;
    }
  } catch { /* dosya yoksa */ }
  return linkCache;
}

/** Kurul/ders içerikten düzeltilir: toplu "Kurul 1" etiketli sınav çıktıları ve hatalı ders etiketleri.
 *  Final/bütünleme sınav türü korunur (contentCommitteeId ile içerik kurulu filtresinde de görünür). */
function applyCurriculum<T extends Record<string, any>>(item: T): T {
  const l = loadResolved()?.get(String(item.id)) || loadLinks()?.get(String(item.id));
  if (!l || !l.kurul) {
    // sınav sistemi çıktısındaki "Kurul 1" toplu etikettir (çoğu yanlış): içerikten kurul bulunamadıysa belirsiz işaretlenir
    if (UNVERIFIED_SOURCES.has(String(item.sourceFile || '')) && item.committeeId === 'donem3-kurul1') {
      return { ...item, committeeUncertain: true,
        updatedAt: new Date(Math.max(Date.parse(item.updatedAt || '') || 0, resolvedMtime)).toISOString() };
    }
    return item;
  }
  const content = `donem3-kurul${l.kurul}`;
  const out: Record<string, any> = { ...item, contentCommitteeId: content, contentDiscipline: l.ders, contentTopic: l.konu,
    contentOutcome: l.kazanim, curriculumSource: (l as any).kaynak || (l.guven === 'hakem' ? 'hakem' : 'faz8_yuksek') };
  const cid = String(item.committeeId || '');
  if (/^donem3-kurul\d$/.test(cid) && cid !== content) {
    out.originalCommitteeId = cid;
    out.committeeId = content;
  }
  if (l.ders && item.discipline !== l.ders) {
    out.originalDiscipline = item.discipline;
    out.discipline = l.ders;
  }
  if (out.committeeId !== item.committeeId || out.discipline !== item.discipline) {
    // istemci önbelleği düzeltilmiş kurul/dersi delta senkronizasyonla alsın
    out.updatedAt = new Date(Math.max(Date.parse(item.updatedAt || '') || 0, resolvedMtime, linkMtime)).toISOString();
  }
  return out as T;
}

export function quarantineMtime(): number {
  load();
  loadKeys();
  loadLinks();
  loadResolved();
  return Math.max(cacheMtime, keyMtime, linkMtime, resolvedMtime);
}

export function applyQuarantine<T extends { id?: string; stem?: string; options?: any[]; correctAnswer?: string }>(list: T[]): T[] {
  const q = load();
  if (!q) return list;
  const out: T[] = [];
  for (const item of list) {
    const id = String(item.id);
    const fix = q.onarim?.[id];          // onarımı olan soru (veritabanı kopyası bozuk olsa da) onarılmış hâliyle gösterilir
    if (!fix && q.sorular?.[id]) continue;
    if (fix) {
      // doğru cevabı şık metnine göre eşle (onarımda harfler kayabilir)
      const oldCorrect = (item.options || []).find((o: any) => o?.key === item.correctAnswer)?.text;
      const newCorrect = fix.options.find((o) => oldCorrect && o.text.trim() === String(oldCorrect).trim())?.key;
      out.push({
        ...item,
        stem: fix.stem,
        options: fix.options.map((o) => ({ ...o, isCorrect: o.key === newCorrect })),
        correctAnswer: newCorrect || item.correctAnswer,
        repaired: true,
        // istemci önbelleği onarılmış hâli delta senkronizasyonla alsın
        updatedAt: new Date(Math.max(Date.parse((item as any).updatedAt || '') || 0, cacheMtime)).toISOString(),
      });
    } else {
      out.push(item);
    }
  }
  return out.map((x) => applyCurriculum(applyAnswerKey(x)));
}
