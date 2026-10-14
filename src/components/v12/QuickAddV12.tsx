import React from 'react';
import {
  AlertCircle, ArrowRight, CheckCircle2, CheckSquare, ChevronDown, Copy, FileText, Layers, Link2, Lock, Plus, Square, Wand2, X,
} from 'lucide-react';
import type { Committee, QuestionItem } from '../../types';
import type { SimilarPastQuestion, SourceRefLite } from '../../services/api';
import type { RealtimeMatchItem } from '../../services/draftClusteringService';
import type { SmartQuestionAssistantResult } from '../../services/medicalPredictorService';
import { FastTextarea } from '../ui/FastTextarea';
import { BlurOverlay } from '../ui/Animations';
import { ComposerAssist } from '../quickadd/ComposerAssist';
import { IntakeEcho } from '../quickadd/IntakeEcho';
import { Colored, WordLegend, ContextBadge } from '../draftHighlight';
import '../../styles/v12/pool.css';

/**
 * Soru ekle — v12 "Net" (canvas panosu Pool.dc.html, sağ yarı).
 * Yalnız gösterim: bütün durum, arama/eşleşme, taslak ve gönderim mantığı QuickAddHero'da kalır, buraya props ile gelir.
 *  - Künye (kurul, ders, sınav yılı, soru no) · soru kökü (FastTextarea + ComposerAssist) · YZ önerisi kutusu
 *  - Şıklar A–E: satır ekle/kaldır (en çok 5) · Cevap segmenti (A–E + Bilmiyorum) · İpucu / hatırladığım
 *  - Canlı: havuzdaki benzer taslaklar (gerçek eşleşme olasılığı), benzer çıkmış sorular, kaynak eşleşmeleri
 *  - Alt çubuk: Taslak olarak kaydet / Havuza gönder. YZ'nin önerdiği ya da tamamladığı her şey İnceleniyor etiketlidir.
 * Geniş kapta (≥ 900 px) form solda, canlı sonuçlar sağda; daha darda alt alta.
 */

export type QaOptionKey = 'A' | 'B' | 'C' | 'D' | 'E';
const KEYS: QaOptionKey[] = ['A', 'B', 'C', 'D', 'E'];
const ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI'];

export interface QuickAddV12Props {
  committee?: Committee;
  committees: Committee[];
  activeCommitteeId: string;
  committeeLabel: (c: Committee) => string;
  isCommitteeLocked: (id: string) => boolean;
  onSelectCommittee: (id: string) => void;
  isLocked: boolean;
  isCollecting: boolean;

  disciplines: string[];
  discipline: string;
  onDiscipline: (d: string) => void;
  discAuto: boolean;
  examYear: string;
  onExamYear: (v: string) => void;
  years: string[];
  currentYear: string;
  questionNumber: string;
  onQuestionNumber: (v: string) => void;
  numAuto: boolean;

  stem: string;
  onStem: (v: string) => void;
  stemPlaceholder: string;
  clue: string;
  onClue: (v: string) => void;
  cluePlaceholder: string;

  qType: 'klasik' | 'onculu' | null;
  onQType: (t: 'klasik' | 'onculu') => void;
  premises: string[];
  premiseMax: number;
  onPremiseAt: (i: number, v: string) => void;
  onAddPremise: (after?: number) => void;
  onRemovePremise: (i: number) => void;
  onPastePremises: (i: number, e: React.ClipboardEvent<HTMLInputElement>) => void;
  looksOnculu: boolean;
  stemPremiseCount: number;
  onExtractPremises: () => void;
  truePremises: Set<string> | null;
  filledPremiseCount: number;
  onFillStandard: () => void;
  comboChips: string[];
  onFillNext: (text: string) => void;

  options: Record<QaOptionKey, string>;
  setOptions: React.Dispatch<React.SetStateAction<Record<QaOptionKey, string>>>;
  optionCount: number;
  setOptionCount: React.Dispatch<React.SetStateAction<number>>;
  answer?: QaOptionKey;
  onAnswer: (k: QaOptionKey | undefined) => void;
  answerReason: string;
  onAnswerReason: (v: string) => void;

