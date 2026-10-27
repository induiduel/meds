/**
 * Çevrimdışı › İndirilebilir: kurul + dönem seçici, arama, branş ve durum süzgeci; her ders tek kart, tek düğmeyle iner
 * (sesli ders, ders paketi, etkileşimli ders, soru çözücü, en önemliler, alternatif çözücü birlikte). Soru bankası ve başvuru
 * verileri ayrı kartlar. "Toplu indir" ile branş × içerik × ses/PDF seçip tek seferde indirilir.
 */
import { useEffect, useMemo, useState } from 'react';
import { Check, CloudDownload, Database, Download, Layers, Loader2, RefreshCw, Search, X } from 'lucide-react';
import {
  cevrimdisiModuAc, kuyrugaEkle, kuyruktanCikar, paketDurumu, secimliBayt, useCevrimdisi, secimAl, type Modul, type Paket, type Secim,
} from '../../services/cevrimdisi/paketMotoru';
import { birimDurumu, boyutYaz, dersBirimleri, katla, UYE_AD, UYE_SIRA, type BirimDurum, type DersBirimi } from '../../services/cevrimdisi/dersBirimleri';
import { aktifKurul } from '../../services/kurulTakvimi';
import { DURUM_AD, DURUM_TON } from './cvOrtak';

type Donem = 'hepsi' | 'guncel' | 'arsiv';
const DONEM_AD: Record<Donem, string> = { hepsi: 'Hepsi', guncel: 'Güncel 2026-27', arsiv: 'Arşiv 2025-26' };
type Suz = 'tum' | 'yok' | 'kismi' | 'guncelleme' | 'tam';
const SUZ_AD: Record<Suz, string> = { tum: 'Tüm durumlar', yok: 'İndirilmedi', kismi: 'Yarım kalan', guncelleme: 'Güncelleme var', tam: 'Cihazda' };
const SUZ_KEY = 'medsoru_cv_suzgec_v1';
const SAYFA = 24;

/** Kurul: 0 = tümü, -1 = kurula bağlı olmayan. Seçim yalnız aynı aktif kurulda hatırlanır. */
function suzOku(): { kurul: number; donem: Donem } {
  const aktif = aktifKurul().kurul;
  try {
    const v = JSON.parse(localStorage.getItem(SUZ_KEY) || 'null');
    if (v && v.aktif === aktif) return { kurul: Number(v.kurul) || 0, donem: ['hepsi', 'guncel', 'arsiv'].includes(v.donem) ? v.donem : 'hepsi' };
  } catch { /* depo yok */ }
  return { kurul: aktif, donem: 'hepsi' };
}

