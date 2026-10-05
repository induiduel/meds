// Shared AI provider layer (server-only).
// Gemini key pool -> Groq fallback. Keys come exclusively from the server .env.
import { GoogleGenAI } from '@google/genai';

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
  // 2-3. Free tier keys from .env
  add(process.env.GEMINI_API_KEY, 'Ücretsiz Plan 1 (Gemini)');
  add(process.env.GEMINI_FREE_KEY_2, 'Ücretsiz Plan 2 (Gemini)');

  return list;
}

export function getBilledGeminiKey(): KeyInfo | null {
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
      num_gpu: 99 // Zorunlu RTX 4060 GPU Offload kuralı (-ngl 99)
    }
  };

  if (isJson) {
    payload.format = 'json';
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 45000);

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
    throw err;
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
          body: JSON.stringify(bodyPayload)
        });

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
        lastErr = err;
      }
    }
  }

  throw lastErr || new Error('Groq Cloud modelleri yanıt vermedi.');
}

// In-memory cooldown cache when Gemini free tier hits 429 quota exhaustion (prevents 4-second delays per request)
let serverGeminiQuotaCooldownUntil = 0;

// Helper to call Google Gemini Key Pool (Free keys + Billed key)
async function callGeminiPool(
  prompt: string,
  customGeminiKey?: string,
  model?: string,
  isJson: boolean = false,
  systemInstruction?: string
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

        const geminiRes = await clientAi.models.generateContent({
          model: m,
          contents: prompt,
          config: configPayload,
        });
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

  throw lastErr || new Error('Google Gemini modelleri yanıt vermedi.');
}

