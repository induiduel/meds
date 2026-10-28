import React from 'react';
import { SayfaBasligi, IstatistikIzgara, IstatistikKart, useAdminSorgu } from '../kit';
import type { SayfaProps } from '../menu';
import { MesajTablosu } from './ortak/mesajTablosu';

/** Topluluk › Şikâyetler — topluluk/sohbet mesajı şikâyetleri (soru şikâyetleri Sorular grubunda). */
export default function Sikayetler({ git }: SayfaProps) {
  const oz = useAdminSorgu<any>('/api/admin/topluluk/ozet', { canliOlay: ['topluluk_changed', 'topluluk'] });
  return (
    <>
      <SayfaBasligi baslik="Şikâyetler" aciklama="Öğrencilerin şikâyet ettiği kanal ve sohbet mesajları. 3 şikâyette mesaj öğrencilere kendiliğinden gizlenir; burada yok sayabilir, gizleyebilir ya da silebilirsiniz." />
      <IstatistikIzgara>
        <IstatistikKart etiket="Bekleyen şikâyet" deger={oz.veri?.sikayet ?? '—'} ton={oz.veri?.sikayet ? 'uyari' : 'iyi'} yukleniyor={oz.yukleniyor && !oz.veri} />
        <IstatistikKart etiket="Son 24 saatte mesaj" deger={oz.veri?.mesaj24 ?? '—'} onClick={() => git('topluluk/mesaj')} />
        {/* H373: bekleyen yokken de sonuçlanmış (gizlenmiş) mesajlara geçiş */}
        <IstatistikKart etiket="Gizlenen mesajlar" deger="Aç" alt="Mesajlar › Durum: Gizli" onClick={() => git('topluluk/mesaj?s.durum=gizli')} />
        <IstatistikKart etiket="Kapalı oda" deger={oz.veri?.kapali_oda ?? '—'} onClick={() => git('topluluk/sohbet?s.durum=kapali')} />
      </IstatistikIzgara>
      <MesajTablosu
        kimlik="topluluk-sikayet" kaynak="/api/admin/topluluk/sikayetler" sikayetModu git={git}
        kanalGit={(k) => git(`topluluk/mesaj?s.kanal=${encodeURIComponent(k)}`)}
        suzgecler={[
          { anahtar: 'durum', etiket: 'Durum', secenekler: [{ deger: 'gorunur', etiket: 'Görünür' }, { deger: 'gizli', etiket: 'Gizli' }] },
          { anahtar: 'tur', etiket: 'Yer', secenekler: [{ deger: 'kanal', etiket: 'Kanal' }, { deger: 'oda', etiket: 'Sohbet odası' }] },
        ]}
      />
    </>
  );
}
