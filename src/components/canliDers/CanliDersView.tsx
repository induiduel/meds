/**
 * /canliders — herkese açık canlı ders sayfası.
 *  - Liste (/canliders): sesi olan dersler; Dinle (ders ekranı), hızlı Oynat, MP3 İndir, diğer sesler.
 *  - Ders (/canliders/<key>): solda PDF (varsa), sağda konuşma metni; metin sesle akar. Oynatıcı alt sabit
 *    çubuktadır (CanliDersDock, App düzeyinde) — ses öğesi canliDersStore'da tek ve kalıcıdır.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { BarChart3, ChevronDown, Clock, Download, Headphones, History, ListMusic, MoreHorizontal, Pause, Play, Search, Star, X } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import {
  cdDosyaAdi, cdKonumListesi, cdSesKimlik, cdTercihVaryant, cdVarsayilanSesAyarla, useCdVarsayilanSes, cdListeGetir, cdOynat, cdSesKisa, cdSesUrl, cdToggle, fmtMb, fmtSure, useCd,
  type CdListeDers, type CdVaryant,
} from './canliDersStore';
import CanliDersDers from './CanliDersDers';
import { cdListeOzetleri, useCdListe } from './canliDersListe';
import { ListeEkleDugme, Listem } from './CanliDersListem';
import { useCdTur } from './useCdTur';
import { CevrimdisiDugme, useCevrimdisiSuzgec } from './CanliDersCevrimdisi';
import { cdBransKisa, cdDersEtiketi, cdKategoriGrupla, cdKonuSayisi, cdParca, type CdKategori } from './canliDersKategori';
import { useCdTvGezinme } from './CanliDersTv';
import { useYildizliSayisi } from '../../services/yildizliParagrafStore';
import { YildizliParagraflarPanel } from '../study/YildizliParagraflarModal';
import { bittiMi, sureYaz, useKonuKaydi, useTakip } from '../../services/calismaTakip';
import { KonuDugmeleri, KonuIsaret, KonuSureEtiketi } from '../takip/KonuTakip';
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
  useCdTvGezinme('liste');
  const [dersler, setDersler] = useState<CdListeDers[] | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [q, setQ] = useState('');
  const [gorunum, setGorunum] = useState<'tum' | 'liste' | 'yildiz'>(() => (location.hash === '#listem' ? 'liste' : location.hash === '#yildiz' ? 'yildiz' : 'tum'));
  const [sureAcik, setSureAcik] = useState(() => location.hash === '#sureler');
  const listeN = useCdListe((s) => s.keys.length);
  const yildizN = useYildizliSayisi();
  // Oynatıcıdaki "Listem" göstergesi /canliders#listem açar (sayfa zaten açıksa da sekmeye geçilsin)
  useEffect(() => {
    const f = () => {
      if (location.hash === '#listem') setGorunum('liste');
      else if (location.hash === '#yildiz') setGorunum('yildiz');
    };
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
    document.title = 'Sesli ders · MeDSor';
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
            <h1>Sesli ders</h1>
            <p>Dersleri sesli dinle; okunan cümle metinde, anlatılan sayfa slaytta kendiliğinden ilerler.</p>
          </div>
          {tanitim.dugme}
        </div>
        <div className="cd-liste-sira">
          <div className="cd-sekmeler cd-gorunum" role="tablist" aria-label="Görünüm">
            <button type="button" role="tab" aria-selected={gorunum === 'tum'} className={gorunum === 'tum' ? 'is-on' : ''} onClick={() => setGorunum('tum')}>
              <Headphones aria-hidden /> Tüm dersler
            </button>
            <button type="button" role="tab" aria-selected={gorunum === 'liste'} className={gorunum === 'liste' ? 'is-on' : ''} onClick={() => setGorunum('liste')}>
              <ListMusic aria-hidden /> Listem{listeN > 0 && <span className="cd-sekme-sayi">{listeN}</span>}
            </button>
            <button type="button" role="tab" aria-selected={gorunum === 'yildiz'} className={gorunum === 'yildiz' ? 'is-on' : ''} onClick={() => setGorunum('yildiz')}>
              <Star aria-hidden className={yildizN > 0 ? "text-amber-500 fill-amber-500" : ""} /> Yıldızlılar{yildizN > 0 && <span className="cd-sekme-sayi">{yildizN}</span>}
            </button>
          </div>
          <div className="cd-liste-arac">
            <button type="button" className="cd-btn" onClick={() => setSureAcik(true)} aria-haspopup="dialog">
              <Clock aria-hidden /> <span>Süreler</span>
            </button>
            {dersler && <VarsayilanSesSecici dersler={dersler} />}
          </div>
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
      ) : gorunum === 'yildiz' ? (
        <YildizliParagraflarPanel inline onClose={() => setGorunum('tum')} />
      ) : !liste.length ? (
        <div className="cd-bos"><p>{q ? `"${q}" için ders bulunamadı.` : 'Henüz sesi hazır ders yok.'}</p></div>
      ) : (
        <>
          {cevrimdisi.serit}
          {son && !q && suzgec === 'tum' && <DevamKarti d={son.d} k={son.k} />}
          {!q && <SureOzeti dersler={dersler} konum={konum} secili={suzgec} onSec={(id) => setSuzgec(suzgec === id ? 'tum' : id)} onListe={() => setSureAcik(true)} />}
          <div className="cd-kat-cipler" role="group" aria-label="Kategoriye göre süz">
            <button type="button" aria-pressed={suzgec === 'tum'} className={suzgec === 'tum' ? 'is-on' : ''} onClick={() => setSuzgec('tum')}>
              Tümü <span>{cdKonuSayisi(dersler)}</span>
            </button>
            {yarimSayi > 0 && (
              <button type="button" aria-pressed={suzgec === 'yarim'} className={`is-yarim${suzgec === 'yarim' ? ' is-on' : ''}`} onClick={() => setSuzgec('yarim')}>
                <History aria-hidden /> Yarım kalanlar <span>{yarimSayi}</span>
              </button>
            )}
            {tumGruplar.map(({ kat, dersler: ds }) => (
              <button key={kat.id} type="button" aria-pressed={suzgec === kat.id} className={suzgec === kat.id ? 'is-on' : ''}
                onClick={() => setSuzgec(suzgec === kat.id ? 'tum' : kat.id)}>
                {kat.kisa} <span>{cdKonuSayisi(ds)}</span>
              </button>
            ))}
          </div>
          {!gorunenN ? (
            <div className="cd-bos"><p>{q ? `"${q}" için bu kategoride ders bulunamadı.` : 'Bu kategoride ders yok.'}</p></div>
          ) : gruplar.map(({ kat, dersler: ds }) => (
            <KategoriBolumu key={kat.id} kat={kat} n={cdKonuSayisi(ds)} sure={toplamSure(ds)} acik={!!q || !kapali.has(kat.id)} onDegistir={() => katDegistir(kat.id)}>
              <ul className="cd-satirlar">
                {ds.map((d) => <DersSatiri key={d.key} d={d} k={konum.get(d.key)} />)}
              </ul>
            </KategoriBolumu>
          ))}
        </>
      )}
      {sureAcik && dersler && <SureDiyalog dersler={dersler} onKapat={() => { setSureAcik(false); if (location.hash === '#sureler') history.replaceState(history.state, '', location.pathname + location.search); }} />}
      {tanitim.tur}
    </div>
  );
}

/** Varsayılan ses: tüm derslerde ortak sesler (EMA kendiliğinden); seçim cihazda + hesapta saklanır */
function VarsayilanSesSecici({ dersler }: { dersler: CdListeDers[] }) {
  const secili = useCdVarsayilanSes();
  const sesler = useMemo(() => {
    const m = new Map<string, { v: CdVaryant; n: number }>();
    for (const d of dersler) for (const v of d.varyantlar) {
      const k = cdSesKimlik(v);
      const x = m.get(k);
      x ? x.n++ : m.set(k, { v, n: 1 });
    }
    return [...m.entries()].sort((a, b) => Number(/ema/i.test(b[1].v.saglayici || '')) - Number(/ema/i.test(a[1].v.saglayici || '')) || b[1].n - a[1].n);
  }, [dersler]);
  if (sesler.length < 2) return null;
  const ema = sesler.find(([, x]) => /ema/i.test(x.v.saglayici || ''))?.[0];
  const deger = secili && sesler.some(([k]) => k === secili) ? secili : ema || sesler[0][0];
  return (
    <label className="cd-vses">
      <span>Ses</span>
      <select value={deger} onChange={(e) => cdVarsayilanSesAyarla(e.target.value === ema ? null : e.target.value)} aria-label="Varsayılan ses (tüm dersler)">
        {sesler.map(([k, x]) => (
          <option key={k} value={k}>{cdSesKisa(x.v)}{k === ema ? ' (standart)' : ''}{x.n < dersler.length ? ` · ${x.n} ders` : ''}</option>
        ))}
      </select>
    </label>
  );
}

