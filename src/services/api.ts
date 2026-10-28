import { FIREBASE_DB_ENABLED } from './dbFlags';
import { SUSPENDED_CODE, showSuspendedNotice } from './suspensionNotice';
import { Committee, QuestionItem, MemoryFragment, ReconstructedQuestion, PastQuestionReviewRecord } from '../types';
import { FirestoreDbService, INITIAL_COMMITTEES, COMMITTEE_SORT_ORDER, filterCurrent2026_2027Committees, db } from './firestoreDb';
import { multiDbManager } from './multiDbManager';
import { SupabaseDbService, getSupabaseClient } from './supabaseDb';
import { pastQuestionsCache } from './pastQuestionsCache';
import { offlineDatabaseService } from './offlineDatabaseService';
import { collection, addDoc } from 'firebase/firestore';
import { ADMIN_EMAIL, getLocalAdminSession } from './auth';
import { attachModeratorToken, isModeratorMode } from './moderatorSession';
import { defaultApiBaseForThisHost, panelApiBase, PANEL_ON_ORACLE_AT_BOOT } from '../config/deployment';
import { clientCache } from './clientCache';
import {
  clusterDraftsForCommittee,
  mergeDrafts,
  unmergeQuestion,
  findRealtimeMatchingDraft,
  ClusterAnalysisSummary,
  ClusterTuning
} from './draftClusteringService';

export const STORAGE_KEY = 'medsoru_db_data_v1';
const API_BASE_URL_KEY = 'medsoru_custom_api_url';

