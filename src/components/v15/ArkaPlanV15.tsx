import { CheckCircle2, Clapperboard, Clock, Download, Pause, Play, RotateCcw, TriangleAlert, X } from 'lucide-react';
import { useArkaPlanOzet } from '../../services/arkaPlanIsleri';
import { ayarYaz, duraklat, kuyrugaEkle, kuyruktanCikar, type Paket } from '../../services/cevrimdisi/paketMotoru';
import { boyutYaz } from '../../services/cevrimdisi/dersBirimleri';
import { cdVideoIptal } from '../canliDers/cdVideoIs';
import { saatDate, useBolge } from '../../services/bolgeTercih';
import { linkClick, navigateTo, pathFor } from '../../router';
import EsitlemeKarti from '../cevrimdisi/EsitlemeKarti';
import { useV15Baslik } from './baslik';
import '../../styles/cevrimdisi.css';
import '../../styles/v15/kisisel.css';

/**
 * v15 · Arka plan işleri (tasarım AB01 arkaPlan) — /arka-plan. Yalnız cihazda gerçekten izlenen işler:
 * çevrimdışı paket indirmeleri (paketMotoru), sesli ders video dışa aktarımı (cdVideoIs), profil eşitlemesi (EsitlemeKarti).
 * Tamamlananlar: cihazdaki son indirilen paketler (IndexedDB kayıt defteri).
 */
const kalanYaz = (sn: number) => (sn < 60 ? `${Math.max(1, Math.round(sn))} sn kaldı` : sn < 3600 ? `${Math.round(sn / 60)} dk kaldı` : `${Math.round(sn / 3600)} sa kaldı`);

