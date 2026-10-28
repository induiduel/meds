import React, { useState } from 'react';
import { VeriTablosu, SayfaBasligi, Rozet, AyrintiCekmecesi, JsonGoruntuleyici, durumTonu, zamanMetni, type DenetimSatiri } from '../kit';
import type { SayfaProps } from '../menu';

/** Sistem › Denetim kaydı — kitin örnek sayfası (VeriTablosu sunucu kipi + çekmece). */
export default function Denetim(_p: SayfaProps) {
  const [acik, setAcik] = useState<DenetimSatiri | null>(null);
  return (
    <>
      <SayfaBasligi baslik="Denetim kaydı" aciklama="Tüm yönetici yazma işlemleri ve kişisel veri okumaları (meds-pg yonetici_denetim)." />
      <VeriTablosu<DenetimSatiri>
        kimlik="sistem-denetim"
        kaynak="/api/admin/denetim"
        canliOlay={['denetim_eklendi']}
        aramaYeri="Uç, hedef ya da kişi ara…"
        satirKimligi={(s) => String(s.id)}
        etkin={acik ? String(acik.id) : null}
        satirTikla={setAcik}
        suzgecler={[
          { anahtar: 'tur', etiket: 'Tür', secenekler: [{ deger: 'yazma', etiket: 'Yazma' }, { deger: 'okuma', etiket: 'Okuma' }] },
          { anahtar: 'durum', etiket: 'Sonuç', secenekler: [{ deger: 'hata', etiket: 'Hatalı' }] },
        ]}
        ekSorgu={{}}
        sutunlar={[
          { anahtar: 'at', baslik: 'Zaman', sirala: true, genislik: '120px', hucre: (s) => <time dateTime={s.at} title={new Date(s.at).toLocaleString('tr-TR')}>{zamanMetni(s.at)}</time> },
          { anahtar: 'yontem', baslik: 'İşlem', genislik: '96px', hucre: (s) => <Rozet ton={durumTonu(s.durum)}>{s.tur === 'okuma' ? 'OKUMA' : s.yontem} {s.durum}</Rozet> },
          { anahtar: 'uc', baslik: 'Uç', sirala: true, genislik: 'minmax(220px,2fr)', hucre: (s) => <code>{s.uc}</code> },
          { anahtar: 'hedef', baslik: 'Hedef', genislik: 'minmax(120px,1fr)' },
          { anahtar: 'kim', baslik: 'Kim', sirala: true, genislik: 'minmax(140px,1fr)' },
          { anahtar: 'sure_ms', baslik: 'Süre', sirala: true, genislik: '72px', hizala: 'sag', gizli: true, hucre: (s) => `${s.sure_ms ?? 0} ms` },
        ]}
      />
      <AyrintiCekmecesi acik={!!acik} kapat={() => setAcik(null)} baslik={acik?.uc || ''} altBaslik={acik ? `${acik.kim} · ${new Date(acik.at).toLocaleString('tr-TR')}` : ''} kayit={acik || undefined} hedef={acik?.hedef || undefined}>
        {acik && <JsonGoruntuleyici veri={acik.ozet} enYuksek={9999} />}
      </AyrintiCekmecesi>
    </>
  );
}
