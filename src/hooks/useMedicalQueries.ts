import { useQuery } from '@tanstack/react-query';
import { ApiService } from '../services/api';
import { multiDbManager } from '../services/multiDbManager';
import { LectureNote } from '../types';

/** Filtre yardımcısı: Şablon yapay zeka cümleleri içeren eski mock notları eler */
export const isPureVerbatimNote = (note: LectureNote): boolean => {
  if (!note || !Array.isArray(note.pages) || note.pages.length === 0) return false;
  return !note.pages.some(p => 
    p.content?.includes('• Temel Tanım ve Kavram:') || 
    p.content?.includes('• Patogenetik Mekanizma & Not:') ||
    p.content?.includes('• Önemli Slayt Maddeleri:')
  );
};

export interface TranscriptionMeta {
  id: string;
  fileName: string;
  title: string;
  discipline: string;
  committeeId: string;
  charCount: number;
  wordCount: number;
  estimatedMinutes: number;
  sectionsCount: number;
  firstSnippet: string;
}

export interface TranscriptionDetail extends TranscriptionMeta {
  content: string;
  sections: Array<{
    title: string;
    level: number;
    content: string;
  }>;
}

/**
 * Transkripsiyon listesi sorgusu.
 * Sayfa geçişlerinde bellekte tutulur, 10 dakika boyunca ağ isteği atmaz.
 */
export function useTranscriptionsQuery() {
  return useQuery<TranscriptionMeta[]>({
    queryKey: ['transcriptions'],
    queryFn: async () => {
      const res = await fetch('/api/transcriptions');
      if (!res.ok) throw new Error('Transkripsiyonlar alınamadı');
      const data = await res.json();
      return data.success && Array.isArray(data.transcriptions) ? data.transcriptions : [];
    },
    staleTime: 1000 * 60 * 10, // 10 dakika
  });
}

/**
 * Tekil transkripsiyon detay sorgusu.
 * Açılan detaylar 30 dakika önbellekte kalır; tekrar tıklandığında anında bellekten döner.
 */
export function useTranscriptionDetailQuery(id: string | null | undefined) {
  return useQuery<TranscriptionDetail | null>({
    queryKey: ['transcription-detail', id],
    queryFn: async () => {
      if (!id) return null;
      const res = await fetch(`/api/transcriptions/${encodeURIComponent(id)}`);
      if (!res.ok) throw new Error('Detay yüklenemedi');
      const data = await res.json();
      return data.success && data.transcription ? data.transcription : null;
    },
    enabled: Boolean(id),
    staleTime: 1000 * 60 * 30, // 30 dakika
  });
}

/**
 * Cevabı belirsiz soru anket bilgisi sorgusu (PastExamsView).
 * 60 saniye staleTime ve 60 saniye arka plan kontrolü ile yönetilir.
 */
export function useAnswerDoubtfulQuery() {
  return useQuery({
    queryKey: ['answer-doubtful'],
    queryFn: () => ApiService.getAnswerDoubtful(),
    staleTime: 1000 * 60, // 1 dakika
    refetchInterval: 1000 * 60,
  });
}

/**
 * AI İnceleme Kuyruğu sorgusu (PastExamsView).
 * 90 saniye staleTime ve 90 saniye arka plan kontrolü ile yönetilir.
 */
export function useAiReviewQueueQuery() {
  return useQuery({
    queryKey: ['ai-review-queue'],
    queryFn: () => ApiService.getAiReviewQueue(),
    staleTime: 1000 * 90, // 1.5 dakika
    refetchInterval: 1000 * 90,
  });
}

/**
 * Ders notları sorgusu (LectureNotesView).
 * Supabase ve yerel fallback ile önbelleğe alınır.
 */
export function useLectureNotesQuery() {
  return useQuery<LectureNote[]>({
    queryKey: ['lectureNotes'],
    queryFn: async () => {
      // 1. Supabase / MultiDb
      try {
        const loaded = await multiDbManager.getLectureNotes();
        if (Array.isArray(loaded) && loaded.length > 0) {
          const valid = loaded.filter(isPureVerbatimNote);
          if (valid.length > 0) return valid;
        }
      } catch (e) {
        console.warn('[useLectureNotesQuery] multiDbManager error:', e);
      }

      // 2. Local API Fallback
      const apiBase = (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_custom_api_url') : '') || '';
      const res = await fetch(`${apiBase}/api/lecture-notes`);
      if (!res.ok) return [];
      const json = await res.json();
      const list = (json.notes || json) as LectureNote[];
      return Array.isArray(list) ? list.filter(isPureVerbatimNote) : [];
    },
    staleTime: 1000 * 60 * 10, // 10 dakika
  });
}

/**
 * Kalite Denetim Durumu sorgusu (LocalAiChatView).
 */
export function useQualityAuditStatusQuery() {
  return useQuery({
    queryKey: ['qualityAuditStatus'],
    queryFn: () => ApiService.getQualityAuditStatus(),
    staleTime: 1000 * 60 * 3, // 3 dakika
  });
}

/**
 * Yapay Zekâ Hata Günlükleri sorgusu (LocalAiChatView).
 */
export function useAiErrorLogsQuery() {
  return useQuery({
    queryKey: ['aiErrorLogs'],
    queryFn: () => ApiService.getAiErrorLogs(),
    staleTime: 1000 * 60 * 2, // 2 dakika
  });
}
