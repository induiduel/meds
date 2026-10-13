/**
 * PDF Stüdyosu düzen motoru: soruları iki kademeli gruplar (ör. Ders › Konu, Konu › Kazanım) ve grup içinde
 * sıralar. Çıktı düz bir listedir; her ögenin grup yolu (path) vardır, belge başlıkları yol değiştiğinde basılır.
 */
import type { PdfQuestion } from './pdfSources';
import { COMMITTEE_NAME } from './pdfSources';
import { matchKazanim, type DeckKazanim, type LessonStep } from '../learn/lesson/lessonModel';

export type GroupBy = 'none' | 'committee' | 'discipline' | 'topic' | 'kazanim' | 'year' | 'difficulty' | 'group';
export type GroupOrder = 'natural' | 'alpha' | 'count';
export type SortBy = 'source' | 'year' | 'number' | 'difficulty' | 'discipline' | 'topic' | 'random';
export type SortDir = 'asc' | 'desc';

export interface ArrangeOptions {
  group1: GroupBy;
  group2: GroupBy;
  groupOrder: GroupOrder;
  sortBy: SortBy;
  sortDir: SortDir;
  /** Karıştırma tohumu: aynı tohum aynı sırayı verir */
  seed: number;
}

export interface GroupStep { key: string; label: string }
export interface ArrangedItem { q: PdfQuestion; idx: number; path: GroupStep[] }

export const GROUP_LABEL: Record<GroupBy, string> = {
  none: 'Yok',
  committee: 'Kurul',
  discipline: 'Ders',
  topic: 'Konu',
  kazanim: 'Kazanım',
  year: 'Yıl',
  difficulty: 'Zorluk',
  group: 'Adım',
};

export const SORT_LABEL: Record<SortBy, string> = {
  source: 'Kaynak sırası',
  year: 'Yıl',
  number: 'Soru no',
  difficulty: 'Zorluk',
  discipline: 'Ders',
  topic: 'Konu',
  random: 'Karışık',
};

const DIFF_RANK: Record<string, number> = { kolay: 0, orta: 1, zor: 2 };
const DIFF_NAME: Record<string, string> = { kolay: 'Kolay', orta: 'Orta', zor: 'Zor' };
const COMMITTEE_IDS = Object.keys(COMMITTEE_NAME);
const cmp = (a: string, b: string) => a.localeCompare(b, 'tr', { numeric: true, sensitivity: 'base' });
const yearKey = (y?: string) => (y && /\d{4}/.test(y) ? y : '');

interface Key { key: string; label: string; rank: string; unknown: boolean }

/** Bir sorunun verilen ölçüte göre grup anahtarı; rank "doğal" sıralamada kullanılır. */
export function groupKeyOf(q: PdfQuestion, by: GroupBy): Key {
  switch (by) {
    case 'committee': {
      const i = q.committeeId ? COMMITTEE_IDS.indexOf(q.committeeId) : -1;
      return q.committeeId
        ? { key: q.committeeId, label: COMMITTEE_NAME[q.committeeId] || q.committeeId, rank: String(i < 0 ? 99 : i).padStart(3, '0'), unknown: false }
        : { key: '?', label: 'Kurulu belirsiz', rank: '', unknown: true };
    }
    case 'discipline':
      return q.discipline ? { key: q.discipline, label: q.discipline, rank: q.discipline, unknown: false } : { key: '?', label: 'Dersi belirsiz', rank: '', unknown: true };
    case 'topic': {
      if (!q.topic) return { key: '?', label: 'Konusu belirsiz', rank: '', unknown: true };
      // Müfredat kimliğinin konu kısmı (k3-d5-c7) varsa program sırası korunur
      const prefix = q.kazanim?.id?.replace(/-kz-\d+$/, '') || '';
      return { key: q.topic, label: q.topic, rank: prefix ? `0 ${prefix}` : `1 ${q.topic}`, unknown: false };
    }
    case 'kazanim':
      return q.kazanim?.text
        ? { key: q.kazanim.id || q.kazanim.text, label: q.kazanim.text, rank: q.kazanim.id ? `0 ${q.kazanim.id}` : `1 ${q.kazanim.text}`, unknown: false }
        : { key: '?', label: 'Kazanımı belirsiz', rank: '', unknown: true };
    case 'year': {
      const y = yearKey(q.year);
      return y ? { key: q.year!, label: q.year!, rank: q.year!, unknown: false } : { key: '?', label: 'Yılı belirsiz', rank: '', unknown: true };
    }
    case 'difficulty':
      return q.difficulty
        ? { key: q.difficulty, label: DIFF_NAME[q.difficulty], rank: String(DIFF_RANK[q.difficulty]), unknown: false }
        : { key: '?', label: 'Zorluğu belirsiz', rank: '', unknown: true };
    case 'group': {
      const label = q.group || q.topic || '';
      if (!label) return { key: '?', label: 'Diğer', rank: '', unknown: true };
      const n = label.match(/^(?:Adım|Kazanım)\s+(\d+)/)?.[1];
      return { key: label, label, rank: n ? n.padStart(5, '0') : label, unknown: false };
    }
    default:
      return { key: '', label: '', rank: '', unknown: false };
  }
}

