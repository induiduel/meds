import React, { useState, useEffect } from 'react';
import { 
  FolderDown, 
  CheckCircle2, 
  Clock, 
  AlertCircle, 
  RefreshCw, 
  FileText, 
  Search, 
  HardDrive, 
  ExternalLink,
  ChevronDown,
  ChevronUp,
  Cpu
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
    <div className={`bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden ${className}`}>
      {/* Header Bar */}
      <div className="bg-ink-surface text-white p-4 sm:p-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-[11px] font-bold text-teal-300 uppercase tracking-wider">
                Google Drive & Yerel Bilgisayar Arşiv İzleyici
              </span>
            </div>
            <h3 className="text-base sm:text-lg font-black text-white flex items-center gap-2">
              <HardDrive className="w-5 h-5 text-emerald-400" />
              <span>Yerel Disk & PDF İndirme Durumu</span>
            </h3>
            <p className="text-xs text-slate-300">
              Hedef klasör: <code className="bg-slate-800 text-teal-300 px-1.5 py-0.5 rounded font-mono text-[11px]">{summary?.databaseDir || 'C:\\Users\\indui\\Desktop\\meds_database'}</code>
            </p>
          </div>

          <div className="flex items-center gap-2 self-start sm:self-auto shrink-0">
            <button
              onClick={fetchStatus}
              disabled={isLoading}
              className="bg-teal-800/60 hover:bg-teal-700 text-teal-200 border border-teal-600/50 font-semibold px-3 py-1.5 rounded-xl text-xs flex items-center gap-1.5 transition-all cursor-pointer active:scale-95"
              title="Durumu yenile"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin text-emerald-400' : ''}`} />
              <span>{isLoading ? 'Kontrol...' : 'Yenile'}</span>
            </button>

            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold p-1.5 rounded-xl text-xs transition-colors cursor-pointer"
              title={isExpanded ? 'Paneli Daralt' : 'Paneli Genişlet'}
            >
              {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Live Progress Metrics Cards */}
        {summary && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4 pt-4 border-t border-slate-800/80">
            {/* 1. Ders Slaytları İlerlemesi */}
            <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-slate-300 flex items-center gap-1.5">
                  <FileText className="w-3.5 h-3.5 text-teal-400" />
                  Ders Notları & Slaytlar
                </span>
                <span className="font-black text-emerald-400 font-mono">
                  {summary.totalLecturesDownloaded} / {summary.totalLecturesTarget}
                </span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden">
                <div 
                  className="bg-accent h-full rounded-full transition-all duration-500"
                  style={{ width: `${summary.lecturesProgressPercent}%` }}
                />
              </div>
              <div className="flex justify-between text-[11px] text-slate-400 font-medium">
                <span>{summary.lecturesProgressPercent}% Tamamlandı</span>
                <span>{summary.totalLecturesDownloaded === summary.totalLecturesTarget ? '✅ Hepsi Hazır' : '⏳ İndiriliyor...'}</span>
              </div>
            </div>

            {/* 2. Çıkmış Sınavlar İlerlemesi */}
            <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-slate-300 flex items-center gap-1.5">
                  <FolderDown className="w-3.5 h-3.5 text-amber-400" />
                  Çıkmış Sınav PDF'leri
                </span>
                <span className="font-black text-amber-300 font-mono">
                  {summary.totalExamsDownloaded} / {summary.totalExamsTarget}
                </span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden">
                <div 
                  className="bg-accent h-full rounded-full transition-all duration-500"
                  style={{ width: `${summary.examsProgressPercent}%` }}
                />
              </div>
              <div className="flex justify-between text-[11px] text-slate-400 font-medium">
                <span>{summary.examsProgressPercent}% Tamamlandı</span>
                <span>{summary.totalExamsDownloaded >= summary.totalExamsTarget ? '✅ Arşiv Tam' : '⏳ Sürüyor...'}</span>
              </div>
            </div>

            {/* 3. Yerel Soru Ayrıştırma & OCR */}
            <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-3 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-slate-300 flex items-center gap-1.5">
                  <Cpu className="w-3.5 h-3.5 text-emerald-400" />
                  Çıkarılan Çıkmış Sorular
                </span>
                <span className="font-black text-white font-mono">
                  {summary.totalParsedQuestions.toLocaleString('tr-TR')} Soru
                </span>
              </div>
              <div className="text-[11px] text-emerald-300/90 font-medium flex items-center gap-1 pt-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>CPU ile birebir (saf metin) olarak veritabanına aktarıldı</span>
              </div>
              <div className="text-[11px] text-slate-400">Son güncelleme: {lastUpdated}</div>
            </div>
          </div>
        )}
      </div>

      {/* Collapsible Content */}
      {isExpanded && (
        <div className="p-4 sm:p-5 space-y-4">
          {/* Navigation & Search Filters */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
            <div className="flex items-center gap-2">
              <button
                onClick={() => setActiveTab('lectures')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  activeTab === 'lectures'
                    ? 'bg-teal-700 text-white shadow-2xs'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                📚 Ders Notları ({lectures.length})
              </button>
              <button
                onClick={() => setActiveTab('exams')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  activeTab === 'exams'
                    ? 'bg-teal-700 text-white shadow-2xs'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
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
                  className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-700 font-semibold focus:outline-none"
                >
                  <option value="all">Tüm Branşlar</option>
                  {disciplines.map((d) => (
                    <option key={d} value={d}>{d}</option>
                  ))}
                </select>
              )}

              <div className="relative flex-1 sm:w-64">
                <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Ders veya dosya adı ara..."
                  className="w-full text-xs pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:bg-white focus:outline-none focus:ring-1 focus:ring-teal-500"
                />
              </div>
            </div>
          </div>

          {/* Table / List */}
          {activeTab === 'lectures' ? (
            <div className="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <div className="max-h-72 overflow-y-auto">
                <table className="w-full text-left border-collapse text-xs">
                  <thead className="sticky top-0 bg-slate-50 border-b border-slate-200 text-slate-700 font-bold uppercase text-[11px] tracking-wider z-10">
                    <tr>
                      <th className="py-2.5 px-3">Ders Slayt Başlığı</th>
                      <th className="py-2.5 px-3">Branş</th>
                      <th className="py-2.5 px-3">Boyut</th>
                      <th className="py-2.5 px-3">Yerel Disk Durumu</th>
                      <th className="py-2.5 px-3 text-right">İşlem</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {filteredLectures.length === 0 ? (
                      <tr>
                        <td colSpan={5} className="py-6 text-center text-slate-400">
                          Arama kriterine uygun ders bulunamadı.
                        </td>
                      </tr>
                    ) : (
                      filteredLectures.map((l, idx) => (
                        <tr key={l.fileId || idx} className="hover:bg-slate-50/80 transition-colors">
                          <td className="py-2 px-3 font-semibold text-slate-900">
                            <span className="block leading-snug">{l.title}</span>
                            <span className="text-[11px] text-slate-400 font-mono block">Dosya: {l.localName}</span>
                          </td>
                          <td className="py-2 px-3 text-slate-600">
                            <span className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-[11px] font-semibold">
                              {l.folderName}
                            </span>
                          </td>
                          <td className="py-2 px-3 text-slate-500 font-mono text-[11px]">
                            {l.isDownloaded ? `${l.sizeMb} MB` : '-'}
                          </td>
                          <td className="py-2 px-3">
                            {l.isDownloaded ? (
                              <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded text-[11px] font-bold">
                                <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                                <span>İndirildi (Bilgisayarda Mevcut)</span>
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1 text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded text-[11px] font-bold">
                                <Clock className="w-3 h-3 text-amber-500 animate-spin" />
                                <span>Drive'dan İndiriliyor...</span>
                              </span>
                            )}
                          </td>
                          <td className="py-2 px-3 text-right">
                            <button
                              onClick={() => onSelectLecture && onSelectLecture(l.title, l.fileId)}
                              className={`text-xs font-bold px-2.5 py-1 rounded-lg cursor-pointer transition-colors ${
                                l.isDownloaded
                                  ? 'bg-teal-700 hover:bg-teal-800 text-white'
                                  : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
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
            <div className="border border-slate-200 rounded-xl overflow-hidden shadow-2xs">
              <div className="max-h-72 overflow-y-auto">
                <table className="w-full text-left border-collapse text-xs">
                  <thead className="sticky top-0 bg-slate-50 border-b border-slate-200 text-slate-700 font-bold uppercase text-[11px] tracking-wider z-10">
                    <tr>
                      <th className="py-2.5 px-3">Çıkmış Sınav Dosyası</th>
                      <th className="py-2.5 px-3">Boyut</th>
                      <th className="py-2.5 px-3">Yerel Durum</th>
                      <th className="py-2.5 px-3 text-right">Metin Çıkarımı</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {filteredExams.length === 0 ? (
                      <tr>
                        <td colSpan={4} className="py-6 text-center text-slate-400">
                          Henüz indirilen çıkmış sınav dosyası bulunamadı.
                        </td>
                      </tr>
                    ) : (
                      filteredExams.map((e, idx) => (
                        <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                          <td className="py-2 px-3 font-semibold text-slate-900">
                            {e.name}
                          </td>
                          <td className="py-2 px-3 text-slate-500 font-mono text-[11px]">
                            {e.sizeMb} MB
                          </td>
                          <td className="py-2 px-3">
                            <span className="inline-flex items-center gap-1 text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded text-[11px] font-bold">
                              <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                              <span>meds_sorular içinde hazır</span>
                            </span>
                          </td>
                          <td className="py-2 px-3 text-right">
                            {e.status === 'extracted' ? (
                              <span className="text-teal-700 font-bold text-[11px]">
                                ✓ Saf Metin (.txt) Hazır
                              </span>
                            ) : (
                              <span className="text-slate-400 text-[11px]">
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
