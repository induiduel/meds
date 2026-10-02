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
import { loadDeepSeekContributions } from './deepseekDataService.ts';

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
  | 'ai_qa'
  | 'deepseek_contribution';

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

// Stopwords to filter out from auto-keyword index (expanded medical question terms)
const TURKISH_STOPWORDS = new Set([
  've', 'ile', 'veya', 'için', 'gibi', 'kadar', 'daha', 'olan', 'olarak', 'bunun',
  'buna', 'şekilde', 'olarak', 'üzere', 'bir', 'bu', 'şu', 'o', 'her', 'tüm', 'bütün',
  'sayfa', 'slayt', 'bölüm', 'ders', 'notu', 'konu', 'ünite', 'tablo', 'şekil', 'görsel',
  'hangisidir', 'aşağıdakilerden', 'hangisi', 'nedir', 'aşağıdaki', 'vardır', 'yoktur',
  'doğrudur', 'yanlıştır', 'göre', 'ilgili', 'ilişkin', 'arasında', 'yer', 'alır', 'almaz',
  'belirtilmiştir', 'örnektir', 'adlandırılır', 'kabul', 'edilen', 'bulunur', 'bulunmaz',
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
// In-Memory Index State (High-Performance BM25 Engine)
// ==============================================================================
let memoryChunks: Map<string, RagChunk> = new Map();
// token -> Map<chunkId, termFrequency> for exact BM25 calculation
let invertedIndex: Map<string, Map<string, number>> = new Map();
let docLengths: Map<string, number> = new Map();
let avgDocLength = 110;
let isInitialized = false;
let isIndexingInProgress = false;
let saveDebounceTimer: NodeJS.Timeout | null = null;
let isSavingToFile = false;

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

    // Also merge real-time AI interactions from ai_interactions.json
    try {
      const interactions = loadAiInteractions();
      for (const act of interactions) {
        const cId = act.ragChunkId || `chunk-aiqa-${act.id}`;
        if (!memoryChunks.has(cId)) {
          const chunkContent = `[YAPAY ZEKA TIBBİ SORU-CEVAP & AÇIKLAMA]
Soru Bağlamı: ${act.discipline || 'Tıp'} - ${act.topic || 'Soru Analizi'}
Öğrencinin Sorusu / Talebi:
"${act.prompt}"

Yapay Zekanın Akademik Yanıtı & Mekanizma Açıklaması:
${act.response}`.trim();

          memoryChunks.set(cId, {
            id: cId,
            documentId: act.questionId || act.id,
            documentType: 'ai_qa',
            committeeId: act.committeeId || 'donem3-kurul1',
            discipline: act.discipline || 'Tıp',
            title: `AI Soru-Cevap: ${act.topic || 'Tıbbi Analiz'} ("${act.prompt.slice(0, 45)}...")`,
            content: chunkContent,
            metadata: {
              interactionId: act.id,
              questionId: act.questionId,
              interactionType: act.interactionType,
              userDisplayName: act.userDisplayName,
              upvotes: act.upvotes || 0
            },
            hash: hashContent(chunkContent),
            createdAt: act.createdAt || new Date().toISOString(),
            updatedAt: act.createdAt || new Date().toISOString()
          });
        }
      }
    } catch (_) {}

    rebuildInvertedIndex();
    console.log(`[LocalRagEngine] 🚀 ${memoryChunks.size} adet yerel parça (chunk) belleğe yüklendi ve BM25 indeksi oluşturuldu.`);
  } catch (err: any) {
    console.warn('[LocalRagEngine] Yerel parça dosyası okunamadı:', err.message);
  }
}

// Asynchronous, debounced, compact disk serialization (avoids event loop blocking)
export async function saveLocalChunksToFile(forceImmediate: boolean = false): Promise<void> {
  if (saveDebounceTimer) {
    clearTimeout(saveDebounceTimer);
    saveDebounceTimer = null;
  }

  const doWrite = async () => {
    if (isSavingToFile) return;
    isSavingToFile = true;
    try {
      const list = Array.from(memoryChunks.values());
      // Compact JSON without 2-space indentation saves ~35MB disk space and reduces I/O by 80%
      const jsonStr = JSON.stringify(list);
      await fs.promises.writeFile(LOCAL_CHUNKS_FILE, jsonStr, 'utf-8');
      console.log(`[LocalRagEngine] 💾 ${list.length} parça diskte güncellendi (${Math.round(jsonStr.length / 1024 / 1024)} MB).`);
    } catch (err: any) {
      console.error('[LocalRagEngine] Yerel parçalar kaydedilemedi:', err.message);
    } finally {
      isSavingToFile = false;
    }
  };

  if (forceImmediate) {
    await doWrite();
  } else {
    saveDebounceTimer = setTimeout(doWrite, 2500);
  }
}

