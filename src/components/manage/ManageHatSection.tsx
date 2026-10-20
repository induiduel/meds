/**
 * Yönetim › Hat panosu (/manage/hat) — canvas HatPanosu.dc.html (v14).
 * Dersler sekmesi: Kurul 2+ ders kayıt defteri × aşama matrisi (GET /api/admin/hat/dersler; src/services/hatActionsRoutes.ts).
 * Hücre renkleri: geçti / çalışıyor / kapıda takıldı / bekliyor (her hücrede ekran okuyucu metni). Seçim + toplu eylem
 * (Baştan üret ve Yayından çek iki dokunuşla), satır → tam sayfa ayrıntı (takılan kapı, hatalar, günlük, tek ders eylemleri).
 * Eylemler kuyruğa yazılır (otomasyon/hat_eylem.py işler); iş varken pano 10 sn'de bir yenilenir.
 * "Şimdi çalıştır" (iki dokunuş): gece hattı birimini hemen başlatır (POST /api/admin/hat/gece/calistir); çalışırken 10 sn'de bir yoklanır.
 * "Baştan üret": önce Oracle ders işçisi PDF'ten yeniden üretir ve yayımlar, ardından cihaz zinciri baştan çalışır (hat_eylem.py).
 * Aşama defteri sekmesi: otomasyon/hat.json + durum.json + hat.log (GET /api/admin/hat).
 * Stil: hat.css (.mh-*), ortak kabuk consoleUi.
 */
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { GitBranch, Play, RefreshCw, ScrollText } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { EmptyState, Panel, Drawer, ConfirmButton, logTone, timeLabel } from './consoleUi';
import { PageActions, StatRow, Toolbar, Tabs14, SearchField, DataTable, DetailNav, DetailLayout, FactList, Card14, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';
import './hat.css';

// ── tipler ──
type HDurum = 'gecti' | 'calisiyor' | 'takildi' | 'bekliyor';
type Hucre = { asama: string; durum: HDurum; kod?: number | null; zaman?: string | null; not?: string; hatalar?: string[] };
type AsamaTanim = { id: string; ad: string; yer: 'oracle' | 'cihaz' };
type Satir = {
  id: string; kod: string; kurul: number; brans: string; ad: string; tarih: string | null; hucreler: Hucre[]; takilan: string | null;
  paket: boolean; is_id: string | null; cekildi: { zaman: string; yedek: string } | null; hataSayisi: number; sonHata: string | null;
  is: { id: string; eylem: string; durum: string } | null; oracleEylem: { yol: string; ad: string } | null; klasor: string;
};
type DerslerYanit = { cihaz: boolean; asamalar: AsamaTanim[]; oracleHata: string | null; oracleZaman: string; dersler: Satir[]; calisan: number };
type Is = { id: string; ders: string; eylem: string; durum: string; olusturma: string; baslama?: string; bitis?: string; kod?: number; kim?: string; not?: string; log?: string[] };
type Ayrinti = { cihaz: boolean; ders: Satir & { ogretim_uyesi: string | null }; isler: Is[]; gece: string[]; claudeLog: string[]; denetimRaporu: string; oracleHata: string | null };
type GeceDurum = { cihaz: boolean; calisiyor: boolean; durum: string; sonuc?: string | null; baslama?: string | null; bitis?: string | null };
type Eylem = 'surdur' | 'bastan' | 'denetci' | 'cek';

type Asama = { id: string; kapsam?: string; durum?: string; gerekir?: string[]; tetik?: string[]; komut?: string; kapi?: string; cikti?: string[]; eksik?: string; not?: string };
type DefterYanit = { defter: { asamalar?: Asama[] } | null; durum: Record<string, { son?: string; kod?: number | null; son_basari?: string }>; log: string[] };

const HUCRE_AD: Record<HDurum, string> = { gecti: 'Geçti', calisiyor: 'Çalışıyor', takildi: 'Kapıda takıldı', bekliyor: 'Bekliyor' };
const EYLEM_AD: Record<Eylem, string> = { surdur: 'Takılan aşamadan sürdür', bastan: 'Baştan üret', denetci: 'Denetçiye gönder', cek: 'Yayından çek' };
const IS_DURUM: Record<string, string> = { bekliyor: 'Sırada', calisiyor: 'Çalışıyor', bitti: 'Bitti', hata: 'Hata verdi', iptal: 'İptal edildi' };
const zaman = (s?: string | null) => (s ? timeLabel(s, true) : '—');
type Suzgec = 'hepsi' | 'takildi' | 'calisiyor' | 'bitti' | 'baslamadi';

const satirDurumu = (r: Satir): Suzgec => {
  if (r.is || r.hucreler.some((h) => h.durum === 'calisiyor')) return 'calisiyor';
  if (r.takilan) return 'takildi';
  if (r.hucreler.every((h) => h.durum === 'gecti')) return 'bitti';
  if (r.hucreler.every((h) => h.durum === 'bekliyor')) return 'baslamadi';
  return 'hepsi';
};

const HucreK: React.FC<{ h: Hucre; ad: string }> = ({ h, ad }) => {
  const metin = `${ad}: ${HUCRE_AD[h.durum]}${h.kod ? ` (kod ${h.kod})` : ''}`;
  return (
    <span className="mh-mhucre" title={h.not ? `${metin} — ${h.not}` : metin}>
      <span className={`mh-hucre is-${h.durum}`} aria-hidden="true" />
      <span className="mh-sr">{metin}</span>
    </span>
  );
};

export const ManageHatSection: React.FC<{ adminEmail?: string }> = ({ adminEmail }) => {
  const [sekme, setSekme] = useState<'dersler' | 'defter'>('dersler');
  const basliklar = useMemo(() => ({ 'x-admin-email': adminEmail || '' }), [adminEmail]);

  // ── ders matrisi ──
  const [kurul, setKurul] = useState('2');
  const [veri, setVeri] = useState<DerslerYanit | null>(null);
  const [hata, setHata] = useState('');
  const [yuk, setYuk] = useState(false);
  const [suzgec, setSuzgec] = useState<Suzgec>('hepsi');
  const [ara, setAra] = useState('');
  const [mesaj, setMesaj] = useState<{ tur: 'ok' | 'hata'; metin: string } | null>(null);
  const [mesgul, setMesgul] = useState(false);

  const yukle = useCallback(async (sessiz = false) => {
    if (!sessiz) setYuk(true);
    const r = await safeJsonFetch<DerslerYanit>(`/api/admin/hat/dersler?kurul=${kurul}`, { headers: basliklar });
    if (!sessiz) setYuk(false);
    if (r.ok && r.data) { setVeri(r.data); setHata(''); } else if (!sessiz) setHata(r.error || `Ders durumu alınamadı (${r.status}).`);
  }, [kurul, basliklar]);
  useEffect(() => { void yukle(); }, [yukle]);

  const dersler = veri?.dersler || [];
  const asamalar = veri?.asamalar || [];
  const asamaAd = (id: string) => asamalar.find((a) => a.id === id)?.ad || id;
  const isVar = !!veri && (veri.calisan > 0 || dersler.some((d) => d.is));

  const [acik, setAcik] = useState<string | null>(null);
  const [ayr, setAyr] = useState<Ayrinti | null>(null);
  const ayrinti = useCallback(async (id: string) => {
    const r = await safeJsonFetch<Ayrinti>(`/api/admin/hat/dersler/${id}`, { headers: basliklar });
    if (r.ok && r.data) setAyr(r.data);
  }, [basliklar]);
  useEffect(() => { setAyr(null); if (acik) void ayrinti(acik); }, [acik, ayrinti]);

  // iş varken yokla (10 sn); sekme gizliyse bekle
  useEffect(() => {
    if (!isVar) return;
    const t = window.setInterval(() => {
      if (document.hidden) return;
      void yukle(true);
      if (acik) void ayrinti(acik);
    }, 10000);
    return () => window.clearInterval(t);
  }, [isVar, yukle, ayrinti, acik]);

  const sayilar = useMemo(() => {
    const s = { hepsi: dersler.length, takildi: 0, calisiyor: 0, bitti: 0, baslamadi: 0 };
    dersler.forEach((d) => { const k = satirDurumu(d); if (k !== 'hepsi') s[k] += 1; });
    return s;
  }, [dersler]);
  const liste = dersler.filter((d) => {
    if (suzgec !== 'hepsi' && satirDurumu(d) !== suzgec) return false;
    const q = ara.trim().toLocaleLowerCase('tr');
    return !q || `${d.ad} ${d.id} ${d.kod} ${d.brans}`.toLocaleLowerCase('tr').includes(q);
  });

  // ── gece hattı: şimdi çalıştır ──
  const [gece, setGece] = useState<GeceDurum | null>(null);
  const geceYukle = useCallback(async () => {
    const r = await safeJsonFetch<GeceDurum>('/api/admin/hat/gece', { headers: basliklar });
    if (r.ok && r.data) setGece(r.data);
  }, [basliklar]);
  useEffect(() => { void geceYukle(); }, [geceYukle]);
  useEffect(() => {
    if (!gece?.calisiyor) return;
    const t = window.setInterval(() => { if (!document.hidden) { void geceYukle(); void yukle(true); } }, 10000);
    return () => window.clearInterval(t);
  }, [gece?.calisiyor, geceYukle, yukle]);
  const geceCalistir = async () => {
    setMesaj(null);
    const r = await safeJsonFetch<any>('/api/admin/hat/gece/calistir', {
      method: 'POST', headers: { ...basliklar, 'Content-Type': 'application/json' }, body: JSON.stringify({ onay: true }),
    });
    if (r.data && typeof r.data.calisiyor === 'boolean') setGece({ cihaz: true, ...r.data });
    setMesaj(r.ok ? { tur: 'ok', metin: 'Gece hattı başlatıldı. Bugün başarıyla geçmiş aşamalar yeniden çalışmaz.' }
      : { tur: 'hata', metin: r.data?.error || r.error || `Gece hattı başlatılamadı (${r.status}).` });
    void geceYukle();
  };
  const geceNot = !gece ? null : gece.calisiyor
    ? <>Gece hattı şu an çalışıyor{gece.baslama ? ` (başlangıç ${zaman(gece.baslama)})` : ''}.</>
    : gece.bitis ? <>Gece hattı en son {zaman(gece.bitis)} bitti{gece.sonuc && gece.sonuc !== 'success' ? ', hata verdi' : ''}.</> : null;

  const secim = useSelection<string>();
  const cur = dersler.find((d) => d.id === acik) || null;

  const eylemYap = useCallback(async (eylem: Eylem, ids: string[]) => {
    if (!ids.length) return;
    setMesgul(true); setMesaj(null);
    const parca: string[] = []; let kotu = false;
    // Oracle aşamasında takılan dersler işçinin kendi uçlarıyla sürdürülür (ders zinciri o aşamaları çalıştırmaz)
    let yerel = ids;
    if (eylem === 'surdur') {
      const oracle = dersler.filter((d) => ids.includes(d.id) && d.oracleEylem);
      yerel = ids.filter((id) => !oracle.some((d) => d.id === id));
      for (const d of oracle) {
        const r = await safeJsonFetch<any>(d.oracleEylem!.yol, { method: 'POST', headers: { ...basliklar, 'Content-Type': 'application/json' }, body: '{}' });
        if (r.ok) parca.push(`${d.id}: ${d.oracleEylem!.ad.toLocaleLowerCase('tr')} istendi`);
        else { kotu = true; parca.push(`${d.id}: ders işçisi isteği reddetti (${r.data?.hata || r.error || r.status})`); }
      }
    }
    if (yerel.length) {
      const r = await safeJsonFetch<any>('/api/admin/hat/eylem', {
        method: 'POST', headers: { ...basliklar, 'Content-Type': 'application/json' },
        body: JSON.stringify({ eylem, dersler: yerel, onay: eylem === 'bastan' || eylem === 'cek' }),
      });
      if (r.ok && r.data) {
        if (r.data.kuyruga?.length) parca.push(`${r.data.kuyruga.length} ders için "${EYLEM_AD[eylem]}" sıraya alındı`);
        (r.data.atlanan || []).forEach((a: { id: string; neden: string }) => { kotu = true; parca.push(`${a.id}: ${a.neden}`); });
        if (r.data.baslatmaHatasi) { kotu = true; parca.push(`İşleyici başlatılamadı: ${r.data.baslatmaHatasi}`); }
      } else { kotu = true; parca.push(r.data?.error || r.error || `İstek başarısız (${r.status}).`); }
    }
    setMesgul(false);
    setMesaj({ tur: kotu ? 'hata' : 'ok', metin: parca.join(' · ') || 'Yapılacak bir şey yok.' });
    secim.clear();
    await yukle(true);
    if (acik) void ayrinti(acik);
  }, [dersler, basliklar, secim, yukle, ayrinti, acik]);

  const iptal = async (isId: string) => {
    const r = await safeJsonFetch<any>(`/api/admin/hat/eylem/${isId}/iptal`, { method: 'POST', headers: basliklar });
    setMesaj(r.ok ? { tur: 'ok', metin: 'Sıradaki iş iptal edildi.' } : { tur: 'hata', metin: r.data?.error || r.error || 'İptal edilemedi.' });
    await yukle(true); if (acik) void ayrinti(acik);
  };

  const salt = veri ? !veri.cihaz : false;
  const kolonlar: Col<Satir>[] = [
    {
      key: 'ad', label: 'Ders', main: true, render: (d) => (
        <span className="mh-ders"><b>{d.ad}</b><code>{d.id} · {d.kod}</code></span>
      ),
    },
    ...asamalar.map((a, i): Col<Satir> => ({
      key: a.id, label: <span className="mh-th" title={a.ad}>{a.ad}</span>, width: 78,
      render: (d) => <HucreK h={d.hucreler[i]} ad={a.ad} />,
    })),
    {
      key: 'is', label: 'İş', width: 110, render: (d) => (d.is ? <span className="mh-rozet is-acc">{IS_DURUM[d.is.durum] || d.is.durum}</span>
        : d.cekildi ? <span className="mh-rozet is-warn">Yayından çekildi</span> : <span className="mh-soluk">—</span>),
    },
  ];

  const tekEylemler = (d: Satir) => {
    const dis = mesgul || salt || !!d.is;
    return (
      <div className="mh-eylemler">
        <button type="button" className="m14-btn primary" disabled={mesgul || (salt && !d.oracleEylem) || !!d.is} onClick={() => void eylemYap('surdur', [d.id])}>
          {d.oracleEylem ? d.oracleEylem.ad : 'Takılan aşamadan sürdür'}
        </button>
        <button type="button" className="m14-btn" disabled={dis} onClick={() => void eylemYap('denetci', [d.id])}>Denetçiye gönder</button>
        <ConfirmButton className="m14-btn danger" disabled={dis} confirmLabel="Eminim, baştan üret" title="Önce ders işçisi PDF'i yeniden okuyup paketi üretir ve yayımlar, ardından cihaz zinciri baştan çalışır" onConfirm={() => eylemYap('bastan', [d.id])}>Baştan üret</ConfirmButton>
        <ConfirmButton className="m14-btn danger" disabled={dis || !d.paket} confirmLabel="Eminim, yayından çek" onConfirm={() => eylemYap('cek', [d.id])}>Yayından çek</ConfirmButton>
      </div>
    );
  };

  return (
    <div className="mh">
      <PageActions note={<>Kurul 2 ve sonrası tam otomatik hat. Ders zinciri her gece 02:30'da çalışır (en çok 3 ders); eylemler sıraya alınır, gece hattı sürerken bekler.{geceNot && <> {geceNot}</>}</>}>
        {gece?.calisiyor ? (
          <button type="button" className="m14-btn" disabled><Play aria-hidden /> Gece hattı çalışıyor</button>
        ) : (
          <ConfirmButton className="m14-btn" icon={Play} disabled={salt || !gece?.cihaz} confirmLabel="Eminim, şimdi çalıştır"
            title={salt ? 'Gece hattı yalnız cihazda çalışır' : 'Gece hattını beklemeden şimdi başlatır'} onConfirm={geceCalistir}>Şimdi çalıştır</ConfirmButton>
        )}
        <button type="button" className="m14-btn" onClick={() => { void geceYukle(); void (sekme === 'dersler' ? yukle() : undefined); }} disabled={yuk}>
          <RefreshCw className={yuk ? 'animate-spin' : ''} aria-hidden /> Yenile
        </button>
      </PageActions>

      <Tabs14 value={sekme} onChange={setSekme} label="Görünüm" options={[{ id: 'dersler', label: 'Dersler' }, { id: 'defter', label: 'Aşama defteri' }]} />

      {sekme === 'defter' ? <AsamaDefteri basliklar={basliklar} /> : (
        <>
          {hata && <p className="mh-hata" role="alert">{hata}</p>}
          {salt && <p className="mh-uyari" role="note">Bu sunucuda pano salt okunur: ders zinciri yalnız cihazda çalışır. Eylemler için paneli cihazdan (localhost) açın.</p>}
          {veri?.oracleHata && <p className="mh-uyari" role="note">{veri.oracleHata}. Ders işçisi ve yayın sütunları cihazdaki yayın kaydı kopyasından gösteriliyor.</p>}
          {mesaj && <p className={mesaj.tur === 'hata' ? 'mh-hata' : 'mh-tamam'} role="status">{mesaj.metin}</p>}
          {!veri && !hata && <p className="mh-bilgi">Yükleniyor…</p>}
          {veri && (
            <>
              <StatRow
                stats={[
                  { label: 'Ders', value: sayilar.hepsi, onClick: () => setSuzgec('hepsi') },
                  { label: 'Kapıda takılan', value: sayilar.takildi, tone: sayilar.takildi ? 'bad' : undefined, onClick: () => setSuzgec('takildi') },
                  { label: 'Çalışan', value: sayilar.calisiyor, tone: sayilar.calisiyor ? 'acc' : undefined, onClick: () => setSuzgec('calisiyor') },
                  { label: 'Tamamlanan', value: sayilar.bitti, tone: 'ok', onClick: () => setSuzgec('bitti') },
                ]}
              />
              <Toolbar>
                <Tabs14
                  value={kurul}
                  onChange={(k) => { setKurul(k); secim.clear(); }}
                  label="Kurul"
                  options={['2', '3', '4', '5', '6'].map((k) => ({ id: k, label: `Kurul ${k}` }))}
                />
                <Tabs14
                  value={suzgec}
                  onChange={setSuzgec}
                  label="Ders durumu"
                  options={[
                    { id: 'hepsi', label: 'Tümü', n: sayilar.hepsi },
                    { id: 'takildi', label: 'Takılan', n: sayilar.takildi },
                    { id: 'calisiyor', label: 'Çalışan', n: sayilar.calisiyor },
                    { id: 'bitti', label: 'Tamamlanan', n: sayilar.bitti },
                    { id: 'baslamadi', label: 'Başlamadı', n: sayilar.baslamadi },
                  ]}
                />
                <SearchField value={ara} onChange={setAra} placeholder="Ders, kimlik ya da branş ara" label="Ders ara" />
              </Toolbar>
              <span className="mh-lejant" aria-label="Renk anlamları">
                <span><i className="mh-hucre is-gecti" />Geçti</span>
                <span><i className="mh-hucre is-calisiyor" />Çalışıyor</span>
                <span><i className="mh-hucre is-takildi" />Kapıda takıldı</span>
                <span><i className="mh-hucre is-bekliyor" />Bekliyor</span>
              </span>
              <BulkBar
                count={secim.count}
                noun="ders"
                busy={mesgul}
                onClear={secim.clear}
                actions={[
                  { label: 'Takılan aşamadan sürdür', kind: 'main', run: () => eylemYap('surdur', [...secim.sel]), disabled: salt },
                  { label: 'Baştan üret', kind: 'danger', confirm: `${secim.count} dersi baştan üret`, run: () => eylemYap('bastan', [...secim.sel]), disabled: salt },
                  { label: 'Denetçiye gönder', run: () => eylemYap('denetci', [...secim.sel]), disabled: salt },
                  { label: 'Yayından çek', kind: 'danger', confirm: `${secim.count} dersi yayından çek`, run: () => eylemYap('cek', [...secim.sel]), disabled: salt },
                ]}
              />
              <DataTable
                rows={liste}
                cols={kolonlar}
                rowKey={(d) => d.id}
                onOpen={(d) => setAcik(d.id)}
                selection={secim}
                activeKey={acik}
                minWidth={980}
                busy={yuk}
                empty={dersler.length ? 'Bu süzgeçte ders yok.' : 'Bu kurulun ders kayıt defteri boş.'}
              />
            </>
          )}
        </>
      )}

      <Drawer
        open={!!cur}
        onClose={() => setAcik(null)}
        title={cur ? cur.ad : 'Ders'}
        wide
        head={<DetailNav list={liste} current={cur} same={(a, b) => a.id === b.id} onGo={(d) => setAcik(d.id)} />}
        foot={cur && tekEylemler(cur)}
      >
        {cur && (
          <DetailLayout
            main={
              <>
                <ol className="mh-adimlar" aria-label="Aşamalar">
                  {cur.hucreler.map((h) => (
                    <li key={h.asama} className={`is-${h.durum}`}>
                      <span className={`mh-hucre is-${h.durum}`} aria-hidden="true" />
                      <span className="mh-adim-ad">{asamaAd(h.asama)}</span>
                      <span className="mh-adim-d">{HUCRE_AD[h.durum]}{h.kod ? ` · kod ${h.kod}` : ''}{h.zaman ? ` · ${zaman(h.zaman)}` : ''}</span>
                      {h.not && <span className="mh-adim-not">{h.not}</span>}
                    </li>
                  ))}
                </ol>
                {cur.hucreler.filter((h) => h.durum === 'takildi').map((h) => (
                  <div key={h.asama} className="mh-takilan" role="alert">
                    <b>Takılan kapı: {asamaAd(h.asama)}</b>
                    <span>{h.not}</span>
                    {(h.hatalar || []).map((x, i) => <span key={i} className="mh-kapi-h">{x}</span>)}
                  </div>
                ))}
                {cur.cekildi && (
                  <p className="mh-uyari">Bu ders {zaman(cur.cekildi.zaman)} tarihinde yayından çekildi; yedek <code>{cur.cekildi.yedek}</code>. Ders zinciri onu kendiliğinden yeniden yayına almaz.</p>
                )}
                {!ayr && <p className="mh-bilgi">Ayrıntı yükleniyor…</p>}
                {ayr && ayr.ders.id === cur.id && (
                  <>
                    {ayr.isler.length > 0 && (
                      <Card14 title="Eylem işleri">
                        <ul className="mh-isler">
                          {ayr.isler.map((j) => (
                            <li key={j.id}>
                              <div className="mh-is-ust">
                                <b>{EYLEM_AD[j.eylem as Eylem] || j.eylem}</b>
                                <span className={`mh-rozet ${j.durum === 'hata' ? 'is-bad' : j.durum === 'bitti' ? 'is-ok' : 'is-acc'}`}>{IS_DURUM[j.durum] || j.durum}{j.kod ? ` · kod ${j.kod}` : ''}</span>
                                <span className="mh-soluk">{zaman(j.olusturma)}</span>
                                {j.durum === 'bekliyor' && !salt && <button type="button" className="m14-btn" onClick={() => void iptal(j.id)}>İptal et</button>}
                              </div>
                              {j.not && <span className="mh-soluk">{j.not}</span>}
                              {!!j.log?.length && <pre className="ms-term mh-log">{j.log.map((l, i) => <div key={i} className={logTone(l)}>{l}</div>)}</pre>}
                            </li>
                          ))}
                        </ul>
                      </Card14>
                    )}
                    <Card14 title="Gece hattı günlüğü (bu ders)">
                      {ayr.gece.length === 0 ? <p className="mh-bilgi">Son gece çalışmalarında bu derse ait satır yok.</p> : (
                        <pre className="ms-term mh-log">{ayr.gece.map((l, i) => <div key={i} className={logTone(l)}>{l}</div>)}</pre>
                      )}
                    </Card14>
                    {ayr.claudeLog.length > 0 && (
                      <Card14 title={`Claude oturum günlüğü (${cur.klasor}, branş geneli, son 40 satır)`}>
                        <pre className="ms-term mh-log">{ayr.claudeLog.map((l, i) => <div key={i} className={logTone(l)}>{l}</div>)}</pre>
                      </Card14>
                    )}
                    {ayr.denetimRaporu && (
                      <Card14 title="Bağımsız denetçi raporu">
                        <pre className="mh-rapor">{ayr.denetimRaporu}</pre>
                      </Card14>
                    )}
                  </>
                )}
              </>
            }
            side={
              <FactList
                items={[
                  { k: 'Kimlik', v: <code>{cur.id}</code> },
                  { k: 'Kod', v: <code>{cur.kod}</code> },
                  { k: 'Kurul', v: `Kurul ${cur.kurul}` },
                  { k: 'Branş', v: cur.brans },
                  { k: 'Öğretim üyesi', v: ayr?.ders.ogretim_uyesi || '—' },
                  { k: 'Ders tarihi', v: cur.tarih || '—' },
                  { k: 'Yayın paketi', v: cur.paket ? 'Var' : 'Yok' },
                  { k: 'İşçi taslağı', v: cur.is_id ? <code>{cur.is_id}</code> : '—' },
                  { k: 'Art arda hata', v: cur.hataSayisi ? `${cur.hataSayisi} (son ${zaman(cur.sonHata)})` : '—' },
                  { k: 'Çalışma klasörü', v: <code>meds_temp/spot_cozucu/{cur.klasor}</code> },
                ]}
              />
            }
          />
        )}
      </Drawer>
    </div>
  );
};

// ── Aşama defteri (önceki pano): hat.json aşamaları + son çalışma + hat.log ──
const AsamaDefteri: React.FC<{ basliklar: Record<string, string> }> = ({ basliklar }) => {
  const [veri, setVeri] = useState<DefterYanit | null>(null);
  const [hata, setHata] = useState('');
  useEffect(() => {
    void safeJsonFetch<DefterYanit>('/api/admin/hat', { headers: basliklar }).then((r) => {
      if (r.ok && r.data) setVeri(r.data); else setHata(r.error || `Hat durumu alınamadı (${r.status}).`);
    });
  }, [basliklar]);
  const asamalar = veri?.defter?.asamalar || [];
  const durum = veri?.durum || {};
  const kolonlar: Col<Asama>[] = [
    { key: 'id', label: 'Aşama', main: true, render: (a) => <code className="mh-id">{a.id}</code> },
    { key: 'tur', label: 'Tür', render: (a) => <span className={`mh-rozet ${a.durum === 'hazir' ? 'is-ok' : a.durum === 'el' ? 'is-warn' : ''}`}>{a.durum === 'hazir' ? 'Otomatik' : a.durum === 'el' ? 'Elle' : 'Planlandı'}</span> },
    {
      key: 'son', label: 'Son çalışma', render: (a) => {
        const d = durum[a.id]; const k: HDurum = d && d.kod != null ? (d.kod === 0 ? 'gecti' : 'takildi') : 'bekliyor';
        return <span className="mh-hucre-k"><span className={`mh-hucre is-${k}`} aria-hidden="true" /><span>{k === 'takildi' ? `Kapıda takıldı (kod ${d?.kod})` : HUCRE_AD[k]}</span></span>;
      },
    },
    { key: 'kapi', label: 'Kapı', mono: true, render: (a) => a.kapi || '—' },
    { key: 'basari', label: 'Son başarı', muted: true, render: (a) => zaman(durum[a.id]?.son_basari) },
  ];
  if (hata) return <p className="mh-hata" role="alert">{hata}</p>;
  if (!veri) return <p className="mh-bilgi">Yükleniyor…</p>;
  if (!veri.defter) return <EmptyState icon={GitBranch} title="Kayıt defteri okunamadı">otomasyon/hat.json bulunamadı ya da bozuk.</EmptyState>;
  return (
    <>
      <DataTable rows={asamalar} cols={kolonlar} rowKey={(a) => a.id} empty="Aşama yok." />
      <Panel title="Hat günlüğü" icon={ScrollText} count={veri.log.length} desc="meds_temp/hat/hat.log son 60 satır, en yenisi altta.">
        {veri.log.length === 0 ? <EmptyState icon={ScrollText} title="Günlük boş">Hat henüz çalışmadı.</EmptyState> : (
          <pre className="ms-term mh-log">{veri.log.map((l, i) => <div key={i} className={logTone(l)}>{l}</div>)}</pre>
        )}
      </Panel>
    </>
  );
};
