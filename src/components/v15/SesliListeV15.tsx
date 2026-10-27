import React, { useDeferredValue, useMemo, useState } from 'react';
import { Check, ChevronDown, ChevronRight, Headphones, Search, X } from 'lucide-react';
import { linkClick, navigateTo } from '../../router';
import { KURUL_NOLAR, kurulKaydet, useSeciliKurul } from '../kurul/KurulSecici';
import { useV15Baslik } from './baslik';
import { bransYolu, dersAdi, dersSirala, dersYolu, hocaYaz, kurulBranslari, sureDk, useDersListesi, useIlerleme } from './dersVeri';
import { Halka } from './Halka';
import '../../styles/v15/dersler.css';
import '../../styles/v15/ogren.css';

/**
 * v15 · Sesli ders listesi (tasarım sistemi v15 › B04). Adres /dersler/canliders[/kurulN] (branşsız). Arama, durum
 * çipleri (Tümü · Yarım kalan · Bitti), branş bölümleri (ilerleme + "Tümü" → branş sayfası), satır → ders ayrıntısı.
 * Liste kendi alanında kayar; sayfa sabit.
 */
type Durum = 'tum' | 'yarim' | 'bitti';
const DURUM: [Durum, string][] = [['tum', 'Tümü'], ['yarim', 'Yarım kalan'], ['bitti', 'Bitti']];
const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

export default function SesliListeV15() {
  const kurul = useSeciliKurul();
  const { dersler, hata } = useDersListesi();
  const ilerleme = useIlerleme();
  const [ara, setAra] = useState('');
  const [araAcik, setAraAcik] = useState(false);
  const q = fold(useDeferredValue(ara).trim());
  const [durum, setDurum] = useState<Durum>('tum');

  const branslar = useMemo(() => (dersler ? kurulBranslari(dersler, kurul) : []), [dersler, kurul]);
  const toplam = branslar.reduce((n, b) => n + b.dersler.length, 0);
  const gruplar = useMemo(
    () =>
      branslar
        .map((b) => ({
          ...b,
          liste: dersSirala(b.dersler).filter((d) => {
            const i = ilerleme(d);
            if (durum === 'yarim' && !(i.t != null && !i.bitti)) return false;
            if (durum === 'bitti' && !i.bitti) return false;
            return !q || fold(`${d.no} ${d.baslik} ${b.ad} ${d.hoca || ''}`).includes(q);
          }),
          biten: b.dersler.filter((d) => ilerleme(d).bitti).length,
        }))
        .filter((g) => g.liste.length),
    [branslar, durum, q, ilerleme],
  );
  useV15Baslik({ baslik: 'Sesli dersler', alt: dersler ? `Kurul ${kurul} · ${toplam} ders` : `Kurul ${kurul}` });

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
            <label className="d15-kurul">
              <span className="sr-only">Kurul seç</span>
              <select value={kurul} onChange={(e) => { const k = Number(e.target.value); kurulKaydet(k); navigateTo(`/dersler/canliders/kurul${k}`); }}>
                {KURUL_NOLAR.map((k) => <option key={k} value={k}>Kurul {k}</option>)}
              </select>
              <ChevronDown aria-hidden />
            </label>
            {DURUM.map(([id, t]) => (
              <button key={id} type="button" className={`o15-cip${durum === id ? ' is-on' : ''}`} aria-pressed={durum === id} onClick={() => setDurum(id)}>{t}</button>
            ))}
          </div>
        )}
        {!araAcik && <button type="button" className="v15-ib" onClick={() => setAraAcik(true)} aria-label="Ara"><Search aria-hidden /></button>}
      </div>

      <div className="sl15-alan">
        {dersler === null ? (
          <span className="v15-skel b15-skel" aria-hidden />
        ) : gruplar.length ? (
          gruplar.map((g) => (
            <section key={g.ad} className="sl15-grup" aria-label={g.kisa}>
              <a className="sl15-bas" href={bransYolu(kurul, g.ad)} onClick={linkClick(() => navigateTo(bransYolu(kurul, g.ad)))}>
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
                      <a className="b15-row" href={dersYolu(d.key)} onClick={linkClick(() => navigateTo(dersYolu(d.key)))}>
                        <span className={`v15-tile ${i.bitti ? 'is-ok' : i.t != null ? '' : 'is-n'}`}>{i.bitti ? <Check aria-hidden /> : <Headphones aria-hidden />}</span>
                        <span className="b15-row-t">
                          <b>{dersAdi(d)}</b>
                          <span>{[hocaYaz(d.hoca), sureDk(i.sure)].filter(Boolean).join(' · ')}</span>
                        </span>
                        <Halka pct={i.pct} etiket={i.bitti ? 'Bitti' : `%${i.pct} dinlendi`} />
                      </a>
                    </li>
                  );
                })}
              </ul>
            </section>
          ))
        ) : (
          <p className="b15-bos v15-card">{hata ? `Ders listesi alınamadı: ${hata}` : q || durum !== 'tum' ? 'Bu süzgeçte ders yok.' : `Kurul ${kurul} için sesli ders henüz yok.`}</p>
        )}
      </div>
    </div>
  );
}
