/**
 * v15 · Çevrimdışı (/cevrimdisi). Yapı: üstte tek durum kartı (bağlantı, çevrimdışı mod, cihaz alanı, eşitleme, süren indirme +
 * sıra) → İndirilenler (kurul → ders, boyut, sil, test/onar) → İndirilebilir (kurul seçici, ders kartları, toplu indir) ;
 * yan sütun: Ayarlar, Cihazdaki yer, Eşitleme, .medspak okuyucu, tümünü sil. Motor: services/cevrimdisi/paketMotoru.ts;
 * arka plan işleri: services/arkaPlanIsleri.ts (/arka-plan). Stil: styles/v15/cevrimdisi15.css (.cv15-*).
 */
import React, { useEffect, useMemo, useState } from 'react';
import {
  Activity, AlertTriangle, ChevronDown, CloudOff, Loader2, Pause, Play, RefreshCw, Signal, Sparkles, VolumeX, Wifi, X, CloudDownload,
} from 'lucide-react';
import {
  agTuru, ayarYaz, cevrimdisiBaslat, cevrimdisiModuAc, cevrimdisiModuKapat, dosyaTuru, duraklat, guncellemeler, katalogYenile, kuyrugaEkle,
  kuyruktanCikar, modulDokumu, paketDurumu, secimAl, secimDegistir, secimliBayt, useCevrimdisi, useDepolama, yerAc, type Modul, type Paket,
} from '../../services/cevrimdisi/paketMotoru';
import { boyutYaz } from '../../services/cevrimdisi/dersBirimleri';
import { sayfaPaketleri } from '../../services/cevrimdisi/sayfaPaketleri';
import { useArkaPlanOzet } from '../../services/arkaPlanIsleri';
import { linkClick, navigateTo, pathFor } from '../../router';
import { useV15Baslik } from '../v15/baslik';
import EsitlemeKarti from './EsitlemeKarti';
import Indirilenler from './Indirilenler';
import Indirilebilir from './Indirilebilir';
import { OnayliSil, sureYaz } from './cvOrtak';
import '../../styles/cevrimdisi.css';
import '../../styles/v15/cevrimdisi15.css';

const MedspakOkuyucu = React.lazy(() => import('./MedspakOkuyucu'));

/** Eski içe aktarımlar için (boyut biçimi tek kaynak: dersBirimleri) */
export { boyutYaz };

const MODUL_AD: Record<Modul, string> = {
  uygulama: 'Uygulama dosyaları', sesli: 'Sesli dersler', medspak: 'Ders paketleri', cozucu: 'Soru çözücü', onem: 'En önemliler',
  alt: 'Alternatif çözücü', ogren: 'Etkileşimli dersler', veri: 'Başvuru verileri', db: 'Çıkmış sorular ve havuz',
};

