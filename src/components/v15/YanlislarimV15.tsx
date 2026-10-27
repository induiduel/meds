import React, { useMemo, useState } from 'react';
import { CheckCircle2, Clock, RotateCcw, Trash2 } from 'lucide-react';
import { PracticeMode } from '../PracticeMode';
import { OGRENILDI_KUTU, useYanlislar, yanlisGruplari, yanlisSil, type YanlisKayit } from '../../services/yanlislarim';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';
import '../../styles/v15/dersler.css';
import '../../styles/v15/soru.css';

/**
 * v15 · Yanlışlarım (tasarım C09). Adres /yanlislarim ↔ /sorular/yanlislarim. Soru çöz / deneme testlerinde yanlış
 * yapılan sorular (services/yanlislarim): Tekrar zamanı (vadesi gelen) · Bekleyen · Öğrenildi. "Hazır olanları çöz"
 * aynı soru ekranını (PracticeMode) bu sorularla açar; cevaplar defteri günceller (doğru → aralık uzar).
 */
type Sekme = 'hazir' | 'bekleyen' | 'ogrenildi';
const kalan = (due: number) => {
  const sa = Math.max(0, Math.round((due - Date.now()) / 3_600_000));
  return sa < 24 ? `${sa} sa sonra` : `${Math.round(sa / 24)} gün sonra`;
};

export default function YanlislarimV15() {
  useYanlislar();
  const g = yanlisGruplari();
  const [sekme, setSekme] = useState<Sekme>(g.hazir.length ? 'hazir' : 'bekleyen');
  const [coz, setCoz] = useState<YanlisKayit[] | null>(null);
  useV15Baslik(coz ? null : { baslik: 'Yanlışlarım', alt: `${g.hazir.length} tekrar zamanı · ${g.bekleyen.length} bekleyen` });
  const liste = g[sekme];
  const sorular = useMemo(() => (coz || []).map((e) => e.q), [coz]);

  if (coz) {
    return <PracticeMode questions={sorular} title="Yanlışlarım" subtitle={`${sorular.length} soru`} onExit={() => setCoz(null)} onOpenContributeModal={() => setCoz(null)} />;
  }

  return (
    <div className="b15 yl15">
      <h1 className="sr-only">Yanlışlarım</h1>
      <div className="v15-seg" role="tablist" aria-label="Yanlışlarım">
        {([['hazir', `Tekrar zamanı (${g.hazir.length})`], ['bekleyen', `Bekleyen (${g.bekleyen.length})`], ['ogrenildi', `Öğrenildi (${g.ogrenildi.length})`]] as [Sekme, string][]).map(([id, t]) => (
          <button key={id} type="button" role="tab" aria-selected={sekme === id} aria-current={sekme === id ? 'page' : undefined} onClick={() => setSekme(id)}>{t}</button>
        ))}
      </div>
      {sekme === 'hazir' && g.hazir.length > 0 && (
        <button type="button" className="v15-btn yl15-coz" onClick={() => setCoz(g.hazir.slice(0, 40))}><RotateCcw aria-hidden /> Hazır olanları çöz ({Math.min(40, g.hazir.length)})</button>
      )}
      {liste.length ? (
        <ul className="b15-list v15-card" role="list">
          {liste.map((e) => (
            <li key={e.q.id} className="yl15-sat">
              <button type="button" className="b15-row" onClick={() => setCoz([e])}>
                <span className={`v15-tile ${e.box >= OGRENILDI_KUTU ? 'is-ok' : sekme === 'hazir' ? 'is-b' : 'is-n'}`}>
                  {e.box >= OGRENILDI_KUTU ? <CheckCircle2 aria-hidden /> : sekme === 'hazir' ? <RotateCcw aria-hidden /> : <Clock aria-hidden />}
                </span>
                <span className="b15-row-t">
                  <b>{e.q.reconstruction?.stem?.slice(0, 110) || 'Soru'}{(e.q.reconstruction?.stem?.length || 0) > 110 ? '…' : ''}</b>
                  <span>{[e.q.discipline?.replace(/^Tıbbi\s+/, ''), e.q.examYear, sekme === 'bekleyen' ? kalan(e.due) : sekme === 'hazir' ? 'şimdi' : 'öğrenildi', e.yanlis > 1 ? `${e.yanlis} kez yanlış` : ''].filter(Boolean).join(' · ')}</span>
                </span>
                {sekme === 'hazir' && <span className="v15-tag is-b">Hazır</span>}
              </button>
              <button type="button" className="v15-ib yl15-sil" onClick={() => yanlisSil(e.q.id)} aria-label="Listeden çıkar" title="Listeden çıkar"><Trash2 aria-hidden /></button>
            </li>
          ))}
        </ul>
      ) : (
        <p className="b15-bos v15-card">
          {sekme === 'hazir' ? 'Şu an tekrar zamanı gelen soru yok.' : sekme === 'bekleyen' ? 'Yanlış yaptığın sorular burada birikir; 48 saat sonra tekrar zamanına geçer.' : 'Tekrarda dört kez doğru yaptığın sorular burada.'}
        </p>
      )}
      <p className="v15-cap">Yanlış yaptığın soru 48 saat sonra yeniden sorulur; doğru yaptıkça aralık uzar (2 · 4 · 8 · 16 gün), dördüncü doğrudan sonra öğrenilmiş sayılır.</p>
    </div>
  );
}
