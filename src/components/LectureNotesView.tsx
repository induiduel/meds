import React, { useState, useEffect, useMemo } from 'react';
import { 
  BookMarked, 
  Plus, 
  Search, 
  FileText, 
  Sparkles, 
  CheckCircle2, 
  ExternalLink, 
  Layers, 
  User, 
  Hash, 
  ChevronRight, 
  AlertCircle,
  HelpCircle,
  ArrowRight,
  BookOpen,
  Trash2,
  Filter,
  Cloud,
  RefreshCw,
  FolderOpen,
  ChevronDown,
  Download,
  Copy,
  Check,
  UploadCloud,
  FileUp
} from 'lucide-react';
import { LectureNote, QuestionItem, Committee, QuestionLectureMatch } from '../types';
import { AppUser } from '../services/auth';
import { getFirestore, collection, getDocs, doc, setDoc, deleteDoc } from 'firebase/firestore';
import { db, cleanForFirestore } from '../services/firestoreDb';
import { ApiService } from '../services/api';
import { InfoPopover } from './InfoPopover';
import { SlideReaderModal } from './SlideReaderModal';
import { 
  TARGET_DRIVE_FOLDER_ID, 
  TARGET_DRIVE_FOLDER_URL, 
  REAL_KURUL1_DRIVE_SLIDES,
  getAutomationStatus, 
  runDriveSyncAndAutoMatch,
  ensureAllSlidePages
} from '../services/driveAutomation';

interface LectureNotesViewProps {
  committee: Committee | undefined;
  committees: Committee[];
  questions: QuestionItem[];
  currentUser: AppUser | null;
  isAdmin: boolean;
  onUpdateQuestionReference: (questionId: string, reference: QuestionLectureMatch) => Promise<void>;
}

const LOCAL_NOTES_KEY = 'medsoru_lecture_notes_v2';

