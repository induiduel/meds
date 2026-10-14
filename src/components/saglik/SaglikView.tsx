import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { LayoutGrid, Landmark, List, RefreshCw } from 'lucide-react';
import { parseLocation, pathFor, writeLocation, linkClick } from '../../router';
import { AtifSaglayici, DersPaneli, Kaynakca, KendiniSina, tarihTR } from './SaglikOrtak';
import { BOLUM_BILESEN, bolumKaynaklari } from './SaglikBolumler';
import { BOLUMLER, BOLUM_GRUPLARI, bolumBySlug, havuzYukle, saglikVeriYukle, type BolumId, type HavuzVeri, type SaglikVeri } from './saglikVeri';
import { GecmisCtx, GorunumCtx, type GecmisIstek, type GorunumModu } from './saglikBaglam';
import { GecmisPencere } from './SaglikGecmis';
import '../../styles/saglik.css';

/**
 * Sağlık Bakanlığı sekmesi (/saglik, /saglik/<bölüm>). Resmî halk sağlığı verileri (Sağlık Bakanlığı, TÜİK,
 * Karabük İl Sağlık Müdürlüğü, Resmî Gazete…) her sayı kaynaklı; yanında dersteki karşılığı (Öğren slaytı,
 * kazanım, sınav spotu) ve bölüm konularından çıkmış sorularla "Kendini sına".
 * Plan ve veri hattı: docs/SAGLIK_BAKANLIGI_PLANI.md. Stil: styles/saglik.css (.sbk-*), yalnız palet token'ları.
 */

/** Bölümün veri dosyasındaki "teyit edilemedi" notları (kaynakçada açılır liste) */
const dogrulanamayanlar = (b: BolumId, v: SaglikVeri): string[] => {
  if (b === 'asi') return v.asi.dogrulanamayan || [];
  if (b === 'karabuk') return v.karabuk.dogrulanamayan || [];
  if (b === 'yenidogan' || b === 'anne_kadin' || b === 'tarama') return v.anne.dogrulanamayan || [];
  if (b === 'genel') return [];
  return v.turkiye.dogrulanamayan || [];
};

/** Bölüm çizilemezse yalnız o bölüm hata gösterir (uygulamanın geneli düşmez) */
class BolumSiniri extends React.Component<{ anahtar: string; children: React.ReactNode }, { hata: string | null }> {
  state = { hata: null as string | null };
  static getDerivedStateFromError(e: unknown) { return { hata: e instanceof Error ? e.message : String(e) }; }
  componentDidUpdate(onceki: { anahtar: string }) { if (onceki.anahtar !== this.props.anahtar && this.state.hata) this.setState({ hata: null }); }
  componentDidCatch(e: unknown) { console.error('[Sağlık Bakanlığı] bölüm hatası', e); }
  render() {
    if (this.state.hata) return <div className="sbk-bos" role="alert">Bu bölüm şu an gösterilemiyor. Sayfayı yenileyip yeniden dene. <small>({this.state.hata.slice(0, 120)})</small></div>;
    return this.props.children;
  }
}

const slugOku = () => {
  const r = parseLocation();
  return r.route === 'health_ministry' ? r.param : undefined;
};
/** Alt sayfa (?sayfa=…), ör. /saglik/karabuk?sayfa=ilceler */
const altOku = () => { try { return new URLSearchParams(window.location.search).get('sayfa') || undefined; } catch { return undefined; } };

