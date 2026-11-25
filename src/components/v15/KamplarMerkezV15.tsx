import React, { useEffect, useState } from 'react';
import { ClipboardCheck, Download, FileText } from 'lucide-react';
import { KlinikDizin } from './klinik/KlinikDizin';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import SinavAgirligiV15, { sinavAgirligiVar } from './SinavAgirligiV15';
import { NAV_ITEMS } from '../shell/navModel';
import { KURUL_NOLAR, kurulIcerikVar, kurulKaydet, varsayilanKurul } from '../kurul/KurulSecici';
import { CHECKUPLAR, MERKEZ_ARACLARI, PDF_NOTLAR } from '../merkez/merkezModel';
import { menudeGorunur } from '../../services/siteAyar';
import { gorunenSekmeler, SEKME_ROUTE, aracYolu, kampOku, type KampSekme } from '../merkez/MerkezView';
import { useV15Baslik } from './baslik';
import KurulSecV15 from './KurulSecV15';
import '../../styles/v15/dersler.css';
import '../../styles/v15/ek15.css';

/**
 * v15 · Sınava hazırlan merkezi (tasarım sistemi v15 › D01). Sekmeler adrestir (/kamplar/kurulN/<sekme>, site haritası
 * kuralı): Hepsi · Son Prova · Kamplar · Check Up · En önemliler. Kartlar: kurula bağlı araçlar (içerik yoksa
 * "henüz yok"), Check Up'lar ve PDF notlar. Kurul seçimi ve adres mantığı eski merkezle aynı (MerkezView yardımcıları).
 */
const git = (url: string) => linkClick(() => navigateTo(url));

