/**
 * Bitirdiklerim (/bitirdiklerim?m=sesli|ogren|cozucu|onem|kamp): beş modülde ders → konu kontrol listesi.
 * Her konu: bitti işareti (dokunarak), harcanan etkin süre, çözülen soru, tekrar turu; "Aç" / "Tekrar et".
 * Her ders ve modül için biten/kalan, toplam süre, soru ve ortalama hıza göre tahmini kalan süre.
 * Veri: services/calismaTakip (süre, soru, durum) + bitirdiklerimVeri (konu listeleri). Stil: styles/takip.css (.bd-*).
 */
import React, { useEffect, useMemo, useState } from 'react';
import { BookOpen, ChevronDown, Tent, Headphones, ListChecks, MessageCircleQuestion, Play, RotateCcw, Search, Star, X } from 'lucide-react';
import {
  MODUL_AD, bittiMi, sesHizi, grupOzeti, gunYaz, hizHesapla, sureYaz, tekrarBasla, useTakip, type Hiz, type TakipModul,
} from '../../services/calismaTakip';
import { KonuIsaret, KonuSureEtiketi } from './KonuTakip';
import { MODUL_YUKLE, type BdDers, type BdKonu } from './bitirdiklerimVeri';
import SinavPlani from './SinavPlani';
import '../../styles/takip.css';

const MODULLER: { id: TakipModul; ikon: React.ComponentType<{ 'aria-hidden'?: boolean }> }[] = [
  { id: 'sesli', ikon: Headphones },
  { id: 'ogren', ikon: BookOpen },
  { id: 'cozucu', ikon: MessageCircleQuestion },
  { id: 'onem', ikon: Star },
  { id: 'kamp', ikon: Tent },
];
const MODUL_KISA: Record<TakipModul, string> = { sesli: 'Sesli ders', ogren: 'Etkileşimli', cozucu: 'Soru çözücü', onem: 'En önemliler', kamp: 'Kurul kampı' };
type Suzgec = 'tum' | 'kalan' | 'biten' | 'tekrar';
const SUZGEC_AD: Record<Suzgec, string> = { tum: 'Tümü', kalan: 'Kalanlar', biten: 'Bitenler', tekrar: 'Tekrarda' };

const sayi = (n: number) => n.toLocaleString('tr-TR');
const katla = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
const urlModul = (): TakipModul => {
  try {
    const m = new URLSearchParams(location.search).get('m');
    return MODULLER.some((x) => x.id === m) ? (m as TakipModul) : 'sesli';
  } catch { return 'sesli'; }
};

type Durum = { yuk: true } | { hata: true } | { veri: BdDers[] };

