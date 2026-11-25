import { Suspense, useEffect, useState } from 'react';
import { guvenliLazy } from '../utils/guvenliLazy';
import { Kabuk, useCihaz } from './Kabuk';
import './v17.css';

/**
 * v17 kökü: v15 kabuğunun üstünde tam ekran katman (App.tsx yalnız v17Acik + V17_ROTALAR iken bağlar).
 * Kök öğeye data-v17-ekran yazar (v15 kabuğu gizlenir, altta bağlı kalır); yazı tiplerini yalnız burada yükler;
 * temayı uygulamanın açık/sepya/koyu kipinden alır.
 */
const Bugun = guvenliLazy(() => import('./Bugun'));
const SesliDers = guvenliLazy(() => import('./SesliDers'));

const FONT_ID = 'v17-yazi-tipleri';
const FONT_URL = 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Instrument+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&display=swap';

const temaOf = () => {
  const m = document.documentElement.dataset.mode;
  return m === 'dark' ? 'koyu' : m === 'sepia' ? 'sepya' : 'acik';
};

export default function V17Kok({ rota, dersKey }: { rota: string; dersKey?: string }) {
  const cihaz = useCihaz();
  const [tema, setTema] = useState(temaOf);
  useEffect(() => {
    const kok = document.documentElement;
    kok.dataset.v17Ekran = 'on';
    if (!document.getElementById(FONT_ID)) {
      const l = document.createElement('link');
      l.id = FONT_ID; l.rel = 'stylesheet'; l.href = FONT_URL;
      document.head.appendChild(l);
    }
    const mo = new MutationObserver(() => setTema(temaOf()));
    mo.observe(kok, { attributes: true, attributeFilter: ['data-mode'] });
    return () => { delete kok.dataset.v17Ekran; mo.disconnect(); };
  }, []);
  const bekle = <Kabuk cihaz={cihaz} aktif="bugun"><p className="k7-not" role="status" style={{ padding: 24 }}>Yükleniyor…</p></Kabuk>;
  return (
    <div className="k7" data-tema={tema} data-cihaz={cihaz}>
      <Suspense fallback={bekle}>
        {rota === 'canli_ders' && dersKey ? (
          <SesliDers dersKey={dersKey} cihaz={cihaz} />
        ) : (
          <Kabuk cihaz={cihaz} aktif="bugun"><Bugun cihaz={cihaz} /></Kabuk>
        )}
      </Suspense>
    </div>
  );
}
