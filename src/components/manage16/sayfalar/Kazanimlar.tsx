import React from 'react';
import { KatalogSayfasi } from '../kit';
import type { SayfaProps } from '../menu';

/** Kazanımlar — veri kataloğu bağdaştırıcısı (/api/admin/k16/katalog/kazanim). */
export default function Kazanimlar(_p: SayfaProps) {
  return <KatalogSayfasi varlik="kazanim" kimlik="ogrenme-kazanim" baslik="Kazanımlar" />;
}
