/**
 * Ders açılış paneli: ders ekranı açılınca (bu ders çalmıyorsa) slayt/metin bölmelerinin üstünde çıkar.
 * Tek ekranda: devam et / baştan başla, görünüm (Metin, Metin + Slayt, Slayt), ses, hız ve bölümler (içindekiler —
 * dokunulan bölümden başlar). "Ders ekranına geç" ya da Esc paneli kapatır; ses başlatılınca da kapanır.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { BookOpen, Check, CircleHelp, Columns2, FileText, Play, RotateCcw, ScrollText, X } from 'lucide-react';
import {
  CD_HIZLAR, cdDetayBagla, cdHiz, cdKayitliKonum, cdOynat, cdParagrafa, cdSesKisa, cdTercihVaryant, fmtSure, useCd,
  type CdDetay,
} from './canliDersStore';
import { cdDersEtiketi } from './canliDersKategori';
import { bittiMi, useKonuKaydi } from '../../services/calismaTakip';
import '../../styles/canli-ders-liste.css';

export type CdGorunum = 'metin' | 'ikisi' | 'pdf';
const GORUNUM_SECENEK: { id: CdGorunum; ad: string; acik: string; ikon: React.ReactNode }[] = [
  { id: 'metin', ad: 'Metin', acik: 'Konuşma metni sesle akar', ikon: <ScrollText aria-hidden /> },
  { id: 'ikisi', ad: 'Metin + Slayt', acik: 'Slayt ve metin yan yana', ikon: <Columns2 aria-hidden /> },
  { id: 'pdf', ad: 'Slayt', acik: 'Yalnız slayt, işaretli', ikon: <FileText aria-hidden /> },
];
const HIZ_SECENEK = [1, 1.25, 1.5, 1.75, 2].filter((h) => (CD_HIZLAR as readonly number[]).includes(h));

export function CanliDersBaslangic({ detay, gorunum, setGorunum, pdfVar, onKapat }: {
  detay: CdDetay; gorunum: CdGorunum; setGorunum: (g: CdGorunum) => void; pdfVar: boolean; onKapat: () => void;
}) {
  const kayit = useMemo(() => cdKayitliKonum(detay.key), [detay.key]);
  const varsayilan = cdTercihVaryant(detay.varyantlar);
  const [vid, setVid] = useState(() => (kayit && detay.varyantlar.some((v) => v.id === kayit.vid) ? kayit.vid : varsayilan?.id) || '');
  const v = detay.varyantlar.find((x) => x.id === vid) || varsayilan;
  const rate = useCd((s) => s.rate);
  const bitti = bittiMi(useKonuKaydi('sesli', detay.key));
  const devamT = kayit && kayit.vid === v?.id ? kayit.t : 0;
  const ilkRef = useRef<HTMLButtonElement>(null);
  const cikmisN = detay.cikmisKonum?.length || 0;
  const paragrafN = detay.bolumler.reduce((n, b) => n + b.paragraflar.length, 0);

  useEffect(() => {
    ilkRef.current?.focus({ preventScroll: true });
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape' && !document.querySelector('[role="dialog"][aria-modal="true"]')) onKapat(); };
    document.addEventListener('keydown', k);
    return () => document.removeEventListener('keydown', k);
  }, [onKapat]);

  /** Sesi bu derse bağlar (başka ders çalıyorsa onu bırakır) ve verilen yerden başlatır */
  const basla = (o: { t?: number; paragraf?: number }) => {
    if (!v) return;
    if (o.paragraf != null) {
      cdOynat(detay, v.id, { oynat: false });
      cdDetayBagla(detay);
      cdParagrafa(o.paragraf, true);
    } else {
      cdOynat(detay, v.id, { t: o.t ?? 0 });
      cdDetayBagla(detay);
    }
    onKapat();
  };

  return (
    <div className="cdb" role="region" aria-label="Ders açılışı">
      <div className="cdb-kart">
        <button type="button" className="cd-btn is-ikon cdb-x" onClick={onKapat} aria-label="Ders ekranına geç" title="Ders ekranına geç (Esc)"><X aria-hidden /></button>
        <header className="cdb-bas">
          <small>{cdDersEtiketi(detay)}{bitti && <span className="cdb-bitti"><Check aria-hidden /> bitti</span>}</small>
          <h2>{detay.baslik}</h2>
          <p className="cdb-ozet">
            {v && <span>{fmtSure(v.sureSn)}</span>}
            <span>{detay.bolumler.length} bölüm</span>
            <span>{paragrafN} paragraf</span>
            {pdfVar && <span>slaytlarla eşleşik</span>}
            {cikmisN > 0 && <span><CircleHelp aria-hidden /> {cikmisN} çıkmış soruya değiniyor</span>}
          </p>
        </header>

        <div className="cdb-ana">
          {devamT > 5 ? (
            <>
              <button ref={ilkRef} type="button" className="cdb-buyuk is-ana" onClick={() => basla({ t: devamT })}>
                <Play aria-hidden />
                <span><b>Kaldığın yerden devam et</b><small>{fmtSure(devamT)} / {fmtSure(v?.sureSn || 0)}</small></span>
              </button>
              <button type="button" className="cdb-buyuk" onClick={() => basla({ t: 0 })}>
                <RotateCcw aria-hidden />
                <span><b>Baştan başla</b><small>İlk bölümden dinle</small></span>
              </button>
            </>
          ) : (
            <button ref={ilkRef} type="button" className="cdb-buyuk is-ana" onClick={() => basla({ t: 0 })}>
              <Play aria-hidden />
              <span><b>{bitti ? 'Tekrar dinle' : 'Dersi başlat'}</b><small>Ses çalar, metin ve slayt kendiliğinden akar</small></span>
            </button>
          )}
          <button type="button" className="cdb-buyuk is-sade" onClick={onKapat}>
            <BookOpen aria-hidden />
            <span><b>Sessiz oku</b><small>Önce metne ve slayta göz at</small></span>
          </button>
        </div>

        <div className="cdb-ayar">
          {pdfVar && (
            <fieldset className="cdb-grup is-genis">
              <legend>Görünüm</legend>
              <div className="cdb-gorunum" role="radiogroup" aria-label="Görünüm">
                {GORUNUM_SECENEK.map((g) => (
                  <button key={g.id} type="button" role="radio" aria-checked={gorunum === g.id} className={gorunum === g.id ? 'is-on' : ''} onClick={() => setGorunum(g.id)}>
                    {g.ikon}<b>{g.ad}</b><small>{g.acik}</small>
                  </button>
                ))}
              </div>
            </fieldset>
          )}
          <fieldset className="cdb-grup">
            <legend>Hız</legend>
            <div className="cdb-hiz" role="radiogroup" aria-label="Oynatma hızı">
              {HIZ_SECENEK.map((h) => (
                <button key={h} type="button" role="radio" aria-checked={rate === h} className={rate === h ? 'is-on' : ''} onClick={() => cdHiz(h)}>
                  {h.toLocaleString('tr')}×
                </button>
              ))}
            </div>
          </fieldset>
          {detay.varyantlar.length > 1 && (
            <fieldset className="cdb-grup">
              <legend>Ses</legend>
              <select className="cdb-ses" value={v?.id || ''} onChange={(e) => setVid(e.target.value)} aria-label="Ses">
                {detay.varyantlar.map((x) => <option key={x.id} value={x.id}>{cdSesKisa(x)} · {fmtSure(x.sureSn)}{x.id === varsayilan?.id ? ' (varsayılan)' : ''}</option>)}
              </select>
            </fieldset>
          )}
        </div>

        {detay.bolumler.length > 1 && (
          <nav className="cdb-bolumler" aria-label="Bölümler">
            <p className="cdb-grup-bas">Bölümler <small>dokunduğun bölümden başlar</small></p>
            <ol>
              {detay.bolumler.map((b, i) => {
                const p0 = b.paragraflar[0]?.i;
                return (
                  <li key={i}>
                    <button type="button" disabled={p0 == null} onClick={() => p0 != null && basla({ paragraf: p0 })}>
                      <span className="cdb-bno">{i + 1}</span>
                      <span className="cdb-bad">{b.baslik || `Bölüm ${i + 1}`}</span>
                      <Play aria-hidden className="cdb-boyn" />
                    </button>
                  </li>
                );
              })}
            </ol>
          </nav>
        )}
      </div>
    </div>
  );
}
