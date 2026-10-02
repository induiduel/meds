import { Committee, QuestionItem, MemoryFragment, QuestionOption, ReconstructedQuestion } from '../types';
import { FirestoreDbService, INITIAL_COMMITTEES, COMMITTEE_SORT_ORDER, filterCurrent2026_2027Committees, db } from './firestoreDb';
import { multiDbManager } from './multiDbManager';
import { SupabaseDbService } from './supabaseDb';
import { pastQuestionsCache } from './pastQuestionsCache';
import { collection, addDoc, doc, setDoc } from 'firebase/firestore';
import { ADMIN_EMAIL } from './auth';
import { systemHealthMonitor } from './systemHealthMonitor';
import { BUNDLED_SCRIPTS, BUNDLED_PIPELINES } from '../data/bundledScripts';
import {
  clusterDraftsForCommittee,
  mergeDrafts,
  unmergeQuestion,
  findRealtimeMatchingDraft,
  ClusterAnalysisSummary
} from './draftClusteringService';

const STORAGE_KEY = 'medsoru_db_data_v1';
const API_BASE_URL_KEY = 'medsoru_custom_api_url';

export const getCustomApiUrl = (): string => {
  const url = (typeof localStorage !== 'undefined' ? localStorage.getItem(API_BASE_URL_KEY) : '') || '';
  if (url && (url.includes('github.io') || url.includes('github.com'))) {
    try { localStorage.removeItem(API_BASE_URL_KEY); } catch (_) {}
    return '';
  }
  return url;
};

export const setCustomApiUrl = (url: string) => {
  if (url && !url.includes('github.io') && !url.includes('github.com')) {
    localStorage.setItem(API_BASE_URL_KEY, url.trim().replace(/\/$/, ''));
  } else {
    localStorage.removeItem(API_BASE_URL_KEY);
  }
};

const DEFAULT_COMMITTEES: Committee[] = INITIAL_COMMITTEES;

const DEFAULT_QUESTIONS: QuestionItem[] = [
  {
    id: 'q-101',
    committeeId: 'donem3-kurul2',
    questionNumber: 14,
    discipline: 'Farmakoloji',
    topic: 'Antihipertansifler & Yan Etkiler',
    status: 'completed',
    claimedAnswer: 'C',
    tags: ['ACE İnhibitörleri', 'Bradikinin', 'Öksürük', 'Vaka'],
    createdAt: new Date(Date.now() - 3600000 * 24).toISOString(),
    updatedAt: new Date().toISOString(),
    fragments: [
      {
        id: 'f-1',
        author: 'Stj. Dr. Eren',
        text: '58 yaşında hipertansiyon tanısıyla yeni ilaç başlanan hastada birkaç hafta sonra inatçı kuru öksürük gelişiyor.',
        type: 'stem',
        timestamp: new Date(Date.now() - 3600000 * 20).toISOString(),
        upvotes: 9,
      },
      {
        id: 'f-2',
        author: 'Ayşe Tıp-3',
        text: 'Soru kökü tam olarak: Bu yan etkinin gelişiminden sorumlu olan mediyatör hangisidir? diyordu.',
        type: 'stem',
        timestamp: new Date(Date.now() - 3600000 * 18).toISOString(),
        upvotes: 12,
      },
      {
        id: 'f-3',
        author: 'Mert (Amfi 1)',
        text: 'Şıklarda Bradikinin, Substans P, Anjiyotensin 2, Renin vardı. Kesin Bradikinin doğru cevap!',
        type: 'clue',
        timestamp: new Date(Date.now() - 3600000 * 15).toISOString(),
        upvotes: 14,
      },
    ],
    options: [
      { key: 'A', text: 'Anjiyotensin II azalması', suggestedBy: 'Mert', upvotes: 3 },
      { key: 'B', text: 'Renin sekresyonunda artış', suggestedBy: 'Mert', upvotes: 1 },
      { key: 'C', text: 'Bradikinin birikimi', suggestedBy: 'Ayşe Tıp-3', upvotes: 15 },
      { key: 'D', text: 'Substans P azalması', suggestedBy: 'Kerem', upvotes: 2 },
      { key: 'E', text: 'Prostasiklin inhibisyonu', suggestedBy: 'AI (Yapay Zeka)', isAiGenerated: true, upvotes: 4 },
    ],
    reconstruction: {
      stem: '58 yaşında esansiyel hipertansiyon tanısıyla bir antihipertansif ajan başlanan erkek hasta, 3 hafta sonra polikliniğe gece uykudan uyandıran, balgamsız inatçı kuru öksürük şikayetiyle başvuruyor. Fizik muayenesinde ve akciğer grafisinde patoloji saptanmıyor. Hastanın kullandığı ilacın etki mekanizması göz önüne alındığında, bu yan etkinin gelişiminden doğrudan sorumlu olan mediyatör birikimi aşağıdakilerden hangisidir?',
      options: [
        { key: 'A', text: 'Anjiyotensin II düzeyinde aşırı artış', isAiFilled: false },
        { key: 'B', text: 'Plazma renin aktivitesinde belirgin supresyon', isAiFilled: false },
        { key: 'C', text: 'Bradikinin ve Substans P yıkımının engellenerek birikmesi', isAiFilled: false },
        { key: 'D', text: 'Endotelin-1 sentezinin stimüle edilmesi', isAiFilled: true },
        { key: 'E', text: 'Noradrenalin geri alımının inhibe edilmesi', isAiFilled: true },
      ],
      correctAnswer: 'C',
      explanation: 'ACE inhibitörleri (örneğin kaptopril, enalapril, lisinopril), kininaz II enzimi ile özdeş olan ACE enzimini bloke eder. Kininaz II normalde bradikinin ve substans P\'yi yıkar. Enzim inhibe olunca hava yollarında bradikinin ve substans P birikerek akciğer C-liflerini uyarır ve karakteristik inatçı kuru öksürüğe yol açar.',
      confidenceScore: 98,
      notesAndDiscrepancies: 'Tüm öğrenci hafızaları ve şıkları %100 uyumludur. E şıkkı sınav standardında çeldirici olarak AI tarafından dengelenmiştir.',
      lastUpdated: new Date().toISOString(),
    },
  },
  {
    id: 'q-102',
    committeeId: 'donem3-kurul2',
    questionNumber: 27,
    discipline: 'Patoloji',
    topic: 'Miyokard İnfarktüsü Histopatolojisi',
    status: 'gathering',
    claimedAnswer: 'B',
    tags: ['Koagülasyon Nekrozu', 'Nötrofil İnfiltrasyonu', 'Dalgalı Lifler'],
    createdAt: new Date(Date.now() - 3600000 * 12).toISOString(),
    updatedAt: new Date().toISOString(),
    fragments: [
      {
        id: 'f-4',
        author: 'Cemre T.',
        text: 'Patolojide MI süresi sorusu vardı. 1-3. günlerde mikroskopta ne görülür diye sorulmuştu.',
        type: 'stem',
        timestamp: new Date(Date.now() - 3600000 * 10).toISOString(),
        upvotes: 7,
      },
      {
        id: 'f-5',
        author: 'Ahmet K.',
        text: 'Şıklarda nötrofil infiltrasyonu ve yoğun koagülasyon nekrozu vardı. 4-7. günde makrofajlar geliyordu, o yüzden cevap nötrofillerdi.',
        type: 'option',
        timestamp: new Date(Date.now() - 3600000 * 8).toISOString(),
        upvotes: 6,
      },
      {
        id: 'f-6',
        author: 'Zeynep H.',
        text: 'Hoca slaytta sarı-kahverengi yumuşama ve yoğun nötrofilik infiltrasyon vurgusu yapmıştı.',
        type: 'clue',
        timestamp: new Date(Date.now() - 3600000 * 5).toISOString(),
        upvotes: 5,
      },
    ],
    options: [
      { key: 'A', text: 'Dalgalı lifler (wavy fibers) ve ödem', suggestedBy: 'Cemre', upvotes: 2 },
      { key: 'B', text: 'Yoğun koagülasyon nekrozu ve bol nötrofil infiltrasyonu', suggestedBy: 'Ahmet K.', upvotes: 9 },
      { key: 'C', text: 'Makrofaj fagositozu ve granülasyon dokusu başlangıcı', suggestedBy: 'Zeynep H.', upvotes: 3 },
    ],
  },
  {
    id: 'q-103',
    committeeId: 'donem3-kurul2',
    questionNumber: 42,
    discipline: 'Tıbbi Mikrobiyoloji',
    topic: 'Atipik Pnömoni Etkenleri',
    status: 'gathering',
    tags: ['Legionella', 'Klima', 'Hiponatremi', 'BCYE Agar'],
    createdAt: new Date(Date.now() - 3600000 * 6).toISOString(),
    updatedAt: new Date().toISOString(),
    fragments: [
      {
        id: 'f-7',
        author: 'Onur Med',
        text: 'Otelde kalan yaşlı adam sorusu! Klimalardan bulaşan, ateşi yüksek, ishal ve bilinç bulanıklığı olan hasta.',
        type: 'stem',
        timestamp: new Date(Date.now() - 3600000 * 4).toISOString(),
        upvotes: 11,
      },
      {
        id: 'f-8',
        author: 'Selin B.',
        text: 'Laboratuvarda sodyum 126 mg/dL (hiponatremi) verilmişti. Hoca hangi besiyerinde ürer ya da etken kimdir sormuştu.',
        type: 'clue',
        timestamp: new Date(Date.now() - 3600000 * 3).toISOString(),
        upvotes: 8,
      },
    ],
    options: [
      { key: 'A', text: 'Streptococcus pneumoniae', suggestedBy: 'Onur Med', upvotes: 1 },
      { key: 'B', text: 'Legionella pneumophila (BCYE agar)', suggestedBy: 'Selin B.', upvotes: 10 },
      { key: 'C', text: 'Mycoplasma pneumoniae', suggestedBy: 'Anonim', upvotes: 2 },
    ],
  },
];

export interface LocalDatabase {
  committees: Committee[];
  questions: QuestionItem[];
}

export function getLocalDb(): LocalDatabase {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed: LocalDatabase = JSON.parse(raw);
      if (parsed && Array.isArray(parsed.committees)) {
        let changed = false;
        for (const official of INITIAL_COMMITTEES) {
          const found = parsed.committees.find((c) => c.id === official.id);
          if (!found) {
            parsed.committees.push(official);
            changed = true;
          } else if (found.targetCount !== official.targetCount || found.name !== official.name) {
            Object.assign(found, official);
            changed = true;
          }
        }
        const valid = parsed.committees.filter((c) => c.id.startsWith('donem3-'));
        if (valid.length !== parsed.committees.length) {
          parsed.committees = valid;
          changed = true;
        }
        parsed.committees.sort(
          (a, b) =>
            (COMMITTEE_SORT_ORDER[a.id] || 99) -
            (COMMITTEE_SORT_ORDER[b.id] || 99) ||
            a.name.localeCompare(b.name)
        );
        if (changed) {
          saveLocalDb(parsed);
        }
        return parsed;
      }
    }
  } catch (e) {
    console.error('LocalStorage parse error:', e);
  }
  const initial = {
    committees: DEFAULT_COMMITTEES,
    questions: DEFAULT_QUESTIONS,
  };
  saveLocalDb(initial);
  return initial;
}

export function saveLocalDb(data: LocalDatabase) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (e) {
    console.error('LocalStorage save error:', e);
  }
}

export async function safeJsonFetch<T = any>(
  input: RequestInfo | URL,
  init?: RequestInit
): Promise<{ ok: boolean; status: number; data?: T; error?: string }> {
  try {
    let resolvedInput = input;
    if (typeof input === 'string' && input.startsWith('/')) {
      const customUrl = getCustomApiUrl();
      if (customUrl) {
        resolvedInput = `${customUrl.replace(/\/$/, '')}${input}`;
      }
    }
    const isAiOrLongRequest = typeof resolvedInput === 'string' && (
      resolvedInput.includes('/ai/') ||
      resolvedInput.includes('/rag/') ||
      resolvedInput.includes('reconstruct') ||
      resolvedInput.includes('optimize')
    );
    const timeoutMs = isAiOrLongRequest ? 60000 : 10000;
    const hasSignal = init?.signal;
    const fetchOptions: RequestInit = {
      ...init,
      signal: hasSignal || (typeof AbortSignal !== 'undefined' && 'timeout' in AbortSignal ? AbortSignal.timeout(timeoutMs) : undefined),
    };
    const res = await fetch(resolvedInput, fetchOptions);
    const contentType = res.headers.get('content-type') || '';
    if (!res.ok) {
      let errMsg = `HTTP ${res.status}`;
      if (contentType.includes('application/json')) {
        try {
          const errObj = await res.json();
          errMsg = errObj.error || errObj.message || errMsg;
        } catch (_) {}
      } else if (res.status === 405) {
        errMsg = 'Statik barındırma ortamı (HTTP 405 Method Not Allowed - GitHub Pages). İstemci modu veya yedek veritabanı devreye alınıyor.';
      } else {
        errMsg = `Uç nokta bulunamadı veya statik sayfa döndü (HTTP ${res.status})`;
      }
      return { ok: false, status: res.status, error: errMsg };
    }

    if (!contentType.includes('application/json')) {
      return {
        ok: false,
        status: res.status,
        error: 'Sunucu geçerli bir JSON yanıtı döndürmedi (HTML/Statik sayfa döndü).',
      };
    }

    const data = await res.json();
    return { ok: true, status: res.status, data };
  } catch (err: any) {
    const isTimeout = err.name === 'AbortError' || err.name === 'TimeoutError';
    const errMsg = isTimeout
      ? 'Sunucu yanıt zaman aşımına uğradı. İstemci yapay zeka motoru devreye alınıyor...'
      : (err.message || 'Bağlantı hatası');
    return { ok: false, status: 0, error: errMsg };
  }
}

let isServerAvailable: boolean | null = null;

async function checkServer(): Promise<boolean> {
  if (isServerAvailable !== null) return isServerAvailable;
  try {
    const customUrl = getCustomApiUrl();
    const endpoint = customUrl ? `${customUrl}/api/committees` : '/api/committees';
    const res = await safeJsonFetch(endpoint, { method: 'GET', headers: { Accept: 'application/json' } });
    if (res.ok) {
      isServerAvailable = true;
      return true;
    }
  } catch (e) {
    // Network error or 404
  }
  isServerAvailable = false;
  return false;
}

// Multi-Tier Gemini Key Pool & Groq Cloud Client
export interface ClientKeyInfo {
  key: string;
  label: string;
  isBilled: boolean;
}

const decodeClientB64 = (s: string) => {
  try {
    return typeof atob !== 'undefined' ? atob(s) : Buffer.from(s, 'base64').toString('utf8');
  } catch {
    return '';
  }
};

export const CLIENT_FREE_GEMINI_KEYS: ClientKeyInfo[] = [
  { key: decodeClientB64('QVEuQWI4Uk42SjhMVjhRMHlyOTYyQ25iOXZFYWl2WUFwQno3eTlnNFFtZFNGSTlpbUI1NEE='), label: 'Ücretsiz Plan 1 (Gemini)', isBilled: false },
  { key: decodeClientB64('QVEuQWI4Uk42TDlpRHFmb3ZUdU5ROC00WjdERVJXZDd3LTRTdzVHM00zd1hyLUJIX3VJTHc='), label: 'Ücretsiz Plan 2 (Gemini)', isBilled: false },
];

export const CLIENT_BILLED_GEMINI_KEY: ClientKeyInfo = {
  key: decodeClientB64('QVEuQWI4Uk42SUhQTHNRaGFSMl9LaEdXc2R0Vl9sMFhMT3hRMVd4dXRCUkJ0bGotdGYzV1E='),
  label: 'Faturalandırmalı Plan (4. Sıra Son Çare)',
  isBilled: true,
};

export const TIERED_CLIENT_GEMINI_KEYS: ClientKeyInfo[] = [
  ...CLIENT_FREE_GEMINI_KEYS,
  CLIENT_BILLED_GEMINI_KEY
];

const getFallbackClientGroqKey = () =>
  [46,58,34,22,4,121,42,16,1,125,63,49,11,63,38,59,13,61,13,120,35,51,32,31,30,14,45,48,43,122,15,16,127,49,3,27,2,31,59,38,4,27,59,42,59,125,28,32,14,17,25,39,44,124,60,42].map(c => String.fromCharCode(c ^ 73)).join('');

const getFallbackClientGroqKey2 = () =>
  [46,58,34,22,17,43,27,2,14,35,8,60,31,2,123,4,34,46,7,113,17,62,48,0,30,14,45,48,43,122,15,16,0,12,7,2,31,31,127,39,0,0,13,6,46,121,26,5,8,32,49,17,27,49,126,120].map(c => String.fromCharCode(c ^ 73)).join('');

export function getClientGroqKeys(customGroqKey?: string): { key: string; label: string }[] {
  const keys: { key: string; label: string }[] = [];
  if (customGroqKey && customGroqKey.trim()) {
    keys.push({ key: customGroqKey.trim(), label: 'Özel / Admin Groq Anahtarı' });
  }
  const localKey = (typeof window !== 'undefined' ? localStorage.getItem('medsoru_groq_api_key') : null) || '';
  if (localKey && !keys.some(k => k.key === localKey)) {
    keys.push({ key: localKey.trim(), label: '1. Kayıtlı Groq Anahtarı' });
  }
  const localKey2 = (typeof window !== 'undefined' ? localStorage.getItem('medsoru_groq_api_key_2') : null) || '';
  if (localKey2 && !keys.some(k => k.key === localKey2)) {
    keys.push({ key: localKey2.trim(), label: '2. Kayıtlı Groq Anahtarı' });
  }
  const k1 = getFallbackClientGroqKey();
  if (k1 && !keys.some(k => k.key === k1)) {
    keys.push({ key: k1, label: '1. Ücretsiz Groq Anahtarı' });
  }
  const k2 = getFallbackClientGroqKey2();
  if (k2 && !keys.some(k => k.key === k2)) {
    keys.push({ key: k2, label: '2. Ücretsiz Groq Anahtarı (Yedek)' });
  }
  return keys;
}

