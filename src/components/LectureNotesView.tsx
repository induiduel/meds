import React, { useState, useEffect, useMemo } from 'react';
import { confirmDialog } from './ui/ConfirmDialog';
import { SourceText } from './ui/SourceText';
import { FilterPills, PageToolbar, type ToolbarChip } from './ui/PageToolbar';
import { Sheet } from './ui/Sheet';
import { useReaderPrefs } from './summary/readerStore';
import {
  BookMarked,
  Search,
  CheckCircle2,
  ExternalLink,
  Copy,
  Check,
  UploadCloud,
  FileUp,
  RefreshCw,
  FolderGit2,
  Trash2,
  Play,
  Eye,
  Plus,
  BookOpen,
  FolderOpen,
  X,
  ListTree,
  FileText,
  ChevronRight,
} from 'lucide-react';
import { LectureNote, QuestionItem, QuestionLectureMatch, UserProfile, Committee } from '../types';
import {
  DRIVE_SLIDES_CATALOG,
  DriveSlideMeta,
  DRIVE_FOLDER_URL,
} from '../data/driveCatalog';
import { renderSingleDriveSlide } from '../services/driveAutomation';
import { SlideReaderModal } from './SlideReaderModal';
import { ApiService } from '../services/api';
import { multiDbManager } from '../services/multiDbManager';
import { triggerDomHighlightAndScroll } from '../services/universalRedirectService';

/**
 * Ders notları (v10 kompakt; ders özetleriyle aynı okuyucu dili). Yapı:
 *   PageToolbar (başlık · sayaç · arama · Slayt kataloğu / İşlenmiş notlar · Süzgeç: anabilim dalı + durum · araçlar)
 *   + tek satır işleme ilerlemesi → katalog: kompakt slayt listesi (no · başlık · dal/sayfa · durum · eylemler)
 *   → işlenmiş notlar: sol ray (not listesi; telefonda/akış düzeninde alt sayfa) + orta okuma sütunu (~660 px,
 *   A− / A+ özetlerle ortak tercih, Slayt PDF'i, tam ekran okuyucu) ve sayfa sayfa metin.
 * Stil: styles/summary.css (.nr-*, liste satırı .sl-list ile ortak).
 */
interface LectureNotesViewProps {
  committee?: Committee;
  committees: Committee[];
  questions: QuestionItem[];
  currentUser: UserProfile | null;
  isAdmin: boolean;
  onUpdateQuestionReference: (questionId: string, reference: QuestionLectureMatch) => Promise<void>;
}

const LOCAL_NOTES_KEY = 'medsoru_lecture_notes_v5_verbatim';

/** "1)Cinsel yolla…" → { no: '1', title: 'Cinsel yolla…' }: numara ayrı mono çipte gösterilir. */
const splitSlideTitle = (raw: string) => {
  const m = String(raw || '').match(/^\s*(\d{1,3})\s*[).\-–]\s*(.*)$/);
  return m ? { no: m[1], title: m[2].trim() } : { no: '', title: String(raw || '').trim() };
};
/** Geçersiz/boş tarihte "Invalid Date" yerine hiçbir şey. */
const fmtDate = (v?: string) => {
  const d = v ? new Date(v) : null;
  return d && !Number.isNaN(d.getTime()) ? d.toLocaleDateString('tr-TR') : '';
};
const LN_TONES = ['accent', 'clinic', 'ai', 'warn', 'ok', 'bad'] as const;
/** Anabilim dalına sabit ton (Hastalıklar ile aynı ölçek, yalnız DS tokenları). */
const disciplineTone = (d: string) => {
  let h = 0;
  for (const ch of String(d || '')) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return LN_TONES[h % LN_TONES.length];
};

// Filter helper: Discard any old mock note that contains AI template sentences
export const isPureVerbatimNote = (note: LectureNote): boolean => {
  if (!note || !Array.isArray(note.pages) || note.pages.length === 0) return false;
  return !note.pages.some(p => 
    p.content?.includes('• Temel Tanım ve Kavram:') || 
    p.content?.includes('• Patogenetik Mekanizma & Not:') ||
    p.content?.includes('• Önemli Slayt Maddeleri:')
  );
};

