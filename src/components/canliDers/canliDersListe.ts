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

export interface CdListeState {
  keys: string[];
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

let st: CdListeState = { keys: keysOku(), ...tekrarOku(), aktif: false, aktifKey: null, dersTur: 0, listeTur: 0 };
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
    if (e.key === LISTE_KEY || e.key == null) keysGuncelle(keysOku(), false);
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
  if (kaydet) yaz(LISTE_KEY, keys);
  set({ keys, ...(keys.length ? {} : { aktif: false }) });
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
  if (st.mod === 'ders' && (st.sayi === 0 || st.dersTur < st.sayi)) {
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
