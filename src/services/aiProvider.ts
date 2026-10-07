// Shared AI provider layer (server-only).
// Gemini key pool -> Groq fallback. Keys come exclusively from the server .env.
import fs from 'fs';
import path from 'path';
import { GoogleGenAI } from '@google/genai';

// Her model ailesi ve sağlayıcı için özelleştirilmiş zaman aşımı süreleri (milisaniye)
export const MODEL_TIMEOUTS_MS: Record<string, number> = {
  // Yerel GPU Modelleri (RTX 4060)
  'gemma3:4b': 45000,           // 45 saniye
  'medgemma1.5:4b': 45000,      // 45 saniye
  'qwen3:1.7b-q8_0': 30000,     // 30 saniye (ultra hafif)
  'deepseek-r1:8b': 120000,     // 120 saniye (2 dakika - derin CoT mantık yürütme)
  'medsoru-d3': 60000,          // 60 saniye (özel eğitilmiş QLoRA)
  'local-default': 60000,       // 60 saniye varsayılan yerel

  // Bulut Modelleri
  'gemini-3.8-flash': 25000,    // 25 saniye (hızlı bulut API)
  'gemini-flash-latest': 25000,
  'openai/gpt-oss-120b': 45000, // 45 saniye (Groq ultra hızlı inference)
  'qwen/qwen3.8-27b': 40000,
  'openai/gpt-oss-20b': 30000,
  'muse-spark-1.3-contributor-free': 35000, // 35 saniye
  'cloud-default': 35000
};

export function getModelTimeoutMs(modelName?: string, isLocal: boolean = false): number {
  if (modelName && MODEL_TIMEOUTS_MS[modelName]) {
    return MODEL_TIMEOUTS_MS[modelName];
  }
  if (modelName) {
    if (modelName.includes('deepseek-r1')) return 120000;
    if (modelName.includes('gpt-oss-120b')) return 45000;
    if (modelName.includes('flash')) return 25000;
    if (modelName.includes('qwen3:1.7b')) return 30000;
  }
  return isLocal ? MODEL_TIMEOUTS_MS['local-default'] : MODEL_TIMEOUTS_MS['cloud-default'];
}

// Kalıcı Yapay Zeka Hata Kayıt Sistemi (Log Recording)
const AI_ERROR_LOG_PATH = path.join(process.cwd(), 'data', 'ai_error_logs.json');

export interface AiErrorRecord {
  id: string;
  timestamp: string;
  provider: string;
  model: string;
  promptSnippet: string;
  errorMessage: string;
  errorStack?: string;
  isTimeout: boolean;
  status: 'unresolved' | 'investigating' | 'resolved';
}

