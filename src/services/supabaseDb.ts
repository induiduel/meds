/**
 * MedSoru veritabanı servisi (istemci). Adı tarihsel: Supabase 2026-10-12'de kaldırıldı.
 *
 * - Okuma/yazma: `getSupabaseClient()` artık `dbRemoteClient` döner; aynı zincir biçimi sunucudaki
 *   POST /api/db/query kapısına gider (meds-pg). Tarayıcıda veritabanı adresi ya da anahtar yoktur.
 * - Canlı yayın: Postgres NOTIFY → sunucu → SSE (`realtimeEventService`). `subscribeToTable` aynı
 *   { eventType, new, old } biçimini verir; istemciden istemciye mesaj `broadcastLiveEvent` ile sunucudan geçer.
 */

import { Committee, QuestionItem, LectureNote } from '../types';
import { filterCurrent2026_2027Committees } from './firestoreDb';
import { dbRemoteClient, dbApiBase, postLiveBroadcast, postLivePing, type DbRemoteClient } from './dbRemoteClient';
import { realtimeEventService } from './realtimeEvents';

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

/** Tanılama ekranları için: veritabanı artık sunucu üzerinden (aynı köken ya da özel API adresi). */
export function getSupabaseConfig(): { url: string; key: string } {
  const base = dbApiBase();
  return { url: (base || (typeof window !== 'undefined' ? window.location.origin : '')) + '/api/db', key: 'server' };
}

/** Eski "özel Supabase adresi" ayarı artık kullanılmaz; kalıntı anahtarlar temizlenir. */
export function setCustomSupabaseConfig(_url?: string, _key?: string) {
  try {
    localStorage.removeItem('medsoru_custom_supabase_url');
    localStorage.removeItem('medsoru_custom_supabase_key');
  } catch (_) {}
}

/** Şikâyet satırları iki kaynaktan (tablo / soru içi JSON) farklı adlarla gelir; tek biçime getir */
function normalizeReportRow(r: any) {
  return {
    ...r,
    questionId: r.questionId ?? r.question_id,
    questionTopic: r.questionTopic ?? r.question_topic ?? r.topic,
    reportedBy: r.reportedBy ?? r.reported_by,
    createdAt: r.createdAt ?? r.created_at ?? r.timestamp,
  };
}

export function getSupabaseClient(): DbRemoteClient {
  return dbRemoteClient;
}

/**
 * İstemciden diğer ziyaretçilere canlı mesaj. "<tablo>_changed" olaylarında sunucu yalnız id + işlemi
 * iletir (asıl içerik veritabanı tetikleyicisinden gelir); "app:*" olayları küçük JSON mesajlardır.
 * Supabase'teki gibi gönderen kendi mesajını almaz.
 */
export function broadcastLiveEvent(event: string, payload: any) {
  void postLiveBroadcast(event, payload, realtimeEventService.getClientId());
}

/** "app:*" canlı mesajlarını dinle (ör. app:presence). Dönen işlev aboneliği kapatır. */
export function onLiveEvent(event: string, fn: (payload: any, from?: string) => void): () => void {
  return realtimeEventService.on('live', (msg: any) => {
    if (msg?.event === event) fn(msg.payload, msg.from);
  });
}

function mapRowToPastQuestion(row: any): QuestionItem {
  return {
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
  };
}

// `past_question_reports` tablosu bulutta yok (bildiren e-postaları buluta çıkmasın diye bilerek uygulanmadı; Oracle/yerel
// Supabase'de var). İlk "tablo yok" yanıtında oturum boyunca bir daha denenmez: her açılışta tekrarlanan 404'ler biter.
const REPORTS_TABLE_KEY = 'medsoru_reports_table_missing_at';
let reportsTableMissing = (() => {
  try {
    const at = Number(localStorage.getItem(REPORTS_TABLE_KEY) || 0);
    return at > 0 && Date.now() - at < 24 * 60 * 60 * 1000; // 24 saatte bir yeniden denenir
  } catch {
    return false;
  }
})();
const noteReportsTable = (error: any) => {
  const msg = String(error?.message || '') + String(error?.code || '');
  if (!/PGRST205|42P01|not find the table|does not exist|404/i.test(msg)) return;
  reportsTableMissing = true;
  try {
    localStorage.setItem(REPORTS_TABLE_KEY, String(Date.now()));
  } catch {
    /* gizli pencere */
  }
};

