import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, Hata, IstatistikIzgara, IstatistikKart, adminIstek, bildir, onayIste, useAdminSorgu, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

/**
 * Sistem › RAG indeksi — vektör kapsaması (GET /api/rag/vectors/health), hat raporu + cron günlüğü + elle denetim durumu
 * (GET /api/admin/sistem/rag). `rag_vektor_hatti.py --denetle` yalnız elle: POST /api/admin/sistem/rag/denetle (onay 'DENETLE';
 * varsayılan --kuru, yazmadan sayar). CPU vektör servisi kullanılır; GPU/LLM yok, zamanlayıcı yok.
 */
export default function Rag(_: SayfaProps) {
  const h = useAdminSorgu<any>('/api/rag/vectors/health');
  const s = useAdminSorgu<any>('/api/admin/sistem/rag', { aralikMs: 10000 });
  const v = s.veri;
  const calisiyor = v?.is && !v.is.bitis;
  const denetle = async (kuru: boolean) => {
    if (!(await onayIste({
      baslik: kuru ? 'Vektör denetimi (kuru) başlatılsın mı?' : 'Vektör denetimi ve ONARIM başlatılsın mı?', tehlikeli: true, yazilacak: 'DENETLE', onayMetni: 'Elle başlat',
      aciklama: <>rag_vektor_hatti.py --denetle{kuru ? ' --kuru' : ''}: yanlış parçaya ait bge-m3 vektörleri aranır{kuru ? ', hiçbir şey yazılmaz' : ' ve yerel meds-pg\'de yeniden vektörlenir (Oracle\'a taşımaz)'}. CPU vektör servisi (bge-m3 :8094) kullanılır.</>,
    }))) return;
    try { await adminIstek('/api/admin/sistem/rag/denetle', { yontem: 'POST', govde: { onay: 'DENETLE', kuru } }); bildir('Denetim başladı', 'iyi'); void s.yenile(); }
    catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  const r = v?.rapor;
  return (
    <>
      <SayfaBasligi baslik="RAG indeksi" aciklama="Vektör kapsaması ve vektör hattı durumu. Denetim yalnız elle ve bu cihazda başlar."
        eylemler={<>
          <button type="button" className="m16-btn" onClick={() => { void h.yenile(); void s.yenile(); }}>Yenile</button>
          <button type="button" className="m16-btn" disabled={!v?.cihaz || calisiyor} onClick={() => denetle(true)}>Denetle (kuru)…</button>
          <button type="button" className="m16-btn tehlike" disabled={!v?.cihaz || calisiyor} onClick={() => denetle(false)}>Denetle ve onar…</button>
        </>} />
      {h.hata && <Hata hata={h.hata} yenile={h.yenile} />}
      <IstatistikIzgara>
        <IstatistikKart etiket="Parça" yukleniyor={!h.veri} deger={h.veri?.toplam?.toLocaleString('tr-TR') ?? '—'} />
        <IstatistikKart etiket="bge-m3 kapsaması" yukleniyor={!h.veri} deger={h.veri ? `%${h.veri.kapsama}` : '—'} ton={h.veri && h.veri.kapsama < 99 ? 'uyari' : 'iyi'} alt={h.veri ? `${h.veri.bge_m3} vektör · e5 ${h.veri.e5}` : ''} />
        <IstatistikKart etiket="Eski vektör" yukleniyor={!h.veri} deger={h.veri?.bge_eski ?? '—'} ton={h.veri?.bge_eski ? 'uyari' : 'iyi'} alt="içerik değişmiş, vektör eski" />
        <IstatistikKart etiket="Son hat çalışması" yukleniyor={!v} deger={r ? zamanMetni(r.zaman) : '—'} alt={r ? `${r.sure_sn} sn · Oracle +${r.oracle?.gonderilecek ?? 0}/−${r.oracle?.silinecek ?? 0}` : 'rapor yok'} />
      </IstatistikIzgara>
      <VeriTablosu<any> kimlik="sistem-rag-tur" ogeler={h.veri?.turler || []} satirKimligi={(t) => t.document_type} adresteDurum={false}
        sutunlar={[
          { anahtar: 'document_type', baslik: 'Tür', genislik: 'minmax(160px,2fr)', deger: (t) => t.document_type },
          { anahtar: 'toplam', baslik: 'Parça', hizala: 'sag', genislik: '100px', deger: (t) => t.toplam },
          { anahtar: 'bge_m3', baslik: 'bge-m3', hizala: 'sag', genislik: '100px', deger: (t) => t.bge_m3, hucre: (t) => <span>{t.bge_m3} {t.bge_m3 < t.toplam ? <Rozet ton="uyari">−{t.toplam - t.bge_m3}</Rozet> : null}</span> },
          { anahtar: 'e5', baslik: 'e5', hizala: 'sag', genislik: '90px', deger: (t) => t.e5 },
          { anahtar: 'bge_eski', baslik: 'Eski', hizala: 'sag', genislik: '80px', deger: (t) => t.bge_eski },
          { anahtar: 'son', baslik: 'Son güncelleme', genislik: '130px', deger: (t) => t.son || '', hucre: (t) => t.son ? zamanMetni(t.son) : '—' },
        ]} />
      <div className="m16-ts-izgara">
        <section className="m16-kart">
          <h2>Elle denetim</h2>
          {!v?.cihaz && <p className="m16-ts-not">Bu sunucu cihaz değil; denetim yalnız yerel panelden (Yerel hedef) başlar.</p>}
          {v?.is ? <>
            <dl className="m16-satirlar">
              <dt>Başlama</dt><dd>{zamanMetni(v.is.baslama)} · {v.is.kim} {v.is.kuru ? <Rozet>kuru</Rozet> : <Rozet ton="uyari">onarım</Rozet>}</dd>
              <dt>Durum</dt><dd>{v.is.bitis ? <Rozet ton={v.is.kod === 0 ? 'iyi' : 'kotu'}>bitti · {v.is.kod}</Rozet> : <Rozet ton="vurgu">çalışıyor</Rozet>}</dd>
            </dl>
            <pre className="m16-ts-log">{(v.is.cikti || []).join('\n')}</pre>
          </> : <p className="m16-ts-not">Bu açılışta denetim çalıştırılmadı.</p>}
        </section>
        <section className="m16-kart">
          <h2>Hat günlüğü (cron, son 40)</h2>
          <p className="m16-ts-not">Cron 2026-10-27'den beri kapalı; hat gece hattından ya da elle çalışır. Hat durumu: {v?.hatDurum ? `${zamanMetni(v.hatDurum.son)} · kod ${v.hatDurum.kod}` : '—'}</p>
          <pre className="m16-ts-log">{(v?.cronLog || []).join('\n') || 'Günlük yok.'}</pre>
        </section>
      </div>
    </>
  );
}
