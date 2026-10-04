import React, { useEffect, useMemo, useState } from 'react';
import { PageHeader } from '../ui/PageHeader';
import { ListChecks, Target, NotebookPen, Zap } from 'lucide-react';
import { Committee, QuestionItem } from '../../types';
import { StudyQuestion, loadArchiveBank, buildBank, getProgress, getReview, getTestHistory, getNotes } from '../../services/studyStore';
import { filterCurrent2026_2027Committees } from '../../services/firestoreDb';
import { SolveView } from './SolveView';
import { SelfTestView } from './SelfTestView';
import { NotesView } from './NotesView';
import { btnSecondary } from './StudyUI';

export type StudySection = 'solve' | 'test' | 'notes';

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
      return s === 'solve' || s === 'test' || s === 'notes' ? s : 'solve';
    } catch {
      return 'solve';
    }
  });
  const [archive, setArchive] = useState<StudyQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [tick, setTick] = useState(0);

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
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tick, section]);

  const bump = () => setTick((t) => t + 1);
  const quickReady = questions.some((q) => q.status === 'completed' && q.reconstruction);

  const tabs: { id: StudySection; label: string; icon: React.ElementType; meta: string }[] = [
    { id: 'solve', label: 'Soru çöz', icon: ListChecks, meta: `${stats.solved} çözüldü` },
    { id: 'test', label: 'Kendini test et', icon: Target, meta: `${stats.tests} deneme` },
    { id: 'notes', label: 'Notlarım', icon: NotebookPen, meta: `${stats.notes} not` },
  ];

  return (
    <div className="flex flex-col gap-3 sm:gap-5">
      <PageHeader
        eyebrow="Pratik"
        title="Çalış"
        description={loading && bank.length === 0 ? 'Soru bankası yükleniyor…' : 'Soru çöz, kendini dene, notlarını tek yerde tut.'}
        stats={[
          { label: 'Çözümlü soru', value: bank.length.toLocaleString('tr-TR') },
          { label: 'Doğruluk', value: `%${stats.accuracy}`, tone: 'ok' },
          { label: 'Tekrar listesi', value: stats.review, tone: 'warn' },
        ]}
        actions={
          <button
            type="button"
            onClick={onStartQuickTest}
            disabled={!quickReady}
            className={`${btnSecondary} shrink-0 px-3`}
            title="Seçili kurulun kurulan sorularıyla tam ekran hızlı test"
            aria-label="Havuzdan hızlı test"
          >
            <Zap className="w-4 h-4" /> <span className="hidden sm:inline">Havuzdan hızlı test</span>
          </button>
        }
      />

      <div role="tablist" aria-label="Çalışma bölümleri" className="grid grid-cols-3 gap-1 bg-white border border-line rounded-xl p-1">
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
              className={`min-h-11 px-2 sm:px-3 py-1.5 rounded-[10px] flex flex-col sm:flex-row items-center justify-center gap-0.5 sm:gap-2 cursor-pointer transition-colors ${
                on ? 'bg-accent-soft text-accent' : 'text-ink-2 hover:bg-canvas hover:text-ink'
              }`}
            >
              <Icon className="w-[18px] h-[18px] shrink-0" strokeWidth={on ? 2.3 : 2} />
              <span className={`text-[13px] sm:text-[15px] leading-tight ${on ? 'font-semibold' : 'font-medium'}`}>{t.label}</span>
              <span className={`hidden md:inline text-[12px] font-mono ${on ? 'text-accent/80' : 'text-ink-3'}`}>{t.meta}</span>
            </button>
          );
        })}
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
          />
        )}
        {section === 'notes' && <NotesView disciplines={disciplines} />}
      </div>
    </div>
  );
};
