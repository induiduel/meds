import React, { useEffect, useMemo, useState } from 'react';
import { Clock, Eraser, Headphones, History, Lightbulb, Play, RotateCcw } from 'lucide-react';
import { cozucuDizinYukle, ozet, setAdi, useIlerleme, type CDizin } from './cozucuVeri';
import { bransTanim, type Brans } from '../brans';
import { getCozucuSureGruplari, dk } from '../sure/spotsSureVeri';
import { SpotsSureOzeti } from '../sure/SpotsSureOzeti';
import { SpotsSureDiyalog } from '../sure/SpotsSureDiyalog';
import '../../../styles/soru-cozucu.css';

/**
 * Sınav spotları › "Soru çözücü" sekmesi (branş seçili: ?brans=patoloji|enfeksiyon|uroloji): ders/set listesi + ilerleme. Ders
 * seçilince tam ekran çözücü açılır (?gorunum=cozucu&ders=<kod>&coz=1; yanlışların tekrarı &coz=yanlis, çıkmışlar &coz=cikmis).
 */
const SoruCozucu = React.lazy(() => import('./SoruCozucu'));

const urlOku = (k: string) => { try { return new URLSearchParams(location.search).get(k); } catch { return null; } };
const urlYaz = (p: Record<string, string | null>) => {
  try {
    const u = new URL(location.href);
    Object.entries(p).forEach(([k, v]) => (v === null ? u.searchParams.delete(k) : u.searchParams.set(k, v)));
    history.replaceState(history.state, '', u.pathname + u.search + u.hash);
  } catch { /* yok */ }
};
const katla = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

