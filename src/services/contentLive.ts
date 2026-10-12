/**
 * Canlı içerik: pakete gömülü veri (sözlük, hastalıklar, Öğren desteleri, örnek sorular) yönetim panelinden
 * değiştirilince ziyaretçiye yeniden derleme beklemeden ulaşsın.
 *
 * Sunucu /api/content/manifest ile paketten yeni olanları bildirir (bkz. src/services/contentOverlay.ts);
 * panel değişikliği SSE `content_changed` olarak gelir. Yükleyiciler `isContentChanged` ile paketteki kopya
 * yerine sunucudakini çeker, ekranlar `onContentChanged` ile tazelenir.
 */
import { realtimeEventService } from './realtimeEvents';
import { safeJsonFetch } from './api';

type Manifest = Record<string, { at: number; ids?: string[] }>;

let manifest: Manifest = {};
let started = false;
let readyPromise: Promise<void> | null = null;
const listeners = new Map<string, Set<(ids: string[]) => void>>();

async function refresh(): Promise<void> {
  const r = await safeJsonFetch<{ entities: Manifest }>('/api/content/manifest', { cache: 'no-store' });
  if (r.ok && r.data?.entities && typeof r.data.entities === 'object') manifest = r.data.entities;
}

function emit(entity: string, ids: string[]) {
  listeners.get(entity)?.forEach((fn) => {
    try { fn(ids); } catch (err) { console.warn('[contentLive] dinleyici hatası:', err); }
  });
}

export function startContentLive() {
  if (started || typeof window === 'undefined') return;
  started = true;
  readyPromise = refresh().catch(() => {});
  realtimeEventService.on('content_changed', async (d: any) => {
    const entity = String(d?.entity || '');
    if (!entity || entity === 'music') return; // müzik kendi çalarında dinleniyor
    await refresh().catch(() => {});
    emit(entity, Array.isArray(d?.ids) ? d.ids.map(String) : []);
  });
  // Bağlantı koptuğu sırada kaçan değişiklik: bildirimi yenile, değişmiş türleri duyur
  let first = true;
  realtimeEventService.onStatusChange((st) => {
    if (st !== 'connected') return;
    if (first) { first = false; return; }
    const before = JSON.stringify(manifest);
    void refresh().then(() => {
      if (JSON.stringify(manifest) === before) return;
      for (const [entity, m] of Object.entries(manifest)) emit(entity, m.ids || []);
    });
  });
}

/** Bildirim gelene dek en çok `ms` bekler (ilk açılışta paketteki eski kopya gösterilmesin) */
export function contentReady(ms = 1500): Promise<void> {
  if (!readyPromise) startContentLive();
  return Promise.race([readyPromise || Promise.resolve(), new Promise<void>((r) => setTimeout(r, ms))]);
}

/** Tür (ya da türdeki tek kayıt: deste kimliği, "k1/k1-01" ders dosyası) paketten yeni mi */
export function isContentChanged(entity: string, id?: string): boolean {
  const m = manifest[entity];
  if (!m) return false;
  if (id === undefined || !m.ids) return true;
  return m.ids.includes(id);
}

export function changedIds(entity: string): string[] {
  return manifest[entity]?.ids || [];
}

export function onContentChanged(entity: string, fn: (ids: string[]) => void): () => void {
  if (!listeners.has(entity)) listeners.set(entity, new Set());
  listeners.get(entity)!.add(fn);
  return () => { listeners.get(entity)?.delete(fn); };
}
