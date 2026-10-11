import React, { useCallback, useEffect, useRef, useState } from 'react';
import { ThumbsUp, ThumbsDown, Flag, MessageSquare, NotebookPen, SquarePen, MessageCircle, Send, X, Undo2, Check, CloudOff, Wifi, WifiOff, Trash2 } from 'lucide-react';
import { Sheet } from '../ui/Sheet';
import { offlineDatabaseService, type OfflineAction } from '../../services/offlineDatabaseService';
import { useNetState } from '../../services/net';

/**
 * Gönderim kuyruğu: bağlantı yokken ya da zayıfken cihazda bekleyen işlemler (beğeni, bildirim, yorum…).
 * Her işlem ne olduğunu, ne zaman yapıldığını ve gönderim durumunu gösterir; tek tek ya da toplu iptal edilir,
 * iptal 6 sn içinde geri alınabilir. Bağlantı gelince kuyruk kendiliğinden boşalır; "Şimdi gönder" beklemeden dener.
 * Açmak için: window.dispatchEvent(new Event('medsoru:pending')) — bağlantı şeridi ve "Daha" sayfası kullanır.
 */
type Row = OfflineAction & { id: number };

interface Meta { icon: React.ElementType; tint: string; title: string; target: string }

/** Uç adresinden insanın anlayacağı ad: "Beğeni · çıkmış soru #4f2a" */
function describe(a: Row): Meta {
  const ep = a.endpoint || '';
  const m = ep.match(/\/api\/([^/]+)\/([^/?]+)(?:\/([^/?]+))?/);
  const area = m?.[1] || '';
  const id = m?.[2] ? decodeURIComponent(m[2]) : '';
  const verb = m?.[3] || '';
  const shortId = id.length > 10 ? `#${id.slice(-6)}` : id ? `#${id}` : '';
  const where =
    area === 'past-exams' ? 'Çıkmış soru' : area === 'questions' ? 'Havuz sorusu' : area === 'ornek-sorular' ? 'Örnek soru' : area === 'terms' ? 'Sözlük terimi' : area === 'learn' ? 'Öğren dersi' : 'Kayıt';
  const target = `${where} ${shortId}`.trim();
  if (verb === 'upvote') return { icon: ThumbsUp, tint: 'var(--color-accent)', title: 'Beğeni', target };
  if (verb === 'downvote') return { icon: ThumbsDown, tint: 'var(--color-ink-2)', title: 'Beğenmeme', target };
  if (verb === 'report' || a.type === 'report') return { icon: Flag, tint: 'var(--color-bad)', title: 'Hata bildirimi', target };
  if (verb === 'comments' || a.type === 'comment') return { icon: MessageSquare, tint: 'var(--color-clinic)', title: 'Yorum', target };
  if (a.type === 'note') return { icon: NotebookPen, tint: 'var(--color-warn)', title: 'Not', target };
  if (a.type === 'contribute') return { icon: SquarePen, tint: 'var(--color-brand)', title: 'Soru katkısı', target };
  if (a.type === 'feedback') return { icon: MessageCircle, tint: 'var(--color-ai)', title: 'Geri bildirim', target };
  return { icon: Send, tint: 'var(--color-ink-3)', title: 'İşlem', target };
}

const snippet = (p: any): string => {
  if (!p || typeof p !== 'object') return '';
  const t = p.reason || p.details || p.text || p.comment || p.message || p.content || '';
  return String(t).replace(/\s+/g, ' ').trim().slice(0, 120);
};

const ago = (iso: string, now: number) => {
  const s = Math.max(0, Math.round((now - Date.parse(iso)) / 1000));
  if (s < 60) return 'az önce';
  if (s < 3600) return `${Math.floor(s / 60)} dk önce`;
  if (s < 86400) return `${Math.floor(s / 3600)} sa önce`;
  return new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};

function status(a: Row, now: number, net: string): { label: string; tone: string } {
  if (net === 'offline') return { label: 'Bağlantı bekleniyor', tone: 'is-warn' };
  if (!a.attempts) return { label: 'Sırada', tone: '' };
  const wait = Math.max(0, Math.ceil(((a.nextAt || 0) - now) / 1000));
  return wait > 0 ? { label: `${a.attempts}. deneme olmadı · ${wait} sn`, tone: 'is-bad' } : { label: `${a.attempts}. deneme olmadı · sırada`, tone: 'is-bad' };
}

