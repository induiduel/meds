import React, { useState, useMemo, useRef } from 'react';
import { confirmText } from '../ui/ConfirmDialog';
import {
  Upload,
  FileText,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  ArrowLeft,
  Table,
  Sparkles,
  Edit3,
  Trash2,
  Search,
  Check,
} from 'lucide-react';
import { toast } from '../ui/Toast';

export interface TargetFieldDef {
  key: string;
  label: string;
  description: string;
  required: boolean;
  type: 'string' | 'options' | 'answer' | 'number';
  synonyms: string[];
}

export const TARGET_FIELDS: TargetFieldDef[] = [
  {
    key: 'stem',
    label: 'Soru Metni (Kökü)',
    description: 'Sorunun ana soru cümlesi veya vaka paragrafı',
    required: true,
    type: 'string',
    synonyms: ['stem', 'question', 'soru', 'sorumetni', 'soru_koku', 'text', 'body', 'questiontext', 'soru_metni']
  },
  {
    key: 'options',
    label: 'Seçenekler (A-E)',
    description: 'Şıklar dizisi veya A, B, C, D, E nesnesi',
    required: true,
    type: 'options',
    synonyms: ['options', 'choices', 'secenekler', 'siklar', 'answers', 'cevaplar', 'optionslist', 'secenek_listesi']
  },
  {
    key: 'correctAnswer',
    label: 'Doğru Cevap',
    description: 'Doğru şıkkın harfi (A, B, C, D veya E)',
    required: true,
    type: 'answer',
    synonyms: ['correctanswer', 'correct_answer', 'dogrucevap', 'dogru_cevap', 'cevap', 'answer', 'key', 'claimedanswer', 'dogru_secenek']
  },
  {
    key: 'explanation',
    label: 'Açıklama & Gerekçe',
    description: 'Fizyopatolojik açıklama, ders notu referansı',
    required: false,
    type: 'string',
    synonyms: ['explanation', 'tibbi_aciklama', 'aciklama', 'rationale', 'gerekce', 'explanationtext', 'cozum']
  },
  {
    key: 'sik_analizi',
    label: 'Şık Analizi (Çürütmeler)',
    description: 'Her seçeneğin neden doğru/yanlış olduğunun analizi',
    required: false,
    type: 'string',
    synonyms: ['sik_analizi', 'optionanalysis', 'sikanalizi', 'analiz', 'optionsanalysis', 'secenek_analizleri']
  },
  {
    key: 'discipline',
    label: 'Ders / Branş',
    description: 'Tıbbi Patoloji, Farmakoloji, Kadın Doğum vb.',
    required: false,
    type: 'string',
    synonyms: ['discipline', 'ders', 'brans', 'anabilimdali', 'bolum', 'subject']
  },
  {
    key: 'topic',
    label: 'Konu / Başlık',
    description: 'İlgili dersin alt konu başlığı',
    required: false,
    type: 'string',
    synonyms: ['topic', 'konu', 'altbaslik', 'subtopic']
  },
  {
    key: 'kurul',
    label: 'Kurul No',
    description: 'Dönem 3 Kurul numarası (1, 2, 3, 4, 5, 6)',
    required: false,
    type: 'number',
    synonyms: ['kurul', 'committee', 'committeeid', 'blok', 'kurulno']
  },
  {
    key: 'examYear',
    label: 'Sınav Yılı',
    description: 'Sınavın ait olduğu akademik yıl (örn: 2023-2024)',
    required: false,
    type: 'string',
    synonyms: ['examyear', 'yil', 'donem', 'year', 'sinavyili']
  },
  {
    key: 'questionNumber',
    label: 'Soru Numarası',
    description: 'Sınav kitapçığındaki soru sırası',
    required: false,
    type: 'number',
    synonyms: ['questionnumber', 'soruno', 'no', 'number', 'qnum', 'sorunumarasi']
  },
  {
    key: 'id',
    label: 'Soru ID',
    description: 'Mevcut soru güncellenecekse sistem ID kütüğü',
    required: false,
    type: 'string',
    synonyms: ['id', 'qid', 'questionid']
  }
];

export interface NormalizedQuestion {
  id?: string;
  stem: string;
  options: Array<{ key: string; text: string; isCorrect: boolean }>;
  correctAnswer: string;
  explanation?: string;
  sik_analizi?: any;
  discipline?: string;
  topic?: string;
  kurul?: number | string;
  examYear?: string;
  questionNumber?: number;
  [key: string]: any;
}

export interface ValidationIssue {
  field: string;
  message: string;
  severity: 'error' | 'warning';
}

export interface RowValidationResult {
  row: NormalizedQuestion;
  index: number;
  isValid: boolean;
  issues: ValidationIssue[];
}

export interface FlatfileOnboardingProps {
  initialRawData?: any;
  targetMode?: 'notebooklm_alternative' | 'database_direct';
  defaultCommitteeId?: string;
  defaultExamYear?: string;
  onComplete: (questions: NormalizedQuestion[], meta: { title: string; count: number; validCount: number }) => Promise<void> | void;
  onCancel?: () => void;
  isSubmitting?: boolean;
}

