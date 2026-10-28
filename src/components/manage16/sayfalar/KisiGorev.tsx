import React from 'react';
import { SayfaBasligi, VeriTablosu, useAdminSorgu, Hata, Yukleniyor } from '../kit';
import type { SayfaProps } from '../menu';
import { kisiYolu, sureMetni } from './kisiOrtak';

type GSatir = { key: string; ad: string; email: string | null; seri: number; enUzun: number; toplamGun: number; sonGiris: string | null; gun: { d: string; giris: boolean; calisma: number; soru: number }[] };

/** Kullanıcılar › Seri ve görevler: giriş serisi ve son 14 günün giriş/çalışma ızgarası. */
export default function KisiGorev({ git }: SayfaProps) {
  const d = useAdminSorgu<{ kisiler: GSatir[]; bugun: string }>('/api/admin/people/gorev-takip', { canliOlay: ['people_changed'] });
  if (d.hata && !d.veri) return <Hata hata={d.hata} yenile={d.yenile} />;
  return (
    <>
      <SayfaBasligi baslik="Seri ve görevler" aciklama="Giriş serisi (çalışma, sayfa ziyareti ya da giriş olan günler) ve son 14 gün." />
      {!d.veri ? <Yukleniyor satir={8} /> : (
        <VeriTablosu<GSatir>
          kimlik="kisi-gorev" ogeler={d.veri.kisiler} satirKimligi={(x) => x.key} aramaYeri="Ad, e-posta…" satirTikla={(x) => git(kisiYolu(x.key, 'calisma'))}
          sutunlar={[
            { anahtar: 'ad', baslik: 'Kişi', genislik: 'minmax(160px,2fr)', sirala: true, deger: (x) => `${x.ad} ${x.email || ''}` , hucre: (x) => <span className="m16-kisalt">{x.ad}</span> },
            { anahtar: 'seri', baslik: 'Seri', genislik: '60px', hizala: 'sag', sirala: true, deger: (x) => x.seri },
            { anahtar: 'enUzun', baslik: 'En uzun', genislik: '70px', hizala: 'sag', sirala: true, deger: (x) => x.enUzun },
            { anahtar: 'toplamGun', baslik: 'Gün', genislik: '60px', hizala: 'sag', sirala: true, deger: (x) => x.toplamGun },
            { anahtar: 'gun', baslik: 'Son 14 gün', genislik: '220px', hucre: (x) => (
              <span style={{ display: 'flex', gap: 2 }} aria-label={`${x.gun.filter((g) => g.giris).length} aktif gün`}>
                {x.gun.map((g) => <span key={g.d} title={`${g.d}: ${sureMetni(g.calisma)}, ${g.soru} soru`} style={{ width: 12, height: 12, borderRadius: 3, background: g.calisma > 0 ? 'var(--color-accent)' : g.giris ? 'var(--color-ink-3)' : 'var(--m16-cizgi)' }} />)}
              </span>
            ) },
          ]}
        />
      )}
    </>
  );
}
