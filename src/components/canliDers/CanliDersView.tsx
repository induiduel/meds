/**
 * /canliders — herkese açık canlı ders sayfası.
 *  - Liste (/canliders): sesi olan dersler; Dinle (ders ekranı), hızlı Oynat, MP3 İndir, diğer sesler.
 *  - Ders (/canliders/<key>): solda PDF (varsa), sağda konuşma metni; metin sesle akar. Oynatıcı alt sabit
 *    çubuktadır (CanliDersDock, App düzeyinde) — ses öğesi canliDersStore'da tek ve kalıcıdır.
 */
import { icerikGizli, useSiteAyar } from '../../services/siteAyar';
import IcerikKapaliV15 from '../v15/IcerikKapaliV15';
import React, { useEffect, useMemo, useState } from 'react';
import { AlertTriangle, Archive, AudioLines, BookOpen, Check, ChevronDown, Clock, Download, FileText, Headphones, History, Layers, LayoutList, ListMusic, MoreHorizontal, Package, Pause, Play, Search, Star, Video, X } from 'lucide-react';
import { navigateTo, pathFor } from '../../router';
import {
  cdDosyaAdi, cdGunlukGetir, cdKonumListesi, cdMedspakUrl, cdSesKimlik, cdTercihVaryant, cdVarsayilanSesAyarla, useCdVarsayilanSes, cdListeGetir, cdOynat, cdSesKisa, cdSesUrl, cdToggle, fmtMb, fmtSure, useCd,
  type CdGunluk, type CdListeDers, type CdVaryant,
} from './canliDersStore';
import CanliDersDers from './CanliDersDers';
import { TopluPdfDugme } from './CanliDersTopluPdf';
import { cdListeOzetleri, useCdListe } from './canliDersListe';
import { ListeEkleDugme, Listem } from './CanliDersListem';
import { useCdTur } from './useCdTur';
import { CevrimdisiDugme, useCevrimdisiSuzgec } from './CanliDersCevrimdisi';
import { CD_SPOT_BRANS, cdBransKisa, cdBransSlug, cdDersEtiketi, cdKategoriGrupla, cdKonuSayisi, cdParca, type CdKategori } from './canliDersKategori';
import { bransAdresi, icKonum } from '../../siteHaritasi';
import { useCdTvGezinme } from './CanliDersTv';
import { useYildizliSayisi } from '../../services/yildizliParagrafStore';
import { YildizliParagraflarPanel } from '../study/YildizliParagraflarModal';
import { bittiMi, sureYaz, sesliKonuId, useKonuKaydi, useTakip } from '../../services/calismaTakip';
import { KonuDugmeleri, KonuIsaret, KonuSureEtiketi } from '../takip/KonuTakip';
import '../../styles/canli-ders.css';
import '../../styles/canli-ders-liste.css';
import CihazdaIsaret from '../cevrimdisi/CihazdaIsaret';
import { KurulBos, kurulKimlikten, useKurulParam } from '../kurul/KurulSuzgec';
import { KurulSecici } from '../kurul/KurulSecici';
import KMB_INDEX from '../../data/kmb/index.json';
import { useAppearance } from '../../utils/appearance';

const BransV15 = React.lazy(() => import('../v15/BransV15'));
const SesliListeV15 = React.lazy(() => import('../v15/SesliListeV15'));

const fold = (s: string) =>
  s.toLocaleLowerCase('tr').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i').replace(/\s+/g, ' ').trim();

/** Son Prova partı (k1-81-son-prova-patoloji-1) → /son-prova/patoloji/1: aşama soruları yalnız orada çalışır */
export function sonProvaYolu(key: string): string | null {
  const m = /^k\d+-\d+-son-prova-([a-z-]+?)(?:-(\d+))?$/.exec(key);
  return m ? `/son-prova/${m[1].replace(/-/g, '')}/${m[2] || 1}` : null;
}

export default function CanliDersView({ dersKey }: { dersKey?: string }) {
  const sp = dersKey ? sonProvaYolu(dersKey) : null;
  const { v15 } = useAppearance();
  useSiteAyar();
  useEffect(() => { if (sp) navigateTo(sp); }, [sp]);
  if (sp) return null;
  // v15: branş adresi (/dersler/canliders/kurulN/<branş>) branş ders listesini açar (components/v15/BransV15)
  if (!dersKey && v15 && new URLSearchParams(icKonum().search).get('brans')) return <React.Suspense fallback={null}><BransV15 /></React.Suspense>;
  // v15: branşsız liste (arşiv dönemi ve #listem gibi özel görünümler eski listede kalır)
  if (!dersKey && v15 && !window.location.hash) return <React.Suspense fallback={null}><SesliListeV15 /></React.Suspense>;
  if (dersKey && icerikGizli('sesli', dersKey)) return <IcerikKapaliV15 ne="Bu ders" geri={{ yol: '/dersler/canliders', etiket: 'Sesli derslere dön' }} />;
  return dersKey ? <CanliDersDers key={dersKey} dersKey={dersKey} /> : <CanliDersListe />;
}

/** Sesli ders kategorisinin adres adı (Tıbbi Genetik → tbg; Kurul 2+ branşları adından) */
const katSlug = (kat: CdKategori) => cdBransSlug(kat.ad);

