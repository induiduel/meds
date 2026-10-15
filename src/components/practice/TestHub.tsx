/**
 * /test — Test çöz: önce "Test oluştur" kurulumu, sonra mevcut çözücü (PracticeMode; v10/v11/v12 görünümleri).
 * Kaynaklar: çıkmış, örnek soru, Öğren mini soru / klinik karar / tuzak avı / boşluk doldurma (services/testBank.ts).
 * Kullanıcı kaynak, kurul, ders, zorluk ve soru sayısını seçebilir; hiçbir şey seçmezse ya da "Rastgele"ye
 * basarsa bütün kaynaklardan rastgele kurulur. Soru havuzundaki kullanıcı soruları bu ekranda listelenmez.
 * Sınıf öneki `tb-` (styles/test-builder.css); v12 kuralları :root[data-design='v12'] altında.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, Shuffle, Play, Archive, Target, HelpCircle, Stethoscope, SearchX, TextCursorInput, Check, RotateCcw } from 'lucide-react';
import type { QuestionItem } from '../../types';
import { PracticeMode } from '../PracticeMode';
import { toast } from '../ui/Toast';
import {
  buildTest, loadArchiveTests, disciplineOptions, catalogCounts, randomCriteria, DEFAULT_CRITERIA, SOURCE_INFO, SOURCE_ORDER, KURUL1,
  difficultyActive, type TestCriteria, type TestQuestion, type TestSource, type Difficulty,
} from '../../services/testBank';
import { COMMITTEE_NAME } from '../pdf/pdfSources';
import '../../styles/test-builder.css';

interface TestHubProps {
  onExit?: () => void;
}

const KEY = 'medsoru_test_kriter_v1';
const COUNTS = [10, 20, 40, 60, 100];
const LEVELS: [Difficulty, string][] = [['kolay', 'Kolay'], ['orta', 'Orta'], ['zor', 'Zor']];
const ICONS: Record<TestSource, React.ElementType> = { cikmis: Archive, ornek: Target, mini: HelpCircle, vaka: Stethoscope, tuzak: SearchX, bosluk: TextCursorInput };
const fmt = (n: number) => n.toLocaleString('tr-TR');

const readSaved = (): TestCriteria => {
  try {
    const raw = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (!raw || typeof raw !== 'object') return { ...DEFAULT_CRITERIA };
    return {
      sources: Array.isArray(raw.sources) ? raw.sources.filter((x: any) => SOURCE_ORDER.includes(x)) : [...SOURCE_ORDER],
      committeeId: typeof raw.committeeId === 'string' ? raw.committeeId : 'all',
      disciplines: Array.isArray(raw.disciplines) ? raw.disciplines.filter((x: any) => typeof x === 'string') : [],
      difficulties: Array.isArray(raw.difficulties) ? raw.difficulties.filter((x: any) => ['kolay', 'orta', 'zor'].includes(x)) : [],
      count: COUNTS.includes(raw.count) ? raw.count : 20,
    };
  } catch {
    return { ...DEFAULT_CRITERIA };
  }
};

/** Çözücü QuestionItem + reconstruction bekler; test sorusu bu kalıba çevrilir. */
const toItem = (q: TestQuestion, i: number): QuestionItem =>
  ({
    id: q.id,
    committeeId: q.committeeId,
    questionNumber: i + 1,
    discipline: q.discipline,
    topic: q.topic,
    status: 'completed',
    fragments: [],
    options: [],
    tags: [],
    examYear: q.year,
    reconstruction: {
      stem: q.stem,
      options: q.options.map((o) => ({ key: o.key as any, text: o.text, isCorrect: o.key === q.answer })),
      correctAnswer: q.answer as any,
      explanation: q.explanation,
      confidenceScore: 1,
    },
  }) as unknown as QuestionItem;

