import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Info, RefreshCw, RotateCcw, ChevronDown, AlertTriangle, ShieldAlert, Inbox, Quote, ListChecks, DatabaseZap, Network, Link2 } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { ChipBar, EmptyState, SearchBox, timeLabel } from './consoleUi';

/**
 * "Serbest girdiler": öğrencilerin tek kutuya yazdığı metinler ve sunucudaki ayrıştırma sonucu
 * (src/services/questionIntake.ts). Solda öğrencinin yazdığı (değişmez ham kayıt), sağda yönlendirici + uzman
 * ajanın çıkardığı ve kod denetiminden geçen alanlar. Her ögenin kanıt alıntısı üzerine gelince görünür.
 * Yönetici tek kaydı ya da istem sürümü eskimiş tüm kayıtları yeniden ayrıştırabilir; ham kayıt hiç değişmez.
 */
type Letter = 'A' | 'B' | 'C' | 'D' | 'E';
type Item = { metin: string; ozgun?: string; kanit: string; guven: number; normalizasyon_guveni?: number };
type Unit = {
  metin_parcasi: string;
  ders_tahmini: string;
  ders_guveni: number;
  ikincil_ders: string | null;
  karisma_notu: string | null;
  kurul_disi_suphesi: boolean;
  konu_tahmini: string | null;
  soru_no: number | null;
  soru_tipi: string;
  uzman: string;
  soru_odagi: Item | null;
  soru_koku_bulgulari: (Item & { tur: string })[];
  hatirlanan_siklar: (Item & { harf: Letter | null })[];
  iddia_edilen_cevap: (Item & { harf: Letter | null; tur: string }) | null;
  olumsuz_soru_koku_ihtimali: number;
  olumsuz_gerekce: string;
  tibbi_varliklar: { ad: string; tip: string }[];
  eksikler: string[];
  model: string;
};
type Status = 'bekliyor' | 'isleniyor' | 'ayristirildi' | 'icerik_yok' | 'kota_bekliyor' | 'hata';
type Row = {
  raw: {
    id: string;
    createdAt: string;
    committeeId: string;
    questionNumber?: number;
    discipline?: string;
    questionId?: string;
    uid?: string;
    author?: string;
    source: string;
    rawText: string;
    formOptions?: { key: Letter; text: string }[];
    formClaimedAnswer?: Letter;
  };
  state: { status: Status; attempts: number; nextTryAt?: string; lastError?: string; updatedAt: string; geriYazma?: 'bekliyor' | 'yazildi' | 'yok' } | null;
  parse: {
    createdAt: string;
    promptVersion: string;
    status: string;
    enjeksiyon_suphesi: boolean;
    units: Unit[];
    models: string[];
    validationErrors: string[];
  } | null;
};
type Resp = {
  promptVersion: string;
  counts: Partial<Record<Status, number>>;
  outdated: number;
  total: number;
  matched: number;
  committees: string[];
  items: Row[];
};
type Filter = 'hepsi' | 'ayristirildi' | 'sirada' | 'kota_bekliyor' | 'hata' | 'icerik_yok' | 'eski';

const PAGE = 30;
const STATUS_LABEL: Record<Status, string> = {
  bekliyor: 'Sırada',
  isleniyor: 'İşleniyor',
  ayristirildi: 'Ayrıştırıldı',
  icerik_yok: 'İçerik yok',
  kota_bekliyor: 'Kota bekliyor',
  hata: 'Hata',
};
const STATUS_TONE: Record<Status, string> = {
  bekliyor: '',
  isleniyor: 'is-accent',
  ayristirildi: 'is-ok',
  icerik_yok: '',
  kota_bekliyor: 'is-warn',
  hata: 'is-bad',
};
const kurulLabel = (id: string) => {
  const m = /donem(\d)-kurul(\d+)/.exec(id);
  return m ? `D${m[1]} · Kurul ${m[2]}` : id;
};
const pct = (v: number) => `%${Math.round(v * 100)}`;
const tone = (v: number) => (v >= 0.75 ? 'text-ok' : v >= 0.5 ? 'text-ink-2' : 'text-warn');

