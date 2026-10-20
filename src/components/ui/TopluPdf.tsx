/**
 * Toplu PDF indirme (sesli dersler, etkileşimli dersler): seçilen derslerin metinlerini tek seferde indirir.
 *  - Her ders ayrı PDF, tek ZIP dosyasında
 *  - Tek PDF: ilk sayfada içindekiler, her ders yeni sayfada, PDF yer imleriyle
 * Dersler sırayla hazırlanır; ilerleme gösterilir, iptal edilebilir, alınamayanlar atlanıp sonda listelenir.
 * Belge üretimi çağırana aittir (`belgeAl`): tek ders "Metni indir" ile aynı biçim kullanılır.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { FileDown, X } from 'lucide-react';
import type { AktarBelge, AktarBolum } from '../../services/metinDisaAktar';
import { duzenEtiketi, duzenOku, duzenYaz, type PdfDuzen } from '../../services/pdfDuzen';
import { PdfDuzenSecici } from './PdfDuzenSecici';
import '../../styles/toplu-pdf.css';

export interface TopluOge { key: string; grup: string; etiket?: string; baslik: string }
export interface TopluAyar { vurgu: boolean; basliklar: boolean }
export interface TopluPdfProps {
  /** "Sesli dersler" / "Etkileşimli dersler": dosya adı ve birleşik PDF başlığı */
  ad: string;
  ogeler: TopluOge[];
  belgeAl: (key: string, ayar: TopluAyar) => Promise<AktarBelge>;
  /** Hangi seçenekler gösterilsin (sesli ders: ikisi de; etkileşimli ders: yok) */
  secenek?: { vurgu?: boolean; basliklar?: boolean };
  /** Birleşik PDF'in alt satırı */
  altMetin?: (n: number, ayar: TopluAyar) => string;
  dugmeSinif?: string;
}

