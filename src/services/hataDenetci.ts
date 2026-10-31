/**
 * Bağlantı ve eşitleme hata denetçisi.
 *
 * Arka planda (açılışta, 90 sn'de bir, bağlantı dönünce, sekme öne gelince) cihazı yoklar; bulduğu sorunu öğrencinin
 * anlayacağı dille kaydeder ve güvenli olanları kendiliğinden onarır:
 *  - ag        : internet yok / zayıf (bilgi; bağlantı gelince kendiliğinden kapanır)
 *  - kuyruk    : gönderim kuyruğunda 3+ kez denenip gidemeyen işlem → bağlantı varsa yeniden gönderir
 *  - dusen     : sunucunun kabul etmediği işlem (eskiden sessizce silinirdi) → öğrenci "yeniden dene" diyebilir
 *  - profil    : ilerleme 10+ dk'dır gönderilemiyor ya da eşitleme hata verdi → eşitlemeyi yeniden çalıştırır
 *  - depolama  : cihaz belleği %90+ dolu / kalıcı depolama izni yok → izin ister
 *  - idb       : cihaz veritabanı açılamıyor (gizli pencere, dolu disk)
 *  - sw        : çevrimdışı çalışma katmanı (service worker) kayıtlı değil → yeniden kaydeder
 *  - saat      : cihaz saati sunucudan 5+ dk sapmış (hangi kaydın yeni olduğu karışır)
 * Kayıtlar cihazda tutulur (son 40). Panel: window.dispatchEvent(new Event('medsoru:denetci')).
 */
import { getNetState, onNetChange } from './net';
import { offlineDatabaseService, type OfflineAction } from './offlineDatabaseService';
import { dirtyKvCount } from './userKvSync';

export type Ciddiyet = 'bilgi' | 'uyari' | 'hata';
export type SorunTuru = 'ag' | 'kuyruk' | 'dusen' | 'profil' | 'depolama' | 'idb' | 'sw' | 'saat';

export interface Sorun {
  id: string;
  tur: SorunTuru;
  ciddiyet: Ciddiyet;
  baslik: string;
  /** Ne oldu, öğrencinin dilinde */
  aciklama: string;
  /** Ne yapılıyor / öğrenci ne yapabilir */
  cozum: string;
  /** Destek için teknik ayrıntı (kopyalanabilir) */
  teknik?: string;
  ilk: number;
  son: number;
  /** Kendiliğinden onarım denendiyse sonucu */
  onarim?: { at: number; ok: boolean; not: string };
  cozuldu?: number;
  /** Panelde "Onar" düğmesi gösterilsin mi */
  onarilabilir?: boolean;
  /** dusen türü: yeniden kuyruğa alınacak işlem */
  eylem?: OfflineAction;
}

const ANAHTAR = 'medsoru_hata_denetci_v1';
const AZAMI = 40;
let kayitlar: Sorun[] = oku();
const dinleyiciler = new Set<() => void>();
let sonDenetim = 0;

function oku(): Sorun[] {
  try { return JSON.parse(localStorage.getItem(ANAHTAR) || '[]'); } catch { return []; }
}
function yaz() {
  kayitlar = kayitlar.sort((a, b) => b.son - a.son).slice(0, AZAMI);
  try { localStorage.setItem(ANAHTAR, JSON.stringify(kayitlar)); } catch { /* dolu / gizli pencere */ }
  dinleyiciler.forEach((f) => f());
}

export const sorunlar = () => kayitlar;
export const acikSorunlar = () => kayitlar.filter((s) => !s.cozuldu);
export const sonDenetimZamani = () => sonDenetim;
export function denetciDinle(f: () => void) { dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; }

/** Aynı kimlikli açık sorun varsa günceller, yoksa ekler */
function bildir(s: Omit<Sorun, 'ilk' | 'son'>) {
  const now = Date.now();
  const var_ = kayitlar.find((k) => k.id === s.id && !k.cozuldu);
  if (var_) Object.assign(var_, s, { son: now });
  else kayitlar.unshift({ ...s, ilk: now, son: now });
  yaz();
}
function kapat(id: string, not?: string) {
  const s = kayitlar.find((k) => k.id === id && !k.cozuldu);
  if (!s) return;
  s.cozuldu = Date.now();
  if (not) s.onarim = { at: Date.now(), ok: true, not };
  yaz();
}
function onarimNotu(id: string, ok: boolean, not: string) {
  const s = kayitlar.find((k) => k.id === id && !k.cozuldu);
  if (s) { s.onarim = { at: Date.now(), ok, not }; yaz(); }
}

