import React from 'react';
import { Check, ChevronRight } from 'lucide-react';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import { BUTUNLEME_TARIHI, FINAL_TARIHI, KURULLAR, aktifKurul, bugun } from '../../services/kurulTakvimi';
import { useV15Baslik } from './baslik';
import { Halka } from './Halka';
import '../../styles/v15/takvim.css';

/**
 * v15 · Sınav takvimi (tasarım sistemi v15 › D06 "Sınavlarım" + J "Kurul takvimi"). Yeni sayfa: /takvim ↔ /kamplar/takvim.
 * Veri yalnız kurul takviminden (src/data/kurul_takvimi_ozet.json, services/kurulTakvimi).
 * Üstte aktif kurulun sınavı (kalan gün + kurul içindeki ilerleme), altında sınavdan 5/3/1 gün önceki hazırlık günleri
 * (her biri o günün işine götürür), en altta yılın bütün sınavları zaman çizelgesi olarak.
 */
const GUN = 86_400_000;
const tarih = (g: string) => new Date(`${g}T12:00:00`);
const fark = (a: string, b: string) => Math.round((tarih(a).getTime() - tarih(b).getTime()) / GUN);
const yaz = (g: string, gunAdi = true) =>
  tarih(g).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', ...(gunAdi ? { weekday: 'short' } : {}) });
const ekle = (g: string, n: number) => {
  const d = tarih(g);
  d.setDate(d.getDate() + n);
  const p = (x: number) => String(x).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
};
/** Takvim verisinde kurul adları büyük harf: Türkçe kurallarıyla sözcük başı büyük ("NÖROPSİKİYATRİ KURULU" → "Nöropsikiyatri Kurulu") */
const adYaz = (s: string) => s.toLocaleLowerCase('tr-TR').replace(/(^|[\s(/-])(\p{L})/gu, (_, a: string, b: string) => a + b.toLocaleUpperCase('tr-TR'));
const kalanYaz = (n: number) => (n === 0 ? 'Bugün' : n === 1 ? 'Yarın' : n > 0 ? `${n} gün kaldı` : `${-n} gün önce`);

const HAZIRLIK: { t: number; ad: string; ne: string; hedef: AppRoute }[] = [
  { t: 5, ad: 'T‑5', ne: 'Son Prova: kurulun sesli özetini bitir', hedef: 'son_prova' },
  { t: 3, ad: 'T‑3', ne: 'Çıkmış çözücü: sınav kadar soruyla dene', hedef: 'cikmis_cozucu' },
  { t: 1, ad: 'T‑1', ne: 'En önemliler: son tekrar', hedef: 'en_onemliler' },
];

export default function SinavTakvimiV15() {
  const g = bugun();
  const k = aktifKurul(g);
  const kalan = fark(k.sinav, g);
  const sure = Math.max(1, fark(k.sinav, k.baslangic));
  const gecen = Math.min(sure, Math.max(0, fark(g, k.baslangic)));
  useV15Baslik({ baslik: 'Sınav takvimi', alt: `Kurul ${k.kurul} · ${kalanYaz(kalan)}` });

  const olaylar = [
    ...KURULLAR.map((x) => ({ id: `k${x.kurul}`, gun: x.sinav, ad: `Kurul ${x.kurul} sınavı`, alt: adYaz(x.ad) })),
    ...(FINAL_TARIHI ? [{ id: 'final', gun: FINAL_TARIHI, ad: 'Final', alt: 'Dönem sonu sınavı' }] : []),
    ...(BUTUNLEME_TARIHI ? [{ id: 'but', gun: BUTUNLEME_TARIHI, ad: 'Bütünleme', alt: 'Telafi sınavı' }] : []),
  ].sort((a, b) => a.gun.localeCompare(b.gun));
  const siradaki = olaylar.find((o) => o.gun >= g)?.id;
  const git = (r: AppRoute) => linkClick(() => navigateTo(pathFor(r)));

  return (
    <div className="tk15">
      <h1 className="sr-only">Sınav takvimi</h1>
      <section className="tk15-hero v15-card" aria-label="Sıradaki sınav">
        <div className="tk15-hero-t">
          <span className="v15-label">Sıradaki sınav</span>
          <b>Kurul {k.kurul} · {adYaz(k.ad)}</b>
          <span className="v15-cap">{yaz(k.sinav)}</span>
          <span className="v15-bar" aria-hidden><span style={{ width: `${(gecen / sure) * 100}%` }} /></span>
          <span className="v15-cap">Kurul {yaz(k.baslangic, false)} başladı · {gecen}/{sure} gün</span>
        </div>
        <Halka pct={(gecen / sure) * 100} boyut={84} etiket={kalanYaz(kalan)} yazi={<span className="tk15-n">{Math.max(0, kalan)}<small>gün</small></span>} />
      </section>

      <section aria-label="Hazırlık günleri">
        <h2 className="v15-h2 tk15-h">Hazırlık günleri</h2>
        <ul className="tk15-hz" role="list">
          {HAZIRLIK.map((h) => {
            const gun = ekle(k.sinav, -h.t);
            const durum = gun < g ? 'gecti' : gun === g ? 'bugun' : 'gelecek';
            return (
              <li key={h.t}>
                <a className={`tk15-hz-a v15-card is-${durum}`} href={pathFor(h.hedef)} onClick={git(h.hedef)}>
                  <span className={`v15-tag ${durum === 'bugun' ? 'is-w' : durum === 'gecti' ? 'is-ok' : 'is-a'}`}>{h.ad}</span>
                  <span className="tk15-hz-t">
                    <b>{yaz(gun)}</b>
                    <span className="v15-cap">{h.ne}</span>
                  </span>
                  {durum === 'gecti' ? <Check className="tk15-ok" aria-label="Geçti" /> : <ChevronRight className="v15-chev" aria-hidden />}
                </a>
              </li>
            );
          })}
        </ul>
      </section>

      <section aria-label="Yılın sınavları">
        <h2 className="v15-h2 tk15-h">Yılın sınavları</h2>
        <ol className="tk15-cizelge v15-card">
          {olaylar.map((o) => {
            const durum = o.gun < g ? 'gecti' : o.id === siradaki ? 'simdi' : 'gelecek';
            return (
              <li key={o.id} className={`is-${durum}`}>
                <span className="tk15-nokta" aria-hidden>{durum === 'gecti' ? <Check /> : null}</span>
                <span className="tk15-c-t">
                  <b>{o.ad}</b>
                  <span className="v15-cap">{o.alt}</span>
                </span>
                <span className="tk15-c-g">
                  <span>{yaz(o.gun, false)}</span>
                  <span className="v15-cap">{kalanYaz(fark(o.gun, g))}</span>
                </span>
              </li>
            );
          })}
        </ol>
      </section>
    </div>
  );
}
