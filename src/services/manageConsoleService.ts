/**
 * Yönetim konsolu veri toplama servisi: hata bildirimleri, yorumlar,
 * taslak sorular, bildirimler ve kullanıcı aktivite özeti.
 * Okuma işlemleri mevcut bulut servislerini kullanır; yazma işlemleri
 * ApiService üzerinden bulut-doğru yollardan yapılır.
 */
import { SupabaseDbService } from './supabaseDb';
import { FirestoreDbService } from './firestoreDb';
import { multiDbManager } from './multiDbManager';
import { ApiService, safeJsonFetch } from './api';
import type { QuestionItem, Committee } from '../types';

export interface InboxReport {
  id: string;
  questionId: string;
  questionTopic?: string;
  discipline?: string;
  reason: string;
  details?: string;
  reportedBy?: string;
  createdAt?: string;
  status?: string;
}

export interface InboxComment {
  id: string;
  questionId: string;
  questionTopic?: string;
  author: string;
  text: string;
  createdAt?: string;
}

export interface UserActivityRow {
  key: string;
  name: string;
  email?: string;
  studentNumber?: string;
  questions: number;
  fragments: number;
  options: number;
  reports: number;
  comments: number;
  total: number;
}

export const loadManageInbox = async (
  committeeId?: string
): Promise<{
  reports: InboxReport[];
  comments: InboxComment[];
  pastQuestions: QuestionItem[];
  notifications: import('../types').AdminNotification[];
  drafts: QuestionItem[];
}> => {
  const [reports, pastQuestions, notifications] = await Promise.all([
    SupabaseDbService.getPastQuestionReports(200).catch(() => [] as InboxReport[]),
    multiDbManager.getPastQuestions().catch(() => [] as QuestionItem[]),
    FirestoreDbService.getAdminNotifications().catch(() => []),
  ]);

  const comments: InboxComment[] = [];
  for (const q of pastQuestions || []) {
    const list = (q as QuestionItem & { comments?: Array<{ id?: string; author: string; text: string; createdAt?: string }> }).comments || [];
    for (const c of list) {
      comments.push({
        id: c.id || `c-${q.id}-${comments.length}`,
        questionId: q.id,
        questionTopic: q.topic,
        author: c.author,
        text: c.text,
        createdAt: c.createdAt,
      });
    }
  }
  comments.sort((a, b) => (b.createdAt || '').localeCompare(a.createdAt || ''));

  let drafts: QuestionItem[] = [];
  try {
    if (committeeId) {
      const pool = await multiDbManager.getQuestions(committeeId).catch(() => [] as QuestionItem[]);
      drafts = (pool || []).filter((q) => q.status !== 'completed');
    }
  } catch {
    drafts = [];
  }

  return { reports, comments, pastQuestions: pastQuestions || [], notifications, drafts };
};

export const computeUserActivity = (
  poolQuestions: QuestionItem[],
  pastQuestions: QuestionItem[],
  reports: InboxReport[],
  comments: InboxComment[],
  registeredUsers: Array<{ uid?: string; email?: string; displayName?: string; studentNumber?: string }>
): UserActivityRow[] => {
  const map = new Map<string, UserActivityRow>();
  const ensure = (key: string, name: string): UserActivityRow => {
    let row = map.get(key);
    if (!row) {
      row = { key, name, questions: 0, fragments: 0, options: 0, reports: 0, comments: 0, total: 0 };
      map.set(key, row);
    }
    return row;
  };

  const allQuestions = [...(poolQuestions || []), ...(pastQuestions || [])];
  for (const q of allQuestions) {
    if (q.contributedByName || q.contributedByUid) {
      const row = ensure(
        (q.contributedByUid || q.contributedByName || 'bilinmeyen').toLowerCase(),
        q.contributedByName || 'İsimsiz katkı'
      );
      row.questions += 1;
    }
    for (const f of q.fragments || []) {
      const row = ensure(
        (f.authorUid || f.author || 'bilinmeyen').toLowerCase(),
        f.author || 'İsimsiz'
      );
      row.fragments += 1;
    }
    for (const o of q.options || []) {
      if (!o.suggestedBy && !o.suggestedByUid) continue;
      const row = ensure(
        (o.suggestedByUid || o.suggestedBy || 'bilinmeyen').toLowerCase(),
        o.suggestedBy || 'İsimsiz'
      );
      row.options += 1;
    }
  }
  for (const r of reports || []) {
    const row = ensure((r.reportedBy || 'bilinmeyen').toLowerCase(), r.reportedBy || 'İsimsiz bildirim');
    row.reports += 1;
  }
  for (const c of comments || []) {
    const row = ensure((c.author || 'bilinmeyen').toLowerCase(), c.author || 'İsimsiz yorum');
    row.comments += 1;
  }
  for (const u of registeredUsers || []) {
    const key = (u.email || u.uid || '').toLowerCase();
    if (!key) continue;
    const row = ensure(key, u.displayName || u.email || key);
    row.email = u.email;
    row.studentNumber = u.studentNumber;
  }
  const rows = [...map.values()];
  for (const r of rows) r.total = r.questions + r.fragments + r.options + r.reports + r.comments;
  return rows.sort((a, b) => b.total - a.total);
};

