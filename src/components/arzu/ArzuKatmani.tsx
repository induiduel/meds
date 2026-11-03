/**
 * Arzu'ya özel katman (yalnız arzuKimlik.ts'teki hesaplarda, tembel yüklenir).
 * - <html data-arzu="on">: marka simgesine kalp rozeti, ufak tema dokunuşları (arzu.css)
 * - Sekme simgesi tilki + kalp olur (çıkışta eski simge geri gelir)
 * - Karşılama ekranı: günde bir kez, siteye girdikten ~35 sn sonra (medsoru_arzu_karsilama_v1 = gün)
 * - Gezinen tilki, asılı kalp, köşeden bakan çift, fısıltı notları
 * - Klavye: metin alanı dışında "arzu" yazınca tilki geçidi + kalp yağmuru, "tilki" tek tilki, "kalp" patlama
 * - Dokunmatik: telefonu sallayınca tilki geçidi (sallama.ts), asılı kalbe uzun basınca karşılama, kalp avı (KalpAvi)
 */
import React, { useEffect, useRef, useState } from 'react';
import type { AppRoute } from '../../router';
import { ARZU_FAVICON_SVG } from './cizimler';
import { kalpPatlat } from './kalpPatlamasi';
import ArzuKarsilama from './ArzuKarsilama';
import GezinenTilki from './GezinenTilki';
import KalpAskisi from './KalpAskisi';
import CiftGizli from './CiftGizli';
import Fisiltilar from './Fisiltilar';
import KalpAvi from './KalpAvi';
import { sallamaDinle } from './sallama';
import '../../styles/arzu.css';

const KARSILAMA_KEY = 'medsoru_arzu_karsilama_v1';
const KARSILAMA_GECIKME_MS = 35_000;

const bugun = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};
const bugunGosterildi = () => { try { return localStorage.getItem(KARSILAMA_KEY) === bugun(); } catch { return false; } };
const gosterildiYaz = () => { try { localStorage.setItem(KARSILAMA_KEY, bugun()); } catch { /* depolama kapalı */ } };

function faviconDegistir(): () => void {
  const eskiler = Array.from(document.querySelectorAll<HTMLLinkElement>('link[rel="icon"]'));
  const hrefler = eskiler.map((l) => l.getAttribute('href') || '');
  const svg = eskiler.find((l) => (l.getAttribute('type') || '').includes('svg'));
  const url = `data:image/svg+xml;utf8,${encodeURIComponent(ARZU_FAVICON_SVG)}`;
  // Yalnız bir simge bırakılır: tarayıcı ilkini seçmesin diye diğerleri geçici kaldırılır
  eskiler.forEach((l) => { if (l !== svg) l.remove(); });
  let eklenen: HTMLLinkElement | null = null;
  if (svg) svg.href = url;
  else {
    eklenen = document.createElement('link');
    eklenen.rel = 'icon'; eklenen.type = 'image/svg+xml'; eklenen.href = url;
    document.head.appendChild(eklenen);
  }
  return () => {
    eklenen?.remove();
    eskiler.forEach((l, i) => { l.setAttribute('href', hrefler[i]); if (!l.isConnected) document.head.appendChild(l); });
  };
}

function metinAlanindaMi(t: EventTarget | null): boolean {
  const el = t as HTMLElement | null;
  if (!el || !el.tagName) return false;
  const tag = el.tagName.toLowerCase();
  return tag === 'input' || tag === 'textarea' || tag === 'select' || el.isContentEditable;
}

export default function ArzuKatmani({ rota }: { rota: AppRoute }) {
  const [karsilama, setKarsilama] = useState(false);
  const tampon = useRef('');

  useEffect(() => {
    document.documentElement.setAttribute('data-arzu', 'on');
    const geri = faviconDegistir();
    const sallamaBirak = sallamaDinle(); // iOS'ta izin KalpAskisi'nin ilk dokunuşunda istenir
    return () => { document.documentElement.removeAttribute('data-arzu'); geri(); sallamaBirak(); };
  }, []);

  // Günlük karşılama: siteye girdikten bir süre sonra, sekme görünürken
  useEffect(() => {
    if (bugunGosterildi()) return;
    let t = window.setTimeout(function dene() {
      if (document.visibilityState !== 'visible' || document.querySelector('[role="dialog"][aria-modal="true"]')) {
        t = window.setTimeout(dene, 15_000);
        return;
      }
      gosterildiYaz();
      setKarsilama(true);
    }, KARSILAMA_GECIKME_MS);
    return () => window.clearTimeout(t);
  }, []);

  // Klavye sürprizleri
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey || e.altKey || metinAlanindaMi(e.target)) return;
      if (e.key.length !== 1) return;
      tampon.current = (tampon.current + e.key.toLocaleLowerCase('tr')).slice(-8);
      const b = tampon.current;
      if (b.endsWith('arzu')) {
        tampon.current = '';
        window.dispatchEvent(new CustomEvent('arzu:tilki', { detail: { adet: 6 } }));
        const { innerWidth: w, innerHeight: h } = window;
        [0.25, 0.5, 0.75].forEach((x, i) => window.setTimeout(() => kalpPatlat(w * x, h * 0.42, 22, 170), i * 180));
      } else if (b.endsWith('tilki')) {
        tampon.current = '';
        window.dispatchEvent(new CustomEvent('arzu:tilki', { detail: { adet: 1 } }));
      } else if (b.endsWith('kalp')) {
        tampon.current = '';
        kalpPatlat(window.innerWidth * (0.2 + Math.random() * 0.6), window.innerHeight * (0.25 + Math.random() * 0.4), 24, 180);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  return (
    <>
      {karsilama && <ArzuKarsilama onKapat={() => setKarsilama(false)} />}
      <KalpAskisi onUcKez={() => setKarsilama(true)} />
      <GezinenTilki />
      <CiftGizli rota={rota} />
      <Fisiltilar rota={rota} />
      <KalpAvi rota={rota} />
    </>
  );
}
