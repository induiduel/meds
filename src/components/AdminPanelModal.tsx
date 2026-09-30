import React, { useState } from 'react';
import { 
  X, 
  ShieldCheck, 
  Database, 
  Download, 
  Upload, 
  RotateCcw, 
  Trash2, 
  Edit3, 
  CheckCircle2, 
  AlertTriangle,
  Search,
  Sparkles,
  Zap,
  FilePlus,
  BookOpen
} from 'lucide-react';
import { QuestionItem, Committee } from '../types';
import { AdminEditQuestionModal } from './AdminEditQuestionModal';
import { AdminPastExamImporterModal } from './AdminPastExamImporterModal';
import { InfoPopover } from './InfoPopover';
import { ApiService } from '../services/api';

interface AdminPanelModalProps {
  isOpen: boolean;
  onClose: () => void;
  adminEmail: string;
  committees: Committee[];
  questions: QuestionItem[];
  selectedCommitteeId: string;
  onRefreshData: () => Promise<void>;
}

export const AdminPanelModal: React.FC<AdminPanelModalProps> = ({
  isOpen,
  onClose,
  adminEmail,
  committees,
  questions,
  selectedCommitteeId,
  onRefreshData,
}) => {
  const [editingQuestion, setEditingQuestion] = useState<QuestionItem | null>(null);
  const [isPastExamImporterOpen, setIsPastExamImporterOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  // Destructive confirmation state
  const [confirmDialog, setConfirmDialog] = useState<{
    isOpen: boolean;
    title: string;
    description: string;
    onConfirm: () => Promise<void>;
  } | null>(null);

  if (!isOpen) return null;

  const currentCommitteeQuestions = questions.filter(
    (q) => !selectedCommitteeId || q.committeeId === selectedCommitteeId
  );

  const filteredQuestions = currentCommitteeQuestions.filter(
    (q) =>
      q.questionNumber.toString().includes(searchQuery) ||
      q.topic.toLowerCase().includes(searchQuery.toLowerCase()) ||
      q.discipline.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Handle Question Edit
  const handleSaveQuestion = async (updated: Partial<QuestionItem>) => {
    if (!editingQuestion) return;
    try {
      await ApiService.adminUpdateQuestion(adminEmail, editingQuestion.id, updated);
      setActionMessage(`Soru #${editingQuestion.questionNumber} başarıyla güncellendi.`);
      await onRefreshData();
    } catch (e: any) {
      alert('Hata: ' + e.message);
    }
  };

  // Handle Question Delete with explicit confirmation
  const handleDeleteQuestion = (question: QuestionItem) => {
    setConfirmDialog({
      isOpen: true,
      title: `Soru #${question.questionNumber} Silinsin mi?`,
      description: `Bu soruyu ve öğrencilerin girdiği tüm hafıza parçalarını kalıcı olarak silmek üzeresiniz. Bu işlem geri alınamaz.`,
      onConfirm: async () => {
        setIsProcessing(true);
        try {
          await ApiService.adminDeleteQuestion(adminEmail, question.id);
          setActionMessage(`Soru #${question.questionNumber} silindi.`);
          await onRefreshData();
        } finally {
          setIsProcessing(false);
          setConfirmDialog(null);
        }
      },
    });
  };

  // Export JSON Backup
  const handleExportJson = async () => {
    try {
      const data = await ApiService.adminExportDb();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `medsoru_database_backup_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e: any) {
      alert('Dışa aktarma hatası: ' + e.message);
    }
  };

  // Import JSON Backup with confirmation
  const handleImportFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (event) => {
      try {
        const json = JSON.parse(event.target?.result as string);
        setConfirmDialog({
          isOpen: true,
          title: 'Veritabanı Yedeği İçe Aktarılsın mı?',
          description: `Seçilen JSON dosyasındaki veriler mevcut veritabanının üzerine yazılacaktır (${json.questions?.length || 0} soru). Onaylıyor musunuz?`,
          onConfirm: async () => {
            setIsProcessing(true);
            try {
              await ApiService.adminImportDb(adminEmail, json);
              setActionMessage('Veritabanı başarıyla içe aktarıldı.');
              await onRefreshData();
            } finally {
              setIsProcessing(false);
              setConfirmDialog(null);
            }
          },
        });
      } catch (err) {
        alert('Geçersiz JSON dosyası.');
      }
    };
    reader.readAsText(file);
  };

  // Reset to seed with confirmation
  const handleResetDatabase = () => {
    setConfirmDialog({
      isOpen: true,
      title: 'Veritabanı Sıfırlansın mı?',
      description: 'Tüm sorular sıfırlanacak ve orijinal tıp fakültesi başlangıç verileri geri yüklenecektir. Bu işlem geri alınamaz.',
      onConfirm: async () => {
        setIsProcessing(true);
        try {
          await ApiService.adminResetDb(adminEmail);
          setActionMessage('Veritabanı sıfırlandı.');
          await onRefreshData();
        } finally {
          setIsProcessing(false);
          setConfirmDialog(null);
        }
      },
    });
  };

  // Helper to fill sample high-confidence questions for the 80/100 threshold test
  const handleSimulateThreshold = () => {
    setConfirmDialog({
      isOpen: true,
      title: 'Drive Eşik Test Verisi Oluşturulsun mu?',
      description: `Sistemde 100 soru oluşturulacak ve 80 tanesi %95 güven oranıyla tamamlanacaktır. Böylece "100 sorunun %80'i %90 doğruluğa ulaştığında otomatik Drive kaydı" özelliğini hemen test edebilirsiniz.`,
      onConfirm: async () => {
        setIsProcessing(true);
        try {
          const disciplines = ['Farmakoloji', 'Patoloji', 'Tıbbi Mikrobiyoloji', 'Dahiliye', 'Pediatri'];
          const sampleTopics = [
            'ACE İnhibitörleri ve Kuru Öksürük',
            'Akut Koroner Sendrom Biyobelirteçleri',
            'Legionella Atipik Pnömoni ve BCYE Agar',
            'Streptococcus pyogenes ve ASO Titresi',
            'Miyokard Enfarktüsü Histopatolojisi',
            'Metotreksat Etki Mekanizması ve Toksisite',
            'Graves Hastalığı ve TSH Reseptör Antikorları',
            'Cushing Sendromu Deksametazon Baskılama Testi',
            'Aplastik Anemi Kemik İliği Biyopsisi',
            'Diyabetik Ketoasidoz Tedavi Protokolü',
          ];

          const generatedQuestions: QuestionItem[] = [];
          for (let i = 1; i <= 100; i++) {
            const isHighConfidence = i <= 82; // 82% >= 90% confidence
            const disc = disciplines[i % disciplines.length];
            const topic = `${disc}: ${sampleTopics[i % sampleTopics.length]} (#${i})`;
            
            generatedQuestions.push({
              id: `q-auto-${i}`,
              committeeId: selectedCommitteeId,
              questionNumber: i,
              discipline: disc,
              topic,
              status: isHighConfidence ? 'completed' : 'gathering',
              claimedAnswer: 'C',
              tags: [disc, 'Kurul Sorusu'],
              createdAt: new Date().toISOString(),
              updatedAt: new Date().toISOString(),
              fragments: [
                {
                  id: `f-auto-${i}`,
                  author: 'Stj. Dr. Eren',
                  text: `Kurul sınavı #${i} vaka sorusu: Klinik tablo ve laboratuvar bulguları verilmişti.`,
                  type: 'stem',
                  timestamp: new Date().toISOString(),
                  upvotes: 8,
                },
              ],
              options: [
                { key: 'A', text: 'Seçenek A çeldiricisi', upvotes: 2 },
                { key: 'B', text: 'Seçenek B çeldiricisi', upvotes: 1 },
                { key: 'C', text: 'Seçenek C (Doğru Yanıt)', upvotes: 14 },
                { key: 'D', text: 'Seçenek D çeldiricisi', upvotes: 3 },
                { key: 'E', text: 'Seçenek E çeldiricisi', upvotes: 1 },
              ],
              reconstruction: isHighConfidence
                ? {
                    stem: `52 yaşında erkek hasta acil servise tipik semptomlarla başvuruyor. Yapılan laboratuvar ve klinik incelemeler neticesinde bu tabloyu en iyi açıklayan tanı ve etki mekanizması aşağıdakilerden hangisidir? (Soru #${i})`,
                    options: [
                      { key: 'A', text: 'A seçeneği patofizyolojik çeldirici', isAiFilled: false },
                      { key: 'B', text: 'B seçeneği farmakolojik çeldirici', isAiFilled: false },
                      { key: 'C', text: 'C seçeneği spesifik klinik ve moleküler mekanizma (Hedef Yanıt)', isAiFilled: false },
                      { key: 'D', text: 'D seçeneği histopatolojik çeldirici', isAiFilled: true },
                      { key: 'E', text: 'E seçeneği ayırıcı tanı alternatifi', isAiFilled: true },
                    ],
                    correctAnswer: 'C',
                    explanation: `Tıp fakültesi kurul sınavı düzeyinde detaylı tıbbi gerekçe: Robbins Patoloji ve Katzung Farmakoloji referans alınarak patofizyolojik mekanizma doğrulanmıştır. (Soru #${i})`,
                    confidenceScore: 95,
                    notesAndDiscrepancies: 'Tüm öğrenci hafızaları %100 uyumludur. Eşik testi için hazırlanmıştır.',
                    lastUpdated: new Date().toISOString(),
                  }
                : undefined,
            });
          }

          await ApiService.adminImportDb(adminEmail, {
            committees,
            questions: generatedQuestions,
          });

          setActionMessage('100 soru hazırlandı (82 tanesi %95 güvenli). Otomatik Drive eşiği karşılandı!');
          await onRefreshData();
        } finally {
          setIsProcessing(false);
          setConfirmDialog(null);
        }
      },
    });
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl max-w-4xl w-full shadow-2xl border border-slate-200 overflow-hidden my-6 flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="bg-slate-900 text-white p-5 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-400 border border-teal-400/30 flex items-center justify-center">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-base">MedSoru Yönetici & Veritabanı Kontrol Paneli</h3>
                <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full">
                  Admin Yetkili
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Hesap: <strong className="text-teal-300">{adminEmail}</strong> (Tam Yetki)
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Action alert message */}
        {actionMessage && (
          <div className="bg-teal-50 border-b border-teal-200 px-5 py-2 text-xs text-teal-900 flex items-center justify-between">
            <span className="flex items-center gap-1.5 font-medium">
              <CheckCircle2 className="w-4 h-4 text-teal-600" />
              {actionMessage}
            </span>
            <button
              onClick={() => setActionMessage(null)}
              className="text-teal-600 hover:text-teal-800 text-xs font-bold"
            >
              Kapat
            </button>
          </div>
        )}

        {/* Main Body */}
        <div className="p-6 space-y-6 overflow-y-auto flex-1 text-xs">
          {/* Quick Database Operations Bar */}
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h4 className="font-bold text-slate-900 flex items-center gap-2 text-sm">
                  <Database className="w-4 h-4 text-teal-600" />
                  Veritabanı Yedekleme & Geri Yükleme
                </h4>
                <p className="text-slate-500 text-[11px] mt-0.5">
                  Tüm soru havuzunu tek tıkla JSON formatında indirebilir, geri yükleyebilir veya eşik testi çalıştırabilirsiniz.
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <button
                  onClick={handleExportJson}
                  className="bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer shadow-2xs"
                >
                  <Download className="w-3.5 h-3.5 text-slate-500" />
                  <span>JSON İndir</span>
                </button>

                <label className="bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer shadow-2xs">
                  <Upload className="w-3.5 h-3.5 text-slate-500" />
                  <span>JSON Yükle</span>
                  <input
                    type="file"
                    accept=".json"
                    onChange={handleImportFile}
                    className="hidden"
                  />
                </label>

                <button
                  onClick={handleResetDatabase}
                  className="bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer"
                >
                  <RotateCcw className="w-3.5 h-3.5 text-rose-600" />
                  <span>Sıfırla</span>
                </button>
              </div>
            </div>

            {/* Past Exam Question Importer Tool (Admin Tool) */}
            <div className="pt-2 border-t border-slate-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-gradient-to-r from-teal-50 to-emerald-50 -mx-4 -mb-4 p-4 rounded-b-xl border-t border-teal-100">
              <div className="space-y-0.5">
                <div className="flex items-center gap-1.5">
                  <span className="font-bold text-teal-950 text-xs flex items-center gap-1">
                    <Sparkles className="w-3.5 h-3.5 text-teal-700" />
                    Çıkmış Soru Yükleme & Yapay Zeka Ayrıştırıcı
                  </span>
                  <InfoPopover title="Çıkmış Soru Aracı Hakkında">
                    <p>
                      Admin olarak geçmiş senelerden (2020-2024 vb.) kısmi veya tam çıkmış sınav sorularını yapıştırabilir veya dosya olarak yükleyebilirsiniz.
                    </p>
                    <p className="mt-1">
                      Yapay Zeka (Gemini); soruların hangi sene, hangi ders, hangi soru numarası ve olası şıklarını otomatik ayrıştırıp standart formata dönüştürür.
                    </p>
                    <p className="mt-1 font-semibold text-teal-900">
                      Veritabanına aktarıldıktan sonra tüm öğrenciler yeni şık önerisi verebilir ve soruları düzenleyebilir.
                    </p>
                  </InfoPopover>
                </div>
                <p className="text-[11px] text-slate-600">
                  Geçmiş senelerin soru dosyalarını yapay zekayla ayrıştırıp veritabanına aktarın; öğrenciler düzenleyebilsin.
                </p>
              </div>

              <button
                type="button"
                onClick={() => setIsPastExamImporterOpen(true)}
                className="bg-gradient-to-r from-teal-700 to-emerald-700 hover:from-teal-800 hover:to-emerald-800 text-white font-bold px-3.5 py-2 rounded-xl flex items-center gap-2 cursor-pointer self-start sm:self-auto shrink-0 shadow-sm text-xs active:scale-95"
              >
                <FilePlus className="w-4 h-4 text-teal-200" />
                <span>Çıkmış Soru Yükleme Aracını Aç</span>
              </button>
            </div>
          </div>

          {/* Question List for Editing / Deletion */}
          <div className="space-y-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <h4 className="font-bold text-slate-900 text-sm">
                Kurul Soruları Yönetimi ({currentCommitteeQuestions.length} Soru)
              </h4>

              <div className="relative max-w-xs w-full">
                <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Soru no, ders veya konu ara..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-8 pr-3 py-1 text-xs text-slate-800"
                />
              </div>
            </div>

            <div className="border border-slate-200 rounded-xl overflow-hidden bg-white">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold text-[11px]">
                    <th className="p-3 w-14">No</th>
                    <th className="p-3">Ders & Konu</th>
                    <th className="p-3">Durum & Güven</th>
                    <th className="p-3">Hafıza Parçaları</th>
                    <th className="p-3 text-right">İşlemler</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filteredQuestions.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="p-6 text-center text-slate-400">
                        Soru bulunamadı.
                      </td>
                    </tr>
                  ) : (
                    filteredQuestions.map((q) => {
                      const hasRec = !!q.reconstruction;
                      return (
                        <tr key={q.id} className="hover:bg-slate-50/70 transition-colors">
                          <td className="p-3 font-bold text-teal-800">#{q.questionNumber}</td>
                          <td className="p-3">
                            <span className="font-semibold text-slate-900 block">{q.topic}</span>
                            <span className="text-[10px] text-slate-500">{q.discipline}</span>
                          </td>
                          <td className="p-3">
                            {hasRec ? (
                              <span className="inline-flex items-center gap-1 bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold px-2 py-0.5 rounded-full text-[10px]">
                                <Sparkles className="w-3 h-3 text-emerald-600" />
                                %{q.reconstruction?.confidenceScore} Güven
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1 bg-amber-50 text-amber-800 border border-amber-200 px-2 py-0.5 rounded-full text-[10px]">
                                Taslak ({q.status})
                              </span>
                            )}
                          </td>
                          <td className="p-3 text-slate-500">
                            {q.fragments.length} parça, {q.options.length} şık
                          </td>
                          <td className="p-3 text-right space-x-1">
                            <button
                              onClick={() => setEditingQuestion(q)}
                              className="p-1.5 text-teal-700 hover:text-teal-900 hover:bg-teal-50 rounded cursor-pointer"
                              title="Soruyu Düzenle"
                            >
                              <Edit3 className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => handleDeleteQuestion(q)}
                              className="p-1.5 text-rose-600 hover:text-rose-800 hover:bg-rose-50 rounded cursor-pointer"
                              title="Soruyu Sil"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between shrink-0">
          <span className="text-[11px] text-slate-500">
            nofrostlife@gmail.com olarak yönetici yetkilerine sahipsiniz.
          </span>
          <button
            onClick={onClose}
            className="bg-slate-800 hover:bg-slate-900 text-white font-semibold px-4 py-1.5 rounded-lg text-xs cursor-pointer"
          >
            Kapat
          </button>
        </div>
      </div>

      {/* Edit Modal */}
      {editingQuestion && (
        <AdminEditQuestionModal
          isOpen={true}
          onClose={() => setEditingQuestion(null)}
          question={editingQuestion}
          adminEmail={adminEmail}
          onSaveQuestion={handleSaveQuestion}
        />
      )}

      {/* Confirmation Dialog (MANDATORY User Confirmation for Destructive Operations) */}
      {confirmDialog && (
        <div className="fixed inset-0 z-60 bg-slate-950/70 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-5 shadow-2xl space-y-4 border border-slate-200">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-full bg-rose-100 text-rose-600 shrink-0">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-slate-900 text-sm">{confirmDialog.title}</h4>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  {confirmDialog.description}
                </p>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setConfirmDialog(null)}
                disabled={isProcessing}
                className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-100 cursor-pointer"
              >
                Vazgeç
              </button>
              <button
                type="button"
                onClick={confirmDialog.onConfirm}
                disabled={isProcessing}
                className="bg-rose-600 hover:bg-rose-700 text-white px-4 py-1.5 rounded-lg text-xs font-bold cursor-pointer disabled:opacity-50"
              >
                {isProcessing ? 'İşleniyor...' : 'Onayla ve Sil/Sıfırla'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Admin Past Exam Importer Modal */}
      <AdminPastExamImporterModal
        isOpen={isPastExamImporterOpen}
        onClose={() => setIsPastExamImporterOpen(false)}
        adminEmail={adminEmail}
        committees={committees}
        selectedCommitteeId={selectedCommitteeId}
        onImportSuccess={async () => {
          await onRefreshData();
          setActionMessage('Çıkmış sorular başarıyla veritabanına aktarıldı ve soru havuzuna eklendi.');
        }}
      />
    </div>
  );
};
