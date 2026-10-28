import React, { useEffect, useState } from 'react';
import { Construction } from 'lucide-react';
import { SayfaBasligi, Hata, Yukleniyor, Rozet, onayIste, zamanMetni, yazimHedefi } from '../kit';
import type { SayfaProps } from '../menu';
import { siteAyarYaz, useSiteAyarAdmin } from './ortak/siteAyarOrtak';

/**
 * Site › Bakım: bakım kipi (öğrenci /api/* istekleri 503 + bakım ekranı; yönetici ve /api/admin/* dışarıda).
 * Kalıcı: site_ayar.bakim (sunucu açılışta uygular). Ortam MEDS_BAKIM=1 ayrıca açık tutabilir.
 */
export default function SiteBakim(_p: SayfaProps) {
  const { veri: a, hata, yenile, setVeri } = useSiteAyarAdmin();
  const [sure, setSure] = useState('');
  const [mesaj, setMesaj] = useState('');
  const [mesgul, setMesgul] = useState(false);
  useEffect(() => { if (a) { setSure(a.bakim?.sure || ''); setMesaj(a.bakim?.mesaj || ''); } }, [a?.bakim?.acik, a?.bakim?.sure, a?.bakim?.mesaj]);
  if (hata && !a) return <><SayfaBasligi baslik="Bakım" /><Hata hata={hata} yenile={yenile} /></>;
  if (!a) return <><SayfaBasligi baslik="Bakım" /><Yukleniyor /></>;
  const acik = !!a.bakim?.acik;
  const yaz = async (yeniAcik: boolean) => {
    if (yeniAcik && !(await onayIste({ baslik: 'Bakım kipi açılsın mı?', aciklama: `Hedef: ${yazimHedefi()}. Öğrenciler siteyi kullanamaz, bakım ekranı görür. Yönetim paneli çalışmaya devam eder.` /* H262: onay hedefi söyler */, tehlikeli: true, yazilacak: 'BAKIM', onayMetni: 'Bakımı aç' }))) return;
    setMesgul(true);
    const r = await siteAyarYaz({ bakim: { acik: yeniAcik, ...(sure.trim() ? { sure: sure.trim() } : {}), ...(mesaj.trim() ? { mesaj: mesaj.trim() } : {}) } }, yeniAcik ? 'Bakım açıldı' : 'Bakım kapatıldı');
    if (r) setVeri(r as any);
    setMesgul(false);
  };
  return (
    <>
      <SayfaBasligi baslik="Bakım" aciklama="Bakımda öğrenci istekleri 503 alır ve bakım ekranı görür; panel ve yönetici istekleri etkilenmez." />
      <section className="m16-kart" style={{ maxWidth: 640 }}>
        <h2><Construction aria-hidden="true" style={{ width: 16, verticalAlign: -3 }} /> Durum: <Rozet ton={acik ? 'kotu' : 'iyi'}>{acik ? 'BAKIMDA' : 'Yayında'}</Rozet></h2>
        <p style={{ color: 'var(--color-ink-3)', fontSize: 13 }}>{a.guncellendi ? `Site ayarı ${zamanMetni(a.guncellendi)} güncellendi${a.guncelleyen ? ` (${a.guncelleyen})` : ''}.` : ''}</p>
        <label style={{ display: 'grid', gap: 4, marginTop: 12 }}>
          <span>Tahmini süre</span>
          <input className="m16-girdi" value={sure} maxLength={40} placeholder="ör. 15 dk" onChange={(e) => setSure(e.target.value)} />
        </label>
        <label style={{ display: 'grid', gap: 4, marginTop: 12 }}>
          <span>Öğrenciye mesaj (boşsa varsayılan metin)</span>
          <textarea className="m16-girdi" rows={3} value={mesaj} maxLength={300} placeholder="Siteyi iyileştiriyoruz. Birazdan kendiliğinden geri döneceğiz." onChange={(e) => setMesaj(e.target.value)} />
        </label>
        <div style={{ display: 'flex', gap: 8, marginTop: 16, flexWrap: 'wrap' }}>
          {acik ? (
            <>
              <button type="button" className="m16-btn birincil" disabled={mesgul} onClick={() => void yaz(false)}>Bakımı kapat</button>
              <button type="button" className="m16-btn" disabled={mesgul} onClick={async () => { setMesgul(true); const r = await siteAyarYaz({ bakim: { acik: true, ...(sure.trim() ? { sure: sure.trim() } : {}), ...(mesaj.trim() ? { mesaj: mesaj.trim() } : {}) } }, 'Bakım metni güncellendi'); if (r) setVeri(r as any); setMesgul(false); }}>Süre/mesajı güncelle</button>
            </>
          ) : (
            <button type="button" className="m16-btn tehlike" disabled={mesgul} onClick={() => void yaz(true)}>Bakımı aç</button>
          )}
        </div>
      </section>
    </>
  );
}