function rebuildInvertedIndex(): void {
  invertedIndex.clear();
  docLengths.clear();
  let totalDocLen = 0;
  for (const chunk of memoryChunks.values()) {
    indexChunkTokens(chunk);
    totalDocLen += (docLengths.get(chunk.id) || 0);
  }
  avgDocLength = memoryChunks.size > 0 ? totalDocLen / memoryChunks.size : 110;
}

function indexChunkTokens(chunk: RagChunk): void {
  // Boost title and discipline by repeating in text representation
  const textToScan = `${chunk.title} ${chunk.title} ${chunk.discipline || ''} ${chunk.content}`;
  const tokens = cleanTextForTokens(textToScan);
  docLengths.set(chunk.id, tokens.length);

  const freqMap = new Map<string, number>();
  for (const t of tokens) {
    freqMap.set(t, (freqMap.get(t) || 0) + 1);
  }

  for (const [t, freq] of freqMap.entries()) {
    let posting = invertedIndex.get(t);
    if (!posting) {
      posting = new Map<string, number>();
      invertedIndex.set(t, posting);
    }
    posting.set(chunk.id, freq);
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
      const rawContent = (page.content || '').trim();
      const repaired = (page.repairedContent || '').trim();
      const pageText = repaired 
        ? (rawContent.length >= 25 ? `${rawContent}\n\n${repaired}` : repaired)
        : rawContent;
      if (pageText.length < 25) continue; // Skip truly empty slides

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

// 9. DeepSeek Düzenlenmiş & Katkı Verileri (deepseek_contribution)
export function chunkDeepSeekData(): RagChunk[] {
  const items = loadDeepSeekContributions();
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();

  for (const item of items) {
    const content = item.content || '';
    if (content.length < 20) continue;
    const h = item.hash || hashContent(content);

    chunks.push({
      id: `chunk-ds-${item.id || h.slice(0, 10)}`,
      documentId: item.id,
      documentType: 'deepseek_contribution',
      committeeId: item.committeeId || 'donem3-kurul1',
      discipline: item.discipline || 'Tıp',
      title: `${item.title} [DeepSeek Katkısı]`,
      pageNumber: undefined,
      content,
      metadata: {
        source: 'deepseek',
        contributor: 'DeepSeek AI',
        isContribution: true,
        attributionBadge: 'DeepSeek Katkısı',
        itemType: item.itemType,
        sourceFile: item.metadata?.sourceFile,
        topic: item.topic
      },
      hash: h,
      createdAt: item.createdAt || now,
      updatedAt: item.updatedAt || now
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

  // 3. Asynchronously generate embedding and mirror to Supabase
  setTimeout(async () => {
    try {
      const emb = await generateGeminiEmbedding(chunk.content);
      if (emb) {
        chunk.embedding = emb;
        memoryChunks.set(chunk.id, chunk);
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
    console.log(`✓ 8/9 AI Soru Sohbetleri: ${aiq.length} parça`);
    allChunks.push(...aiq);

    // 9. DeepSeek Katkı & Düzenlenmiş Verileri
    const dsc = chunkDeepSeekData();
    console.log(`✓ 9/9 DeepSeek Katkıları: ${dsc.length} parça`);
    allChunks.push(...dsc);

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
// Ultra-Fast Unified Local & Hybrid BM25 Search (< 5ms)
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
  if (memoryChunks.size === 0) {
    loadLocalChunksFromFile();
  }
  const limit = options.limit || 5;
  const cleanTokens = cleanTextForTokens(queryText);
  if (cleanTokens.length === 0 && !options.queryEmbedding) return [];

  const N = memoryChunks.size || 1;
  const k1 = 1.2;
  const b = 0.75;
  const avgdl = avgDocLength || 110;

  // 1. Calculate IDF for each query token present in the index
  const tokenInfo: Array<{ token: string; idf: number; postings: Map<string, number> }> = [];
  for (const t of cleanTokens) {
    const postings = invertedIndex.get(t);
    if (postings && postings.size > 0) {
      const df = postings.size;
      const idf = Math.log(1 + (N - df + 0.5) / (df + 0.5));
      tokenInfo.push({ token: t, idf, postings });
    }
  }

  if (tokenInfo.length === 0 && !options.queryEmbedding) return [];

  // Sort by IDF descending: most discriminating / rare medical terms first
  tokenInfo.sort((x, y) => y.idf - x.idf);
  // Optimization: Prune query tokens to top 6 most informative terms (highest IDF) for ultra-fast evaluation (< 5ms)
  const tokensToScore = tokenInfo.slice(0, 6);

  // 2. Accumulate candidate BM25 scores
  const candidateScores = new Map<string, number>();
  const matchedTokensCount = new Map<string, number>();

  for (const { idf, postings } of tokensToScore) {
    for (const [chunkId, tf] of postings.entries()) {
      const docLen = docLengths.get(chunkId) || avgdl;
      const tfNorm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (docLen / avgdl)));
      const termScore = idf * tfNorm;

      candidateScores.set(chunkId, (candidateScores.get(chunkId) || 0) + termScore);
      matchedTokensCount.set(chunkId, (matchedTokensCount.get(chunkId) || 0) + 1);
    }
  }

  // 3. Score and rank candidates
  const scoredResults: Array<{ chunk: RagChunk; score: number; similarity: number }> = [];
  const normalizedQuery = queryText.toLowerCase().replace(/[^a-z0-9ğüşıöç]/gi, ' ').trim();

  for (const [id, bmScore] of candidateScores.entries()) {
    const chunk = memoryChunks.get(id);
    if (!chunk) continue;

    let finalScore = bmScore;

    // Committee and Discipline Relevance Boosts
    if (options.committeeId && chunk.committeeId) {
      if (chunk.committeeId === options.committeeId) {
        finalScore += 20;
      }
    }
    if (options.discipline && chunk.discipline) {
      if (chunk.discipline.toLowerCase().includes(options.discipline.toLowerCase())) {
        finalScore += 25;
      }
    }
    if (options.documentTypes && options.documentTypes.length > 0 && !options.documentTypes.includes(chunk.documentType)) {
      continue;
    }

    // Term coordination boost (chunks matching multiple high-yield query terms)
    const matchCount = matchedTokensCount.get(id) || 1;
    if (matchCount > 1) {
      finalScore *= (1 + 0.25 * (matchCount - 1));
    }

    // Exact phrase match bonus
    const lowerContent = chunk.content.toLowerCase();
    if (lowerContent.includes(normalizedQuery)) {
      finalScore += 25;
    }

    // High yield document types bonus (collected DeepSeek data is top priority ground-truth!)
    if (chunk.documentType === 'deepseek_contribution') {
      finalScore += 25; // Top priority: collected data pool is referenced first!
    } else if (chunk.documentType === 'past_question') {
      finalScore += 15; // Past exam questions
    } else if (chunk.documentType === 'ai_refinement') {
      finalScore += 10;
    } else if (chunk.documentType === 'summary') {
      finalScore += 8;
    } else if (chunk.documentType === 'lecture_slide') {
      finalScore += 5;
    }

    // Cosine similarity if embeddings are present
    let sim = 0;
    if (options.queryEmbedding && chunk.embedding) {
      sim = cosineSimilarity(options.queryEmbedding, chunk.embedding);
      finalScore += sim * 30;
    }

    scoredResults.push({ chunk, score: finalScore, similarity: sim });
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

  // Watch data folder for changes (ONLY core course content files, strictly ignore runtime state/log files!)
  const WATCHED_CONTENT_FILES = new Set([
    'pastQuestions.json',
    'lecture_notes.json',
    'lectureSummariesCatalog.json',
    'questions.json'
  ]);

  let changeDebounce: NodeJS.Timeout | null = null;
  if (fs.existsSync(DATA_DIR)) {
      const watcher = fs.watch(DATA_DIR, (eventType, filename) => {
        if (!filename) return;
        // Strictly ignore everything other than the 4 core content files
        if (!WATCHED_CONTENT_FILES.has(filename)) return;

        if (changeDebounce) clearTimeout(changeDebounce);
        changeDebounce = setTimeout(() => {
          console.log(`[LocalRagEngine] 📂 Çekirdek müfredat dosyasında değişiklik tespit edildi (${filename}), yerel indeks güncelleniyor...`);
          runAutoChunking({ syncToCloud: false }).catch(() => {});
        }, 15000); // 15s debounce to prevent rebuild storms
        changeDebounce.unref();
      });
      watcher.unref(); // Allows node process to exit naturally when tasks complete
  }
}
