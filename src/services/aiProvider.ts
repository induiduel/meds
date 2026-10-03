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

// Resilient Multi-Provider AI Caller with Automated 2-Phase Failover
// Deneme 1: Birincil Sağlayıcı -> Deneme 2: Alternatif Yedek Sağlayıcı (Gemini <-> Groq)
// 2 kez denenip ikisi de başarısız olursa açık uyarı fırlatır.
export async function generateResilientMedicalAi(options: {
  prompt: string;
  customGeminiKey?: string;
  customGroqKey?: string;
  preferredProvider?: 'gemini' | 'groq' | 'auto';
  model?: string;
  responseFormat?: 'json' | 'text';
  systemInstruction?: string;
  messages?: { role: string; content: string }[];
}): Promise<{ text: string; providerUsed: string; planUsed: string; attemptsCount: number; fallbackUsed?: boolean }> {
  const {
    prompt,
    customGeminiKey,
    customGroqKey,
    preferredProvider = 'auto',
    model,
    responseFormat = 'json',
    systemInstruction,
    messages
  } = options;

  const isJson = responseFormat === 'json';
  const isGroqExplicit = preferredProvider === 'groq' || Boolean(model && (model.includes('llama') || model.includes('deepseek') || model.includes('gpt-oss') || model.includes('qwen')));
  const isGeminiInCooldown = Date.now() < serverGeminiQuotaCooldownUntil;

  // Birincil ve İkincil (Yedek) Sağlayıcı Belirleme
  const primaryProvider: 'groq' | 'gemini' = (isGroqExplicit || (isGeminiInCooldown && preferredProvider !== 'gemini')) ? 'groq' : (preferredProvider === 'gemini' ? 'gemini' : 'gemini');
  const secondaryProvider: 'groq' | 'gemini' = primaryProvider === 'groq' ? 'gemini' : 'groq';

  let attempt1Err: any = null;
  let attempt2Err: any = null;

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
  // 2 KEZ DENENDİ VE İKİ SAĞLAYICI DA YANIT VERMEDİ -> UYARI VER
  // =========================================================================
  const primaryName = primaryProvider === 'groq' ? 'Groq Cloud' : 'Google Gemini';
  const secondaryName = secondaryProvider === 'groq' ? 'Groq Cloud' : 'Google Gemini';
  const failureError: any = new Error(
    `2 kez denendi: Hem 1. sağlayıcı (${primaryName}) hem de 2. alternatif sağlayıcı (${secondaryName}) yanıt veremedi. Lütfen API anahtarlarınızı veya internet bağlantınızı kontrol edin.`
  );
  failureError.attemptsCount = 2;
  failureError.isTwoAttemptsFailed = true;
  failureError.primaryError = attempt1Err?.message || 'Bilinmeyen hata';
  failureError.secondaryError = attempt2Err?.message || 'Bilinmeyen hata';
  throw failureError;
}