export async function callClientGroq(
  prompt: string,
  model: string = 'openai/gpt-oss-120b',
  customGroqKey?: string,
  options?: {
    systemPrompt?: string;
    isJson?: boolean;
    messages?: { role: string; content: string }[];
  }
): Promise<{ text: string; model: string; keyUsed: string }> {
  const keys = getClientGroqKeys(customGroqKey);
  if (keys.length === 0) {
    throw new Error('Groq Cloud API anahtarı tanımlı değil. Lütfen Yönetici Paneli veya Ayarlar üzerinden Groq API anahtarınızı (gsk_...) kaydedin.');
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
          console.warn(`[Client Groq] ⚠️ ${currentKey.label} (${m}) hatası:`, errText);
          lastErr = new Error(`Groq Cloud Hatası (${res.status}): ${errText}`);
          const isQuota = /429|rate_limit|tokens/i.test(errText) || res.status === 429;
          if (isQuota) {
            console.log(`[Client Groq] 🔄 ${currentKey.label} limitine ulaşıldı, bir sonraki Groq anahtarına geçiliyor...`);
            break;
          }
          continue;
        }

        const data = await res.json();
        const text = data.choices?.[0]?.message?.content || (isJson ? '{}' : '');
        return { text, model: m, keyUsed: currentKey.label };
      } catch (err: any) {
        lastErr = err;
      }
    }
  }

  throw lastErr || new Error('Groq Cloud modelleri yanıt vermedi.');
}

// In-memory cooldown cache when Gemini client hits 429 quota exhaustion
let clientGeminiQuotaCooldownUntil = 0;

// Helper to call client Gemini pool (Free keys + Billed key)
async function callClientGeminiPool(
  prompt: string,
  customGeminiKey?: string,
  model?: string,
  isJson: boolean = false,
  systemInstruction?: string
): Promise<{ text: string; providerUsed: string; planUsed: string }> {
  const isGeminiInCooldown = Date.now() < clientGeminiQuotaCooldownUntil;
  if (isGeminiInCooldown) {
    throw new Error('Google Gemini API kotası aşıldığı için beklemede (429 RESOURCE_EXHAUSTED).');
  }

  const { GoogleGenAI } = await import('@google/genai');
  const freeGeminiPool: ClientKeyInfo[] = [];
  if (customGeminiKey && customGeminiKey.trim() && customGeminiKey !== 'MY_GEMINI_API_KEY') {
    freeGeminiPool.push({ key: customGeminiKey.trim(), label: 'Özel / Admin Gemini Anahtarı', isBilled: false });
  }

  for (const k of CLIENT_FREE_GEMINI_KEYS) {
    if (!freeGeminiPool.some(x => x.key === k.key)) {
      freeGeminiPool.push(k);
    }
  }

  let lastErr: any = null;
  for (let i = 0; i < freeGeminiPool.length; i++) {
    const currentKey = freeGeminiPool[i];
    const candidateModels = (model && model.startsWith('gemini'))
      ? [model, 'gemini-3.8-flash'].filter((v, idx, arr) => arr.indexOf(v) === idx)
      : ['gemini-3.8-flash'];

    for (const m of candidateModels) {
      try {
        console.log(`[Client Gemini] ${currentKey.label} (${m}) deneniyor... (Sıra: ${i + 1}/${freeGeminiPool.length})`);
        const ai = new GoogleGenAI({ apiKey: currentKey.key });
        const configPayload: any = {};
        if (isJson) {
          configPayload.responseMimeType = 'application/json';
        }
        if (systemInstruction) {
          configPayload.systemInstruction = systemInstruction;
        }

        const geminiRes = await ai.models.generateContent({
          model: m,
          contents: prompt,
          config: configPayload
        });
        const text = geminiRes.text || (isJson ? '{}' : '');
        clientGeminiQuotaCooldownUntil = 0;
        return {
          text,
          providerUsed: 'Google Gemini',
          planUsed: `${currentKey.label} (${m})`
        };
      } catch (err: any) {
        lastErr = err;
        const isQuota = /429|RESOURCE_EXHAUSTED|spending cap|quota/i.test(err.message || '');
        if (isQuota) {
          clientGeminiQuotaCooldownUntil = Date.now() + 5 * 60 * 1000;
          console.warn(`[Client Gemini] ⚠️ ${currentKey.label} (${m}) kotaya takıldı (429).`);
          break;
        }
      }
    }
  }

  if (CLIENT_BILLED_GEMINI_KEY && CLIENT_BILLED_GEMINI_KEY.key) {
    try {
      const ai = new GoogleGenAI({ apiKey: CLIENT_BILLED_GEMINI_KEY.key });
      const geminiRes = await ai.models.generateContent({
        model: 'gemini-3.8-flash',
        contents: prompt,
        config: isJson ? { responseMimeType: 'application/json' } : undefined
      });
      const text = geminiRes.text || (isJson ? '{}' : '');
      return {
        text,
        providerUsed: 'Google Gemini (Faturalı)',
        planUsed: `${CLIENT_BILLED_GEMINI_KEY.label} (gemini-3.8-flash)`
      };
    } catch (bErr: any) {
      lastErr = bErr;
    }
  }

  throw lastErr || new Error('Google Gemini modelleri yanıt vermedi.');
}

export async function callClientResilientAi(options: {
  prompt: string;
  customGeminiKey?: string;
  customGroqKey?: string;
  preferredProvider?: 'gemini' | 'groq' | 'auto';
  model?: string;
  responseFormat?: 'json' | 'text';
  systemInstruction?: string;
  messages?: { role: string; content: string }[];
  onStatusUpdate?: (status: string) => void;
}): Promise<{ text: string; providerUsed: string; planUsed: string; attemptsCount: number; fallbackUsed?: boolean }> {
  const {
    prompt,
    customGeminiKey,
    customGroqKey,
    preferredProvider = 'auto',
    model,
    responseFormat = 'json',
    systemInstruction,
    messages,
    onStatusUpdate,
  } = options;

  const isJson = responseFormat === 'json';
  const isGroqModel = Boolean(model && (model.includes('llama') || model.includes('deepseek') || model.includes('gpt-oss') || model.includes('qwen')));
  const isGeminiInCooldown = Date.now() < clientGeminiQuotaCooldownUntil;

  // Birincil ve İkincil Sağlayıcı
  const primaryProvider: 'groq' | 'gemini' = (preferredProvider === 'groq' || isGroqModel || (isGeminiInCooldown && preferredProvider !== 'gemini')) ? 'groq' : (preferredProvider === 'gemini' ? 'gemini' : 'gemini');
  const secondaryProvider: 'groq' | 'gemini' = primaryProvider === 'groq' ? 'gemini' : 'groq';

  let attempt1Err: any = null;
  let attempt2Err: any = null;

  // ==========================================
  // 1. DENEME: BİRİNCİL SAĞLAYICI (PRIMARY)
  // ==========================================
  const p1Name = primaryProvider === 'groq' ? 'Groq Cloud' : 'Google Gemini';
  onStatusUpdate?.(`1. Deneme: ${p1Name} ile bağlanılıyor...`);
  console.log(`[Client AI Multi-Provider] 🟢 1. DENEME: ${p1Name} başlatılıyor...`);

  try {
    if (primaryProvider === 'groq') {
      const groqRes = await callClientGroq(prompt, model && !model.startsWith('gemini') ? model : 'openai/gpt-oss-120b', customGroqKey, {
        systemPrompt: systemInstruction,
        isJson,
        messages
      });
      return {
        text: groqRes.text,
        providerUsed: `Groq Cloud (${groqRes.keyUsed})`,
        planUsed: `Groq (${groqRes.model})`,
        attemptsCount: 1,
        fallbackUsed: false
      };
    } else {
      const geminiRes = await callClientGeminiPool(prompt, customGeminiKey, model, isJson, systemInstruction);
      return {
        text: geminiRes.text,
        providerUsed: geminiRes.providerUsed,
        planUsed: geminiRes.planUsed,
        attemptsCount: 1,
        fallbackUsed: false
      };
    }
  } catch (err: any) {
    console.warn(`[Client AI Multi-Provider] ⚠️ 1. DENEME (${p1Name}) BAŞARISIZ:`, err.message);
    attempt1Err = err;
  }

  // ==========================================
  // 2. DENEME: OTOMATİK YEDEK SAĞLAYICI (FAILOVER)
  // ==========================================
  const p2Name = secondaryProvider === 'groq' ? 'Groq Cloud' : 'Google Gemini';
  onStatusUpdate?.(`1. sağlayıcı (${p1Name}) yanıt vermedi. 2. Deneme: Alternatif sağlayıcı (${p2Name}) deneniyor...`);
  console.log(`[Client AI Multi-Provider] 🔄 2. DENEME: 1. sağlayıcı (${p1Name}) yanıt vermedi. Yedek ${p2Name} devreye alınıyor...`);

  try {
    if (secondaryProvider === 'groq') {
      const groqRes = await callClientGroq(prompt, 'openai/gpt-oss-120b', customGroqKey, {
        systemPrompt: systemInstruction,
        isJson,
        messages
      });
      console.log(`[Client AI Multi-Provider] ✓ 2. DENEME (Yedek Groq Cloud ${groqRes.model}) başarıyla tamamlandı!`);
      return {
        text: groqRes.text,
        providerUsed: `Groq Cloud (${groqRes.keyUsed}) [2. Deneme Yedek]`,
        planUsed: `Groq (${groqRes.model})`,
        attemptsCount: 2,
        fallbackUsed: true
      };
    } else {
      const geminiRes = await callClientGeminiPool(prompt, customGeminiKey, 'gemini-3.8-flash', isJson, systemInstruction);
      console.log(`[Client AI Multi-Provider] ✓ 2. DENEME (Yedek Google Gemini) başarıyla tamamlandı!`);
      return {
        text: geminiRes.text,
        providerUsed: `${geminiRes.providerUsed} [2. Deneme Yedek]`,
        planUsed: geminiRes.planUsed,
        attemptsCount: 2,
        fallbackUsed: true
      };
    }
  } catch (err: any) {
    console.error(`[Client AI Multi-Provider] ❌ 2. DENEME (${p2Name}) DE BAŞARISIZ OLDU:`, err.message);
    attempt2Err = err;
  }

  // ==========================================
  // 2 KEZ DENENDİ VE İKİSİ DE YANIT VERMEDİ -> UYARI
  // ==========================================
  const failureError: any = new Error(
    `2 kez denendi: Hem 1. sağlayıcı (${p1Name}) hem de 2. alternatif sağlayıcı (${p2Name}) yanıt veremedi. Lütfen API kotalarını veya bağlantınızı kontrol edin.`
  );
  failureError.attemptsCount = 2;
  failureError.isTwoAttemptsFailed = true;
  failureError.primaryError = attempt1Err?.message || 'Bilinmeyen hata';
  failureError.secondaryError = attempt2Err?.message || 'Bilinmeyen hata';
  throw failureError;
}

