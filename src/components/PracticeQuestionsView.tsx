import React, { useEffect, useMemo, useState } from 'react';
import { BookOpen, Check, X, RotateCcw, Sparkles, Filter } from 'lucide-react';
import { PageHeader } from './ui/PageHeader';
import { safeJsonFetch } from '../services/api';
import { KazanimSorulariView, KAZANIM_INDEX } from './KazanimSorulariView';

/**
 * Örnek çalışma soruları (/ornek-sorular): müfredata dayalı, Drive ders notlarından (drive_root) yapay zekâ ile üretilmiş,
 * her biri ders notundan birebir alıntıyla kaynaklı. Yönetici doğrulamasından geçmemiştir — sayfada açıkça belirtilir.
 * Veri: /api/practice-questions (meds_database/derived/ornek_sorular/sorular.jsonl).
 */
type PQ = {
  id: string;
  kurul: number;
  ders: string;
  konu: string;
  soru_koku: string;
  secenekler: Record<string, string>;
  dogru_secenek: string;
  aciklama_maddeleri: string[];
  zorluk?: string;
  kaynak: { ders_notu?: string; sayfa?: number; alinti?: string };
  model?: string;
  olusturma?: string;
};

const LETTERS = ['A', 'B', 'C', 'D', 'E'];

function QuestionCard({ q, n }: { q: PQ; n: number }) {
  const [picked, setPicked] = useState<string | null>(null);
  const done = picked !== null;
  const correct = picked === q.dogru_secenek;
  return (
    <article className="bg-white border border-line rounded-2xl p-4 sm:p-5 flex flex-col gap-3">
      <header className="flex flex-wrap items-center gap-2 text-[12.5px] text-ink-3">
        <span className="font-mono font-semibold text-ink">{n}.</span>
        <span>Kurul {q.kurul} · {q.ders}</span>
        {q.zorluk && <span className="px-1.5 py-0.5 rounded bg-canvas text-ink-2">{q.zorluk}</span>}
      </header>
      <p className="m-0 text-[16px] sm:text-[17px] font-medium text-ink leading-[1.5]">{q.soru_koku}</p>
      <ol className="list-none m-0 p-0 flex flex-col gap-1.5" aria-label="Şıklar">
        {LETTERS.filter((k) => q.secenekler[k]).map((k) => {
          const isRight = k === q.dogru_secenek;
          const isPicked = k === picked;
          const tone = !done
            ? 'bg-white border-line-soft hover:border-accent cursor-pointer'
            : isRight
            ? 'bg-ok-tint border-emerald-400'
            : isPicked
            ? 'bg-rose-50 border-rose-300'
            : 'bg-white border-line-soft opacity-80';
          return (
            <li key={k}>
              <button
                type="button"
                disabled={done}
                onClick={() => setPicked(k)}
                className={`w-full min-h-11 grid grid-cols-[28px_minmax(0,1fr)_auto] items-center gap-2.5 px-3 py-2.5 rounded-xl border text-left ${tone}`}
                aria-pressed={isPicked}
              >
                <span className={`w-7 h-7 rounded-lg flex items-center justify-center font-mono text-[13px] font-semibold ${done && isRight ? 'bg-ok text-white' : 'bg-canvas text-ink-2'}`}>{k}</span>
                <span className="text-[14.5px] leading-[1.45] text-ink">{q.secenekler[k]}</span>
                {done && isRight ? <Check className="w-4 h-4 text-ok" /> : done && isPicked ? <X className="w-4 h-4 text-rose-600" /> : <span />}
              </button>
            </li>
          );
        })}
      </ol>
      {done && (
        <div className="flex flex-col gap-2.5">
          <p className={`m-0 text-[14px] font-semibold ${correct ? 'text-ok' : 'text-rose-700'}`}>
            {correct ? 'Doğru!' : `Yanlış — doğru cevap ${q.dogru_secenek}`}
          </p>
          <ul className="m-0 pl-5 flex flex-col gap-1 text-[14px] text-ink-2 leading-relaxed">
            {q.aciklama_maddeleri.map((m, i) => (
              <li key={i}>{m}</li>
            ))}
          </ul>
          {q.kaynak?.alinti && (
            <blockquote className="m-0 rounded-xl bg-field px-3 py-2.5 text-[13px] text-ink-2 flex flex-col gap-1">
              <span className="flex items-center gap-1.5 text-[12px] font-semibold text-ink-3">
                <BookOpen className="w-3.5 h-3.5" /> {q.kaynak.ders_notu}
                {q.kaynak.sayfa ? ` · sayfa ${q.kaynak.sayfa}` : ''}
              </span>
              <span className="italic">“{q.kaynak.alinti}”</span>
            </blockquote>
          )}
          <button type="button" onClick={() => setPicked(null)} className="self-start h-9 px-3 rounded-lg border border-line text-[13px] text-ink-2 inline-flex items-center gap-1.5 cursor-pointer hover:bg-canvas">
            <RotateCcw className="w-3.5 h-3.5" /> Tekrar çöz
          </button>
        </div>
      )}
    </article>
  );
}