// =========================================================================
// Muse Spark 1.3 Free Integration (Meta / OpenCode Zen / OpenRouter)
// Kota kurtarma: Gemini ve Groq limitleri tükendiğinde devreye giren son çare modeli
// =========================================================================
export function getTieredMuseSparkKeys(customKey?: string): { key: string; label: string }[] {
  const keys: { key: string; label: string }[] = [];
  if (customKey && customKey.trim()) {
    keys.push({ key: customKey.trim(), label: 'Özel Muse Spark Anahtarı' });
  }
  const envKey = (process.env.MUSE_SPARK_API_KEY || process.env.OPENCODE_API_KEY || process.env.OPENROUTER_API_KEY || '').trim();
  if (envKey && !keys.some(x => x.key === envKey)) {
    keys.push({ key: envKey, label: 'Sunucu Muse Spark Anahtarı' });
  }
  if (keys.length === 0) {
    keys.push({ key: 'public-free-tier', label: 'Muse Spark 1.3 Ücretsiz / Contributor Havuzu' });
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
  }
): Promise<{ text: string; model: string; keyUsed: string; providerUsed: string }> {
  const keys = getTieredMuseSparkKeys(customKey);
  const baseUrls = getMuseSparkBaseUrls(options?.baseUrl);

  const candidateModels = [
    model && (model.includes('spark') || model.includes('muse')) ? model : null,
    'muse-spark-1.3-contributor-free',
    'muse-spark-1.3-free',
    'muse-spark-1.3',
    'meta/muse-spark-1.3:free',
    'meta/muse-spark-1.3',
    'meta/muse-spark-1.3-contributor'
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

  for (const baseUrl of baseUrls) {
    for (const keyInfo of keys) {
      for (const m of candidateModels) {
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
          if (keyInfo.key && keyInfo.key !== 'public-free-tier') {
            headers['Authorization'] = `Bearer ${keyInfo.key}`;
          }
          if (baseUrl.includes('openrouter')) {
            headers['HTTP-Referer'] = 'https://induiduel.github.io/meds';
            headers['X-Title'] = 'MedSoru AI Medical Tutor';
          }

          console.log(`[Muse Spark 1.3] Deneniyor: ${baseUrl} (${m}) [${keyInfo.label}]...`);

          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 20000);

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
          lastErr = err;
        }
      }
    }
  }

  throw lastErr || new Error('Muse Spark 1.3 modelleri yanıt vermedi.');
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
    messages
  } = options;

  const isJson = responseFormat === 'json';

  // 0. ÖZEL DURUM: Kullanıcı Yerel Ollama (RTX 4060 GPU) seçtiyse doğrudan yerelde çalıştır
  if (preferredProvider === 'local-ollama' || (model && (model.startsWith('gemma3') || model.startsWith('deepseek-r1') || model.startsWith('qwen3') || model.startsWith('medgemma')))) {
    console.log(`[AI Multi-Provider] 🟢 Yerel GPU Ollama doğrudan seçildi (${model || 'gemma3:4b'})...`);
    try {
      const ollamaRes = await callLocalOllama(prompt, model || 'gemma3:4b', {
        systemPrompt: systemInstruction,
        isJson,
        messages
      });
      return {
        text: ollamaRes.text,
        providerUsed: ollamaRes.providerUsed,
        planUsed: `Yerel RTX 4060 GPU (${ollamaRes.model})`,
        attemptsCount: 1,
        fallbackUsed: false
      };
    } catch (e: any) {
      console.warn('[AI Multi-Provider] ⚠️ Yerel Ollama başarısız, bulut sağlayıcılara düşülüyor:', e.message);
    }
  }
  const isMuseExplicit = preferredProvider === 'muse-spark' || Boolean(model && (model.includes('spark') || model.includes('muse')));
  const isGroqExplicit = preferredProvider === 'groq' || Boolean(model && (model.includes('llama') || model.includes('deepseek') || model.includes('gpt-oss') || model.includes('qwen')));
  const isGeminiInCooldown = Date.now() < serverGeminiQuotaCooldownUntil;

  // 1. ÖZEL DURUM: Kullanıcı doğrudan Muse Spark 1.3 seçtiyse doğrudan 1. sırada çalıştır
  if (isMuseExplicit) {
    console.log(`[AI Multi-Provider] 🟢 1. DENEME: Muse Spark 1.3 Free doğrudan seçildi...`);
    try {
      const sparkRes = await callMuseSpark(
        prompt,
        model || 'muse-spark-1.3-contributor-free',
        customMuseSparkKey,
        {
          systemPrompt: systemInstruction,
          isJson,
          messages,
          baseUrl: museSparkBaseUrl
        }
      );
      return {
        text: sparkRes.text,
        providerUsed: sparkRes.providerUsed,
        planUsed: `Muse Spark (${sparkRes.model})`,
        attemptsCount: 1,
        fallbackUsed: false
      };
    } catch (e: any) {
      console.warn('[AI Multi-Provider] ⚠️ Doğrudan Muse Spark çağrısı başarısız, Gemini/Groq havuzuna düşülüyor:', e.message);
    }
  }

  // Birincil ve İkincil (Yedek) Sağlayıcı Belirleme
  const primaryProvider: 'groq' | 'gemini' = (isGroqExplicit || (isGeminiInCooldown && preferredProvider !== 'gemini')) ? 'groq' : (preferredProvider === 'gemini' ? 'gemini' : 'gemini');
  const secondaryProvider: 'groq' | 'gemini' = primaryProvider === 'groq' ? 'gemini' : 'groq';

  let attempt1Err: any = null;
  let attempt2Err: any = null;
  let attempt3Err: any = null;

  // =========================================================================
  // 1. DENEME: BİRİNCİL SAĞLAYICI (PRIMARY ATTEMPT)
  // =========================================================================
  console.log(`[AI Multi-Provider] 🟢 1. DENEME: ${primaryProvider === 'groq' ? 'Groq Cloud' : 'Google Gemini'} ile başlatılıyor...`);
  try {
    if (primaryProvider === 'groq') {
      const groqModel = model && !model.startsWith('gemini') ? model : 'openai/gpt-oss-120b';
      const groqRes = await callGroqCloud(prompt, groqModel, customGroqKey, {
        systemPrompt: systemInstruction,
        isJson,
        messages
      });
      return {
        text: groqRes.text,
        providerUsed: `Groq Cloud (${groqRes.keyUsed})`,
        planUsed: `Groq Cloud (${groqRes.model})`,
        attemptsCount: 1,
        fallbackUsed: false
      };
    } else {
      const geminiRes = await callGeminiPool(prompt, customGeminiKey, model, isJson, systemInstruction);
      return {
        text: geminiRes.text,
        providerUsed: geminiRes.providerUsed,
        planUsed: geminiRes.planUsed,
        attemptsCount: 1,
        fallbackUsed: false
      };
    }
  } catch (err: any) {
    console.warn(`[AI Multi-Provider] ⚠️ 1. DENEME (${primaryProvider === 'groq' ? 'Groq Cloud' : 'Google Gemini'}) BAŞARISIZ:`, err.message);
    attempt1Err = err;
  }

  // =========================================================================
  // 2. DENEME: OTOMATİK YEDEK SAĞLAYICI (SECONDARY / FALLBACK ATTEMPT)
  // =========================================================================
  console.log(`[AI Multi-Provider] 🔄 2. DENEME: 1. sağlayıcı yanıt vermedi. Yedek sağlayıcı ${secondaryProvider === 'groq' ? 'Groq Cloud' : 'Google Gemini'} deneniyor...`);
  try {
    if (secondaryProvider === 'groq') {
      const groqModel = 'openai/gpt-oss-120b';
      const groqRes = await callGroqCloud(prompt, groqModel, customGroqKey, {
        systemPrompt: systemInstruction,
        isJson,
        messages
      });
      console.log(`[AI Multi-Provider] ✓ 2. DENEME (Yedek Groq Cloud ${groqRes.model}) başarıyla tamamlandı!`);
      return {
        text: groqRes.text,
        providerUsed: `Groq Cloud (${groqRes.keyUsed}) [2. Deneme Yedek]`,
        planUsed: `Groq Cloud (${groqRes.model})`,
        attemptsCount: 2,
        fallbackUsed: true
      };
    } else {
      const geminiRes = await callGeminiPool(prompt, customGeminiKey, 'gemini-3.8-flash', isJson, systemInstruction);
      console.log(`[AI Multi-Provider] ✓ 2. DENEME (Yedek Google Gemini) başarıyla tamamlandı!`);
      return {
        text: geminiRes.text,
        providerUsed: `${geminiRes.providerUsed} [2. Deneme Yedek]`,
        planUsed: geminiRes.planUsed,
        attemptsCount: 2,
        fallbackUsed: true
      };
    }
  } catch (err: any) {
    console.error(`[AI Multi-Provider] ❌ 2. DENEME (${secondaryProvider === 'groq' ? 'Groq Cloud' : 'Google Gemini'}) DE BAŞARISIZ OLDU:`, err.message);
    attempt2Err = err;
  }

  // =========================================================================
  // 3. DENEME: TÜM AI'LAR LİMİT DOLDURDUYSA DEVREYE GİREN MUSE SPARK 1.3 FREE
  // (SON ÇARE KOTA KURTARMA FAZI)
  // =========================================================================
  console.log(`[AI Multi-Provider] ⚡ 3. DENEME (KOTA KURTARMA): Tüm AI'lar limit doldurdu! Muse Spark 1.3 Free devreye alınıyor...`);
  try {
    const sparkRes = await callMuseSpark(
      prompt,
      model && model.includes('spark') ? model : 'muse-spark-1.3-contributor-free',
      customMuseSparkKey,
      {
        systemPrompt: systemInstruction,
        isJson,
        messages,
        baseUrl: museSparkBaseUrl
      }
    );
    console.log(`[AI Multi-Provider] ✓ 3. DENEME (Kurtarıcı Muse Spark 1.3 Free ${sparkRes.model}) başarıyla yanıt verdi!`);
    return {
      text: sparkRes.text,
      providerUsed: `Muse Spark 1.3 Free [Kota Kurtarıcı]`,
      planUsed: `Muse Spark (${sparkRes.model})`,
      attemptsCount: 3,
      fallbackUsed: true
    };
  } catch (sparkErr: any) {
    console.error(`[AI Multi-Provider] ❌ 3. DENEME (Muse Spark 1.3 Free) DE BAŞARISIZ OLDU:`, sparkErr.message);
    attempt3Err = sparkErr;
  }

  // =========================================================================
  // 3 KEZ DENENDİ VE ÜÇ SAĞLAYICI DA YANIT VERMEDİ -> UYARI VER
  // =========================================================================
  const primaryName = primaryProvider === 'groq' ? 'Groq Cloud' : 'Google Gemini';
  const secondaryName = secondaryProvider === 'groq' ? 'Groq Cloud' : 'Google Gemini';
  const failureError: any = new Error(
    `3 kez denendi: Hem Google Gemini hem Groq Cloud hem de Muse Spark 1.3 Free sağlayıcılarının kotaları tükendi veya yanıt veremediler. Lütfen API kotalarınızı veya internet bağlantınızı kontrol edin.`
  );
  failureError.attemptsCount = 3;
  failureError.isTwoAttemptsFailed = true;
  failureError.isThreeAttemptsFailed = true;
  failureError.primaryError = attempt1Err?.message || 'Bilinmeyen hata';
  failureError.secondaryError = attempt2Err?.message || 'Bilinmeyen hata';
  failureError.tertiaryError = attempt3Err?.message || 'Bilinmeyen hata';
  throw failureError;
}
