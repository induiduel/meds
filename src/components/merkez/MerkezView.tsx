/**
 * Merkez sayfaları (2026-10-21): /dersler · /sorular · /kamplar[/kurulN] · /kaynaklar
 * Öğrenci önce ne yapmak istediğini seçer (dört kategori sekmesi), sonra araçlar "ne zaman kullanılır" cümlesiyle
 * listelenir; kategorinin önerilen ilk adımı büyük kartta durur. Ders çalış · Soru çöz · Sınava hazırlan merkezleri
 * Kurul 1–6 seçicisini taşır (/dersler/kurulN, /sorular/kurulN, /kamplar/kurulN; kurula bağlı araçlar o kurulda açılır).
 * Kamplar merkezi ayrıca Son Prova · Kamplar · Check Up · En önemliler sekmelerini taşır (?sekme= → /kamplar/kurulN/<sekme>).
 * Model: merkezModel.ts · adresler: siteHaritasi.ts · stil: styles/merkez.css (.mz-*)
 */
import React, { useEffect, useState } from 'react';
import { ArrowRight, ChevronLeft, BookOpenText, ClipboardCheck, Download, FileText, Flag, GraduationCap, MessageCircleQuestion } from 'lucide-react';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import { KATEGORILER, icKonum, type KategoriId } from '../../siteHaritasi';
import { NAV_ITEMS } from '../shell/navModel';
import { KurulSecici, kurulIcerikVar, varsayilanKurul } from '../kurul/KurulSecici';
import { menudeGorunur } from '../../services/siteAyar';
import { CHECKUPLAR, MERKEZ_ARACLARI, MERKEZ_ROUTE, PDF_NOTLAR, kategoriOf } from './merkezModel';
import '../../styles/merkez.css';
import { useAppearance } from '../../utils/appearance';

const DerslerMerkezV15 = React.lazy(() => import('../v15/DerslerMerkezV15'));
const SorularMerkezV15 = React.lazy(() => import('../v15/SorularMerkezV15'));
const KamplarMerkezV15 = React.lazy(() => import('../v15/KamplarMerkezV15'));
const KaynaklarMerkezV15 = React.lazy(() => import('../v15/KaynaklarMerkezV15'));

export const KATEGORI_IKON: Record<KategoriId, React.ElementType> = {
  dersler: GraduationCap, sorular: MessageCircleQuestion, kamplar: Flag, kaynaklar: BookOpenText,
};

const Bag: React.FC<{ url: string; className?: string; children: React.ReactNode; aria?: Record<string, string | boolean> }> = ({ url, className, children, aria }) => (
  <a href={url} className={className} onClick={linkClick(() => navigateTo(url))} {...aria}>{children}</a>
);

/** Kurula bağlı araçlar merkezde seçili kurulun altında açılır (kurulsuz araçlar kendi adresinde) */
export function aracYolu(id: AppRoute, kurul: number | null): string {
  const k = kurul ? `/kurul${kurul}` : '';
  if (id === 'son_prova') return `/kamplar${k}/son-prova`;
  if (id === 'kamp') return `/kamplar${k}/kamp`;
  if (id === 'cikmis_cozucu') return `/kamplar${k}/cikmis-cozucu`;
  if (id === 'en_onemliler') return `/kamplar${k}/en-onemliler`;
  if (id === 'spots') return `/kamplar${k}/spotlar`;
  if (id === 'canli_ders') return `/dersler/canliders${k}`;
  if (id === 'soru_cozucu') return `/sorular/soru-cozucu${k}`;
  if (kurul && (id === 'learn' || id === 'past_exams' || id === 'olasi_sorular')) return `${pathFor(id)}?kurul=${kurul}`;
  return pathFor(id);
}

