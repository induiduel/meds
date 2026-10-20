/**
 * Kurul kampı (/kamp): hocaların derste verdiği tüyolar + ders bilgi deposundan gece üretilen hızlı tekrar kampları.
 *   /kamp?kurul=N          → kurulun kampları (kart); varsayılan aktif kurul (services/kurulTakvimi)
 *   /kamp/<kurul>/<brans>  → tek kamp: Sesli anlatım (puan sırası, EMA klipleri) · Kalıp kartları · Deneme
 * Veri: data/kamp/k<N>/<brans>.json (kampVeri.ts). Görünüm dili TBG Sınav Kampı'ndan (styles/genetik-kamp.css .tk-*),
 * kampa özel ekler styles/kamp.css (.km-*). Tüyo önerisi: TuyoFormu → POST /api/kamp/tuyo-oner.
 */
import { icKonum, icUrl } from '../../siteHaritasi';
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowLeft, Check, ChevronLeft, ChevronRight, Eye, EyeOff, Lightbulb, Pause, Play, RotateCcw, Search, Shuffle,
  SkipForward, Table2, Tent, Volume2, X, AudioLines, CircleCheck,
} from 'lucide-react';
import { loadDeckCatalog } from '../../data/deckStore';
import { tekrarTamamlandi, useKonuSayaci, useSoruSayaci } from '../../services/calismaTakip';
import { KonuDugmeleri } from '../takip/KonuTakip';
import {
  bildimDegistir, cevapSil, cevapla, dinlendi, kalipSatirId, kampAnahtar, kampOzeti, useKampKaydi, useKampVeri, kampKaydi,
} from './kampIlerleme';
import { linkClick, navigateTo } from '../../router';
import { KURULLAR, aktifKurul } from '../../services/kurulTakvimi';
import { kurulAdi } from '../../services/kurulPencere';
import {
  bransAdi, bransKisa, kampSesUrl, kaynakHedef, kaynakYaz, kurulKampYollari, type Kamp, type KampSoru,
} from './kampVeri';
import { TuyoFormu } from './TuyoFormu';
import '../../styles/genetik-kamp.css';
import '../../styles/kamp.css';

type Sekme = 'anlatim' | 'kalip' | 'deneme';

/** **kalın** işaretlerini <b>'ye çevirir */
function Zengin({ t }: { t: string }) {
  return <>{String(t || '').split(/(\*\*[^*]+\*\*)/g).map((p, i) => (p.startsWith('**') && p.endsWith('**') ? <b key={i}>{p.slice(2, -2)}</b> : <React.Fragment key={i}>{p}</React.Fragment>))}</>;
}

function adresOku(): { kurul: number; brans?: string } {
  const segs = icKonum().pathname.split('/').filter(Boolean);
  const q = Number(new URLSearchParams(icKonum().search).get('kurul'));
  const yol = Number(segs[1]);
  const kurul = [yol, q].find((n) => Number.isInteger(n) && n >= 1 && n <= 6) || aktifKurul().kurul;
  const brans = segs[2] && /^[a-z0-9]{2,30}$/.test(segs[2]) ? segs[2] : undefined;
  return { kurul, brans };
}

const Git: React.FC<{ url: string; className?: string; children: React.ReactNode }> = ({ url, className, children }) => (
  <a href={url} className={className} onClick={linkClick(() => navigateTo(url))}>{children}</a>
);

/** Öğren kataloğu tembel yüklenir; yüklenince kaynak bağlantıları desteye döner */
let katalogHazir = false;
function useKatalog() {
  const [, setT] = useState(0);
  useEffect(() => {
    if (katalogHazir) return;
    let iptal = false;
    loadDeckCatalog().then(() => { katalogHazir = true; if (!iptal) setT((t) => t + 1); }).catch(() => {});
    return () => { iptal = true; };
  }, []);
}

/** Kaynak etiketi: ders defterinde varsa dersin Öğren destesine (yoksa /k/<ders_id>) bağlantı */
const KaynakBag: React.FC<{ k: string; className?: string }> = ({ k, className }) => {
  useKatalog();
  const h = kaynakHedef(k);
  if (!h) return <span className={className}>{kaynakYaz(k)}</span>;
  return h.ic ? <Git url={h.url} className={className}>{kaynakYaz(k)}</Git> : <a href={h.url} className={className}>{kaynakYaz(k)}</a>;
};