const SEKME_KEY = 'medsoru_ornek_sekme';

export const PracticeQuestionsView: React.FC = () => {
  const [sekme, setSekme] = useState<'k1' | 'diger'>(() => {
    try { return window.localStorage.getItem(SEKME_KEY) === 'diger' ? 'diger' : 'k1'; } catch { return 'k1'; }
  });
  const sekmeSec = (v: 'k1' | 'diger') => { setSekme(v); try { window.localStorage.setItem(SEKME_KEY, v); } catch { /* depolama kapalı */ } };
  const k1Soru = KAZANIM_INDEX.reduce((a, x) => a + x.soru_sayisi, 0);
  const k1Kazanim = KAZANIM_INDEX.reduce((a, x) => a + x.kazanim, 0);
  const sekmeBtn = (v: 'k1' | 'diger', label: string) => (
    <button type="button" role="tab" aria-selected={sekme === v} onClick={() => sekmeSec(v)}
      className={`h-10 px-3.5 rounded-lg text-[14px] font-medium cursor-pointer ${sekme === v ? 'bg-white text-ink shadow-sm' : 'text-ink-2 hover:text-ink'}`}>
      {label}
    </button>
  );

  return (
    <div className="flex flex-col gap-4 pb-16 w-full max-w-3xl mx-auto min-w-0">
      <PageHeader
        title="Örnek sorular"
        description="Kurul 1 derslerinin müfredat kazanımlarına göre hazırlanmış çalışma soruları. Her kazanımda kolay, orta ve zor sorular; cevapladıktan sonra her şıkkın neden doğru ya da yanlış olduğu gösterilir."
        stats={sekme === 'k1' ? [
          { label: 'Ders', value: String(KAZANIM_INDEX.length) },
          { label: 'Kazanım', value: k1Kazanim.toLocaleString('tr-TR') },
          { label: 'Soru', value: k1Soru.toLocaleString('tr-TR') },
        ] : undefined}
      />
      <div role="tablist" aria-label="Soru kümesi" className="self-start flex gap-1 p-1 rounded-xl bg-field border border-line-soft">
        {sekmeBtn('k1', 'Kurul 1 · kazanım temelli')}
        {sekmeBtn('diger', 'Diğer üretim')}
      </div>
      {sekme === 'k1' ? <KazanimSorulariView /> : <EskiUretim />}
    </div>
  );
};

