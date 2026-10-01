import { Committee, QuestionItem, LectureNote, AdminNotification } from '../types';
import { FirestoreDbService, db as firestoreDb } from './firestoreDb';
import { SupabaseDbService } from './supabaseDb';
import { safeJsonFetch, getCustomApiUrl } from './api';

export type DatabaseMode = 'auto' | 'supabase' | 'firebase' | 'local_pc';

export interface DatabaseStatus {
  mode: DatabaseMode;
  firebase: {
    status: 'online' | 'quota_exceeded' | 'error' | 'offline';
    details?: string;
  };
  supabase: {
    status: 'online' | 'error' | 'not_configured' | 'offline';
    details?: string;
  };
  localPc: {
    status: 'online' | 'offline';
    details?: string;
  };
}

const DB_MODE_KEY = 'medsoru_active_db_mode';

class MultiDbManager {
  private activeMode: DatabaseMode = 'auto';
  private firebaseQuotaExceeded = false;
  private lastQuotaCheck = 0;

  constructor() {
    if (typeof localStorage !== 'undefined') {
      const saved = localStorage.getItem(DB_MODE_KEY) as DatabaseMode | null;
      if (saved && ['auto', 'supabase', 'firebase', 'local_pc'].includes(saved)) {
        this.activeMode = saved;
      }
    }
  }

  public getActiveMode(): DatabaseMode {
    return this.activeMode;
  }

