/**
 * ==============================================================================
 * MeDSor Local & Hybrid RAG Engine (localRagEngine.ts)
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
import { latestReviews, normalizeKurul } from './phase14Overlay';
import { mergedInto } from './questionMerge';
import { applyCleanOverlay } from './lectureCleanOverlay.ts';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { GoogleGenAI } from '@google/genai';
import { pgDb } from './pgDb';
import { loadDeepSeekContributions } from './deepseekDataService.ts';
import { foldTurkish as foldTrUtil, FastFuzzyVocab } from '../utils/fuzzyMatching.ts';
import { KIND_LABEL, factPlain, normalizeDisease, sectionTexts, sectionTitle } from './diseaseModel.ts';
import type { DiseaseSectionId } from '../types/disease';

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
  | 'deepseek_contribution'
  | 'gemini_v3_question'
  | 'gemini_v3_lecture'
  | 'gemini_v3_term'
  | 'ornek_question'
  | 'deck_slide'
  | 'glossary_term'
  | 'disease';

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
  'the', 'and', 'for', 'with', 'from', 'that', 'this', 'are', 'was',
  // Phrases students use when describing a remembered exam question
  'soru', 'sorusu', 'soruldu', 'sorulmuş', 'sorulmuştu', 'sordu', 'sorular', 'çıktı', 'çıkmış', 'çıkmıştı',
  'geldi', 'gelmişti', 'vardı', 'sınav', 'sınavda', 'hakkında', 'alakalı', 'dair', 'şey', 'galiba', 'sanırım'
]);

// Turkish is agglutinative ("böbrek", "böbreğin", "böbrekte"). A fixed 5-char prefix (F5 stemming)
// is a cheap, well-known stemmer for Turkish retrieval. Measured on 300 past questions: full word +
// stem beats stem-only and word-only (see CLAUDE.md "Retrieval").
const STEM_LENGTH = 5;

function hashContent(content: string): string {
  return crypto.createHash('md5').update(content.trim()).digest('hex');
}

// Fold Turkish characters so "böbrek", "bobrek", "IgE" and "ige" all match:
// students often type without Turkish characters.
export function foldTurkish(text: string): string {
  return foldTrUtil(text);
}
const FOLDED_STOPWORDS = new Set(Array.from(TURKISH_STOPWORDS, (w) => foldTurkish(w)));

function cleanTextForTokens(text: string): string[] {
  return foldTurkish(text)
    .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"'’“”…\[\]<>|\\+]/g, ' ')
    .split(/\s+/)
    .map(w => w.trim())
    .filter(w => w.length >= 3 && !FOLDED_STOPWORDS.has(w))
    // Emit the full word (precision for exact terms) plus its stem (recall across suffixes).
    // The '*' keeps stems from colliding with real 5-letter words.
    .flatMap(w => (w.length > STEM_LENGTH ? [w, w.slice(0, STEM_LENGTH) + '*'] : [w]));
}

// Postgres (meds-pg): rag_chunks + ai_question_interactions kopyası. Yalnız sunucu sürecinde.
function getSupabase() {
  return pgDb;
}

// Gemini Key Pool with Rotation
function getGeminiKeys(): string[] {
  return [
    process.env.GEMINI_API_KEY,
    ...Object.keys(process.env)
      .filter((n) => /^GEMINI_FREE_KEY_\d+$/.test(n))
      .sort((a, b) => Number(a.slice(16)) - Number(b.slice(16)))
      .map((n) => process.env[n]),
    process.env.MEDS_FREE_ONLY !== '0' ? undefined : process.env.GEMINI_BILLED_KEY, // yalnız ücretsiz anahtarlar
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
// Sıkıştırılmış ters dizin: terim -> (belge no, terim sıklığı) tipli dizileri. Eski iç içe
// Map<terim, Map<parçaId, tf>> 73k parçada ~1 GB tutuyor, yeniden kurulumda iki kopya bir arada
// 2 GB yığın tavanını aşıp sunucuyu çökertiyordu (2026-10-13). Belge no -> parça kimliği docIds'te.
type Postings = { docs: Int32Array; tfs: Uint16Array };
let invertedIndex: Map<string, Postings> = new Map();
let docIds: string[] = [];
let docLens: Uint32Array = new Uint32Array(0);
// Dizin kurulduktan sonra tek tek eklenen parçalar (AI etkileşimleri); bir sonraki kurulumda ana dizine geçer
let pendingIndex: Map<string, Map<string, number>> = new Map();
let pendingLengths: Map<string, number> = new Map();
let fuzzyVocab = new FastFuzzyVocab();
let avgDocLength = 110;

function termDf(t: string): number {
  return (invertedIndex.get(t)?.docs.length || 0) + (pendingIndex.get(t)?.size || 0);
}
function hasTerm(t: string): boolean {
  return invertedIndex.has(t) || pendingIndex.has(t);
}
let isInitialized = false;
let isIndexingInProgress = false;
let saveDebounceTimer: NodeJS.Timeout | null = null;
let isSavingToFile = false;

// Açılış yükü (108MB, ~57k parça) olay döngüsünü kilitlemesin: dosya eşzamansız okunur, indeks
// dilimler halinde kurulur. Arama bu söz bitene dek bekler; diğer istekler beklemeden yanıtlanır.
let loadPromise: Promise<void> | null = null;
let indexReady = false;
function ensureLoaded(): Promise<void> {
  if (!loadPromise) loadPromise = loadLocalChunksFromFile();
  return loadPromise;
}

// Her ~20 ms işten sonra olay döngüsüne nefes aldırır
const SLICE_MS = 20;
const yieldToLoop = () => new Promise<void>((resolve) => setImmediate(resolve));
function makeSlicer() {
  let last = performance.now();
  return async () => {
    if (performance.now() - last < SLICE_MS) return;
    await yieldToLoop();
    last = performance.now();
  };
}

// Load stored chunks from local file into memory
async function loadLocalChunksFromFile(): Promise<void> {
  if (!fs.existsSync(LOCAL_CHUNKS_FILE)) {
    memoryChunks = new Map();
    indexReady = true;
    return;
  }
  try {
    const raw = await fs.promises.readFile(LOCAL_CHUNKS_FILE, 'utf-8');
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

    await rebuildInvertedIndex();
    console.log(`[LocalRagEngine] 🚀 ${memoryChunks.size} adet yerel parça (chunk) belleğe yüklendi ve BM25 indeksi oluşturuldu.`);
  } catch (err: any) {
    console.warn('[LocalRagEngine] Yerel parça dosyası okunamadı:', err.message);
  }
  indexReady = true;
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

// Yeni indeks ayrı yapılarda dilim dilim kurulur, sonunda tek adımda yerine konur; kurulum sürerken
// aramalar eski indeksi kullanır. Daha yenisi başlarsa eski kurulum bırakılır.
let rebuildSeq = 0;
async function rebuildInvertedIndex(): Promise<void> {
  const seq = ++rebuildSeq;
  // Kurulum sırasında terim başına [belgeNo, tf, belgeNo, tf, ...] düz dizisi tutulur
  const build: Map<string, number[]> = new Map();
  const ids: string[] = [];
  const lens: number[] = [];
  const slice = makeSlicer();
  const addDoc = (chunk: RagChunk) => {
    const docNo = ids.length;
    ids.push(chunk.id);
    const freq = chunkTermFreqs(chunk);
    let len = 0;
    for (const [t, f] of freq) {
      len += f;
      let arr = build.get(t);
      if (!arr) { arr = []; build.set(t, arr); }
      arr.push(docNo, f);
    }
    lens.push(len);
  };
  const seen = new Set<string>();
  for (const chunk of Array.from(memoryChunks.values())) {
    seen.add(chunk.id);
    addDoc(chunk);
    await slice();
    if (seq !== rebuildSeq) return;
  }
  // Kurulum sırasında eklenen parçalar (ör. yeni AI etkileşimi) da yeni indekse girsin
  for (const chunk of memoryChunks.values()) {
    if (!seen.has(chunk.id)) { seen.add(chunk.id); addDoc(chunk); }
  }

  // Tipli dizilere dönüştür; dönüştürülen düz dizi hemen bırakılır (tepe bellek düşük kalır)
  const nextIndex: Map<string, Postings> = new Map();
  const nextVocab = new FastFuzzyVocab();
  for (const [t, arr] of build) {
    const n = arr.length >> 1;
    const docs = new Int32Array(n);
    const tfs = new Uint16Array(n);
    for (let k = 0, m = 0; k < n; k++, m += 2) { docs[k] = arr[m]; tfs[k] = Math.min(arr[m + 1], 65535); }
    nextIndex.set(t, { docs, tfs });
    build.delete(t);
    if (!t.endsWith('*') && t.length >= 4) nextVocab.add(t);
    await slice();
    if (seq !== rebuildSeq) return;
  }
  let totalDocLen = 0;
  for (const l of lens) totalDocLen += l;

  invertedIndex = nextIndex;
  docIds = ids;
  docLens = Uint32Array.from(lens);
  // Kurulumdan sonra eklenenler bekleyen dizinde kalır; kurulumda olanlar oradan çıkar
  if (pendingLengths.size) {
    const nextPending: Map<string, Map<string, number>> = new Map();
    const nextPendingLens: Map<string, number> = new Map();
    for (const [id, l] of pendingLengths) if (!seen.has(id)) nextPendingLens.set(id, l);
    if (nextPendingLens.size) {
      for (const [t, posting] of pendingIndex) {
        for (const [id, f] of posting) {
          if (!nextPendingLens.has(id)) continue;
          let p = nextPending.get(t);
          if (!p) { p = new Map(); nextPending.set(t, p); }
          p.set(id, f);
        }
      }
    }
    pendingIndex = nextPending;
    pendingLengths = nextPendingLens;
  }
  fuzzyVocab = nextVocab;
  avgDocLength = ids.length > 0 ? totalDocLen / ids.length : 110;
}

function chunkTermFreqs(chunk: RagChunk): Map<string, number> {
  // Boost title and discipline by repeating in text representation
  const textToScan = `${chunk.title} ${chunk.title} ${chunk.discipline || ''} ${chunk.content}`;
  const freqMap = new Map<string, number>();
  for (const t of cleanTextForTokens(textToScan)) {
    freqMap.set(t, (freqMap.get(t) || 0) + 1);
  }
  return freqMap;
}

// Dizin kurulduktan sonra gelen tek parçayı bekleyen dizine ekler (aramada ana dizinle birleşir)
function indexChunkTokens(chunk: RagChunk): void {
  const freq = chunkTermFreqs(chunk);
  let len = 0;
  for (const [t, f] of freq) {
    len += f;
    let posting = pendingIndex.get(t);
    if (!posting) { posting = new Map(); pendingIndex.set(t, posting); }
    posting.set(chunk.id, f);
    if (!t.endsWith('*') && t.length >= 4 && !invertedIndex.has(t)) fuzzyVocab.add(t);
  }
  pendingLengths.set(chunk.id, len);
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

// Bir parçalama turunda pastQuestions.json (~90 MB) yalnız bir kez ayrıştırılır (çıkmış + AI düzeltmeleri)
let pastQuestionsRunCache: { mtimeMs: number; list: any[] } | null = null;
// Sunucu süreci listeyi zaten bellekte tutuyorsa (getPastQuestionsDb) ikinci kopya ayrıştırılmaz
let pastQuestionsProvider: (() => any[]) | null = null;
export function setPastQuestionsProvider(fn: (() => any[]) | null): void {
  pastQuestionsProvider = fn;
}
function readPastQuestionsList(): any[] | null {
  if (pastQuestionsProvider) {
    try { return pastQuestionsProvider(); } catch (err: any) { console.warn('[LocalRagEngine] çıkmış listesi sağlayıcıdan alınamadı:', err?.message || err); }
  }
  const pqPath = path.resolve(DATA_DIR, 'pastQuestions.json');
  if (!fs.existsSync(pqPath)) return null;
  const mtimeMs = fs.statSync(pqPath).mtimeMs;
  if (pastQuestionsRunCache?.mtimeMs === mtimeMs) return pastQuestionsRunCache.list;
  const list = JSON.parse(fs.readFileSync(pqPath, 'utf-8'));
  pastQuestionsRunCache = { mtimeMs, list };
  return list;
}

// 1. Çıkmış Sorular (past_question)
export function chunkPastQuestions(): RagChunk[] {
  const list = readPastQuestionsList();
  if (!list) return [];
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();

  for (const q of list) {
    // Sitede gösterilmeyen kayıtlar dizinlenmez: birleştirmede gizlenen kopya, karantina (check-solve dahil)
    const cs = q.checkSolve?.status;
    // Faz 17 'kaldirildi': soru olmayan/kopya kayıt çöp kutusunda (mezar taşı), sitede yok
    if (cs === 'karantina' || cs === 'kaldirildi' || (!cs && (q.status === 'quarantined' || q.isQuarantined))) continue;
    if (q.id && mergedInto(String(q.id))) continue;
    // Check-solve (Faz 16) kaydı güncel ve doğrulanmış içeriktir; eski denetleyici sürümü onu ezmez
    const csOk = cs === 'onayli';
    const isDenetleyici = !csOk && Boolean(q.denetleyiciOnayi || q.denetleyici_onayi || q.surum === 'denetleyici');
    const denetleyiciData = q.denetleyiciSurumu || {};

    const stem = ((isDenetleyici ? (denetleyiciData.stem || q.stem) : (q.stem || q.reconstruction?.stem || q.rawQuestion?.stem || '')) || '').trim();
    if (!stem) continue;

    const opts = (isDenetleyici && denetleyiciData.options) ? denetleyiciData.options : (q.options || q.reconstruction?.options || q.rawQuestion?.options || []);
    const optLines = Array.isArray(opts)
      ? opts.map((o: any) => typeof o === 'string' ? o : `${o.label || o.key || ''}) ${o.text || ''}`).join('\n')
      : '';
    const claim = isDenetleyici
      ? (denetleyiciData.correctAnswer || q.correctAnswer || q.claimedAnswer || '')
      : (q.correctAnswer || q.claimedAnswer || q.reconstruction?.correctAnswer || q.reconstruction?.correctOption || '');
    const expl = isDenetleyici
      ? (denetleyiciData.tibbi_aciklama || denetleyiciData.explanation || q.explanation || '')
      : (q.explanation || q.reconstruction?.explanation || '');

    // Format option analyses if present
    let optAnalysisSection = '';
    const sa = (isDenetleyici ? denetleyiciData.sik_analizi : null) || q.sik_analizi;
    if (sa && typeof sa === 'object' && Object.keys(sa).length > 0) {
      optAnalysisSection = '\n\nSeçenek Analizi ve Çürütme (Adım Adım Mekanizma):\n' +
        Object.entries(sa).map(([k, v]) => `- ${k}: ${v}`).join('\n');
    }

    // Format references if present
    let refsSection = '';
    const refs = (isDenetleyici ? denetleyiciData.referans_kaynaklar : null) || q.referans_kaynaklar;
    if (Array.isArray(refs) && refs.length > 0) {
      refsSection = '\n\nStandart Referans Tıp Kaynakları:\n' +
        refs.map((r: string) => `- ${r}`).join('\n');
    }

    const header = csOk
      ? '[ÇIKMIŞ SINAV SORUSU - DOĞRULANMIŞ]'
      : isDenetleyici
      ? '[DENETLEYİCİ ONAYLI ÇIKMIŞ SINAV SORUSU - ALTIN STANDART]'
      : '[ÇIKMIŞ SINAV SORUSU]';

    const content = `${header}
Ders / Branş: ${q.discipline || 'Tıp'}
Kurul: ${q.committeeId || 'donem3-kurul1'}${q.kazanim?.metin ? `\nKazanım: ${q.kazanim.metin}` : ''}
Sınav Yılı: ${q.examYear || 'Geçmiş Sınav'}
Konu: ${q.topic || 'Kurul Sorusu'}
${isDenetleyici ? 'Denetim Statüsü: Denetleyici Onayı (Doğrulandı, Guyton/Robbins/Moore Uyumlu)\n' : ''}Soru Kökü:
${stem}

Seçenekler:
${optLines}

Doğru / Kabul Edilen Cevap: ${claim}${isDenetleyici ? ' (Denetleyici Onaylı)' : ''}
${expl ? `\nAkademik Açıklama & Patofizyolojik Mekanizma:\n${expl}` : ''}${optAnalysisSection}${refsSection}`.trim();

    const h = hashContent(content);
    chunks.push({
      id: `chunk-pq-${q.id || h.slice(0, 10)}`,
      documentId: q.id || `pq-${h.slice(0, 8)}`,
      documentType: 'past_question',
      committeeId: q.committeeId || 'donem3-kurul1',
      discipline: q.discipline || 'Tıp',
      title: `${isDenetleyici ? '⭐ [Denetleyici Onaylı] ' : ''}${q.discipline || 'Tıp'} - ${q.topic || 'Çıkmış Soru'} (${q.examYear || 'Çıkmış'})`,
      pageNumber: q.questionNumber || null,
      content,
      metadata: {
        examYear: q.examYear,
        claimedAnswer: claim,
        sourceFile: q.sourceFile,
        topic: q.topic,
        isAmbiguous: q.isAmbiguous,
        hasSlideRef: Boolean(q.matchedNoteTitle || q.lectureReference),
        denetleyiciOnayi: isDenetleyici,
        checkSolve: csOk,
        kazanimId: q.kazanim?.id,
        surum: csOk ? 'check_solve' : isDenetleyici ? 'denetleyici' : 'orijinal',
        onayDurumu: isDenetleyici ? 'Denetleyici Onaylı' : 'Standart',
        hasOptionAnalysis: Boolean(sa && Object.keys(sa).length > 0)
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
  // Faz 12 temizlik katmanı (glif/OCR çöpü/üst-alt bilgi) sayfa metnine uygulanır
  const list = JSON.parse(fs.readFileSync(lnPath, 'utf-8')).map((n: any) => applyCleanOverlay(n));
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

// 3b. Ortak RAG ders materyali deposu (meds_database/ortak/rag/ders_materyali.jsonl — build_unified_store.py):
//     yeni hattın tüm ders slaytları, Faz 12 temiz metin, sınav dökümleri hariç; kurul/ders/konu ve kavram kimlikli.
export function chunkUnifiedMaterial(): RagChunk[] {
  const f = path.join(DESKTOP_DATABASE_DIR, 'ortak', 'rag', 'ders_materyali.jsonl');
  if (!fs.existsSync(f)) return [];
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();
  for (const line of fs.readFileSync(f, 'utf-8').split('\n')) {
    if (!line.trim()) continue;
    let r: any;
    try { r = JSON.parse(line); } catch { continue; }
    const text = String(r.metin || '').trim();
    if (text.length < 40) continue;
    const committeeId = r.kurul ? `donem3-kurul${r.kurul}` : 'donem3';
    const content = `[DERS SLAYTI]
Ders: ${r.ders || 'Tıp'}${r.konu ? `\nKonu: ${r.konu}` : ''}
Kaynak: ${r.kaynak} · Sayfa ${r.sayfa ?? '-'}
İçerik:
${text}`;
    chunks.push({
      id: `chunk-ortak-${r.id}`,
      documentId: String(r.kaynak_id),
      documentType: 'lecture_slide',
      committeeId,
      discipline: r.ders || 'Tıp',
      title: `${r.kaynak} (Sayfa ${r.sayfa ?? '-'})`,
      pageNumber: typeof r.sayfa === 'number' ? r.sayfa : undefined,
      content,
      metadata: { sourceId: r.kaynak_id, chunkId: r.id, topic: r.konu, concepts: r.kavramlar || [], clean: !!r.temiz, origin: 'ortak_rag' },
      hash: hashContent(content),
      createdAt: now,
      updatedAt: now,
    });
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
  const list = readPastQuestionsList();
  if (!list) return [];
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
  // Faz 14 önerileri (onay bekleyen + onaylı): aranabilir ama kaynak değil (ai_refinement, GROUNDING dışında)
  try {
    for (const [qid, r] of latestReviews()) {
      const p = r.proposal;
      if (!p || r.status === 'rejected') continue;
      const opts = Object.entries(p.secenekler || {}).map(([k, v]) => `${k}) ${v}`).join('\n');
      const content = `[FAZ 14 SORU DÜZELTME ÖNERİSİ · ${r.status === 'approved' ? 'onaylı' : 'onay bekliyor'}]
Kurul / Ders / Konu: ${[p.kurul_adi, p.ders_adi, p.konu_adi].filter(Boolean).join(' · ')}
Soru: ${p.soru_koku || ''}
${opts}
Önerilen cevap: ${p.dogru_secenek || ''}${p.cevap_degisti ? ` (kayıttakinden farklı: ${p.cevap_gerekcesi || ''})` : ''}
Açıklama:
${p.aciklama || ''}
Değişiklik özeti: ${typeof p.degisiklik_ozeti === 'string' ? p.degisiklik_ozeti : JSON.stringify(p.degisiklik_ozeti || '')}`.trim();
      chunks.push({
        id: `chunk-faz14-${qid}`,
        documentId: String(qid),
        documentType: 'ai_refinement',
        committeeId: normalizeKurul(p.kurul_adi) || 'donem3-kurul1',
        discipline: p.ders_adi || 'Tıp',
        title: `Faz 14 önerisi: ${p.ders_adi || ''} - ${p.konu_adi || ''}`,
        content,
        metadata: { questionId: String(qid), phase14: true, status: r.status, model: r.model },
        hash: hashContent(content),
        createdAt: r.processed_at || now,
        updatedAt: now,
      });
    }
  } catch {
    // Faz 14 kaydı yoksa atla
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
// Örnek sorular (ornek_sorular/k1/*.json: ders → kazanım → sorular)
// ==============================================================================
export function chunkOrnekSorular(): RagChunk[] {
  const base = path.resolve(PROJECT_ROOT, 'src', 'data', 'ornek_sorular', 'k1');
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();
  let files: string[] = [];
  try {
    files = fs.readdirSync(base).filter((f) => f.endsWith('.json') && f !== 'index.json');
  } catch { return []; }
  for (const f of files) {
    let ders: any;
    try { ders = JSON.parse(fs.readFileSync(path.join(base, f), 'utf-8')); } catch { continue; }
    const dersAd = ders.ders || 'Tıp';
    const konu = ders.konu || '';
    for (const kaz of ders.kazanimlar || []) {
      for (const s of kaz.sorular || []) {
        const kok = String(s.soru || '').trim();
        if (!kok) continue;
        const sec = Array.isArray(s.secenekler)
          ? s.secenekler.map((o: any) => typeof o === 'string' ? o : `${o.label || o.key || ''}) ${o.text || o.metin || ''}`).join('\n')
          : '';
        const content = `[ÖRNEK SORU]\nDers: ${dersAd}\nKonu: ${konu}\nKazanım: ${kaz.metin || s.kazanim || ''}\nZorluk: ${s.zorluk || ''}\nSoru:\n${kok}\n\nSeçenekler:\n${sec}\n\nDoğru: ${s.dogru || ''}\nAçıklama: ${s.aciklama || ''}`.slice(0, 2000);
        if (content.length < 20) continue;
        const h = hashContent(content);
        chunks.push({
          id: `chunk-ornek-${s.id || h.slice(0, 12)}`,
          documentId: String(s.id || ders.id || f),
          documentType: 'ornek_question',
          committeeId: 'donem3-kurul1',
          discipline: dersAd,
          title: `Örnek Soru: ${konu || dersAd}`,
          pageNumber: undefined,
          content,
          metadata: { source: 'ornek_sorular', kurul: ders.kurul, ogretimUyesi: ders.ogretim_uyesi, zorluk: s.zorluk },
          hash: h,
          createdAt: now,
          updatedAt: now,
        });
      }
    }
  }
  return chunks;
}

// ==============================================================================
// İnteraktif öğrenme desteleri (114 deste, slayt başına 1 chunk: anlatım + ögeler)
// ==============================================================================
export function chunkInteractiveDecks(): RagChunk[] {
  const p = path.resolve(PROJECT_ROOT, 'src', 'data', 'interactive_learning_decks.json');
  if (!fs.existsSync(p)) return [];
  const raw = JSON.parse(fs.readFileSync(p, 'utf-8'));
  const decks = Array.isArray(raw) ? raw : raw.decks || [];
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();
  const str = (v: any): string => (typeof v === 'string' ? v : v == null ? '' : JSON.stringify(v)).trim();
  for (const d of decks) {
    const deckId = d.deckId || d.id || '';
    const deckTitle = d.title || d.shortTitle || deckId;
    const disc = d.discipline || 'Tıp';
    for (const sl of d.slides || []) {
      const parts = [
        str(sl.synthesisNarrative), str(sl.content), str(sl.coreContent),
        (sl.spots || []).map(str).join('\n'),
        (sl.spotPearls || []).map(str).join('\n'),
        (sl.flashcards || []).map((f: any) => `${str(f.front || f.soru)} → ${str(f.back || f.cevap)}`).join('\n'),
        str(sl.microQuiz), str(sl.practiceQuestion),
        (sl.interactiveElements || []).map((e: any) => str(e.type || e.baslik || e.title)).join(', '),
        (sl.medicalTerms || []).map(str).join(', '),
      ].filter(Boolean).join('\n\n').slice(0, 2000);
      if (parts.length < 20) continue;
      const content = `[İNTERAKTİF DERS SLAYTI]\nDeste: ${deckTitle}\nDers: ${disc}\nSlayt ${sl.slideNumber || ''}: ${str(sl.title)}\n\n${parts}`;
      const h = hashContent(content);
      chunks.push({
        id: `chunk-deck-${deckId}-s${sl.slideNumber || '0'}`,
        documentId: String(deckId),
        documentType: 'deck_slide',
        committeeId: d.committee || 'donem3-kurul1',
        discipline: disc,
        title: `${deckTitle} — ${str(sl.title).slice(0, 80)}`,
        pageNumber: typeof sl.slideNumber === 'number' ? sl.slideNumber : undefined,
        content,
        metadata: { source: 'interactive_deck', deckId, slideNumber: sl.slideNumber, instructor: d.instructor },
        hash: h,
        createdAt: now,
        updatedAt: now,
      });
    }
  }
  return chunks;
}

// ==============================================================================
// Sözlük + tıbbi terimler (medical_glossary.json + tibbi_terimler_sozlugu.json)
// ==============================================================================
export function chunkGlossaryTerms(): RagChunk[] {
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();
  const push = (term: string, body: string, extra: Record<string, any>) => {
    const content = `[SÖZLÜK TERİMİ]\nTerim: ${term}\n${body}`.slice(0, 1500);
    if (!term || content.length < 20) return;
    const h = hashContent(content);
    chunks.push({
      id: `chunk-gloss-${h.slice(0, 12)}`,
      documentId: term,
      documentType: 'glossary_term',
      committeeId: extra.committee || 'donem3-kurul1',
      discipline: extra.discipline || 'Tıp',
      title: `Sözlük: ${term}`,
      pageNumber: undefined,
      content,
      metadata: { source: 'sozluk', ...extra },
      hash: h,
      createdAt: now,
      updatedAt: now,
    });
  };
  try {
    const g = JSON.parse(fs.readFileSync(path.resolve(PROJECT_ROOT, 'src', 'data', 'medical_glossary.json'), 'utf-8'));
    for (const [k, v] of Object.entries<any>(g)) {
      const body = [`Tanım: ${v.definition || v.description || ''}`, `Kategori: ${v.category || ''}`,
        `Klinik inci: ${v.clinicalPearl || ''}`, `Eşanlamlı: ${(v.aliases || []).join(', ')}`].filter((l) => l.split(': ')[1]?.trim()).join('\n');
      push(v.term || k, body, { discipline: v.discipline, committee: v.committee, category: v.category });
    }
  } catch { /* yoksa atla */ }
  try {
    const t = JSON.parse(fs.readFileSync(path.resolve(PROJECT_ROOT, '..', 'meds_database_v2', 'tibbi_terimler_sozlugu', 'tibbi_terimler_sozlugu.json'), 'utf-8'));
    for (const [k, v] of Object.entries<any>(t.terimler || {})) {
      const body = [`Türkçe: ${v.turkce || k}`, `Latin: ${v.latin || ''}`, `İngilizce: ${v.english || ''}`,
        `Anlam: ${v.kisa_anlam || ''}`, `Kategori: ${v.kategori || ''}`, `ICD-10: ${v['icd10/qid'] || ''}`].filter((l) => l.split(': ')[1]?.trim()).join('\n');
      push(v.turkce || k, body, { discipline: 'Tıp', category: v.kategori, terimId: v.id });
    }
  } catch { /* yoksa atla */ }
  return chunks;
}

