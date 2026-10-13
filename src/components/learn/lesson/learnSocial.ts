/**
 * Öğren ortak katmanı (istemci): herkese açık SPOT / ÖNEMLİ / VURGU notları ve metin bildirimi tartışmaları.
 * Sunucu: src/services/learnSocialRoutes.ts (meds-pg); canlı güncelleme SSE `learn_social` olayıyla gelir.
 * Kimlik `whoAmI()` (öğren geri bildirimiyle aynı): Firebase uid, yönetici oturumu ya da cihaz kimliği.
 */
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { safeJsonFetch } from '../../../services/api';
import { realtimeEventService } from '../../../services/realtimeEvents';
import { whoAmI } from './lessonFeedback';

export type NoteKind = 'spot' | 'onemli' | 'vurgu';
export const NOTE_KINDS: { id: NoteKind; label: string; hint: string }[] = [
  { id: 'spot', label: 'SPOT', hint: 'Sınavda çıkabilecek bilgi' },
  { id: 'onemli', label: 'ÖNEMLİ', hint: 'Atlanmaması gereken nokta' },
  { id: 'vurgu', label: 'VURGU', hint: 'Hocanın vurguladığı / akılda tutulacak' },
];
export const NOTE_MAX = 600;
export const MESSAGE_MAX = 1000;
export const QUOTE_MAX = 400;

export interface SocialAuthor { id: string; name: string }
export interface SocialNote {
  id: string;
  deckId: string;
  stepNumber: number;
  kind: NoteKind;
  body: string;
  anchor: string;
  author: SocialAuthor;
  createdAt: string;
  mine?: boolean;
  canDelete?: boolean;
}
export interface SocialThread {
  id: string;
  deckId: string;
  stepNumber: number;
  quote: string;
  prefix: string;
  suffix: string;
  status: 'open' | 'resolved';
  reporter: SocialAuthor;
  messageCount: number;
  createdAt: string;
  lastMessageAt: string;
  mine?: boolean;
  canResolve?: boolean;
}
export interface SocialMessage {
  id: string;
  threadId: string;
  body: string;
  author: SocialAuthor;
  isAdmin: boolean;
  createdAt: string;
  mine?: boolean;
  canDelete?: boolean;
}

const errOf = (r: { data?: any; error?: string }, d: string) => (r.data as any)?.error || r.error || d;
const json = (method: string, body?: unknown): RequestInit => ({
  method,
  headers: { 'Content-Type': 'application/json' },
  body: body === undefined ? undefined : JSON.stringify(body),
});

export async function createNote(deckId: string, stepNumber: number, kind: NoteKind, body: string, anchor = ''): Promise<SocialNote> {
  const r = await safeJsonFetch<{ item: SocialNote }>('/api/learn/social/notes', json('POST', { deckId, stepNumber, kind, body, anchor, author: whoAmI() }));
  if (r.ok && r.data?.item) return r.data.item;
  throw new Error(errOf(r, 'Not kaydedilemedi.'));
}
export async function deleteNote(id: string): Promise<void> {
  const r = await safeJsonFetch(`/api/learn/social/notes/${encodeURIComponent(id)}?uid=${encodeURIComponent(whoAmI().id)}`, json('DELETE'));
  if (!r.ok) throw new Error(errOf(r, 'Not silinemedi.'));
}
export async function createThread(p: { deckId: string; deckTitle: string; stepNumber: number; quote: string; prefix: string; suffix: string; body: string }): Promise<{ item: SocialThread; created: boolean }> {
  const r = await safeJsonFetch<{ item: SocialThread; created: boolean }>('/api/learn/social/threads', json('POST', { ...p, author: whoAmI() }));
  if (r.ok && r.data?.item) return { item: r.data.item, created: !!r.data.created };
  throw new Error(errOf(r, 'Bildirim gönderilemedi.'));
}
export async function loadThread(id: string): Promise<{ item: SocialThread; messages: SocialMessage[] }> {
  const r = await safeJsonFetch<{ item: SocialThread; messages: SocialMessage[] }>(`/api/learn/social/threads/${encodeURIComponent(id)}?uid=${encodeURIComponent(whoAmI().id)}`);
  if (r.ok && r.data?.item) return { item: r.data.item, messages: r.data.messages || [] };
  throw new Error(errOf(r, 'Tartışma yüklenemedi.'));
}
export async function sendMessage(threadId: string, body: string): Promise<SocialMessage> {
  const r = await safeJsonFetch<{ message: SocialMessage }>(`/api/learn/social/threads/${encodeURIComponent(threadId)}/messages`, json('POST', { body, author: whoAmI() }));
  if (r.ok && r.data?.message) return r.data.message;
  throw new Error(errOf(r, 'Mesaj gönderilemedi.'));
}
export async function deleteMessage(id: string): Promise<void> {
  const r = await safeJsonFetch(`/api/learn/social/messages/${encodeURIComponent(id)}?uid=${encodeURIComponent(whoAmI().id)}`, json('DELETE'));
  if (!r.ok) throw new Error(errOf(r, 'Mesaj silinemedi.'));
}
export async function setThreadStatus(id: string, status: 'open' | 'resolved'): Promise<SocialThread> {
  const r = await safeJsonFetch<{ item: SocialThread }>(`/api/learn/social/threads/${encodeURIComponent(id)}/status`, json('POST', { status, uid: whoAmI().id }));
  if (r.ok && r.data?.item) return r.data.item;
  throw new Error(errOf(r, 'Durum değiştirilemedi.'));
}

