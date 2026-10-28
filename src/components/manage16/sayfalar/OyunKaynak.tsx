import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, Rozet, Hata, Yukleniyor, useAdminSorgu } from '../kit';
import type { SayfaProps } from '../menu';
import { Anahtar, siteAyarYaz } from './ortak/siteAyarOrtak';

/**
 * Oyunlar › Soru kaynakları ve modlar.
 * Kaynak = yayındaki sesli soru çözücü seti (src/data/<branş>_cozucu); kapatınca bayrak oyun_kaynak_<branş>=false → lobide görünmez, soru vermez.
 * Mod bayrağı oyun_mod_<id>=false → OyunlarV15 mod kartı kalkar; canlı/takım için sunucu oda kurmayı da reddeder.
 * Oyunlar genel bayrağı (oyunlar) Site › Özellik bayraklarında da bulunur.
 */
type Kaynak = { brans: string; ad: string; kurul: number; n: number; gorselN: number; acik: boolean; ders: { kod: string; baslik: string; n: number }[] };
type Mod = { id: string; ad: string; sunucu?: boolean; acik: boolean };

export default function OyunKaynak(_p: SayfaProps) {
  const k = useAdminSorgu<{ ogeler: Kaynak[] }>('/api/admin/quiz/kaynaklar', { canliOlay: ['site_ayar_changed'] });
  const m = useAdminSorgu<{ ogeler: Mod[]; oyunlarAcik: boolean }>('/api/admin/quiz/modlar', { canliOlay: ['site_ayar_changed'] });
  const [mesgul, setMesgul] = useState<string | null>(null);
  const yaz = async (ad: string, acik: boolean, metin: string) => {
    setMesgul(ad);
    const r = await siteAyarYaz({ bayraklar: { [ad]: acik ? null : false } }, metin);
    if (r) { void k.yenile(); void m.yenile(); }
    setMesgul(null);
  };
  if ((k.hata && !k.veri) || (m.hata && !m.veri)) return <><SayfaBasligi baslik="Soru kaynakları" /><Hata hata={k.hata || m.hata} yenile={() => { void k.yenile(); void m.yenile(); }} /></>;
  return (
    <>
      <SayfaBasligi baslik="Soru kaynakları ve modlar" aciklama="Oyunlar yalnız yayındaki sesli soru çözücü setlerinden soru alır. Kapatılan kaynak/mod öğrenciye anında kalkar." />
      {!m.veri ? <Yukleniyor /> : (
        <section className="m16-kart">
          <h2 style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <Anahtar acik={m.veri.oyunlarAcik} mesgul={mesgul === 'oyunlar'} etiket="Oyunlar açık" degistir={(v) => void yaz('oyunlar', v, `Oyunlar ${v ? 'açık' : 'kapalı'}`)} />
            Oyunlar {m.veri.oyunlarAcik ? <Rozet ton="iyi">açık</Rozet> : <Rozet ton="kotu">kapalı (sayfa gizli, uçlar 403)</Rozet>}
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 8, marginTop: 8 }}>
            {m.veri.ogeler.map((x) => (
              <label key={x.id} style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                <Anahtar acik={x.acik} mesgul={mesgul === `oyun_mod_${x.id}`} etiket={x.ad} degistir={(v) => void yaz(`oyun_mod_${x.id}`, v, `${x.ad}: ${v ? 'açık' : 'kapalı'}`)} />
                <span>{x.ad}{x.sunucu ? <small style={{ color: 'var(--color-ink-3)' }}> · canlı</small> : null}</span>
              </label>
            ))}
          </div>
        </section>
      )}
      <h2 style={{ margin: '16px 0 8px' }}>Kaynaklar</h2>
      <VeriTablosu<Kaynak>
        kimlik="oyun-kaynak"
        ogeler={k.veri?.ogeler || []}
        satirKimligi={(x) => x.brans}
        adresteDurum={false}
        aramaYeri="Kaynak ara…"
        sutunlar={[
          { anahtar: 'acik', baslik: 'Açık', genislik: '64px', hizala: 'orta', deger: (x) => (x.acik ? 1 : 0),
            hucre: (x) => <span onClick={(e) => e.stopPropagation()}><Anahtar acik={x.acik} mesgul={mesgul === `oyun_kaynak_${x.brans}`} etiket={`${x.ad} kaynağı`} degistir={(v) => void yaz(`oyun_kaynak_${x.brans}`, v, `${x.ad}: ${v ? 'açık' : 'kapalı'}`)} /></span> },
          { anahtar: 'ad', baslik: 'Kaynak', genislik: 'minmax(160px,2fr)', sirala: true, deger: (x) => `${x.ad} ${x.brans}`, hucre: (x) => <span><b>{x.ad}</b> <code style={{ fontSize: 11 }}>{x.brans}</code></span> },
          { anahtar: 'kurul', baslik: 'Kurul', genislik: '70px', hizala: 'sag', sirala: true, deger: (x) => x.kurul },
          { anahtar: 'ders', baslik: 'Ders', genislik: '70px', hizala: 'sag', sirala: true, deger: (x) => x.ders.length, hucre: (x) => x.ders.length },
          { anahtar: 'n', baslik: 'Soru', genislik: '80px', hizala: 'sag', sirala: true, deger: (x) => x.n },
          { anahtar: 'gorselN', baslik: 'Görselli', genislik: '80px', hizala: 'sag', sirala: true, deger: (x) => x.gorselN },
        ]}
      />
    </>
  );
}
