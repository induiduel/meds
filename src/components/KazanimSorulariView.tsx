import React, { useEffect, useMemo, useState } from 'react';
import { Check, X, RotateCcw, ChevronDown, ChevronLeft, ChevronRight, History, Target, Flag, Maximize2, Search, Trophy } from 'lucide-react';
import { ReportQuestionModal } from './ReportQuestionModal';
import { ApiService } from '../services/api';

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
const CEVAP_KEY = 'medsoru_ornek_k1_cevap';

function readSecim(): string | null {
  try { return window.localStorage.getItem(SECIM_KEY); } catch { return null; }
}
function writeSecim(v: string | null) {
  try { v ? window.localStorage.setItem(SECIM_KEY, v) : window.localStorage.removeItem(SECIM_KEY); } catch { /* depolama kapalı */ }
}

/* Cevaplar (soru id → seçilen şık + doğru mu) tarayıcıda tutulur; ders listesindeki ilerleme buradan okunur. */
type Cevap = { s: string; ok: boolean };
let CEVAPLAR: Record<string, Cevap> = (() => {
  try { return JSON.parse(window.localStorage.getItem(CEVAP_KEY) || '{}') || {}; } catch { return {}; }
})();
const dinleyiciler = new Set<() => void>();
function setCevap(id: string, c: Cevap | null) {
  CEVAPLAR = { ...CEVAPLAR };
  if (c) CEVAPLAR[id] = c; else delete CEVAPLAR[id];
  try { window.localStorage.setItem(CEVAP_KEY, JSON.stringify(CEVAPLAR)); } catch { /* depolama kapalı */ }
  dinleyiciler.forEach((f) => f());
}
function useCevaplar() {
  const [, tik] = useState(0);
  useEffect(() => { const f = () => tik((n) => n + 1); dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; }, []);
  return CEVAPLAR;
}
function dersIlerleme(id: string, c: Record<string, Cevap>) {
  let n = 0, d = 0; const p = `${id.split('-').slice(0, 2).join('-')}-q`;
  for (const k in c) if (k.startsWith(p)) { n++; if (c[k].ok) d++; }
  return { n, d };
}

function BildirButonu({ q, ders }: { q: Soru; ders: string }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button type="button" onClick={() => setOpen(true)} title="Soruda hata ya da sorun bildir" aria-label="Soruyu bildir"
        className="ml-auto h-8 px-2 rounded-lg text-[12.5px] font-semibold inline-flex items-center gap-1 text-ink-3 hover:bg-bad-soft hover:text-bad-text cursor-pointer">
        <Flag className="w-3.5 h-3.5" /><span className="hidden sm:inline">Bildir</span>
      </button>
      {open && (
        <ReportQuestionModal
          question={{ stem: q.soru, correctAnswer: q.dogru, discipline: ders, questionNumber: q.id }}
          onClose={() => setOpen(false)}
          onSubmit={async (reason, details) => {
            await ApiService.reportOrnekQuestion(q.id, reason, [details, `Kaynak: Örnek sorular · ${ders} · K${q.kazanim}`].filter(Boolean).join('\n'));
          }}
        />
      )}
    </>
  );
}

