/**
 * KMB hata istatistiği (Eksiklerim): sınavdaki her deneme (vaka, OSCE sırası, kontrol listesi, sahnede bul, etiketleme,
 * hedef anlatımı, tekrar) bir kavram anahtarına yazılır. Kavram = öğrencinin unutabileceği tek şey: bir OSCE basamağı
 * (`b:<akış>:<basamak>`), bir vaka (`v:<id>`), bir yapı (`e:<sahne>:<öge>`, `u:<görev>`), bir hedef (`h:<no>`).
 * Her kavram ilgili öğretim adımını taşır (02.json `adim` alanı) → "bu adımı yeniden çalış".
 * Zayıf: en az bir yanlış ve ardından iki kez üst üste doğru yapılmamış. Veri `medsoru_kmb_hata_<kod>` (userKvSync ile
 * hesaba eşitlenir), olay `kmb-hata` ile ekranlar yenilenir.
 */
import { useEffect, useState } from 'react';

export type Kaynak = 'vaka' | 'sira' | 'kontrol' | 'bul' | 'etiket' | 'hedef' | 'tekrar';
export type KavramTur = 'basamak' | 'vaka' | 'yapi' | 'hedef';
export type Kavram = { tur: KavramTur; ad: string; adim?: string; y: number; d: number; seri: number; t: number; son: Kaynak };
export type HataVeri = { k: Record<string, Kavram>; s: Partial<Record<Kaynak, [number, number]>>; g: Record<string, [number, number]> };

export const KAYNAK_AD: Record<Kaynak, string> = {
  vaka: 'Vaka soruları', sira: 'OSCE sırası', kontrol: 'Kontrol listesi', bul: 'Sahnede bul', etiket: 'Etiketleme', hedef: 'Hedef anlatımı', tekrar: 'Eksik tekrarı',
};
const OLAY = 'kmb-hata';
const anahtar = (kod: string) => `medsoru_kmb_hata_${kod}`;
const bos = (): HataVeri => ({ k: {}, s: {}, g: {} });

export function hataOku(kod: string): HataVeri {
  try {
    const v = JSON.parse(localStorage.getItem(anahtar(kod)) || 'null');
    return v && typeof v === 'object' && v.k ? { k: v.k, s: v.s || {}, g: v.g || {} } : bos();
  } catch { return bos(); }
}
function yaz(kod: string, v: HataVeri) {
  try { localStorage.setItem(anahtar(kod), JSON.stringify(v)); } catch { /* özel pencere: yalnız oturumda */ }
  window.dispatchEvent(new CustomEvent(OLAY, { detail: kod }));
}
const gun = (t = Date.now()) => new Date(t - new Date(t).getTimezoneOffset() * 60000).toISOString().slice(0, 10);

/** Tek denemeyi yaz. `meta` kavramın adı/türü/adımı (ilk kayıtta ve her seferinde güncellenir). */
export function hataKaydet(kod: string, id: string, dogru: boolean, kaynak: Kaynak, meta: { tur: KavramTur; ad: string; adim?: string }) {
  const v = hataOku(kod);
  const o = v.k[id] || { ...meta, y: 0, d: 0, seri: 0, t: 0, son: kaynak };
  v.k[id] = { ...o, ...meta, y: o.y + (dogru ? 0 : 1), d: o.d + (dogru ? 1 : 0), seri: dogru ? o.seri + 1 : 0, t: Date.now(), son: kaynak };
  const s = v.s[kaynak] || [0, 0];
  v.s[kaynak] = dogru ? [s[0] + 1, s[1]] : [s[0], s[1] + 1];
  const g = gun();
  const gg = v.g[g] || [0, 0];
  v.g[g] = dogru ? [gg[0] + 1, gg[1]] : [gg[0], gg[1] + 1];
  // günlük dizi 60 günle sınırlı
  const gunler = Object.keys(v.g).sort();
  for (const eski of gunler.slice(0, Math.max(0, gunler.length - 60))) delete v.g[eski];
  yaz(kod, v);
}

export function hataSifirla(kod: string) { yaz(kod, bos()); }

export function useHata(kod: string): HataVeri {
  const [v, setV] = useState(() => hataOku(kod));
  useEffect(() => {
    setV(hataOku(kod));
    const f = (e: Event) => { const d = (e as CustomEvent).detail; if (!d || d === kod) setV(hataOku(kod)); };
    const s = (e: StorageEvent) => { if (e.key === anahtar(kod)) setV(hataOku(kod)); };
    window.addEventListener(OLAY, f);
    window.addEventListener('storage', s);
    return () => { window.removeEventListener(OLAY, f); window.removeEventListener('storage', s); };
  }, [kod]);
  return v;
}

export const zayifMi = (k: Kavram) => k.y > 0 && k.seri < 2;
/** Zayıflık puanı: yanlış oranı + yanlış sayısı; yakın zamanda yanlış yapılan öne */
const puan = (k: Kavram) => (k.y / Math.max(1, k.y + k.d)) * 2 + Math.min(k.y, 5) * 0.4 - k.seri * 0.6 + (Date.now() - k.t < 864e5 ? 0.3 : 0);

export function zayiflar(v: HataVeri): (Kavram & { id: string })[] {
  return Object.entries(v.k).filter(([, k]) => zayifMi(k)).map(([id, k]) => ({ id, ...k })).sort((a, b) => puan(b) - puan(a));
}

/** Öğretim adımı → o adıma bağlı zayıf kavram sayısı (Öğren listesinde kırmızı nokta) */
export function zayifAdimlar(v: HataVeri): Record<string, number> {
  const r: Record<string, number> = {};
  for (const k of Object.values(v.k)) if (zayifMi(k) && k.adim) r[k.adim] = (r[k.adim] || 0) + 1;
  return r;
}

export function ozet(v: HataVeri) {
  let d = 0, y = 0;
  for (const [a, b] of Object.values(v.s)) { d += a || 0; y += b || 0; }
  return { deneme: d + y, dogru: d, yanlis: y, oran: d + y ? Math.round((d / (d + y)) * 100) : 0, zayif: zayiflar(v).length, ogrenilen: Object.values(v.k).filter((k) => k.y > 0 && k.seri >= 2).length };
}
