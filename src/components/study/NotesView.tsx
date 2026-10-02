import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Plus, Search, Pin, PinOff, Trash2, Download, ArrowLeft, Link2 } from 'lucide-react';
import { StudyNote, getNotes, saveNotes, newNoteId, notesToMarkdown } from '../../services/studyStore';
import { cardCls, btnPrimary, btnSecondary, btnGhost, selectCls, EmptyState } from './StudyUI';

interface NotesViewProps {
  disciplines: string[];
}

const fmt = (iso: string) =>
  new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });

export const NotesView: React.FC<NotesViewProps> = ({ disciplines }) => {
  const [notes, setNotes] = useState<StudyNote[]>(getNotes);
  const [activeId, setActiveId] = useState<string | null>(() => getNotes()[0]?.id || null);
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('all');
  const [mobileEditing, setMobileEditing] = useState(false);
  const [savedAt, setSavedAt] = useState<string | null>(null);
  const saveTimer = useRef<number | undefined>(undefined);
  const titleRef = useRef<HTMLInputElement>(null);

  // Debounced persistence
  const persist = (next: StudyNote[]) => {
    setNotes(next);
    window.clearTimeout(saveTimer.current);
    saveTimer.current = window.setTimeout(() => {
      saveNotes(next);
      setSavedAt(new Date().toISOString());
    }, 400);
  };
  useEffect(() => () => window.clearTimeout(saveTimer.current), []);

  const allDisciplines = useMemo(
    () => [...new Set([...notes.map((n) => n.discipline).filter(Boolean), ...disciplines])].sort((a, b) => a.localeCompare(b, 'tr')),
    [notes, disciplines]
  );

  const visible = useMemo(() => {
    const q = query.trim().toLocaleLowerCase('tr-TR');
    return notes
      .filter((n) => filter === 'all' || n.discipline === filter)
      .filter((n) => !q || `${n.title} ${n.body} ${n.questionStem || ''}`.toLocaleLowerCase('tr-TR').includes(q))
      .sort((a, b) => Number(!!b.pinned) - Number(!!a.pinned) || b.updatedAt.localeCompare(a.updatedAt));
  }, [notes, query, filter]);

  const active = notes.find((n) => n.id === activeId) || null;

  const create = () => {
    const now = new Date().toISOString();
    const n: StudyNote = { id: newNoteId(), title: '', body: '', discipline: filter !== 'all' ? filter : '', createdAt: now, updatedAt: now };
    persist([n, ...notes]);
    setActiveId(n.id);
    setMobileEditing(true);
    setTimeout(() => titleRef.current?.focus(), 0);
  };

  const update = (patch: Partial<StudyNote>) => {
    if (!active) return;
    persist(notes.map((n) => (n.id === active.id ? { ...n, ...patch, updatedAt: new Date().toISOString() } : n)));
  };

  const remove = () => {
    if (!active || !window.confirm('Bu not silinsin mi?')) return;
    const next = notes.filter((n) => n.id !== active.id);
    persist(next);
    setActiveId(next[0]?.id || null);
    setMobileEditing(false);
  };

  const exportMd = () => {
    const blob = new Blob([`# MedSoru notlarım\n\n${notesToMarkdown(visible)}`], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `medsoru-notlar-${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };

  if (notes.length === 0) {
    return (
      <EmptyState
        title="Henüz notun yok"
        body="Konu özetlerini, hocanın vurguladıklarını ya da çözdüğün sorulardan çıkardıklarını burada tut. Soru çözerken “Not al” ile de ekleyebilirsin."
        action={
          <button type="button" onClick={create} className={btnPrimary}>
            <Plus className="w-4 h-4" /> İlk notu yaz
          </button>
        }
      />
    );
  }

  return (
    <div className={`${cardCls} grid grid-cols-1 md:grid-cols-[300px_minmax(0,1fr)] overflow-hidden min-h-[560px]`}>
      {/* ---------- List ---------- */}
      <aside aria-label="Not listesi" className={`${mobileEditing ? 'hidden md:flex' : 'flex'} flex-col border-b md:border-b-0 md:border-r border-line min-w-0`}>
        <div className="p-3 flex flex-col gap-2 border-b border-line">
          <div className="flex gap-2">
            <label className="flex items-center gap-2 h-10 px-3 border border-line-2 rounded-[10px] bg-field flex-1 min-w-0 focus-within:border-accent">
              <Search className="w-4 h-4 text-ink-2 shrink-0" />
              <span className="sr-only">Notlarda ara</span>
              <input
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Notlarda ara"
                className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[14px]"
              />
            </label>
            <button type="button" onClick={create} aria-label="Yeni not" className="w-10 h-10 rounded-[10px] bg-accent hover:bg-accent-hover text-white flex items-center justify-center cursor-pointer shrink-0">
              <Plus className="w-4 h-4" />
            </button>
          </div>
          <div className="flex gap-2">
            <label className="sr-only" htmlFor="notes-filter">
              Ders filtresi
            </label>
            <select id="notes-filter" value={filter} onChange={(e) => setFilter(e.target.value)} className={`${selectCls} h-9 flex-1 text-[13px]`}>
              <option value="all">Tüm dersler ({notes.length})</option>
              {allDisciplines
                .filter((d) => notes.some((n) => n.discipline === d))
                .map((d) => (
                  <option key={d} value={d}>
                    {d} ({notes.filter((n) => n.discipline === d).length})
                  </option>
                ))}
            </select>
            <button type="button" onClick={exportMd} title="Görünen notları Markdown olarak indir" aria-label="Notları indir" className="w-9 h-9 rounded-[10px] border border-line-2 flex items-center justify-center cursor-pointer hover:border-ink-3 shrink-0">
              <Download className="w-4 h-4 text-ink-2" />
            </button>
          </div>
        </div>
        <ul className="list-none m-0 p-1.5 flex flex-col gap-0.5 overflow-y-auto md:max-h-[640px]">
          {visible.length === 0 && <li className="px-3 py-6 text-[14px] text-ink-2">Aramana uyan not yok.</li>}
          {visible.map((n) => {
            const on = n.id === activeId;
            return (
              <li key={n.id}>
                <button
                  type="button"
                  onClick={() => {
                    setActiveId(n.id);
                    setMobileEditing(true);
                  }}
                  aria-current={on ? 'true' : undefined}
                  className={`w-full text-left px-3 py-2.5 rounded-[10px] flex flex-col gap-0.5 cursor-pointer ${on ? 'bg-accent-soft' : 'hover:bg-canvas'}`}
                >
                  <span className="flex items-center gap-1.5 min-w-0">
                    {n.pinned && <Pin className="w-3.5 h-3.5 text-accent shrink-0" />}
                    <span className={`text-[14px] font-semibold truncate ${on ? 'text-accent' : 'text-ink'}`}>{n.title || 'Başlıksız not'}</span>
                  </span>
                  <span className="text-[13px] text-ink-2 line-clamp-2">{n.body || 'Boş not'}</span>
                  <span className="text-[11px] text-ink-3 flex gap-1.5 items-center">
                    {n.discipline && <span className="truncate">{n.discipline}</span>}
                    {n.discipline && <span aria-hidden="true">·</span>}
                    <span className="shrink-0">{fmt(n.updatedAt)}</span>
                    {n.questionId && <Link2 className="w-3 h-3 shrink-0" aria-label="Soruya bağlı" />}
                  </span>
                </button>
              </li>
            );
          })}
        </ul>
      </aside>

      {/* ---------- Editor ---------- */}
      <section aria-label="Not düzenleyici" className={`${mobileEditing ? 'flex' : 'hidden md:flex'} flex-col min-w-0`}>
        {!active ? (
          <div className="flex-1 flex items-center justify-center p-8 text-[14px] text-ink-2">Soldan bir not seç ya da yeni not oluştur.</div>
        ) : (
          <>
            <div className="flex items-center gap-1.5 px-3 py-2 border-b border-line">
              <button type="button" onClick={() => setMobileEditing(false)} className={`${btnGhost} md:hidden px-2`} aria-label="Listeye dön">
                <ArrowLeft className="w-4 h-4" />
              </button>
              <label className="sr-only" htmlFor="note-discipline">
                Ders
              </label>
              <select id="note-discipline" value={active.discipline} onChange={(e) => update({ discipline: e.target.value })} className={`${selectCls} h-9 text-[13px] max-w-[200px]`}>
                <option value="">Ders seç</option>
                {allDisciplines.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
              <span className="flex-1" />
              <span className="hidden sm:inline text-[12px] text-ink-3 mr-1" role="status">
                {savedAt ? 'Kaydedildi' : ''}
              </span>
              <button
                type="button"
                onClick={() => update({ pinned: !active.pinned })}
                aria-pressed={!!active.pinned}
                aria-label={active.pinned ? 'Sabitlemeyi kaldır' : 'Sabitle'}
                title={active.pinned ? 'Sabitlemeyi kaldır' : 'Sabitle'}
                className={`w-9 h-9 rounded-lg flex items-center justify-center cursor-pointer ${active.pinned ? 'bg-accent-soft text-accent' : 'text-ink-2 hover:bg-canvas'}`}
              >
                {active.pinned ? <PinOff className="w-4 h-4" /> : <Pin className="w-4 h-4" />}
              </button>
              <button type="button" onClick={remove} aria-label="Notu sil" title="Notu sil" className="w-9 h-9 rounded-lg flex items-center justify-center text-ink-2 hover:text-bad-text hover:bg-bad-soft cursor-pointer">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>

            <div className="flex-1 flex flex-col gap-3 p-4 sm:p-5">
              <label className="sr-only" htmlFor="note-title">
                Başlık
              </label>
              <input
                id="note-title"
                ref={titleRef}
                value={active.title}
                onChange={(e) => update({ title: e.target.value })}
                placeholder="Başlık"
                className="border-0 outline-0 bg-transparent font-display text-[22px] sm:text-[24px] font-bold tracking-[-0.02em] placeholder:text-[#AEB8C3]"
              />
              {active.questionStem && (
                <div className="flex gap-2 items-start rounded-[10px] bg-canvas px-3 py-2.5 text-[13px] text-ink-2">
                  <Link2 className="w-4 h-4 shrink-0 mt-0.5" />
                  <span className="line-clamp-3">{active.questionStem}</span>
                </div>
              )}
              <label className="sr-only" htmlFor="note-body">
                Not
              </label>
              <textarea
                id="note-body"
                value={active.body}
                onChange={(e) => update({ body: e.target.value })}
                placeholder="Notunu yaz… Madde için satır başına - koyabilirsin."
                className="flex-1 min-h-[320px] resize-none border-0 outline-0 bg-transparent text-[15px] leading-[1.65] placeholder:text-[#8B96A3]"
              />
              <div className="flex flex-wrap items-center justify-between gap-2 border-t border-line-soft pt-3 text-[12px] text-ink-3">
                <span>
                  Oluşturuldu {fmt(active.createdAt)} · {active.body.trim() ? active.body.trim().split(/\s+/).length : 0} kelime
                </span>
                <span>Notlar yalnızca bu cihazda saklanır.</span>
              </div>
            </div>
          </>
        )}
      </section>
    </div>
  );
};
