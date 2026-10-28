import React from 'react';
import { SayfaBasligi, Rozet, Yukleniyor, Hata, adminIstek, useAdminSorgu, onayIste, bildir, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';

/** Sorular › Havuz dondurma — data/havuz_dondur.json. Görüntü + kullanıcı onaylı aç/kapa (yazılacak sözcük). Silme yok. */
export default function HavuzDondurma(_p: SayfaProps) {
  const { veri, hata, yukleniyor, yenile, setVeri } = useAdminSorgu<any>('/api/admin/havuz-dondur', { canliOlay: ['havuz_dondur_changed'] });
  const [neden, setNeden] = React.useState('');
  if (hata) return <Hata hata={hata} yenile={yenile} />;
  if (yukleniyor && !veri) return <Yukleniyor satir={4} />;
  const acik = !!veri?.dondur;
  const degistir = async () => {
    const dondur = !acik;
    const yazilacak = dondur ? 'DONDUR' : 'AC';
    const ok = await onayIste({
      baslik: dondur ? 'Havuz dondurulsun mu?' : 'Dondurma kaldırılsın mı?',
      aciklama: dondur ? 'Serbest metin ayrıştırma, kümeleme, YZ birleştirme ve olası soru sentezi durur. Kayıt, oy ve ham defter etkilenmez.'
        : 'Otomatik işleme (ayrıştırma, kümeleme, YZ birleştirme) yeniden açılır. Bu, kullanıcının açık onayını gerektirir.',
      tehlikeli: true, yazilacak, onayMetni: dondur ? 'Dondur' : 'Aç',
    });
    if (!ok) return;
    try { const r = await adminIstek('/api/admin/havuz-dondur', { yontem: 'PUT', govde: { dondur, neden: neden || undefined, onay: yazilacak } }); setVeri({ var: true, ...r }); bildir('Güncellendi', 'iyi'); }
    catch (e: any) { bildir(e.message, 'kotu'); }
  };
  return (
    <>
      <SayfaBasligi baslik="Havuz dondurma" aciklama="Sınav dönemlerinde öğrenci soruları yalnız toplanır; otomatik işlem kullanıcı onayına kadar kapalı kalır." />
      <div className="m16-kart">
        <h2>Durum: {acik ? <Rozet ton="uyari">Donduruldu</Rozet> : <Rozet ton="iyi">Açık</Rozet>}</h2>
        <dl className="m16-satirlar">
          <dt>Neden</dt><dd>{veri?.neden || '—'}</dd>
          <dt>Başlangıç</dt><dd>{veri?.baslangic ? `${new Date(veri.baslangic).toLocaleString('tr-TR')} (${zamanMetni(veri.baslangic)})` : '—'}</dd>
          {veri?.bitis && (<><dt>Bitiş</dt><dd>{new Date(veri.bitis).toLocaleString('tr-TR')}</dd></>)}
          {veri?.guncelleyen && (<><dt>Son değiştiren</dt><dd>{veri.guncelleyen}</dd></>)}
          <dt>Dosya</dt><dd><code>data/havuz_dondur.json</code>{!veri?.var && ' (yok → açık)'}</dd>
        </dl>
      </div>
      <div className="m16-kart">
        <h2>İşlem (yalnız kullanıcı onayıyla)</h2>
        <p>Bu işlem bayrağı değiştirir; hiçbir kayıt silinmez.</p>
        <input className="m16-girdi" placeholder="Neden (isteğe bağlı)" value={neden} onChange={(e) => setNeden(e.target.value)} maxLength={500} style={{ width: '100%', marginBottom: 8 }} />
        <button type="button" className={`m16-btn ${acik ? '' : 'tehlike'}`} onClick={degistir}>{acik ? 'Dondurmayı kaldır' : 'Havuzu dondur'}</button>
      </div>
    </>
  );
}
