/**
 * Sesli ders metnini dışa aktarma penceresi: derse girmeden de (ders sayfası, ders listesi) açılır.
 * Biçim (PDF / Word / Markdown / düz metin), içerik (kapsam, üslup, işaretler, slayt başlıkları, resimler, ekler),
 * bölüm seçimi, PDF görünümü ve dersin kendi metniyle canlı önizleme. Belge üretimi: canliDersDisaAktar + metinDisaAktar.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { Check, Copy, Download, FileDown, Loader2, X } from 'lucide-react';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import type { AktarBelge, AktarBicim } from '../../services/metinDisaAktar';
import { duzenOku, duzenYaz, type PdfDuzen } from '../../services/pdfDuzen';
import { PdfAyarDugme } from '../ui/PdfDuzenSecici';
import { cdDetayGetir, type CdDetay } from './canliDersStore';
import { cdDersEtiketi } from './canliDersKategori';
import { cdAktarBelgesi, cdAktarSecenekOku, cdAktarSecenekYaz, cdAktarVar, type CdAktarSecenek } from './canliDersDisaAktar';
import type { SlaytBasliklari } from './cdSlaytBasliklari';
import '../../styles/toplu-pdf.css';
import '../../styles/cd-aktar-pencere.css';

const PdfOnizleme = React.lazy(() => import('../ui/PdfOnizleme'));

export const CD_BICIMLER: { id: AktarBicim; ad: string; alt: string }[] = [
  { id: 'pdf', ad: 'PDF', alt: 'Yazdırmaya hazır' },
  { id: 'docx', ad: 'Word', alt: 'Düzenlenebilir' },
  { id: 'md', ad: 'Markdown', alt: 'Not uygulamaları' },
  { id: 'txt', ad: 'Düz metin', alt: 'Her yerde açılır' },
];
const BICIM_ANAHTAR = 'medsoru_cd_aktar_bicim_v1';
export const cdBicimOku = (): AktarBicim => {
  try { const v = localStorage.getItem(BICIM_ANAHTAR) as AktarBicim; if (CD_BICIMLER.some((b) => b.id === v)) return v; } catch { /* yok */ }
  return 'pdf';
};
export const cdBicimYaz = (b: AktarBicim) => { try { localStorage.setItem(BICIM_ANAHTAR, b); } catch { /* yok */ } };

export function BicimSecici({ deger, onDegis, ad }: { deger: AktarBicim; onDegis: (b: AktarBicim) => void; ad: string }) {
  return (
    <div className="cap-bicim" role="radiogroup" aria-label="Dosya biçimi">
      {CD_BICIMLER.map((b) => (
        <label key={b.id} className={deger === b.id ? 'is-on' : ''}>
          <input type="radio" name={`${ad}-bicim`} checked={deger === b.id} onChange={() => onDegis(b.id)} />
          <b>{b.ad}</b><small>{b.alt}</small>
        </label>
      ))}
    </div>
  );
}

type Var = ReturnType<typeof cdAktarVar>;

