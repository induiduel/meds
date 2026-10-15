import React, { useMemo, useState } from 'react';
import { RotateCcw } from 'lucide-react';
import { RESET_SCOPES, countScope, resetProgress, type ResetScope } from '../../services/progressReset';
import { backupUserDataToDatabase } from '../../services/userDataSyncService';
import { toast } from '../ui/Toast';

/**
 * Ayarlar · İlerlemeyi sıfırla: kapsam seçilir, iki adımlı onayla silinir. Çalışma süresi, etkinlik günlüğü ve
 * çözüm/deneme istatistikleri (arşivlenerek) korunur; notlar, favoriler ve kaydedilenler silinmez.
 */
export const ProgressResetRow: React.FC = () => {
  const counts = useMemo(() => Object.fromEntries(RESET_SCOPES.map((s) => [s.id, countScope(s.id)])) as Record<ResetScope, number>, []);
  const [picked, setPicked] = useState<Set<ResetScope>>(() => new Set());
  const [confirm, setConfirm] = useState(false);
  const [busy, setBusy] = useState(false);

  const toggle = (id: ResetScope) => {
    setConfirm(false);
    setPicked((p) => {
      const n = new Set(p);
      n.has(id) ? n.delete(id) : n.add(id);
      return n;
    });
  };

  const secili = RESET_SCOPES.filter((x) => picked.has(x.id));
  const toplam = secili.reduce((a, x) => a + (counts[x.id] || 0), 0);
  const sayi = (n: number) => n.toLocaleString('tr-TR');

  const run = async () => {
    setBusy(true);
    try {
      resetProgress([...picked]);
      // Silme sunucuya gitsin; çevrimdışıysa sıfırlama damgası sonraki eşitlemede gider
      await backupUserDataToDatabase().catch(() => undefined);
      toast.success('İlerleme sıfırlandı', 'İstatistiklerin korundu.');
      window.setTimeout(() => window.location.reload(), 600);
    } catch {
      toast.error('Sıfırlanamadı', 'Tarayıcı depolamasına yazılamadı.');
      setBusy(false);
    }
  };

  return (
    <div className="prs">
      <div className="prs-h">
        <RotateCcw aria-hidden />
        <span>
          <b>İlerlemeyi sıfırla</b>
          <span>Seçtiğin ilerleme bu hesaptan ve tüm cihazlarından silinir. Çalışma süren, etkinlik geçmişin ve çözüm istatistiklerin korunur; notların ve kaydettiklerin silinmez.</span>
        </span>
      </div>
      <div className="prs-list">
        {RESET_SCOPES.map((s) => (
          <label key={s.id} className={`prs-opt${!counts[s.id] ? ' is-bos' : ''}`}>
            <input type="checkbox" checked={picked.has(s.id)} onChange={() => toggle(s.id)} disabled={busy || !counts[s.id]} />
            <span>
              <b>{s.title} <em>{counts[s.id] ? `${sayi(counts[s.id])} kayıt` : 'silinecek kayıt yok'}</em></b>
              <span>{s.desc}</span>
            </span>
          </label>
        ))}
      </div>
      <div className="prs-act">
        {confirm ? (
          <>
            <span className="prs-warn" role="alert">
              Silinecek: {secili.map((x) => x.title).join(', ')} ({sayi(toplam)} kayıt). Bu işlem geri alınamaz.
            </span>
            <button type="button" className="prs-btn" onClick={() => setConfirm(false)} disabled={busy}>Vazgeç</button>
            <button type="button" className="prs-btn is-bad" onClick={run} disabled={busy}>{busy ? 'Siliniyor…' : `Evet, ${sayi(toplam)} kaydı sil`}</button>
          </>
        ) : (
          <>
            {!picked.size && <span className="prs-ipucu">Sıfırlamak istediğin bölümü yukarıdan seç.</span>}
            <button type="button" className="prs-btn is-bad" onClick={() => setConfirm(true)} disabled={!picked.size}>
              {picked.size ? `Seçilenleri sıfırla (${sayi(toplam)} kayıt)` : 'Seçilenleri sıfırla'}
            </button>
          </>
        )}
      </div>
    </div>
  );
};