/** "Ne yapmak istiyorsun?" — dört kategori sekmesi (merkez sayfalarının başı; Bugün'de kart olarak) */
export const NeYapmak: React.FC<{ secili?: KategoriId | null; kart?: boolean }> = ({ secili = null, kart = false }) => (
  <nav className={`mz-ne${kart ? ' is-kart' : ''}`} aria-label="Ne yapmak istiyorsun?">
    {kart && <h2 className="mz-ne-h">Ne yapmak istiyorsun?</h2>}
    <div className="mz-ne-l">
      {KATEGORILER.map((k) => {
        const Ic = KATEGORI_IKON[k.id];
        return (
          <Bag key={k.id} url={k.yol} className={`mz-ne-k is-${k.id}${secili === k.id ? ' is-on' : ''}`} aria={secili === k.id ? { 'aria-current': 'page' } : undefined}>
            <span className="mz-ne-ic" aria-hidden><Ic /></span>
            <span className="mz-ne-t">
              <b>{k.ad}</b>
              <small>{k.soru}</small>
            </span>
          </Bag>
        );
      })}
    </div>
  </nav>
);

/** Bölüm şeridi: araç sayfalarının üstünde kategori adı + kardeş araçlar (sekme gibi) */
/** Tam ekran / tek öge açıkken şerit gizlenir (ders oynatıcısı, sesli ders, çözücü, TBG kampının kendi gezinmesi) */
function seritGizli(route: AppRoute): boolean {
  const { pathname: p, search } = icKonum();
  const sp = new URLSearchParams(search);
  if (route === 'genetik_checkup') return true;
  if (route === 'learn') return p.startsWith('/ogren/');
  if (route === 'canli_ders') return p.startsWith('/canliders/');
  if (route === 'son_prova') return p.replace(/\/+$/, '') !== '/son-prova';
  if (route === 'kamp') return /^\/kamp\/\d/.test(p);
  if (route === 'soru_cozucu' || route === 'en_onemliler' || route === 'cikmis_cozucu') return !!(sp.get('coz') || sp.get('asistan'));
  return false;
}