/** Daha önce API'den gelen, yapay zekâ ile üretilmiş ve doğrulanmamış sorular (meds_database/derived/ornek_sorular). */
const EskiUretim: React.FC = () => {
  const [all, setAll] = useState<PQ[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [kurul, setKurul] = useState<string>('');
  const [ders, setDers] = useState<string>('');
  const [konu, setKonu] = useState<string>('');

  useEffect(() => {
    safeJsonFetch<{ sorular: PQ[] }>('/api/practice-questions').then((r) => {
      if (r.ok && r.data) setAll(r.data.sorular || []);
      else setError('Örnek sorular alınamadı. Bağlantınızı kontrol edip sayfayı yenileyin.');
    });
  }, []);

  const opts = useMemo(() => {
    const list = all || [];
    const kurullar = Array.from(new Set(list.map((q) => q.kurul))).sort((a, b) => a - b);
    const dersler = Array.from(new Set(list.filter((q) => !kurul || String(q.kurul) === kurul).map((q) => q.ders)));
    const konular = Array.from(new Set(list.filter((q) => (!kurul || String(q.kurul) === kurul) && (!ders || q.ders === ders)).map((q) => q.konu)));
    return { kurullar, dersler, konular };
  }, [all, kurul, ders]);

  const shown = useMemo(
    () => (all || []).filter((q) => (!kurul || String(q.kurul) === kurul) && (!ders || q.ders === ders) && (!konu || q.konu === konu)),
    [all, kurul, ders, konu],
  );
  // Konu başlıklarına göre grupla (müfredat sırası korunur: üretim sırası müfredat sırasıdır)
  const groups = useMemo(() => {
    const m = new Map<string, PQ[]>();
    for (const q of shown) {
      const key = `Kurul ${q.kurul} · ${q.ders} · ${q.konu}`;
      m.set(key, [...(m.get(key) || []), q]);
    }
    return Array.from(m.entries());
  }, [shown]);

  const sel = 'h-11 px-3 rounded-xl border border-line bg-white text-[14px] text-ink min-w-0';

  return (
    <div className="flex flex-col gap-4">

      <p className="m-0 rounded-xl bg-amber-50 text-amber-900 px-3.5 py-2.5 text-[13px] flex items-start gap-2">
        <Sparkles className="w-4 h-4 shrink-0 mt-0.5" />
        Bu sorular yapay zekâ ile üretildi ve henüz bir öğretim üyesi ya da yönetici tarafından doğrulanmadı. Cevaplar ders notu
        alıntısına dayanır; şüpheli gördüğünüz soruyu ders notundan kontrol edin.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2" role="group" aria-label="Filtreler">
        <label className="sr-only" htmlFor="pq-kurul">Kurul</label>
        <select id="pq-kurul" className={sel} value={kurul} onChange={(e) => { setKurul(e.target.value); setDers(''); setKonu(''); }}>
          <option value="">Tüm kurullar</option>
          {opts.kurullar.map((k) => <option key={k} value={k}>Kurul {k}</option>)}
        </select>
        <label className="sr-only" htmlFor="pq-ders">Ders</label>
        <select id="pq-ders" className={sel} value={ders} onChange={(e) => { setDers(e.target.value); setKonu(''); }}>
          <option value="">Tüm dersler</option>
          {opts.dersler.map((d) => <option key={d} value={d}>{d}</option>)}
        </select>
        <label className="sr-only" htmlFor="pq-konu">Konu</label>
        <select id="pq-konu" className={sel} value={konu} onChange={(e) => setKonu(e.target.value)}>
          <option value="">Tüm konular</option>
          {opts.konular.map((k) => <option key={k} value={k}>{k}</option>)}
        </select>
      </div>

      {error ? (
        <p className="m-0 text-[14px] text-rose-700">{error}</p>
      ) : all === null ? (
        <p className="m-0 text-[14px] text-ink-3">Sorular yükleniyor…</p>
      ) : shown.length === 0 ? (
        <div className="rounded-2xl border border-line bg-white p-8 text-center text-ink-3 text-[14px] flex flex-col items-center gap-2">
          <Filter className="w-6 h-6" />
          {all.length === 0 ? 'Henüz örnek soru üretilmedi. Sorular her gün müfredat sırasıyla eklenir.' : 'Bu filtreye uyan soru yok.'}
        </div>
      ) : (
        groups.map(([title, qs]) => (
          <section key={title} className="flex flex-col gap-3">
            <h2 className="m-0 text-[13px] font-semibold uppercase tracking-wide text-ink-3">{title} · {qs.length} soru</h2>
            {qs.map((q, i) => (
              <QuestionCard key={q.id} q={q} n={i + 1} />
            ))}
          </section>
        ))
      )}
    </div>
  );
};

export default PracticeQuestionsView;
