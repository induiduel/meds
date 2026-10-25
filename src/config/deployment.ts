/**
 * deployment.ts — tek yerden dağıtım adresleri.
 *
 * - Cihazda (localhost): getCustomApiUrl() boş döner, aynı-köken /api kullanılır.
 * - Canlıda (nofrostlife.com.tr): kullanıcı özel URL girmediyse
 *   Oracle üzerindeki Named Tunnel adresine düşülür.
 * - Build sırasında VITE_ORACLE_API_URL verilirse o ezberlenir, yoksa
 *   aşağıdaki varsayılan kullanılır.
 */
export const ORACLE_API_URL: string =
  ((import.meta as any)?.env?.VITE_ORACLE_API_URL as string) ||
  'https://api.nofrostlife.com.tr';

export const DEFAULT_LOCAL_SERVER_URL = 'http://192.168.1.46:3000';
export const LOCAL_SERVER_URL_KEY = 'medsoru_local_server_url';
export const PANEL_SECRET_STORAGE_KEY = 'medsoru_panel_secret';
export const HYBRID_BRIDGE_KEY = 'medsoru_hybrid_local_bridge';
export const ADMIN_APP_MODE_KEY = 'medsoru_admin_app_mode';

const PROD_HOST_SUFFIX = ['nofrostlife.com.tr'];

/** Capacitor (Android / iOS yerel kabuğu) içinde mi çalışıyor */
export function isCapacitorNative(): boolean {
  if (typeof window === 'undefined') return false;
  const w = window as any;
  if (w.Capacitor?.isNativePlatform?.()) return true;
  const p = window.location.protocol || '';
  return p === 'capacitor:' || p === 'ionic:';
}

/** MeDSor Yönetim Android uygulaması kipi (Capacitor yerel kabuğu ya da ?adminApp=1 / kayıtlı bayrak) */
export function isAdminAppMode(): boolean {
  if (typeof window === 'undefined') return false;
  if (isCapacitorNative()) return true;
  try {
    const sp = new URLSearchParams(window.location.search);
    if (sp.get('adminApp') === '1') {
      localStorage.setItem(ADMIN_APP_MODE_KEY, '1');
      return true;
    }
    if (sp.get('adminApp') === '0') {
      localStorage.removeItem(ADMIN_APP_MODE_KEY);
      return false;
    }
    return localStorage.getItem(ADMIN_APP_MODE_KEY) === '1';
  } catch {
    return false;
  }
}

export function getLocalServerUrl(): string {
  if (typeof localStorage === 'undefined') return DEFAULT_LOCAL_SERVER_URL;
  try {
    const v = (localStorage.getItem(LOCAL_SERVER_URL_KEY) || '').trim().replace(/\/$/, '');
    return v || DEFAULT_LOCAL_SERVER_URL;
  } catch {
    return DEFAULT_LOCAL_SERVER_URL;
  }
}

export function setLocalServerUrl(url: string): void {
  try {
    const clean = url.trim().replace(/\/$/, '');
    if (clean) localStorage.setItem(LOCAL_SERVER_URL_KEY, clean);
    else localStorage.removeItem(LOCAL_SERVER_URL_KEY);
  } catch { /* */ }
}

export function getStoredPanelSecret(): string {
  if (typeof localStorage === 'undefined') return '';
  try {
    return (localStorage.getItem(PANEL_SECRET_STORAGE_KEY) || '').trim();
  } catch {
    return '';
  }
}

export function setStoredPanelSecret(secret: string): void {
  try {
    const clean = secret.trim();
    if (clean) localStorage.setItem(PANEL_SECRET_STORAGE_KEY, clean);
    else localStorage.removeItem(PANEL_SECRET_STORAGE_KEY);
    if (typeof window !== 'undefined') window.dispatchEvent(new Event('medsoru:admin-session'));
  } catch { /* */ }
}

/** Hibrit köprü: Canlı (Oracle) hedefindeyken cihaza özel uçları (hat, betikler, otomasyon) yerel sunucuya yönlendir */
export function isHybridBridgeEnabled(): boolean {
  try {
    return localStorage.getItem(HYBRID_BRIDGE_KEY) === '1';
  } catch {
    return false;
  }
}

export function setHybridBridgeEnabled(on: boolean): void {
  try {
    localStorage.setItem(HYBRID_BRIDGE_KEY, on ? '1' : '0');
  } catch { /* */ }
}

export function isProductionHost(): boolean {
  if (typeof window === 'undefined') return false;
  if (isCapacitorNative()) return true;
  const h = window.location.hostname || '';
  if (h === 'localhost' || h === '127.0.0.1') return false;
  return PROD_HOST_SUFFIX.some((s) => h === s || h.endsWith('.' + s) || h.endsWith(s));
}

export function defaultApiBaseForThisHost(path?: string): string {
  if (isCapacitorNative() || !isLocalHost()) {
    const target = getPanelTarget();
    if (target === 'yerel') {
      return getLocalServerUrl();
    }
    if (path && isHybridBridgeEnabled() && isStrictDeviceOnlyPath(path)) {
      return getLocalServerUrl();
    }
    if (isProductionHost() || isCapacitorNative()) {
      return ORACLE_API_URL.replace(/\/$/, '');
    }
  }
  return '';
}

