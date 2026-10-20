/**
 * Yönetim › Kamp tüyoları (/manage/kamp-tuyolari): öğrencilerin önerdiği hoca tüyoları (onayla / düzenleyip onayla /
 * reddet), onaylılar, reddedilenler ve yöneticinin doğrudan eklemesi. Uçlar services/kampRoutes.ts
 * (GET /api/admin/kamp/tuyolar, POST /api/admin/kamp/tuyo, POST /api/admin/kamp/tuyo/:id/karar). Onaylı tüyolar gece
 * kamp zincirinde (otomasyon/kamp_zinciri.py) kampa işlenir. v14 liste kalıbı (pageKit) + tam alan Drawer.
 */
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { Check, PencilLine, Plus, RefreshCw, Tent, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { KURULLAR, aktifKurul } from '../../services/kurulTakvimi';
import { toast } from '../ui/Toast';
import { Drawer, EmptyState, Field, timeLabel } from './consoleUi';
import { Card14, DataTable, DetailLayout, DetailNav, FactList, PageActions, Pill, SearchField, StatRow, Tabs14, Toolbar, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';
import { bransAdi, bransBul, dersNo, kurulBranslari, kurulDersleri } from '../kamp/kampVeri';

type Durum = 'oneri' | 'onayli' | 'reddedildi';
interface Tuyo { id: string; kurul: number; brans: string; ders_id?: string; metin: string; kaynak?: string; durum: Durum; zaman: string; kim?: string }

const DURUM_AD: Record<Durum, string> = { oneri: 'Bekleyen', onayli: 'Onaylı', reddedildi: 'Reddedilen' };

const dersAdi = (kurul: number, id?: string) => {
  if (!id) return '';
  const d = kurulDersleri(kurul).find((x) => x.id === id);
  return d ? `Ders ${dersNo(d)} · ${d.konu}` : id;
};

export const ManageKampSection: React.FC<{ adminEmail?: string }> = ({ adminEmail }) => {
  const headers = useMemo(() => ({ 'x-admin-email': adminEmail || '', 'Content-Type': 'application/json' }), [adminEmail]);
  const [liste, setListe] = useState<Tuyo[] | null>(null);
  const [hata, setHata] = useState('');
  const [yuk, setYuk] = useState(false);
  const [suzgec, setSuzgec] = useState<Durum>('oneri');
  const [duzen, setDuzen] = useState<Record<string, string>>({});
  const [mesgul, setMesgul] = useState('');
  const [ara, setAra] = useState('');
  const [acikId, setAcikId] = useState<string | null>(null);
  const [ekleAcik, setEkleAcik] = useState(false);
  const [topluBusy, setTopluBusy] = useState(false);
  const secim = useSelection<string>();

  const yukle = useCallback(async () => {
    setYuk(true); setHata('');
    const r = await safeJsonFetch<{ tuyolar: Tuyo[] }>('/api/admin/kamp/tuyolar', { headers });
    setYuk(false);
    if (r.ok && r.data) setListe(r.data.tuyolar || []); else setHata(r.error || `Tüyolar alınamadı (${r.status}).`);
  }, [headers]);
  useEffect(() => { void yukle(); }, [yukle]);

  const say = useMemo(() => {
    const L = liste || [];
    return { oneri: L.filter((t) => t.durum === 'oneri').length, onayli: L.filter((t) => t.durum === 'onayli').length, reddedildi: L.filter((t) => t.durum === 'reddedildi').length };
  }, [liste]);
  const t0 = ara.trim().toLocaleLowerCase('tr');
  const gorunen = (liste || [])
    .filter((t) => t.durum === suzgec)
    .filter((t) => !t0 || `${t.metin} ${t.id} ${bransAdi(t.brans)} ${dersAdi(t.kurul, t.ders_id)} ${t.kim || ''}`.toLocaleLowerCase('tr').includes(t0))
    .sort((a, b) => (b.zaman || '').localeCompare(a.zaman || ''));
  const acik = acikId ? (liste || []).find((t) => t.id === acikId) || null : null;

  const kararGonder = (t: Tuyo, k: 'onayla' | 'reddet', metin?: string) =>
    safeJsonFetch('/api/admin/kamp/tuyo/' + encodeURIComponent(t.id) + '/karar', {
      method: 'POST', headers, body: JSON.stringify({ karar: k, ...(k === 'onayla' && metin && metin !== t.metin ? { metin } : {}) }),
    });

  const karar = async (t: Tuyo, k: 'onayla' | 'reddet') => {
    const metin = duzen[t.id]?.trim();
    if (k === 'onayla' && metin !== undefined && metin.length < 8) { toast.error('Düzeltilmiş metin en az 8 karakter olmalı.'); return false; }
    setMesgul(t.id);
    const r = await kararGonder(t, k, metin);
    setMesgul('');
    if (!r.ok) { toast.error(r.error || 'Karar kaydedilemedi.'); return false; }
    toast.success(k === 'onayla' ? 'Tüyo onaylandı; gece kampa işlenecek.' : 'Tüyo reddedildi.');
    setDuzen((d) => { const n = { ...d }; delete n[t.id]; return n; });
    void yukle();
    return true;
  };

  const toplu = async (k: 'onayla' | 'reddet') => {
    const hedef = (liste || []).filter((t) => secim.has(t.id) && (k === 'onayla' ? t.durum !== 'onayli' : t.durum === 'oneri'));
    if (!hedef.length) { toast.error('Seçilenlerde bu işleme uygun tüyo yok.'); return; }
    setTopluBusy(true);
    let ok = 0, err = 0;
    for (const t of hedef) {
      const r = await kararGonder(t, k);
      if (r.ok) ok++; else err++;
    }
    setTopluBusy(false);
    (err ? toast.error : toast.success)(`${k === 'onayla' ? 'Onay' : 'Ret'}: ${ok} başarılı, ${err} hata.`);
    if (!err) secim.clear();
    void yukle();
  };

  const sonraki = (t: Tuyo) => {
    const i = gorunen.findIndex((x) => x.id === t.id);
    const n = gorunen[i + 1];
    setAcikId(n ? n.id : null);
  };

  const cols: Col<Tuyo>[] = [
    { key: 'm', label: 'Tüyo', main: true, render: (t) => t.metin },
    { key: 'b', label: 'Kurul · branş', render: (t) => `Kurul ${t.kurul} · ${bransAdi(t.brans)}` },
    { key: 'd', label: 'Ders', muted: true, render: (t) => dersAdi(t.kurul, t.ders_id) || '—' },
    { key: 'k', label: 'Kaynak', muted: true, render: (t) => (t.kaynak === 'ogrenci' ? `öğrenci${t.kim ? ` (${t.kim})` : ''}` : t.kaynak || '—') },
    { key: 's', label: 'Durum', render: (t) => <Pill tone={t.durum === 'onayli' ? 'ok' : t.durum === 'oneri' ? 'warn' : 'bad'}>{DURUM_AD[t.durum]}</Pill> },
    { key: 'z', label: 'Zaman', muted: true, render: (t) => timeLabel(t.zaman, true) },
  ];

  const d = acik ? duzen[acik.id] : undefined;

  return (
    <div className="flex flex-col gap-4 min-w-0">
      <PageActions note="Öğrencilerin önerdiği hoca tüyoları. Onaylananlar gece kamp zincirinde ilgili kurul ve branşın kampına işlenir; kayıt silinmez, kararlar deftere eklenir.">
        <button type="button" className="m14-btn" onClick={() => void yukle()} disabled={yuk}><RefreshCw className={yuk ? 'animate-spin' : ''} aria-hidden /> Yenile</button>
        <button type="button" className="m14-btn primary" onClick={() => setEkleAcik(true)}><Plus aria-hidden /> Tüyo ekle</button>
      </PageActions>

      <StatRow
        stats={(['oneri', 'onayli', 'reddedildi'] as Durum[]).map((k) => ({
          label: DURUM_AD[k], value: liste ? say[k].toLocaleString('tr-TR') : '…', tone: k === 'oneri' && say.oneri ? 'warn' as const : undefined, onClick: () => setSuzgec(k),
        }))}
      />

      <Toolbar>
        <Tabs14<Durum> value={suzgec} onChange={setSuzgec} label="Tüyo durumu"
          options={(['oneri', 'onayli', 'reddedildi'] as Durum[]).map((k) => ({ id: k, label: DURUM_AD[k], n: say[k] }))} />
        <SearchField value={ara} onChange={setAra} placeholder="Tüyo, branş ya da ders ara" />
      </Toolbar>

      <BulkBar
        count={secim.count}
        noun="tüyo"
        busy={topluBusy}
        onClear={secim.clear}
        actions={[
          { label: 'Onayla', kind: 'main', run: () => toplu('onayla') },
          { label: 'Reddet', kind: 'danger', confirm: `${secim.count} tüyoyu reddetmeyi onayla`, run: () => toplu('reddet') },
        ]}
      />

      {hata && <p className="text-sm text-bad" role="alert">{hata}</p>}
      {!liste && !hata && <p className="text-sm text-ink-3">Yükleniyor…</p>}
      {liste && (
        <DataTable
          rows={gorunen}
          cols={cols}
          rowKey={(t) => t.id}
          onOpen={(t) => setAcikId(t.id)}
          activeKey={acikId}
          selection={secim}
          busy={yuk}
          empty={
            <EmptyState icon={Tent} title={suzgec === 'oneri' ? 'Bekleyen öneri yok' : `${DURUM_AD[suzgec]} tüyo yok`}>
              {suzgec === 'oneri' ? 'Öğrenciler /kamp sayfasından tüyo önerdikçe burada görünür.' : undefined}
            </EmptyState>
          }
        />
      )}

      <Drawer
        open={!!acik}
        onClose={() => setAcikId(null)}
        title={acik ? `Kurul ${acik.kurul} · ${bransAdi(acik.brans)}` : ''}
        head={acik && <DetailNav list={gorunen} current={acik} same={(a, b) => a.id === b.id} onGo={(t) => setAcikId(t.id)} />}
        foot={acik && acik.durum !== 'onayli' && (
          <div className="flex flex-wrap gap-2">
            {acik.durum === 'oneri' && <button type="button" className="m14-btn danger" disabled={mesgul === acik.id} onClick={() => void karar(acik, 'reddet')}><X aria-hidden /> Reddet</button>}
            {d === undefined
              ? <button type="button" className="m14-btn" onClick={() => setDuzen((x) => ({ ...x, [acik.id]: acik.metin }))}><PencilLine aria-hidden /> Düzenle</button>
              : <button type="button" className="m14-btn ghost" onClick={() => setDuzen((x) => { const n = { ...x }; delete n[acik.id]; return n; })}>Düzenlemeyi bırak</button>}
            <button type="button" className="m14-btn" disabled={mesgul === acik.id} onClick={() => void karar(acik, 'onayla')}>
              <Check aria-hidden /> {d !== undefined ? 'Düzeltip onayla' : 'Onayla'}
            </button>
            <button type="button" className="m14-btn primary" disabled={mesgul === acik.id} onClick={async () => { if (await karar(acik, 'onayla')) sonraki(acik); }}>
              <Check aria-hidden /> Onayla ve sonraki
            </button>
          </div>
        )}
      >
        {acik && (
          <DetailLayout
            main={
              <Card14 title="Tüyo metni">
                {d !== undefined ? (
                  <textarea className="ms-input w-full min-h-[120px]" value={d} maxLength={1500} onChange={(e) => setDuzen((x) => ({ ...x, [acik.id]: e.target.value }))} aria-label="Tüyo metnini düzenle" />
                ) : (
                  <p className="text-[15px] leading-relaxed whitespace-pre-wrap break-words">{acik.metin}</p>
                )}
              </Card14>
            }
            side={
              <FactList items={[
                { k: 'Durum', v: <Pill tone={acik.durum === 'onayli' ? 'ok' : acik.durum === 'oneri' ? 'warn' : 'bad'}>{DURUM_AD[acik.durum]}</Pill> },
                { k: 'Kurul', v: acik.kurul },
                { k: 'Branş', v: bransAdi(acik.brans) },
                { k: 'Ders', v: dersAdi(acik.kurul, acik.ders_id) || '—' },
                { k: 'Kaynak', v: acik.kaynak === 'ogrenci' ? `öğrenci${acik.kim ? ` (${acik.kim})` : ''}` : acik.kaynak || '—' },
                { k: 'Zaman', v: timeLabel(acik.zaman, true) },
                { k: 'Kimlik', v: <code className="text-xs">{acik.id}</code> },
              ]} />
            }
          />
        )}
      </Drawer>

      <Drawer open={ekleAcik} onClose={() => setEkleAcik(false)} title="Tüyo ekle">
        <YoneticiEkle headers={headers} onEklendi={() => { setEkleAcik(false); setSuzgec('onayli'); void yukle(); }} />
      </Drawer>
    </div>
  );
};

function YoneticiEkle({ headers, onEklendi }: { headers: Record<string, string>; onEklendi: () => void }) {
  const [kurul, setKurul] = useState(aktifKurul().kurul);
  const [brans, setBrans] = useState('');
  const [ders, setDers] = useState('');
  const [metin, setMetin] = useState('');
  const [kaynak, setKaynak] = useState('');
  const [gidiyor, setGidiyor] = useState(false);
  const branslar = useMemo(() => kurulBranslari(kurul), [kurul]);
  const dersler = useMemo(() => kurulDersleri(kurul).filter((d) => bransBul(d.brans)?.slug === brans), [kurul, brans]);

  const ekle = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!brans) { toast.error('Branş seçin.'); return; }
    if (metin.trim().length < 8) { toast.error('Tüyo metni en az 8 karakter olmalı.'); return; }
    setGidiyor(true);
    const r = await safeJsonFetch('/api/admin/kamp/tuyo', {
      method: 'POST', headers, body: JSON.stringify({ kurul, brans, ders_id: ders || undefined, metin: metin.trim(), kaynak: kaynak.trim() || undefined }),
    });
    setGidiyor(false);
    if (!r.ok) { toast.error(r.error || 'Tüyo eklenemedi.'); return; }
    toast.success('Tüyo onaylı olarak eklendi.');
    setMetin(''); setKaynak('');
    onEklendi();
  };

  return (
    <div className="flex flex-col gap-3">
      <p className="text-sm text-ink-3">Yöneticinin girdiği tüyo doğrudan onaylı olur.</p>
      <form className="grid gap-3" onSubmit={ekle}>
        <div className="grid gap-3 sm:grid-cols-3">
          <Field label="Kurul">
            <select className="ms-input" value={kurul} onChange={(e) => { setKurul(Number(e.target.value)); setBrans(''); setDers(''); }}>
              {KURULLAR.map((k) => <option key={k.kurul} value={k.kurul}>Kurul {k.kurul}</option>)}
            </select>
          </Field>
          <Field label="Branş">
            <select className="ms-input" value={brans} onChange={(e) => { setBrans(e.target.value); setDers(''); }}>
              <option value="">Seçin</option>
              {branslar.map((b) => <option key={b.slug} value={b.slug}>{b.ad}</option>)}
            </select>
          </Field>
          <Field label="Ders (isteğe bağlı)">
            <select className="ms-input" value={ders} onChange={(e) => setDers(e.target.value)} disabled={!dersler.length}>
              <option value="">—</option>
              {dersler.map((d) => <option key={d.id} value={d.id}>Ders {dersNo(d)} · {d.konu}</option>)}
            </select>
          </Field>
        </div>
        <Field label="Tüyo metni"><textarea className="ms-input min-h-[88px]" value={metin} maxLength={1500} onChange={(e) => setMetin(e.target.value)} /></Field>
        <Field label="Kaynak (isteğe bağlı)" hint="Boş bırakılırsa “hoca (yönetici girdi)” yazılır."><input className="ms-input" value={kaynak} maxLength={120} onChange={(e) => setKaynak(e.target.value)} /></Field>
        <div><button type="submit" className="m14-btn primary" disabled={gidiyor}><Plus aria-hidden /> {gidiyor ? 'Ekleniyor…' : 'Onaylı ekle'}</button></div>
      </form>
    </div>
  );
}
