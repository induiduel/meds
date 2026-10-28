import React, { useState } from 'react';
import { SayfaBasligi, VeriTablosu, AyrintiCekmecesi, useAdminSorgu, Rozet, Hata, Yukleniyor, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';
import { sureMetni, KisiBag } from './kisiOrtak';

type ISatir = { key: string; kind: string; ad: string; email: string | null; konuSay: number; ozet: { sn: number; haftaSn: number; konu: number; bitti: number; soru: number; son: string | null; modul: Record<string, number> } };

/** Kullanıcılar › Ders ilerlemesi: öğrenci × konu çalışma kaydı (sunucu sayfalı; konular satır açılınca gelir). */
export default function KisiIlerleme({ git }: SayfaProps) {
  const [acik, setAcik] = useState<ISatir | null>(null);
  return (
    <>
      <SayfaBasligi baslik="Ders ilerlemesi" aciklama="Konu başına süre, soru ve bitti durumu (medsoru_calisma_takip_v1). Düzenleme: kişinin 360° › Çalışma sekmesi." />
      <VeriTablosu<ISatir>
        kimlik="kisi-ilerleme" kaynak="/api/admin/people/calisma-matris" canliOlay={['people_changed']} aramaYeri="Ad, e-posta…"
        satirKimligi={(x) => x.key} satirTikla={setAcik} etkin={acik?.key}
        suzgecler={[
          { anahtar: 'modul', etiket: 'Modül', secenekler: ['sesli', 'ogren', 'cozucu', 'onem'].map((m) => ({ deger: m, etiket: m })) },
          { anahtar: 'tur', etiket: 'Tür', secenekler: [{ deger: 'account', etiket: 'Hesap' }, { deger: 'guest', etiket: 'Misafir' }] },
        ]}
        sutunlar={[
          { anahtar: 'ad', baslik: 'Kişi', sirala: true, genislik: 'minmax(180px,2fr)', hucre: (x) => <span className="m16-kisalt"><strong>{x.ad}</strong> <small style={{ color: 'var(--color-ink-3)' }}>{x.email}</small></span> },
          { anahtar: 'sn', baslik: 'Toplam', sirala: true, genislik: '90px', hizala: 'sag', hucre: (x) => sureMetni(x.ozet.sn) },
          { anahtar: 'haftaSn', baslik: '7 gün', sirala: true, genislik: '80px', hizala: 'sag', hucre: (x) => sureMetni(x.ozet.haftaSn) },
          { anahtar: 'bitti', baslik: 'Bitti', sirala: true, genislik: '70px', hizala: 'sag', hucre: (x) => x.ozet.bitti },
          { anahtar: 'konu', baslik: 'Konu', sirala: true, genislik: '70px', hizala: 'sag', hucre: (x) => x.ozet.konu },
          { anahtar: 'modul', baslik: 'Modüller', genislik: 'minmax(160px,1fr)', hucre: (x) => <span style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>{Object.entries(x.ozet.modul || {}).map(([m, s]) => <Rozet key={m}>{m} {sureMetni(s)}</Rozet>)}</span> },
          { anahtar: 'son', baslik: 'Son', sirala: true, genislik: '110px', hucre: (x) => (x.ozet.son ? zamanMetni(x.ozet.son) : '—') },
        ]}
      />
      {acik && <Ayrinti s={acik} kapat={() => setAcik(null)} git={git} />}
    </>
  );
}

function Ayrinti({ s, kapat, git }: { s: ISatir; kapat: () => void; git: SayfaProps['git'] }) {
  // Tek kişinin konuları: aynı uç, arama anahtarla + konular=1
  const d = useAdminSorgu<any>('/api/admin/people/calisma-matris', { sorgu: { sayfa: 0, boyut: 5, q: s.key, konular: 1 } });
  const kisi = d.veri?.ogeler?.find((x: any) => x.key === s.key);
  const konular = kisi ? Object.entries<any>(kisi.konular || {}).map(([id, r]) => ({ id, ...r })).sort((a, b) => String(b.sonAt || '').localeCompare(String(a.sonAt || ''))) : [];
  return (
    <AyrintiCekmecesi acik kapat={kapat} genis baslik={s.ad} altBaslik={<KisiBag anahtar={s.key} git={git}>360° › Çalışma</KisiBag>}>
      {d.hata ? <Hata hata={d.hata} yenile={d.yenile} /> : !d.veri ? <Yukleniyor /> : (
        <ul className="m16-liste">{konular.map((k) => (
          <li key={k.id}><span className="m16-kisalt" title={k.id}>{k.id}</span>{k.durum && <Rozet ton={k.durum === 'bitti' ? 'iyi' : 'notr'}>{k.durum}</Rozet>}<span>{sureMetni(k.sn)} · {k.soru} soru</span></li>
        ))}</ul>
      )}
    </AyrintiCekmecesi>
  );
}
