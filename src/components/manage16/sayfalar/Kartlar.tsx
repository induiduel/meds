import React from 'react';
import { KatalogSayfasi } from '../kit';
import type { SayfaProps } from '../menu';

/** Ezber kartları — veri kataloğu bağdaştırıcısı (/api/admin/k16/katalog/cards). */
export default function Kartlar(_p: SayfaProps) {
  return <KatalogSayfasi varlik="cards" kimlik="ogrenme-kart" baslik="Ezber kartları" silinebilir />;
}
