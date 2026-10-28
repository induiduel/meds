import { Clapperboard, Clock, Download, Pause, Play, RotateCcw, TriangleAlert, X } from 'lucide-react';
import { useArkaPlanOzet } from '../../services/arkaPlanIsleri';
import { ayarYaz, duraklat, kuyrugaEkle, kuyruktanCikar, type Paket } from '../../services/cevrimdisi/paketMotoru';
import { boyutYaz } from '../../services/cevrimdisi/dersBirimleri';
import { cdVideoIptal } from '../canliDers/cdVideoIs';
import '../../styles/cevrimdisi.css';
import '../../styles/v15/kisisel.css';

/**
 * H308: Arka plan işleri artık ayrı sayfa değil; birleşik Çevrimdışı ve indirmeler (/cevrimdisi#isler) sayfasının
 * "İndirme kuyruğu" bölümü. Süren paket indirmesi (paketMotoru), sesli ders video dışa aktarımı (cdVideoIs), sıradakiler,
 * yarıda kalanlar. Eşitleme, tamamlananlar (İndirilenler) ve Yalnız Wi-Fi (Ayarlar) CevrimdisiView'da tek yerde.
 */
const kalanYaz = (sn: number) => (sn < 60 ? `${Math.max(1, Math.round(sn))} sn kaldı` : sn < 3600 ? `${Math.round(sn / 60)} dk kaldı` : `${Math.round(sn / 3600)} sa kaldı`);

export default function ArkaPlanIsleri() {
  const { s, video } = useArkaPlanOzet();
  const ad = (id: string) => s.katalog.find((p: Paket) => p.id === id)?.baslik || s.kayitlar[id]?.baslik || (id === 'uygulama' ? 'Uygulama dosyaları' : id);
  const hatalar = Object.entries(s.hatalar);
  const sira = s.kuyruk.filter((id) => id !== s.aktif?.id);
  const a = s.aktif;
  const oran = a && a.toplam ? Math.min(100, Math.round((a.alinan / a.toplam) * 100)) : 0;

  return (
    <div className="ap15 cv15-bolum">
      <section aria-label="Sürenler">
        {!a && !video && !sira.length ? (
          <p className="b15-bos v15-card kp15-bos">Şu an süren indirme ya da video yok. Aşağıdaki Toplu indir bölümünden ders ekleyebilirsin; sesli derste video dışa aktarımı da burada izlenir.</p>
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
        {/* H310: "Hepsini iptal et" eski Çevrimdışı durum kartındaki Sıra açılırından buraya taşındı */}
        {sira.length > 1 && <button type="button" className="v15-btn is-ghost ap15-surdur" onClick={() => kuyruktanCikar([...s.kuyruk])}><X aria-hidden /> Hepsini iptal et</button>}
        {s.duraklat && !a && sira.length > 0 && <button type="button" className="v15-btn is-soft ap15-surdur" onClick={() => duraklat(false)}><Play aria-hidden /> İndirmeleri sürdür</button>}
      </section>

      {hatalar.length > 0 && (
        <section aria-labelledby="ap15-h">
          <h3 id="ap15-h" className="v15-label kp15-sec">Yarıda kalanlar</h3>
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

    </div>
  );
}

