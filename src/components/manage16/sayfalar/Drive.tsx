import React from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, Hata, IstatistikIzgara, IstatistikKart, adminIstek, bildir, onayIste, useAdminSorgu, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

/**
 * Sistem › Drive — Drive envanteri ve son taramalar (GET /api/admin/sistem/drive[/dosyalar]): okul kataloğu (user_drive_catalog.json),
 * öğrenci Drive'ı (ogrenci_drive_envanter.json), son "değişiklik kontrolü" (drive_check_result.json).
 * Tarama yalnız elle ve onayla: POST /api/admin/drive/check-updates (indirme yapmaz, yalnız karşılaştırır). Zamanlayıcı yok.
 */
type Dosya = { id: string; kaynak: string; ad: string; yol: string; tur: string; kurul: string; durum: string; driveId?: string };
const KAYNAK: Record<string, string> = { okul: 'Okul kataloğu', ogrenci: 'Öğrenci Drive', tarama: 'Son tarama' };

export default function Drive(_: SayfaProps) {
  const s = useAdminSorgu<any>('/api/admin/sistem/drive');
  const v = s.veri;
  const tara = async () => {
    if (!(await onayIste({
      baslik: 'Drive değişiklik kontrolü başlatılsın mı?', onayMetni: 'Elle tara',
      aciklama: <>sync-drive-updates.mjs --check-only çalışır: Drive klasörleri listelenir ve yerel arşivle karşılaştırılır (en çok 2 dk). Dosya indirilmez, LLM kullanılmaz.</>,
    }))) return;
    try {
      const r = await adminIstek<any>('/api/admin/drive/check-updates', { yontem: 'POST', govde: { scope: 'all' } });
      bildir(r.message || 'Tarama bitti', r.success ? 'iyi' : 'kotu'); void s.yenile();
    } catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  return (
    <>
      <SayfaBasligi baslik="Drive" aciklama="Drive envanteri ve son taramalar. Tarama yalnız elle başlar; yeni PDF'ten ders üretimi oturumda kullanıcı komutuyla yapılır (kural 20–22)."
        eylemler={<><button type="button" className="m16-btn" onClick={() => void s.yenile()}>Yenile</button><button type="button" className="m16-btn birincil" onClick={tara}>Elle tara…</button></>} />
      {s.hata && <Hata hata={s.hata} yenile={s.yenile} />}
      <IstatistikIzgara>
        <IstatistikKart etiket="Son tarama" yukleniyor={!v} deger={v?.sonTarama ? zamanMetni(v.sonTarama.zaman) : '—'} alt={v?.sonTarama ? `${v.sonTarama.taranan} dosya · ${v.sonTarama.yeni} yeni/değişen` : 'yok'} ton={v?.sonTarama?.var ? 'uyari' : 'notr'} />
        <IstatistikKart etiket="Öğrenci Drive" yukleniyor={!v} deger={v?.ogrenci?.dosya ?? '—'} alt={v?.ogrenci ? `taranma ${v.ogrenci.zaman}` : 'envanter yok'} />
        <IstatistikKart etiket="Okul kataloğu" yukleniyor={!v} deger={v?.katalog?.pdf ?? '—'} alt={v?.katalog ? `PDF · ${zamanMetni(v.katalog.zaman)}` : 'yok'} />
        <IstatistikKart etiket="Otomatik eşitleme" yukleniyor={!v} deger={v?.ayar?.otomatik ? 'AÇIK' : 'Kapalı'} ton={v?.ayar?.otomatik ? 'uyari' : 'iyi'} alt={v ? `son eşitleme ${v.ayar.sonEsitleme ? zamanMetni(v.ayar.sonEsitleme) : '—'}` : ''} />
      </IstatistikIzgara>
      {v?.ayar?.mesaj && <p className="m16-ts-not" style={{ margin: '8px 0' }}>{v.ayar.mesaj}</p>}
      <VeriTablosu<Dosya>
        kimlik="sistem-drive" kaynak="/api/admin/sistem/drive/dosyalar" aramaYeri="Dosya adı ya da yol ara…" satirKimligi={(d) => d.id}
        suzgecler={[
          { anahtar: 'kaynak', etiket: 'Kaynak', secenekler: Object.entries(KAYNAK).map(([deger, etiket]) => ({ deger, etiket })) },
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: ['1', '2', '3', '4', '5', '6'].map((k) => ({ deger: k, etiket: `Kurul ${k}` })) },
        ]}
        sutunlar={[
          { anahtar: 'kaynak', baslik: 'Kaynak', genislik: '120px', hucre: (d) => <Rozet ton={d.kaynak === 'tarama' ? 'uyari' : d.kaynak === 'ogrenci' ? 'bilgi' : 'notr'}>{KAYNAK[d.kaynak] || d.kaynak}</Rozet> },
          { anahtar: 'ad', baslik: 'Dosya', sirala: true, genislik: 'minmax(200px,2fr)', hucre: (d) => d.driveId ? <a href={`https://drive.google.com/file/d/${d.driveId}/view`} target="_blank" rel="noreferrer">{d.ad}</a> : d.ad },
          { anahtar: 'yol', baslik: 'Yol', genislik: 'minmax(220px,3fr)' },
          { anahtar: 'kurul', baslik: 'Kurul', sirala: true, genislik: '70px' },
          { anahtar: 'tur', baslik: 'Tür', genislik: '90px' },
          { anahtar: 'durum', baslik: 'Durum', genislik: '110px' },
        ]}
      />
    </>
  );
}
