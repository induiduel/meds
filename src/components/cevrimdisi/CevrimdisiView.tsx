/**
 * Çevrimdışı merkezi (/cevrimdisi): çevrimdışı modu aç/kapa, ders paketlerini indir · güncelle · sil, indirme kuyruğu, cihaz alanı
 * ve veri eşitleme durumu. Motor: services/cevrimdisi/paketMotoru.ts. Stil: styles/cevrimdisi.css (.cv-*).
 */
import React, { useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle, BookOpen, Check, ChevronDown, CloudDownload, CloudOff, Database, Download, Headphones, HardDrive, Loader2,
  MessageCircleQuestion, Pause, Play, RefreshCw, Search, Smartphone, Star, Trash2, Wifi, X, FileText, VolumeX, Sparkles,
} from 'lucide-react';
import {
  agTuru, ayarYaz, cevrimdisiBaslat, cevrimdisiModuAc, cevrimdisiModuKapat, duraklat, guncellemeler, katalogYenile, kuyrugaEkle,
  kuyruktanCikar, dosyaTuru, modulDokumu, paketDurumu, paketSil, secimAl, secimDegistir, secimliBayt, useCevrimdisi, useDepolama, yerAc,
  type Durum, type Modul, type Paket, type Secim,
} from '../../services/cevrimdisi/paketMotoru';
import { useNetState } from '../../services/net';
import EsitlemeKarti from './EsitlemeKarti';
import '../../styles/cevrimdisi.css';

type Sekme = 'sesli' | 'cozucu' | 'onem' | 'alt' | 'ogren' | 'veri';
const SEKMELER: { id: Sekme; ad: string; kisa: string; ikon: React.ComponentType<any>; moduller: Modul[] }[] = [
  { id: 'sesli', ad: 'Sesli dersler', kisa: 'Sesli', ikon: Headphones, moduller: ['sesli'] },
  { id: 'cozucu', ad: 'Soru çözücü', kisa: 'Çözücü', ikon: MessageCircleQuestion, moduller: ['cozucu'] },
  { id: 'onem', ad: 'En önemliler', kisa: 'Önemli', ikon: Star, moduller: ['onem'] },
  { id: 'alt', ad: 'Alternatif çözücü', kisa: 'Alternatif', ikon: Headphones, moduller: ['alt'] },
  { id: 'ogren', ad: 'Etkileşimli dersler', kisa: 'Öğren', ikon: BookOpen, moduller: ['ogren'] },
  { id: 'veri', ad: 'Sorular ve başvuru', kisa: 'Veri', ikon: Database, moduller: ['db', 'veri'] },
];
type Suzgec = 'tum' | 'cihazda' | 'yok' | 'guncel';
const SUZGEC_AD: Record<Suzgec, string> = { tum: 'Tümü', cihazda: 'Cihazda', yok: 'İndirilmedi', guncel: 'Güncellemesi olan' };

export const boyutYaz = (n: number) => {
  if (!n) return '—';
  if (n < 1024 * 1024) return `${Math.max(1, Math.round(n / 1024))} KB`;
  if (n < 1024 ** 3) return `${(n / 1024 / 1024).toFixed(n < 10 * 1024 * 1024 ? 1 : 0).replace('.', ',')} MB`;
  return `${(n / 1024 ** 3).toFixed(2).replace('.', ',')} GB`;
};
const sureYaz = (sn: number) => {
  if (!isFinite(sn) || sn <= 0) return '';
  if (sn < 60) return `${Math.ceil(sn)} sn`;
  if (sn < 3600) return `${Math.ceil(sn / 60)} dk`;
  return `${Math.floor(sn / 3600)} sa ${Math.ceil((sn % 3600) / 60)} dk`;
};
const katla = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

