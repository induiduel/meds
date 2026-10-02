import React, { useState, useMemo } from 'react';
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
  Hash
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

  return (
    <div className="flex flex-col gap-3 sm:gap-5 min-w-0">
      {/* Title (light, compact) */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
        <div className="min-w-0">
          <h2 className="m-0 font-display font-bold text-[24px] sm:text-[32px] leading-[1.1] tracking-[-0.03em] text-ink">Katkı sıralaması</h2>
          <p className="m-0 mt-1 text-[14px] text-ink-2 max-w-[720px]">
            {filterScope === 'current' ? (currentCommittee ? currentCommittee.name : 'Seçili kurul') : 'Tüm kurullar'} · Soru kökü +10, şık +5, beğeni +2 puan.
          </p>
        </div>
        <button
          type="button"
          onClick={onOpenContributeModal}
          className="self-start sm:self-auto h-10 px-4 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-[14px] font-semibold inline-flex items-center gap-2 cursor-pointer shrink-0"
        >
          <Sparkles className="w-4 h-4" />
          Katkı yap
        </button>
      </div>

      {/* Podium for Top 3 */}
      {top3.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          {/* 2nd Place */}
          {top3[1] && (
            <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs flex flex-col items-center text-center relative order-2 md:order-1 mt-4 md:mt-6">
              <div className="w-10 h-10 rounded-full bg-slate-100 border border-slate-300 flex items-center justify-center text-slate-700 font-black text-sm mb-3">
                🥈 2
              </div>
              <h4 className="font-bold text-slate-900 text-sm">{top3[1].name}</h4>
              {top3[1].studentNumber && (
                <span className="text-[11px] text-slate-500 font-mono mt-0.5">No: {top3[1].studentNumber}</span>
              )}
              <div className="mt-3 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 w-full">
                <span className="text-lg font-black text-slate-800">{top3[1].totalPoints}</span>
                <span className="text-xs text-slate-500 block">Puan</span>
              </div>
              <div className="mt-2 text-[11px] text-slate-600 flex items-center gap-3">
                <span>{top3[1].questionsCount} Soru</span>
                <span>•</span>
                <span>{top3[1].optionsCount} Şık</span>
                <span>•</span>
                <span>{top3[1].upvotesCount} Beğeni</span>
              </div>
            </div>
          )}

          {/* 1st Place (Center / Taller) */}
          {top3[0] && (
            <div className="bg-gradient-to-b from-amber-50 to-white rounded-2xl border-2 border-amber-400 p-6 shadow-md flex flex-col items-center text-center relative order-1 md:order-2">
              <div className="absolute -top-3.5 bg-gradient-to-r from-amber-500 to-amber-600 text-white text-[10px] font-black uppercase tracking-wider px-3 py-1 rounded-full shadow-sm flex items-center gap-1">
                <CrownIcon className="w-3.5 h-3.5" />
                Dönem Lideri
              </div>
              <div className="w-14 h-14 rounded-full bg-amber-100 border-2 border-amber-400 flex items-center justify-center text-amber-800 font-black text-xl mb-3 mt-1 shadow-inner">
                🥇 1
              </div>
              <h4 className="font-black text-slate-900 text-base">{top3[0].name}</h4>
              {top3[0].studentNumber && (
                <span className="text-xs text-amber-800 font-mono mt-0.5 font-semibold">
                  Öğrenci No: {top3[0].studentNumber}
                </span>
              )}
              <div className="mt-4 bg-amber-500 text-white rounded-xl px-6 py-2.5 w-full shadow-xs">
                <span className="text-2xl font-black">{top3[0].totalPoints}</span>
                <span className="text-xs text-amber-100 block font-semibold">Toplam Katkı Puanı</span>
              </div>
              <div className="mt-3 text-xs text-slate-700 font-medium flex items-center gap-3">
                <span className="bg-amber-100/70 px-2 py-0.5 rounded text-amber-900">{top3[0].questionsCount} Soru Kökü</span>
                <span className="bg-amber-100/70 px-2 py-0.5 rounded text-amber-900">{top3[0].optionsCount} Şık</span>
                <span className="bg-amber-100/70 px-2 py-0.5 rounded text-amber-900">{top3[0].upvotesCount} Beğeni</span>
              </div>
            </div>
          )}

          {/* 3rd Place */}
          {top3[2] && (
            <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs flex flex-col items-center text-center relative order-3 mt-4 md:mt-8">
              <div className="w-10 h-10 rounded-full bg-amber-100/50 border border-amber-300 flex items-center justify-center text-amber-900 font-black text-sm mb-3">
                🥉 3
              </div>
              <h4 className="font-bold text-slate-900 text-sm">{top3[2].name}</h4>
              {top3[2].studentNumber && (
                <span className="text-[11px] text-slate-500 font-mono mt-0.5">No: {top3[2].studentNumber}</span>
              )}
              <div className="mt-3 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2 w-full">
                <span className="text-lg font-black text-slate-800">{top3[2].totalPoints}</span>
                <span className="text-xs text-slate-500 block">Puan</span>
              </div>
              <div className="mt-2 text-[11px] text-slate-600 flex items-center gap-3">
                <span>{top3[2].questionsCount} Soru</span>
                <span>•</span>
                <span>{top3[2].optionsCount} Şık</span>
                <span>•</span>
                <span>{top3[2].upvotesCount} Beğeni</span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Controls & Search */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => setFilterScope('current')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
              filterScope === 'current'
                ? 'bg-amber-500 text-white shadow-2xs'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
            }`}
          >
            Seçili Kurul Sıralaması
          </button>
          <button
            onClick={() => setFilterScope('all')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
              filterScope === 'all'
                ? 'bg-amber-500 text-white shadow-2xs'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
            }`}
          >
            Tüm Kurullar Genel Sıralama
          </button>
        </div>

        <div className="w-full sm:w-64">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Rumuz veya öğrenci no ara..."
            className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
        </div>
      </div>

      {/* Main Leaderboard Table */}
      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 uppercase tracking-wider text-[11px] font-bold">
              <tr>
                <th className="py-3 px-4 w-16 text-center">Sıra</th>
                <th className="py-3 px-4">Öğrenci Rumuzu</th>
                <th className="py-3 px-4">Öğrenci No</th>
                <th className="py-3 px-4 text-center">Eklenen Soru</th>
                <th className="py-3 px-4 text-center">Eklenen Şık</th>
                <th className="py-3 px-4 text-center">Alınan Beğeni</th>
                <th className="py-3 px-4 text-right">Toplam Puan</th>
                <th className="py-3 px-4 text-center">Durum</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredLeaderboard.map((item, index) => {
                const rank = index + 1;
                return (
                  <tr
                    key={item.id}
                    className={`transition-colors ${
                      item.isCurrentUser
                        ? 'bg-amber-50/80 font-semibold'
                        : index % 2 === 0
                        ? 'bg-white hover:bg-slate-50/60'
                        : 'bg-slate-50/40 hover:bg-slate-50'
                    }`}
                  >
                    <td className="py-3.5 px-4 text-center font-bold">
                      {rank === 1 ? (
                        <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-amber-400 text-white text-xs font-black shadow-2xs">
                          1
                        </span>
                      ) : rank === 2 ? (
                        <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-slate-300 text-slate-800 text-xs font-bold">
                          2
                        </span>
                      ) : rank === 3 ? (
                        <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-amber-200 text-amber-900 text-xs font-bold">
                          3
                        </span>
                      ) : (
                        <span className="text-slate-500 font-mono">{rank}</span>
                      )}
                    </td>

                    <td className="py-3.5 px-4">
                      <div className="flex items-center gap-2">
                        <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                          item.isCurrentUser ? 'bg-amber-500 text-white' : 'bg-slate-100 text-slate-700'
                        }`}>
                          {item.name.charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <div className="flex items-center gap-1.5">
                            <span className="font-bold text-slate-900">{item.name}</span>
                            {item.isCurrentUser && (
                              <span className="text-[10px] bg-amber-200 text-amber-900 px-1.5 py-0.2 rounded font-bold">
                                Sen
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </td>

                    <td className="py-3.5 px-4 font-mono text-slate-600">
                      {item.studentNumber ? (
                        <span>{item.studentNumber}</span>
                      ) : (
                        <span className="text-slate-400 italic text-[11px]">Belirtilmedi</span>
                      )}
                    </td>

                    <td className="py-3.5 px-4 text-center font-semibold text-slate-700">
                      {item.questionsCount > 0 ? (
                        <span className="bg-teal-50 text-teal-800 px-2 py-0.5 rounded-full border border-teal-200">
                          {item.questionsCount}
                        </span>
                      ) : (
                        <span className="text-slate-400">0</span>
                      )}
                    </td>

                    <td className="py-3.5 px-4 text-center font-semibold text-slate-700">
                      {item.optionsCount > 0 ? (
                        <span className="bg-cyan-50 text-cyan-800 px-2 py-0.5 rounded-full border border-cyan-200">
                          {item.optionsCount}
                        </span>
                      ) : (
                        <span className="text-slate-400">0</span>
                      )}
                    </td>

                    <td className="py-3.5 px-4 text-center font-semibold text-slate-700">
                      {item.upvotesCount > 0 ? (
                        <span className="text-emerald-700 flex items-center justify-center gap-1">
                          <ThumbsUp className="w-3 h-3" />
                          {item.upvotesCount}
                        </span>
                      ) : (
                        <span className="text-slate-400">0</span>
                      )}
                    </td>

                    <td className="py-3.5 px-4 text-right">
                      <span className="font-black text-sm text-amber-700">
                        {item.totalPoints} <span className="text-xs font-normal text-slate-500">puan</span>
                      </span>
                    </td>

                    <td className="py-3.5 px-4 text-center">
                      {item.totalPoints >= 50 ? (
                        <span className="inline-flex items-center gap-1 text-[10px] font-bold bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full border border-amber-300">
                          <Award className="w-3 h-3" />
                          Hafıza Ustası
                        </span>
                      ) : item.totalPoints > 0 ? (
                        <span className="inline-flex items-center gap-1 text-[10px] font-bold bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded-full border border-emerald-200">
                          <CheckCircle2 className="w-3 h-3" />
                          Aktif Katkıcı
                        </span>
                      ) : (
                        <span className="text-[10px] text-slate-400 italic">
                          Katkı Bekleniyor
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
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
