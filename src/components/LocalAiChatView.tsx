import React, { useState, useEffect, useRef } from 'react';
import {
  BotMessageSquare,
  Sparkles,
  Send,
  Cpu,
  Globe,
  HelpCircle,
  Search,
  BookOpen,
  ArrowRight,
  RefreshCw,
  SlidersHorizontal,
  Flame,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  ExternalLink,
  ShieldAlert,
  Clock,
  X,
  Check,
  FileText,
  History
} from 'lucide-react';
import { ApiService } from '../services/api';
import { PageHeader } from './ui/PageHeader';
import { AppUser } from '../services/auth';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  providerUsed?: string;
  planUsed?: string;
  timestamp: string;
  matchedQuestions?: any[];
}

interface LocalAiChatViewProps {
  currentUser: AppUser | null;
  onNavigateToQuestion?: (questionId: string) => void;
}

export const LocalAiChatView: React.FC<LocalAiChatViewProps> = ({
  currentUser,
  onNavigateToQuestion
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>(() => {
    return [
      {
        id: 'msg-welcome',
        role: 'assistant',
        content: `Merhaba! Ben **MedSoru AI Tıp Asistanı**.\n\nBilgisayarındaki yerel donanımı (**RTX 4060 GPU / Ollama**) ve ücretsiz internet yapay zekalarını kullanarak sana kurul sınavlarında rehberlik etmek için buradayım.\n\nNeler yapabilirim:\n- 🔍 **"Soru Dedektifi"**: Sınavda çıkmış ama tam hatırlayamadığın bir sorunun aklında kalan kısımlarını (hasta yaşı, ilaç, semptom) anlat, veri tabanımızdan bulup çıkarayım.\n- 💡 **"Anahtardan Soru Türetme"**: Aklındaki tıbbi terimleri ver, hangi kurul ve ders olduğunu söyleyip 5 şıklı orijinal kurul soruları yazayım.\n- 🧬 **"Mekanizma & Patofizyoloji"**: Anlamadığın tıbbi konuları ve şıkların elenme nedenlerini Robbins/Guyton derinliğinde açıklayayım.`,
        timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
        providerUsed: 'MedSoru AI Motoru'
      }
    ];
  });

  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [providerMode, setProviderMode] = useState<'ollama' | 'auto' | 'groq' | 'muse-spark'>('ollama');
  const [selectedModel, setSelectedModel] = useState<string>('gemma3:4b');
  const [interactionMode, setInteractionMode] = useState<'general' | 'find_question' | 'generate_from_keywords' | 'explain'>('general');
  const [auditSummary, setAuditSummary] = useState<any>(null);

  // Model-spesifik zaman aşımları ve kullanıcı onaylı bulut fallback state'i
  const [fallbackPromptDialog, setFallbackPromptDialog] = useState<{
    query: string;
    originalModel: string;
    errorMsg: string;
  } | null>(null);

  // AI Hata Kayıtları (Error Logs) Denetim Modalı
  const [showErrorLogsModal, setShowErrorLogsModal] = useState(false);
  const [errorLogs, setErrorLogs] = useState<any[]>([]);
  const [unresolvedLogCount, setUnresolvedLogCount] = useState(0);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Model bazlı tahmini yanıt süresi tablosu (bilgilendirme)
  const getModelTimeoutSeconds = (model: string): number => {
    if (model === 'deepseek-r1:8b') return 120; // 2 dakika
    if (model === 'qwen3:1.7b-q8_0') return 30;  // 30 saniye
    if (model === 'gemma3:4b' || model === 'medgemma1.5:4b') return 45; // 45 saniye
    if (model.includes('flash')) return 25;
    if (model.includes('gpt-oss-120b')) return 45;
    return 60;
  };

  const loadErrorLogs = async () => {
    const res = await ApiService.getAiErrorLogs();
    if (res.success) {
      setErrorLogs(res.logs || []);
      setUnresolvedLogCount(res.unresolvedCount || 0);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  useEffect(() => {
    // Soru Denetim Durumunu Çek
    ApiService.getQualityAuditStatus().then(res => {
      if (res && res.hasAudit) {
        setAuditSummary(res);
      }
    });
    loadErrorLogs();
  }, []);

  const handleSendMessage = async (textToSend?: string, forceCloudFallback: boolean = false) => {
    const query = (textToSend || inputText).trim();
    if (!query || isLoading) return;

    if (!forceCloudFallback) {
      const userMsgId = `usr-${Date.now()}`;
      const userMsg: ChatMessage = {
        id: userMsgId,
        role: 'user',
        content: query,
        timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, userMsg]);
      setInputText('');
    }

    setIsLoading(true);
    setFallbackPromptDialog(null);

    const timeoutLimitMs = getModelTimeoutSeconds(selectedModel) * 1000;

    try {
      const historyForApi = messages
        .filter(m => m.id !== 'msg-welcome')
        .map(m => ({ role: m.role, content: m.content }));

      // Eğer kullanıcı yerel GPU seçtiyse ve forceCloudFallback verilmemişse bulut fallback'i ASLA otomatik yapılmaz!
      const shouldAllowCloud = forceCloudFallback || providerMode !== 'ollama';

      const res = await ApiService.sendGeneralAiChat({
        message: query,
        messages: historyForApi,
        provider: forceCloudFallback ? 'auto' : providerMode,
        model: forceCloudFallback ? 'gemini-3.8-flash' : selectedModel,
        mode: interactionMode,
        allowCloudFallback: shouldAllowCloud,
        timeoutMs: timeoutLimitMs
      });

      if (res.success && res.reply) {
        const assistantMsg: ChatMessage = {
          id: `ai-${Date.now()}`,
          role: 'assistant',
          content: res.reply,
          providerUsed: res.providerUsed || (forceCloudFallback ? 'Google Gemini (Kullanıcı Onaylı Bulut)' : 'MedSoru AI'),
          planUsed: res.planUsed,
          matchedQuestions: res.matchedQuestions,
          timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, assistantMsg]);
        loadErrorLogs(); // Varsa çözümleri güncelle
      } else {
        const errDetail = res.error || 'Model yanıt veremedi veya zaman aşımına uğradı.';
        
        // Yerel model yanıt veremediğinde otomatik olarak buluta geçilmez, kullanıcıya onay sorulur:
        if (providerMode === 'ollama' && !forceCloudFallback) {
          setFallbackPromptDialog({
            query,
            originalModel: selectedModel,
            errorMsg: errDetail
          });
        }

        const errorMsg: ChatMessage = {
          id: `err-${Date.now()}`,
          role: 'assistant',
          content: `⚠️ **Yanıt Alınamadı (${selectedModel}):** ${errDetail}\n\n*Hata sistem loglarına işlendi. Model yanıt veremediğinde otomatik olarak bulut AI'ya geçilmez.*`,
          timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, errorMsg]);
        loadErrorLogs();
      }
    } catch (err: any) {
      const errDetail = err.message || 'Sunucuya ulaşılamadı.';
      if (providerMode === 'ollama' && !forceCloudFallback) {
        setFallbackPromptDialog({
          query,
          originalModel: selectedModel,
          errorMsg: errDetail
        });
      }

      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: `⚠️ **Bağlantı/Çalışma Hatası:** ${errDetail}\n\n*Bu sorun sistem hata kayıtlarına kaydedildi.*`,
        timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMsg]);
      loadErrorLogs();
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickPrompt = (promptText: string, mode: typeof interactionMode) => {
    setInteractionMode(mode);
    handleSendMessage(promptText);
  };

  const renderFormattedText = (raw: string) => {
    const paragraphs = raw.split('\n\n');
    return (
      <div className="space-y-2 text-[14px] leading-relaxed">
        {paragraphs.map((para, pIdx) => {
          const trimmed = para.trim();
          if (!trimmed) return null;

          // Header ###
          if (trimmed.startsWith('### ')) {
            return (
              <h4 key={pIdx} className="font-bold text-accent text-[14px] pt-1 pb-0.5 border-b border-line-soft">
                {trimmed.replace(/^###\s*/, '')}
              </h4>
            );
          }
          if (trimmed.startsWith('## ')) {
            return (
              <h3 key={pIdx} className="font-bold text-ink text-[15px] pt-1 pb-0.5 font-display">
                {trimmed.replace(/^##\s*/, '')}
              </h3>
            );
          }
          if (trimmed.startsWith('# ')) {
            return (
              <h2 key={pIdx} className="font-bold text-ink text-[16px] pt-1.5 pb-0.5">
                {trimmed.replace(/^#\s*/, '')}
              </h2>
            );
          }

          // Markdown Table
          if (trimmed.includes('|') && trimmed.split('\n').length >= 3) {
            const rows = trimmed.split('\n').filter(r => r.trim().startsWith('|'));
            if (rows.length >= 3) {
              const headers = rows[0].split('|').map(c => c.trim()).filter((_, idx, arr) => idx > 0 && idx < arr.length - 1);
              const dataRows = rows.slice(2).map(r => r.split('|').map(c => c.trim()).filter((_, idx, arr) => idx > 0 && idx < arr.length - 1));
              return (
                <div key={pIdx} className="overflow-x-auto my-2 rounded-xl border border-line">
                  <table className="w-full text-left text-[12.5px]">
                    <thead className="bg-canvas border-b border-line text-ink-2 font-semibold">
                      <tr>
                        {headers.map((h, hIdx) => (
                          <th key={hIdx} className="p-2.5">{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-line-soft">
                      {dataRows.map((row, rIdx) => (
                        <tr key={rIdx} className="hover:bg-slate-50/50">
                          {row.map((cell, cIdx) => (
                            <td key={cIdx} className="p-2.5" dangerouslySetInnerHTML={{
                              __html: cell
                                .replace(/\*\*(.*?)\*\*/g, '<strong class="text-ink font-semibold">$1</strong>')
                                .replace(/\*(.*?)\*/g, '<em class="italic text-ink-2">$1</em>')
                            }} />
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              );
            }
          }

          // Bullet list
          if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
            const items = trimmed.split('\n').filter(Boolean);
            return (
              <ul key={pIdx} className="space-y-1 my-1 pl-4 list-disc text-ink">
                {items.map((it, iIdx) => (
                  <li key={iIdx} className="leading-snug">
                    <span dangerouslySetInnerHTML={{
                      __html: it
                        .replace(/^[\-\*]\s*/, '')
                        .replace(/\*\*(.*?)\*\*/g, '<strong class="text-ink font-semibold">$1</strong>')
                        .replace(/\*(.*?)\*/g, '<em class="italic text-ink-2">$1</em>')
                    }} />
                  </li>
                ))}
              </ul>
            );
          }

          // Numbered list
          if (/^\d+\.\s/.test(trimmed)) {
            const items = trimmed.split('\n').filter(Boolean);
            return (
              <ol key={pIdx} className="space-y-1 my-1 pl-4 list-decimal text-ink">
                {items.map((it, iIdx) => (
                  <li key={iIdx} className="leading-snug">
                    <span dangerouslySetInnerHTML={{
                      __html: it
                        .replace(/^\d+\.\s*/, '')
                        .replace(/\*\*(.*?)\*\*/g, '<strong class="text-ink font-semibold">$1</strong>')
                        .replace(/\*(.*?)\*/g, '<em class="italic text-ink-2">$1</em>')
                    }} />
                  </li>
                ))}
              </ol>
            );
          }

          // Callout / Blockquote
          if (trimmed.startsWith('>')) {
            return (
              <div key={pIdx} className="border-l-3 border-accent bg-accent-soft/40 px-3 py-2 rounded-r-lg text-ink text-[13px] my-1">
                <span dangerouslySetInnerHTML={{
                  __html: trimmed
                    .replace(/^>\s*/g, '')
                    .replace(/\*\*(.*?)\*\*/g, '<strong class="text-ink font-semibold">$1</strong>')
                    .replace(/\*(.*?)\*/g, '<em class="italic text-ink-2">$1</em>')
                }} />
              </div>
            );
          }

          // Normal Paragraph
          return (
            <p key={pIdx} className="m-0 text-ink leading-relaxed">
              <span dangerouslySetInnerHTML={{
                __html: trimmed
                  .replace(/\*\*(.*?)\*\*/g, '<strong class="text-ink font-semibold">$1</strong>')
                  .replace(/\*(.*?)\*/g, '<em class="italic text-ink-2">$1</em>')
                  .replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.5 rounded bg-slate-100 font-mono text-[12px] text-accent">$1</code>')
              }} />
            </p>
          );
        })}
      </div>
    );
  };

  return (
    <div className="flex flex-col gap-4 pb-12 min-w-0 w-full max-w-[960px] mx-auto">
      <PageHeader
        eyebrow="Tıp Fakültesi AI OS"
        title="AI Tıp Asistanı & Soru Dedektifi"
        description="Yerel RTX 4060 GPU modelleri (qLoRA, Gemma 3, DeepSeek) ve internet erişimli tıp modelleriyle canlı klinik sohbet."
        stats={[
          { label: 'Sağlayıcı', value: providerMode === 'ollama' ? 'Yerel GPU (RTX 4060)' : 'Ücretsiz Web AI' },
          { label: 'Aktif Model', value: selectedModel },
          ...(auditSummary?.totalIssuesFound
            ? [{ label: 'Tespit Edilen Düzenleme', value: `${auditSummary.totalIssuesFound} Soru`, tone: 'warn' as const }]
            : [])
        ]}
      />

      {/* Control Bar: Provider & Interaction Mode Switcher */}
      <div className="bg-white rounded-2xl border border-line p-3.5 flex flex-wrap items-center justify-between gap-3 shadow-xs">
        <div className="flex flex-wrap items-center gap-2">
          {/* Provider Selection */}
          <div className="flex items-center gap-1 bg-canvas p-1 rounded-xl">
            <button
              type="button"
              onClick={() => { setProviderMode('ollama'); setSelectedModel('gemma3:4b'); }}
              className={`h-8 px-2.5 rounded-lg text-[13px] font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
                providerMode === 'ollama' ? 'bg-indigo-600 text-white shadow-xs' : 'text-ink-2 hover:text-ink'
              }`}
            >
              <Cpu className="w-3.5 h-3.5" />
              <span>Yerel GPU (RTX 4060)</span>
            </button>

            <button
              type="button"
              onClick={() => { setProviderMode('auto'); setSelectedModel('gemini-3.8-flash'); }}
              className={`h-8 px-2.5 rounded-lg text-[13px] font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
                providerMode !== 'ollama' ? 'bg-accent text-white shadow-xs' : 'text-ink-2 hover:text-ink'
              }`}
            >
              <Globe className="w-3.5 h-3.5" />
              <span>İnternet / Bulut (Ücretsiz)</span>
            </button>
          </div>

          {/* Model Dropdown */}
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="h-9 px-3 rounded-xl bg-field border border-line text-[13px] text-ink font-medium cursor-pointer outline-0 focus:border-accent"
          >
            {providerMode === 'ollama' ? (
              <>
                <option value="gemma3:4b">Gemma 3 (4B - Hızlı & Yerel GPU)</option>
                <option value="deepseek-r1:8b">DeepSeek-R1 (8B - Derin Mantık)</option>
                <option value="qwen3:1.7b-q8_0">Qwen 3 (1.7B - Ultra Hafif)</option>
                <option value="medgemma1.5:4b">MedGemma 1.5 (4B - Tıp Modeli)</option>
              </>
            ) : (
              <>
                <option value="gemini-3.8-flash">Google Gemini Flash (En Hızlı)</option>
                <option value="openai/gpt-oss-120b">Groq Cloud (GPT-OSS 120B)</option>
                <option value="muse-spark-1.3-contributor-free">Muse Spark 1.3 Free (Sınırsız)</option>
              </>
            )}
          </select>

          {/* Model Timeout Badge */}
          <span className="text-[11px] font-mono text-ink-3 bg-canvas border border-line px-2 py-1 rounded-lg flex items-center gap-1" title="Bu model için izin verilen azami yanıt bekleme süresi">
            <Clock className="w-3 h-3 text-slate-500" />
            <span>Zaman Aşımı: {getModelTimeoutSeconds(selectedModel)}sn</span>
          </span>

          {/* Error Logs Button */}
          <button
            type="button"
            onClick={() => { setShowErrorLogsModal(true); loadErrorLogs(); }}
            className={`h-8 px-2.5 rounded-xl border text-[12px] font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
              unresolvedLogCount > 0
                ? 'bg-amber-50 text-amber-900 border-amber-300 hover:bg-amber-100'
                : 'bg-white text-ink-2 border-line hover:text-ink'
            }`}
            title="Yapay zeka modellerinin hata ve zaman aşımı kayıtlarını incele"
          >
            <History className="w-3.5 h-3.5 text-amber-600" />
            <span>Hata Kayıtları</span>
            {unresolvedLogCount > 0 && (
              <span className="px-1.5 py-0.2 bg-amber-500 text-white rounded-full text-[10px] font-bold">
                {unresolvedLogCount}
              </span>
            )}
          </button>
        </div>

        {/* Mode Selector */}
        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar">
          {(
            [
              ['general', 'Tıbbi Sohbet', Lightbulb],
              ['find_question', 'Soru Dedektifi', Search],
              ['generate_from_keywords', 'Soru Türet', Sparkles],
              ['explain', 'Mekanizma Sor', BookOpen],
            ] as const
          ).map(([mId, label, Icon]) => (
            <button
              key={mId}
              type="button"
              onClick={() => setInteractionMode(mId)}
              className={`h-8 px-2.5 rounded-lg text-[12.5px] font-semibold flex items-center gap-1.5 transition-colors cursor-pointer shrink-0 ${
                interactionMode === mId
                  ? 'bg-ink text-white shadow-xs'
                  : 'bg-field text-ink-2 hover:bg-canvas hover:text-ink'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Suggested Quick Prompts */}
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          onClick={() => handleQuickPrompt('50 yaşında erkek hasta, hiperkalsemi ve lityum kullanımı öyküsü var. Bu hangi kurul sorusudur ve doğru cevabı nedir?', 'find_question')}
          className="text-[12px] bg-white border border-line-2 hover:border-accent hover:text-accent rounded-full px-3 py-1.5 text-ink-2 flex items-center gap-1.5 cursor-pointer transition-colors"
        >
          <Search className="w-3 h-3 text-indigo-500" />
          <span>🔍 "50 yaş hiperkalsemi lityum sorusunu bul"</span>
        </button>

        <button
          type="button"
          onClick={() => handleQuickPrompt('Mycobacterium tuberculosis, Ziehl-Neelsen, kazeöz nekroz anahtar kelimelerinden olası Dönem 3 kurul soruları üret.', 'generate_from_keywords')}
          className="text-[12px] bg-white border border-line-2 hover:border-accent hover:text-accent rounded-full px-3 py-1.5 text-ink-2 flex items-center gap-1.5 cursor-pointer transition-colors"
        >
          <Sparkles className="w-3 h-3 text-amber-500" />
          <span>✨ "Tüberküloz & kazeöz nekrozdan kurul sorusu türet"</span>
        </button>

        <button
          type="button"
          onClick={() => handleQuickPrompt('Kardiyojenik şok ile hipovolemik şok arasındaki Swan-Ganz kateter hemodinami farklarını açıkla.', 'explain')}
          className="text-[12px] bg-white border border-line-2 hover:border-accent hover:text-accent rounded-full px-3 py-1.5 text-ink-2 flex items-center gap-1.5 cursor-pointer transition-colors"
        >
          <BookOpen className="w-3 h-3 text-emerald-500" />
          <span>🧬 "Kardiyojenik vs hipovolemik şok farkı"</span>
        </button>
      </div>

      {/* Chat Messages Log */}
      <div className="bg-canvas border border-line rounded-2xl p-4 sm:p-5 flex flex-col gap-4 min-h-[420px] max-h-[640px] overflow-y-auto">
        {messages.map((m) => {
          const isUser = m.role === 'user';
          return (
            <div
              key={m.id}
              className={`flex flex-col gap-1.5 max-w-[92%] ${isUser ? 'self-end items-end' : 'self-start items-start'}`}
            >
              <div className="flex items-center gap-2 text-[11px] text-ink-3 px-1">
                <span>{isUser ? (currentUser?.displayName || 'Tıp Öğrencisi') : 'MedSoru AI'}</span>
                <span>·</span>
                <span>{m.timestamp}</span>
                {m.providerUsed && (
                  <>
                    <span>·</span>
                    <span className="font-mono text-[10px] text-indigo-600 bg-indigo-50 px-1.5 py-0.2 rounded font-semibold">
                      {m.providerUsed}
                    </span>
                  </>
                )}
              </div>

              <div
                className={`p-4 rounded-2xl text-[14.5px] leading-relaxed break-words ${
                  isUser
                    ? 'bg-accent text-white rounded-tr-xs shadow-xs font-medium whitespace-pre-wrap'
                    : 'bg-white text-ink border border-line rounded-tl-xs shadow-2xs w-full'
                }`}
              >
                {isUser ? m.content : renderFormattedText(m.content)}

                {/* Matched Questions Cards if any */}
                {m.matchedQuestions && m.matchedQuestions.length > 0 && (
                  <div className="mt-3.5 pt-3 border-t border-line-soft flex flex-col gap-2">
                    <span className="text-[12px] font-bold text-indigo-700 flex items-center gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-indigo-600" />
                      Arşivden Eşleşen Sorular ({m.matchedQuestions.length})
                    </span>
                    <div className="grid grid-cols-1 gap-2">
                      {m.matchedQuestions.map((mq: any) => (
                        <div
                          key={mq.id}
                          className="bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-[12.5px] text-slate-800 flex flex-col gap-1"
                        >
                          <div className="flex items-center justify-between">
                            <span className="font-bold text-indigo-800">{mq.discipline} · {mq.topic}</span>
                            <span className="text-[11px] bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded font-bold">
                              Cevap: {mq.correctAnswer}
                            </span>
                          </div>
                          <p className="line-clamp-2 m-0 text-slate-600">{mq.stem}</p>
                          {onNavigateToQuestion && (
                            <button
                              type="button"
                              onClick={() => onNavigateToQuestion(mq.id)}
                              className="self-end text-[11.5px] font-bold text-accent hover:underline flex items-center gap-1 mt-1 cursor-pointer"
                            >
                              Soruyu Görüntüle <ArrowRight className="w-3 h-3" />
                            </button>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="self-start flex items-center gap-2.5 bg-white border border-line rounded-2xl px-4 py-3 text-[13.5px] text-ink-2 shadow-2xs">
            <RefreshCw className="w-4 h-4 text-accent animate-spin" />
            <span>
              {providerMode === 'ollama'
                ? `RTX 4060 GPU üzerinde ${selectedModel} düşünüyor...`
                : 'Tıp veritabanı ve internet kaynakları taranıyor...'}
            </span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Composer */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="flex gap-2 items-center"
      >
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder={
            interactionMode === 'find_question'
              ? 'Hatırladığın soru detaylarını yaz (örn: 50 yaş, hiperkalsemi, lityum kullanımı)...'
              : interactionMode === 'generate_from_keywords'
              ? 'Anahtar kelimeleri yaz (örn: staphylococcus aureus, katalaz pozitif, koagülaz)...'
              : 'Tıp asistanına soru sor veya aklına takılan klinik mekanizmayı danış...'
          }
          disabled={isLoading}
          className="flex-1 h-12 px-4 rounded-xl bg-white border border-line focus:border-accent outline-0 text-[15px] text-ink placeholder:text-slate-600 shadow-xs"
        />

        <button
          type="submit"
          disabled={!inputText.trim() || isLoading}
          className="h-12 px-5 rounded-xl bg-accent hover:bg-accent-hover disabled:opacity-50 text-white font-semibold flex items-center gap-2 cursor-pointer shadow-xs transition-colors shrink-0"
        >
          <Send className="w-4 h-4" />
          <span className="hidden sm:inline">Gönder</span>
        </button>
      </form>

      {/* 1. Kullanıcı Onaylı Bulut Fallback Modalı (Otomatik Geçiş Kesinlikle Engellendi) */}
      {fallbackPromptDialog && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-line p-5 max-w-[500px] w-full shadow-xl flex flex-col gap-4">
            <div className="flex items-start gap-3">
              <div className="p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-700 shrink-0">
                <AlertTriangle className="w-6 h-6" />
              </div>
              <div className="flex-1">
                <h3 className="text-[16px] font-bold text-ink">Yerel GPU Yanıt Vermedi</h3>
                <p className="text-[13px] text-ink-2 mt-1 leading-relaxed">
                  Yerel model <strong className="text-indigo-600 font-semibold">{fallbackPromptDialog.originalModel}</strong> zaman aşımına uğradı veya yanıt oluşturamadı.
                </p>
                <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5 mt-2.5 text-[12px] text-slate-700 font-mono break-words">
                  {fallbackPromptDialog.errorMsg}
                </div>
              </div>
            </div>

            <div className="bg-amber-50/70 border border-amber-200/80 rounded-xl p-3 text-[12.5px] text-amber-900 leading-normal">
              🛡️ <strong>Kullanıcı Gizliliği & Kontrol:</strong> MedSoru AI, onayınız olmadan sorgunuzu asla internet/bulut modellerine yönlendirmez. Bu soruyu ücretsiz bulut modeliyle (Google Gemini Flash) tekrar denemek ister misiniz?
            </div>

            <div className="flex items-center justify-end gap-2.5 pt-2">
              <button
                type="button"
                onClick={() => setFallbackPromptDialog(null)}
                className="px-4 py-2 rounded-xl border border-line text-[13px] font-semibold text-ink-2 hover:bg-canvas transition-colors cursor-pointer"
              >
                İptal Et
              </button>
              <button
                type="button"
                onClick={() => handleSendMessage(fallbackPromptDialog.query, true)}
                className="px-4 py-2 rounded-xl bg-accent hover:bg-accent-hover text-white text-[13px] font-semibold flex items-center gap-1.5 shadow-xs transition-colors cursor-pointer"
              >
                <Globe className="w-4 h-4" />
                <span>Buluttan Dene (Onaylıyorum)</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 2. Yapay Zeka Hata Kayıtları (Error Logs) Denetim Modalı */}
      {showErrorLogsModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl border border-line p-5 max-w-[700px] w-full max-h-[85vh] flex flex-col shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-line">
              <div className="flex items-center gap-2">
                <History className="w-5 h-5 text-amber-600" />
                <h3 className="text-[16px] font-bold text-ink">Yapay Zeka Hata ve Zaman Aşımı Kayıtları</h3>
              </div>
              <button
                type="button"
                onClick={() => setShowErrorLogsModal(false)}
                className="p-1 rounded-lg text-ink-3 hover:text-ink hover:bg-canvas transition-colors cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-[12.5px] text-ink-2 my-2.5">
              Bu panel yerel ve bulut modellerin karşılaştığı tüm zaman aşımı, bellek ve API hatalarını kayıt altına alır. Hataları inceleyebilir ve çözümlendi olarak işaretleyebilirsiniz.
            </p>

            <div className="flex-1 overflow-y-auto space-y-2.5 pr-1 my-2">
              {errorLogs.length === 0 ? (
                <div className="p-8 text-center text-ink-3 text-[13px] bg-canvas rounded-xl border border-line">
                  🎉 Henüz kayıtlı yapay zeka hatası veya zaman aşımı bulunmuyor.
                </div>
              ) : (
                errorLogs.map((log: any) => (
                  <div
                    key={log.id}
                    className={`p-3.5 rounded-xl border text-[12.5px] flex flex-col gap-1.5 transition-colors ${
                      log.status === 'resolved'
                        ? 'bg-slate-50 border-slate-200 opacity-60'
                        : log.isTimeout
                        ? 'bg-amber-50/50 border-amber-200'
                        : 'bg-rose-50/50 border-rose-200'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-0.5 rounded font-mono font-bold text-[11px] ${
                          log.provider === 'ollama' ? 'bg-indigo-100 text-indigo-800' : 'bg-blue-100 text-blue-800'
                        }`}>
                          {log.provider} · {log.model}
                        </span>
                        {log.isTimeout && (
                          <span className="px-1.5 py-0.5 rounded bg-amber-100 text-amber-800 text-[10.5px] font-semibold flex items-center gap-1">
                            <Clock className="w-3 h-3" /> Zaman Aşımı
                          </span>
                        )}
                        <span className={`px-1.5 py-0.5 rounded text-[10.5px] font-semibold ${
                          log.status === 'resolved' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                        }`}>
                          {log.status === 'resolved' ? 'Çözüldü' : 'Açık / İncelenmeli'}
                        </span>
                      </div>
                      <span className="text-[11px] text-ink-3">
                        {new Date(log.timestamp).toLocaleString('tr-TR')}
                      </span>
                    </div>

                    <div className="text-ink font-mono text-[12px] bg-white p-2 rounded-lg border border-line break-words">
                      {log.errorMessage}
                    </div>

                    {log.promptSnippet && (
                      <div className="text-ink-2 text-[11.5px] line-clamp-1 italic">
                        Soru: "{log.promptSnippet}"
                      </div>
                    )}

                    <div className="flex items-center justify-end gap-2 mt-1">
                      {log.status !== 'resolved' ? (
                        <button
                          type="button"
                          onClick={async () => {
                            await ApiService.resolveAiErrorLog(log.id, 'resolved');
                            loadErrorLogs();
                          }}
                          className="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-[11px] flex items-center gap-1 cursor-pointer transition-colors"
                        >
                          <Check className="w-3 h-3" />
                          <span>Çözüldü Olarak İşaretle</span>
                        </button>
                      ) : (
                        <span className="text-[11px] text-emerald-700 font-semibold flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Çözümlendi
                        </span>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-line mt-2">
              <span className="text-[12px] text-ink-3">
                Toplam <strong>{errorLogs.length}</strong> hata kaydı ({unresolvedLogCount} açık)
              </span>
              <div className="flex items-center gap-2">
                {unresolvedLogCount > 0 && (
                  <button
                    type="button"
                    onClick={async () => {
                      await ApiService.resolveAiErrorLog('all', 'resolved');
                      loadErrorLogs();
                    }}
                    className="px-3 py-1.5 rounded-xl border border-line text-ink-2 hover:text-ink text-[12px] font-semibold cursor-pointer transition-colors"
                  >
                    Tümünü Çözüldü Yap
                  </button>
                )}
                <button
                  type="button"
                  onClick={() => setShowErrorLogsModal(false)}
                  className="px-4 py-1.5 rounded-xl bg-ink text-white text-[12px] font-semibold cursor-pointer"
                >
                  Kapat
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
