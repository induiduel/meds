/** H424: ?bolum=<id> varsa (birleştirilen eski sayfadan yönlenme) veri yüklenince o bölüme bir kez kaydırır. */
export function bolumeKaydir(id: string, hazir: boolean): void {
  if (!hazir || new URLSearchParams(window.location.search).get('bolum') !== id) return;
  requestAnimationFrame(() => document.getElementById(id)?.scrollIntoView({ block: 'start' }));
}
