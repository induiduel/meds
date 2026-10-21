/**
 * adminFetchAuth.ts — oturum açmış yönetici için API isteklerine Firebase kimlik jetonu ekler (2026-10-20).
 *
 * Sunucu artık `x-admin-email` başlığına güvenmez (src/services/adminAuth.ts); tarayıcıdaki yönetici
 * `Authorization: Bearer <idToken>` ile doğrulanır. Jeton YALNIZ kendi API'mize gider: aynı köken /api/...,
 * ORACLE_API_URL ya da kullanıcının ayarladığı özel API adresi. Üçüncü taraf kökenlere asla eklenmez.
 * Zaten Authorization taşıyan isteğe dokunulmaz. main.tsx'te uygulama başlamadan kurulur.
 */
import { ORACLE_API_URL } from '../config/deployment';

const ADMIN = 'nofrostlife@gmail.com';
const CUSTOM_API_KEY = 'medsoru_custom_api_url';

function originOf(u: string): string {
  try { return new URL(u).origin; } catch { return ''; }
}

function apiOrigins(): Set<string> {
  const s = new Set<string>([window.location.origin]);
  const o = originOf(ORACLE_API_URL);
  if (o) s.add(o);
  try {
    const c = localStorage.getItem(CUSTOM_API_KEY) || '';
    const co = c ? originOf(c) : '';
    if (co) s.add(co);
  } catch { /* */ }
  return s;
}

function isOurApi(input: RequestInfo | URL): boolean {
  let raw: string;
  if (typeof input === 'string') raw = input;
  else if (input instanceof URL) raw = input.href;
  else if (typeof Request !== 'undefined' && input instanceof Request) raw = input.url;
  else return false;
  let u: URL;
  try { u = new URL(raw, window.location.href); } catch { return false; }
  if (!u.pathname.startsWith('/api/')) return false;
  return apiOrigins().has(u.origin);
}

/**
 * Öğrenci jetonu (2026-10-20, başarım): giriş yapmış her öğrencinin yazma istekleri (POST/PUT/PATCH/DELETE) ve
 * /api/basarim/* istekleri de jeton taşır; sunucu topluluk eylemlerini (soru, yorum, beğeni …) doğrulanmış kişiye yazar.
 */
function ogrenciJetonu(input: RequestInfo | URL, init?: RequestInit): boolean {
  const m = String(init?.method || (typeof Request !== 'undefined' && input instanceof Request ? input.method : 'GET')).toUpperCase();
  if (m !== 'GET' && m !== 'HEAD') return true;
  const raw = typeof input === 'string' ? input : input instanceof URL ? input.href : (input as Request).url;
  // Okuma isteklerinden yalnız jeton gerektirenler: başarım ve ATP kilitli içerik (olası sorular)
  try { return /^\/api\/(basarim|olasi-sorular)\//.test(new URL(raw, window.location.href).pathname); } catch { return false; }
}

let installed = false;

export function installAdminFetchAuth() {
  if (installed || typeof window === 'undefined' || typeof window.fetch !== 'function') return;
  installed = true;
  const inner = window.fetch.bind(window);
  window.fetch = async (input: RequestInfo | URL, init?: RequestInit) => {
    try {
      if (isOurApi(input)) {
        const { auth } = await import('./auth');
        const user = auth?.currentUser;
        if (user && (String(user.email || '').toLowerCase() === ADMIN || ogrenciJetonu(input, init))) {
          const base = init?.headers ?? (typeof Request !== 'undefined' && input instanceof Request ? input.headers : undefined);
          const headers = new Headers(base);
          if (!headers.has('Authorization')) {
            const token = await user.getIdToken();
            if (token) {
              headers.set('Authorization', `Bearer ${token}`);
              return inner(input, { ...init, headers });
            }
          }
        }
      }
    } catch {
      /* jeton alınamazsa istek jetonsuz gider (yerelde loopback, canlıda geçiş kipinde eski yol) */
    }
    return inner(input, init);
  };
}

/** EventSource başlık taşıyamaz: yönetici jetonu canlı olay akışının adresine eklenir (yalnız /api/realtime/events kabul eder). */
let cachedToken = '';
let tokenWatch = false;
export function adminIdTokenForStream(): string {
  if (!tokenWatch && typeof window !== 'undefined') {
    tokenWatch = true;
    void import('./auth').then(({ auth }) => {
      auth?.onIdTokenChanged?.(async (u: any) => {
        const had = !!cachedToken;
        cachedToken = u && String(u.email || '').toLowerCase() === ADMIN ? await u.getIdToken().catch(() => '') : '';
        // İlk jeton gelince canlı akış yönetici olaylarıyla yeniden kurulsun
        if (!had && cachedToken) window.dispatchEvent(new Event('medsoru:admin-session'));
      });
    }).catch(() => {});
  }
  return cachedToken;
}
