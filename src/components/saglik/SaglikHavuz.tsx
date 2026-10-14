import React, { useEffect, useMemo, useState } from 'react';
import { AlertTriangle, BrainCircuit, ChevronDown, Crosshair, Search, Star, X } from 'lucide-react';
import { Atif, Blok, IcBag, KendiniSina, Kpi, OkunurTablo, Rozet, SlaytBag, useGenislik } from './SaglikOrtak';
import { pathFor } from '../../router';
import type { MaddeOge } from './saglikBaglam';
import type { BolumProps } from './SaglikBolumler';
import { havuzYukle, kucukHarf, sayi, type HavuzBaslik, type HavuzBilgi, type HavuzKonu, type HavuzVeri } from './saglikVeri';

/**
 * Sınav bilgi havuzu (src/data/saglik/havuz.json — 5 araştırma grubunun birleşimi). Halk Sağlığı çıkmış sorularından
 * çıkarılan "bilinmesi gereken bilgi → başlık → konu" ağacı; her bilgi: durum (soruldu / muhtemel / resmî), önem (1–3),
 * soru kimlikleri (çıkmışlarda açılır), kaynak + slayt. Konunun sonunda yalnız o konunun sorularıyla "Kendini sına".
 */

type Durum = 'hepsi' | 'soruldu' | 'muhtemel' | 'resmi';
const DURUM_AD: Record<Exclude<Durum, 'hepsi'>, string> = { soruldu: 'Soruldu', muhtemel: 'Muhtemel', resmi: 'Resmî veri' };
const DURUM_TON: Record<Exclude<Durum, 'hepsi'>, 'accent' | 'warn' | 'ok'> = { soruldu: 'accent', muhtemel: 'warn', resmi: 'ok' };

const MiniSatir: React.FC<{ metin: string }> = ({ metin }) => (
  <>{metin.split(/(\*\*[^*]+\*\*|==[^=]+==|\[EN SIK\]|\[İLK\])/g).map((p, i) => {
    if (p.startsWith('**') && p.endsWith('**')) return <strong key={i}>{p.slice(2, -2)}</strong>;
    if (p.startsWith('==') && p.endsWith('==')) return <mark key={i}>{p.slice(2, -2)}</mark>;
    if (p === '[EN SIK]') return <span key={i} className="sbk-vurgu-etiket">en sık</span>;
    if (p === '[İLK]') return <span key={i} className="sbk-vurgu-etiket">ilk</span>;
    return <React.Fragment key={i}>{p}</React.Fragment>;
  })}</>
);

const Onem: React.FC<{ n?: number }> = ({ n = 1 }) => (
  <span className={`sbk-onem o-${n}`} title={n >= 3 ? 'Çok önemli: birden çok kez soruldu ya da ders notunda vurgulu' : n === 2 ? 'Önemli: sorulmuş' : 'Muhtemel'} aria-label={`Önem ${n}/3`}>
    {[1, 2, 3].map((i) => <i key={i} className={i <= n ? 'is-dolu' : ''} />)}
  </span>
);

const BilgiSatiri: React.FC<{ b: HavuzBilgi & { vurgu?: string | string[] } }> = ({ b }) => {
  const [sorular, setSorular] = useState(false);
  const durum = (b.durum || 'muhtemel') as Exclude<Durum, 'hepsi'>;
  const vurgu = Array.isArray(b.vurgu) ? b.vurgu : b.vurgu ? [b.vurgu] : [];
  return (
    <li className={`sbk-bilgi d-${durum}`}>
      <Onem n={b.onem} />
      <div className="sbk-bilgi-g">
        <p>
          <MiniSatir metin={b.metin} />
          <Atif id={b.kaynak} />
          <SlaytBag kaynak={b.kaynak} slayt={b.slayt} />
        </p>
        <div className="sbk-bilgi-m">
          <Rozet ton={DURUM_TON[durum] || 'nötr'}>{DURUM_AD[durum] || durum}</Rozet>
          {vurgu.map((v) => <span key={v} className="sbk-vurgu-etiket">{v}</span>)}
          {(b.sorular?.length || 0) > 0 && (
            <button type="button" className="sbk-bilgi-soru" onClick={() => setSorular((x) => !x)} aria-expanded={sorular}>
              {b.sorular!.length} çıkmış soru <ChevronDown aria-hidden />
            </button>
          )}
        </div>
        {sorular && (
          <div className="sbk-bilgi-sorular">
            {b.sorular!.map((id, i) => (
              <IcBag key={id} to={`${pathFor('past_exams')}/${encodeURIComponent(id)}`} className="sbk-capa-a">Soru {i + 1}</IcBag>
            ))}
          </div>
        )}
      </div>
    </li>
  );
};

