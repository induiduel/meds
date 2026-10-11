import React, { useState } from 'react';
import { logActivity } from '../services/activityLog';
import { FileWarning, ListX, CircleX, Tags, Sparkles, MoreHorizontal, AlertCircle, Send } from 'lucide-react';
import { BlurOverlay, SuccessCheck } from './ui/Animations';
import { toast } from './ui/Toast';
import { Sheet } from './ui/Sheet';

const REASONS: { id: string; label: string; hint: string; icon: React.ElementType; placeholder: string }[] = [
  { id: 'Hatalı Soru Kökü', label: 'Soru kökü', hint: 'Eksik ya da hatalı', icon: FileWarning, placeholder: 'Kökte neyin eksik ya da yanlış olduğunu yaz…' },
  { id: 'Yanlış / Eksik Şıklar', label: 'Şıklar', hint: 'Eksik ya da yanlış', icon: ListX, placeholder: 'Hangi şık eksik ya da hatalı? Doğrusu ne olmalı?' },
  { id: 'Hatalı Doğru Cevap', label: 'Cevap yanlış', hint: 'Anahtar hatalı', icon: CircleX, placeholder: 'Neden bu cevap olmalı? Kaynak ya da hocanın vurgusu…' },
  { id: 'Hatalı Branş / Kurul Eşleşmesi', label: 'Ders / kurul', hint: 'Yanlış eşleşme', icon: Tags, placeholder: 'Hangi ders ya da kurula ait olmalı?' },
  { id: 'Yapay Zeka Redaksiyon Hatası', label: 'AI düzenlemesi', hint: 'Anlamı bozmuş', icon: Sparkles, placeholder: 'AI düzenlemesi soruyu nasıl bozmuş?' },
  { id: 'Diğer', label: 'Başka bir şey', hint: 'İtiraz, öneri', icon: MoreHorizontal, placeholder: 'Sorunu kısaca anlat…' },
];
const KEYS = ['A', 'B', 'C', 'D', 'E'];

/** Şıkka itiraz türleri (şık, mevcut cevap olup olmamasına göre süzülür) */
const OBJECTIONS: { id: string; label: string; when: 'correct' | 'other' | 'any' }[] = [
  { id: 'dogru-olmali', label: 'Doğru cevap bu şık olmalı', when: 'other' },
  { id: 'isaretli-yanlis', label: 'İşaretli cevap yanlış', when: 'correct' },
  { id: 'bu-da-dogru', label: 'Bu şık da doğru (birden fazla doğru var)', when: 'other' },
  { id: 'metin-hatali', label: 'Şık metni hatalı ya da eksik', when: 'any' },
  { id: 'diger', label: 'Başka bir itiraz', when: 'any' },
];

interface ReportQuestionModalProps {
  question: any;
  onClose: () => void;
  onSubmit: (reason: string, details: string) => Promise<void>;
  /** Verilirse pencere "şıkka itiraz" biçiminde açılır */
  objectOption?: { key: string; text: string };
  /** Soru güncellenince e-postanın gideceği adres (yönetici ve giriş yapmamış kullanıcı için verilmez) */
  notifyEmail?: string | null;
}