  linkedQuestion: QuestionItem | null;
  onUnlink: () => void;

  isSearching: boolean;
  queryText: string;
  matches: RealtimeMatchItem[];
  selectedMatchIds: Set<string>;
  onToggleMatch: (id: string) => void;
  onSelectAllMatches: () => void;
  onClearMatchSelection: () => void;
  onLink: (q: QuestionItem) => void;
  onReject: (id: string) => void;
  onMerge: () => void;
  isMerging: boolean;
  isAdmin: boolean;
  onOptimize: (q: QuestionItem) => void;
  sharedColors: Map<string, string>;
  highlightMin: number;
  stemOf: (q: QuestionItem) => string;
  similar: SimilarPastQuestion[];
  onTransfer: (s: SimilarPastQuestion) => void;
  onCopyStem: (stem: string) => void;
  sources: SourceRefLite[];
  assistant: SmartQuestionAssistantResult | null;
  onApplyCommittee: () => void;
  onApplyDiscipline: (d: string) => void;

  savedDraftAt: string | null;
  formEmpty: boolean;
  onSaveDraft: () => void;
  onRestoreDraft: () => void;
  onDropDraft: () => void;
  formError: string | null;
  successMessage: string | null;
  intakeId: string | null;
  onCloseIntake: () => void;
  isSubmitting: boolean;
  onSubmit: (e: React.FormEvent) => void;
}

const timeOf = (iso: string) => new Date(iso).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
const dayOf = (iso: string) => {
  const d = new Date(iso);
  return d.toDateString() === new Date().toDateString()
    ? `${timeOf(iso)}'da kaydedildi`
    : `${d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })} ${timeOf(iso)}`;
};
const focusId = (id: string) => window.setTimeout(() => document.getElementById(id)?.focus(), 0);

