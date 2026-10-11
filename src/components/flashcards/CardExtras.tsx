import React, { useEffect, useRef, useState } from 'react';
import { ChevronDown, Flag, NotebookPen } from 'lucide-react';
import { ReportQuestionModal } from '../ReportQuestionModal';
import { ApiService } from '../../services/api';
import { sendFeedback } from '../learn/lesson/lessonFeedback';
import { toast } from '../ui/Toast';

/**
 * Ezber kartının altındaki iki ek: açılıp kapanan "Notum" (kart başına, cihazda saklanır) ve
 * "Hata bildir". Deste kartları Öğren geri bildirim kuyruğuna, sözlük kartları terim bildirimine gider.
 */
const NOTES_KEY = 'medsoru_card_notes_v1';
const OPEN_KEY = 'medsoru_card_note_open';

const readNotes = (): Record<string, string> => {
  try { return JSON.parse(localStorage.getItem(NOTES_KEY) || '{}') || {}; } catch { return {}; }
};
const writeNote = (id: string, text: string) => {
  try {
    const all = readNotes();
    if (text.trim()) all[id] = text; else delete all[id];
    localStorage.setItem(NOTES_KEY, JSON.stringify(all));
  } catch { /* yoksay */ }
};

interface Props {
  card: { id: string; front: string; back: string; group?: string };
}

export const CardExtras: React.FC<Props> = ({ card }) => {
  const [note, setNote] = useState(() => readNotes()[card.id] || '');
  const [open, setOpen] = useState(() => {
    try { return localStorage.getItem(OPEN_KEY) === '1'; } catch { return false; }
  });
  const [reporting, setReporting] = useState(false);
  const timer = useRef<number | undefined>(undefined);

  // Kart değişince o kartın notu yüklenir.
  useEffect(() => { setNote(readNotes()[card.id] || ''); }, [card.id]);
  useEffect(() => () => window.clearTimeout(timer.current), []);

  const onChange = (v: string) => {
    setNote(v);
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => writeNote(card.id, v), 400);
  };
  const toggle = () => {
    setOpen((o) => {
      try { localStorage.setItem(OPEN_KEY, o ? '0' : '1'); } catch { /* yoksay */ }
      return !o;
    });
  };

  const submitReport = async (reason: string, details: string) => {
    const text = [reason, details].filter(Boolean).join(' · ');
    if (card.id.startsWith('d:')) {
      const [, deckId, slide] = card.id.split(':');
      await sendFeedback(deckId, { key: `card:${card.id}`, label: card.front.slice(0, 80), slideNumber: Number(slide) || 0, location: 'Ezber kartı' }, 'kart', text, card.group || '');
    } else if (card.id.startsWith('g:')) {
      await ApiService.reportTerm(card.id.slice(2), reason, details);
    } else {
      await ApiService.reportTerm(card.id, reason, `${details}\nKart: ${card.front}`);
    }
    toast.success('Bildirim alındı', 'Kart incelemeye gönderildi.');
  };

  return (
    <div className="rb-cardx">
      <div className={`rb-note ${open ? 'is-open' : ''}`}>
        <button type="button" className="rb-note-h" aria-expanded={open} onClick={toggle}>
          <span className="rb-note-ic" aria-hidden><NotebookPen /></span>
          <b>Notum</b>
          {!open && <span className="rb-note-prev">{note.trim() ? note.trim().split('\n')[0] : 'Bu karta not ekle'}</span>}
          <ChevronDown className={`rb-note-chev ${open ? 'is-open' : ''}`} aria-hidden />
        </button>
        {open && (
          <div className="rb-note-b">
            <textarea
              value={note}
              onChange={(e) => onChange(e.target.value)}
              rows={3}
              placeholder="Bu kartla ilgili kendi hatırlatman"
              aria-label="Bu kart için notun"
              onKeyDown={(e) => e.stopPropagation()}
            />
            <span className="rb-note-meta">Yalnız sen görürsün · otomatik kaydedilir</span>
          </div>
        )}
      </div>
      <button type="button" className="rb-cardx-report" onClick={() => setReporting(true)}>
        <Flag aria-hidden /> Hata bildir
      </button>
      {reporting && (
        <ReportQuestionModal
          question={{ stem: card.front, discipline: card.group, questionNumber: card.id }}
          onClose={() => setReporting(false)}
          onSubmit={submitReport}
        />
      )}
    </div>
  );
};
