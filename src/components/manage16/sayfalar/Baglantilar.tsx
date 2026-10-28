import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet } from '../kit';
import type { SayfaProps } from '../menu';

/**
 * Sistem › Bağlantılar — ders ↔ çıkmış soru ↔ ders slaytı ↔ Öğren destesi ↔ terim bağları (faz verisinden, salt okunur).
 * GET /api/admin/sistem/baglanti (ders özeti) ve /api/admin/sistem/baglanti/:ders (sorular). Soru satırı Çıkmış sayfasında açılır.
 */
type Ders = { id: string; ders: string; kurul: string; soru: number; slayt: number; ogren: number; terim: number; kaynak: number };
type Soru = { id: string; kurul: string; konu: string; kazanim: string; kok: string; slayt: string; slaytN: number; ogren: string; ogrenN: number; terim: string; var: string[] };
const oran = (a: number, b: number) => (b ? `${a} (%${Math.round((a / b) * 100)})` : '0');

export default function Baglantilar({ id, git }: SayfaProps) {
  if (id) {
    return (
      <>
        <SayfaBasligi baslik={id} aciklama="Bu derse bağlı çıkmış sorular ve her sorunun slayt, Öğren ve terim bağları."
          eylemler={<button type="button" className="m16-btn" onClick={() => git('sistem/baglanti')}>← Tüm dersler</button>} />
        <VeriTablosu<Soru>
          kimlik="sistem-baglanti-soru" kaynak={`/api/admin/sistem/baglanti/${encodeURIComponent(id)}`} aramaYeri="Soru, konu, kazanım ya da terim ara…" satirKimligi={(s) => s.id}
          satirTikla={(s) => git(`sorular/cikmis/${encodeURIComponent(s.id)}`)}
          suzgecler={[{ anahtar: 'var', etiket: 'Bağ', secenekler: [
            { deger: 'slayt', etiket: 'Slaytı var' }, { deger: '-slayt', etiket: 'Slaytı yok' }, { deger: 'ogren', etiket: 'Öğren bağı var' },
            { deger: '-ogren', etiket: 'Öğren bağı yok' }, { deger: 'terim', etiket: 'Terimi var' }] }]}
          sutunlar={[
            { anahtar: 'id', baslik: 'Soru', genislik: '150px' },
            { anahtar: 'konu', baslik: 'Konu / kazanım', sirala: true, genislik: 'minmax(180px,2fr)', hucre: (s) => <>{s.konu || '—'}{s.kazanim && <div className="m16-ts-not">{s.kazanim}</div>}</> },
            { anahtar: 'kok', baslik: 'Kök', genislik: 'minmax(200px,2fr)', gizli: true },
            { anahtar: 'slaytN', baslik: 'Slayt', sirala: true, genislik: 'minmax(160px,2fr)', hucre: (s) => s.slayt ? <span title={s.slayt}>{s.slaytN > 2 ? `${s.slayt} +${s.slaytN - 2}` : s.slayt}</span> : <Rozet ton="uyari">yok</Rozet> },
            { anahtar: 'ogrenN', baslik: 'Öğren', sirala: true, genislik: 'minmax(140px,1fr)', hucre: (s) => s.ogren || '—' },
            { anahtar: 'terim', baslik: 'Terim / kısaltma', genislik: 'minmax(140px,1fr)', hucre: (s) => s.terim || '—' },
          ]}
        />
      </>
    );
  }
  return (
    <>
      <SayfaBasligi baslik="Bağlantılar" aciklama="Faz verisinden ders başına çıkmış soru ↔ slayt ↔ Öğren ↔ terim bağ kapsaması. Derse tıklayınca soru soru bağlar açılır." />
      <VeriTablosu<Ders>
        kimlik="sistem-baglanti" kaynak="/api/admin/sistem/baglanti" aramaYeri="Ders ara…" satirKimligi={(d) => d.id} boyut={100}
        satirTikla={(d) => git(`sistem/baglanti/${encodeURIComponent(d.id)}`)}
        suzgecler={[{ anahtar: 'kurul', etiket: 'Kurul', secenekler: ['1', '2', '3', '4', '5', '6'].map((k) => ({ deger: k, etiket: `Kurul ${k}` })) }]}
        sutunlar={[
          { anahtar: 'ders', baslik: 'Ders', sirala: true, genislik: 'minmax(180px,2fr)' },
          { anahtar: 'kurul', baslik: 'Kurul', genislik: '120px' },
          { anahtar: 'soru', baslik: 'Çıkmış soru', sirala: true, hizala: 'sag', genislik: '100px' },
          { anahtar: 'slayt', baslik: 'Slaytlı', sirala: true, hizala: 'sag', genislik: '110px', hucre: (d) => oran(d.slayt, d.soru) },
          { anahtar: 'ogren', baslik: 'Öğren bağlı', sirala: true, hizala: 'sag', genislik: '110px', hucre: (d) => oran(d.ogren, d.soru) },
          { anahtar: 'terim', baslik: 'Terimli', sirala: true, hizala: 'sag', genislik: '110px', hucre: (d) => oran(d.terim, d.soru) },
          { anahtar: 'kaynak', baslik: 'Slayt dosyası', hizala: 'sag', genislik: '100px' },
        ]}
      />
    </>
  );
}
