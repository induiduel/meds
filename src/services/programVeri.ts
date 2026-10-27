/**
 * Ders programı verisi (tek yükleyici): ders kayıt defteri `src/data/dersler/kN.json` + sunucudaki yer değişiklikleri
 * (`/api/ders-programi/duzen`). DersProgramiV15, program kartı (Bugün) ve içe aktarma sayfası aynı yükleyiciyi kullanır.
 */
import { safeJsonFetch } from './api';

export interface ProgDers { id: string; brans: string; konu: string; ogretim_uyesi?: string; tarih: string; saat?: string; saat_sayisi?: number; kisisel?: boolean }

export const PROGRAM_KAYITLARI = import.meta.glob('../data/dersler/k[1-6].json');
export const programVar = (kurul: number) => !!PROGRAM_KAYITLARI[`../data/dersler/k${kurul}.json`];
export const saatBas = (s?: string) => s?.split('-')[0] || '';

/** Saat çizelgesi: sabah ve öğleden sonra blokları; çok saatlik ders aynı blokta ardışık dilimleri doldurur */
export const SABAH = ['08:00-08:40', '08:50-09:30', '09:40-10:20', '10:30-11:10', '11:20-12:00'];
export const OGLE = ['13:00-13:40', '13:50-14:30', '14:40-15:20', '15:30-16:10'];

/** Dersin bitiş saati: çok saatlikse bloktaki son dilimin sonu, değilse kayıttaki aralığın sonu */
export function saatBitis(d: Pick<ProgDers, 'saat' | 'saat_sayisi'>): string {
  if (!d.saat) return '';
  const bas = saatBas(d.saat);
  const n = Math.max(1, d.saat_sayisi || 1);
  for (const blok of [SABAH, OGLE]) {
    const i = blok.findIndex((t) => saatBas(t) === bas);
    if (i >= 0) return blok[Math.min(blok.length - 1, i + n - 1)].split('-')[1];
  }
  return d.saat.split('-')[1] || '';
}

const onbellek = new Map<number, Promise<ProgDers[]>>();
export function programYukle(kurul: number, taze = false): Promise<ProgDers[]> {
  if (!taze && onbellek.has(kurul)) return onbellek.get(kurul)!;
  const yukle = PROGRAM_KAYITLARI[`../data/dersler/k${kurul}.json`];
  const p: Promise<ProgDers[]> = !yukle ? Promise.resolve([]) : yukle().then(async (m) => {
    const d = ((m as { default?: { dersler: ProgDers[] } }).default ?? (m as { dersler: ProgDers[] })).dersler || [];
    let duzen: Record<string, { tarih: string; saat?: string }> = {};
    try { duzen = (await safeJsonFetch<{ duzen: typeof duzen }>(`/api/ders-programi/duzen?kurul=${kurul}`)).data?.duzen || {}; } catch { /* resmî program */ }
    return d.map((x) => (duzen[x.id] ? { ...x, ...duzen[x.id] } : x))
      .sort((a, b) => a.tarih.localeCompare(b.tarih) || saatBas(a.saat).localeCompare(saatBas(b.saat)));
  }, () => []);
  onbellek.set(kurul, p);
  p.catch(() => onbellek.delete(kurul));
  return p;
}
