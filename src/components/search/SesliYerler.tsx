/**
 * Sesli derste geçen yerler (tasarım A05): aranan terim sesli ders metinlerinde geçiyorsa ders + cümle parçası +
 * zaman damgası. Veri sunucudan (GET /api/canli-ders/ara, bellek içi dizin); tıklayınca ders o saniyede açılır (?p=&t=).
 */
import React, { useEffect, useState } from 'react';
import { Headphones } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { dkSn } from '../../services/dersKonum';
import { navigateTo, pathFor } from '../../router';
import { Highlight } from './searchShared';
// H149: bu satır yorum bloğunun içine düşmüştü; stil hiç yüklenmiyor, ders adı + parça + zaman bitişik görünüyordu
import '../../styles/sesli-yer.css';

export interface SesliYer { k: string; b: string; p: number; c: number; t: number | null; parca: string }
const onbellek = new Map<string, SesliYer[]>();

export function useSesliYerler(q: string, n = 8): SesliYer[] {
  const query = q.trim();
  const [liste, setListe] = useState<SesliYer[]>(() => onbellek.get(`${n}|${query}`) || []);
  useEffect(() => {
    const anahtar = `${n}|${query}`;
    if (query.length < 3) { setListe([]); return; }
    if (onbellek.has(anahtar)) { setListe(onbellek.get(anahtar)!); return; }
    let canli = true;
    const t = window.setTimeout(() => {
      safeJsonFetch<{ sonuc: SesliYer[] }>(`/api/canli-ders/ara?q=${encodeURIComponent(query)}&n=${n}`)
        .then((r) => { const s = r.ok && Array.isArray(r.data?.sonuc) ? r.data!.sonuc : []; onbellek.set(anahtar, s); if (canli) setListe(s); })
        .catch(() => canli && setListe([]));
    }, 220);
    return () => { canli = false; window.clearTimeout(t); };
  }, [query, n]);
  return liste;
}

export const sesliYerAdresi = (y: SesliYer) => `${pathFor('canli_ders', y.k)}?p=${y.p}${y.t != null ? `&t=${y.t}` : ''}`;

export const SesliYerler: React.FC<{ query: string; n?: number; onGo?: () => void; className?: string }> = ({ query, n = 8, onGo, className }) => {
  const liste = useSesliYerler(query, n);
  if (!liste.length) return null;
  return (
    <section className={`ms-sesli-yer ${className || ''}`} aria-label="Sesli derste geçen yerler">
      <h3 className="s12-pal-gh ms-sesli-yer-bas"><Headphones aria-hidden className="ms-sesli-yer-ico" /> Sesli derste geçen yerler</h3>
      <ul className="m-0 p-0 list-none">
        {liste.map((y) => (
          <li key={`${y.k}-${y.p}-${y.c}`}>
            <a className="ms-sesli-yer-a" href={sesliYerAdresi(y)}
              onClick={(e) => { if (e.metaKey || e.ctrlKey || e.button) return; e.preventDefault(); onGo?.(); navigateTo(sesliYerAdresi(y)); }}>
              <span className="ms-sesli-yer-t">
                <span className="ms-sesli-yer-ders">{y.b}</span>
                <span className="ms-sesli-yer-parca"><Highlight text={y.parca} query={query} /></span>
              </span>
              {y.t != null && <span className="ms-sesli-yer-zaman">{dkSn(y.t)}</span>}
            </a>
          </li>
        ))}
      </ul>
    </section>
  );
};