/* ---------------------------------------------------------------------------
 * Canlı veri: dersin notları + tartışmaları; SSE olaylarıyla güncellenir
 * ------------------------------------------------------------------------- */
export interface SocialState {
  notes: SocialNote[];
  threads: SocialThread[];
  isAdmin: boolean;
  ready: boolean;
  /** Sunucuya ulaşılamadı (tablo yok / bağlantı yok) */
  offline: boolean;
}
type SocialEvent = { deckId: string; type: 'note' | 'thread' | 'message'; op: 'insert' | 'update' | 'delete'; id?: string; threadId?: string; item?: any };

/** Açık tartışma penceresi gibi bileşenler mesaj olaylarını buradan dinler */
const messageListeners = new Set<(e: SocialEvent) => void>();
export const onSocialMessage = (fn: (e: SocialEvent) => void) => {
  messageListeners.add(fn);
  return () => void messageListeners.delete(fn);
};

export function useLearnSocial(deckId: string) {
  const [state, setState] = useState<SocialState>({ notes: [], threads: [], isAdmin: false, ready: false, offline: false });
  const me = useRef(whoAmI().id);
  const adminRef = useRef(false);
  const own = useCallback(<T extends { author?: SocialAuthor; reporter?: SocialAuthor }>(x: T): T => {
    const who = (x.author || x.reporter)?.id;
    const mine = !!who && who === me.current;
    return { ...x, mine, canDelete: mine || adminRef.current, canResolve: mine || adminRef.current };
  }, []);

  const load = useCallback(async () => {
    const r = await safeJsonFetch<{ notes: SocialNote[]; threads: SocialThread[]; isAdmin: boolean }>(
      `/api/learn/social?deckId=${encodeURIComponent(deckId)}&uid=${encodeURIComponent(me.current)}`
    );
    if (r.ok && r.data) {
      adminRef.current = !!r.data.isAdmin;
      setState({ notes: r.data.notes || [], threads: r.data.threads || [], isAdmin: !!r.data.isAdmin, ready: true, offline: false });
    } else setState((s) => ({ ...s, ready: true, offline: true }));
  }, [deckId]);

  useEffect(() => {
    void load();
    const off = realtimeEventService.on('learn_social', (e: SocialEvent) => {
      if (!e || e.deckId !== deckId) return;
      if (e.type === 'message') {
        messageListeners.forEach((fn) => fn(e));
        return;
      }
      setState((s) => {
        if (e.type === 'note') {
          if (e.op === 'delete') return { ...s, notes: s.notes.filter((n) => n.id !== e.id) };
          const n = own(e.item as SocialNote);
          return { ...s, notes: s.notes.some((x) => x.id === n.id) ? s.notes.map((x) => (x.id === n.id ? n : x)) : [...s.notes, n] };
        }
        if (e.op === 'delete') return { ...s, threads: s.threads.filter((t) => t.id !== e.id) };
        const t = own(e.item as SocialThread);
        return { ...s, threads: s.threads.some((x) => x.id === t.id) ? s.threads.map((x) => (x.id === t.id ? t : x)) : [...s.threads, t] };
      });
    });
    // Bağlantı kopup geri gelince kaçan olaylar için yeniden yükle
    let wasDown = false;
    const offStatus = realtimeEventService.onStatusChange((st) => {
      if (st === 'disconnected') wasDown = true;
      else if (st === 'connected' && wasDown) {
        wasDown = false;
        void load();
      }
    });
    return () => {
      off();
      offStatus();
    };
  }, [deckId, load, own]);

  /** Kendi yazımını SSE'yi beklemeden yansıt (olay gelince aynı kimlikle birleşir) */
  const upsertNote = useCallback((n: SocialNote) => setState((s) => ({ ...s, notes: s.notes.some((x) => x.id === n.id) ? s.notes.map((x) => (x.id === n.id ? n : x)) : [...s.notes, n] })), []);
  const removeNote = useCallback((id: string) => setState((s) => ({ ...s, notes: s.notes.filter((x) => x.id !== id) })), []);
  const upsertThread = useCallback((t: SocialThread) => setState((s) => ({ ...s, threads: s.threads.some((x) => x.id === t.id) ? s.threads.map((x) => (x.id === t.id ? t : x)) : [...s.threads, t] })), []);
  return useMemo(() => ({ ...state, reload: load, upsertNote, removeNote, upsertThread }), [state, load, upsertNote, removeNote, upsertThread]);
}

