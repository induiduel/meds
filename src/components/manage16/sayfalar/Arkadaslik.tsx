import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, Rozet, adminIstek, bildir, onayIste, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';

type Iliski = { gonderen: string; alan: string; durum: 'bekliyor' | 'kabul'; olusturma: string; guncelleme: string; gonderen_ad: string | null; alan_ad: string | null };

/** Topluluk › Arkadaşlık — istekler ve kabul edilmiş ilişkiler; kaldır. */
export default function Arkadaslik({ git }: SayfaProps) {
  const [surum, setSurum] = useState(0);
  const kaldir = async (a: Iliski) => {
    if (!(await onayIste({ baslik: a.durum === 'kabul' ? 'Arkadaşlık kaldırılsın mı?' : 'İstek silinsin mi?', aciklama: `${a.gonderen_ad || a.gonderen} → ${a.alan_ad || a.alan}. Kişiler yeniden istek gönderebilir.`, onayMetni: 'Kaldır', tehlikeli: true }))) return;
    try { await adminIstek('/api/admin/topluluk/arkadaslik/kaldir', { yontem: 'POST', govde: { gonderen: a.gonderen, alan: a.alan } }); bildir('Kaldırıldı.', 'iyi'); setSurum((x) => x + 1); }
    catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  const kisi = (uid: string, ad: string | null) => <a href={`/manage/kisi/${encodeURIComponent(uid)}`} onClick={(e) => { e.preventDefault(); git(`kisi/${encodeURIComponent(uid)}`); }} title={uid}>{ad || uid.slice(0, 10) + '…'}</a>;
  return (
    <>
      <SayfaBasligi baslik="Arkadaşlık" aciklama="Arkadaşlık istekleri ve ilişkiler. Adlar kişinin sohbet kayıtlarından gelir; kimlik üstüne gelince görünür. Listeler denetim kaydına yazılır." />
      <VeriTablosu<Iliski>
        key={surum} kimlik="topluluk-arkadaslik" kaynak="/api/admin/topluluk/arkadaslik" canliOlay={['topluluk_changed', 'arkadas_changed']}
        aramaYeri="Ad ya da kimlik…" satirKimligi={(a) => `${a.gonderen}|${a.alan}`}
        suzgecler={[{ anahtar: 'durum', etiket: 'Durum', secenekler: [{ deger: 'bekliyor', etiket: 'Bekleyen' }, { deger: 'kabul', etiket: 'Arkadaş' }] }]}
        sutunlar={[
          { anahtar: 'gonderen', baslik: 'Gönderen', genislik: 'minmax(140px,1fr)', hucre: (a) => kisi(a.gonderen, a.gonderen_ad) },
          { anahtar: 'alan', baslik: 'Alan', genislik: 'minmax(140px,1fr)', hucre: (a) => kisi(a.alan, a.alan_ad) },
          { anahtar: 'durum', baslik: 'Durum', sirala: true, genislik: '96px', hucre: (a) => <Rozet ton={a.durum === 'kabul' ? 'iyi' : 'uyari'}>{a.durum === 'kabul' ? 'Arkadaş' : 'Bekliyor'}</Rozet> },
          { anahtar: 'guncelleme', baslik: 'Güncellendi', sirala: true, genislik: '112px', hucre: (a) => zamanMetni(a.guncelleme) },
          { anahtar: 'olusturma', baslik: 'İstek', sirala: true, genislik: '112px', gizli: true, hucre: (a) => zamanMetni(a.olusturma) },
          { anahtar: 'eylem', baslik: '', genislik: '84px', hucre: (a) => <button type="button" className="m16-btn hayalet" onClick={(e) => { e.stopPropagation(); void kaldir(a); }}>Kaldır</button> },
        ]}
      />
    </>
  );
}
