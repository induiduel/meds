import React, { useEffect, useRef, useState } from 'react';
import { ArrowUp } from 'lucide-react';

/**
 * Başa dön düğmesi: kullanıcı ~1,5 ekran aşağı inince sağ altta yaylanarak belirir (halka = sayfadaki konum).
 * Basınca sayfanın başına yumuşak kayar, sonra sayfanın araması (yoksa başlığı) odaklanır ve kısa vurgulanır.
 * Süzgeç çubukları yapışkan olmadığı için (toolbar.css) süzgeçlere dönüşün tek yolu budur.
 */
const FOCUS_SEL = 'main input[data-page-search], main .cx-dock input[type="search"], main .pt-root input, main input[type="search"], main h1';

export const ScrollTopFab: React.FC<{ routeKey: string }> = ({ routeKey }) => {
  const [on, setOn] = useState(false);
  const [going, setGoing] = useState(false);
  const [oran, setOran] = useState(0);
  const raf = useRef(0);

  useEffect(() => {
    const check = () => {
      raf.current = 0;
      const y = window.scrollY;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      setOn(y > window.innerHeight * 1.5);
      setOran(max > 0 ? Math.min(1, y / max) : 0);
    };
    const onScroll = () => { if (!raf.current) raf.current = requestAnimationFrame(check); };
    check();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    return () => {
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onScroll);
      if (raf.current) cancelAnimationFrame(raf.current);
    };
  }, [routeKey]);

  const go = () => {
    const az = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    setGoing(true);
    window.setTimeout(() => setGoing(false), 540);
    window.scrollTo({ top: 0, behavior: az ? 'auto' : 'smooth' });
    // Kaydırma bitince odak: scrollend destekli tarayıcılarda olaya, diğerlerinde süreye bağlı
    let done = false;
    const focus = () => {
      if (done) return;
      done = true;
      window.removeEventListener('scrollend', focus);
      // Dokunmatikte arama alanına odak klavyeyi açar: orada sayfa başlığına odaklanılır
      const touch = window.matchMedia?.('(pointer: coarse)').matches;
      const el = document.querySelector<HTMLElement>(touch ? 'main h1' : FOCUS_SEL);
      if (!el) return;
      if (el.tagName === 'H1' && !el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');
      el.focus({ preventScroll: true });
      const box = (el.closest('.pt-search, .cx-search, label') as HTMLElement | null) || el;
      box.classList.remove('stf-flash');
      void box.offsetWidth;
      box.classList.add('stf-flash');
      window.setTimeout(() => box.classList.remove('stf-flash'), 1000);
    };
    if (az || window.scrollY === 0) { focus(); return; }
    window.addEventListener('scrollend', focus, { once: true });
    window.setTimeout(focus, 900);
  };

  const r = 14.5;
  const c = 2 * Math.PI * r;
  return (
    <button type="button" className={`stf print:hidden${on ? ' is-on' : ''}${going ? ' is-going' : ''}`} onClick={go}
      aria-label="Sayfanın başına dön" aria-hidden={!on} tabIndex={on ? 0 : -1}>
      <span className="stf-ic">
        <svg className="stf-ring" viewBox="0 0 32 32" aria-hidden><circle cx="16" cy="16" r={r} strokeDasharray={c} strokeDashoffset={c * (1 - oran)} /></svg>
        <ArrowUp strokeWidth={2.6} aria-hidden />
      </span>
      <span className="stf-l">Başa dön</span>
    </button>
  );
};
