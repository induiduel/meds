import React, { useEffect, useMemo, useState } from 'react';
import { Check, Clock, Eraser, Headphones, History, Lightbulb, Play, RotateCcw } from 'lucide-react';
import { cozucuDizinYukle, ozet, setAdi, useIlerleme, type CDizin } from './cozucuVeri';
import { bransTanim, type Brans } from '../brans';
import { getCozucuSureGruplari, dk } from '../sure/spotsSureVeri';
import { SpotsSureDiyalog } from '../sure/SpotsSureDiyalog';
import { useSpotCozucuStats, fmtSureDk } from '../../../services/spotCozucuIstatistik';
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
  const stats = useSpotCozucuStats();
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

  const dersSay = new Set(dizin.dersler.map((d) => d.no)).size;
  // Kaldığın yer: en son çalışılan, bitmemiş ders
  const son = dizin.dersler
    .map((d) => ({ d, p: ilerleme[d.kod], o: ozet(ilerleme[d.kod], d.soru) }))
    .filter((x) => x.p && x.o.cozulen > 0 && !x.o.tamam)
    .sort((a, b) => String(b.p!.at || '').localeCompare(String(a.p!.at || '')))[0];

  return (
    <div className="scs">
      <header className="scs-head">
        <div className="scs-head-t">
          <h2><Headphones aria-hidden />{bt.ad} · Sesli soru çözücü</h2>
          <span className="scs-count">{dersSay} ders · {genel.toplam.toLocaleString('tr-TR')} soru</span>
        </div>
        <p className="scs-desc">Asistan soruyu ve seçenekleri okur, sen seçersin; ardından her seçeneğin nedenini ders sunumuna dayanarak açıklar. <span className="scs-kaynak">Sorular: {bt.cozucuNot}.</span></p>
        <div className="scs-prog" aria-label={`${cozulen} / ${genel.toplam} soru çözüldü`}>
          <div className="scs-cubuk" aria-hidden><i className="is-d" style={{ width: yuzde(genel.d) }} /><i className="is-d2" style={{ width: yuzde(genel.d2) }} /><i className="is-y" style={{ width: yuzde(genel.y) }} /></div>
          <small>
            <b>{cozulen}</b> / {genel.toplam} çözüldü
            {cozulen > 0 && (
              <>
                {' '}· <span className="is-d">{genel.d} ilk denemede doğru (%{Math.round((genel.d / cozulen) * 100)})</span>
                {' '}· <span className="is-d2">{genel.d2} yardımla</span>
                {' '}· <span className="is-y">{genel.y} çözümü dinlendi</span>
                {stats.cozucuSureSn > 0 && <> · <b>⏱️ {fmtSureDk(stats.cozucuSureSn)} çözüldü</b></>}
              </>
            )}
          </small>
        </div>
        <details className="scs-nasil">
          <summary>Nasıl çalışır?</summary>
          <ul className="scs-adimlar">
            <li><Lightbulb aria-hidden /><span><b>İpucu</b>Cevabı söylemeden neyi düşünmen gerektiğini hatırlatır.</span></li>
            <li><Eraser aria-hidden /><span><b>Bir yanlışı ele</b>Bir yanlış seçeneği nedeniyle açıklayıp eler.</span></li>
            <li><Headphones aria-hidden /><span><b>Çözümü dinle</b>Tüm seçenekleri tek tek açıklar, doğru cevabı ve nedenini söyler.</span></li>
          </ul>
        </details>
      </header>

      {son && (
        <button type="button" className="scs-devam" onClick={() => ac(son.d.kod)}>
          <span className="scs-devam-ic" aria-hidden><Play /></span>
          <span className="scs-devam-t"><small>Kaldığın yerden devam</small><b>{son.d.no}. {son.d.baslik}{setAdi(son.d) ? ` · ${setAdi(son.d)}` : ''}</b></span>
          <span className="scs-devam-n">{son.o.cozulen}/{son.d.soru}</span>
        </button>
      )}

      <div className="scs-arac">
        <div className="scs-ara">
          <input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder={`Ders ara (ör. ${bt.araOrnek})`} aria-label="Ders ara" />
        </div>
        <button type="button" className="scs-btn-sure" onClick={() => setSureAcik(true)} title="Tüm branşların ve derslerin soru çözümü süreleri">
          <Clock aria-hidden />
          <span>Süreler</span>
        </button>
      </div>

      <ul className="scs-liste is-satir">
        {dersler.map((d) => {
          const p = ilerleme[d.kod];
          const o = ozet(p, d.soru);
          const y = o.d2 + o.y;
          const w = (n: number) => `${(n / d.soru) * 100}%`;
          const devam = !o.tamam && o.cozulen > 0;
          return (
            <li key={d.kod} className={`scs-row${o.tamam ? ' is-tamam' : ''}`}>
              <button type="button" className="scs-row-b" onClick={() => ac(d.kod)}
                aria-label={`${d.no}. ${d.baslik}${setAdi(d) ? `, ${setAdi(d)}` : ''}: ${o.tamam ? 'yeniden çöz' : devam ? `devam et, ${o.cozulen}/${d.soru}` : 'çözmeye başla'}`}>
                <span className="scs-no">{d.no}</span>
                <span className="scs-ad">
                  <b>{d.baslik}</b>
                  <small>
                    {setAdi(d) ? `${setAdi(d)} · ` : ''}{d.soru} soru{d.sure ? ` · ~${dk(d.sure)} dk` : ''}
                    {o.cozulen ? ` · ${o.d}/${o.cozulen} ilk denemede doğru` : ''}{d.ses ? '' : ' · ses hazırlanıyor'}
                  </small>
                  {o.cozulen > 0 && <span className="scs-cubuk" aria-hidden><i className="is-d" style={{ width: w(o.d) }} /><i className="is-d2" style={{ width: w(o.d2) }} /><i className="is-y" style={{ width: w(o.y) }} /></span>}
                </span>
                <span className={`scs-durum${devam ? ' is-devam' : ''}`}>{o.tamam ? <><Check aria-hidden />Bitti</> : devam ? <>Devam</> : <><Play aria-hidden />Başla</>}</span>
              </button>
              {(!!d.cikmis || y > 0) && (
                <div className="scs-row-ek">
                  {!!d.cikmis && <button type="button" onClick={() => ac(d.kod, 'cikmis')}><History aria-hidden />Yalnız çıkmışlar · {d.cikmis}</button>}
                  {y > 0 && <button type="button" onClick={() => ac(d.kod, 'yanlis')}><RotateCcw aria-hidden />Yanlışlarım · {y}</button>}
                </div>
              )}
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
