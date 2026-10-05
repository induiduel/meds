import React from 'react';
import { safeJsonFetch } from '../../services/api';

export type SearchDocType =
  | 'past_question' | 'active_question' | 'lecture_slide' | 'summary' | 'transcript'
  | 'user_contribution' | 'ai_refinement' | 'ai_qa' | 'deepseek_contribution'
  | 'gemini_v3_question' | 'gemini_v3_lecture' | 'gemini_v3_term';

export interface SearchHit {
  id: string;
  documentId: string;
  documentType: SearchDocType;
  committeeId?: string;
  discipline?: string;
  title: string;
  pageNumber?: number;
  snippet: string;
  content: string;
  score: number;
}

export interface SearchResponse {
  query: string;
  total: number;
  capped: boolean;
  byType: Partial<Record<SearchDocType, number>>;
  results: SearchHit[];
}

export const TYPE_META: Record<SearchDocType, { label: string; dot: string }> = {
  past_question: { label: 'Çıkmış soru', dot: 'bg-violet-500' },
  deepseek_contribution: { label: 'Soru bankası', dot: 'bg-indigo-500' },
  active_question: { label: 'Havuz sorusu', dot: 'bg-blue-500' },
  lecture_slide: { label: 'Ders slaytı', dot: 'bg-emerald-500' },
  summary: { label: 'Özet', dot: 'bg-teal-500' },
  transcript: { label: 'Ses kaydı', dot: 'bg-amber-500' },
  user_contribution: { label: 'Katkı', dot: 'bg-sky-500' },
  ai_refinement: { label: 'AI düzeltme', dot: 'bg-slate-400' },
  ai_qa: { label: 'AI yanıtı', dot: 'bg-slate-400' },
  gemini_v3_question: { label: 'Gemini v3 soru', dot: 'bg-fuchsia-500' },
  gemini_v3_lecture: { label: 'Gemini v3 ders notu', dot: 'bg-fuchsia-500' },
  gemini_v3_term: { label: 'Gemini v3 terim', dot: 'bg-fuchsia-500' },
};

export const TYPE_ORDER: SearchDocType[] = [
  'past_question', 'deepseek_contribution', 'lecture_slide', 'summary', 'transcript',
  'active_question', 'user_contribution', 'gemini_v3_question', 'gemini_v3_lecture', 'gemini_v3_term',
];

