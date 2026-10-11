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
