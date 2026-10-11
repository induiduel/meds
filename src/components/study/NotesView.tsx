import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, Check, Download, Link2, NotebookPen, Pin, PinOff, Plus, Search, Trash2, X } from 'lucide-react';
import { StudyNote, getNotes, saveNotes, newNoteId, notesToMarkdown } from '../../services/studyStore';
import { disciplineClass, disciplineLabel } from '../../utils/discipline';
import { RichTextArea } from '../ui/RichTextArea';
import { TagInput } from '../ui/TagInput';

interface NotesViewProps {
  disciplines: string[];
}

const fmt = (iso: string) =>
  new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });

/** Biçim işaretlerini liste özetinden ayıklar */
const plain = (t: string) => t.replace(/^#{1,4}\s+|^-\s+|^\d+[.)]\s+|^(Not|Sınav):\s*/gim, '').replace(/\*\*/g, '').replace(/\n+/g, ' ').trim();

/**
 * v8 not defteri: ana-ayrıntı. Solda arama, ders ve etiket süzgeçli liste; sağda biçimli düzenleyici
 * (araç çubuğu, önizleme), etiket girişi, otomatik kayıt durumu. Telefonda liste → tam ekran düzenleyici.
 * Silme iki adımlıdır (tarayıcı onay penceresi yok). Notlar cihazda tutulur ve sunucuya yedeklenir
 * (services/notesSync: eşitleme kodu ile cihazlar arası aynı defter).
 */
export const NotesView: React.FC<NotesViewProps> = ({ disciplines }) => {
  const [notes, setNotes] = useState<StudyNote[]>(getNotes);
  const [activeId, setActiveId] = useState<string | null>(() => getNotes()[0]?.id || null);
  const [query, setQuery] = useState('');
  const [ders, setDers] = useState('all');
  const [tag, setTag] = useState<string | null>(null);
  const [mobileEditing, setMobileEditing] = useState(false);
  const [save, setSave] = useState<'idle' | 'saving' | 'saved'>('idle');
  const [mode, setMode] = useState<'write' | 'preview'>('write');
  const [confirmDel, setConfirmDel] = useState(false);
  const saveTimer = useRef<number | undefined>(undefined);
  const titleRef = useRef<HTMLInputElement>(null);

  const persist = (next: StudyNote[]) => {
    setNotes(next);
    setSave('saving');
    window.clearTimeout(saveTimer.current);
    saveTimer.current = window.setTimeout(() => {
      saveTimer.current = undefined;
      saveNotes(next);
      setSave('saved');
    }, 400);
  };
  useEffect(() => () => window.clearTimeout(saveTimer.current), []);
  // Arka plan eşitlemesi (notesSync) başka cihazdan gelen notları yazınca listeyi tazele
  useEffect(() => {
    const on = () => {
      if (saveTimer.current) return; // kullanıcı yazarken ekranı ezme
      setNotes(getNotes());
    };
    window.addEventListener('medsoru:notes-synced', on);
    return () => window.removeEventListener('medsoru:notes-synced', on);
  }, []);
  useEffect(() => {
    setConfirmDel(false);
    setMode('write');
  }, [activeId]);

  const allDisciplines = useMemo(
    () => [...new Set([...notes.map((n) => n.discipline).filter(Boolean), ...disciplines])].sort((a, b) => a.localeCompare(b, 'tr')),
    [notes, disciplines]
  );
  const allTags = useMemo(() => {
    const m = new Map<string, number>();
    notes.forEach((n) => (n.tags || []).forEach((t) => m.set(t, (m.get(t) || 0) + 1)));
    return [...m.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'tr'));
  }, [notes]);

  const visible = useMemo(() => {
    const q = query.trim().toLocaleLowerCase('tr-TR');
    return notes
      .filter((n) => ders === 'all' || n.discipline === ders)
      .filter((n) => !tag || (n.tags || []).includes(tag))
      .filter((n) => !q || `${n.title} ${n.body} ${n.questionStem || ''} ${(n.tags || []).join(' ')}`.toLocaleLowerCase('tr-TR').includes(q))
      .sort((a, b) => Number(!!b.pinned) - Number(!!a.pinned) || b.updatedAt.localeCompare(a.updatedAt));
  }, [notes, query, ders, tag]);

  const active = notes.find((n) => n.id === activeId) || null;

  const create = () => {
    const now = new Date().toISOString();
    const n: StudyNote = { id: newNoteId(), title: '', body: '', discipline: ders !== 'all' ? ders : '', tags: tag ? [tag] : [], createdAt: now, updatedAt: now };
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
    if (!active) return;
    if (!confirmDel) {
      setConfirmDel(true);
      window.setTimeout(() => setConfirmDel(false), 3500);
      return;
    }
    const next = notes.filter((n) => n.id !== active.id);
    persist(next);
    setActiveId(next[0]?.id || null);
    setMobileEditing(false);
  };

  const exportMd = () => {
    const blob = new Blob([`# MeDSor notlarım\n\n${notesToMarkdown(visible)}`], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `medsoru-notlar-${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };

  if (notes.length === 0) {
    return (
      <div className="ui-card nt-empty">
        <span className="ui-ico is-soft" style={{ width: 48, height: 48, borderRadius: 14 }}><NotebookPen className="w-6 h-6" /></span>
        <h3>Henüz notun yok</h3>
        <p>Konu özetlerini, hocanın vurguladıklarını ya da çözdüğün sorulardan çıkardıklarını burada tut. Soru çözerken “Not al” ile de ekleyebilirsin.</p>
        <button type="button" onClick={create} className="ui-btn is-primary"><Plus /> İlk notu yaz</button>
      </div>
    );
  }

  const words = active?.body.trim() ? plain(active.body).split(/\s+/).length : 0;

  return (
    <div className={`nt ${mobileEditing ? 'is-editing' : ''}`}>
      {/* ---------- Liste ---------- */}
      <aside className="nt-side" aria-label="Not listesi">
        <div className="nt-side-head">
          <label className="cx-search nt-search">
            <Search aria-hidden />
            <span className="sr-only">Notlarda ara</span>
            <input type="search" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Notlarda ara" />
            {query && <button type="button" className="cx-search-x" onClick={() => setQuery('')} aria-label="Aramayı temizle"><X /></button>}
          </label>
          <button type="button" onClick={create} className="ui-btn is-primary nt-new" aria-label="Yeni not" title="Yeni not">
            <Plus />
          </button>
        </div>
        <div className="nt-filters">
          <label className="ms-select-chip nt-ders">
            <span className="sr-only">Ders süzgeci</span>
            <select value={ders} onChange={(e) => setDers(e.target.value)} aria-label="Ders süzgeci">
              <option value="all">Tüm dersler ({notes.length})</option>
              {allDisciplines.filter((d) => notes.some((n) => n.discipline === d)).map((d) => (
                <option key={d} value={d}>{d} ({notes.filter((n) => n.discipline === d).length})</option>
              ))}
            </select>
          </label>
          <button type="button" onClick={exportMd} className="ui-btn is-ghost is-sm" title="Görünen notları Markdown olarak indir" aria-label="Notları indir">
            <Download />
          </button>
        </div>
        {allTags.length > 0 && (
          <div className="nt-tags" role="group" aria-label="Etiket süzgeci">
            {allTags.slice(0, 14).map(([t, c]) => (
              <button key={t} type="button" aria-pressed={tag === t} className="cx-fchip" onClick={() => setTag(tag === t ? null : t)}>
                #{t}<span className="n">{c}</span>
              </button>
            ))}
          </div>
        )}
        <ul className="nt-list">
          {visible.length === 0 && <li className="nt-none">Süzgeçlere uyan not yok.</li>}
          {visible.map((n) => (
            <li key={n.id} className={n.discipline ? disciplineClass(n.discipline) : ''}>
              <button
                type="button"
                onClick={() => { setActiveId(n.id); setMobileEditing(true); }}
                aria-current={n.id === activeId ? 'true' : undefined}
                className="nt-row"
              >
                <span className="nt-row-t">
                  {n.pinned && <Pin aria-label="Sabitli" />}
                  <b>{n.title || 'Başlıksız not'}</b>
                </span>
                <span className="nt-row-x">{plain(n.body) || 'Boş not'}</span>
                <span className="nt-row-m">
                  {n.discipline && <><i className="hk-dot" aria-hidden /><span>{disciplineLabel(n.discipline) || n.discipline}</span></>}
                  {(n.tags || []).slice(0, 2).map((t) => <span key={t} className="nt-row-tag">#{t}</span>)}
                  <span className="nt-row-d">{fmt(n.updatedAt)}</span>
                  {n.questionId && <Link2 aria-label="Soruya bağlı" />}
                </span>
              </button>
            </li>
          ))}
        </ul>
      </aside>

      {/* ---------- Düzenleyici ---------- */}
      <section className="nt-main" aria-label="Not düzenleyici">
        {!active ? (
          <div className="nt-pick">Soldan bir not seç ya da yeni not oluştur.</div>
        ) : (
          <>
            <div className="nt-bar">
              <button type="button" onClick={() => setMobileEditing(false)} className="ui-btn is-ghost is-sm nt-back" aria-label="Listeye dön">
                <ArrowLeft />
              </button>
              <label className="ms-select-chip nt-bar-ders">
                <span className="sr-only">Ders</span>
                <select value={active.discipline} onChange={(e) => update({ discipline: e.target.value })} aria-label="Ders">
                  <option value="">Ders seç</option>
                  {allDisciplines.map((d) => <option key={d} value={d}>{d}</option>)}
                </select>
              </label>
              <span className="flex-1" />
              <span className={`nt-save is-${save}`} role="status" aria-live="polite">
                {save === 'saving' ? 'Kaydediliyor…' : save === 'saved' ? <><Check /> Kaydedildi</> : ''}
              </span>
              <button
                type="button"
                onClick={() => update({ pinned: !active.pinned })}
                aria-pressed={!!active.pinned}
                aria-label={active.pinned ? 'Sabitlemeyi kaldır' : 'Sabitle'}
                title={active.pinned ? 'Sabitlemeyi kaldır' : 'Sabitle'}
                className={`ui-btn is-sm ${active.pinned ? 'is-tonal' : 'is-ghost'}`}
              >
                {active.pinned ? <PinOff /> : <Pin />}
              </button>
              <button type="button" onClick={remove} className={`ui-btn is-sm ${confirmDel ? 'is-danger' : 'is-ghost'}`} aria-label={confirmDel ? 'Silmeyi onayla' : 'Notu sil'} title="Notu sil">
                <Trash2 />{confirmDel && <span>Sil?</span>}
              </button>
            </div>

            <div className="nt-doc">
              <label className="sr-only" htmlFor="note-title">Başlık</label>
              <input id="note-title" ref={titleRef} value={active.title} onChange={(e) => update({ title: e.target.value })} placeholder="Başlık" className="nt-title" />
              {active.questionStem && (
                <div className="nt-link">
                  <Link2 aria-hidden />
                  <span>{active.questionStem}</span>
                </div>
              )}
              <TagInput
                label="Etiketler"
                value={active.tags || []}
                onChange={(tags) => update({ tags })}
                suggestions={allTags.map(([t]) => t)}
                placeholder="Etiket ekle (Enter)"
              />
              <RichTextArea
                id="note-body"
                label="Not"
                value={active.body}
                onChange={(body) => update({ body })}
                mode={mode}
                onModeChange={setMode}
                placeholder={'Notunu yaz…\n- Madde için satır başına tire\n## Başlık · **kalın** · Not: önemli satır'}
              />
              <p className="nt-foot">
                <span>Oluşturuldu {fmt(active.createdAt)} · {words} kelime</span>
                <span>Notlar yalnız bu cihazda saklanır.</span>
              </p>
            </div>
          </>
        )}
      </section>
    </div>
  );
};