/** "Hata bildir": pick what is wrong, optionally the right answer and a note. Bottom sheet on phones. */
export const ReportQuestionModal: React.FC<ReportQuestionModalProps> = ({ question, onClose, onSubmit, objectOption, notifyEmail }) => {
  const objection = Boolean(objectOption);
  const [reason, setReason] = useState<string | null>(null);
  const [suggested, setSuggested] = useState<string | null>(null);
  const [details, setDetails] = useState('');
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const stem: string = question?.reconstruction?.stem || question?.stem || question?.rawQuestion?.stem || question?.topic || '';
  const current = question?.reconstruction?.correctAnswer || question?.correctAnswer || question?.claimedAnswer || question?.answer;
  const objKey = String(objectOption?.key || '').toUpperCase();
  const objIsCurrent = objection && !!current && String(current).toUpperCase() === objKey;
  const objectionList = OBJECTIONS.filter((o) => o.when === 'any' || (o.when === 'correct') === objIsCurrent);
  const meta = [question?.questionNumber ? `Soru #${question.questionNumber}` : '', question?.discipline, question?.examYear].filter(Boolean).join(' · ');
  const chosen = REASONS.find((r) => r.id === reason);

  const submit = async () => {
    if (!reason) {
      setError('Önce sorunun ne olduğunu seç.');
      return;
    }
    setError(null);
    setBusy(true);
    try {
      if (objection) {
        const o = OBJECTIONS.find((x) => x.id === reason);
        const text = [
          `İtiraz edilen şık: ${objKey}) ${objectOption?.text || ''}`.trim(),
          current ? `Mevcut cevap: ${current}` : '',
          reason === 'dogru-olmali' ? `Önerilen doğru cevap: ${objKey}` : '',
          details.trim(),
        ].filter(Boolean).join('\n');
        await onSubmit(`Şık itirazı (${objKey}) · ${o?.label || 'İtiraz'}`, text);
      } else {
        const text = [suggested ? `Önerilen doğru cevap: ${suggested}` : '', details.trim()].filter(Boolean).join('\n');
        await onSubmit(reason, text);
      }
      logActivity('katki', 'Hata bildirdin');
      setDone(true);
      setTimeout(onClose, 1700);
    } catch (e: any) {
      setError('Gönderilemedi: ' + (e?.message || 'bilinmeyen hata') + '. Tekrar dener misin?');
      toast.error('Bildirim gönderilemedi', e?.message || 'Bağlantını kontrol edip tekrar dene.');
    } finally {
      setBusy(false);
    }
  };

  const doneView = (
          <div role="status" className="row-span-2 flex flex-col items-center justify-center gap-2 px-6 py-12 text-center">
            <SuccessCheck size={96} />
            <p className="m-0 font-display text-2xl font-bold tracking-[-0.02em]">Teşekkürler!</p>
            <p className="m-0 text-md text-ink-2 max-w-[320px]">{objection ? 'İtirazın bize ulaştı. Şıkkı kaynakla karşılaştırıp inceleyeceğiz.' : 'Bildirimin bize ulaştı. Soruyu inceleyip düzelteceğiz.'}</p>
          </div>
  );
  const bodyView = (
            <div className="overflow-y-auto px-5 pb-4 flex flex-col gap-4">
              {stem && (
                <blockquote className="m-0 rounded-xl bg-canvas px-3.5 py-3 text-base leading-[1.55] text-ink-2 line-clamp-3 border-l-[3px] border-line-2">
                  {stem}
                </blockquote>
              )}

              {objection && (
                <section className="flex flex-col gap-2">
                  <div className="flex items-start gap-2.5 rounded-xl border border-bad/30 bg-bad-soft/60 px-3 py-2.5">
                    <span className="w-7 h-7 rounded-lg bg-bad text-white font-mono text-sm font-semibold inline-flex items-center justify-center shrink-0">{objKey}</span>
                    <span className="min-w-0 text-base leading-[1.5] text-ink pt-0.5">{objectOption?.text}</span>
                  </div>
                  {current && <span className="text-sm text-ink-3">Şu an işaretli cevap: <b className="font-mono text-ink">{String(current).toUpperCase()}</b></span>}
                  <span className="text-xs font-semibold uppercase tracking-[0.07em] text-ink-3 pt-1">İtirazın ne?</span>
                  <div role="radiogroup" aria-label="İtiraz türü" className="flex flex-col gap-1.5">
                    {objectionList.map((o) => {
                      const on = reason === o.id;
                      return (
                        <button
                          key={o.id}
                          type="button"
                          role="radio"
                          aria-checked={on}
                          onClick={() => { setReason(o.id); setError(null); }}
                          className={`min-h-11 px-3 py-2 rounded-xl border text-left text-base flex items-center gap-2.5 cursor-pointer transition-colors ${
                            on ? 'border-bad bg-bad-soft font-semibold text-ink' : 'border-line bg-white hover:border-line-2 text-ink'
                          }`}
                        >
                          <span className={`w-4 h-4 rounded-full border-2 shrink-0 ${on ? 'border-bad bg-bad shadow-[inset_0_0_0_2px_white]' : 'border-line-2'}`} aria-hidden />
                          {o.label}
                        </button>
                      );
                    })}
                  </div>
                </section>
              )}

              {!objection && (
              <section className="flex flex-col gap-2">
                <span className="text-xs font-semibold uppercase tracking-[0.07em] text-ink-3">Sorun ne?</span>
                <div role="radiogroup" aria-label="Sorun türü" className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {REASONS.map((r) => {
                    const on = reason === r.id;
                    const Icon = r.icon;
                    return (
                      <button
                        key={r.id}
                        type="button"
                        role="radio"
                        aria-checked={on}
                        onClick={() => {
                          setReason(r.id);
                          setError(null);
                          if (r.id !== 'Hatalı Doğru Cevap') setSuggested(null);
                        }}
                        className={`min-h-[78px] px-3 py-2.5 rounded-xl border text-left flex flex-col gap-1.5 cursor-pointer transition-all ${
                          on ? 'border-bad bg-bad-soft shadow-xs' : 'border-line bg-white hover:border-line-2'
                        }`}
                      >
                        <Icon className={`w-[18px] h-[18px] ${on ? 'text-bad-text' : 'text-ink-3'}`} />
                        <span className="flex flex-col">
                          <span className={`text-base leading-tight ${on ? 'font-semibold text-ink' : 'font-medium text-ink'}`}>{r.label}</span>
                          <span className="text-xs text-ink-3 leading-tight">{r.hint}</span>
                        </span>
                      </button>
                    );
                  })}
                </div>
              </section>
              )}

              {!objection && reason === 'Hatalı Doğru Cevap' && (
                <section className="ms-pop-in flex flex-col gap-2">
                  <span className="text-xs font-semibold uppercase tracking-[0.07em] text-ink-3">
                    Sence doğrusu{current ? ` (şu an ${current})` : ''}
                  </span>
                  <div className="grid grid-cols-5 gap-1.5">
                    {KEYS.map((k) => {
                      const on = suggested === k;
                      return (
                        <button
                          key={k}
                          type="button"
                          aria-pressed={on}
                          onClick={() => setSuggested(on ? null : k)}
                          className={`h-11 rounded-xl font-mono text-md font-semibold cursor-pointer transition-colors ${
                            on ? 'bg-ok text-white' : k === current ? 'bg-field text-ink-3 line-through' : 'bg-field text-ink hover:bg-line-soft'
                          }`}
                        >
                          {k}
                        </button>
                      );
                    })}
                  </div>
                </section>
              )}

              <section className="flex flex-col gap-2">
                <label htmlFor="report-details" className="text-xs font-semibold uppercase tracking-[0.07em] text-ink-3">
                  Açıklama <span className="normal-case tracking-normal font-normal">· isteğe bağlı</span>
                </label>
                <textarea
                  id="report-details"
                  rows={3}
                  value={details}
                  maxLength={600}
                  onChange={(e) => setDetails(e.target.value)}
                  placeholder={objection ? 'Kaynağın ya da gerekçen (ör. slayt, hocanın vurgusu)…' : chosen?.placeholder || 'Sorunu kısaca anlat…'}
                  className="resize-none rounded-xl bg-field border border-transparent px-3.5 py-3 text-md leading-[1.55] outline-0 focus:border-accent focus:bg-white placeholder:text-ink-2"
                />
                <span className="self-end text-xs text-ink-3 font-mono">{details.length}/600</span>
              </section>

              <p className="ms-report-queue">
                <Sparkles aria-hidden />
                <span>
                  Bildirimin, yazdığın notla birlikte yapay zekâ inceleme kuyruğuna eklenir; düzeltme gerekirse soru otomatik güncellenir.
                  {notifyEmail ? <> Güncellenince eski ve yeni hali <b>{notifyEmail}</b> adresine gönderilir.</> : null}
                </span>
              </p>

              {error && (
                <div role="alert" className="flex items-start gap-2 px-3 py-2.5 rounded-xl bg-bad-soft text-bad-text text-base">
                  <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-bad" />
                  <span>{error}</span>
                </div>
              )}
            </div>
  );
  const footerButtons = (
    <>
              <button
                type="button"
                onClick={onClose}
                disabled={busy}
                className="h-12 sm:h-11 px-4 rounded-xl text-md font-semibold text-ink-2 hover:bg-canvas cursor-pointer disabled:opacity-50"
              >
                Vazgeç
              </button>
              <button
                type="button"
                onClick={submit}
                disabled={busy || !reason}
                className="flex-1 sm:flex-none sm:ml-auto h-12 sm:h-11 px-6 rounded-xl bg-bad hover:bg-bad text-white text-md font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="w-4 h-4" />
                {objection ? 'İtirazı gönder' : 'Bildirimi gönder'}
              </button>
            </>
  );

      // v8: ortak alt sayfa (telefonda sürüklenir, geniş ekranda pencere)
  return (
    <Sheet
      open
      onClose={() => !busy && onClose()}
      title={objection ? `${objKey} şıkkına itiraz` : 'Hata bildir'}
      subtitle={meta || 'Çıkmış soru'}
      width={540}
      footer={done ? undefined : footerButtons}
    >
      <div className="rq">{done ? doneView : bodyView}</div>
      <BlurOverlay show={busy} label="Gönderiliyor…" rounded="rounded-none" />
    </Sheet>
  );
};
