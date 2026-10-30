/**
 * Canlı ders · ses deposu. Uygulamada TEK bir HTMLAudioElement vardır (modül düzeyi): sayfa/rota değişse de çalma
 * sürer, alt oynatıcı (CanliDersDock) ve ders ekranı aynı durumu okur. Media Session ile kilit ekranı / arka sekme
 * denetimleri bağlanır. Ders verisi sözleşmesi: `GET /api/canli-ders`, `GET /api/canli-ders/:key`,
 * ses `GET /api/canli-ders/ses/:key/:vid.mp3` (Range; `?indir=1` indirme).
 *
 * Durum `useCd(seçici)` ile okunur; seçici ilkel değer döndürmeli (her çağrıda yeni nesne → sonsuz çizim).
 * Zaman (t) çalarken her karede güncellenir; paragraf/cümle dizini yalnız değişince değişir (metin listesi yeniden çizilmez).
 */
import { ekranUyanik } from '../../services/ekranUyanik';
import { ekranYazimiEslemeli } from '../../services/ekranYazim';
import { useSyncExternalStore } from 'react';
import { getCustomApiUrl, safeJsonFetch } from '../../services/api';
import { cdCevrimdisiKayitlari, cdCevrimdisiVid } from './canliDersCevrimdisiKayit';
import { cdDersEtiketi } from './canliDersKategori';
import { bitir as konuBitir, sureEkle } from '../../services/calismaTakip';

/** Bir PDF sayfasındaki öğrenci notu işaretleri (sayfa oranı 0–1) */
export interface PdfNot { l: number[][]; y?: number[]; b?: number[][] }

