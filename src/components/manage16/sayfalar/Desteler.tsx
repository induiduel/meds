import React from 'react';
import { KatalogSayfasi } from '../kit';
import { manageAdres, type SayfaProps } from '../menu';

/** Öğrenme › Öğren desteleri: liste, başlık/ders alanlarını düzenle, görünürlük (deste:<id>), çöp kutusuna taşı. */
// H363: desteden bağlı derse dönüş (dersten desteye bağlantı vardı); ders kimliği deste kimliğinin önekidir (icerik.ts dersKatman)
const dersKimligi = (desteId: string) => desteId.match(/k\d+-\d+(?=-)/)?.[0] || '';

export default function Desteler({ git }: SayfaProps) {
  return <KatalogSayfasi varlik="decks" kimlik="ogrenme-desteler" baslik="Öğren desteleri" silinebilir
    ekSekme={(a) => { const d = dersKimligi(a.id); return d ? { id: 'ders', etiket: 'Ders', icerik: <p className="m16-kart">Bağlı ders: <a href={manageAdres(`icerik/dersler/${d}`)} onClick={(e) => { e.preventDefault(); git(`icerik/dersler/${d}`); }}>{d}</a></p> } : null; }}
    aciklama={<>Öğren ekranındaki interaktif ders desteleri. Bir desteyi değiştirdikten sonra deste denetiminin hatasız geçmesi gerekir.{/* H172 */}<span className="m16-kaynak"><code>interactive_learning_decks.json</code></span></>} />;
}
