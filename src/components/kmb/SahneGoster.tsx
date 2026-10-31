/**
 * KMB sahne göstericisi — bir sahnenin 3B tanımı varsa (sahne3b/sahneler3b.ts) three.js ile, yoksa SVG (`SahneCiz`) ile
 * çizer; sözleşme aynı (durum / odak / seçim / işaret). 3B motoru yalnız gerektiğinde yüklenir (React.lazy); WebGL
 * başarısız olursa o oturumda SVG'ye düşer. 3B küme 2026-11-01'de ARŞİVE alındı (kalite yetersiz bulundu): varsayılan SVG;
 * 3B yalnız `localStorage.medsoru_kmb_3b = '1'` ile (geliştirici incelemesi). Ön yüz artık 2B (SVG + Lottie) hattında sürer.
 */
import React, { Suspense, useEffect, useState } from 'react';
import { SahneCiz, type SahneDurum } from './sahneler';
import { SAHNELER3B } from './sahne3b/sahneler3b';

const Sahne3B = React.lazy(() => import('./sahne3b/Sahne3B'));
const TERCIH = 'medsoru_kmb_3b';
/** 3B deneme ARŞİVDE (2026-11-01 kullanıcı kararı): varsayılan KAPALI; yalnız localStorage medsoru_kmb_3b=1 ile açılır (geliştirici) */
export const ucBoyutTercih = () => { try { return localStorage.getItem(TERCIH) === '1'; } catch { return false; } };
export const ucBoyutAyarla = (v: boolean) => { try { localStorage.setItem(TERCIH, v ? '1' : '0'); } catch { /* özel pencere */ } window.dispatchEvent(new Event('kmb-3b')); };
export const sahne3bVar = (sahne: string) => !!SAHNELER3B[sahne];
let webglBozuk = false;

export default function SahneGoster({ sahne, durum, odak, aci, onSec, secilebilir, isaret, olcek }: {
  sahne: string; durum: SahneDurum; odak?: string | null; aci?: [number, number] | null; onSec?: (id: string) => void; secilebilir?: boolean;
  isaret?: { id: string; dogru: boolean } | null; olcek?: number;
}) {
  const [tercih, setTercih] = useState(ucBoyutTercih);
  const [hata, setHata] = useState(webglBozuk);
  useEffect(() => { const f = () => setTercih(ucBoyutTercih()); window.addEventListener('kmb-3b', f); return () => window.removeEventListener('kmb-3b', f); }, []);
  const tanim = SAHNELER3B[sahne];
  if (!tanim || !tercih || hata) return <SahneCiz sahne={sahne} durum={durum} onSec={onSec} secilebilir={secilebilir} isaret={isaret} olcek={olcek} />;
  return (
    <Suspense fallback={<SahneCiz sahne={sahne} durum={durum} />}>
      <Sahne3B tanim={tanim} durum={durum} odak={odak} aci={aci} onSec={onSec} secilebilir={secilebilir} isaret={isaret} onHata={() => { webglBozuk = true; setHata(true); }} />
    </Suspense>
  );
}