export const getCustomApiUrl = (path?: string): string => {
  const url = (typeof localStorage !== 'undefined' ? localStorage.getItem(API_BASE_URL_KEY) : '') || '';
  if (url && (url.includes('github.io') || url.includes('github.com'))) {
    try { localStorage.removeItem(API_BASE_URL_KEY); } catch (_) {}
    return '';
  }
  if (url) return url;
  // Yerel yönetim paneli canlı sitedeki panel gibi Oracle'a bağlanır (cihaza özel bölümler hariç)
  const panel = panelApiBase(path);
  if (panel) return panel;
  // Canlı hostta özel URL yoksa Oracle Named Tunnel'a düş (cihazda localhost → '').
  try {
    return defaultApiBaseForThisHost();
  } catch (_) {
    return '';
  }
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
  let sentHeaders: Headers | null = null;
  let sentTimeoutMs = 30000;
  try {
    let resolvedInput = input;
    if (typeof input === 'string' && input.startsWith('/')) {
      const customUrl = getCustomApiUrl(input);
      if (customUrl) {
        resolvedInput = `${customUrl.replace(/\/$/, '')}${input}`;
      }
    }
    const isAiOrLongRequest = typeof resolvedInput === 'string' && (
      resolvedInput.includes('/ai/') ||
      resolvedInput.includes('/rag/') ||
      resolvedInput.includes('reconstruct') ||
      resolvedInput.includes('optimize') ||
      resolvedInput.includes('/past-question-reviews') ||
      resolvedInput.includes('/audit/') ||
      resolvedInput.includes('/master/')
    );
    const timeoutMs = isAiOrLongRequest ? 60000 : 30000;
    const hasSignal = init?.signal;
    const method = (init?.method || 'GET').toUpperCase();
    const headers = new Headers(init?.headers);
    // Yerel panel → Oracle: orada loopback yöneticisi yok; okuma isteklerinde de yönetici başlığı gider
    if (PANEL_ON_ORACLE_AT_BOOT && typeof resolvedInput === 'string' && !resolvedInput.startsWith('/') && !headers.get('x-admin-email')) {
      headers.set('x-admin-email', ADMIN_EMAIL);
    }
    if (!['GET', 'HEAD', 'OPTIONS'].includes(method) && typeof window !== 'undefined') {
      const adminHeader = headers.get('x-admin-email');
      const localAdmin = getLocalAdminSession();
      const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      const isAdmin = Boolean(
        (adminHeader && adminHeader.toLowerCase() === ADMIN_EMAIL.toLowerCase()) ||
        (localAdmin && localAdmin.email?.toLowerCase() === ADMIN_EMAIL.toLowerCase()) ||
        isLocalhost
      );

      let password = sessionStorage.getItem('medsoru_api_write_password') || '';
      if (!password && isAdmin) {
        // Admin kullanıcı veya yerel geliştirme için şifre sormadan otomatik geçiş sağla
        password = '12345678';
        sessionStorage.setItem('medsoru_api_write_password', password);
      }
      // Eskiden parola yoksa her yazmada window.prompt açılıyordu: sayfayı donduran, iptal edilince her
      // tıklamada yeniden çıkan bir pencere. Artık sorulmaz; sunucu parola isterse 401 yanıtı arayüzde gösterilir
      // (parola gerekiyorsa sessionStorage 'medsoru_api_write_password' anahtarına yazılır).
      if (password) headers.set('X-API-Password', password);
      if (isAdmin && !headers.get('x-admin-email')) {
        headers.set('x-admin-email', ADMIN_EMAIL);
      }
    }
    const resolvedUrlString = typeof resolvedInput === 'string' ? resolvedInput : String(resolvedInput);
    await attachModeratorToken(resolvedUrlString, headers);
    const storedEtagEntry = method === 'GET' ? clientCache.getStoredETag(resolvedUrlString) : null;
    if (storedEtagEntry?.etag && !headers.has('If-None-Match')) {
      headers.set('If-None-Match', storedEtagEntry.etag);
    }

    const fetchOptions: RequestInit = {
      ...init,
      headers,
      signal: hasSignal || (typeof AbortSignal !== 'undefined' && 'timeout' in AbortSignal ? AbortSignal.timeout(timeoutMs) : undefined),
    };
    sentHeaders = headers;
    sentTimeoutMs = timeoutMs;
    const res = await fetch(resolvedInput, fetchOptions);

    // HTTP 304 Not Modified: Sunucuda veri değişmemiş, yerel önbellekteki veriyi anında döndür (0 bayt aktarım)
    if (res.status === 304 && storedEtagEntry?.cachedResponse) {
      return { ok: true, status: 200, data: storedEtagEntry.cachedResponse as T };
    }

    const contentType = res.headers.get('content-type') || '';
    if (!res.ok) {
      let errMsg = `HTTP ${res.status}`;
      if (contentType.includes('application/json')) {
        try {
          const errObj = await res.json();
          errMsg = errObj.error || errObj.hata || errObj.message || errMsg;
          if (res.status === 403 && errObj?.code === SUSPENDED_CODE) showSuspendedNotice(errObj);
        } catch (_) {}
      } else if (res.status === 405) {
        errMsg = 'Statik barındırma ortamı (HTTP 405 Method Not Allowed). İstemci modu veya yedek veritabanı devreye alınıyor.';
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
    const responseEtag = res.headers.get('ETag') || res.headers.get('etag');
    if (method === 'GET' && responseEtag) {
      clientCache.setStoredETag(resolvedUrlString, responseEtag, data);
    }
    return { ok: true, status: res.status, data };
  } catch (err: any) {
    // Ağ düzeyinde hata + kayıtlı özel API adresi varsa: adres bayatlamış olabilir
    // (eski tünel/DNS). Varsayılan adres farklıysa bir kez oradan dene; tutarsa bayat kaydı sil.
    try {
      if (
        (typeof navigator === 'undefined' || navigator.onLine) &&
        typeof input === 'string' &&
        input.startsWith('/') &&
        typeof localStorage !== 'undefined'
      ) {
        const stored = (localStorage.getItem(API_BASE_URL_KEY) || '').trim().replace(/\/$/, '');
        let def = '';
        try { def = defaultApiBaseForThisHost().replace(/\/$/, ''); } catch { def = ''; }
        if (stored && def && stored.replace(/\/$/, '') !== def) {
          const retryInit: RequestInit = {
            ...init,
            headers: sentHeaders || new Headers(init?.headers),
            signal: typeof AbortSignal !== 'undefined' && 'timeout' in AbortSignal ? AbortSignal.timeout(sentTimeoutMs) : undefined,
          };
          const retry = await fetch(`${def}${input}`, retryInit);
          const ct = retry.headers.get('content-type') || '';
          if (retry.ok && ct.includes('application/json')) {
            try { localStorage.removeItem(API_BASE_URL_KEY); } catch (_) {}
            return { ok: true, status: retry.status, data: await retry.json() as T };
          }
        }
      }
    } catch (_) {}
    const isTimeout = err.name === 'AbortError' || err.name === 'TimeoutError';
    const isOffline = typeof navigator !== 'undefined' && !navigator.onLine;
    const errMsg = isOffline
      ? 'Çevrimdışı mod: Cihazınızda internet bağlantısı yok.'
      : isTimeout
        ? 'Sunucu yanıt zaman aşımına uğradı. İstemci yapay zeka motoru devreye alınıyor...'
        : (err.message || 'Bağlantı hatası');
    return { ok: false, status: 0, error: errMsg };
  }
}

let isServerAvailable: boolean | null = null;
if (typeof window !== 'undefined') {
  window.addEventListener('online', () => { isServerAvailable = null; });
  window.addEventListener('offline', () => { isServerAvailable = false; });
}

async function checkServer(): Promise<boolean> {
  if (typeof navigator !== 'undefined' && !navigator.onLine) return false;
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

/** Serbest metin girdisinin öğrenciye dönen ayrıştırma özeti (GET /api/question-intake/:id) */
export interface QuestionIntakeSummary {
  id: string;
  status: 'bekliyor' | 'isleniyor' | 'ayristirildi' | 'icerik_yok' | 'kota_bekliyor' | 'hata';
  nextTryAt?: string;
  units: {
    ders: string;
    konu: string | null;
    soruNo: number | null;
    odak: string | null;
    bulgular: string[];
    siklar: { harf: string | null; metin: string }[];
    cevap: { harf: string | null; metin: string } | null;
    olumsuzKok: number;
    eksikler: string[];
  }[];
}


export interface SourceRefLite {
  documentId: string;
  documentType: string;
  title: string;
  discipline?: string;
  pageNumber?: number;
  snippet: string;
}

/** POST /api/recall/match yanıtı (src/services/poolClusterService.ts → matchText). */
export interface RecallMatchResult {
  engine: string;
  noise: boolean;
  clean: string;
  ders: { name: string; p: number }[];
  konu: { name: string; p: number } | null;
  terms: string[];
  claimedLetter: string | null;
  claimedText: string | null;
  number: number | null;
  negative: boolean;
  corrections: [string, string][];
  /** `question`: kaydın hafif kopyası (istemcide havuz yüklü değilse gösterim için) */
  matches: { questionId: string; prob: number; question?: QuestionItem }[];
}

export interface SimilarPastQuestion {
  id: string;
  title: string;
  discipline?: string;
  committeeId?: string;
  examYear?: string;
  claimedAnswer?: string;
  stem: string;
  score?: number;
  /** Çıkmış sorunun şıkları (chunk içinden ayrıştırılır) */
  options?: { key: string; text: string }[];
}

// AI calls are proxied through the backend (/api/ai/generate). Provider keys live only in the
// server .env; the browser sends at most the user's own key saved in Settings.
export async function callClientResilientAi(options: {
  prompt: string;
  customGeminiKey?: string;
  customGroqKey?: string;
  customMuseSparkKey?: string;
  museSparkBaseUrl?: string;
  preferredProvider?: 'gemini' | 'groq' | 'muse-spark' | 'auto';
  model?: string;
  responseFormat?: 'json' | 'text';
  systemInstruction?: string;
  messages?: { role: string; content: string }[];
  onStatusUpdate?: (status: string) => void;
}): Promise<{ text: string; providerUsed: string; planUsed: string; attemptsCount: number; fallbackUsed?: boolean }> {
  const { onStatusUpdate, customGroqKey, customMuseSparkKey, ...rest } = options;
  const stored = (k: string) => (typeof localStorage !== 'undefined' ? localStorage.getItem(k) : '') || undefined;
  const groqKey = customGroqKey || stored('medsoru_groq_api_key');
  const museKey = customMuseSparkKey || stored('medsoru_muse_spark_api_key');

  onStatusUpdate?.('Yapay zeka sunucusuna bağlanılıyor...');
  const res = await safeJsonFetch<any>('/api/ai/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...rest, customGroqKey: groqKey, customMuseSparkKey: museKey }),
  });

  if (!res.ok || !res.data?.success) {
    const failureError: any = new Error(
      res.data?.error || res.error || 'Yapay zeka sunucusuna ulaşılamadı. Yerel sunucunun (server.ts) çalıştığından emin olun.'
    );
    failureError.attemptsCount = res.data?.attemptsCount;
    failureError.isTwoAttemptsFailed = res.data?.isTwoAttemptsFailed;
    failureError.primaryError = res.data?.primaryError;
    failureError.secondaryError = res.data?.secondaryError;
    throw failureError;
  }

  const { text, providerUsed, planUsed, attemptsCount, fallbackUsed } = res.data;
  return { text, providerUsed, planUsed, attemptsCount, fallbackUsed };
}

export interface AnswerVotes { counts: Record<string, number>; total: number; myVote: string | null }
/** Anketi açık sorular: ids = cevabı belirsiz; resolved = cevabı kabul edilmiş ama anketi açık tutulan. */
export interface AnswerDoubtfulInfo {
  ids: string[];
  options: Record<string, Record<string, string>>;
  resolved: Record<string, { answer: string; by: string }>;
}

/** Faz 14 ayarları (/test/cikmis): Lite yedeği, otomatik ücretsiz inceleme, yetkili kontrol modeli */
export type Phase14Settings = { lite_kullan: boolean; otomatik_ucretsiz: boolean; otomatik_limit: number; kontrol_modeli?: string };

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
    targetQuestionId?: string;
    examYear?: string;
  }): Promise<QuestionItem> {
    const db = getLocalDb();
    // Sınav yılı yalnız boşsa yazılır (önceki katkıların yılı ezilmez)
    const withYear = <T extends { examYear?: string }>(q: T): T => {
      if (data.examYear && !q.examYear) q.examYear = data.examYear;
      return q;
    };
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
          upvotes: 0,
        }
      : null;

    // Doğrudan belirli bir soruya bağlama
    if (data.targetQuestionId) {
      const explicitTarget = db.questions.find((q) => q.id === data.targetQuestionId);
      if (explicitTarget) {
        if (initialFragment) {
          explicitTarget.fragments = explicitTarget.fragments || [];
          explicitTarget.fragments.push(initialFragment);
        }
        if (data.options && data.options.length > 0) {
          explicitTarget.options = explicitTarget.options || [];
          data.options.forEach((o) => {
            if (!o.text || !o.text.trim()) return;
            explicitTarget.fragments.push({
              id: `f-opt-${Date.now()}-${o.key}`,
              author: data.author || 'Anonim',
              authorUid: data.authorUid,
              authorStudentNumber: data.authorStudentNumber,
              text: `${o.key}) ${o.text.trim()}`,
              type: 'option',
              timestamp: new Date().toISOString(),
              upvotes: 0,
            });
            const exOpt = explicitTarget.options.find((opt) => opt.key === o.key);
            if (exOpt) {
              exOpt.upvotes = (exOpt.upvotes || 1) + 1;
            } else {
              explicitTarget.options.push({
                key: o.key,
                text: o.text.trim(),
                suggestedBy: data.author || 'Anonim',
                suggestedByUid: data.authorUid,
                upvotes: 0,
              });
            }
          });
          explicitTarget.options.sort((a, b) => a.key.localeCompare(b.key));
        }
        explicitTarget.status = 'gathering';
        explicitTarget.updatedAt = new Date().toISOString();
        withYear(explicitTarget);
        saveLocalDb(db);
        try {
          await multiDbManager.saveQuestion(explicitTarget);
        } catch (_) {}
        return explicitTarget;
      }
    }

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
              upvotes: 0,
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
                upvotes: 0,
              });
            }
          });
          existing.options.sort((a, b) => a.key.localeCompare(b.key));
        }
        existing.status = 'gathering';
        existing.updatedAt = new Date().toISOString();
        withYear(existing);
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
                upvotes: 0,
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
            options: data.options ? data.options.map(o => ({ key: o.key, text: o.text, upvotes: 0 })) : [],
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
              upvotes: 0,
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
          existing!.options = existing!.options || [];
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
              upvotes: 0,
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
                upvotes: 0,
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
                  upvotes: 0,
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
              options: data.options ? data.options.map(o => ({ key: o.key, text: o.text, upvotes: 0 })) : [],
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
                upvotes: 0,
              });
            }
          });
        }

        db.questions.push(targetQuestion);
      }
    }

    withYear(targetQuestion);
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
      options: data.options ? data.options.map(o => ({ key: o.key, text: o.text, upvotes: 0 })) : [...q.options],
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
          upvotes: 0,
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
          <h2 style="margin: 0; font-size: 20px; font-weight: 700;">MeDSor • Tıp Dönem 3 Kurul Arşivi</h2>
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
            <p style="margin: 0;">MeDSor Kurul Sistemi • nofrostlife@gmail.com</p>
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

  /** Ders materyali / çıkmış soru kaynakları (yalnız arama, AI yok). */
  async findSourcesForFragment(text: string, committeeId?: string, discipline?: string): Promise<SourceRefLite[]> {
    const res = await safeJsonFetch<{ sources: SourceRefLite[] }>('/api/sources/for-fragment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, committeeId, discipline }),
    });
    return res.ok ? res.data?.sources || [] : [];
  },

  /** Past exam questions resembling what a student remembers (retrieval only, no AI cost). */
  /** "Bunu mu kastettiniz?" — derlem sözlüğüne göre yazım önerisi */
  async suggestSpelling(text: string, signal?: AbortSignal): Promise<{ text: string | null; changes: { from: string; to: string }[] } | null> {
    const res = await safeJsonFetch<{ success: boolean; text: string | null; changes: { from: string; to: string }[] }>(
      `/api/search/spell?q=${encodeURIComponent(text)}`,
      { signal }
    );
    return res.ok && res.data?.success ? { text: res.data.text, changes: res.data.changes } : null;
  },

  /** Serbest metin girdisini ham kayıt olarak gönderir; sunucu arka planda ücretsiz Gemini ile ayrıştırır. */
  async submitQuestionIntake(data: {
    rawText: string;
    committeeId: string;
    questionNumber?: number;
    discipline?: string;
    questionId?: string;
    uid?: string;
    author?: string;
    source: string;
    options?: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[];
    claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E';
  }): Promise<string | null> {
    const res = await safeJsonFetch<{ id: string }>('/api/question-intake', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.ok ? res.data?.id || null : null;
  },

  async getQuestionIntake(id: string): Promise<QuestionIntakeSummary | null> {
    const res = await safeJsonFetch<QuestionIntakeSummary>(`/api/question-intake/${encodeURIComponent(id)}`, {
      method: 'GET',
      headers: { Accept: 'application/json' },
    });
    return res.ok ? res.data || null : null;
  },

  /** Soru ekle: hatırlamayı sunucudaki motorla analiz et + havuzda aynı soruyu anlatan kayıtlar (POST /api/recall/match). */
  async recallMatch(input: { text: string; committeeId: string; discipline?: string; options?: { key: string; text: string }[]; questionNumber?: number; limit?: number }, signal?: AbortSignal): Promise<RecallMatchResult | null> {
    const res = await safeJsonFetch<RecallMatchResult>('/api/recall/match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
      signal,
    });
    return res.ok ? res.data || null : null;
  },

  /** Öğrencinin öneri kararı (öğrenme verisi): "ayni" bağladı/birleştirdi, "farkli" reddetti. Hata sessizce yutulur. */
  recallFeedback(input: { text: string; committeeId: string; questionId: string; decision: 'ayni' | 'farkli'; prob?: number }): void {
    void safeJsonFetch('/api/recall/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    }).catch(() => {});
  },

  async findSimilarPastQuestions(text: string, committeeId?: string): Promise<SimilarPastQuestion[]> {
    const res = await safeJsonFetch<{ results: SimilarPastQuestion[] }>('/api/past-questions/similar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, committeeId, limit: 7 }),
    });
    return res.ok ? res.data?.results || [] : [];
  },

  async reconstructWithAi(questionId: string): Promise<QuestionItem> {
    const db = getLocalDb();
    let q = db.questions.find((item) => item.id === questionId);
    if (!q) {
      try {
        q = (await multiDbManager.getPastQuestions()).find((x) => x.id === questionId);
      } catch {}
    }

    const customApiKey = localStorage.getItem('medsoru_gemini_api_key') || localStorage.getItem('medsoru_custom_gemini_key') || '';
    const customGroqKey = localStorage.getItem('medsoru_groq_api_key') || '';

    // Server grounds the reconstruction on course material (RAG) and runs the AI.
    // The question is sent along because it may only exist in Firebase/Supabase.
    const res = await safeJsonFetch<{ reconstruction: ReconstructedQuestion; question: QuestionItem; error?: string }>(
      `/api/questions/${questionId}/ai-reconstruct`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: q,
          apiKey: customApiKey || undefined,
          groqApiKey: customGroqKey || undefined,
        }),
      }
    );

    if (!res.ok || !res.data?.reconstruction) {
      throw new Error(res.data?.error || res.error || 'Yapay zeka rekonstrüksiyonu gerçekleştirilemedi.');
    }

    const updated: QuestionItem = {
      ...(q || res.data.question),
      reconstruction: res.data.reconstruction,
      status: 'completed',
      claimedAnswer: res.data.reconstruction.correctAnswer,
      updatedAt: new Date().toISOString(),
    };
    await multiDbManager.saveQuestion(updated);
    const idx = db.questions.findIndex((item) => item.id === questionId);
    if (idx !== -1) db.questions[idx] = updated;
    else db.questions.push(updated);
    saveLocalDb(db);
    return updated;
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

    const r = await safeJsonFetch(`/api/questions/${encodeURIComponent(id)}`, {
      method: 'DELETE',
      headers: user?.email ? { 'x-admin-email': user.email } : {},
    });
    // Yönetici silmesinde sunucu hatası gizlenmez (404 = zaten yok)
    const byAdmin = Boolean(user?.email && user.email.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase());
    if (!r.ok && r.status !== 404 && byAdmin) throw new Error((r.data as any)?.error || r.error || 'Sunucu soruyu silemedi');
    if (!r.ok && !byAdmin) console.warn('[ApiService] deleteQuestion server error', r.status, r.error);
  },

  async mergeDraftCluster(
    adminEmail: string,
    anchorId: string,
    satelliteIds: string[],
    adminName: string = 'Yönetici'
  ): Promise<QuestionItem> {
    const isAuth = !adminEmail || adminEmail.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase() || isModeratorMode();
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

    // Asıl kaynak sunucu: önce oraya yaz (hata gerçek mesajla gösterilir), sonra yerel kopya.
    // Sunucu çapayı kaydeder, uyduları siler; meds-pg tetikleyicisi diğer sekmelere SSE ile yayar.
    const r = await safeJsonFetch(`/api/admin/drafts/merge`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail || ADMIN_EMAIL },
      body: JSON.stringify({ consolidated, mergedIds }),
    });
    if (!r.ok) throw new Error((r.data as any)?.error || r.error || `Sunucu birleştirmeyi kaydedemedi (HTTP ${r.status}).`);

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

    // İstemci önbellekleri (IndexedDB vb.) — sunucu zaten yazdı, burada hata yalnız uyarı
    try {
      await multiDbManager.saveQuestion(consolidated);
      for (const satId of mergedIds) {
        await multiDbManager.deleteQuestion(satId);
      }
    } catch (e) {
      console.warn('Draft merge cloud sync warning:', e);
    }
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('medsoru:questions-changed', { detail: { eventType: 'MERGE', id: consolidated.id, removed: mergedIds } }));
    }

    return consolidated;
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
      // Statik/çevrimdışı ortam yedeği
    }
    // MultiDbManager with automatic Supabase failover
    try {
      const notes = await multiDbManager.getLectureNotes();
      if (notes && notes.length > 0) return notes;
    } catch (e) {}
    return [];
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

  // Past Exam Questions (Çıkmış Sorular) - Ultra-Hızlı ve Ekonomik Cihaz Depolaması
  async getPastQuestions(params: { committeeId?: string; discipline?: string; year?: string; query?: string; includeAmbiguous?: boolean } = {}): Promise<any[]> {
    let list: any[] = [];

    // 0. Ultra-Hızlı Cihaz Hafızası (IndexedDB < 20ms - Sıfır Veritabanı Maliyeti)
    try {
      const cached = await pastQuestionsCache.getCachedQuestions();
      if (cached && cached.length > 0) {
        list = cached;
        // Arka planda soru bazında artıksal senkronizasyonu tarayıcı boştayken çalıştır (0 UI bloklama)
        if (typeof window !== 'undefined') {
          if ('requestIdleCallback' in window) {
            (window as any).requestIdleCallback(() => pastQuestionsCache.syncWithRemote().catch(() => {}), { timeout: 8000 });
          } else {
            setTimeout(() => pastQuestionsCache.syncWithRemote().catch(() => {}), 4000);
          }
        }
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
        const apiBase = getCustomApiUrl() || '';
        const res = await fetch(`${apiBase}/api/past-exams`);
        if (res.ok) {
          const json = await res.json();
          if (json.questions && Array.isArray(json.questions)) {
            list = json.questions;
            const full = list;
            pastQuestionsCache.saveBatch(full).then(() => {
              let maxTime = new Date(0).toISOString();
              for (const q of full) if (q.updatedAt && q.updatedAt > maxTime) maxTime = q.updatedAt;
              return pastQuestionsCache.setLastSyncTime(maxTime, full.length);
            }).catch(() => {});
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

  async commentPastQuestion(
    questionId: string,
    author: string,
    text: string,
    userMeta?: { uid?: string; email?: string; ownershipToken?: string; parentId?: string }
  ): Promise<any> {
    const apiBase = getCustomApiUrl() || '';
    
    // 1. Try local server
    try {
      const res = await fetch(`${apiBase}/api/past-exams/${encodeURIComponent(questionId)}/comment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          author,
          text,
          authorUid: userMeta?.uid,
          authorEmail: userMeta?.email,
          ownershipToken: userMeta?.ownershipToken,
          parentId: userMeta?.parentId,
        }),
      });
      if (res.ok) {
        return await res.json();
      }
      // Sunucu yanıt verdi ama reddetti (429, 413, 404…): yedeğe düşmeden hatayı göster —
      // eskiden 401 sessizce Firestore'a/yerel sahte kayda düşüyor, yorum kayboluyordu.
      const body = await res.json().catch(() => null);
      throw Object.assign(new Error(body?.error || `HTTP ${res.status}`), { serverRejected: true });
    } catch (e: any) {
      if (e?.serverRejected) throw e;
      console.warn('[commentPastQuestion] Server çağrısı başarısız, Firestore yedeğine geçiliyor:', e);
    }

    // 2. Direct Firestore fallback (sunucuya ulaşılamazsa)
    try {
      const commentObj = {
        id: `c-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
        author: author || 'Tıp Öğrencisi',
        authorUid: userMeta?.uid,
        authorEmail: userMeta?.email,
        ownershipToken: userMeta?.ownershipToken,
        ...(userMeta?.parentId ? { parentId: userMeta.parentId } : {}),
        text: text.trim(),
        createdAt: new Date().toISOString(),
        upvotes: 0
      };
      if (!FIREBASE_DB_ENABLED) throw new Error('Firebase veritabanı devre dışı');
      await addDoc(collection(db, 'past_question_comments'), {
        ...commentObj,
        questionId
      });
      return { success: true, comment: commentObj };
    } catch (err: any) {
      console.warn('[commentPastQuestion] Firestore kaydı da yapılamadı:', err.message);
      throw new Error('Sunucuya ulaşılamadı; yorum gönderilemedi. Bağlantını kontrol edip yeniden dene.');
    }
  },

  async editPastComment(
    questionId: string,
    commentId: string,
    text: string,
    userAuth?: { uid?: string; email?: string; author?: string; ownershipToken?: string; adminEmail?: string }
  ): Promise<{ success: boolean; message?: string; comment?: any }> {
    const apiBase = getCustomApiUrl() || '';
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (userAuth?.adminEmail) headers['x-admin-email'] = userAuth.adminEmail;
    if (userAuth?.uid) headers['x-user-uid'] = userAuth.uid;
    if (userAuth?.email) headers['x-user-email'] = userAuth.email;
    if (userAuth?.author) headers['x-user-name'] = userAuth.author;
    if (userAuth?.ownershipToken) headers['x-ownership-token'] = userAuth.ownershipToken;

    try {
      const res = await fetch(`${apiBase}/api/past-exams/${encodeURIComponent(questionId)}/comments/${encodeURIComponent(commentId)}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify({
          text,
          authorUid: userAuth?.uid,
          authorEmail: userAuth?.email,
          author: userAuth?.author,
          ownershipToken: userAuth?.ownershipToken,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        // Bulutta da güncelle
        await SupabaseDbService.updatePastQuestionComment(questionId, commentId, text).catch(() => {});
        return { success: true, message: data.message || 'Yorum güncellendi.', comment: data.comment };
      }
      const errData = await res.json().catch(() => ({}));
      return { success: false, message: errData.error || 'Yorum güncellenemedi.' };
    } catch (e: any) {
      // Fallback doğrudan Supabase
      const sbRes = await SupabaseDbService.updatePastQuestionComment(questionId, commentId, text);
      return { success: sbRes.success, message: sbRes.success ? 'Yorum güncellendi.' : (sbRes.error || e.message) };
    }
  },

  async deletePastComment(
    questionId: string,
    commentId: string,
    userAuth?: { uid?: string; email?: string; author?: string; ownershipToken?: string; adminEmail?: string }
  ): Promise<{ success: boolean; message?: string }> {
    const apiBase = getCustomApiUrl() || '';
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (userAuth?.adminEmail) headers['x-admin-email'] = userAuth.adminEmail;
    if (userAuth?.uid) headers['x-user-uid'] = userAuth.uid;
    if (userAuth?.email) headers['x-user-email'] = userAuth.email;
    if (userAuth?.author) headers['x-user-name'] = userAuth.author;
    if (userAuth?.ownershipToken) headers['x-ownership-token'] = userAuth.ownershipToken;

    try {
      const res = await fetch(`${apiBase}/api/past-exams/${encodeURIComponent(questionId)}/comments/${encodeURIComponent(commentId)}`, {
        method: 'DELETE',
        headers,
        body: JSON.stringify({
          authorUid: userAuth?.uid,
          authorEmail: userAuth?.email,
          author: userAuth?.author,
          ownershipToken: userAuth?.ownershipToken,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        // Supabase doğrudan silme
        await SupabaseDbService.deletePastQuestionComment(questionId, commentId).catch(() => {});
        return { success: true, message: data.message || 'Yorum silindi.' };
      }
      const errData = await res.json().catch(() => ({}));
      return { success: false, message: errData.error || 'Yorum silinemedi.' };
    } catch (e: any) {
      const sbRes = await SupabaseDbService.deletePastQuestionComment(questionId, commentId);
      return { success: sbRes.success, message: sbRes.success ? 'Yorum silindi.' : (sbRes.error || e.message) };
    }
  },

  async reportPastQuestion(questionId: string, reason: string, details?: string, reportedBy?: string, reporter?: { email?: string | null; uid?: string | null; ownershipToken?: string }): Promise<any> {
    const apiBase = getCustomApiUrl() || '';
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
          reportedBy: reportObj.reportedBy,
          reporterEmail: reporter?.email || undefined,
          reporterUid: reporter?.uid || undefined,
          ownershipToken: reporter?.ownershipToken || undefined,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data?.report) {
          reportObj.id = data.report.id || reportObj.id;
        }
        if (data?.queue) (reportObj as any).queue = data.queue;
      }
    } catch (e) {
      console.warn('[reportPastQuestion] Server çağrısı başarısız, doğrudan buluta geçiliyor:', e);
    }

    // 2. Direct Supabase save (sunucuya ulaşılamazsa Supabase'e yazar)
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

    // Çevrimdışıysa kuyruğa al
    if (typeof navigator !== 'undefined' && !navigator.onLine) {
      offlineDatabaseService.queueAction({
        type: 'report',
        endpoint: `/api/past-exams/${encodeURIComponent(questionId)}/report`,
        method: 'POST',
        payload: {
          id: reportObj.id,
          reason: reportObj.reason,
          details: reportObj.details,
          reportedBy: reportObj.reportedBy,
          reporterEmail: reporter?.email || undefined,
          reporterUid: reporter?.uid || undefined,
          ownershipToken: reporter?.ownershipToken || undefined,
        },
      }).catch(() => {});
    }

    // 4. Firestore Dual Cloud Fallback (Firebase Spark/Cloud kesintisiz yedek)
    if (FIREBASE_DB_ENABLED) try {
      await addDoc(collection(db, 'past_question_reports'), reportObj);
    } catch (err: any) {
      console.warn('[reportPastQuestion] Firestore kaydı yapılamadı:', err.message);
    }

    return { success: true, report: reportObj };
  },

  async editPastReport(
    questionId: string,
    reportId: string,
    updates: { reason: string; details?: string },
    userAuth?: { uid?: string; email?: string; reportedBy?: string; ownershipToken?: string; adminEmail?: string }
  ): Promise<{ success: boolean; message?: string; report?: any }> {
    const apiBase = getCustomApiUrl() || '';
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (userAuth?.adminEmail) headers['x-admin-email'] = userAuth.adminEmail;
    if (userAuth?.uid) headers['x-user-uid'] = userAuth.uid;
    if (userAuth?.email) headers['x-user-email'] = userAuth.email;
    if (userAuth?.reportedBy) headers['x-user-name'] = userAuth.reportedBy;
    if (userAuth?.ownershipToken) headers['x-ownership-token'] = userAuth.ownershipToken;

    const url = questionId 
      ? `${apiBase}/api/past-exams/${encodeURIComponent(questionId)}/reports/${encodeURIComponent(reportId)}`
      : `${apiBase}/api/reports/${encodeURIComponent(reportId)}`;

    try {
      const res = await fetch(url, {
        method: 'PUT',
        headers,
        body: JSON.stringify({
          reason: updates.reason,
          details: updates.details,
          reporterUid: userAuth?.uid,
          reporterEmail: userAuth?.email,
          reportedBy: userAuth?.reportedBy,
          ownershipToken: userAuth?.ownershipToken,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        if (questionId) {
          await SupabaseDbService.updatePastQuestionReport(questionId, reportId, updates).catch(() => {});
        }
        return { success: true, message: data.message || 'Bildirim güncellendi.', report: data.report };
      }
      const errData = await res.json().catch(() => ({}));
      return { success: false, message: errData.error || 'Bildirim güncellenemedi.' };
    } catch (e: any) {
      if (questionId) {
        const sbRes = await SupabaseDbService.updatePastQuestionReport(questionId, reportId, updates);
        return { success: sbRes.success, message: sbRes.success ? 'Bildirim güncellendi.' : (sbRes.error || e.message) };
      }
      return { success: false, message: e.message || 'Bağlantı hatası' };
    }
  },

  async deletePastReport(
    questionId: string,
    reportId: string,
    userAuth?: { uid?: string; email?: string; reportedBy?: string; ownershipToken?: string; adminEmail?: string }
  ): Promise<{ success: boolean; message?: string }> {
    const apiBase = getCustomApiUrl() || '';
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (userAuth?.adminEmail) headers['x-admin-email'] = userAuth.adminEmail;
    if (userAuth?.uid) headers['x-user-uid'] = userAuth.uid;
    if (userAuth?.email) headers['x-user-email'] = userAuth.email;
    if (userAuth?.reportedBy) headers['x-user-name'] = userAuth.reportedBy;
    if (userAuth?.ownershipToken) headers['x-ownership-token'] = userAuth.ownershipToken;

    const url = questionId 
      ? `${apiBase}/api/past-exams/${encodeURIComponent(questionId)}/reports/${encodeURIComponent(reportId)}`
      : `${apiBase}/api/reports/${encodeURIComponent(reportId)}`;

    try {
      const res = await fetch(url, {
        method: 'DELETE',
        headers,
        body: JSON.stringify({
          reporterUid: userAuth?.uid,
          reporterEmail: userAuth?.email,
          reportedBy: userAuth?.reportedBy,
          ownershipToken: userAuth?.ownershipToken,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        if (questionId) {
          await SupabaseDbService.deletePastQuestionReport(questionId, reportId).catch(() => {});
        }
        return { success: true, message: data.message || 'Bildirim kalıcı olarak silindi.' };
      }
      const errData = await res.json().catch(() => ({}));
      return { success: false, message: errData.error || 'Bildirim silinemedi.' };
    } catch (e: any) {
      if (questionId) {
        const sbRes = await SupabaseDbService.deletePastQuestionReport(questionId, reportId);
        return { success: sbRes.success, message: sbRes.success ? 'Bildirim kalıcı olarak silindi.' : (sbRes.error || e.message) };
      }
      return { success: false, message: e.message || 'Bağlantı hatası' };
    }
  },


  async upvotePastQuestion(questionId: string, userId?: string): Promise<{ success: boolean; upvotes: number; downvotes: number; likedBy?: string[]; dislikedBy?: string[] }> {
    try {
      const res = await fetch(`/api/past-exams/${encodeURIComponent(questionId)}/upvote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId }),
      });
      if (res.ok) {
        const data = await res.json();
        return {
          success: true,
          upvotes: data.upvotes || 0,
          downvotes: data.downvotes || 0,
          likedBy: data.likedBy,
          dislikedBy: data.dislikedBy,
        };
      }
    } catch (e) {}

    // Çevrimdışı Mod Fallback: Eylemi arka plan kuyruğuna al ve yerel hafızada uygula
    offlineDatabaseService.queueAction({
      type: 'vote',
      endpoint: `/api/past-exams/${encodeURIComponent(questionId)}/upvote`,
      method: 'POST',
      payload: { userId },
    }).catch(() => {});

    try {
      const q = await pastQuestionsCache.getCachedQuestionById(questionId);
      if (q) {
        q.upvotes = (q.upvotes || 0) + 1;
        await pastQuestionsCache.saveQuestion(q);
        return { success: true, upvotes: q.upvotes, downvotes: (q as any).downvotes || 0 };
      }
    } catch (_) {}

    return { success: true, upvotes: 1, downvotes: 0 };
  },

  async downvotePastQuestion(questionId: string, userId?: string): Promise<{ success: boolean; upvotes: number; downvotes: number; likedBy?: string[]; dislikedBy?: string[] }> {
    try {
      const res = await fetch(`/api/past-exams/${encodeURIComponent(questionId)}/downvote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId }),
      });
      if (res.ok) {
        const data = await res.json();
        return {
          success: true,
          upvotes: data.upvotes || 0,
          downvotes: data.downvotes || 0,
          likedBy: data.likedBy,
          dislikedBy: data.dislikedBy,
        };
      }
    } catch (e) {}

    offlineDatabaseService.queueAction({
      type: 'vote',
      endpoint: `/api/past-exams/${encodeURIComponent(questionId)}/downvote`,
      method: 'POST',
      payload: { userId },
    }).catch(() => {});

    return { success: true, upvotes: 0, downvotes: 1 };
  },

  async reportTerm(termId: string, reason: string, details?: string, reportedBy?: string): Promise<any> {
    const payload = {
      termId,
      reason: (reason || 'Hata Bildirimi').trim(),
      details: (details || '').trim(),
      reportedBy: reportedBy || 'Tıp Öğrencisi',
      timestamp: new Date().toISOString()
    };

    if (typeof navigator !== 'undefined' && !navigator.onLine) {
      await offlineDatabaseService.queueAction({
        type: 'report',
        endpoint: `/api/terms/${encodeURIComponent(termId)}/report`,
        method: 'POST',
        payload
      });
      return { success: true, queued: true };
    }

    try {
      const res = await fetch(`/api/terms/${encodeURIComponent(termId)}/report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {
      await offlineDatabaseService.queueAction({
        type: 'report',
        endpoint: `/api/terms/${encodeURIComponent(termId)}/report`,
        method: 'POST',
        payload
      });
      return { success: true, queued: true };
    }
    return { success: true };
  },

  async reportFlashcard(cardId: string, reason: string, details?: string, reportedBy?: string): Promise<any> {
    const payload = {
      cardId,
      reason: (reason || 'Hata Bildirimi').trim(),
      details: (details || '').trim(),
      reportedBy: reportedBy || 'Tıp Öğrencisi',
      timestamp: new Date().toISOString()
    };

    if (typeof navigator !== 'undefined' && !navigator.onLine) {
      await offlineDatabaseService.queueAction({
        type: 'report',
        endpoint: `/api/cards/${encodeURIComponent(cardId)}/report`,
        method: 'POST',
        payload
      });
      return { success: true, queued: true };
    }

    try {
      const res = await fetch(`/api/cards/${encodeURIComponent(cardId)}/report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {
      await offlineDatabaseService.queueAction({
        type: 'report',
        endpoint: `/api/cards/${encodeURIComponent(cardId)}/report`,
        method: 'POST',
        payload
      });
      return { success: true, queued: true };
    }
    return { success: true };
  },

  /** Çıkmış soruyu kalıcı siler */
  async adminDeletePastQuestion(adminEmail: string, id: string): Promise<void> {
    const res = await safeJsonFetch<{ success: boolean; error?: string }>(`/api/past-exams/${encodeURIComponent(id)}`, {
      method: 'DELETE',
      headers: { 'x-admin-email': adminEmail },
    });
    if (!res.ok || !res.data?.success) throw new Error(res.data?.error || res.error || 'Soru silinemedi.');
    try { await pastQuestionsCache.removeQuestions([id]); } catch { /* önbellek yoksa geç */ }
  },

  /** Anketi açık (cevabı belirsiz) soruların güncel listesi; önbellekten bağımsız. */
  async getAnswerDoubtful(): Promise<AnswerDoubtfulInfo | null> {
    const res = await safeJsonFetch<{ success: boolean } & AnswerDoubtfulInfo>('/api/past-question-reviews/answer-doubtful');
    return res.ok && res.data?.success ? { ids: res.data.ids || [], options: res.data.options || {}, resolved: res.data.resolved || {} } : null;
  },

  /** Soru havuzu (Çalış) sorusunu bildir. */
  async reportOrnekQuestion(questionId: string, reason: string, details?: string): Promise<any> {
    const nowIso = new Date().toISOString();
    const reportObj = {
      id: `rep-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      soru_id: questionId,
      questionId,
      reason: (reason || 'Hata Bildirimi').trim(),
      details: (details || '').trim(),
      reportedBy: 'Tıp Öğrencisi',
      createdAt: nowIso,
      timestamp: nowIso,
    };

    // 1. Try server
    try {
      const res = await safeJsonFetch<{ success: boolean; report: any; error?: string }>(`/api/ornek-sorular/${encodeURIComponent(questionId)}/report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason: reportObj.reason, details: reportObj.details, reportedBy: reportObj.reportedBy }),
      });
      if (res.ok && res.data?.success) {
        return res.data;
      }
    } catch (_) {}

    // 2. Direct Firestore Cloud save (sunucuya ulaşılamazsa)
    try {
      await FirestoreDbService.logAdminNotification({
        id: reportObj.id,
        type: 'report',
        title: `🚨 Örnek Soru Hata Bildirimi (#${questionId})`,
        message: `${reportObj.reason}${reportObj.details ? ` - ${reportObj.details}` : ''}`,
        timestamp: reportObj.timestamp,
        isRead: false,
        author: reportObj.reportedBy,
      });
      if (FIREBASE_DB_ENABLED) {
        await addDoc(collection(db, 'question_reports'), reportObj);
      }
    } catch (e: any) {
      console.warn('[reportOrnekQuestion] Firestore yedeği uyarısı:', e?.message);
    }

    // 3. Direct Supabase Cloud save
    try {
      await SupabaseDbService.reportPastQuestion(questionId, {
        id: reportObj.id,
        reason: reportObj.reason,
        details: reportObj.details,
        reportedBy: reportObj.reportedBy,
        timestamp: reportObj.timestamp,
      });
    } catch (_) {}

    if (typeof navigator !== 'undefined' && !navigator.onLine) {
      offlineDatabaseService.queueAction({
        type: 'report',
        endpoint: `/api/ornek-sorular/${encodeURIComponent(questionId)}/report`,
        method: 'POST',
        payload: { reason: reportObj.reason, details: reportObj.details, reportedBy: reportObj.reportedBy },
      }).catch(() => {});
    }

    return { success: true, report: reportObj };
  },

  async reportPoolQuestion(questionId: string, reason: string, details?: string, reportedBy?: string): Promise<any> {
    const nowIso = new Date().toISOString();
    const reportObj = {
      id: `rep-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      questionId,
      reason: (reason || 'Hata Bildirimi').trim(),
      details: (details || '').trim(),
      reportedBy: reportedBy || 'Tıp Öğrencisi',
      createdAt: nowIso,
      timestamp: nowIso,
    };

    // 1. Try server
    try {
      const res = await safeJsonFetch<{ success: boolean; report: any; error?: string }>(`/api/questions/${encodeURIComponent(questionId)}/report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason: reportObj.reason, details: reportObj.details, reportedBy: reportObj.reportedBy }),
      });
      if (res.ok && res.data?.success) {
        return res.data;
      }
    } catch (_) {}

    // 2. Direct Firestore Cloud save (sunucuya ulaşılamazsa)
    try {
      await FirestoreDbService.logAdminNotification({
        id: reportObj.id,
        type: 'report',
        title: `🚨 Havuz Sorusu Hata Bildirimi (#${questionId})`,
        message: `${reportObj.reason}${reportObj.details ? ` - ${reportObj.details}` : ''}`,
        timestamp: reportObj.timestamp,
        isRead: false,
        author: reportObj.reportedBy,
      });
      if (FIREBASE_DB_ENABLED) {
        await addDoc(collection(db, 'question_reports'), reportObj);
      }
    } catch (e: any) {
      console.warn('[reportPoolQuestion] Firestore yedeği uyarısı:', e?.message);
    }

    // 3. Direct Supabase Cloud save
    try {
      await SupabaseDbService.reportPastQuestion(questionId, {
        id: reportObj.id,
        reason: reportObj.reason,
        details: reportObj.details,
        reportedBy: reportObj.reportedBy,
        timestamp: reportObj.timestamp,
      });
    } catch (_) {}

    if (typeof navigator !== 'undefined' && !navigator.onLine) {
      offlineDatabaseService.queueAction({
        type: 'report',
        endpoint: `/api/questions/${encodeURIComponent(questionId)}/report`,
        method: 'POST',
        payload: { reason: reportObj.reason, details: reportObj.details, reportedBy: reportObj.reportedBy },
      }).catch(() => {});
    }

    return { success: true, report: reportObj };
  },

  async getAnswerVotes(questionId: string, voterUid: string): Promise<AnswerVotes> {
    const res = await safeJsonFetch<AnswerVotes & { success: boolean; error?: string }>(
      `/api/past-question-reviews/${encodeURIComponent(questionId)}/answer-votes`,
      { headers: { 'x-voter-uid': voterUid } }
    );
    if (!res.ok || !res.data?.success) throw new Error(res.data?.error || res.error || 'Oylar okunamadı.');
    return res.data;
  },

  /** Kendi oyunu geri al (şıkkı değiştirmek için). */
  async cancelAnswerVote(questionId: string, voterUid: string): Promise<AnswerVotes> {
    const res = await safeJsonFetch<AnswerVotes & { success: boolean; error?: string }>(
      `/api/past-question-reviews/${encodeURIComponent(questionId)}/answer-votes`,
      { method: 'DELETE', headers: { 'x-voter-uid': voterUid } }
    );
    if (!res.ok || !res.data?.success) throw new Error(res.data?.error || res.error || 'Oy geri alınamadı.');
    return res.data;
  },

  /** Cevabı olan soruyu topluluk anketine aç. */
  async openAnswerPoll(questionId: string, voterUid: string): Promise<{ answer: string }> {
    const res = await safeJsonFetch<{ success: boolean; answer: string; error?: string }>(
      `/api/past-question-reviews/${encodeURIComponent(questionId)}/open-poll`,
      { method: 'POST', headers: { 'x-voter-uid': voterUid } }
    );
    if (!res.ok || !res.data?.success) throw new Error(res.data?.error || res.error || 'Anket açılamadı.');
    return { answer: res.data.answer };
  },

  /** Soruyu Faz 14 yapay zekâ incelemesine gönder (ücretsiz kuyruk). */
  async requestAiReview(questionId: string, body: { message?: string; name?: string; uid?: string; email?: string }): Promise<{ joined: boolean; position: number; waiting: number }> {
    const res = await safeJsonFetch<{ success: boolean; joined: boolean; position: number; waiting: number; error?: string }>(
      `/api/past-exams/${encodeURIComponent(questionId)}/ai-review`,
      { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }
    );
    if (!res.ok || !res.data?.success) throw new Error(res.data?.error || res.error || 'İstek gönderilemedi. Sunucuya ulaşılamıyor olabilir.');
    return res.data;
  },

  /** İnceleme kuyruğundaki sorular (sıra numarasıyla). */
  async getAiReviewQueue(): Promise<{ waiting: number; items: Record<string, { status: string; position?: number; requests: number }> } | null> {
    const res = await safeJsonFetch<{ success: boolean; waiting: number; items: Record<string, any> }>('/api/past-exams/ai-review-queue');
    return res.ok && res.data?.success ? { waiting: res.data.waiting, items: res.data.items || {} } : null;
  },

  async castAnswerVote(questionId: string, voterUid: string, choice: string): Promise<AnswerVotes> {
    const res = await safeJsonFetch<AnswerVotes & { success: boolean; error?: string }>(
      `/api/past-question-reviews/${encodeURIComponent(questionId)}/answer-votes`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-voter-uid': voterUid },
        body: JSON.stringify({ choice }),
      }
    );
    if (!res.ok || !res.data?.success) throw new Error(res.data?.error || res.error || 'Oy kaydedilemedi.');
    return res.data;
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

    return { success: false, error: serverErrorMsg || 'Yapay zeka soru optimizasyonu gerçekleştirilemedi.' };
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

  async chatWithQuestionTutor(params: {
    questionContext: QuestionChatContext;
    messages: { role: 'user' | 'assistant'; content: string }[];
    currentMessage: string;
    apiKey?: string;
    groqApiKey?: string;
    museSparkApiKey?: string;
    preferredProvider?: 'auto' | 'gemini' | 'groq' | 'muse-spark';
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
    isThreeAttemptsFailed?: boolean;
    error?: string;
  }> {
    const customApiKey = params.apiKey ||
      (typeof window !== 'undefined' && (window as any).MEDSORU_GEMINI_KEY) ||
      localStorage.getItem('medsoru_gemini_api_key') ||
      localStorage.getItem('medsoru_custom_gemini_key') ||
      (import.meta as any).env?.VITE_GEMINI_API_KEY ||
      '';

    const customGroqKey = params.groqApiKey || localStorage.getItem('medsoru_groq_api_key') || '';
    const customMuseSparkKey = params.museSparkApiKey || localStorage.getItem('medsoru_muse_spark_api_key') || '';
    const museSparkBaseUrl = localStorage.getItem('medsoru_muse_spark_base_url') || '';
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
          museSparkApiKey: customMuseSparkKey,
          museSparkBaseUrl,
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

      // If server already tried providers and reported multi-attempt failure:
      if (res.data && (res.data.isThreeAttemptsFailed || res.data.isTwoAttemptsFailed || res.data.attemptsCount >= 2)) {
        return {
          success: false,
          attemptsCount: res.data.attemptsCount || 3,
          isTwoAttemptsFailed: true,
          isThreeAttemptsFailed: Boolean(res.data.isThreeAttemptsFailed),
          error: res.data.error || 'Tüm sağlayıcılar denendi: Google Gemini, Groq Cloud ve Muse Spark 1.3 Free yanıt veremedi. Lütfen API kotalarını veya bağlantınızı kontrol edin.'
        };
      }

      serverErrorMsg = res.data?.error || (res as any).error || '';
    } catch (e: any) {
      serverErrorMsg = e.message || '';
    }

    return { success: false, error: serverErrorMsg || 'Yapay zeka asistanı yanıt veremedi. Sunucunun çalıştığından emin olun.' };
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

  async getQualityAuditStatus(): Promise<any> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/audit/status` : `/api/audit/status`;
      const res = await safeJsonFetch<any>(endpoint);
      return res.ok && res.data?.success ? res.data : null;
    } catch (_) {
      return null;
    }
  },

  async sendGeneralAiChat(params: {
    message: string;
    messages?: { role: 'user' | 'assistant'; content: string }[];
    provider?: string;
    model?: string;
    mode?: 'general' | 'find_question' | 'generate_from_keywords' | 'explain';
    apiKey?: string;
    groqApiKey?: string;
    museSparkApiKey?: string;
    allowCloudFallback?: boolean;
    timeoutMs?: number;
  }): Promise<{
    success: boolean;
    reply?: string;
    error?: string;
    providerUsed?: string;
    planUsed?: string;
    matchedQuestions?: any[];
  }> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/ai/general-chat` : `/api/ai/general-chat`;
      const res = await safeJsonFetch<any>(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params)
      });
      if (res.ok && res.data?.success) {
        return res.data;
      }
      return { success: false, error: res.data?.error || 'Yapay zeka yanıt veremedi.' };
    } catch (e: any) {
      return { success: false, error: e.message || 'Bağlantı hatası oluştu.' };
    }
  },

  async getAiErrorLogs(): Promise<{ success: boolean; logs: any[]; unresolvedCount: number }> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/ai/error-logs` : `/api/ai/error-logs`;
      const res = await safeJsonFetch<any>(endpoint);
      if (res.ok && res.data?.success) {
        return res.data;
      }
      return { success: false, logs: [], unresolvedCount: 0 };
    } catch (_) {
      return { success: false, logs: [], unresolvedCount: 0 };
    }
  },

  async resolveAiErrorLog(id: string, status: 'resolved' | 'investigating' = 'resolved'): Promise<{ success: boolean; message?: string }> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/ai/error-logs/resolve` : `/api/ai/error-logs/resolve`;
      const res = await safeJsonFetch<any>(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, status })
      });
      return res.data || { success: false };
    } catch (_) {
      return { success: false };
    }
  },

  async getPoolQuestionClusters(): Promise<any[]> {
    const res = await safeJsonFetch<{ clusters: any[] }>('/api/pool-clusters');
    return res.data?.clusters || [];
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
