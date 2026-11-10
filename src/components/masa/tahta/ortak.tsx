/**
 * Tahta oyunlarının (Go, Çizgi Yarışı, XOX) ortak parçaları: kurulum/lobi ayar seçicileri ve oyuncu şeridi.
 * Kurallar ve tasarım planı: meds/docs/TAHTA_OYUNLARI.md
 */
import React from 'react';
import { GO_SURELER, XOX_HEDEF, type BotZorluk, type OdaAyar, type OdaGorunum, type OyunTur } from '../../../services/masa/tipler';
import { Avatar, sadeAd } from '../kabukOrtak';

export const TAHTA: readonly OyunTur[] = ['go', 'cizgi', 'xox'];
export const tahtaMi = (tur: OyunTur) => TAHTA.includes(tur);

const CIZGI_MOD: { kare: 32 | 64 | 96 | 128; ad: string }[] = [
  { kare: 32, ad: 'Hızlı' }, { kare: 64, ad: 'Klasik' }, { kare: 96, ad: 'Uzun' }, { kare: 128, ad: 'Maraton' },
];
const KOMI = [0.5, 5.5, 6.5, 7.5];

/** Ayar seçicileri: merkezde (bota karşı, yerel taslak) ve lobide (kurucu, masa.ayar) aynı bileşen */
export function TahtaAyar({ tur, ayar, degistir, kilitli }: { tur: OyunTur; ayar: Partial<OdaAyar>; degistir: (a: Partial<OdaAyar>) => void; kilitli?: boolean }) {
  const dilim = <T extends string | number>(ad: string, secenek: { v: T; ad: React.ReactNode }[], deger: T | undefined, yaz: (v: T) => void, not?: React.ReactNode) => (
    <div className="mk-alan">
      <span className="mk-alan-ad">{ad}</span>
      <div className="mk-dilim" role="radiogroup" aria-label={ad}>
        {secenek.map((s) => (
          <button key={String(s.v)} type="button" role="radio" aria-checked={deger === s.v} disabled={kilitli} className={deger === s.v ? 'is-on' : ''} onClick={() => yaz(s.v)}>{s.ad}</button>
        ))}
      </div>
      {not && <small className="mk-alan-not">{not}</small>}
    </div>
  );
  const zorluk = dilim<BotZorluk>('Bot gücü', [{ v: 'kolay', ad: 'Kolay' }, { v: 'orta', ad: 'Orta' }, { v: 'zor', ad: 'Zor' }], ayar.botZorluk ?? 'orta', (v) => degistir({ botZorluk: v }),
    (ayar.botZorluk ?? 'orta') === 'kolay' ? 'Bot sık hata yapar; öğrenmek için.' : (ayar.botZorluk ?? 'orta') === 'orta' ? 'Bot ara sıra tehlikeyi kaçırır; yenilebilir.' : 'Bot hata yapmaz (XOX 3×3\'te yenilmez).');
  if (tur === 'go') {
    const h = ayar.goHandikap ?? 0;
    return (
      <>
        {zorluk}
        {dilim('Tahta', [9, 13, 19].map((n) => ({ v: n, ad: `${n}×${n}` })), ayar.goBoyut ?? 9, (v) => degistir({ goBoyut: v as 9 }),
          (ayar.goBoyut ?? 9) === 9 ? 'Hızlı oyun, yeni başlayanlar için.' : (ayar.goBoyut ?? 9) === 13 ? 'Orta uzunlukta oyun.' : 'Tam boy tahta; uzun oyun.')}
        {dilim('Handikap', [0, 2, 3, 4, 5, 6, 7, 8, 9].map((n) => ({ v: n, ad: n === 0 ? 'Yok' : n })), h, (v) => degistir({ goHandikap: v }),
          h ? `Siyah ${h} taşla yıldız noktalarında başlar, beyaz ilk oynar; komi 0,5.` : 'Eşit oyun: siyah başlar.')}
        {!h && dilim('Komi (beyaza)', KOMI.map((k) => ({ v: k, ad: String(k).replace('.', ',') })), ayar.komi ?? 6.5, (v) => degistir({ komi: v }), 'İlk oynamanın avantajını dengeleyen puan.')}
        {dilim('Süre', GO_SURELER.map((s) => ({ v: s.id, ad: s.ad })), ayar.goSure ?? 'yok', (v) => degistir({ goSure: v }),
          (ayar.goSure ?? 'yok') === 'yok' ? 'Süre sınırı yok.' : 'Ana süre bitince byo-yomi başlar: her hamle aralık içinde yapılmalı; aşan bir hak yer, haklar biterse oyun kaybedilir.')}
      </>
    );
  }
  if (tur === 'cizgi') {
    const k = ayar.cizgiKare ?? 64;
    return <>{dilim<'klasik' | 'eglence'>('Mod', [{ v: 'klasik', ad: 'Klasik' }, { v: 'eglence', ad: 'Eğlenceli' }], ayar.cizgiMod ?? 'klasik', (v) => degistir({ cizgiMod: v }),
      (ayar.cizgiMod ?? 'klasik') === 'eglence' ? 'Pistte bonus kareler (+3 adım, yan hakkı, yeniden zar) ve tuzaklar (2 geri).' : 'Yalnız zar ve kapışma.')}{dilim('Yol uzunluğu', CIZGI_MOD.map((m) => ({ v: m.kare, ad: <>{m.kare}<small> {m.ad}</small></> })), k, (v) => degistir({ cizgiKare: v }),
      `${k} satır, ${({ 32: 3, 64: 5, 96: 5, 128: 7 } as const)[k]} sütun; elde ${({ 32: 2, 64: 3, 96: 4, 128: 5 } as const)[k]} yan geçiş hakkı.`)}</>;
  }
  if (tur === 'xox') {
    return <>{zorluk}{dilim('Tahta', ([3, 4, 5, 6] as const).map((n) => ({ v: n, ad: <>{n}×{n}<small> · {XOX_HEDEF[n]}'lü</small></> })), ayar.xoxBoyut ?? 3, (v) => degistir({ xoxBoyut: v }),
      `Yan yana ${XOX_HEDEF[ayar.xoxBoyut ?? 3]} işaret dizen kazanır (yatay, dikey ya da çapraz).`)}</>;
  }
  return null;
}

/** Oyuncu şeridi: avatar, ad, işaret (taş/çizgi rengi), sağda ek bilgi; sırası olan vurgulanır */
export function OyuncuSerit({ oda, id, isaret, sag, alt }: { oda: OdaGorunum; id: string; isaret?: React.ReactNode; sag?: React.ReactNode; alt?: boolean }) {
  const o = oda.oyuncular.find((x) => x.id === id);
  const sira = oda.asama === 'oyun' && oda.oyun?.sira === id;
  return (
    <div className={`tm-serit${alt ? ' is-alt' : ''}${sira ? ' is-sira' : ''}`}>
      <Avatar ad={o?.ad || 'Oyuncu'} foto={o?.foto} bot={o?.bot} id={id} boy={36} />
      <span className="tm-serit-ad">
        <b>{id === oda.ben ? 'Sen' : sadeAd(o?.ad || 'Oyuncu')}</b>
        {isaret && <span className="tm-serit-isaret">{isaret}</span>}
      </span>
      {sira && <span className="tm-sira-hap">{id === oda.ben ? 'Sıra sende' : 'Düşünüyor'}</span>}
      <span className="tm-serit-sag">{sag}</span>
    </div>
  );
}

/** Masadaki rakip: iki kişilik oyunda bakan dışındaki oyuncu */
export const rakipId = (oda: OdaGorunum) => oda.oyuncular.find((o) => o.id !== oda.ben)?.id || oda.oyuncular[1]?.id || '';
export const benOyuncuMu = (oda: OdaGorunum) => oda.oyuncular.some((o) => o.id === oda.ben);
