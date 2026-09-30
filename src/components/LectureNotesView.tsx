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
  FolderOpen
} from 'lucide-react';
import { LectureNote, QuestionItem, Committee, QuestionLectureMatch } from '../types';
import { AppUser } from '../services/auth';
import { getFirestore, collection, getDocs, doc, setDoc, deleteDoc } from 'firebase/firestore';
import { db, cleanForFirestore } from '../services/firestoreDb';
import { InfoPopover } from './InfoPopover';
import { 
  TARGET_DRIVE_FOLDER_ID, 
  TARGET_DRIVE_FOLDER_URL, 
  getAutomationStatus, 
  runDriveSyncAndAutoMatch 
} from '../services/driveAutomation';

interface LectureNotesViewProps {
  committee: Committee | undefined;
  committees: Committee[];
  questions: QuestionItem[];
  currentUser: AppUser | null;
  isAdmin: boolean;
  onUpdateQuestionReference: (questionId: string, reference: QuestionLectureMatch) => Promise<void>;
}

const LOCAL_NOTES_KEY = 'medsoru_lecture_notes_v1';

// Initial pre-seeded clinical lecture notes for Dönem 3
const INITIAL_LECTURE_NOTES: LectureNote[] = [
  {
    id: 'note-pat-1',
    committeeId: 'donem3-kurul2',
    discipline: 'Tıbbi Patoloji',
    title: 'Hücre Hasarı, İskemi ve Nekroz Çeşitleri',
    instructor: 'Prof. Dr. M. Eren (Patoloji AD)',
    totalSlides: 3,
    uploadedAt: new Date(Date.now() - 86400000 * 3).toISOString(),
    pages: [
      {
        pageNumber: 1,
        content: 'İskemik doku hasarında erken dönem değişiklikleri: Oksijen azlığı -> ATP sentezi durur -> Na+/K+ ATPaz pompası iflas eder -> Hücre içi sodyum ve su birikimi (hidropik dejenerasyon), kalsiyum akışı ve mitokondri membran geçirgenliği artar.',
        keywords: ['iskemi', 'ATP', 'kalsiyum', 'hidropik dejenerasyon', 'hücre hasarı']
      },
      {
        pageNumber: 2,
        content: 'Nekroz Tipleri ve Histopatolojik Özellikleri:\n1. Koagülasyon Nekrozu: En sık görülen tip (beyin hariç tüm solid organ enfarktüsleri). Hücre sınırları (hayalet hücreler - tombstone) birkaç gün korunur. Asidofili artışı ve piknoz görülür.\n2. Likefaksiyon Nekrozu: Beyin enfarktüsleri ve bakteriyel/mantar abselerinde görülür.',
        keywords: ['koagülasyon nekrozu', 'likefaksiyon', 'hayalet hücre', 'tombstone', 'asidofili', 'nekroz']
      },
      {
        pageNumber: 3,
        content: 'Miyokard Enfarktüsü Zaman Çizelgesi ve Histopatoloji:\n• 0-30 dakika: Işık mikroskobunda belirgin değişiklik yok.\n• 4-12 saat: Dalgalı lifler (wavy fibers), ödem, erken koagülasyon nekrozu.\n• 1-3 gün: Belirgin koagülasyon nekrozu, nükleus kaybı ve yoğun nötrofil infiltrasyonu (sarı-kahverengi yumuşama).\n• 4-7 gün: Makrofaj fagositozu, granülasyon dokusu başlangıcı.\n• 1-2 hafta: Granülasyon dokusu, neovaskülarizasyon.\n• >2 ay: Yoğun kollajen fibröz skar.',
        keywords: ['miyokard enfarktüsü', 'koagülasyon nekrozu', 'nötrofil', 'dalgalı lifler', 'wavy fibers', 'makrofaj', 'granülasyon', 'skar']
      }
    ]
  },
  {
    id: 'note-mikro-1',
    committeeId: 'donem3-kurul2',
    discipline: 'Tıbbi Mikrobiyoloji',
    title: 'Solunum Yolu Enfeksiyonları ve Atipik Pnömoniler',
    instructor: 'Doç. Dr. S. Yılmaz (Mikrobiyoloji AD)',
    totalSlides: 2,
    uploadedAt: new Date(Date.now() - 86400000 * 2).toISOString(),
    pages: [
      {
        pageNumber: 1,
        content: 'Atipik Pnömoni Etkenleri:\n• Mycoplasma pneumoniae (hücre duvarı yok, soğuk aglütinin pozitifliği, genç erişkinler).\n• Chlamydia pneumoniae (intrasellüler, inklüzyon cisimcikleri).\n• Legionella pneumophila: Su sistemleri, klima kuleleri, termal kaplıcalardan bulaşır. Yaşlı ve immünsüprese bireylerde ağır pnömoni ve ekstrapulmoner bulgular (konfüzyon, ishal, hiponatremi) ile seyreder.',
        keywords: ['atipik pnömoni', 'Legionella pneumophila', 'Mycoplasma', 'soğuk aglütinin', 'klima', 'su kuleleri', 'hiponatremi']
      },
      {
        pageNumber: 2,
        content: 'Legionella pneumophila Laboratuvar Tanısı:\nGram boyamada zor görünür (zayıf boyanır). Kültür için zenginleştirilmiş BCYE (Buffered Charcoal Yeast Extract) agar gerekir (demir ve L-sistein esastır). Hızlı tanı: İdrar antijen testi (Legionella serogrup 1). Tedavi: Makrolidler (azitromisin) veya florokinolonlar (levofloksasin).',
        keywords: ['Legionella', 'BCYE agar', 'L-sistein', 'idrar antijen testi', 'azitromisin', 'levofloksasin']
      }
    ]
  }
];

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
      if (stored) return JSON.parse(stored);
    } catch (e) {}
    return INITIAL_LECTURE_NOTES;
  });

  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('Tümü');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeNote, setActiveNote] = useState<LectureNote | null>(null);

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

  // Google Drive Automation State
  const [isSyncingDrive, setIsSyncingDrive] = useState(false);
  const [driveSyncFeedback, setDriveSyncFeedback] = useState<string | null>(null);

  // Handler for manual trigger of Drive Automation
  const handleTriggerDriveSync = async () => {
    setIsSyncingDrive(true);
    setDriveSyncFeedback('Google Drive klasörü (1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W) taranıyor...');
    try {
      const result = await runDriveSyncAndAutoMatch(
        committee?.id || 'donem3-kurul2',
        questions,
        notes,
        (msg) => setDriveSyncFeedback(msg)
      );

      setNotes(result.newNotes);
      setDriveSyncFeedback(
        `Drive senkronizasyonu tamamlandı: ${result.newNotes.length} ders notu güncellendi, ${result.matchedQuestionsCount} soru doğrudan ilgili slayt sayfalarıyla eşleştirildi!`
      );

      // Auto update question references if any
      for (const updatedQ of result.updatedQuestions) {
        if (updatedQ.lectureReference) {
          await onUpdateQuestionReference(updatedQ.id, updatedQ.lectureReference);
        }
      }
    } catch (err: any) {
      setDriveSyncFeedback('Senkronizasyon hatası: ' + err.message);
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

      {/* Google Drive Automation Card */}
      <div className="bg-gradient-to-r from-teal-50 via-cyan-50 to-emerald-50 rounded-2xl p-4 sm:p-5 border border-teal-200/90 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="bg-teal-700 text-white font-bold text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full flex items-center gap-1">
              <Cloud className="w-3 h-3 text-teal-200" />
              Drive Otomasyonu
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

          {driveSyncFeedback && (
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
                <span>Senkronize Ediliyor...</span>
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

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          {['Tümü', 'Tıbbi Patoloji', 'Tıbbi Mikrobiyoloji', 'Tıbbi Farmakoloji', 'Tıbbi Biyokimya'].map((disc) => (
            <button
              key={disc}
              onClick={() => setSelectedDiscipline(disc)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                selectedDiscipline === disc
                  ? 'bg-teal-700 text-white shadow-2xs'
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
        {/* Left column: List of uploaded Lecture Notes */}
        <div className="lg:col-span-5 space-y-3">
          <h3 className="font-bold text-sm text-slate-900 flex items-center justify-between">
            <span>Yüklenen Ders Notları ({filteredNotes.length})</span>
            <span className="text-xs text-slate-500 font-normal">Görüntülemek için seçin</span>
          </h3>

          {filteredNotes.length === 0 ? (
            <div className="bg-white rounded-xl border border-slate-200 p-8 text-center space-y-2">
              <BookOpen className="w-8 h-8 text-slate-400 mx-auto" />
              <p className="text-xs font-semibold text-slate-700">Ders notu bulunamadı</p>
              <p className="text-[11px] text-slate-500">Bu kurul için henüz not veya slayt eklenmemiş.</p>
            </div>
          ) : (
            filteredNotes.map((note) => {
              const isSelected = activeNote?.id === note.id;
              return (
                <div
                  key={note.id}
                  onClick={() => setActiveNote(note)}
                  className={`bg-white rounded-xl border p-4 transition-all cursor-pointer shadow-xs ${
                    isSelected
                      ? 'border-teal-500 ring-2 ring-teal-500/20 bg-teal-50/20'
                      : 'border-slate-200 hover:border-teal-300 hover:shadow-sm'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-teal-100 text-teal-800 border border-teal-200">
                      {note.discipline}
                    </span>
                    <span className="text-[11px] font-bold text-slate-500 flex items-center gap-1">
                      <Layers className="w-3.5 h-3.5 text-teal-600" />
                      {note.totalSlides} Sayfa / Slayt
                    </span>
                  </div>

                  <h4 className="font-bold text-sm text-slate-900 mt-2">{note.title}</h4>

                  {note.instructor && (
                    <p className="text-xs text-slate-600 mt-1 flex items-center gap-1">
                      <User className="w-3 h-3 text-slate-400" />
                      {note.instructor}
                    </p>
                  )}

                  <div className="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                    <span>Yükleyen: {note.uploadedBy || 'Öğrenci'}</span>
                    <span className="text-teal-700 font-semibold flex items-center gap-1">
                      Sayfaları Oku <ChevronRight className="w-3.5 h-3.5" />
                    </span>
                  </div>
                </div>
              );
            })
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
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-6">
              <div className="border-b border-slate-100 pb-4">
                <div className="flex items-center justify-between gap-3">
                  <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-teal-100 text-teal-800 border border-teal-200">
                    {activeNote.discipline}
                  </span>
                  <span className="text-xs text-slate-500 font-medium">
                    Toplam {activeNote.totalSlides} Sayfa / Slayt Render Edildi
                  </span>
                </div>
                <h3 className="text-xl font-black text-slate-900 mt-2">{activeNote.title}</h3>
                {activeNote.instructor && (
                  <p className="text-xs text-slate-600 mt-1">Öğretim Üyesi: {activeNote.instructor}</p>
                )}
              </div>

              {/* Rendered Slide Pages */}
              <div className="space-y-4">
                {activeNote.pages.map((page) => (
                  <div
                    key={page.pageNumber}
                    className="bg-slate-50/70 border border-slate-200 rounded-xl p-4.5 space-y-2.5 transition-all hover:bg-white hover:shadow-xs"
                  >
                    <div className="flex items-center justify-between">
                      <span className="bg-slate-900 text-white text-[11px] font-black px-2.5 py-0.5 rounded-md flex items-center gap-1">
                        <FileText className="w-3 h-3 text-teal-400" />
                        Sayfa {page.pageNumber}
                      </span>
                      <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">
                        Slayt Metni
                      </span>
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
                className="text-slate-400 hover:text-slate-600 text-xs px-2 py-1"
              >
                Kapat
              </button>
            </div>

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
                  className="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-50"
                >
                  İptal
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-5 py-2 rounded-lg bg-teal-700 hover:bg-teal-800 text-white font-bold flex items-center gap-1.5 shadow-sm"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>{isSubmitting ? 'Kaydediliyor...' : 'Ders Notunu Render Et & Kaydet'}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
