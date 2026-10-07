import React, { useEffect, useMemo, useState } from 'react';
import { Search, Save, RotateCcw, FlaskConical, Code2 } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { QuestionInsightsPanel, clearInsightsCache } from '../QuestionInsightsPanel';
import { toast } from '../ui/Toast';

/**
 * "Faz verileri": bir çıkmış sorunun tüm faz çıktılarını (Faz 5/6/6.5/8/11/13, Öğren, sınav başlığı müfredatı,
 * karantina) gösterir; elle düzeltme kaydeder (faz çıktısına dokunmaz, okuma sırasında uygulanır);
 * arama motorunu soruyla çalıştırıp Faz 11 eşleşmesiyle karşılaştırır; sitede görüneni önizler.
 */
type Slide = { kaynak: string; sayfa: number; alinti?: string };
type Override = {
  gizle?: string[];
  slaytlar?: Slide[];
  kazanim?: { kurul?: number; ders?: string; konu?: string; kazanim?: string };
  kisaltmalar?: Record<string, string>;
  not?: string;
  guncelleyen?: string;
  guncelleme?: string;
};
type Detail = { id: string; ham: any; gorunen: any; duzeltme: Override | null; kayitlar: Record<string, any> };
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
const card = 'rounded-xl border border-line bg-white p-3.5 flex flex-col gap-2';
const h3 = 'm-0 text-[12px] font-semibold uppercase tracking-wide text-ink-3';
const input = 'w-full rounded-lg border border-line bg-white px-2.5 py-1.5 text-[13.5px]';

