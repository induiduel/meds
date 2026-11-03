/**
 * Kalp patlaması: verilen noktadan kalpler fırlar, yerçekimiyle süzülüp söner. Web Animations API ile tek tek
 * parçacık; React'ten bağımsız (imperatif), hareket azaltılmışsa yalnız kısa bir ışıltı.
 */
import { KALP_YOLU } from './cizimler';

const RENKLER = ['#FF5C86', '#FF8FB0', '#E8306A', '#FFC2D4', '#EF7F2F', '#FFFFFF'];
const azalt = () => typeof window !== 'undefined' && !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

let kat: HTMLDivElement | null = null;
function katman(): HTMLDivElement {
  if (kat && kat.isConnected) return kat;
  kat = document.createElement('div');
  kat.className = 'ar-patlama-kat';
  kat.setAttribute('aria-hidden', 'true');
  document.body.appendChild(kat);
  return kat;
}

function kalpSvg(renk: string, boy: number): SVGSVGElement {
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('width', String(boy));
  svg.setAttribute('height', String(boy));
  const p = document.createElementNS(ns, 'path');
  p.setAttribute('d', KALP_YOLU);
  p.setAttribute('fill', renk);
  svg.appendChild(p);
  return svg;
}

/**
 * @param x,y ekran koordinatı (clientX/Y)
 * @param adet kalp sayısı
 * @param guc yayılma yarıçapı (px)
 */
export function kalpPatlat(x: number, y: number, adet = 18, guc = 150): void {
  if (typeof document === 'undefined') return;
  const k = katman();
  if (azalt()) {
    const s = kalpSvg('#FF5C86', 28);
    s.style.cssText = `position:fixed;left:${x - 14}px;top:${y - 14}px;`;
    k.appendChild(s);
    s.animate([{ opacity: 0, transform: 'scale(.6)' }, { opacity: 1, transform: 'scale(1.2)' }, { opacity: 0, transform: 'scale(1)' }], { duration: 700, easing: 'ease-out' }).onfinish = () => s.remove();
    return;
  }
  const halka = document.createElement('span');
  halka.className = 'ar-halka';
  halka.style.cssText = `left:${x}px;top:${y}px;--r:${Math.round(guc * 0.9)}px`;
  k.appendChild(halka);
  halka.animate(
    [{ transform: 'translate(-50%,-50%) scale(.1)', opacity: .9 }, { transform: 'translate(-50%,-50%) scale(1)', opacity: 0 }],
    { duration: 650, easing: 'cubic-bezier(.1,.8,.3,1)', fill: 'forwards' },
  ).onfinish = () => halka.remove();
  for (let i = 0; i < adet; i++) {
    const boy = 10 + Math.random() * 16;
    const s = kalpSvg(RENKLER[Math.floor(Math.random() * RENKLER.length)], boy);
    s.style.cssText = `position:fixed;left:${x - boy / 2}px;top:${y - boy / 2}px;will-change:transform,opacity;filter:drop-shadow(0 1px 1px rgb(0 0 0 / .15))`;
    k.appendChild(s);
    const aci = (Math.PI * 2 * i) / adet + (Math.random() - 0.5) * 0.9;
    const uz = guc * (0.45 + Math.random() * 0.75);
    const dx = Math.cos(aci) * uz;
    const dy = Math.sin(aci) * uz * 0.8;
    const dus = 70 + Math.random() * 90; // yerçekimi
    const don = (Math.random() - 0.5) * 240;
    const sure = 900 + Math.random() * 600;
    const anim = s.animate(
      [
        { transform: 'translate(0,0) scale(.3) rotate(0deg)', opacity: 1, offset: 0 },
        { transform: `translate(${dx * 0.7}px,${dy * 0.7 - 20}px) scale(1.1) rotate(${don * 0.5}deg)`, opacity: 1, offset: 0.35 },
        { transform: `translate(${dx}px,${dy + dus * 0.4}px) scale(1) rotate(${don * 0.8}deg)`, opacity: 0.9, offset: 0.7 },
        { transform: `translate(${dx * 1.08}px,${dy + dus}px) scale(.7) rotate(${don}deg)`, opacity: 0, offset: 1 },
      ],
      { duration: sure, easing: 'cubic-bezier(.2,.7,.3,1)', fill: 'forwards' },
    );
    anim.onfinish = () => s.remove();
  }
}

/** Süzülerek yukarı çıkan birkaç kalp (tilkiye dokununca): daha sakin bir efekt. */
export function kalpSuzul(x: number, y: number, adet = 5): void {
  if (typeof document === 'undefined') return;
  const k = katman();
  for (let i = 0; i < adet; i++) {
    const boy = 12 + Math.random() * 10;
    const s = kalpSvg(RENKLER[i % 4], boy);
    s.style.cssText = `position:fixed;left:${x - boy / 2 + (Math.random() - 0.5) * 30}px;top:${y - boy / 2}px;will-change:transform,opacity`;
    k.appendChild(s);
    const sal = (Math.random() - 0.5) * 40;
    const yuk = 70 + Math.random() * 60;
    const anim = s.animate(
      azalt()
        ? [{ opacity: 0 }, { opacity: 1 }, { opacity: 0 }]
        : [
            { transform: 'translate(0,0) scale(.5)', opacity: 0 },
            { transform: `translate(${sal * 0.5}px,${-yuk * 0.3}px) scale(1)`, opacity: 1, offset: 0.25 },
            { transform: `translate(${-sal * 0.4}px,${-yuk * 0.7}px) scale(1)`, opacity: 0.9, offset: 0.65 },
            { transform: `translate(${sal}px,${-yuk}px) scale(.8)`, opacity: 0 },
          ],
      { duration: 1400 + i * 160, delay: i * 90, easing: 'ease-out', fill: 'forwards' },
    );
    anim.onfinish = () => s.remove();
  }
}
