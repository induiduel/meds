/**
 * Canlı ders · oynatma listesi ve tekrar. Kullanıcının tek bir "Listem"i vardır (ders anahtarları, sıralı); liste
 * oynatılınca dersler sırayla çalar (ders bitince canliDersStore `cdBitinceKaydet` kancası). Tekrar:
 *  - 'ders'  : biten ders N kez daha çalar (liste çalarken her ders; liste dışında tek ders de),
 *  - 'liste' : liste sonuna gelince başa döner, N kez daha (yalnız liste çalarken).
 * N = 1 | 2 | 3 | 0 (sınırsız). Liste ve tekrar tercihi profilde eşitlenir (userKvSync).
 *
 * Liste "çalıyor" sayılır: aktif && şu an yüklü ders = aktifKey. Kullanıcı başka bir dersi elle açarsa liste kendiliğinden
 * devre dışı kalır (ders bitince sıradakine geçilmez).
 */
import { useSyncExternalStore } from 'react';
import { navigateTo, pathFor } from '../../router';
import { cdAbone, cdBitinceKaydet, cdDurum, cdListeGetir, cdOynat, type CdListeDers, type CdOzet } from './canliDersStore';

export type CdTekrarMod = 'kapali' | 'ders' | 'liste';
/** 0 = sınırsız */
export type CdTekrarSayi = 0 | 1 | 2 | 3;
export const CD_TEKRAR_SAYILAR: CdTekrarSayi[] = [1, 2, 3, 0];
export const tekrarSayiYaz = (n: CdTekrarSayi) => (n === 0 ? '∞' : `${n}×`);

const LISTE_KEY = 'medsoru_canli_ders_liste_v1';
const TEKRAR_KEY = 'medsoru_canli_ders_tekrar_v1';
/** Birden çok adlandırılmış liste (2026-11-20). Eski tek liste (LISTE_KEY) ilk açılışta "Listem" adıyla buraya taşınır;
 *  LISTE_KEY seçili listenin aynası olarak yazılmaya devam eder (eski sürüm sekmeleri/eşitleme kırılmasın). */
const LISTELER_KEY = 'medsoru_canli_ders_listeler_v1';

/** Liste istatistiği: sn = liste çalarken dinlenen süre, ders = listeden bitirilen ders, tekrar = ders tekrarı,
 *  tur = listenin baştan sona bitişi, son = son dinleme (ms) */
export interface CdListeIst { sn: number; ders: number; tekrar: number; tur: number; son?: number }
export interface CdListe { id: string; ad: string; keys: string[]; olusturma?: number; ist?: CdListeIst }
export const bosIst = (): CdListeIst => ({ sn: 0, ders: 0, tekrar: 0, tur: 0 });

export interface CdListeState {
  /** Seçili listenin dersleri */
  keys: string[];
  listeler: CdListe[];
  seciliId: string;
  mod: CdTekrarMod;
  sayi: CdTekrarSayi;
  /** Liste oynatması başlatıldı mı (şu an çalan dersin listeden gelip gelmediği ayrıca denetlenir) */
  aktif: boolean;
  aktifKey: string | null;
  /** Bu dersin kaçıncı tekrarı (0 = ilk çalış) */
  dersTur: number;
  /** Listenin kaçıncı tekrarı */
  listeTur: number;
}

const oku = <T,>(k: string, d: T): T => {
  try {
    const v = JSON.parse(localStorage.getItem(k) || 'null');
    return v == null ? d : v;
  } catch {
    return d;
  }
};
const yaz = (k: string, v: unknown) => {
  try {
    localStorage.setItem(k, JSON.stringify(v));
  } catch {
    /* depolama kapalı */
  }
};
const tekrarOku = (): { mod: CdTekrarMod; sayi: CdTekrarSayi } => {
  const t = oku<{ mod?: string; sayi?: number }>(TEKRAR_KEY, {});
  const mod = t.mod === 'ders' || t.mod === 'liste' ? t.mod : 'kapali';
  const sayi = (CD_TEKRAR_SAYILAR as number[]).includes(Number(t.sayi)) ? (Number(t.sayi) as CdTekrarSayi) : 1;
  return { mod, sayi };
};
const keysOku = () => {
  const v = oku<unknown>(LISTE_KEY, []);
  return Array.isArray(v) ? [...new Set(v.filter((x): x is string => typeof x === 'string' && !!x))] : [];
};

const temizKeys = (v: unknown) =>
  Array.isArray(v) ? [...new Set(v.filter((x): x is string => typeof x === 'string' && !!x))] : [];