export const PendingOpsSheet: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [rows, setRows] = useState<Row[]>([]);
  const [leaving, setLeaving] = useState<Set<number>>(new Set());
  const [undo, setUndo] = useState<{ items: Row[]; at: number } | null>(null);
  const [sending, setSending] = useState(false);
  const [armAll, setArmAll] = useState(false);
  const [now, setNow] = useState(Date.now());
  const net = useNetState();
  const undoTimer = useRef<number | undefined>(undefined);

  const refresh = useCallback(() => {
    offlineDatabaseService.listQueue().then(setRows).catch(() => setRows([]));
  }, []);

  useEffect(() => {
    const on = () => {
      setOpen(true);
      refresh();
    };
    window.addEventListener('medsoru:pending', on);
    return () => window.removeEventListener('medsoru:pending', on);
  }, [refresh]);

  // Açıkken kuyruk değişince (gönderildi / yeni eklendi) ve saniyede bir (geri sayım) tazele
  useEffect(() => {
    if (!open) return;
    const unsub = offlineDatabaseService.subscribe(() => refresh());
    const t = window.setInterval(() => setNow(Date.now()), 1000);
    return () => {
      unsub();
      window.clearInterval(t);
    };
  }, [open, refresh]);
  useEffect(() => () => window.clearTimeout(undoTimer.current), []);
  useEffect(() => { if (!open) { setArmAll(false); setUndo(null); } }, [open]);

  const showUndo = (items: Row[]) => {
    window.clearTimeout(undoTimer.current);
    setUndo({ items, at: Date.now() });
    undoTimer.current = window.setTimeout(() => setUndo(null), 6000);
  };

  const cancelOne = async (r: Row) => {
    setLeaving((s) => new Set(s).add(r.id));
    window.setTimeout(async () => {
      await offlineDatabaseService.cancelQueued([r.id]);
      setLeaving((s) => { const n = new Set(s); n.delete(r.id); return n; });
      refresh();
      showUndo([r]);
    }, 220);
  };

  const cancelAll = async () => {
    if (!armAll) {
      setArmAll(true);
      window.setTimeout(() => setArmAll(false), 4000);
      return;
    }
    const items = rows;
    setLeaving(new Set(items.map((r) => r.id)));
    window.setTimeout(async () => {
      await offlineDatabaseService.cancelQueued();
      setLeaving(new Set());
      setArmAll(false);
      refresh();
      showUndo(items);
    }, 240);
  };

  const restore = async () => {
    if (!undo) return;
    await offlineDatabaseService.restoreQueued(undo.items);
    setUndo(null);
    refresh();
  };

  const sendNow = async () => {
    setSending(true);
    try {
      await offlineDatabaseService.syncOfflineQueue();
    } finally {
      setSending(false);
      refresh();
    }
  };

  const NetIcon = net === 'offline' ? WifiOff : net === 'slow' ? CloudOff : Wifi;
  const netText = net === 'offline' ? 'Çevrimdışı — bağlantı gelince gönderilecek' : net === 'slow' ? 'Bağlantı zayıf — denemeler sürüyor' : 'Bağlantı var — kuyruk boşaltılıyor';

  return (
    <Sheet
      open={open}
      onClose={() => setOpen(false)}
      title="Gönderim kuyruğu"
      subtitle={rows.length ? `${rows.length} işlem cihazında bekliyor` : 'Bekleyen işlem yok'}
      width={480}
      footer={
        rows.length > 0 ? (
          <div className="po-foot">
            <button type="button" className={`ui-btn ${armAll ? 'is-danger' : 'is-ghost'}`} onClick={() => void cancelAll()}>
              <Trash2 /> {armAll ? 'Emin misin? Tümünü iptal et' : 'Tümünü iptal et'}
            </button>
            <button type="button" className={`ui-btn is-primary ${sending ? 'is-loading' : ''}`} disabled={net === 'offline' || sending} onClick={() => void sendNow()}>
              <Send /> Şimdi gönder
            </button>
          </div>
        ) : undefined
      }
    >
      <div className="po">
        <div className={`po-net is-${net}`} role="status">
          <span className="po-net-ic"><NetIcon aria-hidden /></span>
          <span>{netText}</span>
        </div>

        {rows.length === 0 ? (
          <div className="po-empty">
            <span className="po-empty-ic"><Check aria-hidden /></span>
            <b>Bekleyen işlem yok</b>
            <span>Bağlantın koptuğunda yaptığın beğeni, bildirim ve yorumlar burada sıraya girer; buradan görüp iptal edebilirsin.</span>
          </div>
        ) : (
          <ul className="po-list">
            {rows.map((r) => {
              const m = describe(r);
              const st = status(r, now, net);
              const text = snippet(r.payload);
              return (
                <li key={r.id} className={`po-row ${leaving.has(r.id) ? 'is-leaving' : ''}`}>
                  <span className="po-ic" style={{ ['--po-c' as string]: m.tint }}><m.icon aria-hidden /></span>
                  <div className="po-main">
                    <b>{m.title} <span>· {m.target}</span></b>
                    {text && <p>“{text}”</p>}
                    <div className="po-meta">
                      <span className={`po-st ${st.tone}`}>{st.label}</span>
                      <span>{ago(r.timestamp, now)}</span>
                    </div>
                  </div>
                  <button type="button" className="po-x" onClick={() => void cancelOne(r)} aria-label={`${m.title} işlemini iptal et`} title="İptal et">
                    <X aria-hidden />
                  </button>
                </li>
              );
            })}
          </ul>
        )}

        <p className="ui-hint">İptal edilen işlem sunucuya gönderilmez. Ekranda gördüğün geçici değişiklik (ör. beğeni) sayfa yenilenince eski hâline döner.</p>

        {undo && (
          <div className="po-undo" role="status">
            <span>{undo.items.length > 1 ? `${undo.items.length} işlem iptal edildi` : 'İşlem iptal edildi'}</span>
            <button type="button" onClick={() => void restore()}><Undo2 aria-hidden /> Geri al</button>
            <i style={{ animationDuration: '6s' }} aria-hidden />
          </div>
        )}
      </div>
    </Sheet>
  );
};