export function gecmisiTemizle() {
  kayitlar = kayitlar.filter((s) => !s.cozuldu);
  yaz();
}

/** Durum kodundan öğrencinin anlayacağı neden */
export function durumKoduAcikla(kod: number): string {
  if (kod === 401 || kod === 403) return 'Oturumun sona ermiş ya da bu işlem için yetkin yok. Çıkış yapıp yeniden girmen gerekebilir.';
  if (kod === 404) return 'İşlem yapılan kayıt (soru, yorum, ders) sunucuda artık yok; silinmiş ya da taşınmış olabilir.';
  if (kod === 409) return 'Aynı işlem başka bir cihazdan zaten yapılmış; çakışma olduğu için tekrarı kabul edilmedi.';
  if (kod === 413) return 'Gönderilen içerik çok büyük (ör. çok uzun yorum ya da büyük dosya).';
  if (kod === 422 || kod === 400) return 'Gönderilen bilgi eksik ya da hatalı biçimde olduğu için sunucu kabul etmedi.';
  if (kod === 429) return 'Kısa sürede çok fazla işlem yapıldı; sunucu biraz beklemeni istiyor.';
  if (kod >= 500) return 'Sunucuda geçici bir sorun var; senin cihazınla ilgili değil.';
  return 'Sunucu bu işlemi kabul etmedi.';
}

function islemAdi(a: OfflineAction): string {
  const ep = a.endpoint || '';
  if (/upvote|downvote/.test(ep)) return 'Beğeni';
  if (a.type === 'report' || /report/.test(ep)) return 'Hata bildirimi';
  if (a.type === 'comment' || /comments/.test(ep)) return 'Yorum';
  if (a.type === 'note') return 'Not';
  if (a.type === 'contribute') return 'Soru katkısı';
  if (a.type === 'feedback') return 'Geri bildirim';
  return 'İşlem';
}

// ── Denetimler ────────────────────────────────────────────────────────────────

function agDenetle() {
  const ag = getNetState();
  if (ag === 'online') {
    kapat('ag', 'Bağlantı geri geldi.');
    return;
  }
  bildir({
    id: 'ag',
    tur: 'ag',
    ciddiyet: ag === 'offline' ? 'uyari' : 'bilgi',
    baslik: ag === 'offline' ? 'İnternet bağlantısı yok' : 'Bağlantı zayıf',
    aciklama: ag === 'offline'
      ? 'Cihazın internete ya da sitenin sunucusuna ulaşamıyor. İndirdiğin dersler ve sorular çalışmaya devam eder.'
      : 'Sunucu yavaş yanıt veriyor; sayfalar geç açılabilir.',
    cozum: 'Yaptığın her şey bu cihazda güvende tutuluyor; bağlantı gelince kendiliğinden gönderilecek. Wi-Fi ya da mobil veriyi kontrol edebilirsin.',
  });
}

