import fs from 'fs';
import path from 'path';
import { db } from './firestoreDb.ts';
import { collection, getDocs, query, orderBy, limit, onSnapshot } from 'firebase/firestore';

export interface CloudBridgeOptions {
  dataDir: string;
  /** Eski bulut Supabase köprüsü; Supabase kaldırıldı, null verilir (yalnız Firebase dinlenir). */
  cloudSupabase: any | null;
  onNewNotification: (params: {
    type: 'report' | 'comment' | 'test';
    questionId: string;
    reason?: string;
    details?: string;
    text?: string;
    author?: string;
    discipline?: string;
    topic?: string;
  }) => void;
  onSyncSubscriptions?: (subscriptions: any[]) => void;
}

export class CloudNotificationBridge {
  private dataDir: string;
  private idsFile: string;
  private cloudSupabase: any | null;
  private onNewNotification: CloudBridgeOptions['onNewNotification'];
  private onSyncSubscriptions?: CloudBridgeOptions['onSyncSubscriptions'];
  private processedIds: Set<string> = new Set();
  private timer: NodeJS.Timeout | null = null;
  private isChecking = false;
  private firestoreUnsub: (() => void) | null = null;
  private supabaseChannel: any = null;

  constructor(opts: CloudBridgeOptions) {
    this.dataDir = opts.dataDir;
    this.cloudSupabase = opts.cloudSupabase;
    this.onNewNotification = opts.onNewNotification;
    this.onSyncSubscriptions = opts.onSyncSubscriptions;
    this.idsFile = path.resolve(this.dataDir, 'processed_notification_ids.json');
    this.loadProcessedIds();
  }

  private loadProcessedIds() {
    try {
      if (fs.existsSync(this.idsFile)) {
        const arr = JSON.parse(fs.readFileSync(this.idsFile, 'utf-8'));
        if (Array.isArray(arr)) {
          this.processedIds = new Set(arr);
        }
      }
    } catch (_) {}
  }

  private saveProcessedIds() {
    try {
      const arr = Array.from(this.processedIds).slice(-1500);
      fs.writeFileSync(this.idsFile, JSON.stringify(arr, null, 2), 'utf-8');
    } catch (_) {}
  }

  /**
   * Hem Realtime WebSocket dinleyicilerini (Supabase + Firebase) hem de yedek polling döngüsünü başlatır.
   */
  public start(intervalMs = 10000) {
    console.log(`[CloudNotificationBridge] ⚡ Realtime Bildirim Köprüsü başlatılıyor...`);

    // 1. Firebase Realtime (Firestore onSnapshot) Dinleyicisi
    this.setupFirebaseRealtime();

    // 2. Supabase Realtime (WebSocket postgres_changes) Dinleyicisi
    this.setupSupabaseRealtime();

    // 3. İlk Kontrol & Güvenlik Yedek Döngüsü (Polling)
    this.check();
    if (!this.timer) {
      this.timer = setInterval(() => this.check(), intervalMs);
    }
  }

