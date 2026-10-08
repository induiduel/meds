import { useCallback, useEffect, useState } from 'react';
import { safeJsonFetch } from '../../services/api';
import { PageHeader } from '../ui/PageHeader';

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
    <div className="w-full min-w-0 flex flex-col gap-4 pb-12">
      <PageHeader
        title="Veri merkezi"
        description="Kaynaktan doğrulanmış sorular, müfredat/kazanım eşlemesi, ders notu bağlantıları ve toplu tamamlama. GPU/AI kullanılmaz."
        stats={stats ? ([
          ['Soru', stats.sorular], ['Cevaplı', stats.cevapli], ['Açık uçlu', stats.acik_uclu],
          ['Kazanımlı', stats.kazanimli], ['Kaynağa bağlı', stats.kaynak_bagli], ['Not dosyası', stats.notlar_dosya],
          ['Özet dosyası', stats.ozet_dosya], ['Vektör', stats.vektor?.sayi ?? 0],
        ] as const).map(([label, value]) => ({ label, value: Number(value ?? 0).toLocaleString('tr-TR') })) : undefined}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 2xl:grid-cols-3 gap-4 items-start">
      {/* Toplu tamamlama: parça yaz → benzer sorular */}
      <section className="ms-panel ms-panel-body">
        <h2 className="ms-panel-title">Parça yaz → benzer soruları bul (birleştirme)</h2>
        <p className="m-0 text-[12.5px] leading-normal text-ink-3">Hatırladığın parçayı yaz; aynı soruya ait kayıtlar benzerlikle listelenir (AI yok, deterministik).</p>
        <div className="flex gap-2">
          <textarea
            value={similarStem}
            onChange={(e) => setSimilarStem(e.target.value)}
            placeholder="ör. parenteral uygulama toksik antifungal"
            rows={2}
            className="flex-1 ms-input h-auto! py-2.5 resize-y"
          />
          <button onClick={() => findSimilar(similarStem)} className="ms-btn is-primary shrink-0">Bul</button>
        </div>
        <ul className="m-0 p-0 list-none flex flex-col gap-2 empty:hidden">
          {similarHits.map((h) => (
            <li key={h.question_id} className="text-[12.5px] leading-normal rounded-xl bg-canvas px-3 py-2.5 text-ink-2">
              <div className="opacity-60">{h.ders || '—'} · benzerlik {h.benzerlik}{h.answer ? ` · cevap: ${h.answer}` : ''}</div>
              <div className="opacity-90">{h.stem}</div>
            </li>
          ))}
        </ul>
      </section>

      {/* Toplu tamamlama: çok parçayı birleştir */}
      <section className="ms-panel ms-panel-body">
        <h2 className="ms-panel-title">Parçaları birleştir (toplu tamamlama)</h2>
        <p className="m-0 text-[12.5px] leading-normal text-ink-3">Her satıra bir parça yaz; aynı soruya ait olanlar birleşip tam soru adayı üretir (AI yok).</p>
        <textarea
          value={mergeText}
          onChange={(e) => setMergeText(e.target.value)}
          placeholder={"parenteral toksik antifungal hangisidir\nsadece topikal kullanılan antifungal"}
          rows={3}
          className="ms-input h-auto! py-2.5 resize-y"
        />
        <button onClick={() => doMerge(mergeText)} className="ms-btn is-primary self-start">Birleştir</button>
        <ul className="m-0 p-0 list-none flex flex-col gap-2 empty:hidden">
          {mergeOut.map((m, i) => (
            <li key={i} className="text-[12.5px] leading-normal rounded-xl bg-canvas px-3 py-2.5 text-ink-2">
              <div className="font-medium">{m.stem}</div>
              <div className="opacity-60">{m.ders || '—'} · {m.birlesik_parca_sayisi ?? 1} parça{m.answer ? ` · cevap: ${m.answer}` : ''}</div>
            </li>
          ))}
        </ul>
      </section>

      {/* Ders notu araması */}
      <section className="ms-panel ms-panel-body">
        <h2 className="ms-panel-title">Ders notu ara (v2 · anlamsal + BM25)</h2>
        <div className="flex gap-2">
          <input
            value={noteQuery}
            onChange={(e) => setNoteQuery(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') searchNotes(noteQuery); }}
            placeholder="ör. antifungal nistatin"
            className="flex-1 ms-input"
          />
          <button onClick={() => searchNotes(noteQuery)} className="ms-btn is-primary shrink-0">Ara</button>
        </div>
        <ul className="m-0 p-0 list-none flex flex-col gap-2 empty:hidden">
          {noteHits.map((h) => (
            <li key={h.chunk_id} className="text-[12.5px] leading-normal rounded-xl bg-canvas px-3 py-2.5 text-ink-2">
              <div className="opacity-70">{h.ders || '—'} · {h.source_id} · s.{h.page ?? '?'} · skor {h.skor}</div>
              <div className="opacity-90">{h.alinti}</div>
            </li>
          ))}
        </ul>
      </section>

      </div>

      {audit?.toplam && (
        <div className="text-[12.5px] text-ink-3">
          Eski veri denetimi ({audit.zaman}): {audit.toplam.kayit} kayıt · engelleyici {audit.toplam.blocking} · inceleme {audit.toplam.review}
        </div>
      )}

      {revize?.toplam != null && (
        <section className="ms-panel ms-panel-body">
          <h2 className="ms-panel-title">Revize v2 — eski → yeni düzeltmeler</h2>
          <div className="text-xs opacity-70 mb-2">
            {revize.toplam} kayıt · {revize.revize_edilen} revize · {revize.karantina} karantina · değişiklik kaydı {revize.degisiklik_kaydi}
          </div>
          <ul className="m-0 p-0 list-none flex flex-col gap-2">
            {revChanges.map((c: any, i: number) => (
              <li key={i} className="text-[12.5px] leading-normal rounded-xl bg-canvas px-3 py-2.5 text-ink-2">
                <div className="opacity-60 mb-1">{c.id} · {c.model}</div>
                {(c.degisiklikler || []).map((d: any, j: number) => (
                  <div key={j} className="mb-2 whitespace-pre-wrap break-words">
                    <span className="font-medium">{d.alan}</span>:&nbsp;
                    <span className="line-through opacity-60">{String(d.eski ?? '')}</span>
                    &nbsp;→&nbsp;
                    <span className="text-ok">{String(d.yeni ?? '')}</span>
                  </div>
                ))}
              </li>
            ))}
          </ul>
        </section>
      )}

      {revQuestions.length > 0 && (
        <section className="ms-panel ms-panel-body">
          <h2 className="ms-panel-title">Revize v2 — sorular (tam)</h2>
          <ul className="m-0 p-0 list-none flex flex-col gap-3">
            {revQuestions.map((r: any, i: number) => (
              <li key={i} className="ms-panel p-4 flex flex-col gap-1.5">
                <div className="m-0 text-[14.5px] font-medium text-ink leading-snug whitespace-pre-wrap break-words">{r.soru_koku}</div>
                <div className="text-xs opacity-80 grid gap-0.5 mb-1">
                  {Object.entries(r.secenekler || {}).map(([k, v]) => <div key={k} className="break-words">{k}) {String(v)}</div>)}
                </div>
                <div className="text-[11px] mb-1">
                  <span className="rounded-full h-6 px-2 inline-flex items-center text-[12px] font-medium bg-accent-soft text-accent mr-1">Doğru: {r.dogru_secenek || '—'}</span>
                  {r.ders_adi && <span className="rounded-full h-6 px-2 inline-flex items-center text-[12px] font-medium bg-field text-ink-2 mr-1">{r.ders_adi}</span>}
                  {r.konu_adi && <span className="rounded-full h-6 px-2 inline-flex items-center text-[12px] font-medium bg-field text-ink-2">{r.konu_adi}</span>}
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

      <div className="ms-panel p-3 flex flex-wrap gap-2 items-center">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') load(query, onlyAnswered, onlyOpen); }}
          placeholder="Sorularda ara…"
          className="flex-1 min-w-[200px] ms-input"
        />
        <label className="text-[14px] text-ink-2 flex items-center gap-1.5 px-1 cursor-pointer">
          <input type="checkbox" checked={onlyAnswered} onChange={(e) => setOnlyAnswered(e.target.checked)} /> Cevaplı
        </label>
        <label className="text-[14px] text-ink-2 flex items-center gap-1.5 px-1 cursor-pointer">
          <input type="checkbox" checked={onlyOpen} onChange={(e) => setOnlyOpen(e.target.checked)} /> Açık uçlu
        </label>
        <button onClick={() => load(query, onlyAnswered, onlyOpen)} className="ms-btn is-primary shrink-0">Ara</button>
      </div>

      {loading && <div className="opacity-70 text-sm">Yükleniyor…</div>}
      {error && <div className="text-bad-text text-sm">{error}</div>}

      <ul className="m-0 p-0 list-none grid grid-cols-1 xl:grid-cols-2 gap-3 items-start">
        {questions.map((qq) => (
          <li key={qq.question_id} className="ms-panel p-4 flex flex-col gap-1.5">
            <p className="m-0 text-[14.5px] font-medium text-ink leading-snug">{qq.stem}</p>
            <div className="flex flex-wrap gap-1 text-[11px] mb-1">
              {qq.ders && <span className="rounded-full h-6 px-2 inline-flex items-center text-[12px] font-medium bg-field text-ink-2">{qq.ders}</span>}
              {qq.konu && <span className="rounded-full h-6 px-2 inline-flex items-center text-[12px] font-medium bg-field text-ink-2">{qq.konu}</span>}
              {qq.acik_uclu && <span className="rounded-full h-6 px-2 inline-flex items-center text-[12px] font-medium bg-warn-soft text-warn">açık uçlu</span>}
              {qq.answer && <span className="rounded-full h-6 px-2 inline-flex items-center text-[12px] font-medium bg-accent-soft text-accent">cevap: {qq.answer}</span>}
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
        <section className="flex flex-col gap-2">
          <h2 className="ms-panel-title">Toplu tamamlama — birleşik soru adayları</h2>
          <ul className="m-0 p-0 list-none flex flex-col gap-2">
            {clusters.map((c, i) => {
              const m = c.birlesik || c;
              return (
                <li key={i} className="text-[12.5px] leading-normal rounded-xl bg-canvas px-3 py-2.5 text-ink-2">
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
