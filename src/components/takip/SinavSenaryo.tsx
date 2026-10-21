/**
 * 60 planı › Sınav senaryosu: öğrenci her ders için emin olduğu doğru aralığını, kalanların ne kadarını sallayacağını ve
 * salladıklarının ne kadarının tutacağını yazar; üç senaryo (kötümser · mantıksal · iyimser) baraj kuralıyla hesaplanır.
 *
 * Algoritma (ders başına, n soru):
 *  - Model "bildiği" soru = n·(p − 0,2)/0,8 (p: çalışma durumundan beklenen doğru oranı, 0,2 = beş şıkta rastgele).
 *  - Emin olunan K: mantıksalda 0,6·model + 0,4·öğrencinin aralık ortası (mevcut durum > öğrenci güveni);
 *    iyimserde öğrencinin üst sınırı (ya da model, büyük olan); kötümserde alt sınırın %90'ı ve modelin %85'inden küçüğü.
 *  - Emin olunan soruda da hata: iyimser %97, mantıksal %92, kötümser %85 doğru.
 *  - Sallanan = (n − K)·sallama oranı, boş bırakılan puan getirmez/götürmez.
 *  - Sallama isabeti: iyimser max(öğrenci, %55) ("çoğu tutar"); mantıksal 0,7·%30 (toplum: şık elemeli sallama) + 0,3·öğrenci;
 *    kötümser min(öğrenci, %18) (çeldiriciye düşme, rastgelenin altı).
 *  - Doğru beklentisi d → beta-binom dağılımı → baraj puanı → dersler birleştirilir: ortalama, %10–%90 aralığı, P(≥60).
 *  - Öğrencinin kendi hesabı (aralık ortası tam doğru + sallama × kendi isabeti) mantıksalla karşılaştırılıp fazla/eksik tahmin söylenir.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { BIR, beklenen, birlestir, bransDag, enAz, yuzdelik, type BransPlan, type Dag } from './sinavPlani';

/** Profil kv (userKvSync ile cihazlar arası): { g: ders → girdi, s: son hesaplanan senaryolar (yönetim › Kişiler'de görünür), at } */
export const SENARYO_KEY = 'medsoru_sinav_senaryo_v1';
const KEY = SENARYO_KEY;
interface Girdi { a: number; b: number; salla: number; isabet: number }
type Kayit = Record<string, Girdi>;
export interface SenaryoOzet { ort: number; alt: number; ust: number; p60: number; satir: { brans: string; ad: string; n: number; d: number; puan: number }[] }
export interface SenaryoKaydi { g: Kayit; s?: { kaynak: 'simdi' | 'plan'; kendi: number; kotu: SenaryoOzet; mantik: SenaryoOzet; iyi: SenaryoOzet; at: string }; at?: string }
const okuHam = (): SenaryoKaydi => {
  try {
    const x = JSON.parse(localStorage.getItem(KEY) || '{}') || {};
    return x && typeof x.g === 'object' ? x : { g: x }; // eski biçim: doğrudan ders → girdi
  } catch { return { g: {} }; }
};
const oku = (): Kayit => okuHam().g || {};
const yazHam = (v: SenaryoKaydi) => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch { /* yok */ } };
const yaz = (k: Kayit) => yazHam({ ...okuHam(), g: k, at: new Date().toISOString() });

const TOPLUM_ISABET = 0.30;
const fmt = (n: number) => (Math.round(n * 10) / 10).toLocaleString('tr-TR').replace('-', '−');
const tam = (n: number) => String(Math.round(n)).replace('-', '−');
const kirp = (x: number, a: number, b: number) => Math.max(a, Math.min(b, x));

type SenId = 'kotu' | 'mantik' | 'iyi';
const SEN: { id: SenId; ad: string; acik: string }[] = [
  { id: 'kotu', ad: 'Kötümser', acik: 'Stres, dikkat hatası, çeldiriciler: bildiğinin bir kısmı da kaçar, salladıkların çoğu tutmaz.' },
  { id: 'mantik', ad: 'Mantıksal', acik: 'Çalışma durumun önce, kendi tahminin sonra, sallama isabeti en son ağırlıkla.' },
  { id: 'iyi', ad: 'İyimser', acik: 'Bildiğin aralığın üst ucu ve salladıklarının çoğu tutar.' },
];

