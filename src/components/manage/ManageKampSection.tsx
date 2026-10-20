/**
 * Yönetim › Kamp tüyoları (/manage/kamp-tuyolari): öğrencilerin önerdiği hoca tüyoları (onayla / düzenleyip onayla /
 * reddet), onaylılar, reddedilenler ve yöneticinin doğrudan eklemesi. Uçlar services/kampRoutes.ts
 * (GET /api/admin/kamp/tuyolar, POST /api/admin/kamp/tuyo, POST /api/admin/kamp/tuyo/:id/karar). Onaylı tüyolar gece
 * kamp zincirinde (otomasyon/kamp_zinciri.py) kampa işlenir. Ortak kabuk consoleUi (ms-panel …).
 */
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { Check, Lightbulb, PencilLine, Plus, RefreshCw, Tent, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { KURULLAR, aktifKurul } from '../../services/kurulTakvimi';
import { toast } from '../ui/Toast';
import { ChipBar, EmptyState, Field, Panel, timeLabel } from './consoleUi';
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
  const gorunen = (liste || []).filter((t) => t.durum === suzgec).sort((a, b) => (b.zaman || '').localeCompare(a.zaman || ''));

  const karar = async (t: Tuyo, k: 'onayla' | 'reddet') => {
    const metin = duzen[t.id]?.trim();
    if (k === 'onayla' && metin !== undefined && metin.length < 8) { toast.error('Düzeltilmiş metin en az 8 karakter olmalı.'); return; }
    setMesgul(t.id);
    const r = await safeJsonFetch('/api/admin/kamp/tuyo/' + encodeURIComponent(t.id) + '/karar', {
      method: 'POST', headers, body: JSON.stringify({ karar: k, ...(k === 'onayla' && metin && metin !== t.metin ? { metin } : {}) }),
    });
    setMesgul('');
    if (!r.ok) { toast.error(r.error || 'Karar kaydedilemedi.'); return; }
    toast.success(k === 'onayla' ? 'Tüyo onaylandı; gece kampa işlenecek.' : 'Tüyo reddedildi.');
    setDuzen((d) => { const n = { ...d }; delete n[t.id]; return n; });
    void yukle();
  };

  return (
    <div className="grid gap-4">
      <Panel
        title="Kamp tüyoları" icon={Lightbulb} count={liste?.length ?? 0}
        desc="Öğrencilerin önerdiği hoca tüyoları. Onaylananlar gece kamp zincirinde ilgili kurul ve branşın kampına işlenir; kayıt silinmez, kararlar deftere eklenir."
        tools={<button type="button" className="ms-btn" onClick={() => void yukle()} disabled={yuk}><RefreshCw className={yuk ? 'animate-spin' : ''} aria-hidden /> Yenile</button>}
      >
        {hata && <p className="text-sm text-bad" role="alert">{hata}</p>}
        {!liste && !hata && <p className="text-sm text-ink-3">Yükleniyor…</p>}
        {liste && (
          <>
            <ChipBar value={suzgec} onChange={setSuzgec} label="Tüyo durumu" wrap
              options={(['oneri', 'onayli', 'reddedildi'] as Durum[]).map((d) => ({ id: d, label: DURUM_AD[d], n: say[d] }))} />
            {gorunen.length === 0 ? (
              <EmptyState icon={Tent} title={suzgec === 'oneri' ? 'Bekleyen öneri yok' : `${DURUM_AD[suzgec]} tüyo yok`}>
                {suzgec === 'oneri' ? 'Öğrenciler /kamp sayfasından tüyo önerdikçe burada görünür.' : undefined}
              </EmptyState>
            ) : (
              <ul className="grid gap-2 mt-3">
                {gorunen.map((t) => {
                  const d = duzen[t.id];
                  return (
                    <li key={t.id} className="ms-row !block rounded-xl border border-line p-3">
                      <div className="flex flex-wrap items-center gap-2 text-xs text-ink-3">
                        <b className="text-ink">Kurul {t.kurul} · {bransAdi(t.brans)}</b>
                        {t.ders_id && <span>{dersAdi(t.kurul, t.ders_id)}</span>}
                        <span>{timeLabel(t.zaman, true)}</span>
                        <span>{t.kaynak === 'ogrenci' ? `öğrenci${t.kim ? ` (${t.kim})` : ''}` : t.kaynak || ''}</span>
                        <code className="ml-auto">{t.id}</code>
                      </div>
                      {d !== undefined ? (
                        <textarea className="ms-input w-full mt-2 min-h-[88px]" value={d} maxLength={1500} onChange={(e) => setDuzen((x) => ({ ...x, [t.id]: e.target.value }))} aria-label="Tüyo metnini düzenle" />
                      ) : (
                        <p className="mt-2 text-[15px] leading-relaxed whitespace-pre-wrap break-words">{t.metin}</p>
                      )}
                      {t.durum !== 'onayli' && (
                        <div className="flex flex-wrap gap-2 mt-2">
                          <button type="button" className="ms-btn is-primary" disabled={mesgul === t.id} onClick={() => void karar(t, 'onayla')}>
                            <Check aria-hidden /> {d !== undefined ? 'Düzeltip onayla' : 'Onayla'}
                          </button>
                          {d === undefined
                            ? <button type="button" className="ms-btn" onClick={() => setDuzen((x) => ({ ...x, [t.id]: t.metin }))}><PencilLine aria-hidden /> Düzenle</button>
                            : <button type="button" className="ms-btn is-ghost" onClick={() => setDuzen((x) => { const n = { ...x }; delete n[t.id]; return n; })}>Düzenlemeyi bırak</button>}
                          {t.durum === 'oneri' && <button type="button" className="ms-btn is-warn" disabled={mesgul === t.id} onClick={() => void karar(t, 'reddet')}><X aria-hidden /> Reddet</button>}
                        </div>
                      )}
                    </li>
                  );
                })}
              </ul>
            )}
          </>
        )}
      </Panel>
      <YoneticiEkle headers={headers} onEklendi={() => { setSuzgec('onayli'); void yukle(); }} />
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
    <Panel title="Tüyo ekle" icon={Plus} desc="Yöneticinin girdiği tüyo doğrudan onaylı olur.">
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
        <div><button type="submit" className="ms-btn is-primary" disabled={gidiyor}><Plus aria-hidden /> {gidiyor ? 'Ekleniyor…' : 'Onaylı ekle'}</button></div>
      </form>
    </Panel>
  );
}
