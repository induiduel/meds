import React, { useState, useMemo, useLayoutEffect, useRef } from 'react';
import { Segmented } from './ui/kit';
import { PageHeader } from './ui/PageHeader';
import { EmptySearch } from './ui/Animations';
import {
  ChevronDown,
  Sparkles,
  Search,
} from 'lucide-react';
import { QuestionItem, Committee } from '../types';
import { AppUser } from '../services/auth';
import { computeContributorStats } from '../utils/contributionScore';

interface LeaderboardViewProps {
  questions: QuestionItem[];
  committees: Committee[];
  selectedCommitteeId: string;
  onSelectCommittee: (id: string) => void;
  currentUser: AppUser | null;
  onOpenContributeModal: () => void;
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
  const listRef = useRef<HTMLOListElement>(null);
  const lastPos = useRef<Map<string, number>>(new Map());

  const currentCommittee = committees.find((c) => c.id === selectedCommitteeId);

  // Compute leaderboard from questions based on filterScope
  const leaderboard = useMemo(() => {
    const relevantQuestions = filterScope === 'current'
      ? questions.filter((q) => q.committeeId === selectedCommitteeId)
      : questions;

    return computeContributorStats(relevantQuestions, currentUser, { includeSamplePassive: true });
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

  // Canlı sıralama: sıra değişince satırlar eski yerinden yenisine kayar (FLIP)
  useLayoutEffect(() => {
    const ol = listRef.current;
    if (!ol) return;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const next = new Map<string, number>();
    ol.querySelectorAll<HTMLElement>('li[data-id]').forEach((li) => {
      const id = li.dataset.id!;
      const top = li.offsetTop;
      next.set(id, top);
      const prev = lastPos.current.get(id);
      if (!reduce && prev !== undefined && prev !== top) {
        li.animate([{ transform: `translateY(${prev - top}px)` }, { transform: 'none' }], { duration: 320, easing: 'cubic-bezier(.32,.72,0,1)' });
      }
    });
    lastPos.current = next;
  });
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
        {(
          <Segmented<'current' | 'all'>
            className="lb-scope"
            label="Kapsam"
            value={filterScope}
            onChange={setFilterScope}
            options={[{ value: 'current', label: 'Bu kurul' }, { value: 'all', label: 'Tüm kurullar' }]}
          />
        )}
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

      {/* İlk üç: basamaklı podyum (canvas "Leaderboard"; renkler tasarım sistemi tokenlarından) */}
      {top3.some((t) => t.totalPoints > 0) && (
        <ol className="lbx-podium" aria-label="İlk üç">
          {[1, 0, 2].map((i) => {
            const item = top3[i];
            if (!item) return <li key={i} className="lbx-col is-empty" aria-hidden />;
            const photo = item.isCurrentUser ? currentUser?.photoURL : null;
            return (
              <li key={item.id} className={`lbx-col t${i + 1} ${item.isCurrentUser ? 'is-me' : ''}`}>
                <span className="lbx-who">
                  {i === 0 && <CrownIcon className="lbx-crown" />}
                  <span className="lbx-av">{photo ? <img src={photo} alt="" /> : initials(item.name)}</span>
                  <b>{item.name}</b>
                </span>
                <span className="lbx-step">
                  <span className="lbx-rk">{i + 1}</span>
                  <span className="lbx-pt">{item.totalPoints} puan</span>
                </span>
              </li>
            );
          })}
        </ol>
      )}

      {/* Tam liste */}
      <section className="lbx-list" aria-label="Sıralama listesi">
        <label className="lbx-search">
          <Search aria-hidden />
          <input type="search" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} placeholder="Rumuz ya da öğrenci no ara" aria-label="Katkıcı ara" />
          <span className="lbx-count">{filteredLeaderboard.length} kişi</span>
        </label>
        <div className="lbx-row is-head" aria-hidden><span>SIRA</span><span /><span>KİŞİ</span><span>KATKI</span><span>PUAN</span></div>
        {filteredLeaderboard.length === 0 ? (
          <div className="ds-empty"><EmptySearch size={56} /><b>Aramaya uyan katkıcı yok</b></div>
        ) : (
          <ol className="lbx-rows" ref={listRef}>
            {filteredLeaderboard.map((item) => {
              const rank = leaderboard.indexOf(item) + 1;
              return (
                <li key={item.id} data-id={item.id} className={`lbx-row ${item.isCurrentUser ? 'is-me' : ''}`}>
                  <span className={`lbx-rank ${rank <= 3 ? `t${rank}` : ''}`}>{rank}</span>
                  <span className="lbx-av is-sm">{item.isCurrentUser && currentUser?.photoURL ? <img src={currentUser.photoURL} alt="" /> : initials(item.name)}</span>
                  <span className="lbx-name">
                    <b>{item.name}{item.isCurrentUser && <span className="lbx-me">Sen</span>}</b>
                    <span>{item.questionsCount} soru · {item.optionsCount} şık · {item.upvotesCount} beğeni</span>
                  </span>
                  <span className="lbx-bar" aria-hidden><i style={{ width: `${Math.max(item.totalPoints > 0 ? 3 : 0, (item.totalPoints / maxPoints) * 100)}%` }} /></span>
                  <span className="lbx-pts">{item.totalPoints}</span>
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