const dersAc = (key: string) => navigateTo(pathFor('canli_ders', key));

type Konum = { vid: string; t: number; at: number };
/** Kaldığın yer: sayfa açılınca bir kez okunur (ders ekranından dönünce liste yeniden kurulur). */
const konumHaritasi = () => new Map(cdKonumListesi().map((k) => [k.key, k as Konum]));

type ListeGorunum = 'tum' | 'yarim' | 'liste' | 'yildiz' | 'blok';
const HASH_GORUNUM: Record<string, ListeGorunum> = { '#listem': 'liste', '#yildiz': 'yildiz', '#blok': 'blok', '#yarim': 'yarim' };
const KAPALI_KEY = 'medsoru_canli_ders_kapali_kat_v1';
const kapaliOku = (): Set<string> => { try { return new Set(JSON.parse(localStorage.getItem(KAPALI_KEY) || '[]')); } catch { return new Set(); } };

/**
 * Liste iskeleti (2026-10-24 yeniden kurulum):
 *  - üst: başlık + genel ilerleme, arama, araçlar (süreler, ses, toplu PDF, tanıtım)
 *  - sol ray (telefonda üstte yatay şeritler): kurul, görünüm (Tüm / Yarım kalan / Listem / Yıldızlı / Blok), branşlar (ilerleme çubuğuyla)
 *  - içerik: "Devam et" + "Sıradaki ders" kartları, branş bölümleri (bitti/toplam, sıradakini dinle), ders satırları
 */
