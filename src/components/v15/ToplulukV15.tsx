import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { ChevronRight, Flag, Hash, MessageCircle, Reply, Send, Trash2, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { auth, getRememberedStudentInfo } from '../../services/auth';
import { useLiveEvent } from '../../hooks/useLiveEvent';
import { aktifKurul } from '../../services/kurulTakvimi';
import { navigateTo } from '../../router';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';
import '../../styles/v15/topluluk.css';

/**
 * v15 · Topluluk (tasarım sistemi v15 › L01–L06). Yeni sayfa: /topluluk[?kanal=…] (Menü › Ben).
 * Kanallar: Genel, Kurul N, ders yorumları (ders:<anahtar>, ders ayrıntısındaki "Yorumlar"dan açılır).
 * Sunucu: services/topluluk.ts (meds-pg, doğrulanmış kimlik, hız sınırı, şikâyet → 3'te gizlenir). Canlı: SSE `topluluk`.
 * Görünen ad cihazda tutulur; e-posta ya da uid hiçbir yerde gösterilmez.
 */
interface Mesaj { id: number; kanal: string; ad: string; metin: string; yanitId: number | null; at: number; yazar: string; benim: boolean; sikayet?: number }
interface KanalOzet { kanal: string; n: number; son: number }
const AD_KEY = 'medsoru_topluluk_ad';
const kanalAdi = (k: string) => (k === 'genel' ? 'Genel' : k.startsWith('kurul-') ? `Kurul ${k.slice(6)}` : `Ders yorumları · ${k.slice(5).replace(/^y\d+-/, '').replace(/^k\d+-\d+-/, '').replace(/-/g, ' ')}`);
const kanalAlt = (k: string) => (k === 'genel' ? 'Herkesle sohbet' : k.startsWith('kurul-') ? 'Bu kurulun dersleri ve sınavı' : 'Bu ders hakkında soru ve notlar');
const saat = (t: number) => {
  const d = new Date(t), b = new Date();
  return d.toDateString() === b.toDateString() ? d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }) : d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
};
/** yazar özetinden sabit ton (renk kimlik değil, ayırt etmek için; ad her zaman yazılı) */
const ton = (s: string) => parseInt(s.slice(0, 4), 16) % 360;

export default function ToplulukV15() {
  const [kanal, setKanal0] = useState(() => new URLSearchParams(location.search).get('kanal') || '');
  useEffect(() => { const f = () => setKanal0(new URLSearchParams(location.search).get('kanal') || ''); window.addEventListener('popstate', f); return () => window.removeEventListener('popstate', f); }, []);
  const setKanal = (k: string) => { navigateTo(k ? `/topluluk?kanal=${encodeURIComponent(k)}` : '/topluluk'); setKanal0(k); };
  return kanal ? <Sohbet kanal={kanal} /> : <Kanallar ac={setKanal} />;
}

function Kanallar({ ac }: { ac: (k: string) => void }) {
  const [ozet, setOzet] = useState<KanalOzet[] | null>(null);
  const [hata, setHata] = useState('');
  useV15Baslik({ baslik: 'Topluluk', alt: 'Sohbet ve ders yorumları' });
  const yukle = useCallback(() => safeJsonFetch<{ kanallar: KanalOzet[] }>('/api/topluluk/kanallar').then((r) => {
    if (r.ok) { setOzet(r.data?.kanallar || []); setHata(''); } else { setOzet([]); setHata(r.data && (r.data as any).error || 'Topluluğa ulaşılamadı.'); }
  }), []);
  useEffect(() => { void yukle(); }, [yukle]);
  useLiveEvent('topluluk', () => void yukle(), { debounceMs: 1500 });
  const m = new Map((ozet || []).map((k) => [k.kanal, k]));
  const ak = aktifKurul().kurul;
  const sabit = ['genel', `kurul-${ak}`, ...[1, 2, 3, 4, 5, 6].filter((k) => k !== ak).map((k) => `kurul-${k}`)];
  const dersler = (ozet || []).filter((k) => k.kanal.startsWith('ders:')).sort((a, b) => b.son - a.son);
  const satir = (k: string) => {
    const o = m.get(k);
    return (
      <li key={k}>
        <button type="button" className="b15-row" onClick={() => ac(k)}>
          <span className={`v15-tile${o ? '' : ' is-n'}`}>{k.startsWith('ders:') ? <MessageCircle aria-hidden /> : <Hash aria-hidden />}</span>
          <span className="b15-row-t"><b>{kanalAdi(k)}</b><span>{o ? `${o.n} mesaj · son ${saat(o.son)}` : kanalAlt(k)}</span></span>
          <ChevronRight className="v15-chev" aria-hidden />
        </button>
      </li>
    );
  };
  return (
    <div className="tp15">
      <h1 className="sr-only">Topluluk</h1>
      {hata && <p className="tp15-uyari v15-card">{hata}</p>}
      <h2 className="v15-cap tp15-h">Kanallar</h2>
      <ul className="b15-list v15-card">{sabit.map(satir)}</ul>
      <h2 className="v15-cap tp15-h">Ders yorumları</h2>
      {dersler.length ? <ul className="b15-list v15-card">{dersler.map((k) => satir(k.kanal))}</ul>
        : <p className="b15-bos v15-card">Henüz ders yorumu yok. Bir dersin sayfasındaki "Yorumlar" ile o derse yorum yazabilirsin.</p>}
      <p className="v15-cap tp15-kural">Saygılı ol; kişisel bilgi, sınav sorusu fotoğrafı ya da reklam paylaşma. Uygunsuz mesajı bayrakla bildir; üç bildirimde mesaj gizlenir.</p>
    </div>
  );
}

