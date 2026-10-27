/**
 * Erişilebilirlik tercihleri (Profil › Erişilebilirlik). Cihazda tutulur (`medsoru_erisilebilirlik`), kök öğeye
 * data-* olarak yazılır; açılışta index.html'deki erken betik de aynı anahtarı okur (yanıp sönme olmasın).
 * CSS: styles/erisilebilirlik.css. Yazı boyutu ayrı değil: Görünüm › yazı/yakınlaştırma ayarı zaten var.
 */
import { useSyncExternalStore } from 'react';

export interface Erisim {
  /** hareketi azalt: geçiş/animasyon kapalı (sistem tercihi "azalt" ise kendiliğinden) */
  hareket: 'sistem' | 'azalt' | 'normal';
  /** yüksek kontrast: soluk yazı ve çizgiler koyulaşır */
  kontrast: boolean;
  /** bağlantıların altı çizili */
  altCizgi: boolean;
  /** odak halkası her zaman kalın ve belirgin */
  odak: boolean;
  /** okuma kolaylığı: satır ve harf aralığı geniş */
  aralik: boolean;
}
const KEY = 'medsoru_erisilebilirlik';
const OLAY = 'medsoru:erisilebilirlik';
const VARSAYILAN: Erisim = { hareket: 'sistem', kontrast: false, altCizgi: false, odak: false, aralik: false };

let ham: string | null = null;
let onb: Erisim = VARSAYILAN;
export function erisimOku(): Erisim {
  let h: string | null = null;
  try { h = localStorage.getItem(KEY); } catch { /* yok */ }
  if (h !== ham) { ham = h; try { onb = { ...VARSAYILAN, ...(h ? JSON.parse(h) : {}) }; } catch { onb = VARSAYILAN; } }
  return onb;
}
export function erisimUygula(e: Erisim = erisimOku()) {
  const d = document.documentElement.dataset;
  const set = (k: string, v: boolean) => { if (v) d[k] = 'on'; else delete d[k]; };
  set('azHareket', e.hareket === 'azalt');
  set('normalHareket', e.hareket === 'normal');
  set('yuksekKontrast', e.kontrast);
  set('altCizgi', e.altCizgi);
  set('belirginOdak', e.odak);
  set('genisAralik', e.aralik);
}
export function erisimYaz(y: Partial<Erisim>) {
  const e = { ...erisimOku(), ...y };
  try { localStorage.setItem(KEY, JSON.stringify(e)); } catch { /* yok */ }
  erisimUygula(e);
  window.dispatchEvent(new Event(OLAY));
}
const abone = (f: () => void) => { window.addEventListener(OLAY, f); window.addEventListener('storage', f); return () => { window.removeEventListener(OLAY, f); window.removeEventListener('storage', f); }; };
export const useErisim = () => useSyncExternalStore(abone, erisimOku, erisimOku);
