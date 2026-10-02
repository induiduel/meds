/**
 * ==============================================================================
 * MedSoru Local & Hybrid RAG Engine (localRagEngine.ts)
 * ==============================================================================
 * Bu motor:
 * 1. Tüm tıp verilerini 8 farklı kategoride parçalar (chunklar):
 *    - Çıkmış Sorular (past_question)
 *    - Eklenen/Aktif Sorular (active_question)
 *    - Amfi Ders Slaytları (lecture_slide)
 *    - Ders Özetleri & Spot Notlar (summary)
 *    - Ses Transkriptleri (transcript)
 *    - Kullanıcı Katkı & Yorumları (user_contribution)
 *    - Yapay Zeka Düzeltmeleri & Revizyonları (ai_refinement)
 *    - Yapay Zeka Soru Sohbetleri & Tartışmaları (ai_qa)
 * 2. Yerel dosya sistemi (data/local_rag_chunks.json) ve bellek içi (in-memory)
 *    ters indeks ile 5 ms altında ultra hızlı arama sağlar.
 * 3. Gemini embedding modeli ile vektörleri yerel önbelleğe alır ve Supabase
 *    'rag_chunks' & 'ai_question_interactions' tablolarına çift yönlü eşitler.
 * ==============================================================================
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { GoogleGenAI } from '@google/genai';
import { createClient, SupabaseClient } from '@supabase/supabase-js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const DATA_DIR = path.resolve(PROJECT_ROOT, 'data');
const LOCAL_CHUNKS_FILE = path.resolve(DATA_DIR, 'local_rag_chunks.json');
const AI_INTERACTIONS_FILE = path.resolve(DATA_DIR, 'ai_interactions.json');
const MANIFEST_FILE = path.resolve(DATA_DIR, 'rag_indexing_manifest.json');
const DESKTOP_DATABASE_DIR = process.env.MEDS_DATABASE_DIR || 'C:\\Users\\indui\\Desktop\\meds_database';

export type RagDocumentType =
  | 'past_question'
  | 'active_question'
  | 'lecture_slide'
  | 'summary'
  | 'transcript'
  | 'user_contribution'
  | 'ai_refinement'
  | 'ai_qa';

export interface RagChunk {
  id: string;
  documentId: string;
  documentType: RagDocumentType;
  committeeId?: string;
  discipline?: string;
  title: string;
  pageNumber?: number;
  content: string;
  metadata: Record<string, any>;
  hash: string;
  embedding?: number[];
  createdAt: string;
  updatedAt: string;
}

export interface AiInteractionRecord {
  id: string;
  questionId?: string;
  committeeId?: string;
  discipline?: string;
  topic?: string;
  interactionType: 'chat_qa' | 'refinement' | 'redaction' | 'mnemonic' | 'trap_warning' | 'user_comment';
  userId?: string;
  userDisplayName?: string;
  prompt: string;
  response: string;
  contextSnapshot?: Record<string, any>;
  metadata?: Record<string, any>;
  upvotes: number;
  ragChunkId?: string;
  createdAt: string;
}

export interface RagSearchResult {
  id: string;
  documentId: string;
  documentType: RagDocumentType;
  committeeId?: string;
  discipline?: string;
  title: string;
  pageNumber?: number;
  content: string;
  metadata: Record<string, any>;
  similarity: number;
  matchScore: number;
  snippet: string;
  source: 'local' | 'cloud';
}

// Stopwords to filter out from auto-keyword index
const TURKISH_STOPWORDS = new Set([
  've', 'ile', 'veya', 'için', 'gibi', 'kadar', 'daha', 'olan', 'olarak', 'bunun',
  'buna', 'şekilde', 'olarak', 'üzere', 'bir', 'bu', 'şu', 'o', 'her', 'tüm', 'bütün',
  'sayfa', 'slayt', 'bölüm', 'ders', 'notu', 'konu', 'ünite', 'tablo', 'şekil', 'görsel',
  'hangisidir', 'aşağıdakilerden', 'hangisi', 'nedir', 'aşağıdaki', 'vardır', 'yoktur',
  'the', 'and', 'for', 'with', 'from', 'that', 'this', 'are', 'was'
]);

function hashContent(content: string): string {
  return crypto.createHash('md5').update(content.trim()).digest('hex');
}

function cleanTextForTokens(text: string): string[] {
  return text
    .toLowerCase()
    .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"'’“”…\[\]<>|\\+]/g, ' ')
    .split(/\s+/)
    .map(w => w.trim())
    .filter(w => w.length >= 3 && !TURKISH_STOPWORDS.has(w));
}

// Supabase Init
let supabaseClient: SupabaseClient | null = null;
function getSupabase(): SupabaseClient | null {
  if (supabaseClient) return supabaseClient;
  const url = process.env.SUPABASE_URL || 'https://kgutsltgmqbnlxcnzrtl.supabase.co';
  const key = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_PUBLISHABLE_KEY || 'sb_publishable_EVdXdIi_2mxVr3HZKYabwQ_li5KuE1Q';
  if (url && key) {
    try {
      supabaseClient = createClient(url, key);
      return supabaseClient;
    } catch (_) {}
  }
  return null;
}

// Gemini Key Pool with Rotation
function getGeminiKeys(): string[] {
  return [
    process.env.GEMINI_API_KEY,
    process.env.GEMINI_FREE_KEY_2,
    process.env.GEMINI_BILLED_KEY
  ].filter((k): k is string => Boolean(k && k.trim() && k !== 'MY_GEMINI_FREE_KEY_1' && k !== 'MY_GEMINI_API_KEY'));
}

let keyIndex = 0;
function getNextGeminiClient(): GoogleGenAI | null {
  const keys = getGeminiKeys();
  if (keys.length === 0) return null;
  const key = keys[keyIndex % keys.length];
  keyIndex++;
  return new GoogleGenAI({ apiKey: key });
}

// ==============================================================================
// In-Memory Index State
// ==============================================================================
let memoryChunks: Map<string, RagChunk> = new Map();
let invertedIndex: Map<string, Set<string>> = new Map(); // token -> Set of chunk ids
let isInitialized = false;
let isIndexingInProgress = false;

// Load stored chunks from local file into memory
function loadLocalChunksFromFile(): void {
  if (!fs.existsSync(LOCAL_CHUNKS_FILE)) {
    memoryChunks = new Map();
    return;
  }
  try {
    const raw = fs.readFileSync(LOCAL_CHUNKS_FILE, 'utf-8');
    const list: RagChunk[] = JSON.parse(raw);
    memoryChunks.clear();
    for (const chunk of list) {
      memoryChunks.set(chunk.id, chunk);
    }
    rebuildInvertedIndex();
    console.log(`[LocalRagEngine] 🚀 ${memoryChunks.size} adet yerel parça (chunk) belleğe yüklendi.`);
  } catch (err: any) {
    console.warn('[LocalRagEngine] Yerel parça dosyası okunamadı:', err.message);
  }
}

function saveLocalChunksToFile(): void {
  try {
    const list = Array.from(memoryChunks.values());
    fs.writeFileSync(LOCAL_CHUNKS_FILE, JSON.stringify(list, null, 2), 'utf-8');
  } catch (err: any) {
    console.error('[LocalRagEngine] Yerel parçalar kaydedilemedi:', err.message);
  }
}

function rebuildInvertedIndex(): void {
  invertedIndex.clear();
  for (const [id, chunk] of memoryChunks.entries()) {
    indexChunkTokens(chunk);
  }
}

function indexChunkTokens(chunk: RagChunk): void {
  const textToScan = `${chunk.title} ${chunk.discipline || ''} ${chunk.content}`;
  const tokens = cleanTextForTokens(textToScan);
  for (const t of tokens) {
    let set = invertedIndex.get(t);
    if (!set) {
      set = new Set();
      invertedIndex.set(t, set);
    }
    set.add(chunk.id);
  }
}

// ==============================================================================
// Batch Embedding Generator
// ==============================================================================
export async function generateGeminiEmbedding(text: string, apiKey?: string): Promise<number[] | null> {
  const customKey = apiKey || getGeminiKeys()[0];
  if (!customKey) return null;

  try {
    const client = new GoogleGenAI({ apiKey: customKey });
    const res = await client.models.embedContent({
      model: 'gemini-embedding-001',
      contents: [text],
      config: { outputDimensionality: 768 }
    });
    if (res.embeddings && res.embeddings.length > 0 && res.embeddings[0].values) {
      return res.embeddings[0].values;
    }
  } catch (err: any) {
    console.warn('[LocalRagEngine] Embedding üretimi hatası:', err.message);
  }
  return null;
}

export async function batchEmbedTexts(texts: string[]): Promise<Array<number[] | null>> {
  const client = getNextGeminiClient();
  if (!client) return texts.map(() => null);

  try {
    const res = await client.models.embedContent({
      model: 'gemini-embedding-001',
      contents: texts,
      config: { outputDimensionality: 768 }
    });
    if (res.embeddings && res.embeddings.length === texts.length) {
      return res.embeddings.map(e => e.values || null);
    }
  } catch (err: any) {
    console.warn('[LocalRagEngine] Batch embed hatası:', err.message);
  }
  return texts.map(() => null);
}

// Cosine similarity between two vectors
function cosineSimilarity(vecA: number[], vecB: number[]): number {
  if (vecA.length !== vecB.length) return 0;
  let dotProduct = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }
  if (normA === 0 || normB === 0) return 0;
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

// ==============================================================================
// 8 Data Sources Chunk Builders
// ==============================================================================

// 1. Çıkmış Sorular (past_question)
export function chunkPastQuestions(): RagChunk[] {
  const pqPath = path.resolve(DATA_DIR, 'pastQuestions.json');
  if (!fs.existsSync(pqPath)) return [];
  const list = JSON.parse(fs.readFileSync(pqPath, 'utf-8'));
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();

  for (const q of list) {
    const stem = (q.stem || q.reconstruction?.stem || q.rawQuestion?.stem || '').trim();
    if (!stem) continue;

    const opts = q.options || q.reconstruction?.options || q.rawQuestion?.options || [];
    const optLines = Array.isArray(opts)
      ? opts.map((o: any) => typeof o === 'string' ? o : `${o.label || o.key || ''}) ${o.text || ''}`).join('\n')
      : '';
    const claim = q.claimedAnswer || q.reconstruction?.correctAnswer || q.reconstruction?.correctOption || '';
    const expl = q.explanation || q.reconstruction?.explanation || '';

    const content = `[ÇIKMIŞ SINAV SORUSU]
Ders / Branş: ${q.discipline || 'Tıp'}
Kurul: ${q.committeeId || 'donem3-kurul1'}
Sınav Yılı: ${q.examYear || 'Geçmiş Sınav'}
Konu: ${q.topic || 'Kurul Sorusu'}
Soru Kökü:
${stem}

Seçenekler:
${optLines}

Doğru / Kabul Edilen Cevap: ${claim}
${expl ? `\nAkademik Açıklama & Mekanizma:\n${expl}` : ''}`.trim();

    const h = hashContent(content);
    chunks.push({
      id: `chunk-pq-${q.id || h.slice(0, 10)}`,
      documentId: q.id || `pq-${h.slice(0, 8)}`,
      documentType: 'past_question',
      committeeId: q.committeeId || 'donem3-kurul1',
      discipline: q.discipline || 'Tıp',
      title: `${q.discipline || 'Tıp'} - ${q.topic || 'Çıkmış Soru'} (${q.examYear || 'Çıkmış'})`,
      pageNumber: q.questionNumber || null,
      content,
      metadata: {
        examYear: q.examYear,
        claimedAnswer: claim,
        sourceFile: q.sourceFile,
        topic: q.topic,
        isAmbiguous: q.isAmbiguous,
        hasSlideRef: Boolean(q.matchedNoteTitle || q.lectureReference)
      },
      hash: h,
      createdAt: q.createdAt || now,
      updatedAt: q.updatedAt || now
    });
  }
  return chunks;
}

// 2. Eklenen / Aktif Sorular (active_question)
export function chunkActiveQuestions(): RagChunk[] {
  const qPath = path.resolve(DATA_DIR, 'questions.json');
  if (!fs.existsSync(qPath)) return [];
  const data = JSON.parse(fs.readFileSync(qPath, 'utf-8'));
  const list = data.questions || [];
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();

  for (const q of list) {
    const stem = (q.stem || q.reconstruction?.stem || q.rawQuestion?.stem || '').trim();
    if (!stem) continue;

    const opts = q.options || q.reconstruction?.options || [];
    const optLines = Array.isArray(opts)
      ? opts.map((o: any) => typeof o === 'string' ? o : `${o.label || o.key || ''}) ${o.text || ''}`).join('\n')
      : '';
    const claim = q.claimedAnswer || q.reconstruction?.correctAnswer || '';
    const expl = q.reconstruction?.explanation || '';

    const content = `[GÜNCEL TOPLANAN SINAV SORUSU]
Ders / Branş: ${q.discipline || 'Tıp'}
Kurul: ${q.committeeId || 'donem3-kurul1'}
Soru No: ${q.questionNumber || '?'}
Konu: ${q.topic || 'Aktif Soru'}
Soru Kökü:
${stem}

Seçenekler:
${optLines}

Doğru/İddia Edilen Cevap: ${claim}
${expl ? `\nÖğrenci & AI Açıklaması:\n${expl}` : ''}`.trim();

    const h = hashContent(content);
    chunks.push({
      id: `chunk-aq-${q.id || h.slice(0, 10)}`,
      documentId: q.id,
      documentType: 'active_question',
      committeeId: q.committeeId || 'donem3-kurul1',
      discipline: q.discipline || 'Tıp',
      title: `${q.discipline || 'Tıp'} - ${q.topic || 'Aktif Soru'} (Soru ${q.questionNumber || '?'})`,
      pageNumber: q.questionNumber || null,
      content,
      metadata: {
        status: q.status,
        claimedAnswer: claim,
        upvotes: q.upvotes || 0,
        tags: q.tags || []
      },
      hash: h,
      createdAt: q.createdAt || now,
      updatedAt: q.updatedAt || now
    });
  }
  return chunks;
}

// 3. Amfi Ders Notları & Slaytlar (lecture_slide)
export function chunkLectureNotes(): RagChunk[] {
  const lnPath = path.resolve(DATA_DIR, 'lecture_notes.json');
  if (!fs.existsSync(lnPath)) return [];
  const list = JSON.parse(fs.readFileSync(lnPath, 'utf-8'));
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();

  for (const note of list) {
    if (!note.pages || note.pages.length === 0) continue;
    for (const page of note.pages) {
      const pageText = (page.content || '').trim();
      if (pageText.length < 25) continue; // Skip empty slides

      const content = `[DERS SLAYTI NOTU]
Ders: ${note.discipline || 'Tıp'}
Sunum Başlığı: ${note.title || 'Ders Notu'}
Kurul: ${note.committeeId || 'donem3-kurul1'}
Slayt Numarası: #${page.pageNumber}
İçerik:
${pageText}`.trim();

      const h = hashContent(content);
      chunks.push({
        id: `chunk-slide-${note.id}-p${page.pageNumber}`,
        documentId: note.id,
        documentType: 'lecture_slide',
        committeeId: note.committeeId || 'donem3-kurul1',
        discipline: note.discipline || 'Tıp',
        title: `${note.title || 'Ders Notu'} (Slayt #${page.pageNumber})`,
        pageNumber: page.pageNumber,
        content,
        metadata: {
          noteId: note.id,
          totalSlides: note.totalSlides,
          keywords: page.keywords || [],
          source: note.source
        },
        hash: h,
        createdAt: note.createdAt || now,
        updatedAt: note.updatedAt || now
      });
    }
  }
  return chunks;
}

// 4. Ders Özetleri & Spot Notlar (summary)
export function chunkLectureSummaries(): RagChunk[] {
  const sumPath = path.resolve(DATA_DIR, 'lectureSummariesCatalog.json');
  if (!fs.existsSync(sumPath)) return [];
  const list = JSON.parse(fs.readFileSync(sumPath, 'utf-8'));
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();

  for (const item of list) {
    if (!item.content || item.content.length < 50) continue;

    // Split summary by sections (H2 ##)
    const sections = item.content.split(/\n(?=##\s+)/);
    let sectionIdx = 1;

    for (const sec of sections) {
      const trimmed = sec.trim();
      if (trimmed.length < 40) continue;

      const content = `[DERS ÖZETİ & SPOT BİLGİ]
Ders / Branş: ${item.discipline || 'Tıp'}
Konu / Başlık: ${item.title}
Kurul: ${item.committeeId || `donem3-kurul${item.kurul || 1}`}
Bölüm: #${sectionIdx}
Özet Metin:
${trimmed}`.trim();

      const h = hashContent(content);
      chunks.push({
        id: `chunk-sum-${item.id}-${sectionIdx}`,
        documentId: item.id,
        documentType: 'summary',
        committeeId: item.committeeId || `donem3-kurul${item.kurul || 1}`,
        discipline: item.discipline || 'Tıp',
        title: `${item.title} (Özet #${sectionIdx})`,
        pageNumber: sectionIdx,
        content,
        metadata: {
          fileName: item.fileName,
          keyPoints: item.keyPoints || []
        },
        hash: h,
        createdAt: now,
        updatedAt: now
      });
      sectionIdx++;
    }
  }
  return chunks;
}

// 5. Ses Transkriptleri (transcript)
export function chunkAudioTranscripts(): RagChunk[] {
  const transDir = path.resolve(DESKTOP_DATABASE_DIR, 'transcriptions');
  if (!fs.existsSync(transDir)) return [];
  const files = fs.readdirSync(transDir).filter(f => f.endsWith('.md'));
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();

  for (const file of files) {
    const fullPath = path.join(transDir, file);
    const text = fs.readFileSync(fullPath, 'utf-8');
    const paragraphs = text.split(/\n\s*\n/);
    let currentChunkText = '';
    let chunkIndex = 1;

    for (const para of paragraphs) {
      currentChunkText += para + '\n\n';
      if (currentChunkText.length >= 800) {
        const titleClean = file.replace(/_Transkript\.md|_KUSURSUZ\.md|\.md/g, '').replace(/_/g, ' ');
        const discipline = titleClean.toLowerCase().includes('halk')
          ? 'Halk Sağlığı'
          : titleClean.toLowerCase().includes('genetik')
          ? 'Tıbbi Genetik'
          : 'Tıp Dersi';

        const content = `[AMFİ SES KAYDI TRANSKRİPTİ]
Ders / Konu: ${titleClean}
Parça No: #${chunkIndex}
Hoca Sözlü Anlatımı:
${currentChunkText.trim()}`.trim();

        const h = hashContent(content);
        chunks.push({
          id: `chunk-tr-${file.slice(0, 12)}-${chunkIndex}`,
          documentId: file,
          documentType: 'transcript',
          committeeId: 'donem3-kurul1',
          discipline,
          title: `${titleClean} (Transkript #${chunkIndex})`,
          pageNumber: chunkIndex,
          content,
          metadata: { fileName: file },
          hash: h,
          createdAt: now,
          updatedAt: now
        });

        currentChunkText = '';
        chunkIndex++;
      }
    }
  }
  return chunks;
}

// 6. Kullanıcı Katkı & Yorumları (user_contribution)
export function chunkUserContributions(): RagChunk[] {
  const qPath = path.resolve(DATA_DIR, 'questions.json');
  if (!fs.existsSync(qPath)) return [];
  const data = JSON.parse(fs.readFileSync(qPath, 'utf-8'));
  const list = data.questions || [];
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();

  for (const q of list) {
    // A. Fragments (Öğrenci sınav hatırlamaları)
    if (Array.isArray(q.fragments) && q.fragments.length > 0) {
      for (const frag of q.fragments) {
        if (!frag.text || frag.text.length < 15) continue;
        const content = `[ÖĞRENCİ SINAV HATIRLAMASI & İPUCU]
İlgili Soru: ${q.discipline || 'Tıp'} - ${q.topic || 'Kurul Sorusu'} (Soru ${q.questionNumber || '?'})
Hatırlayan / Yazar: ${frag.author || 'Tıp Öğrencisi'}
Parça Türü: ${frag.type || 'İpucu'}
Öğrenci Notu:
${frag.text}`.trim();

        const h = hashContent(content);
        chunks.push({
          id: `chunk-frag-${frag.id || h.slice(0, 10)}`,
          documentId: q.id,
          documentType: 'user_contribution',
          committeeId: q.committeeId || 'donem3-kurul1',
          discipline: q.discipline || 'Tıp',
          title: `Öğrenci İpucu: ${q.topic || 'Soru Katkısı'} (${frag.author || 'Öğrenci'})`,
          content,
          metadata: {
            questionId: q.id,
            author: frag.author,
            fragmentType: frag.type,
            upvotes: frag.upvotes || 0
          },
          hash: h,
          createdAt: frag.timestamp || now,
          updatedAt: now
        });
      }
    }

    // B. Comments (Soru altı tartışmaları)
    if (Array.isArray(q.comments) && q.comments.length > 0) {
      for (const c of q.comments) {
        if (!c.text || c.text.length < 15) continue;
        const content = `[ÖĞRENCİ SORU YORUMU & TARTIŞMA]
İlgili Soru: ${q.discipline || 'Tıp'} - ${q.topic || 'Kurul Sorusu'}
Yorum Yapan: ${c.userName || 'Öğrenci'}
Yorum:
${c.text}`.trim();

        const h = hashContent(content);
        chunks.push({
          id: `chunk-comm-${c.id || h.slice(0, 10)}`,
          documentId: q.id,
          documentType: 'user_contribution',
          committeeId: q.committeeId || 'donem3-kurul1',
          discipline: q.discipline || 'Tıp',
          title: `Öğrenci Tartışması: ${q.topic || 'Soru Yorumu'}`,
          content,
          metadata: {
            questionId: q.id,
            userName: c.userName,
            likes: c.likes || 0
          },
          hash: h,
          createdAt: c.createdAt || now,
          updatedAt: now
        });
      }
    }
  }
  return chunks;
}

// 7. Yapay Zeka Düzeltmeleri & Revizyonları (ai_refinement)
export function chunkAiRefinements(): RagChunk[] {
  const pqPath = path.resolve(DATA_DIR, 'pastQuestions.json');
  if (!fs.existsSync(pqPath)) return [];
  const list = JSON.parse(fs.readFileSync(pqPath, 'utf-8'));
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();

  for (const q of list) {
    if (!q.reconstruction && !q.customRedactionPrompt) continue;

    const recon = q.reconstruction || {};
    const notes = recon.notesAndDiscrepancies || q.customRedactionPrompt || '';
    if (!notes && !recon.explanation) continue;

    const content = `[YAPAY ZEKA SORU DÜZELTMESİ & REDAKSİYON GEREKÇESİ]
Ders / Branş: ${q.discipline || 'Tıp'}
Soru Konusu: ${q.topic || 'Çıkmış Soru'}
Doğru Cevap: ${recon.correctAnswer || q.claimedAnswer || ''}
Düzenleme Gerekçesi / Amfi Notu Zeminlemesi:
${notes}

Yapay Zeka Tıbbi Çözüm Notu:
${recon.explanation || 'Açıklama belirtilmemiş.'}`.trim();

    const h = hashContent(content);
    chunks.push({
      id: `chunk-refine-${q.id}`,
      documentId: q.id,
      documentType: 'ai_refinement',
      committeeId: q.committeeId || 'donem3-kurul1',
      discipline: q.discipline || 'Tıp',
      title: `AI Düzeltme & Zeminleme: ${q.discipline} - ${q.topic}`,
      content,
      metadata: {
        questionId: q.id,
        confidenceScore: recon.confidenceScore || 95,
        customRedactedBy: q.customRedactedBy
      },
      hash: h,
      createdAt: q.customRedactedAt || recon.lastUpdated || now,
      updatedAt: now
    });
  }
  return chunks;
}

// 8. Yapay Zeka Soru Sohbetleri & Tartışmaları (ai_qa)
export function loadAiInteractions(): AiInteractionRecord[] {
  if (!fs.existsSync(AI_INTERACTIONS_FILE)) return [];
  try {
    return JSON.parse(fs.readFileSync(AI_INTERACTIONS_FILE, 'utf-8'));
  } catch (_) {
    return [];
  }
}

export function saveAiInteractions(interactions: AiInteractionRecord[]): void {
  try {
    fs.writeFileSync(AI_INTERACTIONS_FILE, JSON.stringify(interactions, null, 2), 'utf-8');
  } catch (err: any) {
    console.error('[LocalRagEngine] AI etkileşimleri kaydedilemedi:', err.message);
  }
}

export function chunkAiInteractions(): RagChunk[] {
  const interactions = loadAiInteractions();
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();

  for (const act of interactions) {
    const content = `[YAPAY ZEKA TIBBİ SORU-CEVAP & AÇIKLAMA]
Soru Bağlamı: ${act.discipline || 'Tıp'} - ${act.topic || 'Soru Analizi'}
Öğrencinin Sorusu / Talebi:
"${act.prompt}"

Yapay Zekanın Akademik Yanıtı & Mekanizma Açıklaması:
${act.response}`.trim();

    const h = hashContent(content);
    chunks.push({
      id: act.ragChunkId || `chunk-aiqa-${act.id}`,
      documentId: act.questionId || act.id,
      documentType: 'ai_qa',
      committeeId: act.committeeId || 'donem3-kurul1',
      discipline: act.discipline || 'Tıp',
      title: `AI Soru-Cevap: ${act.topic || 'Tıbbi Analiz'} ("${act.prompt.slice(0, 45)}...")`,
      content,
      metadata: {
        interactionId: act.id,
        questionId: act.questionId,
        interactionType: act.interactionType,
        userDisplayName: act.userDisplayName,
        upvotes: act.upvotes || 0
      },
      hash: h,
      createdAt: act.createdAt || now,
      updatedAt: now
    });
  }
  return chunks;
}

// ==============================================================================
// Ingest Single AI Interaction in Real-time (Chat Drawer, Optimizer, Redact)
// ==============================================================================
export async function recordAiInteraction(params: {
  questionId?: string;
  committeeId?: string;
  discipline?: string;
  topic?: string;
  interactionType?: 'chat_qa' | 'refinement' | 'redaction' | 'mnemonic' | 'trap_warning' | 'user_comment';
  userId?: string;
  userDisplayName?: string;
  prompt: string;
  response: string;
  contextSnapshot?: Record<string, any>;
  metadata?: Record<string, any>;
}): Promise<{ interaction: AiInteractionRecord; chunk: RagChunk }> {
  const id = `act-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`;
  const now = new Date().toISOString();
  const chunkId = `chunk-aiqa-${id}`;

  const interaction: AiInteractionRecord = {
    id,
    questionId: params.questionId,
    committeeId: params.committeeId || 'donem3-kurul1',
    discipline: params.discipline || 'Tıp',
    topic: params.topic || 'Soru İncelemesi',
    interactionType: params.interactionType || 'chat_qa',
    userId: params.userId,
    userDisplayName: params.userDisplayName || 'Tıp Öğrencisi',
    prompt: params.prompt.trim(),
    response: params.response.trim(),
    contextSnapshot: params.contextSnapshot || {},
    metadata: params.metadata || {},
    upvotes: 0,
    ragChunkId: chunkId,
    createdAt: now,
  };

  // 1. Save to local ai_interactions.json
  const currentList = loadAiInteractions();
  currentList.unshift(interaction);
  saveAiInteractions(currentList);

  // 2. Create and index local RAG chunk
  const chunkContent = `[YAPAY ZEKA TIBBİ SORU-CEVAP & AÇIKLAMA]
Soru Bağlamı: ${interaction.discipline} - ${interaction.topic}
Öğrencinin Sorusu / Talebi:
"${interaction.prompt}"

Yapay Zekanın Akademik Yanıtı & Mekanizma Açıklaması:
${interaction.response}`.trim();

  const h = hashContent(chunkContent);
  const chunk: RagChunk = {
    id: chunkId,
    documentId: interaction.questionId || id,
    documentType: 'ai_qa',
    committeeId: interaction.committeeId,
    discipline: interaction.discipline,
    title: `AI Soru-Cevap: ${interaction.topic} ("${interaction.prompt.slice(0, 45)}...")`,
    content: chunkContent,
    metadata: {
      interactionId: id,
      questionId: interaction.questionId,
      interactionType: interaction.interactionType,
      userDisplayName: interaction.userDisplayName,
      upvotes: 0
    },
    hash: h,
    createdAt: now,
    updatedAt: now
  };

  // Put in-memory index immediately
  memoryChunks.set(chunk.id, chunk);
  indexChunkTokens(chunk);
  saveLocalChunksToFile();

  // 3. Asynchronously generate embedding and mirror to Supabase
  setTimeout(async () => {
    try {
      const emb = await generateGeminiEmbedding(chunk.content);
      if (emb) {
        chunk.embedding = emb;
        memoryChunks.set(chunk.id, chunk);
        saveLocalChunksToFile();
      }

      const sb = getSupabase();
      if (sb) {
        // Upsert to rag_chunks
        await sb.from('rag_chunks').upsert([{
          id: chunk.id,
          document_id: chunk.documentId,
          document_type: chunk.documentType,
          committee_id: chunk.committeeId,
          discipline: chunk.discipline,
          title: chunk.title,
          page_number: null,
          content: chunk.content,
          metadata: chunk.metadata,
          embedding: emb || null
        }], { onConflict: 'id' });

        // Upsert to ai_question_interactions
        try {
          await sb.from('ai_question_interactions').upsert([{
            id: interaction.id,
            question_id: interaction.questionId,
            committee_id: interaction.committeeId,
            discipline: interaction.discipline,
            topic: interaction.topic,
            interaction_type: interaction.interactionType,
            user_id: interaction.userId,
            user_display_name: interaction.userDisplayName,
            prompt: interaction.prompt,
            response: interaction.response,
            context_snapshot: interaction.contextSnapshot,
            metadata: interaction.metadata,
            upvotes: interaction.upvotes,
            rag_chunk_id: chunkId,
            created_at: interaction.createdAt
          }], { onConflict: 'id' });
        } catch (_) {}
      }
    } catch (err: any) {
      console.warn('[LocalRagEngine] Async Cloud Sync uyarısı:', err.message);
    }
  }, 100);

  return { interaction, chunk };
}

// Upvote an AI interaction
export function upvoteAiInteraction(interactionId: string): boolean {
  const list = loadAiInteractions();
  const item = list.find(x => x.id === interactionId);
  if (!item) return false;

  item.upvotes = (item.upvotes || 0) + 1;
  saveAiInteractions(list);

  // Update in memory chunk if exists
  if (item.ragChunkId && memoryChunks.has(item.ragChunkId)) {
    const chunk = memoryChunks.get(item.ragChunkId)!;
    chunk.metadata = { ...chunk.metadata, upvotes: item.upvotes };
    memoryChunks.set(chunk.id, chunk);
    saveLocalChunksToFile();
  }

  // Update in Supabase
  const sb = getSupabase();
  if (sb) {
    try {
      sb.from('ai_question_interactions')
        .update({ upvotes: item.upvotes })
        .eq('id', interactionId)
        .then(() => {}, () => {});
    } catch (_) {}
  }
  return true;
}

// Fetch all interactions for a specific question
export function getInteractionsByQuestion(questionId: string): AiInteractionRecord[] {
  if (!questionId) return [];
  const list = loadAiInteractions();
  return list.filter(x => x.questionId === questionId);
}

// ==============================================================================
// Full Reindex & Auto-Indexing Workflow
// ==============================================================================
export async function runAutoChunking(options: { limit?: number; syncToCloud?: boolean } = {}): Promise<{
  totalChunks: number;
  byType: Record<string, number>;
  newlyIndexed: number;
}> {
  if (isIndexingInProgress) {
    return {
      totalChunks: memoryChunks.size,
      byType: getChunkCountsByType(),
      newlyIndexed: 0
    };
  }

  isIndexingInProgress = true;
  console.log('\n======================================================');
  console.log('🔄 [LocalRagEngine] Otomatik Çok Modlu Parçalama (Chunking) Başlatıldı');
  console.log('======================================================');

  try {
    const allChunks: RagChunk[] = [];

    // 1. Past questions
    const pq = chunkPastQuestions();
    console.log(`✓ 1/8 Çıkmış Sorular: ${pq.length} parça`);
    allChunks.push(...pq);

    // 2. Active questions
    const aq = chunkActiveQuestions();
    console.log(`✓ 2/8 Aktif Sorular: ${aq.length} parça`);
    allChunks.push(...aq);

    // 3. Lecture slides
    const ls = chunkLectureNotes();
    console.log(`✓ 3/8 Ders Slaytları: ${ls.length} sayfa/parça`);
    allChunks.push(...ls);

    // 4. Summaries & spots
    const sm = chunkLectureSummaries();
    console.log(`✓ 4/8 Ders Özetleri & Spotlar: ${sm.length} bölüm`);
    allChunks.push(...sm);

    // 5. Transcripts
    const tr = chunkAudioTranscripts();
    console.log(`✓ 5/8 Ses Transkriptleri: ${tr.length} parça`);
    allChunks.push(...tr);

    // 6. User contributions
    const uc = chunkUserContributions();
    console.log(`✓ 6/8 Kullanıcı Katkı & Yorumları: ${uc.length} parça`);
    allChunks.push(...uc);

    // 7. AI Refinements
    const ar = chunkAiRefinements();
    console.log(`✓ 7/8 AI Düzeltmeleri & Revizyonları: ${ar.length} parça`);
    allChunks.push(...ar);

    // 8. AI Chat interactions
    const aiq = chunkAiInteractions();
    console.log(`✓ 8/8 AI Soru Sohbetleri: ${aiq.length} parça`);
    allChunks.push(...aiq);

    let newlyIndexed = 0;
    for (const chunk of allChunks) {
      const existing = memoryChunks.get(chunk.id);
      if (!existing || existing.hash !== chunk.hash) {
        // Keep existing embedding if hash did not change
        if (existing?.embedding && existing.hash === chunk.hash) {
          chunk.embedding = existing.embedding;
        }
        memoryChunks.set(chunk.id, chunk);
        newlyIndexed++;
      }
    }

    rebuildInvertedIndex();
    saveLocalChunksToFile();

    console.log(`\n🎉 Toplam Yerel Parça Sayısı: ${memoryChunks.size} (${newlyIndexed} yeni/güncellenen)`);

    // Asynchronously push to Supabase if requested
    if (options.syncToCloud !== false) {
      setTimeout(() => {
        syncPendingChunksToCloud(options.limit || 100).catch(err => {
          console.warn('[LocalRagEngine] Cloud sync arka plan hatası:', err.message);
        });
      }, 500);
    }

    return {
      totalChunks: memoryChunks.size,
      byType: getChunkCountsByType(),
      newlyIndexed
    };
  } finally {
    isIndexingInProgress = false;
  }
}

export function getChunkCountsByType(): Record<string, number> {
  const counts: Record<string, number> = {};
  for (const chunk of memoryChunks.values()) {
    counts[chunk.documentType] = (counts[chunk.documentType] || 0) + 1;
  }
  return counts;
}

// Background sync to Supabase with Gemini embeddings
async function syncPendingChunksToCloud(maxCount: number = 100): Promise<void> {
  const sb = getSupabase();
  if (!sb) return;

  const chunksWithoutCloud: RagChunk[] = [];
  for (const chunk of memoryChunks.values()) {
    if (!chunk.embedding) {
      chunksWithoutCloud.push(chunk);
    }
    if (chunksWithoutCloud.length >= maxCount) break;
  }

  if (chunksWithoutCloud.length === 0) return;

  console.log(`[LocalRagEngine] ☁️ ${chunksWithoutCloud.length} parça Supabase ve Gemini embedding için işleniyor...`);
  const BATCH_SIZE = 10;

  for (let i = 0; i < chunksWithoutCloud.length; i += BATCH_SIZE) {
    const batch = chunksWithoutCloud.slice(i, i + BATCH_SIZE);
    const texts = batch.map(b => b.content);

    try {
      const embeddings = await batchEmbedTexts(texts);
      const rows = batch.map((item, idx) => {
        const emb = embeddings[idx];
        if (emb) {
          item.embedding = emb;
          memoryChunks.set(item.id, item);
        }
        return {
          id: item.id,
          document_id: item.documentId,
          document_type: item.documentType,
          committee_id: item.committeeId,
          discipline: item.discipline,
          title: item.title,
          page_number: item.pageNumber || null,
          content: item.content,
          metadata: item.metadata,
          embedding: emb || null
        };
      });

      await sb.from('rag_chunks').upsert(rows, { onConflict: 'id' });
    } catch (e: any) {
      console.warn('[LocalRagEngine] Batch cloud push uyarısı:', e.message);
    }
  }

  saveLocalChunksToFile();
  console.log(`[LocalRagEngine] ✓ Cloud eşitleme grubu tamamlandı.`);
}

// ==============================================================================
// Ultra-Fast Unified Local & Hybrid Search (< 5ms)
// ==============================================================================
export async function searchLocalRag(
  queryText: string,
  options: {
    committeeId?: string;
    discipline?: string;
    documentTypes?: RagDocumentType[];
    limit?: number;
    queryEmbedding?: number[];
  } = {}
): Promise<RagSearchResult[]> {
  const limit = options.limit || 5;
  const cleanTokens = cleanTextForTokens(queryText);
  if (cleanTokens.length === 0 && !options.queryEmbedding) return [];

  // 1. Gather candidate chunk IDs using inverted index
  const candidateScores = new Map<string, number>();

  for (const token of cleanTokens) {
    const chunkIds = invertedIndex.get(token);
    if (chunkIds) {
      for (const id of chunkIds) {
        candidateScores.set(id, (candidateScores.get(id) || 0) + 1);
      }
    }
  }

  // 2. Score and rank candidates
  const scoredResults: Array<{ chunk: RagChunk; score: number; similarity: number }> = [];
  const normalizedQuery = queryText.toLowerCase().replace(/[^a-z0-9ğüşıöç]/gi, ' ').trim();

  for (const [id, tokenHits] of candidateScores.entries()) {
    const chunk = memoryChunks.get(id);
    if (!chunk) continue;

    // Filters
    if (options.committeeId && chunk.committeeId && chunk.committeeId !== options.committeeId) {
      continue;
    }
    if (options.discipline && chunk.discipline && !chunk.discipline.toLowerCase().includes(options.discipline.toLowerCase())) {
      continue;
    }
    if (options.documentTypes && options.documentTypes.length > 0 && !options.documentTypes.includes(chunk.documentType)) {
      continue;
    }

    let score = (tokenHits / Math.max(1, cleanTokens.length)) * 50;

    // Exact phrase match bonus
    const lowerContent = chunk.content.toLowerCase();
    if (lowerContent.includes(normalizedQuery)) {
      score += 40;
    }

    // High yield document types bonus (past questions & verified summaries & AI QAs)
    if (chunk.documentType === 'past_question' || chunk.documentType === 'ai_qa') {
      score += 10;
    }

    // Cosine similarity if embeddings are present
    let sim = 0;
    if (options.queryEmbedding && chunk.embedding) {
      sim = cosineSimilarity(options.queryEmbedding, chunk.embedding);
      score += sim * 40;
    }

    scoredResults.push({ chunk, score, similarity: sim });
  }

  scoredResults.sort((a, b) => b.score - a.score);
  const topSlice = scoredResults.slice(0, limit);

  return topSlice.map(({ chunk, score, similarity }) => {
    // Generate clean snippet around highest match
    const snippet = chunk.content.length > 350
      ? chunk.content.slice(0, 350) + '...'
      : chunk.content;

    return {
      id: chunk.id,
      documentId: chunk.documentId,
      documentType: chunk.documentType,
      committeeId: chunk.committeeId,
      discipline: chunk.discipline,
      title: chunk.title,
      pageNumber: chunk.pageNumber,
      content: chunk.content,
      metadata: chunk.metadata,
      similarity: similarity || Math.min(1.0, score / 100),
      matchScore: score,
      snippet,
      source: 'local'
    };
  });
}

// ==============================================================================
// Initialize Engine on Boot
// ==============================================================================
export function initLocalRagEngine(): void {
  if (isInitialized) return;
  isInitialized = true;

  console.log('[LocalRagEngine] 🚀 Başlatılıyor...');
  loadLocalChunksFromFile();

  // If local chunks are empty, trigger initial chunking in background
  if (memoryChunks.size === 0) {
    console.log('[LocalRagEngine] Yerel parçalar henüz oluşturulmamış, ilk tarama başlatılıyor...');
    setTimeout(() => {
      runAutoChunking({ syncToCloud: true }).catch(err => {
        console.error('[LocalRagEngine] Başlangıç chunking hatası:', err.message);
      });
    }, 3000);
  } else {
    console.log(`[LocalRagEngine] ✓ Hazır: Toplam ${memoryChunks.size} parça bellekte ve anında aranabilir.`);
  }

  // Watch data folder for changes (debounced auto-reindex)
  let changeDebounce: NodeJS.Timeout | null = null;
  if (fs.existsSync(DATA_DIR)) {
    try {
      fs.watch(DATA_DIR, (eventType, filename) => {
        if (!filename) return;
        if (filename === 'local_rag_chunks.json' || filename === 'rag_indexing_manifest.json') return;
        if (filename.endsWith('.json')) {
          if (changeDebounce) clearTimeout(changeDebounce);
          changeDebounce = setTimeout(() => {
            console.log(`[LocalRagEngine] 📂 Veri dosyasında değişiklik tespit edildi (${filename}), yerel indeks güncelleniyor...`);
            runAutoChunking({ syncToCloud: false }).catch(() => {});
          }, 5000);
        }
      });
    } catch (_) {}
  }
}
