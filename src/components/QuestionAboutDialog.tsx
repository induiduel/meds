import React, { useState } from 'react';
import { BookOpen, Check, Copy, Eye, FileText, GraduationCap, Presentation, ShieldCheck, History, Sparkles, AlertCircle, Code2 } from 'lucide-react';
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
  /** Doğru şık ve metni (cevap özeti için) */
  answerKey?: string;
  options?: { key: string; text: string }[];
  /** Denetleyici incelemesinde değişen cevap anahtarı */
  answerChange?: { from: string; to: string };
  question?: any;
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
  answerKey,
  options,
  learnMatch,
  p14StatusNote,
  isEskiView,
  question,
  onOpenSlide,
  onPreviewSlide,
  onOpenInLearn,
  onShowSource,
  onClose,
}) => {
  const [copied, setCopied] = useState(false);
  const [copiedJson, setCopiedJson] = useState(false);
  const [reveal, setReveal] = useState(false);
  const hidden = answerHidden && !reveal;
  const answerOptionText = options?.find((o) => String(o.key).toUpperCase() === String(answerKey || '').toUpperCase())?.text;
  const optionText = (k: string) => options?.find((o) => String(o.key).toUpperCase() === k.toUpperCase())?.text;

  const copyId = () => {
    navigator.clipboard?.writeText(questionId).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    }).catch(() => {});
  };

  const copyJson = () => {
    const dataToCopy = question || {
      id: questionId,
      answerKey,
      options,
      explanation,
      evidence,
      sikAnalizi,
      referanslar,
      facts,
    };
    navigator.clipboard?.writeText(JSON.stringify(dataToCopy, null, 2)).then(() => {
      setCopiedJson(true);
      setTimeout(() => setCopiedJson(false), 1600);
    }).catch(() => {});
  };

  return (
    <Dialog
      width="max-w-3xl"
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
          <button
            type="button"
            onClick={copyJson}
            className="ms-btn is-ghost"
            title="Soru veri tabanı kaydını JSON olarak panoya kopyala"
          >
            {copiedJson ? <Check className="text-ok" /> : <Code2 />}
            {copiedJson ? 'JSON Kopyalandı' : 'JSON Kopyala'}
          </button>
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
      {p14StatusNote && (
        <div className="p-3 bg-accent-soft/40 border border-accent/20 rounded-xl text-[12.5px] text-ink flex items-start gap-2.5 mb-1">
          <Sparkles className="w-4 h-4 shrink-0 text-accent mt-0.5" />
          <span>{p14StatusNote}</span>
        </div>
      )}


      {/* Cevap özeti */}
      {answerKey && !hidden && (
        <div className="ms-about-answer">
          <span className="ms-about-answer-key" aria-label={`Doğru cevap ${answerKey}`}>{answerKey}</span>
          <div className="min-w-0 flex-1 flex flex-col gap-0.5">
            <span className="text-[11.5px] font-semibold text-ok">Doğru cevap</span>
            {answerOptionText && <span className="text-[14px] font-medium text-ink leading-snug">{answerOptionText}</span>}
            {answerChange && (
              <span className="mt-1 inline-flex items-start gap-1.5 text-[12.5px] text-ink-2">
                <AlertCircle className="w-3.5 h-3.5 shrink-0 text-warn mt-0.5" />
                <span><b className="text-ink">Cevap düzeltildi:</b> eski arşivde <b className="font-mono">{answerChange.from}</b> idi; literatür incelemesiyle <b className="font-mono">{answerChange.to}</b> olarak güncellendi.</span>
              </span>
            )}
          </div>
        </div>
      )}

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
            {denetleyiciOnayi ? 'Açıklama ve patofizyolojik mekanizma' : 'Açıklama'} {explanationNote}
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
          <H><ShieldCheck className="w-3.5 h-3.5 text-ok" /> Şık analizi</H>
          <ol className="ms-about-analysis">
            {Object.entries(sikAnalizi).sort(([a], [b]) => a.localeCompare(b)).map(([k, raw]) => {
              const m = String(raw).match(/^\s*(DOĞRU|YANLIŞ|TARTIŞMALI)(?:\s*\/\s*(TARTIŞMALI|YANLIŞ|DOĞRU))?\s*[:\-–]\s*/i);
              const verdict = m ? m[1].toLocaleUpperCase('tr-TR') : '';
              const disputed = m && /TARTIŞMALI/i.test(m[0]);
              const tone = disputed ? 'is-warn' : verdict === 'DOĞRU' ? 'is-ok' : verdict === 'YANLIŞ' ? 'is-bad' : '';
              const label = disputed ? (verdict === 'TARTIŞMALI' ? 'Tartışmalı' : `${verdict === 'DOĞRU' ? 'Doğru' : 'Yanlış'} · tartışmalı`) : verdict === 'DOĞRU' ? 'Doğru ifade' : verdict === 'YANLIŞ' ? 'Yanlış ifade' : '';
              const reason = m ? String(raw).slice(m[0].length) : String(raw);
              const isAnswer = answerKey && k.toUpperCase() === answerKey.toUpperCase();
              return (
                <li key={k} className={isAnswer ? 'is-answer' : ''}>
                  <span className="ms-about-analysis-key">{k}</span>
                  <div className="min-w-0 flex-1 flex flex-col gap-1">
                    <div className="flex flex-wrap items-center gap-1.5">
                      {optionText(k) && <span className="text-[13.5px] font-medium text-ink leading-snug mr-1">{optionText(k)}</span>}
                      {label && <span className={`ms-tag ${tone}`}>{label}</span>}
                      {isAnswer && <span className="ms-tag is-ok"><Check /> Cevap</span>}
                    </div>
                    <p className="m-0 text-[13px] text-ink-2 leading-relaxed">{reason}</p>
                  </div>
                </li>
              );
            })}
          </ol>
        </section>
      )}

      {/* Standart Referans Kaynaklar */}
      {(() => {
        const cleanRefs = normalizeRefList(referanslar);
        if (!cleanRefs.length || hidden) return null;
        return (
          <section className="flex flex-col gap-1.5">
            <H><BookOpen className="w-3.5 h-3.5" /> Referans kaynaklar</H>
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

      <section className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <H>Künye</H>
          <button
            type="button"
            onClick={copyJson}
            className="ms-btn is-ghost is-sm text-[12px] h-7 px-2.5 gap-1.5"
            title="Soru veri tabanı kaydını JSON olarak panoya kopyala"
          >
            {copiedJson ? <Check className="w-3.5 h-3.5 text-ok" /> : <Code2 className="w-3.5 h-3.5" />}
            <span>{copiedJson ? 'JSON Kopyalandı' : 'JSON Kopyala'}</span>
          </button>
        </div>
        {/* Künye */}
        <dl className="ms-about-facts">
          <div>
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
      </section>

      {/* Müfredat, terimler, ilgili sayfalar (analiz varsa) */}
      <section className="flex flex-col gap-2">
        <H>Müfredat ve terimler</H>
        <QuestionInsightsPanel questionId={questionId} bare onOpenSlide={onOpenSlide} />
      </section>
    </Dialog>
  );
};