export async function fetchSearch(
  q: string,
  opts: { types?: SearchDocType[]; offset?: number; limit?: number; committeeId?: string } = {},
  signal?: AbortSignal
): Promise<SearchResponse | null> {
  const params = new URLSearchParams({ q, offset: String(opts.offset || 0), limit: String(opts.limit || 5) });
  if (opts.types?.length) params.set('types', opts.types.join(','));
  if (opts.committeeId) params.set('committeeId', opts.committeeId);
  const res = await safeJsonFetch<SearchResponse & { success: boolean }>(`/api/search/all?${params}`, { signal });
  if (!res.ok || !res.data?.success) return null;
  const includeV3 = !opts.types?.length || opts.types.some((type) => type.startsWith('gemini_v3_'));
  if (!includeV3 || !q.trim()) return res.data;
  const v3Params = new URLSearchParams({ q, limit: String(Math.max(opts.limit || 5, 20)) });
  if (opts.committeeId) v3Params.set('committeeId', opts.committeeId);
  const [questions, lectures, terms] = await Promise.all([
    safeJsonFetch<any>(`/api/gemini-v3/questions?${v3Params}`, { signal }),
    safeJsonFetch<any>(`/api/gemini-v3/lecture-notes?${v3Params}`, { signal }),
    safeJsonFetch<any>(`/api/gemini-v3/thesaurus?q=${encodeURIComponent(q)}`, { signal }),
  ]);
  const v3Hits: SearchHit[] = [];
  if (questions.ok && questions.data?.items) for (const item of questions.data.items) v3Hits.push({
    id: `gemini-v3-question-${item.question_id}`, documentId: item.question_id, documentType: 'gemini_v3_question',
    committeeId: item.kurul ? `kurul-${item.kurul}` : undefined, discipline: item.ders,
    title: item.stem || 'Gemini v3 sorusu', snippet: item.konu || item.taxonomy_metadata?.ne_sormus || '',
    content: [item.stem, ...Object.values(item.options || {})].join(' '), score: item.medical_accuracy_score || 0,
  });
  if (lectures.ok && lectures.data?.items) for (const item of lectures.data.items) v3Hits.push({
    id: `gemini-v3-lecture-${item.source_id}`, documentId: item.source_id, documentType: 'gemini_v3_lecture',
    committeeId: item.kurul ? `kurul-${item.kurul}` : undefined, discipline: item.ders,
    title: item.title || 'Gemini v3 ders notu', snippet: `${item.pages || 0} sayfa · kaynaklı yeniden yapılandırılmış not`,
    content: item.title || '', score: 0,
  });
  if (terms.ok && terms.data?.items) for (const item of terms.data.items) v3Hits.push({
    id: `gemini-v3-term-${item.key}`, documentId: item.key, documentType: 'gemini_v3_term',
    title: item.turkce || item.key, snippet: item.latin || item.anahtar_bilesenler?.join(', ') || 'Tıbbi terim',
    content: JSON.stringify(item), score: 0,
  });
  const filteredV3 = opts.types?.length ? v3Hits.filter((hit) => opts.types!.includes(hit.documentType)) : v3Hits;
  const merged = [...res.data.results, ...filteredV3].slice(0, opts.offset ? (opts.offset + (opts.limit || 5)) : (opts.limit || 5));
  return { ...res.data, total: res.data.total + filteredV3.length, capped: res.data.capped, results: merged,
    byType: { ...res.data.byType, ...Object.fromEntries(filteredV3.reduce((map, hit) => map.set(hit.documentType, (map.get(hit.documentType) || 0) + 1), new Map<SearchDocType, number>())) } };
}

/* Türkçe duyarlı vurgulama: aranan sözcüklerin ilk 5 harfi (kök) eşleşir */
const fold = (s: string) =>
  s.replace(/İ/g, 'i').replace(/I/g, 'ı').toLocaleLowerCase('tr')
    .replace(/[âà]/g, 'a').replace(/[îı]/g, 'i').replace(/[ûü]/g, 'u').replace(/ö/g, 'o').replace(/ç/g, 'c').replace(/ş/g, 's').replace(/ğ/g, 'g');

export const Highlight: React.FC<{ text: string; query: string }> = ({ text, query }) => {
  const stems = Array.from(new Set(fold(query).split(/[^a-z0-9]+/).filter((w) => w.length >= 3).map((w) => w.slice(0, w.length >= 8 ? 7 : 5))));
  if (stems.length === 0) return <>{text}</>;
  const folded = fold(text);
  // fold() harf sayısını korur; konumlar doğrudan asıl metne uygulanır
  const marks: Array<[number, number]> = [];
  const wordRe = /[\p{L}\p{N}]+/gu;
  let m: RegExpExecArray | null;
  while ((m = wordRe.exec(folded))) {
    if (stems.some((st) => m![0].startsWith(st))) marks.push([m.index, m.index + m[0].length]);
  }
  if (marks.length === 0 || folded.length !== text.length) return <>{text}</>;
  const out: React.ReactNode[] = [];
  let last = 0;
  marks.forEach(([a, b], i) => {
    if (a > last) out.push(text.slice(last, a));
    out.push(<mark key={i} className="ms-hl">{text.slice(a, b)}</mark>);
    last = b;
  });
  out.push(text.slice(last));
  return <>{out}</>;
};

export const TypeTag: React.FC<{ type: SearchDocType }> = ({ type }) => {
  const meta = TYPE_META[type] || { label: type, dot: 'bg-slate-400' };
  return (
    <span className="inline-flex items-center gap-1.5 text-[12px] text-ink-3 whitespace-nowrap">
      <span className={`w-1.5 h-1.5 rounded-full ${meta.dot}`} aria-hidden="true" />
      {meta.label}
    </span>
  );
};