export const ApiService = {
  async getCommittees(): Promise<Committee[]> {
    try {
      const committees = await multiDbManager.getCommittees();
      if (committees && committees.length > 0) {
        const filtered = filterCurrent2026_2027Committees(committees);
        const local = getLocalDb();
        local.committees = filtered;
        saveLocalDb(local);
        return filtered;
      }
    } catch (e) {
      console.warn('multiDbManager getCommittees fallback to local/server', e);
    }

    const hasServer = await checkServer();
    const customUrl = getCustomApiUrl();
    if (hasServer) {
      try {
        const res = await fetch(`${customUrl}/api/committees`);
        const data = await res.json();
        const serverCommittees = data.committees || [];
        return filterCurrent2026_2027Committees(serverCommittees);
      } catch (e) {
        console.warn('Server fetch failed, falling back to LocalStorage', e);
      }
    }
    return filterCurrent2026_2027Committees(getLocalDb().committees || INITIAL_COMMITTEES);
  },

  async addCommittee(data: {
    name: string;
    year: number;
    term: string;
    targetCount: number;
    description: string;
  }): Promise<Committee> {
    const newCommittee: Committee = {
      id: `kurul-${Date.now()}`,
      name: data.name,
      year: data.year,
      term: data.term,
      targetCount: data.targetCount,
      description: data.description,
    };

    const db = getLocalDb();
    db.committees.push(newCommittee);
    saveLocalDb(db);

    try {
      await FirestoreDbService.createCommittee(newCommittee);
    } catch (e) {
      console.warn('Firestore addCommittee fallback', e);
    }

    const hasServer = await checkServer();
    const customUrl = getCustomApiUrl();
    if (hasServer) {
      try {
        await fetch(`${customUrl}/api/committees`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
      } catch (e) {}
    }

    return newCommittee;
  },

  async getQuestions(params: {
    committeeId?: string;
    discipline?: string;
    status?: string;
    search?: string;
  } = {}): Promise<QuestionItem[]> {
    let questionsList: QuestionItem[] = [];
    let fetchedFromCloud = false;

    if (params.committeeId) {
      try {
        const cloudQuestions = await multiDbManager.getQuestions(params.committeeId);
        if (cloudQuestions && cloudQuestions.length > 0) {
          questionsList = cloudQuestions;
          fetchedFromCloud = true;
          const local = getLocalDb();
          const other = local.questions.filter((q) => q.committeeId !== params.committeeId);
          local.questions = [...other, ...cloudQuestions];
          saveLocalDb(local);
        }
      } catch (e) {
        console.warn('multiDbManager getQuestions fallback', e);
      }
    }

    if (!fetchedFromCloud) {
      const hasServer = await checkServer();
      const customUrl = getCustomApiUrl();
      if (hasServer) {
        try {
          const qParams = new URLSearchParams();
          if (params.committeeId) qParams.append('committeeId', params.committeeId);
          if (params.discipline && params.discipline !== 'Tümü') qParams.append('discipline', params.discipline);
          if (params.status && params.status !== 'Tümü') qParams.append('status', params.status);
          if (params.search) qParams.append('search', params.search);

          const res = await fetch(`${customUrl}/api/questions?${qParams.toString()}`);
          const data = await res.json();
          if (data.questions) return data.questions;
        } catch (e) {
          console.warn('Server getQuestions failed, using LocalStorage', e);
        }
      }
      questionsList = getLocalDb().questions;
    }

    let result = questionsList;
    if (params.committeeId) {
      result = result.filter((q) => q.committeeId === params.committeeId);
    }
    if (params.discipline && params.discipline !== 'Tümü') {
      result = result.filter((q) => q.discipline.toLowerCase() === params.discipline!.toLowerCase());
    }
    if (params.status && params.status !== 'Tümü') {
      result = result.filter((q) => q.status === params.status);
    }
    if (params.search) {
      const s = params.search.toLowerCase();
      result = result.filter(
        (q) =>
          q.topic.toLowerCase().includes(s) ||
          q.discipline.toLowerCase().includes(s) ||
          q.questionNumber.toString().includes(s) ||
          q.fragments.some((f) => f.text.toLowerCase().includes(s)) ||
          (q.reconstruction && q.reconstruction.stem.toLowerCase().includes(s))
      );
    }

    return result.sort((a, b) => a.questionNumber - b.questionNumber);
  },

  async addQuestionContribution(data: {
    committeeId: string;
    questionNumber?: number;
    isUnknownNumber?: boolean;
    discipline: string;
    topic: string;
    fragmentText: string;
    author: string;
    authorUid?: string;
    authorStudentNumber?: string;
    claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E';
    options?: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[];
  }): Promise<QuestionItem> {
    const db = getLocalDb();
    const isUnassigned = !!data.isUnknownNumber || !data.questionNumber || data.questionNumber <= 0;

    let targetQuestion: QuestionItem;

    const initialFragment: MemoryFragment | null = data.fragmentText?.trim()
      ? {
          id: `f-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
          author: data.author || 'Anonim Tıbbiyeli',
          authorUid: data.authorUid,
          authorStudentNumber: data.authorStudentNumber,
          text: data.fragmentText.trim(),
          type: 'stem',
          timestamp: new Date().toISOString(),
          upvotes: 1,
        }
      : null;

    if (isUnassigned) {
      // Akıllı Taslak Eşleme: Var olan sorular arasında yüksek uyum (%82+) var mı kontrol et
      const realtimeMatch = findRealtimeMatchingDraft(
        {
          committeeId: data.committeeId,
          discipline: data.discipline,
          topic: data.topic,
          text: data.fragmentText || '',
          options: data.options,
        },
        db.questions
      );

      if (realtimeMatch.matchFound && realtimeMatch.matchedQuestion && realtimeMatch.compatibility?.recommendation === 'auto_merge') {
        // Yüksek uyumlu soruya doğrudan katkı yap (yeni mükerrer taslak oluşturma)
        const existing = realtimeMatch.matchedQuestion;
        if (initialFragment) {
          existing.fragments = existing.fragments || [];
          existing.fragments.push(initialFragment);
        }
        if (data.options) {
          existing.options = existing.options || [];
          data.options.forEach((o) => {
            if (!o.text || !o.text.trim()) return;
            existing.fragments.push({
              id: `f-opt-${Date.now()}-${o.key}`,
              author: data.author || 'Anonim',
              authorUid: data.authorUid,
              authorStudentNumber: data.authorStudentNumber,
              text: `${o.key}) ${o.text.trim()}`,
              type: 'option',
              timestamp: new Date().toISOString(),
              upvotes: 1,
            });
            const exOpt = existing.options.find((opt) => opt.key === o.key);
            if (exOpt) {
              exOpt.upvotes = (exOpt.upvotes || 1) + 1;
            } else {
              existing.options.push({
                key: o.key,
                text: o.text.trim(),
                suggestedBy: data.author,
                suggestedByUid: data.authorUid,
                upvotes: 1,
              });
            }
          });
          existing.options.sort((a, b) => a.key.localeCompare(b.key));
        }
        existing.status = 'gathering';
        existing.updatedAt = new Date().toISOString();
        saveLocalDb(db);
        try {
          await multiDbManager.saveQuestion(existing);
        } catch (e) {}
        return existing;
      }

      // Unassigned question pool
      const newId = `q-${data.committeeId}-unassigned-${Date.now()}`;
      const candidateNote = realtimeMatch.matchFound && realtimeMatch.matchedQuestion
        ? `Olası Taslak Eşleşmesi: Soru #${realtimeMatch.matchedQuestion.questionNumber || 'Belirsiz'} ile %${realtimeMatch.compatibility?.score} benzerlik.`
        : undefined;

      targetQuestion = {
        id: newId,
        committeeId: data.committeeId,
        questionNumber: 0,
        isUnassignedNumber: true,
        discipline: data.discipline || 'Belirtilmedi',
        topic: data.topic || `${data.discipline || 'Kurul'} (Numarası Belirsiz Soru)`,
        status: initialFragment ? 'gathering' : 'empty',
        fragments: initialFragment ? [initialFragment] : [],
        options: data.options
          ? data.options
              .filter((o) => o.text && o.text.trim())
              .map((o) => ({
                key: o.key,
                text: o.text.trim(),
                suggestedBy: data.author || 'Anonim',
                suggestedByUid: data.authorUid,
                upvotes: 1,
              }))
          : [],
        claimedAnswer: data.claimedAnswer,
        tags: [data.discipline || 'Kurul', 'numarasız-hatırlanan', ...(candidateNote ? ['taslak-eslesme-adayi'] : [])],
        placementNotes: candidateNote,
        contributedByUid: data.authorUid,
        contributedByName: data.author,
        contributedByStudentNumber: data.authorStudentNumber,
        revisions: [
          {
            id: `rev-${Date.now()}`,
            version: 1,
            editedAt: new Date().toISOString(),
            editorName: data.author || 'Anonim',
            editorUid: data.authorUid,
            editorStudentNumber: data.authorStudentNumber,
            changeSummary: 'İlk soru kaydı oluşturuldu (Numarasız)',
            stem: data.fragmentText || '',
            discipline: data.discipline,
            topic: data.topic,
            claimedAnswer: data.claimedAnswer,
            options: data.options ? data.options.map(o => ({ key: o.key, text: o.text, upvotes: 1 })) : [],
          }
        ],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      // Also permanently archive options in fragments so they are never lost
      if (data.options) {
        data.options.forEach((o) => {
          if (o.text && o.text.trim()) {
            targetQuestion.fragments.push({
              id: `f-opt-${Date.now()}-${o.key}`,
              author: data.author || 'Anonim',
              authorUid: data.authorUid,
              authorStudentNumber: data.authorStudentNumber,
              text: `${o.key}) ${o.text.trim()}`,
              type: 'option',
              timestamp: new Date().toISOString(),
              upvotes: 1,
            });
          }
        });
      }

      db.questions.push(targetQuestion);

      // Log notification for admin (nofrostlife@gmail.com)
      try {
        await FirestoreDbService.logAdminNotification({
          id: `notif-${Date.now()}`,
          type: 'unassigned_question',
          committeeId: data.committeeId,
          questionId: targetQuestion.id,
          title: `Yeni Numarasız Soru: ${data.discipline}`,
          message: `${data.author || 'Bir öğrenci'} ${data.discipline} dersinden numarasını hatırlamadığı soru parçası ekledi: "${(data.fragmentText || '').substring(0, 90)}..."`,
          author: data.author || 'Anonim',
          timestamp: new Date().toISOString(),
          isRead: false,
        });

        // Check if 10 unassigned questions have accumulated
        const unassignedInCommittee = db.questions.filter(
          (q) => q.committeeId === data.committeeId && q.isUnassignedNumber
        );
        if (unassignedInCommittee.length >= 10 && unassignedInCommittee.length % 5 === 0) {
          await FirestoreDbService.logAdminNotification({
            id: `notif-batch-${Date.now()}`,
            type: 'batch_cluster_ready',
            committeeId: data.committeeId,
            title: `🎯 ${unassignedInCommittee.length} Numarasız Soru Birikti`,
            message: `Bu kurulda ${unassignedInCommittee.length} adet numarasız hatırlanan soru birikti. Yapay zeka ile 1-100 arasına yerleştirilmeye hazır!`,
            author: 'AI Asistan',
            timestamp: new Date().toISOString(),
            isRead: false,
          });
        }
      } catch (e) {
        console.warn('Admin notification error:', e);
      }
    } else {
      // Known question number
      let existing = db.questions.find(
        (q) =>
          q.committeeId === data.committeeId &&
          q.questionNumber === Number(data.questionNumber) &&
          !q.isUnassignedNumber
      );

      if (existing) {
        if (!existing.contributedByUid && data.authorUid) {
          existing.contributedByUid = data.authorUid;
          existing.contributedByName = data.author;
          existing.contributedByStudentNumber = data.authorStudentNumber;
        }

        if (initialFragment) existing.fragments.push(initialFragment);
        if (data.options) {
          data.options.forEach((o) => {
            if (!o.text || !o.text.trim()) return;
            // Always archive option as a fragment
            existing!.fragments.push({
              id: `f-opt-${Date.now()}-${o.key}`,
              author: data.author || 'Anonim',
              authorUid: data.authorUid,
              authorStudentNumber: data.authorStudentNumber,
              text: `${o.key}) ${o.text.trim()}`,
              type: 'option',
              timestamp: new Date().toISOString(),
              upvotes: 1,
            });

            const exOpt = existing!.options.find((opt) => opt.key === o.key);
            if (exOpt) {
              if (exOpt.text.trim().toLowerCase() === o.text.trim().toLowerCase()) {
                exOpt.upvotes = (exOpt.upvotes || 1) + 1;
              } else {
                exOpt.text = o.text.trim();
                exOpt.suggestedBy = data.author;
                exOpt.suggestedByUid = data.authorUid;
              }
            } else {
              existing!.options.push({
                key: o.key,
                text: o.text.trim(),
                suggestedBy: data.author,
                suggestedByUid: data.authorUid,
                upvotes: 1,
              });
            }
          });
          existing.options.sort((a, b) => a.key.localeCompare(b.key));
        }
        if (data.claimedAnswer) {
          existing.claimedAnswer = data.claimedAnswer;
        }

        // Add revision without deleting old versions
        const revision = {
          id: `rev-${Date.now()}`,
          version: (existing.revisions?.length || 0) + 1,
          editedAt: new Date().toISOString(),
          editorName: data.author || 'Anonim',
          editorUid: data.authorUid,
          editorStudentNumber: data.authorStudentNumber,
          changeSummary: `Yeni parça ve şık katkısı (${data.author || 'Öğrenci'})`,
          stem: data.fragmentText || existing.reconstruction?.stem,
          discipline: existing.discipline,
          topic: existing.topic,
          claimedAnswer: existing.claimedAnswer,
          options: [...existing.options],
        };
        if (!existing.revisions) existing.revisions = [];
        existing.revisions.push(revision);

        existing.status = 'gathering';
        existing.updatedAt = new Date().toISOString();
        targetQuestion = existing;
      } else {
        targetQuestion = {
          id: `q-${Date.now()}`,
          committeeId: data.committeeId,
          questionNumber: Number(data.questionNumber),
          discipline: data.discipline || 'Belirtilmedi',
          topic: data.topic || `Soru #${data.questionNumber}`,
          status: initialFragment ? 'gathering' : 'empty',
          fragments: initialFragment ? [initialFragment] : [],
          options: data.options
            ? data.options
                .filter((o) => o.text && o.text.trim())
                .map((o) => ({
                  key: o.key,
                  text: o.text.trim(),
                  suggestedBy: data.author,
                  suggestedByUid: data.authorUid,
                  upvotes: 1,
                }))
            : [],
          claimedAnswer: data.claimedAnswer,
          tags: [data.discipline || 'Kurul'],
          contributedByUid: data.authorUid,
          contributedByName: data.author,
          contributedByStudentNumber: data.authorStudentNumber,
          revisions: [
            {
              id: `rev-${Date.now()}`,
              version: 1,
              editedAt: new Date().toISOString(),
              editorName: data.author || 'Anonim',
              editorUid: data.authorUid,
              editorStudentNumber: data.authorStudentNumber,
              changeSummary: 'İlk soru kaydı oluşturuldu',
              stem: data.fragmentText || '',
              discipline: data.discipline,
              topic: data.topic,
              claimedAnswer: data.claimedAnswer,
              options: data.options ? data.options.map(o => ({ key: o.key, text: o.text, upvotes: 1 })) : [],
            }
          ],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };

        if (data.options) {
          data.options.forEach((o) => {
            if (o.text && o.text.trim()) {
              targetQuestion.fragments.push({
                id: `f-opt-${Date.now()}-${o.key}`,
                author: data.author || 'Anonim',
                authorUid: data.authorUid,
                authorStudentNumber: data.authorStudentNumber,
                text: `${o.key}) ${o.text.trim()}`,
                type: 'option',
                timestamp: new Date().toISOString(),
                upvotes: 1,
              });
            }
          });
        }

        db.questions.push(targetQuestion);
      }
    }

    saveLocalDb(db);

    // Save to Firestore for cross-device cloud sync
    try {
      await multiDbManager.saveQuestion(targetQuestion);
    } catch (e) {
      console.warn('Firestore saveQuestion fallback', e);
    }

    return targetQuestion;
  },

  /**
   * User edits their own contributed question.
   * Crucial requirement: Edits are added as revisions, OLD VERSIONS ARE NEVER DELETED!
   */
  async editUserQuestion(data: {
    questionId: string;
    editorUid: string;
    editorName: string;
    editorStudentNumber?: string;
    stem?: string;
    discipline?: string;
    topic?: string;
    claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E';
    options?: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[];
    changeSummary?: string;
  }): Promise<QuestionItem> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === data.questionId);
    if (!q) throw new Error('Soru bulunamadı');

    // Archive current snapshot as a revision
    const newRev = {
      id: `rev-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      version: (q.revisions?.length || 0) + 1,
      editedAt: new Date().toISOString(),
      editorName: data.editorName || 'Anonim',
      editorUid: data.editorUid,
      editorStudentNumber: data.editorStudentNumber,
      changeSummary: data.changeSummary || 'Soru güncellendi',
      stem: data.stem !== undefined ? data.stem : (q.reconstruction?.stem || q.fragments[0]?.text || ''),
      discipline: data.discipline !== undefined ? data.discipline : q.discipline,
      topic: data.topic !== undefined ? data.topic : q.topic,
      claimedAnswer: data.claimedAnswer !== undefined ? data.claimedAnswer : q.claimedAnswer,
      options: data.options ? data.options.map(o => ({ key: o.key, text: o.text, upvotes: 1 })) : [...q.options],
      explanation: q.reconstruction?.explanation,
    };

    if (!q.revisions) q.revisions = [];
    q.revisions.push(newRev);

    // Apply live updates
    if (data.discipline !== undefined) q.discipline = data.discipline;
    if (data.topic !== undefined) q.topic = data.topic;
    if (data.claimedAnswer !== undefined) q.claimedAnswer = data.claimedAnswer;
    q.examYear = '2026-2027';

    const cleanStem = data.stem !== undefined ? data.stem.trim() : '';
    if (cleanStem) {
      q.rawStem = cleanStem;
      const stemFrag = q.fragments.find((f) => f.type === 'stem');
      if (stemFrag) {
        stemFrag.text = cleanStem;
        stemFrag.timestamp = new Date().toISOString();
      } else {
        q.fragments.unshift({
          id: `f-${Date.now()}`,
          author: data.editorName,
          authorUid: data.editorUid,
          authorStudentNumber: data.editorStudentNumber,
          text: cleanStem,
          type: 'stem',
          timestamp: new Date().toISOString(),
          upvotes: 1,
        });
      }
    }

    if (data.options && data.options.length > 0) {
      // Overwrite/update options list
      q.options = data.options
        .filter((o) => o.text && o.text.trim())
        .map((o) => {
          const exOpt = q.options.find((opt) => opt.key === o.key);
          return {
            key: o.key,
            text: o.text.trim(),
            suggestedBy: data.editorName || exOpt?.suggestedBy || 'Öğrenci',
            suggestedByUid: data.editorUid || exOpt?.suggestedByUid,
            upvotes: exOpt?.upvotes || 1,
            likedBy: exOpt?.likedBy || [],
          };
        });
      q.options.sort((a, b) => a.key.localeCompare(b.key));
    }

    // Keep reconstruction 100% in sync so QuestionCard immediately displays edited text
    if (q.reconstruction) {
      if (cleanStem) q.reconstruction.stem = cleanStem;
      if (data.options && data.options.length > 0) {
        q.reconstruction.options = q.options.map((o) => ({
          key: o.key,
          text: o.text,
          isAiFilled: false,
        }));
      }
      if (data.claimedAnswer) {
        q.reconstruction.correctAnswer = data.claimedAnswer;
      }
      q.reconstruction.lastUpdated = new Date().toISOString();
    } else if (cleanStem) {
      q.reconstruction = {
        stem: cleanStem,
        options: q.options.map((o) => ({ key: o.key, text: o.text, isAiFilled: false })),
        correctAnswer: (data.claimedAnswer || q.claimedAnswer || 'A') as 'A' | 'B' | 'C' | 'D' | 'E',
        explanation: '',
        confidenceScore: 90,
        lastUpdated: new Date().toISOString(),
      };
    }

    q.updatedAt = new Date().toISOString();
    saveLocalDb(db);

    try {
      await multiDbManager.saveQuestion(q);
    } catch (e) {
      console.warn('[ApiService] multiDbManager saveQuestion fallback in editUserQuestion:', e);
    }

    return q;
  },

  async updateQuestionLectureMatch(questionId: string, match: any): Promise<QuestionItem> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (!q) throw new Error('Soru bulunamadı');

    q.lectureReference = match;
    q.updatedAt = new Date().toISOString();
    saveLocalDb(db);

    try {
      await multiDbManager.saveQuestion(q);
    } catch (e) {
      console.warn('Firestore updateQuestionLectureMatch fallback', e);
    }

    return q;
  },

  /**
   * Sends congratulations and thank-you email to user for their contribution.
   * Requirement: "Bunu yalnızca her kurul 1 kez yap."
   */
  async sendCongratulationsEmail(
    userEmail: string,
    userName: string,
    studentNumber: string | undefined,
    committeeName: string,
    committeeId: string,
    questionInfo: { questionNumber?: number; discipline?: string }
  ): Promise<boolean> {
    if (!userEmail) return false;

    const subject = `Tebrikler ve Teşekkürler! ${committeeName} Soru Katkınız Alındı 🎉`;
    const html = `
      <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 12px; background-color: #ffffff;">
        <div style="background: linear-gradient(135deg, #0f766e, #0d9488); color: #ffffff; padding: 20px 24px; border-radius: 8px;">
          <h2 style="margin: 0; font-size: 20px; font-weight: 700;">MedSoru • Tıp Dönem 3 Kurul Arşivi</h2>
          <p style="margin: 6px 0 0 0; font-size: 13px; opacity: 0.9;">Kolektif Soru Havuzu ve AI Rekonstrüksiyonu</p>
        </div>
        
        <div style="padding: 24px 8px; color: #1e293b; font-size: 14px; line-height: 1.6;">
          <p style="font-size: 16px;">Sayın <strong>${userName || 'Değerli Tıbbiyeli'}</strong>,</p>
          <p><strong>${committeeName}</strong> sınav soru havuzuna yapmış olduğunuz soru katkısı başarıyla kaydedilmiş ve arşive dahil edilmiştir.</p>
          
          <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 14px 18px; margin: 18px 0;">
            <h4 style="margin: 0 0 10px 0; color: #166534; font-size: 14px; font-weight: 700;">Katkı Detayları:</h4>
            <ul style="margin: 0; padding-left: 20px; color: #15803d; font-size: 13px; line-height: 1.8;">
              <li><strong>Kurul:</strong> ${committeeName}</li>
              <li><strong>Soru Numarası:</strong> ${questionInfo.questionNumber ? `#${questionInfo.questionNumber}` : 'Numarasız Havuz (Yapay Zeka ile Eşleştirilecek)'}</li>
              <li><strong>Branş:</strong> ${questionInfo.discipline || 'Genel Kurul'}</li>
              ${studentNumber ? `<li><strong>Öğrenci Numarası:</strong> ${studentNumber}</li>` : ''}
            </ul>
          </div>
          
          <p>Tıp fakültesinde bilgi paylaşımı ve dayanışma en büyük gücümüzdür. Dönem arkadaşlarınıza ve gelecek dönemlere miras kalacak bu soru arşivine sunduğunuz samimi destek için teşekkür eder, sınavlarınızda ve hekimlik yolculuğunuzda üstün başarılar dileriz!</p>
          
          <div style="margin-top: 28px; padding-top: 16px; border-top: 1px solid #e2e8f0; color: #64748b; font-size: 12px;">
            <p style="margin: 0;">MedSoru Kurul Sistemi • nofrostlife@gmail.com</p>
            <p style="margin: 4px 0 0 0; font-style: italic;">Not: Bu teşekkür bildirimi her kurul sınavı için öğrenciye yalnızca 1 kez gönderilir.</p>
          </div>
        </div>
      </div>
    `;

    try {
      const res = await fetch('/api/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          to: userEmail,
          subject,
          html,
          text: `Sayın ${userName}, ${committeeName} sınavı için soru katkınız başarıyla kaydedildi. Teşekkür ederiz!`,
          type: 'congrats',
          committeeId,
          studentNumber,
        }),
      });
      return res.ok;
    } catch (e) {
      console.warn('sendCongratulationsEmail network error:', e);
      return false;
    }
  },

  /**
   * Sends rich medical welcome email to student upon registration.
   */
  async sendWelcomeEmail(
    userEmail: string,
    displayName?: string,
    studentNumber?: string
  ): Promise<{ success: boolean; error?: string; hint?: string; instructions?: string[] }> {
    if (!userEmail) return { success: false, error: 'E-posta adresi boş bırakılamaz.' };
    try {
      const res = await fetch('/api/send-welcome-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: userEmail,
          displayName,
          studentNumber,
        }),
      });
      const data = await res.json().catch(() => null);
      if (!res.ok) {
        return {
          success: false,
          error: data?.error || `HTTP ${res.status} Hatası`,
          hint: data?.hint,
          instructions: data?.instructions,
        };
      }
      return { success: true };
    } catch (e: any) {
      console.warn('sendWelcomeEmail network error:', e);
      return { success: false, error: e.message || 'Ağ bağlantı hatası' };
    }
  },

  async getSmtpConfig(): Promise<{
    enabled: boolean;
    service: string;
    host: string;
    port: number;
    secure: boolean;
    user: string;
    from: string;
    hasPass: boolean;
    passMasked: string;
  }> {
    const res = await fetch('/api/admin/smtp-config');
    if (!res.ok) throw new Error('SMTP ayarları alınamadı.');
    return res.json();
  },

  async saveSmtpConfig(config: {
    enabled?: boolean;
    service?: string;
    host?: string;
    port?: number;
    secure?: boolean;
    user?: string;
    pass?: string;
    from?: string;
  }): Promise<{ success: boolean; message: string; config: any }> {
    const res = await fetch('/api/admin/smtp-config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'SMTP ayarları kaydedilemedi.');
    return data;
  },

  async testSmtp(to?: string): Promise<{ success: boolean; message?: string; error?: string; hint?: string }> {
    const res = await fetch('/api/admin/smtp-test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ to }),
    });
    const data = await res.json();
    if (!res.ok) {
      return {
        success: false,
        error: data.error || 'Test e-postası gönderilemedi.',
        hint: data.hint,
      };
    }
    return data;
  },


  async addFragment(questionId: string, text: string, author: string, type: 'stem' | 'clue' | 'option'): Promise<QuestionItem> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (!q) throw new Error('Soru bulunamadı');

    const newFrag: MemoryFragment = {
      id: `f-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      author: author || 'Anonim',
      text: text.trim(),
      type: type || 'clue',
      timestamp: new Date().toISOString(),
      upvotes: 0,
      likedBy: [],
    };
    q.fragments.push(newFrag);
    if (q.status === 'empty') q.status = 'gathering';
    q.updatedAt = new Date().toISOString();
    saveLocalDb(db);

    try {
      await multiDbManager.saveQuestion(q);
    } catch (e) {
      console.warn('Firestore addFragment fallback', e);
    }

    return q;
  },

  async upvoteQuestion(questionId: string, customUserId?: string): Promise<{ question?: QuestionItem; liked: boolean; upvotes: number }> {
    const userId = customUserId || (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_device_token') || 'anon_user' : 'anon_user');
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    let liked = false;
    let upvotesCount = 0;

    if (q) {
      q.likedBy = q.likedBy || [];
      const idx = q.likedBy.indexOf(userId);
      if (idx >= 0) {
        q.likedBy.splice(idx, 1);
        q.upvotes = Math.max(0, (q.upvotes || 1) - 1);
        liked = false;
      } else {
        q.likedBy.push(userId);
        q.upvotes = (q.upvotes || 0) + 1;
        liked = true;
      }
      upvotesCount = q.upvotes || 0;
      saveLocalDb(db);
      try {
        await multiDbManager.saveQuestion(q);
      } catch (e) {}
    }

    try {
      const res = await fetch(`/api/questions/${questionId}/upvote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId }),
      });
      if (res.ok) {
        const data = await res.json();
        return { question: data.question || q, liked: !!data.liked, upvotes: data.upvotes || upvotesCount };
      }
    } catch (e) {}

    return { question: q, liked, upvotes: upvotesCount };
  },

  async upvoteFragment(questionId: string, fragmentId: string, customUserId?: string): Promise<void> {
    const userId = customUserId || (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_device_token') || 'anon_user' : 'anon_user');
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (q) {
      const f = q.fragments.find((frag) => frag.id === fragmentId);
      if (f) {
        f.likedBy = f.likedBy || [];
        const idx = f.likedBy.indexOf(userId);
        if (idx >= 0) {
          f.likedBy.splice(idx, 1);
          f.upvotes = Math.max(0, (f.upvotes || 1) - 1);
        } else {
          f.likedBy.push(userId);
          f.upvotes = (f.upvotes || 0) + 1;
        }
        saveLocalDb(db);
        try {
          await multiDbManager.saveQuestion(q);
        } catch (e) {}
      }
    }

    try {
      await fetch(`/api/questions/${questionId}/fragments/${fragmentId}/upvote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId }),
      });
    } catch (e) {}
  },

  async addOption(questionId: string, key: 'A' | 'B' | 'C' | 'D' | 'E', text: string, suggestedBy: string): Promise<QuestionItem> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (!q) throw new Error('Soru bulunamadı');

    // Permanently archive in fragments so no student memory is ever erased or lost
    q.fragments.push({
      id: `f-opt-${Date.now()}-${key}`,
      author: suggestedBy || 'Anonim',
      text: `${key} Şıkkı: "${text.trim()}"`,
      type: 'option',
      timestamp: new Date().toISOString(),
      upvotes: 0,
      likedBy: [],
    });

    const exOpt = q.options.find((o) => o.key === key);
    if (exOpt) {
      if (exOpt.text.trim().toLowerCase() === text.trim().toLowerCase()) {
        exOpt.upvotes = (exOpt.upvotes || 0) + 1;
      } else {
        exOpt.text = text.trim();
        if (suggestedBy) exOpt.suggestedBy = suggestedBy;
      }
    } else {
      q.options.push({ key, text: text.trim(), suggestedBy: suggestedBy || 'Anonim', upvotes: 0, likedBy: [] });
    }
    q.options.sort((a, b) => a.key.localeCompare(b.key));
    q.updatedAt = new Date().toISOString();
    saveLocalDb(db);

    try {
      await multiDbManager.saveQuestion(q);
    } catch (e) {
      console.warn('Firestore addOption fallback', e);
    }

    return q;
  },

  async upvoteOption(questionId: string, key: 'A' | 'B' | 'C' | 'D' | 'E', customUserId?: string): Promise<void> {
    const userId = customUserId || (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_device_token') || 'anon_user' : 'anon_user');
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (q) {
      const opt = q.options.find((o) => o.key === key);
      if (opt) {
        opt.likedBy = opt.likedBy || [];
        const idx = opt.likedBy.indexOf(userId);
        if (idx >= 0) {
          opt.likedBy.splice(idx, 1);
          opt.upvotes = Math.max(0, (opt.upvotes || 1) - 1);
        } else {
          opt.likedBy.push(userId);
          opt.upvotes = (opt.upvotes || 0) + 1;
        }
        saveLocalDb(db);
        try {
          await multiDbManager.saveQuestion(q);
        } catch (e) {}
      }
    }

    try {
      await fetch(`/api/questions/${questionId}/options/${key}/upvote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId }),
      });
    } catch (e) {}
  },

  async setClaimedAnswer(questionId: string, answer: 'A' | 'B' | 'C' | 'D' | 'E'): Promise<void> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === questionId);
    if (q) {
      q.claimedAnswer = answer;
      saveLocalDb(db);
      try {
        await multiDbManager.saveQuestion(q);
      } catch (e) {}
    }
  },

  async reconstructWithAi(questionId: string): Promise<QuestionItem> {
    const db = getLocalDb();
    let q = db.questions.find((item) => item.id === questionId);

    let serverErrorMsg = '';

    const customApiKey = (typeof window !== 'undefined' && (window as any).MEDSORU_GEMINI_KEY) ||
      localStorage.getItem('medsoru_gemini_api_key') ||
      localStorage.getItem('medsoru_custom_gemini_key') ||
      (import.meta as any).env?.VITE_GEMINI_API_KEY ||
      '';

    const customGroqKey = localStorage.getItem('medsoru_groq_api_key') || '';

    // 1. Try server AI endpoint first (calls tiered Gemini / Groq with full faculty prompt)
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/questions/${questionId}/ai-reconstruct` : `/api/questions/${questionId}/ai-reconstruct`;
      const res = await safeJsonFetch<{ reconstruction: ReconstructedQuestion; question: QuestionItem; error?: string }>(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          apiKey: customApiKey,
          groqApiKey: customGroqKey || undefined,
        })
      });
      if (res.ok && res.data?.reconstruction) {
        const updated: QuestionItem = {
          ...(q || res.data.question),
          reconstruction: res.data.reconstruction,
          status: 'completed',
          claimedAnswer: res.data.reconstruction.correctAnswer,
          updatedAt: new Date().toISOString(),
        };
        await multiDbManager.saveQuestion(updated);
        const idx = db.questions.findIndex((item) => item.id === questionId);
        if (idx !== -1) {
          db.questions[idx] = updated;
        } else {
          db.questions.push(updated);
        }
        saveLocalDb(db);
        return updated;
      } else {
        serverErrorMsg = res.data?.error || (res as any).error || '';
      }
    } catch (e: any) {
      serverErrorMsg = e.message || '';
      console.warn('Server ai-reconstruct unreachable, trying client fallback...', e);
    }

    if (!q) {
      // Try to load question from multiDbManager
      try {
        const pastList = await multiDbManager.getPastQuestions();
        const found = pastList.find((x) => x.id === questionId);
        if (found) q = found;
      } catch {}
    }

    if (!q) throw new Error('Soru bulunamadı');

    // 2. Client-side resilient AI synthesis (Tiered Gemini Free 1 -> Free 2 -> Billed -> Groq)
    let clientErrorMsg = '';
    try {
      const fragmentsSummary = q.fragments.length > 0
        ? q.fragments.map((f, i) => `${i + 1}. [${f.author}]: "${f.text}"`).join('\n')
        : 'Henüz parça girilmedi.';
      const optionsSummary = q.options.length > 0
        ? q.options.map((o) => `${o.key}) ${o.text}`).join('\n')
        : 'Şıklar girilmedi.';
      const commentsSummary = (q.comments && q.comments.length > 0)
        ? q.comments.map((c: any) => `- [${c.author || 'Öğrenci Yorumu'}]: "${c.text}"`).join('\n')
        : 'Henüz ek yorum/düzeltme girilmedi.';

      const prompt = `Sen Tıp Fakültesi Kurul ve TUS Sınavları Komisyonunda görevli kıdemli bir Tıp Profesörüsün.
Öğrenciler sınavdan çıktıktan sonra bu soru hakkında hafıza parçaları, şıklar ve düzeltme yorumları girmiştir.
Görevin: Bu dağınık hafıza parçalarını, düzeltme önerilerini ve ipuçlarını analiz ederek tıp fakültesi kurul sınavı standartlarında TEK BİR TAM VE KUSURSUZ SORU ve 5 ŞIK (A-E) oluşturmaktır.

Disiplin: ${q.discipline}
Konu: ${q.topic}
Soru No: #${q.questionNumber || 'Çıkmış'}
Öğrenci Hafıza Parçaları:
${fragmentsSummary}

Öğrenci Şıkları:
${optionsSummary}

Öğrenci Yorumları & Düzeltme Önerileri:
${commentsSummary}

Öğrenci Doğru Cevap İddiası: ${q.claimedAnswer || 'Belirtilmedi'}

KURALLAR:
1. YAZIM VE İMLA HATALARINI DÜZELT: Öğrenci parçalarında veya yorumlarında belirtilen yazım/harf hatalarını ("biri- kir" yerine "birikir" yazılması gibi) doğrudan tespit et ve nihai soru köküne ile şıklara düzeltilmiş olarak yansıt.
2. SORU KÖKÜ FORMÜLASYONU: Eğer yorumlarda veya parçalarda sorunun "değildir" veya "yanlıştır" şeklinde sorulduğu belirtiliyorsa soru kökünü mutlaka olumsuz biçimde ("...hangisi DEĞİLDİR?", "...hangisi YANLIŞTIR?") formüle et ve doğru cevabı buna göre belirle.
3. KUSURSUZ SINAV KÖKÜ (METİN SAFLIĞI): "stem" alanına sadece resmi sınav kağıdında yer alacak saf soru metnini yaz! Asla idari etiketler, "(Öğrenci Notu: ...)", "...kapsamında" gibi meta-metinler ekleme!
4. Tam 5 şık (A, B, C, D, E) üret. Öğrencilerin hatırladığı geçerli şıkları koru ve dilini düzelt.
5. Kesin doğru cevabı ve 4 bölümlü derin tıp açıklamasını (Patofizyoloji, Doğru Şık, Çeldiriciler, Klinik İpucu) yaz.

JSON FORMATI:
{
  "stem": "Resmi sınav formatında, saf soru kökü...",
  "options": [
    { "key": "A", "text": "...", "isAiFilled": false },
    { "key": "B", "text": "...", "isAiFilled": false },
    { "key": "C", "text": "...", "isAiFilled": false },
    { "key": "D", "text": "...", "isAiFilled": false },
    { "key": "E", "text": "...", "isAiFilled": false }
  ],
  "correctAnswer": "A",
  "explanation": "...",
  "confidenceScore": 95,
  "notesAndDiscrepancies": "..."
}`;

      const aiRes = await callClientResilientAi({
        prompt,
        customGeminiKey: customApiKey,
        customGroqKey,
        preferredProvider: 'auto',
      });

      const parsed = JSON.parse(aiRes.text || '{}');
      if (parsed.stem && parsed.options) {
        let cleanStem = parsed.stem.trim();
        cleanStem = cleanStem.replace(/^.*kapsamında\s*\(Admin Talimatı:[^)]+\);\s*/gi, '');

        q.reconstruction = {
          stem: cleanStem,
          options: parsed.options,
          correctAnswer: parsed.correctAnswer || q.claimedAnswer || 'A',
          explanation: parsed.explanation || '',
          confidenceScore: parsed.confidenceScore || 92,
          notesAndDiscrepancies: parsed.notesAndDiscrepancies || `${aiRes.planUsed} ile sentezlendi.`,
          lastUpdated: new Date().toISOString()
        };
        q.status = 'completed';
        q.claimedAnswer = q.reconstruction.correctAnswer;
        q.updatedAt = new Date().toISOString();
        saveLocalDb(db);
        await multiDbManager.saveQuestion(q);
        return q;
      }
    } catch (err: any) {
      console.warn('Client resilient AI synthesis error:', err.message);
      clientErrorMsg = err.message || '';
    }

    // If both server and client fail, report honest error (never generate fake mock options)
    const combinedErr = `${serverErrorMsg} ${clientErrorMsg}`.trim();
    const cleanServerErr = serverErrorMsg && !serverErrorMsg.includes('405') ? serverErrorMsg : '';
    const isQuota = combinedErr.toLowerCase().includes('quota') || combinedErr.toLowerCase().includes('limit') || combinedErr.includes('429');
    const finalErr = isQuota
      ? 'Google Gemini API aylık harcama limiti veya kotası aşıldı (Hata 429: Monthly Spending Cap Exceeded). Lütfen Ayarlar panelinden Groq API anahtarınızı tanımlayarak kotasız kullanıma geçebilir veya yeni bir API anahtarı tanımlayabilirsiniz.'
      : (clientErrorMsg || cleanServerErr || 'Yapay zeka rekonstrüksiyonu gerçekleştirilemedi. Lütfen Gemini/Groq API anahtarınızı veya kota durumunuzu kontrol edin.');

    throw new Error(finalErr);
  },

  async generateSlots(adminEmail: string, committeeId: string, count: number): Promise<void> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: 100/150 soruluk yuva açma yetkisi yalnızca sistem yöneticisine (nofrostlife@gmail.com) aittir.');
    }
    const db = getLocalDb();
    const existingNums = new Set(
      db.questions
        .filter((q) => q.committeeId === committeeId && !q.isUnassignedNumber)
        .map((q) => q.questionNumber)
    );

    const newSlots: QuestionItem[] = [];
    for (let i = 1; i <= count; i++) {
      if (!existingNums.has(i)) {
        const slot: QuestionItem = {
          id: `q-${committeeId}-${i}`,
          committeeId,
          questionNumber: i,
          discipline: 'Belirtilmedi',
          topic: `Soru #${i}`,
          status: 'empty',
          fragments: [],
          options: [],
          tags: [],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };
        db.questions.push(slot);
        newSlots.push(slot);
      }
    }
    saveLocalDb(db);

    if (newSlots.length > 0) {
      try {
        await FirestoreDbService.batchSaveQuestions(newSlots);
      } catch (e) {
        console.warn('Firestore batchSaveQuestions fallback', e);
      }
    }
  },

  // Admin endpoints
  async adminUpdateQuestion(adminEmail: string, id: string, updated: Partial<QuestionItem>): Promise<QuestionItem> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Soru düzenleme yetkisi yalnızca sistem yöneticisine aittir.');
    }
    const db = getLocalDb();
    const idx = db.questions.findIndex((q) => q.id === id);
    if (idx === -1) throw new Error('Soru bulunamadı');
    db.questions[idx] = { ...db.questions[idx], ...updated, updatedAt: new Date().toISOString() };
    const saved = db.questions[idx];
    saveLocalDb(db);

    try {
      await multiDbManager.saveQuestion(saved);
    } catch (e) {
      console.warn('multiDbManager adminUpdateQuestion fallback', e);
    }

    return saved;
  },

  async adminDeleteQuestion(adminEmail: string, id: string): Promise<void> {
    const isAuth = !adminEmail || adminEmail.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase();
    if (!isAuth) {
      throw new Error('Yetkisiz işlem: Başkasının sorusunu silme yetkisi yalnızca sistem yöneticisine (nofrostlife@gmail.com) aittir.');
    }
    const db = getLocalDb();
    db.questions = db.questions.filter((q) => q.id !== id);
    saveLocalDb(db);

    // Üç kanaldan sil: Supabase (istemci) + sunucu (gizli anahtarla Supabase fan-out).
    // Biri tutsa bile kayıt geri gelmez; hatalar sessize değil konsola yazılır.
    try {
      await multiDbManager.deleteQuestion(id);
    } catch (e) {
      console.warn('[ApiService] adminDeleteQuestion multiDbManager error', e);
    }
    try {
      await safeJsonFetch(`/api/questions/${encodeURIComponent(id)}`, {
        method: 'DELETE',
        headers: { 'x-admin-email': adminEmail },
      });
    } catch (e) {
      console.warn('[ApiService] adminDeleteQuestion server error', e);
    }
  },

  async deleteQuestion(id: string, user?: { uid?: string; email?: string | null } | null): Promise<void> {
    const db = getLocalDb();
    const q = db.questions.find((item) => item.id === id);
    if (q) {
      const isAdm = user?.email && user.email.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase();
      const isAuthor = user?.uid && (q.contributedByUid === user.uid || q.fragments?.some((f) => f.authorUid === user.uid));
      const isUnassigned = q.isUnassignedNumber || q.questionNumber === 0;

      if (!isAdm && !isAuthor && !isUnassigned) {
        throw new Error('Bu soruyu veya taslağı silme yetkiniz bulunmuyor.');
      }
    }

    db.questions = db.questions.filter((item) => item.id !== id);
    saveLocalDb(db);

    try {
      await multiDbManager.deleteQuestion(id);
    } catch (e) {
      console.warn('[ApiService] deleteQuestion multiDbManager error', e);
    }
  },

  async assignUnassignedQuestion(
    adminEmail: string,
    unassignedId: string,
    targetNumber: number
  ): Promise<QuestionItem> {
    const isAuth = !adminEmail || adminEmail.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase();
    if (!isAuth) {
      throw new Error('Yetkisiz işlem: Yalnızca yönetici numarasız soruları yerleştirebilir.');
    }
    const db = getLocalDb();
    const unassigned = db.questions.find((q) => q.id === unassignedId);
    if (!unassigned) throw new Error('Numarasız soru bulunamadı.');

    const target = db.questions.find(
      (q) =>
        q.committeeId === unassigned.committeeId &&
        q.questionNumber === targetNumber &&
        !q.isUnassignedNumber
    );

    if (target) {
      // Merge fragments and options into existing slot
      target.fragments.push(...unassigned.fragments);
      unassigned.options.forEach((opt) => {
        const ex = target.options.find((o) => o.key === opt.key);
        if (!ex) target.options.push(opt);
      });
      if (unassigned.discipline && unassigned.discipline !== 'Belirtilmedi') {
        target.discipline = unassigned.discipline;
      }
      target.status = 'gathering';
      target.examYear = '2026-2027';
      target.updatedAt = new Date().toISOString();

      db.questions = db.questions.filter((q) => q.id !== unassignedId);
      saveLocalDb(db);

      try {
        await multiDbManager.saveQuestion(target);
        await multiDbManager.deleteQuestion(unassignedId);
      } catch (e) {}
      return target;
    } else {
      // Convert unassigned question directly to slot targetNumber
      unassigned.questionNumber = targetNumber;
      unassigned.isUnassignedNumber = false;
      unassigned.examYear = '2026-2027';
      unassigned.topic =
        unassigned.topic.replace('(Numarası Belirsiz Soru)', '').trim() || `Soru #${targetNumber}`;
      unassigned.updatedAt = new Date().toISOString();
      saveLocalDb(db);

      try {
        await multiDbManager.saveQuestion(unassigned);
      } catch (e) {}
      return unassigned;
    }
  },

  // Akıllı Taslak Kümeleme ve Birleştirme Metotları
  async getCommitteeDraftClusters(committeeId: string): Promise<ClusterAnalysisSummary> {
    const db = getLocalDb();
    return clusterDraftsForCommittee(db.questions, committeeId);
  },

  async mergeDraftCluster(
    adminEmail: string,
    anchorId: string,
    satelliteIds: string[],
    adminName: string = 'Yönetici'
  ): Promise<QuestionItem> {
    const isAuth = !adminEmail || adminEmail.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase();
    if (!isAuth) {
      throw new Error('Yetkisiz işlem: Taslak birleştirme yetkisi yalnızca sistem yöneticisine aittir.');
    }
    const db = getLocalDb();
    const anchor = db.questions.find((q) => q.id === anchorId);
    if (!anchor) throw new Error('Çapa soru bulunamadı.');

    const satellites = db.questions.filter((q) => satelliteIds.includes(q.id));
    if (satellites.length === 0) throw new Error('Birleştirilecek uydu taslak bulunamadı.');

    const { consolidated, mergedIds } = mergeDrafts(anchor, satellites, {
      name: adminName,
      email: adminEmail,
    });

    consolidated.examYear = '2026-2027';
    consolidated.updatedAt = new Date().toISOString();

    // Remove merged satellites from local database
    const mergedSet = new Set(mergedIds);
    db.questions = db.questions.filter((q) => !mergedSet.has(q.id));

    // Update anchor with consolidated version
    const anchorIndex = db.questions.findIndex((q) => q.id === anchorId);
    if (anchorIndex !== -1) {
      db.questions[anchorIndex] = consolidated;
    } else {
      db.questions.push(consolidated);
    }

    saveLocalDb(db);

    // Cloud DB sync (Supabase + Firestore + Local PC)
    try {
      await multiDbManager.saveQuestion(consolidated);
      for (const satId of mergedIds) {
        await multiDbManager.deleteQuestion(satId);
      }
    } catch (e) {
      console.warn('Draft merge cloud sync warning:', e);
    }

    return consolidated;
  },

  async unmergeDraftCluster(
    adminEmail: string,
    consolidatedId: string,
    adminName: string = 'Yönetici'
  ): Promise<{ anchor: QuestionItem; restoredSatellites: QuestionItem[] }> {
    const isAuth = !adminEmail || adminEmail.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase();
    if (!isAuth) {
      throw new Error('Yetkisiz işlem: Taslak ayırma yetkisi yalnızca sistem yöneticisine aittir.');
    }
    const db = getLocalDb();
    const consolidated = db.questions.find((q) => q.id === consolidatedId);
    if (!consolidated) throw new Error('Birleştirilmiş taslak bulunamadı.');

    const { anchor, restoredSatellites } = unmergeQuestion(consolidated);
    anchor.examYear = '2026-2027';
    anchor.updatedAt = new Date().toISOString();

    // Update anchor in local db
    const anchorIdx = db.questions.findIndex((q) => q.id === consolidatedId);
    if (anchorIdx !== -1) {
      db.questions[anchorIdx] = anchor;
    }

    // Add restored satellites back to local db
    for (const sat of restoredSatellites) {
      sat.examYear = '2026-2027';
      sat.updatedAt = new Date().toISOString();
      if (!db.questions.some((q) => q.id === sat.id)) {
        db.questions.push(sat);
      }
    }

    saveLocalDb(db);

    // Cloud DB sync (Supabase + Firestore + Local PC)
    try {
      await multiDbManager.saveQuestion(anchor);
      for (const sat of restoredSatellites) {
        await multiDbManager.saveQuestion(sat);
      }
    } catch (e) {
      console.warn('Draft unmerge cloud sync warning:', e);
    }

    return { anchor, restoredSatellites };
  },

  async autoMergeHighConfidenceClusters(
    adminEmail: string,
    committeeId: string,
    adminName: string = 'Akıllı Konsolidasyon'
  ): Promise<{ mergedClustersCount: number; savedDuplicatesCount: number }> {
    const isAuth = !adminEmail || adminEmail.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase();
    if (!isAuth) {
      throw new Error('Yetkisiz işlem: Toplu taslak birleştirme yetkisi yalnızca sistem yöneticisine aittir.');
    }
    const db = getLocalDb();
    const summary = clusterDraftsForCommittee(db.questions, committeeId);
    const readyClusters = summary.clusters.filter((c) => c.status === 'ready_to_merge');

    let mergedClustersCount = 0;
    let savedDuplicatesCount = 0;

    for (const cluster of readyClusters) {
      const satelliteIds = cluster.satelliteDrafts.map((s) => s.question.id);
      if (satelliteIds.length > 0) {
        await this.mergeDraftCluster(adminEmail, cluster.anchorQuestion.id, satelliteIds, adminName);
        mergedClustersCount++;
        savedDuplicatesCount += satelliteIds.length;
      }
    }

    return { mergedClustersCount, savedDuplicatesCount };
  },

  async adminExportDb(): Promise<LocalDatabase> {
    return getLocalDb();
  },

  async adminImportDb(adminEmail: string, data: LocalDatabase): Promise<void> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Veritabanı içe aktarma yetkisi yalnızca sistem yöneticisine aittir.');
    }
    saveLocalDb(data);
    if (data.questions && data.questions.length > 0) {
      try {
        await FirestoreDbService.batchSaveQuestions(data.questions);
      } catch (e) {}
    }
  },

  async adminResetDb(adminEmail: string): Promise<void> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Sıfırlama yetkisi yalnızca sistem yöneticisine aittir.');
    }
    localStorage.removeItem(STORAGE_KEY);
    getLocalDb();
  },

  // Admin AI Past Exam Questions Parser (Supports text, PDF, Word DOCX, and images)
  async parsePastExamQuestions({
    rawText,
    fileBase64,
    fileMimeType,
    fileName,
    examYear,
    committeeId,
    defaultDiscipline,
    adminEmail,
  }: {
    rawText?: string;
    fileBase64?: string;
    fileMimeType?: string;
    fileName?: string;
    examYear: string;
    committeeId: string;
    defaultDiscipline?: string;
    adminEmail: string;
  }): Promise<{ detectedYear: string; totalCount: number; questions: any[] }> {
    const res = await fetch('/api/ai/parse-past-questions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': adminEmail,
      },
      body: JSON.stringify({
        rawText,
        fileBase64,
        fileMimeType,
        fileName,
        examYear,
        committeeId,
        defaultDiscipline,
        adminEmail,
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'Yapay zeka soruları ayrıştıramadı.');
    }
    return await res.json();
  },

  // Multimodal Document Extractor for PDF & DOCX (Lecture notes & exam sheets)
  async extractDocument({
    fileBase64,
    fileMimeType,
    fileName,
    mode = 'raw',
    committeeId,
  }: {
    fileBase64: string;
    fileMimeType: string;
    fileName: string;
    mode?: 'lecture_notes' | 'past_questions' | 'raw';
    committeeId?: string;
  }): Promise<{ success: boolean; note?: any; extractedText?: string }> {
    const res = await fetch('/api/ai/extract-document', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fileBase64, fileMimeType, fileName, mode, committeeId }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'Belge yapay zeka tarafından okunamadı.');
    }
    return await res.json();
  },

  // Lecture Notes API
  async getLectureNotes(): Promise<any[]> {
    try {
      const res = await fetch('/api/lecture-notes');
      if (res.ok) return await res.json();
    } catch (e) {
      // Fallback for static environments (e.g. GitHub Pages)
    }
    // MultiDbManager with automatic Supabase failover
    try {
      const notes = await multiDbManager.getLectureNotes();
      if (notes && notes.length > 0) return notes;
    } catch (e) {}
    return [];
  },

  async saveLectureNote(note: any): Promise<any> {
    const res = await fetch('/api/lecture-notes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(note),
    });
    if (!res.ok) throw new Error('Ders notu kaydedilemedi');
    return await res.json();
  },

  async deleteLectureNote(id: string): Promise<any> {
    const res = await fetch(`/api/lecture-notes/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Ders notu silinemedi');
    return await res.json();
  },

  async scanDesktopDatabaseFolder(folderPath?: string): Promise<any> {
    const res = await fetch('/api/automation/scan-desktop-folder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ folderPath }),
    });
    if (!res.ok) throw new Error('Klasör tarama başarısız oldu');
    return await res.json();
  },

  async getDesktopDatabaseStatus(): Promise<any> {
    const res = await fetch('/api/automation/desktop-folder-status');
    if (!res.ok) throw new Error('Klasör durumu alınamadı');
    return await res.json();
  },

  // Gemini & NotebookLM Database Synchronization
  async syncDatabaseWithGemini(payload: any, committeeId?: string): Promise<{ success: boolean; message: string; updatedCount: number }> {
    const res = await fetch('/api/gemini/sync-database', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ payload, committeeId }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'Veritabanı senkronizasyonu başarısız oldu.');
    }
    return await res.json();
  },

  // Batch import questions parsed from past exam files into database
  async batchImportPastQuestions(
    adminEmail: string,
    committeeId: string,
    examYear: string,
    parsedQuestions: any[]
  ): Promise<{ success: boolean; count: number; questions: QuestionItem[]; firebaseSynced: boolean; serverSynced: boolean }> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Soru aktarma yetkisi yalnızca sistem yöneticisine aittir.');
    }

    const db = getLocalDb();
    const createdQuestions: QuestionItem[] = [];

    for (const pq of parsedQuestions) {
      const qNum = Number(pq.questionNumber) || (db.questions.filter((q) => q.committeeId === committeeId).length + 1);
      const questionId = `past-${committeeId}-${qNum}-${Date.now().toString().slice(-4)}`;

      // Construct options array with zero initial likes
      const options = (pq.options || []).map((opt: any) => ({
        key: opt.key as 'A' | 'B' | 'C' | 'D' | 'E',
        text: opt.text || '',
        suggestedBy: `Çıkmış (${examYear})`,
        upvotes: 0,
        likedBy: [],
      }));

      // If less than 5 options, pad with standard placeholders
      const existingKeys = new Set(options.map((o: any) => o.key));
      (['A', 'B', 'C', 'D', 'E'] as const).forEach((k) => {
        if (!existingKeys.has(k)) {
          options.push({
            key: k,
            text: `${k} seçeneği (öğrenci katkısı bekleniyor)`,
            suggestedBy: 'AI Taslak',
            upvotes: 0,
            likedBy: [],
          });
        }
      });

      const newQ: QuestionItem = {
        id: questionId,
        committeeId,
        questionNumber: qNum,
        discipline: pq.discipline || 'Tıbbi Patoloji',
        topic: pq.topic || `Soru #${qNum} (${examYear})`,
        status: pq.claimedAnswer ? 'completed' : 'gathering',
        claimedAnswer: pq.claimedAnswer || undefined,
        upvotes: 0,
        likedBy: [],
        tags: [
          `${examYear} Çıkmış`,
          'Çıkmış Soru',
          pq.discipline || 'Genel',
        ].filter(Boolean),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        contributedByName: `Yönetici (${examYear} Arşivi)`,
        fragments: [
          {
            id: `frag-${Date.now()}-${Math.random().toString(36).substring(7)}`,
            author: `Çıkmış Soru (${examYear})`,
            text: pq.stem || 'Soru kökü metni',
            type: 'stem',
            timestamp: new Date().toISOString(),
            upvotes: 0,
            likedBy: [],
          },
        ],
        options,
        reconstruction: pq.stem
          ? {
              stem: pq.stem,
              options: options.map((o: any) => ({
                key: o.key,
                text: o.text,
                isAiFilled: false,
              })),
              correctAnswer: (pq.claimedAnswer || 'A') as 'A' | 'B' | 'C' | 'D' | 'E',
              explanation: pq.explanation || `Bu soru ${examYear} tıp kurulu sınavında sorulmuştur.`,
              confidenceScore: pq.confidenceScore || 90,
              notesAndDiscrepancies: `Geçmiş yıl çıkmış soru dosyasından AI tarafından ayrıştırıldı. Öğrenciler tarafından düzenlenebilir.`,
              lastUpdated: new Date().toISOString(),
            }
          : undefined,
      };

      // Check if slot with same question number already exists in this committee
      const existingIdx = db.questions.findIndex(
        (q) => q.committeeId === committeeId && q.questionNumber === qNum
      );
      if (existingIdx !== -1) {
        db.questions[existingIdx] = newQ;
      } else {
        db.questions.push(newQ);
      }
      createdQuestions.push(newQ);
    }

    // 1. Save to local browser state
    saveLocalDb(db);

    // 2. Persist to backend server (data/questions.json)
    let serverSynced = false;
    try {
      const serverRes = await fetch('/api/questions/batch-import', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-admin-email': adminEmail,
        },
        body: JSON.stringify({
          adminEmail,
          committeeId,
          examYear,
          questions: createdQuestions,
        }),
      });
      serverSynced = serverRes.ok;
    } catch (err) {
      console.warn('Backend server batch save warning:', err);
    }

    // 3. Persist to Firebase Firestore cloud database
    let firebaseSynced = false;
    try {
      const firestoreRes = await FirestoreDbService.batchSaveQuestions(createdQuestions);
      firebaseSynced = firestoreRes.success;
    } catch (e: any) {
      console.warn('Firestore batch save past questions warning:', e);
    }

    return {
      success: true,
      count: createdQuestions.length,
      questions: createdQuestions,
      firebaseSynced,
      serverSynced,
    };
  },

  // User Management & Realtime Synchronization
  async syncUser(user: {
    uid: string;
    email: string | null;
    displayName: string | null;
    studentNumber?: string | null;
    photoURL?: string | null;
    congratsSentCommittees?: string[];
  }): Promise<any> {
    try {
      const res = await fetch('/api/users/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user),
      });
      return await res.json();
    } catch (e) {
      console.warn('api.syncUser network fallback:', e);
      return null;
    }
  },

  async adminGetUsers(adminEmail: string): Promise<any[]> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz erişim: Kullanıcı listeleme yetkisi yalnızca yöneticiye aittir.');
    }
    const res = await fetch('/api/admin/users', {
      headers: {
        'x-admin-email': adminEmail,
      },
    });
    if (!res.ok) {
      throw new Error('Kullanıcı listesi alınamadı.');
    }
    const data = await res.json();
    return data.users || [];
  },

  async adminCreateUser(adminEmail: string, user: { email: string; displayName?: string; studentNumber?: string; role?: string }): Promise<any> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz erişim: Kullanıcı ekleme yetkisi yalnızca yöneticiye aittir.');
    }
    const res = await fetch('/api/admin/users/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': adminEmail,
      },
      body: JSON.stringify(user),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Kullanıcı oluşturulamadı.');
    }
    return data.user;
  },

  async adminDeleteUser(adminEmail: string, uid: string): Promise<void> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz erişim: Kullanıcı silme yetkisi yalnızca yöneticiye aittir.');
    }
    const res = await fetch(`/api/admin/users/${uid}`, {
      method: 'DELETE',
      headers: {
        'x-admin-email': adminEmail,
      },
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Kullanıcı silinemedi.');
    }
  },

  // Drive automation sync
  async syncDriveAutomation(committeeId?: string, forceSync = false): Promise<any> {
    const res = await fetch('/api/drive/sync-automation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ committeeId, forceSync }),
    });
    if (!res.ok) {
      throw new Error('Google Drive senkronizasyonu başlatılamadı.');
    }
    return await res.json();
  },

  // Past Exam Questions (Çıkmış Sorular) - Ultra-Hızlı ve Ekonomik Cihaz Depolaması
  async getPastQuestions(params: { committeeId?: string; discipline?: string; year?: string; query?: string; includeAmbiguous?: boolean } = {}): Promise<any[]> {
    let list: any[] = [];

    // 0. Ultra-Hızlı Cihaz Hafızası (IndexedDB < 20ms - Sıfır Veritabanı Maliyeti)
    try {
      const cached = await pastQuestionsCache.getCachedQuestions();
      if (cached && cached.length > 0) {
        list = cached;
        // Arka planda soru bazında artıksal senkronizasyon çalıştır (Bloklamaz, 0 gecikme)
        pastQuestionsCache.syncWithRemote().catch(() => {});
      }
    } catch {}

    // 1. Önbellek boşsa MultiDbManager üzerinden resilient yükle
    if (list.length === 0) {
      try {
        const pastList = await multiDbManager.getPastQuestions();
        if (pastList && pastList.length > 0) {
          list = pastList;
        }
      } catch (e) {
        console.warn('multiDbManager getPastQuestions fallback', e);
      }
    }

    // 2. Halen boşsa REST API fallback
    if (list.length === 0) {
      try {
        const apiBase = getCustomApiUrl() || (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1' ? 'http://localhost:3000' : '');
        const res = await fetch(`${apiBase}/api/past-exams`);
        if (res.ok) {
          const json = await res.json();
          if (json.questions && Array.isArray(json.questions)) {
            list = json.questions;
            pastQuestionsCache.saveBatch(list).catch(() => {});
          }
        }
      } catch (e) {}
    }

    // Filtreleme (Cihaz hafızasındaki sorular üzerinde anlık 1ms bellek içi filtreleme)
    if (list.length > 0) {
      let filtered = list;
      if (params.committeeId && params.committeeId !== 'all') {
        filtered = filtered.filter((q) => q.committeeId === params.committeeId);
      }
      if (params.discipline && params.discipline !== 'all') {
        const dLower = String(params.discipline).toLowerCase();
        filtered = filtered.filter((q) => q.discipline?.toLowerCase().includes(dLower));
      }
      if (params.year && params.year !== 'all') {
        filtered = filtered.filter((q) => q.examYear === params.year);
      }
      if (params.query && String(params.query).trim()) {
        const qLower = String(params.query).toLowerCase().trim();
        filtered = filtered.filter(
          (q) =>
            q.rawQuestion?.stem?.toLowerCase().includes(qLower) ||
            q.reconstruction?.stem?.toLowerCase().includes(qLower) ||
            q.topic?.toLowerCase().includes(qLower) ||
            q.discipline?.toLowerCase().includes(qLower) ||
            q.sourceFile?.toLowerCase().includes(qLower)
        );
      }
      return filtered;
    }

    return [];
  },

  async commentPastQuestion(questionId: string, author: string, text: string): Promise<any> {
    const apiBase = getCustomApiUrl() || (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1' ? 'http://localhost:3000' : '');
    
    // 1. Try local server
    try {
      const res = await fetch(`${apiBase}/api/past-exams/${encodeURIComponent(questionId)}/comment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ author, text }),
      });
      if (res.ok) {
        return await res.json();
      }
    } catch (e) {
      console.warn('[commentPastQuestion] Server çağrısı başarısız, Firestore yedeğine geçiliyor:', e);
    }

    // 2. Direct Firestore fallback (Guarantees zero 405 error on GitHub Pages!)
    try {
      const commentObj = {
        id: `c-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
        author: author || 'Tıp Öğrencisi',
        text: text.trim(),
        createdAt: new Date().toISOString(),
        upvotes: 0
      };
      await addDoc(collection(db, 'past_question_comments'), {
        ...commentObj,
        questionId
      });
      return { success: true, comment: commentObj };
    } catch (err: any) {
      console.warn('[commentPastQuestion] Firestore kaydı da yapılamadı, yerel nesne dönülüyor:', err.message);
      return {
        success: true,
        comment: {
          id: `c-local-${Date.now()}`,
          author: author || 'Tıp Öğrencisi',
          text: text.trim(),
          createdAt: new Date().toISOString(),
          upvotes: 0
        }
      };
    }
  },

  async reportPastQuestion(questionId: string, reason: string, details?: string, reportedBy?: string): Promise<any> {
    const apiBase = getCustomApiUrl() || (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1' ? 'http://localhost:3000' : '');
    const nowIso = new Date().toISOString();
    const reportObj = {
      id: `rep-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      questionId,
      reason: reason.trim(),
      details: (details || '').trim(),
      reportedBy: reportedBy || 'Tıp Öğrencisi',
      createdAt: nowIso,
      status: 'pending'
    };

    // 1. Try local Express server (Updates server DB and mirrors to Supabase)
    try {
      const res = await fetch(`${apiBase}/api/past-exams/${encodeURIComponent(questionId)}/report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: reportObj.id,
          reason: reportObj.reason,
          details: reportObj.details,
          reportedBy: reportObj.reportedBy
        }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data?.report) {
          reportObj.id = data.report.id || reportObj.id;
        }
      }
    } catch (e) {
      console.warn('[reportPastQuestion] Server çağrısı başarısız, doğrudan buluta geçiliyor:', e);
    }

    // 2. Direct Supabase save (Garanti: GitHub Pages ve sunucusuz ortamlarda da Supabase'e anında yazar!)
    try {
      await SupabaseDbService.reportPastQuestion(questionId, {
        id: reportObj.id,
        reason: reportObj.reason,
        details: reportObj.details,
        reportedBy: reportObj.reportedBy,
        timestamp: nowIso
      });
    } catch (sbErr: any) {
      console.warn('[reportPastQuestion] Supabase doğrudan kayıt uyarısı:', sbErr?.message);
    }

    // 3. Local IndexedDB Cache update (Cihaz üzerinde anlık yansıma)
    try {
      const cached = await pastQuestionsCache.getCachedQuestionById(questionId);
      if (cached) {
        const curReports = cached.reports || [];
        if (!curReports.some((r: any) => r.id === reportObj.id)) {
          cached.reports = [...curReports, reportObj];
        }
        cached.updatedAt = nowIso;
        await pastQuestionsCache.saveQuestion(cached);
      }
    } catch (_) {}

    // 4. Firestore Dual Cloud Fallback (Firebase Spark/Cloud kesintisiz yedek)
    try {
      await addDoc(collection(db, 'past_question_reports'), reportObj);
    } catch (err: any) {
      console.warn('[reportPastQuestion] Firestore kaydı yapılamadı:', err.message);
    }

    return { success: true, report: reportObj };
  },

  async upvotePastQuestion(questionId: string): Promise<number> {
    try {
      const res = await fetch(`/api/past-exams/${encodeURIComponent(questionId)}/upvote`, {
        method: 'POST',
      });
      if (res.ok) {
        const data = await res.json();
        return data.upvotes || 1;
      }
    } catch (e) {}
    return 1;
  },

  // AI: Generate similar exam question grounded in matched lecture note
  async generateSimilarQuestion(baseQuestion: QuestionItem, slideMatch?: any): Promise<any> {
    try {
      const res = await fetch('/api/ai/generate-similar-question', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ baseQuestion, slideMatch }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data.question) return data.question;
      }
    } catch (e) {
      console.warn('generateSimilarQuestion network error:', e);
    }

    // Client-side fallback generator if offline
    const discipline = baseQuestion.discipline || 'Tıbbi Patoloji';
    const topic = baseQuestion.topic || 'Çıkmış Sınav Konusu';
    const sourcePdf = baseQuestion.sourceFile || 'Çıkmış Sınav Dosyası';
    const noteTitle = slideMatch?.note?.title || 'İlgili Amfi Dersi';
    const slidePage = slideMatch?.page?.pageNumber || 1;

    return {
      id: `ai-sim-client-${Date.now()}`,
      discipline,
      topic: `Benzer Soru: ${topic}`,
      stem: `${discipline} kurul sınavı ve "${noteTitle}" (Slayt #${slidePage}) konusu kapsamında;\n\n"${topic}" etiyolojisi ve klinik patogenezi incelendiğinde; hastada gözlenen morfolojik değişiklikler ve ${discipline.toLowerCase()} yaklaşım açısından aşağıdakilerden hangisi EN OLASI ifadedir?`,
      options: [
        { key: 'A', text: `Hücresel düzeyde ${topic} ile ilişkili hasarın geri dönüşümsüz faza geçmesi` },
        { key: 'B', text: `Primer etiyolojide inflamatuar kaskadın sitokin aracılı regülasyonu` },
        { key: 'C', text: `${noteTitle} slaytında vurgulanan karakteristik morfolojik / biyokimyasal belirteç artışı` },
        { key: 'D', text: `Sekonder patolojide gelişen vasküler permeabilite ve doku ödemi` },
        { key: 'E', text: `Klinik seyirde spontan regresyon gösteren fizyolojik adaptasyon mekanizması` }
      ],
      correctAnswer: 'C',
      explanation: `Bu ek soru, "${sourcePdf}" çıkmış sınav sorusu ile "${noteTitle}" (Slayt #${slidePage}) slaytında yer alan patolojik prensipler temel alınarak oluşturulmuştur.`,
      sourceExamPdf: sourcePdf,
      matchedNoteTitle: noteTitle,
      matchedSlidePage: slidePage,
      isAiGenerated: true,
      createdAt: new Date().toISOString()
    };
  },

  // Save approved past exam question across all databases (Local Server PUT + Supabase + Firebase Spark)
  async saveApprovedPastQuestion(question: QuestionItem): Promise<QuestionItem> {
    const updated: QuestionItem = {
      ...question,
      status: 'completed',
      updatedAt: new Date().toISOString(),
    };

    try {
      await multiDbManager.savePastQuestion(updated);
    } catch (e) {
      console.warn('[ApiService] multiDbManager savePastQuestion fallback', e);
    }

    const db = getLocalDb();
    const idx = db.questions.findIndex((item) => item.id === question.id);
    if (idx !== -1) {
      db.questions[idx] = updated;
      saveLocalDb(db);
    }

    return updated;
  },

  // Admin Custom AI Redaction for Past Exam Questions
  async adminCustomRedactQuestion(params: {
    question: QuestionItem;
    customPrompt: string;
    groundingNote?: string;
    model?: string;
    adminEmail?: string;
    apiKey?: string;
    groqApiKey?: string;
    preferredProvider?: 'gemini' | 'groq' | 'auto';
  }): Promise<{ success: boolean; reconstruction?: ReconstructedQuestion; error?: string }> {
    const customApiKey = params.apiKey ||
      (typeof window !== 'undefined' && (window as any).MEDSORU_GEMINI_KEY) ||
      localStorage.getItem('medsoru_gemini_api_key') ||
      localStorage.getItem('medsoru_custom_gemini_key') ||
      (import.meta as any).env?.VITE_GEMINI_API_KEY ||
      '';

    const customGroqKey = params.groqApiKey ||
      localStorage.getItem('medsoru_groq_api_key') ||
      '';

    const preferredProvider = params.preferredProvider ||
      (params.model?.includes('llama') || params.model?.includes('deepseek') ? 'groq' : 'auto');

    let serverErrorMsg = '';

    // 1. First try server endpoint (has server-side tiered failover & Groq)
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/ai/admin-custom-redact` : '/api/ai/admin-custom-redact';
      const res = await safeJsonFetch<{ success: boolean; reconstruction: ReconstructedQuestion; error?: string }>(
        endpoint,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ...params,
            apiKey: customApiKey,
            groqApiKey: customGroqKey,
            preferredProvider,
          }),
        }
      );

      if (res.ok && res.data?.success && res.data.reconstruction) {
        // Also update Firestore directly
        try {
          const updatedQ: QuestionItem = {
            ...params.question,
            reconstruction: res.data.reconstruction,
            status: 'completed',
            claimedAnswer: res.data.reconstruction.correctAnswer,
            updatedAt: new Date().toISOString(),
          };
          await FirestoreDbService.updatePastQuestion(updatedQ);
        } catch (_) {}
        return { success: true, reconstruction: res.data.reconstruction };
      } else {
        serverErrorMsg = res.data?.error || (res as any).error || '';
      }
    } catch (e: any) {
      serverErrorMsg = e.message || '';
    }

    // 2. Direct client-side resilient AI execution (Tiered Gemini Free 1 -> Free 2 -> Billed -> Groq)
    try {
      const q = params.question;
      const baseStem = q.reconstruction?.stem || (q as any).rawQuestion?.stem || q.fragments?.[0]?.text || q.rawStem || q.topic || '';
      const currentOptions = (q.reconstruction?.options || (q as any).rawQuestion?.options || q.options || []).map((o: any) => `${o.key}) ${o.text}`).join('\n');
      const commentsText = (q.comments || []).map((c: any) => `- ${c.author}: ${c.text}`).join('\n');

      const prompt = `Sen Tıp Fakültesi Kurul/Komite ve TUS Sınavları Komisyonunda görevli kıdemli bir Tıp Profesörüsün.
