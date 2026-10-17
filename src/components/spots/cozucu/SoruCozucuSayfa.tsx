import React, { useEffect, useMemo, useState } from 'react';
import { Eraser, Headphones, History, Lightbulb, Play, RotateCcw } from 'lucide-react';
import { cozucuDizinYukle, ozet, useIlerleme, type CDizin } from './cozucuVeri';
import '../../../styles/soru-cozucu.css';

/**
 * Sınav spotları › "Patoloji · Soru çözücü" sekmesi: ders listesi + ilerleme. Ders seçilince tam ekran çözücü açılır
 * (?gorunum=cozucu&ders=<kod>&coz=1; yanlışların tekrarı &coz=yanlis). Sorular 2026-27 örnek soruları.
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

export const SoruCozucuSayfa: React.FC = () => {
  const [dizin, setDizin] = useState<CDizin | null>(null);
  const [hata, setHata] = useState(false);
  const [ara, setAra] = useState('');
  const [acik, setAcik] = useState<{ kod: string; mod?: 'yanlis' | 'cikmis' } | null>(() => {
    const k = urlOku('ders'); const c = urlOku('coz');
    return k && c ? { kod: k, mod: c === 'yanlis' || c === 'cikmis' ? c : undefined } : null;
  });
  const ilerleme = useIlerleme();
  useEffect(() => { cozucuDizinYukle().then(setDizin).catch(() => setHata(true)); }, []);

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
  const yuzde = (n: number) => `${genel.toplam ? (n / genel.toplam) * 100 : 0}%`;
  const cozulen = genel.d + genel.d2 + genel.y;

  return (
    <div className="scs">
      <section className="scs-hero">
        <div>
          <h2><Headphones aria-hidden />Patoloji · Sesli soru çözücü</h2>
          <p>{dizin.dersler.length} derste {genel.toplam} soru: 2026-27 örnek soruları, aynı üslupta orta-zor benzer sorular ve konunun çıkmış soruları. Asistan soruyu ve seçenekleri okur, sen seçersin; her seçeneğin neden doğru ya da yanlış olduğunu ders sunumuna dayanarak kısaca anlatır.</p>
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

      <div className="scs-ara">
        <input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Ders ara (ör. nefrotik, meme, tromboz)" aria-label="Ders ara" />
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
                    <small>{d.soru} soru{d.cikmis ? ` (${d.cikmis} çıkmış)` : ''}{o.cozulen ? ` · ${o.cozulen} çözüldü · ${o.d} ilk denemede doğru` : ''}{d.ses ? '' : ' · ses hazırlanıyor'}</small>
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

      {acik && (
        <React.Suspense fallback={null}>
          <SoruCozucu key={`${acik.kod}-${acik.mod || ''}`} kod={acik.kod} mod={acik.mod} onClose={kapat} onDersDegis={(k) => urlYaz({ ders: k, coz: '1' })} />
        </React.Suspense>
      )}
    </div>
  );
};

export default SoruCozucuSayfa;
