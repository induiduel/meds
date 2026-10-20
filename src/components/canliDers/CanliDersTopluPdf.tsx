/**
 * Sesli dersler › Toplu PDF: seçilen derslerin konuşma metinlerini (tek ders "⋯ › Metni indir" ile aynı biçimde,
 * slayt başlıkları ve önemli yer işaretleriyle) tek seferde indirir. İki biçim:
 *  - Her ders ayrı PDF, tek ZIP dosyasında
 *  - Tek PDF: ilk sayfada içindekiler, her ders yeni sayfada, PDF yer imleriyle
 * Dersler sırayla (tek tek) hazırlanır; ilerleme gösterilir, iptal edilebilir, alınamayan dersler atlanıp sonda listelenir.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { FileDown, X } from 'lucide-react';
import { cdDetayGetir, type CdListeDers } from './canliDersStore';
import { cdDersEtiketi, cdKategoriGrupla } from './canliDersKategori';
import { cdAktarBelgesi } from './canliDersDisaAktar';
import type { AktarBelge, AktarBolum } from '../../services/metinDisaAktar';

type Bicim = 'zip' | 'tek';

const dosyaAdi = (s: string) => s.replace(/[\\/:*?"<>|\u0000-\u001f]/g, '-').replace(/\s+/g, ' ').trim().slice(0, 110);

function indir(blob: Blob, ad: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = ad;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}

export function TopluPdfDugme({ dersler }: { dersler: CdListeDers[] }) {
  const [acik, setAcik] = useState(false);
  return (
    <>
      <button type="button" className="cd-btn" onClick={() => setAcik(true)} aria-haspopup="dialog" title="Birden çok dersin metnini PDF olarak indir">
        <FileDown aria-hidden /> <span>Toplu PDF</span>
      </button>
      {acik && <TopluPdfDiyalog dersler={dersler} onKapat={() => setAcik(false)} />}
    </>
  );
}

function TopluPdfDiyalog({ dersler, onKapat }: { dersler: CdListeDers[]; onKapat: () => void }) {
  const gruplar = useMemo(() => cdKategoriGrupla(dersler), [dersler]);
  const sirali = useMemo(() => gruplar.flatMap((g) => g.dersler), [gruplar]);
  const [secili, setSecili] = useState<Set<string>>(() => new Set(dersler.map((d) => d.key)));
  const [bicim, setBicim] = useState<Bicim>('zip');
  const [vurgu, setVurgu] = useState(true);
  const [basliklar, setBasliklar] = useState(true);
  const [is, setIs] = useState<{ i: number; n: number; ad: string } | null>(null);
  const [sonuc, setSonuc] = useState<{ tamam: number; atlanan: string[] } | null>(null);
  const iptal = useRef(false);
  const kapatRef = useRef<HTMLButtonElement>(null);
  const calisiyor = !!is;

  useEffect(() => {
    kapatRef.current?.focus();
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape' && !calisiyorRef.current) onKapat(); };
    document.addEventListener('keydown', k);
    const eski = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.removeEventListener('keydown', k); document.body.style.overflow = eski; iptal.current = true; };
  }, [onKapat]);
  const calisiyorRef = useRef(false);
  calisiyorRef.current = calisiyor;

  const degis = (keys: string[], on: boolean) => setSecili((s) => {
    const n = new Set(s);
    keys.forEach((k) => (on ? n.add(k) : n.delete(k)));
    return n;
  });
  const secilenler = sirali.filter((d) => secili.has(d.key));

  const baslat = async () => {
    if (!secilenler.length) return;
    iptal.current = false;
    setSonuc(null);
    const { metinDosyasi, zipIkili } = await import('../../services/metinDisaAktar');
    const slayt = basliklar ? await import('./cdSlaytBasliklari').then((m) => m.cdSlaytBasliklari).catch(() => null) : null;
    const dosyalar: [string, Uint8Array][] = [];
    const birlesik: AktarBolum[] = [];
    const icindekiler: string[] = [];
    const atlanan: string[] = [];
    const adlar = new Set<string>();
    for (let i = 0; i < secilenler.length; i++) {
      if (iptal.current) break;
      const d = secilenler[i];
      const etiket = cdDersEtiketi(d);
      const ad = `${etiket ? `${etiket} - ` : ''}${d.baslik}`;
      setIs({ i: i + 1, n: secilenler.length, ad });
      try {
        const detay = await cdDetayGetir(d.key);
        const bas = slayt ? await slayt(detay).catch(() => undefined) : undefined;
        const belge = cdAktarBelgesi(detay, cdDersEtiketi(detay) || etiket, vurgu, bas);
        if (bicim === 'zip') {
          const blob = await metinDosyasi(belge, 'pdf');
          let dosya = `${String(i + 1).padStart(2, '0')} ${dosyaAdi(ad)}.pdf`;
          while (adlar.has(dosya)) dosya = dosya.replace(/\.pdf$/, ' (2).pdf');
          adlar.add(dosya);
          dosyalar.push([dosya, new Uint8Array(await blob.arrayBuffer())]);
        } else {
          icindekiler.push(`- **${etiket || d.no}** ${d.baslik}`);
          belge.bolumler.forEach((b, j) => birlesik.push(j === 0 ? { ...b, ders: { baslik: ad, alt: belge.alt } } : b));
        }
      } catch (e) {
        atlanan.push(`${ad}${e instanceof Error && e.message ? ` (${e.message})` : ''}`);
      }
      // Arayüz donmasın: dersler arasında tarayıcıya nefes aldır
      await new Promise((r) => setTimeout(r, 0));
    }
    if (iptal.current) { setIs(null); return; }
    const tarih = new Date().toLocaleDateString('tr-TR').replace(/\./g, '-');
    try {
      if (bicim === 'zip' && dosyalar.length) {
        indir(zipIkili(dosyalar), `Sesli dersler - ${dosyalar.length} ders - ${tarih}.zip`);
      } else if (bicim === 'tek' && birlesik.length) {
        const belge: AktarBelge = {
          baslik: 'Sesli dersler',
          dersDuzeni: true,
          alt: `${icindekiler.length} ders · konuşma metinleri${vurgu ? ' · işaretli yerler çıkmış, örnek soru ve spotlarla eşleşen önemli bilgiler' : ''}`,
          bolumler: [{ baslik: 'İçindekiler', md: icindekiler.join('\n') }, ...birlesik],
        };
        indir(await metinDosyasi(belge, 'pdf'), `Sesli dersler - ${icindekiler.length} ders - ${tarih}.pdf`);
      }
    } catch (e) {
      atlanan.push(`Dosya oluşturulamadı${e instanceof Error && e.message ? `: ${e.message}` : ''}`);
    }
    setSonuc({ tamam: bicim === 'zip' ? dosyalar.length : icindekiler.length, atlanan });
    setIs(null);
  };

  return (
    <div className="cd-dlg" role="presentation" onClick={(e) => { if (e.target === e.currentTarget && !calisiyor) onKapat(); }}>
      <div className="cd-dlg-kart is-genis cd-toplu" role="dialog" aria-modal="true" aria-labelledby="cd-tp-b">
        <header className="cd-dlg-bas">
          <b id="cd-tp-b" className="cd-dlg-baslik"><FileDown aria-hidden /> Toplu PDF indir</b>
          <button ref={kapatRef} type="button" className="cd-btn is-ikon" onClick={() => { iptal.current = true; onKapat(); }} aria-label="Kapat"><X aria-hidden /></button>
        </header>
        <div className="cd-dlg-govde">
          <fieldset className="cd-toplu-ayar" disabled={calisiyor}>
            <legend className="sr-only">Biçim</legend>
            <label><input type="radio" name="cd-tp-bicim" checked={bicim === 'zip'} onChange={() => setBicim('zip')} /> Her ders ayrı PDF <small>(tek ZIP dosyası)</small></label>
            <label><input type="radio" name="cd-tp-bicim" checked={bicim === 'tek'} onChange={() => setBicim('tek')} /> Tek PDF <small>(içindekiler + her ders yeni sayfada)</small></label>
            <label><input type="checkbox" checked={vurgu} onChange={(e) => setVurgu(e.target.checked)} /> Önemli yer işaretleri</label>
            <label><input type="checkbox" checked={basliklar} onChange={(e) => setBasliklar(e.target.checked)} /> Slayt başlıkları <small>(daha yavaş)</small></label>
          </fieldset>

          <div className="cd-toplu-ust">
            <span>{secilenler.length} / {sirali.length} ders seçili</span>
            <span className="cd-toplu-hizli">
              <button type="button" className="cd-btn" disabled={calisiyor} onClick={() => setSecili(new Set(sirali.map((d) => d.key)))}>Tümünü seç</button>
              <button type="button" className="cd-btn" disabled={calisiyor} onClick={() => setSecili(new Set())}>Temizle</button>
            </span>
          </div>

          <div className="cd-toplu-liste">
            {gruplar.map(({ kat, dersler: ds }) => {
              const hepsi = ds.every((d) => secili.has(d.key));
              const biri = ds.some((d) => secili.has(d.key));
              return (
                <section key={kat.id}>
                  <label className="cd-toplu-grup">
                    <input
                      type="checkbox"
                      disabled={calisiyor}
                      checked={hepsi}
                      ref={(el) => { if (el) el.indeterminate = biri && !hepsi; }}
                      onChange={(e) => degis(ds.map((d) => d.key), e.target.checked)}
                    />
                    <b>{kat.ad}</b> <span>{ds.length}</span>
                  </label>
                  <ul>
                    {ds.map((d) => (
                      <li key={d.key}>
                        <label>
                          <input type="checkbox" disabled={calisiyor} checked={secili.has(d.key)} onChange={(e) => degis([d.key], e.target.checked)} />
                          <span className="cd-toplu-no">{cdDersEtiketi(d)}</span>
                          <span className="cd-toplu-ad">{d.baslik}</span>
                        </label>
                      </li>
                    ))}
                  </ul>
                </section>
              );
            })}
          </div>
        </div>
        <footer className="cd-toplu-alt">
          {is ? (
            <div className="cd-toplu-ilerleme" role="status" aria-live="polite">
              <span>{is.i} / {is.n} · {is.ad}</span>
              <span className="cd-toplu-cubuk" aria-hidden><i style={{ transform: `scaleX(${is.i / is.n})` }} /></span>
            </div>
          ) : sonuc ? (
            <div className="cd-toplu-ilerleme" role="status">
              <span>{sonuc.tamam} ders indirildi{sonuc.atlanan.length ? `, ${sonuc.atlanan.length} ders alınamadı` : ''}.</span>
              {!!sonuc.atlanan.length && <small className="cd-toplu-atlanan">{sonuc.atlanan.join(' · ')}</small>}
            </div>
          ) : <span className="cd-toplu-not">Metinler cihazında hazırlanır; çok ders seçince birkaç dakika sürebilir.</span>}
          {is ? (
            <button type="button" className="cd-btn" onClick={() => { iptal.current = true; }}>İptal</button>
          ) : (
            <button type="button" className="cd-btn is-ana" disabled={!secilenler.length} onClick={baslat}>
              <FileDown aria-hidden /> {secilenler.length} dersi indir
            </button>
          )}
        </footer>
      </div>
    </div>
  );
}