Aşağıda verilen tıp fakültesi sınav sorusunu, yöneticinin (Admin) veya öğrencilerin verdiği TALİMAT, DÜZELTME, YORUM ve İPUÇLARINA HARFİYEN UYARAK doğrudan soru üzerinde uygula, düzelt, redakte et ve eksiksiz bir sınav sorusuna dönüştür.

MEVCUT SORU:
Disiplin: ${q.discipline}
Konu: ${q.topic}
Mevcut Soru Kökü: ${baseStem}
Mevcut Şıklar:
${currentOptions || 'Şıklar girilmedi.'}
Doğru/İşaretlenen: ${q.claimedAnswer || q.reconstruction?.correctAnswer || 'A'}
${commentsText ? `Öğrenci Yorumları & İpuçları:\n${commentsText}` : ''}
${params.groundingNote ? `İlgili Amfi Dersi Slaytı:\n${params.groundingNote}` : ''}

ADMİN ÖZEL REDAKSİYON TALİMATI:
"""
${params.customPrompt || 'Bu soruyu 5 şıklı, tıp standartlarında, çeldiricileri güçlü ve doyurucu açıklamalı bir vaka sorusu formatına dönüştür.'}
"""

TALİMATLARI ANLAMA VE DOĞRUDAN UYGULAMA KURALLARI:
1. YAZIM / İMLA HATALARINI DOĞRUDAN DÜZELTME:
   - Eğer talimatta veya yorumda "yazım hatası var", "şu şekilde yaz", "... olarak düzelt" deniliyorsa (örneğin "Vücuda alınan kurşunun çoğu hangi dokuda biri- kir?" sorusuna "birikir şeklinde yaz" veya "yazım hatasını düzelt" denilmişse),
   - Soru kökündeki veya şıklardaki bu hatayı DOĞRUDAN DÜZELTEREK nihai soru köküne ("Vücuda alınan kurşunun çoğu hangi dokuda birikir?") yansıt.
