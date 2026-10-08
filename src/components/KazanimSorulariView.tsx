import React, { useEffect, useMemo, useState } from 'react';
import { Check, X, RotateCcw, ChevronDown, ChevronLeft, History, Target } from 'lucide-react';

/**
 * Kurul 1 kazanım temelli örnek sorular (/ornek-sorular, varsayılan sekme).
 * Veri: src/data/ornek_sorular/k1/<ders-id>.json — `python -m v2 ornek-k1 build --export`
 * (ders paketi özeti + bilgi paketi + müfredat kazanımları; editör yazımı, doğrulayıcıdan geçmiş).
 * Ders → kazanım → sorular; her kazanımda en az bir kolay/orta/zor soru, her şık için açıklama.
 */
type Zorluk = 'kolay' | 'orta' | 'zor';
type Soru = {
  id: string;
  kazanim: number;
  zorluk: Zorluk;
  soru: string;
  secenekler: Record<string, string>;
  dogru: string;
  aciklama: string;
  sik_aciklamalari: Record<string, string>;
};
type Cikmis = { id: string; soru: string; secenekler: Record<string, string>; cevap?: string | null };
type Kazanim = { no: number; metin: string; sorular: Soru[]; ilgili_cikmis: Cikmis[] };
type Ders = {
  id: string; sira: number; ders: string; konu: string; ogretim_uyesi: string; tarih: string;
  kazanimlar: Kazanim[]; soru_sayisi: number;
};
type IndexRow = { id: string; sira: number; ders: string; konu: string; ogretim_uyesi: string; soru_sayisi: number; kazanim: number };

const indexModules = import.meta.glob('../data/ornek_sorular/k1/index.json', { eager: true, import: 'default' }) as Record<string, IndexRow[]>;
const loaders = import.meta.glob('../data/ornek_sorular/k1/k1-*.json', { import: 'default' }) as Record<string, () => Promise<Ders>>;
const INDEX: IndexRow[] = Object.values(indexModules)[0] || [];

const LETTERS = ['A', 'B', 'C', 'D', 'E'];
const ZORLUK_STIL: Record<Zorluk, string> = {
  kolay: 'bg-ok-tint text-ok',
  orta: 'bg-accent-soft text-accent',
  zor: 'bg-warn-soft text-warn',
};
const SECIM_KEY = 'medsoru_ornek_k1_ders';

function readSecim(): string | null {
  try { return window.localStorage.getItem(SECIM_KEY); } catch { return null; }
}
function writeSecim(v: string | null) {
  try { v ? window.localStorage.setItem(SECIM_KEY, v) : window.localStorage.removeItem(SECIM_KEY); } catch { /* depolama kapalı */ }
}

function SoruKarti({ q, n, onAnswer }: { q: Soru; n: number; onAnswer: (id: string, ok: boolean | null) => void }) {
  const [picked, setPicked] = useState<string | null>(null);
  const done = picked !== null;
  const correct = picked === q.dogru;
  const pick = (k: string) => { setPicked(k); onAnswer(q.id, k === q.dogru); };
  const reset = () => { setPicked(null); onAnswer(q.id, null); };
  return (
    <article className="bg-white border border-line rounded-2xl p-4 sm:p-5 flex flex-col gap-3">
      <header className="flex items-center gap-2 text-[12.5px] text-ink-3">
        <span className="font-mono font-semibold text-ink">{n}.</span>
        <span className={`px-1.5 py-0.5 rounded-md text-[11.5px] font-semibold capitalize ${ZORLUK_STIL[q.zorluk]}`}>{q.zorluk}</span>
      </header>
      <p className="m-0 text-[16px] font-medium text-ink leading-[1.55] whitespace-pre-line">{q.soru}</p>
      <ol className="list-none m-0 p-0 flex flex-col gap-1.5" aria-label="Şıklar">
        {LETTERS.filter((k) => q.secenekler[k]).map((k) => {
          const isRight = k === q.dogru;
          const isPicked = k === picked;
          const tone = !done
            ? 'bg-white border-line-soft hover:border-accent cursor-pointer'
            : isRight
            ? 'bg-ok-tint border-emerald-400'
            : isPicked
            ? 'bg-rose-50 border-rose-300'
            : 'bg-white border-line-soft';
          return (
            <li key={k} className={`rounded-xl border ${tone}`}>
              <button
                type="button"
                disabled={done}
                onClick={() => pick(k)}
                className="w-full min-h-11 grid grid-cols-[28px_minmax(0,1fr)_auto] items-center gap-2.5 px-3 py-2.5 text-left disabled:cursor-default"
                aria-pressed={isPicked}
              >
                <span className={`w-7 h-7 rounded-lg flex items-center justify-center font-mono text-[13px] font-semibold ${done && isRight ? 'bg-ok text-white' : 'bg-canvas text-ink-2'}`}>{k}</span>
                <span className="text-[14.5px] leading-[1.45] text-ink">{q.secenekler[k]}</span>
                {done && isRight ? <Check className="w-4 h-4 text-ok" aria-label="Doğru şık" /> : done && isPicked ? <X className="w-4 h-4 text-rose-600" aria-label="Seçtiğiniz yanlış şık" /> : <span />}
              </button>
              {done && q.sik_aciklamalari[k] && (
                <p className={`m-0 px-3 pb-2.5 pl-[50px] text-[13.5px] leading-relaxed ${isRight ? 'text-ok' : 'text-ink-2'}`}>{q.sik_aciklamalari[k]}</p>
              )}
            </li>
          );
        })}
      </ol>
      {done && (
        <div className="flex flex-col gap-2.5">
          <div className={`rounded-xl px-3 py-2.5 text-[14px] leading-relaxed ${correct ? 'bg-ok-tint text-ink' : 'bg-rose-50 text-ink'}`}>
            <span className={`font-semibold ${correct ? 'text-ok' : 'text-rose-700'}`}>{correct ? 'Doğru. ' : `Yanlış, doğru cevap ${q.dogru}. `}</span>
            {q.aciklama}
          </div>
          <button type="button" onClick={reset} className="self-start h-9 px-3 rounded-lg border border-line text-[13px] text-ink-2 inline-flex items-center gap-1.5 cursor-pointer hover:bg-canvas">
            <RotateCcw className="w-3.5 h-3.5" /> Tekrar çöz
          </button>
        </div>
      )}
    </article>
  );
}