export function logAiExecutionError(entry: {
  provider: string;
  model: string;
  prompt: string;
  error: any;
}): void {
  try {
    const isTimeout = /abort|timeout|timed out|zaman aşımı/i.test(entry.error?.message || '');
    const newRecord: AiErrorRecord = {
      id: `err-log-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      timestamp: new Date().toISOString(),
      provider: entry.provider,
      model: entry.model,
      promptSnippet: (entry.prompt || '').slice(0, 250),
      errorMessage: entry.error?.message || String(entry.error),
      errorStack: entry.error?.stack ? entry.error.stack.slice(0, 500) : undefined,
      isTimeout,
      status: 'unresolved'
    };

    let logs: AiErrorRecord[] = [];
    if (fs.existsSync(AI_ERROR_LOG_PATH)) {
      try {
        const raw = fs.readFileSync(AI_ERROR_LOG_PATH, 'utf8');
        logs = JSON.parse(raw);
        if (!Array.isArray(logs)) logs = [];
      } catch (_) {
        logs = [];
      }
    }

    logs.unshift(newRecord);
    // Maksimum 200 en güncel hata kaydını tut
    if (logs.length > 200) {
      logs = logs.slice(0, 200);
    }

    fs.writeFileSync(AI_ERROR_LOG_PATH, JSON.stringify(logs, null, 2), 'utf8');
    console.error(`[AI Error Logger] 📝 Hata kaydedildi: [${entry.provider} - ${entry.model}] -> ${newRecord.errorMessage}`);
  } catch (err: any) {
    console.warn('[AI Error Logger] ⚠️ Hata loglanırken dosya yazma sorunu:', err.message);
  }
}

export function getAiErrorLogs(): AiErrorRecord[] {
  try {
    if (fs.existsSync(AI_ERROR_LOG_PATH)) {
      const raw = fs.readFileSync(AI_ERROR_LOG_PATH, 'utf8');
      return JSON.parse(raw);
    }
  } catch (_) {}
  return [];
}

// Multi-Tier Gemini Key Pool & Groq Cloud Engine
export interface KeyInfo {
  key: string;
  label: string;
  isBilled: boolean;
}

// All provider keys come from the server environment (.env). Never hardcode keys here:
// anything committed to the repo or shipped in the client bundle is public.
const isRealKey = (k?: string): k is string =>
  Boolean(k && k.trim() && !/^MY_[A-Z0-9_]+$/.test(k.trim()));

export function getFreeGeminiKeys(customKey?: string): KeyInfo[] {
  const list: KeyInfo[] = [];
  const add = (key: string | undefined, label: string) => {
    if (isRealKey(key) && !list.some(x => x.key === key.trim())) {
      list.push({ key: key.trim(), label, isBilled: false });
    }
  };

  // 1. Custom key passed by user/admin (their own key, sent per request)
  add(customKey, 'Kullanıcı Özel Anahtarı');
  // 2-4. Free tier keys from .env
  add(process.env.GEMINI_API_KEY, 'Ücretsiz Plan 1 (Gemini)');
  add(process.env.GEMINI_FREE_KEY_2, 'Ücretsiz Plan 2 (Gemini)');
  // GEMINI_BACKUP_KEY ücretliydi: yalnız Faz 14 kullanır (PHASE14_PAID_GEMINI_KEY), site kullanmaz

  return list;
}

// MEDS_FREE_ONLY (varsayılan açık): yalnız ücretsiz anahtarlar; faturalı anahtar hiç kullanılmaz.
export const FREE_ONLY = process.env.MEDS_FREE_ONLY !== '0';

export function getBilledGeminiKey(): KeyInfo | null {
  if (FREE_ONLY) return null;
  const billed = process.env.GEMINI_BILLED_KEY;
  if (!isRealKey(billed)) return null;
  return { key: billed.trim(), label: 'Faturalandırmalı Plan (Son Çare)', isBilled: true };
}

export function getTieredGeminiKeys(customKey?: string): KeyInfo[] {
  const billed = getBilledGeminiKey();
  const free = getFreeGeminiKeys(customKey);
  return billed && !free.some(x => x.key === billed.key) ? [...free, billed] : free;
}

// Helper for resilient Gemini API calls with fallback
export async function generateGeminiWithFallback(contents: any, config?: any) {
  const geminiKeys = getTieredGeminiKeys();
  const models = ['gemini-3.8-flash', 'gemini-flash-latest'];
  let lastErr: any = null;

  for (const keyInfo of geminiKeys) {
    for (const m of models) {
      try {
        const client = new GoogleGenAI({ apiKey: keyInfo.key });
        return await client.models.generateContent({
          model: m,
          contents,
          config,
        });
      } catch (e: any) {
        lastErr = e;
      }
    }
  }
  throw lastErr || new Error('Gemini API yanıt vermedi.');
}

// Groq Cloud Integration (Fast & Free OpenAI GPT-OSS 120B / Qwen / Llama 3.3)
export function getTieredGroqKeys(customGroqKey?: string): { key: string; label: string }[] {
  const keys: { key: string; label: string }[] = [];
  const add = (key: string | undefined, label: string) => {
    if (isRealKey(key) && !keys.some(x => x.key === key.trim())) {
      keys.push({ key: key.trim(), label });
    }
  };
  add(customGroqKey, 'Özel / Admin Groq Anahtarı');
  add(process.env.GROQ_API_KEY, '1. Groq Anahtarı');
  add(process.env.GROQ_API_KEY_2, '2. Groq Anahtarı (Yedek)');
  return keys;
}

// =========================================================================
// Yerel GPU Ollama Entegrasyonu (RTX 4060 - Qwen2.5 / Gemma 3 / DeepSeek-R1 / qLoRA)
// Sıfır Maliyet & Tamamen Yerel Donanım
// =========================================================================
export const OLLAMA_HOST = process.env.OLLAMA_HOST || process.env.OLLAMA_URL || 'http://127.0.0.1:11434';

export async function callLocalOllama(
  prompt: string,
  model: string = 'gemma3:4b',
  options?: {
    systemPrompt?: string;
    isJson?: boolean;
    messages?: { role: string; content: string }[];
    timeoutMs?: number;
  }
): Promise<{ text: string; model: string; keyUsed: string; providerUsed: string }> {
  const isJson = options?.isJson === true;
  const sysMsg = options?.systemPrompt || (isJson
    ? 'Sen Tıp Fakültesi komite ve TUS sınavları konusunda uzmanlaşmış kıdemli bir tıp akademisyenisin. İstenen sınav sorusunu harfiyen belirtilen geçerli JSON şemasında oluştur.'
    : 'Sen Tıp Fakültesi öğrencilerine sınav sorularında rehberlik eden kıdemli bir tıp hocası ve eğitmenisin.');

  const chatMessages: any[] = options?.messages && options.messages.length > 0
    ? [
        { role: 'system', content: sysMsg },
        ...options.messages
      ]
    : [
        { role: 'system', content: sysMsg },
        { role: 'user', content: prompt }
      ];

  const payload: any = {
    model: model || 'gemma3:4b',
    messages: chatMessages,
    stream: false,
    options: {
      temperature: isJson ? 0.2 : 0.4,
      num_ctx: 2048, // Optimize context size to prevent CUDA OOM on 8GB VRAM
      num_gpu: 99 // Zorunlu RTX 4060 GPU Offload kuralı (-ngl 99)
    }
  };

  if (isJson) {
    payload.format = 'json';
  }

  // Model bazlı dinamik zaman aşımı süresi
  const effectiveTimeout = options?.timeoutMs || getModelTimeoutMs(model, true);
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), effectiveTimeout);

  try {
    const res = await fetch(`${OLLAMA_HOST}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Ollama Hatası (${res.status}): ${errText}`);
    }

    const data: any = await res.json();
    let text = data.message?.content || (isJson ? '{}' : '');
    if (isJson) {
      text = text.replace(/^```json\s*/i, '').replace(/\s*```$/i, '').trim();
    }
    return {
      text,
      model,
      keyUsed: 'Yerel Donanım (RTX 4060 GPU)',
      providerUsed: `Yerel Ollama (${model})`
    };
  } catch (err: any) {
    clearTimeout(timeoutId);
    const isTimeout = /abort|timeout|timed out/i.test(err.message || '') || controller.signal.aborted;
    const finalErr = isTimeout
      ? new Error(`Yerel model (${model}) ${Math.round(effectiveTimeout / 1000)} saniye içinde yanıt veremedi (Zaman Aşımı).`)
      : err;
    logAiExecutionError({
      provider: 'ollama',
      model,
      prompt,
      error: finalErr
    });
    throw finalErr;
  }
}

export async function callGroqCloud(
  prompt: string,
  model: string = 'openai/gpt-oss-120b',
  customGroqKey?: string,
  options?: {
    systemPrompt?: string;
    isJson?: boolean;
    messages?: { role: string; content: string }[];
    timeoutMs?: number;
  }
): Promise<{ text: string; model: string; keyUsed: string }> {
  const keys = getTieredGroqKeys(customGroqKey);
  if (keys.length === 0) {
    throw new Error('Groq Cloud API anahtarı (GROQ_API_KEY) tanımlı değil. Lütfen .env dosyasına ekleyin veya Ayarlar panelinden girin.');
  }

  const candidateModels = [
    model && !model.startsWith('gemini') ? model : null,
    'openai/gpt-oss-120b',
    'qwen/qwen3.8-27b',
    'openai/gpt-oss-20b',
  ].filter(Boolean) as string[];

  const isJson = options?.isJson !== false;
  const sysMsg = options?.systemPrompt || (isJson
    ? 'Sen Tıp Fakültesi komite ve TUS sınavları konusunda uzmanlaşmış kıdemli bir tıp akademisyenisin. İstenen sınav sorusunu harfiyen belirtilen geçerli JSON şemasında oluştur.'
    : 'Sen Tıp Fakültesi öğrencilerine sınav sorularında rehberlik eden kıdemli bir tıp hocası ve eğitmenisin.');

  const chatMessages: any[] = options?.messages && options.messages.length > 0
    ? [
        { role: 'system', content: sysMsg },
        ...options.messages
      ]
    : [
        { role: 'system', content: sysMsg },
        { role: 'user', content: prompt }
      ];

  let lastErr: any = null;
  for (let ki = 0; ki < keys.length; ki++) {
    const currentKey = keys[ki];
    for (const m of candidateModels) {
      const effectiveTimeout = options?.timeoutMs || getModelTimeoutMs(m, false);
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), effectiveTimeout);

      try {
        const bodyPayload: any = {
          model: m,
          messages: chatMessages,
          temperature: isJson ? 0.2 : 0.4
        };
        if (isJson) {
          bodyPayload.response_format = { type: 'json_object' };
        }

        const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${currentKey.key}`,
          },
          body: JSON.stringify(bodyPayload),
          signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (!res.ok) {
          const errText = await res.text();
          console.warn(`[Groq Cloud] ⚠️ ${currentKey.label} (${m}) başarısız:`, errText);
          lastErr = new Error(`Groq Cloud Hatası (${res.status}): ${errText}`);
          const isQuota = /429|rate_limit|tokens/i.test(errText) || res.status === 429;
          if (isQuota) {
            console.log(`[Groq Cloud] 🔄 ${currentKey.label} limitine ulaşıldı, bir sonraki Groq anahtarına geçiliyor...`);
            break;
          }
          continue;
        }

        const data: any = await res.json();
        const text = data.choices?.[0]?.message?.content || (isJson ? '{}' : '');
        return { text, model: m, keyUsed: currentKey.label };
      } catch (err: any) {
        clearTimeout(timeoutId);
        const isTimeout = /abort|timeout|timed out/i.test(err.message || '') || controller.signal.aborted;
        lastErr = isTimeout
          ? new Error(`Groq modeli (${m}) ${Math.round(effectiveTimeout / 1000)} saniye içinde yanıt veremedi (Zaman Aşımı).`)
          : err;
      }
    }
  }

  const finalError = lastErr || new Error('Groq Cloud modelleri yanıt vermedi.');
  logAiExecutionError({
    provider: 'groq',
    model,
    prompt,
    error: finalError
  });
  throw finalError;
}

