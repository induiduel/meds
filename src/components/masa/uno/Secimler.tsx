/** Uno mod seçimleri: hedef (rakip), flex yüzü, kapalı kart beyanı ve karar pencereleri. Hepsi masanın üstünde kipli katmandır. */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Check, EyeOff, X, Zap } from 'lucide-react';
import type { OdaGorunum, UnoBeyan, UnoDeger, UnoGorunum, UnoKart, UnoRenk } from '../../../services/masa/tipler';
import { UNO_BEYAN_DEGERLER, UNO_DEGER_AD } from '../../../services/masa/motor/unoAsistan';
import { oyuncuAdi } from '../ortak';
import { KartGorsel, RenkBicimi } from './Kart';
import { renkAl, UNO_SIRA } from './temalar';

/** Açan dokunuşun ardından gelen "hayalet tıklama" seçim sayılmasın; Esc = vazgeç */
function useKatman(onVazgec?: () => void) {
  const acildi = useRef(performance.now());
  useEffect(() => {
    if (!onVazgec) return;
    const tus = (e: KeyboardEvent) => { if (e.key === 'Escape') { e.stopPropagation(); onVazgec(); } };
    window.addEventListener('keydown', tus, true);
    return () => window.removeEventListener('keydown', tus, true);
  }, [onVazgec]);
  return () => performance.now() - acildi.current < 320;
}

/** Ortak pencere: başlık, açıklama, içerik; perdeye dokunmak (varsa) vazgeçer */
export function Pencere({ baslik, alt, children, onVazgec, etiket, genis }: { baslik: React.ReactNode; alt?: React.ReactNode; children: React.ReactNode; onVazgec?: () => void; etiket: string; genis?: boolean }) {
  const taze = useKatman(onVazgec);
  const kokRef = useRef<HTMLDivElement>(null);
  useEffect(() => { kokRef.current?.querySelector<HTMLButtonElement>('button:not(.um-pencere-perde):not(:disabled)')?.focus({ preventScroll: true }); }, []);
  return (
    <div ref={kokRef} className="um-pencere" role="dialog" aria-modal="true" aria-label={etiket}>
      <button type="button" className="um-pencere-perde" tabIndex={-1} aria-label={onVazgec ? 'Vazgeç' : undefined} aria-hidden={onVazgec ? undefined : true} onClick={() => { if (onVazgec && !taze()) onVazgec(); }} />
      {/* Pencereyi açan dokunuşun gecikmeli tıklaması içerideki bir düğmeye düşmesin */}
      <div className={`um-pencere-kutu${genis ? ' um-genis' : ''}`} onClickCapture={(e) => { if (taze()) { e.stopPropagation(); e.preventDefault(); } }}>
        <div className="um-pencere-bas">
          <b>{baslik}</b>
          {onVazgec && <button type="button" className="um-pencere-kapat" onClick={onVazgec} aria-label="Vazgeç, kartı geri al"><X size={20} aria-hidden="true" /></button>}
        </div>
        {alt && <p className="um-pencere-alt">{alt}</p>}
        {children}
      </div>
    </div>
  );
}

/** Hedefli kartlar için rakip seçimi */
export function HedefSecici({ oda, oyun, adaylar, baslik, alt, onSec, onVazgec }: {
  oda: OdaGorunum; oyun: UnoGorunum; adaylar: string[]; baslik: string; alt?: string; onSec: (id: string) => void; onVazgec: () => void;
}) {
  return (
    <Pencere baslik={baslik} alt={alt} onVazgec={onVazgec} etiket={baslik}>
      <div className="um-liste">
        {adaylar.map((id) => {
          const o = oyun.oyuncular.find((p) => p.id === id);
          const bilgi = oda.oyuncular.find((p) => p.id === id);
          const ad = oyuncuAdi(oda, id);
          return (
            <button key={id} type="button" className="um-liste-oge" onClick={() => onSec(id)}>
              <span className="um-avatar" aria-hidden="true">{bilgi?.foto ? <img className="um-avatar-foto" src={bilgi.foto} alt="" draggable={false} /> : ad.trim().charAt(0).toLocaleUpperCase('tr')}</span>
              <span className="um-liste-ad">{ad}</span>
              <span className="um-liste-sayi">{o?.kartSayisi ?? 0} kart{o?.unoDedi ? ' · UNO' : ''}</span>
            </button>
          );
        })}
      </div>
    </Pencere>
  );
}

/** Flex kartı: düz yüz mü, flex yüzü mü */
export function FlexSecici({ kart, tema, duz, flex, onSec, onVazgec }: { kart: UnoKart; tema: string; duz: string; flex: string; onSec: (flex: boolean) => void; onVazgec: () => void }) {
  return (
    <Pencere baslik="Hangi yüzüyle oynayacaksın?" alt="Flex yüzünü kullanınca güç kartın kırmızıya döner." onVazgec={onVazgec} etiket="Flex seçimi">
      <div className="um-flex-secim">
        <KartGorsel kart={kart} tema={tema} boy={64} />
        <div className="um-liste">
          <button type="button" className="um-liste-oge um-iki" onClick={() => onSec(false)}>
            <span className="um-liste-ad">Düz yüz</span><span className="um-liste-acik">{duz}</span>
          </button>
          <button type="button" className="um-liste-oge um-iki um-flexli" onClick={() => onSec(true)}>
            <span className="um-liste-ad"><Zap size={16} aria-hidden="true" /> Flex yüzü</span><span className="um-liste-acik">{flex}</span>
          </button>
        </div>
      </div>
    </Pencere>
  );
}

