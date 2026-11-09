/**
 * Toplu PDF indirme (sesli dersler, etkileşimli dersler): seçilen derslerin metinlerini tek seferde indirir.
 *  - Her ders ayrı PDF, tek ZIP dosyasında
 *  - Tek PDF: ilk sayfada içindekiler, her ders yeni sayfada, PDF yer imleriyle
 * Dersler sırayla hazırlanır; ilerleme gösterilir, iptal edilebilir, alınamayanlar atlanıp sonda listelenir.
 * Belge üretimi çağırana aittir (`belgeAl`): tek ders "Metni indir" ile aynı biçim kullanılır.
 * Dosya türü PDF, Word, Markdown ya da düz metin olabilir; çağıran kendi içerik seçeneklerini `ekAyar` ile pencereye koyar.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { createPortal } from 'react-dom';
import { FileDown, X } from 'lucide-react';
import type { AktarBelge, AktarBicim, AktarBolum } from '../../services/metinDisaAktar';
import { duzenOku, duzenYaz, type PdfDuzen } from '../../services/pdfDuzen';
import { PdfAyarDugme } from './PdfDuzenSecici';
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
  /** Çağıranın kendi içerik seçenekleri (durumu çağıranda; belgeAl okur) */
  ekAyar?: React.ReactNode;
  dugmeSinif?: string;
  /** düğme yazısı (varsayılan "Toplu PDF") */
  dugmeYazi?: string;
  /** iş bitince (PDF sihirbazının geçmişi için) */
  onBitti?: (s: { tamam: number; atlanan: number; bicim: 'zip' | 'tek' }) => void;
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
      <button type="button" className={p.dugmeSinif || 'tp-btn'} onClick={() => setAcik(true)} aria-haspopup="dialog" title="Birden çok dersin metnini PDF, Word ya da metin dosyası olarak indir">
        <FileDown aria-hidden /> <span>{p.dugmeYazi || 'Toplu PDF'}</span>
      </button>
      {/* body'ye taşınır: sayfa kabının katman bağlamında kalınca v15 üst/alt çubuğu pencerenin üstüne biniyordu */}
      {acik && createPortal(<TopluPdfDiyalog {...p} onKapat={() => setAcik(false)} />, document.body)}
    </>
  );
}

const TURLER: [AktarBicim, string][] = [['pdf', 'PDF'], ['docx', 'Word'], ['md', 'Markdown'], ['txt', 'Düz metin']];

function TopluPdfDiyalog({ ad, ogeler, belgeAl, secenek, ekAyar, altMetin, onKapat, onBitti }: TopluPdfProps & { onKapat: () => void }) {
  const gruplar = useMemo(() => {
    const m = new Map<string, TopluOge[]>();
    for (const o of ogeler) m.set(o.grup, [...(m.get(o.grup) || []), o]);
    return [...m.entries()].map(([grup, l]) => ({ grup, l }));
  }, [ogeler]);
  const sirali = useMemo(() => gruplar.flatMap((g) => g.l), [gruplar]);
  const [secili, setSecili] = useState<Set<string>>(() => new Set(ogeler.map((d) => d.key)));
  const [bicim, setBicim] = useState<'zip' | 'tek'>('zip');
  const [tur, setTur] = useState<AktarBicim>('pdf');
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
    lockScroll();
    return () => { document.removeEventListener('keydown', k); unlockScroll(); iptal.current = true; };
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
    const metinDosyasi = async (b: AktarBelge) => (tur === 'pdf' ? pdfDuzenle(await hamPdf(b, 'pdf', duzen), duzen) : hamPdf(b, tur));
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
          const blob = await metinDosyasi(belge);
          let dosya = `${String(i + 1).padStart(2, '0')} ${dosyaAdi(tamAd)}.${tur}`;
          while (adlar.has(dosya)) dosya = dosya.replace(/\.\w+$/, ` (2).${tur}`);
          adlar.add(dosya);
          dosyalar.push([dosya, new Uint8Array(await blob.arrayBuffer())]);
        } else {
          icindekiler.push(`- ${d.etiket ? `**${d.etiket}** ` : ''}${d.baslik}`);
          // PDF: yeni sayfa + ders başlığı + yer imi; öteki türlerde ders adı ayrı başlık satırı olur
          if (tur !== 'pdf' && belge.bolumler.length) birlesik.push({ baslik: tamAd, alt: belge.alt, md: '' });
          belge.bolumler.forEach((b, j) => birlesik.push(j === 0 && tur === 'pdf' ? { ...b, ders: { baslik: tamAd, alt: belge.alt } } : b));
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
        indir(await metinDosyasi(belge), `${ad} - ${icindekiler.length} ders - ${tarih}.${tur}`);
      }
    } catch (e) {
      atlanan.push(`Dosya oluşturulamadı${e instanceof Error && e.message ? `: ${e.message}` : ''}`);
    }
    setSonuc({ tamam: bicim === 'zip' ? dosyalar.length : icindekiler.length, atlanan });
    onBitti?.({ tamam: bicim === 'zip' ? dosyalar.length : icindekiler.length, atlanan: atlanan.length, bicim });
    setIs(null);
  };

  return (
    <div className="tp-perde" role="presentation" onClick={(e) => { if (e.target === e.currentTarget && !calisiyor) onKapat(); }}>
      <div className="tp-kart" role="dialog" aria-modal="true" aria-labelledby="tp-b">
        <header className="tp-bas">
          <b id="tp-b" className="tp-baslik"><FileDown aria-hidden /> Toplu dışa aktar</b>
          <button ref={kapatRef} type="button" className="tp-btn is-ikon" onClick={() => { iptal.current = true; onKapat(); }} aria-label="Kapat"><X aria-hidden /></button>
        </header>
        <div className="tp-govde">
          <fieldset className="tp-ayar" disabled={calisiyor}>
            <legend className="tp-gizli">Biçim</legend>
            <div className="tp-tur" role="radiogroup" aria-label="Dosya türü">
              {TURLER.map(([id, a]) => (
                <label key={id} className={tur === id ? 'is-on' : ''}><input type="radio" name="tp-tur" checked={tur === id} onChange={() => setTur(id)} />{a}</label>
              ))}
            </div>
            <label><input type="radio" name="tp-bicim" checked={bicim === 'zip'} onChange={() => setBicim('zip')} /> Her ders ayrı dosya <small>(tek ZIP dosyası)</small></label>
            <label><input type="radio" name="tp-bicim" checked={bicim === 'tek'} onChange={() => setBicim('tek')} /> Tek dosya <small>(içindekiler + dersler art arda{tur === 'pdf' ? ', her ders yeni sayfada' : ''})</small></label>
            {secenek?.vurgu && <label><input type="checkbox" checked={vurgu} onChange={(e) => setVurgu(e.target.checked)} /> Önemli yer işaretleri</label>}
            {secenek?.basliklar && <label><input type="checkbox" checked={basliklar} onChange={(e) => setBasliklar(e.target.checked)} /> Slayt başlıkları <small>(daha yavaş)</small></label>}
          </fieldset>

          {ekAyar && (
            <fieldset className="tp-ayar" disabled={calisiyor}>
              <legend className="tp-gizli">İçerik</legend>
              {ekAyar}
            </fieldset>
          )}

          {tur === 'pdf' && (
            <fieldset className="tp-ayar" disabled={calisiyor}>
              <legend className="tp-gizli">Sayfa düzeni</legend>
              <PdfAyarDugme ad="tp-duzen" deger={duzen} onDegis={setDuzen} />
            </fieldset>
          )}

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
