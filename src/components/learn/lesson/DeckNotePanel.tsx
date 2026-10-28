import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ListPlus, Quote, Sparkles, ListChecks, CornerDownRight } from 'lucide-react';
import { RichTextArea } from '../../ui/RichTextArea';
import { getNotes, saveNotes, StudyNote } from '../../../services/studyStore';
import { toast } from '../../ui/Toast';
import '../../../styles/ogren-ders.css';

/**
 * Öğren oynatıcısında "Notlarım": deste başına tek, biçimli not. Notlar sayfasındaki defterle aynı
 * depoda (`medsoru_notes_v1`) tutulur, sunucuya yedeklenir (services/notesSync) ve Notlar ekranında da düzenlenir.
 * Hızlı ekleme: bu adımın başlığı, derste seçili metin (alıntı), adımın spotları ve ana maddeleri (kontrol listesi).
 * Nottaki "Adım N" başlıkları çip olur: dokununca derste o adıma gidilir. Yazılanlar 600 ms durunca kaydedilir.
 */
interface Props {
  deckId: string;
  deckTitle: string;
  discipline?: string;
  stepNumber: number;
  stepTitle: string;
  spots?: string[];
  bullets?: string[];
  onJump?: (stepNumber: number) => void;
}

const noteIdFor = (deckId: string) => `deck-note-${deckId}`;
const STEP_RE = /^## Adım (\d+) · (.+)$/gm;

export const DeckNotePanel: React.FC<Props> = ({ deckId, deckTitle, discipline, stepNumber, stepTitle, spots = [], bullets = [], onJump }) => {
  const id = noteIdFor(deckId);
  const [body, setBody] = useState(() => getNotes().find((n) => n.id === id)?.body || '');
  const [mode, setMode] = useState<'write' | 'preview'>(() => (body.trim() ? 'preview' : 'write'));
  const [savedAt, setSavedAt] = useState<string | null>(null);
  const timer = useRef<number | undefined>(undefined);
  const first = useRef(true);
  // Panel açılınca kaybolmasın diye derste son seçilen metin tutulur
  const lastSel = useRef('');
  useEffect(() => {
    const on = () => {
      const sel = window.getSelection();
      const t = sel && !sel.isCollapsed ? sel.toString().trim() : '';
      const inLesson = sel?.anchorNode && (sel.anchorNode.parentElement?.closest('.ls-col, .ls-B-body') as Element | null);
      if (t && inLesson) lastSel.current = t.slice(0, 600);
    };
    document.addEventListener('selectionchange', on);
    return () => document.removeEventListener('selectionchange', on);
  }, []);

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

  const heading = `## Adım ${stepNumber} · ${stepTitle}`;
  /** Bu adımın başlığının altına (yoksa başlıkla birlikte) satır ekler */
  const appendUnderStep = (lines: string[]) => {
    setBody((b) => {
      const text = lines.join('\n');
      if (!b.includes(heading)) return `${b.trimEnd()}${b.trim() ? '\n\n' : ''}${heading}\n${text}\n`;
      // Başlığın bölümünün sonuna ekle (bir sonraki "## " başlığından önce)
      const start = b.indexOf(heading) + heading.length;
      const next = b.indexOf('\n## ', start);
      const end = next === -1 ? b.length : next;
      return `${b.slice(0, end).trimEnd()}\n${text}\n${b.slice(end)}`;
    });
    setMode('write');
  };

  const addStepHeading = () => {
    if (body.includes(heading)) return toast.info('Bu adım zaten notta');
    appendUnderStep(['- ']);
  };
  const quoteSelection = () => {
    const sel = window.getSelection()?.toString().trim() || lastSel.current;
    if (!sel) return toast.info('Önce dersten bir metin seç', 'Seçtiğin cümle alıntı olarak bu adımın altına eklenir.');
    appendUnderStep(sel.split(/\n+/).map((l) => `> ${l.trim()}`));
    lastSel.current = '';
  };
  const addSpots = () => {
    if (!spots.length) return toast.info('Bu adımda spot yok');
    appendUnderStep(spots.map((x) => `- ==${x.replace(/\s+/g, ' ').trim()}==`));
  };
  const addChecklist = () => {
    const items = bullets.filter(Boolean);
    if (!items.length) return toast.info('Bu adımda ana madde yok');
    appendUnderStep(items.map((x) => `- [ ] ${x.replace(/\s+/g, ' ').trim()}`));
  };

  const stepsInNote = useMemo(() => Array.from(body.matchAll(STEP_RE), (m) => ({ n: Number(m[1]), t: m[2] })), [body]);

  return (
    <div className="flex flex-col gap-2">
      <div className="ls-note-tools" role="toolbar" aria-label="Nota hızlı ekle">
        <button type="button" onClick={addStepHeading} className="ls-btn is-sm" title="Bu adımın başlığını nota ekle"><ListPlus aria-hidden /> Adım</button>
        <button type="button" onClick={quoteSelection} className="ls-btn is-sm" title="Derste seçtiğin metni alıntı olarak ekle"><Quote aria-hidden /> Alıntı</button>
        <button type="button" onClick={addSpots} className="ls-btn is-sm" disabled={!spots.length} title="Bu adımın sınav spotlarını vurgulu ekle"><Sparkles aria-hidden /> Spotlar</button>
        <button type="button" onClick={addChecklist} className="ls-btn is-sm" disabled={!bullets.length} title="Ana maddeleri tekrar listesi olarak ekle"><ListChecks aria-hidden /> Liste</button>
        <span className="flex-1" />
        <span className="text-xs text-ink-3" aria-live="polite">{savedAt ? `Kaydedildi · ${savedAt}` : 'Otomatik kaydedilir'}</span>
      </div>
      {stepsInNote.length > 0 && onJump && (
        <div className="ls-note-steps" aria-label="Nottaki adımlar">
          {stepsInNote.map((s) => (
            <button key={s.n} type="button" className={`ls-note-step ${s.n === stepNumber ? 'is-cur' : ''}`} onClick={() => onJump(s.n)} title={`Adım ${s.n}: ${s.t}`}>
              <CornerDownRight aria-hidden /> {s.n}
            </button>
          ))}
        </div>
      )}
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
