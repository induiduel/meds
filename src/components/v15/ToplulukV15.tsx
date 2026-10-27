import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { ChevronRight, Flag, Hash, Heart, Link2, LogOut, Mail, MessageCircle, MessagesSquare, Reply, Search, Send, SquarePen, Trash2, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';
import { auth, getRememberedStudentInfo } from '../../services/auth';
import { useLiveEvent } from '../../hooks/useLiveEvent';
import { aktifKurul } from '../../services/kurulTakvimi';
import { navigateTo } from '../../router';
import { useV15Baslik } from './baslik';
import '../../styles/v15/ogren.css';
import '../../styles/v15/dersler.css';
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

interface SohbetOzet { id: number; tur: 'dm' | 'grup'; ad: string; kod?: string; uyeN: number; okunmamis: number; son: { ad: string; metin: string; at: number } | null; at: number }
interface Yorum extends Mesaj { begeni: number; begendim: boolean; yanitlar?: Yorum[] }
const benimAd = () => { try { const a = localStorage.getItem(AD_KEY); if (a) return a; } catch { /* yok */ } return (auth.currentUser?.displayName || getRememberedStudentInfo().name || 'Öğrenci').split(' ')[0]; };
const basHarf = (s: string) => s.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toLocaleUpperCase('tr-TR') || '?';
const kisaZaman = (t: number) => {
  const dk = Math.round((Date.now() - t) / 60_000);
  if (dk < 1) return 'şimdi'; if (dk < 60) return `${dk} dk`; if (dk < 24 * 60) return `${Math.round(dk / 60)} sa`;
  if (dk < 48 * 60) return 'dün'; return new Date(t).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};
const post = <T,>(url: string, body?: any) => safeJsonFetch<T>(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) });

type Gorunum = { t: 'kanallar' } | { t: 'kanal'; k: string } | { t: 'sohbetler' } | { t: 'oda'; id: number } | { t: 'yorum'; k: string } | { t: 'katil'; kod: string };
const oku = (): Gorunum => {
  const q = new URLSearchParams(location.search);
  if (q.get('katil')) return { t: 'katil', kod: q.get('katil')! };
  if (Number(q.get('sohbet'))) return { t: 'oda', id: Number(q.get('sohbet')) };
  if (q.get('gorunum') === 'sohbetler') return { t: 'sohbetler' };
  if (q.get('yorum')) return { t: 'yorum', k: q.get('yorum')! };
  if (q.get('kanal')) return { t: 'kanal', k: q.get('kanal')! };
  return { t: 'kanallar' };
};
const git = (adres: string) => { navigateTo(adres); window.dispatchEvent(new PopStateEvent('popstate')); };

export default function ToplulukV15() {
  const [g, setG] = useState<Gorunum>(oku);
  useEffect(() => { const f = () => setG(oku()); window.addEventListener('popstate', f); return () => window.removeEventListener('popstate', f); }, []);
  if (g.t === 'kanal') return <Sohbet key={g.k} kanal={g.k} />;
  if (g.t === 'oda') return <Sohbet key={`oda${g.id}`} kanal={`oda:${g.id}`} oda={g.id} />;
  if (g.t === 'sohbetler') return <SohbetListe />;
  if (g.t === 'yorum') return <Yorumlar key={g.k} kanal={g.k} />;
  if (g.t === 'katil') return <Katil kod={g.kod} />;
  return <Kanallar ac={(k) => git(`/topluluk?kanal=${encodeURIComponent(k)}`)} />;
}

