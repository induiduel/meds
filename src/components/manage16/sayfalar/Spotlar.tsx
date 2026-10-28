import React from 'react';
import { KatalogSayfasi } from '../kit';
import type { SayfaProps } from '../menu';

/** Sınav spotları — veri kataloğu bağdaştırıcısı (/api/admin/k16/katalog/spot). */
export default function Spotlar(_p: SayfaProps) {
  return <KatalogSayfasi varlik="spot" kimlik="ogrenme-spot" baslik="Sınav spotları" />;
}
