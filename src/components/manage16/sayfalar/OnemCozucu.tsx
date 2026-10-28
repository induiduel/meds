import React from 'react';
import { SayfaBasligi, VeriTablosu, Rozet, GorunurlukRozeti, GorunurlukBaglantisi } from '../kit';
import type { SayfaProps } from '../menu';

type Satir = { id: string; dizin: string; onek: string; tur: string; kod: string; no: number; baslik: string; madde: number; kurul: string; ses?: boolean; cikmis?: number; gorunurluk: string };
const TUR: Record<string, string> = { onem: 'Önem', asistan: 'Asistan', cozucu: 'Çözücü' };

/** Öğrenme › Önem ve çözücü: src/data/*_onem|_asistan|_cozucu index envanteri; satırda görünürlük (<tür>:<dizin>/<kod>). */
export default function OnemCozucu({ git }: SayfaProps) {
  return (
    <>
      <SayfaBasligi baslik="Önem ve çözücü" aciklama="Branş × ders envanteri: önem listesi maddesi, sınav asistanı adımı, çözücü sorusu. İçerik üretimi oturumda yapılır; burada yalnız görünürlük." />
      <VeriTablosu<Satir>
        kimlik="ogrenme-onem" kaynak="/api/admin/spot-cozucu" canliOlay={['site_ayar_changed']} aramaYeri="Dizin, kod, başlık…"
        satirKimligi={(x) => `${x.tur}:${x.id}`}
        suzgecler={[
          { anahtar: 'tur', etiket: 'Tür', secenekler: Object.entries(TUR).map(([deger, etiket]) => ({ deger, etiket })) },
          { anahtar: 'kurul', etiket: 'Kurul', secenekler: [1, 2, 3, 4, 5, 6].map((k) => ({ deger: String(k), etiket: String(k) })) },
          { anahtar: 'gorunurluk', etiket: 'Görünürlük', secenekler: [{ deger: 'gizli', etiket: 'Gizli' }, { deger: 'yalniz-yonetici', etiket: 'Yalnız yönetici' }] },
        ]}
        sutunlar={[
          { anahtar: 'tur', baslik: 'Tür', genislik: '80px', hucre: (x) => <Rozet ton={x.tur === 'onem' ? 'vurgu' : x.tur === 'cozucu' ? 'bilgi' : 'notr'}>{TUR[x.tur]}</Rozet> },
          { anahtar: 'kod', baslik: 'Dizin / kod', sirala: true, genislik: 'minmax(150px,1fr)', hucre: (x) => <code>{x.onek}/{x.kod}</code> },
          { anahtar: 'baslik', baslik: 'Ders', sirala: true, genislik: 'minmax(200px,3fr)', hucre: (x) => <span className="m16-kisalt" title={x.baslik}>{x.baslik}</span> },
          { anahtar: 'madde', baslik: 'Sayı', sirala: true, genislik: '64px', hizala: 'sag' },
          { anahtar: 'gorunurluk', baslik: 'Görünürlük', genislik: 'minmax(160px,1fr)', hucre: (x) => <span onClick={(e) => e.stopPropagation()}><GorunurlukBaglantisi anahtar={`${x.tur}:${x.id}`} deger={x.gorunurluk} git={git} />{/* H325 */}</span> },
          { anahtar: 'g', baslik: 'Durum', genislik: '90px', gizli: true, hucre: (x) => <GorunurlukRozeti deger={x.gorunurluk} /> },
        ]}
      />
    </>
  );
}
