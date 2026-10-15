/** Canlı ders tanıtım turu kancası: ilk ziyarette bir kez kendiliğinden açılır; "Tanıtım" düğmesiyle yeniden başlar. */
import React, { Suspense, lazy, useEffect, useState } from 'react';
import { CircleHelp } from 'lucide-react';
import { cdTurGoruldu, type CdTurTuru } from './canliDersTurDurum';

const CanliDersTur = lazy(() => import('./CanliDersTur'));

/** Tanıtım turu: ilk ziyarette bir kez kendiliğinden (hazır=true olunca), sonra "?" düğmesiyle. */
export function useCdTur(tur: CdTurTuru, hazir: boolean, bekle?: () => boolean) {
  const [acik, setAcik] = useState(false);
  useEffect(() => {
    if (!hazir || cdTurGoruldu(tur)) return;
    // Sayfa (ve ders ekranında tembel yüklenen oynatıcı) yerleşsin; en çok ~2,5 sn bekle
    let n = 0;
    const id = window.setInterval(() => {
      n += 1;
      if (n >= 10 || !bekle || bekle()) {
        window.clearInterval(id);
        if (!cdTurGoruldu(tur)) setAcik(true);
      }
    }, 250);
    return () => window.clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tur, hazir]);
  const tur_ = acik ? (
    <Suspense fallback={null}>
      <CanliDersTur tur={tur} onClose={() => setAcik(false)} />
    </Suspense>
  ) : null;
  const dugme = (
    <button type="button" className="cd-tur-btn" onClick={() => setAcik(true)} aria-label="Tanıtım turunu başlat" title="Tanıtım">
      <CircleHelp aria-hidden />
      <span>Tanıtım</span>
    </button>
  );
  return { tur: tur_, dugme };
}