export const LectureNotesView: React.FC<LectureNotesViewProps> = ({
  committee,
  committees,
  questions,
  currentUser,
  isAdmin,
  onUpdateQuestionReference,
}) => {
  const [notes, setNotes] = useState<LectureNote[]>(() => {
    try {
      const stored = localStorage.getItem(LOCAL_NOTES_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed.map((n) => ({
            ...n,
            totalSlides: n.pages?.length || n.totalSlides || 1,
            pages: n.pages || [],
          }));
        }
      }
    } catch (e) {}
    return REAL_KURUL1_DRIVE_SLIDES.map(s => ({
      ...s,
      committeeId: committee?.id || 'donem3-kurul1',
      totalSlides: s.pages?.length || 5,
      pages: s.pages || [],
    }));
  });

  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('Tümü');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeNote, setActiveNote] = useState<LectureNote | null>(() => {
    return notes[0] || null;
  });

  // Export & Reader Enhancements
  const [exportFeedback, setExportFeedback] = useState<string | null>(null);
  const [copyPageSuccess, setCopyPageSuccess] = useState<Record<number, boolean>>({});
  const [slideSearchQuery, setSlideSearchQuery] = useState('');
  const [isUploadingPdf, setIsUploadingPdf] = useState(false);
  const [pdfUploadStatus, setPdfUploadStatus] = useState<string | null>(null);
  const [addMode, setAddMode] = useState<'upload' | 'text'>('upload');

  // Google Drive Automation State & Live Rendering Progress
  const [isSyncingDrive, setIsSyncingDrive] = useState(false);
  const [driveSyncFeedback, setDriveSyncFeedback] = useState<string | null>(null);
  const [currentlyRenderingSlide, setCurrentlyRenderingSlide] = useState<string | null>(null);

  // New Note Modal / Form state
  const [isAddingNote, setIsAddingNote] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newDiscipline, setNewDiscipline] = useState('Tıbbi Patoloji');
  const [newInstructor, setNewInstructor] = useState('');
  const [newRawContent, setNewRawContent] = useState('');
  const [pageDelimiter, setPageDelimiter] = useState('--- Sayfa ---');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Matching tool state
  const [matchingQuestionId, setMatchingQuestionId] = useState<string | null>(null);
  const [isMatching, setIsMatching] = useState(false);
  const [readerNote, setReaderNote] = useState<LectureNote | null>(null);
  const [collapsedCategories, setCollapsedCategories] = useState<Record<string, boolean>>({});

  const toggleCategory = (cat: string) => {
    setCollapsedCategories((prev) => ({ ...prev, [cat]: !prev[cat] }));
  };

  // Export full slide text as TXT, Markdown, or clipboard
  const exportNoteText = (note: LectureNote, format: 'txt' | 'md' | 'copy') => {
    let content = '';
    if (format === 'md') {
      content = `# ${note.title}\n\n`;
      content += `**Anabilim Dalı:** ${note.discipline}  \n`;
      if (note.instructor) content += `**Öğretim Üyesi:** ${note.instructor}  \n`;
      content += `**Toplam Slayt/Sayfa:** ${note.totalSlides}  \n`;
      content += `**Dışa Aktarım Tarihi:** ${new Date().toLocaleDateString('tr-TR')}  \n\n---\n\n`;
      note.pages.forEach((p) => {
        content += `## Sayfa ${p.pageNumber}\n\n${p.content}\n\n`;
        if (p.keywords && p.keywords.length > 0) {
          content += `*Anahtar Kelimeler: ${p.keywords.join(', ')}*\n\n`;
        }
        content += `---\n\n`;
      });
    } else {
      content = `========================================================\n`;
      content += `${note.title.toUpperCase()}\n`;
      content += `Anabilim Dalı: ${note.discipline}\n`;
      if (note.instructor) content += `Öğretim Üyesi: ${note.instructor}\n`;
      content += `Toplam Slayt Sayısı: ${note.totalSlides}\n`;
      content += `Dışa Aktarım Tarihi: ${new Date().toLocaleString('tr-TR')}\n`;
      content += `========================================================\n\n`;
      note.pages.forEach((p) => {
        content += `--- SAYFA ${p.pageNumber} ---\n`;
        content += `${p.content}\n`;
        if (p.keywords && p.keywords.length > 0) {
          content += `Anahtar Kelimeler: ${p.keywords.join(', ')}\n`;
        }
        content += `\n`;
      });
    }

    if (format === 'copy') {
      navigator.clipboard.writeText(content);
      setExportFeedback('✓ Slaytın tüm metni panoya kopyalandı!');
      setTimeout(() => setExportFeedback(null), 3500);
    } else {
      const sanitized = note.title.replace(/[^a-zA-Z0-9_\u00C0-\u017F-]/g, '_');
      const filename = `${sanitized}_Metni.${format}`;
      const blob = new Blob([content], {
        type: format === 'md' ? 'text/markdown;charset=utf-8' : 'text/plain;charset=utf-8',
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      setExportFeedback(`✓ "${filename}" başarıyla dışarı aktarıldı!`);
      setTimeout(() => setExportFeedback(null), 3500);
    }
  };

  // Copy single page content
  const copyPageContent = (pageNumber: number, text: string) => {
    navigator.clipboard.writeText(text);
    setCopyPageSuccess((prev) => ({ ...prev, [pageNumber]: true }));
    setTimeout(() => {
      setCopyPageSuccess((prev) => ({ ...prev, [pageNumber]: false }));
    }, 2000);
  };

  // Direct PDF/DOCX file upload and extraction
  const handlePdfFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploadingPdf(true);
    setPdfUploadStatus(`"${file.name}" okunuyor... Sayfalar render ediliyor...`);

    try {
      const reader = new FileReader();
      const base64Promise = new Promise<string>((resolve, reject) => {
        reader.onload = () => {
          const res = reader.result as string;
          const b64 = res.split(',')[1] || res;
          resolve(b64);
        };
        reader.onerror = reject;
      });
      reader.readAsDataURL(file);
      const base64 = await base64Promise;

      setPdfUploadStatus(`PDF motoru çalışıyor, tüm sayfalar tek tek okunuyor...`);
      const resp = await ApiService.extractDocument({
        fileBase64: base64,
        fileName: file.name,
        fileMimeType: file.type || 'application/pdf',
        mode: 'lecture_notes',
        committeeId: committee?.id || 'donem3-kurul1',
      });

      if (resp.success && resp.note) {
        const extractedNote = resp.note;
        const newNote: LectureNote = {
          id: `note-${Date.now()}`,
          committeeId: committee?.id || 'donem3-kurul1',
          discipline: extractedNote.discipline || newDiscipline,
          title: extractedNote.title || file.name.replace(/\.[^/.]+$/, ''),
          instructor: extractedNote.instructor || undefined,
          totalSlides: extractedNote.pages?.length || 1,
          pages: extractedNote.pages || [],
          uploadedBy: currentUser?.displayName || currentUser?.email || 'Öğrenci',
          uploadedAt: new Date().toISOString(),
        };

        const updated = [newNote, ...notes];
        setNotes(updated);
        setActiveNote(newNote);
        setIsAddingNote(false);
        setPdfUploadStatus(null);
        setDriveSyncFeedback(
          `✓ "${newNote.title}" başarıyla yüklendi: Toplam ${newNote.totalSlides} sayfa eksiksiz render edildi!`
        );
        try {
          await setDoc(doc(db, 'lecture_notes', newNote.id), cleanForFirestore(newNote));
        } catch (err) {}
      } else {
        throw new Error((resp as any).error || 'Belge okunamadı');
      }
    } catch (err: any) {
      setPdfUploadStatus('Hata: ' + err.message);
    } finally {
      setIsUploadingPdf(false);
    }
  };

  // Handler for manual trigger of Drive Automation
  const handleTriggerDriveSync = async () => {
    setIsSyncingDrive(true);
    setCurrentlyRenderingSlide('Kurul 1 Drive Klasörü Taranıyor (1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W)...');
    setDriveSyncFeedback('Google Drive klasörü taranıyor...');
    try {
      const result = await runDriveSyncAndAutoMatch(
        committee?.id || 'donem3-kurul1',
        questions,
        (msg) => {
          setDriveSyncFeedback(msg);
          if (msg.includes('Render Ediliyor')) {
            setCurrentlyRenderingSlide(msg);
          }
        }
      );

      setNotes(result.syncedNotes);
      setDriveSyncFeedback(
        `Drive senkronizasyonu tamamlandı: ${result.syncedNotes.length} ders slaytı başarıyla render edildi, ${result.matchedQuestions.length} soru doğrudan ilgili slayt sayfalarıyla eşleştirildi!`
      );
      setCurrentlyRenderingSlide(null);

      // Auto update question references if any
      for (const item of result.matchedQuestions) {
        if (item.match) {
          await onUpdateQuestionReference(item.questionId, item.match);
        }
      }
    } catch (err: any) {
      setDriveSyncFeedback('Senkronizasyon hatası: ' + err.message);
      setCurrentlyRenderingSlide(null);
    } finally {
      setIsSyncingDrive(false);
    }
  };

  // Sync to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(LOCAL_NOTES_KEY, JSON.stringify(notes));
    } catch (e) {}
  }, [notes]);

  // Load from Firestore if available
  useEffect(() => {
    async function loadFirestoreNotes() {
      try {
        const colRef = collection(db, 'lecture_notes');
        const snap = await getDocs(colRef);
        if (!snap.empty) {
          const remoteNotes: LectureNote[] = [];
          snap.forEach((d) => remoteNotes.push(d.data() as LectureNote));
          if (remoteNotes.length > 0) {
            setNotes(remoteNotes);
          }
        }
      } catch (e) {
        console.warn('Firestore lecture notes fetch fallback to local', e);
      }
    }
    loadFirestoreNotes();
  }, []);

  // Clear or restore default mock slides
  const handleClearDefaultNotes = () => {
    const customOnly = notes.filter((n) => !n.id.startsWith('drive-'));
    setNotes(customOnly);
    setActiveNote(customOnly[0] || null);
    localStorage.setItem(LOCAL_NOTES_KEY, JSON.stringify(customOnly));
    setDriveSyncFeedback('✓ Varsayılan örnek slaytlar gizlendi. Yalnızca yüklediğiniz kendi ders notlarınız listelenmektedir.');
  };

  const handleResetSampleNotes = () => {
    const defaultSlides = REAL_KURUL1_DRIVE_SLIDES.map((s) => ({
      ...s,
      committeeId: committee?.id || 'donem3-kurul1',
      totalSlides: s.pages?.length || 5,
      pages: s.pages || [],
    }));
    setNotes(defaultSlides);
    setActiveNote(defaultSlides[0] || null);
    localStorage.setItem(LOCAL_NOTES_KEY, JSON.stringify(defaultSlides));
    setDriveSyncFeedback('✓ Örnek kurul slaytları geri yüklendi.');
  };

  const filteredNotes = useMemo(() => {
    return notes.filter((n) => {
      const matchesCommittee = !committee || n.committeeId === committee.id || !n.committeeId;
      const matchesDiscipline = selectedDiscipline === 'Tümü' || n.discipline === selectedDiscipline;
      const matchesSearch = !searchQuery || 
        n.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        n.discipline.toLowerCase().includes(searchQuery.toLowerCase()) ||
        n.pages.some((p) => p.content.toLowerCase().includes(searchQuery.toLowerCase()));
      return matchesCommittee && matchesDiscipline && matchesSearch;
    });
  }, [notes, committee, selectedDiscipline, searchQuery]);

  const groupedNotes = useMemo(() => {
    const groups: Record<string, LectureNote[]> = {};
    filteredNotes.forEach((n) => {
      const disc = n.discipline || 'Tıbbi Patoloji';
      if (!groups[disc]) groups[disc] = [];
      groups[disc].push(n);
    });
    return groups;
  }, [filteredNotes]);

  // Handle adding new lecture notes
  const handleSaveNewNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newRawContent.trim()) return;

    setIsSubmitting(true);
    try {
      // Split into pages by delimiter or paragraphs
      const rawPages = newRawContent
        .split(new RegExp(pageDelimiter || '--- Sayfa ---', 'i'))
        .map((p) => p.trim())
        .filter((p) => p.length > 0);

      const parsedPages = rawPages.map((text, idx) => {
        // Extract basic keywords (words > 4 chars)
        const words = text
          .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"']/g, ' ')
          .split(/\s+/)
          .filter((w) => w.length > 4)
          .slice(0, 8);
        return {
          pageNumber: idx + 1,
          content: text,
          keywords: Array.from(new Set(words)),
        };
      });

      const newNote: LectureNote = {
        id: `note-${Date.now()}`,
        committeeId: committee?.id || 'donem3-kurul2',
        discipline: newDiscipline,
        title: newTitle.trim(),
        instructor: newInstructor.trim() || undefined,
        totalSlides: parsedPages.length,
        pages: parsedPages,
        uploadedBy: currentUser?.displayName || currentUser?.email || 'Öğrenci',
        uploadedAt: new Date().toISOString(),
      };

      const updated = [newNote, ...notes];
      setNotes(updated);
      setActiveNote(newNote);
      setIsAddingNote(false);
      setNewTitle('');
      setNewInstructor('');
      setNewRawContent('');

      // Save to Firestore
      try {
        await setDoc(doc(db, 'lecture_notes', newNote.id), cleanForFirestore(newNote));
      } catch (err) {
        console.warn('Firestore setDoc lecture note error', err);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Automated Question Matcher Algorithm:
  // Scans question text, options, and fragments against all lecture note pages to pinpoint exact source page
  const findMatchesForQuestion = (q: QuestionItem) => {
    const questionText = [
      q.topic,
      ...q.fragments.map((f) => f.text),
      ...q.options.map((o) => o.text),
      q.reconstruction?.stem || '',
    ].join(' ').toLowerCase();

    const matches: { note: LectureNote; page: number; score: number; snippet: string; reasoning: string }[] = [];

    notes.forEach((note) => {
      note.pages.forEach((page) => {
        let score = 0;
        const pageLower = page.content.toLowerCase();

        // 1. Keyword overlap
        page.keywords.forEach((kw) => {
          if (questionText.includes(kw.toLowerCase())) score += 15;
        });

        // 2. Direct topic/discipline overlap
        if (q.discipline && note.discipline && q.discipline.toLowerCase() === note.discipline.toLowerCase()) {
          score += 20;
        }

        // 3. Substring matching
        const words = q.topic.split(/\s+/).filter((w) => w.length > 3);
        words.forEach((w) => {
          if (pageLower.includes(w.toLowerCase())) score += 10;
        });

        if (score >= 25) {
          // Extract matching snippet
          const snippet = page.content.length > 140 ? page.content.slice(0, 140) + '...' : page.content;
          matches.push({
            note,
            page: page.pageNumber,
            score: Math.min(98, score),
            snippet,
            reasoning: `${note.discipline} ders notlarında ilgili kavram ve bulgular tespit edildi.`,
          });
        }
      });
    });

    return matches.sort((a, b) => b.score - a.score);
  };

  return (
    <div className="space-y-6">
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-teal-800 via-teal-900 to-slate-900 rounded-2xl p-5 sm:p-6 text-white shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-black uppercase tracking-wider bg-teal-500/20 text-teal-200 border border-teal-400/30 px-2.5 py-0.5 rounded-full flex items-center gap-1.5">
              <BookMarked className="w-3.5 h-3.5" />
              Ders Notları & Slayt Veritabanı
            </span>
            <span className="text-xs text-teal-300">
              {committee?.name || 'Tüm Kurullar'}
            </span>
            <InfoPopover title="Ders Notları & Slayt Sistemi Hakkında" buttonClassName="text-teal-200 hover:text-white">
              <p>
                Tıp fakültesinde her kurulda hocaların anlattığı ders notları ve slaytlar soru çıkma potansiyeli en yüksek kaynaklardır.
              </p>
              <p className="mt-1">
                Öğrencilerin sınav sonrası hatırladığı soru parçaları bu notlarla otomatik eşleştirilir, yapay zeka bağlamı doğrular ve hangi ders notunun hangi sayfasında bilginin yer aldığını soru kartlarında gösterir.
              </p>
            </InfoPopover>
          </div>
          <h2 className="text-lg sm:text-xl font-black tracking-tight">
            Ders Notlarını Render Et & Soruları Sayfalarla Eşleştir
          </h2>
          <p className="text-xs text-teal-100/90 max-w-2xl hidden sm:block">
            Hocaların ders slaytlarını ve notlarını buraya ekleyin. Sistem notları render eder, veritabanında saklar ve her sorunun hangi ders notunun hangi sayfasından çıktığını tespit eder.
          </p>
        </div>

        <button
          onClick={() => setIsAddingNote(true)}
          className="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black px-4 py-2.5 rounded-xl text-xs sm:text-sm flex items-center gap-2 shadow-md transition-all shrink-0 cursor-pointer active:scale-95"
        >
          <Plus className="w-4 h-4" />
          <span>Yeni Not / Slayt Ekle</span>
        </button>
      </div>

      {/* Google Drive Automation Card - Only visible to Admin */}
      {isAdmin && (
        <div className="bg-gradient-to-r from-teal-50 via-cyan-50 to-emerald-50 rounded-2xl p-4 sm:p-5 border border-teal-200/90 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="bg-teal-700 text-white font-bold text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full flex items-center gap-1">
                <Cloud className="w-3 h-3 text-teal-200" />
                Drive Otomasyonu (Yönetici)
              </span>
              <span className="text-xs text-teal-900 font-semibold">
                Hafta İçi Her Gün 18:00 Senkronizasyonu
              </span>
              <InfoPopover title="Google Drive Otomasyonu Hakkında">
                <p>
                  Sistem, hafta içi her gün saat 18:00'de paylaşılan Google Drive klasörünü otomatik olarak tarar.
                </p>
                <p className="mt-1">
                  Klasöre yüklenen yeni PDF ders notları doğrudan çekilerek sayfa sayfa taranır ve öğrencilerin eklediği sorularla karşılaştırılır.
                </p>
                <p className="mt-1 font-semibold text-teal-900">
                  Hedef Klasör ID: {TARGET_DRIVE_FOLDER_ID}
                </p>
              </InfoPopover>
            </div>

            <h3 className="font-bold text-sm text-slate-900">
              Ders Notları Google Drive Klasörüyle Otomatik Eşleşiyor
            </h3>
            <p className="text-xs text-slate-600 max-w-xl">
              Drive klasörüne yüklenen PDF'ler çekilir ve soruların hangi ders notunun hangi sayfasından çıktığı otomatik tespit edilir.
            </p>

            {currentlyRenderingSlide && (
              <div className="mt-2.5 bg-amber-500/15 border border-amber-500/40 text-amber-950 p-2.5 rounded-xl flex items-center gap-2.5 animate-pulse text-xs font-semibold">
                <div className="w-3.5 h-3.5 border-2 border-amber-600 border-t-transparent rounded-full animate-spin shrink-0" />
                <span>İşlemde Olan Slayt (Render): <strong>{currentlyRenderingSlide}</strong></span>
              </div>
            )}

            {driveSyncFeedback && !currentlyRenderingSlide && (
              <div className="mt-2 text-xs font-semibold text-teal-950 bg-white/80 p-2 rounded-lg border border-teal-300 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-700 shrink-0" />
                <span>{driveSyncFeedback}</span>
              </div>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-2 shrink-0">
            <a
              href={TARGET_DRIVE_FOLDER_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-white hover:bg-slate-50 text-teal-900 font-bold px-3.5 py-2 rounded-xl text-xs flex items-center gap-1.5 border border-teal-300 shadow-2xs transition-all cursor-pointer"
            >
              <FolderOpen className="w-4 h-4 text-teal-700" />
              <span>Drive Klasörünü Aç</span>
              <ExternalLink className="w-3 h-3 text-slate-400" />
            </a>

            <button
              onClick={handleTriggerDriveSync}
              disabled={isSyncingDrive}
              className="bg-teal-700 hover:bg-teal-800 disabled:opacity-50 text-white font-bold px-4 py-2 rounded-xl text-xs flex items-center gap-2 shadow-sm transition-all cursor-pointer active:scale-95"
            >
              {isSyncingDrive ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-teal-200" />
                  <span>Slaytlar Render Ediliyor...</span>
                </>
              ) : (
                <>
                  <RefreshCw className="w-4 h-4 text-teal-200" />
                  <span>Şimdi Tara & Sorularla Eşleştir</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
          {['Tümü', 'Tıbbi Patoloji', 'Tıbbi Genetik', 'Halk Sağlığı', 'Üroloji', 'Enfeksiyon Hastalıkları'].map((disc) => (
            <button
              key={disc}
              onClick={() => setSelectedDiscipline(disc)}
              className={`px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                selectedDiscipline === disc
                  ? 'bg-teal-700 text-white shadow-2xs font-bold'
                  : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
              }`}
            >
              {disc}
            </button>
          ))}
        </div>

        <div className="w-full sm:w-64">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Ders notlarında veya sayfalarında ara..."
            className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-teal-500"
          />
        </div>
      </div>

      {/* Main Grid: Notes list and Note Reader / Question Matcher */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left column: Categorized List of uploaded Lecture Notes */}
        <div className="lg:col-span-5 space-y-3.5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <h3 className="font-bold text-sm text-slate-900 flex items-center gap-2">
              <span>Ders Slaytları ({filteredNotes.length})</span>
            </h3>

            <div className="flex items-center gap-1.5">
              {notes.some(n => n.id.startsWith('drive-')) ? (
                <button
                  onClick={handleClearDefaultNotes}
                  className="text-[10px] text-slate-500 hover:text-rose-600 bg-slate-100 hover:bg-rose-50 px-2 py-1 rounded-md border border-slate-200 transition-colors cursor-pointer"
                  title="Varsayılan örnek slaytları gizle, sadece kendi yüklediğin PDF'leri göster"
                >
                  Örnekleri Gizle
                </button>
              ) : (
                <button
                  onClick={handleResetSampleNotes}
                  className="text-[10px] text-teal-700 hover:text-teal-900 bg-teal-50 hover:bg-teal-100 px-2 py-1 rounded-md border border-teal-200 transition-colors cursor-pointer"
                  title="Varsayılan örnek slaytları geri getir"
                >
                  Örnekleri Getir
                </button>
              )}
            </div>
          </div>

          {filteredNotes.length === 0 ? (
            <div className="bg-white rounded-xl border border-slate-200 p-8 text-center space-y-2">
              <BookOpen className="w-8 h-8 text-slate-400 mx-auto" />
              <p className="text-xs font-semibold text-slate-700">Ders notu bulunamadı</p>
              <p className="text-[11px] text-slate-500">Bu kurul için henüz not veya slayt eklenmemiş.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {Object.entries(groupedNotes).map(([disciplineName, catNotes]) => {
                const isCollapsed = Boolean(collapsedCategories[disciplineName]);
                return (
                  <div key={disciplineName} className="border border-slate-200 rounded-xl bg-white overflow-hidden shadow-2xs">
                    <button
                      onClick={() => toggleCategory(disciplineName)}
                      className="w-full bg-slate-50 hover:bg-slate-100/90 px-3.5 py-2.5 flex items-center justify-between text-left transition-colors cursor-pointer border-b border-slate-100"
                    >
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-xs sm:text-sm text-slate-900">{disciplineName}</span>
                        <span className="bg-teal-100 text-teal-900 text-[10px] font-bold px-2 py-0.5 rounded-full border border-teal-200">
                          {catNotes.length} Slayt
                        </span>
                      </div>
                      <ChevronDown className={`w-4 h-4 text-slate-500 transition-transform duration-200 ${isCollapsed ? '-rotate-90' : ''}`} />
                    </button>

                    {!isCollapsed && (
                      <div className="p-3 space-y-2.5 divide-y divide-slate-100">
                        {catNotes.map((note) => {
                          const isSelected = activeNote?.id === note.id;
                          return (
                            <div
                              key={note.id}
                              onClick={() => setActiveNote(note)}
                              className={`pt-2.5 first:pt-0 rounded-lg p-2.5 transition-all cursor-pointer ${
                                isSelected
                                  ? 'bg-teal-50/50 ring-1 ring-teal-500/40'
                                  : 'hover:bg-slate-50'
                              }`}
                            >
                              <div className="flex items-start justify-between gap-2">
                                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-teal-100 text-teal-800 border border-teal-200">
                                  {note.discipline}
                                </span>
                                <span className="text-[11px] font-bold text-slate-500 flex items-center gap-1">
                                  <Layers className="w-3.5 h-3.5 text-teal-600" />
                                  {note.totalSlides} Slayt
                                </span>
                              </div>

                              <h4 className="font-bold text-xs sm:text-sm text-slate-900 mt-1.5">{note.title}</h4>

                              {note.instructor && (
                                <p className="text-[11px] text-slate-600 mt-1 flex items-center gap-1">
                                  <User className="w-3 h-3 text-slate-400" />
                                  {note.instructor}
                                </p>
                              )}

                              <div className="mt-2.5 pt-2 border-t border-slate-100 flex items-center justify-between gap-2 text-[11px]">
                                <div className="flex items-center gap-2">
                                  {note.driveFileUrl && (
                                    <a
                                      href={note.driveFileUrl}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      onClick={(e) => e.stopPropagation()}
                                      className="text-[10px] font-bold text-teal-800 hover:text-teal-950 flex items-center gap-1 bg-teal-50 hover:bg-teal-100 border border-teal-200 px-2 py-0.5 rounded shadow-2xs"
                                    >
                                      <ExternalLink className="w-2.5 h-2.5 text-teal-600" />
                                      <span>Drive</span>
                                    </a>
                                  )}
                                </div>

                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    setReaderNote(note);
                                  }}
                                  className="bg-teal-700 hover:bg-teal-800 text-white font-bold text-xs px-2.5 py-1 rounded-lg flex items-center gap-1 shadow-2xs cursor-pointer transition-all active:scale-95"
                                >
                                  <BookOpen className="w-3 h-3 text-teal-200" />
                                  <span>Slaytları Oku</span>
                                </button>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {/* Quick Match Tool Card */}
          <div className="bg-gradient-to-br from-amber-50 to-teal-50 rounded-2xl border border-amber-200 p-5 mt-6 shadow-xs">
            <h4 className="font-bold text-sm text-slate-900 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-amber-600" />
              Soruları Ders Notlarıyla Otomatik Eşleştir
            </h4>
            <p className="text-xs text-slate-600 mt-1">
              Kurul havuzundaki soruların metinlerini ve şıklarını yüklenen slaytlarla karşılaştırarak hangi soru hangi sayfadan geldiğini tespit eder.
            </p>

            <div className="mt-4 space-y-2">
              <label className="text-xs font-semibold text-slate-700 block">Eşleştirilecek Soruyu Seçin:</label>
              <select
                value={matchingQuestionId || ''}
                onChange={(e) => setMatchingQuestionId(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300 bg-white focus:outline-none focus:ring-2 focus:ring-teal-500"
              >
                <option value="">-- Soru Seçiniz --</option>
                {questions.map((q) => (
                  <option key={q.id} value={q.id}>
                    #{q.questionNumber} ({q.discipline}) - {q.topic.slice(0, 35)}...
                  </option>
                ))}
              </select>

              {matchingQuestionId && (
                <div className="mt-3 space-y-2 pt-2 border-t border-amber-200/60">
                  {(() => {
                    const targetQ = questions.find((q) => q.id === matchingQuestionId);
                    if (!targetQ) return null;
                    const matches = findMatchesForQuestion(targetQ);

                    if (matches.length === 0) {
                      return (
                        <p className="text-xs text-slate-500 italic">
                          Bu soru için yüklenen notlarda henüz net bir sayfa eşleşmesi bulunamadı. Daha fazla ders notu ekleyebilirsiniz.
                        </p>
                      );
                    }

                    return (
                      <div className="space-y-2">
                        <span className="text-[11px] font-bold text-emerald-800 uppercase block">
                          Tespit Edilen Ders Notu Sayfaları:
                        </span>
                        {matches.slice(0, 2).map((m, i) => (
                          <div key={i} className="bg-white rounded-lg p-2.5 border border-emerald-300 text-xs space-y-1">
                            <div className="flex items-center justify-between">
                              <span className="font-bold text-slate-900">{m.note.title}</span>
                              <span className="bg-emerald-100 text-emerald-900 font-bold px-1.5 py-0.5 rounded text-[10px]">
                                Sayfa {m.page} (%{m.score} Uyumluluk)
                              </span>
                            </div>
                            <p className="text-[11px] text-slate-600 line-clamp-2 italic">
                              "{m.snippet}"
                            </p>
                            <button
                              onClick={async () => {
                                await onUpdateQuestionReference(targetQ.id, {
                                  noteId: m.note.id,
                                  noteTitle: m.note.title,
                                  discipline: m.note.discipline,
                                  pageNumber: m.page,
                                  matchedSnippet: m.snippet,
                                  confidenceScore: m.score,
                                  reasoning: m.reasoning,
                                });
                              }}
                              className="w-full mt-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-1 px-2 rounded text-[11px] flex items-center justify-center gap-1 cursor-pointer transition-colors"
                            >
                              <CheckCircle2 className="w-3.5 h-3.5" />
                              <span>Bu Sayfayı Soru #{targetQ.questionNumber}'e Kaydet</span>
                            </button>
                          </div>
                        ))}
                      </div>
                    );
                  })()}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right column: Rendered Note Reader */}
        <div className="lg:col-span-7">
          {activeNote ? (
            <div className="bg-white rounded-2xl border border-slate-200 p-5 sm:p-6 shadow-xs space-y-5">
              <div className="border-b border-slate-100 pb-4 space-y-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-teal-100 text-teal-800 border border-teal-200">
                    {activeNote.discipline}
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-500 font-medium">
                      Toplam {activeNote.totalSlides} Sayfa Eksiksiz Render Edildi
                    </span>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h3 className="text-lg sm:text-xl font-black text-slate-900">{activeNote.title}</h3>
                    {activeNote.instructor && (
                      <p className="text-xs text-slate-600 mt-0.5">Öğretim Üyesi: {activeNote.instructor}</p>
                    )}
                  </div>

                  <div className="flex flex-wrap items-center gap-1.5 shrink-0">
                    {/* Export Text Dropdown/Buttons */}
                    <button
                      onClick={() => exportNoteText(activeNote, 'txt')}
                      title="Slayt metnini .txt olarak kaydet"
                      className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold transition-all cursor-pointer"
                    >
                      <Download className="w-3.5 h-3.5 text-slate-600" />
                      <span>TXT İndir</span>
                    </button>

                    <button
                      onClick={() => exportNoteText(activeNote, 'md')}
                      title="Slayt metnini Markdown olarak kaydet"
                      className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold transition-all cursor-pointer"
                    >
                      <FileText className="w-3.5 h-3.5 text-slate-600" />
                      <span>MD İndir</span>
                    </button>

                    <button
                      onClick={() => exportNoteText(activeNote, 'copy')}
                      title="Tüm slayt metnini kopyala"
                      className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 text-xs font-bold transition-all cursor-pointer"
                    >
                      <Copy className="w-3.5 h-3.5 text-teal-600" />
                      <span>Tümünü Kopyala</span>
                    </button>

                    {activeNote.driveFileUrl && (
                      <a
                        href={activeNote.driveFileUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-teal-700 hover:bg-teal-800 text-white text-xs font-bold transition-all cursor-pointer"
                      >
                        <ExternalLink className="w-3.5 h-3.5 text-teal-200" />
                        <span>Drive'da Aç</span>
                      </a>
                    )}
                  </div>
                </div>

                {/* Export Feedback Alert */}
                {exportFeedback && (
                  <div className="bg-emerald-50 border border-emerald-300 text-emerald-950 p-2.5 rounded-xl text-xs font-semibold flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                    <span>{exportFeedback}</span>
                  </div>
                )}

                {/* Search within slide deck */}
                <div className="relative pt-1">
                  <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    value={slideSearchQuery}
                    onChange={(e) => setSlideSearchQuery(e.target.value)}
                    placeholder={`"${activeNote.title}" içinde ara (konu, terim, ilaç veya sayfa no)...`}
                    className="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:bg-white"
                  />
                </div>
              </div>

              {/* Rendered Slide Pages */}
              <div className="space-y-4">
                {activeNote.pages
                  .filter((page) => {
                    if (!slideSearchQuery.trim()) return true;
                    const q = slideSearchQuery.toLowerCase();
                    return (
                      page.content.toLowerCase().includes(q) ||
                      `sayfa ${page.pageNumber}`.includes(q) ||
                      (page.keywords && page.keywords.some((kw) => kw.toLowerCase().includes(q)))
                    );
                  })
                  .map((page) => (
                    <div
                      key={page.pageNumber}
                      className="bg-slate-50/70 border border-slate-200 rounded-xl p-4.5 space-y-2.5 transition-all hover:bg-white hover:shadow-xs"
                    >
                      <div className="flex items-center justify-between">
                        <span className="bg-slate-900 text-white text-[11px] font-black px-2.5 py-0.5 rounded-md flex items-center gap-1">
                          <FileText className="w-3 h-3 text-teal-400" />
                          Sayfa {page.pageNumber} / {activeNote.totalSlides}
                        </span>

                        <button
                          onClick={() => copyPageContent(page.pageNumber, page.content)}
                          className="text-[10px] text-slate-600 hover:text-teal-700 bg-white hover:bg-teal-50 border border-slate-200 px-2 py-0.5 rounded flex items-center gap-1 cursor-pointer transition-colors"
                        >
                          {copyPageSuccess[page.pageNumber] ? (
                            <>
                              <Check className="w-3 h-3 text-emerald-600" />
                              <span className="text-emerald-700 font-bold">Kopyalandı!</span>
                            </>
                          ) : (
                            <>
                              <Copy className="w-3 h-3 text-slate-400" />
                              <span>Sayfayı Kopyala</span>
                            </>
                          )}
                        </button>
                      </div>

                      <div className="text-xs text-slate-800 whitespace-pre-line leading-relaxed font-sans font-medium">
                        {page.content}
                      </div>

                      {page.keywords && page.keywords.length > 0 && (
                        <div className="pt-2 border-t border-slate-200/60 flex flex-wrap items-center gap-1">
                          <span className="text-[10px] text-slate-500 font-bold mr-1">Anahtar Kelimeler:</span>
                          {page.keywords.map((kw, i) => (
                            <span
                              key={i}
                              className="bg-white border border-slate-200 text-slate-700 text-[10px] px-2 py-0.5 rounded"
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
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3 shadow-xs">
              <BookMarked className="w-12 h-12 text-teal-600 mx-auto" />
              <h4 className="font-bold text-base text-slate-900">Ders Notu Görüntüleyici</h4>
              <p className="text-xs text-slate-500 max-w-md mx-auto">
                Sol taraftaki listeden bir ders notu seçin ya da yukarıdaki butona tıklayarak döneminize ait yeni bir slayt veya ders notu ekleyin.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Modal: Add New Lecture Note */}
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
                onClick={() => setAddMode('upload')}
                className={`flex-1 py-2 text-center border-b-2 cursor-pointer transition-colors ${
                  addMode === 'upload'
                    ? 'border-teal-700 text-teal-900 bg-teal-50/50'
                    : 'border-transparent text-slate-500 hover:text-slate-800'
                }`}
              >
                📄 PDF / DOCX Slayt Dosyası Yükle
              </button>
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
                      Sistem 200 sayfaya kadar olan tüm slaytları tek tek tarar, her sayfayı eksiksiz ve yorumsuz olarak doğrudan slayt içindeki metinle birebir aktarır.
                    </p>
                  </div>
                  <label className="inline-flex items-center gap-2 bg-teal-700 hover:bg-teal-800 text-white font-bold px-4 py-2 rounded-lg cursor-pointer transition-all shadow-xs">
                    <FileUp className="w-4 h-4 text-teal-200" />
                    <span>Dosya Seç (.pdf, .docx)</span>
                    <input
                      type="file"
                      accept=".pdf,.docx,.doc"
                      onChange={handlePdfFileUpload}
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
              <form onSubmit={handleSaveNewNote} className="space-y-4 text-xs">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Ders / Anabilim Dalı</label>
                  <select
                    value={newDiscipline}
                    onChange={(e) => setNewDiscipline(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300 bg-white"
                  >
                    <option value="Tıbbi Patoloji">Tıbbi Patoloji</option>
                    <option value="Tıbbi Mikrobiyoloji">Tıbbi Mikrobiyoloji</option>
                    <option value="Tıbbi Farmakoloji">Tıbbi Farmakoloji</option>
                    <option value="Tıbbi Biyokimya">Tıbbi Biyokimya</option>
                    <option value="İç Hastalıkları (Dahiliye)">İç Hastalıkları (Dahiliye)</option>
                    <option value="Genel Cerrahi">Genel Cerrahi</option>
                    <option value="Tıbbi Genetik">Tıbbi Genetik</option>
                    <option value="Halk Sağlığı">Halk Sağlığı</option>
                    <option value="Üroloji">Üroloji</option>
                  </select>
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Ders / Slayt Başlığı</label>
                  <input
                    type="text"
                    required
                    placeholder="Ör: Farmakoloji - Sempatomimetikler ve Adrenerjik Reseptörler"
                    value={newTitle}
                    onChange={(e) => setNewTitle(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-slate-300"
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Öğretim Üyesi (İsteğe bağlı)</label>
                  <input
                    type="text"
                    placeholder="Ör: Prof. Dr. ..."
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
                    İpucu: Slaytları ayırmak için aralarına <code>--- Sayfa ---</code> yazın. Sayfalar otomatik olarak numaralandırılacak ve soru eşleştirmelerinde kullanılacaktır.
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

      {/* Interactive Slide Reader Modal */}
      <SlideReaderModal
        isOpen={Boolean(readerNote)}
        note={readerNote}
        onClose={() => setReaderNote(null)}
      />
    </div>
  );
};
