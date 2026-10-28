import React, { useMemo, useState } from 'react';
import { useSiteAyar } from '../../services/siteAyar';
import { ChevronRight, Search, X } from 'lucide-react';
import { linkClick, pathFor, type AppRoute } from '../../router';
import { aktifKurul, sinavaKalanGun } from '../../services/kurulTakvimi';
import { NAV_ITEMS, type NavItem } from '../shell/navModel';
import { menuGruplari } from './navV15';
import { sonSayfalar } from './gezinme';

/**
 * v15 · Bütün sayfalar (telefon alt çubuğu "Menü" ve tablet rayı "Menü" aynı içeriği açar). Uygulama arşivi düzeni:
 *  1 sayfa arama · 2 kurul kartı (sınava kalan gün → sınav planı) · 3 kompakt araç sırası (tam ekran, kronometre…)
 *  · 4 "Son açtıkların" (yatay) · 5 grup kartları, her biri renkli simge ızgarası.
 * Liste navV15.menuGruplari'den: NAV_TREE'ye eklenen her sayfa burada kendiliğinden görünür (erişilemeyen sayfa kalmaz).
 * Simge rengi sayfanın kimlik tonu (navModel tint); zemin palet yüzeyiyle karıştırılır, metin hep palet mürekkebi.
 */
export interface Arac { id: string; ad: string; icon: React.ElementType; on?: boolean; rozet?: number; tikla: () => void }

const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
const ad = (it: NavItem) => (it.short && it.label.length > 16 ? it.short : it.label);

export function TumSayfalarV15({ active, onGo, isAdmin, araclar }: { active: AppRoute; onGo: (r: AppRoute) => void; isAdmin: boolean; araclar: Arac[] }) {
  const [q, setQ] = useState('');
  // Site ayarı değişince menü yeniden süzülür (services/siteAyar)
  const siteAyarSurum = useSiteAyar();
  const gruplar = useMemo(() => menuGruplari(isAdmin), [isAdmin, siteAyarSurum]);
  const son = useMemo(() => sonSayfalar().map((r) => NAV_ITEMS[r]).filter((x): x is NavItem => !!x).slice(0, 6), []);
  const k = aktifKurul();
  const kalan = sinavaKalanGun();
  const f = fold(q.trim());
  const suzulu = f ? gruplar.map((g) => ({ ...g, items: g.items.filter((it) => fold(`${it.label} ${it.hint || ''} ${g.label}`).includes(f)) })).filter((g) => g.items.length) : gruplar;

  const oge = (it: NavItem, cls = 'ts15-oge') => (
    <a href={pathFor(it.id)} onClick={linkClick(() => onGo(it.id))} aria-current={active === it.id ? 'page' : undefined} className={cls} title={it.hint}
      style={{ '--t': it.tint || 'var(--color-accent)' } as React.CSSProperties}>
      <span className="ts15-ic"><it.icon aria-hidden="true" /></span>
      <span className="ts15-l">{ad(it)}</span>
    </a>
  );

  return (
    <div className="ts15">
      <label className="ts15-ara">
        <Search aria-hidden="true" />
        <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Sayfa ara: takvim, notlar, oyun…" aria-label="Sayfa ara" />
        {q && <button type="button" onClick={() => setQ('')} aria-label="Aramayı temizle"><X aria-hidden="true" /></button>}
      </label>

      {!f && (
        <>
          <a className="ts15-kurul" href={pathFor('sinav_plani')} onClick={linkClick(() => onGo('sinav_plani'))}>
            <span className="ts15-kurul-n"><b>{kalan != null && kalan >= 0 ? kalan : '—'}</b><small>gün</small></span>
            <span className="ts15-kurul-t"><b>Kurul {k.kurul} sınavına</b><span>Sınav planını aç</span></span>
            <ChevronRight aria-hidden="true" />
          </a>

          <div className="ts15-arac" role="group" aria-label="Araçlar">
            {araclar.map((a) => (
              <button key={a.id} type="button" className={a.on ? 'is-on' : ''} aria-pressed={a.on} onClick={a.tikla} title={a.ad}>
                <span className="ts15-arac-ic"><a.icon aria-hidden="true" />{a.rozet ? <i>{a.rozet}</i> : null}</span>
                <span className="ts15-arac-l">{a.ad}</span>
              </button>
            ))}
          </div>

          {son.length > 0 && (
            <section className="ts15-son" aria-label="Son açtıkların">
              <h3 className="ts15-h">Son açtıkların</h3>
              <ul role="list">{son.map((it) => <li key={it.id}>{oge(it, 'ts15-oge is-son')}</li>)}</ul>
            </section>
          )}
        </>
      )}

      {suzulu.map((g) => (
        <section key={g.id} className="ts15-grup" aria-label={g.label}>
          <div className="ts15-gb">
            <span className="ts15-gi"><g.icon aria-hidden="true" /></span>
            <span className="ts15-gt"><h3 className="ts15-h">{g.label}</h3>{!f && g.alt && <span className="ts15-galt">{g.alt}</span>}</span>
            {g.hub && !f && <a href={pathFor(g.hub)} onClick={linkClick(() => onGo(g.hub!))} className="ts15-merkez">Merkez<ChevronRight aria-hidden="true" /></a>}
          </div>
          <ul className="ts15-izgara" role="list">{g.items.map((it) => <li key={it.id}>{oge(it)}</li>)}</ul>
        </section>
      ))}
      {f && !suzulu.length && <p className="ts15-bos">"{q}" adında sayfa yok. Ders, soru ya da terim aramak için araçlardaki Ara'yı kullan.</p>}
    </div>
  );
}
