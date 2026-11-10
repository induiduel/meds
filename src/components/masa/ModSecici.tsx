/** Mod seçici: başlık + kısa tanıtım taşıyan kartlardan tekli seçim. Merkezdeki kurulum yaprağı ve lobi aynı bileşeni kullanır. */
import React from 'react';
import { AlertTriangle, BookOpen, Check, GraduationCap, Swords } from 'lucide-react';
import { UNO_MODLAR, UNO_MOD_GRUPLAR, unoModTanim, unoOyuncuUygun, type OyunTur, type UnoMod } from '../../services/masa/tipler';
import { KartOrnek } from './kabukOrtak';
import { MOD_REHBER } from './uno/kartRehber';
import { tahtaMi } from './tahta/ortak';
import '../../styles/masa/lobi.css';
import '../../styles/masa/uno-rehber.css';

const ZORLUK_AD = ['', 'Kolay', 'Orta', 'Zor'];

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
        { v: false, ad: 'Zorlu', kisa: tahta ? 'Yardımcı işaret yok' : 'İpucu ve otomatik hamle yok', ikon: <Swords size={18} aria-hidden="true" /> },
      ]}
      not={asistan
        ? (tahta ? 'Tahtada konulabilecek noktalar hafifçe gösterilir (9×9).' : 'İpucu, otomatik işleme, en iyi hamle, ıstakayı ve masayı otomatik dizme açık.')
        : tahta ? 'Yardımcı yok: yasal nokta gösterilmez.' : 'İpucu, otomatik işleme ve otomatik dizme kapalı. Masadaki perler yalnız el bitince kendiliğinden dizilir.'}
    />
  );
}

/**
 * Uno mod kataloğu: gruplu (kutu oyunları / ev kuralları / özel) mod kartları; seçili modun tanıtımı ve kural bağlantısı altta.
 * `oyuncuSayisi` verilirse moda uymayan masa için uyarı çıkar (Takım: 4, 6, 8). `kurallarAc`: kural sayfasını o modla açar.
 */
export function UnoModu({ mod, sec, kilitli, oyuncuSayisi, kurallarAc, tema = 'klasik' }: {
  mod: UnoMod; sec: (m: UnoMod) => void; kilitli?: boolean; oyuncuSayisi?: number; kurallarAc?: (m: UnoMod) => void; tema?: string;
}) {
  const secili = unoModTanim(mod);
  const uymaz = oyuncuSayisi !== undefined ? unoOyuncuUygun(mod, oyuncuSayisi) : null;
  return (
    <div className="mk-alan mk-ukat">
      <span className="mk-alan-ad">Uno modu <small className="mk-ukat-sayi">{UNO_MODLAR.length} mod</small></span>
      <div role="radiogroup" aria-label="Uno modu" className="mk-ukat-gruplar">
        {UNO_MOD_GRUPLAR.map((g) => (
          <div key={g.id} className="mk-ukat-grup" role="presentation">
            <div className="mk-ukat-grup-bas"><b>{g.ad}</b><span>{g.alt}</span></div>
            <div className="mk-ukat-kartlar">
              {UNO_MODLAR.filter((m) => m.grup === g.id).map((m) => {
                const on = m.id === mod;
                return (
                  <button key={m.id} type="button" role="radio" aria-checked={on} disabled={kilitli} className={`mk-ukat-kart${on ? ' is-on' : ''}`} onClick={() => sec(m.id)}>
                    <span className="mk-ukat-yelpaze" aria-hidden="true">
                      {m.ornek.slice(0, 3).map(([renk, deger], i, a) => (
                        <span key={i} style={{ transform: `rotate(${(i - (a.length - 1) / 2) * 11}deg) translateY(${Math.abs(i - (a.length - 1) / 2) * 3}px)` }}><KartOrnek renk={renk} deger={deger} tema={tema} boy={34} /></span>
                      ))}
                    </span>
                    <span className="mk-ukat-metin">
                      <span className="mk-ukat-ad"><b>{m.ad}</b>{on && <Check className="mk-mod-tik" size={16} aria-hidden="true" />}</span>
                      <span className="mk-ukat-kisa">{m.kisa}</span>
                      <span className="mk-ukat-cipler">
                        <i>{m.deste} kart</i>
                        <i>{m.cift ? '4/6/8 kişi' : `${m.enAz}–${m.enCok} kişi`}</i>
                        <i className="mk-ukat-zor" role="img" aria-label={`Zorluk: ${ZORLUK_AD[m.zorluk]}`}>{[1, 2, 3].map((z) => <u key={z} className={z <= m.zorluk ? 'is-dolu' : ''} />)}</i>
                      </span>
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
      <div className="mk-ukat-secili" aria-live="polite">
        <div className="mk-ukat-secili-bas">
          <b>{secili.ad}</b>
          <span>{MOD_REHBER[mod].slogan}</span>
        </div>
        <p>{secili.aciklama}</p>
        <div className="mk-ukat-secili-alt">
          <span className="mk-ukat-cipler">
            <i>{secili.deste} kart</i><i>Kişi başı {secili.elKart}</i><i>{secili.cift ? '4, 6 ya da 8 oyuncu' : `${secili.enAz}–${secili.enCok} oyuncu`}</i><i>{ZORLUK_AD[secili.zorluk]}</i>
            {secili.hedef > 0 && <i className="is-hedef">Hedef {secili.hedef} puan</i>}
          </span>
          {kurallarAc && <button type="button" className="mk-cip mk-ukat-kural" onClick={() => kurallarAc(mod)}><BookOpen size={16} aria-hidden="true" /> Kartları ve kuralları gör</button>}
        </div>
        {uymaz && <p className="mk-ipucu is-uyari mk-ukat-uyari" role="alert"><AlertTriangle size={16} aria-hidden="true" /> {uymaz}</p>}
      </div>
    </div>
  );
}
