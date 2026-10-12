// RAG: retrieve course material (slides, summaries, transcripts, past exam questions)
// and ground AI answers on it. Server-only.
//
// Retrieval order: local BM25 index (localRagEngine) -> Supabase pgvector (only if local
// finds nothing). AI-generated chunks are excluded so model output never becomes a "source".
import { semanticSearch, fuseRRF } from './vectorSearch';
import { GoogleGenAI } from '@google/genai';
import { pgDb } from './pgDb';
import { searchLocalRag, foldTurkish, findChunksById, findCardsByName, cardNameKey, type RagDocumentType } from './localRagEngine.ts';
import { generateResilientMedicalAi, getTieredGeminiKeys } from './aiProvider.ts';
import { getCachedLectureNotes } from '../serverLectureNotes.ts';

/** Human-authored material that may be used as evidence. */
export const GROUNDING_DOC_TYPES: RagDocumentType[] = ['past_question', 'lecture_slide', 'summary', 'transcript', 'ornek_question', 'deck_slide', 'glossary_term', 'disease'];
/** Course material only (no exam questions). */
export const MATERIAL_DOC_TYPES: RagDocumentType[] = ['lecture_slide', 'summary', 'transcript', 'deck_slide', 'glossary_term', 'disease'];

export interface RagChunkResult {
  id: string;
  documentId: string;
  documentType: RagDocumentType;
  committeeId?: string;
  discipline?: string;
  title: string;
  pageNumber?: number;
  content: string;
  metadata?: any;
  similarity: number;
  combinedScore?: number;
}

export interface RagAskOptions {
  query: string;
  committeeId?: string;
  discipline?: string;
  mode?: 'qa' | 'chat' | 'redact' | 'reduction' | 'verify';
  targetQuestion?: any;
  limit?: number;
}

export interface RagAskResponse {
  answer: string;
  mode: string;
  references: RagChunkResult[];
  usedModel: string;
  sourcesCount: number;
}

const DOC_TYPE_LABELS: Record<string, string> = {
  past_question: 'Çıkmış Sınav Sorusu',
  lecture_slide: 'Ders Slaytı',
  summary: 'Ders Özeti',
  transcript: 'Amfi Ses Transkripti',
};

/** Generate a 768-dim embedding (used only for the Supabase pgvector path). */
export async function generateEmbedding(text: string, apiKey: string): Promise<number[]> {
  const client = new GoogleGenAI({ apiKey });
  const res = await client.models.embedContent({
    model: 'gemini-embedding-001',
    contents: [text],
    config: { outputDimensionality: 768 },
  });
  const values = res.embeddings?.[0]?.values;
  if (!values) throw new Error('Embedding üretilemedi.');
  return values;
}

// The same deck is often uploaded several times under slightly different titles, so
// chunk headers differ. Compare the tail of the body and the title+page instead.
function dedupeKeys(r: { content: string; title: string; pageNumber?: number }): string[] {
  const norm = (t: string) => t.toLocaleLowerCase('tr').replace(/[^a-z0-9çğıöşü]+/g, '');
  return [`body:${norm(r.content).slice(-300)}`, `page:${norm(r.title)}#${r.pageNumber ?? ''}`];
}

// Many "lecture notes" are actually uploaded exam dumps (question PDFs). They are not course
// material: citing them as a "slide" would just echo questions back. A note counts as an exam dump
// when most of its pages look like exam questions.
export function isExamLikePage(content: string): boolean {
  if (/Sıra\s*No\s*Cevap|Cevabınız/i.test(content)) return true;
  const q = (content.match(/hangisi(dir)?|hangileri|aşağıdakilerden|nedir\s*\?|\?\s*$/gim) || []).length;
  const opts = (content.match(/(^|\s)[a-eA-E]\s*[).]\s+\S/gm) || []).length;
  const ans = (content.match(/cevap\s*[:=]|doğru cevap/gi) || []).length;
  const numberedQuestions = (content.match(/(^|\s)\d{1,3}\s*[-.)]\s*[^?]{5,120}\?/g) || []).length; // "12- Kibas bulguları?"
  return (q >= 2 && opts >= 4) || q >= 3 || ans >= 2 || numberedQuestions >= 2;
}

let examDumpCache: { source: unknown; ids: Set<string> } | null = null;
export function getExamDumpNoteIds(): Set<string> {
  const notes = getCachedLectureNotes();
  if (examDumpCache && examDumpCache.source === notes) return examDumpCache.ids;
  const ids = new Set<string>();
  for (const note of notes) {
    // Ignore OCR debris pages ("- - -"): only pages with real text count toward the ratio.
    const pages = (note.pages || []).filter((p: any) => (p.content?.match(/[a-zA-ZçğıöşüÇĞİÖŞÜ]/g) || []).length >= 40);
    if (pages.length === 0) continue;
    const examPages = pages.filter((p: any) => isExamLikePage(p.content)).length;
    if (examPages / pages.length >= 0.5) ids.add(note.id);
  }
  examDumpCache = { source: notes, ids };
  return ids;
}

