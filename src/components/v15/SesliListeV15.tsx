import React, { useDeferredValue, useEffect, useMemo, useState } from 'react';
import { Archive, ArrowUpDown, Check, ChevronDown, ChevronRight, Download, Headphones, RotateCcw, Search, X } from 'lucide-react';
import { cdCevrimdisiKayitlari, CD_CEVRIMDISI_DEGISTI } from '../canliDers/canliDersCevrimdisiKayit';
import { linkClick, navigateTo, pathFor } from '../../router';
import { icKonum } from '../../siteHaritasi';
import { KURUL_NOLAR, kurulKaydet, useSeciliKurul } from '../kurul/KurulSecici';
import { useV15Baslik } from './baslik';
import KurulSecV15 from './KurulSecV15';
import { bransYolu, dersAdi, dersSirala, dersYolu, hocaYaz, kurulBranslari, sureDk, useDersListesi, useIlerleme } from './dersVeri';
import { Halka } from './Halka';
import '../../styles/v15/dersler.css';
import '../../styles/v15/ogren.css';

/**
 * v15 · Sesli ders listesi (tasarım sistemi v15 › B04). Adres /dersler/canliders[/kurulN] (branşsız). Arama, durum
 * çipleri (Tümü · Yarım kalan · Bitti), branş bölümleri (ilerleme + "Tümü" → branş sayfası), satır → ders ayrıntısı.
 * Liste kendi alanında kayar; sayfa sabit. "2025-26 arşivi" çipi (?donem=2025-2026) geçen yılın kayıtlarını listeler;
 * arşiv dersleri ders ayrıntısında değil doğrudan oynatıcıda açılır (ayrıntı sayfası yalnız güncel dönemi bilir).
 */
type Durum = 'tum' | 'yeni' | 'yarim' | 'bitti' | 'indirilen';
/** "Yeni" = henüz hiç dinlemediğin (listede eklenme tarihi yok; uydurma tarih kullanılmaz) */
const DURUM: [Durum, string][] = [['tum', 'Tümü'], ['yeni', 'Yeni'], ['yarim', 'Yarım kalan'], ['bitti', 'Bitti'], ['indirilen', 'İndirilen']];
type Sira = 'sira' | 'son' | 'kisa';
const SIRA: [Sira, string][] = [['sira', 'Ders sırası'], ['son', 'Son dinlenen'], ['kisa', 'Kısa olan önce']];
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
  const { dersler, hata } = useDersListesi(arsiv ? '2025-2026' : '2026-2027');
  const satirYolu = (key: string) => (arsiv ? pathFor('canli_ders', key) : dersYolu(key));
  const ilerleme = useIlerleme();
  const [ara, setAra] = useState('');
  const [araAcik, setAraAcik] = useState(false);
  const q = fold(useDeferredValue(ara).trim());
  const [durum, setDurum] = useState<Durum>('tum');
  const [sira, setSira] = useState<Sira>('sira');
  const [indirilen, setIndirilen] = useState(() => cdCevrimdisiKayitlari());
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
          liste: dersSirala(b.dersler).filter((d) => {
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
    [branslar, durum, q, ilerleme, sira, indirilen],
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
        ) : gruplar.length ? (
          gruplar.map((g) => (
            <section key={g.ad} className="sl15-grup" aria-label={g.kisa}>
              <a className="sl15-bas" href={bransYolu(kurul, g.ad)} onClick={linkClick(() => navigateTo(bransYolu(kurul, g.ad)))} {...(arsiv ? { onClick: (e: React.MouseEvent) => e.preventDefault(), 'aria-disabled': true, tabIndex: -1 } : {})}>
                <b>{g.kisa}</b>
                <span className="v15-cap">{g.biten}/{g.dersler.length} bitti</span>
                <span className="v15-bar sl15-bar" aria-hidden><span style={{ width: `${g.dersler.length ? (g.biten / g.dersler.length) * 100 : 0}%` }} /></span>
                <ChevronRight className="v15-chev" aria-hidden />
              </a>
              <ul className="b15-list v15-card" role="list">
                {g.liste.map((d) => {
                  const i = ilerleme(d);
                  return (
                    <li key={d.key}>
                      <a className="b15-row" href={satirYolu(d.key)} onClick={linkClick(() => navigateTo(satirYolu(d.key)))}>
                        <span className={`v15-tile ${i.tekrar ? 'is-tekrar' : i.bitti ? 'is-ok' : i.t != null ? '' : 'is-n'}`}>{i.tekrar ? <RotateCcw aria-hidden /> : i.bitti ? <Check aria-hidden /> : <Headphones aria-hidden />}</span>
                        <span className="b15-row-t">
                          <b>{dersAdi(d)}{indirilen[d.key] && <Download className="sl15-indi" aria-label="İndirildi" />}</b>
                          <span>{i.tekrar && <em className="sl15-tekrar">{i.tur > 0 ? `${i.tur + 1}. tekrar` : 'Tekrarda'} · %{i.pct}</em>}{[hocaYaz(d.hoca), sureDk(i.sure)].filter(Boolean).join(' · ')}</span>
                        </span>
                        <Halka pct={i.pct} etiket={i.tekrar ? `Tekrar: %${i.pct} dinlendi` : i.bitti ? 'Bitti' : `%${i.pct} dinlendi`} />
                      </a>
                      {!!d.surumlar?.length && (
                        <span className="sl15-surum" role="group" aria-label="Sürüm">
                          {[d.key, ...d.surumlar].map((k, n) => (
                            <a key={k} href={satirYolu(k)} onClick={linkClick(() => navigateTo(satirYolu(k)))}>V{n + 1}</a>
                          ))}
                        </span>
                      )}
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
      </div>
    </div>
  );
}
