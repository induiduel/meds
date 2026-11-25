import React from 'react';
import { pathFor, type AppRoute } from '../router';
import { TASARRUF_SAYFALAR, botTasarrufAyarla } from './bayrak';
import { setAppearance, useAppearance } from '../utils/appearance';
import './tasarruf.css';

type Props = {
  aktif: AppRoute;
  git: (t: AppRoute) => void;
  children: React.ReactNode;
};

/** Sade kabuk: tek satır üst çubuk + içerik. Yan menü, arama, bildirim, profil, müzik çalar yok. */
export default function TasarrufKabuk({ aktif, git, children }: Props) {
  return (
    <div className="tsf-kok">
      <header className="tsf-ust">
        <span className="tsf-ad">MeDSor</span>
        <nav className="tsf-nav" aria-label="Ana gezinme">
          {TASARRUF_SAYFALAR.map((s) => (
            <a
              key={s.tab}
              href={pathFor(s.tab)}
              aria-current={aktif === s.tab ? 'page' : undefined}
              onClick={(e) => { e.preventDefault(); git(s.tab); }}
            >
              {s.ad}
            </a>
          ))}
        </nav>
      </header>
      <main id="ana-icerik" tabIndex={-1} className="tsf-icerik">{children}</main>
    </div>
  );
}

/** Tasarruf ayarları: profil/sıralama/çevrimdışı yok; arayüz seçimi (v15/v18, H681) + hesap çıkışı */
export function TasarrufAyarlar({ ad, cikis, bot = false }: { ad?: string | null; cikis: () => void; bot?: boolean }) {
  const v18 = useAppearance().v18 === true;
  return (
    <section className="tsf-ayar">
      <h1>Ayarlar</h1>
      <div className="tsf-satir">
        <span id="tsf-arayuz">Arayüz</span>
        <div className="tsf-sec" role="radiogroup" aria-labelledby="tsf-arayuz">
          {([[false, 'v15 · Yalın'], [true, 'v18 · Canlı']] as const).map(([d, et]) => (
            <button key={et} type="button" role="radio" aria-checked={v18 === d} className={v18 === d ? 'is-on' : undefined} onClick={() => setAppearance({ v18: d })}>{et}</button>
          ))}
        </div>
      </div>
      {bot && (
        <div className="tsf-satir">
          <span>Test oturumu: tasarruf kipi</span>
          <button type="button" onClick={() => botTasarrufAyarla(false)}>Normal moda geç</button>
        </div>
      )}
      <div className="tsf-satir">
        <span>{ad ? `${ad} olarak giriş yapıldı` : 'Giriş yapıldı'}</span>
        <button type="button" onClick={cikis}>Çıkış yap</button>
      </div>
    </section>
  );
}
