/**
 * Öğren geri bildirimleri (istemci): hata bildir, listele, beğen/reddet.
 * Sunucuya ulaşılamazsa (ör. tünel kapalı) bildirim bu cihazda saklanır ve öyle işaretlenir.
 */
import { safeJsonFetch } from '../../../services/api';
import { auth, getLocalAdminSession, getRememberedStudentInfo } from '../../../services/auth';

export interface FeedbackItem {
  id: string;
  deckId: string;
  slideNumber: number;
  targetKey: string;
  targetLabel: string;
  /** Öğenin ekrandaki yeri, ör. "Pekiştir › Gizli tablo" */
  location?: string;
  /** Yöneticinin öğeye gittiği bağlantı */
  link?: string;
  field: string;
  reason: string;
  author: { id: string; name: string };
  createdAt: string;
  up: number;
  down: number;
  myVote: 0 | 1 | -1;
  mine: boolean;
  local?: boolean;
}

export interface FeedbackTarget { key: string; label: string; slideNumber: number; hint?: string; location?: string }

const VOTER_KEY = 'medsoru_learn_voter_id';
const LOCAL_KEY = 'medsoru_learn_feedback_local_v1';

export const whoAmI = (): { id: string; name: string } => {
  const fb = auth.currentUser;
  if (fb?.uid) return { id: fb.uid, name: fb.displayName || (fb.email ? fb.email.split('@')[0] : 'Öğrenci') };
  const admin = getLocalAdminSession();
  if (admin?.uid) return { id: admin.uid, name: admin.displayName || 'Yönetici' };
  let id = '';
  try {
    id = localStorage.getItem(VOTER_KEY) || '';
    if (!id) {
      id = `anon-${Math.random().toString(36).slice(2, 10)}`;
      localStorage.setItem(VOTER_KEY, id);
    }
  } catch {
    id = 'anon-gecici';
  }
  const remembered = getRememberedStudentInfo().name;
  return { id, name: remembered || 'Anonim öğrenci' };
};

const readLocal = (): FeedbackItem[] => {
  try {
    return JSON.parse(localStorage.getItem(LOCAL_KEY) || '[]');
  } catch {
    return [];
  }
};
const writeLocal = (list: FeedbackItem[]) => {
  try {
    localStorage.setItem(LOCAL_KEY, JSON.stringify(list.slice(-300)));
  } catch {
    /* ignore */
  }
};

export async function listFeedback(deckId: string): Promise<FeedbackItem[]> {
  const me = whoAmI();
  const res = await safeJsonFetch<{ items: FeedbackItem[] }>(`/api/learn/feedback?deckId=${encodeURIComponent(deckId)}&voterId=${encodeURIComponent(me.id)}`);
  const local = readLocal().filter((f) => f.deckId === deckId);
  return [...(res.ok && Array.isArray(res.data?.items) ? res.data!.items : []), ...local];
}

export async function sendFeedback(deckId: string, target: FeedbackTarget, field: string, reason: string, deckTitle = ''): Promise<FeedbackItem> {
  const author = whoAmI();
  const location = target.location || target.label;
  const body = { deckId, deckTitle, slideNumber: target.slideNumber, targetKey: target.key, targetLabel: target.label, location, field, reason, author };
  const res = await safeJsonFetch<{ item: FeedbackItem; error?: string }>('/api/learn/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (res.ok && res.data?.item) return res.data.item;
  if (res.status === 400) throw new Error((res.data as any)?.error || res.error || 'Bildirim gönderilemedi.');
  const item: FeedbackItem = { ...body, id: `local-${Date.now().toString(36)}`, createdAt: new Date().toISOString(), up: 0, down: 0, myVote: 0, mine: true, local: true };
  writeLocal([...readLocal(), item]);
  return item;
}

export async function voteFeedback(item: FeedbackItem, vote: 0 | 1 | -1): Promise<FeedbackItem> {
  if (item.local) throw new Error('Bu bildirim yalnızca bu cihazda; sunucuya ulaşınca oylanabilir.');
  const res = await safeJsonFetch<{ item: FeedbackItem; error?: string }>(`/api/learn/feedback/${encodeURIComponent(item.id)}/vote`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ voterId: whoAmI().id, vote }),
  });
  if (res.ok && res.data?.item) return res.data.item;
  throw new Error((res.data as any)?.error || res.error || 'Oy kaydedilemedi.');
}
