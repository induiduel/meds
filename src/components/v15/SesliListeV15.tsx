import React, { useDeferredValue, useEffect, useMemo, useState } from 'react';
import { Archive, ArrowUpDown, Check, ChevronDown, ChevronRight, Download, ListMusic, Eraser, Headphones, RotateCcw, Search, X } from 'lucide-react';
import { TemizleDiyalog } from '../canliDers/CdIlerlemeTemizle';
import { cdCevrimdisiKayitlari, CD_CEVRIMDISI_DEGISTI } from '../canliDers/canliDersCevrimdisiKayit';
import { linkClick, navigateTo, pathFor } from '../../router';
import { icKonum } from '../../siteHaritasi';
import { KURUL_NOLAR, kurulKaydet, useSeciliKurul } from '../kurul/KurulSecici';
import { useV15Baslik } from './baslik';
import KurulSecV15 from './KurulSecV15';
import { cdSiraKaydet, cdSiraSecimi } from '../canliDers/canliDersKategori';
import { bransYolu, dersAdi, dersNumaralari, dersSirala, type DersSiraTur, dersSurumleri, dersYolu, hocaYaz, kurulBranslari, sureDk, useDersListesi, useIlerleme } from './dersVeri';
import SurumSecV15 from './SurumSecV15';
import { cdDersSesSurumu } from '../canliDers/canliDersStore';
import { Halka } from './Halka';
import { ListeEkleDugme, Listem, TopluEkleDugme } from '../canliDers/CanliDersListem';
import { useCdListe } from '../canliDers/canliDersListe';
import { dersCozucu } from '../canliDers/dersCozucu';
import { ClipboardCheck } from 'lucide-react';
import '../../styles/canli-ders.css';
import '../../styles/v15/dersler.css';
import '../../styles/v15/ogren.css';

/**
 * v15 · Sesli ders listesi (tasarım sistemi v15 › B04). Adres /dersler/canliders[/kurulN] (branşsız). Arama, durum
 * çipleri (Tümü · Yarım kalan · Bitti), branş bölümleri (ilerleme + "Tümü" → branş sayfası), satır → ders ayrıntısı.
 * Liste kendi alanında kayar; sayfa sabit. "2025-26 arşivi" çipi (?donem=2025-2026) geçen yılın kayıtlarını listeler;
 * arşiv dersleri ders ayrıntısında değil doğrudan oynatıcıda açılır (ayrıntı sayfası yalnız güncel dönemi bilir).
 */
type Durum = 'tum' | 'yeni' | 'yarim' | 'bitti' | 'indirilen' | 'liste';
/** "Yeni" = henüz hiç dinlemediğin (listede eklenme tarihi yok; uydurma tarih kullanılmaz) */
const DURUM: [Durum, string][] = [['tum', 'Tümü'], ['yeni', 'Yeni'], ['yarim', 'Yarım kalan'], ['bitti', 'Bitti'], ['indirilen', 'İndirilen']];
type Sira = DersSiraTur | 'son' | 'kisa';
const SIRA: [Sira, string][] = [['drive', 'Drive sırası'], ['program', 'Ders programı'], ['eklenme', 'Eklenme tarihi'], ['son', 'Son dinlenen'], ['kisa', 'Kısa olan önce']];
const ilkSira = (): Sira => { const v = cdSiraSecimi(); return SIRA.some(([id]) => id === v) ? (v as Sira) : 'drive'; };
const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