export const TestHub: React.FC<TestHubProps> = ({ onExit }) => {
  const [c, setC] = useState<TestCriteria>(readSaved);
  const [archive, setArchive] = useState<TestQuestion[] | null>(null);
  const [archiveErr, setArchiveErr] = useState(false);
  const [busy, setBusy] = useState<string | null>(null);
  const [run, setRun] = useState<{ items: QuestionItem[]; title: string; subtitle: string; nonce: number } | null>(null);

  const patch = (p: Partial<TestCriteria>) => setC((prev) => ({ ...prev, ...p }));
  useEffect(() => {
    try {
      localStorage.setItem(KEY, JSON.stringify(c));
    } catch {}
  }, [c]);

  useEffect(() => {
    let alive = true;
    loadArchiveTests()
      .then((a) => alive && setArchive(a))
      .catch(() => alive && setArchiveErr(true));
    return () => {
      alive = false;
    };
  }, []);

  const committees = useMemo(() => {
    const m = new Map<string, number>();
    const srcs = c.sources.length ? c.sources : SOURCE_ORDER;
    (archive || []).forEach((q) => q.committeeId && m.set(q.committeeId, (m.get(q.committeeId) || 0) + (srcs.includes('cikmis') ? 1 : 0)));
    // Kurul 1: seçili kaynaklara göre örnek + Öğren ögeleri de sayılır
    const k1 = catalogCounts({ committeeId: KURUL1, disciplines: [] });
    m.set(KURUL1, (m.get(KURUL1) || 0) + srcs.reduce((n, src) => n + (src === 'cikmis' ? 0 : src === 'ornek' ? k1.ornekQuestions : k1[src]), 0));
    const order = Object.keys(COMMITTEE_NAME);
    const rank = (id: string) => (order.indexOf(id) < 0 ? 99 : order.indexOf(id));
    return [...m.entries()].sort((a, b) => rank(a[0]) - rank(b[0]) || a[0].localeCompare(b[0], 'tr', { numeric: true }));
  }, [archive, c.sources]);
  const discOpts = useMemo(() => disciplineOptions(archive || [], c.committeeId, c.sources), [archive, c.committeeId, c.sources]);
  // Kurul değişince listede olmayan ders seçimleri düşer (kaynak değişimi seçimi silmez; ders 0 ile görünür kalır)
  const discList = useMemo(() => {
    const seen = new Set(discOpts.map(([d]) => d));
    return [...discOpts, ...c.disciplines.filter((d) => !seen.has(d)).map((d) => [d, 0] as [string, number])];
  }, [discOpts, c.disciplines]);
  useEffect(() => {
    if (!archive) return;
    const ok = new Set(disciplineOptions(archive, c.committeeId).map(([d]) => d));
    setC((prev) => (prev.disciplines.every((d) => ok.has(d)) ? prev : { ...prev, disciplines: prev.disciplines.filter((d) => ok.has(d)) }));
  }, [archive, c.committeeId]);

  const k1Open = c.committeeId === 'all' || c.committeeId === KURUL1;
  const cat = useMemo(() => catalogCounts(c), [c]);
  const archiveCount = useMemo(
    () => (archive || []).filter((q) => (c.committeeId === 'all' || q.committeeId === c.committeeId) && (!c.disciplines.length || c.disciplines.includes(q.discipline))).length,
    [archive, c.committeeId, c.disciplines]
  );
  const sourceCount = (src: TestSource): string => {
    if (src === 'cikmis') return archive ? fmt(archiveCount) : '…';
    if (!k1Open) return '—';
    if (src === 'ornek') return fmt(cat.ornekQuestions);
    return fmt(cat[src]);
  };
  const activeSources = c.sources.filter((src) => !SOURCE_INFO[src].kurul1Only || k1Open);
  const byLevel = difficultyActive(c);
  const available = byLevel ? cat.ornekQuestions : (activeSources.length ? activeSources : SOURCE_ORDER.filter((src) => !SOURCE_INFO[src].kurul1Only || k1Open)).reduce(
    (n, src) => n + (src === 'cikmis' ? archiveCount : src === 'ornek' ? cat.ornekQuestions : cat[src]),
    0
  );

  const start = async (crit: TestCriteria, label: string) => {
    if (busy) return;
    setBusy('Sorular hazırlanıyor…');
    try {
      const qs = await buildTest(crit, (m) => setBusy(m));
      if (!qs.length) {
        toast.error('Bu seçimde soru bulunamadı', 'Kaynak ya da ders seçimini genişlet.');
        return;
      }
      if (qs.length < crit.count) toast.info(`Bu seçimde ${qs.length} soru bulundu`, 'Test bu kadar soruyla kuruldu.');
      const used = SOURCE_ORDER.filter((src) => qs.some((q) => q.source === src)).map((src) => SOURCE_INFO[src].label);
      setRun({ items: qs.map(toItem), title: `${label} · ${qs.length} soru`, subtitle: used.join(' · '), nonce: Date.now() });
      window.scrollTo({ top: 0 });
    } catch (e: any) {
      toast.error('Test kurulamadı', e?.message || 'Bağlantını kontrol edip tekrar dene.');
    } finally {
      setBusy(null);
    }
  };

  if (run) {
    return (
      <PracticeMode
        key={run.nonce}
        questions={run.items}
        title={run.title}
        subtitle={run.subtitle}
        onExit={() => setRun(null)}
        onOpenContributeModal={() => setRun(null)}
      />
    );
  }

  const customized =
    c.sources.length !== SOURCE_ORDER.length || c.committeeId !== 'all' || c.disciplines.length > 0 || c.difficulties.length > 0;
  const toggle = <T,>(list: T[], v: T) => (list.includes(v) ? list.filter((x) => x !== v) : [...list, v]);

  return (
    <div className="tb" aria-busy={!!busy}>
      <header className="tb-head">
        {onExit && (
          <button type="button" className="tb-ib" onClick={onExit} aria-label="Çalış'a dön">
            <ArrowLeft aria-hidden />
          </button>
        )}
        <div className="tb-head-t">
          <h1>Test çöz</h1>
          <p>Çıkmış, örnek ve Öğren sorularından test kur. Bir şey seçmezsen sorular rastgele gelir.</p>
        </div>
        <button type="button" className="tb-btn" onClick={() => start(randomCriteria(), 'Rastgele test')} disabled={!!busy}>
          <Shuffle aria-hidden /> Rastgele 20 soru
        </button>
      </header>

      <section className="tb-panel" aria-labelledby="tb-src-h">
        <div className="tb-sec">
          <div className="tb-sec-h">
            <h2 id="tb-src-h">Kaynaklar</h2>
            <span>{activeSources.length ? `${activeSources.length} seçili` : 'hiçbiri seçili değil → hepsi'}</span>
          </div>
          <div className="tb-srcs">
            {SOURCE_ORDER.map((src) => {
              const info = SOURCE_INFO[src];
              const Icon = ICONS[src];
              const locked = info.kurul1Only && !k1Open;
              const on = c.sources.includes(src) && !locked;
              return (
                <button
                  key={src}
                  type="button"
                  role="checkbox"
                  aria-checked={on}
                  disabled={locked}
                  className={`tb-src ${on ? 'is-on' : ''}`}
                  onClick={() => patch({ sources: toggle(c.sources, src) })}
                >
                  <span className="tb-src-ic"><Icon aria-hidden /></span>
                  <span className="tb-src-t">
                    <b>{info.label}</b>
                    <small>{locked ? 'Yalnız Kurul 1' : info.hint}</small>
                  </span>
                  <span className="tb-src-n">{sourceCount(src)}</span>
                  <span className="tb-check" aria-hidden>{on && <Check />}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="tb-sec">
          <div className="tb-sec-h">
            <h2>Kurul</h2>
          </div>
          <div className="tb-chips" role="radiogroup" aria-label="Kurul">
            <button type="button" role="radio" aria-checked={c.committeeId === 'all'} className={`tb-chip ${c.committeeId === 'all' ? 'is-on' : ''}`} onClick={() => patch({ committeeId: 'all' })}>
              Tümü
            </button>
            {committees.map(([id, n]) => (
              <button key={id} type="button" role="radio" aria-checked={c.committeeId === id} className={`tb-chip ${c.committeeId === id ? 'is-on' : ''}`} onClick={() => patch({ committeeId: id })} title={COMMITTEE_NAME[id] || id}>
                {(COMMITTEE_NAME[id] || id).split(' · ')[0]}
                {n > 0 && <small>{fmt(n)}</small>}
              </button>
            ))}
          </div>
          {!k1Open && <p className="tb-hint">Örnek sorular ve Öğren ögeleri şimdilik yalnız Kurul 1'de; bu kurulda yalnız çıkmış sorular kullanılır.</p>}
        </div>

        <div className="tb-sec">
          <div className="tb-sec-h">
            <h2>Dersler</h2>
            <span>{c.disciplines.length ? `${c.disciplines.length} seçili` : 'hepsi'}</span>
            {c.disciplines.length > 0 && (
              <button type="button" className="tb-link" onClick={() => patch({ disciplines: [] })}>
                Temizle
              </button>
            )}
          </div>
          <div className="tb-chips is-scroll">
            {!archive && !archiveErr && <span className="tb-hint">Dersler yükleniyor…</span>}
            {discList.map(([d, n]) => {
              const on = c.disciplines.includes(d);
              return (
                <button key={d} type="button" aria-pressed={on} className={`tb-chip ${on ? 'is-on' : ''}`} onClick={() => patch({ disciplines: toggle(c.disciplines, d) })}>
                  {d} <small>{fmt(n)}</small>
                </button>
              );
            })}
          </div>
          {archiveErr && <p className="tb-hint is-warn">Çıkmış sorular yüklenemedi; test yalnız örnek ve Öğren sorularından kurulur.</p>}
        </div>

        <div className="tb-row">
          <div className="tb-sec">
            <div className="tb-sec-h">
              <h2>Soru sayısı</h2>
            </div>
            <div className="tb-seg" role="radiogroup" aria-label="Soru sayısı">
              {COUNTS.map((n) => (
                <button key={n} type="button" role="radio" aria-checked={c.count === n} className={c.count === n ? 'is-on' : ''} onClick={() => patch({ count: n })}>
                  {n}
                </button>
              ))}
            </div>
          </div>
          {c.sources.includes('ornek') && k1Open && (
            <div className="tb-sec">
              <div className="tb-sec-h">
                <h2>Zorluk</h2>
                <span>{byLevel ? 'test yalnız örnek sorulardan kurulur' : 'örnek sorular'}</span>
              </div>
              <div className="tb-seg" role="group" aria-label="Zorluk">
                {LEVELS.map(([v, l]) => {
                  const on = c.difficulties.includes(v);
                  return (
                    <button key={v} type="button" aria-pressed={on} className={on ? 'is-on' : ''} onClick={() => patch({ difficulties: toggle(c.difficulties, v) })}>
                      {l}
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        <footer className="tb-foot">
          <p className="tb-sum" role="status">
            <b>{busy || `${c.count} soru`}</b>
            {!busy && <span>{archive ? `${fmt(available)} uygun soru` : 'uygun sorular sayılıyor…'}</span>}
            {!busy && (
              <span>
                {[
                  activeSources.length === 0 || activeSources.length === SOURCE_ORDER.length ? 'tüm kaynaklar' : activeSources.map((x) => SOURCE_INFO[x].label).join(', '),
                  c.committeeId === 'all' ? 'tüm kurullar' : (COMMITTEE_NAME[c.committeeId] || c.committeeId).split(' · ')[0],
                  c.disciplines.length ? `${c.disciplines.length} ders` : 'tüm dersler',
                ].join(' · ')}
              </span>
            )}
          </p>
          {customized && (
            <button type="button" className="tb-btn is-ghost" onClick={() => setC({ ...DEFAULT_CRITERIA, count: c.count })} disabled={!!busy}>
              <RotateCcw aria-hidden /> Sıfırla
            </button>
          )}
          <button
            type="button"
            className="tb-btn is-primary"
            onClick={() => start({ ...c, sources: activeSources.length ? activeSources : [...SOURCE_ORDER] }, customized ? 'Test' : 'Rastgele test')}
            disabled={!!busy}
          >
            <Play aria-hidden /> {busy ? 'Hazırlanıyor…' : 'Testi oluştur'}
          </button>
        </footer>
        <p className="tb-note">Soru havuzuna kullanıcıların eklediği sorular bu testlere girmez.</p>
      </section>
    </div>
  );
};

export default TestHub;