/** L01 · Sohbet listesi: grup ve birebir sohbetler, arama, yeni grup (davet bağlantısıyla) */
function SohbetListe() {
  const [liste, setListe] = useState<SohbetOzet[] | null>(null);
  const [girisli, setGirisli] = useState(true);
  const [ara, setAra] = useState('');
  const [yeni, setYeni] = useState(false);
  const [grupAd, setGrupAd] = useState('');
  const [hata, setHata] = useState('');
  useV15Baslik({ baslik: 'Sohbet', alt: 'Topluluk', geri: '/topluluk' });
  const yukle = useCallback(() => safeJsonFetch<{ sohbetler: SohbetOzet[]; girisli: boolean }>('/api/topluluk/sohbetler').then((r) => {
    if (r.ok && r.data) { setListe(r.data.sohbetler); setGirisli(r.data.girisli); setHata(''); }
    else { setListe((l) => l || []); setHata((r.data as any)?.error || 'Sohbetler alınamadı.'); }
  }), []);
  useEffect(() => { void yukle(); }, [yukle]);
  useLiveEvent('topluluk_sohbet', () => void yukle(), { debounceMs: 600 });
  const olustur = async () => {
    const ad = grupAd.trim(); if (!ad) return;
    const r = await post<{ id: number }>('/api/topluluk/sohbet', { tur: 'grup', ad, benAd: benimAd() });
    if (r.ok && r.data?.id) git(`/topluluk?sohbet=${r.data.id}`); else setHata((r.data as any)?.error || 'Grup kurulamadı.');
  };
  const q = ara.trim().toLocaleLowerCase('tr-TR');
  const gorunen = (liste || []).filter((s) => !q || `${s.ad} ${s.son?.metin || ''}`.toLocaleLowerCase('tr-TR').includes(q));
  return (
    <div className="tp15">
      <h1 className="sr-only">Sohbet</h1>
      <div className="tp15-arac">
        <label className="tp15-ara"><Search aria-hidden /><input value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Sohbet ara" aria-label="Sohbet ara" /></label>
        <button type="button" className="tp15-ib" onClick={() => setYeni((v) => !v)} aria-label="Yeni sohbet" aria-expanded={yeni}><SquarePen aria-hidden /></button>
      </div>
      {yeni && (
        <div className="tp15-yeni v15-card">
          <b>Yeni grup</b>
          <div className="tp15-giris">
            <input className="tp15-ad" value={grupAd} onChange={(e) => setGrupAd(e.target.value.slice(0, 60))} placeholder="Grup adı (ör. Patoloji çalışma)" aria-label="Grup adı"
              onKeyDown={(e) => { if (e.key === 'Enter') void olustur(); }} />
            <button type="button" className="v15-btn" onClick={olustur} disabled={!grupAd.trim()}>Kur</button>
          </div>
          <p className="v15-cap">Kurduktan sonra davet bağlantısını paylaş. Birebir sohbet için bir kanalda kişinin mesajındaki zarf simgesine dokun.</p>
        </div>
      )}
      {hata && <p className="tp15-uyari v15-card">{hata}</p>}
      {!girisli ? <p className="b15-bos v15-card">Sohbetleri görmek için giriş yapmalısın.</p>
        : liste === null ? <span className="v15-skel b15-skel" aria-hidden />
        : !gorunen.length ? <p className="b15-bos v15-card">{q ? 'Aramana uyan sohbet yok.' : 'Henüz sohbetin yok. Kalem simgesiyle bir grup kur ya da bir kanalda birine özel mesaj gönder.'}</p>
        : (
          <ul className="b15-list v15-card">
            {gorunen.map((s) => (
              <li key={s.id}>
                <button type="button" className="b15-row tp15-sr" onClick={() => git(`/topluluk?sohbet=${s.id}`)}>
                  <span className="tp15-av" style={{ '--t': (s.id * 47) % 360 } as React.CSSProperties}>{basHarf(s.ad)}</span>
                  <span className="b15-row-t"><b>{s.ad}</b><span>{s.son ? `${s.son.ad}: ${s.son.metin}` : s.tur === 'grup' ? `${s.uyeN} üye · henüz mesaj yok` : 'Henüz mesaj yok'}</span></span>
                  <span className="tp15-sag"><time>{kisaZaman(s.at)}</time>{s.okunmamis > 0 && <span className="tp15-rozet">{s.okunmamis > 99 ? '99+' : s.okunmamis}</span>}</span>
                </button>
              </li>
            ))}
          </ul>
        )}
    </div>
  );
}

function Katil({ kod }: { kod: string }) {
  const [hata, setHata] = useState('');
  useV15Baslik({ baslik: 'Gruba katıl', alt: 'Topluluk', geri: '/topluluk?gorunum=sohbetler' });
  const katil = async () => {
    const r = await post<{ id: number }>('/api/topluluk/sohbet/katil', { kod, benAd: benimAd() });
    if (r.ok && r.data?.id) git(`/topluluk?sohbet=${r.data.id}`); else setHata((r.data as any)?.error || r.error || 'Katılınamadı.');
  };
  return (
    <div className="tp15">
      <div className="b15-bos v15-card">
        <span>Bir sohbet grubuna davet edildin. Katılınca görünen adın grup üyelerine gösterilir.</span>
        {hata && <span className="tp15-hata">{hata}</span>}
        <button type="button" className="v15-btn" onClick={katil}>Gruba katıl</button>
      </div>
    </div>
  );
}

