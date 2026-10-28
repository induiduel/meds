/**
 * Çalışma anı site ayarı — istemci (Yönetim v16, 2026-10-28).
 *
 * Varsayılan: derleme sabitleri (merkezModel.GIZLI_SAYFALAR / KAPALI_SAYFALAR). Panel ayarı (GET /api/site-ayar) üstüne yazar.
 * İlk boyamadan önce localStorage'daki son ayar SENKRON okunur (gizli sayfa bir an görünmesin); sonra ağdan tazelenir ve
 * SSE `site_ayar_changed` ile canlı güncellenir. Ayar SW önbelleğine alınmaz (public/sw.js baypas listesi).
 */
import { useSyncExternalStore } from 'react';
import { GIZLI_SAYFALAR, KAPALI_SAYFALAR } from '../components/merkez/merkezModel';

export type SayfaDurumu = 'acik' | 'gizli' | 'kapali';
export type GenelSiteAyar = {
  surum: number;
  guncellendi: string;
  sayfalar: Record<string, SayfaDurumu>;
  bayraklar: Record<string, boolean>;
  gorunurluk: Record<string, 'acik' | 'gizli' | 'yalniz-yonetici'>;
  duyuru: { acik: boolean; metin: string; ton: 'bilgi' | 'uyari' | 'hata'; baglanti?: string; bitis?: string } | null;
  bakim: { acik: boolean; sure?: string };
};

const KEY = 'medsoru_site_ayar_v1';
const BOS: GenelSiteAyar = { surum: 0, guncellendi: '', sayfalar: {}, bayraklar: {}, gorunurluk: {}, duyuru: null, bakim: { acik: false } };

function ilkOku(): GenelSiteAyar {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) return { ...BOS, ...JSON.parse(raw) };
  } catch { /* gizli pencere */ }
  return BOS;
}

let ayar: GenelSiteAyar = ilkOku();
const dinleyiciler = new Set<() => void>();

function uygula(a: Partial<GenelSiteAyar> | null | undefined) {
  if (!a || typeof a !== 'object') return;
  const yeni = { ...BOS, ...a } as GenelSiteAyar;
  ayar = yeni;
  try { localStorage.setItem(KEY, JSON.stringify(ayar)); } catch { /* */ }
  dinleyiciler.forEach((f) => f());
}

export function getSiteAyar(): GenelSiteAyar { return ayar; }

/** Menüden ve adresten gizli mi (öğrenci için). Panel 'acik' derse sabit gizli sayfa da açılır. */
export function sayfaGizli(route: string): boolean {
  const d = ayar.sayfalar[route];
  if (d === 'gizli') return true;
  if (d === 'acik' || d === 'kapali') return false;
  return GIZLI_SAYFALAR.has(route as never);
}

/** Öğrenciye kapalı mı (sayfa "kapalı" ekranı gösterir; KAPALI_SAYFALAR anlamı) */
export function sayfaKapali(route: string): boolean {
  const d = ayar.sayfalar[route];
  if (d === 'kapali') return true;
  if (d === 'acik' || d === 'gizli') return false;
  return KAPALI_SAYFALAR.has(route as never);
}

export function bayrak(ad: string, varsayilan = false): boolean {
  const v = ayar.bayraklar[ad];
  return typeof v === 'boolean' ? v : varsayilan;
}

/** '<tür>:<kimlik>' görünürlüğü; yoksa 'acik' */
export function gorunurluk(anahtar: string): 'acik' | 'gizli' | 'yalniz-yonetici' {
  return ayar.gorunurluk[anahtar] || 'acik';
}

function abone(f: () => void) { dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; }

/** Bileşen ayar değişince yeniden çizilir */
export function useSiteAyar(): GenelSiteAyar {
  return useSyncExternalStore(abone, getSiteAyar, getSiteAyar);
}

export async function siteAyarTazele(): Promise<void> {
  try {
    const { safeJsonFetch } = await import('./api');
    const r = await safeJsonFetch<GenelSiteAyar>('/api/site-ayar', { cache: 'no-cache' });
    if (r.ok && r.data) uygula(r.data);
  } catch { /* çevrimdışı: önbellek/varsayılan */ }
}

// Modül düzeyinde kayıt setTimeout(0) içinde (içe aktarma döngüsü açılışı kilitlemesin; contentLive tuzağı)
if (typeof window !== 'undefined') {
  setTimeout(() => {
    void siteAyarTazele();
    import('./realtimeEvents').then(({ realtimeEventService }) => {
      realtimeEventService.on('site_ayar_changed', (p: any) => uygula(p));
      realtimeEventService.on('resync', () => void siteAyarTazele());
    }).catch(() => {});
  }, 0);
}