  public setActiveMode(mode: DatabaseMode) {
    this.activeMode = mode;
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(DB_MODE_KEY, mode);
    }
    console.log(`[MultiDbManager] Aktif veritabanı modu değiştirildi: ${mode}`);
  }

  public markFirebaseQuotaExceeded() {
    this.firebaseQuotaExceeded = true;
    this.lastQuotaCheck = Date.now();
    console.warn('[MultiDbManager] Firebase Spark günlük okuma/yazma kotası aşıldı! Otomatik olarak Supabase / Yerel PC devraldı.');
  }

  public isFirebaseQuotaExceeded(): boolean {
    // Reset check every 30 minutes in case quota reset
    if (this.firebaseQuotaExceeded && Date.now() - this.lastQuotaCheck > 1800000) {
      this.firebaseQuotaExceeded = false;
    }
    return this.firebaseQuotaExceeded;
  }

  /**
   * Health check across all databases
   */
  public async getStatuses(): Promise<DatabaseStatus> {
    const status: DatabaseStatus = {
      mode: this.activeMode,
      firebase: {
        status: this.isFirebaseQuotaExceeded() ? 'quota_exceeded' : 'online',
        details: this.isFirebaseQuotaExceeded() ? 'Spark günlük ücretsiz limit (50K okuma) aşıldı' : 'Aktif (Spark Plan)',
      },
      supabase: {
        status: 'not_configured',
      },
      localPc: {
        status: 'offline',
      },
    };

    // Test Supabase
    try {
      const supaHealth = await SupabaseDbService.healthCheck();
      if (supaHealth.connected) {
        status.supabase.status = 'online';
        status.supabase.details = `Bağlı (${supaHealth.latencyMs}ms)`;
      } else {
        status.supabase.status = supaHealth.error?.includes('yapılandırılmamış') ? 'not_configured' : 'error';
        status.supabase.details = supaHealth.error || 'Bağlantı kurulamadı';
      }
    } catch (e: any) {
      status.supabase.status = 'error';
      status.supabase.details = e.message;
    }

    // Test Local PC
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/health` : '/api/health';
      const res = await safeJsonFetch<any>(endpoint);
      if (res.ok && res.data?.status === 'online') {
        status.localPc.status = 'online';
        status.localPc.details = `Aktif (Uptime: ${res.data.uptime}s)`;
      } else {
        status.localPc.status = 'offline';
        status.localPc.details = 'Yerel sunucu yanıt vermiyor';
      }
    } catch {
      status.localPc.status = 'offline';
    }

    return status;
  }

  /**
   * Resilient Committee fetcher with failover
   */
  public async getCommittees(): Promise<Committee[]> {
    const mode = this.activeMode;

    // 1. If explicit Supabase mode
    if (mode === 'supabase') {
      try {
        const supa = await SupabaseDbService.getCommittees();
        if (supa && supa.length > 0) return supa;
      } catch (e) {
        console.warn('[MultiDbManager] Supabase getCommittees failed, falling back', e);
      }
    }

    // 2. If explicit Local PC mode
    if (mode === 'local_pc') {
      return this.getLocalCommittees();
    }

    // 3. Auto or Firebase mode: Try Firebase Spark first if quota not marked exceeded
    if (!this.isFirebaseQuotaExceeded() && mode !== 'supabase') {
      try {
        const fbCommittees = await FirestoreDbService.getCommittees();
        if (fbCommittees && fbCommittees.length > 0) {
          return fbCommittees;
        }
      } catch (err: any) {
        if (err?.message?.includes('Quota limit exceeded') || err?.code === 'resource-exhausted') {
          this.markFirebaseQuotaExceeded();
        } else {
          console.warn('[MultiDbManager] Firebase getCommittees failed, falling back to Supabase/Local', err);
        }
      }
    }

    // 4. Fallback to Supabase
    try {
      const supaCommittees = await SupabaseDbService.getCommittees();
      if (supaCommittees && supaCommittees.length > 0) {
        return supaCommittees;
      }
    } catch (e) {
      console.warn('[MultiDbManager] Supabase fallback getCommittees failed', e);
    }

    // 5. Final fallback to Local PC Express Server or LocalStorage
    return this.getLocalCommittees();
  }

  private async getLocalCommittees(): Promise<Committee[]> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/committees` : '/api/committees';
      const res = await safeJsonFetch<{ committees: Committee[] }>(endpoint);
      if (res.ok && res.data?.committees?.length) {
        return res.data.committees;
      }
    } catch (e) {
      console.warn('[MultiDbManager] Local server committees fetch failed', e);
    }
    return [];
  }

  /**
   * Resilient Questions fetcher with failover
   */
  public async getQuestions(committeeId: string): Promise<QuestionItem[]> {
    const mode = this.activeMode;

    // 1. Explicit Supabase
    if (mode === 'supabase') {
      try {
        const supa = await SupabaseDbService.getQuestions(committeeId);
        if (supa && supa.length > 0) return supa;
      } catch (e) {
        console.warn('[MultiDbManager] Supabase getQuestions failed', e);
      }
    }

    // 2. Explicit Local PC
    if (mode === 'local_pc') {
      return this.getLocalQuestions(committeeId);
    }

    // 3. Auto / Firebase mode
    if (!this.isFirebaseQuotaExceeded() && mode !== 'supabase') {
      try {
        const fbQ = await FirestoreDbService.getQuestions(committeeId);
        if (fbQ && fbQ.length > 0) return fbQ;
      } catch (err: any) {
        if (err?.message?.includes('Quota limit exceeded') || err?.code === 'resource-exhausted') {
          this.markFirebaseQuotaExceeded();
        } else {
          console.warn('[MultiDbManager] Firebase getQuestions failed', err);
        }
      }
    }

    // 4. Fallback to Supabase
    try {
      const supaQ = await SupabaseDbService.getQuestions(committeeId);
      if (supaQ && supaQ.length > 0) return supaQ;
    } catch (e) {}

    // 5. Final fallback to Local PC server
    return this.getLocalQuestions(committeeId);
  }

  private async getLocalQuestions(committeeId: string): Promise<QuestionItem[]> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl
        ? `${customUrl}/api/questions?committeeId=${encodeURIComponent(committeeId)}`
        : `/api/questions?committeeId=${encodeURIComponent(committeeId)}`;
      const res = await safeJsonFetch<{ questions: QuestionItem[] }>(endpoint);
      if (res.ok && res.data?.questions) {
        return res.data.questions;
      }
    } catch (e) {}
    return [];
  }

  /**
   * Resilient Past Questions fetcher with failover
   */
  public async getPastQuestions(): Promise<QuestionItem[]> {
    const mode = this.activeMode;

    // 1. Explicit Supabase
    if (mode === 'supabase') {
      try {
        const supa = await SupabaseDbService.getPastQuestions();
        if (supa && supa.length > 0) return supa;
      } catch (e) {
        console.warn('[MultiDbManager] Supabase getPastQuestions failed', e);
      }
    }

    // 2. Explicit Local PC
    if (mode === 'local_pc') {
      return this.getLocalPastQuestions();
    }

    // 3. Auto / Firebase mode
    if (!this.isFirebaseQuotaExceeded() && mode !== 'supabase') {
      try {
        const fbPast = await FirestoreDbService.getPastQuestions();
        if (fbPast && fbPast.length > 0) return fbPast;
      } catch (err: any) {
        if (err?.message?.includes('Quota limit exceeded') || err?.code === 'resource-exhausted') {
          this.markFirebaseQuotaExceeded();
        }
      }
    }

    // 4. Fallback to Supabase
    try {
      const supaPast = await SupabaseDbService.getPastQuestions();
      if (supaPast && supaPast.length > 0) return supaPast;
    } catch (e) {}

    // 5. Final fallback to Local PC server
    return this.getLocalPastQuestions();
  }

  private async getLocalPastQuestions(): Promise<QuestionItem[]> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/past-exams` : '/api/past-exams';
      const res = await safeJsonFetch<{ questions: QuestionItem[] }>(endpoint);
      if (res.ok && res.data?.questions) {
        return res.data.questions;
      }
    } catch (e) {}
    return [];
  }

  /**
   * Multi-Write / Parallel Sync:
   * "Lütfen tüm sistemlerin kayıtların veritabanını ayrıca sparka da ekle"
   * Saves to local PC, Supabase, AND mirrors to Firebase Spark plan!
   */
  public async saveQuestion(question: QuestionItem): Promise<void> {
    const promises: Promise<any>[] = [];

    // 1. Local PC Express API
    promises.push(
      (async () => {
        try {
          const customUrl = getCustomApiUrl();
          const endpoint = customUrl ? `${customUrl}/api/questions/${question.id}` : `/api/questions/${question.id}`;
          await safeJsonFetch(endpoint, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(question),
          });
        } catch (e) {
          console.warn('[MultiDbManager] Local server saveQuestion fallback', e);
        }
      })()
    );

    // 2. Supabase
    promises.push(
      (async () => {
        try {
          await SupabaseDbService.saveQuestion(question);
        } catch (e) {
          console.warn('[MultiDbManager] Supabase saveQuestion error', e);
        }
      })()
    );

    // 3. Firebase Spark (Mirror / Dual Write)
    promises.push(
      (async () => {
        try {
          await FirestoreDbService.saveQuestion(question);
        } catch (e: any) {
          if (e?.message?.includes('Quota limit exceeded')) {
            this.markFirebaseQuotaExceeded();
          }
          console.warn('[MultiDbManager] Firebase Spark saveQuestion mirror warning', e?.message);
        }
      })()
    );

    await Promise.allSettled(promises);
  }

  /**
   * Multi-Write / Parallel Sync for Past Exam Questions:
   * Saves to Local Server, Supabase, AND mirrors to Firebase Spark!
   */
  public async savePastQuestion(question: QuestionItem): Promise<void> {
    const promises: Promise<any>[] = [];

    // 1. Local Server Express API
    promises.push(
      (async () => {
        try {
          const customUrl = getCustomApiUrl();
          const endpoint = customUrl ? `${customUrl}/api/past-exams/${question.id}` : `/api/past-exams/${question.id}`;
          await safeJsonFetch(endpoint, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(question),
          });
        } catch (e) {
          console.warn('[MultiDbManager] Local server savePastQuestion fallback', e);
        }
      })()
    );

    // 2. Supabase
    promises.push(
      (async () => {
        try {
          await SupabaseDbService.savePastQuestion(question);
        } catch (e) {
          console.warn('[MultiDbManager] Supabase savePastQuestion error', e);
        }
      })()
    );

    // 3. Firebase Spark (Mirror / Dual Write)
    promises.push(
      (async () => {
        try {
          await FirestoreDbService.updatePastQuestion(question);
        } catch (e: any) {
          if (e?.message?.includes('Quota limit exceeded')) {
            this.markFirebaseQuotaExceeded();
          }
          console.warn('[MultiDbManager] Firebase Spark savePastQuestion mirror warning', e?.message);
        }
      })()
    );

    await Promise.allSettled(promises);
  }

  /**
   * Multi-Write for Committees
   */
  public async saveCommittee(committee: Committee): Promise<void> {
    const promises: Promise<any>[] = [];

    // 1. Supabase
    promises.push(
      (async () => {
        try {
          await SupabaseDbService.saveCommittee(committee);
        } catch (e) {
          console.warn('[MultiDbManager] Supabase saveCommittee error', e);
        }
      })()
    );

    // 2. Firebase Spark
    promises.push(
      (async () => {
        try {
          await FirestoreDbService.createCommittee(committee);
        } catch (e: any) {
          if (e?.message?.includes('Quota limit exceeded')) {
            this.markFirebaseQuotaExceeded();
          }
          console.warn('[MultiDbManager] Firebase Spark saveCommittee mirror warning', e?.message);
        }
      })()
    );

    await Promise.allSettled(promises);
  }
}

export const multiDbManager = new MultiDbManager();