export interface CdVaryant {
  id: string;
  etiket: string;
  saglayici: string;
  ses: string;
  sureSn: number;
  bayt: number;
  zamanlama?: [number, number][] | null;
  /** Paragraf → 2., 3., … cümlenin seste başladığı saniye (sesteki duraklamalardan ölçülü; yoksa karakter oranı) */
  cumleZaman?: Record<string, number[]> | null;
  /** cümle başına sesteki konuşma parçaları [a1, b1, a2, b2, …] sn (cumle_zaman.py surum 2) */
  cumleKonusma?: Record<string, number[][]> | null;
  /** Paragraf → her kelimenin (/\S+/g) seste başladığı saniye (kelime_zaman.py: konuşma tanıma + harf hizalama) */
  kelimeZaman?: Record<string, number[]> | null;
  /** Metin sürümü adı (v1, v2…; sunucu kayit.json `surumAd`) — aynı sesin eski/yeni metin seslendirmesini ayırır */
  surumAd?: string;
}
export interface CdListeDers {
  key: string;
  /** V1 satırında: aynı dersin sonraki sürümleri (…-v2, …-v3); listede ayrı satır olmaz, satırdaki seçiciden açılır */
  surumlar?: string[];
  donem?: '2025-2026' | '2026-2027';
  arsiv?: boolean;
  /** Sınama (test) verisi: güncel derslerle aynı listede gösterilmez (data/sinama.json) */
  sinama?: boolean;
  sinamaEtiket?: string;
  desteId?: string;
  gunlukVar?: boolean;
  medspakVar?: boolean;
  medspakBayt?: number;
  medspakSurum?: string;
  /** Branş içi numara (Tıbbi Patoloji 16); eski sunucu/çevrimdışı kayıtta kurul sırası olabilir */
  no: string | number;
  /** Ders (branş) adı: "Tıbbi Patoloji"; kurulNo: kurul genelindeki sıra */
  brans?: string;
  hoca?: string;
  /** Aynı PDF iki derste anlatıldıysa 1/2 ("Part 1") */
  parca?: number;
  /** Listede sıralama numarası no'dan farklıysa (no çözücü numarasıdır; Meme Kanseri 35 ama listede 34,5) */
  listeNo?: number;
  kurul?: number;
  kurulNo?: number;
  baslik: string;
  sira: number;
  varsayilan: CdVaryant;
  varyantlar: CdVaryant[];
  pdf: boolean;
}
export interface CdGunlukKayit {
  surum: number;
  tarih: string;
  neden: string;
  hatali_bilgiler: string[];
  degisiklikler: string[];
  metrikler?: {
    sureSn?: number;
    sureDk?: number;
    sayfaSayisi?: number;
    atlananSayfa?: number;
    bolumSayisi?: number;
    paragrafSayisi?: number;
    cumleSayisi?: number;
    slaytAdimSayisi?: number;
    cizimSayisi?: number;
    cikmisEslesme?: number;
  };
}
export interface CdGunluk {
  key: string;
  donem: string;
  kurul: number;
  brans: string;
  baslik: string;
  kayitlar: CdGunlukKayit[];
}
export interface CdParagraf { i: number; metin: string }
export interface CdBolum { baslik: string; paragraflar: CdParagraf[] }
export interface CdPdfDosya { path: string; name: string; fileId?: string; pages?: number }
export interface CdPdfEsleme { dosya: number; sayfa: number; guven?: number; sayfalar?: number[]; dosyalar?: number[] }
export interface CdPdf {
  deckId: string; dosyalar: CdPdfDosya[]; paragraflar: (CdPdfEsleme | null)[];
  /** Özet (kırpılmış) PDF'te sayfa (i+1) → asıl ders ve slayt (Son Prova) */
  sayfaKaynak?: { kod: string; no: string; ad: string; s: number }[];
}
export interface CdDetay {
  key: string;
  donem?: '2025-2026' | '2026-2027';
  arsiv?: boolean;
  sinama?: boolean;
  sinamaEtiket?: string;
  desteId?: string;
  gunlukVar?: boolean;
  medspakVar?: boolean;
  medspakBayt?: number;
  medspakSurum?: string;
  no: string | number;
  brans?: string;
  hoca?: string;
  parca?: number;
  kurul?: number;
  kurulNo?: number;
  sira?: number;
  baslik: string;
  bolumler: CdBolum[];
  varyantlar: CdVaryant[];
  pdf: CdPdf | null;
  /** önemli cümle (c) ve anahtar terim (t) aralıkları, paragraf dizinine göre: [baş, son, tür, önem 1–3] */
  vurgu?: Record<string, [number, number, "c" | "t", number][]> | null;
  /** okunan cümlenin slayttaki karşılığı, paragraf dizini → cümle başına (pdf_isaret.py) */
  isaret?: Record<string, (CdIsaret | null)[]> | null;
  /** öğrenci notunda işaretli yerler: dosya dizini → sayfa → kırmızı marker kutuları + yıldız */
  ogrenciNot?: Record<string, Record<string, PdfNot>> | null;
  /** çıkmış sorular ve dayandıkları cümle (paragraf p, cümle c); PDF yeri isaret[p][c]'den */
  cikmisKonum?: CdCikmisKonum[] | null;
  /** Kurul 2+ sesli metin v2: paragraf dizini → cümle başına ekran maddesi (e), düzey (d), vurgu [metin, tür] (v),
   *  çıkmış kimlikleri (c), Öğren destesinde slayt adımı (a); deste = Öğren deste kimliği */
  v2?: { deste: string; p: Record<string, CdV2Cumle[]> } | null;
  /** PDF terim yardımcısı: dosya dizini → sayfa → { alt boş oran, terimler } (terim_sozlugu.py) */
  terim?: Record<string, Record<string, CdTerimSayfa>> | null;
  /** PDF kısaltma yardımcısı (ayrı katman): dosya dizini → sayfa → { alt boş oran, kısaltmalar } (kisaltma_sozlugu.py) */
  kisaltma?: Record<string, Record<string, CdTerimSayfa>> | null;
}
/** k: terim | latince | karisan | kisaltma; f: karıştırılan terim; acilim: kısaltmanın açılımı; b: slayttaki kutular */
export interface CdTerim { t: string; a: string; k: 'terim' | 'latince' | 'karisan' | 'kisaltma'; f?: string; acilim?: string; b: number[][] }
export interface CdTerimSayfa { bos: number; t: CdTerim[] }
/** o: geçmiş yıl öğrenci notunda önem (A: çıkmış kanıtlı, B: vurgulu + el notlu) */
export interface CdV2Cumle { e: string; d: number; v: [string, string][]; c: string[]; a: number | null; s?: unknown; o?: 'A' | 'B' | null }
/** s/d: elle doğrulanmış slayt (PDF sayfası) ve dosya; dogrulandi olanlar slaytta yanıp sönen chip olarak gösterilir.
 *  seviye: dogrudan (slayttaki bilgi doğrudan soruldu) | ilgili; kanit: slayttan birebir dayanak */
export interface CdCikmisKonum { id: string; kok: string; cevap: string; yil?: number | string | null; p: number; c: number; skor: number;
  s?: number; d?: number; seviye?: 'dogrudan' | 'ilgili'; kanit?: string; dogrulandi?: boolean;
  /** Ham sınav belgesindeki yeri (doğrulama kanıtı; pencerede gösterilir) */
  kaynak?: string }
