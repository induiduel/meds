/**
 * İstemci kimlik doğrulaması — MeDSor'un kendi kimlik sistemi (2026-11-02; Firebase Auth ve Google girişi kaldırıldı).
 *
 * Hesaplar/oturumlar Oracle meds-pg'de (sunucu: src/services/yerelKimlik.ts, jeton: kimlikDogrulama.ts).
 * Tarayıcıda `medsoru_kimlik_v1` = { user, token, exp, yenileme } tutulur. `auth` nesnesi eski Firebase Auth'un
 * projede kullanılan alt kümesini taklit eder (currentUser.getIdToken(), onAuthStateChanged, onIdTokenChanged,
 * authStateReady, signOut): çağıran dosyalar değişmeden çalışır.
 *
 * Firebase döneminden kalan hesapların uid'i aynıdır; şifre bilinmediği için kullanıcı bir kez "Şifre belirle"
 * (e-postaya 6 haneli kod) yapar, sonra tüm verisi yerinde açılır.
 */
import { claimForUser, releaseUser } from './userScope';
import { FIREBASE_DB_ENABLED } from './dbFlags';

export const ADMIN_EMAIL = 'nofrostlife@gmail.com';

export interface AppUser {
  uid: string;
  email: string | null;
  displayName: string | null;
  studentNumber?: string | null;
  photoURL?: string | null;
  congratsSentCommittees?: string[];
  isAdmin?: boolean;
}

const LOCAL_ADMIN_KEY = 'medsoru_local_admin_session';
const LOCAL_TOKEN_KEY = 'medsoru_drive_token';
const KIMLIK_KEY = 'medsoru_kimlik_v1';
export const SAVED_NAME_KEY = 'medsoru_saved_contributor_name';
export const SAVED_STUDENT_NUMBER_KEY = 'medsoru_saved_student_number';
const USER_PROFILE_CACHE_KEY = 'medsoru_user_profile_cache';

// Defensive storage wrapper that never throws in iframes or restricted environments
export const safeStorage = {
  getItem: (key: string): string | null => {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        return window.localStorage.getItem(key);
      }
    } catch (e) {}
    return null;
  },
  setItem: (key: string, value: string): void => {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.setItem(key, value);
      }
    } catch (e) {}
  },
  removeItem: (key: string): void => {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.removeItem(key);
      }
    } catch (e) {}
  }
};

/* ======================================================================
 * Oturum deposu + Firebase Auth benzeri `auth` nesnesi
 * ==================================================================== */

type SunucuHesap = { uid: string; email: string; displayName: string | null; photoURL: string | null; sifreVar?: boolean };
type Kayit = { user: SunucuHesap; token: string; exp: number; yenileme: string };

export interface KimlikKullanici {
  uid: string;
  email: string | null;
  displayName: string | null;
  photoURL: string | null;
  providerData: { providerId: string }[];
  getIdToken: (forceRefresh?: boolean) => Promise<string>;
}

type Dinleyici = (u: KimlikKullanici | null) => void;

const kayitOku = (): Kayit | null => {
  try {
    const raw = safeStorage.getItem(KIMLIK_KEY);
    const k = raw ? JSON.parse(raw) : null;
    return k?.user?.uid && k?.yenileme ? k : null;
  } catch {
    return null;
  }
};

let kayit: Kayit | null = typeof window !== 'undefined' ? kayitOku() : null;
const durumDinleyicileri = new Set<Dinleyici>();
const jetonDinleyicileri = new Set<Dinleyici>();
let hazir = false;
let hazirBekleyenler: (() => void)[] = [];

class AuthHatasi extends Error {
  code: string;
  constructor(msg: string, code = '') { super(msg); this.code = code; }
}

/** /api/kimlik/* çağrısı. Ağ hatası AuthHatasi('…', 'ag') fırlatır; sunucu hatası iletisiyle fırlatılır. */
async function kimlikIstek(yol: string, govde?: unknown, token?: string, method = 'POST'): Promise<any> {
  let r: Response;
  try {
    r = await fetch(`/api/kimlik/${yol}`, {
      method,
      headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
      body: method === 'GET' ? undefined : JSON.stringify(govde || {}),
      cache: 'no-store',
    });
  } catch {
    throw new AuthHatasi('Bağlantı kurulamadı. İnternetinizi kontrol edip tekrar deneyin.', 'ag');
  }
  let j: any = null;
  try { j = await r.json(); } catch { /* boş */ }
  if (!r.ok || !j?.ok) {
    if (r.status >= 500 && !j?.error) throw new AuthHatasi('Sunucuya ulaşılamadı. Biraz sonra tekrar deneyin.', 'ag');
    throw new AuthHatasi(j?.error || 'İşlem yapılamadı. Lütfen tekrar deneyin.', j?.kod || String(r.status));
  }
  return j;
}