export default function KamplarMerkezV15() {
  const [d, setD] = useState(kampOku);
  useEffect(() => {
    const f = () => setD(kampOku());
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  const kurul = d.kurul ?? varsayilanKurul();
  const sekme: KampSekme = d.sekme;
  const yol = (k: number, s: KampSekme) => `/kamplar/kurul${k}${s === 'hepsi' ? '' : `/${s}`}`;
  const araclar = MERKEZ_ARACLARI.kamplar.filter((a) => NAV_ITEMS[a.id] && (sekme === 'hepsi' || (SEKME_ROUTE[sekme] || []).includes(a.id)));
  const checkup = (sekme === 'hepsi' || sekme === 'checkup') ? CHECKUPLAR.filter((c) => c.kurul === kurul) : [];
  const pdfler = (sekme === 'hepsi' || sekme === 'en-onemliler') ? PDF_NOTLAR.filter((p) => p.kurul === kurul) : [];
  useV15Baslik({ baslik: 'Sınava hazırlan', alt: `Kurul ${kurul}` });

  return (
    <div className="d15 k15">
      <h1 className="sr-only">Sınava hazırlan</h1>
      <div className="k15-ust">
        <nav className="v15-seg k15-sekme" aria-label="Sınava hazırlık bölümleri">
          {gorunenSekmeler().map(([id, ad]) =>
            id === sekme ? <span key={id} aria-current="page">{ad}</span> : <a key={id} href={yol(kurul, id)} onClick={git(yol(kurul, id))}>{ad}</a>,
          )}
        </nav>
        <KurulSecV15 className="s15-kurul" kurul={kurul} onSec={(k) => navigateTo(yol(k, sekme))} />
      </div>

      <div className="k15-alan kl-dizinler">
        {/* H676: karo + kart ızgarası yerine klinik dizin (numaralı satırlar, harfli bölümler) */}
        <KlinikDizin
          harf="A"
          baslik="Hazırlık araçları"
          ogeler={araclar.map((a) => {
            const it = NAV_ITEMS[a.id];
            const bos = kurulIcerikVar(a.id, kurul) === false;
            return { id: a.id, ad: it.label, ne: bos ? `Kurul ${kurul} için henüz yok · ${a.ne}` : a.ne, url: aracYolu(a.id, kurul), ikon: it.icon, etiket: a.oner ? 'Önerilen' : undefined, soluk: bos };
          })}
        />
        <KlinikDizin
          harf="B"
          baslik="Check-up"
          baslangic={araclar.length + 1}
          ogeler={checkup.map((c) => ({ id: c.id, ad: c.ad, ne: c.alt, url: c.yol, ikon: ClipboardCheck, meta: c.surum }))}
        />
        {pdfler.length > 0 && <ul className="k15-izgara" role="list">
          {pdfler.map((p) => (
            <li key={p.id}>
              <div className="k15-kart v15-card">
                <span className="v15-tile is-b"><FileText aria-hidden /></span>
                <span className="k15-kart-t"><b>{p.ad}<span className="v15-tag">{p.sayfa} sayfa</span></b><span>{p.alt}</span></span>
                <span className="k15-pdf">
                  <a className="v15-btn is-soft" href={p.dosya} target="_blank" rel="noopener">Aç</a>
                  <a className="v15-ib" href={p.dosya} download aria-label="İndir"><Download aria-hidden /></a>
                </span>
              </div>
            </li>
          ))}
        </ul>}
        {/* H200: olası sorular gizliyken "Planlama" başlığı altında boş liste kalıyordu; başlık ve liste yalnız içerik varken çizilir */}
        {sekme === 'hepsi' && ((NAV_ITEMS.olasi_sorular && menudeGorunur('olasi_sorular')) || sinavAgirligiVar(kurul)) && (
          <section className="k15-plan" aria-labelledby="k15-plan-b">
            <h2 id="k15-plan-b" className="sr-only">Planlama</h2>
            {NAV_ITEMS.olasi_sorular && menudeGorunur('olasi_sorular') && (
              <KlinikDizin
                harf="C"
                baslik="Planlama"
                id="k15-plan-d"
                baslangic={araclar.length + checkup.length + 1}
                ogeler={[{ id: 'olasi', ad: NAV_ITEMS.olasi_sorular.label, ne: 'Sınavdan sonra öğrenci hatıralarından kurulan soruları çöz · ATP ile açılır', url: `${pathFor('olasi_sorular')}?kurul=${kurul}`, ikon: NAV_ITEMS.olasi_sorular.icon }]}
              />
            )}
            {sinavAgirligiVar(kurul) && (
              <a className="k15-agirlik v15-card" href={pathFor('sinav_plani')} onClick={git(pathFor('sinav_plani'))}>
                <span className="k15-kart-t"><b>Sınav ağırlığı</b><span>Kurul {kurul} teorik sınavında branş başına soru sayısı; kabarcık büyüdükçe soru artar. Ayrıntı için sınav planını aç.</span>{/* H201: kartın Sınav planı'na gittiği önceden söylenmiyordu */}</span>
                <SinavAgirligiV15 kurul={kurul} />
              </a>
            )}
          </section>
        )}
        {sekme === 'checkup' && !checkup.length && (
          // H161: boş check-up sekmesi çıkmazdı; var olan check-up'ların kuruluna ya da tüm hazırlık araçlarına götürür
          <div className="d15-bos v15-card k15-bos">
            <p>Kurul {kurul} için henüz check-up yok; içerik hazırlandıkça burada görünecek.</p>
            <div className="k15-bos-eylem">
              {(() => {
                const baska = CHECKUPLAR.find((c) => c.kurul !== kurul);
                return baska ? (
                  <a className="v15-btn is-soft" href={yol(baska.kurul, 'checkup')} onClick={git(yol(baska.kurul, 'checkup'))}>Kurul {baska.kurul} check-up'larını aç</a>
                ) : null;
              })()}
              <a className="v15-btn is-ghost" href={yol(kurul, 'hepsi')} onClick={git(yol(kurul, 'hepsi'))}>Tüm hazırlık araçları</a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
