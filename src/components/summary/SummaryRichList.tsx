import React from 'react';
import { ArrowRight, CheckCircle2, HelpCircle, Info, Pill } from 'lucide-react';
import type { InlineListKind, RegimenBlock, RichGroup, RichItem } from './summaryStructure';

/** Konu grubu renkleri; aynı başlık her bölümde aynı rengi alır */
const TONES = [
  { bar: 'border-l-teal-500', head: 'bg-teal-50/80 dark:bg-teal-950/40 text-teal-900 dark:text-teal-200', dot: 'bg-teal-500', num: 'bg-teal-600', line: 'border-teal-200 dark:border-teal-800', chip: 'bg-teal-50 dark:bg-teal-950/50 border-teal-200 dark:border-teal-800 text-teal-900 dark:text-teal-100' },
  { bar: 'border-l-indigo-500', head: 'bg-indigo-50/80 dark:bg-indigo-950/40 text-indigo-900 dark:text-indigo-200', dot: 'bg-indigo-500', num: 'bg-indigo-600', line: 'border-indigo-200 dark:border-indigo-800', chip: 'bg-indigo-50 dark:bg-indigo-950/50 border-indigo-200 dark:border-indigo-800 text-indigo-900 dark:text-indigo-100' },
  { bar: 'border-l-amber-500', head: 'bg-amber-50/80 dark:bg-amber-950/40 text-amber-900 dark:text-amber-200', dot: 'bg-amber-500', num: 'bg-amber-600', line: 'border-amber-200 dark:border-amber-800', chip: 'bg-amber-50 dark:bg-amber-950/50 border-amber-200 dark:border-amber-800 text-amber-900 dark:text-amber-100' },
  { bar: 'border-l-rose-500', head: 'bg-rose-50/80 dark:bg-rose-950/40 text-rose-900 dark:text-rose-200', dot: 'bg-rose-500', num: 'bg-rose-600', line: 'border-rose-200 dark:border-rose-800', chip: 'bg-rose-50 dark:bg-rose-950/50 border-rose-200 dark:border-rose-800 text-rose-900 dark:text-rose-100' },
  { bar: 'border-l-sky-500', head: 'bg-sky-50/80 dark:bg-sky-950/40 text-sky-900 dark:text-sky-200', dot: 'bg-sky-500', num: 'bg-sky-600', line: 'border-sky-200 dark:border-sky-800', chip: 'bg-sky-50 dark:bg-sky-950/50 border-sky-200 dark:border-sky-800 text-sky-900 dark:text-sky-100' },
  { bar: 'border-l-violet-500', head: 'bg-violet-50/80 dark:bg-violet-950/40 text-violet-900 dark:text-violet-200', dot: 'bg-violet-500', num: 'bg-violet-600', line: 'border-violet-200 dark:border-violet-800', chip: 'bg-violet-50 dark:bg-violet-950/50 border-violet-200 dark:border-violet-800 text-violet-900 dark:text-violet-100' },
];
type Tone = (typeof TONES)[number];

const NEUTRAL: Tone = {
  bar: 'border-l-slate-300 dark:border-l-slate-600',
  head: '',
  dot: 'bg-teal-600',
  num: 'bg-teal-600',
  line: 'border-slate-200 dark:border-slate-700',
  chip: 'bg-slate-50 dark:bg-slate-800/60 border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-100',
};

const toneFor = (title: string): Tone => {
  let h = 0;
  for (const ch of title.toLocaleLowerCase('tr')) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return TONES[h % TONES.length];
};

type RenderText = (text: string) => React.ReactNode;

