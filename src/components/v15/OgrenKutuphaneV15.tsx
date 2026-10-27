import React, { useDeferredValue, useMemo, useState } from 'react';
import { ChevronRight, Layers, RotateCcw, Search, X } from 'lucide-react';
import { deckName, type DeckCatalogEntry } from '../../data/deckStore';
import { useReviewCounts } from '../../hooks/useReviewCounts';
import { branchOf, isPublished, kurulOf, orderOf, schedOf, stateOf, urlKurulSuzgeci } from '../learn/LearnLibrary';
import type { LearnLibraryV12Props } from '../v12/LearnLibraryV12';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';

/**
 * v15 · Öğren desteleri (tasarım sistemi v15 › B05). Veri ve kurallar v12 kitaplığıyla aynı (LearnLibrary yardımcıları);
 * yalnız düzen yeni: başlık üst barda, tek satır çip (durum + branş, kenarı solan kaydırma), arama, kart ızgarası
 * (telefon 1 · tablet 2 · PC 3 sütun). Kart: deste simgesi, durum rozeti (%n · Bitti · Yeni), ad, slayt sayısı.
 * Izgara kendi alanında kayar; sayfa ekrana sabit.
 */
type Durum = 'all' | 'active' | 'done';
const DURUM: [Durum, string][] = [['all', 'Tümü'], ['active', 'Devam eden'], ['done', 'Biten']];
const SAYFA = 60;

