import React, { Suspense, useEffect, useMemo, useState } from 'react';
import { BookOpenCheck, CheckCircle2, ClipboardList, Eye, FileWarning, RefreshCw, RotateCcw, XCircle, PenLine, Library } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { toast } from '../ui/Toast';
import { NoteMarkdown } from '../ui/NoteMarkdown';
import { ChipBar, EmptyState, Panel } from './consoleUi';

const LessonPlayer = React.lazy(() => import('../learn/lesson/LessonPlayer').then((m) => ({ default: m.LessonPlayer })));

/**
 * "Yeni dersler": Oracle'daki ders işçisinin (scripts/ders_isci) Drive'dan yakalayıp Claude ile ürettiği ders paketleri.
 * Yönetici taslağı inceler (rapor, deste önizlemesi, sorular, sözlük, hastalıklar, bilgi havuzu, çıkmış bağları, kitaptan
 * tamamlanan bilgiler) ve karar verir. Karar taslağa yazılır; yayına birleştirme ayrı adımdır (onaylananlar).
 * Veri: /api/admin/ders-isci/* (sunucu → işçinin iç API'si).
 */
type Program = { kurul?: number; ders?: string; konu?: string; ogretim_uyesi?: string; tarih?: string; guven?: string; skor?: number };
type Karar = { karar: 'onayla' | 'reddet' | 'duzelt'; not?: string; kim?: string; zaman?: number } | null;
type Taslak = {
  is_id: string;
  durum: string;
  ozet: string;
  ders_id?: string;
  deste_id?: string;
  mod?: 'yeni' | 'guncelleme';
  uyari?: string;
  pdf?: string;
  program: Program;
  sayilar: Record<string, number>;
  denetim_hata?: number;
  referans?: number;
  karar: Karar;
  zaman?: number;
  yayin?: { durum?: string; hatalar?: string[]; yayin_zamani?: string; site_derlendi?: boolean } | null;
};
type Ayrinti = Taslak & { rapor: string; denetim: { hatalar?: string[]; uyarilar?: string[]; referansla_tamamlanan?: string[] }; dosyalar: string[] };
type Sekme = 'rapor' | 'deste' | 'sorular' | 'sozluk' | 'hastaliklar' | 'havuz' | 'cikmis' | 'kaynak';
type Filtre = 'bekleyen' | 'karar' | 'hepsi';

const DURUM: Record<string, { label: string; cls: string }> = {
  onay_bekliyor: { label: 'Onay bekliyor', cls: 'is-warn' },
  isleniyor: { label: 'İşleniyor', cls: '' },
  onayla: { label: 'Onaylandı', cls: 'is-ok' },
  reddet: { label: 'Reddedildi', cls: 'is-bad' },
  duzelt: { label: 'Düzeltme istendi', cls: 'is-warn' },
  yayinlandi: { label: 'Yayınlandı', cls: 'is-ok' },
  reddedildi: { label: 'Reddedildi', cls: 'is-bad' },
};

const ManageDersRevizeSection = React.lazy(() => import('./ManageDersRevizeSection').then((m) => ({ default: m.ManageDersRevizeSection })));

type Kategori = 'otomatik' | 'revize';

/** Yeni dersler: Otomatik (Oracle'daki işçi, Drive'dan) ve Revize (cihazda yeniden üretilen mevcut dersler). */
export const ManageDersIsciSection: React.FC<{ adminEmail: string }> = ({ adminEmail }) => {
  const [kategori, setKategori] = useState<Kategori>(() => {
    try {
      return (localStorage.getItem('manage:dersIsciKategori') as Kategori) || 'otomatik';
    } catch {
      return 'otomatik';
    }
  });
  const sec = (k: Kategori) => {
    setKategori(k);
    try {
      localStorage.setItem('manage:dersIsciKategori', k);
    } catch {}
  };
  return (
    <div className="flex flex-col gap-3">
      <ChipBar<Kategori>
        label="Ders işçisi kategorisi"
        value={kategori}
        onChange={sec}
        options={[
          { id: 'otomatik', label: 'Otomatik Ders İşçisi' },
          { id: 'revize', label: 'Revize Ders İşçisi' },
        ]}
      />
      {kategori === 'otomatik' ? (
        <OtomatikDersIsci adminEmail={adminEmail} />
      ) : (
        <Suspense fallback={<p className="text-sm text-ink-2">Yükleniyor…</p>}>
          <ManageDersRevizeSection adminEmail={adminEmail} />
        </Suspense>
      )}
    </div>
  );
};

