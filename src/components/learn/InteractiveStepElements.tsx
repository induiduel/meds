import React, { useState } from 'react';
import {
  HelpCircle,
  CheckCircle2,
  XCircle,
  ArrowRight,
  Eye,
  EyeOff,
  Sparkles,
  GitBranch,
  Layers,
  Activity,
  AlertTriangle,
  RotateCcw,
  Sliders,
  ChevronRight,
  Network
} from 'lucide-react';

export type InteractiveElementType =
  | 'cloze_masking'
  | 'active_recall'
  | 'before_after_slider'
  | 'hotspots'
  | 'branching_logic'
  | 'micro_quiz'
  | 'node_graph'
  | 'causal_chain'
  | 'interactive_table';

export interface InteractiveElementData {
  type: InteractiveElementType;
  // Cloze Masking
  sentence?: string;
  maskedTerm?: string;
  hint?: string;
  explanation?: string;
  // Active Recall
  question?: string;
  answer?: string;
  // Before / After Slider
  leftTitle?: string;
  rightTitle?: string;
  leftPoints?: string[];
  rightPoints?: string[];
  // Hotspots
  title?: string;
  items?: Array<{ label: string; detail: string; x?: number; y?: number }>;
  // Branching Logic
  scenario?: string;
  options?: Array<{ key?: string; text: string; isCorrect: boolean; feedback: string }>;
  // Micro Quiz
  microQuizOptions?: Array<{ key: string; text: string; isCorrect: boolean; explanation: string }>;
  // Node Graph
  centerNode?: string;
  nodes?: Array<{ id: string; label: string; role: string }>;
  // Causal Chain
  chainTitle?: string;
  steps?: string[];
  // Interactive Masked Table (Hafıza / Ezber Tablosu)
  tableTitle?: string;
  tableHeaders?: string[];
  tableRows?: Array<{
    cells: Array<{
      text: string;
      isMasked?: boolean;
      hint?: string;
    }>;
  }>;
}

export const InteractiveStepRenderer: React.FC<{
  data?: InteractiveElementData | InteractiveElementData[] | null;
}> = ({ data }) => {
  if (!data) return null;

  const elements = Array.isArray(data) ? data.filter(Boolean) : [data];
  if (elements.length === 0) return null;

  return (
    <div className="mt-4 pt-4 border-t border-line/70 flex flex-col gap-4">
      {elements.map((el, idx) => {
        if (!el || !el.type) return null;
        const t = (el.type || '').toLowerCase();
        const isCloze = t === 'cloze_masking' || t === 'cloze' || t === 'masking';
        const isActiveRecall = t === 'active_recall' || t === 'recall' || t === 'active';
        const isBeforeAfter = t === 'before_after_slider' || t === 'before_after' || t === 'slider';
        const isHotspots = t === 'hotspots' || t === 'hotspot';
        const isBranching = t === 'branching_logic' || t === 'branching' || t === 'decision';
        const isMicroQuiz = t === 'micro_quiz' || t === 'quiz' || t === 'mini_quiz';
        const isNodeGraph = t === 'node_graph' || t === 'graph' || t === 'nodes';
        const isCausalChain = t === 'causal_chain' || t === 'chain' || t === 'causal';
        const isInteractiveTable = t === 'interactive_table' || t === 'masked_table' || t === 'table_masked' || t === 'table';

        return (
          <div key={idx} className="relative">
            {elements.length > 1 && (
              <div className="text-[11px] font-bold uppercase tracking-wider text-accent mb-1.5 flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-accent" />
                <span>İnteraktif Alıştırma {idx + 1} / {elements.length}</span>
              </div>
            )}
            {isCloze && <ClozeMaskingElement data={el} />}
            {isActiveRecall && <ActiveRecallElement data={el} />}
            {isBeforeAfter && <BeforeAfterElement data={el} />}
            {isHotspots && <HotspotsElement data={el} />}
            {isBranching && <BranchingLogicElement data={el} />}
            {isMicroQuiz && <MicroQuizElement data={el} />}
            {isNodeGraph && <NodeGraphElement data={el} />}
            {isCausalChain && <CausalChainElement data={el} />}
            {isInteractiveTable && <InteractiveTableElement data={el} />}
          </div>
        );
      })}
    </div>
  );
};

