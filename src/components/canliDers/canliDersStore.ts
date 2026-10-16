/**
 * Canlı ders · ses deposu. Uygulamada TEK bir HTMLAudioElement vardır (modül düzeyi): sayfa/rota değişse de çalma
 * sürer, alt oynatıcı (CanliDersDock) ve ders ekranı aynı durumu okur. Media Session ile kilit ekranı / arka sekme
 * denetimleri bağlanır. Ders verisi sözleşmesi: `GET /api/canli-ders`, `GET /api/canli-ders/:key`,
 * ses `GET /api/canli-ders/ses/:key/:vid.mp3` (Range; `?indir=1` indirme).
 *
 * Durum `useCd(seçici)` ile okunur; seçici ilkel değer döndürmeli (her çağrıda yeni nesne → sonsuz çizim).
 * Zaman (t) çalarken her karede güncellenir; paragraf/cümle dizini yalnız değişince değişir (metin listesi yeniden çizilmez).
 */
import { useSyncExternalStore } from 'react';
import { getCustomApiUrl, safeJsonFetch } from '../../services/api';
import { cdCevrimdisiKayitlari, cdCevrimdisiVid } from './canliDersCevrimdisiKayit';

export interface CdVaryant {
  id: string;
  etiket: string;
  saglayici: string;
  ses: string;
  sureSn: number;
  bayt: number;
  zamanlama?: [number, number][] | null;
}
export interface CdListeDers {
  key: string;
  no: string | number;
  baslik: string;
  sira: number;
  varsayilan: CdVaryant;
  varyantlar: CdVaryant[];
  pdf: boolean;
}
export interface CdParagraf { i: number; metin: string }
export interface CdBolum { baslik: string; paragraflar: CdParagraf[] }
export interface CdPdfDosya { path: string; name: string; fileId?: string; pages?: number }
export interface CdPdfEsleme { dosya: number; sayfa: number; guven?: number }
export interface CdPdf { deckId: string; dosyalar: CdPdfDosya[]; paragraflar: (CdPdfEsleme | null)[] }
export interface CdDetay {
  key: string;
  no: string | number;
  baslik: string;
  bolumler: CdBolum[];
  varyantlar: CdVaryant[];
  pdf: CdPdf | null;
}
/** Çalmaya başlamak için en az bu kadarı yeter (liste satırından hızlı oynatma) */
export interface CdOzet { key: string; no: string | number; baslik: string; varyantlar: CdVaryant[] }

export const CD_HIZLAR = [1, 1.25, 1.5, 2, 3, 4] as const;
const HIZ_KEY = 'medsoru_canli_ders_hiz';
const KONUM_KEY = 'medsoru_canli_ders_konum_v1';
const VARYANT_KEY = 'medsoru_canli_ders_ses';

/* ---------------- adresler ---------------- */
const yol = (key: string, vid: string) => `/api/canli-ders/ses/${encodeURIComponent(key)}/${encodeURIComponent(vid)}.mp3`;
/** Ses dosyası sürümü (bayt): dosya yenilenirse (onarım vb.) adres değişir, tarayıcı/oynatıcı eskisini kullanmaz. */
const surumler = new Map<string, number>();
const surumKaydet = (key: string, vs: { id: string; bayt?: number; surum?: number }[] | undefined) =>
  (vs || []).forEach((v) => (v?.surum || v?.bayt) && surumler.set(`${key}/${v.id}`, v.surum || v.bayt!));