export default function Indirilebilir({ topluAcik, setTopluAcik }: { topluAcik: boolean; setTopluAcik: (v: boolean) => void }) {
  const S = useCevrimdisi();
  const birimler = useMemo(() => dersBirimleri(S.katalog), [S.katalog]);
  const [{ kurul, donem }, setKd] = useState(suzOku);
  const [ara, setAra] = useState('');
  const [grup, setGrup] = useState('');
  const [suz, setSuz] = useState<Suz>('tum');
  const [limit, setLimit] = useState(SAYFA);
  const aktifNo = aktifKurul().kurul;
  useEffect(() => { try { localStorage.setItem(SUZ_KEY, JSON.stringify({ aktif: aktifNo, kurul, donem })); } catch { /* depo yok */ } }, [kurul, donem, aktifNo]);
  useEffect(() => { setLimit(SAYFA); setGrup(''); }, [kurul, donem]);
  useEffect(() => { setLimit(SAYFA); }, [ara, grup, suz]);

  const donemde = useMemo(() => birimler.filter((b) => donem === 'hepsi' || (donem === 'arsiv' ? b.donem === '2025-2026' : b.donem !== '2025-2026')), [birimler, donem]);
  const kurulSay = useMemo(() => { const m = new Map<number, number>(); donemde.forEach((b) => m.set(b.kurul || -1, (m.get(b.kurul || -1) || 0) + 1)); return m; }, [donemde]);
  const kurulda = useMemo(() => donemde.filter((b) => (kurul === -1 ? !b.kurul : kurul === 0 || b.kurul === kurul)), [donemde, kurul]);
  const branslar = useMemo(() => { const m = new Map<string, number>(); kurulda.forEach((b) => m.set(b.grup, (m.get(b.grup) || 0) + 1)); return [...m.entries()].sort((a, b) => b[1] - a[1]); }, [kurulda]);
  const durumlar = useMemo(() => new Map(birimler.map((b) => [b.id, birimDurumu(b, S)])), [birimler, S]);
  const liste = useMemo(() => {
    const q = katla(ara.trim());
    return kurulda.filter((b) => {
      if (grup && b.grup !== grup) return false;
      if (q && !katla(`${b.baslik} ${b.grup}`).includes(q)) return false;
      const d = durumlar.get(b.id)!.durum;
      if (suz === 'tam') return d === 'tam';
      if (suz === 'kismi') return d === 'kismi' || d === 'iniyor';
      if (suz === 'yok') return d === 'yok' || d === 'hata';
      if (suz === 'guncelleme') return d === 'guncelleme';
      return true;
    });
  }, [kurulda, ara, grup, suz, durumlar]);
  const diger = useMemo(() => S.katalog.filter((p) => p.modul === 'db' || p.modul === 'veri').sort((a, b) => a.sira - b.sira), [S.katalog]);

  if (!S.hazir || (!S.katalog.length && !S.katalogHata)) {
    return <div className="cv15-bos v15-card"><Loader2 className="cv15-don" aria-hidden /> <span className="v15-cap">Paketler yükleniyor…</span></div>;
  }

  return (
    <div className="cv15-yigin">
      {topluAcik ? <TopluIndir katalog={S.katalog} kapat={() => setTopluAcik(false)} /> : (
        <button type="button" className="cv15-toplu-ac v15-card" onClick={() => setTopluAcik(true)}>
          <span className="v15-tile"><Layers aria-hidden /></span>
          <span><b>Toplu indir</b><span className="v15-cap">Branş ve içerik seçip tek seferde indir</span></span>
        </button>
      )}

      <div className="cv15-suz">
        <div className="cv15-kurul v15-hscroll" role="group" aria-label="Kurul">
          <button type="button" className={`cv15-cip${kurul === 0 ? ' is-on' : ''}`} aria-pressed={kurul === 0} onClick={() => setKd({ kurul: 0, donem })}>Tümü <small>{donemde.length}</small></button>
          {[1, 2, 3, 4, 5, 6].map((n) => (
            <button key={n} type="button" className={`cv15-cip${kurul === n ? ' is-on' : ''}`} aria-pressed={kurul === n}
              disabled={!kurulSay.get(n) && kurul !== n} onClick={() => setKd({ kurul: n, donem })}>
              Kurul {n}{n === aktifNo ? ' · şimdi' : ''} <small>{kurulSay.get(n) || 0}</small>
            </button>
          ))}
          {!!kurulSay.get(-1) && <button type="button" className={`cv15-cip${kurul === -1 ? ' is-on' : ''}`} aria-pressed={kurul === -1} onClick={() => setKd({ kurul: -1, donem })}>Kurulsuz <small>{kurulSay.get(-1)}</small></button>}
        </div>
        <div className="v15-seg cv15-donem" role="group" aria-label="Dönem">
          {(Object.keys(DONEM_AD) as Donem[]).map((d) => (
            <button key={d} type="button" aria-pressed={donem === d} aria-current={donem === d ? 'page' : undefined} onClick={() => setKd({ kurul, donem: d })}>{DONEM_AD[d]}</button>
          ))}
        </div>
        <div className="cv15-suz-sira">
          <label className="cv15-ara">
            <Search aria-hidden />
            <input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Ders ara" aria-label="Ders ara" />
            {ara && <button type="button" onClick={() => setAra('')} aria-label="Aramayı temizle"><X aria-hidden /></button>}
          </label>
          <select className="cv15-sec" value={grup} onChange={(e) => setGrup(e.target.value)} aria-label="Branş">
            <option value="">Tüm branşlar</option>
            {branslar.map(([g, n]) => <option key={g} value={g}>{g} ({n})</option>)}
          </select>
          <select className="cv15-sec" value={suz} onChange={(e) => setSuz(e.target.value as Suz)} aria-label="Durum">
            {(Object.keys(SUZ_AD) as Suz[]).map((s) => <option key={s} value={s}>{SUZ_AD[s]}</option>)}
          </select>
        </div>
      </div>

      {!liste.length ? (
        <div className="cv15-bos v15-card">
          <b>Bu seçimde ders yok</b>
          <span className="v15-cap">{kurul > 0 ? `Kurul ${kurul}` : 'Seçili kurullar'} için {donem === 'hepsi' ? '' : `${DONEM_AD[donem].toLocaleLowerCase('tr-TR')} döneminde `}eşleşen paket bulunamadı.</span>
          <span className="cv15-arac">
            {donem !== 'hepsi' && <button type="button" className="cv15-b" onClick={() => setKd({ kurul, donem: 'hepsi' })}>Tüm dönemler</button>}
            {kurul !== 0 && <button type="button" className="cv15-b" onClick={() => setKd({ kurul: 0, donem })}>Tüm kurullar</button>}
            {(ara || suz !== 'tum' || grup) && <button type="button" className="cv15-b" onClick={() => { setAra(''); setSuz('tum'); setGrup(''); }}>Süzgeci sıfırla</button>}
          </span>
        </div>
      ) : (
        <>
          <p className="v15-cap cv15-say">{liste.length} ders</p>
          <ul className="cv15-kartlar">
            {liste.slice(0, limit).map((b) => <DersKarti key={b.id} b={b} d={durumlar.get(b.id)!} />)}
          </ul>
          {liste.length > limit && <button type="button" className="v15-btn is-ghost cv15-daha" onClick={() => setLimit(limit + SAYFA)}>Daha fazla göster ({liste.length - limit})</button>}
        </>
      )}

      {diger.length > 0 && (
        <section aria-labelledby="cv15-diger" className="cv15-yigin">
          <h3 id="cv15-diger" className="v15-label">Soru bankası ve başvuru</h3>
          <ul className="cv15-kartlar">{diger.map((p) => <PaketKarti key={p.id} p={p} />)}</ul>
        </section>
      )}
    </div>
  );
}

