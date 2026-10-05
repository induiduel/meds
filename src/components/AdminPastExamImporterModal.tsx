import React, { useState } from 'react';
import { 
  X, 
  Sparkles, 
  Upload, 
  FileText, 
  CheckCircle2, 
  AlertCircle, 
  Layers, 
  Trash2, 
  Edit3, 
  Plus, 
  RefreshCw,
  FolderPlus,
  BookOpen,
  Calendar,
  Check,
  ChevronDown,
  Info,
  Cloud,
  Database
} from 'lucide-react';
import { Committee, QuestionItem } from '../types';
import { ApiService } from '../services/api';
import { InfoPopover } from './InfoPopover';
import { DONEM3_CURRICULUM_DISCIPLINES } from '../data/curriculumData';

interface AdminPastExamImporterModalProps {
  isOpen: boolean;
  onClose: () => void;
  adminEmail: string;
  committees: Committee[];
  selectedCommitteeId: string;
  onImportSuccess: () => Promise<void>;
}

export const AdminPastExamImporterModal: React.FC<AdminPastExamImporterModalProps> = ({
  isOpen,
  onClose,
  adminEmail,
  committees,
  selectedCommitteeId,
  onImportSuccess,
}) => {
  const [examYear, setExamYear] = useState('2023-2024');
  const [targetCommitteeId, setTargetCommitteeId] = useState(selectedCommitteeId || (committees[0]?.id || 'donem3-kurul2'));
  const [defaultDiscipline, setDefaultDiscipline] = useState('Otomatik (Yapay Zeka Tespit Etsin)');
  const [rawText, setRawText] = useState('');
  const [fileName, setFileName] = useState<string | null>(null);
  const [uploadedFileBase64, setUploadedFileBase64] = useState<string | null>(null);
  const [uploadedFileMime, setUploadedFileMime] = useState<string | null>(null);

  // Parsing state
  const [isParsing, setIsParsing] = useState(false);
  const [isExtractingFile, setIsExtractingFile] = useState(false);
  const [fileExtractStatus, setFileExtractStatus] = useState<string | null>(null);
  const [parseError, setParseError] = useState<string | null>(null);
  const [parsedQuestions, setParsedQuestions] = useState<any[]>([]);
  const [autoSaveToFirebase, setAutoSaveToFirebase] = useState(true);

  // Importing state
  const [isImporting, setIsImporting] = useState(false);
  const [importSuccessMessage, setImportSuccessMessage] = useState<string | null>(null);

  if (!isOpen) return null;

  // Handle file upload (.pdf, .docx, .txt, .md) with AI text extraction
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setParseError(null);
    setFileExtractStatus(null);

    const isBinaryDoc = file.name.toLowerCase().endsWith('.pdf') || 
                        file.name.toLowerCase().endsWith('.docx') || 
                        file.name.toLowerCase().endsWith('.doc');

    if (isBinaryDoc) {
      setIsExtractingFile(true);
      setFileExtractStatus(`Belge hazırlanıyor: ${file.name}...`);

      const mimeType = file.type || (file.name.endsWith('.pdf') ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document');
      setUploadedFileMime(mimeType);

      const reader = new FileReader();
      reader.onload = async (ev) => {
        const base64Data = ev.target?.result as string;
        setUploadedFileBase64(base64Data);

        try {
          setFileExtractStatus(`Yapay zeka ${file.name} belgesini inceliyor ve metne döküyor...`);
          const res = await fetch('/api/ai/extract-document', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              fileBase64: base64Data,
              fileName: file.name,
              fileMimeType: mimeType,
            }),
          });

          const resText = await res.text();
          let data: any = {};
          try {
            data = JSON.parse(resText);
          } catch (jsonErr) {
            // Server returned non-JSON error
            throw new Error(resText.slice(0, 100) || `Sunucu yanıtı geçersiz (${res.status})`);
          }

          if (!res.ok) {
            throw new Error(data.error || 'Dosya okunamadı');
          }

          if (data.extractedText) {
            setRawText(data.extractedText);
            setFileExtractStatus(`✓ ${file.name} başarıyla okundu! (${data.extractedText.length} karakter metin aktarıldı)`);
          } else {
            setFileExtractStatus(`✓ ${file.name} doğrudan PDF olarak hazırlandı. Şimdi "Soruları Ayrıştır" butonuna tıklayabilirsiniz.`);
          }
        } catch (err: any) {
          // Keep file in memory so direct PDF parsing can still succeed
          setFileExtractStatus(`ℹ️ ${file.name} yüklendi. Doğrudan PDF analiziyle sorular ayrıştırılacaktır.`);
        } finally {
          setIsExtractingFile(false);
        }
      };
      reader.readAsDataURL(file);
    } else {
      // Plain text or Markdown
      const reader = new FileReader();
      reader.onload = (ev) => {
        const content = ev.target?.result as string;
        if (content) {
          setRawText(content);
          setFileExtractStatus(`✓ ${file.name} metin olarak yüklendi.`);
        }
      };
      reader.readAsText(file);
    }
  };

  // Run AI extraction
  const handleParseQuestions = async () => {
    if (!rawText.trim() && !uploadedFileBase64) {
      setParseError('Lütfen çıkmış soru metnini yapıştırın veya bir PDF/DOCX dosya seçin.');
      return;
    }

    setIsParsing(true);
    setParseError(null);
    setImportSuccessMessage(null);

    try {
      const res = await ApiService.parsePastExamQuestions({
        rawText: rawText.trim() || undefined,
        fileBase64: uploadedFileBase64 || undefined,
        fileMimeType: uploadedFileMime || undefined,
        fileName: fileName || undefined,
        examYear,
        committeeId: targetCommitteeId,
        defaultDiscipline: defaultDiscipline.startsWith('Otomatik') ? undefined : defaultDiscipline,
        adminEmail,
      });

      if (!res.questions || res.questions.length === 0) {
        throw new Error('Belgede geçerli bir soru formatı tespit edilemedi.');
      }

      setParsedQuestions(res.questions);

      // If Auto-Save to Firebase & Server is enabled, save immediately
      if (autoSaveToFirebase) {
        setIsImporting(true);
        try {
          const importResult = await ApiService.batchImportPastQuestions(
            adminEmail,
            targetCommitteeId,
            examYear,
            res.questions
          );

          const syncTargets = [];
          if (importResult.serverSynced) syncTargets.push('Yerel Sunucu');
          if (importResult.firebaseSynced) syncTargets.push('Firebase Firestore Bulut Veritabanı');
          const syncedStr = syncTargets.length > 0 ? syncTargets.join(' ve ') : 'Veritabanı';

          setImportSuccessMessage(
            `✓ ${importResult.count} adet çıkmış soru yapay zeka ile ayrıştırıldı ve doğrudan ${syncedStr} üzerine kaydedildi! (Tüm beğeniler 0 olarak başlatıldı)`
          );
          await onImportSuccess();
        } catch (saveErr: any) {
          setParseError(`Sorular ayrıştırıldı ancak veritabanına otomatik aktarılırken uyarı oluştu: ${saveErr.message}. Aşağıdaki yeşil butondan manuel aktarımı deneyebilirsiniz.`);
        } finally {
          setIsImporting(false);
        }
      } else {
        setFileExtractStatus(`✓ ${res.questions.length} adet soru ayrıştırıldı. Şimdi aşağıdaki 'Tümünü Veritabanına ve Firebase'e Aktar' butonuna tıklayarak kaydedebilirsiniz.`);
      }
    } catch (err: any) {
      setParseError(err.message || 'Yapay zeka ayrıştırma sırasında hata oluştu.');
    } finally {
      setIsParsing(false);
    }
  };

  // Inline edit handlers for parsed list
  const handleUpdateParsedField = (index: number, field: string, value: any) => {
    setParsedQuestions((prev) =>
      prev.map((q, i) => (i === index ? { ...q, [field]: value } : q))
    );
  };

  const handleUpdateOption = (qIndex: number, optKey: string, newText: string) => {
    setParsedQuestions((prev) =>
      prev.map((q, i) => {
        if (i !== qIndex) return q;
        const newOptions = (q.options || []).map((opt: any) =>
          opt.key === optKey ? { ...opt, text: newText } : opt
        );
        return { ...q, options: newOptions };
      })
    );
  };

  const handleDeleteParsedQuestion = (index: number) => {
    setParsedQuestions((prev) => prev.filter((_, i) => i !== index));
  };

  // Save to database
  const handleBatchImport = async (questionsOverride?: any[]) => {
    const listToSave = questionsOverride || parsedQuestions;
    if (listToSave.length === 0) return;

    setIsImporting(true);
    try {
      const result = await ApiService.batchImportPastQuestions(
        adminEmail,
        targetCommitteeId,
        examYear,
        listToSave
      );

      const syncTargets = [];
      if (result.serverSynced) syncTargets.push('Yerel Sunucu');
      if (result.firebaseSynced) syncTargets.push('Firebase Firestore Bulutu');
      const syncedStr = syncTargets.length > 0 ? syncTargets.join(' ve ') : 'Veritabanı';

      setImportSuccessMessage(
        `✓ ${result.count} adet çıkmış soru ${syncedStr} üzerine başarıyla kaydedildi! (Beğeniler 0 olarak başlatıldı, çift tıklamayla beğeni iptali devrede)`
      );
      setParsedQuestions([]);
      setRawText('');
      setFileName(null);
      await onImportSuccess();
    } catch (err: any) {
      alert('İçe aktarma hatası: ' + err.message);
    } finally {
      setIsImporting(false);
    }
  };

  return (
    <div className="ms-overlay fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-2 sm:p-4 overflow-y-auto">
      <div className="ms-modal-panel bg-white rounded-2xl w-full max-w-5xl shadow-2xl border border-slate-200 overflow-hidden my-auto flex flex-col max-h-[92dvh]">
        {/* Header */}
        <div className="bg-ink-surface text-white p-4 sm:p-5 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-300 border border-teal-400/30 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-teal-300" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-sm sm:text-base">
                  Çıkmış Soru Yükleme & Yapay Zeka Ayrıştırıcı
                </h3>
                <span className="bg-teal-500/20 text-teal-200 border border-teal-400/30 text-[11px] font-bold px-2 py-0.5 rounded-full">
                  Admin Aracı
                </span>
              </div>
              <p className="text-xs text-slate-300">
                Geçmiş senelerin kısmi veya tam sorularını yükleyin, yapay zeka standart formata çevirsin.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <InfoPopover title="Çıkmış Soru Yükleme Rehberi" buttonClassName="text-white hover:text-teal-200">
              <p>
                Geçmiş senelerin (2020-2024 vb.) çıkmış sorularını Word'den, PDF'ten, Telegram/WhatsApp gruplarından kopyalayıp buraya yapıştırabilirsiniz.
              </p>
              <p className="mt-1">
                Yapay Zeka (Gemini); soru kökünü, 5 şıkkı, varsa doğru cevabı ve branşı otomatik tespit eder.
              </p>
              <p className="mt-1 font-semibold text-teal-800">
                Veritabanına aktarıldıktan sonra tüm öğrenciler sorular üzerinde yeni şık önerisi verebilir, oylayabilir ve düzenleyebilir.
              </p>
            </InfoPopover>

            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Success Banner */}
        {importSuccessMessage && (
          <div className="bg-emerald-50 border-b border-emerald-200 p-4 text-emerald-900 text-xs flex items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
              <span>{importSuccessMessage}</span>
            </div>
            <button
              onClick={() => setImportSuccessMessage(null)}
              className="font-bold text-emerald-700 hover:text-emerald-900 cursor-pointer shrink-0"
            >
              Kapat
            </button>
          </div>
        )}

        {/* Error Banner */}
        {parseError && (
          <div className="bg-rose-50 border-b border-rose-200 p-3 text-rose-900 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{parseError}</span>
          </div>
        )}

        {/* Content Body */}
        <div className="p-4 sm:p-6 overflow-y-auto space-y-5 text-xs">
          {/* Metadata Controls Bar */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 bg-slate-50 p-3.5 rounded-xl border border-slate-200">
            {/* Exam Year */}
            <div>
              <label className="block text-[11px] font-bold text-slate-700 mb-1">
                Sınav Senesi / Yıl
              </label>
              <select
                value={examYear}
                onChange={(e) => setExamYear(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs font-semibold text-slate-800"
              >
                <option value="Kategorisiz">Kategorisiz / Belirtilmemiş Yıl</option>
                <option value="2024-2025">2024-2025</option>
                <option value="2023-2024">2023-2024</option>
                <option value="2022-2023">2022-2023</option>
                <option value="2021-2022">2021-2022</option>
                <option value="2020-2021">2020-2021</option>
                <option value="Geçmiş Yıllar">Geçmiş Yıllar (Genel)</option>
              </select>
            </div>

            {/* Target Committee */}
            <div>
              <label className="block text-[11px] font-bold text-slate-700 mb-1">
                Hedef Kurul / Komite
              </label>
              <select
                value={targetCommitteeId}
                onChange={(e) => setTargetCommitteeId(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs font-semibold text-slate-800 truncate"
              >
                {committees.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Discipline */}
            <div>
              <label className="block text-[11px] font-bold text-slate-700 mb-1">
                Ders / Branş (Dönem 3 Müfredatı)
              </label>
              <select
                value={defaultDiscipline}
                onChange={(e) => setDefaultDiscipline(e.target.value)}
                className="w-full bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs font-semibold text-slate-800"
              >
                <option value="Otomatik (Yapay Zeka Tespit Etsin)">Otomatik (Yapay Zeka Tespit Etsin)</option>
                {DONEM3_CURRICULUM_DISCIPLINES.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Paste or Upload Area */}
          <div className="space-y-2">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <label className="font-bold text-slate-800 text-xs flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-teal-600" />
                <span>Çıkmış Soru Metni veya Dosya İçeriği</span>
              </label>

              <label className="inline-flex items-center gap-1.5 px-3 py-1 bg-white hover:bg-slate-50 border border-slate-300 rounded-lg text-[11px] font-semibold text-slate-700 cursor-pointer shadow-2xs">
                <Upload className="w-3.5 h-3.5 text-teal-600" />
                <span>{fileName ? `Dosya: ${fileName}` : 'Dosya Seç (.pdf, .docx, .txt)'}</span>
                <input
                  type="file"
                  accept=".pdf,.docx,.doc,.txt,.md"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </label>
            </div>

            {isExtractingFile && (
              <div className="bg-teal-50 border border-teal-200 text-teal-900 p-2.5 rounded-xl flex items-center gap-2 text-xs font-semibold animate-pulse">
                <div className="w-3.5 h-3.5 border-2 border-teal-600 border-t-transparent rounded-full animate-spin shrink-0" />
                <span>Yapay zeka PDF / Word belgesini metne dönüştürüyor...</span>
              </div>
            )}

            {fileExtractStatus && !isExtractingFile && (
              <div className="bg-emerald-50 border border-emerald-200 text-emerald-900 p-2 rounded-xl flex items-center gap-2 text-xs font-medium">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>{fileExtractStatus}</span>
              </div>
            )}

            <textarea
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              placeholder="Örnek:
1) 54 yaşında erkek hasta göğüs ağrısıyla geliyor...
A) Miyokard enfarktüsü
B) Perikardit
C) Aort diseksiyonu
D) Pulmoner emboli
E) Özofajit
Cevap: A

