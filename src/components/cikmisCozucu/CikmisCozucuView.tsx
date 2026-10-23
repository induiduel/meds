import React, { useEffect, useMemo, useState } from 'react';
import { Check, ChevronLeft, History, Play, RotateCcw, WandSparkles } from 'lucide-react';
import { icKonum, icUrl } from '../../siteHaritasi';
import { navigateTo } from '../../router';
import { ilerlemeYaz, ozet, useIlerleme } from '../spots/cozucu/cozucuVeri';
import { bransTanim, type Brans } from '../spots/brans';
import { ccDers, ccDizin, ccKurulYukle, ccKurullar, paketAdi, paketKod, type KurulPaket } from './ccVeri';
import { KurulBos } from '../kurul/KurulSuzgec';
import { KurulSecici, kurulIcerikVar } from '../kurul/KurulSecici';
import '../../styles/soru-cozucu.css';

/**
 * Sınava hazırlan › Çıkmış çözücü (/kamplar/kurul<N>/cikmis-cozucu[/<branş>]; iç adres /cikmis-cozucu?kurul=&brans=).
 * Branş seçilir → kurul sınavındaki soru sayısı kadar çıkmış sorudan paketler → paket sesli soru çözücüde (EMA) birlikte
 * çözülür (&ders=<paket kodu>&coz=1; yanlışlar &coz=yanlis; &coz=oto: asistan beklemeden çözer — soruyu ve şıkları okur,
 * doğru şıkkı seçer, nedenini ve kısa notu anlatır, sonraki soruya geçer). Veri: ccVeri.ts.
 */
const SoruCozucu = React.lazy(() => import('../spots/cozucu/SoruCozucu'));

const oku = () => {
  const sp = new URLSearchParams(icKonum().search);
  const k = Number(sp.get('kurul'));
  const l = ccKurullar();
  return {
    // adresteki kurul her zaman uyulur (içeriği yoksa boş durum); yoksa içeriği olan en yeni kurul
    kurul: Number.isInteger(k) && k >= 1 && k <= 6 ? k : l[l.length - 1] ?? 1,
    brans: (sp.get('brans') || null) as Brans | null,
    ders: sp.get('ders'),
    coz: sp.get('coz'),
  };
};
const yaz = (p: Record<string, string | null>, push = false) => {
  try {
    const u = icUrl();
    Object.entries(p).forEach(([k, v]) => (v === null ? u.searchParams.delete(k) : u.searchParams.set(k, v)));
    history[push ? 'pushState' : 'replaceState'](history.state, '', u.pathname + u.search + u.hash);
  } catch { /* yok */ }
};

