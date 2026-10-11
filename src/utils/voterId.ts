/**
 * Oy veren kimliği: giriş yapmış kullanıcıda uid/e-posta, değilse cihaza özgü kalıcı bir
 * kimlik. Eskiden anonim herkes "local_user"/"anonim-std" ile oy verdiği için tek kişi gibi
 * sayılıyordu; sunucu artık bu ortak kimlikleri reddeder.
 */
const KEY = 'medsoru_device_token';

function newToken(): string {
  try {
    if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) return `dev-${crypto.randomUUID()}`;
  } catch { /* yoksay */ }
  return `dev-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

export function getDeviceToken(): string {
  try {
    const existing = localStorage.getItem(KEY);
    if (existing) return existing;
    const token = newToken();
    localStorage.setItem(KEY, token);
    return token;
  } catch {
    return newToken();
  }
}

export function getVoterId(user?: { uid?: string | null; email?: string | null } | null): string {
  return user?.uid || user?.email || getDeviceToken();
}

interface VoteTarget { upvotes?: number; likedBy?: string[] }

/** Sunucudaki toggleVote ile aynı hesap; iyimser arayüz güncellemesi için. */
export function toggledVote<T extends VoteTarget>(target: T, voterId: string): T & { upvotes: number; likedBy: string[] } {
  const voters = Array.from(new Set((target.likedBy || []).filter(Boolean)));
  const count = typeof target.upvotes === 'number' ? target.upvotes : 0;
  const base = voters.length === 0 && count <= 1 ? 0 : Math.max(0, count - voters.length);
  const has = voters.includes(voterId);
  const likedBy = has ? voters.filter((v) => v !== voterId) : [...voters, voterId];
  return { ...target, likedBy, upvotes: base + likedBy.length };
}