2) Bradikinin birikimine bağlı kuru öksürük yapan ilaç hangisidir?..."
              rows={7}
              className="w-full p-3 bg-white border border-slate-300 rounded-xl font-mono text-[11px] text-slate-800 focus:outline-hidden focus:ring-2 focus:ring-teal-500/20"
            />
          </div>

          {/* Action Button & Auto-Save Toggle */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-2">
            <label className="flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer bg-slate-50 border border-slate-200 px-3 py-2 rounded-xl hover:bg-slate-100 transition-colors">
              <input
                type="checkbox"
                checked={autoSaveToFirebase}
                onChange={(e) => setAutoSaveToFirebase(e.target.checked)}
                className="w-4 h-4 text-teal-600 rounded focus:ring-teal-500"
              />
              <span className="flex items-center gap-1.5">
                <Cloud className="w-3.5 h-3.5 text-teal-600" />
                <span>Ayrıştırıldığında doğrudan Firebase & Sunucuya Otomatik Kaydet</span>
              </span>
            </label>

            <button
              onClick={handleParseQuestions}
              disabled={isParsing || isImporting || (!rawText.trim() && !uploadedFileBase64)}
              className="bg-accent hover:from-teal-800 hover:to-emerald-800 disabled:opacity-50 text-white font-bold px-5 py-2.5 rounded-xl text-xs flex items-center justify-center gap-2 shadow-md cursor-pointer active:scale-95"
            >
              {isParsing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Yapay Zeka Soruları Ayrıştırıyor...</span>
                </>
              ) : isImporting ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Firebase & Sunucuya Kaydediliyor...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-teal-200" />
                  <span>Yapay Zeka ile Ayrıştır & Şıkları Çıkar</span>
                </>
              )}
            </button>
          </div>

          {/* Staging / Parsed Questions List */}
          {parsedQuestions.length > 0 && (
            <div className="space-y-4 pt-4 border-t border-slate-200">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-canvas p-3.5 rounded-xl border border-teal-300 shadow-2xs">
                <div className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-teal-700" />
                    <span className="font-bold text-teal-950 text-xs">
                      {parsedQuestions.length} Soru Tespit Edildi ({examYear})
                    </span>
                    <span className="bg-teal-700 text-white font-mono text-[11px] font-bold px-2 py-0.5 rounded-full">
                      Beğeniler: 0
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-600">
                    Aşağıdaki sorularda düzenleme yapabilir veya doğrudan bulut havuzuna aktarabilirsiniz.
                  </p>
                </div>

                <button
                  onClick={() => handleBatchImport()}
                  disabled={isImporting}
                  className="bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold px-4 py-2.5 rounded-xl text-xs flex items-center justify-center gap-1.5 shadow-md cursor-pointer active:scale-95 shrink-0"
                >
                  {isImporting ? (
                    <>
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                      <span>Firebase & Sunucuya Aktarılıyor...</span>
                    </>
                  ) : (
                    <>
                      <Cloud className="w-4 h-4 text-emerald-200" />
                      <span>Tümünü Firebase ve Sunucuya Aktar</span>
                    </>
                  )}
                </button>
              </div>

              {/* Individual Question Cards for Editing */}
              <div className="space-y-3">
                {parsedQuestions.map((q, idx) => (
                  <div
                    key={idx}
                    className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-3 relative group"
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="bg-slate-900 text-white font-black px-2 py-0.5 rounded text-[11px]">
                          Soru #{q.questionNumber || idx + 1}
                        </span>
                        <input
                          type="text"
                          value={q.discipline || ''}
                          onChange={(e) => handleUpdateParsedField(idx, 'discipline', e.target.value)}
                          className="bg-white border border-slate-300 rounded px-2 py-0.5 text-[11px] font-bold text-teal-800"
                          placeholder="Ders / Branş"
                        />
                        <input
                          type="text"
                          value={q.topic || ''}
                          onChange={(e) => handleUpdateParsedField(idx, 'topic', e.target.value)}
                          className="bg-white border border-slate-300 rounded px-2 py-0.5 text-[11px] text-slate-700 flex-1 min-w-[140px]"
                          placeholder="Soru Başlığı / Konusu"
                        />
                      </div>

                      <div className="flex items-center gap-2">
                        <div className="flex items-center gap-1">
                          <span className="text-[11px] font-bold text-slate-600">Doğru Yanıt:</span>
                          <select
                            value={q.claimedAnswer || 'C'}
                            onChange={(e) => handleUpdateParsedField(idx, 'claimedAnswer', e.target.value)}
                            className="bg-white border border-slate-300 rounded px-1.5 py-0.5 text-xs font-bold text-emerald-700"
                          >
                            <option value="A">A</option>
                            <option value="B">B</option>
                            <option value="C">C</option>
                            <option value="D">D</option>
                            <option value="E">E</option>
                          </select>
                        </div>

                        <button
                          onClick={() => handleDeleteParsedQuestion(idx)}
                          className="text-slate-400 hover:text-rose-600 p-1 rounded transition-colors"
                          title="Bu soruyu listeden çıkar"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>

                    {/* Question Stem */}
                    <div>
                      <label className="block text-[11px] font-bold text-slate-500 mb-0.5">Soru Kökü</label>
                      <textarea
                        value={q.stem || ''}
                        onChange={(e) => handleUpdateParsedField(idx, 'stem', e.target.value)}
                        rows={2}
                        className="w-full p-2 bg-white border border-slate-300 rounded-lg text-xs text-slate-900"
                      />
                    </div>

                    {/* Options Grid */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {(q.options || []).map((opt: any) => (
                        <div key={opt.key} className="flex items-center gap-1.5 bg-white p-1.5 rounded-lg border border-slate-200">
                          <span
                            className={`w-5 h-5 rounded-full flex items-center justify-center font-bold text-[11px] shrink-0 ${
                              q.claimedAnswer === opt.key
                                ? 'bg-emerald-600 text-white'
                                : 'bg-slate-100 text-slate-700'
                            }`}
                          >
                            {opt.key}
                          </span>
                          <input
                            type="text"
                            value={opt.text || ''}
                            onChange={(e) => handleUpdateOption(idx, opt.key, e.target.value)}
                            className="w-full text-xs text-slate-800 bg-transparent outline-hidden"
                            placeholder={`${opt.key} şıkkı metni`}
                          />
                        </div>
                      ))}
                    </div>

                    {/* Explanation */}
                    {q.explanation && (
                      <p className="text-[11px] text-slate-500 bg-white/70 p-2 rounded-lg border border-slate-200/60 italic">
                        <strong>Tıbbi Açıklama:</strong> {q.explanation}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-slate-50 p-4 border-t border-slate-200 flex items-center justify-between shrink-0">
          <span className="text-[11px] text-slate-500">
            MeDSor Admin Motoru • Sorular eklendikten sonra soru havuzunda anında listelenir.
          </span>

          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded-lg font-semibold text-xs cursor-pointer"
          >
            Kapat
          </button>
        </div>
      </div>
    </div>
  );
};
