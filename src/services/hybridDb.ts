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
import { multiDbManager } from './multiDbManager';

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

  // Parallel / Resilient Fetch for Committees (Delegates to MultiDbManager)
  async getCommittees(): Promise<Committee[]> {
    return await multiDbManager.getCommittees();
  },

  // Parallel / Resilient Fetch for Past Questions (Delegates to MultiDbManager)
  async getPastQuestions(): Promise<QuestionItem[]> {
    return await multiDbManager.getPastQuestions();
  },

  // Parallel / Resilient Fetch for Lecture Notes (Delegates to MultiDbManager)
  async getLectureNotes(): Promise<LectureNote[]> {
    return await multiDbManager.getLectureNotes();
  },
};
