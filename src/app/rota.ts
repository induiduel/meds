/**
 * Uygulama düzeyi rota yardımcıları (2026-11-17, App.tsx'ten taşındı — davranış aynı).
 */
// Yönetim v16 kabuğu (varsayılan); eski v14 konsolu ?kabuk=v14 ile (oturum boyunca hatırlanır, ?kabuk=v16 döndürür) ve moderatörde
export const manageKabugu = (): 'v16' | 'v14' => {
  try {
    const k = new URLSearchParams(window.location.search).get('kabuk');
    if (k === 'v14' || k === 'v16') sessionStorage.setItem('medsoru_manage_kabuk', k);
    return sessionStorage.getItem('medsoru_manage_kabuk') === 'v14' ? 'v14' : 'v16';
  } catch { return 'v16'; }
};
// Yönetim ayrı girişi (manage.html, 2026-10-28): uygulama içinden /manage'e geçince tam sayfa gezinmesi yapılır ki yönetim
// kendi hafif girişiyle açılsın. Sunucu manage.html vermiyorsa (eski sunucu) döngüye girmemek için 10 sn içinde ikinci deneme yok.
let yonetimGecisBasladi = false;
export const yonetimGirisineGec = (): boolean => {
  if (yonetimGecisBasladi) return true;
  try {
    const k = 'medsoru_yonetim_gecis';
    if (Date.now() - Number(sessionStorage.getItem(k) || 0) < 10_000) return false;
    sessionStorage.setItem(k, String(Date.now()));
    const p = window.location.pathname;
    yonetimGecisBasladi = true;
    window.location.assign(/^\/manage(\/|$)/.test(p) ? p + window.location.search : '/manage');
    return true;
  } catch { return false; }
};
