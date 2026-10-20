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
import { getLocalAdminSession, auth } from './auth';
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
  revisions: number;
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
  // 1. Önce hafif ve hızlı Express API gelen kutusunu dene (60MB yerine 20KB, 20ms anlık yanıt)
  try {
    const admin = getLocalAdminSession();
    const email = admin?.email || auth?.currentUser?.email || 'nofrostlife@gmail.com';
    const serverInbox = await safeJsonFetch<{ success: boolean; reports: InboxReport[]; comments: InboxComment[] }>(
      '/api/admin/inbox',
      { headers: { 'x-admin-email': email } }
    );
    if (serverInbox.ok && serverInbox.data?.success && Array.isArray(serverInbox.data.reports)) {
      const [notifications, drafts] = await Promise.all([
        FirestoreDbService.getAdminNotifications().catch(() => []),
        committeeId
          ? multiDbManager.getQuestions(committeeId).then((p) => (p || []).filter((q) => q.status !== 'completed')).catch(() => [] as QuestionItem[])
          : Promise.resolve([] as QuestionItem[]),
      ]);
      return {
        reports: serverInbox.data.reports,
        comments: serverInbox.data.comments || [],
        pastQuestions: [],
        notifications,
        drafts,
      };
    }
  } catch (e) {
    console.warn('[loadManageInbox] Hızlı sunucu inbox fallback yapılıyor:', e);
  }

  // 2. Fallback: Bulut servisleri üzerinden çek
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
  const isBotOrSystem = (name?: string, key?: string) => {
    const s = `${name || ''} ${key || ''}`.toLocaleLowerCase('tr-TR');
    return (
      s.includes('yapay zeka') ||
      s.includes('ai (') ||
      s.includes(' ai') ||
      s.startsWith('ai') ||
      s.includes('bot') ||
      s.includes('gemini') ||
      s.includes('gpt') ||
      s.includes('deepseek') ||
      s.includes('claude') ||
      s.includes('asistan') ||
      s.includes('reconstruct') ||
      s.includes('otomasyon') ||
      s.includes('sistem') ||
      s.includes('system') ||
      s.includes('ocr') ||
      s.includes('taranmış') ||
      s.includes('arşivi') ||
      s.includes('arşiv') ||
      s.includes('taslak ayırma')
    );
  };

  const map = new Map<string, UserActivityRow>();
  const ensure = (key: string, name: string): UserActivityRow | null => {
    if (isBotOrSystem(name, key)) return null;
    let row = map.get(key);
    if (!row) {
      row = { key, name, questions: 0, revisions: 0, fragments: 0, options: 0, reports: 0, comments: 0, total: 0 };
      map.set(key, row);
    }
    return row;
  };

  const allQuestions = [...(poolQuestions || []), ...(pastQuestions || [])];
  for (const q of allQuestions) {
    if (q.contributedByName || q.contributedByUid) {
      const row = ensure(
        normKey(q.contributedByUid || q.contributedByName || 'bilinmeyen'),
        q.contributedByName || 'İsimsiz katkı'
      );
      if (row) row.questions += 1;
    }
    for (const rev of q.revisions || []) {
      if (rev.editorName || rev.editorUid) {
        const row = ensure(
          normKey(rev.editorUid || rev.editorName || 'bilinmeyen'),
          rev.editorName || 'İsimsiz düzenleyen'
        );
        if (row) row.revisions += 1;
      }
    }
    for (const f of q.fragments || []) {
      const row = ensure(
        normKey(f.authorUid || f.author || 'bilinmeyen'),
        f.author || 'İsimsiz'
      );
      if (row) row.fragments += 1;
    }
    for (const o of q.options || []) {
      if (!o.suggestedBy && !o.suggestedByUid) continue;
      const row = ensure(
        normKey(o.suggestedByUid || o.suggestedBy || 'bilinmeyen'),
        o.suggestedBy || 'İsimsiz'
      );
      if (row) row.options += 1;
    }
  }
  for (const r of reports || []) {
    const row = ensure(normKey(r.reportedBy || 'bilinmeyen'), r.reportedBy || 'İsimsiz bildirim');
    if (row) row.reports += 1;
  }
  for (const c of comments || []) {
    const row = ensure(normKey(c.author || 'bilinmeyen'), c.author || 'İsimsiz yorum');
    if (row) row.comments += 1;
  }
  // Kayıtlı kullanıcıları katkı satırlarıyla BİRLEŞTİR:
  // aynı kişinin e-posta/uid/görünen-ad anahtarları tek satırda toplanır.
  for (const u of registeredUsers || []) {
    const keys = [u.email, u.uid, u.displayName].map(normKey).filter(Boolean);
    if (keys.length === 0) continue;
    const primaryKey = normKey(u.email || u.uid);
    let primary = map.get(primaryKey);
    if (!primary) {
      primary = { key: primaryKey, name: u.displayName || u.email || primaryKey, questions: 0, revisions: 0, fragments: 0, options: 0, reports: 0, comments: 0, total: 0 };
      map.set(primaryKey, primary);
    }
    for (const k of keys) {
      if (k === primaryKey) continue;
      const other = map.get(k);
      if (other && other !== primary) {
        primary.questions += other.questions;
        primary.revisions += other.revisions;
        primary.fragments += other.fragments;
        primary.options += other.options;
        primary.reports += other.reports;
        primary.comments += other.comments;
        map.delete(k);
      }
      map.set(k, primary);
    }
    if (!primary.name || primary.name === primaryKey) primary.name = u.displayName || u.email || primaryKey;
    primary.email = u.email || primary.email;
    primary.studentNumber = u.studentNumber || primary.studentNumber;
  }
  const rows = [...new Set(map.values())];
  for (const r of rows) r.total = r.questions + r.revisions + r.fragments + r.options + r.reports + r.comments;
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