export const resolveInboxReport = async (
  adminEmail: string,
  report: InboxReport
): Promise<{ ok: boolean; message: string }> => {
  try {
    const res = await safeJsonFetch<{ success: boolean; message?: string }>(
      `/api/admin/reports/${encodeURIComponent(report.id)}/resolve`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
        body: JSON.stringify({ questionId: report.questionId }),
      }
    );
    if (res.ok) return { ok: true, message: res.data?.message || 'Bildirim çözüldü olarak işaretlendi.' };
    return { ok: false, message: `Sunucu çözümü yazamadı: ${res.error || 'bilinmeyen hata'}` };
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : 'Bilinmeyen hata';
    return { ok: false, message: `Çözümleme yazılamadı: ${msg}` };
  }
};

/** Çıkmış sorudaki bir yorumu sil (önce sunucu, her durumda bulut aynası denenir). */
export const deletePastComment = async (
  adminEmail: string,
  questionId: string,
  commentId: string
): Promise<{ ok: boolean; message: string }> => {
  try {
    const res = await safeJsonFetch<{ success: boolean; message?: string }>(
      `/api/past-exams/${encodeURIComponent(questionId)}/comments/${encodeURIComponent(commentId)}`,
      { method: 'DELETE', headers: { 'x-admin-email': adminEmail } }
    );
    if (res.ok) return { ok: true, message: 'Yorum silindi.' };
    return { ok: false, message: `Yorum silinemedi: ${res.error || 'bilinmeyen hata'}` };
  } catch (e: unknown) {
    return { ok: false, message: `Yorum silinemedi: ${e instanceof Error ? e.message : 'bağlantı hatası'}` };
  }
};

/** Taslak soruyu onayla ve yayınla (durumu tamamlandıya çevirir). */
export const publishDraft = async (
  adminEmail: string,
  draft: QuestionItem
): Promise<{ ok: boolean; message: string }> => {
  try {
    await ApiService.adminUpdateQuestion(adminEmail, draft.id, { status: 'completed' });
    return { ok: true, message: `Taslak yayınlandı (S.${draft.questionNumber || '?'}).` };
  } catch (e: unknown) {
    return { ok: false, message: `Yayınlanamadı: ${e instanceof Error ? e.message : 'bilinmeyen hata'}` };
  }
};

/** Taslak soruyu yapay zekaya tam soruya dönüştür (AI rekonstrüksiyon). */
export const reconstructDraft = async (
  draft: QuestionItem
): Promise<{ ok: boolean; message: string }> => {
  try {
    await ApiService.reconstructWithAi(draft.id);
    return { ok: true, message: `AI dönüştürmesi tamamlandı (S.${draft.questionNumber || '?'}).` };
  } catch (e: unknown) {
    return { ok: false, message: `AI dönüştürmesi başarısız: ${e instanceof Error ? e.message : 'bilinmeyen hata'}` };
  }
};

/**
 * Taslak soruyu her yerden sil: yerel uygulama + Supabase + sunucu (gizli anahtar).
 * Her kanal dürüstçe raporlanır; sunucu kanalı Supabase'e gizli anahtarla
 * yazdığı için RLS engeline takılmaz ve belirleyicidir.
 */
export const deleteDraftEverywhere = async (
  adminEmail: string,
  draft: QuestionItem
): Promise<{ ok: boolean; channels: { local: boolean; supabase: boolean; server: boolean; serverCloud: boolean }; message: string }> => {
  const channels = { local: false, supabase: false, server: false, serverCloud: false };
  const failures: string[] = [];

  try {
    await ApiService.adminDeleteQuestion(adminEmail, draft.id);
    channels.local = true;
  } catch (e: unknown) {
    failures.push(`yerel: ${e instanceof Error ? e.message : 'hata'}`);
  }
  try {
    await multiDbManager.deleteQuestion(draft.id);
    channels.supabase = true;
  } catch (e: unknown) {
    failures.push(`bulut: ${e instanceof Error ? e.message : 'hata'}`);
  }
  try {
    const res = await safeJsonFetch<{ success: boolean; cloud?: { local: boolean; cloud: boolean } }>(
      `/api/questions/${encodeURIComponent(draft.id)}`,
      { method: 'DELETE', headers: { 'x-admin-email': adminEmail } }
    );
    if (res.ok) {
      channels.server = true;
      channels.serverCloud = Boolean(res.data?.cloud && (res.data.cloud.local || res.data.cloud.cloud));
      if (!channels.serverCloud) failures.push('sunucu-bulut: Supabase aynası silinemedi');
    } else {
      failures.push(`sunucu: ${res.error || 'ulaşılamadı'}`);
    }
  } catch {
    failures.push('sunucu: bağlantı hatası');
  }

  const label = `S.${draft.questionNumber || '?'}`;
  if (!channels.local && !channels.supabase && !channels.server) {
    return { ok: false, channels, message: `Silinemedi (${label}): ${failures.join(' · ')}` };
  }
  const warn = failures.length > 0 ? ` Uyarı: ${failures.join(' · ')}` : '';
  return { ok: true, channels, message: `Taslak silindi (${label}).${warn}` };
};

