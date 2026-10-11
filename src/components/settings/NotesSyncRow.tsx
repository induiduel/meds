import React, { useEffect, useState } from 'react';
import { Copy, RefreshCw, CloudUpload, Check } from 'lucide-react';
import { getSyncCode, lastSyncedAt, setSyncCode, syncNotes } from '../../services/notesSync';
import { toast } from '../ui/Toast';

/**
 * Ayarlar · Not eşitleme: notlar sunucuya yedeklenir; aynı kodu başka cihaza girince iki cihaz aynı
 * not defterini kullanır. Kod gizli bir anahtardır — yalnız kendi cihazlarında kullan.
 */
export const NotesSyncRow: React.FC = () => {
  const [code, setCode] = useState(getSyncCode);
  const [other, setOther] = useState('');
  const [busy, setBusy] = useState(false);
  const [at, setAt] = useState(lastSyncedAt);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const on = () => setAt(lastSyncedAt());
    window.addEventListener('medsoru:notes-synced', on);
    return () => window.removeEventListener('medsoru:notes-synced', on);
  }, []);

  const now = async () => {
    setBusy(true);
    const ok = await syncNotes();
    setBusy(false);
    if (ok) toast.success('Notlar eşitlendi');
    else toast.error('Eşitlenemedi', 'Bağlantıyı kontrol edip yeniden deneyin.');
  };
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1500);
    } catch {
      toast.error('Kopyalanamadı');
    }
  };
  const join = () => {
    try {
      setSyncCode(other);
      setCode(getSyncCode());
      setOther('');
      toast.success('Kod kaydedildi', 'Bu cihazın notları o defterle birleştiriliyor.');
    } catch (e: any) {
      toast.error('Kod geçersiz', e.message);
    }
  };

  return (
    <div className="ui-row has-icon ui-row-stack">
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, minWidth: 0 }}>
        <span className="ui-ico" style={{ '--ico-bg': 'var(--color-clinic)', '--ico-fg': 'var(--color-on-solid)' } as React.CSSProperties}>
          <CloudUpload strokeWidth={2.1} />
        </span>
        <span className="ui-row-main">
          <b>Not eşitleme</b>
          <span>{at ? `Son yedek: ${new Date(at).toLocaleString('tr-TR', { dateStyle: 'short', timeStyle: 'short' })}` : 'Notların sunucuya yedeklenir'}</span>
        </span>
        <button type="button" className={`ui-btn is-sm is-tonal ${busy ? 'is-loading' : ''}`} onClick={() => void now()} disabled={busy}>
          <RefreshCw /> Şimdi
        </button>
      </div>
      <div className="ui-field">
        <label htmlFor="ns-code">Bu cihazın kodu (başka cihaza gir)</label>
        <div style={{ display: 'flex', gap: 6 }}>
          <input id="ns-code" className="ui-input" readOnly value={code} onFocus={(e) => e.currentTarget.select()} style={{ fontFamily: 'var(--font-mono)', fontSize: 12.5 }} />
          <button type="button" className="ui-btn is-sm" onClick={() => void copy()} aria-label="Kodu kopyala">{copied ? <Check /> : <Copy />}</button>
        </div>
      </div>
      <form className="ui-field" onSubmit={(e) => { e.preventDefault(); join(); }}>
        <label htmlFor="ns-other">Başka cihazın kodunu kullan</label>
        <div style={{ display: 'flex', gap: 6 }}>
          <input id="ns-other" className="ui-input" value={other} onChange={(e) => setOther(e.target.value)} placeholder="dev-…" autoComplete="off" />
          <button type="submit" className="ui-btn is-sm is-primary" disabled={other.trim().length < 12}>Bağla</button>
        </div>
        <span className="ui-hint">Kod bir anahtardır: yalnız kendi cihazlarında kullan, kimseyle paylaşma.</span>
      </form>
    </div>
  );
};
