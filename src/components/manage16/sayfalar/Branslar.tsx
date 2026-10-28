import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, AyrintiCekmecesi, Form, Hata, Yukleniyor, useAdminSorgu, adminIstek, bildir } from '../kit';
import type { SayfaProps } from '../menu';

type Brans = { harf: string; ad: string; slug: string; kisa: string; dersSayisi: number };

/** Kurullar ve dersler › Branşlar (dersler/branslar.json): ad ve kısa ad düzenlenir; harf ve slug kalıcıdır (kural 15). */
export default function Branslar(_p: SayfaProps) {
  const { veri, hata, yenile } = useAdminSorgu<{ branslar: Brans[]; aciklama: string }>('/api/admin/branslar', { canliOlay: ['content_changed'] });
  const [acik, setAcik] = useState<string | null>(null);
  const [kirli, setKirli] = useState(false);
  if (hata) return <Hata hata={hata} yenile={yenile} />;
  if (!veri) return <Yukleniyor satir={6} />;
  const b = veri.branslar.find((x) => x.harf === acik);
  return (
    <>
      <SayfaBasligi baslik="Branşlar" aciklama={veri.aciklama} />
      <VeriTablosu<Brans> kimlik="icerik-branslar" ogeler={veri.branslar} satirKimligi={(x) => x.harf} etkin={acik} satirTikla={(x) => setAcik(x.harf)} adresteDurum={false}
        sutunlar={[
          { anahtar: 'harf', baslik: 'Harf', genislik: '60px', deger: (x) => x.harf, hucre: (x) => <code>{x.harf}</code> },
          { anahtar: 'ad', baslik: 'Ad', genislik: 'minmax(160px,2fr)', deger: (x) => x.ad },
          { anahtar: 'kisa', baslik: 'Kısa', genislik: 'minmax(100px,1fr)', deger: (x) => x.kisa },
          { anahtar: 'slug', baslik: 'Klasör', genislik: 'minmax(100px,1fr)', deger: (x) => x.slug, hucre: (x) => <code>{x.slug}</code> },
          { anahtar: 'dersSayisi', baslik: 'Ders', genislik: '70px', hizala: 'sag', deger: (x) => x.dersSayisi },
        ]} />
      <AyrintiCekmecesi acik={!!b} kapat={() => setAcik(null)} baslik={b?.ad || ''} kayit={b} hedef={b ? `brans:${b.harf}` : undefined} kirli={kirli}>
        {b && <Form kirliDegisti={setKirli} alanlar={[{ ad: 'ad', etiket: 'Ad', zorunlu: true, enFazla: 80 }, { ad: 'kisa', etiket: 'Kısa ad', zorunlu: true, enFazla: 40 }, { ad: 'harf', etiket: 'Harf', salt: true }, { ad: 'slug', etiket: 'Klasör (slug)', salt: true }]}
          deger={{ ad: b.ad, kisa: b.kisa, harf: b.harf, slug: b.slug }}
          kaydet={async (_y, d) => { const { harf: _h, slug: _s, ...g } = d as any; await adminIstek(`/api/admin/branslar/${b.harf}`, { yontem: 'PUT', govde: g }); bildir('Kaydedildi'); await yenile(); }} />}
      </AyrintiCekmecesi>
    </>
  );
}
