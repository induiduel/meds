import React, { useEffect, useState } from 'react';
import { linkClick, navigateTo } from '../router';
import { Ikon, type IkonAd } from '../components/v16/Ikon';

/**
 * v17 kabuğu: cihaza göre üç ayrı iskelet (docs/V17_PLAN.md).
 *  - telefon (<700): üst bar yok, sayfa kendi başlığını çizer; altta yüzen koyu komut şeridi
 *  - tablet (700–1179): etiketli sol ray (açılır/kapanır)
 *  - PC (≥1180): üst yatay gezinme, yan menü yok
 * Ölçü pencere genişliğinden; bölünmüş ekranda da doğru iskelet seçilir.
 */
export type Cihaz = 'tel' | 'tab' | 'pc';
export const cihazOf = (w: number): Cihaz => (w < 700 ? 'tel' : w < 1180 ? 'tab' : 'pc');

export function useCihaz(): Cihaz {
  const [c, setC] = useState<Cihaz>(() => cihazOf(typeof window === 'undefined' ? 1280 : window.innerWidth));
  useEffect(() => {
    const f = () => setC(cihazOf(window.innerWidth));
    window.addEventListener('resize', f);
    return () => window.removeEventListener('resize', f);
  }, []);
  return c;
}

export type Bolge = 'bugun' | 'ders' | 'soru' | 'sinav' | 'basvuru';
const NAV: { id: Bolge; ad: string; kisa: string; yol: string; ikon: IkonAd }[] = [
  { id: 'bugun', ad: 'Bugün', kisa: 'Bugün', yol: '/bugun', ikon: 'ev' },
  { id: 'ders', ad: 'Ders çalış', kisa: 'Ders', yol: '/dersler', ikon: 'kitap' },
  { id: 'soru', ad: 'Soru çöz', kisa: 'Soru', yol: '/sorular', ikon: 'soru' },
  { id: 'sinav', ad: 'Sınava hazırlan', kisa: 'Sınav', yol: '/kamplar', ikon: 'hedef' },
  { id: 'basvuru', ad: 'Başvuru', kisa: 'Başvuru', yol: '/kaynaklar', ikon: 'klasor' },
];

const Bag = ({ n, aktif, cls, kisa }: { n: (typeof NAV)[number]; aktif: Bolge; cls?: string; kisa?: boolean }) => (
  <a href={n.yol} className={cls} aria-current={n.id === aktif ? 'page' : undefined} onClick={linkClick(() => navigateTo(n.yol))}>
    {cls !== 'pc' && <Ikon ad={n.ikon} />}
    {kisa ? n.kisa : n.ad}
  </a>
);

export function Kabuk({ cihaz, aktif, rayAcik = true, tam = false, children }: {
  cihaz: Cihaz; aktif: Bolge; rayAcik?: boolean; tam?: boolean; children: React.ReactNode;
}) {
  if (cihaz === 'pc') {
    return (
      <div className="k7-govde">
        {!tam && (
          <header className="k7-ustnav">
            <a href="/bugun" className="k7-marka" onClick={linkClick(() => navigateTo('/bugun'))}>MeDSor</a>
            <nav aria-label="Ana gezinme">{NAV.map((n) => <Bag key={n.id} n={n} aktif={aktif} cls="pc" />)}</nav>
            <span style={{ flex: 1 }} />
            <a href="/ayarlar" className="k7-dg2" onClick={linkClick(() => navigateTo('/ayarlar'))}>Ayarlar</a>
          </header>
        )}
        {children}
      </div>
    );
  }
  if (cihaz === 'tab') {
    return (
      <>
        {rayAcik && !tam && (
          <nav className="k7-ray k7-belir" aria-label="Ana gezinme">
            <a href="/bugun" className="k7-marka" style={{ fontSize: 15, padding: '0 0 14px', minHeight: 0, width: 'auto' }} onClick={linkClick(() => navigateTo('/bugun'))}>MeDSor</a>
            {NAV.map((n) => <Bag key={n.id} n={n} aktif={aktif} kisa />)}
          </nav>
        )}
        <div className="k7-govde">{children}</div>
      </>
    );
  }
  return (
    <div className="k7-govde">
      {children}
      {!tam && <nav className="k7-serit" aria-label="Ana gezinme">{NAV.map((n) => <Bag key={n.id} n={n} aktif={aktif} kisa />)}</nav>}
    </div>
  );
}
