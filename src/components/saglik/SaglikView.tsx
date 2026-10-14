import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Landmark, RefreshCw } from 'lucide-react';
import { parseLocation, pathFor, writeLocation, linkClick } from '../../router';
import { AtifSaglayici, DersPaneli, Kaynakca, KendiniSina, tarihTR } from './SaglikOrtak';
import { BOLUM_BILESEN, bolumKaynaklari } from './SaglikBolumler';
import { BOLUMLER, bolumBySlug, saglikVeriYukle, type BolumId, type SaglikVeri } from './saglikVeri';
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

const slugOku = () => {
  const r = parseLocation();
  return r.route === 'health_ministry' ? r.param : undefined;
};

export const SaglikView: React.FC = () => {
  const [bolum, setBolum] = useState<BolumId>(() => bolumBySlug(slugOku()).id);
  const [veri, setVeri] = useState<SaglikVeri | null>(null);
  const [hata, setHata] = useState(false);
  const [deneme, setDeneme] = useState(0);
  const navRef = useRef<HTMLElement>(null);

  useEffect(() => {
    let iptal = false;
    setHata(false);
    saglikVeriYukle().then((v) => { if (!iptal) setVeri(v); }).catch(() => { if (!iptal) setHata(true); });
    return () => { iptal = true; };
  }, [deneme]);

  // Geri/ileri: adres çubuğundaki bölüm
  useEffect(() => {
    const f = () => setBolum(bolumBySlug(slugOku()).id);
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
    writeLocation('health_ministry', b.slug || undefined);
    window.scrollTo({ top: 0 });
  }, []);

  const tanim = BOLUMLER.find((b) => b.id === bolum) || BOLUMLER[0];
  const bag = veri?.baglantilar.bolumler[bolum];
  const kaynakIds = useMemo(() => (veri ? bolumKaynaklari(bolum, veri) : []), [veri, bolum]);
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
        {veri?.guncelleme && <span className="sbk-ust-g">Veriler {tarihTR(veri.guncelleme)} tarihinde resmî kaynaklardan derlendi</span>}
      </header>

      <nav ref={navRef} className="sbk-nav" aria-label="Sağlık Bakanlığı bölümleri">
        {BOLUMLER.map((b) => {
          const Ic = b.icon;
          const yol = `${pathFor('health_ministry')}${b.slug ? `/${b.slug}` : ''}`;
          return (
            <a key={b.id} href={yol} aria-current={b.id === bolum ? 'page' : undefined} onClick={linkClick(() => git(b.id))}>
              <Ic aria-hidden /><span>{b.kisa}</span>
            </a>
          );
        })}
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
        <AtifSaglayici ids={kaynakIds} kaynaklar={veri.kaynaklar}>
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
              <Bilesen v={veri} bag={bag} git={git} />
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
      )}
    </div>
  );
};