const beyanYazi = (d: UnoDeger) => (d === 'yon' ? 'Yön' : d === 'pas' ? 'Atlat' : d);
/** Söylenen kart ortadakine uyar mı: aynı renk, aynı değer ya da +4 */
export const beyanUyar = (b: UnoBeyan, oyun: UnoGorunum): boolean => b.deger === '+4' || b.renk === oyun.aktifRenk || b.deger === oyun.ust.deger;

/** Yalancı: kapalı oynanan kartın ne olduğunu söyle (doğru ya da blöf) */
export function BeyanSecici({ kart, oyun, tema, onSec, onVazgec }: { kart: UnoKart; oyun: UnoGorunum; tema: string; onSec: (b: UnoBeyan) => void; onVazgec: () => void }) {
  const palet = renkAl(tema);
  const gercek: UnoBeyan | null = useMemo(() => {
    if (!(UNO_BEYAN_DEGERLER as readonly string[]).includes(kart.deger)) return null;
    return { renk: kart.renk ?? oyun.aktifRenk, deger: kart.deger };
  }, [kart, oyun.aktifRenk]);
  const gercekUyar = !!gercek && beyanUyar(gercek, oyun);
  const [renk, setRenk] = useState<UnoRenk>(gercekUyar ? gercek!.renk : oyun.aktifRenk);
  const [deger, setDeger] = useState<UnoDeger>(gercekUyar ? gercek!.deger : gercek && gercek.deger !== '+4' ? gercek.deger : '1');
  const beyan: UnoBeyan = { renk, deger };
  const uyar = beyanUyar(beyan, oyun);
  const dogru = !!gercek && gercek.deger === deger && (kart.renk === null || kart.renk === renk);
  const ustAd = `${palet[oyun.aktifRenk].ad} ${UNO_DEGER_AD[oyun.ust.deger] ?? ''}`.trim();
  return (
    <Pencere
      baslik="Kapalı oyna: bu kart ne?" etiket="Kapalı kart beyanı" onVazgec={onVazgec} genis
      alt={<>Kartın kapalı konur; ne olduğunu sen söylersin. Söylediğin kart ortadakine (<b>{ustAd}</b>) uymalı: aynı renk, aynı değer ya da +4. İnanmayan “Yalan!” diyebilir.</>}
    >
      <div className="um-beyan">
        <div className="um-beyan-kartlar">
          <figure><KartGorsel kart={kart} tema={tema} boy={58} /><figcaption>Gerçeği</figcaption></figure>
          <span className="um-beyan-ok" aria-hidden="true">→</span>
          <figure><KartGorsel kart={{ renk: deger === '+4' ? null : renk, deger }} tema={tema} boy={58} /><figcaption>Söylediğin</figcaption></figure>
          <span className={`um-beyan-durum ${!uyar ? 'um-kotu' : dogru ? 'um-iyi' : 'um-blof'}`}>
            {!uyar ? 'Ortadakine uymuyor' : dogru ? <><Check size={15} aria-hidden="true" /> Doğruyu söylüyorsun</> : <><EyeOff size={15} aria-hidden="true" /> Blöf yapıyorsun</>}
          </span>
        </div>
        <div className="um-beyan-renkler" role="radiogroup" aria-label={deger === '+4' ? '+4 sonrası geçerli renk' : 'Söylenen renk'}>
          {UNO_SIRA.map((r) => (
            <button key={r} type="button" role="radio" aria-checked={renk === r} className={`um-beyan-renk${renk === r ? ' um-secik' : ''}`} style={{ background: palet[r].ana, color: r === 's' ? '#1d1a16' : '#fff' }} onClick={() => setRenk(r)}>
              <svg viewBox="-10 -10 20 20" aria-hidden="true"><RenkBicimi renk={r} b={5.5} /></svg>
              <span>{palet[r].ad}</span>
            </button>
          ))}
        </div>
        <div className="um-beyan-degerler" role="radiogroup" aria-label="Söylenen değer">
          {UNO_BEYAN_DEGERLER.map((d) => (
            <button key={d} type="button" role="radio" aria-checked={deger === d} aria-label={UNO_DEGER_AD[d]} className={`um-beyan-deger${deger === d ? ' um-secik' : ''}`} onClick={() => setDeger(d)}>{beyanYazi(d)}</button>
          ))}
        </div>
        <div className="um-pencere-dugmeler">
          {gercekUyar && !dogru && <button type="button" className="um-dugme" onClick={() => { setRenk(gercek!.renk); setDeger(gercek!.deger); }}>Doğruyu seç</button>}
          <button type="button" className="um-dugme um-dugme-oyna" disabled={!uyar} onClick={() => onSec(beyan)}>
            <EyeOff size={18} aria-hidden="true" /> <span className="um-dugme-yazi um-hep">“{palet[renk].ad} {beyanYazi(deger)}” de ve oyna</span>
          </button>
        </div>
      </div>
    </Pencere>
  );
}
