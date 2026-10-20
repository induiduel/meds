import { useCallback, useEffect, useRef, useSyncExternalStore } from 'react';

/**
 * Konu bazlı çalışma takibi — Sesli ders, Etkileşimli dersler (Öğren), Soru çözücü ve En önemliler.
 *
 * Her konu ("modül:konuKimliği") için: etkin çalışma süresi (sn), çözülen soru sayısı, durum (bitti / tekrarda / açık),
 * tekrar turu ve tarihler tutulur. Ayrıca modül başına gün → saniye (son 120 gün) tutulur; tahmini kalan süre
 * ve "bu hızla kaç gün" hesabı buradan yapılır.
 *
 * Süre yalnız etkin çalışmada artar: sekme görünür ve son 60 sn içinde dokunma/tuş/kaydırma varken ya da ders sesi
 * çalarken (ses arka planda da sayılır). Kayıt `medsoru_calisma_takip_v1` (userKvSync ile cihazlar arası eşitlenir).
 *
 * Durum: `undefined` → içerikten türetilir (ör. tüm sorular çözüldüyse bitti); 'bitti' / 'acik' kullanıcının açık
 * seçimi; 'tekrar' → "Tekrar et" ile yeni tur başladı (türetilen bitti yok sayılır, yeniden "Bitirdim" beklenir).
 */

export type TakipModul = 'sesli' | 'ogren' | 'cozucu' | 'onem' | 'kamp';
export type KonuDurum = 'bitti' | 'tekrar' | 'acik';

export interface KonuKaydi {
  sn: number;
  soru: number;
  durum?: KonuDurum;
  /** kaçıncı tekrar turu (ilk çalışma 0) */
  tur?: number;
  bittiAt?: string;
  ilkAt?: string;
  sonAt?: string;
}

interface TakipVeri {
  k: Record<string, KonuKaydi>;
  /** modül → gün (YYYY-AA-GG) → saniye */
  g: Partial<Record<TakipModul, Record<string, number>>>;
}

export const TAKIP_KEY = 'medsoru_calisma_takip_v1';
const OLAY = 'medsor:calisma-takip';
const GUN_SAKLA = 120;

export const MODUL_AD: Record<TakipModul, string> = {
  sesli: 'Sesli ders',
  ogren: 'Etkileşimli dersler',
  cozucu: 'Soru çözücü',
  onem: 'En önemliler',
  kamp: 'Kurul kampı',
};

const anahtar = (m: TakipModul, konu: string) => `${m}:${konu}`;
const gunAnahtari = (d = new Date()) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

let onbellek: { ham: string | null; v: TakipVeri } = { ham: null, v: { k: {}, g: {} } };
const oku = (): TakipVeri => {
  let ham: string | null = null;
  try { ham = localStorage.getItem(TAKIP_KEY); } catch { /* özel pencere */ }
  if (ham !== onbellek.ham) {
    let v: TakipVeri = { k: {}, g: {} };
    try {
      const x = JSON.parse(ham || '{}');
      if (x && typeof x === 'object') v = { k: x.k && typeof x.k === 'object' ? x.k : {}, g: x.g && typeof x.g === 'object' ? x.g : {} };
    } catch { /* bozuk kayıt */ }
    onbellek = { ham, v };
  }
  return onbellek.v;
};

const yaz = (v: TakipVeri) => {
  try {
    const ham = JSON.stringify(v);
    localStorage.setItem(TAKIP_KEY, ham);
    onbellek = { ham, v };
  } catch { /* kota / özel pencere */ }
  window.dispatchEvent(new Event(OLAY));
};

const guncelle = (m: TakipModul, konu: string, f: (k: KonuKaydi) => KonuKaydi) => {
  if (typeof window === 'undefined' || !konu) return;
  const v = oku();
  const a = anahtar(m, konu);
  const simdi = new Date().toISOString();
  const eski = v.k[a] || { sn: 0, soru: 0 };
  yaz({ ...v, k: { ...v.k, [a]: { ...f(eski), ilkAt: eski.ilkAt || simdi } } });
};

export const konuKaydi = (m: TakipModul, konu: string): KonuKaydi | undefined => oku().k[anahtar(m, konu)];
export const takipOku = oku;

/** Etkin çalışma süresi ekler (konu + modülün o günkü toplamı). */
export function sureEkle(m: TakipModul, konu: string, sn: number) {
  if (typeof window === 'undefined' || !konu || sn <= 0) return;
  const v = oku();
  const a = anahtar(m, konu);
  const simdi = new Date().toISOString();
  const eski = v.k[a] || { sn: 0, soru: 0 };
  const gun = gunAnahtari();
  let mg = { ...(v.g[m] || {}) };
  mg[gun] = (mg[gun] || 0) + sn;
  const gunler = Object.keys(mg);
  if (gunler.length > GUN_SAKLA) mg = Object.fromEntries(gunler.sort().slice(-GUN_SAKLA).map((d) => [d, mg[d]]));
  yaz({ k: { ...v.k, [a]: { ...eski, sn: eski.sn + sn, ilkAt: eski.ilkAt || simdi, sonAt: simdi } }, g: { ...v.g, [m]: mg } });
}

