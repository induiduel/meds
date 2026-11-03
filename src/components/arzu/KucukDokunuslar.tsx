/**
 * Küçük dokunuşlar (görünmez bileşen):
 * - Boş yere çift dokunma / çift tıklama → o noktada kalp (etkileşimli ögeler ve metin alanları hariç).
 * - Uzun sayfanın sonuna inince, sayfa başına bir kez: "Buraya kadar okudun." satırı.
 * - 11:11 ve 22:22'de bir not: "Dilek tut."
 * - 40 dakika aralıksız sekme açıkken: mola tilkisi + not (sekme gizlenince sayaç sıfırlanır).
 * - Sekme arka plana gidince başlık "Tilki seni bekliyor", dönünce eski başlık.
 */
import React, { useEffect, useState } from 'react';
import type { AppRoute } from '../../router';
import { kalpPatlat } from './kalpPatlamasi';

const ETKILESIMLI = 'a, button, input, textarea, select, label, summary, [role="button"], [role="link"], [role="tab"], [contenteditable], [class^="ar-"], [class*=" ar-"]';

export default function KucukDokunuslar({ rota }: { rota: AppRoute }) {
  const [sonNot, setSonNot] = useState(false);

  // Çift dokunma kalbi
  useEffect(() => {
    let son = 0, sx = 0, sy = 0;
    const onDown = (e: PointerEvent) => {
      if (!e.isPrimary || e.button !== 0) return;
      const t = e.target as HTMLElement | null;
      if (!t || t.closest(ETKILESIMLI) || document.querySelector('[role="dialog"][aria-modal="true"]')) return;
      const now = Date.now();
      if (now - son < 320 && Math.hypot(e.clientX - sx, e.clientY - sy) < 28) {
        son = 0;
        kalpPatlat(e.clientX, e.clientY, 7, 56);
        return;
      }
      son = now; sx = e.clientX; sy = e.clientY;
    };
    document.addEventListener('pointerdown', onDown, { passive: true });
    return () => document.removeEventListener('pointerdown', onDown);
  }, []);

  // Sayfa sonu satırı (rota başına bir kez)
  useEffect(() => {
    setSonNot(false);
    let gosterildi = false, bekle: number | undefined;
    const onScroll = () => {
      if (gosterildi) return;
      const el = document.scrollingElement || document.documentElement;
      if (el.scrollHeight < window.innerHeight * 1.8) return;
      if (el.scrollTop + window.innerHeight < el.scrollHeight - 24) return;
      gosterildi = true;
      setSonNot(true);
      bekle = window.setTimeout(() => setSonNot(false), 4200);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => { window.removeEventListener('scroll', onScroll); window.clearTimeout(bekle); };
  }, [rota]);

  // 11:11 / 22:22 + 40 dakika aralıksız çalışma
  useEffect(() => {
    let dilekGunu = '';
    let baslangic = document.visibilityState === 'visible' ? Date.now() : 0;
    let molaVerildi = false;
    const tik = window.setInterval(() => {
      const d = new Date();
      const hh = d.getHours(), mm = d.getMinutes();
      const key = `${d.toDateString()}-${hh}`;
      if ((hh === 11 || hh === 22) && mm === 11 + (hh === 22 ? 11 : 0) && dilekGunu !== key && document.visibilityState === 'visible') {
        dilekGunu = key;
        window.dispatchEvent(new CustomEvent('arzu:fisilti', { detail: { metin: `${hh}:${mm}. Dilek tut.` } }));
      }
      if (baslangic && !molaVerildi && Date.now() - baslangic > 40 * 60_000 && document.visibilityState === 'visible') {
        molaVerildi = true;
        window.dispatchEvent(new CustomEvent('arzu:tilki', { detail: { adet: 1 } }));
        window.setTimeout(() => window.dispatchEvent(new CustomEvent('arzu:fisilti', { detail: { metin: 'Kırk dakika oldu. Biraz kalk, su iç, gözlerini dinlendir.' } })), 1500);
      }
    }, 15_000);
    const onVis = () => {
      if (document.visibilityState === 'visible') { baslangic = Date.now(); molaVerildi = false; }
      else baslangic = 0;
    };
    document.addEventListener('visibilitychange', onVis);
    return () => { window.clearInterval(tik); document.removeEventListener('visibilitychange', onVis); };
  }, []);

  // Sekme başlığı
  useEffect(() => {
    let eski = '';
    const onVis = () => {
      if (document.visibilityState === 'hidden') { eski = document.title; document.title = 'Tilki seni bekliyor'; }
      else if (eski) { document.title = eski; eski = ''; }
    };
    document.addEventListener('visibilitychange', onVis);
    return () => { document.removeEventListener('visibilitychange', onVis); if (eski) document.title = eski; };
  }, []);

  return sonNot ? <div className="ar-son" role="status">Buraya kadar okudun. Aferin.</div> : null;
}