function SoruKarti({ q, n, ders, buyuk = false }: { q: Soru; n: number; ders: string; buyuk?: boolean }) {
  const cevaplar = useCevaplar();
  const picked = cevaplar[q.id]?.s ?? null;
  const done = picked !== null;
  const correct = picked === q.dogru;
  const pick = (k: string) => { if (!done) setCevap(q.id, { s: k, ok: k === q.dogru }); };
  const reset = () => setCevap(q.id, null);
  return (
    <article className={`bg-white border border-line rounded-2xl flex flex-col gap-3 ${buyuk ? 'p-5 sm:p-7' : 'p-4 sm:p-5'}`}>
      <header className="flex items-center gap-2 text-[12.5px] text-ink-3">
        <span className="font-mono font-semibold text-ink">{n}.</span>
        <span className={`px-1.5 py-0.5 rounded-md text-[11.5px] font-semibold capitalize ${ZORLUK_STIL[q.zorluk]}`}>{q.zorluk}</span>
        <span className="font-mono text-[11.5px]">K{q.kazanim}</span>
        <BildirButonu q={q} ders={ders} />
      </header>
      <p className={`m-0 font-medium text-ink leading-[1.55] whitespace-pre-line ${buyuk ? 'text-[18px] sm:text-[19px]' : 'text-[16px]'}`}>{q.soru}</p>
      <ol className="list-none m-0 p-0 flex flex-col gap-1.5" aria-label="Şıklar">
        {LETTERS.filter((k) => q.secenekler[k]).map((k) => {
          const isRight = k === q.dogru;
          const isPicked = k === picked;
          const tone = !done
            ? 'bg-white border-line-soft hover:border-accent hover:bg-accent-soft/40 cursor-pointer'
            : isRight
            ? 'bg-ok-tint border-ok'
            : isPicked
            ? 'bg-bad-soft border-bad'
            : 'bg-white border-line-soft opacity-80';
          return (
            <li key={k} className={`rounded-xl border transition-colors ${tone}`}>
              <button type="button" disabled={done} onClick={() => pick(k)}
                className="w-full min-h-11 grid grid-cols-[28px_minmax(0,1fr)_auto] items-center gap-2.5 px-3 py-2.5 text-left disabled:cursor-default"
                aria-pressed={isPicked}>
                <span className={`w-7 h-7 rounded-lg flex items-center justify-center font-mono text-[13px] font-semibold ${done && isRight ? 'bg-ok text-white' : done && isPicked ? 'bg-bad text-white' : 'bg-canvas text-ink-2'}`}>{k}</span>
                <span className={`${buyuk ? 'text-[15.5px]' : 'text-[14.5px]'} leading-[1.45] text-ink`}>{q.secenekler[k]}</span>
                {done && isRight ? <Check className="w-4 h-4 text-ok" aria-label="Doğru şık" /> : done && isPicked ? <X className="w-4 h-4 text-bad" aria-label="Seçtiğiniz yanlış şık" /> : <span />}
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
          <div className={`rounded-xl px-3 py-2.5 text-[14px] leading-relaxed ${correct ? 'bg-ok-tint text-ink' : 'bg-bad-soft text-ink'}`}>
            <span className={`font-semibold ${correct ? 'text-ok' : 'text-bad-text'}`}>{correct ? 'Doğru. ' : `Yanlış, doğru cevap ${q.dogru}. `}</span>
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

/** Tam ekran çözüm: tek soru, ilerleme çubuğu, klavye (A–E, ←/→, Esc), sonunda özet. */
function TamEkran({ sorular, ders, baslik, onClose }: { sorular: Soru[]; ders: string; baslik: string; onClose: () => void }) {
  const cevaplar = useCevaplar();
  const ilk = Math.max(0, sorular.findIndex((q) => !cevaplar[q.id]));
  const [i, setI] = useState(ilk);
  const ozet = i >= sorular.length;
  const q = sorular[Math.min(i, sorular.length - 1)];
  const cozulen = sorular.filter((x) => cevaplar[x.id]).length;
  const dogru = sorular.filter((x) => cevaplar[x.id]?.ok).length;

  useEffect(() => {
    const prev = document.body.style.overflow; document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = prev; };
  }, []);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (document.querySelector('[role="dialog"][aria-modal="true"]:not([data-tam-ekran])')) return;
      if (e.target instanceof HTMLElement && /INPUT|TEXTAREA/.test(e.target.tagName)) return;
      if (e.key === 'Escape') onClose();
      else if (e.key === 'ArrowRight') setI((n) => Math.min(sorular.length, n + 1));
      else if (e.key === 'ArrowLeft') setI((n) => Math.max(0, n - 1));
      else if (!ozet && q) {
        const k = e.key.toUpperCase();
        if (q.secenekler[k] && !CEVAPLAR[q.id]) setCevap(q.id, { s: k, ok: k === q.dogru });
      }
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [q, ozet, sorular.length, onClose]);

  const yanlislar = sorular.filter((x) => cevaplar[x.id] && !cevaplar[x.id].ok);
  return (
    <div role="dialog" aria-modal="true" data-tam-ekran aria-label="Tam ekran çözüm" className="fixed inset-0 z-50 bg-canvas flex flex-col">
      <div className="shrink-0 border-b border-line bg-white">
        <div className="max-w-5xl mx-auto px-4 h-14 flex items-center gap-3">
          <button type="button" onClick={onClose} aria-label="Tam ekrandan çık" className="h-9 w-9 -ml-2 rounded-lg inline-flex items-center justify-center text-ink-2 hover:bg-canvas cursor-pointer"><X className="w-5 h-5" /></button>
          <span className="min-w-0 truncate text-[14px] font-semibold text-ink">{baslik}</span>
          <span className="ml-auto shrink-0 font-mono text-[13px] text-ink-2">{ozet ? 'Özet' : `${i + 1} / ${sorular.length}`}</span>
        </div>
        <div className="h-1 bg-line-soft"><div className="h-full bg-accent transition-all" style={{ width: `${(cozulen / sorular.length) * 100}%` }} /></div>
      </div>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-5xl mx-auto px-4 py-5 sm:py-8">
          {ozet ? (
            <div className="bg-white border border-line rounded-2xl p-6 flex flex-col gap-4 text-center items-center">
              <Trophy className="w-10 h-10 text-accent" />
              <h3 className="m-0 text-[22px] font-bold text-ink">Bitti!</h3>
              <p className="m-0 text-[15px] text-ink-2">{cozulen} sorudan <b className="text-ok">{dogru}</b> doğru{cozulen ? ` · %${Math.round((dogru / cozulen) * 100)}` : ''}</p>
              {cozulen < sorular.length && <p className="m-0 text-[13px] text-ink-3">{sorular.length - cozulen} soru boş bırakıldı.</p>}
              <div className="flex flex-wrap gap-2 justify-center">
                {yanlislar.length > 0 && (
                  <button type="button" onClick={() => setI(sorular.indexOf(yanlislar[0]))} className="h-10 px-4 rounded-xl border border-line bg-white text-[14px] font-semibold text-ink cursor-pointer hover:bg-canvas">Yanlışlara dön ({yanlislar.length})</button>
                )}
                <button type="button" onClick={() => { sorular.forEach((x) => setCevap(x.id, null)); setI(0); }} className="h-10 px-4 rounded-xl border border-line bg-white text-[14px] font-semibold text-ink cursor-pointer hover:bg-canvas inline-flex items-center gap-1.5"><RotateCcw className="w-4 h-4" /> Baştan çöz</button>
                <button type="button" onClick={onClose} className="h-10 px-4 rounded-xl bg-ink text-white text-[14px] font-semibold cursor-pointer">Kapat</button>
              </div>
            </div>
          ) : (
            <SoruKarti key={q.id} q={q} n={i + 1} ders={ders} buyuk />
          )}
          <p className="hidden sm:block m-0 mt-4 text-center text-[12px] text-ink-3">Klavye: A–E şık seçer · ← → sorular arasında gezer · Esc çıkar</p>
        </div>
      </div>
      <div className="shrink-0 border-t border-line bg-white">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center gap-2">
          <button type="button" disabled={i === 0} onClick={() => setI((n) => Math.max(0, n - 1))}
            className="h-11 px-4 rounded-xl border border-line bg-white text-[14px] font-semibold text-ink-2 inline-flex items-center gap-1 cursor-pointer disabled:opacity-40 disabled:cursor-default"><ChevronLeft className="w-4 h-4" /> Önceki</button>
          <span className="mx-auto text-[13px] text-ink-3 font-mono">{dogru}/{cozulen} doğru</span>
          {!ozet && (
            <button type="button" onClick={() => setI((n) => n + 1)}
              className={`h-11 px-5 rounded-xl text-[14px] font-semibold inline-flex items-center gap-1 cursor-pointer ${cevaplar[q.id] ? 'bg-ink text-white' : 'border border-line bg-white text-ink-2'}`}>
              {i === sorular.length - 1 ? 'Bitir' : cevaplar[q.id] ? 'Sonraki' : 'Atla'} <ChevronRight className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

function DersGorunumu({ id, onBack }: { id: string; onBack: () => void }) {
  const [ders, setDers] = useState<Ders | null>(null);
  const [hata, setHata] = useState(false);
  const [zorluk, setZorluk] = useState<Zorluk | ''>('');
  const [tam, setTam] = useState<{ sorular: Soru[]; baslik: string } | null>(null);
  const cevaplar = useCevaplar();

  useEffect(() => {
    const load = loaders[`../data/ornek_sorular/k1/${id}.json`];
    if (!load) { setHata(true); return; }
    setDers(null);
    load().then(setDers).catch(() => setHata(true));
  }, [id]);

  if (hata) return <p className="m-0 text-[14px] text-bad-text">Bu dersin soruları yüklenemedi. Sayfayı yenileyip tekrar deneyin.</p>;
  if (!ders) return <p className="m-0 text-[14px] text-ink-3">Sorular yükleniyor…</p>;

  const tumu = ders.kazanimlar.flatMap((k) => k.sorular);
  const filtreli = tumu.filter((q) => !zorluk || q.zorluk === zorluk);
  const cozulen = tumu.filter((q) => cevaplar[q.id]).length;
  const dogru = tumu.filter((q) => cevaplar[q.id]?.ok).length;
  const yanlis = tumu.filter((q) => cevaplar[q.id] && !cevaplar[q.id].ok);
  let sayac = 0;

  return (
    <div className="flex flex-col gap-4">
      <button type="button" onClick={onBack} className="self-start h-9 px-2.5 -ml-1 rounded-lg text-[13.5px] text-ink-2 inline-flex items-center gap-1 cursor-pointer hover:bg-canvas">
        <ChevronLeft className="w-4 h-4" /> Tüm dersler
      </button>
      <header className="bg-white border border-line rounded-2xl p-4 sm:p-5 flex flex-col gap-3">
        <div className="flex flex-col gap-1">
          <span className="ms-eyebrow">Kurul 1 · {ders.sira}. ders · {ders.ders}</span>
          <h2 className="m-0 text-[22px] sm:text-[24px] font-bold text-ink leading-tight">{ders.konu}</h2>
          <p className="m-0 text-[13.5px] text-ink-3">{ders.ogretim_uyesi} · {ders.kazanimlar.length} kazanım · {ders.soru_sayisi} soru</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex-1 h-2 rounded-full bg-line-soft overflow-hidden" aria-hidden>
            <div className="h-full bg-accent" style={{ width: `${(cozulen / tumu.length) * 100}%` }} />
          </div>
          <span className="shrink-0 text-[13px] text-ink-2 font-mono">{cozulen}/{tumu.length} · {dogru} doğru</span>
        </div>
        <div className="flex flex-wrap gap-2">
          <button type="button" onClick={() => setTam({ sorular: filtreli, baslik: ders.konu })}
            className="h-11 px-4 rounded-xl bg-ink text-white text-[14px] font-semibold inline-flex items-center gap-2 cursor-pointer">
            <Maximize2 className="w-4 h-4" /> Tam ekran çöz{zorluk ? ` (${zorluk})` : ''}
          </button>
          {yanlis.length > 0 && (
            <button type="button" onClick={() => setTam({ sorular: yanlis, baslik: `${ders.konu} · yanlışlarım` })}
              className="h-11 px-4 rounded-xl border border-line bg-white text-[14px] font-semibold text-ink inline-flex items-center gap-2 cursor-pointer hover:bg-canvas">
              <RotateCcw className="w-4 h-4" /> Yanlışlarımı çöz ({yanlis.length})
            </button>
          )}
          {cozulen > 0 && (
            <button type="button" onClick={() => tumu.forEach((q) => setCevap(q.id, null))}
              className="h-11 px-3 rounded-xl text-[13px] text-ink-3 cursor-pointer hover:bg-canvas">Sıfırla</button>
          )}
        </div>
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
        <label className="ml-auto">
          <span className="sr-only">Kazanıma git</span>
          <select onChange={(e) => { document.getElementById(`kz-${e.target.value}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' }); e.target.value = ''; }}
            defaultValue="" className="h-9 max-w-[220px] px-2 rounded-lg border border-line bg-white text-[13px] text-ink-2 cursor-pointer">
            <option value="" disabled>Kazanıma git…</option>
            {ders.kazanimlar.map((k) => <option key={k.no} value={k.no}>K{k.no} · {k.metin.slice(0, 60)}</option>)}
          </select>
        </label>
      </div>

      {ders.kazanimlar.map((k) => {
        const qs = k.sorular.filter((q) => !zorluk || q.zorluk === zorluk);
        const kc = k.sorular.filter((q) => cevaplar[q.id]).length;
        return (
          <section key={k.no} className="flex flex-col gap-3 scroll-mt-16" id={`kz-${k.no}`} aria-labelledby={`kzb-${k.no}`}>
            <div className="flex items-start gap-2.5 rounded-xl bg-accent-soft px-3.5 py-3">
              <Target className="w-4 h-4 mt-0.5 shrink-0 text-accent" />
              <div className="min-w-0 flex-1">
                <h3 id={`kzb-${k.no}`} className="m-0 text-[14.5px] font-semibold text-ink leading-snug">
                  <span className="font-mono text-accent mr-1.5">K{k.no}</span>{k.metin}
                </h3>
                <p className="m-0 mt-0.5 text-[12.5px] text-ink-3">{k.sorular.length} soru · {kc} çözüldü</p>
              </div>
              <button type="button" onClick={() => setTam({ sorular: qs, baslik: `K${k.no} · ${k.metin}` })} title="Bu kazanımı tam ekran çöz" aria-label="Bu kazanımı tam ekran çöz"
                className="shrink-0 h-8 w-8 rounded-lg inline-flex items-center justify-center text-accent hover:bg-white cursor-pointer"><Maximize2 className="w-4 h-4" /></button>
            </div>
            {qs.map((q) => { sayac += 1; return <SoruKarti key={q.id} q={q} n={sayac} ders={ders.ders} />; })}
            <CikmisListesi items={k.ilgili_cikmis} />
          </section>
        );
      })}
      {tam && tam.sorular.length > 0 && <TamEkran sorular={tam.sorular} ders={ders.ders} baslik={tam.baslik} onClose={() => setTam(null)} />}
    </div>
  );
}

export const KazanimSorulariView: React.FC = () => {
  const [secili, setSecili] = useState<string | null>(() => {
    const s = readSecim();
    return s && INDEX.some((x) => x.id === s) ? s : null;
  });
  const [brans, setBrans] = useState('');
  const [ara, setAra] = useState('');
  const cevaplar = useCevaplar();
  const branslar = useMemo(() => {
    const m = new Map<string, number>();
    INDEX.forEach((x) => m.set(x.ders, (m.get(x.ders) || 0) + 1));
    return Array.from(m.entries());
  }, []);
  const norm = (t: string) => t.toLocaleLowerCase('tr');
  const liste = INDEX.filter((x) => (!brans || x.ders === brans) && (!ara || norm(`${x.konu} ${x.ders} ${x.ogretim_uyesi}`).includes(norm(ara))));
  const toplamSoru = INDEX.reduce((a, x) => a + x.soru_sayisi, 0);
  const toplamCozulen = Object.keys(cevaplar).filter((k) => k.startsWith('k1-')).length;

  const sec = (id: string | null) => { setSecili(id); writeSecim(id); window.scrollTo({ top: 0 }); };

  if (secili) return <DersGorunumu id={secili} onBack={() => sec(null)} />;

  if (!INDEX.length) {
    return <p className="m-0 rounded-2xl border border-line bg-white p-6 text-center text-[14px] text-ink-3">Kurul 1 örnek soruları henüz hazırlanmadı.</p>;
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="grid grid-cols-3 gap-2">
        {[[INDEX.length, 'ders'], [toplamSoru, 'soru'], [toplamCozulen, 'çözdüğün']].map(([v, l]) => (
          <div key={l as string} className="rounded-xl border border-line bg-white px-3 py-2.5">
            <div className="text-[20px] font-bold text-ink font-mono leading-none">{v}</div>
            <div className="mt-1 text-[12px] text-ink-3">{l}</div>
          </div>
        ))}
      </div>
      <label className="relative block">
        <span className="sr-only">Ders ara</span>
        <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-ink-3" />
        <input value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Ders, konu veya öğretim üyesi ara…"
          className="w-full h-11 pl-9 pr-3 rounded-xl border border-line bg-white text-[14px] text-ink placeholder:text-ink-3 outline-none focus:border-accent" />
      </label>
      <div className="flex gap-1.5 overflow-x-auto pb-1 -mx-1 px-1" role="group" aria-label="Branş filtresi">
        {([['', INDEX.length], ...branslar] as [string, number][]).map(([b, c]) => (
          <button key={b || 'tum'} type="button" onClick={() => setBrans(b)} aria-pressed={brans === b}
            className={`shrink-0 h-9 px-3 rounded-lg text-[13px] font-medium cursor-pointer border inline-flex items-center gap-1.5 ${brans === b ? 'bg-ink text-white border-ink' : 'bg-white text-ink-2 border-line hover:bg-canvas'}`}>
            {b || 'Tümü'}<span className={`font-mono text-[11.5px] ${brans === b ? 'text-white/70' : 'text-ink-3'}`}>{c}</span>
          </button>
        ))}
      </div>
      {liste.length === 0 && <p className="m-0 py-8 text-center text-[14px] text-ink-3">Aramanla eşleşen ders yok.</p>}
      <ul className="m-0 p-0 list-none grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-2">
        {liste.map((x) => {
          const { n, d } = dersIlerleme(x.id, cevaplar);
          const yuzde = Math.min(100, Math.round((n / x.soru_sayisi) * 100));
          return (
            <li key={x.id}>
              <button type="button" onClick={() => sec(x.id)}
                className="group w-full h-full flex flex-col gap-2 p-3.5 rounded-xl border border-line bg-white text-left cursor-pointer hover:border-accent transition-colors">
                <span className="flex items-start gap-2.5">
                  <span className="shrink-0 w-8 h-8 rounded-lg bg-canvas flex items-center justify-center font-mono text-[12.5px] font-semibold text-ink-2 group-hover:bg-accent-soft group-hover:text-accent">{String(x.sira).padStart(2, '0')}</span>
                  <span className="min-w-0 flex-1">
                    <span className="block text-[15px] font-semibold text-ink leading-snug">{x.konu}</span>
                    <span className="block mt-0.5 text-[12.5px] text-ink-3 truncate">{x.ders} · {x.ogretim_uyesi}</span>
                  </span>
                  <ChevronRight className="shrink-0 w-4 h-4 mt-1 text-ink-3 group-hover:text-accent" />
                </span>
                <span className="flex items-center gap-2.5 pl-[42px]">
                  <span className="flex-1 h-1.5 rounded-full bg-line-soft overflow-hidden"><span className="block h-full bg-accent" style={{ width: `${yuzde}%` }} /></span>
                  <span className="shrink-0 text-[12px] text-ink-3 font-mono">{n ? `${n}/${x.soru_sayisi} · ${d} doğru` : `${x.soru_sayisi} soru · ${x.kazanim} kazanım`}</span>
                </span>
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export const KAZANIM_INDEX = INDEX;
export default KazanimSorulariView;