/* ---------------------------------------------------------------- satır ---------------------------------------------------------------- */
/** Ses / PDF parçası aç-kapa: indirilmişse kaldırmak anında yer açar, eklemek eksik dosyaları indirir */
function EkCip({ p, tur, secim }: { p: Paket; tur: 'ses' | 'pdf'; secim: Secim }) {
  const e = p.ek?.[tur];
  if (!e) return null;
  const acik = secim[tur];
  const Ik = tur === 'ses' ? Headphones : FileText;
  const ad = tur === 'ses' ? 'Ses' : 'PDF';
  return (
    <button type="button" className={`cv-ek${acik ? ' is-on' : ''}`} aria-pressed={acik}
      title={acik ? `${ad} dahil (${boyutYaz(e.b)}). Kaldırmak için dokun.` : `${ad} dahil değil. Eklemek için dokun (+${boyutYaz(e.b)}).`}
      aria-label={`${p.baslik}: ${ad.toLocaleLowerCase('tr-TR')} ${acik ? 'dahil, kaldır' : 'dahil değil, ekle'} (${boyutYaz(e.b)})`}
      onClick={() => void secimDegistir([p.id], { [tur]: !acik })}>
      {acik ? <Ik aria-hidden="true" /> : tur === 'ses' ? <VolumeX aria-hidden="true" /> : <FileText aria-hidden="true" />}
      <span>{acik ? ad : tur === 'ses' ? 'Sessiz' : 'PDF yok'}</span>
    </button>
  );
}

function PaketSatiri({ p, durum, hata, oran }: { p: Paket; durum: Durum; hata?: string; oran?: number }) {
  const S = useCevrimdisi();
  const secim = secimAl(p.id, S);
  const [onay, setOnay] = useState(false);
  useEffect(() => {
    if (!onay) return;
    const t = window.setTimeout(() => setOnay(false), 3500);
    return () => window.clearTimeout(t);
  }, [onay]);
  return (
    <li className={`cv-satir is-${durum}`}>
      <span className="cv-isaret" aria-hidden="true">
        {durum === 'tamam' ? <Check /> : durum === 'iniyor' ? <Loader2 className="cv-don" /> : durum === 'guncelleme' ? <RefreshCw /> : durum === 'hata' ? <AlertTriangle /> : durum === 'kuyrukta' ? <Download /> : null}
      </span>
      <span className="cv-satir-metin">
        <b>{p.baslik}</b>
        <small>
          {p.alt ? `${p.alt} · ` : ''}{boyutYaz(durum === 'tamam' || durum === 'guncelleme' ? (S.kayitlar[p.id]?.bayt || secimliBayt(p, secim)) : secimliBayt(p, secim))}
          {durum === 'guncelleme' && <em className="cv-etiket is-warn">Güncelleme var</em>}
          {durum === 'kuyrukta' && <em className="cv-etiket">Sırada</em>}
          {durum === 'iniyor' && <em className="cv-etiket is-acc">%{Math.round((oran || 0) * 100)}</em>}
        </small>
        {durum === 'hata' && hata && <small className="cv-hata">{hata}</small>}
        {p.ek && (
          <span className="cv-ekler">
            <EkCip p={p} tur="ses" secim={secim} />
            <EkCip p={p} tur="pdf" secim={secim} />
          </span>
        )}
        {durum === 'iniyor' && <span className="cv-cubuk"><i style={{ width: `${Math.round((oran || 0) * 100)}%` }} /></span>}
      </span>
      <span className="cv-satir-eylem">
        {(durum === 'yok' || durum === 'hata') && (
          <button type="button" className="cv-btn is-birincil" onClick={() => kuyrugaEkle([p.id])}>
            <Download aria-hidden="true" /> <span>{durum === 'hata' ? 'Yeniden dene' : 'İndir'}</span>
          </button>
        )}
        {durum === 'guncelleme' && (
          <button type="button" className="cv-btn is-birincil" onClick={() => kuyrugaEkle([p.id], true)}>
            <RefreshCw aria-hidden="true" /> <span>Güncelle</span>
          </button>
        )}
        {(durum === 'kuyrukta' || durum === 'iniyor') && (
          <button type="button" className="cv-btn" onClick={() => kuyruktanCikar([p.id])} aria-label={`${p.baslik} indirmesini iptal et`}>
            <X aria-hidden="true" /> <span>İptal</span>
          </button>
        )}
        {(durum === 'tamam' || durum === 'guncelleme') && !p.zorunlu && (
          <button type="button" className={`cv-btn is-sil${onay ? ' is-onay' : ''}`} onClick={() => (onay ? void paketSil([p.id]) : setOnay(true))}
            aria-label={onay ? `${p.baslik}: silmeyi onayla` : `${p.baslik}: cihazdan sil`}>
            <Trash2 aria-hidden="true" /> <span>{onay ? 'Sil?' : 'Sil'}</span>
          </button>
        )}
      </span>
    </li>
  );
}

