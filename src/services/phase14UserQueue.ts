/**
 * Faz 14 kullanıcı kuyruğu (yalnız sunucu).
 *
 * Kullanıcılar bir çıkmış soruyu "yapay zekâ incelemesine" gönderebilir; hatalı soru bildirimleri de buraya düşer.
 * Kuyruğu yalnız sunucu yazar (kullanici_kuyrugu.json). Faz 14 betiği (--kullanici-kuyrugu) "bekliyor" istekleri
 * okur, yalnız ücretsiz anahtarlarla inceler ve sonucu ayrı bir dosyaya ekler (kullanici_sonuclari.jsonl).
 * Böylece iki süreç aynı dosyaya yazmaz. Sunucu sonuçları okuyup soruyu otomatik günceller ve bildirenlere e-posta atar.
 */
import fs from 'fs';
import path from 'path';

export type QueueStatus = 'bekliyor' | 'guncellendi' | 'degisiklik_yok' | 'yonetici_onayi' | 'hata';
export type QueueKind = 'inceleme' | 'hata';

export interface QueueNote {
  kind: QueueKind;
  name: string;
  uid?: string;
  /** Yalnız bu yerel dosyada tutulur; soru kaydına ya da buluta yazılmaz. */
  email?: string;
  isAdmin?: boolean;
  reason?: string;
  message?: string;
  at: string;
}

export interface QueueItem {
  id: string;
  questionId: string;
  questionNumber?: string | number;
  status: QueueStatus;
  notes: QueueNote[];
  createdAt: string;
  updatedAt: string;
  /** Betik bu isteği işlediğinde yazdığı inceleme kaydının zamanı */
  reviewProcessedAt?: string;
  resultNote?: string;
  mailedTo?: string[];
}

export interface QueueResult {
  istek_id: string;
  question_id: string;
  ok: boolean;
  processed_at?: string;
  model?: string;
  error?: string;
}

const clip = (s: unknown, n: number) => String(s ?? '').trim().slice(0, n);

export function createPhase14UserQueue(dir: string) {
  const queueFile = path.join(dir, 'kullanici_kuyrugu.json');
  const resultsFile = path.join(dir, 'kullanici_sonuclari.jsonl');

  const read = (): QueueItem[] => {
    try {
      const d = JSON.parse(fs.readFileSync(queueFile, 'utf-8'));
      return Array.isArray(d) ? d : [];
    } catch {
      return [];
    }
  };
  const write = (items: QueueItem[]) => {
    fs.mkdirSync(dir, { recursive: true });
    // Tamamlananların yalnız son 2000'i tutulur
    const open = items.filter((i) => i.status === 'bekliyor' || i.status === 'yonetici_onayi');
    const closed = items.filter((i) => !(i.status === 'bekliyor' || i.status === 'yonetici_onayi')).slice(-2000);
    const tmp = `${queueFile}.tmp`;
    fs.writeFileSync(tmp, JSON.stringify([...closed, ...open], null, 1), 'utf-8');
    fs.renameSync(tmp, queueFile);
  };

  const readResults = (): QueueResult[] => {
    try {
      return fs
        .readFileSync(resultsFile, 'utf-8')
        .split('\n')
        .filter(Boolean)
        .map((l) => {
          try {
            return JSON.parse(l);
          } catch {
            return null;
          }
        })
        .filter(Boolean) as QueueResult[];
    } catch {
      return [];
    }
  };

  /** Soruya not ekler; aynı soru için bekleyen istek varsa ona eklenir (tek inceleme, tüm notlar). */
  const enqueue = (questionId: string, note: Omit<QueueNote, 'at'>, questionNumber?: string | number) => {
    const items = read();
    const now = new Date().toISOString();
    const clean: QueueNote = {
      kind: note.kind,
      name: clip(note.name, 80) || 'Tıp öğrencisi',
      uid: clip(note.uid, 128) || undefined,
      email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(note.email || '')) ? clip(note.email, 160).toLowerCase() : undefined,
      isAdmin: !!note.isAdmin,
      reason: clip(note.reason, 200) || undefined,
      message: clip(note.message, 1500) || undefined,
      at: now,
    };
    let item = items.find((i) => i.questionId === questionId && i.status === 'bekliyor');
    let joined = false;
    if (item) {
      // Aynı kişi aynı mesajı ikinci kez gönderirse yinelenmez
      const dup = item.notes.some((n) => n.kind === clean.kind && (n.uid || n.name) === (clean.uid || clean.name) && n.message === clean.message && n.reason === clean.reason);
      if (!dup) item.notes.push(clean);
      item.updatedAt = now;
      joined = true;
    } else {
      item = {
        id: `fq-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`,
        questionId,
        questionNumber,
        status: 'bekliyor',
        notes: [clean],
        createdAt: now,
        updatedAt: now,
      };
      items.push(item);
    }
    write(items);
    const pending = items.filter((i) => i.status === 'bekliyor');
    return { item, joined, position: pending.findIndex((i) => i.id === item!.id) + 1, waiting: pending.length };
  };

  /** Sitenin gösterdiği özet: bekleyen ve yönetici onayı bekleyen soruların sırası (kişisel veri yok). */
  const publicStatus = () => {
    const items = read();
    const pending = items.filter((i) => i.status === 'bekliyor');
    const out: Record<string, { status: QueueStatus; position?: number; requests: number }> = {};
    pending.forEach((i, k) => (out[i.questionId] = { status: i.status, position: k + 1, requests: i.notes.length }));
    items.filter((i) => i.status === 'yonetici_onayi').forEach((i) => (out[i.questionId] = { status: i.status, requests: i.notes.length }));
    return { waiting: pending.length, items: out };
  };

  const pendingCount = () => read().filter((i) => i.status === 'bekliyor').length;

  /** Betiğin yazdığı ve henüz işlenmemiş sonuçlar */
  const unconsumedResults = () => {
    const items = read();
    const byId = new Map(items.map((i) => [i.id, i]));
    return readResults().filter((r) => byId.get(r.istek_id)?.status === 'bekliyor');
  };

  const update = (id: string, patch: Partial<QueueItem>) => {
    const items = read();
    const it = items.find((i) => i.id === id);
    if (!it) return null;
    Object.assign(it, patch, { updatedAt: new Date().toISOString() });
    write(items);
    return it;
  };

  const find = (id: string) => read().find((i) => i.id === id) || null;
  const openForQuestion = (questionId: string, status: QueueStatus) => read().filter((i) => i.questionId === questionId && i.status === status);

  return { read, enqueue, publicStatus, pendingCount, unconsumedResults, update, find, openForQuestion, queueFile, resultsFile };
}

export type Phase14UserQueue = ReturnType<typeof createPhase14UserQueue>;