/** L03 · Yorumlar: ders/soru yorumları, En faydalı | En yeni, beğeni (kişi başına bir), yanıtla */
function Yorumlar({ kanal }: { kanal: string }) {
  const [sira, setSira] = useState<'faydali' | 'yeni'>('faydali');
  const [veri, setVeri] = useState<{ yorumlar: Yorum[]; toplam: number; girisli: boolean } | null>(null);
  const [metin, setMetin] = useState('');
  const [yanit, setYanit] = useState<Yorum | null>(null);
  const [hata, setHata] = useState('');
  const [gonderiyor, setGonderiyor] = useState(false);
  const alt = kanal.startsWith('soru:') ? `Soru ${kanal.slice(5)}` : kanalAdi(kanal).replace(/^Ders yorumları · /, '');
  useV15Baslik({ baslik: 'Yorumlar', alt: veri ? `${alt} · ${veri.toplam} yorum` : alt, geri: '/topluluk' });
  const yukle = useCallback(async () => {
    const r = await safeJsonFetch<{ yorumlar: Yorum[]; toplam: number; girisli: boolean }>(`/api/topluluk/yorumlar?kanal=${encodeURIComponent(kanal)}&sira=${sira}`);
    if (r.ok && r.data) { setVeri({ ...r.data, girisli: r.data.girisli || !!auth.currentUser }); }
    else { setVeri((v) => v || { yorumlar: [], toplam: 0, girisli: !!auth.currentUser }); setHata((r.data as any)?.error || 'Yorumlar alınamadı.'); }
  }, [kanal, sira]);
  useEffect(() => { void yukle(); }, [yukle]);
  useLiveEvent('topluluk', (p) => { if (!p || p.resync || p.kanal === kanal) void yukle(); }, { debounceMs: 400 });
  const begen = async (y: Yorum) => {
    const r = await post<{ begendim: boolean; begeni: number }>(`/api/topluluk/mesaj/${y.id}/begen`);
    if (!r.ok || !r.data) return setHata((r.data as any)?.error || 'Beğenilemedi.');
    const { begendim, begeni } = r.data;
    const g = (l: Yorum[]): Yorum[] => l.map((x) => (x.id === y.id ? { ...x, begendim, begeni } : { ...x, yanitlar: x.yanitlar && g(x.yanitlar) }));
    setVeri((v) => v && { ...v, yorumlar: g(v.yorumlar) });
  };
  const gonder = async () => {
    const t = metin.trim(); if (!t || gonderiyor) return;
    setGonderiyor(true); setHata('');
    const r = await post<{ mesaj: Mesaj }>('/api/topluluk/mesaj', { kanal, metin: t, ad: benimAd(), yanitId: yanit?.id });
    setGonderiyor(false);
    if (r.ok) { setMetin(''); setYanit(null); void yukle(); } else setHata((r.data as any)?.error || r.error || 'Gönderilemedi.');
  };
  const satir = (y: Yorum, ic = false) => (
    <div className={ic ? 'tp15-yic' : ''} style={{ '--t': ton(y.yazar) } as React.CSSProperties}>
      <div className="tp15-yb"><span className={`tp15-av${ic ? ' is-k' : ''}`}>{basHarf(y.benim ? 'Sen' : y.ad)}</span><b>{y.benim ? 'Sen' : y.ad}</b></div>
      <p className="tp15-ym">{y.metin}</p>
      <div className="tp15-yis">
        <button type="button" className={y.begendim ? 'is-on' : ''} onClick={() => begen(y)} aria-pressed={y.begendim} aria-label={`Beğen, ${y.begeni} beğeni`} disabled={!veri?.girisli}><Heart aria-hidden />{y.begeni}</button>
        {!ic && veri?.girisli && <button type="button" onClick={() => setYanit(y)}>Yanıtla</button>}
        <time>{kisaZaman(y.at)}</time>
      </div>
    </div>
  );
  return (
    <div className="tp15">
      <h1 className="sr-only">Yorumlar</h1>
      <div className="v15-seg tp15-seg" role="tablist" aria-label="Sıralama">
        {(['faydali', 'yeni'] as const).map((s) => <button key={s} type="button" role="tab" aria-selected={sira === s} className={sira === s ? 'is-on' : ''} onClick={() => setSira(s)}>{s === 'faydali' ? 'En faydalı' : 'En yeni'}</button>)}
      </div>
      {veri === null ? <span className="v15-skel b15-skel" aria-hidden />
        : !veri.yorumlar.length ? <p className="b15-bos v15-card">Henüz yorum yok. İlk yorumu sen yaz.</p>
        : veri.yorumlar.map((y) => (
          <article key={y.id} className="v15-card tp15-yorum">
            {satir(y)}
            {y.yanitlar?.map((x) => <React.Fragment key={x.id}>{satir(x, true)}</React.Fragment>)}
          </article>
        ))}
      <div className="tp15-yaz v15-card">
        {hata && <p className="tp15-hata" role="status">{hata}</p>}
        {!veri?.girisli ? <p className="v15-cap">Yorum yazmak için giriş yapmalısın.</p> : (
          <>
            {yanit && <p className="tp15-yanit"><Reply aria-hidden /><span><b>{yanit.ad}</b> · {yanit.metin.slice(0, 70)}</span><button type="button" onClick={() => setYanit(null)} aria-label="Yanıtı kaldır"><X aria-hidden /></button></p>}
            <div className="tp15-giris">
              <textarea value={metin} onChange={(e) => setMetin(e.target.value.slice(0, 800))} placeholder="Yorum yaz…" rows={1} aria-label="Yorum" />
              <button type="button" className="tp15-gonder" onClick={gonder} disabled={!metin.trim() || gonderiyor} aria-label="Gönder"><Send aria-hidden /></button>
            </div>
          </>
        )}
      </div>
    </div>
  );
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
        <button type="button" className="b15-row" onClick={() => (k.startsWith('ders:') ? git(`/topluluk?yorum=${encodeURIComponent(k)}`) : ac(k))}>
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
      <ul className="b15-list v15-card">
        <li><button type="button" className="b15-row" onClick={() => git('/topluluk?gorunum=sohbetler')}>
          <span className="v15-tile"><MessagesSquare aria-hidden /></span>
          <span className="b15-row-t"><b>Sohbet</b><span>Grup ve birebir sohbetlerin</span></span>
          <ChevronRight className="v15-chev" aria-hidden />
        </button></li>
      </ul>
      <h2 className="v15-cap tp15-h">Kanallar</h2>
      <ul className="b15-list v15-card">{sabit.map(satir)}</ul>
      <h2 className="v15-cap tp15-h">Ders yorumları</h2>
      {dersler.length ? <ul className="b15-list v15-card">{dersler.map((k) => satir(k.kanal))}</ul>
        : <p className="b15-bos v15-card">Henüz ders yorumu yok. Bir dersin sayfasındaki "Yorumlar" ile o derse yorum yazabilirsin.</p>}
      <p className="v15-cap tp15-kural">Saygılı ol; kişisel bilgi, sınav sorusu fotoğrafı ya da reklam paylaşma. Uygunsuz mesajı bayrakla bildir; üç bildirimde mesaj gizlenir.</p>
    </div>
  );
}