const Kaynaklar: React.FC<{ k?: string[] | string }> = ({ k }) => {
  const L = (Array.isArray(k) ? k : k ? [k] : []).filter(Boolean);
  if (!L.length) return null;
  return <p className="km-kaynak">{L.map((x) => <KaynakBag key={x} k={x} />)}</p>;
};

export default function KampView() {
  const [adres, setAdres] = useState(adresOku);
  useEffect(() => {
    const f = () => setAdres(adresOku());
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  return adres.brans ? <KampSayfasi kurul={adres.kurul} brans={adres.brans} /> : <KampListesi kurul={adres.kurul} />;
}

/* ——— liste ——— */
function KampListesi({ kurul }: { kurul: number }) {
  const [kamplar, setKamplar] = useState<Kamp[] | null>(null);
  const [form, setForm] = useState(false);
  const kurulBilgi = KURULLAR.find((k) => k.kurul === kurul);
  const ilerleme = useKampVeri();
  useEffect(() => { document.title = 'Kurul kampı · MeDSor'; }, []);
  useEffect(() => {
    let iptal = false;
    setKamplar(null);
    Promise.all(kurulKampYollari(kurul).map((x) => x.yukle().catch(() => null)))
      .then((L) => { if (!iptal) setKamplar(L.filter((x): x is Kamp => !!x).sort((a, b) => a.baslik.localeCompare(b.baslik, 'tr'))); });
    return () => { iptal = true; };
  }, [kurul]);

  return (
    <div className="tk km">
      <header className="tk-bas">
        <span className="tk-ic" aria-hidden><Tent /></span>
        <div className="tk-bas-t">
          <span className="tk-ust">Kurul {kurul}{kurulBilgi ? ` · ${kurulAdi(kurulBilgi)}` : ''}</span>
          <h1>Kurul kampı</h1>
          <p>Hocalarınızın derste “bunu sorarım” dediği yerler ve ders notlarındaki en önemli bilgiler: sesli anlatım, kalıp kartları ve deneme.</p>
        </div>
        <div className="tk-bas-arac">
          <button type="button" className="tk-btn" onClick={() => setForm((f) => !f)} aria-expanded={form}><Lightbulb aria-hidden /> Hocanın tüyosunu ekle</button>
        </div>
      </header>

      <nav className="km-kurullar" aria-label="Kurul seç">
        {KURULLAR.map((k) => (
          <Git key={k.kurul} url={`/kamp?kurul=${k.kurul}`} className={`km-kurul${k.kurul === kurul ? ' is-on' : ''}`}>Kurul {k.kurul}</Git>
        ))}
      </nav>

      {form && <TuyoFormu kurul={kurul} onKapat={() => setForm(false)} />}

      {kamplar === null ? <p className="km-bilgi">Yükleniyor…</p> : kamplar.length === 0 ? (
        <div className="km-bos">
          <Tent aria-hidden />
          <b>Bu kurulun kampı henüz yok</b>
          <p>Hocalarınızın derste verdiği ipuçları onaylandıkça bu kurulun kampları burada oluşur.</p>
          {!form && <button type="button" className="tk-btn tk-btn-ana" onClick={() => setForm(true)}><Lightbulb aria-hidden /> Hocanın tüyosunu ekle</button>}
        </div>
      ) : (
        <ul className="km-kartlar">
          {kamplar.map((k) => { const o = kampOzeti(k, kampKaydi(kampAnahtar(k.kurul, k.brans), ilerleme)); return (
            <li key={k.brans}>
              <Git url={`/kamp/${k.kurul}/${k.brans}`} className="km-kart">
                <span className="tk-ust">{bransKisa(k.brans)}</span>
                <b>{k.baslik}</b>
                {k.kisa && <span className="km-kart-kisa">{k.kisa}</span>}
                <span className="km-kart-say">{k.anlatim.length} anlatım · {k.kalipler.length} kalıp · {k.deneme.length} soru{k.tuyolar.length ? ` · ${k.tuyolar.length} hoca vurgusu` : ''}</span>
                {o.yapilan > 0 && (
                  <span className="km-ilerleme" aria-label={`İlerleme yüzde ${o.yuzde}`}>
                    <span className="km-ilerleme-bar"><span style={{ width: `${o.yuzde}%` }} /></span>
                    <span className="km-ilerleme-t"><span className="tk-mono">%{o.yuzde}</span> · {o.anlatim}/{k.anlatim.length} dinlendi · {o.cevaplanan}/{k.deneme.length} soru{o.cevaplanan ? ` (${o.dogru} doğru)` : ''}</span>
                  </span>
                )}
              </Git>
            </li>
          ); })}
        </ul>
      )}
    </div>
  );
}

/* ——— tek kamp ——— */
function KampSayfasi({ kurul, brans }: { kurul: number; brans: string }) {
  const [kamp, setKamp] = useState<Kamp | null | undefined>(undefined);
  const [sekme, setSekme] = useState<Sekme>('anlatim');
  const [form, setForm] = useState(false);
  const audio = useRef<HTMLAudioElement | null>(null);
  const zincir = useRef<(() => void) | null>(null);
  const [calan, setCalan] = useState<{ anahtar: string; oynuyor: boolean } | null>(null);
  const ka = kampAnahtar(kurul, brans);
  useKonuSayaci('kamp', kamp ? ka : null, !!calan?.oynuyor);
  const kayit = useKampKaydi(ka);
  const ozet = kamp ? kampOzeti(kamp, kayit) : null;
  useEffect(() => { if (ozet?.tamam) tekrarTamamlandi('kamp', ka); }, [ozet?.tamam, ka]);

  useEffect(() => {
    let iptal = false;
    setKamp(undefined);
    const y = kurulKampYollari(kurul).find((x) => x.brans === brans);
    if (!y) { setKamp(null); return; }
    y.yukle().then((k) => { if (!iptal) setKamp(k); }).catch(() => { if (!iptal) setKamp(null); });
    return () => { iptal = true; };
  }, [kurul, brans]);
  useEffect(() => { document.title = `${kamp?.baslik || 'Kurul kampı'} · MeDSor`; }, [kamp]);

  const durdur = useCallback(() => {
    zincir.current = null;
    const a = audio.current;
    if (a) { a.onended = null; a.pause(); }
    setCalan(null);
  }, []);
  useEffect(() => () => durdur(), [durdur]);

  const cal = useCallback((anahtar: string, bitince?: () => void) => {
    if (!kamp) return;
    const url = kampSesUrl(kamp, anahtar);
    durdur();
    if (!url) { bitince?.(); return; }
    const a = audio.current || new Audio();
    audio.current = a;
    a.src = url;
    zincir.current = bitince || null;
    a.onended = () => { setCalan(null); const z = zincir.current; zincir.current = null; z?.(); };
    a.onerror = () => setCalan(null);
    setCalan({ anahtar, oynuyor: true });
    a.play().catch(() => setCalan(null));
  }, [durdur, kamp]);

  const duraklat = useCallback(() => {
    const a = audio.current;
    if (!a || !calan) return;
    if (calan.oynuyor) { a.pause(); setCalan({ ...calan, oynuyor: false }); }
    else { a.play().catch(() => {}); setCalan({ ...calan, oynuyor: true }); }
  }, [calan]);

  const geri = `/kamp?kurul=${kurul}`;
  if (kamp === undefined) return <div className="tk km"><p className="km-bilgi">Yükleniyor…</p></div>;
  if (kamp === null) {
    return (
      <div className="tk km">
        <Git url={geri} className="km-geri"><ArrowLeft aria-hidden /> Kurul {kurul} kampları</Git>
        <div className="km-bos">
          <Tent aria-hidden />
          <b>{bransAdi(brans)} kampı henüz hazır değil</b>
          <p>Hocalarınızın derste verdiği ipuçları onaylandıkça bu kurulun kampları burada oluşur.</p>
          {form ? <TuyoFormu kurul={kurul} brans={brans} onKapat={() => setForm(false)} />
            : <button type="button" className="tk-btn tk-btn-ana" onClick={() => setForm(true)}><Lightbulb aria-hidden /> Hocanın tüyosunu ekle</button>}
        </div>
      </div>
    );
  }

  return (
    <div className="tk km">
      <Git url={geri} className="km-geri"><ArrowLeft aria-hidden /> Kurul {kurul} kampları</Git>
      <header className="tk-bas">
        <span className="tk-ic" aria-hidden><Tent /></span>
        <div className="tk-bas-t">
          <span className="tk-ust">Kurul {kurul} · {bransAdi(kamp.brans)}</span>
          <h1>{kamp.baslik}</h1>
          {kamp.kisa && <p>{kamp.kisa}</p>}
        </div>
        <div className="tk-bas-arac">
          <KonuDugmeleri modul="kamp" konu={ka} ad={kamp.baslik} turetilen={!!ozet?.tamam} />
          <button type="button" className="tk-btn" onClick={() => setForm((f) => !f)} aria-expanded={form}><Lightbulb aria-hidden /> Hocanın tüyosunu ekle</button>
        </div>
      </header>
      {ozet && ozet.yapilan > 0 && (
        <p className="km-ozet"><span className="tk-mono">%{ozet.yuzde}</span> tamam · {ozet.anlatim}/{kamp.anlatim.length} madde dinlendi · {ozet.bildim}/{ozet.satirToplam} kalıp bildim · {ozet.cevaplanan}/{kamp.deneme.length} soru ({ozet.dogru} doğru, {ozet.yanlis} yanlış)</p>
      )}

      {form && <TuyoFormu kurul={kurul} brans={kamp.brans} onKapat={() => setForm(false)} />}

      <nav className="tk-sekme" role="tablist" aria-label="Bölümler">
        {([['anlatim', 'Sesli anlatım', AudioLines], ['kalip', 'Kalıp kartları', Table2], ['deneme', 'Deneme', Shuffle]] as const).map(([id, ad, Ic]) => (
          <button key={id} type="button" role="tab" aria-selected={sekme === id} className={sekme === id ? 'is-on' : ''} onClick={() => { durdur(); setSekme(id); }}>
            <Ic aria-hidden /> {ad}
          </button>
        ))}
      </nav>

      {sekme === 'anlatim' && <Anlatim kamp={kamp} ka={ka} dinlenen={kayit.dinlenen} cal={cal} calan={calan} duraklat={duraklat} durdur={durdur} />}
      {sekme === 'kalip' && <Kaliplar kamp={kamp} ka={ka} bildim={kayit.bildim} />}
      {sekme === 'deneme' && <Deneme kamp={kamp} ka={ka} cevap={kayit.cevap} cal={cal} durdur={durdur} />}
    </div>
  );
}

/* ——— sesli anlatım ——— */
function Anlatim({ kamp, ka, dinlenen, cal, calan, duraklat, durdur }: {
  kamp: Kamp; ka: string; dinlenen: Record<string, number>; cal: (a: string, b?: () => void) => void; calan: { anahtar: string; oynuyor: boolean } | null; duraklat: () => void; durdur: () => void;
}) {
  const maddeler = useMemo(() => [...kamp.anlatim].sort((a, b) => b.puan - a.puan), [kamp]);
  const tuyo = useMemo(() => new Map(kamp.tuyolar.map((t) => [t.id, t.metin])), [kamp]);
  const [i, setI] = useState(0);
  const refs = useRef<(HTMLElement | null)[]>([]);
  const n = maddeler[i];

  const oynat = useCallback((j: number) => {
    const m = maddeler[j];
    if (!m) return;
    setI(j);
    refs.current[j]?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    cal(m.id, () => { dinlendi(ka, m.id); if (j + 1 < maddeler.length) oynatRef.current(j + 1); });
  }, [cal, maddeler, ka]);
  const oynatRef = useRef(oynat);
  oynatRef.current = oynat;

  if (!n) return <p className="km-bilgi">Bu kampta anlatım maddesi yok.</p>;
  const buCalan = calan && maddeler.some((m) => m.id === calan.anahtar);
  const sesVar = !!kamp.ses?.[n.id];

  return (
    <div className="km-anlatim">
      <div className="tk-oynat km-oynat">
        {buCalan ? (
          <button type="button" className="tk-btn tk-btn-ana" onClick={duraklat}>{calan!.oynuyor ? <Pause aria-hidden /> : <Play aria-hidden />}{calan!.oynuyor ? 'Duraklat' : 'Devam et'}</button>
        ) : (
          <button type="button" className="tk-btn tk-btn-ana" onClick={() => oynat(i)} disabled={!sesVar}><Play aria-hidden /> {i === 0 ? 'Baştan dinle' : 'Buradan dinle'}</button>
        )}
        <button type="button" className="tk-btn" onClick={() => (buCalan ? oynat(i + 1) : setI(i + 1))} disabled={i >= maddeler.length - 1}><SkipForward aria-hidden /> Sonraki</button>
        {buCalan && <button type="button" className="tk-btn" onClick={durdur}><X aria-hidden /> Durdur</button>}
        <span className="km-sira tk-mono">{i + 1}/{maddeler.length}</span>
      </div>
      <ol className="km-maddeler">
        {maddeler.map((m, j) => (
          <li key={m.id} ref={(el) => { refs.current[j] = el; }}>
            <article className={`tk-kart km-madde${j === i ? ' is-on' : ''}`}>
              <div className="tk-kart-ust">
                <span className="tk-ust">{j + 1}. madde</span>
                {dinlenen[m.id] ? <span className="km-dinlendi"><CircleCheck aria-hidden /> Dinlendi</span> : null}
                {m.tuyo && <span className="km-rozet"><Lightbulb aria-hidden /> Hocanızın vurgusu</span>}
              </div>
              <h2>
                <button type="button" className="km-madde-bas" onClick={() => (kamp.ses?.[m.id] ? oynat(j) : setI(j))} title="Bu maddeyi dinle">
                  {calan?.anahtar === m.id && calan.oynuyor ? <Volume2 aria-hidden /> : null}{m.baslik}
                </button>
              </h2>
              {m.tuyo && tuyo.get(m.tuyo) && <p className="km-tuyo">“{tuyo.get(m.tuyo)}”</p>}
              <p className="km-metin"><Zengin t={m.metin} /></p>
              <Kaynaklar k={m.k} />
            </article>
          </li>
        ))}
      </ol>
    </div>
  );
}

/* ——— kalıp kartları ——— */
function Kaliplar({ kamp, ka, bildim }: { kamp: Kamp; ka: string; bildim: Record<string, number> }) {
  const [ara, setAra] = useState('');
  const [gizle, setGizle] = useState(false);
  const [yalnizH, setYalnizH] = useState(false);
  const [acik, setAcik] = useState<Record<string, boolean>>({});
  const q = ara.trim().toLocaleLowerCase('tr');
  if (!kamp.kalipler.length) return <p className="km-bilgi">Bu kampta kalıp kartı yok.</p>;
  let gorunen = 0;
  return (
    <div className="tk-kalip">
      <div className="tk-kalip-arac">
        <label className="tk-ara"><Search aria-hidden /><input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Kalıplarda ara" /></label>
        <button type="button" className={`tk-btn${yalnizH ? ' is-on' : ''}`} aria-pressed={yalnizH} onClick={() => setYalnizH((h) => !h)}>
          <Lightbulb aria-hidden /> Yalnız sorulanlar
        </button>
        <button type="button" className={`tk-btn${gizle ? ' is-on' : ''}`} aria-pressed={gizle} onClick={() => { setGizle((g) => !g); setAcik({}); }}>
          {gizle ? <Eye aria-hidden /> : <EyeOff aria-hidden />}{gizle ? 'Cevapları göster' : 'Cevapları gizle, kendini sına'}
        </button>
      </div>
      {kamp.kalipler.map((k) => {
        const R = k.satir.map((r, i) => ({ r, id: kalipSatirId(k.id, i) }))
          .filter(({ r }) => (!yalnizH || r.h) && (!q || `${r.s} ${r.t}`.toLocaleLowerCase('tr').includes(q)));
        if (!R.length) return null;
        gorunen += 1;
        return (
          <section key={k.id} className="tk-kalip-k">
            <header><h3>{k.baslik}</h3><span>{k.soru}</span></header>
            <div className="tk-tablo" role="table">
              <div className="tk-tablo-s tk-tablo-bas" role="row"><span role="columnheader">{k.sutun[0]}</span><span role="columnheader">{k.sutun[1]}</span></div>
              {R.map(({ r, id }) => {
                const goster = !gizle || acik[id];
                const bil = !!bildim[id];
                return (
                  <div key={id} className={`tk-tablo-s${bil ? ' km-bildim' : ''}`} role="row">
                    <span role="cell">{r.s}{r.h ? <span className="tk-cik" title="Çıkmışta ya da hoca vurgusunda geçiyor">!</span> : null}</span>
                    <span role="cell">
                      {goster ? <><b>{r.t}</b>{r.k && <KaynakBag k={r.k} className="km-kaynak-k" />}
                        <button type="button" className={`km-bildim-btn${bil ? ' is-on' : ''}`} aria-pressed={bil} onClick={() => bildimDegistir(ka, id)}
                          title={bil ? 'Bildim işaretini kaldır' : 'Bunu bildim'}><Check aria-hidden /> {bil ? 'Bildim' : 'Bildim mi?'}</button></> : (
                        <button type="button" className="tk-gizli" onClick={() => setAcik((a) => ({ ...a, [id]: true }))}>Göster</button>
                      )}
                    </span>
                  </div>
                );
              })}
            </div>
          </section>
        );
      })}
      {gorunen === 0 && <p className="km-bilgi">Aramaya uyan satır yok.</p>}
    </div>
  );
}

/* ——— deneme ——— */
function Deneme({ kamp, ka, cevap: kayitli, cal, durdur }: {
  kamp: Kamp; ka: string; cevap: Record<string, { s: string; d: boolean }>; cal: (a: string, b?: () => void) => void; durdur: () => void;
}) {
  /** "Yanlışlarımı tekrar çöz" turunda yalnız bu sorular gösterilir */
  const [tur, setTur] = useState<string[] | null>(null);
  const [i, setI] = useState(0);
  const soruSay = useSoruSayaci('kamp', ka);
  const tum = kamp.deneme;
  const set = tur ? tum.filter((x) => tur.includes(x.id)) : tum;
  const cevap = useMemo(() => Object.fromEntries(Object.entries(kayitli).map(([k, v]) => [k, v.s])), [kayitli]);
  if (!tum.length) return <p className="km-bilgi">Bu kampta deneme sorusu yok.</p>;
  if (!set.length) return <p className="km-bilgi">Tekrar edilecek soru kalmadı.</p>;
  const s = set[Math.min(i, set.length - 1)];
  const cevaplanan = tum.filter((x) => cevap[x.id]);
  const dogru = cevaplanan.filter((x) => cevap[x.id] === x.dogru).length;
  const yanlislar = cevaplanan.filter((x) => cevap[x.id] !== x.dogru).map((x) => x.id);
  const bitti = set.every((x) => cevap[x.id]);
  const git = (j: number) => { durdur(); setI(j); };
  const sifirla = () => { durdur(); cevapSil(ka, tum.map((x) => x.id)); setTur(null); setI(0); };
  const yanlisTekrar = () => { durdur(); cevapSil(ka, yanlislar); setTur(yanlislar); setI(0); };
  return (
    <div className="tk-deneme">
      <div className="tk-deneme-ust">
        <div className="tk-nokta" role="tablist" aria-label="Sorular">
          {set.map((x, j) => (
            <button key={x.id} type="button" aria-label={`${j + 1}. soru`} className={`${j === i ? 'is-on' : ''}${cevap[x.id] ? (cevap[x.id] === x.dogru ? ' is-dogru' : ' is-yanlis') : ''}`} onClick={() => git(j)}>{j + 1}</button>
          ))}
        </div>
        {cevaplanan.length > 0 && <span className="tk-skor"><b>{dogru}</b> doğru · <b>{cevaplanan.length - dogru}</b> yanlış · {cevaplanan.length}/{tum.length}</span>}
      </div>
      {(cevaplanan.length > 0 || tur) && (
        <div className="km-deneme-arac">
          {tur && <span className="km-tur">Yanlışları tekrar · {set.length} soru</span>}
          {yanlislar.length > 0 && <button type="button" className="tk-btn" onClick={yanlisTekrar}><RotateCcw aria-hidden /> Yanlışlarımı tekrar çöz ({yanlislar.length})</button>}
          {tur && <button type="button" className="tk-btn" onClick={() => { durdur(); setTur(null); setI(0); }}>Tüm sorulara dön</button>}
          {cevaplanan.length > 0 && <button type="button" className="tk-btn" onClick={sifirla}><X aria-hidden /> Denemeyi sıfırla</button>}
        </div>
      )}
      <DenemeSoru key={s.id} s={s} no={tum.indexOf(s) + 1} secim={cevap[s.id]} sesVar={(a) => !!kamp.ses?.[a]} tuyoVar={!!s.tuyo}
        onSec={(h) => { cevapla(ka, s.id, { s: h, d: h === s.dogru }); soruSay(s.id); cal(`${s.id}-${h.toLowerCase()}`); }}
        onOku={() => cal(s.id)} onTekrar={() => { durdur(); cevapSil(ka, [s.id]); }} />
      <div className="tk-gezin">
        <button type="button" className="tk-btn" onClick={() => git(i - 1)} disabled={i === 0}><ChevronLeft aria-hidden /> Önceki</button>
        {i < set.length - 1 ? <button type="button" className="tk-btn tk-btn-ana" onClick={() => git(i + 1)}>Sonraki <ChevronRight aria-hidden /></button>
          : bitti ? <button type="button" className="tk-btn tk-btn-ana" onClick={sifirla}><RotateCcw aria-hidden /> Baştan çöz</button>
            : <button type="button" className="tk-btn" disabled>Son soru</button>}
      </div>
    </div>
  );
}

function DenemeSoru({ s, no, secim, sesVar, tuyoVar, onSec, onOku, onTekrar }: {
  s: KampSoru; no: number; secim?: string; sesVar: (a: string) => boolean; tuyoVar: boolean; onSec: (h: string) => void; onOku: () => void; onTekrar: () => void;
}) {
  const bitti = !!secim;
  const harfler = Object.keys(s.secenekler).sort();
  return (
    <section className="tk-soru">
      <div className="tk-soru-ust">
        <span className="tk-etiket">{tuyoVar ? 'Hocanızın vurgusundan' : 'Deneme sorusu'}</span>
        <span className="tk-soru-arac">
          {sesVar(s.id) && <button type="button" className="tk-metin-btn" onClick={onOku} title="Soruyu sesli oku"><Volume2 aria-hidden /></button>}
          {bitti && <button type="button" className="tk-metin-btn" onClick={onTekrar} title="Yeniden çöz"><RotateCcw aria-hidden /></button>}
        </span>
      </div>
      <p className="tk-kok"><span className="tk-mono">{no}.</span> {s.kok}</p>
      <ul className="tk-siklar">
        {harfler.map((h) => {
          const durum = !bitti ? '' : h === s.dogru ? ' is-dogru' : h === secim ? ' is-yanlis' : ' is-sonuk';
          return (
            <li key={h}>
              <button type="button" className={`tk-sik${durum}`} disabled={bitti} onClick={() => onSec(h)}>
                <span className="tk-harf">{h}</span><span>{s.secenekler[h]}</span>
                {bitti && h === s.dogru && <Check aria-hidden className="tk-sik-ic" />}
                {bitti && h === secim && h !== s.dogru && <X aria-hidden className="tk-sik-ic" />}
              </button>
            </li>
          );
        })}
      </ul>
      {bitti && (
        <>
          <p className={`tk-geri${secim === s.dogru ? ' is-dogru' : ' is-yanlis'}`}>
            <b>{secim === s.dogru ? 'Doğru. ' : `Yanlış, doğrusu ${s.dogru}. `}</b><Zengin t={s.aciklama[secim!] || ''} />
          </p>
          {secim !== s.dogru && s.aciklama[s.dogru] && <p className="tk-geri is-dogru"><b>{s.dogru}) </b><Zengin t={s.aciklama[s.dogru]} /></p>}
          <Kaynaklar k={s.k} />
        </>
      )}
    </section>
  );
}
