import { useSyncExternalStore } from 'react';
import type { Brans } from '../brans';
import { icerikGizli } from '../../../services/siteAyar';

/**
 * Sınav için en önemliler — ortak tipler, sabitler, ders yükleyici ve "öğrendim" deposu (branş geneli).
 * Veri: src/data/<brans>_onem/{index,<kod>}.json (patoloji: scripts/patoloji_onem/birlestir.py; enfeksiyon/üroloji:
 * scripts/spot_cozucu/birlestir.py; her madde branşın Kurul 1 ders PDF'inden birebir alıntılı). Ders başına ayrı dosya, ilk
 * gerektiğinde indirilir. `ornek26`: patolojide hocanın 2026-27 örnek soruları; diğer branşlarda ders PDF'ine dayalı, çıkmışların
 * üslubunda örnek sorular (`zorluk` alanlı; aynı sorular soru çözücüde de var).
 */

export type Tur = 'tanim' | 'en_sik' | 'karakteristik' | 'sayi' | 'eslesme' | 'mekanizma' | 'siniflama' | 'tuzak' | 'tani_tedavi';
export type Kat = 'patoloji' | 'prognoz' | 'tedavi' | 'klinik';
export interface Soru { kok: string; secenekler: Record<string, string>; dogru: string; aciklama?: string; zorluk?: 'kolay' | 'orta' | 'zor' }
export interface Madde {
  id: string; puan: number; baslik: string; bilgi: string; alt?: string[]; tur: Tur;
  alinti: { sayfa: number; metin: string }[]; neden: string; detay: string; ornek_soru?: Soru | null; cikmis?: string[];
  /** 2026-27 örnek soruları (hocanın biçiminde, ders PDF'ine dayalı) */
  ornek26?: Soru[];
  /** sınav kuralı: tablo/şekilden ve klinik bulgudan soru yok */
  kaynak?: 'metin' | 'tablo' | 'sekil'; klinik?: boolean; sinavUygun?: boolean;
  /** patoloji (morfoloji/mekanizma/tanım…) · prognoz · tedavi (sorulabilir) · klinik bulgu (sorulmaz) */
  kategori?: Kat;
}
export interface Aday { id: string; sira: number; gerekce: string }
export interface Cikmis { sinav: string; kok: string; secenekler: Record<string, string>; dogru: string; /** aynı sorunun sorulduğu diğer sınavlar */ tekrar?: string[] }
export interface Ders { kod: string; no: number; baslik: string; pdf: string; ozet: string; neden_onemli: string; maddeler: Madde[]; cikmis: Record<string, Cikmis>; sinavAdaylari?: Aday[]; soruSayisi?: number }
export interface DizinDers { kod: string; no: number; baslik: string; madde: number; bant?: Record<string, number> }
export interface Dizin { surum: string; dersler: DizinDers[] }

const DOSYALAR = import.meta.glob('../../../data/*_onem/*.json') as Record<string, () => Promise<{ default: Ders | Dizin }>>;
const yol = (brans: Brans, kod: string) => `../../../data/${brans}_onem/${kod}.json`;
const bellek = new Map<string, Promise<Ders>>();
/** Panel görünürlüğü (onem:<dizin>/<kod>, kurul:<n>): kapalı ders öğrenciye listelenmez ve açılmaz */
const kapali = (brans: Brans, kod: string) => icerikGizli('onem', `${brans}_onem/${kod}`);
export const dersVar = (kod: string, brans: Brans = 'patoloji') => kod !== 'index' && !kapali(brans, kod) && !!DOSYALAR[yol(brans, kod)];
/** Ders dosyası (modül önbellekli; aynı ders ikinci kez indirilmez) */
export const dersYukle = (kod: string, brans: Brans = 'patoloji'): Promise<Ders> => {
  const a = `${brans}/${kod}`;
  let p = bellek.get(a);
  if (!p) {
    const f = DOSYALAR[yol(brans, kod)];
    if (!f || kod === 'index') return Promise.reject(new Error(`ders yok: ${kod}`));
    if (kapali(brans, kod)) return Promise.reject(new Error('Bu içerik şu an kapalı'));
    p = f().then((m) => m.default as Ders);
    p.catch(() => bellek.delete(a));
    bellek.set(a, p);
  }
  return p;
};
export const dizinYukle = (brans: Brans = 'patoloji'): Promise<Dizin> => {
  const f = DOSYALAR[yol(brans, 'index')];
  return f ? f().then((m) => { const d = m.default as Dizin; return { ...d, dersler: (d.dersler || []).filter((x) => !kapali(brans, x.kod)) }; }) : Promise.resolve({ surum: '', dersler: [] });
};