function kullaniciYap(k: Kayit): KimlikKullanici {
  return {
    uid: k.user.uid,
    email: k.user.email,
    displayName: k.user.displayName,
    photoURL: k.user.photoURL,
    providerData: [{ providerId: 'password' }],
    getIdToken: (force?: boolean) => jetonAl(!!force),
  };
}

let mevcut: KimlikKullanici | null = kayit ? kullaniciYap(kayit) : null;

function yay(jetonDegisti = true) {
  for (const f of durumDinleyicileri) { try { f(mevcut); } catch (e) { console.warn(e); } }
  if (jetonDegisti) for (const f of jetonDinleyicileri) { try { f(mevcut); } catch (e) { console.warn(e); } }
}

function kayitYaz(k: Kayit | null, bildir = true) {
  const onceki = kayit?.user.uid || null;
  kayit = k;
  if (k) safeStorage.setItem(KIMLIK_KEY, JSON.stringify(k));
  else safeStorage.removeItem(KIMLIK_KEY);
  mevcut = k ? kullaniciYap(k) : null;
  if (bildir) yay(true);
  else if (onceki !== (k?.user.uid || null)) yay(true);
}

let yenilemeSurer: Promise<string> | null = null;
async function jetonAl(force: boolean): Promise<string> {
  if (!kayit) return '';
  if (!force && kayit.token && kayit.exp * 1000 - Date.now() > 120_000) return kayit.token;
  if (!yenilemeSurer) {
    const yenileme = kayit.yenileme;
    yenilemeSurer = (async () => {
      try {
        const j = await kimlikIstek('yenile', { yenileme });
        if (kayit && kayit.yenileme === yenileme) {
          kayit = { ...kayit, token: j.token, exp: j.exp, user: { ...kayit.user, ...j.user } };
          safeStorage.setItem(KIMLIK_KEY, JSON.stringify(kayit));
          mevcut = kullaniciYap(kayit);
          for (const f of jetonDinleyicileri) { try { f(mevcut); } catch { /* yok */ } }
        }
        return j.token as string;
      } catch (e: any) {
        // Ağ yoksa oturum korunur (çevrimdışı kullanım); sunucu oturumu reddettiyse çıkış yapılır.
        if (e?.code === 'ag') return kayit?.token || '';
        if (kayit && kayit.yenileme === yenileme) {
          await yerelCikis();
        }
        return '';
      } finally {
        yenilemeSurer = null;
      }
    })();
  }
  return yenilemeSurer;
}

/** Firebase Auth benzeri nesne (projede kullanılan alt küme) */
export const auth = {
  get currentUser(): KimlikKullanici | null { return mevcut; },
  onAuthStateChanged(cb: Dinleyici): () => void {
    durumDinleyicileri.add(cb);
    if (hazir) queueMicrotask(() => { if (durumDinleyicileri.has(cb)) cb(mevcut); });
    return () => { durumDinleyicileri.delete(cb); };
  },
  onIdTokenChanged(cb: Dinleyici): () => void {
    jetonDinleyicileri.add(cb);
    if (hazir) queueMicrotask(() => { if (jetonDinleyicileri.has(cb)) cb(mevcut); });
    return () => { jetonDinleyicileri.delete(cb); };
  },
  authStateReady(): Promise<void> {
    return hazir ? Promise.resolve() : new Promise((ok) => hazirBekleyenler.push(ok));
  },
  async signOut(): Promise<void> {
    const y = kayit?.yenileme;
    if (y) void kimlikIstek('cikis', { yenileme: y }).catch(() => {});
    kayitYaz(null);
  },
};

/** Firebase'in `onAuthStateChanged(auth, cb)` imzası (eski içe aktarmalar için) */
export const onAuthStateChanged = (_a: typeof auth, cb: Dinleyici) => auth.onAuthStateChanged(cb);

async function yerelCikis() {
  kayitYaz(null);
}

