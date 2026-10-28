import React, { useState } from 'react';
import { SayfaBasligi, Hata, Yukleniyor, Rozet } from '../kit';
import type { SayfaProps } from '../menu';
import { NAV_TREE_HAM } from '../../shell/navModel';
import { ogrenciGorunumu } from '../../../services/siteAyar';
import { Anahtar, siteAyarYaz, useSiteAyarAdmin } from './ortak/siteAyarOrtak';

/**
 * Site › Menü: öğrencinin kenar menüsünün önizlemesi (yapı ve sıra kodda: shell/navModel NAV_TREE_HAM + siteHaritasi, kural 16).
 * Panel yalnız menüde gizler/açar (site_ayar.menu); sayfa erişimi Görünürlük sayfasındadır.
 */
export default function SiteMenu({ git }: SayfaProps) {
  const { veri: a, hata, yenile, setVeri } = useSiteAyarAdmin();
  const [mesgul, setMesgul] = useState<string | null>(null);
  if (hata && !a) return <><SayfaBasligi baslik="Menü" /><Hata hata={hata} yenile={yenile} /></>;
  if (!a) return <><SayfaBasligi baslik="Menü" /><Yukleniyor satir={6} /></>;
  return (
    <>
      <SayfaBasligi baslik="Menü" aciklama="Öğrencinin gördüğü menü. Sıra ve gruplar koddadır; buradan yalnız menüde gizlenir. Erişimi değiştirmek için Görünürlük."
        eylemler={<button type="button" className="m16-btn" onClick={() => git('site/gorunurluk')}>Görünürlük</button>} />
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 12 }}>
        {NAV_TREE_HAM.map((g, i) => (
          <section key={i} className="m16-kart">
            <h2>{g.label || 'Başlangıç'}</h2>
            <ul className="m16-liste" style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gap: 6 }}>
              {g.items.map((it) => {
                const o = ogrenciGorunumu(it.id, a);
                return (
                  <li key={it.id} style={{ display: 'flex', alignItems: 'center', gap: 8, opacity: o.menude ? 1 : 0.5 }}>
                    <span style={{ flex: 1, minWidth: 0, textDecoration: o.menude ? undefined : 'line-through' }}>{it.label}</span>
                    {o.erisim !== 'acik' && <Rozet ton="uyari">{o.erisim === 'bayrak' ? 'bayrak' : o.erisim}</Rozet>}
                    <Anahtar acik={a.menu[it.id] !== false} mesgul={mesgul === it.id} etiket={`${it.label} menüde`}
                      degistir={async (v) => { setMesgul(it.id); const r = await siteAyarYaz({ menu: { [it.id]: v ? null : false } }, `${it.label}: menüde ${v ? 'görünür' : 'gizli'}`); if (r) setVeri(r as any); setMesgul(null); }} />
                  </li>
                );
              })}
            </ul>
          </section>
        ))}
      </div>
    </>
  );
}