type CdDonemSecim = '2026-2027' | '2025-2026' | 'sinama';
const donemOku = (): CdDonemSecim => {
  const d = new URLSearchParams(icKonum().search).get('donem');
  return d === '2025-2026' ? '2025-2026' : d === 'sinama' ? 'sinama' : '2026-2027';
};
function CanliDersListe() {
  useCdTvGezinme('liste');
  const [donem, setDonem0] = useState<CdDonemSecim>(() => donemOku());
  // Sınama (test) dersleri yalnız varsa seçenek görünür (data/sinama.json)
  const [sinamaVar, setSinamaVar] = useState(false);
  useEffect(() => { cdListeGetir(false, 'sinama').then((l) => setSinamaVar(l.length > 0), () => { /* yok */ }); }, []);
  const [hamDersler, setDersler] = useState<CdListeDers[] | null>(null);
  // Blok özetler (k1-95-blok-ozet-patoloji-1 …): birkaç dersi tek sesli derste anlatır; ayrı görünümde listelenir
  const [hamBlok, setBlok] = useState<CdListeDers[]>([]);
  const kurul = useKurulParam();
  // ?kurul=N: yalnız o kurulun dersleri (parametre yoksa hepsi)
  const dersler = useMemo(
    () => (hamDersler && kurul ? hamDersler.filter((d) => (d.kurul ?? kurulKimlikten(d.key)) === kurul) : hamDersler),
    [hamDersler, kurul],
  );
  const [hata, setHata] = useState<string | null>(null);
  const [q, setQ] = useState('');
  const [gorunum, setGorunum0] = useState<ListeGorunum>(() => HASH_GORUNUM[location.hash] || 'tum');
  const setGorunum = (g: ListeGorunum) => {
    setGorunum0(g);
    const h = Object.entries(HASH_GORUNUM).find(([, v]) => v === g)?.[0] || '';
    try { history.replaceState(history.state, '', location.pathname + location.search + h); } catch { /* yok */ }
  };
  const blok = useMemo(() => (kurul ? hamBlok.filter((d) => (d.kurul ?? kurulKimlikten(d.key)) === kurul) : hamBlok), [hamBlok, kurul]);
  const [sureAcik, setSureAcik] = useState(() => location.hash === '#sureler');
  const [gunlukModalKey, setGunlukModalKey] = useState<string | null>(null);
  const listeN = useCdListe((s) => s.keys.length);
  const yildizN = useYildizliSayisi();
  const takip = useTakip();
  // Oynatıcıdaki "Listem" göstergesi /canliders#listem açar (sayfa zaten açıksa da görünüme geçilsin)
  useEffect(() => {
    const f = () => {
      const g = HASH_GORUNUM[location.hash];
      if (g) setGorunum0(g);
      setDonem0(donemOku());
    };
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  /** 'tum' | kategori kimliği */
  const [suzgec, setSuzgec0] = useState<string>('tum');
  // Adresteki branş (/dersler/canliders/kurul1/tbg → ?brans=tbg): liste gelince o branş seçilir
  const [urlBrans] = useState(() => new URLSearchParams(icKonum().search).get('brans'));
  const [kapali, setKapali] = useState<Set<string>>(kapaliOku);
  const [konum] = useState(konumHaritasi);
  const tanitim = useCdTur('liste', !!dersler?.length, () => !!document.querySelector('.cd-satir'));

  const setDonem = (yeni: CdDonemSecim) => {
    if (yeni === donem) return;
    setDonem0(yeni);
    setSuzgec0('tum');
    const sp = new URLSearchParams(icKonum().search);
    if (yeni !== '2026-2027') sp.set('donem', yeni);
    else sp.delete('donem');
    const qs = sp.toString();
    try { history.replaceState(history.state, '', `/canliders${qs ? `?${qs}` : ''}`); } catch { /* yok */ }
  };

  const yukle = (yenile = false, aktifDonem = donem) => {
    setHata(null);
    setDersler(null);
    cdListeGetir(yenile, aktifDonem).then((ds) => { cdListeOzetleri(ds); setDersler(ds.filter((d) => !/-son-prova-|-blok-ozet-/.test(d.key) && !icerikGizli('sesli', d.key))); setBlok(ds.filter((d) => /-blok-ozet-/.test(d.key))); /* Son Prova partları kendi sayfasında (/son-prova) */ }, (e) => setHata(e?.message || 'Liste alınamadı.'));
  };
  useEffect(() => {
    document.title = donem === '2025-2026' ? '2025-2026 Arşiv Sesli Dersler · MeDSor' : donem === 'sinama' ? 'Sınama (test verisi) Sesli Dersler · MeDSor' : 'Sesli ders · MeDSor';
    yukle(false, donem);
  }, [donem]);

  const bitti = (d: CdListeDers) => bittiMi(takip.k[`sesli:${sesliKonuId(d.key)}`]);
  const liste = useMemo(() => {
    if (!dersler) return [];
    const f = fold(q);
    let l = gorunum === 'yarim' ? dersler.filter((d) => konum.has(d.key)) : dersler;
    if (f) l = l.filter((d) => fold(`${d.brans ? `${d.brans} ${cdBransKisa(d.brans)} ` : ''}${d.no} ${d.baslik}`).includes(f));
    return l;
  }, [dersler, q, gorunum, konum]);
  const cevrimdisi = useCevrimdisiSuzgec(liste);
  // Tüm derslerin kategorileri (ray sayıları aramadan bağımsız); görünen gruplar süzülmüş listeden
  const tumGruplar = useMemo(() => cdKategoriGrupla(dersler || []), [dersler]);
  const gruplar = useMemo(() => {
    const g = cdKategoriGrupla(cevrimdisi.liste);
    return suzgec === 'tum' ? g : g.filter((x) => x.kat.id === suzgec);
  }, [cevrimdisi.liste, suzgec]);
  // Branş seçilince adres de o branşa döner (/dersler/canliders/kurul<N>/<branş>); paylaşılabilir, geri tuşu bozulmaz
  const setSuzgec = (id: string) => {
    setSuzgec0(id);
    if (gorunum !== 'tum' && gorunum !== 'yarim') setGorunum0('tum');
    const kat = tumGruplar.find((g) => g.kat.id === id);
    const k = kurul ?? kat?.dersler[0]?.kurul ?? (dersler?.[0] ? (dersler[0].kurul ?? kurulKimlikten(dersler[0].key)) : null);
    const sp = new URLSearchParams(icKonum().search);
    sp.delete('brans'); sp.delete('kurul');
    if (kat && k) { sp.set('kurul', String(k)); sp.set('brans', katSlug(kat.kat)); } else if (kurul) sp.set('kurul', String(kurul));
    const qs = sp.toString();
    try { history.replaceState(history.state, '', `/canliders${qs ? `?${qs}` : ''}`); } catch { /* yok */ }
    document.querySelector('.cdl-icerik')?.scrollIntoView({ block: 'start', behavior: 'smooth' });
  };
  useEffect(() => {
    if (!urlBrans || !tumGruplar.length) return;
    const g = tumGruplar.find((x) => katSlug(x.kat) === urlBrans) || tumGruplar.find((x) => fold(x.kat.ad).includes(urlBrans.replace(/-/g, ' ')));
    if (g) setSuzgec0(g.kat.id);
  }, [urlBrans, tumGruplar]);
  const gorunenN = gruplar.reduce((n, g) => n + g.dersler.length, 0);
  const katDegistir = (id: string) => setKapali((s) => {
    const n = new Set(s); n.has(id) ? n.delete(id) : n.add(id);
    try { localStorage.setItem(KAPALI_KEY, JSON.stringify([...n])); } catch { /* yok */ }
    return n;
  });
  const yarimSayi = useMemo(() => (dersler ? dersler.filter((d) => konum.has(d.key)).length : 0), [dersler, konum]);
  const bittiN = useMemo(() => (dersler ? dersler.filter(bitti).length : 0), [dersler, takip]);
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
  // Sıradaki ders: son dinlenenin branşında ondan sonraki bitmemiş ders; yoksa ilk bitmemiş ders
  const siradaki = useMemo(() => {
    if (!dersler?.length) return null;
    const sira = tumGruplar.flatMap((g) => g.dersler);
    const i = son ? sira.findIndex((d) => d.key === son.d.key) : -1;
    const aday = [...sira.slice(i + 1), ...sira.slice(0, Math.max(0, i))].find((d) => !bitti(d) && d.key !== son?.d.key);
    return aday || null;
  }, [dersler, tumGruplar, son, takip]);
  const odak = gorunum === 'tum' && !q && suzgec === 'tum';
  const oran = dersler?.length ? bittiN / dersler.length : 0;

  return (
    <div className="cd-root cd-liste cdl">
      <header className="cdl-ust">
        <div className="cdl-kimlik cd-liste-baslik">
          <span className="cdl-halka" style={{ '--x': oran } as React.CSSProperties} aria-hidden><Headphones /></span>
          <div>
            <h1>Sesli Dersler</h1>
            <p>{dersler ? <>{cdKonuSayisi(dersler)} ders · {fmtSaat(toplamSure(dersler))} · <b>{bittiN} bitti</b></> : 'Yükleniyor…'}</p>
          </div>
        </div>
        <label className="cd-ara cdl-ara">
          <Search aria-hidden />
          <input type="search" value={q} onChange={(e) => { setQ(e.target.value); if (gorunum !== 'tum' && gorunum !== 'yarim') setGorunum0('tum'); }}
            placeholder="Ders ara: ad, branş ya da numara" aria-label="Ders ara" />
          {q && <button type="button" className="cd-ara-sil" onClick={() => setQ('')} aria-label="Aramayı temizle"><X /></button>}
        </label>
        <div className="cdl-arac">
          <button type="button" className="cd-btn" onClick={() => setSureAcik(true)} aria-haspopup="dialog"><Clock aria-hidden /> <span>Süreler</span></button>
          {dersler && <VarsayilanSesSecici dersler={dersler} />}
          {dersler && !!dersler.length && <TopluPdfDugme dersler={cevrimdisi.liste.length ? cevrimdisi.liste : dersler} />}
          {tanitim.dugme}
        </div>
      </header>

      <div className="cdl-govde">
        <aside className="cdl-ray" aria-label="Sesli ders gezinme">
          <div className="cdl-donem-sec" role="group" aria-label="Akademik dönem seçimi">
            <button
              type="button"
              className={`cdl-donem-btn${donem === '2026-2027' ? ' is-on' : ''}`}
              aria-pressed={donem === '2026-2027'}
              onClick={() => setDonem('2026-2027')}
            >
              <b>2026-2027</b>
              <small>Güncel Dönem</small>
            </button>
            <button
              type="button"
              className={`cdl-donem-btn is-arsiv${donem === '2025-2026' ? ' is-on' : ''}`}
              aria-pressed={donem === '2025-2026'}
              onClick={() => setDonem('2025-2026')}
            >
              <b>2025-2026</b>
              <small>Geçen Yıl Arşivi</small>
            </button>
            {(sinamaVar || donem === 'sinama') && (
              <button
                type="button"
                className={`cdl-donem-btn is-sinama${donem === 'sinama' ? ' is-on' : ''}`}
                aria-pressed={donem === 'sinama'}
                onClick={() => setDonem('sinama')}
              >
                <b>Sınama</b>
                <small>Test verisi</small>
              </button>
            )}
          </div>
          <KurulSecici
            className="cdl-kurul"
            secili={kurul}
            yol={(k) => `/dersler/canliders/kurul${k}${donem !== '2026-2027' ? `?donem=${donem}` : ''}`}
            tumuYol={`/dersler/canliders${donem !== '2026-2027' ? `?donem=${donem}` : ''}`}
          />
          <nav className="cdl-gorunum" aria-label="Görünüm">
            <RayDugme on={gorunum === 'tum'} ikon={<LayoutList />} ad="Tüm dersler" n={dersler ? cdKonuSayisi(dersler) : undefined} onClick={() => setGorunum('tum')} />
            {yarimSayi > 0 && <RayDugme on={gorunum === 'yarim'} ikon={<History />} ad="Yarım kalanlar" n={yarimSayi} onClick={() => setGorunum('yarim')} />}
            <RayDugme on={gorunum === 'liste'} ikon={<ListMusic />} ad="Listem" n={listeN || undefined} onClick={() => setGorunum('liste')} />
            <RayDugme on={gorunum === 'yildiz'} ikon={<Star />} ad="Yıldızlılar" n={yildizN || undefined} onClick={() => setGorunum('yildiz')} />
            {blok.length > 0 && <RayDugme on={gorunum === 'blok'} ikon={<Layers />} ad="Blok özetler" n={blok.length} onClick={() => setGorunum('blok')} />}
          </nav>
          {dersler && !!dersler.length && (gorunum === 'tum' || gorunum === 'yarim') && (
            <nav className="cdl-branslar cd-kat-cipler" aria-label="Branşa göre süz">
              <p className="cdl-ray-bas">Branşlar</p>
              <button type="button" aria-pressed={suzgec === 'tum'} className={`cdl-brans${suzgec === 'tum' ? ' is-on' : ''}`} onClick={() => setSuzgec('tum')}>
                <span className="cdl-brans-ad">Tümü</span><span className="cdl-brans-n">{cdKonuSayisi(dersler)}</span>
              </button>
              {tumGruplar.map(({ kat, dersler: ds }) => {
                const b = ds.filter(bitti).length;
                return (
                  <button key={kat.id} type="button" aria-pressed={suzgec === kat.id} className={`cdl-brans${suzgec === kat.id ? ' is-on' : ''}`}
                    onClick={() => setSuzgec(suzgec === kat.id ? 'tum' : kat.id)} title={`${kat.ad}: ${b}/${ds.length} bitti`}>
                    <span className="cdl-brans-ad">{kat.kisa}</span>
                    <span className="cdl-brans-n">{b ? `${b}/` : ''}{ds.length}</span>
                    <span className="cdl-brans-cubuk" aria-hidden><i style={{ transform: `scaleX(${ds.length ? b / ds.length : 0})` }} /></span>
                  </button>
                );
              })}
            </nav>
          )}
          <KmbKarti />
        </aside>

        <main className="cdl-icerik">
          {donem === 'sinama' && (
            <div className="cd-arsiv-uyari is-sinama" role="note">
              <AlertTriangle aria-hidden />
              <div>
                <b>SINAMA — test verisi</b>
                <p>
                  Bu bölümdeki dersler sınama amacıyla eklenmiş test verisidir; içerikleri henüz doğrulanmış güncel ders sayılmaz.
                  <b> Güncel dönem derslerinin listesinde görünmezler</b>, ikisi aynı anda gösterilmez.
                </p>
              </div>
            </div>
          )}
          {donem === '2025-2026' && (
            <div className="cd-arsiv-uyari" role="note">
              <AlertTriangle aria-hidden />
              <div>
                <b>2025-2026 Dönemi (Geçen Yıl Arşivi · Kurul 2–6 Sınama Paketi)</b>
                <p>
                  Bu listedeki dersler geçen yılın (2025-2026) slaytlarından ve çıkmış sorularından üretilmiş arşiv dersleridir.
                  <b> 2026-2027 güncel dönem dersleriyle kesinlikle karışmaz</b>; yeni dönem PDF'leri gelene kadar ön çalışma ve sınama amacıyla ayrı veritabanında tutulmaktadır.
                </p>
              </div>
            </div>
          )}
          {odak && dersler && (son || siradaki) && (
            <div className="cdl-kahraman">
              {son && <DevamKarti d={son.d} k={son.k} />}
              {siradaki && <SiradakiKart d={siradaki} ilk={!son} />}
            </div>
          )}
          {hata ? (
            <div className="cd-bos">
              <p>{hata}</p>
              <button type="button" className="cd-btn" onClick={() => yukle(true)}>Yeniden dene</button>
            </div>
          ) : !dersler ? (
            <div className="cd-bos" role="status"><span className="cd-spin" aria-hidden /> Dersler yükleniyor…</div>
          ) : gorunum === 'liste' ? (
            <Listem dersler={dersler} onTumu={() => setGorunum('tum')} />
          ) : gorunum === 'blok' ? (
            <section className="cd-kat cdl-kat">
              <div className="cdl-kat-bas"><span className="cdl-kat-ad"><b>Blok özetler</b><small>Birkaç dersi tek sesli derste, çıkmış sorulara odaklanarak anlatır. Her biri bir ile iki saat arası.</small></span></div>
              <ul className="cd-satirlar">{blok.map((d) => <DersSatiri key={d.key} d={d} k={konum.get(d.key)} />)}</ul>
            </section>
          ) : gorunum === 'yildiz' ? (
            <YildizliParagraflarPanel inline onClose={() => setGorunum('tum')} />
          ) : kurul && !dersler.length ? (
            <KurulBos kurul={kurul} ne="sesli ders" />
          ) : !liste.length ? (
            <div className="cd-bos"><p>{q ? `"${q}" için ders bulunamadı.` : gorunum === 'yarim' ? 'Yarım kalan ders yok.' : 'Henüz sesi hazır ders yok.'}</p></div>
          ) : (
            <>
              {cevrimdisi.serit}
              {!gorunenN ? (
                <div className="cd-bos"><p>{q ? `"${q}" için bu branşta ders bulunamadı.` : 'Bu branşta ders yok.'}</p></div>
              ) : gruplar.map(({ kat, dersler: ds }) => (
                <KategoriBolumu key={kat.id} kat={kat} ds={ds} bitenN={ds.filter(bitti).length} sonraki={ds.find((d) => !bitti(d))}
                  acik={!!q || suzgec !== 'tum' || !kapali.has(kat.id)} onDegistir={() => katDegistir(kat.id)}>
                  <ul className="cd-satirlar">
                    {ds.map((d) => <DersSatiri key={d.key} d={d} k={konum.get(d.key)} onGunlukAc={setGunlukModalKey} />)}
                  </ul>
                </KategoriBolumu>
              ))}
            </>
          )}
        </main>
      </div>
      {sureAcik && dersler && <SureDiyalog dersler={dersler} onKapat={() => { setSureAcik(false); if (location.hash === '#sureler') history.replaceState(history.state, '', location.pathname + location.search); }} />}
      {gunlukModalKey && <GunlukDiyalog dersKey={gunlukModalKey} onKapat={() => setGunlukModalKey(null)} />}
      {tanitim.tur}
    </div>
  );
}

function RayDugme({ on, ikon, ad, n, onClick }: { on: boolean; ikon: React.ReactNode; ad: string; n?: number; onClick: () => void }) {
  return (
    <button type="button" className={`cdl-rd${on ? ' is-on' : ''}`} aria-current={on ? 'page' : undefined} onClick={onClick}>
      <span className="cdl-rd-ikon" aria-hidden>{ikon}</span>
      <span className="cdl-rd-ad">{ad}</span>
      {n != null && <span className="cdl-rd-n">{n}</span>}
    </button>
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


const dk = (s: number) => Math.round(s / 60);

/** Süreler sekmesi: her branşta her ders (konu) ayrı satır, dakika + saat; branş ara toplamı ve genel toplam. Part 1/2 tek konu altında. */
function SureListesi({ dersler, onDersAc }: { dersler: CdListeDers[]; onDersAc?: () => void }) {
  const takip = useTakip();
  const harcanan = (ps: CdListeDers[]) => ps.reduce((n, p) => n + (takip.k[`sesli:${sesliKonuId(p.key)}`]?.sn || 0), 0);
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
  const kokRef = React.useRef<HTMLDivElement>(null);
  const topRef = React.useRef<HTMLElement>(null);
  useEffect(() => {
    const el = topRef.current; if (!el || typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(() => kokRef.current?.style.setProperty('--sl-top', `${el.offsetHeight}px`));
    ro.observe(el); return () => ro.disconnect();
  }, []);
  return (
    <div className="cd-sl" ref={kokRef}>
      <section ref={topRef} className="cd-sl-toplam" aria-label="Tüm dersler toplamı">
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
                  <td className="cd-sl-sure">{harcanan(k.parcalar) ? <b>{sureYaz(harcanan(k.parcalar))}</b> : <small>—</small>}{k.parcalar.every((p) => bittiMi(takip.k[`sesli:${sesliKonuId(p.key)}`])) && <small className="cd-sl-bitti">bitti</small>}</td>
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
  const caliyor = useCd((s) => s.key === d.key && s.playing);
  const canliT = useCd((s) => (s.key === d.key ? Math.floor(s.t) : -1));
  const t = canliT >= 0 ? canliT : k.t;
  const oran = dur ? Math.min(1, t / dur) : 0;
  const devam = () => {
    if (!yuklu) cdOynat(d, v?.id, { t: k.t });
    dersAc(d.key);
  };
  return (
    <section className="cdl-kart is-devam" aria-label="Kaldığın yerden devam et">
      <small className="cdl-kart-ust">{caliyor ? 'Şu an çalıyor' : yuklu ? 'Duraklatıldı' : 'Kaldığın yerden devam et'}</small>
      <b className="cdl-kart-ad">{d.baslik}</b>
      <span className="cdl-kart-alt">{cdDersEtiketi(d)} · {fmtSure(Math.max(0, dur - t))} kaldı</span>
      <span className="cd-ilerleme cdl-kart-cubuk" aria-hidden><i style={{ transform: `scaleX(${oran})` }} /></span>
      <div className="cdl-kart-eylem">
        <button type="button" className="cd-btn is-ana" onClick={devam}>
          <Play aria-hidden /> {yuklu ? 'Derse dön' : `Devam et · ${fmtSure(k.t)}`}
        </button>
        {yuklu && (
          <button type="button" className="cd-btn" onClick={() => cdToggle()} aria-label={caliyor ? 'Duraklat' : 'Sesi sürdür'}>
            {caliyor ? <Pause aria-hidden /> : <Play aria-hidden />} <span>{caliyor ? 'Duraklat' : 'Sürdür'}</span>
          </button>
        )}
      </div>
    </section>
  );
}

/** Sıradaki önerilen ders: son dinlenenden sonra gelen ilk bitmemiş ders */
function SiradakiKart({ d, ilk }: { d: CdListeDers; ilk: boolean }) {
  const v = cdTercihVaryant(d.varyantlar) || d.varsayilan;
  return (
    <section className="cdl-kart is-sira" aria-label="Sıradaki ders">
      <small className="cdl-kart-ust">{ilk ? 'Buradan başla' : 'Sıradaki ders'}</small>
      <b className="cdl-kart-ad">{d.baslik}</b>
      <span className="cdl-kart-alt">{cdDersEtiketi(d)}{v ? ` · ${fmtSure(v.sureSn)}` : ''}</span>
      <div className="cdl-kart-eylem">
        <button type="button" className="cd-btn" onClick={() => dersAc(d.key)}><BookOpen aria-hidden /> Dersi aç</button>
        {v && <OynatDugme d={d} v={v} />}
      </div>
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
  const etiket = caliyor ? 'Duraklat' : yuvarlak ? 'Oynat' : 'Yalnız sesi çal';
  return (
    <button
      type="button"
      className={`cd-btn${kucuk ? ' is-ince' : ''}${yuvarlak ? ' is-yuvarlak' : ''}${buMu ? ' is-on' : ''}`}
      onClick={() => (buMu ? cdToggle() : cdOynat(d, v.id))}
      aria-label={`${etiket}: ${d.baslik}${kucuk ? ` (${sesAdi(v)})` : yuvarlak ? ' (yalnız ses, metin açılmadan)' : ''}`}
      title={yuvarlak ? (caliyor ? 'Duraklat' : 'Yalnız sesi çal — sayfada gezinirken alt çubukta sürer') : undefined}
    >
      {caliyor ? <Pause aria-hidden /> : <Play aria-hidden />}
      {!yuvarlak && <span>{kucuk ? (caliyor ? 'Duraklat' : 'Oynat') : etiket}</span>}
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

/** Branş bölümü: başlıkta ilerleme (bitti/toplam), toplam süre ve "Sıradakini aç"; başlığa dokununca katlanır */
function KategoriBolumu({ kat, ds, bitenN, sonraki, acik, onDegistir, children }: {
  kat: CdKategori; ds: CdListeDers[]; bitenN: number; sonraki?: CdListeDers; acik: boolean; onDegistir: () => void; children: React.ReactNode;
}) {
  const n = cdKonuSayisi(ds);
  return (
    <section className={`cd-kat cdl-kat${acik ? '' : ' is-kapali'}`} aria-label={kat.ad}>
      <div className="cdl-kat-bas">
        <button type="button" className="cdl-kat-ac" aria-expanded={acik} onClick={onDegistir}>
          <ChevronDown aria-hidden className="cd-kat-ok" />
          <span className="cdl-kat-ad"><b>{kat.ad}</b><small>{kat.alt ? `${kat.alt} · ` : ''}{n} ders · {fmtSaat(toplamSure(ds))}</small></span>
        </button>
        <span className="cdl-kat-ilerleme" title={`${bitenN}/${ds.length} bitti`}>
          <span className="cd-ilerleme" aria-hidden><i style={{ transform: `scaleX(${ds.length ? bitenN / ds.length : 0})` }} /></span>
          <small>{bitenN}/{ds.length} bitti</small>
        </span>
        {sonraki && (
          <button type="button" className="cd-btn is-ince cdl-kat-sira" onClick={() => dersAc(sonraki.key)} title={`Sıradaki: ${sonraki.baslik}`}>
            <Play aria-hidden /> <span>{bitenN ? 'Sıradakini aç' : 'Başla'}</span>
          </button>
        )}
      </div>
      {acik && children}
    </section>
  );
}

const DersSatiri = React.memo(function DersSatiri({ d, k, onGunlukAc }: { d: CdListeDers; k?: Konum; onGunlukAc?: (key: string) => void }) {
  const [acik, setAcik] = useState(false);
  useCdVarsayilanSes();
  const v = cdTercihVaryant(d.varyantlar) || d.varsayilan;
  const caliyor = useCd((s) => s.key === d.key && s.playing);
  const bitti = bittiMi(useKonuKaydi('sesli', d.key));
  if (!v) return null;
  const sesN = d.varyantlar.length;
  const isArsiv = d.arsiv || d.donem === '2025-2026' || d.key.startsWith('y25-');
  return (
    <li className={`cd-satir cdl-satir${caliyor ? ' is-caliyor' : ''}${acik ? ' is-acik' : ''}${bitti ? ' is-bitti' : ''}${isArsiv ? ' is-arsiv' : ''}`}>
      <div className="cdl-satir-ana">
        <span className="cdl-no" aria-hidden>{bitti ? <Check /> : caliyor ? <AudioLines /> : d.no}</span>
        <a
          className="cd-satir-ad cdl-satir-ad"
          href={pathFor('canli_ders', d.key)}
          onClick={(e) => {
            if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
            e.preventDefault();
            dersAc(d.key);
          }}
        >
          <b>
            {isArsiv && <span className="cd-chip is-arsiv">2025-2026 Arşiv</span>}
            {d.sinama && <span className="cd-chip is-arsiv is-sinama">SINAMA</span>}
            {d.parca ? <><em className="cd-parca">{cdParca(d)}</em> </> : null}
            {d.baslik}
          </b>
          <small>
            <span>{fmtSure(v.sureSn)}</span>
            {d.pdf && <span>slaytlı</span>}
            {d.desteId && <span>Öğren desteli</span>}
            {d.medspakVar && <span>.medspak</span>}
            {sesN > 1 && <span>{sesN} ses</span>}
            <SatirIlerleme d={d} k={k} dur={v.sureSn} />
            <CihazdaIsaret paket={`sesli:${d.key}`} indir={false} />
            <KonuSureEtiketi modul="sesli" konu={d.key} />
          </small>
        </a>
        <div className="cdl-satir-eylem">
          {d.gunlukVar && onGunlukAc && (
            <button
              type="button"
              className="cd-btn is-ince"
              onClick={() => onGunlukAc(d.key)}
              title="Sesli ders güncelleme günlüğü"
            >
              <FileText aria-hidden /> <span>Günlük</span>
            </button>
          )}
          <KonuIsaret modul="sesli" konu={d.key} ad={d.baslik} />
          <OynatDugme d={d} v={v} yuvarlak />
          <button
            type="button"
            className={`cd-btn is-ikon${acik ? ' is-on' : ''}`}
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
            {d.desteId && (
              <button type="button" className="cd-btn is-ince" onClick={() => navigateTo(`/dersler/interaktif/${d.desteId}`)}>
                <BookOpen aria-hidden /> <span>Öğren Destesi</span>
              </button>
            )}
            {d.medspakVar && (
              <a className="cd-btn is-ince" href={cdMedspakUrl(d.key)} download={`${d.key}.medspak`}>
                <Package aria-hidden /> <span>.medspak İndir</span>
              </a>
            )}
            {onGunlukAc && (
              <button type="button" className="cd-btn is-ince" onClick={() => onGunlukAc(d.key)}>
                <FileText aria-hidden /> <span>Güncelleme Günlüğü</span>
              </button>
            )}
            <KonuDugmeleri kucuk modul="sesli" konu={d.key} ad={d.baslik} onTekrar={() => { cdOynat(d, v.id, { t: 0 }); dersAc(d.key); }} />
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

export function GunlukDiyalog({ dersKey, onKapat }: { dersKey: string; onKapat: () => void }) {
  const [veri, setVeri] = useState<CdGunluk | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const kapatRef = React.useRef<HTMLButtonElement>(null);

  useEffect(() => {
    kapatRef.current?.focus();
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') onKapat(); };
    document.addEventListener('keydown', k);
    cdGunlukGetir(dersKey).then(setVeri, (e) => setHata(e?.message || 'Günlük alınamadı.'));
    return () => document.removeEventListener('keydown', k);
  }, [dersKey, onKapat]);

  return (
    <div className="cd-dlg" role="presentation" onClick={(e) => { if (e.target === e.currentTarget) onKapat(); }}>
      <div className="cd-dlg-kart is-genis" role="dialog" aria-modal="true" aria-labelledby="cd-gnl-b">
        <header className="cd-dlg-bas">
          <b id="cd-gnl-b" className="cd-dlg-baslik"><FileText aria-hidden /> Güncelleme Günlüğü · {veri?.baslik || dersKey}</b>
          <button ref={kapatRef} type="button" className="cd-btn is-ikon" onClick={onKapat} aria-label="Kapat"><X aria-hidden /></button>
        </header>
        <div className="cd-dlg-govde cd-gunluk-govde">
          {hata ? (
            <p className="cd-hata">{hata}</p>
          ) : !veri ? (
            <div className="cd-bos" role="status"><span className="cd-spin" aria-hidden /> Günlük yükleniyor…</div>
          ) : !veri.kayitlar.length ? (
            <p className="cd-bos">Bu ders için henüz kayıtlı güncelleme günlüğü yok.</p>
          ) : (
            <div className="cd-gunluk-liste">
              <div className="cd-gunluk-ust">
                <span className="cd-chip is-arsiv">Dönem: {veri.donem}</span>
                <span className="cd-chip">Kurul {veri.kurul}</span>
                {veri.brans && <span className="cd-chip">{veri.brans}</span>}
              </div>
              {veri.kayitlar.slice().reverse().map((k) => (
                <article key={k.surum} className="cd-gunluk-kart">
                  <header className="cd-gunluk-kart-bas">
                    <b>Sürüm v{k.surum}</b>
                    <time>{k.tarih}</time>
                  </header>
                  <p className="cd-gunluk-neden"><b>Güncelleme Nedeni:</b> {k.neden}</p>
                  {k.metrikler && (
                    <div className="cd-gunluk-metrikler">
                      {k.metrikler.sureDk != null && <span>Süre: <b>{k.metrikler.sureDk} dk</b></span>}
                      {k.metrikler.sayfaSayisi != null && <span>PDF Sayfa: <b>{k.metrikler.sayfaSayisi} (Atlanan: {k.metrikler.atlananSayfa ?? 0})</b></span>}
                      {k.metrikler.paragrafSayisi != null && <span>Paragraf/Cümle: <b>{k.metrikler.paragrafSayisi} / {k.metrikler.cumleSayisi}</b></span>}
                      {k.metrikler.slaytAdimSayisi != null && <span>Öğren Adımı: <b>{k.metrikler.slaytAdimSayisi}</b></span>}
                      {k.metrikler.cizimSayisi != null && <span>Canlı Çizim: <b>{k.metrikler.cizimSayisi}</b></span>}
                      {k.metrikler.cikmisEslesme != null && <span>Çıkmış Eşleşme: <b>{k.metrikler.cikmisEslesme}</b></span>}
                    </div>
                  )}
                  {k.hatali_bilgiler?.length > 0 && (
                    <div className="cd-gunluk-blok">
                      <h4>Tespit Edilen / Denetlenen Hatalar ve Eksikler</h4>
                      <ul>
                        {k.hatali_bilgiler.map((m, i) => <li key={i}>{m}</li>)}
                      </ul>
                    </div>
                  )}
                  {k.degisiklikler?.length > 0 && (
                    <div className="cd-gunluk-blok">
                      <h4>Yapılan Değişiklikler ve İyileştirmeler</h4>
                      <ul>
                        {k.degisiklikler.map((m, i) => <li key={i}>{m}</li>)}
                      </ul>
                    </div>
                  )}
                </article>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


/** KMB (Klinik Mesleki Beceri) sesli video dersleri: rayda kısa bağlantı listesi (/dersler/kmb/<beceri>) */
function KmbKarti() {
  const hazir = KMB_INDEX.beceriler.filter((b) => b.durum === 'hazir');
  if (!hazir.length) return null;
  return (
    <section className="cdl-kmb" aria-labelledby="cd-kmb-h">
      <p className="cdl-ray-bas" id="cd-kmb-h">KMB video dersler</p>
      {hazir.map((b) => (
        <a key={b.slug} href={`/dersler/kmb/${b.slug}`} className="cdl-kmb-bag" onClick={(e) => { e.preventDefault(); navigateTo(`/kmb?beceri=${b.slug}`); }}>
          <Video aria-hidden /><span><b>{b.ad}</b><small>{b.belgeKodu}</small></span>
        </a>
      ))}
    </section>
  );
}
