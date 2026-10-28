import React, { useState } from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, Yukleniyor, Hata, useAdminSorgu, JsonGoruntuleyici, adminIstek, bildir, onayIste, zamanMetni, type Ton } from '../kit';
import { manageAdres, type SayfaProps } from '../menu';

/**
 * Öğrenme › Ses kuyruğu — sesli ders üretim işleri (data/sesli_anlatim/kuyruk.json). Görünüm + iş başına elle eylem
 * (yeniden dene / öne al / iptal; mevcut /api/sesli-anlatim/kuyruk/:id/:eylem). Yeni üretim BAŞLATILMAZ: kural 20, EMA GPU yolu
 * (cozucu_ses_gpu.sh) yalnız kullanıcının komutuyla çalışır.
 */
type Satir = { id: string; sira: number; key: string; saglayici: string; ses: string; durum: string; isci: string; ilerleme: string; yuzde: number; olusturuldu: string; bitti: string; hata: string };
const TON: Record<string, Ton> = { bekliyor: 'notr', calisiyor: 'bilgi', bitti: 'iyi', hata: 'kotu', iptal: 'notr', 'kota-bekliyor': 'uyari', 'butce-durdu': 'uyari' };

function Ayrinti({ id, kapat, git }: { id: string; kapat: () => void; git: SayfaProps['git'] }) {
  const { veri, hata, yukleniyor, yenile } = useAdminSorgu<any>(`/api/admin/sesli-kuyruk/${encodeURIComponent(id)}`);
  const [mesgul, setMesgul] = useState(false);
  const eylem = async (e: 'yeniden' | 'one-al' | 'iptal') => {
    if (e !== 'one-al' && !(await onayIste({ baslik: e === 'iptal' ? 'İş iptal edilsin mi?' : 'İş yeniden sıraya alınsın mı?', aciklama: 'Ses işçisi yalnız elle başlatıldığında işler; bu eylem işçiyi başlatmaz.', tehlikeli: e === 'iptal', onayMetni: e === 'iptal' ? 'İptal et' : 'Sıraya al' }))) return;
    setMesgul(true);
    try { await adminIstek(`/api/sesli-anlatim/kuyruk/${encodeURIComponent(id)}/${e}`, { yontem: 'POST' }); bildir('Yapıldı', 'iyi'); yenile(); }
    catch (x: any) { bildir(x?.message || 'Olmadı', 'kotu'); } finally { setMesgul(false); }
  };
  const d = veri?.durum;
  return (
    <AyrintiCekmecesi acik genis kapat={kapat} baslik={veri?.key || id} altBaslik={id} kayit={veri} hedef={`sesli:${veri?.key || ''}`}
      eylemler={veri && <>
        {/* H362: işin ait olduğu sesli derse panel içi bağlantı */}
        {veri.key && <a className="m16-btn hayalet" href={`${manageAdres('ogrenme/sesli')}?ac=${encodeURIComponent(veri.key)}`} onClick={(e) => { e.preventDefault(); git(`ogrenme/sesli?ac=${encodeURIComponent(veri.key)}`); }}>Sesli derse git</a>}
        {['hata', 'iptal', 'butce-durdu', 'kota-bekliyor'].includes(d) && <button type="button" className="m16-btn" disabled={mesgul} onClick={() => eylem('yeniden')}>Yeniden dene</button>}
        {['bekliyor', 'kota-bekliyor'].includes(d) && <button type="button" className="m16-btn" disabled={mesgul} onClick={() => eylem('one-al')}>Öne al</button>}
        {d !== 'bitti' && d !== 'iptal' && <button type="button" className="m16-btn tehlike" disabled={mesgul} onClick={() => eylem('iptal')}>İptal</button>}
      </>}>
      {hata ? <Hata hata={hata} yenile={yenile} /> : yukleniyor && !veri ? <Yukleniyor satir={5} /> : veri && (
        <div className="m16-kart">
          <h2>Notlar</h2>
          <ol className="m16-liste">{(veri.notlar || []).map((n: string, i: number) => <li key={i}>{n}</li>)}</ol>
          {veri.hata && <JsonGoruntuleyici veri={veri.hata} />}
        </div>
      )}
    </AyrintiCekmecesi>
  );
}

export default function SesKuyrugu({ id, git }: SayfaProps) {
  return (
    <>
      <SayfaBasligi baslik="Ses kuyruğu" aciklama="Sesli ders üretim işleri. Yeni üretim bu panelden başlatılmaz; işçi yalnız elle komutla çalışır (kural 20)." />
      <VeriTablosu<Satir>
        kimlik="ogrenme-ses-kuyruk" kaynak="/api/admin/sesli-kuyruk" aramaYeri="Ders anahtarı ya da iş ara…" satirKimligi={(s) => s.id} etkin={id || null}
        satirTikla={(s) => git(`ogrenme/ses-kuyrugu/${encodeURIComponent(s.id)}${window.location.search}`)}
        canliOlay={['sesli_anlatim']}
        suzgecler={[{ anahtar: 'durum', etiket: 'Durum', secenekler: Object.keys(TON).map((k) => ({ deger: k, etiket: k })) }]}
        sutunlar={[
          { anahtar: 'olusturuldu', baslik: 'Eklendi', sirala: true, genislik: '110px', hucre: (s) => <time title={s.olusturuldu}>{zamanMetni(s.olusturuldu)}</time> },
          { anahtar: 'key', baslik: 'Ders', genislik: 'minmax(220px,3fr)' },
          { anahtar: 'saglayici', baslik: 'Sağlayıcı', genislik: '120px' },
          { anahtar: 'ilerleme', baslik: 'İlerleme', genislik: '90px', hizala: 'sag' },
          { anahtar: 'durum', baslik: 'Durum', sirala: true, genislik: '120px', hucre: (s) => <Rozet ton={TON[s.durum] || 'notr'}>{s.durum}</Rozet> },
        ]}
      />
      {id && <Ayrinti id={id} git={git} kapat={() => git(`ogrenme/ses-kuyrugu${window.location.search}`)} />}
    </>
  );
}