/*
 * Yerel yönetim paneli → Oracle. Cihazda (localhost) /manage açıkken istekler canlı sitedeki panel gibi
 * Oracle'a gider; panelden yapılan değişiklik doğrudan canlıya yazılır. Cihazda çalışması gereken bölümler
 * (ders revize, otomasyon/betikler) yerel sunucuda kalır. Panel başlığındaki seçimle "Yerel" yapılabilir.
 */
export const PANEL_TARGET_KEY = 'medsoru_panel_hedef';
// Kişiler (kişisel veri): yerel sunucuya gider, o da Oracle'a gizli anahtarla vekillik eder (x-panel-target: oracle);
// başlıktaki e-postaya güvenen doğrudan istek Oracle'da reddedilir.
const PANEL_DEVICE_ONLY = ['/api/admin/ders-revize', '/api/automation/', '/api/admin/scripts/', '/api/admin/people', '/api/admin/hat', '/api/admin/pg/', '/api/admin/servis/'];
// Yalnız yerel makinede çalışabilen veya hibrit köprüyle yerel sunucuya gidebilen uçlar:
const STRICT_DEVICE_ONLY = ['/api/admin/ders-revize', '/api/automation/', '/api/admin/scripts/', '/api/admin/hat'];

export function isStrictDeviceOnlyPath(path?: string): boolean {
  return Boolean(path && STRICT_DEVICE_ONLY.some((p) => path.startsWith(p)));
}

export function isLocalHost(): boolean {
  if (typeof window === 'undefined') return false;
  if (isCapacitorNative()) return false;
  const h = window.location.hostname || '';
  return h === 'localhost' || h === '127.0.0.1';
}

/** Canlı ↔ Yerel geçiş düğmesi masaüstü localhost'ta ve mobil yönetim uygulamasında açıktır */
export function canSwitchPanelTarget(): boolean {
  if (isLocalHost() || isCapacitorNative() || isAdminAppMode()) return true;
  try {
    return Boolean(localStorage.getItem(LOCAL_SERVER_URL_KEY) || localStorage.getItem(PANEL_SECRET_STORAGE_KEY));
  } catch {
    return false;
  }
}

export function getPanelTarget(): 'oracle' | 'yerel' {
  try { return localStorage.getItem(PANEL_TARGET_KEY) === 'yerel' ? 'yerel' : 'oracle'; } catch { return 'oracle'; }
}

/** Uygulama /manage'de mi açıldı (açılışta bir kez okunur: sayfadaki tüm veri aynı kaynaktan gelsin) */
export const PANEL_ON_ORACLE_AT_BOOT: boolean =
  isLocalHost() && /^\/manage(\/|$)/.test(window.location.pathname) && getPanelTarget() === 'oracle';

/** Yerel paneldeyken bu yol Oracle'a mı gider (yerel sunucunun vekili üzerinden: x-panel-proxy / ?panelProxy=oracle) */
export function panelProxied(path?: string): boolean {
  if (!PANEL_ON_ORACLE_AT_BOOT) return false;
  return !(path && PANEL_DEVICE_ONLY.some((p) => path.startsWith(p)));
}

/**
 * Eskiden Oracle taban adresi dönerdi (tarayıcı doğrudan Oracle'a x-admin-email ile giderdi). 2026-10-20'den beri
 * yerel panel istekleri aynı kökende kalır; yerel sunucu gerçek loopback isteğini gizli anahtarla Oracle'a iletir
 * (src/services/adminAuth.ts panelOracleProxyMiddleware). Mobil uygulamada (Capacitor) ya da uzaktan yerel sunucu
 * seçildiğinde doğrudan hedef sunucu taban adresini döndürür.
 */
export function panelApiBase(path?: string): string {
  if (isCapacitorNative() || (!isLocalHost() && getPanelTarget() === 'yerel')) {
    return defaultApiBaseForThisHost(path);
  }
  if (!isLocalHost() && path && isHybridBridgeEnabled() && isStrictDeviceOnlyPath(path)) {
    return getLocalServerUrl();
  }
  return '';
}

// Ön eksiz `fetch('/api/...')` çağrıları:
// 1) Masaüstü localhost'ta /manage açıkken aynı kökende kalır, `x-panel-proxy: oracle` eklenir.
// 2) Capacitor Android uygulamasında (veya uzaktan Yerel/Hibrit sunucu seçiliyse) `/api/...` göreli adresi
//    doğrudan hedef sunucu adresiyle (Oracle veya Yerel Sunucu) birleştirilir.
if (typeof window !== 'undefined' && typeof window.fetch === 'function') {
  const nativeFetch = window.fetch.bind(window);
  window.fetch = (input: RequestInfo | URL, init?: RequestInit) => {
    let path: string | null = null;
    if (typeof input === 'string') {
      if (input.startsWith('/')) path = input;
      else if (input.startsWith(window.location.origin + '/')) path = input.slice(window.location.origin.length);
    } else if (input instanceof URL && input.origin === window.location.origin) {
      path = input.pathname + input.search;
    }
    if (path && path.startsWith('/api/')) {
      if (PANEL_ON_ORACLE_AT_BOOT && panelProxied(path)) {
        const headers = new Headers(init?.headers);
        headers.set('x-panel-proxy', 'oracle');
        return nativeFetch(path, { ...init, headers });
      }
      const remoteBase = panelApiBase(path) || (isCapacitorNative() ? defaultApiBaseForThisHost(path) : '');
      if (remoteBase) {
        return nativeFetch(`${remoteBase.replace(/\/$/, '')}${path}`, init);
      }
    }
    return nativeFetch(input as RequestInfo, init);
  };
}
