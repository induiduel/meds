import React, { useEffect, useMemo, useState } from 'react';
import { PageHeader } from '../ui/PageHeader';
import { ListChecks, Target, NotebookPen, Zap, Bookmark } from 'lucide-react';
import { ListsView } from './ListsView';
import { Committee, QuestionItem } from '../../types';
import { StudyQuestion, loadArchiveBank, buildBank, getProgress, getReview, getTestHistory, getNotes, getFavorites, getFavoriteCards } from '../../services/studyStore';
import { filterCurrent2026_2027Committees } from '../../services/firestoreDb';
import { SolveView } from './SolveView';
import { SelfTestView } from './SelfTestView';
import { NotesView } from './NotesView';
import { Segmented as Seg } from '../ui/kit';
import { useAppearance } from '../../utils/appearance';
import { StudyHubV12 } from '../v12/StudyV12';

export type StudySection = 'solve' | 'test' | 'notes' | 'lists';

const SECTION_KEY = 'medsoru_study_section';

interface StudyHubProps {
  questions: QuestionItem[];
  committees: Committee[];
  selectedCommitteeId?: string;
  onSelectCommittee?: (id: string) => void;
  onStartQuickTest: () => void;
}

export const StudyHub: React.FC<StudyHubProps> = ({
  questions,
  committees,
  selectedCommitteeId,
  onStartQuickTest,
}) => {
  // v12 "Net": başlık + sekmeler ayrı yapı (components/v12/StudyV12.tsx); bölüm içerikleri ortak
  const gor = useAppearance();
  const v12 = gor.design === 'v12';
  const [section, setSection] = useState<StudySection>(() => {
    try {
      const s = localStorage.getItem(SECTION_KEY) as StudySection | null;
      return s === 'solve' || s === 'test' || s === 'notes' || s === 'lists' ? s : 'solve';
    } catch {
      return 'solve';
    }
  });
  const [archive, setArchive] = useState<StudyQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [tick, setTick] = useState(0);
  const [quickNonce, setQuickNonce] = useState(0);

  // Strict 2026-2027 committees
  const cleanCommittees = useMemo(() => filterCurrent2026_2027Committees(committees), [committees]);

  useEffect(() => {
    let alive = true;
    loadArchiveBank().then((a) => {
      if (!alive) return;
      setArchive(a);
      setLoading(false);
    });
    return () => {
      alive = false;
    };
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(SECTION_KEY, section);
    } catch {
      /* ignore */
    }
  }, [section]);

  const bank = useMemo(() => buildBank(archive, questions), [archive, questions]);
  const disciplines = useMemo(() => [...new Set(bank.map((q) => q.discipline))], [bank]);

  // Summary numbers (recomputed when a child reports progress)
  const stats = useMemo(() => {
    const p = getProgress();
    const solved = Object.values(p);
    const correct = solved.filter((a) => a.correct).length;
    return {
      solved: solved.length,
      accuracy: solved.length ? Math.round((correct / solved.length) * 100) : 0,
      review: getReview().size,
      tests: getTestHistory().length,
      notes: getNotes().length,
      favorites: getFavorites().size + getFavoriteCards().length,
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tick, section]);

  const bump = () => setTick((t) => t + 1);
  const tabs: { id: StudySection; label: string; icon: React.ElementType; count?: number }[] = [
    { id: 'solve', label: 'Soru çöz', icon: ListChecks },
    { id: 'test', label: 'Test', icon: Target },
    { id: 'lists', label: 'Listelerim', icon: Bookmark, count: stats.review + stats.favorites },
    { id: 'notes', label: 'Notlar', icon: NotebookPen, count: stats.notes || undefined },
  ];

  // Hızlı test artık tüm bankadan (arşiv + havuz) çeker; havuzdaki az sayıda kurulmuş soruya takılmaz
  const startQuick = () => {
    setSection('test');
    setQuickNonce((n) => n + 1);
  };

  const panel = (
    <div role="tabpanel" id={`study-panel-${section}`} aria-labelledby={`study-tab-${section}`}>
      {section === 'solve' && (
        <SolveView
          bank={bank}
          committees={cleanCommittees}
          loading={loading}
          initialCommitteeId={selectedCommitteeId}
          onProgressChange={bump}
        />
      )}
      {section === 'test' && (
        <SelfTestView
          bank={bank}
          committees={cleanCommittees}
          loading={loading}
          initialCommitteeId={selectedCommitteeId}
          onProgressChange={bump}
          quickStartNonce={quickNonce}
        />
      )}
      {section === 'lists' && <ListsView bank={bank} onChange={bump} />}
      {section === 'notes' && <NotesView disciplines={disciplines} />}
    </div>
  );

  if (v12) {
    return (
      <>
      <StudyHubV12
        loading={loading}
        bankSize={bank.length}
        solved={stats.solved}
        accuracy={stats.accuracy}
        tabs={tabs}
        section={section}
        onSection={(id) => setSection(id as StudySection)}
        onQuick={startQuick}
      >
        {panel}
      </StudyHubV12>
      </>
    );
  }

  return (
    <div className="flex flex-col gap-3 sm:gap-4">
      <PageHeader
        title="Listelerim ve notlar"
        description={loading && bank.length === 0 ? 'Soru bankası yükleniyor…' : undefined}
        stats={loading && bank.length === 0 ? undefined : [
          { label: 'soru', value: bank.length.toLocaleString('tr-TR') },
          ...(stats.solved > 0
            ? [
                { label: 'çözülen', value: stats.solved.toLocaleString('tr-TR') },
                { label: 'doğru', value: `%${stats.accuracy}`, tone: (stats.accuracy >= 70 ? 'ok' : stats.accuracy >= 50 ? 'warn' : 'default') as 'ok' | 'warn' | 'default' },
              ]
            : []),
        ]}
      />

          {/* v8: özet satırı + kayan sekmeler; hızlı test her zaman görünür */}
          {/* Özet tek satır olarak başlıkta; ayrı dört kutulu KPI şeridi aynı bilgiyi tekrarlıyordu. */}
          <div className="cx-dock st-dock">
            <div className="st-dock-row">
              <Seg<StudySection>
                className="st-tabs"
                label="Çalışma bölümleri"
                value={section}
                onChange={setSection}
                options={tabs.map((t) => {
                  const Icon = t.icon;
                  return {
                    value: t.id,
                    label: (
                      <span className="inline-flex items-center gap-1.5">
                        <Icon className="w-4 h-4 shrink-0" />
                        <span className="st-tab-l">{t.label}</span>
                        {t.count ? <span className="lh-n">{t.count}</span> : null}
                      </span>
                    ),
                  };
                })}
              />
              <button type="button" onClick={startQuick} disabled={bank.length === 0} className="ui-btn is-primary st-quick" title="Karışık 20 soruluk hızlı test">
                <Zap /> <span className="st-tab-l">Hızlı<span className="st-hide-xs"> test</span></span>
              </button>
            </div>
          </div>

      {panel}
    </div>
  );
};