/** Çıkmış sorudaki bir yorumu düzenle. */
export const editPastComment = async (
  adminEmail: string,
  questionId: string,
  commentId: string,
  text: string
): Promise<{ ok: boolean; message: string; comment?: any }> => {
  try {
    const res = await safeJsonFetch<{ success: boolean; message?: string; comment?: any; error?: string }>(
      `/api/past-exams/${encodeURIComponent(questionId)}/comments/${encodeURIComponent(commentId)}`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
        body: JSON.stringify({ text }),
      }
    );
    if (res.ok && res.data?.success) return { ok: true, message: 'Yorum güncellendi.', comment: res.data.comment };
    return { ok: false, message: `Yorum güncellenemedi: ${res.data?.error || res.error || 'bilinmeyen hata'}` };
  } catch (e: unknown) {
    return { ok: false, message: `Yorum güncellenemedi: ${e instanceof Error ? e.message : 'bağlantı hatası'}` };
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

/** Gelen kutusundaki bir hata bildirimini düzenle. */
export const editInboxReport = async (
  adminEmail: string,
  reportId: string,
  updates: { reason: string; details?: string },
  questionId?: string
): Promise<{ ok: boolean; message: string; report?: any }> => {
  try {
    const url = questionId
      ? `/api/past-exams/${encodeURIComponent(questionId)}/reports/${encodeURIComponent(reportId)}`
      : `/api/reports/${encodeURIComponent(reportId)}`;
    const res = await safeJsonFetch<{ success: boolean; message?: string; report?: any; error?: string }>(url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
      body: JSON.stringify(updates),
    });
    if (res.ok && res.data?.success) return { ok: true, message: 'Bildirim güncellendi.', report: res.data.report };
    return { ok: false, message: `Bildirim güncellenemedi: ${res.data?.error || res.error || 'bilinmeyen hata'}` };
  } catch (e: unknown) {
    return { ok: false, message: `Bildirim güncellenemedi: ${e instanceof Error ? e.message : 'bağlantı hatası'}` };
  }
};

