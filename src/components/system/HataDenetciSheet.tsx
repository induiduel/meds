import React, { useEffect, useState } from 'react';
import { AlertTriangle, CheckCircle2, Info, XCircle, RefreshCw, Wrench, Copy, X, ShieldCheck } from 'lucide-react';
import { Sheet } from '../ui/Sheet';
import { toast } from '../ui/Toast';
import {
  acikSorunlar, sorunlar, denetle, onar, sorunuKapat, gecmisiTemizle, denetciDinle, sonDenetimZamani, type Sorun,
} from '../../services/hataDenetci';

/**
 * Sorun denetçisi paneli: bağlantı ve eşitleme sorunlarını sade dille, ne yapıldığıyla birlikte gösterir.
 * Açmak için: window.dispatchEvent(new Event('medsoru:denetci')) — bağlantı şeridi, eşitleme kartı ve toast'lar kullanır.
 */
const ago = (t: number) => {
  const s = Math.max(0, Math.round((Date.now() - t) / 1000));
  if (s < 60) return 'az önce';
  if (s < 3600) return `${Math.floor(s / 60)} dk önce`;
  if (s < 86400) return `${Math.floor(s / 3600)} sa önce`;
  return new Date(t).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};

const IKON = { hata: XCircle, uyari: AlertTriangle, bilgi: Info } as const;

const Satir: React.FC<{ s: Sorun; busy: boolean; onOnar: () => void }> = ({ s, busy, onOnar }) => {
  const [acik, setAcik] = useState(false);
  const Ic = s.cozuldu ? CheckCircle2 : IKON[s.ciddiyet];
  const kopyala = () => {
    const metin = `${s.baslik}\n${s.aciklama}\n${s.teknik || ''}\n${new Date(s.son).toISOString()} · ${navigator.userAgent}`;
    void navigator.clipboard?.writeText(metin).then(() => toast.success('Kopyalandı', 'Destek için yapıştırabilirsin.'));
  };
  return (
    <li className={`hd-row is-${s.cozuldu ? 'ok' : s.ciddiyet}`}>
      <span className="hd-ic"><Ic aria-hidden /></span>
      <div className="hd-main">
        <b>{s.baslik}</b>
        {!s.cozuldu && <p>{s.aciklama}</p>}
        {!s.cozuldu && <p className="hd-cozum"><Wrench aria-hidden /> {s.cozum}</p>}
        {s.onarim && (
          <p className={`hd-onarim ${s.onarim.ok ? 'is-ok' : 'is-bad'}`}>{s.onarim.ok ? '✓ ' : ''}{s.onarim.not}</p>
        )}
        <div className="hd-meta">
          <span>{s.cozuldu ? `Çözüldü · ${ago(s.cozuldu)}` : `İlk ${ago(s.ilk)}`}</span>
          {s.teknik && <button type="button" onClick={() => setAcik((v) => !v)}>{acik ? 'Ayrıntıyı gizle' : 'Teknik ayrıntı'}</button>}
          {s.teknik && <button type="button" onClick={kopyala} aria-label="Ayrıntıyı kopyala"><Copy aria-hidden /></button>}
        </div>
        {acik && s.teknik && <pre className="hd-teknik">{s.teknik}</pre>}
      </div>
      {!s.cozuldu && (
        <div className="hd-act">
          {s.onarilabilir && (
            <button type="button" className={`ui-btn is-primary is-sm ${busy ? 'is-loading' : ''}`} disabled={busy} onClick={onOnar}>
              {s.tur === 'dusen' ? 'Yeniden dene' : 'Onar'}
            </button>
          )}
          {(s.tur === 'dusen' || s.ciddiyet === 'bilgi') && (
            <button type="button" className="po-x" onClick={() => sorunuKapat(s.id)} aria-label="Kapat" title="Kapat"><X aria-hidden /></button>
          )}
        </div>
      )}
    </li>
  );
};

export const HataDenetciSheet: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [, tick] = useState(0);
  const [busy, setBusy] = useState<string>('');

  useEffect(() => denetciDinle(() => tick((n) => n + 1)), []);
  useEffect(() => {
    const on = () => { setOpen(true); void denetle(false); };
    window.addEventListener('medsoru:denetci', on);
    return () => window.removeEventListener('medsoru:denetci', on);
  }, []);

  const calistir = async (id: string, fn: () => Promise<void>) => {
    setBusy(id);
    try { await fn(); } finally { setBusy(''); }
  };

  const acik = acikSorunlar();
  const gecmis = sorunlar().filter((s) => s.cozuldu);
  const son = sonDenetimZamani();

  return (
    <Sheet
      open={open}
      onClose={() => setOpen(false)}
      title="Sorun denetçisi"
      subtitle={acik.length ? `${acik.length} açık sorun` : 'Her şey yolunda'}
      width={500}
      footer={
        <div className="po-foot">
          {gecmis.length > 0 ? <button type="button" className="ui-btn is-ghost" onClick={gecmisiTemizle}>Geçmişi temizle</button> : <span />}
          <button type="button" className={`ui-btn is-primary ${busy === '*' ? 'is-loading' : ''}`} disabled={!!busy} onClick={() => void calistir('*', () => denetle(true))}>
            <RefreshCw /> Denetle ve onar
          </button>
        </div>
      }
    >
      <div className="po">
        {acik.length === 0 ? (
          <div className="po-empty">
            <span className="po-empty-ic"><ShieldCheck aria-hidden /></span>
            <b>Sorun bulunamadı</b>
            <span>Bağlantın, cihaz belleğin ve eşitlemen düzgün çalışıyor. Denetçi arka planda düzenli kontrol eder; bir şey olursa sana haber verir ve onarabildiğini kendisi onarır.</span>
          </div>
        ) : (
          <ul className="hd-list">
            {acik.map((s) => <Satir key={s.id + s.ilk} s={s} busy={busy === s.id} onOnar={() => void calistir(s.id, () => onar(s.id))} />)}
          </ul>
        )}
        {gecmis.length > 0 && (
          <>
            <h3 className="hd-h">Çözülenler</h3>
            <ul className="hd-list is-gecmis">
              {gecmis.slice(0, 12).map((s) => <Satir key={s.id + s.ilk} s={s} busy={false} onOnar={() => {}} />)}
            </ul>
          </>
        )}
        <p className="ui-hint">{son ? `Son denetim ${ago(son)}.` : 'Denetim sürüyor…'} Kayıtlar yalnız bu cihazda tutulur.</p>
      </div>
    </Sheet>
  );
};