/** Kanıtı üzerine gelince gösteren tek öge; güven rengi ve "öğrencinin yazdığı" farkı. */
const Ev: React.FC<{ it: Item; prefix?: string }> = ({ it, prefix }) => {
  const changed = it.ozgun && it.ozgun.trim().toLocaleLowerCase('tr') !== it.metin.trim().toLocaleLowerCase('tr');
  return (
    <span
      className="inline-block px-2 py-0.5 rounded-lg bg-canvas text-sm text-ink leading-snug max-w-full break-words"
      title={`Kanıt: "${it.kanit}"${changed ? `\nÖğrencinin yazdığı: "${it.ozgun}"` : ''}\nGüven: ${pct(it.guven)}`}
    >
      {prefix && <b className="font-mono text-xs whitespace-nowrap mr-1">{prefix}</b>}
      {it.metin}
      {changed && <span className="text-xs text-ink-3"> ← {it.ozgun}</span>}
      <span className={`text-xs tabular-nums whitespace-nowrap ml-1.5 ${tone(it.guven)}`}>{pct(it.guven)}</span>
    </span>
  );
};

const Line: React.FC<{ label: string; children: React.ReactNode }> = ({ label, children }) => (
  <div className="grid grid-cols-[7.5rem_1fr] gap-2 items-start max-sm:grid-cols-1 max-sm:gap-1">
    <span className="text-xs font-semibold uppercase tracking-wide text-ink-3 pt-1">{label}</span>
    <div className="flex flex-wrap gap-1.5 min-w-0">{children}</div>
  </div>
);

const UnitView: React.FC<{ u: Unit; n: number; of: number }> = ({ u, n, of }) => (
  <div className="flex flex-col gap-2 min-w-0">
    <div className="flex flex-wrap items-center gap-1.5">
      {of > 1 && <span className="ms-tag is-accent">Soru birimi {n}/{of}</span>}
      <span className="font-semibold text-ink">{u.ders_tahmini === 'Belirsiz' ? 'Ders belirsiz' : u.ders_tahmini}</span>
      {u.ders_tahmini !== 'Belirsiz' && <span className={`text-xs tabular-nums ${tone(u.ders_guveni)}`}>{pct(u.ders_guveni)}</span>}
      {u.ikincil_ders && <span className="ms-tag">+ {u.ikincil_ders}</span>}
      {u.soru_no && <span className="ms-tag">Soru {u.soru_no}</span>}
      {u.kurul_disi_suphesi && <span className="ms-tag is-warn">Kurul dışı olabilir</span>}
      <span className="text-xs text-ink-3">{u.uzman} · {u.soru_tipi}</span>
    </div>
    {u.konu_tahmini && <p className="m-0 text-sm text-ink-2">Konu: {u.konu_tahmini}</p>}
    {u.karisma_notu && <p className="m-0 text-sm text-warn">Ders karışması: {u.karisma_notu}</p>}
    {u.soru_odagi && <Line label="Sorulan"><Ev it={u.soru_odagi} /></Line>}
    {u.soru_koku_bulgulari.length > 0 && (
      <Line label="Kökte">{u.soru_koku_bulgulari.map((b, i) => <Ev key={i} it={b} />)}</Line>
    )}
    <Line label="Şıklar">
      {u.hatirlanan_siklar.length ? u.hatirlanan_siklar.map((s, i) => <Ev key={i} it={s} prefix={s.harf ? `${s.harf})` : '?)'} />) : <span className="text-sm text-ink-3 pt-0.5">Hatırlanan şık yok</span>}
    </Line>
    {u.iddia_edilen_cevap && (
      <Line label={u.iddia_edilen_cevap.tur === 'dogru_cevap_dedi' ? 'Doğru dediği' : 'İşaretlediği'}>
        <Ev it={u.iddia_edilen_cevap} prefix={u.iddia_edilen_cevap.harf ? `${u.iddia_edilen_cevap.harf})` : undefined} />
      </Line>
    )}
    <Line label="Olumsuz kök">
      <span className="flex items-center gap-2 min-w-[10rem] pt-1" title={u.olumsuz_gerekce}>
        <span className="ms-progress w-24 shrink-0"><span style={{ width: pct(u.olumsuz_soru_koku_ihtimali).slice(1) + '%', background: u.olumsuz_soru_koku_ihtimali >= 0.5 ? 'var(--color-warn)' : undefined }} /></span>
        <span className={`text-xs tabular-nums whitespace-nowrap ${u.olumsuz_soru_koku_ihtimali >= 0.5 ? 'text-warn font-semibold' : 'text-ink-3'}`}>{pct(u.olumsuz_soru_koku_ihtimali)}</span>
        {u.olumsuz_soru_koku_ihtimali >= 0.5 && u.iddia_edilen_cevap && <span className="text-xs text-warn">işaretlenen şık doğru önerme olabilir</span>}
      </span>
    </Line>
    {u.tibbi_varliklar.length > 0 && (
      <Line label="Varlıklar">{u.tibbi_varliklar.map((v, i) => <span key={i} className="ms-tag" title={v.tip}>{v.ad}</span>)}</Line>
    )}
    {u.eksikler.length > 0 && <Line label="Eksik"><span className="text-sm text-ink-3 pt-0.5">{u.eksikler.join(' · ')}</span></Line>}
    <span className="text-xs text-ink-3 font-mono">{u.model}</span>
  </div>
);

