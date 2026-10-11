/**
 * Oy (beğeni) kuralları — soru, şık ve hafıza parçası için ortak.
 *
 * - Kaynak doğruluk `likedBy` listesidir; bir kullanıcı/cihaz yalnız bir kez sayılır.
 * - İkinci basış oyu geri çeker (toggle).
 * - Yeni kayıtlar 0 oyla başlar. Eskiden varsayılan olarak yazılan "1" (kimseye ait
 *   olmayan oy) 0'a indirilir.
 * - `likedBy` tutulmadan önce verilmiş eski oylar (sahibi bilinmeyen) silinmez;
 *   `upvotes - likedBy.length` farkı "eski taban" olarak korunur.
 */

export interface Votable {
  upvotes?: number;
  likedBy?: string[];
}

const ANON_IDS = new Set(['', 'anon', 'anonim-user', 'anonim-std', 'local_user', 'undefined', 'null']);

/** İstekten oy veren kimliğini çıkarır; kimlik yoksa null döner (oy reddedilir). */
export function voterIdFrom(req: { body?: any; query?: any; headers?: any }): string | null {
  const raw = req.body?.userId ?? req.query?.userId ?? req.headers?.['x-user-id'];
  const id = String(Array.isArray(raw) ? raw[0] : raw ?? '').trim().slice(0, 200);
  return ANON_IDS.has(id) ? null : id;
}

function uniqueVoters(target: Votable): string[] {
  const list = Array.isArray(target.likedBy) ? target.likedBy : [];
  return Array.from(new Set(list.filter((u) => typeof u === 'string' && u.trim() && !ANON_IDS.has(u.trim()))));
}

/** Sahibi bilinmeyen eski oy sayısı (varsayılan "1" sayılmaz). */
function legacyBase(target: Votable, voters: string[]): number {
  const count = typeof target.upvotes === 'number' && Number.isFinite(target.upvotes) ? target.upvotes : 0;
  if (voters.length === 0 && count <= 1) return 0;
  return Math.max(0, Math.floor(count) - voters.length);
}

/** Kaydı yerinde düzeltir: tekrarlı/anonim oyları ayıklar, varsayılan 1'i sıfırlar. */
export function normalizeVotes<T extends Votable>(target: T): T {
  if (!target || typeof target !== 'object') return target;
  const voters = uniqueVoters(target);
  target.upvotes = legacyBase(target, voters) + voters.length;
  target.likedBy = voters;
  return target;
}

/** Oyu açar/kapatır. Dönüş: işlemden sonra kullanıcının oyu duruyor mu. */
export function toggleVote(target: Votable, userId: string): boolean {
  const voters = uniqueVoters(target);
  const base = legacyBase(target, voters);
  const idx = voters.indexOf(userId);
  if (idx >= 0) voters.splice(idx, 1);
  else voters.push(userId);
  target.likedBy = voters;
  target.upvotes = base + voters.length;
  return idx < 0;
}

/** Bir sorunun kendisini, şıklarını ve parçalarını normalize eder. */
export function normalizeQuestionVotes<T extends Votable & { options?: Votable[]; fragments?: Votable[] }>(q: T): T {
  if (!q || typeof q !== 'object') return q;
  normalizeVotes(q);
  if (Array.isArray(q.options)) q.options.forEach((o) => normalizeVotes(o));
  if (Array.isArray(q.fragments)) q.fragments.forEach((f) => normalizeVotes(f));
  return q;
}
