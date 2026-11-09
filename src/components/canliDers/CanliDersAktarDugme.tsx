/** "⋯" menüsünde: sesli ders metnini dışa aktarma penceresini açar (biçim, içerik, bölüm ve PDF görünümü seçenekleri). */
import React from 'react';
import type { CdDetay } from './canliDersStore';
import { SesliMetinAktarDugme } from './CanliDersAktarPencere';

export function MetniAktarDugme({ detay, vurguAcik }: { detay: CdDetay; vurguAcik: boolean }) {
  return <SesliMetinAktarDugme dersKey={detay.key} detay={detay} vurguAcik={vurguAcik} />;
}
