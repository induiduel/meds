import React, { useEffect, useState } from 'react';
import { ChevronDown, ChevronRight, ClipboardCheck, Download, FileText } from 'lucide-react';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import SinavAgirligiV15, { sinavAgirligiVar } from './SinavAgirligiV15';
import { NAV_ITEMS } from '../shell/navModel';
import { KURUL_NOLAR, kurulIcerikVar, kurulKaydet, varsayilanKurul } from '../kurul/KurulSecici';
import { CHECKUPLAR, MERKEZ_ARACLARI, PDF_NOTLAR } from '../merkez/merkezModel';
import { KAMP_SEKMELER, SEKME_ROUTE, aracYolu, kampOku, type KampSekme } from '../merkez/MerkezView';
import { useV15Baslik } from './baslik';
import KurulSecV15 from './KurulSecV15';
import '../../styles/v15/dersler.css';
import '../../styles/v15/ek15.css';

/**
 * v15 · Sınava hazırlan merkezi (tasarım sistemi v15 › D01). Sekmeler adrestir (/kamplar/kurulN/<sekme>, site haritası
 * kuralı): Hepsi · Son Prova · Kamplar · Check Up · En önemliler. Kartlar: kurula bağlı araçlar (içerik yoksa
 * "henüz yok"), Check Up'lar ve PDF notlar. Kurul seçimi ve adres mantığı eski merkezle aynı (MerkezView yardımcıları).
 */
const TON: Partial<Record<AppRoute, string>> = { son_prova: 'is-b', kamp: 'is-ai', cikmis_cozucu: 'is-ok', en_onemliler: 'is-w', spots: 'is-w', sinav_plani: '' };
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
          {KAMP_SEKMELER.map(([id, ad]) =>
            id === sekme ? <span key={id} aria-current="page">{ad}</span> : <a key={id} href={yol(kurul, id)} onClick={git(yol(kurul, id))}>{ad}</a>,
          )}
        </nav>
        <KurulSecV15 className="s15-kurul" kurul={kurul} onSec={(k) => navigateTo(yol(k, sekme))} />
      </div>

      <div className="k15-alan">
        <ul className="k15-izgara" role="list">
          {araclar.map((a) => {
            const it = NAV_ITEMS[a.id];
            const bos = kurulIcerikVar(a.id, kurul) === false;
            const url = aracYolu(a.id, kurul);
            return (
              <li key={a.id}>
                <a className={`k15-kart v15-card${bos ? ' is-bos' : ''}`} href={url} onClick={git(url)}>
                  <span className={`v15-tile ${TON[a.id] ?? 'is-ai'}`}><it.icon aria-hidden /></span>
                  <span className="k15-kart-t">
                    <b>{it.label}{a.oner && <span className="v15-tag is-a">Önerilen</span>}{bos && <span className="v15-tag">Kurul {kurul}: henüz yok</span>}</b>
                    <span>{a.ne}</span>
                  </span>
                  <ChevronRight className="v15-chev" aria-hidden />
                </a>
              </li>
            );
          })}
          {checkup.map((c) => (
            <li key={c.id}>
              <a className="k15-kart v15-card" href={c.yol} onClick={git(c.yol)}>
                <span className="v15-tile is-c"><ClipboardCheck aria-hidden /></span>
                <span className="k15-kart-t"><b>{c.ad}{c.surum && <span className="v15-tag">{c.surum}</span>}</b><span>{c.alt}</span></span>
                <ChevronRight className="v15-chev" aria-hidden />
              </a>
            </li>
          ))}
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
        </ul>
        {sekme === 'hepsi' && (
          <section className="k15-plan" aria-labelledby="k15-plan-b">
            <h2 id="k15-plan-b" className="v15-cap">Planlama</h2>
            <ul className="k15-izgara" role="list">
              {NAV_ITEMS.olasi_sorular && (() => {
                const url = `${pathFor('olasi_sorular')}?kurul=${kurul}`;
                const it = NAV_ITEMS.olasi_sorular;
                return (
                  <li>
                    <a className="k15-kart v15-card" href={url} onClick={git(url)}>
                      <span className="v15-tile is-b"><it.icon aria-hidden /></span>
                      <span className="k15-kart-t"><b>{it.label}</b><span>Sınavdan sonra öğrenci hatıralarından kurulan soruları çöz</span></span>
                      <ChevronRight className="v15-chev" aria-hidden />
                    </a>
                  </li>
                );
              })()}
            </ul>
            {sinavAgirligiVar(kurul) && (
              <a className="k15-agirlik v15-card" href={pathFor('sinav_plani')} onClick={git(pathFor('sinav_plani'))}>
                <span className="k15-kart-t"><b>Sınav ağırlığı</b><span>Kurul {kurul} teorik sınavında branş başına soru sayısı; kabarcık büyüdükçe soru artar</span></span>
                <SinavAgirligiV15 kurul={kurul} />
              </a>
            )}
          </section>
        )}
        {sekme === 'checkup' && !checkup.length && (
          <p className="d15-bos v15-card">Kurul {kurul} için henüz check-up yok; içerik hazırlandıkça burada görünecek.</p>
        )}
      </div>
    </div>
  );
}