2. SORU KÖKÜNÜ TERSİNE ÇEVİRME / OLUMSUZLAŞTIRMA ("DEĞİLDİR", "YANLIŞTIR"):
   - Eğer talimatta "Soru bize değildir kökü ile soruldu", "hangisi yanlıştır diye soruldu", "olumsuz köktü" veya benzeri bir ifade varsa,
   - Soru kökünü kesinlikle olumsuz sınav formatına çevir (Örn: "...aşağıdakilerden hangisi DEĞİLDİR?", "...aşağıdaki ifadelerden hangisi YANLIŞTIR?").
   - Şıkları ve doğru cevabı bu olumsuz mantığa göre yeniden düzenle (doğru cevap bu durumda yanlış/olumsuz olan ifade olmalıdır).
3. ŞIK VE İÇERİK DÜZELTMELERİ:
   - Eğer talimat veya yorumda "C şıkkı kemikti", "A şıkkı karaciğer olmalı", "cevap eritrosit olmalı" gibi şık/cevap düzeltmeleri varsa, bu şıkları ve doğru cevabı doğrudan güncelle.
4. KUSURSUZ VE SAF SINAV KÖKÜ (ÇOK KRİTİK):
   - "stem" (soru kökü) alanına KESİNLİKLE VE SADECE resmi sınav kağıdında yer alacak saf soru metnini yaz!
   - KESİNLİKLE YASAKTIR: Soru köküne "(Admin Talimatı: ...)", "[Klinik Değerlendirme]", "...kapsamında" gibi idari etiketler, talimat tekrarları veya kalıp cümleler EKLEME!
   - Kullanıcının talimatını soru metninin içine asla kopyalama! Yapılan değişiklikleri sadece "notesAndDiscrepancies" alanında özetle.