function Sohbet({ kanal, oda }: { kanal: string; oda?: number }) {
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
  const [odaBilgi, setOdaBilgi] = useState<{ ad: string; tur: string; kod?: string; uyeler: string[] } | null>(null);
  useV15Baslik(oda ? { baslik: odaBilgi?.ad || 'Sohbet', alt: odaBilgi?.tur === 'grup' ? `${odaBilgi.uyeler.length} üye` : 'Birebir sohbet', geri: '/topluluk?gorunum=sohbetler' }
    : { baslik: kanalAdi(kanal), alt: 'Topluluk', geri: '/topluluk' });

  const yukle = useCallback(async () => {
    if (oda) {
      const r = await safeJsonFetch<{ oda: any; mesajlar: Mesaj[]; dahaVar: boolean }>(`/api/topluluk/sohbet/${oda}`);
      if (r.ok && r.data) { setOdaBilgi(r.data.oda); setMesajlar(r.data.mesajlar); setDahaVar(r.data.dahaVar); setGirisli(true); void post(`/api/topluluk/sohbet/${oda}/okundu`); }
      else { setMesajlar((m) => m || []); setHata((r.data as any)?.error || 'Sohbet açılamadı.'); }
      return;
    }
    const r = await safeJsonFetch<{ mesajlar: Mesaj[]; dahaVar: boolean; girisli: boolean }>(`/api/topluluk/mesajlar?kanal=${encodeURIComponent(kanal)}`);
    if (r.ok && r.data) { setMesajlar(r.data.mesajlar); setDahaVar(r.data.dahaVar); setGirisli(r.data.girisli || !!auth.currentUser); }
    else { setMesajlar((m) => m || []); setHata((r.data as any)?.error || 'Mesajlar alınamadı.'); }
  }, [kanal, oda]);
  useEffect(() => { setMesajlar(null); void yukle(); }, [yukle]);
  useLiveEvent(oda ? 'topluluk_sohbet' : 'topluluk', (p) => { if (!p || p.resync || (oda ? p.oda === oda : p.kanal === kanal)) void yukle(); }, { debounceMs: 200 });
  const eskiler = async () => {
    const ilk = mesajlar?.[0]?.id; if (!ilk) return;
    const r = await safeJsonFetch<{ mesajlar: Mesaj[]; dahaVar: boolean }>(oda ? `/api/topluluk/sohbet/${oda}?once=${ilk}` : `/api/topluluk/mesajlar?kanal=${encodeURIComponent(kanal)}&once=${ilk}`);
    if (r.ok && r.data) { altta.current = false; setMesajlar((m) => [...r.data!.mesajlar, ...(m || [])]); setDahaVar(r.data.dahaVar); }
  };
  useLayoutEffect(() => { const el = liste.current; if (el && altta.current) el.scrollTop = el.scrollHeight; }, [mesajlar]);
  const kaydir = () => { const el = liste.current; if (el) altta.current = el.scrollHeight - el.scrollTop - el.clientHeight < 80; };

  const gonder = async () => {
    const t = metin.trim(); if (!t || gonderiyor) return;
    const gorunen = ad.trim() || (auth.currentUser?.displayName || getRememberedStudentInfo().name || 'Öğrenci').split(' ')[0];
    setGonderiyor(true); setHata('');
    const r = oda ? await post<{ mesaj: Mesaj }>(`/api/topluluk/sohbet/${oda}/mesaj`, { metin: t, yanitId: yanit?.id })
      : await post<{ mesaj: Mesaj }>('/api/topluluk/mesaj', { kanal, metin: t, ad: gorunen, yanitId: yanit?.id });
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
  const ozel = async (x: Mesaj) => {
    const r = await post<{ id: number }>('/api/topluluk/sohbet', { tur: 'dm', yazar: x.yazar, benAd: benimAd() });
    if (r.ok && r.data?.id) git(`/topluluk?sohbet=${r.data.id}`); else setHata((r.data as any)?.error || 'Sohbet açılamadı.');
  };
  const davet = async () => {
    if (!odaBilgi?.kod) return;
    const url = `${location.origin}/topluluk?katil=${odaBilgi.kod}`;
    try { await navigator.clipboard.writeText(url); setHata('Davet bağlantısı kopyalandı.'); } catch { setHata(url); }
  };
  const ayril = async () => {
    if (!oda || !confirm('Sohbetten ayrılınsın mı?')) return;
    const r = await post(`/api/topluluk/sohbet/${oda}/ayril`);
    if (r.ok) git('/topluluk?gorunum=sohbetler'); else setHata((r.data as any)?.error || 'Ayrılınamadı.');
  };
  const byId = useMemo(() => new Map((mesajlar || []).map((x) => [x.id, x])), [mesajlar]);

  return (
    <div className="tp15 tp15-s">
      {oda && odaBilgi && (
        <div className="tp15-odaust">
          <span className="v15-cap">{odaBilgi.uyeler.join(', ')}</span>
          {odaBilgi.kod && <button type="button" className="tp15-ib" onClick={davet} aria-label="Davet bağlantısını kopyala"><Link2 aria-hidden /></button>}
          <button type="button" className="tp15-ib" onClick={ayril} aria-label="Sohbetten ayrıl"><LogOut aria-hidden /></button>
        </div>
      )}
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
                {!oda && !x.benim && girisli && <button type="button" onClick={() => ozel(x)} aria-label="Özel mesaj gönder"><Mail aria-hidden /></button>}
                {x.benim || x.sikayet !== undefined ? <button type="button" onClick={() => sil(x)} aria-label="Sil"><Trash2 aria-hidden /></button>
                  : oda ? null : <button type="button" onClick={() => bildir(x)} aria-label="Uygunsuz olarak bildir"><Flag aria-hidden /></button>}
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
            {!ad && !oda && <input className="tp15-ad" value={ad} onChange={(e) => setAd(e.target.value.slice(0, 24))} placeholder="Görünen adın (isteğe bağlı)" aria-label="Görünen ad" />}
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
