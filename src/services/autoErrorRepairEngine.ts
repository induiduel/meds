/**
 * Otomatik Hata İnceleme ve Onarım Motoru (Auto Error Repair Engine)
 * 
 * Amaç: Sitedeki tüm hata bildirimlerini (Çıkmış sorular, örnek sorular, interaktif öğrenme desteleri)
 * merkezi bir kuyruğa alır. YALNIZCA ÜCRETSİZ Gemini API anahtarları ve modelleri (gemini-2.5-flash) ile
 * bildirimin bağlamını derinlemesine araştırır, hataları otomatik düzeltir ve veritabanına işler.
 * 
 * ESKİ VERİLER MUTLAKA KORUNUR: Her işlem öncesi 'beforeSnapshot' kaydedilir, admin dilediği zaman
 * tek tıkla değişikliği geri alabilir (Rollback).
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { getFreeGeminiKeys } from './aiProvider.ts';
import {
  detectQuestionCrossData,
  buildCrossDataPromptSection,
  releaseQuestionFromQuarantine,
  restoreQuestionToQuarantine,
  QuestionCrossData,
} from './questionCrossAuditService.ts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT_DIR = path.resolve(__dirname, '..', '..'); // meds/
const DATA_DIR = path.resolve(ROOT_DIR, 'data');
const SRC_DATA_DIR = path.resolve(ROOT_DIR, 'src', 'data');
const REPO_ROOT = path.resolve(ROOT_DIR, '..');

// Dosya Yolları
const REPAIR_DIR = path.resolve(DATA_DIR, 'auto_repair');
const QUEUE_FILE = path.resolve(REPAIR_DIR, 'queue.json');
const HISTORY_FILE = path.resolve(REPAIR_DIR, 'history.jsonl');
const BANNED_IDS_FILE = path.resolve(REPAIR_DIR, 'banned_report_ids.json');

const PAST_QUESTIONS_FILE = path.resolve(DATA_DIR, 'pastQuestions.json');
const SRC_PAST_QUESTIONS_FILE = path.resolve(SRC_DATA_DIR, 'pastQuestions.json');
const PRACTICE_QUESTIONS_FILE = path.resolve(DATA_DIR, 'questions.json');

const DECKS_FILE = path.resolve(SRC_DATA_DIR, 'interactive_learning_decks.json');
const DECK_ITEMS_DIR = path.resolve(SRC_DATA_DIR, 'decks', 'items');
const PACKAGES_DIR = path.resolve(REPO_ROOT, 'packages');

export type ErrorSource = 'past_question' | 'practice_question' | 'interactive_deck' | 'lecture_summary' | 'term' | 'flashcard';
export type RepairStatus = 'pending' | 'processing' | 'applied' | 'no_change' | 'rolled_back' | 'error';

export interface RepairUserReport {
  reason: string;
  details: string;
  reportedBy: string;
  reportedAt: string;
  email?: string;
  suggestedAnswer?: string;
}

export interface RepairAiAnalysis {
  detectedIssues: string[];
  medicalReasoning: string;
  actionTaken: 'corrected' | 'verified_correct' | 'inconclusive';
  changesSummary: string;
  processedAt: string;
  modelUsed: string;
  releaseQuarantine?: boolean;
  referencedRedactedId?: string;
  crossDataAuditApplied?: boolean;
}

export interface AutoRepairItem {
  id: string;
  source: ErrorSource;
  targetId: string;
  subTarget?: {
    slideNumber?: number;
    targetKey?: string;
    optionKey?: string;
    location?: string;
    label?: string;
  };
  userReport: RepairUserReport;
  fullContext: any;
  status: RepairStatus;
  aiAnalysis?: RepairAiAnalysis;
  beforeSnapshot?: any;
  afterSnapshot?: any;
  ticketNo?: string;
  crossData?: QuestionCrossData;
  errorDetails?: string;
  rolledBackAt?: string;
  retryCount?: number;
}

// Yardımcı Fonksiyonlar
function ensureDirs() {
  if (!fs.existsSync(REPAIR_DIR)) fs.mkdirSync(REPAIR_DIR, { recursive: true });
}

function readJsonSafe<T>(filePath: string, fallback: T): T {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    }
  } catch (err) {
    console.error(`[AutoRepairEngine] JSON okuma hatası (${filePath}):`, err);
  }
  return fallback;
}

function writeJsonAtomic(filePath: string, data: any) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  const content = JSON.stringify(data, null, 2);
  const tempPath = `${filePath}.tmp_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`;
  fs.writeFileSync(tempPath, content, 'utf-8');
  fs.renameSync(tempPath, filePath);
}

function appendHistory(item: AutoRepairItem) {
  try {
    ensureDirs();
    fs.appendFileSync(HISTORY_FILE, JSON.stringify(item) + '\n', 'utf-8');
  } catch (err) {
    console.error('[AutoRepairEngine] Geçmiş kaydı yazılamadı:', err);
  }
}

function dismissQuestionReportsInDb(targetId: string, _itemId?: string) {
  try {
    const list = readJsonSafe<any[]>(PAST_QUESTIONS_FILE, []);
    const idx = list.findIndex((q) => String(q.id) === String(targetId));
    if (idx !== -1) {
      const q = list[idx];
      const curReports = Array.isArray(q.reports) ? [...q.reports] : [];
      let changed = false;
      for (let i = 0; i < curReports.length; i++) {
        const r = curReports[i];
        if (r.status !== 'resolved' && r.status !== 'verified_correct' && r.status !== 'dismissed') {
          curReports[i] = {
            ...r,
            status: 'dismissed',
            resolvedAt: new Date().toISOString(),
            resolvedBy: 'Yönetici (Silindi/Banlandı)',
            resolutionSummary: 'Yönetici tarafından bildirim kuyruktan kaldırıldı ve kalıcı olarak kapatıldı.',
          };
          changed = true;
        }
      }
      if (changed) {
        q.reports = curReports;
        q.qualityIssues = (Array.isArray(q.qualityIssues) ? q.qualityIssues : []).filter(
          (issue: string) => !issue.startsWith('sikayet-')
        );
        q.qualityScore = Math.max(Number(q.qualityScore || 0), 92);
        q.updatedAt = new Date().toISOString();
        list[idx] = q;
        writeJsonAtomic(PAST_QUESTIONS_FILE, list);
        if (fs.existsSync(SRC_PAST_QUESTIONS_FILE)) {
          writeJsonAtomic(SRC_PAST_QUESTIONS_FILE, list);
        }
      }
    }
  } catch (err) {
    console.error('[AutoRepairEngine] dismissQuestionReportsInDb hatası:', err);
  }
}

// --- Kuyruk Depolama & Banlı Rapor ID Yönetimi ---
class AutoRepairStore {
  private queue: AutoRepairItem[] = [];
  private bannedIds: Set<string> = new Set();
  private isLoaded = false;

  private load() {
    ensureDirs();
    this.queue = readJsonSafe<AutoRepairItem[]>(QUEUE_FILE, []);
    const bannedArr = readJsonSafe<string[]>(BANNED_IDS_FILE, []);
    this.bannedIds = new Set(Array.isArray(bannedArr) ? bannedArr : []);
    this.isLoaded = true;
  }

  private save() {
    ensureDirs();
    writeJsonAtomic(QUEUE_FILE, this.queue);
  }

  private saveBanned() {
    ensureDirs();
    writeJsonAtomic(BANNED_IDS_FILE, Array.from(this.bannedIds));
  }

  isBanned(id: string): boolean {
    if (!this.isLoaded) this.load();
    return this.bannedIds.has(id);
  }

  getBannedList(): string[] {
    if (!this.isLoaded) this.load();
    return Array.from(this.bannedIds);
  }

  getAll(): AutoRepairItem[] {
    this.load();
    return [...this.queue];
  }

  getById(id: string): AutoRepairItem | undefined {
    this.load();
    return this.queue.find((q) => q.id === id);
  }

  getPending(): AutoRepairItem[] {
    this.load();
    return this.queue.filter((q) => q.status === 'pending');
  }

  enqueue(item: Omit<AutoRepairItem, 'id' | 'status'> & { id?: string }): AutoRepairItem | null {
    this.load();
    // Her yeni hata bildirimine kriptografik/zaman damgalı BENZERSİZ bir ID ver
    const id = item.id || `rep_uniq_${Date.now()}_${Math.random().toString(36).slice(2, 9)}_${Math.random().toString(36).slice(2, 6)}`;

    // Eğer bu ID admin tarafından banlanmışsa ASLA KUYRUĞA ALMA!
    if (this.isBanned(id)) {
      console.warn(`[AutoRepairEngine] 🛑 Banlı bildirim ID'si reddedildi (tekrar eklenemez): ${id}`);
      return null;
    }

    // 1. Doğrudan aynı id ile kayıt varsa mükerrer ekleme
    const existingById = this.queue.find((q) => q.id === id);
    if (existingById) {
      return existingById;
    }
    
    // 2. Zaten bekleyen veya işlenen aynı hedef ve kullanıcı şikayeti varsa birleştir
    const existing = this.queue.find(
      (q) =>
        (q.status === 'pending' || q.status === 'processing') &&
        q.source === item.source &&
        q.targetId === item.targetId &&
        q.subTarget?.slideNumber === item.subTarget?.slideNumber &&
        q.subTarget?.targetKey === item.subTarget?.targetKey
    );

    if (existing) {
      if (item.userReport.details && !existing.userReport.details.includes(item.userReport.details)) {
        existing.userReport.details = `${existing.userReport.details}\nEk Bildirim (${item.userReport.reportedBy}): ${item.userReport.details}`.trim();
      }
      this.save();
      return existing;
    }

    let ticketNo = item.ticketNo;
    if (!ticketNo) {
      const maxTicket = this.queue.reduce((max, it) => {
        if (it.ticketNo && /^#\d+$/.test(it.ticketNo)) {
          const val = parseInt(it.ticketNo.slice(1), 10);
          return val > max ? val : max;
        }
        return max;
      }, 0);
      ticketNo = `#${String(maxTicket + 1).padStart(6, '0')}`;
    }

    const newItem: AutoRepairItem = {
      ...item,
      id,
      ticketNo,
      status: 'pending',
      retryCount: 0,
    };

    this.queue.unshift(newItem); // En yenisi başa veya sıraya
    this.save();
    return newItem;
  }

  update(id: string, patch: Partial<AutoRepairItem>): AutoRepairItem | null {
    this.load();
    const idx = this.queue.findIndex((q) => q.id === id);
    if (idx === -1) return null;
    this.queue[idx] = { ...this.queue[idx], ...patch };
    this.save();
    return this.queue[idx];
  }

  /** Bir hata bildirimini kuyruktan siler ve ID'sini kalıcı olarak banlar; asla geri gelemez */
  banAndRemove(id: string): boolean {
    this.load();
    this.bannedIds.add(id);
    const item = this.queue.find((q) => q.id === id);
    if (item && item.source === 'past_question') {
      dismissQuestionReportsInDb(item.targetId, item.id);
    }
    this.queue = this.queue.filter((q) => q.id !== id);
    this.save();
    this.saveBanned();
    console.log(`[AutoRepairEngine] 🚫 Hata bildirimi ID'si kalıcı olarak banlandı ve silindi: ${id}`);
    return true;
  }

  remove(id: string): boolean {
    return this.banAndRemove(id);
  }

  /** Birden fazla ID'yi topluca banlar ve siler */
  bulkBanAndRemove(ids: string[]): { removedCount: number } {
    this.load();
    const idSet = new Set(ids);
    let count = 0;
    for (const id of ids) {
      this.bannedIds.add(id);
      const item = this.queue.find((q) => q.id === id);
      if (item && item.source === 'past_question') {
        dismissQuestionReportsInDb(item.targetId, item.id);
      }
    }
    this.queue = this.queue.filter((q) => {
      if (idSet.has(q.id)) {
        count++;
        return false;
      }
      return true;
    });
    this.save();
    this.saveBanned();
    console.log(`[AutoRepairEngine] 🚫 ${count} adet hata bildirimi topluca banlandı ve silindi.`);
    return { removedCount: count };
  }

  /** Tüm işlem yapılmış (applied, no_change, rolled_back) bildirimleri banlar ve kuyruktan temizler */
  clearProcessed(): { clearedCount: number; bannedCount: number } {
    this.load();
    const toClear = this.queue.filter(
      (q) => q.status === 'applied' || q.status === 'no_change' || q.status === 'rolled_back'
    );
    for (const item of toClear) {
      this.bannedIds.add(item.id);
      if (item.source === 'past_question') {
        dismissQuestionReportsInDb(item.targetId, item.id);
      }
    }
    const clearedCount = toClear.length;
    this.queue = this.queue.filter(
      (q) => q.status !== 'applied' && q.status !== 'no_change' && q.status !== 'rolled_back'
    );
    this.save();
    this.saveBanned();
    console.log(`[AutoRepairEngine] 🧹 İşlem yapılan ${clearedCount} adet bildirim temizlendi ve ID'leri banlandı.`);
    return { clearedCount, bannedCount: this.bannedIds.size };
  }
}