// In-memory cooldown cache when Gemini free tier hits 429 quota exhaustion (prevents 4-second delays per request)
let serverGeminiQuotaCooldownUntil = 0;

// Helper to call Google Gemini Key Pool (Free keys + Billed key)
async function callGeminiPool(
  prompt: string,
  customGeminiKey?: string,
  model?: string,
  isJson: boolean = false,
  systemInstruction?: string,
  timeoutMs?: number
): Promise<{ text: string; providerUsed: string; planUsed: string }> {
  const isGeminiInCooldown = Date.now() < serverGeminiQuotaCooldownUntil;
  if (isGeminiInCooldown) {
    throw new Error('Google Gemini API kotası aşıldığı için beklemede (429 RESOURCE_EXHAUSTED).');
  }

  const allGeminiKeys = getTieredGeminiKeys(customGeminiKey);
  if (allGeminiKeys.length === 0) {
    throw new Error('Gemini API anahtarı (GEMINI_API_KEY) sunucu .env dosyasında tanımlı değil.');
  }
  let lastErr: any = null;

  for (let i = 0; i < allGeminiKeys.length; i++) {
    const keyInfo = allGeminiKeys[i];
    const candidateModels = (model && model.startsWith('gemini'))
      ? [model, 'gemini-3.8-flash'].filter((v, idx, arr) => arr.indexOf(v) === idx)
      : ['gemini-3.8-flash'];

    for (const m of candidateModels) {
      const effectiveTimeout = timeoutMs || getModelTimeoutMs(m, false);
      try {
        console.log(`[Gemini Engine] ${keyInfo.label} (${m}) deneniyor... (Sıra: ${i + 1}/${allGeminiKeys.length})`);
        const clientAi = new GoogleGenAI({ apiKey: keyInfo.key });
        const configPayload: any = {};
        if (isJson) {
          configPayload.responseMimeType = 'application/json';
        }
        if (systemInstruction) {
          configPayload.systemInstruction = systemInstruction;
        }

        const callPromise = clientAi.models.generateContent({
          model: m,
          contents: prompt,
          config: configPayload,
        });

        const timeoutPromise = new Promise<never>((_, reject) => {
          setTimeout(() => reject(new Error(`Gemini modeli (${m}) ${Math.round(effectiveTimeout / 1000)} saniye içinde yanıt veremedi (Zaman Aşımı).`)), effectiveTimeout);
        });

        const geminiRes: any = await Promise.race([callPromise, timeoutPromise]);
        const text = geminiRes.text || (isJson ? '{}' : '');
        serverGeminiQuotaCooldownUntil = 0;
        return {
          text,
          providerUsed: keyInfo.isBilled ? 'Google Gemini (Faturalı)' : 'Google Gemini',
          planUsed: `${keyInfo.label} (${m})`,
        };
      } catch (err: any) {
        lastErr = err;
        const isQuota = /429|RESOURCE_EXHAUSTED|spending cap|quota/i.test(err.message || '');
        if (isQuota) {
          serverGeminiQuotaCooldownUntil = Date.now() + 5 * 60 * 1000;
          console.warn(`[Gemini Engine] ⚠️ ${keyInfo.label} (${m}) kotaya takıldı (429).`);
          break;
        }
      }
    }
  }

  const finalError = lastErr || new Error('Google Gemini modelleri yanıt vermedi.');
  logAiExecutionError({
    provider: 'gemini',
    model: model || 'gemini-3.8-flash',
    prompt,
    error: finalError
  });
  throw finalError;
}

