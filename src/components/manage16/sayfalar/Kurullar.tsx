import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, AyrintiCekmecesi, Form, Rozet, Hata, Yukleniyor, GorunurlukBaglantisi, useAdminSorgu, adminIstek, bildir, type AlanTanim } from '../kit';
import { manageAdres, type SayfaProps } from '../menu';

type Kurul = { kurul: number; kod: string; ad: string; baslangic: string; sinav: string; bitis: string; dersSayisi: number; gorunurluk: string };
type Yanit = { egitimYili: string; donem: number; final: string; butunleme: string; kaynak: string; katmanda: boolean; aktif: number; kurullar: Kurul[] };

const TARIH = { desen: /^\d{4}-\d{2}-\d{2}$/, yerTutucu: 'YYYY-AA-GG' };
const ALANLAR: AlanTanim[] = [
  { ad: 'ad', etiket: 'Ad', zorunlu: true, enFazla: 120 },
  { ad: 'kod', etiket: 'Kod', enFazla: 30 },
  { ad: 'baslangic', etiket: 'Başlangıç', tur: 'tarih', zorunlu: true, ...TARIH },
  { ad: 'sinav', etiket: 'Sınav', tur: 'tarih', zorunlu: true, ...TARIH, ipucu: 'Aktif kurul = sınav günü geçmemiş ilk kurul.' },
  { ad: 'bitis', etiket: 'Bitiş', tur: 'tarih', zorunlu: true, ...TARIH },
];

/** Kurullar ve dersler › Kurullar: takvim (kurul_takvimi_ozet.json), aktif kurul, tarih düzenleme, kurul görünürlüğü. */
export default function Kurullar({ git }: SayfaProps) {
  const { veri, hata, yenile, yukleniyor } = useAdminSorgu<Yanit>('/api/admin/kurullar', { canliOlay: ['content_changed', 'site_ayar_changed'] });
  const [acik, setAcik] = useState<number | 'genel' | null>(null);
  const [kirli, setKirli] = useState(false);
  if (hata) return <Hata hata={hata} yenile={yenile} />;
  if (!veri) return <Yukleniyor satir={6} />;
  const k = typeof acik === 'number' ? veri.kurullar.find((x) => x.kurul === acik) : null;
  const kaydet = async (degisen: Record<string, unknown>) => {
    await adminIstek(`/api/admin/kurullar/${acik}`, { yontem: 'PUT', govde: degisen });
    bildir('Kaydedildi');
    await yenile();
  };
  return (
    <>
      <SayfaBasligi baslik="Kurullar" aciklama={<>{veri.egitimYili} · Dönem {veri.donem} · final {veri.final} · bütünleme {veri.butunleme}{veri.katmanda && <> · <Rozet ton="uyari">panelde değişti (dağıtımda eşitlenir)</Rozet></>}</>}
        eylemler={<button type="button" className="m16-btn" onClick={() => setAcik('genel')}>Final / bütünleme</button>} />
      <VeriTablosu<Kurul>
        kimlik="icerik-kurullar"
        ogeler={veri.kurullar}
        satirKimligi={(x) => String(x.kurul)}
        etkin={acik == null ? null : String(acik)}
        satirTikla={(x) => setAcik(x.kurul)}
        adresteDurum={false}
        sutunlar={[
          { anahtar: 'kurul', baslik: 'Kurul', genislik: '90px', deger: (x) => x.kurul, hucre: (x) => <>{x.kurul}{x.kurul === veri.aktif && <> <Rozet ton="vurgu">aktif</Rozet></>}</> },
          { anahtar: 'ad', baslik: 'Ad', genislik: 'minmax(200px,3fr)', deger: (x) => x.ad },
          { anahtar: 'baslangic', baslik: 'Başlangıç', genislik: '110px', deger: (x) => x.baslangic },
          { anahtar: 'sinav', baslik: 'Sınav', genislik: '110px', deger: (x) => x.sinav },
          { anahtar: 'dersSayisi', baslik: 'Ders', genislik: '70px', hizala: 'sag', deger: (x) => x.dersSayisi,
            hucre: (x) => <a href={manageAdres(`icerik/dersler?s.kurul=${x.kurul}`)} onClick={(e) => { e.preventDefault(); e.stopPropagation(); git(`icerik/dersler?s.kurul=${x.kurul}`); }}>{x.dersSayisi}</a> },
          { anahtar: 'gorunurluk', baslik: 'Görünürlük', genislik: '170px', hucre: (x) => <GorunurlukBaglantisi anahtar={`kurul:${x.kurul}`} deger={x.gorunurluk} git={git} /> } /* H324 */,
        ]}
      />
      <AyrintiCekmecesi acik={acik != null} kapat={() => setAcik(null)} kirli={kirli}
        baslik={acik === 'genel' ? 'Final ve bütünleme' : k ? `Kurul ${k.kurul}: ${k.ad}` : ''}
        kayit={acik === 'genel' ? { final: veri.final, butunleme: veri.butunleme } : k || undefined}
        hedef={acik === 'genel' ? 'kurul-takvimi' : k ? `kurul:${k.kurul}` : undefined}>
        {acik === 'genel' ? (
          <Form kirliDegisti={setKirli} alanlar={[{ ad: 'final', etiket: 'Final', tur: 'tarih', zorunlu: true, ...TARIH }, { ad: 'butunleme', etiket: 'Bütünleme', tur: 'tarih', zorunlu: true, ...TARIH }]}
            deger={{ final: veri.final, butunleme: veri.butunleme }} kaydet={(_y, d) => kaydet(d)} />
        ) : k ? (
          <>
            <div className="m16-kart"><h2>Görünürlük</h2><GorunurlukBaglantisi anahtar={`kurul:${k.kurul}`} deger={k.gorunurluk} git={git} />{/* H324 */}</div>
            <Form kirliDegisti={setKirli} alanlar={ALANLAR} deger={{ ad: k.ad, kod: k.kod, baslangic: k.baslangic, sinav: k.sinav, bitis: k.bitis }} kaydet={(_y, d) => kaydet(d)} />
            <p className="m16-alan-ipucu">Ön yüz ve betikler takvimi derlemede okur: değişiklik canlıya dağıtımla (katman eşitlemesi + derleme) yansır.{yukleniyor ? ' …' : ''}</p>
          </>
        ) : null}
      </AyrintiCekmecesi>
    </>
  );
}
