/**
 * Öğrenci kararları (Soru ekle): önerilen havuz kaydı için "aynı soru" (bağladı / birleştirdi) ya da "farklı soru"
 * (öneriyi reddetti). `data/recall_feedback.jsonl`'e eklenir; scripts/recall/learn.mts bunlarla çift modelini yeniden
 * öğrenir. Metin kişisel veriden maskelenir; kimlik/e-posta yazılmaz.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { maskPersonal } from '../questionIntake.ts';

export type RecallDecision = 'ayni' | 'farkli';
export interface RecallFeedback { at: string; committeeId: string; questionId: string; decision: RecallDecision; prob: number | null; text: string; engine: string }

export const FEEDBACK_FILE = 'recall_feedback.jsonl';

export function readFeedback(dataDir: string): RecallFeedback[] {
  try {
    return fs.readFileSync(path.join(dataDir, FEEDBACK_FILE), 'utf8').split('\n').filter(Boolean).map((l) => JSON.parse(l));
  } catch {
    return [];
  }
}

/** Aynı metin + kayıt için son karar geçerlidir (öğrenci fikrini değiştirebilir). */
export function latestDecisions(list: RecallFeedback[]): RecallFeedback[] {
  const m = new Map<string, RecallFeedback>();
  for (const f of list) m.set(`${crypto.createHash('sha1').update(f.text).digest('hex')}|${f.questionId}`, f);
  return [...m.values()];
}

export function createRecallFeedback(dataDir: string) {
  const file = path.join(dataDir, FEEDBACK_FILE);
  const recent = new Map<string, number>(); // ip → bu saatteki kayıt sayısı (kötüye kullanım sınırı)
  let hourAt = Date.now();
  let chain = Promise.resolve();
  let count = readFeedback(dataDir).length;
  return {
    count: () => count,
    record(input: { committeeId: string; questionId: string; decision: RecallDecision; prob?: number | null; text: string; engine: string; ip?: string }): boolean {
      if (Date.now() - hourAt > 3_600_000) { recent.clear(); hourAt = Date.now(); }
      const ip = input.ip || '-';
      const n = (recent.get(ip) || 0) + 1;
      if (n > 120) return false;
      recent.set(ip, n);
      const row: RecallFeedback = {
        at: new Date().toISOString(),
        committeeId: input.committeeId,
        questionId: input.questionId,
        decision: input.decision,
        prob: typeof input.prob === 'number' && Number.isFinite(input.prob) ? Math.round(input.prob * 100) / 100 : null,
        text: maskPersonal(input.text).slice(0, 2000),
        engine: input.engine,
      };
      count++;
      chain = chain.then(() => fs.promises.appendFile(file, JSON.stringify(row) + '\n', 'utf8')).catch((e) => console.warn('[Geri bildirim] yazılamadı:', e?.message));
      return true;
    },
  };
}
