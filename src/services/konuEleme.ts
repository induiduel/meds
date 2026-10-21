/**
 * Bitirdiklerim › konu eleme (2026-10-21): öğrenci bir dersi iki biçimde hesap dışı bırakır.
 *  - 'calisma'  "Çalışmayacağım": sınavda sorusu var ama çalışmayacak. Kalan süreden düşer; Sınav planı o derse adım
 *               koymaz, sorularını bugünkü bilgisiyle (çalışılmamış) sayar.
 *  - 'sorusuz'  "Sınavda sorusu yok": kalan süreden düşer; Sınav planı dersi soru dağılımından tamamen çıkarır.
 *  - 'baska'    "Başka yerden çalıştım": konu bitmiş sayılır (kalan süreden düşer, plan o kaynağı tamam sayar) ama
 *               uygulamada süre ölçülmediği için çalışma hızına girmez. Yalnız o modülün konusuna uygulanır.
 * Anahtar ('calisma'/'sorusuz'): modüller arası ortak ders `<branş>|<no>` (sesli, çözücü, en önemliler aynı dersi paylaşır); eşleşmeyen
 * konularda `<modül>:<konu id>`. Profil kv ile cihazlar arası eşitlenir (userKvSync).
 */
import { useSyncExternalStore } from 'react';

export type ElemeTur = 'calisma' | 'sorusuz' | 'baska';
export const ELEME_AD: Record<ElemeTur, string> = { baska: 'Başka yerden çalıştım', calisma: 'Çalışmayacağım', sorusuz: 'Sınavda sorusu yok' };
export const ELEME_KEY = 'medsoru_konu_eleme_v1';
type Kayit = Record<string, ElemeTur>;

let onbellek: { ham: string | null; v: Kayit } = { ham: null, v: {} };
export function elemeOku(): Kayit {
  let ham: string | null = null;
  try { ham = localStorage.getItem(ELEME_KEY); } catch { /* yok */ }
  if (ham === onbellek.ham) return onbellek.v;
  let v: Kayit = {};
  try { const x = JSON.parse(ham || '{}'); if (x && typeof x === 'object') v = x; } catch { /* bozuk */ }
  onbellek = { ham, v };
  return v;
}
const abone = new Set<() => void>();
export function elemeYaz(anahtar: string, tur: ElemeTur | null) {
  const v = { ...elemeOku() };
  if (tur) v[anahtar] = tur; else delete v[anahtar];
  try { localStorage.setItem(ELEME_KEY, JSON.stringify(v)); } catch { /* yok */ }
  abone.forEach((f) => f());
}
const aboneOl = (f: () => void) => {
  abone.add(f);
  const st = (e: StorageEvent) => { if (e.key == null || e.key === ELEME_KEY) f(); };
  window.addEventListener('storage', st);
  return () => { abone.delete(f); window.removeEventListener('storage', st); };
};
export const useEleme = () => useSyncExternalStore(aboneOl, elemeOku, () => ({} as Kayit));

/** Konunun eleme anahtarı: ortak ders varsa `<branş>|<no>`, yoksa `<modül>:<id>` ('baska' her zaman modül konusu) */
export const elemeAnahtari = (modul: string, k: { id: string; ders?: string }, tur?: ElemeTur) =>
  tur === 'baska' || !k.ders ? `${modul}:${k.id}` : k.ders;
/** Konunun geçerli işareti: önce ders geneli (çalışmayacağım / sorusuz), sonra modül konusu (başka yerden) */
export const konuElemesi = (v: Record<string, ElemeTur>, modul: string, k: { id: string; ders?: string }): ElemeTur | undefined =>
  (k.ders && v[k.ders]) || v[`${modul}:${k.id}`];
