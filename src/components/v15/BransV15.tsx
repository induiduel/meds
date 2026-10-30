import React, { useMemo } from 'react';
import { Check, Headphones } from 'lucide-react';
import { linkClick, navigateTo } from '../../router';
import { icKonum } from '../../siteHaritasi';
import { cdBransKisa, cdBransSlug } from '../canliDers/canliDersKategori';
import { useV15Baslik } from './baslik';
import { dersAdi, dersBransi, dersKurulu, dersSirala, dersSurumleri, dersYolu, hocaYaz, merkezYolu, sureDk, useDersListesi, useIlerleme } from './dersVeri';
import SurumSecV15 from './SurumSecV15';
import { cdDersSesSurumu } from '../canliDers/canliDersStore';
import { Halka } from './Halka';
import '../../styles/v15/dersler.css';

/**
 * v15 · Branş ders listesi (tasarım sistemi v15 › B02). Adres: /dersler/canliders/kurulN/<branş> (iç ?kurul=&brans=).
 * Üstte Dersler · Önem listesi · Çıkmışlar seçicisi (her biri kendi sayfası), altta sıralı dersler: durum karosu,
 * hoca ve süre, ilerleme halkası. Satır ders ayrıntısını açar. Liste uzunsa kart kendi içinde kayar (sayfa sabit).
 */
export default function BransV15() {
  const sp = new URLSearchParams(icKonum().search);
  const slug = sp.get('brans') || '';
  const kurulQ = Number(sp.get('kurul')) || null;
  const liste0 = useDersListesi();
  const { dersler, hata } = liste0;
  const ilerleme = useIlerleme();

  const liste = useMemo(() => {
    if (!dersler) return null;
    return dersSirala(dersler.filter((d) => (!kurulQ || dersKurulu(d) === kurulQ) && cdBransSlug(dersBransi(d)) === slug));
  }, [dersler, slug, kurulQ]);
  const ad = liste?.[0] ? cdBransKisa(dersBransi(liste[0])) : slug.replace(/-/g, ' ');
  const kurul = kurulQ ?? (liste?.[0] ? dersKurulu(liste[0]) : 1);
  const bitenN = liste ? liste.filter((d) => ilerleme(d).bitti).length : 0;

  useV15Baslik({
    baslik: ad.charAt(0).toLocaleUpperCase('tr-TR') + ad.slice(1),
    alt: liste ? `Kurul ${kurul} · ${liste.length} ders${bitenN ? ` · ${bitenN} bitti` : ''}` : `Kurul ${kurul}`,
    geri: merkezYolu(kurul),
  });

  const sekmeler: [string, string][] = [
    ['Dersler', ''],
    ['Önem listesi', `/kamplar/kurul${kurul}/en-onemliler/${slug}`],
    ['Çıkmışlar', `/sorular/soru-cozucu/kurul${kurul}/${slug}`],
  ];

  return (
    <div className="b15">
      <h1 className="sr-only">{ad} dersleri</h1>
      <nav className="v15-seg" aria-label={`${ad} sayfaları`}>
        {sekmeler.map(([t, url]) =>
          url ? (
            <a key={t} href={url} onClick={linkClick(() => navigateTo(url))}>{t}</a>
          ) : (
            <span key={t} aria-current="page">{t}</span>
          ),
        )}
      </nav>

      {liste === null ? (
        <span className="v15-skel b15-skel" aria-hidden />
      ) : liste.length ? (
        <ul className="b15-list v15-card" role="list">
          {liste.map((d) => {
            const i = ilerleme(d);
            const hoca = hocaYaz(d.hoca);
            return (
              <li key={d.key}>
                <a className="b15-row" href={dersYolu(d.key)} onClick={linkClick(() => navigateTo(dersYolu(d.key)))}>
                  <span className={`v15-tile ${i.bitti ? 'is-ok' : i.t != null ? '' : 'is-n'}`}>{i.bitti ? <Check aria-hidden /> : <Headphones aria-hidden />}</span>
                  <span className="b15-row-t">
                    <b>{dersAdi(d)}</b>
                    <span>{[hoca, sureDk(i.sure)].filter(Boolean).join(' · ')}</span>
                  </span>
                  <Halka pct={i.pct} etiket={i.bitti ? 'Bitti' : `%${i.pct} dinlendi`} />
                </a>
                <SurumListe dk={d.key} d={liste0} />
              </li>
            );
          })}
        </ul>
      ) : (
        <p className="b15-bos v15-card">{hata ? `Ders listesi alınamadı: ${hata}` : `Kurul ${kurul} için bu branşta sesli ders yok.`}</p>
      )}
    </div>
  );
}

/** Satırdaki sürüm bağlantıları: seçili (ya da güncel) sürüm vurgulu */
function SurumListe({ dk, d }: { dk: string; d: ReturnType<typeof useDersListesi> }) {
  const ss = dersSurumleri(dk, d);
  if (!ss.length) return null;
  const sec = ss.find((s) => s.vid && cdDersSesSurumu(s.key) === s.vid) || ss.find((s) => s.yeni) || null;
  return <SurumSecV15 surumler={ss} aktif={sec} />;
}