const InlineList: React.FC<{ kind: InlineListKind; items: string[]; tone: Tone; renderText: RenderText }> = ({ kind, items, tone, renderText }) => {
  if (kind === 'steps') {
    return (
      <ol className="list-none m-0 p-0 space-y-1.5">
        {items.map((it, i) => (
          <li key={i} className="flex items-start gap-2.5">
            <span className={`w-5 h-5 rounded-full ${tone.num} text-white text-[11px] font-bold flex items-center justify-center shrink-0 mt-0.5 tabular-nums`}>{i + 1}</span>
            <span className="min-w-0 leading-relaxed">{renderText(it)}</span>
          </li>
        ))}
      </ol>
    );
  }
  if (kind === 'checks') {
    return (
      <ul className="list-none m-0 p-0 space-y-1.5">
        {items.map((it, i) => (
          <li key={i} className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
            <span className="min-w-0 leading-relaxed">{renderText(it)}</span>
          </li>
        ))}
      </ul>
    );
  }
  // Kısa maddeler etiket gibi yan yana; uzunlar alt alta
  if (items.every((it) => it.length <= 36)) {
    return (
      <div className="flex flex-wrap gap-1.5">
        {items.map((it, i) => (
          <span key={i} className={`px-2 py-0.5 rounded-md border text-[0.95em] font-medium ${tone.chip}`}>
            {renderText(it)}
          </span>
        ))}
      </div>
    );
  }
  return (
    <ul className="list-none m-0 p-0 space-y-1.5">
      {items.map((it, i) => (
        <li key={i} className="flex items-start gap-2">
          <span className={`w-1.5 h-1.5 rounded-sm ${tone.dot} shrink-0 mt-[0.55em]`} />
          <span className="min-w-0 leading-relaxed">{renderText(it)}</span>
        </li>
      ))}
    </ul>
  );
};

/** Tedavi seçenekleri: numaralı kutu, satır satır ilaç, doz etiketleri, "→" devam ve not */
const RegimenList: React.FC<{ block: RegimenBlock; tone: Tone; renderText: RenderText }> = ({ block, tone, renderText }) => (
  <div className="space-y-2">
    <ol className="list-none m-0 p-0 space-y-2">
      {block.items.map((r, i) => (
        <li key={i} className="rounded-lg border border-[var(--reader-border,#e2e8f0)] bg-[var(--reader-surface,#f8fafc)] px-3 py-2.5 space-y-1.5">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`h-5 min-w-5 px-1.5 rounded-full ${tone.num} text-white text-[11px] font-bold inline-flex items-center justify-center tabular-nums`}>{i + 1}</span>
            {block.items.length > 1 && <span className="text-[11px] font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">Seçenek</span>}
            {r.condition && (
              <span className="px-2 py-0.5 rounded-md text-[0.9em] font-semibold bg-amber-100 text-amber-900 dark:bg-amber-950/60 dark:text-amber-200">{renderText(r.condition)}</span>
            )}
          </div>
          <ul className="list-none m-0 p-0 space-y-1">
            {r.drugs.map((d, di) => (
              <li key={di} className="flex items-start gap-2">
                <span className="w-4 shrink-0 mt-0.5 text-center font-bold text-slate-400">{di > 0 ? '+' : <Pill className="w-4 h-4 text-slate-400" />}</span>
                <span className="min-w-0 flex flex-wrap items-center gap-x-1.5 gap-y-1">
                  <span className="font-semibold text-slate-900 dark:text-slate-100">{renderText(d.name)}</span>
                  {d.route && <span className="px-1.5 rounded text-[10.5px] font-bold bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-200">{d.route}</span>}
                  {d.doses.map((dose, k) => (
                    <React.Fragment key={k}>
                      {k > 0 && <span className="text-[0.85em] italic text-slate-500">veya</span>}
                      <span className={`reader-dose px-2 py-0.5 rounded-md border text-[0.95em] font-medium ${tone.chip}`}>{renderText(dose)}</span>
                    </React.Fragment>
                  ))}
                </span>
              </li>
            ))}
          </ul>
          {r.then && (
            <p className="m-0 flex items-start gap-2 text-slate-600 dark:text-slate-300 leading-relaxed">
              <ArrowRight className="w-4 h-4 shrink-0 mt-0.5 text-slate-400" />
              <span>{renderText(r.then)}</span>
            </p>
          )}
          {r.note && (
            <p className="m-0 flex items-start gap-2 text-slate-500 dark:text-slate-400 text-[0.95em] leading-relaxed">
              <Info className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{renderText(r.note)}</span>
            </p>
          )}
        </li>
      ))}
    </ol>
    {block.after && <p className="m-0 pt-1 font-semibold text-slate-900 dark:text-slate-100">{renderText(block.after)}</p>}
  </div>
);