export const QuickAddV12: React.FC<QuickAddV12Props> = (p) => {
  const lastFilled = KEYS.reduce((n, k, i) => (p.options[k].trim() ? i + 1 : n), 0);
  const answerIdx = p.answer ? KEYS.indexOf(p.answer) + 1 : 0;
  const vis = Math.min(5, Math.max(2, p.optionCount, lastFilled, answerIdx));
  const visKeys = KEYS.slice(0, vis);

  const removeOption = (i: number) => {
    p.setOptions((prev) => {
      const vals = KEYS.map((k) => prev[k]);
      vals.splice(i, 1);
      vals.push('');
      return KEYS.reduce((acc, k, j) => ({ ...acc, [k]: vals[j] }), {} as Record<QaOptionKey, string>);
    });
    if (p.answer) {
      const ai = KEYS.indexOf(p.answer);
      if (ai === i) { p.onAnswer(undefined); p.onAnswerReason(''); }
      else if (ai > i) p.onAnswer(KEYS[ai - 1]);
    }
    p.setOptionCount(Math.max(1, vis - 1));
  };
  const addOption = () => {
    if (vis >= 5) return;
    p.setOptionCount(vis + 1);
    focusId(`q12-opt-${KEYS[vis]}`);
  };
  const pickCombo = (c: string) => {
    const el = document.activeElement as HTMLInputElement | null;
    const fk = el?.classList.contains('q12-opt-in') ? (el.dataset.k as QaOptionKey | undefined) : undefined;
    if (fk) p.setOptions((prev) => ({ ...prev, [fk]: c }));
    else p.onFillNext(c);
  };

  const submitOnCtrlEnter = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      e.currentTarget.form?.requestSubmit();
    }
  };

  const a = p.assistant;
  const crossSuggest = !!a?.crossCommitteeWarning && !!a.predictedCommittee;
  const discSuggest = !!a?.predictedDiscipline && a.predictedDiscipline.discipline !== p.discipline && p.disciplines.includes(a.predictedDiscipline.discipline);
  const topics = a?.suggestedTopics?.slice(0, 3) || [];
  const showSuggest = crossSuggest || discSuggest || topics.length > 0;

  const typed = p.stem.trim().length >= 6 || !!p.queryText;
  const nothing = p.matches.length === 0 && p.similar.length === 0 && p.sources.length === 0;
  const yearLabel = (y: string) => `${y.slice(0, 4)}–${y.slice(7, 9)}`;

  return (
    <div className="q12-add">
      <form
        className="q12-panel q12-addp"
        onSubmit={p.onSubmit}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && (e.target as HTMLElement).tagName === 'INPUT') e.preventDefault();
        }}
        aria-busy={p.isSubmitting}
        aria-labelledby="q12-add-h"
      >
        <BlurOverlay show={p.isSubmitting} label="Havuza ekleniyor…" hint="Benzer parçalar varsa aynı soruya bağlıyoruz" />
        <div className="q12-panel-h">
          <h1 className="q12-h2 q12-add-title" id="q12-add-h">Soru ekle</h1>
          <span className={`q12-live ${p.isCollecting ? 'is-on' : ''}`}>
            <i aria-hidden />{p.committee ? p.committeeLabel(p.committee) : 'Kurul'}{p.isCollecting ? ' · toplama açık' : ''}
          </span>
          <span className="q12-grow" />
          {p.savedDraftAt && !p.formEmpty && <span className="q12-meta">Taslak · {dayOf(p.savedDraftAt)}</span>}
        </div>

        <div className="q12-add-grid">
          <div className="q12-body">
            {p.isLocked && (
              <p className="q12-note is-warn" role="status"><Lock aria-hidden /><span>Ders programına göre sınav tamamlanmadan bu kurula soru yazılamaz.</span></p>
            )}
            {p.savedDraftAt && p.formEmpty && (
              <div className="q12-note" role="status">
                <FileText aria-hidden />
                <span className="q12-grow">Kaydedilmiş taslağın var · {dayOf(p.savedDraftAt)}</span>
                <button type="button" className="q12-btn is-sm" onClick={p.onRestoreDraft}>Geri yükle</button>
                <button type="button" className="q12-btn is-sm is-ghost" onClick={p.onDropDraft}>Sil</button>
              </div>
            )}

            <div className="q12-two">
              <div>
                <label className="q12-label" htmlFor="q12-kurul">Kurul</label>
                <span className="q12-field">
                  <select id="q12-kurul" value={p.committee?.id || ''} onChange={(e) => p.onSelectCommittee(e.target.value)}>
                    {!p.committee && <option value="">Seç</option>}
                    {p.committees.map((c) => {
                      const locked = p.isCommitteeLocked(c.id);
                      return (
                        <option key={c.id} value={c.id} disabled={locked}>
                          {p.committeeLabel(c)}{locked ? ' · açılmadı' : c.id === p.activeCommitteeId ? ' · toplama açık' : ''}
                        </option>
                      );
                    })}
                  </select>
                  <ChevronDown aria-hidden className="q12-field-chev" />
                </span>
              </div>
              <div>
                <label className="q12-label" htmlFor="q12-ders">
                  Ders{p.discAuto && <span className="q12-auto">otomatik</span>}
                </label>
                <span className="q12-field">
                  <select id="q12-ders" value={p.discipline} onChange={(e) => p.onDiscipline(e.target.value)}>
                    {p.disciplines.map((d) => <option key={d} value={d}>{d}</option>)}
                  </select>
                  <ChevronDown aria-hidden className="q12-field-chev" />
                </span>
              </div>
              <div>
                <label className="q12-label" htmlFor="q12-yil">Sınav yılı</label>
                <span className="q12-field">
                  <select id="q12-yil" value={p.examYear} onChange={(e) => p.onExamYear(e.target.value)}>
                    <option value="">Bilmiyorum</option>
                    {p.years.map((y) => <option key={y} value={y}>{yearLabel(y)}{y === p.currentYear ? ' · bu yıl' : ''}</option>)}
                  </select>
                  <ChevronDown aria-hidden className="q12-field-chev" />
                </span>
              </div>
              <div>
                <label className="q12-label" htmlFor="q12-no">
                  Soru no{p.numAuto && <span className="q12-auto">otomatik</span>}
                </label>
                <span className="q12-field">
                  <input
                    id="q12-no"
                    type="text"
                    inputMode="numeric"
                    className="q12-num"
                    value={p.questionNumber}
                    onChange={(e) => p.onQuestionNumber(e.target.value)}
                    placeholder="Bilmiyorsan boş bırak"
                  />
                </span>
              </div>
            </div>

            <div>
              <label className="q12-label" htmlFor="q12-stem">Soru kökü</label>
              <div className="q12-stem">
                <FastTextarea
                  id="q12-stem"
                  rows={4}
                  className="q12-ta"
                  value={p.stem}
                  onValue={p.onStem}
                  onKeyDown={submitOnCtrlEnter}
                  placeholder={p.stemPlaceholder}
                />
                <ComposerAssist active value={p.stem} onChange={p.onStem} textareaId="q12-stem" committeeId={p.committee?.id} />
              </div>
              {p.linkedQuestion && (
                <p className="q12-note is-ok" role="status">
                  <Link2 aria-hidden />
                  <span className="q12-grow">{p.linkedQuestion.questionNumber ? `Soru #${p.linkedQuestion.questionNumber} ile bağlandı` : 'Mevcut taslakla bağlandı'} · yazdıkların bu sorunun katkılarına eklenecek</span>
                  <button type="button" className="q12-btn is-icon is-sm is-ghost" onClick={p.onUnlink} aria-label="Bağlantıyı kaldır"><X aria-hidden /></button>
                </p>
              )}
            </div>

            {showSuggest && a && (
              <div className="q12-sug" role="note">
                <span className="q12-badge is-ai">YZ önerisi</span>
                <span className="q12-sug-b">
                  {crossSuggest && (
                    <span className="q12-sug-row">
                      <span className="q12-grow">Kurul uyuşmazlığı olabilir: {a.crossCommitteeWarning}</span>
                      <button type="button" className="q12-btn is-sm is-ghost" onClick={p.onApplyCommittee}>Bu kurula geç <ArrowRight aria-hidden /></button>
                    </span>
                  )}
                  {discSuggest && a.predictedDiscipline && (
                    <span className="q12-sug-row">
                      <span className="q12-grow">Ders “{a.predictedDiscipline.discipline}” olabilir · güven <span className="q12-num">%{a.predictedDiscipline.confidence}</span></span>
                      <button type="button" className="q12-btn is-sm is-ghost" onClick={() => p.onApplyDiscipline(a.predictedDiscipline!.discipline)}>Uygula</button>
                    </span>
                  )}
                  {topics.length > 0 && <span className="q12-sug-row q12-meta">İlişkili konular: {topics.map((t) => t.topic).join(', ')}</span>}
                  <span className="q12-meta">Öneri doğrulanmış bilgi değildir; havuzda <b className="q12-warn-t">İnceleniyor</b> olarak görünür.</span>
                </span>
              </div>
            )}

            <div className="q12-typerow">
              <span className="q12-label" id="q12-type-l">Soru tipi</span>
              <div className="q12-seg" role="radiogroup" aria-labelledby="q12-type-l">
                <button type="button" role="radio" aria-checked={p.qType !== 'onculu'} className={p.qType !== 'onculu' ? 'is-on' : ''} onClick={() => p.onQType('klasik')}>Klasik</button>
                <button type="button" role="radio" aria-checked={p.qType === 'onculu'} className={p.qType === 'onculu' ? 'is-on' : ''} onClick={() => { p.onQType('onculu'); if (!p.premises.some((x) => x.trim())) focusId('qh-prem-0'); }}>Öncüllü</button>
              </div>
              {p.looksOnculu && (
                <button type="button" className="q12-btn is-sm is-ghost" onClick={() => (p.stemPremiseCount >= 2 ? p.onExtractPremises() : (p.onQType('onculu'), focusId('qh-prem-0')))}>
                  <Wand2 aria-hidden />{p.stemPremiseCount >= 2 ? `Kökteki ${p.stemPremiseCount} öncülü ayır` : 'Öncüllü soruya benziyor'}
                </button>
              )}
            </div>

            {p.qType === 'onculu' && (
              <fieldset className="q12-fs">
                <legend className="q12-label">Öncüller</legend>
                <div className="q12-opts">
                  {p.premises.map((pr, i) => {
                    const r = ROMAN[i];
                    const verdict = p.truePremises ? (p.truePremises.has(r) ? 'doğru' : 'yanlış') : '';
                    return (
                      <div key={i} className="q12-opt">
                        <span className={`q12-k is-roman ${verdict === 'doğru' ? 'is-on' : ''}`} aria-hidden>{r}</span>
                        <span className="q12-field q12-grow">
                          <input
                            id={`qh-prem-${i}`}
                            value={pr}
                            onChange={(e) => p.onPremiseAt(i, e.target.value)}
                            onPaste={(e) => p.onPastePremises(i, e)}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') {
                                e.preventDefault();
                                if (i + 1 < p.premises.length) focusId(`qh-prem-${i + 1}`);
                                else if (pr.trim() && p.premises.length < p.premiseMax) p.onAddPremise(i);
                                else focusId('q12-opt-A');
                              } else if (e.key === 'Backspace' && !pr && p.premises.length > 2) {
                                e.preventDefault();
                                p.onRemovePremise(i);
                              }
                            }}
                            placeholder={i === 0 ? 'Öncül yaz · Enter ile sonraki' : `${r}. öncül`}
                            aria-label={`${r}. öncül`}
                          />
                          {verdict && <span className="q12-meta">{verdict}</span>}
                        </span>
                        <button type="button" className="q12-btn is-icon is-sm is-ghost" onClick={() => p.onRemovePremise(i)} aria-label={`${r}. öncülü sil`}><X aria-hidden /></button>
                      </div>
                    );
                  })}
                </div>
                {p.premises.length < p.premiseMax && (
                  <div className="q12-addrow">
                    <button type="button" className="q12-btn is-sm is-ghost" onClick={() => p.onAddPremise()}><Plus aria-hidden />{ROMAN[p.premises.length]}. öncülü ekle</button>
                  </div>
                )}
              </fieldset>
            )}

            <fieldset className="q12-fs">
              <legend className="q12-label">Şıklar</legend>
              {p.qType === 'onculu' && (
                <div className="q12-combos">
                  <button type="button" className="q12-pill is-soft" onClick={p.onFillStandard} disabled={p.filledPremiseCount < 2} title="A–E'yi öncül sayısına uygun sık kalıplarla doldur">
                    <Wand2 aria-hidden /><span>Kalıp şıkları doldur</span>
                  </button>
                  {p.comboChips.map((c) => (
                    <button key={c} type="button" className="q12-pill" onMouseDown={(e) => e.preventDefault()} onClick={() => pickCombo(c)}><span>{c}</span></button>
                  ))}
                </div>
              )}
              <div className="q12-opts">
                {visKeys.map((k, i) => (
                  <div key={k} className="q12-opt">
                    <span className={`q12-k ${p.answer === k ? 'is-on' : ''}`} aria-hidden>{k}</span>
                    <span className="q12-field q12-grow">
                      <input
                        id={`q12-opt-${k}`}
                        className="q12-opt-in"
                        data-k={k}
                        value={p.options[k]}
                        onChange={(e) => {
                          const v = e.target.value;
                          p.setOptions((prev) => ({ ...prev, [k]: v }));
                          if (v.trim() && i + 1 > p.optionCount) p.setOptionCount(i + 1);
                        }}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            e.preventDefault();
                            if (i + 1 < vis) focusId(`q12-opt-${KEYS[i + 1]}`);
                            else if (vis < 5 && p.options[k].trim()) addOption();
                          }
                        }}
                        enterKeyHint={i < 4 ? 'next' : 'done'}
                        placeholder={p.qType === 'onculu' ? 'örn. I ve III' : i === vis - 1 && i > 0 ? 'Hatırlamıyorsan boş bırak' : 'Şık yaz'}
                        aria-label={`${k} şıkkı${p.answer === k ? ' (doğru cevap)' : ''}`}
                      />
                    </span>
                    <button type="button" className="q12-btn is-icon is-sm is-ghost" onClick={() => removeOption(i)} aria-label={`${k} şıkkını kaldır`}><X aria-hidden /></button>
                  </div>
                ))}
              </div>
              <div className="q12-addrow">
                <button type="button" className="q12-btn is-sm is-ghost" onClick={addOption} disabled={vis >= 5}><Plus aria-hidden />Şık ekle</button>
                <span className="q12-meta">En çok 5 şık</span>
              </div>
            </fieldset>

            <div className="q12-ansrow">
              <span className="q12-label" id="q12-ans-l">Cevap</span>
              <div className="q12-seg" role="radiogroup" aria-labelledby="q12-ans-l">
                {visKeys.map((k) => (
                  <button key={k} type="button" role="radio" aria-checked={p.answer === k} className={p.answer === k ? 'is-on' : ''} onClick={() => p.onAnswer(k)}>{k}</button>
                ))}
                <button type="button" role="radio" aria-checked={!p.answer} className={!p.answer ? 'is-on' : ''} onClick={() => { p.onAnswer(undefined); p.onAnswerReason(''); }}>Bilmiyorum</button>
              </div>
              {p.answer && (
                <span className="q12-field q12-why">
                  <input
                    value={p.answerReason}
                    onChange={(e) => p.onAnswerReason(e.target.value)}
                    placeholder={`Neden ${p.answer}? (isteğe bağlı)`}
                    aria-label="Cevap gerekçesi (isteğe bağlı)"
                  />
                </span>
              )}
            </div>

            <div>
              <label className="q12-label" htmlFor="q12-clue">İpucu / hatırladığım</label>
              <FastTextarea
                id="q12-clue"
                rows={2}
                className="q12-ta is-sm"
                value={p.clue}
                onValue={p.onClue}
                onKeyDown={submitOnCtrlEnter}
                placeholder={p.cluePlaceholder}
              />
            </div>

            {p.formError && <p role="alert" className="q12-note is-bad"><AlertCircle aria-hidden /><span>{p.formError}</span></p>}
            {p.successMessage && <p role="status" className="q12-note is-ok"><CheckCircle2 aria-hidden /><span>Teşekkürler! {p.successMessage}</span></p>}
            {p.intakeId && <IntakeEcho key={p.intakeId} intakeId={p.intakeId} onClose={p.onCloseIntake} />}
          </div>

          <aside className="q12-live-col" aria-label="Benzer sorular ve kaynaklar">
            {(p.matches.length > 0 || (p.isSearching && typed && nothing)) && (
              <section className="q12-sec" aria-labelledby="q12-pm-h" aria-busy={p.isSearching}>
                <div className="q12-sech">
                  <h2 className="q12-h3" id="q12-pm-h">Havuzda benzer taslaklar</h2>
                  <span className="q12-meta q12-grow">tekrar riski</span>
                  {p.matches.length > 1 && (
                    <button type="button" className="q12-btn is-sm is-ghost" onClick={p.selectedMatchIds.size === p.matches.length ? p.onClearMatchSelection : p.onSelectAllMatches}>
                      {p.selectedMatchIds.size === p.matches.length ? 'Seçimi bırak' : 'Tümünü seç'}
                    </button>
                  )}
                </div>
                {p.matches.length === 0 && (
                  <div className="q12-hits-skel" aria-hidden>{[0, 1].map((i) => <span key={i} className="q12-skel" />)}</div>
                )}
                {p.matches.map((m, idx) => {
                  const mq = m.question;
                  const sel = p.selectedMatchIds.has(mq.id);
                  const score = m.compatibility.score;
                  return (
                    <div key={mq.id} className={`q12-hit ${sel ? 'is-on' : ''}`}>
                      <span className="q12-sim q12-num" title="Eşleşme olasılığı">%{score}</span>
                      <span className="q12-grow q12-hit-b">
                        <span className="q12-clamp2 q12-hit-t"><Colored text={p.stemOf(mq)} colors={p.sharedColors} /></span>
                        <span className="q12-hit-m">
                          <span className="q12-meta">{[mq.questionNumber ? `Soru ${mq.questionNumber}` : 'Numarasız', mq.discipline, idx === 0 ? 'en yakın' : ''].filter(Boolean).join(' · ')}</span>
                          {m.isCrossCommittee && <span className="q12-badge is-ai">Farklı kurul</span>}
                          {m.contextHashtag && score >= p.highlightMin && <ContextBadge hashtag={m.contextHashtag} colorIndex={idx} />}
                        </span>
                        <span className="q12-hit-a">
                          <button type="button" className="q12-btn is-sm" onClick={() => p.onLink(mq)}>
                            <Link2 aria-hidden />{mq.questionNumber ? `Soru ${mq.questionNumber} ile bağla` : 'Bu taslakla bağla'}
                          </button>
                          <button type="button" className="q12-btn is-sm is-ghost" onClick={() => p.onReject(mq.id)} title="Bu öneri benim hatırladığım soru değil (öneriler bundan öğrenir)">Farklı soru</button>
                          <button type="button" className="q12-btn is-icon is-sm is-ghost" onClick={() => p.onToggleMatch(mq.id)} aria-pressed={sel} aria-label={`Soru ${mq.questionNumber || 'taslak'} birleştirmek için seç`}>
                            {sel ? <CheckSquare aria-hidden /> : <Square aria-hidden />}
                          </button>
                          {p.isAdmin && (
                            <button type="button" className="q12-btn is-sm is-ghost q12-ai-t" onClick={() => p.onOptimize(mq)} title="Taslağı ders slaytları ve YZ ile tam soruya dönüştür (sonuç İnceleniyor olarak kalır)">
                              <Wand2 aria-hidden />YZ ile dönüştür
                            </button>
                          )}
                        </span>
                      </span>
                    </div>
                  );
                })}
                {p.matches.length > 0 && (
                  <WordLegend texts={[p.queryText || p.stem, ...p.matches.map((m) => p.stemOf(m.question))]} colors={p.sharedColors} />
                )}
                {p.selectedMatchIds.size > 0 && (
                  <div className="q12-merge">
                    <span className="q12-grow q12-meta"><span className="q12-num">{p.selectedMatchIds.size}</span> soru seçildi</span>
                    <button type="button" className="q12-btn is-sm is-ghost" onClick={p.onClearMatchSelection}>İptal</button>
                    <button type="button" className="q12-btn is-sm is-pri" disabled={p.isMerging} onClick={p.onMerge}>
                      <Layers aria-hidden />
                      {p.isMerging ? 'Birleştiriliyor…' : p.selectedMatchIds.size === 1 ? 'Bu soruyla birleştir' : `Birleştir (${p.selectedMatchIds.size})`}
                    </button>
                  </div>
                )}
              </section>
            )}

            <section className="q12-sec" aria-labelledby="q12-past-h" aria-live="polite">
              <div className="q12-sech">
                <h2 className="q12-h3" id="q12-past-h">Benzer çıkmış sorular</h2>
                <span className="q12-meta q12-grow">yazdıkça güncellenir</span>
              </div>
              {p.similar.length === 0 && (
                p.isSearching && typed
                  ? <div className="q12-hits-skel" aria-hidden>{[0, 1, 2].map((i) => <span key={i} className="q12-skel" />)}</div>
                  : <p className="q12-meta q12-hint">{typed ? 'Bu metne yakın çıkmış soru bulunmadı.' : 'Kökü yazdıkça benzer çıkmış sorular burada belirir; aynı soruyu ikinci kez eklemeyi önler.'}</p>
              )}
              {p.similar.map((s) => (
                <div key={s.id} className="q12-hit">
                  <span className="q12-sim q12-num" title="Sınav yılı">{s.examYear ? s.examYear.slice(0, 4) : '—'}</span>
                  <span className="q12-grow q12-hit-b">
                    <span className="q12-clamp2 q12-hit-t">{s.stem}</span>
                    <span className="q12-meta">{['Çıkmış', s.discipline, s.claimedAnswer ? `Cevap: ${s.claimedAnswer}` : ''].filter(Boolean).join(' · ')}</span>
                    {s.options && s.options.length > 0 && (
                      <details className="q12-pastopts">
                        <summary>Şıkları göster</summary>
                        <ol>
                          {s.options.map((o) => (
                            <li key={o.key} className={o.key === s.claimedAnswer ? 'is-ok' : ''}><b>{o.key})</b> {o.text}</li>
                          ))}
                        </ol>
                      </details>
                    )}
                    <span className="q12-hit-a">
                      <button type="button" className="q12-btn is-sm" onClick={() => p.onTransfer(s)} title="Sorunun kökünü, dersini ve şıklarını forma aktar">
                        <FileText aria-hidden />{s.options && s.options.length ? 'Kök + şıkları aktar' : 'Soruyu aktar'}
                      </button>
                      <button type="button" className="q12-btn is-sm is-ghost" onClick={() => p.onCopyStem(s.stem)} title="Yalnızca soru kökünü forma yaz ve panoya kopyala">
                        <Copy aria-hidden />Yalnızca kökü al
                      </button>
                    </span>
                  </span>
                </div>
              ))}
            </section>

            <section className="q12-sec" aria-labelledby="q12-src-h">
              <div className="q12-sech">
                <h2 className="q12-h3" id="q12-src-h">Kaynak eşleşmeleri</h2>
                <span className="q12-meta q12-grow">ders slaytları</span>
              </div>
              {p.sources.length === 0 ? (
                <p className="q12-meta q12-hint">{typed ? 'Henüz eşleşen ders kaynağı yok.' : 'Yazdığın parçaya uyan ders slaytı sayfaları burada görünür.'}</p>
              ) : (
                p.sources.map((s) => (
                  <div key={`${s.documentId}:${s.pageNumber ?? ''}`} className="q12-hit">
                    <FileText aria-hidden className="q12-hit-ico" />
                    <span className="q12-grow q12-hit-b">
                      <span className="q12-clamp1 q12-hit-t is-strong">{s.title}</span>
                      <span className="q12-meta q12-clamp2">{s.snippet}</span>
                    </span>
                    {s.pageNumber != null && <span className="q12-badge">s. <span className="q12-num">{s.pageNumber}</span></span>}
                  </div>
                ))
              )}
            </section>
          </aside>
        </div>

        <div className="q12-foot">
          <span className="q12-meta q12-grow q12-foot-t">
            Kök ve şıklarıyla gönderilen soru havuzda <b>İnceleniyor</b>, eksik kalan <b className="is-plain">Parça</b> olarak açılır; inceleme sonrası doğrulanır.
            <span className="q12-kbdhint"> · Ctrl + Enter ile gönder</span>
          </span>
          <button type="button" className="q12-btn is-ghost" onClick={p.onSaveDraft} disabled={p.formEmpty}>Taslak olarak kaydet</button>
          <button type="submit" className="q12-btn is-pri" disabled={p.isSubmitting || p.isLocked}>
            {p.isSubmitting ? 'Gönderiliyor…' : 'Havuza gönder'}
          </button>
        </div>
      </form>
    </div>
  );
};