const OtomatikDersIsci: React.FC<{ adminEmail: string }> = ({ adminEmail }) => {
  const headers = useMemo(() => ({ 'Content-Type': 'application/json', 'x-admin-email': adminEmail || '' }), [adminEmail]);
  const [liste, setListe] = useState<Taslak[] | null>(null);
  const [hata, setHata] = useState<string | null>(null);
  const [ozet, setOzet] = useState<{ sayim?: Record<string, number>; uretim?: string } | null>(null);
  const [secili, setSecili] = useState<string | null>(null);
  const [ayr, setAyr] = useState<Ayrinti | null>(null);
  const [sekme, setSekme] = useState<Sekme>('rapor');
  const [filtre, setFiltre] = useState<Filtre>('bekleyen');
  const [dosya, setDosya] = useState<Record<string, any>>({});
  const [onizle, setOnizle] = useState<any | null>(null);
  const [not, setNot] = useState('');
  const [busy, setBusy] = useState(false);

  const api = (yol: string, init?: RequestInit) => safeJsonFetch<any>(`/api/admin/ders-isci${yol}`, { headers, ...init });

  const yukle = async () => {
    setHata(null);
    const [t, c] = await Promise.all([api('/taslaklar'), api('/checklist')]);
    if (!t.ok) {
      setHata((t.data as any)?.hata || 'Ders işçisine ulaşılamıyor.');
      setListe([]);
      return;
    }
    setListe(t.data || []);
    if (c.ok && c.data) setOzet({ sayim: c.data.sayim, uretim: c.data.uretim });
  };
  useEffect(() => {
    yukle();
  }, []);

  useEffect(() => {
    if (!secili) return;
    setAyr(null);
    setDosya({});
    setNot('');
    setSekme('rapor');
    api(`/taslak/${secili}`).then((r) => (r.ok ? setAyr(r.data) : toast.error('Taslak alınamadı.')));
  }, [secili]);

  const dosyaAl = async (ad: string) => {
    if ((dosya[ad] !== undefined && dosya[ad] !== null) || !secili) return dosya[ad];
    const iste = () => fetch(`/api/admin/ders-isci/taslak/${secili}/dosya/${ad}`, { headers }).catch(() => null);
    let r = await iste();
    if (!r || !r.ok) {
      await new Promise((t) => setTimeout(t, 1500)); // geçici aksaklık (yeniden başlatma, ağ): bir kez daha dene
      r = await iste();
    }
    if (!r || !r.ok) {
      setDosya((d) => ({ ...d, [ad]: null })); // önbelleğe "kalıcı" yazılmaz: sekmeye/düğmeye yeniden basınca tekrar denenir
      return null;
    }
    const txt = await r.text();
    const v = ad.endsWith('.jsonl') ? txt.split('\n').filter(Boolean).map((x) => JSON.parse(x)) : ad.endsWith('.json') ? JSON.parse(txt) : txt;
    setDosya((d) => ({ ...d, [ad]: v }));
    return v;
  };
  useEffect(() => {
    const ad = { sorular: 'ornek_sorular.json', sozluk: 'sozluk.json', hastaliklar: 'hastaliklar.json', havuz: 'bilgi_havuzu.jsonl', cikmis: 'cikmis_baglantilari.json' }[sekme as string];
    if (ad) dosyaAl(ad);
  }, [sekme, secili]);

  const karar = async (k: 'onayla' | 'reddet' | 'duzelt') => {
    if (!secili) return;
    if (k !== 'onayla' && !not.trim()) return toast.error('Reddetme ya da düzeltme için kısa bir not yaz.');
    setBusy(true);
    const r = await api(`/taslak/${secili}/karar`, { method: 'POST', body: JSON.stringify({ karar: k, not }) });
    setBusy(false);
    if (!r.ok) return toast.error((r.data as any)?.hata || 'Karar kaydedilemedi.');
    toast.success(k === 'onayla' ? 'Onaylandı; yayına birleştirme sırasına alındı.' : k === 'reddet' ? 'Reddedildi.' : 'Düzeltme istendi.');
    await yukle();
    api(`/taslak/${secili}`).then((x) => x.ok && setAyr(x.data));
  };

  const yenidenGonder = async () => {
    if (!secili) return;
    setBusy(true);
    const r = await api(`/taslak/${secili}/yeniden`, { method: 'POST', body: '{}' });
    setBusy(false);
    if (!r.ok) return toast.error((r.data as any)?.hata || 'Yeniden gönderilemedi.');
    toast.success('Yeniden gönderildi; sunucu en geç 10 dakika içinde yeniden dener.');
    await yukle();
    api(`/taslak/${secili}`).then((x) => x.ok && setAyr(x.data));
  };

  // yayınlanan taslak (scripts/ders_isci/yayinla.py) kararın önüne geçer; onaylı ama aktarılmamışsa "Onaylandı"
  const durumAnahtari = (t: Taslak) => (t.durum === 'yayinlandi' ? t.durum : t.karar?.karar ? t.karar.karar : t.durum);
  const gorunen = (liste || []).filter((t) =>
    filtre === 'hepsi' ? true : filtre === 'bekleyen' ? !t.karar && t.durum === 'onay_bekliyor' : !!t.karar,
  );

  const s = ayr?.sayilar || {};
  return (
    <div className="flex flex-col gap-3">
      <Panel
        title="Otomatik Ders İşçisi"
        icon={BookOpenCheck}
        count={liste ? liste.length : undefined}
        desc="Drive'a eklenen ders PDF'lerinden ders işçisinin ürettiği paketler. İncele, önizle, karar ver; onaylananlar yayına birleştirilir."
        tools={
          <button type="button" className="ms-btn is-sm" onClick={yukle}>
            <RefreshCw aria-hidden /> Yenile
          </button>
        }
      >
        {ozet?.sayim && (
          <p className="text-sm text-ink-2 mb-2">
            <b>2026-27 checklist</b> ({ozet.uretim}): tamam {ozet.sayim.tamam_2627 || 0} · onay bekliyor {ozet.sayim.onay_bekliyor || 0} ·
            kuyrukta {(ozet.sayim.kuyrukta || 0) + (ozet.sayim.isleniyor || 0)} · yenilenmeli {ozet.sayim.yenilenmeli || 0} · işlenmeli{' '}
            {ozet.sayim.islenmeli || 0} · geçen yıl kaynaklı {ozet.sayim.gecen_yil_kaynakli || 0} · PDF bekleniyor {ozet.sayim.pdf_bekleniyor || 0}
          </p>
        )}
        <ChipBar<Filtre>
          label="Taslak süzgeci"
          value={filtre}
          onChange={setFiltre}
          options={[
            { id: 'bekleyen', label: 'Onay bekleyen', n: (liste || []).filter((t) => !t.karar && t.durum === 'onay_bekliyor').length },
            { id: 'karar', label: 'Karar verilen', n: (liste || []).filter((t) => !!t.karar).length },
            { id: 'hepsi', label: 'Hepsi', n: (liste || []).length },
          ]}
        />
        {hata && <EmptyState icon={FileWarning} title="Ders işçisine ulaşılamıyor">{hata}</EmptyState>}
        {!hata && liste && gorunen.length === 0 && <EmptyState icon={ClipboardList} title="Bu süzgeçte taslak yok" />}
        <ul className="flex flex-col gap-2 mt-2">
          {gorunen.map((t) => {
            const d = DURUM[durumAnahtari(t)] || { label: t.durum, cls: '' };
            return (
              <li key={t.is_id}>
                <button
                  type="button"
                  onClick={() => setSecili(t.is_id)}
                  aria-pressed={secili === t.is_id}
                  className={`ms-panel w-full text-left p-3 ${secili === t.is_id ? 'is-on' : ''}`}
                >
                  <div className="flex flex-wrap items-center gap-2">
                    <b className="min-w-0">{t.program?.konu || t.ders_id}</b>
                    <span className="ms-tag">{t.program?.ders}</span>
                    <span className="ms-tag">K{t.program?.kurul}</span>
                    <span className="ms-tag">{t.mod === 'guncelleme' ? `güncelleme · ${t.deste_id}` : 'yeni ders'}</span>
                    <span className={`ms-tag ${d.cls}`}>{d.label}</span>
                  </div>
                  <p className="text-sm text-ink-2 mt-1">{t.ozet}</p>
                  {t.uyari && <p className="text-sm text-warn mt-1">⚠ {t.uyari}</p>}
                </button>
              </li>
            );
          })}
        </ul>
      </Panel>

      {secili && (
        <Panel
          title={ayr?.program?.konu || 'Taslak yükleniyor…'}
          icon={Library}
          desc={
            ayr
              ? `${ayr.program?.ders || ''} · Kurul ${ayr.program?.kurul ?? '?'} · ${ayr.program?.ogretim_uyesi || 'hoca belirsiz'} · program eşleşmesi: ${ayr.program?.guven || '?'} · PDF: ${ayr.pdf || ''}`
              : undefined
          }
        >
          {ayr && (
            <>
              <p className="text-sm mb-2">
                <b>{s.slayt || 0}</b> slayt · <b>{s.soru || 0}</b> soru · <b>{s.terim || 0}</b> terim · <b>{s.hastalik || 0}</b> hastalık ·{' '}
                <b>{s.havuz || 0}</b> bilgi · <b>{s.bag || 0}</b> çıkmış bağı · <b>{ayr.referans || 0}</b> kitaptan tamamlanan · denetim{' '}
                <b className={ayr.denetim_hata ? 'text-bad' : 'text-ok'}>{ayr.denetim_hata ?? '?'} hata</b>
              </p>
              {ayr.uyari && <p className="text-sm text-warn mb-2">⚠ {ayr.uyari}</p>}
              <ChipBar<Sekme>
                label="Taslak bölümleri"
                wrap
                value={sekme}
                onChange={setSekme}
                options={[
                  { id: 'rapor', label: 'Rapor' },
                  { id: 'deste', label: 'Deste', n: s.slayt },
                  { id: 'sorular', label: 'Sorular', n: s.soru },
                  { id: 'sozluk', label: 'Sözlük', n: s.terim },
                  { id: 'hastaliklar', label: 'Hastalıklar', n: s.hastalik },
                  { id: 'havuz', label: 'Bilgi havuzu', n: s.havuz },
                  { id: 'cikmis', label: 'Çıkmış bağları', n: s.bag },
                  { id: 'kaynak', label: 'Kitaptan', n: ayr.referans },
                ]}
              />
              <div className="mt-3">
                {sekme === 'rapor' && <NoteMarkdown text={ayr.rapor || '_Rapor yok._'} />}
                {sekme === 'deste' && (
                  <div className="flex flex-col gap-2">
                    <p className="text-sm text-ink-2">
                      Deste, sitedeki ders oynatıcısıyla açılır; öğrencinin göreceğinin aynısıdır. Kimlik: <code>{ayr.deste_id}</code>
                      {ayr.mod === 'guncelleme' ? ' (onaylanırsa mevcut destenin yerine geçer)' : ' (yeni deste)'}.
                    </p>
                    <button
                      type="button"
                      className="ms-btn is-primary self-start"
                      onClick={async () => {
                        const d = await dosyaAl('deck.json');
                        if (d) setOnizle(d);
                        else toast.error('Deste dosyası alınamadı.');
                      }}
                    >
                      <Eye aria-hidden /> Desteyi önizle
                    </button>
                  </div>
                )}
                {sekme === 'sorular' && <Sorular veri={dosya['ornek_sorular.json']} />}
                {sekme === 'sozluk' && <Sozluk veri={dosya['sozluk.json']} />}
                {sekme === 'hastaliklar' && <Hastaliklar veri={dosya['hastaliklar.json']} />}
                {sekme === 'havuz' && <Havuz veri={dosya['bilgi_havuzu.jsonl']} />}
                {sekme === 'cikmis' && <Cikmis veri={dosya['cikmis_baglantilari.json']} />}
                {sekme === 'kaynak' && (
                  <ul className="flex flex-col gap-1 text-sm">
                    {(ayr.denetim?.referansla_tamamlanan || []).map((r, i) => (
                      <li key={i}>📚 {r}</li>
                    ))}
                    {!ayr.denetim?.referansla_tamamlanan?.length && <li>Kitaptan tamamlanan bilgi yok; her bilgi ders PDF'inden alıntıyla doğrulandı.</li>}
                  </ul>
                )}
              </div>

              <div className="mt-4 border-t border-line pt-3 flex flex-col gap-2">
                {ayr.karar ? (
                  <>
                    <p className="text-sm">
                      Karar: <b>{DURUM[ayr.karar.karar]?.label}</b>
                      {ayr.karar.not ? ` — ${ayr.karar.not}` : ''}
                      {ayr.karar.kim ? ` (${ayr.karar.kim})` : ''}
                      {ayr.karar.karar === 'onayla' &&
                        (ayr.yayin?.durum === 'yayinlandi' && ayr.yayin.site_derlendi === false
                          ? ' · Kaynaklara yazıldı ama site derlenemedi.'
                          : ayr.durum === 'yayinlandi'
                          ? ' · Sitede yayında.'
                          : ayr.yayin?.durum === 'denetim_hatasi'
                            ? ' · Yayınlanamadı (yayın denetimi):'
                            : ' · Sunucu en geç 10 dakika içinde siteye ekler.')}
                    </p>
                    {ayr.yayin?.durum === 'denetim_hatasi' && (
                      <ul className="text-sm text-ink-2 list-disc pl-5">
                        {(ayr.yayin.hatalar || []).slice(0, 8).map((h) => (
                          <li key={h}>{h}</li>
                        ))}
                      </ul>
                    )}
                    {ayr.karar.karar === 'onayla' &&
                      ayr.yayin &&
                      (ayr.yayin.durum !== 'yayinlandi' || ayr.yayin.site_derlendi === false) && (
                        <button type="button" disabled={busy} className="ms-btn is-bad self-start" onClick={yenidenGonder}>
                          <RotateCcw aria-hidden /> {ayr.yayin.durum === 'yayinlandi' ? 'Siteyi yeniden derle' : 'Yeniden gönder'}
                        </button>
                      )}
                  </>
                ) : ayr.durum === 'onay_bekliyor' ? (
                  <>
                    <label className="text-sm text-ink-2" htmlFor="isci-not">
                      Not (reddetme ya da düzeltme için gerekli; düzeltmede işçi bu notla taslağı yeniden üretir)
                    </label>
                    <textarea id="isci-not" className="ms-input min-h-[72px]" value={not} onChange={(e) => setNot(e.target.value)} />
                    <div className="flex flex-wrap gap-2">
                      <button type="button" disabled={busy} className="ms-btn is-ok" onClick={() => karar('onayla')}>
                        <CheckCircle2 aria-hidden /> Onayla
                      </button>
                      <button type="button" disabled={busy} className="ms-btn" onClick={() => karar('duzelt')}>
                        <PenLine aria-hidden /> Düzeltme iste
                      </button>
                      <button type="button" disabled={busy} className="ms-btn is-bad" onClick={() => karar('reddet')}>
                        <XCircle aria-hidden /> Reddet
                      </button>
                    </div>
                  </>
                ) : (
                  <p className="text-sm text-ink-2">Taslak hâlâ işleniyor.</p>
                )}
              </div>
            </>
          )}
        </Panel>
      )}

      {onizle && (
        <Suspense fallback={null}>
          <LessonPlayer deck={onizle} startAt={0} onProgress={() => {}} onClose={() => setOnizle(null)} />
        </Suspense>
      )}
    </div>
  );
};

const Yukleniyor: React.FC<{ veri: any }> = ({ veri }) =>
  veri === undefined ? <p className="text-sm text-ink-2">Yükleniyor…</p> : veri === null ? <p className="text-sm text-bad">Dosya alınamadı.</p> : null;

const Kanit: React.FC<{ k?: any }> = ({ k }) =>
  !k ? null : k.referans ? (
    <span className="text-xs text-ink-3">📚 {k.referans}</span>
  ) : (
    <span className="text-xs text-ink-3">
      s.{k.sayfa}: “{k.alinti}”
    </span>
  );

export const Sorular: React.FC<{ veri: any }> = ({ veri }) => {
  if (!veri) return <Yukleniyor veri={veri} />;
  return (
    <ol className="flex flex-col gap-3">
      {(veri.sorular || []).map((q: any) => (
        <li key={q.id} className="text-sm">
          <p>
            <span className="ms-tag">{q.zorluk}</span> <span className="ms-tag">kazanım {q.kazanim}</span> {q.soru}
          </p>
          <ul className="ml-4 mt-1">
            {Object.entries(q.secenekler || {}).map(([h, m]) => (
              <li key={h} className={h === q.dogru ? 'text-ok font-semibold' : ''}>
                {h}) {String(m)}
              </li>
            ))}
          </ul>
          <details className="mt-1">
            <summary className="cursor-pointer text-ink-2">Açıklama</summary>
            <p className="mt-1">{q.aciklama}</p>
            <Kanit k={q.kanit} />
          </details>
        </li>
      ))}
    </ol>
  );
};