async function kuyrukDenetle(onar: boolean) {
  let rows: (OfflineAction & { id: number })[] = [];
  try { rows = await offlineDatabaseService.listQueue(); } catch { return; }
  const takili = rows.filter((r) => (r.attempts || 0) >= 3);
  if (!takili.length) {
    kapat('kuyruk', rows.length ? undefined : 'Bekleyen işlemler gönderildi.');
    return;
  }
  bildir({
    id: 'kuyruk',
    tur: 'kuyruk',
    ciddiyet: 'uyari',
    baslik: `${takili.length} işlem gönderilemiyor`,
    aciklama: `${[...new Set(takili.map(islemAdi))].join(', ')} birkaç kez denendi ama sunucuya ulaştırılamadı.`,
    cozum: getNetState() === 'online'
      ? 'Denetçi yeniden göndermeyi deniyor. Gitmezse "Gönderim kuyruğu"ndan bakıp iptal edebilirsin.'
      : 'Bağlantı gelince yeniden denenecek; bir şey yapmana gerek yok.',
    teknik: takili.map((r) => `${r.method} ${r.endpoint} · ${r.attempts} deneme`).join('\n'),
    onarilabilir: true,
  });
  if (onar && getNetState() === 'online') {
    // Bekleme sürelerini sıfırla ve hemen gönder
    await offlineDatabaseService.cancelQueued(takili.map((r) => r.id));
    await offlineDatabaseService.restoreQueued(takili);
    const r = await offlineDatabaseService.syncOfflineQueue().catch(() => null);
    const kalan = (await offlineDatabaseService.listQueue().catch(() => [])).filter((x) => (x.attempts || 0) >= 1).length;
    if (r && kalan === 0) kapat('kuyruk', `${r.synced} işlem gönderildi.`);
    else onarimNotu('kuyruk', false, 'Yeniden denendi, hâlâ gidemeyen işlem var.');
  }
}

let profilHataMetni = '';
async function profilDenetle(onar: boolean) {
  const bekleyen = dirtyKvCount();
  let son = '';
  try { son = (await import('./userDataSyncService')).getLastBackupTime(); } catch { /* yok */ }
  const gecikme = son ? Date.now() - Date.parse(son) : Infinity;
  const sorunlu = bekleyen > 0 && getNetState() === 'online' && (gecikme > 10 * 60_000 || !!profilHataMetni);
  if (!sorunlu) {
    if (bekleyen === 0) kapat('profil', 'İlerlemen hesabına yazıldı.');
    return;
  }
  bildir({
    id: 'profil',
    tur: 'profil',
    ciddiyet: profilHataMetni ? 'hata' : 'uyari',
    baslik: 'İlerlemen hesabına gönderilemedi',
    aciklama: `${bekleyen} değişiklik (çözdüğün sorular, çalışma süren, işaretlerin) yalnız bu cihazda duruyor; diğer cihazların bunları henüz göremez.`,
    cozum: 'Veriler kaybolmaz. Denetçi eşitlemeyi yeniden deniyor; sürerse çıkış yapıp yeniden giriş yapmayı dene.',
    teknik: profilHataMetni || `Son başarılı eşitleme: ${son || 'yok'}`,
    onarilabilir: true,
  });
  if (onar) {
    const { backupUserDataToDatabase } = await import('./userDataSyncService');
    const r = await backupUserDataToDatabase();
    if (r.success) { profilHataMetni = ''; kapat('profil', 'Eşitleme yeniden çalıştırıldı, ilerlemen gönderildi.'); }
    else onarimNotu('profil', false, `Yeniden denendi: ${r.error || 'olmadı'}`);
  }
}

async function depolamaDenetle(onar: boolean) {
  const st = typeof navigator !== 'undefined' ? navigator.storage : undefined;
  if (!st?.estimate) return;
  try {
    const { usage = 0, quota = 0 } = await st.estimate();
    const oran = quota ? usage / quota : 0;
    if (oran >= 0.9) {
      bildir({
        id: 'depolama-dolu',
        tur: 'depolama',
        ciddiyet: 'hata',
        baslik: 'Cihaz belleği dolmak üzere',
        aciklama: `Sitenin bu cihazda kullanabileceği alanın %${Math.round(oran * 100)}'i dolu. Yeni indirmeler ve çevrimdışı kayıtlar yazılamayabilir.`,
        cozum: 'Çevrimdışı merkezinden artık kullanmadığın ders indirmelerini sil ya da cihazda yer aç.',
        teknik: `${(usage / 1e6).toFixed(0)} MB / ${(quota / 1e6).toFixed(0)} MB`,
      });
    } else kapat('depolama-dolu', 'Bellekte yeterli yer var.');

    if (st.persisted && !(await st.persisted())) {
      bildir({
        id: 'depolama-kalici',
        tur: 'depolama',
        ciddiyet: 'bilgi',
        baslik: 'İndirmeler kalıcı değil',
        aciklama: 'Tarayıcı, cihazda yer azalınca indirdiğin dersleri ve bekleyen kayıtları kendiliğinden silebilir.',
        cozum: 'Denetçi kalıcı depolama izni istiyor. Siteyi ana ekrana eklemek de izni kalıcı yapar.',
        onarilabilir: true,
      });
      if (onar && st.persist) {
        const ok = await st.persist().catch(() => false);
        if (ok) kapat('depolama-kalici', 'Kalıcı depolama izni alındı.');
        else onarimNotu('depolama-kalici', false, 'Tarayıcı izni vermedi; siteyi ana ekrana eklersen izin kalıcı olur.');
      }
    } else kapat('depolama-kalici');
  } catch { /* desteklenmiyor */ }
}