export default function BitirdiklerimView() {
  const [modul, setModul0] = useState<TakipModul>(urlModul);
  const [durumlar, setDurumlar] = useState<Partial<Record<TakipModul, Durum>>>({});
  const [ara, setAra] = useState('');
  const [suzgec, setSuzgec] = useState<Suzgec>('tum');
  const [acik, setAcik] = useState<Record<string, boolean>>({});
  const takip = useTakip();

  useEffect(() => { document.title = 'Bitirdiklerim · MeDSor'; }, []);
  useEffect(() => {
    let canli = true;
    for (const { id } of MODULLER) {
      setDurumlar((d) => ({ ...d, [id]: { yuk: true } }));
      MODUL_YUKLE[id]().then(
        (veri) => canli && setDurumlar((d) => ({ ...d, [id]: { veri } })),
        () => canli && setDurumlar((d) => ({ ...d, [id]: { hata: true } })),
      );
    }
    return () => { canli = false; };
  }, []);

  const setModul = (m: TakipModul) => {
    setModul0(m);
    setAcik({});
    try {
      const u = new URL(location.href);
      u.searchParams.set('m', m);
      history.replaceState(history.state, '', u.pathname + u.search + u.hash);
    } catch { /* yok */ }
  };

  // Her modülün hızı ve özeti (sekme sayıları dahil)
  const ozetler = useMemo(() => {
    const r: Partial<Record<TakipModul, { hiz: Hiz; dersler: { d: BdDers; o: ReturnType<typeof grupOzeti> }[]; genel: ReturnType<typeof grupOzeti> }>> = {};
    for (const { id } of MODULLER) {
      const dz = durumlar[id];
      if (!dz || !('veri' in dz)) continue;
      const tum = dz.veri.flatMap((d) => d.konular);
      const hiz = hizHesapla(id, tum, takip);
      r[id] = { hiz, dersler: dz.veri.map((d) => ({ d, o: grupOzeti(id, d.konular, hiz, takip) })), genel: grupOzeti(id, tum, hiz, takip) };
    }
    return r;
  }, [durumlar, takip]);

  // plan modülü hızı değişmedikçe yeniden hesaplamasın
  const hizAnahtar = MODULLER.map(({ id }) => { const h = ozetler[id]?.hiz; return h ? `${h.oran.toFixed(2)}` : '-'; }).join('|');
  const planHiz = useMemo(() => Object.fromEntries(MODULLER.map(({ id }) => [id, ozetler[id]?.hiz]).filter(([, h]) => h)), [hizAnahtar]); // eslint-disable-line react-hooks/exhaustive-deps

  const dz = durumlar[modul];
  const oz = ozetler[modul];
  const q = katla(ara.trim());

  const konuDurumu = (k: BdKonu) => {
    const kayit = takip.k[`${modul}:${k.id}`];
    return { kayit, bitti: bittiMi(kayit, k.turetilen), tekrar: kayit?.durum === 'tekrar' };
  };
  const gorunur = (k: BdKonu) => {
    if (q && !katla(`${k.no ?? ''} ${k.ad} ${k.alt || ''}`).includes(q)) return false;
    if (suzgec === 'tum') return true;
    const s = konuDurumu(k);
    return suzgec === 'biten' ? s.bitti : suzgec === 'kalan' ? !s.bitti : s.tekrar;
  };
  // varsayılan açık ders: yarım kalanlar; hiç yoksa ilki
  const varsayilanAcik = (d: BdDers, o: ReturnType<typeof grupOzeti>, i: number) =>
    (o.biten > 0 && o.biten < o.toplam) || o.tekrarda > 0 || (i === 0 && !(oz?.dersler.some((x) => x.o.biten > 0 && x.o.biten < x.o.toplam)));

  return (
    <div className="bd">
      <header className="bd-bas">
        <span className="bd-ic" aria-hidden><ListChecks /></span>
        <div>
          <h1>Bitirdiklerim</h1>
          <p>Konuları işaretle; her konuda geçirdiğin süre, çözdüğün soru ve kalanların tahmini süresi burada.</p>
        </div>
      </header>

      <SinavPlani hiz={planHiz} />

      <div className="bd-modul" role="tablist" aria-label="Modül">
        {MODULLER.map(({ id, ikon: Ikon }) => {
          const g = ozetler[id]?.genel;
          const kalanSayi = g ? g.toplam - g.biten : 0;
          return (
            <button key={id} type="button" role="tab" aria-selected={modul === id} className={modul === id ? 'is-on' : ''} onClick={() => setModul(id)}>
              <Ikon aria-hidden />
              <span className="bd-modul-ad">{MODUL_AD[id]}</span>
              <span className="bd-modul-kisa" aria-hidden>{MODUL_KISA[id]}</span>
              <span className="bd-modul-n">
                {g ? `${g.biten}/${g.toplam}` : '…'}
                {g && kalanSayi > 0 && <em className="bd-modul-s"> · {sureYaz(g.kalanIcerikSn)}</em>}
              </span>
            </button>
          );
        })}
      </div>

      {!dz || 'yuk' in dz ? (
        <div className="bd-bos" role="status"><span className="bd-spin" aria-hidden /> Konular yükleniyor…</div>
      ) : 'hata' in dz ? (
        <div className="bd-bos"><p>{MODUL_AD[modul]} listesi alınamadı. Bağlantını kontrol edip sayfayı yenile.</p></div>
      ) : !oz || !dz.veri.length ? (
        <div className="bd-bos"><p>{MODUL_AD[modul]} için henüz konu yok.</p></div>
      ) : (
        <>
          <OzetKartlari genel={oz.genel} hiz={oz.hiz} modul={modul} />

          <div className="bd-arac">
            <label className="bd-ara">
              <Search aria-hidden />
              <input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Konu ara" aria-label="Konu ara" />
              {ara && <button type="button" onClick={() => setAra('')} aria-label="Aramayı temizle"><X aria-hidden /></button>}
            </label>
            <div className="bd-suz" role="group" aria-label="Duruma göre süz">
              {(Object.keys(SUZGEC_AD) as Suzgec[]).map((s) => {
                const n = s === 'tum' ? oz.genel.toplam : s === 'biten' ? oz.genel.biten : s === 'kalan' ? oz.genel.toplam - oz.genel.biten : oz.genel.tekrarda;
                if (s === 'tekrar' && !n) return null;
                return (
                  <button key={s} type="button" aria-pressed={suzgec === s} className={suzgec === s ? 'is-on' : ''} onClick={() => setSuzgec(s)}>
                    {SUZGEC_AD[s]} <span>{sayi(n)}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="bd-dersler">
            {oz.dersler.map(({ d, o }, i) => {
              const konular = d.konular.filter(gorunur);
              if (!konular.length) return null;
              const ac = q || suzgec !== 'tum' ? true : acik[d.id] ?? varsayilanAcik(d, o, i);
              const yuzde = o.toplam ? Math.round((o.biten / o.toplam) * 100) : 0;
              const kalanGun = gunYaz(o.kalanSn, oz.hiz.gunluk);
              return (
                <section key={d.id} className={`bd-ders${ac ? ' is-acik' : ''}${o.biten === o.toplam ? ' is-tamam' : ''}`} aria-label={d.ad}>
                  <button type="button" className="bd-ders-bas" aria-expanded={ac} onClick={() => setAcik((a) => ({ ...a, [d.id]: !ac }))}>
                    <span className="bd-ders-ust">
                      <b>{d.ad}</b>
                      <span className="bd-ders-n"><b>{o.biten}</b>/{o.toplam} bitti · %{yuzde}</span>
                      <ChevronDown aria-hidden className="bd-ok" />
                    </span>
                    <span className="bd-cubuk" aria-hidden><i style={{ width: `${yuzde}%` }} /></span>
                    <span className="bd-ders-meta">
                      <span>{sureYaz(o.sn)} çalıştın</span>
                      {o.soru > 0 && <span>{sayi(o.soru)} soru</span>}
                      {o.biten < o.toplam
                        ? (
                          <>
                            <span className="is-icerik">{o.toplam - o.biten} kalan ders · {sureYaz(o.kalanIcerikSn)} ders süresi 1× (toplam {sureYaz(o.toplamIcerikSn)})</span>
                            <span className="is-kalan">Hızına göre tahmini: ~{sureYaz(o.kalanSn)}{kalanGun ? ` (${kalanGun})` : ''}</span>
                          </>
                        )
                        : <span className="is-tamam">Tamamlandı · toplam {sureYaz(o.toplamIcerikSn)} ders süresi</span>}
                    </span>
                  </button>
                  {ac && (
                    <ul className="bd-konular">
                      {konular.map((k) => <KonuSatiri key={k.id} modul={modul} k={k} {...konuDurumu(k)} />)}
                    </ul>
                  )}
                </section>
              );
            })}
            {!oz.dersler.some(({ d }) => d.konular.some(gorunur)) && (
              <div className="bd-bos"><p>{q ? `“${ara}” ile eşleşen konu yok.` : `${SUZGEC_AD[suzgec]} listesinde konu yok.`}</p></div>
            )}
          </div>
        </>
      )}
    </div>
  );
}

function OzetKartlari({ genel, hiz, modul }: { genel: ReturnType<typeof grupOzeti>; hiz: Hiz; modul: TakipModul }) {
  const yuzde = genel.toplam ? Math.round((genel.biten / genel.toplam) * 100) : 0;
  const kalan = genel.toplam - genel.biten;
  const gun = gunYaz(genel.kalanSn, hiz.gunluk);
  const soruNot = modul === 'sesli' ? 'ilgili konuların soru çözücüsünde' : modul === 'ogren' ? 'derslerdeki etkileşimlerde' : 'bu modülde';
  return (
    <section className="bd-ozet" aria-label="Özet">
      <div className="bd-kart is-ana">
        <small>Biten konu</small>
        <b><span>{sayi(genel.biten)}</span>/{sayi(genel.toplam)}</b>
        <span className="bd-cubuk" aria-hidden><i style={{ width: `${yuzde}%` }} /></span>
        <em>%{yuzde} · {sayi(kalan)} konu kaldı</em>
      </div>
      <div className="bd-kart">
        <small>Toplam çalışma</small>
        <b>{sureYaz(genel.sn)}</b>
        <em>{hiz.gunluk ? `Günde ort. ${sureYaz(hiz.gunluk)} (son 14 gün, boş günler dahil; çalıştığın ${hiz.aktifGun} günde ${sureYaz(hiz.aktifGunluk)})` : 'Etkin süre: sekme açık ve etkileşimdeyken'}</em>
      </div>
      <div className="bd-kart">
        <small>Çözülen soru</small>
        <b>{sayi(genel.soru)}</b>
        <em>{soruNot}</em>
      </div>
      <div className="bd-kart">
        <small>Kalan ders süresi</small>
        <b>{kalan ? sureYaz(genel.kalanIcerikSn) : '—'}</b>
        <em>
          {!kalan
            ? `Hepsi bitti · toplam ${sureYaz(genel.toplamIcerikSn)}`
            : `1× ses hızında (${sayi(kalan)} kalan ders · toplam ${sureYaz(genel.toplamIcerikSn)})`}
        </em>
      </div>
      <div className="bd-kart">
        <small>Tahmini kalan (hızına göre)</small>
        <b>{kalan ? `~${sureYaz(genel.kalanSn)}` : '—'}</b>
        <em>
          {!kalan ? 'Hepsi bitti' : hiz.kaynak === 'senin'
            ? `Hızına göre (${hiz.ornek} konu, içerik süresinin %${Math.round(hiz.oran * 100)} kadarı)${gun ? ` · ${gun}` : ''}`
            : `${modul === 'sesli' || modul === 'onem' || modul === 'cozucu' ? `${sesHizi(modul).toLocaleString('tr-TR')}× ses hızına göre, ` : ''}çalışılan süre düşülerek; konu bitirdikçe hızına uyar${gun ? ` · ${gun}` : ''}`}
        </em>
      </div>
    </section>
  );
}

function KonuSatiri({ modul, k, bitti, tekrar }: { modul: TakipModul; k: BdKonu; bitti: boolean; tekrar: boolean }) {
  return (
    <li className={`bd-konu${bitti ? ' is-bitti' : ''}${tekrar ? ' is-tekrar' : ''}`}>
      <KonuIsaret modul={modul} konu={k.id} ad={k.ad} turetilen={k.turetilen} />
      <button type="button" className="bd-konu-ad" onClick={k.ac} title="Konuyu aç">
        {k.no != null && k.no !== '' && <span className="bd-no">{k.no}</span>}
        <span className="bd-konu-t">
          <b>{k.ad}</b>
          <small>
            {k.alt && <span>{k.alt}</span>}
            {k.beklenen > 0 && <span>~{sureYaz(k.beklenen)}</span>}
            {tekrar && <span className="bd-etiket">Tekrarda</span>}
          </small>
          <KonuSureEtiketi modul={modul} konu={k.id} ekSoru={k.ekSoru} />
        </span>
      </button>
      {bitti ? (
        <button type="button" className="kt-btn is-tekrar" onClick={() => { tekrarBasla(modul, k.id); k.tekrar(); }} aria-label={`Tekrar et: ${k.ad}`}>
          <RotateCcw aria-hidden /><span>Tekrar et</span>
        </button>
      ) : (
        <button type="button" className="kt-btn" onClick={k.ac} aria-label={`Aç: ${k.ad}`}>
          <Play aria-hidden /><span>Aç</span>
        </button>
      )}
    </li>
  );
}
