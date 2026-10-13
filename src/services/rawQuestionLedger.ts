/**
 * Ham soru defteri (append-only).
 *
 * Kullanıcıların havuza eklediği her soru ve o soruya yapılan her katkı (ipucu/parça, şık ekleme,
 * "şu şık yoktu" itirazı, cevap iddiası, yorum, bildirim, oy) soru başına TEK bir kümede ham olay
 * olarak saklanır: data/question_ledger/<id>.jsonl.
 *
 * Kurallar:
 * - Dosyaya yalnız EKLENİR; hiçbir kod yolu satır silmez ya da değiştirmez (karma zinciri bozulmayı gösterir).
 * - Yapay zekâ çıktıları ayrı olay türüdür (ai_*); ham veriyi değiştirmez.
 * - saveDatabase her kayıtta önceki/sonraki hali karşılaştırır (recordAndGuard): kullanıcı katkısı
 *   kaybolmuşsa geri koyar ve olayı yazar. Yalnız yönetici silmesi (allowRemoval) kaldırmaya izin verir;
 *   o durumda da tam anlık görüntü deftere yazılır.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

export type LedgerActorKind = 'user' | 'admin' | 'ai' | 'system';
export interface LedgerActor { kind: LedgerActorKind; uid?: string; name?: string; email?: string }
export interface LedgerEvent {
  eventId: string;
  qid: string;
  ts: string;
  seq: number;
  type: string;
  actor: LedgerActor;
  payload: any;
  prevHash: string;
  hash: string;
}

/** Soruda kullanıcı katkısı taşıyan diziler ve öge kimliği. */
const CONTRIB_ARRAYS: Record<string, (x: any) => string> = {
  fragments: (x) => String(x?.id ?? x?.text ?? ''),
  options: (x) => `${x?.key ?? ''}|${String(x?.text ?? '').trim()}`,
  alternativeOptions: (x) => String(x?.id ?? `${x?.key ?? ''}|${x?.text ?? ''}`),
  comments: (x) => String(x?.id ?? x?.text ?? ''),
  reports: (x) => String(x?.id ?? x?.reason ?? ''),
  mergedSatellites: (x) => String(x?.id ?? JSON.stringify(x)),
};
const VOTE_ARRAYS = ['likedBy', 'dislikedBy'];
const IGNORED_FIELDS = new Set(['updatedAt', 'upvotes', 'downvotes', 'status']);

let LEDGER_DIR = '';
const lastHash = new Map<string, { seq: number; hash: string }>();
const snapshots = new Map<string, string>();
let mirror: ((ev: LedgerEvent) => void) | null = null;
let removalAllowance = new Set<string>();

const safe = (id: string) => String(id).replace(/[^A-Za-z0-9._-]/g, '_').slice(0, 160);
const fileOf = (qid: string) => path.join(LEDGER_DIR, `${safe(qid)}.jsonl`);
const sha = (s: string) => crypto.createHash('sha256').update(s).digest('hex');

export function initLedger(dataDir: string, onEvent?: (ev: LedgerEvent) => void) {
  LEDGER_DIR = path.join(dataDir, 'question_ledger');
  fs.mkdirSync(LEDGER_DIR, { recursive: true });
  mirror = onEvent || null;
}

function tail(qid: string) {
  const cached = lastHash.get(qid);
  if (cached) return cached;
  const f = fileOf(qid);
  let out = { seq: 0, hash: 'GENESIS' };
  if (fs.existsSync(f)) {
    const lines = fs.readFileSync(f, 'utf-8').trim().split('\n').filter(Boolean);
    const last = lines.length ? JSON.parse(lines[lines.length - 1]) : null;
    if (last) out = { seq: last.seq, hash: last.hash };
  }
  lastHash.set(qid, out);
  return out;
}

