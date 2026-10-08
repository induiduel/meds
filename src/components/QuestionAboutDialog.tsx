import React, { useState } from 'react';
import { BookOpen, Check, Copy, Eye, FileText, GraduationCap, Presentation, ShieldCheck, History, Sparkles, AlertCircle } from 'lucide-react';
import { Dialog } from './ui/Dialog';
import { SourceText } from './ui/SourceText';
import { QuestionInsightsPanel } from './QuestionInsightsPanel';
import { QuestionLearnMatch } from '../services/learnMatcher';

export const normalizeRefList = (raw: any): string[] => {
  if (!raw) return [];
  if (Array.isArray(raw)) return raw.map((r) => String(r || '').trim()).filter(Boolean);
  if (typeof raw === 'string') {
    const trimmed = raw.trim();
    if (!trimmed) return [];
    if (trimmed.includes('\n')) {
      return trimmed.split(/\r?\n/).map((s) => s.trim().replace(/^[-*•\d.]+\s*/, '')).filter(Boolean);
    }
    if (trimmed.includes(';') && !trimmed.includes('&')) {
      return trimmed.split(/;/).map((s) => s.trim()).filter(Boolean);
    }
    return [trimmed];
  }
  return [];
};

interface Props {
  questionId: string;
  title: string;
  subtitle?: string;
  facts: { label: string; value?: React.ReactNode; mono?: boolean; wide?: boolean }[];
  explanation?: string;
  explanationNote?: React.ReactNode;
  evidence?: string;
  evidenceTitle?: string;
  /** Kendini sına modunda şık seçilmeden açıklama gizli kalır */
  answerHidden?: boolean;
  /** Açıklamada işaretlenecek doğru şık ifadeleri */
  answerTerms?: string[];
  sikAnalizi?: Record<string, string>;
  referanslar?: any;
  denetleyiciOnayi?: boolean;
  learnMatch?: QuestionLearnMatch | null;
  p14StatusNote?: string;
  isEskiView?: boolean;
  /** Denetleyici incelemesinde değişen cevap anahtarı */
  answerChange?: { from: string; to: string };
  onOpenSlide?: (kaynak: string, sayfa: number) => void;
  onPreviewSlide?: () => void;
  onOpenInLearn?: () => void;
  onShowSource?: () => void;
  onClose: () => void;
}

const H = ({ children }: { children: React.ReactNode }) => (
  <h3 className="m-0 text-[11.5px] font-bold uppercase tracking-[0.07em] text-ink-3 flex items-center gap-1.5">{children}</h3>
);

/**
 * Çıkmış soru "Hakkında": kimlik ve müfredat künyesi, ilgili slayt, açıklama, kanıt ve terimler tek, kompakt pencerede.
 * Kartta yer kaplamasınlar diye üç nokta menüsünden ve kart altındaki (i) ikonundan açılır.
 */