/* ---------------------------------------------------------------- hızlı kurulum ---------------------------------------------------------------- */
function HizliKurulum({ katalog, kapat }: { katalog: Paket[]; kapat?: () => void }) {
  const gruplar = useMemo(() => {
    const m = new Map<string, number>();
    for (const p of katalog) if (['sesli', 'cozucu', 'onem', 'alt'].includes(p.modul)) m.set(p.grup, (m.get(p.grup) || 0) + 1);
    return [...m.entries()].sort((a, b) => b[1] - a[1]).map(([g]) => g);
  }, [katalog]);
  const [grupSec, setGrupSec] = useState<string[]>([]);
  const [modulSec, setModulSec] = useState<Modul[]>(['sesli', 'cozucu', 'onem', 'db']);
  const ayar = useCevrimdisi().ayar;
  const [secim, setSecim] = useState<Secim>({ ses: ayar.ses, pdf: ayar.pdf });
  useEffect(() => { if (!grupSec.length && gruplar.length) setGrupSec(gruplar.slice(0, 1)); }, [gruplar]); // eslint-disable-line react-hooks/exhaustive-deps
  const MODS: { id: Modul; ad: string }[] = [
    { id: 'sesli', ad: 'Sesli dersler' }, { id: 'cozucu', ad: 'Soru çözücü' }, { id: 'onem', ad: 'En önemliler + sesli asistan' },
    { id: 'alt', ad: 'Alternatif çözücü' }, { id: 'ogren', ad: 'Etkileşimli dersler' }, { id: 'db', ad: 'Çıkmış sorular ve havuz' },
    { id: 'veri', ad: 'Sözlük, özetler, notlar' },
  ];
  const secilen = katalog.filter((p) => modulSec.includes(p.modul) && (p.modul === 'db' || p.modul === 'veri' || grupSec.includes(p.grup)));
  const bayt = secilen.reduce((a, p) => a + (paketDurumu(p.id) === 'tamam' ? 0 : secimliBayt(p, secim)), 0);
  const sesBayt = secilen.reduce((a, p) => a + (paketDurumu(p.id) === 'tamam' ? 0 : p.ek?.ses?.b || 0), 0);
  const pdfBayt = secilen.reduce((a, p) => a + (paketDurumu(p.id) === 'tamam' ? 0 : p.ek?.pdf?.b || 0), 0);
  const ac = (arr: string[], x: string) => (arr.includes(x) ? arr.filter((y) => y !== x) : [...arr, x]);
  return (
    <section className="cv-kart cv-kurulum" aria-labelledby="cv-kurulum-b">
      <div className="cv-kart-bas">
        <h2 id="cv-kurulum-b">Neleri cihaza alalım?</h2>
        {kapat && <button type="button" className="cv-ikonbtn" onClick={kapat} aria-label="Kapat"><X aria-hidden="true" /></button>}
      </div>
      <p className="cv-not">Seçtiğin dersler arka planda iner. İnenler internetsiz de açılır; istediğin zaman aşağıdan tek tek silebilir ya da ekleyebilirsin.</p>
      <div className="cv-alan">
        <span className="cv-alan-ad">Dersler</span>
        <div className="cv-cipler">
          {gruplar.map((g) => (
            <button key={g} type="button" className={`cv-cip${grupSec.includes(g) ? ' is-on' : ''}`} aria-pressed={grupSec.includes(g)} onClick={() => setGrupSec(ac(grupSec, g))}>{g}</button>
          ))}
        </div>
      </div>
      <div className="cv-alan">
        <span className="cv-alan-ad">İçerik</span>
        <div className="cv-cipler">
          {MODS.map((m) => (
            <button key={m.id} type="button" className={`cv-cip${modulSec.includes(m.id) ? ' is-on' : ''}`} aria-pressed={modulSec.includes(m.id)}
              onClick={() => setModulSec(ac(modulSec, m.id) as Modul[])}>{m.ad}</button>
          ))}
        </div>
      </div>
      <div className="cv-alan">
        <span className="cv-alan-ad">Ek dosyalar</span>
        <div className="cv-cipler">
          <button type="button" className={`cv-cip${secim.ses ? ' is-on' : ''}`} aria-pressed={secim.ses} onClick={() => setSecim({ ...secim, ses: !secim.ses })}>
            {secim.ses ? 'Sesli' : 'Sessiz'}{sesBayt ? ` · ${boyutYaz(sesBayt)}` : ''}
          </button>
          <button type="button" className={`cv-cip${secim.pdf ? ' is-on' : ''}`} aria-pressed={secim.pdf} onClick={() => setSecim({ ...secim, pdf: !secim.pdf })}>
            {secim.pdf ? 'Ders PDF\'leri dahil' : 'PDF yok'}{pdfBayt ? ` · ${boyutYaz(pdfBayt)}` : ''}
          </button>
        </div>
      </div>
      <p className="cv-not">Sessiz indirilen dersler metin, soru ve açıklamalarla tam çalışır; sesi sonra tek dokunuşla ekleyebilirsin.</p>
      <div className="cv-kurulum-alt">
        <span><b>{secilen.length}</b> paket · yaklaşık <b>{boyutYaz(bayt)}</b> indirilecek</span>
        <button type="button" className="cv-btn is-birincil is-buyuk" disabled={!secilen.length}
          onClick={() => { cevrimdisiModuAc(secilen.filter((p) => paketDurumu(p.id) !== 'tamam').map((p) => p.id), secim); kapat?.(); }}>
          <CloudDownload aria-hidden="true" /> <span>İndirmeyi başlat</span>
        </button>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- sayfa ---------------------------------------------------------------- */
export default function CevrimdisiView() {
  const S = useCevrimdisi();
  const dep = useDepolama();
  const ag = useNetState();
  const [sekme, setSekme] = useState<Sekme>('sesli');
  const [ara, setAra] = useState('');
  const [suzgec, setSuzgec] = useState<Suzgec>('tum');
  const [kapali, setKapali] = useState<Record<string, boolean>>({});
  const [kurulumAcik, setKurulumAcik] = useState(false);
  const [kuyrukAcik, setKuyrukAcik] = useState(false);
  const [kapatSor, setKapatSor] = useState(false);

  useEffect(() => { document.title = 'Çevrimdışı · MeDSor'; }, []);
  useEffect(() => { void cevrimdisiBaslat().then(() => katalogYenile(true)); }, []);

  const durumlar = useMemo(() => {
    const m: Record<string, Durum> = {};
    for (const p of S.katalog) m[p.id] = paketDurumu(p.id, S);
    return m;
  }, [S]);
  const cihazda = (id: string) => durumlar[id] === 'tamam' || durumlar[id] === 'guncelleme';
  const guncel = useMemo(() => guncellemeler(S), [S]);
  const cihazBayt = Object.values(S.kayitlar).filter((k) => !k.yarim).reduce((a, k) => a + k.bayt, 0);
  const cihazSay = Object.values(S.kayitlar).filter((k) => !k.yarim).length;
  const aktifP = S.aktif ? S.katalog.find((p) => p.id === S.aktif!.id) : null;
  const aktifOran = S.aktif && S.aktif.toplam ? Math.min(1, S.aktif.alinan / S.aktif.toplam) : 0;
  const kuyrukBayt = S.kuyruk.reduce((a, id) => a + (S.katalog.find((p) => p.id === id)?.bayt || 0), 0) - (S.aktif?.alinan || 0);

  const sekmePaketleri = (s: Sekme) => {
    const t = SEKMELER.find((x) => x.id === s)!;
    return S.katalog.filter((p) => t.moduller.includes(p.modul));
  };
  const liste = useMemo(() => {
    const q = katla(ara.trim());
    return sekmePaketleri(sekme).filter((p) => {
      if (q && !katla(`${p.baslik} ${p.alt || ''} ${p.grup}`).includes(q)) return false;
      const d = durumlar[p.id];
      if (suzgec === 'cihazda') return d === 'tamam' || d === 'guncelleme';
      if (suzgec === 'yok') return d === 'yok' || d === 'hata' || d === 'kuyrukta' || d === 'iniyor';
      if (suzgec === 'guncel') return d === 'guncelleme';
      return true;
    });
  }, [S.katalog, sekme, ara, suzgec, durumlar]); // eslint-disable-line react-hooks/exhaustive-deps
  const gruplu = useMemo(() => {
    const m = new Map<string, Paket[]>();
    for (const p of liste) {
      if (!m.has(p.grup)) m.set(p.grup, []);
      m.get(p.grup)!.push(p);
    }
    for (const ps of m.values()) ps.sort((a, b) => a.sira - b.sira);
    return [...m.entries()];
  }, [liste]);

  const agMetni = ag === 'offline' ? 'İnternet yok' : ag === 'slow' ? 'Bağlantı zayıf' : 'Çevrimiçi';
  const a = agTuru();
  const hicPaketYok = cihazSay === 0 && !S.kuyruk.length;

  return (
    <div className="cv">
      <header className="cv-bas">
        <span className="cv-ic" aria-hidden="true"><CloudDownload /></span>
        <div>
          <h1>Çevrimdışı</h1>
          <p>Dersleri cihazına indir; internet yokken ya da bağlantı yavaşken sesli dersler, soru çözücü, en önemliler ve sorular aynı hızla açılır. Çözdüğün sorular ve çalışma süren bağlantı gelince kendiliğinden eşitlenir.</p>
        </div>
      </header>

      {/* Mod + durum */}
      <section className="cv-kart cv-mod" aria-label="Çevrimdışı mod">
        <div className="cv-mod-ust">
          <div className="cv-mod-metin">
            <b>Çevrimdışı mod</b>
            <small>
              {S.ayar.acik
                ? paketDurumu('uygulama', S) === 'tamam' ? 'Açık · uygulama cihazında, internetsiz açılır' : 'Açık · uygulama dosyaları iniyor'
                : 'Kapalı · yalnız indirdiğin dersler cihazda'}
            </small>
          </div>
          <button type="button" role="switch" aria-checked={S.ayar.acik} className={`cv-anahtar${S.ayar.acik ? ' is-on' : ''}`}
            onClick={() => (S.ayar.acik ? setKapatSor(true) : hicPaketYok ? setKurulumAcik(true) : cevrimdisiModuAc([]))}>
            <i /><span className="sr-only">Çevrimdışı mod</span>
          </button>
        </div>
        {kapatSor && (
          <div className="cv-sor" role="alertdialog" aria-label="Çevrimdışı modu kapat">
            <span>Çevrimdışı mod kapansın mı? İndirdiğin dersler istersen cihazda kalır.</span>
            <div>
              <button type="button" className="cv-btn" onClick={() => { void cevrimdisiModuKapat(false); setKapatSor(false); }}>Kapat, dersler kalsın</button>
              <button type="button" className="cv-btn is-sil" onClick={() => { void cevrimdisiModuKapat(true); setKapatSor(false); }}>Kapat ve hepsini sil</button>
              <button type="button" className="cv-btn is-sade" onClick={() => setKapatSor(false)}>Vazgeç</button>
            </div>
          </div>
        )}
        <div className="cv-bilgiler">
          <span className={`cv-bilgi is-${ag}`}>{ag === 'offline' ? <CloudOff aria-hidden="true" /> : <Wifi aria-hidden="true" />}{agMetni}{a.hucresel ? ' · mobil veri' : ''}</span>
          <span className="cv-bilgi"><Smartphone aria-hidden="true" />{cihazSay} paket · {boyutYaz(cihazBayt)}</span>
          {dep && dep.kota > 0 && (
            <span className="cv-bilgi"><HardDrive aria-hidden="true" />Boş alan ≈ {boyutYaz(Math.max(0, dep.kota - dep.kullanilan))}{dep.kalici ? ' · kalıcı' : ''}</span>
          )}
        </div>
        {dep && dep.kota > 0 && (
          <span className="cv-cubuk is-alan" title={`Kullanılan ${boyutYaz(dep.kullanilan)} / ${boyutYaz(dep.kota)}`}>
            <i style={{ width: `${Math.min(100, (dep.kullanilan / dep.kota) * 100)}%` }} />
          </span>
        )}
        <div className="cv-ayarlar">
          <label className="cv-onay">
            <input type="checkbox" checked={S.ayar.wifi} onChange={(e) => ayarYaz({ wifi: e.target.checked })} />
            <span>Yalnız Wi-Fi'de indir</span>
          </label>
          <label className="cv-onay">
            <input type="checkbox" checked={S.ayar.otoGuncelle} onChange={(e) => ayarYaz({ otoGuncelle: e.target.checked })} />
            <span>Güncellemeleri kendiliğinden indir</span>
          </label>
          <label className="cv-onay">
            <input type="checkbox" checked={S.ayar.ses} onChange={(e) => ayarYaz({ ses: e.target.checked })} />
            <span>Yeni derslerde sesleri de indir</span>
          </label>
          <label className="cv-onay">
            <input type="checkbox" checked={S.ayar.pdf} onChange={(e) => ayarYaz({ pdf: e.target.checked })} />
            <span>Yeni derslerde ders PDF'lerini de indir</span>
          </label>
          <label className="cv-onay cv-secim">
            <span>Cihazda boş bırak</span>
            <select value={S.ayar.pay} onChange={(e) => ayarYaz({ pay: Number(e.target.value) })}>
              {[100, 300, 1024, 2048].map((m) => <option key={m} value={m * 1024 * 1024}>{m >= 1024 ? `${m / 1024} GB` : `${m} MB`}</option>)}
            </select>
          </label>
        </div>
      </section>

      {/* Hızlı kurulum */}
      {(kurulumAcik || (hicPaketYok && S.katalog.length > 0)) && (
        <HizliKurulum katalog={S.katalog} kapat={kurulumAcik ? () => setKurulumAcik(false) : undefined} />
      )}

      {/* Süren indirme */}
      {(S.aktif || S.kuyruk.length > 0) && (
        <section className="cv-kart cv-aktif" aria-live="polite" aria-label="İndirme">
          <div className="cv-aktif-ust">
            <span className="cv-aktif-metin">
              <b>{S.duraklat ? 'Duraklatıldı' : S.aktif?.bekliyor || (aktifP ? `İniyor: ${aktifP.baslik}` : 'Hazırlanıyor…')}</b>
              <small>
                {S.aktif && !S.aktif.bekliyor ? `${boyutYaz(S.aktif.alinan)} / ${boyutYaz(S.aktif.toplam)}` : ''}
                {S.aktif && !S.aktif.bekliyor && S.aktif.hiz > 0 ? ` · ${boyutYaz(S.aktif.hiz)}/sn` : ''}
                {S.aktif && !S.aktif.bekliyor && S.aktif.hiz > 0 && kuyrukBayt > 0 ? ` · kalan ≈ ${sureYaz(kuyrukBayt / S.aktif.hiz)}` : ''}
                {` · sırada ${S.kuyruk.length} paket`}
              </small>
            </span>
            <span className="cv-aktif-eylem">
              <button type="button" className="cv-btn" onClick={() => duraklat(!S.duraklat)}>
                {S.duraklat ? <><Play aria-hidden="true" /> <span>Sürdür</span></> : <><Pause aria-hidden="true" /> <span>Duraklat</span></>}
              </button>
              <button type="button" className="cv-btn is-sade" aria-expanded={kuyrukAcik} onClick={() => setKuyrukAcik(!kuyrukAcik)}>
                <span>Sıra</span> <ChevronDown aria-hidden="true" className={kuyrukAcik ? 'is-ters' : ''} />
              </button>
            </span>
          </div>
          <span className="cv-cubuk is-buyuk"><i style={{ width: `${Math.round(aktifOran * 100)}%` }} /></span>
          {kuyrukAcik && (
            <ul className="cv-kuyruk">
              {S.kuyruk.map((id) => {
                const p = S.katalog.find((x) => x.id === id);
                return (
                  <li key={id}>
                    <span>{p?.baslik || id}<small>{p ? ` · ${p.grup} · ${boyutYaz(p.bayt)}` : ''}</small></span>
                    <button type="button" className="cv-ikonbtn" onClick={() => kuyruktanCikar([id])} aria-label="Sıradan çıkar"><X aria-hidden="true" /></button>
                  </li>
                );
              })}
              {S.kuyruk.length > 1 && (
                <li><button type="button" className="cv-btn is-sade" onClick={() => kuyruktanCikar([...S.kuyruk])}>Sıradakilerin hepsini iptal et</button></li>
              )}
            </ul>
          )}
        </section>
      )}

      {guncel.length > 0 && (
        <div className="cv-serit" role="status">
          <RefreshCw aria-hidden="true" />
          <span>{guncel.length} pakette yeni içerik var.</span>
          <button type="button" className="cv-btn is-birincil" onClick={() => kuyrugaEkle(guncel, true)}>Tümünü güncelle</button>
        </div>
      )}
      {S.katalogHata && <div className="cv-serit is-hata" role="alert"><AlertTriangle aria-hidden="true" /><span>{S.katalogHata}</span></div>}

      {/* Modüller */}
      <nav className="cv-sekmeler" aria-label="İçerik türü">
        {SEKMELER.map((t) => {
          const ps = sekmePaketleri(t.id);
          const n = ps.filter((p) => cihazda(p.id)).length;
          const Ik = t.ikon;
          return (
            <button key={t.id} type="button" className={sekme === t.id ? 'is-on' : ''} aria-pressed={sekme === t.id} onClick={() => setSekme(t.id)}>
              <Ik aria-hidden="true" />
              <span className="cv-sekme-ad">{t.ad}</span>
              <span className="cv-sekme-kisa">{t.kisa}</span>
              <span className="cv-sekme-n">{n}/{ps.length}</span>
            </button>
          );
        })}
      </nav>

      <div className="cv-arac">
        <label className="cv-ara">
          <Search aria-hidden="true" />
          <input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Ders ara" aria-label="Ders ara" />
          {ara && <button type="button" onClick={() => setAra('')} aria-label="Aramayı temizle"><X aria-hidden="true" /></button>}
        </label>
        <div className="cv-suz" role="group" aria-label="Süzgeç">
          {(Object.keys(SUZGEC_AD) as Suzgec[]).map((s) => (
            <button key={s} type="button" className={`cv-cip${suzgec === s ? ' is-on' : ''}`} aria-pressed={suzgec === s} onClick={() => setSuzgec(s)}>{SUZGEC_AD[s]}</button>
          ))}
        </div>
      </div>

      {!S.hazir || (!S.katalog.length && !S.katalogHata) ? (
        <div className="cv-bos"><Loader2 className="cv-don" aria-hidden="true" /> Paketler yükleniyor…</div>
      ) : !gruplu.length ? (
        <div className="cv-bos">Bu süzgeçte paket yok.</div>
      ) : (
        gruplu.map(([g, ps]) => {
          const inen = ps.filter((p) => cihazda(p.id));
          const eksik = ps.filter((p) => ['yok', 'hata'].includes(durumlar[p.id]));
          const gun = ps.filter((p) => durumlar[p.id] === 'guncelleme');
          const anahtar = `${sekme}|${g}`;
          const acik = !kapali[anahtar];
          return (
            <section key={g} className="cv-grup">
              <div className="cv-grup-bas">
                <button type="button" className="cv-grup-ac" aria-expanded={acik} onClick={() => setKapali({ ...kapali, [anahtar]: acik })}>
                  <ChevronDown aria-hidden="true" className={acik ? '' : 'is-kapali'} />
                  <b>{g}</b>
                  <small>{inen.length}/{ps.length} cihazda · {boyutYaz(inen.reduce((x, p) => x + (S.kayitlar[p.id]?.bayt || p.bayt), 0))} / {boyutYaz(ps.reduce((x, p) => x + secimliBayt(p, secimAl(p.id, S)), 0))}</small>
                </button>
                <span className="cv-grup-eylem">
                  {gun.length > 0 && <button type="button" className="cv-btn" onClick={() => kuyrugaEkle(gun.map((p) => p.id), true)}><RefreshCw aria-hidden="true" /> <span>Güncelle</span></button>}
                  {eksik.length > 0 && (
                    <button type="button" className="cv-btn is-birincil" onClick={() => kuyrugaEkle(eksik.map((p) => p.id))}>
                      <Download aria-hidden="true" /> <span>{eksik.length === ps.length ? 'Hepsini indir' : `Kalan ${eksik.length}`}</span>
                      <em>{boyutYaz(eksik.reduce((x, p) => x + secimliBayt(p, secimAl(p.id, S)), 0))}</em>
                    </button>
                  )}
                  {(() => {
                    const sesli = inen.filter((p) => p.ek?.ses && secimAl(p.id, S).ses);
                    const sesB = sesli.reduce((x, p) => x + (p.ek?.ses?.b || 0), 0);
                    return sesli.length > 1 ? (
                      <button type="button" className="cv-btn" onClick={() => void secimDegistir(sesli.map((p) => p.id), { ses: false })}
                        title="Bu gruptaki indirilmiş derslerin seslerini sil; dersler sessiz çalışır">
                        <VolumeX aria-hidden="true" /> <span>Sesleri kaldır</span><em>{boyutYaz(sesB)}</em>
                      </button>
                    ) : null;
                  })()}
                  {inen.length > 1 && <GrupSil ids={inen.filter((p) => !p.zorunlu).map((p) => p.id)} />}
                </span>
              </div>
              {acik && (
                <ul className="cv-liste">
                  {ps.map((p) => (
                    <PaketSatiri key={p.id} p={p} durum={durumlar[p.id]} hata={S.hatalar[p.id]} oran={S.aktif?.id === p.id ? aktifOran : 0} />
                  ))}
                </ul>
              )}
            </section>
          );
        })
      )}

      {cihazSay > 0 && <AlanKarti />}

      <EsitlemeKarti />

      {cihazSay > 0 && (
        <section className="cv-kart cv-tehlike">
          <div>
            <b>Cihazdaki tüm içerik</b>
            <small>{cihazSay} paket · {boyutYaz(cihazBayt)}. Çözdüğün sorular ve ilerlemen silinmez; yalnız indirilen dersler kalkar.</small>
          </div>
          <GrupSil ids={Object.keys(S.kayitlar)} etiket="Tümünü sil" />
        </section>
      )}
    </div>
  );
}

function GrupSil({ ids, etiket = 'Sil' }: { ids: string[]; etiket?: string }) {
  const [onay, setOnay] = useState(false);
  useEffect(() => {
    if (!onay) return;
    const t = window.setTimeout(() => setOnay(false), 3500);
    return () => window.clearTimeout(t);
  }, [onay]);
  if (!ids.length) return null;
  return (
    <button type="button" className={`cv-btn is-sil${onay ? ' is-onay' : ''}`} onClick={() => (onay ? (setOnay(false), void paketSil(ids)) : setOnay(true))}>
      <Trash2 aria-hidden="true" /> <span>{onay ? `${ids.length} paket silinsin mi?` : etiket}</span>
    </button>
  );
}

const MODUL_AD: Record<Modul, string> = {
  uygulama: 'Uygulama dosyaları', sesli: 'Sesli dersler', cozucu: 'Soru çözücü', onem: 'En önemliler', alt: 'Alternatif çözücü',
  ogren: 'Etkileşimli dersler', veri: 'Başvuru verileri', db: 'Çıkmış sorular ve havuz',
};

/** Yer kullanımı: modül başına döküm, sesleri toplu kaldırma ve artık dosya temizliği */
function AlanKarti() {
  const S = useCevrimdisi();
  const dokum = useMemo(() => modulDokumu(S), [S]);
  const [sonuc, setSonuc] = useState<string | null>(null);
  const [calisiyor, setCalisiyor] = useState(false);
  const toplam = dokum.reduce((a, x) => a + x.bayt, 0) || 1;
  const sesliIds = Object.values(S.kayitlar).filter((k) => !k.yarim && k.dosyalar.some((d) => dosyaTuru(d.u) === 'ses')).map((k) => k.id)
    .filter((id) => S.katalog.find((p) => p.id === id)?.ek?.ses);
  const sesToplam = dokum.reduce((a, x) => a + (x.modul === 'sesli' ? 0 : x.ses), 0);
  return (
    <section className="cv-kart cv-alan-kart" aria-labelledby="cv-alan-b">
      <div className="cv-kart-bas"><h2 id="cv-alan-b">Cihazdaki yer</h2></div>
      <ul className="cv-dokum">
        {dokum.map((x) => (
          <li key={x.modul}>
            <span>{MODUL_AD[x.modul]}<small> · {x.n} paket{x.ses && x.modul !== 'sesli' ? ` · ses ${boyutYaz(x.ses)}` : ''}</small></span>
            <b>{boyutYaz(x.bayt)}</b>
            <span className="cv-cubuk"><i style={{ width: `${Math.max(2, (x.bayt / toplam) * 100)}%` }} /></span>
          </li>
        ))}
      </ul>
      <div className="cv-alan-eylem">
        {sesliIds.length > 0 && sesToplam > 0 && (
          <button type="button" className="cv-btn" onClick={() => void secimDegistir(sesliIds, { ses: false })}>
            <VolumeX aria-hidden="true" /> <span>Tüm sesleri kaldır</span><em>{boyutYaz(sesToplam)}</em>
          </button>
        )}
        <button type="button" className="cv-btn" disabled={calisiyor}
          onClick={async () => { setCalisiyor(true); const b = await yerAc().catch(() => 0); setCalisiyor(false); setSonuc(b ? `${boyutYaz(b)} artık dosya silindi.` : 'Silinecek artık dosya yok.'); }}>
          {calisiyor ? <Loader2 className="cv-don" aria-hidden="true" /> : <Sparkles aria-hidden="true" />} <span>Artık dosyaları temizle</span>
        </button>
      </div>
      {sonuc && <p className="cv-not" role="status">{sonuc}</p>}
      <p className="cv-not">Sesleri kaldırılan dersler internetsiz de açılır; ses yerine metin ve açıklamalar gösterilir.</p>
    </section>
  );
}