const yeniId = () => `l${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`;
function listelerOku(): { listeler: CdListe[]; seciliId: string } {
  const v = oku<{ listeler?: unknown; seciliId?: unknown } | null>(LISTELER_KEY, null);
  let listeler: CdListe[] = Array.isArray(v?.listeler)
    ? (v!.listeler as any[])
        .filter((l) => l && typeof l.id === 'string')
        .map((l) => ({ id: l.id, ad: String(l.ad || 'Liste').slice(0, 40), keys: temizKeys(l.keys), olusturma: Number(l.olusturma) || undefined, ist: l.ist && typeof l.ist === 'object' ? { ...bosIst(), ...l.ist } : bosIst() }))
    : [];
  if (!listeler.length) listeler = [{ id: 'listem', ad: 'Listem', keys: keysOku(), olusturma: Date.now(), ist: bosIst() }];
  const seciliId = listeler.some((l) => l.id === v?.seciliId) ? String(v!.seciliId) : listeler[0].id;
  return { listeler, seciliId };
}
const ilk = listelerOku();
let st: CdListeState = { keys: ilk.listeler.find((l) => l.id === ilk.seciliId)!.keys, ...ilk, ...tekrarOku(), aktif: false, aktifKey: null, dersTur: 0, listeTur: 0 };
/** Çalan ders listeden çıkarılırsa sıradaki dizin (aktifKey artık listede değil) */
let sonIdx = 0;
/** dersTur hangi derse ait (başka ders çalınca sıfırlanır) */
let dersTurKey: string | null = null;

const subs = new Set<() => void>();
const set = (p: Partial<CdListeState>) => {
  st = { ...st, ...p };
  subs.forEach((f) => f());
};
const subscribe = (f: () => void) => {
  subs.add(f);
  return () => subs.delete(f);
};
export const cdListeDurum = () => st;
export function useCdListe<T>(sel: (s: CdListeState) => T): T {
  return useSyncExternalStore(subscribe, () => sel(st), () => sel(st));
}

// Başka sekme / profil eşitlemesi değiştirirse
if (typeof window !== 'undefined') {
  window.addEventListener('storage', (e) => {
    if (e.key === LISTELER_KEY || e.key == null) {
      const l = listelerOku();
      set({ ...l, keys: l.listeler.find((x) => x.id === l.seciliId)!.keys });
    }
    if (e.key === TEKRAR_KEY || e.key == null) set(tekrarOku());
  });
}

/* ---------------- ders özetleri (sıradakine geçerken eşzamanlı gerekir) ---------------- */
let ozetler = new Map<string, CdListeDers>();
const ozetYukle = () =>
  cdListeGetir().then((ds) => {
    ozetler = new Map(ds.map((d) => [d.key, d]));
    return ozetler;
  });
async function ozet(key: string): Promise<CdOzet | null> {
  if (!ozetler.has(key)) await ozetYukle().catch(() => null);
  return ozetler.get(key) || null;
}

