/**
 * Study workspace data: a normalized question bank (archive + reconstructed pool)
 * plus per-device progress, review list, self-test history and personal notes.
 * Everything personal lives in localStorage and every access is guarded, so the
 * pages still render when storage is blocked (private mode, cleared site data).
 */
import { QuestionItem } from '../types';
import { ApiService } from './api';

export type OptionKey = 'A' | 'B' | 'C' | 'D' | 'E';

export interface StudyQuestion {
  id: string;
  source: 'arşiv' | 'havuz';
  committeeId: string;
  year: string;
  number: number;
  discipline: string;
  topic: string;
  stem: string;
  options: { key: OptionKey; text: string }[];
  answer: OptionKey;
  explanation: string;
}

export interface AttemptRecord {
  picked: OptionKey;
  correct: boolean;
  at: string;
}

export interface SelfTestResult {
  id: string;
  at: string;
  title: string;
  durationSec: number;
  total: number;
  correct: number;
  wrong: number;
  blank: number;
  byDiscipline: Record<string, { total: number; correct: number }>;
  questionIds: string[];
  answers: Record<string, OptionKey | undefined>;
}

export interface StudyNote {
  id: string;
  title: string;
  body: string;
  discipline: string;
  questionId?: string;
  questionStem?: string;
  pinned?: boolean;
  createdAt: string;
  updatedAt: string;
}

const KEYS = {
  progress: 'medsoru_study_progress_v1',
  review: 'medsoru_study_review_v1',
  tests: 'medsoru_selftest_history_v1',
  notes: 'medsoru_notes_v1',
};

const read = <T,>(key: string, fallback: T): T => {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
};

const write = (key: string, value: unknown) => {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* storage unavailable: keep working in memory */
  }
};

// ---------------- Question bank ----------------

const VALID: OptionKey[] = ['A', 'B', 'C', 'D', 'E'];

const normalizeArchive = (q: any): StudyQuestion | null => {
  const rec = q?.reconstruction;
  const rawOpts = rec?.options || q?.options || q?.rawQuestion?.options || [];
  const opts = rawOpts
    .filter((o: any) => o && VALID.includes(String(o.key || '').trim().toUpperCase() as OptionKey) && String(o.text || '').trim())
    .map((o: any) => ({ key: String(o.key || '').trim().toUpperCase() as OptionKey, text: String(o.text).trim() }));
  const answer = (
    rec?.correctAnswer ||
    q?.correctAnswer ||
    rec?.options?.find((o: any) => o.isCorrect)?.key ||
    q?.options?.find((o: any) => o.isCorrect)?.key ||
    q?.claimedAnswer ||
    q?.rawQuestion?.claimedAnswer
  ) as OptionKey;
  const stem = String(rec?.stem || q?.stem || q?.rawQuestion?.stem || '').trim();
  if (!stem || opts.length < 2 || !VALID.includes(answer) || !opts.some((o: any) => o.key === answer)) return null;
  return {
    id: String(q.id),
    source: 'arşiv',
    committeeId: q.committeeId || '',
    year: q.examYear || '',
    number: Number(q.questionNumber) || 0,
    discipline: q.discipline || 'Genel',
    topic: q.topic || '',
    stem,
    options: opts,
    answer,
    explanation: String(rec?.explanation || q?.explanation || '').trim(),
  };
};