function Sohbet({ kanal }: { kanal: string }) {
  const [mesajlar, setMesajlar] = useState<Mesaj[] | null>(null);
  const [dahaVar, setDahaVar] = useState(false);
  const [girisli, setGirisli] = useState(true);
  const [metin, setMetin] = useState('');
  const [ad, setAd] = useState(() => { try { return localStorage.getItem(AD_KEY) || ''; } catch { return ''; } });
  const [yanit, setYanit] = useState<Mesaj | null>(null);
  const [hata, setHata] = useState('');
  const [gonderiyor, setGonderiyor] = useState(false);
  const liste = useRef<HTMLDivElement>(null);
  const altta = useRef(true);
  useV15Baslik({ baslik: kanalAdi(kanal), alt: 'Topluluk', geri: '/topluluk' });

  const yukle = useCallback(async () => {
    const r = await safeJsonFetch<{ mesajlar: Mesaj[]; dahaVar: boolean; girisli: boolean }>(`/api/topluluk/mesajlar?kanal=${encodeURIComponent(kanal)}`);
    if (r.ok && r.data) { setMesajlar(r.data.mesajlar); setDahaVar(r.data.dahaVar); setGirisli(r.data.girisli || !!auth.currentUser); }
    else { setMesajlar((m) => m || []); setHata((r.data as any)?.error || 'Mesajlar alınamadı.'); }
  }, [kanal]);
  useEffect(() => { setMesajlar(null); void yukle(); }, [yukle]);
  useLiveEvent('topluluk', (p) => { if (!p || p.resync || p.kanal === kanal) void yukle(); }, { debounceMs: 200 });
  const eskiler = async () => {
    const ilk = mesajlar?.[0]?.id; if (!ilk) return;
    const r = await safeJsonFetch<{ mesajlar: Mesaj[]; dahaVar: boolean }>(`/api/topluluk/mesajlar?kanal=${encodeURIComponent(kanal)}&once=${ilk}`);
    if (r.ok && r.data) { altta.current = false; setMesajlar((m) => [...r.data!.mesajlar, ...(m || [])]); setDahaVar(r.data.dahaVar); }
  };
  useLayoutEffect(() => { const el = liste.current; if (el && altta.current) el.scrollTop = el.scrollHeight; }, [mesajlar]);
  const kaydir = () => { const el = liste.current; if (el) altta.current = el.scrollHeight - el.scrollTop - el.clientHeight < 80; };

  const gonder = async () => {
    const t = metin.trim(); if (!t || gonderiyor) return;
    const gorunen = ad.trim() || (auth.currentUser?.displayName || getRememberedStudentInfo().name || 'Öğrenci').split(' ')[0];
    setGonderiyor(true); setHata('');
    const r = await safeJsonFetch<{ mesaj: Mesaj }>('/api/topluluk/mesaj', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ kanal, metin: t, ad: gorunen, yanitId: yanit?.id }) });
    setGonderiyor(false);
    if (r.ok && r.data?.mesaj) {
      altta.current = true; setMetin(''); setYanit(null);
      try { if (ad.trim()) localStorage.setItem(AD_KEY, ad.trim()); } catch { /* yok */ }
      setMesajlar((m) => (m?.some((x) => x.id === r.data!.mesaj.id) ? m : [...(m || []), r.data!.mesaj]));
    } else setHata((r.data as any)?.error || r.error || 'Gönderilemedi.');
  };
  const sil = async (x: Mesaj) => {
    if (!confirm('Mesaj silinsin mi?')) return;
    const r = await safeJsonFetch(`/api/topluluk/mesaj/${x.id}/sil`, { method: 'POST' });
    if (r.ok) setMesajlar((m) => (m || []).filter((y) => y.id !== x.id)); else setHata((r.data as any)?.error || 'Silinemedi.');
  };
  const bildir = async (x: Mesaj) => {
    if (!confirm('Bu mesajı uygunsuz olarak bildir?')) return;
    const r = await safeJsonFetch(`/api/topluluk/mesaj/${x.id}/sikayet`, { method: 'POST' });
    setHata(r.ok ? 'Bildirdin, teşekkürler.' : (r.data as any)?.error || 'Bildirilemedi.');
  };
  const byId = useMemo(() => new Map((mesajlar || []).map((x) => [x.id, x])), [mesajlar]);

  return (
    <div className="tp15 tp15-s">
      <div ref={liste} className="tp15-liste" onScroll={kaydir} aria-live="polite">
        {dahaVar && <button type="button" className="tp15-eski" onClick={eskiler}>Daha eski mesajlar</button>}
        {mesajlar === null ? <span className="v15-skel b15-skel" aria-hidden /> : !mesajlar.length ? (
          <p className="tp15-bos">{kanalAlt(kanal)}. İlk mesajı sen yaz.</p>
        ) : mesajlar.map((x, i) => {
          const onceki = mesajlar[i - 1];
          const grup = onceki && onceki.yazar === x.yazar && x.at - onceki.at < 5 * 60_000 && !x.yanitId;
          const y = x.yanitId ? byId.get(x.yanitId) : null;
          return (
            <article key={x.id} className={`tp15-m${x.benim ? ' is-ben' : ''}${grup ? ' is-grup' : ''}`} style={{ '--t': ton(x.yazar) } as React.CSSProperties}>
              {!grup && <header><b>{x.benim ? 'Sen' : x.ad}</b><time>{saat(x.at)}</time>{x.sikayet ? <span className="tp15-sk">{x.sikayet} bildirim</span> : null}</header>}
              <div className="tp15-balon">
                {x.yanitId && <p className="tp15-alinti">{y ? <><b>{y.ad}:</b> {y.metin.slice(0, 90)}</> : 'Silinmiş mesaja yanıt'}</p>}
                <p>{x.metin}</p>
              </div>
              <div className="tp15-is">
                <button type="button" onClick={() => setYanit(x)} aria-label="Yanıtla"><Reply aria-hidden /></button>
                {x.benim || x.sikayet !== undefined ? <button type="button" onClick={() => sil(x)} aria-label="Sil"><Trash2 aria-hidden /></button>
                  : <button type="button" onClick={() => bildir(x)} aria-label="Uygunsuz olarak bildir"><Flag aria-hidden /></button>}
              </div>
            </article>
          );
        })}
      </div>
      <div className="tp15-yaz v15-card">
        {hata && <p className="tp15-hata" role="status">{hata}</p>}
        {!girisli ? <p className="v15-cap">Yazmak için giriş yapmalısın.</p> : (
          <>
            {yanit && <p className="tp15-yanit"><Reply aria-hidden /><span><b>{yanit.ad}</b> · {yanit.metin.slice(0, 70)}</span><button type="button" onClick={() => setYanit(null)} aria-label="Yanıtı kaldır"><X aria-hidden /></button></p>}
            {!ad && <input className="tp15-ad" value={ad} onChange={(e) => setAd(e.target.value.slice(0, 24))} placeholder="Görünen adın (isteğe bağlı)" aria-label="Görünen ad" />}
            <div className="tp15-giris">
              <textarea value={metin} onChange={(e) => setMetin(e.target.value.slice(0, 800))} placeholder="Mesaj yaz…" rows={1} aria-label="Mesaj"
                onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); void gonder(); } }} />
              <button type="button" className="tp15-gonder" onClick={gonder} disabled={!metin.trim() || gonderiyor} aria-label="Gönder"><Send aria-hidden /></button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
