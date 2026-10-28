import React, { useEffect, useState } from 'react';
import { SayfaBasligi, VeriTablosu, AyrintiCekmecesi, Rozet, Hata, adminIstek, bildir, onayIste, useAdminSorgu, zamanMetni } from '../kit';
import type { SayfaProps } from '../menu';
import './ortak/ts16.css';

type Betik = { name: string; title: string; category: string; description: string; defaultArgs: string; danger: boolean; runtime: string; modifiedAt: string | null; isCustom: boolean };
type Hat = { id: string; title: string; description: string; steps: { script: string; title: string }[] };
type Is = { id: string; name: string; title: string; type: string; status: string; startedAt: string; durationMs: number; exitCode?: number; requestedBy?: string; lastLog: string; logs?: string[] };
type Liste = { scripts: Betik[]; pipelines: Hat[]; jobs: { active: Is[]; history: Is[] } };

/** LLM/bulut API kullanabilecek betik (kural 20): ek onay ve uyarı */
const llmMi = (b: { name: string; category?: string; description?: string }) =>
  b.category === 'AI & Doğrulama' || /\b(ai|llm|claude|gemini|groq|openrouter|opencode|deepseek|phase14|faz14)\b|_ai_|ai-|-ai/i.test(`${b.name} ${b.description || ''}`);
// H182: tehlike tespiti ad regex'ine dayanıyordu (adında "sil/reset" geçmeyen yazıcı betik onaysız çalışıyordu). Artık tersine:
// yalnız salt okunur olduğu bilinen betikler güvenli; bilinmeyen/sınıflanmamış/özel her betik varsayılan TEHLİKELİ (yazılı onay).
const GUVENLI_BETIK = new Set([
  'detect-database-updates.mjs', 'detect-faulty-ocr.mjs', 'inspect-sources.mjs', 'check-online-status.ts',
  'test-drive-folders.mjs', 'test-sample-pdfs.mjs', 'test-filter-donem3.mjs',
]);
const tehlikeMi = (b: Betik) => b.danger || b.isCustom || !GUVENLI_BETIK.has(b.name);

