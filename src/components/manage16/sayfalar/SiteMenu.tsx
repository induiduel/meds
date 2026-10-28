import React, { useState } from 'react';
import { SayfaBasligi, Hata, Yukleniyor, Rozet, onayIste, bildir, yazimHedefi } from '../kit';
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
  // H185: menü yazımı Görünürlük sayfasındaki gibi: gizleme onay ister (hedef sunucu yazılı), her yazımda 8 sn "Geri al"
  const yaz = async (id: string, ad: string, v: boolean) => {
    if (!v && !(await onayIste({ baslik: `${ad} menüden gizlensin mi?`, aciklama: `Değişiklik ${yazimHedefi()} üzerinde hemen uygulanır; sayfa menüde görünmez ama adresi açık kalır. 8 saniye içinde geri alabilirsin.`, onayMetni: 'Gizle' }))) return;
    setMesgul(id);
    const once = a?.menu[id] === false ? false : null;
    const r = await siteAyarYaz({ menu: { [id]: v ? null : false } });
    if (r) {
      setVeri(r as any);
      bildir(`${ad}: menüde ${v ? 'görünür' : 'gizli'}`, 'iyi', { etiket: 'Geri al', yap: () => { void siteAyarYaz({ menu: { [id]: once } }, 'Geri alındı').then((g) => { if (g) setVeri(g as any); }); } });
    }
    setMesgul(null);
  };
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
                // H185: erişimi kapalı sayfada menü anahtarı açık görünüp üstü çiziliyordu (menude erişime de bağlı). Artık anahtar
                // kilitli + kapalı gösterilir ve nedeni yazılır; üstü çizili yalnız menüden gizlenen sayfada
                const erisimKapali = o.erisim !== 'acik';
                const ERISIM: Record<string, string> = { gizli: 'Erişim gizli', kapali: 'Erişim kapalı', 'yalniz-yonetici': 'Yalnız yönetici', bayrak: 'Özellik bayrağı kapalı' };
                return (
                  <li key={it.id} style={{ display: 'flex', alignItems: 'center', gap: 8, opacity: o.menude ? 1 : 0.55 }}>
                    <span style={{ flex: 1, minWidth: 0, textDecoration: !erisimKapali && !o.menude ? 'line-through' : undefined }}>
                      {it.label}
                      {erisimKapali && <small style={{ display: 'block', color: 'var(--color-ink-3)' }}>Menüde görünmez; açmak için Görünürlük</small>}
                    </span>
                    {erisimKapali && <Rozet ton="uyari">{ERISIM[o.erisim] || o.erisim}</Rozet>}
                    <Anahtar acik={!erisimKapali && a.menu[it.id] !== false} devreDisi={erisimKapali} mesgul={mesgul === it.id}
                      etiket={erisimKapali ? `${it.label}: ${ERISIM[o.erisim] || o.erisim}; menü ayarı Görünürlük'ten erişim açılınca geçerli olur` : `${it.label} menüde`}
                      degistir={(v) => void yaz(it.id, it.label, v)} />
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
