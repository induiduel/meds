import React, { useCallback, useEffect, useId, useMemo, useState } from 'react';
import { ChevronDown, Highlighter as PenIcon } from 'lucide-react';
import { HL_COLORS, type HlColor } from '../ui/Highlighter';
import { KAT, Zengin, type Kategori, type Spot as ExamSpot, type Veri } from '../spots/spotsShared';
import '../../styles/summary.css';

/**
 * Okuyucunun sağ paneli (v10): "Spotlar · n" (bu dersin sınav spotları, src/data/exam_spots_k1.json — tembel)
 * ve "Notlarım · n" (bu özette kalemle işaretlenen yerler). Masaüstünde (≥1180) sağ sütunda, daha dar ekranda ve
 * akış düzeninde makalenin altında aynı bileşen çizilir. Stil: styles/summary.css (.sr-panel*, .sr-xs*).
 */

// ── Sınav spotları: dosya bir kez yüklenir, ders ders süzülür ──────────────────────────────────────
let spotsP: Promise<Veri | null> | null = null;
const loadSpots = () =>
  (spotsP ||= import('../../data/exam_spots_k1.json')
    .then((m) => ((m as any).default ?? m) as unknown as Veri)
    .catch(() => {
      spotsP = null;
      return null;
    }));

const fold = (s: string) => s.toLocaleLowerCase('tr').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();

/** Ders eşleşmesi: önce kimlik (k1-NN-…), olmazsa başlığın sadeleştirilmiş hâli. Eşleşme yoksa spot gösterilmez. */
export function useLessonSpots(lesson: { id: string; kurul: number; title: string }): ExamSpot[] | null | undefined {
  // undefined: yükleniyor · null: bu ders için spot yok
  const [spots, setSpots] = useState<ExamSpot[] | null | undefined>(lesson.kurul === 1 ? undefined : null);
  useEffect(() => {
    if (lesson.kurul !== 1) {
      setSpots(null);
      return;
    }
    let live = true;
    setSpots(undefined);
    loadSpots().then((v) => {
      if (!live) return;
      const t = fold(lesson.title);
      const ders = v?.dersler.find((d) => d.id === lesson.id) || v?.dersler.find((d) => fold(d.baslik) === t);
      const list = ders ? v!.spotlar.filter((s) => s.ders === ders.no).sort((a, b) => b.onem - a.onem) : [];
      setSpots(list.length ? list : null);
    });
    return () => {
      live = false;
    };
  }, [lesson.id, lesson.kurul, lesson.title]);
  return spots;
}

// ── Kalem işaretleri (ui/Highlighter.tsx · STORE_KEY ile aynı anahtar; yalnız okunur) ──────────────
export interface ScopeMark {
  id: string;
  color: HlColor;
  start: number;
  end: number;
  text: string;
}
const HL_KEY = 'medsoru_highlights_v1';
const readMarks = (scope: string): ScopeMark[] => {
  try {
    const all = JSON.parse(localStorage.getItem(HL_KEY) || '{}');
    return Array.isArray(all[scope]) ? [...all[scope]].sort((a: ScopeMark, b: ScopeMark) => a.start - b.start) : [];
  } catch {
    return [];
  }
};