export function appendEvent(qid: string, type: string, actor: LedgerActor, payload: any): LedgerEvent {
  if (!LEDGER_DIR) throw new Error('ledger başlatılmadı');
  const t = tail(qid);
  const base = {
    eventId: `ev-${Date.now().toString(36)}-${crypto.randomBytes(4).toString('hex')}`,
    qid: String(qid),
    ts: new Date().toISOString(),
    seq: t.seq + 1,
    type,
    actor,
    payload,
    prevHash: t.hash,
  };
  const ev: LedgerEvent = { ...base, hash: sha(t.hash + JSON.stringify(base)) };
  // 'a' bayrağı: yalnız sona ekleme. fsync ile diske indirilir — veri kaybı kabul edilmez.
  const fd = fs.openSync(fileOf(qid), 'a');
  try { fs.writeSync(fd, JSON.stringify(ev) + '\n'); fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
  lastHash.set(qid, { seq: ev.seq, hash: ev.hash });
  try { mirror?.(ev); } catch { /* yansı en iyi çaba */ }
  return ev;
}

export function readEvents(qid: string): LedgerEvent[] {
  const f = fileOf(qid);
  if (!fs.existsSync(f)) return [];
  return fs.readFileSync(f, 'utf-8').split('\n').filter(Boolean).map((l) => JSON.parse(l));
}

export function verifyChain(qid: string): { ok: boolean; brokenAt?: number } {
  let prev = 'GENESIS';
  for (const ev of readEvents(qid)) {
    const { hash, ...rest } = ev;
    if (ev.prevHash !== prev || sha(prev + JSON.stringify(rest)) !== hash) return { ok: false, brokenAt: ev.seq };
    prev = hash;
  }
  return { ok: true };
}

export function listLedgerIds(): string[] {
  if (!LEDGER_DIR || !fs.existsSync(LEDGER_DIR)) return [];
  return fs.readdirSync(LEDGER_DIR).filter((f) => f.endsWith('.jsonl')).map((f) => {
    const first = fs.readFileSync(path.join(LEDGER_DIR, f), 'utf-8').split('\n', 1)[0];
    try { return JSON.parse(first).qid as string; } catch { return f.replace(/\.jsonl$/, ''); }
  });
}

/** Bir sorunun ham kümesi: olaylar türe göre gruplanmış hali + yönetici sınıflandırması + son hal. */
export function buildCluster(qid: string, current?: any) {
  const events = readEvents(qid);
  const by = (types: string[]) => events.filter((e) => types.includes(e.type));
  // İlk anlık görüntüdeki (defter öncesi / ilk ekleme) katkılar da kümeye girer.
  const origin = by(['baseline', 'question_created'])[0];
  const seed = (field: string) => (Array.isArray(origin?.payload?.[field]) ? origin!.payload[field] : []).map((x: any) => ({ ...x, ts: x.timestamp || x.createdAt || origin!.ts, fromSnapshot: true }));
  const classes = by(['admin_classify']).reduce((acc: any, e) => ({ ...acc, ...e.payload }), {});
  return {
    qid,
    eventCount: events.length,
    chain: verifyChain(qid),
    firstSeen: events[0]?.ts,
    lastEvent: events[events.length - 1]?.ts,
    classification: classes,
    original: by(['baseline', 'question_created'])[0]?.payload ?? null,
    contributions: {
      fragments: [...seed('fragments'), ...by(['fragment_added']).map((e) => ({ ...e.payload, ts: e.ts, actor: e.actor }))],
      options: [...seed('options'), ...by(['option_added']).map((e) => ({ ...e.payload, ts: e.ts, actor: e.actor }))],
      alternativeOptions: [...seed('alternativeOptions'), ...by(['alternativeOption_added']).map((e) => ({ ...e.payload, ts: e.ts, actor: e.actor }))],
      comments: [...seed('comments'), ...by(['comment_added']).map((e) => ({ ...e.payload, ts: e.ts, actor: e.actor }))],
      reports: [...seed('reports'), ...by(['report_added']).map((e) => ({ ...e.payload, ts: e.ts, actor: e.actor }))],
      votes: by(['vote_added', 'vote_removed']).map((e) => ({ type: e.type, ...e.payload, ts: e.ts })),
      fieldChanges: by(['field_changed']).map((e) => ({ ...e.payload, ts: e.ts, actor: e.actor })),
    },
    ai: by(['ai_suggestion']).map((e) => ({ ...e.payload, ts: e.ts, actor: e.actor })),
    admin: by(['admin_edit', 'admin_classify', 'admin_delete', 'admin_note']).map((e) => ({ type: e.type, ...e.payload, ts: e.ts, actor: e.actor })),
    guard: by(['guard_restored']).map((e) => ({ ...e.payload, ts: e.ts })),
    current: current ?? null,
    events,
  };
}

/** Yönetici silmesi için tek seferlik izin (endpoint saveDatabase'den hemen önce çağırır). */
export function allowRemoval(qid: string, actor: LedgerActor, snapshot: any, reason = '') {
  appendEvent(qid, 'admin_delete', actor, { reason, snapshot });
  removalAllowance.add(String(qid));
}

/** Açılışta: defteri olmayan her soruya mevcut halinin tam kopyasıyla 'baseline' yazılır. */
export function seedBaselines(questions: any[]) {
  let n = 0;
  for (const q of questions || []) {
    if (!q?.id) continue;
    if (!fs.existsSync(fileOf(q.id))) {
      appendEvent(q.id, 'baseline', { kind: 'system', name: 'defter-öncesi-durum' }, JSON.parse(JSON.stringify(q)));
      n++;
    }
    snapshots.set(String(q.id), JSON.stringify(q));
  }
  return n;
}

const actorFrom = (x: any): LedgerActor => ({
  kind: x?.isAiGenerated || x?.isAiFilled ? 'ai' : 'user',
  uid: x?.authorUid || x?.suggestedByUid || x?.reporterUid || undefined,
  name: x?.author || x?.suggestedBy || x?.reportedBy || undefined,
});

/**
 * saveDatabase'den yazmadan ÖNCE çağrılır. Değişiklikleri deftere yazar, kaybolan kullanıcı katkısını
 * ve izinsiz silinen soruları geri koyar. `questions` yerinde düzeltilebilir (dizi döner).
 */
export function recordAndGuard(questions: any[]): any[] {
  const nextIds = new Set<string>();
  for (const q of questions) {
    if (!q?.id) continue;
    const id = String(q.id);
    nextIds.add(id);
    const prevRaw = snapshots.get(id);
    if (!prevRaw) {
      appendEvent(id, 'question_created', { kind: q.isAiGenerated ? 'ai' : 'user', uid: q.contributedByUid, name: q.contributedByName }, JSON.parse(JSON.stringify(q)));
      snapshots.set(id, JSON.stringify(q));
      continue;
    }
    const curRaw = JSON.stringify(q);
    if (curRaw === prevRaw) continue;
    const prev = JSON.parse(prevRaw);

    for (const [field, keyOf] of Object.entries(CONTRIB_ARRAYS)) {
      const before: any[] = Array.isArray(prev[field]) ? prev[field] : [];
      const after: any[] = Array.isArray(q[field]) ? q[field] : [];
      const afterKeys = new Set(after.map(keyOf));
      const beforeKeys = new Set(before.map(keyOf));
      for (const item of after) {
        if (!beforeKeys.has(keyOf(item))) appendEvent(id, `${field.replace(/s$/, '')}_added`, actorFrom(item), item);
      }
      const lost = before.filter((item) => !afterKeys.has(keyOf(item)));
      if (lost.length) {
        if (field === 'options') {
          // Şık metni değiştirildiyse eski metin alternatif şık olarak korunur; aynı harf yeni metni taşır.
          q.alternativeOptions = [...(Array.isArray(q.alternativeOptions) ? q.alternativeOptions : []),
            ...lost.map((o) => ({ ...o, id: `opt-${o.key}-${sha(String(o.text)).slice(0, 8)}`, preservedFrom: 'options' }))];
        } else {
          q[field] = [...after, ...lost];
        }
        appendEvent(id, 'guard_restored', { kind: 'system', name: 'koruma' }, { field, items: lost });
      }
      // Aynı kimlikli ögenin içeriği değiştiyse önceki hali kayda geçer (ham hal defterde kalır).
      if (field !== 'options') {
        const prevById = new Map(before.map((x) => [keyOf(x), JSON.stringify(x)]));
        for (const item of after) {
          const p = prevById.get(keyOf(item));
          if (p && p !== JSON.stringify(item)) appendEvent(id, 'field_changed', { kind: 'system' }, { field, key: keyOf(item), before: JSON.parse(p), after: item });
        }
      }
    }
    for (const field of VOTE_ARRAYS) {
      const b = new Set<string>((prev[field] || []).map(String));
      const a = new Set<string>((q[field] || []).map(String));
      for (const v of a) if (!b.has(v)) appendEvent(id, 'vote_added', { kind: 'user', uid: v }, { field, voter: v });
      for (const v of b) if (!a.has(v)) appendEvent(id, 'vote_removed', { kind: 'user', uid: v }, { field, voter: v });
    }
    for (const k of new Set([...Object.keys(prev), ...Object.keys(q)])) {
      if (k in CONTRIB_ARRAYS || VOTE_ARRAYS.includes(k) || IGNORED_FIELDS.has(k) || k === 'alternativeOptions') continue;
      const b = JSON.stringify(prev[k]);
      const a = JSON.stringify(q[k]);
      if (a !== b) appendEvent(id, 'field_changed', { kind: 'system' }, { field: k, before: prev[k] ?? null, after: q[k] ?? null });
    }
    snapshots.set(id, JSON.stringify(q));
  }

  // İzinsiz kaybolan sorular geri konur.
  for (const [id, raw] of [...snapshots.entries()]) {
    if (nextIds.has(id)) continue;
    if (removalAllowance.has(id)) { snapshots.delete(id); removalAllowance.delete(id); continue; }
    questions.push(JSON.parse(raw));
    appendEvent(id, 'guard_restored', { kind: 'system', name: 'koruma' }, { field: '*', note: 'yetkisiz soru silme engellendi' });
  }
  return questions;
}
