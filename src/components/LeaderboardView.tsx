import React, { useState, useMemo } from 'react';
import { PageHeader } from './ui/PageHeader';
import { 
  Trophy, 
  Medal, 
  Award, 
  Sparkles, 
  User, 
  ThumbsUp, 
  FileText, 
  CheckCircle2, 
  ListFilter,
  Shield,
  HelpCircle,
  Hash,
  Search,
} from 'lucide-react';
import { QuestionItem, Committee } from '../types';
import { AppUser } from '../services/auth';
import { getCleanRumuz } from '../services/profanityFilter';

interface LeaderboardViewProps {
  questions: QuestionItem[];
  committees: Committee[];
  selectedCommitteeId: string;
  onSelectCommittee: (id: string) => void;
  currentUser: AppUser | null;
  onOpenContributeModal: () => void;
}

interface ContributorStats {
  id: string;
  name: string;
  studentNumber?: string;
  questionsCount: number;
  optionsCount: number;
  upvotesCount: number;
  revisionsCount: number;
  totalPoints: number;
  isCurrentUser: boolean;
}

export const LeaderboardView: React.FC<LeaderboardViewProps> = ({
  questions,
  committees,
  selectedCommitteeId,
  onSelectCommittee,
  currentUser,
  onOpenContributeModal,
}) => {
  const [filterScope, setFilterScope] = useState<'current' | 'all'>('current');
  const [searchTerm, setSearchTerm] = useState('');

  const currentCommittee = committees.find((c) => c.id === selectedCommitteeId);

  // Compute leaderboard from questions based on filterScope
  const leaderboard = useMemo(() => {
    const relevantQuestions = filterScope === 'current'
      ? questions.filter((q) => q.committeeId === selectedCommitteeId)
      : questions;

    const statsMap: Record<string, ContributorStats> = {};

    // Helper to get or create stats entry
    const getEntry = (key: string, name: string, studentNumber?: string): ContributorStats => {
      const cleanKey = key.trim().toLowerCase();
      if (!statsMap[cleanKey]) {
        const isCurrent = !!(
          (currentUser?.uid && key === currentUser.uid) ||
          (currentUser?.displayName && cleanKey === currentUser.displayName.toLowerCase())
        );

        statsMap[cleanKey] = {
          id: cleanKey,
          name: getCleanRumuz(name || 'Anonim Tıbbiyeli'),
          studentNumber: studentNumber || (isCurrent ? currentUser?.studentNumber || undefined : undefined),
          questionsCount: 0,
          optionsCount: 0,
          upvotesCount: 0,
          revisionsCount: 0,
          totalPoints: 0,
          isCurrentUser: isCurrent,
        };
      }
      return statsMap[cleanKey];
    };

    // Calculate points from questions
    relevantQuestions.forEach((q) => {
      // 1. Question creators
      if (q.contributedByName || q.contributedByUid) {
        const key = q.contributedByUid || q.contributedByName!;
        const entry = getEntry(key, q.contributedByName || 'Öğrenci', q.contributedByStudentNumber);
        entry.questionsCount += 1;
        entry.totalPoints += 10; // +10 points for introducing a question
      }

      // 2. Memory fragments (stem, clue, text)
      q.fragments.forEach((f) => {
        if (f.author && f.author !== 'Anonim' && f.author !== 'Hafıza Parçası') {
          const key = f.authorUid || f.author;
          const entry = getEntry(key, f.author, f.authorStudentNumber);
          if (f.type === 'stem') {
            entry.questionsCount += 1;
            entry.totalPoints += 10;
          } else {
            entry.totalPoints += 5;
          }
          entry.upvotesCount += (f.upvotes || 0);
          entry.totalPoints += (f.upvotes || 0) * 2; // +2 points per upvote
        }
      });

      // 3. Options
      q.options.forEach((opt) => {
        if (opt.suggestedBy && opt.suggestedBy !== 'Anonim' && !opt.isAiGenerated) {
          const key = opt.suggestedByUid || opt.suggestedBy;
          const entry = getEntry(key, opt.suggestedBy);
          entry.optionsCount += 1;
          entry.totalPoints += 5; // +5 points for providing an option
          entry.upvotesCount += (opt.upvotes || 0);
          entry.totalPoints += (opt.upvotes || 0) * 2; // +2 points per upvote
        }
      });

      // 4. Revisions
      if (q.revisions) {
        q.revisions.forEach((rev) => {
          if (rev.editorName && rev.editorName !== 'Anonim') {
            const key = rev.editorUid || rev.editorName;
            const entry = getEntry(key, rev.editorName, rev.editorStudentNumber);
            entry.revisionsCount += 1;
            entry.totalPoints += 5; // +5 points for refining and editing
          }
        });
      }
    });

    // Ensure current logged-in user is listed even if 0 contributions
    if (currentUser) {
      const userKey = currentUser.uid || currentUser.displayName || currentUser.email || 'me';
      const cleanUserKey = userKey.trim().toLowerCase();
      if (!statsMap[cleanUserKey]) {
        statsMap[cleanUserKey] = {
          id: cleanUserKey,
          name: getCleanRumuz(currentUser.displayName || currentUser.email?.split('@')[0] || 'Ben'),
          studentNumber: currentUser.studentNumber || undefined,
          questionsCount: 0,
          optionsCount: 0,
          upvotesCount: 0,
          revisionsCount: 0,
          totalPoints: 0,
          isCurrentUser: true,
        };
      } else {
        statsMap[cleanUserKey].isCurrentUser = true;
      }
    }

    // Add sample registered classmates who haven't contributed yet so they appear in list as requested
    const samplePassiveUsers = [
      { key: 'ogrenci_ali', name: 'Alperen_Tıp3', studentNumber: '2101030012' },
      { key: 'ogrenci_selin', name: 'DrSelin', studentNumber: '2101030045' },
      { key: 'ogrenci_burak', name: 'BurakC_Med', studentNumber: '2101030089' },
    ];
    samplePassiveUsers.forEach((su) => {
      if (!statsMap[su.key]) {
        statsMap[su.key] = {
          id: su.key,
          name: getCleanRumuz(su.name),
          studentNumber: su.studentNumber,
          questionsCount: 0,
          optionsCount: 0,
          upvotesCount: 0,
          revisionsCount: 0,
          totalPoints: 0,
          isCurrentUser: false,
        };
      }
    });

    // Sort descending by totalPoints
    const sorted = Object.values(statsMap).sort((a, b) => {
      if (b.totalPoints !== a.totalPoints) return b.totalPoints - a.totalPoints;
      if (b.questionsCount !== a.questionsCount) return b.questionsCount - a.questionsCount;
      return b.upvotesCount - a.upvotesCount;
    });

    return sorted;
  }, [questions, selectedCommitteeId, filterScope, currentUser]);

  const filteredLeaderboard = useMemo(() => {
    if (!searchTerm.trim()) return leaderboard;
    const term = searchTerm.toLowerCase();
    return leaderboard.filter(
      (item) =>
        item.name.toLowerCase().includes(term) ||
        (item.studentNumber && item.studentNumber.includes(term))
    );
  }, [leaderboard, searchTerm]);

  const top3 = leaderboard.slice(0, 3);

  const me = leaderboard.find((x) => x.isCurrentUser);
  const myRank = me ? leaderboard.indexOf(me) + 1 : 0;
  const maxPoints = Math.max(1, leaderboard[0]?.totalPoints || 1);
  const podiumTone = ['#B7791F', '#6B7785', '#A0592B'];
  const initials = (name: string) =>
    name
      .split(/[^\p{L}\p{N}]+/u)
      .filter(Boolean)
      .slice(0, 2)
      .map((w) => w[0])
      .join('')
      .toLocaleUpperCase('tr-TR') || '?';

  return (
    <div className="w-full flex flex-col gap-3 sm:gap-4 min-w-0">
      <PageHeader
        eyebrow="Topluluk"
        title="Sıralama"
        description="Soru kökü +10 · şık +5 · aldığın her beğeni +2 puan."
        actions={
          <button
            type="button"
            onClick={onOpenContributeModal}
            className="h-10 px-3.5 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-[14px] font-semibold inline-flex items-center gap-1.5 cursor-pointer shrink-0 shadow-sm"
          >
            <Sparkles className="w-4 h-4" />
            Katkı yap
          </button>
        }
      />

      {/* Scope + committee */}
      <div className="flex flex-wrap items-center gap-2">
        <div role="radiogroup" aria-label="Kapsam" className="inline-grid grid-cols-2 gap-1 bg-white border border-line rounded-xl p-1">
          {(
            [
              ['current', 'Bu kurul'],
              ['all', 'Tüm kurullar'],
            ] as const
          ).map(([id, label]) => (
            <button
              key={id}
              type="button"
              role="radio"
              aria-checked={filterScope === id}
              onClick={() => setFilterScope(id)}
              className={`h-8 px-3 rounded-lg text-[13.5px] cursor-pointer whitespace-nowrap ${
                filterScope === id ? 'bg-ink text-white font-semibold' : 'text-ink-2 hover:text-ink'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
        {filterScope === 'current' && (
          <label className="min-w-0 flex-1 sm:flex-none">
            <span className="sr-only">Kurul</span>
            <select
              value={selectedCommitteeId}
              onChange={(e) => onSelectCommittee(e.target.value)}
              className="w-full sm:w-auto sm:max-w-[320px] h-10 rounded-xl bg-white border border-line px-3 text-[14px] text-ink cursor-pointer truncate"
            >
              {committees.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </label>
        )}
      </div>

      {/* Your rank */}
      {me && (
        <div className="bg-ink text-white rounded-2xl px-4 sm:px-5 py-4 flex items-center gap-4">
          <span className="font-display font-bold text-[34px] leading-none tracking-[-0.03em] w-14 text-center shrink-0">{myRank}.</span>
          <span className="flex-1 min-w-0">
            <span className="block text-[13px] text-white/60">Senin sıran</span>
            <span className="block text-[16px] font-semibold truncate">{me.name}</span>
          </span>
          <span className="text-right shrink-0">
            <span className="block font-mono text-[20px] font-semibold">{me.totalPoints}</span>
            <span className="block text-[12px] text-white/60">puan</span>
          </span>
        </div>
      )}

      {/* Podium */}
      {top3.some((t) => t.totalPoints > 0) && (
        <ol className="list-none m-0 p-0 grid grid-cols-3 gap-2 sm:gap-3">
          {top3.map((item, i) => (
            <li
              key={item.id}
              className={`bg-white border rounded-2xl px-2 sm:px-4 pt-4 pb-3 flex flex-col items-center text-center gap-1.5 min-w-0 ${
                item.isCurrentUser ? 'border-accent' : 'border-line'
              } ${i === 0 ? 'shadow-md' : ''}`}
            >
              <span className="relative">
                <span
                  className="w-12 h-12 sm:w-14 sm:h-14 rounded-full flex items-center justify-center text-white font-semibold text-[15px] sm:text-[17px]"
                  style={{ background: podiumTone[i] }}
                >
                  {initials(item.name)}
                </span>
                <span className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-white border border-line flex items-center justify-center font-mono text-[12px] font-semibold">
                  {i + 1}
                </span>
              </span>
              <span className="text-[14px] sm:text-[15px] font-semibold text-ink truncate max-w-full">{item.name}</span>
              <span className="font-mono text-[13px] text-ink-2">{item.totalPoints} puan</span>
            </li>
          ))}
        </ol>
      )}

      {/* Full list */}
      <div className="bg-white border border-line rounded-2xl overflow-hidden">
        <div className="flex items-center gap-2 px-3 sm:px-4 py-2.5 border-b border-line-soft">
          <Search className="w-4 h-4 text-ink-3 shrink-0" />
          <input
            type="search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Rumuz ya da öğrenci no ara"
            aria-label="Katkıcı ara"
            className="flex-1 min-w-0 h-9 bg-transparent border-0 outline-0 text-[16px] sm:text-[14px] placeholder:text-slate-600"
          />
          <span className="text-[12.5px] text-ink-3 shrink-0">{filteredLeaderboard.length} kişi</span>
        </div>
        {filteredLeaderboard.length === 0 ? (
          <p className="m-0 px-4 py-10 text-center text-[14px] text-ink-3">Aramaya uyan katkıcı yok.</p>
        ) : (
          <ol className="list-none m-0 p-0">
            {filteredLeaderboard.map((item) => {
              const rank = leaderboard.indexOf(item) + 1;
              return (
                <li
                  key={item.id}
                  className={`grid grid-cols-[32px_minmax(0,1fr)_auto] items-center gap-3 px-3 sm:px-4 py-3 border-b border-line-soft last:border-b-0 ${
                    item.isCurrentUser ? 'bg-accent-soft/60' : ''
                  }`}
                >
                  <span className={`font-mono text-[14px] text-center ${rank <= 3 ? 'font-bold text-ink' : 'text-ink-3'}`}>{rank}</span>
                  <span className="min-w-0 flex flex-col gap-1">
                    <span className="flex items-center gap-2 min-w-0">
                      <span className="text-[15px] font-semibold text-ink truncate">{item.name}</span>
                      {item.isCurrentUser && (
                        <span className="h-5 px-1.5 rounded-full bg-accent text-white text-[11px] font-semibold inline-flex items-center shrink-0">Sen</span>
                      )}
                    </span>
                    <span className="flex items-center gap-2">
                      <span className="flex-1 max-w-[220px] h-1.5 rounded-full bg-line-soft overflow-hidden" aria-hidden="true">
                        <span
                          className="block h-full rounded-full bg-accent"
                          style={{ width: `${Math.max(item.totalPoints > 0 ? 3 : 0, (item.totalPoints / maxPoints) * 100)}%` }}
                        />
                      </span>
                      <span className="text-[12px] text-ink-3 whitespace-nowrap">
                        {item.questionsCount} soru · {item.optionsCount} şık
                        <span className="hidden sm:inline"> · {item.upvotesCount} beğeni</span>
                      </span>
                    </span>
                  </span>
                  <span className="font-mono text-[15px] font-semibold text-ink text-right">{item.totalPoints}</span>
                </li>
              );
            })}
          </ol>
        )}
      </div>
    </div>
  );
};

function CrownIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5zm14 3c0 .6-.4 1-1 1H6c-.6 0-1-.4-1-1v-1h14v1z" />
    </svg>
  );
}
