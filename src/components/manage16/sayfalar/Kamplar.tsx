import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, AyrintiCekmecesi, Form, Rozet, Hata, Yukleniyor, useAdminSorgu, adminIstek, bildir, zamanMetni, type AlanTanim } from '../kit';
import type { SayfaProps } from '../menu';

type Tuyo = { id: string; kurul: number; brans: string; ders_id?: string; metin: string; kaynak?: string; durum: 'oneri' | 'onayli' | 'reddedildi'; zaman: string; kim?: string };
const TON = { oneri: 'uyari', onayli: 'iyi', reddedildi: 'kotu' } as const;
const AD = { oneri: 'Öneri', onayli: 'Onaylı', reddedildi: 'Reddedildi' };

const YENI: AlanTanim[] = [
  { ad: 'kurul', etiket: 'Kurul', tur: 'secim', zorunlu: true, secenekler: [1, 2, 3, 4, 5, 6].map((k) => ({ deger: String(k), etiket: String(k) })) },
  { ad: 'brans', etiket: 'Branş (slug)', zorunlu: true, desen: /^[a-z0-9]{2,30}$/, yerTutucu: 'k2farmakoloji' },
  { ad: 'ders_id', etiket: 'Ders kimliği', desen: /^k[1-6]-\d{2}$/, yerTutucu: 'k2-07' },
  { ad: 'metin', etiket: 'Tüyo', tur: 'uzun', zorunlu: true, enAz: 8, enFazla: 1500 },
  { ad: 'kaynak', etiket: 'Kaynak', yerTutucu: 'hoca (yönetici girdi)' },
];

/** Öğrenme › Kamplar: hoca tüyoları (data/kamp/tuyolar.jsonl, olay defteri) — öneriyi onayla/reddet, düzeltilmiş metinle onayla, yeni ekle. */
export default function Kamplar(_p: SayfaProps) {
  const { veri, hata, yenile } = useAdminSorgu<{ tuyolar: Tuyo[] }>('/api/admin/kamp/tuyolar');
  const [acik, setAcik] = useState<string | 'yeni' | null>(null);
  if (hata) return <Hata hata={hata} yenile={yenile} />;
  if (!veri) return <Yukleniyor satir={6} />;
  const t = veri.tuyolar.find((x) => x.id === acik);
  const karar = async (karar: 'onayla' | 'reddet', metin?: string) => {
    await adminIstek(`/api/admin/kamp/tuyo/${t!.id}/karar`, { yontem: 'POST', govde: { karar, ...(metin ? { metin } : {}) } });
    bildir(karar === 'onayla' ? 'Onaylandı' : 'Reddedildi');
    setAcik(null);
    await yenile();
  };
  return (
    <>
      <SayfaBasligi baslik="Kamplar" aciklama="Kamp içeriği yalnız ONAYLI tüyolardan üretilir. Defter salt eklemelidir: karar yeni olay olarak yazılır."
        eylemler={<button type="button" className="m16-btn birincil" onClick={() => setAcik('yeni')}>Tüyo ekle</button>} />
      <VeriTablosu<Tuyo> kimlik="ogrenme-kamp" ogeler={[...veri.tuyolar].reverse()} satirKimligi={(x) => x.id} etkin={acik} satirTikla={(x) => setAcik(x.id)}
        suzgecler={[{ anahtar: 'durum', etiket: 'Durum', secenekler: Object.entries(AD).map(([deger, etiket]) => ({ deger, etiket })) }]}
        sutunlar={[
          { anahtar: 'durum', baslik: 'Durum', genislik: '96px', deger: (x) => x.durum, hucre: (x) => <Rozet ton={TON[x.durum]}>{AD[x.durum]}</Rozet> },
          { anahtar: 'kurul', baslik: 'Kurul', genislik: '60px', deger: (x) => x.kurul },
          { anahtar: 'brans', baslik: 'Branş', genislik: 'minmax(110px,1fr)', deger: (x) => x.brans },
          { anahtar: 'metin', baslik: 'Tüyo', genislik: 'minmax(240px,4fr)', deger: (x) => x.metin, hucre: (x) => <span className="m16-kisalt" title={x.metin}>{x.metin}</span> },
          { anahtar: 'zaman', baslik: 'Zaman', genislik: '100px', deger: (x) => x.zaman, hucre: (x) => zamanMetni(x.zaman) },
        ]} />
      <AyrintiCekmecesi acik={!!acik} kapat={() => setAcik(null)} baslik={acik === 'yeni' ? 'Yeni tüyo' : t ? `${t.brans} · Kurul ${t.kurul}` : ''} kayit={t} hedef={t ? t.id : undefined}>
        {acik === 'yeni' ? (
          <Form alanlar={YENI} deger={{ kurul: '2', brans: '', ders_id: '', metin: '', kaynak: '' }} kaydetMetni="Onaylı ekle"
            kaydet={async (y) => { await adminIstek('/api/admin/kamp/tuyo', { yontem: 'POST', govde: { ...y, kurul: Number(y.kurul), ders_id: y.ders_id || undefined } }); bildir('Eklendi'); setAcik(null); await yenile(); }} />
        ) : t ? (
          <>
            <Form alanlar={[{ ad: 'metin', etiket: 'Metin (düzeltip onaylayabilirsiniz)', tur: 'uzun', zorunlu: true, enAz: 8, enFazla: 1500 }]} deger={{ metin: t.metin }} kaydetMetni="Onayla"
              kaydet={(y) => karar('onayla', y.metin !== t.metin ? String(y.metin) : undefined)} />
            {t.durum !== 'reddedildi' && <button type="button" className="m16-btn tehlike" onClick={() => void karar('reddet')}>Reddet</button>}
            <p className="m16-alan-ipucu">{t.kaynak || ''} {t.kim ? `· ${t.kim}` : ''} {t.ders_id ? `· ${t.ders_id}` : ''}</p>
          </>
        ) : null}
      </AyrintiCekmecesi>
    </>
  );
}