function hazirIsaretle() {
  if (hazir) return;
  hazir = true;
  const b = hazirBekleyenler; hazirBekleyenler = [];
  b.forEach((f) => f());
  yay(true);
}

if (typeof window !== 'undefined') {
  // İlk durum: kayıt varsa kullanıcı hemen geri yüklenir (çevrimdışı da açılır); jeton arka planda tazelenir.
  queueMicrotask(() => {
    hazirIsaretle();
    if (kayit) void jetonAl(false);
  });
  // Başka sekmede giriş/çıkış
  window.addEventListener('storage', (e) => {
    if (e.key !== KIMLIK_KEY) return;
    const yeni = kayitOku();
    if ((yeni?.user.uid || null) === (kayit?.user.uid || null)) {
      kayit = yeni; mevcut = yeni ? kullaniciYap(yeni) : null;
      return;
    }
    kayitYaz(yeni);
  });
}

/** Sunucunun döndürdüğü oturumu kaydeder ve dinleyicilere bildirir */
function oturumKaydet(j: any): KimlikKullanici {
  kayitYaz({ user: j.user, token: j.token, exp: j.exp, yenileme: j.yenileme });
  return mevcut!;
}

/* ======================================================================
 * Profil önbelleği ve sunucu profili
 * ==================================================================== */

let cachedAccessToken: string | null = safeStorage.getItem(LOCAL_TOKEN_KEY) || null;

export const rememberStudentInfo = (name: string, studentNumber?: string) => {
  if (name && name.trim()) {
    safeStorage.setItem(SAVED_NAME_KEY, name.trim());
  }
  if (studentNumber && studentNumber.trim()) {
    safeStorage.setItem(SAVED_STUDENT_NUMBER_KEY, studentNumber.trim().replace(/\D/g, ''));
  }
};

export const getRememberedStudentInfo = (): { name: string; studentNumber: string } => {
  return {
    name: safeStorage.getItem(SAVED_NAME_KEY) || '',
    studentNumber: safeStorage.getItem(SAVED_STUDENT_NUMBER_KEY) || '',
  };
};

export const loadStoredUserProfile = (uid: string): Partial<AppUser> | null => {
  try {
    const raw = safeStorage.getItem(`${USER_PROFILE_CACHE_KEY}_${uid}`);
    if (raw) return JSON.parse(raw);
  } catch (e) {}
  return null;
};

export const cacheUserProfile = (user: AppUser) => {
  try {
    safeStorage.setItem(`${USER_PROFILE_CACHE_KEY}_${user.uid}`, JSON.stringify(user));
    if (user.displayName) {
      safeStorage.setItem(SAVED_NAME_KEY, user.displayName);
    }
    if (user.studentNumber) {
      safeStorage.setItem(SAVED_STUDENT_NUMBER_KEY, user.studentNumber);
    }
  } catch (e) {}
};

/** Sunucudaki profil (data/users.json → meds-pg users); ad eski adıyla korunur (FIREBASE_DB_ENABLED yalnız tür uyumu). */
export const fetchFirestoreUserProfile = async (uid: string): Promise<Partial<AppUser> | null> => {
  void FIREBASE_DB_ENABLED;
  if (!mevcut || mevcut.uid !== uid) return null;
  try {
    const token = await mevcut.getIdToken();
    if (!token) return null;
    const r = await fetch('/api/users/me', { headers: { Authorization: `Bearer ${token}` }, cache: 'no-store' });
    if (!r.ok) return null;
    const j = await r.json();
    return j?.user || null;
  } catch {
    return null;
  }
};

export const saveFirestoreUserProfile = async (user: AppUser): Promise<void> => {
  try {
    // Kimlik jetonu: sunucu e-postayla eşleşen eski kaydı doğrulanmış uid'ye taşır.
    const idToken = mevcut?.uid === user.uid ? await mevcut.getIdToken().catch(() => '') : '';
    fetch('/api/users/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...(idToken ? { Authorization: `Bearer ${idToken}` } : {}) },
      body: JSON.stringify({
        uid: user.uid,
        email: user.email || null,
        displayName: user.displayName || null,
        studentNumber: user.studentNumber || null,
        photoURL: user.photoURL || null,
        congratsSentCommittees: user.congratsSentCommittees || [],
      }),
    }).catch(() => {});
  } catch (err) {}
};