export const SupabaseDbService = {
  isConfigured(): boolean {
    return true;
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
        message: 'Veritabanı yapılandırılmamış.',
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
      const list = data.map((row: any) => ({
        id: row.id,
        name: row.name,
        academicYear: row.academic_year || '2026-2027',
        targetQuestions: row.target_questions || 100,
        color: row.color,
        createdAt: row.created_at,
        ...(row.data || {}),
      }));
      return filterCurrent2026_2027Committees(list);
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

      return data.map((row: any) => {
        const qNum = row.question_number ?? row.data?.questionNumber ?? 0;
        const isUnassigned = qNum === 0 || !!row.data?.isUnassignedNumber;
        return {
          ...(row.data || {}),
          id: row.id,
          committeeId: row.committee_id || row.data?.committeeId,
          questionNumber: qNum,
          isUnassignedNumber: isUnassigned,
          discipline: row.discipline || row.data?.discipline || 'Belirtilmedi',
          topic: row.topic || row.data?.topic || '',
          status: row.status || row.data?.status || 'gathering',
          claimedAnswer: row.claimed_answer || row.data?.claimedAnswer,
          upvotes: row.upvotes ?? row.data?.upvotes ?? 0,
          tags: row.tags || row.data?.tags || [],
          fragments: row.fragments || row.data?.fragments || [],
          options: row.options || row.data?.options || [],
          reconstruction: row.reconstruction || row.data?.reconstruction || null,
          createdAt: row.created_at || row.data?.createdAt,
          updatedAt: row.updated_at || row.data?.updatedAt,
        };
      });
    } catch (err) {
      console.warn('Supabase getQuestions error:', err);
      return [];
    }
  },

  async saveQuestion(question: QuestionItem): Promise<boolean> {
    const client = getSupabaseClient();
    if (!client || !question.id) return false;

    try {
      const qNum = typeof question.questionNumber === 'number' ? question.questionNumber : 0;
      const row = cleanForPostgres({
        id: question.id,
        committee_id: question.committeeId,
        question_number: qNum,
        discipline: question.discipline || 'Belirtilmedi',
        topic: question.topic || '',
        status: question.status || 'gathering',
        claimed_answer: question.claimedAnswer || null,
        upvotes: question.upvotes || 0,
        tags: question.tags || [],
        fragments: question.fragments || [],
        options: question.options || [],
        reconstruction: question.reconstruction || null,
        data: {
          ...question,
          questionNumber: qNum,
          isUnassignedNumber: qNum === 0 || !!question.isUnassignedNumber,
          updatedAt: question.updatedAt || new Date().toISOString()
        },
        updated_at: question.updatedAt || new Date().toISOString(),
      });

      const { error } = await client.from('questions').upsert([row], { onConflict: 'id' });
      if (error) {
        console.warn('[SupabaseDbService] saveQuestion upsert error:', error.message || error);
        return false;
      }
      return true;
    } catch (err) {
      console.warn('Supabase saveQuestion error:', err);
      return false;
    }
  },

  // Past Questions (PostgREST 1000 satır sınırını aşan chunk-build sayfalamalı yükleme)
  async getAllPastQuestions(): Promise<QuestionItem[]> {
    const client = getSupabaseClient();
    if (!client) return [];

    try {
      const allRows: any[] = [];
      const PAGE_SIZE = 1000;
      let from = 0;
      let hasMore = true;

      while (hasMore) {
        const { data, error } = await client
          .from('past_questions')
          .select('*')
          .range(from, from + PAGE_SIZE - 1);

        if (error) {
          console.warn('Supabase getAllPastQuestions page error:', error);
          break;
        }

        if (!data || data.length === 0) {
          hasMore = false;
        } else {
          allRows.push(...data);
          if (data.length < PAGE_SIZE) {
            hasMore = false;
          } else {
            from += PAGE_SIZE;
          }
        }
      }

      return allRows.map(mapRowToPastQuestion);
    } catch (err) {
      console.warn('Supabase getAllPastQuestions error:', err);
      return [];
    }
  },

  // Past Questions Meta (Lightweight ~100 bytes check to test if anything changed)
  async getPastQuestionsMeta(): Promise<{ latestUpdatedAt: string | null; count: number }> {
    const client = getSupabaseClient();
    if (!client) return { latestUpdatedAt: null, count: 0 };
    try {
      const { data, count, error } = await client
        .from('past_questions')
        .select('updated_at', { count: 'exact' })
        .order('updated_at', { ascending: false })
        .limit(1);

      if (error) {
        console.warn('Supabase getPastQuestionsMeta error:', error);
        return { latestUpdatedAt: null, count: 0 };
      }

      return {
        latestUpdatedAt: data?.[0]?.updated_at || null,
        count: count ?? 0,
      };
    } catch (err) {
      console.warn('Supabase getPastQuestionsMeta exception:', err);
      return { latestUpdatedAt: null, count: 0 };
    }
  },

  // Past Questions Delta (Fetch ONLY questions modified since timestamp)
  async getPastQuestionsDelta(sinceIso: string): Promise<QuestionItem[]> {
    const client = getSupabaseClient();
    if (!client) return [];
    try {
      const allRows: any[] = [];
      const PAGE_SIZE = 1000;
      let from = 0;
      let hasMore = true;

      while (hasMore) {
        const { data, error } = await client
          .from('past_questions')
          .select('*')
          .gt('updated_at', sinceIso)
          .order('updated_at', { ascending: true })
          .range(from, from + PAGE_SIZE - 1);

        if (error) {
          console.warn('Supabase getPastQuestionsDelta page error:', error);
          break;
        }

        if (!data || data.length === 0) {
          hasMore = false;
        } else {
          allRows.push(...data);
          if (data.length < PAGE_SIZE) {
            hasMore = false;
          } else {
            from += PAGE_SIZE;
          }
        }
      }

      return allRows.map(mapRowToPastQuestion);
    } catch (err) {
      console.warn('Supabase getPastQuestionsDelta error:', err);
      return [];
    }
  },

  // Past Questions IDs (Sayfalamalı tam ID listesi)
  async getPastQuestionsIds(): Promise<string[]> {
    const client = getSupabaseClient();
    if (!client) return [];
    try {
      const ids: string[] = [];
      const PAGE_SIZE = 1000;
      let from = 0;
      let hasMore = true;

      while (hasMore) {
        const { data, error } = await client
          .from('past_questions')
          .select('id')
          .range(from, from + PAGE_SIZE - 1);

        if (error) {
          console.warn('Supabase getPastQuestionsIds page error:', error);
          break;
        }

        if (!data || data.length === 0) {
          hasMore = false;
        } else {
          for (const r of data) ids.push(r.id);
          if (data.length < PAGE_SIZE) {
            hasMore = false;
          } else {
            from += PAGE_SIZE;
          }
        }
      }

      return ids;
    } catch (err) {
      console.warn('Supabase getPastQuestionsIds error:', err);
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

  async reportPastQuestion(
    questionId: string,
    report: { id?: string; reason: string; details?: string; reportedBy?: string; timestamp?: string }
  ): Promise<{ success: boolean; error?: string; report?: any }> {
    const client = getSupabaseClient();
    if (!client || !questionId) {
      return { success: false, error: 'Supabase istemcisi veya soru kimliği eksik.' };
    }

    try {
      const nowIso = report.timestamp || new Date().toISOString();
      const reportObj = {
        id: report.id || `rep-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
        reason: report.reason,
        details: report.details || '',
        reportedBy: report.reportedBy || 'Tıp Öğrencisi',
        timestamp: nowIso,
      };

      // 1. Fetch current question row from past_questions to update reports JSONB array
      const { data: row, error: fetchError } = await client
        .from('past_questions')
        .select('id, reports, data')
        .eq('id', questionId)
        .maybeSingle();

      if (fetchError) {
        console.warn('[SupabaseDbService.reportPastQuestion] Soru çekilirken uyarı:', fetchError.message);
      }

      const existingReports = Array.isArray(row?.reports)
        ? row.reports
        : Array.isArray(row?.data?.reports)
        ? row.data.reports
        : [];

      // Avoid duplicate report ID insertion
      const alreadyHas = existingReports.some((r: any) => r.id === reportObj.id);
      const updatedReports = alreadyHas ? existingReports : [...existingReports, reportObj];

      const updatePayload: Record<string, any> = {
        reports: cleanForPostgres(updatedReports),
        updated_at: nowIso,
      };

      if (row?.data) {
        updatePayload.data = cleanForPostgres({
          ...row.data,
          reports: updatedReports,
          updatedAt: nowIso,
        });
      }

      const { error: updateError } = await client
        .from('past_questions')
        .update(updatePayload)
        .eq('id', questionId);

      if (updateError) {
        console.warn('[SupabaseDbService.reportPastQuestion] past_questions reports update hatası:', updateError.message);
      }

      // 2. Also try inserting into dedicated past_question_reports table if it exists
      if (!reportsTableMissing) try {
        const { error: tblErr } = await client.from('past_question_reports').insert([cleanForPostgres({
          id: reportObj.id,
          question_id: questionId,
          reason: reportObj.reason,
          details: reportObj.details,
          reported_by: reportObj.reportedBy,
          status: 'pending',
          created_at: nowIso,
        })]);
        noteReportsTable(tblErr);
      } catch (_) {
        // Tablo yoksa birincil depo past_questions.reports kolonudur
      }

      // Canlı duyuru veritabanı tetikleyicisinden gelir (past_question_reports → inbox_update); ayrı istemci yayını
      // sunucuda geçersiz olay adıyla 400 alıyordu.
      return { success: !updateError, report: reportObj };
    } catch (err: any) {
      console.warn('[SupabaseDbService.reportPastQuestion] Beklenmeyen hata:', err);
      return { success: false, error: err?.message || 'Bilinmeyen hata' };
    }
  },

  async deletePastQuestionReport(questionId: string, reportId: string): Promise<{ success: boolean; error?: string }> {
    const client = getSupabaseClient();
    if (!client || !questionId || !reportId) return { success: false, error: 'Eksik parametre' };

    try {
      // 1. past_questions tablosundaki reports jsonb alanından sil
      const { data: row } = await client
        .from('past_questions')
        .select('id, reports, data')
        .eq('id', questionId)
        .maybeSingle();

      if (row) {
        const curReports = Array.isArray(row.reports)
          ? row.reports
          : Array.isArray(row.data?.reports)
          ? row.data.reports
          : [];
        const filtered = curReports.filter((r: any) => r.id !== reportId);
        const updatePayload: Record<string, any> = {
          reports: cleanForPostgres(filtered),
          updated_at: new Date().toISOString(),
        };
        if (row.data) {
          updatePayload.data = cleanForPostgres({ ...row.data, reports: filtered, updatedAt: updatePayload.updated_at });
        }
        await client.from('past_questions').update(updatePayload).eq('id', questionId);
      }

      // 2. past_question_reports tablosundan da sil
      if (!reportsTableMissing) try {
        const { error: tblErr } = await client.from('past_question_reports').delete().eq('id', reportId);
        noteReportsTable(tblErr);
      } catch (_) {}

      return { success: true };
    } catch (e: any) {
      return { success: false, error: e?.message };
    }
  },

  async updatePastQuestionReport(
    questionId: string,
    reportId: string,
    updates: { reason: string; details?: string }
  ): Promise<{ success: boolean; error?: string }> {
    const client = getSupabaseClient();
    if (!client || !questionId || !reportId) return { success: false, error: 'Eksik parametre' };

    try {
      const nowIso = new Date().toISOString();
      const { data: row } = await client
        .from('past_questions')
        .select('id, reports, data')
        .eq('id', questionId)
        .maybeSingle();

      if (row) {
        const curReports = Array.isArray(row.reports)
          ? row.reports
          : Array.isArray(row.data?.reports)
          ? row.data.reports
          : [];
        const updated = curReports.map((r: any) => {
          if (r.id === reportId) {
            return { ...r, reason: updates.reason, details: updates.details || '', updatedAt: nowIso, isEdited: true };
          }
          return r;
        });
        const updatePayload: Record<string, any> = {
          reports: cleanForPostgres(updated),
          updated_at: nowIso,
        };
        if (row.data) {
          updatePayload.data = cleanForPostgres({ ...row.data, reports: updated, updatedAt: nowIso });
        }
        await client.from('past_questions').update(updatePayload).eq('id', questionId);
      }

      if (!reportsTableMissing) try {
        const { error: tblErr } = await client.from('past_question_reports').update(cleanForPostgres({
          reason: updates.reason,
          details: updates.details || '',
          updated_at: nowIso,
        })).eq('id', reportId);
        noteReportsTable(tblErr);
      } catch (_) {}

      return { success: true };
    } catch (e: any) {
      return { success: false, error: e?.message };
    }
  },

  async deletePastQuestionComment(questionId: string, commentId: string): Promise<{ success: boolean; error?: string }> {
    const client = getSupabaseClient();
    if (!client || !questionId || !commentId) return { success: false, error: 'Eksik parametre' };

    try {
      const { data: row } = await client
        .from('past_questions')
        .select('id, comments, data')
        .eq('id', questionId)
        .maybeSingle();

      if (row) {
        const curComments = Array.isArray(row.comments)
          ? row.comments
          : Array.isArray(row.data?.comments)
          ? row.data.comments
          : [];
        const filtered = curComments.filter((c: any) => c.id !== commentId);
        const updatePayload: Record<string, any> = {
          comments: cleanForPostgres(filtered),
          updated_at: new Date().toISOString(),
        };
        if (row.data) {
          updatePayload.data = cleanForPostgres({ ...row.data, comments: filtered, updatedAt: updatePayload.updated_at });
        }
        await client.from('past_questions').update(updatePayload).eq('id', questionId);
      }
      return { success: true };
    } catch (e: any) {
      return { success: false, error: e?.message };
    }
  },

  async updatePastQuestionComment(questionId: string, commentId: string, newText: string): Promise<{ success: boolean; error?: string }> {
    const client = getSupabaseClient();
    if (!client || !questionId || !commentId) return { success: false, error: 'Eksik parametre' };

    try {
      const nowIso = new Date().toISOString();
      const { data: row } = await client
        .from('past_questions')
        .select('id, comments, data')
        .eq('id', questionId)
        .maybeSingle();

      if (row) {
        const curComments = Array.isArray(row.comments)
          ? row.comments
          : Array.isArray(row.data?.comments)
          ? row.data.comments
          : [];
        const updated = curComments.map((c: any) => {
          if (c.id === commentId) {
            return { ...c, text: newText.trim(), updatedAt: nowIso, isEdited: true };
          }
          return c;
        });
        const updatePayload: Record<string, any> = {
          comments: cleanForPostgres(updated),
          updated_at: nowIso,
        };
        if (row.data) {
          updatePayload.data = cleanForPostgres({ ...row.data, comments: updated, updatedAt: nowIso });
        }
        await client.from('past_questions').update(updatePayload).eq('id', questionId);
      }
      return { success: true };
    } catch (e: any) {
      return { success: false, error: e?.message };
    }
  },

  async getPastQuestionReports(limit: number = 100): Promise<any[]> {
    const client = getSupabaseClient();
    if (!client) return [];

    // First try dedicated past_question_reports table
    if (!reportsTableMissing) try {
      const { data, error } = await client
        .from('past_question_reports')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(limit);
      noteReportsTable(error);
      if (!error && Array.isArray(data) && data.length > 0) {
        // Tablo satırları snake_case; yönetim ekranı camelCase alanlar bekler
        return data.map(normalizeReportRow);
      }
    } catch (_) {}

    // Fallback: collect reports from past_questions table
    try {
      const { data, error } = await client
        .from('past_questions')
        .select('id, discipline, topic, reports, updated_at')
        .not('reports', 'is', null)
        .limit(limit);

      if (!error && Array.isArray(data)) {
        const flat: any[] = [];
        for (const q of data) {
          if (Array.isArray(q.reports)) {
            for (const r of q.reports) {
              flat.push(normalizeReportRow({ ...r, question_id: q.id, discipline: q.discipline, topic: q.topic }));
            }
          }
        }
        return flat;
      }
    } catch (_) {}

    return [];
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

  async batchSaveLectureNotes(notes: LectureNote[]): Promise<{ success: boolean; count: number }> {
    const client = getSupabaseClient();
    if (!client || notes.length === 0) return { success: false, count: 0 };

    let totalSaved = 0;
    const batchSize = 50;
    try {
      for (let i = 0; i < notes.length; i += batchSize) {
        const chunk = notes.slice(i, i + batchSize);
        const rows = cleanForPostgres(chunk.map((n) => ({
          id: n.id,
          committee_id: n.committeeId || 'donem3-kurul1',
          discipline: n.discipline || 'Tıp Dersi',
          title: n.title,
          pages: n.pages || [],
          page_count: n.pageCount || (n.pages ? n.pages.length : 0),
          data: n,
        })));
        const { error } = await client.from('lecture_notes').upsert(rows, { onConflict: 'id' });
        if (!error) totalSaved += chunk.length;
      }
      return { success: true, count: totalSaved };
    } catch (err) {
      console.warn('Supabase batchSaveLectureNotes error:', err);
      return { success: false, count: totalSaved };
    }
  },

  async deleteLectureNote(id: string): Promise<boolean> {
    const client = getSupabaseClient();
    if (!client || !id) return false;
    try {
      const { error } = await client.from('lecture_notes').delete().eq('id', id);
      return !error;
    } catch (err) {
      console.warn('Supabase deleteLectureNote error:', err);
      return false;
    }
  },

  async deleteQuestion(id: string): Promise<boolean> {
    const client = getSupabaseClient();
    if (!client || !id) return false;
    try {
      const { error } = await client.from('questions').delete().eq('id', id);
      return !error;
    } catch (err) {
      console.warn('Supabase deleteQuestion error:', err);
      return false;
    }
  },

  async deletePastQuestion(id: string): Promise<boolean> {
    const client = getSupabaseClient();
    if (!client || !id) return false;
    try {
      const { error } = await client.from('past_questions').delete().eq('id', id);
      return !error;
    } catch (err) {
      console.warn('Supabase deletePastQuestion error:', err);
      return false;
    }
  },

  // Canlı abonelik: sunucu SSE 'db_change' (Postgres NOTIFY kaynaklı) + diğer istemcilerin 'live' ipuçları.
  // Geri çağrı Supabase postgres_changes biçimini alır: { eventType, new, old }.
  subscribeToTable(table: string, callback: (payload: any) => void): () => void {
    const safe = (p: any) => {
      try {
        callback(p);
      } catch (e) {
        console.warn(`[Canlı] ${table} geri çağrı hatası:`, e);
      }
    };
    const offDb = realtimeEventService.on('db_change', (p: any) => {
      if (p?.table === table && p.eventType !== 'BULK') safe(p);
    });
    const offLive = realtimeEventService.on('live', (m: any) => {
      if (m?.event !== `${table}_changed` || !m.payload?.id) return;
      const { id, eventType } = m.payload;
      safe(eventType === 'DELETE' ? { eventType, old: { id }, id } : { eventType, id });
    });
    return () => {
      offDb();
      offLive();
    };
  },

  subscribeToQuestions(callback: (payload: any) => void): () => void {
    return this.subscribeToTable('questions', callback);
  },

  subscribeToPastQuestions(callback: (payload: any) => void): () => void {
    return this.subscribeToTable('past_questions', callback);
  },

  subscribeToLectureNotes(callback: (payload: any) => void): () => void {
    return this.subscribeToTable('lecture_notes', callback);
  },

  subscribeToCommittees(callback: (payload: any) => void): () => void {
    return this.subscribeToTable('committees', callback);
  },

  // Detailed Diagnostics for Online Status Check
  async getDetailedStatus(): Promise<{
    connected: boolean;
    latencyMs: number;
    counts: {
      questions: number;
      pastQuestions: number;
      lectureNotes: number;
      committees: number;
      users: number;
    };
    error?: string;
  }> {
    const client = getSupabaseClient();
    if (!client) {
      return {
        connected: false,
        latencyMs: 0,
        counts: { questions: 0, pastQuestions: 0, lectureNotes: 0, committees: 0, users: 0 },
        error: 'Veritabanı yapılandırılmamış.',
      };
    }

    const start = Date.now();
    try {
      const [resC, resQ, resP, resL, resU] = await Promise.all([
        client.from('committees').select('id', { count: 'exact', head: true }),
        client.from('questions').select('id', { count: 'exact', head: true }),
        client.from('past_questions').select('id', { count: 'exact', head: true }),
        client.from('lecture_notes').select('id', { count: 'exact', head: true }),
        client.from('users').select('uid', { count: 'exact', head: true }),
      ]);

      const latencyMs = Date.now() - start;

      if (resC.error && (resC.error.message.includes('relation') || resC.error.message.includes('schema cache'))) {
        return {
          connected: false,
          latencyMs,
          counts: { questions: 0, pastQuestions: 0, lectureNotes: 0, committees: 0, users: 0 },
          error: 'Tablolar henüz oluşturulmamış (SQL Şeması çalıştırılmalı).',
        };
      }

      return {
        connected: !resC.error,
        latencyMs,
        counts: {
          committees: resC.count || 0,
          questions: resQ.count || 0,
          pastQuestions: resP.count || 0,
          lectureNotes: resL.count || 0,
          users: resU.count || 0,
        },
        error: resC.error ? resC.error.message : undefined,
      };
    } catch (err: any) {
      return {
        connected: false,
        latencyMs: Date.now() - start,
        counts: { questions: 0, pastQuestions: 0, lectureNotes: 0, committees: 0, users: 0 },
        error: err.message,
      };
    }
  },

  // Gidiş-dönüş testi: sunucu Postgres'e NOTIFY yazar → LISTEN eden hub → SSE 'pong' bu sekmeye döner.
  async testRealtimeRoundtrip(timeoutMs: number = 4000): Promise<{
    success: boolean;
    latencyMs: number;
    message: string;
    broadcastActive?: boolean;
    postgresActive?: boolean;
    broadcastLatencyMs?: number;
    postgresLatencyMs?: number;
  }> {
    const start = Date.now();
    realtimeEventService.connect();
    // SSE bağlantısının kimliği gerekir (pong yalnız bu sekmeye gönderilir)
    while (!realtimeEventService.getClientId() && Date.now() - start < timeoutMs) {
      await new Promise((r) => setTimeout(r, 100));
    }
    const clientId = realtimeEventService.getClientId();
    if (!clientId) {
      return { success: false, latencyMs: Date.now() - start, broadcastActive: false, postgresActive: false, message: 'Canlı akışa (SSE) bağlanılamadı.' };
    }
    return new Promise((resolve) => {
      let pingId: string | null = null;
      let dbLatency = 0;
      const t0 = Date.now();
      const done = (r: any) => {
        clearTimeout(timer);
        off();
        resolve(r);
      };
      const early = new Set<string>();
      const finishOk = () => {
        const ms = Date.now() - t0;
        done({
          success: true,
          latencyMs: ms,
          broadcastActive: true,
          postgresActive: true,
          broadcastLatencyMs: ms,
          postgresLatencyMs: dbLatency,
          message: `✓ Canlı yayın çalışıyor (Postgres NOTIFY → SSE gidiş-dönüş: ${ms} ms)`,
        });
      };
      // pong, ping yanıtından önce de gelebilir: erken gelenler saklanır
      const off = realtimeEventService.on('pong', (p: any) => {
        if (!p?.id) return;
        if (pingId === p.id) finishOk();
        else if (!pingId) early.add(p.id);
      });
      const timer = setTimeout(
        () => done({ success: false, latencyMs: Date.now() - t0, broadcastActive: true, postgresActive: false, message: 'Canlı yayın zaman aşımı (Postgres bildirimi geri gelmedi).' }),
        Math.max(500, timeoutMs - (Date.now() - start))
      );
      void postLivePing(clientId).then((r) => {
        if (!r) done({ success: false, latencyMs: Date.now() - t0, broadcastActive: true, postgresActive: false, message: 'Sunucu veritabanına ulaşamadı.' });
        else {
          pingId = r.id;
          dbLatency = r.dbLatencyMs;
          if (early.has(r.id)) finishOk();
        }
      });
    });
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

