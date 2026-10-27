/**
 * Kişisel program kayıtları: öğrencinin ders programına elle eklediği etkinlikler (lab, grup çalışması, telafi…).
 * Profil anahtarı (userKvSync SYNC_PATTERNS) — cihazlar arasında eşitlenir. Resmî program (ders kayıt defteri)
 * değişmez; bu kayıtlar yalnız öğrencinin kendi görünümüne eklenir.
 */
import { useSyncExternalStore } from 'react';

export interface KisiselEtkinlik { id: string; baslik: string; tarih: string; bas: string; bit: string; yer?: string; at: string }
export const KISISEL_PROGRAM_KEY = 'medsoru_kisisel_program_v1';
const OLAY = 'medsor:kisisel-program';

let ham: string | null | undefined;
let onb: KisiselEtkinlik[] = [];
export const kisiselOku = (): KisiselEtkinlik[] => {
  let h: string | null = null;
  try { h = localStorage.getItem(KISISEL_PROGRAM_KEY); } catch { /* yok */ }
  if (h !== ham) {
    ham = h;
    try { const v = h ? JSON.parse(h) : []; onb = Array.isArray(v) ? v : []; } catch { onb = []; }
  }
  return onb;
};
const yaz = (l: KisiselEtkinlik[]) => {
  try { localStorage.setItem(KISISEL_PROGRAM_KEY, JSON.stringify(l)); } catch { /* dolu */ }
  window.dispatchEvent(new Event(OLAY));
};
export const kisiselEkle = (e: Omit<KisiselEtkinlik, 'id' | 'at'>) =>
  yaz([...kisiselOku(), { ...e, id: `kp-${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`, at: new Date().toISOString() }]
    .sort((a, b) => a.tarih.localeCompare(b.tarih) || a.bas.localeCompare(b.bas)));
export const kisiselSil = (id: string) => yaz(kisiselOku().filter((x) => x.id !== id));
const abone = (f: () => void) => {
  const g = (e: Event) => { if (!(e instanceof StorageEvent) || e.key === KISISEL_PROGRAM_KEY) f(); };
  window.addEventListener(OLAY, g); window.addEventListener('storage', g); window.addEventListener('medsoru:user-data-applied', f);
  return () => { window.removeEventListener(OLAY, g); window.removeEventListener('storage', g); window.removeEventListener('medsoru:user-data-applied', f); };
};
export const useKisiselProgram = () => useSyncExternalStore(abone, kisiselOku, kisiselOku);