export const OgrenKutuphaneV15: React.FC<LearnLibraryV12Props> = ({ decks: all, progress, isAdmin, onOpen, versions, onOpenReview, onRestart, actions }) => {
  const review = useReviewCounts();
  const [ara, setAra] = useState('');
  const [araAcik, setAraAcik] = useState(false);
  const q = useDeferredValue(ara).trim().toLocaleLowerCase('tr-TR');
  const [durum, setDurum] = useState<Durum>('all');
  const [dal, setDal] = useState('all');
  const [kurul] = useState(urlKurulSuzgeci);
  const [sinir, setSinir] = useState(SAYFA);

  const yayinda = (d: DeckCatalogEntry) => isPublished(d) || !!versions?.[d.id];
  const kapsam = useMemo(() => {
    const l = all.filter(yayinda);
    return (l.length || isAdmin ? l : all)
      .filter((d) => kurul === 'all' || kurulOf(d) === kurul)
      .slice()
      .sort((a, b) => (schedOf(a)?.s ?? 1e4 + orderOf(a)) - (schedOf(b)?.s ?? 1e4 + orderOf(b)) || deckName(a).localeCompare(deckName(b), 'tr'));
  }, [all, isAdmin, versions, kurul]); // eslint-disable-line react-hooks/exhaustive-deps

  const dallar = useMemo(() => {
    const m = new Map<string, number>();
    kapsam.forEach((d) => m.set(branchOf(d), (m.get(branchOf(d)) || 0) + 1));
    return [...m.entries()].sort((a, b) => b[1] - a[1]);
  }, [kapsam]);

  const gorunen = useMemo(
    () =>
      kapsam.filter(
        (d) =>
          (dal === 'all' || branchOf(d) === dal) &&
          (durum === 'all' || stateOf(d, progress).status === durum) &&
          (!q || [d.title, d.shortTitle, d.discipline, d.instructor].join(' ').toLocaleLowerCase('tr-TR').includes(q)),
      ),
    [kapsam, dal, durum, q, progress],
  );
  const sayi = useMemo(() => {
    const c = { all: 0, active: 0, done: 0 };
    kapsam.forEach((d) => {
      if (dal !== 'all' && branchOf(d) !== dal) return;
      c.all += 1;
      const s = stateOf(d, progress).status;
      if (s !== 'new') c[s] += 1;
    });
    return c;
  }, [kapsam, dal, progress]);

  useV15Baslik({ baslik: 'Öğren desteleri', alt: `${kurul === 'all' ? 'Tüm kurullar' : kurul} · ${kapsam.length} deste` });

  return (
    <div className="o15">
      <h1 className="sr-only">Öğren desteleri</h1>
      <div className="o15-ust">
        {araAcik ? (
          <label className="o15-ara">
            <Search aria-hidden />
            <input autoFocus type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Deste, ders ya da hoca ara" aria-label="Destelerde ara" />
            <button type="button" className="v15-ib" onClick={() => { setAra(''); setAraAcik(false); }} aria-label="Aramayı kapat"><X aria-hidden /></button>
          </label>
        ) : (
          <div className="o15-cipler v15-hscroll" role="toolbar" aria-label="Süzgeç">
            {DURUM.map(([id, t]) => (
              <button key={id} type="button" className={`o15-cip${durum === id ? ' is-on' : ''}`} aria-pressed={durum === id} onClick={() => setDurum(id)}>
                {t}{id !== 'all' && sayi[id] ? <span>{sayi[id]}</span> : null}
              </button>
            ))}
            <span className="o15-ayr" aria-hidden />
            {dallar.map(([g, n]) => (
              <button key={g} type="button" className={`o15-cip${dal === g ? ' is-on' : ''}`} aria-pressed={dal === g} onClick={() => setDal(dal === g ? 'all' : g)}>
                {g}<span>{n}</span>
              </button>
            ))}
          </div>
        )}
        {!araAcik && (
          <button type="button" className="v15-ib o15-arab" onClick={() => setAraAcik(true)} aria-label="Ara"><Search aria-hidden /></button>
        )}
        {actions && <span className="o15-eylem">{actions}</span>}
      </div>

      {review.total.due > 0 && onOpenReview && (
        <button type="button" className="o15-hata" onClick={() => onOpenReview()}>
          <span className="v15-tile is-b"><RotateCcw aria-hidden /></span>
          <span className="o15-hata-t"><b>Hata defteri</b><span>{review.total.due} kart tekrar zamanı geldi</span></span>
          <ChevronRight className="v15-chev" aria-hidden />
        </button>
      )}

      <div className="o15-alan">
        {gorunen.length ? (
          <ul className="o15-izgara" role="list">
            {gorunen.slice(0, sinir).map((d) => {
              const s = stateOf(d, progress);
              return (
                <li key={d.id}>
                  <button type="button" className="o15-kart v15-card" onClick={() => onOpen(d.id)} title={d.title}>
                    <span className="o15-kart-ust">
                      <span className="v15-tile is-c"><Layers aria-hidden /></span>
                      <span className={`v15-tag ${s.status === 'done' ? 'is-ok' : s.status === 'active' ? 'is-a' : ''}`}>
                        {s.status === 'done' ? 'Bitti' : s.status === 'active' ? `%${s.pct}` : 'Yeni'}
                      </span>
                    </span>
                    <b className="o15-ad">{deckName(d, false)}</b>
                    <span className="o15-alt">
                      {[branchOf(d), d.slideCount ? `${d.slideCount} slayt` : '', s.status === 'active' ? `adım ${s.last}` : ''].filter(Boolean).join(' · ')}
                    </span>
                    {s.status === 'active' && (
                      <span className="v15-bar" aria-hidden><span style={{ width: `${s.pct}%` }} /></span>
                    )}
                  </button>
                  {s.status === 'done' && onRestart && (
                    <button type="button" className="o15-tekrar" onClick={() => onRestart(d.id)} aria-label={`${deckName(d, false)}: baştan tekrar et`} title="Baştan tekrar et">
                      <RotateCcw aria-hidden />
                    </button>
                  )}
                </li>
              );
            })}
          </ul>
        ) : (
          <p className="o15-bos v15-card">
            {q ? `“${ara}” için deste bulunamadı.` : 'Bu süzgeçte deste yok.'}{' '}
            {(durum !== 'all' || dal !== 'all' || q) && (
              <button type="button" className="o15-temizle" onClick={() => { setDurum('all'); setDal('all'); setAra(''); }}>Süzgeçleri temizle</button>
            )}
          </p>
        )}
        {gorunen.length > sinir && (
          <button type="button" className="v15-btn is-soft o15-daha" onClick={() => setSinir((n) => n + SAYFA)}>
            {gorunen.length - sinir} deste daha göster
          </button>
        )}
      </div>
    </div>
  );
};
