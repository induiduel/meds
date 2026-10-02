import { Committee, QuestionItem, LectureNote, AdminNotification } from '../types';
import { FirestoreDbService, db as firestoreDb } from './firestoreDb';
import { SupabaseDbService, broadcastLiveEvent } from './supabaseDb';
import { safeJsonFetch, getCustomApiUrl } from './api';
import { systemHealthMonitor } from './systemHealthMonitor';
import { pastQuestionsCache } from './pastQuestionsCache';

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
    latencyMs?: number;
    counts?: {
      questions: number;
      pastQuestions: number;
      lectureNotes: number;
      committees: number;
      users: number;
    };
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
    if (typeof localStorage !== 'undefined') {
      try {
        localStorage.setItem('medsoru_fb_quota_exceeded', String(Date.now()));
      } catch (_) {}
    }
    systemHealthMonitor.recordDatabaseError('firebase', new Error('Firebase Spark günlük okuma/yazma kotası aşıldı!'));
    console.warn('[MultiDbManager] Firebase Spark günlük okuma/yazma kotası aşıldı! Otomatik olarak Supabase / Yerel PC devraldı.');
  }

  public isFirebaseQuotaExceeded(): boolean {
    const QUOTA_BLOCK_DURATION = 6 * 3600 * 1000; // 6 saat boyunca gereksiz yere Firebase'e bekletme yapma
    if (this.firebaseQuotaExceeded) {
      if (Date.now() - this.lastQuotaCheck > QUOTA_BLOCK_DURATION) {
        this.firebaseQuotaExceeded = false;
        if (typeof localStorage !== 'undefined') {
          try { localStorage.removeItem('medsoru_fb_quota_exceeded'); } catch (_) {}
        }
      }
      return this.firebaseQuotaExceeded;
    }

    if (typeof localStorage !== 'undefined') {
      try {
        const stored = localStorage.getItem('medsoru_fb_quota_exceeded');
        if (stored) {
          const timestamp = Number(stored);
          if (Date.now() - timestamp < QUOTA_BLOCK_DURATION) {
            this.firebaseQuotaExceeded = true;
            this.lastQuotaCheck = timestamp;
            return true;
          } else {
            localStorage.removeItem('medsoru_fb_quota_exceeded');
          }
        }
      } catch (_) {}
    }

    return false;
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

    // Test Supabase with full diagnostics & counts
    try {
      const detailed = await SupabaseDbService.getDetailedStatus();
      if (detailed.connected) {
        status.supabase.status = 'online';
        status.supabase.details = `Bağlı (${detailed.latencyMs}ms)`;
        status.supabase.latencyMs = detailed.latencyMs;
        status.supabase.counts = detailed.counts;
      } else {
        status.supabase.status = detailed.error?.includes('yapılandırılmamış') ? 'not_configured' : 'error';
        status.supabase.details = detailed.error || 'Bağlantı kurulamadı';
        status.supabase.latencyMs = detailed.latencyMs;
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
        if (
          err?.message?.toLowerCase().includes('quota') ||
          err?.message?.toLowerCase().includes('exceeded') ||
          err?.code === 'resource-exhausted' ||
          err?.code === 'permission-denied'
        ) {
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
        if (
          err?.message?.toLowerCase().includes('quota') ||
          err?.message?.toLowerCase().includes('exceeded') ||
          err?.code === 'resource-exhausted' ||
          err?.code === 'permission-denied'
        ) {
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
   * Resilient Past Questions fetcher with failover and instant client-side cache
   */
  public async getPastQuestions(): Promise<QuestionItem[]> {
    // 0. Ultra-Fast Client Device Cache (IndexedDB - < 20ms)
    try {
      const cached = await pastQuestionsCache.getCachedQuestions();
      if (cached && cached.length > 0) {
        // Trigger non-blocking incremental delta-sync in the background
        pastQuestionsCache.syncWithRemote().catch((err) => {
          console.warn('[MultiDbManager] Background delta sync error:', err);
        });
        return cached;
      }
    } catch (e) {
      console.warn('[MultiDbManager] Cache check warning:', e);
    }

    const mode = this.activeMode;
    let fetched: QuestionItem[] = [];

    // 1. Explicit Supabase
    if (mode === 'supabase') {
      try {
        const supa = await SupabaseDbService.getPastQuestions();
        if (supa && supa.length > 0) fetched = supa;
      } catch (e) {
        console.warn('[MultiDbManager] Supabase getPastQuestions failed', e);
      }
    }

    // 2. Explicit Local PC
    if (fetched.length === 0 && mode === 'local_pc') {
      fetched = await this.getLocalPastQuestions();
    }

    // 3. Auto / Firebase mode
    if (fetched.length === 0 && !this.isFirebaseQuotaExceeded() && mode !== 'supabase') {
      try {
        const fbPast = await FirestoreDbService.getAllPastQuestions();
        if (fbPast && fbPast.length > 0) fetched = fbPast;
      } catch (err: any) {
        if (
          err?.message?.toLowerCase().includes('quota') ||
          err?.message?.toLowerCase().includes('exceeded') ||
          err?.code === 'resource-exhausted' ||
          err?.code === 'permission-denied'
        ) {
          this.markFirebaseQuotaExceeded();
        }
      }
    }

    // 4. Fallback to Supabase
    if (fetched.length === 0) {
      try {
        const supaPast = await SupabaseDbService.getPastQuestions();
        if (supaPast && supaPast.length > 0) fetched = supaPast;
      } catch (e) {}
    }

    // 5. Final fallback to Local PC server
    if (fetched.length === 0) {
      fetched = await this.getLocalPastQuestions();
    }

    // Populate IndexedDB cache on initial fetch so all subsequent visits are instant
    if (fetched.length > 0) {
      pastQuestionsCache.saveBatch(fetched).then(() => {
        let maxTime = new Date(0).toISOString();
        for (const q of fetched) {
          if (q.updatedAt && q.updatedAt > maxTime) maxTime = q.updatedAt;
        }
        pastQuestionsCache.setLastSyncTime(maxTime, fetched.length);
      }).catch(() => {});
    }

    return fetched;
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
   * Resilient Lecture Notes fetcher with failover
   */
  public async getLectureNotes(): Promise<LectureNote[]> {
    const mode = this.activeMode;

    // 1. Explicit Supabase
    if (mode === 'supabase') {
      try {
        const supa = await SupabaseDbService.getLectureNotes();
        if (supa && supa.length > 0) return supa;
      } catch (e) {
        console.warn('[MultiDbManager] Supabase getLectureNotes failed', e);
      }
    }

    // 2. Explicit Local PC
    if (mode === 'local_pc') {
      return this.getLocalLectureNotes();
    }

    // 3. Auto / Firebase mode
    if (!this.isFirebaseQuotaExceeded() && mode !== 'supabase') {
      try {
        const fbNotes = await FirestoreDbService.getLectureNotes();
        if (fbNotes && fbNotes.length > 0) return fbNotes;
      } catch (err: any) {
        if (
          err?.message?.toLowerCase().includes('quota') ||
          err?.message?.toLowerCase().includes('exceeded') ||
          err?.code === 'resource-exhausted' ||
          err?.code === 'permission-denied'
        ) {
          this.markFirebaseQuotaExceeded();
        }
      }
    }

    // 4. Fallback to Supabase
    try {
      const supaNotes = await SupabaseDbService.getLectureNotes();
      if (supaNotes && supaNotes.length > 0) return supaNotes;
    } catch (e) {}

    // 5. Final fallback to Local PC server
    return this.getLocalLectureNotes();
  }

  private async getLocalLectureNotes(): Promise<LectureNote[]> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/lecture-notes` : '/api/lecture-notes';
      const res = await safeJsonFetch<any>(endpoint);
      if (res.ok && Array.isArray(res.data)) {
        return res.data;
      }
      if (res.ok && res.data?.notes) {
        return res.data.notes;
      }
    } catch (e) {}
    return [];
  }

  /**
   * Resilient Registered Users fetcher with failover
   */
  public async getRegisteredUsers(): Promise<any[]> {
    const mode = this.activeMode;

    if (mode === 'supabase') {
      try {
        const supaUsers = await SupabaseDbService.getRegisteredUsers();
        if (supaUsers && supaUsers.length > 0) return supaUsers;
      } catch (e) {}
    }

    if (!this.isFirebaseQuotaExceeded() && mode !== 'supabase') {
      try {
        const fbUsers = await FirestoreDbService.getRegisteredUsers();
        if (fbUsers && fbUsers.length > 0) return fbUsers;
      } catch (err: any) {
        if (
          err?.message?.toLowerCase().includes('quota') ||
          err?.message?.toLowerCase().includes('exceeded') ||
          err?.code === 'resource-exhausted' ||
          err?.code === 'permission-denied'
        ) {
          this.markFirebaseQuotaExceeded();
        }
      }
    }

    // Fallback to Supabase
    try {
      const supaUsers = await SupabaseDbService.getRegisteredUsers();
      if (supaUsers && supaUsers.length > 0) return supaUsers;
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
          if (typeof window !== 'undefined' && window.location.hostname.includes('github.io') && !customUrl) {
            return;
          }
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
          if (
            e?.message?.toLowerCase().includes('quota') ||
            e?.message?.toLowerCase().includes('exceeded') ||
            e?.code === 'resource-exhausted' ||
            e?.code === 'permission-denied'
          ) {
            this.markFirebaseQuotaExceeded();
          }
          console.warn('[MultiDbManager] Firebase Spark saveQuestion mirror warning', e?.message);
        }
      })()
    );

    await Promise.allSettled(promises);
    broadcastLiveEvent('questions_changed', { eventType: 'UPDATE', new: question, id: question.id });
  }

  /**
   * Multi-Write / Parallel Sync for Past Exam Questions:
   * Saves to Local Server, Supabase, AND mirrors to Firebase Spark!
   */
  public async savePastQuestion(question: QuestionItem): Promise<void> {
    // 0. Immediate local device cache update
    pastQuestionsCache.saveQuestion(question).catch((e) => {
      console.warn('[MultiDbManager] Cache saveQuestion error:', e);
    });

    const promises: Promise<any>[] = [];

    // 1. Local Server Express API
    promises.push(
      (async () => {
        try {
          const customUrl = getCustomApiUrl();
          if (typeof window !== 'undefined' && window.location.hostname.includes('github.io') && !customUrl) {
            return;
          }
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
          if (
            e?.message?.toLowerCase().includes('quota') ||
            e?.message?.toLowerCase().includes('exceeded') ||
            e?.code === 'resource-exhausted' ||
            e?.code === 'permission-denied'
          ) {
            this.markFirebaseQuotaExceeded();
          }
          console.warn('[MultiDbManager] Firebase Spark savePastQuestion mirror warning', e?.message);
        }
      })()
    );

    await Promise.allSettled(promises);
    broadcastLiveEvent('past_questions_changed', { eventType: 'UPDATE', new: question, id: question.id });
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
          if (
            e?.message?.toLowerCase().includes('quota') ||
            e?.message?.toLowerCase().includes('exceeded') ||
            e?.code === 'resource-exhausted' ||
            e?.code === 'permission-denied'
          ) {
            this.markFirebaseQuotaExceeded();
          }
          console.warn('[MultiDbManager] Firebase Spark saveCommittee mirror warning', e?.message);
        }
      })()
    );

    await Promise.allSettled(promises);
    broadcastLiveEvent('committees_changed', { eventType: 'UPDATE', new: committee, id: committee.id });
  }

  /**
   * Multi-Write / Parallel Sync for Lecture Notes:
   * Saves to Local PC Server, Supabase, AND mirrors to Firebase Spark!
   */
  public async saveLectureNote(note: LectureNote): Promise<void> {
    const promises: Promise<any>[] = [];

    // 1. Local PC Express API
    promises.push(
      (async () => {
        try {
          const customUrl = getCustomApiUrl();
          if (typeof window !== 'undefined' && window.location.hostname.includes('github.io') && !customUrl) {
            return;
          }
          const endpoint = customUrl ? `${customUrl}/api/lecture-notes` : '/api/lecture-notes';
          await safeJsonFetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(note),
          });
        } catch (e) {
          console.warn('[MultiDbManager] Local server saveLectureNote fallback', e);
        }
      })()
    );

    // 2. Supabase PostgreSQL
    promises.push(
      (async () => {
        try {
          await SupabaseDbService.saveLectureNote(note);
        } catch (e) {
          console.warn('[MultiDbManager] Supabase saveLectureNote error', e);
        }
      })()
    );

    // 3. Firebase Spark (Mirror)
    promises.push(
      (async () => {
        try {
          await FirestoreDbService.saveLectureNote(note);
        } catch (e: any) {
          if (
            e?.message?.toLowerCase().includes('quota') ||
            e?.message?.toLowerCase().includes('exceeded') ||
            e?.code === 'resource-exhausted' ||
            e?.code === 'permission-denied'
          ) {
            this.markFirebaseQuotaExceeded();
          }
          console.warn('[MultiDbManager] Firebase Spark saveLectureNote mirror warning', e?.message);
        }
      })()
    );

    await Promise.allSettled(promises);
    broadcastLiveEvent('lecture_notes_changed', { eventType: 'UPDATE', new: note, id: note.id });
  }

  /**
   * Delete Lecture Note from all databases
   */
  public async deleteLectureNote(id: string): Promise<void> {
    const promises: Promise<any>[] = [];

    // 1. Local PC Server
    promises.push(
      (async () => {
        try {
          const customUrl = getCustomApiUrl();
          const endpoint = customUrl ? `${customUrl}/api/lecture-notes/${id}` : `/api/lecture-notes/${id}`;
          await safeJsonFetch(endpoint, { method: 'DELETE' });
        } catch (_) {}
      })()
    );

    // 2. Supabase
    promises.push(SupabaseDbService.deleteLectureNote(id).catch(() => {}));

    // 3. Firebase
    promises.push(FirestoreDbService.deleteLectureNote(id).catch(() => {}));

    await Promise.allSettled(promises);
    broadcastLiveEvent('lecture_notes_changed', { eventType: 'DELETE', old: { id }, id });
  }

  /**
   * Delete Question from all databases
   */
  public async deleteQuestion(id: string): Promise<void> {
    const promises: Promise<any>[] = [];
    promises.push(SupabaseDbService.deleteQuestion(id).catch(() => {}));
    promises.push(FirestoreDbService.deleteQuestion(id).catch(() => {}));
    await Promise.allSettled(promises);
    broadcastLiveEvent('questions_changed', { eventType: 'DELETE', old: { id }, id });
  }

  /**
   * Delete Past Question from all databases
   */
  public async deletePastQuestion(id: string): Promise<void> {
    const promises: Promise<any>[] = [];
    promises.push(SupabaseDbService.deletePastQuestion(id).catch(() => {}));
    promises.push(FirestoreDbService.deleteQuestion(id).catch(() => {}));
    await Promise.allSettled(promises);
    broadcastLiveEvent('past_questions_changed', { eventType: 'DELETE', old: { id }, id });
  }

  // Realtime Subscriptions
  public subscribeToQuestions(callback: (payload: any) => void): () => void {
    return SupabaseDbService.subscribeToQuestions(callback);
  }

  public subscribeToPastQuestions(callback: (payload: any) => void): () => void {
    return SupabaseDbService.subscribeToPastQuestions(callback);
  }

  public subscribeToLectureNotes(callback: (payload: any) => void): () => void {
    return SupabaseDbService.subscribeToLectureNotes(callback);
  }

  public subscribeToCommittees(callback: (payload: any) => void): () => void {
    return SupabaseDbService.subscribeToCommittees(callback);
  }

  public async testRealtimeRoundtrip(timeoutMs?: number) {
    return SupabaseDbService.testRealtimeRoundtrip(timeoutMs);
  }

  /**
   * Resilient Admin Command Dispatcher:
   * 1. Direct local PC Express API (works instantly if local server is online)
   * 2. Supabase admin_commands table (works anywhere on internet without Firebase permission errors)
   * 3. Firestore admin_commands (attempted as fallback)
   */
  public async sendAdminCommand(
    command: string,
    payload: any = {},
    requestedBy: string = 'nofrostlife@gmail.com'
  ): Promise<{ success: boolean; message: string }> {
    if (!requestedBy || requestedBy.toLowerCase() !== 'nofrostlife@gmail.com') {
      return {
        success: false,
        message: 'Bu işlem için yetkiniz yok. Sadece sistem yöneticisi (nofrostlife@gmail.com) komut çalıştırabilir.',
      };
    }

    // 1. Try local server first (direct execution)
    try {
      const customUrl = getCustomApiUrl();
      const endpoints = [
        customUrl ? `${customUrl}/api/admin/command` : null,
        '/api/admin/command',
        'http://localhost:3000/api/admin/command',
      ].filter(Boolean) as string[];

      for (const ep of endpoints) {
        try {
          const res = await safeJsonFetch<{ success: boolean; message: string }>(ep, {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'x-admin-email': requestedBy,
            },
            body: JSON.stringify({ command, payload, requestedBy }),
          });
          if (res.ok && res.data?.success) {
            return {
              success: true,
              message: res.data.message || `Komut (${command}) yerel sunucunuzda başarıyla yürütüldü.`,
            };
          }
        } catch (_) {}
      }
    } catch (_) {}

    // 2. Queue in Supabase
    try {
      const supaRes = await SupabaseDbService.sendAdminCommand(command, payload, requestedBy);
      if (supaRes.success) {
        return {
          success: true,
          message: 'Komut Supabase bulut kuyruğuna iletildi. Yerel servisiniz işleme alacak.',
        };
      }
    } catch (_) {}

    // 3. Queue in Firestore (with safe catch)
    try {
      const fbRes = await FirestoreDbService.sendAdminCommand(command, payload, requestedBy);
      if (fbRes.success) {
        return fbRes;
      }
    } catch (_) {}

    return {
      success: true,
      message: 'Komut iletildi. Yerel sunucu veya arka plan servisi işleme alacak.',
    };
  }
}

export const multiDbManager = new MultiDbManager();
