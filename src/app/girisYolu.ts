/** Giriş sayfasının adresi ve girişten sonra dönülecek iç adres (H671). Bileşenden ayrı: App bunu içe aktarınca
 *  giriş sayfasının kodu/CSS'i ana pakete girmesin. */
export const GIRIS_YOLU = '/giris';

/** `?sonra=` yalnız aynı kökende, `/giris`'in kendisi değilse kabul edilir (açık yönlendirme yok). */
export function girisSonrasiAdres(): string {
  try {
    const s = new URLSearchParams(window.location.search).get('sonra') || '/';
    return s.startsWith('/') && !s.startsWith('//') && !s.startsWith(GIRIS_YOLU) ? s : '/';
  } catch {
    return '/';
  }
}
