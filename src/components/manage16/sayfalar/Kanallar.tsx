import React from 'react';
import { SayfaBasligi, VeriTablosu, Rozet, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';

type Kanal = { kanal: string; n: number; gizli: number; sikayet: number; yazar: number; son: string };

/** Topluluk › Yorumlar ve kanallar — topluluk kanalları ve ders yorum kanalları; satır mesaj moderasyonuna götürür. */
export default function Kanallar({ git }: SayfaProps) {
  return (
    <>
      <SayfaBasligi baslik="Yorumlar ve kanallar" aciklama="Topluluk kanalları ve ders/soru yorum kanalları (sohbet odaları hariç). Bir kanala tıklayınca mesajları moderasyon için açılır." />
      <VeriTablosu<Kanal>
        kimlik="topluluk-kanal" kaynak="/api/admin/topluluk/kanallar" canliOlay={['topluluk_changed', 'topluluk']} boyut={100}
        aramaYeri="Kanal adı…" satirKimligi={(k) => k.kanal} satirTikla={(k) => git(`topluluk/mesaj?s.kanal=${encodeURIComponent(k.kanal)}`)}
        sutunlar={[
          { anahtar: 'kanal', baslik: 'Kanal', sirala: true, genislik: 'minmax(200px,3fr)', hucre: (k) => <code>#{k.kanal}</code> },
          { anahtar: 'n', baslik: 'Mesaj', sirala: true, genislik: '80px', hizala: 'sag' },
          { anahtar: 'yazar', baslik: 'Yazar', genislik: '72px', hizala: 'sag' },
          { anahtar: 'sikayet', baslik: 'Şikâyetli', sirala: true, genislik: '88px', hizala: 'sag', hucre: (k) => (k.sikayet ? <Rozet ton="uyari">{k.sikayet}</Rozet> : '—') },
          { anahtar: 'gizli', baslik: 'Gizli', genislik: '64px', hizala: 'sag' },
          { anahtar: 'son', baslik: 'Son mesaj', sirala: true, genislik: '112px', hucre: (k) => zamanMetni(k.son) },
        ]}
      />
    </>
  );
}
