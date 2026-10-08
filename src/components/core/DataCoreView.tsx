import { useCallback, useEffect, useState } from 'react';
import { safeJsonFetch } from '../../services/api';

/**
 * MedSoru Core v2 — Veri Merkezi (salt okunur).
 * CORE verisini (sorular, müfredat/kazanım, kaynak bağları, not araması, birleşik adaylar) siteye bağlar.
 * Tüm istekler `safeJsonFetch` ile gider; GPU/AI kullanılmaz.
 */
type V2Question = {
  question_id: string;
  stem: string;
  options?: Record<string, string>;
  acik_uclu?: boolean;
  answer?: string | null;
  aciklama?: string | null;
  aciklama_maddeleri?: string[];
  ders?: string | null;
  konu?: string | null;
  kazanim?: string | null;
  terimler?: string[];
  kaynak_baglari?: { source_id?: string; sayfa?: number; alinti?: string }[];
};
type V2Hit = { chunk_id: string; source_id?: string; page?: number; ders?: string; konu?: string; skor?: number; alinti?: string };

export default function DataCoreView() {
  const [stats, setStats] = useState<any>(null);
  const [audit, setAudit] = useState<any>(null);
  const [questions, setQuestions] = useState<V2Question[]>([]);
  const [query, setQuery] = useState('');
  const [onlyAnswered, setOnlyAnswered] = useState(false);
  const [onlyOpen, setOnlyOpen] = useState(false);
  const [noteQuery, setNoteQuery] = useState('');
  const [noteHits, setNoteHits] = useState<V2Hit[]>([]);
  const [similarStem, setSimilarStem] = useState('');
  const [similarHits, setSimilarHits] = useState<any[]>([]);
  const [mergeText, setMergeText] = useState('');
  const [mergeOut, setMergeOut] = useState<any[]>([]);
  const [clusters, setClusters] = useState<any[]>([]);
  const [revize, setRevize] = useState<any>(null);
  const [revChanges, setRevChanges] = useState<any[]>([]);
  const [revQuestions, setRevQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (search: string, answered: boolean, open: boolean) => {
    setLoading(true);
    setError(null);
    try {
      const s = (await safeJsonFetch('/api/v2/stats')).data;
      setStats(s);
      const params = new URLSearchParams({ limit: '50' });
      if (search) params.set('q', search);
      if (answered) params.set('answer', '1');
      if (open) params.set('acik_uclu', '1');
      const r = (await safeJsonFetch(`/api/v2/questions?${params.toString()}`)).data;
      setQuestions(r?.questions || []);
      const c = (await safeJsonFetch('/api/v2/cluster?limit=10')).data;
      setClusters(c?.ornekler || []);
      const a = (await safeJsonFetch('/api/v2/audit?summary=1')).data;
      setAudit(a);
      const rv = (await safeJsonFetch('/api/v2/revize')).data;
      setRevize(rv);
      const rc = (await safeJsonFetch('/api/v2/revize/changes?limit=8')).data;
      setRevChanges(rc?.degisiklikler || []);
      const rq = (await safeJsonFetch('/api/v2/revize/questions?limit=8&durum=revize')).data;
      setRevQuestions(rq?.sorular || []);
    } catch (e: any) {
      setError(e?.message || 'v2 verisi alınamadı');
    } finally {
      setLoading(false);
    }
  }, []);

  const searchNotes = useCallback(async (q: string) => {
    if (!q.trim()) { setNoteHits([]); return; }
    try {
      const r = (await safeJsonFetch(`/api/v2/search?q=${encodeURIComponent(q)}&limit=10`)).data;
      setNoteHits(r?.sonuc || []);
    } catch { setNoteHits([]); }
  }, []);

  const findSimilar = useCallback(async (s: string) => {
    if (!s.trim()) { setSimilarHits([]); return; }
    try {
      const r = (await safeJsonFetch(`/api/v2/similar?stem=${encodeURIComponent(s)}&limit=8`)).data;
      setSimilarHits(r?.sonuc || []);
    } catch { setSimilarHits([]); }
  }, []);

  const doMerge = useCallback(async (txt: string) => {
    const lines = txt.split('\n').map((s) => s.trim()).filter(Boolean);
    if (!lines.length) { setMergeOut([]); return; }
    try {
      const r = (await safeJsonFetch('/api/v2/merge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ parcalar: lines.map((stem) => ({ stem, options: {} })) }),
      })).data;
      setMergeOut(r?.birlesik || []);
    } catch { setMergeOut([]); }
  }, []);

  useEffect(() => { load('', false, false); }, [load]);

  return (
    <div className="mx-auto w-full max-w-5xl px-4 py-6">
      <h1 className="text-xl font-semibold mb-1">Veri Merkezi (Core v2)</h1>
      <p className="text-sm opacity-70 mb-4">
        Kaynaktan doğrulanmış sorular, müfredat/kazanım eşlemesi, ders notu bağlantıları ve toplu tamamlama. GPU/AI kullanılmaz.
      </p>

      {stats && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-5">
          {[
            ['Soru', stats.sorular], ['Cevaplı', stats.cevapli], ['Açık uçlu', stats.acik_uclu],
            ['Kazanımlı', stats.kazanimli], ['Kaynağa bağlı', stats.kaynak_bagli], ['Not dosyası', stats.notlar_dosya],
            ['Özet dosyası', stats.ozet_dosya], ['Vektör', stats.vektor?.sayi ?? 0],
          ].map(([label, value]) => (
            <div key={String(label)} className="rounded-lg border border-black/10 dark:border-white/15 p-3">
              <div className="text-xs opacity-60">{label}</div>
              <div className="text-lg font-semibold">{String(value ?? 0)}</div>
            </div>
          ))}
        </div>
      )}

      {/* Toplu tamamlama: parça yaz → benzer sorular */}
      <section className="mb-6 rounded-xl border border-black/10 dark:border-white/15 p-3">
        <div className="text-sm font-medium mb-1">Parça yaz → benzer soruları bul (birleştirme)</div>
        <p className="text-xs opacity-60 mb-2">Hatırladığın parçayı yaz; aynı soruya ait kayıtlar benzerlikle listelenir (AI yok, deterministik).</p>
        <div className="flex gap-2">
          <textarea
            value={similarStem}
            onChange={(e) => setSimilarStem(e.target.value)}
            placeholder="ör. parenteral uygulama toksik antifungal"
            rows={2}
            className="flex-1 rounded-lg border border-black/15 dark:border-white/20 bg-transparent px-3 py-2 text-sm"
          />
          <button onClick={() => findSimilar(similarStem)} className="rounded-lg bg-emerald-700 text-white px-3 py-2 text-sm">Bul</button>
        </div>
        <ul className="mt-2 space-y-2">
          {similarHits.map((h) => (
            <li key={h.question_id} className="text-xs rounded border border-black/10 dark:border-white/10 p-2">
              <div className="opacity-60">{h.ders || '—'} · benzerlik {h.benzerlik}{h.answer ? ` · cevap: ${h.answer}` : ''}</div>
              <div className="opacity-90">{h.stem}</div>
            </li>
          ))}
        </ul>
      </section>

      {/* Toplu tamamlama: çok parçayı birleştir */}
      <section className="mb-6 rounded-xl border border-black/10 dark:border-white/15 p-3">
        <div className="text-sm font-medium mb-1">Parçaları birleştir (toplu tamamlama)</div>
        <p className="text-xs opacity-60 mb-2">Her satıra bir parça yaz; aynı soruya ait olanlar birleşip tam soru adayı üretir (AI yok).</p>
        <textarea
          value={mergeText}
          onChange={(e) => setMergeText(e.target.value)}
          placeholder={"parenteral toksik antifungal hangisidir\nsadece topikal kullanılan antifungal"}
          rows={3}
          className="w-full rounded-lg border border-black/15 dark:border-white/20 bg-transparent px-3 py-2 text-sm"
        />
        <button onClick={() => doMerge(mergeText)} className="mt-2 rounded-lg bg-violet-700 text-white px-3 py-2 text-sm">Birleştir</button>
        <ul className="mt-2 space-y-2">
          {mergeOut.map((m, i) => (
            <li key={i} className="text-xs rounded border border-black/10 dark:border-white/10 p-2">
              <div className="font-medium">{m.stem}</div>
              <div className="opacity-60">{m.ders || '—'} · {m.birlesik_parca_sayisi ?? 1} parça{m.answer ? ` · cevap: ${m.answer}` : ''}</div>
            </li>
          ))}
        </ul>
      </section>

      {/* Ders notu araması */}
      <section className="mb-6 rounded-xl border border-black/10 dark:border-white/15 p-3">
        <div className="text-sm font-medium mb-2">Ders notu ara (v2 · anlamsal + BM25)</div>
        <div className="flex gap-2">
          <input
            value={noteQuery}
            onChange={(e) => setNoteQuery(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') searchNotes(noteQuery); }}
            placeholder="ör. antifungal nistatin"
            className="flex-1 rounded-lg border border-black/15 dark:border-white/20 bg-transparent px-3 py-2 text-sm"
          />
          <button onClick={() => searchNotes(noteQuery)} className="rounded-lg bg-slate-700 text-white px-3 py-2 text-sm">Ara</button>
        </div>
        <ul className="mt-2 space-y-2">
          {noteHits.map((h) => (
            <li key={h.chunk_id} className="text-xs rounded border border-black/10 dark:border-white/10 p-2">
              <div className="opacity-70">{h.ders || '—'} · {h.source_id} · s.{h.page ?? '?'} · skor {h.skor}</div>
              <div className="opacity-90">{h.alinti}</div>
            </li>
          ))}
        </ul>
      </section>

      {audit?.toplam && (
        <div className="text-xs opacity-70 mb-4">
          Eski veri denetimi ({audit.zaman}): {audit.toplam.kayit} kayıt · engelleyici {audit.toplam.blocking} · inceleme {audit.toplam.review}
        </div>
      )}

      {revize?.toplam != null && (
        <section className="mb-6 rounded-xl border border-black/10 dark:border-white/15 p-3">
          <div className="text-sm font-medium mb-1">Revize v2 — eski → yeni düzeltmeler</div>
          <div className="text-xs opacity-70 mb-2">
            {revize.toplam} kayıt · {revize.revize_edilen} revize · {revize.karantina} karantina · değişiklik kaydı {revize.degisiklik_kaydi}
          </div>
          <ul className="space-y-2">
            {revChanges.map((c: any, i: number) => (
              <li key={i} className="text-xs rounded border border-black/10 dark:border-white/10 p-2">
                <div className="opacity-60 mb-1">{c.id} · {c.model}</div>
                {(c.degisiklikler || []).map((d: any, j: number) => (
                  <div key={j} className="mb-2 whitespace-pre-wrap break-words">
                    <span className="font-medium">{d.alan}</span>:&nbsp;
                    <span className="line-through opacity-60">{String(d.eski ?? '')}</span>
                    &nbsp;→&nbsp;
                    <span className="text-emerald-700 dark:text-emerald-400">{String(d.yeni ?? '')}</span>
                  </div>
                ))}
              </li>
            ))}
          </ul>
        </section>
      )}

      {revQuestions.length > 0 && (
        <section className="mb-6 rounded-xl border border-black/10 dark:border-white/15 p-3">
          <div className="text-sm font-medium mb-2">Revize v2 — sorular (tam)</div>
          <ul className="space-y-3">
            {revQuestions.map((r: any, i: number) => (
              <li key={i} className="rounded-xl border border-black/10 dark:border-white/10 p-3">
                <div className="text-sm font-medium mb-1 whitespace-pre-wrap break-words">{r.soru_koku}</div>
                <div className="text-xs opacity-80 grid gap-0.5 mb-1">
                  {Object.entries(r.secenekler || {}).map(([k, v]) => <div key={k} className="break-words">{k}) {String(v)}</div>)}
                </div>
                <div className="text-[11px] mb-1">
                  <span className="rounded bg-indigo-100 text-indigo-800 px-1.5 py-0.5 mr-1">Doğru: {r.dogru_secenek || '—'}</span>
                  {r.ders_adi && <span className="rounded bg-sky-100 text-sky-800 px-1.5 py-0.5 mr-1">{r.ders_adi}</span>}
                  {r.konu_adi && <span className="rounded bg-emerald-100 text-emerald-800 px-1.5 py-0.5">{r.konu_adi}</span>}
                </div>
                {((r.aciklama_maddeleri || []).length > 0) ? (
                  <ul className="text-xs opacity-90 list-disc pl-4 space-y-0.5">
                    {(r.aciklama_maddeleri as string[]).map((m, j) => <li key={j} className="break-words">{m}</li>)}
                  </ul>
                ) : r.aciklama ? (
                  <div className="text-xs opacity-80 whitespace-pre-wrap break-words">{r.aciklama}</div>
                ) : null}
                <div className="text-[11px] opacity-50 mt-1">model: {r.model} · kategori: {r.kategori} · destek: {r.support_ratio}</div>
              </li>
            ))}
          </ul>
        </section>
      )}

      <div className="flex flex-wrap gap-2 items-center mb-4">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') load(query, onlyAnswered, onlyOpen); }}
          placeholder="Sorularda ara…"
          className="flex-1 min-w-[200px] rounded-lg border border-black/15 dark:border-white/20 bg-transparent px-3 py-2 text-sm"
        />
        <label className="text-sm flex items-center gap-1">
          <input type="checkbox" checked={onlyAnswered} onChange={(e) => setOnlyAnswered(e.target.checked)} /> Cevaplı
        </label>
        <label className="text-sm flex items-center gap-1">
          <input type="checkbox" checked={onlyOpen} onChange={(e) => setOnlyOpen(e.target.checked)} /> Açık uçlu
        </label>
        <button onClick={() => load(query, onlyAnswered, onlyOpen)} className="rounded-lg bg-indigo-600 text-white px-3 py-2 text-sm">Ara</button>
      </div>

      {loading && <div className="opacity-70 text-sm">Yükleniyor…</div>}
      {error && <div className="text-red-600 text-sm">{error}</div>}

      <ul className="space-y-3">
        {questions.map((qq) => (
          <li key={qq.question_id} className="rounded-xl border border-black/10 dark:border-white/15 p-3">
            <div className="text-sm font-medium mb-1">{qq.stem}</div>
            <div className="flex flex-wrap gap-1 text-[11px] mb-1">
              {qq.ders && <span className="rounded bg-sky-100 text-sky-800 px-1.5 py-0.5">{qq.ders}</span>}
              {qq.konu && <span className="rounded bg-emerald-100 text-emerald-800 px-1.5 py-0.5">{qq.konu}</span>}
              {qq.acik_uclu && <span className="rounded bg-amber-100 text-amber-800 px-1.5 py-0.5">açık uçlu</span>}
              {qq.answer && <span className="rounded bg-indigo-100 text-indigo-800 px-1.5 py-0.5">cevap: {qq.answer}</span>}
            </div>
            {qq.kazanim && <div className="text-xs opacity-70 mb-1">Kazanım: {qq.kazanim}</div>}
            {!qq.acik_uclu && qq.options && (
              <div className="text-xs opacity-80 grid gap-0.5">
                {Object.entries(qq.options).map(([k, v]) => <div key={k}>{k}) {v}</div>)}
              </div>
            )}
            {(qq.terimler || []).length > 0 && (
              <div className="text-[11px] opacity-60 mt-1">Terimler: {qq.terimler!.slice(0, 8).join(', ')}</div>
            )}
            {((qq as any).aciklama_maddeleri || []).length > 0 ? (
              <ul className="text-xs opacity-90 mt-2 list-disc pl-4 space-y-0.5">
                {((qq as any).aciklama_maddeleri as string[]).map((m, mi) => <li key={mi} className="break-words">{m}</li>)}
              </ul>
            ) : (qq as any).aciklama ? (
              <div className="text-xs opacity-80 mt-2 whitespace-pre-wrap break-words">{(qq as any).aciklama}</div>
            ) : null}
            {(qq.kaynak_baglari || []).length > 0 && (
              <div className="text-[11px] opacity-60 mt-1">
                Kaynak: {qq.kaynak_baglari![0].source_id} · s.{qq.kaynak_baglari![0].sayfa ?? '?'}
              </div>
            )}
          </li>
        ))}
      </ul>
      {!loading && questions.length === 0 && !error && <div className="opacity-60 text-sm">Sonuç yok.</div>}

      {clusters.length > 0 && (
        <section className="mt-6">
          <h2 className="text-sm font-semibold mb-2">Toplu tamamlama — birleşik soru adayları</h2>
          <ul className="space-y-2">
            {clusters.map((c, i) => {
              const m = c.birlesik || c;
              return (
                <li key={i} className="text-xs rounded border border-black/10 dark:border-white/15 p-2">
                  <div className="font-medium mb-0.5">{String(m.stem || '').slice(0, 140)}</div>
                  <div className="opacity-60">
                    {m.ders || '—'} · {m.birlesik_parca_sayisi ?? 1} parça birleşti
                    {m.answer ? ` · cevap: ${m.answer}` : ''}
                  </div>
                </li>
              );
            })}
          </ul>
        </section>
      )}
    </div>
  );
}