export const soruEkle = (m: TakipModul, konu: string, n = 1) =>
  guncelle(m, konu, (k) => ({ ...k, soru: k.soru + n, sonAt: new Date().toISOString() }));

export const bitir = (m: TakipModul, konu: string) =>
  guncelle(m, konu, (k) => ({ ...k, durum: 'bitti', bittiAt: new Date().toISOString() }));

/** "Bitirdim" işaretini kaldırır: içerikten türetilen "bitti" de yok sayılır. */
export const bitirmeyiGeriAl = (m: TakipModul, konu: string) =>
  guncelle(m, konu, (k) => ({ ...k, durum: 'acik', bittiAt: undefined }));

/** Yeni tekrar turu başlatır. */
export const tekrarBasla = (m: TakipModul, konu: string) =>
  guncelle(m, konu, (k) => ({ ...k, durum: 'tekrar', tur: (k.tur || 0) + 1, bittiAt: undefined, sonAt: new Date().toISOString() }));

/** Tekrar turundaki konu içerikten yeniden tamamlanınca (ör. tüm sorular yeniden çözüldü) bitti sayılır. */
export const tekrarTamamlandi = (m: TakipModul, konu: string) => {
  const k = konuKaydi(m, konu);
  if (k?.durum === 'tekrar') bitir(m, konu);
};

/** Son durum: açık seçim önce gelir; seçim yoksa içerikten türetilen tamamlanma. */
export const bittiMi = (k: KonuKaydi | undefined, turetilen = false) =>
  k?.durum === 'bitti' || (!k?.durum && turetilen);

const abone = (f: () => void) => {
  const g = (e: Event) => { if (e.type === OLAY || (e as StorageEvent).key == null || (e as StorageEvent).key === TAKIP_KEY) f(); };
  window.addEventListener('storage', g);
  window.addEventListener(OLAY, g);
  return () => { window.removeEventListener('storage', g); window.removeEventListener(OLAY, g); };
};

/** Tüm takip verisi (değişince yeniden çizer). */
export const useTakip = () => useSyncExternalStore(abone, oku, oku);

/** Tek konunun kaydı. */
export const useKonuKaydi = (m: TakipModul, konu: string | null | undefined) =>
  useSyncExternalStore(abone, () => (konu ? oku().k[anahtar(m, konu)] : undefined), () => undefined);

/* ── Etkin süre sayacı ─────────────────────────────────────────────────── */

let sonHareket = Date.now();
let hareketKurulu = false;
const hareketKur = () => {
  if (hareketKurulu || typeof window === 'undefined') return;
  hareketKurulu = true;
  const f = () => { sonHareket = Date.now(); };
  ['pointerdown', 'keydown', 'wheel', 'touchstart', 'scroll'].forEach((ev) => window.addEventListener(ev, f, { passive: true, capture: true }));
};
const BOSTA_SN = 60;
const TIK = 5;

/** Sekme görünür ve son 60 sn içinde etkileşim var mı (ya da ses çalıyor mu). */
export const etkinMi = (sesCaliyor = false) => {
  hareketKur();
  if (sesCaliyor) return true;
  return document.visibilityState === 'visible' && Date.now() - sonHareket <= BOSTA_SN * 1000;
};

/**
 * Bileşen açıkken konunun süresini sayar. `konu` null ise saymaz. `sesCaliyor` true iken (ders sesi) sekme arka
 * planda olsa da sayar.
 */
export function useKonuSayaci(m: TakipModul, konu: string | null | undefined, sesCaliyor = false) {
  const ses = useRef(sesCaliyor);
  ses.current = sesCaliyor;
  useEffect(() => {
    if (!konu) return;
    hareketKur();
    sonHareket = Date.now(); // konu açılışı etkileşim sayılır
    const id = window.setInterval(() => { if (etkinMi(ses.current)) sureEkle(m, konu, TIK); }, TIK * 1000);
    return () => window.clearInterval(id);
  }, [m, konu]);
}

/**
 * Soru sayacı: aynı açılışta her soru bir kez sayılır (yeniden açılınca yeniden çözülen soru yine sayılır).
 * Dönen işlev soru kimliğiyle çağrılır.
 */
export function useSoruSayaci(m: TakipModul, konu: string | null | undefined) {
  const sayilan = useRef<{ konu: string | null | undefined; s: Set<string> }>({ konu, s: new Set() });
  if (sayilan.current.konu !== konu) sayilan.current = { konu, s: new Set() };
  return useCallback((soruId: string | number) => {
    if (!konu) return;
    const id = String(soruId);
    if (sayilan.current.s.has(id)) return;
    sayilan.current.s.add(id);
    soruEkle(m, konu, 1);
  }, [m, konu]);
}

/* ── Özet ve tahmin ───────────────────────────────────────────────────── */

