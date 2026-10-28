import React, { useState } from 'react';
import { SayfaBasligi, AyrintiCekmecesi, Form, Rozet, Hata, Yukleniyor, useAdminSorgu, adminIstek, bildir } from '../kit';
import type { SayfaProps } from '../menu';

type Kurul = { toplam: number; hedef: number; tahmini?: boolean; yontem?: string; branslar: Record<string, number> };

/** Kaynaklar › Sınav dağılımı (sinav_dagilimi.json): kurul başına branş soru sayıları; 60 planı ve son prova okur. */
export default function SinavDagilimi(_p: SayfaProps) {
  const { veri, hata, yenile } = useAdminSorgu<{ aciklama: string; kurullar: Record<string, Kurul> }>('/api/admin/sinav-dagilimi', { canliOlay: ['content_changed'] });
  const [acik, setAcik] = useState<string | null>(null);
  if (hata) return <Hata hata={hata} yenile={yenile} />;
  if (!veri) return <Yukleniyor satir={4} />;
  const k = acik ? veri.kurullar[acik] : null;
  return (
    <>
      <SayfaBasligi baslik="Sınav dağılımı" aciklama={veri.aciklama}
        eylemler={<select className="m16-girdi" value="" aria-label="Kurul ekle" onChange={(e) => e.target.value && setAcik(e.target.value)}><option value="">Kurul düzenle…</option>{[1, 2, 3, 4, 5, 6].map((n) => <option key={n} value={n}>Kurul {n}</option>)}</select>} />
      <div className="m16-izgara-2">
        {Object.entries(veri.kurullar).map(([no, x]) => {
          const toplam = Object.values(x.branslar || {}).reduce((a, n) => a + n, 0);
          return (
            <div key={no} className="m16-kart">
              <h2>Kurul {no} {x.tahmini && <Rozet ton="uyari">tahmini</Rozet>} {toplam !== x.toplam && <Rozet ton="kotu">toplam {toplam} ≠ {x.toplam}</Rozet>}</h2>
              <p className="m16-alan-ipucu">{x.toplam} soru · hedef {x.hedef}{x.yontem ? ` · ${x.yontem}` : ''}</p>
              <dl className="m16-satirlar">{Object.entries(x.branslar || {}).map(([b, n]) => <React.Fragment key={b}><dt>{b}</dt><dd>{n}</dd></React.Fragment>)}</dl>
              <button type="button" className="m16-btn" onClick={() => setAcik(no)}>Düzenle</button>
            </div>
          );
        })}
      </div>
      <AyrintiCekmecesi acik={!!acik} kapat={() => setAcik(null)} baslik={`Kurul ${acik}`} kayit={k || undefined} hedef={acik ? `sinav-dagilimi:${acik}` : undefined}>
        {acik && <Form
          alanlar={[{ ad: 'toplam', etiket: 'Toplam soru', tur: 'sayi', zorunlu: true }, { ad: 'hedef', etiket: 'Hedef doğru', tur: 'sayi', zorunlu: true }, { ad: 'tahmini', etiket: 'Tahmini', tur: 'anahtar' }, { ad: 'branslar', etiket: 'Branşlar (slug → soru)', tur: 'json' }]}
          deger={{ toplam: k?.toplam ?? 100, hedef: k?.hedef ?? 60, tahmini: !!k?.tahmini, branslar: k?.branslar || {} }}
          kaydet={async (_y, d) => { await adminIstek(`/api/admin/sinav-dagilimi/${acik}`, { yontem: 'PUT', govde: { ...d, ...('toplam' in d ? { toplam: Number(d.toplam) } : {}), ...('hedef' in d ? { hedef: Number(d.hedef) } : {}) } }); bildir('Kaydedildi'); await yenile(); }} />}
      </AyrintiCekmecesi>
    </>
  );
}
