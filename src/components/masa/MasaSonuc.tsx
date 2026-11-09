/** El sonu ve maç sonu katmanları (sahnenin üstünde; masa arkada son durumuyla görünür kalır). */
import React, { useEffect, useMemo } from 'react';
import { motion } from 'motion/react';
import { ArrowRight, BarChart3, Crown, Handshake, Home, Layers, RotateCcw, Star, Trophy } from 'lucide-react';
import { masa } from '../../services/masa/istemci';
import { OYUN_ADI, type ElSonuc, type OdaGorunum, type OyuncuBilgi } from '../../services/masa/tipler';
import { azHareket, sesCal, titret } from './ortak';
import { Avatar, Konfeti, SkorTablo, birim, cezaBilgi, puanYaz, sadeAd, useSayac } from './kabukOrtak';

const TESELLI = ['Bir sonraki el senin.', 'Şans bu el karşı taraftaydı.', 'Az kaldı, bir sonraki elde toparlarsın.', 'Her el yeni bir başlangıç.'];
const perde = { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 }, transition: { duration: 0.22 } };
const kutu = () => (azHareket() ? {} : { initial: { y: 26, scale: 0.96 }, animate: { y: 0, scale: 1 }, transition: { type: 'spring' as const, stiffness: 300, damping: 26 } });

/** Düşen taş/kart parçacıkları (yalnız transform + opacity) */
function Dokulen({ adet, kart }: { adet: number; kart: boolean }) {
  const p = useMemo(() => Array.from({ length: Math.min(12, Math.max(4, adet)) }, (_, i) => ({ x: 6 + ((i * 53) % 88), g: (i % 5) * 0.09, d: ((i * 47) % 60) - 30, s: 1.1 + (i % 3) * 0.25 })), [adet]);
  if (azHareket()) return null;
  return (
    <div className="mk-dokulen" aria-hidden="true">
      {p.map((q, i) => <i key={i} className={kart ? 'is-kart' : ''} style={{ left: `${q.x}%`, animationDelay: `${q.g}s`, animationDuration: `${q.s}s`, ['--mk-don' as any]: `${q.d}deg` }} />)}
    </div>
  );
}

function Yildizlar() {
  if (azHareket()) return null;
  return (
    <div className="mk-yildizlar" aria-hidden="true">
      {Array.from({ length: 8 }, (_, i) => {
        const a = (i / 8) * Math.PI * 2;
        return (
          <motion.span key={i} initial={{ x: 0, y: 0, scale: 0, opacity: 1 }} animate={{ x: Math.cos(a) * 78, y: Math.sin(a) * 78, scale: [0, 1.2, 0.8], opacity: [1, 1, 0] }} transition={{ duration: 0.95, delay: 0.12 + i * 0.02, ease: 'easeOut' }}>
            <Star size={16} fill="currentColor" />
          </motion.span>
        );
      })}
    </div>
  );
}

/* ------------------------------------------------------------------ el sonu ------------------------------------------------------------------ */

