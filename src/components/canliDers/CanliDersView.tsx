/**
 * /canliders — herkese açık canlı ders sayfası.
 *  - Liste (/canliders): sesi olan dersler; Dinle (ders ekranı), hızlı Oynat, MP3 İndir, diğer sesler.
 *  - Ders (/canliders/<key>): solda PDF (varsa), sağda konuşma metni; metin sesle akar. Oynatıcı alt sabit
 *    çubuktadır (CanliDersDock, App düzeyinde) — ses öğesi canliDersStore'da tek ve kalıcıdır.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { ChevronDown, Download, Headphones, History, ListMusic, MoreHorizontal, Pause, Play, Search, X } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import {
  cdDosyaAdi, cdKonumListesi, cdListeGetir, cdOynat, cdSesKisa, cdSesUrl, cdToggle, fmtMb, fmtSure, useCd,
  type CdListeDers, type CdVaryant,
} from './canliDersStore';
import CanliDersDers from './CanliDersDers';
import { cdListeOzetleri, useCdListe } from './canliDersListe';
import { ListeEkleDugme, Listem } from './CanliDersListem';
import { useCdTur } from './useCdTur';
import { CevrimdisiDugme, useCevrimdisiSuzgec } from './CanliDersCevrimdisi';
import { cdBransKisa, cdDersEtiketi, cdKategoriGrupla, type CdKategori } from './canliDersKategori';
import '../../styles/canli-ders.css';

const fold = (s: string) =>
  s.toLocaleLowerCase('tr').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i').replace(/\s+/g, ' ').trim();

export default function CanliDersView({ dersKey }: { dersKey?: string }) {
  return dersKey ? <CanliDersDers key={dersKey} dersKey={dersKey} /> : <CanliDersListe />;
}

const dersAc = (key: string) => navigateTo(pathFor('canli_ders', key));

type Konum = { vid: string; t: number; at: number };
/** Kaldığın yer: sayfa açılınca bir kez okunur (ders ekranından dönünce liste yeniden kurulur). */
const konumHaritasi = () => new Map(cdKonumListesi().map((k) => [k.key, k as Konum]));

