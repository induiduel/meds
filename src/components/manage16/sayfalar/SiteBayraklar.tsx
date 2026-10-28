import React, { useState } from 'react';
import { SayfaBasligi, Hata, Yukleniyor, Rozet, useAdminSorgu } from '../kit';
import type { SayfaProps } from '../menu';
import { Anahtar, siteAyarYaz } from './ortak/siteAyarOrtak';

/**
 * Site › Özellik bayrakları: tek şema (sunucu yonetim16/siteAyar.ts BAYRAKLAR + BAYRAK_UC kapısı, istemci services/siteAyar BAYRAK_SAYFA).
 * Bayrak ayarlı değilse AÇIK sayılır. Kapatınca sunucu ilgili uçları öğrenciye 403 ile kapatır, sayfası menüden kalkar.
 * Oyun modu ve oyun kaynağı bayrakları Oyunlar grubundadır.
 */
type Bayrak = { ad: string; etiket: string; aciklama: string; acik: boolean; ayarli: boolean };

export default function SiteBayraklar({ git }: SayfaProps) {
  const { veri, hata, yenile, setVeri } = useAdminSorgu<{ ogeler: Bayrak[] }>('/api/admin/site-ayar/bayraklar', { canliOlay: ['site_ayar_changed'] });
  const [mesgul, setMesgul] = useState<string | null>(null);
  if (hata && !veri) return <><SayfaBasligi baslik="Özellik bayrakları" /><Hata hata={hata} yenile={yenile} /></>;
  if (!veri) return <><SayfaBasligi baslik="Özellik bayrakları" /><Yukleniyor satir={6} /></>;
  return (
    <>
      <SayfaBasligi baslik="Özellik bayrakları" aciklama="Her bayrak sunucuda ilgili uçları ve öğrenci menüsünü canlı açıp kapatır. Yönetici her zaman erişir."
        eylemler={<button type="button" className="m16-btn" onClick={() => git('oyun/kaynak')}>Oyun modları ve kaynakları</button>} />
      <section className="m16-kart">
        <ul style={{ listStyle: 'none', margin: 0, padding: 0, display: 'grid', gap: 12 }}>
          {veri.ogeler.map((b) => (
            <li key={b.ad} style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
              <Anahtar acik={b.acik} mesgul={mesgul === b.ad} etiket={b.etiket} degistir={async (v) => {
                setMesgul(b.ad);
                const r = await siteAyarYaz({ bayraklar: { [b.ad]: v ? null : false } }, `${b.etiket}: ${v ? 'açık' : 'kapalı'}`);
                if (r) setVeri({ ogeler: veri.ogeler.map((x) => (x.ad === b.ad ? { ...x, acik: v, ayarli: !v } : x)) });
                setMesgul(null);
              }} />
              <div style={{ flex: 1, minWidth: 0 }}>
                <b>{b.etiket}</b> <code style={{ fontSize: 11 }}>{b.ad}</code> {!b.acik && <Rozet ton="uyari">kapalı</Rozet>}
                <div style={{ color: 'var(--color-ink-3)', fontSize: 13 }}>{b.aciklama}</div>
              </div>
            </li>
          ))}
        </ul>
      </section>
    </>
  );
}
