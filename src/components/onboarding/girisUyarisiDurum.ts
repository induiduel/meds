/**
 * Giriş bilgilendirmesi (yapay zekâ uyarısı) durumu. Ana pakette küçük kalır; diyalog (GirisUyarisi) tembel yüklenir.
 * Kabul cihaz başınadır (profil eşitlemesine girmez: oturum değişince yeniden sorulmasın). Metin esaslı biçimde
 * değişirse SURUM artırılır → herkese bir kez daha sorulur.
 */
export const GIRIS_UYARISI_KEY = 'medsoru_giris_uyarisi_v1';
export const GIRIS_UYARISI_SURUM = 1;
/** Kabul edilince yayılır (otomatik turlar bunu bekler) */
export const GIRIS_UYARISI_KABUL_OLAYI = 'medsoru:giris-uyarisi-kabul';

export function girisUyarisiKabulEdildi(): boolean {
  try {
    const v = JSON.parse(localStorage.getItem(GIRIS_UYARISI_KEY) || 'null');
    return !!v && Number(v.surum) >= GIRIS_UYARISI_SURUM;
  } catch {
    // Depolama kapalıysa (özel pencere vb.) kabul saklanamaz: her açılışta yeniden sorulur
    return false;
  }
}

export function girisUyarisiKabulEt() {
  try {
    localStorage.setItem(GIRIS_UYARISI_KEY, JSON.stringify({ surum: GIRIS_UYARISI_SURUM, at: new Date().toISOString() }));
  } catch {
    /* depolama kapalı: bu oturumda yine de devam edilir */
  }
  window.dispatchEvent(new Event(GIRIS_UYARISI_KABUL_OLAYI));
}