export default function SesliListeV15() {
  const kurul = useSeciliKurul();
  const [arsiv, setArsiv0] = useState(() => new URLSearchParams(icKonum().search).get('donem') === '2025-2026');
  const setArsiv = (a: boolean) => {
    setArsiv0(a);
    const sp = new URLSearchParams(location.search);
    if (a) sp.set('donem', '2025-2026'); else sp.delete('donem');
    const qs = sp.toString();
    try { history.replaceState(history.state, '', location.pathname + (qs ? `?${qs}` : '') + location.hash); } catch { /* yok */ }
  };
  const liste0 = useDersListesi(arsiv ? '2025-2026' : '2026-2027');
  const { dersler, hata } = liste0;
  const satirYolu = (key: string) => (arsiv ? pathFor('canli_ders', key) : dersYolu(key));
  const ilerleme = useIlerleme();
  const [ara, setAra] = useState('');
  const [araAcik, setAraAcik] = useState(false);
  const q = fold(useDeferredValue(ara).trim());
  const [durum, setDurum] = useState<Durum>(() => (location.hash === '#listem' ? 'liste' : 'tum'));
  const listeN = useCdListe((s) => s.keys.length);
  useEffect(() => {
    const f = () => { if (location.hash === '#listem') setDurum('liste'); };
    window.addEventListener('hashchange', f);
    return () => window.removeEventListener('hashchange', f);
  }, []);
  const [sira, setSiraHam] = useState<Sira>(ilkSira);
  const setSira = (v: Sira) => { setSiraHam(v); cdSiraKaydet(v); };
  // Numara ve temel sıra: Drive / ders programı / eklenme; "son"/"kısa" yalnız yeniden dizer, numara Drive'dan
  const numTur: DersSiraTur = sira === 'program' || sira === 'eklenme' ? sira : 'drive';
  const [indirilen, setIndirilen] = useState(() => cdCevrimdisiKayitlari());
  const [temizleAcik, setTemizleAcik] = useState(false);
  /** Açık ders satırı (akordeon): aynı anda tek ders açık */
  const [acik, setAcik] = useState<string | null>(null);
  useEffect(() => {
    const f = () => setIndirilen(cdCevrimdisiKayitlari());
    window.addEventListener(CD_CEVRIMDISI_DEGISTI, f);
    return () => window.removeEventListener(CD_CEVRIMDISI_DEGISTI, f);
  }, []);

  const branslar = useMemo(() => (dersler ? kurulBranslari(dersler, kurul) : []), [dersler, kurul]);
  const toplam = branslar.reduce((n, b) => n + b.dersler.length, 0);
  const gruplar = useMemo(
    () =>
      branslar
        .map((b) => ({
          ...b,
          numara: dersNumaralari(b.dersler, numTur),
          liste: dersSirala(b.dersler, numTur).filter((d) => {
            const i = ilerleme(d);
            if (durum === 'yeni' && (i.bitti || i.t != null)) return false;
            if (durum === 'indirilen' && !indirilen[d.key]) return false;
            if (durum === 'yarim' && !(i.t != null && (!i.bitti || i.tekrar))) return false;
            if (durum === 'bitti' && !i.bitti) return false;
            return !q || fold(`${d.no} ${d.baslik} ${b.ad} ${d.hoca || ''}`).includes(q);
          }).sort((a, c) => (sira === 'son' ? ilerleme(c).at - ilerleme(a).at : sira === 'kisa' ? (ilerleme(a).sure || 1e9) - (ilerleme(c).sure || 1e9) : 0)),
          biten: b.dersler.filter((d) => ilerleme(d).bitti).length,
        }))
        .filter((g) => g.liste.length),
    [branslar, durum, q, ilerleme, sira, numTur, indirilen],
  );
  useV15Baslik({ baslik: arsiv ? 'Sesli dersler · Arşiv' : 'Sesli dersler', alt: `${arsiv ? '2025-2026 · ' : ''}Kurul ${kurul}${dersler ? ` · ${toplam} ders` : ''}` });

  return (
    <div className="b15 sl15">
      <h1 className="sr-only">Sesli dersler</h1>
      <div className="o15-ust">
        {araAcik ? (
          <label className="o15-ara">
            <Search aria-hidden />
            <input autoFocus type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Ders, branş ya da hoca ara" aria-label="Sesli derslerde ara" />
            <button type="button" className="v15-ib" onClick={() => { setAra(''); setAraAcik(false); }} aria-label="Aramayı kapat"><X aria-hidden /></button>
          </label>
        ) : (
          <div className="o15-cipler v15-hscroll" role="toolbar" aria-label="Süzgeç">
            <KurulSecV15 kurul={kurul} onSec={(k) => navigateTo(`/dersler/canliders/kurul${k}${arsiv ? '?donem=2025-2026' : ''}`)} />
            {/* tasarım L06: dönem seçici (bu yıl · geçen yılın arşivi)
                H158: "2026–27 / 2025–26" telefonda süzgeç satırını taşırıp sıralama simgesinin altına kesiliyordu; kısa ad + yıl ipucu */}
            <div className="v15-seg sl15-donem" role="radiogroup" aria-label="Dönem">
              <button type="button" role="radio" aria-checked={!arsiv} aria-current={!arsiv ? 'page' : undefined} onClick={() => setArsiv(false)} title="Bu yılın (2026-2027) sesli dersleri">Bu yıl</button>
              <button type="button" role="radio" aria-checked={arsiv} aria-current={arsiv ? 'page' : undefined} onClick={() => setArsiv(true)} title="Geçen yılın (2025-2026) sesli dersleri"><Archive aria-hidden />Arşiv</button>
            </div>
            <button type="button" className={`o15-cip sl15-liste-cip${durum === 'liste' ? ' is-on' : ''}`} aria-pressed={durum === 'liste'} onClick={() => setDurum('liste')} title="Oynatma listelerim">
              <ListMusic aria-hidden />Listem{listeN ? ` (${listeN})` : ''}
            </button>
            {DURUM.map(([id, t]) => (
              <button key={id} type="button" className={`o15-cip${durum === id ? ' is-on' : ''}`} aria-pressed={durum === id} onClick={() => setDurum(id)}>{t}</button>
            ))}
          </div>
        )}
        {!araAcik && (
          <label className="v15-ib sl15-sira" title={`Sıralama: ${SIRA.find((x) => x[0] === sira)![1]}`}>
            <ArrowUpDown aria-hidden />
            <select value={sira} onChange={(e) => setSira(e.target.value as Sira)} aria-label="Sıralama">
              {SIRA.map(([id, t]) => <option key={id} value={id}>{t}</option>)}
            </select>
          </label>
        )}
        {!araAcik && <button type="button" className="v15-ib" onClick={() => setAraAcik(true)} aria-label="Ara"><Search aria-hidden /></button>}
      </div>

      {arsiv && (
        <p className="sl15-not v15-card"><Archive aria-hidden /><span><b>Geçen yılın arşivi.</b> 2025-2026 kayıtları; bu yılın programı ve hocası farklı olabilir.</span>
          <button type="button" onClick={() => setArsiv(false)}>Bu yıla dön</button></p>
      )}
      <div className="sl15-alan">
        {dersler === null ? (
          <span className="v15-skel b15-skel" aria-hidden />
        ) : durum === 'liste' ? (
          <div className="sl15-listem"><Listem dersler={dersler} onTumu={() => setDurum('tum')} /></div>
        ) : gruplar.length ? (
          gruplar.map((g) => (
            <section key={g.ad} className="sl15-grup" aria-label={g.kisa}>
              <div className="sl15-bas-sat">
              <a className="sl15-bas" href={bransYolu(kurul, g.ad)} onClick={linkClick(() => navigateTo(bransYolu(kurul, g.ad)))} {...(arsiv ? { onClick: (e: React.MouseEvent) => e.preventDefault(), 'aria-disabled': true, tabIndex: -1 } : {})}>
                <b>{g.kisa}</b>
                <span className="v15-cap">{g.biten}/{g.dersler.length} bitti</span>
                <span className="v15-bar sl15-bar" aria-hidden><span style={{ width: `${g.dersler.length ? (g.biten / g.dersler.length) * 100 : 0}%` }} /></span>
                <ChevronRight className="v15-chev" aria-hidden />
              </a>
              <TopluEkleDugme keys={g.liste.map((d) => d.key)} ad={g.kisa} />
              </div>
              <ul className="b15-list v15-card" role="list">
                {g.liste.map((d) => {
                  const i = ilerleme(d);
                  return (
                    <li key={d.key} className="sl15-li">
                      <a className="b15-row" href={satirYolu(d.key)} onClick={linkClick(() => navigateTo(satirYolu(d.key)))}>
                        <span className={`v15-tile ${i.tekrar ? 'is-tekrar' : i.bitti ? 'is-ok' : i.t != null ? '' : 'is-n'}`}>{i.tekrar ? <RotateCcw aria-hidden /> : i.bitti ? <Check aria-hidden /> : <Headphones aria-hidden />}</span>
                        <span className="b15-row-t">
                          <b>{dersAdi(d, g.numara.get(d.key))}{indirilen[d.key] && <Download className="sl15-indi" aria-label="İndirildi" />}</b>
                          <span>{i.tekrar && <em className="sl15-tekrar">{i.tur > 0 ? `${i.tur + 1}. tekrar` : 'Tekrarda'} · %{i.pct}</em>}{[hocaYaz(d.hoca), sureDk(dersSurumleri(d.key, liste0).find((x) => x.yeni)?.sureSn || i.sure)].filter(Boolean).join(' · ')}</span>
                        </span>
                        <Halka pct={i.pct} etiket={i.tekrar ? `Tekrar: %${i.pct} dinlendi` : i.bitti ? 'Bitti' : `%${i.pct} dinlendi`} />
                      </a>
                      <button type="button" className={`v15-ib sl15-ac${acik === d.key ? ' is-acik' : ''}`} aria-expanded={acik === d.key}
                        aria-label={acik === d.key ? 'Ders seçeneklerini kapat' : 'Ders seçeneklerini aç'} onClick={() => setAcik((a) => (a === d.key ? null : d.key))}>
                        <ChevronDown aria-hidden />
                      </button>
                      <ListeEkleDugme dersKey={d.key} baslik={d.baslik} />
                      <SurumSecV15 surumler={dersSurumleri(d.key, liste0)}
                        aktif={dersSurumleri(d.key, liste0).find((s) => s.vid && cdDersSesSurumu(s.key) === s.vid) || dersSurumleri(d.key, liste0).find((s) => s.yeni)} />
                      {acik === d.key && (() => {
                        const c = dersCozucu(d.baslik, d.key);
                        const url = c ? `${c.url}&dk=${encodeURIComponent(d.key)}` : null;
                        return (
                          <div className="sl15-panel">
                            {url ? (
                              <a className="v15-btn is-soft" href={url} onClick={linkClick(() => navigateTo(url))}>
                                <ClipboardCheck aria-hidden />Sesli check-up · {c!.soru} soru
                              </a>
                            ) : <span className="v15-cap">Bu ders için check-up soruları henüz hazır değil.</span>}
                            <small className="v15-cap">Örnek ve çıkmış sorular sesli çözülür; yanlışlarının açıklamasını görüp dersin ilgili bölümünü dinleyebilirsin.</small>
                          </div>
                        );
                      })()}
                    </li>
                  );
                })}
              </ul>
            </section>
          ))
        ) : (
          <p className={`b15-bos v15-card${hata ? ' is-hata' : ''}`}>{hata ? <><b>Ders listesi alınamadı</b><span>{hata}</span><button type="button" className="v15-btn is-soft" onClick={() => location.reload()}>Yeniden dene</button></> : q || durum !== 'tum' ? 'Bu süzgeçte ders yok.' : arsiv ? `2025-2026 arşivinde Kurul ${kurul} dersi yok.` : <>
            {/* H158: boş listede geçen yılın kayıtlarına geçiren eylem */}
            <span>Kurul {kurul} için bu yıl sesli ders henüz yok.</span>
            <button type="button" className="v15-btn is-soft" onClick={() => setArsiv(true)}><Archive aria-hidden />Geçen yılın derslerini aç</button>
          </>}</p>
        )}
        {toplam > 0 && (
          <p className="sl15-temizlik">
            <button type="button" className="v15-btn is-ghost" onClick={() => setTemizleAcik(true)} title="Bu cihazdaki kaldığın yer kayıtlarını ve bitti işaretlerini sil; derslere sıfırdan başla">
              <Eraser aria-hidden />İlerlemeyi temizle
            </button>
            <span>Yalnız bu cihazdaki kayıtlar silinir; ses dosyaları ve listen kalır.</span>
          </p>
        )}
      </div>
      {temizleAcik && <TemizleDiyalog keys={branslar.flatMap((b) => b.dersler.map((d) => d.key))} onKapat={() => setTemizleAcik(false)} />}
    </div>
  );
}
