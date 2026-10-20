import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Info, RefreshCw, RotateCcw, ChevronDown, AlertTriangle, ShieldAlert, Inbox, Quote, ListChecks, DatabaseZap, Network, Link2 } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { EmptyState, timeLabel, Drawer } from './consoleUi';
import { PageActions, StatRow, Tabs14, SearchField, Toolbar, DataTable, Pill, DetailNav, DetailLayout, FactList, Card14, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';

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
const STATUS_TONE: Record<Status, 'ok' | 'warn' | 'bad' | 'acc' | ''> = {
  bekliyor: '',
  isleniyor: 'acc',
  ayristirildi: 'ok',
  icerik_yok: '',
  kota_bekliyor: 'warn',
  hata: 'bad',
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
  const [openId, setOpenId] = useState<string | null>(null);
  const selection = useSelection<string>();
  const [bulkBusy, setBulkBusy] = useState(false);
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
  const items = data?.items || [];
  const openRow = items.find((r) => r.raw.id === openId) || null;

  const bulkReparse = async () => {
    const ids = items.filter((r) => selection.has(r.raw.id)).map((r) => r.raw.id);
    setBulkBusy(true);
    let ok = 0;
    let bad = 0;
    for (const id of ids) {
      const r = await safeJsonFetch(`/api/admin/question-intake/${encodeURIComponent(id)}/reparse`, { method: 'POST', headers });
      if (r.ok) ok++; else bad++;
    }
    setBulkBusy(false);
    if (bad) toast.error(`${ok} başarılı, ${bad} hata.`);
    else { toast.success(`${ok} başarılı, 0 hata.`); selection.clear(); }
    load(true);
  };

  const cols: Col<Row>[] = [
    { key: 'txt', label: 'Girdi', main: true, render: (row) => row.raw.rawText || 'Metin yok, yalnız şık' },
    {
      key: 'st', label: 'Ayrıştırma', render: (row) => {
        const st = row.state?.status || 'bekliyor';
        const old = row.parse && row.parse.promptVersion !== data?.promptVersion;
        return (
          <span className="inline-flex gap-1 flex-wrap">
            <Pill tone={STATUS_TONE[st]}>{STATUS_LABEL[st]}</Pill>
            {old && <Pill tone="warn">Eski</Pill>}
            {row.parse?.enjeksiyon_suphesi && <Pill tone="bad">Enjeksiyon</Pill>}
          </span>
        );
      },
    },
    { key: 'ders', label: 'Ders', render: (row) => <span className="clip">{row.parse?.units?.[0]?.ders_tahmini || row.raw.discipline || '—'}</span> },
    { key: 'g', label: 'Güven', right: true, render: (row) => { const u = row.parse?.units?.[0]; return u ? <span className={tone(u.ders_guveni)}>{pct(u.ders_guveni)}</span> : '—'; } },
    { key: 'k', label: 'Kurul', muted: true, render: (row) => kurulLabel(row.raw.committeeId) },
    { key: 't', label: 'Zaman', muted: true, render: (row) => timeLabel(row.raw.createdAt, true) },
  ];

  const renderDetail = (row: Row) => {
    const st = row.state?.status || 'bekliyor';
    const p = row.parse;
    const old = p && p.promptVersion !== data?.promptVersion;
    const errs = p?.validationErrors || [];
    const errOpen = openErr.has(row.raw.id);
    return (
      <DetailLayout
        main={
          <>
            <Card14 title={<span className="inline-flex items-center gap-1.5"><Quote className="w-4 h-4" aria-hidden="true" /> Öğrencinin yazdığı</span>}>
              <div className="flex flex-col gap-2">
                <p className="m-0 text-base text-ink leading-relaxed break-words whitespace-pre-wrap">{row.raw.rawText || <i className="text-ink-3">Metin yok, yalnız şık</i>}</p>
                {row.raw.formOptions && row.raw.formOptions.length > 0 && (
                  <ul className="m-0 p-0 list-none flex flex-col gap-0.5 text-sm text-ink-2">
                    {row.raw.formOptions.map((o) => <li key={o.key}><b className="font-mono">{o.key})</b> {o.text}{row.raw.formClaimedAnswer === o.key && <span className="text-ok font-semibold"> · işaretledi</span>}</li>)}
                  </ul>
                )}
                {row.raw.formClaimedAnswer && !row.raw.formOptions?.some((o) => o.key === row.raw.formClaimedAnswer) && (
                  <p className="m-0 text-sm text-ink-2">İşaretlediği: <b>{row.raw.formClaimedAnswer}</b></p>
                )}
              </div>
            </Card14>
            <Card14 title={<span className="inline-flex items-center gap-1.5"><ListChecks className="w-4 h-4" aria-hidden="true" /> Ayrıştırma kanıtı</span>}>
              <div className="flex flex-col gap-3 min-w-0">
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
                      <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" aria-hidden="true" />
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
                  <div className="flex flex-wrap items-center gap-2 text-xs text-ink-3">
                    <span className="font-mono break-words">{p.models.join(' → ')}</span>
                    <span>· {timeLabel(p.createdAt, true)}</span>
                    {errs.length > 0 && (
                      <button
                        type="button"
                        className="m14-btn ghost"
                        aria-expanded={errOpen}
                        onClick={() => setOpenErr((s) => { const n = new Set(s); n.has(row.raw.id) ? n.delete(row.raw.id) : n.add(row.raw.id); return n; })}
                      >
                        <ChevronDown className={errOpen ? 'rotate-180' : ''} aria-hidden="true" /> Denetim notu ({errs.length})
                      </button>
                    )}
                  </div>
                )}
                {errOpen && (
                  <ul className="m-0 pl-4 text-xs text-ink-2 flex flex-col gap-0.5">
                    {errs.map((e, i) => <li key={i} className="break-words">{e}</li>)}
                  </ul>
                )}
              </div>
            </Card14>
          </>
        }
        side={
          <Card14 title="Bilgi">
            <FactList
              items={[
                { k: 'Durum', v: <Pill tone={STATUS_TONE[st]}>{STATUS_LABEL[st]}</Pill> },
                ...(old ? [{ k: 'Sürüm', v: <Pill tone="warn">Eski: {p!.promptVersion}</Pill> }] : []),
                ...(p?.enjeksiyon_suphesi ? [{ k: 'Uyarı', v: <Pill tone="bad"><ShieldAlert aria-hidden="true" /> Talimat enjeksiyonu</Pill> }] : []),
                ...(row.state?.geriYazma === 'yazildi' ? [{ k: 'Soru kaydı', v: <Pill tone="ok"><Link2 aria-hidden="true" /> Soruya yazıldı</Pill> }] : []),
                ...(row.state?.geriYazma === 'bekliyor' ? [{ k: 'Soru kaydı', v: <Pill tone="warn">Soruya yazılacak</Pill> }] : []),
                { k: 'Kurul', v: kurulLabel(row.raw.committeeId) },
                ...(row.raw.questionNumber ? [{ k: 'Soru no', v: row.raw.questionNumber }] : []),
                { k: 'Zaman', v: timeLabel(row.raw.createdAt, true) },
                { k: 'Gönderen', v: row.raw.author || '—' },
                ...(row.raw.discipline ? [{ k: 'Formdaki ders', v: row.raw.discipline }] : []),
                { k: 'Kaynak', v: row.raw.source },
                ...(row.raw.questionId ? [{ k: 'Bağlı soru', v: <span className="font-mono text-xs [overflow-wrap:anywhere]">{row.raw.questionId}</span> }] : []),
                { k: 'Kimlik', v: <span className="font-mono text-xs [overflow-wrap:anywhere]">{row.raw.id}</span> },
              ]}
            />
          </Card14>
        }
      />
    );
  };

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <PageActions
        note={
          <span className="inline-flex flex-wrap items-center gap-1.5">
            <Network className="w-4 h-4" aria-hidden="true" />
            {kume?.lastRun
              ? <span>Kümeleme: {kume.lastRun.items} öge → <b>{kume.lastRun.clusters} küme</b> · {kume.lastRun.ms} ms · {timeLabel(kume.lastRun.at, true)}</span>
              : <span>Kümeleme henüz çalışmadı.</span>}
            {kume?.running && <Pill tone="acc">Hesaplanıyor</Pill>}
            {kume?.scheduled && !kume.running && <Pill>Sırada</Pill>}
            {kume && kume.aiQueue > 0 && <Pill>AI kuyruğu {kume.aiQueue}</Pill>}
          </span>
        }
      >
        <button type="button" onClick={() => load()} className="m14-btn ghost"><RefreshCw aria-hidden="true" /> Yenile</button>
        <button type="button" disabled={busy === 'backfill'} onClick={backfill} className="m14-btn" title="Serbest metin girdisi olmayan havuz sorularını da ayrıştırır (ders, konu, terimler); kümeleme bunları kullanır">
          <DatabaseZap aria-hidden="true" /> Havuz sorularını ayrıştır
        </button>
        <button type="button" disabled={busy === '*' || !retryable} onClick={reparseOutdated} className="m14-btn" title="İstem sürümü eskimiş ve hata almış kayıtları yeniden ayrıştırır">
          <RotateCcw aria-hidden="true" /> Eskileri yeniden ayrıştır{retryable ? ` (${retryable})` : ''}
        </button>
        <button type="button" disabled={busy === 'kume' || kume?.running} onClick={reclusterNow} className="m14-btn primary"><RefreshCw aria-hidden="true" /> Kümeleme hattını çalıştır</button>
      </PageActions>

      <div className="ms-alert is-accent">
        <Info aria-hidden="true" />
        <span>
          Öğrencilerin hızlı ekle kutusuna yazdığı metinler (<b>değişmez ham kayıt</b>) ve ücretsiz Gemini ajanlarının çıkardığı, kod denetiminden
          geçen alanlar. Ayrıntıda her ögenin üzerine gelince dayandığı alıntı ve güveni görünür. İstem sürümü: <span className="font-mono">{data?.promptVersion || '…'}</span>
        </span>
      </div>

      <StatRow
        stats={[
          { label: 'Ayrıştırılmış', value: (c.ayristirildi || 0).toLocaleString('tr-TR'), tone: 'ok', onClick: () => { setFilter('ayristirildi'); setLimit(PAGE); } },
          { label: 'Eski ayrıştırıcı', value: (data?.outdated || 0).toLocaleString('tr-TR'), tone: data?.outdated ? 'warn' : undefined, onClick: () => { setFilter('eski'); setLimit(PAGE); } },
          { label: 'Sırada', value: pending.toLocaleString('tr-TR'), onClick: () => { setFilter('sirada'); setLimit(PAGE); } },
          { label: 'Hata', value: (c.hata || 0).toLocaleString('tr-TR'), tone: c.hata ? 'bad' : undefined, onClick: () => { setFilter('hata'); setLimit(PAGE); } },
        ]}
      />

      <Toolbar>
        <Tabs14
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
        <SearchField value={query} onChange={(v) => { setQuery(v); setLimit(PAGE); }} placeholder="Metin, ders ya da terim ara" label="Girdi metninde ara" />
        <label className="ms-select-chip !h-9">
          <span className="sr-only">Kurul</span>
          <select value={committee} onChange={(e) => { setCommittee(e.target.value); setLimit(PAGE); }}>
            <option value="">Tüm kurullar</option>
            {(data?.committees || []).map((id) => <option key={id} value={id}>{kurulLabel(id)}</option>)}
          </select>
        </label>
        {data && <span className="text-sm text-ink-3 tabular-nums">{data.matched.toLocaleString('tr-TR')} sonuç</span>}
      </Toolbar>

      <BulkBar
        count={selection.count}
        noun="girdi"
        busy={bulkBusy}
        onClear={selection.clear}
        actions={[{ label: 'Yeniden ayrıştır', kind: 'main', run: bulkReparse }]}
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
          <DataTable rows={items} cols={cols} rowKey={(r) => r.raw.id} onOpen={(r) => setOpenId(r.raw.id)} selection={selection} activeKey={openId} minWidth={820} />
          {data.matched > data.items.length && (
            <button type="button" onClick={() => setLimit((n) => n + PAGE)} className="m14-btn self-center">
              <ChevronDown aria-hidden="true" /> {data.matched - data.items.length} girdi daha
            </button>
          )}
        </>
      )}

      <Drawer
        open={!!openRow}
        onClose={() => setOpenId(null)}
        title={openRow ? (openRow.raw.rawText || 'Serbest girdi').slice(0, 80) : 'Serbest girdi'}
        label="Serbest girdi ayrıntısı"
        wide
        head={<DetailNav list={items} current={openRow} same={(a, b) => a.raw.id === b.raw.id} onGo={(r) => setOpenId(r.raw.id)} />}
        foot={openRow && (
          <button type="button" disabled={busy === openRow.raw.id || openRow.state?.status === 'isleniyor'} onClick={() => reparse(openRow.raw.id)} className="m14-btn primary">
            <RotateCcw aria-hidden="true" /> Yeniden ayrıştır
          </button>
        )}
      >
        {openRow && renderDetail(openRow)}
      </Drawer>
    </div>
  );
};

export default ManageIntakeSection;
