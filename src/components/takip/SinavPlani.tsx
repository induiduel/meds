/**
 * Bitirdiklerim › Sınav planı: en az 60 için kişiye özel, gün gün yol haritası (algoritma: ./sinavPlani.ts).
 * Her adım ilgili sayfayı açar (sesli ders, en önemliler sesli asistanı, soru çözücü). Stil: styles/takip.css (.sp-*).
 */
import React, { useEffect, useMemo, useState } from 'react';
import { ChevronDown, Headphones, MessageCircleQuestion, Play, Star, Target } from 'lucide-react';
import { sureYaz, useTakip, type Hiz, type TakipModul } from '../../services/calismaTakip';
import { ASAMA_AD, planHesapla, planVerisiYukle, type AdimTur, type PlanAdim, type PlanVeri } from './sinavPlani';

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
  const [acik, setAcik] = useState(true);
  const [tumGun, setTumGun] = useState<Record<number, boolean>>({});
  const takip = useTakip();

  useEffect(() => { let c = true; planVerisiYukle().then((v) => c && setVeri(v), () => c && setVeri(null)); return () => { c = false; }; }, []);
  const setSaat = (n: number) => { setSaat0(n); try { localStorage.setItem(SAAT_KEY, String(n)); } catch { /* yok */ } };

  // takip değişince (işaret, süre) yeniden hesaplanır
  const plan = useMemo(() => (veri ? planHesapla(veri, hiz, { gunlukSaat: saat }) : null), [veri, hiz, saat, takip]);

  if (veri === undefined) return <section className="sp sp-bos" aria-busy="true"><span className="bd-spin" aria-hidden /> Sınav planı hazırlanıyor…</section>;
  if (!plan) return null;

  const { simdi, sonra } = plan;
  const durumMetni = plan.guvende
    ? 'Bugünkü durumunla 60 büyük olasılıkla geliyor. Aşağıdakiler güvenceyi artırır; yorgunsan dinlenmek de plana dahil.'
    : plan.yetersiz
      ? plan.adimlar.length
        ? `Bu sürede en yüksek puanı getiren sıra aşağıda. Günlük saati artırabilirsen olasılık yükselir; ama uykudan kesme — yorgun beyin bildiği soruda da hata yapar.`
        : 'Plana yer kalmadı. Sınav sabahı yalnız en önemliler listesine göz at ve dinlen.'
      : `Bu sırayla gidersen 60'ı %90 olasılıkla geçersin. Kalan vaktini dinlenmeye ve tekrara ayırabilirsin.`;

  const sirali = [...plan.branslar].sort((a, b) => (b.calismaSn + b.soruSn) - (a.calismaSn + a.soruSn) || b.n - a.n);

  return (
    <section className={`sp${acik ? ' is-acik' : ''}`} aria-label="Sınav planı">
      <button type="button" className="sp-bas" aria-expanded={acik} onClick={() => setAcik(!acik)}>
        <span className="sp-ic" aria-hidden><Target /></span>
        <span className="sp-bas-t">
          <b>Kurul {plan.kurul} sınavı için 60 planı</b>
          <small>{kalanYaz(plan.sinav)} · {plan.hedef} puan hedefi · baraj kuralı hesaba katıldı</small>
        </span>
        <ChevronDown aria-hidden className="bd-ok" />
      </button>

      {acik && (
        <div className="sp-ic-alan">
          <div className="sp-skor">
            <div className="sp-skor-k">
              <small>Bugünkü durumunla</small>
              <b>~{tamYaz(simdi.beklenen)}</b>
              <em>60 olasılığı {yuzde(simdi.olasilik)}</em>
              <span className="sp-olc" aria-hidden><i style={{ width: `${Math.round(simdi.olasilik * 100)}%` }} /></span>
            </div>
            <div className="sp-skor-ok" aria-hidden>→</div>
            <div className="sp-skor-k is-plan">
              <small>Planı uygularsan</small>
              <b>~{tamYaz(sonra.beklenen)}</b>
              <em>60 olasılığı {yuzde(sonra.olasilik)} · kötü günde bile ~{tamYaz(sonra.kotu)}</em>
              <span className="sp-olc" aria-hidden><i style={{ width: `${Math.round(sonra.olasilik * 100)}%` }} /></span>
            </div>
          </div>

          <div className="sp-saat">
            <span>Günde kaç saat ayırabilirsin?</span>
            <div role="group" aria-label="Günlük çalışma saati">
              {SAATLER.map((n) => (
                <button key={n} type="button" aria-pressed={saat === n} className={saat === n ? 'is-on' : ''} onClick={() => setSaat(n)}>{n} sa</button>
              ))}
            </div>
            <small>
              Plan süresi {sureYaz(plan.planSn)} · ayırabileceğin {sureYaz(plan.butceSn)} (her saatte 10 dk mola, gece 23.30 sonrası yok)
              {plan.hepsiSn > plan.butceSn ? ` · hepsini bitirmek ${sureYaz(plan.hepsiSn)} sürerdi, bu yüzden öncelik sırası var` : ''}
            </small>
          </div>

          <p className={`sp-not${plan.guvende || !plan.yetersiz ? ' is-iyi' : ' is-uyari'}`}>{durumMetni}</p>

          <h3 className="sp-h">Derslere göre yoğunlaşma</h3>
          <ul className="sp-brans">
            {sirali.map((b) => {
              const baraj = b.n / 2;
              const altta = b.dogru < baraj;
              const sure = b.calismaSn + b.soruSn;
              return (
                <li key={b.brans} className={`sp-b${altta ? ' is-altta' : ''}${!sure ? ' is-sakin' : ''}`}>
                  <div className="sp-b-ust">
                    <b>{b.ad}</b>
                    <span>{b.n} soru · baraj {puanYaz(baraj)}</span>
                  </div>
                  <div className="sp-b-cubuk" aria-label={`Tahmini doğru ${puanYaz(b.dogru)}, planla ${puanYaz(b.planDogru)}, baraj ${puanYaz(baraj)}`}>
                    <i className="is-plan" style={{ width: `${(b.planDogru / b.n) * 100}%` }} />
                    <i className="is-simdi" style={{ width: `${(b.dogru / b.n) * 100}%` }} />
                    <span className="sp-b-baraj" style={{ left: '50%' }} />
                  </div>
                  <div className="sp-b-alt">
                    <span>~{puanYaz(b.dogru)} doğru{b.planDogru - b.dogru > 0.2 ? ` → ~${puanYaz(b.planDogru)}` : ''}</span>
                    <span className="sp-b-puan">{puanYaz(b.puan)}{b.planPuan - b.puan > 0.2 ? ` → ${puanYaz(b.planPuan)}` : ''} puan</span>
                  </div>
                  <div className="sp-b-oneri">
                    {sure
                      ? <>{b.calismaSn > 0 && <span>Konu {sureYaz(b.calismaSn)}</span>}{b.soruSn > 0 && <span>Soru {sureYaz(b.soruSn)}</span>}</>
                      : <span>Şimdilik ek çalışma gerekmiyor</span>}
                    {altta && <em>Baraj altında: buradaki her doğru 2 puan değerinde</em>}
                    {b.isabet != null && <em className="is-gri">Soru çözücüde ilk denemede {yuzde(b.isabet)} doğru ({b.cozulen} soru)</em>}
                  </div>
                </li>
              );
            })}
          </ul>

          {plan.gunler.some((g) => g.adimlar.length) && <h3 className="sp-h">Aşama aşama yol haritası</h3>}
          {plan.gunler.filter((g) => g.adimlar.length).map((g) => {
            const hepsi = tumGun[g.gun];
            const L = hepsi ? g.adimlar : g.adimlar.slice(0, 6);
            return (
              <div key={g.gun} className="sp-gun">
                <div className="sp-gun-bas">
                  <b>{g.tarih}</b>
                  <span>{g.adimlar.length} adım · {sureYaz(g.sn)}</span>
                </div>
                <ol className="sp-adimlar">
                  {L.map((a, i) => {
                    const Ikon = IKON[a.tur];
                    return (
                      <li key={`${a.ders.anahtar}-${a.tur}`} className={`sp-a is-${a.asama}`}>
                        <span className="sp-a-no">{plan.adimlar.indexOf(a) + 1}</span>
                        <span className="sp-a-t">
                          <span className="sp-a-etiket">{ASAMA_AD[a.asama]}</span>
                          <b>{a.ders.ad}</b>
                          <small>
                            <span className="sp-a-tur"><Ikon aria-hidden /> {adimAdi(a)}</span>
                            <span>{bransKisa(a.ders.brans, plan)}</span>
                            <span>~{sureYaz(a.sn)}</span>
                            {a.kazanc >= 0.05 && <span className="sp-a-k">+{puanYaz(a.kazanc)} puan</span>}
                          </small>
                        </span>
                        <button type="button" className="kt-btn sp-a-ac" onClick={a.ac} aria-label={`${adimAdi(a)}: ${a.ders.ad}`}>
                          <Play aria-hidden /><span>{i === 0 && g.gun === plan.gunler[0].gun ? 'Başla' : 'Aç'}</span>
                        </button>
                      </li>
                    );
                  })}
                </ol>
                {g.adimlar.length > 6 && (
                  <button type="button" className="sp-daha" onClick={() => setTumGun((t) => ({ ...t, [g.gun]: !hepsi }))}>
                    {hepsi ? 'Daha az göster' : `${g.adimlar.length - 6} adım daha`}
                  </button>
                )}
              </div>
            );
          })}

          <details className="sp-nasil">
            <summary>Plan nasıl hesaplanıyor?</summary>
            <ul>
              <li><b>Baraj:</b> bir dersin sorularının yarısından az doğru yaparsan eksik kalan her doğru kadar puan düşülür. 20 soruda 8 doğru 6 puan, 5 doğru 0 puan. Bu yüzden baraj altındaki derste her yeni doğru 2 puan değerindedir.</li>
              <li><b>Ders payı:</b> sınavdaki soru sayısı dersin konularına kazanım (en önemli madde) sayısı, soru bankası büyüklüğü ve ders süresine göre dağıtılır.</li>
              <li><b>Bilgi düzeyi:</b> sesli ders, en önemliler ve soru çözücüde bitirdiğin her konu doğru olasılığını artırır; hiç çalışılmamış konuda bile şık elemeyle bir pay vardır. 12 günden eski çalışmada biraz unutma hesaba katılır.</li>
              <li><b>Hata payı:</b> çalıştığın konudan gelen soruyu da yanlış yapabilirsin; çalışılmış konuda bile doğru olasılığı ~%75 sayılır, soru çözücüdeki ilk deneme sonuçların bunu sana göre düzeltir. Olasılık, şanslı ve şanssız günleri birlikte hesaplar.</li>
              <li><b>Sıra:</b> her adımda "kazandıracağı puan ÷ süresi" en yüksek iş seçilir; önce konu (en kısa yol: en önemliler asistanı), sonra o konunun soruları. 60 olasılığı %90'a ulaşınca plan durur.</li>
              <li><b>Süre:</b> içerik süresi senin çalışma hızınla (bitirdiğin konulardaki gerçek süre) çarpılır; her saatin 10 dakikası mola, gece 23.30 sonrası ve sınav sabahı plana konmaz.</li>
            </ul>
          </details>
        </div>
      )}
    </section>
  );
}

const bransKisa = (b: string, p: { branslar: { brans: string; ad: string }[] }) => p.branslar.find((x) => x.brans === b)?.ad || b;
