/**
 * MedSoru Hibrit Veritabanı & Kota Koruma Servisi (hybridDb.ts)
 * 
 * Bu servis:
 * 1. Firebase Firestore ve Yerel PC Veritabanını paralel olarak yönetir.
 * 2. Firebase kotası tükendiğinde (RESOURCE_EXHAUSTED / 429) otomatik olarak
 *    kullanıcının yerel bilgisayarına (port 3000 veya Tünel URL'sine) yönlenir.
 * 3. Böylece site asla çökmeyip sınırsız ve ücretsiz çalışmaya devam eder.
 */

import { QuestionItem, Committee, LectureNote } from '../types';
import { FirestoreDbService } from './firestoreDb';
import { safeJsonFetch, getCustomApiUrl } from './api';

export type HybridDbMode = 'auto' | 'local_first' | 'cloud_only';

const HYBRID_MODE_KEY = 'medsoru_hybrid_mode';

export function getHybridMode(): HybridDbMode {
  return (localStorage.getItem(HYBRID_MODE_KEY) as HybridDbMode) || 'auto';
}

export function setHybridMode(mode: HybridDbMode) {
  localStorage.setItem(HYBRID_MODE_KEY, mode);
}

// Checks if an error is a Firebase quota or network failure
export function isFirebaseQuotaExceeded(error: any): boolean {
  if (!error) return false;
  const msg = String(error.message || error.code || error).toLowerCase();
  return (
    msg.includes('resource-exhausted') ||
    msg.includes('quota') ||
    msg.includes('rate-limit') ||
    msg.includes('exceeded') ||
    msg.includes('too many requests') ||
    msg.includes('unavailable')
  );
}

export const HybridDbService = {
  // Get best API base URL (custom tunnel or local server)
  getBaseUrl(): string {
    const custom = getCustomApiUrl();
    if (custom) return custom;
    if (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
      return '';
    }
    return '';
  },

  // Parallel / Resilient Fetch for Committees
  async getCommittees(): Promise<Committee[]> {
    const mode = getHybridMode();

    if (mode === 'local_first') {
      const localRes = await safeJsonFetch<any>(`${this.getBaseUrl()}/api/committees`);
      if (localRes.ok && localRes.data?.committees) {
        return localRes.data.committees;
      }
    }

    try {
      const cloudData = await FirestoreDbService.getCommittees();
      if (cloudData && cloudData.length > 0) return cloudData;
    } catch (err: any) {
      if (isFirebaseQuotaExceeded(err)) {
        console.warn('⚠️ [HybridDB] Firebase kotası aşıldı! Yerel PC veritabanına geçiliyor.');
      }
    }

    // Fallback to local server
    const localRes = await safeJsonFetch<any>(`${this.getBaseUrl()}/api/committees`);
    if (localRes.ok && localRes.data?.committees) {
      return localRes.data.committees;
    }

    return FirestoreDbService.getCommittees();
  },

  // Parallel / Resilient Fetch for Past Questions
  async getPastQuestions(): Promise<QuestionItem[]> {
    const mode = getHybridMode();

    if (mode === 'local_first') {
      const localRes = await safeJsonFetch<any>(`${this.getBaseUrl()}/api/past-exams`);
      if (localRes.ok && localRes.data?.questions) {
        return localRes.data.questions;
      }
    }

    try {
      const cloudData = await FirestoreDbService.getAllPastQuestions();
      if (cloudData && cloudData.length > 0) return cloudData;
    } catch (err: any) {
      if (isFirebaseQuotaExceeded(err)) {
        console.warn('⚠️ [HybridDB] Firebase kotası aşıldı! Yerel PC veritabanından sorular getiriliyor.');
      }
    }

    // Fallback to local server
    const localRes = await safeJsonFetch<any>(`${this.getBaseUrl()}/api/past-exams`);
    if (localRes.ok && localRes.data?.questions) {
      return localRes.data.questions;
    }

    // Static fallback
    try {
      const staticData = await import('../data/pastQuestions.json');
      return (staticData.default || staticData) as QuestionItem[];
    } catch (_) {}

    return [];
  },

  // Parallel / Resilient Fetch for Lecture Notes
  async getLectureNotes(): Promise<LectureNote[]> {
    const mode = getHybridMode();

    if (mode === 'local_first') {
      const localRes = await safeJsonFetch<any>(`${this.getBaseUrl()}/api/lecture-notes`);
      if (localRes.ok && localRes.data?.notes) {
        return localRes.data.notes;
      }
    }

    try {
      const cloudData = await FirestoreDbService.getLectureNotes();
      if (cloudData && cloudData.length > 0) return cloudData;
    } catch (err: any) {
      if (isFirebaseQuotaExceeded(err)) {
        console.warn('⚠️ [HybridDB] Firebase kotası aşıldı! Yerel PC ders notlarına geçiliyor.');
      }
    }

    // Fallback to local server
    const localRes = await safeJsonFetch<any>(`${this.getBaseUrl()}/api/lecture-notes`);
    if (localRes.ok && localRes.data?.notes) {
      return localRes.data.notes;
    }

    // Static fallback
    try {
      const staticData = await import('../data/lecture_notes.json');
      return (staticData.default || staticData) as LectureNote[];
    } catch (_) {}

    return [];
  }
};