export const Sozluk: React.FC<{ veri: any }> = ({ veri }) => {
  if (!veri) return <Yukleniyor veri={veri} />;
  return (
    <div className="flex flex-col gap-3 text-sm">
      <b>Yeni terimler ({(veri.yeni || []).length})</b>
      {(veri.yeni || []).map((t: any, i: number) => (
        <p key={i}>
          <b>{t.term}</b> <span className="ms-tag">{t.category}</span> — {t.definition} <Kanit k={t.kanit} />
        </p>
      ))}
      <b>Zenginleştirilen ({(veri.zenginlestir || []).length})</b>
      {(veri.zenginlestir || []).map((t: any, i: number) => (
        <p key={i}>
          <b>{t.key}</b>: {t.definition || t.pearl || ''} <span className="text-ink-3">({t.neden})</span> <Kanit k={t.kanit} />
        </p>
      ))}
    </div>
  );
};

const ALANLAR: [string, string][] = [
  ['etiology', 'Etiyoloji'],
  ['physiology_pathophysiology', 'Patofizyoloji'],
  ['morphology_pathology', 'Morfoloji'],
  ['symptoms_clinical', 'Klinik'],
  ['pathognomonic_features', 'Patognomonik'],
  ['diagnostic_methods', 'Tanı'],
  ['imaging_findings', 'Görüntüleme'],
  ['treatment', 'Tedavi'],
];