// =========================================================================
// Muse Spark 1.3 Free Integration (Meta / OpenCode Zen / OpenRouter)
// Kota kurtarma: Gemini ve Groq limitleri tükendiğinde devreye giren son çare modeli
// =========================================================================
export function getTieredMuseSparkKeys(customKey?: string): { key: string; label: string }[] {
  const keys: { key: string; label: string }[] = [];
  if (customKey && isRealKey(customKey)) {
    keys.push({ key: customKey.trim(), label: 'Özel Muse Spark / OpenRouter Anahtarı' });
  }
  const envKey = (process.env.MUSE_SPARK_API_KEY || process.env.OPENCODE_API_KEY || process.env.OPENROUTER_API_KEY || '').trim();
  if (isRealKey(envKey) && !keys.some(x => x.key === envKey)) {
    keys.push({ key: envKey, label: 'Sunucu Muse Spark Anahtarı' });
  }
  return keys;
}

export function getMuseSparkBaseUrls(customUrl?: string): string[] {
  const urls: string[] = [];
  if (customUrl && customUrl.trim()) {
    urls.push(customUrl.trim().replace(/\/+$/, ''));
  }
  if (process.env.MUSE_SPARK_BASE_URL) {
    urls.push(process.env.MUSE_SPARK_BASE_URL.trim().replace(/\/+$/, ''));
  }
  urls.push('https://opencode.ai/zen/v1');
  urls.push('https://openrouter.ai/api/v1');
  urls.push('https://api.meta.ai/v1');
  return [...new Set(urls)];
}

