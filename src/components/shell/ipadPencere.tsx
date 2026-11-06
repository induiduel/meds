/**
 * iPad pencere kipi (Stage Manager / bölünmüş ekran) — 2026-11-06.
 * Sistem sol üste kapat/küçült/tam ekran düğmelerini çizer; sayfa bu katmanı göremez ve geri tuşumuzu kapatır.
 *  1. Algı: iPad + pencere ekranı tam kaplamıyor → :root[data-pencere="dar"] (CSS üst barı sağa kaydırır).
 *  2. Alt geri hapı: pencere kipinde (ya da öğrenilmiş cihazda) başparmak bölgesinde yüzen "‹ Geri".
 *  3. Başlık = geri: üst bar başlığına dokunmak geri götürür (shell.css .v15-top-h.is-geri).
 *  4. Yedekler: sol kenardan sağa kaydırma, Esc ve ⌘[ / Alt+←.
 *  5. Öğrenme: pencere kipinde yedek yollar 2 kez kullanıldıysa tuş erişilemiyor sayılır → hap kalıcı (localStorage).
 */
import React, { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { ChevronLeft } from 'lucide-react';

const OGREN_ANAHTAR = 'medsoru_ipad_geri_hap';
const KENAR = 24; // px: kenar kaydırması bu şeritte başlamalı

export const ipadMi = (): boolean =>
  typeof navigator !== 'undefined' &&
  (/iPad/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1));

const pencereDar = (): boolean => {
  if (!ipadMi()) return false;
  const w = window.innerWidth, h = window.innerHeight;
  const sw = Math.max(screen.width, screen.height), sh = Math.min(screen.width, screen.height);
  const yatay = w > h;
  const tamW = yatay ? sw : sh;
  const tamH = yatay ? sh : sw;
  // tarayıcı çubukları yüksekliği yer; genişlik farkı ya da çok büyük yükseklik farkı pencere demektir
  return w < tamW - 8 || h < tamH - 160;
};

const ogrenildi = (): boolean => { try { return localStorage.getItem(OGREN_ANAHTAR) === '1'; } catch { return false; } };
let yedekSayac = 0;
const yedekKullanildi = () => {
  if (document.documentElement.dataset.pencere !== 'dar') return;
  if (++yedekSayac >= 2) { try { localStorage.setItem(OGREN_ANAHTAR, '1'); } catch { /* yok */ } window.dispatchEvent(new Event('ipad-hap')); }
};

/** Görünür ilk geri düğmesine tıklar (odak ekranı dahil); yoksa tarayıcı geçmişi. */
export const geriTetikle = (yedek = true): void => {
  if (yedek) yedekKullanildi();
  const els = document.querySelectorAll<HTMLElement>('.cd15-geri button, .cd15-geri a, .v15-back');
  for (const el of els) if (el.getClientRects().length) { el.click(); return; }
  if (window.history.length > 1) window.history.back();
};

const yaziAlani = (t: EventTarget | null) =>
  t instanceof HTMLElement && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));
const pencereAcik = () => !!document.querySelector('[aria-modal="true"], [role="dialog"]:not([hidden])');

/** Kabukta bir kez çağrılır: algı + klavye + kenar kaydırması. */
export function useIpadPencere(): boolean {
  const [dar, setDar] = useState(pencereDar);
  useEffect(() => {
    const guncelle = () => {
      const d = pencereDar();
      setDar(d);
      if (d) document.documentElement.dataset.pencere = 'dar';
      else delete document.documentElement.dataset.pencere;
    };
    guncelle();
    window.addEventListener('resize', guncelle);
    window.visualViewport?.addEventListener('resize', guncelle);

    const tus = (e: KeyboardEvent) => {
      if (yaziAlani(e.target) || e.defaultPrevented) return;
      const esc = e.key === 'Escape' && !pencereAcik() && !document.fullscreenElement;
      const kose = (e.metaKey && e.key === '[') || (e.altKey && e.key === 'ArrowLeft');
      if (esc || kose) { e.preventDefault(); geriTetikle(); }
    };
    let bas: { x: number; y: number; t: number } | null = null;
    const dokun = (e: TouchEvent) => {
      const p = e.touches[0];
      // sistem kenar hareketiyle çakışmasın: en soldaki 6 px dışarıda
      bas = p && p.clientX > 6 && p.clientX < KENAR + 6 ? { x: p.clientX, y: p.clientY, t: Date.now() } : null;
    };
    const birak = (e: TouchEvent) => {
      const p = e.changedTouches[0];
      if (!bas || !p) return;
      const dx = p.clientX - bas.x, dy = Math.abs(p.clientY - bas.y);
      if (dx > 80 && dy < 50 && Date.now() - bas.t < 600 && !pencereAcik()) geriTetikle();
      bas = null;
    };
    // Başlık = geri (odak ekranları dahil): sesli ders başlığı (.cd15-baslik) kabuk dışında çizildiği için
    // .v15-top-h.is-geri yolu oraya hiç ulaşmıyordu; iPad'de başlığa dokunmak her ekranda geri götürür.
    const baslik = (e: MouseEvent) => {
      if (!ipadMi() || !(e.target instanceof Element) || !e.target.closest('.cd15-baslik')) return;
      e.preventDefault();
      geriTetikle(false);
    };
    document.addEventListener('click', baslik);
    window.addEventListener('keydown', tus);
    window.addEventListener('touchstart', dokun, { passive: true });
    window.addEventListener('touchend', birak, { passive: true });
    return () => {
      window.removeEventListener('resize', guncelle);
      window.visualViewport?.removeEventListener('resize', guncelle);
      document.removeEventListener('click', baslik);
      window.removeEventListener('keydown', tus);
      window.removeEventListener('touchstart', dokun);
      window.removeEventListener('touchend', birak);
      delete document.documentElement.dataset.pencere;
    };
  }, []);
  return dar;
}

/** Başparmak bölgesinde yüzen geri hapı; aşağı kaydırınca küçülür. */
export const IpadGeriHap: React.FC<{ goster: boolean; etiket?: string }> = ({ goster, etiket }) => {
  const [kalici, setKalici] = useState(ogrenildi);
  const [kucuk, setKucuk] = useState(false);
  useEffect(() => {
    const ogren = () => setKalici(true);
    window.addEventListener('ipad-hap', ogren);
    let son = window.scrollY;
    const kay = (e: Event) => {
      const y = e.target instanceof HTMLElement ? e.target.scrollTop : window.scrollY;
      if (Math.abs(y - son) > 12) { setKucuk(y > son); son = y; }
    };
    window.addEventListener('scroll', kay, { capture: true, passive: true });
    return () => { window.removeEventListener('ipad-hap', ogren); window.removeEventListener('scroll', kay, { capture: true }); };
  }, []);
  if (!goster || (!kalici && !ipadMi() && document.documentElement.dataset.pencere !== 'dar')) return null;
  return createPortal(
    <button type="button" className={`ipad-geri-hap print:hidden${kucuk ? ' is-kucuk' : ''}`} onClick={() => geriTetikle(false)} aria-label={etiket ? `Geri: ${etiket}` : 'Geri'}>
      <ChevronLeft aria-hidden="true" />
      <span>{etiket || 'Geri'}</span>
    </button>,
    document.body,
  );
};
