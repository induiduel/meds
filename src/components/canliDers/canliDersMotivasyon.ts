/**
 * Sesli ders · motivasyon konuşmaları ve mola. Ders sesine DOKUNMAZ: kısa klipler (public/ses/motivasyon/<id>.mp3,
 * metinler src/data/sesli_motivasyon/havuz.json, üretim scripts/sesli_anlatim/motivasyon_ses_uret.py) ayrı bir ses
 * öğesiyle çalar; o sırada ders duraklar, klip bitince kaldığı paragrafın başından sürer.
 *
 * Yerler: dersin başı (baştan başlarken), ortası (yarıyı geçince ilk paragraf sınırında), sonu (ders bitince) — her
 * ders oturumunda birer kez. Satır öğrencinin durumuna göre seçilir (ilk ders, bitirilen ders sayısı, tekrar, sınava
 * kalan gün, saat); son kullanılan satırlar yinelenmez, seçim ders anahtarına göre dağılır (çoğu derste farklı cümle).
 * Mola: kesintisiz ~15–20 dk dinlemeden sonra paragraf sınırında ders durur, mola penceresi açılır (CanliDersMola).
 * Ekran gizliyken klip çalınmaz (mobil arka planda ikinci ses öğesi engellenebilir; ders kesilmesin).
 */
import { useSyncExternalStore } from 'react';
import havuzVeri from '../../data/sesli_motivasyon/havuz.json';
import { cdAbone, cdAralik, cdDurum, cdDuraklat, cdToggle, cdAtla } from './canliDersStore';
import { takipOku } from '../../services/calismaTakip';
import { sinavaKalanGun } from '../../services/kurulTakvimi';

type Yer = 'basla' | 'orta' | 'son' | 'mola';
interface Satir { id: string; yer: Yer; bag: string; metin: string }
const SATIRLAR: Satir[] = (havuzVeri as { satirlar: Satir[] }).satirlar;

const ACIK_KEY = 'medsoru_cd_motivasyon_v1';
const SON_KEY = 'medsoru_cd_motivasyon_son_v1';
const SON_SAKLA = 30;

/* ---------- tercih (açık/kapalı) ---------- */
const tercihAbone = new Set<() => void>();
export const cdMotivasyonAcik = (): boolean => { try { return localStorage.getItem(ACIK_KEY) !== '0'; } catch { return true; } };
export function cdMotivasyonAyarla(acik: boolean) {
  try { localStorage.setItem(ACIK_KEY, acik ? '1' : '0'); } catch { /* yok */ }
  tercihAbone.forEach((f) => f());
}
export const useCdMotivasyonAcik = () => useSyncExternalStore(
  (f) => { tercihAbone.add(f); return () => tercihAbone.delete(f); }, cdMotivasyonAcik, () => true,
);

/* ---------- bağlam (öğrencinin ilerleyişi) ---------- */
function baglamlar(key: string): string[] {
  const k = takipOku().k;
  const sesli = Object.entries(k).filter(([a]) => a.startsWith('sesli:'));
  const biten = sesli.filter(([, v]) => v.durum === 'bitti').length;
  const bu = k[`sesli:${key}`];
  const gun = (() => { try { return sinavaKalanGun(); } catch { return 99; } })();
  const saat = new Date().getHours();
  const b: string[] = [];
  if (gun >= 0 && gun <= 2) b.push('sinav_kapida');
  else if (gun >= 0 && gun <= 10) b.push('sinav_yakin');
  if (bu?.durum === 'bitti' || bu?.bittiAt || (bu?.tur || 0) > 0) b.push('tekrar');
  if (biten === 0 && sesli.length <= 1) b.push('ilk');
  if (biten >= 20) b.push('cok');
  else if (biten >= 5) b.push('ilerleme');
  if (saat >= 23 || saat < 5) b.push('gece');
  else if (saat >= 5 && saat < 10) b.push('sabah');
  return b;
}

