/**
 * Bitirdiklerim › Sınav planı: en az 60 için kişiye özel, gün gün yol haritası (algoritma: ./sinavPlani.ts).
 * Her adım ilgili sayfayı açar (sesli ders, en önemliler sesli asistanı, soru çözücü). Stil: styles/takip.css (.sp-*).
 */
import React, { useEffect, useMemo, useState } from 'react';
import { Headphones, MessageCircleQuestion, Play, Star } from 'lucide-react';
import { sureYaz, useTakip, type Hiz, type TakipModul } from '../../services/calismaTakip';
import SinavSenaryo from './SinavSenaryo';
import { planHesapla, planVerisiYukle, type AdimTur, type PlanAdim, type PlanGun, type PlanVeri } from './sinavPlani';

const SAAT_KEY = 'medsoru_sinav_plani_saat_v1';
const SAATLER = [3, 5, 7, 9, 11];
const okuSaat = () => { try { const n = Number(localStorage.getItem(SAAT_KEY)); return SAATLER.includes(n) ? n : 7; } catch { return 7; } };
const yuzde = (p: number) => `%${Math.round(p * 100)}`;
const puanYaz = (n: number) => (Math.round(n * 10) / 10).toLocaleString('tr-TR').replace('-', '−');
const tamYaz = (n: number) => String(Math.round(n)).replace('-', '−');

const IKON: Record<AdimTur, React.ComponentType<{ 'aria-hidden'?: boolean }>> = { onem: Star, cozucu: MessageCircleQuestion, sesli: Headphones };
const adimAdi = (a: PlanAdim) => (a.tur === 'onem' ? (a.ders.onem?.asistan ? 'Sesli asistan' : 'En önemliler') : a.tur === 'cozucu' ? 'Soru çöz' : 'Sesli ders');

function kalanYaz(sinav: string) {
  const ms = Date.parse(`${sinav}T09:30:00`) - Date.now();
  if (ms <= 0) return 'Sınav günü';
  const sa = Math.floor(ms / 3600_000);
  return sa >= 24 ? `${Math.floor(sa / 24)} gün ${sa % 24} sa kaldı` : `${sa} sa kaldı`;
}

