import React, { useMemo, useState } from 'react';
import { Star, RotateCcw, Layers, Trash2 } from 'lucide-react';
import {
  StudyQuestion,
  getReview,
  setInReview,
  getFavorites,
  setFavorite,
  getFavoriteCards,
  toggleFavoriteCard,
  getProgress,
} from '../../services/studyStore';
import { Collapsible } from '../ui/Collapsible';
import { ExplanationBlock, EmptyState } from './StudyUI';

type ListId = 'review' | 'favorites' | 'cards';

interface ListsViewProps {
  bank: StudyQuestion[];
  onChange?: () => void;
}

/** Tekrar listesi, favori sorular ve favori kartlar tek ekranda. */
export const ListsView: React.FC<ListsViewProps> = ({ bank, onChange }) => {
  const [list, setList] = useState<ListId>('review');
  const [review, setReview] = useState(getReview);
  const [favorites, setFavorites] = useState(getFavorites);
  const [cards, setCards] = useState(getFavoriteCards);
  const byId = useMemo(() => new Map(bank.map((q) => [q.id, q])), [bank]);
  const progress = useMemo(getProgress, [review]);

  const reviewQs = [...review].map((id) => byId.get(id)).filter((q): q is StudyQuestion => !!q);
  const favoriteQs = [...favorites].map((id) => byId.get(id)).filter((q): q is StudyQuestion => !!q);

  const tabs: { id: ListId; label: string; icon: React.ElementType; count: number }[] = [
    { id: 'review', label: 'Tekrar', icon: RotateCcw, count: reviewQs.length },
    { id: 'favorites', label: 'Favori sorular', icon: Star, count: favoriteQs.length },
    { id: 'cards', label: 'Favori kartlar', icon: Layers, count: cards.length },
  ];

  const removeReview = (id: string) => { setReview(new Set(setInReview(id, false))); onChange?.(); };
  const removeFavorite = (id: string) => { setFavorites(new Set(setFavorite(id, false))); onChange?.(); };

  const QuestionRow: React.FC<{ q: StudyQuestion; onRemove: () => void; removeLabel: string }> = ({ q, onRemove, removeLabel }) => {
    const attempt = progress[q.id];
    return (
      <li className="bg-white border border-line rounded-2xl px-1 min-w-0">
        <Collapsible
          title={
            <span className="flex flex-col gap-0.5 py-2 min-w-0 text-left">
              <span className="text-[12px] text-ink-3 font-normal truncate">
                {[q.discipline, q.year, attempt ? (attempt.correct ? 'Doğru çözdün' : `Yanlış · ${attempt.picked}`) : null].filter(Boolean).join(' · ')}
              </span>
              <span className="text-[15px] text-ink font-medium line-clamp-2 whitespace-normal">{q.stem}</span>
            </span>
          }
        >
          <div className="px-3 pb-3 flex flex-col gap-2">
            <ol className="m-0 p-0 list-none flex flex-col gap-1 text-[14px]">
              {q.options.map((o) => (
                <li key={o.key} className={`flex gap-2 rounded-lg px-2.5 py-1.5 ${o.key === q.answer ? 'bg-ok-soft text-ok font-semibold' : 'text-ink-2'}`}>
                  <span className="font-mono shrink-0">{o.key})</span>
                  <span className="min-w-0 [overflow-wrap:anywhere]">{o.text}</span>
                </li>
              ))}
            </ol>
            <ExplanationBlock q={q} compact />
            <button type="button" onClick={onRemove} className="self-start h-9 px-3 rounded-full text-[13px] font-medium text-ink-3 hover:text-ink hover:bg-field inline-flex items-center gap-1.5 cursor-pointer">
              <Trash2 className="w-3.5 h-3.5" /> {removeLabel}
            </button>
          </div>
        </Collapsible>
      </li>
    );
  };

  return (
    <div className="flex flex-col gap-3">
      <div className="ms-f-seg max-w-full sm:max-w-[520px]" role="tablist" aria-label="Listeler">
        {tabs.map((t) => (
          <button key={t.id} type="button" role="tab" aria-selected={list === t.id} onClick={() => setList(t.id)} className={`inline-flex items-center justify-center gap-1.5 ${list === t.id ? 'is-on' : ''}`}>
            <t.icon className="w-3.5 h-3.5" />
            {t.label}
            <span className="text-ink-3 text-[12px]">{t.count}</span>
          </button>
        ))}
      </div>

      {list === 'review' && (
        reviewQs.length === 0 ? (
          <EmptyState title="Tekrar listen boş" body="Yanlış çözdüğün ya da işaretlediğin sorular burada toplanır." />
        ) : (
          <ul className="m-0 p-0 list-none flex flex-col gap-2">
            {reviewQs.map((q) => <QuestionRow key={q.id} q={q} onRemove={() => removeReview(q.id)} removeLabel="Listeden çıkar" />)}
          </ul>
        )
      )}

      {list === 'favorites' && (
        favoriteQs.length === 0 ? (
          <EmptyState title="Favori sorun yok" body="Soru çözerken yıldıza dokunarak favorilere ekleyebilirsin." />
        ) : (
          <ul className="m-0 p-0 list-none flex flex-col gap-2">
            {favoriteQs.map((q) => <QuestionRow key={q.id} q={q} onRemove={() => removeFavorite(q.id)} removeLabel="Favorilerden çıkar" />)}
          </ul>
        )
      )}

      {list === 'cards' && (
        cards.length === 0 ? (
          <EmptyState title="Favori kartın yok" body="Kartlar bölümünde yıldıza dokunarak ekleyebilirsin." />
        ) : (
          <ul className="m-0 p-0 list-none grid grid-cols-1 md:grid-cols-2 gap-2">
            {cards.map((c) => (
              <li key={c.id} className="bg-white border border-line rounded-2xl p-4 flex flex-col gap-1.5 min-w-0">
                <div className="flex items-start gap-2 min-w-0">
                  <span className="flex-1 min-w-0 font-semibold text-[15px] text-ink [overflow-wrap:anywhere]">{c.front}</span>
                  <button
                    type="button"
                    onClick={() => setCards(toggleFavoriteCard({ id: c.id, front: c.front, back: c.back, group: c.group }))}
                    aria-label="Favorilerden çıkar"
                    className="w-8 h-8 -m-1 rounded-full flex items-center justify-center text-amber-500 hover:bg-amber-50 cursor-pointer shrink-0"
                  >
                    <Star className="w-4 h-4" fill="currentColor" />
                  </button>
                </div>
                {c.group && <span className="text-[12px] text-ink-3">{c.group}</span>}
                <p className="m-0 text-[14px] text-ink-2 leading-[1.6] line-clamp-4 [overflow-wrap:anywhere]">{c.back}</p>
              </li>
            ))}
          </ul>
        )
      )}
    </div>
  );
};
