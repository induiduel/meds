/**
 * Ders özetleri dizini — v12 "Net". Yalnız data-design='v12' iken LectureSummariesView'den çizilir; veri, süzgeç,
 * gruplama ve okuma ilerlemesi oradan gelir (bu dosya yalnız görünümdür). Araç çubuğu ortak PageToolbar'dır.
 * Yapı: araç çubuğu → "Okumaya devam" (en çok 3 sıkı satır, ince ilerleme çubuğu) → kurul/ders grupları: tek panelde
 * sıkı satırlar (ders no · başlık · ders + kurul + hoca · süre / % / Bitti). Okuyucu: summary/SummaryReader (v12 dalı
 * ReaderV12 çerçevesini kullanır). Stil: styles/v12/reader.css (.r12-*).
 */
import React from 'react';
import { Check, ChevronRight, Search } from 'lucide-react';
import type { SummaryMeta } from '../LectureSummariesView';
import type { ReadingMark } from '../summary/readerStore';
import { disciplineClass, disciplineLabel } from '../../utils/discipline';
import '../../styles/v12/reader.css';

export interface SummaryGroupV12 {
  key: string;
  title: string;
  sub: string;
  items: SummaryMeta[];
  d?: string;
}

export interface LectureSummariesV12Props {
  toolbar: React.ReactNode;
  inProgress: { s: SummaryMeta; m: ReadingMark }[];
  showContinue: boolean;
  groups: SummaryGroupV12[];
  filteredCount: number;
  /** Arama ya da süzgeç etkin (düz liste + "n sonuç") */
  filtering: boolean;
  onClearFilters: () => void;
  progress: Record<string, ReadingMark>;
  kurulAll: boolean;
  lessonNo: (id: string, fallback: number) => number;
  onOpen: (s: SummaryMeta) => void;
  reader?: React.ReactNode;
}

const State: React.FC<{ mark?: ReadingMark; minutes: number }> = ({ mark, minutes }) => {
  if (mark && mark.p >= 97)
    return (
      <span className="r12-badge is-ok">
        <Check aria-hidden /> Bitti
      </span>
    );
  if (mark && mark.p >= 2)
    return (
      <span className="r12-row-s is-reading" aria-label={`%${Math.round(mark.p)} okundu`}>
        <span className="r12-bar" aria-hidden>
          <i style={{ transform: `scaleX(${mark.p / 100})` }} />
        </span>
        %{Math.round(mark.p)}
      </span>
    );
  return <span className="r12-row-s">{minutes} dk</span>;
};

export const LectureSummariesV12: React.FC<LectureSummariesV12Props> = ({
  toolbar,
  inProgress,
  showContinue,
  groups,
  filteredCount,
  filtering,
  onClearFilters,
  progress,
  kurulAll,
  lessonNo,
  onOpen,
  reader,
}) => {
  let idx = 0;
  return (
    <div className="r12-page">
      {toolbar}

      {showContinue && inProgress.length > 0 && (
        <section className="r12-group" aria-label="Okumaya devam">
          <header className="r12-group-h">
            <h2>Okumaya devam</h2>
          </header>
          <ul className="r12-list">
            {inProgress.map(({ s, m }) => (
              <li key={s.id} className={disciplineClass(s.discipline)}>
                <button type="button" className="r12-row" onClick={() => onOpen(s)}>
                  <span className="r12-row-main">
                    <span className="r12-row-t">{s.title}</span>
                    <span className="r12-row-m">
                      <i className="r12-dot" aria-hidden />
                      <span>{disciplineLabel(s.discipline)}</span>
                      <span className="is-fill">· ~{Math.max(1, Math.round(s.readingTimeMinutes * (1 - m.p / 100)))} dk kaldı</span>
                    </span>
                  </span>
                  <State mark={m} minutes={s.readingTimeMinutes} />
                  <ChevronRight className="r12-go" aria-hidden />
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      {filteredCount === 0 ? (
        <div className="r12-empty">
          <Search aria-hidden />
          <h3>Bu süzgeçte özet yok</h3>
          <p>Aramayı temizle ya da başka bir kurul seç.</p>
          {filtering && (
            <button type="button" className="r12-btn" onClick={onClearFilters}>
              Süzgeçleri temizle
            </button>
          )}
        </div>
      ) : (
        <div className="r12-groups">
          {groups.map((g) => (
            <section key={g.key} className={`r12-group ${g.d ? disciplineClass(g.d) : ''}`} aria-label={g.title || 'Sonuçlar'}>
              {g.title ? (
                <header className="r12-group-h">
                  {g.d && <i className="r12-dot" aria-hidden />}
                  <h2>{g.title}</h2>
                  {g.sub && <span>{g.sub}</span>}
                  <small>{g.items.length}</small>
                </header>
              ) : (
                filtering && (
                  <p className="r12-result" aria-live="polite">
                    {g.items.length} sonuç
                  </p>
                )
              )}
              <ul className="r12-list">
                {g.items.map((s) => {
                  const no = lessonNo(s.id, ++idx);
                  return (
                    <li key={s.id} className={disciplineClass(s.discipline)}>
                      <button type="button" className="r12-row" onClick={() => onOpen(s)}>
                        <span className="r12-no" aria-hidden>
                          {no}
                        </span>
                        <span className="r12-row-main">
                          <span className="r12-row-t">{s.title}</span>
                          <span className="r12-row-m">
                            <i className="r12-dot" aria-hidden />
                            <span>{disciplineLabel(s.discipline)}</span>
                            {kurulAll && !g.title && <span className="r12-badge">Kurul {s.kurul}</span>}
                            {s.instructor && <span className="is-fill is-opt">· {s.instructor}</span>}
                          </span>
                        </span>
                        <State mark={progress[s.id]} minutes={s.readingTimeMinutes} />
                        <ChevronRight className="r12-go" aria-hidden />
                      </button>
                    </li>
                  );
                })}
              </ul>
            </section>
          ))}
        </div>
      )}

      {reader}
    </div>
  );
};