/* ---------------- liste düzenleme ---------------- */
function keysGuncelle(keys: string[], kaydet = true) {
  if (st.aktifKey) {
    const i = keys.indexOf(st.aktifKey);
    if (i >= 0) sonIdx = i + 1;
    else {
      // Çalan ders çıkarıldı: ondan önce kalan öge sayısı = sıradakinin yeni dizini
      const eski = st.keys.indexOf(st.aktifKey);
      if (eski >= 0) sonIdx = st.keys.slice(0, eski).filter((k) => keys.includes(k)).length;
    }
  }
  const listeler = st.listeler.map((l) => (l.id === st.seciliId ? { ...l, keys } : l));
  if (kaydet) listelerYaz(listeler, st.seciliId);
  set({ keys, listeler, ...(keys.length ? {} : { aktif: false }) });
}
function listelerYaz(listeler: CdListe[], seciliId: string) {
  yaz(LISTELER_KEY, { listeler, seciliId });
  yaz(LISTE_KEY, listeler.find((l) => l.id === seciliId)?.keys || []);
}
/* ---------------- çoklu liste ---------------- */
export function cdListeSec(id: string) {
  const l = st.listeler.find((x) => x.id === id);
  if (!l || id === st.seciliId) return;
  listelerYaz(st.listeler, id);
  // Çalan liste değişti: o anki ders sürer, bitince sıradakine geçilmez
  set({ seciliId: id, keys: l.keys, aktif: false, aktifKey: null, listeTur: 0 });
}
export function cdListeYeni(ad: string, keys: string[] = []): string {
  const id = yeniId();
  const listeler = [...st.listeler, { id, ad: ad.trim().slice(0, 40) || `Liste ${st.listeler.length + 1}`, keys: temizKeys(keys), olusturma: Date.now(), ist: bosIst() }];
  listelerYaz(listeler, st.seciliId);
  set({ listeler });
  cdListeSec(id);
  return id;
}
export function cdListeAdlandir(id: string, ad: string) {
  const a = ad.trim().slice(0, 40);
  if (!a) return;
  const listeler = st.listeler.map((l) => (l.id === id ? { ...l, ad: a } : l));
  listelerYaz(listeler, st.seciliId);
  set({ listeler });
}
/** Listeyi siler; son liste silinmez, boşaltılır */
export function cdListeSil(id: string) {
  if (st.listeler.length <= 1) return cdListeTemizle();
  const listeler = st.listeler.filter((l) => l.id !== id);
  const seciliId = id === st.seciliId ? listeler[0].id : st.seciliId;
  listelerYaz(listeler, seciliId);
  set({ listeler, seciliId, keys: listeler.find((l) => l.id === seciliId)!.keys, ...(id === st.seciliId ? { aktif: false, aktifKey: null } : {}) });
}
/* ---------------- istatistik ---------------- */
let istKirli = false;
function istEkle(p: Partial<Record<keyof CdListeIst, number>>, kaydet = false) {
  const id = st.seciliId;
  const listeler = st.listeler.map((l) => {
    if (l.id !== id) return l;
    const i = { ...bosIst(), ...l.ist };
    for (const [k, v] of Object.entries(p)) (i as any)[k] = k === 'son' ? v : ((i as any)[k] || 0) + (v || 0);
    return { ...l, ist: i };
  });
  istKirli = true;
  st = { ...st, listeler };
  if (kaydet) istYaz(); else subs.forEach((f) => f());
}
function istYaz() {
  if (!istKirli) return;
  istKirli = false;
  listelerYaz(st.listeler, st.seciliId);
  subs.forEach((f) => f());
}
// Dinleme süresi: liste çalarken oynatıcı zamanındaki ilerleme (atlama/sarma sayılmaz)
let sonT = -1;
let sonKey: string | null = null;
if (typeof window !== 'undefined') {
  cdAbone(() => {
    const c = cdDurum();
    if (!c.playing || !cdListeCaliyor()) { sonT = -1; return; }
    if (c.key !== sonKey) { sonKey = c.key; sonT = c.t; return; }
    const dt = c.t - sonT;
    sonT = c.t;
    if (dt > 0 && dt < 3) istEkle({ sn: dt, son: Date.now() });
  });
  window.setInterval(istYaz, 30000);
  window.addEventListener('pagehide', istYaz);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') istYaz(); });
}

/** Birden çok dersi seçili listenin sonuna ekler (zaten olanları atlar); eklenen sayıyı döndürür */
export function cdListeTopluEkle(keys: string[]): number {
  const yeni = temizKeys(keys).filter((k) => !st.keys.includes(k));
  if (yeni.length) keysGuncelle([...st.keys, ...yeni]);
  return yeni.length;
}
export const cdListedeMi = (key: string) => st.keys.includes(key);
export function cdListeEkle(key: string) {
  if (!cdListedeMi(key)) keysGuncelle([...st.keys, key]);
}
export function cdListeCikar(key: string) {
  if (cdListedeMi(key)) keysGuncelle(st.keys.filter((k) => k !== key));
}
export const cdListeDegistir = (key: string) => (cdListedeMi(key) ? cdListeCikar(key) : cdListeEkle(key));
export function cdListeTasi(key: string, yon: -1 | 1) {
  const i = st.keys.indexOf(key);
  const j = i + yon;
  if (i < 0 || j < 0 || j >= st.keys.length) return;
  const k = st.keys.slice();
  [k[i], k[j]] = [k[j], k[i]];
  keysGuncelle(k);
}
/** Sürükle-bırak: dersi verilen sıraya taşı */
export function cdListeKonumla(key: string, hedef: number) {
  const i = st.keys.indexOf(key);
  if (i < 0) return;
  const j = Math.max(0, Math.min(st.keys.length - 1, hedef));
  if (i === j) return;
  const k = st.keys.slice();
  k.splice(i, 1);
  k.splice(j, 0, key);
  keysGuncelle(k);
}
export function cdListeTemizle() {
  keysGuncelle([]);
}
export function cdTekrarAyarla(mod: CdTekrarMod, sayi?: CdTekrarSayi) {
  const p = { mod, sayi: sayi ?? st.sayi };
  yaz(TEKRAR_KEY, p);
  set(p);
}

/* ---------------- oynatma ---------------- */
/** Şu an çalan ders listeden mi (liste oynatması sürüyor mu)? */
export const cdListeCaliyor = (s: CdListeState = st) => s.aktif && !!s.aktifKey && cdDurum().key === s.aktifKey;

