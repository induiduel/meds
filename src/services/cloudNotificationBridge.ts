import fs from 'fs';
import path from 'path';
import type { SupabaseClient } from '@supabase/supabase-js';
import { db } from './firestoreDb.ts';
import { collection, getDocs, query, orderBy, limit } from 'firebase/firestore';

export interface CloudBridgeOptions {
  dataDir: string;
  cloudSupabase: SupabaseClient;
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
  private cloudSupabase: SupabaseClient;
  private onNewNotification: CloudBridgeOptions['onNewNotification'];
  private onSyncSubscriptions?: CloudBridgeOptions['onSyncSubscriptions'];
  private processedIds: Set<string> = new Set();
  private timer: NodeJS.Timeout | null = null;
  private isChecking = false;

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

  public start(intervalMs = 10000) {
    if (this.timer) return;
    console.log(`[CloudNotificationBridge] Bulut bildirim köprüsü başlatıldı (Aralık: ${intervalMs / 1000}s).`);
    // İlk kontrol
    this.check();
    this.timer = setInterval(() => this.check(), intervalMs);
  }

  public stop() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
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

          // Yeni bildirim yakalandı, mail ve push tetikle
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
        // 1. Reports kontrolü
        if (Array.isArray(row.reports) && row.reports.length > 0) {
          for (const r of row.reports) {
            const repKey = r.id ? `rep-${r.id}` : `rep-${row.id}-${r.timestamp || r.createdAt || r.reason}`;
            if (!this.processedIds.has(repKey)) {
              this.processedIds.add(repKey);
              this.saveProcessedIds();

              console.log(`[CloudBridge] 🚨 Supabase past_questions içinde yeni hata bildirimi tespit edildi (#${row.id})`);
              this.onNewNotification({
                type: 'report',
                questionId: row.id,
                reason: r.reason || 'Hata Bildirimi',
                details: r.details || '',
                author: r.reportedBy || 'Tıp Öğrencisi',
                discipline: row.discipline,
                topic: row.topic,
              });
            }
          }
        }

        // 2. Comments kontrolü
        if (Array.isArray(row.comments) && row.comments.length > 0) {
          for (const c of row.comments) {
            const commKey = c.id ? `comm-${c.id}` : `comm-${row.id}-${c.timestamp || c.createdAt || c.text}`;
            if (!this.processedIds.has(commKey)) {
              this.processedIds.add(commKey);
              this.saveProcessedIds();

              console.log(`[CloudBridge] 💬 Supabase past_questions içinde yeni yorum tespit edildi (#${row.id})`);
              this.onNewNotification({
                type: 'comment',
                questionId: row.id,
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
                questionId: row.id,
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

      // 1. Mobil Push Aboneliklerini Senkronize Et
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
