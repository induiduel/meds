import React, { useState, useMemo } from 'react';
import { PageHeader } from './ui/PageHeader';
import { EmptySearch } from './ui/Animations';
import {
  ChevronDown,
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

    // Yapay zeka botları ve sistem hesaplarını sıralamadan hariç tut
    const isBotOrSystem = (name?: string, key?: string) => {
      const s = `${name || ''} ${key || ''}`.toLocaleLowerCase('tr-TR');
      return (
        s.includes('yapay zeka') ||
        s.includes('ai (') ||
        s.includes(' ai') ||
        s.startsWith('ai') ||
        s.includes('bot') ||
        s.includes('gemini') ||
        s.includes('gpt') ||
        s.includes('deepseek') ||
        s.includes('claude') ||
        s.includes('asistan') ||
        s.includes('reconstruct') ||
        s.includes('otomasyon') ||
        s.includes('sistem') ||
        s.includes('system') ||
        s.includes('ocr') ||
        s.includes('taranmış') ||
        s.includes('arşivi') ||
        s.includes('arşiv') ||
        s.includes('taslak ayırma')
      );
    };

    // Helper to get or create stats entry
    const getEntry = (key: string, name: string, studentNumber?: string): ContributorStats | null => {
      if (isBotOrSystem(name, key)) return null;
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
        if (entry) {
          entry.questionsCount += 1;
          entry.totalPoints += 10; // +10 points for introducing a question
        }
      }

      // 2. Memory fragments (stem, clue, text)
      q.fragments.forEach((f) => {
        if (f.author && f.author !== 'Anonim' && f.author !== 'Hafıza Parçası') {
          const key = f.authorUid || f.author;
          const entry = getEntry(key, f.author, f.authorStudentNumber);
          if (entry) {
            if (f.type === 'stem') {
              entry.questionsCount += 1;
              entry.totalPoints += 10;
            } else {
              entry.totalPoints += 5;
            }
            entry.upvotesCount += (f.upvotes || 0);
            entry.totalPoints += (f.upvotes || 0) * 2; // +2 points per upvote
          }
        }
      });

      // 3. Options
      q.options.forEach((opt) => {
        if (opt.suggestedBy && opt.suggestedBy !== 'Anonim' && !opt.isAiGenerated) {
          const key = opt.suggestedByUid || opt.suggestedBy;
          const entry = getEntry(key, opt.suggestedBy);
          if (entry) {
            entry.optionsCount += 1;
            entry.totalPoints += 5; // +5 points for providing an option
            entry.upvotesCount += (opt.upvotes || 0);
            entry.totalPoints += (opt.upvotes || 0) * 2; // +2 points per upvote
          }
        }
      });

      // 4. Revisions
      if (q.revisions) {
        q.revisions.forEach((rev) => {
          if (rev.editorName && rev.editorName !== 'Anonim') {
            const key = rev.editorUid || rev.editorName;
            const entry = getEntry(key, rev.editorName, rev.editorStudentNumber);
            if (entry) {
              entry.revisionsCount += 1;
              entry.totalPoints += 5; // +5 points for refining and editing
            }
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
  const initials = (name: string) =>
    name
      .split(/[^\p{L}\p{N}]+/u)
      .filter(Boolean)
      .slice(0, 2)
      .map((w) => w[0])
      .join('')
      .toLocaleUpperCase('tr-TR') || '?';

  return (
    <div className="ds-page">
      <PageHeader
        title="Sıralama"
        stats={[
          { label: 'katkıcı', value: leaderboard.length },
          ...(me ? [{ label: 'senin sıran', value: `${myRank}.`, tone: 'accent' as const }] : []),
        ]}
        description="Soru kökü +10 · şık +5 · aldığın her beğeni +2 puan."
        actions={
          <button type="button" onClick={onOpenContributeModal} className="ms-btn is-primary">
            <Sparkles aria-hidden />
            Katkı yap
          </button>
        }
      />

      {/* Kapsam + kurul */}
      <div className="ds-toolbar">
        <div role="radiogroup" aria-label="Kapsam" className="ds-seg">
          {(
            [
              ['current', 'Bu kurul'],
              ['all', 'Tüm kurullar'],
            ] as const
          ).map(([id, label]) => (
            <button key={id} type="button" role="radio" aria-checked={filterScope === id} onClick={() => setFilterScope(id)}>
              {label}
            </button>
          ))}
        </div>
        {filterScope === 'current' && (
          <label className="ds-select is-wide">
            <span>Kurul</span>
            <select value={selectedCommitteeId} onChange={(e) => onSelectCommittee(e.target.value)} aria-label="Kurul">
              {committees.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
            <ChevronDown aria-hidden />
          </label>
        )}
      </div>

      {/* İlk üç: sade podyum */}
      {top3.some((t) => t.totalPoints > 0) && (
        <ol className="ds-podium">
          {top3.map((item, i) => (
            <li key={item.id} className={`${i === 0 ? 'is-first' : ''} ${item.isCurrentUser ? 'is-me' : ''}`}>
              <span className="ds-avatar is-lg">{initials(item.name)}<i>{i + 1}</i></span>
              <span className="ds-podium-t">
                <b>{item.name}</b>
                <span>{item.totalPoints} puan</span>
              </span>
            </li>
          ))}
        </ol>
      )}

      {/* Senin sıran */}
      {me && (
        <div className="ds-me">
          <span className="ds-me-rank">{myRank}.</span>
          <span className="ds-row-t">
            <span>Senin sıran</span>
            <b>{me.name}</b>
          </span>
          <span className="ds-me-pts">{me.totalPoints}<small>puan</small></span>
        </div>
      )}

      {/* Tam liste */}
      <section className="ds-panel is-flush">
        <label className="ds-panel-search">
          <Search aria-hidden />
          <input
            type="search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Rumuz ya da öğrenci no ara"
            aria-label="Katkıcı ara"
          />
          <span className="ds-count">{filteredLeaderboard.length} kişi</span>
        </label>
        {filteredLeaderboard.length === 0 ? (
          <div className="ds-empty">
            <EmptySearch size={56} />
            <b>Aramaya uyan katkıcı yok</b>
          </div>
        ) : (
          <ol className="ds-rank-list">
            {filteredLeaderboard.map((item) => {
              const rank = leaderboard.indexOf(item) + 1;
              return (
                <li key={item.id} className={item.isCurrentUser ? 'is-me' : ''}>
                  <span className={`ds-rank ${rank <= 3 ? 'is-top' : ''}`}>{rank}</span>
                  <span className="ds-avatar">{initials(item.name)}</span>
                  <span className="ds-row-t">
                    <b>
                      {item.name}
                      {item.isCurrentUser && <span className="ms-tag is-new">Sen</span>}
                    </b>
                    <span>
                      {item.questionsCount} soru · {item.optionsCount} şık · {item.upvotesCount} beğeni
                    </span>
                  </span>
                  <span className="ds-bar" aria-hidden="true">
                    <i style={{ width: `${Math.max(item.totalPoints > 0 ? 3 : 0, (item.totalPoints / maxPoints) * 100)}%` }} />
                  </span>
                  <span className="ds-pts">{item.totalPoints}</span>
                </li>
              );
            })}
          </ol>
        )}
      </section>
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
