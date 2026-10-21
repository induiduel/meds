/**
 * Başarım istemci deposu (2026-10-20): kurallar (`/api/basarim/tanim`) + kişinin durumu (`/api/basarim/durum`).
 * Açılışta, 90 sn'de bir (sekme görünürken), odakta ve sunucunun `basarim_changed` olayında tazelenir.
 * Yeni ödüller (`durum.yeni`) kutlama kuyruğuna girer; kutlama kapanınca `goruldu` ile tüm cihazlarda işaretlenir.
 * Kimlik: istekler services/adminFetchAuth.ts ile Firebase jetonu taşır.
 */
import { useSyncExternalStore } from 'react';
import yerelTanim from '../data/basarim/tanim.json';
import { safeJsonFetch } from './api';

export type Seviye = [number, number, number];
export interface HedefT { id: string; donem: 'gun' | 'hafta' | 'kurul'; ad: string; olcu: string; ikon?: string; seviyeler: Seviye[] }
export interface BasarimT { id: string; ad: string; aciklama?: string; olcu: string; ikon?: string; renk?: string; topluluk?: boolean; seviyeler: Seviye[] }
export interface KilitT { id: string; tur: 'unvan' | 'cerceve' | 'efekt' | 'icerik' | 'renk' | 'esya'; ad: string; fiyat: number; etkin: boolean; renk?: string; aciklama?: string; kidem?: number; kidemAcar?: boolean; eski?: boolean }
export interface KidemT { no: number; ad: string; tavan: number; aciklama?: string }
export interface Tanim {
  atp: { baslangic: number; gunlukTavan: number; haftalikSiralama: number[]; kurulSiralama: number[]; siralamaEsikPuan: { hafta: number; kurul: number } };
  taban: Record<string, number>;
  eylemler: { id: string; ad: string; p: number; gunlukTavan: number }[];
  hedefler: HedefT[]; basarimlar: BasarimT[]; kilitler: KilitT[]; kidemler?: KidemT[];
}
export interface Odul { id: string; t: 'baslangic' | 'hedef' | 'basarim' | 'siralama' | 'harcama' | 'yonetici'; by?: string; geriAlindi?: string; ad: string; p: number; a: number; at: string; g: string; ust?: boolean; ref?: string }
export interface Pencere { id: string; bas: string; son: string; ad: string }
export interface Durum {
  profil: { donem: number | null; kurul: number | null; ad: string };
  puan: { toplam: number; bugun: number };
  /** tavan null: sınırsız (yönetici / muaf) */
  atp: { bakiye: number; kuyrukta: number; bugunAlinan: number; tavan: number | null };
  kidem?: KidemT & { sonraki: KidemT | null };
  esya?: Record<string, number>;
  calisma?: { bugun: number; hafta: number; dersler: CalismaDers[] };
  seri: number;
  hedefler: { id: string; deger: number; pencere: Pencere; alinan: number }[];
  basarimlar: { id: string; deger: number; alinan: number }[];
  siralama: Record<'hafta' | 'kurul' | 'tum', { sira: number | null; kisi: number; puan: number }>;
  kurulPencere: Pencere;
  defter: Odul[];
  yeni: Odul[];
  kilit: Record<string, string>;
  secili: { unvan?: string; cerceve?: string; efekt?: string; renk?: string };
  /** Yöneticinin verdiği gizli unvan (muaf: günlük sınırlar ve içerik kilitleri uygulanmaz) */
  ozel?: { unvan: string; muaf: boolean } | null;
}

interface Durumu { tanim: Tanim; durum: Durum | null; hata: string; uid: string | null; kutlama: Odul[] }
let s: Durumu = { tanim: yerelTanim as any, durum: null, hata: '', uid: null, kutlama: [] };
const dinleyici = new Set<() => void>();
const yay = (y: Partial<Durumu>) => { s = { ...s, ...y }; dinleyici.forEach((f) => f()); };
const abone = (f: () => void) => { dinleyici.add(f); return () => dinleyici.delete(f); };
export const useBasarim = () => useSyncExternalStore(abone, () => s, () => s);
export const basarimDurumu = () => s;

