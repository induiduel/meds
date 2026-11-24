/**
 * Erişim sınırı (2026-11-23, kullanıcı kararı): site YALNIZ Arzu Türk ve yönetici hesabına açıktır.
 * Diğer hesaplar giriş yapabilir (kayıt açık kalır) ama uygulamaya giremez: hata sayfası görür, sunucu
 * veri uçlarına 403 döner, hiçbir veri/ses/görsel indirilmez.
 *
 * TEK KAYNAK: izinli e-posta listesi buradadır; sunucu kapısı (src/services/erisimKapisi.ts) ve istemci
 * ekranı (App.tsx, main.tsx) aynı listeyi okur. İkinci bir liste yazmak YASAK (H320–H329 dersi: aynı kural
 * beş ayrı yerden düzenlenince tutarsız kalıyordu).
 *
 * Bu dosya BAĞIMSIZDIR (express/fs/window zorunlu değil): sunucu da, tarayıcı da içe aktarabilir.
 */

/** Girişine izin verilen hesaplar (küçük harf): Arzu Türk'ün iki hesabı + ana yönetici. Ayrıca kullanıcı kaydında
 *  rolü 'admin' olan hesap (sunucu: rolIzinli). Moderatör rolü GİRMEZ (2026-11-24 kullanıcı kararı). Liste yalnız
 *  e-postası doğrulanmış hesaba işler (sunucu: epostaDogrulandi). Sınama botları imzalı ai-test çereziyle girer. */
export const ERISIM_EPOSTALARI: readonly string[] = [
  'arzuturk361@gmail.com',
  'drarzuturk@gmail.com',
  'nofrostlife@gmail.com',
];

const IZINLI = new Set(ERISIM_EPOSTALARI.map((e) => e.trim().toLowerCase()));

/** E-posta izinli mi (boş e-posta izinli sayılmaz). */
export function erisimEpostasiIzinli(email: string | null | undefined): boolean {
  const e = String(email || '').trim().toLowerCase();
  if (!e) return false;
  return IZINLI.has(e);
}

export const ERISIM_KAPALI_KODU = 'INTERNAL_ERROR';

/** Kapalı ekranda gösterilen metin (tek kaynak; sunucu 403 gövdesi de bunu kullanır). */
export const ERISIM_KAPALI_MESAJI = 'Sunucu hatası. İstek işlenemedi.';

/* ---------------- Tarayıcı tarafı: oturum açık mı, engelli mi ---------------- */

/** auth.ts ile aynı anahtarlar (auth.ts tarayıcı bağımlılıkları taşıdığı için buradan içe aktarılmaz). */
const KIMLIK_ANAHTARI = 'medsoru_kimlik_v1';
const YEREL_YONETICI_ANAHTARI = 'medsoru_local_admin_session';

function oku(anahtar: string): any {
  try {
    if (typeof window === 'undefined' || !window.localStorage) return null;
    const raw = window.localStorage.getItem(anahtar);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

/**
 * Rol izni önbelleği (2026-11-24): listede olmayan ama sunucuda rolü moderatör/yönetici olan hesap.
 * Rol /api/me/access'ten öğrenilir ve e-postayla bağlı saklanır; asıl denetim sunucudadır (erisimKapisi.ts).
 */
const ROL_ANAHTARI = 'medsoru_erisim_rol_v1';

export function rolIzniKaydet(email: string | null | undefined, izinli: boolean): void {
  try {
    if (typeof window === 'undefined' || !window.localStorage) return;
    const e = String(email || '').trim().toLowerCase();
    if (izinli && e) window.localStorage.setItem(ROL_ANAHTARI, JSON.stringify({ email: e }));
    else window.localStorage.removeItem(ROL_ANAHTARI);
  } catch { /* depolama yok */ }
}

export function rolIzniVar(email: string | null | undefined): boolean {
  const e = String(email || '').trim().toLowerCase();
  return !!e && oku(ROL_ANAHTARI)?.email === e;
}

/** Liste ya da önbellekteki rol izni */
export function erisimIzinliMi(email: string | null | undefined): boolean {
  return erisimEpostasiIzinli(email) || rolIzniVar(email);
}

/**
 * Cihazdaki oturum engelli mi (senkron; ilk boyamadan önce veri isteği başlamasın diye localStorage'dan okur).
 * Oturum yoksa false: oturumsuz ziyaretçiyi kapı (Onboarding) karşılar; sunucu yine veri vermez.
 */
export function erisimEngelliMi(): boolean {
  const kimlik = oku(KIMLIK_ANAHTARI);
  const email = kimlik?.user?.email;
  if (email) return !erisimIzinliMi(email);
  const yerel = oku(YEREL_YONETICI_ANAHTARI);
  if (yerel?.email) return !erisimIzinliMi(yerel.email);
  return false;
}
