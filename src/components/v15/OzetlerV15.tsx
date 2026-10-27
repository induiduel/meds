import React from 'react';
import { BookOpen, Check, Search, X } from 'lucide-react';
import type { SummaryMeta } from '../LectureSummariesView';
import type { ReadingMark } from '../summary/readerStore';
import { disciplineLabel } from '../../utils/discipline';
import { useV15Baslik } from './baslik';
import { Halka } from './Halka';
import '../../styles/v15/ogren.css';
import '../../styles/v15/ozet.css';

/**
 * v15 · Ders özetleri (tasarım sistemi v15.4 › b2ozet). Yalnız görünüm: veri, süzgeç, gruplama ve okuma ilerlemesi
 * LectureSummariesView'den gelir. Üstte kaldığın özet (büyük %), kurul + dal çipleri, altta kendi alanında kayan liste.
 */
export interface OzetlerV15Props {
  inProgress: { s: SummaryMeta; m: ReadingMark }[];
  groups: { key: string; title: string; sub: string; items: SummaryMeta[] }[];
  progress: Record<string, ReadingMark>;
  toplam: number;
  bitti: number;
  sorgu: string;
  setSorgu: (v: string) => void;
  kurul: number | 'all';
  kurullar: { id: string; label: string }[];
  setKurul: (v: string) => void;
  dallar: string[];
  dal: string;
  setDal: (v: string) => void;
  onOpen: (s: SummaryMeta) => void;
  reader?: React.ReactNode;
}

export default function OzetlerV15(p: OzetlerV15Props) {
  const [araAcik, setAraAcik] = React.useState(!!p.sorgu);
  useV15Baslik({ baslik: 'Ders özetleri', alt: `${p.toplam} özet${p.bitti ? ` · ${p.bitti} bitti` : ''}` });
  const devam = !p.sorgu && p.inProgress[0];
  const say = p.groups.reduce((n, g) => n + g.items.length, 0);

  return (
    <div className="oz15">
      <h1 className="sr-only">Ders özetleri</h1>
      {devam && (
        <button type="button" className="oz15-devam v15-card" onClick={() => p.onOpen(devam.s)}>
          <span className="v15-label">Kaldığın özet</span>
          <b>{devam.s.title}</b>
          <span className="v15-cap">{disciplineLabel(devam.s.discipline)} · {devam.s.readingTimeMinutes} dk</span>
          <span className="oz15-pct">%{Math.round(devam.m.p)}</span>
          <span className="v15-bar" aria-hidden><span style={{ width: `${devam.m.p}%` }} /></span>
        </button>
      )}
      <div className="o15-ust">
        {araAcik ? (
          <label className="o15-ara">
            <Search aria-hidden />
            <input autoFocus type="search" value={p.sorgu} onChange={(e) => p.setSorgu(e.target.value)} placeholder="Ders, konu ya da hoca ara" aria-label="Özetlerde ara" />
            <button type="button" className="v15-ib" onClick={() => { p.setSorgu(''); setAraAcik(false); }} aria-label="Aramayı kapat"><X aria-hidden /></button>
          </label>
        ) : (
          <div className="o15-cipler v15-hscroll" role="toolbar" aria-label="Süzgeç">
            {p.kurullar.map((k) => (
              <button key={k.id} type="button" className={`o15-cip${String(p.kurul) === k.id ? ' is-on' : ''}`} aria-pressed={String(p.kurul) === k.id} onClick={() => p.setKurul(k.id)}>{k.label}</button>
            ))}
          </div>
        )}
        {!araAcik && <button type="button" className="v15-ib" onClick={() => setAraAcik(true)} aria-label="Ara"><Search aria-hidden /></button>}
      </div>
      {p.dallar.length > 1 && !araAcik && (
        <div className="o15-cipler v15-hscroll oz15-dal" role="toolbar" aria-label="Ders">
          {['all', ...p.dallar].map((d) => (
            <button key={d} type="button" className={`o15-cip${p.dal === d ? ' is-on' : ''}`} aria-pressed={p.dal === d} onClick={() => p.setDal(d)}>{d === 'all' ? 'Tüm dersler' : disciplineLabel(d)}</button>
          ))}
        </div>
      )}
      <div className="oz15-alan">
        {say ? p.groups.map((g) => (
          <section key={g.key} aria-label={g.title || 'Sonuçlar'}>
            {g.title && <h2 className="v15-h2 oz15-gb">{g.title}<span className="v15-cap"> {g.items.length}</span></h2>}
            <ul className="oz15-izgara" role="list">
              {g.items.map((s) => {
                const m = p.progress[s.id];
                const pct = Math.round(m?.p || 0);
                const bitti = pct >= 97;
                return (
                  <li key={s.id}>
                    <button type="button" className="oz15-kart v15-card" onClick={() => p.onOpen(s)}>
                      <span className={`v15-tile ${bitti ? 'is-ok' : 'is-n'}`}>{bitti ? <Check aria-hidden /> : <BookOpen aria-hidden />}</span>
                      <span className="oz15-kt">
                        <b>{s.title}</b>
                        <span>{[disciplineLabel(s.discipline), s.instructor, `${s.readingTimeMinutes} dk`].filter(Boolean).join(' · ')}</span>
                      </span>
                      {pct >= 2 && <Halka pct={pct} etiket={bitti ? 'Okundu' : `%${pct} okundu`} />}
                    </button>
                  </li>
                );
              })}
            </ul>
          </section>
        )) : <p className="b15-bos v15-card">Bu süzgeçte özet yok.</p>}
      </div>
      {p.reader}
    </div>
  );
}
