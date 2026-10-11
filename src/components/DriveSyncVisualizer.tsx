import React, { useState, useEffect } from 'react';
import {
  FolderDown,
  CheckCircle2,
  Clock,
  RefreshCw,
  FileText,
  Search,
  HardDrive,
  ChevronDown,
  ChevronUp,
  Cpu,
} from 'lucide-react';

interface DriveFileStatusSummary {
  totalExamsDownloaded: number;
  totalExamsTarget: number;
  examsProgressPercent: number;
  totalLecturesDownloaded: number;
  totalLecturesTarget: number;
  lecturesProgressPercent: number;
  totalParsedQuestions: number;
  databaseDir: string;
}

interface LectureSlideItem {
  title: string;
  folderName: string;
  fileId: string;
  isDownloaded: boolean;
  isExtracted: boolean;
  sizeMb: string;
  localName: string;
}

interface ExamFileItem {
  name: string;
  sizeMb: string;
  modifiedAt: string;
  status: 'extracted' | 'downloaded';
  type: string;
}

export const DriveSyncVisualizer: React.FC<{
  onSelectLecture?: (title: string, fileId?: string) => void;
  className?: string;
}> = ({ onSelectLecture, className = '' }) => {
  const [summary, setSummary] = useState<DriveFileStatusSummary | null>(null);
  const [lectures, setLectures] = useState<LectureSlideItem[]>([]);
  const [exams, setExams] = useState<ExamFileItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('all');
  const [activeTab, setActiveTab] = useState<'lectures' | 'exams'>('lectures');
  const [isExpanded, setIsExpanded] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<string>('');

  const fetchStatus = async () => {
    setIsLoading(true);
    try {
      const res = await fetch('/api/automation/drive-files-status');
      if (res.ok) {
        const data = await res.json();
        setSummary(data.summary);
        setLectures(data.lectures || []);
        setExams(data.exams || []);
        setLastUpdated(new Date().toLocaleTimeString('tr-TR'));
      }
    } catch (e) {
      console.warn('drive-files-status fetch err:', e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    // Otomatik olarak her 5 saniyede bir durumu güncelle (indirme takibi için)
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const disciplines = Array.from(new Set(lectures.map((l) => l.folderName).filter(Boolean)));

  const filteredLectures = lectures.filter((l) => {
    const matchesSearch = 
      !searchQuery || 
      l.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      l.folderName.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDisc = selectedDiscipline === 'all' || l.folderName === selectedDiscipline;
    return matchesSearch && matchesDisc;
  });

  const filteredExams = exams.filter((e) => 
    !searchQuery || e.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className={`bg-white border border-line rounded-2xl shadow-xs overflow-hidden ${className}`}>
      {/* Header Bar */}
      <div className="bg-ink-surface text-white p-4 sm:p-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-ok animate-pulse" />
              <span className="text-2xs font-bold text-ok uppercase tracking-wider">
                Google Drive & Yerel Bilgisayar Arşiv İzleyici
              </span>
            </div>
            <h3 className="text-base sm:text-lg font-black text-white flex items-center gap-2">
              <HardDrive className="w-5 h-5 text-ok" />
              <span>Yerel Disk & PDF İndirme Durumu</span>
            </h3>
            <p className="text-xs text-ink-3">
              Hedef klasör: <code className="bg-ink text-ok px-1.5 py-0.5 rounded font-mono text-2xs">{summary?.databaseDir || 'C:\\Users\\indui\\Desktop\\meds_database'}</code>
            </p>
          </div>

          <div className="flex items-center gap-2 self-start sm:self-auto shrink-0">
            <button
              onClick={fetchStatus}
              disabled={isLoading}
              className="bg-ok/60 hover:bg-ok text-ok-soft border border-ok/50 font-semibold px-3 py-1.5 rounded-xl text-xs flex items-center gap-1.5 transition-all cursor-pointer active:scale-95"
              title="Durumu yenile"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin text-ok' : ''}`} />
              <span>{isLoading ? 'Kontrol...' : 'Yenile'}</span>
            </button>

            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="bg-ink hover:bg-ink-2 text-ink-3 font-semibold p-1.5 rounded-xl text-xs transition-colors cursor-pointer"
              title={isExpanded ? 'Paneli Daralt' : 'Paneli Genişlet'}
            >
              {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Live Progress Metrics Cards */}
        {summary && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4 pt-4 border-t border-line-2/80">
            {/* 1. Ders Slaytları İlerlemesi */}
            <div className="bg-ink/60 border border-line-2/60 rounded-xl p-3 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-ink-3 flex items-center gap-1.5">
                  <FileText className="w-3.5 h-3.5 text-ok" />
                  Ders Notları & Slaytlar
                </span>
                <span className="font-black text-ok font-mono">
                  {summary.totalLecturesDownloaded} / {summary.totalLecturesTarget}
                </span>
              </div>
              <div className="w-full bg-ink rounded-full h-2 overflow-hidden">
                <div 
                  className="bg-accent h-full rounded-full transition-all duration-500"
                  style={{ width: `${summary.lecturesProgressPercent}%` }}
                />
              </div>
              <div className="flex justify-between text-2xs text-ink-3 font-medium">
                <span>{summary.lecturesProgressPercent}% Tamamlandı</span>
                <span>{summary.totalLecturesDownloaded === summary.totalLecturesTarget ? '✅ Hepsi Hazır' : '⏳ İndiriliyor...'}</span>
              </div>
            </div>

            {/* 2. Çıkmış Sınavlar İlerlemesi */}
            <div className="bg-ink/60 border border-line-2/60 rounded-xl p-3 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-ink-3 flex items-center gap-1.5">
                  <FolderDown className="w-3.5 h-3.5 text-warn" />
                  Çıkmış Sınav PDF'leri
                </span>
                <span className="font-black text-warn font-mono">
                  {summary.totalExamsDownloaded} / {summary.totalExamsTarget}
                </span>
              </div>
              <div className="w-full bg-ink rounded-full h-2 overflow-hidden">
                <div 
                  className="bg-accent h-full rounded-full transition-all duration-500"
                  style={{ width: `${summary.examsProgressPercent}%` }}
                />
              </div>
              <div className="flex justify-between text-2xs text-ink-3 font-medium">
                <span>{summary.examsProgressPercent}% Tamamlandı</span>
                <span>{summary.totalExamsDownloaded >= summary.totalExamsTarget ? '✅ Arşiv Tam' : '⏳ Sürüyor...'}</span>
              </div>
            </div>

            {/* 3. Yerel Soru Ayrıştırma & OCR */}
            <div className="bg-ink/60 border border-line-2/60 rounded-xl p-3 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-ink-3 flex items-center gap-1.5">
                  <Cpu className="w-3.5 h-3.5 text-ok" />
                  Çıkarılan Çıkmış Sorular
                </span>
                <span className="font-black text-white font-mono">
                  {summary.totalParsedQuestions.toLocaleString('tr-TR')} Soru
                </span>
              </div>
              <div className="text-2xs text-ok/90 font-medium flex items-center gap-1 pt-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-ok shrink-0" />
                <span>CPU ile birebir (saf metin) olarak veritabanına aktarıldı</span>
              </div>
              <div className="text-2xs text-ink-3">Son güncelleme: {lastUpdated}</div>
            </div>
          </div>
        )}
      </div>

      {/* Collapsible Content */}
      {isExpanded && (
        <div className="p-4 sm:p-5 space-y-4">
          {/* Navigation & Search Filters */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-line pb-4">
            <div className="flex items-center gap-2">
              <button
                onClick={() => setActiveTab('lectures')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  activeTab === 'lectures'
                    ? 'bg-ok text-white shadow-2xs'
                    : 'bg-field text-ink-2 hover:bg-line'
                }`}
              >
                📚 Ders Notları ({lectures.length})
              </button>
              <button
                onClick={() => setActiveTab('exams')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  activeTab === 'exams'
                    ? 'bg-ok text-white shadow-2xs'
                    : 'bg-field text-ink-2 hover:bg-line'
                }`}
              >
                📝 Çıkmış Sınavlar ({exams.length})
              </button>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              {activeTab === 'lectures' && disciplines.length > 0 && (
                <select
                  value={selectedDiscipline}
                  onChange={(e) => setSelectedDiscipline(e.target.value)}
                  className="text-xs bg-field border border-line rounded-lg px-2.5 py-1.5 text-ink-2 font-semibold focus:outline-none"
                >
                  <option value="all">Tüm Branşlar</option>
                  {disciplines.map((d) => (
                    <option key={d} value={d}>{d}</option>
                  ))}
                </select>
              )}

              <div className="relative flex-1 sm:w-64">
                <Search className="w-3.5 h-3.5 text-ink-3 absolute left-2.5 top-2.5" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Ders veya dosya adı ara..."
                  className="w-full text-xs pl-8 pr-3 py-1.5 bg-field border border-line rounded-lg text-ink focus:bg-white focus:outline-none focus:ring-1 focus:ring-ok"
                />
              </div>
            </div>
          </div>

          {/* Table / List */}
          {activeTab === 'lectures' ? (
            <div className="border border-line rounded-xl overflow-hidden shadow-2xs">
              <div className="max-h-72 overflow-y-auto">
                <table className="w-full text-left border-collapse text-xs">
                  <thead className="sticky top-0 bg-field border-b border-line text-ink-2 font-bold uppercase text-2xs tracking-wider z-10">
                    <tr>
                      <th className="py-2.5 px-3">Ders Slayt Başlığı</th>
                      <th className="py-2.5 px-3">Branş</th>
                      <th className="py-2.5 px-3">Boyut</th>
                      <th className="py-2.5 px-3">Yerel Disk Durumu</th>
                      <th className="py-2.5 px-3 text-right">İşlem</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-line">
                    {filteredLectures.length === 0 ? (
                      <tr>
                        <td colSpan={5} className="py-6 text-center text-ink-3">
                          Arama kriterine uygun ders bulunamadı.
                        </td>
                      </tr>
                    ) : (
                      filteredLectures.map((l, idx) => (
                        <tr key={l.fileId || idx} className="hover:bg-field/80 transition-colors">
                          <td className="py-2 px-3 font-semibold text-ink">
                            <span className="block leading-snug">{l.title}</span>
                            <span className="text-2xs text-ink-3 font-mono block">Dosya: {l.localName}</span>
                          </td>
                          <td className="py-2 px-3 text-ink-2">
                            <span className="bg-field text-ink-2 px-2 py-0.5 rounded text-2xs font-semibold">
                              {l.folderName}
                            </span>
                          </td>
                          <td className="py-2 px-3 text-ink-3 font-mono text-2xs">
                            {l.isDownloaded ? `${l.sizeMb} MB` : '-'}
                          </td>
                          <td className="py-2 px-3">
                            {l.isDownloaded ? (
                              <span className="inline-flex items-center gap-1 text-ok bg-ok-soft border border-ok/30 px-2 py-0.5 rounded text-2xs font-bold">
                                <CheckCircle2 className="w-3 h-3 text-ok" />
                                <span>İndirildi (Bilgisayarda Mevcut)</span>
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1 text-warn bg-warn-soft border border-warn/30 px-2 py-0.5 rounded text-2xs font-bold">
                                <Clock className="w-3 h-3 text-warn animate-spin" />
                                <span>Drive'dan İndiriliyor...</span>
                              </span>
                            )}
                          </td>
                          <td className="py-2 px-3 text-right">
                            <button
                              onClick={() => onSelectLecture && onSelectLecture(l.title, l.fileId)}
                              className={`text-xs font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors ${
                                l.isDownloaded
                                  ? 'bg-ok hover:bg-ok text-white'
                                  : 'bg-field hover:bg-line text-ink-2'
                              }`}
                            >
                              {l.isDownloaded ? 'Dersi Oku' : 'İndir & Oku'}
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          ) : (
            <div className="border border-line rounded-xl overflow-hidden shadow-2xs">
              <div className="max-h-72 overflow-y-auto">
                <table className="w-full text-left border-collapse text-xs">
                  <thead className="sticky top-0 bg-field border-b border-line text-ink-2 font-bold uppercase text-2xs tracking-wider z-10">
                    <tr>
                      <th className="py-2.5 px-3">Çıkmış Sınav Dosyası</th>
                      <th className="py-2.5 px-3">Boyut</th>
                      <th className="py-2.5 px-3">Yerel Durum</th>
                      <th className="py-2.5 px-3 text-right">Metin Çıkarımı</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-line">
                    {filteredExams.length === 0 ? (
                      <tr>
                        <td colSpan={4} className="py-6 text-center text-ink-3">
                          Henüz indirilen çıkmış sınav dosyası bulunamadı.
                        </td>
                      </tr>
                    ) : (
                      filteredExams.map((e, idx) => (
                        <tr key={idx} className="hover:bg-field/80 transition-colors">
                          <td className="py-2 px-3 font-semibold text-ink">
                            {e.name}
                          </td>
                          <td className="py-2 px-3 text-ink-3 font-mono text-2xs">
                            {e.sizeMb} MB
                          </td>
                          <td className="py-2 px-3">
                            <span className="inline-flex items-center gap-1 text-ok bg-ok-soft border border-ok/30 px-2 py-0.5 rounded text-2xs font-bold">
                              <CheckCircle2 className="w-3 h-3 text-ok" />
                              <span>meds_sorular içinde hazır</span>
                            </span>
                          </td>
                          <td className="py-2 px-3 text-right">
                            {e.status === 'extracted' ? (
                              <span className="text-ok font-bold text-2xs">
                                ✓ Saf Metin (.txt) Hazır
                              </span>
                            ) : (
                              <span className="text-ink-3 text-2xs">
                                İndirildi
                              </span>
                            )}
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
