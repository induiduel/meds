/**
 * Ansiklopedi verisinin TEK yükleyicisi (Sözlük ekranı + glossary.ts takma ad zenginleştirmesi).
 * Paketteki kopya ayrı parça olarak dinamik iner; panel / NotebookLM ile değiştirilmişse (içerik katmanı,
 * `encyclopedia` türü) sunucudaki güncel kopya çekilir. Değişince önbellek düşer, dinleyenler haber alır (H582).
 */
import { safeJsonFetch } from '../services/api';
import { contentReady, isContentChanged, onContentChanged } from '../services/contentLive';

let veri: Promise<any[]> | null = null;
const dinleyenler = new Set<() => void>();

async function getir(): Promise<any[]> {
  await contentReady(1500);
  if (isContentChanged('encyclopedia')) {
    const r = await safeJsonFetch<unknown>('/api/content/encyclopedia', { cache: 'no-store' });
    if (r.ok && Array.isArray(r.data)) return r.data as any[];
  }
  const m = await import('./medical_encyclopedia.json');
  return ((m as { default?: unknown }).default ?? m) as any[];
}

export function ansiklopediYukle(): Promise<any[]> {
  if (!veri) veri = getir().catch((err) => { veri = null; throw err; });
  return veri;
}

/** Sunucudaki ansiklopedi değişince çağrılır (önbellek zaten düşürülmüştür) */
export function ansiklopediDegisince(fn: () => void): () => void {
  dinleyenler.add(fn);
  return () => { dinleyenler.delete(fn); };
}

if (typeof window !== 'undefined') setTimeout(() => {
  onContentChanged('encyclopedia', () => { veri = null; dinleyenler.forEach((fn) => { try { fn(); } catch { /* dinleyici */ } }); });
}, 0);