function Json({ value }: { value: any }) {
  return (
    <pre className="m-0 max-h-72 overflow-auto rounded-lg bg-canvas p-2 text-[11.5px] leading-snug whitespace-pre-wrap break-words">
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
    <div className="flex flex-col gap-4">
      <div className={card}>
        <label className="flex items-center gap-2 rounded-lg border border-line px-2.5 h-10">
          <Search className="w-4 h-4 text-ink-3" />
          <input
            value={term}
            onChange={(e) => setTerm(e.target.value)}
            placeholder="Soru numarası (#1529), kimlik ya da soru metninden bir parça"
            className="flex-1 bg-transparent outline-none text-[14px]"
          />
        </label>
        {matches.length > 0 && (
          <ul className="m-0 p-0 list-none flex flex-col max-h-64 overflow-auto">
            {matches.map((q) => (
              <li key={q.id}>
                <button
                  type="button"
                  onClick={() => load(q.id)}
                  className={`w-full text-left px-2 py-1.5 rounded-lg text-[13px] hover:bg-canvas ${q.id === selId ? 'bg-canvas font-semibold' : ''}`}
                >
                  <span className="font-mono text-ink-3">#{q.questionNumber}</span> {stemOf(q).slice(0, 120)}
                </button>
              </li>
            ))}
          </ul>
        )}
        {term.trim().length >= 2 && matches.length === 0 && <p className="m-0 text-[13px] text-ink-3">Eşleşen soru yok.</p>}
      </div>

      {detail && (
        <>
          <div className={card}>
            <div className="flex items-start justify-between gap-2">
              <p className="m-0 text-[14px] font-semibold text-ink">
                <span className="font-mono text-ink-3">#{selQ?.questionNumber}</span> {stemOf(selQ)}
              </p>
              <button type="button" onClick={() => setShowRaw((v) => !v)} className="shrink-0 inline-flex items-center gap-1 text-[12.5px] text-ink-3">
                <Code2 className="w-4 h-4" /> {showRaw ? 'Kartlar' : 'Ham JSON'}
              </button>
            </div>
            {detail.gorunen?.elle_duzeltildi && (
              <p className="m-0 text-[12.5px] text-warn">
                Elle düzeltilmiş · {detail.duzeltme?.guncelleyen} · {detail.duzeltme?.guncelleme?.slice(0, 16).replace('T', ' ')}
              </p>
            )}
          </div>

          {showRaw ? (
            <div className="grid gap-3 md:grid-cols-2">
              <div className={card}><h3 className={h3}>Faz çıktısı (ham)</h3><Json value={ham} /></div>
              <div className={card}><h3 className={h3}>Diğer kayıtlar</h3><Json value={kay} /></div>
            </div>
          ) : (
            <div className="grid gap-3 md:grid-cols-2">
              <div className={card}>
                <h3 className={h3}>Müfredat</h3>
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
                <h3 className={h3}>Slaytlar (Faz 11) · güven {ham.slayt?.guven || '—'}</h3>
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
                <h3 className={h3}>Kısaltmalar · terimler</h3>
                <p className="m-0 text-[13px]">
                  {Object.entries(ham.faz6_5?.kisaltmalar || {}).map(([k, v]) => `${k} = ${v}`).join(' · ') || 'Kısaltma yok'}
                </p>
                <p className="m-0 text-[13px] text-ink-2">{[...(ham.faz6_5?.terimler || []), ...(ham.faz5?.terimler || [])].join(', ') || '—'}</p>
              </div>
              <div className={card}>
                <h3 className={h3}>Faz 13 varlıkları ({(kay.varliklar_tum || []).length})</h3>
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
                <h3 className={h3}>Ayırıcı tanı (Faz 6) · {ham.faz6 ? (ham.faz6.dogrulanmadi ? 'doğrulanmadı' : 'materyalle desteklenen') : '—'}</h3>
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

          <div className={card}>
            <h3 className={h3}>Elle düzelt</h3>
            <div className="flex flex-wrap gap-x-4 gap-y-1.5">
              {HIDEABLE.map(([k, label]) => (
                <label key={k} className="inline-flex items-center gap-1.5 text-[13px]">
                  <input
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
              <button type="button" disabled={busy !== ''} onClick={() => save(false)} className="h-10 px-3.5 rounded-lg bg-accent text-white text-[13.5px] font-semibold inline-flex items-center gap-1.5 disabled:opacity-60">
                <Save className="w-4 h-4" /> Kaydet
              </button>
              <button type="button" disabled={busy !== '' || !detail.duzeltme} onClick={() => save(true)} className="h-10 px-3.5 rounded-lg border border-line text-[13.5px] inline-flex items-center gap-1.5 disabled:opacity-50">
                <RotateCcw className="w-4 h-4" /> Düzeltmeyi kaldır
              </button>
            </div>
          </div>

          <div className={card}>
            <h3 className={h3}>Arama testi (ders slaytları, BM25 + temiz ders materyali)</h3>
            <textarea className={`${input} min-h-[56px]`} value={query} onChange={(e) => setQuery(e.target.value)} />
            <button type="button" disabled={busy !== ''} onClick={runTest} className="self-start h-10 px-3.5 rounded-lg border border-line text-[13.5px] inline-flex items-center gap-1.5 disabled:opacity-60">
              <FlaskConical className="w-4 h-4" /> {busy === 'test' ? 'Aranıyor…' : 'Testi çalıştır'}
            </button>
            {test && (
              <ol className="m-0 pl-5 flex flex-col gap-1.5 text-[13px]">
                {test.sonuclar.map((r, i) => (
                  <li key={i}>
                    <b>{r.baslik}</b> {r.sayfa != null && <span className="text-ink-3">· s.{r.sayfa}</span>} <span className="text-ink-3">· {r.skor}</span>
                    {faz11Keys.has(`${fold(r.baslik)}#${r.sayfa}`) && <span className="ml-1.5 px-1.5 rounded bg-ok-soft text-ok text-[11.5px] font-semibold">Faz 11 ile aynı</span>}
                    <div className="text-ink-2 text-[12.5px]">{r.metin}</div>
                  </li>
                ))}
              </ol>
            )}
          </div>

          <div className={card}>
            <h3 className={h3}>Sitede görünen (önizleme)</h3>
            <QuestionInsightsPanel key={`${selId}-${previewKey}`} questionId={selId!} />
          </div>
        </>
      )}
    </div>
  );
};
