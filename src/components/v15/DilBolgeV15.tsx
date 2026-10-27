import { Globe } from 'lucide-react';
import { bolgeYaz, saatDilimi, saatYaz, tarihYaz, useBolge, type BolgeTercih } from '../../services/bolgeTercih';
import { bugun } from '../../services/kurulTakvimi';
import { useV15Baslik } from './baslik';
import '../../styles/v15/kisisel.css';

/**
 * v15 · Dil ve bölge (tasarım AB08 dilBolge) — /dil-bolge. Site yalnız Türkçedir; dil seçeneği gösterilmez.
 * Tercihler cihaza özgüdür (services/bolgeTercih, DEVICE_PREFS) ve ders programı, Bugün program kartı, arka plan işlerinde uygulanır.
 */
function Secim<K extends keyof BolgeTercih>({ ad, alan, secenekler, deger }: { ad: string; alan: K; deger: BolgeTercih[K]; secenekler: [BolgeTercih[K], string][] }) {
  return (
    <div className="db15-r">
      <span className="db15-ad" id={`db15-${String(alan)}`}>{ad}</span>
      <div className="v15-seg db15-seg" role="radiogroup" aria-labelledby={`db15-${String(alan)}`}>
        {secenekler.map(([v, et]) => (
          <button key={String(v)} type="button" role="radio" aria-checked={deger === v} aria-current={deger === v ? 'page' : undefined} onClick={() => bolgeYaz({ [alan]: v } as Partial<BolgeTercih>)}>{et}</button>
        ))}
      </div>
    </div>
  );
}

export default function DilBolgeV15() {
  const t = useBolge();
  const g = bugun();
  const tz = saatDilimi();
  useV15Baslik({ baslik: 'Dil ve bölge', alt: 'Profil ve ayarlar' });
  const farkYaz = tz.farkDk === 0 ? '' : `${Math.abs(tz.farkDk) % 60 ? `${(Math.abs(tz.farkDk) / 60).toFixed(1).replace('.', ',')}` : Math.abs(tz.farkDk) / 60} saat ${tz.farkDk > 0 ? 'ileride' : 'geride'}`;
  return (
    <div className="db15">
      <h1 className="sr-only">Dil ve bölge</h1>
      <div className="db15-dil v15-card">
        <span className="v15-tile"><Globe aria-hidden /></span>
        <span className="kp15-t"><b>Dil: Türkçe</b><span className="v15-cap">MeDSor şimdilik yalnız Türkçe; ders içerikleri, sesli anlatımlar ve sorular Türkçedir.</span></span>
      </div>

      <section className="v15-card db15-k" aria-label="Biçim tercihleri">
        <Secim ad="Tarih biçimi" alan="tarih" deger={t.tarih} secenekler={[['uzun', tarihYaz(g, { ...t, tarih: 'uzun' }, { gunAdi: false })], ['kisa', tarihYaz(g, { ...t, tarih: 'kisa' }, { gunAdi: false })]]} />
        <Secim ad="Saat biçimi" alan="saat" deger={t.saat} secenekler={[['24', saatYaz('13:30', { ...t, saat: '24' })], ['12', saatYaz('13:30', { ...t, saat: '12' })]]} />
        <Secim ad="Haftanın ilk günü" alan="haftaBas" deger={t.haftaBas} secenekler={[[1, 'Pazartesi'], [0, 'Pazar']]} />
      </section>
      <p className="v15-cap db15-not">Bu tercihler bu cihazda saklanır; ders programında, Bugün sayfasındaki program kartında ve arka plan işlerinde uygulanır.</p>

      <div className="db15-dil v15-card">
        <span className="kp15-t">
          <b>Saat dilimi</b>
          <span className="v15-cap">Cihazın: {tz.ad || 'bilinmiyor'}{farkYaz ? ` · Türkiye saatinden ${farkYaz}` : ' · Türkiye saati'}</span>
          <span className="v15-cap">Ders programı ve sınav takvimi Türkiye saatine (UTC+3) göredir; saatler olduğu gibi gösterilir.</span>
        </span>
      </div>
    </div>
  );
}
