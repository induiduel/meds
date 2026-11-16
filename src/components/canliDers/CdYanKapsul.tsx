// Kabuk yan kapsülü: çalan sesli dersin küçük oynatıcısı. CdSesliEk'ten ayrıldı (2026-11-16) — kabuk her sayfada
// yüklenir; sesli ders eklerinin tamamı (CdSesliEk + çıkmış penceresi + stilleri) yalnız ders sayfasında gereksin diye.
import React from 'react';
import { Pause, Play } from 'lucide-react';
import { cdToggle, useCd } from './canliDersStore';
import { linkClick, navigateTo, pathFor } from '../../router';
import './cdYanKapsul.css';

export function CdYanKapsul() {
  const key = useCd((s) => s.key);
  const baslik = useCd((s) => s.baslik);
  const calar = useCd((s) => s.playing);
  const oran = useCd((s) => (s.dur > 0 ? Math.min(1, s.t / s.dur) : 0));
  if (!key) return null;
  const href = pathFor('canli_ders', key);
  return (
    <div className={`cdy${calar ? ' is-calar' : ''}`}>
      <button type="button" className="cdy-oyn" onClick={() => cdToggle()} aria-label={calar ? 'Duraklat' : 'Oynat'}>
        {calar ? <Pause aria-hidden /> : <Play aria-hidden />}
      </button>
      <a className="cdy-t" href={href} onClick={linkClick(() => navigateTo(href))} title={baslik}>
        <small>{calar ? 'Şimdi çalınıyor' : 'Duraklatıldı'}</small>
        <b>{baslik}</b>
      </a>
      <i className="cdy-bar" style={{ width: `${Math.round(oran * 100)}%` }} aria-hidden />
    </div>
  );
}