  public stop() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
    if (this.firestoreUnsub) {
      try { this.firestoreUnsub(); } catch (_) {}
      this.firestoreUnsub = null;
    }
    if (this.supabaseChannel && this.cloudSupabase) {
      try { this.cloudSupabase.removeChannel(this.supabaseChannel); } catch (_) {}
      this.supabaseChannel = null;
    }
  }

  /**
   * Firebase Firestore Realtime Listener:
   * Yeni admin bildirimleri veya hata raporları eklendiğinde 0 gecikmeyle WebSocket ile tetiklenir.
   */
  private setupFirebaseRealtime() {
    try {
      const q = query(collection(db, 'admin_notifications'), orderBy('timestamp', 'desc'), limit(15));
      this.firestoreUnsub = onSnapshot(
        q,
        (snap) => {
          snap.docChanges().forEach((change) => {
            if (change.type === 'added') {
              const data = change.doc.data();
              const id = change.doc.id;
              if (!this.processedIds.has(id)) {
                this.processedIds.add(id);
                this.saveProcessedIds();

                console.log(`[CloudBridge] 🔥 Firebase Realtime: Yeni bildirim yakalandı (#${data.questionId || id})!`);
                const type = (data.type === 'comment' ? 'comment' : 'report') as 'report' | 'comment';
                this.onNewNotification({
                  type,
                  questionId: data.questionId || 'Genel',
                  reason: data.title || data.reason,
                  details: data.message || data.details,
                  text: data.text || data.message,
                  author: data.author || 'Tıp Öğrencisi',
                  discipline: data.discipline,
                  topic: data.topic,
                });
              }
            }
          });
        },
        (err) => {
          console.warn('[CloudBridge] Firebase Realtime dinleme uyarısı (polling devrede):', err.message);
        }
      );
      console.log('[CloudBridge] 🔥 Firebase Realtime (Firestore onSnapshot) aktif.');
    } catch (e: any) {
      console.warn('[CloudBridge] Firebase Realtime başlatılamadı:', e.message);
    }
  }

  /**
   * Supabase Realtime Listener:
   * 'past_question_reports', 'past_questions' ve 'questions' tablolarında INSERT/UPDATE olduğunda
   * WebSocket ile derhal tetiklenir.
   */
  private setupSupabaseRealtime() {
    try {
      if (!this.cloudSupabase) return;

      this.supabaseChannel = this.cloudSupabase
        .channel('realtime_error_notifications')
        // 1. Doğrudan rapor tablosu (varsa)
        .on(
          'postgres_changes',
          { event: 'INSERT', schema: 'public', table: 'past_question_reports' },
          (payload: any) => {
            const r = payload?.new;
            if (!r) return;
            const repKey = `sb-rep-${r.id || Date.now()}`;
            if (!this.processedIds.has(repKey)) {
              this.processedIds.add(repKey);
              this.saveProcessedIds();

              console.log(`[CloudBridge] ⚡ Supabase Realtime: Yeni çıkmış soru hata bildirimi yakalandı (#${r.question_id})!`);
              this.onNewNotification({
                type: 'report',
                questionId: String(r.question_id || ''),
                reason: r.reason || 'Hata Bildirimi',
                details: r.details || '',
                author: r.reported_by || 'Tıp Öğrencisi',
              });
            }
          }
        )
        // 2. past_questions güncellemesi (reports alanı yenilendiğinde)
        .on(
          'postgres_changes',
          { event: 'UPDATE', schema: 'public', table: 'past_questions' },
          (payload: any) => {
            const row = payload?.new;
            if (!row || !Array.isArray(row.reports) || row.reports.length === 0) return;
            for (const r of row.reports) {
              const repKey = r.id ? `rep-${r.id}` : `rep-${row.id}-${r.timestamp || r.createdAt || r.reason}`;
              if (!this.processedIds.has(repKey)) {
                this.processedIds.add(repKey);
                this.saveProcessedIds();

                console.log(`[CloudBridge] ⚡ Supabase Realtime: past_questions içinde yeni hata yakalandı (#${row.id})!`);
                this.onNewNotification({
                  type: 'report',
                  questionId: String(row.id),
                  reason: r.reason || 'Hata Bildirimi',
                  details: r.details || '',
                  author: r.reportedBy || 'Tıp Öğrencisi',
                  discipline: row.discipline,
                  topic: row.topic,
                });
              }
            }
          }
        )
        // 3. questions (havuz) güncellemesi
        .on(
          'postgres_changes',
          { event: 'UPDATE', schema: 'public', table: 'questions' },
          (payload: any) => {
            const row = payload?.new;
            if (!row || !Array.isArray(row.reports) || row.reports.length === 0) return;
            for (const r of row.reports) {
              const repKey = r.id ? `rep-${r.id}` : `pool-rep-${row.id}-${r.timestamp || r.createdAt}`;
              if (!this.processedIds.has(repKey)) {
                this.processedIds.add(repKey);
                this.saveProcessedIds();

                console.log(`[CloudBridge] ⚡ Supabase Realtime: havuz sorusunda yeni hata yakalandı (#${row.id})!`);
                this.onNewNotification({
                  type: 'report',
                  questionId: String(row.id),
                  reason: r.reason || 'Hata Bildirimi',
                  details: r.details || '',
                  author: r.reportedBy || 'Tıp Öğrencisi',
                  discipline: row.discipline,
                  topic: row.topic,
                });
              }
            }
          }
        )
        .subscribe((status: string) => {
          console.log(`[CloudBridge] ⚡ Supabase Realtime kanal durumu: ${status}`);
        });
    } catch (e: any) {
      console.warn('[CloudBridge] Supabase Realtime başlatılamadı:', e.message);
    }
  }

  public async check() {
    if (this.isChecking) return;
    this.isChecking = true;

    try {
      await Promise.all([
        this.checkFirestoreNotifications(),
        this.checkSupabasePastQuestions(),
        this.checkSupabasePoolQuestions(),
        this.checkSupabaseSystemStatus()
      ]);
    } catch (err: any) {
      // sessizce geç
    } finally {
      this.isChecking = false;
    }
  }

  private async checkFirestoreNotifications() {
    try {
      const q = query(collection(db, 'admin_notifications'), orderBy('timestamp', 'desc'), limit(15));
      const snap = await getDocs(q);
      snap.forEach((doc) => {
        const data = doc.data();
        const id = doc.id;
        if (!this.processedIds.has(id)) {
          this.processedIds.add(id);
          this.saveProcessedIds();

          const type = (data.type === 'comment' ? 'comment' : 'report') as 'report' | 'comment';
          this.onNewNotification({
            type,
            questionId: data.questionId || 'Genel',
            reason: data.title || data.reason,
            details: data.message || data.details,
            text: data.text || data.message,
            author: data.author || 'Tıp Öğrencisi',
            discipline: data.discipline,
            topic: data.topic,
          });
        }
      });
    } catch (_) {}
  }

  private async checkSupabasePastQuestions() {
    try {
      if (!this.cloudSupabase) return;
      const { data, error } = await this.cloudSupabase
        .from('past_questions')
        .select('id, updated_at, topic, discipline, reports, comments')
        .order('updated_at', { ascending: false })
        .limit(30);

      if (error || !Array.isArray(data)) return;

      for (const row of data) {
        if (Array.isArray(row.reports) && row.reports.length > 0) {
          for (const r of row.reports) {
            const repKey = r.id ? `rep-${r.id}` : `rep-${row.id}-${r.timestamp || r.createdAt || r.reason}`;
            if (!this.processedIds.has(repKey)) {
              this.processedIds.add(repKey);
              this.saveProcessedIds();

              console.log(`[CloudBridge] 🚨 Supabase past_questions içinde yeni hata bildirimi tespit edildi (#${row.id})`);
              this.onNewNotification({
                type: 'report',
                questionId: String(row.id),
                reason: r.reason || 'Hata Bildirimi',
                details: r.details || '',
                author: r.reportedBy || 'Tıp Öğrencisi',
                discipline: row.discipline,
                topic: row.topic,
              });
            }
          }
        }

        if (Array.isArray(row.comments) && row.comments.length > 0) {
          for (const c of row.comments) {
            const commKey = c.id ? `comm-${c.id}` : `comm-${row.id}-${c.timestamp || c.createdAt || c.text}`;
            if (!this.processedIds.has(commKey)) {
              this.processedIds.add(commKey);
              this.saveProcessedIds();

              this.onNewNotification({
                type: 'comment',
                questionId: String(row.id),
                text: c.text || '',
                author: c.author || 'Tıp Öğrencisi',
                discipline: row.discipline,
                topic: row.topic,
              });
            }
          }
        }
      }
    } catch (e: any) {
      console.warn('[CloudBridge] checkSupabasePastQuestions uyarısı:', e?.message);
    }
  }

  private async checkSupabasePoolQuestions() {
    try {
      if (!this.cloudSupabase) return;
      const { data, error } = await this.cloudSupabase
        .from('questions')
        .select('id, updated_at, topic, discipline, reports, comments')
        .order('updated_at', { ascending: false })
        .limit(20);

      if (error || !Array.isArray(data)) return;

      for (const row of data) {
        if (Array.isArray(row.reports) && row.reports.length > 0) {
          for (const r of row.reports) {
            const repKey = r.id ? `rep-${r.id}` : `pool-rep-${row.id}-${r.timestamp || r.createdAt}`;
            if (!this.processedIds.has(repKey)) {
              this.processedIds.add(repKey);
              this.saveProcessedIds();

              this.onNewNotification({
                type: 'report',
                questionId: String(row.id),
                reason: r.reason || 'Hata Bildirimi',
                details: r.details || '',
                author: r.reportedBy || 'Tıp Öğrencisi',
                discipline: row.discipline,
                topic: row.topic,
              });
            }
          }
        }
      }
    } catch (_) {}
  }

  private async checkSupabaseSystemStatus() {
    try {
      if (!this.cloudSupabase) return;

      const { data: subData } = await this.cloudSupabase
        .from('system_status')
        .select('data')
        .eq('id', 'admin_push_subscriptions')
        .maybeSingle();

      if (subData?.data?.subscriptions && Array.isArray(subData.data.subscriptions)) {
        if (this.onSyncSubscriptions) {
          this.onSyncSubscriptions(subData.data.subscriptions);
        }
      }
    } catch (_) {}
  }
}