// 1. Örtülü Hatırlama / Kilit Terim Maskesi (Yalnızca Kritik Klinik Kavramlar)
const ClozeMaskingElement: React.FC<{ data: InteractiveElementData }> = ({ data }) => {
  const [revealed, setRevealed] = useState(false);
  
  // Parantezleri temizleme ve terimi akıllı ayrıştırma
  const rawSentence = data.sentence || '';
  const term = data.maskedTerm || '';

  // Eğer cümlede [Terim] varsa parantez içindekini tespit et
  const bracketMatch = rawSentence.match(/\[(.*?)\]/);
  const activeTerm = term || (bracketMatch ? bracketMatch[1] : '');

  // Cümleyi sol ve sağ parçalara ayırırken [ ve ] işaretlerini tamamen temizle
  let prefix = '';
  let suffix = '';

  if (bracketMatch && bracketMatch[0]) {
    const splitArr = rawSentence.split(bracketMatch[0]);
    prefix = splitArr[0];
    suffix = splitArr.slice(1).join(bracketMatch[0]);
  } else if (activeTerm && rawSentence.includes(activeTerm)) {
    const splitArr = rawSentence.split(activeTerm);
    prefix = splitArr[0].replace(/\[\s*$/, '');
    suffix = splitArr.slice(1).join(activeTerm).replace(/^\s*\]/, '');
  } else {
    prefix = rawSentence;
    suffix = '';
  }

  // Kalan olası tekil köşeli parantez artıklarını da temizle
  prefix = prefix.replace(/\[/g, '').trimEnd() + ' ';
  suffix = ' ' + suffix.replace(/\]/g, '').trimStart();

  return (
    <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-br from-violet-50/90 via-white to-purple-50/70 dark:from-violet-950/30 dark:via-zinc-900 dark:to-purple-950/20 border-2 border-violet-200/90 dark:border-violet-800/50 shadow-sm transition-all duration-300">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3 pb-2 border-b border-violet-100 dark:border-violet-900/40">
        <span className="text-[12px] font-bold uppercase tracking-wider text-violet-800 dark:text-violet-300 flex items-center gap-1.5 bg-violet-100/80 dark:bg-violet-900/40 px-2.5 py-1 rounded-lg">
          <Eye className="w-3.5 h-3.5 text-violet-600" />
          Kritik Tıbbi Terim Maskesi
        </span>
        {data.hint && !revealed && (
          <span className="text-[11.5px] font-medium text-violet-700/80 dark:text-violet-300/80 bg-white/80 dark:bg-zinc-800 px-2 py-0.5 rounded-md border border-violet-200/60">
            İpucu: {data.hint}
          </span>
        )}
      </div>

      <p className="text-[13.5px] sm:text-[14.5px] font-medium leading-[1.8] text-ink m-0">
        {prefix}
        <button
          type="button"
          onClick={() => setRevealed(!revealed)}
          className={`inline-flex items-center gap-1.5 px-3 py-1 mx-1 rounded-lg text-[13.5px] font-bold cursor-pointer transition-all duration-300 select-none shadow-xs active:scale-95 ${
            revealed
              ? 'bg-violet-600 text-white shadow-md ring-2 ring-violet-300 dark:ring-violet-700 animate-fadeIn'
              : 'bg-violet-100 text-violet-900 hover:bg-violet-200 border border-violet-300/80 dark:bg-violet-900/60 dark:text-violet-100'
          }`}
          title={revealed ? 'Gizle' : 'Kilit tıbbi terimi açmak için tıklayın'}
        >
          {revealed ? (
            <>
              <span>{activeTerm}</span>
              <EyeOff className="w-3.5 h-3.5 opacity-80" />
            </>
          ) : (
            <>
              <span className="tracking-widest">??????</span>
              <span className="text-[11px] opacity-75">(Açmak İçin Dokun)</span>
            </>
          )}
        </button>
        {suffix}
      </p>

      {revealed && data.explanation && (
        <div className="mt-3.5 p-3 rounded-xl bg-violet-100/60 dark:bg-violet-900/30 border border-violet-200 dark:border-violet-800/60 text-[12.5px] sm:text-[13px] text-violet-950 dark:text-violet-200 flex items-start gap-2.5 animate-fadeIn">
          <Sparkles className="w-4 h-4 text-violet-600 shrink-0 mt-0.5" />
          <div className="leading-relaxed">
            <strong className="block font-bold text-[12.5px] text-violet-900 dark:text-violet-100 mb-0.5">Sınav Hatırlatması:</strong>
            {data.explanation}
          </div>
        </div>
      )}
    </div>
  );
};

