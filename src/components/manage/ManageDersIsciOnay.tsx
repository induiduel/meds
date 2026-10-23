import React, { useEffect, useMemo, useRef, useState } from 'react';
import { FileAudio, FileText, Play, SkipForward, Trash2, Upload } from 'lucide-react';
import { getCustomApiUrl } from '../../services/api';
import { toast } from '../ui/Toast';
import { Card14, Pill } from '../v14/pageKit';

/**
 * Onay kapısı (2026-10-24): Drive'a gelen yeni ders PDF'i işlenmeden önce yönetici onayı bekler (telefona bildirim gider).
 * Yönetici öğrenci notu / ders ses kaydı yükleyip "Notlarla başlat" ya da "Yalnız PDF ile başlat" der; "Atla" işlemeden geçer.
 * Dosyalar site sunucusuna akar (/api/admin/ders-isci-ek, dersIsciEkRoutes.ts), işçi onayda iş kaydına alır (api.py _onay).
 */
type Ek = { ad: string; boyut: number };
type OnayIs = {
  is_id: string;
  ad: string;
  yol: string;
  konular: { konu: string; sayfa_bas?: number; sayfa_bit?: number }[];
  eklendi?: number;
  uyari?: string;
  ekler: { not: Ek[]; ses: Ek[] };
};
type Api = (yol: string, init?: RequestInit) => Promise<{ ok: boolean; data?: any; error?: string; status?: number }>;

const MB = (b: number) => `${(b / 1048576).toFixed(b > 10485760 ? 0 : 1)} MB`;
const ekUrl = (isId: string, q = '') => {
  const yol = `/api/admin/ders-isci-ek/${isId}${q}`;
  const kok = getCustomApiUrl(yol);
  return kok ? `${kok.replace(/\/$/, '')}${yol}` : yol;
};

/** Büyük ses dosyası için XHR (ilerleme + zaman aşımı yok); yönetici jetonu fetch yamasıyla değil burada eklenir. */
async function jeton(): Promise<string> {
  try {
    const { auth } = await import('../../services/auth');
    return (await auth?.currentUser?.getIdToken()) || '';
  } catch {
    return '';
  }
}

async function yukle(isId: string, tur: 'not' | 'ses', f: File, adminEmail: string, ilerle: (p: number) => void): Promise<void> {
  const t = await jeton();
  return new Promise((coz, red) => {
    const x = new XMLHttpRequest();
    x.open('POST', ekUrl(isId, `?tur=${tur}&ad=${encodeURIComponent(f.name)}`));
    x.setRequestHeader('Content-Type', 'application/octet-stream');
    if (adminEmail) x.setRequestHeader('x-admin-email', adminEmail);
    if (t) x.setRequestHeader('Authorization', `Bearer ${t}`);
    x.upload.onprogress = (e) => e.lengthComputable && ilerle(e.loaded / e.total);
    x.onload = () => {
      if (x.status >= 200 && x.status < 300) return coz();
      let m = `HTTP ${x.status}`;
      try { m = JSON.parse(x.responseText).hata || m; } catch { /* metin değil */ }
      red(new Error(m));
    };
    x.onerror = () => red(new Error('bağlantı hatası'));
    x.send(f);
  });
}

