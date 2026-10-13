import React, { useEffect, useState } from 'react';
import { CloudUpload, Download, RefreshCw, CheckCircle2, ShieldCheck, MessageSquare, BookOpen, Clock, Bell } from 'lucide-react';
import {
  backupUserDataToDatabase,
  restoreUserDataFromDatabase,
  getLastBackupTime,
  collectLocalUserData,
} from '../../services/userDataSyncService';
import { toast } from '../ui/Toast';

/**
 * Ayarlar · Kullanıcı Veri, İstatistik & Bildirim Senkronizasyon Satırı:
 * Tüm istatistiklerin, deneme sınavlarının, çalışma sürelerinin, bildirimlerin,
 * notların ve yorumların Express sunucusuna ve Supabase PostgreSQL veritabanına
 * aktarılmasını, saklanmasını ve tek tıkla geri yüklenmesini sağlar.
 */
export const UserDataSyncRow: React.FC = () => {
  const [backupAt, setBackupAt] = useState<string>(getLastBackupTime);
  const [busyBackup, setBusyBackup] = useState(false);
  const [busyRestore, setBusyRestore] = useState(false);
  const [dataStats, setDataStats] = useState(() => {
    const bundle = collectLocalUserData();
    const selftestCount = Array.isArray(bundle.stats.selftestHistory) ? bundle.stats.selftestHistory.length : 0;
    const notifCount = Array.isArray(bundle.notifications) ? bundle.notifications.length : 0;
    const notesCount = Array.isArray(bundle.notes) ? bundle.notes.length : 0;
    const favCount = Array.isArray(bundle.stats.favorites) ? bundle.stats.favorites.length : 0;
    const sec = Object.values(bundle.stats.studySeconds || {}).reduce((a, s) => a + (Number(s) || 0), 0);
    const m = Math.round(sec / 60);
    return { selftestCount, notifCount, notesCount, favCount, minutes: m };
  });

  const refreshStats = () => {
    const bundle = collectLocalUserData();
    const selftestCount = Array.isArray(bundle.stats.selftestHistory) ? bundle.stats.selftestHistory.length : 0;
    const notifCount = Array.isArray(bundle.notifications) ? bundle.notifications.length : 0;
    const notesCount = Array.isArray(bundle.notes) ? bundle.notes.length : 0;
    const favCount = Array.isArray(bundle.stats.favorites) ? bundle.stats.favorites.length : 0;
    const sec = Object.values(bundle.stats.studySeconds || {}).reduce((a, s) => a + (Number(s) || 0), 0);
    const m = Math.round(sec / 60);
    setDataStats({ selftestCount, notifCount, notesCount, favCount, minutes: m });
    setBackupAt(getLastBackupTime());
  };

  useEffect(() => {
    const onSynced = () => refreshStats();
    window.addEventListener('medsoru:user-data-synced', onSynced);
    window.addEventListener('medsoru:user-data-restored', onSynced);
    window.addEventListener('storage', onSynced);
    return () => {
      window.removeEventListener('medsoru:user-data-synced', onSynced);
      window.removeEventListener('medsoru:user-data-restored', onSynced);
      window.removeEventListener('storage', onSynced);
    };
  }, []);

  const handleBackup = async () => {
    setBusyBackup(true);
    try {
      const res = await backupUserDataToDatabase();
      if (res.success) {
        setBackupAt(res.backedUpAt || new Date().toISOString());
        refreshStats();
        toast.success('Veritabanına Kaydedildi', 'İstatistiklerin, bildirimlerin ve verilerin başarıyla yedeklendi.');
      } else {
        toast.error('Yedekleme Başarısız', res.error || 'Bağlantı hatası');
      }
    } catch (err: any) {
      toast.error('Hata', err.message);
    } finally {
      setBusyBackup(false);
    }
  };

  const handleRestore = async () => {
    if (!window.confirm('Veritabanındaki verileriniz çekilecek ve bu cihazdaki verilerinizle birleştirilecektir. Devam edilsin mi?')) {
      return;
    }
    setBusyRestore(true);
    try {
      const res = await restoreUserDataFromDatabase();
      if (res.success) {
        refreshStats();
        toast.success('Veriler Geri Yüklendi', 'Veritabanındaki tüm verileriniz yerel depolama ile birleştirildi.');
      } else {
        toast.error('Geri Yükleme Başarısız', res.error || 'Veritabanında kayıtlı yedek bulunamadı.');
      }
    } catch (err: any) {
      toast.error('Hata', err.message);
    } finally {
      setBusyRestore(false);
    }
  };

  return (
    <div className="ui-row has-icon ui-row-stack">
      {/* Dar ekranda düğmeler başlığın altına iner (başlık tek harflik sütuna sıkışmasın) */}
      <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '10px 12px', minWidth: 0, justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, minWidth: 0, flex: '1 1 220px' }}>
          <span
            className="ui-ico"
            style={{ '--ico-bg': 'var(--color-accent)', '--ico-fg': 'var(--color-on-solid)' } as React.CSSProperties}
          >
            <ShieldCheck strokeWidth={2.1} />
          </span>
          <span className="ui-row-main">
            <b>Veritabanı Eşitleme & Yedekleme</b>
            <span>
              {backupAt
                ? `Son yedek: ${new Date(backupAt).toLocaleString('tr-TR', { dateStyle: 'short', timeStyle: 'short' })}`
                : 'İstatistikler, bildirimler ve ilerlemeler veritabanına aktarılır'}
            </span>
          </span>
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginLeft: 'auto' }}>
          <button
            type="button"
            className={`ui-btn is-sm is-tonal ${busyRestore ? 'is-loading' : ''}`}
            onClick={handleRestore}
            disabled={busyRestore || busyBackup}
            title="Veritabanındaki verileri indir ve birleştir"
          >
            <Download className="w-3.5 h-3.5" /> Geri Yükle
          </button>
          <button
            type="button"
            className={`ui-btn is-sm is-primary ${busyBackup ? 'is-loading' : ''}`}
            onClick={handleBackup}
            disabled={busyBackup || busyRestore}
            title="Tüm verileri sunucuya ve Supabase veritabanına kaydet"
          >
            <CloudUpload className="w-3.5 h-3.5" /> Veritabanına Yedekle
          </button>
        </div>
      </div>

      {/* Mini İstatistik Sayacı */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(110px, 1fr))',
          gap: 8,
          padding: '10px 12px',
          background: 'var(--color-surface-2)',
          borderRadius: 8,
          fontSize: 12,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <BookOpen className="w-3.5 h-3.5 text-accent" />
          <span><b>{dataStats.selftestCount}</b> deneme/test</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <Clock className="w-3.5 h-3.5 text-info" />
          <span><b>{dataStats.minutes}</b> dk çalışma</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <Bell className="w-3.5 h-3.5 text-warning" />
          <span><b>{dataStats.notifCount}</b> bildirim</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <CheckCircle2 className="w-3.5 h-3.5 text-success" />
          <span><b>{dataStats.notesCount}</b> not / <b>{dataStats.favCount}</b> fav</span>
        </div>
      </div>

      <span className="ui-hint" style={{ fontSize: 11.5 }}>
        Verileriniz sunucu diskinde atomik olarak saklanır ve Oracle/Supabase PostgreSQL veritabanı bulutuna senkronize edilir.
      </span>
    </div>
  );
};
