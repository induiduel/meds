/**
 * Canlı ders oynatıcısının kapısı (App'te her zaman bağlı, ana pakette küçük): bir ders yüklenince oynatıcı parçası
 * tembel yüklenir. Yalnız "yüklü ders var mı" değişince çizilir (çalarken App yeniden çizilmez).
 * Çevrimdışı indirilen derslerin kurulu bitip 3 gün geçtiyse silme sorusu da buradan (tembel) açılır.
 */
import React, { Suspense, lazy, useEffect, useState } from 'react';
import { useCd } from './canliDersStore';
import { cdCevrimdisiKayitlari, cdSilinebilirKurullar } from './canliDersCevrimdisiKayit';

const CanliDersDock = lazy(() => import('./CanliDersDock'));
const CevrimdisiSoru = lazy(() => import('./CanliDersCevrimdisi'));
const CozucuSoru = lazy(() => import('./CanliDersCozucuSoru'));
const Mola = lazy(() => import('./CanliDersMola'));

export function CanliDersDockGate({ activeTab, dersKey }: { activeTab: string; dersKey?: string }) {
  const var_ = useCd((s) => !!s.key);
  const [soru, setSoru] = useState(false);
  useEffect(() => {
    // Açılıştan biraz sonra ve 6 saatte bir bakılır (yalnız localStorage okur)
    const bak = () => setSoru(cdSilinebilirKurullar().size > 0);
    const t = window.setTimeout(() => {
      bak();
      // Cihazda ders varsa: güncellenen uygulamanın canlı ders parçaları da internetsiz açılsın diye önbelleğe alınır
      if (navigator.onLine && Object.keys(cdCevrimdisiKayitlari()).length) import('./canliDersCevrimdisi').then((m) => m.cdCevrimdisiOnIsit()).catch(() => {});
    }, 8000);
    const i = window.setInterval(bak, 6 * 3600_000);
    return () => { window.clearTimeout(t); window.clearInterval(i); };
  }, []);
  return (
    <>
      {var_ && (
        <Suspense fallback={null}>
          <CanliDersDock activeTab={activeTab} dersKey={dersKey} />
          <CozucuSoru />
          <Mola />
        </Suspense>
      )}
      {soru && (
        <Suspense fallback={null}>
          <CevrimdisiSoru />
        </Suspense>
      )}
    </>
  );
}
