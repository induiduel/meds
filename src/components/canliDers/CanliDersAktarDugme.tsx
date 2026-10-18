/** "⋯" menüsünde: sesli ders metnini (önemli yer işaretleriyle) .pdf / .docx / .md / .txt olarak indirir. */
import React from 'react';
import type { CdDetay } from './canliDersStore';
import { cdDersEtiketi } from './canliDersKategori';
import { cdAktarBelgesi } from './canliDersDisaAktar';
import { MetinAktarMenu } from '../MetinAktarMenu';

export function MetniAktarDugme({ detay, vurguAcik }: { detay: CdDetay; vurguAcik: boolean }) {
  const etiket = cdDersEtiketi(detay);
  return <MetinAktarMenu belge={() => cdAktarBelgesi(detay, etiket, vurguAcik)} dosyaAdi={`${etiket} - ${detay.baslik}`} />;
}