async function searchCloud(
  query: string,
  apiKey: string,
  options: { committeeId?: string; discipline?: string; documentType?: string; limit: number }
): Promise<RagChunkResult[]> {
  if (!apiKey) return [];
  const run = async (): Promise<RagChunkResult[]> => {
    const embedding = await generateEmbedding(query, apiKey);
    const { data, error } = await pgDb.rpc('hybrid_match_rag_chunks', {
      query_text: query,
      query_embedding: embedding,
      match_count: options.limit,
      filter_committee: options.committeeId || null,
      filter_discipline: options.discipline || null,
      filter_doc_type: options.documentType || null,
    });
    if (error || !Array.isArray(data)) return [];
    return data
      .filter((item: any) => GROUNDING_DOC_TYPES.includes(item.document_type))
      .map((item: any) => ({
        id: item.id,
        documentId: item.document_id,
        documentType: item.document_type,
        committeeId: item.committee_id,
        discipline: item.discipline,
        title: item.title,
        pageNumber: item.page_number,
        content: item.content,
        metadata: item.metadata,
        similarity: item.similarity,
        combinedScore: item.combined_score,
      }));
  };
  const timeout = new Promise<RagChunkResult[]>((resolve) => setTimeout(() => resolve([]), 1500));
  try {
    return await Promise.race([run(), timeout]);
  } catch {
    return [];
  }
}

/**
 * Find the most relevant human-authored chunks for a query.
 * `documentType` narrows to a single type; otherwise all GROUNDING_DOC_TYPES are searched.
 */

/** Başlıksız ortak chunk ("8 (Sayfa 49)", "Sayfa 12" vb.) tespiti — gösterim cezası için. */
function isGenericTitle(t: unknown): boolean {
  if (typeof t !== 'string') return true;
  const s = t.trim();
  return s.length === 0 || /^\d+\s*\(sayfa[^)]*\)$/i.test(s) || /^sayfa\s*\d+$/i.test(s) || /^\d+$/.test(s);
}

export async function searchRagChunks(
  query: string,
  apiKey?: string,
  options: {
    committeeId?: string;
    discipline?: string;
    documentType?: string;
    documentTypes?: RagDocumentType[];
    limit?: number;
  } = {}
): Promise<RagChunkResult[]> {
  const limit = options.limit || 5;
  const documentTypes = options.documentType
    ? [options.documentType as RagDocumentType]
    : (options.documentTypes || GROUNDING_DOC_TYPES).filter((t) => GROUNDING_DOC_TYPES.includes(t));

  let results: RagChunkResult[] = [];
  try {
    // Over-fetch so de-duplication and exam-dump filtering still leave `limit` results.
    const local = await searchLocalRag(query, {
      committeeId: options.committeeId,
      discipline: options.discipline,
      documentTypes,
      limit: limit * 8,
    });
    // Karma arama: BM25 + anlamsal (yerel vektör servisi + Supabase rpc) RRF birleşimi; vektör servisi yoksa yalnız BM25
    const vec = await semanticSearch(query, { documentTypes, committeeId: options.committeeId, limit: limit * 8 });
    let fused = vec.length
      ? fuseRRF(local as any[], vec, (r: any) => ({
          id: r.id, documentId: r.document_id, documentType: r.document_type, committeeId: r.committee_id,
          discipline: r.discipline, title: r.title, pageNumber: r.page_number, content: r.content, metadata: r.metadata,
          similarity: r.similarity, matchScore: r.similarity,
        }) as any, limit * 8)
      : local;
    // Başlıksız ("Sayfa N" gibi) ortak chunk cezası: RRF sırası korunur, yalnızca
    // en az 3 başlıklı alternatif varsa başlıksızlar alta taşınır (içerik gizlenmez).
    if (vec.length && Array.isArray(fused)) {
      const good: any[] = [];
      const bad: any[] = [];
      for (const it of fused as any[]) (isGenericTitle(it?.title) ? bad : good).push(it);
      if (good.length >= 3) fused = [...good, ...bad] as any;
    }
    results = (fused as typeof local).map((item) => ({
      id: item.id,
      documentId: item.documentId,
      documentType: item.documentType,
      committeeId: item.committeeId,
      discipline: item.discipline,
      title: item.title,
      pageNumber: item.pageNumber,
      content: item.content,
      metadata: item.metadata,
      similarity: item.similarity,
      combinedScore: item.matchScore,
    }));
  } catch (err: any) {
    console.warn('[RagService] Yerel RAG arama uyarısı:', err.message);
  }

  if (results.length === 0) {
    const key = apiKey || getTieredGeminiKeys()[0]?.key || '';
    results = await searchCloud(query, key, { ...options, limit: limit * 2 });
  }

  const examDumps = getExamDumpNoteIds();
  const seen = new Set<string>();
  const unique: RagChunkResult[] = [];
  for (const r of results) {
    if (r.documentType === 'lecture_slide' && examDumps.has(r.documentId)) continue;
    const keys = dedupeKeys(r);
    // Aynı adlı sözlük kartları ("sifiliz" ve "Sifiliz (Frengi)") tek sonuçta toplanır
    if (r.documentType === 'glossary_term') keys.push(`gl:${cardNameKey(r.title.replace(/^Sözlük:\s*/, '').replace(/\([^)]*\)/g, ' '))}`);
    if (keys.some((k) => seen.has(k))) continue;
    keys.forEach((k) => seen.add(k));
    unique.push(r);
    if (unique.length >= limit) break;
  }
  return unique;
}