function CikmisListesi({ items }: { items: Cikmis[] }) {
  const [open, setOpen] = useState(false);
  if (!items.length) return null;
  return (
    <div className="rounded-xl border border-line-soft bg-field">
      <button type="button" onClick={() => setOpen((o) => !o)} aria-expanded={open}
        className="w-full min-h-10 px-3 flex items-center gap-2 text-[13px] font-semibold text-ink-2 cursor-pointer">
        <History className="w-4 h-4" /> Bu kazanımla ilişkili çıkmış sorular ({items.length})
        <ChevronDown className={`w-4 h-4 ml-auto transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <ul className="m-0 px-3 pb-3 flex flex-col gap-2 list-none">
          {items.map((c) => (
            <li key={c.id} className="text-[13.5px] text-ink-2 leading-relaxed border-t border-line-soft pt-2">
              <p className="m-0 text-ink">{c.soru}</p>
              {Object.keys(c.secenekler || {}).length > 0 && (
                <p className="m-0 mt-1 text-[12.5px]">
                  {Object.entries(c.secenekler).map(([k, v]) => (
                    <span key={k} className={`mr-3 ${c.cevap === k ? 'font-semibold text-ok' : ''}`}>{k}) {v}</span>
                  ))}
                </p>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function DersGorunumu({ id, onBack }: { id: string; onBack: () => void }) {
  const [ders, setDers] = useState<Ders | null>(null);
  const [hata, setHata] = useState(false);
  const [sonuc, setSonuc] = useState<Record<string, boolean>>({});
  const [zorluk, setZorluk] = useState<Zorluk | ''>('');

  useEffect(() => {
    const load = loaders[`../data/ornek_sorular/k1/${id}.json`];
    if (!load) { setHata(true); return; }
    setDers(null); setSonuc({});
    load().then(setDers).catch(() => setHata(true));
  }, [id]);

  const onAnswer = (qid: string, ok: boolean | null) =>
    setSonuc((s) => { const n = { ...s }; if (ok === null) delete n[qid]; else n[qid] = ok; return n; });

  if (hata) return <p className="m-0 text-[14px] text-rose-700">Bu dersin soruları yüklenemedi. Sayfayı yenileyip tekrar deneyin.</p>;
  if (!ders) return <p className="m-0 text-[14px] text-ink-3">Sorular yükleniyor…</p>;

  const cozulen = Object.keys(sonuc).length;
  const dogru = Object.values(sonuc).filter(Boolean).length;
  let sayac = 0;

  return (
    <div className="flex flex-col gap-4">
      <button type="button" onClick={onBack} className="self-start h-9 px-2.5 -ml-1 rounded-lg text-[13.5px] text-ink-2 inline-flex items-center gap-1 cursor-pointer hover:bg-canvas">
        <ChevronLeft className="w-4 h-4" /> Tüm dersler
      </button>
      <header className="flex flex-col gap-1.5">
        <span className="ms-eyebrow">Kurul 1 · {ders.sira}. ders · {ders.ders}</span>
        <h2 className="m-0 text-[22px] sm:text-[24px] font-bold text-ink leading-tight">{ders.konu}</h2>
        <p className="m-0 text-[13.5px] text-ink-3">{ders.ogretim_uyesi} · {ders.kazanimlar.length} kazanım · {ders.soru_sayisi} soru</p>
      </header>

      <div className="sticky top-0 z-10 -mx-1 px-1 py-2 bg-canvas/95 backdrop-blur flex flex-wrap items-center gap-2">
        <div className="flex gap-1" role="group" aria-label="Zorluk filtresi">
          {(['', 'kolay', 'orta', 'zor'] as const).map((z) => (
            <button key={z || 'tum'} type="button" onClick={() => setZorluk(z)} aria-pressed={zorluk === z}
              className={`h-9 px-3 rounded-lg text-[13px] font-medium cursor-pointer border ${zorluk === z ? 'bg-ink text-white border-ink' : 'bg-white text-ink-2 border-line hover:bg-canvas'}`}>
              {z ? z[0].toUpperCase() + z.slice(1) : 'Tümü'}
            </button>
          ))}
        </div>
        <span className="ml-auto text-[13px] text-ink-2 font-mono">{cozulen}/{ders.soru_sayisi} çözüldü · {dogru} doğru</span>
      </div>

      {ders.kazanimlar.map((k) => {
        const qs = k.sorular.filter((q) => !zorluk || q.zorluk === zorluk);
        return (
          <section key={k.no} className="flex flex-col gap-3" aria-labelledby={`kz-${k.no}`}>
            <div className="flex items-start gap-2.5 rounded-xl bg-accent-soft px-3.5 py-3">
              <Target className="w-4 h-4 mt-0.5 shrink-0 text-accent" />
              <div className="min-w-0">
                <h3 id={`kz-${k.no}`} className="m-0 text-[14.5px] font-semibold text-ink leading-snug">
                  <span className="font-mono text-accent mr-1.5">K{k.no}</span>{k.metin}
                </h3>
                <p className="m-0 mt-0.5 text-[12.5px] text-ink-3">{k.sorular.length} soru</p>
              </div>
            </div>
            {qs.map((q) => { sayac += 1; return <SoruKarti key={q.id} q={q} n={sayac} onAnswer={onAnswer} />; })}
            <CikmisListesi items={k.ilgili_cikmis} />
          </section>
        );
      })}
    </div>
  );
}

export const KazanimSorulariView: React.FC = () => {
  const [secili, setSecili] = useState<string | null>(() => {
    const s = readSecim();
    return s && INDEX.some((x) => x.id === s) ? s : null;
  });
  const [brans, setBrans] = useState('');
  const branslar = useMemo(() => Array.from(new Set(INDEX.map((x) => x.ders))), []);
  const liste = INDEX.filter((x) => !brans || x.ders === brans);

  const sec = (id: string | null) => { setSecili(id); writeSecim(id); window.scrollTo({ top: 0 }); };

  if (secili) return <DersGorunumu id={secili} onBack={() => sec(null)} />;

  if (!INDEX.length) {
    return <p className="m-0 rounded-2xl border border-line bg-white p-6 text-center text-[14px] text-ink-3">Kurul 1 örnek soruları henüz hazırlanmadı.</p>;
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-wrap gap-1.5" role="group" aria-label="Ders (branş) filtresi">
        {['', ...branslar].map((b) => (
          <button key={b || 'tum'} type="button" onClick={() => setBrans(b)} aria-pressed={brans === b}
            className={`h-9 px-3 rounded-lg text-[13px] font-medium cursor-pointer border ${brans === b ? 'bg-ink text-white border-ink' : 'bg-white text-ink-2 border-line hover:bg-canvas'}`}>
            {b || 'Tüm dersler'}
          </button>
        ))}
      </div>
      <ul className="m-0 p-0 list-none flex flex-col gap-1.5">
        {liste.map((x) => (
          <li key={x.id}>
            <button type="button" onClick={() => sec(x.id)}
              className="w-full min-h-14 grid grid-cols-[36px_minmax(0,1fr)_auto] items-center gap-3 px-3.5 py-2.5 rounded-xl border border-line bg-white text-left cursor-pointer hover:border-accent">
              <span className="font-mono text-[13px] text-ink-3">{String(x.sira).padStart(2, '0')}</span>
              <span className="min-w-0">
                <span className="block text-[15px] font-semibold text-ink leading-snug">{x.konu}</span>
                <span className="block text-[12.5px] text-ink-3">{x.ders} · {x.ogretim_uyesi}</span>
              </span>
              <span className="text-right text-[12.5px] text-ink-2 font-mono leading-tight">{x.soru_sayisi} soru<br />{x.kazanim} kazanım</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export const KAZANIM_INDEX = INDEX;
export default KazanimSorulariView;
