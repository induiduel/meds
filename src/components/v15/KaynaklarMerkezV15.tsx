import React from 'react';
import { ChevronRight, FileDown, MessagesSquare, NotebookPen, Search } from 'lucide-react';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import { NAV_ITEMS, openSearch } from '../shell/navModel';
import { MERKEZ_ARACLARI } from '../merkez/merkezModel';
import { useV15Baslik } from './baslik';
import '../../styles/v15/dersler.css';
import '../../styles/v15/ek15.css';

/**
 * v15 · Başvuru merkezi (tasarım sistemi v15 › G01). Kurulsuz: üstte genel arama girişi (terim, hastalık, ilaç; arama
 * paletini açar), altında "ne zaman kullanılır" cümleli kaynak kartları (merkezModel.MERKEZ_ARACLARI.kaynaklar).
 */
const TON: Partial<Record<AppRoute, string>> = { oncelikli_dersler: '', glossary: 'is-c', diseases: 'is-b', health_ministry: 'is-ok', kazanimlar: 'is-ai', gecmis_kurullar: 'is-w', guncellemeler: '' };
const git = (url: string) => linkClick(() => navigateTo(url));

/** PdfSihirbaziV15 geçmişi (cihazda; dosyanın kendisi değil, ne üretildiği) */
const pdfSayisi = () => { try { const g = JSON.parse(localStorage.getItem('medsoru_pdf_gecmis_v1') || '[]'); return Array.isArray(g) ? g.length : 0; } catch { return 0; } };

export default function KaynaklarMerkezV15() {
  const nPdf = pdfSayisi();
  // Z05 "Topluluk ve belgeler": yalnız gerçek sayfalara giden satırlar
  const topluluk: { url: string; ad: string; alt: string; ic: React.ElementType; ton: string }[] = [
    { url: '/topluluk?gorunum=sohbetler', ad: 'Sohbet', alt: 'Sınıf grupları ve birebir sohbetler', ic: MessagesSquare, ton: 'is-a' },
    { url: '/notlarim?gorunum=paylasilan', ad: 'Paylaşılan notlar', alt: 'Seninle paylaşılan ders notları', ic: NotebookPen, ton: 'is-w' },
    ...(nPdf > 0 ? [{ url: pathFor('pdf_olustur'), ad: 'Oluşturduğum PDF’ler', alt: `${nPdf} belge · bu cihazda`, ic: FileDown, ton: '' }] : []),
    // H405: "Kurul takvimi" kartı Sınav takvimi'nin (/kamplar/takvim) ikinci adıydı; kanonik giriş Sınava hazırlan › Sınav takvimi
  ];
  useV15Baslik({ baslik: 'Başvuru', alt: 'Sözlük, hastalıklar, resmî veriler ve kazanımlar' }); // H400: geçmiş kurullar kurul seçicide
  const araclar = MERKEZ_ARACLARI.kaynaklar.filter((a) => NAV_ITEMS[a.id]);
  return (
    <div className="d15 k15">
      <h1 className="sr-only">Başvuru</h1>
      <button type="button" className="g15-ara" onClick={openSearch}>
        <Search aria-hidden />
        <span>Terim, hastalık, ilaç ya da kazanım ara</span>
        <kbd>⌘K</kbd>
      </button>
      <div className="k15-alan">
        <ul className="k15-izgara" role="list">
          {araclar.map((a) => {
            const it = NAV_ITEMS[a.id];
            const url = pathFor(a.id);
            return (
              <li key={a.id}>
                <a className="k15-kart v15-card" href={url} onClick={git(url)}>
                  <span className={`v15-tile ${TON[a.id] ?? ''}`}><it.icon aria-hidden /></span>
                  <span className="k15-kart-t">
                    <b>{it.label}{a.oner && <span className="v15-tag is-a">Önerilen</span>}</b>
                    <span>{a.ne}</span>
                  </span>
                  <ChevronRight className="v15-chev" aria-hidden />
                </a>
              </li>
            );
          })}
        </ul>
        <section className="k15-plan" aria-labelledby="k15-top-b">
          <h2 id="k15-top-b" className="v15-cap">Topluluk ve belgeler</h2>
          <ul className="k15-izgara" role="list">
            {topluluk.map((t) => (
              <li key={t.url}>
                <a className="k15-kart v15-card" href={t.url} onClick={git(t.url)}>
                  <span className={`v15-tile ${t.ton}`}><t.ic aria-hidden /></span>
                  <span className="k15-kart-t"><b>{t.ad}</b><span>{t.alt}</span></span>
                  <ChevronRight className="v15-chev" aria-hidden />
                </a>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}
