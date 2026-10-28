import React from 'react';
import { SayfaBasligi, Hata, Yukleniyor, VeriTablosu, useAdminSorgu } from '../kit';
import type { SayfaProps } from '../menu';

/** Site › Sürüm (salt okunur): guncelleme_notu.json, derlenen sürüm (dist/surum.json), dağıtım damgası, sürüm günlüğü. Uç: GET /api/admin/site/surum */
type G = { surum: number; tarih: string; commit?: string; baslik: string; ogrenci?: { eklenen?: string[]; degisen?: string[]; duzeltilen?: string[] } };
type Y = { not: any; derleme: any; dagitim: any; gecmis: G[]; gecmisUretildi: string | null };

export default function SiteSurum(_p: SayfaProps) {
  const { veri: v, hata, yenile } = useAdminSorgu<Y>('/api/admin/site/surum');
  if (hata && !v) return <><SayfaBasligi baslik="Sürüm" /><Hata hata={hata} yenile={yenile} /></>;
  if (!v) return <><SayfaBasligi baslik="Sürüm" /><Yukleniyor /></>;
  const n = v.not || {};
  return (
    <>
      <SayfaBasligi baslik="Sürüm" aciklama="Salt okunur. Güncelleme notu commit/dağıtımda elle güncellenir (kural 13: onem +1)." />
      <div className="m16-izgara-2">
        <section className="m16-kart">
          <h2>Güncelleme notu · önem {n.onem ?? '–'}</h2>
          <b>{n.baslik || '—'}</b>
          <ul>{(n.maddeler || []).map((m: string, i: number) => <li key={i}>{m}</li>)}</ul>
          {(['eklenen', 'degisen', 'duzeltilen', 'silinen'] as const).filter((k) => n[k]?.length).map((k) => (
            <div key={k}><small style={{ color: 'var(--color-ink-3)' }}>{k}</small><ul>{n[k].map((m: string, i: number) => <li key={i}>{m}</li>)}</ul></div>
          ))}
        </section>
        <section className="m16-kart">
          <h2>Bu sunucu</h2>
          <dl className="m16-satirlar">
            <dt>Derlenen önem</dt><dd>{v.derleme?.onem ?? '–'}</dd>
            <dt>Derleme damgası</dt><dd>{v.derleme?.surum ?? '–'}</dd>
            <dt>Dağıtım commit</dt><dd>{v.dagitim?.commit ? String(v.dagitim.commit).slice(0, 10) : '–'}</dd>
            <dt>Dağıtım zamanı</dt><dd>{v.dagitim?.zaman || v.dagitim?.tarih || '–'}</dd>
            <dt>Günlük üretildi</dt><dd>{v.gecmisUretildi ? new Date(v.gecmisUretildi).toLocaleString('tr-TR') : '–'}</dd>
          </dl>
        </section>
      </div>
      <h2 style={{ margin: '16px 0 8px' }}>Geçmiş</h2>
      <VeriTablosu<G>
        kimlik="site-surum-gecmis"
        ogeler={v.gecmis}
        satirKimligi={(g) => `${g.surum}-${g.tarih}`}
        adresteDurum={false}
        sutunlar={[
          { anahtar: 'surum', baslik: 'Sürüm', genislik: '72px', sirala: true, deger: (g) => g.surum },
          { anahtar: 'tarih', baslik: 'Tarih', genislik: '150px', sirala: true, deger: (g) => g.tarih, hucre: (g) => new Date(g.tarih).toLocaleString('tr-TR') },
          { anahtar: 'commit', baslik: 'Commit', genislik: '90px', hucre: (g) => <code>{g.commit || ''}</code> },
          { anahtar: 'baslik', baslik: 'Başlık', genislik: 'minmax(240px,3fr)', deger: (g) => `${g.baslik} ${(g.ogrenci?.eklenen || []).join(' ')}`,
            hucre: (g) => <span title={[...(g.ogrenci?.eklenen || []), ...(g.ogrenci?.duzeltilen || [])].join('\n')}>{g.baslik}</span> },
        ]}
      />
    </>
  );
}