/** Tek düğme durum makinesi: İndir → İniyor (çubuk + iptal) → Cihazda; güncelleme/eksik/hata durumları */
function IndirDugmesi({ ids, durum, kalan, oran, ad }: { ids: { eksik: string[]; gun: string[]; inen: string[] }; durum: BirimDurum; kalan: number; oran: number | null; ad: string }) {
  if (durum === 'iniyor') {
    return (
      <div className="cv15-iniyor">
        <span className="v15-bar" role="progressbar" aria-label={`${ad} indiriliyor`} aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round((oran || 0) * 100)}>
          <span style={{ width: `${Math.round((oran || 0) * 100)}%` }} />
        </span>
        <span className="v15-cap">{oran === null ? 'Sırada' : `%${Math.round(oran * 100)}`}</span>
        <button type="button" className="cv15-b is-ikon" onClick={() => kuyruktanCikar(ids.inen)} aria-label={`${ad} indirmesini iptal et`} title="İptal"><X aria-hidden /></button>
      </div>
    );
  }
  if (durum === 'tam') return <span className="cv15-tamam"><Check aria-hidden /> Cihazda</span>;
  const gun = durum === 'guncelleme';
  return (
    <button type="button" className="v15-btn cv15-indir" onClick={() => { if (ids.eksik.length) kuyrugaEkle(ids.eksik); if (ids.gun.length) kuyrugaEkle(ids.gun, true); }}>
      {gun ? <RefreshCw aria-hidden /> : <Download aria-hidden />}
      {gun ? 'Güncelle' : durum === 'kismi' ? 'Eksikleri indir' : durum === 'hata' ? 'Yeniden dene' : 'İndir'}
      <small>{boyutYaz(kalan)}</small>
    </button>
  );
}

