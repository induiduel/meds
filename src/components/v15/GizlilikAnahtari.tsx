import React, { useEffect, useState } from 'react';
import { safeJsonFetch } from '../../services/api';

/**
 * "Profilim herkese açık" anahtarı (varsayılan AÇIK). Kapatan kişi sıralamada adsız "Gizli kullanıcı" görünür,
 * açık profili ve kişi aramasında görünmez. Sunucu: GET /api/kisi/ben, POST /api/kisi/gizlilik {acik}.
 */
export default function GizlilikAnahtari() {
  const [acik, setAcik] = useState<boolean | null>(null);
  const [hata, setHata] = useState('');
  useEffect(() => {
    void safeJsonFetch<{ girisli: boolean; acik?: boolean }>('/api/kisi/ben').then((r) => { if (r.ok && r.data?.girisli) setAcik(r.data.acik !== false); });
  }, []);
  if (acik == null) return null;
  const degistir = async () => {
    const yeni = !acik;
    setAcik(yeni); setHata('');
    const r = await safeJsonFetch<{ acik: boolean }>('/api/kisi/gizlilik', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ acik: yeni }) });
    if (!r.ok) { setAcik(!yeni); setHata((r.data as any)?.error || 'Kaydedilemedi.'); }
  };
  return (
    <div className="v15-card ks15-gizlilik">
      <label>
        <span><b>Profilim herkese açık</b><small>{acik ? 'Adın, çalışma süren, çözdüğün sorular ve çalıştığın dersler herkese görünür.' : 'Sıralamada "Gizli kullanıcı" olarak görünürsün; profilin ve aramada adın gizli.'}</small></span>
        <input type="checkbox" role="switch" checked={acik} onChange={() => void degistir()} aria-checked={acik} />
      </label>
      {hata && <small className="ks15-hata">{hata}</small>}
    </div>
  );
}
