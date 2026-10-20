import React, { useEffect, useState } from 'react';
import { ArrowLeft, ArrowRight, Home, LayoutGrid, Shrink, X } from 'lucide-react';
import { NAV_TREE } from './navModel';
import { AppRoute, pathFor, navigateTo } from '../../router';
import { useAppFullscreen } from '../../utils/fullscreen';
import '../../styles/tam-ekran-gezinme.css';

/**
 * Tam ekranda kabuk (üst çubuk, kenar menüsü, alt sekmeler) gizlidir; bu yüzen ada sayfalar arası
 * gezinmeyi tam ekrandan çıkmadan sağlar: Geri/İleri (tarayıcı geçmişi), Ana sayfa, Sayfalar listesi
 * ve tam ekrandan çıkış. Gezinme pushState/popstate ile yapılır; `releasePageFullscreen` sayesinde
 * kapanan sayfa tam ekranı kapatmaz. Ada birkaç saniye sonra kendiliğinden kenar tutamacına katlanır.
 */
const KATLAN_MS = 3500;

export const TamEkranGezinme: React.FC<{ active: AppRoute; onGo: (r: AppRoute) => void }> = ({ active, onGo }) => {
  const [fs, , exit] = useAppFullscreen();
  const [acik, setAcik] = useState(false);
  // Otomatik katlanma: ada açıldıktan KATLAN_MS sonra kenar tutamacına iner (içeriği kapatmasın).
  // Dokunma/odak/üzerinde durma süreyi yeniler; Sayfalar menüsü açıkken katlanmaz. Tutamağa dokununca açılır.
  const [katli, setKatli] = useState(false);
  const [canli, setCanli] = useState(0);
  const [ustunde, setUstunde] = useState(false);
  const durt = () => setCanli((n) => n + 1);

  // Açık bir pencere (tanıtım, onay, ayar diyaloğu) varken ada gizlenir; üstüne binmesin, odak tuzağını bozmasın.
  // Tam ekran oynatıcılar da aria-modal taşır (ders, çözücü, asistan, büyütülmüş PDF, tam ekran okuyucu): onlar pencere sayılmaz.
  const [pencere, setPencere] = useState(false);
  useEffect(() => {
    if (!fs) return;
    let raf = 0;
    const bak = () => {
      raf = 0;
      setPencere(!!document.querySelector('[aria-modal="true"]:not(.ls-root):not(.sc):not(.pa):not(.dpv):not(.r12-root.is-immersive), .sh-sheet-root'));
    };
    bak();
    const mo = new MutationObserver(() => { if (!raf) raf = window.setTimeout(bak, 50); });
    mo.observe(document.body, { childList: true, subtree: true });
    return () => { mo.disconnect(); if (raf) clearTimeout(raf); };
  }, [fs]);

  useEffect(() => { if (!fs) setAcik(false); else setKatli(false); }, [fs]);
  useEffect(() => {
    if (!fs || katli || acik || ustunde) return;
    const t = window.setTimeout(() => setKatli(true), KATLAN_MS);
    return () => clearTimeout(t);
  }, [fs, katli, acik, ustunde, canli, active]);
  useEffect(() => { setAcik(false); }, [active]);
  useEffect(() => {
    if (!acik) return;
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') { e.stopPropagation(); setAcik(false); } };
    window.addEventListener('keydown', k, true);
    return () => window.removeEventListener('keydown', k, true);
  }, [acik]);

  if (!fs || pencere) return null;

  const katla = (v: boolean) => { setKatli(v); setUstunde(false); durt(); };
  const geri = () => {
    if (window.history.length > 1) window.history.back();
    else navigateTo(pathFor('today'));
  };
  const git = (r: AppRoute) => { setAcik(false); onGo(r); };

  if (katli) {
    return (
      <button type="button" className="teg-kulak" onClick={() => katla(false)} aria-label="Gezinmeyi göster" title="Gezinmeyi göster">
        <LayoutGrid size={16} />
      </button>
    );
  }

  return (
    <>
      <nav
        className="teg"
        aria-label="Tam ekran gezinme"
        onPointerDown={durt}
        onFocus={durt}
        onPointerEnter={(e) => { if (e.pointerType === 'mouse') setUstunde(true); }}
        onPointerLeave={(e) => { if (e.pointerType === 'mouse') setUstunde(false); }}
      >
        <button type="button" onClick={geri} aria-label="Geri" title="Geri (Alt+←)"><ArrowLeft size={18} /></button>
        <button type="button" onClick={() => window.history.forward()} aria-label="İleri" title="İleri (Alt+→)"><ArrowRight size={18} /></button>
        <button type="button" onClick={() => git('today')} aria-label="Ana sayfa" title="Ana sayfa"><Home size={18} /></button>
        <button type="button" onClick={() => setAcik((v) => !v)} aria-label="Sayfalar" aria-expanded={acik} title="Sayfalar" className={acik ? 'is-on' : ''}><LayoutGrid size={18} /></button>
        <span className="teg-ayrac" aria-hidden />
        <button type="button" onClick={exit} aria-label="Tam ekrandan çık" title="Tam ekrandan çık"><Shrink size={18} /></button>
        <button type="button" onClick={() => katla(true)} aria-label="Gezinmeyi gizle" title="Gezinmeyi gizle" className="teg-kucuk"><X size={14} /></button>
      </nav>
      {acik && (
        <div className="teg-perde" onClick={() => setAcik(false)}>
          <div className="teg-sayfalar" role="dialog" aria-label="Sayfalar" onClick={(e) => e.stopPropagation()}>
            {NAV_TREE.map((g, gi) => (
              <section key={gi}>
                {g.label && <h3>{g.label}</h3>}
                <div className="teg-izgara">
                  {g.items.map((it) => {
                    const Icon = it.icon;
                    return (
                      <a
                        key={it.id}
                        href={pathFor(it.id)}
                        className={it.id === active ? 'is-on' : ''}
                        aria-current={it.id === active ? 'page' : undefined}
                        onClick={(e) => { e.preventDefault(); git(it.id); }}
                      >
                        <Icon size={16} />
                        <span>{it.label}</span>
                      </a>
                    );
                  })}
                </div>
              </section>
            ))}
          </div>
        </div>
      )}
    </>
  );
};
