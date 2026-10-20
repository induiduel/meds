/** "⋯" menüsünde: sesli ders metnini (önemli yer işaretleriyle) .pdf / .docx / .md / .txt olarak indirir. */
import React from 'react';
import type { CdDetay } from './canliDersStore';
import { cdDersEtiketi } from './canliDersKategori';
import { cdAktarBelgesi } from './canliDersDisaAktar';
import { MetinAktarMenu } from '../MetinAktarMenu';

export function MetniAktarDugme({ detay, vurguAcik }: { detay: CdDetay; vurguAcik: boolean }) {
  const etiket = cdDersEtiketi(detay);
  return <MetinAktarMenu belge={async (bicim) => {
    // PDF/DOCX: slayt başlıkları alt başlık olur (PDF açılamazsa başlıksız sürer)
    const basliklar = bicim === 'txt' ? undefined : await import('./cdSlaytBasliklari').then((m) => m.cdSlaytBasliklari(detay)).catch(() => undefined);
    return cdAktarBelgesi(detay, etiket, vurguAcik, basliklar);
  }} dosyaAdi={`${etiket} - ${detay.baslik}`} />;
}
