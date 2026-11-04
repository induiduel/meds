// Sesli ders "ara resim" (mekanizma resmi) ara sayfası (kullanıcı kararı 2026-11-04; docs/ARA_RESIM_KURALLARI.md).
// Etkin paragraf bir resmin [paragraf, bitis] aralığındayken PDF alanının üstünde resim kartı açılır; ders sesi DURMAZ
// (ara soru sayfasından farkı), aralık bitince kart kendiliğinden kalkar. "Slayta dön" o aralık bitene dek gizler.
// Kart resim kimliğiyle anahtarlanır: giriş animasyonu her yeniden çizimde değil, yalnız yeni resimde oynar (kural 18 ruhu).
// Araç çubuğu düğmesi (CdAraResimDugme) dersin tüm resimlerini galeride gösterir; birine dokununca ders o paragrafa gider.
import React, { useEffect, useLayoutEffect, useRef, useState, useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
import { ChevronDown, ChevronUp, Images, Maximize2, Undo2, X } from 'lucide-react';
import { cdParagrafa, useCd } from './canliDersStore';
import { araResimBitis, araResimBul, araResimleri, araResimYolu, type AraResim } from './araResimVeri';
import '../../styles/v15/ara_resim.css';

/* "Slayta dön" ile gizlenen resim: aralığı bitene dek; galeri ve tam ekran durumu (tek ders ekranı) */
let gizli: string | null = null;
const dinle = new Set<() => void>();
const gizle = (id: string | null) => { if (gizli !== id) { gizli = id; dinle.forEach((f) => f()); } };
const abone = (f: () => void) => { dinle.add(f); return () => { dinle.delete(f); }; };

function Buyuk({ r, onKapat }: { r: AraResim; onKapat: () => void }) {
  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); };
    window.addEventListener('keydown', k);
    return () => window.removeEventListener('keydown', k);
  }, [onKapat]);
  return createPortal(
    <div className="ar-buyuk" role="dialog" aria-modal="true" aria-label={r.baslik} onClick={onKapat}>
      <div className="ar-buyuk-ic" onClick={(e) => e.stopPropagation()}>
        <div className="ar-buyuk-bas">
          <b>{r.baslik}</b>
          <button type="button" className="ar-ib" onClick={onKapat} aria-label="Büyük görünümü kapat" title="Kapat"><X /></button>
        </div>
        <div className="ar-buyuk-resim"><img src={araResimYolu(r)} alt={r.aciklama || r.baslik} /></div>
        {r.aciklama && <p className="ar-alt">{r.aciklama}</p>}
      </div>
    </div>,
    document.body,
  );
}

