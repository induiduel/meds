import React, { useState } from 'react';
import { BookOpen, Check, Copy, Eye, FileText, GraduationCap, Presentation } from 'lucide-react';
import { Dialog } from './ui/Dialog';
import { SourceText } from './ui/SourceText';
import { QuestionInsightsPanel } from './QuestionInsightsPanel';
import { QuestionLearnMatch } from '../services/learnMatcher';

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
  learnMatch?: QuestionLearnMatch | null;
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
 * Kartta yer kaplamasınlar diye üç nokta menüsünden açılır.
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
  learnMatch,
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
          <H><BookOpen className="w-3.5 h-3.5" /> Açıklama {explanationNote}</H>
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
        <QuestionInsightsPanel questionId={questionId} bare />
      </section>
    </Dialog>
  );
};
