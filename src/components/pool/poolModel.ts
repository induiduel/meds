import type { QuestionItem } from '../../types';
import { questionStemText } from '../QuickAddHero';

/**
 * Soru havuzu (v11) veri yardımcıları: son etkinlik, şık doluluğu, katkıcılar ve katkı olayları.
 * Hepsi saf işlevlerdir; ekran bileşenleri (PoolView, PoolRow, PoolLiveFeed) useMemo ile çağırır.
 */

export const OPTION_KEYS = ['A', 'B', 'C', 'D', 'E'] as const;
export type PoolSegment = 'new' | 'order' | 'missing' | 'mine';

export const HOUR = 3600_000;
export const DAY = 24 * HOUR;

const ts = (v?: string | number | null): number => {
  if (v == null || v === '') return 0;
  const n = typeof v === 'number' ? v : Date.parse(v);
  return Number.isFinite(n) ? n : 0;
};

export type PoolEventKind = 'stem' | 'option' | 'clue' | 'answer' | 'optionKey' | 'comment' | 'revision' | 'create';

export interface PoolEvent {
  id: string;
  qid: string;
  qno: number;
  who: string;
  uid?: string;
  kind: PoolEventKind;
  /** "B şıkkını ekledi" gibi eylem cümlesi (özne hariç) */
  action: string;
  text: string;
  at: number;
}

const FRAGMENT_ACTION: Record<string, string> = {
  stem: 'kök parçası ekledi',
  option: 'şık parçası ekledi',
  clue: 'ipucu ekledi',
  answer: 'cevap önerdi',
};

const anon = (n?: string | null) => (n && n.trim()) || 'Anonim';

/** Bir sorudaki tüm katkıları olay listesine çevirir (yeniden eskiye; zamansızlar sonda). */
export function questionEvents(q: QuestionItem): PoolEvent[] {
  const out: PoolEvent[] = [];
  const qno = q.questionNumber || 0;
  const created = ts((q as any).createdAt);
  if (q.contributedByName && created) {
    out.push({ id: `${q.id}:c`, qid: q.id, qno, who: anon(q.contributedByName), uid: q.contributedByUid, kind: 'create', action: 'soruyu açtı', text: '', at: created });
  }
  (q.fragments || []).forEach((f, i) => {
    out.push({
      id: `${q.id}:f:${f.id || i}`, qid: q.id, qno, who: anon(f.author), uid: f.authorUid,
      kind: f.type, action: FRAGMENT_ACTION[f.type] || 'parça ekledi', text: f.text || '', at: ts(f.timestamp),
    });
  });
  (q.options || []).forEach((o) => {
    if (!o.text?.trim() || o.isAiGenerated) return;
    out.push({
      id: `${q.id}:o:${o.key}`, qid: q.id, qno, who: anon(o.suggestedBy), uid: o.suggestedByUid,
      kind: 'optionKey', action: `${o.key} şıkkını ekledi`, text: o.text, at: ts((o as any).timestamp || (o as any).createdAt),
    });
  });
  (q.comments || []).forEach((c, i) => {
    out.push({ id: `${q.id}:m:${c.id || i}`, qid: q.id, qno, who: anon(c.author), kind: 'comment', action: 'yorum yaptı', text: c.text || '', at: ts(c.createdAt) });
  });
  (q.revisions || []).forEach((r, i) => {
    out.push({
      id: `${q.id}:r:${r.id || i}`, qid: q.id, qno, who: anon(r.editorName), uid: r.editorUid,
      kind: 'revision', action: `düzenledi (v${r.version ?? i + 1})`, text: r.changeSummary || '', at: ts(r.editedAt),
    });
  });
  return out.sort((a, b) => b.at - a.at);
}

export interface PoolSummary {
  q: QuestionItem;
  stem: string;
  hasStem: boolean;
  /** Metni olan şık harfleri */
  filled: Set<string>;
  lastAt: number;
  firstAt: number;
  people: { name: string; key: string }[];
  comments: number;
  events: PoolEvent[];
}

