import React, { useEffect, useState } from 'react';
import {
  Archive, BookOpenText, CheckCircle2, CloudDownload, Layers, RefreshCw, Share2, Smartphone, Trash2, WifiOff, FileQuestion, Database, Inbox,
} from 'lucide-react';
import { offlineDatabaseService, OfflineState } from '../../services/offlineDatabaseService';
import { pwaService, PwaState } from '../../services/pwaService';
import { Dialog } from '../ui/Dialog';
import { DeviceStorageSection } from './DeviceStorageSection';
import '../../styles/ayrik-of.css';

interface OfflineDatabaseModalProps {
  isOpen: boolean;
  onClose: () => void;
  /** Yönetici teknik ayrıntıyı (depo sayıları, SW, kuyruk) görür; öğrenci yalnız durumu ve tek eylemi */
  isAdmin?: boolean;
}

const nf = (n: number) => n.toLocaleString('tr-TR');
const when = (iso: string | null, full = false) =>
  iso
    ? new Date(iso).toLocaleString('tr-TR', full
      ? { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' }
      : { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' })
    : '';

const useOfflineState = () => {
  const [o, setO] = useState<OfflineState>(offlineDatabaseService.getState());
  const [p, setP] = useState<PwaState>(pwaService.getState());
  useEffect(() => {
    const a = offlineDatabaseService.subscribe(setO);
    const b = pwaService.subscribe(setP);
    return () => {
      a();
      b();
    };
  }, []);
  return [o, p] as const;
};

const isIos = () => typeof window !== 'undefined' && /iphone|ipad|ipod/i.test(window.navigator.userAgent);

/** Durum satırı: tek bakışta "cihazda hazır mı" */
const StateLine: React.FC<{ o: OfflineState; full?: boolean }> = ({ o, full }) => {
  const tone = o.isDownloading ? 'is-busy' : !o.isOnline ? 'is-offline' : o.isDatabaseDownloaded ? 'is-ready' : 'is-empty';
  const Icon = o.isDownloading ? RefreshCw : !o.isOnline ? WifiOff : o.isDatabaseDownloaded ? CheckCircle2 : CloudDownload;
  const title = o.isDownloading
    ? 'İndiriliyor'
    : !o.isOnline
      ? o.isDatabaseDownloaded ? 'İnternet yok · cihazdaki veriyle çalışıyor' : 'İnternet yok'
      : o.isDatabaseDownloaded ? 'Cihazında hazır' : 'Henüz cihazında değil';
  const sub = o.isDownloading
    ? o.progress.stage
    : o.isDatabaseDownloaded
      ? o.stats.downloadedAt ? `Son güncelleme ${when(o.stats.downloadedAt, full)}` : 'İnternet olmadan da çalışır.'
      : 'İndirince internet olmadan da çalışırsın.';
  return (
    <div className={`of-state ${tone}`} role="status">
      <span className="of-orb" aria-hidden><Icon /></span>
      <div className="of-state-t">
        <b>{title}</b>
        <span>{sub}</span>
      </div>
    </div>
  );
};

const Progress: React.FC<{ o: OfflineState; detail?: boolean }> = ({ o, detail }) => (
  <div className="of-progress" aria-live="polite">
    <div className="of-progress-top">
      <span>{o.progress.stage}</span>
      <b>%{o.progress.percent}</b>
    </div>
    <div className="ms-progress"><span style={{ width: `${o.progress.percent}%` }} /></div>
    {detail && o.progress.totalCount ? <span className="of-mono">{nf(o.progress.currentCount || 0)} / {nf(o.progress.totalCount)}</span> : null}
  </div>
);

const InstallRow: React.FC<{ p: PwaState }> = ({ p }) => {
  if (p.isInstalled) {
    return <p className="of-note is-ok"><Smartphone aria-hidden /> Uygulama olarak kurulu (Tam ekran PWA aktif).</p>;
  }
  return (
    <div className="of-install">
      <div className="of-install-t">
        <Smartphone aria-hidden />
        <span>
          <b>Uygulamayı cihaza yükle (PWA)</b>
          <small>
            {p.isIos
              ? p.iosBrowser === 'crios'
                ? 'Chrome adres çubuğundaki Paylaş › Ana Ekrana Ekle ile tam ekran açılır.'
                : 'Safari Paylaş › Ana Ekrana Ekle ile gerçek tam ekran açılır.'
              : 'Ana ekrandan adres çubuğu olmadan, gerçek tam ekran açılır.'}
          </small>
        </span>
        <button
          type="button"
          className="ms-btn is-tonal is-sm"
          onClick={() => pwaService.promptInstall()}
        >
          {p.hasNativePrompt ? 'Yükle' : 'Ana Ekrana Ekle'}
        </button>
      </div>
    </div>
  );
};

/** İki adımlı kaldırma: ilk dokunuş onay ister */
const ClearButton: React.FC<{ disabled?: boolean; label: string }> = ({ disabled, label }) => {
  const [arm, setArm] = useState(false);
  useEffect(() => {
    if (!arm) return;
    const t = window.setTimeout(() => setArm(false), 3500);
    return () => window.clearTimeout(t);
  }, [arm]);
  return (
    <button
      type="button"
      disabled={disabled}
      className={`ms-btn is-danger is-sm ${arm ? 'is-armed' : ''}`}
      onClick={async () => {
        if (!arm) return setArm(true);
        setArm(false);
        await offlineDatabaseService.clearDatabase();
      }}
    >
      <Trash2 /> {arm ? 'Emin misin? Tekrar dokun' : label}
    </button>
  );
};

const StudentView: React.FC<{ o: OfflineState; p: PwaState }> = ({ o, p }) => {
  const s = o.stats;
  const rows: [React.ElementType, string, string][] = [
    [Archive, 'Çıkmış sorular', s.pastQuestionsCount ? nf(s.pastQuestionsCount) : ''],
    [Layers, 'Öğren desteleri', s.decksCount ? nf(s.decksCount) : ''],
    [BookOpenText, 'Sözlük', s.glossaryCount ? nf(s.glossaryCount) : ''],
    [FileQuestion, 'Ezber kartları', s.flashcardsCount ? nf(s.flashcardsCount) : ''],
  ];
  return (
    <>
      <StateLine o={o} />
      <ul className={`of-list ${o.isDatabaseDownloaded ? 'is-ready' : ''}`}>
        {rows.map(([Icon, label, n], i) => (
          <li key={label} style={{ '--i': i } as React.CSSProperties}>
            <Icon aria-hidden />
            <span>{label}</span>
            {o.isDatabaseDownloaded ? (n ? <b>{n}</b> : <em>güncellemede gelir</em>) : <i aria-hidden />}
          </li>
        ))}
      </ul>
      {o.isDownloading ? (
        <Progress o={o} />
      ) : (
        <button
          type="button"
          className="ms-btn is-primary of-main"
          disabled={!o.isOnline}
          onClick={() => offlineDatabaseService.downloadEntireDatabase()}
        >
          {o.isDatabaseDownloaded ? <><RefreshCw /> Güncelle</> : <><CloudDownload /> Cihaza indir · ~{s.estimatedSizeMb || 25} MB</>}
        </button>
      )}
      {!o.isOnline && !o.isDownloading && <p className="of-note">İndirmek için internete bağlan.</p>}
      <InstallRow p={p} />
      <DeviceStorageSection o={o} />
      {o.isDatabaseDownloaded && !o.isDownloading && (
        <div className="of-foot"><ClearButton label="Cihazdan kaldır" /></div>
      )}
    </>
  );
};

const AdminView: React.FC<{ o: OfflineState; p: PwaState }> = ({ o, p }) => {
  const s = o.stats;
  const [syncing, setSyncing] = useState(false);
  const [syncMsg, setSyncMsg] = useState('');
  const kv: [string, string][] = [
    ['Çıkmış soru', nf(s.pastQuestionsCount)],
    ['Havuz sorusu', nf(s.poolQuestionsCount)],
    ['Kurul', nf(s.committeesCount)],
    ['Deste', nf(s.decksCount)],
    ['Özet', nf(s.summariesCount)],
    ['Sözlük', nf(s.glossaryCount)],
    ['Kart', nf(s.flashcardsCount)],
    ['Toplam öge', nf(s.totalItems)],
    ['Tahmini boyut', `${s.estimatedSizeMb || 0} MB`],
    ['Son indirme', s.downloadedAt ? when(s.downloadedAt, true) : '—'],
  ];
  const sys: [string, boolean, string, string][] = [
    ['Ağ', o.isOnline, 'çevrimiçi', 'çevrimdışı'],
    ['Service Worker', p.isRegistered, 'kayıtlı', 'yok'],
    ['Background Sync', p.backgroundSyncSupported, 'var', 'yok'],
    ['Periodic Sync', p.periodicSyncSupported, 'var', 'yok'],
    ['Kurulum', p.isInstalled, 'uygulama', 'tarayıcı'],
  ];
  return (
    <>
      <StateLine o={o} full />
      {o.isDownloading && <Progress o={o} detail />}
      <section className="of-sec" aria-label="Depolar">
        <h3>IndexedDB · medsoru_offline_db</h3>
        <dl className="of-kv">
          {kv.map(([k, v]) => (
            <div key={k}><dt>{k}</dt><dd>{v}</dd></div>
          ))}
        </dl>
      </section>
      <section className="of-sec" aria-label="Sistem">
        <h3>Sistem</h3>
        <ul className="of-sys">
          {sys.map(([k, ok, yes, no]) => (
            <li key={k} className={ok ? 'is-ok' : ''}><i aria-hidden />{k}<b>{ok ? yes : no}</b></li>
          ))}
          {p.hasUpdate && <li className="is-warn"><i aria-hidden />Yeni sürüm<b>hazır</b></li>}
          <li className={o.queuedActionsCount ? 'is-warn' : 'is-ok'}><i aria-hidden />Bekleyen işlem<b>{nf(o.queuedActionsCount)}</b></li>
        </ul>
      </section>
      <InstallRow p={p} />
      <DeviceStorageSection o={o} />
      {syncMsg && <p className="of-note">{syncMsg}</p>}
      <div className="of-actions">
        <button type="button" className="ms-btn is-primary is-sm" disabled={o.isDownloading || !o.isOnline} onClick={() => offlineDatabaseService.downloadEntireDatabase()}>
          {o.isDatabaseDownloaded ? <><RefreshCw /> Yeniden indir</> : <><CloudDownload /> İndir</>}
        </button>
        <button
          type="button"
          className="ms-btn is-sm"
          disabled={syncing || !o.isOnline || !o.queuedActionsCount}
          onClick={async () => {
            setSyncing(true);
            const r = await offlineDatabaseService.syncOfflineQueue();
            setSyncing(false);
            setSyncMsg(`Kuyruk: ${r.synced} eşitlendi, ${r.failed} başarısız.`);
          }}
        >
          <Inbox /> Kuyruğu eşitle
        </button>
        <span className="flex-1" />
        <ClearButton disabled={o.isDownloading || !o.isDatabaseDownloaded} label="Temizle" />
      </div>
    </>
  );
};

export const OfflineDatabaseModal: React.FC<OfflineDatabaseModalProps> = ({ isOpen, onClose, isAdmin }) => {
  const [o, p] = useOfflineState();
  if (!isOpen) return null;
  return (
    <Dialog
      title={isAdmin ? <span className="inline-flex items-center gap-2"><Database className="w-4 h-4 text-ink-3" /> Çevrimdışı veritabanı</span> : 'Çevrimdışı kullanım'}
      subtitle={isAdmin ? 'Yönetici görünümü · depolar, eşitleme, PWA' : undefined}
      onClose={onClose}
      width={isAdmin ? 'max-w-lg' : 'max-w-md'}
    >
      <button type="button" className="ui-btn is-primary" style={{ width: '100%', marginBottom: 12, whiteSpace: 'normal', height: 'auto', minHeight: 44, padding: '10px 14px', lineHeight: 1.3, textAlign: 'center' }}
        onClick={() => { onClose(); void import('../../router').then((m) => m.navigateTo('/cevrimdisi')); }}>
        Çevrimdışı merkezini aç — dersleri seç, indir, yönet
      </button>
      <div className="of">{isAdmin ? <AdminView o={o} p={p} /> : <StudentView o={o} p={p} />}</div>
    </Dialog>
  );
};