function CanliDersListe() {
  const [dersler, setDersler] = useState<CdListeDers[] | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [q, setQ] = useState('');
  const [gorunum, setGorunum] = useState<'tum' | 'liste'>(() => (location.hash === '#listem' ? 'liste' : 'tum'));
  const listeN = useCdListe((s) => s.keys.length);
  // Oynatıcıdaki "Listem" göstergesi /canliders#listem açar (sayfa zaten açıksa da sekmeye geçilsin)
  useEffect(() => {
    const f = () => { if (location.hash === '#listem') setGorunum('liste'); };
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  /** 'tum' | 'yarim' | kategori kimliği */
  const [suzgec, setSuzgec] = useState<string>('tum');
  const [kapali, setKapali] = useState<Set<string>>(() => new Set());
  const [konum] = useState(konumHaritasi);
  const tanitim = useCdTur('liste', !!dersler?.length, () => !!document.querySelector('.cd-satir'));

  const yukle = (yenile = false) => {
    setHata(null);
    cdListeGetir(yenile).then((ds) => { cdListeOzetleri(ds); setDersler(ds); }, (e) => setHata(e?.message || 'Liste alınamadı.'));
  };
  useEffect(() => {
    document.title = 'Canlı ders · MeDSor';
    yukle();
  }, []);

  const liste = useMemo(() => {
    if (!dersler) return [];
    const f = fold(q);
    let l = suzgec === 'yarim' ? dersler.filter((d) => konum.has(d.key)) : dersler;
    if (f) l = l.filter((d) => fold(`${d.brans ? `${d.brans} ${cdBransKisa(d.brans)} ` : ''}${d.no} ${d.baslik}`).includes(f));
    return l;
  }, [dersler, q, suzgec, konum]);
  const cevrimdisi = useCevrimdisiSuzgec(liste);
  // Tüm derslerin kategorileri (çip sayıları aramadan bağımsız); görünen gruplar süzülmüş listeden
  const tumGruplar = useMemo(() => cdKategoriGrupla(dersler || []), [dersler]);
  const gruplar = useMemo(() => {
    const g = cdKategoriGrupla(cevrimdisi.liste);
    return suzgec === 'tum' || suzgec === 'yarim' ? g : g.filter((x) => x.kat.id === suzgec);
  }, [cevrimdisi.liste, suzgec]);
  const gorunenN = gruplar.reduce((n, g) => n + g.dersler.length, 0);
  const katDegistir = (id: string) => setKapali((s) => { const n = new Set(s); n.has(id) ? n.delete(id) : n.add(id); return n; });
  const yarimSayi = useMemo(() => (dersler ? dersler.filter((d) => konum.has(d.key)).length : 0), [dersler, konum]);
  // En son dinlenen (listede olan) ders: "Kaldığın yerden devam"
  const son = useMemo(() => {
    if (!dersler) return null;
    const byKey = new Map(dersler.map((d) => [d.key, d]));
    for (const k of cdKonumListesi()) {
      const d = byKey.get(k.key);
      if (d) return { d, k };
    }
    return null;
  }, [dersler]);

  return (
    <div className="cd-root cd-liste">
      <header className="cd-liste-bas">
        <div className="cd-liste-baslik">
          <span className="cd-ikon" aria-hidden><Headphones /></span>
          <div>
            <h1>Canlı ders</h1>
            <p>Dersleri sesli dinle; okunan cümle metinde, anlatılan sayfa slaytta kendiliğinden ilerler.</p>
          </div>
          {tanitim.dugme}
        </div>
        <div className="cd-sekmeler cd-gorunum" role="tablist" aria-label="Görünüm">
          <button type="button" role="tab" aria-selected={gorunum === 'tum'} className={gorunum === 'tum' ? 'is-on' : ''} onClick={() => setGorunum('tum')}>
            <Headphones aria-hidden /> Tüm dersler
          </button>
          <button type="button" role="tab" aria-selected={gorunum === 'liste'} className={gorunum === 'liste' ? 'is-on' : ''} onClick={() => setGorunum('liste')}>
            <ListMusic aria-hidden /> Listem{listeN > 0 && <span className="cd-sekme-sayi">{listeN}</span>}
          </button>
        </div>
        {gorunum === 'tum' && <label className="cd-ara">
          <Search aria-hidden />
          <input
            type="search"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Ders ara (ad, branş ya da numara)"
            aria-label="Ders ara"
          />
          {q && (
            <button type="button" className="cd-ara-sil" onClick={() => setQ('')} aria-label="Aramayı temizle">
              <X />
            </button>
          )}
        </label>}
      </header>

      {hata ? (
        <div className="cd-bos">
          <p>{hata}</p>
          <button type="button" className="cd-btn" onClick={() => yukle(true)}>Yeniden dene</button>
        </div>
      ) : !dersler ? (
        <div className="cd-bos" role="status"><span className="cd-spin" aria-hidden /> Dersler yükleniyor…</div>
      ) : gorunum === 'liste' ? (
        <Listem dersler={dersler} onTumu={() => setGorunum('tum')} />
      ) : !liste.length ? (
        <div className="cd-bos"><p>{q ? `"${q}" için ders bulunamadı.` : 'Henüz sesi hazır ders yok.'}</p></div>
      ) : (
        <>
          {cevrimdisi.serit}
          {son && !q && suzgec === 'tum' && <DevamKarti d={son.d} k={son.k} />}
          <div className="cd-kat-cipler" role="group" aria-label="Kategoriye göre süz">
            <button type="button" aria-pressed={suzgec === 'tum'} className={suzgec === 'tum' ? 'is-on' : ''} onClick={() => setSuzgec('tum')}>
              Tümü <span>{dersler.length}</span>
            </button>
            {yarimSayi > 0 && (
              <button type="button" aria-pressed={suzgec === 'yarim'} className={`is-yarim${suzgec === 'yarim' ? ' is-on' : ''}`} onClick={() => setSuzgec('yarim')}>
                <History aria-hidden /> Yarım kalanlar <span>{yarimSayi}</span>
              </button>
            )}
            {tumGruplar.map(({ kat, dersler: ds }) => (
              <button key={kat.id} type="button" aria-pressed={suzgec === kat.id} className={suzgec === kat.id ? 'is-on' : ''}
                onClick={() => setSuzgec(suzgec === kat.id ? 'tum' : kat.id)}>
                {kat.kisa} <span>{ds.length}</span>
              </button>
            ))}
          </div>
          {!gorunenN ? (
            <div className="cd-bos"><p>{q ? `"${q}" için bu kategoride ders bulunamadı.` : 'Bu kategoride ders yok.'}</p></div>
          ) : gruplar.map(({ kat, dersler: ds }) => (
            <KategoriBolumu key={kat.id} kat={kat} n={ds.length} acik={!!q || !kapali.has(kat.id)} onDegistir={() => katDegistir(kat.id)}>
              <ul className="cd-satirlar">
                {ds.map((d) => <DersSatiri key={d.key} d={d} k={konum.get(d.key)} />)}
              </ul>
            </KategoriBolumu>
          ))}
        </>
      )}
      {tanitim.tur}
    </div>
  );
}

const sesAdi = (v: CdVaryant) => cdSesKisa(v);

/** Son dinlenen ders: tek dokunuşla kaldığı yerden çalar ve ders ekranını açar */
function DevamKarti({ d, k }: { d: CdListeDers; k: Konum }) {
  const v = d.varyantlar.find((x) => x.id === k.vid) || d.varsayilan || d.varyantlar[0];
  const dur = v?.sureSn || 0;
  const yuklu = useCd((s) => s.key === d.key);
  const canliT = useCd((s) => (s.key === d.key ? Math.floor(s.t) : -1));
  const t = canliT >= 0 ? canliT : k.t;
  const oran = dur ? Math.min(1, t / dur) : 0;
  const devam = () => {
    if (!yuklu) cdOynat(d, v?.id, { t: k.t });
    dersAc(d.key);
  };
  return (
    <section className="cd-devam" aria-label="Kaldığın yerden devam et">
      <span className="cd-ikon" aria-hidden><History /></span>
      <div className="cd-devam-ad">
        <small>{yuklu ? 'Şu an dinlediğin ders' : 'Kaldığın yerden devam et'}</small>
        <b>{cdDersEtiketi(d)} · {d.baslik}</b>
        <span className="cd-ilerleme" aria-hidden><i style={{ transform: `scaleX(${oran})` }} /></span>
        <small className="cd-devam-t">{fmtSure(t)} / {fmtSure(dur)} · %{Math.round(oran * 100)} dinlendi</small>
      </div>
      <button type="button" className="cd-btn is-ana is-buyuk" onClick={devam} aria-label={yuklu ? `Derse dön: ${d.baslik}` : `Devam et: ${d.baslik}, ${fmtSure(k.t)} konumundan`}>
        <Play aria-hidden /> <span>{yuklu ? 'Derse dön' : 'Devam et'}</span>
      </button>
    </section>
  );
}

/** Satırdaki ilerleme: çalan derste canlı, diğerlerinde kayıtlı konum */
function SatirIlerleme({ d, k, dur }: { d: CdListeDers; k?: Konum; dur: number }) {
  const canliT = useCd((s) => (s.key === d.key ? Math.floor(s.t) : -1));
  const t = canliT >= 0 ? canliT : k?.t ?? -1;
  if (t < 5 || !dur) return null;
  const oran = Math.min(1, t / dur);
  return (
    <span className="cd-satir-ilerleme" title={`${fmtSure(t)} / ${fmtSure(dur)}`}>
      <span className="cd-ilerleme" aria-hidden><i style={{ transform: `scaleX(${oran})` }} /></span>
      <span>%{Math.round(oran * 100)}</span>
    </span>
  );
}

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
      download={cdDosyaAdi(cdDersEtiketi(d), d.baslik, v.ses || v.etiket)}
      aria-label={`MP3 indir: ${d.baslik} (${sesAdi(v)}${v.bayt ? `, ${fmtMb(v.bayt)}` : ''})`}
    >
      <Download aria-hidden />
      <span>{kucuk ? 'İndir' : 'MP3'}</span>
    </a>
  );
}

