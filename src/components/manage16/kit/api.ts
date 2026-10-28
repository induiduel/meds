/**
 * Yönetim v16 — veri katmanı. Ön eksiz fetch('/api/...') kullanılır: yerel panel → Oracle vekili ve yönetici jetonu
 * (config/deployment.ts + adminFetchAuth.ts) bu yolda otomatik eklenir. safeJsonFetch KULLANMAYIN (vekil başlığını atlar).
 */
import { useCallback, useEffect, useRef, useState } from 'react';
import { realtimeEventService } from '../../../services/realtimeEvents';

export class AdminHata extends Error {
  durum: number;
  constructor(mesaj: string, durum: number) { super(mesaj); this.durum = durum; }
}

export type IstekSecenek = { yontem?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'; govde?: unknown; sorgu?: Record<string, unknown>; sinyal?: AbortSignal };

export function sorguDizesi(s?: Record<string, unknown>): string {
  if (!s) return '';
  const p = new URLSearchParams();
  for (const [k, v] of Object.entries(s)) if (v !== undefined && v !== null && v !== '') p.set(k, String(v));
  const t = p.toString();
  return t ? `?${t}` : '';
}

/** JSON isteği; 2xx dışında AdminHata fırlatır (sunucunun {error} metniyle) */
export async function adminIstek<T = any>(yol: string, o: IstekSecenek = {}): Promise<T> {
  const r = await fetch(`${yol}${sorguDizesi(o.sorgu)}`, {
    method: o.yontem || 'GET',
    headers: o.govde !== undefined ? { 'Content-Type': 'application/json' } : undefined,
    body: o.govde !== undefined ? JSON.stringify(o.govde) : undefined,
    signal: o.sinyal,
    cache: 'no-store',
  });
  const metin = await r.text();
  let veri: any = null;
  try { veri = metin ? JSON.parse(metin) : null; } catch { veri = null; }
  if (!r.ok) throw new AdminHata(veri?.error || veri?.message || `${r.status} ${r.statusText}`, r.status);
  // Uç hedef sunucuda yoksa SPA geri dönüşü HTML gelir (ör. Oracle henüz bu sürümde değil)
  if (metin && veri === null && /^\s*</.test(metin)) throw new AdminHata(`Uç bulunamadı: ${yol} (hedef sunucu bu sürümü henüz taşımıyor olabilir)`, 404);
  return veri as T;
}

const onbellek = new Map<string, { at: number; veri: unknown }>();

/**
 * Basit SWR: önbellekteki veri hemen döner, arkadan tazelenir.
 * canliOlay: bu SSE olaylarından biri gelince (ve resync'te) yeniden çeker.
 * yol null ise istek atılmaz.
 */
export function useAdminSorgu<T = any>(yol: string | null, o: { sorgu?: Record<string, unknown>; canliOlay?: string[]; aralikMs?: number } = {}) {
  const anahtar = yol ? `${yol}${sorguDizesi(o.sorgu)}` : '';
  const [veri, setVeri] = useState<T | undefined>(() => (anahtar ? (onbellek.get(anahtar)?.veri as T) : undefined));
  const [yukleniyor, setYukleniyor] = useState(Boolean(anahtar));
  const [hata, setHata] = useState<AdminHata | Error | null>(null);
  const istekNo = useRef(0);

  const yenile = useCallback(async () => {
    if (!anahtar) return;
    const no = ++istekNo.current;
    setYukleniyor(true);
    try {
      const v = await adminIstek<T>(anahtar);
      if (no !== istekNo.current) return;
      onbellek.set(anahtar, { at: Date.now(), veri: v });
      setVeri(v);
      setHata(null);
    } catch (e: any) {
      if (no === istekNo.current) setHata(e);
    } finally {
      if (no === istekNo.current) setYukleniyor(false);
    }
  }, [anahtar]);

  useEffect(() => {
    setVeri(anahtar ? (onbellek.get(anahtar)?.veri as T) : undefined);
    void yenile();
  }, [anahtar, yenile]);

  const olaylar = (o.canliOlay || []).join(',');
  useEffect(() => {
    if (!olaylar) return;
    let t: ReturnType<typeof setTimeout> | null = null;
    const tetik = () => { if (t) return; t = setTimeout(() => { t = null; void yenile(); }, 400); };
    const offs = [...olaylar.split(','), 'resync'].map((ev) => realtimeEventService.on(ev, tetik));
    return () => { offs.forEach((f) => f()); if (t) clearTimeout(t); };
  }, [olaylar, yenile]);

  useEffect(() => {
    if (!o.aralikMs) return;
    const t = setInterval(() => { if (document.visibilityState === 'visible') void yenile(); }, o.aralikMs);
    return () => clearInterval(t);
  }, [o.aralikMs, yenile]);

  return { veri, yukleniyor, hata, yenile, setVeri };
}

/** Sunucu liste yanıtı (src/services/yonetim16/sayfalama.ts) */
export type ListeYaniti<T> = { ogeler: T[]; toplam: number; sayfa: number; boyut: number; yuzler?: Record<string, { deger: string; n: number }[]> };