export const SoruCozucuSayfa: React.FC<{ brans?: Brans }> = ({ brans = 'patoloji' }) => {
  const bt = bransTanim(brans);
  const [dizin, setDizin] = useState<CDizin | null>(null);
  const [hata, setHata] = useState(false);
  const [ara, setAra] = useState('');
  const [sureAcik, setSureAcik] = useState(() => location.hash === '#sureler');
  const [acik, setAcik] = useState<{ kod: string; mod?: 'yanlis' | 'cikmis' } | null>(() => {
    const k = urlOku('ders'); const c = urlOku('coz');
    return k && c ? { kod: k, mod: c === 'yanlis' || c === 'cikmis' ? c : undefined } : null;
  });
  const ilerleme = useIlerleme();
  const cozucuSureGruplari = useMemo(() => getCozucuSureGruplari(), [ilerleme]);

  useEffect(() => {
    const f = () => { if (location.hash === '#sureler') setSureAcik(true); };
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);

  useEffect(() => { setDizin(null); setHata(false); cozucuDizinYukle(brans).then(setDizin).catch(() => setHata(true)); }, [brans]);

  const ac = (kod: string, mod?: 'yanlis' | 'cikmis') => { setAcik({ kod, mod }); urlYaz({ ders: kod, coz: mod || '1' }); };
  const kapat = () => { setAcik(null); urlYaz({ coz: null }); };

  const genel = useMemo(() => {
    const t = { d: 0, d2: 0, y: 0, toplam: 0 };
    dizin?.dersler.forEach((d) => { const o = ozet(ilerleme[d.kod], d.soru); t.d += o.d; t.d2 += o.d2; t.y += o.y; t.toplam += d.soru; });
    return t;
  }, [dizin, ilerleme]);
  const dersler = useMemo(() => {
    const q = katla(ara.trim());
    return (dizin?.dersler || []).filter((d) => !q || katla(`${d.no} ${d.baslik}`).includes(q));
  }, [dizin, ara]);

  if (hata) return <p className="scs-bos">Soru çözücü yüklenemedi.</p>;
  if (!dizin) return <p className="scs-bos">Yükleniyor…</p>;
  if (!dizin.dersler.length) return <p className="scs-bos">{bt.ad} soru çözücüsü hazırlanıyor.</p>;
  const yuzde = (n: number) => `${genel.toplam ? (n / genel.toplam) * 100 : 0}%`;
  const cozulen = genel.d + genel.d2 + genel.y;

  return (
    <div className="scs">
      <section className="scs-hero">
        <div>
          <h2><Headphones aria-hidden />{bt.ad} · Sesli soru çözücü</h2>
          <p>{new Set(dizin.dersler.map((d) => d.no)).size} derste {genel.toplam} soru: {bt.cozucuNot}. Asistan soruyu ve seçenekleri okur, sen seçersin; her seçeneğin neden doğru ya da yanlış olduğunu ders sunumuna dayanarak kısaca anlatır.</p>
        </div>
        <div className="scs-genel" aria-label={`${cozulen} / ${genel.toplam} soru çözüldü`}>
          <b>{cozulen}<small> / {genel.toplam}</small></b>
          <div className="scs-cubuk" aria-hidden><i className="is-d" style={{ width: yuzde(genel.d) }} /><i className="is-d2" style={{ width: yuzde(genel.d2) }} /><i className="is-y" style={{ width: yuzde(genel.y) }} /></div>
          <small>{genel.d} ilk denemede doğru · {genel.d2} yardımla · {genel.y} çözümü dinlendi</small>
        </div>
        <ul className="scs-adimlar">
          <li><Lightbulb aria-hidden /><span><b>İpucu</b>Cevabı söylemeden neyi düşünmen gerektiğini hatırlatır.</span></li>
          <li><Eraser aria-hidden /><span><b>Bir yanlışı ele</b>Bir yanlış seçeneği nedeniyle açıklayıp eler.</span></li>
          <li><Headphones aria-hidden /><span><b>Çözümü dinle</b>Tüm seçenekleri tek tek açıklar, doğru cevabı ve nedenini söyler.</span></li>
        </ul>
      </section>

      <SpotsSureOzeti
        baslik="Sesli Soru Çözümü Toplam Süresi"
        gruplar={cozucuSureGruplari}
        seciliBrans={brans}
        onSecBrans={(b) => {
          if (b !== 'tum' && b !== brans) {
            const u = new URL(location.href);
            u.searchParams.set('brans', b);
            history.pushState(history.state, '', u.pathname + u.search + u.hash);
            window.dispatchEvent(new PopStateEvent('popstate'));
          }
        }}
        onTamListe={() => setSureAcik(true)}
        birimAd="set"
        tercihKey="medsoru_cozucu_sure_acik"
      />

      <div className="scs-arac">
        <div className="scs-ara">
          <input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder={`Ders ara (ör. ${bt.araOrnek})`} aria-label="Ders ara" />
        </div>
        <button type="button" className="scs-btn-sure" onClick={() => setSureAcik(true)} title="Tüm branşların ve derslerin soru çözümü süreleri">
          <Clock aria-hidden />
          <span>Çözüm süreleri</span>
        </button>
      </div>

      <ul className="scs-liste">
        {dersler.map((d) => {
          const p = ilerleme[d.kod];
          const o = ozet(p, d.soru);
          const y = o.d2 + o.y;
          const w = (n: number) => `${(n / d.soru) * 100}%`;
          const devam = !o.tamam && o.cozulen > 0;
          return (
            <li key={d.kod}>
              <div className={`scs-ders${o.tamam ? ' is-tamam' : ''}`}>
                <div className="scs-ders-ust">
                  <span className="scs-no">{d.no}</span>
                  <span className="scs-ad">
                    <b>{d.baslik}</b>
                    <small>
                      {setAdi(d) ? `${setAdi(d)} · ` : ''}{d.soru} soru
                      {d.sure ? ` · ~${dk(d.sure)} dk çözüm` : ''}
                      {d.cikmis ? ` (${d.cikmis} çıkmış)` : ''}
                      {o.cozulen ? ` · ${o.cozulen} çözüldü · ${o.d} ilk denemede doğru` : ''}
                      {d.ses ? '' : ' · ses hazırlanıyor'}
                    </small>
                  </span>
                </div>
                <div className="scs-cubuk" aria-hidden><i className="is-d" style={{ width: w(o.d) }} /><i className="is-d2" style={{ width: w(o.d2) }} /><i className="is-y" style={{ width: w(o.y) }} /></div>
                <div className="scs-ders-alt">
                  <button type="button" className="is-ana" onClick={() => ac(d.kod)}><Play aria-hidden />{o.tamam ? 'Yeniden çöz' : devam ? 'Devam et' : 'Çözmeye başla'}</button>
                  {!!d.cikmis && <button type="button" onClick={() => ac(d.kod, 'cikmis')}><History aria-hidden />Çıkmışlar · {d.cikmis}</button>}
                  {y > 0 && <button type="button" onClick={() => ac(d.kod, 'yanlis')}><RotateCcw aria-hidden />Yanlışlar · {y}</button>}
                </div>
              </div>
            </li>
          );
        })}
      </ul>
      {!dersler.length && <p className="scs-bos">“{ara}” ile eşleşen ders yok.</p>}

      {sureAcik && (
        <SpotsSureDiyalog
          baslik="Sesli soru çözücü süreleri"
          gruplar={cozucuSureGruplari}
          onKapat={() => {
            setSureAcik(false);
            if (location.hash === '#sureler') {
              history.replaceState(history.state, '', location.pathname + location.search);
            }
          }}
          onDersAc={(b, k) => {
            if (b !== brans) {
              const u = new URL(location.href);
              u.searchParams.set('brans', b);
              u.searchParams.set('ders', k);
              u.searchParams.set('coz', '1');
              history.pushState(history.state, '', u.pathname + u.search + u.hash);
              window.dispatchEvent(new PopStateEvent('popstate'));
            } else {
              ac(k);
            }
          }}
          birimAd="set"
          not="Süreler EMA seslendirmesine göredir. Soru kökü, seçenekler, ipucu, eleme ve detaylı çözüm açıklamalarını içerir."
        />
      )}

      {acik && (
        <React.Suspense fallback={null}>
          <SoruCozucu key={`${brans}-${acik.kod}-${acik.mod || ''}`} brans={brans} kod={acik.kod} mod={acik.mod} onClose={kapat} onDersDegis={(k) => urlYaz({ ders: k, coz: '1' })} />
        </React.Suspense>
      )}
    </div>
  );
};

export default SoruCozucuSayfa;