export const TUR_AD: Record<Tur, string> = {
  tanim: 'Tanım', en_sik: 'En sık', karakteristik: 'Karakteristik', sayi: 'Sayı', eslesme: 'Eşleşme',
  mekanizma: 'Mekanizma', siniflama: 'Sınıflama', tuzak: 'Tuzak', tani_tedavi: 'Tanı',
};
export const TUR_IPUCU: Record<Tur, string> = {
  tanim: 'Tanım ve kavram', en_sik: 'En sık · en az · tek · ilk', karakteristik: 'Tipik görünüm, patognomonik bulgu',
  sayi: 'Sayı, oran, eşik', eslesme: 'Etken → hastalık, gen → sendrom', mekanizma: 'Neden–sonuç zinciri',
  siniflama: 'Tip, evre, derece', tuzak: 'Karıştırılan kavram, çeldirici', tani_tedavi: 'Tanı yöntemi, tedavi',
};
export const BANTLAR = [
  { b: 9, ad: '90–100', kisa: '90+', not: 'Olmazsa olmaz' },
  { b: 8, ad: '80–89', kisa: '80+', not: 'Çok sık sorulur' },
  { b: 7, ad: '70–79', kisa: '70+', not: 'Sık sorulur' },
  { b: 6, ad: '60–69', kisa: '60+', not: 'Bilinmeli' },
  { b: 5, ad: '50–59', kisa: '50+', not: 'Destekleyici' },
  { b: 4, ad: '0–49', kisa: '<50', not: 'Ayrıntı' },
] as const;
export const bantOf = (p: number) => Math.max(4, Math.min(9, Math.floor(p / 10)));
export const katOf = (m: Madde): Kat => m.kategori || (m.klinik ? 'klinik' : 'patoloji');
export const KAT_AD: Record<Kat, string> = { patoloji: 'Patoloji', prognoz: 'Prognoz', tedavi: 'Tedavi', klinik: 'Klinik bulgu' };
export const KAYNAK_AD = { metin: 'Slayt metni', tablo: 'Tablo', sekil: 'Şekil/resim' } as const;
export const ilkSayfa = (m: Madde) => Math.min(...m.alinti.map((a) => a.sayfa), 9999);
export const HEPSI = '*';
export const ADAY = '#';
export const dersAdi = (d: { no: number; baslik: string }) => `${d.no}) ${d.baslik}`;

/** "Öğrendim" işaretleri: madde kimliği dizisi (kimlik ders koduyla başlar, tüm dersler arasında tekil). Profille eşitlenir. */
export const OGRENDIM_KEY = 'medsoru_onem_ogrendim_v1';
let ogr: Set<string> | null = null;
const dinleyiciler = new Set<() => void>();
const oku = (): Set<string> => {
  try { return new Set<string>(JSON.parse(localStorage.getItem(OGRENDIM_KEY) || '[]')); } catch { return new Set(); }
};
const al = () => (ogr ??= oku());
const yay = () => dinleyiciler.forEach((f) => f());
if (typeof window !== 'undefined') {
  window.addEventListener('storage', (e) => { if (e.key === OGRENDIM_KEY) { ogr = oku(); yay(); } });
}
export const ogrenildiAyarla = (ids: string[], v: boolean) => {
  const n = new Set(al());
  ids.forEach((id) => (v ? n.add(id) : n.delete(id)));
  ogr = n;
  try { localStorage.setItem(OGRENDIM_KEY, JSON.stringify([...n])); } catch { /* özel pencere */ }
  yay();
};
export const ogrenilenler = () => al();
export const useOgrenilen = () => useSyncExternalStore((f) => { dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; }, al, al);

/** Küçük, cihaz başına + profil eşitlemeli tercih kaydı (JSON). */
export const tercihOku = <T extends object>(key: string, varsayilan: T): T => {
  try { const v = JSON.parse(localStorage.getItem(key) || 'null'); return v && typeof v === 'object' ? { ...varsayilan, ...v } : varsayilan; } catch { return varsayilan; }
};
export const tercihYaz = (key: string, v: object) => { try { localStorage.setItem(key, JSON.stringify(v)); } catch { /* özel pencere */ } };
export const TERCIH_KEY = 'medsoru_onem_tercih_v1';
/** Son açılan önem dersi (branşlar arası): En önemliler başlangıcındaki "Kaldığın yerden devam" */
export const ONEM_SON_KEY = 'medsoru_onem_son_v1';
export const PDF_KEY = 'medsoru_onem_pdf_v1';
