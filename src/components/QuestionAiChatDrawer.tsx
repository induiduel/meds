import React, { useState, useEffect, useRef } from 'react';
import { 
  Sparkles, 
  X, 
  Send, 
  RotateCcw, 
  Copy, 
  Check, 
  Bot, 
  User, 
  Lightbulb, 
  Brain, 
  AlertTriangle, 
  FileText, 
  Stethoscope, 
  ChevronDown, 
  ChevronUp, 
  SlidersHorizontal,
  Database,
  ThumbsUp
} from 'lucide-react';
import { ApiService, QuestionChatContext, QuestionChatMessage } from '../services/api';

interface QuestionAiChatDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  questionContext: QuestionChatContext | null;
}

export const QuestionAiChatDrawer: React.FC<QuestionAiChatDrawerProps> = ({
  isOpen,
  onClose,
  questionContext,
}) => {
  const [messages, setMessages] = useState<QuestionChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [isContextExpanded, setIsContextExpanded] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [preferredProvider, setPreferredProvider] = useState<'auto' | 'gemini' | 'groq'>('auto');
  const [selectedModel, setSelectedModel] = useState('gemini-3.8-flash');
  const [lastUsedProvider, setLastUsedProvider] = useState<string>('');
  const [pastInteractions, setPastInteractions] = useState<any[]>([]);
  const [showPastInteractions, setShowPastInteractions] = useState(false);
  const [upvotedIds, setUpvotedIds] = useState<Set<string>>(new Set());

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom whenever messages or loading state changes
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isLoading, isOpen]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => {
        inputRef.current?.focus();
      }, 200);
    }
  }, [isOpen]);

  // Reset or initialize welcoming greeting when question changes
  useEffect(() => {
    if (!questionContext) {
      setMessages([]);
      return;
    }

    const { discipline, topic, correctAnswer, userAnswer } = questionContext;
    let welcome = `Merhaba! 👋 Ben senin **AI Tıp Asistanınım**.\n\n`;
    welcome += `Şu an **${discipline || 'Tıp Fakültesi'}** dersinden **${topic || 'Kurul Sorusu'}** sorusunu inceliyoruz.`;

    if (userAnswer && correctAnswer) {
      if (userAnswer === correctAnswer) {
        welcome += ` Tebrikler, **${userAnswer}** şıkkını işaretleyerek soruyu **doğru** çözdün! 🎉 İstersen altında yatan mekanizmayı, sınav tuzaklarını veya aklında tutman için özel bir mnemonik konuşabiliriz.`;
      } else {
        welcome += ` **${userAnswer}** şıkkını işaretledin, ancak doğru cevap **${correctAnswer}**. Neden bu şıkkın doğru olduğunu veya işaretlediğin şıkkın hangi durumda geçerli olabileceğini hemen açıklayabilirim.`;
      }
    } else if (correctAnswer) {
      welcome += ` Sorunun doğru cevabı **${correctAnswer}** şıkkı olarak belirlenmiş. Bu soruyla ilgili aklına takılan her şeyi bana sorabilirsin!`;
    } else {
      welcome += ` Bu soruyla ilgili aklına takılan mekanizmaları veya çeldiricileri bana anlık olarak sorabilirsin!`;
    }

    setMessages([
      {
        role: 'assistant',
        content: welcome,
        timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
        providerUsed: 'AI Soru Hocası',
      },
    ]);

    if (questionContext?.id) {
      ApiService.getQuestionAiInteractions(questionContext.id).then((list) => {
        setPastInteractions(list);
        if (list.length > 0) {
          setShowPastInteractions(true);
        }
      });
    } else {
      setPastInteractions([]);
    }
  }, [questionContext?.id, questionContext?.stem, questionContext?.userAnswer]);

  const handleUpvote = async (interactionId: string) => {
    if (upvotedIds.has(interactionId)) return;
    const ok = await ApiService.upvoteAiInteraction(interactionId);
    if (ok) {
      setUpvotedIds((prev) => new Set(prev).add(interactionId));
      setPastInteractions((prev) =>
        prev.map((item) =>
          item.id === interactionId ? { ...item, upvotes: (item.upvotes || 0) + 1 } : item
        )
      );
    }
  };

  if (!isOpen || !questionContext) return null;

  const handleSendMessage = async (textToSend?: string) => {
    const text = (textToSend || inputMessage).trim();
    if (!text || isLoading) return;

    const userMsg: QuestionChatMessage = {
      role: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
    };

    const nextMessages = [...messages, userMsg];
    setMessages(nextMessages);
    setInputMessage('');
    setIsLoading(true);

    try {
      const res = await ApiService.chatWithQuestionTutor({
        questionContext,
        messages: nextMessages.map((m) => ({ role: m.role, content: m.content })),
        currentMessage: text,
        preferredProvider,
        model: selectedModel,
      });

      if (res.success && res.reply) {
        const assistantMsg: QuestionChatMessage = {
          role: 'assistant',
          content: res.reply,
          providerUsed: res.providerUsed || 'AI Asistan',
          planUsed: res.planUsed,
          timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, assistantMsg]);
        if (res.providerUsed) setLastUsedProvider(res.providerUsed);
      } else {
        const errorMsg: QuestionChatMessage = {
          role: 'assistant',
          content: `⚠️ **Üzgünüm, bir sorun oluştu:** ${res.error || 'Yapay zeka yanıt üretemedi. Lütfen tekrar deneyin.'}`,
          timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, errorMsg]);
      }
    } catch (err: any) {
      const errorMsg: QuestionChatMessage = {
        role: 'assistant',
        content: `⚠️ **Bağlantı hatası:** ${err.message || 'Yapay zekaya ulaşılamadı.'}`,
        timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleCopy = (content: string, index: number) => {
    navigator.clipboard.writeText(content);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const handleClearHistory = () => {
    if (!questionContext) return;
    setMessages([
      {
        role: 'assistant',
        content: `Sohbet geçmişi temizlendi. Soru hakkında sormak istediğin yeni bir konuyu yazabilirsin.`,
        timestamp: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
        providerUsed: 'AI Soru Hocası',
      },
    ]);
  };

  // Quick Action Chips
  const isWrong = questionContext.userAnswer && questionContext.correctAnswer && questionContext.userAnswer !== questionContext.correctAnswer;
  const quickChips = [
    isWrong
      ? { label: `Neden ${questionContext.userAnswer} değil de ${questionContext.correctAnswer}?`, icon: AlertTriangle, prompt: `Bu soruda ben ${questionContext.userAnswer} şıkkını işaretlemiştim ama doğru cevap ${questionContext.correctAnswer}. Neden ${questionContext.userAnswer} şıkkı elenmeli ve ${questionContext.correctAnswer} şıkkının mekanizması nedir?` }
      : { label: 'Mekanizmayı açıkla', icon: Lightbulb, prompt: 'Bu sorunun doğru cevabının altında yatan temel patofizyolojik ve farmakolojik mekanizmayı adım adım açıklar mısın?' },
    { label: 'Diğer şıklar neden yanlış?', icon: Stethoscope, prompt: 'Doğru cevap dışındaki diğer tüm şıkların neden elendiğini ve hangi klinik senaryoda doğru olabileceklerini tek tek açıkla.' },
    { label: 'Akılda tutucu mnemonik ver', icon: Brain, prompt: 'Bu bilgiyi ve soru kökündeki püf noktayı sınavda ve TUS\'ta asla unutmamam için pratik, akılda kalıcı bir mnemonik veya hafıza tekniği verebilir misin?' },
    { label: 'Sınav tuzağı nedir?', icon: AlertTriangle, prompt: 'Bu soruda hocaların öğrencileri düşürmek için kurduğu tipik sınav tuzağı nedir ve benzer bir soru kurulda nasıl karşımıza çıkabilir?' },
    ...(questionContext.slideSnippet || questionContext.lectureReference?.matchedSnippet
      ? [{ label: 'Amfi slaytıyla karşılaştır', icon: FileText, prompt: 'Bu soru amfi ders notlarında ve slaytlarda tam olarak nasıl anlatılmıştı, slayttaki kilit kavramlar nelerdir?' }]
      : [])
  ];

  // Helper to render markdown text with formatting
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
                }} />
              </div>
            );
          }

          // Normal Paragraph
          return (
            <p key={pIdx} className="m-0 text-ink">
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
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-ink/25 backdrop-blur-[2px] z-40 transition-opacity animate-fade-in"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Slide-out Drawer Panel */}
      <aside 
        role="dialog"
        aria-label="Yapay Zeka Tıp Asistanı Canlı Sohbet"
        className="fixed inset-y-0 right-0 z-50 w-full sm:w-[500px] lg:w-[560px] bg-white shadow-2xl flex flex-col border-l border-line animate-slide-left"
      >
        {/* Header */}
        <header className="px-4 py-3.5 border-b border-line bg-white/95 backdrop-blur-md flex items-center justify-between gap-3 shrink-0">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-accent to-indigo-500 text-white flex items-center justify-center shrink-0 shadow-xs">
              <Sparkles className="w-4 h-4 animate-pulse" />
            </div>
            <div className="flex flex-col min-w-0 leading-tight">
              <div className="flex items-center gap-1.5">
                <span className="font-semibold text-ink text-[15px] truncate">AI Tıp Asistanı</span>
                <span className="bg-emerald-50 text-emerald-700 text-[10px] font-bold px-1.5 py-0.5 rounded border border-emerald-200 uppercase tracking-wider shrink-0">
                  Canlı
                </span>
              </div>
              <span className="text-[12px] text-ink-2 truncate">
                {questionContext.discipline || 'Tıp Fakültesi'} · {questionContext.topic || 'Soru İncelemesi'}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-1">
            <button
              type="button"
              onClick={() => setShowSettings(!showSettings)}
              title="Model ve sağlayıcı ayarları"
              aria-label="Model ve sağlayıcı ayarları"
              className={`w-8 h-8 rounded-lg flex items-center justify-center text-ink-2 hover:bg-canvas cursor-pointer transition-colors ${
                showSettings ? 'bg-accent-soft text-accent' : ''
              }`}
            >
              <SlidersHorizontal className="w-4 h-4" />
            </button>
            <button
              type="button"
              onClick={handleClearHistory}
              title="Sohbeti sıfırla"
              aria-label="Sohbeti sıfırla"
              className="w-8 h-8 rounded-lg flex items-center justify-center text-ink-2 hover:bg-canvas cursor-pointer transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
            <button
              type="button"
              onClick={onClose}
              title="Kapat"
              aria-label="Kapat"
              className="w-8 h-8 rounded-lg flex items-center justify-center text-ink hover:bg-canvas cursor-pointer transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </header>

        {/* Model Settings Accordion (Optional) */}
        {showSettings && (
          <div className="px-4 py-2.5 bg-slate-50 border-b border-line flex flex-wrap items-center justify-between gap-2 text-xs">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-ink-2">Sağlayıcı:</span>
              <select
                value={preferredProvider}
                onChange={(e) => setPreferredProvider(e.target.value as any)}
                className="bg-white border border-line-2 rounded px-2 py-1 text-ink outline-none"
              >
                <option value="auto">Otomatik (Gemini + Groq Yedekli)</option>
                <option value="groq">Groq Cloud (Ultra Hızlı)</option>
                <option value="gemini">Google Gemini (Tıbbi Muhakeme)</option>
              </select>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-semibold text-ink-2">Model:</span>
              <select
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                className="bg-white border border-line-2 rounded px-2 py-1 text-ink outline-none"
              >
                <option value="gemini-3.8-flash">Gemini 3.8 Flash</option>
                <option value="gemini-3.5-flash">Gemini 3.5 Flash</option>
                <option value="openai/gpt-oss-120b">Groq GPT-OSS 120B</option>
                <option value="llama-3.3-70b-versatile">Groq Llama 3.3 70B</option>
                <option value="qwen/qwen3.8-27b">Groq Qwen 27B</option>
              </select>
            </div>
          </div>
        )}

        {/* Question Context Quick Card (Collapsible) */}
        <div className="bg-canvas border-b border-line px-4 py-2 text-[12px] flex flex-col gap-1 shrink-0">
          <button
            type="button"
            onClick={() => setIsContextExpanded(!isContextExpanded)}
            className="flex items-center justify-between text-ink-2 hover:text-ink font-semibold cursor-pointer w-full text-left"
          >
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-accent" />
              <span>İncelenen Soru Bağlamı</span>
              {questionContext.correctAnswer && (
                <span className="text-ok font-bold">· Doğru: {questionContext.correctAnswer}</span>
              )}
              {questionContext.userAnswer && (
                <span className={questionContext.userAnswer === questionContext.correctAnswer ? 'text-ok' : 'text-bad-text font-bold'}>
                  · Senin Cevabın: {questionContext.userAnswer}
                </span>
              )}
            </span>
            {isContextExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>

          {isContextExpanded ? (
            <div className="mt-1.5 p-2.5 bg-white rounded-lg border border-line-soft space-y-2 text-[13px] text-ink leading-relaxed max-h-48 overflow-y-auto">
              <p className="font-medium text-ink m-0">{questionContext.stem}</p>
              {questionContext.options && questionContext.options.length > 0 && (
                <div className="space-y-1 pt-1 border-t border-line-soft">
                  {questionContext.options.map((opt) => (
                    <div 
                      key={opt.key}
                      className={`px-2 py-0.5 rounded text-[12px] flex items-start gap-1.5 ${
                        opt.key === questionContext.correctAnswer 
                          ? 'bg-ok-soft text-ok font-bold' 
                          : opt.key === questionContext.userAnswer 
                          ? 'bg-bad-soft text-bad-text font-semibold' 
                          : 'text-ink-2'
                      }`}
                    >
                      <span className="font-mono">{opt.key})</span>
                      <span>{opt.text}</span>
                    </div>
                  ))}
                </div>
              )}
              {questionContext.explanation && (
                <div className="pt-1 border-t border-line-soft text-[12px] text-ink-2">
                  <strong className="text-ink">Mevcut Açıklama:</strong> {questionContext.explanation}
                </div>
              )}
              {(questionContext.slideSnippet || questionContext.lectureReference?.matchedSnippet) && (
                <div className="pt-1 border-t border-line-soft text-[11px] text-ink-3">
                  <strong>Amfi Notu:</strong> {questionContext.slideSnippet || questionContext.lectureReference?.matchedSnippet}
                </div>
              )}
            </div>
          ) : (
            <p className="m-0 text-ink-2 line-clamp-1 truncate text-[11px]">
              {questionContext.stem}
            </p>
          )}
        </div>

        {/* Chat Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Past Community & AI Interactions Accordion */}
          {pastInteractions.length > 0 && (
            <div className="bg-indigo-50/80 border border-indigo-200/80 rounded-xl p-3 text-ink shadow-xs transition-all">
              <div 
                className="flex items-center justify-between cursor-pointer select-none" 
                onClick={() => setShowPastInteractions(!showPastInteractions)}
              >
                <div className="flex items-center gap-2.5">
                  <div className="w-6 h-6 rounded-md bg-indigo-600 text-white flex items-center justify-center text-[12px] font-bold shadow-xs">
                    {pastInteractions.length}
                  </div>
                  <div>
                    <h4 className="font-semibold text-[13px] text-indigo-950 flex items-center gap-1.5 m-0">
                      <span>Bu Soru İçin Kayıtlı AI Soru-Cevapları</span>
                      <span className="text-[10px] font-bold bg-indigo-200/70 text-indigo-800 px-1.5 py-0.5 rounded">RAG Arşivi</span>
                    </h4>
                    <p className="text-[11px] text-indigo-800/80 m-0">Daha önce sorulan sorular ve açıklamalar tek tıkla incelenebilir.</p>
                  </div>
                </div>
                {showPastInteractions ? <ChevronUp className="w-4 h-4 text-indigo-600" /> : <ChevronDown className="w-4 h-4 text-indigo-600" />}
              </div>

              {showPastInteractions && (
                <div className="mt-2.5 space-y-2.5 pt-2.5 border-t border-indigo-200/70 max-h-72 overflow-y-auto pr-1">
                  {pastInteractions.map((item, pIdx) => (
                    <div key={item.id || pIdx} className="bg-white p-3 rounded-lg border border-indigo-100 text-[13px] space-y-2 shadow-2xs">
                      <div className="font-medium text-indigo-950 flex items-start gap-1.5">
                        <span className="text-indigo-600 font-bold shrink-0">❓ Soru:</span>
                        <span className="text-ink font-semibold">"{item.prompt}"</span>
                      </div>
                      <div className="text-ink-2 bg-slate-50 p-2.5 rounded-md text-[12px] max-h-40 overflow-y-auto border border-slate-100">
                        {renderFormattedText(item.response)}
                      </div>
                      <div className="flex items-center justify-between text-[11px] pt-1.5 border-t border-slate-100">
                        <span className="text-ink-3 text-[10px]">
                          {item.userDisplayName || 'Öğrenci'} · {new Date(item.createdAt).toLocaleDateString('tr-TR')}
                        </span>
                        <div className="flex items-center gap-2">
                          <button
                            type="button"
                            onClick={() => handleUpvote(item.id)}
                            className={`inline-flex items-center gap-1 px-2.5 py-1 rounded text-[11px] font-medium transition-colors cursor-pointer ${
                              upvotedIds.has(item.id) 
                                ? 'bg-emerald-100 text-emerald-800 font-bold' 
                                : 'bg-slate-100 hover:bg-slate-200 text-ink'
                            }`}
                          >
                            <ThumbsUp className="w-3 h-3" />
                            <span>{item.upvotes || 0} Faydalı</span>
                          </button>
                          <button
                            type="button"
                            onClick={() => handleSendMessage(`"${item.prompt}" konusuyla ilgili daha detaylı klinik örnek verebilir misin?`)}
                            className="text-accent hover:underline font-semibold text-[11px] cursor-pointer"
                          >
                            Detay İste &rarr;
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {messages.map((msg, idx) => {
            const isMe = msg.role === 'user';
            return (
              <div 
                key={idx} 
                className={`flex gap-3 ${isMe ? 'justify-end' : 'justify-start'}`}
              >
                {!isMe && (
                  <div className="w-8 h-8 rounded-full bg-accent-soft text-accent flex items-center justify-center shrink-0 mt-0.5 border border-accent/20">
                    <Bot className="w-4 h-4" />
                  </div>
                )}

                <div 
                  className={`max-w-[85%] rounded-2xl px-4 py-3 text-[14px] leading-relaxed relative group ${
                    isMe
                      ? 'bg-accent text-white rounded-br-xs shadow-xs'
                      : 'bg-white border border-line rounded-bl-xs text-ink shadow-xs'
                  }`}
                >
                  {isMe ? (
                    <p className="m-0 whitespace-pre-wrap">{msg.content}</p>
                  ) : (
                    renderFormattedText(msg.content)
                  )}

                  {/* Message Footer / Timestamp / Copy */}
                  <div className={`flex items-center justify-between gap-3 mt-1.5 text-[11px] ${
                    isMe ? 'text-white/70' : 'text-ink-3'
                  }`}>
                    <span>{msg.timestamp || ''}</span>
                    {!isMe && (
                      <div className="flex items-center gap-2">
                        <span className="inline-flex items-center gap-1 text-[10px] text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200 font-medium">
                          <Database className="w-2.5 h-2.5" />
                          RAG Kütüphanesinde
                        </span>
                        {msg.providerUsed && (
                          <span className="font-mono text-[10px] opacity-75">{msg.providerUsed}</span>
                        )}
                        <button
                          type="button"
                          onClick={() => handleCopy(msg.content, idx)}
                          title="Cevabı kopyala"
                          className="hover:text-ink cursor-pointer inline-flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          {copiedIndex === idx ? (
                            <>
                              <Check className="w-3 h-3 text-ok" />
                              <span className="text-ok">Kopyalandı</span>
                            </>
                          ) : (
                            <>
                              <Copy className="w-3 h-3" />
                              <span>Kopyala</span>
                            </>
                          )}
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                {isMe && (
                  <div className="w-8 h-8 rounded-full bg-ink text-white flex items-center justify-center shrink-0 mt-0.5">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            );
          })}

          {/* Thinking / Loading Indicator */}
          {isLoading && (
            <div className="flex gap-3 justify-start items-center">
              <div className="w-8 h-8 rounded-full bg-accent-soft text-accent flex items-center justify-center shrink-0 border border-accent/20 animate-spin-slow">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-white border border-line rounded-2xl rounded-bl-xs px-4 py-3 shadow-xs flex items-center gap-2">
                <div className="flex gap-1">
                  <span className="w-2 h-2 rounded-full bg-accent animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 rounded-full bg-accent animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 rounded-full bg-accent animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
                <span className="text-xs text-ink-2 italic font-sans ml-1">
                  Tıp literatürü ve amfi notları taranıyor...
                </span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick Suggestion Chips */}
        <div className="px-4 py-2 border-t border-line-soft bg-slate-50/70 overflow-x-auto flex items-center gap-2 scrollbar-none shrink-0">
          <span className="text-[11px] font-semibold text-ink-3 uppercase tracking-wider shrink-0 mr-1 flex items-center gap-1">
            <Lightbulb className="w-3.5 h-3.5 text-accent" />
            Öneriler:
          </span>
          {quickChips.map((chip, cIdx) => {
            const Icon = chip.icon;
            return (
              <button
                key={cIdx}
                type="button"
                disabled={isLoading}
                onClick={() => handleSendMessage(chip.prompt)}
                className="whitespace-nowrap px-2.5 py-1 rounded-full bg-white border border-line-2 hover:border-accent hover:bg-accent-soft text-ink hover:text-accent text-[12px] font-medium transition-all shrink-0 cursor-pointer disabled:opacity-50 flex items-center gap-1.5 shadow-2xs"
              >
                <Icon className="w-3 h-3 text-accent" />
                <span>{chip.label}</span>
              </button>
            );
          })}
        </div>

        {/* Chat Input Bar */}
        <footer className="p-3 sm:p-4 border-t border-line bg-white shrink-0">
          <div className="flex items-end gap-2 bg-canvas border border-line-2 rounded-2xl p-1.5 focus-within:border-accent focus-within:ring-2 focus-within:ring-accent/15 transition-all">
            <textarea
              ref={inputRef}
              rows={2}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              placeholder="Soru hakkında aklına takılanı sor... (Örn: Neden A şıkkı olamaz?)"
              className="flex-1 bg-transparent border-0 outline-none resize-none px-2 py-1 text-[14px] text-ink placeholder:text-ink-3 max-h-32 min-h-[44px]"
            />
            <button
              type="button"
              disabled={!inputMessage.trim() || isLoading}
              onClick={() => handleSendMessage()}
              aria-label="Mesajı Gönder"
              className="w-10 h-10 rounded-xl bg-accent hover:bg-accent-hover text-white flex items-center justify-center shrink-0 cursor-pointer transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-xs"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          <div className="flex items-center justify-between text-[11px] text-ink-3 px-1 pt-2">
            <span>Enter: Gönder · Shift+Enter: Yeni satır</span>
            {lastUsedProvider && (
              <span className="font-mono text-[10px] text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded">
                ⚡ {lastUsedProvider}
              </span>
            )}
          </div>
        </footer>
      </aside>
    </>
  );
};
