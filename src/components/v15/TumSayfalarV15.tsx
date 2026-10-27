import React, { useMemo, useState } from 'react';
import { ChevronRight, Search, X } from 'lucide-react';
import { linkClick, pathFor, type AppRoute } from '../../router';
import { menuGruplari } from './navV15';

/**
 * v15 · Bütün sayfalar (telefon alt çubuğu "Menü" ve tablet rayı "Menü" aynı içeriği açar).
 * Üstte sayfa arama, altında tek sıra kompakt araçlar (tam ekran, kronometre…), sonra gruplu simge ızgarası.
 * Liste navV15.menuGruplari'den: NAV_TREE'ye eklenen her sayfa burada kendiliğinden görünür (erişilemeyen sayfa kalmaz).
 */
export interface Arac { id: string; ad: string; icon: React.ElementType; on?: boolean; rozet?: number; tikla: () => void }

const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

export function TumSayfalarV15({ active, onGo, isAdmin, araclar }: { active: AppRoute; onGo: (r: AppRoute) => void; isAdmin: boolean; araclar: Arac[] }) {
  const [q, setQ] = useState('');
  const gruplar = useMemo(() => menuGruplari(isAdmin), [isAdmin]);
  const f = fold(q.trim());
  const suzulu = f ? gruplar.map((g) => ({ ...g, items: g.items.filter((it) => fold(`${it.label} ${it.hint || ''} ${g.label}`).includes(f)) })).filter((g) => g.items.length) : gruplar;

  return (
    <div className="ts15">
      <label className="ts15-ara">
        <Search aria-hidden="true" />
        <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Sayfa ara: takvim, notlar, oyun…" aria-label="Sayfa ara" />
        {q && <button type="button" onClick={() => setQ('')} aria-label="Aramayı temizle"><X aria-hidden="true" /></button>}
      </label>

      {!f && (
        <div className="ts15-arac" role="group" aria-label="Araçlar">
          {araclar.map((a) => (
            <button key={a.id} type="button" className={a.on ? 'is-on' : ''} aria-pressed={a.on} onClick={a.tikla} title={a.ad}>
              <span className="ts15-arac-ic"><a.icon aria-hidden="true" />{a.rozet ? <i>{a.rozet}</i> : null}</span>
              <span className="ts15-arac-l">{a.ad}</span>
            </button>
          ))}
        </div>
      )}

      {suzulu.map((g) => (
        <section key={g.id} className="ts15-grup" aria-label={g.label}>
          <div className="ts15-gb">
            <h3>{g.label}</h3>
            {g.hub && !f && (
              <a href={pathFor(g.hub)} onClick={linkClick(() => onGo(g.hub!))} className="ts15-merkez">Merkez<ChevronRight aria-hidden="true" /></a>
            )}
          </div>
          <ul className="ts15-izgara" role="list">
            {g.items.map((it) => (
              <li key={it.id}>
                <a href={pathFor(it.id)} onClick={linkClick(() => onGo(it.id))} aria-current={active === it.id ? 'page' : undefined} className="ts15-oge" title={it.hint}>
                  <span className="ts15-ic"><it.icon aria-hidden="true" /></span>
                  <span className="ts15-l">{it.short && it.label.length > 16 ? it.short : it.label}</span>
                </a>
              </li>
            ))}
          </ul>
        </section>
      ))}
      {f && !suzulu.length && <p className="ts15-bos">"{q}" adında sayfa yok. Ders, soru ya da terim aramak için üstteki büyük aramayı kullan.</p>}
    </div>
  );
}