export const autoRepairStore = new AutoRepairStore();

// --- Ortam Değişkenlerini Güvenli Yükleme ---
function loadMedsEnv() {
  const envPaths = [
    path.resolve(ROOT_DIR, '.env'),
    path.resolve(REPO_ROOT, '.env'),
    path.resolve(process.cwd(), '.env'),
    path.resolve(process.cwd(), 'meds', '.env'),
  ];
  for (const p of envPaths) {
    if (fs.existsSync(p)) {
      try {
        const content = fs.readFileSync(p, 'utf-8');
        for (const line of content.split('\n')) {
          const trimmed = line.trim();
          if (!trimmed || trimmed.startsWith('#') || !trimmed.includes('=')) continue;
          const [k, ...vParts] = trimmed.split('=');
          const keyName = k.trim();
          const val = vParts.join('=').trim().replace(/^['"]|['"]$/g, '');
          if (!process.env[keyName]) {
            process.env[keyName] = val;
          }
        }
      } catch (_) {}
    }
  }
}
loadMedsEnv();

export function getAutoRepairFreeKeys(): { key: string; label: string }[] {
  loadMedsEnv();
  const keys: { key: string; label: string }[] = [];
  const add = (k: string | undefined, label: string) => {
    if (k && k.trim() && !k.startsWith('MY_') && !keys.some((x) => x.key === k.trim())) {
      keys.push({ key: k.trim(), label });
    }
  };
  add(process.env.GEMINI_API_KEY, 'Ücretsiz Plan 1 (Gemini)');
  add(process.env.GEMINI_FREE_KEY_2, 'Ücretsiz Plan 2 (Gemini)');
  for (const n of Object.keys(process.env)) {
    if (/^GEMINI_FREE_KEY_\d+$/.test(n)) {
      add(process.env[n], `Ücretsiz Plan ${n.slice(16)} (Gemini)`);
    }
  }
  return keys;
}

// --- Güvenli JSON Çözümleyici (Tüm Yapay Zeka Çıktıları İçin) ---
function parseAiJsonOutput(text: string): any {
  if (!text) throw new Error('Yapay zeka boş yanıt döndürdü.');
  let cleaned = text.trim();
  if (cleaned.startsWith('```')) {
    cleaned = cleaned.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/i, '').trim();
  }
  try {
    return JSON.parse(cleaned);
  } catch (_) {
    const match = cleaned.match(/\{[\s\S]*\}/);
    if (match) {
      try {
        return JSON.parse(match[0]);
      } catch (_) {}
    }
    throw new Error('Yapay zeka geçerli bir JSON çıktısı üretemedi: ' + text.slice(0, 150));
  }
}

// --- Ücretsiz Yapay Zeka Entegrasyonu & Çok Katmanlı Fall-back Sistemi ---
// 1. Aşama: Google Gemini Ücretsiz Havuzu (7 Adet Key)
// 2. Aşama: Groq Cloud Ücretsiz (openai/gpt-oss-120b, qwen/qwen3.8-27b, openai/gpt-oss-20b)
// 3. Aşama: OpenRouter / Muse Spark Ücretsiz Modeller (:free)
// 4. Aşama: Yerel Ollama GPU Modelleri (qwen3:1.7b, medgemma1.5:4b)
const FREE_GEMINI_MODELS = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash-latest', 'gemini-flash-latest'];

async function callFreeAiWithFallback(prompt: string, systemInstruction: string): Promise<{ data: any; model: string }> {
  let lastError: any = null;

  // 1. AŞAMA: Google Gemini Ücretsiz Havuzu
  const geminiKeys = getAutoRepairFreeKeys();
  if (geminiKeys.length > 0) {
    for (const keyInfo of geminiKeys) {
      for (const model of FREE_GEMINI_MODELS) {
        try {
          const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${encodeURIComponent(keyInfo.key)}`;
          const body = {
            contents: [
              {
                role: 'user',
                parts: [{ text: prompt }],
              },
            ],
            systemInstruction: {
              role: 'system',
              parts: [{ text: systemInstruction }],
            },
            generationConfig: {
              temperature: 0.1, // Tıbbi denetim ve hassas doğruluk için düşük sıcaklık
              responseMimeType: 'application/json',
            },
          };

          const res = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
          });

          if (!res.ok) {
            const errText = await res.text().catch(() => '');
            lastError = new Error(`Gemini ${model} [${keyInfo.label}] HTTP ${res.status}: ${errText}`);
            // Rate limit (429) veya hata durumunda diğer anahtara/modele geç
            continue;
          }

          const json = await res.json();
          const text = json?.candidates?.[0]?.content?.parts?.[0]?.text;
          const parsed = parseAiJsonOutput(text);
          return { data: parsed, model };
        } catch (err: any) {
          lastError = err;
        }
      }
    }
  }

  console.warn('[AutoRepairEngine] ⚠️ Tüm ücretsiz Gemini anahtarları/modelleri tükendi veya limit aşıldı. 1. Fallback (Groq Cloud) devreye giriyor...');

  // 2. AŞAMA (FALLBACK 1): Groq Cloud Ücretsiz (openai/gpt-oss-120b, qwen/qwen3.8-27b)
  loadMedsEnv();
  const groqKeys = [process.env.GROQ_API_KEY, process.env.GROQ_API_KEY_2].filter(
    (k): k is string => Boolean(k && k.trim() && !k.startsWith('MY_'))
  );
  const GROQ_MODELS = ['openai/gpt-oss-120b', 'qwen/qwen3.8-27b', 'openai/gpt-oss-20b'];

  if (groqKeys.length > 0) {
    for (const groqKey of groqKeys) {
      for (const model of GROQ_MODELS) {
        try {
          console.log(`[AutoRepairEngine] 🔄 [Groq Fallback] ${model} ile analiz yapılıyor...`);
          const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${groqKey}`,
            },
            body: JSON.stringify({
              model,
              messages: [
                { role: 'system', content: `${systemInstruction}\n\nÖNEMLİ KURAL: Çıktıyı YALNIZCA geçerli bir JSON nesnesi olarak üret, markdown dışı açıklama yazma.` },
                { role: 'user', content: prompt },
              ],
              temperature: 0.1,
              response_format: { type: 'json_object' },
            }),
          });

          if (!res.ok) {
            const errText = await res.text().catch(() => '');
            lastError = new Error(`Groq ${model} HTTP ${res.status}: ${errText}`);
            continue;
          }

          const json = await res.json();
          const content = json?.choices?.[0]?.message?.content;
          const parsed = parseAiJsonOutput(content);
          console.log(`[AutoRepairEngine] ✅ Groq (${model}) başarıyla yanıt verdi.`);
          return { data: parsed, model: `groq/${model}` };
        } catch (err: any) {
          lastError = err;
        }
      }
    }
  }

  console.warn('[AutoRepairEngine] ⚠️ Groq limitine ulaşıldı. 2. Fallback (OpenRouter Ücretsiz Modeller) devreye giriyor...');

  // 3. AŞAMA (FALLBACK 2): OpenRouter / Muse Spark Ücretsiz Modeller (:free)
  const openRouterKeys = [process.env.OPENROUTER_API_KEY, process.env.MUSE_SPARK_API_KEY].filter(
    (k): k is string => Boolean(k && k.trim() && !k.startsWith('MY_'))
  );
  const OPENROUTER_MODELS = [
    'google/gemma-4-31b-it:free',
    'nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free',
    'liquid/lfm-2.5-2.6b:free',
  ];

  if (openRouterKeys.length > 0) {
    for (const orKey of openRouterKeys) {
      for (const model of OPENROUTER_MODELS) {
        try {
          console.log(`[AutoRepairEngine] 🔄 [OpenRouter Fallback] ${model} deneniyor...`);
          const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${orKey}`,
              'HTTP-Referer': 'https://induiduel.github.io/meds',
              'X-Title': 'MeDSor Auto Repair',
            },
            body: JSON.stringify({
              model,
              messages: [
                { role: 'system', content: `${systemInstruction}\n\nÖNEMLİ KURAL: Çıktıyı YALNIZCA geçerli bir JSON nesnesi olarak üret.` },
                { role: 'user', content: prompt },
              ],
              temperature: 0.1,
            }),
          });

          if (!res.ok) {
            const errText = await res.text().catch(() => '');
            lastError = new Error(`OpenRouter ${model} HTTP ${res.status}: ${errText}`);
            continue;
          }

          const json = await res.json();
          const content = json?.choices?.[0]?.message?.content;
          const parsed = parseAiJsonOutput(content);
          console.log(`[AutoRepairEngine] ✅ OpenRouter (${model}) başarıyla yanıt verdi.`);
          return { data: parsed, model: `openrouter/${model}` };
        } catch (err: any) {
          lastError = err;
        }
      }
    }
  }

  // 4. AŞAMA (FALLBACK 3): Yerel Ollama (Eğer aktifse)
  try {
    console.log('[AutoRepairEngine] 🔄 [Ollama Fallback] Yerel Ollama (qwen3:1.7b-q8_0) deneniyor...');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 12000);
    const ollamaRes = await fetch('http://localhost:11434/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'qwen3:1.7b-q8_0',
        prompt: `${systemInstruction}\n\nİstek:\n${prompt}\n\nLütfen yalnızca geçerli bir JSON nesnesi döndür:`,
        format: 'json',
        stream: false,
      }),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    if (ollamaRes.ok) {
      const data = await ollamaRes.json();
      const parsed = parseAiJsonOutput(data.response);
      console.log('[AutoRepairEngine] ✅ Yerel Ollama başarıyla yanıt verdi.');
      return { data: parsed, model: 'ollama/qwen3:1.7b-q8_0' };
    }
  } catch (_) {}

  throw lastError || new Error('Tüm ücretsiz yapay zeka modelleri (Gemini, Groq, OpenRouter, Ollama) tükendi veya erişilemez durumda.');
}

// Geriye dönük uyumluluk için alias
const callFreeGeminiJson = callFreeAiWithFallback;

// --- Hedef Veri Okuma ve Zenginleştirme ---
export function enrichAndFetchContext(source: ErrorSource, targetId: string, subTarget?: any): any {
  if (source === 'past_question') {
    const list = readJsonSafe<any[]>(PAST_QUESTIONS_FILE, []);
    let q = list.find((item) => String(item.id) === String(targetId));
    if (!q) {
      // Yedek kaynak olarak src'ye bak
      const srcList = readJsonSafe<any[]>(SRC_PAST_QUESTIONS_FILE, []);
      q = srcList.find((item) => String(item.id) === String(targetId)) || null;
    }
    if (q) {
      const crossData = detectQuestionCrossData(targetId, 'past_question');
      return {
        ...q,
        _crossData: crossData,
      };
    }
    return null;
  }

  if (source === 'practice_question') {
    const list = readJsonSafe<any[]>(PRACTICE_QUESTIONS_FILE, []);
    const q = list.find((item) => String(item.id) === String(targetId));
    if (q) {
      const crossData = detectQuestionCrossData(targetId, 'practice_question');
      return {
        ...q,
        _crossData: crossData,
      };
    }
    return null;
  }

  if (source === 'interactive_deck') {
    // 1. Deste dosyasından oku
    const decks = readJsonSafe<any[]>(DECKS_FILE, []);
    let deck = decks.find((d) => String(d.id) === String(targetId));
    if (!deck) {
      // items/<id>.json dosyasından dene
      const itemFile = path.resolve(DECK_ITEMS_DIR, `${targetId}.json`);
      deck = readJsonSafe<any>(itemFile, null);
    }
    if (deck) {
      const slideNum = subTarget?.slideNumber;
      const targetSlide = slideNum ? deck.slides?.find((s: any) => s.slideNumber === slideNum) : null;
      return {
        deckMeta: { id: deck.id, title: deck.title, topic: deck.topic, committee: deck.committee },
        targetSlide: targetSlide || deck.slides?.[0] || null,
        fullDeck: deck,
      };
    }
    return null;
  }

  if (source === 'term') {
    const GLOSSARY_FILE = path.resolve(SRC_DATA_DIR, 'medical_glossary.json');
    const terms = readJsonSafe<any[]>(GLOSSARY_FILE, []);
    const term = terms.find((t: any) => String(t.id) === String(targetId));
    return term || { id: targetId };
  }

  if (source === 'flashcard') {
    return { id: targetId, subTarget };
  }

  return null;
}

// --- Tıbbi Denetim ve Onarım Mantığı ---

/**
 * Kullanıcı eksik açıklama girse bile derinlemesine araştırma felsefesi:
 * "Hata bildirimi varsa hata olabilir, hata bildiriminin geldiği konum burasıysa burada hata olabilir.
 * Hiçbir şey doğru kabul edilemez. Hatalı ifade, şık, bilgi, tablo, soru kökü vb her şey denetlenir."
 */
async function inspectAndRepairQuestion(item: AutoRepairItem): Promise<{
  hasError: boolean;
  detectedIssues: string[];
  medicalReasoning: string;
  changesSummary: string;
  correctedQuestion: any;
  modelUsed: string;
  releaseQuarantine?: boolean;
  referencedRedactedId?: string;
}> {
  const currentQ = item.fullContext || enrichAndFetchContext(item.source, item.targetId, item.subTarget);
  if (!currentQ) {
    throw new Error(`Soru verisi bulunamadı (ID: ${item.targetId})`);
  }

  const crossData: QuestionCrossData =
    currentQ._crossData || item.crossData || detectQuestionCrossData(item.targetId, item.source as any);
  const crossDataPromptSection = buildCrossDataPromptSection(crossData);

  const systemInstruction = `Sen kıdemli bir tıp fakültesi profesörü ve tıbbi soru denetim kurulu başkanısın.
Görev: Kullanıcılar sistemdeki bir tıp sorusuna hata bildirimi yapmıştır.
MUTLAK KURALLAR:
1. "Hata bildirimi varsa hata olabilir, hata bildiriminin geldiği konum burasıysa burada hata olabilir. Hiçbir şey peşinen doğru kabul edilemez."
2. ÇAPRAZ VERİ, KARANTİNA & REDAKSİYON KORUMA KURALI (KESİNLİKLE ZORUNLU):
   - Bazı sorular karantinada (sınav sitesi enkazı, kesik kök, şık kayması vb.) yer almaktadır.
   - Ancak bu soruya ait daha önce yapılmış bir redaksiyon (reconstruction) veya sistemde aynı ya da farklı ID ile redakte edilmiş temiz bir kardeş soru (merge group / ikiz kayıt) bulunabilir!
   - ZATEN VAR OLAN TEMİZ VE DOĞRU BİR REDAKSİYONU ASLA ÇÖPE ATMA, BOZMA VEYA KÖRÜ KÖRÜNE ÜZERİNE YAZMA!
   - Karantinadaki bozuk/sınav sitesi artığı metin yerine; SİSTEMDE TESPİT EDİLEN EN KALİTELİ REDAKTE REFERANS KAYDI temel al.
   - Kullanıcının şikayetini ve itirazını bu temiz redaksiyon üzerinden değerlendir.
   - Eğer mevcut redaksiyon zaten tıbben ve akademik olarak doğru ise ve kullanıcının şikayeti haksız ise:
     "has_error": false, "actionTaken": "verified_correct" döndür, mevcut redaksiyonu koru ve gerekçesini açıkla.
   - Eğer soru karantinada ise ve bu inceleme/onarım ile soru kusursuz hale getiriliyorsa:
     "release_quarantine": true döndür (böylece soru resmi olarak karantinadan tahliye edilir).
   - Düzeltilen veya doğrulanan sorunun kök, şık, doğru cevap ve açıklama ('reconstruction') verilerini eksiksiz tamamla.
3. Tıbbi Denetim Kriterleri:
   - Soru kökünde mantıksal, gramatik veya olumsuzluk (değildir / beklenmez) çelişkisi var mı?
   - Şıklardan birden fazlası doğru mu ya da hiçbiri doğru değil mi?
   - Mevcut işaretli doğru cevap gerçekten doğru mu, yoksa kullanıcının veya tıbbi gerçeğin işaret ettiği başka bir şık mı doğru?
   - Açıklama fizyopatolojik mekanizmayı tam ve doyurucu anlatıyor mu? Şıkların tek tek çürütmesi var mı?
4. Eğer soruda HATA, YANLIŞLIK veya EKSİKLİK tespit edersen:
   - has_error: true
   - detected_issues: Tespit edilen tüm hataların listesi (maddeler halinde)
   - medical_reasoning: Altta yatan fizyopatolojik/biyokimyasal tıp mekanizması ve Robbins/Guyton referanslı gerekçe
   - changes_summary: Yapılan değişikliğin 1-2 cümlelik net özeti
   - release_quarantine: Soru karantinada ise ve düzeltilip temizlendiyse true, değilse false
   - referenced_redacted_id: Eğer sistemdeki redakte bir soru baz alındıysa onun ID'si, yoksa null
   - corrected_data: Sorunun düzeltilmiş tam nesnesi (stem, options, correctAnswer, explanation, reconstruction vb.)
5. Eğer soru incelendikten sonra tıbben ve akademik olarak KESİNLİKLE KUSURSUZ VE DOĞRU ise:
   - has_error: false
   - detected_issues: []
   - medical_reasoning: Sorunun/redaksiyonun neden tıbben tam ve doğru olduğunun ayrıntılı gerekçesi
   - changes_summary: "Soru incelendi; mevcut kök, şıklar ve cevap tıbbi literatüre tamamen uygundur."
   - release_quarantine: crossData.isQuarantined ? true : false
   - referenced_redacted_id: crossData.bestRedactedReference?.id || null
   - corrected_data: null

Çıktı Şeması (JSON):
{
  "has_error": boolean,
  "detected_issues": ["..."],
  "medical_reasoning": "...",
  "changes_summary": "...",
  "release_quarantine": boolean,
  "referenced_redacted_id": "string veya null",
  "corrected_data": { ... } // Soru nesnesinin tamamı (has_error=false ise null)
}`;

  const prompt = `LÜTFEN AŞAĞIDAKİ TIP SORUSUNU, SİSTEMSEL ÇAPRAZ VERİ RAPORUNU VE GELEN BİLDİRİMİ TİTİZLİKLE İNCELE VE GEREKİYORSA DÜZELT:

${crossDataPromptSection}

KULLANICI BİLDİRİMİ:
- Şikayet Sebebi / Başlık: ${item.userReport.reason || 'Belirtilmedi'}
- Kullanıcı Detayı / İtirazı: ${item.userReport.details || 'Kullanıcı ek detay yazmadı; sorunun tamamını (kök, şıklar, cevap, açıklama) bağımsız olarak baştan sona denetle.'}
- Önerilen Şık / Yanıt: ${item.userReport.suggestedAnswer || 'Belirtilmedi'}
- İtiraz Edilen Şık: ${item.subTarget?.optionKey || 'Genel'}

MEVCUT HAM SORU VERİSİ:
${JSON.stringify(currentQ, null, 2)}

Yanıtını yukarıda belirtilen JSON şemasına harfiyen uygun olarak ver.`;

  const { data, model } = await callFreeGeminiJson(prompt, systemInstruction);

  return {
    hasError: Boolean(data?.has_error),
    detectedIssues: Array.isArray(data?.detected_issues) ? data.detected_issues : [],
    medicalReasoning: String(data?.medical_reasoning || ''),
    changesSummary: String(data?.changes_summary || ''),
    correctedQuestion: data?.corrected_data || null,
    modelUsed: model,
    releaseQuarantine: Boolean(data?.release_quarantine),
    referencedRedactedId: data?.referenced_redacted_id ? String(data.referenced_redacted_id) : undefined,
  };
}


/**
 * İnteraktif Öğrenme Destesi / Slaytı İnceleme ve Onarımı
 */
async function inspectAndRepairInteractiveDeck(item: AutoRepairItem): Promise<{
  hasError: boolean;
  detectedIssues: string[];
  medicalReasoning: string;
  changesSummary: string;
  correctedDeckOrSlide: any;
  modelUsed: string;
}> {
  const context = item.fullContext || enrichAndFetchContext(item.source, item.targetId, item.subTarget);
  if (!context || !context.targetSlide) {
    throw new Error(`Deste veya slayt verisi bulunamadı (Deste ID: ${item.targetId})`);
  }

  const systemInstruction = `Sen tıp fakültesi interaktif müfredat ve ders notu baş denetçisisin.
Görev: Kullanıcı interaktif öğrenme destesindeki bir slaytta veya etkileşimli öğede (gizli tablo, cloze masking boşluk doldurma, mini soru micro_quiz, mekanizma zinciri, karşılaştırma) hata bildirmiştir.
MUTLAK KURALLAR:
1. "Hata bildirimi varsa hata olabilir, hata bildiriminin geldiği konum burasıysa burada hata olabilir. Hiçbir şey doğru kabul edilemez."
2. Kullanıcı eksik açıklama girse bile bildirilen öğeyi, slayt metnini (synthesisNarrative/content), tablolardaki değerleri, gizlenen anahtar kelimeleri ve mini soruları Guyton, Robbins, Harrison tıp referanslarına göre satır satır denetle.
3. Şema ve Format Kuralları:
   - Slayt anlatım metni ASLA 60 kelimenin altına düşmemelidir (ideal: 70-150 kelime).
   - Metinler ayrık, madde imli (- **Başlık:** Açıklama) ve nefes alan yapıda olmalıdır.
   - Hiçbir alan '...' veya '…' ile kesilemez.
   - İpuçları asla cevabı sızdıramaz.
4. Hata bulursan has_error: true, bulamazsan has_error: false döndür.

Çıktı Şeması (JSON):
{
  "has_error": boolean,
  "detected_issues": ["..."],
  "medical_reasoning": "...",
  "changes_summary": "...",
  "corrected_slide": { ... } // Düzeltilmiş slayt nesnesi (slideNumber, title, synthesisNarrative, interactions vb. tam hali)
}`;

  const prompt = `LÜTFEN AŞAĞIDAKİ İNTERAKTİF DERS SLAYTINI VE GELEN BİLDİRİMİ İNCELE VE GEREKİYORSA DÜZELT:

KULLANICI BİLDİRİMİ:
- Bildirilen Alan / Öğe: ${item.subTarget?.label || item.subTarget?.targetKey || 'Slayt içeriği'}
- Konum: ${item.subTarget?.location || `Adım ${item.subTarget?.slideNumber || 'Bilinmiyor'}`}
- Kullanıcı Şikayeti: ${item.userReport.reason || 'Belirtilmedi'}
- Kullanıcı Açıklaması: ${item.userReport.details || 'Açıklama girilmedi; slayt ve etkileşimleri baştan sona bağımsız denetle.'}

DESTE BİLGİSİ:
- Deste: ${context.deckMeta?.title} (${context.deckMeta?.id})
- Konu / Kurul: ${context.deckMeta?.topic || ''} / ${context.deckMeta?.committee || ''}

MEVCUT SLAYT VERİSİ:
${JSON.stringify(context.targetSlide, null, 2)}

Yanıtını JSON şemasına tam uygun olarak ver.`;

  const { data, model } = await callFreeGeminiJson(prompt, systemInstruction);

  return {
    hasError: Boolean(data?.has_error),
    detectedIssues: Array.isArray(data?.detected_issues) ? data.detected_issues : [],
    medicalReasoning: String(data?.medical_reasoning || ''),
    changesSummary: String(data?.changes_summary || ''),
    correctedDeckOrSlide: data?.corrected_slide || null,
    modelUsed: model,
  };
}

function syncSisterQuestions(
  sisterMembers: Array<{ id: string }>,
  item: AutoRepairItem,
  ticketNo: string,
  resolutionSummary: string
) {
  try {
    const list = readJsonSafe<any[]>(PAST_QUESTIONS_FILE, []);
    let modified = false;

    for (const sister of sisterMembers) {
      const idx = list.findIndex((q) => String(q.id) === String(sister.id));
      if (idx !== -1) {
        const sq = list[idx];
        const curRevs = Array.isArray(sq.revisions) ? [...sq.revisions] : [];
        curRevs.push({
          id: `rev-sync-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
          version: curRevs.length + 1,
          ticketNo,
          editedAt: new Date().toISOString(),
          editorName: 'Yapay Zekâ Çapraz Senkronizasyon',
          editorRole: 'ai_auto_repair',
          changeSummary: `[Kardeş Soru #${item.targetId} Bildirimi ile Senkronize Edildi]: ${resolutionSummary}`,
          stem: sq.stem,
          discipline: sq.discipline,
          topic: sq.topic,
          claimedAnswer: sq.correctAnswer,
          options: sq.options,
          explanation: sq.explanation,
        });
        list[idx] = { ...sq, revisions: curRevs, updatedAt: new Date().toISOString() };
        modified = true;
      }
    }

    if (modified) {
      writeJsonAtomic(PAST_QUESTIONS_FILE, list);
      if (fs.existsSync(SRC_PAST_QUESTIONS_FILE)) {
        writeJsonAtomic(SRC_PAST_QUESTIONS_FILE, list);
      }
    }
  } catch (err) {
    console.error('[AutoRepairEngine] Kardeş soru senkronizasyon hatası:', err);
  }
}