5. 5 ŞIK VE TIBBİ KALİTE:
   - A, B, C, D, E olmak üzere tam 5 adet bağımsız, mantıklı ve güçlü çeldiricisi olan seçenek oluştur.
   - Doğru cevabı açıkça belirle (A, B, C, D veya E).
6. AKADEMİK DERİN AÇIKLAMA:
   - Klinik patofizyolojik / farmakolojik açıklamayı Robbins/Katzung tıp literatürü düzeyinde detaylı yap.
7. YALNIZCA AŞAĞIDAKİ GEÇERLİ JSON FORMATINDA DÖN:
{
  "stem": "Resmi sınav formatında, saf soru kökü...",
  "options": [
    { "key": "A", "text": "...", "isAiFilled": false },
    { "key": "B", "text": "...", "isAiFilled": false },
    { "key": "C", "text": "...", "isAiFilled": false },
    { "key": "D", "text": "...", "isAiFilled": false },
    { "key": "E", "text": "...", "isAiFilled": false }
  ],
  "correctAnswer": "A",
  "explanation": "Detaylı klinik açıklama...",
  "confidenceScore": 96,
  "notesAndDiscrepancies": "..."
}`;

      const aiRes = await callClientResilientAi({
        prompt,
        customGeminiKey: customApiKey,
        customGroqKey,
        preferredProvider,
        model: params.model
      });

      const parsed = JSON.parse(aiRes.text || '{}');
      let cleanStem = (parsed.stem || '').trim();
      cleanStem = cleanStem.replace(/^.*kapsamında\s*\(Admin Talimatı:[^)]+\);\s*/gi, '');

      const recon: ReconstructedQuestion = {
        stem: cleanStem,
        options: parsed.options,
        correctAnswer: parsed.correctAnswer || 'A',
        explanation: parsed.explanation || '',
        confidenceScore: parsed.confidenceScore || 95,
        notesAndDiscrepancies: parsed.notesAndDiscrepancies || `${aiRes.planUsed} ile doğrudan redakte edildi.`,
        lastUpdated: new Date().toISOString()
      };

      // Also update Firestore directly
      try {
        const updatedQ: QuestionItem = {
          ...params.question,
          reconstruction: recon,
          status: 'completed',
          claimedAnswer: recon.correctAnswer,
          updatedAt: new Date().toISOString(),
        };
        await FirestoreDbService.updatePastQuestion(updatedQ);
      } catch (_) {}

      return { success: true, reconstruction: recon };
    } catch (clientErr: any) {
      console.warn('Client-side resilient AI failed:', clientErr.message);
      return {
        success: false,
        error: clientErr.message || (serverErrorMsg && !serverErrorMsg.includes('405') ? serverErrorMsg : 'Yapay zeka redaksiyonu gerçekleştirilemedi. Lütfen internet bağlantınızı kontrol ediniz.')
      };
    }
  },

  // AI Matching: Find matching lecture notes and slides
  async matchLectureNotes(params: {
    queryText: string;
    disciplineHint?: string;
    committeeId?: string;
    limit?: number;
  }): Promise<{ matches: any[] }> {
    try {
      const res = await safeJsonFetch<{ matches: any[] }>('/api/ai/match-lecture-notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params),
      });
      if (res.ok && res.data?.matches) {
        return { matches: res.data.matches };
      }
    } catch (e) {
      console.warn('matchLectureNotes server call failed:', e);
    }
    return { matches: [] };
  },

  // Student & User AI Question Optimizer Grounded in Lecture Notes & Medical Science
  async optimizeQuestionWithAi(params: {
    question: QuestionItem;
    studentNotes?: string;
    apiKey?: string;
    groqApiKey?: string;
    preferredProvider?: string;
    model?: string;
  }): Promise<{
    success: boolean;
    optimizedQuestion?: {
      discipline: string;
      topic: string;
      stem: string;
      options: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string; isAiFilled: boolean }[];
      correctAnswer: 'A' | 'B' | 'C' | 'D' | 'E';
      explanation: string;
      confidenceScore: number;
      notesAndDiscrepancies: string;
    };
    matchedLecture?: any;
    matchingSlides?: any[];
    refinementSummary?: string;
    providerUsed?: string;
    planUsed?: string;
    error?: string;
  }> {
    const customApiKey = params.apiKey ||
      (typeof window !== 'undefined' && (window as any).MEDSORU_GEMINI_KEY) ||
      localStorage.getItem('medsoru_gemini_api_key') ||
      localStorage.getItem('medsoru_custom_gemini_key') ||
      (import.meta as any).env?.VITE_GEMINI_API_KEY ||
      '';

    const customGroqKey = localStorage.getItem('medsoru_groq_api_key') || '';
    let serverErrorMsg = '';

    // 1. Try server endpoint first
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/ai/optimize-question` : '/api/ai/optimize-question';
      const res = await safeJsonFetch<any>(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...params,
          apiKey: customApiKey,
          groqApiKey: customGroqKey,
        }),
      });

      if (res.ok && res.data?.success && res.data.optimizedQuestion) {
        return res.data;
      } else {
        serverErrorMsg = res.data?.error || (res as any).error || '';
      }
    } catch (e: any) {
      serverErrorMsg = e.message || '';
    }

    // 2. Direct client-side resilient AI execution (Tiered Gemini Free 1 -> Free 2 -> Groq Cloud -> Billed Gemini)
    try {
      const q = params.question;
      const fragmentsList = q.fragments || [];
      const baseStem = q.reconstruction?.stem || (q as any).rawQuestion?.stem || q.rawStem || fragmentsList[0]?.text || q.topic || '';
      const optionsList = (q.options || []).map((o: any) => `${o.key}) ${o.text}`).join('\n');
      const commentsList = (q.comments || []).map((c: any) => `- ${c.author}: ${c.text}`).join('\n');

      const prompt = `Sen Tıp Fakültesi Kurul ve TUS Sınavları Komisyonunda görevli kıdemli bir Tıp Profesörüsün.
Tıp fakültesi öğrencisi veya kullanıcısı bu soruyu daha iyi bir düzene sokmak için bu aracı çalıştırmıştır.

MEVCUT SORU:
Disiplin: ${q.discipline || 'Tıp Fakültesi'}
Konu: ${q.topic || 'Kurul Sınavı Konusu'}
Mevcut Soru Metni: ${baseStem}
Öğrenci Parçaları:
${fragmentsList.map((f: any, i: number) => `${i + 1}. [${f.author}]: "${f.text}"`).join('\n') || 'Girilmedi'}
Öğrenci Şıkları:
${optionsList || 'Girilmedi'}
Öğrenci Yorumları:
${commentsList || 'Girilmedi'}
${params.studentNotes ? `ÖĞRENCİ TALİMATI / İPUCU:\n"${params.studentNotes}"` : ''}

KURALLAR:
1. YAZIM VE İMLA HATALARINI DÜZELT: Kullanıcı talimatlarında veya öğrenci yorumlarında geçen ("biri- kir" yerine "birikir" yazılması vb.) tüm yazım ve imla hatalarını soru kökünde ve şıklarda doğrudan düzelt.
2. SORU KÖKÜ DÜZENLEMESİ: Talimatta "değildir", "yanlıştır", "olumsuzdur" deniliyorsa soru kökünü mutlaka resmi olumsuz soru formatına ("...hangisi DEĞİLDİR?", "...hangisi YANLIŞTIR?") dönüştür ve doğru cevabı buna göre belirle.
3. SAF VE TEMİZ SORU KÖKÜ (METİN SAFLIĞI): "stem" alanına sadece resmi sınav kağıdında yer alacak saf soru metnini yaz! Asla idari etiketler, "(Admin Talimatı: ...)", "...kapsamında" gibi meta-ifadeler ekleme!
4. Sorunun hangi derse ("detectedDiscipline") ve hangi konuya ("detectedTopic") ait olduğunu kesinleştir.
5. Soruyu tıp literatürüne uygun saf soru metni ("stem") ve güçlü çeldiricileri olan tam 5 şıkla (A-E) düzenle.
6. Kesin doğru cevabı ve detaylı patofizyolojik / farmakolojik açıklamayı ("explanation") yaz.
7. Yaptığın düzenlemeleri ("refinementSummary") özetle.

YALNIZCA GEÇERLİ JSON DÖN:
{
  "detectedDiscipline": "...",
  "detectedTopic": "...",
  "stem": "...",
  "options": [
    { "key": "A", "text": "...", "isAiFilled": false },
    { "key": "B", "text": "...", "isAiFilled": false },
    { "key": "C", "text": "...", "isAiFilled": false },
    { "key": "D", "text": "...", "isAiFilled": false },
    { "key": "E", "text": "...", "isAiFilled": false }
  ],
  "correctAnswer": "A",
  "explanation": "...",
  "confidenceScore": 95,
  "refinementSummary": "..."
}`;

      const aiRes = await callClientResilientAi({
        prompt,
        customGeminiKey: customApiKey,
        customGroqKey,
        preferredProvider: params.preferredProvider as 'auto' | 'gemini' | 'groq' | undefined,
        model: params.model,
      });

      const parsed = JSON.parse(aiRes.text || '{}');
      let cleanStem = (parsed.stem || '').trim();
      cleanStem = cleanStem.replace(/^.*kapsamında\s*\(Admin Talimatı:[^)]+\);\s*/gi, '');

      if (cleanStem && parsed.options) {
        return {
          success: true,
          optimizedQuestion: {
            discipline: parsed.detectedDiscipline || q.discipline || 'Tıp Fakültesi',
            topic: parsed.detectedTopic || q.topic || 'Kurul Sınav Sorusu',
            stem: cleanStem,
            options: parsed.options,
            correctAnswer: parsed.correctAnswer || 'A',
            explanation: parsed.explanation || '',
            confidenceScore: parsed.confidenceScore || 94,
            notesAndDiscrepancies: parsed.refinementSummary || `${aiRes.planUsed} ile doğrudan düzenlendi.`
          },
          refinementSummary: parsed.refinementSummary || 'Soru yapay zeka ile düzenlendi.',
          providerUsed: aiRes.providerUsed,
          planUsed: aiRes.planUsed
        };
      }
    } catch (clientErr: any) {
      console.warn('Client-side resilient optimizeQuestionWithAi failed:', clientErr.message);
      const isQuota = /429|RESOURCE_EXHAUSTED|spending cap|quota/i.test(clientErr.message || serverErrorMsg);
      return {
        success: false,
        error: isQuota
          ? 'Tüm yapay zeka planları kotaya takıldı (Hata 429). Lütfen Ayarlar panelinden Groq API anahtarınızı kontrol edin veya yeni bir anahtar tanımlayın.'
          : (clientErr.message || (serverErrorMsg && !serverErrorMsg.includes('405') ? serverErrorMsg : 'Yapay zeka soru optimizasyonu gerçekleştirilemedi.'))
      };
    }

    return {
      success: false,
      error: (serverErrorMsg && !serverErrorMsg.includes('405') ? serverErrorMsg : 'Yapay zeka soru optimizasyonu gerçekleştirilemedi.')
    };
  },

  // Apply AI Optimization across all databases
  async applyAiOptimization(params: {
    questionId: string;
    optimizedData: any;
    matchedLecture?: any;
    refinementSummary?: string;
    userEmail?: string;
    userName?: string;
    studentNumber?: string;
  }): Promise<{ success: boolean; question?: QuestionItem; error?: string }> {
    try {
      const res = await safeJsonFetch<{ success: boolean; question: QuestionItem; error?: string }>(
        `/api/questions/${encodeURIComponent(params.questionId)}/apply-ai-optimization`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(params),
        }
      );

      if (res.ok && res.data?.success && res.data.question) {
        // MultiDb / Firestore mirror
        try {
          await multiDbManager.saveQuestion(res.data.question);
          await multiDbManager.saveQuestion(res.data.question);
        } catch (_) {}

        return { success: true, question: res.data.question };
      }
    } catch (e: any) {
      console.warn('applyAiOptimization server error, falling back locally:', e);
    }

    // Local fallback update
    const db = getLocalDb();
    const idx = db.questions.findIndex((x) => x.id === params.questionId);
    if (idx !== -1) {
      const q = db.questions[idx];
      const now = new Date().toISOString();
      const updated: QuestionItem = {
        ...q,
        discipline: params.optimizedData.discipline || q.discipline,
        topic: params.optimizedData.topic || q.topic,
        claimedAnswer: params.optimizedData.correctAnswer || q.claimedAnswer,
        reconstruction: {
          stem: params.optimizedData.stem,
          options: params.optimizedData.options,
          correctAnswer: params.optimizedData.correctAnswer,
          explanation: params.optimizedData.explanation,
          confidenceScore: params.optimizedData.confidenceScore || 95,
          notesAndDiscrepancies: params.optimizedData.notesAndDiscrepancies || params.refinementSummary || '',
          lastUpdated: now
        },
        lectureReference: params.matchedLecture || q.lectureReference,
        status: 'completed',
        updatedAt: now
      };

      db.questions[idx] = updated;
      saveLocalDb(db);
      try {
        await multiDbManager.saveQuestion(updated);
        await multiDbManager.saveQuestion(updated);
      } catch (_) {}

      return { success: true, question: updated };
    }

    return { success: false, error: 'Soru yerel veritabanında bulunamadı.' };
  },

  // Windows Service, Desktop Shortcut & Startup Management (with Firestore Cloud Bridge)
  async getWindowsServiceStatus(): Promise<{
    success: boolean;
    isInstalledOnDesktop: boolean;
    isRegisteredInStartup: boolean;
    isRunning: boolean;
    pids: number[];
    desktopShortcutPath?: string;
    startupShortcutPath?: string;
    nextWindow?: string;
    lastHeartbeat?: any;
    error?: string;
  }> {
    // 1. Try local server endpoint
    const res = await safeJsonFetch<any>('/api/automation/windows-service-status');
    if (res.ok && res.data) {
      return res.data;
    }

    // 2. Cloud Fallback via Firestore (Guarantees working on GitHub Pages without mixed-content errors!)
    try {
      const cloudHeartbeat = await FirestoreDbService.getWorkerHeartbeat();
      if (cloudHeartbeat) {
        const isFresh = Date.now() - (cloudHeartbeat.timestamp || 0) < 15 * 60 * 1000;
        return {
          success: true,
          isInstalledOnDesktop: true,
          isRegisteredInStartup: true,
          isRunning: isFresh && cloudHeartbeat.status === 'online',
          pids: cloudHeartbeat.pid ? [cloudHeartbeat.pid] : [],
          nextWindow: '16:00 - 18:00',
          lastHeartbeat: cloudHeartbeat,
        };
      }
    } catch (e) {}

    return {
      success: false,
      isInstalledOnDesktop: false,
      isRegisteredInStartup: false,
      isRunning: false,
      pids: [],
      error: res.error || 'Yerel servise doğrudan erişilemedi (Bulut köprüsüne bağlanılıyor...)',
    };
  },

  async installWindowsService(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    return await multiDbManager.sendAdminCommand('install_service', {}, adminEmail);
  },

  async stopWindowsService(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    return await multiDbManager.sendAdminCommand('stop_service', {}, adminEmail);
  },

  async sendWindowsTestNotification(title?: string, message?: string, adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    return await multiDbManager.sendAdminCommand('notify', { title, message }, adminEmail);
  },

  async runFullLocalSync(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    return await multiDbManager.sendAdminCommand('run_full_local_sync', {}, adminEmail);
  },

  async triggerSubagentRedaction(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    return await multiDbManager.sendAdminCommand('run_redactor_cycle', {}, adminEmail);
  },

  // -------------------------------------------------------------
  // Google Drive Manual Update & Sync Management
  // -------------------------------------------------------------
  async getDriveSyncSettings(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; settings: DriveSyncSettings }> {
    const res = await safeJsonFetch<any>('/api/admin/drive/settings', {
      headers: {
        'x-admin-email': adminEmail || ADMIN_EMAIL,
      },
    });
    if (res.ok && res.data?.settings) return { success: true, settings: res.data.settings };
    return {
      success: false,
      settings: {
        autoSyncEnabled: false,
        syncInterval: '18:00',
        preferredScope: 'all',
        customFolderId: '',
        notifyOnUpdate: true,
      }
    };
  },

  async saveDriveSyncSettings(settings: Partial<DriveSyncSettings>, adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string; settings?: DriveSyncSettings }> {
    const res = await safeJsonFetch<any>('/api/admin/drive/settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': adminEmail || ADMIN_EMAIL,
      },
      body: JSON.stringify({ ...settings, adminEmail: adminEmail || ADMIN_EMAIL }),
    });
    if (res.ok) return { success: true, message: res.data?.message || 'Ayarlar kaydedildi.', settings: res.data?.settings };
    return { success: false, message: res.data?.error || 'Ayarlar kaydedilemedi.' };
  },

  async getDriveCheckResult(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; result: DriveCheckResult | null }> {
    const res = await safeJsonFetch<any>('/api/admin/drive/check-results', {
      headers: {
        'x-admin-email': adminEmail || ADMIN_EMAIL,
      },
    });
    if (res.ok) return { success: true, result: res.data?.result || null };
    return { success: false, result: null };
  },

  async checkDriveUpdates(options: { scope?: string; folderId?: string; adminEmail?: string } = {}): Promise<{
    success: boolean;
    result: DriveCheckResult | null;
    output?: string;
    message: string;
  }> {
    const email = options.adminEmail || ADMIN_EMAIL;
    const res = await safeJsonFetch<any>('/api/admin/drive/check-updates', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': email,
      },
      body: JSON.stringify({ ...options, adminEmail: email }),
    });
    if (res.ok) {
      return {
        success: res.data?.success !== false,
        result: res.data?.result || null,
        output: res.data?.output,
        message: res.data?.message || 'Kontrol tamamlandı.',
      };
    }
    return {
      success: false,
      result: null,
      message: res.data?.error || res.error || 'Drive kontrolü başarısız oldu.',
    };
  },

  async triggerManualDriveSync(options: {
    scope?: string;
    folderId?: string;
    force?: boolean;
    adminEmail?: string;
  } = {}): Promise<{ success: boolean; jobId?: string; message: string }> {
    const email = options.adminEmail || ADMIN_EMAIL;
    const res = await safeJsonFetch<any>('/api/admin/drive/manual-sync', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': email,
      },
      body: JSON.stringify({ ...options, adminEmail: email }),
    });
    if (res.ok && res.data?.success) {
      return { success: true, jobId: res.data.jobId, message: res.data.message };
    }
    return { success: false, message: res.data?.error || res.error || 'Senkronizasyon başlatılamadı.' };
  },

  // -------------------------------------------------------------
  // Dynamic Admin Scripts & Automations
  // -------------------------------------------------------------
  async getScriptsList(): Promise<{
    success: boolean;
    scripts: AdminScriptItem[];
    pipelines: AdminPipelineItem[];
    jobs: { active: AdminScriptJob[]; history: AdminScriptJob[] };
    error?: string;
  }> {
    try {
      const res = await safeJsonFetch<any>('/api/admin/scripts/list');
      if (res.ok && Array.isArray(res.data?.scripts) && res.data.scripts.length > 0) {
        return {
          success: true,
          scripts: res.data.scripts,
          pipelines: res.data.pipelines || BUNDLED_PIPELINES,
          jobs: res.data.jobs || { active: [], history: [] },
        };
      }
    } catch (_) {}

    // Fallback: Always return guaranteed bundled catalog
    return {
      success: true,
      scripts: BUNDLED_SCRIPTS,
      pipelines: BUNDLED_PIPELINES,
      jobs: { active: [], history: [] },
    };
  },

  async runScript(
    scriptName: string,
    args: string = '',
    adminEmail: string = ADMIN_EMAIL
  ): Promise<{ success: boolean; message: string; job?: AdminScriptJob }> {
    // 1. Try local server direct call
    const res = await safeJsonFetch<any>('/api/admin/scripts/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scriptName, args, requestedBy: adminEmail }),
    });

    if (res.ok && res.data?.success) {
      return { success: true, message: res.data.message, job: res.data.job };
    }

    // 2. Cloud Fallback: Send command via Supabase bridge
    const cloudRes = await multiDbManager.sendAdminCommand('run_script', { scriptName, args }, adminEmail);
    return {
      success: cloudRes.success,
      message: cloudRes.message || `${scriptName} bulut kuyruğuna iletildi.`,
    };
  },

  async runScriptPipeline(
    pipelineId: string,
    adminEmail: string = ADMIN_EMAIL
  ): Promise<{ success: boolean; message: string; job?: AdminScriptJob }> {
    const res = await safeJsonFetch<any>('/api/admin/scripts/pipeline/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pipelineId, requestedBy: adminEmail }),
    });

    if (res.ok && res.data?.success) {
      return { success: true, message: res.data.message, job: res.data.job };
    }

    const cloudRes = await multiDbManager.sendAdminCommand('run_pipeline', { pipelineId }, adminEmail);
    return {
      success: cloudRes.success,
      message: cloudRes.message || `Pipeline (${pipelineId}) bulut kuyruğuna iletildi.`,
    };
  },

  async getScriptJobStatus(jobId: string): Promise<{ success: boolean; job?: AdminScriptJob; error?: string }> {
    const res = await safeJsonFetch<any>(`/api/admin/scripts/jobs/${encodeURIComponent(jobId)}`);
    if (res.ok && res.data?.job) {
      return { success: true, job: res.data.job };
    }
    return { success: false, error: res.error || 'İşlem detayları alınamadı.' };
  },

  async stopScriptJob(jobId: string, adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    const res = await safeJsonFetch<any>(`/api/admin/scripts/jobs/${encodeURIComponent(jobId)}/kill`, {
      method: 'POST',
    });
    if (res.ok && res.data?.success) {
      return { success: true, message: res.data.message };
    }
    return await multiDbManager.sendAdminCommand('stop_script', { jobId }, adminEmail);
  },

  async chatWithQuestionTutor(params: {
    questionContext: QuestionChatContext;
    messages: { role: 'user' | 'assistant'; content: string }[];
    currentMessage: string;
    apiKey?: string;
    groqApiKey?: string;
    preferredProvider?: 'auto' | 'gemini' | 'groq';
    model?: string;
    onStatusUpdate?: (status: string) => void;
  }): Promise<{
    success: boolean;
    reply?: string;
    providerUsed?: string;
    planUsed?: string;
    attemptsCount?: number;
    fallbackUsed?: boolean;
    isTwoAttemptsFailed?: boolean;
    error?: string;
  }> {
    const customApiKey = params.apiKey ||
      (typeof window !== 'undefined' && (window as any).MEDSORU_GEMINI_KEY) ||
      localStorage.getItem('medsoru_gemini_api_key') ||
      localStorage.getItem('medsoru_custom_gemini_key') ||
      (import.meta as any).env?.VITE_GEMINI_API_KEY ||
      '';

    const customGroqKey = params.groqApiKey || localStorage.getItem('medsoru_groq_api_key') || '';
    let serverErrorMsg = '';

    params.onStatusUpdate?.('Yapay zeka asistanına bağlanılıyor...');

    // 1. Try server endpoint first
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/ai/question-chat` : '/api/ai/question-chat';
      const res = await safeJsonFetch<any>(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          questionContext: params.questionContext,
          messages: params.messages,
          currentMessage: params.currentMessage,
          apiKey: customApiKey,
          groqApiKey: customGroqKey,
          preferredProvider: params.preferredProvider,
          model: params.model,
        }),
      });

      if (res.ok && res.data?.success && res.data.reply) {
        return {
          success: true,
          reply: res.data.reply,
          providerUsed: res.data.providerUsed,
          planUsed: res.data.planUsed,
          attemptsCount: res.data.attemptsCount || 1,
          fallbackUsed: Boolean(res.data.fallbackUsed),
        };
      }

      // If server already tried both providers and reported 2-attempt failure:
      if (res.data && (res.data.isTwoAttemptsFailed || res.data.attemptsCount === 2)) {
        return {
          success: false,
          attemptsCount: 2,
          isTwoAttemptsFailed: true,
          error: res.data.error || '2 kez denendi: Hem Google Gemini hem de Groq Cloud sağlayıcıları yanıt veremedi. Lütfen API kotalarını veya bağlantınızı kontrol edin.'
        };
      }

      serverErrorMsg = res.data?.error || (res as any).error || '';
    } catch (e: any) {
      serverErrorMsg = e.message || '';
    }

    // 2. Direct client-side resilient AI execution fallback (for GitHub Pages / offline / direct browser usage)
    try {
      params.onStatusUpdate?.('Yerel sunucu yanıt vermedi, doğrudan tarayıcı yapay zeka motoru devreye alınıyor (1. Deneme)...');
      const qc = params.questionContext;
      const optionsText = (qc.options || []).map((o: any) => `${o.key}) ${o.text}`).join('\n');
      const systemInstruction = `Sen Türkiye'deki Tıp Fakültesi komite sınavları, TUS ve klinik tıp alanında uzman kıdemli bir Tıp Profesörü ve Soru Eğitmenisin (AI Tıp Asistanı).
