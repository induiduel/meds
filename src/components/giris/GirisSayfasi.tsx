import { Suspense, useEffect } from 'react';
import { guvenliLazy } from '../../utils/guvenliLazy';
import type { AppUser } from '../../services/auth';
import '../../styles/giris.css';

const UserAuthModal = guvenliLazy(() => import('../UserAuthModal').then((m) => ({ default: m.UserAuthModal })));

const MADDELER = [
  { b: 'Sesli dersler', t: 'Hocanın anlattığı cümle metinde ve PDF’te aynı anda işaretlenir.' },
  { b: 'Açıklamalı sorular', t: 'Her şıkkın ne olduğu ve neden doğru ya da yanlış olduğu yazılı.' },
  { b: 'Çıkmışlar', t: 'Geçmiş yılların soruları konu konu, derse bağlı.' },
];

/**
 * Giriş sayfası (2026-11-25, H671): eskiden tanıtım + giriş ana uygulamanın üstüne açılan bir katmandı
 * (`role="dialog"`), altında kabuk ve sayfa verisi yine kuruluyordu. Artık kendi adresi (/giris) olan,
 * kabuğu hiç kurmayan ayrı sayfa. Kimlik formu mevcut `UserAuthModal` (gömülü kip); giriş mantığı değişmedi.
 */
export default function GirisSayfasi({ onAuthSuccess }: { onAuthSuccess: (user: AppUser, token?: string | null) => void }) {
  useEffect(() => {
    const onceki = document.title;
    document.title = 'Giriş · MeDSor';
    return () => { document.title = onceki; };
  }, []);

  return (
    <div className="gr">
      <a className="gr-atla" href="#gr-form">Giriş formuna geç</a>
      <header className="gr-ust">
        <span className="gr-marka" aria-label="MeDSor">MeDSor</span>
      </header>
      <main className="gr-ana">
        <section className="gr-tanitim" aria-labelledby="gr-baslik">
          <p className="gr-ust-etiket">Dönem 3 · Kurul hazırlığı</p>
          <h1 id="gr-baslik" className="gr-baslik">Kurul sınavlarına hocanın sesiyle hazırlan.</h1>
          <p className="gr-giris">Sesli dersler, çıkmış sorular ve konu konu soru çözücü tek yerde.</p>
          <ul className="gr-maddeler">
            {MADDELER.map((m) => (
              <li key={m.b}>
                <b>{m.b}</b>
                <span>{m.t}</span>
              </li>
            ))}
          </ul>
        </section>
        <section id="gr-form" className="gr-form" aria-label="Hesabına gir" tabIndex={-1}>
          <Suspense fallback={<div className="gr-form-iskelet" aria-hidden="true" />}>
            <UserAuthModal isOpen embedded mandatory onClose={() => {}} onAuthSuccess={onAuthSuccess} initialMode="login" />
          </Suspense>
        </section>
      </main>
      <footer className="gr-alt">
        <span>MeDSor · tıp fakültesi kurul hazırlığı</span>
      </footer>
    </div>
  );
}
