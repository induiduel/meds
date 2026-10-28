import React from 'react';
import { KatalogSayfasi } from '../kit';
import type { SayfaProps } from '../menu';

/** Hastalıklar — veri kataloğu bağdaştırıcısı (/api/admin/k16/katalog/diseases). */
export default function Hastaliklar(_p: SayfaProps) {
  return <KatalogSayfasi varlik="diseases" kimlik="kaynak-hastalik" baslik="Hastalıklar" silinebilir />;
}