/* ---------------------------------------------------------------------------
 * Metin bağlama: seçimden alıntı + önü/arkası; derste alıntının yerini bulma
 * ------------------------------------------------------------------------- */
const norm = (s: string) => s.replace(/\s+/g, ' ').trim();
const CTX = 60;

/** Seçimin, içinde bulunduğu ders metnine göre önü ve arkası (yeniden konumlandırma için) */
export function selectionContext(range: Range): { quote: string; prefix: string; suffix: string } {
  const quote = norm(range.toString()).slice(0, QUOTE_MAX);
  const start = range.startContainer.nodeType === 1 ? (range.startContainer as Element) : range.startContainer.parentElement;
  const root = start?.closest('.ls-content') || start?.closest('.ls-prose') || start?.parentElement;
  if (!root) return { quote, prefix: '', suffix: '' };
  try {
    const before = document.createRange();
    before.selectNodeContents(root);
    before.setEnd(range.startContainer, range.startOffset);
    const after = document.createRange();
    after.selectNodeContents(root);
    after.setStart(range.endContainer, range.endOffset);
    return { quote, prefix: norm(before.toString()).slice(-CTX), suffix: norm(after.toString()).slice(0, CTX) };
  } catch {
    return { quote, prefix: '', suffix: '' };
  }
}

/** Yalnız ham HTML adacıklarında (Prose/Inline, `data-ls-html`) aranır: React'in yönettiği düğümlere dokunulmaz. */
const ISLAND = '[data-ls-html]';
const SKIP = '.ls-sx-flag, script, style';

interface FlatText { flat: string; map: { node: Text; off: number }[] }
function flatten(root: Element): FlatText {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode: (n) => {
      const p = n.parentElement;
      if (!p || p.closest(SKIP) || !p.closest(ISLAND)) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    },
  });
  let flat = '';
  const map: FlatText['map'] = [];
  let prevSpace = true;
  for (let n = walker.nextNode() as Text | null; n; n = walker.nextNode() as Text | null) {
    const t = n.data;
    for (let i = 0; i < t.length; i++) {
      const sp = /\s/.test(t[i]);
      if (sp && prevSpace) continue;
      flat += sp ? ' ' : t[i];
      map.push({ node: n, off: i });
      prevSpace = sp;
    }
    // Adacıklar/bloklar arası sınır boşluk sayılır (seçim "…son kelime ilk kelime…" gibi gelir)
    if (!prevSpace) {
      flat += ' ';
      map.push({ node: n, off: t.length });
      prevSpace = true;
    }
  }
  return { flat, map };
}

const fold = (s: string) => s.toLocaleLowerCase('tr-TR');
/** Ortak sonek/önek uzunluğu: aynı alıntının birden çok geçtiği yerde doğru olanı seçmek için */
const tailMatch = (a: string, b: string) => {
  let k = 0;
  while (k < a.length && k < b.length && a[a.length - 1 - k] === b[b.length - 1 - k]) k++;
  return k;
};
const headMatch = (a: string, b: string) => {
  let k = 0;
  while (k < a.length && k < b.length && a[k] === b[k]) k++;
  return k;
};

/** Alıntıyı kökte bulur; birden çok geçiyorsa önü/arkası en çok tutanı seçer. Bulamazsa null. */
export function findQuoteRange(root: Element, quote: string, prefix = '', suffix = '', flatCache?: FlatText): Range | null {
  const q = fold(norm(quote));
  if (q.length < 3) return null;
  const { flat, map } = flatCache || flatten(root);
  const hay = fold(flat);
  let best = -1;
  let bestScore = -1;
  for (let i = hay.indexOf(q); i >= 0; i = hay.indexOf(q, i + 1)) {
    const score = tailMatch(hay.slice(Math.max(0, i - CTX), i).trimEnd(), fold(prefix)) + headMatch(hay.slice(i + q.length).trimStart(), fold(suffix));
    if (score > bestScore) {
      best = i;
      bestScore = score;
    }
  }
  if (best < 0) return null;
  const a = map[best];
  const b = map[Math.min(best + q.length - 1, map.length - 1)];
  if (!a || !b) return null;
  const r = document.createRange();
  r.setStart(a.node, a.off);
  r.setEnd(b.node, Math.min(b.off + 1, b.node.data.length));
  return r;
}
export const flattenForSearch = flatten;