function DersKarti({ b, d }: { b: DersBirimi; d: ReturnType<typeof birimDurumu> }) {
  const S = useCevrimdisi();
  const ids = {
    eksik: b.uyeler.filter((u) => ['yok', 'hata'].includes(paketDurumu(u.id, S))).map((u) => u.id),
    gun: b.uyeler.filter((u) => paketDurumu(u.id, S) === 'guncelleme').map((u) => u.id),
    inen: b.uyeler.filter((u) => ['kuyrukta', 'iniyor'].includes(paketDurumu(u.id, S))).map((u) => u.id),
  };
  const aktifUye = S.aktif && b.uyeler.find((u) => u.id === S.aktif!.id);
  // Ders ilerlemesi: biten üyeler + süren üyenin oranı
  const oran = d.durum === 'iniyor'
    ? (aktifUye ? (d.tamam + (S.aktif!.toplam ? S.aktif!.alinan / S.aktif!.toplam : 0)) / d.toplam : null)
    : null;
  const moduller = UYE_SIRA.filter((m) => b.uyeler.some((u) => u.modul === m));
  const hata = b.uyeler.map((u) => S.hatalar[u.id]).find(Boolean);
  return (
    <li className={`cv15-kart v15-card is-${d.durum}`}>
      <div className="cv15-kart-ust">
        <span className="v15-cap">{b.grup}{b.kurul ? ` · K${b.kurul}` : ''}{b.donem === '2025-2026' ? ' · arşiv' : ''}</span>
        {d.durum !== 'yok' && <span className={`v15-tag ${DURUM_TON[d.durum]}`}>{DURUM_AD[d.durum]}</span>}
      </div>
      <b className="cv15-kart-ad" title={b.baslik}>{b.no ? `${b.no}. ` : ''}{b.baslik}</b>
      <span className="v15-cap cv15-kart-moduller">{moduller.map((m) => UYE_AD[m]).join(' · ')}</span>
      {hata && d.durum === 'hata' && <span className="v15-cap cv15-kotu">{hata}</span>}
      <div className="cv15-kart-alt">
        <span className="v15-cap">{d.tamam}/{d.toplam} bölüm · {boyutYaz(d.toplamBayt)}</span>
        <IndirDugmesi ids={ids} durum={d.durum} kalan={d.kalanBayt} oran={oran} ad={b.baslik} />
      </div>
    </li>
  );
}

function PaketKarti({ p }: { p: Paket }) {
  const S = useCevrimdisi();
  const pd = paketDurumu(p.id, S);
  const durum: BirimDurum = pd === 'tamam' ? 'tam' : pd === 'kuyrukta' || pd === 'iniyor' ? 'iniyor' : pd === 'guncelleme' ? 'guncelleme' : pd === 'hata' ? 'hata' : 'yok';
  const oran = pd === 'iniyor' && S.aktif?.id === p.id && S.aktif.toplam ? S.aktif.alinan / S.aktif.toplam : null;
  const bayt = secimliBayt(p, secimAl(p.id, S));
  return (
    <li className={`cv15-kart v15-card is-${durum}`}>
      <div className="cv15-kart-ust">
        <span className="v15-cap"><Database aria-hidden className="cv15-mini" /> {p.grup}</span>
        {durum !== 'yok' && <span className={`v15-tag ${DURUM_TON[durum]}`}>{DURUM_AD[durum]}</span>}
      </div>
      <b className="cv15-kart-ad" title={p.baslik}>{p.baslik}</b>
      <span className="v15-cap cv15-kart-moduller">{p.alt || ''}</span>
      {pd === 'hata' && S.hatalar[p.id] && <span className="v15-cap cv15-kotu">{S.hatalar[p.id]}</span>}
      <div className="cv15-kart-alt">
        <span className="v15-cap">{boyutYaz(pd === 'tamam' || pd === 'guncelleme' ? S.kayitlar[p.id]?.bayt || bayt : bayt)}</span>
        <IndirDugmesi ids={{ eksik: pd === 'yok' || pd === 'hata' ? [p.id] : [], gun: pd === 'guncelleme' ? [p.id] : [], inen: [p.id] }} durum={durum} kalan={bayt} oran={oran} ad={p.baslik} />
      </div>
    </li>
  );
}

/* ---------------------------------------------------------------- toplu indirme ---------------------------------------------------------------- */
const MODS: { id: Modul; ad: string }[] = [
  { id: 'sesli', ad: 'Sesli dersler' }, { id: 'medspak', ad: 'Ders paketi' }, { id: 'ogren', ad: 'Etkileşimli dersler' },
  { id: 'cozucu', ad: 'Soru çözücü' }, { id: 'onem', ad: 'En önemliler' }, { id: 'alt', ad: 'Alternatif çözücü' },
  { id: 'db', ad: 'Çıkmış sorular ve havuz' }, { id: 'veri', ad: 'Sözlük, özetler, notlar' },
];