/** Kutular sayfa oranıdır (0–1). l: ≥%80'i okunan madde satırları (ya da resim); w: [kelimenin cümle içi baş, son, x0, y0, x1, y1] */
/** y: hareketli imleç yolu [[cümle içi karakter, x, y]] — ses o karaktere gelince imleç (x, y)'ye kayar */
export interface CdIsaret { d: number; s: number; t: 'metin' | 'tablo' | 'kelime' | 'resim' | 'sayfa'; l: number[][]; w: number[][]; y?: number[][] }
/** Çalmaya başlamak için en az bu kadarı yeter (liste satırından hızlı oynatma) */
export interface CdOzet { key: string; no: string | number; brans?: string; parca?: number; baslik: string; varyantlar: CdVaryant[] }

export const CD_HIZLAR = [
  0.75, 0.875, 1, 1.125, 1.25, 1.375, 1.5, 1.625, 1.75, 1.875, 2, 2.125, 2.25, 2.375, 2.5, 2.625, 2.75, 2.875, 3,
] as const;
const HIZ_KEY = 'medsoru_canli_ders_hiz';
const KONUM_KEY = 'medsoru_canli_ders_konum_v1';

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
export const cdSesKisa = (v: (Pick<CdVaryant, 'etiket' | 'ses' | 'saglayici' | 'id'> & { surumAd?: string }) | null | undefined) => {
  if (!v) return '';
  const p = v.saglayici || '';
  const kaynak = /edge/i.test(p) ? 'Edge' : /gemini/i.test(p) ? 'Gemini' : /ema/i.test(p) ? 'EMA Lightning' : /xtts/i.test(p) ? 'XTTS' : '';
  const ad = v.ses || (v.etiket || '').split('·').pop()?.trim() || v.id;
  const temel = kaynak ? `${ad} · ${kaynak}` : ad;
  return v.surumAd ? `${temel} · ${v.surumAd}` : temel;
};
export const fmtMb = (b: number) => (b > 0 ? `${(b / 1048576).toFixed(b < 10485760 ? 1 : 0)} MB` : '');

/* ---------------- veri ---------------- */
const listeCache = new Map<string, Promise<CdListeDers[]>>();
export function cdListeGetir(yenile = false, donem: '2026-2027' | '2025-2026' | 'sinama' = '2026-2027'): Promise<CdListeDers[]> {
  if (!listeCache.has(donem) || yenile) {
    const url = donem === '2025-2026' ? '/api/canli-ders?donem=2025-2026' : donem === 'sinama' ? '/api/canli-ders?donem=sinama' : '/api/canli-ders';
    const getir = (taze: boolean) => safeJsonFetch<{ dersler: CdListeDers[] }>(url, taze ? ({ cache: 'no-store' } as RequestInit) : undefined);
    const p = getir(yenile).then((r) => (r.ok && Array.isArray(r.data?.dersler) && !r.data!.dersler.length ? getir(true) : r)).then((r) => {
      if (r.ok && Array.isArray(r.data?.dersler) && !r.data!.dersler.length) listeCache.delete(donem);
      if (!r.ok || !Array.isArray(r.data?.dersler)) {
        listeCache.delete(donem);
        // İnternet yok: cihaza indirilmiş dersler (canliDersCevrimdisi)
        if (donem === '2026-2027' && Object.keys(cdCevrimdisiKayitlari()).length) {
          return import('./canliDersCevrimdisi').then((m) => m.cdYerelListe()).then((ds) => {
            if (!ds.length) throw new Error(r.error || `Liste alınamadı (${r.status})`);
            return ds.sort((a, b) => (a.sira ?? 0) - (b.sira ?? 0));
          });
        }
        throw new Error(r.error || `Liste alınamadı (${r.status})`);
      }
      r.data!.dersler.forEach((d) => surumKaydet(d.key, d.varyantlar as any));
      return r.data!.dersler.slice().sort((a, b) => (a.kurul || 1) - (b.kurul || 1) || (a.sira ?? 0) - (b.sira ?? 0));
    });
    listeCache.set(donem, p);
  }
  return listeCache.get(donem)!;
}

export async function cdGunlukGetir(key: string): Promise<CdGunluk> {
  const r = await safeJsonFetch<CdGunluk>(`/api/canli-ders/${encodeURIComponent(key)}/gunluk`, { cache: 'no-store' } as RequestInit);
  if (!r.ok || !r.data) throw new Error(r.error || 'Güncelleme günlüğü alınamadı.');
  return r.data;
}