/** İçerik seçenekleri (tek ders penceresi ve toplu indirme ortak). `varlik` verilirse derste karşılığı olmayan seçenek kapanır. */
export function CdSecenekAlani({ deger, onDegis, ad, varlik, bicim }: { deger: CdAktarSecenek; onDegis: (s: CdAktarSecenek) => void; ad: string; varlik?: Var; bicim?: AktarBicim }) {
  const yaz = (p: Partial<CdAktarSecenek>) => onDegis({ ...deger, ...p });
  const ozet = deger.kapsam === 'onemli';
  const duz = bicim === 'txt';
  const Kutu = ({ k, ad: etiket, alt, kapali, neden }: { k: 'vurgu' | 'terim' | 'basliklar' | 'resimler' | 'sozluk' | 'cikmis'; ad: string; alt?: string; kapali?: boolean; neden?: string }) => {
    const yok = varlik ? !varlik[k] : false;
    return (
      <label className={yok || kapali ? 'is-kapali' : ''}>
        <input type="checkbox" disabled={yok || kapali} checked={deger[k] && !yok && !kapali} onChange={(e) => yaz({ [k]: e.target.checked })} />
        <span>{etiket}{(yok || kapali || alt) && <small> {yok ? '(bu derste yok)' : kapali ? neden : alt}</small>}</span>
      </label>
    );
  };
  return (
    <div className="cap-secenek">
      <div className="cap-ikili" role="radiogroup" aria-label="Kapsam">
        <label className={!ozet ? 'is-on' : ''}><input type="radio" name={`${ad}-kapsam`} checked={!ozet} onChange={() => yaz({ kapsam: 'tam' })} /><b>Tüm metin</b><small>Dersin bütün anlatımı</small></label>
        <label className={`${ozet ? 'is-on' : ''}${varlik && !varlik.vurgu ? ' is-kapali' : ''}`}>
          <input type="radio" name={`${ad}-kapsam`} disabled={!!varlik && !varlik.vurgu} checked={ozet} onChange={() => yaz({ kapsam: 'onemli' })} />
          <b>Yalnız önemli yerler</b><small>{varlik && !varlik.vurgu ? 'Bu derste işaret yok' : 'Kısa tekrar notu'}</small>
        </label>
      </div>
      <div className="cap-ikili" role="radiogroup" aria-label="Üslup">
        <label className={deger.uslup === 'not' ? 'is-on' : ''}><input type="radio" name={`${ad}-uslup`} checked={deger.uslup === 'not'} onChange={() => yaz({ uslup: 'not' })} /><b>Ders notu</b><small>Madde madde, sade</small></label>
        <label className={deger.uslup === 'konusma' ? 'is-on' : ''}><input type="radio" name={`${ad}-uslup`} checked={deger.uslup === 'konusma'} onChange={() => yaz({ uslup: 'konusma' })} /><b>Konuşma metni</b><small>Seslendirildiği gibi</small></label>
      </div>
      <div className="cap-kutular">
        <Kutu k="vurgu" ad="Önemli yer işaretleri" kapali={duz} neden="(düz metinde gösterilemez)" />
        <Kutu k="terim" ad="Terimler kalın" kapali={duz} neden="(düz metinde gösterilemez)" />
        <Kutu k="basliklar" ad="Slayt başlıkları" alt="(biraz daha yavaş)" />
        <Kutu k="resimler" ad="Resimler" kapali={ozet} neden="(özet notunda yok)" />
        <Kutu k="sozluk" ad="Ek: terimler ve kısaltmalar" />
        <Kutu k="cikmis" ad="Ek: çıkmış sorular" alt="(doğrulanmış eşlemeler)" />
      </div>
    </div>
  );
}

