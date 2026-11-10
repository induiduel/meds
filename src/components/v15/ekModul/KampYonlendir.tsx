import React, { useEffect, useState } from 'react';
import { Tent } from 'lucide-react';
import { navigateTo } from '../../../router';

/** Siteye her girişte (oturum başına bir kez) Yürüyüş ve Kampçılık dersine yönlendirme sorusu. */
const ADRES = '/dersler/ek-moduller/kurul2/yuruyus-kampcilik';
const KEY = 'medsoru_kamp_yonlendir_soruldu';

const KampYonlendir: React.FC = () => {
  const [acik, setAcik] = useState(false);
  useEffect(() => {
    try {
      if (sessionStorage.getItem(KEY) || location.pathname.startsWith('/dersler/ek-moduller')) return;
      sessionStorage.setItem(KEY, '1');
    } catch { /* depolama yoksa yine sor */ }
    const t = setTimeout(() => setAcik(true), 1200);
    return () => clearTimeout(t);
  }, []);
  if (!acik) return null;
  return (
    <div role="dialog" aria-modal="true" aria-labelledby="kamp-yon-b" onClick={() => setAcik(false)}
      style={{ position: 'fixed', inset: 0, zIndex: 9000, background: 'rgba(0,0,0,.55)', display: 'grid', placeItems: 'center', padding: 16 }}>
      <div className="v15-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: 380, width: '100%', padding: 20, display: 'grid', gap: 12 }}>
        <Tent aria-hidden style={{ width: 32, height: 32 }} />
        <b id="kamp-yon-b" style={{ fontSize: 18 }}>Yürüyüş ve Kampçılık dersine gidelim mi?</b>
        <span style={{ opacity: .8 }}>Sesli ders, hocanın çalışma soruları, çalışma föyü ve PDF kitapçıkları tek sayfada.</span>
        <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
          <button type="button" className="v15-btn is-ghost" onClick={() => setAcik(false)}>Şimdi değil</button>
          <button type="button" className="v15-btn" autoFocus onClick={() => { setAcik(false); navigateTo(ADRES); }}>Evet, götür</button>
        </div>
      </div>
    </div>
  );
};
export default KampYonlendir;
