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

const PROD_HOST_SUFFIX = ['nofrostlife.com.tr'];

export function isProductionHost(): boolean {
  if (typeof window === 'undefined') return false;
  const h = window.location.hostname || '';
  if (h === 'localhost' || h === '127.0.0.1') return false;
  return PROD_HOST_SUFFIX.some((s) => h === s || h.endsWith('.' + s) || h.endsWith(s));
}

export function defaultApiBaseForThisHost(): string {
  return isProductionHost() ? ORACLE_API_URL.replace(/\/$/, '') : '';
}

/*
 * Yerel yönetim paneli → Oracle. Cihazda (localhost) /manage açıkken istekler canlı sitedeki panel gibi
 * Oracle'a gider; panelden yapılan değişiklik doğrudan canlıya yazılır. Cihazda çalışması gereken bölümler
 * (ders revize, otomasyon/betikler) yerel sunucuda kalır. Panel başlığındaki seçimle "Yerel" yapılabilir.
 */
export const PANEL_TARGET_KEY = 'medsoru_panel_hedef';
// Kişiler (kişisel veri): yerel sunucuya gider, o da Oracle'a gizli anahtarla vekillik eder (x-panel-target: oracle);
// başlıktaki e-postaya güvenen doğrudan istek Oracle'da reddedilir.
const PANEL_DEVICE_ONLY = ['/api/admin/ders-revize', '/api/automation/', '/api/admin/scripts/', '/api/admin/people', '/api/admin/hat'];

export function isLocalHost(): boolean {
  if (typeof window === 'undefined') return false;
  const h = window.location.hostname || '';
  return h === 'localhost' || h === '127.0.0.1';
}

export function getPanelTarget(): 'oracle' | 'yerel' {
  try { return localStorage.getItem(PANEL_TARGET_KEY) === 'yerel' ? 'yerel' : 'oracle'; } catch { return 'oracle'; }
}

/** Uygulama /manage'de mi açıldı (açılışta bir kez okunur: sayfadaki tüm veri aynı kaynaktan gelsin) */
export const PANEL_ON_ORACLE_AT_BOOT: boolean =
  isLocalHost() && /^\/manage(\/|$)/.test(window.location.pathname) && getPanelTarget() === 'oracle';

/** Yerel paneldeyken bu yol Oracle'a mı gider (gidiyorsa taban adres, yoksa '') */
export function panelApiBase(path?: string): string {
  if (!PANEL_ON_ORACLE_AT_BOOT) return '';
  if (path && PANEL_DEVICE_ONLY.some((p) => path.startsWith(p))) return '';
  return ORACLE_API_URL.replace(/\/$/, '');
}

// Ön eksiz `fetch('/api/...')` çağrıları da (api.ts dışındaki eski yollar) yerel panelde Oracle'a gitsin:
// yalnız localhost'ta /manage ile açılmışken, tek noktadan sarılır.
if (PANEL_ON_ORACLE_AT_BOOT && typeof window.fetch === 'function') {
  const nativeFetch = window.fetch.bind(window);
  window.fetch = (input: RequestInfo | URL, init?: RequestInit) => {
    let path: string | null = null;
    if (typeof input === 'string') path = input;
    else if (input instanceof URL && input.origin === window.location.origin) path = input.pathname + input.search;
    if (path && path.startsWith('/api/')) {
      const base = panelApiBase(path);
      if (base) {
        const headers = new Headers(init?.headers);
        // auth.ts ADMIN_EMAIL ile aynı (burada firebase'i içe aktarmamak için yazılı)
        if (!headers.has('x-admin-email')) headers.set('x-admin-email', 'nofrostlife@gmail.com');
        return nativeFetch(`${base}${path}`, { ...init, headers });
      }
    }
    return nativeFetch(input as RequestInfo, init);
  };
}