/** Render retrieved chunks as numbered sources for a prompt. */
export function formatSourcesForPrompt(sources: RagChunkResult[], maxCharsPerSource = 900): string {
  if (sources.length === 0) {
    return 'Ders materyallerinde ilgili kaynak bulunamadı. Genel tıp bilgisine dayan ve bunu notlarda açıkça belirt.';
  }
  return sources
    .map((ref, idx) => {
      const label = DOC_TYPE_LABELS[ref.documentType] || ref.documentType;
      const page = ref.pageNumber ? ` (s. ${ref.pageNumber})` : '';
      const body = ref.content.length > maxCharsPerSource ? ref.content.slice(0, maxCharsPerSource) + '…' : ref.content;
      return `--- [KAYNAK ${idx + 1}: ${label} | ${ref.discipline || 'Tıp'} - ${ref.title}${page}] ---\n${body.trim()}`;
    })
    .join('\n\n');
}

/** Compact source descriptor returned to the client for display. */
export function toSourceRef(ref: RagChunkResult) {
  return {
    documentId: ref.documentId,
    documentType: ref.documentType,
    title: ref.title,
    discipline: ref.discipline,
    pageNumber: ref.pageNumber,
    snippet: ref.content.replace(/\s+/g, ' ').slice(0, 220),
  };
}

// Response cache for /api/rag/ask (30 min, max 150 entries)
const ragResponseCache = new Map<string, { response: RagAskResponse; expiresAt: number }>();

/**
 * Build tailored system prompts for each medical mode
 */
function buildSystemPrompt(mode: string): string {
  switch (mode) {
    case 'redact':
      return `Sen Tıp Fakültesi Soru Redaksiyon ve Doğrulama Uzmanısın.
Görevin: Öğrencilerin sınavdan eksik/hatalı hatırladığı soruları, sana verilen resmi fakülte amfi ders slaytları ve geçmiş kurul çıkmış soruları referansıyla profesyonel, eksiksiz ve hatasız bir tıp sorusu haline getirmektir (Redaksiyon).
Kurallar:
1. Kesinlikle tıbbi amfi ders notuna ve referanslara sadık kal, hayal ürünü (halüsinasyon) tıbbi bilgi ekleme.
2. Soru kökünü berrak ve net kıl (örn: "Aşağıdakilerden hangisi...").
3. 5 seçenek oluştur (A, B, C, D, E) ve her şıkkın tıbbi açıdan mantıklı bir çeldirici veya doğru cevap olmasını sağla.
4. Doğru seçeneği açıkça belirt ve amfi ders notunun hangi slaytına veya konusuna dayandığını açıkla.
5. Diğer şıkların neden yanlış olduğunu 1-2 cümlelik hap bilgiyle gerekçelendir.`;

    case 'reduction':
      return `Sen Tıp Fakültesi Redüksiyon (Özetleme & Sentezleme) Uzmanısın.
Görevin: Sana sağlanan tıbbi ders notu parçalarından ve sınav sorularından, öğrencinin sınavda en yüksek neti yapmasını sağlayacak "Yüksek Verimli Hap Bilgileri (High-Yield Pearls)", tanı kriterlerini, altın standartları ve hoca tuzaklarını damıtmaktır (Redüksiyon).
Kurallar:
1. Gereksiz dolgu cümlelerini at, doğrudan ezberlenmesi ve bilinmesi gereken anahtar mekanizmaları maddeler halinde ver.
2. Klinik ipuçlarını, triadları, pentadları ve sık karıştırılan ayırıcı tanıları tablo veya net maddeler halinde sun.
3. Çıkmış sınav sorularında bu konudan hangi soru tiplerinin geldiğini belirt.`;

    case 'verify':
      return `Sen Tıp Fakültesi Sınav İtiraz ve Akademik Doğruluk Hakemisin.
Görevin: İlgili sorunun, doğru kabul edilen cevabın ve şıkların fakülte amfi ders notlarıyla uyumlu olup olmadığını denetlemektir.
Kurallar:
1. İddia edilen cevabın ders notundaki doğrudan karşılığını tespit et.
2. Eğer soruda veya şıklarda amfi notlarına göre çelişki, iki doğru cevap veya amfi notuna aykırı bir durum varsa net olarak açıkla.
3. Hangi slaytta veya hangi konuda bu bilginin geçtiğini belirt.`;

    default: // 'qa' or 'chat'
      return `Sen Tıp Fakültesi öğrencilerine rehberlik eden kıdemli bir Tıp Eğitmeni ve RAG Asistanısın.
Sana fakülte amfi ders notları, slayt sayfaları ve çıkmış kurul sınav sorularından derlenen en alakalı doğrudan referans parçaları verilmiştir.
Kurallar:
1. Yalnızca verilen güvenilir tıp referanslarını kullanarak net, akademik ve anlaşılır yanıt ver.
2. Cevabının sonunda kullandığın ders notu başlığını, slayt numarasını veya çıkmış soru yılını referans olarak göster.
3. Klinik mekanizmaları ve patofizyolojiyi adım adım açıkla.`;
  }
}

