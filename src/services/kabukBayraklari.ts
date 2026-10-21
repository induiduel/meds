/**
 * Kabuk durum bayrakları: tam ekran oynatıcı/okuyucu, dock vb. açık mı → <html> sınıfı.
 * Eskiden CSS `:root:has(...)` / `.sh-main:has(...) > *` ile yapılıyordu; o kalıp sayfadaki HER DOM değişikliğinde
 * (sesli derste kelime vurgusu, soru seçimi, yazma) tüm belgenin stilini yeniden hesaplatıyordu (2026-10-22 ölçüm:
 * tek öğe ekleme 27 ms → 0,15 ms; telefonda ~4×). MutationObserver geri çağrısı boyamadan önce (mikro görev) çalışır,
 * bayrak bir kare bile geç kalmaz. Yeni kural yazarken `:has` yerine buraya bayrak ekle.
 */
const BAYRAKLAR: [cls: string, sel: string][] = [
  // .sh-main içinde tam ekran görünüm (v12.css: kap zoom/transform sıfırlanır)
  ['kb-tam', '.sh-main :is(.ls-root, .lv-skel, .r12-root, .sr-root, .cd-ders.is-tam, .pa, .sc)'],
  // üst çubuk / yan ray / sekmeler gizlenir (v12.css, v13/shell.css)
  ['kb-gizle', ':is(.ls-root, .lv-skel, .sr-root, .cd-ders.is-tam, .pa, .sc, .r12-root.is-focus, .r12-root.is-immersive)'],
  ['kb-r12', '.r12-root'],
  ['kb-fs', ':is(.ls-root, .r12-root, .sr-root, .cd-ders.is-tam, .pa, .sc)'],
  ['kb-ls', '.ls-root'],
  ['kb-cxdock', '.cx-dock'],
  ['kb-fab', '.sh-main .ms-fab-wrap'],
  ['kb-cdtam', '.sh-main .cd-ders.is-tam'],
];

let kurulu = false;
export function installKabukBayraklari() {
  if (kurulu || typeof document === 'undefined' || typeof MutationObserver === 'undefined') return;
  kurulu = true;
  const kok = document.documentElement;
  const guncelle = () => {
    for (const [c, s] of BAYRAKLAR) {
      const var_ = !!document.querySelector(s);
      if (kok.classList.contains(c) !== var_) kok.classList.toggle(c, var_);
    }
  };
  guncelle();
  new MutationObserver(guncelle).observe(document.body || kok, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
}