export const SaglikView: React.FC = () => {
  const [bolum, setBolum] = useState<BolumId>(() => bolumBySlug(slugOku()).id);
  const [alt, setAlt] = useState<string | undefined>(altOku);
  const [veri, setVeri] = useState<SaglikVeri | null>(null);
  const [hata, setHata] = useState(false);
  const [deneme, setDeneme] = useState(0);
  const navRef = useRef<HTMLElement>(null);
  // Görünüm: kart (görsel) ya da madde madde — tarayıcıda hatırlanır (yalnız kişisel tercih)
  const [mod, setModHam] = useState<GorunumModu>(() => {
    try { return localStorage.getItem('medsoru_saglik_gorunum') === 'madde' ? 'madde' : 'kart'; } catch { return 'kart'; }
  });
  const setMod = useCallback((m: GorunumModu) => {
    setModHam(m);
    try { localStorage.setItem('medsoru_saglik_gorunum', m); } catch { /* özel pencere */ }
  }, []);
  const gorunum = useMemo(() => ({ mod, setMod }), [mod, setMod]);
  const [gecmis, setGecmis] = useState<GecmisIstek | null>(null);

  useEffect(() => {
    let iptal = false;
    setHata(false);
    saglikVeriYukle().then((v) => { if (!iptal) setVeri(v); }).catch(() => { if (!iptal) setHata(true); });
    return () => { iptal = true; };
  }, [deneme]);

  // Geri/ileri: adres çubuğundaki bölüm
  useEffect(() => {
    const f = () => { setBolum(bolumBySlug(slugOku()).id); setAlt(altOku()); };
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);

  // Etkin sekme şeritte görünür kalsın
  useEffect(() => {
    const el = navRef.current?.querySelector<HTMLElement>('[aria-current="page"]');
    el?.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
  }, [bolum]);

  const git = useCallback((id: BolumId) => {
    const b = BOLUMLER.find((x) => x.id === id) || BOLUMLER[0];
    setBolum(b.id);
    setAlt(undefined);
    setGecmis(null);
    // Aynı bölümün alt sayfasındayken (?sayfa=) bölüm adına dokunmak özet sayfasına döner
    if (window.location.search && window.location.pathname === pathFor('health_ministry', b.slug || undefined)) {
      try { window.history.pushState({ route: 'health_ministry', param: b.slug }, '', window.location.pathname); } catch { /* geçmiş yazılamadı */ }
    } else writeLocation('health_ministry', b.slug || undefined);
    window.scrollTo({ top: 0 });
  }, []);

  const altGit = useCallback((id: string) => {
    setAlt(id === 'ozet' ? undefined : id);
    setGecmis(null);
    const yol = `${window.location.pathname}${id === 'ozet' ? '' : `?sayfa=${encodeURIComponent(id)}`}`;
    if (window.location.pathname + window.location.search !== yol) {
      try { window.history.pushState({ route: 'health_ministry', param: slugOku() }, '', yol); } catch { /* geçmiş yazılamadı */ }
    }
    document.querySelector('.sbk-bolum-h')?.scrollIntoView({ block: 'start' });
  }, []);

  // Bilgi havuzu büyük: yalnız havuz bölümü açılınca yüklenir ve kaynakçası için veriye eklenir
  const [havuz, setHavuz] = useState<HavuzVeri | null>(null);
  useEffect(() => {
    if (bolum !== 'havuz' || havuz) return;
    let iptal = false;
    havuzYukle().then((x) => { if (!iptal) setHavuz(x); }).catch(() => { /* bölüm kendi hatasını gösterir */ });
    return () => { iptal = true; };
  }, [bolum, havuz]);
  const veriH = useMemo(() => (veri && havuz ? { ...veri, havuz } : veri), [veri, havuz]);

  const tanim = BOLUMLER.find((b) => b.id === bolum) || BOLUMLER[0];
  const bag = veri?.baglantilar.bolumler[bolum];
  const kaynakIds = useMemo(() => (veriH ? bolumKaynaklari(bolum, veriH, alt) : []), [veriH, bolum, alt]);
  const Bilesen = BOLUM_BILESEN[bolum];
  const TanimIc = tanim.icon;

  useEffect(() => {
    document.title = `${bolum === 'genel' ? 'Sağlık Bakanlığı' : `${tanim.ad} · Sağlık Bakanlığı`} · MeDSor`;
  }, [bolum, tanim.ad]);

  return (
    <div className="sbk">
      <header className="sbk-ust">
        <span className="sbk-amblem" aria-hidden><Landmark /></span>
        <div className="sbk-ust-m">
          <p className="sbk-ust-e">T.C. Sağlık Bakanlığı · TÜİK · Karabük İl Sağlık Müdürlüğü</p>
          <h1>Sağlık Bakanlığı</h1>
          <p className="sbk-ust-a">Resmî halk sağlığı verileri; her biri dersteki slaytına, kazanımına ve çıkmış sorularına bağlı.</p>
        </div>
        <div className="sbk-ust-sag">
          <div className="sbk-seg" role="radiogroup" aria-label="Görünüm">
            <button type="button" role="radio" aria-checked={mod === 'kart'} className={mod === 'kart' ? 'is-sec' : ''} onClick={() => setMod('kart')}><LayoutGrid aria-hidden /> Kart</button>
            <button type="button" role="radio" aria-checked={mod === 'madde'} className={mod === 'madde' ? 'is-sec' : ''} onClick={() => setMod('madde')}><List aria-hidden /> Madde madde</button>
          </div>
          {veri?.guncelleme && <span className="sbk-ust-g">Veriler {tarihTR(veri.guncelleme)} tarihinde resmî kaynaklardan derlendi</span>}
        </div>
      </header>

      <nav ref={navRef} className="sbk-nav" aria-label="Sağlık Bakanlığı bölümleri">
        {BOLUM_GRUPLARI.map((g) => (
          <div key={g.id} className="sbk-nav-grup" role="group" aria-label={g.ad}>
            <span className="sbk-nav-gad">{g.ad}</span>
            <div className="sbk-nav-ogeler">
              {BOLUMLER.filter((b) => b.grup === g.id).map((b) => {
                const Ic = b.icon;
                const yol = `${pathFor('health_ministry')}${b.slug ? `/${b.slug}` : ''}`;
                return (
                  <a key={b.id} href={yol} aria-current={b.id === bolum ? 'page' : undefined} onClick={linkClick(() => git(b.id))}>
                    <Ic aria-hidden /><span>{b.kisa}</span>
                  </a>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {hata ? (
        <div className="sbk-durum" role="alert">
          <p>Veriler yüklenemedi. Bağlantını kontrol edip yeniden dene.</p>
          <button type="button" className="sbk-btn is-dolu" onClick={() => setDeneme((n) => n + 1)}><RefreshCw aria-hidden /> Yeniden dene</button>
        </div>
      ) : !veri ? (
        <div className="sbk-durum is-yuk" aria-busy="true" aria-label="Yükleniyor">
          <span className="ui-skel" style={{ height: 64 }} />
          <div className="sbk-kpi-g">{[0, 1, 2, 3].map((i) => <span key={i} className="ui-skel" style={{ height: 96 }} />)}</div>
          <span className="ui-skel" style={{ height: 280 }} />
        </div>
      ) : (
        <GorunumCtx.Provider value={gorunum}>
        <GecmisCtx.Provider value={setGecmis}>
        <AtifSaglayici ids={kaynakIds} kaynaklar={veri.kaynaklar}>
          <GecmisPencere istek={gecmis} onClose={() => setGecmis(null)} />
          {bolum !== 'genel' && (
            <div className="sbk-bolum-h">
              <span className="sbk-bolum-ic" aria-hidden><TanimIc /></span>
              <div>
                <h2>{tanim.ad}</h2>
                <p>{tanim.aciklama}</p>
              </div>
            </div>
          )}
          <div className={`sbk-izgara ${bag ? 'has-yan' : ''}`}>
            <div className="sbk-icerik">
              <BolumSiniri anahtar={bolum}><Bilesen v={veriH || veri} bag={bag} git={git} alt={alt} altGit={altGit} /></BolumSiniri>
              {bag && bag.havuz > 0 && bolum !== 'genel' && <KendiniSina bolum={bolum} baslik={tanim.ad} toplam={bag.soru_sayisi} />}
              <Kaynakca dogrulanamayan={dogrulanamayanlar(bolum, veri)} />
            </div>
            {bag && (
              <aside className="sbk-yan" aria-label="Derste ve sınavda">
                <DersPaneli b={bag} onSina={() => document.getElementById('sbk-sina')?.scrollIntoView({ behavior: 'smooth', block: 'start' })} />
              </aside>
            )}
          </div>
        </AtifSaglayici>
        </GecmisCtx.Provider>
        </GorunumCtx.Provider>
      )}
    </div>
  );
};
