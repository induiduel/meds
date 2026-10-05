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
import { btnSecondary } from './StudyUI';

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

  return (
    <div className="flex flex-col gap-3 sm:gap-4">
      <PageHeader
        title="Çalış"
        description={loading && bank.length === 0 ? 'Soru bankası yükleniyor…' : `${bank.length.toLocaleString('tr-TR')} soru · %${stats.accuracy} doğruluk`}
      />

      {/* Tek satır: sekmeler solda, hızlı test sağda */}
      <div className="flex items-center gap-2 min-w-0">
        <div role="tablist" aria-label="Çalışma bölümleri" className="ms-f-seg flex-1 sm:flex-none">
          {tabs.map((t) => {
            const on = section === t.id;
            const Icon = t.icon;
            return (
              <button
                key={t.id}
                type="button"
                role="tab"
                id={`study-tab-${t.id}`}
                aria-selected={on}
                aria-controls={`study-panel-${t.id}`}
                onClick={() => setSection(t.id)}
                className={`inline-flex items-center justify-center gap-1.5 ${on ? 'is-on' : ''}`}
              >
                <Icon className="w-4 h-4 shrink-0" strokeWidth={on ? 2.3 : 2} />
                <span className="hidden min-[420px]:inline">{t.label}</span>
                {t.count ? <span className="text-[12px] text-ink-3">{t.count}</span> : null}
              </button>
            );
          })}
        </div>
        <span className="hidden sm:block flex-1" />
        <button
          type="button"
          onClick={startQuick}
          disabled={bank.length === 0}
          className="h-10 px-4 rounded-full bg-accent hover:bg-accent-hover text-white text-[14px] font-semibold inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50 shrink-0"
          title="Karışık 20 soruluk hızlı test"
        >
          <Zap className="w-4 h-4" /> <span className="hidden sm:inline">Hızlı test</span>
        </button>
      </div>

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
    </div>
  );
};
