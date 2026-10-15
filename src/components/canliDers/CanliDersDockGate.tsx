/**
 * Canlı ders oynatıcısının kapısı (App'te her zaman bağlı, ana pakette küçük): bir ders yüklenince oynatıcı parçası
 * tembel yüklenir. Yalnız "yüklü ders var mı" değişince çizilir (çalarken App yeniden çizilmez).
 */
import React, { Suspense, lazy } from 'react';
import { useCd } from './canliDersStore';

const CanliDersDock = lazy(() => import('./CanliDersDock'));

export function CanliDersDockGate({ activeTab, dersKey }: { activeTab: string; dersKey?: string }) {
  const var_ = useCd((s) => !!s.key);
  if (!var_) return null;
  return (
    <Suspense fallback={null}>
      <CanliDersDock activeTab={activeTab} dersKey={dersKey} />
    </Suspense>
  );
}