export async function callMuseSpark(
  prompt: string,
  model: string = 'muse-spark-1.3-contributor-free',
  customKey?: string,
  options?: {
    systemPrompt?: string;
    isJson?: boolean;
    messages?: { role: string; content: string }[];
    baseUrl?: string;
    timeoutMs?: number;
  }
): Promise<{ text: string; model: string; keyUsed: string; providerUsed: string }> {
  const keys = getTieredMuseSparkKeys(customKey);
  const baseUrls = getMuseSparkBaseUrls(options?.baseUrl);

  const candidateModels = [
    model && (model.includes('spark') || model.includes('muse') || model.includes('openrouter')) ? model : null,
    'muse-spark-1.3-contributor-free',
    'muse-spark-1.3-free',
    'muse-spark-1.3',
    'liquid/lfm-2.5-2.6b:free',
    'qwen/qwen3.8-27b:free',
    'google/gemma-4-31b-it:free',
    'nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free',
    'meta/muse-spark-1.3:free',
    'meta/muse-spark-1.3'
  ].filter(Boolean) as string[];

  const isJson = options?.isJson !== false;
  const sysMsg = options?.systemPrompt || (isJson
    ? 'Sen Tıp Fakültesi komite ve TUS sınavları konusunda uzmanlaşmış kıdemli bir tıp akademisyenisin. İstenen sınav sorusunu harfiyen belirtilen geçerli JSON şemasında oluştur.'
    : 'Sen Tıp Fakültesi öğrencilerine sınav sorularında rehberlik eden kıdemli bir tıp hocası ve eğitmenisin.');

  const chatMessages: any[] = options?.messages && options.messages.length > 0
    ? [
        { role: 'system', content: sysMsg },
        ...options.messages
      ]
    : [
        { role: 'system', content: sysMsg },
        { role: 'user', content: prompt }
      ];

  if (keys.length === 0) {
    throw new Error('Muse Spark / OpenRouter API anahtarı tanımlı değil (MUSE_SPARK_API_KEY). Lütfen .env dosyasına ekleyin veya geçerli bir API anahtarı girin.');
  }

  let lastErr: any = null;

  for (const baseUrl of baseUrls) {
    for (const keyInfo of keys) {
      for (const m of candidateModels) {
        const effectiveTimeout = options?.timeoutMs || getModelTimeoutMs(m, false);
        try {
          const bodyPayload: any = {
            model: m,
            messages: chatMessages,
            temperature: isJson ? 0.2 : 0.4
          };
          if (isJson) {
            bodyPayload.response_format = { type: 'json_object' };
          }

          const headers: Record<string, string> = {
            'Content-Type': 'application/json'
          };
          if (keyInfo.key) {
            headers['Authorization'] = `Bearer ${keyInfo.key}`;
          }
          if (baseUrl.includes('openrouter')) {
            headers['HTTP-Referer'] = 'https://induiduel.github.io/meds';
            headers['X-Title'] = 'MedSoru AI Medical Tutor';
          }

          console.log(`[Muse Spark 1.3] Deneniyor: ${baseUrl} (${m}) [${keyInfo.label}]...`);

          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), effectiveTimeout);

          const res = await fetch(`${baseUrl}/chat/completions`, {
            method: 'POST',
            headers,
            body: JSON.stringify(bodyPayload),
            signal: controller.signal
          });
          clearTimeout(timeoutId);

          if (!res.ok) {
            const errText = await res.text();
            console.warn(`[Muse Spark 1.3] ⚠️ ${baseUrl} (${m}) hatası:`, errText);
            lastErr = new Error(`Muse Spark Hatası (${res.status}): ${errText}`);
            continue;
          }

          const data: any = await res.json();
          let text = data.choices?.[0]?.message?.content || (isJson ? '{}' : '');
          if (isJson) {
            text = text.replace(/^```json\s*/i, '').replace(/\s*```$/i, '').trim();
          }
          return {
            text,
            model: m,
            keyUsed: keyInfo.label,
            providerUsed: `Muse Spark 1.3 Free (${keyInfo.label})`
          };
        } catch (err: any) {
          const isTimeout = /abort|timeout|timed out/i.test(err.message || '');
          lastErr = isTimeout
            ? new Error(`Muse Spark modeli (${m}) ${Math.round(effectiveTimeout / 1000)} saniye içinde yanıt veremedi (Zaman Aşımı).`)
            : err;
        }
      }
    }
  }

  const finalError = lastErr || new Error('Muse Spark 1.3 modelleri yanıt vermedi.');
  logAiExecutionError({
    provider: 'muse-spark',
    model,
    prompt,
    error: finalError
  });
  throw finalError;
}

