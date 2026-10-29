/**
 * Not eşitleme (istemci). Notlar tarayıcıda (studyStore, medsoru_notes_v1) yaşar; her değişiklikten ~4 sn
 * sonra ve açılışta sunucu yedeğiyle (PUT /api/notes) birleştirilir. Kimlik:
 * - Oturum açık: Firebase ID jetonu → defter hesaba bağlıdır, her cihazda aynı defter gelir. İlk girişte
 *   cihazdaki notlar hesabın defterine birleştirilir (kaybolmaz).
 * - Girişsiz: eşitleme kodu (varsayılan cihaz belirteci; kullanıcı kodu başka cihaza girerek defteri paylaşır).
 * Çevrimdışıyken sessizce bekler; bağlantı gelince tekrar dener. Ekranlar 'medsoru:notes-synced' olayını dinler.
 */
import { getNotes, onNotesChanged, replaceNotesFromSync, StudyNote } from './studyStore';
import { getDeviceToken } from '../utils/voterId';
import { getCustomApiUrl } from './api';
import { getNetState, onNetChange } from './net';
import { auth } from './auth';

const CODE_KEY = 'medsoru_notes_sync_code';
const DEL_KEY = 'medsoru_notes_deleted_v1';
const LAST_KEY = 'medsoru_notes_synced_at';
// Son eşitlemenin hangi deftere (hesap/kod) yapıldığı: değişince delta yerine tam eşitleme gerekir
const IDENT_KEY = 'medsoru_notes_synced_identity';

const readJson = <T,>(k: string, f: T): T => {
  try { const r = localStorage.getItem(k); return r ? (JSON.parse(r) as T) : f; } catch { return f; }
};
const writeJson = (k: string, v: unknown) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* yok */ } };

export const getSyncCode = () => {
  try { return localStorage.getItem(CODE_KEY) || getDeviceToken(); } catch { return getDeviceToken(); }
};
/** Başka cihazın kodunu gir: bu cihazdaki notlar o defterle birleşir. */
export const setSyncCode = (code: string) => {
  const c = code.trim();
  if (c.length < 12) throw new Error('Kod en az 12 karakter olmalı');
  if (c.toLowerCase().startsWith('acct:')) throw new Error('Bu kod biçimi kullanılamaz');
  try { localStorage.setItem(CODE_KEY, c); } catch { /* yok */ }
  void syncNotes();
};
export const lastSyncedAt = () => { try { return localStorage.getItem(LAST_KEY) || ''; } catch { return ''; } };

/** İstek başlıkları ve defter kimliği: oturum açıksa hesap, değilse eşitleme kodu. */
async function notesIdentity(): Promise<{ headers: Record<string, string>; ident: string }> {
  const code = getSyncCode();
  const user = auth.currentUser;
  if (user) {
    try {
      const token = await user.getIdToken();
      return { headers: { Authorization: `Bearer ${token}`, 'x-user-id': code }, ident: `acct:${user.uid}` };
    } catch {
      /* jeton alınamadı: cihaz koduyla devam */
    }
  }
  return { headers: { 'x-user-id': code }, ident: code };
}

/** Sunucunun SSE 'notes_changed' olayındaki defter özeti (sha256(kimlik) ilk 16 hane) bu cihazın defteri mi? */
export async function isOwnNotebook(codeHash: string | undefined): Promise<boolean> {
  if (!codeHash) return true;
  try {
    const { ident } = await notesIdentity();
    const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(ident));
    const hex = Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, '0')).join('');
    return hex.slice(0, 16) === codeHash;
  } catch {
    return true; // karşılaştırılamıyorsa güvenli taraf: çek
  }
}

let timer: number | undefined;
let running: Promise<boolean> | null = null;

export function syncNotes(): Promise<boolean> {
  if (running) return running;
  running = (async () => {
    if (getNetState() === 'offline') return false;
    const base = (getCustomApiUrl() || '').replace(/\/$/, '');
    const deleted = readJson<Record<string, string>>(DEL_KEY, {});
    try {
      const who = await notesIdentity();
      const res = await fetch(`${base}/api/notes`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', ...who.headers },
        body: JSON.stringify({ notes: getNotes(), deleted }),
      });
      if (!res.ok) return false;
      const merged = (await res.json()) as { notes: StudyNote[]; deleted: Record<string, string> };
      // Eşitleme sürerken kullanıcı not yazdıysa onu ezme: yereldeki daha yeni sürüm kazanır
      const local = new Map(getNotes().map((n) => [n.id, n]));
      const out = merged.notes.map((n) => {
        const l = local.get(n.id);
        return l && l.updatedAt > n.updatedAt ? l : n;
      });
      for (const [id, n] of local) if (!out.some((o) => o.id === id) && !(merged.deleted || {})[id]) out.unshift(n);
      replaceNotesFromSync(out);
      writeJson(DEL_KEY, merged.deleted || {});
      try {
        localStorage.setItem(LAST_KEY, new Date().toISOString());
        localStorage.setItem(IDENT_KEY, who.ident);
      } catch { /* yok */ }
      window.dispatchEvent(new CustomEvent('medsoru:notes-synced'));
      return true;
    } catch {
      return false;
    } finally {
      running = null;
    }
  })();
  return running;
}

