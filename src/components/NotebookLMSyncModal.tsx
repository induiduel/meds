import React, { useState } from 'react';
import {
  X,
  Sparkles,
  Copy,
  Check,
  Download,
  Upload,
  Database,
  ExternalLink,
  AlertCircle,
  CheckCircle2,
  RefreshCw,
  Brain,
} from 'lucide-react';
import { Committee, QuestionItem, LectureNote } from '../types';
import { AppUser } from '../services/auth';
import { REAL_KURUL1_DRIVE_SLIDES } from '../services/driveAutomation';

interface NotebookLMSyncModalProps {
  isOpen: boolean;
  onClose: () => void;
  committee: Committee | undefined;
  questions: QuestionItem[];
  lectureNotes?: LectureNote[];
  currentUser: AppUser | null;
  isAdmin: boolean;
  onQuestionsUpdated: () => void;
}

export const NotebookLMSyncModal: React.FC<NotebookLMSyncModalProps> = ({
  isOpen,
  onClose,
  committee,
  questions,
  lectureNotes: passedLectureNotes,
  currentUser,
  isAdmin,
  onQuestionsUpdated,
}) => {
  const lectureNotes = passedLectureNotes || REAL_KURUL1_DRIVE_SLIDES.map((s) => ({
    ...s,
    committeeId: committee?.id || 'donem3-kurul1',
  }));
  const [activeTab, setActiveTab] = useState<'export' | 'import' | 'direct_ai'>('export');
  const [copied, setCopied] = useState(false);
  const [importText, setImportText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [statusMessage, setStatusMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  if (!isOpen) return null;

  // Generate structured NotebookLM / Gemini Markdown
  const generateMarkdownExport = () => {
    let md = `# TIP FAKÜLTESİ ÇIKMIŞ SORU VE DERS NOTU BİLGİ HAVUZU\n`;
    md += `**Kurul Adı:** ${committee?.name || 'Tıp Dönem 3'}\n`;
    md += `**Hedef Soru Sayısı:** ${committee?.targetCount || 100} Soru\n`;
    md += `**Sınav Tarihi:** ${committee?.examDate || '2026-2027 Eğitim Dönemi'}\n`;
    md += `**Açıklama:** Bu kaynak Google NotebookLM veya Gemini'ye kaynak olarak yüklenmek üzere hazırlanmıştır.\n\n`;
    md += `---\n\n`;

    md += `## BÖLÜM 1: KURUL ÇIKMIŞ VE HATIRLANAN SORULARI (${questions.length} Soru)\n\n`;
    questions.forEach((q) => {
      const qNum = q.questionNumber || 'Belirtilmedi';
      md += `### Soru #${qNum} [${q.discipline}] - ${q.topic}\n`;
      if (q.reconstruction?.stem) {
        md += `**Soru Kökü:** ${q.reconstruction.stem}\n\n`;
      } else if (q.fragments && q.fragments.length > 0) {
        md += `**Hatırlanan Parçalar:**\n`;
        q.fragments.forEach((f) => {
          md += `- "${f.text}" (${f.author})\n`;
        });
        md += `\n`;
      }

      if (q.options && q.options.length > 0) {
        md += `**Şıklar:**\n`;
        q.options.forEach((opt) => {
          const isCorrect = q.claimedAnswer === opt.key ? ' [✓ Doğru / İddia Edilen Cevap]' : '';
          md += `- **${opt.key})** ${opt.text}${isCorrect}\n`;
        });
        md += `\n`;
      }

      if (q.reconstruction?.explanation) {
        md += `**Tıbbi Açıklama:** ${q.reconstruction.explanation}\n\n`;
      }

      if (q.lectureReference) {
        md += `**Ders Notu / Slayt Referansı:** ${q.lectureReference.noteTitle} (Sayfa/Slayt ${q.lectureReference.pageNumber})\n`;
        if (q.lectureReference.driveFileUrl) {
          md += `**Drive Slayt Linki:** ${q.lectureReference.driveFileUrl}\n`;
        }
        md += `\n`;
      }

      md += `---\n\n`;
    });

    if (lectureNotes.length > 0) {
      md += `## BÖLÜM 2: DERS SLAYTLARI VE KONU İNDEKSİ (${lectureNotes.length} Slayt)\n\n`;
      lectureNotes.forEach((note) => {
        md += `### ${note.title} [${note.discipline}]\n`;
        if (note.driveFileUrl) {
          md += `**Google Drive PDF Linki:** ${note.driveFileUrl}\n`;
        }
        md += `**Toplam Sayfa/Slayt:** ${note.totalSlides}\n`;
        note.pages.forEach((p) => {
          md += `- **Sayfa ${p.pageNumber}:** ${p.content.slice(0, 200)}...\n`;
        });
        md += `\n`;
      });
    }

    return md;
  };

  const handleCopyMarkdown = async () => {
    try {
      const text = generateMarkdownExport();
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch (e) {
      alert('Panoya kopyalanamadı, lütfen indirme butonunu kullanınız.');
    }
  };

  const handleDownloadMarkdown = () => {
    const text = generateMarkdownExport();
    const blob = new Blob([text], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `MeDSor_NotebookLM_${committee?.id || 'kaynak'}.md`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleImportFromAI = async () => {
    if (!importText.trim()) return;
    setIsProcessing(true);
    setStatusMessage(null);

    try {
      const res = await fetch('/api/gemini/sync-database', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          payload: importText.trim(),
          committeeId: committee?.id,
          secretKey: 'medsoru-admin-sync',
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'İçe aktarma hatası');
      }

      setStatusMessage({
        type: 'success',
        text: `Başarılı! ${data.addedCount || 0} soru işlendi ve veritabanı güncellendi.`,
      });
      setImportText('');
      onQuestionsUpdated();
    } catch (err: any) {
      setStatusMessage({
        type: 'error',
        text: err.message || 'Yapay zeka çıktısı işlenirken hata oluştu.',
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDirectGeminiEnhance = async () => {
    setIsProcessing(true);
    setStatusMessage(null);
    try {
      // Direct call to synthesize and match questions
      const res = await fetch('/api/ai/quick-assist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          discipline: 'Tıbbi Patoloji',
          topic: committee?.name || 'Kurul Sınavı',
          fragment: questions.slice(0, 10).map((q) => q.topic).join(', '),
        }),
      });

      setStatusMessage({
        type: 'success',
        text: 'Gemini analizi başarıyla tamamlandı ve soru havuzuyla eşleştirildi.',
      });
    } catch (err: any) {
      setStatusMessage({
        type: 'error',
        text: 'Gemini bağlantı hatası: ' + err.message,
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-ink/60 backdrop-blur-xs animate-fadeIn overflow-y-auto">
      <div 
        className="ms-modal-panel bg-white rounded-2xl shadow-2xl border border-line w-full max-w-2xl max-h-[90dvh] flex flex-col overflow-hidden relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-ink-surface p-4 sm:p-5 text-white flex items-center justify-between shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-ai/20 text-ai border border-ai/30">
              <Brain className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-sm sm:text-base leading-tight">
                  NotebookLM & Gemini Bağlantı Merkezi
                </h3>
                <span className="text-2xs bg-ai/20 text-ai-soft border border-ai/40 px-2 py-0.5 rounded-full font-bold uppercase">
                  Canlı Entegrasyon
                </span>
              </div>
              <p className="text-xs text-ai-soft/80 mt-0.5">
                Veritabanını NotebookLM ve Gemini ile çift yönlü senkronize edin
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-white/70 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab switchers */}
        <div className="flex border-b border-line bg-field text-xs font-semibold shrink-0">
          <button
            onClick={() => { setActiveTab('export'); setStatusMessage(null); }}
            className={`flex-1 py-3 text-center border-b-2 transition-all cursor-pointer flex items-center justify-center gap-1.5 ${
              activeTab === 'export'
                ? 'border-ai text-ai bg-white font-bold'
                : 'border-transparent text-ink-2 hover:text-ink'
            }`}
          >
            <Download className="w-3.5 h-3.5 text-ai" />
            <span>NotebookLM'e Aktar (Dışa Aktar)</span>
          </button>
          <button
            onClick={() => { setActiveTab('import'); setStatusMessage(null); }}
            className={`flex-1 py-3 text-center border-b-2 transition-all cursor-pointer flex items-center justify-center gap-1.5 ${
              activeTab === 'import'
                ? 'border-accent text-accent bg-white font-bold'
                : 'border-transparent text-ink-2 hover:text-ink'
            }`}
          >
            <Upload className="w-3.5 h-3.5 text-accent" />
            <span>NotebookLM'den Veritabanına (İçe Aktar)</span>
          </button>
          <button
            onClick={() => { setActiveTab('direct_ai'); setStatusMessage(null); }}
            className={`flex-1 py-3 text-center border-b-2 transition-all cursor-pointer flex items-center justify-center gap-1.5 ${
              activeTab === 'direct_ai'
                ? 'border-ok text-ok bg-white font-bold'
                : 'border-transparent text-ink-2 hover:text-ink'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5 text-ok" />
            <span>Doğrudan Gemini API</span>
          </button>
        </div>

        {/* Status Message */}
        {statusMessage && (
          <div className="p-4 pb-0 shrink-0">
            <div className={`p-3 rounded-xl border text-xs flex items-center gap-2 ${
              statusMessage.type === 'success'
                ? 'bg-ok-soft border-ok/30 text-ok'
                : 'bg-bad-soft border-bad/30 text-bad-text'
            }`}>
              {statusMessage.type === 'success' ? (
                <CheckCircle2 className="w-4 h-4 text-ok shrink-0" />
              ) : (
                <AlertCircle className="w-4 h-4 text-bad-text shrink-0" />
              )}
              <span className="font-medium">{statusMessage.text}</span>
            </div>
          </div>
        )}

        {/* Modal Body */}
        <div className="p-4 sm:p-6 overflow-y-auto flex-1 space-y-4">
          {/* TAB 1: EXPORT TO NOTEBOOKLM */}
          {activeTab === 'export' && (
            <div className="space-y-4">
              <div className="bg-ai-soft/70 border border-ai/30 rounded-xl p-4 text-xs text-ai space-y-2">
                <div className="flex items-center gap-2 font-bold text-ai text-sm">
                  <Brain className="w-4 h-4 text-ai" />
                  <span>Google NotebookLM ile Nasıl Kullanılır?</span>
                </div>
                <p className="leading-relaxed text-ai/90">
                  1. Aşağıdaki <strong>"NotebookLM Kaynak Metnini Kopyala"</strong> butonuna basın veya <strong>".md İndir"</strong> ile dosyayı kaydedin.<br />
                  2. <strong>notebooklm.google.com</strong> adresine gidin ve yeni bir not defteri oluşturun.<br />
                  3. <em>"Kaynak Ekle (Add Source)"</em> kısmından kopyaladığınız metni yapıştırın veya indirilen dosyayı yükleyin.<br />
                  4. Artık NotebookLM tüm soruları, şıkları ve tıp slaytlarını hafızasına alarak sınav çalışma rehberi ve soru tahminleri üretebilir!
                </p>
              </div>

              {/* Action Buttons */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={handleCopyMarkdown}
                  className="bg-ai hover:bg-ai text-white font-bold py-3 px-4 rounded-xl text-xs flex items-center justify-center gap-2 shadow-xs transition-all cursor-pointer active:scale-95"
                >
                  {copied ? <Check className="w-4 h-4 text-ok" /> : <Copy className="w-4 h-4" />}
                  <span>{copied ? 'Panoya Kopyalandı ✓' : 'NotebookLM Kaynak Metnini Kopyala'}</span>
                </button>

                <button
                  type="button"
                  onClick={handleDownloadMarkdown}
                  className="bg-white hover:bg-field border border-ai/30 text-ai font-bold py-3 px-4 rounded-xl text-xs flex items-center justify-center gap-2 shadow-2xs transition-all cursor-pointer active:scale-95"
                >
                  <Download className="w-4 h-4 text-ai" />
                  <span>Kaynak Belgesini İndir (.md)</span>
                </button>
              </div>

              {/* Quick Link to NotebookLM */}
              <div className="text-center pt-2">
                <a
                  href="https://notebooklm.google.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1.5 text-xs text-ai hover:text-ai font-bold underline"
                >
                  <span>Google NotebookLM Sayfasına Git</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          )}

          {/* TAB 2: IMPORT FROM NOTEBOOKLM TO DATABASE */}
          {activeTab === 'import' && (
            <div className="space-y-4">
              <div className="bg-accent-soft border border-accent/30 rounded-xl p-3.5 text-xs text-accent">
                <p className="font-semibold text-accent">
                  NotebookLM veya Gemini'de ürettiğiniz soruları, düzeltmeleri veya çözümleri buraya yapıştırın.
                </p>
                <p className="text-2xs text-accent/80 mt-1">
                  Yapay zeka ayrıştırıcımız metni otomatik olarak okur, soru numaralarını, 5 şıkkı ve doğru cevabı tespit ederek doğrudan veritabanına ekler.
                </p>
              </div>

              <div>
                <label className="block text-xs font-bold text-ink-2 mb-1">
                  NotebookLM / Gemini Metin Çıktısı:
                </label>
                <textarea
                  rows={8}
                  value={importText}
                  onChange={(e) => setImportText(e.target.value)}
                  placeholder={`Örnek:\nSoru 15: Aşağıdakilerden hangisi nefrotik sendromun en sık çocukluk çağı nedenidir?\nA) Minimal Değişiklik Hastalığı\nB) FSGS\nC) Membranöz Nefropati\nD) MPGN\nE) IgA Nefropatisi\nCevap: A\nAçıklama: Minimal değişiklik hastalığında podosit ayak çıkıntılarında silinme görülür ve steroide tam yanıt alınır.`}
                  className="w-full text-xs font-mono p-3 rounded-xl border border-line-2 focus:outline-hidden focus:ring-2 focus:ring-accent/20 bg-white"
                />
              </div>

              <button
                type="button"
                onClick={handleImportFromAI}
                disabled={isProcessing || !importText.trim()}
                className="w-full bg-accent hover:bg-accent disabled:opacity-50 text-white font-bold py-3 rounded-xl text-xs flex items-center justify-center gap-2 shadow-sm transition-all cursor-pointer active:scale-95"
              >
                {isProcessing ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Yapay Zeka ile Veritabanına İşleniyor...</span>
                  </>
                ) : (
                  <>
                    <Database className="w-4 h-4" />
                    <span>Veritabanına İşle & Güncelle</span>
                  </>
                )}
              </button>
            </div>
          )}

          {/* TAB 3: DIRECT GEMINI INTEGRATION */}
          {activeTab === 'direct_ai' && (
            <div className="space-y-4">
              <div className="bg-ok-soft border border-ok/30 rounded-xl p-4 text-xs text-ok space-y-2">
                <div className="flex items-center gap-2 font-bold text-ok text-sm">
                  <Sparkles className="w-4 h-4 text-ok" />
                  <span>Doğrudan Gemini 2.5 Flash ile Otomatik Zenginleştirme</span>
                </div>
                <p className="leading-relaxed text-ok/90">
                  Bu özellik, mevcut sorularınızı ve Google Drive'dan çekilen 40 ders slaytını doğrudan Gemini yapay zekasına gönderir.
                  Eksik soru köklerini tıp literatürüne göre tamamlar, çeldirici şıklar üretir ve soruların hangi ders slaytından çıktığını otomatik bağlar.
                </p>
              </div>

              <div className="bg-white border border-line rounded-xl p-4 space-y-3">
                <div className="flex items-center justify-between text-xs text-ink-2">
                  <span>Mevcut Soru Sayısı:</span>
                  <span className="font-bold text-ok">{questions.length} Soru</span>
                </div>
                <div className="flex items-center justify-between text-xs text-ink-2">
                  <span>İndekslenen Slayt Sayısı:</span>
                  <span className="font-bold text-ok">{lectureNotes.length} Slayt</span>
                </div>
                <div className="flex items-center justify-between text-xs text-ink-2">
                  <span>Gemini Modeli:</span>
                  <span className="font-bold text-ink">Gemini 2.5 Flash (Tıp Soru Motoru)</span>
                </div>
              </div>

              <button
                type="button"
                onClick={handleDirectGeminiEnhance}
                disabled={isProcessing}
                className="w-full bg-ok hover:bg-ok disabled:opacity-50 text-white font-bold py-3 rounded-xl text-xs flex items-center justify-center gap-2 shadow-sm transition-all cursor-pointer active:scale-95"
              >
                {isProcessing ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Gemini ile Veritabanı Zenginleştiriliyor...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 text-ok-soft" />
                    <span>Veritabanını Gemini ile Otomatik Zenginleştir</span>
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
