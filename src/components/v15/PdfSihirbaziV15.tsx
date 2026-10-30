import React, { useEffect, useMemo, useState } from 'react';
import { BookOpen, Check, ChevronRight, FileDown, Headphones, History, ListChecks, Trash2 } from 'lucide-react';
import { linkClick, navigateTo, pathFor } from '../../router';
import { cdListeGetir, type CdListeDers } from '../canliDers/canliDersStore';
import { cdTekSurum } from '../canliDers/canliDersKategori';
import { TopluPdfDugme as SesliPdf } from '../canliDers/CanliDersTopluPdf';
import { TopluPdfDugme } from '../ui/TopluPdf';
import { deckName, loadDeck, loadDeckCatalog, type DeckCatalogEntry } from '../../data/deckStore';
import { dersKurulu } from './dersVeri';
import { useV15Baslik } from './baslik';
import '../../styles/toplu-pdf.css';
import '../../styles/v15/ogren.css';
import '../../styles/v15/dersler.css';
import '../../styles/v15/pdfsihirbaz.css';

/**
 * v15 · PDF oluştur sihirbazı (tasarım sistemi v15 › Y07–Y13). Yeni sayfa: /pdf-olustur (Menü › Araçlar › PDF oluştur).
 * Adımlar: 1 kaynak (sesli ders metinleri · etkileşimli dersler · 2025-26 arşivi) → 2 kurul → 3 dersleri seç ve oluştur.
 * Seçim, biçim (her ders ayrı ZIP / tek PDF), sayfa düzeni ve üretim ortak pencerede (components/ui/TopluPdf);
 * PDF tarayıcıda üretilir, sunucuya yük yok. Geçmiş cihazda tutulur (dosyanın kendisi değil, ne üretildiği).
 */
type Kaynak = 'sesli' | 'ogren' | 'arsiv';
interface Gecmis { ad: string; kaynak: Kaynak; kurul: number; n: number; bicim: 'zip' | 'tek'; at: number }
const GKEY = 'medsoru_pdf_gecmis_v1';
const gOku = (): Gecmis[] => { try { return JSON.parse(localStorage.getItem(GKEY) || '[]'); } catch { return []; } };
const KAYNAK: { id: Kaynak; ad: string; alt: string; Ic: React.ElementType }[] = [
  { id: 'sesli', ad: 'Sesli ders metinleri', alt: 'Konuşma metni, slayt başlıkları ve önemli yer işaretleriyle', Ic: Headphones },
  { id: 'ogren', ad: 'Etkileşimli dersler', alt: 'Adım adım ders anlatımı', Ic: BookOpen },
  { id: 'arsiv', ad: '2025-26 arşivi', alt: 'Geçen yılın sesli ders metinleri', Ic: History },
];
const kurulOf = (d: DeckCatalogEntry) => Number(String(d.committee || '').match(/Kurul\s*(\d+)/i)?.[1] || 0);