export const FlatfileDataOnboarding: React.FC<FlatfileOnboardingProps> = ({
  initialRawData,
  targetMode = 'notebooklm_alternative',
  defaultCommitteeId = '1',
  defaultExamYear = '2023-2024',
  onComplete,
  onCancel,
  isSubmitting = false
}) => {
  // Wizard steps: 1: Upload, 2: Map Columns, 3: Validate & Edit Grid, 4: Finish
  const [step, setStep] = useState<'upload' | 'mapping' | 'grid'>('upload');

  // Step 1: Input text / file
  const [rawText, setRawText] = useState<string>('');
  const [loadedFileName, setLoadedFileName] = useState<string>('');
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Raw parsed records from Step 1
  const [rawRecords, setRawRecords] = useState<any[]>([]);
  const [detectedSourceKeys, setDetectedSourceKeys] = useState<string[]>([]);

  // Step 2: Key mapping (targetFieldKey -> sourceRawKey)
  const [fieldMappings, setFieldMappings] = useState<Record<string, string>>({});

  // Step 3: Grid search & filter
  const [filterMode, setFilterMode] = useState<'all' | 'errors' | 'valid'>('all');
  const [gridSearch, setGridSearch] = useState('');
  const [editingRowIndex, setEditingRowIndex] = useState<number | null>(null);

  // Batch override tools
  const [batchKurul, setBatchKurul] = useState<string>('');
  const [batchYear, setBatchYear] = useState<string>('');
  const [batchDiscipline, setBatchDiscipline] = useState<string>('');

  // Auto-init if initialRawData is provided
  React.useEffect(() => {
    if (initialRawData) {
      processRawData(initialRawData);
    }
  }, [initialRawData]);

  // Clean and parse text / JSON
  const processRawData = (data: any, fileName?: string) => {
    try {
      let parsed = data;
      if (typeof data === 'string') {
        let str = data.trim();
        const codeMatch = str.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
        if (codeMatch) str = codeMatch[1];
        parsed = JSON.parse(str);
      }

      let items: any[] = [];
      if (Array.isArray(parsed)) {
        items = parsed;
      } else if (parsed && typeof parsed === 'object') {
        if (Array.isArray(parsed.questions)) items = parsed.questions;
        else if (Array.isArray(parsed.corrections)) items = parsed.corrections;
        else if (Array.isArray(parsed.data)) items = parsed.data;
        else if (parsed.stem || parsed.question || parsed.soru) items = [parsed];
        else {
          // Flatten dictionary of questions
          const vals = Object.values(parsed);
          if (vals.length > 0 && typeof vals[0] === 'object') {
            items = vals;
          }
        }
      }

      if (items.length === 0) {
        toast.error('Geçerli bir veri nesnesi veya soru dizisi bulunamadı.');
        return;
      }

      setRawRecords(items);
      if (fileName) setLoadedFileName(fileName);

      // Collect all unique keys across all items
      const keysSet = new Set<string>();
      items.forEach((item) => {
        if (item && typeof item === 'object') {
          Object.keys(item).forEach((k) => keysSet.add(k));
        }
      });
      const allKeys = Array.from(keysSet);
      setDetectedSourceKeys(allKeys);

      // Auto-match target fields to source keys using synonyms
      const initialMap: Record<string, string> = {};
      TARGET_FIELDS.forEach((tf) => {
        const matchedKey = allKeys.find((sourceKey) => {
          const sLower = sourceKey.toLowerCase().replace(/[^a-z0-9]/g, '');
          return tf.synonyms.some((syn) => syn.toLowerCase().replace(/[^a-z0-9]/g, '') === sLower);
        });
        if (matchedKey) {
          initialMap[tf.key] = matchedKey;
        }
      });

      // Special fallback: if reconstruction object exists, check inside it
      if (!initialMap.stem && allKeys.includes('reconstruction')) {
        initialMap.stem = 'reconstruction';
      }

      setFieldMappings(initialMap);
      setStep('mapping');
      toast.success(`${items.length} kayıt tespit edildi. Kolon eşleştirmelerini inceleyin.`);
    } catch (err: any) {
      toast.error('Veri ayrıştırılamadı: ' + err.message);
    }
  };

  const handleFileUpload = (file: File) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      setRawText(content);
      processRawData(content, file.name);
    };
    reader.onerror = () => toast.error('Dosya okunamadı!');
    reader.readAsText(file, 'UTF-8');
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFileUpload(file);
  };

  // Convert raw records into normalized questions according to field mappings
  const normalizedRecords: NormalizedQuestion[] = useMemo(() => {
    return rawRecords.map((item, idx) => {
      // 1. Stem
      const stemKey = fieldMappings.stem;
      let rawStem = stemKey ? item[stemKey] : undefined;
      if (!rawStem && item.reconstruction?.stem) rawStem = item.reconstruction.stem;
      if (typeof rawStem === 'object' && rawStem !== null) {
        rawStem = rawStem.stem || rawStem.text || rawStem.question || JSON.stringify(rawStem);
      }
      const stem = String(rawStem || item.stem || item.question || item.soru || '').trim();

      // 2. Correct Answer
      const ansKey = fieldMappings.correctAnswer;
      let rawAns = ansKey ? item[ansKey] : undefined;
      if (!rawAns && item.reconstruction?.correctAnswer) rawAns = item.reconstruction.correctAnswer;
      const ansStr = String(rawAns || item.correctAnswer || item.claimedAnswer || 'A').toUpperCase().trim();
      const ansMatch = ansStr.match(/[A-E]/);
      const correctAnswer = ansMatch ? ansMatch[0] : 'A';

      // 3. Options
      const optKey = fieldMappings.options;
      let rawOpts = optKey ? item[optKey] : undefined;
      if (!rawOpts && item.reconstruction?.options) rawOpts = item.reconstruction.options;
      if (!rawOpts) rawOpts = item.options || item.secenekler || item.siklar;

      const keys = ['A', 'B', 'C', 'D', 'E'];
      let normOpts: Array<{ key: string; text: string; isCorrect: boolean }> = [];

      if (Array.isArray(rawOpts)) {
        normOpts = rawOpts.map((opt, oIdx) => {
          const fallbackK = keys[oIdx] || 'A';
          if (typeof opt === 'string') {
            const m = opt.match(/^\s*([A-Ea-e])[\).\s:-]+(.*)$/);
            const k = (m ? m[1].toUpperCase() : fallbackK);
            const text = (m ? m[2] : opt).trim();
            return { key: k, text, isCorrect: k === correctAnswer };
          } else if (typeof opt === 'object' && opt !== null) {
            const k = String(opt.key || opt.label || fallbackK).toUpperCase();
            const text = String(opt.text || opt.content || opt.value || '').trim();
            const isCor = opt.isCorrect !== undefined ? Boolean(opt.isCorrect) : k === correctAnswer;
            return { key: k, text, isCorrect: isCor };
          }
          return { key: fallbackK, text: String(opt || ''), isCorrect: fallbackK === correctAnswer };
        });
      } else if (typeof rawOpts === 'object' && rawOpts !== null) {
        normOpts = keys
          .filter((k) => rawOpts[k] !== undefined || rawOpts[k.toLowerCase()] !== undefined)
          .map((k) => {
            const text = String(rawOpts[k] ?? rawOpts[k.toLowerCase()] ?? '').trim();
            return { key: k, text, isCorrect: k === correctAnswer };
          });
      }

      // Ensure at least A-E placeholders if completely empty
      if (normOpts.length === 0) {
        normOpts = keys.map((k) => ({ key: k, text: '', isCorrect: k === correctAnswer }));
      }

      // 4. Explanation
      const expKey = fieldMappings.explanation;
      const rawExp = expKey ? item[expKey] : undefined;
      const explanation = String(rawExp || item.explanation || item.tibbi_aciklama || item.aciklama || item.reconstruction?.explanation || '').trim();

      // 5. Sik analizi
      const anaKey = fieldMappings.sik_analizi;
      const sik_analizi = anaKey ? item[anaKey] : (item.sik_analizi || item.denetleyiciSurumu?.sik_analizi || '');

      // 6. Discipline & Topic
      const discKey = fieldMappings.discipline;
      const topKey = fieldMappings.topic;
      const discipline = String(discKey ? item[discKey] : (item.discipline || item.ders || '')).trim();
      const topic = String(topKey ? item[topKey] : (item.topic || item.konu || '')).trim();

      // 7. Kurul & Year & QuestionNumber
      const kurulKey = fieldMappings.kurul;
      const yearKey = fieldMappings.examYear;
      const qNumKey = fieldMappings.questionNumber;
      const idKey = fieldMappings.id;

      const kurul = kurulKey ? item[kurulKey] : (item.kurul || defaultCommitteeId);
      const examYear = String(yearKey ? item[yearKey] : (item.examYear || defaultExamYear));
      const questionNumber = Number(qNumKey ? item[qNumKey] : (item.questionNumber || idx + 1));
      const id = String(idKey ? item[idKey] : (item.id || '')).replace(/^q:/i, '').trim();

      return {
        ...item,
        id: id || undefined,
        stem,
        options: normOpts,
        correctAnswer,
        explanation: explanation || undefined,
        sik_analizi: sik_analizi || undefined,
        discipline: discipline || undefined,
        topic: topic || undefined,
        kurul: kurul ? Number(String(kurul).replace(/[^0-9]/g, '')) || 1 : 1,
        examYear,
        questionNumber: isNaN(questionNumber) ? idx + 1 : questionNumber
      };
    });
  }, [rawRecords, fieldMappings, defaultCommitteeId, defaultExamYear]);

  // Validation engine for Step 3 Grid
  const validatedRows: RowValidationResult[] = useMemo(() => {
    return normalizedRecords.map((row, index) => {
      const issues: ValidationIssue[] = [];

      // Stem check
      if (!row.stem || row.stem.trim().length < 5) {
        issues.push({
          field: 'stem',
          message: 'Soru metni çok kısa veya boş.',
          severity: 'error'
        });
      }

      // Options check
      const validOptions = row.options.filter((o) => o.text && o.text.trim().length > 0);
      if (validOptions.length < 2) {
        issues.push({
          field: 'options',
          message: `En az 2 seçenek gereklidir (Şu an: ${validOptions.length}).`,
          severity: 'error'
        });
      }

      // Correct answer check
      if (!row.correctAnswer || !['A', 'B', 'C', 'D', 'E'].includes(row.correctAnswer)) {
        issues.push({
          field: 'correctAnswer',
          message: 'Doğru seçenek A, B, C, D veya E olmalıdır.',
          severity: 'error'
        });
      } else {
        const hasCorrectInOpts = validOptions.some((o) => o.key === row.correctAnswer);
        if (!hasCorrectInOpts && validOptions.length > 0) {
          issues.push({
            field: 'correctAnswer',
            message: `Doğru seçenek (${row.correctAnswer}) seçenekler listesinde bulunamadı.`,
            severity: 'error'
          });
        }
      }

      // Explanation warning
      if (!row.explanation || row.explanation.trim().length < 5) {
        issues.push({
          field: 'explanation',
          message: 'Tıbbi açıklama veya gerekçe eksik.',
          severity: 'warning'
        });
      }

      const hasErrors = issues.some((i) => i.severity === 'error');
      return {
        row,
        index,
        isValid: !hasErrors,
        issues
      };
    });
  }, [normalizedRecords]);

  // Filtered rows for grid
  const displayedRows = useMemo(() => {
    return validatedRows.filter((v) => {
      if (filterMode === 'errors' && v.isValid) return false;
      if (filterMode === 'valid' && !v.isValid) return false;
      if (gridSearch.trim()) {
        const q = gridSearch.toLowerCase();
        const mStem = v.row.stem.toLowerCase().includes(q);
        const mExp = v.row.explanation?.toLowerCase().includes(q);
        const mDisc = v.row.discipline?.toLowerCase().includes(q);
        return mStem || mExp || mDisc;
      }
      return true;
    });
  }, [validatedRows, filterMode, gridSearch]);

  const validCount = useMemo(() => validatedRows.filter((r) => r.isValid).length, [validatedRows]);
  const errorCount = validatedRows.length - validCount;

  // Inline edit row updater
  const handleUpdateRecord = (rowIndex: number, updatedFields: Partial<NormalizedQuestion>) => {
    setRawRecords((prev) => {
      const copy = [...prev];
      copy[rowIndex] = { ...copy[rowIndex], ...updatedFields };
      return copy;
    });
  };

  // Batch actions
  const applyBatchToAll = (field: keyof NormalizedQuestion, value: any) => {
    if (!value) return;
    setRawRecords((prev) => {
      return prev.map((item) => ({ ...item, [field]: value }));
    });
    toast.success(`Tüm kayıtlara "${value}" değeri uygulandı.`);
  };

  const handleFinish = async () => {
    if (errorCount > 0) {
      if (!(await confirmText(`${errorCount} adet soruda eksik veya hatalı alan tespit edildi. Yine de içe aktarıma devam etmek istiyor musunuz?`))) {
        return;
      }
    }
    const cleanQuestions = normalizedRecords;
    const title = loadedFileName
      ? loadedFileName.replace(/\.[^/.]+$/, '').replace(/[_-]/g, ' ')
      : `${cleanQuestions.length} Çıkmış Soru Paketi`;

    await onComplete(cleanQuestions, {
      title,
      count: cleanQuestions.length,
      validCount
    });
  };

  return (
    <div className="flex flex-col h-full min-h-[580px] bg-card rounded-2xl border border-border shadow-xl overflow-hidden">
      {/* Top Header & Flatfile Stepper */}
      <div className="flex flex-wrap items-center justify-between p-4 border-b border-border bg-surface-1 gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-primary/10 text-primary">
            <Table className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xs font-bold tracking-wider uppercase px-1.5 py-0.5 rounded bg-primary/10 text-primary">
                Flatfile Data Onboarding
              </span>
              <span className="text-xs text-ink-3">• Akıllı Şema Eşleme &amp; Doğrulama</span>
            </div>
            <h3 className="text-sm sm:text-base font-bold text-ink">
              {step === 'upload' && '1. Adım: Veri Yükleme & Tespit'}
              {step === 'mapping' && '2. Adım: Kolon & Alan Eşleştirme (Schema Mapping)'}
              {step === 'grid' && '3. Adım: Veri Doğrulama & Tablo Düzenleme (Spreadsheet)'}
            </h3>
          </div>
        </div>

        {/* Stepper Pills */}
        <div className="flex items-center gap-1.5">
          <button
            type="button"
            onClick={() => setStep('upload')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              step === 'upload'
                ? 'bg-primary text-white shadow-xs'
                : 'bg-surface-2 text-ink-3 hover:text-ink'
            }`}
          >
            <span>1. Yükle</span>
          </button>
          <ArrowRight className="w-3.5 h-3.5 text-ink-3" />
          <button
            type="button"
            disabled={rawRecords.length === 0}
            onClick={() => setStep('mapping')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition disabled:opacity-40 ${
              step === 'mapping'
                ? 'bg-primary text-white shadow-xs'
                : 'bg-surface-2 text-ink-3 hover:text-ink'
            }`}
          >
            <span>2. Eşleştir</span>
          </button>
          <ArrowRight className="w-3.5 h-3.5 text-ink-3" />
          <button
            type="button"
            disabled={rawRecords.length === 0}
            onClick={() => setStep('grid')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition disabled:opacity-40 ${
              step === 'grid'
                ? 'bg-primary text-white shadow-xs'
                : 'bg-surface-2 text-ink-3 hover:text-ink'
            }`}
          >
            <span>3. Doğrula &amp; Düzenle ({rawRecords.length})</span>
          </button>
        </div>
      </div>

      {/* Main Body */}
      <div className="flex-1 p-4 sm:p-6 overflow-y-auto">
        {/* STEP 1: UPLOAD & PASTE */}
        {step === 'upload' && (
          <div className="flex flex-col gap-5 max-w-4xl mx-auto">
            <div className="p-4 bg-primary/5 border border-primary/20 rounded-xl flex items-start gap-3 text-xs text-primary">
              <Sparkles className="w-5 h-5 shrink-0 mt-0.5" />
              <div className="leading-relaxed">
                <strong>Flatfile Akıllı Veri Onboarding Sistemi:</strong> NotebookLM, ChatGPT, Excel veya arşiv dosyalarınızdaki JSON/CSV verilerini doğrudan yükleyin. Sistem alan adlarını (kök, şıklar, doğru cevap vb.) otomatik eşler ve içe aktarmadan önce tablosal doğrulama ızgarasında eksikleri düzeltmenize olanak tanır.
              </div>
            </div>

            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept=".json,.csv,.tsv,.txt,.jsonl,application/json,text/plain"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleFileUpload(file);
              }}
              className="hidden"
            />

            {/* Dropzone */}
            <div
              onDragOver={(e) => {
                e.preventDefault();
                setIsDragging(true);
              }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all flex flex-col items-center justify-center gap-3 ${
                isDragging
                  ? 'border-primary bg-primary/10 scale-[0.99]'
                  : 'border-border hover:border-primary/60 hover:bg-surface-2/60 bg-surface-1/40'
              }`}
            >
              <div className="p-4 rounded-full bg-primary/10 text-primary">
                <Upload className="w-8 h-8" />
              </div>
              <div className="flex flex-col items-center gap-1">
                <div className="text-sm font-bold text-ink">
                  Bilgisayarınızdan JSON / CSV Dosyası Seçin
                </div>
                <div className="text-xs text-ink-3">
                  veya dosyayı buraya sürükleyip bırakın (.json, .csv, .txt)
                </div>
              </div>
              <button type="button" className="ms-btn is-sm is-secondary text-xs pointer-events-none mt-1">
                Dosya Gezginini Aç
              </button>
            </div>

            {/* OR Paste Text */}
            <div className="flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold text-ink flex items-center gap-1.5">
                  <FileText className="w-4 h-4 text-primary" />
                  Veya JSON Metnini Doğrudan Yapıştırın
                </label>
                <button
                  type="button"
                  onClick={() => {
                    const sample = [
                      {
                        stem: "Gebelikte fetal virilizasyonu engellemek amacıyla kullanılan steroid aşağıdakilerden hangisidir?",
                        options: [
                          { key: "A", text: "Fludrokortizon" },
                          { key: "B", text: "Androstenedion" },
                          { key: "C", text: "Aldosteron" },
                          { key: "D", text: "Prednizolon" },
                          { key: "E", text: "Deksametazon" }
                        ],
                        correctAnswer: "E",
                        explanation: "Deksametazon plasental 11-beta-HSD2 enzimi tarafından inaktive edilmeden plasentayı geçer.",
                        kurul: 1,
                        discipline: "Kadın Doğum / Perinatoloji"
                      }
                    ];
                    setRawText(JSON.stringify(sample, null, 2));
                    processRawData(sample, 'ornek_soru.json');
                  }}
                  className="text-2xs text-primary hover:underline font-semibold"
                >
                  Örnek Şablonu Doldur
                </button>
              </div>
              <textarea
                rows={8}
                value={rawText}
                onChange={(e) => setRawText(e.target.value)}
                placeholder={`[
  {
    "stem": "Soru metni...",
    "options": [ {"key": "A", "text": "..."}, {"key": "B", "text": "..."} ],
    "correctAnswer": "A",
    "explanation": "Tıbbi açıklama..."
  }
]`}
                className="ms-input font-mono text-xs w-full leading-relaxed"
              />
            </div>

            <div className="flex items-center justify-end gap-2 pt-2">
              {onCancel && (
                <button type="button" onClick={onCancel} className="ms-btn is-sm is-ghost text-xs">
                  İptal
                </button>
              )}
              <button
                type="button"
                disabled={!rawText.trim()}
                onClick={() => processRawData(rawText, 'pasted_data.json')}
                className="ms-btn is-sm is-primary text-xs flex items-center gap-1.5"
              >
                <span>Veriyi Ayrıştır ve Devam Et</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}

        {/* STEP 2: COLUMN / SCHEMA MAPPING */}
        {step === 'mapping' && (
          <div className="flex flex-col gap-5 max-w-4xl mx-auto">
            <div className="flex flex-wrap items-center justify-between p-4 bg-surface-1 border border-border rounded-xl gap-3">
              <div>
                <h4 className="text-sm font-bold text-ink">Kolon &amp; Alan Eşleştirme Masası</h4>
                <p className="text-xs text-ink-3 mt-0.5">
                  İçe aktarılan verideki {detectedSourceKeys.length} farklı alan, sistemin standart tıp sorusu şeması ile eşleştirildi. İhtiyaca göre düzenleyin.
                </p>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <span className="px-2.5 py-1 rounded-full bg-ok/10 text-ok font-semibold border border-ok/20">
                  {Object.keys(fieldMappings).length} / {TARGET_FIELDS.length} Alan Eşleşti
                </span>
              </div>
            </div>

            {/* Mapping Table */}
            <div className="border border-border rounded-xl overflow-hidden bg-card">
              <table className="w-full text-xs text-left">
                <thead className="bg-surface-2/80 text-ink-3 uppercase font-semibold text-2xs border-b border-border">
                  <tr>
                    <th className="p-3 w-1/3">Hedef Sistem Alanı</th>
                    <th className="p-3 w-1/3">Yüklenen Verideki Karşılığı</th>
                    <th className="p-3 w-1/3">Örnek Veri Önizlemesi</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {TARGET_FIELDS.map((tf) => {
                    const selectedSource = fieldMappings[tf.key] || '';
                    const sampleVal = selectedSource && rawRecords[0] ? rawRecords[0][selectedSource] : null;
                    const sampleStr = sampleVal !== undefined && sampleVal !== null
                      ? (typeof sampleVal === 'object' ? JSON.stringify(sampleVal).slice(0, 45) + '...' : String(sampleVal).slice(0, 45))
                      : '—';

                    return (
                      <tr key={tf.key} className="hover:bg-surface-1/50 transition">
                        <td className="p-3">
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-ink">{tf.label}</span>
                            {tf.required && (
                              <span className="text-2xs px-1.5 py-0.2 rounded bg-bad/10 text-bad-text font-bold">
                                Zorunlu
                              </span>
                            )}
                          </div>
                          <div className="text-2xs text-ink-3 mt-0.5">{tf.description}</div>
                        </td>
                        <td className="p-3">
                          <select
                            value={selectedSource}
                            onChange={(e) => {
                              const val = e.target.value;
                              setFieldMappings((prev) => ({
                                ...prev,
                                [tf.key]: val
                              }));
                            }}
                            className={`ms-input text-xs w-full font-medium ${
                              selectedSource ? 'border-primary/50 text-ink' : tf.required ? 'border-warn/50 bg-warn/5' : 'text-ink-3'
                            }`}
                          >
                            <option value="">(Atla / Eşleme Yapma)</option>
                            {detectedSourceKeys.map((sk) => (
                              <option key={sk} value={sk}>
                                {sk}
                              </option>
                            ))}
                          </select>
                        </td>
                        <td className="p-3 text-2xs font-mono text-ink-3 truncate max-w-[220px]">
                          {sampleStr}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            <div className="flex items-center justify-between pt-2">
              <button
                type="button"
                onClick={() => setStep('upload')}
                className="ms-btn is-sm is-ghost text-xs flex items-center gap-1.5"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                Geri (Yükleme)
              </button>
              <button
                type="button"
                onClick={() => setStep('grid')}
                className="ms-btn is-sm is-primary text-xs flex items-center gap-1.5"
              >
                <span>Doğrulama ve Tablo Düzenleyiciye Geç ({rawRecords.length} Kayıt)</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}

        {/* STEP 3: FLATFILE SPREADSHEET VALIDATION GRID */}
        {step === 'grid' && (
          <div className="flex flex-col gap-4">
            {/* Top Stat & Filter Bar */}
            <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 bg-surface-1 border border-border rounded-xl">
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setFilterMode('all')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                    filterMode === 'all' ? 'bg-primary text-white shadow-xs' : 'bg-surface-2 text-ink-3 hover:text-ink'
                  }`}
                >
                  Tümü ({validatedRows.length})
                </button>
                <button
                  type="button"
                  onClick={() => setFilterMode('errors')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
                    filterMode === 'errors' ? 'bg-bad text-white shadow-xs' : 'bg-bad/10 text-bad-text hover:bg-bad/20'
                  }`}
                >
                  <AlertCircle className="w-3.5 h-3.5" />
                  Hatalı ({errorCount})
                </button>
                <button
                  type="button"
                  onClick={() => setFilterMode('valid')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
                    filterMode === 'valid' ? 'bg-ok text-white shadow-xs' : 'bg-ok/10 text-ok hover:bg-ok/20'
                  }`}
                >
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Geçerli ({validCount})
                </button>
              </div>

              {/* Search */}
              <div className="relative min-w-[200px]">
                <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-ink-3" />
                <input
                  type="text"
                  placeholder="Kayıtlar içinde ara..."
                  value={gridSearch}
                  onChange={(e) => setGridSearch(e.target.value)}
                  className="ms-input text-xs pl-8 w-full py-1.5"
                />
              </div>
            </div>

            {/* Quick Batch Tools Toolbar */}
            <div className="flex flex-wrap items-center gap-2 p-2.5 bg-surface-2/60 border border-border rounded-xl text-xs">
              <span className="font-bold text-ink-2 flex items-center gap-1 text-2xs shrink-0 mr-1">
                <Sparkles className="w-3.5 h-3.5 text-primary" /> Toplu Araçlar:
              </span>
              <div className="flex items-center gap-1">
                <input
                  type="text"
                  placeholder="Kurul No (1-6)"
                  value={batchKurul}
                  onChange={(e) => setBatchKurul(e.target.value)}
                  className="ms-input text-xs py-1 w-24"
                />
                <button
                  type="button"
                  onClick={() => applyBatchToAll('kurul', batchKurul)}
                  className="ms-btn is-xs is-secondary text-xs"
                >
                  Uygula
                </button>
              </div>

              <div className="flex items-center gap-1">
                <input
                  type="text"
                  placeholder="Sınav Yılı (2023-2024)"
                  value={batchYear}
                  onChange={(e) => setBatchYear(e.target.value)}
                  className="ms-input text-xs py-1 w-32"
                />
                <button
                  type="button"
                  onClick={() => applyBatchToAll('examYear', batchYear)}
                  className="ms-btn is-xs is-secondary text-xs"
                >
                  Uygula
                </button>
              </div>

              <div className="flex items-center gap-1">
                <input
                  type="text"
                  placeholder="Ders Branşı"
                  value={batchDiscipline}
                  onChange={(e) => setBatchDiscipline(e.target.value)}
                  className="ms-input text-xs py-1 w-36"
                />
                <button
                  type="button"
                  onClick={() => applyBatchToAll('discipline', batchDiscipline)}
                  className="ms-btn is-xs is-secondary text-xs"
                >
                  Uygula
                </button>
              </div>
            </div>

            {/* Interactive Grid Table */}
            <div className="border border-border rounded-xl overflow-x-auto bg-card max-h-[500px]">
              <table className="w-full text-xs text-left border-collapse min-w-[900px]">
                <thead className="bg-surface-2 sticky top-0 z-10 text-2xs text-ink-3 uppercase font-semibold border-b border-border shadow-xs">
                  <tr>
                    <th className="p-2.5 w-12 text-center">#</th>
                    <th className="p-2.5 w-24">Durum</th>
                    <th className="p-2.5 min-w-[280px]">Soru Metni</th>
                    <th className="p-2.5 w-28 text-center">Doğru Şık</th>
                    <th className="p-2.5 min-w-[200px]">Seçenekler</th>
                    <th className="p-2.5 min-w-[220px]">Açıklama</th>
                    <th className="p-2.5 w-24">Kurul / Ders</th>
                    <th className="p-2.5 w-16 text-center">İşlem</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {displayedRows.length === 0 ? (
                    <tr>
                      <td colSpan={8} className="p-8 text-center text-xs text-ink-3">
                        Filtreye uygun soru kaydı bulunamadı.
                      </td>
                    </tr>
                  ) : (
                    displayedRows.map(({ row, index, isValid, issues }) => {
                      const isEditing = editingRowIndex === index;
                      const hasStemError = issues.some((i) => i.field === 'stem');
                      const hasAnsError = issues.some((i) => i.field === 'correctAnswer');
                      const hasOptError = issues.some((i) => i.field === 'options');

                      return (
                        <tr
                          key={index}
                          className={`hover:bg-surface-1/60 transition ${
                            !isValid ? 'bg-bad/5' : ''
                          }`}
                        >
                          {/* Row Index */}
                          <td className="p-2.5 text-center font-mono font-bold text-ink-3">
                            {index + 1}
                          </td>

                          {/* Status Badge */}
                          <td className="p-2.5">
                            {isValid ? (
                              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-2xs font-bold bg-ok/10 text-ok border border-ok/20">
                                <Check className="w-3 h-3" /> Geçerli
                              </span>
                            ) : (
                              <div className="flex flex-col gap-0.5">
                                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-2xs font-bold bg-bad/10 text-bad-text border border-bad/20">
                                  <AlertCircle className="w-3 h-3" /> Hata ({issues.filter(i => i.severity === 'error').length})
                                </span>
                                <div className="text-2xs text-bad-text font-medium truncate max-w-[120px]" title={issues.map(i => i.message).join(' | ')}>
                                  {issues[0]?.message}
                                </div>
                              </div>
                            )}
                          </td>

                          {/* Stem Cell (Inline Editable) */}
                          <td className="p-2.5">
                            {isEditing ? (
                              <textarea
                                rows={3}
                                value={row.stem}
                                onChange={(e) => handleUpdateRecord(index, { stem: e.target.value })}
                                className="ms-input text-xs w-full leading-snug p-2"
                              />
                            ) : (
                              <div
                                onClick={() => setEditingRowIndex(index)}
                                className={`text-xs text-ink line-clamp-3 cursor-pointer hover:bg-surface-2/80 p-1.5 rounded transition ${
                                  hasStemError ? 'border border-bad/40 bg-bad/10' : ''
                                }`}
                                title="Düzenlemek için tıklayın"
                              >
                                {row.stem || <span className="text-bad-text italic">Soru metni boş! (Tıklayın)</span>}
                              </div>
                            )}
                          </td>

                          {/* Correct Answer Dropdown */}
                          <td className="p-2.5 text-center">
                            <select
                              value={row.correctAnswer}
                              onChange={(e) => handleUpdateRecord(index, { correctAnswer: e.target.value })}
                              className={`ms-input text-xs py-1 px-2 font-bold text-center w-16 mx-auto ${
                                hasAnsError ? 'border-bad bg-bad/10 text-bad-text' : 'text-ok bg-ok/10 border-ok/30'
                              }`}
                            >
                              {['A', 'B', 'C', 'D', 'E'].map((k) => (
                                <option key={k} value={k}>
                                  {k}
                                </option>
                              ))}
                            </select>
                          </td>

                          {/* Options Summary */}
                          <td className="p-2.5">
                            <div className={`flex flex-col gap-0.5 max-w-[240px] ${hasOptError ? 'p-1 rounded border border-bad/30 bg-bad/5' : ''}`}>
                              {row.options.map((opt) => (
                                <div key={opt.key} className="text-2xs truncate flex items-center gap-1">
                                  <span className={`w-4 h-4 rounded text-2xs font-bold inline-flex items-center justify-center shrink-0 ${
                                    opt.key === row.correctAnswer ? 'bg-ok text-white' : 'bg-surface-2 text-ink-3'
                                  }`}>
                                    {opt.key}
                                  </span>
                                  <span className="truncate text-ink">{opt.text || <em className="text-ink-3">boş</em>}</span>
                                </div>
                              ))}
                            </div>
                          </td>

                          {/* Explanation */}
                          <td className="p-2.5">
                            {isEditing ? (
                              <textarea
                                rows={3}
                                value={row.explanation || ''}
                                onChange={(e) => handleUpdateRecord(index, { explanation: e.target.value })}
                                className="ms-input text-xs w-full leading-snug p-2"
                              />
                            ) : (
                              <div
                                onClick={() => setEditingRowIndex(index)}
                                className="text-xs text-ink-2 line-clamp-3 cursor-pointer hover:bg-surface-2/80 p-1.5 rounded transition"
                                title="Düzenlemek için tıklayın"
                              >
                                {row.explanation || <span className="text-ink-3 italic">Açıklama yok</span>}
                              </div>
                            )}
                          </td>

                          {/* Kurul / Discipline */}
                          <td className="p-2.5">
                            <div className="flex flex-col gap-1">
                              <span className="text-2xs font-mono px-1.5 py-0.5 rounded bg-surface-2 text-ink-2 w-max">
                                Kurul {row.kurul || 1}
                              </span>
                              <span className="text-2xs text-ink truncate max-w-[110px]" title={row.discipline}>
                                {row.discipline || 'Genel Tıp'}
                              </span>
                            </div>
                          </td>

                          {/* Actions */}
                          <td className="p-2.5 text-center">
                            <div className="flex items-center justify-center gap-1">
                              <button
                                type="button"
                                onClick={() => setEditingRowIndex(isEditing ? null : index)}
                                className="p-1 rounded text-ink-3 hover:text-ink hover:bg-surface-2"
                                title={isEditing ? 'Düzenlemeyi Bitir' : 'Düzenle'}
                              >
                                <Edit3 className="w-3.5 h-3.5" />
                              </button>
                              <button
                                type="button"
                                onClick={async () => {
                                  if ((await confirmText(`Soru #${index + 1} kaydını kaldırmak istediğinize emin misiniz?`))) {
                                    setRawRecords((prev) => prev.filter((_, i) => i !== index));
                                  }
                                }}
                                className="p-1 rounded text-ink-3 hover:text-bad-text hover:bg-bad/10"
                                title="Sil"
                              >
                                <Trash2 className="w-3.5 h-3.5" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>

            {/* Bottom Actions & Summary Bar */}
            <div className="flex flex-wrap items-center justify-between p-4 border-t border-border bg-surface-1 rounded-xl gap-3">
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setStep('mapping')}
                  className="ms-btn is-sm is-ghost text-xs flex items-center gap-1.5"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  Eşleştirmelere Geri Dön
                </button>
                <span className="text-xs text-ink-3">
                  Toplam <strong>{normalizedRecords.length}</strong> soru ({validCount} geçerli, {errorCount} düzeltme bekliyor)
                </span>
              </div>

              <div className="flex items-center gap-2">
                {onCancel && (
                  <button type="button" onClick={onCancel} className="ms-btn is-sm is-ghost text-xs">
                    Vazgeç
                  </button>
                )}
                <button
                  type="button"
                  disabled={isSubmitting || normalizedRecords.length === 0}
                  onClick={handleFinish}
                  className="ms-btn is-sm is-primary text-xs flex items-center gap-1.5 shadow-sm"
                >
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  {isSubmitting
                    ? 'İçe Aktarılıyor...'
                    : targetMode === 'notebooklm_alternative'
                      ? `${normalizedRecords.length} Soruyu Alternatif Olarak Onboard Et`
                      : `${normalizedRecords.length} Soruyu Veritabanına Aktar`}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