function SureDiyalog({ dersler, onKapat }: { dersler: CdListeDers[]; onKapat: () => void }) {
  const kapatRef = React.useRef<HTMLButtonElement>(null);
  useEffect(() => {
    kapatRef.current?.focus();
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); };
    document.addEventListener('keydown', k);
    const eski = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.removeEventListener('keydown', k); document.body.style.overflow = eski; };
  }, [onKapat]);
  return (
    <div className="cd-dlg" role="presentation" onClick={(e) => { if (e.target === e.currentTarget) onKapat(); }}>
      <div className="cd-dlg-kart is-genis" role="dialog" aria-modal="true" aria-labelledby="cd-sl-b">
        <header className="cd-dlg-bas">
          <b id="cd-sl-b" className="cd-dlg-baslik"><Clock aria-hidden /> Ders süreleri</b>
          <button ref={kapatRef} type="button" className="cd-btn is-ikon" onClick={onKapat} aria-label="Kapat"><X aria-hidden /></button>
        </header>
        <div className="cd-dlg-govde"><SureListesi dersler={dersler} onDersAc={onKapat} /></div>
      </div>
    </div>
  );
}

const sesAdi = (v: CdVaryant) => cdSesKisa(v);

const dersSure = (d: CdListeDers) => (cdTercihVaryant(d.varyantlar) || d.varsayilan)?.sureSn || 0;
const toplamSure = (ds: CdListeDers[]) => ds.reduce((n, d) => n + dersSure(d), 0);
/** "12 sa 40 dk" / "45 dk" */
const fmtSaat = (s: number) => {
  const dk = Math.round(s / 60);
  const h = Math.floor(dk / 60);
  return h ? `${h} sa${dk % 60 ? ` ${dk % 60} dk` : ''}` : `${dk} dk`;
};