export default function CevrimdisiView() {
  const S = useCevrimdisi();
  const [topluAcik, setTopluAcik] = useState(false);
  useEffect(() => { document.title = 'Çevrimdışı · MeDSor'; }, []);
  useEffect(() => { void cevrimdisiBaslat().then(() => katalogYenile(true)); }, []);

  const cihaz = Object.values(S.kayitlar).filter((k) => !k.yarim);
  const cihazBayt = cihaz.reduce((a, k) => a + k.bayt, 0);
  const guncel = useMemo(() => guncellemeler(S), [S]);
  useV15Baslik({ baslik: 'Çevrimdışı', alt: cihaz.length ? `${cihaz.length} paket · ${boyutYaz(cihazBayt)} cihazda` : 'Dersleri internetsiz kullanmak için indir' });

  // İlk açılışta (cihazda hiçbir şey yokken) toplu indirme açık gelir
  const hicYok = cihaz.length === 0 && !S.kuyruk.length;
  useEffect(() => { if (S.hazir && hicYok && S.katalog.length) setTopluAcik(true); }, [S.hazir, S.katalog.length]); // eslint-disable-line react-hooks/exhaustive-deps

  const indirilebilirGit = () => document.getElementById('cv15-indirilebilir')?.scrollIntoView({ behavior: 'smooth', block: 'start' });

  return (
    <div className="cv15">
      <h1 className="sr-only">Çevrimdışı</h1>
      <SayfaKarti />
      <DurumKarti cihazSay={cihaz.length} cihazBayt={cihazBayt} toplu={() => { setTopluAcik(true); indirilebilirGit(); }} />

      {guncel.length > 0 && (
        <div className="cv15-serit is-w" role="status">
          <RefreshCw aria-hidden /><span>{guncel.length} pakette yeni içerik var.</span>
          <button type="button" className="cv15-b is-a" onClick={() => kuyrugaEkle(guncel, true)}>Tümünü güncelle</button>
        </div>
      )}
      {S.katalogHata && <div className="cv15-serit is-b" role="alert"><AlertTriangle aria-hidden /><span>{S.katalogHata}</span></div>}

      <div className="cv15-izgara">
        <div className="cv15-ana">
          <section aria-labelledby="cv15-indirilenler" className="cv15-bolum">
            <h2 id="cv15-indirilenler" className="cv15-bb">İndirilenler</h2>
            <Indirilenler gotur={indirilebilirGit} />
          </section>
          <section aria-labelledby="cv15-indirilebilir" className="cv15-bolum">
            <h2 id="cv15-indirilebilir" className="cv15-bb">İndirilebilir</h2>
            <Indirilebilir topluAcik={topluAcik} setTopluAcik={setTopluAcik} />
          </section>
        </div>
        <aside className="cv15-yan">
          <section aria-labelledby="cv15-ayarlar" className="cv15-bolum">
            <h2 id="cv15-ayarlar" className="cv15-bb">Ayarlar</h2>
            <Ayarlar />
          </section>
          {cihaz.length > 0 && (
            <section aria-labelledby="cv15-yer" className="cv15-bolum">
              <h2 id="cv15-yer" className="cv15-bb">Cihazdaki yer</h2>
              <AlanKarti />
            </section>
          )}
          <section aria-labelledby="cv15-esit" className="cv15-bolum">
            <h2 id="cv15-esit" className="cv15-bb">Eşitleme</h2>
            <div className="cv cv15-gomulu"><EsitlemeKarti /></div>
          </section>
          <section aria-label="Ders paketi aç" className="cv15-bolum">
            <div className="cv cv15-gomulu"><React.Suspense fallback={null}><MedspakOkuyucu /></React.Suspense></div>
          </section>
          {cihaz.length > 0 && (
            <div className="cv15-tehlike v15-card">
              <span><b>Cihazdaki tüm içerik</b><span className="v15-cap">{cihaz.length} paket · {boyutYaz(cihazBayt)}. Çözdüğün sorular ve ilerlemen silinmez.</span></span>
              <OnayliSil ids={Object.keys(S.kayitlar)} etiket="Tümünü sil" />
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}

/* ---------------------------------------------------------------- durum kartı ---------------------------------------------------------------- */
function DurumKarti({ cihazSay, cihazBayt, toplu }: { cihazSay: number; cihazBayt: number; toplu: () => void }) {
  const { s: S, ag, kv, kuyruk, toplam: isSay } = useArkaPlanOzet();
  const dep = useDepolama();
  const a = agTuru();
  const [kapatSor, setKapatSor] = useState(false);
  const [siraAcik, setSiraAcik] = useState(false);
  const arkaHref = pathFor('arka_plan');
  const aktif = S.aktif;
  const aktifP = aktif ? S.katalog.find((p) => p.id === aktif.id) : null;
  const oran = aktif && aktif.toplam ? Math.min(1, aktif.alinan / aktif.toplam) : 0;
  const kalanBayt = S.kuyruk.reduce((t, id) => t + (S.katalog.find((p) => p.id === id)?.bayt || 0), 0) - (aktif?.alinan || 0);
  const bekleyen = kv + kuyruk;
  const dolu = dep && dep.kota > 0 ? Math.min(100, (dep.kullanilan / dep.kota) * 100) : 0;
  const AgIk = ag === 'offline' ? CloudOff : a.hucresel ? Signal : Wifi;
  const hicYok = cihazSay === 0 && !S.kuyruk.length;

  return (
    <section className="cv15-durum v15-card" aria-label="Durum">
      <div className="cv15-durum-ust">
        <span className={`v15-tile ${ag === 'offline' ? 'is-w' : ag === 'slow' ? 'is-w' : 'is-ok'}`}><AgIk aria-hidden /></span>
        <span className="cv15-durum-t">
          <b>{ag === 'offline' ? 'İnternet yok' : ag === 'slow' ? 'Bağlantı zayıf' : 'Çevrimiçi'}{a.hucresel ? ' · mobil veri' : ''}</b>
          <span className="v15-cap">
            {S.ayar.acik
              ? paketDurumu('uygulama', S) === 'tamam' ? 'Çevrimdışı mod açık · uygulama internetsiz açılır' : 'Çevrimdışı mod açık · uygulama dosyaları iniyor'
              : 'Çevrimdışı mod kapalı · yalnız indirdiğin dersler cihazda'}
          </span>
        </span>
        <label className="cv15-anahtar">
          <span className="sr-only">Çevrimdışı mod</span>
          <input type="checkbox" role="switch" checked={S.ayar.acik}
            onChange={() => (S.ayar.acik ? setKapatSor(true) : hicYok ? toplu() : cevrimdisiModuAc([]))} />
        </label>
      </div>
      {kapatSor && (
        <div className="cv15-sor" role="alertdialog" aria-label="Çevrimdışı modu kapat">
          <span>Çevrimdışı mod kapansın mı? İndirdiğin dersler istersen cihazda kalır.</span>
          <span className="cv15-arac">
            <button type="button" className="cv15-b" onClick={() => { void cevrimdisiModuKapat(false); setKapatSor(false); }}>Kapat, dersler kalsın</button>
            <button type="button" className="cv15-b is-sil" onClick={() => { void cevrimdisiModuKapat(true); setKapatSor(false); }}>Kapat ve hepsini sil</button>
            <button type="button" className="cv15-b is-sade" onClick={() => setKapatSor(false)}>Vazgeç</button>
          </span>
        </div>
      )}

      <dl className="cv15-olcu">
        <div>
          <dt className="v15-label">Cihazda</dt>
          <dd><b>{cihazBayt ? boyutYaz(cihazBayt) : '0 MB'}</b><span className="v15-cap">{cihazSay} paket</span></dd>
        </div>
        <div>
          <dt className="v15-label">Alan</dt>
          <dd>
            {dep && dep.kota > 0 ? (
              <>
                <b>{boyutYaz(dep.kullanilan)} <span className="v15-cap">/ {boyutYaz(dep.kota)}</span></b>
                <span className="v15-bar" role="meter" aria-label="Kullanılan alan" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(dolu)}><span style={{ width: `${Math.max(1, dolu)}%` }} /></span>
                <span className="v15-cap">Boş ≈ {boyutYaz(Math.max(0, dep.kota - dep.kullanilan))}{dep.kalici ? ' · kalıcı depo' : ''}</span>
              </>
            ) : <span className="v15-cap">Tarayıcı alan bilgisi vermiyor</span>}
          </dd>
        </div>
        <div>
          <dt className="v15-label">Eşitleme</dt>
          <dd><b>{bekleyen ? `${bekleyen} bekliyor` : 'Güncel'}</b><span className="v15-cap">{bekleyen ? (ag === 'offline' ? 'Bağlantı gelince gönderilir' : 'Gönderiliyor') : 'Gönderilmemiş değişiklik yok'}</span></dd>
        </div>
      </dl>

      {(aktif || S.kuyruk.length > 0) && (
        <div className="cv15-aktif" aria-live="polite">
          <div className="cv15-aktif-ust">
            <span className="cv15-durum-t">
              <b>{S.duraklat ? 'Duraklatıldı' : aktif?.bekliyor || (aktifP ? aktifP.baslik : 'Hazırlanıyor…')}</b>
              <span className="v15-cap">
                {aktif && !aktif.bekliyor ? `${boyutYaz(aktif.alinan)} / ${boyutYaz(aktif.toplam)}` : ''}
                {aktif && !aktif.bekliyor && aktif.hiz > 0 ? ` · ${boyutYaz(aktif.hiz)}/sn` : ''}
                {aktif && !aktif.bekliyor && aktif.hiz > 0 && kalanBayt > 0 ? ` · kalan ≈ ${sureYaz(kalanBayt / aktif.hiz)}` : ''}
                {` · sırada ${S.kuyruk.length}`}
              </span>
            </span>
            {aktif?.bekliyor?.startsWith('Wi-Fi')
              ? <button type="button" className="cv15-b" onClick={() => ayarYaz({ wifi: false })}>Şimdi indir</button>
              : <button type="button" className="cv15-b is-ikon" onClick={() => duraklat(!S.duraklat)} aria-label={S.duraklat ? 'Sürdür' : 'Duraklat'} title={S.duraklat ? 'Sürdür' : 'Duraklat'}>{S.duraklat ? <Play aria-hidden /> : <Pause aria-hidden />}</button>}
            <button type="button" className="cv15-b" aria-expanded={siraAcik} onClick={() => setSiraAcik(!siraAcik)}>Sıra <ChevronDown aria-hidden className={siraAcik ? 'is-ac' : ''} /></button>
          </div>
          <span className="v15-bar" role="progressbar" aria-label="İndirme" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(oran * 100)}><span style={{ width: `${Math.round(oran * 100)}%` }} /></span>
          {siraAcik && (
            <ul className="cv15-sira">
              {S.kuyruk.map((id) => {
                const p = S.katalog.find((x) => x.id === id);
                return (
                  <li key={id}>
                    <span className="cv15-durum-t"><b>{p?.baslik || id}</b><span className="v15-cap">{p ? `${p.grup} · ${boyutYaz(p.bayt)}` : ''}</span></span>
                    <button type="button" className="cv15-b is-ikon" onClick={() => kuyruktanCikar([id])} aria-label="Sıradan çıkar"><X aria-hidden /></button>
                  </li>
                );
              })}
              {S.kuyruk.length > 1 && <li><button type="button" className="cv15-b is-sade" onClick={() => kuyruktanCikar([...S.kuyruk])}>Hepsini iptal et</button></li>}
            </ul>
          )}
        </div>
      )}

      <a className="cv15-arka" href={arkaHref} onClick={linkClick(() => navigateTo(arkaHref))}>
        <Activity aria-hidden /><span>Arka plan işleri</span><span className="v15-cap">{isSay ? `${isSay} iş` : 'İş yok'}</span>
      </a>
    </section>
  );
}

/* ---------------------------------------------------------------- ayarlar ---------------------------------------------------------------- */
function Anahtar({ ad, alt, deger, degis }: { ad: string; alt: string; deger: boolean; degis: (v: boolean) => void }) {
  return (
    <label className="cv15-ayar">
      <span className="cv15-durum-t"><b>{ad}</b><span className="v15-cap">{alt}</span></span>
      <span className="cv15-anahtar"><input type="checkbox" role="switch" checked={deger} onChange={(e) => degis(e.target.checked)} /></span>
    </label>
  );
}

function Ayarlar() {
  const { ayar } = useCevrimdisi();
  return (
    <div className="cv15-ayarlar v15-card">
      <Anahtar ad="Yalnız Wi-Fi'de indir" alt="Mobil veride indirmeler Wi-Fi gelene dek bekler." deger={ayar.wifi} degis={(v) => ayarYaz({ wifi: v })} />
      <Anahtar ad="Güncellemeleri kendiliğinden indir" alt="İndirdiğin derslerin yeni sürümü çıkınca arka planda iner." deger={ayar.otoGuncelle} degis={(v) => ayarYaz({ otoGuncelle: v })} />
      <Anahtar ad="Sesleri de indir" alt="Yeni indirmelerde varsayılan. Kapalıyken dersler sessiz, çok daha az yer kaplar." deger={ayar.ses} degis={(v) => ayarYaz({ ses: v })} />
      <Anahtar ad="Ders PDF'lerini de indir" alt="Yeni indirmelerde varsayılan." deger={ayar.pdf} degis={(v) => ayarYaz({ pdf: v })} />
      <label className="cv15-ayar">
        <span className="cv15-durum-t"><b>Cihazda boş bırak</b><span className="v15-cap">İndirme bu boş alanın altına düşürmez.</span></span>
        <select className="cv15-sec" value={ayar.pay} onChange={(e) => ayarYaz({ pay: Number(e.target.value) })}>
          {[100, 300, 1024, 2048].map((m) => <option key={m} value={m * 1024 * 1024}>{m >= 1024 ? `${m / 1024} GB` : `${m} MB`}</option>)}
        </select>
      </label>
    </div>
  );
}

/* ---------------------------------------------------------------- alan dökümü ---------------------------------------------------------------- */
function AlanKarti() {
  const S = useCevrimdisi();
  const dokum = useMemo(() => modulDokumu(S), [S]);
  const [sonuc, setSonuc] = useState<string | null>(null);
  const [calisiyor, setCalisiyor] = useState(false);
  const toplam = dokum.reduce((t, x) => t + x.bayt, 0) || 1;
  const sesliIds = Object.values(S.kayitlar)
    .filter((k) => !k.yarim && k.dosyalar.some((d) => dosyaTuru(d.u) === 'ses') && S.katalog.find((p) => p.id === k.id)?.ek?.ses)
    .map((k) => k.id);
  const sesToplam = dokum.reduce((t, x) => t + (x.modul === 'sesli' ? 0 : x.ses), 0);
  return (
    <div className="cv15-alan-k v15-card">
      <ul className="cv15-dokum">
        {dokum.map((x) => (
          <li key={x.modul}>
            <span className="cv15-dokum-ad">{MODUL_AD[x.modul]}<span className="v15-cap"> · {x.n}</span></span>
            <b>{boyutYaz(x.bayt)}</b>
            <span className="v15-bar"><span style={{ width: `${Math.max(2, (x.bayt / toplam) * 100)}%` }} /></span>
          </li>
        ))}
      </ul>
      <div className="cv15-arac">
        {sesliIds.length > 0 && sesToplam > 0 && (
          <button type="button" className="cv15-b" onClick={() => void secimDegistir(sesliIds, { ses: false })}><VolumeX aria-hidden /> <span>Tüm sesleri kaldır · {boyutYaz(sesToplam)}</span></button>
        )}
        <button type="button" className="cv15-b" disabled={calisiyor}
          onClick={async () => { setCalisiyor(true); const b = await yerAc().catch(() => 0); setCalisiyor(false); setSonuc(b ? `${boyutYaz(b)} artık dosya silindi.` : 'Silinecek artık dosya yok.'); }}>
          {calisiyor ? <Loader2 className="cv15-don" aria-hidden /> : <Sparkles aria-hidden />} <span>Artık dosyaları temizle</span>
        </button>
      </div>
      {sonuc && <p className="v15-cap" role="status">{sonuc}</p>}
    </div>
  );
}

/* ---------------------------------------------------------------- bu sayfa (?sayfa=) ---------------------------------------------------------------- */
function SayfaKarti() {
  const S = useCevrimdisi();
  const sayfa = useMemo(() => { try { return new URLSearchParams(location.search).get('sayfa') || ''; } catch { return ''; } }, []);
  if (!sayfa || !S.katalog.length) return null;
  const ids = sayfaPaketleri(sayfa, S.katalog);
  const paketler = ids.map((id) => S.katalog.find((p) => p.id === id)).filter((p): p is Paket => !!p);
  const eksik = paketler.filter((p) => !['tamam', 'guncelleme', 'kuyrukta', 'iniyor'].includes(paketDurumu(p.id, S)));
  const suruyor = paketler.some((p) => ['kuyrukta', 'iniyor'].includes(paketDurumu(p.id, S)));
  const bayt = eksik.reduce((t, p) => t + secimliBayt(p, secimAl(p.id, S)), 0);
  const ad = paketler.length === 1 ? paketler[0].baslik : `${paketler.length} paket`;
  const ilgili = paketler.length <= 3
    ? [...new Set(paketler.flatMap((p) => p.ilgili || []))].filter((id) => !ids.includes(id) && paketDurumu(id, S) === 'yok')
      .map((id) => S.katalog.find((p) => p.id === id)).filter((p): p is Paket => !!p)
    : [];
  return (
    <section className="cv15-sayfa v15-card" aria-label="Geldiğin sayfa">
      <div className="cv15-durum-ust">
        <span className="v15-tile"><CloudDownload aria-hidden /></span>
        <span className="cv15-durum-t">
          <b>Geldiğin sayfa</b>
          <span className="v15-cap">
            {!paketler.length ? 'Bu sayfa internet gerektirir ya da indirilecek ayrı içeriği yok.'
              : !eksik.length ? (suruyor ? `${ad} iniyor…` : `${ad} cihazında: bu sayfa internetsiz açılır.`)
                : `${ad} · ${eksik.length < paketler.length ? `${eksik.length} eksik · ` : ''}${boyutYaz(bayt)}`}
          </span>
        </span>
        {eksik.length > 0 && <button type="button" className="v15-btn" onClick={() => kuyrugaEkle(eksik.map((p) => p.id))}>İndir</button>}
      </div>
      {ilgili.length > 0 && (
        <ul className="cv15-sira" aria-label="Aynı dersin öteki bölümleri">
          {ilgili.map((p) => (
            <li key={p.id}>
              <span className="cv15-durum-t"><b>{MODUL_AD[p.modul] || p.grup}</b><span className="v15-cap">{p.baslik} · {boyutYaz(secimliBayt(p, secimAl(p.id, S)))}</span></span>
              <button type="button" className="cv15-b" onClick={() => kuyrugaEkle([p.id])}>Ekle</button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
