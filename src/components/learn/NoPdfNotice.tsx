/**
 * Ders PDF'i Drive'da olmayan (içerikle doğrulanmış eşleşmesi bulunmayan) deste açılırken çıkan uyarı.
 * Kapı InteractiveDeckView'da: PDF bilgisi gelene kadar iskelet, PDF yoksa önce bu pencere, sonra ders.
 * Aynı oturumda onaylanan deste yeniden sorulmaz; "bir daha gösterme" deste başına kalıcıdır.
 * PDF sonradan Drive'a gelince (dosya listesi dolunca) uyarı kendiliğinden kalkar.
 */
import React, { useEffect, useState } from 'react';
import { CalendarClock, FileX, Info } from 'lucide-react';
import { Dialog } from '../ui/Dialog';
import { resolveDeckPdf } from '../../services/deckPdfService';

const MUTE_KEY = 'medsoru_learn_nopdf_mute';
const sessionAck = new Set<string>();

const readMuted = (): string[] => {
  try {
    const v = JSON.parse(localStorage.getItem(MUTE_KEY) || '[]');
    return Array.isArray(v) ? v : [];
  } catch {
    return [];
  }
};
const isMuted = (id: string) => sessionAck.has(id) || readMuted().includes(id);

/** PDF bilgisi bu süreyi aşarsa ders uyarısız açılır (yavaş ağda kullanıcı bekletilmez). */
const CHECK_TIMEOUT_MS = 2500;

export type NoPdfGate =
  | { id: string; state: 'checking' }
  | { id: string; state: 'warn'; date?: string }
  | { id: string; state: 'ok' };

/** Açılan destenin PDF kapısı: checking → (warn) → ok. */
export function useNoPdfGate(deckId: string | null): [NoPdfGate | null, (mute: boolean) => void] {
  const [gate, setGate] = useState<NoPdfGate | null>(null);
  useEffect(() => {
    if (!deckId) {
      setGate(null);
      return;
    }
    if (isMuted(deckId)) {
      setGate({ id: deckId, state: 'ok' });
      return;
    }
    let live = true;
    setGate({ id: deckId, state: 'checking' });
    const settle = (next: NoPdfGate) => setGate((g) => (live && g?.id === deckId && g.state === 'checking' ? next : g));
    const t = window.setTimeout(() => settle({ id: deckId, state: 'ok' }), CHECK_TIMEOUT_MS);
    resolveDeckPdf(deckId)
      .then((info) => settle(info.files.length ? { id: deckId, state: 'ok' } : { id: deckId, state: 'warn', date: info.missingDate }))
      .catch(() => settle({ id: deckId, state: 'ok' }))
      .finally(() => window.clearTimeout(t));
    return () => {
      live = false;
      window.clearTimeout(t);
    };
  }, [deckId]);

  const accept = (mute: boolean) => {
    if (!deckId) return;
    sessionAck.add(deckId);
    if (mute) {
      try {
        localStorage.setItem(MUTE_KEY, JSON.stringify([...new Set([...readMuted(), deckId])]));
      } catch {
        /* depolama kapalı: yalnız bu oturum */
      }
    }
    setGate({ id: deckId, state: 'ok' });
  };
  return [gate, accept];
}

export const NoPdfNotice: React.FC<{
  title: string;
  date?: string;
  onContinue: (mute: boolean) => void;
  onBack: () => void;
}> = ({ title, date, onContinue, onBack }) => {
  const [mute, setMute] = useState(false);
  const when = date ? new Date(`${date}T12:00:00`) : null;
  const today = !!when && when.toDateString() === new Date().toDateString();
  const upcoming = when ? today || when.getTime() > Date.now() : false;
  const dateTxt = when ? when.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', weekday: 'long' }) : '';

  return (
    <Dialog
      title={
        <span className="flex items-center gap-2">
          <FileX aria-hidden className="w-5 h-5 shrink-0" style={{ color: 'var(--color-warn)' }} />
          Bu dersin PDF'i bulunamadı
        </span>
      }
      subtitle={title}
      onClose={onBack}
      width="max-w-lg"
      footer={
        <>
          <label className="mr-auto flex items-center gap-2 text-sm text-ink-2 cursor-pointer select-none">
            <input type="checkbox" checked={mute} onChange={(e) => setMute(e.target.checked)} />
            Bu ders için bir daha gösterme
          </label>
          <button type="button" className="ms-btn is-ghost" onClick={onBack}>
            Kitaplığa dön
          </button>
          <button type="button" className="ms-btn is-primary" onClick={() => onContinue(mute)}>
            Derse devam et
          </button>
        </>
      }
    >
      <p className="m-0 text-[15px] leading-relaxed text-ink">
        Bu dersin 2026-27 slaytı Drive'da yok. Etkileşimli içerik önceki yılın kaynağından hazırlandı; bu yılki slaytla birebir aynı olmayabilir.
      </p>
      {when && (
        <div className="ui-callout is-warn">
          <CalendarClock aria-hidden />
          <span>
            {upcoming
              ? `Ders ${today ? `bugün (${dateTxt})` : `${dateTxt} günü`}. Hoca slaytı Drive'a yükleyince PDF burada kendiliğinden açılır.`
              : `Ders ${dateTxt} günü işlendi ama slaytı Drive'a henüz yüklenmedi. Yüklendiğinde PDF burada kendiliğinden açılır.`}
          </span>
        </div>
      )}
      <ul className="m-0 pl-5 flex flex-col gap-1.5 text-sm text-ink-2 list-disc">
        <li>PDF görünümü ve yan yana okuma bu derste çalışmaz.</li>
        <li>Adımların slayt sayfası karşılığı gösterilmez.</li>
        <li>Elinde slayt varsa ders içindeki PDF görünümünden kendi dosyanı açabilirsin.</li>
      </ul>
      <div className="ui-callout">
        <Info aria-hidden />
        <span>Sınava hazırlanırken içeriği hocanın bu yılki slaytıyla karşılaştırmanı öneririz.</span>
      </div>
    </Dialog>
  );
};