/** Konu anlatım süreleri: toplam + branş başına (dokununca o branşa süzer). Açık/kapalı tercihi cihazda saklanır. */
function SureOzeti({ dersler, konum, secili, onSec, onListe }: { dersler: CdListeDers[]; konum: Map<string, Konum>; secili: string; onSec: (id: string) => void; onListe: () => void }) {
  const [acik, setAcik] = useState(() => { try { return localStorage.getItem('medsoru_cd_sure_acik') === '1'; } catch { return false; } });
  const degistir = () => setAcik((x) => { try { localStorage.setItem('medsoru_cd_sure_acik', x ? '0' : '1'); } catch { /* yok */ } return !x; });
  const gruplar = useMemo(() => cdKategoriGrupla(dersler).map((g) => {
    const sure = toplamSure(g.dersler);
    const dinlenen = g.dersler.reduce((n, d) => n + Math.min(dersSure(d), konum.get(d.key)?.t || 0), 0);
    return { ...g, sure, dinlenen, konu: cdKonuSayisi(g.dersler) };
  }), [dersler, konum]);
  const toplam = gruplar.reduce((n, g) => n + g.sure, 0);
  const dinlenen = gruplar.reduce((n, g) => n + g.dinlenen, 0);
  const konu = cdKonuSayisi(dersler);
  const enCok = Math.max(1, ...gruplar.map((g) => g.sure));
  return (
    <section className={`cd-szk${acik ? '' : ' is-kapali'}`} aria-label="Konu anlatım süreleri">
      <button type="button" className="cd-sure-bas" aria-expanded={acik} onClick={degistir}>
        <span className="cd-ikon" aria-hidden><Clock /></span>
        <span className="cd-sure-ana">
          <small>Toplam konu anlatımı</small>
          <b>{fmtSaat(toplam)}</b>
        </span>
        <span className="cd-sure-kutu"><b>{konu}</b><small>konu</small></span>
        <span className="cd-sure-kutu"><b>{fmtSaat(konu ? toplam / konu : 0)}</b><small>ortalama</small></span>
        <span className="cd-sure-kutu"><b>%{toplam ? Math.round((dinlenen / toplam) * 100) : 0}</b><small>dinledin</small></span>
        <span className="cd-sure-ac"><BarChart3 aria-hidden /><span>{acik ? 'Gizle' : 'Branşlar'}</span><ChevronDown aria-hidden className="cd-kat-ok" /></span>
      </button>
      {acik && (
        <ul className="cd-sure-liste">
          {gruplar.map((g) => (
            <li key={g.kat.id}>
              <button type="button" aria-pressed={secili === g.kat.id} className={secili === g.kat.id ? 'is-on' : ''} onClick={() => onSec(g.kat.id)}
                aria-label={`${g.kat.ad}: ${g.konu} konu, ${fmtSaat(g.sure)} anlatım${g.dinlenen > 30 ? `, ${fmtSaat(g.dinlenen)} dinledin` : ''}. Bu branşı göster`}>
                <span className="cd-sure-ad"><b>{g.kat.kisa}</b>{g.kat.alt && <small>{g.kat.alt}</small>}</span>
                <span className="cd-sure-cubuk" aria-hidden>
                  <i style={{ width: `${(g.sure / enCok) * 100}%` }}><em style={{ width: `${g.sure ? (g.dinlenen / g.sure) * 100 : 0}%` }} /></i>
                </span>
                <span className="cd-sure-deger"><b>{fmtSaat(g.sure)}</b><small>{g.konu} konu · ort. {fmtSaat(g.konu ? g.sure / g.konu : 0)}</small></span>
              </button>
            </li>
          ))}
          <li><button type="button" className="cd-sure-tumu" onClick={onListe}><Clock aria-hidden /> Her dersin süresi — tam liste</button></li>
        </ul>
      )}
    </section>
  );
}

