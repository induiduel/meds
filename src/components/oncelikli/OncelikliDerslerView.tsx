/**
 * Öncelikli dersler (/oncelikli-dersler, Başvuru): sesli dersleri "az ezber, mantıkla çözülür, çıkmışı kolay, kısa,
 * puan getirisi yüksek" ölçütlerine göre sıralar. Öğrenci hazır profil seçer ya da ağırlıkları kendisi ayarlar,
 * eşik süzgeçleri ve branşla daraltır. Bitirdiği sesli dersler (calismaTakip 'sesli:<key>') işaretlidir;
 * "Çalışabileceklerim" yalnız bitmemişleri listeler. Algoritma: oncelikliModel.ts; veri: scripts/oncelikli_dersler.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { ChevronDown, Gauge, Headphones, SlidersHorizontal } from 'lucide-react';
import { bittiMi, sesliKonuId, useTakip, sureYaz } from '../../services/calismaTakip';
import { KonuIsaret } from '../takip/KonuTakip';
import { navigateTo, pathFor } from '../../router';
import {
  BOYUTLAR, ESIK, PROFILLER, TUR_AD, esikGecer, oncelikPuani, veriYukle,
  type Agirlik, type Boyut, type DersTuru, type OncelikliDers, type OncelikliVeri,
} from './oncelikliModel';
import '../../styles/takip.css';
import '../../styles/oncelikli.css';
import '../../styles/v15/liste2.css';

const BRANS_AD: Record<string, string> = {
  patoloji: 'Patoloji', enfeksiyon: 'Enfeksiyon', uroloji: 'Üroloji', genetik: 'Genetik',
  halksagligi: 'Halk Sağlığı', kadindogum: 'Kadın Doğum', farmakoloji: 'Farmakoloji',
};
type Durum = 'kalan' | 'tum' | 'biten';
const DURUM_AD: Record<Durum, string> = { kalan: 'Çalışabileceklerim', tum: 'Tümü', biten: 'Bitirdiklerim' };
const KONU_SIRA: Record<DersTuru, number> = { mantik: 0, karma: 1, ezber: 2 };
const TUR_KISA: Record<DersTuru, string> = { mantik: 'Mantık', karma: 'Karma', ezber: 'Ezber' };
const AYAR_KEY = 'medsoru_oncelikli_ayar_v1';

interface Ayar { profil: string; agirlik: Agirlik; esik: Boyut[]; brans: string[]; tur: DersTuru[]; durum: Durum }
const VARSAYILAN: Ayar = { profil: 'kolay', agirlik: PROFILLER[0].agirlik, esik: [], brans: [], tur: [], durum: 'kalan' };
const ayarOku = (): Ayar => {
  try { return { ...VARSAYILAN, ...JSON.parse(localStorage.getItem(AYAR_KEY) || '{}') }; } catch { return VARSAYILAN; }
};

const sayi = (n: number, k = 0) => n.toLocaleString('tr-TR', { maximumFractionDigits: k });
const ac = (key: string) => navigateTo(pathFor('canli_ders', key));

export default function OncelikliDerslerView() {
  const [veri, setVeri] = useState<OncelikliVeri | null>(null);
  const [hata, setHata] = useState(false);
  const [ayar, setAyar0] = useState<Ayar>(ayarOku);
  const [ayarAcik, setAyarAcik] = useState(false);
  const [nasil, setNasil] = useState(false);
  const [acik, setAcik] = useState<string | null>(null);
  const takip = useTakip();

  useEffect(() => { document.title = 'Öncelikli dersler · MeDSor'; }, []);
  useEffect(() => { veriYukle(1).then(setVeri, () => setHata(true)); }, []);
  const setAyar = (f: (a: Ayar) => Ayar) => setAyar0((a) => {
    const y = f(a);
    try { localStorage.setItem(AYAR_KEY, JSON.stringify(y)); } catch { /* özel pencere */ }
    return y;
  });
  const degistir = <T,>(l: T[], x: T) => (l.includes(x) ? l.filter((y) => y !== x) : [...l, x]);

  const durumOf = (d: OncelikliDers) => {
    const k = takip.k[`sesli:${sesliKonuId(d.key)}`];
    return { bitti: bittiMi(k), basladi: !!k && k.sn > 60 };
  };

  const satirlar = useMemo(() => {
    if (!veri) return [];
    return veri.dersler
      .map((d) => ({ d, p: oncelikPuani(d, ayar.agirlik), ...durumOf(d) }))
      .sort((a, b) => b.p - a.p || b.d.beklenen - a.d.beklenen)
      .map((x, i) => ({ ...x, sira: i + 1 }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [veri, ayar.agirlik, takip]);

  const gorunen = satirlar.filter(({ d, bitti }) =>
    (ayar.durum === 'tum' || (ayar.durum === 'biten') === bitti)
    && (!ayar.brans.length || ayar.brans.includes(d.brans))
    && (!ayar.tur.length || ayar.tur.includes(d.tur))
    && esikGecer(d, ayar.esik));

  const ozet = useMemo(() => {
    const kalan = satirlar.filter((x) => !x.bitti);
    return {
      biten: satirlar.length - kalan.length,
      toplam: satirlar.length,
      gorunenSn: gorunen.reduce((s, x) => s + (x.d.sureSn || 0), 0),
      gorunenSoru: gorunen.reduce((s, x) => s + x.d.beklenen, 0),
    };
  }, [satirlar, gorunen]);

  const branslar = useMemo(() => [...new Set(veri?.dersler.map((d) => d.brans) || [])], [veri]);

  return (
    <div className="bd od">
      <header className="bd-bas">
        <span className="bd-ic" aria-hidden><Gauge /></span>
        <div>
          <h1>Öncelikli dersler</h1>
          <p>Sesli dersler ezber yüküne, mantıkla çözülebilmesine ve çıkmışlarına göre sıralandı. Az ezberli, kolay puan getiren derslerden başla.</p>
        </div>
      </header>

      {hata && <div className="bd-bos"><p>Analiz yüklenemedi. Sayfayı yenile.</p></div>}
      {!veri && !hata && <div className="bd-bos" role="status"><span className="bd-spin" aria-hidden /> Dersler yükleniyor…</div>}

      {veri && (
        <>
          {/* tasarım B19 pano: görünen (süzgeçten geçen, bitmemiş) derslerin sayısı, dinleme süresi, beklenen soru;
              branş başına puan/emek (beklenen soru ÷ saat) çubukları — veri oncelikliModel'den, uydurma yok */}
          {(() => {
            const kalan = gorunen.filter((x) => !x.bitti);
            const sn = kalan.reduce((a, x) => a + (x.d.sureSn || 0), 0);
            const soru = kalan.reduce((a, x) => a + x.d.beklenen, 0);
            const br = branslar.map((b) => {
              const l = satirlar.filter((x) => x.d.brans === b && !x.bitti);
              const saat = l.reduce((a, x) => a + (x.d.sureSn || 0), 0) / 3600;
              return { b, v: saat > 0 ? l.reduce((a, x) => a + x.d.beklenen, 0) / saat : 0 };
            }).filter((x) => x.v > 0);
            const enc = Math.max(...br.map((x) => x.v), 0.0001);
            const en = br.slice().sort((x, y) => y.v - x.v)[0];
            return (
              <section className="od15-pano v15-card" aria-label="Kolay puan özeti">
                <span className="v15-label">Bu süzgeçte kolay puan</span>
                <div className="od15-buyuk"><b>{kalan.length}</b><span>ders · ~{sureYaz(sn)} dinleme<br /><em>≈ {sayi(soru, 0)} soru getirir</em></span></div>
                {br.length > 1 && (
                  <>
                    <div className="od15-cubuk" role="img" aria-label={`Branşlara göre puan/emek oranı; en verimli ${BRANS_AD[en?.b] || en?.b}`}>
                      {br.map((x) => <span key={x.b} className={x.b === en?.b ? 'is-on' : ''}><i style={{ height: `${Math.max(8, (x.v / enc) * 100)}%` }} /><small>{(BRANS_AD[x.b] || x.b).slice(0, 4)}</small></span>)}
                    </div>
                    <div className="od15-alt"><span>Puan / emek oranı (soru ÷ saat)</span><span>{BRANS_AD[en.b] || en.b} en verimli</span></div>
                  </>
                )}
              </section>
            );
          })()}
          <div className="od-profil" role="radiogroup" aria-label="Öncelik profili">
            {PROFILLER.map((p) => (
              <button key={p.id} type="button" role="radio" aria-checked={ayar.profil === p.id}
                className={`od-profil-k${ayar.profil === p.id ? ' is-on' : ''}`}
                onClick={() => setAyar((a) => ({ ...a, profil: p.id, agirlik: p.agirlik }))}>
                <b>{p.ad}</b><small>{p.ne}</small>
              </button>
            ))}
          </div>

          <section className="od-suz" aria-label="Süzgeçler">
            <div className="od-satir">
              <div className="bd-suz" role="group" aria-label="Duruma göre">
                {(Object.keys(DURUM_AD) as Durum[]).map((k) => (
                  <button key={k} type="button" aria-pressed={ayar.durum === k} className={ayar.durum === k ? 'is-on' : ''}
                    onClick={() => setAyar((a) => ({ ...a, durum: k }))}>{DURUM_AD[k]}</button>
                ))}
              </div>
              <button type="button" className={`od-ayar-dug${ayarAcik ? ' is-on' : ''}`} aria-expanded={ayarAcik} onClick={() => setAyarAcik((x) => !x)}>
                <SlidersHorizontal aria-hidden /> Ağırlıklar
              </button>
            </div>

            <div className="od-cipler" role="group" aria-label={`En az ${ESIK} puan olsun`}>
              <span className="od-cip-l">Şart koş:</span>
              {BOYUTLAR.map((b) => (
                <button key={b.id} type="button" title={b.ne} aria-pressed={ayar.esik.includes(b.id)}
                  className={`od-cip${ayar.esik.includes(b.id) ? ' is-on' : ''}`}
                  onClick={() => setAyar((a) => ({ ...a, esik: degistir(a.esik, b.id) }))}>{b.ad}</button>
              ))}
            </div>
            <div className="od-cipler" role="group" aria-label="Ders türü ve branş">
              {(Object.keys(TUR_AD) as DersTuru[]).map((t) => (
                <button key={t} type="button" aria-pressed={ayar.tur.includes(t)}
                  className={`od-cip is-tur-${t}${ayar.tur.includes(t) ? ' is-on' : ''}`}
                  onClick={() => setAyar((a) => ({ ...a, tur: degistir(a.tur, t) }))}>{TUR_AD[t]}</button>
              ))}
              <span className="od-ayrac" aria-hidden />
              {branslar.map((b) => (
                <button key={b} type="button" aria-pressed={ayar.brans.includes(b)}
                  className={`od-cip${ayar.brans.includes(b) ? ' is-on' : ''}`}
                  onClick={() => setAyar((a) => ({ ...a, brans: degistir(a.brans, b) }))}>{BRANS_AD[b] || b}</button>
              ))}
            </div>

            {ayarAcik && (
              <div className="od-agirlik">
                {BOYUTLAR.map((b) => (
                  <label key={b.id} className="od-ag">
                    <span><b>{b.ad}</b><small>{b.ne}</small></span>
                    <input type="range" min={0} max={3} step={0.5} value={ayar.agirlik[b.id]}
                      onChange={(e) => { const v = Number(e.target.value); setAyar((a) => ({ ...a, profil: 'ozel', agirlik: { ...a.agirlik, [b.id]: v } })); }} />
                    <em>{sayi(ayar.agirlik[b.id], 1)}</em>
                  </label>
                ))}
              </div>
            )}
          </section>

          <div className="od-ozet" role="status">
            <span><b>{ozet.biten}</b>/{ozet.toplam} ders bitti</span>
            <span><b>{gorunen.length}</b> ders listede</span>
            {ozet.gorunenSn > 0 && <span><b>{sureYaz(ozet.gorunenSn)}</b> dinleme</span>}
            <span>sınavda ≈ <b>{sayi(ozet.gorunenSoru, 1)}</b> soru</span>
          </div>

          {!gorunen.length && (
            <div className="bd-bos"><p>{ayar.durum === 'biten' ? 'Henüz bitirdiğin sesli ders yok.' : 'Bu süzgeçlere uyan ders yok; bir şartı kaldır.'}</p></div>
          )}

          <ol className="od-liste">
            {gorunen.map(({ d, p, sira, bitti, basladi }) => {
              const acikMi = acik === d.key;
              return (
                <li key={d.key} className={`od-ders${bitti ? ' is-bitti' : ''}`}>
                  <div className="od-ust">
                    <span className="od-sira" aria-label={`${sira}. sıra`}>{sira}</span>
                    <button type="button" className="od-bas" aria-expanded={acikMi} onClick={() => setAcik(acikMi ? null : d.key)}>
                      <span className="od-ad">{d.baslik}</span>
                      <span className="od-meta">
                        <span>{BRANS_AD[d.brans]}</span>
                        <span className={`od-tur is-${d.tur}`}>{TUR_AD[d.tur]}</span>
                        {d.sureSn ? <span>{sureYaz(d.sureSn)}</span> : null}
                        <span>{d.cikmis} çıkmış</span>
                        {bitti ? <span className="od-durum is-bitti">Bitti</span> : basladi ? <span className="od-durum">Başladın</span> : null}
                      </span>
                    </button>
                    <span className="od-puan" title="Öncelik puanı (0–100)">{p}</span>
                    <KonuIsaret modul="sesli" konu={d.key} ad={d.baslik} />
                  </div>
                  <div className="od-bar" aria-hidden>
                    {BOYUTLAR.map((b) => {
                      const v = d.boyut[b.id];
                      return (
                        <span key={b.id} className="od-bar-k" title={`${b.ad}: ${v ?? 'bilinmiyor'}`}>
                          <small>{b.kisa}</small>
                          <i><s style={{ width: `${v ?? 0}%` }} className={v == null ? 'is-yok' : v >= 60 ? 'is-iyi' : v < 35 ? 'is-zor' : ''} /></i>
                        </span>
                      );
                    })}
                  </div>
                  {acikMi && (
                    <div className="od-detay">
                      {d.yz?.gerekce && <p className="od-gerekce">{d.yz.gerekce}</p>}
                      {d.yz?.konular && d.yz.konular.length > 0 && (
                        <div className="od-konular">
                          <small>Konular (önce mantıkla çözülenler):</small>
                          <ul>
                            {[...d.yz.konular].sort((x, y) => KONU_SIRA[x.tur] - KONU_SIRA[y.tur]).map((k, i) => (
                              <li key={i} className={`is-${k.tur}`}>
                                <span className={`od-tur is-${k.tur}`}>{TUR_KISA[k.tur]}</span> {k.baslik}{k.cikmis ? <em> · çıkmış</em> : null}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {d.yz?.ezberCekirdegi && d.yz.ezberCekirdegi.length > 0 && (
                        <p className="od-terim"><b className="od-etiket">Kaçınılmaz ezber:</b> {d.yz.ezberCekirdegi.join(', ')}</p>
                      )}
                      {d.yz?.cikmisNot && <p className="od-terim"><b className="od-etiket">Çıkmışlar:</b> {d.yz.cikmisNot}</p>}
                      <ul>
                        <li><b>{sayi(d.terim)}</b> farklı yabancı terim ({sayi(d.terim1000, 1)} / 1000 kelime) · <b>{d.ilac}</b> ilaç · <b>{d.hastalik}</b> hastalık/etken adı · <b>{d.sayi}</b> sayısal değer</li>
                        <li>Neden-sonuç bağlacı: <b>{sayi(d.mantik1000, 1)}</b> / 1000 kelime · anlatım <b>{sayi(d.kelime)}</b> kelime</li>
                        <li>
                          Çıkmış: <b>{d.cikmis}</b> soru, <b>{d.yil}</b> farklı yıl
                          {d.cikmisIsim != null && <> · isim soran soru %{Math.round(d.cikmisIsim * 100)} · olumsuz kök %{Math.round((d.cikmisNegatif || 0) * 100)}</>}
                        </li>
                        <li>Bu dersten sınavda beklenen ≈ <b>{sayi(d.beklenen, 1)}</b> soru</li>
                      </ul>
                      <button type="button" className="kt-btn" onClick={() => ac(d.key)}><Headphones aria-hidden /> Dersi dinle</button>
                    </div>
                  )}
                </li>
              );
            })}
          </ol>

          <section className="od-nasil">
            <button type="button" aria-expanded={nasil} onClick={() => setNasil((x) => !x)}>
              Sıralama nasıl hesaplanıyor? <ChevronDown aria-hidden />
            </button>
            {nasil && (
              <div>
                <p>Her sesli dersin anlatım metni ve o dersten gelmiş çıkmış sorular hem sayısal olarak ölçüldü hem de yapay zekâ tarafından baştan sona okunup değerlendirildi (ezber, mantık ve çıkmış puanlarında yapay zekâ yargısı %60, metin ölçümü %40). Her ders altı ölçütte 0–100 puan aldı (yüksek puan senin lehine):</p>
                <ul>
                  {BOYUTLAR.map((b) => <li key={b.id}><b>{b.ad}:</b> {b.ne}.</li>)}
                </ul>
                <p>Öncelik puanı, seçtiğin profildeki ağırlıklarla bu altı puanın ağırlıklı ortalamasıdır. Beklenen soru, branşın sınavdaki soru sayısının dersin çıkmış payına bölünmesiyle bulunur. “Şart koş” seçtiğin ölçütte {ESIK} puanın altındaki dersleri gizler.</p>
                <p>Ders türü: mantık ağırlıklı dersler hem az ezberli hem neden-sonuç yoğunudur; ezber ağırlıklılarda terim yükü yüksektir. Bunlar metinden çıkarılan ölçümlerdir; kendi zorlandığın dersi ağırlıklarla aşağı itebilirsin.</p>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}