function syncQuestionRevisionsAndReports(q: any, item: AutoRepairItem, correctedData: any): any {
  const curReports = Array.isArray(q.reports) ? [...q.reports] : [];
  const ticketNo = item.ticketNo || '#000001';

  const crossData: QuestionCrossData =
    q._crossData || item.crossData || detectQuestionCrossData(item.targetId, (item.source as any) || 'past_question');

  const shouldReleaseQuarantine = Boolean(
    item.aiAnalysis?.releaseQuarantine ||
      correctedData?.release_quarantine ||
      (crossData?.isQuarantined && (correctedData?.stem || correctedData?.reconstruction?.stem))
  );

  const prefixTags: string[] = [];
  if (shouldReleaseQuarantine) prefixTags.push('[Karantinadan Kurtarıldı]');
  if (item.aiAnalysis?.referencedRedactedId) {
    prefixTags.push(`[#${item.aiAnalysis.referencedRedactedId} Referans Alındı]`);
  }
  const prefixStr = prefixTags.length > 0 ? `${prefixTags.join(' ')} ` : '';

  const resolutionInfo = {
    status: item.aiAnalysis?.actionTaken === 'corrected' ? 'resolved' : 'verified_correct',
    ticketNo,
    resolvedAt: item.aiAnalysis?.processedAt || new Date().toISOString(),
    resolvedBy: item.aiAnalysis?.modelUsed ? `Yapay Zekâ (${item.aiAnalysis.modelUsed})` : 'Yapay Zekâ Onarım Motoru',
    resolutionSummary: `${prefixStr}${item.aiAnalysis?.changesSummary || 'Hata bildirimi incelendi ve düzenlendi.'}`,
    medicalReasoning: item.aiAnalysis?.medicalReasoning,
    detectedIssues: item.aiAnalysis?.detectedIssues,
  };

  // Raporları güncelle: Bu incelemeyle eşleşen veya soru tıbben incelendiğinde açıkta kalan tüm raporları kapat
  let matchedAny = false;
  for (let i = 0; i < curReports.length; i++) {
    const r = curReports[i];
    const matchesId = Boolean(
      (r.id && item.id.includes(r.id)) ||
      (r.id && item.userReport?.details && item.userReport.details.includes(r.id)) ||
      (r.details && item.userReport?.details && item.userReport.details.includes(r.details))
    );
    const matchesReasonAuthor = Boolean(
      r.reason === item.userReport?.reason && r.reportedBy === item.userReport?.reportedBy
    );
    const isOpen = r.status !== 'resolved' && r.status !== 'verified_correct' && r.status !== 'dismissed';

    // Eğer ID eşleşiyorsa, yazar/sebep eşleşiyorsa VEYA soru incelenip doğru bulunduysa açık raporları kapat
    if (matchesId || matchesReasonAuthor || isOpen) {
      curReports[i] = { ...curReports[i], ...resolutionInfo };
      matchedAny = true;
      if (r.id) {
        autoRepairStore.banAndRemove(`past-rep-${item.targetId}-${r.id}`);
        autoRepairStore.banAndRemove(r.id);
      }
    }
  }

  if (!matchedAny) {
    curReports.unshift({
      id: item.id,
      reason: item.userReport?.reason || 'Hata Bildirimi',
      details: item.userReport?.details || '',
      reportedBy: item.userReport?.reportedBy || 'Tıp Öğrencisi',
      reportedAt: item.userReport?.reportedAt || new Date().toISOString(),
      ...resolutionInfo,
    });
  }

  const curRevisions = Array.isArray(q.revisions) ? [...q.revisions] : [];
  // Yalnızca içerik gerçekten düzeltildiyse yeni revizyon ekle (no_change durumunda gereksiz revizyon kalabalığı yapma)
  if (item.aiAnalysis?.actionTaken === 'corrected') {
    curRevisions.push({
      id: `rev-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      version: curRevisions.length + 1,
      ticketNo,
      editedAt: new Date().toISOString(),
      editorName: resolutionInfo.resolvedBy,
      editorRole: 'ai_auto_repair',
      changeSummary: resolutionInfo.resolutionSummary,
      medicalReasoning: item.aiAnalysis?.medicalReasoning,
      detectedIssues: item.aiAnalysis?.detectedIssues,
      stem: correctedData.stem || q.stem,
      discipline: correctedData.discipline || q.discipline,
      topic: correctedData.topic || q.topic,
      claimedAnswer: correctedData.correctAnswer || correctedData.claimedAnswer || q.correctAnswer,
      options: correctedData.options || q.options,
      explanation: correctedData.explanation || q.explanation,
    });
  }

  // Var olan reconstruction nesnesini KORU ve güncelle (asla çöpe gitmesin)
  const existingRec = q.reconstruction && typeof q.reconstruction === 'object' ? q.reconstruction : {};
  const updatedReconstruction = {
    ...existingRec,
    stem: correctedData.stem || existingRec.stem || q.stem,
    options: correctedData.options || existingRec.options || q.options,
    correctAnswer: correctedData.correctAnswer || correctedData.claimedAnswer || existingRec.correctAnswer || q.correctAnswer,
    explanation: correctedData.explanation || existingRec.explanation || q.explanation,
    updatedAt: new Date().toISOString(),
  };

  const updatedTags = (Array.isArray(q.tags) ? [...q.tags] : []).filter(
    (t: string) => !shouldReleaseQuarantine || t !== 'karantina'
  );

  // Çözülen bildirimler sonrasında sikayet-* etiketlerini temizle ve puanı güncelle
  const updatedQualityIssues = (Array.isArray(q.qualityIssues) ? [...q.qualityIssues] : []).filter(
    (issue: string) => !issue.startsWith('sikayet-')
  );

  return {
    ...q,
    ...correctedData,
    isQuarantined: shouldReleaseQuarantine ? false : q.isQuarantined,
    status: shouldReleaseQuarantine ? 'verified' : (q.status === 'quarantined' ? 'verified' : q.status),
    quarantineReasons: shouldReleaseQuarantine ? [] : q.quarantineReasons,
    quarantineReason: shouldReleaseQuarantine ? undefined : q.quarantineReason,
    tags: updatedTags,
    qualityIssues: updatedQualityIssues,
    qualityScore: Math.max(Number(q.qualityScore || 0), 95),
    reconstruction: updatedReconstruction,
    reports: curReports,
    revisions: curRevisions,
    updatedAt: new Date().toISOString(),
  };
}

function syncSlideRevisionsAndReports(slide: any, item: AutoRepairItem, correctedData: any): any {
  const curReports = Array.isArray(slide.reports) ? [...slide.reports] : [];
  const ticketNo = item.ticketNo || '#000001';

  const resolutionInfo = {
    status: item.aiAnalysis?.actionTaken === 'corrected' ? 'resolved' : 'verified_correct',
    ticketNo,
    resolvedAt: item.aiAnalysis?.processedAt || new Date().toISOString(),
    resolvedBy: item.aiAnalysis?.modelUsed ? `Yapay Zekâ (${item.aiAnalysis.modelUsed})` : 'Yapay Zekâ Onarım Motoru',
    resolutionSummary: item.aiAnalysis?.changesSummary || 'Slayt içeriği incelendi ve düzeltildi.',
    medicalReasoning: item.aiAnalysis?.medicalReasoning,
    detectedIssues: item.aiAnalysis?.detectedIssues,
  };

  const repIdx = curReports.findIndex((r: any) =>
    (r.id && item.id.includes(r.id)) ||
    (r.reason === item.userReport?.reason && r.reportedBy === item.userReport?.reportedBy)
  );

  if (repIdx !== -1) {
    curReports[repIdx] = { ...curReports[repIdx], ...resolutionInfo };
  } else {
    curReports.unshift({
      id: item.id,
      reason: item.userReport?.reason || 'Slayt Bildirimi',
      details: item.userReport?.details || '',
      reportedBy: item.userReport?.reportedBy || 'Tıp Öğrencisi',
      reportedAt: item.userReport?.reportedAt || new Date().toISOString(),
      ...resolutionInfo,
    });
  }

  const curRevisions = Array.isArray(slide.revisions) ? [...slide.revisions] : [];
  curRevisions.push({
    id: `rev-slide-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
    version: curRevisions.length + 1,
    ticketNo,
    editedAt: new Date().toISOString(),
    editorName: resolutionInfo.resolvedBy,
    changeSummary: item.aiAnalysis?.changesSummary || 'Slayt güncellendi.',
    medicalReasoning: item.aiAnalysis?.medicalReasoning,
    detectedIssues: item.aiAnalysis?.detectedIssues,
  });

  return {
    ...slide,
    ...correctedData,
    reports: curReports,
    revisions: curRevisions,
  };
}

// --- Değişiklikleri Atomik Uygulama (Atomic Apply) ---
export function applyRepairToDatabase(item: AutoRepairItem, correctedData: any): { success: boolean; error?: string } {
  try {
    if (item.source === 'past_question') {
      const crossData: QuestionCrossData =
        item.crossData || item.fullContext?._crossData || detectQuestionCrossData(item.targetId, 'past_question');

      const shouldReleaseQuarantine = Boolean(
        item.aiAnalysis?.releaseQuarantine ||
          correctedData?.release_quarantine ||
          (crossData?.isQuarantined && (correctedData?.stem || correctedData?.reconstruction?.stem))
      );

      // 1. pastQuestions.json güncelle
      const list = readJsonSafe<any[]>(PAST_QUESTIONS_FILE, []);
      const idx = list.findIndex((q) => String(q.id) === String(item.targetId));
      if (idx !== -1) {
        list[idx] = syncQuestionRevisionsAndReports(list[idx], item, correctedData);
        writeJsonAtomic(PAST_QUESTIONS_FILE, list);
      }
      // 2. src/data/pastQuestions.json güncelle
      if (fs.existsSync(SRC_PAST_QUESTIONS_FILE)) {
        const srcList = readJsonSafe<any[]>(SRC_PAST_QUESTIONS_FILE, []);
        const sIdx = srcList.findIndex((q) => String(q.id) === String(item.targetId));
        if (sIdx !== -1) {
          srcList[sIdx] = syncQuestionRevisionsAndReports(srcList[sIdx], item, correctedData);
          writeJsonAtomic(SRC_PAST_QUESTIONS_FILE, srcList);
        }
      }

      // 3. Karantina dosyasından tahliye et (derived/quarantine/karantina.json)
      if (shouldReleaseQuarantine) {
        releaseQuestionFromQuarantine(item.targetId, {
          stem: correctedData.stem,
          options: correctedData.options,
        });
      }

      // 4. Birleştirme Grubu ve Kardeş Soruları Senkronize Et
      if (crossData.mergeGroup && crossData.mergeGroup.otherMembers?.length > 0) {
        syncSisterQuestions(
          crossData.mergeGroup.otherMembers,
          item,
          item.ticketNo || '#000001',
          item.aiAnalysis?.changesSummary || 'Kardeş soru onarımı tamamlandı.'
        );
      }

      return { success: true };
    }


    if (item.source === 'practice_question') {
      const list = readJsonSafe<any[]>(PRACTICE_QUESTIONS_FILE, []);
      const idx = list.findIndex((q) => String(q.id) === String(item.targetId));
      if (idx !== -1) {
        list[idx] = syncQuestionRevisionsAndReports(list[idx], item, correctedData);
        writeJsonAtomic(PRACTICE_QUESTIONS_FILE, list);
        return { success: true };
      }
      return { success: false, error: 'Örnek soru bulunamadı.' };
    }

    if (item.source === 'interactive_deck') {
      const decks = readJsonSafe<any[]>(DECKS_FILE, []);
      const deckIdx = decks.findIndex((d) => String(d.id) === String(item.targetId));
      if (deckIdx === -1) {
        return { success: false, error: 'İnteraktif deste bulunamadı.' };
      }

      const deck = decks[deckIdx];
      const slideNum = item.subTarget?.slideNumber || correctedData?.slideNumber;

      // Slaytı güncelle
      if (slideNum && Array.isArray(deck.slides)) {
        const sIdx = deck.slides.findIndex((s: any) => s.slideNumber === slideNum);
        if (sIdx !== -1) {
          deck.slides[sIdx] = syncSlideRevisionsAndReports(deck.slides[sIdx], item, correctedData);
        } else {
          deck.slides.push(syncSlideRevisionsAndReports(correctedData, item, correctedData));
        }
      } else if (correctedData?.slides) {
        // Tüm deste verildiyse
        decks[deckIdx] = { ...deck, ...correctedData };
      }

      // Senkronize Et: DECKS_FILE
      writeJsonAtomic(DECKS_FILE, decks);

      // Senkronize Et: items/<id>.json
      const itemFile = path.resolve(DECK_ITEMS_DIR, `${item.targetId}.json`);
      if (fs.existsSync(DECK_ITEMS_DIR)) {
        writeJsonAtomic(itemFile, decks[deckIdx]);
      }

      // Senkronize Et: packages/<id>/<id>.json
      const pkgFile = path.resolve(PACKAGES_DIR, item.targetId, `${item.targetId}.json`);
      if (fs.existsSync(path.dirname(pkgFile))) {
        writeJsonAtomic(pkgFile, decks[deckIdx]);
      }

      return { success: true };
    }

    return { success: false, error: `Bilinmeyen kaynak: ${item.source}` };
  } catch (err: any) {
    return { success: false, error: err.message };
  }
}

// --- Değişikliği Geri Alma (Rollback) Fonksiyonu ---
export function rollbackRepair(itemId: string): { success: boolean; message: string; error?: string } {
  const item = autoRepairStore.getById(itemId);
  if (!item) {
    return { success: false, message: 'İşlem kaydı bulunamadı.' };
  }

  if (item.status === 'rolled_back') {
    return { success: false, message: 'Bu işlem zaten daha önce geri alınmış.' };
  }

  if (!item.beforeSnapshot) {
    return { success: false, message: 'Bu işlem için geri alınabilecek orijinal veri kopyası (beforeSnapshot) mevcut değil.' };
  }

  try {
    // Eğer karantinadan çıkarılmış idiyse eski karantina kaydını geri koy
    if (item.crossData?.isQuarantined && item.crossData.quarantineRecord) {
      restoreQuestionToQuarantine(
        item.targetId,
        item.crossData.quarantineRecord,
        Boolean(item.crossData.quarantineRepair),
        item.crossData.quarantineRepair
      );
    }

    const applyRes = applyRepairToDatabase(item, item.beforeSnapshot);
    if (!applyRes.success) {
      return { success: false, message: 'Geri alma veritabanına uygulanamadı: ' + applyRes.error };
    }

    const updated = autoRepairStore.update(itemId, {
      status: 'rolled_back',
      rolledBackAt: new Date().toISOString(),
    });

    if (updated) {
      appendHistory({
        ...updated,
        aiAnalysis: {
          ...(updated.aiAnalysis || {
            detectedIssues: [],
            actionTaken: 'inconclusive',
            processedAt: new Date().toISOString(),
            modelUsed: 'system',
          }),
          medicalReasoning: (updated.aiAnalysis?.medicalReasoning || '') + ' [YÖNETİCİ TARAFINDAN GERİ ALINDI / ROLLBACK]',
          changesSummary: 'Değişiklik yönetici tarafından başarıyla geri alındı (orijinal haline döndürüldü).',
        },
      });
    }

    return {
      success: true,
      message: 'Değişiklik başarıyla geri alındı ve orijinal veri yerine konuldu.',
    };
  } catch (err: any) {
    return { success: false, message: 'Geri alma sırasında hata oluştu: ' + err.message };
  }
}

// --- Sıradaki Öğeyi İşleme (Process Item) ---
export async function processQueueItem(itemId: string): Promise<AutoRepairItem> {
  const item = autoRepairStore.getById(itemId);
  if (!item) throw new Error('İşlem kaydı bulunamadı');

  autoRepairStore.update(itemId, { status: 'processing' });

  try {
    // 1. Orijinal veriyi al ve snapshot'a yaz
    const currentContext = enrichAndFetchContext(item.source, item.targetId, item.subTarget);
    if (!currentContext) {
      throw new Error(`Hedef kaynak (${item.source} - ${item.targetId}) veritabanında bulunamadı.`);
    }

    const beforeSnapshot = JSON.parse(JSON.stringify(
      item.source === 'interactive_deck' ? currentContext.targetSlide : currentContext
    ));

    item.fullContext = currentContext;
    item.beforeSnapshot = beforeSnapshot;
    if (currentContext._crossData) {
      item.crossData = currentContext._crossData;
    }

    // 2. Yapay Zekayı Çalıştır
    let result: {
      hasError: boolean;
      detectedIssues: string[];
      medicalReasoning: string;
      changesSummary: string;
      correctedData: any;
      modelUsed: string;
      releaseQuarantine?: boolean;
      referencedRedactedId?: string;
    };

    if (item.source === 'past_question' || item.source === 'practice_question') {
      const qRes = await inspectAndRepairQuestion(item);
      result = {
        hasError: qRes.hasError,
        detectedIssues: qRes.detectedIssues,
        medicalReasoning: qRes.medicalReasoning,
        changesSummary: qRes.changesSummary,
        correctedData: qRes.correctedQuestion,
        modelUsed: qRes.modelUsed,
        releaseQuarantine: qRes.releaseQuarantine,
        referencedRedactedId: qRes.referencedRedactedId,
      };
    } else if (item.source === 'interactive_deck') {
      const dRes = await inspectAndRepairInteractiveDeck(item);
      result = {
        hasError: dRes.hasError,
        detectedIssues: dRes.detectedIssues,
        medicalReasoning: dRes.medicalReasoning,
        changesSummary: dRes.changesSummary,
        correctedData: dRes.correctedDeckOrSlide,
        modelUsed: dRes.modelUsed,
      };
    } else {
      throw new Error(`Desteklenmeyen kaynak türü: ${item.source}`);
    }

    // 3. Sonuca göre aksiyon al
    if (result.hasError && result.correctedData) {
      // Hata var ve düzeltme üretildi -> Otomatik Uygula!
      const applyRes = applyRepairToDatabase(item, {
        ...result.correctedData,
        release_quarantine: result.releaseQuarantine,
      });
      if (!applyRes.success) {
        throw new Error('Düzeltme veritabanına yazılamadı: ' + applyRes.error);
      }

      const updated = autoRepairStore.update(itemId, {
        status: 'applied',
        beforeSnapshot,
        afterSnapshot: result.correctedData,
        aiAnalysis: {
          detectedIssues: result.detectedIssues,
          medicalReasoning: result.medicalReasoning,
          actionTaken: 'corrected',
          changesSummary: result.changesSummary,
          processedAt: new Date().toISOString(),
          modelUsed: result.modelUsed,
          releaseQuarantine: result.releaseQuarantine,
          referencedRedactedId: result.referencedRedactedId,
          crossDataAuditApplied: true,
        },
      });

      if (updated) appendHistory(updated);
      return updated!;
    } else if (result.releaseQuarantine && item.source === 'past_question') {
      // Hata yok ancak soru karantinadaydı ve temiz/doğru bulunup tahliye edilmeli
      const bestCandidate = item.crossData?.bestRedactedReference;
      const releaseData = bestCandidate ? {
        stem: bestCandidate.stem,
        options: bestCandidate.options,
        correctAnswer: bestCandidate.correctAnswer,
        explanation: bestCandidate.explanation,
        release_quarantine: true,
      } : { release_quarantine: true };

      applyRepairToDatabase(item, releaseData);

      const updated = autoRepairStore.update(itemId, {
        status: 'applied',
        beforeSnapshot,
        aiAnalysis: {
          detectedIssues: result.detectedIssues,
          medicalReasoning: result.medicalReasoning,
          actionTaken: 'verified_correct',
          changesSummary: result.changesSummary || 'Soru incelendi, redaksiyonu doğrulandı ve karantinadan kurtarıldı.',
          processedAt: new Date().toISOString(),
          modelUsed: result.modelUsed,
          releaseQuarantine: true,
          referencedRedactedId: result.referencedRedactedId,
          crossDataAuditApplied: true,
        },
      });

      if (updated) appendHistory(updated);
      return updated!;
    } else {
      // Hata yok, mevcut durum doğru bulundu
      const updated = autoRepairStore.update(itemId, {
        status: 'no_change',
        beforeSnapshot,
        aiAnalysis: {
          detectedIssues: result.detectedIssues,
          medicalReasoning: result.medicalReasoning,
          actionTaken: 'verified_correct',
          changesSummary: result.changesSummary || 'Soru/içerik incelendi, tıbben doğru ve güncel bulundu.',
          processedAt: new Date().toISOString(),
          modelUsed: result.modelUsed,
          releaseQuarantine: result.releaseQuarantine,
          referencedRedactedId: result.referencedRedactedId,
          crossDataAuditApplied: true,
        },
      });

      // ÖNEMLİ: Hata olmasa bile veritabanındaki açık raporları "verified_correct" olarak işaretle!
      // Aksi takdirde hydrateExistingReportsToAutoRepair her döngüde bu raporları açık sanıp tekrar tekrar kuyruğa alır!
      if (updated) {
        try {
          applyRepairToDatabase(updated, {
            stem: beforeSnapshot?.stem || item.fullContext?.stem,
            options: beforeSnapshot?.options || item.fullContext?.options,
            correctAnswer: beforeSnapshot?.correctAnswer || item.fullContext?.correctAnswer,
            explanation: beforeSnapshot?.explanation || item.fullContext?.explanation,
            release_quarantine: result.releaseQuarantine,
          });
        } catch (dbErr) {
          console.warn(`[AutoRepairEngine] no_change rapor kapatma uyarısı (${itemId}):`, dbErr);
        }
        appendHistory(updated);
      }
      return updated!;
    }
  } catch (err: any) {
    console.error(`[AutoRepairEngine] Hata (${itemId}):`, err);
    const updated = autoRepairStore.update(itemId, {
      status: 'error',
      errorDetails: err.message || 'Bilinmeyen inceleme hatası',
      retryCount: (item.retryCount || 0) + 1,
    });
    return updated || item;
  }
}


// --- Arka Plan Otomasyon Çalıştırıcısı (Worker Daemon) ---
let isWorkerRunning = false;
let workerInterval: NodeJS.Timeout | null = null;
let isWorkerPaused = false;

export function isAutoRepairWorkerActive(): boolean {
  return !isWorkerPaused && isWorkerRunning;
}

export function setAutoRepairWorkerPaused(paused: boolean) {
  isWorkerPaused = paused;
}

export function startAutoRepairWorker() {
  if (workerInterval) return;

  isWorkerRunning = true;
  console.log('[AutoRepairEngine] 🚀 Ücretsiz Gemini Hata İnceleme & Onarım Otomasyonu başlatıldı.');

  workerInterval = setInterval(async () => {
    if (isWorkerPaused) return;

    const pending = autoRepairStore.getPending();
    if (pending.length === 0) return;

    const next = pending[0];
    try {
      console.log(`[AutoRepairEngine] ⏳ Kuyruktaki işlem işleniyor: ${next.id} (${next.source} - #${next.targetId})...`);
      await processQueueItem(next.id);
      console.log(`[AutoRepairEngine] ✅ İşlem tamamlandı: ${next.id}`);
    } catch (err: any) {
      console.warn(`[AutoRepairEngine] ⚠️ Kuyruk işlenirken hata:`, err.message);
    }
  }, 20000); // 20 saniyede bir kuyruk kontrolü
}

export function stopAutoRepairWorker() {
  if (workerInterval) {
    clearInterval(workerInterval);
    workerInterval = null;
  }
  isWorkerRunning = false;
}