export interface KonuGirdi {
  id: string;
  /** içeriğin beklenen süresi (sn): ses uzunluğu, soru × ortalama vb. */
  beklenen: number;
  /** içerikten türetilen tamamlanma (tüm sorular çözüldü, tüm adımlar görüldü …) */
  turetilen?: boolean;
  /** konuya bağlı başka kaynaktan gelen soru sayısı (ör. sesli derste ilgili çözücü soruları) */
  ekSoru?: number;
}

export interface Hiz {
  /** gerçek süre / beklenen süre (bitirilen konulardan); veri yoksa 1 */
  oran: number;
  kaynak: 'senin' | 'icerik';
  /** bitirilen ve süresi ölçülen konu sayısı */
  ornek: number;
  /** son 14 günde çalışılan günlerin ortalaması (sn/gün); veri yoksa 0 */
  gunluk: number;
}

/** Hız ölçümüne yalnız uygulamada gerçekten çalışılmış konular girer: önceden çalışılıp "Bitirdim" ile işaretlenen
 *  (beklenen sürenin %25'inden ve 2 dk'dan az süreli) konular hızı bozmasın. */
const olculebilir = (sn: number, beklenen: number) => sn >= Math.max(120, beklenen * 0.25);

/** Modülün ortalama ilerleme hızı: bitirdiği konularda harcadığı süre ÷ içeriğin beklenen süresi. */
export function hizHesapla(m: TakipModul, konular: KonuGirdi[], v: TakipVeri = oku()): Hiz {
  let gercek = 0, beklenen = 0, ornek = 0;
  for (const g of konular) {
    const k = v.k[anahtar(m, g.id)];
    if (!k || !g.beklenen || !olculebilir(k.sn, g.beklenen) || !bittiMi(k, g.turetilen)) continue;
    gercek += k.sn; beklenen += g.beklenen; ornek++;
  }
  const oran = ornek ? Math.max(0.35, Math.min(4, gercek / beklenen)) : 1;
  const mg = v.g[m] || {};
  const sinir = gunAnahtari(new Date(Date.now() - 13 * 86400_000));
  const gunler = Object.entries(mg).filter(([d, sn]) => d >= sinir && sn >= 120);
  const gunluk = gunler.length ? gunler.reduce((s, [, sn]) => s + sn, 0) / gunler.length : 0;
  return { oran, kaynak: ornek ? 'senin' : 'icerik', ornek, gunluk };
}

export interface GrupOzeti {
  toplam: number;
  biten: number;
  tekrarda: number;
  sn: number;
  soru: number;
  /** kalan konuları bitirmek için çalışma hızına göre tahmini süre (sn) */
  kalanSn: number;
  /** kalan konuların çalışma hızından bağımsız ham ders/içerik süresi (sn) */
  kalanIcerikSn: number;
  /** tüm konuların toplam ders/içerik süresi (sn) */
  toplamIcerikSn: number;
}

/** Bir dersin (konu listesi) özeti; `hiz` aynı modülün tüm konularından hesaplanır. */
export function grupOzeti(m: TakipModul, konular: KonuGirdi[], hiz: Hiz, v: TakipVeri = oku()): GrupOzeti {
  const o: GrupOzeti = { toplam: konular.length, biten: 0, tekrarda: 0, sn: 0, soru: 0, kalanSn: 0, kalanIcerikSn: 0, toplamIcerikSn: 0 };
  for (const g of konular) {
    const k = v.k[anahtar(m, g.id)];
    o.sn += k?.sn || 0;
    o.soru += (k?.soru || 0) + (g.ekSoru || 0);
    o.toplamIcerikSn += g.beklenen || 0;
    if (bittiMi(k, g.turetilen)) { o.biten++; continue; }
    if (k?.durum === 'tekrar') o.tekrarda++;
    o.kalanIcerikSn += g.beklenen || 0;
    const hedef = g.beklenen * hiz.oran;
    // tekrar turunda önceki turun süresi düşülmez; ilk turda harcanan süre düşülür (en az %15 kalır)
    const harcanan = k?.durum === 'tekrar' ? 0 : k?.sn || 0;
    o.kalanSn += Math.max(hedef * 0.15, hedef - harcanan);
  }
  o.kalanSn = Math.round(o.kalanSn);
  o.kalanIcerikSn = Math.round(o.kalanIcerikSn);
  o.toplamIcerikSn = Math.round(o.toplamIcerikSn);
  return o;
}

/* ── Biçim ────────────────────────────────────────────────────────────── */

/** 0 → "0 dk", 45 → "1 dk", 3720 → "1 sa 2 dk" */
export const sureYaz = (sn: number) => {
  const dk = Math.round(sn / 60);
  if (sn > 0 && dk === 0) return '<1 dk';
  const sa = Math.floor(dk / 60);
  return sa ? `${sa} sa${dk % 60 ? ` ${dk % 60} dk` : ''}` : `${dk} dk`;
};

/** Günlük ortalamaya göre kaç gün: "≈ 3 gün" (veri yoksa boş) */
export const gunYaz = (kalanSn: number, gunluk: number) => {
  if (!gunluk || kalanSn <= 0) return '';
  const g = Math.max(1, Math.ceil(kalanSn / gunluk));
  return g > 365 ? '' : `≈ ${g} gün`;
};