export const cdSesUrl = (key: string, vid: string, indir = false) => {
  const p = yol(key, vid);
  const qs = new URLSearchParams();
  const v = surumler.get(`${key}/${vid}`);
  if (v) qs.set('v', String(v));
  if (indir) qs.set('indir', '1');
  const q = qs.toString();
  return `${(getCustomApiUrl(p) || '').replace(/\/$/, '')}${p}${q ? `?${q}` : ''}`;
};
export const cdDosyaAdi = (no: string | number, baslik: string, etiket?: string) =>
  `${String(no).padStart(2, '0')} ${baslik}${etiket ? ` - ${etiket}` : ''}.mp3`.replace(/[\\/:*?"<>|]+/g, ' ').replace(/\s+/g, ' ').trim();

export const fmtSure = (s: number) => {
  if (!Number.isFinite(s) || s < 0) s = 0;
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sn = Math.floor(s % 60);
  return h ? `${h}:${String(m).padStart(2, '0')}:${String(sn).padStart(2, '0')}` : `${m}:${String(sn).padStart(2, '0')}`;
};
/** Kısa ses adı: "Emel · Edge", "Aoede · Gemini" (tam etiket title'da kalır) */
export const cdSesKisa = (v: Pick<CdVaryant, 'etiket' | 'ses' | 'saglayici' | 'id'> | null | undefined) => {
  if (!v) return '';
  const p = v.saglayici || '';
  const kaynak = /edge/i.test(p) ? 'Edge' : /gemini/i.test(p) ? 'Gemini' : /ema/i.test(p) ? 'EMA Lightning' : /xtts/i.test(p) ? 'XTTS' : '';
  const ad = v.ses || (v.etiket || '').split('·').pop()?.trim() || v.id;
  return kaynak ? `${ad} · ${kaynak}` : ad;
};
export const fmtMb = (b: number) => (b > 0 ? `${(b / 1048576).toFixed(b < 10485760 ? 1 : 0)} MB` : '');

/* ---------------- veri ---------------- */
let listeP: Promise<CdListeDers[]> | null = null;
export function cdListeGetir(yenile = false): Promise<CdListeDers[]> {
  if (!listeP || yenile) {
    listeP = safeJsonFetch<{ dersler: CdListeDers[] }>('/api/canli-ders').then((r) => {
      if (!r.ok || !Array.isArray(r.data?.dersler)) {
        listeP = null;
        // İnternet yok: cihaza indirilmiş dersler (canliDersCevrimdisi)
        if (Object.keys(cdCevrimdisiKayitlari()).length) {
          return import('./canliDersCevrimdisi').then((m) => m.cdYerelListe()).then((ds) => {
            if (!ds.length) throw new Error(r.error || `Liste alınamadı (${r.status})`);
            return ds.sort((a, b) => (a.sira ?? 0) - (b.sira ?? 0));
          });
        }
        throw new Error(r.error || `Liste alınamadı (${r.status})`);
      }
      r.data!.dersler.forEach((d) => surumKaydet(d.key, d.varyantlar as any));
      return r.data!.dersler.slice().sort((a, b) => (a.sira ?? 0) - (b.sira ?? 0));
    });
  }
  return listeP;
}
// Ders ayrıntısı (metin + zamanlama + PDF eşlemesi) 3 dk önbellekte: ses yeniden üretilir/onarılırsa zamanlama da tazelenir
const DETAY_OMUR_MS = 3 * 60 * 1000;
const detayCache = new Map<string, { p: Promise<CdDetay>; at: number }>();
export function cdDetayGetir(key: string, yenile = false): Promise<CdDetay> {
  const hit = detayCache.get(key);
  if (hit && !yenile && Date.now() - hit.at < DETAY_OMUR_MS) return hit.p;
  const p = safeJsonFetch<CdDetay>(`/api/canli-ders/${encodeURIComponent(key)}`, { cache: 'no-store' } as RequestInit).then((r) => {
    if (!r.ok || !r.data || !Array.isArray(r.data.bolumler)) {
      detayCache.delete(key);
      if (r.status !== 404 && cdCevrimdisiKayitlari()[key]) {
        return import('./canliDersCevrimdisi').then((m) => m.cdYerelDetay(key)).then((d) => {
          if (!d) throw new Error(r.error || `Ders alınamadı (${r.status})`);
          surumKaydet(key, d.varyantlar as any);
          return d;
        });
      }
      throw new Error(r.status === 404 ? 'Bu ders bulunamadı.' : r.error || `Ders alınamadı (${r.status})`);
    }
    surumKaydet(key, r.data.varyantlar as any);
    return r.data;
  });
  detayCache.set(key, { p, at: Date.now() });
  return p;
}

/* ---------------- durum ---------------- */
export interface CdState {
  key: string | null;
  no: string;
  baslik: string;
  detay: CdDetay | null;
  varyantlar: CdVaryant[];
  vid: string | null;
  playing: boolean;
  t: number;
  dur: number;
  rate: number;
  bekliyor: boolean;
  hata: string | null;
  /** Etkin paragrafın global dizini (i); yoksa -1 */
  aktif: number;
  /** Etkin paragraf içindeki tahmini cümle sırası */
  cumle: number;
  /** Etkin bölüm sırası */
  bolum: number;
  /** Zamanlama sürümü: süre/varyant değişince artar (bölüm işaretleri yeniden hesaplanır) */
  zs: number;
}

const okuHiz = () => {
  try {
    const v = Number(localStorage.getItem(HIZ_KEY));
    return (CD_HIZLAR as readonly number[]).includes(v) ? v : 1;
  } catch {
    return 1;
  }
};

let st: CdState = {
  key: null, no: '', baslik: '', detay: null, varyantlar: [], vid: null,
  playing: false, t: 0, dur: 0, rate: 1, bekliyor: false, hata: null, aktif: -1, cumle: -1, bolum: -1, zs: 0,
};
const subs = new Set<() => void>();
const set = (p: Partial<CdState>) => {
  let ch = false;
  for (const k in p) if ((p as any)[k] !== (st as any)[k]) { ch = true; break; }
  if (!ch) return;
  st = { ...st, ...p };
  subs.forEach((f) => f());
};
const subscribe = (f: () => void) => {
  subs.add(f);
  return () => subs.delete(f);
};
export const cdDurum = () => st;
export const cdAbone = subscribe;
export function useCd<T>(sel: (s: CdState) => T): T {
  return useSyncExternalStore(subscribe, () => sel(st), () => sel(st));
}

/* ---------------- zamanlama ---------------- */
interface ParaBilgi { i: number; len: number; bolum: number; metin: string; cumleler?: number[] }
let paras: ParaBilgi[] = [];
let posByI = new Map<number, number>();
let starts: number[] = [];
let ends: number[] = [];
let bolumBas: number[] = []; // her bölümün ilk paragrafının konumu (paras dizini)

function parasKur(d: CdDetay | null) {
  paras = [];
  bolumBas = [];
  if (d) {
    d.bolumler.forEach((b, bi) => {
      bolumBas.push(paras.length);
      for (const p of b.paragraflar) paras.push({ i: p.i, len: Math.max(1, p.metin.length), bolum: bi, metin: p.metin });
    });
  }
  posByI = new Map(paras.map((p, k) => [p.i, k]));
}

function zamanlamaKur() {
  starts = [];
  ends = [];
  const v = st.varyantlar.find((x) => x.id === st.vid);
  const z = v?.zamanlama;
  if (paras.length && z && z.length) {
    let ok = true;
    for (const p of paras) {
      const r = z[p.i];
      if (!r || !Number.isFinite(r[0])) { ok = false; break; }
      starts.push(r[0]);
      ends.push(Number.isFinite(r[1]) ? r[1] : r[0]);
    }
    if (ok) return void set({ zs: st.zs + 1 });
    starts = [];
    ends = [];
  }
  const dur = st.dur || v?.sureSn || 0;
  if (paras.length && dur > 0) {
    const total = paras.reduce((a, p) => a + p.len, 0);
    let acc = 0;
    for (const p of paras) {
      starts.push((acc / total) * dur);
      acc += p.len;
      ends.push((acc / total) * dur);
    }
  }
  set({ zs: st.zs + 1 });
}

/** Paragrafı cümlelere böler: her cümlenin bitiş karakter konumu */
function cumleSinirlari(p: ParaBilgi): number[] {
  if (p.cumleler) return p.cumleler;
  const out: number[] = [];
  const re = /[^.!?…]+(?:[.!?…]+["'”’)\]]*\s*|$)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(p.metin))) {
    if (!m[0]) { re.lastIndex++; continue; }
    out.push(m.index + m[0].length);
    if (re.lastIndex >= p.metin.length) break;
  }
  if (!out.length || out[out.length - 1] < p.metin.length) out.push(p.metin.length);
  p.cumleler = out;
  return out;
}
/** Etkin cümlenin [başlangıç, bitiş) karakter aralığı */
export function cdCumleAraligi(i: number, cumle: number): [number, number] | null {
  const k = posByI.get(i);
  if (k == null || cumle < 0) return null;
  const s = cumleSinirlari(paras[k]);
  if (cumle >= s.length) return null;
  return [cumle ? s[cumle - 1] : 0, s[cumle]];
}

function konumBul(t: number) {
  if (!starts.length) return { aktif: -1, cumle: -1, bolum: -1 };
  let lo = 0;
  let hi = starts.length - 1;
  let k = 0;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (starts[mid] <= t + 0.05) { k = mid; lo = mid + 1; } else hi = mid - 1;
  }
  const p = paras[k];
  const s = cumleSinirlari(p);
  const span = Math.max(0.001, ends[k] - starts[k]);
  const frac = Math.min(1, Math.max(0, (t - starts[k]) / span));
  const pos = frac * p.len;
  let c = s.findIndex((e) => pos < e);
  if (c < 0) c = s.length - 1;
  return { aktif: p.i, cumle: c, bolum: p.bolum };
}

/** Paragrafın seste başlangıç/bitiş saniyesi */
export const cdAralik = (i: number): [number, number] | null => {
  const k = posByI.get(i);
  return k == null || k >= starts.length ? null : [starts[k], ends[k]];
};
/** Bölüm başlangıç saniyeleri (zs değişince yeniden okunmalı) */
export const cdBolumBaslari = (): number[] => bolumBas.map((k) => (k < starts.length ? starts[k] : NaN)).filter((x) => Number.isFinite(x));

/* ---------------- ses öğesi ---------------- */
/** Ders bitince çağrılır (oynatma listesi / tekrar: canliDersListe.ts kaydeder) */
let bitinceFn: (() => void) | null = null;
export const cdBitinceKaydet = (f: (() => void) | null) => { bitinceFn = f; };
let audio: HTMLAudioElement | null = null;
let raf = 0;
let sonKayit = 0;

function tick() {
  if (!audio) return;
  const t = audio.currentTime || 0;
  set({ t, ...konumBul(t) });
  if (Date.now() - sonKayit > 5000) konumKaydet();
}
function loop() {
  raf = 0;
  tick();
  if (st.playing && document.visibilityState === 'visible') raf = requestAnimationFrame(loop);
}
const loopBaslat = () => { if (!raf && st.playing) raf = requestAnimationFrame(loop); };

function pitch(a: HTMLAudioElement) {
  const x = a as HTMLAudioElement & { mozPreservesPitch?: boolean; webkitPreservesPitch?: boolean };
  x.preservesPitch = true;
  x.mozPreservesPitch = true;
  x.webkitPreservesPitch = true;
}

function ses(): HTMLAudioElement {
  if (audio) return audio;
  const a = new Audio();
  a.preload = 'metadata';
  pitch(a);
  a.addEventListener('play', () => { set({ playing: true, hata: null }); loopBaslat(); msDurum(); });
  a.addEventListener('pause', () => { set({ playing: false }); tick(); konumKaydet(); msDurum(); });
  a.addEventListener('ended', () => { set({ playing: false }); konumKaydet(true); msDurum(); bitinceFn?.(); });
  a.addEventListener('timeupdate', () => { if (!raf) tick(); });
  a.addEventListener('seeked', () => { tick(); msKonum(); });
  a.addEventListener('waiting', () => set({ bekliyor: true }));
  a.addEventListener('playing', () => set({ bekliyor: false }));
  a.addEventListener('canplay', () => set({ bekliyor: false }));
  a.addEventListener('ratechange', () => msKonum());
  const sureAl = () => {
    const d = a.duration;
    if (Number.isFinite(d) && d > 0 && Math.abs(d - st.dur) > 0.5) {
      set({ dur: d });
      zamanlamaKur();
      tick();
      msKonum();
    }
    // Ses dosyası zamanlamadaki süreden belirgin farklıysa (ses yeniden üretildi/onarıldı) ayrıntıyı tazele
    const z = st.detay?.varyantlar.find((v) => v.id === st.vid)?.zamanlama;
    const zSon = z && z.length ? z[z.length - 1][1] : 0;
    if (st.key && Number.isFinite(d) && zSon > 0 && Math.abs(d - zSon) > 3) {
      const key = st.key;
      cdDetayGetir(key, true).then((yeni) => { if (st.key === key) cdDetayBagla(yeni); }).catch(() => {});
    }
  };
  a.addEventListener('loadedmetadata', sureAl);
  a.addEventListener('durationchange', sureAl);
  a.addEventListener('error', () => {
    if (!a.getAttribute('src')) return;
    set({ hata: 'Ses dosyası açılamadı.', playing: false, bekliyor: false });
  });
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') loopBaslat(); });
  window.addEventListener('pagehide', () => konumKaydet());
  audio = a;
  msKur();
  return a;
}

/* ---------------- kaldığın yer ---------------- */
type Konumlar = Record<string, { vid: string; t: number; at: number }>;
const konumlar = (): Konumlar => {
  try {
    return JSON.parse(localStorage.getItem(KONUM_KEY) || '{}') || {};
  } catch {
    return {};
  }
};
function konumKaydet(bitti = false) {
  sonKayit = Date.now();
  if (!st.key || !st.vid || !audio) return;
  try {
    const all = konumlar();
    const t = audio.currentTime || 0;
    if (bitti || t < 5) delete all[st.key];
    else all[st.key] = { vid: st.vid, t, at: Date.now() };
    const keys = Object.keys(all).sort((a, b) => all[b].at - all[a].at).slice(0, 40);
    localStorage.setItem(KONUM_KEY, JSON.stringify(Object.fromEntries(keys.map((k) => [k, all[k]]))));
  } catch {
    /* depolama kapalı */
  }
}
export const cdKayitliKonum = (key: string) => konumlar()[key] || null;
/** Tüm kaldığın yer kayıtları (en yeni önce) */
export const cdKonumListesi = () =>
  Object.entries(konumlar())
    .map(([key, k]) => ({ key, ...k }))
    .sort((a, b) => b.at - a.at);
const tercihVaryant = (vs: CdVaryant[]) => {
  try {
    const want = localStorage.getItem(VARYANT_KEY);
    if (want) {
      const v = vs.find((x) => x.etiket === want || x.id === want);
      if (v) return v.id;
    }
  } catch {
    /* yok */
  }
  return vs[0]?.id ?? null;
};

/* ---------------- eylemler ---------------- */
function kaynakKur(o: CdOzet, vid: string, t0: number, oynat: boolean) {
  const a = ses();
  const v = o.varyantlar.find((x) => x.id === vid);
  const yeniDers = st.key !== o.key;
  if (yeniDers) {
    parasKur(null);
    starts = [];
    ends = [];
  }
  set({
    key: o.key, no: String(o.no), baslik: o.baslik, varyantlar: o.varyantlar, vid,
    detay: yeniDers ? null : st.detay, dur: v?.sureSn || 0, t: t0, hata: null, bekliyor: oynat,
    ...(yeniDers ? { aktif: -1, cumle: -1, bolum: -1 } : {}),
  });
  a.src = cdSesUrl(o.key, vid);
  a.playbackRate = st.rate;
  a.defaultPlaybackRate = st.rate;
  pitch(a);
  if (t0 > 0) {
    const atla = () => { try { a.currentTime = t0; } catch { /* yok */ } };
    if (a.readyState >= 1) atla();
    else a.addEventListener('loadedmetadata', atla, { once: true });
  }
  zamanlamaKur();
  msMeta();
  if (oynat) a.play().catch((e) => { if (e?.name !== 'AbortError') set({ hata: e?.name === 'NotAllowedError' ? 'Oynatmak için düğmeye dokunun.' : 'Ses çalınamadı.', bekliyor: false }); });
  else a.load();
  // Hızlı oynatmada metin/bölümler arkadan gelir
  if (!st.detay || st.detay.key !== o.key) cdDetayGetir(o.key).then((d) => { if (st.key === d.key) cdDetayBagla(d); }).catch(() => {});
}

/** Dersi/varyantı çal. Aynı ders ve varyant ise yalnız oynat/duraklat. Kullanıcı hareketi içinde çağrılmalı. */
export function cdOynat(o: CdOzet, vid?: string, opts: { t?: number; oynat?: boolean } = {}) {
  const oynat = opts.oynat ?? true;
  // İnternet yokken cihaza indirilen seslerden biri çalınır (indirilmemiş ses açılamaz)
  const kendi = vid || (st.key === o.key && st.vid ? st.vid : tercihVaryant(o.varyantlar));
  const v = cdCevrimdisiVid(o.key, [vid, st.key === o.key ? st.vid : null, kendi]) || kendi;
  if (!v) return;
  if (st.key === o.key && st.vid === v && audio?.getAttribute('src')) {
    if (opts.t != null) cdAtla(opts.t);
    if (oynat) audio.play().catch(() => {});
    return;
  }
  let t0 = opts.t ?? 0;
  if (opts.t == null) {
    const k = cdKayitliKonum(o.key);
    if (k && k.vid === v) t0 = k.t;
  }
  kaynakKur(o, v, t0, oynat);
}

/** Ders ekranı açılınca: aynı ders yüklüyse metni bağlar; başka bir şey çalmıyorsa dersi (oynatmadan) yükler. */
export function cdDetayBagla(d: CdDetay): 'bagli' | 'yuklendi' | 'baska' {
  if (st.key === d.key) {
    if (st.detay !== d) {
      parasKur(d);
      set({ detay: d, varyantlar: d.varyantlar.length ? d.varyantlar : st.varyantlar });
      zamanlamaKur();
      tick();
    }
    return 'bagli';
  }
  if (st.key && st.playing) return 'baska';
  cdOynat(d, undefined, { oynat: false });
  parasKur(d);
  set({ detay: d });
  zamanlamaKur();
  tick();
  return 'yuklendi';
}

export function cdToggle() {
  const a = audio;
  if (!a || !st.key) return;
  if (a.paused) a.play().catch((e) => { if (e?.name !== 'AbortError') set({ hata: 'Ses çalınamadı.' }); });
  else a.pause();
}
export function cdDuraklat() { audio?.pause(); }
export function cdAtla(t: number) {
  const a = audio;
  if (!a || !st.key) return;
  const max = st.dur || a.duration || 0;
  const v = Math.max(0, max ? Math.min(max - 0.1, t) : t);
  try {
    a.currentTime = v;
  } catch { /* henüz yüklenmedi */ }
  set({ t: v, ...konumBul(v) });
}
export const cdSar = (d: number) => cdAtla((audio?.currentTime || st.t) + d);
export function cdHiz(r: number) {
  set({ rate: r });
  try { localStorage.setItem(HIZ_KEY, String(r)); } catch { /* yok */ }
  if (audio) {
    audio.playbackRate = r;
    audio.defaultPlaybackRate = r;
    pitch(audio);
  }
}
export function cdHizDongu() {
  const i = (CD_HIZLAR as readonly number[]).indexOf(st.rate);
  cdHiz(CD_HIZLAR[(i + 1) % CD_HIZLAR.length]);
}
/** Varyant değişince aynı paragrafın aynı oranına geçilir (zamanlama yoksa süre oranı) */
export function cdVaryant(vid: string) {
  if (!st.key || vid === st.vid) return;
  const v = st.varyantlar.find((x) => x.id === vid);
  if (!v) return;
  try { localStorage.setItem(VARYANT_KEY, v.etiket || v.id); } catch { /* yok */ }
  const t = audio?.currentTime || st.t;
  let t0 = st.dur ? (t / st.dur) * (v.sureSn || st.dur) : 0;
  const k = posByI.get(st.aktif);
  if (k != null && starts.length) {
    const frac = Math.min(1, Math.max(0, (t - starts[k]) / Math.max(0.001, ends[k] - starts[k])));
    const z = v.zamanlama?.[st.aktif];
    if (z) t0 = z[0] + frac * (z[1] - z[0]);
  }
  const playing = st.playing;
  kaynakKur({ key: st.key, no: st.no, baslik: st.baslik, varyantlar: st.varyantlar }, vid, t0, playing);
}
/** Önceki/sonraki bölüm. Öncekide bölümün ilk 3 sn'sinden sonraysa aynı bölümün başına döner. */
export function cdBolumAtla(yon: 1 | -1) {
  const b = cdBolumBaslari();
  if (!b.length) return cdSar(yon * 30);
  const t = audio?.currentTime || st.t;
  let cur = 0;
  for (let k = 0; k < b.length; k++) if (b[k] <= t + 0.05) cur = k;
  if (yon > 0) { if (cur + 1 < b.length) cdAtla(b[cur + 1]); return; }
  cdAtla(t - b[cur] > 3 || cur === 0 ? b[cur] : b[cur - 1]);
}
export function cdParagrafa(i: number, oynat = true) {
  const r = cdAralik(i);
  if (!r) return;
  cdAtla(r[0]);
  if (oynat && audio?.paused) audio.play().catch(() => {});
}
export function cdKapat() {
  konumKaydet();
  if (audio) {
    audio.pause();
    audio.removeAttribute('src');
    audio.load();
  }
  if (raf) cancelAnimationFrame(raf);
  raf = 0;
  parasKur(null);
  starts = [];
  ends = [];
  set({ key: null, detay: null, vid: null, varyantlar: [], playing: false, t: 0, dur: 0, aktif: -1, cumle: -1, bolum: -1, hata: null, bekliyor: false });
  if ('mediaSession' in navigator) {
    try {
      navigator.mediaSession.metadata = null;
      navigator.mediaSession.playbackState = 'none';
    } catch { /* yok */ }
  }
}

/* ---------------- Media Session ---------------- */
function msKur() {
  if (!('mediaSession' in navigator)) return;
  const ms = navigator.mediaSession;
  const h = (a: MediaSessionAction, f: MediaSessionActionHandler) => {
    try { ms.setActionHandler(a, f); } catch { /* desteklenmiyor */ }
  };
  h('play', () => { audio?.play().catch(() => {}); });
  h('pause', () => audio?.pause());
  h('stop', () => audio?.pause());
  h('seekbackward', (d) => cdSar(-(d.seekOffset || 10)));
  h('seekforward', (d) => cdSar(d.seekOffset || 10));
  h('seekto', (d) => { if (d.seekTime != null) cdAtla(d.seekTime); });
  h('previoustrack', () => cdBolumAtla(-1));
  h('nexttrack', () => cdBolumAtla(1));
}
function msMeta() {
  if (!('mediaSession' in navigator) || typeof MediaMetadata === 'undefined') return;
  const v = st.varyantlar.find((x) => x.id === st.vid);
  try {
    navigator.mediaSession.metadata = new MediaMetadata({
      title: `${st.no ? `${st.no}. ` : ''}${st.baslik}`,
      artist: 'MeDSor',
      album: `Canlı ders${v?.etiket ? ` · ${v.etiket}` : ''}`,
      artwork: [
        { src: '/icons/icon-192x192.png?v=9', sizes: '192x192', type: 'image/png' },
        { src: '/icons/icon-512x512.png?v=9', sizes: '512x512', type: 'image/png' },
      ],
    });
  } catch { /* yok */ }
}
function msDurum() {
  if (!('mediaSession' in navigator)) return;
  try { navigator.mediaSession.playbackState = st.playing ? 'playing' : 'paused'; } catch { /* yok */ }
  msKonum();
}
function msKonum() {
  if (!('mediaSession' in navigator) || !audio) return;
  const d = audio.duration;
  if (!Number.isFinite(d) || d <= 0) return;
  try {
    navigator.mediaSession.setPositionState({ duration: d, playbackRate: audio.playbackRate || 1, position: Math.min(d, audio.currentTime || 0) });
  } catch { /* yok */ }
}

// Hız tercihi açılışta okunur (ses öğesi ilk çalmada kurulur)
st = { ...st, rate: okuHiz() };