export const CikmisCozucuView: React.FC = () => {
  const [a, setA] = useState(oku);
  const [veri, setVeri] = useState<KurulPaket | null>(null);
  const ilerleme = useIlerleme();
  useEffect(() => {
    const f = () => setA(oku());
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  useEffect(() => { setVeri(null); ccKurulYukle(a.kurul).then(setVeri).catch(() => setVeri({ kurul: a.kurul, surum: '', branslar: [] })); }, [a.kurul]);

  const bp = veri?.branslar.find((b) => b.brans === a.brans) || null;
  const kaynak = useMemo(() => (a.brans ? {
    ders: ccDers, dizin: () => ccDizin(a.kurul, a.brans as Brans), etiket: 'çıkmış çözücü',
  } : undefined), [a.kurul, a.brans]);

  const bransSec = (b: Brans | null) => { yaz({ brans: b, ders: null, coz: null }, true); setA(oku()); window.scrollTo?.(0, 0); };
  const ac = (kod: string, mod?: 'yanlis' | 'oto') => { yaz({ ders: kod, coz: mod || '1' }); setA(oku()); };
  const kapat = () => { yaz({ coz: null }); setA(oku()); };

  if (!veri) return <p className="scs-bos">Yükleniyor…</p>;
  const secici = (
    <KurulSecici secili={a.kurul} yol={(k) => `/kamplar/kurul${k}/cikmis-cozucu`} icerik={(k) => kurulIcerikVar('cikmis_cozucu', k)} />
  );
  if (!veri.branslar.length) {
    return (
      <div className="scs">
        {secici}
        <KurulBos kurul={a.kurul} ne="çıkmış paketi" onTumu={() => navigateTo('/kamplar/kurul1/cikmis-cozucu')} tumuEtiket="Kurul 1 paketlerine git" />
      </div>
    );
  }

  const paketOzet = (kod: string, n: number) => ozet(ilerleme[kod], n);

  return (
    <div className="scs">
      {!bp ? (
        <>
          {secici}
          <header className="scs-head">
            <div className="scs-head-t">
              <h2><History aria-hidden />Çıkmış çözücü · Kurul {a.kurul}</h2>
              <span className="scs-count">{veri.branslar.reduce((t, b) => t + b.soru, 0)} çıkmış soru</span>
            </div>
            <p className="scs-desc">
              Her paket, o dersin kurul sınavındaki soru sayısı kadar çıkmış sorudan oluşur ve dersin tüm konularına yayılır.
              Yalnız kazanımı ders slaytlarında anlatılan sorular alındı. Sesli asistan soruyu okur, sen cevaplarsın; takılınca
              ipucu verir, her seçeneğin neden doğru ya da yanlış olduğunu anlatır.
            </p>
          </header>
          <ul className="scs-liste is-satir">
            {veri.branslar.map((b) => {
              const t = b.paketler.reduce((s, p) => s + paketOzet(paketKod(a.kurul, b.brans, p.no), p.sorular.length).cozulen, 0);
              const bitti = b.paketler.filter((p) => paketOzet(paketKod(a.kurul, b.brans, p.no), p.sorular.length).tamam).length;
              return (
                <li key={b.brans} className="scs-row">
                  <button type="button" className="scs-row-b" onClick={() => bransSec(b.brans)}>
                    <span className="scs-no">{b.sinavSoru}</span>
                    <span className="scs-ad">
                      <b>{bransTanim(b.brans).ad}</b>
                      <small>Sınavda {b.sinavSoru} soru · {b.paketler.length} paket · {b.soru} çıkmış{t ? ` · ${t} çözüldü` : ''}{bitti ? ` · ${bitti} paket bitti` : ''}</small>
                    </span>
                    <span className="scs-durum"><Play aria-hidden />Aç</span>
                  </button>
                </li>
              );
            })}
          </ul>
        </>
      ) : (
        <>
          <header className="scs-head">
            <button type="button" className="scs-btn-sure" onClick={() => bransSec(null)}><ChevronLeft aria-hidden /><span>Dersler</span></button>
            <div className="scs-head-t">
              <h2><History aria-hidden />{bransTanim(bp.brans).ad} · Çıkmış çözücü</h2>
              <span className="scs-count">{bp.paketler.length} paket · {bp.soru} soru</span>
            </div>
            <p className="scs-desc">
              Kurul {a.kurul} sınavında {bransTanim(bp.brans).ad} {bp.sinavSoru} soru; her paket {bp.sinavSoru} çıkmış sorudur ve
              sınavdaki gibi tüm konulara dağılır. Birlikte çöz: şıkkı seç, yanlışsa nedenini dinle, yeniden dene; çözümden sonra konunun kısa notu gelir. Otomatik çözde asistan seni beklemeden doğru şıkkı seçip nedenini anlatır ve devam eder.
            </p>
          </header>
          <ul className="scs-liste is-satir">
            {bp.paketler.map((p) => {
              const kod = paketKod(a.kurul, bp.brans, p.no);
              const o = paketOzet(kod, p.sorular.length);
              const y = o.d2 + o.y;
              const devam = !o.tamam && o.cozulen > 0;
              const w = (n: number) => `${(n / p.sorular.length) * 100}%`;
              return (
                <li key={kod} className={`scs-row${o.tamam ? ' is-tamam' : ''}`}>
                  <button type="button" className="scs-row-b" onClick={() => ac(kod)}>
                    <span className="scs-no">{p.no}</span>
                    <span className="scs-ad">
                      <b>{paketAdi(bp, p)}</b>
                      <small>{p.sorular.length} soru · {p.ders} konu{o.cozulen ? ` · ${o.d}/${o.cozulen} ilk denemede doğru` : ''}</small>
                      {o.cozulen > 0 && <span className="scs-cubuk" aria-hidden><i className="is-d" style={{ width: w(o.d) }} /><i className="is-d2" style={{ width: w(o.d2) }} /><i className="is-y" style={{ width: w(o.y) }} /></span>}
                    </span>
                    <span className={`scs-durum${devam ? ' is-devam' : ''}`}>{o.tamam ? <><Check aria-hidden />Bitti</> : devam ? <>Devam</> : <><Play aria-hidden />Başla</>}</span>
                  </button>
                  {(
                    <div className="scs-row-ek">
                      <button type="button" onClick={() => ac(kod, 'oto')} title="Asistan seni beklemeden soruyu okur, doğru şıkkı seçer, nedenini ve kısa notu anlatır, sonrakine geçer"><WandSparkles aria-hidden />Otomatik çöz</button>
                      {y > 0 && <button type="button" onClick={() => ac(kod, 'yanlis')}><RotateCcw aria-hidden />Yanlışlarım · {y}</button>}
                      {o.tamam && <button type="button" onClick={() => { ilerlemeYaz(kod, null); ac(kod); }}><RotateCcw aria-hidden />Baştan çöz</button>}
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        </>
      )}

      {bp && a.ders && a.coz && kaynak && (
        <React.Suspense fallback={null}>
          <SoruCozucu key={`${a.ders}-${a.coz}`} brans={bp.brans} kod={a.ders} mod={a.coz === 'yanlis' ? 'yanlis' : undefined} otoBasla={a.coz === 'oto'}
            kaynak={kaynak} onClose={kapat} onDersDegis={(k) => yaz({ ders: k, coz: '1' })} />
        </React.Suspense>
      )}
    </div>
  );
};

export default CikmisCozucuView;
