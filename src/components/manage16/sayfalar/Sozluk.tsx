import React, { useState } from 'react';
import { KatalogSayfasi } from '../kit';
import type { SayfaProps } from '../menu';

const TURLER = [
  { id: 'glossary', etiket: 'Sözlük' },
  { id: 'kisaltma', etiket: 'Kısaltmalar' },
  { id: 'terim', etiket: 'Terim yardımcısı' },
];

/** Kaynaklar › Sözlük: tıbbi sözlük + kısaltma + terim yardımcısı (üç sekme, her biri sunucu sayfalı). */
export default function Sozluk(_p: SayfaProps) {
  const [tur, setTur] = useState(() => new URLSearchParams(location.search).get('tur') || 'glossary');
  const sec = (t: string) => {
    const u = new URL(location.href);
    for (const k of [...u.searchParams.keys()]) u.searchParams.delete(k);
    if (t !== 'glossary') u.searchParams.set('tur', t);
    history.replaceState(history.state, '', u);
    setTur(t);
  };
  const t = TURLER.find((x) => x.id === tur) || TURLER[0];
  return (
    <KatalogSayfasi key={t.id} varlik={t.id} kimlik={`kaynak-sozluk-${t.id}`} baslik={t.etiket} silinebilir={t.id === 'glossary'}
      /* H267: silinemeyen sekmede nedeni söylenir */
      aciklama={t.id === 'glossary' ? undefined : 'Bu sekmedeki kayıtlar yalnız düzenlenir; silme ve çöp kutusu yalnız Sözlük sekmesinde açıktır.'}
      ust={<div className="m16-sekmeler" role="tablist">{TURLER.map((x) => <button key={x.id} type="button" role="tab" aria-selected={x.id === t.id} className={x.id === t.id ? 'on' : ''} onClick={() => sec(x.id)}>{x.etiket}</button>)}</div>} />
  );
}
