import React from 'react';
import { VeriTablosu, SayfaBasligi, useAdminSorgu, IstatistikIzgara, IstatistikKart, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';

/** Sorular › Olası sorular — data/olasi_sorular/k<N>.json setleri + öğrenci geri bildirimi. Salt okunur; üretim yalnız elle (kural 20). */
type Satir = { id: string; kurul: string; ders: string; soru: string; olasilik: number | null; boyleydi: number; degildi: number; duzeltme: number };

export default function OlasiSorular(_p: SayfaProps) {
  const { veri } = useAdminSorgu<{ setler: { kurul: number; soru: number; uretildi: string | null }[] }>('/api/admin/sorular/olasi', { sorgu: { boyut: 1 } });
  return (
    <>
      <SayfaBasligi baslik="Olası sorular" aciklama="Kurul başına yayımlanmış olası soru setleri ve öğrencilerin “böyleydi / değildi” geri bildirimi." />
      {veri && (veri.setler.length ? (
        <IstatistikIzgara>{veri.setler.map((s) => <IstatistikKart key={s.kurul} etiket={`Kurul ${s.kurul}`} deger={s.soru} alt={s.uretildi ? `üretildi ${zamanMetni(s.uretildi)}` : ''} />)}</IstatistikIzgara>
      ) : <p className="m16-kart">Bu sunucuda yayımlanmış olası soru seti yok (data/olasi_sorular).</p>)}
      <VeriTablosu<Satir>
        kimlik="sorular-olasi" kaynak="/api/admin/sorular/olasi" aramaYeri="Soru ya da ders ara…" satirKimligi={(s) => `${s.kurul}-${s.id}`}
        suzgecler={[{ anahtar: 'kurul', etiket: 'Kurul', secenekler: ['1', '2', '3', '4', '5', '6'].map((k) => ({ deger: k, etiket: `Kurul ${k}` })) }]}
        sutunlar={[
          { anahtar: 'kurul', baslik: 'Kurul', genislik: '64px' },
          { anahtar: 'soru', baslik: 'Soru', genislik: 'minmax(260px,3fr)' },
          { anahtar: 'ders', baslik: 'Ders', genislik: 'minmax(100px,1fr)' },
          { anahtar: 'olasilik', baslik: 'Olasılık', sirala: true, genislik: '80px', hizala: 'sag', hucre: (s) => (s.olasilik == null ? '—' : String(s.olasilik)) },
          { anahtar: 'boyleydi', baslik: 'Böyleydi', sirala: true, genislik: '80px', hizala: 'sag' },
          { anahtar: 'degildi', baslik: 'Değildi', sirala: true, genislik: '76px', hizala: 'sag' },
          { anahtar: 'duzeltme', baslik: 'Düzeltme', genislik: '76px', hizala: 'sag' },
        ]}
      />
    </>
  );
}
