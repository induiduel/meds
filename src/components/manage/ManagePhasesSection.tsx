import React, { useEffect, useMemo, useState } from 'react';
import { Search, Save, RotateCcw, FlaskConical, Code2, ChevronLeft, ChevronRight, ArrowUpDown, Info } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { QuestionInsightsPanel, clearInsightsCache } from '../QuestionInsightsPanel';
import { toast } from '../ui/Toast';
import { SearchBox, ChipBar, EmptyState, Drawer } from './consoleUi';
import { ApiService } from '../../services/api';

/**
 * "Faz verileri": bir çıkmış sorunun tüm faz çıktılarını (Faz 5/6/6.5/8/11/13, Öğren, sınav başlığı müfredatı,
 * karantina) gösterir; elle düzeltme kaydeder (faz çıktısına dokunmaz, okuma sırasında uygulanır);
 * arama motorunu soruyla çalıştırıp Faz 11 eşleşmesiyle karşılaştırır; sitede görüneni önizler.
 */
type Slide = { kaynak: string; sayfa: number; alinti?: string };
type Override = {
  gizle?: string[];
  kaldir?: string[];
  slaytlar?: Slide[];
  kazanim?: { kurul?: number; ders?: string; konu?: string; kazanim?: string };
  kisaltmalar?: Record<string, string>;
  not?: string;
  guncelleyen?: string;
  guncelleme?: string;
};
type Detail = { id: string; ham: any; gorunen: any; duzeltme: Override | null; kayitlar: Record<string, any> };
type Cat = { id: string; label: string; desc: string; satir: number; soru: number; alanlar: string[] };
type ExploreRes = { alanlar: string[]; toplam: number; sayfa: number; boyut: number; satirlar: Record<string, any>[]; dagilim: { deger: string; sayi: number }[] };
type TestResult = { sonuclar: { baslik: string; sayfa: number | null; skor: number; metin: string }[]; faz11: Slide[] };

const HIDEABLE: [string, string][] = [
  ['mufredat', 'Kazanım'],
  ['slayt', 'Slaytlar (Faz 11)'],
  ['kisaltmalar', 'Kısaltmalar'],
  ['terimler', 'Terimler'],
  ['varliklar', 'Varlıklar (Faz 13)'],
  ['faz6', 'Ayırıcı tanı (Faz 6)'],
];
const stemOf = (q: any) => q?.reconstruction?.stem || q?.stem || q?.rawQuestion?.stem || '';
const fold = (s: string) => s.toLocaleLowerCase('tr-TR');
const card = 'rounded-xl bg-canvas p-3.5 flex flex-col gap-2 min-w-0';
const h3 = 'm-0 text-[12.5px] font-semibold text-ink-2';
const input = 'ms-input';

function Json({ value }: { value: any }) {
  return (
    <pre className="ms-term !max-h-72 !min-h-0 !text-[11.5px]">
      {value == null ? '—' : JSON.stringify(value, null, 1)}
    </pre>
  );
}