function idbDenetle(): Promise<void> {
  if (typeof indexedDB === 'undefined') return Promise.resolve();
  return new Promise((res) => {
    let bitti = false;
    const sonuc = (ok: boolean, teknik?: string) => {
      if (bitti) return;
      bitti = true;
      if (ok) kapat('idb', 'Cihaz veritabanı açılabiliyor.');
      else bildir({
        id: 'idb',
        tur: 'idb',
        ciddiyet: 'hata',
        baslik: 'Cihaz veritabanı açılamıyor',
        aciklama: 'İnternetsizken yaptığın işlemler ve indirmeler bu cihaza kaydedilemiyor.',
        cozum: 'Gizli/özel pencere kullanıyorsan normal pencereye geç; cihaz belleği doluysa yer aç ve sayfayı yenile.',
        teknik,
      });
      res();
    };
    try {
      const r = indexedDB.open('medsoru_denetci_yoklama', 1);
      r.onsuccess = () => { try { r.result.close(); } catch { /* */ } sonuc(true); };
      r.onerror = () => sonuc(false, String(r.error?.name || r.error));
      r.onblocked = () => sonuc(true);
      setTimeout(() => sonuc(false, 'zaman aşımı (5 sn)'), 5000);
    } catch (e: any) { sonuc(false, String(e?.name || e)); }
  });
}

async function swDenetle(onar: boolean) {
  if (typeof navigator === 'undefined' || !('serviceWorker' in navigator) || location.hostname === 'localhost') return;
  const reg = await navigator.serviceWorker.getRegistration().catch(() => undefined);
  if (reg?.active) { kapat('sw', 'Çevrimdışı çalışma katmanı etkin.'); return; }
  bildir({
    id: 'sw',
    tur: 'sw',
    ciddiyet: 'uyari',
    baslik: 'Çevrimdışı çalışma kapalı',
    aciklama: 'İnternet kesilince sayfaların ve indirdiğin derslerin açılmasını sağlayan katman bu cihazda çalışmıyor.',
    cozum: 'Denetçi katmanı yeniden kuruyor. Olmazsa sayfayı bir kez yenile.',
    onarilabilir: true,
  });
  if (onar && getNetState() === 'online') {
    const { pwaService } = await import('./pwaService');
    const r = await pwaService.initServiceWorker().catch(() => null);
    if (r) kapat('sw', 'Çevrimdışı çalışma katmanı yeniden kuruldu.');
    else onarimNotu('sw', false, 'Kurulamadı; sayfayı yenilemeyi dene.');
  }
}

async function saatDenetle() {
  if (getNetState() !== 'online') return;
  try {
    const once = Date.now();
    const r = await fetch(`/api/surum?t=${once}`, { cache: 'no-store' });
    const d = r.headers.get('date');
    if (!d) return;
    const fark = Date.parse(d) + (Date.now() - once) / 2 - Date.now();
    if (Math.abs(fark) > 5 * 60_000) {
      const dk = Math.round(Math.abs(fark) / 60_000);
      bildir({
        id: 'saat',
        tur: 'saat',
        ciddiyet: 'uyari',
        baslik: 'Cihaz saati yanlış',
        aciklama: `Cihazının saati gerçek saatten yaklaşık ${dk} dakika ${fark > 0 ? 'geride' : 'ileride'}. Bu yüzden diğer cihazlarla eşitlemede hangi kaydın daha yeni olduğu karışabilir.`,
        cozum: 'Cihaz ayarlarından "Saati otomatik ayarla" seçeneğini aç.',
        teknik: `Sapma ${Math.round(fark / 1000)} sn`,
      });
    } else kapat('saat', 'Cihaz saati doğru.');
  } catch { /* bağlantı yok: ağ denetimi bildirir */ }
}