export const setLocalAdminSession = (email: string = ADMIN_EMAIL, token?: string): AppUser => {
  const user: AppUser = {
    uid: 'local-admin-' + Date.now(),
    email,
    displayName: 'Yönetici (nofrostlife)',
    studentNumber: null,
    photoURL: null,
    congratsSentCommittees: [],
  };
  safeStorage.setItem(LOCAL_ADMIN_KEY, JSON.stringify(user));
  try { window.dispatchEvent(new Event('medsoru:admin-session')); } catch { /* sunucu */ }
  if (token) {
    cachedAccessToken = token;
    safeStorage.setItem(LOCAL_TOKEN_KEY, token);
  }
  return user;
};

export const getLocalAdminSession = (): AppUser | null => {
  try {
    const raw = safeStorage.getItem(LOCAL_ADMIN_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) {
    // ignore
  }
  return null;
};

export const clearLocalAdminSession = () => {
  safeStorage.removeItem(LOCAL_ADMIN_KEY);
  try { window.dispatchEvent(new Event('medsoru:admin-session')); } catch { /* sunucu */ }
  safeStorage.removeItem(LOCAL_TOKEN_KEY);
  cachedAccessToken = null;
};

/** Oturumdaki kişiden uygulama kullanıcısı (önbellek + hatırlanan ad/numara) */
function appUserOf(u: KimlikKullanici): AppUser {
  const cached = loadStoredUserProfile(u.uid);
  const remembered = getRememberedStudentInfo();
  return {
    uid: u.uid,
    email: u.email,
    displayName: cached?.displayName || u.displayName || remembered.name || (u.email ? u.email.split('@')[0] : null),
    studentNumber: cached?.studentNumber || remembered.studentNumber || null,
    // Kullanıcının kırptığı fotoğraf önce gelir
    photoURL: cached?.photoURL ?? u.photoURL,
    congratsSentCommittees: cached?.congratsSentCommittees || [],
  };
}

/** Sunucu profiliyle birleştirir (ad, numara, fotoğraf) */
async function sunucuProfiliyle(appUser: AppUser): Promise<AppUser | null> {
  const remote = await fetchFirestoreUserProfile(appUser.uid);
  if (!remote) return null;
  return {
    ...appUser,
    displayName: remote.displayName || appUser.displayName,
    studentNumber: remote.studentNumber || appUser.studentNumber,
    photoURL: remote.photoURL || appUser.photoURL,
    congratsSentCommittees: remote.congratsSentCommittees || appUser.congratsSentCommittees,
  };
}

export const initAuth = (
  onAuthSuccess?: (user: AppUser, token: string | null) => void,
  onAuthFailure?: () => void
) => {
  return auth.onAuthStateChanged(async (kisi) => {
    // Tarayıcıdaki kişisel veri yalnız sahibine görünür; sahip değiştiyse sayfa temiz durumla yeniden açılır.
    if (kisi ? claimForUser(kisi.uid) : releaseUser(false)) {
      await purgePersonalCaches();
      window.location.reload();
      return;
    }
    if (kisi) {
      let appUser = appUserOf(kisi);
      if (appUser.email?.toLowerCase() === ADMIN_EMAIL.toLowerCase() && !getLocalAdminSession()) {
        setLocalAdminSession(ADMIN_EMAIL);
      }
      cacheUserProfile(appUser);
      if (onAuthSuccess) onAuthSuccess(appUser, cachedAccessToken);
      sunucuProfiliyle(appUser).then((p) => {
        if (!p || mevcut?.uid !== kisi.uid) return;
        appUser = p;
        cacheUserProfile(appUser);
        if (onAuthSuccess) onAuthSuccess(appUser, cachedAccessToken);
      });
    } else {
      clearLocalAdminSession();
      cachedAccessToken = null;
      if (onAuthFailure) onAuthFailure();
    }
  });
};

/**
 * Register with Email and Password
 * Supports student number (8-12 digits) and display name.
 */
export const registerWithEmailPassword = async (
  email: string,
  pass: string,
  displayName?: string,
  studentNumber?: string
): Promise<AppUser> => {
  const cleanEmail = email.trim().toLowerCase();
  const cleanPass = pass.trim();

  if (!cleanEmail || !cleanPass) {
    throw new Error('Lütfen geçerli bir e-posta adresi ve şifre giriniz.');
  }
  if (cleanPass.length < 6) {
    throw new Error('Şifreniz en az 6 karakter olmalıdır.');
  }

  const cleanNum = studentNumber ? studentNumber.replace(/\D/g, '').slice(0, 12) : null;
  const cleanName = displayName?.trim() || cleanEmail.split('@')[0];

  const j = await kimlikIstek('kayit', { email: cleanEmail, sifre: cleanPass, ad: cleanName, ogrenciNo: cleanNum });
  const appUser: AppUser = {
    uid: j.user.uid,
    email: j.user.email,
    displayName: cleanName,
    studentNumber: cleanNum,
    photoURL: null,
    congratsSentCommittees: [],
  };
  cacheUserProfile(appUser);
  rememberStudentInfo(cleanName, cleanNum || undefined);
  oturumKaydet(j);
  await saveFirestoreUserProfile(appUser);

  // Dispatch Welcome Email automatically to registered student
  try {
    fetch('/api/send-welcome-email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: cleanEmail,
        displayName: cleanName,
        studentNumber: cleanNum || undefined,
      }),
    }).catch((e) => console.warn('Welcome email trigger error:', e));
  } catch (err) {}

  return appUser;
};