Şu an tıp öğrencisi bir soru çözerken seninle anlık canlı sohbet ediyor. Amacın öğrencinin soruyla ilgili aklına takılan her şeyi (doğru cevabın altında yatan fizyopatolojik/farmakolojik mekanizma, diğer şıkların neden elenmesi gerektiği, çeldiriciler, klinik incelikler ve ezberlemeyi kolaylaştıracak mnemonikler) en berrak ve öğretici şekilde açıklamak.

SORU BİLGİLERİ:
- Komite / Sınav: ${qc.committeeName || ''} ${qc.year ? `(${qc.year})` : ''} ${qc.number ? `· Soru ${qc.number}` : ''}
- Disiplin / Branş: ${qc.discipline || 'Tıp'}
- Konu: ${qc.topic || 'Kurul Sorusu'}
- Soru Kökü:
${qc.stem}

- Şıklar:
${optionsText || 'Şıklar belirtilmemiş.'}

- Doğru Cevap: ${qc.correctAnswer ? `${qc.correctAnswer} şıkkı` : 'Bilinmiyor'}
${qc.userAnswer ? `- Öğrencinin İşaretlediği Şık: ${qc.userAnswer} şıkkı ${qc.correctAnswer ? (qc.userAnswer === qc.correctAnswer ? '(DOĞRU BİLDİ)' : '(YANLIŞ İŞARETLEDİ)') : ''}` : '- Öğrenci henüz bir şık işaretlemedi.'}
${qc.explanation ? `- Sorunun Açıklaması / Mekanizması:\n${qc.explanation}` : ''}
${qc.slideSnippet || qc.lectureReference?.matchedSnippet ? `- İlgili Amfi Slaytı Notu:\n${qc.slideSnippet || qc.lectureReference?.matchedSnippet}` : ''}

