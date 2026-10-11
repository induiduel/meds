import React, { useEffect, useRef, useState } from 'react';
import { ListPlus } from 'lucide-react';
import { RichTextArea } from '../../ui/RichTextArea';
import { getNotes, saveNotes, StudyNote } from '../../../services/studyStore';

/**
 * Öğren oynatıcısında "Notlarım": deste başına tek, biçimli not. Notlar sayfasındaki defterle aynı
 * depoda (`medsoru_notes_v1`) tutulur; Notlar ekranında da görünür ve düzenlenebilir.
 * Yazılanlar 600 ms durunca otomatik kaydedilir.
 */
interface Props {
  deckId: string;
  deckTitle: string;
  discipline?: string;
  stepNumber: number;
  stepTitle: string;
}

const noteIdFor = (deckId: string) => `deck-note-${deckId}`;

export const DeckNotePanel: React.FC<Props> = ({ deckId, deckTitle, discipline, stepNumber, stepTitle }) => {
  const id = noteIdFor(deckId);
  const [body, setBody] = useState(() => getNotes().find((n) => n.id === id)?.body || '');
  const [mode, setMode] = useState<'write' | 'preview'>(() => (body.trim() ? 'preview' : 'write'));
  const [savedAt, setSavedAt] = useState<string | null>(null);
  const timer = useRef<number | undefined>(undefined);
  const first = useRef(true);

  useEffect(() => {
    if (first.current) { first.current = false; return; }
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => {
      const now = new Date().toISOString();
      const notes = getNotes();
      const existing = notes.find((n) => n.id === id);
      if (!body.trim() && !existing) return;
      const note: StudyNote = existing
        ? { ...existing, body, updatedAt: now }
        : { id, title: deckTitle, body, discipline: discipline || '', tags: ['Öğren'], createdAt: now, updatedAt: now };
      saveNotes(existing ? notes.map((n) => (n.id === id ? note : n)) : [note, ...notes]);
      setSavedAt(new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }));
    }, 600);
    return () => window.clearTimeout(timer.current);
  }, [body, id, deckTitle, discipline]);

  const addStepHeading = () => {
    const heading = `## Adım ${stepNumber} · ${stepTitle}`;
    if (body.includes(heading)) return;
    setBody((b) => `${b.trimEnd()}${b.trim() ? '\n\n' : ''}${heading}\n- `);
    setMode('write');
  };

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-2">
        <button type="button" onClick={addStepHeading} className="ls-btn is-sm" title="Bu adımın başlığını nota ekle">
          <ListPlus aria-hidden /> Bu adımı ekle
        </button>
        <span className="flex-1" />
        <span className="text-xs text-ink-3" aria-live="polite">{savedAt ? `Kaydedildi · ${savedAt}` : 'Otomatik kaydedilir'}</span>
      </div>
      <RichTextArea
        id={`deck-note-${deckId}`}
        label="Bu ders için notun"
        value={body}
        onChange={setBody}
        mode={mode}
        onModeChange={setMode}
        placeholder="Notunu yaz. Madde için '- ', alt madde için Tab, tablo için araç çubuğundaki tablo düğmesi."
      />
    </div>
  );
};
