/** Oyuncu koltuğu: ad, foto/baş harf, taş sayısı, açtı/açmadı, ceza rozetleri (işlek ≠ per), bağlantı, sıra ışıltısı; 101'de atık yığını. */
import React from 'react';
import { Bot, WifiOff } from 'lucide-react';
import type { OdaGorunum, OkeyGorunum, OkeyOyuncuGorunum, Renk } from '../../../services/masa/tipler';
import { TasGorsel } from './Tas';

export const CEZA_BILGI: Record<string, { kisa: string; ad: string }> = {
  islek: { kisa: 'İ', ad: 'İşlek taşı işlemedi' },
  per: { kisa: 'P', ad: 'Açabileceği peri bekletti' },
  islekAtti: { kisa: 'İ', ad: 'İşlek taş attı' },
  okeyAtti: { kisa: '★', ad: 'Okey attı' },
  acmadi: { kisa: 'A', ad: 'Açamadı' },
  gosterge: { kisa: 'G', ad: 'Rakip göstergeyi gösterdi' },
};

export function CezaRozetleri({ o }: { o: OkeyOyuncuGorunum }) {
  if (!o.cezalar.length) return null;
  const say = new Map<string, number>();
  for (const c of o.cezalar) say.set(c.tur, (say.get(c.tur) || 0) + 1);
  return (
    <span className="om-cezalar">
      {[...say].map(([tur, n]) => (
        <span key={tur} className={`om-cezarozet om-cezarozet--${tur === 'per' ? 'per' : tur === 'islek' || tur === 'islekAtti' ? 'islek' : 'diger'}`} title={`${CEZA_BILGI[tur]?.ad || tur} × ${n}`}>
          {CEZA_BILGI[tur]?.kisa || '!'}{n > 1 && <b>{n}</b>}
        </span>
      ))}
    </span>
  );
}

export function AtikYigini({ o, oda, okey, gizli, alinabilir, ben, hedef }: { o: OkeyOyuncuGorunum; oda: OdaGorunum; okey?: { s: number; r: Renk }; gizli: ReadonlySet<number>; alinabilir?: boolean; ben?: boolean; hedef?: boolean }) {
  const a = o.atiklar || [];
  const ust = a[a.length - 1], alt = a[a.length - 2];
  const ustGizli = ust && gizli.has(ust.id);
  return (
    <div className={`om-atik${alinabilir ? ' om-atik--al' : ''}${ben ? ' om-atik--ben' : ''}${hedef ? ' om-atik--hedef' : ''}`} data-om-atik={o.id} {...(ben ? { 'data-om-hedef': 'atik' } : null)} title={ben ? 'Atık alanın' : alinabilir ? 'Yandan al' : 'Atılan taşlar'}>
      {(alt || (ust && ustGizli)) && alt && <span className="om-atik-alt"><TasGorsel tas={alt} renkler={oda.ayar.renkler} tema={oda.ayar.tema} okey={okey} /></span>}
      {ust ? (
        <span className={`om-atik-ust${ustGizli ? ' om-gizli' : ''}`} data-om-atiktas={ust.id} {...(alinabilir ? { 'data-om-src': 'atik', 'data-om-id': ust.id, role: 'button', tabIndex: 0, 'aria-label': 'Yandan al' } : null)}>
          <TasGorsel tas={ust} renkler={oda.ayar.renkler} tema={oda.ayar.tema} okey={okey} />
        </span>
      ) : <span className="om-atik-bos">{ben ? 'At' : ''}</span>}
      {a.length > 1 && <span className="om-atik-say">{a.length}</span>}
    </div>
  );
}

export default function Koltuk({ oda, g, o, yon, sarsil, gizli, alinabilir }: { oda: OdaGorunum; g: OkeyGorunum; o: OkeyOyuncuGorunum; yon: 'ust' | 'sol' | 'sag'; sarsil: boolean; gizli: ReadonlySet<number>; alinabilir: boolean }) {
  const bilgi = oda.oyuncular.find((x) => x.id === o.id);
  const ad = bilgi?.ad || 'Oyuncu';
  const sira = g.sira === o.id && !g.bitti;
  const acti = o.acti || !!o.ciftActi;
  return (
    <div className={`om-koltuk om-koltuk--${yon}${sira ? ' om-koltuk--sira' : ''}${sarsil ? ' om-sars' : ''}${o.takim ? ` om-koltuk--takim${o.takim}` : ''}${bilgi && !bilgi.bagli && !bilgi.bot ? ' om-koltuk--kopuk' : ''}`}>
      <div className="om-koltuk-kart" data-om-koltuk={o.id}>
        <span className="om-avatar">
          {bilgi?.foto ? <img src={bilgi.foto} alt="" draggable={false} /> : <span>{ad.trim().charAt(0).toLocaleUpperCase('tr') || '?'}</span>}
          {bilgi?.bot && <i className="om-avatar-ek" title="Bot"><Bot size={11} /></i>}
          {bilgi && !bilgi.bagli && !bilgi.bot && <i className="om-avatar-ek om-avatar-ek--kopuk" title="Bağlantısı koptu"><WifiOff size={11} /></i>}
        </span>
        <span className="om-koltuk-yazi">
          <span className="om-koltuk-ad"><span className="om-koltuk-adyazi">{ad}</span>{o.takim && <em className="om-takim">{o.takim}</em>}</span>
          <span className="om-koltuk-alt">
            <span className="om-tassay" title="Elindeki taş"><i aria-hidden="true" />{o.tasSayisi}</span>
            {(g.tur as string) !== 'duz' && <span className={`om-acti${acti ? ' om-acti--evet' : ''}`}>{o.ciftActi ? 'Çift açtı' : acti ? 'Açtı' : 'Açmadı'}</span>}
            <CezaRozetleri o={o} />
          </span>
        </span>
        {sira && <span className="om-koltuk-sira">Sırası</span>}
      </div>
      {(g.tur === 'yuzbir' || (g.tur as string) === 'duz') && <AtikYigini o={o} oda={oda} okey={g.okey} gizli={gizli} alinabilir={alinabilir} />}
    </div>
  );
}