export const LectureNotesView: React.FC<LectureNotesViewProps> = ({
  committee,
  questions,
  currentUser,
  isAdmin,
  onUpdateQuestionReference,
}) => {
  // Main view tab: 'drive_catalog' (Google Drive Slayt Kataloğu) or 'rendered_notes' (İşlenmiş Notlar & Okuyucu)
  const [activeTab, setActiveTab] = useState<'drive_catalog' | 'rendered_notes'>('drive_catalog');

  // Notes state - starts strictly with persistent server/firestore data, NEVER pre-seeded with fake mocks
  const [notes, setNotes] = useState<LectureNote[]>(() => {
    try {
      // Clear legacy storage keys containing fake data
      localStorage.removeItem('medsoru_lecture_notes');
      localStorage.removeItem('medsoru_lecture_notes_v1');
      localStorage.removeItem('medsoru_lecture_notes_v2');
      localStorage.removeItem('medsoru_lecture_notes_v3');

      const stored = localStorage.getItem(LOCAL_NOTES_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed.filter(n => !n.id.startsWith('mock-') && isPureVerbatimNote(n));
        }
      }
    } catch (e) {}
    return [];
  });

  // Active note in reader
  const [activeNote, setActiveNote] = useState<LectureNote | null>(null);
  const [readerNote, setReaderNote] = useState<LectureNote | null>(null);

  // Catalog filters & search
  const [catalogDiscipline, setCatalogDiscipline] = useState<string>('Tümü');
  const [catalogSearch, setCatalogSearch] = useState<string>('');
  const [catalogStatusFilter, setCatalogStatusFilter] = useState<'all' | 'unrendered' | 'rendered'>('all');

  // Rendered notes filters
  const [notesDiscipline, setNotesDiscipline] = useState<string>('Tümü');
  const [notesSearch, setNotesSearch] = useState<string>('');

  // UI feedback and loaders
  const [renderingSlideId, setRenderingSlideId] = useState<string | null>(null);
  const [feedbackMessage, setFeedbackMessage] = useState<string | null>(null);
  const [copySuccess, setCopySuccess] = useState<Record<number, boolean>>({});

  // Add Note Modal
  const [isAddingNote, setIsAddingNote] = useState(false);
  const [addMode, setAddMode] = useState<'upload' | 'text'>('text');
  const [newTitle, setNewTitle] = useState('');
  const [newDiscipline, setNewDiscipline] = useState('Tıbbi Patoloji');
  const [newInstructor, setNewInstructor] = useState('');
  const [newRawContent, setNewRawContent] = useState('');
  const [pageDelimiter, setPageDelimiter] = useState('--- Sayfa ---');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isUploadingPdf, setIsUploadingPdf] = useState(false);
  const [pdfUploadStatus, setPdfUploadStatus] = useState<string | null>(null);
  const [isSyncingDesktop, setIsSyncingDesktop] = useState(false);
  const [railSheet, setRailSheet] = useState(false);
  const [prefs, setPrefs] = useReaderPrefs();

  // Notes are managed in memory and synced via multiDbManager & Supabase Realtime

  // Universal Text / Sentence Deep-linking Highlight listener
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const urlParams = new URLSearchParams(window.location.search);
    const highlight = urlParams.get('highlight');
    if (highlight) {
      const timer = setTimeout(() => {
        triggerDomHighlightAndScroll(highlight);
      }, 700);
      return () => clearTimeout(timer);
    }
  }, []);

  // Load verified notes from Multi-Database (Supabase / Local / Firestore) and listen for Realtime updates
  useEffect(() => {
    let isMounted = true;

    async function loadSavedNotes() {
      try {
        const loaded = await multiDbManager.getLectureNotes();
        if (isMounted && Array.isArray(loaded) && loaded.length > 0) {
          const valid = loaded.filter(isPureVerbatimNote);
          if (valid.length > 0) {
            setNotes(valid);
            setActiveNote((prev) => prev || valid[0]);
            return;
          }
        }
      } catch (e) {
        console.warn('[LectureNotesView] multiDbManager.getLectureNotes error:', e);
      }

      // Fallback: Local Server API
      try {
        const apiBase = localStorage.getItem('medsoru_custom_api_url') || '';
        const res = await fetch(`${apiBase}/api/lecture-notes`);
        if (res.ok) {
          const json = await res.json();
          const list = (json.notes || json) as LectureNote[];
          if (isMounted && Array.isArray(list) && list.length > 0) {
            const valid = list.filter(isPureVerbatimNote);
            if (valid.length > 0) {
              setNotes(valid);
              setActiveNote((prev) => prev || valid[0]);
            }
          }
        }
      } catch (_) {}
    }

    loadSavedNotes();

    // Supabase Realtime Subscription: Anlık ders notu ekleme, düzenleme ve silmeleri canlı dinle
    const unsubscribe = multiDbManager.subscribeToLectureNotes((payload) => {
      if (!isMounted) return;
      if ((payload.eventType === 'INSERT' || payload.eventType === 'UPDATE') && payload.new) {
        const newNote: LectureNote = payload.new.data || {
          id: payload.new.id,
          committeeId: payload.new.committee_id,
          discipline: payload.new.discipline,
          title: payload.new.title,
          pages: payload.new.pages || [],
          pageCount: payload.new.page_count,
          createdAt: payload.new.created_at,
        };

        if (newNote && isPureVerbatimNote(newNote)) {
          setNotes((prev) => {
            const exists = prev.some((n) => n.id === newNote.id);
            if (exists) {
              return prev.map((n) => (n.id === newNote.id ? { ...n, ...newNote } : n));
            }
            return [newNote, ...prev];
          });
        }
      } else if (payload.eventType === 'DELETE' && payload.old) {
        const deletedId = (payload.old as any)?.id;
        if (deletedId) {
          setNotes((prev) => prev.filter((n) => n.id !== deletedId));
        }
      }
    });

    return () => {
      isMounted = false;
      unsubscribe();
    };
  }, []);

  // Compute catalog statistics
  const TOTAL_CATALOG_SLIDES = DRIVE_SLIDES_CATALOG.length; // 40
  const TOTAL_CATALOG_PAGES = useMemo(() => {
    return DRIVE_SLIDES_CATALOG.reduce((acc, s) => acc + s.totalRealPages, 0); // 1,353
  }, []);

  const normTitle = (t: string) => (t || '')
    .toLowerCase()
    .replace(/\.pdf$/i, '')
    .replace(/^[0-9]+[\.\)\-\s_]+/, '')
    .replace(/[^a-zA-Z0-9ğüşıöçĞÜŞİÖÇ]/g, '')
    .trim();

  const renderedNotesMap = useMemo(() => {
    const map = new Map<string, LectureNote>();
    notes.forEach(n => {
      map.set(n.id, n);
      if (n.driveFileId) map.set(n.driveFileId, n);
      const nKey = normTitle(n.title);
      if (nKey) map.set(nKey, n);
    });
    return map;
  }, [notes]);

  const isSlideRendered = useMemo(() => {
    return (s: DriveSlideMeta): LectureNote | undefined => {
      if (renderedNotesMap.has(s.id)) return renderedNotesMap.get(s.id);
      if (s.fileId && renderedNotesMap.has(s.fileId)) return renderedNotesMap.get(s.fileId);
      const sKey = normTitle(s.title);
      if (sKey && renderedNotesMap.has(sKey)) return renderedNotesMap.get(sKey);
      for (const [key, note] of renderedNotesMap.entries()) {
        if (key.length > 5 && sKey.length > 5 && (key.includes(sKey) || sKey.includes(key))) {
          return note;
        }
      }
      return undefined;
    };
  }, [renderedNotesMap]);

  const renderedSlidesCount = useMemo(() => {
    return DRIVE_SLIDES_CATALOG.filter(s => Boolean(isSlideRendered(s))).length;
  }, [isSlideRendered]);

  const renderedPagesCount = useMemo(() => {
    return DRIVE_SLIDES_CATALOG
      .filter(s => Boolean(isSlideRendered(s)))
      .reduce((acc, s) => acc + s.totalRealPages, 0);
  }, [isSlideRendered]);

  const progressPercent = Math.round((renderedPagesCount / TOTAL_CATALOG_PAGES) * 100);

  // Derin bağlantı: /notlar?id=<notId>&page=<n> → işlenmiş notlar sekmesinde o not açılır, sayfaya kayılır.
  useEffect(() => {
    if (typeof window === 'undefined' || notes.length === 0) return;
    const sp = new URLSearchParams(window.location.search);
    const id = sp.get('id');
    if (!id) return;
    const note = notes.find((n) => n.id === id);
    if (!note) return;
    setActiveTab('rendered_notes');
    setActiveNote(note);
    const page = Number(sp.get('page') || 0);
    if (page > 0) {
      window.setTimeout(() => {
        const el = document.getElementById(`ln-page-${page}`);
        el?.scrollIntoView({ block: 'start', behavior: 'smooth' });
        el?.classList.add('deep-link-highlight-pulse');
      }, 350);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [notes.length]);

  // Anabilim dalı çipleri katalogdan sayılır (sabit sayı yok).
  const catalogDisciplines = useMemo(() => {
    const m = new Map<string, number>();
    DRIVE_SLIDES_CATALOG.forEach((s) => m.set(s.discipline, (m.get(s.discipline) || 0) + 1));
    return [['Tümü', DRIVE_SLIDES_CATALOG.length] as [string, number], ...[...m.entries()].sort((x, y) => y[1] - x[1])];
  }, []);

  // Filter catalog slides
  const filteredCatalog = useMemo(() => {
    return DRIVE_SLIDES_CATALOG.filter(s => {
      if (catalogDiscipline !== 'Tümü' && s.discipline !== catalogDiscipline) return false;
      const isRendered = Boolean(isSlideRendered(s));
      if (catalogStatusFilter === 'unrendered' && isRendered) return false;
      if (catalogStatusFilter === 'rendered' && !isRendered) return false;
      if (catalogSearch.trim()) {
        const query = catalogSearch.toLowerCase();
        const matchesTitle = s.title.toLowerCase().includes(query);
        const matchesTopics = s.keyTopics.some(t => t.toLowerCase().includes(query));
        const matchesDiscipline = s.discipline.toLowerCase().includes(query);
        if (!matchesTitle && !matchesTopics && !matchesDiscipline) return false;
      }
      return true;
    });
  }, [catalogDiscipline, catalogStatusFilter, catalogSearch, isSlideRendered]);

  // Filter rendered notes
  const filteredRenderedNotes = useMemo(() => {
    return notes.filter(n => {
      if (notesDiscipline !== 'Tümü' && n.discipline !== notesDiscipline) return false;
      if (notesSearch.trim()) {
        const query = notesSearch.toLowerCase();
        const matchesTitle = n.title.toLowerCase().includes(query);
        const matchesInstructor = n.instructor?.toLowerCase().includes(query);
        if (!matchesTitle && !matchesInstructor) return false;
      }
      return true;
    });
  }, [notes, notesDiscipline, notesSearch]);

  // Handler: Render a single slide with ALL its real pages (e.g. 28, 35, 42 pages)
  const handleRenderSlide = async (meta: DriveSlideMeta) => {
    setRenderingSlideId(meta.id);
    setFeedbackMessage(`"${meta.title}" taranıyor... Toplam ${meta.totalRealPages} sayfa tek tek render ediliyor...`);

    try {
      const { note, matchedQuestions } = await renderSingleDriveSlide(
        meta,
        committee?.id || 'donem3-kurul1',
        questions
      );

      // Add to state
      setNotes(prev => {
        const filtered = prev.filter(n => n.id !== note.id);
        return [note, ...filtered];
      });
      setActiveNote(note);

      // Auto update matched questions reference
      for (const m of matchedQuestions) {
        if (m.match) {
          await onUpdateQuestionReference(m.questionId, m.match);
        }
      }

      setFeedbackMessage(
        `✓ "${meta.title}" dersinin ${note.totalSlides} sayfasının tamamı başarıyla render edildi ve soru havuzuna bağlandı!`
      );
    } catch (err: any) {
      setFeedbackMessage('Hata: ' + err.message);
    } finally {
      setRenderingSlideId(null);
    }
  };

  // Handler: Delete rendered note
  const handleDeleteNote = async (id: string, title: string) => {
    if (!(await confirmDialog({ title: 'Ders notu silinsin mi?', message: `“${title}” silinir.`, confirmLabel: 'Sil', tone: 'danger' }))) return;

    setNotes(prev => prev.filter(n => n.id !== id));
    if (activeNote?.id === id) {
      const remaining = notes.filter(n => n.id !== id);
      setActiveNote(remaining[0] || null);
    }

    try {
      await multiDbManager.deleteLectureNote(id);
    } catch (e) {}

    setFeedbackMessage(`"${title}" silindi.`);
  };

  // Handler: Purge all local/sample notes
  const handlePurgeMockNotes = async () => {
    if (!(await confirmDialog({ title: 'Örnek ders notları sıfırlansın mı?', message: 'Yerel hafızadaki tüm örnek ders notları silinir.', confirmLabel: 'Sıfırla', tone: 'danger' }))) return;
    localStorage.removeItem(LOCAL_NOTES_KEY);
    localStorage.removeItem('medsoru_lecture_notes');
    localStorage.removeItem('medsoru_lecture_notes_v2');
    setNotes([]);
    setActiveNote(null);
    setFeedbackMessage('✓ Yerel önbellekteki tüm ders notu örnekleri silindi.');
  };

  // Handler: Save manual new note
  const handleSaveManualNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newRawContent.trim()) return;

    setIsSubmitting(true);
    try {
      const rawPages = newRawContent
        .split(new RegExp(pageDelimiter || '--- Sayfa ---', 'i'))
        .map(p => p.trim())
        .filter(p => p.length > 0);

      const parsedPages = rawPages.map((text, idx) => {
        const words = text
          .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"']/g, ' ')
          .split(/\s+/)
          .filter(w => w.length > 4)
          .slice(0, 8);
        return {
          pageNumber: idx + 1,
          content: text,
          keywords: Array.from(new Set(words)),
        };
      });

      const newNote: LectureNote = {
        id: `manual-note-${Date.now()}`,
        committeeId: committee?.id || 'donem3-kurul1',
        discipline: newDiscipline,
        title: newTitle.trim(),
        instructor: newInstructor.trim() || undefined,
        totalSlides: parsedPages.length,
        pages: parsedPages,
        uploadedBy: currentUser?.displayName || currentUser?.email || 'Öğrenci',
        uploadedAt: new Date().toISOString(),
      };

      // 1. Update State
      setNotes(prev => [newNote, ...prev]);
      setActiveNote(newNote);
      setIsAddingNote(false);
      setNewTitle('');
      setNewInstructor('');
      setNewRawContent('');
      setActiveTab('rendered_notes');

      // 2. Parallel Dual-Write (Supabase + Local Server + Firebase Spark)
      try {
        await multiDbManager.saveLectureNote(newNote);
      } catch (err) {}

      setFeedbackMessage(`✓ "${newNote.title}" başarıyla kaydedildi (${newNote.totalSlides} sayfa).`);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handler: PDF file upload
  const handlePdfUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploadingPdf(true);
    setPdfUploadStatus(`"${file.name}" taranıyor... Sayfalar okunuyor...`);

    try {
      const reader = new FileReader();
      const base64Promise = new Promise<string>((resolve, reject) => {
        reader.onload = () => {
          const res = reader.result as string;
          resolve(res.split(',')[1] || res);
        };
        reader.onerror = reject;
      });
      reader.readAsDataURL(file);
      const base64 = await base64Promise;

      const resp = await ApiService.extractDocument({
        fileBase64: base64,
        fileMimeType: file.type || 'application/pdf',
        fileName: file.name,
        mode: 'lecture_notes',
      });

      if (resp.success && resp.note) {
        const extracted = resp.note;
        const newNote: LectureNote = {
          id: `upload-pdf-${Date.now()}`,
          committeeId: committee?.id || 'donem3-kurul1',
          discipline: extracted.discipline || 'Tıbbi Patoloji',
          title: extracted.title || file.name.replace(/\.[^/.]+$/, ''),
          instructor: extracted.instructor || 'Ders Anabilim Dalı',
          totalSlides: extracted.totalSlides || extracted.pages?.length || 1,
          pages: extracted.pages || [],
          uploadedBy: currentUser?.displayName || currentUser?.email || 'Öğrenci',
          uploadedAt: new Date().toISOString(),
        };

        setNotes(prev => [newNote, ...prev]);
        setActiveNote(newNote);
        setIsAddingNote(false);
        setActiveTab('rendered_notes');
        setPdfUploadStatus(null);

        try {
          await multiDbManager.saveLectureNote(newNote);
        } catch (err) {}

        setFeedbackMessage(`✓ "${newNote.title}" belgesinin ${newNote.totalSlides} sayfası eksiksiz render edildi!`);
      } else {
        throw new Error((resp as any).error || 'Belge okunamadı');
      }
    } catch (err: any) {
      setPdfUploadStatus('Hata: ' + err.message);
    } finally {
      setIsUploadingPdf(false);
    }
  };

  // Handler for manual trigger of Desktop Folder (meds_database) Sync
  const handleTriggerDesktopSync = async () => {
    setIsSyncingDesktop(true);
    setFeedbackMessage('C:\\Users\\indui\\Desktop\\meds_database taranıyor...');
    try {
      const res = await ApiService.scanDesktopDatabaseFolder();
      const updatedNotes = await ApiService.getLectureNotes();
      if (updatedNotes && updatedNotes.length > 0) {
        setNotes(updatedNotes);
        setActiveNote(updatedNotes[0]);
      }
      setFeedbackMessage(
        `✓ Masaüstü klasörü senkronize edildi: Toplam ${res.totalFilesFound || 0} belge bulundu, ${res.newlyAdded || 0} yeni ders notu eklendi!`
      );
    } catch (err: any) {
      setFeedbackMessage('Masaüstü klasör tarama hatası: ' + err.message);
    } finally {
      setIsSyncingDesktop(false);
    }
  };

  const copyPageContent = (text: string, pageNum: number) => {
    navigator.clipboard.writeText(text);
    setCopySuccess(prev => ({ ...prev, [pageNum]: true }));
    setTimeout(() => {
      setCopySuccess(prev => ({ ...prev, [pageNum]: false }));
    }, 2000);
  };

  const onCatalog = activeTab === 'drive_catalog';
  const notesDisciplines = useMemo(() => {
    const m = new Map<string, number>();
    notes.forEach((n) => m.set(n.discipline, (m.get(n.discipline) || 0) + 1));
    return [['Tümü', notes.length] as [string, number], ...[...m.entries()].sort((x, y) => y[1] - x[1])];
  }, [notes]);
  const discipline = onCatalog ? catalogDiscipline : notesDiscipline;
  const setDiscipline = onCatalog ? setCatalogDiscipline : setNotesDiscipline;
  const chips: ToolbarChip[] = [
    ...(discipline !== 'Tümü' ? [{ id: 'd', label: discipline, onRemove: () => setDiscipline('Tümü') }] : []),
    ...(onCatalog && catalogStatusFilter !== 'all'
      ? [{ id: 's', label: catalogStatusFilter === 'rendered' ? 'İşlenen' : 'Bekleyen', onRemove: () => setCatalogStatusFilter('all') }]
      : []),
  ];
  // Okunan notun özgün slaydı: notun kendi Drive kimliği, yoksa katalogdaki eşi
  const activeSlide = activeNote ? DRIVE_SLIDES_CATALOG.find((sl) => isSlideRendered(sl)?.id === activeNote.id) : undefined;
  const activeDriveId = activeNote?.driveFileId || activeSlide?.fileId;
  const activePdfHref = activeNote?.driveFileUrl || (activeDriveId ? `https://drive.google.com/file/d/${activeDriveId}/view?usp=sharing` : undefined);

  const NotesRail = (
    <nav className="nr-rail-in" aria-label="İşlenmiş notlar">
      <ol className="nr-list">
        {filteredRenderedNotes.map((note) => {
          const on = activeNote?.id === note.id;
          const { no, title } = splitSlideTitle(note.title);
          return (
            <li key={note.id}>
              <button
                type="button"
                className={on ? 'is-on' : ''}
                aria-current={on ? 'true' : undefined}
                onClick={() => {
                  setActiveNote(note);
                  setRailSheet(false);
                }}
              >
                {no && <span className="nr-no">{no}</span>}
                <span className="nr-list-t">
                  <b>{title}</b>
                  <small>
                    {note.discipline} · {note.totalSlides} sayfa
                  </small>
                </span>
              </button>
            </li>
          );
        })}
        {filteredRenderedNotes.length === 0 && <li className="nr-none">Eşleşen not yok.</li>}
      </ol>
      <button type="button" className="nr-railfoot" onClick={() => setActiveTab('drive_catalog')}>
        <Plus aria-hidden /> Katalogdan slayt işle
      </button>
    </nav>
  );

  return (
    <div className="nr-page">
      <PageToolbar<'drive_catalog' | 'rendered_notes'>
        title="Ders notları"
        count={
          onCatalog
            ? `${renderedSlidesCount} / ${TOTAL_CATALOG_SLIDES} işlendi`
            : `${filteredRenderedNotes.length === notes.length ? notes.length : `${filteredRenderedNotes.length} / ${notes.length}`} not`
        }
        search={
          onCatalog
            ? { value: catalogSearch, onChange: setCatalogSearch, placeholder: 'Slayt adı ya da konu ara' }
            : { value: notesSearch, onChange: setNotesSearch, placeholder: 'Notlarda ara' }
        }
        segments={{
          label: 'Ders notu görünümü',
          value: activeTab,
          onChange: setActiveTab,
          options: [
            { id: 'drive_catalog', label: 'Slayt kataloğu', count: TOTAL_CATALOG_SLIDES },
            { id: 'rendered_notes', label: 'İşlenmiş notlar', count: notes.length },
          ],
        }}
        filters={
          <>
            <FilterPills
              label="Anabilim dalı"
              value={discipline}
              onChange={setDiscipline}
              options={(onCatalog ? catalogDisciplines : notesDisciplines).map(([name, count]) => ({ id: name, label: name, count }))}
            />
            {onCatalog && (
              <FilterPills<'all' | 'unrendered' | 'rendered'>
                label="Durum"
                value={catalogStatusFilter}
                onChange={setCatalogStatusFilter}
                options={[
                  { id: 'all', label: 'Tümü', count: TOTAL_CATALOG_SLIDES },
                  { id: 'unrendered', label: 'Bekleyen', count: TOTAL_CATALOG_SLIDES - renderedSlidesCount },
                  { id: 'rendered', label: 'İşlenen', count: renderedSlidesCount },
                ]}
              />
            )}
          </>
        }
        filterCount={chips.length}
        chips={chips}
        onClearChips={() => {
          setDiscipline('Tümü');
          setCatalogStatusFilter('all');
        }}
        tools={
          <>
            {isAdmin && (
              <button type="button" onClick={handleTriggerDesktopSync} disabled={isSyncingDesktop} className="pt-icon" aria-label="Yerel ders notu klasörünü tara" title="Yerel ders notu klasörünü şimdi tara">
                {isSyncingDesktop ? <RefreshCw className="animate-spin" aria-hidden /> : <FolderOpen aria-hidden />}
              </button>
            )}
            <a href={DRIVE_FOLDER_URL} target="_blank" rel="noreferrer" className="pt-icon" aria-label="Drive klasörü" title="Drive klasörü">
              <ExternalLink aria-hidden />
            </a>
            {isAdmin && (
              <button type="button" onClick={() => setIsAddingNote(true)} className="pt-icon" aria-label="Not yükle" title="Not yükle">
                <Plus aria-hidden />
              </button>
            )}
          </>
        }
      >
        <div className="nr-prog" aria-label="Slayt işleme durumu">
          <span className="nr-prog-t">
            <b>%{progressPercent}</b> · {renderedPagesCount.toLocaleString('tr-TR')} / {TOTAL_CATALOG_PAGES.toLocaleString('tr-TR')} sayfa işlendi
          </span>
          <span className="nr-prog-bar" role="progressbar" aria-valuenow={progressPercent} aria-valuemin={0} aria-valuemax={100} aria-label="Slayt işleme ilerlemesi">
            <i style={{ transform: `scaleX(${progressPercent / 100})` }} />
          </span>
          {isAdmin && notes.length > 0 && (
            <button type="button" onClick={handlePurgeMockNotes} title="Önbellekte kalan örnek notları temizler" className="nr-link is-bad">
              Örnekleri temizle
            </button>
          )}
        </div>
      </PageToolbar>

      {feedbackMessage && (
        <div role="status" className="nr-feedback">
          <CheckCircle2 aria-hidden />
          <span>{feedbackMessage}</span>
          <button type="button" onClick={() => setFeedbackMessage(null)} aria-label="Bildirimi kapat">
            <X aria-hidden />
          </button>
        </div>
      )}

      {onCatalog &&
        (filteredCatalog.length === 0 ? (
          <div className="sl-empty">
            <Search aria-hidden />
            <h3>Aramana uygun slayt yok</h3>
            <p>Başka bir anabilim dalı ya da anahtar kelime dene.</p>
          </div>
        ) : (
          <ul className="sl-list">
            {filteredCatalog.map((slide, i) => {
              const renderedNote = isSlideRendered(slide);
              const isRendered = Boolean(renderedNote);
              const isProcessing = renderingSlideId === slide.id;
              const { no, title } = splitSlideTitle(slide.title);
              const topics = slide.keyTopics
                .map((t) => splitSlideTitle(t).title)
                .filter((t) => t && t.toLocaleLowerCase('tr-TR') !== title.toLocaleLowerCase('tr-TR'));
              return (
                <li key={slide.id} className={`sl-item nr-row ${isRendered ? 'is-done' : ''}`} data-tone={disciplineTone(slide.discipline)}>
                  <span className="sl-no" aria-hidden>
                    {(no || String(i + 1)).padStart(2, '0')}
                  </span>
                  <span className="sl-row-main">
                    <span className="sl-row-t">{title}</span>
                    <span className="sl-row-m">
                      <i className="nr-dot" aria-hidden />
                      <span>{slide.discipline}</span>
                      <span>· {slide.totalRealPages} sayfa</span>
                      {topics.length > 0 && <span className="sl-row-who">· {topics.slice(0, 4).join(', ')}</span>}
                    </span>
                  </span>
                  <span className={`sl-state ${isRendered ? 'is-done' : ''}`}>
                    {isRendered ? (
                      <>
                        <CheckCircle2 aria-hidden /> İşlendi
                      </>
                    ) : (
                      'Bekliyor'
                    )}
                  </span>
                  <span className="nr-acts">
                    <a className="nr-ib" href={`https://drive.google.com/file/d/${slide.fileId}/view?usp=sharing`} target="_blank" rel="noreferrer" aria-label="Drive'da aç" title="Drive'da aç">
                      <ExternalLink aria-hidden />
                    </a>
                    {isRendered && (
                      <button type="button" className="nr-ib" onClick={() => handleRenderSlide(slide)} disabled={isProcessing} aria-label="Yeniden işle" title="Tüm sayfaları yeniden işler">
                        <RefreshCw className={isProcessing ? 'animate-spin' : ''} aria-hidden />
                      </button>
                    )}
                    {isRendered && isAdmin && (
                      <button type="button" className="nr-ib is-danger" onClick={() => handleDeleteNote(slide.id, slide.title)} aria-label="İşlenmiş notu sil" title="İşlenmiş notu sil">
                        <Trash2 aria-hidden />
                      </button>
                    )}
                    {isRendered ? (
                      <button
                        type="button"
                        className="nr-btn"
                        onClick={() => {
                          if (renderedNote) {
                            setActiveNote(renderedNote);
                            setActiveTab('rendered_notes');
                          }
                        }}
                      >
                        <Eye aria-hidden /> Oku
                      </button>
                    ) : (
                      <button type="button" className={`nr-btn is-primary ${isProcessing ? 'is-busy' : ''}`} onClick={() => handleRenderSlide(slide)} disabled={isProcessing}>
                        {isProcessing ? (
                          <>
                            <RefreshCw className="animate-spin" aria-hidden /> İşleniyor…
                          </>
                        ) : (
                          <>
                            <Play aria-hidden /> İşle
                          </>
                        )}
                      </button>
                    )}
                  </span>
                </li>
              );
            })}
          </ul>
        ))}

      {!onCatalog &&
        (notes.length === 0 ? (
          <div className="sl-empty">
            <BookMarked aria-hidden />
            <h3>Henüz işlenmiş ders notu yok</h3>
            <p>Slayt kataloğundan bir slaytı işle ya da kendi notunu yükle.</p>
            <button type="button" className="ui-btn is-sm" onClick={() => setActiveTab('drive_catalog')}>
              <FolderGit2 aria-hidden /> Slayt kataloğuna git
            </button>
          </div>
        ) : (
          <div className="nr-read">
            <aside className="nr-rail">{NotesRail}</aside>

            <section className="nr-doc" aria-label="Not sayfaları" style={{ '--sr-scale': prefs.scale / 100 } as React.CSSProperties}>
              <div className="sr-tools nr-tools">
                <button type="button" className="sr-tool nr-railbtn" onClick={() => setRailSheet(true)}>
                  <ListTree aria-hidden /> Notlar · {filteredRenderedNotes.length}
                </button>
                <div className="sr-fs" role="group" aria-label="Yazı boyutu">
                  <button type="button" onClick={() => setPrefs({ scale: prefs.scale - 10 })} disabled={prefs.scale <= 80} aria-label="Yazıyı küçült" title={`Yazı %${prefs.scale}`}>
                    A−
                  </button>
                  <button type="button" onClick={() => setPrefs({ scale: prefs.scale + 10 })} disabled={prefs.scale >= 150} aria-label="Yazıyı büyüt" title={`Yazı %${prefs.scale}`}>
                    A+
                  </button>
                </div>
                {activeNote && activePdfHref && (
                  <a className="sr-tool" href={activePdfHref} target="_blank" rel="noreferrer">
                    <FileText aria-hidden /> Slayt PDF’i
                  </a>
                )}
                {activeNote && (
                  <button type="button" className="sr-tool" onClick={() => setReaderNote(activeNote)}>
                    <BookOpen aria-hidden /> Tam ekran
                  </button>
                )}
                {activeNote && isAdmin && (
                  <button type="button" className="nr-ib is-danger" onClick={() => handleDeleteNote(activeNote.id, activeNote.title)} aria-label="Bu notu sil" title="Bu notu sil">
                    <Trash2 aria-hidden />
                  </button>
                )}
              </div>

              {activeNote ? (
                <article className="nr-article">
                  <header className="nr-head">
                    <span className="nr-crumb">
                      Ders notları <ChevronRight aria-hidden /> {activeNote.discipline}
                    </span>
                    <h1>{splitSlideTitle(activeNote.title).title}</h1>
                    <p>
                      {[`${activeNote.totalSlides} sayfa`, activeNote.instructor, activeNote.uploadedBy ? `Yükleyen: ${activeNote.uploadedBy}` : null, fmtDate(activeNote.uploadedAt)]
                        .filter(Boolean)
                        .join(' · ')}
                    </p>
                  </header>
                  <ol className="nr-pages">
                    {activeNote.pages.map((page) => (
                      <li key={page.pageNumber} id={`ln-page-${page.pageNumber}`} className="nr-pg">
                        <div className="nr-pg-h">
                          <span>
                            Sayfa {page.pageNumber}
                            <small> / {activeNote.totalSlides}</small>
                          </span>
                          <button type="button" className={`nr-copy ${copySuccess[page.pageNumber] ? 'is-done' : ''}`} onClick={() => copyPageContent(page.content, page.pageNumber)}>
                            {copySuccess[page.pageNumber] ? (
                              <>
                                <Check aria-hidden /> Kopyalandı
                              </>
                            ) : (
                              <>
                                <Copy aria-hidden /> Kopyala
                              </>
                            )}
                          </button>
                        </div>
                        <SourceText text={String(page.content || '')} />
                        {page.keywords && page.keywords.length > 0 && (
                          <ul className="nr-kw" aria-label="Kavramlar">
                            {page.keywords.map((kw, i) => (
                              <li key={i}>{kw}</li>
                            ))}
                          </ul>
                        )}
                      </li>
                    ))}
                  </ol>
                </article>
              ) : (
                <div className="sl-empty">
                  <BookOpen aria-hidden />
                  <h3>Bir not seç</h3>
                  <p>Okumak için listeden bir ders notu seç.</p>
                </div>
              )}
            </section>
          </div>
        ))}

      <Sheet open={railSheet} onClose={() => setRailSheet(false)} title="İşlenmiş notlar" subtitle={`${filteredRenderedNotes.length} not`} size="full">
        {NotesRail}
      </Sheet>

      {/* MODAL: ADD MANUAL / CUSTOM LECTURE NOTE */}
      {isAddingNote && (
        <div className="ms-overlay fixed inset-0 z-50 bg-[var(--color-scrim)] flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl border border-line max-w-2xl w-full p-6 shadow-2xl space-y-4 my-8">
            <div className="flex items-center justify-between border-b border-line pb-3">
              <div className="flex items-center gap-2 text-ink font-bold">
                <BookMarked className="w-5 h-5 text-ok" />
                <span>Yeni Ders Notu / Slayt Yükle</span>
              </div>
              <button
                onClick={() => setIsAddingNote(false)}
                className="text-ink-3 hover:text-ink-2 text-xs px-2 py-1 cursor-pointer"
              >
                Kapat
              </button>
            </div>

            {/* Upload Mode Selector */}
            <div className="flex border-b border-line text-xs font-bold">
              <button
                type="button"
                onClick={() => setAddMode('text')}
                className={`flex-1 py-2 text-center border-b-2 cursor-pointer transition-colors ${
                  addMode === 'text'
                    ? 'border-ok text-ok bg-ok-soft/50'
                    : 'border-transparent text-ink-3 hover:text-ink'
                }`}
              >
                Metin Yapıştırarak Ekle
              </button>
              <button
                type="button"
                onClick={() => setAddMode('upload')}
                className={`flex-1 py-2 text-center border-b-2 cursor-pointer transition-colors ${
                  addMode === 'upload'
                    ? 'border-ok text-ok bg-ok-soft/50'
                    : 'border-transparent text-ink-3 hover:text-ink'
                }`}
              >
                PDF / DOCX Dosyası Yükle
              </button>
            </div>

            {addMode === 'upload' ? (
              <div className="space-y-4 text-xs">
                <div className="border-2 border-dashed border-ok/30 rounded-xl p-6 text-center bg-ok-soft/30 space-y-3">
                  <div className="w-12 h-12 rounded-full bg-ok-soft text-ok flex items-center justify-center mx-auto">
                    <UploadCloud className="w-6 h-6" />
                  </div>
                  <div>
                    <h4 className="font-bold text-ink">Ders Slaytını Yükleyin (.pdf veya .docx)</h4>
                    <p className="text-ink-3 text-2xs mt-1">
                      Sistem slayttaki tüm sayfaları metin olarak ayıklar ve soru eşleştirmelerine bağlar.
                    </p>
                  </div>
                  <label className="inline-flex items-center gap-2 bg-ok hover:bg-ok text-white font-bold px-4 py-2 rounded-lg cursor-pointer transition-all shadow-xs">
                    <FileUp className="w-4 h-4 text-ok-soft" />
                    <span>Dosya Seç (.pdf, .docx)</span>
                    <input
                      type="file"
                      accept=".pdf,.docx,.doc"
                      onChange={handlePdfUpload}
                      disabled={isUploadingPdf}
                      className="hidden"
                    />
                  </label>
                </div>

                {pdfUploadStatus && (
                  <div className="p-3 bg-warn-soft border border-warn/30 text-warn rounded-xl flex items-center gap-2.5 font-medium animate-pulse">
                    <RefreshCw className="w-4 h-4 text-warn animate-spin shrink-0" />
                    <span>{pdfUploadStatus}</span>
                  </div>
                )}
              </div>
            ) : (
              <form onSubmit={handleSaveManualNote} className="space-y-4 text-xs">
                <div>
                  <label className="font-bold text-ink-2 block mb-1">Ders / Anabilim Dalı</label>
                  <select
                    value={newDiscipline}
                    onChange={(e) => setNewDiscipline(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-line-2 bg-white"
                  >
                    <option value="Tıbbi Patoloji">Tıbbi Patoloji</option>
                    <option value="Tıbbi Genetik">Tıbbi Genetik</option>
                    <option value="Halk Sağlığı">Halk Sağlığı</option>
                    <option value="Üroloji">Üroloji</option>
                    <option value="Enfeksiyon Hastalıkları">Enfeksiyon Hastalıkları</option>
                    <option value="Tıbbi Farmakoloji">Tıbbi Farmakoloji</option>
                    <option value="Tıbbi Mikrobiyoloji">Tıbbi Mikrobiyoloji</option>
                  </select>
                </div>

                <div>
                  <label className="font-bold text-ink-2 block mb-1">Ders Başlığı</label>
                  <input
                    type="text"
                    required
                    placeholder="Örn: 2) Hücre Hasarı ve Nekroz"
                    value={newTitle}
                    onChange={(e) => setNewTitle(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-line-2 focus:ring-2 focus:ring-ok"
                  />
                </div>

                <div>
                  <label className="font-bold text-ink-2 block mb-1">Dersi Veren Öğretim Üyesi (İsteğe bağlı)</label>
                  <input
                    type="text"
                    placeholder="Örn: Prof. Dr. ..."
                    value={newInstructor}
                    onChange={(e) => setNewInstructor(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-line-2"
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="font-bold text-ink-2 block">
                      Ders Notu / Slayt İçeriği (Sayfa sayfa yapıştırın)
                    </label>
                    <span className="text-2xs text-ink-3">
                      Sayfa ayracı: <code>{pageDelimiter}</code>
                    </span>
                  </div>
                  <textarea
                    required
                    rows={8}
                    placeholder={`Sayfa 1 slayt metni...\n\n--- Sayfa ---\n\nSayfa 2 slayt metni...\n\n--- Sayfa ---\n\nSayfa 3 slayt metni...`}
                    value={newRawContent}
                    onChange={(e) => setNewRawContent(e.target.value)}
                    className="w-full p-3 rounded-lg border border-line-2 font-mono text-xs focus:ring-2 focus:ring-ok"
                  />
                  <p className="text-2xs text-ink-3 mt-1">
                    İpucu: Slayt sayfalarını ayırmak için aralarına <code>--- Sayfa ---</code> yazın. Sayfalar numaralandırılacak ve soru eşleştirmelerinde kullanılacaktır.
                  </p>
                </div>

                <div className="flex items-center justify-end gap-2 pt-2 border-t border-line">
                  <button
                    type="button"
                    onClick={() => setIsAddingNote(false)}
                    className="px-4 py-2 rounded-lg border border-line-2 text-ink-2 hover:bg-field cursor-pointer"
                  >
                    İptal
                  </button>
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="px-5 py-2 rounded-lg bg-ok hover:bg-ok text-white font-bold flex items-center gap-1.5 shadow-sm cursor-pointer"
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    <span>{isSubmitting ? 'Kaydediliyor...' : 'Ders Notunu Render Et & Kaydet'}</span>
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}

      {/* Slide Reader Modal */}
      <SlideReaderModal
        isOpen={Boolean(readerNote)}
        note={readerNote}
        onClose={() => setReaderNote(null)}
      />
    </div>
  );
};
