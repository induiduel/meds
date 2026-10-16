/**
 * Giriş bilgilendirmesi: uygulama ilk açıldığında (cihaz başına bir kez) çıkar; okunup onaylanmadan kapanmaz.
 * İçeriğin yapay zekâ destekli olduğu ve hata içerebileceği açıkça söylenir. Esc, dış tıklama ve kapat düğmesi yok;
 * odak pencere içinde döner. Tüm tasarımlarda (v10/v11/v12) aynı görünür: stiller palet token'larıyla, önek gu-.
 */
import React, { useEffect, useId, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Activity, BookOpen, Check, Flag, ShieldAlert, Sparkles, Stethoscope, Users } from 'lucide-react';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { girisUyarisiKabulEt } from './girisUyarisiDurum';
import './giris-uyarisi.css';

const FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),[tabindex]:not([tabindex="-1"])';

const MADDELER: { ikon: React.ReactNode; baslik: string; metin: string }[] = [
  {
    ikon: <BookOpen />,
    baslik: 'Asıl kaynak ders notların',
    metin: 'Ders slaytları, hocaların anlatımı ve resmî kaynaklar esastır. Bir bilgiden emin değilsen oradan doğrula.',
  },
  {
    ikon: <Users />,
    baslik: 'Çıkmış sorular hafızadan kurulur',
    metin: 'Öğrencilerin sınavdan hatırladıklarıyla yeniden yazılır; soru kökü, şıklar ve cevap anahtarı kesin değildir.',
  },
  {
    ikon: <Stethoscope />,
    baslik: 'Tıbbi tavsiye değildir',
    metin: 'Yalnız eğitim ve sınav hazırlığı içindir; hasta tanı ve tedavisinde kullanılmaz.',
  },
  {
    ikon: <Flag />,
    baslik: 'Hata görürsen bildir',
    metin: 'Soru ve içeriklerdeki bildir düğmesiyle haber ver; düzeltmeler herkese yansır. Eklediğin sorular ve yorumlar diğer öğrencilerle paylaşılır.',
  },
];

export default function GirisUyarisi({ onKabul }: { onKabul: () => void }) {
  const id = useId();
  const panelRef = useRef<HTMLDivElement>(null);
  const [onay, setOnay] = useState(false);
  const [cikiyor, setCikiyor] = useState(false);

  useEffect(() => {
    lockScroll();
    panelRef.current?.focus({ preventScroll: true });
    const onKey = (e: KeyboardEvent) => {
      // Esc kapatmaz; arkadaki sayfaların kısayolları da çalışmasın
      if (e.key === 'Escape') {
        e.preventDefault();
        e.stopPropagation();
        return;
      }
      if (e.key === 'Tab' && panelRef.current) {
        const f = panelRef.current.querySelectorAll<HTMLElement>(FOCUSABLE);
        if (!f.length) return;
        const first = f[0];
        const last = f[f.length - 1];
        if (!panelRef.current.contains(document.activeElement)) {
          e.preventDefault();
          first.focus();
        } else if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    };
    document.addEventListener('keydown', onKey, true);
    return () => {
      document.removeEventListener('keydown', onKey, true);
      unlockScroll();
    };
  }, []);

  const kabul = () => {
    if (!onay || cikiyor) return;
    girisUyarisiKabulEt();
    const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    setCikiyor(true);
    window.setTimeout(onKabul, reduce ? 0 : 180);
  };

  return createPortal(
    <div className={`gu-ortu${cikiyor ? ' is-cikis' : ''}`}>
      <div
        ref={panelRef}
        className="gu-kart"
        role="dialog"
        aria-modal="true"
        aria-labelledby={`${id}-b`}
        aria-describedby={`${id}-a`}
        tabIndex={-1}
      >
        <header className="gu-bas">
          <span className="gu-marka" aria-hidden><Activity strokeWidth={2.4} /></span>
          <div>
            <small>MeDSor · Başlamadan önce</small>
            <h2 id={`${id}-b`}>Önemli bilgilendirme</h2>
          </div>
        </header>

        <div className="gu-govde">
          <section className="gu-ai" id={`${id}-a`} aria-label="Yapay zekâ uyarısı">
            <span className="gu-ai-ikon" aria-hidden><ShieldAlert /></span>
            <div>
              <b>İçerikler yapay zekâya dayanır ve hata içerebilir.</b>
              <p>
                Sorular, açıklamalar, özetler, cevaplar, ders–slayt eşleşmeleri ve sesli anlatımlar büyük ölçüde yapay
                zekâ yardımıyla üretilir ya da düzenlenir. Yanlış, eksik veya güncel olmayan bilgi bulunabilir.
              </p>
            </div>
          </section>

          <p className="gu-giris">
            <Sparkles aria-hidden /> MeDSor öğrencilerin birlikte kurduğu bir çalışma aracıdır. Lütfen şunları bilerek kullan:
          </p>
          <ul className="gu-liste">
            {MADDELER.map((m) => (
              <li key={m.baslik}>
                <span className="gu-ikon" aria-hidden>{m.ikon}</span>
                <span>
                  <b>{m.baslik}</b>
                  <span>{m.metin}</span>
                </span>
              </li>
            ))}
          </ul>
        </div>

        <footer className="gu-alt">
          <label className={`gu-onay${onay ? ' is-on' : ''}`}>
            <input type="checkbox" checked={onay} onChange={(e) => setOnay(e.target.checked)} />
            <span className="gu-kutu" aria-hidden><Check /></span>
            <span>Okudum. İçeriklerin yapay zekâ destekli olduğunu ve hata içerebileceğini anlıyorum.</span>
          </label>
          <button type="button" className="gu-btn" disabled={!onay} onClick={kabul}>
            Kabul et ve devam et
          </button>
        </footer>
      </div>
    </div>,
    document.body,
  );
}