// ── Dış olaylar ───────────────────────────────────────────────────────────────

/** offlineDatabaseService: sunucunun kalıcı olarak reddettiği işlem (eskiden sessizce silinirdi) */
function dusenIslem(e: Event) {
  const { eylem, durum } = (e as CustomEvent<{ eylem: OfflineAction; durum: number }>).detail || ({} as any);
  if (!eylem) return;
  const ad = islemAdi(eylem);
  bildir({
    id: `dusen-${eylem.timestamp}-${eylem.endpoint}`,
    tur: 'dusen',
    ciddiyet: 'hata',
    baslik: `${ad} gönderilemedi`,
    aciklama: durum ? durumKoduAcikla(durum) : 'Çok kez denendi ama sunucuya ulaştırılamadı.',
    cozum: durum >= 500 || !durum
      ? 'Biraz sonra "Yeniden dene"ye basabilirsin; işlem kaybolmadı, burada saklanıyor.'
      : 'İstersen "Yeniden dene" ile bir kez daha gönderebilir ya da bu kaydı kapatabilirsin.',
    teknik: `${eylem.method} ${eylem.endpoint} → ${durum ? `HTTP ${durum}` : 'ağ hatası / deneme sınırı'}`,
    onarilabilir: true,
    eylem,
  });
}

function profilHatasi(e: Event) {
  const hata = String((e as CustomEvent<{ hata: string }>).detail?.hata || '');
  if (/Failed to fetch|NetworkError|Load failed|çevrimdışı|Çok sık/i.test(hata)) return; // geçici, kendiliğinden yeniden denenir
  profilHataMetni = hata;
  void profilDenetle(false);
}

// ── Genel ─────────────────────────────────────────────────────────────────────

let suren: Promise<void> | null = null;
/** Tüm denetimleri çalıştırır; onar=true ise güvenli onarımları da dener */
export function denetle(onar = true): Promise<void> {
  if (suren) return suren;
  suren = (async () => {
    agDenetle();
    await Promise.all([
      kuyrukDenetle(onar), profilDenetle(onar), depolamaDenetle(onar), idbDenetle(), swDenetle(onar), saatDenetle(),
    ].map((p) => p.catch(() => {})));
    sonDenetim = Date.now();
    dinleyiciler.forEach((f) => f());
  })().finally(() => { suren = null; });
  return suren;
}

/** Paneldeki "Onar" / "Yeniden dene" düğmesi */
export async function onar(id: string): Promise<void> {
  const s = kayitlar.find((k) => k.id === id && !k.cozuldu);
  if (!s) return;
  if (s.tur === 'dusen' && s.eylem) {
    await offlineDatabaseService.restoreQueued([{ ...s.eylem, id: 0 } as any]);
    kapat(id, 'Yeniden gönderim kuyruğuna alındı.');
    void offlineDatabaseService.syncOfflineQueue();
    return;
  }
  if (s.tur === 'kuyruk') return kuyrukDenetle(true);
  if (s.tur === 'profil') return profilDenetle(true);
  if (s.tur === 'depolama') return depolamaDenetle(true);
  if (s.tur === 'sw') return swDenetle(true);
  return denetle(true);
}

export function sorunuKapat(id: string) { kapat(id); }

let kuruldu = false;
export function installHataDenetci() {
  if (kuruldu || typeof window === 'undefined') return;
  kuruldu = true;
  window.addEventListener('medsoru:islem-dustu', dusenIslem);
  window.addEventListener('medsoru:esitleme-hatasi', profilHatasi);
  window.addEventListener('medsoru:user-data-synced', () => { profilHataMetni = ''; kapat('profil', 'İlerlemen hesabına yazıldı.'); });
  onNetChange(() => {
    agDenetle();
    if (getNetState() === 'online') window.setTimeout(() => void denetle(true), 3000);
  });
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && Date.now() - sonDenetim > 30_000) void denetle(true);
  });
  window.setTimeout(() => void denetle(true), 8000);
  window.setInterval(() => { if (document.visibilityState === 'visible') void denetle(true); }, 90_000);
}
