import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';

/**
 * Sorular › Taslaklar — havuzdaki eksik (kök/şık/cevap tamamlanmamış) ve birleştirilmiş taslaklar, sunucu sayfalı, salt okunur.
 * Satır havuz sayfasındaki soruyu açar. Kümeleme/birleştirme aracı eski konsolda kalır (?kabuk=v14 › Taslaklar).
 */
type Satir = { id: string; tur: 'eksik' | 'birlesik'; kurul: string; ders: string; no: number; metin: string; parca: number; uydu: number; at: string };

export default function Taslaklar({ git }: SayfaProps) {
  return (
    <>
      <SayfaBasligi baslik="Taslaklar" aciklama="Tamamlanmamış ya da birleştirilmiş havuz soruları. Satıra tıklayınca soru havuzda açılır."
        eylemler={<a className="m16-btn" href="/manage/taslaklar?kabuk=v14">Kümeleme aracı (eski konsol)</a>} />
      <VeriTablosu<Satir>
        kimlik="sorular-taslak" kaynak="/api/admin/sorular/taslak" aramaYeri="Metin, ders ya da kimlik ara…" satirKimligi={(s) => s.id}
        satirTikla={(s) => git(`sorular/havuz/${encodeURIComponent(s.id)}`)}
        canliOlay={['question_updated', 'db_change']}
        suzgecler={[
          { anahtar: 'tur', etiket: 'Tür', secenekler: [{ deger: 'eksik', etiket: 'Eksik' }, { deger: 'birlesik', etiket: 'Birleştirilmiş' }] },
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: ['1', '2', '3', '4', '5', '6'].map((k) => ({ deger: k, etiket: `Kurul ${k}` })) },
        ]}
        sutunlar={[
          { anahtar: 'no', baslik: 'No', sirala: true, genislik: '56px', hizala: 'sag' },
          { anahtar: 'metin', baslik: 'Taslak', genislik: 'minmax(260px,3fr)' },
          { anahtar: 'ders', baslik: 'Ders', genislik: 'minmax(100px,1fr)' },
          { anahtar: 'parca', baslik: 'Parça', sirala: true, genislik: '64px', hizala: 'sag' },
          { anahtar: 'tur', baslik: 'Tür', genislik: '120px', hucre: (s) => (s.tur === 'birlesik' ? <Rozet ton="bilgi">Birleştirilmiş{s.uydu ? ` · ${s.uydu}` : ''}</Rozet> : <Rozet ton="uyari">Eksik</Rozet>) },
          { anahtar: 'at', baslik: 'Güncellendi', sirala: true, genislik: '110px', hucre: (s) => (s.at ? <time title={s.at}>{zamanMetni(s.at)}</time> : '—') },
        ]}
      />
    </>
  );
}