/** İşaretler kalem bırakılınca yazılır; okuyucu dokunuş/tuş sonrası `refresh` çağırır. */
export function useScopeMarks(scope: string) {
  const [marks, setMarks] = useState<ScopeMark[]>(() => readMarks(scope));
  const refresh = useCallback(() => setMarks(readMarks(scope)), [scope]);
  useEffect(() => {
    refresh();
    const onStorage = (e: StorageEvent) => e.key === HL_KEY && refresh();
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, [refresh]);
  return [marks, refresh] as const;
}

// ── Panel ─────────────────────────────────────────────────────────────────────────────────────────
const TONE: Partial<Record<Kategori, string>> = {
  tuzak: 'warn',
  karakteristik: 'ai',
  mekanizma: 'ai',
  eslesme: 'ok',
  tani_tedavi: 'ok',
  sayi: 'accent',
  en_sik: 'accent',
};

const SpotItem: React.FC<{ s: ExamSpot }> = ({ s }) => {
  const [open, setOpen] = useState(false);
  const ansId = useId();
  const k = KAT[s.kategori];
  return (
    <li className="sr-xs">
      <span className={`sr-xs-tag is-${TONE[s.kategori] || 'ink'}`}>{k?.kisa || s.kategori}</span>
      <strong>{s.baslik}</strong>
      <p>
        <Zengin metin={s.spot} />
      </p>
      {s.tuzak && (
        <p className="sr-xs-trap">
          <b>Tuzak:</b> <Zengin metin={s.tuzak} />
        </p>
      )}
      {s.soru && s.cevap && (
        <>
          <button type="button" className="sr-xs-q" aria-expanded={open} aria-controls={ansId} onClick={() => setOpen((v) => !v)}>
            <span>{s.soru}</span>
            <ChevronDown aria-hidden />
          </button>
          <p id={ansId} className="sr-xs-a" hidden={!open}>
            <Zengin metin={s.cevap} />
          </p>
        </>
      )}
    </li>
  );
};

export const ReaderPanel: React.FC<{
  spots: ExamSpot[] | null | undefined;
  marks: ScopeMark[];
  onJump: (m: ScopeMark) => void;
  inline?: boolean;
}> = ({ spots, marks, onJump, inline }) => {
  const hasSpots = spots !== null;
  const [tab, setTab] = useState<'spots' | 'notes'>(hasSpots ? 'spots' : 'notes');
  useEffect(() => {
    if (!hasSpots) setTab('notes');
  }, [hasSpots]);
  const uid = useId();
  const swatch = useMemo(() => Object.fromEntries(HL_COLORS.map((c) => [c.id, c.swatch])) as Record<HlColor, string>, []);

  const tabs: { id: 'spots' | 'notes'; label: string }[] = [
    ...(hasSpots ? [{ id: 'spots' as const, label: `Spotlar${spots ? ` · ${spots.length}` : ''}` }] : []),
    { id: 'notes', label: `Notlarım · ${marks.length}` },
  ];

  return (
    <section className={`sr-panel ${inline ? 'is-inline' : ''}`} aria-label="Spotlar ve notlarım">
      <div className="sr-ptabs" role="tablist" aria-label="Panel" style={{ '--n': tabs.length } as React.CSSProperties}>
        {tabs.map((t) => (
          <button
            key={t.id}
            type="button"
            role="tab"
            id={`${uid}-t-${t.id}`}
            aria-selected={tab === t.id}
            aria-controls={`${uid}-p-${t.id}`}
            className={tab === t.id ? 'is-on' : ''}
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="sr-ppane" role="tabpanel" id={`${uid}-p-${tab}`} aria-labelledby={`${uid}-t-${tab}`}>
        {tab === 'spots' ? (
          spots === undefined ? (
            <div className="sr-pskel" aria-busy="true" aria-label="Spotlar yükleniyor">
              {[0, 1, 2].map((i) => (
                <span key={i} className="ui-skel" />
              ))}
            </div>
          ) : (
            <ol className="sr-xs-list">{spots?.map((s) => <SpotItem key={s.id} s={s} />)}</ol>
          )
        ) : marks.length === 0 ? (
          <p className="sr-pempty">
            <PenIcon aria-hidden />
            Üst çubuktaki kalemle metni işaretle; işaretlediğin yerler burada toplanır.
          </p>
        ) : (
          <ol className="sr-xs-list">
            {marks.map((m) => (
              <li key={m.id}>
                <button type="button" className="sr-mark" onClick={() => onJump(m)}>
                  <i style={{ background: swatch[m.color] }} aria-hidden />
                  <span>{m.text}</span>
                </button>
              </li>
            ))}
          </ol>
        )}
      </div>
    </section>
  );
};
