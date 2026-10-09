/**
 * Öğren ders ekranı geri bildirimleri (sunucu tarafı): öğrenciler bir etkinlikte, tabloda ya da bilgi
 * kutusunda gördükleri hatayı bildirir; diğer öğrenciler bildirimi beğenir ya da reddeder.
 * Kayıtlar data/learn_feedback.json içinde tutulur (yerel JSON veritabanı düzeni).
 */
import fs from 'fs';
import path from 'path';

export interface LearnFeedbackAuthor { id: string; name: string }
export interface LearnFeedback {
  id: string;
  deckId: string;
  slideNumber: number;
  targetKey: string;
  targetLabel: string;
  /** Öğenin ekrandaki yeri (ör. "Pekiştir › Gizli tablo") */
  location: string;
  deckTitle: string;
  /** Yöneticinin tıklayınca öğeye gittiği bağlantı (uygulama kökünden yol) */
  link: string;
  /** Hangi bilgi yanlış */
  field: string;
  /** Neden yanlış / doğrusu ne */
  reason: string;
  author: LearnFeedbackAuthor;
  createdAt: string;
  status: 'open' | 'resolved';
  votes: Record<string, 1 | -1>;
}
export type LearnFeedbackView = Omit<LearnFeedback, 'votes'> & { up: number; down: number; myVote: 0 | 1 | -1; mine: boolean };

const clip = (v: unknown, n: number) => String(v ?? '').replace(/\s+/g, ' ').trim().slice(0, n);
const ID_RE = /^[\p{L}\p{N}._:-]{1,160}$/u;

/** Öğeye giden derin bağlantı: ders bu adımda açılır, öğe vurgulanır. */
export const learnFeedbackLink = (deckId: string, slideNumber: number, targetKey: string) =>
  `/ogren/${encodeURIComponent(deckId)}?adim=${slideNumber}&hedef=${encodeURIComponent(targetKey)}`;

export function createLearnFeedbackStore(dataDir: string) {
  const file = path.join(dataDir, 'learn_feedback.json');
  let cache: LearnFeedback[] | null = null;

  const load = (): LearnFeedback[] => {
    if (cache) return cache;
    try {
      const raw = JSON.parse(fs.readFileSync(file, 'utf8'));
      cache = Array.isArray(raw) ? raw : [];
    } catch {
      cache = [];
    }
    return cache;
  };
  const save = () => {
    fs.mkdirSync(dataDir, { recursive: true });
    const tmp = `${file}.tmp`;
    fs.writeFileSync(tmp, JSON.stringify(load(), null, 1), 'utf8');
    fs.renameSync(tmp, file);
  };
  const view = (f: LearnFeedback, voterId: string): LearnFeedbackView => {
    const { votes, ...rest } = f;
    const vals = Object.values(votes || {});
    return { ...rest, up: vals.filter((v) => v === 1).length, down: vals.filter((v) => v === -1).length, myVote: (votes || {})[voterId] || 0, mine: f.author.id === voterId };
  };

  return {
    list(deckId: string, voterId = ''): LearnFeedbackView[] {
      return load()
        .filter((f) => f.deckId === deckId && f.status !== 'resolved')
        .map((f) => view(f, voterId));
    },

    create(body: any): { ok: true; item: LearnFeedbackView } | { ok: false; error: string } {
      const deckId = clip(body?.deckId, 160);
      const targetKey = clip(body?.targetKey, 160);
      const authorId = clip(body?.author?.id, 120);
      if (!ID_RE.test(deckId) || !ID_RE.test(targetKey) || !authorId) return { ok: false, error: 'Geçersiz hedef.' };
      const field = clip(body?.field, 600);
      const reason = clip(body?.reason, 1500);
      if (field.length < 3 || reason.length < 5) return { ok: false, error: 'Hangi bilginin neden yanlış olduğunu yazın.' };
      // Aynı kişi aynı öğeye arka arkaya aynı metni gönderirse ikinci kayıt açılmaz
      const dup = load().find((f) => f.targetKey === targetKey && f.deckId === deckId && f.author.id === authorId && f.field === field && f.status === 'open');
      if (dup) return { ok: true, item: view(dup, authorId) };
      const item: LearnFeedback = {
        id: `lf-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`,
        deckId,
        slideNumber: Number(body?.slideNumber) || 0,
        targetKey,
        targetLabel: clip(body?.targetLabel, 120) || 'Ders öğesi',
        location: clip(body?.location, 200) || clip(body?.targetLabel, 120) || 'Ders öğesi',
        deckTitle: clip(body?.deckTitle, 160) || deckId,
        link: learnFeedbackLink(deckId, Number(body?.slideNumber) || 0, targetKey),
        field,
        reason,
        author: { id: authorId, name: clip(body?.author?.name, 80) || 'Anonim öğrenci' },
        createdAt: new Date().toISOString(),
        status: 'open',
        votes: {},
      };
      load().push(item);
      save();
      return { ok: true, item: view(item, authorId) };
    },

    vote(id: string, voterId: string, vote: number): { ok: true; item: LearnFeedbackView } | { ok: false; error: string; status: number } {
      const f = load().find((x) => x.id === id);
      if (!f) return { ok: false, error: 'Bildirim bulunamadı.', status: 404 };
      const vid = clip(voterId, 120);
      if (!vid) return { ok: false, error: 'Oy veren belirsiz.', status: 400 };
      if (f.author.id === vid) return { ok: false, error: 'Kendi bildirimine oy veremezsin.', status: 400 };
      f.votes = f.votes || {};
      if (vote === 1 || vote === -1) f.votes[vid] = vote;
      else delete f.votes[vid];
      save();
      return { ok: true, item: view(f, vid) };
    },

    resolve(id: string): boolean {
      const f = load().find((x) => x.id === id);
      if (!f) return false;
      f.status = 'resolved';
      save();
      return true;
    },
  };
}