async function baslat(idx: number, takip: boolean) {
  const key = st.keys[idx];
  if (!key) return set({ aktif: false });
  const o = await ozet(key);
  if (!o) {
    // Sesi kaldırılmış ders: atla
    sonIdx = idx + 1;
    set({ aktifKey: null });
    if (idx + 1 < st.keys.length) return baslat(idx + 1, takip);
    return set({ aktif: false });
  }
  const onceki = cdDurum().key;
  dersTurKey = key;
  sonIdx = idx + 1;
  set({ aktif: true, aktifKey: key, dersTur: 0 });
  cdOynat(o, undefined, { t: 0 });
  // Önceki dersin ekranındaysa yeni dersin ekranına geç (metin/PDF sesle birlikte aksın)
  if (takip && onceki && onceki !== key && window.location.pathname === pathFor('canli_ders', onceki)) {
    navigateTo(pathFor('canli_ders', key));
  }
}

/** Listeyi baştan (ya da verilen dersten) oynat. Kullanıcı hareketi içinde çağrılmalı. */
export function cdListeOynat(baslangicKey?: string) {
  const i = baslangicKey ? Math.max(0, st.keys.indexOf(baslangicKey)) : 0;
  if (!st.keys.length) return;
  set({ listeTur: 0 });
  // Özetler önbellekteyse oynatma kullanıcı hareketiyle eşzamanlı başlar (mobil tarayıcı izni)
  if (ozetler.has(st.keys[i])) void baslat(i, false);
  else ozetYukle().then(() => baslat(i, false), () => {});
}
/** Listede önceki/sonraki ders */
export function cdListeAtla(yon: -1 | 1) {
  if (!cdListeCaliyor()) return;
  const i = st.keys.indexOf(st.aktifKey!);
  const j = (i < 0 ? sonIdx - (yon > 0 ? 1 : 0) : i) + yon;
  if (j < 0 || j >= st.keys.length) return;
  void baslat(j, true);
}
export function cdListeDurdur() {
  set({ aktif: false });
}

/** Ders sona erdi ve sırada başka ders yok: CanliDersDock soru çözücü önerisini açar */
const dersBittiBildir = (key: string) => window.dispatchEvent(new CustomEvent('cd:ders-bitti', { detail: { key } }));

function bitti() {
  const s = cdDurum();
  if (!s.key) return;
  if (dersTurKey !== s.key) {
    dersTurKey = s.key;
    set({ dersTur: 0 });
  }
  const listeden = cdListeCaliyor();
  // Ders tekrarı
  if (listeden) istEkle({ ders: 1, son: Date.now() });
  if (st.mod === 'ders' && (st.sayi === 0 || st.dersTur < st.sayi)) {
    if (listeden) istEkle({ tekrar: 1 }, true);
    set({ dersTur: st.dersTur + 1 });
    cdOynat({ key: s.key, no: s.no, baslik: s.baslik, varyantlar: s.varyantlar }, s.vid || undefined, { t: 0 });
    return;
  }
  if (!listeden) {
    set({ dersTur: 0, ...(st.aktif ? { aktif: false } : {}) });
    dersBittiBildir(s.key);
    return;
  }
  let j = st.keys.indexOf(st.aktifKey!);
  j = j < 0 ? sonIdx : j + 1;
  if (j >= st.keys.length) {
    istEkle({ tur: 1 }, true);
    try { window.dispatchEvent(new CustomEvent('cd:liste-bitti', { detail: { id: st.seciliId } })); } catch { /* yok */ }
    if (st.mod === 'liste' && st.keys.length && (st.sayi === 0 || st.listeTur < st.sayi)) {
      set({ listeTur: st.listeTur + 1 });
      j = 0;
    } else {
      set({ aktif: false, dersTur: 0 });
      dersBittiBildir(s.key);
      return;
    }
  }
  void baslat(j, true);
}
cdBitinceKaydet(bitti);

/** Liste sayfası listeyi yükleyince özetleri paylaşır (ilk oynatma eşzamanlı başlasın) */
export function cdListeOzetleri(ds: CdListeDers[]) {
  ozetler = new Map(ds.map((d) => [d.key, d]));
}

/** Liste çalıyorsa çalan dersin listedeki sırası, değilse -1 (iki depoyu birlikte izler) */
export function useCdListeSira(): number {
  const key = useSyncExternalStore(cdAbone, () => cdDurum().key, () => cdDurum().key);
  return useCdListe((s) => (s.aktif && s.aktifKey && s.aktifKey === key ? s.keys.indexOf(key) : -1));
}