export const QuestionAboutDialog: React.FC<Props> = ({
  questionId,
  title,
  subtitle,
  facts,
  explanation,
  explanationNote,
  evidence,
  evidenceTitle = 'Ders notu kanıtı',
  answerHidden,
  answerTerms,
  sikAnalizi,
  referanslar,
  denetleyiciOnayi,
  answerChange,
  learnMatch,
  p14StatusNote,
  isEskiView,
  onOpenSlide,
  onPreviewSlide,
  onOpenInLearn,
  onShowSource,
  onClose,
}) => {
  const [copied, setCopied] = useState(false);
  const [reveal, setReveal] = useState(false);
  const hidden = answerHidden && !reveal;

  const copyId = () => {
    navigator.clipboard?.writeText(questionId).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    }).catch(() => {});
  };

  return (
    <Dialog
      width="max-w-2xl"
      title={title}
      subtitle={subtitle}
      onClose={onClose}
      footer={
        <>
          {onShowSource && (
            <button type="button" onClick={onShowSource} className="ms-btn is-ghost mr-auto">
              <FileText /> Kaynak belge
            </button>
          )}
          <button type="button" onClick={onClose} className="ms-btn">Kapat</button>
        </>
      }
    >
      {/* Durum Bildirimleri (Eski sürüm, Faz 14 vb.) */}
      {isEskiView && (
        <div className="p-3 bg-warn/10 border border-warn/20 rounded-xl text-[12.5px] text-warn flex items-start gap-2.5 mb-1">
          <History className="w-4 h-4 shrink-0 text-warn mt-0.5" />
          <span><b>Eski Sınav Arşiv Sürümü:</b> Doğrulanmış ve gerekçelendirilmiş hâl için Denetleyici Sürümüne geçebilirsiniz.</span>
        </div>
      )}
      {answerChange && (
        <div className="p-3 bg-warn-soft border border-warn/20 rounded-xl text-[12.5px] text-ink flex items-start gap-2.5 mb-1">
          <AlertCircle className="w-4 h-4 shrink-0 text-warn mt-0.5" />
          <span><b>Cevap düzeltildi:</b> Eski sınav arşivindeki cevap ({answerChange.from}) literatür incelemesi sonucunda <b>{answerChange.to}</b> olarak güncellendi.</span>
        </div>
      )}
      {p14StatusNote && (
        <div className="p-3 bg-accent-soft/40 border border-accent/20 rounded-xl text-[12.5px] text-ink flex items-start gap-2.5 mb-1">
          <Sparkles className="w-4 h-4 shrink-0 text-accent mt-0.5" />
          <span>{p14StatusNote}</span>
        </div>
      )}

      {/* Künye */}
      <dl className="ms-about-facts">
        <div className="is-wide">
          <dt>Soru kimliği</dt>
          <dd className="flex items-center gap-1 min-w-0">
            <span className="font-mono text-[12.5px] truncate" title={questionId}>{questionId}</span>
            <button type="button" onClick={copyId} className="ms-btn is-ghost is-icon is-sm shrink-0" aria-label="Kimliği kopyala" title="Kimliği kopyala">
              {copied ? <Check className="text-ok" /> : <Copy />}
            </button>
          </dd>
        </div>
        {facts.filter((f) => f.value).map((f) => (
          <div key={f.label} className={f.wide ? 'is-wide' : ''}>
            <dt>{f.label}</dt>
            <dd className={f.mono ? 'font-mono' : ''}>{f.value}</dd>
          </div>
        ))}
      </dl>

      {/* İlgili slayt */}
      {learnMatch && (
        <section className="flex flex-col gap-1.5">
          <H><Presentation className="w-3.5 h-3.5" /> İlgili slayt</H>
          <div className="ms-about-slide">
            <span className="ms-about-slide-num" aria-hidden>{learnMatch.slideNumber}</span>
            <span className="min-w-0 flex-1">
              <span className="block text-[13.5px] font-semibold text-ink truncate">{learnMatch.slideTitle || `Slayt ${learnMatch.slideNumber}`}</span>
              <span className="block text-[12px] text-ink-3 truncate">
                {learnMatch.deckTitle} · {learnMatch.matchType === 'direct' ? 'müfredat eşleşmesi' : 'konu eşleşmesi'}
              </span>
            </span>
            {onPreviewSlide && (
              <button type="button" onClick={onPreviewSlide} className="ms-btn is-ghost is-sm shrink-0" title="Slayt özetini burada gör">
                <Eye /> <span className="hidden sm:inline">Önizle</span>
              </button>
            )}
            {onOpenInLearn && (
              <button type="button" onClick={onOpenInLearn} className="ms-btn is-tonal is-sm shrink-0" title="Öğren'de aç; soru ve doğru şık slaytta işaretlenir">
                <GraduationCap /> Öğren'de aç
              </button>
            )}
          </div>
        </section>
      )}

      {/* Açıklama */}
      {explanation && (
        <section className="flex flex-col gap-2">
          <H>
            <BookOpen className="w-3.5 h-3.5" /> 
            {denetleyiciOnayi ? 'Tıbbi Açıklama & Patofizyolojik Mekanizma' : 'Açıklama'} {explanationNote}
          </H>
          {hidden ? (
            <div className="rounded-xl bg-field px-3.5 py-3 flex flex-wrap items-center gap-2 text-[13px] text-ink-2">
              Açıklama cevabı gösterir. Önce şıkkını seç ya da
              <button type="button" onClick={() => setReveal(true)} className="ms-btn is-ghost is-sm">
                <Eye /> yine de göster
              </button>
            </div>
          ) : (
            <SourceText text={explanation} answerTerms={answerTerms} />
          )}
        </section>
      )}

      {/* Şık Analizleri & Çürütmeler */}
      {sikAnalizi && Object.keys(sikAnalizi).length > 0 && !hidden && (
        <section className="flex flex-col gap-2">
          <H><ShieldCheck className="w-3.5 h-3.5 text-ok" /> Şık analizi & patofizyolojik mekanizma</H>
          <div className="flex flex-col gap-1.5 rounded-xl bg-field p-3 text-[13px]">
            {Object.entries(sikAnalizi).sort(([a], [b]) => a.localeCompare(b)).map(([k, text]) => {
              const isCorrect = String(text).toUpperCase().startsWith('DOĞRU');
              return (
                <div key={k} className="flex items-start gap-2 py-1 border-b border-line-2/40 last:border-b-0">
                  <span className={`px-2 py-0.5 rounded text-[11px] font-mono font-bold shrink-0 ${isCorrect ? 'bg-ok-soft text-ok' : 'bg-bad-soft text-bad-text'}`}>
                    {k}
                  </span>
                  <span className="text-ink leading-relaxed text-[12.5px]">{text}</span>
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* Standart Referans Kaynaklar */}
      {(() => {
        const cleanRefs = normalizeRefList(referanslar);
        if (!cleanRefs.length || hidden) return null;
        return (
          <section className="flex flex-col gap-1.5">
            <H><BookOpen className="w-3.5 h-3.5" /> Standart Referans Tıp Kaynakları</H>
            <ul className="m-0 pl-4 text-[12.5px] text-ink-2 list-disc flex flex-col gap-1">
              {cleanRefs.map((ref, idx) => (
                <li key={idx} className="leading-snug">{ref}</li>
              ))}
            </ul>
          </section>
        );
      })()}

      {evidence && !hidden && (
        <section className="flex flex-col gap-2">
          <H>{evidenceTitle}</H>
          <div className="ms-about-quote">
            <SourceText text={evidence} size="sm" answerTerms={answerTerms} />
          </div>
        </section>
      )}

      {/* Müfredat, terimler, ilgili sayfalar (analiz varsa) */}
      <section className="flex flex-col gap-2">
        <H>Müfredat ve terimler</H>
        <QuestionInsightsPanel questionId={questionId} bare onOpenSlide={onOpenSlide} />
      </section>
    </Dialog>
  );
};