export function ElSonu({ oda, sonuc, macBitti, macaGec }: { oda: OdaGorunum; sonuc: ElSonuc; macBitti: boolean; macaGec: () => void }) {
  const benim = sonuc.satirlar.find((s) => s.id === oda.ben);
  const notr = sonuc.neden !== 'bitti' || !sonuc.kazananlar.length;
  const kazandim = !notr && !!benim?.kazandi;
  const hal: 'kazandi' | 'kaybetti' | 'notr' = notr || !benim ? 'notr' : kazandim ? 'kazandi' : 'kaybetti';
  const uno = oda.tur === 'uno', takim = oda.tur === 'takim';
  const ad = (id: string) => sadeAd(oda.oyuncular.find((o) => o.id === id)?.ad || 'Oyuncu');
  const bitiren = sonuc.satirlar.find((s) => s.kazandi && s.kalan === 0)?.id || sonuc.kazananlar[0];
  const sayac = useSayac(benim?.puan || 0, 950, 350);

  useEffect(() => {
    if (hal === 'kazandi') { sesCal('kazan'); titret([20, 40, 20]); }
    else if (hal === 'kaybetti') { sesCal('kaybet'); titret(60); }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const tahta = oda.tur === 'go' || oda.tur === 'cizgi' || oda.tur === 'xox';
  const baslik = tahta && hal !== 'notr' ? (hal === 'kazandi' ? 'Eli kazandın!' : `${ad(bitiren)} kazandı`) : hal === 'kazandi'
    ? (takim && bitiren !== oda.ben ? 'Takımın kazandı!' : uno ? 'Kartlarını bitirdin!' : 'Elini bitirdin!')
    : hal === 'kaybetti'
      ? (takim ? `${sonuc.kazananTakim || ''} takımı kazandı` : `${ad(bitiren)} ${uno ? 'kartlarını' : 'elini'} bitirdi`)
      : sonuc.neden === 'berabere' ? 'Berabere' : 'Deste bitti';
  const altMetin = tahta ? (hal === 'kaybetti' ? `${benim?.aciklama || ''}. ${TESELLI[oda.elNo % TESELLI.length]}` : hal === 'kazandi' ? (benim?.aciklama || '') : 'Tahta doldu, dizi çıkmadı: bu elin kazananı yok.')
    : hal === 'kazandi'
    ? (takim && bitiren !== oda.ben ? `${ad(bitiren)} elini bitirdi; kalan taşların sayılmadı.` : uno ? 'Rakiplerin elindeki kartların puanı senin.' : 'Rakiplerin kalan taşları eksi yazıldı.')
    : hal === 'kaybetti'
      ? `${benim!.aciklama || `${benim!.kalan} ${birim(oda.tur)} kaldı`}. ${TESELLI[oda.elNo % TESELLI.length]}`
      : sonuc.neden === 'berabere' ? `Yığın bitti, kimse oynayamıyor. Bu elin kazananı yok; herkes elinde kalan ${birim(oda.tur)} kadar eksi aldı.` : 'Deste tükendi; bu eli kazanan yok. Herkes elindekine göre puan aldı.';

  const sirali = [...sonuc.satirlar].sort((a, b) => Number(b.kazandi) - Number(a.kazandi) || b.puan - a.puan);
  const cezalilar = sonuc.satirlar.filter((s) => s.cezalar.length);
  const kurucu = oda.kurucu === oda.ben;
  const kurucuBagli = !!oda.oyuncular.find((o) => o.id === oda.kurucu)?.bagli;
  const elMetni = `${OYUN_ADI[oda.tur]} · ${oda.elNo}. el${oda.ayar.elSayisi ? ` / ${oda.ayar.elSayisi}` : ''}`;

  return (
    <motion.div className="mk-sonuc" {...perde} role="dialog" aria-modal="true" aria-label="El sonucu">
      <motion.div className={`mk-sonuc-kutu is-${hal}`} {...kutu()}>
        <div className="mk-sonuc-kahraman">
          {hal === 'kazandi' && <Konfeti />}
          {hal === 'kaybetti' && <Dokulen adet={benim?.kalan || 5} kart={uno} />}
          <span className="mk-ust-etiket">{elMetni}</span>
          <div className="mk-sonuc-simge">
            {hal === 'kazandi' && <><Yildizlar /><motion.span className="mk-kupa" initial={azHareket() ? false : { scale: 0, rotate: -24 }} animate={{ scale: 1, rotate: 0 }} transition={{ type: 'spring', stiffness: 260, damping: 12, delay: 0.1 }}><Trophy size={46} /></motion.span></>}
            {hal === 'kaybetti' && <span className="mk-eksi-sayac">{puanYaz(sayac)}</span>}
            {hal === 'notr' && <span className="mk-notr-simge">{sonuc.neden === 'berabere' ? <Handshake size={40} /> : <Layers size={40} />}</span>}
          </div>
          <h2>{baslik}</h2>
          {hal === 'kazandi' && <p className="mk-sonuc-puan">{puanYaz(sayac)} <small>puan</small></p>}
          {hal === 'notr' && benim && !tahta && <p className="mk-sonuc-puan is-notr">{puanYaz(sayac)} <small>puan · {benim.kalan} {birim(oda.tur)} kaldı</small></p>}
          <p className="mk-sonuc-alt">{altMetin}</p>
        </div>

        <div className="mk-sonuc-govde">
          <table className="mk-el-tablo">
            <thead><tr><th scope="col">Oyuncu</th><th scope="col">Kalan</th><th scope="col">El puanı</th><th scope="col">Toplam</th></tr></thead>
            <tbody>
              {sirali.map((s) => {
                const o = oda.oyuncular.find((x) => x.id === s.id);
                return (
                  <tr key={s.id} className={`${s.kazandi ? 'is-kazanan' : ''}${s.id === oda.ben ? ' is-ben' : ''}`}>
                    <th scope="row">
                      <span className="mk-el-oyuncu">
                        <Avatar ad={o?.ad || '?'} foto={o?.foto} bot={o?.bot} id={s.id} boy={30} />
                        <span>
                          <b>{ad(s.id)}{s.id === oda.ben && <em>sen</em>}{o?.takim && <i className={`mk-takim-nokta is-${o.takim}`}>{o.takim}</i>}{s.kazandi && <Crown size={14} className="mk-el-tac" aria-label="Kazandı" />}</b>
                          {s.aciklama && <small>{s.aciklama}</small>}
                        </span>
                      </span>
                    </th>
                    <td>{s.kalan} <small>{birim(oda.tur)}</small></td>
                    <td className={s.puan < 0 ? 'is-eksi' : s.puan > 0 ? 'is-arti' : ''}><b>{puanYaz(s.puan)}</b></td>
                    <td>{puanYaz(oda.skor[s.id] || 0)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          <section className="mk-cezalar">
            <h3>Cezalar</h3>
            {!cezalilar.length ? <p className="mk-bos is-ince">Bu elde ceza yazılmadı.</p> : (
              <ul>
                {cezalilar.map((s) => (
                  <li key={s.id}>
                    <b>{ad(s.id)}</b>
                    <div>
                      {s.cezalar.map((c, i) => {
                        const b = cezaBilgi(c);
                        return (
                          <span key={i} className={`mk-ceza ${b.sinif}`}>
                            <i className={`mk-ceza-rozet ${b.sinif}`}>{b.ad}</i>
                            <em>{c.puan ? puanYaz(c.puan) : '2 kart'}</em>
                            <small>{b.ne}</small>
                          </span>
                        );
                      })}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>

        <footer className="mk-sonuc-alt-cubuk">
          {macBitti ? (
            <button type="button" className="mk-dugme is-ana is-buyuk" onClick={macaGec}>Maç sonucunu gör <ArrowRight size={18} /></button>
          ) : kurucu || !kurucuBagli ? (
            <button type="button" className="mk-dugme is-ana is-buyuk" onClick={() => masa.sonrakiEl()}>{kurucu ? 'Sonraki el' : 'Sonraki eli başlat'} <ArrowRight size={18} /></button>
          ) : (
            <p><span className="mk-donen" /> Kurucu sonraki eli başlatacak.</p>
          )}
        </footer>
      </motion.div>
    </motion.div>
  );
}

/* ------------------------------------------------------------------ maç sonu ------------------------------------------------------------------ */

interface Sira { ad: string; puan: number; sira: number; uyeler: OyuncuBilgi[]; ben: boolean }

export function MacSonu({ oda, istatAc }: { oda: OdaGorunum; istatAc: () => void }) {
  const takim = oda.tur === 'takim';
  const liste: Sira[] = useMemo(() => {
    const ham = takim
      ? (['A', 'B'] as const).map((t) => { const u = oda.oyuncular.filter((o) => (o.takim || 'A') === t); return { ad: `${t} takımı`, puan: u.reduce((n, o) => n + (oda.skor[o.id] || 0), 0), uyeler: u, ben: u.some((o) => o.id === oda.ben) }; }).filter((x) => x.uyeler.length)
      : oda.oyuncular.map((o) => ({ ad: sadeAd(o.ad), puan: oda.skor[o.id] || 0, uyeler: [o], ben: o.id === oda.ben }));
    ham.sort((a, b) => b.puan - a.puan);
    return ham.map((x) => ({ ...x, sira: 1 + ham.filter((y) => y.puan > x.puan).length }));
  }, [oda.oyuncular, oda.skor, takim, oda.ben]);
  const ben = liste.find((x) => x.ben);
  const oynandi = oda.eller.length > 0;
  const birinci = oynandi && ben?.sira === 1;
  const berabere = birinci && liste.filter((x) => x.sira === 1).length > 1;
  const kurucu = oda.kurucu === oda.ben;
  const kursu = liste.slice(0, 3);
  // Kürsü dizilişi: 2 · 1 · 3
  const dizi = kursu.length === 3 ? [kursu[1], kursu[0], kursu[2]] : kursu.length === 2 ? [kursu[1], kursu[0]] : kursu;

  useEffect(() => {
    if (!oynandi) return;
    if (birinci) { sesCal('kazan'); titret([20, 40, 20, 40, 30]); } else sesCal('kaybet');
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <motion.div className="mk-sonuc is-mac" {...perde} role="dialog" aria-modal="true" aria-label="Maç sonucu">
      <motion.div className={`mk-sonuc-kutu is-mac ${birinci ? 'is-kazandi' : 'is-notr'}`} {...kutu()}>
        <div className="mk-sonuc-kahraman is-mac">
          {birinci && <Konfeti adet={120} />}
          <span className="mk-ust-etiket">{OYUN_ADI[oda.tur]} · {oda.eller.length} el oynandı</span>
          <h2>{!oynandi ? 'Maç bitti' : berabere ? 'Maç berabere bitti' : birinci ? 'Maçı kazandın!' : `Maç bitti: ${ben?.sira || '–'}. oldun`}</h2>
          <p className="mk-sonuc-alt">{!oynandi ? 'Hiç el tamamlanmadan bitirildi; puan yazılmadı.' : birinci ? (takim ? 'Takımın en yüksek puanla bitirdi.' : 'En yüksek toplam puan senin.') : `${liste[0].ad} ${puanYaz(liste[0].puan)} puanla birinci. Rövanş için aynı masada yeni maç başlatılabilir.`}</p>
          {oynandi && (
            <div className={`mk-kursu is-${dizi.length}`}>
              {dizi.map((x, i) => (
                <motion.div key={x.ad + i} className={`mk-kursu-yer is-${x.sira}${x.ben ? ' is-ben' : ''}`} initial={azHareket() ? false : { y: 40, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.15 + (3 - Math.min(3, x.sira)) * 0.16, type: 'spring', stiffness: 240, damping: 20 }}>
                  <span className="mk-kursu-avatarlar">{x.uyeler.slice(0, 3).map((o) => <Avatar key={o.id} ad={o.ad} foto={o.foto} bot={o.bot} id={o.id} boy={x.sira === 1 ? 46 : 38} tac={x.sira === 1 && x.uyeler.length === 1} />)}</span>
                  <b>{x.ad}</b>
                  <em className={x.puan < 0 ? 'is-eksi' : ''}>{puanYaz(x.puan)}</em>
                  <span className="mk-kursu-basamak">{x.sira}</span>
                </motion.div>
              ))}
            </div>
          )}
        </div>

        <div className="mk-sonuc-govde">
          {oynandi && (
            <>
              <h3 className="mk-sonuc-bolum">Sıralama</h3>
              <ol className="mk-siralama">
                {liste.map((x, i) => (
                  <li key={x.ad + i} className={x.ben ? 'is-ben' : ''}>
                    <i>{x.sira}</i>
                    <span className="mk-siralama-ad"><b>{x.ad}{x.ben && !takim && <em>sen</em>}</b>{takim && <small>{x.uyeler.map((o) => `${sadeAd(o.ad)} ${puanYaz(oda.skor[o.id] || 0)}`).join(' · ')}</small>}</span>
                    <b className={x.puan < 0 ? 'is-eksi' : ''}>{puanYaz(x.puan)}</b>
                  </li>
                ))}
              </ol>
              <h3 className="mk-sonuc-bolum">Maçın özeti</h3>
              <SkorTablo oda={oda} />
            </>
          )}
        </div>

        <footer className="mk-sonuc-alt-cubuk is-mac">
          {kurucu
            ? <button type="button" className="mk-dugme is-ana is-buyuk" onClick={() => masa.baslat()}><RotateCcw size={18} /> Aynı masada yeni maç</button>
            : <p><span className="mk-donen" /> Kurucu aynı masada yeni maç başlatabilir.</p>}
          <button type="button" className="mk-dugme is-acik" onClick={() => masa.cik()}><Home size={18} /> Merkeze dön</button>
          <button type="button" className="mk-dugme is-soluk" onClick={istatAc}><BarChart3 size={18} /> İstatistikler</button>
        </footer>
      </motion.div>
    </motion.div>
  );
}
