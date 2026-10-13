/**
 * Öğren hata defteri + aralıklı tekrar kuyruğu + odak seansı kayıtları (yalnız istemci; profil eşitlemesiyle
 * cihazlar arası taşınır — userKvSync izin listesi: medsoru_learn_review_v1, medsoru_learn_sessions_v1).
 *
 * - Ders içinde doğruluğu ölçülebilen bir etkileşim YANLIŞ yapılınca öge kutu 0'a girer, ertesi gün vadesi gelir.
 * - Tekrar ekranında doğru yapılırsa bir üst kutuya çıkar (1-3-7-14-30 gün; FlashcardsView'daki Leitner aralıkları),
 *   yine yanlışsa kutu 0'a döner. 5. kutuyu geçen öge "öğrenildi" sayılır, defterde kalır ama kuyruğa girmez.
 * - Ders içinde DOĞRU yapılan öge deftere eklenmez (defter = hatalar); defterdeki bir öge ders içinde doğru
 *   yapılırsa da bir kutu ilerler.
 * - Öge kimliği: deste + slayt numarası + etkileşim sırası; içerik özeti (`sig`) değişirse (deste güncellendi)
 *   öge tekrar ekranında sessizce düşer.
 * - Deneme günlüğü (son 500, yalnız bu cihaz) odak seansının dikkat nabzı ve kişisel hız ortalaması içindir.
 */
import type { IxResult, PracticeItem } from '../components/learn/lesson/lessonModel';

export const REVIEW_KEY = 'medsoru_learn_review_v1';
export const SESSIONS_KEY = 'medsoru_learn_sessions_v1';
const ATTEMPTS_KEY = 'medsoru_learn_attempts_v1';
const DAY = 86_400_000;
/** Kutu → bir sonraki tekrara kalan gün (kutu 0 = ertesi gün) */
const INTERVALS = [1, 1, 3, 7, 14, 30];
export const MASTER_BOX = INTERVALS.length;
export const REVIEW_EVENT = 'medsoru:learn-review-changed';
/** Bugün ekranından "Tekrara başla": Öğren açılınca tekrar ekranı açılır (sessionStorage bayrağı) */
export const OPEN_REVIEW_FLAG = 'medsoru_open_learn_review';

export interface ReviewEntry {
  key: string;
  deckId: string;
  deckTitle: string;
  slide: number;
  /** Adımın etkileşim listesindeki sırası (practiceOf sırası) */
  ix: number;
  type: string;
  stepTitle: string;
  sig: string;
  box: number;
  due: number;
  wrong: number;
  right: number;
  first: number;
  last: number;
}
export interface Attempt {
  deckId: string;
  slide: number;
  ix: number;
  type: string;
  ok: boolean;
  ms?: number;
  at: number;
  review?: boolean;
}
export interface FocusSessionLog {
  id: string;
  deckId: string;
  deckTitle: string;
  start: number;
  activeMs: number;
  plannedMin: number;
  goal: string;
  stepsDone: number;
  ix: number;
  correct: number;
  weak: { slide: number; title: string; wrong: number }[];
}

const read = <T,>(k: string, fb: T): T => {
  try {
    const v = JSON.parse(localStorage.getItem(k) || 'null');
    return v ?? fb;
  } catch {
    return fb;
  }
};
const write = (k: string, v: unknown) => {
  try {
    localStorage.setItem(k, JSON.stringify(v));
  } catch {
    /* depolama dolu ya da kapalı: defter bu oturumda tutulmaz */
  }
};

/** Etkileşimin içerik özeti: deste güncellenip öge değişirse eski kayıt eşleşmez */
export const itemSig = (p: PracticeItem): string => {
  const raw = p.kind === 'ix' ? JSON.stringify(p.data) : p.kind === 'question' ? p.q.id + p.q.stem : JSON.stringify(p.cards.map((c) => c.front));
  let h = 2166136261;
  for (let i = 0; i < raw.length; i++) h = Math.imul(h ^ raw.charCodeAt(i), 16777619);
  return (h >>> 0).toString(36);
};
export const itemType = (p: PracticeItem) => (p.kind === 'ix' ? String(p.data?.type || 'ix') : p.kind);
const keyOf = (deckId: string, slide: number, ix: number) => `${deckId}|${slide}|${ix}`;
const tomorrow = (now: number) => {
  const d = new Date(now);
  d.setHours(4, 0, 0, 0); // gün dönümü sabah 4: gece yarısı çalışan öğrencinin "yarın"ı uyuyunca gelir
  return d.getTime() + (d.getTime() <= now ? DAY : 0);
};
const nextDue = (box: number, now: number) => (box <= 0 ? tomorrow(now) : now + INTERVALS[Math.min(box, INTERVALS.length - 1)] * DAY);

