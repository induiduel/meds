import React from 'react';
import { KatalogSayfasi } from '../kit';
import type { SayfaProps } from '../menu';

/** Öğrenme › Öğren desteleri: liste, başlık/ders alanlarını düzenle, görünürlük (deste:<id>), çöp kutusuna taşı. */
export default function Desteler(_p: SayfaProps) {
  return <KatalogSayfasi varlik="decks" kimlik="ogrenme-desteler" baslik="Öğren desteleri" silinebilir
    aciklama={<>Öğren ekranındaki interaktif ders desteleri. Bir desteyi değiştirdikten sonra deste denetiminin hatasız geçmesi gerekir.{/* H172 */}<span className="m16-kaynak"><code>interactive_learning_decks.json</code></span></>} />;
}
