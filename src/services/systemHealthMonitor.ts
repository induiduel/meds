/**
 * MedSoru Sistem & Veritabanı Sağlık Takip Servisi (systemHealthMonitor.ts)
 * 
 * Bu servis:
 * 1. Online Firebase Firestore (Spark kotası, izinler, bağlantı) durumunu izler.
 * 2. Online Supabase PostgreSQL (tablo varlığı, satır sayıları, gecikme) durumunu izler.
 * 3. Yapay Zeka (Gemini kotaları, 429 Rate Limit, Groq Cloud, harcama limiti) durumunu izler.
 * 4. Veritabanı ya da AI limiti aşıldığında UI bileşenlerine anında reaktif bildirim gönderir.
 * 5. Tarayıcı konsolunda doğrudan `window.medsoruCheckStatus()` ile çalıştırılabilir.
 */

import { SupabaseDbService, getSupabaseConfig } from './supabaseDb';
import { FirestoreDbService } from './firestoreDb';
import { CLIENT_FREE_GEMINI_KEYS, CLIENT_BILLED_GEMINI_KEY } from './api';

export type ServiceStatus = 'healthy' | 'warning' | 'critical' | 'unknown';

export interface FirebaseHealth {
  status: 'online' | 'quota_exceeded' | 'permission_denied' | 'network_error' | 'offline';
  sparkReadLimit: string;
  details?: string;
  lastChecked: number;
}

export interface SupabaseHealth {
  status: 'online' | 'missing_tables' | 'auth_error' | 'network_error' | 'not_configured' | 'offline';
  latencyMs?: number;
  tables: {
    committees: boolean;
    questions: boolean;
    past_questions: boolean;
    lecture_notes: boolean;
  };
  rowCounts: {
    committees: number;
    questions: number;
    past_questions: number;
    lecture_notes: number;
  };
  details?: string;
  lastChecked: number;
}

export interface AiKeyHealth {
  label: string;
  status: 'ok' | 'quota_exceeded' | 'high_demand' | 'spending_cap_exceeded' | 'not_configured' | 'error';
  model?: string;
  statusCode?: number;
  retryAfterSeconds?: number;
  details?: string;
}

export interface AiSystemHealth {
  status: 'ready' | 'degraded' | 'all_exhausted';
  keys: AiKeyHealth[];
  groqConfigured: boolean;
  lastAiError?: {
    timestamp: number;
    message: string;
    isQuota: boolean;
    provider: string;
  } | null;
  lastChecked: number;
}

export interface SystemOverallHealth {
  timestamp: number;
  overallStatus: ServiceStatus;
  databaseFailureLevel: 'none' | 'warning' | 'critical';
  firebase: FirebaseHealth;
  supabase: SupabaseHealth;
  ai: AiSystemHealth;
  localPcOnline: boolean;
  activeDatabaseMode: string;
  hasCriticalDatabaseError: boolean;
  hasAiQuotaAlert: boolean;
  statusMessage: string;
}

type HealthListener = (health: SystemOverallHealth) => void;

class SystemHealthMonitor {
  private currentHealth: SystemOverallHealth;
  private listeners: Set<HealthListener> = new Set();
  private isChecking = false;
  private checkIntervalTimer: any = null;

  constructor() {
    this.currentHealth = {
      timestamp: Date.now(),
      overallStatus: 'unknown',
      databaseFailureLevel: 'none',
      firebase: {
        status: 'online',
        sparkReadLimit: '50.000 okuma/gün',
        lastChecked: 0,
      },
      supabase: {
        status: 'online',
        tables: { committees: false, questions: false, past_questions: false, lecture_notes: false },
        rowCounts: { committees: 0, questions: 0, past_questions: 0, lecture_notes: 0 },
        lastChecked: 0,
      },
      ai: {
        status: 'ready',
        keys: [],
        groqConfigured: false,
        lastAiError: null,
        lastChecked: 0,
      },
      localPcOnline: false,
      activeDatabaseMode: 'auto',
      hasCriticalDatabaseError: false,
      hasAiQuotaAlert: false,
      statusMessage: 'Sistem durumu kontrol ediliyor...',
    };

    // Global erişim için tarayıcı penceresine bağla
    if (typeof window !== 'undefined') {
      (window as any).medsoruHealth = this;
      (window as any).medsoruCheckStatus = () => this.runFullDiagnostic(true);
    }
  }