/** Gelen kutusundaki bir hata bildirimini KALICI olarak tüm veritabanından sil. */
export const deleteInboxReport = async (
  adminEmail: string,
  reportId: string,
  questionId?: string
): Promise<{ ok: boolean; message: string }> => {
  try {
    const url = questionId
      ? `/api/past-exams/${encodeURIComponent(questionId)}/reports/${encodeURIComponent(reportId)}`
      : `/api/reports/${encodeURIComponent(reportId)}`;
    const res = await safeJsonFetch<{ success: boolean; message?: string; error?: string }>(url, {
      method: 'DELETE',
      headers: { 'x-admin-email': adminEmail },
    });
    if (res.ok && res.data?.success) return { ok: true, message: 'Hata bildirimi kalıcı olarak silindi.' };
    return { ok: false, message: `Bildirim silinemedi: ${res.data?.error || res.error || 'bilinmeyen hata'}` };
  } catch (e: unknown) {
    return { ok: false, message: `Bildirim silinemedi: ${e instanceof Error ? e.message : 'bağlantı hatası'}` };
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

/** Türkçe uyumlu anahtar normalizasyonu (İ/i, I/ı eşleşmeleri için). */
export const normKey = (s: unknown): string => {
  try {
    return String(s || '').toLocaleLowerCase('tr-TR').trim();
  } catch {
    return String(s || '').toLowerCase().trim();
  }
};

export interface ManageUser {
  uid?: string;
  email?: string;
  displayName?: string;
  studentNumber?: string;
  role?: string;
  createdAt?: string;
  lastLoginAt?: string;
}

/** Kayıtlı kullanıcıları birleştir: sunucu JSON + Supabase (e-posta/uid'ye göre tekille). */
export const loadManageUsers = async (adminEmail: string): Promise<ManageUser[]> => {
  const [serverUsers, supaUsers] = await Promise.all([
    ApiService.adminGetUsers(adminEmail).catch(() => []),
    SupabaseDbService.getRegisteredUsers().catch(() => []),
  ]);
  const map = new Map<string, ManageUser>();
  const keyOf = (u: any) =>
    ((u.email || u.uid || '') as string).toLowerCase() || (u.uid || '').toLowerCase();
  for (const u of [...(supaUsers || []), ...(serverUsers || [])]) {
    if (!u) continue;
    const key = keyOf(u);
    if (!key) continue;
    const shaped: ManageUser = {
      uid: u.uid || (u as any).id,
      email: u.email,
      displayName: u.displayName || (u as any).display_name,
      studentNumber: u.studentNumber || (u as any).student_number,
      role: u.role,
      createdAt: u.createdAt || (u as any).created_at,
      lastLoginAt: u.lastLoginAt || (u as any).last_login_at || (u as any).updatedAt || (u as any).updated_at,
    };
    const prev = map.get(key);
    map.set(key, {
      uid: shaped.uid || prev?.uid,
      email: shaped.email || prev?.email,
      displayName: shaped.displayName || prev?.displayName,
      studentNumber: shaped.studentNumber || prev?.studentNumber,
      role: shaped.role || prev?.role,
      createdAt: shaped.createdAt || prev?.createdAt,
      lastLoginAt: shaped.lastLoginAt || prev?.lastLoginAt,
    });
  }
  return [...map.values()];
};

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

export interface SendNotificationPayload {
  target: 'single' | 'all';
  targetUser?: { uid?: string; email?: string };
  title: string;
  message: string;
  type?: 'app_info' | 'app_success' | 'app_error';
  deepLinkUrl?: string;
  targetType?: string;
}

/** Yönetici olarak kullanıcıya ya da tüm kullanıcılara bildirim mesajı gönderir. */
export const sendAdminNotification = async (
  adminEmail: string,
  payload: SendNotificationPayload
): Promise<{ ok: boolean; message: string; count?: number }> => {
  try {
    const res = await safeJsonFetch<{ success: boolean; message: string; count?: number; error?: string }>(
      '/api/admin/send-notification',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-admin-email': adminEmail,
        },
        body: JSON.stringify(payload),
      }
    );
    if (res.ok && res.data?.success) {
      return { ok: true, message: res.data.message || 'Bildirim iletildi.', count: res.data.count };
    }
    return { ok: false, message: res.error || res.data?.error || 'Bildirim iletilemedi.' };
  } catch (e: unknown) {
    return { ok: false, message: e instanceof Error ? e.message : 'Bağlantı hatası.' };
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

/** Kayıtsız (hayalet) yazarın tüm katkı izlerini temizle: parça, şık, yorum, bildirim. */
export const purgeAuthorContributions = async (
  committees: { id: string }[],
  authorKey: string
): Promise<{ ok: boolean; fragments: number; options: number; comments: number; reports: number; questionsTouched: number; message: string }> => {
  const stat = { fragments: 0, options: 0, comments: 0, reports: 0, questionsTouched: 0 };
  try {
    for (const c of committees || []) {
      let pool: QuestionItem[] = [];
      try {
        pool = await multiDbManager.getQuestions(c.id);
      } catch {
        continue;
      }
      for (const q of pool) {
        const beforeF = (q.fragments || []).length;
        const beforeO = (q.options || []).length;
        const nextF = (q.fragments || []).filter((f) => normKey(f.authorUid || f.author) !== authorKey);
        const nextO = (q.options || []).filter((o) => {
          if (!o.suggestedBy && !o.suggestedByUid) return true;
          return normKey(o.suggestedByUid || o.suggestedBy) !== authorKey;
        });
        if (nextF.length !== beforeF || nextO.length !== beforeO) {
          stat.fragments += beforeF - nextF.length;
          stat.options += beforeO - nextO.length;
          stat.questionsTouched += 1;
          try {
            await multiDbManager.saveQuestion({ ...q, fragments: nextF, options: nextO, updatedAt: new Date().toISOString() });
          } catch {
            /* tekil hata tümünü durdurmaz */
          }
        }
      }
    }
    let past: QuestionItem[] = [];
    try {
      past = await multiDbManager.getPastQuestions();
    } catch {
      past = [];
    }
    for (const q of past) {
      const qAny = q as QuestionItem & { comments?: Array<{ id?: string; author: string; text: string }>; reports?: Array<{ id?: string; reason: string; reportedBy?: string }> };
      const beforeC = (qAny.comments || []).length;
      const beforeR = (qAny.reports || []).length;
      const nextC = (qAny.comments || []).filter((cm) => normKey(cm.author) !== authorKey);
      const nextR = (qAny.reports || []).filter((rp) => normKey(rp.reportedBy) !== authorKey);
      if (nextC.length !== beforeC || nextR.length !== beforeR) {
        stat.comments += beforeC - nextC.length;
        stat.reports += beforeR - nextR.length;
        stat.questionsTouched += 1;
        try {
          await multiDbManager.savePastQuestion({ ...q, updatedAt: new Date().toISOString(), comments: nextC, reports: nextR } as QuestionItem);
        } catch {
          /* tekil hata tümünü durdurmaz */
        }
      }
    }
    const total = stat.fragments + stat.options + stat.comments + stat.reports;
    return { ok: true, ...stat, message: total > 0 ? `${total} katkı izi temizlendi (${stat.questionsTouched} soruda).` : 'Bu isme ait katkı izi bulunamadı.' };
  } catch (e: unknown) {
    return { ok: false, ...stat, message: e instanceof Error ? e.message : 'Temizleme başarısız.' };
  }
};

// --- Ücretsiz Gemini Hata İnceleme ve Onarım Otomasyonu İstemci Servisleri ---
export interface AutoRepairStats {
  total: number;
  pending: number;
  processing: number;
  applied: number;
  noChange: number;
  rolledBack: number;
  error: number;
  isWorkerActive: boolean;
}

export interface AutoRepairItemClient {
  id: string;
  source: 'past_question' | 'practice_question' | 'interactive_deck' | 'lecture_summary';
  targetId: string;
  subTarget?: {
    slideNumber?: number;
    targetKey?: string;
    optionKey?: string;
    location?: string;
    label?: string;
  };
  userReport: {
    reason: string;
    details: string;
    reportedBy: string;
    reportedAt: string;
    email?: string;
    suggestedAnswer?: string;
  };
  status: 'pending' | 'processing' | 'applied' | 'no_change' | 'rolled_back' | 'error';
  aiAnalysis?: {
    detectedIssues: string[];
    medicalReasoning: string;
    actionTaken: 'corrected' | 'verified_correct' | 'inconclusive';
    changesSummary: string;
    processedAt: string;
    modelUsed: string;
    releaseQuarantine?: boolean;
    referencedRedactedId?: string;
    crossDataAuditApplied?: boolean;
  };
  beforeSnapshot?: any;
  afterSnapshot?: any;
  crossData?: any;
  errorDetails?: string;
  rolledBackAt?: string;
  retryCount?: number;
}

const getAdminHeader = () => {
  const admin = getLocalAdminSession();
  const email = admin?.email || auth?.currentUser?.email || 'nofrostlife@gmail.com';
  return { 'x-admin-email': email };
};

export const loadAutoRepairItems = async (): Promise<AutoRepairItemClient[]> => {
  const res = await safeJsonFetch<{ success: boolean; items: AutoRepairItemClient[] }>('/api/admin/auto-repair/items', {
    headers: getAdminHeader(),
  });
  return res.ok && res.data?.items ? res.data.items : [];
};

export const loadAutoRepairStats = async (): Promise<AutoRepairStats | null> => {
  const res = await safeJsonFetch<{ success: boolean; stats: AutoRepairStats }>('/api/admin/auto-repair/stats', {
    headers: getAdminHeader(),
  });
  return res.ok && res.data?.stats ? res.data.stats : null;
};

export const runNextAutoRepair = async (): Promise<{ success: boolean; message?: string; item?: AutoRepairItemClient; error?: string }> => {
  const res = await safeJsonFetch<any>('/api/admin/auto-repair/run-next', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAdminHeader() },
  });
  return res.ok && res.data ? res.data : { success: false, error: res.error || 'Sunucu yanıt vermedi.' };
};

