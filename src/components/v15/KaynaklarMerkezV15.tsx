import React from 'react';
import { FileDown, MessagesSquare, NotebookPen, Search } from 'lucide-react';
import { pathFor } from '../../router';
import { KlinikDizin } from './klinik/KlinikDizin';
import { NAV_ITEMS, openSearch } from '../shell/navModel';
import { MERKEZ_ARACLARI } from '../merkez/merkezModel';
import { useV15Baslik } from './baslik';
import '../../styles/v15/dersler.css';
import '../../styles/v15/ek15.css';

/**
 * v15 · Başvuru merkezi (tasarım sistemi v15 › G01). Kurulsuz: üstte genel arama girişi (terim, hastalık, ilaç; arama
 * paletini açar), altında "ne zaman kullanılır" cümleli kaynak kartları (merkezModel.MERKEZ_ARACLARI.kaynaklar).
 */

/** PdfSihirbaziV15 geçmişi (cihazda; dosyanın kendisi değil, ne üretildiği) */
const pdfSayisi = () => { try { const g = JSON.parse(localStorage.getItem('medsoru_pdf_gecmis_v1') || '[]'); return Array.isArray(g) ? g.length : 0; } catch { return 0; } };

export default function KaynaklarMerkezV15() {
  const nPdf = pdfSayisi();
  // Z05 "Topluluk ve belgeler": yalnız gerçek sayfalara giden satırlar
  const topluluk: { url: string; ad: string; alt: string; ic: React.ElementType }[] = [
    { url: '/topluluk?gorunum=sohbetler', ad: 'Sohbet', alt: 'Sınıf grupları ve birebir sohbetler', ic: MessagesSquare },
    { url: '/notlarim?gorunum=paylasilan', ad: 'Paylaşılan notlar', alt: 'Seninle paylaşılan ders notları', ic: NotebookPen },
    ...(nPdf > 0 ? [{ url: pathFor('pdf_olustur'), ad: 'Oluşturduğum PDF’ler', alt: `${nPdf} belge · bu cihazda`, ic: FileDown }] : []),
    // H405: "Kurul takvimi" kartı Sınav takvimi'nin (/kamplar/takvim) ikinci adıydı; kanonik giriş Sınava hazırlan › Sınav takvimi
  ];
  useV15Baslik({ baslik: 'Başvuru', alt: 'Sözlük, hastalıklar, resmî veriler ve kazanımlar' }); // H400: geçmiş kurullar kurul seçicide
  const araclar = MERKEZ_ARACLARI.kaynaklar.filter((a) => NAV_ITEMS[a.id]);
  return (
    <div className="d15 k15 kl-merkez">
      <h1 className="sr-only">Başvuru</h1>
      <button type="button" className="kl-ara" onClick={openSearch}>
        <Search aria-hidden />
        <span>Terim, hastalık, ilaç ya da kazanım ara</span>
        <kbd>⌘K</kbd>
      </button>
      {/* H676: karo kartları yerine klinik dizin (Figma › Başvuru) */}
      <div className="kl-dizinler">
        <KlinikDizin
          harf="A"
          baslik="Kaynaklar"
          ogeler={araclar.map((a) => ({ id: a.id, ad: NAV_ITEMS[a.id].label, ne: a.ne, url: pathFor(a.id), ikon: NAV_ITEMS[a.id].icon, etiket: a.oner ? 'Önerilen' : undefined }))}
        />
        <KlinikDizin
          harf="B"
          baslik="Topluluk ve belgeler"
          baslangic={araclar.length + 1}
          ogeler={topluluk.map((t) => ({ id: t.url, ad: t.ad, ne: t.alt, url: t.url, ikon: t.ic }))}
        />
      </div>
    </div>
  );
}