const sonlar = (): string[] => { try { return JSON.parse(localStorage.getItem(SON_KEY) || '[]') || []; } catch { return []; } };
const sonaEkle = (id: string) => {
  try { localStorage.setItem(SON_KEY, JSON.stringify([id, ...sonlar().filter((x) => x !== id)].slice(0, SON_SAKLA))); } catch { /* yok */ }
};
const karma = (s: string) => { let h = 2166136261; for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619); return h >>> 0; };

/** Duruma uygun satır: önce özel bağlamlar (%65), sonra genel; son kullanılanlar dışarıda; ders anahtarıyla dağıtılır. */
export function cdMotivasyonSec(yer: Yer, key: string): Satir | null {
  const tumu = SATIRLAR.filter((s) => s.yer === yer);
  if (!tumu.length) return null;
  const son = new Set(sonlar());
  const bag = baglamlar(key);
  const ozel = tumu.filter((s) => bag.includes(s.bag) && !son.has(s.id));
  const genel = tumu.filter((s) => s.bag === 'genel' && !son.has(s.id));
  const tohum = karma(`${key}|${yer}|${Date.now() >> 16}`);
  let aday = ozel.length && (tohum % 100 < 65 || !genel.length) ? ozel : genel;
  if (!aday.length) aday = tumu.filter((s) => s.bag === 'genel' || bag.includes(s.bag));
  if (!aday.length) aday = tumu;
  return aday[tohum % aday.length];
}

/* ---------- mola penceresi durumu ---------- */
export type MolaAnim = 'zirve' | 'calisma' | 'sevgi' | 'gunes' | 'kutlama';
/** tip: 'mola' (15–20 dk) | 'bitis' (ders sonu; key = biten ders) */
export interface MolaDurum { acik: boolean; metin: string; dk: number; anim: MolaAnim; tip: 'mola' | 'bitis'; key: string | null; baslik: string;
  /** ders sonu: pekiştirme penceresi (CanliDersCozucuSoru) açıldıysa animasyon + söz onun içinde gösterilir */
  birlesik: boolean }
let mola: MolaDurum = { acik: false, metin: '', dk: 0, anim: 'kutlama', tip: 'mola', key: null, baslik: '', birlesik: false };
const ANIM_KEY = 'medsoru_cd_mola_anim_v1';
/** Hikâyeli animasyon: sınav yakınsa zirve (azim), gece güneş (zor günler geçer); yoksa dörtlü sırayla, öncekinden farklı */
function animSec(bag: string | undefined): MolaAnim {
  // sınama: medsoru_cd_mola_test=<zirve|calisma|sevgi|gunes> o animasyonu zorlar (yalnız bu tarayıcı)
  try {
    const z = localStorage.getItem('medsoru_cd_mola_test');
    if (z === 'zirve' || z === 'calisma' || z === 'sevgi' || z === 'gunes') return z;
  } catch { /* yok */ }
  let son = '';
  try { son = localStorage.getItem(ANIM_KEY) || ''; } catch { /* yok */ }
  let a: MolaAnim;
  if (bag === 'sinav_yakin' || bag === 'sinav_kapida') a = son === 'zirve' ? 'sevgi' : 'zirve';
  else if (bag === 'gece') a = son === 'gunes' ? 'sevgi' : 'gunes';
  else {
    const dort: MolaAnim[] = ['zirve', 'calisma', 'sevgi', 'gunes'].filter((x) => x !== son) as MolaAnim[];
    a = dort[Math.floor(Math.random() * dort.length)];
  }
  try { localStorage.setItem(ANIM_KEY, a); } catch { /* yok */ }
  return a;
}
const molaAbone = new Set<() => void>();
const molaYaz = (m: MolaDurum) => { mola = m; molaAbone.forEach((f) => f()); };
export const useCdMola = () => useSyncExternalStore((f) => { molaAbone.add(f); return () => molaAbone.delete(f); }, () => mola, () => mola);

