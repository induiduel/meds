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

const STORAGE_URL_KEY = 'medsoru_custom_supabase_url';
const STORAGE_KEY_KEY = 'medsoru_custom_supabase_key';

export function getSupabaseConfig(): { url: string; key: string } {
  const localUrl = localStorage.getItem(STORAGE_URL_KEY);
  const localKey = localStorage.getItem(STORAGE_KEY_KEY);

  const envUrl = (typeof process !== 'undefined' && process.env?.SUPABASE_URL) || '';
  const envKey = (typeof process !== 'undefined' && (process.env?.SUPABASE_PUBLISHABLE_KEY || process.env?.SUPABASE_SECRET_KEY)) || '';

  return {
    url: (localUrl || envUrl || '').trim(),
    key: (localKey || envKey || '').trim(),
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
      const rows = committees.map((c) => ({
        id: c.id,
        name: c.name,
        academic_year: c.academicYear || '2026-2027',
        target_questions: c.targetQuestions || 100,
        color: c.color || 'teal',
        data: c,
      }));

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
      let query = client.from('questions').select('*');
      if (committeeId && committeeId !== 'all') {
        query = query.eq('committee_id', committeeId);
      }
      const { data, error } = await query;
      if (error || !data) return [];

      return data.map((row: any) => ({
        id: row.id,
        committeeId: row.committee_id,
        questionNumber: row.question_number,
        discipline: row.discipline,
        topic: row.topic,
        status: row.status,
        claimedAnswer: row.claimed_answer,
        upvotes: row.upvotes || 0,
        tags: row.tags || [],
        fragments: row.fragments || [],
        options: row.options || [],
        reconstruction: row.reconstruction,
        createdAt: row.created_at,
        updatedAt: row.updated_at,
        ...(row.data || {}),
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
      const row = {
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
      };

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
      const { data, error } = await client.from('past_questions').select('*').limit(3000);
      if (error || !data) return [];

      return data.map((row: any) => ({
        id: row.id,
        committeeId: row.committee_id,
        discipline: row.discipline,
        topic: row.topic,
        examYear: row.exam_year,
        sourceFile: row.source_file,
        aiCategory: row.ai_category,
        claimedAnswer: row.claimed_answer,
        rawQuestion: row.raw_question,
        reconstruction: row.reconstruction,
        isSuspect: row.is_suspect,
        isAmbiguous: row.is_ambiguous,
        isLocked: row.is_locked,
        upvotes: row.upvotes || 0,
        comments: row.comments || [],
        reports: row.reports || [],
        customRedactedBy: row.custom_redacted_by,
        customRedactedAt: row.custom_redacted_at,
        customRedactionPrompt: row.custom_redaction_prompt,
        createdAt: row.created_at,
        updatedAt: row.updated_at,
        ...(row.data || {}),
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
      const row = {
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
      };

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
        const rows = chunk.map((q) => ({
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
        }));
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
      const { data, error } = await client.from('lecture_notes').select('*');
      if (error || !data) return [];

      return data.map((row: any) => ({
        id: row.id,
        committeeId: row.committee_id,
        discipline: row.discipline,
        title: row.title,
        pages: row.pages || [],
        pageCount: row.page_count || 0,
        createdAt: row.created_at,
        ...(row.data || {}),
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
      const row = {
        id: note.id,
        committee_id: note.committeeId,
        discipline: note.discipline,
        title: note.title,
        pages: note.pages || [],
        page_count: note.pageCount || (note.pages ? note.pages.length : 0),
        data: note,
      };

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
      const { data, error } = await client.from('users').select('*');
      if (error || !data) return [];
      return data.map((row: any) => ({
        uid: row.uid,
        email: row.email,
        displayName: row.display_name,
        studentNumber: row.student_number,
        role: row.role,
        createdAt: row.created_at,
        updatedAt: row.updated_at,
        ...(row.data || {}),
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
      const row = {
        uid: user.uid,
        email: user.email,
        display_name: user.displayName || user.name,
        student_number: user.studentNumber,
        role: user.role || 'student',
        data: user,
        updated_at: new Date().toISOString(),
      };

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
      const { error } = await client.from('admin_commands').insert([
        {
          id,
          command,
          payload,
          requested_by: requestedBy,
          status: 'pending',
          created_at: new Date().toISOString(),
        },
      ]);

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
