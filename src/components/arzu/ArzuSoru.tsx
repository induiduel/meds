/**
 * Bir kerelik soru (kullanıcı isteği 2026-11-06): sürprizler açık kalsın mı?
 * Cevap ne olursa olsun bir daha sorulmaz (medsoru_arzu_soru_v1, cihaza özel). Kapat → arzuKatmaniAyarla(false);
 * sonradan Ayarlar › "Küçük sürprizler" satırından geri açılabilir.
 */
import React, { useEffect, useState } from 'react';
import { arzuKatmaniAyarla } from './arzuKimlik';

const SORU_KEY = 'medsoru_arzu_soru_v1';
const soruldu = () => { try { return localStorage.getItem(SORU_KEY) === '1'; } catch { return true; } };
const isaretle = () => { try { localStorage.setItem(SORU_KEY, '1'); } catch { /* depolama kapalı */ } };

export default function ArzuSoru() {
  const [acik, setAcik] = useState(false);
  useEffect(() => {
    if (soruldu()) return;
    const t = window.setTimeout(() => setAcik(true), 2500);
    return () => window.clearTimeout(t);
  }, []);
  if (!acik) return null;
  const cevap = (kalsin: boolean) => {
    isaretle();
    setAcik(false);
    if (!kalsin) arzuKatmaniAyarla(false);
  };
  return (
    <div className="ar-soru" role="dialog" aria-modal="true" aria-labelledby="ar-soru-b">
      <div className="ar-soru-k">
        <p className="ar-soru-s" aria-hidden="true">🦊</p>
        <h2 id="ar-soru-b">Küçük sürprizler açık kalsın mı?</h2>
        <p>Sayfalarda gezinen tilki, kalpler ve küçük notlar sadece sana özel. Ders çalışırken dikkatini dağıtıyorsa kapatabilirsin; istersen Ayarlar'dan yeniden açarsın.</p>
        <div className="ar-soru-d">
          <button type="button" className="is-ikincil" onClick={() => cevap(false)}>Kapat</button>
          <button type="button" onClick={() => cevap(true)} autoFocus>Açık kalsın</button>
        </div>
      </div>
    </div>
  );
}