const EkAlani: React.FC<{
  isId: string; tur: 'not' | 'ses'; ekler: Ek[]; adminEmail: string; onDegisti: () => void;
}> = ({ isId, tur, ekler, adminEmail, onDegisti }) => {
  const girdi = useRef<HTMLInputElement>(null);
  const [ilerleme, setIlerleme] = useState<number | null>(null);
  const kabul = tur === 'not' ? '.pdf,.png,.jpg,.jpeg,.webp,.heic,.txt,.md,.docx' : 'audio/*,.m4a,.mp3,.wav,.ogg,.opus,.webm,.mp4,.amr,.3gp';
  const sec = async (dosyalar: FileList | null) => {
    if (!dosyalar?.length) return;
    for (const f of Array.from(dosyalar)) {
      try {
        setIlerleme(0);
        await yukle(isId, tur, f, adminEmail, setIlerleme);
        toast.success(`${f.name} yüklendi`);
      } catch (e: any) {
        toast.error(`${f.name}: ${e.message}`);
      }
    }
    setIlerleme(null);
    if (girdi.current) girdi.current.value = '';
    onDegisti();
  };
  const sil = async (ad: string) => {
    await fetch(ekUrl(isId, `?tur=${tur}&ad=${encodeURIComponent(ad)}`), { method: 'DELETE', headers: { 'x-admin-email': adminEmail } }).catch(() => null);
    onDegisti();
  };
  const Ikon = tur === 'not' ? FileText : FileAudio;
  return (
    <div className="flex flex-col gap-1" style={{ minWidth: 0 }}>
      <div className="flex items-center gap-2 flex-wrap">
        <b className="text-sm">{tur === 'not' ? 'Öğrenci notu' : 'Ders ses kaydı'}</b>
        <button type="button" className="m14-btn ghost" disabled={ilerleme !== null} onClick={() => girdi.current?.click()}>
          <Upload aria-hidden /> {ilerleme !== null ? `Yükleniyor %${Math.round(ilerleme * 100)}` : 'Dosya seç'}
        </button>
        <input ref={girdi} type="file" accept={kabul} multiple hidden onChange={(e) => sec(e.target.files)} />
      </div>
      {ekler.length === 0 ? (
        <span className="text-xs text-ink-3">{tur === 'not' ? 'PDF, fotoğraf, metin ya da Word (en çok 50 MB)' : 'Telefon kaydı vb. (en çok 600 MB)'}</span>
      ) : (
        <ul className="text-xs" style={{ margin: 0, paddingLeft: 0, listStyle: 'none' }}>
          {ekler.map((e) => (
            <li key={e.ad} className="flex items-center gap-2">
              <Ikon size={14} aria-hidden /> <span style={{ overflowWrap: 'anywhere' }}>{e.ad}</span>
              <span className="text-ink-3">{MB(e.boyut)}</span>
              <button type="button" className="m14-btn ghost" aria-label={`${e.ad} dosyasını kaldır`} onClick={() => sil(e.ad)}>
                <Trash2 aria-hidden />
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export const OnayKapisi: React.FC<{ api: Api; adminEmail: string; onDegisti: () => void; tazele: number }> = ({
  api, adminEmail, onDegisti, tazele,
}) => {
  const [liste, setListe] = useState<OnayIs[] | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const vurgu = useMemo(() => {
    try { return new URLSearchParams(window.location.search).get('onay'); } catch { return null; }
  }, []);
  const getir = async () => {
    const r = await api('/onay');
    setListe(r.ok && Array.isArray(r.data) ? r.data : []);
  };
  useEffect(() => { void getir(); }, [tazele]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (vurgu && liste?.some((x) => x.is_id === vurgu)) document.getElementById(`onay-${vurgu}`)?.scrollIntoView({ block: 'center' });
  }, [vurgu, liste]);
  if (!liste?.length) return null;

  const eylem = async (x: OnayIs, yol: 'onayla' | 'onay-atla', mod?: 'ekli' | 'yalniz_pdf') => {
    setBusy(x.is_id);
    const r = await api(`/kuyruk/${x.is_id}/${yol}`, { method: 'POST', body: JSON.stringify(mod ? { mod } : {}) });
    setBusy(null);
    if (!r.ok) return toast.error(r.data?.hata || r.error || 'İşlem yapılamadı');
    toast.success(yol === 'onay-atla' ? `${x.ad} işlenmeden geçildi` : `${x.ad} kuyruğa alındı`);
    await getir();
    onDegisti();
  };

  return (
    <Card14 title={<>Onay bekleyen yeni PDF'ler <Pill tone="warn">{liste.length}</Pill></>}>
      <p className="text-sm text-ink-2" style={{ marginTop: 0 }}>
        Drive'a gelen ders PDF'i siz başlatmadan işlenmez. Varsa öğrenci notunu ve dersin ses kaydını yükleyin: hocanın vurguladığı
        noktalar ve sesli anlatımdaki "Burası önemli" bunlara dayanır. Yoksa yalnız PDF ile başlatın.
      </p>
      <div className="flex flex-col gap-3">
        {liste.map((x) => {
          const ekVar = x.ekler.not.length + x.ekler.ses.length > 0;
          return (
            <div
              key={x.is_id}
              id={`onay-${x.is_id}`}
              className="flex flex-col gap-2"
              style={{ border: '1px solid var(--line, rgba(127,127,127,.25))', borderRadius: 12, padding: 12,
                       outline: vurgu === x.is_id ? '2px solid var(--acc, #3b82f6)' : undefined }}
            >
              <div className="flex items-center gap-2 flex-wrap">
                <b style={{ overflowWrap: 'anywhere' }}>{x.ad.replace(/\.pdf$/i, '')}</b>
                {x.uyari && <Pill tone="warn">{x.uyari}</Pill>}
              </div>
              <div className="text-xs text-ink-3" style={{ overflowWrap: 'anywhere' }}>
                {x.konular.map((k) => `${k.konu}${k.sayfa_bas ? ` (s. ${k.sayfa_bas}–${k.sayfa_bit})` : ''}`).join(' · ') || x.yol}
              </div>
              <div className="grid gap-3" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))' }}>
                <EkAlani isId={x.is_id} tur="not" ekler={x.ekler.not} adminEmail={adminEmail} onDegisti={getir} />
                <EkAlani isId={x.is_id} tur="ses" ekler={x.ekler.ses} adminEmail={adminEmail} onDegisti={getir} />
              </div>
              <div className="flex gap-2 flex-wrap">
                <button type="button" className="m14-btn" disabled={!ekVar || busy === x.is_id} onClick={() => eylem(x, 'onayla', 'ekli')}
                        title={ekVar ? undefined : 'Önce not ya da ses kaydı yükleyin'}>
                  <Play aria-hidden /> Notlarla başlat
                </button>
                <button type="button" className="m14-btn ghost" disabled={busy === x.is_id} onClick={() => eylem(x, 'onayla', 'yalniz_pdf')}>
                  <Play aria-hidden /> Yalnız PDF ile başlat
                </button>
                <button type="button" className="m14-btn ghost" disabled={busy === x.is_id}
                        onClick={() => { if (window.confirm(`${x.ad} işlenmeden geçilsin mi? (Yeniden taramada kuyruğa girmez.)`)) void eylem(x, 'onay-atla'); }}>
                  <SkipForward aria-hidden /> Atla
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </Card14>
  );
};