export default function SinavSenaryo({ branslar, hedef, planli }: { branslar: BransPlan[]; hedef: number; planli: boolean }) {
  const [kayit, setKayit] = useState<Kayit>(oku);
  const [kaynak, setKaynak] = useState<'simdi' | 'plan'>('simdi');
  const [acikSen, setAcikSen] = useState<SenId | null>('mantik');
  // başka cihazdan eşitlenince girdileri yenile
  useEffect(() => {
    const f = (e: StorageEvent) => { if (e.key == null || e.key === KEY) setKayit(oku()); };
    window.addEventListener('storage', f);
    return () => window.removeEventListener('storage', f);
  }, []);

  const model = (b: BransPlan) => {
    const d = kaynak === 'plan' ? b.planDogru : b.dogru;
    return kirp(b.n * (d / b.n - 0.2) / 0.8, 0, b.n);
  };
  const girdi = (b: BransPlan): Girdi => {
    const g = kayit[b.brans];
    if (g) return { ...g, a: kirp(g.a, 0, b.n), b: kirp(g.b, 0, b.n) };
    const m = model(b);
    return { a: Math.max(0, Math.floor(m * 0.85)), b: Math.min(b.n, Math.ceil(m * 1.15)), salla: 80, isabet: 33 };
  };
  const degis = (b: BransPlan, p: Partial<Girdi>) => {
    const g = { ...girdi(b), ...p };
    if (p.a != null && g.b < g.a) g.b = g.a;
    if (p.b != null && g.a > g.b) g.a = g.b;
    const k = { ...kayit, [b.brans]: g };
    setKayit(k); yaz(k);
  };

  const sonuc = useMemo(() => {
    const hesap = (id: SenId) => {
      let top: Dag = BIR;
      const satir = branslar.map((b) => {
        const g = girdi(b);
        const m = model(b), orta = (g.a + g.b) / 2, h = g.isabet / 100, s = g.salla / 100;
        let K: number, dog: number, his: number;
        if (id === 'iyi') { K = Math.max(g.b, m); dog = 0.97; his = Math.max(h, 0.55); }
        else if (id === 'kotu') { K = Math.min(g.a * 0.9, m * 0.85); dog = 0.85; his = Math.min(h, 0.18); }
        else { K = 0.6 * m + 0.4 * orta; dog = 0.92; his = 0.7 * TOPLUM_ISABET + 0.3 * h; }
        K = kirp(K, 0, b.n);
        const sallanan = (b.n - K) * s;
        const d = kirp(K * dog + sallanan * his, 0, b.n);
        const dag = bransDag(b.n, kirp(d / b.n, 0.001, 0.999));
        top = birlestir(top, dag);
        return { b, d, puan: beklenen(dag), sallanan, bos: b.n - K - sallanan };
      });
      return { satir, ort: beklenen(top), alt: yuzdelik(top, 0.1), ust: yuzdelik(top, 0.9), p60: enAz(top, hedef) };
    };
    // öğrencinin kendi hesabı: aralık ortası tam doğru + sallama × kendi isabeti (baraj kuralıyla)
    const kendi = branslar.reduce((t, b) => {
      const g = girdi(b);
      const orta = (g.a + g.b) / 2;
      const d = Math.min(b.n, orta + (b.n - orta) * (g.salla / 100) * (g.isabet / 100));
      return t + (2 * d >= b.n ? d : 2 * d - b.n / 2);
    }, 0);
    return { kotu: hesap('kotu'), mantik: hesap('mantik'), iyi: hesap('iyi'), kendi };
  }, [branslar, kayit, kaynak, hedef]); // eslint-disable-line react-hooks/exhaustive-deps

  const fark = sonuc.kendi - sonuc.mantik.ort;

  // Sonuçları profile yaz (yönetici görür): yalnız öğrenci girdi yazmışsa ve yuvarlanmış sonuç değiştiyse, 3 sn sonra.
  // Plan her süre tıkında yeniden hesaplanır; zamanlayıcı yalnız yuvarlanmış sonucun imzası değişince yeniden kurulur.
  const imza = useMemo(() => {
    if (!Object.keys(kayit).length) return '';
    const oz = (r: typeof sonuc.mantik): SenaryoOzet => ({
      ort: Math.round(r.ort * 10) / 10, alt: Math.round(r.alt), ust: Math.round(r.ust), p60: Math.round(r.p60 * 100) / 100,
      satir: r.satir.map((x) => ({ brans: x.b.brans, ad: x.b.ad, n: x.b.n, d: Math.round(x.d * 10) / 10, puan: Math.round(x.puan * 10) / 10 })),
    });
    return JSON.stringify({ kaynak, kendi: Math.round(sonuc.kendi * 10) / 10, kotu: oz(sonuc.kotu), mantik: oz(sonuc.mantik), iyi: oz(sonuc.iyi) });
  }, [sonuc, kaynak, kayit]);
  useEffect(() => {
    if (!imza) return;
    const eski = okuHam().s;
    if (eski) { const { at: _at, ...e } = eski; if (JSON.stringify(e) === imza) return; }
    const t = window.setTimeout(() => yazHam({ ...okuHam(), s: { ...JSON.parse(imza), at: new Date().toISOString() } }), 3000);
    return () => window.clearTimeout(t);
  }, [imza]);

  return (
    <div className="ss">
      <h3 className="sp-h">Sınav senaryosu: kendi tahminin</h3>
      <p className="ss-acik">
        Her ders için emin olduğun doğru sayısını aralık olarak yaz, kalan soruların ne kadarını sallayacağını ve salladıklarının
        ne kadarının tutacağını düşündüğünü seç. Hesap; çalışma durumunu, kendi tahminini ve şıklardan eleyerek sallayanların
        genel isabetini (~%30) birlikte değerlendirir.
      </p>
      {planli && (
        <div className="ss-kaynak" role="group" aria-label="Çalışma durumu">
          <button type="button" aria-pressed={kaynak === 'simdi'} className={kaynak === 'simdi' ? 'is-on' : ''} onClick={() => setKaynak('simdi')}>Bugünkü durumumla</button>
          <button type="button" aria-pressed={kaynak === 'plan'} className={kaynak === 'plan' ? 'is-on' : ''} onClick={() => setKaynak('plan')}>Planı bitirirsem</button>
        </div>
      )}

      <ul className="ss-dersler">
        {branslar.map((b) => {
          const g = girdi(b);
          const m = model(b);
          return (
            <li key={b.brans} className="ss-d">
              <div className="ss-d-ust">
                <b>{b.ad}</b>
                <span>{b.n} soru · baraj {fmt(b.n / 2)} · çalışmana göre ~{tam(m)} soruyu biliyorsun</span>
              </div>
              <div className="ss-alan">
                <label className="ss-aralik">
                  <span>Emin olduğum doğru</span>
                  <span className="ss-sayilar">
                    <Sayi deger={g.a} min={0} max={b.n} onChange={(v) => degis(b, { a: v })} etiket={`${b.ad} en az`} />
                    <em>–</em>
                    <Sayi deger={g.b} min={0} max={b.n} onChange={(v) => degis(b, { b: v })} etiket={`${b.ad} en çok`} />
                  </span>
                </label>
                <label className="ss-kaydir">
                  <span>Kalandan sallayacağım: <b>%{g.salla}</b></span>
                  <input type="range" min={0} max={100} step={10} value={g.salla} onChange={(e) => degis(b, { salla: Number(e.target.value) })} />
                </label>
                <label className="ss-kaydir">
                  <span>Salladığımdan tutacak: <b>%{g.isabet}</b></span>
                  <input type="range" min={10} max={80} step={1} value={g.isabet} onChange={(e) => degis(b, { isabet: Number(e.target.value) })} />
                </label>
              </div>
            </li>
          );
        })}
      </ul>

      <div className="ss-sen">
        {SEN.map(({ id, ad, acik }) => {
          const r = sonuc[id];
          return (
            <button key={id} type="button" className={`ss-s is-${id}${acikSen === id ? ' is-secili' : ''}`} aria-pressed={acikSen === id} onClick={() => setAcikSen(acikSen === id ? null : id)}>
              <small>{ad}</small>
              <b>{tam(r.ort)} <span>net</span></b>
              <em>%80 olasılıkla {tam(r.alt)} ile {tam(r.ust)} arası · 60 olasılığı %{Math.round(r.p60 * 100)}</em>
              <i>{acik}</i>
            </button>
          );
        })}
      </div>

      {acikSen && (
        <div className="ss-tablo" role="table" aria-label={`${SEN.find((x) => x.id === acikSen)!.ad} senaryo, ders ders`}>
          <div className="ss-tr is-bas" role="row"><span role="columnheader">Ders</span><span role="columnheader">Doğru</span><span role="columnheader">Sallanan</span><span role="columnheader">Net</span></div>
          {sonuc[acikSen].satir.map((x) => (
            <div key={x.b.brans} className={`ss-tr${x.d < x.b.n / 2 ? ' is-altta' : ''}`} role="row">
              <span role="cell">{x.b.ad}</span>
              <span role="cell">~{fmt(x.d)} / {x.b.n}</span>
              <span role="cell">{fmt(x.sallanan)}{x.bos >= 0.5 ? ` · boş ${fmt(x.bos)}` : ''}</span>
              <span role="cell"><b>{fmt(x.puan)}</b></span>
            </div>
          ))}
        </div>
      )}

      <p className={`sp-not ${Math.abs(fark) < 3 ? 'is-iyi' : 'is-uyari'}`}>
        Kendi hesabınla ~{tam(sonuc.kendi)} net bekliyorsun; mantıksal senaryo ~{tam(sonuc.mantik.ort)}.{' '}
        {Math.abs(fark) < 3
          ? 'Tahminin çalışma durumunla uyumlu.'
          : fark > 0
            ? `Kendine ~${tam(fark)} puan fazla güveniyor olabilirsin: emin olduğun sorularda da hata yapılır, sallamaların çoğu %30 civarında tutar.`
            : `Kendini ~${tam(-fark)} puan eksik değerlendiriyor olabilirsin: çalıştığın konular düşündüğünden fazla doğru getirebilir.`}
      </p>
    </div>
  );
}

function Sayi({ deger, min, max, onChange, etiket }: { deger: number; min: number; max: number; onChange: (v: number) => void; etiket: string }) {
  return (
    <span className="ss-sayi">
      <button type="button" onClick={() => onChange(Math.max(min, deger - 1))} aria-label={`${etiket} azalt`} disabled={deger <= min}>−</button>
      <input type="number" inputMode="numeric" min={min} max={max} value={deger} aria-label={etiket}
        onChange={(e) => { const v = Number(e.target.value); if (Number.isFinite(v)) onChange(kirp(Math.round(v), min, max)); }} />
      <button type="button" onClick={() => onChange(Math.min(max, deger + 1))} aria-label={`${etiket} artır`} disabled={deger >= max}>+</button>
    </span>
  );
}
