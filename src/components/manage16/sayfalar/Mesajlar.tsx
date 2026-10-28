import React from 'react';
import { SayfaBasligi } from '../kit';
import type { SayfaProps } from '../menu';
import { MesajTablosu } from './ortak/mesajTablosu';

/** Topluluk › Mesajlar — tüm kanal ve oda mesajlarında arama, gizle/sil. Her liste okuması denetime düşer (kişisel veri). */
export default function Mesajlar({ git }: SayfaProps) {
  const sp = new URLSearchParams(window.location.search);
  const kanal = sp.get('s.kanal');
  const uid = sp.get('s.uid');
  return (
    <>
      <SayfaBasligi baslik="Mesajlar" aciklama="Kanal ve sohbet odası mesajları. Bu sayfadaki her okuma kişisel veri okuması olarak denetim kaydına yazılır."
        eylemler={kanal || uid ? <button type="button" className="m16-btn hayalet" onClick={() => git('topluluk/mesaj', { degistir: true })}>{uid ? 'Kişi süzgecini kaldır' : 'Kanal süzgecini kaldır'}</button> : undefined} />
      <MesajTablosu
        kimlik="topluluk-mesaj" kaynak="/api/admin/topluluk/mesajlar"
        kanalGit={(k) => git(`topluluk/mesaj?s.kanal=${encodeURIComponent(k)}`)}
        git={git}
        suzgecler={[
          { anahtar: 'tur', etiket: 'Yer', secenekler: [{ deger: 'kanal', etiket: 'Kanal' }, { deger: 'oda', etiket: 'Sohbet odası' }] },
          { anahtar: 'durum', etiket: 'Durum', secenekler: [{ deger: 'gorunur', etiket: 'Görünür' }, { deger: 'gizli', etiket: 'Gizli' }] },
          { anahtar: 'sikayet', etiket: 'Şikâyet', secenekler: [{ deger: 'var', etiket: 'Şikâyetli' }] },
          ...(kanal ? [{ anahtar: 'kanal', etiket: 'Kanal', secenekler: [{ deger: kanal, etiket: kanal }] }] : []),
          ...(uid ? [{ anahtar: 'uid', etiket: 'Kişi', secenekler: [{ deger: uid, etiket: uid.slice(0, 12) }] }] : []),
        ]}
      />
    </>
  );
}
