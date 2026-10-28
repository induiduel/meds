import React from 'react';
import { KatalogSayfasi } from '../kit';
import type { SayfaProps } from '../menu';

/** Sağlık Bakanlığı kaynakları — veri kataloğu bağdaştırıcısı (/api/admin/k16/katalog/saglik). */
export default function SaglikBakanligi(_p: SayfaProps) {
  return <KatalogSayfasi varlik="saglik" kimlik="kaynak-saglik" baslik="Sağlık Bakanlığı kaynakları" />;
}