/**
 * Answer a query grounded on retrieved course material.
 */
export async function executeRagQuery(
  options: RagAskOptions,
  apiKey?: string,
  modelName: string = 'gemini-3.8-flash'
): Promise<RagAskResponse> {
  const mode = options.mode || 'qa';
  const cacheKey = `${mode}:${options.committeeId || ''}:${options.discipline || ''}:${options.query.trim().toLowerCase()}`;
  const cached = ragResponseCache.get(cacheKey);
  if (cached && cached.expiresAt > Date.now()) return cached.response;

  const effectiveQuery = (mode === 'redact' && options.targetQuestion)
    ? `${options.query} ${options.targetQuestion.rawStem || options.targetQuestion.stem || ''} ${options.targetQuestion.claimedAnswer || ''}`.trim()
    : options.query;

  const references = await searchRagChunks(effectiveQuery, apiKey, {
    committeeId: options.committeeId,
    discipline: options.discipline,
    limit: options.limit || 4,
  });
  const contextBlock = formatSourcesForPrompt(references, 550);

  const userPrompt = mode === 'redact' && options.targetQuestion
    ? `REDAKTE EDİLECEK HAM SORU:
${JSON.stringify(options.targetQuestion, null, 2)}

ÖĞRENCİ / KULLANICI TALİMATI:
${options.query}

GÜVENİLİR DERS VE ÇIKMIŞ SORU REFERANSLARI:
${contextBlock}

Lütfen yukarıdaki amfi notlarına dayanarak soruyu kusursuz bir şekilde redakte et.`
    : `SORU / TALEP:
${options.query}

GÜVENİLİR DERS VE ÇIKMIŞ SORU REFERANSLARI:
${contextBlock}

Lütfen bu referansları temel alarak talimatı yerine getir.`;

  const ai = await generateResilientMedicalAi({
    prompt: userPrompt,
    customGeminiKey: apiKey,
    model: modelName,
    responseFormat: 'text',
    systemInstruction: buildSystemPrompt(mode),
  });

  const response: RagAskResponse = {
    answer: ai.text || 'Yanıt üretilemedi.',
    mode,
    references,
    usedModel: ai.planUsed,
    sourcesCount: references.length,
  };

  if (ragResponseCache.size > 150) {
    const first = ragResponseCache.keys().next().value;
    if (first) ragResponseCache.delete(first);
  }
  ragResponseCache.set(cacheKey, { response, expiresAt: Date.now() + 30 * 60 * 1000 });
  return response;
}