// ==============================================================================
// Hastalıklar (diseases.json: tanı, belirti, tedavi)
// ==============================================================================
export function chunkDiseases(): RagChunk[] {
  const p = path.resolve(PROJECT_ROOT, 'src', 'data', 'diseases.json');
  if (!fs.existsSync(p)) return [];
  const list = JSON.parse(fs.readFileSync(p, 'utf-8'));
  const chunks: RagChunk[] = [];
  const now = new Date().toISOString();
  // Şema 2: her profil 3 parça (genel bakış · mekanizma · tanı-tedavi); bölüm başlıkları türe göre, maddeler "Etiket: metin"
  const GROUPS: Array<{ suffix: string; label: string; secs: DiseaseSectionId[] }> = [
    { suffix: '', label: 'Genel bakış', secs: ['definition', 'symptoms', 'pathognomonic', 'lecture'] },
    { suffix: '-mekanizma', label: 'Etiyoloji ve patoloji', secs: ['etiology', 'physiology', 'pathology', 'epidemiology'] },
    { suffix: '-tani-tedavi', label: 'Tanı ve tedavi', secs: ['diagnosis', 'imaging', 'treatment', 'complications'] },
  ];
  for (const raw of Array.isArray(list) ? list : []) {
    const d = normalizeDisease(raw);
    if (!d.name) continue;
    const head = [`[HASTALIK] ${d.name}${d.latinName ? ` (${d.latinName})` : ''}`, `Tür: ${KIND_LABEL[d.kind]} · ${d.category}${d.icd_code ? ` · ICD-10 ${d.icd_code}` : ''}`];
    if (d.altNames?.length) head.push(`Diğer adlar: ${d.altNames.join(', ')}`);
    for (const g of GROUPS) {
      const lines = [...head];
      if (!g.suffix && d.hallmarks.length) lines.push(`Karakteristik özellik: ${d.hallmarks.map(factPlain).join(' · ')}`);
      for (const sec of g.secs) {
        const title = sectionTitle(d.kind, sec);
        const items = sectionTexts(d, sec);
        if (title && items.length) lines.push(`${title}:`, ...items.map((t) => `- ${t}`));
      }
      if (lines.length <= head.length) continue;
      const content = lines.join('\n').slice(0, 2400);
      const h = hashContent(content);
      chunks.push({
        id: `chunk-dis-${d.id}${g.suffix}`,
        documentId: String(d.id),
        documentType: 'disease',
        committeeId: 'donem3-kurul1',
        discipline: 'Tıp',
        title: g.suffix ? `Hastalık: ${d.name} — ${g.label}` : `Hastalık: ${d.name}`,
        pageNumber: undefined,
        content,
        metadata: { source: 'hastaliklar', icd: d.icd_code, category: d.category, latin: d.latinName, kind: d.kind },
        hash: h,
        createdAt: now,
        updatedAt: now,
      });
    }
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
  // 1b. Veritabanında ayrı bölge: AI bilgilendirmeleri (kalıcı arşiv; kaynak değildir)
  try {
    const dir = path.join(process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database'), 'derived', 'ai_bilgi');
    fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(path.join(dir, 'ai_etkilesimleri.jsonl'), JSON.stringify(interaction) + '\n');
  } catch (e) {
    console.warn('ai_bilgi arşivine yazılamadı:', e);
  }

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

  // 3. Asynchronously generate embedding and mirror to meds-pg
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

  // Update in meds-pg
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
  await ensureLoaded(); // açılış yükü bitmeden birleştirirse yükleme sonradan üzerine yazar
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
    // Her kaynak üretilir üretilmez birleştirilir; tüm kaynakların yeni parçaları aynı anda bellekte tutulmaz
    let newlyIndexed = 0;
    const merge = (list: RagChunk[]) => {
      for (const chunk of list) {
        const existing = memoryChunks.get(chunk.id);
        if (!existing || existing.hash !== chunk.hash) {
          memoryChunks.set(chunk.id, chunk);
          newlyIndexed++;
        }
      }
    };
    pastQuestionsRunCache = null;

    // 1. Past questions
    const pq = chunkPastQuestions();
    console.log(`✓ 1/8 Çıkmış Sorular: ${pq.length} parça`);
    merge(pq);

    // 2. Active questions
    // Havuz (kullanıcı kaynaklı) soruları ham veridir ve sürekli değişir: RAG'e alınmaz.
    const aq: any[] = [];
    console.log(`✓ 2/8 Aktif Sorular: ${aq.length} parça`);
    merge(aq);

    // 3. Lecture slides
    const ls = chunkLectureNotes();
    console.log(`✓ 3/8 Ders Slaytları: ${ls.length} sayfa/parça`);
    merge(ls);

    // 3b. Ortak RAG deposu (yeni hat ders materyali, temiz metin)
    const um = chunkUnifiedMaterial();
    console.log(`✓ 3b Ortak Ders Materyali (yeni hat): ${um.length} parça`);
    merge(um);

    // 4. Summaries & spots
    const sm = chunkLectureSummaries();
    console.log(`✓ 4/8 Ders Özetleri & Spotlar: ${sm.length} bölüm`);
    merge(sm);

    // 5. Transcripts
    const tr = chunkAudioTranscripts();
    console.log(`✓ 5/8 Ses Transkriptleri: ${tr.length} parça`);
    merge(tr);

    // 6. User contributions
    const uc: any[] = []; // kullanıcı katkıları ham veri olarak kalır, RAG'e alınmaz
    console.log(`✓ 6/8 Kullanıcı Katkı & Yorumları: ${uc.length} parça`);
    merge(uc);

    // 7. AI Refinements
    const ar = chunkAiRefinements();
    console.log(`✓ 7/8 AI Düzeltmeleri & Revizyonları: ${ar.length} parça`);
    merge(ar);
    pastQuestionsRunCache = null; // büyük liste artık gerekmiyor

    // 8. AI Chat interactions
    const aiq = chunkAiInteractions();
    console.log(`✓ 8/9 AI Soru Sohbetleri: ${aiq.length} parça`);
    merge(aiq);

    // 9. DeepSeek Katkı & Düzenlenmiş Verileri
    const dsc = chunkDeepSeekData();
    console.log(`✓ 9/9 DeepSeek Katkıları: ${dsc.length} parça`);
    merge(dsc);

    // 10. Örnek sorular (k1 ders dosyaları)
    const os = chunkOrnekSorular();
    console.log(`✓ 10/12 Örnek Sorular: ${os.length} parça`);
    merge(os);

    // 11. İnteraktif öğrenme desteleri (slayt başına 1 chunk)
    const dk = chunkInteractiveDecks();
    console.log(`✓ 11/12 İnteraktif Deste Slaytları: ${dk.length} parça`);
    merge(dk);

    // 12. Sözlük terimleri + hastalıklar
    const gl = chunkGlossaryTerms();
    console.log(`✓ 12/12 Sözlük Terimleri: ${gl.length} parça`);
    merge(gl);
    const dz = chunkDiseases();
    console.log(`✓ 12/12 Hastalıklar: ${dz.length} parça`);
    merge(dz);

    // Çıkmış soru parçaları kaynak dosyanın tam yansımasıdır: artık üretilmeyen (silinen, birleştirilen, karantinaya alınan) soru parçası atılır
    const pqIds = new Set(pq.map((c) => c.id));
    pastQuestionsRunCache = null;
    let pruned = 0;
    for (const [id, c] of memoryChunks) {
      if (c.documentType === 'past_question' && !pqIds.has(id)) { memoryChunks.delete(id); pruned++; }
    }
    if (pruned) console.log(`🧹 Artık gösterilmeyen ${pruned} çıkmış soru parçası dizinden çıkarıldı`);

    await rebuildInvertedIndex();
    void warmSurfaceForms(); // yeni terimler öneri sözlüğüne de girsin (eskisi hazır olana dek kullanılır)
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
    pastQuestionsRunCache = null;
  }
}

export function getChunkCountsByType(): Record<string, number> {
  const counts: Record<string, number> = {};
  for (const chunk of memoryChunks.values()) {
    counts[chunk.documentType] = (counts[chunk.documentType] || 0) + 1;
  }
  return counts;
}

// Background sync to meds-pg with Gemini embeddings
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

  console.log(`[LocalRagEngine] ☁️ ${chunksWithoutCloud.length} parça meds-pg ve Gemini embedding için işleniyor...`);
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
  await ensureLoaded();
  const limit = options.limit || 5;
  const rawWords = foldTurkish(queryText)
    .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"'’“”…\[\]<>|\\+]/g, ' ')
    .split(/\s+/)
    .map((w) => w.trim())
    .filter((w) => w.length >= 3 && !FOLDED_STOPWORDS.has(w));

  const effectiveTokens: string[] = [];
  // Genişletilmiş her token'ın hangi sorgu kelimesinden geldiği (kök+tam sözcük
  // aynı kelime sayılır; yoksa tek kelime 2 eşleşme gibi görünür ve "sendromu"
  // tek başına tüm sendromları getirir).
  const tokenBase = new Map<string, string>();
  for (const w of rawWords) {
    if (fuzzyVocab.size() > 0 && !hasTerm(w)) {
      const hits = fuzzyVocab.findMatches(w, 2);
      if (hits.length > 0) {
        // En düşük mesafe ve en yüksek doküman frekansına göre sırala
        hits.sort((a, b) => a.dist - b.dist || termDf(b.term) - termDf(a.term));
        if (hits[0].dist <= (w.length >= 6 ? 2 : 1)) {
          const best = hits[0].term;
          effectiveTokens.push(best);
          tokenBase.set(best, w);
          if (best.length > STEM_LENGTH) {
            const st = best.slice(0, STEM_LENGTH) + '*';
            effectiveTokens.push(st);
            tokenBase.set(st, w);
          }
          continue;
        }
      }
    }
    effectiveTokens.push(w);
    tokenBase.set(w, w);
    if (w.length > STEM_LENGTH) {
      const st = w.slice(0, STEM_LENGTH) + '*';
      effectiveTokens.push(st);
      tokenBase.set(st, w);
    }
  }
  const cleanTokens = Array.from(new Set(effectiveTokens));
  if (cleanTokens.length === 0 && !options.queryEmbedding) return [];

  const N = memoryChunks.size || 1;
  const k1 = 1.2;
  const b = 0.75;
  const avgdl = avgDocLength || 110;

  // 1. Calculate IDF for each query token present in the index
  const tokenInfo: Array<{ token: string; idf: number }> = [];

  for (const t of cleanTokens) {
    const df = termDf(t);
    if (df > 0) {
      const idf = Math.log(1 + (N - df + 0.5) / (df + 0.5));
      tokenInfo.push({ token: t, idf });
    }
  }

  if (tokenInfo.length === 0 && !options.queryEmbedding) return [];

  // Sort by IDF descending: most discriminating / rare medical terms first
  tokenInfo.sort((x, y) => y.idf - x.idf);
  // Optimization: Prune query tokens to top 12 most informative terms (highest IDF)
  const tokensToScore = tokenInfo.slice(0, 12);
  // Budamada hayatta kalan taban kelimeler: kapsama koşulu bunlara göre kurulur
  const scoredBases = new Set(tokensToScore.map((t) => tokenBase.get(t.token) || t.token));
  // En ayırt edici taban kelime (örn. "down"): adayda mutlaka bulunmalı
  const rarestBase = tokenBase.get(tokensToScore[0]?.token || '') || '';

  // 2. Accumulate candidate BM25 scores
  const candidateScores = new Map<string, number>();
  const matchedTokensCount = new Map<string, number>();
  const matchedBases = new Map<string, Set<string>>();

  const ids = docIds;
  const lens = docLens;
  for (const { token, idf } of tokensToScore) {
    const base = tokenBase.get(token) || token;
    const add = (chunkId: string, tf: number, docLen: number) => {
      const tfNorm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (docLen / avgdl)));
      const termScore = idf * tfNorm;

      candidateScores.set(chunkId, (candidateScores.get(chunkId) || 0) + termScore);
      matchedTokensCount.set(chunkId, (matchedTokensCount.get(chunkId) || 0) + 1);
      let set = matchedBases.get(chunkId);
      if (!set) {
        set = new Set<string>();
        matchedBases.set(chunkId, set);
      }
      set.add(base);
    };
    const postings = invertedIndex.get(token);
    if (postings) {
      const { docs, tfs } = postings;
      for (let k = 0; k < docs.length; k++) add(ids[docs[k]], tfs[k], lens[docs[k]] || avgdl);
    }
    const pending = pendingIndex.get(token);
    if (pending) for (const [chunkId, tf] of pending) add(chunkId, tf, pendingLengths.get(chunkId) || avgdl);
  }

  // 3. Score and rank candidates
  const scoredResults: Array<{ chunk: RagChunk; score: number; similarity: number }> = [];
  const normalizedQuery = queryText.toLowerCase().replace(/[^a-z0-9ğüşıöç]/gi, ' ').trim();

  for (const [id, bmScore] of candidateScores.entries()) {
    const chunk = memoryChunks.get(id);
    if (!chunk) continue;

    // Kapsama koşulu: indekste karşılığı bulunan ≥2 taban kelime varsa adayda
    // en az 2'si geçmeli ve en ayırt edici kelime ("down") mutlaka bulunmalı.
    // Tek yaygın kelime ("sendromu") ile gelen Alport-benzeri sonuçlar burada elenir.
    const bases = matchedBases.get(id);
    const distinctBases = bases ? bases.size : 0;
    if (scoredBases.size >= 2) {
      if (distinctBases < 2) continue;
      if (rarestBase && !bases?.has(rarestBase)) continue;
    }

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

    // Term coordination boost: aynı kökün tam+kök çifti iki sayılmaz,
    // yalnızca farklı taban kelime sayısı (örn. down + sendromu) büyütür.
    const matchCount = distinctBases || 1;
    if (matchCount > 1) {
      finalScore *= (1 + 0.25 * (matchCount - 1));
    }

    // Exact phrase match bonus
    const lowerContent = chunk.content.toLowerCase();
    if (lowerContent.includes(normalizedQuery)) {
      finalScore += 25;
    }

    // Denetleyici Onayı (Altın Standart Soru): En yüksek doğruluk ve güncellik önceliği
    if (chunk.metadata?.denetleyiciOnayi) {
      finalScore += 50; // Denetleyici Onaylı doğrulanmış yeni sürüm en öncelikli gelir!
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
  ensureLoaded().then(() => {
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
  });

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

/**
 * Kimlikle arama (ör. "q-kurul4birc__km_s_-3", "note-2b4764e6f3"): chunk id ve documentId,
 * harf/rakam dışındaki karakterler yok sayılarak karşılaştırılır; tam eşleşme önce gelir.
 * BM25 sıralamasına dokunmaz.
 */
export function findChunksById(term: string, limit = 50): RagChunk[] {
  if (!indexReady) { void ensureLoaded(); return []; }
  const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '');
  const needle = norm(term);
  if (needle.length < 4) return [];
  const exact: RagChunk[] = [];
  const partial: RagChunk[] = [];
  for (const c of memoryChunks.values()) {
    const doc = norm(c.documentId || '');
    const id = norm(c.id || '');
    if (doc === needle || id === needle) exact.push(c);
    else if (doc.includes(needle) || id.includes(needle)) partial.push(c);
    if (exact.length >= limit) break;
  }
  return [...exact, ...partial].slice(0, limit);
}

// ------------------------------------------------------------------
// Kart adı dizini: hastalık ve sözlük kartları adıyla, parantez içi kısaltmasıyla
// ve "Diğer adlar"/"Eşanlamlı" satırlarıyla doğrudan bulunur. BM25 kısa kartları
// uzun soru metinlerinin altında havuz dışına itebildiği için ad eşleşmesi ayrı yoldan gelir.
// ------------------------------------------------------------------
export const cardNameKey = (s: string) => foldTurkish(s).replace(/[^a-z0-9]+/g, ' ').trim();
let cardNames: { size: number; map: Map<string, Array<{ chunk: RagChunk; kind: 'name' | 'alias' }>> } | null = null;
export function findCardsByName(name: string): Array<{ chunk: RagChunk; kind: 'name' | 'alias' }> {
  if (!indexReady) return [];
  if (!cardNames || cardNames.size !== memoryChunks.size) {
    const map = new Map<string, Array<{ chunk: RagChunk; kind: 'name' | 'alias' }>>();
    const add = (k: string, chunk: RagChunk, kind: 'name' | 'alias') => {
      if (k.length < 3) return;
      const list = map.get(k) || [];
      if (!list.some((e) => e.chunk.id === chunk.id)) list.push({ chunk, kind });
      map.set(k, list);
    };
    for (const c of memoryChunks.values()) {
      if (c.documentType !== 'disease' && c.documentType !== 'glossary_term') continue;
      const t = (c.title || '').replace(/^(Hastalık|Sözlük):\s*/, '').split(' — ')[0];
      add(cardNameKey(t.replace(/\([^)]*\)/g, ' ')), c, 'name');
      for (const m of t.matchAll(/\(([^)]+)\)/g)) for (const a of m[1].split(/[,;/]/)) add(cardNameKey(a), c, 'alias');
      const al = (c.content || '').match(/^(?:Diğer adlar|Eşanlamlı):\s*(.+)$/m);
      if (al) for (const a of al[1].split(/[,;]/)) add(cardNameKey(a.replace(/\([^)]*\)/g, ' ')), c, 'alias');
    }
    cardNames = { size: memoryChunks.size, map };
  }
  return cardNames.map.get(cardNameKey(name)) || [];
}