export const cdMedspakUrl = (key: string) => {
  const p = `/api/canli-ders/${encodeURIComponent(key)}/medspak`;
  return `${(getCustomApiUrl(p) || '').replace(/\/$/, '')}${p}`;
};
// Ders ayrıntısı (metin + zamanlama + PDF eşlemesi) 3 dk önbellekte: ses yeniden üretilir/onarılırsa zamanlama da tazelenir
const DETAY_OMUR_MS = 3 * 60 * 1000;
/** Okunuşla yazılmış sayı, sıra sayısı, kısaltma ve açılımları ekranda yazılı biçimiyle gösterir (ekranYazim.ts); önemli cümle /
 *  terim aralıkları yeni metne taşınır. Cümle sınırları değişmez (dönüşüm nokta eklemez/silmez), ses senkronu korunur. */
function sayilariDuzelt(d: CdDetay): CdDetay {
  for (const b of d.bolumler) {
    for (const p of b.paragraflar) {
      const r = ekranYazimiEslemeli(p.metin);
      if (r.metin === p.metin) continue;
      // PDF işaretinin kelime konumları cümle başına göredir: eski metindeki mutlak konum üzerinden yeni metne taşınır
      const is = d.isaret?.[String(p.i)];
      if (is) {
        const sinir = cumleSinirlari({ i: p.i, len: p.metin.length, bolum: 0, metin: p.metin });
        is.forEach((x, ci) => {
          if (!x) return;
          const b0 = ci ? sinir[ci - 1] : 0;
          const y0 = r.konum(b0);
          x.w = x.w.map(([b, e, ...k]) => [r.konum(b0 + b) - y0, r.konum(b0 + e, true) - y0, ...k]);
          // hareketli imleç yolu da cümle içi karakter konumuyla: yeni metne taşınır
          if (x.y) x.y = x.y.map(([c, ...k]) => [r.konum(b0 + c) - y0, ...k]);
        });
      }
      // Ölçülü kelime zamanı eski metnin kelimelerine göredir ("yirmi dört" iki kelime, "24" bir): yeni metnin her
      // kelimesine, içine düşen ilk eski kelimenin başlangıcı verilir. Taşınmazsa sayılı paragrafta takip tahmine düşer.
      const eski = [...p.metin.matchAll(/\S+/g)].map((m) => r.konum(m.index!));
      const yeni = [...r.metin.matchAll(/\S+/g)].map((m) => m.index!);
      for (const va of d.varyantlar || []) {
        const kz = va.kelimeZaman?.[String(p.i)];
        if (!Array.isArray(kz) || kz.length !== eski.length) continue;
        const out: number[] = [];
        let w = 0;
        for (let j = 0; j < yeni.length; j++) {
          const son = j + 1 < yeni.length ? yeni[j + 1] : Infinity;
          while (w < eski.length && eski[w] < yeni[j]) w++;
          out.push(w < eski.length && eski[w] < son ? kz[w] : out.length ? out[out.length - 1] : kz[0]);
        }
        va.kelimeZaman![String(p.i)] = out;
      }
      p.metin = r.metin;
      const v = d.vurgu?.[p.i];
      if (v) d.vurgu![p.i] = v.map(([bas, son, tur, onem]) => [r.konum(bas), r.konum(son, true), tur, onem]);
    }
  }
  return d;
}