const goste = new Set<string>();
const durumAl = (d: Durum) => {
  // Yönetici düzeltmesi (düşme, not) ve geri alınan ödül kutlanmaz; yalnız hediye kutlanır
  const yeni = (d.yeni || []).filter((o) => !goste.has(o.id) && !o.geriAlindi && (o.t !== 'yonetici' || o.p > 0 || o.a > 0));
  yeni.forEach((o) => goste.add(o.id));
  // Aynı anda çok ödül gelirse (ilk açılış) en değerli 6'sı tek tek, gerisi özet olarak gösterilir
  const sirali = [...yeni].sort((a, b) => b.a * 20 + b.p - (a.a * 20 + a.p));
  const kutlama = [...s.kutlama, ...sirali.slice(0, 6)];
  if (sirali.length > 6) {
    const kalan = sirali.slice(6);
    kutlama.push({ id: `ozet-${Date.now()}`, t: 'hedef', ad: `${kalan.length} ödül daha`, p: kalan.reduce((x, o) => x + o.p, 0), a: kalan.reduce((x, o) => x + o.a, 0), at: kalan[0].at, g: kalan[0].g });
  }
  yay({ durum: d, hata: '', kutlama });
  // Açılmış kilitler cihazda da tutulur: internetsizken (durum gelmeden) açılmış içerik kilit ekranında kalmasın
  try { if (s.uid) localStorage.setItem(`${KILIT_KEY}:${s.uid}`, JSON.stringify(d.kilit || {})); } catch { /* gizli pencere */ }
};
const KILIT_KEY = 'medsoru_basarim_kilit_v1';
/** Son bilinen açık kilitler (sunucu durumu henüz gelmediyse / internet yoksa) */
export function kilitOnbellek(): Record<string, string> {
  try { return s.uid ? JSON.parse(localStorage.getItem(`${KILIT_KEY}:${s.uid}`) || '{}') : {}; } catch { return {}; }
}

async function istek<T>(url: string, init?: RequestInit): Promise<T> {
  const r = await safeJsonFetch<any>(url, { ...init, headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) } });
  if (!r.ok) throw new Error(r.data?.error || r.error || `İstek başarısız (${r.status})`);
  return r.data as T;
}

let sonIstek = 0;
let calisiyor: Promise<void> | null = null;
export function yenile(zorla = false): Promise<void> {
  if (!s.uid) return Promise.resolve();
  if (!zorla && Date.now() - sonIstek < 15_000) return calisiyor || Promise.resolve();
  sonIstek = Date.now();
  calisiyor = istek<Durum>('/api/basarim/durum').then(durumAl, (e) => yay({ hata: e.message })).finally(() => { calisiyor = null; });
  return calisiyor;
}

let kurulu = false;
let sseKurulu = false;
/** Oturum açılınca App çağırır; çıkışta null. */
export function basarimBaslat(uid: string | null) {
  if (uid === s.uid) return;
  goste.clear();
  yay({ uid, durum: null, kutlama: [], hata: '' });
  if (!uid) return;
  void istek<Tanim>('/api/basarim/tanim').then((t) => t?.hedefler && yay({ tanim: t })).catch(() => 0);
  void yenile(true);
  if (!kurulu) {
    kurulu = true;
    window.setInterval(() => { if (document.visibilityState === 'visible') void yenile(); }, 90_000);
    document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') void yenile(); });
  }
  if (!sseKurulu) {
    sseKurulu = true;
    void import('./realtimeEvents').then(({ realtimeEventService }) => {
      realtimeEventService.on('basarim_changed', async (p: any) => {
        if (!p?.who || !s.uid) return;
        const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(`ud:${s.uid}`));
        const hex = Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, '0')).join('');
        if (hex.slice(0, 16) === p.who) void yenile(true);
      });
    }).catch(() => 0);
  }
}