/** Sistem › Betikler — betik ve zincir çalıştırma, iş geçmişi ve günlük. Tehlikeli ve LLM betikleri yazılı çift onay ister. */
export default function Betikler(_p: SayfaProps) {
  const s = useAdminSorgu<Liste>('/api/admin/scripts/list', { aralikMs: 5000 });
  const [acik, setAcik] = useState<Betik | null>(null);
  const [arg, setArg] = useState('');
  const [isId, setIsId] = useState<string | null>(null);
  useEffect(() => { setArg(acik?.defaultArgs || ''); }, [acik]);

  const calistir = async (b: Betik) => {
    const llm = llmMi(b), tehlike = tehlikeMi(b);
    const ok = await onayIste({
      baslik: `${b.title} çalıştırılsın mı?`, tehlikeli: llm || tehlike, onayMetni: 'Çalıştır',
      yazilacak: llm || tehlike ? 'CALISTIR' : undefined,
      aciklama: <>
        <code>{b.name} {arg}</code>
        {llm && <><br /><b>LLM/API kullanabilir.</b> Kural 20: yalnız elle başlatılır; betik llm_kilit ile korunuyorsa panel bayrağı olmadan çıkış 75 verir.</>}
        {tehlike && <><br /><b>Tehlikeli{!b.danger && !b.isCustom ? ' (salt okunur olduğu doğrulanmadı)' : ''}:</b> veri silebilir, ezebilir ya da dışarı gönderebilir.</>}
      </>,
    });
    if (!ok) return;
    try { const r = await adminIstek<any>('/api/admin/scripts/run', { yontem: 'POST', govde: { scriptName: b.name, args: arg } }); bildir(r.message || 'Başlatıldı.', 'iyi'); setIsId(r.job?.id || null); void s.yenile(); }
    catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  const hatCalistir = async (h: Hat) => {
    const ok = await onayIste({ baslik: `${h.title} zinciri çalıştırılsın mı?`, tehlikeli: true, yazilacak: 'CALISTIR', onayMetni: 'Zinciri çalıştır',
      aciklama: <>{h.description}<ol>{h.steps.map((x) => <li key={x.script}>{x.title} <code>{x.script}</code></li>)}</ol></> });
    if (!ok) return;
    try { const r = await adminIstek<any>('/api/admin/scripts/pipeline/run', { yontem: 'POST', govde: { pipelineId: h.id } }); bildir(r.message || 'Başlatıldı.', 'iyi'); setIsId(r.job?.id || null); }
    catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  const etkin = s.veri?.jobs.active || [];
  return (
    <>
      <SayfaBasligi baslik="Betikler" aciklama="Sunucudaki bakım betikleri ve zincirleri. Tehlikeli ya da LLM kullanan betikler yazılı onay ister; her çalıştırma denetim kaydına düşer." />
      {s.hata && <Hata hata={s.hata} yenile={s.yenile} />}
      {etkin.length > 0 && (
        <section className="m16-kart" style={{ marginBottom: 12 }}>
          <h2>Çalışan işler ({etkin.length})</h2>
          <ul className="m16-liste">{etkin.map((j) => (
            <li key={j.id}><Rozet ton="vurgu">çalışıyor</Rozet><span className="m16-kisalt">{j.title} — {j.lastLog}</span><time>{Math.round(j.durationMs / 1000)} sn</time>
              <button type="button" className="m16-btn hayalet" onClick={() => setIsId(j.id)}>Günlük</button></li>
          ))}</ul>
        </section>
      )}
      <VeriTablosu<Betik>
        kimlik="sistem-betik" ogeler={s.veri?.scripts || []} aramaYeri="Betik adı ya da açıklama…" satirKimligi={(b) => b.name}
        etkin={acik?.name || null} satirTikla={setAcik}
        suzgecler={[{ anahtar: 'category', etiket: 'Kategori', secenekler: [...new Set((s.veri?.scripts || []).map((b) => b.category))].map((c) => ({ deger: c, etiket: c })) }]}
        sutunlar={[
          { anahtar: 'title', baslik: 'Betik', sirala: true, genislik: 'minmax(200px,2fr)', deger: (b) => `${b.title} ${b.name}`, hucre: (b) => <span className="m16-kisalt" title={b.name}>{b.title}</span> },
          { anahtar: 'category', baslik: 'Kategori', sirala: true, genislik: 'minmax(120px,1fr)' },
          { anahtar: 'risk', baslik: 'Risk', genislik: '110px', deger: (b) => `${llmMi(b) ? 'llm' : ''} ${tehlikeMi(b) ? 'tehlikeli' : ''}`, hucre: (b) => <>{llmMi(b) && <Rozet ton="uyari">LLM</Rozet>} {tehlikeMi(b) && <Rozet ton="kotu">Tehlikeli</Rozet>}</> },
          { anahtar: 'runtime', baslik: 'Çalışma', genislik: '80px', gizli: true },
          { anahtar: 'description', baslik: 'Açıklama', genislik: 'minmax(200px,3fr)', gizli: true, hucre: (b) => <span className="m16-kisalt">{b.description}</span> },
        ]}
      />
      <section className="m16-kart" style={{ marginTop: 12 }}>
        <h2>Zincirler</h2>
        <ul className="m16-liste">{(s.veri?.pipelines || []).map((h) => (
          <li key={h.id}><span className="m16-kisalt" title={h.description}>{h.title}</span><small>{h.steps.length} adım</small>
            <button type="button" className="m16-btn hayalet" onClick={() => hatCalistir(h)}>Çalıştır…</button></li>
        ))}</ul>
      </section>
      <section className="m16-kart" style={{ marginTop: 12 }}>
        <h2>Son işler</h2>
        <ul className="m16-liste">{(s.veri?.jobs.history || []).map((j) => (
          <li key={j.id}><Rozet ton={j.status === 'completed' ? 'iyi' : j.status === 'failed' ? 'kotu' : 'notr'}>{j.status}</Rozet>
            <span className="m16-kisalt">{j.title}</span><time>{zamanMetni(j.startedAt)}</time>
            <button type="button" className="m16-btn hayalet" onClick={() => setIsId(j.id)}>Günlük</button></li>
        ))}</ul>
      </section>
      <AyrintiCekmecesi acik={!!acik} kapat={() => setAcik(null)} baslik={acik?.title || ''} altBaslik={acik?.name} kayit={acik || undefined}
        eylemler={acik && <button type="button" className={`m16-btn ${tehlikeMi(acik) || llmMi(acik) ? 'tehlike' : 'birincil'}`} onClick={() => calistir(acik)}>Çalıştır…</button>}>
        {acik && (
          <>
            <p>{acik.description || 'Açıklama yok.'}</p>
            <dl className="m16-satirlar"><dt>Kategori</dt><dd>{acik.category}</dd><dt>Çalışma</dt><dd>{acik.runtime}</dd>{acik.modifiedAt && <><dt>Değişti</dt><dd>{zamanMetni(acik.modifiedAt)}</dd></>}</dl>
            <label className="m16-alan" style={{ marginTop: 8 }}><span>Argümanlar</span>
              <input className="m16-girdi" value={arg} onChange={(e) => setArg(e.target.value)} spellCheck={false} /></label>
          </>
        )}
      </AyrintiCekmecesi>
      <IsGunlugu id={isId} kapat={() => setIsId(null)} />
    </>
  );
}

function IsGunlugu({ id, kapat }: { id: string | null; kapat: () => void }) {
  const s = useAdminSorgu<{ job: Is }>(id ? `/api/admin/scripts/jobs/${id}` : null, { aralikMs: id ? 1500 : undefined });
  const j = s.veri?.job;
  const durdur = async () => {
    if (!j || !(await onayIste({ baslik: 'İş durdurulsun mu?', tehlikeli: true, onayMetni: 'Durdur' }))) return;
    try { await adminIstek(`/api/admin/scripts/jobs/${j.id}/kill`, { yontem: 'POST', govde: {} }); bildir('Durduruldu.', 'iyi'); void s.yenile(); }
    catch (e: any) { bildir(e?.message || String(e), 'kotu'); }
  };
  return (
    <AyrintiCekmecesi acik={!!id} kapat={kapat} genis baslik={j?.title || 'İş'} altBaslik={j ? `${j.status} · ${zamanMetni(j.startedAt)}` : ''}
      eylemler={j?.status === 'running' && <button type="button" className="m16-btn tehlike" onClick={durdur}>Durdur</button>}>
      <pre className="m16-ts-log">{(j?.logs || []).join('\n') || 'Günlük yok.'}</pre>
    </AyrintiCekmecesi>
  );
}
