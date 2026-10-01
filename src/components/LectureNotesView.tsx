import React, { useState, useEffect, useMemo } from 'react';
import { 
  BookMarked, 
  Search, 
  FileText, 
  CheckCircle2, 
  ExternalLink, 
  Copy, 
  Check, 
  Download, 
  UploadCloud, 
  FileUp, 
  RefreshCw, 
  SlidersHorizontal, 
  FolderGit2, 
  ChevronRight, 
  Trash2, 
  Play, 
  Eye, 
  Sparkles,
  AlertCircle,
  Plus,
  BookOpen,
  FolderOpen
} from 'lucide-react';
import { LectureNote, QuestionItem, QuestionLectureMatch, UserProfile, Committee } from '../types';
import { 
  DRIVE_SLIDES_CATALOG, 
  DriveSlideMeta, 
  DRIVE_FOLDER_ID, 
  DRIVE_FOLDER_URL 
} from '../data/driveCatalog';
import { renderSingleDriveSlide } from '../services/driveAutomation';
import { SlideReaderModal } from './SlideReaderModal';
import { db, cleanForFirestore } from '../services/firestoreDb';
import { collection, doc, setDoc, deleteDoc, getDocs } from 'firebase/firestore';
import { ApiService } from '../services/api';

interface LectureNotesViewProps {
  committee?: Committee;
  committees: Committee[];
  questions: QuestionItem[];
  currentUser: UserProfile | null;
  isAdmin: boolean;
  onUpdateQuestionReference: (questionId: string, reference: QuestionLectureMatch) => Promise<void>;
}

const LOCAL_NOTES_KEY = 'medsoru_lecture_notes_v3';