const detayCache = new Map<string, { p: Promise<CdDetay>; at: number }>();
export function cdDetayGetir(key: string, yenile = false): Promise<CdDetay> {
  const hit = detayCache.get(key);
  if (hit && !yenile && Date.now() - hit.at < DETAY_OMUR_MS) return hit.p;
  const p = safeJsonFetch<CdDetay>(`/api/canli-ders/${encodeURIComponent(key)}`, { cache: 'no-store' } as RequestInit).then((r) => {
    if (!r.ok || !r.data || !Array.isArray(r.data.bolumler)) {
      detayCache.delete(key);
      // 403 = yönetici içeriği kapattı (icerikKapali): cihazdaki kopyaya düşülmez
      if (r.status !== 404 && r.status !== 403 && cdCevrimdisiKayitlari()[key]) {
        return import('./canliDersCevrimdisi').then((m) => m.cdYerelDetay(key)).then((d) => {
          if (!d) throw new Error(r.error || `Ders alınamadı (${r.status})`);
          surumKaydet(key, d.varyantlar as any);
          return sayilariDuzelt(d);
        });
      }
      throw new Error(r.status === 404 ? 'Bu ders bulunamadı.' : r.error || `Ders alınamadı (${r.status})`);
    }
    surumKaydet(key, r.data.varyantlar as any);
    return sayilariDuzelt(r.data);
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
let cumleBas: (number[] | null)[] = []; // paras dizini → ölçülü cümle başlangıçları
let konusma: (number[][] | null)[] = []; // paras dizini → cümle başına konuşma parçaları
let kelimeT: (number[] | null)[] = []; // paras dizini → ölçülü kelime başlangıçları (saniye)
let kelimeC: (number[] | null)[] = []; // paras dizini → kelimelerin paragraf içi karakter başlangıçları

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
  cumleBas = [];
  konusma = [];
  kelimeT = [];
  kelimeC = [];
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
    if (ok) {
      const cz = v?.cumleZaman;
      cumleBas = paras.map((p) => {
        const t = cz?.[String(p.i)];
        // Cümle sayısı istemcideki bölmeyle tutmuyorsa (metin değişti) tahmine dön
        return Array.isArray(t) && t.length === cumleSinirlari(p).length - 1 ? t : null;
      });
      const ck = v?.cumleKonusma;
      konusma = paras.map((p, k) => {
        const x = ck?.[String(p.i)];
        return cumleBas[k] && Array.isArray(x) && x.length === cumleSinirlari(p).length ? x : null;
      });
      // Ölçülü kelime zamanı: kelime sayısı istemcideki bölmeyle tutuyorsa kullanılır; cümle başları da ondan türer
      // (cümlenin ilk kelimesinin sesteki başı) — metin, slayt işareti ve cümle geçişi tek ölçümden yürür.
      const kz = v?.kelimeZaman;
      paras.forEach((p, k) => {
        const t = kz?.[String(p.i)];
        const c = [...p.metin.matchAll(/\S+/g)].map((m) => m.index!);
        if (!Array.isArray(t) || t.length !== c.length || !c.length) { kelimeT.push(null); kelimeC.push(null); return; }
        kelimeT.push(t);
        kelimeC.push(c);
        const sinir = cumleSinirlari(p);
        const cb: number[] = [];
        let w = 0;
        for (let q = 0; q + 1 < sinir.length; q++) {
          while (w < c.length && c[w] < sinir[q]) w++;
          if (w >= c.length) break;
          cb.push(t[w]);
        }
        if (cb.length === sinir.length - 1) { cumleBas[k] = cb; konusma[k] = null; }
      });
      return void set({ zs: st.zs + 1 });
    }
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

/** Paragrafı cümlelere böler: her cümlenin bitiş karakter konumu.
 *  scripts/sesli_anlatim/pdf_hizala.py::cumle_sinirlari ile BİREBİR aynı kural (hizalamanın cümle dizini buna dayanır):
 *  [.!?…]+ (+ kapanan tırnak/parantez) ardından boşluk ya da metin sonu; sonraki karakter küçük harfse sınır değil
 *  ("2. basamak", "1.'si" bölünmez). */
function cumleSinirlari(p: ParaBilgi): number[] {
  if (p.cumleler) return p.cumleler;
  const out: number[] = [];
  const re = /[.!?…]+["'”’)\]]*(?:\s+|$)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(p.metin))) {
    if (!m[0]) { re.lastIndex++; continue; }
    const e = m.index + m[0].length;
    const sonraki = p.metin.charAt(e);
    if (sonraki && sonraki !== sonraki.toLocaleUpperCase('tr') && sonraki === sonraki.toLocaleLowerCase('tr')) continue;
    if (e > (out[out.length - 1] || 0)) out.push(e);
    if (re.lastIndex >= p.metin.length) break;
  }
  if (!out.length || out[out.length - 1] < p.metin.length) out.push(p.metin.length);
  p.cumleler = out;
  return out;
}
/** Türkçe hece ≈ ünlü sayısı: kelimenin okunma süresi hecesiyle orantılıdır (harf sayısından çok daha yakın) */
const heceSay = (w: string) => Math.max(1, (w.match(/[aeıioöuüâîû]/gi) || []).length + (/\d/.test(w) ? w.replace(/\D/g, '').length * 1.5 : 0));
const heceOnbellek = new Map<string, { bas: number[]; birikim: number[] }>();
/** Cümledeki kelimeler: başlangıç karakteri ve o kelimeye kadarki hece birikimi */
function heceler(c: string) {
  let h = heceOnbellek.get(c);
  if (!h) {
    const bas: number[] = [], birikim: number[] = [];
    let top = 0;
    for (const m of c.matchAll(/\S+/g)) { bas.push(m.index!); birikim.push(top); top += heceSay(m[0]); }
    birikim.push(top);
    h = { bas, birikim };
    if (heceOnbellek.size > 400) heceOnbellek.clear();
    heceOnbellek.set(c, h);
  }
  return h;
}
/** Ses öne alma (sn): çizim + göz algısı gecikmesini karşılar, işaret kelimeyle aynı anda yanar */
const ONDE = 0.08;
/** Sesin o an okuduğu konum: etkin cümle içindeki karakter (cümle başına göre) ve cümlenin paragraf içi başlangıcı.
 *  Ölçülü konuşma parçaları varsa duraklamalar atlanır ve kelimeler hece sayısıyla paylaştırılır. */
export function cdKonusulanKarakter(): { cumleBas: number; c: number } | null {
  const k = posByI.get(st.aktif);
  const r = cdCumleAraligi(st.aktif, st.cumle);
  if (k == null || !r) return null;
  const p = paras[k];
  const t = st.t + ONDE * (st.rate || 1);
  const kt = kelimeT[k], kc = kelimeC[k];
  if (kt && kc) {
    // Ölçülü: sesin geçtiği son kelime; cümle dışına taşmasın
    let lo = 0, hi = kt.length - 1, w = 0;
    while (lo <= hi) { const m = (lo + hi) >> 1; if (kt[m] <= t) { w = m; lo = m + 1; } else hi = m - 1; }
    const c = Math.min(Math.max(kc[w], r[0]), r[1] - 1);
    return { cumleBas: r[0], c: c - r[0] };
  }
  const metin = p.metin.slice(r[0], r[1]);
  const h = heceler(metin);
  const parca = konusma[k]?.[st.cumle];
  let oran: number;
  if (parca && parca.length >= 2) {
    let top = 0, gecen = 0;
    for (let q = 0; q + 1 < parca.length; q += 2) {
      const d = parca[q + 1] - parca[q];
      top += d;
      gecen += Math.min(d, Math.max(0, t - parca[q]));
    }
    oran = top > 0 ? gecen / top : 0;
  } else {
    const s = cumleSinirlari(p);
    const cb = cumleBas[k];
    let t0: number, t1: number;
    if (cb) {
      t0 = st.cumle ? cb[st.cumle - 1] : starts[k];
      t1 = st.cumle < cb.length ? cb[st.cumle] : ends[k];
    } else {
      const span = ends[k] - starts[k];
      t0 = starts[k] + ((st.cumle ? s[st.cumle - 1] : 0) / p.len) * span;
      t1 = starts[k] + (s[st.cumle] / p.len) * span;
    }
    oran = t1 > t0 ? Math.min(1, Math.max(0, (t - t0) / (t1 - t0))) : 0;
  }
  // hece birikimine göre kelime
  const hedef = oran * h.birikim[h.birikim.length - 1];
  let w = 0;
  while (w + 1 < h.bas.length && h.birikim[w + 1] <= hedef) w++;
  return { cumleBas: r[0], c: h.bas[w] ?? 0 };
}
/** Okunan kelimenin paragraf içi başlangıcı (yalnız kelime değişince değişir: seçici olarak kullanılır) */
export function cdKelimeBas(): number {
  const k = cdKonusulanKarakter();
  const pi = posByI.get(st.aktif);
  if (!k || pi == null) return -1;
  return k.cumleBas + k.c;
}
/** Etkin cümlenin [başlangıç, bitiş) karakter aralığı */
/** Görüntü için cümle sınırları: yüklü dersin (ses hizalı) sınırları, yoksa aynı kural metinden. */
export function cdParagrafSinirlari(i: number, metin: string): number[] {
  const k = posByI.get(i);
  if (k != null && paras[k]?.metin === metin) return cumleSinirlari(paras[k]);
  return cumleSinirlari({ metin } as ParaBilgi);
}

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
  const cb = cumleBas[k];
  if (cb) {
    let c = 0;
    while (c < cb.length && cb[c] <= t + 0.05) c++;
    return { aktif: p.i, cumle: c, bolum: p.bolum };
  }
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
/** Çalma noktasının önünde arabellekte kalan saniye (bağlantı koptu kartı, tasarım S17) */
export function cdTampon(): number {
  const a = audio; if (!a) return 0;
  const t = a.currentTime;
  for (let i = 0; i < a.buffered.length; i += 1) if (a.buffered.start(i) <= t + 0.5 && a.buffered.end(i) >= t) return Math.max(0, a.buffered.end(i) - t);
  return 0;
}
/** Bağlantı gelince sesi kaldığı yerden yeniden yükleyip çalar */
export function cdYenidenDene() {
  const a = audio; const src = a?.getAttribute('src'); if (!a || !src) return;
  const t = st.t || a.currentTime || 0;
  a.src = src;
  a.addEventListener('loadedmetadata', () => { try { a.currentTime = t; } catch { /* yok */ } a.play().catch(() => {}); }, { once: true });
  a.load();
}
let raf = 0;
let sonKayit = 0;

let sonTik = 0;
function tick() {
  sonTik = performance.now();
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
// Yedek saat: kare döngüsü kısılırsa (gömülü pencere, güç tasarrufu, düşük kare hızı) timeupdate ~250 ms–1 sn'de bir gelir;
// kelime kelime işaret sesten geri kalmasın diye çalarken 70 ms'den eski konum 50 ms'de bir tazelenir.
// Yalnız çalarken kurulur: eskiden modül yüklenince her öğrencide (ders açılmasa da) saniyede 20 kez uyanıyordu.
let yedekSaat = 0;
function yedekSaatBaslat() {
  if (yedekSaat || typeof window === 'undefined') return;
  yedekSaat = window.setInterval(() => {
    if (!st.playing) { yedekSaatDurdur(); return; }
    if (performance.now() - sonTik > 70) tick();
  }, 50);
}
function yedekSaatDurdur() {
  if (yedekSaat) { window.clearInterval(yedekSaat); yedekSaat = 0; }
}

function pitch(a: HTMLAudioElement) {
  const x = a as HTMLAudioElement & { mozPreservesPitch?: boolean; webkitPreservesPitch?: boolean };
  x.preservesPitch = true;
  x.mozPreservesPitch = true;
  x.webkitPreservesPitch = true;
}

let sonYenidenBag = 0;
/** Son duraklatma kullanıcıdan mı (düğme / bildirim)? Ağ kopmasında yalnız kullanıcı durdurmadıysa sürdürülür. */
let kullaniciDurdurdu = true;
function ses(): HTMLAudioElement {
  if (audio) return audio;
  const a = new Audio();
  a.preload = 'metadata';
  // Arka planda (ekran kapalı / başka uygulama) çalmayı sürdürmesi için öğe belgeye bağlı olmalı:
  // bağsız Audio nesnesini mobil tarayıcılar (özellikle iOS PWA) gizlenince askıya alabiliyor.
  a.setAttribute('playsinline', '');
  a.setAttribute('aria-hidden', 'true');
  a.style.display = 'none';
  document.body.appendChild(a);
  pitch(a);
  a.addEventListener('play', () => {
    kullaniciDurdurdu = false;
    set({ playing: true, hata: null }); loopBaslat(); yedekSaatBaslat(); ekranUyanik(true);
    // Medya oturumunu müzik çalardan geri al (yoksa arka planda bildirim/kulaklık "oynat" müziği başlatır)
    (window as any).__medsorMsSahip = 'canli';
    window.dispatchEvent(new Event('medsor:canli-ders-oynuyor'));
    msKur(); msMeta(); msDurum();
  });
  a.addEventListener('pause', () => { yedekSaatDurdur(); ekranUyanik(false); set({ playing: false }); tick(); konumKaydet(); msDurum(); });
  // Bitirdiklerim: dersin sonuna kadar dinlenince konu "bitti" olur
  a.addEventListener('ended', () => { yedekSaatDurdur(); ekranUyanik(false); if (st.key) konuBitir('sesli', st.key); set({ playing: false }); konumKaydet(true); msDurum(); bitinceFn?.(); try { window.dispatchEvent(new CustomEvent('cd:bitti', { detail: { key: st.key } })); } catch { /* yok */ } });
  // Bitirdiklerim: ses çalarken (sekme arka planda da) konunun dinleme süresi
  window.setInterval(() => { if (st.playing && st.key && !st.bekliyor) sureEkle('sesli', st.key, 5); }, 5000);
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
    // Arka planda uzun akışta ağ kopması: kaldığı yerden bir kez yeniden bağlan
    if (a.error?.code === MediaError.MEDIA_ERR_NETWORK && !kullaniciDurdurdu && Date.now() - sonYenidenBag > 15000) {
      sonYenidenBag = Date.now();
      const t = st.t || 0;
      const src = a.getAttribute('src')!;
      a.src = src;
      a.addEventListener('loadedmetadata', () => { try { a.currentTime = t; } catch { /* yok */ } a.play().catch(() => {}); }, { once: true });
      a.load();
      return;
    }
    set({ hata: 'Ses dosyası açılamadı.', playing: false, bekliyor: false });
  });
  // Arka plana geçerken konum yazılır: mobil tarayıcı arka plandaki sekmeyi pagehide olmadan da kapatabilir
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') loopBaslat(); else konumKaydet(); });
  window.addEventListener('pagehide', () => konumKaydet());
  // Müzik başlarsa ders duraklar (iki ses üst üste binmesin, medya tuşları karışmasın)
  window.addEventListener('medsor:muzik-oynuyor', () => { if (!a.paused) cdDuraklat(); });
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
const tercihVaryant = (vs: CdVaryant[]) => cdTercihVaryant(vs)?.id ?? null;

/* ---------------- varsayılan ses (kullanıcı tercihi; yoksa EMA) ---------------- */
const VARSAYILAN_SES_KEY = 'medsoru_canli_ders_varsayilan_ses_v1';
/** Sesin dersler arası kimliği: sağlayıcı + ses adı ("ema-yerel|Ema") */
export const cdSesKimlik = (v: Pick<CdVaryant, 'saglayici' | 'ses' | 'id'>) => `${v.saglayici || ''}|${v.ses || v.id}`;
const varsayilanAbone = new Set<() => void>();
export const cdVarsayilanSes = (): string | null => { try { return localStorage.getItem(VARSAYILAN_SES_KEY); } catch { return null; } };
export function cdVarsayilanSesAyarla(kimlik: string | null) {
  try { kimlik ? localStorage.setItem(VARSAYILAN_SES_KEY, kimlik) : localStorage.removeItem(VARSAYILAN_SES_KEY); } catch { /* yok */ }
  varsayilanAbone.forEach((f) => f());
}
/** Bileşenlerde: tercih değişince yeniden çizilir */
export const useCdVarsayilanSes = () => useSyncExternalStore(
  (f) => { varsayilanAbone.add(f); window.addEventListener('storage', f); return () => { varsayilanAbone.delete(f); window.removeEventListener('storage', f); }; },
  cdVarsayilanSes, () => null,
);
/** Dersin çalınacak sesi: kullanıcının varsayılanı → aynı sağlayıcı → EMA → ilk ses */
export function cdTercihVaryant(vs: CdVaryant[]): CdVaryant | undefined {
  const k = cdVarsayilanSes();
  if (k) {
    const v = vs.find((x) => cdSesKimlik(x) === k) || vs.find((x) => x.saglayici && x.saglayici === k.split('|')[0]);
    if (v) return v;
  }
  return vs.find((x) => /ema/i.test(x.saglayici || '')) || vs[0];
}

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
    // no: görünen etiket ("Patoloji 16"); yeniden kurulumda (tekrar) brans gelmez, etiket aynen kalır
    key: o.key, no: cdDersEtiketi(o), baslik: o.baslik, varyantlar: o.varyantlar, vid,
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
  else cdDuraklat();
}
export function cdDuraklat() { kullaniciDurdurdu = true; audio?.pause(); }
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
  h('pause', () => cdDuraklat());
  h('stop', () => cdDuraklat());
  // tasarım S16: kilit ekranında ±15 sn
  h('seekbackward', (d) => cdSar(-(d.seekOffset || 15)));
  h('seekforward', (d) => cdSar(d.seekOffset || 15));
  h('seekto', (d) => { if (d.seekTime != null) cdAtla(d.seekTime); });
  h('previoustrack', () => cdBolumAtla(-1));
  h('nexttrack', () => cdBolumAtla(1));
}
function msMeta() {
  if (!('mediaSession' in navigator) || typeof MediaMetadata === 'undefined') return;
  const v = st.varyantlar.find((x) => x.id === st.vid);
  try {
    // tasarım S16: kilit ekranında o an okunan cümle altyazı satırı (artist), bölüm adı (album)
    const p = st.detay?.bolumler.flatMap((b) => b.paragraflar).find((x) => x.i === st.aktif);
    const ar = p && st.cumle >= 0 ? cdCumleAraligi(st.aktif, st.cumle) : null;
    const cumle = p && ar ? p.metin.slice(ar[0], ar[1]).trim() : '';
    const bolumAd = st.bolum >= 0 ? st.detay?.bolumler[st.bolum]?.baslik : '';
    navigator.mediaSession.metadata = new MediaMetadata({
      title: `${st.no ? `${st.no} · ` : ''}${st.baslik}`,
      artist: cumle ? (cumle.length > 110 ? `${cumle.slice(0, 107)}…` : cumle) : 'MeDSor',
      album: bolumAd || `Sesli ders${v?.ses ? ` · ${v.ses}` : ''}`,
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

// Kilit ekranı altyazısı: okunan cümle değişince medya bilgisi yenilenir (cümle başına bir kez)
let msSonCumle = '';
subscribe(() => {
  const k = `${st.key}|${st.aktif}|${st.cumle}`;
  if (k === msSonCumle || !st.key) return;
  msSonCumle = k;
  msMeta();
});