const dosyaAdi = (s: string) => s.replace(/[\\/:*?"<>|\u0000-\u001f]/g, '-').replace(/\s+/g, ' ').trim().slice(0, 110);

function indir(blob: Blob, ad: string) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = ad;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}

export function TopluPdfDugme(p: TopluPdfProps) {
  const [acik, setAcik] = useState(false);
  return (
    <>
      <button type="button" className={p.dugmeSinif || 'tp-btn'} onClick={() => setAcik(true)} aria-haspopup="dialog" title="Birden çok dersin metnini PDF olarak indir">
        <FileDown aria-hidden /> <span>Toplu PDF</span>
      </button>
      {acik && <TopluPdfDiyalog {...p} onKapat={() => setAcik(false)} />}
    </>
  );
}

function TopluPdfDiyalog({ ad, ogeler, belgeAl, secenek, altMetin, onKapat }: TopluPdfProps & { onKapat: () => void }) {
  const gruplar = useMemo(() => {
    const m = new Map<string, TopluOge[]>();
    for (const o of ogeler) m.set(o.grup, [...(m.get(o.grup) || []), o]);
    return [...m.entries()].map(([grup, l]) => ({ grup, l }));
  }, [ogeler]);
  const sirali = useMemo(() => gruplar.flatMap((g) => g.l), [gruplar]);
  const [secili, setSecili] = useState<Set<string>>(() => new Set(ogeler.map((d) => d.key)));
  const [bicim, setBicim] = useState<'zip' | 'tek'>('zip');
  const [vurgu, setVurgu] = useState(true);
  const [basliklar, setBasliklar] = useState(true);
  const [duzen, setDuzenH] = useState<PdfDuzen>(duzenOku);
  const setDuzen = (d: PdfDuzen) => { setDuzenH(d); duzenYaz(d); };
  const [is, setIs] = useState<{ i: number; n: number; ad: string } | null>(null);
  const [sonuc, setSonuc] = useState<{ tamam: number; atlanan: string[] } | null>(null);
  const iptal = useRef(false);
  const kapatRef = useRef<HTMLButtonElement>(null);
  const calisiyorRef = useRef(false);
  calisiyorRef.current = !!is;
  const calisiyor = !!is;

  useEffect(() => {
    kapatRef.current?.focus();
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape' && !calisiyorRef.current) onKapat(); };
    document.addEventListener('keydown', k);
    const eski = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.removeEventListener('keydown', k); document.body.style.overflow = eski; iptal.current = true; };
  }, [onKapat]);

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
    const ayar: TopluAyar = { vurgu: !!secenek?.vurgu && vurgu, basliklar: !!secenek?.basliklar && basliklar };
    const { metinDosyasi: hamPdf, zipIkili } = await import('../../services/metinDisaAktar');
    const { pdfDuzenle } = await import('../../services/pdfDuzen');
    const metinDosyasi = async (b: AktarBelge, f: 'pdf') => pdfDuzenle(await hamPdf(b, f), duzen);
    const dosyalar: [string, Uint8Array][] = [];
    const birlesik: AktarBolum[] = [];
    const icindekiler: string[] = [];
    const atlanan: string[] = [];
    const adlar = new Set<string>();
    for (let i = 0; i < secilenler.length; i++) {
      if (iptal.current) break;
      const d = secilenler[i];
      const tamAd = `${d.etiket ? `${d.etiket} - ` : ''}${d.baslik}`;
      setIs({ i: i + 1, n: secilenler.length, ad: tamAd });
      try {
        const belge = await belgeAl(d.key, ayar);
        if (bicim === 'zip') {
          const blob = await metinDosyasi(belge, 'pdf');
          let dosya = `${String(i + 1).padStart(2, '0')} ${dosyaAdi(tamAd)}.pdf`;
          while (adlar.has(dosya)) dosya = dosya.replace(/\.pdf$/, ' (2).pdf');
          adlar.add(dosya);
          dosyalar.push([dosya, new Uint8Array(await blob.arrayBuffer())]);
        } else {
          icindekiler.push(`- ${d.etiket ? `**${d.etiket}** ` : ''}${d.baslik}`);
          belge.bolumler.forEach((b, j) => birlesik.push(j === 0 ? { ...b, ders: { baslik: tamAd, alt: belge.alt } } : b));
        }
      } catch (e) {
        atlanan.push(`${tamAd}${e instanceof Error && e.message ? ` (${e.message})` : ''}`);
      }
      // Arayüz donmasın: dersler arasında tarayıcıya nefes aldır
      await new Promise((r) => setTimeout(r, 0));
    }
    if (iptal.current) { setIs(null); return; }
    const tarih = new Date().toLocaleDateString('tr-TR').replace(/\./g, '-');
    try {
      if (bicim === 'zip' && dosyalar.length) {
        indir(zipIkili(dosyalar), `${ad} - ${dosyalar.length} ders - ${tarih}.zip`);
      } else if (bicim === 'tek' && birlesik.length) {
        const belge: AktarBelge = {
          baslik: ad,
          dersDuzeni: true,
          alt: altMetin ? altMetin(icindekiler.length, ayar) : `${icindekiler.length} ders`,
          bolumler: [{ baslik: 'İçindekiler', md: icindekiler.join('\n') }, ...birlesik],
        };
        indir(await metinDosyasi(belge, 'pdf'), `${ad} - ${icindekiler.length} ders - ${tarih}.pdf`);
      }
    } catch (e) {
      atlanan.push(`Dosya oluşturulamadı${e instanceof Error && e.message ? `: ${e.message}` : ''}`);
    }
    setSonuc({ tamam: bicim === 'zip' ? dosyalar.length : icindekiler.length, atlanan });
    setIs(null);
  };

  return (
    <div className="tp-perde" role="presentation" onClick={(e) => { if (e.target === e.currentTarget && !calisiyor) onKapat(); }}>
      <div className="tp-kart" role="dialog" aria-modal="true" aria-labelledby="tp-b">
        <header className="tp-bas">
          <b id="tp-b" className="tp-baslik"><FileDown aria-hidden /> Toplu PDF indir</b>
          <button ref={kapatRef} type="button" className="tp-btn is-ikon" onClick={() => { iptal.current = true; onKapat(); }} aria-label="Kapat"><X aria-hidden /></button>
        </header>
        <div className="tp-govde">
          <fieldset className="tp-ayar" disabled={calisiyor}>
            <legend className="tp-gizli">Biçim</legend>
            <label><input type="radio" name="tp-bicim" checked={bicim === 'zip'} onChange={() => setBicim('zip')} /> Her ders ayrı PDF <small>(tek ZIP dosyası)</small></label>
            <label><input type="radio" name="tp-bicim" checked={bicim === 'tek'} onChange={() => setBicim('tek')} /> Tek PDF <small>(içindekiler + her ders yeni sayfada)</small></label>
            {secenek?.vurgu && <label><input type="checkbox" checked={vurgu} onChange={(e) => setVurgu(e.target.checked)} /> Önemli yer işaretleri</label>}
            {secenek?.basliklar && <label><input type="checkbox" checked={basliklar} onChange={(e) => setBasliklar(e.target.checked)} /> Slayt başlıkları <small>(daha yavaş)</small></label>}
          </fieldset>

          <fieldset className="tp-ayar" disabled={calisiyor}>
            <legend className="tp-gizli">Sayfa düzeni</legend>
            <b className="tp-alt-baslik">Sayfa düzeni <small>{duzen.nup > 1 ? duzenEtiketi(duzen) : 'tek yaprakta bir sayfa'}</small></b>
            <PdfDuzenSecici ad="tp-duzen" deger={duzen} onDegis={setDuzen} />
          </fieldset>

          <div className="tp-ust">
            <span>{secilenler.length} / {sirali.length} ders seçili</span>
            <span className="tp-hizli">
              <button type="button" className="tp-btn" disabled={calisiyor} onClick={() => setSecili(new Set(sirali.map((d) => d.key)))}>Tümünü seç</button>
              <button type="button" className="tp-btn" disabled={calisiyor} onClick={() => setSecili(new Set())}>Temizle</button>
            </span>
          </div>

          <div className="tp-liste">
            {gruplar.map(({ grup, l }) => {
              const hepsi = l.every((d) => secili.has(d.key));
              const biri = l.some((d) => secili.has(d.key));
              return (
                <section key={grup}>
                  <label className="tp-grup">
                    <input
                      type="checkbox"
                      disabled={calisiyor}
                      checked={hepsi}
                      ref={(el) => { if (el) el.indeterminate = biri && !hepsi; }}
                      onChange={(e) => degis(l.map((d) => d.key), e.target.checked)}
                    />
                    <b>{grup}</b> <span>{l.length}</span>
                  </label>
                  <ul>
                    {l.map((d) => (
                      <li key={d.key}>
                        <label>
                          <input type="checkbox" disabled={calisiyor} checked={secili.has(d.key)} onChange={(e) => degis([d.key], e.target.checked)} />
                          {d.etiket && <span className="tp-no">{d.etiket}</span>}
                          <span className="tp-ad">{d.baslik}</span>
                        </label>
                      </li>
                    ))}
                  </ul>
                </section>
              );
            })}
          </div>
        </div>
        <footer className="tp-alt">
          {is ? (
            <div className="tp-ilerleme" role="status" aria-live="polite">
              <span>{is.i} / {is.n} · {is.ad}</span>
              <span className="tp-cubuk" aria-hidden><i style={{ transform: `scaleX(${is.i / is.n})` }} /></span>
            </div>
          ) : sonuc ? (
            <div className="tp-ilerleme" role="status">
              <span>{sonuc.tamam} ders indirildi{sonuc.atlanan.length ? `, ${sonuc.atlanan.length} ders alınamadı` : ''}.</span>
              {!!sonuc.atlanan.length && <small className="tp-atlanan">{sonuc.atlanan.join(' · ')}</small>}
            </div>
          ) : <span className="tp-not">Metinler cihazında hazırlanır; çok ders seçince birkaç dakika sürebilir.</span>}
          {is ? (
            <button type="button" className="tp-btn" onClick={() => { iptal.current = true; }}>İptal</button>
          ) : (
            <button type="button" className="tp-btn is-ana" disabled={!secilenler.length} onClick={baslat}>
              <FileDown aria-hidden /> {secilenler.length} dersi indir
            </button>
          )}
        </footer>
      </div>
    </div>
  );
}