const bilgiUyar = (b: HavuzBilgi, durum: Durum, onemli: boolean, k: string) =>
  (durum === 'hepsi' || (b.durum || 'muhtemel') === durum) && (!onemli || (b.onem || 1) >= 3) && (!k || kucukHarf(b.metin).includes(k));

const BaslikBolumu: React.FC<{ h: HavuzBaslik; durum: Durum; onemli: boolean; k: string; acikBaslangic: boolean }> = ({ h, durum, onemli, k, acikBaslangic }) => {
  const [acik, setAcik] = useState(acikBaslangic);
  useEffect(() => { if (k) setAcik(true); }, [k]);
  const bilgiler = h.bilgiler.filter((b) => bilgiUyar(b, durum, onemli, k));
  const tablolar = (h.tablolar || []).filter((t) => !k || kucukHarf(`${t.baslik} ${t.satirlar.flat().join(' ')}`).includes(k));
  if (!bilgiler.length && !tablolar.length && !(durum === 'hepsi' && !onemli && !k && h.tuzaklar?.length)) return null;
  const sorulan = h.bilgiler.filter((b) => b.durum === 'soruldu').length;
  return (
    <section className={`sbk-havuz-baslik ${acik ? 'is-acik' : ''}`}>
      <button type="button" className="sbk-havuz-bb" onClick={() => setAcik((x) => !x)} aria-expanded={acik}>
        <span>{h.baslik}</span>
        <small>{bilgiler.length} bilgi{sorulan ? ` · ${sorulan} sorulmuş` : ''}{tablolar.length ? ` · ${tablolar.length} tablo` : ''}</small>
        <ChevronDown aria-hidden />
      </button>
      {acik && (
        <div className="sbk-havuz-ic">
          {bilgiler.length > 0 && <ul className="sbk-bilgi-l">{bilgiler.map((b, i) => <BilgiSatiri key={i} b={b} />)}</ul>}
          {tablolar.map((t) => (
            <div key={t.baslik} className="sbk-havuz-tablo">
              <h5>{t.baslik}<Atif id={t.kaynak} /></h5>
              <OkunurTablo
                baslik={t.baslik}
                sutunlar={t.sutunlar.map((s, i) => ({ anahtar: `c${i}`, ad: s }))}
                satirlar={t.satirlar.map((r) => Object.fromEntries(r.map((c, i) => [`c${i}`, i === 0 ? <b><MiniSatir metin={String(c ?? '')} /></b> : <MiniSatir metin={String(c ?? '—')} />])))}
              />
            </div>
          ))}
          {(h.tuzaklar?.length || 0) > 0 && durum === 'hepsi' && (
            <div className="sbk-tuzak">
              <h5><AlertTriangle aria-hidden /> Sınav tuzakları</h5>
              <ul>{h.tuzaklar!.map((x, i) => <li key={i}><MiniSatir metin={x} /></li>)}</ul>
            </div>
          )}
        </div>
      )}
    </section>
  );
};

const KonuIcerik: React.FC<{ x: HavuzKonu; durum: Durum; onemli: boolean; k: string }> = ({ x, durum, onemli, k }) => (
  <div className="sbk-havuz-konu">
    <header>
      <h3>{x.konu}</h3>
      <p className="sbk-muted">Kurul {x.kurul ?? '?'} · {x.soru_sayisi ?? 0} çıkmış soru · {x.basliklar.length} başlık</p>
      {x.ozet && <p><MiniSatir metin={x.ozet} /></p>}
    </header>
    {x.basliklar.map((hb, i) => <BaslikBolumu key={hb.id || hb.baslik} h={hb} durum={durum} onemli={onemli} k={k} acikBaslangic={i < 2 || !!k} />)}
  </div>
);

const konuMaddeleri = (k: HavuzKonu): MaddeOge => ({
  metin: `**${k.konu}** (Kurul ${k.kurul ?? '?'}, ${k.soru_sayisi ?? 0} soru)`,
  alt: k.basliklar.map((h) => ({
    metin: `**${h.baslik}**`,
    alt: [
      ...h.bilgiler.map((b) => ({ metin: `${b.metin} — ${DURUM_AD[(b.durum || 'muhtemel') as Exclude<Durum, 'hepsi'>] || b.durum}${b.sorular?.length ? ` (${b.sorular.length} soru)` : ''}`, kaynak: b.kaynak } as MaddeOge)),
      ...(h.tuzaklar || []).map((t) => `Tuzak: ${t}`),
    ],
  })),
});