const normalizePool = (q: QuestionItem): StudyQuestion | null => {
  const rec = q.reconstruction;
  const stem = String(rec?.stem || (q as any).stem || (q.fragments && q.fragments.length > 0 ? q.fragments.map((f: any) => f.text).join(' ') : '')).trim();
  const rawOpts = rec?.options && rec.options.length >= 2 ? rec.options : q.options || [];
  const opts = rawOpts
    .filter((o: any) => o && VALID.includes(String(o.key || '').trim().toUpperCase() as OptionKey) && String(o.text || '').trim())
    .map((o: any) => ({ key: String(o.key || '').trim().toUpperCase() as OptionKey, text: String(o.text).trim() }));
  const answer = (
    rec?.correctAnswer ||
    q.claimedAnswer ||
    rec?.options?.find((o: any) => o.isCorrect)?.key ||
    q.options?.find((o: any) => o.isCorrect)?.key
  ) as OptionKey;
  if (!stem || opts.length < 2 || !VALID.includes(answer) || !opts.some((o) => o.key === answer)) return null;
  return {
    id: q.id,
    source: 'havuz',
    committeeId: q.committeeId,
    year: q.examYear || '',
    number: q.questionNumber,
    discipline: q.discipline || 'Genel',
    topic: q.topic || '',
    stem,
    options: opts,
    answer,
    explanation: rec?.explanation || '',
  };
};

let archiveCache: StudyQuestion[] | null = null;
let archivePromise: Promise<StudyQuestion[]> | null = null;

export const loadArchiveBank = (): Promise<StudyQuestion[]> => {
  if (archiveCache) return Promise.resolve(archiveCache);
  if (!archivePromise) {
    archivePromise = ApiService.getPastQuestions()
      .then((list) => {
        const seen = new Set<string>();
        archiveCache = (list || [])
          .map(normalizeArchive)
          .filter((q): q is StudyQuestion => !!q && !seen.has(q.id) && !!seen.add(q.id));
        return archiveCache;
      })
      .catch(() => {
        archivePromise = null;
        return [];
      });
  }
  return archivePromise;
};

export const buildBank = (archive: StudyQuestion[], pool: QuestionItem[]): StudyQuestion[] => {
  const poolQs = pool.map(normalizePool).filter((q): q is StudyQuestion => !!q);
  const ids = new Set(poolQs.map((q) => q.id));
  return [...poolQs, ...archive.filter((q) => !ids.has(q.id))];
};

export const shuffle = <T,>(arr: T[]): T[] => {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};

// ---------------- Progress & review ----------------

export const getProgress = () => read<Record<string, AttemptRecord>>(KEYS.progress, {});
export const recordAttempt = (id: string, picked: OptionKey, correct: boolean) => {
  const all = getProgress();
  all[id] = { picked, correct, at: new Date().toISOString() };
  write(KEYS.progress, all);
  // Wrong answers go straight to the review list
  if (!correct) setInReview(id, true);
  return all;
};
export const resetProgress = (ids?: string[]) => {
  if (!ids) return write(KEYS.progress, {});
  const all = getProgress();
  ids.forEach((id) => delete all[id]);
  write(KEYS.progress, all);
};

export const getReview = () => new Set(read<string[]>(KEYS.review, []));
export const setInReview = (id: string, on: boolean) => {
  const s = getReview();
  if (on) s.add(id);
  else s.delete(id);
  write(KEYS.review, [...s]);
  return s;
};

// ---------------- Self-test history ----------------

export const getTestHistory = () => read<SelfTestResult[]>(KEYS.tests, []);
export const saveTestResult = (r: SelfTestResult) => {
  const all = [r, ...getTestHistory()].slice(0, 30);
  write(KEYS.tests, all);
  return all;
};
export const clearTestHistory = () => write(KEYS.tests, []);

// ---------------- Notes ----------------

export const getNotes = () => read<StudyNote[]>(KEYS.notes, []);
export const saveNotes = (notes: StudyNote[]) => write(KEYS.notes, notes);
export const newNoteId = () => `note-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`;

/** Exports notes as a Markdown file the viewer can keep. */
export const notesToMarkdown = (notes: StudyNote[]) =>
  notes
    .map((n) => {
      const meta = [n.discipline, n.questionStem ? `Soru: ${n.questionStem.slice(0, 120)}` : ''].filter(Boolean).join(' · ');
      return `## ${n.title || 'Başlıksız not'}\n${meta ? `_${meta}_\n` : ''}\n${n.body}\n`;
    })
    .join('\n---\n\n');
