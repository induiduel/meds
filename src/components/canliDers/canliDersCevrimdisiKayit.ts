/**
 * Çevrimdışı indirilen canlı derslerin kayıt defteri (localStorage). Ana pakette durur (küçük, önbelleğe dokunmaz):
 * oynatıcı internet yokken indirilmiş sesi seçer, kapı (CanliDersDockGate) silme sorusunun zamanını buradan okur.
 * Önbellek işleri canliDersCevrimdisi.ts'te.
 */
/** Cihaza indirilen tek ses varyantı */
export interface CdCevrimdisiSes {
  vid: string;
  surum: number;
  etiket?: string;
  bayt: number;
}
export interface CdCevrimdisiKayit {
  /** İlk (birincil) ses — eski kayıtlar yalnız bunu taşır */
  vid: string;
  surum: number;
  etiket?: string;
  baslik: string;
  no: string;
  /** Toplam (sesler + PDF) */
  bayt: number;
  /** İndirilen tüm sesler (yoksa yalnız `vid`) */
  sesler?: CdCevrimdisiSes[];
  pdfler: string[];
  deckId?: string;
  at: number;
  kurul?: number;
  /** Kurul sınavı + 3 gün (ms): bundan sonra silmek için kullanıcıya sorulur */
  silinebilir?: number;
}

const KAYIT_KEY = 'medsoru_canli_ders_cevrimdisi_v1';
/** Silme sorusu: kurul → { ertele: ms (bu zamana dek sorma), bildirildi: bildirim düşüldü mü } */
const SORU_KEY = 'medsoru_canli_ders_cevrimdisi_soru_v1';
export const CD_CEVRIMDISI_DEGISTI = 'medsoru:cd-cevrimdisi';

export function cdCevrimdisiKayitlari(): Record<string, CdCevrimdisiKayit> {
  try {
    const o = JSON.parse(localStorage.getItem(KAYIT_KEY) || '{}');
    return o && typeof o === 'object' ? o : {};
  } catch {
    return {};
  }
}
export function cdCevrimdisiYaz(key: string, k: CdCevrimdisiKayit | null) {
  const all = cdCevrimdisiKayitlari();
  if (k) all[key] = k;
  else delete all[key];
  try {
    localStorage.setItem(KAYIT_KEY, JSON.stringify(all));
  } catch { /* depolama kapalı */ }
  window.dispatchEvent(new Event(CD_CEVRIMDISI_DEGISTI));
}

/** Kaydın sesleri (eski tek sesli kayıtlar dahil) */
export function cdKayitSesleri(k: CdCevrimdisiKayit | null | undefined): CdCevrimdisiSes[] {
  if (!k) return [];
  if (Array.isArray(k.sesler) && k.sesler.length) return k.sesler;
  return k.vid ? [{ vid: k.vid, surum: k.surum, etiket: k.etiket, bayt: k.bayt }] : [];
}

/**
 * İnternet yokken oynatıcının seçeceği ses: istenen adaylardan (seçilen, çalan, tercih) cihazda olan ilki,
 * yoksa cihazdaki ilk ses. İnternet varken null (oynatıcı kendi seçer).
 */
export function cdCevrimdisiVid(key: string, adaylar: (string | null | undefined)[] = []): string | null {
  if (typeof navigator === 'undefined' || navigator.onLine) return null;
  const sesler = cdKayitSesleri(cdCevrimdisiKayitlari()[key]);
  if (!sesler.length) return null;
  return adaylar.find((a) => a && sesler.some((x) => x.vid === a)) || sesler[0].vid;
}

type Soru = Record<string, { ertele?: number; bildirildi?: boolean }>;
export function cdSoruDurumu(): Soru {
  try {
    return JSON.parse(localStorage.getItem(SORU_KEY) || '{}') || {};
  } catch {
    return {};
  }
}
export function cdSoruYaz(kurul: number, p: { ertele?: number; bildirildi?: boolean }) {
  const s = cdSoruDurumu();
  s[kurul] = { ...s[kurul], ...p };
  try {
    localStorage.setItem(SORU_KEY, JSON.stringify(s));
  } catch { /* yok */ }
}

/** Silinme zamanı gelmiş (kurul + 3 gün geçmiş) ve ertelenmemiş kurullar → dersleri */
export function cdSilinebilirKurullar(now = Date.now()): Map<number, string[]> {
  const soru = cdSoruDurumu();
  const out = new Map<number, string[]>();
  for (const [key, k] of Object.entries(cdCevrimdisiKayitlari())) {
    if (!k.kurul || !k.silinebilir || now < k.silinebilir) continue;
    if ((soru[k.kurul]?.ertele || 0) > now) continue;
    out.set(k.kurul, [...(out.get(k.kurul) || []), key]);
  }
  return out;
}
