/** Mod seçici: başlık + kısa tanıtım taşıyan kartlardan tekli seçim. Merkezdeki kurulum yaprağı ve lobi aynı bileşeni kullanır. */
import React from 'react';
import { Check, GraduationCap, Swords } from 'lucide-react';
import { UNO_MODLAR, type OyunTur, type UnoMod } from '../../services/masa/tipler';
import { UNO_MOD_KISA } from './oyunKatalog';
import { tahtaMi } from './tahta/ortak';
import '../../styles/masa/lobi.css';

export interface ModSecenek<T> { v: T; ad: string; kisa: string; ikon?: React.ReactNode }

export function ModSecici<T extends string | number | boolean>({ ad, secenek, deger, sec, kilitli, not, dar }: {
  ad: string; secenek: ModSecenek<T>[]; deger: T; sec: (v: T) => void; kilitli?: boolean; not?: React.ReactNode; dar?: boolean;
}) {
  return (
    <div className="mk-alan">
      <span className="mk-alan-ad">{ad}</span>
      <div className={`mk-modlar${dar ? ' is-dar' : ''}`} role="radiogroup" aria-label={ad}>
        {secenek.map((s) => {
          const on = s.v === deger;
          return (
            <button key={String(s.v)} type="button" role="radio" aria-checked={on} disabled={kilitli} className={`mk-mod${on ? ' is-on' : ''}`} onClick={() => sec(s.v)}>
              <span className="mk-mod-bas">{s.ikon}<b>{s.ad}</b>{on && <Check className="mk-mod-tik" size={16} aria-hidden="true" />}</span>
              <span className="mk-mod-kisa">{s.kisa}</span>
            </button>
          );
        })}
      </div>
      {not && <small className="mk-alan-not">{not}</small>}
    </div>
  );
}

/** Normal / Zorlu: yardımcı asistan açık mı */
export function OyunModu({ tur, asistan, sec, kilitli }: { tur: OyunTur; asistan: boolean; sec: (asistan: boolean) => void; kilitli?: boolean }) {
  const tahta = tahtaMi(tur);
  return (
    <ModSecici
      ad="Zorluk" deger={asistan} sec={sec} kilitli={kilitli} dar
      secenek={[
        { v: true, ad: 'Normal', kisa: tahta ? 'Konulabilecek noktalar gösterilir' : 'İpucu ve otomatik dizme açık', ikon: <GraduationCap size={18} aria-hidden="true" /> },
        { v: false, ad: 'Zorlu', kisa: tahta ? 'Yardımcı işaret yok' : 'Yardımcı yok, her şey elle', ikon: <Swords size={18} aria-hidden="true" /> },
      ]}
      not={asistan
        ? (tahta ? 'Tahtada konulabilecek noktalar hafifçe gösterilir (9×9).' : 'İpucu, otomatik işleme, en iyi hamle, ıstakayı ve masayı otomatik dizme açık.')
        : tahta ? 'Yardımcı yok: yasal nokta gösterilmez.' : 'İpucu, otomatik işleme ve otomatik dizme kapalı. Masadaki perler yalnız el bitince kendiliğinden dizilir.'}
    />
  );
}

export function UnoModu({ mod, sec, kilitli }: { mod: UnoMod; sec: (m: UnoMod) => void; kilitli?: boolean }) {
  return (
    <ModSecici
      ad="Uno modu" deger={mod} sec={sec} kilitli={kilitli}
      secenek={UNO_MODLAR.map((m) => ({ v: m.id, ad: m.ad, kisa: UNO_MOD_KISA[m.id] }))}
      not={UNO_MODLAR.find((m) => m.id === mod)?.aciklama}
    />
  );
}
