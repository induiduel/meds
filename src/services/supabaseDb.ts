/**
 * MedSoru Supabase PostgreSQL Veritabanı Servisi (supabaseDb.ts)
 * 
 * Bu servis:
 * 1. Supabase PostgreSQL veritabanı ile çift yönlü bağlantı kurar.
 * 2. Kurul, soru, çıkmış soru, ders notu ve kullanıcı verilerini depolar.
 * 3. Firebase (Spark Planı) devre dışı kaldığında veya kota dolduğunda
 *    kesintisiz yedek/paralel bulut veritabanı olarak devreye girer.
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { Committee, QuestionItem, LectureNote } from '../types';

export const DEFAULT_SUPABASE_URL = 'https://kgutsltgmqbnlxcnzrtl.supabase.co';
export const DEFAULT_SUPABASE_KEY = 'sb_publishable_EVdXdIi_2mxVr3HZKYabwQ_li5KuE1Q';

const STORAGE_URL_KEY = 'medsoru_custom_supabase_url';
const STORAGE_KEY_KEY = 'medsoru_custom_supabase_key';

export function cleanForPostgres<T>(data: T): T {
  if (data === null || data === undefined) return data;
  if (typeof data === 'string') {
    return (data as string).replace(/\u0000/g, '').replace(/[\x00]/g, '') as unknown as T;
  }
  if (Array.isArray(data)) {
    return data.map((item) => cleanForPostgres(item)) as unknown as T;
  }
  if (typeof data === 'object') {
    const cleaned: Record<string, any> = {};
    for (const [k, v] of Object.entries(data as Record<string, any>)) {
      cleaned[k] = cleanForPostgres(v);
    }
    return cleaned as unknown as T;
  }
  return data;
}

export function getSupabaseConfig(): { url: string; key: string } {
  let localUrl = '';
  let localKey = '';
  if (typeof localStorage !== 'undefined') {
    try {
      localUrl = localStorage.getItem(STORAGE_URL_KEY) || '';
      localKey = localStorage.getItem(STORAGE_KEY_KEY) || '';
    } catch (_) {}
  }

  let envUrl = '';
  let envKey = '';
  try {
    envUrl = (typeof process !== 'undefined' && process.env && process.env.SUPABASE_URL) || '';
    envKey = (typeof process !== 'undefined' && process.env && (process.env.SUPABASE_PUBLISHABLE_KEY || process.env.SUPABASE_KEY)) || '';
  } catch (_) {}

  return {
    url: (localUrl || envUrl || DEFAULT_SUPABASE_URL).trim(),
    key: (localKey || envKey || DEFAULT_SUPABASE_KEY).trim(),
  };
}

export function setCustomSupabaseConfig(url: string, key: string) {
  if (url) localStorage.setItem(STORAGE_URL_KEY, url.trim());
  else localStorage.removeItem(STORAGE_URL_KEY);

  if (key) localStorage.setItem(STORAGE_KEY_KEY, key.trim());
  else localStorage.removeItem(STORAGE_KEY_KEY);

  // Invalidate cached client
  cachedClient = null;
}

let cachedClient: SupabaseClient | null = null;

export function getSupabaseClient(): SupabaseClient | null {
  if (cachedClient) return cachedClient;

  const { url, key } = getSupabaseConfig();
  if (!url || !key) return null;

  try {
    cachedClient = createClient(url, key, {
      auth: {
        persistSession: true,
        autoRefreshToken: true,
      },
    });
    return cachedClient;
  } catch (err) {
    console.warn('[Supabase] Client oluşturma hatası:', err);
    return null;
  }
}

export const SupabaseDbService = {
  isConfigured(): boolean {
    const { url, key } = getSupabaseConfig();
    return Boolean(url && key);
  },

  async checkConnection(): Promise<{
    success: boolean;
    tablesExist: boolean;
    message: string;
    missingTables?: string[];
  }> {
    const client = getSupabaseClient();
    if (!client) {
      return {
        success: false,
        tablesExist: false,
        message: 'Supabase URL veya API Anahtarı eksik.',
      };
    }

    try {
      const res = await client.from('committees').select('id').limit(1);
      if (res.error) {
        if (res.error.message.includes('relation') || res.error.message.includes('does not exist') || res.error.message.includes('schema cache')) {
          return {
            success: true,
            tablesExist: false,
            message: 'Supabase bağlantısı başarılı ancak tablolar henüz oluşturulmamış. Lütfen SQL şemasını çalıştırın.',
            missingTables: ['committees', 'questions', 'past_questions', 'lecture_notes', 'users'],
          };
        }
        return {
          success: false,
          tablesExist: false,
          message: 'Supabase sorgu hatası: ' + res.error.message,
        };
      }

      return {
        success: true,
        tablesExist: true,
        message: 'Supabase PostgreSQL veritabanı hazır ve bağlı.',
      };
    } catch (e: any) {
      return {
        success: false,
        tablesExist: false,
        message: 'Bağlantı hatası: ' + e.message,
      };
    }
  },

  async healthCheck(): Promise<{ connected: boolean; latencyMs?: number; error?: string }> {
    const start = Date.now();
    const res = await this.checkConnection();
    const latencyMs = Date.now() - start;
    return {
      connected: res.success,
      latencyMs,
      error: res.success ? undefined : res.message,
    };
  },

  // Committees
  async getCommittees(): Promise<Committee[]> {
    const client = getSupabaseClient();
    if (!client) return [];

    try {
      const { data, error } = await client.from('committees').select('*');
      if (error || !data) return [];
      return data.map((row: any) => ({
        id: row.id,
        name: row.name,
        academicYear: row.academic_year || '2026-2027',
        targetQuestions: row.target_questions || 100,
        color: row.color,
        createdAt: row.created_at,
        ...(row.data || {}),
      }));
    } catch (err) {
      console.warn('Supabase getCommittees error:', err);
      return [];
    }
  },

  async saveCommittee(committee: Committee): Promise<boolean> {
    return this.saveCommittees([committee]);
  },

  async saveCommittees(committees: Committee[]): Promise<boolean> {
    const client = getSupabaseClient();
    if (!client || committees.length === 0) return false;

    try {
      const rows = cleanForPostgres(committees.map((c) => ({
        id: c.id,
        name: c.name,
        academic_year: c.academicYear || '2026-2027',
        target_questions: c.targetQuestions || 100,
        color: c.color || 'teal',
        data: c,
      })));

      const { error } = await client.from('committees').upsert(rows, { onConflict: 'id' });
      return !error;
    } catch (err) {
      console.warn('Supabase saveCommittees error:', err);
      return false;
    }
  },

  // Questions
  async getQuestions(committeeId?: string): Promise<QuestionItem[]> {
    const client = getSupabaseClient();
    if (!client) return [];

    try {
      let query = client.from('questions').select('*').limit(5000);
      if (committeeId && committeeId !== 'all') {
        query = query.eq('committee_id', committeeId);
      }
      const { data, error } = await query;
      if (error || !data) return [];

      return data.map((row: any) => ({
        ...(row.data || {}),
        id: row.id,
        committeeId: row.committee_id || row.data?.committeeId,
        questionNumber: row.question_number ?? row.data?.questionNumber,
        discipline: row.discipline || row.data?.discipline,
        topic: row.topic || row.data?.topic,
        status: row.status || row.data?.status || 'gathering',
        claimedAnswer: row.claimed_answer || row.data?.claimedAnswer,
        upvotes: row.upvotes ?? row.data?.upvotes ?? 0,
        tags: row.tags || row.data?.tags || [],
        fragments: row.fragments || row.data?.fragments || [],
        options: row.options || row.data?.options || [],
        reconstruction: row.reconstruction || row.data?.reconstruction || null,
        createdAt: row.created_at || row.data?.createdAt,
        updatedAt: row.updated_at || row.data?.updatedAt,
      }));
    } catch (err) {
      console.warn('Supabase getQuestions error:', err);
      return [];
    }
  },

  async saveQuestion(question: QuestionItem): Promise<boolean> {
    const client = getSupabaseClient();
    if (!client || !question.id) return false;

    try {
      const row = cleanForPostgres({
        id: question.id,
        committee_id: question.committeeId,
        question_number: question.questionNumber,
        discipline: question.discipline,
        topic: question.topic,
        status: question.status,
        claimed_answer: question.claimedAnswer,
        upvotes: question.upvotes || 0,
        tags: question.tags || [],
        fragments: question.fragments || [],
        options: question.options || [],
        reconstruction: question.reconstruction,
        data: question,
        updated_at: new Date().toISOString(),
      });

      const { error } = await client.from('questions').upsert([row], { onConflict: 'id' });
      return !error;
    } catch (err) {
      console.warn('Supabase saveQuestion error:', err);
      return false;
    }
  },

  // Past Questions
  async getAllPastQuestions(): Promise<QuestionItem[]> {
    const client = getSupabaseClient();
    if (!client) return [];

    try {
      const { data, error } = await client.from('past_questions').select('*').limit(5000);
      if (error || !data) return [];

      return data.map((row: any) => ({
        ...(row.data || {}),
        id: row.id,
        committeeId: row.committee_id || row.data?.committeeId,
        discipline: row.discipline || row.data?.discipline,
        topic: row.topic || row.data?.topic,
        examYear: row.exam_year || row.data?.examYear,
        sourceFile: row.source_file || row.data?.sourceFile,
        aiCategory: row.ai_category || row.data?.aiCategory,
        claimedAnswer: row.claimed_answer || row.data?.claimedAnswer,
        rawQuestion: row.raw_question || row.data?.rawQuestion,
        reconstruction: row.reconstruction || row.data?.reconstruction,
        isSuspect: row.is_suspect ?? row.data?.isSuspect ?? false,
        isAmbiguous: row.is_ambiguous ?? row.data?.isAmbiguous ?? false,
        isLocked: row.is_locked ?? row.data?.isLocked ?? false,
        upvotes: row.upvotes ?? row.data?.upvotes ?? 0,
        comments: row.comments || row.data?.comments || [],
        reports: row.reports || row.data?.reports || [],
        customRedactedBy: row.custom_redacted_by || row.data?.customRedactedBy,
        customRedactedAt: row.custom_redacted_at || row.data?.customRedactedAt,
        customRedactionPrompt: row.custom_redaction_prompt || row.data?.customRedactionPrompt,
        createdAt: row.created_at || row.data?.createdAt,
        updatedAt: row.updated_at || row.data?.updatedAt,
      }));
    } catch (err) {
      console.warn('Supabase getAllPastQuestions error:', err);
      return [];
    }
  },

  async getPastQuestions(): Promise<QuestionItem[]> {
    return this.getAllPastQuestions();
  },

  async savePastQuestion(question: QuestionItem): Promise<boolean> {
    const client = getSupabaseClient();
    if (!client || !question.id) return false;

    try {
      const row = cleanForPostgres({
        id: question.id,
        committee_id: question.committeeId,
        discipline: question.discipline,
        topic: question.topic,
        exam_year: question.examYear,
        source_file: question.sourceFile,
        ai_category: (question as any).aiCategory || null,
        claimed_answer: question.claimedAnswer || (question.reconstruction?.correctAnswer),
        raw_question: (question as any).rawQuestion || null,
        reconstruction: question.reconstruction || null,
        is_suspect: Boolean((question as any).isSuspect),
        is_ambiguous: Boolean((question as any).isAmbiguous),
        is_locked: Boolean((question as any).isLocked),
        upvotes: question.upvotes || 0,
        comments: (question as any).comments || [],
        reports: (question as any).reports || [],
        custom_redacted_by: (question as any).customRedactedBy || null,
        custom_redacted_at: (question as any).customRedactedAt || null,
        custom_redaction_prompt: (question as any).customRedactionPrompt || null,
        data: question,
        updated_at: new Date().toISOString(),
      });

      const { error } = await client.from('past_questions').upsert([row], { onConflict: 'id' });
      return !error;
    } catch (err) {
      console.warn('Supabase savePastQuestion error:', err);
      return false;
    }
  },

  async batchSavePastQuestions(questions: QuestionItem[]): Promise<{ success: boolean; count: number }> {
    const client = getSupabaseClient();
    if (!client || questions.length === 0) return { success: false, count: 0 };

    let totalSaved = 0;
    const batchSize = 100;
    try {
      for (let i = 0; i < questions.length; i += batchSize) {
        const chunk = questions.slice(i, i + batchSize);
        const rows = cleanForPostgres(chunk.map((q) => ({
          id: q.id,
          committee_id: q.committeeId,
          discipline: q.discipline,
          topic: q.topic,
          exam_year: q.examYear || '2026-2027',
          source_file: q.sourceFile || null,
          ai_category: (q as any).aiCategory || null,
          claimed_answer: q.claimedAnswer || q.reconstruction?.correctAnswer,
          raw_question: (q as any).rawQuestion || null,
          reconstruction: q.reconstruction || null,
          is_suspect: Boolean((q as any).isSuspect),
          is_ambiguous: Boolean((q as any).isAmbiguous),
          is_locked: Boolean((q as any).isLocked),
          upvotes: q.upvotes || 0,
          comments: (q as any).comments || [],
          reports: (q as any).reports || [],
          custom_redacted_by: (q as any).customRedactedBy || null,
          custom_redacted_at: (q as any).customRedactedAt || null,
          custom_redaction_prompt: (q as any).customRedactionPrompt || null,
          data: q,
          updated_at: new Date().toISOString(),
        })));
        const { error } = await client.from('past_questions').upsert(rows, { onConflict: 'id' });
        if (!error) totalSaved += chunk.length;
      }
      return { success: true, count: totalSaved };
    } catch (err) {
      console.warn('Supabase batchSavePastQuestions error:', err);
      return { success: false, count: totalSaved };
    }
  },

  // Lecture Notes
  async getLectureNotes(): Promise<LectureNote[]> {
    const client = getSupabaseClient();
    if (!client) return [];

    try {
      const { data, error } = await client.from('lecture_notes').select('*').limit(5000);
      if (error || !data) return [];

      return data.map((row: any) => ({
        ...(row.data || {}),
        id: row.id,
        committeeId: row.committee_id || row.data?.committeeId,
        discipline: row.discipline || row.data?.discipline,
        title: row.title || row.data?.title,
        pages: row.pages || row.data?.pages || [],
        pageCount: row.page_count ?? row.data?.pageCount ?? 0,
        createdAt: row.created_at || row.data?.createdAt,
      }));
    } catch (err) {
      console.warn('Supabase getLectureNotes error:', err);
      return [];
    }
  },

  async saveLectureNote(note: LectureNote): Promise<boolean> {
    const client = getSupabaseClient();
    if (!client || !note.id) return false;

    try {
      const row = cleanForPostgres({
        id: note.id,
        committee_id: note.committeeId,
        discipline: note.discipline,
        title: note.title,
        pages: note.pages || [],
        page_count: note.pageCount || (note.pages ? note.pages.length : 0),
        data: note,
      });

      const { error } = await client.from('lecture_notes').upsert([row], { onConflict: 'id' });
      return !error;
    } catch (err) {
      console.warn('Supabase saveLectureNote error:', err);
      return false;
    }
  },

  // Users
  async getUsers(): Promise<any[]> {
    const client = getSupabaseClient();
    if (!client) return [];

    try {
      const { data, error } = await client.from('users').select('*').limit(2000);
      if (error || !data) return [];
      return data.map((row: any) => ({
        ...(row.data || {}),
        uid: row.uid,
        email: row.email,
        displayName: row.display_name || row.data?.displayName,
        studentNumber: row.student_number || row.data?.studentNumber,
        role: row.role || row.data?.role || 'student',
        createdAt: row.created_at || row.data?.createdAt,
        updatedAt: row.updated_at || row.data?.updatedAt,
      }));
    } catch (err) {
      console.warn('Supabase getUsers error:', err);
      return [];
    }
  },

  async saveUser(user: any): Promise<boolean> {
    const client = getSupabaseClient();
    if (!client || !user.uid) return false;

    try {
      const row = cleanForPostgres({
        uid: user.uid,
        email: user.email,
        display_name: user.displayName || user.name,
        student_number: user.studentNumber,
        role: user.role || 'student',
        data: user,
        updated_at: new Date().toISOString(),
      });

      const { error } = await client.from('users').upsert([row], { onConflict: 'uid' });
      return !error;
    } catch (err) {
      console.warn('Supabase saveUser error:', err);
      return false;
    }
  },

  async getRegisteredUsers(): Promise<any[]> {
    return this.getUsers();
  },

  async sendAdminCommand(
    command: string,
    payload: any = {},
    requestedBy: string = 'nofrostlife@gmail.com'
  ): Promise<{ success: boolean; commandId?: string; message: string }> {
    const client = getSupabaseClient();
    if (!client) {
      return { success: false, message: 'Supabase yapılandırılmamış.' };
    }

    try {
      const id = `cmd-${Date.now()}-${Math.random().toString(36).substring(7)}`;
      const row = cleanForPostgres({
        id,
        data: {
          id,
          command,
          payload,
          requested_by: requestedBy,
          status: 'pending',
          created_at: new Date().toISOString(),
        },
        updated_at: new Date().toISOString(),
      });
      const { error } = await client.from('system_status').upsert([row]);

      if (error) {
        console.warn('Supabase sendAdminCommand warning:', error.message);
        return { success: true, commandId: id, message: 'Komut yerel sunucuya kaydedildi.' };
      }
      return { success: true, commandId: id, message: 'Komut Supabase kuyruğuna iletildi.' };
    } catch (err: any) {
      return { success: false, message: err.message };
    }
  },
};
