/**
 * Sesli dersler › Toplu PDF: seçilen derslerin konuşma metinlerini tek ders "⋯ › Metni indir" ile aynı biçimde
 * (slayt başlıkları ve önemli yer işaretleriyle) indirir. Pencere ve paketleme ortak: components/ui/TopluPdf.
 */
import React, { useMemo } from 'react';
import { cdDetayGetir, type CdListeDers } from './canliDersStore';
import { cdDersEtiketi, cdKategoriGrupla } from './canliDersKategori';
import { cdAktarBelgesi } from './canliDersDisaAktar';
import { TopluPdfDugme as Ortak, type TopluAyar } from '../ui/TopluPdf';

async function belgeAl(key: string, ayar: TopluAyar, etiketYedek: string) {
  const detay = await cdDetayGetir(key);
  const bas = ayar.basliklar
    ? await import('./cdSlaytBasliklari').then((m) => m.cdSlaytBasliklari(detay)).catch(() => undefined)
    : undefined;
  return cdAktarBelgesi(detay, cdDersEtiketi(detay) || etiketYedek, ayar.vurgu, bas);
}

export function TopluPdfDugme({ dersler, ad = 'Sesli dersler', dugmeYazi, dugmeSinif = 'cd-btn', onBitti }: { dersler: CdListeDers[]; ad?: string; dugmeYazi?: string; dugmeSinif?: string; onBitti?: (s: { tamam: number; atlanan: number; bicim: 'zip' | 'tek' }) => void }) {
  const ogeler = useMemo(
    () => cdKategoriGrupla(dersler).flatMap(({ kat, dersler: ds }) => ds.map((d) => ({ key: d.key, grup: kat.ad, etiket: cdDersEtiketi(d), baslik: d.baslik }))),
    [dersler],
  );
  const etiketler = useMemo(() => new Map(ogeler.map((o) => [o.key, o.etiket || ''])), [ogeler]);
  return (
    <Ortak
      ad={ad}
      dugmeYazi={dugmeYazi}
      onBitti={onBitti}
      dugmeSinif={dugmeSinif}
      ogeler={ogeler}
      secenek={{ vurgu: true, basliklar: true }}
      belgeAl={(key, ayar) => belgeAl(key, ayar, etiketler.get(key) || '')}
      altMetin={(n, ayar) => `${n} ders · konuşma metinleri${ayar.vurgu ? ' · işaretli yerler çıkmış, örnek soru ve spotlarla eşleşen önemli bilgiler' : ''}`}
    />
  );
}
