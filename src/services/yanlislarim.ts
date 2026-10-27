/**
 * Yanlışlarım (tasarım v15 › C04 "48 saat sonra yeniden soracağım", C09 Yanlışlarım).
 * Soru çöz / deneme testlerinde yanlış yapılan soru deftere girer; vadesi 48 sa sonra gelir. Tekrarda doğru
 * yapılınca kutu bir artar ve aralık uzar (2 → 4 → 8 → 16 gün); 4. kutudan sonra "öğrenildi". Yanlışta kutu sıfırlanır.
 * Sorunun kendisi de saklanır (çözüm ekranı soruyu yeniden kurabilsin). En çok 400 kayıt; anahtar userKvSync
 * SYNC_PATTERNS'te (hesaba eşitlenir). Öğren hata defterinden (learnReview) ayrıdır.
 */
import { useSyncExternalStore } from 'react';
import type { QuestionItem } from '../types';

/** neden: öğrencinin kendi seçtiği yanlış nedeni (tasarım C05 "Neden yanlış yaptın?") */
export interface YanlisKayit { q: QuestionItem; box: number; due: number; son: number; yanlis: number; neden?: string }
export const NEDENLER = ['Bilmiyordum', 'Karıştırdım', 'Dikkatsizlik', 'Soruyu yanlış okudum'] as const;
export const YANLIS_KEY = 'medsoru_yanlislarim_v1';
const OLAY = 'medsoru:yanlislarim';
const GUN = 86_400_000;
const ARALIK = [2, 4, 8, 16]; // gün; kutu 0 → 2 gün (48 sa)
export const OGRENILDI_KUTU = ARALIK.length;

let ham: string | null = null;
let onb: Record<string, YanlisKayit> = {};
export function yanlisOku(): Record<string, YanlisKayit> {
  let h: string | null = null;
  try { h = localStorage.getItem(YANLIS_KEY); } catch { /* yok */ }
  if (h !== ham) { ham = h; try { onb = h ? JSON.parse(h) : {}; } catch { onb = {}; } }
  return onb;
}
function yaz(d: Record<string, YanlisKayit>) {
  const l = Object.entries(d).sort((a, b) => b[1].son - a[1].son).slice(0, 400);
  try { localStorage.setItem(YANLIS_KEY, JSON.stringify(Object.fromEntries(l))); } catch { /* dolu */ }
  window.dispatchEvent(new Event(OLAY));
}

/** Cevap sonrası: yanlışsa deftere (kutu 0, 48 sa), defterdeki soru doğruysa kutu artar */
export function yanlisKaydet(q: QuestionItem, dogru: boolean, simdi = Date.now()) {
  if (!q?.id || !q.reconstruction) return;
  const d = { ...yanlisOku() };
  const e = d[q.id];
  if (!dogru) d[q.id] = { q, box: 0, due: simdi + ARALIK[0] * GUN, son: simdi, yanlis: (e?.yanlis || 0) + 1 };
  else if (e) {
    const box = Math.min(OGRENILDI_KUTU, e.box + 1);
    d[q.id] = { ...e, box, son: simdi, due: box >= OGRENILDI_KUTU ? Infinity : simdi + ARALIK[box] * GUN };
  } else return;
  yaz(d);
}
export const yanlisNeden = (id: string, neden: string | null) => { const d = { ...yanlisOku() }; if (!d[id]) return; d[id] = { ...d[id], neden: neden || undefined }; yaz(d); };
export const yanlisGeriKoy = (e: YanlisKayit) => { const d = { ...yanlisOku() }; d[e.q.id] = e; yaz(d); };
export const yanlisSil = (id: string) => { const d = { ...yanlisOku() }; delete d[id]; yaz(d); };

export function yanlisGruplari(simdi = Date.now()) {
  const l = Object.values(yanlisOku());
  return {
    hazir: l.filter((e) => e.box < OGRENILDI_KUTU && e.due <= simdi).sort((a, b) => a.due - b.due),
    bekleyen: l.filter((e) => e.box < OGRENILDI_KUTU && e.due > simdi).sort((a, b) => a.due - b.due),
    ogrenildi: l.filter((e) => e.box >= OGRENILDI_KUTU).sort((a, b) => b.son - a.son),
  };
}
const abone = (f: () => void) => {
  const g = (e: Event) => { if (!(e instanceof StorageEvent) || e.key === YANLIS_KEY) f(); };
  window.addEventListener(OLAY, g); window.addEventListener('storage', g);
  return () => { window.removeEventListener(OLAY, g); window.removeEventListener('storage', g); };
};
export const useYanlislar = () => useSyncExternalStore(abone, yanlisOku, yanlisOku);