export const ManageIntakeSection: React.FC<{ adminEmail: string }> = ({ adminEmail }) => {
  const headers = useMemo(() => ({ 'Content-Type': 'application/json', 'x-admin-email': adminEmail || '' }), [adminEmail]);
  const [data, setData] = useState<Resp | null>(null);
  const [filter, setFilter] = useState<Filter>('hepsi');
  const [committee, setCommittee] = useState('');
  const [query, setQuery] = useState('');
  const [limit, setLimit] = useState(PAGE);
  const [busy, setBusy] = useState<string | null>(null);
  const [openErr, setOpenErr] = useState<Set<string>>(new Set());
  const reqId = useRef(0);
  type ClusterStatus = { running: boolean; scheduled: boolean; aiQueue: number; aiRunning: boolean; lastRun: { at: string; ms: number; items: number; clusters: number } | null };
  const [kume, setKume] = useState<ClusterStatus | null>(null);
  const loadKume = () =>
    safeJsonFetch<{ status: ClusterStatus }>('/api/pool-clusters', { headers }).then((r) => { if (r.ok && r.data?.status) setKume(r.data.status); });
  useEffect(() => { loadKume(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const statusParam = filter === 'hepsi' ? '' : filter === 'sirada' ? 'bekliyor' : filter;
  const load = async (quiet = false) => {
    const id = ++reqId.current;
    const qs = new URLSearchParams({ limit: String(limit) });
    if (statusParam) qs.set('status', statusParam);
    if (committee) qs.set('committeeId', committee);
    if (query.trim()) qs.set('q', query.trim());
    const r = await safeJsonFetch<Resp>(`/api/admin/question-intake?${qs}`, { headers });
    if (id !== reqId.current) return;
    if (r.ok && r.data) setData(r.data);
    else if (!quiet) toast.error('Serbest girdiler alınamadı.', r.error);
  };

  useEffect(() => {
    const t = setTimeout(() => load(), query ? 250 : 0);
    return () => clearTimeout(t);
  }, [filter, committee, query, limit]); // eslint-disable-line react-hooks/exhaustive-deps

  // Sırada/işlenen kayıt varken liste kendiliğinden tazelenir
  const pending = (data?.counts.bekliyor || 0) + (data?.counts.isleniyor || 0);
  useEffect(() => {
    if (!pending) return;
    const t = setInterval(() => load(true), 5000);
    return () => clearInterval(t);
  }, [pending, filter, committee, query, limit]); // eslint-disable-line react-hooks/exhaustive-deps

  const reparse = async (id: string) => {
    setBusy(id);
    const r = await safeJsonFetch(`/api/admin/question-intake/${encodeURIComponent(id)}/reparse`, { method: 'POST', headers });
    setBusy(null);
    if (r.ok) {
      toast.success('Yeniden ayrıştırma sıraya alındı.');
      load(true);
    } else toast.error('Sıraya alınamadı.', r.error);
  };

  const reparseOutdated = async () => {
    setBusy('*');
    const r = await safeJsonFetch<{ queued: number }>('/api/admin/question-intake/reparse-outdated', { method: 'POST', headers });
    setBusy(null);
    if (r.ok) {
      toast.success(r.data?.queued ? `${r.data.queued} kayıt yeniden sıraya alındı.` : 'Yeniden ayrıştırılacak kayıt yok.');
      load(true);
    } else toast.error('Sıraya alınamadı.', r.error);
  };

  const backfill = async () => {
    setBusy('backfill');
    const r = await safeJsonFetch<{ queued: number }>('/api/admin/question-intake/backfill', { method: 'POST', headers });
    setBusy(null);
    if (r.ok) {
      toast.success(r.data?.queued ? `${r.data.queued} soru ayrıştırma sırasına alındı.` : 'Ayrıştırılmamış soru kalmadı.');
      load(true);
    } else toast.error('Sıraya alınamadı.', r.error);
  };

  const reclusterNow = async () => {
    setBusy('kume');
    const r = await safeJsonFetch('/api/pool-clusters/run-pipeline', { method: 'POST', headers });
    setBusy(null);
    if (r.ok) {
      toast.success('Kümeler yeniden hesaplanıyor.');
      setTimeout(loadKume, 1500);
    } else toast.error('Başlatılamadı.', r.error);
  };

  const c = data?.counts || {};
  const retryable = (data?.outdated || 0) + (c.hata || 0);

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <div className="ms-alert is-accent">
        <Info aria-hidden="true" />
        <span>
          Öğrencilerin hızlı ekle kutusuna yazdığı metinler. Solda öğrencinin yazdığı (<b>değişmez ham kayıt</b>), sağda ücretsiz Gemini ajanlarının
          çıkardığı ve kod denetiminden geçen alanlar. Bir ögenin üzerine gelince dayandığı alıntı ve güveni görünür; kanıtı metinde olmayan
          öge zaten düşürülmüştür. İstem sürümü: <span className="font-mono">{data?.promptVersion || '…'}</span>
        </span>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <div className="flex-1 min-w-0 basis-full sm:basis-[16rem]">
          <SearchBox value={query} onChange={(v) => { setQuery(v); setLimit(PAGE); }} placeholder="Metin, ders ya da terim ara" count={data ? `${data.matched}` : undefined} className="w-full" />
        </div>
        <label className="ms-select-chip !h-9">
          <span className="sr-only">Kurul</span>
          <select value={committee} onChange={(e) => { setCommittee(e.target.value); setLimit(PAGE); }}>
            <option value="">Tüm kurullar</option>
            {(data?.committees || []).map((id) => <option key={id} value={id}>{kurulLabel(id)}</option>)}
          </select>
        </label>
        <button type="button" onClick={() => load()} className="ms-btn is-sm" aria-label="Yenile"><RefreshCw /> Yenile</button>
        <button type="button" disabled={busy === 'backfill'} onClick={backfill} className="ms-btn is-sm is-tonal" title="Serbest metin girdisi olmayan havuz sorularını da ayrıştırır (ders, konu, terimler); kümeleme bunları kullanır">
          <DatabaseZap /> Havuz sorularını ayrıştır
        </button>
        <button type="button" disabled={busy === '*' || !retryable} onClick={reparseOutdated} className="ms-btn is-sm is-tonal" title="İstem sürümü eskimiş ve hata almış kayıtları yeniden ayrıştırır">
          <RotateCcw /> Eski ve hatalıları yeniden ayrıştır{retryable ? ` (${retryable})` : ''}
        </button>
      </div>

      <div className="flex flex-wrap items-center gap-2 text-sm text-ink-3">
        <Network className="w-4 h-4" aria-hidden />
        {kume?.lastRun
          ? <span>Kümeleme: {kume.lastRun.items} öge → <b className="text-ink-2">{kume.lastRun.clusters} küme</b> · {kume.lastRun.ms} ms · {timeLabel(kume.lastRun.at, true)}</span>
          : <span>Kümeleme henüz çalışmadı.</span>}
        {kume?.running && <span className="ms-tag is-accent">Hesaplanıyor</span>}
        {kume?.scheduled && !kume.running && <span className="ms-tag">Sırada</span>}
        {kume && kume.aiQueue > 0 && <span className="ms-tag" title="Yapay zekâ birleştirmesi bekleyen küme">AI kuyruğu {kume.aiQueue}</span>}
        <button type="button" disabled={busy === 'kume' || kume?.running} onClick={reclusterNow} className="ms-btn is-ghost is-sm"><RefreshCw /> Kümeleri yeniden hesapla</button>
      </div>

      <ChipBar
        label="Durum"
        value={filter}
        onChange={(v) => { setFilter(v); setLimit(PAGE); }}
        options={[
          { id: 'hepsi', label: 'Hepsi', n: data?.total },
          { id: 'ayristirildi', label: 'Ayrıştırıldı', n: c.ayristirildi || 0 },
          { id: 'sirada', label: 'Sırada', n: pending },
          { id: 'kota_bekliyor', label: 'Kota bekliyor', n: c.kota_bekliyor || 0 },
          { id: 'hata', label: 'Hata', n: c.hata || 0 },
          { id: 'icerik_yok', label: 'İçerik yok', n: c.icerik_yok || 0 },
          { id: 'eski', label: 'Eski sürüm', n: data?.outdated || 0 },
        ]}
      />

      {data === null ? (
        <div className="flex flex-col gap-3" role="status" aria-label="Yükleniyor">
          {[0, 1].map((i) => <div key={i} className="h-44 rounded-2xl ms-shimmer" />)}
        </div>
      ) : data.items.length === 0 ? (
        <section className="ms-panel">
          <EmptyState icon={Inbox} title={data.total ? 'Bu süzgeçte girdi yok' : 'Henüz serbest metin girdisi yok'}>
            {data.total ? null : 'Öğrenciler hızlı ekle kutusuna yazdıkça burada görünür.'}
          </EmptyState>
        </section>
      ) : (
        <>
          {data.items.map((row) => {
            const st = row.state?.status || 'bekliyor';
            const p = row.parse;
            const old = p && p.promptVersion !== data.promptVersion;
            const errs = p?.validationErrors || [];
            const errOpen = openErr.has(row.raw.id);
            return (
              <section key={row.raw.id} className="ms-panel">
                <header className="ms-panel-head">
                  <span className="flex flex-wrap items-center gap-1.5 min-w-0">
                    <span className={`ms-tag ${STATUS_TONE[st]}`}>{STATUS_LABEL[st]}</span>
                    {old && <span className="ms-tag is-warn" title={`Ayrıştırıldığı sürüm: ${p!.promptVersion}`}>Eski sürüm</span>}
                    {p?.enjeksiyon_suphesi && <span className="ms-tag is-bad"><ShieldAlert /> Talimat enjeksiyonu</span>}
                    {row.state?.geriYazma === 'yazildi' && <span className="ms-tag is-ok" title="Ayrıştırma soru kaydına yazıldı"><Link2 /> Soruya yazıldı</span>}
                    {row.state?.geriYazma === 'bekliyor' && <span className="ms-tag is-warn" title="Soru kaydı sunucuya ulaşınca yazılacak">Soruya yazılacak</span>}
                    <span className="text-sm text-ink-2">{kurulLabel(row.raw.committeeId)}</span>
                    {row.raw.questionNumber && <span className="text-sm text-ink-3">· Soru {row.raw.questionNumber}</span>}
                    <span className="text-sm text-ink-3 tabular-nums">· {timeLabel(row.raw.createdAt, true)}</span>
                    <span className="font-mono text-xs text-ink-3 truncate max-w-[22ch]" title={row.raw.id}>{row.raw.id}</span>
                  </span>
                  <span className="ms-panel-tools">
                    <button type="button" disabled={busy === row.raw.id || st === 'isleniyor'} onClick={() => reparse(row.raw.id)} className="ms-btn is-sm">
                      <RotateCcw /> Yeniden ayrıştır
                    </button>
                  </span>
                </header>

                <div className="p-3 grid gap-3" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 320px), 1fr))' }}>
                  <article className="rounded-xl p-3 bg-canvas flex flex-col gap-2 min-w-0">
                    <span className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-ink-3"><Quote className="w-3.5 h-3.5" /> Öğrencinin yazdığı</span>
                    <p className="m-0 text-base text-ink leading-relaxed break-words whitespace-pre-wrap">{row.raw.rawText || <i className="text-ink-3">Metin yok, yalnız şık</i>}</p>
                    {row.raw.formOptions && row.raw.formOptions.length > 0 && (
                      <ul className="m-0 p-0 list-none flex flex-col gap-0.5 text-sm text-ink-2">
                        {row.raw.formOptions.map((o) => <li key={o.key}><b className="font-mono">{o.key})</b> {o.text}{row.raw.formClaimedAnswer === o.key && <span className="text-ok font-semibold"> · işaretledi</span>}</li>)}
                      </ul>
                    )}
                    {row.raw.formClaimedAnswer && !row.raw.formOptions?.some((o) => o.key === row.raw.formClaimedAnswer) && (
                      <p className="m-0 text-sm text-ink-2">İşaretlediği: <b>{row.raw.formClaimedAnswer}</b></p>
                    )}
                    <p className="m-0 mt-auto pt-1 text-xs text-ink-3 break-words">
                      {[row.raw.author, row.raw.discipline && `formdaki ders: ${row.raw.discipline}`, row.raw.source].filter(Boolean).join(' · ')}
                      {row.raw.questionId && <> · bağlı soru <span className="font-mono">{row.raw.questionId}</span></>}
                    </p>
                  </article>

                  <article className="rounded-xl p-3 border border-line-soft flex flex-col gap-3 min-w-0">
                    <span className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-ink-3"><ListChecks className="w-3.5 h-3.5" /> Ayrıştırılan</span>
                    {st === 'ayristirildi' && p ? (
                      p.units.map((u, i) => (
                        <div key={i} className={i > 0 ? 'pt-3 border-t border-line-soft' : ''}>
                          <UnitView u={u} n={i + 1} of={p.units.length} />
                        </div>
                      ))
                    ) : st === 'icerik_yok' ? (
                      <p className="m-0 text-sm text-ink-3">Metinde soruya ait bilgi bulunmadı (sohbet ya da şikâyet).</p>
                    ) : st === 'kota_bekliyor' || st === 'hata' ? (
                      <div className="flex flex-col gap-1 text-sm">
                        <p className={`m-0 flex gap-1.5 ${st === 'hata' ? 'text-bad-text' : 'text-warn'}`}>
                          <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
                          {st === 'hata' ? `${row.state?.attempts || 0} denemede ayrıştırılamadı.` : `Ücretsiz kota ya da model yoğunluğu; ${row.state?.attempts || 0}. deneme bekliyor.`}
                        </p>
                        {row.state?.nextTryAt && st !== 'hata' && <p className="m-0 text-ink-3">Sonraki deneme: {timeLabel(row.state.nextTryAt, true)}</p>}
                        {row.state?.lastError && <p className="m-0 text-xs font-mono text-ink-3 break-words">{row.state.lastError}</p>}
                      </div>
                    ) : (
                      <div className="flex flex-col gap-2" role="status">
                        <span className="text-sm text-ink-3">{st === 'isleniyor' ? 'Ajanlar çalışıyor…' : 'Sırada bekliyor…'}</span>
                        <span className="ms-progress is-indeterminate"><span /></span>
                      </div>
                    )}
                    {p && (
                      <div className="mt-auto flex flex-wrap items-center gap-2 text-xs text-ink-3">
                        <span className="font-mono">{p.models.join(' → ')}</span>
                        <span>· {timeLabel(p.createdAt, true)}</span>
                        {errs.length > 0 && (
                          <button
                            type="button"
                            className="ms-btn is-ghost is-sm"
                            aria-expanded={errOpen}
                            onClick={() => setOpenErr((s) => { const n = new Set(s); n.has(row.raw.id) ? n.delete(row.raw.id) : n.add(row.raw.id); return n; })}
                          >
                            <ChevronDown className={errOpen ? 'rotate-180' : ''} /> Denetim notu ({errs.length})
                          </button>
                        )}
                      </div>
                    )}
                    {errOpen && (
                      <ul className="m-0 pl-4 text-xs text-ink-2 flex flex-col gap-0.5">
                        {errs.map((e, i) => <li key={i} className="break-words">{e}</li>)}
                      </ul>
                    )}
                  </article>
                </div>
              </section>
            );
          })}
          {data.matched > data.items.length && (
            <button type="button" onClick={() => setLimit((n) => n + PAGE)} className="ms-btn self-center">
              <ChevronDown /> {data.matched - data.items.length} girdi daha
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default ManageIntakeSection;
