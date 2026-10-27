import { useState } from 'react';
import { Check, ChevronRight, X } from 'lucide-react';
import { linkClick, navigateTo, pathFor, type AppRoute } from '../../router';
import { ilkAdimlarKapat, useIlkAdimlar, useIlkAdimlarKapali, type IlkAdim } from '../../services/ilkAdimlar';
import { userNotificationService } from '../../services/userNotificationService';
import { profilKurulumAc } from './ProfilKurulumV15';
import { useV15Baslik } from './baslik';
import '../../styles/v15/kisisel.css';

/**
 * v15 · İlk adımlar (tasarım AB11 baslangicGorev) — /ilk-adimlar sayfası + Bugün'de kapatılabilir kart.
 * Durum services/ilkAdimlar'dan (gerçek kayıtlar); ödül/puan vaadi yok.
 */
function Liste({ adimlar, onIzin }: { adimlar: IlkAdim[]; onIzin: () => void }) {
  return (
    <ul className="ia15-l">
      {adimlar.map((a) => {
        const ic = (
          <>
            <span className={`ia15-chk${a.tamam ? ' is-on' : ''}`} aria-hidden>{a.tamam && <Check />}</span>
            <span className="ia15-t"><b>{a.ad}</b><span className="v15-cap">{a.ac}</span></span>
            {!a.tamam && <ChevronRight className="ia15-ok" aria-hidden />}
          </>
        );
        const etiket = `${a.ad}${a.tamam ? ' (tamamlandı)' : ''}`;
        if (a.tamam) return <li key={a.id} className="is-tamam"><div className="ia15-r" aria-label={etiket}>{ic}</div></li>;
        if (a.git === 'profil') return <li key={a.id}><button type="button" className="ia15-r" onClick={profilKurulumAc}>{ic}</button></li>;
        if (a.git === 'bildirim') return <li key={a.id}><button type="button" className="ia15-r" onClick={onIzin}>{ic}</button></li>;
        const r = a.git as AppRoute;
        return <li key={a.id}><a className="ia15-r" href={pathFor(r)} onClick={linkClick(() => navigateTo(pathFor(r)))}>{ic}</a></li>;
      })}
    </ul>
  );
}

const useIzin = () => {
  const [, yenile] = useState(0);
  const [not, setNot] = useState('');
  const izin = async () => {
    if (typeof Notification === 'undefined') { setNot('Bu tarayıcı bildirimleri desteklemiyor.'); return; }
    const ok = await userNotificationService.requestPushPermission();
    setNot(ok ? '' : 'Bildirim izni verilmedi; tarayıcının site ayarlarından açabilirsin.');
    yenile((n) => n + 1);
  };
  return { izin, not };
};

export default function IlkAdimlarV15() {
  const adimlar = useIlkAdimlar();
  const kapali = useIlkAdimlarKapali();
  const { izin, not } = useIzin();
  const n = adimlar.filter((a) => a.tamam).length;
  useV15Baslik({ baslik: 'İlk adımlar', alt: `${n} / ${adimlar.length} tamam` });
  return (
    <div className="ia15">
      <h1 className="sr-only">İlk adımlar</h1>
      <div className="v15-card ia15-kart">
        <span className="v15-bar" role="progressbar" aria-valuemin={0} aria-valuemax={adimlar.length} aria-valuenow={n} aria-label="İlerleme"><span style={{ width: `${(n / adimlar.length) * 100}%` }} /></span>
        <Liste adimlar={adimlar} onIzin={izin} />
      </div>
      {not && <p className="v15-cap" role="status">{not}</p>}
      <p className="v15-cap ia15-alt">
        {n === adimlar.length ? 'Hepsini tamamladın. ' : 'Durumlar çalışma kayıtlarından kendiliğinden işaretlenir. '}
        {kapali
          ? <button type="button" className="ia15-link" onClick={() => ilkAdimlarKapat(false)}>Bugün sayfasında yeniden göster</button>
          : <button type="button" className="ia15-link" onClick={() => ilkAdimlarKapat(true)}>Bugün sayfasında gösterme</button>}
      </p>
    </div>
  );
}

/** Bugün kartı: kapatılmadıysa ve tamamlanmamış adım varsa ilk üç eksik adım */
export function IlkAdimlarKarti() {
  const adimlar = useIlkAdimlar();
  const kapali = useIlkAdimlarKapali();
  const { izin } = useIzin();
  const n = adimlar.filter((a) => a.tamam).length;
  if (kapali || n === adimlar.length) return null;
  const href = pathFor('ilk_adimlar');
  return (
    <section className="v15-card ia15-kart ia15-bugun" aria-labelledby="ia15-h">
      <div className="ia15-bas">
        <h2 id="ia15-h" className="v15-h2">İlk adımlar</h2>
        <span className="v15-cap">{n} / {adimlar.length}</span>
        <button type="button" className="v15-ib ia15-x" onClick={() => ilkAdimlarKapat(true)} aria-label="İlk adımlar kartını kapat" title="Kapat"><X aria-hidden /></button>
      </div>
      <span className="v15-bar" role="progressbar" aria-valuemin={0} aria-valuemax={adimlar.length} aria-valuenow={n} aria-label="İlerleme"><span style={{ width: `${(n / adimlar.length) * 100}%` }} /></span>
      <Liste adimlar={adimlar.filter((a) => !a.tamam).slice(0, 3)} onIzin={izin} />
      <a className="ia15-tum" href={href} onClick={linkClick(() => navigateTo(href))}>Tüm adımlar</a>
    </section>
  );
}