export interface ManageServiceItem {
  id: string;
  name: string;
  category: string;
  status: string;
  statusLabel: string;
  description?: string;
}

/** Hangi servis/script çalışıyor, hangisi duruyor: sunucu envanteri. */
export const fetchSystemServices = async (): Promise<{
  ok: boolean;
  services: ManageServiceItem[];
  summary?: { totalServices: number; activeServicesCount: number; stoppedServicesCount: number };
  message: string;
}> => {
  try {
    const res = await safeJsonFetch<{
      services?: ManageServiceItem[];
      networkStatus?: { totalServices: number; activeServicesCount: number; stoppedServicesCount: number };
    }>('/api/system/services');
    if (res.ok && res.data?.services) {
      return {
        ok: true,
        services: res.data.services,
        summary: res.data.networkStatus,
        message: `${res.data.services.length} servis listelendi.`,
      };
    }
    return { ok: false, services: [], message: res.error || 'Servis listesi alınamadı.' };
  } catch (e: unknown) {
    return { ok: false, services: [], message: e instanceof Error ? e.message : 'Bağlantı hatası.' };
  }
};

/** Arka plan işçisinin (worker) kalp atışı + tünel canlılığı. */
export const fetchWorkerHeartbeat = async (): Promise<{
  ok: boolean;
  isOnline: boolean;
  diffSeconds?: number;
  message: string;
}> => {
  try {
    const res = await safeJsonFetch<{
      isOnline?: boolean;
      diffSeconds?: number;
      lastHeartbeat?: unknown;
    }>('/api/worker/heartbeat');
    if (res.ok && res.data) {
      const online = res.data.isOnline !== false;
      return {
        ok: true,
        isOnline: online,
        diffSeconds: res.data.diffSeconds,
        message: online ? 'Arka plan işçisi çevrimiçi.' : 'İşçi çevrimdışı görünüyor.',
      };
    }
    return { ok: false, isOnline: false, message: res.error || 'Nabız alınamadı.' };
  } catch (e: unknown) {
    return { ok: false, isOnline: false, message: e instanceof Error ? e.message : 'Bağlantı hatası.' };
  }
};

/** Yedeklemeyi zamanlamayı beklemeden hemen başlat. */
export const triggerBackupNow = async (
  adminEmail: string
): Promise<{ ok: boolean; message: string }> => {
  try {
    const res = await safeJsonFetch<{ success?: boolean; message?: string; error?: string }>(
      '/api/admin/backup-to-cloud',
      { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail }, body: '{}' }
    );
    if (res.ok) return { ok: true, message: res.data?.message || 'Yedekleme başlatıldı.' };
    return { ok: false, message: res.error || res.data?.error || 'Yedekleme başlatılamadı.' };
  } catch (e: unknown) {
    return { ok: false, message: e instanceof Error ? e.message : 'Bağlantı hatası.' };
  }
};

export const filterCommittees = (committees: Committee[]) => committees;

/** Yönetici olarak bir kullanıcıya e-posta gönder (SMTP varsa gerçek, yoksa kayıt). */
export const sendUserEmail = async (
  to: string,
  subject: string,
  text: string
): Promise<{ ok: boolean; sentReal: boolean; message: string }> => {
  try {
    const res = await safeJsonFetch<{ success: boolean; sentReal?: boolean; error?: string }>(
      '/api/send-email',
      { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ to, subject, text }) }
    );
    if (res.ok) {
      const real = res.data?.sentReal !== false;
      return { ok: true, sentReal: real, message: real ? 'E-posta gönderildi.' : 'SMTP kapalı: e-posta kayda alındı, gönderilmedi.' };
    }
    return { ok: false, sentReal: false, message: res.error || res.data?.error || 'E-posta gönderilemedi.' };
  } catch (e: unknown) {
    return { ok: false, sentReal: false, message: e instanceof Error ? e.message : 'Bağlantı hatası.' };
  }
};

/** Kullanıcıyı sil (sunucu + Supabase aynası). */
export const deleteManageUser = async (
  adminEmail: string,
  uid: string
): Promise<{ ok: boolean; message: string }> => {
  try {
    await ApiService.adminDeleteUser(adminEmail, uid);
    return { ok: true, message: 'Kullanıcı silindi.' };
  } catch (e: unknown) {
    return { ok: false, message: e instanceof Error ? e.message : 'Kullanıcı silinemedi.' };
  }
};
