/**
 * Not eşitleme (istemci). Notlar tarayıcıda (studyStore, medsoru_notes_v1) yaşar; her değişiklikten ~4 sn
 * sonra ve açılışta sunucu yedeğiyle (PUT /api/notes) birleştirilir. Kimlik = eşitleme kodu: varsayılan
 * cihaz belirteci; kullanıcı kodu başka cihaza girerek aynı not defterini paylaşır.
 * Çevrimdışıyken sessizce bekler; bağlantı gelince tekrar dener. Ekranlar 'medsoru:notes-synced' olayını dinler.
 */
import { getNotes, onNotesChanged, replaceNotesFromSync, StudyNote } from './studyStore';
import { getDeviceToken } from '../utils/voterId';
import { getCustomApiUrl } from './api';
import { getNetState, onNetChange } from './net';

const CODE_KEY = 'medsoru_notes_sync_code';
const DEL_KEY = 'medsoru_notes_deleted_v1';
const LAST_KEY = 'medsoru_notes_synced_at';

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
  try { localStorage.setItem(CODE_KEY, c); } catch { /* yok */ }
  void syncNotes();
};
export const lastSyncedAt = () => { try { return localStorage.getItem(LAST_KEY) || ''; } catch { return ''; } };

let timer: number | undefined;
let running: Promise<boolean> | null = null;

export function syncNotes(): Promise<boolean> {
  if (running) return running;
  running = (async () => {
    if (getNetState() === 'offline') return false;
    const base = (getCustomApiUrl() || '').replace(/\/$/, '');
    const deleted = readJson<Record<string, string>>(DEL_KEY, {});
    try {
      const res = await fetch(`${base}/api/notes`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'x-user-id': getSyncCode() },
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
      try { localStorage.setItem(LAST_KEY, new Date().toISOString()); } catch { /* yok */ }
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
export async function pullDeltaNotes(): Promise<boolean> {
  if (getNetState() === 'offline') return false;
  const since = lastSyncedAt();
  if (!since) return syncNotes(); // İlk kez ise tam senkronizasyon yap

  const base = (getCustomApiUrl() || '').replace(/\/$/, '');
  try {
    const res = await fetch(`${base}/api/notes?since=${encodeURIComponent(since)}`, {
      method: 'GET',
      headers: { 'x-user-id': getSyncCode() },
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