/**
 * Delta / Incremental Sync: Sunucudan yalnızca son senkronizasyondan sonraki değişiklikleri çeker.
 * Megabaytlarca veriyi boş yere tekrar indirmeyi engeller.
 */
/** Son fark çekiminin zamanı: açılışta ağ durumu olayı + açılış zamanlayıcısı + SSE telafisi birkaç saniye içinde
 *  aynı çekimi yineliyordu (açılışta iki-dört /api/notes). Aynı defter için 8 sn içinde ikinci çekim yapılmaz. */
let sonFarkCekim = { ident: '', zaman: 0 };
export async function pullDeltaNotes(): Promise<boolean> {
  if (getNetState() === 'offline') return false;
  const since = lastSyncedAt();
  const who = await notesIdentity();
  let lastIdent = '';
  try { lastIdent = localStorage.getItem(IDENT_KEY) || ''; } catch { /* yok */ }
  // İlk kez ya da defter değiştiyse (giriş/çıkış, kod girme) tam eşitleme: cihazdaki notlar yeni deftere birleşir
  if (!since || lastIdent !== who.ident) return syncNotes();
  if (sonFarkCekim.ident === who.ident && Date.now() - sonFarkCekim.zaman < 8000) return false;
  sonFarkCekim = { ident: who.ident, zaman: Date.now() };

  const base = (getCustomApiUrl() || '').replace(/\/$/, '');
  try {
    const res = await fetch(`${base}/api/notes?since=${encodeURIComponent(since)}`, {
      method: 'GET',
      headers: who.headers,
    });
    if (!res.ok) return false;
    const data = await res.json();
    if (data.upToDate) {
      // Veri tamamen güncel, ağ tasarrufu sağlandı
      return true;
    }

    const localNotes = getNotes();
    const localMap = new Map(localNotes.map((n) => [n.id, n]));
    const incomingDelta: StudyNote[] = Array.isArray(data.notes) ? data.notes : [];
    const incomingDeleted: Record<string, string> = data.deleted || {};

    let hasChange = false;

    // Silinenleri yerelden kaldır
    for (const [delId, delAt] of Object.entries(incomingDeleted)) {
      const existing = localMap.get(delId);
      if (existing && existing.updatedAt <= delAt) {
        localMap.delete(delId);
        hasChange = true;
      }
    }

    // Güncellenenleri veya yeni eklenenleri birleştir
    for (const inNote of incomingDelta) {
      const existing = localMap.get(inNote.id);
      if (!existing || existing.updatedAt < inNote.updatedAt) {
        localMap.set(inNote.id, inNote);
        hasChange = true;
      }
    }

    if (hasChange) {
      const updatedList = Array.from(localMap.values()).sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
      replaceNotesFromSync(updatedList);
      window.dispatchEvent(new CustomEvent('medsoru:notes-synced'));
    }

    if (data.updatedAt) {
      try { localStorage.setItem(LAST_KEY, data.updatedAt); } catch { /* yok */ }
    }
    return true;
  } catch {
    return false;
  }
}


const schedule = (ms = 4000) => {
  window.clearTimeout(timer);
  timer = window.setTimeout(() => void syncNotes(), ms);
};

let installed = false;
export function installNotesSync() {
  if (installed || typeof window === 'undefined') return;
  installed = true;
  onNotesChanged((removed) => {
    if (removed.length) {
      const del = readJson<Record<string, string>>(DEL_KEY, {});
      const now = new Date().toISOString();
      for (const id of removed) del[id] = now;
      writeJson(DEL_KEY, del);
    }
    schedule();
  });
  onNetChange(() => {
    if (getNetState() === 'online') {
      window.setTimeout(() => void pullDeltaNotes(), 1500);
    }
  });
  // Açılışta bir kez delta kontrolü (ilk boyamayı geciktirmesin)
  window.setTimeout(() => void pullDeltaNotes(), 5000);
}
