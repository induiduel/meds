import React from 'react';
import { KatalogSayfasi } from '../kit';
import type { SayfaProps } from '../menu';

/** Öğrenme › Öğren desteleri: liste, başlık/ders alanlarını düzenle, görünürlük (deste:<id>), çöp kutusuna taşı. */
export default function Desteler(_p: SayfaProps) {
  return <KatalogSayfasi varlik="decks" kimlik="ogrenme-desteler" baslik="Öğren desteleri" silinebilir
    aciklama="Kaynak src/data/interactive_learning_decks.json (panel yazımı data/content). İçerik değişikliğinden sonra validate_learning_decks.py 0 HATA olmalı." />;
}
