/**
 * Çalışma anı site ayarı — istemci (Yönetim v16, 2026-10-28).
 *
 * Varsayılan: derleme sabitleri (merkezModel.GIZLI_SAYFALAR / KAPALI_SAYFALAR). Panel ayarı (GET /api/site-ayar) üstüne yazar.
 * İlk boyamadan önce localStorage'daki son ayar SENKRON okunur (gizli sayfa bir an görünmesin); sonra ağdan tazelenir ve
 * SSE `site_ayar_changed` ile canlı güncellenir. Ayar SW önbelleğine alınmaz (public/sw.js baypas listesi).
 */
import { useSyncExternalStore } from 'react';
import { GIZLI_SAYFALAR, KAPALI_SAYFALAR } from '../components/merkez/sayfaSabitleri';
import { icerikDurumu, type IcerikTur } from './icerikGorunurlukKural';
export type { IcerikTur } from './icerikGorunurlukKural';

export type SayfaDurumu = 'acik' | 'gizli' | 'kapali' | 'yalniz-yonetici';
export type Duyuru = { acik: boolean; metin: string; ton: 'bilgi' | 'uyari' | 'hata'; baglanti?: string; baslangic?: string; bitis?: string; kurul?: number[]; kapatilabilir?: boolean };
export type GenelSiteAyar = {
  surum: number;
  guncellendi: string;
  sayfalar: Record<string, SayfaDurumu>;
  /** Rota → menüde görünsün mü (false: menü/merkezden kalkar, adresle açılır) */
  menu: Record<string, boolean>;
  bayraklar: Record<string, boolean>;
  gorunurluk: Record<string, 'acik' | 'gizli' | 'yalniz-yonetici'>;
  duyuru: Duyuru | null;
  bakim: { acik: boolean; sure?: string; mesaj?: string };
};

const KEY = 'medsoru_site_ayar_v1';
const BOS: GenelSiteAyar = { surum: 0, guncellendi: '', sayfalar: {}, menu: {}, bayraklar: {}, gorunurluk: {}, duyuru: null, bakim: { acik: false } };

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

/** Yönetici mi (App.tsx bildirir): 'yalniz-yonetici' / 'kapali' sayfalar yöneticinin menüsünde kalır */
let yonetici = false;
export function yoneticiAyarla(v: boolean) {
  if (yonetici === v) return;
  yonetici = v;
  ayar = { ...ayar };
  dinleyiciler.forEach((f) => f());
}

/**
 * Bayrağa bağlı sayfalar: bayrak kapalıyken sayfa öğrenciye gizlidir (menüden kalkar, adresle Bugün'e döner).
 * Bayrak listesi ve anlamı: docs/YONETIM_V16_KIT.md §5.4 (sunucu kapısı yonetim16/siteAyar.ts BAYRAK_UC).
 */
export const BAYRAK_SAYFA: Record<string, string[]> = {
  oyunlar: ['oyunlar'],
  arkadaslik: ['arkadaslar'],
  siralama_herkese: ['leaderboard'],
};

/** Menüden ve adresten gizli mi (öğrenci için). Panel 'acik' derse sabit gizli sayfa da açılır. */
export function sayfaGizli(route: string): boolean {
  const d = ayar.sayfalar[route];
  if (d === 'gizli') return true;
  if (d === 'acik' || d === 'kapali' || d === 'yalniz-yonetici') return false;
  return GIZLI_SAYFALAR.has(route as never);
}

/** Sayfa bayrağı kapalı mı (BAYRAK_SAYFA) */
function bayrakKapatti(route: string): boolean {
  for (const [ad, rotalar] of Object.entries(BAYRAK_SAYFA)) if (rotalar.includes(route) && ayar.bayraklar[ad] === false) return true;
  return false;
}

/** Öğrenci bu adrese girerse Bugün'e mi dönmeli (gizli, yalnız yönetici ya da bayrağı kapalı) */
export function sayfaYonlendir(route: string, admin = yonetici): boolean {
  if (sayfaGizli(route)) return true;
  if (admin) return false;
  return ayar.sayfalar[route] === 'yalniz-yonetici' || bayrakKapatti(route);
}

/** Menüde ve merkez kartlarında görünsün mü (çalışma anı; navModel/merkezModel/navV15 çizim anında süzer) */
export function menudeGorunur(route: string): boolean {
  if (ayar.menu[route] === false) return false;
  if (sayfaGizli(route)) return false;
  if (yonetici) return true;
  return !sayfaKapali(route) && !sayfaYonlendir(route, false);
}

/** Öğrenciye kapalı mı (sayfa "kapalı" ekranı gösterir; KAPALI_SAYFALAR anlamı) */
export function sayfaKapali(route: string): boolean {
  const d = ayar.sayfalar[route];
  if (d === 'kapali') return true;
  if (d === 'acik' || d === 'gizli' || d === 'yalniz-yonetici') return false;
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

/**
 * İçerik görünürlüğü (öğrenci): ders/kurul/deste/sesli/paket/onem/asistan/cozucu kapalı mı. Yönetici her şeyi görür.
 * Kural (ders ve kurul kalıtımı) icerikGorunurlukKural.ts'de; sunucu kapısı aynı kuralı kullanır (yonetim16/siteAyar.ts icerikKapisi).
 * Bileşen useSiteAyar() ile abone olmalı ki panel değişince liste yeniden süzülsün.
 */
export function icerikGizli(tur: IcerikTur, id: string | number | null | undefined, admin = yonetici): boolean {
  if (admin || id == null || id === '') return false;
  return icerikDurumu(ayar.gorunurluk, tur, String(id)) !== 'acik';
}
export const kurulGizli = (n: number, admin = yonetici) => icerikGizli('kurul', n, admin);
export const yoneticiMi = () => yonetici;

/**
 * Saf hesap (yönetim paneli önizlemesi): verilen ayarla bir öğrencinin bu sayfayı nasıl gördüğü.
 * İstemci kuralları (sayfaGizli/sayfaKapali/sayfaYonlendir/menudeGorunur) ile aynı mantık.
 */
export function ogrenciGorunumu(route: string, a: Pick<GenelSiteAyar, 'sayfalar' | 'menu' | 'bayraklar'>): { erisim: 'acik' | 'gizli' | 'kapali' | 'yalniz-yonetici' | 'bayrak'; menude: boolean; kaynak: 'panel' | 'varsayilan' } {
  const d = a.sayfalar?.[route];
  let erisim: 'acik' | 'gizli' | 'kapali' | 'yalniz-yonetici' | 'bayrak' = d || (GIZLI_SAYFALAR.has(route as never) ? 'gizli' : KAPALI_SAYFALAR.has(route as never) ? 'kapali' : 'acik');
  if (erisim === 'acik') for (const [ad, r] of Object.entries(BAYRAK_SAYFA)) if (r.includes(route) && a.bayraklar?.[ad] === false) erisim = 'bayrak';
  return { erisim, menude: erisim === 'acik' && a.menu?.[route] !== false, kaynak: d ? 'panel' : 'varsayilan' };
}

function abone(f: () => void) { dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; }

/** Modül düzeyi abonelik (menü listelerini yerinde yeniden hesaplamak için); React bileşenleri useSiteAyar kullanır */
export const siteAyarAbone = abone;

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
