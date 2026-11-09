/**
 * Taş Masası ortak istemci yardımcıları: cihaz tercihleri (2B/3B, ses, titreşim), sentez ses efektleri (dosya yok, WebAudio)
 * ve küçük okuma yardımcıları. Masa bileşenleri (okey/, uno/) ve kabuk (MasaView) buradan paylaşır.
 */
import { useSyncExternalStore } from 'react';
import type { OdaGorunum } from '../../services/masa/tipler';

export interface MasaTercih { boyut: '2b' | '3b'; ses: boolean; titresim: boolean; ipucu: boolean }
const KEY = 'medsoru_masa_tercih_v1';
const VARSAYILAN: MasaTercih = { boyut: '2b', ses: true, titresim: true, ipucu: true };
let tercih: MasaTercih = (() => { try { return { ...VARSAYILAN, ...JSON.parse(localStorage.getItem(KEY) || '{}') }; } catch { return VARSAYILAN; } })();
const aboneler = new Set<() => void>();
export function tercihYaz(p: Partial<MasaTercih>) {
  tercih = { ...tercih, ...p };
  try { localStorage.setItem(KEY, JSON.stringify(tercih)); } catch { /* yok */ }
  aboneler.forEach((f) => f());
}
export const tercihOku = () => tercih;
export function useTercih(): MasaTercih {
  return useSyncExternalStore((f) => { aboneler.add(f); return () => { aboneler.delete(f); }; }, tercihOku, tercihOku);
}

export const azHareket = () => { try { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch { return false; } };

/* ---------------- ses ---------------- */
export type SesAd = 'tas' | 'birak' | 'cek' | 'ac' | 'isle' | 'sira' | 'ceza' | 'kazan' | 'kaybet' | 'uno' | 'dagit' | 'hata' | 'tepki';
let ctx: AudioContext | null = null;
const nota = (f: number, bas: number, sure: number, tur: OscillatorType = 'sine', siddet = 0.12) => {
  if (!ctx) return;
  const o = ctx.createOscillator(), g = ctx.createGain(), t = ctx.currentTime + bas;
  o.type = tur; o.frequency.setValueAtTime(f, t);
  g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(siddet, t + 0.008); g.gain.exponentialRampToValueAtTime(0.0001, t + sure);
  o.connect(g).connect(ctx.destination); o.start(t); o.stop(t + sure + 0.02);
};
/** Taş tıkırtısı: kısa süzülmüş gürültü */
const tik = (bas: number, f = 2200, siddet = 0.25) => {
  if (!ctx) return;
  const n = Math.floor(ctx.sampleRate * 0.05), buf = ctx.createBuffer(1, n, ctx.sampleRate), d = buf.getChannelData(0);
  for (let i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / n) ** 3;
  const s = ctx.createBufferSource(), fl = ctx.createBiquadFilter(), g = ctx.createGain();
  s.buffer = buf; fl.type = 'bandpass'; fl.frequency.value = f; fl.Q.value = 1.2; g.gain.value = siddet;
  s.connect(fl).connect(g).connect(ctx.destination); s.start(ctx.currentTime + bas);
};
const CALGI: Record<SesAd, () => void> = {
  tas: () => tik(0, 2600, 0.18),
  birak: () => { tik(0, 1700, 0.3); tik(0.035, 1200, 0.12); },
  cek: () => { tik(0, 2000, 0.2); nota(520, 0.02, 0.09, 'triangle', 0.05); },
  ac: () => { [0, 0.06, 0.12].forEach((b) => tik(b, 1800, 0.28)); nota(660, 0.1, 0.18, 'triangle', 0.07); },
  isle: () => { tik(0, 1900, 0.3); nota(740, 0.03, 0.12, 'triangle', 0.06); },
  sira: () => { nota(660, 0, 0.12, 'sine', 0.09); nota(880, 0.11, 0.2, 'sine', 0.09); },
  ceza: () => { nota(220, 0, 0.22, 'sawtooth', 0.09); nota(165, 0.18, 0.35, 'sawtooth', 0.09); },
  kazan: () => [523, 659, 784, 1047].forEach((f, i) => nota(f, i * 0.11, 0.3, 'triangle', 0.11)),
  kaybet: () => [392, 330, 262].forEach((f, i) => nota(f, i * 0.17, 0.36, 'sine', 0.1)),
  uno: () => { nota(784, 0, 0.1, 'square', 0.07); nota(1175, 0.09, 0.22, 'square', 0.07); },
  dagit: () => [0, 0.07, 0.14, 0.21, 0.28].forEach((b) => tik(b, 2100, 0.16)),
  hata: () => nota(196, 0, 0.16, 'square', 0.06),
  tepki: () => nota(988, 0, 0.1, 'sine', 0.06),
};
/** İlk kullanıcı dokunuşundan sonra çalışır (tarayıcı kuralı); tercih kapalıysa sessiz */
export function sesCal(ad: SesAd) {
  if (!tercih.ses) return;
  try {
    ctx ||= new (window.AudioContext || (window as any).webkitAudioContext)();
    if (ctx.state === 'suspended') void ctx.resume();
    CALGI[ad]();
  } catch { /* ses yoksa oyun sürer */ }
}
export function titret(ms: number | number[] = 12) {
  if (!tercih.titresim) return;
  try { navigator.vibrate?.(ms); } catch { /* yok */ }
}

/* ---------------- okuma yardımcıları ---------------- */
export const oyuncuAdi = (oda: OdaGorunum, id: string | undefined | null) => (id && oda.oyuncular.find((o) => o.id === id)?.ad) || 'Oyuncu';
/** Oturma düzeni: bakan en altta, diğerleri saat yönünde (dizinin geri kalanı sırayla) */
export function benOnde<T extends { id: string }>(oyuncular: T[], ben: string): T[] {
  const i = oyuncular.findIndex((o) => o.id === ben);
  return i <= 0 ? oyuncular : [...oyuncular.slice(i), ...oyuncular.slice(0, i)];
}
