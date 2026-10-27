import React, { useState } from 'react';
import { ChevronRight } from 'lucide-react';
import '../../styles/v15/cikmis.css';

/**
 * v15 · Çıkmışlar girişi (tasarım C07): Yıla göre / Konuya göre seçici ve kartlar (soru sayısı + senin ilerlemen).
 * Veri çıkmış sayfasının kendi listesinden (PastExamsView prepared + çözüm kayıtları); karta dokununca liste o yıla
 * ya da derse süzülür. Hoca bilgisi soru kayıtlarında olmadığı için "Hocaya göre" yok.
 */
export interface CikmisGrup { ad: string; toplam: number; cozulen: number; dogru: number; yeni: number }

export default function CikmisGirisV15({ yillar, dersler, onYil, onDers }: { yillar: CikmisGrup[]; dersler: CikmisGrup[]; onYil: (y: string) => void; onDers: (d: string) => void }) {
  const [kip, setKip] = useState<'yil' | 'ders'>('yil');
  const liste = kip === 'yil' ? yillar : dersler;
  if (!yillar.length && !dersler.length) return null;
  return (
    <section className="cg15" aria-label="Çıkmışlara göz at">
      <div className="v15-seg cg15-seg" role="tablist" aria-label="Gruplama">
        <button type="button" role="tab" aria-selected={kip === 'yil'} aria-current={kip === 'yil' ? 'page' : undefined} onClick={() => setKip('yil')}>Yıla göre</button>
        <button type="button" role="tab" aria-selected={kip === 'ders'} aria-current={kip === 'ders' ? 'page' : undefined} onClick={() => setKip('ders')}>Konuya göre</button>
      </div>
      <div className="cg15-izgara">
        {liste.map((g) => {
          const pct = g.toplam ? Math.round((g.cozulen / g.toplam) * 100) : 0;
          const basari = g.cozulen ? Math.round((g.dogru / g.cozulen) * 100) : 0;
          return (
            <button key={g.ad} type="button" className="cg15-kart v15-card" onClick={() => (kip === 'yil' ? onYil(g.ad) : onDers(g.ad))}>
              <span className="cg15-ust">
                <b>{kip === 'yil' && g.ad === 'Kategorisiz' ? 'Yılı belirsiz' : g.ad.replace(/^Tıbbi\s+/, '')}</b>
                {g.cozulen ? <span className={`v15-tag ${basari >= 60 ? 'is-ok' : 'is-w'}`}>%{basari} doğru</span> : g.yeni ? <span className="v15-tag is-a">{g.yeni} yeni</span> : null}
              </span>
              <span className="v15-cap">{g.toplam.toLocaleString('tr-TR')} soru{g.cozulen ? ` · ${g.cozulen} çözdün` : ''}</span>
              <span className="v15-bar" aria-label={`%${pct} çözüldü`}><span style={{ width: `${pct}%` }} /></span>
              <ChevronRight className="cg15-ok" aria-hidden />
            </button>
          );
        })}
      </div>
      <h2 className="v15-cap cg15-alt">Tüm sorular</h2>
    </section>
  );
}