/** Hata iletisini öğrenciye gösterilecek metne çevirir (sunucu iletileri zaten Türkçe). */
export function authErrorMessage(err: any): string {
  return String(err?.message || '') || 'Giriş yapılamadı. Lütfen tekrar deneyin.';
}

/** Sunucunun "şifre belirlemelisin" yanıtı mı (Firebase'den taşınan hesap) */
export const sifreBelirlemeGerekli = (err: any): boolean => String(err?.code || '') === 'sifre-belirle';

/**
 * E-postaya 6 haneli kod gönderir: amac 'sifre' (şifre belirle / sıfırla) ya da 'giris' (şifresiz giriş).
 */
export const sendAuthCode = async (email: string, amac: 'sifre' | 'giris' = 'sifre'): Promise<string> => {
  const clean = email.trim().toLowerCase();
  if (!clean || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(clean)) {
    throw new Error('Kod için lütfen e-posta adresinizi yazın.');
  }
  const j = await kimlikIstek('kod-gonder', { email: clean, amac });
  return j.mesaj || 'Kod gönderildi.';
};

/** Kodu doğrular; amac 'sifre' ise yeni şifreyi kaydeder. Ardından oturum açılır. */
export const verifyAuthCode = async (
  email: string, kod: string, amac: 'sifre' | 'giris' = 'sifre', yeniSifre?: string,
): Promise<AppUser> => {
  const j = await kimlikIstek('kod-dogrula', { email: email.trim().toLowerCase(), kod: kod.trim(), amac, yeniSifre });
  const kisi = oturumKaydet(j);
  const appUser = appUserOf(kisi);
  cacheUserProfile(appUser);
  if (appUser.email?.toLowerCase() === ADMIN_EMAIL.toLowerCase()) setLocalAdminSession(ADMIN_EMAIL);
  return appUser;
};

/** Eski ad: e-postaya şifre belirleme kodu gönderir. */
export const sendPasswordReset = async (email: string): Promise<void> => {
  await sendAuthCode(email, 'sifre');
};

/** Açık oturumdaki hesabın şifresini belirler ya da günceller. */
export const setOrUpdateAccountPassword = async (newPassword: string): Promise<void> => {
  const cleanPass = newPassword.trim();
  if (cleanPass.length < 6) {
    throw new Error('Şifreniz en az 6 karakter olmalıdır.');
  }
  const token = mevcut ? await mevcut.getIdToken() : '';
  if (!token) throw new Error('Şifre belirlemek için önce giriş yapmalısınız.');
  await kimlikIstek('sifre', { yeniSifre: cleanPass }, token);
};

/**
 * Sign in with Email and Password
 */
export const loginWithEmailPassword = async (
  email: string,
  pass: string
): Promise<AppUser> => {
  const cleanEmail = email.trim().toLowerCase();
  const cleanPass = pass.trim();

  if (!cleanEmail || !cleanPass) {
    throw new Error('Lütfen e-posta ve şifrenizi giriniz.');
  }

  // Hata AuthHatasi olarak (code: 'sifre-belirle' | 'yok' | 'hatali' …) çağırana gider
  const j = await kimlikIstek('giris', { email: cleanEmail, sifre: cleanPass });
  const kisi = oturumKaydet(j);
  let appUser = appUserOf(kisi);
  appUser = (await sunucuProfiliyle(appUser)) || appUser;

  cacheUserProfile(appUser);
  if (appUser.email?.toLowerCase() === ADMIN_EMAIL.toLowerCase()) {
    setLocalAdminSession(ADMIN_EMAIL);
  }
  if (appUser.displayName) {
    rememberStudentInfo(appUser.displayName, appUser.studentNumber || undefined);
  }
  await saveFirestoreUserProfile(appUser);

  return appUser;
};

