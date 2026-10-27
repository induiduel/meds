/**
 * Arkadaşlık + açık profil istemcisi (sunucu: services/arkadaslik.ts). Kimlik = açık profil kimliği (10 hex), uid değil.
 * Canlı: SSE `arkadas_changed` {who} yalnız bu kullanıcıya aitse dinleyiciyi çağırır.
 */
import { useEffect, useRef } from 'react';
import { safeJsonFetch } from './api';
import { auth, getRememberedStudentInfo } from './auth';
import { realtimeEventService } from './realtimeEvents';
import { navigateTo } from '../router';

export type Iliski = 'ben' | 'arkadas' | 'giden' | 'gelen' | 'yok';
export interface KisiKart { kimlik: string; ad: string; foto?: string; universite?: string; donem?: number | null; gizli?: boolean; haftaSn?: number; bugunSn?: number; son?: { ad: string; modul: string; at: number }; iliski?: Iliski; at?: number }
export interface DersSatir { ad: string; modul: string; sn: number; soru?: number; bitti?: boolean; at?: number }
export interface AcikProfil {
  kimlik: string; ben?: boolean; iliski: Iliski; gizli?: boolean; acik?: boolean; arkadasN?: number;
  ad: string; foto?: string; universite?: string; donem?: number | null; kidem?: string; unvan?: string;
  calisma?: { toplam: number; hafta: number; bugun: number }; soru?: { toplam: number; hafta: number; bugun: number };
  bitirilen?: number; basarim?: number; puan?: { hafta: number; toplam: number }; dogru?: number; yanlis?: number;
  son?: { ad: string; modul: string; at: number } | null; dersler?: DersSatir[]; haftaDersler?: DersSatir[];
}

const post = <T,>(url: string, body?: any) => safeJsonFetch<T>(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) });
const hataOf = (r: { data?: any; error?: string }, yedek: string) => r.data?.error || r.error || yedek;

export const benimAdim = () => {
  try { const a = localStorage.getItem('medsoru_topluluk_ad'); if (a) return a; } catch { /* yok */ }
  return (auth.currentUser?.displayName || getRememberedStudentInfo().name || 'Öğrenci').split(' ')[0];
};

export async function arkadasIslem(tur: 'istek' | 'kabul' | 'reddet' | 'cikar', kimlik: string): Promise<{ iliski?: Iliski; hata?: string }> {
  const r = await post<{ iliski: Iliski }>(`/api/arkadas/${tur}`, { kimlik });
  return r.ok ? { iliski: r.data?.iliski } : { hata: hataOf(r, 'İşlem yapılamadı.') };
}
/** Birebir sohbeti açar ve Topluluk sohbet ekranına gider */
export async function mesajAc(kimlik: string): Promise<string> {
  const r = await post<{ id: number }>('/api/arkadas/sohbet', { kimlik, benAd: benimAdim() });
  if (!r.ok || !r.data?.id) return hataOf(r, 'Sohbet açılamadı.');
  git(`/topluluk?sohbet=${r.data.id}`);
  return '';
}
export async function davetEt(kimlik: string, oda: string): Promise<string> {
  const r = await post('/api/arkadas/davet', { kimlik, oda, benAd: benimAdim() });
  return r.ok ? '' : hataOf(r, 'Davet gönderilemedi.');
}

export const git = (adres: string) => { navigateTo(adres); window.dispatchEvent(new PopStateEvent('popstate')); };
export const profilYolu = (kimlik: string) => `/kisi/${kimlik}`;

export const sure = (sn = 0) => {
  const dk = Math.round(sn / 60);
  if (dk < 60) return `${dk} dk`;
  const sa = Math.floor(dk / 60), k = dk % 60;
  return k ? `${sa} sa ${k} dk` : `${sa} sa`;
};
export const once = (t?: number) => {
  if (!t) return '';
  const dk = Math.round((Date.now() - t) / 60_000);
  if (dk < 1) return 'şimdi'; if (dk < 60) return `${dk} dk önce`; if (dk < 24 * 60) return `${Math.round(dk / 60)} sa önce`;
  if (dk < 48 * 60) return 'dün'; return new Date(t).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};
export const basHarf = (s: string) => s.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toLocaleUpperCase('tr-TR') || '?';

/** Bu kullanıcıya ait arkadaşlık olayında (istek, kabul, davet) fn çağrılır */
export function useArkadasCanli(fn: () => void) {
  const ref = useRef(fn); ref.current = fn;
  useEffect(() => {
    let benim = '';
    const uid = auth.currentUser?.uid;
    if (uid && crypto?.subtle) void crypto.subtle.digest('SHA-256', new TextEncoder().encode(`ud:${uid}`)).then((b) => {
      benim = Array.from(new Uint8Array(b), (x) => x.toString(16).padStart(2, '0')).join('').slice(0, 16);
    }).catch(() => 0);
    const offs = [
      realtimeEventService.on('arkadas_changed', (p: any) => { if (p?.who && p.who === benim) ref.current(); }),
      realtimeEventService.on('resync', () => ref.current()),
    ];
    return () => offs.forEach((o) => o());
  }, []);
}