export const readReview = (): Record<string, ReviewEntry> => read<Record<string, ReviewEntry>>(REVIEW_KEY, {});
const writeReview = (m: Record<string, ReviewEntry>) => {
  write(REVIEW_KEY, m);
  try {
    window.dispatchEvent(new Event(REVIEW_EVENT));
  } catch {
    /* sunucu tarafı */
  }
};
export const readAttempts = (): Attempt[] => read<Attempt[]>(ATTEMPTS_KEY, []);

export interface RecordCtx {
  deckId: string;
  deckTitle: string;
  slide: number;
  stepTitle: string;
  ix: number;
  item: PracticeItem;
  review?: boolean;
}

/** Bir etkileşim sonucunu deftere ve günlüğe işler. Dönen değer: öge defterde mi (yanlış ya da daha önce yanlış) */
export function recordResult(c: RecordCtx, r: IxResult, now = Date.now()): ReviewEntry | null {
  const att: Attempt = { deckId: c.deckId, slide: c.slide, ix: c.ix, type: itemType(c.item), ok: r.ok, ms: r.ms, at: now, review: c.review };
  write(ATTEMPTS_KEY, [...readAttempts(), att].slice(-500));

  const all = readReview();
  const key = keyOf(c.deckId, c.slide, c.ix);
  const sig = itemSig(c.item);
  const cur = all[key] && all[key].sig === sig ? all[key] : null;
  if (r.ok && !cur) return null;
  const base: ReviewEntry = cur || {
    key, deckId: c.deckId, deckTitle: c.deckTitle, slide: c.slide, ix: c.ix, type: att.type, stepTitle: c.stepTitle,
    sig, box: 0, due: 0, wrong: 0, right: 0, first: now, last: now,
  };
  const box = r.ok ? Math.min(MASTER_BOX, base.box + 1) : 0;
  const next: ReviewEntry = {
    ...base, deckTitle: c.deckTitle, stepTitle: c.stepTitle, box,
    due: box >= MASTER_BOX ? Number.MAX_SAFE_INTEGER : nextDue(box, now),
    wrong: base.wrong + (r.ok ? 0 : 1), right: base.right + (r.ok ? 1 : 0), last: now,
  };
  all[key] = next;
  writeReview(all);
  return next;
}

export const isMastered = (e: ReviewEntry) => e.box >= MASTER_BOX;
export const dueEntries = (now = Date.now(), deckId?: string) =>
  Object.values(readReview()).filter((e) => !isMastered(e) && e.due <= now && (!deckId || e.deckId === deckId));
export const openEntries = (deckId?: string) =>
  Object.values(readReview()).filter((e) => !isMastered(e) && (!deckId || e.deckId === deckId));
export const dropEntry = (key: string) => {
  const all = readReview();
  if (!all[key]) return;
  delete all[key];
  writeReview(all);
};
/** Deste başına açık (öğrenilmemiş) ve vadesi gelmiş öge sayısı */
export const reviewCounts = (now = Date.now()) => {
  const out: Record<string, { open: number; due: number }> = {};
  for (const e of Object.values(readReview())) {
    if (isMastered(e)) continue;
    const o = (out[e.deckId] ||= { open: 0, due: 0 });
    o.open++;
    if (e.due <= now) o.due++;
  }
  return out;
};

/** Kişisel yanıt hızı: son denemelerin ortanca süresi (ms); yeterli örnek yoksa null */
export const medianMs = (): number | null => {
  const ms = readAttempts().map((a) => a.ms).filter((x): x is number => typeof x === 'number' && x > 300 && x < 600_000).sort((a, b) => a - b);
  return ms.length >= 10 ? ms[Math.floor(ms.length / 2)] : null;
};

export const readSessions = (): FocusSessionLog[] => read<FocusSessionLog[]>(SESSIONS_KEY, []);
export const saveSession = (s: FocusSessionLog) => write(SESSIONS_KEY, [...readSessions().filter((x) => x.id !== s.id), s].slice(-100));