// ------------------------------------------------------------------
// "Bunu mu kastettiniz?": indeks sözlüğünden yazım önerisi.
// Sözlük katlanmış (aksansız) tutulur; öneri gösterilirken her terimin
// derlemde en sık geçen Türkçe yazımı kullanılır (tumoru → tümörü).
// ------------------------------------------------------------------
let surfaceForms: Map<string, string> | null = null;

let surfaceFormsBuild: Promise<void> | null = null;
function warmSurfaceForms(): Promise<void> {
  if (!surfaceFormsBuild) {
    surfaceFormsBuild = ensureLoaded()
      .then(buildSurfaceForms)
      .then((m) => { surfaceForms = m; })
      .finally(() => { surfaceFormsBuild = null; });
  }
  return surfaceFormsBuild;
}

async function buildSurfaceForms(): Promise<Map<string, string>> {
  const counts = new Map<string, Map<string, number>>();
  const slice = makeSlicer();
  for (const c of Array.from(memoryChunks.values())) {
    await slice();
    const words = c.content.match(/[\p{L}]{4,}/gu);
    if (!words) continue;
    for (const raw of words) {
      const w = raw.toLocaleLowerCase('tr');
      const f = foldTurkish(w);
      let m = counts.get(f);
      if (!m) { m = new Map(); counts.set(f, m); }
      m.set(w, (m.get(w) || 0) + 1);
    }
  }
  const out = new Map<string, string>();
  for (const [f, m] of counts) {
    await slice();
    let best = '';
    let n = 0;
    for (const [w, k] of m) if (k > n) { best = w; n = k; }
    out.set(f, best);
  }
  return out;
}

