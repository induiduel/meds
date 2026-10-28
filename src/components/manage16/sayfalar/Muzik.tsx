import React from 'react';
import { KatalogSayfasi } from '../kit';
import type { SayfaProps } from '../menu';

/** Müzik listesi — veri kataloğu bağdaştırıcısı (/api/admin/k16/katalog/music). */
export default function Muzik(_p: SayfaProps) {
  return <KatalogSayfasi varlik="music" kimlik="kaynak-muzik" baslik="Müzik listesi" silinebilir />;
}
