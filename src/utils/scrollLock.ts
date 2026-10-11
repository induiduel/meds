/**
 * Ortak sayfa kaydırma kilidi (sayaçlı). Sheet, Dialog, açılır menü ve tam ekran katmanlar bunu kullanır.
 *  - İlk kilit kök öğeye `overflow: hidden` + `html.scroll-locked` yazar; son kilit açılınca geri alır.
 *    (Eski yöntem body'yi position:fixed yapıp scrollY'yi 0'a çekiyordu → üst çubuk, alt menü ve kaydırma
 *    kaydı tetiklenip açılış animasyonunun ortasında tüm sayfa yeniden hesaplanıyordu.)
 *  - Masaüstünde kaybolan kaydırma çubuğunun genişliği kadar sağ boşluk eklenir → içerik kaymaz.
 *  - Kilit sırası karışsa da (iç içe pencereler aynı anda kapanırsa) durum sayaçla doğru kalır.
 */
let count = 0;
let saved: { overflow: string; paddingRight: string } | null = null;

export function lockScroll() {
  if (typeof document === 'undefined') return;
  if (count++ > 0) return;
  const root = document.documentElement;
  const gap = window.innerWidth - root.clientWidth;
  saved = { overflow: root.style.overflow, paddingRight: document.body.style.paddingRight };
  root.style.overflow = 'hidden';
  if (gap > 0) document.body.style.paddingRight = `${gap}px`;
  root.classList.add('scroll-locked');
}

export function unlockScroll() {
  if (typeof document === 'undefined' || count === 0) return;
  if (--count > 0) return;
  const root = document.documentElement;
  root.style.overflow = saved?.overflow || '';
  document.body.style.paddingRight = saved?.paddingRight || '';
  root.classList.remove('scroll-locked');
  saved = null;
}

export const isScrollLocked = () => count > 0;
