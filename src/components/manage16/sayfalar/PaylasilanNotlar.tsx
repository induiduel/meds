import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, AyrintiCekmecesi, Rozet, adminIstek, bildir, onayIste, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

type Not = { id: number; oda_id: number; sahip: string; sahip_ad: string; baslik: string; metin: string; uzunluk: number; renk: string; silindi: boolean; olusturma: string; oda_ad: string | null; oda_tur: string | null };

/** Topluluk › Paylaşılan notlar — sohbet odalarında paylaşılan notlar; gizle/göster. */
export default function PaylasilanNotlar({ git }: SayfaProps) {
  const [acik, setAcik] = useState<Not | null>(null);
  const [surum, setSurum] = useState(0);
  const gizle = async (n: Not) => {
    const gizli = !n.silindi;
    if (gizli && !(await onayIste({ baslik: 'Not gizlensin mi?', aciklama: 'Odadaki öğrenciler notu göremez. Geri açılabilir.', onayMetni: 'Gizle' }))) return;
    try { await adminIstek(`/api/admin/topluluk/notlar/${n.id}/gizle`, { yontem: 'POST', govde: { gizli } }); bildir(gizli ? 'Not gizlendi.' : 'Not görünür.', 'iyi'); setAcik(null); setSurum((x) => x + 1); }
    catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  return (
    <>
      <SayfaBasligi baslik="Paylaşılan notlar" aciklama="Öğrencilerin sohbet odalarında paylaştığı notlar. Listeler denetim kaydına yazılır." />
      <VeriTablosu<Not>
        key={surum} kimlik="topluluk-not" kaynak="/api/admin/topluluk/notlar" canliOlay={['topluluk_changed', 'not_paylas']}
        aramaYeri="Başlık, metin ya da sahip…" satirKimligi={(n) => String(n.id)} etkin={acik ? String(acik.id) : null} satirTikla={setAcik}
        suzgecler={[{ anahtar: 'durum', etiket: 'Durum', secenekler: [{ deger: 'gorunur', etiket: 'Görünür' }, { deger: 'gizli', etiket: 'Gizli' }] }]}
        sutunlar={[
          { anahtar: 'baslik', baslik: 'Başlık', sirala: true, genislik: 'minmax(160px,2fr)', hucre: (n) => <span className="m16-kisalt">{n.baslik || 'Başlıksız not'}</span> },
          { anahtar: 'sahip_ad', baslik: 'Paylaşan', sirala: true, genislik: 'minmax(120px,1fr)' },
          { anahtar: 'oda_ad', baslik: 'Oda', genislik: 'minmax(120px,1fr)', hucre: (n) => (n.oda_tur === 'dm' ? `Birebir #${n.oda_id}` : n.oda_ad || `#${n.oda_id}`) },
          { anahtar: 'uzunluk', baslik: 'Uzunluk', genislik: '80px', hizala: 'sag', hucre: (n) => `${n.uzunluk} kr` },
          { anahtar: 'olusturma', baslik: 'Zaman', sirala: true, genislik: '104px', hucre: (n) => zamanMetni(n.olusturma) },
          { anahtar: 'silindi', baslik: 'Durum', genislik: '84px', hucre: (n) => (n.silindi ? <Rozet>Gizli</Rozet> : <Rozet ton="iyi">Görünür</Rozet>) },
        ]}
      />
      <AyrintiCekmecesi acik={!!acik} kapat={() => setAcik(null)} baslik={acik?.baslik || 'Başlıksız not'} altBaslik={acik ? `${acik.sahip_ad} · ${new Date(acik.olusturma).toLocaleString('tr-TR')}` : ''}
        kayit={acik || undefined} hedef={acik ? `not:${acik.id}` : undefined}
        eylemler={acik && <div className="m16-ts-eylem">
          <button type="button" className="m16-btn" onClick={() => git(`topluluk/sohbet/${acik.oda_id}`)}>Odayı aç</button>
          <button type="button" className={`m16-btn ${acik.silindi ? '' : 'tehlike'}`} onClick={() => gizle(acik)}>{acik.silindi ? 'Yeniden göster' : 'Gizle'}</button>
        </div>}>
        {acik && <div className="m16-ts-metin">{acik.metin}{acik.uzunluk > 4000 ? '\n… (ilk 4000 karakter)' : ''}</div>}
      </AyrintiCekmecesi>
    </>
  );
}