export const HavuzBolum: React.FC<BolumProps> = ({ v }) => {
  const [h, setH] = useState<HavuzVeri | null>(v.havuz || null);
  const [hata, setHata] = useState(false);
  useEffect(() => {
    if (h) return;
    let iptal = false;
    havuzYukle().then((x) => { if (!iptal) setH(x); }).catch(() => { if (!iptal) setHata(true); });
    return () => { iptal = true; };
  }, [h]);
  const konular = useMemo(() => [...(h?.konular || [])].sort((a, b) => Number(a.kurul) - Number(b.kurul) || (b.soru_sayisi || 0) - (a.soru_sayisi || 0)), [h]);
  const [sec, setSec] = useState<string | null>(() => { try { return new URLSearchParams(window.location.search).get('konu'); } catch { return null; } });
  useEffect(() => {
    const f = () => { try { const x = new URLSearchParams(window.location.search).get('konu'); if (x) setSec(x); } catch { /* adres okunamadı */ } };
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  const [q, setQ] = useState('');
  const [durum, setDurum] = useState<Durum>('hepsi');
  const [onemli, setOnemli] = useState(false);
  const [sina, setSina] = useState(false);
  const [ref, w] = useGenislik<HTMLDivElement>();
  const dar = w > 0 && w < 860;
  const k = kucukHarf(q.trim());
  const konu = konular.find((x) => x.id === sec) || konular[0];
  useEffect(() => { setSina(false); }, [sec]);

  const istatistik = useMemo(() => {
    let bilgi = 0, soruldu = 0, muhtemel = 0, resmi = 0, tablo = 0, baslik = 0;
    const soru = new Set<string>();
    for (const x of konular) for (const hb of x.basliklar) {
      baslik++; tablo += hb.tablolar?.length || 0;
      for (const b of hb.bilgiler) { bilgi++; if (b.durum === 'soruldu') soruldu++; else if (b.durum === 'resmi') resmi++; else muhtemel++; b.sorular?.forEach((s) => soru.add(s)); }
    }
    return { bilgi, soruldu, muhtemel, resmi, tablo, baslik, soru: soru.size };
  }, [konular]);

  // Arama: tüm konularda eşleşen başlıklar
  const aramaKonulari = useMemo(() => (k ? konular.filter((x) => x.basliklar.some((hb) => hb.bilgiler.some((b) => bilgiUyar(b, durum, onemli, k)) || kucukHarf(hb.baslik).includes(k))) : []), [konular, k, durum, onemli]);
  const konuSorulari = useMemo(() => [...new Set((konu?.basliklar || []).flatMap((hb) => hb.bilgiler.flatMap((b) => b.sorular || [])))], [konu]);

  if (hata) return <p className="sbk-bos">Bilgi havuzu yüklenemedi.</p>;
  if (!h) return <div className="sbk-durum is-yuk" aria-busy="true"><span className="ui-skel" style={{ height: 220 }} /></div>;
  if (!konular.length) return <p className="sbk-bos">Bilgi havuzu henüz derlenmedi.</p>;

  const kurullar = [...new Set(konular.map((x) => String(x.kurul ?? '?')))];

  return (
    <>
      <Blok baslik="Sınav bilgi havuzu" ikon={BrainCircuit} genis alt="Çıkmış sorulardan çıkarılan bilgiler; ders notu, Öğren slaytı ve Sağlık Bakanlığı kaynaklarıyla tamamlandı" maddeler={() => konular.map(konuMaddeleri)}>
        <div className="sbk-kpi-g">
          <Kpi ad="Konu" deger={konular.length} not={`${istatistik.baslik} başlık`} />
          <Kpi ad="Bilgi" deger={sayi(istatistik.bilgi)} not={`${istatistik.soruldu} sorulmuş · ${istatistik.muhtemel} muhtemel · ${istatistik.resmi} resmî`} />
          <Kpi ad="Kapsanan çıkmış soru" deger={sayi(istatistik.soru)} />
          <Kpi ad="Tablo" deger={istatistik.tablo} />
        </div>
      </Blok>

      <div className="sbk-havuz-arac">
        <label className="sbk-ara">
          <Search aria-hidden />
          <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Tüm havuzda ara (ör. Kessner, BCG, insidans)" aria-label="Bilgi havuzunda ara" />
          {q && <button type="button" className="sbk-ara-sil" onClick={() => setQ('')} aria-label="Aramayı temizle"><X aria-hidden /></button>}
        </label>
        <div className="sbk-seg" role="radiogroup" aria-label="Bilgi türü">
          {(['hepsi', 'soruldu', 'muhtemel', 'resmi'] as Durum[]).map((d) => (
            <button key={d} type="button" role="radio" aria-checked={durum === d} className={durum === d ? 'is-sec' : ''} onClick={() => setDurum(d)}>{d === 'hepsi' ? 'Tümü' : DURUM_AD[d]}</button>
          ))}
        </div>
        <button type="button" className={`sbk-btn ${onemli ? 'is-dolu' : ''}`} aria-pressed={onemli} onClick={() => setOnemli((x) => !x)}><Star aria-hidden /> Yalnız çok önemli</button>
      </div>

      {k ? (
        <section className="sbk-blok" aria-live="polite">
          <h3 className="sbk-havuz-sonuc">"{q}" için {aramaKonulari.length} konu</h3>
          {aramaKonulari.map((x) => <KonuIcerik key={x.id} x={x} durum={durum} onemli={onemli} k={k} />)}
          {!aramaKonulari.length && <p className="sbk-bos">Eşleşen bilgi yok.</p>}
        </section>
      ) : (
        <div ref={ref} className={`sbk-havuz ${dar ? 'is-dar' : ''}`}>
          {dar ? (
            <label className="sbk-alan sbk-havuz-sec">
              <span>Konu</span>
              <select className="sbk-sec" value={konu?.id} onChange={(e) => setSec(e.target.value)}>
                {kurullar.map((kr) => (
                  <optgroup key={kr} label={`Kurul ${kr}`}>
                    {konular.filter((x) => String(x.kurul ?? '?') === kr).map((x) => <option key={x.id} value={x.id}>{x.konu} ({x.soru_sayisi ?? 0} soru)</option>)}
                  </optgroup>
                ))}
              </select>
            </label>
          ) : (
            <nav className="sbk-havuz-nav" aria-label="Konular">
              {kurullar.map((kr) => (
                <div key={kr}>
                  <h4>Kurul {kr}</h4>
                  <ul>
                    {konular.filter((x) => String(x.kurul ?? '?') === kr).map((x) => (
                      <li key={x.id}>
                        <button type="button" aria-current={x.id === konu?.id ? 'true' : undefined} onClick={() => setSec(x.id)}>
                          <span>{x.konu}</span><small>{x.soru_sayisi ?? 0}</small>
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </nav>
          )}
          {konu && (
            <div className="sbk-havuz-sag">
              <KonuIcerik key={konu.id} x={konu} durum={durum} onemli={onemli} k={k} />
              {konuSorulari.length > 0 && (
                sina ? (
                  <KendiniSina bolum="havuz" baslik={konu.konu} toplam={konuSorulari.length} idler={konuSorulari} />
                ) : (
                  <button type="button" className="sbk-btn is-dolu sbk-havuz-sina" onClick={() => setSina(true)}><Crosshair aria-hidden /> Bu konunun {konuSorulari.length} çıkmış sorusuyla kendini sına</button>
                )
              )}
            </div>
          )}
        </div>
      )}

      {(h.anahtar_suphesi?.length || 0) > 0 && (
        <details className="sbk-dogrulanamayan">
          <summary><AlertTriangle aria-hidden /> Cevap anahtarı şüpheli çıkmış sorular ({h.anahtar_suphesi!.length})</summary>
          <p>Bu soruların kayıtlı cevabı ders notuyla çelişiyor; havuzdaki bilgi ders notuna göre yazıldı. Çıkmış soru kaydı değiştirilmedi.</p>
          <ul>{h.anahtar_suphesi!.map((x) => (
            <li key={x.soru}><AlertTriangle aria-hidden /><span><IcBag to={`${pathFor('past_exams')}/${encodeURIComponent(x.soru)}`}>Soruyu aç</IcBag> — kayıtlı {x.kayitli}, olması gereken {x.olmasi_gereken}. {x.gerekce}</span></li>
          ))}</ul>
        </details>
      )}
    </>
  );
};