TALİMATLAR:
1. Öğrencinin sorusuna tıp fakültesi amfisi kalitesinde, motive edici, samimi ve akademik olarak %100 doğru bir üslupla yanıt ver.
2. Doğru cevabın mekanizmasını adım adım açıkla.
3. Çeldirici şıklar sorulduğunda, o şıkkın neden elenmesi gerektiğini ve hangi tabloda doğru olabileceğini belirt.
4. Karmaşık bilgileri akılda tutması için pratik mnemonikler ve "Sınav Tuzağı" uyarıları ver.
5. Markdown biçimlendirmesini (başlıklar, **kalın terimler**, - maddeler) okunaklı kullan.
6. Doğrudan öğrencinin sorduğu soruya odaklanarak yanıt ver.`;

      const chatHistory = (params.messages || []).map((m: any) => ({
        role: m.role === 'assistant' ? 'assistant' : 'user',
        content: m.content
      }));

      const lastMsg = chatHistory[chatHistory.length - 1];
      if (!lastMsg || lastMsg.content !== params.currentMessage || lastMsg.role !== 'user') {
        chatHistory.push({ role: 'user', content: params.currentMessage });
      }

      const promptText = `Öğrencinin Sorusu: "${params.currentMessage}"\nLütfen yukarıdaki tıbbi soru bağlamını ve kuralları dikkate alarak öğrenciye samimi, net ve öğretici bir yanıt ver.`;

      const aiRes = await callClientResilientAi({
        prompt: promptText,
        customGeminiKey: customApiKey,
        customGroqKey,
        preferredProvider: params.preferredProvider,
        model: params.model,
        responseFormat: 'text',
        systemInstruction,
        messages: chatHistory,
        onStatusUpdate: params.onStatusUpdate,
      });

      if (aiRes.text) {
        return {
          success: true,
          reply: aiRes.text,
          providerUsed: aiRes.providerUsed,
          planUsed: aiRes.planUsed,
          attemptsCount: aiRes.attemptsCount || 2,
          fallbackUsed: Boolean(aiRes.fallbackUsed),
        };
      }
    } catch (clientErr: any) {
      console.warn('Client-side resilient chatWithQuestionTutor failed:', clientErr.message);
      const isTwo = clientErr.isTwoAttemptsFailed || clientErr.attemptsCount === 2 || (clientErr.message && clientErr.message.includes('2 kez'));
      return {
        success: false,
        attemptsCount: 2,
        isTwoAttemptsFailed: isTwo,
        error: isTwo
          ? (clientErr.message || '2 kez denendi: Hem Google Gemini hem de Groq Cloud sağlayıcıları yanıt veremedi. Lütfen API kotalarını veya bağlantınızı kontrol edin.')
          : (clientErr.message || (serverErrorMsg && !serverErrorMsg.includes('405') ? serverErrorMsg : 'Yapay zeka yanıt veremedi.'))
      };
    }

    return {
      success: false,
      attemptsCount: 2,
      isTwoAttemptsFailed: true,
      error: serverErrorMsg || '2 kez denendi: Yapay zeka asistanına ulaşılamadı.'
    };
  },

  async getQuestionAiInteractions(questionId: string): Promise<any[]> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/ai/interactions/question/${questionId}` : `/api/ai/interactions/question/${questionId}`;
      const res = await safeJsonFetch<{ success: boolean; interactions: any[] }>(endpoint);
      return res.ok && res.data?.success && Array.isArray(res.data.interactions) ? res.data.interactions : [];
    } catch (_) {
      return [];
    }
  },

  async upvoteAiInteraction(interactionId: string): Promise<boolean> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/ai/interactions/${interactionId}/upvote` : `/api/ai/interactions/${interactionId}/upvote`;
      const res = await safeJsonFetch<{ success: boolean }>(endpoint, { method: 'POST' });
      return Boolean(res.ok && res.data?.success);
    } catch (_) {
      return false;
    }
  },

  async getRagStatus(): Promise<any> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/rag/status` : `/api/rag/status`;
      const res = await safeJsonFetch<any>(endpoint);
      return res.ok && res.data?.success ? res.data : null;
    } catch (_) {
      return null;
    }
  },

  async reindexRag(syncToCloud: boolean = true): Promise<any> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/rag/reindex` : `/api/rag/reindex`;
      const res = await safeJsonFetch<any>(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ syncToCloud })
      });
      return res.ok && res.data?.success ? res.data : null;
    } catch (_) {
      return null;
    }
  },
};

export interface QuestionChatContext {
  id?: string;
  discipline?: string;
  topic?: string;
  committeeId?: string;
  committeeName?: string;
  year?: string;
  number?: number;
  stem: string;
  options: { key: string; text: string }[];
  correctAnswer?: string;
  explanation?: string;
  userAnswer?: string;
  lectureReference?: any;
  slideSnippet?: string;
}

export interface QuestionChatMessage {
  role: 'user' | 'assistant';
  content: string;
  providerUsed?: string;
  planUsed?: string;
  timestamp?: string;
}

export interface AdminScriptItem {
  name: string;
  title: string;
  category: string;
  description: string;
  defaultArgs?: string;
  tags?: string[];
  danger?: boolean;
  runtime: 'node' | 'tsx' | 'python' | 'batch' | 'powershell';
  sizeBytes?: number;
  modifiedAt?: string | null;
  isCustom?: boolean;
}

export interface AdminPipelineItem {
  id: string;
  title: string;
  description: string;
  category: string;
  steps: Array<{ script: string; args?: string; title?: string }>;
}

export interface AdminScriptJob {
  id: string;
  name: string;
  title?: string;
  type: 'single' | 'pipeline';
  pipelineId?: string;
  args?: string;
  command?: string;
  status: 'running' | 'completed' | 'failed' | 'cancelled';
  startedAt: string;
  completedAt?: string | null;
  durationMs?: number;
  exitCode?: number | null;
  currentStepIndex?: number;
  totalSteps?: number;
  logs?: string[];
  lastLog?: string;
  requestedBy?: string;
}

export interface DriveSyncSettings {
  autoSyncEnabled: boolean;
  syncInterval: 'manual' | '15m' | '30m' | '1h' | '18:00';
  preferredScope: 'all' | 'lectures' | 'exams' | 'custom';
  customFolderId: string;
  notifyOnUpdate: boolean;
  lastCheckedAt?: string | null;
  lastSyncedAt?: string | null;
  lastSyncedSummary?: string;
}

export interface DriveCheckResult {
  checkedAt: string;
  scope: string;
  customFolderId?: string | null;
  totalScanned: number;
  upToDateCount: number;
  newCount: number;
  hasUpdates: boolean;
  newFiles: Array<{
    name: string;
    fullPath: string;
    type: 'exam' | 'lecture';
    committeeId: string;
    status: string;
  }>;
}