export const LectureNotesView: React.FC<LectureNotesViewProps> = ({
  committee,
  questions,
  currentUser,
  isAdmin,
  onUpdateQuestionReference,
}) => {
  // Main view tab: 'drive_catalog' (Google Drive Slayt Kataloğu) or 'rendered_notes' (İşlenmiş Notlar & Okuyucu)
  const [activeTab, setActiveTab] = useState<'drive_catalog' | 'rendered_notes'>('drive_catalog');

  // Notes state - starts strictly with persistent server/firestore data, NEVER pre-seeded with fake 5-page mocks
  const [notes, setNotes] = useState<LectureNote[]>(() => {
    try {
      const stored = localStorage.getItem(LOCAL_NOTES_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed.filter(n => !n.id.startsWith('mock-'));
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

  // Save notes to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(LOCAL_NOTES_KEY, JSON.stringify(notes));
    } catch (e) {}
  }, [notes]);

  // Load verified notes from Server API and Firestore
  useEffect(() => {
    async function loadSavedNotes() {
      // 1. Server API
      try {
        const res = await fetch('/api/lecture-notes');
        if (res.ok) {
          const apiNotes: LectureNote[] = await res.json();
          if (Array.isArray(apiNotes) && apiNotes.length > 0) {
            setNotes(apiNotes);
            setActiveNote(apiNotes[0]);
            return;
          }
        }
      } catch (e) {}

      // 2. Firestore fallback
      try {
        const colRef = collection(db, 'lecture_notes');
        const snap = await getDocs(colRef);
        if (!snap.empty) {
          const remote: LectureNote[] = [];
          snap.forEach(d => remote.push(d.data() as LectureNote));
          if (remote.length > 0) {
            setNotes(remote);
            setActiveNote(remote[0]);
          }
        }
      } catch (e) {}
    }

    loadSavedNotes();
  }, []);

  // Compute catalog statistics
  const TOTAL_CATALOG_SLIDES = DRIVE_SLIDES_CATALOG.length; // 40
  const TOTAL_CATALOG_PAGES = useMemo(() => {
    return DRIVE_SLIDES_CATALOG.reduce((acc, s) => acc + s.totalRealPages, 0); // 1,353
  }, []);

  const renderedNotesMap = useMemo(() => {
    const map = new Map<string, LectureNote>();
    notes.forEach(n => {
      map.set(n.id, n);
      if (n.driveFileId) map.set(n.driveFileId, n);
    });
    return map;
  }, [notes]);

  const renderedSlidesCount = useMemo(() => {
    return DRIVE_SLIDES_CATALOG.filter(s => renderedNotesMap.has(s.id)).length;
  }, [renderedNotesMap]);

  const renderedPagesCount = useMemo(() => {
    return DRIVE_SLIDES_CATALOG
      .filter(s => renderedNotesMap.has(s.id))
      .reduce((acc, s) => acc + s.totalRealPages, 0);
  }, [renderedNotesMap]);

  const progressPercent = Math.round((renderedPagesCount / TOTAL_CATALOG_PAGES) * 100);

  // Filter catalog slides
  const filteredCatalog = useMemo(() => {
    return DRIVE_SLIDES_CATALOG.filter(s => {
      if (catalogDiscipline !== 'Tümü' && s.discipline !== catalogDiscipline) return false;
      const isRendered = renderedNotesMap.has(s.id);
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
  }, [catalogDiscipline, catalogStatusFilter, catalogSearch, renderedNotesMap]);

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
    if (!confirm(`"${title}" ders notunu silmek istediğinize emin misiniz?`)) return;

    setNotes(prev => prev.filter(n => n.id !== id));
    if (activeNote?.id === id) {
      const remaining = notes.filter(n => n.id !== id);
      setActiveNote(remaining[0] || null);
    }

    try {
      await fetch(`/api/lecture-notes/${id}`, { method: 'DELETE' });
    } catch (e) {}

    try {
      await deleteDoc(doc(db, 'lecture_notes', id));
    } catch (e) {}

    setFeedbackMessage(`"${title}" silindi.`);
  };

  // Handler: Purge all local/sample notes
  const handlePurgeMockNotes = () => {
    if (!confirm('Yerel hafızadaki tüm örnek ders notlarını silmek ve listeyi sıfırlamak istediğinize emin misiniz?')) return;
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

      // 2. Save Server API
      try {
        await fetch('/api/lecture-notes', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newNote),
        });
      } catch (err) {}

      // 3. Save Firestore
      try {
        await setDoc(doc(db, 'lecture_notes', newNote.id), cleanForFirestore(newNote));
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
          await fetch('/api/lecture-notes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newNote),
          });
        } catch (err) {}

        try {
          await setDoc(doc(db, 'lecture_notes', newNote.id), cleanForFirestore(newNote));
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

  return (
    <div className="space-y-6">
      {/* Top Header Card */}
      <div className="bg-slate-900 text-white rounded-2xl p-5 sm:p-6 shadow-xl border border-slate-800 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-teal-400">
              <FolderGit2 className="w-5 h-5" />
              <span className="text-xs font-bold uppercase tracking-wider">Masaüstü & Google Drive Ders Notu Merkezi</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-black tracking-tight">
              Kurul 1 Ders Slaytları & Birebir Not Havuzu
            </h2>
            <p className="text-xs text-slate-400 max-w-2xl leading-relaxed">
              <strong>C:\\Users\\indui\\Desktop\\meds_database</strong> klasörüne eklenen veya Drive'a yüklenen PDF ders notları her gün saat 18:00'da ve anında taranır. Tüm sayfalar yapay zeka yorumu veya özetleme olmaksızın birebir metin olarak veritabanına işlenir.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2 shrink-0">
            <button
              onClick={handleTriggerDesktopSync}
              disabled={isSyncingDesktop}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-bold px-3.5 py-2 rounded-xl text-xs flex items-center gap-1.5 shadow-md transition-all cursor-pointer active:scale-95"
              title="C:\\Users\\indui\\Desktop\\meds_database klasörünü şimdi tara ve yeni PDF'leri veritabanına ekle"
            >
              {isSyncingDesktop ? (
                <>
                  <RefreshCw className="w-4 h-4 text-indigo-200 animate-spin" />
                  <span>Taranıyor...</span>
                </>
              ) : (
                <>
                  <FolderOpen className="w-4 h-4 text-indigo-200" />
                  <span>Masaüstü Klasörünü Tara (meds_database)</span>
                </>
              )}
            </button>

            <a
              href={DRIVE_FOLDER_URL}
              target="_blank"
              rel="noreferrer"
              className="bg-white/10 hover:bg-white/20 text-white px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all border border-white/10"
            >
              <ExternalLink className="w-4 h-4 text-teal-400" />
              <span>Drive Klasörünü Aç</span>
            </a>

            <button
              onClick={() => setIsAddingNote(true)}
              className="bg-teal-600 hover:bg-teal-500 text-white font-bold px-4 py-2 rounded-xl text-xs flex items-center gap-1.5 shadow-md transition-all cursor-pointer active:scale-95"
            >
              <Plus className="w-4 h-4" />
              <span>Yeni Slayt / Not Yükle</span>
            </button>
          </div>
        </div>

        {/* Global Progress Bar Banner */}
        <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700 space-y-2.5">
          <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
            <div className="flex items-center gap-2">
              <span className="text-slate-300 font-semibold">Genel İşleme İlerlemesi:</span>
              <span className="font-bold text-teal-300">
                {renderedSlidesCount} / {TOTAL_CATALOG_SLIDES} Slayt İşlendi
              </span>
              <span className="text-slate-400 text-[11px]">
                ({renderedPagesCount.toLocaleString('tr-TR')} / {TOTAL_CATALOG_PAGES.toLocaleString('tr-TR')} Sayfa • %{progressPercent})
              </span>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-[11px] text-amber-300 font-medium">
                Kalan: {(TOTAL_CATALOG_PAGES - renderedPagesCount).toLocaleString('tr-TR')} Sayfa
              </span>
              {notes.length > 0 && (
                <button
                  onClick={handlePurgeMockNotes}
                  title="Önbellekte kalan eski veya 5 sayfalık örnek notları temizler"
                  className="text-[10px] text-rose-400 hover:text-rose-300 underline cursor-pointer ml-2"
                >
                  Örnekleri Temizle
                </button>
              )}
            </div>
          </div>

          <div className="w-full bg-slate-900 rounded-full h-3 overflow-hidden p-0.5 border border-slate-700">
            <div 
              className="bg-linear-to-r from-teal-500 to-emerald-400 h-full rounded-full transition-all duration-500 shadow-sm"
              style={{ width: `${Math.max(2, progressPercent)}%` }}
            />
          </div>
        </div>

        {/* Feedback alert */}
        {feedbackMessage && (
          <div className="p-3 bg-teal-950/80 border border-teal-500/40 rounded-xl text-teal-200 text-xs flex items-center justify-between animate-fade-in">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0" />
              <span>{feedbackMessage}</span>
            </div>
            <button onClick={() => setFeedbackMessage(null)} className="text-teal-400 hover:text-white text-xs">
              ✕
            </button>
          </div>
        )}

        {/* Navigation Tabs */}
        <div className="flex border-b border-slate-800 pt-2 gap-2 text-xs font-bold">
          <button
            onClick={() => setActiveTab('drive_catalog')}
            className={`pb-3 px-4 border-b-2 flex items-center gap-2 transition-colors cursor-pointer ${
              activeTab === 'drive_catalog'
                ? 'border-teal-400 text-teal-300'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <FolderGit2 className="w-4 h-4" />
            <span>Google Drive Slayt Kataloğu ({TOTAL_CATALOG_SLIDES} Dosya)</span>
          </button>

          <button
            onClick={() => setActiveTab('rendered_notes')}
            className={`pb-3 px-4 border-b-2 flex items-center gap-2 transition-colors cursor-pointer ${
              activeTab === 'rendered_notes'
                ? 'border-teal-400 text-teal-300'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <BookOpen className="w-4 h-4" />
            <span>İşlenmiş Notlar & Sayfa Okuyucu</span>
            <span className="bg-teal-500/20 text-teal-300 text-[10px] px-2 py-0.5 rounded-full border border-teal-500/30">
              {notes.length}
            </span>
          </button>
        </div>
      </div>

      {/* TAB 1: GOOGLE DRIVE SLIDES CATALOG */}
      {activeTab === 'drive_catalog' && (
        <div className="space-y-4">
          {/* Filter Bar */}
          <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-xs space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              {/* Search */}
              <div className="relative flex-1">
                <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Drive slayt adı veya konu ara (örn. Nekroz, Glomerül, BPH, Sepsis)..."
                  value={catalogSearch}
                  onChange={(e) => setCatalogSearch(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-teal-500/30 focus:bg-white"
                />
              </div>

              {/* Status Filter */}
              <div className="flex items-center gap-1.5 text-xs shrink-0">
                <span className="text-slate-500 font-semibold text-[11px]">Durum:</span>
                <button
                  onClick={() => setCatalogStatusFilter('all')}
                  className={`px-2.5 py-1.5 rounded-lg font-bold text-xs cursor-pointer ${
                    catalogStatusFilter === 'all'
                      ? 'bg-slate-900 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  Tümü ({TOTAL_CATALOG_SLIDES})
                </button>
                <button
                  onClick={() => setCatalogStatusFilter('unrendered')}
                  className={`px-2.5 py-1.5 rounded-lg font-bold text-xs cursor-pointer ${
                    catalogStatusFilter === 'unrendered'
                      ? 'bg-amber-600 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  İşlenmemiş ({TOTAL_CATALOG_SLIDES - renderedSlidesCount})
                </button>
                <button
                  onClick={() => setCatalogStatusFilter('rendered')}
                  className={`px-2.5 py-1.5 rounded-lg font-bold text-xs cursor-pointer ${
                    catalogStatusFilter === 'rendered'
                      ? 'bg-emerald-600 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  İşlenmiş ({renderedSlidesCount})
                </button>
              </div>
            </div>

            {/* Discipline Badges */}
            <div className="flex flex-wrap gap-1.5 pt-1 border-t border-slate-100 text-xs">
              {[
                { name: 'Tümü', count: 40 },
                { name: 'Tıbbi Patoloji', count: 22 },
                { name: 'Tıbbi Genetik', count: 5 },
                { name: 'Halk Sağlığı', count: 5 },
                { name: 'Üroloji', count: 4 },
                { name: 'Enfeksiyon Hastalıkları', count: 4 },
              ].map((d) => (
                <button
                  key={d.name}
                  onClick={() => setCatalogDiscipline(d.name)}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold cursor-pointer transition-colors ${
                    catalogDiscipline === d.name
                      ? 'bg-teal-700 text-white shadow-xs'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {d.name} <span className="opacity-70 text-[10px]">({d.count})</span>
                </button>
              ))}
            </div>
          </div>

          {/* Slide Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredCatalog.map((slide) => {
              const isRendered = renderedNotesMap.has(slide.id);
              const renderedNote = renderedNotesMap.get(slide.id);
              const isProcessing = renderingSlideId === slide.id;

              return (
                <div
                  key={slide.id}
                  className={`rounded-2xl p-5 border transition-all space-y-3.5 ${
                    isRendered
                      ? 'bg-emerald-50/40 border-emerald-300 shadow-xs'
                      : 'bg-white border-slate-200 hover:border-teal-300 shadow-xs'
                  }`}
                >
                  {/* Card Header */}
                  <div className="flex items-start justify-between gap-3">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
                          {slide.discipline}
                        </span>
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-teal-100 text-teal-800">
                          {slide.totalRealPages} Gerçek Sayfa
                        </span>
                      </div>
                      <h3 className="font-bold text-sm text-slate-900 leading-snug">
                        {slide.title}
                      </h3>
                    </div>

                    {isRendered ? (
                      <span className="inline-flex items-center gap-1 bg-emerald-100 text-emerald-800 text-[11px] font-bold px-2.5 py-1 rounded-full border border-emerald-300 shrink-0">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        <span>Render Edildi</span>
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 bg-slate-100 text-slate-600 text-[11px] font-bold px-2.5 py-1 rounded-full border border-slate-200 shrink-0">
                        <span>İşlenmedi</span>
                      </span>
                    )}
                  </div>

                  {/* Key Topics */}
                  <div className="space-y-1">
                    <span className="text-[10px] text-slate-400 font-semibold uppercase block">
                      Dersin Kapsadığı Konular:
                    </span>
                    <div className="flex flex-wrap gap-1">
                      {slide.keyTopics.map((topic, i) => (
                        <span
                          key={i}
                          className="bg-slate-100 text-slate-600 text-[10px] px-2 py-0.5 rounded-md font-medium"
                        >
                          {topic}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Card Actions */}
                  <div className="pt-2 border-t border-slate-100 flex items-center justify-between gap-2">
                    <a
                      href={`https://drive.google.com/file/d/${slide.fileId}/view?usp=sharing`}
                      target="_blank"
                      rel="noreferrer"
                      className="text-xs text-slate-500 hover:text-teal-700 flex items-center gap-1"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                      <span>Drive'da İncele</span>
                    </a>

                    <div className="flex items-center gap-2">
                      {isRendered ? (
                        <>
                          <button
                            onClick={() => {
                              if (renderedNote) {
                                setActiveNote(renderedNote);
                                setActiveTab('rendered_notes');
                              }
                            }}
                            className="bg-emerald-700 hover:bg-emerald-800 text-white font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1 cursor-pointer shadow-xs"
                          >
                            <Eye className="w-3.5 h-3.5" />
                            <span>Sayfaları Oku</span>
                          </button>

                          <button
                            onClick={() => handleRenderSlide(slide)}
                            disabled={isProcessing}
                            title="Tüm sayfaları yeniden oluşturup günceller"
                            className="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 cursor-pointer"
                          >
                            <RefreshCw className={`w-3.5 h-3.5 ${isProcessing ? 'animate-spin' : ''}`} />
                          </button>

                          <button
                            onClick={() => handleDeleteNote(slide.id, slide.title)}
                            title="İşlenmiş notu siler"
                            className="text-rose-400 hover:text-rose-600 p-1.5 rounded-lg hover:bg-rose-50 cursor-pointer"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </>
                      ) : (
                        <button
                          onClick={() => handleRenderSlide(slide)}
                          disabled={isProcessing}
                          className="bg-teal-700 hover:bg-teal-800 text-white font-bold px-3.5 py-1.5 rounded-lg text-xs flex items-center gap-1.5 cursor-pointer shadow-xs disabled:opacity-50"
                        >
                          {isProcessing ? (
                            <>
                              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                              <span>{slide.totalRealPages} Sayfa İşleniyor...</span>
                            </>
                          ) : (
                            <>
                              <Play className="w-3.5 h-3.5 fill-current" />
                              <span>Bu Slaytı Render Et ({slide.totalRealPages} Sayfa)</span>
                            </>
                          )}
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {filteredCatalog.length === 0 && (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
              <Search className="w-10 h-10 text-slate-300 mx-auto" />
              <h4 className="font-bold text-slate-800">Aramanıza uygun slayt bulunamadı</h4>
              <p className="text-xs text-slate-500">
                Farklı bir anabilim dalı veya anahtar kelime seçebilirsiniz.
              </p>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: RENDERED NOTES & SLIDE READER */}
      {activeTab === 'rendered_notes' && (
        <div className="space-y-4">
          {notes.length === 0 ? (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-4 shadow-xs">
              <div className="w-14 h-14 rounded-2xl bg-teal-50 text-teal-600 flex items-center justify-center mx-auto">
                <BookMarked className="w-8 h-8" />
              </div>
              <div className="space-y-1">
                <h4 className="font-bold text-base text-slate-900">Henüz Render Edilmiş Ders Notu Bulunmuyor</h4>
                <p className="text-xs text-slate-500 max-w-md mx-auto leading-relaxed">
                  Gerçek dışı örnek notlar temizlendi. Google Drive kataloğundan istediğiniz slaytı tek tıkla renderlayabilir ya da "+ Yeni Slayt / Not Yükle" butonunu kullanarak kendi ders notunuzu ekleyebilirsiniz.
                </p>
              </div>
              <button
                onClick={() => setActiveTab('drive_catalog')}
                className="bg-teal-700 hover:bg-teal-800 text-white font-bold px-4 py-2 rounded-xl text-xs inline-flex items-center gap-1.5 cursor-pointer shadow-sm"
              >
                <FolderGit2 className="w-4 h-4" />
                <span>Google Drive Slayt Kataloğuna Git</span>
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Left Sidebar: Rendered Notes List */}
              <div className="lg:col-span-4 space-y-3">
                <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-xs space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-bold text-sm text-slate-900">İşlenmiş Notlar ({notes.length})</h3>
                    <button
                      onClick={() => setActiveTab('drive_catalog')}
                      className="text-[11px] font-bold text-teal-700 hover:underline"
                    >
                      + Daha Fazla Slayt Ekle
                    </button>
                  </div>

                  <div className="relative">
                    <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                    <input
                      type="text"
                      placeholder="Notlarda ara..."
                      value={notesSearch}
                      onChange={(e) => setNotesSearch(e.target.value)}
                      className="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                    />
                  </div>

                  <div className="space-y-1.5 max-h-[600px] overflow-y-auto pr-1">
                    {filteredRenderedNotes.map((note) => {
                      const isSelected = activeNote?.id === note.id;
                      return (
                        <div
                          key={note.id}
                          onClick={() => setActiveNote(note)}
                          className={`p-3 rounded-xl border text-left cursor-pointer transition-all ${
                            isSelected
                              ? 'bg-teal-50 border-teal-500 shadow-xs'
                              : 'bg-white border-slate-200 hover:border-slate-300'
                          }`}
                        >
                          <div className="flex items-center justify-between text-[10px] text-slate-400 mb-1">
                            <span className="font-bold uppercase text-teal-700">{note.discipline}</span>
                            <span>{note.totalSlides} Sayfa</span>
                          </div>
                          <h4 className="font-bold text-xs text-slate-900 line-clamp-1">{note.title}</h4>
                          <p className="text-[11px] text-slate-500 mt-0.5">
                            {note.instructor || 'Anabilim Dalı'} • {new Date(note.uploadedAt).toLocaleDateString('tr-TR')}
                          </p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Right Content: Page-by-Page Interactive Slide Reader */}
              <div className="lg:col-span-8">
                {activeNote ? (
                  <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden space-y-4 p-5 sm:p-6">
                    {/* Note Header */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="bg-teal-100 text-teal-800 text-[10px] font-bold px-2 py-0.5 rounded-full">
                            {activeNote.discipline}
                          </span>
                          <span className="text-slate-400 text-xs">
                            Toplam {activeNote.totalSlides} Sayfa
                          </span>
                        </div>
                        <h3 className="font-black text-lg text-slate-900">{activeNote.title}</h3>
                        <p className="text-xs text-slate-500 mt-0.5">
                          {activeNote.instructor && `Eğitici: ${activeNote.instructor} • `}
                          Yükleyen: {activeNote.uploadedBy}
                        </p>
                      </div>

                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => setReaderNote(activeNote)}
                          className="bg-slate-900 hover:bg-slate-800 text-white font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 cursor-pointer shadow-xs"
                        >
                          <BookOpen className="w-3.5 h-3.5" />
                          <span>Tam Ekran Okuyucu</span>
                        </button>

                        <button
                          onClick={() => handleDeleteNote(activeNote.id, activeNote.title)}
                          className="text-rose-500 hover:text-rose-700 p-1.5 rounded-lg hover:bg-rose-50 cursor-pointer"
                          title="Bu notu sil"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>

                    {/* Pages List */}
                    <div className="space-y-4 max-h-[700px] overflow-y-auto pr-2">
                      {activeNote.pages.map((page) => (
                        <div
                          key={page.pageNumber}
                          className="border border-slate-200 rounded-xl p-4 bg-slate-50/50 space-y-2.5"
                        >
                          <div className="flex items-center justify-between text-xs border-b border-slate-200/60 pb-2">
                            <span className="font-bold text-slate-700 bg-white px-2 py-0.5 rounded border border-slate-200">
                              Sayfa / Slayt #{page.pageNumber} / {activeNote.totalSlides}
                            </span>

                            <button
                              onClick={() => copyPageContent(page.content, page.pageNumber)}
                              className="text-slate-500 hover:text-slate-900 flex items-center gap-1 cursor-pointer text-[11px]"
                            >
                              {copySuccess[page.pageNumber] ? (
                                <>
                                  <Check className="w-3 h-3 text-emerald-600" />
                                  <span className="text-emerald-700 font-bold">Kopyalandı</span>
                                </>
                              ) : (
                                <>
                                  <Copy className="w-3 h-3" />
                                  <span>Sayfa Metnini Kopyala</span>
                                </>
                              )}
                            </button>
                          </div>

                          <div className="text-xs text-slate-800 whitespace-pre-wrap leading-relaxed font-sans bg-white p-3.5 rounded-lg border border-slate-100">
                            {page.content}
                          </div>

                          {page.keywords && page.keywords.length > 0 && (
                            <div className="flex flex-wrap gap-1 items-center pt-1">
                              <span className="text-[10px] text-slate-400 font-bold">Kavramlar:</span>
                              {page.keywords.map((kw, i) => (
                                <span
                                  key={i}
                                  className="bg-slate-200/70 text-slate-700 text-[10px] px-1.5 py-0.5 rounded"
                                >
                                  {kw}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-slate-400">
                    Sol taraftaki listeden görüntülemek istediğiniz ders notunu seçiniz.
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* MODAL: ADD MANUAL / CUSTOM LECTURE NOTE */}
      {isAddingNote && (
        <div className="fixed inset-0 z-50 bg-slate-950/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl border border-slate-200 max-w-2xl w-full p-6 shadow-2xl space-y-4 my-8">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-2 text-slate-900 font-bold">
                <BookMarked className="w-5 h-5 text-teal-600" />
                <span>Yeni Ders Notu / Slayt Yükle</span>
              </div>
              <button
                onClick={() => setIsAddingNote(false)}
                className="text-slate-400 hover:text-slate-600 text-xs px-2 py-1 cursor-pointer"
              >
                Kapat
              </button>
            </div>

            {/* Upload Mode Selector */}
            <div className="flex border-b border-slate-200 text-xs font-bold">
              <button
                type="button"
                onClick={() => setAddMode('text')}
                className={`flex-1 py-2 text-center border-b-2 cursor-pointer transition-colors ${
                  addMode === 'text'
                    ? 'border-teal-700 text-teal-900 bg-teal-50/50'
                    : 'border-transparent text-slate-500 hover:text-slate-800'
                }`}
              >
                ✍️ Metin Yapıştırarak Ekle
              </button>
              <button
                type="button"
                onClick={() => setAddMode('upload')}
                className={`flex-1 py-2 text-center border-b-2 cursor-pointer transition-colors ${
                  addMode === 'upload'
                    ? 'border-teal-700 text-teal-900 bg-teal-50/50'
                    : 'border-transparent text-slate-500 hover:text-slate-800'
                }`}
              >
                📄 PDF / DOCX Dosyası Yükle
              </button>
            </div>

            {addMode === 'upload' ? (
              <div className="space-y-4 text-xs">
                <div className="border-2 border-dashed border-teal-300 rounded-xl p-6 text-center bg-teal-50/30 space-y-3">
                  <div className="w-12 h-12 rounded-full bg-teal-100 text-teal-700 flex items-center justify-center mx-auto">
                    <UploadCloud className="w-6 h-6" />
                  </div>
                  <div>
                    <h4 className="font-bold text-slate-900">Ders Slaytını Yükleyin (.pdf veya .docx)</h4>
                    <p className="text-slate-500 text-[11px] mt-1">
                      Sistem slayttaki tüm sayfaları metin olarak ayıklar ve soru eşleştirmelerine bağlar.
                    </p>
                  </div>
                  <label className="inline-flex items-center gap-2 bg-teal-700 hover:bg-teal-800 text-white font-bold px-4 py-2 rounded-lg cursor-pointer transition-all shadow-xs">
                    <FileUp className="w-4 h-4 text-teal-200" />
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
                  <div className="p-3 bg-amber-50 border border-amber-300 text-amber-950 rounded-xl flex items-center gap-2.5 font-medium animate-pulse">
                    <RefreshCw className="w-4 h-4 text-amber-700 animate-spin shrink-0" />
                    <span>{pdfUploadStatus}</span>
                  </div>
                )}
              </div>
            ) : (
              <form onSubmit={handleSaveManualNote} className="space-y-4 text-xs">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Ders / Anabilim Dalı</label>
                  <select
                    value={newDiscipline}
                    onChange={(e) => setNewDiscipline(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 bg-white"
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
                  <label className="font-bold text-slate-700 block mb-1">Ders Başlığı</label>
                  <input
                    type="text"
                    required
                    placeholder="Örn: 2) Hücre Hasarı ve Nekroz"
                    value={newTitle}
                    onChange={(e) => setNewTitle(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-teal-500"
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Dersi Veren Öğretim Üyesi (İsteğe bağlı)</label>
                  <input
                    type="text"
                    placeholder="Örn: Prof. Dr. ..."
                    value={newInstructor}
                    onChange={(e) => setNewInstructor(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300"
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="font-bold text-slate-700 block">
                      Ders Notu / Slayt İçeriği (Sayfa sayfa yapıştırın)
                    </label>
                    <span className="text-[11px] text-slate-500">
                      Sayfa ayracı: <code>{pageDelimiter}</code>
                    </span>
                  </div>
                  <textarea
                    required
                    rows={8}
                    placeholder={`Sayfa 1 slayt metni...\n\n--- Sayfa ---\n\nSayfa 2 slayt metni...\n\n--- Sayfa ---\n\nSayfa 3 slayt metni...`}
                    value={newRawContent}
                    onChange={(e) => setNewRawContent(e.target.value)}
                    className="w-full p-3 rounded-lg border border-slate-300 font-mono text-xs focus:ring-2 focus:ring-teal-500"
                  />
                  <p className="text-[11px] text-slate-500 mt-1">
                    İpucu: Slayt sayfalarını ayırmak için aralarına <code>--- Sayfa ---</code> yazın. Sayfalar numaralandırılacak ve soru eşleştirmelerinde kullanılacaktır.
                  </p>
                </div>

                <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={() => setIsAddingNote(false)}
                    className="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-50 cursor-pointer"
                  >
                    İptal
                  </button>
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="px-5 py-2 rounded-lg bg-teal-700 hover:bg-teal-800 text-white font-bold flex items-center gap-1.5 shadow-sm cursor-pointer"
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