// 2. Aktif Hatırlama (Active Recall)
const ActiveRecallElement: React.FC<{ data: InteractiveElementData }> = ({ data }) => {
  const [flipped, setFlipped] = useState(false);

  return (
    <div className="p-3.5 sm:p-4 rounded-xl bg-amber-50/70 dark:bg-amber-950/20 border border-amber-200/80 dark:border-amber-800/40">
      <div className="flex items-center justify-between mb-2">
        <span className="text-[11.5px] font-bold uppercase tracking-wider text-amber-800 dark:text-amber-300 flex items-center gap-1.5">
          <Layers className="w-3.5 h-3.5" />
          Aktif Hatırlama Kartı
        </span>
        <button
          type="button"
          onClick={() => setFlipped(!flipped)}
          className="text-[11.5px] font-medium text-amber-700 hover:text-amber-900 dark:text-amber-400 underline cursor-pointer flex items-center gap-1"
        >
          <RotateCcw className="w-3 h-3" />
          {flipped ? 'Soruyu Gör' : 'Cevabı Çevir'}
        </button>
      </div>

      <div
        onClick={() => setFlipped(!flipped)}
        className="cursor-pointer min-h-[56px] flex flex-col justify-center p-3 rounded-lg bg-white dark:bg-zinc-900 border border-amber-200/60 shadow-2xs transition-all hover:border-amber-300"
      >
        {!flipped ? (
          <div>
            <p className="text-[13.5px] font-semibold text-ink m-0 flex items-start gap-2">
              <span className="text-amber-600 font-bold shrink-0">S:</span>
              <span>{data.question}</span>
            </p>
            {data.hint && (
              <p className="text-[11.5px] text-ink-3 m-0 mt-1 pl-5 italic">İpucu: {data.hint}</p>
            )}
          </div>
        ) : (
          <div className="animate-fadeIn">
            <p className="text-[13px] font-medium text-emerald-800 dark:text-emerald-300 m-0 flex items-start gap-2 leading-relaxed">
              <span className="text-emerald-600 font-bold shrink-0">Cevap:</span>
              <span>{data.answer}</span>
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

// 3. Karşılaştırma Kaydırıcısı / Ayırıcı Tanı Tablosu (Fonksiyonel & Yaratıcı Tasarım)
const BeforeAfterElement: React.FC<{ data: InteractiveElementData }> = ({ data }) => {
  const [focusedIdx, setFocusedIdx] = useState<number | null>(null);
  const title = (data as any).title || 'Karşılaştırmalı Ayırıcı Tanı Matrisi';
  const leftPoints = Array.isArray(data.leftPoints) ? data.leftPoints : (typeof data.leftPoints === 'string' ? [data.leftPoints] : []);
  const rightPoints = Array.isArray(data.rightPoints) ? data.rightPoints : (typeof data.rightPoints === 'string' ? [data.rightPoints] : []);
  const maxRows = Math.max(leftPoints.length, rightPoints.length);

  return (
    <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-br from-slate-50 via-white to-zinc-50 dark:from-zinc-900 dark:via-zinc-900 dark:to-zinc-955 border-2 border-line shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3.5 pb-2.5 border-b border-line">
        <div className="flex items-center gap-2">
          <span className="w-7 h-7 rounded-xl bg-indigo-600 text-white flex items-center justify-center shrink-0 shadow-2xs">
            <Sliders className="w-3.5 h-3.5" />
          </span>
          <div>
            <h4 className="m-0 text-[13.5px] sm:text-[14.5px] font-bold text-ink flex items-center gap-2">
              <span>{title}</span>
            </h4>
            <p className="m-0 text-[11px] text-ink-3">
              Maddelere tıklayarak karşılıklı klinik ve patofizyolojik farkları vurgulayabilirsiniz
            </p>
          </div>
        </div>
      </div>

      {/* İki Sütunlu Grid Başlıkları */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-2">
        <div className="p-2.5 rounded-xl bg-indigo-50/80 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800/60 text-center">
          <span className="text-[11px] uppercase tracking-wider font-bold text-indigo-700 dark:text-indigo-300 block mb-0.5">Konsept A</span>
          <h5 className="m-0 text-[14px] font-extrabold text-indigo-950 dark:text-indigo-100">{data.leftTitle}</h5>
        </div>
        <div className="p-2.5 rounded-xl bg-rose-50/80 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800/60 text-center">
          <span className="text-[11px] uppercase tracking-wider font-bold text-rose-700 dark:text-rose-300 block mb-0.5">Konsept B</span>
          <h5 className="m-0 text-[14px] font-extrabold text-rose-950 dark:text-rose-100">{data.rightTitle}</h5>
        </div>
      </div>

      {/* Karşılıklı Eşleşen Madde Satırları */}
      <div className="space-y-2 mt-3">
        {Array.from({ length: maxRows }).map((_, rIdx) => {
          const lText = leftPoints[rIdx] || '';
          const rText = rightPoints[rIdx] || '';
          const isFocused = focusedIdx === rIdx;

          return (
            <div
              key={rIdx}
              onClick={() => setFocusedIdx(isFocused ? null : rIdx)}
              className={`grid grid-cols-1 sm:grid-cols-2 gap-2.5 p-2.5 rounded-xl transition-all duration-200 cursor-pointer border ${
                isFocused
                  ? 'bg-amber-50/80 dark:bg-amber-950/30 border-amber-300 dark:border-amber-700 shadow-xs ring-2 ring-amber-200'
                  : 'bg-canvas hover:bg-white dark:hover:bg-zinc-800/70 border-line/60'
              }`}
            >
              {/* Sol Madde */}
              <div className="flex items-start gap-2 text-[12.5px] sm:text-[13px] leading-relaxed text-ink-2">
                <span className="w-5 h-5 rounded-full bg-indigo-100 dark:bg-indigo-900/60 text-indigo-700 dark:text-indigo-300 text-[10.5px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                  {rIdx + 1}
                </span>
                <span className="flex-1">{lText}</span>
              </div>

              {/* Sağ Madde */}
              <div className="flex items-start gap-2 text-[12.5px] sm:text-[13px] leading-relaxed text-ink-2">
                <span className="w-5 h-5 rounded-full bg-rose-100 dark:bg-rose-900/60 text-rose-700 dark:text-rose-300 text-[10.5px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                  {rIdx + 1}
                </span>
                <span className="flex-1">{rText}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// 4. Tıklanabilir Odak Noktaları (Hotspots)
const HotspotsElement: React.FC<{ data: InteractiveElementData }> = ({ data }) => {
  const [selectedIdx, setSelectedIdx] = useState<number | null>(0);
  const items = data.items || [];

  return (
    <div className="p-3.5 sm:p-4 rounded-xl bg-teal-50/60 dark:bg-teal-950/20 border border-teal-200/70">
      <div className="flex items-center gap-2 mb-2 text-teal-800 dark:text-teal-300 font-semibold text-[12px] uppercase tracking-wider">
        <Activity className="w-3.5 h-3.5" />
        <span>{data.title || 'Kritik Odak Noktaları'}</span>
      </div>

      <div className="flex flex-wrap gap-1.5 mb-2.5">
        {items.map((it, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => setSelectedIdx(idx)}
            className={`px-2.5 py-1 rounded-lg text-[12px] font-medium cursor-pointer transition-all flex items-center gap-1.5 ${
              selectedIdx === idx
                ? 'bg-teal-600 text-white shadow-2xs ring-2 ring-teal-300'
                : 'bg-white dark:bg-zinc-800 text-ink-2 border border-teal-200 hover:bg-teal-50'
            }`}
          >
            <span className="w-4 h-4 rounded-full bg-teal-100 dark:bg-teal-900 text-teal-800 dark:text-teal-200 flex items-center justify-center text-[10px] font-bold">
              {idx + 1}
            </span>
            <span>{it.label}</span>
          </button>
        ))}
      </div>

      {selectedIdx !== null && items[selectedIdx] && (
        <div className="p-2.5 rounded-lg bg-white dark:bg-zinc-900 border border-teal-200/80 text-[12.5px] text-ink-2 leading-relaxed animate-fadeIn">
          <strong className="text-teal-900 dark:text-teal-300 block mb-0.5">
            {items[selectedIdx].label}:
          </strong>
          {items[selectedIdx].detail}
        </div>
      )}
    </div>
  );
};

// 5. Dallanan Karar Senaryoları (Branching Logic)
const BranchingLogicElement: React.FC<{ data: InteractiveElementData }> = ({ data }) => {
  const [selectedKey, setSelectedKey] = useState<number | null>(null);
  const options = data.options || [];

  return (
    <div className="p-3.5 sm:p-4 rounded-xl bg-sky-50/70 dark:bg-sky-950/20 border border-sky-200/80 dark:border-sky-800/40">
      <div className="flex items-center gap-2 mb-2 text-sky-800 dark:text-sky-300 font-semibold text-[12px] uppercase tracking-wider">
        <GitBranch className="w-3.5 h-3.5" />
        <span>Klinik Karar Senaryosu</span>
      </div>

      {data.scenario && (
        <p className="text-[13px] sm:text-[13.5px] font-medium text-ink mb-3 leading-relaxed">
          {data.scenario}
        </p>
      )}

      <div className="space-y-2">
        {options.map((opt, idx) => {
          const isSelected = selectedKey === idx;
          return (
            <div key={idx} className="flex flex-col">
              <button
                type="button"
                onClick={() => setSelectedKey(idx)}
                className={`text-left p-2.5 rounded-lg text-[12.5px] font-medium transition-all cursor-pointer border flex items-start gap-2 ${
                  isSelected
                    ? opt.isCorrect
                      ? 'bg-emerald-50 border-emerald-300 text-emerald-950 dark:bg-emerald-950/30 dark:border-emerald-700'
                      : 'bg-rose-50 border-rose-300 text-rose-950 dark:bg-rose-950/30 dark:border-rose-700'
                    : 'bg-white dark:bg-zinc-800 border-sky-200/60 hover:border-sky-300 text-ink-2'
                }`}
              >
                <ChevronRight className="w-3.5 h-3.5 text-sky-600 mt-0.5 shrink-0" />
                <span className="flex-1">{opt.text}</span>
              </button>

              {isSelected && (
                <div
                  className={`mt-1.5 p-2 rounded-lg text-[12px] leading-relaxed flex items-start gap-1.5 animate-fadeIn ${
                    opt.isCorrect
                      ? 'bg-emerald-100/70 text-emerald-900 border border-emerald-300'
                      : 'bg-rose-100/70 text-rose-900 border border-rose-300'
                  }`}
                >
                  {opt.isCorrect ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700 shrink-0 mt-0.5" />
                  ) : (
                    <AlertTriangle className="w-3.5 h-3.5 text-rose-700 shrink-0 mt-0.5" />
                  )}
                  <span>{opt.feedback}</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// 6. Anında Düzeltici Geri Bildirimli Mikro-Quiz
const MicroQuizElement: React.FC<{ data: InteractiveElementData }> = ({ data }) => {
  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  const options = data.microQuizOptions || [];
  const questionText = data.question || data.sentence || (data as any).stem || '';

  return (
    <div className="p-4 sm:p-5 rounded-2xl bg-indigo-50/80 dark:bg-indigo-950/30 border-2 border-indigo-200/90 dark:border-indigo-800/60 shadow-sm transition-all">
      <div className="flex items-center gap-2 mb-2.5 pb-1.5 border-b border-indigo-100 dark:border-indigo-900/40 text-indigo-900 dark:text-indigo-200 font-bold text-[12px] uppercase tracking-wider">
        <HelpCircle className="w-4 h-4 text-indigo-600" />
        <span>Kavram Pekiştirme Mikro-Quiz</span>
      </div>

      {questionText && (
        <p className="text-[13.5px] sm:text-[14.5px] font-bold text-ink mb-3 leading-relaxed">
          {questionText}
        </p>
      )}

      <div className="space-y-2">
        {options.map((opt) => {
          const isSelected = selectedKey === opt.key;
          return (
            <div key={opt.key} className="flex flex-col">
              <button
                type="button"
                onClick={() => setSelectedKey(opt.key)}
                className={`text-left p-2.5 rounded-lg text-[12.5px] font-medium transition-all cursor-pointer border flex items-start gap-2.5 ${
                  isSelected
                    ? opt.isCorrect
                      ? 'bg-emerald-50 border-emerald-400 text-emerald-950 font-bold'
                      : 'bg-rose-50 border-rose-400 text-rose-950 font-bold'
                    : 'bg-white dark:bg-zinc-800 border-indigo-200/70 hover:border-indigo-300 text-ink-2'
                }`}
              >
                <span className="w-5 h-5 rounded-full bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 font-bold text-[11px] flex items-center justify-center shrink-0">
                  {opt.key}
                </span>
                <span className="flex-1">{opt.text}</span>
              </button>

              {isSelected && (
                <div
                  className={`mt-1.5 p-2 rounded-lg text-[12px] leading-relaxed flex items-start gap-1.5 animate-fadeIn ${
                    opt.isCorrect
                      ? 'bg-emerald-100/70 text-emerald-900 border border-emerald-300'
                      : 'bg-rose-100/70 text-rose-900 border border-rose-300'
                  }`}
                >
                  {opt.isCorrect ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                  ) : (
                    <XCircle className="w-4 h-4 text-rose-700 shrink-0 mt-0.5" />
                  )}
                  <div>
                    <strong>{opt.isCorrect ? 'Doğru Gerekçe:' : 'Çürütme & Açıklama:'}</strong>{' '}
                    {opt.explanation}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// 7. Genişleyebilir Kavram Düğümleri (Node Graph)
const NodeGraphElement: React.FC<{ data: InteractiveElementData }> = ({ data }) => {
  const [activeNode, setActiveNode] = useState<string | null>(null);
  const nodes = data.nodes || [];

  return (
    <div className="p-3.5 sm:p-4 rounded-xl bg-purple-50/60 dark:bg-purple-950/20 border border-purple-200/70">
      <div className="flex items-center gap-2 mb-2 text-purple-800 dark:text-purple-300 font-semibold text-[12px] uppercase tracking-wider">
        <Network className="w-3.5 h-3.5" />
        <span>Kavram Düğümleri & İlişkiler</span>
      </div>

      <div className="text-center my-2">
        <span className="inline-block px-3 py-1 rounded-full bg-purple-700 text-white text-[12.5px] font-bold shadow-2xs">
          {data.centerNode}
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-3">
        {nodes.map((node) => {
          const isSelected = activeNode === node.id;
          return (
            <button
              key={node.id}
              type="button"
              onClick={() => setActiveNode(isSelected ? null : node.id)}
              className={`p-2.5 rounded-lg border text-left cursor-pointer transition-all ${
                isSelected
                  ? 'bg-purple-100 dark:bg-purple-900/40 border-purple-400 ring-2 ring-purple-300'
                  : 'bg-white dark:bg-zinc-800 border-purple-200 hover:border-purple-300'
              }`}
            >
              <div className="text-[12.5px] font-bold text-ink">{node.label}</div>
              <div className="text-[11px] text-purple-700 dark:text-purple-300 mt-0.5">{node.role}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
};

// 8. Patolojik Neden-Sonuç Zinciri (Causal Chain)
const CausalChainElement: React.FC<{ data: InteractiveElementData }> = ({ data }) => {
  const steps = data.steps || [];

  return (
    <div className="p-3.5 sm:p-4 rounded-xl bg-emerald-50/60 dark:bg-emerald-950/20 border border-emerald-200/70">
      <div className="flex items-center gap-2 mb-2.5 text-emerald-800 dark:text-emerald-300 font-semibold text-[12px] uppercase tracking-wider">
        <Activity className="w-3.5 h-3.5" />
        <span>{data.chainTitle || 'Patolojik Neden-Sonuç Zinciri'}</span>
      </div>

      <div className="space-y-1.5">
        {steps.map((st, i) => (
          <div key={i} className="flex items-start gap-2">
            <span className="w-5 h-5 rounded-full bg-emerald-600 text-white font-bold text-[11px] flex items-center justify-center shrink-0 mt-0.5 shadow-2xs">
              {i + 1}
            </span>
            <div className="flex-1 p-2 rounded-lg bg-white dark:bg-zinc-800 border border-emerald-200/60 text-[12.5px] text-ink font-medium leading-snug">
              {st}
            </div>
            {i < steps.length - 1 && (
              <span className="hidden">➔</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

// 9. İnteraktif Hücre Maskeli Ezber Tablosu (Interactive Masked Memorization Table)
const InteractiveTableElement: React.FC<{ data: InteractiveElementData }> = ({ data }) => {
  const d = data as any;
  const headers: string[] = (d.tableHeaders && d.tableHeaders.length ? d.tableHeaders : d.headers) || (d.table && d.table.headers) || [];
  const rawRows: any[] = (d.tableRows && d.tableRows.length ? d.tableRows : d.rows) || (d.table && d.table.rows) || [];
  const rows: { cells: { text?: string; isMasked?: boolean; [k: string]: any }[] }[] = rawRows.map((r: any) => {
    if (r && Array.isArray(r.cells)) return r;
    if (Array.isArray(r)) {
      return {
        cells: r.map((c: any) => (typeof c === 'object' && c ? c : { text: String(c ?? ''), isMasked: false })),
      };
    }
    return { cells: [] };
  });

  // Track revealed cells by key: `rIdx-cIdx`
  const [revealedCells, setRevealedCells] = useState<Record<string, boolean>>({});
  const [allRevealed, setAllRevealed] = useState(false);

  const toggleCell = (key: string) => {
    setRevealedCells((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const toggleAll = () => {
    if (allRevealed) {
      setRevealedCells({});
      setAllRevealed(false);
    } else {
      const all: Record<string, boolean> = {};
      rows.forEach((r: any, rIdx: number) => {
        (r.cells || []).forEach((c: any, cIdx: number) => {
          if (c.isMasked) all[`${rIdx}-${cIdx}`] = true;
        });
      });
      setRevealedCells(all);
      setAllRevealed(true);
    }
  };

  return (
    <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-br from-amber-50/70 via-white to-orange-50/50 dark:from-zinc-900 dark:via-zinc-850 dark:to-zinc-900 border-2 border-amber-300/80 dark:border-amber-700/60 shadow-sm transition-all">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3 pb-2 border-b border-amber-200/70 dark:border-amber-800/50">
        <div className="flex items-center gap-2 text-amber-900 dark:text-amber-200 font-bold text-[12.5px] uppercase tracking-wider">
          <Layers className="w-4 h-4 text-amber-600" />
          <span>{data.tableTitle || 'Hafıza & Ezber Tablosu (Maskeli Pekiştirme)'}</span>
        </div>
        <button
          type="button"
          onClick={toggleAll}
          className="text-[11.5px] font-semibold text-amber-800 dark:text-amber-300 bg-amber-100 hover:bg-amber-200 dark:bg-amber-900/60 dark:hover:bg-amber-800/80 px-2.5 py-1 rounded-lg border border-amber-300/70 cursor-pointer transition-colors shadow-2xs"
        >
          {allRevealed ? 'Hücreleri Maskele' : 'Tüm Maskeleri Aç'}
        </button>
      </div>

      <div className="overflow-x-auto rounded-xl border border-amber-200/60 dark:border-zinc-700">
        <table className="w-full text-left text-[12.5px] sm:text-[13px] border-collapse bg-white dark:bg-zinc-900">
          {headers.length > 0 && (
            <thead>
              <tr className="bg-amber-500/10 border-b border-amber-200/70 dark:border-zinc-700 text-amber-900 dark:text-amber-300 font-bold">
                {headers.map((h, idx) => (
                  <th key={idx} className="px-3.5 py-2.5 whitespace-nowrap">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
          )}
          <tbody className="divide-y divide-amber-100/80 dark:divide-zinc-800">
            {rows.map((row, rIdx) => (
              <tr key={rIdx} className={rIdx % 2 === 1 ? 'bg-amber-50/30 dark:bg-zinc-850/40' : ''}>
                {(row.cells || []).map((cell, cIdx) => {
                  const cellKey = `${rIdx}-${cIdx}`;
                  const isMasked = cell.isMasked;
                  const isRevealed = revealedCells[cellKey];

                  return (
                    <td key={cIdx} className="px-3.5 py-2.5 text-ink-2 align-middle leading-relaxed">
                      {isMasked ? (
                        <button
                          type="button"
                          onClick={() => toggleCell(cellKey)}
                          className={`px-2.5 py-1 rounded-lg text-[12px] font-semibold transition-all cursor-pointer inline-flex items-center gap-1.5 shadow-2xs ${
                            isRevealed
                              ? 'bg-emerald-100 text-emerald-900 border border-emerald-300 dark:bg-emerald-950/60 dark:text-emerald-200'
                              : 'bg-amber-200/80 hover:bg-amber-300 text-amber-950 border border-amber-300/80 dark:bg-amber-900/60 dark:text-amber-100'
                          }`}
                          title={isRevealed ? 'Tekrar gizlemek için tıkla' : 'Hücreyi açmak için tıkla'}
                        >
                          {isRevealed ? (
                            <span>{cell.text}</span>
                          ) : (
                            <span className="italic font-mono text-[11px] opacity-85">
                              [Tıkla & Gör{cell.hint ? `: ${cell.hint}` : ''}]
                            </span>
                          )}
                        </button>
                      ) : (
                        <span>{cell.text}</span>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
