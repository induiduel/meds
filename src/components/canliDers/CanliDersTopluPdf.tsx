/**
 * Sesli dersler › Toplu PDF: seçilen derslerin metinlerini tek ders "Metni dışa aktar" penceresiyle aynı içerik
 * seçenekleriyle (kapsam, üslup, işaretler, slayt başlıkları, resimler, ekler) indirir. Pencere ve paketleme ortak: components/ui/TopluPdf.
 */
import React, { useMemo, useRef, useState } from 'react';
import { cdDetayGetir, type CdListeDers } from './canliDersStore';
import { cdDersEtiketi, cdKategoriGrupla } from './canliDersKategori';
import { cdAktarBelgesi, cdAktarSecenekOku, cdAktarSecenekYaz, cdAktarVar, type CdAktarSecenek } from './canliDersDisaAktar';
import { CdSecenekAlani } from './CanliDersAktarPencere';
import { TopluPdfDugme as Ortak } from '../ui/TopluPdf';

async function belgeAl(key: string, s: CdAktarSecenek, etiketYedek: string) {
  const detay = await cdDetayGetir(key);
  // "Yalnız önemli yerler" işareti olmayan derste boş belge verir: o ders tüm metinle girer
  const sec = s.kapsam === 'onemli' && !cdAktarVar(detay).vurgu ? { ...s, kapsam: 'tam' as const } : s;
  const bas = sec.basliklar && detay.pdf
    ? await import('./cdSlaytBasliklari').then((m) => m.cdSlaytBasliklari(detay)).catch(() => undefined)
    : undefined;
  return cdAktarBelgesi(detay, cdDersEtiketi(detay) || etiketYedek, sec, bas);
}

export function TopluPdfDugme({ dersler, ad = 'Sesli dersler', dugmeYazi, dugmeSinif = 'cd-btn', onBitti }: { dersler: CdListeDers[]; ad?: string; dugmeYazi?: string; dugmeSinif?: string; onBitti?: (s: { tamam: number; atlanan: number; bicim: 'zip' | 'tek' }) => void }) {
  const ogeler = useMemo(
    () => cdKategoriGrupla(dersler).flatMap(({ kat, dersler: ds }) => ds.map((d) => ({ key: d.key, grup: kat.ad, etiket: cdDersEtiketi(d), baslik: d.baslik }))),
    [dersler],
  );
  const etiketler = useMemo(() => new Map(ogeler.map((o) => [o.key, o.etiket || ''])), [ogeler]);
  const [secenek, setSecenekH] = useState<CdAktarSecenek>(cdAktarSecenekOku);
  const guncel = useRef(secenek);
  guncel.current = secenek;
  const setSecenek = (s: CdAktarSecenek) => { setSecenekH(s); cdAktarSecenekYaz(s); };
  return (
    <Ortak
      ad={ad}
      dugmeYazi={dugmeYazi}
      onBitti={onBitti}
      dugmeSinif={dugmeSinif}
      ogeler={ogeler}
      ekAyar={<CdSecenekAlani deger={secenek} onDegis={setSecenek} ad="tp-cd" />}
      belgeAl={(key) => belgeAl(key, guncel.current, etiketler.get(key) || '')}
      altMetin={(n) => `${n} ders · ${secenek.kapsam === 'onemli' ? 'önemli yerler özeti' : 'konuşma metinleri'}${secenek.vurgu ? ' · işaretli yerler çıkmış, örnek soru ve spotlarla eşleşen önemli bilgiler' : ''}`}
    />
  );
}