/**
 * Update current user's profile (name & 11-digit student number)
 */
export const updateUserProfileData = async (
  currentUser: AppUser,
  updates: {
    displayName?: string;
    studentNumber?: string;
    congratsSentCommittees?: string[];
    /** Kırpılmış profil fotoğrafı (data URL) ya da null = kaldır */
    photoURL?: string | null;
  }
): Promise<AppUser> => {
  const cleanName = updates.displayName !== undefined ? updates.displayName.trim() : currentUser.displayName;
  const cleanNumber = updates.studentNumber !== undefined
    ? updates.studentNumber.replace(/\D/g, '')
    : currentUser.studentNumber;
  const congrats = updates.congratsSentCommittees !== undefined
    ? updates.congratsSentCommittees
    : (currentUser.congratsSentCommittees || []);

  const updatedUser: AppUser = {
    ...currentUser,
    displayName: cleanName || null,
    studentNumber: cleanNumber || null,
    congratsSentCommittees: congrats,
    photoURL: updates.photoURL !== undefined ? updates.photoURL : currentUser.photoURL ?? null,
  };

  if (mevcut && mevcut.uid === currentUser.uid) {
    const degisti: Record<string, unknown> = {};
    if (cleanName && cleanName !== mevcut.displayName) degisti.ad = cleanName;
    if (updates.photoURL !== undefined) degisti.foto = updates.photoURL;
    if (Object.keys(degisti).length) {
      try {
        const token = await mevcut.getIdToken();
        if (token) await kimlikIstek('profil', degisti, token);
        if (kayit) kayitYaz({ ...kayit, user: { ...kayit.user, displayName: cleanName || null, photoURL: updatedUser.photoURL ?? null } }, false);
      } catch (e) {}
    }
  }

  cacheUserProfile(updatedUser);
  if (cleanName) {
    rememberStudentInfo(cleanName, cleanNumber || undefined);
  }
  await saveFirestoreUserProfile(updatedUser);

  return updatedUser;
};

export const getAccessToken = async (): Promise<string | null> => {
  return cachedAccessToken || safeStorage.getItem(LOCAL_TOKEN_KEY);
};

export const setCustomAccessToken = (token: string) => {
  cachedAccessToken = token.trim();
  safeStorage.setItem(LOCAL_TOKEN_KEY, cachedAccessToken);
};

/** Hizmet çalışanının API yanıt önbelleği kişisel yanıt tutabilir: oturum değişince boşaltılır. */
export const purgePersonalCaches = async () => {
  try {
    navigator.serviceWorker?.controller?.postMessage({ type: 'PURGE_DATA_CACHE' });
    const names = await caches.keys();
    await Promise.all(names.filter((n) => /data|api/i.test(n)).map((n) => caches.delete(n)));
  } catch {
    /* önbellek yok */
  }
};

export const logout = async () => {
  // Çıkmadan önce son değişiklikler hesaba gönderilir; sonra tarayıcıdaki kişisel veri silinir (sonraki öğrenci görmez).
  let sent = false;
  if (mevcut) {
    try {
      const { backupUserDataToDatabase } = await import('./userDataSyncService');
      const r = await Promise.race([backupUserDataToDatabase(), new Promise<{ success: boolean }>((ok) => setTimeout(() => ok({ success: false }), 8000))]);
      sent = !!r?.success;
    } catch {
      /* gönderilemedi: veri bu kullanıcı adına cihazda saklanır */
    }
  }
  releaseUser(sent);
  try {
    // Dinleyiciye releaseUser zaten yapıldığı için yeniden yükleme tetiklenmez (sahip artık '').
    await auth.signOut();
  } catch (e) {
    // ignore
  }
  clearLocalAdminSession();
  await purgePersonalCaches();
};

export const isAdminUser = (user: AppUser | null): boolean => {
  if (!user || !user.email) {
    return false;
  }
  return user.email.toLowerCase() === ADMIN_EMAIL.toLowerCase();
};
