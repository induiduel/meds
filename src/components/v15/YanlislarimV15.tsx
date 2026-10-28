import React, { useMemo, useState } from 'react';
import { CheckCircle2, Clock, RotateCcw, Trash2 } from 'lucide-react';
import { PracticeMode } from '../PracticeMode';
import { OGRENILDI_KUTU, useYanlislar, yanlisGeriKoy, yanlisGruplari, yanlisSil, type YanlisKayit } from '../../services/yanlislarim';
import { geriAlinabilir } from '../ui/Toast';
import { navigateTo } from '../../router';
import { useV15Baslik } from './baslik';
import SoruSuzgecV15, { suzgecUyar, type SuzgecDegeri, type SuzgecYonu } from './SoruSuzgecV15';
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
  const [suz, setSuz] = useState<SuzgecDegeri>({});
  const ham = g[sekme];
  const dersOf = (e: YanlisKayit) => e.q.discipline?.replace(/^Tıbbi\s+/, '') || 'Diğer';
  const yilOf = (e: YanlisKayit) => String(e.q.examYear || 'Bilinmiyor');
  const yonler: SuzgecYonu[] = useMemo(() => {
    const say = (f: (e: YanlisKayit) => string) => { const m = new Map<string, number>(); ham.forEach((e) => { const v = f(e); m.set(v, (m.get(v) || 0) + 1); }); return [...m.entries()].sort((a, b) => b[1] - a[1]).map(([deger, n]) => ({ deger, n })); };
    return [{ id: 'ders', ad: 'Ders', secenekler: say(dersOf) }, { id: 'yil', ad: 'Yıl', secenekler: say(yilOf) }, { id: 'neden', ad: 'Neden', secenekler: say((e) => e.neden || 'Belirtilmedi') }];
  }, [ham]);
  const liste = ham.filter((e) => suzgecUyar(suz, 'ders', dersOf(e)) && suzgecUyar(suz, 'yil', yilOf(e)) && suzgecUyar(suz, 'neden', e.neden || 'Belirtilmedi'));
  const sorular = useMemo(() => (coz || []).map((e) => e.q), [coz]);

  if (coz) {
    return <PracticeMode questions={sorular} title="Yanlışlarım" subtitle={`${sorular.length} soru`} onExit={() => setCoz(null)} onOpenContributeModal={() => setCoz(null)} />;
  }

  return (
    <div className="b15 yl15">
      <h1 className="sr-only">Yanlışlarım</h1>
      {/* H160: "Tekrar zamanı (0)" telefonda iki satıra bölünüyordu; sekme adı kısa, satır kırılmaz */}
      <div className="v15-seg yl15-seg" role="tablist" aria-label="Yanlışlarım">
        {([['hazir', `Tekrar (${g.hazir.length})`], ['bekleyen', `Bekleyen (${g.bekleyen.length})`], ['ogrenildi', `Öğrenildi (${g.ogrenildi.length})`]] as [Sekme, string][]).map(([id, t]) => (
          <button key={id} type="button" role="tab" aria-selected={sekme === id} aria-current={sekme === id ? 'page' : undefined} onClick={() => setSekme(id)}>{t}</button>
        ))}
      </div>
      {sekme === 'hazir' && liste.length > 0 && (
        <button type="button" className="v15-btn yl15-coz" onClick={() => setCoz(liste.slice(0, 40))}><RotateCcw aria-hidden /> Hazır olanları çöz ({Math.min(40, liste.length)})</button>
      )}
      <SoruSuzgecV15 yonler={yonler} deger={suz} onChange={setSuz} kayitAnahtari="yanlislarim" sonuc={liste.length}>
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
                  <span>{[e.q.discipline?.replace(/^Tıbbi\s+/, ''), e.q.examYear, sekme === 'bekleyen' ? kalan(e.due) : sekme === 'hazir' ? 'şimdi' : 'öğrenildi', e.yanlis > 1 ? `${e.yanlis} kez yanlış` : '', e.neden || ''].filter(Boolean).join(' · ')}</span>
                </span>
                {sekme === 'hazir' && <span className="v15-tag is-b">Hazır</span>}
              </button>
              <button type="button" className="v15-ib yl15-sil" onClick={() => { const yedek = e; yanlisSil(e.q.id); geriAlinabilir('Listeden çıkarıldı', () => yanlisGeriKoy(yedek)); }} aria-label="Listeden çıkar" title="Listeden çıkar"><Trash2 aria-hidden /></button>
            </li>
          ))}
        </ul>
      ) : (
        <p className="b15-bos v15-card">
          {ham.length && !liste.length ? 'Süzgece uyan soru yok; süzgeci gevşet ya da temizle.' : sekme === 'hazir' ? 'Şu an tekrar zamanı gelen soru yok.' : sekme === 'bekleyen' ? 'Yanlış yaptığın sorular burada birikir; 48 saat sonra tekrar zamanına geçer.' : 'Tekrarda dört kez doğru yaptığın sorular burada.'}
          {/* H160: boş durumda soru çözmeye götüren eylem (süzgeç boşaltıyorsa gerekmez) */}
          {!ham.length && <button type="button" className="v15-btn is-soft" onClick={() => navigateTo('/sorular')}>Soru çözmeye başla</button>}
        </p>
      )}
      </SoruSuzgecV15>
      <p className="v15-cap">Yanlış yaptığın soru 48 saat sonra yeniden sorulur; doğru yaptıkça aralık uzar (2 · 4 · 8 · 16 gün), dördüncü doğrudan sonra öğrenilmiş sayılır.</p>
    </div>
  );
}