/** Sunucu açıldıktan sonra arka planda yüzey biçimlerini hazırlar (ilk öneri beklemesin) */
export function warmSpellIndex(): void {
  setTimeout(() => { warmSurfaceForms().catch(() => { /* yok say */ }); }, 15000);
}

export interface SpellSuggestion {
  /** Düzeltilmiş tam metin; değişiklik yoksa null */
  text: string | null;
  changes: Array<{ from: string; to: string }>;
}

export function suggestSpelling(text: string): SpellSuggestion {
  // Sözlük hazır değilken öneri yok (kurulumu tetikler, isteği bekletmez)
  if (!indexReady || !surfaceForms) { void warmSurfaceForms(); return { text: null, changes: [] }; }
  const changes: Array<{ from: string; to: string }> = [];
  const df = termDf;
  const prefix = (x: string, y: string) => { let i = 0; while (i < x.length && i < y.length && x[i] === y[i]) i++; return i; };
  const fixed = text.replace(/[\p{L}]{4,}/gu, (word) => {
    const f = foldTurkish(word);
    if (FOLDED_STOPWORDS.has(f)) return word;
    const own = df(f);
    let target = f;
    // Bilinmeyen sözcük (derlemde hiç geçmeyen): yakın ve yaygın terim ara
    if (own === 0 && f.length >= 5) {
      const best = fuzzyVocab.findMatches(f, 1)
        .filter((h) => h.term !== f && df(h.term) >= 10 && prefix(f, h.term) >= 2)
        .sort((x, y) => x.dist - y.dist || prefix(f, y.term) - prefix(f, x.term) || df(y.term) - df(x.term))[0];
      if (best) target = best.term;
      else return word;
    }
    // Türkçe karakter geri kazanımı: "tumoru" → "tümörü" (yalnızca kullanıcı Türkçe harf yazmadıysa)
    let to = surfaceForms!.get(target) || target;
    if (target === f && /[çğıöşü]/i.test(word)) return word;
    if (word[0] === word[0].toLocaleUpperCase('tr') && word[0] !== word[0].toLocaleLowerCase('tr')) {
      to = to.charAt(0).toLocaleUpperCase('tr') + to.slice(1);
    }
    if (to === word || to.toLocaleLowerCase('tr') === word.toLocaleLowerCase('tr')) return word;
    changes.push({ from: word, to });
    return to;
  });
  return { text: changes.length ? fixed : null, changes };
}
