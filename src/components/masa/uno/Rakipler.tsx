import React from 'react';
import { Check, Handshake, X } from 'lucide-react';
import type { OdaGorunum, UnoGorunum } from '../../../services/masa/tipler';
import { KartGorsel } from './Kart';
import type { Yerlesim } from './yerlesim';

interface Props {
  oda: OdaGorunum;
  oyun: UnoGorunum;
  yer: Yerlesim;
  tema: string;
  etkin: boolean;
  /** Sarsılan (yakalanan) oyuncu ve sayaç */
  sarsilan: { id: string; n: number } | null;
  oneriHedef: string | null;
  onYakala: (id: string) => void;
}

const YELPAZE_EN_COK = 8;
/** Takım renkleri (takım numarasına göre halka) */
export const TAKIM_RENK = ['#ffd21f', '#4fc3f7', '#ff8a65', '#b388ff'];

/** Masanın çevresindeki rakipler: kart yelpazesi (Flip'te öbür yüzleri açık), ad, sıra ışığı, UNO rozeti, mod rozetleri, Yakala düğmesi */
export default function Rakipler({ oda, oyun, yer, tema, etkin, sarsilan, oneriHedef, onYakala }: Props) {
  const benTakim = oyun.oyuncular.find((p) => p.id === oda.ben)?.takim;
  return (
    <div className="um-rakipler" style={{ ['--um-o' as string]: yer.olcek }}>
      {oyun.oyuncular.filter((p) => p.id !== oda.ben && yer.koltuk[p.id]).map((p) => {
        const bilgi = oda.oyuncular.find((o) => o.id === p.id);
        const ad = bilgi?.ad || 'Oyuncu';
        const k = yer.koltuk[p.id];
        const sirada = oyun.sira === p.id && !oyun.bitti;
        const ortak = benTakim !== undefined && p.takim === benTakim;
        const yakala = etkin && !ortak && oyun.yakalanabilir.includes(p.id);
        const goster = Math.min(p.kartSayisi, YELPAZE_EN_COK);
        const mk = yer.mk;
        const adim = goster > 1 ? Math.min(mk * 0.38, (92 * yer.olcek - mk) / (goster - 1)) : 0;
        const egim = Math.min(4.5, 26 / Math.max(1, goster));
        const tehlike = oyun.mod === 'noMercy' && !p.elendi && p.kartSayisi >= 18;
        const durum = p.elendi ? ', elendi' : p.cikti ? ', elini bitirdi, ortağını bekliyor' : '';
        return (
          <div key={p.id} className="um-koltuk-yer" style={{ transform: `translate3d(${k.x}px, ${k.y}px, 0)` }}>
            <div
              key={sarsilan?.id === p.id ? `s${sarsilan.n}` : 's'}
              className={`um-koltuk${yer.kucukKoltuk ? ' um-koltuk-kucuk' : ''}${sirada ? ' um-sirada' : ''}${bilgi && !bilgi.bagli && !bilgi.bot ? ' um-kopuk' : ''}${sarsilan?.id === p.id ? ' um-sars' : ''}${p.elendi ? ' um-elendi' : ''}${p.cikti ? ' um-cikti' : ''}`}
              style={p.takim !== undefined ? { ['--um-takim' as string]: TAKIM_RENK[p.takim % TAKIM_RENK.length] } : undefined}
              aria-label={`${ad}: ${p.kartSayisi} kart${sirada ? ', sırası' : ''}${p.unoDedi ? ', UNO dedi' : ''}${ortak ? ', ortağın' : ''}${durum}${p.guc !== undefined ? (p.guc ? ', gücü yeşil' : ', gücü kırmızı') : ''}`}
              role="group"
            >
              <div className="um-yelpaze" style={{ height: mk * 1.5 }} aria-hidden="true">
                {mk > 0 && Array.from({ length: goster }, (_, i) => {
                  const u = i - (goster - 1) / 2;
                  const arka = p.arka?.[i];
                  return (
                    <div key={i} className="um-yelpaze-kart" style={{ width: mk, marginLeft: -mk / 2, transform: `translate3d(${u * adim}px, ${Math.abs(u) * Math.abs(u) * 0.5}px, 0) rotate(${u * egim}deg)` }}>
                      {arka ? <KartGorsel kart={arka} tema={tema} boy={mk} /> : <KartGorsel tema={tema} boy={mk} kapali />}
                    </div>
                  );
                })}
                <span className={`um-sayi${p.kartSayisi > YELPAZE_EN_COK ? ' um-cok' : ''}${tehlike ? ' um-tehlike' : ''}`}>{p.kartSayisi}{tehlike ? '/25' : ''}</span>
              </div>
              <div className="um-kimlik">
                <span className={`um-avatar${p.takim !== undefined ? ' um-takimli' : ''}`} aria-hidden="true">
                  {bilgi?.foto ? <img className="um-avatar-foto" src={bilgi.foto} alt="" draggable={false} /> : ad.trim().charAt(0).toLocaleUpperCase('tr')}
                </span>
                <span className="um-ad">{ad}</span>
                {p.guc !== undefined && <span className={`um-guc${p.guc ? ' um-acik' : ''}`} aria-hidden="true">{p.guc ? <Check size={11} strokeWidth={3.5} /> : <X size={11} strokeWidth={3.5} />}</span>}
              </div>
              {ortak && <span className="um-ortak-rozet"><Handshake size={12} aria-hidden="true" /> Ortağın</span>}
              {p.elendi && <span className="um-durum-rozet">Elendi</span>}
              {p.cikti && <span className="um-durum-rozet um-iyi">Bitirdi</span>}
              {p.unoDedi && <span className="um-uno-rozet">UNO!</span>}
              {yakala && (
                <button type="button" className={`um-yakala${oneriHedef === p.id ? ' um-oneri' : ''}`} onClick={() => onYakala(p.id)} aria-label={`${ad} UNO demedi: yakala`}>
                  Yakala!
                </button>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