// Resilient Multi-Provider AI Caller with Automated 3-Phase Failover
// Deneme 1: Birincil Sağlayıcı (Gemini / Groq / Muse Spark)
// Deneme 2: Alternatif Yedek Sağlayıcı (Groq / Gemini)
// Deneme 3 (Kurtarıcı / Son Çare): Tüm AI'lar Limit Doldurduysa Otomatik Devreye Giren Muse Spark 1.3 Free
export async function generateResilientMedicalAi(options: {
  prompt: string;
  customGeminiKey?: string;
  customGroqKey?: string;
  customMuseSparkKey?: string;
  museSparkBaseUrl?: string;
  preferredProvider?: 'gemini' | 'groq' | 'muse-spark' | 'local-ollama' | 'auto';
  model?: string;
  responseFormat?: 'json' | 'text';
  systemInstruction?: string;
  messages?: { role: string; content: string }[];
  allowCloudFallback?: boolean;
  timeoutMs?: number;
}): Promise<{ text: string; providerUsed: string; planUsed: string; attemptsCount: number; fallbackUsed?: boolean }> {
  const {
    prompt,
    customGeminiKey,
    customGroqKey,
    customMuseSparkKey,
    museSparkBaseUrl,
    preferredProvider = 'auto',
    model,
    responseFormat = 'json',
    systemInstruction,
    messages,
    allowCloudFallback = true,
    timeoutMs
  } = options;

  const isJson = responseFormat === 'json';

  // =========================================================================
  // 1. BASAMAK: YEREL GPU MODELLERİ (RTX 4060)
  // Kullanıcı yerel moddaysa veya model yerel ise, sırasıyla yerel modelleri dene.
  // =========================================================================
  const isLocalPreferred = preferredProvider === 'local-ollama' || preferredProvider === 'ollama' ||
    Boolean(model && (model.startsWith('gemma3') || model.startsWith('deepseek-r1') || model.startsWith('qwen3') || model.startsWith('medgemma')));

  if (isLocalPreferred) {
    // Sırayla denenecek yerel modeller havuzu
    const requestedModel = model || 'gemma3:4b';
    const candidateLocalModels = [requestedModel, 'gemma3:4b', 'deepseek-r1:8b', 'qwen3:1.7b-q8_0', 'medgemma1.5:4b']
      .filter((m, idx, arr) => arr.indexOf(m) === idx);

    for (const localCandidate of candidateLocalModels) {
      console.log(`[AI Multi-Provider] 🟢 1. BASAMAK: Yerel RTX 4060 GPU deneniyor (${localCandidate})...`);
      try {
        const ollamaRes = await callLocalOllama(prompt, localCandidate, {
          systemPrompt: systemInstruction,
          isJson,
          messages,
          timeoutMs: timeoutMs || 30000 // Hızlı fallback için 30sn
        });
        return {
          text: ollamaRes.text,
          providerUsed: ollamaRes.providerUsed,
          planUsed: `Yerel RTX 4060 GPU (${ollamaRes.model})`,
          attemptsCount: 1,
          fallbackUsed: localCandidate !== requestedModel
        };
      } catch (localErr: any) {
        console.warn(`[AI Multi-Provider] ⚠️ Yerel model (${localCandidate}) başarısız:`, localErr.message);
      }
    }

    if (!allowCloudFallback) {
      throw new Error(`Yerel RTX 4060 GPU modelleri yanıt veremedi ve bulut fallback'i devre dışı.`);
    }
    console.warn('[AI Multi-Provider] ⚠️ Yerel GPU modellerinin HİÇBİRİ yanıt vermedi! Otomatik bulut basamağına geçiliyor: yerel -> groq -> muse -> gemini');
  }

  // =========================================================================
  // 2. BASAMAK: GROQ CLOUD (GPT-OSS 120B / Llama 3)
  // Yerel çalışmadığında İLK BULUT SEÇENEĞİ her zaman Groq'tur.
  // =========================================================================
  console.log(`[AI Multi-Provider] 🟢 2. BASAMAK: Groq Cloud (openai/gpt-oss-120b) devreye alınıyor...`);
  try {
    const groqModel = 'openai/gpt-oss-120b';
    const groqRes = await callGroqCloud(prompt, groqModel, customGroqKey, {
      systemPrompt: systemInstruction,
      isJson,
      messages
    });
    console.log(`[AI Multi-Provider] ✓ 2. BASAMAK (Groq Cloud ${groqRes.model}) başarıyla yanıt verdi!`);
    return {
      text: groqRes.text,
      providerUsed: `Groq Cloud (${groqRes.keyUsed})`,
      planUsed: `Groq Cloud (${groqRes.model})`,
      attemptsCount: isLocalPreferred ? 2 : 1,
      fallbackUsed: isLocalPreferred
    };
  } catch (groqErr: any) {
    console.warn(`[AI Multi-Provider] ⚠️ 2. BASAMAK (Groq Cloud) başarısız oldu:`, groqErr.message);
  }

  // =========================================================================
  // 3. BASAMAK: MUSE SPARK 1.3 FREE (SINIRSIZ / ÜCRETSİZ KATMAN)
  // Groq yanıt vermezse devreye giren 2. bulut alternatifi
  // =========================================================================
  console.log(`[AI Multi-Provider] ⚡ 3. BASAMAK: Muse Spark 1.3 Free devreye alınıyor...`);
  try {
    const sparkRes = await callMuseSpark(
      prompt,
      'muse-spark-1.3-contributor-free',
      customMuseSparkKey,
      {
        systemPrompt: systemInstruction,
        isJson,
        messages,
        baseUrl: museSparkBaseUrl
      }
    );
    console.log(`[AI Multi-Provider] ✓ 3. BASAMAK (Muse Spark 1.3 Free ${sparkRes.model}) başarıyla yanıt verdi!`);
    return {
      text: sparkRes.text,
      providerUsed: `Muse Spark 1.3 Free [Yedek]`,
      planUsed: `Muse Spark (${sparkRes.model})`,
      attemptsCount: isLocalPreferred ? 3 : 2,
      fallbackUsed: true
    };
  } catch (sparkErr: any) {
    console.warn(`[AI Multi-Provider] ⚠️ 3. BASAMAK (Muse Spark 1.3 Free) başarısız oldu:`, sparkErr.message);
  }

  // =========================================================================
  // 4. BASAMAK: GOOGLE GEMINI FLASH (EN SON SEÇENEK)
  // Yerel, Groq ve Muse başarısız olduğunda en son çare olarak Gemini denenir.
  // =========================================================================
  console.log(`[AI Multi-Provider] 🛡️ 4. BASAMAK (EN SON SEÇENEK): Google Gemini Flash deneniyor...`);
  try {
    const geminiModel = 'gemini-3.8-flash';
    const geminiRes = await callGeminiPool(prompt, customGeminiKey, geminiModel, isJson, systemInstruction);
    console.log(`[AI Multi-Provider] ✓ 4. BASAMAK (Google Gemini Flash ${geminiRes.model}) başarıyla yanıt verdi!`);
    return {
      text: geminiRes.text,
      providerUsed: `${geminiRes.providerUsed} [Son Çare Yedek]`,
      planUsed: geminiRes.planUsed,
      attemptsCount: isLocalPreferred ? 4 : 3,
      fallbackUsed: true
    };
  } catch (geminiErr: any) {
    console.error(`[AI Multi-Provider] ❌ 4. BASAMAK (Google Gemini Flash) DA BAŞARISIZ OLDU:`, geminiErr.message);
  }

  // =========================================================================
  // TÜM BASAMAKLAR BAŞARISIZ OLDUĞUNDA HATA FIRLAT
  // =========================================================================
  const failureError: any = new Error(
    `Tüm yapay zeka basamakları denendi ve hiçbiri yanıt veremedi (Sıra: Yerel GPU RTX 4060 -> Groq Cloud -> Muse Spark -> Google Gemini). Lütfen internet bağlantınızı veya API durumunuzu kontrol edin.`
  );
  failureError.attemptsCount = 4;
  failureError.isAllFailed = true;
  throw failureError;
}