const ItemView: React.FC<{ item: RichItem; tone: Tone; depth: number; renderText: RenderText }> = ({ item, tone, depth, renderText }) => (
  <li className="flex items-start gap-2.5">
    {/* Yalnızca listeden oluşan madde kendi işaretlerini taşır; ayrıca nokta konmaz */}
    {!item.label && !item.text && (item.list || item.regimens) ? null : depth === 0 ? (
      <span className={`w-2 h-2 rounded-full ${tone.dot} shrink-0 mt-[0.5em]`} />
    ) : (
      <span className="w-1.5 h-1.5 rounded-full bg-slate-400 dark:bg-slate-500 shrink-0 mt-[0.55em]" />
    )}
    <div className="min-w-0 flex-1 space-y-1.5">
      {item.label && (
        <p className="m-0 font-semibold text-slate-900 dark:text-slate-100 leading-snug flex items-start gap-1.5">
          {item.label.endsWith('?') && <HelpCircle className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />}
          <span>{renderText(item.label)}</span>
        </p>
      )}
      {item.text && <p className="m-0 text-slate-700 dark:text-slate-300 leading-relaxed">{renderText(item.text)}</p>}
      {item.list && (
        <div className="text-slate-700 dark:text-slate-300">
          <InlineList kind={item.list.kind} items={item.list.items} tone={tone} renderText={renderText} />
        </div>
      )}
      {item.regimens && (
        <div className="text-slate-700 dark:text-slate-300">
          <RegimenList block={item.regimens} tone={tone} renderText={renderText} />
        </div>
      )}
      {item.children.length > 0 && (
        <ul className={`list-none m-0 pl-3 border-l-2 ${tone.line} space-y-2`}>
          {item.children.map((c, i) => (
            <ItemView key={i} item={c} tone={tone} depth={depth + 1} renderText={renderText} />
          ))}
        </ul>
      )}
    </div>
  </li>
);

/** Ders özeti maddelerini konu kartları, numaralı adımlar ve işaret listeleriyle çizer. */
export const SummaryRichList: React.FC<{ groups: RichGroup[]; renderText: RenderText }> = ({ groups, renderText }) => (
  <div className="space-y-3 text-xs sm:text-sm">
    {groups.map((g, gi) => {
      const tone = g.title ? toneFor(g.title) : NEUTRAL;
      return (
        <div
          key={gi}
          className={`rounded-xl border border-[var(--reader-border,#e2e8f0)] border-l-4 ${tone.bar} bg-[var(--reader-card,#ffffff)] overflow-hidden shadow-2xs`}
        >
          {g.title && (
            <div className={`px-3.5 sm:px-4 py-2 flex items-center gap-2 ${tone.head}`}>
              <h4 className="m-0 font-bold text-[0.95em] tracking-tight">{renderText(g.title)}</h4>
              <span className="ml-auto text-[11px] font-medium opacity-70 tabular-nums">{g.items.length} madde</span>
            </div>
          )}
          <ul className="list-none m-0 px-3.5 sm:px-4 py-3 space-y-3">
            {g.items.map((it, i) => (
              <ItemView key={i} item={it} tone={tone} depth={0} renderText={renderText} />
            ))}
          </ul>
        </div>
      );
    })}
  </div>
);