/** Build a retrieval query from everything students remembered about a question. */
export function buildQuestionSearchQuery(question: any, extra?: string): string {
  const parts = [
    question.topic,
    question.reconstruction?.stem || question.rawQuestion?.stem || question.rawStem,
    ...(question.fragments || []).map((f: any) => f.text),
    ...(question.options || []).map((o: any) => o.text),
    ...(question.comments || []).map((c: any) => c.text),
    extra,
  ];
  return parts
    .filter((p) => typeof p === 'string' && p.trim() && !/^Soru #\d+$/.test(p.trim()))
    .join(' ')
    .slice(0, 2000);
}

const isRealDiscipline = (d?: string) => Boolean(d && d.trim() && !/^(Belirtilmedi|Tıp|Genel)$/i.test(d.trim()));

/** Course material and past exam questions most relevant to a student-recalled question. */
export async function findSourcesForQuestion(question: any, extra?: string, limit = 6): Promise<RagChunkResult[]> {
  const query = buildQuestionSearchQuery(question, extra);
  if (!query.trim()) return [];
  const results = await searchRagChunks(query, undefined, {
    committeeId: question.committeeId,
    discipline: isRealDiscipline(question.discipline) ? question.discipline : undefined,
    limit: limit + 1,
  });
  // A past question being edited must not be cited as evidence for itself.
  return results.filter((r) => !question.id || r.documentId !== question.id).slice(0, limit);
}

/** Past exam questions similar to a free-text description ("ACE inhibitörü öksürük sorusu çıktı"). */
export async function findSimilarPastQuestions(text: string, committeeId?: string, limit = 5) {
  const results = await searchRagChunks(text, undefined, { committeeId, documentType: 'past_question', limit });
  return results.map((r) => {
    const stemMatch = r.content.match(/Soru Kökü:\n([\s\S]*?)\n\nSeçenekler:/);
    // "Seçenekler:\nA) …\nB) …" bloğu: şıkları aktarabilmek için ayrıştır
    const optBlock = r.content.match(/Seçenekler:\s*\n([\s\S]*?)(?:\n\s*\n|$)/)?.[1] || '';
    const options = Array.from(optBlock.matchAll(/^\s*([A-E])\s*[).:-]\s*(.+)$/gm)).map((m) => ({ key: m[1], text: m[2].trim() }));
    const answer = r.content.match(/(?:Doğru[^:\n]*Cevap|Cevap)\s*:\s*([A-E])\b/i)?.[1];
    return {
      options,
      id: r.documentId,
      title: r.title,
      discipline: r.discipline,
      committeeId: r.committeeId,
      examYear: r.metadata?.examYear,
      claimedAnswer: r.metadata?.claimedAnswer || answer,
      stem: (stemMatch?.[1] || r.content).trim().slice(0, 400),
      score: r.combinedScore,
    };
  });
}

// ------------------------------------------------------------------
// Uygulama içi genel arama: tüm veri setleri (chunk'lar) üzerinde BM25.
// Sonuçlar tekilleştirilir, eşleşmenin çevresinden kesit çıkarılır ve
// türe göre sayılır; arayüz ilk 5'i gösterir, "Tümünü gör" sayfalar.
// ------------------------------------------------------------------
export interface SearchHit {
  id: string;
  documentId: string;
  documentType: RagDocumentType;
  committeeId?: string;
  discipline?: string;
  title: string;
  pageNumber?: number;
  snippet: string;
  content: string;
  score: number;
}

export interface SearchEverythingResult {
  query: string;
  total: number;
  /** Havuz sınırına ulaşıldı: gerçek sonuç sayısı daha fazla olabilir */
  capped: boolean;
  byType: Partial<Record<RagDocumentType, number>>;
  results: SearchHit[];
  /** Sorgunun anlaşılma biçimi: düzeltme, kavramlar (varlık kartı), niyet, eşanlamlı yeniden yazımlar */
  understanding?: {
    corrected: string | null;
    changes: Array<{ from: string; to: string }>;
    concepts: Array<{ label: string; type: string; ref: { kind: string; id: string } | null }>;
    intent: string | null;
    rewrites: string[];
  };
}

const SEARCH_POOL = 400;

/** Sorgu köklerinin en yoğun geçtiği pencereden okunabilir bir kesit çıkarır. */
export function makeSnippet(content: string, query: string, size = 240): string {
  const text = content.replace(/^\s*\[[^\]]{2,60}\]\s*/, '').replace(/\s+/g, ' ').trim();
  if (text.length <= size) return text;
  // foldTurkish uzunluğu korur: katlanmış metindeki konumlar asıl metne denk gelir
  const folded = foldTurkish(text);
  const stems = Array.from(new Set(foldTurkish(query).split(/[^a-z0-9]+/).filter((w) => w.length >= 3).map((w) => w.slice(0, w.length >= 8 ? 7 : 5))));
  const hits: Array<{ at: number; stem: number }> = [];
  stems.forEach((st, i) => {
    for (let at = folded.indexOf(st); at >= 0 && hits.length < 400; at = folded.indexOf(st, at + 1)) hits.push({ at, stem: i });
  });
  if (hits.length === 0) return text.slice(0, size).trimEnd() + '…';
  hits.sort((x, y) => x.at - y.at);
  let best = hits[0].at;
  let bestScore = 0;
  for (let i = 0; i < hits.length; i++) {
    const seenStems = new Set<number>();
    for (let j = i; j < hits.length && hits[j].at - hits[i].at < size * 0.7; j++) seenStems.add(hits[j].stem);
    if (seenStems.size > bestScore) { bestScore = seenStems.size; best = hits[i].at; }
  }
  let start = Math.max(0, best - Math.floor(size / 4));
  const sp = text.lastIndexOf(' ', start);
  if (start > 0 && sp > start - 20) start = sp + 1;
  const end = Math.min(text.length, start + size);
  return (start > 0 ? '…' : '') + text.slice(start, end).trim() + (end < text.length ? '…' : '');
}