  public subscribe(listener: HealthListener): () => void {
    this.listeners.add(listener);
    // Hemen mevcut durumu ilet
    listener(this.currentHealth);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notify() {
    for (const l of this.listeners) {
      try {
        l(this.currentHealth);
      } catch (e) {
        console.warn('[SystemHealthMonitor] Listener error:', e);
      }
    }
  }

  public getHealth(): SystemOverallHealth {
    return this.currentHealth;
  }

  /**
   * Herhangi bir API / DB çağrısında hata fırlatıldığında anında tetiklenir
   */
  public recordDatabaseError(source: 'firebase' | 'supabase', error: any) {
    const errMsg = error?.message || String(error);
    const isQuota = /quota|resource-exhausted|exceeded|429/i.test(errMsg);
    const isPermission = /permission-denied|unauthorized|forbidden/i.test(errMsg);

    if (source === 'firebase') {
      if (isQuota) {
        this.currentHealth.firebase.status = 'quota_exceeded';
        this.currentHealth.firebase.details = 'Firebase Spark 50.000 günlük ücretsiz okuma kotası doldu.';
      } else if (isPermission) {
        this.currentHealth.firebase.status = 'permission_denied';
        this.currentHealth.firebase.details = 'Firebase Firestore erişim yetkisi reddedildi.';
      } else {
        this.currentHealth.firebase.status = 'offline';
        this.currentHealth.firebase.details = errMsg;
      }
      this.currentHealth.firebase.lastChecked = Date.now();
    } else if (source === 'supabase') {
      this.currentHealth.supabase.status = 'error' as any;
      this.currentHealth.supabase.details = errMsg;
      this.currentHealth.supabase.lastChecked = Date.now();
    }

    this.recalculateOverall();
    this.notify();
  }

  /**
   * Yapay Zeka (Gemini / Groq) çağrısında limit veya hata alındığında anında tetiklenir
   */
  public recordAiError(error: any, provider: string = 'Gemini', model: string = 'gemini-3.8-flash') {
    const errMsg = error?.message || String(error);
    const isQuota = /429|resource_exhausted|spending cap|quota|rate limit/i.test(errMsg);
    const isSpendingCap = /spending cap/i.test(errMsg);

    this.currentHealth.ai.lastAiError = {
      timestamp: Date.now(),
      message: errMsg,
      isQuota,
      provider,
    };

    if (isQuota) {
      this.currentHealth.hasAiQuotaAlert = true;
      if (isSpendingCap) {
        this.currentHealth.statusMessage = 'Yapay zeka projesi aylık harcama limitine ulaştı.';
      } else {
        this.currentHealth.statusMessage = 'Yapay zeka ücretsiz istek kotası (HTTP 429) aşıldı.';
      }
    }

    this.recalculateOverall();
    this.notify();
  }

  /**
   * Kapsamlı tam sistem teşhis testi (Firebase, Supabase ve AI havuzu)
   */
  public async runFullDiagnostic(logToConsole = true): Promise<SystemOverallHealth> {
    if (this.isChecking) return this.currentHealth;
    this.isChecking = true;

    if (logToConsole) {
      console.log('%c🔍 [MedSoru Teşhis] Tam sistem sağlık kontrolü başlatılıyor...', 'color:#2563EB;font-weight:bold;font-size:14px;');
    }

    // 1. Firebase Firestore Testi
    await this.checkFirebase(logToConsole);

    // 2. Supabase PostgreSQL Testi
    await this.checkSupabase(logToConsole);

    // 3. Yapay Zeka (Gemini & Groq) Testi
    await this.checkAiPool(logToConsole);

    this.recalculateOverall();
    this.isChecking = false;
    this.notify();

    if (logToConsole) {
      this.printConsoleSummary();
    }

    return this.currentHealth;
  }

  private async checkFirebase(logToConsole: boolean) {
    const start = Date.now();
    try {
      // Doğrudan Firebase Firestore'dan hızlı okuma testi
      const committees = await FirestoreDbService.getCommittees();
      this.currentHealth.firebase = {
        status: 'online',
        sparkReadLimit: '50.000 okuma/gün',
        details: `Aktif (${committees.length} kurul, ${Date.now() - start}ms)`,
        lastChecked: Date.now(),
      };
      if (logToConsole) console.log('✅ [Firebase Firestore] Çevrimiçi ve erişilebilir.');
    } catch (err: any) {
      const msg = err?.message || String(err);
      const isQuota = /quota|resource-exhausted|exceeded/i.test(msg);
      const isPermission = /permission-denied/i.test(msg);

      if (isQuota) {
        this.currentHealth.firebase = {
          status: 'quota_exceeded',
          sparkReadLimit: '50.000 okuma/gün (DOLDU)',
          details: 'Spark ücretsiz günlük okuma kotası (50.000) tükendi. Supabase otomatik devreye girmeli.',
          lastChecked: Date.now(),
        };
        if (logToConsole) console.warn('⚠️ [Firebase Firestore] Spark 50K okuma kotası dolmuş!');
      } else if (isPermission) {
        this.currentHealth.firebase = {
          status: 'permission_denied',
          sparkReadLimit: 'Erişim Engellendi',
          details: 'Firestore güvenlik kuralları erişimi engelledi.',
          lastChecked: Date.now(),
        };
        if (logToConsole) console.error('❌ [Firebase Firestore] Yetki hatası: ' + msg);
      } else {
        this.currentHealth.firebase = {
          status: 'offline',
          sparkReadLimit: 'Bilinmiyor',
          details: msg,
          lastChecked: Date.now(),
        };
        if (logToConsole) console.error('❌ [Firebase Firestore] Bağlantı hatası: ' + msg);
      }
    }
  }

  private async checkSupabase(logToConsole: boolean) {
    const { url, key } = getSupabaseConfig();
    if (!url || !key) {
      this.currentHealth.supabase = {
        status: 'not_configured',
        tables: { committees: false, questions: false, past_questions: false, lecture_notes: false },
        rowCounts: { committees: 0, questions: 0, past_questions: 0, lecture_notes: 0 },
        details: 'Supabase URL veya Anon Key ayarlanmamış.',
        lastChecked: Date.now(),
      };
      return;
    }

    try {
      const client = (SupabaseDbService as any).getSupabaseClient ? (SupabaseDbService as any).getSupabaseClient() : null;
      if (!client) {
        const { createClient } = await import('@supabase/supabase-js');
        const tempClient = createClient(url, key);
        await this.inspectSupabaseTables(tempClient, logToConsole);
      } else {
        await this.inspectSupabaseTables(client, logToConsole);
      }
    } catch (err: any) {
      this.currentHealth.supabase = {
        status: 'offline',
        tables: { committees: false, questions: false, past_questions: false, lecture_notes: false },
        rowCounts: { committees: 0, questions: 0, past_questions: 0, lecture_notes: 0 },
        details: err?.message || 'Supabase ile bağlantı kurulamadı.',
        lastChecked: Date.now(),
      };
      if (logToConsole) console.error('❌ [Supabase] Bağlantı hatası:', err.message);
    }
  }

  private async inspectSupabaseTables(client: any, logToConsole: boolean) {
    const start = Date.now();
    const tables = { committees: false, questions: false, past_questions: false, lecture_notes: false };
    const rowCounts = { committees: 0, questions: 0, past_questions: 0, lecture_notes: 0 };
    let hasTableError = false;
    let authError = false;

    for (const t of ['committees', 'questions', 'past_questions', 'lecture_notes'] as const) {
      try {
        const { count, error } = await client.from(t).select('*', { count: 'exact', head: true });
        if (error) {
          if (/relation|does not exist/i.test(error.message)) {
            hasTableError = true;
          } else if (/JWT|unauthorized|API key/i.test(error.message)) {
            authError = true;
          }
        } else {
          tables[t] = true;
          rowCounts[t] = count ?? 0;
        }
      } catch {
        hasTableError = true;
      }
    }

    const latencyMs = Date.now() - start;

    if (authError) {
      this.currentHealth.supabase = {
        status: 'auth_error',
        latencyMs,
        tables,
        rowCounts,
        details: 'Supabase API anahtarı geçersiz veya yetkisiz.',
        lastChecked: Date.now(),
      };
      if (logToConsole) console.error('❌ [Supabase] Yetki / API anahtarı hatası.');
    } else if (hasTableError && !tables.committees && !tables.questions) {
      this.currentHealth.supabase = {
        status: 'missing_tables',
        latencyMs,
        tables,
        rowCounts,
        details: 'Supabase bağlantısı kuruldu ancak SQL tabloları henüz oluşturulmamış.',
        lastChecked: Date.now(),
      };
      if (logToConsole) console.warn('⚠️ [Supabase] Tablolar bulunamadı, SQL şeması çalıştırılmalı.');
    } else {
      this.currentHealth.supabase = {
        status: 'online',
        latencyMs,
        tables,
        rowCounts,
        details: `Bağlı (${latencyMs}ms, ${rowCounts.past_questions + rowCounts.questions} soru hazır)`,
        lastChecked: Date.now(),
      };
      if (logToConsole) console.log(`✅ [Supabase] Çevrimiçi (${rowCounts.past_questions} çıkmış soru, ${rowCounts.committees} kurul).`);
    }
  }

  private async checkAiPool(logToConsole: boolean) {
    const keysReport: AiKeyHealth[] = [];
    const customGroqKey = (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_groq_api_key') : '') || '';
    const customGeminiKey = (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_gemini_api_key') : '') || '';

    const testKeys = [
      ...(customGeminiKey ? [{ key: customGeminiKey, label: 'Kullanıcı Özel Gemini Anahtarı', isBilled: false }] : []),
      ...CLIENT_FREE_GEMINI_KEYS,
      ...(CLIENT_BILLED_GEMINI_KEY ? [CLIENT_BILLED_GEMINI_KEY] : [])
    ];

    let anyKeyWorking = false;
    let anyQuotaExceeded = false;

    // Sadece ilk 2 anahtarı hızlı pingleyelim (kullanıcıyı bekletmemek için)
    for (let i = 0; i < Math.min(testKeys.length, 3); i++) {
      const k = testKeys[i];
      try {
        const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash?key=${k.key}`, {
          method: 'GET',
          headers: { 'Accept': 'application/json' }
        });
        const data = await res.json();
        if (res.ok) {
          keysReport.push({
            label: k.label,
            status: 'ok',
            model: 'gemini-3.8-flash',
            statusCode: 200,
            details: 'Model hazır ve yanıt veriyor.',
          });
          anyKeyWorking = true;
        } else {
          const errMsg = data.error?.message || '';
          const is429 = res.status === 429 || /quota|resource_exhausted/i.test(errMsg);
          const isSpendingCap = /spending cap/i.test(errMsg);
          const is503 = res.status === 503;

          if (isSpendingCap) {
            keysReport.push({
              label: k.label,
              status: 'spending_cap_exceeded',
              statusCode: 429,
              details: 'Aylık proje harcama sınırı aşıldı.',
            });
            anyQuotaExceeded = true;
          } else if (is429) {
            keysReport.push({
              label: k.label,
              status: 'quota_exceeded',
              statusCode: 429,
              details: 'Dakikalık/günlük istek limiti aşıldı.',
            });
            anyQuotaExceeded = true;
          } else if (is503) {
            keysReport.push({
              label: k.label,
              status: 'high_demand',
              statusCode: 503,
              details: 'Sunucu aşırı yüklü, geçici yoğunluk.',
            });
          } else {
            keysReport.push({
              label: k.label,
              status: 'error',
              statusCode: res.status,
              details: errMsg,
            });
          }
        }
      } catch (e: any) {
        keysReport.push({
          label: k.label,
          status: 'error',
          details: e.message,
        });
      }
    }

    const groqOk = Boolean(customGroqKey && customGroqKey.startsWith('gsk_'));
    this.currentHealth.ai = {
      status: anyKeyWorking ? 'ready' : (groqOk ? 'ready' : (anyQuotaExceeded ? 'all_exhausted' : 'degraded')),
      keys: keysReport,
      groqConfigured: groqOk,
      lastAiError: this.currentHealth.ai.lastAiError,
      lastChecked: Date.now(),
    };

    if (anyQuotaExceeded && !anyKeyWorking && !groqOk) {
      this.currentHealth.hasAiQuotaAlert = true;
    }

    if (logToConsole) {
      if (anyKeyWorking) {
        console.log('✅ [Yapay Zeka] Gemini modelleri aktif ve yanıt veriyor.');
      } else if (groqOk) {
        console.log('ℹ️ [Yapay Zeka] Gemini kotaları doldu ancak Groq Cloud (Llama 3.3) yedek olarak hazır.');
      } else {
        console.warn('⚠️ [Yapay Zeka] Gemini ücretsiz kotaları aşıldı (HTTP 429)!');
      }
    }
  }

  private recalculateOverall() {
    const fb = this.currentHealth.firebase;
    const supa = this.currentHealth.supabase;
    const ai = this.currentHealth.ai;

    const fbWorking = fb.status === 'online';
    const supaWorking = supa.status === 'online';

    // KRİTİK VERİTABANI HATASI: Hem Firebase hem Supabase çalışmıyorsa
    if (!fbWorking && !supaWorking) {
      this.currentHealth.databaseFailureLevel = 'critical';
      this.currentHealth.hasCriticalDatabaseError = true;
      this.currentHealth.overallStatus = 'critical';
      this.currentHealth.statusMessage =
        '🚨 KRİTİK VERİTABANI HATASI: Hem Firebase hem Supabase veritabanlarına ulaşılamıyor! Soru havuzu ve senkronizasyon çalışamaz.';
    } else if (!fbWorking && supaWorking) {
      // Firebase kotası dolmuş ama Supabase devralmış
      this.currentHealth.databaseFailureLevel = 'warning';
      this.currentHealth.hasCriticalDatabaseError = false;
      this.currentHealth.overallStatus = 'warning';
      this.currentHealth.statusMessage =
        '⚠️ Firebase Spark kotası doldu. Supabase PostgreSQL bulut veritabanı aktif olarak devraldı.';
    } else if (fbWorking && !supaWorking) {
      this.currentHealth.databaseFailureLevel = 'warning';
      this.currentHealth.hasCriticalDatabaseError = false;
      this.currentHealth.overallStatus = 'warning';
      this.currentHealth.statusMessage =
        '⚠️ Supabase çevrimdışı, Firebase Firestore üzerinden çalışılıyor.';
    } else {
      this.currentHealth.databaseFailureLevel = 'none';
      this.currentHealth.hasCriticalDatabaseError = false;
      this.currentHealth.overallStatus = ai.status === 'all_exhausted' ? 'warning' : 'healthy';
      this.currentHealth.statusMessage =
        ai.status === 'all_exhausted'
          ? '⚠️ Yapay zeka limitleri aşıldı (Hata 429). Veritabanı sağlıklı.'
          : '✅ Tüm sistemler ve bulut veritabanları sağlıklı.';
    }

    if (ai.status === 'all_exhausted') {
      this.currentHealth.hasAiQuotaAlert = true;
    }
  }

  private printConsoleSummary() {
    console.group('%c📊 [MedSoru Teşhis Özeti]', 'color:#10B981;font-weight:bold;');
    console.log('Genel Durum:', this.currentHealth.overallStatus.toUpperCase());
    console.log('Firebase Durumu:', this.currentHealth.firebase.status, `(${this.currentHealth.firebase.details || ''})`);
    console.log('Supabase Durumu:', this.currentHealth.supabase.status, `(${this.currentHealth.supabase.details || ''})`);
    console.log('Yapay Zeka Durumu:', this.currentHealth.ai.status);
    if (this.currentHealth.hasCriticalDatabaseError) {
      console.error('%c🚨 KRİTİK VERİTABANI HATASI: Hem Firebase hem Supabase çevrimdışı!', 'font-size:16px;font-weight:bold;color:red;');
    }
    if (this.currentHealth.hasAiQuotaAlert) {
      console.warn('%c⚠️ YAPAY ZEKA KOTA UYARISI: Gemini limitleri aşıldı!', 'font-size:14px;font-weight:bold;color:orange;');
    }
    console.groupEnd();
  }

  public startAutoMonitoring(intervalMs = 60000) {
    if (this.checkIntervalTimer) clearInterval(this.checkIntervalTimer);
    // İlk açılışta hemen kontrol et
    this.runFullDiagnostic(false);
    this.checkIntervalTimer = setInterval(() => {
      this.runFullDiagnostic(false);
    }, intervalMs);
  }

  public stopAutoMonitoring() {
    if (this.checkIntervalTimer) {
      clearInterval(this.checkIntervalTimer);
      this.checkIntervalTimer = null;
    }
  }
}

export const systemHealthMonitor = new SystemHealthMonitor();