export default function ArkaPlanV15() {
  const { s, video, indirme } = useArkaPlanOzet();
  const bolge = useBolge();
  const ad = (id: string) => s.katalog.find((p: Paket) => p.id === id)?.baslik || s.kayitlar[id]?.baslik || (id === 'uygulama' ? 'Uygulama dosyaları' : id);
  const surer = indirme + (video ? 1 : 0);
  const hatalar = Object.entries(s.hatalar);
  const sira = s.kuyruk.filter((id) => id !== s.aktif?.id);
  useV15Baslik({ baslik: 'Arka plan işleri', alt: surer ? `${surer} iş${sira.length ? ` · ${sira.length} sırada` : ''}` : 'Şu an iş yok' });
  const tamamlanan = Object.values(s.kayitlar).filter((k) => !k.yarim).sort((a, b) => b.at - a.at).slice(0, 6);
  const a = s.aktif;
  const oran = a && a.toplam ? Math.min(100, Math.round((a.alinan / a.toplam) * 100)) : 0;
  const cevrimdisiHref = pathFor('cevrimdisi');

  return (
    <div className="ap15">
      <h1 className="sr-only">Arka plan işleri</h1>
      <section aria-labelledby="ap15-s">
        <h2 id="ap15-s" className="v15-label kp15-sec">Sürenler</h2>
        {!a && !video && !sira.length ? (
          <p className="b15-bos v15-card kp15-bos">Şu an arka planda süren indirme ya da video yok. Dersleri cihaza <a href={cevrimdisiHref} onClick={linkClick(() => navigateTo(cevrimdisiHref))}>Çevrimdışı</a> sayfasından indirebilirsin; sesli derste video dışa aktarımı da burada izlenir.</p>
        ) : (
          <ul className="ap15-l v15-card">
            {a && (
              <li>
                <span className={`v15-tile ${a.bekliyor ? 'is-w' : ''}`}>{a.bekliyor ? <Clock aria-hidden /> : <Download aria-hidden />}</span>
                <span className="ap15-t">
                  <b>{ad(a.id)}{a.bekliyor ? '' : s.duraklat ? ' · duraklatıldı' : ' indiriliyor'}</b>
                  {a.bekliyor ? <span className="v15-cap">{a.bekliyor}</span> : (
                    <>
                      <span className="v15-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={oran} aria-label="İndirme"><span style={{ width: `${oran}%` }} /></span>
                      <span className="v15-cap">{boyutYaz(a.alinan)} / {boyutYaz(a.toplam)} · dosya {a.dosya}/{a.dosyaSay}{a.hiz > 0 && a.toplam > a.alinan ? ` · ${kalanYaz((a.toplam - a.alinan) / a.hiz)}` : ''}</span>
                    </>
                  )}
                </span>
                {a.bekliyor?.startsWith('Wi-Fi') ? (
                  <button type="button" className="v15-btn is-ghost ap15-b" onClick={() => ayarYaz({ wifi: false })} title="Yalnız Wi-Fi ayarını kapatır">Şimdi indir</button>
                ) : !a.bekliyor && (
                  <button type="button" className="v15-ib" onClick={() => duraklat(!s.duraklat)} aria-label={s.duraklat ? 'Sürdür' : 'Duraklat'} title={s.duraklat ? 'Sürdür' : 'Duraklat'}>{s.duraklat ? <Play aria-hidden /> : <Pause aria-hidden />}</button>
                )}
              </li>
            )}
            {video && (
              <li>
                <span className="v15-tile is-ai"><Clapperboard aria-hidden /></span>
                <span className="ap15-t">
                  <b>Video hazırlanıyor · {video.baslik}</b>
                  <span className="v15-bar" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(video.ilerleme.oran * 100)} aria-label="Video"><span style={{ width: `${Math.round(video.ilerleme.oran * 100)}%` }} /></span>
                  <span className="v15-cap">{video.ilerleme.asama === 'hazirlik' ? 'Hazırlanıyor' : video.ilerleme.asama === 'bitiriliyor' ? 'Dosya bitiriliyor' : `%${Math.floor(video.ilerleme.oran * 100)}`}{video.ilerleme.kalanSn ? ` · ${kalanYaz(video.ilerleme.kalanSn)}` : ''} · {video.ad}</span>
                </span>
                <button type="button" className="v15-ib" onClick={cdVideoIptal} aria-label="Videoyu iptal et" title="İptal"><X aria-hidden /></button>
              </li>
            )}
            {sira.map((id) => (
              <li key={id}>
                <span className="v15-tile is-n"><Clock aria-hidden /></span>
                <span className="ap15-t"><b>{ad(id)}</b><span className="v15-cap">Sırada{s.duraklat ? ' · indirmeler duraklatıldı' : ''}</span></span>
                <button type="button" className="v15-ib" onClick={() => kuyruktanCikar([id])} aria-label={`${ad(id)} sırasından çıkar`} title="Sıradan çıkar"><X aria-hidden /></button>
              </li>
            ))}
          </ul>
        )}
        {s.duraklat && !a && sira.length > 0 && <button type="button" className="v15-btn is-soft ap15-surdur" onClick={() => duraklat(false)}><Play aria-hidden /> İndirmeleri sürdür</button>}
      </section>

      {hatalar.length > 0 && (
        <section aria-labelledby="ap15-h">
          <h2 id="ap15-h" className="v15-label kp15-sec">Yarıda kalanlar</h2>
          <ul className="ap15-l v15-card">
            {hatalar.map(([id, m]) => (
              <li key={id}>
                <span className="v15-tile is-b"><TriangleAlert aria-hidden /></span>
                <span className="ap15-t"><b>{ad(id)}</b><span className="v15-cap">{m}</span></span>
                <button type="button" className="v15-ib" onClick={() => kuyrugaEkle([id])} aria-label={`${ad(id)} yeniden dene`} title="Yeniden dene"><RotateCcw aria-hidden /></button>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section aria-labelledby="ap15-e">
        <h2 id="ap15-e" className="v15-label kp15-sec">Eşitleme</h2>
        <div className="cv ap15-cv"><EsitlemeKarti /></div>
      </section>

      <section aria-labelledby="ap15-t">
        <h2 id="ap15-t" className="v15-label kp15-sec">Tamamlanan indirmeler</h2>
        {!tamamlanan.length ? (
          <p className="b15-bos v15-card kp15-bos">Bu cihazda indirilmiş paket yok.</p>
        ) : (
          <ul className="ap15-l v15-card">
            {tamamlanan.map((k) => (
              <li key={k.id}>
                <span className="v15-tile is-ok"><CheckCircle2 aria-hidden /></span>
                <span className="ap15-t"><b>{k.baslik}</b><span className="v15-cap">{boyutYaz(k.bayt)} · {new Date(k.at).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })} {saatDate(new Date(k.at), bolge)}</span></span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <label className="ap15-ayar v15-card">
        <span><b>Yalnız Wi-Fi'dayken indir</b><span className="v15-cap">Hücresel veride indirmeler Wi-Fi gelene dek bekler.</span></span>
        <input type="checkbox" role="switch" checked={s.ayar.wifi} onChange={(e) => ayarYaz({ wifi: e.target.checked })} />
      </label>
    </div>
  );
}