export default function SinavPlani({ hiz }: { hiz: Partial<Record<TakipModul, Hiz>> }) {
  const [veri, setVeri] = useState<PlanVeri | null | undefined>(undefined);
  const [saat, setSaat0] = useState(okuSaat);
  const [tumGun, setTumGun] = useState<Record<number, boolean>>({});
  const takip = useTakip();

  useEffect(() => {
    const f = (e: StorageEvent) => { if (e.key == null || e.key === SAAT_KEY) setSaat0(okuSaat()); };
    window.addEventListener('storage', f);
    return () => window.removeEventListener('storage', f);
  }, []);
  useEffect(() => { let c = true; planVerisiYukle().then((v) => c && setVeri(v), () => c && setVeri(null)); return () => { c = false; }; }, []);
  const setSaat = (n: number) => { setSaat0(n); try { localStorage.setItem(SAAT_KEY, String(n)); } catch { /* yok */ } };

  // takip değişince (işaret, süre) yeniden hesaplanır
  const plan = useMemo(() => (veri ? planHesapla(veri, hiz, { gunlukSaat: saat }) : null), [veri, hiz, saat, takip]);

  if (veri === undefined) return <section className="sp sp-bos" aria-busy="true"><span className="bd-spin" aria-hidden /> Sınav planı hazırlanıyor…</section>;
  if (!plan) return null;

  const { simdi, sonra } = plan;
  const durum: 'iyi' | 'orta' | 'zor' = plan.guvende ? 'iyi' : !plan.yetersiz ? 'orta' : 'zor';
  const DURUM_AD = { iyi: 'Güvendesin', orta: 'Plana uyarsan geçersin', zor: 'Zor ama puanını artırabilirsin' } as const;
  const ozet = plan.guvende
    ? `Şu anki durumunla 60'ı büyük olasılıkla alırsın. Aşağıdaki adımlar güvenceni artırır.`
    : !plan.yetersiz
      ? `Aşağıdaki adımları bitirirsen 60'ı büyük olasılıkla alırsın (%90). Kalan vaktini dinlenmeye ayırabilirsin.`
      : plan.adimlar.length
        ? `Kalan sürede her şeyi bitiremezsin; plan sana en çok puanı getirecek işleri sıraladı. Günlük saati artırırsan şansın yükselir, ama uykudan kesme.`
        : 'Plana yer kalmadı. Sınav sabahı yalnız en önemliler listesine göz at ve dinlen.';

  const gunler = plan.gunler.filter((g) => g.adimlar.length);
  const [bugun, ...sonraki] = gunler;
  const sirali = [...plan.branslar].sort((a, b) => (b.calismaSn + b.soruSn) - (a.calismaSn + a.soruSn) || b.n - a.n);
  const altta = plan.branslar.filter((b) => b.dogru < b.n / 2).length;

  const adimSatiri = (a: PlanAdim, ilk: boolean) => {
    const Ikon = IKON[a.tur];
    return (
      <li key={`${a.ders.anahtar}-${a.tur}`} className={`sp-a is-${a.asama}${ilk ? ' is-ilk' : ''}`}>
        <span className="sp-a-no">{plan.adimlar.indexOf(a) + 1}</span>
        <span className="sp-a-t">
          <b>{a.ders.ad}</b>
          <small>
            <span className="sp-a-tur"><Ikon aria-hidden /> {adimAdi(a)}</span>
            <span>{bransKisa(a.ders.brans, plan)}</span>
            <span>~{sureYaz(a.sn)}</span>
            {a.kazanc >= 0.05 && <span className="sp-a-k">+{puanYaz(a.kazanc)} puan</span>}
          </small>
        </span>
        <button type="button" className="kt-btn sp-a-ac" onClick={a.ac} aria-label={`${adimAdi(a)}: ${a.ders.ad}`}>
          <Play aria-hidden /><span>{ilk ? 'Başla' : 'Aç'}</span>
        </button>
      </li>
    );
  };
  const gunListesi = (g: PlanGun, ilkGun: boolean) => {
    const hepsi = tumGun[g.gun];
    const L = hepsi ? g.adimlar : g.adimlar.slice(0, ilkGun ? 8 : 5);
    return (
      <div key={g.gun} className="sp-gun">
        <div className="sp-gun-bas"><b>{g.tarih}</b><span>{g.adimlar.length} iş · toplam {sureYaz(g.sn)}</span></div>
        <ol className="sp-adimlar">{L.map((a, i) => adimSatiri(a, ilkGun && i === 0))}</ol>
        {g.adimlar.length > L.length || hepsi ? (
          <button type="button" className="sp-daha" onClick={() => setTumGun((t) => ({ ...t, [g.gun]: !hepsi }))}>
            {hepsi ? 'Daha az göster' : `${g.adimlar.length - L.length} iş daha göster`}
          </button>
        ) : null}
      </div>
    );
  };
  const isaret = (v: number) => ({ left: `${Math.max(0, Math.min(100, v))}%` });

  return (
    <section className="sp is-sayfa" aria-label="Sınav planı">
      <ol className="sp-nasil-kullan" aria-label="Nasıl kullanılır">
        <li><span>1</span><div><b>Günlük saatini seç</b><small>Plan bu süreye göre gün gün bölünür.</small></div></li>
        <li><span>2</span><div><b>Bugünün listesine bas</b><small>"Başla" ilgili dersi ya da soruları açar.</small></div></li>
        <li><span>3</span><div><b>Bitince işaretle</b><small>Biten iş listeden düşer, puanın güncellenir.</small></div></li>
      </ol>

      <div className="sp-kutu">
        <h3 className="sp-h"><span className="sp-h-no">1</span> Günde kaç saat çalışabilirsin?</h3>
        <div className="sp-saat">
          <div role="group" aria-label="Günlük çalışma saati">
            {SAATLER.map((n) => (
              <button key={n} type="button" aria-pressed={saat === n} className={saat === n ? 'is-on' : ''} onClick={() => setSaat(n)}>{n} saat</button>
            ))}
          </div>
          <small>
            Sınava {kalanYaz(plan.sinav).replace(' kaldı', '')} var. Bu sürede çalışabileceğin toplam vakit {sureYaz(plan.butceSn)} (her saatte 10 dk mola, gece 23.30 sonrası sayılmaz).
            {plan.hepsiSn > plan.butceSn ? ` Her şeyi bitirmek ${sureYaz(plan.hepsiSn)} sürerdi; bu yüzden en çok puan getirenler öne alındı.` : ''}
          </small>
        </div>
      </div>

      <div className={`sp-kutu sp-sonuc is-${durum}`}>
        <h3 className="sp-h"><span className="sp-h-no">2</span> Durumun</h3>
        <p className="sp-hukum"><b>{DURUM_AD[durum]}</b> {ozet}</p>
        <div className="sp-iki">
          <div><small>Bugün sınava girsen</small><b>~{tamYaz(simdi.beklenen)}</b><span>puan</span></div>
          <div className="is-plan"><small>Bu planı bitirirsen</small><b>~{tamYaz(sonra.beklenen)}</b><span>puan</span></div>
          <div><small>60 alma şansın</small><b>{yuzde(simdi.olasilik)} → {yuzde(sonra.olasilik)}</b><span>&nbsp;</span></div>
        </div>
        <div className="sp-olcek" aria-hidden>
          <div className="sp-olcek-yol">
            <i className="sp-olcek-dolu" style={{ width: `${Math.max(0, Math.min(100, sonra.beklenen))}%` }} />
            <i className="sp-olcek-simdi" style={{ width: `${Math.max(0, Math.min(100, simdi.beklenen))}%` }} />
            <span className="sp-olcek-hedef" style={isaret(plan.hedef)}><em>Hedef {plan.hedef}</em></span>
          </div>
          <div className="sp-olcek-alt"><span>0</span><span>100</span></div>
        </div>
        <p className="sp-acikla">
          Puanlar 100 üzerinden, baraj kuralı uygulanmış tahminlerdir. Kötü bir günde planla bile ~{tamYaz(sonra.kotu)} puan bekle.
          {altta ? ` ${altta} derste barajın altındasın; oradaki her yeni doğru 2 puan getirir, plan bu yüzden önce o derslere yönelir.` : ''}
        </p>
      </div>

      {bugun && (
        <div className="sp-kutu">
          <h3 className="sp-h"><span className="sp-h-no">3</span> Bugün ne yapacaksın?</h3>
          <p className="sp-acikla">Sırayla git; her satırdaki tahmini süre senin çalışma hızına göredir. Yeşil "+puan" o işin sınav puanına katkısıdır.</p>
          {gunListesi(bugun, true)}
          {sonraki.length > 0 && (
            <details className="sp-sonraki">
              <summary>Sonraki günler ({sonraki.length} gün)</summary>
              {sonraki.map((g) => gunListesi(g, false))}
            </details>
          )}
        </div>
      )}

      <div className="sp-kutu">
        <h3 className="sp-h"><span className="sp-h-no">{bugun ? 4 : 3}</span> Ders ders durumun</h3>
        <p className="sp-acikla">
          Her derste soruların en az yarısını doğru yapman gerekir (baraj). Çubukta <i className="sp-lej is-simdi" /> şu anki tahmini doğrun,
          <i className="sp-lej is-plan" /> planla ulaşacağın, dikey çizgi de baraj.
        </p>
        <ul className="sp-tablo">
          {sirali.map((b) => {
            const baraj = b.n / 2;
            const alt = b.dogru < baraj;
            const planAlt = b.planDogru < baraj;
            const sure = b.calismaSn + b.soruSn;
            return (
              <li key={b.brans} className={alt ? 'is-altta' : ''}>
                <div className="sp-t-ad">
                  <b>{b.ad}</b>
                  <small>{b.n} soru · baraj {puanYaz(baraj)} doğru</small>
                </div>
                <div className="sp-t-cubuk">
                  <div className="sp-b-cubuk">
                    <i className="is-plan" style={{ width: `${(b.planDogru / b.n) * 100}%` }} />
                    <i className="is-simdi" style={{ width: `${(b.dogru / b.n) * 100}%` }} />
                    <span className="sp-b-baraj" style={{ left: '50%' }} />
                  </div>
                  <small>Şu an ~{puanYaz(b.dogru)} doğru ({puanYaz(b.puan)} puan) → planla ~{puanYaz(b.planDogru)} doğru ({puanYaz(b.planPuan)} puan)</small>
                </div>
                <div className="sp-t-durum">
                  <span className={`sp-rozet ${alt ? (planAlt ? 'is-kotu' : 'is-orta') : 'is-iyi'}`}>
                    {alt ? (planAlt ? 'Baraj altında' : 'Planla barajı geçer') : 'Barajı geçiyor'}
                  </span>
                  <small>{sure ? `${sureYaz(sure)} çalışma` : 'Ek çalışma gerekmiyor'}</small>
                  {b.isabet != null && <small>Çözücüde ilk deneme {yuzde(b.isabet)} ({b.cozulen} soru)</small>}
                </div>
              </li>
            );
          })}
        </ul>
      </div>

      <details className="sp-kutu sp-ek">
        <summary>Kendi tahminini dene: sınavda kaç doğru yaparsın?</summary>
        <SinavSenaryo branslar={plan.branslar} hedef={plan.hedef} planli={plan.adimlar.length > 0} />
      </details>

      <details className="sp-kutu sp-ek sp-nasil">
        <summary>Bu sayılar nasıl hesaplanıyor?</summary>
        <ul>
          <li><b>Baraj:</b> bir dersin sorularının yarısından az doğru yaparsan eksik kalan her doğru kadar puan düşülür. 20 soruda 8 doğru 6 puan, 5 doğru 0 puan. Bu yüzden baraj altındaki derste her yeni doğru 2 puan değerindedir.</li>
          <li><b>Ders payı:</b> sınavdaki soru sayısı dersin konularına kazanım (en önemli madde) sayısı, soru bankası büyüklüğü ve ders süresine göre dağıtılır.</li>
          <li><b>Bilgi düzeyi:</b> en çok soru çözücü işe yarar (çıkmış ve çıkmış üslubunda sorular), ardından sesli ders, sonra en önemliler. Hiç çalışılmamış konuda bile şık eleme payı (~%30) vardır; 12 günden eski çalışmada biraz unutma hesaba katılır.</li>
          <li><b>Hata payı:</b> çalıştığın konudan gelen soruyu da yanlış yapabilirsin; tek kaynakla ~%61–65, üçüyle ~%78 doğru sayılır, soru çözücüdeki ilk deneme sonuçların bunu sana göre düzeltir.</li>
          <li><b>Sıra:</b> her adımda "kazandıracağı puan ÷ süresi" en yüksek iş seçilir. 60 olasılığı %90'a ulaşınca plan durur.</li>
          <li><b>Süre:</b> içerik süresi senin çalışma hızınla (bitirdiğin konulardaki gerçek süre) çarpılır; her saatin 10 dakikası mola, gece 23.30 sonrası ve sınav sabahı plana konmaz.</li>
        </ul>
      </details>
    </section>
  );
}

const bransKisa = (b: string, p: { branslar: { brans: string; ad: string }[] }) => p.branslar.find((x) => x.brans === b)?.ad || b;
