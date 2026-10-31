/**
 * Sürüm notunun ortak gösterimi: açılış penceresi (UpdatePrompt) ve /guncellemeler sayfası aynı bileşeni kullanır.
 * Veri guncelleme_notu.json → "yenilikler": [{ ad, nerede: { ad, yol }, amac, islevler[], ipucu? }].
 * Yenilik kartı yoksa "maddeler" listesine düşülür; "Başlık: açıklama" biçimindeki madde kalın başlıkla gösterilir.
 */
import React from 'react';
import { ArrowUpRight, CalendarDays, Lightbulb, MapPin, Target } from 'lucide-react';

export type Yenilik = { ad: string; nerede?: { ad?: string; yol?: string }; amac?: string; islevler?: string[]; ipucu?: string };

/** "Başlık: açıklama" → kalın başlık + metin */
export function Madde({ m }: { m: string }) {
  const i = m.indexOf(':');
  if (i > 2 && i < 48 && !/https?$/.test(m.slice(0, i))) {
    return <><b>{m.slice(0, i)}</b>{m.slice(i)}</>;
  }
  return <>{m}</>;
}

export const tarihYaz = (iso?: string) => (iso ? new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }) : '');

export function YenilikKarti({ y, tarih, onGit }: { y: Yenilik; tarih?: string; onGit?: () => void }) {
  const islevler = (y.islevler || []).filter(Boolean);
  return (
    <article className="sn-kart">
      <h4 className="sn-ad">{y.ad}</h4>
      <div className="sn-meta">
        {y.nerede?.ad && (
          <span><MapPin aria-hidden />
            {y.nerede.yol ? <a href={y.nerede.yol} onClick={onGit}>{y.nerede.ad}<ArrowUpRight aria-hidden /></a> : y.nerede.ad}
          </span>
        )}
        {tarih && <span><CalendarDays aria-hidden />{tarihYaz(tarih)}</span>}
      </div>
      {y.amac && <p className="sn-amac"><Target aria-hidden /><span><b>Amacı: </b>{y.amac}</span></p>}
      {islevler.length > 0 && (
        <ul className="sn-islev" aria-label="Neler yapabilirsin">
          {islevler.map((m, i) => <li key={i}><Madde m={m} /></li>)}
        </ul>
      )}
      {y.ipucu && <p className="sn-ipucu"><Lightbulb aria-hidden /><span>{y.ipucu}</span></p>}
    </article>
  );
}