/* ---------- klip oynatma ---------- */
let klip: HTMLAudioElement | null = null;
let klipCaliyor = false;
/** Klip bitince ders sürsün mü (mola penceresinde sürmez) */
let sonraSur = false;
let surT: number | null = null;
let klipBas = 0;

const klipUrl = (id: string) => `${import.meta.env.BASE_URL || '/'}ses/motivasyon/${id}.mp3`.replace(/\/{2,}/g, '/');

function dersiSur() {
  const st = cdDurum();
  if (surT != null) cdAtla(surT);
  surT = null;
  if (st.key && !st.playing) cdToggle();
}

function klipBitti() {
  klipCaliyor = false;
  if (sonraSur) { sonraSur = false; dersiSur(); }
}

function klipCal(s: Satir, sur: boolean, paragrafBasi: number | null): boolean {
  if (typeof document === 'undefined' || document.visibilityState !== 'visible') return false;
  if (!klip) {
    klip = new Audio();
    klip.preload = 'auto';
    klip.setAttribute('playsinline', '');
    klip.addEventListener('ended', klipBitti);
    klip.addEventListener('error', klipBitti);
  }
  const st = cdDurum();
  sonraSur = sur;
  surT = paragrafBasi;
  if (st.playing) cdDuraklat();
  klip.src = klipUrl(s.id);
  klip.playbackRate = Math.min(1.25, Math.max(0.9, st.rate || 1));
  klipCaliyor = true;
  klipBas = performance.now();
  sonaEkle(s.id);
  klip.play().catch(() => klipBitti());
  return true;
}
export const cdKlipDurdur = () => { if (klip && klipCaliyor) { klip.pause(); klipCaliyor = false; } sonraSur = false; };

/* ---------- izleyici ---------- */
let kurulu = false;
const yapildi = new Map<string, Set<Yer>>();
const yap = (key: string, y: Yer) => { const s = yapildi.get(key) || new Set<Yer>(); s.add(y); yapildi.set(key, s); };
const yapildiMi = (key: string, y: Yer) => !!yapildi.get(key)?.has(y);

let oncekiKey: string | null = null;
let oncekiCaliyor = false;
let oncekiAktif = -1;
let oncekiT = 0;
/** Kesintisiz dinleme (sn) ve molanın geleceği eşik (15–20 dk arası rastgele) */
let dinlenen = 0;
let molaEsik = 0;
// medsoru_cd_mola_test=1: sınama için 20 sn
const yeniEsik = () => { let t = false; try { t = !!localStorage.getItem('medsoru_cd_mola_test'); } catch { /* yok */ } molaEsik = t ? 20 : (15 + Math.random() * 5) * 60; };
let molaBekliyor = false;
let sonSaat = 0;

