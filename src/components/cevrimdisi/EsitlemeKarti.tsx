/**
 * Çevrimdışı merkezi › eşitleme kartı: bu cihazda bekleyen profil değişiklikleri (çözülen sorular, süre, ilerleme — userKvSync),
 * gönderim kuyruğundaki işlemler (oy, yorum, hata bildirimi — offlineDatabaseService) ve son eşitleme zamanı. "Şimdi eşitle"
 * ikisini birden gönderir. Bağlantı gelince bunlar zaten kendiliğinden gider (userDataSyncService 'online' + arka plan eşitleme).
 */
import { useEffect, useState } from 'react';
import { Check, CloudOff, Loader2, RefreshCw } from 'lucide-react';
import { useNetState } from '../../services/net';
import { dirtyKvCount, onProfileDataChange } from '../../services/userKvSync';

// H309: durum kartı da son eşitleme zamanını aynı biçimde yazar
export const zamanYaz = (iso: string) => {
  if (!iso) return 'henüz yok';
  const fark = (Date.now() - Date.parse(iso)) / 1000;
  if (!isFinite(fark)) return 'henüz yok';
  if (fark < 60) return 'az önce';
  if (fark < 3600) return `${Math.round(fark / 60)} dk önce`;
  if (fark < 86400) return `${Math.round(fark / 3600)} sa önce`;
  return new Date(iso).toLocaleString('tr-TR', { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' });
};

export default function EsitlemeKarti() {
  const ag = useNetState();
  const [bekleyen, setBekleyen] = useState(dirtyKvCount);
  const [kuyruk, setKuyruk] = useState(0);
  const [son, setSon] = useState('');
  const [is, setIs] = useState<'bos' | 'gonder' | 'tamam' | 'hata'>('bos');
  const [hata, setHata] = useState('');

  useEffect(() => {
    let canli = true;
    const yenile = async () => {
      setBekleyen(dirtyKvCount());
      const [{ getLastBackupTime }, { offlineDatabaseService }] = await Promise.all([
        import('../../services/userDataSyncService'), import('../../services/offlineDatabaseService'),
      ]);
      if (!canli) return;
      setSon(getLastBackupTime());
      setKuyruk(offlineDatabaseService.getState().queuedActionsCount || 0);
    };
    void yenile();
    const off = onProfileDataChange(() => setBekleyen(dirtyKvCount()));
    const t = window.setInterval(yenile, 5000);
    window.addEventListener('medsoru:user-data-synced', yenile);
    return () => { canli = false; off(); window.clearInterval(t); window.removeEventListener('medsoru:user-data-synced', yenile); };
  }, []);

  const esitle = async () => {
    setIs('gonder');
    setHata('');
    const [{ backupUserDataToDatabase, getLastBackupTime }, { offlineDatabaseService }] = await Promise.all([
      import('../../services/userDataSyncService'), import('../../services/offlineDatabaseService'),
    ]);
    const [r] = await Promise.all([backupUserDataToDatabase(), offlineDatabaseService.syncOfflineQueue().catch(() => null)]);
    setBekleyen(dirtyKvCount());
    setSon(getLastBackupTime());
    setKuyruk(offlineDatabaseService.getState().queuedActionsCount || 0);
    if (r.success) setIs('tamam');
    else { setIs('hata'); setHata(r.error || 'Eşitlenemedi.'); }
  };

  const hepsiGitti = bekleyen === 0 && kuyruk === 0;
  return (
    <section className="cv-kart cv-esit" aria-labelledby="cv-esit-b">
      <div className="cv-kart-bas">
        <h2 id="cv-esit-b">Veri eşitleme</h2>
        <span className={`cv-etiket ${hepsiGitti ? 'is-ok' : 'is-warn'}`}>{hepsiGitti ? 'Güncel' : 'Bekleyen var'}</span>
      </div>
      <ul className="cv-esit-liste">
        <li><span>Gönderilmeyi bekleyen ilerleme</span><b>{bekleyen ? `${bekleyen} kayıt` : 'yok'}</b></li>
        <li><span>Gönderim kuyruğu (oy, yorum, bildirim)</span><b>{kuyruk ? `${kuyruk} işlem` : 'yok'}</b></li>
        <li><span>Son eşitleme</span><b>{zamanYaz(son)}</b></li>
      </ul>
      <p className="cv-not">
        {ag === 'offline'
          ? 'İnternet yok: çözdüğün sorular, çalışma süren ve ilerlemen bu cihazda güvende; bağlantı gelince kendiliğinden gönderilir.'
          : 'Çözdüğün sorular, çalışma süren, işaretlerin ve ilerlemen birkaç saniye içinde hesabına yazılır; diğer cihazların da anında görür.'}
      </p>
      <div className="cv-esit-alt">
        {is === 'hata' && <small className="cv-hata">{hata}</small>}
        {is === 'tamam' && <small className="cv-ok"><Check aria-hidden="true" /> Eşitlendi</small>}
        <button type="button" className="cv-btn" disabled={ag === 'offline' || is === 'gonder'} onClick={() => void esitle()}>
          {is === 'gonder' ? <Loader2 className="cv-don" aria-hidden="true" /> : ag === 'offline' ? <CloudOff aria-hidden="true" /> : <RefreshCw aria-hidden="true" />}
          <span>Şimdi eşitle</span>
        </button>
      </div>
    </section>
  );
}