/** PDF bölmesinde bir kez bulunur: etkin paragrafın resmi varsa PDF alanının üstünde kart */
export function CdAraResimKok({ dersKey }: { dersKey: string }) {
  const liste = araResimleri(dersKey);
  const aktif = useCd((s) => s.aktif);
  const gz = useSyncExternalStore(abone, () => gizli);
  const [buyuk, setBuyuk] = useState(false);
  const [adimAcik, setAdimAcik] = useState(() => !(typeof window !== 'undefined' && window.matchMedia?.('(max-width: 599px)').matches));
  const ref = useRef<HTMLDivElement>(null);
  const r = liste.length ? araResimBul(liste, aktif) : null;
  // gizlenen resmin aralığı bitti → gizleme düşer
  useEffect(() => { if (gz && (!r || r.id !== gz)) gizle(null); }, [gz, r]);
  const goster = r && r.id !== gz ? r : null;
  useEffect(() => { setBuyuk(false); }, [goster?.id]);
  // Kart PDF gövdesinin (araç çubuğunun altı) üstüne oturur; çubuk gizlenip açılınca yeniden ölçülür
  useLayoutEffect(() => {
    const el = ref.current;
    const govde = el?.parentElement?.querySelector<HTMLElement>('.cd-pdf-govde');
    if (!el || !govde) return;
    // alttaki sabit oynatıcı (--cd-dock-h) kartın alt yazısını örtmesin
    const olc = () => {
      el.style.top = `${govde.offsetTop}px`;
      const dock = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--cd-dock-h')) || 0;
      const alt = (el.parentElement?.getBoundingClientRect().bottom ?? 0) - (window.innerHeight - dock);
      el.style.paddingBottom = alt > 0 ? `${Math.round(alt + 8)}px` : '';
    };
    olc();
    const ro = new ResizeObserver(olc);
    ro.observe(govde);
    if (el.parentElement) ro.observe(el.parentElement);
    window.addEventListener('resize', olc);
    const id = window.setInterval(olc, 1500); // oynatıcı açılıp kapanınca (--cd-dock-h) olay yok
    return () => { ro.disconnect(); window.removeEventListener('resize', olc); clearInterval(id); };
  }, [goster?.id]);
  if (!goster) return null;
  const adimlar = (goster.adimlar || []).slice(0, 6);
  return (
    <div ref={ref} className="ar-kat" role="region" aria-label={`Ara resim: ${goster.baslik}`}>
      <figure key={goster.id} className="ar-kart">
        <div className="ar-bas">
          <span className="ar-et"><Images aria-hidden /> Ara resim</span>
          <b className="ar-baslik">{goster.baslik}</b>
          <button type="button" className="ar-ib" onClick={() => setBuyuk(true)} aria-label="Resmi tam ekran büyüt" title="Büyüt"><Maximize2 /></button>
          <button type="button" className="ar-btn" onClick={() => gizle(goster.id)} title="Bu bölüm bitene dek slaytı göster">
            <Undo2 aria-hidden /> <span>Slayta dön</span>
          </button>
        </div>
        <button type="button" className="ar-resim" onClick={() => setBuyuk(true)} aria-label="Resmi büyüt">
          <img src={araResimYolu(goster)} alt={goster.aciklama || goster.baslik} draggable={false} />
        </button>
        <figcaption className="ar-yazi">
          {goster.aciklama && <p className="ar-alt">{goster.aciklama}</p>}
          {!!adimlar.length && (
            <div className={`ar-adim${adimAcik ? ' is-acik' : ''}`}>
              <button type="button" className="ar-adim-tgl" onClick={() => setAdimAcik((x) => !x)} aria-expanded={adimAcik}>
                {adimAcik ? <ChevronUp aria-hidden /> : <ChevronDown aria-hidden />} Adımlar ({adimlar.length})
              </button>
              {adimAcik && <ol>{adimlar.map((a, i) => <li key={i}>{a.replace(/^\s*\d+[.)]\s*/, '')}</li>)}</ol>}
            </div>
          )}
          {!!goster.kaynak?.length && <small className="ar-kaynak">Kaynak: slayt {goster.kaynak.join(', ')}</small>}
        </figcaption>
      </figure>
      {buyuk && <Buyuk r={goster} onKapat={() => setBuyuk(false)} />}
    </div>
  );
}

/** Araç çubuğu düğmesi: dersin tüm ara resimleri; dokununca ders o paragrafa gider */
export function CdAraResimDugme({ dersKey }: { dersKey: string }) {
  const liste = araResimleri(dersKey);
  const [acik, setAcik] = useState(false);
  const aktif = useCd((s) => s.aktif);
  useEffect(() => {
    if (!acik) return;
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') setAcik(false); };
    window.addEventListener('keydown', k);
    return () => window.removeEventListener('keydown', k);
  }, [acik]);
  if (!liste.length) return null;
  return (
    <>
      <button type="button" className="cd-btn is-ikon ar-dugme" onClick={() => setAcik(true)}
        aria-label={`Ara resimler (${liste.length})`} title={`Ara resimler (${liste.length}): mekanizma resimleri`}>
        <Images aria-hidden /><span className="ar-dugme-n" aria-hidden>{liste.length}</span>
      </button>
      {acik && createPortal(
        <div className="ar-buyuk" role="dialog" aria-modal="true" aria-label="Ara resimler" onClick={() => setAcik(false)}>
          <div className="ar-galeri" onClick={(e) => e.stopPropagation()}>
            <div className="ar-buyuk-bas">
              <b>Ara resimler · {liste.length}</b>
              <button type="button" className="ar-ib" onClick={() => setAcik(false)} aria-label="Galeriyi kapat" title="Kapat"><X /></button>
            </div>
            <ul className="ar-galeri-l">
              {liste.map((r) => (
                <li key={r.id}>
                  <button type="button" className={aktif >= r.paragraf && aktif <= araResimBitis(r) ? 'is-aktif' : ''}
                    onClick={() => { gizle(null); setAcik(false); cdParagrafa(r.paragraf); }}>
                    <span className="ar-galeri-r"><img src={araResimYolu(r)} alt="" loading="lazy" /></span>
                    <b>{r.baslik}</b>
                    {r.aciklama && <small>{r.aciklama}</small>}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </div>,
        document.body,
      )}
    </>
  );
}