const cleanTitle = (t: string) => t.replace(/\s*\[[^\]]*\]?\s*$/, '').replace(/\s+/g, ' ').trim() || t;

export async function searchEverything(
  query: string,
  options: { types?: RagDocumentType[]; committeeId?: string; offset?: number; limit?: number } = {}
): Promise<SearchEverythingResult> {
  const q = query.trim();
  const offset = Math.max(0, options.offset || 0);
  const limit = Math.min(50, Math.max(1, options.limit || 5));
  if (!q) return { query: q, total: 0, capped: false, byType: {}, results: [] };

  // Sıralanmış havuz önbelleği: sayfalama ve aynı sorgunun tekrarı (palet → tüm sonuçlar) anında döner
  const cacheKey = `${q.toLocaleLowerCase('tr-TR')}|${options.committeeId || ''}`;
  const cached = searchPoolCache.get(cacheKey);
  if (cached && Date.now() - cached.at < 10 * 60_000) return finishSearch(cached, options, q, offset, limit);

  // Sorgu zekâsı: yazım düzeltme, kavramlar, niyet, eşdeğerlik yuvaları ("böbrek tümörü" ≈ "renal neoplazm")
  const { analyzeFor, getQueryIntel } = await import('./queryIntel/server.ts');
  const intelReady = Boolean(getQueryIntel());
  const { EVIDENCE_CUES } = await import('./queryIntel/core.ts');
  // Tırnak içindeki sorgu ("…") olduğu gibi aranır: düzeltme/eşanlamlı yok (kullanıcı "özgün sorguyla ara" dedi)
  const exact = /^".+"$/.test(q);
  const u = exact
    ? { query: q, corrected: null, changes: [], concepts: [], intent: null, rewrites: [], focus: [], slots: [] }
    : analyzeFor(q);
  const base = exact ? q.slice(1, -1) : u.corrected || q;
  const variants: string[] = [base];
  for (const rw of u.rewrites.slice(0, 2)) variants.push(rw);
  // Yuva varyantları: tek seferde bir sözcüğü eşdeğer kökle değiştir (en çok 2)
  const baseWords = foldTurkish(base).split(/[^a-z0-9]+/).filter(Boolean);
  for (const sl of u.slots) {
    if (variants.length >= 5) break;
    const alt = sl.alts.find((a) => a.length >= 4);
    if (!alt) continue;
    const at = baseWords.indexOf(sl.w);
    if (at < 0) continue;
    variants.push(baseWords.map((w, i) => (i === at ? alt : w)).join(' '));
  }
  // Vektör kolu BM25 ile PARALEL başlar (eskiden sırayla: ~400 ms kayıp). Kavram etiketleri yoğun sorguya eklenir.
  const vecText = [base, ...u.concepts.filter((c) => c.strong !== false).map((c) => c.label.replace(/\s*\([^)]*\)/g, ''))].join(' ').slice(0, 500);
  const vecPromise = Promise.race([
    semanticSearch(vecText, { committeeId: options.committeeId, limit: 30 }),
    new Promise<never>((_, rej) => setTimeout(() => rej(new Error('vec-zamanasimi')), 2500)),
  ]).catch(() => [] as any[]);

  // AI üretimi kayıtlar kaynak değildir (bkz. GROUNDING_DOC_TYPES): aramada gösterilmez
  const byId = new Map<string, Awaited<ReturnType<typeof searchLocalRag>>[number]>();
  const parts = await Promise.all(
    variants.map((v, vi) =>
      searchLocalRag(v, { committeeId: options.committeeId, limit: vi === 0 ? SEARCH_POOL : 150 })
    )
  );
  for (let vi = 0; vi < parts.length; vi++) {
    const part = parts[vi];
    for (const r of part) {
      if (r.documentType === 'ai_qa' || r.documentType === 'ai_refinement') continue;
      const prev = byId.get(r.id);
      // Varyanttan gelen sonuç ana sorgudan biraz geride başlar
      const sc = vi === 0 ? r.matchScore : r.matchScore * 0.9;
      if (!prev || prev.matchScore < sc) byId.set(r.id, { ...r, matchScore: sc });
    }
  }
  // Ad eşleşmesi: sorgu (niyet sözcükleri atılmış hâli de) bir hastalık/sözlük kartının adı ya da
  // eşanlamlısıysa kart havuza kesin girer ve sıralamada öne alınır ("Hiperlipidemi" → kendi kartı).
  const intentCut = (v: string) => cardNameKey(v).split(' ').filter((w) => !(EVIDENCE_CUES.some((x) => x.stems.some((st: string) => w.startsWith(st))))).join(' ');
  const nameHit = new Map<string, 'name' | 'alias'>();
  for (const v of new Set([base, q.replace(/^"|"$/g, ''), ...variants].flatMap((v) => [v, intentCut(v)]))) {
    for (const { chunk, kind } of findCardsByName(v)) {
      if (options.committeeId && chunk.committeeId && chunk.committeeId !== options.committeeId && chunk.documentType !== 'disease') continue;
      if (nameHit.get(chunk.id) !== 'name') nameHit.set(chunk.id, kind);
      if (!byId.has(chunk.id)) byId.set(chunk.id, { ...chunk, similarity: 1, matchScore: 60, snippet: '', source: 'local' as const } as any);
    }
  }
  const pooled = [...byId.values()];
  // Yeniden sıralama: kapsama yuva bazında ölçülür (yuvadaki herhangi bir eşdeğer kök yeter);
  // uzun tıbbi terimlerde 5 harf kök fazla geniş (tromboksan ≠ trombosit): 8+ harfte 7 harf kullanılır.
  const stemOf = (w: string) => w.slice(0, w.length >= 8 ? 7 : 5);
  const slotStems: string[][] = (u.slots.length ? u.slots.map((sl) => [sl.w, ...sl.alts]) : baseWords.filter((w) => w.length >= 3).map((w) => [w]))
    .filter((alts) => alts[0].length >= 3)
    .map((alts) => Array.from(new Set(alts.map(stemOf))));
  const stems = Array.from(new Set(slotStems.flat()));
  const fullWords = Array.from(new Set(baseWords.filter((w) => w.length >= 4)));
  const conceptKeys = u.concepts
    .filter((c) => c.strong !== false)
    .map((c) => ({ key: foldTurkish(c.label.replace(/\s*\([^)]*\)/g, '')).replace(/[^a-z0-9]+/g, ' ').trim(), entity: c.type !== 'topic' }))
    .filter((c) => c.key.length >= 3);
  const intentStems = u.intent ? (EVIDENCE_CUES.find((x) => x.k === u.intent)?.stems || []) : [];
  const denseRank = new Map<string, number>();
  ((await vecPromise) as any[]).forEach((r: any, i: number) => {
    if (r?.id && !denseRank.has(r.id)) denseRank.set(r.id, i);
  });
  const rank = (r: (typeof pooled)[number]) => {
    if (slotStems.length === 0) return r.matchScore;
    const body = foldTurkish(r.content);
    const title = foldTurkish(r.title);
    const has = (txt: string, alts: string[]) => alts.some((st) => txt.includes(st));
    const cover = slotStems.filter((alts) => has(body, alts) || has(title, alts)).length / slotStems.length;
    const inTitle = slotStems.filter((alts) => has(title, alts)).length / slotStems.length;
    // Tam kelime başlıkta geçiyorsa güçlü sinyal ("Hipotiroidi" başlığı > "hipotir" kök geçişi).
    const inTitleFull = fullWords.filter((w) => title.includes(w)).length / Math.max(1, fullWords.length);
    // Yoğunluk: konuyla ilgili belge terimi sık geçirir (tekil etiyoloji listesinden ayrışır).
    let hits = 0;
    for (const st of stems) {
      let p = body.indexOf(st);
      while (p >= 0 && hits < 40) { hits++; p = body.indexOf(st, p + st.length); }
    }
    const words = Math.max(50, body.split(/\s+/).length);
    const dens = Math.min(10, (hits / words) * 100);
    const d = denseRank.get(r.id);
    const vecBonus = d === undefined ? 0 : (1 - d / 30) * 40;
    // Kavram: başlığında sorgudaki kavramın adı geçen belge öne; hastalık/sözlük kartı en öne (varlık kartı)
    let conceptBonus = 0;
    const titleN = title.replace(/\([^)]*\)/g, ' ').replace(/[^a-z0-9]+/g, ' ').trim();
    for (const c of conceptKeys) {
      if (!titleN.includes(c.key)) continue;
      // Varlık kartı yalnız kavramın KENDİ kartı: "Hastalık: Nefrotik sendrom" evet, "Sözlük: silinme ve nefrotik sendrom" hayır
      const core = titleN.replace(/^(hastalik|sozluk)\s+/, '');
      const own = core === c.key || (core.startsWith(c.key) && core.length <= c.key.length + 3);
      const card = r.documentType === 'disease' || r.documentType === 'glossary_term';
      conceptBonus = Math.max(conceptBonus, c.entity && card && own ? (r.documentType === 'disease' ? 95 : 85) : card ? 10 : 35);
    }
    // Niyet: "tedavisi" aranıyorsa tedavi anlatan parça öne
    const intentBonus = intentStems.length && intentStems.some((st) => body.includes(st)) ? 18 : 0;
    // Kartın kendi adı/eşanlamlısı sorguyla birebir: en güçlü sinyal. Hastalık ana kartı > alt bölüm > sözlük
    const nh = nameHit.get(r.id);
    const section = r.documentType === 'disease' && r.title.includes(' — ');
    const nameBonus = !nh ? 0 : (r.documentType === 'disease' ? (section ? (intentStems.length ? 150 : 70) : 170) : 90) - (nh === 'alias' ? 15 : 0);
    return cover * 100 + inTitle * 30 + inTitleFull * 60 + dens * 4 + vecBonus + conceptBonus + intentBonus + nameBonus + Math.min(r.matchScore, 120) * 0.25;
  };
  const ranked = pooled
    .map((r) => ({ r, k: rank(r) }))
    .sort((a, b) => b.k - a.k)
    .map(({ r }) => r);
  // Kimliğe benzeyen sorgu (boşluksuz, rakam ve -/_ içeren): önce kimlik eşleşmeleri
  const looksLikeId = !/\s/.test(q) && /\d/.test(q) && /[-_]/.test(q);
  const idHits = looksLikeId
    ? findChunksById(q)
        .filter((c) => c.documentType !== 'ai_qa' && c.documentType !== 'ai_refinement')
        .map((c) => ({ ...c, similarity: 1, matchScore: 999, snippet: '', source: 'local' as const }))
    : [];
  // Kimlik bulunduysa yalnızca onlar gösterilir; bulunamadıysa normal metin araması
  const raw = idHits.length > 0 ? idHits : ranked;
  const examDumps = getExamDumpNoteIds();
  const seen = new Set<string>();
  const pool: SearchHit[] = [];
  const byType: Partial<Record<RagDocumentType, number>> = {};
  for (const r of raw) {
    if (r.documentType === 'lecture_slide' && examDumps.has(r.documentId)) continue;
    const keys = dedupeKeys(r);
    const snippet = makeSnippet(r.content, q);
    const sig = foldTurkish(snippet).replace(/[^a-z0-9]+/g, '');
    keys.push(`snip:${sig.slice(10, 110)}`);
    // Aynı soru farklı dosyalarda tekrar indekslenmiş olabilir: soru kökü ile de tekilleştir
    const stemPart = r.content.split(/Seçenekler\s*:/i)[0];
    if (stemPart.length < r.content.length) keys.push(`stem:${foldTurkish(stemPart).replace(/[^a-z0-9]+/g, '').slice(-70)}`);
    if (keys.some((k) => seen.has(k))) continue;
    keys.forEach((k) => seen.add(k));
    byType[r.documentType] = (byType[r.documentType] || 0) + 1;
    pool.push({
      id: r.id,
      documentId: r.documentId,
      documentType: r.documentType,
      committeeId: r.committeeId,
      discipline: r.discipline,
      title: cleanTitle(r.title),
      pageNumber: r.pageNumber,
      snippet,
      content: r.content.length > 4000 ? r.content.slice(0, 4000) + '…' : r.content,
      score: Math.round(r.matchScore * 10) / 10,
    });
  }
  const understanding = {
    corrected: u.corrected,
    changes: u.changes.map((c) => ({ from: c.from, to: c.to })),
    concepts: u.concepts.filter((c) => c.strong !== false).slice(0, 3).map((c) => ({ label: c.label, type: c.type, ref: c.ref })),
    intent: u.intent,
    rewrites: u.rewrites.slice(0, 2),
  };
  const entry = { at: Date.now(), pool, byType, capped: raw.length >= SEARCH_POOL, understanding };
  // Motor henüz yüklenmemişken (açılışın ilk saniyeleri) yapılan anlamlandırmasız sonuç önbelleğe girmez
  if (intelReady) searchPoolCache.set(cacheKey, entry);
  if (searchPoolCache.size > 300) searchPoolCache.delete(searchPoolCache.keys().next().value as string);
  return finishSearch(entry, options, q, offset, limit);
}

interface PoolEntry {
  at: number;
  pool: SearchHit[];
  byType: Partial<Record<RagDocumentType, number>>;
  capped: boolean;
  understanding: SearchEverythingResult['understanding'];
}
const searchPoolCache = new Map<string, PoolEntry>();

function finishSearch(e: PoolEntry, options: { types?: RagDocumentType[] }, q: string, offset: number, limit: number): SearchEverythingResult {
  const pool = options.types?.length ? e.pool.filter((r) => options.types!.includes(r.documentType)) : e.pool;
  return { query: q, total: pool.length, capped: e.capped, byType: e.byType, results: pool.slice(offset, offset + limit), understanding: e.understanding };
}
