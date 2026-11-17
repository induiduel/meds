/**
 * Sesli ders metninin "Zengin görünüm" okuma kipi (kullanıcı kararı 2026-11-17).
 * Veri: src/data/zengin_transkript/<key>.json (scripts/uretim/sesli_anlatim/zengin_transkript.py, LLM yok).
 * Bloklar türüne göre çizilir: giriş, madde, açıklama, liste, sıralama, tablo, sınav notu, örnek, alıntı, terim.
 * Canlı takip: her paragraf grubu `.cd-z-p[data-i]` taşır → etkin paragraf vurgusu ve kaydırma sürer, dokununca oraya atlanır.
 * Kelime/cümle vurgusu metnin birebir aynı olmasını ister; bu kipte kapalıdır (normal kipte değişmez).
 */
import React, { memo, useEffect, useState } from 'react';
import { BookOpen, Lightbulb, Quote, Star } from 'lucide-react';
import { ekranYazimi } from '../../services/ekranYazim';
import { cdZenginYukle, type ZBlok, type ZModel } from './canliDersDisaAktar';
import type { CdDetay } from './canliDersStore';
import '../../styles/cd-zengin.css';

const yaz = (t?: string) => ekranYazimi((t || '').replace(/\s*\n+\s*/g, ' ').trim());

/** Ders modeli yüklenir; yoksa null (kip düğmesi hiç görünmez) */
export function useZenginModel(key: string | undefined): ZModel | null {
  const [m, setM] = useState<ZModel | null>(null);
  useEffect(() => {
    let iptal = false;
    setM(null);
    if (key) cdZenginYukle(key).then((x) => { if (!iptal) setM(x); }, () => {});
    return () => { iptal = true; };
  }, [key]);
  return m;
}

function Blok({ b }: { b: ZBlok }) {
  switch (b.t) {
    case 'giris': return <p className="cd-z-giris">{yaz(b.x)}</p>;
    case 'madde': return <ul className={`cd-z-ul sv${b.sv || 1}`}><li>{yaz(b.x)}</li></ul>;
    case 'aciklama': return <p className="cd-z-acik">{yaz(b.x)}</p>;
    case 'liste': return (
      <div className="cd-z-liste"><b>{yaz(b.bas)}</b><ul>{(b.ogeler || []).map((o, j) => <li key={j}>{yaz(o)}</li>)}</ul></div>
    );
    case 'sirali': return (
      <div className="cd-z-sira">{b.bas && <b>{yaz(b.bas)}</b>}<ol>{(b.ogeler || []).map((o, j) => <li key={j}>{yaz(o)}</li>)}</ol></div>
    );
    case 'tablo': return (
      <div className="cd-z-tablo-sar"><table className="cd-z-tablo">
        <thead><tr>{(b.basliklar || []).map((h, j) => <th key={j} scope="col">{yaz(h)}</th>)}</tr></thead>
        <tbody>{(b.satirlar || []).map((r, j) => <tr key={j}>{r.map((c, k) => <td key={k}>{yaz(c)}</td>)}</tr>)}</tbody>
      </table></div>
    );
    case 'sinav': return <aside className="cd-z-kutu is-sinav"><Star aria-hidden /><div><b>Sınavda soruldu</b><p>{yaz(b.x)}</p></div></aside>;
    case 'ornek': return <aside className="cd-z-kutu is-ornek"><Lightbulb aria-hidden /><div><b>Örnek</b><p>{yaz(b.x)}</p></div></aside>;
    case 'alinti': return <blockquote className="cd-z-alinti"><Quote aria-hidden /><p>{yaz(b.x)}</p></blockquote>;
    case 'terim': return <aside className="cd-z-terim"><BookOpen aria-hidden /><p><b>{yaz(b.ad)}</b> {yaz(b.tanim)}</p></aside>;
    default: return b.x ? <p>{yaz(b.x)}</p> : null;
  }
}

/** Zengin metin listesi. p (modeldeki paragraf sırası) → dersteki paragraf kimliği eşlenir; eşlenemezse dokunma kapalı. */
export const ZenginListe = memo(function ZenginListe({ detay, model, onTik }: { detay: CdDetay; model: ZModel; onTik: (i: number) => void }) {
  const pi = detay.bolumler.flatMap((b) => b.paragraflar.filter((p) => p.metin.trim()).map((p) => p.i));
  return (
    <>
      {model.bolumler.map((bl, bi) => {
        // aynı paragraftan gelen ardışık bloklar tek grupta (canlı takip ve dokunma birimi)
        const gruplar: { p: number; bloklar: ZBlok[] }[] = [];
        for (const b of bl.bloklar) {
          const son = gruplar[gruplar.length - 1];
          if (son && son.p === b.p) son.bloklar.push(b); else gruplar.push({ p: b.p, bloklar: [b] });
        }
        return (
          <section key={bi} className="cd-bolum cd-z-bolum" aria-label={bl.baslik}>
            <h2 className="cd-bolum-ad">{yaz(bl.baslik)}</h2>
            {gruplar.map((g) => {
              const i = pi[g.p];
              return (
                <div key={g.p} className="cd-z-p" data-i={i ?? undefined} onClick={i != null ? () => onTik(i) : undefined}>
                  {g.bloklar.map((b, j) => <Blok key={j} b={b} />)}
                </div>
              );
            })}
          </section>
        );
      })}
    </>
  );
});
