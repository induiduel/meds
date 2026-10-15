/**
 * /canliders — herkese açık canlı ders sayfası.
 *  - Liste (/canliders): sesi olan dersler; Dinle (ders ekranı), hızlı Oynat, MP3 İndir, diğer sesler.
 *  - Ders (/canliders/<key>): solda PDF (varsa), sağda konuşma metni; metin sesle akar. Oynatıcı alt sabit
 *    çubuktadır (CanliDersDock, App düzeyinde) — ses öğesi canliDersStore'da tek ve kalıcıdır.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { ChevronDown, Download, Headphones, Pause, Play, Search, X } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import {
  cdDosyaAdi, cdListeGetir, cdOynat, cdSesUrl, cdToggle, fmtMb, fmtSure, useCd,
  type CdListeDers, type CdVaryant,
} from './canliDersStore';
import CanliDersDers from './CanliDersDers';
import '../../styles/canli-ders.css';
import { useCdTur } from './useCdTur';
import { CevrimdisiDugme, useCevrimdisiSuzgec } from './CanliDersCevrimdisi';

const fold = (s: string) =>
  s.toLocaleLowerCase('tr').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i').replace(/\s+/g, ' ').trim();

export default function CanliDersView({ dersKey }: { dersKey?: string }) {
  return dersKey ? <CanliDersDers key={dersKey} dersKey={dersKey} /> : <CanliDersListe />;
}

const dersAc = (key: string) => navigateTo(pathFor('canli_ders', key));

function CanliDersListe() {
  const [dersler, setDersler] = useState<CdListeDers[] | null>(null);
  const tanitim = useCdTur('liste', !!dersler?.length, () => !!document.querySelector('.cd-satir'));
  const [hata, setHata] = useState<string | null>(null);
  const [q, setQ] = useState('');

  const yukle = (yenile = false) => {
    setHata(null);
    cdListeGetir(yenile).then(setDersler, (e) => setHata(e?.message || 'Liste alınamadı.'));
  };
  useEffect(() => {
    document.title = 'Canlı ders · MeDSor';
    yukle();
  }, []);

  const liste = useMemo(() => {
    if (!dersler) return [];
    const f = fold(q);
    if (!f) return dersler;
    return dersler.filter((d) => fold(`${d.no} ${d.baslik}`).includes(f));
  }, [dersler, q]);
  const cevrimdisi = useCevrimdisiSuzgec(liste);

  return (
    <div className="cd-root cd-liste">
      <header className="cd-liste-bas">
        <div className="cd-liste-baslik">
          <span className="cd-ikon" aria-hidden><Headphones /></span>
          <div>
            <h1>Canlı ders</h1>
            <p>Dersleri dinle; metin ve slaytlar sesle birlikte akar. İstediğin dersi MP3 olarak indir.</p>
          </div>
          {tanitim.dugme}
        </div>
        <label className="cd-ara">
          <Search aria-hidden />
          <input
            type="search"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Ders ara (ad ya da numara)"
            aria-label="Ders ara"
          />
          {q && (
            <button type="button" className="cd-ara-sil" onClick={() => setQ('')} aria-label="Aramayı temizle">
              <X />
            </button>
          )}
        </label>
      </header>

      {hata ? (
        <div className="cd-bos">
          <p>{hata}</p>
          <button type="button" className="cd-btn" onClick={() => yukle(true)}>Yeniden dene</button>
        </div>
      ) : !dersler ? (
        <div className="cd-bos" role="status"><span className="cd-spin" aria-hidden /> Dersler yükleniyor…</div>
      ) : !liste.length ? (
        <div className="cd-bos"><p>{q ? `"${q}" için ders bulunamadı.` : 'Henüz sesi hazır ders yok.'}</p></div>
      ) : (
        <>
          {cevrimdisi.serit}
          <p className="cd-sayi">{liste.length === dersler.length ? `${dersler.length} ders` : `${liste.length} / ${dersler.length} ders`}</p>
          <ul className="cd-satirlar">
            {cevrimdisi.liste.map((d) => <DersSatiri key={d.key} d={d} />)}
          </ul>
        </>
      )}
      {tanitim.tur}
    </div>
  );
}

const sesAdi = (v: CdVaryant) => v.etiket || v.ses || v.id;

function OynatDugme({ d, v, kucuk }: { d: CdListeDers; v: CdVaryant; kucuk?: boolean }) {
  const buMu = useCd((s) => s.key === d.key && s.vid === v.id);
  const caliyor = useCd((s) => s.key === d.key && s.vid === v.id && s.playing);
  const etiket = caliyor ? 'Duraklat' : 'Oynat';
  return (
    <button
      type="button"
      className={`cd-btn${kucuk ? ' is-ince' : ''}${buMu ? ' is-on' : ''}`}
      onClick={() => (buMu ? cdToggle() : cdOynat(d, v.id))}
      aria-label={`${etiket}: ${d.baslik}${kucuk ? ` (${sesAdi(v)})` : ''}`}
    >
      {caliyor ? <Pause aria-hidden /> : <Play aria-hidden />}
      <span>{etiket}</span>
    </button>
  );
}

function IndirDugme({ d, v, kucuk }: { d: CdListeDers; v: CdVaryant; kucuk?: boolean }) {
  return (
    <a
      className={`cd-btn${kucuk ? ' is-ince' : ''}`}
      href={cdSesUrl(d.key, v.id, true)}
      download={cdDosyaAdi(d.no, d.baslik, v.ses || v.etiket)}
      aria-label={`MP3 indir: ${d.baslik} (${sesAdi(v)}${v.bayt ? `, ${fmtMb(v.bayt)}` : ''})`}
    >
      <Download aria-hidden />
      <span>{kucuk ? 'İndir' : 'MP3'}</span>
    </a>
  );
}

const DersSatiri = React.memo(function DersSatiri({ d }: { d: CdListeDers }) {
  const [acik, setAcik] = useState(false);
  const v = d.varsayilan || d.varyantlar[0];
  const diger = d.varyantlar.filter((x) => x.id !== v?.id);
  const caliyor = useCd((s) => s.key === d.key && s.playing);
  if (!v) return null;
  return (
    <li className={`cd-satir${caliyor ? ' is-caliyor' : ''}`}>
      <div className="cd-satir-ana">
        <span className="cd-no" aria-hidden>{d.no}</span>
        <a
          className="cd-satir-ad"
          href={pathFor('canli_ders', d.key)}
          onClick={(e) => {
            if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
            e.preventDefault();
            dersAc(d.key);
          }}
        >
          <b>{d.baslik}</b>
          <small>
            <span>{fmtSure(v.sureSn)}</span>
            <span className="cd-chip" title={v.saglayici || undefined}>{sesAdi(v)}</span>
            {d.pdf && <span className="cd-chip is-pdf">PDF</span>}
            {v.bayt > 0 && <span>{fmtMb(v.bayt)}</span>}
          </small>
        </a>
        <div className="cd-satir-eylem">
          <button type="button" className="cd-btn is-ana" onClick={() => dersAc(d.key)} aria-label={`Dinle: ${d.baslik} (metin ve slaytlarla)`}>
            <Headphones aria-hidden />
            <span>Dinle</span>
          </button>
          <OynatDugme d={d} v={v} />
          <IndirDugme d={d} v={v} />
          <CevrimdisiDugme dersKey={d.key} baslik={d.baslik} varyantlar={d.varyantlar} />
          {diger.length > 0 ? (
            <button
              type="button"
              className={`cd-btn is-ikon${acik ? ' is-acik' : ''}`}
              aria-expanded={acik}
              aria-label={`Diğer sesler (${diger.length})`}
              title="Diğer sesler"
              onClick={() => setAcik((x) => !x)}
            >
              <ChevronDown aria-hidden />
            </button>
          ) : (
            <span className="cd-btn-yer" aria-hidden />
          )}
        </div>
      </div>
      {acik && diger.length > 0 && (
        <ul className="cd-varyantlar">
          {[v, ...diger].map((x) => (
            <li key={x.id}>
              <span className="cd-var-ad">
                <b>{sesAdi(x)}</b>
                <small>{[fmtSure(x.sureSn), fmtMb(x.bayt)].filter(Boolean).join(' · ')}</small>
              </span>
              <OynatDugme d={d} v={x} kucuk />
              <IndirDugme d={d} v={x} kucuk />
            </li>
          ))}
        </ul>
      )}
    </li>
  );
});