export function summarize(q: QuestionItem): PoolSummary {
  const events = questionEvents(q);
  const stemSrc = q.reconstruction?.stem || q.rawStem || q.stem || q.fragments?.find((f) => f.type === 'stem')?.text;
  const filled = new Set<string>();
  (q.reconstruction?.options || []).forEach((o) => { if (o.text?.trim()) filled.add(o.key); });
  (q.options || []).forEach((o) => { if (o.text?.trim()) filled.add(o.key); });
  const dated = events.filter((e) => e.at > 0);
  const extra = [ts((q as any).updatedAt), ts(q.customRedactedAt)];
  const lastAt = Math.max(0, ...dated.map((e) => e.at), ...extra);
  const firstAt = dated.length ? Math.min(...dated.map((e) => e.at)) : ts((q as any).createdAt);
  // Katkıcılar: en yeni katkı önce, aynı kişi bir kez
  const seen = new Set<string>();
  const people: PoolSummary['people'] = [];
  const push = (name: string, uid?: string) => {
    const key = uid || name.toLocaleLowerCase('tr-TR');
    if (seen.has(key)) return;
    seen.add(key);
    people.push({ name, key });
  };
  events.filter((e) => e.kind !== 'comment' && e.kind !== 'revision').forEach((e) => push(e.who, e.uid));
  if (q.contributedByName) push(q.contributedByName, q.contributedByUid);
  return {
    q,
    stem: (stemSrc || questionStemText(q) || '').replace(/\s+/g, ' ').trim(),
    hasStem: !!stemSrc?.trim(),
    filled,
    lastAt,
    firstAt,
    people,
    comments: q.comments?.length || 0,
    events,
  };
}

export const isMissing = (s: PoolSummary) => s.filled.size < 5 || !s.hasStem;

/** "Ayşe Bilgin" → "Ayşe B." */
export function shortName(name: string): string {
  const parts = name.trim().split(/\s+/);
  if (parts.length < 2) return name.trim();
  return `${parts[0]} ${parts[parts.length - 1].charAt(0).toLocaleUpperCase('tr-TR')}.`;
}

export function initials(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (!parts.length) return '?';
  const a = parts[0].charAt(0);
  const b = parts.length > 1 ? parts[parts.length - 1].charAt(0) : parts[0].charAt(1);
  return (a + (b || '')).toLocaleUpperCase('tr-TR');
}

/** Katkıcı rengi: isimden kararlı ton (5 anlamsal ton; renkler CSS'te) */
export function toneOf(key: string): number {
  let h = 0;
  for (let i = 0; i < key.length; i++) h = (h * 31 + key.charCodeAt(i)) >>> 0;
  return h % 5;
}

/** Kısa göreli zaman: "şimdi", "3 dk", "2 sa", "dün", "4 gün", "12 Eki" */
export function relTime(at: number, now: number): string {
  if (!at) return '';
  const d = Math.max(0, now - at);
  if (d < 60_000) return 'şimdi';
  if (d < HOUR) return `${Math.floor(d / 60_000)} dk`;
  if (d < DAY) return `${Math.floor(d / HOUR)} sa`;
  if (d < 2 * DAY) return 'dün';
  if (d < 7 * DAY) return `${Math.floor(d / DAY)} gün`;
  return new Date(at).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
}

export const fullTime = (at: number) =>
  at ? new Date(at).toLocaleString('tr-TR', { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' }) : '';

/** Belirli pencerede havuz etkinliği (bant için) */
export function activityIn(sums: PoolSummary[], windowMs: number, now: number) {
  const from = now - windowMs;
  let newQ = 0;
  let parts = 0;
  const people = new Set<string>();
  for (const s of sums) {
    if (s.firstAt >= from) newQ++;
    for (const e of s.events) {
      if (e.at < from) break; // olaylar yeniden eskiye sıralı
      if (e.kind !== 'comment' && e.kind !== 'revision') parts++;
      people.add(e.uid || e.who.toLocaleLowerCase('tr-TR'));
    }
  }
  return { newQ, parts, people: people.size };
}