export default function PdfSihirbaziV15() {
  const [kaynak, setKaynak] = useState<Kaynak>('sesli');
  const [kurul, setKurul] = useState<number | null>(null);
  const [sesli, setSesli] = useState<CdListeDers[] | null>(null);
  const [arsiv, setArsiv] = useState<CdListeDers[] | null>(null);
  const [desteler, setDesteler] = useState<DeckCatalogEntry[] | null>(null);
  const [gecmis, setGecmis] = useState<Gecmis[]>(gOku);
  useV15Baslik({ baslik: 'PDF oluştur', alt: 'Ders metinlerini indir' });

  useEffect(() => {
    if (kaynak === 'sesli' && !sesli) cdListeGetir().then((d) => setSesli(cdTekSurum(d.filter((x) => !/-son-prova-|-blok-ozet-/.test(x.key)))), () => setSesli([]));
    if (kaynak === 'arsiv' && !arsiv) cdListeGetir(false, '2025-2026').then(setArsiv, () => setArsiv([]));
    if (kaynak === 'ogren' && !desteler) {
      Promise.all([loadDeckCatalog(), import('../learn/LearnLibrary')]).then(([k, m]) => setDesteler(k.filter((d) => m.isPublished(d))), () => setDesteler([]));
    }
  }, [kaynak, sesli, arsiv, desteler]);

  const liste = kaynak === 'sesli' ? sesli : kaynak === 'arsiv' ? arsiv : null;
  const kurullar = useMemo(() => {
    const m = new Map<number, number>();
    if (kaynak === 'ogren') for (const d of desteler || []) { const k = kurulOf(d); if (k) m.set(k, (m.get(k) || 0) + 1); }
    else for (const d of liste || []) { const k = dersKurulu(d); m.set(k, (m.get(k) || 0) + 1); }
    return [...m].sort((a, b) => a[0] - b[0]);
  }, [kaynak, liste, desteler]);
  useEffect(() => { if (kurullar.length && (kurul == null || !kurullar.some(([k]) => k === kurul))) setKurul(kurullar[kurullar.length - 1][0]); }, [kurullar, kurul]);

  const secSesli = useMemo(() => (liste || []).filter((d) => dersKurulu(d) === kurul), [liste, kurul]);
  const secDeste = useMemo(() => (desteler || []).filter((d) => kurulOf(d) === kurul), [desteler, kurul]);
  const yukleniyor = kaynak === 'ogren' ? desteler === null : liste === null;
  const n = kaynak === 'ogren' ? secDeste.length : secSesli.length;
  const kAd = KAYNAK.find((k) => k.id === kaynak)!.ad;

  const kaydet = (s: { tamam: number; bicim: 'zip' | 'tek' }) => {
    if (!s.tamam || kurul == null) return;
    const g = [{ ad: `${kAd} · Kurul ${kurul}`, kaynak, kurul, n: s.tamam, bicim: s.bicim, at: Date.now() }, ...gOku()].slice(0, 30);
    try { localStorage.setItem(GKEY, JSON.stringify(g)); } catch { /* yok */ }
    setGecmis(g);
  };

  return (
    <div className="ps15">
      <h1 className="sr-only">PDF oluştur</h1>
      <a className="v15-card ps15-soru" href={pathFor('soru_aktar')} onClick={linkClick(() => navigateTo(pathFor('soru_aktar')))}>
        <span className="v15-tile is-a"><ListChecks aria-hidden /></span>
        <span><b>Soruları mı indirmek istiyorsun?</b><small>Çıkmış, örnek, çözücü ve hoca sorularını seç; 1-2-4-8 düzen, tasarım modu ve çözüm seçenekleriyle PDF, Word ya da PowerPoint indir.</small></span>
        <ChevronRight aria-hidden />
      </a>
      <section className="v15-card ps15-adim">
        <h2><span>1</span>Ne indirmek istiyorsun?</h2>
        <div className="ps15-kaynak" role="radiogroup" aria-label="Kaynak">
          {KAYNAK.map(({ id, ad, alt, Ic }) => (
            <button key={id} type="button" role="radio" aria-checked={kaynak === id} className={`ps15-k${kaynak === id ? ' is-on' : ''}`} onClick={() => { setKaynak(id); setKurul(null); }}>
              <Ic aria-hidden /><span><b>{ad}</b><small>{alt}</small></span>{kaynak === id && <Check aria-hidden className="ps15-ok" />}
            </button>
          ))}
        </div>
      </section>

      <section className="v15-card ps15-adim">
        <h2><span>2</span>Hangi kurul?</h2>
        {yukleniyor ? <span className="v15-skel b15-skel" aria-hidden /> : !kurullar.length ? <p className="v15-cap">Bu kaynakta ders yok.</p> : (
          <div className="o15-cipler v15-hscroll" role="radiogroup" aria-label="Kurul">
            {kurullar.map(([k, c]) => <button key={k} type="button" role="radio" aria-checked={kurul === k} className={`o15-cip${kurul === k ? ' is-on' : ''}`} onClick={() => setKurul(k)}>Kurul {k} · {c}</button>)}
          </div>
        )}
      </section>

      <section className="v15-card ps15-adim">
        <h2><span>3</span>Dersleri seç ve oluştur</h2>
        <p className="v15-cap">Açılan pencerede istemediğin dersleri çıkar; her dersi ayrı PDF (ZIP) ya da tek PDF olarak, içindekiler sayfasıyla indir.</p>
        {!yukleniyor && n > 0 && kurul != null && (
          <div className="ps15-olustur">
            {kaynak === 'ogren' ? (
              <TopluPdfDugme
                ad={`Etkileşimli dersler · Kurul ${kurul}`}
                dugmeSinif="ps15-btn"
                dugmeYazi={`${n} dersi seç ve oluştur`}
                ogeler={secDeste.map((d) => ({ key: d.id, grup: d.discipline || 'Diğer', baslik: deckName(d) }))}
                belgeAl={async (key) => {
                  const [d, { ogrenAktarBelgesi }] = await Promise.all([loadDeck<any>(key), import('../learn/lesson/ogrenAktar')]);
                  if (!d || !Array.isArray(d.slides) || !d.slides.length) throw new Error('ders yüklenemedi');
                  return ogrenAktarBelgesi(d);
                }}
                altMetin={(x) => `${x} ders · etkileşimli ders metinleri`}
                onBitti={kaydet}
              />
            ) : (
              <SesliPdf dersler={secSesli} ad={`${kaynak === 'arsiv' ? '2025-26 arşivi' : 'Sesli dersler'} · Kurul ${kurul}`} dugmeYazi={`${n} dersi seç ve oluştur`} dugmeSinif="ps15-btn" onBitti={kaydet} />
            )}
          </div>
        )}
      </section>

      {gecmis.length > 0 && (
        <section className="ps15-gecmis">
          <div className="ps15-gb"><h2 className="v15-cap">Geçmiş</h2>
            <button type="button" className="v15-ib" aria-label="Geçmişi temizle" onClick={() => { try { localStorage.removeItem(GKEY); } catch { /* yok */ } setGecmis([]); }}><Trash2 aria-hidden /></button>
          </div>
          <ul className="b15-list v15-card">
            {gecmis.map((g) => (
              <li key={g.at}>
                <button type="button" className="b15-row" onClick={() => { setKaynak(g.kaynak); setKurul(g.kurul); window.scrollTo({ top: 0, behavior: 'smooth' }); }}>
                  <span className="v15-tile is-n"><FileDown aria-hidden /></span>
                  <span className="b15-row-t"><b>{g.ad}</b><span>{g.n} ders · {g.bicim === 'zip' ? 'ayrı PDF (ZIP)' : 'tek PDF'} · {new Date(g.at).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })}</span></span>
                </button>
              </li>
            ))}
          </ul>
          <p className="v15-cap">Dosyalar cihazına indirildi; satıra dokunursan aynı seçimle yeniden oluşturabilirsin.</p>
        </section>
      )}
    </div>
  );
}
