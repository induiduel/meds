import React, { useEffect, useRef, useState } from 'react';
import { X } from 'lucide-react';
import { JsonGoruntuleyici } from './JsonGoruntuleyici';
import { DegisiklikGecmisi } from './DegisiklikGecmisi';
import { onayIste } from './Onay';

export type CekmeceSekme = { id: string; etiket: string; icerik: React.ReactNode };

/**
 * Sağdan açılan ayrıntı çekmecesi. Varsayılan sekmeler: Alanlar (children) / JSON (kayit) / Geçmiş (hedef).
 * ekSekmeler ile ek sekme; kirli=true ise kapatırken onay sorulur. Esc kapatır.
 */
export const AyrintiCekmecesi: React.FC<{
  acik: boolean;
  kapat: () => void;
  baslik: React.ReactNode;
  altBaslik?: React.ReactNode;
  kayit?: unknown;
  /** Denetim geçmişi hedefi (ör. 'site-ayar', 'kisi:<uid>') */
  hedef?: string;
  ekSekmeler?: CekmeceSekme[];
  eylemler?: React.ReactNode;
  kirli?: boolean;
  genis?: boolean;
  children?: React.ReactNode;
}> = (p) => {
  const [sekme, setSekme] = useState('alanlar');
  const ref = useRef<HTMLElement>(null);
  const sekmeler: CekmeceSekme[] = [
    ...(p.children ? [{ id: 'alanlar', etiket: 'Alanlar', icerik: p.children }] : []),
    ...(p.ekSekmeler || []),
    ...(p.kayit !== undefined ? [{ id: 'json', etiket: 'JSON', icerik: <JsonGoruntuleyici veri={p.kayit} enYuksek={9999} /> }] : []),
    ...(p.hedef ? [{ id: 'gecmis', etiket: 'Geçmiş', icerik: <DegisiklikGecmisi hedef={p.hedef} /> }] : []),
  ];
  const etkin = sekmeler.find((s) => s.id === sekme) || sekmeler[0];

  const kapat = async () => {
    if (p.kirli && !(await onayIste({ baslik: 'Kaydedilmemiş değişiklikler silinsin mi?', onayMetni: 'Kapat', tehlikeli: true }))) return;
    p.kapat();
  };

  useEffect(() => {
    if (!p.acik) return;
    const once = document.activeElement as HTMLElement | null;
    setTimeout(() => ref.current?.focus(), 0);
    const tus = (e: KeyboardEvent) => { if (e.key === 'Escape' && !document.querySelector('.m16-onay')) void kapat(); };
    document.addEventListener('keydown', tus);
    return () => { document.removeEventListener('keydown', tus); once?.focus?.(); };
  }, [p.acik]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!p.acik) return null;
  return (
    <>
      <div className="m16-cekmece-perde" onClick={() => void kapat()} aria-hidden="true" />
      <aside ref={ref} tabIndex={-1} className={`m16-cekmece ${p.genis ? 'genis' : ''}`} role="dialog" aria-modal="true" aria-label={typeof p.baslik === 'string' ? p.baslik : 'Ayrıntı'}>
        <header className="m16-cekmece-bas">
          <div>
            <h2>{p.baslik}</h2>
            {p.altBaslik && <p>{p.altBaslik}</p>}
          </div>
          <button type="button" className="m16-btn hayalet ikon" onClick={() => void kapat()} aria-label="Kapat"><X aria-hidden="true" /></button>
        </header>
        {sekmeler.length > 1 && (
          <div className="m16-sekmeler" role="tablist">
            {sekmeler.map((s) => (
              <button key={s.id} type="button" role="tab" aria-selected={etkin?.id === s.id} className={etkin?.id === s.id ? 'on' : ''} onClick={() => setSekme(s.id)}>{s.etiket}</button>
            ))}
          </div>
        )}
        <div className="m16-cekmece-govde" role="tabpanel">{etkin?.icerik}</div>
        {p.eylemler && <footer className="m16-cekmece-alt">{p.eylemler}</footer>}
      </aside>
    </>
  );
};
