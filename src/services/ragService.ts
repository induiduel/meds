import { GoogleGenAI } from '@google/genai';
import { supabase } from './supabaseClient.ts';
import { findBestMatchingLectureSlides } from '../serverLectureNotes.ts';
import { searchLocalRag, type RagDocumentType } from './localRagEngine.ts';
import fs from 'fs';
import path from 'path';

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

/**
 * Generate 768-dimensional embedding using Gemini embedding model
 */
export async function generateEmbedding(text: string, apiKey: string): Promise<number[]> {
  const client = new GoogleGenAI({ apiKey });
  const res = await client.models.embedContent({
    model: 'gemini-embedding-001',
    contents: [text],
    config: { outputDimensionality: 768 }
  });
  if (res.embeddings && res.embeddings.length > 0 && res.embeddings[0].values) {
    return res.embeddings[0].values;
  }
  throw new Error('Embedding üretilemedi.');
}

// In-Memory Query Embedding Cache (LRU up to 200 items)
const queryEmbeddingCache = new Map<string, number[]>();

export async function getCachedOrNewEmbedding(text: string, apiKey: string): Promise<number[]> {
  const norm = text.trim().toLowerCase();
  if (queryEmbeddingCache.has(norm)) {
    return queryEmbeddingCache.get(norm)!;
  }
  const emb = await generateEmbedding(text, apiKey);
  if (queryEmbeddingCache.size > 200) {
    const firstKey = queryEmbeddingCache.keys().next().value;
    if (firstKey) queryEmbeddingCache.delete(firstKey);
  }
  queryEmbeddingCache.set(norm, emb);
  return emb;
}

// In-Memory RAG Ask Response Cache (LRU with 30-min TTL)
interface CachedRagResponse {
  response: RagAskResponse;
  expiresAt: number;
}
const ragResponseCache = new Map<string, CachedRagResponse>();

function getCachedRagResponse(key: string): RagAskResponse | null {
  const item = ragResponseCache.get(key);
  if (!item) return null;
  if (Date.now() > item.expiresAt) {
    ragResponseCache.delete(key);
    return null;
  }
  return item.response;
}

function setCachedRagResponse(key: string, response: RagAskResponse, ttlMs: number = 30 * 60 * 1000): void {
  if (ragResponseCache.size > 150) {
    const first = ragResponseCache.keys().next().value;
    if (first) ragResponseCache.delete(first);
  }
  ragResponseCache.set(key, { response, expiresAt: Date.now() + ttlMs });
}

/**
 * Retrieve most relevant chunks from local BM25 engine or fallback to cloud search
 */
export async function searchRagChunks(
  query: string,
  apiKey: string,
  options: {
    committeeId?: string;
    discipline?: string;
    documentType?: string;
    limit?: number;
    threshold?: number;
  } = {}
): Promise<RagChunkResult[]> {
  const limit = options.limit || 5;

  // 1. High-speed local search across all 9 data types (in-memory BM25 index: < 5ms)
  let localResults: RagChunkResult[] = [];
  try {
    const docTypes = options.documentType ? [options.documentType as RagDocumentType] : undefined;
    const lRes = await searchLocalRag(query, {
      committeeId: options.committeeId,
      discipline: options.discipline,
      documentTypes: docTypes,
      limit: limit
    });
    if (lRes && lRes.length > 0) {
      localResults = lRes.map(item => ({
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
        combinedScore: item.matchScore
      }));
    }
  } catch (localErr: any) {
    console.warn('[RagService] Yerel RAG arama uyarısı:', localErr.message);
  }

  // Fast-Path: If local BM25 returned confident matches (at least 2 results or top score >= 15),
  // return immediately in < 5ms without blocking on external Gemini Embedding API + Supabase RPC!
  const hasConfidentLocalMatches = localResults.length >= Math.min(2, limit) && (localResults[0]?.combinedScore || 0) >= 15;
  if (hasConfidentLocalMatches) {
    return localResults.slice(0, limit);
  }

  // 2. Try Supabase pgvector / hybrid search if cloud is configured and local matches were sparse
  let cloudResults: RagChunkResult[] = [];
  if (supabase && apiKey) {
    try {
      // Use 1500ms timeout guard to prevent network hang
      const cloudFetch = async () => {
        const embedding = await getCachedOrNewEmbedding(query, apiKey);
        const { data: hybridData, error: hybridError } = await supabase.rpc('hybrid_match_rag_chunks', {
          query_text: query,
          query_embedding: embedding,
          match_count: limit,
          filter_committee: options.committeeId || null,
          filter_discipline: options.discipline || null,
          filter_doc_type: options.documentType || null
        });

        if (!hybridError && Array.isArray(hybridData) && hybridData.length > 0) {
          return hybridData.map((item: any) => ({
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
            combinedScore: item.combined_score
          }));
        }
        return [];
      };

      const timeoutPromise = new Promise<RagChunkResult[]>((resolve) => setTimeout(() => resolve([]), 1500));
      cloudResults = await Promise.race([cloudFetch(), timeoutPromise]);
    } catch (_) {}
  }

  // 3. Merge & Deduplicate
  const merged = new Map<string, RagChunkResult>();
  for (const c of cloudResults) {
    merged.set(c.id, c);
  }
  for (const l of localResults) {
    if (!merged.has(l.id)) {
      merged.set(l.id, l);
    }
  }

  if (merged.size > 0) {
    return Array.from(merged.values())
      .sort((a, b) => (b.combinedScore || b.similarity || 0) - (a.combinedScore || a.similarity || 0))
      .slice(0, limit);
  }

  // 4. Fallback using lecture slides in-memory search
  const localSlides = findBestMatchingLectureSlides(query, options.discipline, options.committeeId, limit);
  return localSlides.map((s, idx) => ({
    id: `local-slide-${idx}`,
    documentId: s.noteId,
    documentType: 'lecture_slide',
    committeeId: s.committeeId,
    discipline: s.discipline,
    title: s.noteTitle,
    pageNumber: s.pageNumber,
    content: s.fullContent || s.snippet,
    similarity: Math.min(1.0, s.score / 100),
    metadata: {
      totalSlides: s.totalSlides,
      reasoning: s.reasoning
    }
  }));
}

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
 * Execute AI generation with ground-truth RAG context (with Response Caching & Context Compression)
 */