const dk = (s: number) => Math.round(s / 60);

/** Süreler sekmesi: her branşta her ders (konu) ayrı satır, dakika + saat; branş ara toplamı ve genel toplam. Part 1/2 tek konu altında. */
function SureListesi({ dersler, onDersAc }: { dersler: CdListeDers[]; onDersAc?: () => void }) {
  const takip = useTakip();
  const harcanan = (ps: CdListeDers[]) => ps.reduce((n, p) => n + (takip.k[`sesli:${p.key}`]?.sn || 0), 0);
  const gruplar = useMemo(() => cdKategoriGrupla(dersler).map((g) => {
    const konular: { no: string; baslik: string; parcalar: CdListeDers[]; sure: number }[] = [];
    for (const d of g.dersler) {
      const son = konular[konular.length - 1];
      if (son && d.parca && son.no === String(d.no)) { son.parcalar.push(d); son.sure += dersSure(d); }
      else konular.push({ no: String(d.no), baslik: d.baslik, parcalar: [d], sure: dersSure(d) });
    }
    return { kat: g.kat, konular, sure: toplamSure(g.dersler) };
  }), [dersler]);
  const toplam = gruplar.reduce((n, g) => n + g.sure, 0);
  const konuN = gruplar.reduce((n, g) => n + g.konular.length, 0);
  return (
    <div className="cd-sl">
      <section className="cd-sl-toplam" aria-label="Tüm dersler toplamı">
        <div><small>Tüm dersler</small><b>{dk(toplam).toLocaleString('tr')} dk</b><span>{fmtSaat(toplam)} · {konuN} konu · {gruplar.length} branş</span></div>
        <ul>
          {gruplar.map((g) => (
            <li key={g.kat.id}><a href={`#sure-${g.kat.id}`} onClick={(e) => { e.preventDefault(); document.getElementById(`sure-${g.kat.id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' }); }}>
              <b>{g.kat.kisa}</b><span>{dk(g.sure)} dk</span></a></li>
          ))}
        </ul>
      </section>
      {gruplar.map((g) => (
        <section key={g.kat.id} id={`sure-${g.kat.id}`} className="cd-sl-grup" aria-label={`${g.kat.ad} süreleri`}>
          <h2><span>{g.kat.ad}{g.kat.alt && <small> · {g.kat.alt}</small>}</span><span className="cd-sl-ara">{g.konular.length} konu · {dk(g.sure)} dk · {fmtSaat(g.sure)}</span></h2>
          <table className="cd-sl-tablo">
            <thead><tr><th scope="col">No</th><th scope="col">Konu</th><th scope="col">Süre</th><th scope="col">Dinlediğin</th></tr></thead>
            <tbody>
              {g.konular.map((k) => (
                <tr key={k.no + k.baslik}>
                  <td className="cd-sl-no">{k.no}</td>
                  <td>
                    <a href={pathFor('canli_ders', k.parcalar[0].key)} onClick={(e) => { if (e.button || e.metaKey || e.ctrlKey) return; e.preventDefault(); onDersAc?.(); dersAc(k.parcalar[0].key); }}>{k.baslik}</a>
                    {k.parcalar.length > 1 && (
                      <small className="cd-sl-parca">{k.parcalar.map((p) => `${cdParca(p)}: ${dk(dersSure(p))} dk`).join(' · ')}</small>
                    )}
                  </td>
                  <td className="cd-sl-sure"><b>{dk(k.sure)} dk</b><small>{fmtSure(k.sure)}</small></td>
                  <td className="cd-sl-sure">{harcanan(k.parcalar) ? <b>{sureYaz(harcanan(k.parcalar))}</b> : <small>—</small>}{k.parcalar.every((p) => bittiMi(takip.k[`sesli:${p.key}`])) && <small className="cd-sl-bitti">bitti</small>}</td>
                </tr>
              ))}
            </tbody>
            <tfoot><tr><td /><th scope="row">{g.kat.kisa} toplamı</th><td className="cd-sl-sure"><b>{dk(g.sure)} dk</b><small>{fmtSaat(g.sure)}</small></td><td className="cd-sl-sure"><b>{sureYaz(harcanan(g.konular.flatMap((x) => x.parcalar)))}</b></td></tr></tfoot>
          </table>
        </section>
      ))}
      <p className="cd-sl-not">Süreler her dersin varsayılan sesine göredir; Part 1/2 olan konular tek satırda toplanır. "Dinlediğin": ses çalarken geçen gerçek süren (tekrar dinlemeler dahil). Konu konu liste: <a href={pathFor('bitirdiklerim')} onClick={(e) => { if (e.button || e.metaKey || e.ctrlKey) return; e.preventDefault(); onDersAc?.(); navigateTo(`${pathFor('bitirdiklerim')}?m=sesli`); }}>Bitirdiklerim</a>.</p>
    </div>
  );
}

/** Son dinlenen ders: tek dokunuşla kaldığı yerden çalar ve ders ekranını açar */
function DevamKarti({ d, k }: { d: CdListeDers; k: Konum }) {
  const v = d.varyantlar.find((x) => x.id === k.vid) || cdTercihVaryant(d.varyantlar) || d.varsayilan;
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

function OynatDugme({ d, v, kucuk, yuvarlak }: { d: CdListeDers; v: CdVaryant; kucuk?: boolean; yuvarlak?: boolean }) {
  const buMu = useCd((s) => s.key === d.key && s.vid === v.id);
  const caliyor = useCd((s) => s.key === d.key && s.vid === v.id && s.playing);
  const etiket = caliyor ? 'Duraklat' : 'Oynat';
  return (
    <button
      type="button"
      className={`cd-btn${kucuk ? ' is-ince' : ''}${yuvarlak ? ' is-yuvarlak' : ''}${buMu ? ' is-on' : ''}`}
      onClick={() => (buMu ? cdToggle() : cdOynat(d, v.id))}
      aria-label={`${etiket}: ${d.baslik}${kucuk ? ` (${sesAdi(v)})` : yuvarlak ? ' (yalnız ses, metin açılmadan)' : ''}`}
      title={yuvarlak ? (caliyor ? 'Duraklat' : 'Yalnız sesi çal — sayfada gezinirken alt çubukta sürer') : undefined}
    >
      {caliyor ? <Pause aria-hidden /> : <Play aria-hidden />}
      {!yuvarlak && <span>{etiket}</span>}
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

function KategoriBolumu({ kat, n, sure, acik, onDegistir, children }: { kat: CdKategori; n: number; sure: number; acik: boolean; onDegistir: () => void; children: React.ReactNode }) {
  return (
    <section className={`cd-kat${acik ? '' : ' is-kapali'}`} aria-label={kat.ad}>
      <button type="button" className="cd-kat-bas" aria-expanded={acik} onClick={onDegistir}>
        <span className="cd-kat-ad"><b>{kat.ad}</b>{kat.alt && <small>{kat.alt}</small>}</span>
        <span className="cd-kat-n">{n} ders · {fmtSaat(sure)}</span>
        <ChevronDown aria-hidden className="cd-kat-ok" />
      </button>
      {acik && children}
    </section>
  );
}

const DersSatiri = React.memo(function DersSatiri({ d, k }: { d: CdListeDers; k?: Konum }) {
  const [acik, setAcik] = useState(false);
  useCdVarsayilanSes();
  const v = cdTercihVaryant(d.varyantlar) || d.varsayilan;
  const caliyor = useCd((s) => s.key === d.key && s.playing);
  const bitti = bittiMi(useKonuKaydi('sesli', d.key));
  if (!v) return null;
  const sesN = d.varyantlar.length;
  return (
    <li className={`cd-satir${caliyor ? ' is-caliyor' : ''}${acik ? ' is-acik' : ''}${bitti ? ' is-bitti' : ''}`}>
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
          <b>{d.parca ? <><em className="cd-parca">{cdParca(d)}</em> </> : null}{d.baslik}</b>
          <small>
            <span>{fmtSure(v.sureSn)}</span>
            {sesN > 1 && <span>{sesN} ses</span>}
            <SatirIlerleme d={d} k={k} dur={v.sureSn} />
            <KonuSureEtiketi modul="sesli" konu={d.key} />
          </small>
        </a>
        <div className="cd-satir-eylem">
          <KonuIsaret modul="sesli" konu={d.key} ad={d.baslik} />
          <OynatDugme d={d} v={v} yuvarlak />
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
            <KonuDugmeleri kucuk modul="sesli" konu={d.key} ad={d.baslik} onTekrar={() => { cdOynat(d, v.id, { t: 0 }); dersAc(d.key); }} />
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