function izle() {
  const st = cdDurum();
  const key = st.key;
  const acik = cdMotivasyonAcik();
  // Bir klip çalarken ders başlarsa (ör. oynatma listesi sonraki derse geçti) klip bitene dek ders bekler
  // (klip başlarken verilen duraklatmanın 'pause' olayı eşzamansız gelir; ilk 600 ms beklenir)
  if (klipCaliyor && st.playing && key && performance.now() - klipBas > 600) {
    cdDuraklat();
    if (!mola.acik) sonraSur = true;
  }
  // Ders sonu penceresi açıkken oynatma listesi sonraki derse geçerse, pencere kapanana dek bekler
  else if (mola.acik && mola.tip === 'bitis' && st.playing && key && key !== mola.key) cdDuraklat();
  if (!key) { oncekiKey = null; oncekiCaliyor = false; return; }

  const yeni = key !== oncekiKey;
  if (yeni) { oncekiAktif = st.aktif; }

  // Ders bitti: sonda bir kez
  if (!yeni && oncekiCaliyor && !st.playing && st.dur > 0 && oncekiT >= st.dur - 1.5 && !klipCaliyor && acik && !yapildiMi(key, 'son')) {
    yap(key, 'son');
    const s = cdMotivasyonSec('son', key);
    const dk = Math.round(dinlenen / 60);
    molaYaz({ acik: true, tip: 'bitis', birlesik: false, key, baslik: st.baslik, anim: animSec(s?.bag), dk,
      metin: s?.metin || 'Tebrikler, bu dersi bitirdin. Sınava bir adım daha yaklaştın.' });
    dinlenen = 0;
    yeniEsik();
    if (s) klipCal(s, false, null);
  }

  if (st.playing && !klipCaliyor && acik) {
    // Baş: baştan başlarken
    if (!yapildiMi(key, 'basla') && st.t < 8) {
      yap(key, 'basla');
      const s = cdMotivasyonSec('basla', key);
      if (s && klipCal(s, true, Math.max(0, st.t - 0.3))) { oncekiKey = key; oncekiCaliyor = true; return; }
    }
    if (!yapildiMi(key, 'basla') && st.t >= 8) yap(key, 'basla');
    // Orta: yarıyı geçince ilk paragraf sınırında
    if (st.aktif !== oncekiAktif && st.aktif >= 0 && st.dur > 120 && st.t > st.dur * 0.45 && st.t < st.dur * 0.8 && !yapildiMi(key, 'orta')) {
      yap(key, 'orta');
      const s = cdMotivasyonSec('orta', key);
      const r = cdAralik(st.aktif);
      if (s && klipCal(s, true, r ? r[0] : null)) { oncekiAktif = st.aktif; oncekiKey = key; oncekiCaliyor = true; return; }
    }
  }

  // Mola: eşik aşıldıysa ilk paragraf sınırında
  if (molaBekliyor && st.playing && st.aktif !== oncekiAktif && st.aktif >= 0 && !klipCaliyor) {
    molaBekliyor = false;
    const r = cdAralik(st.aktif);
    cdDuraklat();
    if (r) cdAtla(r[0]);
    const s = cdMotivasyonSec('mola', key);
    const dk = Math.round(dinlenen / 60);
    dinlenen = 0;
    yeniEsik();
    molaYaz({ acik: true, tip: 'mola', birlesik: false, key, baslik: st.baslik, anim: animSec(s?.bag), metin: s?.metin || 'Uzun süredir dinliyorsun, harikasın. Kısa bir mola ver, sonra kaldığın yerden devam edersin.', dk });
    if (s && acik) klipCal(s, false, null);
  }

  oncekiKey = key;
  oncekiCaliyor = st.playing;
  oncekiAktif = st.aktif;
  oncekiT = st.t;
}

/** Oynatıcı yüklenince bir kez çağrılır (CanliDersDock). */
export function cdMotivasyonKur() {
  if (kurulu || typeof window === 'undefined') return;
  kurulu = true;
  yeniEsik();
  cdAbone(izle);
  sonSaat = Date.now();
  window.setInterval(() => {
    const simdi = Date.now();
    const gecen = Math.min(5, (simdi - sonSaat) / 1000);
    sonSaat = simdi;
    const st = cdDurum();
    if (st.playing && !st.bekliyor) dinlenen += gecen;
    else if (!st.playing && !klipCaliyor && !mola.acik) dinlenen = Math.max(0, dinlenen - gecen * 0.5); // uzun duraklama da moladır
    if (dinlenen >= molaEsik && !molaBekliyor && !mola.acik && cdMotivasyonAcik()) molaBekliyor = true;
  }, 1000);
}

/** Pekiştirme penceresi bu dersin sonu için açıldı: ayrı ders sonu penceresi gösterilmez. */
export function cdBitisBirlestir(key: string) {
  if (mola.acik && mola.tip === 'bitis' && mola.key === key && !mola.birlesik) molaYaz({ ...mola, birlesik: true });
}

export function cdMolaKapat(devam: boolean) {
  cdKlipDurdur();
  molaYaz({ ...mola, acik: false });
  dinlenen = 0;
  if (devam) dersiSur();
}