export const BolumSeridi: React.FC<{ route: AppRoute }> = ({ route }) => {
  const [, setT] = useState(0);
  useEffect(() => {
    const f = () => setT((t) => t + 1);
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  const kat = kategoriOf(route);
  if (!kat || seritGizli(route)) return null;
  const tanim = KATEGORILER.find((k) => k.id === kat)!;
  const checkup = route === 'genetik_checkup' || route === 'patoloji_checkup';
  const it = NAV_ITEMS[route];
  return (
    <nav className={`mz-iz is-${kat}`} aria-label="Konum">
      <Bag url={pathFor(MERKEZ_ROUTE[kat])} className="mz-iz-kat"><ChevronLeft aria-hidden /><span>{tanim.ad}</span></Bag>
      {checkup && <><span className="mz-iz-ayir" aria-hidden>/</span><Bag url="/kamplar/kurul1/checkup" className="mz-iz-kat"><span>Check Up</span></Bag></>}
      <span className="mz-iz-ayir" aria-hidden>/</span>
      <span className="mz-iz-sayfa" aria-current="page">{it?.label}</span>
    </nav>
  );
};

export type KampSekme = 'hepsi' | 'son-prova' | 'kamp' | 'checkup' | 'en-onemliler';
export const KAMP_SEKMELER: [KampSekme, string][] = [['hepsi', 'Hepsi'], ['son-prova', 'Son Prova'], ['kamp', 'Kamplar'], ['checkup', 'Check Up'], ['en-onemliler', 'En önemliler']];
export const SEKME_ROUTE: Partial<Record<KampSekme, AppRoute[]>> = { 'son-prova': ['son_prova', 'cikmis_cozucu'], kamp: ['kamp'], 'en-onemliler': ['en_onemliler', 'spots'] };
/** H139: tüm sayfaları gizli (menudeGorunur) sekme gösterilmez — tıklayınca öğrenci açıklamasız Bugün'e atılıyordu */
export const gorunenSekmeler = () => KAMP_SEKMELER.filter(([id]) => !SEKME_ROUTE[id] || SEKME_ROUTE[id]!.some((r) => menudeGorunur(r)));

export const kampOku = () => {
  const sp = new URLSearchParams(icKonum().search);
  const n = Number(sp.get('kurul'));
  const s = sp.get('sekme') as KampSekme | null;
  return { kurul: n >= 1 && n <= 6 ? n : null, sekme: s && KAMP_SEKMELER.some(([id]) => id === s) ? s : 'hepsi' as KampSekme };
};

/** v15'te Ders çalış merkezi kendi düzenini kullanır (components/v15/DerslerMerkezV15); diğerleri aşama aşama taşınır */
export default function MerkezView({ kategori }: { kategori: KategoriId }) {
  const { v15 } = useAppearance();
  if (v15 && kategori === 'dersler') return <React.Suspense fallback={null}><DerslerMerkezV15 /></React.Suspense>;
  if (v15 && kategori === 'sorular') return <React.Suspense fallback={null}><SorularMerkezV15 /></React.Suspense>;
  if (v15 && kategori === 'kamplar') return <React.Suspense fallback={null}><KamplarMerkezV15 /></React.Suspense>;
  if (v15 && kategori === 'kaynaklar') return <React.Suspense fallback={null}><KaynaklarMerkezV15 /></React.Suspense>;
  return <MerkezViewEski kategori={kategori} />;
}

function MerkezViewEski({ kategori }: { kategori: KategoriId }) {
  const tanim = KATEGORILER.find((k) => k.id === kategori)!;
  const [kamp, setKamp] = useState(kampOku);
  useEffect(() => {
    const f = () => setKamp(kampOku());
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  useEffect(() => { document.title = `${tanim.ad} · MeDSor`; }, [tanim.ad]);

  const kampMi = kategori === 'kamplar';
  // Ders çalış · Soru çöz · Sınava hazırlan kurul seçer (adres → son seçim → takvim); Başvuru kurulsuz
  const kurul = kategori === 'kaynaklar' ? null : (kamp.kurul ?? varsayilanKurul());
  const sekme = kampMi ? kamp.sekme : 'hepsi';
  const araclar = MERKEZ_ARACLARI[kategori].filter((a) => sekme === 'hepsi' || (SEKME_ROUTE[sekme] || []).includes(a.id));
  const oneri = sekme === 'hepsi' ? araclar.find((a) => a.oner) : undefined;
  const digerleri = araclar.filter((a) => a !== oneri);
  const checkuplar = CHECKUPLAR.filter((c) => c.kurul === kurul);
  const pdfler = PDF_NOTLAR.filter((p) => p.kurul === kurul);
  const Ic = KATEGORI_IKON[kategori];
  const kurulYol = (k: number, s: KampSekme = sekme) => (kampMi ? `/kamplar/kurul${k}${s === 'hepsi' ? '' : `/${s}`}` : `${tanim.yol}/kurul${k}`);
  /** Kartın kurul rozeti: araç bu kurulda henüz içerik taşımıyorsa */
  const bosRozet = (id: AppRoute) => (kurul && kurulIcerikVar(id, kurul) === false ? <em className="mz-yok">Kurul {kurul}: henüz yok</em> : null);

  return (
    <div className={`mz is-${kategori}`}>
      <NeYapmak secili={kategori} />

      <header className="mz-bas">
        <span className="mz-bas-ic" aria-hidden><Ic /></span>
        <div className="mz-bas-t">
          <h2>{tanim.ad}</h2>
          <p>{tanim.alt}</p>
        </div>
      </header>

      {kurul && (
        <div className="mz-kamp-ust">
          <KurulSecici secili={kurul} yol={(k) => kurulYol(k)} />
          {kampMi && <div className="mz-sekmeler" role="tablist" aria-label="Sınava hazırlık bölümleri">
            {gorunenSekmeler().map(([id, ad]) => (
              <Bag key={id} url={kurulYol(kurul, id)} className={`mz-sekme${id === sekme ? ' is-on' : ''}`} aria={{ role: 'tab', 'aria-selected': id === sekme }}>{ad}</Bag>
            ))}
          </div>}
        </div>
      )}

      {oneri && (() => {
        const it = NAV_ITEMS[oneri.id];
        const AIc = it.icon;
        return (
          <Bag url={aracYolu(oneri.id, kurul)} className="mz-oneri">
            <span className="mz-oneri-ic" style={{ '--mz-t': it.tint } as React.CSSProperties} aria-hidden><AIc /></span>
            <span className="mz-oneri-t">
              <span className="mz-ust">Buradan başla</span>
              <b>{it.label}{bosRozet(oneri.id)}</b>
              <span>{oneri.ne}</span>
            </span>
            <span className="mz-oneri-git">Aç <ArrowRight aria-hidden /></span>
          </Bag>
        );
      })()}

      {kampMi && (sekme === 'hepsi' || sekme === 'checkup') && (
        <section className="mz-bolum" aria-labelledby="mz-checkup-h">
          <h2 id="mz-checkup-h" className="mz-h2"><ClipboardCheck aria-hidden /> Check Up</h2>
          {checkuplar.length ? (
            <div className="mz-izgara">
              {checkuplar.map((c) => (
                <Bag key={c.id} url={c.yol} className="mz-kart is-checkup">
                  <span className="mz-kart-t">
                    <b>{c.ad}{c.surum && <em className="mz-surum">{c.surum}</em>}</b>
                    <span>{c.alt}</span>
                  </span>
                  <ArrowRight className="mz-ok" aria-hidden />
                </Bag>
              ))}
            </div>
          ) : (
            <p className="mz-bos">Kurul {kurul} için henüz check-up yok; içerik hazırlandıkça burada görünecek.</p>
          )}
        </section>
      )}

      {kampMi && (sekme === 'hepsi' || sekme === 'en-onemliler') && pdfler.length > 0 && (
        <section className="mz-bolum" aria-labelledby="mz-pdf-h">
          <h2 id="mz-pdf-h" className="mz-h2"><FileText aria-hidden /> PDF notlar</h2>
          <div className="mz-izgara">
            {pdfler.map((p) => (
              <div key={p.id} className="mz-kart is-pdf">
                <span className="mz-kart-ic" aria-hidden><FileText /></span>
                <span className="mz-kart-t">
                  <b>{p.ad}<em className="mz-surum">{p.sayfa} sayfa</em></b>
                  <span>{p.alt}</span>
                  <span className="mz-pdf-eylem">
                    <a href={p.dosya} target="_blank" rel="noopener" className="mz-pdf-btn is-ana">Aç</a>
                    <a href={p.dosya} download className="mz-pdf-btn"><Download aria-hidden /> İndir</a>
                  </span>
                </span>
              </div>
            ))}
          </div>
        </section>
      )}

      {digerleri.length > 0 && (
        <section className="mz-bolum" aria-label="Araçlar">
          {kampMi && sekme === 'hepsi' && <h2 className="mz-h2">Diğer hazırlık araçları</h2>}
          <div className="mz-izgara">
            {digerleri.map((a) => {
              const it = NAV_ITEMS[a.id];
              const AIc = it.icon;
              return (
                <Bag key={a.id} url={aracYolu(a.id, kurul)} className="mz-kart">
                  <span className="mz-kart-ic" style={{ '--mz-t': it.tint } as React.CSSProperties} aria-hidden><AIc /></span>
                  <span className="mz-kart-t">
                    <b>{it.label}{bosRozet(a.id)}</b>
                    <span>{a.ne}</span>
                  </span>
                  <ArrowRight className="mz-ok" aria-hidden />
                </Bag>
              );
            })}
          </div>
        </section>
      )}
    </div>
  );
}