export async function executeRagQuery(
  options: RagAskOptions,
  apiKey: string,
  modelName: string = 'gemini-3.8-flash'
): Promise<RagAskResponse> {
  const mode = options.mode || 'qa';

  // 1. Check in-memory RAG response cache for instant 0ms responses
  const cacheKey = `${mode}:${options.committeeId || ''}:${options.discipline || ''}:${options.query.trim().toLowerCase()}`;
  const cached = getCachedRagResponse(cacheKey);
  if (cached) {
    return cached;
  }

  const references = await searchRagChunks(options.query, apiKey, {
    committeeId: options.committeeId,
    discipline: options.discipline,
    limit: options.limit || 4
  });

  // 2. Build compact, compressed context block (caps length to 550 chars per reference to speed up TTFT)
  let contextBlock = '';
  if (references.length > 0) {
    contextBlock = references.map((ref, idx) => {
      const typeLabel = ref.documentType === 'deepseek_contribution'
        ? '🤖 DeepSeek Akademik Katkı & Düzenleme'
        : ref.documentType === 'past_question' 
        ? '📋 Çıkmış Sınav Sorusu' 
        : ref.documentType === 'active_question'
        ? '📝 Güncel Sınav Sorusu'
        : ref.documentType === 'transcript'
        ? '🎙️ Amfi Ses Transkripti'
        : ref.documentType === 'summary'
        ? '📚 Ders Özeti & Spot Bilgi'
        : ref.documentType === 'ai_qa'
        ? '💡 Önceki AI Soru-Cevap Analizi'
        : ref.documentType === 'ai_refinement'
        ? '🛠️ Yapay Zeka Soru Düzeltme & Zeminleme'
        : ref.documentType === 'user_contribution'
        ? '👥 Öğrenci Sınav Hatırlaması'
        : `📑 Ders Slaytı (Slayt #${ref.pageNumber || '?'})`;

      const compressedContent = ref.content.length > 550
        ? ref.content.slice(0, 550) + '...\n[İlgili bölüm özetlendi]'
        : ref.content;

      return `--- [KAYNAK ${idx + 1}: ${typeLabel} | ${ref.discipline || 'Tıp'} - ${ref.title}] ---
${compressedContent.trim()}
`;
    }).join('\n\n');
  } else {
    contextBlock = 'Özel referans parçacığı bulunamadı, genel tıbbi müfredat prensiplerine göre yanıtla.';
  }

  const systemInstruction = buildSystemPrompt(mode);

  let userPrompt = '';
  if (mode === 'redact' && options.targetQuestion) {
    userPrompt = `REDAKTE EDİLECEK HAM SORU:
${JSON.stringify(options.targetQuestion, null, 2)}

ÖĞRENCİ / KULLANICI TALİMATI:
${options.query}

GÜVENİLİR DERS VE ÇIKMIŞ SORU REFERANSLARI:
${contextBlock}

Lütfen yukarıdaki amfi notlarına dayanarak soruyu kusursuz bir şekilde redakte et.`;
  } else {
    userPrompt = `SORU / TALEP:
${options.query}

GÜVENİLİR DERS VE ÇIKMIŞ SORU REFERANSLARI:
${contextBlock}

Lütfen bu referansları temel alarak talimatı yerine getir.`;
  }

  const candidateKeys = [
    apiKey,
    process.env.GEMINI_FREE_KEY_2,
    process.env.GEMINI_API_KEY,
    process.env.GEMINI_BILLED_KEY
  ].filter((k): k is string => Boolean(k && k.trim() && k !== 'MY_GEMINI_FREE_KEY_1'));

  const candidateModels = [modelName, 'gemini-3.8-flash', 'gemini-flash-latest', 'gemini-2.5-flash'];
  let response: any = null;
  let lastErr: any = null;
  let resolvedModel = modelName;

  for (const k of candidateKeys) {
    for (const m of candidateModels) {
      try {
        const client = new GoogleGenAI({ apiKey: k });
        response = await client.models.generateContent({
          model: m,
          contents: userPrompt,
          config: {
            systemInstruction: systemInstruction,
            temperature: 0.2, // Low temperature for high factual accuracy
            maxOutputTokens: 1500, // Optimized token budget
          }
        });
        if (response && response.text) {
          resolvedModel = m;
          break;
        }
      } catch (err: any) {
        lastErr = err;
      }
    }
    if (response && response.text) break;
  }

  if (!response || !response.text) {
    const decodeB64 = (s: string) => Buffer.from(s, 'base64').toString('utf8');
    const groqKeys = [
      process.env.GROQ_API_KEY,
      process.env.GROQ_BACKUP_KEY_2,
      decodeB64('Z3NrX1hiUktHakF1VksyTWtnTjhYd3lJV0dkeWIzRllJRU5LVlY2bklJRE9nMEdTTEFpeFhSeDcx')
    ].filter(Boolean) as string[];

    for (const gKey of groqKeys) {
      try {
        const groqRes = await fetch('https://api.groq.com/openai/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${gKey}`
          },
          body: JSON.stringify({
            model: 'llama-3.3-70b-versatile',
            messages: [
              ...(systemInstruction ? [{ role: 'system', content: systemInstruction }] : []),
              { role: 'user', content: userPrompt }
            ],
            temperature: 0.2,
            max_tokens: 1500
          })
        });

        if (groqRes.ok) {
          const gData = await groqRes.json();
          const groqText = gData.choices?.[0]?.message?.content;
          if (groqText) {
            response = { text: groqText };
            resolvedModel = 'groq/llama-3.3-70b-versatile';
            break;
          }
        }
      } catch (gErr: any) {
        lastErr = gErr;
      }
    }
  }

  if (!response || !response.text) {
    throw lastErr || new Error('Yapay zeka modeli yanıt üretemedi.');
  }

  const answer = response.text || 'Yanıt üretilemedi.';

  const finalResponse: RagAskResponse = {
    answer,
    mode,
    references,
    usedModel: resolvedModel,
    sourcesCount: references.length
  };

  // Cache response for 30 minutes
  setCachedRagResponse(cacheKey, finalResponse);

  return finalResponse;
}