export const runAllAutoRepair = async (): Promise<{ success: boolean; message?: string; count?: number; error?: string }> => {
  const res = await safeJsonFetch<any>('/api/admin/auto-repair/run-all', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAdminHeader() },
  });
  return res.ok && res.data ? res.data : { success: false, error: res.error || 'Sunucu yanıt vermedi.' };
};

export const rollbackAutoRepair = async (id: string): Promise<{ success: boolean; message?: string; error?: string }> => {
  const res = await safeJsonFetch<any>(`/api/admin/auto-repair/${encodeURIComponent(id)}/rollback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAdminHeader() },
  });
  return res.ok && res.data ? res.data : { success: false, error: res.error || 'Sunucu yanıt vermedi.' };
};

export const retryAutoRepair = async (id: string): Promise<{ success: boolean; item?: AutoRepairItemClient; error?: string }> => {
  const res = await safeJsonFetch<any>(`/api/admin/auto-repair/${encodeURIComponent(id)}/retry`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAdminHeader() },
  });
  return res.ok && res.data ? res.data : { success: false, error: res.error || 'Sunucu yanıt vermedi.' };
};

export const toggleAutoRepairWorker = async (paused: boolean): Promise<{ success: boolean; isWorkerActive?: boolean }> => {
  const res = await safeJsonFetch<any>('/api/admin/auto-repair/toggle-worker', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAdminHeader() },
    body: JSON.stringify({ paused }),
  });
  if (!res.ok || !res.data?.success) throw new Error(res.error || 'Sunucu ayarı yazamadı.');
  return res.data;
};

export const deleteAutoRepairItem = async (id: string): Promise<boolean> => {
  const res = await safeJsonFetch<any>(`/api/admin/auto-repair/${encodeURIComponent(id)}`, {
    method: 'DELETE',
    headers: getAdminHeader(),
  });
  if (!res.ok || !res.data?.success) throw new Error(res.error || 'Sunucu kaydı silemedi.');
  return true;
};

export const clearProcessedAutoRepair = async (): Promise<{ success: boolean; clearedCount?: number; message?: string }> => {
  const res = await safeJsonFetch<any>('/api/admin/auto-repair/clear-processed', {
    method: 'POST',
    headers: getAdminHeader(),
  });
  return res.ok && res.data ? res.data : { success: false, message: res.error || 'Sunucu yanıt vermedi.' };
};

export const bulkDeleteAutoRepair = async (ids: string[]): Promise<{ success: boolean; removedCount?: number; message?: string }> => {
  const res = await safeJsonFetch<any>('/api/admin/auto-repair/bulk-delete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...getAdminHeader() },
    body: JSON.stringify({ ids }),
  });
  return res.ok && res.data ? res.data : { success: false, message: res.error || 'Sunucu yanıt vermedi.' };
};
