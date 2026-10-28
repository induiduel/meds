/**
 * Yönetim / panel / Faz 14 / betik / nadir ekran uçları.
 * api.ts'deki ApiService'ten ayrıldı (açılış parçasını küçültmek için); yalnız yönetim
 * ve nadir ekranlar buradan içe aktarır. Çekirdek (safeJsonFetch, kimlik, sık uçlar) api.ts'de.
 */
import {
  ApiService, safeJsonFetch, getLocalDb, saveLocalDb, getCustomApiUrl, STORAGE_KEY,
  type LocalDatabase, type AdminPipelineItem, type AdminScriptItem, type AdminScriptJob,
  type DriveCheckResult, type DriveSyncSettings, type Phase14Settings,
} from '../api';
import { QuestionItem, ReconstructedQuestion, PastQuestionReviewRecord } from '../../types';
import { FirestoreDbService } from '../firestoreDb';
import { multiDbManager } from '../multiDbManager';
import { SupabaseDbService, getSupabaseClient } from '../supabaseDb';
import { pastQuestionsCache } from '../pastQuestionsCache';
import { ADMIN_EMAIL } from '../auth';
import { isModeratorMode } from '../moderatorSession';
import { clusterDraftsForCommittee, unmergeQuestion, ClusterAnalysisSummary, ClusterTuning } from '../draftClusteringService';
export const YonetimApi = {

  /**
   * Sends rich medical welcome email to student upon registration.
   */
  async sendWelcomeEmail(
    userEmail: string,
    displayName?: string,
    studentNumber?: string
  ): Promise<{ success: boolean; error?: string; hint?: string; instructions?: string[] }> {
    if (!userEmail) return { success: false, error: 'E-posta adresi boş bırakılamaz.' };
    try {
      const res = await fetch('/api/send-welcome-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: userEmail,
          displayName,
          studentNumber,
        }),
      });
      const data = await res.json().catch(() => null);
      if (!res.ok) {
        return {
          success: false,
          error: data?.error || `HTTP ${res.status} Hatası`,
          hint: data?.hint,
          instructions: data?.instructions,
        };
      }
      return { success: true };
    } catch (e: any) {
      console.warn('sendWelcomeEmail network error:', e);
      return { success: false, error: e.message || 'Ağ bağlantı hatası' };
    }
  },

  async getSmtpConfig(): Promise<{
    enabled: boolean;
    service: string;
    host: string;
    port: number;
    secure: boolean;
    user: string;
    from: string;
    hasPass: boolean;
    passMasked: string;
  }> {
    const res = await fetch('/api/admin/smtp-config');
    if (!res.ok) throw new Error('SMTP ayarları alınamadı.');
    return res.json();
  },

  async saveSmtpConfig(config: {
    enabled?: boolean;
    service?: string;
    host?: string;
    port?: number;
    secure?: boolean;
    user?: string;
    pass?: string;
    from?: string;
  }): Promise<{ success: boolean; message: string; config: any }> {
    const res = await fetch('/api/admin/smtp-config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'SMTP ayarları kaydedilemedi.');
    return data;
  },

  async testSmtp(to?: string): Promise<{ success: boolean; message?: string; error?: string; hint?: string }> {
    const res = await fetch('/api/admin/smtp-test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ to }),
    });
    const data = await res.json();
    if (!res.ok) {
      return {
        success: false,
        error: data.error || 'Test e-postası gönderilemedi.',
        hint: data.hint,
      };
    }
    return data;
  },

  /** Yönetici: yeni soru kaydı (AI alternatifleri için). */
  async adminCreateQuestion(adminEmail: string, q: QuestionItem): Promise<QuestionItem> {
    if (adminEmail !== ADMIN_EMAIL) throw new Error('Yetkisiz işlem: yalnız sistem yöneticisi soru ekleyebilir.');
    const db = getLocalDb();
    db.questions.push(q);
    saveLocalDb(db);
    try {
      await multiDbManager.saveQuestion(q);
    } catch (e) {
      console.warn('multiDbManager adminCreateQuestion fallback', e);
    }
    return q;
  },

  // Admin endpoints
  async adminUpdateQuestion(adminEmail: string, id: string, updated: Partial<QuestionItem>): Promise<QuestionItem> {
    if (adminEmail !== ADMIN_EMAIL && !isModeratorMode()) {
      throw new Error('Yetkisiz işlem: Soru düzenleme yetkisi yalnızca sistem yöneticisine aittir.');
    }
    // Soru bu tarayıcının yerel kopyasında olmayabilir (yalnız sunucudan yüklenmiş): eskiden burada
    // "Soru bulunamadı" atılıp sunucuya hiç gidilmiyordu. Yerel kopya varsa güncellenir, sunucu her durumda yazılır.
    const db = getLocalDb();
    const idx = db.questions.findIndex((q) => q.id === id);
    const saved = { ...(idx >= 0 ? db.questions[idx] : {}), ...updated, id, updatedAt: new Date().toISOString() } as QuestionItem;
    if (idx >= 0) {
      db.questions[idx] = saved;
      saveLocalDb(db);
    }

    try {
      await multiDbManager.saveQuestion(saved);
    } catch (e) {
      console.warn('multiDbManager adminUpdateQuestion fallback', e);
    }

    const r = await safeJsonFetch(`/api/admin/questions/${encodeURIComponent(id)}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': adminEmail,
      },
      body: JSON.stringify(saved),
    });
    // Sunucu yazmadıysa başarı gösterme (eskiden yerel kopya varsa hata yutuluyor, düzenleme sunucuya hiç ulaşmıyordu)
    if (!r.ok) throw new Error(r.error || 'Sunucu soruyu güncelleyemedi');

    return saved;
  },

  async adminUpdatePastQuestion(adminEmail: string, id: string, updated: any): Promise<any> {
    if (adminEmail !== ADMIN_EMAIL && !isModeratorMode()) {
      throw new Error('Yetkisiz işlem: Çıkmış soru düzenleme yetkisi yalnızca sistem yöneticisine aittir.');
    }
    const merged = { ...updated, id, updatedAt: new Date().toISOString() };

    try {
      await multiDbManager.savePastQuestion(merged);
    } catch (e) {
      console.warn('multiDbManager adminUpdatePastQuestion fallback', e);
    }

    // Sunucu yazımı asıl kayıttır: başarısızsa hata fırlatılır (eskiden sessizce yutulup "Kaydedildi" deniyordu)
    const r = await safeJsonFetch<{ success?: boolean; question?: any; error?: string }>(`/api/admin/past-questions/${encodeURIComponent(id)}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': adminEmail,
      },
      body: JSON.stringify(merged),
    });
    if (!r.ok) throw new Error(r.data?.error || r.error || 'Sunucu çıkmış soruyu güncelleyemedi');

    try {
      await pastQuestionsCache.saveQuestion(merged);
    } catch (e) {
      console.warn('pastQuestionsCache saveQuestion fallback', e);
    }

    return merged;
  },

  async adminUpdateUser(adminEmail: string, uid: string, updated: any): Promise<any> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz erişim: Kullanıcı düzenleme yetkisi yalnızca yöneticiye aittir.');
    }
    const res = await fetch(`/api/admin/users/${encodeURIComponent(uid)}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': adminEmail,
      },
      body: JSON.stringify(updated),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Kullanıcı güncellenemedi.');
    }
    return data.user;
  },

  async adminUpdateSummary(adminEmail: string, id: string, updated: any): Promise<any> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz erişim: Özet düzenleme yetkisi yalnızca yöneticiye aittir.');
    }
    const res = await fetch(`/api/admin/summaries/${encodeURIComponent(id)}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': adminEmail,
      },
      body: JSON.stringify(updated),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Özet güncellenemedi.');
    }
    return data.summary;
  },

  async adminDeleteQuestion(adminEmail: string, id: string): Promise<void> {
    const isAuth = !adminEmail || adminEmail.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase();
    if (!isAuth) {
      throw new Error('Yetkisiz işlem: Başkasının sorusunu silme yetkisi yalnızca sistem yöneticisine (nofrostlife@gmail.com) aittir.');
    }
    const db = getLocalDb();
    db.questions = db.questions.filter((q) => q.id !== id);
    saveLocalDb(db);

    // Üç kanaldan sil: Supabase (istemci) + sunucu (gizli anahtarla Supabase fan-out).
    // Biri tutsa bile kayıt geri gelmez; hatalar sessize değil konsola yazılır.
    try {
      await multiDbManager.deleteQuestion(id);
    } catch (e) {
      console.warn('[ApiService] adminDeleteQuestion multiDbManager error', e);
    }
    const r = await safeJsonFetch(`/api/questions/${encodeURIComponent(id)}`, {
      method: 'DELETE',
      headers: { 'x-admin-email': adminEmail || ADMIN_EMAIL },
    });
    // 404 = sunucuda zaten yok; diğer hatalar toplu işlem sayacına yansısın diye fırlatılır
    if (!r.ok && r.status !== 404) throw new Error((r.data as any)?.error || r.error || 'Sunucu soruyu silemedi');
  },

  async assignUnassignedQuestion(
    adminEmail: string,
    unassignedId: string,
    targetNumber: number
  ): Promise<QuestionItem> {
    const isAuth = !adminEmail || adminEmail.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase();
    if (!isAuth) {
      throw new Error('Yetkisiz işlem: Yalnızca yönetici numarasız soruları yerleştirebilir.');
    }
    const db = getLocalDb();
    const unassigned = db.questions.find((q) => q.id === unassignedId);
    if (!unassigned) throw new Error('Numarasız soru bulunamadı.');

    const target = db.questions.find(
      (q) =>
        q.committeeId === unassigned.committeeId &&
        q.questionNumber === targetNumber &&
        !q.isUnassignedNumber
    );

    if (target) {
      // Merge fragments and options into existing slot
      target.fragments.push(...unassigned.fragments);
      unassigned.options.forEach((opt) => {
        const ex = target.options.find((o) => o.key === opt.key);
        if (!ex) target.options.push(opt);
      });
      if (unassigned.discipline && unassigned.discipline !== 'Belirtilmedi') {
        target.discipline = unassigned.discipline;
      }
      target.status = 'gathering';
      target.examYear = '2026-2027';
      target.updatedAt = new Date().toISOString();

      db.questions = db.questions.filter((q) => q.id !== unassignedId);
      saveLocalDb(db);

      try {
        await multiDbManager.saveQuestion(target);
        await multiDbManager.deleteQuestion(unassignedId);
      } catch (e) {}
      return target;
    } else {
      // Convert unassigned question directly to slot targetNumber
      unassigned.questionNumber = targetNumber;
      unassigned.isUnassignedNumber = false;
      unassigned.examYear = '2026-2027';
      unassigned.topic =
        unassigned.topic.replace('(Numarası Belirsiz Soru)', '').trim() || `Soru #${targetNumber}`;
      unassigned.updatedAt = new Date().toISOString();
      saveLocalDb(db);

      try {
        await multiDbManager.saveQuestion(unassigned);
      } catch (e) {}
      return unassigned;
    }
  },

  // Akıllı Taslak Kümeleme ve Birleştirme Metotları
  async getCommitteeDraftClusters(committeeId: string, tuning?: ClusterTuning): Promise<ClusterAnalysisSummary> {
    const db = getLocalDb();
    return clusterDraftsForCommittee(db.questions, committeeId, tuning);
  },

  async unmergeDraftCluster(
    adminEmail: string,
    consolidatedId: string,
    adminName: string = 'Yönetici'
  ): Promise<{ anchor: QuestionItem; restoredSatellites: QuestionItem[] }> {
    const isAuth = !adminEmail || adminEmail.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase();
    if (!isAuth) {
      throw new Error('Yetkisiz işlem: Taslak ayırma yetkisi yalnızca sistem yöneticisine aittir.');
    }
    const db = getLocalDb();
    const consolidated = db.questions.find((q) => q.id === consolidatedId);
    if (!consolidated) throw new Error('Birleştirilmiş taslak bulunamadı.');

    const { anchor, restoredSatellites } = unmergeQuestion(consolidated);
    anchor.examYear = '2026-2027';
    anchor.updatedAt = new Date().toISOString();

    // Update anchor in local db
    const anchorIdx = db.questions.findIndex((q) => q.id === consolidatedId);
    if (anchorIdx !== -1) {
      db.questions[anchorIdx] = anchor;
    }

    // Add restored satellites back to local db
    for (const sat of restoredSatellites) {
      sat.examYear = '2026-2027';
      sat.updatedAt = new Date().toISOString();
      if (!db.questions.some((q) => q.id === sat.id)) {
        db.questions.push(sat);
      }
    }

    saveLocalDb(db);

    // Cloud DB sync (Supabase + Firestore + Local PC)
    try {
      await multiDbManager.saveQuestion(anchor);
      for (const sat of restoredSatellites) {
        await multiDbManager.saveQuestion(sat);
      }
    } catch (e) {
      console.warn('Draft unmerge cloud sync warning:', e);
    }

    return { anchor, restoredSatellites };
  },

  async autoMergeHighConfidenceClusters(
    adminEmail: string,
    committeeId: string,
    adminName: string = 'Akıllı Konsolidasyon'
  ): Promise<{ mergedClustersCount: number; savedDuplicatesCount: number }> {
    const isAuth = !adminEmail || adminEmail.trim().toLowerCase() === ADMIN_EMAIL.toLowerCase();
    if (!isAuth) {
      throw new Error('Yetkisiz işlem: Toplu taslak birleştirme yetkisi yalnızca sistem yöneticisine aittir.');
    }
    const db = getLocalDb();
    const summary = clusterDraftsForCommittee(db.questions, committeeId);
    const readyClusters = summary.clusters.filter((c) => c.status === 'ready_to_merge');

    let mergedClustersCount = 0;
    let savedDuplicatesCount = 0;

    for (const cluster of readyClusters) {
      const satelliteIds = cluster.satelliteDrafts.map((s) => s.question.id);
      if (satelliteIds.length > 0) {
        await ApiService.mergeDraftCluster(adminEmail, cluster.anchorQuestion.id, satelliteIds, adminName);
        mergedClustersCount++;
        savedDuplicatesCount += satelliteIds.length;
      }
    }

    return { mergedClustersCount, savedDuplicatesCount };
  },

  async adminExportDb(): Promise<LocalDatabase> {
    return getLocalDb();
  },

  async adminImportDb(adminEmail: string, data: LocalDatabase): Promise<void> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Veritabanı içe aktarma yetkisi yalnızca sistem yöneticisine aittir.');
    }
    saveLocalDb(data);
    if (data.questions && data.questions.length > 0) {
      try {
        await FirestoreDbService.batchSaveQuestions(data.questions);
      } catch (e) {}
    }
  },

  async adminResetDb(adminEmail: string): Promise<void> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Sıfırlama yetkisi yalnızca sistem yöneticisine aittir.');
    }
    localStorage.removeItem(STORAGE_KEY);
    getLocalDb();
  },

  // Admin AI Past Exam Questions Parser (Supports text, PDF, Word DOCX, and images)
  async parsePastExamQuestions({
    rawText,
    fileBase64,
    fileMimeType,
    fileName,
    examYear,
    committeeId,
    defaultDiscipline,
    adminEmail,
  }: {
    rawText?: string;
    fileBase64?: string;
    fileMimeType?: string;
    fileName?: string;
    examYear: string;
    committeeId: string;
    defaultDiscipline?: string;
    adminEmail: string;
  }): Promise<{ detectedYear: string; totalCount: number; questions: any[] }> {
    const res = await fetch('/api/ai/parse-past-questions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': adminEmail,
      },
      body: JSON.stringify({
        rawText,
        fileBase64,
        fileMimeType,
        fileName,
        examYear,
        committeeId,
        defaultDiscipline,
        adminEmail,
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'Yapay zeka soruları ayrıştıramadı.');
    }
    return await res.json();
  },

  async saveLectureNote(note: any): Promise<any> {
    const res = await fetch('/api/lecture-notes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(note),
    });
    if (!res.ok) throw new Error('Ders notu kaydedilemedi');
    return await res.json();
  },

  async deleteLectureNote(id: string): Promise<any> {
    const res = await fetch(`/api/lecture-notes/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Ders notu silinemedi');
    return await res.json();
  },

  async getDesktopDatabaseStatus(): Promise<any> {
    const res = await fetch('/api/automation/desktop-folder-status');
    if (!res.ok) throw new Error('Klasör durumu alınamadı');
    return await res.json();
  },

  // Gemini & NotebookLM Database Synchronization
  async syncDatabaseWithGemini(payload: any, committeeId?: string): Promise<{ success: boolean; message: string; updatedCount: number }> {
    const res = await fetch('/api/gemini/sync-database', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ payload, committeeId }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'Veritabanı senkronizasyonu başarısız oldu.');
    }
    return await res.json();
  },

  // Batch import questions parsed from past exam files into database
  async batchImportPastQuestions(
    adminEmail: string,
    committeeId: string,
    examYear: string,
    parsedQuestions: any[]
  ): Promise<{ success: boolean; count: number; questions: QuestionItem[]; firebaseSynced: boolean; serverSynced: boolean }> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz işlem: Soru aktarma yetkisi yalnızca sistem yöneticisine aittir.');
    }

    const db = getLocalDb();
    const createdQuestions: QuestionItem[] = [];

    for (const pq of parsedQuestions) {
      const qNum = Number(pq.questionNumber) || (db.questions.filter((q) => q.committeeId === committeeId).length + 1);
      const questionId = `past-${committeeId}-${qNum}-${Date.now().toString().slice(-4)}`;

      // Construct options array with zero initial likes
      const options = (pq.options || []).map((opt: any) => ({
        key: opt.key as 'A' | 'B' | 'C' | 'D' | 'E',
        text: opt.text || '',
        suggestedBy: `Çıkmış (${examYear})`,
        upvotes: 0,
        likedBy: [],
      }));

      // If less than 5 options, pad with standard placeholders
      const existingKeys = new Set(options.map((o: any) => o.key));
      (['A', 'B', 'C', 'D', 'E'] as const).forEach((k) => {
        if (!existingKeys.has(k)) {
          options.push({
            key: k,
            text: `${k} seçeneği (öğrenci katkısı bekleniyor)`,
            suggestedBy: 'AI Taslak',
            upvotes: 0,
            likedBy: [],
          });
        }
      });

      const newQ: QuestionItem = {
        id: questionId,
        committeeId,
        questionNumber: qNum,
        discipline: pq.discipline || 'Tıbbi Patoloji',
        topic: pq.topic || `Soru #${qNum} (${examYear})`,
        status: pq.claimedAnswer ? 'completed' : 'gathering',
        claimedAnswer: pq.claimedAnswer || undefined,
        upvotes: 0,
        likedBy: [],
        tags: [
          `${examYear} Çıkmış`,
          'Çıkmış Soru',
          pq.discipline || 'Genel',
        ].filter(Boolean),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        contributedByName: `Yönetici (${examYear} Arşivi)`,
        fragments: [
          {
            id: `frag-${Date.now()}-${Math.random().toString(36).substring(7)}`,
            author: `Çıkmış Soru (${examYear})`,
            text: pq.stem || 'Soru kökü metni',
            type: 'stem',
            timestamp: new Date().toISOString(),
            upvotes: 0,
            likedBy: [],
          },
        ],
        options,
        reconstruction: pq.stem
          ? {
              stem: pq.stem,
              options: options.map((o: any) => ({
                key: o.key,
                text: o.text,
                isAiFilled: false,
              })),
              correctAnswer: (pq.claimedAnswer || 'A') as 'A' | 'B' | 'C' | 'D' | 'E',
              explanation: pq.explanation || `Bu soru ${examYear} tıp kurulu sınavında sorulmuştur.`,
              confidenceScore: pq.confidenceScore || 90,
              notesAndDiscrepancies: `Geçmiş yıl çıkmış soru dosyasından AI tarafından ayrıştırıldı. Öğrenciler tarafından düzenlenebilir.`,
              lastUpdated: new Date().toISOString(),
            }
          : undefined,
      };

      // Check if slot with same question number already exists in this committee
      const existingIdx = db.questions.findIndex(
        (q) => q.committeeId === committeeId && q.questionNumber === qNum
      );
      if (existingIdx !== -1) {
        db.questions[existingIdx] = newQ;
      } else {
        db.questions.push(newQ);
      }
      createdQuestions.push(newQ);
    }

    // 1. Save to local browser state
    saveLocalDb(db);

    // 2. Persist to backend server (data/questions.json)
    let serverSynced = false;
    try {
      const serverRes = await fetch('/api/questions/batch-import', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-admin-email': adminEmail,
        },
        body: JSON.stringify({
          adminEmail,
          committeeId,
          examYear,
          questions: createdQuestions,
        }),
      });
      serverSynced = serverRes.ok;
    } catch (err) {
      console.warn('Backend server batch save warning:', err);
    }

    // 3. Persist to Firebase Firestore cloud database
    let firebaseSynced = false;
    try {
      const firestoreRes = await FirestoreDbService.batchSaveQuestions(createdQuestions);
      firebaseSynced = firestoreRes.success;
    } catch (e: any) {
      console.warn('Firestore batch save past questions warning:', e);
    }

    return {
      success: true,
      count: createdQuestions.length,
      questions: createdQuestions,
      firebaseSynced,
      serverSynced,
    };
  },

  // User Management & Realtime Synchronization
  async syncUser(user: {
    uid: string;
    email: string | null;
    displayName: string | null;
    studentNumber?: string | null;
    photoURL?: string | null;
    congratsSentCommittees?: string[];
  }): Promise<any> {
    try {
      const res = await fetch('/api/users/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user),
      });
      return await res.json();
    } catch (e) {
      console.warn('api.syncUser network fallback:', e);
      return null;
    }
  },

  async adminGetUsers(adminEmail: string): Promise<any[]> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz erişim: Kullanıcı listeleme yetkisi yalnızca yöneticiye aittir.');
    }
    const res = await fetch(`${getCustomApiUrl('/api/admin/users')}/api/admin/users`, {
      headers: {
        'x-admin-email': adminEmail,
      },
    });
    if (!res.ok) {
      throw new Error('Kullanıcı listesi alınamadı.');
    }
    const data = await res.json();
    return data.users || [];
  },

  async adminCreateUser(adminEmail: string, user: { email: string; displayName?: string; studentNumber?: string; role?: string }): Promise<any> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz erişim: Kullanıcı ekleme yetkisi yalnızca yöneticiye aittir.');
    }
    const res = await fetch('/api/admin/users/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': adminEmail,
      },
      body: JSON.stringify(user),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Kullanıcı oluşturulamadı.');
    }
    return data.user;
  },

  async adminDeleteUser(adminEmail: string, uid: string): Promise<void> {
    if (adminEmail !== ADMIN_EMAIL) {
      throw new Error('Yetkisiz erişim: Kullanıcı silme yetkisi yalnızca yöneticiye aittir.');
    }
    const res = await fetch(`/api/admin/users/${uid}`, {
      method: 'DELETE',
      headers: {
        'x-admin-email': adminEmail,
      },
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Kullanıcı silinemedi.');
    }
  },

  // Drive automation sync
  async syncDriveAutomation(committeeId?: string, forceSync = false): Promise<any> {
    const res = await fetch('/api/drive/sync-automation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ committeeId, forceSync }),
    });
    if (!res.ok) {
      throw new Error('Google Drive senkronizasyonu başlatılamadı.');
    }
    return await res.json();
  },

  // AI: Generate similar exam question grounded in matched lecture note
  async generateSimilarQuestion(baseQuestion: QuestionItem, slideMatch?: any): Promise<any> {
    try {
      const res = await fetch('/api/ai/generate-similar-question', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ baseQuestion, slideMatch }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data.question) return data.question;
      }
    } catch (e) {
      console.warn('generateSimilarQuestion network error:', e);
    }

    // Client-side fallback generator if offline
    const discipline = baseQuestion.discipline || 'Tıbbi Patoloji';
    const topic = baseQuestion.topic || 'Çıkmış Sınav Konusu';
    const sourcePdf = baseQuestion.sourceFile || 'Çıkmış Sınav Dosyası';
    const noteTitle = slideMatch?.note?.title || 'İlgili Amfi Dersi';
    const slidePage = slideMatch?.page?.pageNumber || 1;

    return {
      id: `ai-sim-client-${Date.now()}`,
      discipline,
      topic: `Benzer Soru: ${topic}`,
      stem: `${discipline} kurul sınavı ve "${noteTitle}" (Slayt #${slidePage}) konusu kapsamında;\n\n"${topic}" etiyolojisi ve klinik patogenezi incelendiğinde; hastada gözlenen morfolojik değişiklikler ve ${discipline.toLowerCase()} yaklaşım açısından aşağıdakilerden hangisi EN OLASI ifadedir?`,
      options: [
        { key: 'A', text: `Hücresel düzeyde ${topic} ile ilişkili hasarın geri dönüşümsüz faza geçmesi` },
        { key: 'B', text: `Primer etiyolojide inflamatuar kaskadın sitokin aracılı regülasyonu` },
        { key: 'C', text: `${noteTitle} slaytında vurgulanan karakteristik morfolojik / biyokimyasal belirteç artışı` },
        { key: 'D', text: `Sekonder patolojide gelişen vasküler permeabilite ve doku ödemi` },
        { key: 'E', text: `Klinik seyirde spontan regresyon gösteren fizyolojik adaptasyon mekanizması` }
      ],
      correctAnswer: 'C',
      explanation: `Bu ek soru, "${sourcePdf}" çıkmış sınav sorusu ile "${noteTitle}" (Slayt #${slidePage}) slaytında yer alan patolojik prensipler temel alınarak oluşturulmuştur.`,
      sourceExamPdf: sourcePdf,
      matchedNoteTitle: noteTitle,
      matchedSlidePage: slidePage,
      isAiGenerated: true,
      createdAt: new Date().toISOString()
    };
  },

  // Save approved past exam question across all databases (Local Server PUT + Supabase + Firebase Spark)
  /** Çıkmış soruda alan güncelle (gizleme vb.); yerel veritabanı + Supabase aynası */
  async adminPatchPastQuestion(adminEmail: string, id: string, patch: Record<string, any>): Promise<QuestionItem> {
    const res = await safeJsonFetch<{ success: boolean; question: QuestionItem; error?: string }>(`/api/past-exams/${encodeURIComponent(id)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
      body: JSON.stringify(patch),
    });
    if (!res.ok || !res.data?.success) throw new Error(res.data?.error || res.error || 'Soru güncellenemedi.');
    try { await pastQuestionsCache.saveQuestion(res.data.question); } catch { /* önbellek yoksa geç */ }
    return res.data.question;
  },

  /** Faz 14: Çıkmış soru redaksiyon inceleme katmanını listeler */
  async getPastQuestionReviews(params?: { status?: string; questionId?: string }): Promise<{
    reviews: PastQuestionReviewRecord[];
    totalCount: number;
    filteredCount: number;
    report: any;
  }> {
    const sp = new URLSearchParams();
    if (params?.status && params.status !== 'all') sp.set('status', params.status);
    if (params?.questionId) sp.set('questionId', params.questionId);
    const qs = sp.toString() ? `?${sp.toString()}` : '';
    const res = await safeJsonFetch<{
      success: boolean;
      reviews: PastQuestionReviewRecord[];
      totalCount: number;
      filteredCount: number;
      report: any;
      error?: string;
    }>(`/api/past-question-reviews${qs}`, {
      method: 'GET',
      headers: { Accept: 'application/json' },
    });
    if (!res.ok || !res.data?.success) {
      throw new Error(res.data?.error || res.error || 'İnceleme kayıtları alınamadı.');
    }
    return {
      reviews: res.data.reviews || [],
      totalCount: res.data.totalCount || 0,
      filteredCount: res.data.filteredCount || 0,
      report: res.data.report || null,
    };
  },

  /** Faz 14: Öneriyi açık onayla ve geçmiş soru havuzuna uygula */
  async approvePastQuestionReview(adminEmail: string, questionId: string): Promise<any> {
    const res = await safeJsonFetch<{
      success: boolean;
      message: string;
      question?: QuestionItem;
      review?: PastQuestionReviewRecord;
      error?: string;
    }>(`/api/past-question-reviews/${encodeURIComponent(questionId)}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
    });
    if (!res.ok || !res.data?.success) {
      throw new Error(res.data?.error || res.error || 'Öneri onaylanamadı.');
    }
    if (res.data.question) {
      try { await pastQuestionsCache.saveQuestion(res.data.question); } catch { /* ignore */ }
    }
    return res.data;
  },

  /** Faz 14: Öneriyi reddet */
  async rejectPastQuestionReview(adminEmail: string, questionId: string, reason?: string): Promise<any> {
    const res = await safeJsonFetch<{
      success: boolean;
      message: string;
      review?: PastQuestionReviewRecord;
      error?: string;
    }>(`/api/past-question-reviews/${encodeURIComponent(questionId)}/reject`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
      body: JSON.stringify({ reason }),
    });
    if (!res.ok || !res.data?.success) {
      throw new Error(res.data?.error || res.error || 'Öneri reddedilemedi.');
    }
    return res.data;
  },

  /** Faz 14: Soruyu inceleme listesinden ve veritabanından kalıcı olarak sil */
  async deletePastQuestionReview(adminEmail: string, questionId: string): Promise<any> {
    const res = await safeJsonFetch<{
      success: boolean;
      message: string;
      id?: string;
      error?: string;
    }>(`/api/past-question-reviews/${encodeURIComponent(questionId)}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
    });
    if (!res.ok || !res.data?.success) {
      throw new Error(res.data?.error || res.error || 'Soru kalıcı olarak silinemedi.');
    }
    return res.data;
  },

  /** Faz 14: Bekleyen öneriyi şüpheli olarak işaretle / işareti kaldır */
  async setPastQuestionAnswerDoubt(adminEmail: string, questionId: string, value: boolean): Promise<any> {
    const res = await safeJsonFetch<{ success: boolean; message: string; error?: string }>(
      `/api/past-question-reviews/${encodeURIComponent(questionId)}/answer-doubt`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
        body: JSON.stringify({ value }),
      }
    );
    if (!res.ok || !res.data?.success) throw new Error(res.data?.error || res.error || 'İşaret güncellenemedi.');
    return res.data;
  },

  async completeAnswerDoubt(adminEmail: string, questionId: string, choice?: string): Promise<{ winner: string; message: string }> {
    const res = await safeJsonFetch<{ success: boolean; winner: string; message: string; error?: string }>(
      `/api/past-question-reviews/${encodeURIComponent(questionId)}/answer-doubt/complete`,
      { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail }, body: JSON.stringify({ ...(choice ? { choice } : {}), keepPoll: true }) }
    );
    if (!res.ok || !res.data?.success) throw new Error(res.data?.error || res.error || 'Anket tamamlanamadı.');
    return res.data;
  },

  async editPoolQuestionReport(
    questionId: string,
    reportId: string,
    updates: { reason: string; details?: string },
    userAuth?: { uid?: string; email?: string; reportedBy?: string; ownershipToken?: string; adminEmail?: string }
  ): Promise<{ success: boolean; message?: string; report?: any }> {
    const apiBase = getCustomApiUrl() || '';
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (userAuth?.adminEmail) headers['x-admin-email'] = userAuth.adminEmail;
    if (userAuth?.uid) headers['x-user-uid'] = userAuth.uid;
    if (userAuth?.email) headers['x-user-email'] = userAuth.email;
    if (userAuth?.reportedBy) headers['x-user-name'] = userAuth.reportedBy;
    if (userAuth?.ownershipToken) headers['x-ownership-token'] = userAuth.ownershipToken;

    try {
      const res = await safeJsonFetch<{ success: boolean; message?: string; report?: any; error?: string }>(
        `${apiBase}/api/questions/${encodeURIComponent(questionId)}/reports/${encodeURIComponent(reportId)}`,
        { method: 'PUT', headers, body: JSON.stringify(updates) }
      );
      if (res.ok && res.data?.success) {
        return { success: true, message: res.data.message || 'Bildirim güncellendi.', report: res.data.report };
      }
      return { success: false, message: res.data?.error || res.error || 'Bildirim güncellenemedi.' };
    } catch (e: any) {
      return { success: false, message: e.message || 'Bağlantı hatası' };
    }
  },

  async deletePoolQuestionReport(
    questionId: string,
    reportId: string,
    userAuth?: { uid?: string; email?: string; reportedBy?: string; ownershipToken?: string; adminEmail?: string }
  ): Promise<{ success: boolean; message?: string }> {
    const apiBase = getCustomApiUrl() || '';
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (userAuth?.adminEmail) headers['x-admin-email'] = userAuth.adminEmail;
    if (userAuth?.uid) headers['x-user-uid'] = userAuth.uid;
    if (userAuth?.email) headers['x-user-email'] = userAuth.email;
    if (userAuth?.reportedBy) headers['x-user-name'] = userAuth.reportedBy;
    if (userAuth?.ownershipToken) headers['x-ownership-token'] = userAuth.ownershipToken;

    try {
      const res = await safeJsonFetch<{ success: boolean; message?: string; error?: string }>(
        `${apiBase}/api/questions/${encodeURIComponent(questionId)}/reports/${encodeURIComponent(reportId)}`,
        { method: 'DELETE', headers }
      );
      if (res.ok && res.data?.success) {
        return { success: true, message: res.data.message || 'Bildirim kalıcı olarak silindi.' };
      }
      return { success: false, message: res.data?.error || res.error || 'Bildirim silinemedi.' };
    } catch (e: any) {
      return { success: false, message: e.message || 'Bağlantı hatası' };
    }
  },

  async editLearnFeedback(
    feedbackId: string,
    updates: { field?: string; reason?: string },
    userAuth?: { voterId?: string; adminEmail?: string }
  ): Promise<{ success: boolean; message?: string; item?: any }> {
    const apiBase = getCustomApiUrl() || '';
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (userAuth?.adminEmail) headers['x-admin-email'] = userAuth.adminEmail;
    if (userAuth?.voterId) headers['x-user-uid'] = userAuth.voterId;

    try {
      const res = await safeJsonFetch<{ success: boolean; item?: any; error?: string }>(
        `${apiBase}/api/learn/feedback/${encodeURIComponent(feedbackId)}`,
        { method: 'PUT', headers, body: JSON.stringify({ ...updates, voterId: userAuth?.voterId }) }
      );
      if (res.ok && res.data?.success) {
        return { success: true, message: 'Öğrenme bildirimi güncellendi.', item: res.data.item };
      }
      return { success: false, message: res.data?.error || res.error || 'Güncellenemedi.' };
    } catch (e: any) {
      return { success: false, message: e.message || 'Bağlantı hatası' };
    }
  },

  async deleteLearnFeedback(
    feedbackId: string,
    userAuth?: { voterId?: string; adminEmail?: string }
  ): Promise<{ success: boolean; message?: string }> {
    const apiBase = getCustomApiUrl() || '';
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (userAuth?.adminEmail) headers['x-admin-email'] = userAuth.adminEmail;
    if (userAuth?.voterId) headers['x-user-uid'] = userAuth.voterId;

    try {
      const res = await safeJsonFetch<{ success: boolean; message?: string; error?: string }>(
        `${apiBase}/api/learn/feedback/${encodeURIComponent(feedbackId)}`,
        { method: 'DELETE', headers, body: JSON.stringify({ voterId: userAuth?.voterId }) }
      );
      if (res.ok && res.data?.success) {
        return { success: true, message: res.data.message || 'Öğrenme bildirimi kalıcı olarak silindi.' };
      }
      return { success: false, message: res.data?.error || res.error || 'Silinemedi.' };
    } catch (e: any) {
      return { success: false, message: e.message || 'Bağlantı hatası' };
    }
  },

  async setPastQuestionReviewSuspicious(adminEmail: string, questionId: string, value: boolean): Promise<any> {
    const res = await safeJsonFetch<{ success: boolean; message: string; error?: string }>(
      `/api/past-question-reviews/${encodeURIComponent(questionId)}/suspicious`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
        body: JSON.stringify({ value }),
      }
    );
    if (!res.ok || !res.data?.success) {
      throw new Error(res.data?.error || res.error || 'İşaret güncellenemedi.');
    }
    return res.data;
  },

  /** Faz 14 ayarları: lite_kullan (Flash kotası bitince Flash-Lite yedeği) */
  async getPhase14Settings(adminEmail: string): Promise<Phase14Settings | null> {
    const res = await safeJsonFetch<Phase14Settings>('/api/past-question-reviews/settings', {
      headers: { 'x-admin-email': adminEmail },
    });
    return res.ok && res.data ? res.data : null;
  },

  async setPhase14Settings(adminEmail: string, settings: Partial<Phase14Settings>): Promise<Phase14Settings & { started?: boolean; running?: boolean }> {
    const res = await safeJsonFetch<Phase14Settings & { success: boolean; started?: boolean; running?: boolean; error?: string }>('/api/past-question-reviews/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
      body: JSON.stringify(settings),
    });
    if (!res.ok || !res.data?.success) throw new Error(res.data?.error || res.error || 'Ayar kaydedilemedi.');
    return res.data;
  },

  /** Faz 14: Redaksiyon işlemini başlat (bulut veya yerel) */
  async triggerPastQuestionReview(adminEmail: string, mode: 'cloud' | 'local' | 'free', limit: number = 10): Promise<any> {
    const res = await safeJsonFetch<{
      success: boolean;
      message: string;
      mode?: string;
      error?: string;
    }>('/api/past-question-reviews/trigger', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
      body: JSON.stringify({ mode, limit }),
    });
    if (!res.ok || !res.data?.success) {
      throw new Error(res.data?.error || res.error || 'İşlem başlatılamadı.');
    }
    return res.data;
  },

  /** Faz 14: Çalışan redaksiyon sürecini durdur */
  async stopPastQuestionReview(adminEmail: string): Promise<any> {
    const res = await safeJsonFetch<{ success: boolean; message: string; error?: string }>('/api/past-question-reviews/stop', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
    });
    if (!res.ok || !res.data?.success) {
      throw new Error(res.data?.error || res.error || 'İşlem durdurulamadı.');
    }
    return res.data;
  },

  /** Faz 14: Canlı logları ve ilerleme durumunu oku */
  async getPastQuestionReviewLogs(): Promise<{
    isRunning: boolean;
    activeMode: 'cloud' | 'local' | null;
    totalCandidate: number;
    processed: number;
    remaining: number;
    approved: number;
    pending: number;
    report: any;
    costTracking?: {
      month: string;
      total_requests: number;
      input_tokens: number;
      output_tokens: number;
      cost_usd: number;
      cost_tl: number;
      max_budget_tl: number;
      last_updated: string;
    } | null;
    paralel?: { guncelleme: string; anahtarlar: Record<string, { kalan: number; cozulen: number; bekleme_bitis: string | null; ardisik_hata: number }> } | null;
    logs: string[];
  }> {
    const res = await safeJsonFetch<{
      success: boolean;
      isRunning: boolean;
      activeMode: 'cloud' | 'local' | null;
      totalCandidate: number;
      processed: number;
      remaining: number;
      approved: number;
      pending: number;
      report: any;
      costTracking?: any;
      logs: string[];
      error?: string;
    }>('/api/past-question-reviews/logs', {
      method: 'GET',
      headers: { Accept: 'application/json' },
    });
    if (!res.ok || !res.data?.success) {
      throw new Error(res.data?.error || res.error || 'Loglar alınamadı.');
    }
    return res.data;
  },

  /** Faz 14: Beğenilmeyen/değiştirilmek istenen soru önerisini manuel düzenle */
  async updatePastQuestionReviewProposal(
    adminEmail: string,
    questionId: string,
    proposalData: {
      soru_koku?: string;
      secenekler?: Record<string, string>;
      dogru_secenek?: string;
      aciklama?: string;
      kurul_adi?: string;
      ders_adi?: string;
      konu_adi?: string;
      degisiklik_ozeti?: string;
    }
  ): Promise<{ success: boolean; message: string; review: PastQuestionReviewRecord }> {
    const res = await safeJsonFetch<{
      success: boolean;
      message: string;
      review: PastQuestionReviewRecord;
      error?: string;
    }>(`/api/past-question-reviews/${encodeURIComponent(questionId)}/proposal`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
      body: JSON.stringify(proposalData),
    });
    if (!res.ok || !res.data?.success) {
      throw new Error(res.data?.error || res.error || 'Öneri güncellenemedi.');
    }
    return res.data;
  },

  /** Faz 14: Değişiklik olmayan soruları tekrar değerlendirme kuyruğuna al */
  async reEvaluateUnchangedPastQuestionReviews(adminEmail: string, questionId?: string): Promise<{ success: boolean; message: string; count: number; questionIds?: string[] }> {
    const res = await safeJsonFetch<{
      success: boolean;
      message: string;
      count: number;
      questionIds?: string[];
      error?: string;
    }>('/api/past-question-reviews/re-evaluate-unchanged', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
      body: JSON.stringify({ questionId }),
    });
    if (!res.ok || !res.data?.success) {
      throw new Error(res.data?.error || res.error || 'Tekrar değerlendirmeye gönderilemedi.');
    }
    return res.data;
  },


  async saveApprovedPastQuestion(question: QuestionItem, adminEmailHint?: string): Promise<QuestionItem> {
    const updated: QuestionItem = {
      ...question,
      status: 'completed',
      updatedAt: new Date().toISOString(),
    };

    // 1. Express sunucusuna PUT gönder (sunucu belleği + pastQuestions.json + Supabase anında güncellenir)
    // Sunucu yazımı asıl kayıttır: başarısızsa hata fırlatılır (eskiden yutulup bildirim "çözüldü" sayılıyordu)
    const email = adminEmailHint || (typeof window !== 'undefined' && (window as any).currentUser?.email) || ADMIN_EMAIL;
    const put = await safeJsonFetch<{ success?: boolean; error?: string }>(`/api/past-exams/${encodeURIComponent(question.id)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': email },
      body: JSON.stringify(updated),
    });
    if (!put.ok) throw new Error(put.data?.error || put.error || 'Sunucu çıkmış soruyu kaydedemedi');

    // 2. İstemci IndexedDB Cache'ini anında güncelle (ekranda ve sınav listesinde hemen güncel görünür)
    try {
      await pastQuestionsCache.saveQuestion(updated);
    } catch (_) {}

    // 3. multiDbManager ile Supabase/Firestore doğrudan aynala
    try {
      await multiDbManager.savePastQuestion(updated);
    } catch (e) {
      console.warn('[ApiService] multiDbManager savePastQuestion fallback', e);
    }

    // 4. Local DB fallback
    const db = getLocalDb();
    const idx = db.questions.findIndex((item) => item.id === question.id);
    if (idx !== -1) {
      db.questions[idx] = updated;
      saveLocalDb(db);
    }

    return updated;
  },

  // Admin Custom AI Redaction for Past Exam Questions
  async adminCustomRedactQuestion(params: {
    question: QuestionItem;
    customPrompt: string;
    groundingNote?: string;
    model?: string;
    adminEmail?: string;
    apiKey?: string;
    groqApiKey?: string;
    preferredProvider?: 'gemini' | 'groq' | 'auto';
  }): Promise<{ success: boolean; reconstruction?: ReconstructedQuestion; error?: string }> {
    const customApiKey = params.apiKey ||
      (typeof window !== 'undefined' && (window as any).MEDSORU_GEMINI_KEY) ||
      localStorage.getItem('medsoru_gemini_api_key') ||
      localStorage.getItem('medsoru_custom_gemini_key') ||
      (import.meta as any).env?.VITE_GEMINI_API_KEY ||
      '';

    const customGroqKey = params.groqApiKey ||
      localStorage.getItem('medsoru_groq_api_key') ||
      '';

    const preferredProvider = params.preferredProvider ||
      (params.model?.includes('llama') || params.model?.includes('deepseek') ? 'groq' : 'auto');

    let serverErrorMsg = '';

    // 1. First try server endpoint (has server-side tiered failover & Groq)
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/ai/admin-custom-redact` : '/api/ai/admin-custom-redact';
      const res = await safeJsonFetch<{ success: boolean; reconstruction: ReconstructedQuestion; error?: string }>(
        endpoint,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ...params,
            apiKey: customApiKey,
            groqApiKey: customGroqKey,
            preferredProvider,
          }),
        }
      );

      if (res.ok && res.data?.success && res.data.reconstruction) {
        // Also update Firestore directly
        try {
          const updatedQ: QuestionItem = {
            ...params.question,
            reconstruction: res.data.reconstruction,
            status: 'completed',
            claimedAnswer: res.data.reconstruction.correctAnswer,
            updatedAt: new Date().toISOString(),
          };
          await FirestoreDbService.updatePastQuestion(updatedQ);
        } catch (_) {}
        return { success: true, reconstruction: res.data.reconstruction };
      } else {
        serverErrorMsg = res.data?.error || (res as any).error || '';
      }
    } catch (e: any) {
      serverErrorMsg = e.message || '';
    }

    return { success: false, error: serverErrorMsg || 'Yapay zeka redaksiyonu gerçekleştirilemedi.' };
  },

  // Windows Service, Desktop Shortcut & Startup Management (with Firestore Cloud Bridge)
  async getWindowsServiceStatus(): Promise<{
    success: boolean;
    isInstalledOnDesktop: boolean;
    isRegisteredInStartup: boolean;
    isRunning: boolean;
    pids: number[];
    desktopShortcutPath?: string;
    startupShortcutPath?: string;
    nextWindow?: string;
    lastHeartbeat?: any;
    error?: string;
  }> {
    // 1. Try local server endpoint
    const res = await safeJsonFetch<any>('/api/automation/windows-service-status');
    if (res.ok && res.data) {
      return res.data;
    }

    // 2. Cloud Fallback via Firestore (sunucuya ulaşılamazsa)
    try {
      const cloudHeartbeat = await FirestoreDbService.getWorkerHeartbeat();
      if (cloudHeartbeat) {
        const isFresh = Date.now() - (cloudHeartbeat.timestamp || 0) < 15 * 60 * 1000;
        return {
          success: true,
          isInstalledOnDesktop: true,
          isRegisteredInStartup: true,
          isRunning: isFresh && cloudHeartbeat.status === 'online',
          pids: cloudHeartbeat.pid ? [cloudHeartbeat.pid] : [],
          nextWindow: '16:00 - 18:00',
          lastHeartbeat: cloudHeartbeat,
        };
      }
    } catch (e) {}

    return {
      success: false,
      isInstalledOnDesktop: false,
      isRegisteredInStartup: false,
      isRunning: false,
      pids: [],
      error: res.error || 'Yerel servise doğrudan erişilemedi (Bulut köprüsüne bağlanılıyor...)',
    };
  },

  async installWindowsService(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    return await multiDbManager.sendAdminCommand('install_service', {}, adminEmail);
  },

  async stopWindowsService(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    return await multiDbManager.sendAdminCommand('stop_service', {}, adminEmail);
  },

  async sendWindowsTestNotification(title?: string, message?: string, adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    return await multiDbManager.sendAdminCommand('notify', { title, message }, adminEmail);
  },

  async runFullLocalSync(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    return await multiDbManager.sendAdminCommand('run_full_local_sync', {}, adminEmail);
  },

  async triggerSubagentRedaction(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    return await multiDbManager.sendAdminCommand('run_redactor_cycle', {}, adminEmail);
  },

  // -------------------------------------------------------------
  // Google Drive Manual Update & Sync Management
  // -------------------------------------------------------------
  async getDriveSyncSettings(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; settings: DriveSyncSettings }> {
    const res = await safeJsonFetch<any>('/api/admin/drive/settings', {
      headers: {
        'x-admin-email': adminEmail || ADMIN_EMAIL,
      },
    });
    if (res.ok && res.data?.settings) return { success: true, settings: res.data.settings };
    return {
      success: false,
      settings: {
        autoSyncEnabled: false,
        syncInterval: '18:00',
        preferredScope: 'all',
        customFolderId: '',
        notifyOnUpdate: true,
      }
    };
  },

  async saveDriveSyncSettings(settings: Partial<DriveSyncSettings>, adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string; settings?: DriveSyncSettings }> {
    const res = await safeJsonFetch<any>('/api/admin/drive/settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': adminEmail || ADMIN_EMAIL,
      },
      body: JSON.stringify({ ...settings, adminEmail: adminEmail || ADMIN_EMAIL }),
    });
    if (res.ok) return { success: true, message: res.data?.message || 'Ayarlar kaydedildi.', settings: res.data?.settings };
    return { success: false, message: res.data?.error || 'Ayarlar kaydedilemedi.' };
  },

  async getDriveCheckResult(adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; result: DriveCheckResult | null }> {
    const res = await safeJsonFetch<any>('/api/admin/drive/check-results', {
      headers: {
        'x-admin-email': adminEmail || ADMIN_EMAIL,
      },
    });
    if (res.ok) return { success: true, result: res.data?.result || null };
    return { success: false, result: null };
  },

  async checkDriveUpdates(options: { scope?: string; folderId?: string; adminEmail?: string } = {}): Promise<{
    success: boolean;
    result: DriveCheckResult | null;
    output?: string;
    message: string;
  }> {
    const email = options.adminEmail || ADMIN_EMAIL;
    const res = await safeJsonFetch<any>('/api/admin/drive/check-updates', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': email,
      },
      body: JSON.stringify({ ...options, adminEmail: email }),
    });
    if (res.ok) {
      return {
        success: res.data?.success !== false,
        result: res.data?.result || null,
        output: res.data?.output,
        message: res.data?.message || 'Kontrol tamamlandı.',
      };
    }
    return {
      success: false,
      result: null,
      message: res.data?.error || res.error || 'Drive kontrolü başarısız oldu.',
    };
  },

  async triggerManualDriveSync(options: {
    scope?: string;
    folderId?: string;
    force?: boolean;
    adminEmail?: string;
  } = {}): Promise<{ success: boolean; jobId?: string; message: string }> {
    const email = options.adminEmail || ADMIN_EMAIL;
    const res = await safeJsonFetch<any>('/api/admin/drive/manual-sync', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-admin-email': email,
      },
      body: JSON.stringify({ ...options, adminEmail: email }),
    });
    if (res.ok && res.data?.success) {
      return { success: true, jobId: res.data.jobId, message: res.data.message };
    }
    return { success: false, message: res.data?.error || res.error || 'Senkronizasyon başlatılamadı.' };
  },

  // -------------------------------------------------------------
  // Dynamic Admin Scripts & Automations
  // -------------------------------------------------------------
  async getScriptsList(): Promise<{
    success: boolean;
    scripts: AdminScriptItem[];
    pipelines: AdminPipelineItem[];
    jobs: { active: AdminScriptJob[]; history: AdminScriptJob[] };
    error?: string;
  }> {
    try {
      const res = await safeJsonFetch<any>('/api/admin/scripts/list');
      // Yedek katalog yalnız yönetim betikleri ekranında gerekir: ana pakete gömülmesin (H111d).
      const { BUNDLED_PIPELINES } = await import('../../data/bundledScripts');
      if (res.ok && Array.isArray(res.data?.scripts) && res.data.scripts.length > 0) {
        return {
          success: true,
          scripts: res.data.scripts,
          pipelines: res.data.pipelines || BUNDLED_PIPELINES,
          jobs: res.data.jobs || { active: [], history: [] },
        };
      }
    } catch (_) {}

    // Fallback: Always return guaranteed bundled catalog
    const { BUNDLED_SCRIPTS, BUNDLED_PIPELINES } = await import('../../data/bundledScripts');
    return {
      success: true,
      scripts: BUNDLED_SCRIPTS,
      pipelines: BUNDLED_PIPELINES,
      jobs: { active: [], history: [] },
    };
  },

  async runScript(
    scriptName: string,
    args: string = '',
    adminEmail: string = ADMIN_EMAIL
  ): Promise<{ success: boolean; message: string; job?: AdminScriptJob }> {
    // 1. Try local server direct call
    const res = await safeJsonFetch<any>('/api/admin/scripts/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scriptName, args, requestedBy: adminEmail }),
    });

    if (res.ok && res.data?.success) {
      return { success: true, message: res.data.message, job: res.data.job };
    }

    // 2. Cloud Fallback: Send command via Supabase bridge
    const cloudRes = await multiDbManager.sendAdminCommand('run_script', { scriptName, args }, adminEmail);
    return {
      success: cloudRes.success,
      message: cloudRes.message || `${scriptName} bulut kuyruğuna iletildi.`,
    };
  },

  async runScriptPipeline(
    pipelineId: string,
    adminEmail: string = ADMIN_EMAIL
  ): Promise<{ success: boolean; message: string; job?: AdminScriptJob }> {
    const res = await safeJsonFetch<any>('/api/admin/scripts/pipeline/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pipelineId, requestedBy: adminEmail }),
    });

    if (res.ok && res.data?.success) {
      return { success: true, message: res.data.message, job: res.data.job };
    }

    const cloudRes = await multiDbManager.sendAdminCommand('run_pipeline', { pipelineId }, adminEmail);
    return {
      success: cloudRes.success,
      message: cloudRes.message || `Pipeline (${pipelineId}) bulut kuyruğuna iletildi.`,
    };
  },

  async getScriptJobStatus(jobId: string): Promise<{ success: boolean; job?: AdminScriptJob; error?: string }> {
    const res = await safeJsonFetch<any>(`/api/admin/scripts/jobs/${encodeURIComponent(jobId)}`);
    if (res.ok && res.data?.job) {
      return { success: true, job: res.data.job };
    }
    return { success: false, error: res.error || 'İşlem detayları alınamadı.' };
  },

  async stopScriptJob(jobId: string, adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; message: string }> {
    const res = await safeJsonFetch<any>(`/api/admin/scripts/jobs/${encodeURIComponent(jobId)}/kill`, {
      method: 'POST',
    });
    if (res.ok && res.data?.success) {
      return { success: true, message: res.data.message };
    }
    return await multiDbManager.sendAdminCommand('stop_script', { jobId }, adminEmail);
  },

  async getRagStatus(): Promise<any> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/rag/status` : `/api/rag/status`;
      const res = await safeJsonFetch<any>(endpoint);
      return res.ok && res.data?.success ? res.data : null;
    } catch (_) {
      return null;
    }
  },

  async triggerQualityAudit(): Promise<any> {
    try {
      const customUrl = getCustomApiUrl();
      const endpoint = customUrl ? `${customUrl}/api/audit/trigger` : `/api/audit/trigger`;
      const res = await safeJsonFetch<any>(endpoint, { method: 'POST' });
      return res.ok && res.data?.success ? res.data : null;
    } catch (_) {
      return null;
    }
  },

  // -------------------------------------------------------------
  // Admin Mobile & Web Push & Email Notification Service
  // -------------------------------------------------------------
  async getAdminPushStatus(adminEmail: string = ADMIN_EMAIL): Promise<{
    success: boolean;
    adminEmail: string;
    deviceCount: number;
    devices: Array<{ endpoint: string; userAgent?: string; createdAt: string }>;
    recentNotifications: any[];
    emailEnabled: boolean;
  }> {
    const res = await safeJsonFetch<any>('/api/admin/push/status', {
      headers: { 'x-admin-email': adminEmail },
    });
    if (!res.ok) throw new Error(res.error || 'Bildirim durumu okunamadı.');
    return res.data;
  },

  async getAdminVapidPublicKey(adminEmail: string = ADMIN_EMAIL): Promise<string> {
    try {
      const res = await safeJsonFetch<{ success: boolean; publicKey: string }>('/api/admin/push/vapid-public-key', {
        headers: { 'x-admin-email': adminEmail },
      });
      if (res.ok && res.data?.publicKey) return res.data.publicKey;
    } catch (_) {}
    return 'BI6Q_ruuWLdDrA8E0xEmNtVmko7dcnfax3WYH7201eFoJqlbshzwMTveNyAJBwEJjk3h7qeS9pYsh2mD2wiKnPI';
  },

  async subscribeAdminPush(subscription: any, adminEmail: string = ADMIN_EMAIL): Promise<any> {
    // 1. Try local server
    try {
      const res = await safeJsonFetch<{ success: boolean; message: string }>('/api/admin/push/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
        body: JSON.stringify({ subscription }),
      });
      if (res.ok) return res.data;
    } catch (_) {}

    // 2. Direct Supabase sync (Ensures mobile devices on nofrostlife.com.tr are registered)
    try {
      const client = getSupabaseClient();
      if (client) {
        const { data: existing } = await client.from('system_status').select('data').eq('id', 'admin_push_subscriptions').maybeSingle();
        const curSubs: any[] = existing?.data?.subscriptions || [];
        const filtered = curSubs.filter((s: any) => s.endpoint !== subscription.endpoint);
        filtered.push({
          ...subscription,
          userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : 'Mobil Web',
          createdAt: new Date().toISOString()
        });

        await client.from('system_status').upsert([{
          id: 'admin_push_subscriptions',
          data: { subscriptions: filtered },
          updated_at: new Date().toISOString()
        }]);
        return { success: true, message: 'Mobil bildirim aboneliği buluta kaydedildi.' };
      }
    } catch (e: any) {
      console.warn('subscribeAdminPush Supabase fallback error:', e?.message);
    }
    return { success: true, message: 'Bildirim aboneliği tarayıcıda etkinleştirildi.' };
  },

  async unsubscribeAdminPush(endpoint: string, adminEmail: string = ADMIN_EMAIL): Promise<any> {
    try {
      await safeJsonFetch<{ success: boolean; message: string }>('/api/admin/push/unsubscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
        body: JSON.stringify({ endpoint }),
      });
    } catch (_) {}

    try {
      const client = getSupabaseClient();
      if (client) {
        const { data: existing } = await client.from('system_status').select('data').eq('id', 'admin_push_subscriptions').maybeSingle();
        const curSubs: any[] = existing?.data?.subscriptions || [];
        const filtered = curSubs.filter((s: any) => s.endpoint !== endpoint);
        await client.from('system_status').upsert([{
          id: 'admin_push_subscriptions',
          data: { subscriptions: filtered },
          updated_at: new Date().toISOString()
        }]);
      }
    } catch (_) {}

    return { success: true, message: 'Abonelik iptal edildi.' };
  },

  async sendAdminPushTest(adminEmail: string = ADMIN_EMAIL): Promise<any> {
    try {
      const res = await safeJsonFetch<{ success: boolean; message: string }>('/api/admin/push/test', {
        method: 'POST',
        headers: { 'x-admin-email': adminEmail },
      });
      if (res.ok) return res.data;
    } catch (_) {}

    try {
      const res = await SupabaseDbService.sendAdminCommand('test_admin_push', { trigger: 'mobile_ui_test' }, adminEmail);
      if (res.success) {
        return { success: true, message: 'Test komutu buluta iletildi, sunucu telefonunuza push gönderecek.' };
      }
    } catch (_) {}

    return { success: false, message: 'Test bildirimi başlatılamadı.' };
  },

  async sendAdminEmailTest(adminEmail: string = ADMIN_EMAIL): Promise<any> {
    try {
      const res = await safeJsonFetch<{ success: boolean; message: string }>('/api/admin/notifications/test-email', {
        method: 'POST',
        headers: { 'x-admin-email': adminEmail },
      });
      if (res.ok) return res.data;
    } catch (_) {}

    try {
      const res = await SupabaseDbService.sendAdminCommand('test_admin_email', { trigger: 'mobile_ui_test' }, adminEmail);
      if (res.success) {
        return { success: true, message: 'Test e-posta komutu buluta iletildi.' };
      }
    } catch (_) {}

    return { success: false, message: 'Test e-postası başlatılamadı.' };
  },

  async toggleAdminEmail(enabled: boolean, adminEmail: string = ADMIN_EMAIL): Promise<{ success: boolean; emailEnabled: boolean; message: string }> {
    const res = await safeJsonFetch<{ success: boolean; emailEnabled: boolean; message: string }>('/api/admin/notifications/toggle-email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
      body: JSON.stringify({ enabled }),
    });
    if (!res.ok || !res.data) throw new Error(res.error || 'E-posta bildirim ayarı değiştirilemedi.');
    return res.data;
  },

  async getAdminRecentNotifications(limit = 50, adminEmail: string = ADMIN_EMAIL): Promise<any[]> {
    const res = await safeJsonFetch<{ success: boolean; notifications: any[] }>(`/api/admin/notifications/recent?limit=${limit}`, {
      headers: { 'x-admin-email': adminEmail },
    });
    return res.data?.notifications || [];
  },

  async markAdminNotificationRead(id?: string, adminEmail: string = ADMIN_EMAIL): Promise<void> {
    await safeJsonFetch('/api/admin/notifications/mark-read', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-admin-email': adminEmail },
      body: JSON.stringify({ id }),
    });
  },

  async contributeToPoolCluster(
    clusterId: string,
    studentName: string,
    text: string,
    studentUid?: string
  ): Promise<{ success: boolean; contribution: any; cluster: any }> {
    const res = await safeJsonFetch<{ success: boolean; contribution: any; cluster: any }>(
      `/api/pool-clusters/${encodeURIComponent(clusterId)}/contribute`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ studentName, text, studentUid }),
      }
    );
    if (!res.ok || !res.data) throw new Error(res.error || 'Katkı eklenemedi.');
    return res.data;
  },

  /** Yönetici: öneri taslağından bir parçayı "farklı soru" diye ayırır (kalıcı); güncel küme listesini döner. */
  async splitPoolClusterMember(clusterId: string, key: string): Promise<any[]> {
    const res = await safeJsonFetch<{ success: boolean; clusters: any[] }>(`/api/pool-clusters/${encodeURIComponent(clusterId)}/split`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key }),
    });
    if (!res.ok || !res.data) throw new Error(res.error || 'Parça ayrılamadı.');
    return res.data.clusters || [];
  },

  async runPoolQuestionClusterPipeline(): Promise<{ success: boolean; message: string }> {
    const res = await safeJsonFetch<{ success: boolean; message: string }>('/api/pool-clusters/run-pipeline', {
      method: 'POST',
    });
    if (!res.ok || !res.data) throw new Error(res.error || 'Otomasyon başlatılamadı.');
    return res.data;
  },};