export const ManagePhasesSection: React.FC<{ adminEmail: string }> = ({ adminEmail }) => {
  const headers = { 'Content-Type': 'application/json', 'x-admin-email': adminEmail || '' };
  const [pool, setPool] = useState<any[]>([]);
  const [term, setTerm] = useState('');
  const [selId, setSelId] = useState<string | null>(null);
  const [detail, setDetail] = useState<Detail | null>(null);
  const [form, setForm] = useState<{ gizle: string[]; slaytlar: string; kazanim: Override['kazanim']; kisaltmalar: string; not: string }>(
    { gizle: [], slaytlar: '', kazanim: {}, kisaltmalar: '', not: '' },
  );
  const [query, setQuery] = useState('');
  const [test, setTest] = useState<TestResult | null>(null);
  const [busy, setBusy] = useState<'' | 'save' | 'test'>('');
  const [showRaw, setShowRaw] = useState(false);
  const [previewKey, setPreviewKey] = useState(0);
  // Gezgin: kategori + alan sorgusu (arama yapmadan listelenir)
  const [cats, setCats] = useState<Cat[]>([]);
  const [eq, setEq] = useState({ kategori: 'mufredat', alan: '', deger: '', sirala: '', yon: 'artan' as 'artan' | 'azalan', sayfa: 1, boyut: 50 });
  const [ex, setEx] = useState<ExploreRes | null>(null);
  const [exLoading, setExLoading] = useState(false);
  const [degerInput, setDegerInput] = useState('');

  useEffect(() => {
    safeJsonFetch<{ kategoriler: Cat[] }>('/api/admin/phases/categories', { headers }).then((r) => r.ok && r.data && setCats(r.data.kategoriler));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  useEffect(() => {
    setExLoading(true);
    const qs = new URLSearchParams(Object.entries(eq).map(([k, v]) => [k, String(v)])).toString();
    safeJsonFetch<ExploreRes>(`/api/admin/phases/explore?${qs}`, { headers }).then((r) => {
      setExLoading(false);
      if (r.ok && r.data) setEx(r.data);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [eq]);
  // değer kutusu: yazmayı bekle (300 ms)
  useEffect(() => {
    const t = window.setTimeout(() => setEq((q) => (q.deger === degerInput ? q : { ...q, deger: degerInput, sayfa: 1 })), 300);
    return () => window.clearTimeout(t);
  }, [degerInput]);
  const curCat = cats.find((c) => c.id === eq.kategori);
  const cols = (ex?.alanlar || []).filter((k) => k !== 'soru_id');

  useEffect(() => {
    safeJsonFetch<any>('/api/past-exams').then((r) => {
      const d = r.ok ? r.data : null;
      setPool(Array.isArray(d) ? d : d?.questions || []);
    });
  }, []);

  const matches = useMemo(() => {
    const t = fold(term.trim());
    if (t.length < 2) return [];
    const num = /^#?\d+$/.test(t) ? t.replace('#', '') : null;
    return pool
      .filter((q) => (num ? String(q.questionNumber) === num : q.id === t || fold(stemOf(q)).includes(t)))
      .slice(0, 20);
  }, [term, pool]);
  const selQ = useMemo(() => pool.find((q) => q.id === selId), [pool, selId]);

  const load = async (id: string) => {
    setSelId(id);
    setTest(null);
    const r = await safeJsonFetch<Detail>(`/api/admin/phases/question/${encodeURIComponent(id)}`, { headers });
    if (!r.ok || !r.data) {
      toast.error('Faz verisi alınamadı');
      return;
    }
    const d = r.data;
    setDetail(d);
    const ov = d.duzeltme || {};
    setForm({
      gizle: ov.gizle || [],
      slaytlar: (ov.slaytlar || []).map((s) => `${s.kaynak} | ${s.sayfa}${s.alinti ? ' | ' + s.alinti : ''}`).join('\n'),
      kazanim: ov.kazanim || {},
      kisaltmalar: Object.entries(ov.kisaltmalar || {}).map(([k, v]) => `${k} = ${v}`).join('\n'),
      not: ov.not || '',
    });
    const q = pool.find((x) => x.id === id);
    setQuery(stemOf(q));
  };

  const buildOverride = (): Override | null => {
    const slaytlar = form.slaytlar
      .split('\n')
      .map((l) => l.split('|').map((x) => x.trim()))
      .filter((p) => p[0] && Number(p[1]) > 0)
      .map((p) => ({ kaynak: p[0], sayfa: Number(p[1]), ...(p[2] ? { alinti: p[2] } : {}) }));
    const kisaltmalar = Object.fromEntries(
      form.kisaltmalar
        .split('\n')
        .map((l) => l.split('=').map((x) => x.trim()))
        .filter((p) => p[0] && p[1]),
    );
    const k = form.kazanim || {};
    const hasK = Boolean(k.ders || k.konu || k.kazanim);
    const ov: Override = {
      ...(form.gizle.length ? { gizle: form.gizle } : {}),
      ...(detail?.duzeltme?.kaldir?.length ? { kaldir: detail.duzeltme.kaldir } : {}),
      ...(slaytlar.length ? { slaytlar } : {}),
      ...(hasK ? { kazanim: { ...k, kurul: k.kurul ? Number(k.kurul) : undefined } } : {}),
      ...(Object.keys(kisaltmalar).length ? { kisaltmalar } : {}),
      ...(form.not.trim() ? { not: form.not.trim() } : {}),
    };
    return Object.keys(ov).length ? ov : null;
  };

  const save = async (reset = false) => {
    if (!selId) return;
    setBusy('save');
    const r = await safeJsonFetch<any>(`/api/admin/phases/question/${encodeURIComponent(selId)}/override`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(reset ? {} : buildOverride() || {}),
    });
    setBusy('');
    if (!r.ok) {
      toast.error('Kaydedilemedi');
      return;
    }
    toast.success(reset ? 'Elle düzeltme kaldırıldı' : 'Düzeltme kaydedildi; sitede hemen görünür');
    clearInsightsCache(selId);
    setPreviewKey((k) => k + 1);
    await load(selId);
  };

  // Bölüm işlemi (gizle / kaldır) — mevcut elle düzeltmeyi koruyarak tek tıkla kaydeder
  const toggleSection = async (kind: 'gizle' | 'kaldir', key: string) => {
    if (!selId || !detail) return;
    const ov: Override = { ...(detail.duzeltme || {}) };
    delete (ov as any).guncelleyen;
    delete (ov as any).guncelleme;
    const list = new Set(ov[kind] || []);
    if (list.has(key)) list.delete(key);
    else list.add(key);
    if (list.size) ov[kind] = [...list];
    else delete ov[kind];
    const r = await safeJsonFetch<any>(`/api/admin/phases/question/${encodeURIComponent(selId)}/override`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(ov),
    });
    if (!r.ok) {
      toast.error('İşlem kaydedilemedi');
      return;
    }
    toast.success(`${key}: ${list.has(key) ? (kind === 'gizle' ? 'gizlendi' : 'kaldırıldı') : 'geri alındı'}`);
    clearInsightsCache(selId);
    setPreviewKey((k) => k + 1);
    await load(selId);
  };

  const rereview = async (tur: 'slayt' | 'konu' | 'faz14') => {
    if (!selId) return;
    if (tur === 'faz14') {
      try {
        const r = await ApiService.reEvaluateUnchangedPastQuestionReviews(adminEmail, selId);
        toast.success(r.message || 'Faz 14 kuyruğuna alındı');
      } catch (e: any) {
        toast.error(`Faz 14: ${e?.message || 'bu soru için Faz 14 kaydı yok'}`);
      }
      return;
    }
    const r = await safeJsonFetch<any>(`/api/admin/phases/question/${encodeURIComponent(selId)}/rereview`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ tur }),
    });
    if (r.ok) toast.success(r.data?.mesaj || 'Hakem kuyruğuna eklendi');
    else toast.error('Hakem kuyruğuna eklenemedi');
  };

  // Kart başlığına bölüm işlemleri
  const SecActions = ({ k }: { k: string }) => {
    const ov = detail?.duzeltme || {};
    const hid = (ov.gizle || []).includes(k);
    const rem = (ov.kaldir || []).includes(k);
    return (
      <span className="inline-flex items-center gap-1">
        {(hid || rem) && <span className={`ms-tag ${rem ? 'is-bad' : 'is-warn'}`}>{rem ? 'Kaldırıldı' : 'Gizli'}</span>}
        <button type="button" className="ms-btn is-sm is-ghost" onClick={() => toggleSection('gizle', k)}>{hid ? 'Göster' : 'Gizle'}</button>
        <button type="button" className={`ms-btn is-sm ${rem ? 'is-ghost' : 'is-danger'}`} onClick={() => toggleSection('kaldir', k)}>{rem ? 'Geri al' : 'Kaldır'}</button>
      </span>
    );
  };

  const runTest = async () => {
    if (!selId) return;
    setBusy('test');
    const r = await safeJsonFetch<TestResult>(`/api/admin/phases/question/${encodeURIComponent(selId)}/test`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ query }),
    });
    setBusy('');
    if (!r.ok || !r.data) {
      toast.error('Arama testi çalışmadı');
      return;
    }
    setTest(r.data);
  };

  const ham = detail?.ham || {};
  const kay = detail?.kayitlar || {};
  const faz11Keys = new Set((test?.faz11 || []).map((s) => `${fold(s.kaynak)}#${s.sayfa}`));

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <div className="relative">
        <SearchBox value={term} onChange={setTerm} placeholder="Soruya git: numara (#1529), kimlik ya da kökten bir parça" />
        {term.trim().length >= 2 && (
          <div className="ms-suggest">
            {matches.length === 0 ? (
              <p className="m-0 px-3 py-3 text-[13px] text-ink-3">Eşleşen soru yok.</p>
            ) : (
              matches.map((q) => (
                <button key={q.id} type="button" onClick={() => { void load(q.id); setTerm(''); }} className="ms-suggest-row !min-h-[42px]">
                  <span className="font-mono text-[12px] text-ink-3 shrink-0">#{q.questionNumber}</span>
                  <span className="truncate">{stemOf(q).slice(0, 140)}</span>
                </button>
              ))
            )}
          </div>
        )}
      </div>

      <ChipBar
        label="Veri kategorisi"
        value={eq.kategori}
        onChange={(id) => {
          setDegerInput('');
          setEq({ kategori: id, alan: '', deger: '', sirala: '', yon: 'artan', sayfa: 1, boyut: eq.boyut });
        }}
        options={cats.map((c) => ({ id: c.id, label: c.label, n: c.soru }))}
      />

      <section className="ms-panel">
        <header className="ms-panel-head">
          <h2 className="ms-panel-title">{curCat?.label || 'Kategori'}</h2>
          {curCat && <span className="text-[12.5px] text-ink-3 tabular-nums">{curCat.satir.toLocaleString('tr-TR')} kayıt · {curCat.soru.toLocaleString('tr-TR')} soru</span>}
          {curCat?.desc && <p className="ms-panel-desc">{curCat.desc}</p>}
        </header>
        <div className="px-4 pt-3 pb-2 flex flex-col gap-2">
          <div className="grid gap-2 sm:grid-cols-[minmax(0,11rem)_minmax(0,1fr)_minmax(0,11rem)_auto]">
            <select className="ms-input" value={eq.alan} onChange={(e) => setEq((q) => ({ ...q, alan: e.target.value, sayfa: 1 }))} aria-label="Sorgulanacak alan">
              <option value="">Tüm alanlar</option>
              {cols.map((k) => <option key={k} value={k}>{k}</option>)}
            </select>
            <input className="ms-input" value={degerInput} onChange={(e) => setDegerInput(e.target.value)} placeholder='Değer: içerir · "=yuksek" tam eşleşme · "boş" / "dolu"' aria-label="Sorgu değeri" />
            <select className="ms-input" value={eq.sirala} onChange={(e) => setEq((q) => ({ ...q, sirala: e.target.value }))} aria-label="Sıralama alanı">
              <option value="">Sıralama yok</option>
              {cols.map((k) => <option key={k} value={k}>{k}</option>)}
            </select>
            <button type="button" onClick={() => setEq((q) => ({ ...q, yon: q.yon === 'artan' ? 'azalan' : 'artan' }))} className="ms-btn" aria-label="Sıralama yönü">
              <ArrowUpDown /> {eq.yon === 'artan' ? 'Artan' : 'Azalan'}
            </button>
          </div>
          {eq.alan && (ex?.dagilim?.length ?? 0) > 0 && (
            <div className="ms-chipbar is-wrap">
              <span className="text-[12.5px] text-ink-3 self-center">{eq.alan}:</span>
              {ex!.dagilim.map((d) => (
                <button key={d.deger} type="button" onClick={() => setDegerInput('=' + d.deger)} className={`ms-fchip !h-7 ${eq.deger === '=' + d.deger ? 'is-on' : ''}`}>
                  {d.deger.length > 40 ? d.deger.slice(0, 40) + '…' : d.deger} <span className="n">{d.sayi}</span>
                </button>
              ))}
            </div>
          )}
        </div>
        <div className="overflow-x-auto">
          <table className={`ms-table ${exLoading ? 'opacity-60' : ''}`}>
            <thead>
              <tr>
                <th scope="col">Soru</th>
                {cols.map((k) => <th key={k} scope="col">{k}</th>)}
              </tr>
            </thead>
            <tbody>
              {(ex?.satirlar || []).map((r, i) => (
                <tr key={i} onClick={() => load(String(r.soru_id))} className={`is-button ${r.soru_id === selId ? 'is-on' : ''}`}>
                  <td className="max-w-[22rem]">
                    <span className="block truncate" title={r._kok}>{r._kok || <span className="font-mono text-ink-3">{r.soru_id}</span>}</span>
                    {(r._durum || r._elle) && (
                      <span className="flex gap-1 pt-0.5">
                        {r._durum && <span className={`ms-tag ${r._durum === 'kaldırıldı' ? 'is-bad' : 'is-warn'}`}>{r._durum}</span>}
                        {r._elle && <span className="ms-tag is-warn">Elle düzeltildi</span>}
                      </span>
                    )}
                  </td>
                  {cols.map((k) => (
                    <td key={k} className="max-w-[16rem]">
                      <span className="block truncate" title={String(r[k] ?? '')}>{r[k] === true ? 'evet' : r[k] === false ? 'hayır' : String(r[k] ?? '—')}</span>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          {ex && ex.toplam === 0 && <EmptyState icon={Search} title="Bu sorguya uyan kayıt yok" />}
          {!ex && <div className="p-3 flex flex-col gap-2">{[0, 1, 2, 3].map((i) => <div key={i} className="h-8 rounded-lg ms-shimmer" />)}</div>}
        </div>
        {ex && ex.toplam > 0 && (
          <footer className="flex flex-wrap items-center justify-between gap-2 px-4 py-2.5 border-t border-line-soft text-[12.5px] text-ink-3">
            <span className="tabular-nums">{ex.toplam.toLocaleString('tr-TR')} kayıt · sayfa {ex.sayfa} / {Math.max(1, Math.ceil(ex.toplam / ex.boyut))} · satıra dokununca ayrıntı açılır</span>
            <div className="flex items-center gap-1">
              <select className="ms-input is-sm !w-auto" value={eq.boyut} onChange={(e) => setEq((q) => ({ ...q, boyut: Number(e.target.value), sayfa: 1 }))} aria-label="Sayfa boyutu">
                {[25, 50, 100, 200].map((n) => <option key={n} value={n}>{n} satır</option>)}
              </select>
              <button type="button" disabled={eq.sayfa <= 1} onClick={() => setEq((q) => ({ ...q, sayfa: q.sayfa - 1 }))} className="ms-btn is-sm is-icon is-ghost" aria-label="Önceki sayfa"><ChevronLeft /></button>
              <button type="button" disabled={eq.sayfa * eq.boyut >= ex.toplam} onClick={() => setEq((q) => ({ ...q, sayfa: q.sayfa + 1 }))} className="ms-btn is-sm is-icon is-ghost" aria-label="Sonraki sayfa"><ChevronRight /></button>
            </div>
          </footer>
        )}
      </section>

      <Drawer
        open={!!detail}
        onClose={() => { setDetail(null); setSelId(null); }}
        wide
        label="Faz verisi ayrıntısı"
        title={selQ ? `#${selQ.questionNumber}` : 'Soru'}
        head={
          <button type="button" onClick={() => setShowRaw((v) => !v)} className="ms-btn is-sm is-ghost">
            <Code2 /> {showRaw ? 'Kartlar' : 'Ham JSON'}
          </button>
        }
      >
      {detail && (
        <>
          <p className="m-0 text-[15px] leading-relaxed text-ink font-medium">{stemOf(selQ)}</p>
          {detail.gorunen?.elle_duzeltildi && (
            <div className="ms-alert is-warn !py-2">
              <Info aria-hidden="true" />
              <span>Elle düzeltilmiş · {detail.duzeltme?.guncelleyen} · {detail.duzeltme?.guncelleme?.slice(0, 16).replace('T', ' ')}</span>
            </div>
          )}
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="text-[12.5px] text-ink-3 mr-1">Yeniden incele</span>
            <button type="button" onClick={() => rereview('slayt')} className="ms-btn is-sm">Hakem · slayt</button>
            <button type="button" onClick={() => rereview('konu')} className="ms-btn is-sm">Hakem · konu</button>
            <button type="button" onClick={() => rereview('faz14')} className="ms-btn is-sm">Faz 14 · soru düzeltme</button>
          </div>

          {detail.duzeltme && (
            <section className="ms-dsec">
              <h3>Faz çıktısı ↔ sitede görünen</h3>
              {(['mufredat', 'slayt', 'faz6_5', 'faz6', 'varliklar'] as const)
                .filter((k) => JSON.stringify(ham?.[k] ?? null) !== JSON.stringify(detail.gorunen?.[k] ?? null))
                .map((k) => (
                  <div key={k} className="grid gap-2 md:grid-cols-2">
                    <div><p className="m-0 mb-1 text-[12px] font-semibold text-ink-3">{k} · faz çıktısı</p><Json value={ham?.[k] ?? null} /></div>
                    <div><p className="m-0 mb-1 text-[12px] font-semibold text-accent">{k} · sitede görünen</p><Json value={detail.gorunen?.[k] ?? null} /></div>
                  </div>
                ))}
            </section>
          )}
          {showRaw ? (
            <div className="grid gap-3 md:grid-cols-2">
              <div className={card}><h3 className={h3}>Faz çıktısı (ham)</h3><Json value={ham} /></div>
              <div className={card}><h3 className={h3}>Diğer kayıtlar</h3><Json value={kay} /></div>
            </div>
          ) : (
            <div className="grid gap-3 md:grid-cols-2">
              <div className={card}>
                <div className="flex items-center justify-between gap-2"><h3 className={h3}>Müfredat</h3><SecActions k="mufredat" /></div>
                <p className="m-0 text-[13px]">
                  <b>Sınav başlığı:</b>{' '}
                  {kay.mufredat_sinav_basligi ? `Kurul ${kay.mufredat_sinav_basligi.kurul} · ${kay.mufredat_sinav_basligi.ders} · ${kay.mufredat_sinav_basligi.konu}` : '—'}
                </p>
                <p className="m-0 text-[13px]">
                  <b>Faz 8/9 kazanım:</b>{' '}
                  {(() => {
                    const k = (ham.mufredat || ham.faz8)?.kazanimlar?.[0];
                    return k ? `${k.ders || ''} · ${k.konu || ''}${k.kazanim ? ' — ' + k.kazanim : ''}` : '—';
                  })()}
                </p>
              </div>
              <div className={card}>
                <div className="flex items-center justify-between gap-2"><h3 className={h3}>Slaytlar (Faz 11) · güven {ham.slayt?.guven || '—'}</h3><SecActions k="slayt" /></div>
                {(ham.slayt?.slaytlar || []).map((s: any) => (
                  <p key={`${s.kaynak}${s.sayfa}`} className="m-0 text-[13px]">
                    <b>{s.kaynak}</b> · s.{s.sayfa} <span className="text-ink-3">{(s.gerekce || []).join(', ')}</span>
                  </p>
                ))}
                {!ham.slayt && <p className="m-0 text-[13px] text-ink-3">Eşleşme yok</p>}
                <p className="m-0 text-[13px]">
                  <b>Öğren:</b> {kay.ogren ? `${kay.ogren.deckTitle} · slayt ${kay.ogren.slideNumber} (${kay.ogren.guven}, ${kay.ogren.skor})` : '—'}
                </p>
              </div>
              <div className={card}>
                <div className="flex items-center justify-between gap-2"><h3 className={h3}>Kısaltmalar · terimler</h3><SecActions k="kisaltmalar" /></div>
                <p className="m-0 text-[13px]">
                  {Object.entries(ham.faz6_5?.kisaltmalar || {}).map(([k, v]) => `${k} = ${v}`).join(' · ') || 'Kısaltma yok'}
                </p>
                <p className="m-0 text-[13px] text-ink-2">{[...(ham.faz6_5?.terimler || []), ...(ham.faz5?.terimler || [])].join(', ') || '—'}</p>
              </div>
              <div className={card}>
                <div className="flex items-center justify-between gap-2"><h3 className={h3}>Faz 13 varlıkları ({(kay.varliklar_tum || []).length})</h3><SecActions k="varliklar" /></div>
                <div className="flex flex-wrap gap-1.5">
                  {(kay.varliklar_tum || []).map((v: any, i: number) => (
                    <span
                      key={i}
                      title={`${v.kaynak}${v.tur ? ' · ' + v.tur : ''}`}
                      className={`px-2 py-0.5 rounded-full text-[12px] ${v.kavram ? 'bg-ok-soft text-ok' : 'bg-canvas text-ink-3'}`}
                    >
                      {v.ad || v.metin}
                    </span>
                  ))}
                </div>
                <p className="m-0 text-[11.5px] text-ink-3">Yeşil: kimlikli (sitede görünür) · gri: kimliksiz GLiNER tahmini (gizli)</p>
              </div>
              <div className={card}>
                <div className="flex items-center justify-between gap-2"><h3 className={h3}>Ayırıcı tanı (Faz 6) · {ham.faz6 ? (ham.faz6.dogrulanmadi ? 'doğrulanmadı' : 'materyalle desteklenen') : '—'}</h3><SecActions k="faz6" /></div>
                {(ham.faz6?.ayirici_tani || []).map((d: any) => (
                  <p key={d.hastalik} className="m-0 text-[13px]"><b>{d.hastalik}</b> — {d.ozellik}</p>
                ))}
              </div>
              <div className={card}>
                <h3 className={h3}>Karantina</h3>
                {kay.karantina ? <Json value={kay.karantina} /> : <p className="m-0 text-[13px] text-ink-3">Karantinada değil</p>}
              </div>
            </div>
          )}

          <section className="ms-dsec">
            <h3>Elle düzelt</h3>
            <div className="flex flex-wrap gap-x-4 gap-y-1.5">
              {HIDEABLE.map(([k, label]) => (
                <label key={k} className="inline-flex items-center gap-1.5 text-[13px] cursor-pointer">
                  <input
                    className="w-[15px] h-[15px] accent-accent"
                    type="checkbox"
                    checked={form.gizle.includes(k)}
                    onChange={(e) => setForm((f) => ({ ...f, gizle: e.target.checked ? [...f.gizle, k] : f.gizle.filter((x) => x !== k) }))}
                  />
                  {label} gizle
                </label>
              ))}
            </div>
            <div className="grid gap-2 sm:grid-cols-4">
              <input className={input} placeholder="Kurul" inputMode="numeric" value={form.kazanim?.kurul ?? ''} onChange={(e) => setForm((f) => ({ ...f, kazanim: { ...f.kazanim, kurul: e.target.value ? Number(e.target.value) : undefined } }))} />
              <input className={input} placeholder="Ders" value={form.kazanim?.ders || ''} onChange={(e) => setForm((f) => ({ ...f, kazanim: { ...f.kazanim, ders: e.target.value } }))} />
              <input className={input} placeholder="Konu" value={form.kazanim?.konu || ''} onChange={(e) => setForm((f) => ({ ...f, kazanim: { ...f.kazanim, konu: e.target.value } }))} />
              <input className={input} placeholder="Kazanım" value={form.kazanim?.kazanim || ''} onChange={(e) => setForm((f) => ({ ...f, kazanim: { ...f.kazanim, kazanim: e.target.value } }))} />
            </div>
            <textarea className={`${input} min-h-[64px] font-mono`} placeholder={'Slaytlar: her satıra "kaynak | sayfa | alıntı (isteğe bağlı)"'} value={form.slaytlar} onChange={(e) => setForm((f) => ({ ...f, slaytlar: e.target.value }))} />
            <textarea className={`${input} min-h-[48px] font-mono`} placeholder={'Kısaltmalar: her satıra "KISALTMA = açılım"'} value={form.kisaltmalar} onChange={(e) => setForm((f) => ({ ...f, kisaltmalar: e.target.value }))} />
            <input className={input} placeholder="Not (neden düzeltildi)" value={form.not} onChange={(e) => setForm((f) => ({ ...f, not: e.target.value }))} />
            <div className="flex flex-wrap gap-2">
              <button type="button" disabled={busy !== ''} onClick={() => save(false)} className="ms-btn is-primary">
                <Save /> Düzeltmeyi kaydet
              </button>
              <button type="button" disabled={busy !== '' || !detail.duzeltme} onClick={() => save(true)} className="ms-btn is-ghost">
                <RotateCcw /> Tüm elle düzeltmeleri kaldır
              </button>
            </div>
          </section>

          <section className="ms-dsec">
            <h3>Arama testi · ders slaytları, BM25 + temiz ders materyali</h3>
            <textarea className={`${input} min-h-[56px]`} value={query} onChange={(e) => setQuery(e.target.value)} />
            <button type="button" disabled={busy !== ''} onClick={runTest} className="ms-btn self-start">
              <FlaskConical /> {busy === 'test' ? 'Aranıyor…' : 'Testi çalıştır'}
            </button>
            {test && (
              <ol className="m-0 pl-5 flex flex-col gap-1.5 text-[13px]">
                {test.sonuclar.map((r, i) => (
                  <li key={i}>
                    <b>{r.baslik}</b> {r.sayfa != null && <span className="text-ink-3">· s.{r.sayfa}</span>} <span className="text-ink-3">· {r.skor}</span>
                    {faz11Keys.has(`${fold(r.baslik)}#${r.sayfa}`) && <span className="ml-1.5 ms-tag is-ok">Faz 11 ile aynı</span>}
                    <div className="text-ink-2 text-[12.5px]">{r.metin}</div>
                  </li>
                ))}
              </ol>
            )}
          </section>

          <section className="ms-dsec">
            <h3>Sitede görünen · önizleme</h3>
            <QuestionInsightsPanel key={`${selId}-${previewKey}`} questionId={selId!} />
          </section>
        </>
      )}
      </Drawer>
    </div>
  );
};