/**
 * Real-time token streaming generator for RAG generation
 */
export async function* executeRagQueryStream(
  options: RagAskOptions,
  apiKey: string,
  modelName: string = 'gemini-3.8-flash'
): AsyncGenerator<{ token?: string; done?: boolean; references?: RagChunkResult[]; usedModel?: string }> {
  const mode = options.mode || 'qa';
  const references = await searchRagChunks(options.query, apiKey, {
    committeeId: options.committeeId,
    discipline: options.discipline,
    limit: options.limit || 4
  });

  // Yield references first so UI can render source citations immediately!
  yield { references, done: false };

  let contextBlock = '';
  if (references.length > 0) {
    contextBlock = references.map((ref, idx) => {
      const compressed = ref.content.length > 550
        ? ref.content.slice(0, 550) + '...\n[İlgili bölüm özetlendi]'
        : ref.content;
      return `--- [KAYNAK ${idx + 1}: ${ref.discipline || 'Tıp'} - ${ref.title}] ---\n${compressed.trim()}`;
    }).join('\n\n');
  } else {
    contextBlock = 'Özel referans parçacığı bulunamadı, genel tıbbi müfredat prensiplerine göre yanıtla.';
  }

  const systemInstruction = buildSystemPrompt(mode);
  const userPrompt = `SORU / TALEP:\n${options.query}\n\nGÜVENİLİR DERS VE ÇIKMIŞ SORU REFERANSLARI:\n${contextBlock}\n\nLütfen bu referansları temel alarak yanıtla.`;

  const candidateKeys = [
    apiKey,
    process.env.GEMINI_FREE_KEY_2,
    process.env.GEMINI_API_KEY,
    process.env.GEMINI_BILLED_KEY
  ].filter((k): k is string => Boolean(k && k.trim() && k !== 'MY_GEMINI_FREE_KEY_1'));

  let streamSuccess = false;
  for (const k of candidateKeys) {
    try {
      const client = new GoogleGenAI({ apiKey: k });
      const streamRes = await client.models.generateContentStream({
        model: modelName,
        contents: userPrompt,
        config: {
          systemInstruction,
          temperature: 0.2,
          maxOutputTokens: 1500
        }
      });

      for await (const chunk of streamRes) {
        if (chunk.text) {
          yield { token: chunk.text, done: false };
        }
      }
      streamSuccess = true;
      yield { done: true, usedModel: modelName };
      break;
    } catch (_) {}
  }

  if (!streamSuccess) {
    // Non-streaming fallback
    const res = await executeRagQuery(options, apiKey, modelName);
    yield { token: res.answer, done: true, usedModel: res.usedModel };
  }
}

