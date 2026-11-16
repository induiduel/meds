/**
 * Kronometre ve çalışma kapsülünün hafif ortak parçası (2026-11-16): kabuk menüsü ve Bugün ekranı yalnız bu
 * olayları/biçimlendiriciyi kullanır; böylece KronometreV15 + KapsulV15 + kronometre.css açılış paketine girmez,
 * App.tsx'te tembel yüklenir. Bileşen `medsoru:kronometre` olayını dinler.
 */
export const sureYaz = (ms: number) => {
  const s = Math.floor(ms / 1000), sa = Math.floor(s / 3600), dk = Math.floor((s % 3600) / 60), sn = s % 60;
  const p = (n: number) => String(n).padStart(2, '0');
  return sa ? `${sa}:${p(dk)}:${p(sn)}` : `${p(dk)}:${p(sn)}`;
};
/** Menü ve kenar menüsünden açmak için */
export const kronometreAc = () => window.dispatchEvent(new CustomEvent('medsoru:kronometre', { detail: 'kronometre' }));
/** Çalışma kapsülünü (odak) açar */
export const kapsulAc = () => window.dispatchEvent(new CustomEvent('medsoru:kronometre', { detail: 'odak' }));