const kelimeSay = (b: AktarBelge) => b.bolumler.reduce((n, x) => n + (x.md.replace(/!\[[^\]]*\]\([^)]*\)/g, ' ').replace(/[*=#>|-]+/g, ' ').match(/\S+/g)?.length || 0), 0);

export function CdAktarPencere({ dersKey, detay: hazir, vurguAcik, onKapat }: { dersKey: string; detay?: CdDetay; vurguAcik?: boolean; onKapat: () => void }) {
  const [detay, setDetay] = useState<CdDetay | null>(hazir || null);
  const [yukHata, setYukHata] = useState('');
  const [bicim, setBicimH] = useState<AktarBicim>(cdBicimOku);
  const [secenek, setSecenekH] = useState<CdAktarSecenek>(() => ({ ...cdAktarSecenekOku(), ...(vurguAcik === false ? { vurgu: false } : {}) }));
  const [duzen, setDuzenH] = useState<PdfDuzen>(duzenOku);
  const [bolum, setBolum] = useState<Set<number> | null>(null);
  const [belge, setBelge] = useState<AktarBelge | null>(null);
  const [onizle, setOnizle] = useState(false);
  const [is, setIs] = useState<'indir' | 'kopya' | null>(null);
  const [durum, setDurum] = useState<{ tur: 'ok' | 'hata'; yazi: string } | null>(null);
  const basliklarRef = useRef<Promise<SlaytBasliklari | undefined> | null>(null);
  const kapatRef = useRef<HTMLButtonElement>(null);
  const setBicim = (b: AktarBicim) => { setBicimH(b); cdBicimYaz(b); };
  const setSecenek = (s: CdAktarSecenek) => { setSecenekH(s); cdAktarSecenekYaz(s); };
  const setDuzen = (d: PdfDuzen) => { setDuzenH(d); duzenYaz(d); };

  useEffect(() => {
    kapatRef.current?.focus();
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); };
    document.addEventListener('keydown', k);
    lockScroll();
    return () => { document.removeEventListener('keydown', k); unlockScroll(); };
  }, [onKapat]);

  useEffect(() => {
    if (detay) return;
    let iptal = false;
    cdDetayGetir(dersKey).then((d) => { if (!iptal) setDetay(d); }, (e) => { if (!iptal) setYukHata(e instanceof Error && e.message ? e.message : 'Ders alınamadı.'); });
    return () => { iptal = true; };
  }, [dersKey, detay]);

  const varlik = useMemo(() => (detay ? cdAktarVar(detay) : undefined), [detay]);
  const etiket = detay ? cdDersEtiketi(detay) : '';
  /** Derste karşılığı olmayan seçenekler kapalı sayılır (kayıtlı tercih bozulmaz) */
  const etkin = useMemo<CdAktarSecenek>(() => {
    if (!varlik) return secenek;
    const kapsam = secenek.kapsam === 'onemli' && !varlik.vurgu ? 'tam' : secenek.kapsam;
    return { ...secenek, kapsam, vurgu: secenek.vurgu && varlik.vurgu, terim: secenek.terim && varlik.terim, basliklar: secenek.basliklar && varlik.basliklar,
      resimler: secenek.resimler && varlik.resimler, sozluk: secenek.sozluk && varlik.sozluk, cikmis: secenek.cikmis && varlik.cikmis };
  }, [secenek, varlik]);

  const kur = async (b: AktarBicim): Promise<AktarBelge> => {
    if (!detay) throw new Error('ders yok');
    let bas: SlaytBasliklari | undefined;
    if (etkin.basliklar && b !== 'txt') {
      // PDF bir kez açılır; açılamazsa başlıksız sürer
      basliklarRef.current ||= import('./cdSlaytBasliklari').then((m) => m.cdSlaytBasliklari(detay)).catch(() => undefined);
      bas = await basliklarRef.current;
    }
    return cdAktarBelgesi(detay, etiket, etkin, bas, bolum || undefined);
  };

  const anahtar = JSON.stringify([etkin, bicim === 'txt', bolum ? [...bolum].sort() : null]);
  useEffect(() => {
    if (!detay) return;
    let iptal = false;
    setDurum(null);
    kur(bicim).then((b) => { if (!iptal) setBelge(b); }, () => { if (!iptal) setBelge(null); });
    return () => { iptal = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [detay, anahtar]);

  /** Önizleme: ilk üç bölüm, resimsiz (hızlı kalsın) */
  const ornek = useMemo<AktarBelge | null>(() => belge && {
    ...belge, bolumler: belge.bolumler.slice(0, 3).map((b) => ({ ...b, md: b.md.split('\n').filter((l) => !/^\s*!\[/.test(l)).join('\n') })),
  }, [belge]);

  const bos = !!belge && !belge.bolumler.length;
  const dosyaAdi = detay ? `${etiket ? `${etiket} - ` : ''}${detay.baslik}${etkin.kapsam === 'onemli' ? ' (önemli yerler)' : ''}` : '';

  const indir = async () => {
    setIs('indir'); setDurum(null);
    try {
      const { metniIndir } = await import('../../services/metinDisaAktar');
      await metniIndir(await kur(bicim), bicim, dosyaAdi, duzen);
      setDurum({ tur: 'ok', yazi: 'Dosya indirildi.' });
    } catch (e) {
      console.warn('dışa aktarma', e);
      setDurum({ tur: 'hata', yazi: 'Dosya oluşturulamadı, yeniden dene.' });
    } finally { setIs(null); }
  };
  const kopyala = async () => {
    setIs('kopya'); setDurum(null);
    try {
      const { metinDosyasi } = await import('../../services/metinDisaAktar');
      const yazi = (await (await metinDosyasi(await kur('txt'), 'txt')).text()).replace(/^﻿/, '');
      await navigator.clipboard.writeText(yazi);
      setDurum({ tur: 'ok', yazi: 'Metin panoya kopyalandı.' });
    } catch {
      setDurum({ tur: 'hata', yazi: 'Kopyalanamadı; düz metin olarak indirebilirsin.' });
    } finally { setIs(null); }
  };

  const bolumler = detay?.bolumler || [];
  const seciliN = bolum ? bolum.size : bolumler.length;
  const bolumDegis = (i: number, on: boolean) => {
    const n = new Set(bolum || bolumler.map((_, k) => k));
    if (on) n.add(i); else n.delete(i);
    setBolum(n.size === bolumler.length ? null : n);
  };

  return (
    <div className="tp-perde" data-ls-keep role="presentation" onClick={(e) => { if (e.target === e.currentTarget && !is) onKapat(); }}>
      <div className="tp-kart cap-kart" role="dialog" aria-modal="true" aria-labelledby="cap-b">
        <header className="tp-bas">
          <span className="cap-baslik">
            <b id="cap-b" className="tp-baslik"><FileDown aria-hidden /> Ders metnini dışa aktar</b>
            {detay && <small>{etiket ? `${etiket} · ` : ''}{detay.baslik}</small>}
          </span>
          <button ref={kapatRef} type="button" className="tp-btn is-ikon" onClick={onKapat} aria-label="Kapat"><X aria-hidden /></button>
        </header>
        <div className="tp-govde">
          {!detay ? (
            yukHata ? <p className="cap-durum is-hata" role="alert">{yukHata}</p> : <p className="cap-durum" role="status"><Loader2 aria-hidden className="cap-don" /> Ders metni alınıyor…</p>
          ) : (
            <>
              <fieldset className="tp-ayar" disabled={!!is}>
                <legend className="cap-leg">Biçim</legend>
                <BicimSecici deger={bicim} onDegis={setBicim} ad="cap" />
              </fieldset>

              <fieldset className="tp-ayar" disabled={!!is}>
                <legend className="cap-leg">İçerik</legend>
                <CdSecenekAlani deger={secenek} onDegis={setSecenek} ad="cap" varlik={varlik} bicim={bicim} />
              </fieldset>

              {bolumler.length > 1 && (
                <details className="tp-ayar cap-bolum">
                  <summary><b>Bölümler</b><small>{seciliN === bolumler.length ? `tümü (${bolumler.length})` : `${seciliN} / ${bolumler.length} seçili`}</small></summary>
                  <div className="tp-hizli">
                    <button type="button" className="tp-btn" disabled={!!is} onClick={() => setBolum(null)}>Tümünü seç</button>
                    <button type="button" className="tp-btn" disabled={!!is} onClick={() => setBolum(new Set())}>Temizle</button>
                  </div>
                  <ul>
                    {bolumler.map((b, i) => (
                      <li key={i}>
                        <label>
                          <input type="checkbox" disabled={!!is} checked={!bolum || bolum.has(i)} onChange={(e) => bolumDegis(i, e.target.checked)} />
                          <span className="tp-no">{i + 1}</span><span className="tp-ad">{b.baslik}</span>
                        </label>
                      </li>
                    ))}
                  </ul>
                </details>
              )}

              {bicim === 'pdf' && (
                <fieldset className="tp-ayar" disabled={!!is}>
                  <legend className="cap-leg">Görünüm</legend>
                  <PdfAyarDugme ad="cap-duzen" deger={duzen} onDegis={setDuzen} />
                  <label className="cap-onizle-ac">
                    <input type="checkbox" checked={onizle} onChange={(e) => setOnizle(e.target.checked)} /> Bu dersin metniyle önizle <small>(ilk bölümler)</small>
                  </label>
                  {onizle && ornek && !bos && (
                    <div className="cap-onizle">
                      <React.Suspense fallback={<p className="cap-durum" role="status"><Loader2 aria-hidden className="cap-don" /> Önizleme hazırlanıyor…</p>}>
                        <PdfOnizleme d={duzen} belge={ornek} />
                      </React.Suspense>
                    </div>
                  )}
                </fieldset>
              )}
            </>
          )}
        </div>
        <footer className="tp-alt">
          <span className={`tp-not${durum ? ` cap-sonuc is-${durum.tur}` : ''}`} role="status" aria-live="polite">
            {durum ? <>{durum.tur === 'ok' && <Check aria-hidden />}{durum.yazi}</>
              : bos ? 'Bu seçimle belgeye girecek metin yok; kapsamı ya da bölümleri değiştir.'
              : belge ? `${belge.bolumler.length} bölüm · yaklaşık ${kelimeSay(belge).toLocaleString('tr-TR')} kelime · dosya cihazında hazırlanır`
              : 'Dosya cihazında hazırlanır.'}
          </span>
          <span className="cap-dugmeler">
            <button type="button" className="tp-btn" disabled={!detay || !!is || bos} onClick={kopyala}>
              {is === 'kopya' ? <Loader2 aria-hidden className="cap-don" /> : <Copy aria-hidden />} Kopyala
            </button>
            <button type="button" className="tp-btn is-ana" disabled={!detay || !!is || bos} onClick={indir}>
              {is === 'indir' ? <Loader2 aria-hidden className="cap-don" /> : <Download aria-hidden />} {CD_BICIMLER.find((b) => b.id === bicim)!.ad} indir
            </button>
          </span>
        </footer>
      </div>
    </div>
  );
}

/** Düğme + pencere. `detay` verilmezse ders metni pencere açılınca alınır (ders sayfası, ders listesi). */
export function SesliMetinAktarDugme({ dersKey, detay, vurguAcik, sinif = 'cd-btn', etiket = 'Metni dışa aktar', yalnizIkon }: {
  dersKey: string; detay?: CdDetay; vurguAcik?: boolean; sinif?: string; etiket?: string; yalnizIkon?: boolean;
}) {
  const [acik, setAcik] = useState(false);
  return (
    <>
      <button type="button" className={sinif} onClick={() => setAcik(true)} aria-haspopup="dialog" aria-label={yalnizIkon ? etiket : undefined} title="Ders metnini PDF, Word ya da metin dosyası olarak indir">
        <FileDown aria-hidden /> {!yalnizIkon && <span>{etiket}</span>}
      </button>
      {acik && createPortal(<CdAktarPencere dersKey={dersKey} detay={detay} vurguAcik={vurguAcik} onKapat={() => setAcik(false)} />, document.body)}
    </>
  );
}