/** Basit, tohumlu karıştırma anahtarı (FNV-1a). */
const hash = (s: string, seed: number) => {
  let h = 2166136261 ^ seed;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
};

const itemCompare = (o: ArrangeOptions) => {
  const dir = o.sortDir === 'desc' ? -1 : 1;
  return (a: ArrangedItem, b: ArrangedItem): number => {
    let r = 0;
    switch (o.sortBy) {
      case 'year':
        // Yılı olmayan sorular yönden bağımsız sona düşer
        if (!yearKey(a.q.year) !== !yearKey(b.q.year)) return yearKey(a.q.year) ? -1 : 1;
        r = cmp(yearKey(a.q.year), yearKey(b.q.year)) || (a.q.number || 0) - (b.q.number || 0);
        break;
      case 'number':
        r = (a.q.number || 0) - (b.q.number || 0);
        break;
      case 'difficulty':
        r = (DIFF_RANK[a.q.difficulty || ''] ?? 9) - (DIFF_RANK[b.q.difficulty || ''] ?? 9);
        break;
      case 'discipline':
        r = cmp(a.q.discipline, b.q.discipline);
        break;
      case 'topic':
        r = cmp(a.q.topic || '￿', b.q.topic || '￿');
        break;
      case 'random':
        return hash(a.q.id, o.seed) - hash(b.q.id, o.seed) || a.idx - b.idx;
      default:
        r = 0;
    }
    return r * dir || (o.sortBy === 'source' ? (a.idx - b.idx) * dir : a.idx - b.idx);
  };
};

const orderGroups = (keys: Map<string, { k: Key; n: number }>, by: GroupBy, order: GroupOrder): string[] =>
  [...keys.entries()]
    .sort(([, a], [, b]) => {
      if (a.k.unknown !== b.k.unknown) return a.k.unknown ? 1 : -1;
      if (order === 'count') return b.n - a.n || cmp(a.k.label, b.k.label);
      if (order === 'alpha') return cmp(a.k.label, b.k.label);
      // Doğal: yıl yeniden eskiye, diğerleri müfredat/program sırası
      return by === 'year' ? cmp(b.k.rank, a.k.rank) : cmp(a.k.rank, b.k.rank) || cmp(a.k.label, b.k.label);
    })
    .map(([key]) => key);

/** Soruları gruplayıp sıralar; sonuç düz listedir (ilk N kesimi grup sırasını korur). */
export function arrangeQuestions(questions: PdfQuestion[], o: ArrangeOptions): ArrangedItem[] {
  const items: ArrangedItem[] = questions.map((q, idx) => ({ q, idx, path: [] }));
  const levels = [o.group1, o.group2].filter((g, i, arr) => g !== 'none' && arr.indexOf(g) === i) as GroupBy[];
  const sortItems = (list: ArrangedItem[]) => [...list].sort(itemCompare(o));

  const build = (list: ArrangedItem[], depth: number, path: GroupStep[]): ArrangedItem[] => {
    if (depth >= levels.length) return sortItems(list).map((it) => ({ ...it, path }));
    const by = levels[depth];
    const buckets = new Map<string, { k: Key; n: number; items: ArrangedItem[] }>();
    list.forEach((it) => {
      const k = groupKeyOf(it.q, by);
      const b = buckets.get(k.key);
      if (b) {
        b.n++;
        b.items.push(it);
      } else buckets.set(k.key, { k, n: 1, items: [it] });
    });
    return orderGroups(buckets, by, o.groupOrder).flatMap((key) => {
      const b = buckets.get(key)!;
      return build(b.items, depth + 1, [...path, { key: `${by}:${key}`, label: b.k.label }]);
    });
  };
  return build(items, 0, []);
}

/** Mini sorulara deste kazanım dizininden (byDeck.json) adım eşleşmesiyle kazanım bağlar. */
export function attachDeckKazanim(questions: PdfQuestion[], deckId: string, deckTitle: string, steps: LessonStep[], index: Record<string, DeckKazanim[]> | null): PdfQuestion[] {
  const list = index?.[deckId];
  if (!list?.length) return questions;
  const cache = new Map<number, DeckKazanim | undefined>();
  const order = new Map(list.map((k, i) => [k.m, i]));
  return questions.map((q) => {
    const slideNo = Number(q.id.split(':').slice(-2, -1)[0]);
    if (!Number.isFinite(slideNo)) return q;
    if (!cache.has(slideNo)) {
      const step = steps.find((s) => s.number === slideNo);
      cache.set(slideNo, step ? matchKazanim(step, list, undefined, deckTitle)[0] : undefined);
    }
    const k = cache.get(slideNo);
    return k ? { ...q, kazanim: { id: `${deckId}-kz-${String(order.get(k.m) ?? 999).padStart(3, '0')}`, text: k.m } } : q;
  });
}

/** Belgede bağlantı hedefi olacak güvenli kimlik (aynı kimlik ikinci kez gelirse sıra eklenir). */
export function makeAnchorer() {
  const used = new Map<string, number>();
  return (raw: string) => {
    const base = raw.replace(/[^A-Za-z0-9_-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80) || 'x';
    const n = used.get(base) || 0;
    used.set(base, n + 1);
    return n ? `${base}-${n + 1}` : base;
  };
}
