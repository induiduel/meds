import React, { useState } from 'react';
import { Compass, Search } from 'lucide-react';
import { linkClick, navigateTo, pathFor } from '../../router';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ek15.css';

/**
 * v15 · 404 (tasarım AB16 hata404). parseLocation, siteHaritasi çevirisi ve takma adlarla eşleşmeyen yolda
 * 'bulunamadi' döndürür; adres çubuğu olduğu gibi kalır. Ara → /ara/<sorgu>, Bugün'e dön → /bugun.
 */
export default function BulunamadiV15() {
  useV15Baslik({ baslik: 'Sayfa bulunamadı' });
  const yol = typeof window !== 'undefined' ? decodeURIComponent(window.location.pathname) : '';
  const ilk = yol.split('/').filter(Boolean).pop()?.replace(/[-_]+/g, ' ') || '';
  const [q, setQ] = useState(ilk);
  const ara = (e: React.FormEvent) => {
    e.preventDefault();
    const t = q.trim();
    navigateTo(pathFor('search', t || undefined));
  };
  return (
    <div className="nf15 v15-card" role="main" aria-labelledby="nf15-b">
      <Compass className="nf15-ik" aria-hidden />
      <h1 id="nf15-b">Bu sayfa bulunamadı</h1>
      <p className="v15-cap">Adres yanlış yazılmış ya da sayfa taşınmış olabilir.</p>
      {yol && <code className="nf15-yol">{yol}</code>}
      <form className="nf15-ara" onSubmit={ara} role="search">
        <Search aria-hidden />
        <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Ders, terim ya da soru ara" aria-label="Sitede ara" />
        <button type="submit" className="v15-btn is-ghost">Ara</button>
      </form>
      <a className="v15-btn nf15-don" href={pathFor('today')} onClick={linkClick(() => navigateTo(pathFor('today')))}>Bugün'e dön</a>
    </div>
  );
}
