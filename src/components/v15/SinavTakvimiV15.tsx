import React, { useState } from 'react';
import { Bell, Check, ChevronRight, Plus, Trash2, X } from 'lucide-react';
import { kisiselOku, kisiselYaz, hatirlatOku, hatirlatYaz, type KisiselSinav } from '../../services/sinavlarim';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import { BUTUNLEME_TARIHI, FINAL_TARIHI, KURULLAR, aktifKurul, bugun } from '../../services/kurulTakvimi';
import { useV15Baslik } from './baslik';
import { menudeGorunur } from '../../services/siteAyar';
import { geriAlinabilir } from '../ui/Toast';
import { Halka } from './Halka';
import '../../styles/v15/takvim.css';
import '../../styles/v15/kronometre.css';

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
  const [kisisel, setKisisel0] = useState<KisiselSinav[]>(kisiselOku);
  const [hatirlat, setHatirlat0] = useState(hatirlatOku);
  const [form, setForm] = useState<{ ad: string; gun: string; tur: KisiselSinav['tur'] } | null>(null);
  const setKisisel = (l: KisiselSinav[]) => { setKisisel0(l); kisiselYaz(l); };
  const olaylarK = [...olaylar, ...kisisel.map((x) => ({ id: x.id, gun: x.gun, ad: x.ad, alt: x.tur, kisisel: true as const }))].sort((a, b) => a.gun.localeCompare(b.gun));
  const yaklasan = kisisel.filter((x) => x.gun >= g).sort((a, b) => a.gun.localeCompare(b.gun));
  const siradaki = olaylarK.find((o) => o.gun >= g)?.id;
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

      {/* tasarım D06: pratik soru hatırlatması + kişisel sınav ekleme */}
      <section className="tk15-hat v15-card">
        <Bell aria-hidden />
        <div><b>Sınav öncesi pratik soruları gönder</b><span className="v15-cap">5, 3 ve 1 gün önce Bildirimler'e soru çözme hatırlatması düşer</span></div>
        <button type="button" role="switch" aria-checked={hatirlat} aria-label="Sınav öncesi pratik soruları gönder" className={`kre-tgl${hatirlat ? ' is-on' : ''}`} onClick={() => { setHatirlat0(!hatirlat); hatirlatYaz(!hatirlat); }}><i /></button>
      </section>

      <section aria-label="Sınavlarım">
        <div className="tk15-bas"><h2 className="v15-h2 tk15-h">Sınavlarım</h2>
          <button type="button" className="v15-ib" onClick={() => setForm(form ? null : { ad: '', gun: ekle(g, 7), tur: 'Pratik' })} aria-label={form ? 'Vazgeç' : 'Sınav ekle'} title="Sınav ekle">{form ? <X aria-hidden /> : <Plus aria-hidden />}</button>
        </div>
        {form && (
          <form className="v15-card tk15-form" onSubmit={(e) => { e.preventDefault(); if (!form.ad.trim()) return; setKisisel([...kisisel, { id: `ks${Date.now().toString(36)}`, ad: form.ad.trim().slice(0, 60), gun: form.gun, tur: form.tur }]); setForm(null); }}>
            <input value={form.ad} onChange={(e) => setForm({ ...form, ad: e.target.value })} placeholder="Sınavın adı (örn. KMB uygulama)" aria-label="Sınavın adı" autoFocus />
            <input type="date" value={form.gun} min={g} onChange={(e) => setForm({ ...form, gun: e.target.value })} aria-label="Tarih" />
            <div className="v15-seg" role="radiogroup" aria-label="Tür">
              {(['Komite', 'Pratik', 'Ara sınav', 'Diğer'] as const).map((t) => <button key={t} type="button" role="radio" aria-checked={form.tur === t} aria-current={form.tur === t ? 'page' : undefined} onClick={() => setForm({ ...form, tur: t })}>{t}</button>)}
            </div>
            <button type="submit" className="v15-btn" disabled={!form.ad.trim()}>Ekle</button>
          </form>
        )}
        {yaklasan.length ? (
          <ul className="tk15-ks" role="list">
            {yaklasan.map((x) => (
              <li key={x.id} className="v15-card">
                <div className="tk15-ks-u"><b>{x.ad}</b><span className="v15-tag is-a">{x.tur}</span></div>
                <span className="v15-cap">{yaz(x.gun)} · {kalanYaz(fark(x.gun, g))}</span>
                <div className="tk15-ks-t">{[5, 3, 1].map((t) => { const d = ekle(x.gun, -t); return <span key={t} className={`v15-tag ${d < g ? 'is-ok' : d === g ? 'is-w' : ''}`}>T‑{t} · {tarih(d).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })}</span>; })}</div>
                <button type="button" className="v15-ib tk15-ks-sil" onClick={() => { const once = kisisel; setKisisel(kisisel.filter((y) => y.id !== x.id)); geriAlinabilir('Sınav silindi', () => setKisisel(once)); }} aria-label={`${x.ad} sınavını sil`}><Trash2 aria-hidden /></button>
              </li>
            ))}
          </ul>
        ) : !form && <p className="v15-cap tk15-ks-bos">Kurul sınavları takvimden gelir. Pratik, KMB ya da ara sınavlarını + ile ekle; yılın çizelgesinde de görünür.</p>}
      </section>

      <section aria-label="Hazırlık günleri">
        <h2 className="v15-h2 tk15-h">Hazırlık günleri</h2>
        <ul className="tk15-hz" role="list">
          {HAZIRLIK.filter((h) => menudeGorunur(h.hedef)).map((h) => {
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
          {olaylarK.map((o) => {
            const durum = o.gun < g ? 'gecti' : o.id === siradaki ? 'simdi' : 'gelecek';
            return (
              <li key={o.id} className={`is-${durum}`}>
                <span className="tk15-nokta" aria-hidden>{durum === 'gecti' ? <Check /> : null}</span>
                <span className="tk15-c-t">
                  <b>{o.ad}{'kisisel' in o && <span className="v15-tag is-a tk15-k">Senin</span>}</b>
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
