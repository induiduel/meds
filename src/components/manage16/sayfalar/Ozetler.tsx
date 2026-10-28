import React from 'react';
import { KatalogSayfasi } from '../kit';
import type { SayfaProps } from '../menu';

/** Ders özetleri — veri kataloğu bağdaştırıcısı (/api/admin/k16/katalog/summaries). */
export default function Ozetler(_p: SayfaProps) {
  return <KatalogSayfasi varlik="summaries" kimlik="kaynak-ozet" baslik="Ders özetleri" />;
}
