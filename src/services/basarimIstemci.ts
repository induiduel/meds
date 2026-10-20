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
export interface KilitT { id: string; tur: 'unvan' | 'cerceve' | 'efekt' | 'icerik'; ad: string; fiyat: number; etkin: boolean; renk?: string }
export interface Tanim {
  atp: { baslangic: number; gunlukTavan: number; haftalikSiralama: number[]; kurulSiralama: number[]; siralamaEsikPuan: { hafta: number; kurul: number } };
  taban: Record<string, number>;
  eylemler: { id: string; ad: string; p: number; gunlukTavan: number }[];
  hedefler: HedefT[]; basarimlar: BasarimT[]; kilitler: KilitT[];
}
export interface Odul { id: string; t: 'baslangic' | 'hedef' | 'basarim' | 'siralama' | 'harcama'; ad: string; p: number; a: number; at: string; g: string; ust?: boolean; ref?: string }
export interface Pencere { id: string; bas: string; son: string; ad: string }
export interface Durum {
  profil: { donem: number | null; kurul: number | null; ad: string };
  puan: { toplam: number; bugun: number };
  atp: { bakiye: number; kuyrukta: number; bugunAlinan: number; tavan: number };
  seri: number;
  hedefler: { id: string; deger: number; pencere: Pencere; alinan: number }[];
  basarimlar: { id: string; deger: number; alinan: number }[];
  siralama: Record<'hafta' | 'kurul' | 'tum', { sira: number | null; kisi: number; puan: number }>;
  kurulPencere: Pencere;
  defter: Odul[];
  yeni: Odul[];
  kilit: Record<string, string>;
  secili: { unvan?: string; cerceve?: string; efekt?: string };
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
  const yeni = (d.yeni || []).filter((o) => !goste.has(o.id));
  yeni.forEach((o) => goste.add(o.id));
  // Aynı anda çok ödül gelirse (ilk açılış) en değerli 6'sı tek tek, gerisi özet olarak gösterilir
  const sirali = [...yeni].sort((a, b) => b.a * 20 + b.p - (a.a * 20 + a.p));
  const kutlama = [...s.kutlama, ...sirali.slice(0, 6)];
  if (sirali.length > 6) {
    const kalan = sirali.slice(6);
    kutlama.push({ id: `ozet-${Date.now()}`, t: 'hedef', ad: `${kalan.length} ödül daha`, p: kalan.reduce((x, o) => x + o.p, 0), a: kalan.reduce((x, o) => x + o.a, 0), at: kalan[0].at, g: kalan[0].g });
  }
  yay({ durum: d, hata: '', kutlama });
};

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
export async function sec(tur: 'unvan' | 'cerceve' | 'efekt', id: string | null) {
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

export interface SiraSatir { sira: number; ad: string; puan: number; ben: boolean; unvan?: string; cerceve?: string; basarim: number }
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
export const KILIT_TUR_AD: Record<KilitT['tur'], string> = { unvan: 'Unvanlar', cerceve: 'Çerçeveler', efekt: 'Kutlama efektleri', icerik: 'İçerikler' };