function TopluIndir({ katalog, kapat }: { katalog: Paket[]; kapat: () => void }) {
  const ayar = useCevrimdisi().ayar;
  const gruplar = useMemo(() => {
    const m = new Map<string, number>();
    for (const p of katalog) if (['sesli', 'cozucu', 'onem', 'alt'].includes(p.modul)) m.set(p.grup, (m.get(p.grup) || 0) + 1);
    return [...m.entries()].sort((a, b) => b[1] - a[1]).map(([g]) => g);
  }, [katalog]);
  const [grupSec, setGrupSec] = useState<string[]>([]);
  const [modulSec, setModulSec] = useState<Modul[]>(['sesli', 'medspak', 'ogren', 'cozucu', 'onem', 'db']);
  const [secim, setSecim] = useState<Secim>({ ses: ayar.ses, pdf: ayar.pdf });
  useEffect(() => { if (!grupSec.length && gruplar.length) setGrupSec(gruplar.slice(0, 1)); }, [gruplar]); // eslint-disable-line react-hooks/exhaustive-deps
  const ac = <T,>(arr: T[], x: T) => (arr.includes(x) ? arr.filter((y) => y !== x) : [...arr, x]);
  const secilen = katalog.filter((p) => modulSec.includes(p.modul) && (p.modul === 'db' || p.modul === 'veri' || grupSec.includes(p.grup)));
  const eksik = secilen.filter((p) => paketDurumu(p.id) !== 'tamam');
  const bayt = eksik.reduce((a, p) => a + secimliBayt(p, secim), 0);
  const sesB = eksik.reduce((a, p) => a + (p.ek?.ses?.b || 0), 0);
  const pdfB = eksik.reduce((a, p) => a + (p.ek?.pdf?.b || 0), 0);
  return (
    <section className="cv15-toplu v15-card" aria-labelledby="cv15-toplu-b">
      <header className="cv15-grup-bas">
        <span className="cv15-grup-ad"><b id="cv15-toplu-b">Toplu indir</b><span className="v15-cap">Seçtiklerin arka planda iner; sonra tek tek silebilirsin.</span></span>
        <button type="button" className="cv15-b is-ikon" onClick={kapat} aria-label="Toplu indirmeyi kapat"><X aria-hidden /></button>
      </header>
      <fieldset className="cv15-alan"><legend className="v15-label">Branşlar</legend>
        <div className="cv15-cipler">{gruplar.map((g) => <button key={g} type="button" className={`cv15-cip${grupSec.includes(g) ? ' is-on' : ''}`} aria-pressed={grupSec.includes(g)} onClick={() => setGrupSec(ac(grupSec, g))}>{g}</button>)}</div>
      </fieldset>
      <fieldset className="cv15-alan"><legend className="v15-label">İçerik</legend>
        <div className="cv15-cipler">{MODS.map((m) => <button key={m.id} type="button" className={`cv15-cip${modulSec.includes(m.id) ? ' is-on' : ''}`} aria-pressed={modulSec.includes(m.id)} onClick={() => setModulSec(ac(modulSec, m.id))}>{m.ad}</button>)}</div>
      </fieldset>
      <fieldset className="cv15-alan"><legend className="v15-label">Ek dosyalar</legend>
        <div className="cv15-cipler">
          <button type="button" className={`cv15-cip${secim.ses ? ' is-on' : ''}`} aria-pressed={secim.ses} onClick={() => setSecim({ ...secim, ses: !secim.ses })}>{secim.ses ? 'Sesler dahil' : 'Sessiz'}{sesB ? ` · ${boyutYaz(sesB)}` : ''}</button>
          <button type="button" className={`cv15-cip${secim.pdf ? ' is-on' : ''}`} aria-pressed={secim.pdf} onClick={() => setSecim({ ...secim, pdf: !secim.pdf })}>{secim.pdf ? "PDF'ler dahil" : 'PDF yok'}{pdfB ? ` · ${boyutYaz(pdfB)}` : ''}</button>
        </div>
        <span className="v15-cap">Sessiz inen dersler metin, soru ve açıklamalarla tam çalışır; sesi sonra ekleyebilirsin.</span>
      </fieldset>
      <div className="cv15-toplu-alt">
        <span className="v15-cap"><b>{eksik.length}</b> paket · yaklaşık <b>{boyutYaz(bayt)}</b></span>
        <button type="button" className="v15-btn" disabled={!eksik.length} onClick={() => { cevrimdisiModuAc(eksik.map((p) => p.id), secim); kapat(); }}>
          <CloudDownload aria-hidden /> İndirmeyi başlat
        </button>
      </div>
    </section>
  );
}