export async function profilKaydet(donem: number, kurul: number, ad?: string) {
  durumAl(await istek<Durum>('/api/basarim/profil', { method: 'POST', body: JSON.stringify({ donem, kurul, ad }) }));
}
export async function satinAl(id: string) {
  durumAl(await istek<Durum>('/api/basarim/satin-al', { method: 'POST', body: JSON.stringify({ id }) }));
}
export async function sec(tur: 'unvan' | 'cerceve' | 'efekt' | 'renk', id: string | null) {
  durumAl(await istek<Durum>('/api/basarim/sec', { method: 'POST', body: JSON.stringify({ tur, id }) }));
}
/** Kutlama kuyruğunun başı kapandı. */
export function kutlamaKapat() {
  const [ilk, ...kalan] = s.kutlama;
  yay({ kutlama: kalan });
  if (!kalan.length && ilk) {
    const at = [ilk, ...(s.durum?.yeni || [])].reduce((m, o) => (o.at > m ? o.at : m), '');
    if (at) void istek('/api/basarim/goruldu', { method: 'POST', body: JSON.stringify({ at }) }).catch(() => 0);
  }
}
export function kutlamalariAtla() {
  const at = [...s.kutlama, ...(s.durum?.yeni || [])].reduce((m, o) => (o.at > m ? o.at : m), '');
  yay({ kutlama: [] });
  if (at) void istek('/api/basarim/goruldu', { method: 'POST', body: JSON.stringify({ at }) }).catch(() => 0);
}

export interface CalismaDers { id: string; ad: string; modul: string; sn: number }
export interface CalismaSatir { sira: number; ad: string; sn: number; ben: boolean; renk?: string; cerceve?: string; kidem?: string; dersler: CalismaDers[] }
export const calismaGetir = (kapsam: 'gun' | 'hafta', donem?: number) =>
  istek<{ donem: number; pencere: Pencere; satir: CalismaSatir[]; benim: number | null; odul: number; esikSn: number }>(`/api/basarim/calisma?kapsam=${kapsam}${donem ? `&donem=${donem}` : ''}`);
export interface SiraSatir { sira: number; ad: string; puan: number; ben: boolean; unvan?: string; ozel?: boolean; renk?: string; kidem?: string; cerceve?: string; basarim: number }
export const siralamaGetir = (kapsam: 'hafta' | 'kurul' | 'tum', donem?: number) =>
  istek<{ donem: number; pencere: Pencere; satir: SiraSatir[]; atpOdul: number[] }>(`/api/basarim/siralama?kapsam=${kapsam}${donem ? `&donem=${donem}` : ''}`);

// ───── Biçim ─────
export const sayi = (n: number) => Math.round(n).toLocaleString('tr-TR');
export function olcuYaz(olcu: string, n: number): string {
  if (olcu === 'calisma_sn') {
    const sa = n / 3600;
    return sa >= 10 ? `${sayi(sa)} sa` : sa >= 1 ? `${(Math.floor(sa * 10) / 10).toLocaleString('tr-TR')} sa` : `${Math.floor(n / 60)} dk`;
  }
  const birim: Record<string, string> = {
    soru: 'soru', bitirilen: 'ders', oturum: 'oturum', aktif_gun: 'gün', giris_gun: 'gün', seri: 'gün', oturum_max: 'oturum',
    ust_hedef: 'hedef', podyum: 'hafta', soru_ekle: 'soru', parca: 'katkı', sik: 'şık', yorum: 'yorum', begeni: 'beğeni', hata: 'bildirim',
  };
  return `${sayi(n)} ${birim[olcu] || ''}`.trim();
}
export const KILIT_TUR_AD: Record<KilitT['tur'], string> = { unvan: 'Kıdem ve unvanlar', cerceve: 'Çerçeveler', efekt: 'Kutlama efektleri', icerik: 'İçerikler', renk: 'İsim renkleri', esya: 'Eşyalar' };
export const sureYaz = (sn: number) => { const sa = Math.floor(sn / 3600), dk = Math.floor((sn % 3600) / 60); return sa ? `${sa} sa ${dk} dk` : `${dk} dk`; };