function KategoriBolumu({ kat, n, acik, onDegistir, children }: { kat: CdKategori; n: number; acik: boolean; onDegistir: () => void; children: React.ReactNode }) {
  return (
    <section className={`cd-kat${acik ? '' : ' is-kapali'}`} aria-label={kat.ad}>
      <button type="button" className="cd-kat-bas" aria-expanded={acik} onClick={onDegistir}>
        <span className="cd-kat-ad"><b>{kat.ad}</b>{kat.alt && <small>{kat.alt}</small>}</span>
        <span className="cd-kat-n">{n} ders</span>
        <ChevronDown aria-hidden className="cd-kat-ok" />
      </button>
      {acik && children}
    </section>
  );
}

const DersSatiri = React.memo(function DersSatiri({ d, k }: { d: CdListeDers; k?: Konum }) {
  const [acik, setAcik] = useState(false);
  const v = d.varsayilan || d.varyantlar[0];
  const caliyor = useCd((s) => s.key === d.key && s.playing);
  if (!v) return null;
  const sesN = d.varyantlar.length;
  return (
    <li className={`cd-satir${caliyor ? ' is-caliyor' : ''}${acik ? ' is-acik' : ''}`}>
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
            {sesN > 1 && <span>{sesN} ses</span>}
            <SatirIlerleme d={d} k={k} dur={v.sureSn} />
          </small>
        </a>
        <div className="cd-satir-eylem">
          <button type="button" className="cd-btn is-ana" onClick={() => dersAc(d.key)} aria-label={`Dinle: ${d.baslik} (metin ve slaytlarla)`} title="Metin ve slaytlarla aç">
            <Headphones aria-hidden />
            <span>Dinle</span>
          </button>
          <OynatDugme d={d} v={v} />
        </div>
        <div className="cd-satir-diger">
          <button
            type="button"
            className={`cd-btn is-ikon${acik ? ' is-acik' : ''}`}
            aria-expanded={acik}
            aria-label={`Seçenekler: ${d.baslik} (sesler, MP3, çevrimdışı, listem)`}
            title="Sesler, indirme ve listem"
            onClick={() => setAcik((x) => !x)}
          >
            <MoreHorizontal aria-hidden />
          </button>
        </div>
      </div>
      {acik && (
        <div className="cd-secenek">
          <div className="cd-secenek-arac">
            <CevrimdisiDugme dersKey={d.key} baslik={d.baslik} varyantlar={d.varyantlar} />
            <ListeEkleDugme dersKey={d.key} baslik={d.baslik} etiketli />
            {d.pdf && <span className="cd-secenek-not">Slaytlar sesle birlikte açılır</span>}
          </div>
          <p className="cd-secenek-bas">{sesN > 1 ? `Sesler (${sesN})` : 'Ses'}</p>
          <ul className="cd-varyantlar">
            {d.varyantlar.map((x) => (
              <li key={x.id}>
                <span className="cd-var-ad">
                  <b title={x.etiket || undefined}>{sesAdi(x)}{x.id === v.id && <em> · varsayılan</em>}</b>
                  <small>{[fmtSure(x.sureSn), fmtMb(x.bayt)].filter(Boolean).join(' · ')}</small>
                </span>
                <OynatDugme d={d} v={x} kucuk />
                <IndirDugme d={d} v={x} kucuk />
              </li>
            ))}
          </ul>
        </div>
      )}
    </li>
  );
});
