/** İstatistiklerim: genel (oyun türüne göre), rakiplere karşı ve son eller. Veri: GET /api/masa/istatistik. */
import React, { useEffect, useState } from 'react';
import { RefreshCw } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { OYUN_ADI, type Istatistik, type OyunTur } from '../../services/masa/tipler';
import { Avatar, birim, puanYaz, sadeAd } from './kabukOrtak';

type Sekme = 'genel' | 'rakip' | 'son';
const yuzde = (a: number, b: number) => (b > 0 ? Math.round((a / b) * 100) : 0);
const zaman = (t: number) => {
  const dk = Math.round((Date.now() - t) / 60_000);
  if (dk < 1) return 'şimdi';
  if (dk < 60) return `${dk} dk önce`;
  if (dk < 24 * 60) return `${Math.round(dk / 60)} sa önce`;
  return new Date(t).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};

export default function MasaIstatistik() {
  const [veri, setVeri] = useState<Istatistik | null>(null);
  const [hata, setHata] = useState(false);
  const [sekme, setSekme] = useState<Sekme>('genel');
  const [tur, setTur] = useState(0);

  useEffect(() => {
    let canli = true;
    setHata(false);
    void safeJsonFetch<Istatistik>('/api/masa/istatistik').then((r) => {
      if (!canli) return;
      const d = r.data;
      if (r.ok && d && Array.isArray(d.genel) && Array.isArray(d.rakipler) && Array.isArray(d.son)) setVeri(d);
      else setHata(true);
    });
    return () => { canli = false; };
  }, [tur]);

  if (hata) {
    return (
      <div className="mk-bos">
        <p>İstatistikler şu an okunamadı.</p>
        <button type="button" className="mk-dugme is-soluk" onClick={() => setTur((n) => n + 1)}><RefreshCw size={16} /> Yeniden dene</button>
      </div>
    );
  }
  if (!veri) return <p className="mk-bos">Yükleniyor…</p>;

  const topEl = veri.genel.reduce((t, g) => t + g.el, 0), topKaz = veri.genel.reduce((t, g) => t + g.kazanma, 0);
  const topPuan = veri.genel.reduce((t, g) => t + g.puan, 0), topCeza = veri.genel.reduce((t, g) => t + g.ceza, 0);

  return (
    <div className="mk-ist">
      <div className="mk-dilim mk-ist-sekme" role="tablist" aria-label="İstatistik bölümü">
        {([['genel', 'Genel'], ['rakip', `Rakiplere karşı${veri.rakipler.length ? ` (${veri.rakipler.length})` : ''}`], ['son', 'Son eller']] as [Sekme, string][]).map(([k, a]) => (
          <button key={k} type="button" role="tab" aria-selected={sekme === k} className={sekme === k ? 'is-on' : ''} onClick={() => setSekme(k)}>{a}</button>
        ))}
      </div>

      {sekme === 'genel' && (!topEl ? <p className="mk-bos">Henüz tamamladığın el yok. İlk elini bitirince sayılar burada birikir.</p> : (
        <>
          <div className="mk-ist-ozet">
            <div><b>{topEl}</b><span>el</span></div>
            <div><b>{topKaz}</b><span>kazanılan</span></div>
            <div><b>%{yuzde(topKaz, topEl)}</b><span>kazanma oranı</span></div>
            <div><b className={topPuan < 0 ? 'is-eksi' : ''}>{puanYaz(topPuan)}</b><span>toplam puan</span></div>
            <div><b>{topCeza}</b><span>ceza</span></div>
          </div>
          <div className="mk-ist-turler">
            {veri.genel.map((g) => (
              <article key={g.tur} className="mk-ist-tur">
                <header><h3>{OYUN_ADI[g.tur] || g.tur}</h3><span>{g.el} el</span></header>
                <div className="mk-oran" role="img" aria-label={`Kazanma oranı yüzde ${yuzde(g.kazanma, g.el)}`}><i style={{ transform: `scaleX(${g.el ? g.kazanma / g.el : 0})` }} /></div>
                <dl>
                  <div><dt>Kazanma</dt><dd>{g.kazanma} <small>(%{yuzde(g.kazanma, g.el)})</small></dd></div>
                  <div><dt>Toplam puan</dt><dd className={g.puan < 0 ? 'is-eksi' : ''}>{puanYaz(g.puan)}</dd></div>
                  <div><dt>Ceza</dt><dd>{g.ceza}</dd></div>
                  <div><dt>En iyi el</dt><dd className="is-arti">{puanYaz(g.enIyi)}</dd></div>
                  <div><dt>En kötü el</dt><dd className={g.enKotu < 0 ? 'is-eksi' : ''}>{puanYaz(g.enKotu)}</dd></div>
                </dl>
              </article>
            ))}
          </div>
        </>
      ))}

      {sekme === 'rakip' && (!veri.rakipler.length ? <p className="mk-bos">Henüz bir arkadaşınla el bitirmedin. Botlarla oynanan eller burada sayılmaz.</p> : (
        <ul className="mk-ist-rakipler">
          {veri.rakipler.map((r) => {
            const karar = r.benKazandim + r.oKazandi;
            const pay = karar ? r.benKazandim / karar : 0.5;
            const turler = (Object.entries(r.turler) as [OyunTur, number][]).map(([t, n]) => `${OYUN_ADI[t] || t} ${n}`).join(' · ');
            return (
              <li key={r.kimlik}>
                <div className="mk-rakip-bas">
                  <Avatar ad={r.ad} id={r.kimlik} boy={40} />
                  <span><b>{sadeAd(r.ad)}</b><small>{r.el} el birlikte{turler ? ` · ${turler}` : ''}</small></span>
                  <em className={pay > 0.5 ? 'is-arti' : pay < 0.5 ? 'is-eksi' : ''}>{!karar ? 'Henüz üstünlük yok' : pay > 0.5 ? 'Öndesin' : pay < 0.5 ? 'O önde' : 'Başa baş'}</em>
                </div>
                <div className="mk-ustunluk" role="img" aria-label={`Sen ${r.benKazandim} el kazandın, ${sadeAd(r.ad)} ${r.oKazandi} el kazandı`}>
                  <i style={{ transform: `scaleX(${pay})` }} />
                </div>
                <div className="mk-rakip-sayi">
                  <span><b>{r.benKazandim}</b> ben kazandım</span>
                  <span><b>{r.oKazandi}</b> o kazandı</span>
                </div>
                <div className="mk-rakip-sayi is-puan">
                  <span>Puanım <b className={r.benPuan < 0 ? 'is-eksi' : ''}>{puanYaz(r.benPuan)}</b></span>
                  <span>Puanı <b className={r.oPuan < 0 ? 'is-eksi' : ''}>{puanYaz(r.oPuan)}</b></span>
                </div>
              </li>
            );
          })}
        </ul>
      ))}

      {sekme === 'son' && (!veri.son.length ? <p className="mk-bos">Son ellerin burada listelenir.</p> : (
        <ul className="mk-ist-son">
          {veri.son.map((s, i) => (
            <li key={`${s.kod}-${s.elNo}-${i}`} className={s.kazandi ? 'is-kazandi' : ''}>
              <span className="mk-son-puan">{puanYaz(s.puan)}</span>
              <span className="mk-son-metin">
                <b>{OYUN_ADI[s.tur] || s.tur} · {s.elNo}. el {s.kazandi && <i className="mk-rozet is-iyi">Kazandın</i>}</b>
                <small>
                  {s.rakipler.length ? s.rakipler.map(sadeAd).join(', ') : 'Rakip yok'}
                  {!s.kazandi && ` · ${s.kalan} ${birim(s.tur)} kaldı`}{s.ceza > 0 && ` · ${s.ceza} ceza`}
                </small>
              </span>
              <time>{zaman(s.at)}</time>
            </li>
          ))}
        </ul>
      ))}
    </div>
  );
}
