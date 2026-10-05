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
  ExternalLink
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

  const messagesEndRef = useRef<HTMLDivElement>(null);

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
  }, []);

  const handleSendMessage = async (textToSend?: string) => {
    const query = (textToSend || inputText).trim();
    if (!query || isLoading) return;

    const userMsgId = `usr-${Date.now()}`;
    const userMsg: ChatMessage = {
      id: userMsgId,
      role: 'user',
      content: query,
      timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setIsLoading(true);

    try {
      const historyForApi = messages
        .filter(m => m.id !== 'msg-welcome')
        .map(m => ({ role: m.role, content: m.content }));

      const res = await ApiService.sendGeneralAiChat({
        message: query,
        messages: historyForApi,
        provider: providerMode,
        model: selectedModel,
        mode: interactionMode,
      });

      if (res.success && res.reply) {
        const assistantMsg: ChatMessage = {
          id: `ai-${Date.now()}`,
          role: 'assistant',
          content: res.reply,
          providerUsed: res.providerUsed || 'MedSoru AI',
          planUsed: res.planUsed,
          matchedQuestions: res.matchedQuestions,
          timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, assistantMsg]);
      } else {
        const errorMsg: ChatMessage = {
          id: `err-${Date.now()}`,
          role: 'assistant',
          content: `⚠️ Yanıt oluşturulamadı: ${res.error || 'Yapay zeka servisi meşgul. Lütfen model seçimini değiştirip tekrar deneyin.'}`,
          timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, errorMsg]);
      }
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: `⚠️ Bağlantı hatası: ${err.message || 'Sunucuya ulaşılamadı.'}`,
        timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickPrompt = (promptText: string, mode: typeof interactionMode) => {
    setInteractionMode(mode);
    handleSendMessage(promptText);
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
              className={`flex flex-col gap-1.5 max-w-[88%] ${isUser ? 'self-end items-end' : 'self-start items-start'}`}
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
                className={`p-4 rounded-2xl text-[14.5px] leading-relaxed whitespace-pre-wrap break-words ${
                  isUser
                    ? 'bg-accent text-white rounded-tr-xs shadow-xs font-medium'
                    : 'bg-white text-ink border border-line rounded-tl-xs shadow-2xs'
                }`}
              >
                {m.content}

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
    </div>
  );
};