export const Hastaliklar: React.FC<{ veri: any }> = ({ veri }) => {
  if (!veri) return <Yukleniyor veri={veri} />;
  return (
    <div className="flex flex-col gap-3 text-sm">
      {(veri || []).map((h: any) => (
        <details key={h.id} className="ms-panel p-2">
          <summary className="cursor-pointer">
            <b>{h.name}</b> {h.mevcut ? <span className="ms-tag">mevcut kayda ekleme</span> : <span className="ms-tag is-ok">yeni</span>}
          </summary>
          {ALANLAR.filter(([a]) => (h[a] || []).length).map(([a, ad]) => (
            <div key={a} className="mt-1">
              <b>{ad}:</b>
              <ul className="ml-4 list-disc">
                {h[a].map((m: string, i: number) => (
                  <li key={i}>
                    {m} <Kanit k={(h.kanitlar || []).find((k: any) => k.alan === a && k.madde === i)} />
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </details>
      ))}
    </div>
  );
};

export const Havuz: React.FC<{ veri: any }> = ({ veri }) => {
  if (!veri) return <Yukleniyor veri={veri} />;
  return (
    <ul className="flex flex-col gap-1 text-sm">
      {(veri || []).map((b: any, i: number) => (
        <li key={i}>
          <span className="ms-tag">{b.tur}</span> <b>{b.varlik}</b> <i>{b.iliski}</i> <b>{b.hedef}</b> — {b.bilgi} <Kanit k={b.kanit} />
        </li>
      ))}
    </ul>
  );
};

export const Cikmis: React.FC<{ veri: any }> = ({ veri }) => {
  if (!veri) return <Yukleniyor veri={veri} />;
  const ilgili = (veri || []).filter((c: any) => c.ilgili);
  return (
    <ul className="flex flex-col gap-2 text-sm">
      {ilgili.map((c: any) => (
        <li key={c.soru_id}>
          <span className={`ms-tag ${c.guven === 'yuksek' ? 'is-ok' : ''}`}>{c.guven}</span> <code>{c.soru_id}</code> → slayt {c.slideNumber}: {c.slideTitle}
          <p className="text-ink-2">{c.gerekce}</p>
        </li>
      ))}
      <li className="text-ink-3">{(veri || []).length - ilgili.length} aday "bu derste anlatılmıyor" diye ayrıldı.</li>
    </ul>
  );
};
